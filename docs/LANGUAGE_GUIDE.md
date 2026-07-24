# Jakana Language Guide (Full Python Ecosystem Integration)

**Jakana** uses its clean, minimal identity to unlock the entire Python library ecosystem dynamically.

---

## Complete Ecosystem Example

```jakana
use math
use random
use json
use os
use requests
use torch

# 1. Math
val = 144
echo sqrt(val)

# 2. Random
num = randint(1, 100)
echo num

# 3. JSON
payload = dumps({"status": "active", "val": num})
echo payload

# 4. OS
cwd = getcwd()
echo cwd

# 5. Multiline Pipeline Transformation
[10, 20, 30, 40, 50]
    |> sum
    |> echo
```

---

## How Dynamic Qualification Works

When you write `use <module>` (for standard libraries like `math`, `os`, `random`, `json`, `re`, `sys`, `time`, `datetime`, or third-party packages like `numpy`, `pandas`, `requests`, `torch`, `fastapi`, `cv2`, `scipy`, etc.):

- Jakana dynamically inspects the imported module at parse time.
- Any function call matching an exported function of the module (e.g. `randint()`, `dumps()`, `getcwd()`, `sqrt()`, `get()`, `tensor()`) automatically qualifies to `<module>.<func>()`!
- You enjoy a clean, elegant syntax while getting 100% access to every Python library ever built.
