"""Parse Jakana source code into a language-owned AST."""

import importlib
import re
from typing import List, Dict, Any, Tuple

from .ast import (
    AssignmentStatement,
    EchoStatement,
    ExpressionStatement,
    FunctionStatement,
    IfStatement,
    ImportStatement,
    Program,
    ReturnStatement,
    WhileStatement,
)
import builtins

from .transpiler import JakanaSyntaxError


USE_PATTERN = re.compile(r"use(?:\s+python|\s+cpp)?\s+([A-Za-z_0-9.]+)(?:\s+as\s+([A-Za-z_]\w*)|:\s+(.+))?$", re.IGNORECASE)
_BUILTINS = set(dir(builtins))
LET_PATTERN = re.compile(r"(?:let\s+)?([A-Za-z_]\w*)\s*=\s*(.+)$")
ECHO_PATTERN = re.compile(r"(?:echo|print)\s*(?:\((.*)\)|(.+))$")
FUNCTION_PATTERN = re.compile(r"(?:func|fn)\s+([A-Za-z_]\w*)\s*\(([^)]*)\)\s*(?::|\{)?\s*$")
IF_PATTERN = re.compile(r"if\s+(.+?)\s*(?::|\{)?\s*$")
WHILE_PATTERN = re.compile(r"while\s+(.+?)\s*(?::|\{)?\s*$")
RETURN_PATTERN = re.compile(r"return(?:\s+(.+))?$")

_MODULE_EXPORT_CACHE: Dict[str, List[str]] = {}


def get_module_exported_functions(mod_name: str) -> List[str]:
    """Dynamically inspect any Python standard library or third-party module for callable attributes."""
    if mod_name in _MODULE_EXPORT_CACHE:
        return _MODULE_EXPORT_CACHE[mod_name]

    DEFAULT_CATALOG = {
        "math": ["sqrt", "sin", "cos", "tan", "floor", "ceil", "log", "pow", "exp", "radians", "degrees", "pi", "e"],
        "numpy": ["array", "zeros", "ones", "sum", "mean", "std", "dot", "reshape"],
        "random": ["randint", "choice", "shuffle", "random", "uniform", "sample"],
        "os": ["getcwd", "listdir", "mkdir", "remove", "rename"],
        "json": ["dumps", "loads", "dump", "load"],
        "re": ["search", "match", "findall", "sub"],
        "requests": ["get", "post", "put", "delete"],
        "torch": ["tensor", "zeros", "ones", "randn", "matmul"],
        "time": ["sleep", "time"],
        "datetime": ["now", "today"],
    }

    funcs = list(DEFAULT_CATALOG.get(mod_name, []))

    try:
        mod = importlib.import_module(mod_name)
        for attr in dir(mod):
            if not attr.startswith("_") and attr not in funcs:
                try:
                    obj = getattr(mod, attr, None)
                    if callable(obj):
                        funcs.append(attr)
                except Exception:
                    pass
    except Exception:
        pass

    _MODULE_EXPORT_CACHE[mod_name] = funcs
    return funcs


