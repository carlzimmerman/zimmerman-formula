# AS059 — Deep coefficient in a general static action

**Group:** A03 — Coefficient mechanisms and their missing premises
**Kind:** audit · **Branch:** CORE coefficient; conditional MU_n statistical response
**Run:** `AS059-r1-20260928T020000Z-dsv4f-hermes`
**Task SHA-256:** `f3533ad894ba8834ec9b16346afb17928c36d8f0501939dd625a7a50625154ba` (verified against the pinned value before execution; source hashes PD01/PD08/k01 verified against SOURCE_MANIFEST.json)

---

## 1. Claim, symbol dictionary, boundary conditions, assumptions

**Mathematical object.** The general static action with a kinetic built from a
function of the field strength and a linear source coupling,

```
E[Phi] = A s^2 ∫ K(|grad Phi|/s) dV  +  B ∫ rho Phi dV,
```

with the response defined by `K'(Y)/(2Y)` after normalization.

| symbol | meaning | status |
|---|---|---|
| `Phi` | scalar potential (standard sign: `Phi -> -G M/r` at infinity, so `rho` sources `div(-g) ...`) | framework |
| `Y = |grad Phi|/s` | dimensionless field strength | framework |
| `s = c sqrt(G rho_Lambda)` | vacuum's own acceleration scale (mass density `rho_Lambda`) | framework |
| `a0 = kappa c sqrt(G rho_Lambda) = kappa s` | deep acceleration scale | framework |
| `kappa = 1/2` | **adopted as input** in this task (no independent derivation supplied); NOT a derived result here | input |
| `r_M = sqrt(G M_b/a0)` | mass scale of a body `M_b` | framework |
| `v_flat^4 = G M_b a0` | deep flat-rotation identity | framework |
| `A, B` | action coefficients with units `[A] = m^-2 s^-2`-flux factors, `B/2A = 4 pi G` (Newtonian identification, see §3) | to be constrained |
| `K(Y)`, `k0, k1, k2, k3` | kinetic function and its expansion `K = k3 Y^3 + k2 Y^2 + k1 Y + k0` | to be constrained |
| `mu_n(Y) = 1 - (1+Y)^(-n)`, `n >= 1` | the allowed interpolation family reproducing slope `n` and saturation 1 (channel-count reading) | conditional (statistical response) |
| `G`, `c`, `M_sun`, `pc` | `6.67430e-11`, `299792458`, `1.98847e30`, `3.085677581491367e16` (SI) | measured input |

**Boundary conditions (frozen vacuum, from the vacuum sector k01/PD01 premise):
** `K(0) = K'(0) = 0` (the vacuum carries no energy and no response), and the
response `mu(Y) = K'(Y)/(2Y)` satisfies `mu(0)=0`, `mu(infinity)=1` (deep regime
linear, Newtonian regime saturated). These kill the constant, linear and
quadratic coefficients of K:

```
k1 = K'(0) = 0         (linear term)
k2 : from mu(0)=0 and K'(0)/(2Y) regular at Y->0 with K'(0)=0  ->  k1 = 0;
     the quadratic coefficient k2 contributes mu_2(Y) = k2  at Y=0,
     so mu(0)=0 forces k2 = 0.
```

**Two footings (must be carried separately, never with both fixed density and
fixed kappa simultaneously):**

| footing | a0 (m/s^2) | status |
|---|---|---|
| canonical | `9.3619e-11` | equals `s/2` for `kappa = 1/2`; used in A7a |
| alternative | `1.1279e-10` | ratio to canonical is `sqrt(rho_ratio)`, `rho_ratio = 1.45148715739961...` (a fixed-density *different* vacuum reading); used in A7b/A7c with its own `kappa_alt = 0.60238840406327775...`; A7c additionally fixes the canonical density and solves for the slope `n_alt = 1.66005851582587...` |

Numerics: `s = 1.87238e-10 m/s`, `rho_Lambda = 5.84441245402188e-27 kg/m^3`
(consistent with a0 = s/2), `r_M(1e11 M_sun) = 12201.97 pc` (canonical),
`11116.72 pc` (alternative).

