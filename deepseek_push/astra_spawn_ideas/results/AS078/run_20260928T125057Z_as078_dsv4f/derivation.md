# AS078 — General slope normalizability

**Run:** `run_20260928T125057Z_as078_dsv4f` · **Seed SHA-256:**
`5530aaa93a14ff01c0333394d0baa2cc27f19746c44763177a5072a4227113e8`
**Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter), Hermes Agent
subagent `sa-0-46b402dc` · **Branch:** Conditional deep-equilibrium sector
(G084/G091/G233 equilibrium lane); no automatic particle ontology; κ = 1/2
ADOPTED as input; no Q/RAR/MU2/EXP/MONO kernel claim is made by this result.

---

## 1. The precise claim, symbol dictionary, boundary conditions

**Named claim under test (task Mathematics + first-principles obligation).**
For the power-law density family on the spherical shell
0 < r_in ≤ r ≤ R, R finite,

```
rho(r) = A r^(-gamma);   M = 4 pi A (R^(3-gamma) - r_in^(3-gamma)) / (3 - gamma),   gamma != 3,
```

the task asks whether "general slope normalizability" holds: which slopes γ
are normalizable, on which domains, and how the framework's γ = 2 isothermal
member is normalized.

**Symbols** (all SI unless stated).

| symbol | meaning | status |
|---|---|---|
| ρ(r) | mass density of the phantom/equilibrium sector, kg m⁻³ | derived object |
| A | amplitude, kg m^(γ-3) (fixes ρ(r_in) at unit radius) | normalization constant |
| γ | power-law slope (dimensionless) | derived exponent γ = C/σ² |
| r_in, R | shell boundaries, m; 0 < r_in < R < ∞ | boundary conditions, inputs |
| M_b | baryon mass, kg | input (proxy; both footings evaluated at 7.0e10 and 6.5e10 M_sun) |
| C | C = sqrt(G_N M_b a0) = v_flat², m² s⁻² | framework input (G091 V1) |
| r_M | r_M = sqrt(G_N M_b/a0), m | framework input (definition) |
| a0 | deep-acceleration scale, m s⁻² | framework input (two footings) |
| σ² | 1-D velocity dispersion squared | source result σ² = C/2 (G091 V2b, adopted as conditional input) |
| G_N | 6.67430e-11 m³ kg⁻¹ s⁻² (measured Newton constant) | input |
| κ | 1/2 adopted | input, not derived (framework contract) |

**Assumptions/premises** (all from the cited sources; none invented here):

1. Fixed baryon well Φ_b = C ln r on the shell (G084 §1, G091 V1), the
   deep-sector log-potential ansatz. Its status is *interior ansatz* (R ≤ r_M
   fixtures), per the task’s warning; it is **not** transferred to the deep
   exterior without a kernel check (§7).
2. Isothermal collisionless equilibrium with σ² = C/2 (G091 V2b: virial with
   the fluid closure, boundary term 3P_s V = σ²M_T).
3. Equipartition normalization M_ph(<r_M) = M_b (G03E/G091 V1a): the phantom
   mass inside r_M equals the baryon mass; with ρ = A/r² this fixes
   A = M_b/(4π(r_M − r_in)) exactly, and A → C/(4πG_N) as r_in → 0 (G03E
   limit).
4. G = G_N throughout. G_bare and G_cosmo do not appear in any relation of
   this cell; a0 = κc√(G ρ_Λ) is used only through its two registered
   numerical footings (κ = 1/2 adopted; ρ_Λ computed per footing below).

**Framework inputs vs conclusions.** Inputs: G_N, M_b, a0 (both footings),
κ = 1/2, the well, σ² = C/2, the shell (r_in, R). Conclusions to be
established: the closed-form enclosed mass for every real γ (γ = 3 by
continuous extension), the divergences as r_in → 0 and R → ∞, the γ = 3
limit value with its leading neglected term, the impossibility of global
(0, ∞) normalization, the exact finite-shell normalization identities at
γ = 2, and the boundary fixtures B(r_M) = g(r_M) = a0.

## 2. The finite-shell mass formula (derivation)

Density ρ(r) = A r^(−γ), shell volume element dV = 4πs² ds. Enclosed mass
between r_in and a radius r ≤ R:

