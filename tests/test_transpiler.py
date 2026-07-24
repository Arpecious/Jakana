import unittest

from jakana.ast import FunctionStatement, AssignmentStatement, EchoStatement, ReturnStatement, ImportStatement, IfStatement, WhileStatement
from jakana.cli import format_natural_error
from jakana.parser import parse
from jakana.transpiler import JakanaSyntaxError, transpile


class TranspilerTests(unittest.TestCase):
    def test_transpiles_user_exact_phase1_example(self):
        source = (
            "use math\n"
            "number = 25\n"
            "root = sqrt(number)\n"
            "echo root\n"
            "if root == 5 {\n"
            '    echo "Verified"\n'
            "}\n"
            "fn square(x) {\n"
            "    return x * x\n"
            "}\n"
            "echo square(5)\n"
            "[1,2,3,4,5]\n"
            "    |> sum\n"
            "    |> echo\n"
        )
        expected = (
            "import math\n"
            "number = 25\n"
            "root = math.sqrt(number)\n"
            "print(root)\n"
            "if root == 5:\n"
            '    print("Verified")\n'
            "def square(x):\n"
            "    return x * x\n"
            "print(square(5))\n"
            "print(sum([1,2,3,4,5]))\n"
        )
        self.assertEqual(transpile(source), expected)

    def test_format_natural_error_diagnostic(self):
        err = NameError("name 'undefined_var' is not defined")
        report = format_natural_error("test.jk", err, ["echo undefined_var"])
        self.assertIn("[Jakana Natural Diagnostic Error]", report)
        self.assertIn("The identifier 'undefined_var' is referenced before being defined.", report)
        self.assertIn("How to fix it:", report)

    def test_transpiles_multiline_pipeline_operator(self):
        source = "[1, 2, 3, 4, 5]\n    |> sum\n    |> echo"
        expected = "print(sum([1, 2, 3, 4, 5]))\n"
        self.assertEqual(transpile(source), expected)

    def test_transpiles_variables_and_echo(self):
        source = 'greeting = "Hello"\necho greeting'
        self.assertEqual(transpile(source), 'greeting = "Hello"\nprint(greeting)\n')

    def test_ignores_blank_lines_and_comments(self):
        self.assertEqual(transpile("# comment\n\nvalue = 42\n"), "value = 42\n")

    def test_transpiles_use_import(self):
        source = "use math\nuse numpy as np\nres = math.sqrt(25)"
        expected = "import math\nimport numpy as np\nres = math.sqrt(25)\n"
        self.assertEqual(transpile(source), expected)

    def test_transpiles_if_else_and_while_braces(self):
        source = "x = 10\nif x > 5 {\n    echo x\n} else {\n    echo 0\n}\nwhile x > 0 {\n    x = x - 1\n}"
        expected = "x = 10\nif x > 5:\n    print(x)\nelse:\n    print(0)\nwhile x > 0:\n    x = x - 1\n"
        self.assertEqual(transpile(source), expected)

    def test_transpiles_to_cpp(self):
        source = 'use iostream\nmsg = "Hello Jakana"\necho msg'
        output = transpile(source, target="cpp")
        self.assertIn("#include <iostream>", output)
        self.assertIn("auto msg = \"Hello Jakana\";", output)
        self.assertIn("std::cout << (msg) << std::endl;", output)


if __name__ == "__main__":
    unittest.main()