## 2. Variation of the functional (all constants retained)

```
delta K(Y) = K'(Y) delta Y,   delta Y = (grad Phi . delta grad Phi)/(s |grad Phi|)
delta E = ∫ A s^2 K'(Y) (grad Phi . delta grad Phi)/(s |grad Phi|) dV + B ∫ rho delta Phi dV
        = ∫ [A K'(Y)/Y grad Phi] . delta grad Phi dV + B ∫ rho delta Phi dV
        = -∫ div[ A K'(Y)/Y grad Phi ] delta Phi dV + B ∫ rho delta Phi dV
```

Stationarity for all `delta Phi`:

```
div[ A K'(Y)/Y grad Phi ] = B rho ,        Y = |grad Phi|/s          (E-L)
```

All factors are retained: the two `s` in `A s^2 K'(Y)` and `delta Y` cancel
exactly (`s^2 / s = s`, and `|grad Phi| = s Y` contributes the second), leaving
the **flux coefficient** `A K'(Y)/Y`. With the response `mu(Y) = K'(Y)/(2Y)` the
E-L equation is

```
div[ 2 A mu(Y) grad Phi ] = B rho .
```

(Cross-checked symbolically with sympy in section [1] of the code and by direct
80-dps substitution in section [7]; the flux identity
`|grad Phi| = s Y  =>  A K'(Y)/Y = 2 A mu(Y)` is exact.)

## 3. Newtonian identification (signs and units)

In the regime `Y >> 1`, `mu -> 1`, the E-L equation is `div[2A grad Phi] = B rho`,
i.e. the Poisson coefficient is `B/2A`. With the standard potential sign
(`Lap Phi = 4 pi G rho` for `Phi = -G M/r`):

```
B/2A = 4 pi G            (physical pair, corpus PD08: particle-free derivation)
```

This is a normalization/identification condition on the ratio `B/A` (equivalently
`B = 8 pi A G`); the overall scale of `(A,B)` is fixed by nothing in the field
equation — see NC2: the pair `(A,B) -> (2A,2B)` leaves every field unchanged.

**Units:** `[B rho] = m s^-2 = [div(2A mu g)]` with `[A]` chosen so the flux
`2A mu g` has units `m/s^2`; the deep matching below carries `s` in `m/s^2`,
`G` in `m^3 kg^-1 s^-2`, `r` in m.

## 4. Deep regime: the a0-line and the combination that sets kappa

Deep regime `r >> r_M` (`Y << 1`): with the frozen-vacuum conditions
`k1 = k2 = 0`, the kinetic is `K(Y) = k3 Y^3 + O(Y^4)` and the response is
linear:

```
mu(Y) = K'(Y)/(2Y) = (3 k3 Y^2)/(2Y) = (3 k3/2) Y          (Y != 0)
slope n := mu'(0) = 3 k3/2 ,  i.e.  k3 = 2n/3 .
```

**The cubic deep coefficient sets the deep response slope** (Lean R3; the
quadratic coefficient contributes zero — Lean R4 negative control; the linear
and constant terms are killed by the vacuum boundary conditions).

Spherically symmetric point mass `M_b`: flux balance `4 pi r^2 (2A mu g) = B M_b`
with `mu = n g/s`:

```
n g^2/s = B M_b/(8 pi A r^2)     =>    g^2 = (B s / (8 pi A n)) (M_b/r^2)      (deep line)
```

Comparing with `v_flat^4 = G M_b a0` (i.e. `g^2 = a0 G M_b/r^2`):

```
a0 = B s/(8 pi A G n)   =>   kappa := a0/s = B/(8 pi A G n)
```

With the cubic coefficient:

```
kappa = B/(12 pi A G k3)          (since n = 3 k3/2)
```

**This is the exact combination of A, B and the cubic deep coefficient that
sets kappa** (Lean R5, R6; `g^2 = a0 GM/r^2` is an exact identity of the matched
line, and `kappa = B/(8 pi A G n)` is exact algebra — no limiting statement).

Under the Newtonian normalization `B = 8 pi A G` the combination collapses to
the slope alone:

