# AS012 — Propagating correlated vacuum uncertainties

**Run:** `run_20260927T2240` · **Task:** `deepseek_push/astra_spawn_ideas/AS012_propagating_correlated_vacuum_uncertainties.md`
**Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter) subagent `sa-1-78020bd7` (Hermes Agent) · **Started:** 2026-09-27T22:40:00Z · **Finished:** 2026-09-27T23:06:12Z
**Cell:** CORE scale identities (group A01) — no kernel, no branch, no coupling is touched. `kappa = 1/2` is an **adopted input**, not a derived result. `G = G_N = 6.67430e-11` (measured Newton constant); `G_bare` and `G_cosmo` are distinct symbols that are **not used** here.

All numerics: `compute_AS012_covariance_propagation.py` (python3, conda base; numpy 1.26.4, mpmath 1.3.0), raw output `raw_output.txt`, residuals `residuals.json`. Lean 4 (v4.34.0-rc2) certificates: `AS012_covariance_certificates.lean` (compile log `lean_check.out`).

---

## 1. Precise claim, symbols, domain, assumptions

**Task equation (manifest):** `ln a0 = ln kappa + ln c + (ln G + ln rho_L)/2;  Var(ln a0) = J*Cov*J^T`.

**Symbol dictionary** (all SI; log-uncertainties are dimensionless):

| symbol | meaning | status |
|---|---|---|
| κ | coefficient of the vacuum scale | **adopted input**, κ = 1/2 (NOT derived; consistent with the recorded zero-mode no-go) |
| c | speed of light = 299792458 m/s | fixed input (exact) |
| G | Newtonian gravitational constant = 6.67430e-11 m³ kg⁻¹ s⁻² | measured input (= G_N; G_bare, G_cosmo distinct and unused) |
| ρ_L | vacuum mass density, kg/m³ | input (footing-dependent value, see §5) |
| a0 = κ c √(G ρ_L) | vacuum acceleration scale (framework base) | derived from the four inputs |
| M_b | baryonic mass | input of the derived scales (example: M_sun = 1.98847e30 kg) |
| r_M = √(G M_b/a0) | MOND radius (transition scale) | derived scale |
| v_flat⁴ = G M_b a0 | deep flat-speed law (exact framework identity) | derived scale |
| σ² = C/2, C = √(G M_b a0) | deep-equilibrium velocity scale | **conditional deep-equilibrium input/target** (this task propagates the identity, it does not derive equilibrium formation) |
| ρ_ph = C/(4πG r²), P = σ² ρ_ph | phantom density and pressure | same conditional status |
| J | Jacobian d ln a0 / d(ln κ, ln G, ln ρ_L) = (1, 1/2, 1/2) | derived |
| Σ | covariance matrix of (ln κ, ln G, ln ρ_L) | synthetic diagnostic input, declared PSD |

**Domain / boundary conditions:** ρ_L > 0, G > 0, κ > 0, M_b > 0, r > 0 (logs and square roots used). ρ_L → 0 makes ln ρ_L and a0 → 0: the log-space diagnostic is not defined at that boundary (stated, not hidden). No observational fit is performed anywhere in this run — every covariance entry and σ is a declared **synthetic** diagnostic input (σ_ln G is fixed at the CODATA-2018-style relative level 2.2e-5; σ_ln ρ_L = 2% and σ_ln κ = 5% are synthetic).

**Assumptions (explicit):**
1. the framework identity a0 = κ c √(G ρ_L) is the CORE scale relation (FRAMEWORK_CONTRACT "Mandatory scale and units"); κ = 1/2 adopted;
2. input log-uncertainties are described by a Gaussian law on (ln κ, ln G, ln ρ_L) with covariance Σ (synthetic model);
3. the conditional deep-equilibrium targets σ² = C/2, ρ_ph = C/(4πGr²), P = σ²ρ_ph are used **as identities to propagate**, with no equilibrium-formation claim (FRAMEWORK_CONTRACT: they are "conditional deep-equilibrium inputs/targets … need their own derivations");
4. M_b and r are held fixed in this run (their channels are written but set to zero; general formula given).

---

## 2. Derivation

### 2.1 Log-affineness and the exact variance

ln a0 is **affine** in the logs:

    ln a0 = ln κ + ln c + (1/2) ln G + (1/2) ln ρ_L .              (1)

For any random vector Y = (ln κ, ln G, ln ρ_L) with covariance Σ (finite second moments), an affine map is exact:

    Var(ln a0) = J Σ Jᵀ ,   J = (1, 1/2, 1/2).                     (2)

No small-uncertainty expansion is used at this level: (2) is an identity for *any* symmetric Σ, not an approximation. Writing Σ's entries as

        [ s_κ²         c_κG  c_κρ ]
    Σ = [ c_κG         s_G²  c_Gρ ]
        [ c_κρ         c_Gρ  s_ρ² ]

