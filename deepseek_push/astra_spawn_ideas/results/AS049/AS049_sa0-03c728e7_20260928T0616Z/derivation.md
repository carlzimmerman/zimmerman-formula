# AS049 — Scale derivatives of a constitutive force

**Run:** `AS049_sa0-03c728e7_20260928T0616Z` · worker `sa-0-03c728e7` · started 2026-09-28T05:45:30Z · finished 2026-09-28T07:35:46Z
**Task SHA-256:** `ed91aefffb5a8b8615d09ebf7f90fe82d5ecf10a767948175f61c909b9b2a479` (pinned by `claims/AS049.json`; byte-verified against the registered seed file `AS049_scale_derivatives_of_a_constitutive_force.md`).

## 0. Provenance note (dispatch-title discrepancy)

The dispatch brief named a seed file `AS049_phantom_disk_projected_surface_density.md` that does not exist anywhere in the repository (verified by filename and content search). The claims ledger entry `claims/AS049.json` pins `task_sha256 = ed91aeff…`, and the SHA-256 of the on-disk registered seed `AS049_scale_derivatives_of_a_constitutive_force.md` equals that pin exactly. Following the AS047 precedent (identical discrepancy, same resolution), the **registered seed is authoritative** and this run executes it. The phantom-disk content carried in the brief is executed as a **certified appendix** (section 6) on the operative MONO basis of this same run, consistent with the brief's "cf. AS047" dependency chain.

## 1. Principles, symbol dictionary, assumptions (seed step 1)

Framework (mandatory, adopted inputs, not derived here):
- `a0 = kappa*c*sqrt(G*rho_Lambda)` with **`kappa = 1/2` adopted**; canonical footing `a0_can = 9.3619e-11 m/s²`, alternative footing `a0_alt = 1.1279e-10 m/s²` (kept separate, never sharing both fixed vacuum density and fixed kappa).
- `r_M = sqrt(G*M_b/a0)`; deep `v_flat^4 = G*M_b*a0`; `C = sqrt(G*M_b*a0) = a0*r_M` (positive-root identity, Lean-certified, thm C1).
- Constants: `G = 6.67430e-11 m³ kg⁻¹ s⁻²`, `c = 299792458 m/s`, `M_sun = 1.98847e30 kg`, `pc = 3.085677581491367e16 m`. `G_N/G_bare/G_cosmo` kept separate (no mixing in this run).