```
M(r) = int_{r_in}^{r} 4 pi s^2 · A s^(-gamma) ds
     = 4 pi A int_{r_in}^{r} s^(2-gamma) ds.

gamma != 3:   M(r) = 4 pi A (r^(3-gamma) - r_in^(3-gamma)) / (3 - gamma).
gamma = 3:    M(r) = 4 pi A [ln(r) - ln(r_in)] = 4 pi A ln(r/r_in).
```

*Every factor, sign, unit, and the γ→3 step.* (i) The factor 4πA: solid
angle 4π × amplitude A (units: ρ = kg m⁻³ ⇒ A = kg m^(γ−3); with γ = 2,
A has units kg m⁻¹, i.e. mass per unit length — the standard isothermal
sphere amplitude). (ii) The exponent: s²·s^(−γ) = s^(2−γ); the integrand is
positive for A > 0, so the mass is strictly increasing — the sign of
M(r) − M(r_in) is positive. (iii) The antiderivative
s^(1−γ)… no: ∫s^(2−γ) ds = s^(3−γ)/(3−γ), valid as real rpow for s > 0,
γ ≠ 3; the boundary term at the lower edge: −r_in^(3−γ)/(3−γ). (iv) The
γ = 3 step: with δ := 3 − γ ≠ 0 the 0/0 form
(1/δ)(r^δ − r_in^δ) has the removal identity

```
r^δ = exp(δ ln r) = 1 + δ ln r + (δ²/2)(ln r)² + O(δ³),
(r^δ - r_in^δ)/δ = ln r - ln r_in + (δ/2)[(ln r)² - (ln r_in)²] + O(δ²)
                -> ln(r/r_in) as delta -> 0.
```

So the γ = 3 enclosed mass is the *continuous extension*
M(r) = 4πA ln(r/r_in), and the leading neglected term of the γ → 3
limiting regime is + (δ/2)·[(ln r)² − (ln r_in)²], δ = 3 − γ — verified
numerically to 1e-20 (§5.2) and certified in Lean (γ→3 limit,
leading-coefficient check §5.2). Physical check: at γ = 3 the shell mass is
finite for every finite shell and diverges only as an endpoint logs →
∞; the extension is the unique continuous completion.

Mass positivity/normalization at finite boundaries: for any real γ ≠ 3 the
shell mass is finite and positive for finite r_in, R; solving for the
amplitude at fixed shell mass,

```
A(gamma) = M_b (3 - gamma) / [4 pi (R^(3-gamma) - r_in^(3-gamma))]  > 0  for ALL gamma != 3,
A(3)     = M_b / [4 pi ln(R/r_in)]                                     > 0,
```

because numerator and denominator have the same sign for all γ ≠ 3. Hence
**every slope is exactly normalizable on a finite shell** — this is the
surviving content of "general slope normalizability", and the divergence
structure below is precisely what restricts the untruncated problem.

## 3. The γ→3 limit and the divergence classification

**γ → 3.** (R^δ − r_in^δ)/δ → ln(R/r_in); the naive 0/0 evaluation of
(R^(3−γ) − r_in^(3−γ))/(3−γ) at γ = 3 is singular (ZeroDivision),
the continuous extension is the log form. Verified: 50-digit δ-sequence
δ = 10⁻¹…10⁻²¹, residual ∝ δ with the predicted coefficient; residual at
δ = 1e-20: 1.63e-20, at 1e-21: 1.63e-21 (rel resid 1.6e-50 scale vs the
limit — 50-digit clean; table in `as078_residuals.json` `gamma3_limit`).

**Divergences.**

| integral | behaviour as r_in → 0 (inner end) | behaviour as R → ∞ (outer end) |
|---|---|---|
| γ < 3 | converges | diverges ∝ R^(3−γ) |
| γ = 3 | log-diverges (ln R − ln r_in → ∞) | log-diverges |
| γ > 3 | diverges ∝ r_in^(3−γ) | converges |

Necessary and sufficient conditions: inner integrability of s^(2−γ) at 0
requires 2 − γ > −1 i.e. **γ < 3**; outer integrability at ∞ requires
2 − γ < −1 i.e. **γ > 3**. The conditions are disjoint: **no real γ renders
the power law normalizable on (0, ∞)** (Lean-certified.
`no_gamma_both_ends`).

