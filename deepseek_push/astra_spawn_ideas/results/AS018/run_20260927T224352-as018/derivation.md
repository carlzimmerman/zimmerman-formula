# AS018 — Reference potential and gauge-independent force

**Run**: `run_20260927T224352-as018`
**Worker**: deepseek/deepseek-v4-flash-0731 (Hermes Agent subagent, openrouter)
**Task hash**: `4ce68e954be29f7c62eab91023099a734a01df35280677874637d3b8e9d2397d` (AS018 seed file)
**Branch cell**: CORE scale identities; deep-MOND radial potential `Phi = C ln(r/r_ref)`; MONO (filtered RAR) used as the operative deep-interpolation reference; causality criterion B.
**Sources (hash-verified against SOURCE_MANIFEST.json before execution)**: README.md `91a5fac4…`, FRIED_CHICKEN_SPEC.md `98d9149f…`, DERIVATIONS.md `8da8176e…`.

---

## 1. Precise claim, symbol dictionary, boundary conditions, assumptions

### 1.1 Framework inputs (adopted, not derived here)

```text
a0        = kappa · c · sqrt(G · rho_Lambda),        kappa = 1/2 ADOPTED
rho_Lambda= 4 a0^2 / (G c^2)                          [kg/m^3]
r_M       = sqrt(G M_b / a0)
C         = sqrt(G M_b a0)   so that  v_flat^4 = G M_b a0 = C^2
```

Numerical conventions (SI): `G = 6.67430e-11`, `c = 299792458`, `M_sun = 1.98847e30`, `pc = 3.085677581491367e16`, `k_B = 1.380649e-23`. `G_N`, `G_bare`, `G_cosmo` are kept as separate symbols; this task uses the single Newton constant `G` only — no identification of distinct couplings is made (framework contract, mandatory-scale section).

Both footings are carried separately and labelled, never mixed:
**canonical** `a0_c = 9.3619e-11 m/s^2` and **alternative** `a0_a = 1.1279e-10 m/s^2` (alternative normalization: different density for the same kappa; the two do not share both a fixed rho_Lambda and a fixed kappa simultaneously).

### 1.2 Symbols

| Symbol | Meaning | Units |
|---|---|---|
| `Phi` | deep radial potential, `Phi(r) = C ln(r/r_ref)` | m^2/s^2 |
| `r_ref` | reference radius (potential zero), > 0 | m |
| `K` | additive gauge constant, `Phi -> Phi + K` | m^2/s^2 |
| `g` | radial force magnitude, `g = |d Phi/dr|` (inward positive) | m/s^2 |
| `B = g_N` | Newtonian (baryonic) radial acceleration, > 0 | m/s^2 |
| `y = B/a0`, `z = sqrt(y) = r_M/r` | dimensionless deep variables | 1 |
| `nu_RAR(y)` | `1/(1 - exp(-sqrt y))` (RAR branch) | 1 |
| `h_RAR(y)` | `y (nu_RAR(y) - 1)`; peak `y_p`, value `h_p = h_RAR(y_p)` | 1 |
| `y*` | MONO splice point (`h'_RAR(y*) = delta·h_p/(y*+y_p)`) | 1 |
| `delta` | 0.05 (framework MONO parameter) | 1 |
| `S` | heat filter `exp[(xi^2/2) Delta]`; `xi` smoothing scale | 1 |
| `S*` | adjoint of `S` in the chosen measure | 1 |
| `N` | lapse weight for filtered-system measure `d mu_N = N d mu` | 1 |
| `E` | fixed-well energy `E = ∫ rho_b Phi dV` at fixed mass | J |
| `rho_b` | baryonic mass density (fixed under the gauge) | kg/m^3 |
| `M_b` | total baryonic mass `∫ rho_b dV` (fixed) | kg |

### 1.3 Assumptions and boundary conditions (distinguished from conclusions)