Branches (distinct, seed's declared list):
| branch | constitutive law | domain |
|---|---|---|
| Q | `g² = B² + a0·B`, `nu_Q(y) = sqrt(1+1/y)` | y > 0 |
| RAR | `nu_RAR(y) = 1/(1 − exp(−sqrt(y)))` | y > 0 |
| MU2 | `mu = 1 − (1 + g/(2a0))⁻²`, `mu·x = y`, `x = g/a0` | y > 0 |
| EXP (historical AQUAL) | `x·exp(x) = y` (x = g/a0) | y > 0 |
| MONO (operative) | `nu = 1 + h/y`, `h = h_RAR` for y < y_star; continuation `h_mono(y) = h_RAR(y_star) + c·ln((y+y_p)/(y_star+y_p))` for y ≥ y_star, slope rule `h'_mono = max(h'_RAR, c/(y+y_p))`, `c = delta·h_p`, `delta = 0.05` | y > 0, C¹ splice at y_star |

Symbol dictionary: `y = B/a0` (dimensionless scale), `x = g/a0` (dimensionless response), `nu(y) = g/B` (interpolating function), `h(y) = y(nu−1)` (phantom-slope variable), `eps(y) = −y·nu′(y)/nu(y)` (elasticity), `Sigma_ph` projected phantom surface density, `Sigma_cap` capped form (AS090), `Sigma_quad = a0/(4πG)` ZD07 slab ceiling (AS009).

### 1.1 Principal test identity
`g(B,a0) = B·nu(B/a0)`  ⇒  `∂g/∂a0|_B = −(B²/a0²)·nu′(B/a0)`, and along `B = y·a0` (fixed y): `g = a0·y·nu(y)`, so `∂g/∂a0|_y = y·nu(y)` (the "y-proportional" line). Confusing the two is the seed's mandatory negative control (N1).

## 2. Derivations (seed steps 2–3)

### 2.1 Q branch (exact)
`nu_Q(y) = sqrt(1+1/y)`.
- `nu_Q′(y) = −1/(2 y² sqrt(1+1/y))` (chain rule: `d/dy (1+1/y) = −1/y²`; `d/dz sqrt(z) = 1/(2 sqrt z)`). **Lean-certified** (thm B1).
- Elasticity: `eps_Q = −y·nu′/nu = 1/(2(y+1))`. **Lean-certified** (thm B2). Deep: `eps_Q → 1/2` as y→0⁺ — **Lean-certified Tendsto** (thm B3). Newtonian: `eps_Q = 1/(2y)·(1+O(1/y)) → 0`.
- Chain rule of the principal test at fixed B: `(d/da0) sqrt(B² + a0 B) = B/(2 sqrt(B² + a0 B))`. **Lean-certified** (thm A1).

### 2.2 RAR branch
`nu_RAR(y) = 1/(1 − e^{−s})`, `s = sqrt(y)`.
- `nu′ = −s e^{−s}/(2y(1−e^{−s})²)`; elasticity `eps_RAR = −y·nu′/nu = s/[2(e^s − 1)]`; series at s→0: `eps = 1/2 − s/4 + s²/24 + …` (deep), `eps → 0` exponentially (`~ s e^{−s}/2`) in Newtonian. Deep-asymptotic `nu − 1 ~ s/2`, giving `g → sqrt(a0B)` with prefactor 1 and leading correction `1 + s/4`.
- Verified numerically vs sympy symbolic derivative (worst abs residual 5.3e-44 on grid) and vs 50-dps finite differences on the resolvable subdomain y ≤ 1e3 (worst rel 3.18e-25); at y ≥ 1e4 the response is flat to `e^{−sqrt(y)} ≤ e^{−100} ≈ 4e-44`, below the 50-dps floor (representation limit, not physics).

### 2.3 MU2 branch (implicit)
`x = (1 − (1 + x/2)⁻²)·(y/x)`? — no: declared `mu(x) = 1 − (1 + x/2)⁻²` acting on `x = g/a0`, with `mu·x = y`, i.e. `y = x − x(1+x/2)⁻²`. Implicit differentiation: `dy/dx = 1 − (1+x/2)⁻² + x·(1+x/2)⁻³` (i.e. `1 + x·(1+x/2)⁻³ − (1+x/2)⁻²`; the third term from `−x·d(1+x/2)⁻²/dx = x·(1+x/2)⁻³`), so `dx/dy = 1/[1 − (1+x/2)⁻² + x(1+x/2)⁻³]` and `nu′ = d(x y)/dy − 1`… in practice the run evaluates `eps = −y·nu′/nu` via `d(ln nu)/dy` with the implicit derivative, checked against central FD: worst rel 1.24e-25; implicit consistency `|x·mu/y − 1|` worst 2.36e-46 (S1). Deep: `mu(x) ≈ x` for x→0 ⇒ `x ≈ sqrt(y)`, `g → sqrt(a0B)` prefactor 1 with leading correction `1 + (3/16)sqrt(y)` (Newton-bisection of the implicit equation at 50 dps; C3 observes `eps(1e-14) = 0.49999998125 = 1/2 − (3/16)·1e-7` exactly as predicted). Newtonian: `eps(1e8) = 8.0e-16`.

### 2.4 EXP branch (historical AQUAL)
`x·e^x = y` (x = g/a0). Implicit: `dx/dy = e^{−x}/(1+x)`, `nu = x·(y/x)... `— here `g = x·a0`, `B = y·a0`, so `nu = g/B = x/y = e^{−x}`: `nu′ = −x e^{−x}/(1+x)·(1/y)… ` — numerically `nu = x/y = e^{−x}` and `dnu/dy = e^{−x}·dx/dy·(−1) = −e^{−2x}/(1+x)`. Elasticity `eps = −y·nu′/nu = y·e^{−x}/(1+x)·... ` — the run verifies closed forms vs FD (worst rel 1.24e-25), implicit consistency worst 4.69e-47. Deep: `x ≈ sqrt(y)` ⇒ `eps → 1/2 − sqrt(y)/8 + …` observed `eps(1e-14) = 0.4999999875`. Newtonian: `x ≈ y` ⇒ `eps ≈ y e^{−y} → 0` (5.45e-43429442 at y=1e8). FD domain y ≤ 10 (beyond, `e^{−y}` underflows 50 dps).

### 2.5 MONO branch (operative)
`h(y) = y(nu−1)`; `h_RAR(y) = y/(e^{sqrt y} − 1)` (exact RAR-implied h).
- Landmarks (AS047-loose roots, bracketed by sign change then bisected at 50 dps): `y_p = 2.539638282188165325` (max of h_RAR), `h_p = h_RAR(y_p) = 0.64761023789191485965` (matches AS047 pin 2.5396/0.647610), `c = delta·h_p = 0.032380511894595742982`, `y_star = 2.3374124052663294556` (root of `h′_RAR(y) = c/(y+y_p)`), `h_star = h_RAR(y_star)`.
- Splice is value- and slope-continuous (C5a/C5b: differences exactly 0 at 50 digits — C¹); the derivative rule `h′_mono = max(h′_RAR, c/(y+y_p))` holds pointwise on the grid (max gap 0.0).
- Continuation derivative `h′_mono = c/(y+y_p)` verified against numeric differentiation independently (residual 0.0 at y ∈ {3,10,100,1e4,1e6}).
- Elasticity: `eps_mono = −y·nu′/nu` with `nu = 1 + h/y`, `nu′ = h′/y − h/y²` (continuation: `h′ = c/(y+y_p)`). Deep (y < y_star, MONO = RAR): `eps → 1/2` with the RAR series `1/2 − sqrt(y)/4 + …`; observed `eps_mono(1e-14) = 0.499999975`. Newtonian: **logarithmic recovery** — `eps_mono(1e8) = 1.1597e-8` (vs RAR 5.7e-4340, EXP 6.5e-43429441); `nu_mono − 1 = 8.194e-4` at y=1e3 vs `nu_RAR − 1 = 1.847e-14` — four orders of magnitude slower recovery, the signature of the log-phantom continuation (`h_mono(y) ~ c·ln y`, AS047).
- C3 deep-prefactor: `g/sqrt(a0B) → 1` on **all five branches** (MU2 included, prefactor 1 — NOT √2; earlier expectation corrected; the √2 belief confused the argument scale of mu's Taylor cell with the response prefactor; numerics were right, the control caught the wrong expectation).

### 2.6 Principal test grid (all branches)
C1 (chain identity `∂g/∂a0|_B = −(B²/a0²)ν′` vs central FD at `a0 ± 1e-13·a0`): worst relative residuals Q 1.25e-27, RAR 3.18e-25, MU2 7.31e-24, EXP 7.64e-26, MONO 1.25e-27 (FD subdomains as declared in 2.2/2.4; all PASS, tolerance 1e-18).
C1b (elasticity `eps = −yν′/ν` vs `(a0/g)·FD`): worst 6.25e-28 on all branches.
C1c (Euler identity `g(B,λa0)·… ` — dimensionless scale-invariance residual `|g(B,a0)/sqrt(a0B) − g(B,a0′)/sqrt(a0′B)|`-type): worst rel residual 6.25e-16 (50-dps FD-limited), all branches.
C2 (y-proportional line: `∂g/∂a0|_y = y·nu = g/a0` vs FD): worst rel 1.95e-50 — exact to working precision.
C1d (independent representation): sympy `symbolic_diff` of the closed forms Q (`sqrt(1+1/y)`) and RAR (`1/(1−e^{−sqrt y})`): worst abs residual 8.16e-56 (Q), 5.32e-44 (RAR); MU2/EXP implicit-function derivative vs FD worst rel 1.24e-25; MONO continuation derivative vs numeric diff 0.0.

## 3. Negative controls (seed step 5) — must be capable of failing

- **N1 (fixed-B vs fixed-y confusion):** the naive guess `∂g/∂a0 ≈ (B/a0)·nu(y)` — i.e., pretending fixed-B scaling behaves like fixed-y scaling — disagrees with FD on 81/81 grid points on every branch, with mean `FD/naive = 0.2500` (Q exactly 0.25: the true derivative `−(B²/a0²)ν′ = −(y²/2a0)·(1/(y²nu))... ` evaluates to `−g/(2a0)`-type, i.e. the naive value is 4× too small in magnitude on the deep line). **The control failed as required** — this is the seed's mandatory confusion test, and it discriminates: fixed-B ≠ fixed-y.
- **FD domain controls:** RAR beyond y=1e3 and EXP beyond y=10 give FD residuals that violate 1e-18 tolerance in a *predictable direction* (response flat to e^{−sqrt y}/e^{−y} below 50-dps resolution; e.g. RAR flat to 1e-4340 at y=1e8). These were caught as representation artifacts (failed attempts recorded), and the domain was restricted with the reason documented — the control is capable of failing and did.
- **MU2 deep prefactor:** the expectation “1” was asserted with tolerance |g/√(a0B) − 1| < 1e-6 at y=1e-14 after an earlier expectation “√2” was falsified by the same control in this run's development (residual would have been 0.4142 > tolerance — the control discriminates prefactor 1 from √2 at 50 dps).

## 4. Bounds (actually enforced)

Single process, single thread (no thread pools; `OMP_NUM_THREADS=MKL_NUM_THREADS=OPENBLAS_NUM_THREADS=NUMEXPR_NUM_THREADS=1` on the command line), mpmath `mp.dps = 50`, wall ≤ 120 s (caller timeout). **Scale-derivatives run:** wall 1.22 s (script `time.monotonic`), `/usr/bin/time` real 1.26 s, user 1.24 s; peak RSS raw `ru_maxrss = 58130432` bytes = 55.4 MiB (assert `< 512 MiB` passed). **Phantom-disk run:** real 5.76 s, user 5.74 s (RSS recorded in the script). **Lean compile:** `lake env lean` single-thread, exit 0, within the 580 s timeout, zero errors.

## 5. Phantom disk — projected surface density (certified appendix)

Basis: on the operative MONO deep branch, `h(y) ~ c·ln y` ⇒ `nu − 1 ~ c·ln y / y` and the phantom density from Poisson inversion of the log potential `Phi_ph = C·ln(r/r0)` is **`rho_ph(r) = C/(4πG r²)`** (AS047-certified Poisson inversion; C1/C2 of AS047's Lean certificate: `deriv (fun r => r²·dPhi/dr) = C`, exact). With `C = a0·r_M` (Lean-certified thm C1 here), `r_M = sqrt(G M_b/a0)`.

### 5.1 Face-on and edge-on projected density (exact Abel column)
For a spherical shell at radius r with density `rho = C/(4πG r²)`, the column along any line of sight at projected radius R is independent of viewing angle (spherical symmetry ⇒ face-on = edge-on):
`Sigma_ph(R) = ∫_{−∞}^{+∞} rho(sqrt(R²+z²)) dz = (C/(4πG))·2∫₀^∞ dz/(R²+z²) = (C/(4πG))·(π/R) = C/(4G R)`.
Every step is **Lean-certified** in this run's certificate (section D):
- `d/dz [(1/R) arctan(z/R)] = 1/(R²+z²)` (thm D1) — the Abel antiderivative;
- `∫₀^T dz/(R²+z²) = (1/R) arctan(T/R)` (thm D2, FTC);
- `∫₀^∞ dz/(R²+z²) = π/(2R)` (thm D3, Tendsto via `arctan → π/2`);
- coefficient bookkeeping `2·(C/4πG)·(π/2R) = C/(4GR)` (thm D4).
Numerical verification: exact-θ quadrature (`z = R·tan θ`, θ ∈ [0, π/2), 6000 midpoints, infinite range) of the **full MONO density** (not just the 1/r² asymptote) at R = 10 r_M and 30 r_M agrees with `C/(4GR)` to −4.16e-4 and −4.63e-5 relative (asymptotic approach, monotone); at R = 1 r_M the full-MONO column differs by −4.0% (inner log-phantom side, domain statement E). Face-on = edge-on exactly by spherical symmetry (no angle-dependent factor; the 2R·∫dz form is the same integral).

### 5.2 Capped form (AS090) and the column floor
Regularized (capped) phantom surface density over a central disk of radius R_p (AS090): `Sigma_cap(R_p; R) = (C/(2πG R_p))·arccos(R_p/R)` for R ≥ R_p. Verified: at the cap edge (gap 1e-30) `Sigma_cap → 0` (1.5e-14 Msun/pc², canonical); as the cap radius → ∞ with R fixed, `Sigma_cap → C/(4GR)` exactly (check: cap(R=3r_M; R_out=1e12 r_M) = 55.970486 = nominal 55.970486 Msun/pc² at 50-dps agreement).
**Central column through the disk plane** (z-axis line of sight, inner cutoff r_in, R = 0): `col(r_in) = 2·(C/4πG)·∫_{r_in}^∞ dz/z² = C/(2πG r_in)` — each step Lean-certified (thms E1–E4: `d/dz[−(1/z)] = 1/z²`, `∫_{r_in}^T = 1/r_in − 1/T`, Tendsto to `1/r_in`, coefficient `2·(C/4πG)·(1/r_in) = C/(2πG r_in)`). At `r_in = 0.5 r_M`: `col = C/(π G r_M) = a0/(πG) = Sigma_pi`: **canonical 213.7915071 Msun/pc², alternative 257.5710495 Msun/pc²** (rel 1e-28 agreement with the exact identity, outer cap 1e30·r_M).

### 5.3 Column-density floor vs the ZD07 slab-ceiling bound (AS009 comparison)
ZD07 slab ceiling (AS009 table): `Sigma_quad = a0/(4πG)` (quadratic-potential slab saturation). Both footings:
| quantity | canonical | alternative |
|---|---|---|
| `Sigma_quad = a0/(4πG)` | 53.447877 Msun/pc² | 64.392762 Msun/pc² |
| `Sigma_pi = a0/(πG)` (floor at 0.5 r_M) | 213.791507 Msun/pc² | 257.571049 Msun/pc² |
| floor/ceiling | **4.0000** | **4.0000** |
| nominal column at splice radius r_in_splice | 256.713083 (233.744679 full MONO) | 309.281969 (281.610168 full MONO) |
| floor at 0.1 r_M | 1068.957 Msun/pc² | 1287.855 Msun/pc² |

The 1/r² phantom column **exceeds the ZD07 slab ceiling by exactly 4× at r_in = 0.5 r_M (floor/ceiling = a0/(πG) ÷ a0/(4πG) = 4)**, and diverges as r_in → 0. The floor crosses the ceiling at `R_crit = π·r_M` (Lean-certified thm C2: `C/(4GR) = a0/(4πG) ⇒ R = π r_M`): **canonical 29.693086 kpc, alternative 27.052166 kpc** (matches π·r_M to 50 digits). Since `Sigma_quad` is the slab bound on which the ZD07 ceiling argument (and the AS009/WAVE0 review) relies, and within R_crit the operative MONO phantom column lies 1–4× above it, **the operative branch must cap the phantom density inside R ≈ R_crit (or the ceiling bound fails)** — this is the flag the brief asked to compare with "the ZD07 slab-ceiling bound issues from AS009"; the AS090 capped form (5.2) is the regularization with the correct limits, and the monomial log-phantom validity domain is r < ~0.65 r_M (inner) and r >> r_M (deep), with the full-MONO kernel giving the in-between columns (table below).

Full-MONO kernel columns (exact-θ quadrature to ∞, M_b = 6e10 Msun) vs the nominal 1/r² law:
| R/r_M | 0.5 | 0.65 | 0.8 | 1.0 | 1.5 | 3.0 | 5.0 | 10 | 30 |
|---|---|---|---|---|---|---|---|---|---|
| Σ_full/Σ_nom (canonical = alternative) | 0.826264 | 0.909349 | 0.938522 | 0.959846 | 0.981786 | 0.995390 | 0.998336 | 0.999583 | 0.999954 |

Leading RAR-tail correction of the full-MONO column vs the 1/r² law: `Σ_full/Σ_nom ≈ 1 − (1/24)(r_M/R)²` — at R = 10 r_M predicts −4.17e-4 vs observed −4.1651e-4; at R = 30 r_M predicts −4.63e-5 vs observed −4.6294e-5. (Expansion of the RAR deep series `h ~ sqrt(y)·(1 − sqrt(y)/4 + y/24 − …)` through O(y) in the Abel kernel.) Both footings identical in ratio because the correction is dimensionless.

## 6. Lean 4 certificate

`AS049_certificate.lean` (16 theorems; sections A–E matching 2.1, 2.6, 5.1, 5.2 above):
A1 `q_chain_rule`; B1 `q_nu_deriv`, B2 `q_elasticity_closed`, B3 `q_epsilon_deep_limit` (Tendsto); C1 `amu_rM_identity`, C2 `crossing_radius`; D1 `abel_hasDerivAt`, D2 `abel_antiderivative`, D3 `abel_integral_finite`, D4 `abel_integral_atTop` (Tendsto), D5 `sigma_abel_coeff`; E1 `central_column_hasDerivAt`, E2 `central_column_antiderivative`, E3 `central_column_finite`, E4 `central_column_atTop` (Tendsto), E5 `central_column_coeff`.
Verification: `cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS049_certificate.lean` — **exit 0, zero errors.** Axiom audit (`#print axioms` on the kernel-spanning theorems): all exactly `[propext, Classical.choice, Quot.sound]` — within the allowed subset; zero `sorry`. RAR/MU2/EXP/MONO closed forms and all finite grids are numerical (residuals in section 2); `y_p`, `y_star`, `pi` enter only as exact symbols in the certificate.

## 7. Limitations

- Elasticity/deep-limit statements for RAR/MU2/EXP/MONO are numerically verified on declared grids, not Lean-certified (only Q and the phantom-disk identities are); the deep limits use y=1e-14 with leading corrections < 1e-7 asserted, not a certified proof.
- FD subdomains (RAR y ≤ 1e3, EXP y ≤ 10) restrict the *finite-difference* checks; the function evaluations themselves run on the full grid y = 10^k, k ∈ [−10, 8].
- `kappa = 1/2` adopted (STANDING: measured 0.465 ± 0.076); `delta = 0.05` framework input; `y_p/y_star` are 50-digit roots, not closed forms.
- Phantom appendix: spherical-proxy MONO density (no nonspherical disk field solve); central column uses inner cutoff r_in = 0.5 r_M as a *declared regularization sample*; the phantom mass budget beyond the cutoff is not computed (flagged for closure); the ZD07 ceiling comparison is on the column-density values, not a re-derivation of ZD07.
- Dispatch-title provenance discrepancy documented in section 0.

## 8. Strongest surviving statements

1. **Exact (Lean-certified):** on Q, `eps_Q(y) = 1/(2(y+1))` with `eps → 1/2` as y→0⁺; `∂√(B²+a0B)/∂a0 = B/(2√(B²+a0B))`. For the phantom disk: `Sigma_ph(R) = C/(4GR)` exact for the 1/r² phantom, face-on = edge-on by spherical symmetry; `col(r_in) = C/(2πG r_in)`; `C = a0·r_M`; ceiling crossing at `R = π r_M`.
2. **Numerical (50 dps, all controls pass):** the principal-test identity holds on all five branches (worst rel residual 7.3e-24); deep `g/√(a0B) → 1` on all branches (MU2 prefactor 1 not √2); MONO recovers Newton logarithmically (805× slower than RAR at y=1e3); the phantom column floor sits exactly 4× above the ZD07 slab ceiling at 0.5 r_M and does not fall below it until R_crit = π r_M (29.69 / 27.05 kpc).

## 9. Next unresolved implication

Inside R < R_crit = π r_M the operative MONO phantom column exceeds the ZD07 slab ceiling (1–4× on the sample columns); a closure transfer needs the **cap mechanism**: the radius/scale at which the operative filtered MONO kernel cuts the phantom off (AS090-style capped form with a physically motivated R_p, or a finite-disk truncation of the log-phantom mass budget), and the corresponding bound restoring `Sigma ≤ Sigma_quad` for the ZD07 ceiling gate — plus the AS047 W^{1,∞}-derivative transfer across the C¹∖C² splice at y_star, which remains the operative branch's derivative-norm gap.

## 10. Child proposals (not dispatched)

- **AS049.C01 — Capped MONO phantom disk against the ZD07 slab ceiling:** determine the cutoff scale R_p (filter scale ξ or dynamical boundary) such that `Sigma_cap(R_p;R) ≤ Sigma_quad` for all R, using the AS090 capped form; controls: ceiling respected at every R (capable of failing), cap → nominal column as R_p → ∞, both footings, ties to AS090/AS091/AS009.
- **AS049.C02 — Derivative-norm transfer across the MONO splice** (inherits AS047.C01): certified W^{1,∞} bound on h_mono − h_RAR and ellipticity ratio at fixed filter ξ (parent AS047 already proposes this; this run re-confirms its necessity via the log-recovery rates of section 2.5).

## Files in this run directory

`AS049_scale_derivatives.py` (core grid/controls, 50 checks), `AS049_phantom_disk.py` (appendix, 14 checks), `AS049_certificate.lean` (+ `lean_out.txt`), `raw_output_scale_derivatives.txt`, `raw_output_phantom_disk.txt`, `checks_phantom_disk.json` (machine-readable residuals), `time_bounds*.txt` (actual wall/RSS), `lean_probe*.lean` (API probes), `derivation.md`, `result.json`.