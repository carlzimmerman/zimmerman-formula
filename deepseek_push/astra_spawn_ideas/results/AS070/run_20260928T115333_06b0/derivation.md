# AS070 — Coupling a proposed normalization constraint consistently

**Run:** `run_20260928T115333_06b0` · **Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter), Hermes Agent subagent, single-run seed worker
**Branch:** CORE coefficient; conditional MU_n statistical response (no branch translation performed)
**Task SHA-256:** `f298c932b31ecbfd3c14320a45d71be82fd36ce4048fb9f8fef9baee585c5694` (verified at start, matches dispatch)
**Inputs verified:** PD01 `37e39d1a…c74d`, PD08 `83f6054c…fcfb`, k01 `8df5a3ab…b25c` — all match pinned hashes (SOURCE_MANIFEST).

---

## 1. Precise claim, symbol dictionary, assumptions (seed step 1)

### 1.1 The named candidate

> Candidate constraint `F = 4*a0^2 - G*c^2*rho_L = 0` enforced with multiplier `eta` in an action.

### 1.2 Symbol dictionary

| Symbol | Meaning | Status |
|---|---|---|
| `a0` | galactic acceleration scale | framework scale `a0 = kappa*c*sqrt(G*rho_Lambda)`, `kappa = 1/2` **adopted input** (never derived below) |
| `kappa` | dimensionless coefficient | adopted `= 1/2`; candidates `kappa = a0/(c*sqrt(G*rho_L))` evaluated as diagnostics |
| `G` | Newton/scale gravitational constant | measured input `6.67430e-11 m^3 kg^-1 s^-2`; `G_N`, `G_bare`, `G_cosmo` kept separate per FRAMEWORK_CONTRACT |
| `c` | speed of light | exact `299792458 m/s` |
| `rho_L` | mass density of the vacuum in the candidate constraint | kg/m^3; the quantity the constraint ties to `a0` |
| `rho_Lambda` | framework vacuum mass density `= 4*a0^2/(G*c^2)` | derived from the adopted `a0` + `kappa = 1/2` (input number, not a mechanism) |
| `lambda` | dimensionless ratio `rho_L / rho_Lambda` (ratio to the **adopted** framework density) | `lambda = 1/(4*kappa^2)`; diagnostics at `lambda = 1/2, 1, 2` |
| `F` | constraint function `4*a0^2 - G*c^2*rho_L` | units m^2 s^-4 (acceleration squared) |
| `eta` | Lagrange multiplier | units: action density / [F] = kg s^2 m^-3 = [G^-1]. |
| `s` | vacuum rate `c*sqrt(G*rho_L)` | m/s^2 (acceleration scale of the MU_n branch argument) |
| `Y` | `g/s` | dimensionless response argument |
| `g` | total radial acceleration | m/s^2 |
| `mu_n` | `1 - (1+Y)^(-n)`, `n >= 1` | conditional MU_n statistical response; MU2 = n=2 cell |
| `T^eta_munu` | stress contributed by the constraint term | kg m^-1 s^-2 |
| `pi_a0, pi_rho, pi_eta` | conjugate momenta in the Dirac–Bergmann analysis | zero for non-propagating auxiliaries |

### 1.3 Framework inputs vs. conclusions

**Framework inputs (not derived here):** `kappa = 1/2`, `G`, `c`, the two registered footings `a0 = 9.3619e-11 m/s^2` (canonical) and `a0 = 1.1279e-10 m/s^2` (alternative), `M_sun`, `pc`, `rho_Lambda = 4*a0^2/(G c^2)`, and the branches Q, RAR, MU2, EXP, MONO as distinct (FRAMEWORK_CONTRACT dictionary).

**Conclusions to be established (this run):**

1. (T1) `F = 0` is **algebraically identical** to the adopted one-half normalization: for `rho_L > 0`, `a0 > 0`, `G c != 0`, with `kappa := a0/(c sqrt(G rho_L))` (candidate definition) and `lambda := rho_L/rho_Lambda`:

   `F = 0  <=>  rho_L = 4a0^2/(G c^2)  <=>  kappa^2 = 1/4  <=>  kappa = 1/2`.

   The constraint *is* the statement `kappa = 1/2`; it cannot certify the adopted value without circularity.