*Assumptions (framework inputs, per contract):* kappa = 1/2 adopted; the deep functional form `Phi = C ln(r/r_ref)` (from `-dPhi/dr = C/r`, i.e. `v_flat^4 = C^2 = G M_b a0`); `rho_b` fixed and independent of `Phi` (no back-reaction on the source — the well is a test well; source coupling is a separately listed open dependency); positive-domain variables `r > 0`, `r_ref > 0`.

*Boundary conventions (each stated, each is a *convention*, not a conclusion):*
1. **Potential zero / reference radius** `r_ref`: the point where `Phi = 0`. The named task's object of study: *changing `r_ref` shifts `Phi` by a constant* (proved, §3.1); the zero location is therefore a pure convention.
2. **Fixed-well energy** `E = ∫ rho_b Phi dV`: for compactly supported / sufficiently decaying `rho_b` the integral converges and the gauge shift is `E -> E + K M_b`; for unbounded-mass or non-decaying `rho_b` the log well diverges at large `r` and a box normalization `Phi_box(r) = C ln(r/r_box)` (zero at the box edge `r_box`) is required. Either way a boundary condition must fix the reference before `E` is a number; gradients never need it. (§3.2, Lean `well_energy_shift`.)
3. **S operator** (framework contract requires "specify the metric, measure, domain and boundary conditions that define S and its adjoint S*"): in the filtered system the flat Euclid metric is used for the Laplacian; the concrete certificates here use (i) the finite chain with **uniform counting measure** on a **periodic domain** (S^1, 64 sites, wrap-around edges) and (ii) the same chain with **zero Dirichlet boundary** (vanishing at both ends); the **lapse-weighted measure** `d mu_N = N d mu` with `N(theta) = 1 + 0.3 sin(theta)` is considered separately. On the periodic domain the constant function is the zero mode (`S·1 = 1` exactly, residual 2.9e-15), so `S` preserves constants; on the Dirichlet domain there is **no constant mode** and `S·1 != 1` (defect 0.326) — the smoothing operator genuinely depends on the boundary data. `S` is symmetric in the uniform measure (`||S - S^T||/||S|| = 8.9e-17`) but **not** in the lapse-weighted measure: `S*_N = N^{-1} S^T N != S` (norm ratio 0.014, adjoint identity residual 8.5e-16). Consequence recorded (not re-derived here): a gauge- or measure-variation of the filtered system must vary `S` itself when the action is varied; varying only `u` while holding `S` fixed is a different mathematical model.

### 1.4 Precise claims established

Let `kappa = 1/2`, `a0 = kappa c sqrt(G rho_Lambda)`, `M_b > 0`, `C = sqrt(G M_b a0)`. For all `r > 0`, all `r_ref, r_ref1, r_ref2 > 0`, all `K`:

- **(C1) Principal test identity**: `d/dr [C ln(r/r_ref)] = C/r` identically.
- **(C2) Gauge invariance of the force**: adding any constant `K` to `Phi`, or changing `r_ref`, leaves the force `C/r` pointwise unchanged.
- **(C3) Reference shift is a constant shift**: `C ln(r/r_ref2) - C ln(r/r_ref1) = C ln(r_ref1/r_ref2)`, independent of `r`.
- **(C4) Fixed-well energy shift**: at fixed `rho_b` (fixed `M_b`), `E[Phi + K] = E[Phi] + K·M_b`.
- **(C5) Rejection of the gauge artifact**: interpreting the arbitrary potential zero as a measured extra vacuum density is an **invalid inference** (negative control H, §5); the framework density `rho_Lambda = 4 a0^2/(G c^2)` is gauge-invariant and unaffected by `K`.

(C1)–(C4) hold identically in both footings (they enter only through `C`, `r_M`); (C5) is verified numerically on both footings' `rho_Lambda`.

---

## 2. Force invariance and the fixed-well energy shift

**Force invariance.** By the chain rule,

```text
d/dr [C ln(r/r_ref)] = C · (1/(r/r_ref)) · (1/r_ref) = C/r,
```

the two scale factors `r_ref` cancel exactly — this is the cancellation the task asks to exhibit. For `Phi_K(r) = C ln(r/r_ref) + K`,

