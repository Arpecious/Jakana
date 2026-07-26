<p align="center">
  <img src="assets/logo.svg" alt="Jakana logo" width="180">
</p>

<h1 align="center">Jakana</h1>

<p align="center">
  A simple, powerful, unified programming language for moving across technology ecosystems.
</p>

## Project status

Jakana is in its first generation, Jakana 1. The current release is `1.0.0`. Jakana uses one unified, easy-to-learn syntax with multiple backends: **Python first** (granting immediate access to AI, ML, Data Science, and Web libraries), followed by **C++** (for high performance), JavaScript, and Java backends.

## First program

```jakana
use math

number = 25
root = sqrt(number)

echo root

if root == 5 {
    echo "Verified"
}

fn square(x) {
    return x * x
}

echo square(5)

[1, 2, 3, 4, 5]
    |> sum
    |> echo
```

## Install and run

```powershell
python -m pip install -e .
jakana run examples/phase1_demo.jk
jakana transpile examples/phase1_demo.jk
jakana transpile --target cpp examples/phase1_demo.jk
```

## Ecosystem examples

Tested, working examples in `examples/ecosystem/`:

| File | Modules |
| :--- | :--- |
| `math_and_stats.jk` | `math`, `statistics` |
| `strings_and_text.jk` | `string`, `re`, `textwrap` |
| `files_and_os.jk` | `os`, `pathlib`, `tempfile`, `shutil` |
| `json_and_data.jk` | `json`, `collections` |
| `datetime_and_time.jk` | `datetime`, `time`, `calendar` |
| `crypto_and_encoding.jk` | `hashlib`, `base64`, `secrets`, `uuid` |
| `itertools_and_functional.jk` | `itertools`, `functools` |
| `networking_and_web.jk` | `urllib.parse`, `html`, `ipaddress` |
| `system_and_platform.jk` | `platform`, `sys` |
| `compression_and_archive.jk` | `zlib`, `gzip`, `base64` |

Run any example:

```powershell
jakana run examples/ecosystem/math_and_stats.jk
```

## Documentation

- **[docs/LANGUAGE_GUIDE.md](docs/LANGUAGE_GUIDE.md)**: Beginner-friendly tutorial and syntax reference.
- **[docs/PYTHON_ECOSYSTEM.md](docs/PYTHON_ECOSYSTEM.md)**: Complete Python ecosystem reference (15 categories, 60+ modules).
- **[docs/AI_ML_DEEP_LEARNING.md](docs/AI_ML_DEEP_LEARNING.md)**: AI, Machine Learning, Deep Learning (PyTorch, TensorFlow, Hugging Face).
- **[docs/SCIENCE_AND_ENGINEERING.md](docs/SCIENCE_AND_ENGINEERING.md)**: Physics, Biology, Chemistry, Astronomy, Math, Engineering.
- **[docs/API_SDK_AND_SYSTEMS.md](docs/API_SDK_AND_SYSTEMS.md)**: REST APIs, Databases, Message Queues, SDKs, Cloud, DevOps.
- **[docs/VISUALIZATION_AND_MEDIA.md](docs/VISUALIZATION_AND_MEDIA.md)**: Data visualization, image/audio/video processing, GUIs, Game Dev.
- **[docs/ADVANCED_AI_AND_ALGORITHMS.md](docs/ADVANCED_AI_AND_ALGORITHMS.md)**: MCMC, MCTS, RL, Evolutionary Algorithms, AGI concepts.
- **[docs/COMMANDS_AND_INTERNALS.md](docs/COMMANDS_AND_INTERNALS.md)**: CLI commands, internal function call graphs, and AST pipeline.
- **[docs/ROADMAP.md](docs/ROADMAP.md)**: Jakana 1 development plan and milestones.
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**: Independent frontend and multi-backend compiler design.
- **[docs/PYTHON_BACKEND.md](docs/PYTHON_BACKEND.md)**: Python target mapping and interop details.
- **[docs/VSCODE.md](docs/VSCODE.md)**: `.jk` syntax highlighting in VS Code.
