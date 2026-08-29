# COMPILER VERDICT — inverse-design search for relativistic MOND

**Date:** 2026-08-29
**Directory:** `qwen_claude_field_theory/closure_2026/mond_compiler_2026/`
**Arm:** covariant finite-operator-basis arm (stages 1, 2A, 2B, 3-synthesis).
A parallel *response-space* arm ran in the same directory and is complementary on exactly one
axis: it admits `k^-2` (nonlocal) kernels, which this basis excludes. Its results are quoted
here where they bear on the verdict, and are always labelled as its results, not mine.

---

# VERDICT: **NO_GO_STRENGTHENED**

Zero candidates in the searched class satisfy G1–G5 together. The emptiness is not a
null result: it resolves into a **dichotomy theorem** that extends the Part-I lensing no-go
to two classes Part I explicitly did not cover — metric-affine / algebraic (degenerate)
auxiliary carriers, and frame-carried (TeVeS-type disformal) MOND.

**It is NOT a claim that relativistic MOND is impossible.** Four named doors are open, one of
them found *by* this search and verified open under exact arithmetic. Section 7 lists them.

---

## 1. The strengthened theorem (Part II)

### Hypotheses

Single physical metric `g` with the gravity sector fixed at `(1/16 pi G) R(g)` (G3 forbids
rescaling it). Carrier multiplet: shift-symmetric scalar `phi`, constitutive scalar `chi`,
vector `A_mu`, symmetric-traceless `S_mn`, Lagrange multiplier `lam`. Matter couples only
through the frame map

```
g~_mn = e^{2(M1 phi + M2 chi)} ( g_mn + M3 A_m A_n + M4 S_mn
                                     + M5 phi A_m A_n + M6 phi S_mn
                                     + M7 d_m phi d_n phi + M8 phi d_m phi d_n phi )
```

Operators: **local**, **≤ 2 derivatives**, **≤ degree 4 in the carrier**, no free functions of
the carrier, no extra mass scales, no torsion, no parity-odd (Levi-Civita) operators, no
Riemann/Weyl couplings, no second copy of any irrep, **no nonlocality**. 57 operators + 8
frame parameters = **65 searchable coefficients** (`basis.json`).

### Statement

> **(P) — the forcing.** G2 (lensing tracks dynamics in the matter frame) forces a matter-frame
> disformal coupling to a carrier VEV with a **nonzero timelike component**:
> `M5 = 4 M1 (1 - M3)/A_0^2` on the vector route, `M6 = 6 M1 / S_00` on the tensor route.
> Both diverge as the timelike component goes to zero, and both are nonzero for every
> `M1 != 0`. *(Independently re-derived: `s3_synthesis_verify_2026.py` C3, C5, D1, D2.)*
>
> **(a) — carrier with a derivative operator.** Its boost orientation then propagates, and the
> same disformal coupling that supplied G2 sources it from `T~^{0i}`: the matter-frame metric
> acquires `g~_0i = -(M3 + M5 phi) w_i`, whose `M5 phi` piece is *not* removable by a
> coordinate boost because `phi` varies in space. In the only instance the basis actually
> realises (`F_mn F^mn` as the sole vector-kinetic operator), the failure is worse than large:
> `c123 = 0` **exactly**, so the quasi-static longitudinal operator `D(k) = (c1-c4) k^2 (k.v)^2`
> vanishes identically on the whole plane `k.v = 0` where the G2-forced source has support —
> the PPN boundary-value problem is not elliptic and `alpha_2` is a **pole**, not a number.
> Simultaneously the longitudinal channel has time-kinetic coefficient `1/2` and gradient
> coefficient `0`, i.e. `c_s^2 = 0` exactly: **infinite strong coupling, not a second-class
> constraint**, so G5 fails on the same operator. `alpha_1 = -2`.
>
> **(b) — carrier with no derivative operator (degenerate / Palatini branch), matter coupling
> retained.** The orientation moduli have no field equation of their own. Their would-be
> equation is the transverse projection of the matter coupling, which is not an equation for
> the carrier at all but an **over-determining constraint on matter**: `u^mu || A^mu` (vector)
> or `[S, T~] = 0` (tensor). G4 and G5 fail together; there is no solution for matter in motion
> relative to the carrier's own frame.
>
> **(c) — degeneracy made structural, matter coupling dropped.** For the only ≤2-derivative
> **isotropic** algebraic carrier `C^{ab} = P g^{ab}`, the degenerate branch `P = 0` has
> `dim ker = 4` and the trace-free stress **vanishes identically** in `A` and in `g`. The
> carrier's entire stress is `-a0^2 V g_mn`, a cosmological constant: the field equations are
> exactly GR + Lambda, `mu == 1`, no MOND. `Phi - Psi = 0` and `alpha_1 = alpha_2 = 0` hold
> **exactly but vacuously**. *(Independently re-verified: E2.)*
>
> **Therefore: within this class, G2 and G4 cannot be satisfied simultaneously.**