```text
d Phi_K/dr = d Phi/dr + dK/dr = C/r,
```

so `g = |d Phi/dr| = C/r` for every `K` and every `r_ref`:

```text
Phi(r; r_ref2) - Phi(r; r_ref1) = C [ln(r/r_ref2) - ln(r/r_ref1)]
                                = C ln(r_ref1/r_ref2)  =  constant in r.
```

**Fixed-well energy at fixed mass.** With `rho_b` independent of the gauge,

```text
E[K] = ∫ rho_b (Phi + K) dV = ∫ rho_b Phi dV + K ∫ rho_b dV = E[0] + K M_b.
```

(Lean certificate `well_energy_shift` proves the identity in Bochner-integral form: `∫_s rho·(Phi + c) d mu = ∫_s rho·Phi d mu + c·∫_s rho d mu`, with `IntegrableOn` and `MeasurableSet s` hypotheses.)

**Required boundary-energy convention.** The two-parameter gauge orbit `(r_ref, K)` of the deep potential is generated by `Phi -> Phi + const`. A fixed-well `E` becomes a number only after a convention selects the constant: prescribed `r_ref` (then `Phi(r_ref) = 0`), a box edge `r_box` with `Phi(r_box) = 0` for truncated domains, or — where it converges — the large-`r` normalization. `g = grad Phi` and all gradient observables are convention-independent; the energy is convention-dependent by exactly `K M_b`. There is no gauge-invariant "absolute level" of the logarithmic well.

---

## 3. Intermediate algebra, scale factors, signs, units

**Derivative.** `d/dr ln u = u'/u` with `u = r/r_ref`: `(d Phi/dr) = C·(1/r)`; sign convention: `Phi` increases outward (`d Phi/dr = C/r > 0`), the inward force magnitude is `|d Phi/dr| = C/r`; all numerics use `|grad|`. Units: `C = sqrt(G M_b a0)` has `(m^3 kg^-1 s^-2 · kg · m s^-2)^{1/2} = m^2 s^-2`; `C/r` is `m s^-2` ✓; `Phi` in `m^2 s^-2`; `rho_Lambda = 4 a0^2/(G c^2)` is `(m s^-2)^2 / (m^3 kg^-1 s^-2 · m^2 s^-2) = kg m^-3` ✓; `E_K - E_0 = K M_b` in `(m^2 s^-2)·kg = J` ✓.

**Footing constants (both footings, M_b = M_sun; mpmath 60-digit, printed to 10–16 digits).**

| quantity | canonical a0 = 9.3619e-11 | alternative a0 = 1.1279e-10 | unit |
|---|---|---|---|
| rho_Lambda = 4a0^2/(Gc^2) | 5.8444124540e-27 | 8.4830896196e-27 | kg/m^3 |
| C = sqrt(G M_sun a0) | 1.1146650453e+05 | 1.2234822744e+05 | m^2/s^2 |
| r_M = sqrt(G M_sun/a0) | 1.1906397690e+15 | 1.0847435716e+15 | m |
| v_flat = (G M_sun a0)^{1/4} | 333.866 | 349.783 | m/s |
| C^2 - v_flat^4 | -1.34e-51 (rounding) | -1.34e-51 (rounding) | (m^2/s^2)^2 |
| r_M^2 - G M_sun/a0 | 0.0 | 0.0 | m^2 |

The identities `v_flat^4 = G M_b a0` (i.e. `= C^2`) and `r_M^2 = G M_b/a0` hold to machine precision in both footings.

**Deep expansion (leading neglected term and its domain).** For `y = B/a0 = (r_M/r)^2`, `z = sqrt y`, the RAR/MONO force is `g = (C/r)·f(z)` with `f(z) = z/(1 - e^{-z})`. Exact series (Bernoulli generating function):

