"""Language-owned abstract syntax tree nodes."""

from dataclasses import dataclass
from typing import Optional, Tuple, Any


@dataclass(frozen=True)
class Program:
    statements: Tuple[Any, ...]


@dataclass(frozen=True)
class AssignmentStatement:
    name: str
    expression: str
    line: int
    is_let: bool = False


# Backward compatibility alias
LetStatement = AssignmentStatement


@dataclass(frozen=True)
class EchoStatement:
    expression: str
    line: int


# Backward compatibility alias
PrintStatement = EchoStatement


@dataclass(frozen=True)
class ReturnStatement:
    expression: str
    line: int


@dataclass(frozen=True)
class FunctionStatement:
    name: str
    parameters: Tuple[str, ...]
    body: Tuple[Any, ...]
    line: int


@dataclass(frozen=True)
class ImportStatement:
    module: str
    alias: Optional[str]
    names: Optional[Tuple[str, ...]]
    target: str
    line: int


@dataclass(frozen=True)
class IfStatement:
    condition: str
    then_body: Tuple[Any, ...]
    else_body: Tuple[Any, ...]
    line: int


@dataclass(frozen=True)
class WhileStatement:
    condition: str
    body: Tuple[Any, ...]
    line: int


@dataclass(frozen=True)
class ExpressionStatement:
    expression: str
    line: int