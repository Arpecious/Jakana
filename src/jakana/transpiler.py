"""API for transpiling Jakana source code to target backends (Python, C++)."""


class JakanaSyntaxError(ValueError):
    """Raised when source is outside the supported Jakana syntax."""

    def __init__(self, message: str, line: int | None = None, expected: str | None = None, found: str | None = None):
        super().__init__(message)
        self.line = line
        self.expected = expected
        self.found = found


def transpile(source: str, target: str = "python") -> str:
    """Parse Jakana and generate target backend source code (Python or C++)."""
    from .parser import parse

    program = parse(source)
    if target.lower() in ("cpp", "c++"):
        from .backends.cpp import generate as generate_cpp
        return generate_cpp(program)
    else:
        from .backends.python import generate as generate_python
        return generate_python(program)