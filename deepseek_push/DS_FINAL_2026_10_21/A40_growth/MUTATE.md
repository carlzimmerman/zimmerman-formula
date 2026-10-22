# A40 — MUTATIONS

Three mutations, each of which must break at least one declared check. The base run is
`A40 COMPLETE: 17/17 checks PASS.` (exit 0). Each mutation is a single, named, physically meaningful
change to one line of physics; the mutated run exits 1.

```
python3 a40_checks.py                        # A40 COMPLETE: 17/17 checks PASS.   exit 0
python3 a40_checks.py --mutate quad           # 16/17                              exit 1
python3 a40_checks.py --mutate nocold         # 16/17                              exit 1
python3 a40_checks.py --mutate bgflat         # 16/17                              exit 1
```

## 1. `--mutate quad` — the rival interpolation

Replaces the canonical response `dg/dg_N = (1+s)²/(4s)` by the n = 2 (quadrature) law's
`(1 + 1/(2y))/√(1 + 1/y)`. This is the theory's documented rival (BRIEF §1: "n = 1 and n = 2 are
different effective theories"), so it is the mutation that matters: if the code cannot tell them
apart, the derivation is not wired to the numbers.

```
K2b FAIL max relative error = 1.91e-01   < 1e-8
A40 COMPLETE: 16/17 checks PASS.
```

K2b is the bridge between the symbolic result and the ODE: the response the integrator calls must
equal the finite difference of the law the code inverts. The rival law is **19 % off** that derivative
at some point in `(10⁻², 10⁴) a₀`. The two laws are barely distinguishable in the growth: canonical σ8(0) = 0.7619 vs quadrature
0.7605 (0.18 %), χ²(fσ8) 14.21 vs 14.69 — the growth sector, like SPARC's total χ² (THEORY.md §4),
cannot separate n = 1 from n = 2; the shape tests (A25) do.

## 2. `--mutate nocold` — the "dg/dg_N already carries the cold sector" branch as the primary

Sets `SRC_MODE = "A"`: the growth source becomes `(3/2)Ω_b(a)(dg/dg_N)δ` instead of
`(3/2)Ω_m(a)(dg/dg_N)δ` — i.e. the reading in which the law's response already contains the cold
sector, so `ρ_c` must not be added. This is not a straw man: it is exactly the branch the task asks
to resolve, and it is the branch a careless "avoid double counting" argument produces.

```
K15 FAIL sigma8(0) = 0.0024 vs Planck 0.811 (-0.8086, -134.77 sigma on sigma8); S8(dyn) = 0.0021
     vs KiDS-1000 0.759 +- 0.021   |sigma8-0.811|/0.811 < 15%
A40 COMPLETE: 16/17 checks PASS.
```

σ8 = 0.0024, 323× below the measured amplitude (and χ²(fσ8) = 747.2/8): with only `Ω_b = 0.0497` in
the source, the
matter-era growing mode is `δ ∝ a^0.30` instead of `a`. The check has teeth because the branch is
not a small perturbation of the answer — it is a different cosmology, and it is dead. (The branch
table in `report.md` §5 keeps this number as a *reported* branch; the mutation makes it the primary,
which is what fails.)

## 3. `--mutate bgflat` — the background normalisation

Sets `Ω_Λ,eff = 1 − Ω_m` instead of 1, i.e. the flat ΛCDM normalisation (the branch in which A33's
clock stress `ρ_β` cancels the excess vacuum) rather than the literal `Λ_bare = 3H₀²/c²` reading the
task specifies.

```
K5 FAIL E^2(0) = 1.000000 = 1 + 0.3163; H(0) = 67.40 km/s/Mpc = 1.0000 x H0(dS)
     |E^2(0)-(1+Omega_m)| < 1e-12
A40 COMPLETE: 16/17 checks PASS.
```

K5 asserts the identity that the literal reading is *defined* by: `E²(0) = Ω_Λ,eff + Ω_m` with
`Ω_Λ,eff = 1`. Under the flat mutation `E²(0) = 1` and the identity fails by 0.3163. This is the
check that pins the background, and it is the one that matters most: the same mutation moves
σ8(0) from 0.7619 to 0.8132 (report §7), so a silent switch of background would change every number
in the lane by more than any effect the lane measures.

## What is *not* mutated, and why

- **`a₀`** — the two footings (1.132e−10, 9.36e−11) are a declared sensitivity, not a mutation: they
  move σ8(0) by 0.05 %, which is smaller than the print precision of the report's tables. A mutation
  has to break a check.
- **The σ8 anchor (0.811)** — it is an external input with a stated source (Planck 2018 ΛCDM), and the
  lane's conclusions are about the *ratio* `D_th/D_ΛCDM`, which is anchor-independent. Mutating it
  would only rescale every σ8 by the same factor and break nothing structural.
- **The fσ8 data** — external, with its provenance and bibliography in `report.md` §4. Mutating data
  to make a check fail would prove nothing about the code.