### What this adds to Part I

Part I forbade `Phi = Psi` for **local, ≤2-derivative, single-metric, non-degenerate** constraint
MOND, and explicitly did not cover degenerate carriers, higher irreps, or constrained-multiplier
sectors. Part II covers those three, plus the frame-carried route, and kills them **at a
different gate**:

| escape from Part I | how it evades Part I | where it dies now |
|---|---|---|
| degenerate carrier, `det H = 0` | no isotropic-Legendre structure | G2: zero traceless stress (c) |
| higher irrep (traceless `S_mn`) | independent traceless stress exists | G4+G5: `[S,T~]=0`, 6 undetermined moduli |
| constrained-multiplier vector | unit-norm `lam` sector | G4+G5: pole / over-determination (a),(b) |
| frame-carried (TeVeS) | `Sigma_P` becomes a ~1e-7 effect | G4+G5: `M5` forced, then (a) |

---

## 2. Basis and exclusions

**65 coefficients** = 57 covariant operators + 8 matter-frame parameters
(`basis.json`, groups P/V/D/K/C).

**Deliberately excluded (11, all recorded machine-readably in `basis.json`, none silent):**
torsion; >2 derivatives; degree >4 in the carrier; Riemann/Weyl couplings; parity-odd
(Levi-Civita) operators; **nonlocal `box^-1` / `k^-2` kernels** (the most important one —
locality is an explicit Part-I premise, so leaving it is a separate programme, and it is
exactly where the parallel arm goes); second copies of an irrep; free functions of the carrier
(`chi`'s potential capped at quartic — this is the anti-hiding discipline, and it bites: the
compiler *reports* `mu(y) = (sqrt(k^2+4y)-k)^2/(4y)` rather than being handed `1-e^{-y}`);
extra mass scales; matter couplings beyond the frame map; `S_0z` in the static reduction only.

**Capped, not dropped:** the disformal coefficients are degree ≤1 polynomials in the carrier
(`M3 + M5 phi`), not free functions. Degree 0 was provably too small — it excludes Bekenstein's
construction, the only known G2 pass — and admitting degree 1 changed the result qualitatively.

**UNRECORDED TRUNCATION FOUND AND REPORTED (not hidden):** the Einstein-aether operator
`c4 = (A^m nabla_m A_a)(A^n nabla_n A^a)` is 2-derivative and degree 4 — **inside every stated
cap** — yet it is absent from the 57 and absent from the exclusion list. Verified independently:
the basis' whole vector-kinetic sector `{K3, K4, K5}` maps to Einstein-aether as
`c1 = 2 aK4 + aK5`, `c2 = aK3`, `c3 = -2 aK4`, **`c4 = 0` identically** (B2). Since Foster–Jacobson
gives `alpha_1 = -8(c3^2 + c1 c4)/(2c1 - c1^2 + c3^2)`, at `c4 = 0` the condition `alpha_1 = 0`
collapses to `c3 = 0` alone (B5). **Branch (a) was searched only on the `c4 = 0` slice.** This is
a genuine scope hole and is listed as an open door (§7.2).

---

## 3. Mortality table (stage 1) — 108,000 candidates

100,000 main screen + 8,000 corrected `FRAME_TUNED2` re-run. Gates short-circuit in order.

