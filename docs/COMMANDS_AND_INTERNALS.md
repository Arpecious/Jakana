# Jakana Commands & Architecture Internals

This document provides a deep technical reference of all **Jakana** CLI commands, internal compiler pipeline functions, AST structure, and backend dispatch mechanisms.

---

## 1. CLI Commands Reference

The Jakana CLI entry point is defined in [`src/jakana/cli.py`](file:///c:/Users/aryan/OneDrive/Desktop/Jakana-lang/src/jakana/cli.py).

### Command 1: `jakana --version`
- **Purpose**: Displays the installed Jakana release version.
- **Under the Hood**:
  - `argparse` matches `--version`.
  - Reads `jakana.__version__` defined in `src/jakana/__init__.py`.
  - Prints `1.0.0` and exits.

### Command 2: `jakana run <file.jk>`
- **Purpose**: Parses, compiles, and executes a Jakana program immediately.
- **Under the Hood**:
  1. Opens `<file.jk>` and reads UTF-8 text.
  2. Calls `jakana.parser.parse(source)` to produce a `Program` AST object.
  3. Calls `jakana.transpiler.transpile(source, target="python")`.
  4. Passes the generated Python source string to `compile(python_source, filename, "exec")`.
  5. Executes the compiled bytecode in an isolated scope using `exec()`.

### Command 3: `jakana transpile <file.jk> [--target python|cpp]`
- **Purpose**: Converts Jakana source code into target language code (Python or C++) without executing it.
- **Under the Hood**:
  1. Calls `jakana.parser.parse(source)` -> `Program(statements)`.
  2. Dispatches to target backend:
     - `target="python"` calls `jakana.backends.python.generate(program)`.
     - `target="cpp"` calls `jakana.backends.cpp.generate(program)`.
  3. Prints generated source code to standard output (`stdout`).

### Command 4: `jakana debug <file.jk>`
- **Purpose**: Launches an interactive step-by-step debugger for Jakana programs.
- **Under the Hood**:
  1. Parses source into `Program` AST.
  2. Instantiates `Debugger(program, source_lines)` from [`src/jakana/debugger.py`](file:///c:/Users/aryan/OneDrive/Desktop/Jakana-lang/src/jakana/debugger.py).
  3. Pauses execution before each statement AST node, matching line numbers to original `.jk` source lines.
  4. Responds to debugger commands: `next`, `continue`, `break LINE`, `print EXPR`, `locals`.

---

## 2. Compiler Pipeline & Internal Functions

The Jakana compiler follows a strict 4-stage pipeline:

```text
Jakana Source Code (.jk)
       │
       ▼
   [1. Parser] ────▶ jakana.parser.parse(source)
       │
       ▼
   [2. AST] ───────▶ jakana.ast.Program
       │
       ▼
   [3. Backend] ───▶ jakana.backends.python.generate() OR jakana.backends.cpp.generate()
       │
       ▼
   [4. Execution] ─▶ Python exec() OR C++ Compiler (g++/clang++)
```

### Stage 1: Parser (`src/jakana/parser.py`)
- **Main Function**: `parse(source: str) -> Program`
- **Internal Helper**: `add_statement(statement: object)` manages nested blocks (`function`, `if`, `while`).
- **Data Structure**: `block_stack` keeps track of open control structures expecting `end` markers.

### Stage 2: Abstract Syntax Tree (`src/jakana/ast.py`)
Represented as frozen dataclasses:
- `Program(statements)`
- `LetStatement(name, expression, line)`
- `PrintStatement(expression, line)`
- `ReturnStatement(expression, line)`
- `FunctionStatement(name, parameters, body, line)`
- `ImportStatement(target, module, alias, line)`
- `IfStatement(condition, then_body, else_body, line)`
- `WhileStatement(condition, body, line)`
- `ExpressionStatement(expression, line)`

### Stage 3: Python Backend (`src/jakana/backends/python.py`)
- **Main Function**: `generate(program: Program) -> str`
- **Internal Helper**: `generate_statement(statement, indent="")` recurses over AST nodes and converts them to valid Python statements.

### Stage 4: C++ Backend (`src/jakana/backends/cpp.py`)
- **Main Function**: `generate(program: Program) -> str`
- **Internal Helper**: Converts AST nodes to C++ lambdas, auto type declarations, and `std::cout` streams inside `main()`.

---

## 3. Function Call Graph

```text
jakana.cli.main()
   ├── parse() [parser.py]
   │      ├── Regex matching (USE, LET, PRINT, FUNCTION, IF, WHILE)
   │      └── Constructs AST nodes (ast.py)
   │
   ├── transpile() [transpiler.py]
   │      ├── python.generate() [backends/python.py]
   │      └── cpp.generate() [backends/cpp.py]
   │
   └── exec() (Built-in Python execution engine)
```