**Why the untruncated γ = 2 halo has infinite mass.** At γ = 2 the inner
end is integrable (M(ε) → finite), but the outer end grows linearly:
M(R) = 4πA(R − r_in) → ∞ as R → ∞ (M(R)/R → 4πA ≠ 0; M(2R)/M(R) → 2).
The γ = 3 member diverges logarithmically at *both* ends. Any claim of an
untruncated isothermal halo therefore requires an outer fixture — the
framework’s equipartition cap at r_M (below) is exactly such a fixture, and
it is what makes the *truncated* equilibrium normalizable.

## 4. The framework’s γ = 2 member: exact finite-shell identities

Framework amplitude A = C/(4πG_N), A·r_M relationship. At γ = 2, using
A = C/(4πG_N) (the r_in → 0 limit of equipartition; G03E), the *exact*
identities (all verified numerically on both footings and both mass proxies;
Lean-certified: `equipartition_mass` for the algebra 4πA·r_M = M_b):

```
M_ph(<r)       = 4 pi A (r - r_in)                [finite-shell, exact]
M_ph(<r_M)     = M_b                                [equipartition, exact]
M_ph(<r)/M_b   = (r - r_in)/(r_M - r_in)            [fraction, exact]
v_c²(r)        = G_N M_ph(<r)/r = (G_N M_b/r)(r - r_in)/(r_M - r_in)
v_c²(r_M)      = C  EXACTLY for any r_in;  v_c²(r) = C  IDENTICALLY ON THE SHELL only as r_in -> 0.
```

The flat deep curve v_c² ≡ C is the r_in → 0 (point-like baryon core) limit
— with a finite inner boundary the circular speed deviates from C:
v_c²(0.62 r_M)/C = 0.9938, 0.9319, 0.3871 at r_in/R = 0.01, 0.1, 0.5
(respectively, fixture R = r_M). The finite-boundary amplitude correction is
A_ex/A_lim − 1 = r_in/(r_M − r_in) = +1.010e-2 at r_in/R = 0.01. These are
the "finite boundaries explicit" statements the task demands; they are
recorded, not smoothed away.

Boundary fixtures where the deep sector meets the Newtonian field (exact,
both footings, both proxies verified to 1e-12):

```
B(r_M) = G_N M_b / r_M² = a0        (definition fixture)
g(r_M) = C / r_M        = a0        (deep-sector equipartition boundary)
rho(r_M) = C/(4 pi G_N r_M²);  P(r_M) = sigma² rho(r_M) = a0²/(8 pi G_N)   (G233 identity, re-verified to 2e-16)
```