| gate | killed | % | note |
|---|---:|---:|---|
| Gate-H | 27,209 | 25.19% | robust ghost: negative kinetic eigenvalue at **every** reference background |
| Gate-CARRIER | 33,125 | 30.67% | 18,129 `CARRIER_OFF` (physics) + 14,996 `NO_SOLUTION` (solver) |
| Gate-MOND | 14,520 | 13.44% | 11,965 physics + 2,555 solver. `MU_CONSTANT` 3,210; `NO_NEWTONIAN_REACH` 2,284; `NO_DEEP_MOND_REACH` 2,214; `G3_FAIL` 120 |
| Gate-SLIP | 1,112 | 1.03% | lensing does not track dynamics (all frame-slip kills) |
| Gate-H2 | 2 | 0.00% | ghost at the candidate's **own** solved background |
| Gate-PPN | 59 | 0.05% | preferred-frame carrier vacuum |
| TUNING_FAILED | 31,973 | 29.60% | the targeted tuning had no root; candidate never constructed |
| **SURVIVOR** | **0** | **0.00%** | |

**Reached-gate profile:** entered the chain 76,027 → Gate-CARRIER 48,818 → Gate-MOND 15,693 →
Gate-SLIP 1,173 → Gate-H2 61 → Gate-PPN 59 → survivor 0.

**Honest partition of the 108,000** (independently recounted, `s3` A2/A4/A5, sums exactly):

```
  58,417  physics kills
  17,551  solver non-convergence   -- UNDECIDED, not a physics result
  31,973  never constructed        -- tuning had no root; says nothing about the basis
      59  gate-UNDECIDED at stage 1 -- Gate-PPN was a PROXY, not a computation
       0  survivors
```

The 59 were subsequently **decided** by stage 2A's exact certificate (§4), not by the proxy.

---

## 4. Certificates

Stage 2A produced **40 machine certificates** in exact rational sympy (34 PROVEN,
4 COMPUTATIONALLY_VERIFIED, 1 PARTIAL, 1 ASSUMED, 0 fabricated) for the three deepest
non-survivors. Stage 2B produced 35 + 19 + 10 independent adversarial checks. Stage 3
(this synthesis) added **37 independent checks, 37/37 passing**.

### The three deepest, and how they die

| candidate | G1 MOND | G2 LENS | G3 NEWTON | G4 PPN | G5 HEALTH |
|---|---|---|---|---|---|
| **C1** Maxwell aether + Bekenstein disformal (= TeVeS, rediscovered) | PASS | PASS | PASS\* | **FAIL** | **FAIL** |
| **C2** algebraic (kinetic-free) aether | PASS | PASS | PASS | **FAIL** | **FAIL** |
| **C3** algebraic traceless tensor `S_mn` | PASS | PASS | PASS | **FAIL** | **FAIL** |

\* G3 passes once `G_N` is the *measured* constant; the Maxwell aether renormalises the bare `G`
by `G_N/G_bare = 4/3 = 1/(1 - c14/2)` with `c14 = 1/2`. Three independent routes agree
(stage-2A exact static solve; stage-2B `R2b` from-scratch quadratic action; the Einstein-aether
formula). A renormalisation, not a repair. It leaves the separate testable
`G_cosmo/G_N = 1 - c14/2 = 3/4` (BBN).

**Identification (stage 2B, independent):** 59 of the 61 deepest share one 6-operator core
`{P2, V3, V15, K4, M1_conf, M5_disf}` with `M5/M1 = 4.000` (min 3.999716, max 4.000236) — they
**are Bekenstein TeVeS**, rediscovered from a 65-parameter basis. Linearising
`g~ = e^{-2 lam phi}(g + AA) - e^{+2 lam phi} AA` gives `M1 = -lam`, `M5 = -4 lam` exactly.

### Load-bearing certificates