def transform_pipeline(expr_str: str, known_free_functions: set) -> str:
    """Transform pipe expressions like `x |> f |> g` into nested function calls `g(f(x))` or method calls `f(x).g()`."""
    if "|>" not in expr_str:
        return expr_str

    prefix = ""
    target_str = expr_str
    
    # Handle let assignments or regular assignments
    if " = " in target_str:
        eq_idx = target_str.find(" = ")
        pipe_idx = target_str.find("|>")
        if pipe_idx == -1 or eq_idx < pipe_idx:
            prefix = target_str[:eq_idx + 3]
            target_str = target_str[eq_idx + 3:]

    # Handle echo/print
    if target_str.startswith("echo ") or target_str.startswith("print "):
        parts = target_str.split(" ", 1)
        prefix += parts[0] + " "
        target_str = parts[1]

    parts = [p.strip() for p in target_str.split("|>") if p.strip()]
    if len(parts) <= 1:
        return expr_str

    result = parts[0]
    for step in parts[1:]:
        if step in ("echo", "print"):
            result = f"echo({result})"
        elif "(" in step and step.endswith(")"):
            idx = step.find("(")
            fn_name = step[:idx]
            fn_args = step[idx+1:-1].strip()
            
            if fn_name in known_free_functions:
                if fn_args:
                    result = f"{fn_name}({result}, {fn_args})"
                else:
                    result = f"{fn_name}({result})"
            else:
                if fn_args:
                    result = f"{result}.{fn_name}({fn_args})"
                else:
                    result = f"{result}.{fn_name}()"
        else:
            if step in known_free_functions:
                result = f"{step}({result})"
            else:
                result = f"{result}.{step}()"

    if prefix and result.startswith("echo("):
        return result

    return prefix + result


def auto_qualify_modules(expr_str: str, imported_modules: List[str], selectively_imported: set) -> str:
    """Auto-prefix any Python module functions if imported via `use module` (e.g. randint -> random.randint)."""
    if not imported_modules:
        return expr_str

    result = expr_str
    for mod in imported_modules:
        funcs = get_module_exported_functions(mod)
        for fn in funcs:
            if fn in selectively_imported:
                continue
            pattern = r"(?<![A-Za-z0-9_.])" + fn + r"\("
            replacement = f"{mod}.{fn}("
            result = re.sub(pattern, replacement, result)

    return result


def join_multiline_statements(lines: List[str]) -> List[Tuple[int, str, str]]:
    """Join multiline statements such as pipeline operators starting with `|>`."""
    processed: List[Tuple[int, str, str]] = []
    current_line = ""
    current_raw = ""
    current_line_num = 1

    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("|>"):
            current_line += " " + line
            current_raw += " " + raw_line
        else:
            if current_line:
                processed.append((current_line_num, current_line, current_raw))
            current_line = line
            current_raw = raw_line
            current_line_num = line_number

    if current_line:
        processed.append((current_line_num, current_line, current_raw))

    return processed


