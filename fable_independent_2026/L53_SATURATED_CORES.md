# L53 — the saturated branch where it is actually realised: the non-spherical solve, and what it costs

2026-09-09. Lane L53 of [CHARTER.md](CHARTER.md), opened by [L30_SATURATION.md](L30_SATURATION.md)'s check G4
and [L33_SCALAR_CONE.md](L33_SCALAR_CONE.md)'s check D2.
Script: [L53_saturated_cores.py](L53_saturated_cores.py) → [L53_saturated_cores.out](L53_saturated_cores.out).
**26 PASS, 14 FAIL. All 13 controls PASS** (K0–K7, R4, N1–N5, P4); every FAIL is a substantive finding.
Runtime 144 s. Both footings throughout.

## Verdict in three sentences

The saturated branch — `Δ′ = 0`, `Σ_∥ = 1/Δ′ = ∞`, no cubic action — is **not an ill-posed boundary-value
problem even off spherical symmetry**: it is a *gradient-constrained variational inequality* of
elastic–plastic-torsion type, whose energy stays convex, whose solution exists, is unique (three genuinely
different admissible starting fields agree to `1.4×10⁻¹⁰`) and depends Lipschitz-continuously on the data
(response/ε constant to 0.5% over three decades); `Σ_∥ = +∞` is a **constraint**, `|∇φ| ≤ C a₀`, and only
`Σ_∥ < 0` — which the bounded-boost theorem already forbids — would be genuinely ill posed. It has **not**
been silently affecting this programme's numbers: the degeneracy lives only in the *carrier* reading of the
field equation (in the AQUAL-on-total-potential reading `Δ′ = 0` gives `Σ_∥ = 1` exactly, and QUMOND is
linear in the unknown), and no committed script in the repository runs a multi-dimensional nonlinear carrier
solve. What the lane does buy is one hardening and two corrections: the bounded-boost ceiling becomes a
**pointwise, geometry-free constraint**, so the cluster failure cannot be relaxed by triaxiality and is
strengthened rather than weakened; **L30's address for the branch is wrong about clusters**; and solving the
non-spherical equation instead of applying the algebraic law moves a disc's inner rotation curve by
**2.7 km/s, one-signed and mesh-converged** — small, real, and not zero.

## 1. Where the branch is actually realised (R1–R3b)

Computed from the repository's own committed baryon models: 175 SPARC rotmod files, the cluster measurement
audit, and McMillan 2017 Table 3 (the same parameters `hunt_2026/g02_vertical_vs_planar_frequency_split.py`
uses). Controls K1–K3 first reproduce L30's Solar saturation radius (**0.0242 pc = 4994 AU canonical /
0.0221 pc = 4550 AU alt**), L33's corollary sphere at the same radius, and L30 G4's statement that the
standing coherence length (0.10 / 0.15 pc) **exceeds** it by 4.1× / 6.8×, so the Sun never sits on the branch.

| system | canonical | alt |
|---|---|---|
| SPARC discs reaching the branch anywhere | **37 / 175** | 35 / 175 |
| …out to a median / maximum radius | **3.91 / 7.99 kpc** | 3.80 / 6.94 kpc |
| NGC 2903 (representative saturating disc) | 4.80 kpc | 3.84 kpc |
| NGC 3198 (the archetype) | **never** (max s = 2.166) | never (1.798) |
| DDO 154 (dwarf) | **never** (max s = 0.063, 40× short) | never (0.053) |
| clusters, at any radius the audit tabulates | **0 / 12** (max s = 0.909) | 0 / 12 (0.755) |
| cluster core with a BCG added (M\* = 8×10¹¹ M☉, R_e = 30 kpc) | inside **5.1 kpc** | 3.2 kpc |

**R2 FAIL and R3 FAIL are corrections to L30 §7**, which gave the branch's address as "the inner few
kiloparsecs of *every* galaxy and the cores of clusters." Neither half survives contact with the data:

- it is realised in the inner few kpc of the **baryon-densest fifth** of SPARC discs, not of every galaxy —
  138 of 175 never reach it, the archetype NGC 3198 included, and no dwarf comes within a factor 40;
- at **no radius the cluster audit tabulates** does `g_bar` reach `s_sat a₀`, at either footing. 144 of the
  248 audit rows already include BCG stars and none of them saturates either. Adding a BCG explicitly puts
  the branch inside ~5 kpc — **inside the audit's innermost radius of 30 kpc**, i.e. the branch exists in
  cluster cores but nowhere the cluster failure is actually measured.