| # | claim | status |
|---|---|---|
| C1-G1 | `mu(y) = [(sqrt(k^2+4y)-k)/2]^2 / y`, `k^2 = 3 sqrt 2` exact; `mu -> 1`, `mu -> y/k^2`. A genuinely nonlinear interpolation **output** by eliminating algebraic `chi`, no free function supplied | PROVEN |
| C1-G2 | `Phi~' - Psi~' == 0` on shell; the structural condition is `M5 = 4 M1 (1 - M3)` | PROVEN |
| C1-G4 | `c123 = 0` exactly; `D(k) = (c1-c4) k^2 (k.v)^2` vanishes on `k.v = 0` where the source lives ⇒ not elliptic, `alpha_2` is a pole | PROVEN |
| C1-G4 scope | the only regulator (`lam_bar` from the unit-norm multiplier) is `O(G rho)` and vanishes in vacuum, where PPN is defined | **PARTIAL** |
| C1-G4 numbers | Foster–Jacobson at `(c1,c2,c3,c4) = (1/2,0,-1/2,0)` ⇒ `alpha_1 = -2`, `alpha_2` denominator identically 0 | **ASSUMED** (literature cross-check) |
| C1-G5 | longitudinal channel: time-kinetic `1/2`, gradient `0` ⇒ `c_s^2 = 0`. Hessian direction **not** null ⇒ strong coupling, **not** second-class | PROVEN |
| C2-G4 | transverse `A`-equation is not an equation for `A`; forces `u || A` (matter comoving with the aether) | PROVEN |
| C3-G4 | carrier side is a matrix polynomial in `S`, so it commutes with `S`; the equation forces `[S, T~] = 0` | PROVEN |
| C2/C3-G5 | 3 boost moduli (C2) / 6 Lorentz-orbit moduli (C3) have identically zero action and no secondary constraint: **undetermined functions**, not second-class constraints | PROVEN |
| S6 | the dichotomy theorem itself | PROVEN (over this basis) |
| S0 | basis truncation `c4 = 0` — **reported, not hidden** | PROVEN |
| s3 C3/C5/D1/D2 | **(P)**: G2 forces `M5 ∝ 1/A_0^2`, `M6 = 6 M1/S_00` — nonzero **timelike** VEV forced | PROVEN (independent) |
| s3 E2 | isotropic algebraic degenerate ⇒ `Sigma_P == 0` identically | PROVEN (independent) |
| s3 F1–F5 | anisotropic **structural** degenerate ⇒ exact shift invariance, `dim ker = 1`, nonzero `c`-independent traceless stress | PROVEN (independent) |
| s3 G1–G3 | Part-I slip magnitude, exact ODE solve | PROVEN (independent) |
| s3 B2–B5 | `c4 = 0` slice, and `alpha_1 = 0 ⇒ c3 = 0` there | PROVEN (independent) |
| s3 I1–I5 | the surviving direction's preferred-frame pass is **kernel-fork dependent**: frozen `1-e^{-y}` passes hugely, the framework's canonical kernel exceeds the `alpha_2` bound 1.8x–197x from Saturn outward | COMPUTATIONALLY_VERIFIED (independent) |

Scripts (all committed, all self-checking, all run clean):
`mc_screen.py`/`mc_gates.py`/`mc_report.py` (stage 1) ·
`s2a_static_exact_2026.py`, `s2a_ppn_exact_2026.py`, `s2a_report_2026.py` (stage 2A) ·
`stage2b/s2b_palatini_identity_2026.py` (10/10), `stage2b/s2b_degenerate_branch_2026.py` (35/35),
`stage2b/s2b_refute_2026.py` (19/19) · **`s3_synthesis_verify_2026.py` (37/37, `.out` committed)**,
which imports nothing from any of them and reads `screen_results.json` / `basis.json` as data only.

---

## 5. The live lead, resolved: the Palatini degenerate archetype

`R(Gamma) = R(g) - 3 div A + 3 A^2` **verified independently** (exact rational jets, 4 random
metrics; coefficients metric-independent). Closure PROVEN by enumeration: a torsion-free vector
distortion reaches the action only through `{div A, A^2}`, and `div A` is a total derivative at
constant coefficient — so the **only** channel is `A^2`, with coefficient `P(chi) = 3 + 25 chi`.

On the degenerate branch `chi = -3/25`:

