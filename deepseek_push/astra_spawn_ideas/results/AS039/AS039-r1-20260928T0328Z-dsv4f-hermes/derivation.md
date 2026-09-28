# AS039 — Deep homogeneity of the static energy: derivation

**Run:** `AS039-r1-20260928T0328Z-dsv4f-hermes` · worker `sa-0-94583ba2` (Hermes
subagent, deepseek-v4-flash-0731) · task SHA-256
`57e18fb2f5b554ba665f3ef204971c91cd6fe30976508c4389dcd4b200cf6220`

All source hashes (README.md, FRIED_CHICKEN_SPEC.md, peer_review README,
STANDING.md) verified against `SOURCE_MANIFEST.json` before computing. The
reserved claim `claims/AS039.json` (owner hermes-orchestrator, state running)
was read, not modified.

---------------------------------------------------------------------------
## 0. Statement of the object of study

**Convention (AS038-adjacent AQUAL primitive, fixed by the task family):**

```
X  := |grad Phi|^2 / a0^2        (dimensionless strain variable)
mu : R_{>=0} -> R_{>=0}          constitutive response, mu(x) = (-1)-inverse factor,
                                 spherical field equation   mu(g/a0) * g = B
F(X)  := int_0^X mu(sqrt(t)) dt  static energy primitive (dimensionless)
```

Spherical variables: `y = B/a0 > 0` (baryonic Newtonian acceleration), `x = g/a0`
(total acceleration), both `> 0` deep; `B = G_N M_b/r^2`, `g = |grad Phi|`.

The five branches (FRAMEWORK_CONTRACT branch dictionary — used only their
declared domain; no branch is silently identified with another):

| label | mu(x) | x(y) | F(X) |
|---|---|---|---|
| Q | `(sqrt(1+4x^2)-1)/(2x)` | `sqrt(y^2+y)` | closed form `(s/2)sqrt(1+4X) + (1/4)asinh(2s) - s`, `s=sqrt(X)` |
| EXP (historical) | `1-e^{-x}` | solves `x(1-e^{-x})=y` | exact `X - 2 + 2(1+s)e^{-s}` |
| MU2 | `1-(1+x/2)^{-2}` | solves `x mu(x)=y` | quadrature |
| RAR | `1-e^{-sqrt(y(x))}`, x = y/(1-e^{-sqrt(y)}) | `y/(1-e^{-sqrt(y)})` | u-parametrized quadrature |
| MONO (operative) | = RAR on `y < y*` (splice at `y* ~ 2.3374`) | = RAR | = RAR deep |

**MONO note (not an assumption, a definitional fact):** the operative filtered
MONO continuation coincides with RAR on the entire RAR segment `y <= y* ~
2.3374` by construction (h' = max(h'_RAR, ...) acts only for `y > y*`). The deep
regime `y << 1` lies strictly inside the RAR segment, so **every deep-domain
statement below transfers from RAR to MONO verbatim**; the heat filter S does
not act in the spherical point-source net (it is a smoothing of the source
argument of nu_mono, and deep point-source statements below are statements
about the response function, not about filtered configurations — flagged in
Limitations).

**Task principal test:** `mu(x) ~ x  (x -> 0)  implies  F(X) ~ (2/3) X^(3/2)`.

---------------------------------------------------------------------------
## 1. Precise claim, symbol dictionary, assumptions

**Claim (supported, scoped):**
For each branch in {Q, EXP, MU2, RAR} and for MONO on its RAR segment
`y in (0, y*)`:

1. **Asymptotic homogeneity degree 3/2 in X (degree 3 in |grad Phi|):**
   `lim_{X->0+} F(lam^2 X)/F(X) = lam^3` for every `lam >= 0` (equivalently
   `alpha(X) := X F'(X)/F(X) -> 3/2`). For the **pure deep primitive**
   `F0(X) = (2/3) X sqrt(X)` the identity `F0(lam^2 X) = lam^3 F0(X)` holds
   **exactly for all X >= 0** (Lean-certified).