```text
f(z) = 1 + z/2 + z^2/12 - z^4/720 + z^6/30240 - z^8/1209600 + z^10/47900160 + ...
       (all odd z-powers vanish; sympy exact algebra)
g    = (C/r) [1 + z/2 + y/12 - y^2/720 + y^3/30240 + O(y^5)],   z = sqrt y = r_M/r.
```

The predicate was `1 + z/2 + y/12 - y^2/720` (terms through `O(y^2)`); the **leading neglected term is `+y^3/30240` relative**. Domain of validity verified: `10^{-8} <= y <= 10^{-1}`; measured `|remainder|/y^3 = 3.3068783e-5` vs predicted `1/30240 = 3.3068783e-5` (agreement to 8 digits), log-log slope of `|remainder|` vs `y` = 3.0000 (theory: 3). The remarkable feature: the `y^3`-term (i.e. `z^6`) survives while `z^3` vanishes — the deep series has **no odd z-power** (the `exp(-z)` in `nu_RAR` is even-power symmetric at this order). A subtlety worth stating: naive odd-power expectations (slope 5/2) are wrong; Bernoulli structure gives slope 3.

**MONO construction (framework definition, reproduced).** `h_RAR(y) = y(nu_RAR(y)-1) = y e^{-sqrt y}/(1-e^{-sqrt y})`; `h'_mono(y) = max(h'_RAR(y), delta·h_p/(y+y_p))` with `delta = 0.05`; splice at the actual crossing `y*`; continuation `h_mono(y) = h_RAR(y*) + delta·h_p ln[(y+y_p)/(y*+y_p)]`; `nu_mono(y) = 1 + h_mono(y)/y`. Reproduced landmarks: `y_p = 2.53963828` (landmark 2.5396; `h_p = 0.647610`; README's "s = 2.540, Δ = 0.6476" is the same object — noted as a cross-check, not a new input), `y* = 2.33741241` (landmark 2.3374), `h`-continuity at `y*`: 6.6e-17, `C^1` join: 1.6e-62, and the quoted small force difference is `max |log10(nu_mono/nu_RAR)| = 0.01037 dex` (spec bound 0.0104) attained at `y = 14.13`. Per the framework contract this difference cannot transfer derivative/stability/regularity statements by itself — it is a pointwise force bound only, and is used here only as a labelled interpolation cross-check on branch MONO.

---

## 4. Independent check in a different representation (actual residuals)

Four independent representations were run; all residuals are actual numbers from the recorded run (`raw_output.txt`, `residuals.json`).

**(a) Exact symbolic algebra (sympy).** `diff(C ln(r/r_ref), r) - C/r == 0`; `r_ref`-shift constant: `C ln(r/r2) - C ln(r/r1) - C ln(r1/r2) == 0`; gauge derivatives identical; all `True` (exact, not numerical).

**(b) 60-digit numerical differentiation (mpmath `mp.diff`)** over the parameter box `r in {1e11, 1e14, r_M, 1e16, 1e17} m`, `r_ref in {1, r_M/2, 1e17} m`, gauge `K = 12345.678`:
- `d/dr [C ln(r/r_ref)]` vs `C/r`: max relative residual **1.40e-52**;
- gauge-shifted force vs `C/r`: max relative residual **1.40e-52**;
- re-reference `Phi(r; r_ref) - Phi(r; r_ref0) - C ln(r_ref0/r_ref)`: max relative residual **2.93e-60**.

**(c) Float64 radial-grid independent representation (Green + quadrature + finite differences).** Spherical shell source `M_b = 1` at `r_s = 0.1 r_M`, Gaussian width `0.02 r_M`, `N = 65536` log-spaced points over `[0.01, 2000] r_M`. `g_N` from the closed-form erf mass-enclosure `M_enc(r) = M_b/2 [1 + erf((r - r_s)/(sigma sqrt 2))]`; `g = g_N nu_mono(y)`; `Phi` by cumulative trapezoid quadrature outward from `r_M`, then `-d Phi/dr` by finite differences; phantom mass `M_ph = (a0/G) r^2 h_mono(y)` vs `(g - g_N) r^2/G`. Residuals:
- `|grad Phi|` vs `g`: max relative **1.62e-7** (finite-difference + quadrature scale);
- gauge `K0 = 1e-9` (comparable to `|Phi| ~ 1e-10` scale): `|grad(Phi+K0) - grad Phi|_max = 2.17e-19 m/s^2` (float roundoff floor);
- gauge `K0 = 3.14159e+4` (huge): difference 3.81e-6 `m/s^2` **bounded by the predicted rounding bound** `4 eps K0/dx_min = 1.77e-5` (`hugeK_diff_within_rounding_bound = True`; the huge-K difference is float noise, and the bound — not the tiny difference — is the honest pass criterion);
- energy shift: `(E[K]-E[0])/(K M_b) = 0.9999966`, identity relative error **1.16e-16**; mass quadrature `M_enc(inf) = 0.9999966` with deficit `3.39e-6 = 0.5 erfc(4.5)` — the Gaussian tail beyond the 2000 r_M box, a physical truncation, stated as such;
- phantom-mass identity max relative **1.43e-14**;
- deep regime: `g r/C = 1.000250021` vs `1 + z/2 = 1.000250000` (`deep_in_band = True`, band 1.1% of the leading correction); `(v^2 - C)/C = 2.5002e-4` vs leading prediction `z/2 = 2.5000e-4`;
- Newtonian regime: `|nu_mono - 1| < 1e-3` at `y >= 1e5` and the formula-differentiation consistency holds to 1e-12 (`newt_formula_matches_direct = True`).

**(d) Lean 4 certificate** (`AS018_reference_potential_certificates.lean`, compiled with `lake env lean`, exit 0, **zero sorry**, unfiltered `#print axioms` = exactly `[propext, Classical.choice, Quot.sound]` for all seven theorems):
1. `grad_gauge_invariance`: `HasDerivAt f f' x -> HasDerivAt (fun y => f y + c) f' x`;
2. `log_scaled_deriv` and 3. `log_potential_gradient_exact`: `HasDerivAt (fun s => C log(s/r_ref)) (C/r) r` for `0 < r`, `r_ref != 0` (chain rule with the exact cancellation `(r/r_ref)^-1 · (1/r_ref) = 1/r`);
4. `reference_shift_is_constant_shift`: `C log(s/r_ref2) = C log(s/r_ref1) + C log(r_ref1/r_ref2)`;
5. `gradient_reference_independent`: force at `r_ref2` for any `r_ref1`;
6. `well_energy_shift`: `∫_s rho(Phi+c) = ∫_s rho Phi + c ∫_s rho` (Bochner integrals, `IntegrableOn`, `MeasurableSet s`);
7. `deep_series_truncated_inverse`: the truncated-inverse identity `E·F - 1 = z^5/720 + z^6/2160 + z^7/17280 - z^8/86400` with `E = (1 - e^{-z})/z` truncated at `z^4` and `F = z/(1-e^{-z})` truncated at `z^4` (coefficients: `z^3`-term **zero**, `z^4`-term **-1/720** — the two specific statements the deep expansion needs).

These certificates cover the exact algebra used in §2–3; the physical-layer claims (gauge rejection test, footing numerics, grid residuals) are computational evidence per this file, not Lean statements.

---

## 5. Negative control (capable of failing) and the strongest surviving statement

### 5.1 Negative control H: "potential zero = measured extra vacuum density" — REJECTED

Estimator `rho_est(K) = K M_b/(c^2 V_box)` with `V_box = (10 r_M)^3` (a "vacuum density" read off the potential zero inside the box). The control is designed to fail if the inference were valid — that is, if `rho_est` were anchored by anything other than the arbitrary gauge:

- `d rho_est/dK = 1.848e-20 kg/m^3 per (m^2/s^2) of gauge`, range over `K in [-1e4, +1e4]`: 3.70e-16 kg/m^3;
- contrived gauge constants `K* = rho_target c^2 V_box/M_b` reproduce **any** target density exactly: `K* = 3.1619e-07 (m^2/s^2)` gives `rho_Lambda(canonical)`, `K* = 4.5894e-07` gives `rho_Lambda(alternative)`, `K* = 1.5809e-07` gives `rho_Lambda/2`; distinct densities require distinct `K*` (`distinct_K_needed_for_distinct_densities = True`);
- simultaneously every gradient observable is inert: small-K gauge gradient difference **2.17e-19 m/s^2**; huge-K difference bounded by float rounding as in §4(c);
- framework `rho_Lambda` itself is `K`-independent in both footings: 5.8444124540e-27 and 8.4830896196e-27 kg/m^3.

**Conclusion**: *any* alleged vacuum density can be "explained" by *some* potential-zero choice; the potential zero carries no physics; the inference is rejected. The control was capable of failing (e.g., if `rho_est` had a `K`-anchor from the actual `Phi` shape — it does not: `rho_est` is exactly linear in `K` with no offset).

### 5.2 Other controls that can fail

- **Boundary dependence of S** (fails if the operator were boundary-blind): Dirichlet `S·1 = 1 + 0.326` — constant *not* preserved, `Dirichlet_zero_mode_dist = 2.34e-3 > 0` (no zero mode), vs periodic `S·1 = 1` at 2.9e-15 and zero-mode eigenvalue distance 1.15e-16. The operator genuinely changes with the boundary data.
- **Measure dependence of S*** (fails if self-adjointness were measure-independent): in the lapse-weighted measure `S*_N = N^{-1}S^T N != S` (norm ratio 0.01398), adjoint identity `(S u, N v) = (u, N S*_N v)` residual 8.5e-16. Self-adjoint in one measure does not imply self-adjoint in another — exhibited numerically.
- **Deep/Newtonian limits**: deep band check (tolerance 1.1% of the leading correction, actual band error 2.1e-8 relative) and Newtonian `|nu_mono - 1| < 1e-3` at `y >= 1e5`, with the formula-vs-direct consistency at 1e-12.

### 5.3 Strongest surviving statement (domain included)

**Theorem (gauge structure of the deep potential; framework cell: kappa = 1/2, a0 = kappa c sqrt(G rho_Lambda), C = sqrt(G M_b a0), branch MONO for the interpolation only, criterion B).** For `r in (0, ∞)`, `r_ref in (0, ∞)`, any `K`, fixed `rho_b` with `M_b = ∫ rho_b dV < ∞`:

1. `d/dr [C ln(r/r_ref)] = C/r` for all `r` (exact; Lean-certified);
2. the map `(r_ref, K) |-> Phi` is a two-parameter gauge orbit: `Phi(r; r_ref2) + K2 = Phi(r; r_ref1) + K1 + const` with `const = C ln(r_ref1/r_ref2) + (K2-K1)`;
3. every gradient observable `g = |grad Phi| = C/r` is gauge-invariant (C1–C3, Lean-certified); 
4. the fixed-well energy transforms as `E -> E + K M_b` (C4, Lean-certified), so `E` requires an explicit boundary convention (box/reference-radius) while forces do not;
5. any vacuum-density number extracted from the potential-zero location is a gauge artifact (control H) — rejected;
6. statements 1–4 are footing-independent (dimensionless), and apply to both `a0 = 9.3619e-11` and `a0 = 1.1279e-10 m/s^2` with their separate `rho_Lambda = 4 a0^2/(G c^2)`; the huge-`K` numeric invariances hold to within predicted float-rounding bounds on the tested grid (`[0.01, 2000] r_M`, 65536 sites).

Verified domains: symbolic (all `r`, `r_ref` positive); mpmath box `r in [1e11, 1e17] m`; grid `r in [0.01, 2000] r_M`; deep series `y in [1e-8, 1e-1]`; MONO landmarks around `y* = 2.3374`, `y_p = 2.5396`; `S`-checks on 64-site chains (periodic and Dirichlet) and lapse-weighted measure.

### 5.4 First additional implication needed to transfer to the full theory

The gauge orbit (C1–C4) is established for the **unfiltered** radial potential. In the filtered MONO system the operative object is `S u` (`S = exp[(xi^2/2) Delta]`, gate `Delta Phi = 4 pi G rho_b + S* div[(nu_mono(|grad S u|/a0) - 1) grad S u]`), and the gauge question must be re-asked for the *filtered* gradient observables `grad S u` and `S* div[(nu_mono - 1) grad S u]`. Section G shows the boundary-condition sensitivity (`S·1 != 1` on Dirichlet domains) and measure-dependence of `S*` — so the filtered gauge orbit is **not** automatically the constant shift of the unfiltered one. The missing bridge: prove (or bound the failure of) `u -> u + K` and `r_ref`-shifts being inert on all filtered observables on the operative domain with the operative lapse, with `S` itself varied when the action is varied.

---

## 6. Execution record

- **Commands**: `python3 compute_AS018_gauge_audit.py` (cwd = this run dir; bounded inside the process: `RLIMIT_CPU = 120 s` enforced; `RLIMIT_AS = 512 MB` attempted, not enforceable on macOS — recorded verbatim in `residuals.json` meta; `OMP/OPENBLAS/MKL/NUMEXPR/VECLIB_MAXIMUM_THREADS = 1`); wall 0.362 s; peak RSS 96.5 MB (macOS `ru_maxrss` bytes = 101,203,968; byte-units probed empirically with an 80 MB allocation, see `rss_probe.py`); 1 thread; mpmath dps 60; largest array 65536 floats (no BLAS above 64x64 eigenchecks). Lean: `cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS018_reference_potential_certificates.lean` — exit 0.
- **Failed attempts (preserved)**: `compute_AS018_gauge_audit.py` v1 (superseded in-place): (i) `q_minus_pred_max_abs` tuple-unpacking bug; (ii) mpmath/float mixing in a max-abs normalization; (iii) scalar `math.erf` applied to arrays (fixed via `np.vectorize`); (iv) `np.trapezoid` absent in numpy 1.26.4 (→ `np.trapz`); (v) conceptually: y_p root-finder drifted to the inflection instead of the `h_RAR` peak; the deep-series check initially *expected* a slope 5/2 with odd powers, which the exact Bernoulli series falsified — the code's expectation was corrected to the actual math (slope 3, leading `y^3/30240`) and the discrepancy documented; (vi) Dirichlet eigencheck and grid-gauge checks mis-specified in v1 and re-specified. Lean: two compile-iteration rounds (method-arg-order of `HasDerivAt.comp`, instance alignment of `HasDerivAt.add`, set-integral lemma selection, `congr 1` for the energy-sum step) — all resolved; `probe.lean` records the API probes.
- **Artifacts**: this `derivation.md`, `result.json`, `compute_AS018_gauge_audit.py`, `raw_output.txt`, `residuals.json`, `AS018_reference_potential_certificates.lean`, `probe.lean`, `rss_probe.py`, `err.txt` (empty).

## 7. Limitations

- Numerical agreement is finite evidence; the grid checks are float64 consistency tests, not universal theorems (the Lean certificates cover only the exact algebraic layer: C1–C4 and the truncated inverse).
- The filtered-MONO gauge problem (with `S` varied) is **not** solved here; only its operator-behaviour foundations (boundary/measure sensitivity, adjoint identity) are exhibited.
- kappa = 1/2 remains an adopted input; no independent derivation of the normalization is attempted (contract's first-principles obligation: "The adopted one-half normalization is not a derived result unless an independent argument removes its freedom").
- `G_N = G_bare = G_cosmo = G` is *not* asserted; only the single `G` enters this calculation.
- Pointwise force differences between MONO and RAR (0.0104 dex max) do not transfer derivative, stability, or regularity statements — used here only as a labelled cross-check.
- The well-energy statement assumes `rho_b` fixed (no source back-reaction) and either decaying mass or an explicit box; dynamic or self-coupled sources are outside this result.