* `A` is nonzero, but `A^2 = a0^2 V'(-3/25)/25` is a **universal constant** (`V'` is evaluated at
  the frozen `chi`), and its **direction is fixed by no field equation**. A constant-norm vector
  cannot track `|grad Phi|/a0`: **G1 is dead before the stress question is even asked.**
* The same `P(chi)` that degenerates the `A`-equation multiplies the entire carrier stress:
  `T_mn = -a0^2 V g_mn` exactly ⇒ `Sigma_P == 0` ⇒ **G2 has no source**; `mu == 1`; GR + Lambda.
* `Phi - Psi = 0`, `alpha_1 = alpha_2 = 0` **exactly — and vacuously.**
* G5 is **PARTIAL**: the bracket matrix has rank 2 on this branch; `(A_parallel, dchi)` *is* a
  genuine second-class pair, but the **3 transverse components are undetermined multipliers**,
  not second-class. This is not "det H = 0 with a genuine second-class constraint" in Part I's
  sense. It is also *not* strong coupling — the degeneracy is exact, not a limit.

**The archetype is CARRIER_OFF in disguise.** Escapes E1–E5 each followed to death in the log
(`D1 chi div A` → minimally coupled quintessence; `K3` → `A_0` a ghost; `K4` → back to the aether
jaw; `C4` → background-dependent, non-constant rank; matter coupling → over-determined; tensor
`chi^{ab}` → no metric dependence, zero stress by construction).

---

## 6. Two findings that cut FOR the candidate class (reported because they weaken my own verdict)

### 6.1 Part I is a true theorem whose observable size is ~1e-6

Solving the linearised slip ODE **exactly** for a deep-MOND point mass (not a scaling estimate:
`s3` G1–G3, sympy, residual 0):

```
  Pi = (1/4 pi G) mu |grad phi|^2 ,   D'' - D'/r = 8 pi G Pi
  =>  D = Phi - Psi = (2/3) G M sqrt(G M a0) / r          (exact particular solution)
  =>  |d(Phi-Psi)/dr| / |dPhi/dr| = (2/3) G M / (r c^2)
  =>  peaks at the MOND radius at (2/3) v_flat^2 / c^2
```

| system | `(2/3) v_flat^2/c^2` |
|---|---|
| dwarf, 40 km/s | 1.19e-08 |
| Milky Way, 220 km/s | 3.59e-07 |
| massive spiral, 300 km/s | 6.68e-07 |

So in the **metric-carried** class, Part I's `Sigma_P != 0` obstruction produces a fractional
lensing-vs-dynamics discrepancy of order 1e-8 to 1e-6 — **unobservable.** Part I remains exactly
true and is not withdrawn; what is corrected is its *use*. **G2 as written is ambiguous**: it
conflates a mechanism (`T^carrier_{ij,TF} != 0`) with an observable (`Phi = Psi`, both enhanced),
and the two readings select different theories. The deepest candidates pass G2 observationally
(metric-carried fraction ~1e-7) and fail its mechanistic parenthetical.

**Consequence for the programme:** lensing is *not* the binding constraint on metric-carried
MOND. The binding constraints are G4 and G5. Future rounds should gate on the observable.

### 6.2 Gate-PPN's kill rule is not a theorem

The forward direction (boost-invariant vacuum ⇒ `alpha = 0`) is sound; **the converse is false**,
and the degenerate Palatini branch is an explicit counterexample — a timelike, boost-breaking
carrier VEV with `alpha_1 = alpha_2 = 0` **exactly**. Stage 1 therefore *undecided* 59 candidates
rather than refuting them; they were decided later, at 2A, on exact grounds.

Two further leniencies, both recorded: Gate-H2 passed the deepest candidates while leaving up to
13 null directions unclassified (gauge vs strong coupling not separated); and stage-1's Gate-MOND
scored `mu` against the pure-GR reference `g_N = Sigma/8`, which is the **wrong** Newtonian
reference for any candidate with a vector kinetic term (`G_N/G_bare = 4/3` there). Both errors
run toward leniency, so neither manufactures the zero — but the affected candidates are exactly
the deepest ones, and it is only stage 2A's exact certificate that decides them.

---

