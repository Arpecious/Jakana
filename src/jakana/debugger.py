"""Interactive source-level debugger for the current Jakana AST."""

from dataclasses import dataclass, field
from typing import Callable, TextIO

from .ast import FunctionStatement, LetStatement, PrintStatement, Program, ReturnStatement


class DebuggerExit(Exception):
    """Raised when the user ends a debug session."""


class FunctionReturn(Exception):
    def __init__(self, value: object):
        self.value = value


@dataclass
class Debugger:
    program: Program
    source_lines: list[str]
    breakpoints: set[int] = field(default_factory=set)
    input_stream: TextIO | None = None
    output_stream: TextIO | None = None
    _step_mode: bool = True
    _environment: dict[str, object] = field(default_factory=dict)

    def start(self) -> None:
        """Start an interactive debug session."""
        self.input_stream = self.input_stream or __import__("sys").stdin
        self.output_stream = self.output_stream or __import__("sys").stdout
        self._write("Jakana debugger started. Type 'help' for commands.")
        try:
            self._execute_statements(self.program.statements)
        except DebuggerExit:
            self._write("Debugging stopped.")

    def _write(self, text: str) -> None:
        print(text, file=self.output_stream)

    def _execute_statements(self, statements: tuple[object, ...], environment: dict[str, object] | None = None) -> None:
        previous_environment = self._environment
        if environment is not None:
            self._environment = environment
        try:
            for statement in statements:
                self._before_statement(statement)
                if isinstance(statement, LetStatement):
                    self._environment[statement.name] = self._evaluate(statement.expression)
                elif isinstance(statement, PrintStatement):
                    self._write(str(self._evaluate(statement.expression)))
                elif isinstance(statement, FunctionStatement):
                    self._environment[statement.name] = self._make_function(statement)
                elif isinstance(statement, ReturnStatement):
                    raise FunctionReturn(self._evaluate(statement.expression))
        finally:
            self._environment = previous_environment

    def _make_function(self, statement: FunctionStatement) -> Callable[..., object]:
        def call(*arguments: object) -> object:
            if len(arguments) != len(statement.parameters):
                raise TypeError(
                    f"{statement.name} expected {len(statement.parameters)} arguments, got {len(arguments)}"
                )
            function_environment = dict(zip(statement.parameters, arguments))
            function_environment.update({name: value for name, value in self._environment.items() if callable(value)})
            try:
                self._execute_statements(statement.body, function_environment)
            except FunctionReturn as returned:
                return returned.value
            return None

        return call

    def _evaluate(self, expression: str) -> object:
        return eval(expression, {"__builtins__": {}}, self._environment)

    def _before_statement(self, statement: object) -> None:
        line = getattr(statement, "line", None)
        if line is None or (line not in self.breakpoints and not self._step_mode):
            return
        self._step_mode = False
        source = self.source_lines[line - 1].strip() if line <= len(self.source_lines) else ""
        self._write(f"Paused at line {line}: {source}")
        self._command_loop()

    def _command_loop(self) -> None:
        while True:
            self.output_stream.write("(jakana-debug) ")
            self.output_stream.flush()
            command = self.input_stream.readline()
            if not command:
                raise DebuggerExit()
            parts = command.strip().split(maxsplit=1)
            name = parts[0] if parts else ""
            argument = parts[1] if len(parts) == 2 else ""
            if name in {"continue", "c"}:
                return
            if name in {"next", "step", "s"}:
                self._step_mode = True
                return
            if name in {"break", "b"}:
                try:
                    line = int(argument)
                except ValueError:
                    self._write("Usage: break LINE")
                    continue
                self.breakpoints.add(line)
                self._write(f"Breakpoint set at line {line}")
                continue
            if name in {"print", "p"}:
                try:
                    self._write(repr(self._evaluate(argument)))
                except Exception as error:
                    self._write(f"Cannot evaluate {argument!r}: {error}")
                continue
            if name in {"locals", "l"}:
                self._write(repr(self._environment))
                continue
            if name in {"help", "h", "?"}:
                self._write("Commands: break LINE, continue, next, print EXPR, locals, quit")
                continue
            if name in {"quit", "q", "exit"}:
                raise DebuggerExit()
            self._write("Unknown command. Type 'help'.")