## 2. The mathematical core: what infinite longitudinal stiffness is (M1–M5)

Write `u = |∇φ|/a₀` and `σ(u) = s(u) = Δ⁻¹(u)` — the Newtonian source magnitude that produces that gradient.
The static equation is the Euler–Lagrange equation of

    E[phi] = INT [ W(u) + q phi ] dV ,   W'(u) = sigma(u) ,
    Sigma_perp = sigma(u)/u = J_Y ,   Sigma_par = dsigma/du = 1/Delta' ,

and `Σ_⊥`, `Σ_∥` are *exactly* the two eigenvalues of the energy density's Hessian.

**THEOREM L53-1 (the classification).** On the published kernel `Δ` is flat above `s_sat`, so `σ(u)` has a
**vertical segment at `u = C = 0.647610`**: any source `s ≥ s_sat` produces the same gradient. That is a
*maximal monotone graph*, hence the subdifferential of a convex function, and the correct statement of the
boundary-value problem is a **variational inequality with the pointwise gradient constraint `|∇φ| ≤ C a₀`** —
formally the elastic–plastic torsion problem of Brezis–Stampacchia. `Σ_∥ = +∞` is a **constraint, not a loss
of ellipticity**. The dangerous case is `Σ_∥ ≤ 0`, and measured on the alternative — continuing ν_RAR past
its maximum instead of truncating — `Σ_∥ = −5.5×10³` at `s = 100` and `Δ` falls from 0.6476 to 0.0718 over
`s = 2.54 → 40`, i.e. a non-monotone `σ(u)`, a non-convex energy, and a genuinely ill-posed problem.
**The truncation is the repair, not the disease.**

Verified on the actual non-spherical disc problem, not asserted:

| property | test | result |
|---|---|---|
| strict convexity (M4a) | min eigenvalue of the element Hessian over 30 318 triangles | `Σ_⊥ ≥ 0.214`, `Σ_∥ ≥ 0.475`, both **> 0** |
| uniqueness (M4b) | three different **admissible** starts: 0.9× tapered, the deposited-kernel solution, the L30-repair solution | agree to `1.4×10⁻¹⁰` in `‖φ‖`, `6.4×10⁻⁷ a₀` in `∇φ` |
| continuous dependence (M5) | source perturbed by ε = 10⁻⁴, 10⁻³, 10⁻² | response/ε = 0.2424, 0.2422, 0.2412 — **Lipschitz to 0.5% over three decades** |

One practical warning falls out: an **inadmissible** start (`|∇φ| > C a₀` anywhere, i.e. infinite energy) does
not converge at all — 200 Newton steps and still `3.5×10⁻⁴` away. Anyone solving this equation must start
inside the constraint set. What genuinely fails is **`C²` regularity at the free boundary**, and the cubic
action, exactly as L30 and L33 said — not existence, not uniqueness, not continuous dependence.

### The localisation, and why nothing was silently affected (M3, M4)

Three readings of the modified field equation appear in this repository and they do **not** share the pathology:

| reading | equation | `Σ_∥` at saturation |
|---|---|---|
| **carrier** (THE_ACTION §1, PAPER5 §7, g03x) | `div[J_Y(\|∇φ\|²)∇φ] = 4πGρ`, `g = g_N + g_φ` | `1/Δ′` → **∞** |
| AQUAL on the total potential (g03c, g03d, f24, aqual_efe_full_solve) | `div[μ(\|∇Φ\|/a₀)∇Φ] = 4πGρ` | `1/(1 + Δ′)` = **1 exactly** |
| QUMOND (g02, k04, hunt_efe_lib, every non-spherical solve in hunt_2026) | `div grad Φ = div[ν(\|∇Φ_N\|/a₀)∇Φ_N]` | **linear** in the unknown |

Scripted, not asserted: of **133** committed `.py` files that mention `J_Y`, only **2** also build a spatial
grid, and the sparse operators those assemble are **tridiagonal (1-D radial)** or the grid solve is of a
**linear** operator. Every other use of `J_Y` is the algebraic relation `J_Y(g_φ)g_φ = g_N` on a sphere, or
symbolic. **The only multi-dimensional nonlinear carrier solve in the repository is this lane's own**, so no
committed number was computed on the degenerate operator. The liability was real and worth checking; it has
never been drawn on.

## 3. The solver, and its noise floor (N1–N5)