## 7. OPEN DOORS — what this verdict does **not** close

### 7.1 Structurally-degenerate **anisotropic** carrier (found by this search; recommended next target)

For any algebraic carrier `S = int sqrt(-g)[ C^{ab} A_a A_b + B^a A_a + L_0 ]` with `C^{ab} n_b = 0`
there is a trichotomy: (i) `B.n != 0` → over-determined; (ii) **structural** degeneracy (holds
identically in `g`) → `A -> A + c n` leaves `L` exactly invariant, `dT_mn == 0`, **well-posed**;
(iii) **configurational** degeneracy → `dT_mn != 0`, ill-posed with non-constant rank.

*Corollary 1 (CLOSED):* the isotropic case `C = P g` — the only ≤2-derivative option without a
curvature coupling — has `dim ker = 4`, so `Sigma_P == 0`. The archetype's whole class is closed.
This is the vector-sector twin of Part I's "the same `mu` controls the Gauss law and `Sigma_P`".

*Corollary 2 (**OPEN**):* `C^{ab} = N(q^a q^b - q^2 g^{ab})` with `q_a = d_a chi` has
**`dim ker = 1`**. Independently verified (`s3` F1–F5): exact shift invariance in the metric,
null direction `= q`, and a **nonzero traceless stress that is independent of the undetermined
component**. Well-posed, non-propagating in `A`, **and** a lensing source. Eliminating `A` returns
`L_eff = (1/(4 N q^2))[B^2 - (q.B)^2/q^2]` — a non-polynomial function of the kinetic invariants
generated from a *finite* operator basis, i.e. it respects the anti-hiding discipline.