2. **Uniform leading correction with branch-specific order:** on `X -> 0+`,
   `F(X) = (2/3) X^(3/2) [1 + c_b X^(q_b) + O(X^(q_b+1/2 or 1))]` with
   `q_Q = 1, c_Q = -3/5` and `q = 1/2` for EXP (`c=-3/8`), MU2 (`c=-9/16`),
   RAR (`c=-3/4`, MONO same). The exact leading neglected terms are listed in
   §3. **Domain of the claim:** `X in (0, X_c)` with asymptotic meaning
   `X -> 0`; numerically verified on `X in [1e-20, 1e-6]` (see §4); the series
   converge for `X < 1/4` (Q), `X < 4` (MU2), all `X > 0` (EXP exact form,
   RAR/MONO all `y < y*`).
3. **Second-variation structure at zero field:** `mu(0) = F'(0) = 0` for all
   five branches — the quadratic (linear-response) energy term **vanishes
   identically**; `F''(X) = mu'(sqrt(X))/(2 sqrt(X)) ~ (1/2) X^{-1/2} -> +inf`
   — the Hessian is not a bounded quadratic form at zero field; the leading
   surviving term is the **cubic** `|grad Phi|^3` energy
   `eps_phi = g^3/(12 pi G_N a0)` (degree 3 in the field; C^1, not C^2, at
   zero field). This is the energy-side twin of the XC2 review statement that
   the leading deep-MOND flux is homogeneous of degree 1/2 (flux response
   ~ sqrt(eps-perturbation)).
4. **Energy content of the homogeneous law:** the static field energy of a
   point source in the deep regime is
   `E_field(R) = (1/3) M_b C ln(R/r_in) + O(M_b C)`, per e-fold (per ln r)
   `dE/d ln r = (1/3) M_b C = (2/3) * (1/2) M_b v_flat^2` — the factor 2/3 is
   **exact** for the pure deep law; totals diverge logarithmically.
5. **Phantom interpretation consequence:** the phantom bookkeeping density
   `rho_ph = C/(4 pi G_N r^2)`, `M_ph(R) = C R/G_N` gives a phantom-gas energy
   `E_ph(R) = C^2 R/(4 G_N) = (1/4) M_b a0 R` (with the *conditional* inputs
   sigma^2 = C/2, P = sigma^2 rho_ph), which diverges **linearly**, while the
   field energy diverges **logarithmically**. `E_ph/E_field ~
   (3/4)(R/r_M)/ln(R/r_M) -> inf`. The phantom is a flux-divergence
   bookkeeping object; its thermodynamic energy is **not** the static field
   energy, and no field-gas identification follows from the shared deep law
   without a new bridge.

**Assumptions (inputs), all from the framework contract:**
`a0 = kappa c sqrt(G_N rho_Lambda)` as **adopted input**, `kappa = 1/2`
(adopted, not derived here); `r_M = sqrt(G_N M_b/a0)`; `C = sqrt(G_N M_b a0) =
v_flat^2`; `v_flat^4 = G_N M_b a0`; `G_N = 6.67430e-11 SI` (G_bare and G_cosmo
kept separate symbols, not used); spherical symmetry + static + point-source
for the force/energy integrals (energy integrals assume r >= r_M so X <= 1;
the crossover region r < r_M contributes a bounded O(M_b C) constant, tracked
numerically in §4.5).

**Conclusions established (not inputs):** asymptotic homogeneity degree 3/2,
branch-specific correction exponent/coefficient, second-variation divergence
class, log-vs-linear divergence classes of E_field vs E_ph, the 2/3 virial
coefficient.

---------------------------------------------------------------------------
## 2. Scaling under grad Phi -> lam grad Phi; second variation near zero field

**Scaling.** Let `Phi' = lam Phi`. Then `X' = lam^2 X`. For the pure deep law
`F0(X') = (2/3)(lam^2 X) sqrt(lam^2 X) = lam^3 F0(X)` (algebra, Lean-certified:
`deep_energy_homogeneity_degree_three`, all `lam >= 0`, `X >= 0`). Hence the
energy functional `E[Phi] = (a0^2/8 pi G_N) int F(|grad Phi|^2/a0^2) d^3x`
satisfies `E[lam Phi] = lam^3 E[Phi]` in the deep regime — homogeneous of
**degree 3** in the field amplitude (degree 3/2 in X).