Axisymmetric P1 finite elements, damped Newton with a sparse direct solve, the Newton decrement as the
convergence measure and Armijo on the energy, plus a fraction-to-the-boundary safeguard that keeps every
iterate inside `|∇φ| ≤ C a₀`. Two details cost real work and are recorded because they are traps:

1. **the energy must be built by Legendre transform**, `W(u) = u·s(u) − Ψ(s(u))` with `Ψ(s) = ∫₀ˢ Δ dt`.
   Tabulating `W` directly in `u` is fatal — near the ceiling `s(u)` is near-vertical, a piecewise-linear
   table's derivative is a staircase, and the line search then compares energies whose difference is smaller
   than the interpolation error and stalls;
2. **the residual is the wrong convergence measure on this branch.** It is measured in the stress variable
   `s = J_Y u`, whose derivative with respect to `u` is `Σ_∥ = 10⁸` — it stalls at an enormous value while the
   field itself is converged to `10⁻¹⁰`.

| control | result |
|---|---|
| **N1** MacLaurin interior field of a homogeneous oblate spheroid (`c/a = 0.5`) — a NON-SPHERICAL analytic result at finite stiffness | max relative error **1.73%** |
| **N2** the nonlinear carrier on a spherical Plummer source vs the exact algebraic law, three meshes | **5.18% → 2.84% → 1.44%** as `h` halves: first order, converging |
| **N3** spurious misalignment on that spherical source (exact answer: exactly radial) | **11.3° → 4.70° → 2.12°**: discretisation, with a known scale |
| **N4** the kinematic bound `\|∇φ\| ≤ C a₀` | max `u` = 0.647610 vs C = 0.647610 |
| **N5** disc carrier solve, three meshes (6 077 / 15 416 / 36 288 nodes) | converged to <1% at **R = 4, 6, 8.2, 12, 20 kpc**; **NOT** converged at R = 1, 2, 3 kpc |
| **P4** regularisation: `Σ_∥` capped at 1e4 vs 1e8 | **0.018 km/s** in `V_c` — the constrained limit exists and is what is computed |

Rows at R ≤ 3 kpc are reported as **bounds**, never as measurements. The bulge cusp (`ρ ∝ r^−1.8`) and the
cylindrical axis are what refuse to converge there.

## 4. The three targets

### (a) The inner rotation curve — the one place something moves (O1 PASS)

Comparing the algebraic prescription the repository uses everywhere (`g_tot = g_bar + a₀Δ(g_bar/a₀)`, both
vectors radial) against the actual non-spherical solve, on the McMillan 2017 Milky Way:

| R [kpc] | s = g_N/a₀ | u solved | u algebraic | ratio | V_c alg | V_c solved | difference | mesh floor |
|---|---|---|---|---|---|---|---|---|
| 1.0 † | 7.959 | 0.5554 | 0.6476 | 0.858 | 157.51 | 154.75 | −2.760 | 0.453 |
| 2.0 † | 5.212 | 0.5111 | 0.6476 | 0.789 | 183.88 | 180.78 | −3.098 | 0.381 |
| 3.0 † | 3.829 | 0.5311 | 0.6476 | 0.820 | 196.86 | 193.77 | −3.086 | 0.200 |
| **4.0** | 2.964 | 0.5599 | 0.6476 | 0.865 | 204.20 | 201.48 | **−2.717** | 0.059 |
| **6.0** | 1.976 | 0.5960 | 0.6419 | 0.929 | 212.93 | 211.01 | −1.928 | 0.017 |
| **8.178** | 1.330 | 0.5887 | 0.6134 | 0.960 | 214.25 | 212.86 | −1.386 | 0.005 |
| **12.0** | 0.690 | 0.5271 | 0.5328 | 0.989 | 205.85 | 205.36 | −0.488 | 0.008 |
| **20.0** | 0.267 | 0.3991 | 0.3947 | 1.011 | 195.51 | 196.16 | +0.649 | 0.031 |

(† = not mesh-converged, a bound.) The carrier's midplane force runs **79–101%** of the algebraic value: a
**one-signed geometric deficit** worth ~1.4% in `V_c`, i.e. **2.7 km/s at the mesh-converged radii**
(3.6 km/s on the alt footing), against a radius-specific mesh floor of at most 0.45 km/s. That is comparable
to the current systematic error on the Milky Way's `V_c` (±2.6 km/s, Eilers et al. 2019).

