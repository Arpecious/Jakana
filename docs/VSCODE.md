# VS Code Support

Jakana files use the `.jk` extension. Syntax highlighting comes from the local extension in `editors/vscode-jakana`.

## Current setup

The compiler and editor support are separate:

- `jakana run file.jk` executes a Jakana file.
- The VS Code extension recognizes `.jk` and highlights Jakana syntax.

## Enable highlighting

1. Open the `editors/vscode-jakana` folder in VS Code.
2. Press `F5`.
3. In the new Extension Development Host window, open this project's `examples/hello.jk`.

The extension highlights:

- Jakana keywords such as `let`, `fn`, `if`, `return`, and `use`
- Python interop words such as `python`
- strings and numbers
- comments beginning with `#`
- operators and built-in `print`

If a `.jk` file is still shown as Plain Text, use the language selector in the bottom-right of VS Code, choose **Jakana**, and reload the Extension Development Host.

## Jakana file icon

File icons are controlled by the active VS Code icon theme. To replace the default Python-looking icon for `.jk` files:

1. Run **Preferences: File Icon Theme** from the Command Palette.
2. Select **Jakana File Icons**.
3. Open or create a `.jk` file.

The icon theme is included in the Jakana extension and maps the `.jk` extension to the Jakana red-to-light-orange bird mark.