the quadratic form expands to the six-term formula (Lean-certified, `quad_form_expansion`):

    Var(ln a0) = s_κ² + (1/4)s_G² + (1/4)s_ρ² + c_κG + c_κρ + (1/2)c_Gρ .   (3)

The kappa–rho_L correlation the task asks for is the term `c_κρ` (coefficient 1); the G–ρ_L correlation enters with coefficient 1/2 (its power 1/2 in a0); the kappa–G term with coefficient 1.

### 2.2 Derived scales

From the framework definitions and (1):

    ln r_M   =         −(1/2) ln κ − (1/4) ln G − (1/4) ln ρ_L  + ½ ln M_b − ½ ln c
    ln v_flat= ln σ  =   (1/4) ln κ + (3/8) ln G + (1/8) ln ρ_L  + ¼ ln M_b + ¼ ln c
    ln P     =            (1) ln κ + (1/2) ln G + (1/2) ln ρ_L  + ln M_b − 2 ln r − ln(8π)
    (ln σ² = ln C − ln 2; ln C = ½ ln G + ½ ln M_b + ½ ln a0; ln ρ_ph = ln C − ln(4π) − ln G − 2 ln r)

**G-cancellation in P.** Substituting σ² = C/2 and ρ_ph = C/(4πGr²):

    P = (C/2) · C/(4πGr²) = C²/(8πGr²) = (G M_b a0)/(8π G r²) = M_b a0/(8π r²).   (4)

The explicit Newton constant G cancels **identically** (Lean-certified, `P_G_cancels`). Uncertainty content: at fixed (κ, ρ_L, M_b, r), P carries **no direct G dependence**; its log-sensitivity vector over (ln κ, ln G, ln ρ_L) equals J itself, so

    Var(ln P) = Var(ln a0)     (at fixed M_b, r).                                  (5)

