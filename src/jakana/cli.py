""Command-line interface for Jakana.""

import argparse
import sys
from pathlib import Path

from . import __version__
from .debugger import Debugger
from .parser import parse
from .transpiler import JakanaSyntaxError, transpile


def format_natural_error(filename: str, error: Exception, source_lines: list) -> str:
    """Format backend/runtime errors into natural language frontend Jakana diagnostic suggestions."""
    line_num = getattr(error, "lineno", None)
    error_msg = str(error)

    explanation = ""
    fix_suggestion = ""

    if isinstance(error, SyntaxError):
        explanation = f"Jakana detected code syntax structure that cannot be executed (Line {line_num or '?'}: {error_msg})."
        fix_suggestion = "Check that every opening brace '{' has a matching closing brace '}', and function declarations use 'fn name(params) { ... }'."
    elif isinstance(error, NameError):
        var_name = error_msg.split("'")[1] if "'" in error_msg else error_msg
        explanation = f"The identifier '{var_name}' is referenced before being defined."
        fix_suggestion = f"Define '{var_name}' before using it (e.g. {var_name} = value) or import its library using 'use <module>'."
    elif isinstance(error, TypeError):
        explanation = f"Invalid type operation: {error_msg}."
        fix_suggestion = "Ensure arguments passed to functions or arithmetic operations match expected types."
    elif isinstance(error, AttributeError):
        explanation = f"Module or object property error: {error_msg}."
        fix_suggestion = "Check function name spelling or verify that the required module was imported using 'use <module>'."
    elif isinstance(error, ZeroDivisionError):
        explanation = "Division by zero detected."
        fix_suggestion = "Ensure denominator values are non-zero before dividing."
    else:
        explanation = f"Execution error: {error_msg}."
        fix_suggestion = "Review the source line for logical errors or missing dependencies."

    code_snippet = ""
    if line_num and 1 <= line_num <= len(source_lines):
        code_snippet = f"\n  Source Code Line {line_num}:\n    {source_lines[line_num - 1].strip()}\n"

    report = (
        f"  [Jakana Natural Diagnostic Error]\n"
        f"  File : {filename}\n"
        f"  Line : {line_num or 'N/A'}\n"
        f"-------------------------------------------------------\n"
        f"  What went wrong:\n"
        f"    {explanation}\n"
        f"{code_snippet}"
        f"  How to fix it:\n"
        f"    -> {fix_suggestion}\n"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(prog="jakana")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)

    run_command = commands.add_parser("run", help="run a Jakana file")
    run_command.add_argument("file", type=Path)

    transpile_command = commands.add_parser("transpile", help="transpile a Jakana file to target backend (python/cpp)")
    transpile_command.add_argument("file", type=Path)
    transpile_command.add_argument("--target", "-t", default="python", choices=["python", "cpp", "c++"], help="target backend target language")

    debug_command = commands.add_parser("debug", help="debug a Jakana file")
    debug_command.add_argument("file", type=Path)

    arguments = parser.parse_args()
    if not arguments.file.is_file():
        parser.error(f"{arguments.file}: file not found; use examples/{arguments.file.name} from the project root")
    source = arguments.file.read_text(encoding="utf-8")
    source_lines = source.splitlines()

    if not source.strip():
        parser.error(f"{arguments.file}: file is empty; save the file before running it")

    try:
        program = parse(source)
        target = getattr(arguments, "target", "python")
        generated_source = transpile(source, target=target)
    except JakanaSyntaxError as error:
        location = f":{error.line}" if error.line is not None else ""
        print(f"\n[Jakana Syntax Error] {arguments.file}{location}\n  Problem: {error}", file=sys.stderr)
        if error.expected:
            print(f"  Expected: {error.expected}", file=sys.stderr)
        if error.found:
            print(f"  Found   : {error.found}", file=sys.stderr)
        print("  How to fix it:\n    -> Check your block braces '{ ... }' and statement syntax.\n", file=sys.stderr)
        raise SystemExit(2)

    if arguments.command == "transpile":
        print(generated_source, end="")
    elif arguments.command == "debug":
        Debugger(program, source_lines).start()
    else:
        python_source = transpile(source, target="python")
        try:
            compiled_code = compile(python_source, str(arguments.file), "exec")
            exec(compiled_code, {})
        except Exception as error:
            print(format_natural_error(str(arguments.file), error, source_lines), file=sys.stderr)
            raise SystemExit(1)


if __name__ == "__main__":
    main()