def parse(source: str) -> Program:
    statements: List[Any] = []
    block_stack: List[Dict[str, Any]] = []
    imported_modules: List[str] = []
    selectively_imported = set()
    user_defined_functions = set()
    
    # Pre-parse to find user defined functions
    for line in source.splitlines():
        match = FUNCTION_PATTERN.fullmatch(line.strip())
        if match and not line.strip().startswith("echo") and not line.strip().startswith("print"):
            user_defined_functions.add(match.group(1))

    known_free_functions = set(_BUILTINS)
    known_free_functions.update(user_defined_functions)

    def add_statement(statement: Any) -> None:
        if block_stack:
            current_block = block_stack[-1]
            if current_block["type"] in ("function", "while"):
                current_block["body"].append(statement)
            elif current_block["type"] == "if":
                if current_block["current_branch"] == "then":
                    current_block["then_body"].append(statement)
                else:
                    current_block["else_body"].append(statement)
        else:
            statements.append(statement)

    logical_lines = join_multiline_statements(source.splitlines())

    for line_number, line, raw_line in logical_lines:
        # Import statements (`use <module>`) processed early to populate imported_modules
        use_match = USE_PATTERN.fullmatch(line)
        if use_match:
            module_name = use_match.group(1)
            alias = use_match.group(2)
            specific_names = use_match.group(3)
            
            names = None
            if specific_names:
                names = tuple(n.strip() for n in specific_names.split(","))
                selectively_imported.update(names)
                known_free_functions.update(names)
            else:
                imported_modules.append(module_name)
                known_free_functions.update(get_module_exported_functions(module_name))
                
            target = "python"
            if "cpp" in raw_line.lower():
                target = "cpp"
            add_statement(ImportStatement(module_name, alias, names, target, line_number))
            continue

        # Pipeline transformation & module auto-qualification
        line = transform_pipeline(line, known_free_functions)
        line = auto_qualify_modules(line, imported_modules, selectively_imported)

        # Closing braces or end keywords
        if line in ("}", "end", "}:", "else"):
            if line == "else":
                line = "else:"

        if line in ("else:", "} else {", "} else:"):
            if not block_stack or block_stack[-1]["type"] != "if":
                raise JakanaSyntaxError("unexpected else statement", line_number, expected="matching if statement", found=line)
            if block_stack[-1]["current_branch"] == "else":
                raise JakanaSyntaxError("multiple else blocks in single if statement", line_number, expected="end or } after else block", found=line)
            block_stack[-1]["current_branch"] = "else"
            continue

        if line in ("}", "end"):
            if not block_stack:
                raise JakanaSyntaxError("unexpected end of block", line_number, expected="a valid statement", found=line)
            block = block_stack.pop()
            if block["type"] == "function":
                add_statement(FunctionStatement(
                    block["name"],
                    block["parameters"],
                    tuple(block["body"]),
                    block["line"],
                ))
            elif block["type"] == "if":
                add_statement(IfStatement(
                    block["condition"],
                    tuple(block["then_body"]),
                    tuple(block["else_body"]),
                    block["line"],
                ))
            elif block["type"] == "while":
                add_statement(WhileStatement(
                    block["condition"],
                    tuple(block["body"]),
                    block["line"],
                ))
            continue

        # Function definitions (`fn name(...) {` or `name(...):`)
        function_match = FUNCTION_PATTERN.fullmatch(line)
        if function_match and not line.startswith("echo") and not line.startswith("print") and not line.startswith("return"):
            fn_name = function_match.group(1)
            raw_params = function_match.group(2)
            params = tuple(p.strip() for p in raw_params.split(",") if p.strip())
            block_stack.append({
                "type": "function",
                "name": fn_name,
                "parameters": params,
                "body": [],
                "line": line_number,
            })
            continue

        # If statements (`if cond {` or `if cond:`)
        if_match = IF_PATTERN.fullmatch(line)
        if if_match and not line.startswith("echo") and not line.startswith("print"):
            block_stack.append({
                "type": "if",
                "condition": if_match.group(1).rstrip("{:").strip(),
                "then_body": [],
                "else_body": [],
                "current_branch": "then",
                "line": line_number,
            })
            continue

        # While loops (`while cond {` or `while cond:`)
        while_match = WHILE_PATTERN.fullmatch(line)
        if while_match:
            block_stack.append({
                "type": "while",
                "condition": while_match.group(1).rstrip("{:").strip(),
                "body": [],
                "line": line_number,
            })
            continue

        # Output (`echo expr` or `echo(expr)`)
        echo_match = ECHO_PATTERN.fullmatch(line)
        if echo_match:
            expr = echo_match.group(1) or echo_match.group(2)
            add_statement(EchoStatement(expr.strip(), line_number))
            continue

        # Return statements
        return_match = RETURN_PATTERN.fullmatch(line)
        if return_match:
            expr = return_match.group(1) or ""
            add_statement(ReturnStatement(expr.strip(), line_number))
            continue

        # Assignments (`let x = expr` or `x = expr`)
        let_match = LET_PATTERN.fullmatch(line)
        if let_match and not line.startswith("if ") and not line.startswith("while "):
            var_name = let_match.group(1)
            expr = let_match.group(2)
            is_let = line.startswith("let ")
            add_statement(AssignmentStatement(var_name, expr, line_number, is_let=is_let))
            continue

        # General expression statements
        add_statement(ExpressionStatement(line, line_number))

    if block_stack:
        block = block_stack[-1]
        kind = block["type"]
        name = block.get("name", kind)
        raise JakanaSyntaxError(f"missing closing brace '}}' or 'end' for {kind} {name} opened here", block["line"], expected="}", found="end of file")

    return Program(tuple(statements))