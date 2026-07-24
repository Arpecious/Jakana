# Jakana 1 Architecture

Jakana is a unified programming language with several execution backends. Python is the first backend because it gives Jakana immediate access to a mature ecosystem. Python remains an implementation target and interoperability boundary, not the language definition.

## Compiler pipeline

Every Jakana backend must begin with the same language-owned pipeline:

```text
Jakana source
    -> lexer
    -> Jakana parser
    -> Jakana abstract syntax tree
    -> semantic analysis
    -> selected backend
```

The first backend emits or executes through Python. Later backends can target C++, JavaScript, and Java. Every backend consumes the same Jakana AST and follows the same language rules.

## Language-owned components

- **Lexer:** recognizes Jakana tokens and reports source locations.
- **Parser:** defines Jakana grammar and builds Jakana AST nodes.
- **AST:** represents Jakana concepts independently of Python, JavaScript, or C++.
- **Semantic analysis:** checks names, types, scopes, imports, and valid control flow.
- **Runtime contract:** defines values, functions, modules, errors, and standard behavior.
- **Backends:** translate the checked AST to a target or execute it through a Jakana runtime.

## Backend strategy

1. Build the Python backend first and make it useful.
2. Support Python packages through explicit `use python` imports instead of reimplementing them.
3. Add a C++ backend for performance and systems programming.
4. Add a JavaScript backend for web applications.
5. Add a Java backend for JVM ecosystems.
6. Add a native Jakana runtime only when real use cases justify its cost.

## Unified style principles

- One grammar across every backend.
- One standard library interface where practical.
- Explicit interop syntax instead of accidental target-language syntax.
- Predictable values and errors across platforms.
- No requirement that Jakana users learn Python, JavaScript, or C++ to use core Jakana.

## Bootstrap boundary

Jakana `1.0.0` currently has a small Python-backed implementation with a language-owned AST, parser, and Python code-generation backend. It supports `let` and `print` so language design can be tested with executable programs. The next implementation work is semantic validation, expressions, and Python imports.

## Python ecosystem

Jakana should not copy or rewrite every Python library. A Python-backed Jakana program should be able to use installed Python packages directly:

```jakana
use python math

let result = math.sqrt(25)
print(result)
```

This gives Jakana access to scientific computing, AI, automation, web, and data libraries immediately.