Newtonian-regime statement (where the check exists): in this cell the
Newtonian well is Φ_b = −G_N M_b/r (G091's inner-edge bookkeeping, r < r_b);
there the Boltzmann factor exp(−βΦ_b) is exponential in 1/r, not a power
law, so **the power-law family has no Newtonian-regime member within this
declared cell** — the family is a deep-sector object. Consistency check at
small radii: M_ph(<r)/M_b = (r − r_in)/(r_M − r_in) = 1.0000e-2 at
r/r_M = 0.01 (r_in → 0): the phantom mass fraction is small in the
near-Newtonian interior — no conflict with the baryon-dominated region.

## 5. Computation and independent checks (actual residuals)

Prototype `as078_slope_normalizability.py`; bounds *enforced and measured*:
wall 0.143 s (limit 120 s), max RSS 45.1 MB (limit 512 MB), 1 thread
(OMP/OPENBLAS/MKL pinned to 1; no vectorized parallelism), ≤ 512 grid cells
(trapezoid n = 128 → 256 → 512, two refinements), mpmath mp.dps = 50.
All residuals are actual, saved in `as078_residuals.json`.

1. **Closed form vs independent quadrature** (different representation:
   direct tanh-sinh integration of the defining integral vs the closed
   form), dimensionless identity ∫u^(2−γ)du = (u2^(3−γ) − u1^(3−γ))/(3−γ),
   γ ∈ {0.5, 1, 1.5, 2, 2.5, 2.9, 3(log), 3.1, 4} × 6 interior shells
   ((r_in/R, R/r_M) ∈ {(0.01,0.62),(0.01,1),(0.1,0.62),(0.1,1),(0.5,0.62),
   (0.5,1)}) × both footings: **worst relative residual 1.78e-50**
   (tolerance set before evaluation: 1e-40 → PASS on every cell). Physical
   scaling consistency (float inputs): ≤ 1.98e-15, informational.
2. **γ → 3 limit and its leading neglected term:** δ-sequence with the
   exact decimal endpoints u1 = 0.062, u2 = 0.62; deviation from the log
   limit equals (δ/2)[(ln u2)² − (ln u1)²] at every decades — δ shown:
   1e-4 → dev 3.75e-4, 1e-10 → 3.75e-10, 1e-20 → 3.75e-20 (leading term
   matched to the printed digits). This is the *leading neglected term* of
   the γ → 3 limiting regime, domain δ ∈ (0, 1).
3. **Independent representation — FTC differentiation:** d/dR M(R) computed
   by mpmath Richardson differentiation of the closed form vs the surface
   term 4πA·R^(2−γ) = 4πR²ρ(R): relative residuals 5.6e-17 … 7.4e-41
   (γ ∈ {1.5, 2, 2.5}, both footings) — i.e., the closed form is the
   antiderivative of the flux with M(r_in) = 0 (boundary condition, exact:
   `mass_at_inner_edge`), which is what makes it *the* enclosed mass.
4. **Finite-grid consistency:** log-trapezoid n = 128/256/512,
   γ = 2, residual ≤ 1.8e-16 relative (float64-limited — a finite numerical
   consistency check, *not* an identity; exactness is carried by 1. and by
   the Lean certificate).

## 6. Negative controls (all capable of failing; the task's three controls)

- **NC1 — global normalization of r^−2 on all positive radii: REFUTED.**
  M(R) = 4πA(R − r_in) grows without bound: M(10^k r_M)/M(10^(k−1) r_M) =
  10 exactly (ratio trend 2.001001 → 2.00000001 for M(2R)/M(R) at
  R = 10^6 r_M): the untruncated γ = 2 halo has infinite mass. The control
  fires (would *fail* if the untruncated integral were finite).
- **NC2 — naive 0/0 evaluation at γ = 3: REFUTED/SINGULAR.**
  (R^(3−γ) − r_in^(3−γ))/(3−γ) at γ = 3 raises ZeroDivisionError; the
  continuous extension 4πA·ln(R/r_in) = 2.0349e21 kg on the fixture — the
  log form is the limit of the δ-sequence (§5.2) and the Lean-certified
  limit (γ→3). Exact identity (limit) vs finite numerical check
  (δ-sequence agreement) distinguished explicitly.
- **NC3 — flatness for any finite r_in: REFUTED.** v_c²(0.62 r_M)/C =
  0.9938/0.9319/0.3871 for r_in/R = 0.01/0.1/0.5; the deep flat identity
  v_c² ≡ C holds only in the r_in → 0 limit (and exactly at r_M). The
  control fires.
- **NC4 (task step 5) — interior ansatz transferred to the deep exterior:
  NOT ESTABLISHED (open dependency, not repaired by any import).** Under
  the extrapolated γ = 2 ansatz with the interior normalization, the shell
  mass in the deep exterior (r_in/r_M = 10, 100; R/r_in = 2, 10) is
  exactly M_shell/M_b = (R − r_in)/r_M = 10, 90, 100, 900 — growing ∝ R,
  both footings identical (dimensionless). The interior equipartition
  normalization therefore does **not** control the phantom mass at
  r ≫ r_M. Whether filtered MONO actually generates ρ ∝ C/(4πG r²) outside
  r_M is a kernel question: it requires the point-source MONO solve with
  the heat filter (catalog seed AS044 is the natural prerequisite) — an
  explicit open dependency of this result, per the task's warning
  "Do not transfer an interior ansatz to filtered MONO without that check."
  The check is not performed here and no branch is imported to fake it.

## 7. Strongest surviving statement (domain, conditions)

**Theorem (conditional, this run).** In the declared conditional
deep-equilibrium cell — fixed log well Φ = C ln r, σ² = C/2 (G091 V2b,
conditional), equipartition M_ph(<r_M) = M_b, G = G_N, κ = 1/2 adopted, both
registered footings — on every finite shell 0 < r_in < R < ∞:

(i) every member of the family ρ = A r^(−γ), γ ∈ ℝ, is exactly normalizable
with the closed form M(r) = 4πA(r^(3−γ) − r_in^(3−γ))/(3−γ) (γ ≠ 3), γ = 3
given by the 4πA ln(r/r_in) extension, whose leading neglected term at
γ = 3 ± δ is (δ/2)[(ln r)² − (ln r_in)²] (all residuals ≤ 1.8e-50, Lean-
certified identities `mass_closed_form`, `mass_at_inner_edge`, γ→3 limit
theorems);

(ii) global normalization on (0, ∞) fails for **every** γ: inner end needs
γ < 3, outer end needs γ > 3 (γ = 3: log-divergent at both ends; γ = 2:
outward-linear divergence M ∝ 4πA R) — hence the framework's
ρ_ph = C/(4πG r²) is a *finite-domain* equilibrium profile whose amplitude
is fixed by boundary/equipartition data, not by any property of the
untruncated problem (Lean: `gamma2_outer_unbounded`, `gamma3_outer_diverges`,
`gamma3_inner_diverges`, `horn_gamma_lt_3`, `horn_gamma_gt_3`,
`no_gamma_both_ends`);

(iii) at γ = 2 with A = C/(4πG): M_ph(<r_M) = M_b exactly, v_c²(r_M) = C
exactly for any r_in, and v_c² ≡ C on the shell exactly in the r_in → 0
limit only (finite-r_in deviations recorded, §4); B(r_M) = g(r_M) = a0 and
P(r_M) = a0²/(8πG) on both footings (Lean: `equipartition_mass`).

**Domain:** γ ∈ {0.5, 1.0, 1.5, 2.0, 2.5, 2.9, 3.0, 3.1, 4.0} × interior
shells (r_in/R ∈ {0.01, 0.1, 0.5}, R/r_M ∈ {0.62, 1.0}) × {canonical,
alternative footing} × M_b ∈ {7.0e10, 6.5e10} M_sun (proxies) on the
numerical side; all real γ, all 0 < r_in < R on the Lean/algebraic side
(γ ≠ 3 for the closed form, γ = 3 by limit). No fit: the diagnostics
r_in/R = 0.01/0.1/0.5 and R/r_M = 0.62/1 are the task's fixture values,
not parameters.

**Both footings reconciled:** every statement of (i)–(iii) except the
dimensional amplitude values is a dimensionless identity holding for both
a0 values; the dimensional numbers (A, C, r_M, v_flat, ρ_Λ, masses) are
reported separately for canonical a0 = 9.3619e-11 and alternative
a0 = 1.1279e-10 m/s² in §8; the two footings cannot share fixed
(κ, ρ_Λ): ρ_Λ = 5.844412e-27 (canonical) vs 8.483090e-27 (alt) kg/m³ at
κ = 1/2; at fixed canonical ρ_Λ the alternative a0 implies κ_eff =
0.6023884 (≠ 1/2).

## 8. Dimensional examples — both footings (M_b = 7.0e10 M_sun)

| quantity | canonical | alternative |
|---|---|---|
| a0 (m/s²) | 9.3619e-11 | 1.1279e-10 |
| ρ_Λ = 4a0²/(Gc²) (kg/m³) | 5.844412e-27 | 8.483090e-27 |
| C = (G_N M_b a0)^(1/2) (m²/s²) | 2.9501e10 | 3.2371e10 |
| v_flat = C^(1/2) (m/s) | 1.71730e5 | 1.79917e5 |
| σ = (C/2)^(1/2) (km/s) | 121.43 | 127.22 |
| r_M (m) | 3.1501e20 | 2.8700e20 |
| A = C/(4πG_N) (kg/m) | 3.5180e19 | 3.8600e19 |
| ρ(r_M) (kg/m³) | 3.5458e-22 | 4.6872e-22 |
| P(r_M) = a0²/(8πG) (Pa) | 5.4868e-13 | 7.9607e-13 |

(Anchors: at M_b = 6.5e10 M_sun the virial temperature reproduces the
registered σ = 119.20 / 124.89 km/s for the two footings ✓ — G091's anchor
values; the 7.0e10-proxy numbers above are the G084/G233 lane convention.)

All dimensional numbers are *proxies*, not fits: the theorem does not depend
on M_b.

## 9. Lean certificate (algebraic core)

`AS078_general_slope.lean` (12 theorems, Mathlib v4.34.0-rc2):
`mass_closed_form`, `mass_at_inner_edge` (closed form + boundary pinning),
`slope_rpow_at_zero`, `gamma3_limit`, `gamma3_limit_log_ratio` (γ → 3),
`gamma2_outer_unbounded`, `gamma3_outer_diverges`, `gamma3_inner_diverges`
(untruncated unboundedness), `horn_gamma_lt_3`, `horn_gamma_gt_3`
(classification horns), `no_gamma_both_ends` (no global normalization),
`equipartition_mass` (4πA r_M = M_b). Compilation: `lake env lean
<abs path>/AS078_general_slope.lean` from `fable_independent_2026/lean_2026`
— exit 0, zero `sorry` (grep count 0 outside the header comment),
unfiltered `#print axioms` for all 12 theorems =
`[propext, Classical.choice, Quot.sound]` (captured in `lean_check.out`).
House rules followed: no file written into `fable_independent_2026/lean_2026`
(compile host only); `Tendsto.congr'` used with the eventual-equality
argument first; no trailing tactic after a closing `field_simp`/`rw`;
`mul_left_cancel`-type reasoning avoided in favor of divisions guarded by
the explicit γ ≠ 3 / positivity hypotheses.

## 10. What this result does and does not establish; next implication

**Establishes (scoped, unreviewed):** the complete normalizability/
divergence classification of the power-law equilibrium family of the
deep-equilibrium sector, with exact finite-shell mass formulas, the γ = 3
limit with its leading term, exact two-footing normalization identities at
γ = 2, and four failing controls — including the explicit nonexistence of
global r^−2 normalization and the explicit non-transfer of the interior
ansatz to the deep exterior.

**Does not establish:** (a) that filtered MONO's actual point-source
solution produces ρ ∝ r^−2 at r > r_M (kernel solve open — the exterior
error bound is the first missing bridge; dependency: deep point-source
potential and boundary matching, catalog seed AS044); (b) κ = 1/2 (adopted);
(c) any dynamics/attainment (formation of the equilibrium, G035's kill
stands; max-entropy stationarity ≠ dynamical attractor, G084 status (iii));
(d) the common-action witness (no action is varied in this run; gate 12
(RAR segment/MONO continuation) is *affected* only via the profile
normalization leg, whose exterior transfer is precisely the open item (a)).

**First additional implication needed to transfer to the full theory:**
bound the error of the interior r^−2 ansatz against the filtered-MONO
point-source kernel on the exterior shells r_in/r_M = 10, 100 (R/r_in = 2,
10) — i.e., compute the actual phantom density profile of the operative
kernel at r ≫ r_M (using the AS044 deep point-source solve) and compare
its shell-mass normalization with M_b(R − r_in)/r_M (NC4's ansatz value).
Until that error bound exists, no statement of this run licenses an
outer-halo mass assignment under the amended thirteen-item target.

## 11. Run bounds, provenance, outputs

- Bounds (declared ≤ 120 s / ≤ 512 MB / 1 thread; enforced and measured):
  wall 0.143 s (python wall from `time`), max RSS 45.1 MB (both
  `resource.getrusage` and `/usr/bin/time -l`), 1 CPU thread (env-pinned),
  mpmath dps = 50, ≤ 512 grid cells, 2 refinements; Lean: single
  `lake env lean` invocation (Mathlib cached; compile ~15 s within the tool
  ceiling).
- Source hashes verified against SOURCE_MANIFEST.json before execution:
  G084 `752999fd…`; G091 `8164360f…`; G233 `ad89298d…` (all match pins
  exactly). Seed SHA-256 recorded in result.json (task_sha256).
- Outputs of this run (run dir
  `deepseek_push/astra_spawn_ideas/results/AS078/run_20260928T125057Z_as078_dsv4f/`):
  this file, `as078_slope_normalizability.py`, `raw_output.txt`,
  `as078_residuals.json`, `err_and_time.txt`, `AS078_general_slope.lean`,
  `AS078_axioms.lean`, `lean_check.out`; all content-addressed in
  result.json `artifacts_sha256` (result.json itself excluded per the
  contract).