```
kappa = 1/n = 2/(3 k3)             (Lean R7 with n=2: kappa = 1/2; Lean R8)
```

With the **adopted** channel count `n = 2` (kappa = 1/2): `kappa = 1/2` lands.

**Leading neglected term (domain Y << 1):** the on-shell deep solution of the
full E-L with `mu_n` satisfies

```
g^2/g_deep^2 - 1 = a Y + c Y^2 + O(Y^3),
a = (n+1)/2 ,  c = (n+1)(n-1)/12 ,   g_deep^2 = (s/n)(G M_b/r^2),   Y = g/s .
```

(both coefficients verified at 80 dps, checks N3a; the deepest grid point leaves
a `Y^3`-scaled residual with O(1) coefficient, checks N3b). For the member
`n = 1` the identity is exact to all orders: `g^2/g_deep^2 - 1 = Y`.

The Newtonian approach rate is the exact flux identity

```
g/g_N - 1 = (1+Y)^(-n)/(1-(1+Y)^(-n)) ~ Y^(-n)      (r -> 0 limit, Y -> infinity)
```

with `g_N = G M_b/r^2` (checks N1a; the deep rate is N1b).

## 5. Negative controls (capable of failing)

- **NC1 — pre-set A, B before variation.** Take a perturbed physical pair
  `(A', B')` (chosen so that the Newtonian identification holds: `B'/2A' = 4 pi G`,
  i.e. the same ratio, different convenient normalization). The pre-set reading
  `kappa = 1/2` is *wrong* for the perturbed pair (measured `|kappa_meas - 0.5| = 0.5`,
  failing hard); the general combination `kappa = B/(8 pi A G n)` with the deep
  recovery `kap_meas = (g^2/g_N)/s / (1 + aY + cY^2)` reproduces the general
  prediction to `1e-20` relative: **the freedom lost by pre-setting A and B is
  exactly the freedom of kappa.**
- **NC2 — only the ratio B/A matters:** `(A,B) -> (2A,2B)` leaves every field
  unchanged to `0.0` (141-pt grid).
- **NC3 — the quadratic floor destroys the deep regime:** with `k2 != 0`
  (violating the vacuum boundary), the deep response is the floor branch with
  slope `-2` measured vs `-1/2` for the pure cubic — the a0-line does not exist.
- **NC4 — a linear term in K destroys the scale-invariance of the matched
  coefficient:** `|kappa_A - kappa_B| = 0.125` across two radii,
  `>> 0` (matching radius shifts the recovered coefficient).

All four controls carry explicit thresholds and are implemented to fail; the
full run records `50/50 PASS` with measured (not Boolean) residuals.

## 6. Independent checks (different representations)

1. **Canonical on-shell E-L residual** (section N2): the exact Newton solve of
   `mu_n(g/s) g = B M_b/(8 pi A r^2)` substituted back into the E-L gives worst
   `|mu g - h|/h` between `4.8e-67` and `8.9e-67` across the 301-point grid
   (`log10 r/r_M` in -15..15) for all four diagnostics — at the 80-dps floor.
2. **SI substitution into the original E-L** (section A7): with
   `mu_2(Y) = 1-(1+Y)^(-2)` and the SI constants of §1, the exact solve gives
   worst residual `1.05e-75` (canonical footing), `2.63e-74` (alternative
   footing, fixed `kappa = 1/2`), `6.10e-74` (alternative footing, fixed density
   with slope `n_alt = 1.6600585158...`, non-integer — integrality of the slope
   is extra structure, not action-imposed).
3. The deep **line** is an asymptotic solution: substituting `g_deep` directly
   leaves a residual `7.5e-6 ~ ((n+1)/2) Y` (the leading neglected term of §4),
   consistent with the O(Y) prediction to `1e-4` relative — the on-shell solve
   is exact; the line is its leading order.

## 7. Diagnostic counterexamples lambda in {1/2, 1, 2}

The family `mu_n`, `n = 1/kappa = {2, 1, 1/2}`, at 301 radii each (plus the edge
`kappa = 1/4` for the Newtonian rate):

