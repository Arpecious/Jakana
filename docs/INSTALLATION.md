# Installing Jakana

Jakana will provide one official command, `jakana`, across supported platforms. The installer should place the command on the user's `PATH`, install the selected backend, and provide `jakana --version`.

## Current development installation

The package is currently installed from a local checkout while Jakana 1 is being developed:

```powershell
python -m pip install -e .
jakana --version
```

The editable install makes the `jakana` command available while pointing it at the current source tree.

Without installing the command, run a file from the repository root with:

```powershell
.\run.ps1 model.jk
```

## Planned Windows installation

After Jakana is published to the Python Package Index:

```powershell
py -m pip install jakana
jakana --version
```

After the official Windows Package Manager manifest is published:

```powershell
winget install Jakana.Jakana
jakana --version
```

The Winget package must be created only after the release artifacts, publisher identity, checksums, upgrade behavior, and uninstall behavior are stable.

## Planned macOS installation

Homebrew is the preferred macOS distribution channel:

```bash
brew install jakana
jakana --version
```

A direct installer package can be provided later for users who do not use Homebrew.

## Planned Linux installation

Jakana should provide a package for common distributions and a portable archive:

```bash
# Debian or Ubuntu, after the official repository is published
sudo apt install jakana

# Fedora, after the official repository is published
sudo dnf install jakana

# Portable fallback
curl -fsSL https://jakana.dev/install.sh | sh
```

The shell installer must verify downloads, support a custom install directory, and never require root unless the user selects a system-wide installation.

## Planned development installation

Contributors can clone the repository and install an editable development package:

```bash
git clone https://github.com/jakana-lang/jakana.git
cd jakana
python -m pip install -e .
jakana --version
```

## Device and backend model

The CLI remains the same across devices:

```text
jakana run app.jk
```

The installer selects the appropriate runtime for the operating system and CPU. Jakana source files should remain portable. Backend-specific dependencies should be installed by commands such as:

```text
jakana backend list
jakana backend install python
```

The Python backend is the first supported backend. C++, JavaScript, and Java backends should be optional packages so a user does not need to install every toolchain to use basic Jakana.

## Release requirements before public installers

- publish signed or checksum-verified release artifacts
- test Windows, macOS, and Linux installation and uninstall flows
- include x64 and ARM64 support where the backend supports it
- ensure `jakana` is placed on `PATH`
- support `jakana --version` and `jakana doctor`
- document Python, C++, JavaScript, and Java backend prerequisites
- publish upgrade and rollback instructions
