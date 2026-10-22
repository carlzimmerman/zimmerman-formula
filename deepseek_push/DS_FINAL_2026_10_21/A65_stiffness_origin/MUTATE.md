# A65 — mutations

Each mutation must break at least one check and exit 1. Commands were run from this
directory; the full outputs are `a65_MUTATE_<name>.out` (and the JSON copies
`a65_results_MUTATE_<name>.json`). The unmutated run is `a65.out`, **24/24 PASS, exit 0**.

```
python3 a65_checks.py --mutate coeff2      -> exit 1   11/24 PASS
python3 a65_checks.py --mutate jeans_rho   -> exit 1   18/24 PASS
python3 a65_checks.py --mutate footing_alt -> exit 1   11/24 PASS
python3 a65_checks.py --mutate quantum     -> exit 1   23/24 PASS
python3 a65_checks.py --mutate guard       -> exit 1   23/24 PASS
```

## coeff2 — `L* → 2 L*` (a non-unit coefficient)

Breaks **K1, K2, K4, K5, K6, K11, K12b, K13, K16, K17, K18, K21, K22**. The first failure is the
point: `L* = 48.050024 pc`, and K16 reports `coeff = 0.500000000` against the required
`1.000000000`. Every ratio-to-`L*` check moves by the same factor, which is exactly what a
tuned coefficient would do to the lane.

## jeans_rho — cosmic cold density `2.2566e-27 → 1e-20 kg/m³`

Breaks **K7, K9, K13, K15, K17, K18**. K7 moves from 196.227 kpc to 0.0932 kpc; K13's
"density needed" ratio collapses from `6.671e7 ρ_c` to `15.05 ρ_c`; K18 admits 4 candidates
because the (a) Jeans row now sits in the window. This is the mutation that shows why (a)
cannot be a derivation: the answer tracks the density.

## footing_alt — use `a0 = 1.13e-10 m/s²`

Breaks **K1, K2, K4, K5, K6, K11, K12b, K13, K16, K17, K19, K21, K22**. `L* = 19.900364 pc`,
17 % below the floor. K19 and K20 together are the guard: the number is footing-conditional,
and this mutation is the 21 % error the P3 footing would produce.

## quantum — exponent 1/4 → 1/2 in the quantum-pressure length

Breaks **K17** only: `L_Q(m_P) = 9.28e24 kpc` instead of 548.39 kpc. This isolates the (d)
result — the only thing wrong is the dimensional power, and the check catches it without
touching anything else.

## guard — let candidate (b) pass

Breaks **K18** only: pass count 1 → 2. This is the anti-juggling check itself; the mutation
is a candidate being waved through the pre-registered criterion, and the check refuses it.