**Named liability before anyone gets excited:** `q_a = d_a chi` carries a derivative, so `chi`
propagates and the preferred-frame question re-enters through `chi`. Untested: whether the
traceless stress actually **cancels** `Sigma_P` on shell (profile-matching is necessary, not
sufficient — that is the lesson that refuted the parallel arm's S3), DOF/Dirac rank, `alpha_1`,
`alpha_2`, `c_T`, cosmology.

### 7.2 The `c4 = 0` truncation

`(A^m nabla_m A_a)(A^n nabla_n A^a)` is 2-derivative, degree 4, inside every stated cap, and
missing. Branch (a) of the theorem was searched only on the `c4 = 0` slice of Einstein-aether,
where `alpha_1 = 0` forces `c3 = 0`. **A direct 1PN solve on the `c4 != 0` slice is the cheapest
way to widen or break the no-go.** Note this hole does *not* reopen the `M5 phi` channel: that
preferred-frame term is additive and carries a different radial profile
(`phi ~ sqrt(G M a0) ln r` vs `U ~ G M/r`), so no aether tuning cancels it at more than one
radius. But see §8 — its observational magnitude was never computed by anyone.

### 7.3 Nonlocality (basis exclusion #6, and an explicit Part-I hypothesis)

`FROZEN_PRIMITIVE.md` carries a causal nonlocal single-metric primitive with the exact kernel
`F+(Z) = 4[1 - (1 + sqrt Z/2) e^{-sqrt Z/2}]` ⇒ `mu(y) = 1 - e^{-y}` exactly. Its architecture
passes: single metric, causal nonlocal, MOND weak field, BTFR, leading spherical lensing,
`c_T = 1` at quadratic TT order. **Every closure gate is unrun:** causal variational formulation,
localization, full nonlinear DOF/Dirac rank, `alpha_1`, `alpha_2`, `Z < 0` / cosmology. Banked
warning: a previous localization of a closely-related model found a genuine scalar characteristic
`omega^2 = (1/2) c^2 k^2` even after removing the naive localization ghost, so localization is not
automatically harmless.

### 7.4 The parallel arm's `lambda_K != 1` khronometric route — the session's surviving direction

Keeps MOND (`G_eff = G/mu`), and the static gates force the `a.a` coefficient to
`alp_kh(y) = 2(1 - mu(y))`, hence `alpha_1 = -8(1 - mu(y))`, `alpha_2 ≈ -(1 - mu(y))` — generated
by the lapse-tied MOND sector alone. The parallel arm calls this **MOND self-screening**: the
preferred-frame coupling rides on the MOND *deviation* `1 - mu`, which vanishes where PPN is
measured, whereas AeST's rode on the constant `K_B`. Its headline is "the `alpha_2` pole that
killed AeST is beaten by ~30000 orders."

**That headline is KERNEL-FORK DEPENDENT and must not be quoted unqualified.** Computed both ways
here (`s3` I1–I5, and the arithmetic is in the log, not asserted):

| location | `y = g_bar/a0` | `\|alpha_1\|` frozen `1-e^{-y}` | `\|alpha_1\|` canonical | `\|alpha_2\|` canonical | vs `4e-7` |
|---|---:|---:|---:|---:|---|
| Earth 1 AU | 6.34e7 | underflow | 6.31e-08 | 7.89e-09 | PASS |
| Saturn 9.5 AU | 7.02e5 | underflow | 5.70e-06 | 7.12e-07 | **FAIL 1.8x** |
| Neptune 30 AU | 7.04e4 | underflow | 5.68e-05 | 7.10e-06 | **FAIL 17.8x** |
| 100 AU | 6.34e3 | underflow | 6.31e-04 | 7.89e-05 | **FAIL 197x** |

With the **frozen** exponential kernel the suppression is structural and the gate is passed
enormously. With the **framework's own canonical** kernel `g_obs = sqrt(g_bar^2 + g_bar a0)`
(⇒ `mu = sqrt(y/(y+1))`, `1 - mu -> 1/(2y)`, verified I1) the suppression is only power-law and the
same construction **exceeds the `alpha_2` bound throughout the outer solar system**.

**A caveat that cuts against BOTH readings (I5):** standard PPN assumes *constant* alphas, but
`alp_kh` runs with position through `y`, so the bound assignment is not rigorous in either
direction. The fork is **unresolved**, and it decides this door.

**Also untested:** `c_T`, BBN `lambda_K in [0.923, 1.100]`, cosmology, khronon stability, and the
DOF count — which is **3, not 2** (2 tensor + 1 khronon), and which *jumps* between vacuum and
excited states. The healthy branch requires `lam2 != 0`; at the Einstein–Hilbert point `lam2 = 0`
the khronon is infinitely strongly coupled (the Horava `lambda -> 1` disease), which is where the
2-DOF version of this candidate died.

### 7.4b Closed while this verdict was being written (parallel arm, commits `a9261161`, `afaad0e6`)

The **linear-curvature-coupled trace-free auxiliary carrier** class (`THEORY_CLASS_2026.md`'s
design: `Q^ij[f(chi) A_ij + lambda R_ij]`) is **DEAD**, by order counting, 19/19 exact sympy:
`Sigma_P` is the unique `(eps^2, Phi^2)` traceless stress; the designed canceller
`Sigma_AR = lambda f A KK^{-1} R` is `(eps^3, Phi^2 Psi)` — one `eps`-order too high, because
`KK^{-1} ~ 1/k^2` shifts *derivative* order, never `eps`-order. The only same-order carrier stress
`Sigma_RR` is pure-curvature (`Psi^2`), spin-0 only, so it cannot match `Sigma_P`'s spin-2 part for
any `(lambda, KK)`; and its `y`-weight is constant while `c(y) = mu(y)` is not. **Part-I/T3 upgrades
to forbid linear-curvature-coupled trace-free auxiliary carriers**, and the parallel arm declares
the local 2-DOF auxiliary-carrier programme closed.

*Consistency note, both ways:* that kill is a **mechanistic-G2** kill (`Sigma^TF_total != 0`, so
`Phi != Psi`). Under the **observational** reading of G2 established in §6.1 it is not a kill at
all — a residual `Sigma_P` buys only a ~1e-6 fractional slip. The two results do not contradict
each other; together they say the *design target* was misplaced, not that the algebra was wrong.
This is precisely the G2 ambiguity, and it now has a body count on both sides.

### 7.5 Everything the basis excluded by construction

Torsionful Palatini distortion (**out of scope, not failed** — the probe returns terms linear in
`A` with no derivative, the tell-tale of a non-covariant remainder, plus a genuine curvature-
convention ambiguity); >2 derivatives (Horndeski/Galileon, `f(R)`, Gauss–Bonnet); degree >4;
Riemann/Weyl couplings; parity-odd operators; second copies of an irrep; free functions of the
carrier; extra mass scales; richer matter couplings (pressure/shear).

---

## 8. What is NOT established (stated so nobody quotes it as settled)

1. **The general form of branch (a) is structural, not quantified.** The exact kill (pole +
   `c_s^2 = 0`) is proven for `c123 = 0`, the only vector-kinetic structure the basis realises at
   the deepest point. For a general `c123 != 0` carrier the argument is the `M5 phi w_i`
   certificate plus a profile-mismatch no-cancellation argument. **Nobody computed the
   observational size of the `M5 phi` term against the `|alpha_1| < 1e-4` bound.** It is an open
   number, not a bound comparison.
2. `alpha_1 = -2` for C1 is **ASSUMED** (Foster–Jacobson evaluated at the derived `c_i`), and the
   `alpha_2`-pole scope certificate is **PARTIAL** (the vacuum/inside-matter distinction).
3. 17,551 solver non-convergences are **undecided**, not physics. 31,973 tuning failures say
   nothing about the basis.
4. The screen never independently tested Part I's `Sigma_P` branch: **every** lensing kill in the
   run is a frame-slip kill (its own `metric_carried` sweep reached Gate-SLIP zero times). Part I
   is inherited here, not reproduced.
5. `c_T`, cosmology, BBN, structure formation, Cassini and the fold/caustic gates were **never
   run** on anything in this arm. Nothing here is a full closure of any candidate.

---

## 9. Process notes (recorded rather than quietly repaired)

* Stage 2B's **first draft** of the algebraic-carrier theorem claimed anisotropic degenerate
  carriers are always ill-posed. The machine check **refuted it** and forced the
  structural/configurational split — which is what produced open door §7.1.
* Stage 2B's **first pass** on failure mode (a) examined only the scalar sector and concluded "no
  bare-`G` rescaling anywhere". Incomplete: the Maxwell aether gives `G_N/G_bare = 4/3`. Corrected
  in Amendment 1, cross-checked three ways.
* The parallel arm's Section D **reconstructed Foster–Jacobson from recall; it was wrong** and its
  checks failed. Rewritten to check only pole structure and discontinuity of in-script formulas.
* The parallel arm's Route-A result S3 ("the carrier cancels `Sigma_P` for a chi-dependent
  kernel") was **REFUTED** by its own stage 4: eliminating a local traceless carrier gives a pure
  redefinition `F(A) -> F(A) - f^2 A^2/(3M)` for *any* local kernel, so hypothesis (H4) is never
  violated and Part I applies verbatim.

---

## 10. One-line summary

Eight chassis died on the lensing/PPN pincer; this compiler searched 108,000 points of a
65-coefficient covariant basis, found **zero survivors**, and converted the emptiness into a
dichotomy theorem that extends Part I to degenerate and frame-carried carriers — while finding,
in the process, that **lensing is not the binding constraint at all** (the Part-I slip is ~1e-6),
that the real wall is **G2 forcing a timelike carrier VEV that G4 then cannot tolerate**, and that
**one anisotropic degenerate carrier survives every argument made here** and is the recommended
next target.

**Recommended next three experiments, cheapest first:**
1. Does the Corollary-2 anisotropic carrier's traceless stress actually *cancel* `Sigma_P` on
   shell, or only match its profile? (Profile-matching is necessary, not sufficient — that is the
   lesson that refuted the parallel arm's S3.) One weak-field static solve decides it.
2. A direct 1PN solve on the `c4 != 0` slice of the aether sector — the one truncation inside the
   stated cap, and the slice where `alpha_1 = 0` is reachable without `c3 = 0`.
3. **Resolve the kernel fork in §7.4**, which is now the single number that decides the session's
   surviving direction. It is a framework-internal question (frozen `1-e^{-y}` vs canonical
   `sqrt(g_bar^2 + g_bar a0)`), not a new physics computation.