| kappa | n | Newtonian rate | deep rate | worst grid residual | a0 = s/n recovered |
|---|---|---|---|---|---|
| 1/4 | 4 | `Y^-4` to 1.6e-13 rel. | `aY+cY^2` to 1.6e-16 rel. | 5.62e-66 | s/4, err 9.8e-48 |
| 1/2 | 2 | `Y^-2` to 4.1e-22 rel. | to 2.1e-16 rel. | 8.82e-67 | s/2, err 1.6e-47 |
| 1 | 1 | `Y^-1` to 1.7e-51 rel. | exact (`= Y`) | 8.87e-67 | s, err 4.7e-68 |
| 2 | 1/2 | `Y^-1/2` to 7.1e-8 rel. | to 1.7e-15 rel. | 4.79e-67 | 2s, err 2.5e-46 |

The four recovered deep coefficients `s/n = {4s, 2s, s, s/2}` are pairwise
distinct (A6): the diagnostics are **distinct actions**, not one law relabelled.

## 8. Branch discipline (criterion B comparison)

Branches `Q`, `RAR`, `MU2`, `EXP`, `MONO` (filtered): deep shared limit
`x^2/y -> 1` holds for all with the branch-dependent rate (`y` for Q, `sqrt(y)`
for RAR/MU2/EXP/MONO — measured to ~1e-5 relative at `y = 1e-6`), and the
finite-y disagreement is **real**: at `y = 0.1`, `x/x_MU2 = 0.92879 (Q),
1.03296 (RAR), 0.96267 (EXP), 1.032956 (MONO)`, with MU2 identically 1 — the
laws differ beyond relabelling (B1, B2; splice parameters `y* = 2.3374`,
`y_p = 2.5396`, `h_p = 0.6476`, delta 0.05). The **amended thirteen-item target
uses filtered MONO and causality criterion B**; the present result is a CORE
coefficient statement with the MU_n family as conditional statistical response —
no branch is imported to repair anything.

## 9. Sources inspected

- `PD01_polarization_count.py` — sha `37e39d1a...c74d` ✓ (vacuum boundary conditions; channel-count context)
- `PD08_particle_free_derivation.py` — sha `83f6054c...0cfb` ✓ (particle-free Newtonian pair `B/2A = 4 pi G`)
- `k01_zero_mode_theorem_and_lambda_free_vacuum.py` — sha `8df5a3ab...b25c` ✓ (vacuum zero-mode; `kappa` enters here as adopted)

## 10. Strongest surviving statement, domain, and first additional implication

**Surviving statement (all 50 checks pass; 80-dps floor).**
*In the general static action `E[Phi] = A s^2 ∫K(|grad Phi|/s)dV + B ∫rho Phi dV`
with response `mu(Y) = K'(Y)/(2Y)`, frozen-vacuum boundary conditions
(`K(0)=K'(0)=0`, `mu(0)=0`, `mu(inf)=1`) and the Newtonian identification
`B/2A = 4 pi G`: the E-L equation is exactly `div[2A mu(Y) grad Phi] = B rho`;
the cubic deep coefficient sets the deep slope `n = 3 k3/2`; the exact
combination setting kappa is `kappa = B/(8 pi A G n) = B/(12 pi A G k3)`, which
collapses to `kappa = 1/n = 2/(3 k3)` at `B = 8 pi A G`; with the adopted
`n = 2` this lands `kappa = 1/2`. Domain: static scalar field, spherical
sources, `Y in (0, inf)`, `n > 0`; deep statements on `r >> r_M` with leading
neglected term `((n+1)/2)Y + ((n+1)(n-1)/12)Y^2`, Newtonian statements on
`r << r_M` with the exact rate `Y^(-n)`.*

**Negative-control finding (the point of the audit).** The action class removes
*no* independent freedom: for *any* coefficient `kap0 != 0`, the inputs
(`B = 8 pi A G`, `n = 1/kap0`) give `kappa = kap0` exactly (Lean R9; the slope
map is injective, Lean R10). The general static two-slot action determines the
coefficient **given its inputs** but cannot determine it from its own
structure: pre-setting `A, B` (and hence `kappa`) before variation is exactly
the lost freedom (NC1). `kappa = 1/2` is an input here — as the seed requires.