**Is it saturation, or the disc correction any nonlinear kernel has?** The same equation with an *unbounded*
kernel (`Δ = √s`, no ceiling at all) gives **85–101%**. So the deficit is the generic AQUAL disc correction
**amplified by the approach to the ceiling** — the two effects are comparable at R ≥ 6 kpc and saturation
roughly doubles the deficit at R = 2–4 kpc.

### (b) Vertical structure — invisible (O2 FAIL, O3 FAIL)

`Σ_1.1 = |K_z(R₀, 1.1 kpc)|/(2πG)`, the Kuijken–Gilmore convention, against measurements 71 ± 6 (KG91),
74 ± 6 (Holmberg & Flynn 2004), 68 ± 4 (Bovy & Rix 2013). Note the Milky Way's own footing: `s = 1.318`
(canonical) / 1.094 (alt) at that point — **below `s_sat` — so the solar neighbourhood is not on the branch.**

| footing | Σ_1.1 algebraic | Σ_1.1 solved | difference |
|---|---|---|---|
| canonical, published | 89.31 | 87.64 | −1.67 |
| alt, published | 94.01 | 92.24 | −1.77 |

Max **1.80 M☉/pc²** against a 4 M☉/pc² measurement error and a 2.67 M☉/pc² mesh floor. The direction cosine
of `g_φ` moves by at most 0.027 from the Newtonian one. **The vertical front is untouched.**

The misalignment between `g_φ` and `g_N` — the channel through which a non-spherical solve could differ in
*direction* rather than in magnitude — is likewise not material where the solve is trustworthy:

| region | n | median | 90th pct | max | fraction above the 4.70° floor |
|---|---|---|---|---|---|
| mesh-converged, 4 < R < 20 kpc | 12 787 | 1.46° | 2.78° | 14.34° | 4.2% |
| inner, 1 < R < 4 kpc (bounds) | 5 658 | 2.57° | 15.25° | 46.64° | — |
| the saturated set itself | 3 584 | 2.27° | 12.80° | 61.72° | — |

The large tail lives at R < 4 kpc where the solve is not mesh-converged, so it is a bound. **The non-spherical
solve departs from the algebraic prescription mainly in the magnitude of `g_φ`, not in its direction.**

### (c) Cluster cores — the ceiling becomes geometry-free, which hardens the kill (O4 PASS, O5 FAIL, O6 FAIL)

Recomputed from the repository's own cluster measurement audit:

| footing | radius | n | mean excess | median | max | relaxed mean | mean / ceiling |
|---|---|---|---|---|---|---|---|
| canonical | 40 kpc | 12 | 2.790 | 2.838 | 4.684 | 3.785 | **4.31×** |
| alt | 40 kpc | 12 | 2.316 | 2.355 | 3.888 | 3.142 | **3.58×** |

THE_COMPLETE_THEORY §H-A's **3.37 a₀** sits between the all-cluster mean (2.79) and the relaxed-subset mean
(3.79) at 40 kpc canonical; `3.37/0.6476 = 5.20×`. The worst single cluster is **7.23×** the ceiling.

**The corollary the variational form supplies.** In spherical symmetry the ceiling is a statement about the
algebraic law. In the variational form it is a **pointwise constraint on the solution for any source and any
geometry**: every finite-energy configuration satisfies `|∇φ| ≤ C a₀` everywhere. And because the excess is
the magnitude of a *vector sum*, `|g_N + g_φ| − |g_N| ≤ |g_φ| ≤ C a₀`, **misalignment can only reduce it.**
Tested directly on a flattened (`q = 0.6`) β-model cluster with the BCG of R3b:

| axis ratio | footing | max \|∇φ\|/a₀ | / own ceiling | saturated out to |
|---|---|---|---|---|
| 1.0 | canonical | 0.647610 | 1.0000 | 8.0 kpc |
| **0.6** | canonical | 0.647610 | **1.0000** | 5.0 kpc |
| 0.6 | alt | 0.647610 | 1.0000 | 3.5 kpc |

Flattening changes nothing. **The 4.3× (canonical) / 3.6× (alt) cluster failure against the bounded-boost
ceiling is not an artefact of the spherical solve, and no geometry can rescue it.** That is a hardening of an
existing kill, reported as such and not as a win.

And the 9σ ΔΣ shape error over 0.5–2 Mpc is not on this branch at all: at `r ≥ 750 kpc` the largest `s` in
the audit is **0.170**, fifteen times below `s_sat`. **Nothing in this lane touches it.**

## 5. What the smooth repair changes: essentially nothing (P1–P3 FAIL, P4 PASS)

