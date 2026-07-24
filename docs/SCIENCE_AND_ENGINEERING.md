# Jakana for Science and Engineering

This document outlines how Jakana is used across various scientific and engineering disciplines. For each section, we provide Jakana code and its Python transpilation.

## 1. Physics

Jakana leverages Python's scientific computing libraries, making it an excellent choice for physics simulations and calculations.

### Constants and Basic Calculations
```jakana
use scipy.constants as const

# E = mc^2
fn rest_energy(mass) {
    energy = mass * const.c * const.c
    energy |> echo
}

rest_energy(1.0)
```

**Transpiles to:**
```python
import scipy.constants as const

def rest_energy(mass):
    energy = mass * const.c * const.c
    print(energy)

rest_energy(1.0)
```

### Classical Mechanics (Projectile Motion)
```jakana
use math

fn projectile_range(v0, theta_deg) {
    g = 9.81
    theta_rad = math.radians(theta_deg)
    range = (v0 * v0 * math.sin(2 * theta_rad)) / g
    range |> echo
}

projectile_range(25.0, 45.0)
```

**Transpiles to:**
```python
import math

def projectile_range(v0, theta_deg):
    g = 9.81
    theta_rad = math.radians(theta_deg)
    range = (v0 * v0 * math.sin(2 * theta_rad)) / g
    print(range)

projectile_range(25.0, 45.0)
```

### Quantum Mechanics (Energy Levels)
```jakana
use scipy.constants as const

# Energy levels of particle in a 1D box
fn energy_level(n, L, m) {
    E = (n * n * const.h * const.h) / (8 * m * L * L)
    E |> echo
}
```

**Transpiles to:**
```python
import scipy.constants as const

def energy_level(n, L, m):
    E = (n * n * const.h * const.h) / (8 * m * L * L)
    print(E)
```

## 2. Biology & Bioinformatics

Jakana integrates seamlessly with `biopython`.

### Sequence Analysis
```jakana
use Bio.Seq as Seq

fn analyze_sequence(dna_str) {
    seq = Seq.Seq(dna_str)
    
    # GC content and complement
    seq.complement() |> echo
    seq.transcribe() |> echo
    seq.translate() |> echo
}

analyze_sequence("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG")
```

**Transpiles to:**
```python
import Bio.Seq as Seq

def analyze_sequence(dna_str):
    seq = Seq.Seq(dna_str)
    
    print(seq.complement())
    print(seq.transcribe())
    print(seq.translate())

analyze_sequence("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG")
```

## 3. Chemistry

RDKit is a powerful tool for cheminformatics in Jakana.

### Molecular Properties
```jakana
use rdkit.Chem as Chem
use rdkit.Chem.Descriptors as Descriptors

fn get_mol_weight(smiles) {
    mol = Chem.MolFromSmiles(smiles)
    if mol {
        weight = Descriptors.MolWt(mol)
        weight |> echo
    } else {
        "Invalid SMILES" |> echo
    }
}

get_mol_weight("CCO") # Ethanol
```

**Transpiles to:**
```python
import rdkit.Chem as Chem
import rdkit.Chem.Descriptors as Descriptors

def get_mol_weight(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        weight = Descriptors.MolWt(mol)
        print(weight)
    else:
        print("Invalid SMILES")

get_mol_weight("CCO")
```

## 4. Astronomy & Space

`astropy` provides core functionality for astronomical calculations.

### Orbital Mechanics
```jakana
use math
use astropy.constants as const

fn escape_velocity(mass, radius) {
    v = math.sqrt((2 * const.G.value * mass) / radius)
    v |> echo
}

escape_velocity(5.972e24, 6371000) # Earth
```

**Transpiles to:**
```python
import math
import astropy.constants as const

def escape_velocity(mass, radius):
    v = math.sqrt((2 * const.G.value * mass) / radius)
    print(v)

escape_velocity(5.972e24, 6371000)
```

## 5. Mathematics (Exact & Symbolic)

Use `sympy` for symbolic mathematics.

### Symbolic Differentiation
```jakana
use sympy

fn differentiate_expr() {
    x = sympy.Symbol("x")
    expr = sympy.sin(x) * sympy.exp(x)
    
    derivative = sympy.diff(expr, x)
    derivative |> echo
}

differentiate_expr()
```

**Transpiles to:**
```python
import sympy

def differentiate_expr():
    x = sympy.Symbol("x")
    expr = sympy.sin(x) * sympy.exp(x)
    
    derivative = sympy.diff(expr, x)
    print(derivative)

differentiate_expr()
```

## 6. Statistics & Probability

`scipy.stats` covers extensive statistical needs.

### Normal Distribution
```jakana
use scipy.stats as stats

fn norm_prob(x, mu, sigma) {
    p = stats.norm.cdf(x, mu, sigma)
    p |> echo
}

norm_prob(1.96, 0, 1)
```

**Transpiles to:**
```python
import scipy.stats as stats

def norm_prob(x, mu, sigma):
    p = stats.norm.cdf(x, mu, sigma)
    print(p)

norm_prob(1.96, 0, 1)
```

## 7. Algorithms

Jakana can easily implement complex algorithms like graph traversals.

### Breadth-First Search (BFS)
```jakana
fn bfs(graph, start) {
    visited = set()
    queue = [start]
    
    while queue {
        node = queue.pop(0)
        if node not in visited {
            node |> echo
            visited.add(node)
            queue.extend(graph[node])
        }
    }
}
```

**Transpiles to:**
```python
def bfs(graph, start):
    visited = set()
    queue = [start]
    
    while queue:
        node = queue.pop(0)
        if node not in visited:
            print(node)
            visited.add(node)
            queue.extend(graph[node])
```

## 8. Signal Processing & Control

### FFT Computation
```jakana
use scipy.fft as fft

fn compute_fft(data) {
    freq_domain = fft.fft(data)
    freq_domain |> echo
}
```

**Transpiles to:**
```python
import scipy.fft as fft

def compute_fft(data):
    freq_domain = fft.fft(data)
    print(freq_domain)
```

## 9. Geospatial & Earth Science

### Distance Calculation
```jakana
use geopy.distance as distance

fn calculate_distance(coord1, coord2) {
    dist = distance.distance(coord1, coord2).km
    dist |> echo
}
```

**Transpiles to:**
```python
import geopy.distance as distance

def calculate_distance(coord1, coord2):
    dist = distance.distance(coord1, coord2).km
    print(dist)
```

## 10. Engineering

### Electrical Impedance
```jakana
use math

fn rc_impedance(r, c, f) {
    omega = 2 * math.pi * f
    xc = 1 / (omega * c)
    z = math.sqrt(r * r + xc * xc)
    z |> echo
}
```

**Transpiles to:**
```python
import math

def rc_impedance(r, c, f):
    omega = 2 * math.pi * f
    xc = 1 / (omega * c)
    z = math.sqrt(r * r + xc * xc)
    print(z)
```