(the pressure inherits the vacuum-scale variance 1:1; G's own variance enters only through its correlation with ρ_L via a0). Conversely the MOND radius and flat speed retain explicit G content (J_rM, J_v above).

### 2.3 Null directions: which covariance content matters

The map J has a 2-dimensional kernel: perturbations (u, v, w) of (ln κ, ln G, ln ρ_L) with

    u + v/2 + w/2 = 0                                                                 (6)

leave a0 **exactly** invariant (Lean-certified, `null_direction_invariance`:

    a0(κ e^u, G e^v, ρ e^w) = a0(κ, G, ρ)   for u + v/2 + w/2 = 0).

Consequences: (i) covariance mass in the null space of J contributes zero to Var(ln a0); the only relevant projection is the scalar JΣJᵀ; (ii) any change of variables that stays on the level sets of a0 (directions ⊥ J) cannot be an independent fitted input — this is the task's "same prediction in equivalent variables" made precise for the CORE scale cell. Note that r_M and v_flat depend on G beyond a0, so they *do* feel null-direction motion; only a0-functionals — e.g. P at fixed (M_b, r) — are null-direction invariant.

### 2.4 Leading neglected terms

- In log space there is **no neglected term**: (2) is exact (affine map).
- Conversion to linear-space bands uses the log-Gaussian law: the 1σ band of the log is ±σ_ln; the linear-space variance is Var(a0) = a0̄²(e^{s²}−1) = a0̄²s²(1 + s²/2 + O(s⁴)) with mean a0̄ e^{s²/2}. The leading correction to the linear treatment is relative **s²/2 ≈ 1.3e-3** at s ≈ 0.051 (0.13%), quoted for the declared model. Domain: any distribution with finite second log-moment; exact for lognormal.

---

## 3. Synthetic covariances and numbers

Synthetic log-sds: s_κ = 0.05 (adopted-κ uncertainty), s_G = 2.2e-5 (CODATA-2018-style G_N level), s_ρ = 0.02 (vacuum density).

- **Case A (uncorrelated):** c_κG = c_κρ = c_Gρ = 0.
  Var(ln a0) = 2.600000121e-3 → σ_ln a0 = 5.0990196e-2.
- **Case B (correlated, synthetic):** c_κG = +0.10·s_κ·s_G = 1.1e-7, c_κρ = −0.20·s_κ·s_ρ = −2.0e-4, c_Gρ = +0.35·s_G·s_ρ = 1.54e-7.
  Var(ln a0) = 2.400187121e-3 → σ_ln a0 = 4.8991705e-2.
  Term decomposition of (3): s_κ² 2.5e-3; ¼s_G² 1.21e-10; ¼s_ρ² 1.0e-4; c_κG +1.1e-7; c_κρ −2.0e-4; ½c_Gρ +7.7e-8. The κ–ρ_L correlation channel is the dominant cross term (−7.7% of the variance), exactly the term the task singles out. Both Σ matrices are verified PSD (eigenvalues ≥ 0; case A: (2.5e-3, 4e-4, 4.84e-10); case B: (2.519e-3, 3.811e-4, 4.10e-10)).

Derived log-variances (cases A / B): Var(ln r_M) = 6.5000e-4 / 6.0005e-4; Var(ln v_flat) = 1.625e-4 / 1.5004e-4; Var(ln σ) = identical to v_flat; Var(ln P) = 2.60000e-3 / 2.40019e-3 = Var(ln a0) exactly (G-cancellation, check residual 0.0 in float).

---

## 4. Independent checks (different representations)

All tolerances were set before evaluation (residuals.json). Actual residuals:

| check | method | observed | tolerance | pass |
|---|---|---|---|---|
| MC1 | 120,000-sample seeded lognormal Monte Carlo (seed 20260927) vs closed form Var(ln a0), cases A and B | rel. 3.78e-3 / 9.68e-4 (MC noise floor ~√(2/N) ≈ 4.1e-3) | 2e-2 | ✓ |
| MC2 | same samples vs Var(ln r_M), Var(ln v_flat), Var(ln σ), Var(ln P) | ≤ 3.8e-3 rel. | 2e-2 | ✓ |
| MC3 | full two-step evaluation P = σ²ρ_ph on every sample vs closed form M_b a0/(8πr²) | max |ln-residual| = 1.60e-14 | 1e-9 | ✓ (empirical confirmation of the G-cancellation) |
| MC4 | empirical covariance of the drawn samples vs declared Σ | max abs 6.51e-6 | 1e-4 | ✓ (sampler integrity) |
| FD | central-difference Jacobian of ln a0 vs analytic J = (1, ½, ½), h = 1e-5, both footings | ≤ 1.97e-10 | 1e-9 | ✓ |
| HP | mpmath 80-digit recomputation of Var(ln a0) case B | rel. 3.30e-16 | 1e-14 | ✓ |
| NC3 | quadratic-form homogeneity Var(f·Σ) = f²·Var(Σ), f = 0.5, 3, 7 | ≤ 2.36e-16 | 1e-12 | ✓ (exact identity: f² re-read from a scaled covariance matrix) |

Actual convergence/refinement: none needed (closed-form identities + one Monte Carlo pass; N fixed at 120,000, seed recorded).

---

## 5. Negative controls (capable of failing)

**NC1 — indefinite covariance (the task's named control).** Σ_ind with correlations (κG, κρ, Gρ) = (+0.95, +0.95, −0.95) at equal σ = 0.05 is not a covariance at all: eigenvalues (−2.250e-3, 4.875e-3, 4.875e-3), det = −5.35e-8. The run **detected the negative eigenvalue and refused to quote any σ_ln a0** (`sigma_refused: true`): a Gaussian with this Σ has a direction of *negative variance* (eigenvector of −2.25e-3), so JΣJᵀ is not a meaningful uncertainty even when the J-projection happens to be positive. The control is capable of failing: a PSD-checker bug (or quoting JΣJᵀ mechanically) would have produced a spurious "variance".

**NC2 — deep and Newtonian limiting regimes.** Log-derivatives of the speed law: Newtonian limit r ≪ r_M: d ln v/d ln a0 → 0 (v² = GM/r contains no a0 — exact), d ln v/d ln r = −1/2; deep regime r ≫ r_M: d ln v/d ln a0 = +1/4 (v_flat⁴ = GMa0, exact identity), d ln v/d ln r → 0. Evaluated by finite differences across r/r_M ∈ {1e-4 … 1e4} on both footings: deviations ≤ 2e-10 (raw_output.txt NC2_regimes; e.g. d ln v/d ln r = −0.50000000007 / d ln v/d ln a0 = 0.0 Newtonian, 0.24999999981 / 0.0 deep). Distinction recorded: v_flat⁴ = GMa0 and d ln v/d ln a0 = 1/4 are **exact identities** of the framework; the regime table is a finite consistency check.

**NC3 — normalization/homogeneity:** see table (exact identity, verified).

---

## 6. Node E: footings carried separately (mandatory)

Both registered footings at κ = 1/2, with G, c fixed:

| quantity | canonical (a0 = 9.3619e-11 m/s²) | alternative (a0 = 1.1279e-10 m/s²) |
|---|---|---|
| implied vacuum density | ρ_Lambda = 5.844412454e-27 kg/m³ | ρ_total = 8.483089620e-27 kg/m³ |
| r_M (M = M_sun) | 1.190640e15 m | 1.084744e15 m |
| v_flat | 333.866 m/s | 349.783 m/s |
| σ = v_flat/√2 | 236.079 m/s | 247.334 m/s |
| P at r = 1 kpc (example radius only) | 7.7793e-15 Pa | 9.3724e-15 Pa |
| ratio (a0_alt/a0_can)² = ρ_total/ρ_Lambda | 1.45148716 | (exact footing relation, cf. AS001) |

`Var(ln a0)` is **identical on the two footings** (same J, same Σ — log space does not know the central values). The linear-space 1σ bands are quoted per footing (case A): a0_can ± 4.774e-12 vs a0_alt ± 5.751e-12 m/s²; r_M ± 6.071e13 vs ± 5.531e13 m; v_flat ± 17.02 vs ± 17.84 m/s; P ± 3.97e-16 vs ± 4.78e-16 Pa. Case B bands: a0 ± 4.587e-12 / 5.526e-12 m/s², etc. (raw_output.txt `linear_bands`). No mixed-footing number is quoted anywhere.

---

## 7. Strongest surviving statement

> **Theorem (conditional, CORE scale cell).** With κ = 1/2 adopted, G = G_N = 6.67430e-11, c exact, Z = {κ, G, ρ_L} ⊂ ℝ₊₊, and any symmetric covariance Σ of (ln κ, ln G, ln ρ_L): (i) Var(ln a0) = JΣJᵀ exactly, J = (1, ½, ½), with the six-term expansion (3) — Lean-certified; (ii) the covariance content relevant to a0 is only the scalar JΣJᵀ: directions with u + v/2 + w/2 = 0 leave a0 exactly invariant — Lean-certified; (iii) for the conditional deep-equilibrium targets, P = M_b a0/(8πr²) — Lean-certified — hence Var(ln P) = Var(ln a0) at fixed (M_b, r) (no direct G channel); (iv) an indefinite Σ (negative eigenvalue) must not be interpreted as an uncertainty — run detects and refuses; (v) all numerical checks across cases A/B and both footings pass with residuals ≤ 3.8e-3 (MC), ≤ 2.0e-10 (FD), ≤ 3.3e-16 (mpmath 80-digit); the variance numbers of §3 are valid only for the declared synthetic (σ_κ, σ_ρ, correlations) — **no observational input was fitted**.

Domain: ρ_L, G, κ, M_b, r > 0; log-Gaussian synthetic model; exact statements (i)–(iii) hold for any joint law with finite second log-moments.

**What is not claimed:** no derivation of κ = 1/2 (adopted); no empirical covariance is certified (synthetic only); no equilibrium-formation claim for σ², ρ_ph, P; no transfer to the operative filtered-MONO target (Requirement 1) — no branch (Q, RAR, MU², EXP, MONO) is imported or translated.

---

## 8. Closure implication and next unresolved implication

- **Named gate:** Requirement 13 ("a0–vacuum relation preserved as input or genuinely derived"), ORCHESTRATOR gate-map cell A01 (this seed). This run supplies the uncertainty-propagation leg for the adopted input; the gate itself stays **open** (no dynamics anywhere).
- **Next unresolved implication:** the *physical* covariance to substitute for Σ — the measured joint distribution of (G_N, ρ_Lambda) including its correlation — cannot be derived inside the CORE scale cell: it requires the A03 (critical-density closure) / A11 (cosmological coupling) dynamics that tie the actual vacuum density entering the kernel to the action, plus the footing choice (canonical vs alternative). Until that exists, every quoted band is a synthetic template, not a measurement of a0's uncertainty.
- **Suggested follow-up:** child AS012.C01 (below) and, independently, the AS011 seed (footing as a separate hypothesis) with AS001 as its prerequisite.

## 9. Bounded execution record

Enforced: CPU soft limit 120 s via `resource.setrlimit(RLIMIT_CPU, (120, ∞))` (SIGXCPU kill by the OS); threads: 1 (single-threaded CPython/numpy; BLAS/OpenMP threads disabled via env); memory measured after run `ru_maxrss = 80,429,056` bytes ≈ 77 MiB on macOS (well inside the 512 MB target; no allocation cap set — macOS rejects a hard AS limit below the current infinite value, recorded). Wall time per run: 0.19–0.25 s. Monte Carlo: N = 120,000, seed 20260927, single pass. Initial prototype bound ≤ 120 s / ≤ 512 MB / 1 thread was respected and is recorded as actually enforced/modestly measured.

## 10. Sources and integrity

Pinned hashes (verified against SOURCE_MANIFEST.json: README 91a5fac4…, STANDING 660462eb…, FRIED_CHICKEN_SPEC 98d9149f…, DERIVATIONS 8da8176e…, task file 0f6d1859… matching the dispatcher's claim record `claims/AS012.json`): see `input_sha256` in result.json. The branch dictionary of FRAMEWORK_CONTRACT (Q, RAR, MU², EXP, MONO) is untouched by this run; no branch translation is performed or claimed.