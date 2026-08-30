# Phase X — High-Acceleration (GR) Limit

Status labels: `DERIVED` / `IMPOSED` / `FITTED` / `UNKNOWN`.

## 1. The high-acceleration limit

In the regime `a_N >> a₀` (i.e. `y = a_N/a₀ >> 1`), the interpolation function
satisfies
```
μ(y) = 1 - e^{-y}  ->  1      (as y -> ∞) .
```
Therefore the effective acceleration is
```
a_eff = μ(y) a_N -> a_N        (GR / Newtonian limit) .
```
**DERIVED:** The high-acceleration limit **reduces to GR** (Newtonian gravity
in the weak-field case). The nonlocal M-term becomes negligible: `Z = 4y² >> 1`,
`F_+'(Z) = (1/2)e^{-y} -> 0`, so the M-stress tensor `E_{μν}` is exponentially
small (`~ e^{-y}`) and the field equation reduces to Einstein's equation
`G_{μν} - Λg_{μν} = (8πG/c⁴)T^{(m)}_{μν}`.

## 2. Consistency of the GR limit

| Check | Result | Status |
|-------|--------|--------|
| `μ(y) -> 1` as `y -> ∞` | PASS | DERIVED |
| `F_+'(Z) -> 0` as `Z -> ∞` | PASS (`(1/2)e^{-y}`) | DERIVED |
| `E_{μν} -> 0` (exponentially) | PASS | DERIVED |
| Field equation -> Einstein equation | PASS | DERIVED |
| Regulator irrelevant for `Z >> ε` | PASS (regulator only on `[0,ε]`) | DERIVED |

**Phase X verdict: PASS.** The high-acceleration limit correctly reduces to GR.
This is a **necessary** condition and it is satisfied. The candidate is
**GR-consistent** at high acceleration.

> Note: GR-consistency at high acceleration is independent of the three fatal
> defects (regulator no-go at low acceleration, T-gap, physical ghost). The
> candidate recovers GR where MOND is not needed, but is broken where MOND is
> needed (deep-MOND regime) and is unstable (ghost) everywhere.