2. (T2) In every consistent coupling, `F = 0` arises as **the multiplier equation of motion** (variation w.r.t. `eta`). The relation is **imposed by construction — never emergent**. No variation of the host/matter/vacuum sector produces it.

3. (T3) Minimal coupling (constraint term only; `a0, rho_L, eta` independent fields, no other action terms in those fields): on shell `eta = 0` and the pair `(a0, rho_L)` is a **one-parameter family** `(alpha, 4 alpha^2/(G c^2))`, `alpha > 0`. The Dirac–Bergmann classification of the sector is 4 second-class + 1 first-class constraints (first-class generator `chi = (G c^2/(8 a0)) pi_a0 + pi_rho`), **zero propagating degrees of freedom**, and the one-parameter family is exactly the gauge orbit of `chi`. The constraint **removes no independent freedom**.

4. (T4) Vacuum-energy coupling (add `-chi int rho_L sqrt(-g)`, `chi = c^2`; `a0` a parameter, `rho_L`, `eta` fields): `eta = -chi/(G c^2) = -1/G` is forced (no new free coupling), `F = 0` at the stationary point, the multiplier stress `T^eta_munu = eta F g_munu` vanishes **on-shell**, and the vacuum sector is a cosmological constant `Lambda_eff = 32 pi (G_E/G_N) a0^2/c^4` — the framework `Lambda = 32 pi a0^2/c^4` identity restored **only when the Einstein and scale constants coincide** (`G_E = G_N`) and `kappa = 1/2`; the ratio is carried, not set equal.

5. (T5) If **both** `a0` and `rho_L` are fields with the vacuum term present, the sector is **overdetermined and has no on-shell solution** (`eta = 0` forced by the `a0` axis, `eta = -1/G` forced by the `rho_L` axis; consistent only for `chi = 0`). The naive "consistent coupling" does not exist for that variable choice.

6. (T6) If `a0` (or `rho_L`) carries metric dependence or host couplings, `T^eta` is no longer proportional to `F` and the eta sector modifies the gravity equations even on the constraint surface — the theory is changed, and the on-shell cancellation of the multiplier stress is lost.

