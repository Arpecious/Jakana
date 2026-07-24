"""Python code generation backend for the Jakana AST."""

from ..ast import (
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


def generate(program: Program) -> str:
    """Generate clean, idiomatic Python code from a Jakana program AST."""
    output = []

    def generate_statement(statement: object, indent: str = "") -> None:
        if isinstance(statement, AssignmentStatement):
            output.append(f"{indent}{statement.name} = {statement.expression}")
        elif isinstance(statement, EchoStatement):
            output.append(f"{indent}print({statement.expression})")
        elif isinstance(statement, ReturnStatement):
            if statement.expression:
                output.append(f"{indent}return {statement.expression}")
            else:
                output.append(f"{indent}return")
        elif isinstance(statement, ImportStatement):
            if statement.names:
                names_str = ", ".join(statement.names)
                output.append(f"{indent}from {statement.module} import {names_str}")
            elif statement.alias:
                output.append(f"{indent}import {statement.module} as {statement.alias}")
            else:
                output.append(f"{indent}import {statement.module}")
        elif isinstance(statement, ExpressionStatement):
            output.append(f"{indent}{statement.expression}")
        elif isinstance(statement, FunctionStatement):
            parameters = ", ".join(statement.parameters)
            output.append(f"{indent}def {statement.name}({parameters}):")
            if statement.body:
                for body_statement in statement.body:
                    generate_statement(body_statement, indent + "    ")
            else:
                output.append(f"{indent}    pass")
        elif isinstance(statement, IfStatement):
            output.append(f"{indent}if {statement.condition}:")
            if statement.then_body:
                for body_statement in statement.then_body:
                    generate_statement(body_statement, indent + "    ")
            else:
                output.append(f"{indent}    pass")
            if statement.else_body:
                output.append(f"{indent}else:")
                for body_statement in statement.else_body:
                    generate_statement(body_statement, indent + "    ")
        elif isinstance(statement, WhileStatement):
            output.append(f"{indent}while {statement.condition}:")
            if statement.body:
                for body_statement in statement.body:
                    generate_statement(body_statement, indent + "    ")
            else:
                output.append(f"{indent}    pass")
        else:
            raise TypeError(f"Unsupported Jakana AST node: {type(statement).__name__}")

    for statement in program.statements:
        generate_statement(statement)

    return "\n".join(output) + ("\n" if output else "")