# Jakana 1 Roadmap

Jakana is a unified, readable programming language that begins with Python interoperability and can grow toward additional backends.

## Version policy

Jakana follows Semantic Versioning during its first generation:

- `1.0.0`: first stable language release
- `1.x.0`: backward-compatible language or tooling features
- `1.x.y`: backward-compatible bug fixes
- `2.0.0`: breaking language or runtime changes

The `1.x` series is the complete first generation of Jakana. Once `1.0.0` is released, existing Jakana 1 programs should continue to work across compatible `1.x` releases.

## Milestones

### Step 0: Project foundation - complete

- Choose the implementation language and project layout.
- Define the command-line interface: `jakana run file.jk`.
- Add a version command: `jakana --version`.
- Add a test command and continuous integration.

### Step 1: First executable slice - bootstrap complete

Support a small Jakana program containing:

- comments
- string and number values
- variables with `let`
- output with `print`
- basic expressions

Example:

```jakana
let message = "Hello from Jakana"
print(message)
```

The initial prototype runs this program successfully. It is a bootstrap backend only and is not the definition of Jakana.

### Step 1.5: Shared language frontend - initial slice complete

- define Jakana tokens and grammar
- implement a language-owned lexer
- implement a language-owned parser and AST
- add semantic validation and source-location errors
- make the Python backend consume the AST
- keep the AST independent of Python, C++, JavaScript, and Java

The initial parser, AST, and Python backend are now implemented for `let` and `print`.

### Step 2: Core control flow - functions initial slice complete

- functions with `name(parameters): ... end` and `return`
- `if` and `else`
- `for` and `while`
- `return`
- useful error messages with source locations

### Step 3: Python backend and interoperability

- import Python modules through explicit `use python` syntax
- call Python functions
- use Python values from Jakana
- expose a clear boundary for Python exceptions
- support installed Python packages without rewriting them

### Step 3.5: Additional backends

- define backend compatibility tests
- add a C++ backend for native and performance-sensitive programs
- add a JavaScript backend for web programs
- add a Java backend for JVM programs
- preserve the same Jakana source syntax and semantics across targets

Example:

```jakana
use python math

print(math.sqrt(16))
```

### Step 4: Modules and packages

- project configuration file
- local module imports
- dependency metadata
- initial package registry and `jakana add`

### Step 5: Developer experience

- formatter
- syntax highlighting
- language server diagnostics
- debugger integration - initial CLI debugger complete
- beginner and migration documentation

### Step 6: Jakana 1.0.0

Release only after the core syntax, Python interoperability, error messages, documentation, and compatibility rules are tested and documented.

## Design rules for Jakana 1

1. Keep the core language small and readable.
2. Prefer predictable behavior over clever syntax.
3. Preserve access to Python instead of rebuilding its ecosystem.
4. Make compiler errors useful to beginners and precise for experienced developers.
5. Avoid breaking syntax changes during the `1.x` series.

## Immediate next task

Complete Step 1.5 before expanding the language. Then add functions and control flow to the shared Jakana AST, implement Python imports, and begin the additional backends only after the Python path is useful.