L30's minimal C² continuation (`D_inf = 0.655589`, `A = 1.317369×10⁻²`, `β = 0.801759`, control K5) differs
from the published kernel by at most **0.008 a₀** and only above `s_sat`:

| target | change under L30's repair | reference scale |
|---|---|---|
| inner rotation curve | **0.186 km/s** | mesh floor 0.453 km/s |
| vertical structure Σ_1.1 | **0.003 M☉/pc²** | measurement error 4 M☉/pc² |
| cluster excess / ceiling | **4.31× → 4.26×** | the failure is untouched |

**The saturation repair is invisible on all three targets.** For contrast the *deposited* kernel
(THE_COMPLETE_THEORY §4.3, `C[1 − W(u)^{−p}]`, control K6) moves the rotation curve by 2.46 km/s and Σ_1.1 by
2.40 M☉/pc² — but that is its different shape at **every** acceleration (0.011 dex over twenty decades), not
the saturated branch: it differs from the published kernel most at R = 6–12 kpc, where `s = 0.7–2.0` and
nothing is saturated. That distinction matters and is easy to get wrong.

## 6. One thing the solve says that the algebraic law does not (M6 FAIL)

Asked of the *solve* rather than of the algebraic law, "on the saturated branch" means "the constraint is
exactly active" — and the approach to the ceiling is astonishingly sharp: `Σ_∥ = 10⁸` requires `|∇φ|` within
`10⁻¹⁵ a₀` of `C`, and even `Σ_∥ = 200` requires it within `3×10⁻⁴ a₀`.

| | volume fraction | radial extent | midplane triangles |
|---|---|---|---|
| what the ALGEBRAIC law calls saturated | 1.26×10⁻³ | R = 0.02–5.04 kpc | 313 |
| what the SOLVE finds saturated | 8.03×10⁻⁴ | R = 0.02–5.16 kpc | 58 |

**54% of the volume the algebraic law calls saturated is not saturated in the solve.** The active set moves
**off the midplane**, and in the midplane at R = 1–4 kpc the solved `|∇φ|` sits 14–21% *below* the ceiling the
algebraic law pins it to. This is the mechanism behind O1's rotation-curve deficit, and it is the one place
where "solve it properly" and "apply the kernel pointwise" give qualitatively different pictures of where the
theory's own pathological branch lives.

## PASS/FAIL, verbatim

See [L53_saturated_cores.out](L53_saturated_cores.out). 13 controls PASS (K0–K7, R4, N1–N5, P4). The 14 FAILs
are: **R2** (the branch is not generic — 138/175 SPARC discs and every dwarf never reach it), **R3** (it is
realised at *no* radius the cluster audit tabulates — L30 §7's cluster address corrected), **M4** (no
committed script solves the carrier equation off spherical symmetry), **M6** (the algebraic law and the solve
disagree about where the branch is active), **O2** and **O3** (the vertical force and the misalignment do not
move), **O5** (non-sphericity does not relax the ceiling — it is a pointwise constraint for every geometry),
**O6** (the 9σ lensing-shape failure is 15× below `s_sat`), **P1**, **P2**, **P3** (the saturation repair
changes none of the three targets), and the three verdict lines **V1** (not a numerical hazard that has been
silently affecting committed solves), **V2** (not a physical effect the programme has been missing in cluster
cores) and **V3** (not entirely without observable consequence — the rotation curve moves by 2.7 km/s).
**V4 PASSES:** the branch is well posed as a variational inequality.

## Scope — what is not done here

The disc solve is axisymmetric; a bar or spiral structure is not modelled. The inner rotation-curve rows at
R ≤ 3 kpc do not mesh-converge and are reported as bounds, not measurements — refining them means resolving
the McMillan bulge cusp and the cylindrical axis, which this lane did not do. The cluster is a β-model plus a
Hernquist BCG normalised to the audit's median `g_bar(40 kpc)`, not a fit to any individual cluster; the
ceiling result (O5) is a theorem about the constraint and does not depend on that model, but the saturated
radii quoted for it do. The coherence operator `ξ²` is absent throughout — this lane solves the `ξ = 0`
carrier equation, which is the right one at kiloparsec scales for any `ξ` the programme carries (0.10 pc to
L30's 4 pc are all ≪ 1 kpc), but it means nothing here bears on L30's Solar-System floor or on L47's
collision. The lensing observable itself is not recomputed; only the acceleration regime the lensing radii
occupy is checked. `a₀` enters the ceiling and the location of the branch but not the well-posedness result,
so the two footings separate only the radii, never the classification.