The field equation is covariant in the deep regime only together with a source
rescale: with `mu(s) = s`, `div[(|grad Phi|/a0) grad Phi] = 4 pi G_N rho`
becomes, under `Phi -> lam Phi`, `lam^2 div[(|grad Phi|/a0) grad Phi] =
4 pi G_N rho`, i.e. the rescaled field solves the equation for source
`rho' = lam^2 rho`. Consistent with `E ~ M^{3/2} sqrt(G_N a0)`: mass scales as
`lam^2`, energy as `lam^3`. For a point source the deep branch solution is
`g = C/r` (from `g^2 = a0 B`, `B = G_N M_b/r^2`), i.e. `Phi = C ln r +
const`, and the deep law is not a plain symmetry of the source-free problem.

**Second variation near zero field (what vanishes, what remains
nonsmooth).** Let `Phi = eta psi`, `eta -> 0`. With `X = eta^2 |grad psi|^2/
a0^2`:

- `F(X) = (2/3) X^(3/2) + ...` is `O(eta^3)`, so the **quadratic variation
  vanishes identically**: `F'(0) = mu(0) = 0` on all five branches
  (numerically: F(0) = 0 and F'(0+) = 0 checked in the residual audit).
- The leading term is the cubic `(1/12 pi G_N a0) int |grad psi|^3 d^3x`:
  homogeneous degree 3, `C^1` in the field but **not C^2** — `F''(X) =
  (1/2) X^{-1/2} mu'(sqrt(X))` with `mu'(0+) = 1` on every branch, so
  `F''(X) = (1/2) X^{-1/2} (1 + O(sqrt X or X)) -> +inf` as `X -> 0`.
  Numerically `2 sqrt(X) F''(X) -> 1` at `X = 1e-12` to 6 digits on all four
  computed branches (Table 3).
- Consequence for the linearized theory: the linearized operator about zero
  field `div[mu(0) grad delta Phi]` is identically zero — there is **no
  quadratic/L2 energy and no linear restoring term** in any channel at zero
  field; deep perturbations respond as `O(eta^{1/2})` in the flux (the XC2
  review's sqrt-eps response), and the zero-field limit is degenerate
  (spec requirement 9 territory: controlled y -> 0 treatment).

**What vanishes / what remains nonsmooth (one-line):** the quadratic term of
the static energy vanishes (mu(0) = 0); the cubic `|grad Phi|^3` term remains,
and the second derivative `F''` is singular as `X^{-1/2}` — the functional is
C^1 but not C^2 at zero field, with divergent Hessian coefficient.

---------------------------------------------------------------------------
## 3. Intermediate algebra: series, leading neglected terms, signs, units

**Dictionaries and expansions (all `x -> 0`, then `F` via
`F(X) = 2 int_0^{sqrt X} s mu(s) ds`).**

Q: `mu_Q(x) = (sqrt(1+4x^2) - 1)/(2x) = x - x^3 + 2 x^5 - 5 x^7 + O(x^9)`,
radius of convergence `|x| < 1/2` (branch point at `x = i/2`). Hence
`F_Q(X) = (2/3) X^(3/2) - (2/5) X^(5/2) + (4/7) X^(7/2) - ...`
`= (2/3) X^(3/2) [1 - (3/5) X + (6/7) X^2 - ...]`.
**Leading neglected term: `-(2/5) X^(5/2)`, relative `-(3/5) X`, domain
`|X| < 1/4`.** The Q primitive is odd-power only — no X^2 term: the algebraic
a0-line is the unique quadratic field equation among the five, and this shows
up as the correction order O(X) (vs O(sqrt X) for the exponential family).

EXP (historical, exact closed form):
`F_EXP(X) = X - 2 + 2(1 + sqrt X) e^{-sqrt X}`
(exact: `F_EXP'(X) = 1 - e^{-sqrt X} = mu_EXP(sqrt X)`, verified analytically
and numerically).
`F_EXP(X) = (2/3) X^(3/2) [1 - (3/8) X^(1/2) + (1/5) X - (5/48) X^(3/2) +
O(X^2)]` · leading neglected term relative `-(3/8) sqrt X`; domain all
`X > 0` (exact form) — the series itself converges everywhere.

MU2: `mu_MU2(x) = x - (3/4) x^2 + (1/2) x^3 - (5/16) x^4 + O(x^5)`,
`F_MU2(X) = (2/3) X^(3/2) - (3/8) X^2 + (1/5) X^(5/2) - ...`
`= (2/3) X^(3/2) [1 - (9/16) X^(1/2) + (3/10) X + ...]`.
Leading neglected term relative `-(9/16) sqrt X`; convergence `|x| < 2`,
i.e. `|X| < 4`.

RAR (and MONO on `y < y*`): parametrize by `u = sqrt y`, `x(u) = u^2/(1-e^{-u})`,
`mu(u) = 1 - e^{-u}`; inverse expansion `mu(x) = x - x^2 + (1/2) x^3 - O(x^4)`
(invert `x = y/(1-e^{-sqrt y})`). Then
`F_RAR(X) = (2/3) X^(3/2) - (1/2) X^2 + (1/5) X^(5/2) - O(X^3)`
`= (2/3) X^(3/2) [1 - (3/4) X^(1/2) + (3/10) X + ...]`.
Leading neglected term relative `-(3/4) sqrt X`; valid for `y < y*` on MONO,
all `y > 0` on RAR.

**Signs:** all corrections negative (each branch approaches the homogeneous
law from below); `F(0) = 0`, `F` strictly increasing (`F(X+h) - F(X) > 0`,
Table 5), `F(1)` differs across branches (Q 0.4789, EXP 0.4715, MU2 0.4229,
RAR 0.3920) — **matching one asymptote (the shared deep slope 1 of mu, and
the shared Newtonian mu -> 1) does not make the finite laws equivalent**, and
at the crossover X ~ 1 the primitives differ by up to 18% (RAR vs Q).

**Units:** X, mu, F dimensionless; `eps_phi = (a0^2/8 pi G_N) F` [J/m^3];
`E_field = int eps d^3x` [J]; `rho_ph = C/(4 pi G_N r^2)` [kg/m^3];
`C = sqrt(G_N M_b a0)` [m^2/s^2] = v_flat^2; `M_b C` [J]; every dimensional
number below carried on both footings separately.

---------------------------------------------------------------------------
## 4. Independent checks (different representation, actual residuals)

All numerics: mpmath dps=50, single thread, fixed grids (y-grid
`10^k, k = -10..8 step 0.1`, 181 points; log-X grid `10^m, m = -20..8 step
0.2`, 141 points), in-script wall budget 120 s — elapsed 4.77 s, peak RSS
26.7 MB (measured by /usr/bin/time -l). Script `compute_as039.py`; raw data
`raw_output.json`.

**4.1 F'(X) = mu(sqrt X) — central-difference audit.** For each branch,
relative residual `| (F(Xe^h)-F(Xe^{-h}))/(2hX) / mu(sqrt X) - 1 |` with
h = 1e-3, maximized over the log-X grid: **max 3.75e-7** for all four
branches (dominated by the O(h^2) scheme truncation, ~ (h^2/6) x ~2.25; this
is the actual recorded residual, not a boolean).

**4.2 Homogeneity audit.** `alpha(X) = X mu(sqrt X)/F(X) -> 3/2`:

| branch | alpha(1e-12) | alpha(1e-6) |
|---|---|---|
| Q | 1.4999999999994 | 1.4999994000 |
| EXP | 1.4999998125 | 1.4998125297 |
| MU2 | 1.4999997188 | 1.4997188917 |
| RAR | 1.4999996250 | 1.4996253683 |

Deviation scales exactly as the predicted corrections (Q: O(X); others O(sqrt X)).
Scaling law `F(4X)/(8F(X)) - 1` at X = 1e-12: Q **-1.800e-12** (predicted
`-(3/5)(4X-X) = -1.8 X` ✓); EXP **-3.7500e-7** (predicted `-(3/8) sqrt X` =
-3.75e-7 ✓); MU2 **-5.6250e-7** (predicted `-(9/16) sqrt X` ✓); RAR
**-7.5000e-7** (predicted `-(3/4) sqrt X` ✓). At X = 1e-16 and 1e-20 all four
track the same predicted power law to 5+ digits.

**4.3 Correction-exponent fit** (least squares on ln|delta| vs ln X over
X in [1e-16, 1e-6], 51 points each):

| branch | beta_fit | beta_pred | c_fit | c_pred |
|---|---|---|---|---|
| Q | 1.000000 | 1 | -0.6000 | -3/5 |
| EXP | 0.499995 | 1/2 | -0.3750 | -3/8 |
| MU2 | 0.499989 | 1/2 | -0.5624 | -9/16 |
| RAR | 0.499983 | 1/2 | -0.7496 | -3/4 |

(max fit residual in ln: 1.2e-6 Q, 5.8e-4 RAR — the RAR residual reflects the
next-order term contaminating the window.)

**4.4 Second-variation diagnostic** `2 sqrt(X) F''(X) -> 1` (with
`F''(X) = mu'(sqrt X)/(2 sqrt X)`):

| branch | at X = 1e-8 | at X = 1e-12 |
|---|---|---|
| Q | 0.99999997 | 0.999999999997 |
| EXP | 0.99990001 | 0.999999 |
| MU2 | 0.99985001 | 0.9999985 |
| RAR | 0.99980003 | 0.999998 |

**4.5 Enclosed field energy vs the deep-law integral** (branch Q primitive,
`solve g^2 = B^2 + a0 B`, exact integration from r_M to R; fiducial
M = 1e11 M_sun): E_Q(R) / [(M C/3) ln(R/r_M)] - 1 = **-0.0840 (R=10 r_M),
-0.0426 (100), -0.0213 (1e4), -0.0142 (1e6)** — converging to 0 as ln R
grows; the offset is the bounded UV/crossover correction (excluded region
r < r_M contributes O(M C), not O(M C ln R)). Deep per-e-fold coefficient
(M C/3) vs (1/2) M v_flat^2: ratio = 2/3 to 12 digits (all branches).
Independent verification that the log law is the correct leading behavior of
the *actual* branch primitives, not only of F0.

**4.6 Support points (both footings; M = 1e11 M_sun unless noted).**

| quantity | canonical a0 = 9.3619e-11 m/s^2 | alternative a0 = 1.1279e-10 |
|---|---|---|
| rho_Lambda [kg/m^3] | 5.8444e-27 | 8.4831e-27 |
| epsilon_Lambda [J/m^3] | 5.2527e-10 | 7.6242e-10 |
| kappa effective at fixed rho | 0.5 (input) | 0.6024 (kappa_eff = 0.5 a0_alt/a0_can) |
| r_M(1e11 M_sun) [pc] | 12202 | 11117 |
| C = v_flat^2 [m^2/s^2] | 3.5249e10 | 3.8690e10 |
| v_flat [km/s] | 187.7 | 196.7 |
| M C [J] | 7.0091e51 | 7.6934e51 |
| eps_phi(r_M) [J/m^3] | 3.4833e-12 | 5.0560e-12 |
| per-log-decade E_field [J] | 5.3797e51 | 5.9049e51 = (2/3)(1/2) M v^2 ln 10, branch-checked |
| M_ph(10^6 r_M) [kg] | 1.9885e47 | 1.9885e47 (= 10^6 M_b exactly, both footings) |
| E_ph/E_field at 10,1e2,1e4,1e6 r_M | 3.26, 16.29, 814.3, 54286.8 | same ratios (scale-free) |

(r_M(M_sun) = 0.0386 pc = 7960 AU, v_flat(M_sun) = 334 m/s — standard MOND
check values reproduced.)

---------------------------------------------------------------------------
## 5. Negative controls (capable of failing — both failed as required)

**NC-1 — replace X^(3/2) with X.** Take `F_1(X) = X` (homogeneity degree 1):
then `mu_1(sqrt X) = F_1'(X) = 1`, the field equation becomes `g = B` — the
deep force is **Newtonian**, exactly: on every grid point and every branch
`x = y` to machine precision (max residual 0.0 at angular precision), and the
deep-law discriminator `x^2/y` (the BTFR indicator) equals `y = 1e-10` at
y_min instead of 1 — the control **fails loudly**, proving the degree-3/2
statement is the one that carries the deep MOND force, and that the control
can discriminate. (Contrast: with the true deep law x^2/y -> 1 as verified in
NC-2.)

**NC-2 — deep and Newtonian limits.** Deep: max |x/sqrt(y) - 1| over
y <= 1e-8: Q 5.0e-9 (O(y) correction, predicted 5e-9 ✓), EXP 2.50e-5,
MU2 3.75e-5, RAR 5.00e-5 (O(sqrt y) corrections with the exact predicted
coefficients c/2: 2.5e-5, 3.75e-5, 5.0e-5 ✓). Newtonian: max |x/y - 1| over
y >= 1e4: Q 5.000e-5 (= 1/(2y) ✓), MU2 4.0e-8 (= 4/y^2 ✓), RAR 3.72e-44
(= e^{-100} ✓), EXP ~ e^{-10000} (below dps-50 resolution, recorded 0.0).
Normalization/boundary: F(0) = 0 exact for Q and EXP closed forms (and
quadratures at X=0), F strictly increasing at X = 1 (positive increments for
all branches, Table 5), F(1) branch-spread 0.392-0.479 quoted above.

**All numbers are actual computed values; no boolean was substituted for a
residual anywhere.**

---------------------------------------------------------------------------
## 6. Strongest surviving statement and first unresolved implication

**Strongest statement (scoped, evidence-backed):**
In the deep regime `g << a0` (X -> 0+), the static energy primitive of every
declared branch (Q, RAR, MU2, EXP, and MONO on its RAR segment `y < y*`) is
asymptotically homogeneous of exact degree **3/2 in X = |grad Phi|^2/a0^2**
(= degree 3 in the field, i.e. `E[lam Phi] = lam^3 E[Phi]`
— exact for the pure deep law F0, Lean-certified), with branch-ordered
approach: `F(X) = (2/3) X^(3/2)[1 + c_b X^{q_b} + ...]`, `q = 1` for Q
(c = -3/5) and `q = 1/2` for EXP/RAR/MU2/MONO (c = -3/8, -3/4, -9/16). The
quadratic energy term vanishes identically at zero field (mu(0) = 0 on all
five branches) and the Hessian diverges as `(1/2) X^{-1/2}` — the deep
functional is C^1, not C^2, at zero field, and the deep sector has no
linearized (quadratic) energy. Energy content: `E_field(R) = (1/3) M_b C
ln(R/r_in) + O(M_b C)`, per e-fold `= (2/3) * (1/2) M_b v_flat^2` (exact 2/3
coefficient), log-divergent for an isolated point source, while the phantom
bookkeeping gas (conditional inputs sigma^2 = C/2, P = sigma^2 rho_ph) has
energy `C^2 R/(4 G_N)` — **linear** divergence; the two energies are different
objects and the phantom-gas identification transfers only via a new derivation.

**First unresolved implication (gate transfer):** the divergence-class split
(log vs linear) means the finite-domain truncation of a real system (halo
edge, virial radius, the L342-style bound-region switch) is **not a removable
cutoff for the energy balance**: the virial/surface terms of the deep field
(AS083-AS088 family) must be re-derived with the actual branch primitive
under the operative filtered MONO field equation (with the heat filter's
measure), not with F0, before any "M C ln R" energy budget can be promoted to
a galaxy-scale statement. Also open: the positivity/ensemble question whether
the negative-definite deep-pressure sector (2X F' - F < 0 at deep X) is
healthy in the relativistic embedding — that is a separate action-level gate.

---------------------------------------------------------------------------
## 7. Phantom-interpretation meaning (summary table)

| observable | deep behavior | divergence class as R -> inf |
|---|---|---|
| field energy density eps_phi = g^3/(12 pi G_N a0) = M C/(12 pi r^3) | 1/r^3 | — |
| E_field(R) | (M C/3) ln(R/r_in) | **logarithmic** |
| rho_ph = C/(4 pi G_N r^2) | 1/r^2 | — |
| M_ph(R) = C R/G_N | R | **linear** |
| E_ph(R) = (1/4) M a0 R (conditional sigma^2 = C/2) | R | **linear** |
| E_ph/E_field | (3/4)(R/r_M)/ln(R/r_M) | -> inf (measured 3.26 ... 5.4e4) |

Interpretation: the phantom mass-density is the exact flux-divergence
bookkeeping of the deep force (rho_ph = div(g - g_N)/(4 pi G_N) on the deep
branch, no new species — ontology guardrail: no dark-matter particle), but
**the phantom gas is not the energy carrier of the static field**: energy
identifications would need an additional (unproved) constitutive/thermo
bridge, and the log-divergent field energy itself requires a boundary
prescription (inside r_in and at halo edge) that the deep homogeneity
statement does not supply.

---------------------------------------------------------------------------
## 8. Closure implication, gate map, children

**Closure implication:** supports spec requirement 1's deep-law content
(`g^2 = a0 g_N => v^4 = G a0 M_b`), requirement 9's zero-field limit
(mu(0) = 0, degenerate linearization, no quadratic energy), and requirement
12's branch fidelity (RAR segment deep behavior preserved by MONO; Q/EXP/...
not transferable to the operative branch). It does **not** touch gates 2-8,
10-11, 13 (kappa remains adopted input).

**Child proposals (spec-written for the orchestrator; not dispatched):**
1. **AS039.C01** — finite-domain energy balance: derive E_field(R_edge) for
   the operative filtered-MONO equation with the heat-filter measure and a
   finite source profile (exp-disc), quantifying the boundary/virial terms
   that the log law omits; control: R_edge -> inf recovers (1/3) M C ln R
   with bounded remainder; discriminates the sigma^2 = C/2 -based phantom
   energy identity.
2. **AS039.C02** — deep perturbation response: quantify the O(sqrt(eps)) flux
   response (peer-review XC2 statement) as a first-variation statement of the
   actual branches, with the second-variation Hessian bounded on the
   Newtonian side X >= X_c; control: linear kernel -> eps response.
Duplicate check: closest live tasks AS038 (primitive recovery, sibling in
flight at execution time), AS037 (Hessians), AS041 (nonspherical algebraicity)
— none covers the homogeneity degree/divergence-class statement; catalog
search (AS626 dilation, AS653 flux power) contains no landed result at
execution time.

**Limitations:** (i) point-source spherical statements; nonspherical source
configurations and the filtered (heat) MONO equation are not treated (the
deep response-function statements transfer to MONO only on its RAR segment
domain; the filter's action is outside this audit); (ii) energy integrals cut
at r = r_M from below — the crossover/UV region contributes a bounded but
branch-dependent constant (recorded -8.4%..-1.4% offsets); (iii) asymptotic
claims are limit statements — numeric support is finite evidence on
X in [1e-20, 1e-6] with the exact analytic corrections fitted, not a proof of
the limit (the limit itself is the elementary calculus of the listed series);
(iv) F'' divergence is analytic (mu'(0) = 1 per branch) and numerically
confirmed; no Lean certificate of the derivative exists because this build
lacks Real.hasDerivAt_sqrt (derivative content is carried by the certified
algebra + lane numerics); (v) all dimensional examples carry both footings
separately; the alternative footing keeps kappa = 1/2 and its own
rho_Lambda (kappa_eff = 0.6024 at the canonical vacuum, reported, not
combined).
