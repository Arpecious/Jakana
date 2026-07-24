"""C++ backend generator for the Jakana AST."""

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
    """Generate C++ source code from a Jakana AST program."""
    includes = ["#include <iostream>"]
    output = []

    def generate_statement(statement: object, indent: str = "    ") -> None:
        if isinstance(statement, AssignmentStatement):
            output.append(f"{indent}auto {statement.name} = {statement.expression};")
        elif isinstance(statement, EchoStatement):
            output.append(f"{indent}std::cout << ({statement.expression}) << std::endl;")
        elif isinstance(statement, ReturnStatement):
            if statement.expression:
                output.append(f"{indent}return {statement.expression};")
            else:
                output.append(f"{indent}return;")
        elif isinstance(statement, ExpressionStatement):
            output.append(f"{indent}{statement.expression};")
        elif isinstance(statement, ImportStatement):
            if statement.names:
                names_str = ", ".join(statement.names)
                includes.append(f"// Imported module: {statement.module} (symbols: {names_str})")
            else:
                includes.append(f"// Imported module: {statement.module}")
        elif isinstance(statement, FunctionStatement):
            params = ", ".join(f"auto {p}" for p in statement.parameters)
            output.append(f"{indent}auto {statement.name} = []({params}) {{")
            if statement.body:
                for body_stmt in statement.body:
                    generate_statement(body_stmt, indent + "    ")
            output.append(f"{indent}}};")
        elif isinstance(statement, IfStatement):
            output.append(f"{indent}if ({statement.condition}) {{")
            if statement.then_body:
                for body_stmt in statement.then_body:
                    generate_statement(body_stmt, indent + "    ")
            output.append(f"{indent}}}")
            if statement.else_body:
                output.append(f"{indent}else {{")
                for body_stmt in statement.else_body:
                    generate_statement(body_stmt, indent + "    ")
                output.append(f"{indent}}}")
        elif isinstance(statement, WhileStatement):
            output.append(f"{indent}while ({statement.condition}) {{")
            if statement.body:
                for body_stmt in statement.body:
                    generate_statement(body_stmt, indent + "    ")
            output.append(f"{indent}}}")
        else:
            raise TypeError(f"Unsupported C++ Jakana AST node: {type(statement).__name__}")

    for statement in program.statements:
        generate_statement(statement)

    cpp_code = []
    cpp_code.extend(includes)
    cpp_code.append("\nint main() {")
    cpp_code.extend(output)
    cpp_code.append("    return 0;\n}")

    return "\n".join(cpp_code) + "\n"