**Counterexample to the claim that the multiplier-enforced constraint removes the kappa freedom / derives kappa = 1/2:** the full on-shell solution set of the minimally coupled constrained system contains, for *every* `alpha > 0`, the configuration `(a0, rho_L) = (alpha, 4 alpha^2/(G c^2))`. Relative to the adopted reference footing `(a0*, rho_Lambda*)`, the members at `rho_L/rho_Lambda* = 1/2, 1, 2` (equivalently `kappa = 1/sqrt(2), 1/2, 1/(2 sqrt(2))`) are all admissible, with distinct vacuum rates `s = c sqrt(G rho_L) = 2 alpha` and distinct MU_n branch arguments `Y = g/(2 a0* sqrt(lambda))`. Nothing in the constrained system selects `alpha = a0*`. `kappa = 1/2` remains an adopted input. (k01's audit rule — "no mechanism counts unless a0 and Lambda begin independent and the equations remove one degree of freedom" — is therefore **not** satisfied by this coupling: the constraint relates the pair without pinning its member.)

**Assumptions / boundary conditions / domain:** `G != 0`, `c != 0`, `a0 > 0`, `rho_L >= 0` (physical `rho_L > 0` for `sqrt(G rho_L)`); `lambda > 0`; `g > 0`, `s > 0`, `Y = g/s`, `n >= 1` symbolic with numerical diagnostics `n = 1, 2, 3`; flat-local variation (`sqrt(-g) = 1` conventions carried explicitly); static/algebraic constraint — no time derivatives of `a0, rho_L, eta` in the constraint term; no limiting regime used (exact algebra throughout; the "leading neglected term" of any expansion is exactly zero, stated rather than assumed). Pointwise multiplier (any smearing argument rescales `eta` by the smearing function; classification unchanged).

---

## 2. Vary eta and every dynamical quantity: extra equations and stresses (seed step 2)

### 2.1 Variation algebra (with signs, factors, units)

Let the total action be

```
S = S_host[g, psi; a0] + S_vac(rho_L) + S_eta,
S_eta = int eta (4 a0^2 - G c^2 rho_L) sqrt(-g) d^4x.
```

Variations (all factors and signs shown):

```
delta S_eta / delta eta       = F = 4 a0^2 - G c^2 rho_L              [constraint]
delta S_eta / delta rho_L     = -G c^2 eta                            [multiplier axis]
delta S_eta / delta a0        = +8 a0 eta                             [scale axis]
delta S_eta / delta g^{mu nu} :  delta sqrt(-g) = -(1/2) sqrt(-g) g_{mu nu} delta g^{mu nu}
  =>  delta S_eta = int eta F (-(1/2) sqrt(-g) g_{mu nu} delta g^{mu nu})
  =>  T^eta_{mu nu} := -(2/sqrt(-g)) delta S_eta/delta g^{mu nu} = +eta F g_{mu nu}.
```

Units: `[F] = m^2 s^-4`; `[eta] = [L]/[F] = (kg m^-1 s^-2)/(m^2 s^-4) = kg s^2 m^-3 = [G^-1]` — so `eta = -1/G` (case T4) is dimensionally forced, a sign check. `[eta F] = kg m^-1 s^-2` — pressure/energy density, consistent with `T^eta`.

Vacuum term `S_vac = -chi int rho_L sqrt(-g)` (for the standard vacuum energy density `chi = c^2`):

```
delta S_vac / delta rho_L = -chi sqrt(-g)                  [density axis]
T^vac_{mu nu} = -chi rho_L g_{mu nu}                       [vacuum stress]
```

Divergence consistency: `nabla^mu T^eta_{mu nu} = eta nabla_nu F` (for constant `eta`), so the Bianchi identity forces `F = const` along the flow; the constraint `F = 0` is exactly the consistency condition. Any configuration kept off-shell with `F != 0` violates energy conservation at `O(eta nabla F)`.

### 2.2 Taxonomy of couplings

**Case I — global parameters (a0, rho_L constants; eta a global multiplier).** Stationarity in `eta` gives the parameter restriction `F = 0`; the host equations are untouched; `eta` is undetermined (dummy). The restriction is a re-statement of the definition `rho_Lambda = 4 a0^2/(G c^2)` — i.e., of the adopted `kappa = 1/2`. Freedom not removed: the pair `(a0, rho_L)` still ranges over the one-parameter family.

**Case II — local fields, no dynamics for a0, rho_L (S_vac = 0, S_host independent of rho_L).** Equations of motion:

```
F = 0        (eta variation)
-G c^2 eta = 0  =>  eta = 0                      (rho_L variation; G,c != 0)
+8 a0 eta = 0  =>  eta = 0                       (a0 variation; a0 > 0)
```

On shell: `eta = 0`, `F = 0`; the pair `(a0, rho_L) = (alpha, 4 alpha^2/(G c^2))` with `alpha > 0` free. The constraint sector is **dynamically inert**: `T^eta = eta F g = 0` identically on shell. The relation is imposed (it is an equation of motion) but constrains *nothing observable*: `alpha` remains a free input, so the number that must be measured (the vacuum scale/density) is not fixed.

**Case III — vacuum term present, a0 a parameter.** Equations:

```
F = 0,    -G c^2 eta - chi = 0  =>  eta = -chi/(G c^2),   chi = c^2:  eta = -1/G.
```

`eta` is **not a free coupling** — it is fixed by the density coefficient `chi`. On-shell stress:

```
T^eta = eta F g_munu = 0  (on shell),    T^vac = -chi rho_L g_munu = -rho_L c^2 g_munu,
Lambda_eff = 8 pi G_E chi rho_L / c^4 = 32 pi (G_E/G_N) a0^2 / c^4  (using F = 0),
with G_E = G_N:  Lambda = 32 pi a0^2 / c^4  —  the framework Lambda identity.
```

The multiplier couples consistently *on the constraint surface*, at the price of (i) one fixed coupling `eta = -1/G` with no freedom, and (ii) `a0` still an input parameter. Imposed, not emergent; freedom not removed.

**Case IV — a0 and rho_L both fields + vacuum term.** `eta = -1/G` (rho_L axis) vs `eta = 0` (a0 axis): **no solution** unless `chi = 0`. Overdetermined; the consistent coupling does not exist for this variable choice. (Recorded as the correct resolution of the would-be "two equations, one constraint": one of `a0`, `rho_L` must be demoted to a parameter.)

**Case V — metric/host-coupled a0.** If `a0` (or `rho_L`) depends on `g` or enters `S_host` (e.g., the a0-cell of a MOND kernel or the heat filter), then

```
T^eta_{mu nu} = eta F g_{mu nu} + (terms from delta(eta F)/delta g^{mu nu} at fixed eta)
```

does not vanish on shell unless `delta F/delta g^{mu nu}` vanishes on the surface, and `S_host`'s a0-variation feeds back through `delta F/delta a0`. The theory is changed; the "coupling without consequence" claim fails in this case a fortiori.

### 2.3 Dirac–Bergmann classification of the minimal sector (Case II)

Canonical pairs per space point: `(a0, pi_a0)`, `(rho_L, pi_rho)`, `(eta, pi_eta)`. The constraint term has no time derivatives, so all three momenta are primary constraints. Consistency chain (H_T = H + int lambda_i C_i, H_c = -eta F):

```
pi_eta ~ 0  ->  {pi_eta, H_T} = -dH/deta = +F  =>  C_F := F ~ 0            (secondary)
pi_rho ~ 0  ->  {pi_rho, H_T} = -dH/drho_L = -eta G c^2  =>  C_eta := eta ~ 0  (tertiary)
pi_a0 ~ 0  ->  {pi_a0, H_T} = -dH/da0 = +8 eta a0  ~ 0   (automatic given eta ~ 0)
{F, H_T} = 0   (F is algebraic in a0, rho_L, which Poisson-commute)          (automatic)
```

Constraint set `C = {pi_a0, pi_rho, pi_eta, F, eta}`. Poisson matrix (local, per point; delta-factors common):

```
       pi_a0  pi_rho  pi_eta  F       eta
pi_a0   0      0       0       -8 a0   0
pi_rho  0      0       0       +G c^2  0
pi_eta  0      0       0       0       -1
F       +8 a0  -G c^2  0       0       0
eta     0      0       +1      0       0
```

Rank = 4 (block ranks 2 + 2). Null vector `(G c^2/(8 a0), 1, 0, 0, 0)` → **exactly one first-class constraint** `chi = (G c^2/(8 a0)) pi_a0 + pi_rho` (verified symbolically in the prototype). Its gauge orbit:

```
delta a0 = {chi, a0} = -G c^2/(8 a0),   delta rho_L = {chi, rho_L} = -1,
delta F = 8 a0 delta a0 - G c^2 delta rho_L = -G c^2 + G c^2 = 0.
```

i.e. exactly the tangent of the family `(alpha, 4 alpha^2/(G c^2))`. **The surviving freedom of the constraint sector is a first-class gauge direction**: the constrained theory cannot select `alpha`; physical DOF count `(2*3 - 4 - 2*1)/2 = 0` — the sector propagates nothing. (Case I: same, with `eta` a dummy; Case III: same classification, `eta` shifted by the vacuum coefficient; Case IV: inconsistent chain as in 2.2.)

**Imposed or emergent? — Answer.** In every case `F = 0` is the multiplier (eta) equation of motion: **imposed by construction**. It never arises from the host/vacuum sector dynamics (**not emergent**). Moreover the imposition is degenerate: it encodes `kappa = 1/2` (T1) and leaves the physical scale as a gauge/family direction (T3). The constraint is a repackaged adoption, not a derivation, and the seeded claim that coupling it "consistently" removes an independent freedom is false (explicit counterexample: the family members at `lambda = 1/2, 2`).

---

## 3. Intermediate algebra, scale factors, signs, units (seed step 3)

Exact identities (no limit taken; no neglected term):

```
rho_Lambda := 4 a0^2/(G c^2)   (framework density at adopted a0, kappa = 1/2)
F = 4 a0^2 - G c^2 rho_L = 4 a0^2 (1 - lambda),   lambda := rho_L/rho_Lambda
kappa := a0/(c sqrt(G rho_L))  =>  kappa^2 = 1/(4 lambda)  <=>  lambda = 1/(4 kappa^2)
s = c sqrt(G rho_L) = 2 a0 sqrt(lambda)             (scale identity, derived in full below)
Y = g/s = g/(2 a0 sqrt(lambda))
mu_n(Y) = 1 - (1+Y)^(-n);  at lambda = 1: Y = g/(2 a0),  mu_2 = 1 - (1 + g/(2a0))^(-2)  ==  MU2 cell
```

Derivation of the scale identity `s = 2 a0 sqrt(lambda)` (all signs/factors):

```
s^2 = c^2 (G rho_L) = c^2 G (lambda 4 a0^2/(G c^2)) = 4 a0^2 lambda = (2 a0 sqrt(lambda))^2,
s >= 0 and 2 a0 sqrt(lambda) >= 0  =>  s = 2 a0 sqrt(lambda).
```

Diagnostic values (canonical footing `a0* = 9.3619e-11 m/s^2`; `g = a0*`, `x = 1`):

```
lambda = 1/2 :  s = sqrt(2) a0* = 1.32400e-10 m/s^2,  Y = 0.70711,  kappa = 1/sqrt(2) = 0.70711
lambda = 1   :  s = 2 a0*      = 1.87238e-10 m/s^2,  Y = 0.50000,  kappa = 1/2        = 0.50000
lambda = 2   :  s = 2 sqrt(2) a0* = 2.64799e-10 m/s^2, Y = 0.35355, kappa = 1/(2 sqrt 2) = 0.35355

mu_2 = 1 - (1+Y)^(-2):  lambda=1/2: 0.65685;  lambda=1: 0.55556;  lambda=2: 0.45418
mu_1 = 1 - (1+Y)^(-1):  lambda=1/2: 0.41421;  lambda=1: 0.33333;  lambda=2: 0.26120
mu_3 = 1 - (1+Y)^(-3):  lambda=1/2: 0.79899;  lambda=1: 0.70370;  lambda=2: 0.59675
```

Only `lambda = 1` reproduces the framework MU2 cell at `Y = x/2`. The other two diagnostics are perfectly good constrained-theory configurations (they satisfy every equation of motion of Case II with their own `alpha`) — the constraint does not select among them.

**Units ledger** (SI exponent vectors):

```
[a0] = (0,1,-2);  [F] = (0,2,-4);  [eta] = (1,0,2)·? => kg s^2 m^-3 = (1,-3,2);
[eta F] = (1,-1,-2) kg m^-1 s^-2;  [rho_L c^2] = (1,-1,-2);  [Lambda_eff] = (0,0,-2)·? => m^-2 ✓;
[kappa], [lambda], [Y], [mu_n] dimensionless ✓.
```

**Two-footing rule (FRAMEWORK_CONTRACT):** the footings cannot share both fixed `rho_Lambda` and fixed `kappa`:

```
fixed kappa = 1/2:  rho_Lambda(canonical) = 4(9.3619e-11)^2/(G c^2) = 5.844412454e-27 kg/m^3,
                    rho_Lambda(alt)      = 4(1.1279e-10)^2/(G c^2) = 8.483089620e-27 kg/m^3,
                    ratio = (a0_alt/a0_can)^2 = 1.45148716
fixed rho_Lambda = 5.844412454e-27:   kappa_eff = a0_alt/(c sqrt(G rho_Lambda)) = 0.60238840.
```

The two registered footings are **two members of the same one-parameter family** of the constrained theory (member `lambda = (a0_alt/a0_can)^2 = 1.45148716` relative to the canonical reference): both are internally consistent with `F = 0`, and the constraint cannot prefer either. This is the concrete, quantitative face of "no freedom removed."

---

## 4. Independent checks, different representations, actual residuals (seed step 4)

All residuals are computed in the prototype (`compute_AS070_prototype.py`, mpmath 60 digits) and recorded in `residuals.json`. Tolerances set before evaluation: 1e-30 relative (numeric identity checks), exact zero for fraction-symbolic checks.

| Check | Representation | Observed residual | Pass |
|---|---|---|---|
| C1 F-residual, canonical footing | direct substitution `4a0^2 - G c^2 rho_Lambda` | ~1e-60 relative | yes |
| C2 F-residual, alternative footing | direct substitution | ~1e-60 relative | yes |
| C3 exact identity `F = 4a0^2(1-lambda)` | sympy expand-difference | 0 (exact symbol) | yes |
| C4 `s = 2 a0 sqrt(lambda)` on lambda-grid {1/2, 1, 2} × both footings | direct vs composed | ~1e-60 relative | yes |
| C5 `kappa = 1/(2 sqrt(lambda))` on the grid | direct vs composed | ~1e-60 relative | yes |
| C6 direct differentiation: `dF/dlambda = -4 a0^2` | central finite difference, step 1e-8 | ~1e-34 relative | yes |
| C7 Dirac matrix rank = 4, null vector `(G c^2/(8a0), 1, 0, 0, 0)` | sympy Matrix.rank()/nullspace() | exact | yes |
| C8 MU2 cell mapping at lambda = 1, `mu_2(g/(2a0)) = 1-(1+g/(2a0))^(-2)` | mpmath 60 | ~1e-60 | yes |

(Lean certificate section 6 certifies the algebraic core: T1, the s-identity, the kappa-lambda correspondence, and the mu2 rational form.)

---

## 5. Negative controls (seed step 5) — both capable of failing, both fail as designed

**NC1 — "Vary only eta and ignore its stress contribution while claiming an unchanged theory."** Take the Case-III coupling (`eta = -1/G`, nonzero multiplier — the only regime in which `eta` "does something") and evaluate the multiplier stress at off-shell diagnostics:

```
T^eta_00 = eta F = -(1/G) 4 a0^2 (1 - lambda):
  lambda = 1/2:  T^eta_00 = -2 a0^2/G = -2.62630e-10 kg m^-1 s^-2,
                 T^vac_00   = -rho_L c^2 = -2.62630e-10 kg m^-1 s^-2
                 =>  |T^eta_00| / |T^vac_00| = 1.00000  — O(1) stress omitted.
  lambda = 2:    T^eta_00 = +4 a0^2/G = +5.25261e-10,  ratio |T^eta|/|T^vac| = 0.50000, sign flip.
  lambda = 1:    T^eta_00 = 0 (on-shell cancellation survives).
```

**Finding:** dropping `T^eta` while enforcing `F = 0` with `eta != 0` misstates the total vacuum stress by O(1) (factor 2 at `lambda = 1/2`, factor 1.5 at `lambda = 2`). The claim "theory unchanged" is **false off-shell and in any numerical scheme that holds `F != 0` transiently**; the only regime in which it holds (Case II, `eta = 0`) is exactly the regime in which the constraint removes nothing (T3). The control **fails as it must**.

**NC2 — deep/Newtonian regimes.** `F` is algebraic in `(a0, rho_L)` with no `g`-dependence: deep/Newtonian limits do not exist for the constraint itself. Substitute (normalization + boundary cases, exact identities):

```
(a) F(lambda=1-eps) = +4 a0^2 eps > 0,  F(lambda=1+eps) = -4 a0^2 eps < 0:  sign flip at the adopted point;
(b) lambda -> 0+:  s -> 0, kappa -> inf:  family degenerates onto a0 -> 0 (MOND scale vanishes) — consistent limiting algebra;
(c) lambda -> inf: s -> inf, kappa -> 0:  family degenerates onto rho_L -> inf — consistent limiting algebra;
(d) vacuity witness: the Case-II configuration (a0, rho_L, eta) = (a0* sqrt(lambda), lambda rho_Lambda*, 0) satisfies
    EVERY field equation of the constrained system for lambda = 1/2, 1, 2 (checks F = 0, eta = 0, host EOMs unchanged) — exact identities, not numerics.
```

These are exact algebraic identities (fraction arithmetic), not finite numerical agreements; the distinction is recorded in `residuals.json`.

---

## 6. Lean certificate

File: `AS070_constraint_coupling_certificates.lean` (self-contained, Mathlib v4.34.0-rc2, verified `lake env lean` from `fable_independent_2026/lean_2026`, exit 0, zero `sorry`, unfiltered `#print axioms` = `[propext, Classical.choice, Quot.sound]`; compile host untouched).

Certified (all in `Real`):

- `f_iff_lambda_eq_one`: `4*a0^2 - G*c^2*rho_L = 0 <-> lambda = 1` (`G,c,a0 != 0`, `lambda = G*c^2*rho_L/(4*a0^2)`) — the constraint *is* the adopted normalization.
- `f_iff_rho_framework`: `F = 0 <-> rho_L = 4*a0^2/(G*c^2)`.
- `f_eq_4a0sq_one_sub_lambda`: the exact factor form used by all diagnostics.
- `s_two_a0_sqrt_lambda`: `c*sqrt(G*rho_L) = 2*a0*sqrt(lambda)` (`G,c > 0`, `a0 > 0`, `rho_L >= 0`) — the MU_n scale identity, via `Real.mul_self_sqrt`/`mul_self_eq_mul_self_iff` reasoning on squares.
- `kappa_sq`: `(a0/(c*sqrt(G*rho_L)))^2 = (1/4)/lambda` and `kappa_half`: `F = 0` + positivity ⇒ `kappa = 1/2` — the "constraint ⟺ one-half" statement.
- `mu2_rational_form`: `(1+Y)^2 * mu2(Y) = Y*(Y+2)` with `mu2(Y) = 1 - (1+Y)^(-2)`-form — the MU2 algebraic identity used in section 3.
- `mu2_framework_mapping`: the `Y = g/(2a0)` form equals the `(g/a0)/2` form — the framework MU2 cell at `lambda = 1`.

---

## 7. Strongest surviving statement and next implication (seed step 5, contribution to closure)

**Strongest surviving statement (conditional theorem, exact):** For the same-theory cell `S = S_host[g, psi; a0] + S_vac(rho_L) + int eta F sqrt(-g)`, `F = 4a0^2 - G c^2 rho_L`, with `G,c != 0`, `a0 > 0`, `rho_L >= 0`:

the relation `F = 0` is **imposed (multiplier EOM), never emergent**; it is **algebraically identical to the adopted `kappa = 1/2`** (T1); the multiplier sector carries **zero propagating degrees of freedom** and leaves a **one-parameter gauge/family freedom** `(a0, rho_L) = (alpha, 4 alpha^2/(G c^2))` (T3, Dirac rank 4 + first-class `chi`); a vacuum term pins `eta = -1/G` (no new coupling) and reproduces `Lambda_eff = 32 pi (G_E/G_N) a0^2/c^4` (T4); both `a0` and `rho_L` dynamical + vacuum term is **inconsistent** (T5); metric/host-coupled `a0` changes the theory (T6). **The proposed normalization constraint, coupled consistently, does not remove the kappa freedom** — the counterexample is the on-shell family at `lambda = 1/2, 1, 2` — so `kappa = 1/2` and the vacuum magnitude `alpha` remain adopted inputs, exactly as the seed's principle anticipates ("The adopted one-half normalization is not a derived result unless an independent argument removes its freedom").

**First additional implication needed to transfer to the full theory (do not fix by a different branch):** the surviving one-parameter freedom `alpha` (the physical value of the vacuum density / the footing choice) must be pinned by a mechanism *outside* the constraint sector. The repository's own first-principles obstructions line up with this result rather than against it: k01's zero-mode theorem (the static bulk action is invariant under adding a constant to the kernel primitive — no local action term fixes the additive normalization) and PD08's premise `s = c sqrt(G rho_Lambda)` set *independently of a0* are the only routes on record that could supply the missing input, and neither is a multiplier constraint. Transfer to the operative filtered-MONO target additionally requires the branch bridge: this run concerns the CORE coefficient cell and the conditional MU_n response only; nothing here is asserted about RAR/MONO kinematics, the heat filter, or the thirteen-requirement target.

**Affected gate:** Requirement 13 (a0–vacuum relation kept as input or genuinely derived) gate-map cell A03 ("coefficient mechanisms and their missing premises"): this run closes the *normalization-constraint* branch of that gate (it cannot serve as the missing premise); the gate remains OPEN (no mechanism, kappa and rho magnitude adopted inputs).

---

## 8. Limitations

- Does **not** derive `kappa = 1/2`; demonstrates that the studied constraint mechanism cannot (imposed-vs-emergent determination, all cases).
- Does not fix the vacuum density magnitude (footing choice canonical vs alternative remains a physical/data question, cf. AS001/AS011).
- Does not treat time-dependent or nonlinear closures of the constraint chain beyond the pointwise Dirac classification (no dynamics of `a0, rho_L, eta` were introduced; the classification is exact for the minimal static sector).
- Does not analyze the eta sector when `a0`/`rho_L` carry host couplings (Case V direction recorded as the changed-theory statement, not fully classified) — this is the child proposal.
- Numerical residuals are finite evidence (60-digit, tolerances pre-set); exactness rests on the algebra and the Lean certificate for the algebraic core. No observational data used; no fit performed; "observational preference as proof" explicitly avoided per the seed.
- Branch scope: conclusions are confined to the CORE coefficient / MU_n cell; no branch translation performed; MONO/RAR/EXP claims untouched.

*(Full command records, bounds, residuals, hashes, and the schema-v2 result are in `result.json`.)*