# a0kit — the de Sitter–Unruh modified-inertia acceleration-scale toolkit

A small, dependency-light (numpy only) Python library implementing the formulas of the
de Sitter–Unruh **modified-inertia** framework: the horizon-derived MOND acceleration
scale, its interpolation kernel, the a₀-line identity, the Λ↔a₀ inversion, and the
redshift law a₀(z) ∝ √ρ_DE(z).

## What it computes
| Function | Formula |
|---|---|
| `a0_from_lambda(Λ)` | a₀ = c²√(Λ/32π) (canonical, ~9.36×10⁻¹¹ m/s²) |
| `a0_from_hubble(H0, footing)` | a₀ = cH_Λ/Z (canonical) or cH₀/Z (alt) |
| `lambda_from_a0(a0)` | Λ = 32π a₀²/c⁴ |
| `rho_de_from_a0(a0)` | ρ_DE = 4a₀²/(Gc²) |
| `nu(y)` | ν = √(1+1/y), y = g_bar/a₀ |
| `g_obs(g_bar, a0)` | g_obs = √(g_bar² + g_bar·a₀) (the a₀-line) |
| `a0_line(g_obs, g_bar)` | a₀ = (g_obs² − g_bar²)/g_bar (invert) |
| `a0_of_z(z, w0, wa, a0_0)` | a₀(z) = a₀(0)√(ρ_DE(z)/ρ_DE,0), CPL |
| `btfr_vflat(M_bar, a0)` | V_flat = (a₀ G M_bar)¹ᐟ⁴ (deep-MOND BTFR) |
| `footings()` | both a₀ footings (canonical / alt) |

## Install & use
```bash
git clone https://github.com/carlzimmerman/zimmerman-formula
python3 zimmerman-formula/a0kit/a0kit.py    # self-test
```
```python
import a0kit
a0 = a0kit.a0_from_lambda()                 # 9.35e-11 m/s^2
a0kit.lambda_from_a0(a0)                     # -> Planck Lambda
a0kit.a0_of_z(3, w0=-0.84, wa=-0.62)/a0      # -> 0.77 (evolving-DE decline)
```

## Honest scope (read before citing)
This library **computes the framework's relations; it does not prove them.** The *value*
of a₀, the coefficient Z = √(32π/3), and the sign of the inertial correction are
**posited, not derived**. The interpolation ν(y)=√(1+1/y) is the functional form of
**Milgrom (1999)**; the framework's distinctive content is the cH_Λ/Z coefficient and a
modified-*inertia* (not modified-gravity) completion. Both a₀ footings are provided
because which cosmic density sets the scale is not settled by the framework.

## References & citation
- Milgrom 1983 (ApJ 270, 365); Milgrom 1999 (Phys. Lett. A 253, 273) — the interpolation kernel.
- Framework: Zimmerman, flagship 10.5281/zenodo.21312654; the a₀-line / Λ-from-rotation
  10.5281/zenodo.21419735; MI field-theory results 10.5281/zenodo.21403470.
- **Code DOI (cite this for the software): 10.5281/zenodo.21478982** (version-locked 1.0.0 archive).
- If you use this code, please cite the code DOI and the framework papers above.

License: AGPL-3.0 (per the parent repository).