**First additional implication (unresolved).** Why `n = 2` — i.e., which
independent mechanism counts the deep-response channels so that the slope is
the integer `2` (and `kappa = 1/2 = 1/n` becomes derived rather than adopted).
A7c shows the E-L alone tolerates non-integer slopes (`n_alt = 1.66006`);
the integer counting is exactly the missing premise. The natural next step is
the k01 zero-mode/the vacuum counting argument: if the zero-mode sector
physically forces `n in N` and the deep/Newtonian pair fixes the count, then
`kappa = 1/2` is derived — that implication is dispatched as a child
specification (see result.json child_proposals); it is **not** claimed here.

## 11. Lean certificate

`AS059_deep_coeff_general_action.lean` — 8 theorems, all compiled with
`lake env lean` in `fable_independent_2026/lean_2026` (compiled host:
`fable_independent_2026/lean_2026`; no files written into that tree):

| theorem | content |
|---|---|
| `response_expansion` | `K'(Y)/(2Y) = k1/(2Y) + k2 + (3k3/2)Y` for `Y != 0` |
| `deep_response_frozen_vacuum` | `(3k3 Y^2)/(2Y) = (3k3/2) Y` for `Y != 0` |
| `deep_slope_set_by_cubic` | `HasDerivAt (fun Y => (3k3/2)Y) (3k3/2) 0` |
| `quadratic_offset_irrelevant` | `HasDerivAt (fun Y => (3k3/2)Y + k2) (3k3/2) 0` — the k2 negative control |
| `deep_line_from_flux` | `n g^2/s = BM/(8 pi A r^2)  =>  g^2 = BMs/(8 pi A n r^2)` |
| `kappa_combination` | `a0 = Bs/(8 pi A G n)  =>  kappa = a0/s = B/(8 pi A G n)` |
| `kappa_half_conditional` | `B = 8 pi A G` and slope 2 `=> kappa = 1/2` |
| `kappa_from_cubic` | `B = 8 pi A G`, `n = 3k3/2  =>  kappa = 2/(3k3)` |
| `any_kappa_realized` | for any `kap0 != 0`: `(8 pi A G, 1/kap0)` realizes `kappa = kap0` — the anti-uniqueness counterexample |
| `slope_injects_into_coefficient` | `1/n1 = 1/n2` with nonzero slopes implies `n1 = n2` |

Zero `sorry`/`admit`; the unfiltered `#print axioms` output for every theorem is
exactly `{propext, Classical.choice, Quot.sound}` (verified in
`lean_compile_out.txt`). Checks R1–R10 map to numbered checks A1–A4 (algebra),
NC-group (controls), N1–N3 (limits), with the numeric residual ledger in
`raw_output.txt`/`raw_output.json`.

## 12. Bounds, commands, limitations

- Bounded prototype: **target** wall `< = 120 s`, memory `< = 512 MB`, 1 thread.
  **Actually enforced:** `signal.alarm(120)` inside the script (kills on
  timeout); single-threaded (no threading/multiprocessing subprocesses);
  measured wall `0.874 s`; measured max RSS `62,406,656 B = 59.5 MiB`
  (`/usr/bin/time -l`). Note the *enforced* wall cap is the alarm; RSS was
  measured but not hard-capped by the script (the interpreter did not exceed
  it).
- Commands (full lines in result.json): sha verification; the compute run;
  `cd fable_independent_2026/lean_2026 && lake env lean <abs path>.lean`.
- Limitations: (i) spherical/static reduction of the E-L in the numeric checks
  (the variational derivation itself is full 3-D); (ii) the family `mu_n` is the
  conditional statistical response — Q/RAR/EXP/MONO enter only as labelled
  comparisons (criterion B); (iii) observational preference (flatness at
  `v_flat^4 = G M a0`) is not used as a mathematical proof; (iv) the physical
  identification of the slope `n` and the vacuum count is an open dependency
  (k01 link), explicitly listed, not passed over.