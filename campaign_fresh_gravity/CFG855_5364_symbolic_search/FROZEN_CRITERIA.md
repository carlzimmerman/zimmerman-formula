# CFG855 FROZEN CRITERIA: closed-form symbols for Ω_c/Ω_b = 5.364, with a look-elsewhere base rate (before any script)

**Owner request (2026-10-19):** find the numerical symbols for the 5.364 ratio. Prior record: CFG642 (physical Buckingham-pi
monomials, 1.6M forms) CHANCE-LEVEL; CFG360 baryon tie NO-GO. This lane searches pure-number expressions and calibrates them.

## Target
R = ω_c/ω_b = 0.1200/0.02237 = 5.364 ± 0.065 (Planck 2018; 1σ = 1.2%). Window: |value − R| ≤ 0.065 (1σ); "close" ≤ 0.0065 (0.1σ).

## Enumeration (exhaustive, declared before running)
- Atoms: 1–9, π, e, √2, √3, √5, φ = (1+√5)/2, Z = 2√(8π/3) (the framework's coefficient).
- Unary: √x, x². Binary: +, −, ×, ÷. Complexity = number of atoms + operators; all expressions up to complexity 5, values kept in
  [0.01, 100], deduplicated by value (12 significant digits), each value tagged with its simplest expression.
## Statistic and classes
- n_hit = number of distinct values within 1σ of R; list the 15 closest with complexity.
- Base rate: n_hit for 1000 random targets log-uniform in [4, 7] with the same 1.2% relative window (seed 855) → percentile of R.
- **SPECIAL** only if R's n_hit is above the 99th percentile of random targets AND a complexity ≤ 3 expression lies within 0.1σ.
- **ORDINARY (numerology level)** otherwise. Either way, no expression is a derivation unless it follows from physics; stated.

## Controls
- K1: the enumerator recovers Z = 5.78881… and 16/3 exactly. MUTATE (separate output): target R × 1.07 → its percentile is reported
  (should be ordinary).

κ = ½ fitted; not theory closed.
