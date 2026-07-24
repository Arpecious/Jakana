# Jakana Python Backend

Jakana 1 uses Python as its first backend. Jakana source is parsed into a Jakana AST, and the Python backend generates Python from that AST.

```text
Jakana source -> parser -> Jakana AST -> Python backend -> Python execution
```

Python is the first execution target and ecosystem bridge. Python syntax does not define Jakana syntax.

## CLI commands

### Show the Jakana version

```powershell
jakana --version
```

The command calls `jakana.cli:main`, and the version is read from `jakana.__version__`.

Current result:

```text
1.0.0
```

### Run a Jakana file

```powershell
jakana run model.jk
```

The command performs these operations:

1. Read `model.jk` as UTF-8 text.
2. Reject the file if it is empty.
3. Parse the source into a Jakana `Program` AST.
4. Generate Python source from the AST.
5. Compile and execute the generated Python.

Equivalent development command:

```powershell
$env:PYTHONPATH = "src"
python -m jakana.cli run model.jk
```

Repository-local Windows fallback:

```powershell
.\run.ps1 model.jk
```

### Show generated Python

```powershell
jakana transpile model.jk
```

This parses Jakana and prints the generated Python without executing it.

For example, this Jakana source:

```jakana
let message = "Hello from Jakana"
print(message)
```

currently generates:

```python
message = "Hello from Jakana"
print(message)
```

## Current Jakana syntax mapping

### Comments

Jakana:

```jakana
# This line is ignored
```

Python result:

```python
# No Python statement is generated.
```

A comment must begin the line after optional whitespace. Inline comments are not yet part of the supported grammar.

### Variables with `let`

Jakana:

```jakana
let name = "Jakana"
let count = 3
```

AST representation:

```text
Program
  LetStatement(name="name", expression="\"Jakana\"")
  LetStatement(name="count", expression="3")
```

Python result:

```python
name = "Jakana"
count = 3
```

`let` is Jakana syntax. The Python backend emits an assignment because Python has no equivalent `let` declaration in this backend.

Supported variable names begin with a letter or underscore and may contain letters, numbers, and underscores.

### Output with `print`

Jakana:

```jakana
print(name)
print("Hello")
```

Python result:

```python
print(name)
print("Hello")
```

Whitespace between `print` and `(` is allowed:

```jakana
print (name)
```

The backend normalizes this to:

```python
print(name)
```

### Expressions

The current backend passes basic expressions through to Python:

```jakana
let total = 2 + 3
print(total)
```

Generated Python:

```python
total = 2 + 3
print(total)
```

Expression validation is still being expanded. A future Jakana semantic layer will define expression rules independently of Python.

## AST-to-Python backend API

The backend can also be called from Python code:

```python
from jakana.backends.python import generate
from jakana.parser import parse

source = 'let message = "Hello"\nprint(message)'
program = parse(source)
python_source = generate(program)
print(python_source)
```

The important separation is:

- `jakana.parser.parse()` owns Jakana parsing.
- `jakana.ast` owns Jakana program structures.
- `jakana.backends.python.generate()` owns Python code generation.
- `jakana.cli` owns command-line behavior.

A future C++, JavaScript, or Java backend should implement the same backend contract against the same Jakana AST.

## Python interoperability plan

Python packages will be available through explicit Jakana syntax rather than accidental Python imports:

```jakana
use python math

let result = math.sqrt(25)
print(result)
```

The planned backend behavior is equivalent to:

```python
import math

result = math.sqrt(25)
print(result)
```

This feature is planned and is not yet implemented in the current parser.

Jakana should use installed Python libraries directly instead of rewriting every library. This is how Jakana can access AI, scientific, web, automation, and data ecosystems quickly.

## Current limitations

The Python backend currently supports:

- comments on their own lines
- `let` variable declarations
- string and number expressions accepted by the bootstrap backend
- `print(...)`
- execution through the installed `jakana` command

The following are planned next:

- a dedicated lexer
- expression AST nodes
- semantic validation
- `use python` imports
- functions and `return`
- `if` and `else`
- loops
- Python exception boundaries
- backend compatibility tests
