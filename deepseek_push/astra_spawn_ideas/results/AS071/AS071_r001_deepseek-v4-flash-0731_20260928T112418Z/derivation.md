# AS071 — Physical response versus probability interpretation: bounded audit

**Run:** `AS071_r001_deepseek-v4-flash-0731_20260928T112418Z`
**Worker:** hermes-agent subagent; model `deepseek/deepseek-v4-flash-0731` (openrouter) · **Started:** 2026-09-28T11:24:18Z · **Finished:** 2026-09-28T12:01:25Z
**Task sha256:** `402a14ba05050e9c166a23ade404073f3dc6d781ad530eaaba72113fbd098178` (verified equal to the dispatched seed on disk; the seed was executed as-is, nothing renamed or paraphrased)
**Group A03 (coefficient mechanisms and their missing premises) · Kind: audit · Branch: CORE coefficient; conditional MU_n statistical response**

---

## 1. Sources inspected and their pinned hashes (all match SOURCE_MANIFEST.json)

| source | sha256 | status |
|---|---|---|
| `deepseek_push/PD01_polarization_count.py` | `37e39d1abb…c74d` | matches pin exactly |
| `deepseek_push/PD08_particle_free_derivation.py` | `83f6054cdfb…f0cfb` | matches pin exactly |
| `kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py` | `8df5a3ab5a…25c` | matches pin exactly |
| `STANDING.md`, `FRIED_CHICKEN_SPEC.md` (Sept-26 amendment block), `FRAMEWORK_CONTRACT.md` | `660462ebe8…63`, `98d9149fce…3f`, `ca696c7fe7…df9` | read in order required by the contract |

The operative target is **filtered ν_mono with causality criterion B** (September 26 amendment). This task's branch is the **CORE coefficient via conditional MU_n statistical response**; every conclusion below is restricted to that branch and is a *conditional lemma or counterexample relative to that branch*. No conclusion here is transferred to Q, RAR, MU2-in-the-operator-sense, EXP, or MONO.

## 2. The precise claim under audit, symbol dictionary, boundary conditions, assumptions

**Claim (seed's "Mathematics and principal test").** For the candidate kappa-derivation route PD01/PD08 the response function of the quasi-linear Poisson equation is read as a probability:

```
div(mu(|grad Phi|/s) grad Phi) = 4 pi G rho_b          (field equation, spherical reduction: mu(g) g = g_N)
mu(Y) = 1 - (1 - p(Y))^n                                (OR over n equal, independent channels)
p : per-channel engagement;   Y = g/s ;  s = c sqrt(G rho_Lambda) ;  kappa = a0/s = 1/n
```

The audited assertion: *"mu(Y) = CDF(Y) ensures 0 ≤ mu ≤ 1; it does not specify what sample space maps to gravitational response."* The audit decides whether the CDF/probability reading supplies a map from a positive measure to the acceleration flux, i.e. whether it is a physical response at all, and whether it can carry the kappa = 1/2 derivation.

**Symbol dictionary (framework inputs first).**

| symbol | meaning | value/units |
|---|---|---|
| a0 | the MOND acceleration scale | 9.3619e-11 m s⁻² (canonical) **or** 1.1279e-10 m s⁻² (alternative); **kappa = 1/2 ADOPTED** (task input, not derived) |
| κ | a0/(c√(G ρ_Λ)) | 1/2 adopted; effective 0.602388 if ρ_Λ held at canonical and a0 = alternative (see §7) |
| ρ_Λ | vacuum mass density, 4 a0²/(G c²) | 5.84441e-27 kg m⁻³ (canonical), 8.48309e-27 kg m⁻³ (alternative) |
| s | c√(G ρ_Λ) = 2 a0 exactly on the adopted footing | 1.87238e-10 m s⁻² (canonical), 2.2558e-10 m s⁻² (alternative) |
| Y | g/s, dimensionless drive | positive finite |
| g, g_N | total radial acceleration; Newtonian baryonic | m s⁻² |
| B | g_N (branch-dictionary notation) | m s⁻² |
| mu_n | 1 − (1+Y)⁻ⁿ, the corpus family = OR class with p = Y/(1+Y) | dimensionless |
| p | per-channel engagement function | dimensionless, CDF-like (see below) |
| n | channel count, ℕ, n ≥ 1 in this audit (n = 2 metric count in the candidates) | dimensionless |
| r_M | √(G M_b/a0) | 1.19064e15 m (M = M_sun, canonical); 1.08474e15 m (alternative) |
| v_flat | (G M_b a0)^(1/4) | 0.333866 km/s (canonical, M_sun); 0.349783 km/s (alternative) |
| G_N | measured Newton constant 6.67430e-11 m³ kg⁻¹ s⁻² (used here; G_bare, G_cosmo kept as separate symbols, no relation asserted) |
| c | 299792458 m/s ; M_sun 1.98847e30 kg ; pc 3.085677581491367e16 m |

**Boundary conditions on the response** (framework requirements 9 and 10): μ(0) = 0 (controlled zero-field limit), μ(∞) = 1 (Newtonian recovery). CDF-structure adds 0 ≤ μ ≤ 1 and monotonicity — all satisfied by the corpus family.

**Assumptions and their status.** (i) OR composition of equal independent binary channels — *assumed semantics* (PD01); (ii) p(0) = 0, p(∞) = 1 — boundary conditions, also physical limits; (iii) p′(0) = 1 ("fraction identity", L230) — *independent premise* (one-scale argument); (iv) n = 2 from "two Poisson channels of the linearized metric" — *physical computation*, but its identification with two probability channels is L237's unresolved two-readings item; (v) kappa = 1/2 — *adopted input* for this task. Conclusions to be established: none of these is removed by the CDF property.

## 3. The map from a positive measure to the acceleration flux

Let the response be the random variable ξ(Y) ∈ {0,1} of a channel-engagement law with marginal P(ξ(Y)=1) = p(Y). The field equation uses μ(Y) = 1 − (1 − E[ξ(Y)])ⁿ, i.e. **first moments only**:

```
flux(Y) = E[response] · Y · s         (the operator div(mu grad Phi) reads the mean of the response)
```

Any two laws with the same marginals (same p(Y), hence same μ(Y)) give the **identical** quasi-linear operator. The joint law — the covariance kernel K(Y₁,Y₂) = Cov[ξ(Y₁),ξ(Y₂)] and higher cumulants — is unconstrained. **Exact missing datum:** the joint law (equivalently the generator/transition law) of the channel process; the CDF fixes only the marginal. No dynamics in the static action sector can supply it: k01 K1/K2 prove for the candidate action class that the static Euler–Lagrange equations contain the kinetic function J only through J′, and that at Y = 0 the constant enters only as Λ_eff = Λ + (2−K_B)J(0)/2 + K(Q₀)/2 — with Λ explicit and free, no equation of that action relates a0 to Λ ("outcome 3" of k01). Consistent with this audit: the sample space is a free datum of the probability reading.

**One testable consequence beyond matching the CDF.** If the response were realized by N independent fluctuation cells per aperture, the ensemble dispersion of the measured response would be σ_μ = √(μ(1−μ)/N); via the spherical reduction g = g_N/μ,

```
sigma_g/g_N = sqrt(mu(1-mu)/N) / mu^2        (stochastic N-cell reading)
            = 0                               (deterministic reading; predicted shot noise zero, PD01)
```

Numerical values at the metric count n = 2, Y = 1 (μ = 3/4): σ_g/g_N = 0.7698 (N=1), 0.2434 (N=10), 7.698e-3 (N=10⁴) vs **exactly 0** for the deterministic response. This observable is not producible from the CDF; no empirical verdict is claimed here — it is the derived discriminating quantity.

## 4. The mathematics: intermediate algebra, signs, units, leading neglected terms

### 4.1 OR-class slope identity (exact, every completion; Lean-certified, §9)

For any completion p with p(0) = 0, p′(0) = 1 and any n ∈ ℕ:

```
d/dY [ 1 - (1 - p(Y))^n ]|_{Y=0} = n (1 - p(0))^(n-1) p'(0) = n
```

Chain rule: with w = 1 − p, μ = 1 − wⁿ, μ′ = −n wⁿ⁻¹ w′ = n (1−p)ⁿ⁻¹ p′ → n at Y = 0. **The slope equals the channel count for every completion** (PD01 A1 re-derived; σ_μ independence from the completion's quadratic coefficient, PD08 STEP 4). The slope is therefore NOT a CDF property: the CDF axioms are satisfied by the whole family {μ_m : m ∈ ℕ} with slopes m = 1, 2, 3, … (Lean: `corpus_slope_one`, `corpus_slope_two`). CDF-ness cannot fix the slope; the slope is carried by (i) the OR composition, (iii) p′(0) = 1, (iv) the count n.

### 4.2 Corpus family: exact expansion and both limiting regimes

```
mu_n(Y) = 1 - (1+Y)^(-n) = 1 - (1/(1+Y))^n
        = nY - n(n+1)Y^2/2 + n(n+1)(n+2)Y^3/6 - ...   (|Y| < 1; exact coefficients
          c_k = (-1)^(k+1) C(n+k-1, k), verified to order 6, |diff| = 0)
```

**Deep regime (Y → 0):** μ_n = nY − n(n+1)Y²/2 + O(Y³), leading neglected term −n(n+1)Y²/2, **domain |Y| < 1**. Spherical matching μ(g) g = g_N with μ ≈ n g/s:

```
n g^2 / s = g_N  =>  g^2 = (s/n) g_N = a0 g_N,   a0 = s/n = kappa s,   kappa = 1/n
```

The transfer is asymptotic, not exact. Exact spherical solution Y* of Y μ_n(Y) = D (D = g_N/s) expanded in Y_dm = √(D/n) (perturbation of nY²[1 − (n+1)Y/2 + (n+1)(n+2)Y²/6 − …] = D):

```
Y*/Y_dm = 1 + a1 Y_dm + a2 Y_dm^2 + ...
a1 = (n+1)/4,   a2 = (n+1)(7n-1)/96          (second coefficient derived here)
```

Numerics (mpmath, 50 digits; threshold set before evaluation):
- n = 1, D = 0.01: |(Y*/Y_dm − 1) − a1Y_dm| = 1.24922e-3, a2Y_dm² = 1.25e-3 → PASS (|rel − lead| < 2·a2Y_dm²).
- n = 2, D = 0.01: 2.08e-3 vs 2.03e-3 → PASS; n = 3, D = 0.01: 2.87493e-3 vs 2.77778e-3 → PASS; all six (n, D) pairs PASS.
- Residual at finite D is real: rel ∈ [5.0e-3, 6.1e-2] > 0 (DM2): **the deep law is a limiting identity, not exact at finite D** — quantified, not boolean.

**Newtonian regime (Y → ∞):** μ_n = 1 − Y⁻ⁿ + nY⁻ⁿ⁻¹ − n(n+1)Y⁻ⁿ⁻²/2 + …; leading deficit Y⁻ⁿ, next term −nY⁻ⁿ⁻¹, **domain Y ≫ 1**. Checks at Y = 1e2, 1e4 for n = 1,2,3: |(1−μ) − (Y⁻ⁿ − nY⁻ⁿ⁻¹)| bounded by the (n(n+1)/2)Y⁻ⁿ⁻² term (all six PASS, residual/ratio in [0.98, 1.0]).

### 4.3 Both footings (framework requirement; carried separately, never jointly)

| quantity | canonical a0 = 9.3619e-11 | alternative a0 = 1.1279e-10 |
|---|---|---|
| ρ_Λ = 4a0²/(G c²) | 5.84441e-27 kg m⁻³ | 8.48309e-27 kg m⁻³ (ratio 1.45149 = (a0_a/a0_c)²) |
| s = c√(Gρ_Λ) = 2a0 | 1.87238e-10 m s⁻² | 2.2558e-10 m s⁻² |
| κ (adopted input) | 1/2 | 1/2 |
| κ_eff if ρ_Λ fixed at canonical | — | **0.602388** (≠ 1/2) |
| r_M(M_sun) | 1.19064e15 m | 1.08474e15 m |
| v_flat(M_sun) | 0.333866 km/s | 0.349783 km/s |

F1: |s − 2a0| = 0 to 50 digits (exact algebraic identity, residual only). F2: κ = 1/2 on both footings with their own densities. F3: the footings cannot share both fixed ρ_Λ and fixed κ; the alternative footing at fixed canonical density forces κ_eff = 0.602388 ≠ 1/2 — stated as the seed demands. The dimensionless theorems of §4.1–4.2 are proved once and apply to both footings through the single dimensionless variable Y = g/s (s footing-specific); all dimensional examples are carried separately.

## 5. Step 2's required map, and the negative control (must be capable of failing)

**Step 2 deliverable:** the map from measure to flux is `flux(Y) = E[response at Y]·Y·s` — first moment only; the missing equation is the joint law of the channel process (covariance kernel/generator). If no dynamics supplies it (and k01 K1/K2 show the candidate action class cannot), the exact missing statement is: *the law of (ξ(Y))_{Y>0} as a stochastic process, i.e. its finite-dimensional joint distributions, constrained by the action* — nothing in the action pins them.

**Negative control — the seed's required control:** assign two different underlying measures with identical CDF shape but different fluctuation spectra:

- **Measure A (deterministic):** ξ(Y) = 1{U ≤ p(Y)} for one global U ~ Uni(0,1). Perfectly reproducible; Cov_A(Y₁,Y₂) = min(p₁,p₂) − p₁p₂.
- **Measure B (independent):** ξ(Y) ~ Ber(p(Y)) i.i.d. per Y. Cov_B(Y₁,Y₂) = 0 for Y₁ ≠ Y₂.
- **Measure C_λ (block-correlated, λ = 1/2, 1, 2):** ξ(Y) = 1{U_⌊Y/λ⌋ ≤ p(Y)}; Cov_C = Cov_A within a block, 0 across blocks.

p(Y) = Y/(1+Y) (the corpus engagement). On the grid Y ∈ {0.1, 0.25, 0.75, 1.25}: max |E_A − E_B| = 0 (identical expectation at every point, **identical field equation**, check N1); the marginal CDFs — including the on-diagonal variance Var ξ = p(1−p) — are identical for A and B (N4); the two-point spectra differ maximally: Cov_A = 0.190476 vs Cov_B = 0 at (0.75, 1.25), etc. (N2, three pairs); the C_λ family interpolates: Cov_C(0.75, 1.25) = 0, 0, 0.190476 for λ = 1/2, 1, 2 (block length; λ = 2 puts 0.75 and 1.25 in the same block). Joint-table consistency of A checked by direct enumeration (N3). **The control is capable of failing and does not**: the measures are genuinely distinct as laws (different spectra) yet invisible to every static field equation — exactly the audited assertion. The single-point marginal cannot discriminate; only a two-point (spatial/temporal covariance or run-to-run dispersion, §3) measurement can.

## 6. Independent checks in a different representation (actual residuals)

1. **Root substitution** (DM0): |Y·μ_n(Y) − D| at the solved root < 1e-45 for all six (n, D) — actual residuals in [4.2e-53, 1.0e-46] (printed in full).
2. **Direct differentiation** (T3): μ′_exact(Y) = n(1+Y)⁻ⁿ⁻¹ vs O(h²) centered difference, h = Y·1e-7: |diff| ∈ [4.9e-16, 2.2e-15], threshold 1e-8.
3. **Exact-rational series vs 50-digit numerical Taylor** (T1): max coefficient diff = 0.0 for n = 1,2,3 to order 6.
4. **Closed-form two-point joints by direct enumeration** (N3, N4) — probabilities recomputed from the table, covariance re-derived from P₁₁ = min(p₁,p₂).

All residuals above are real printed numbers, not booleans; every check states threshold-before-evaluation.

## 7. Strongest surviving statement and the audit conclusion

**Conditional theorem (branch: CORE coefficient, MU_n statistical response).** *If* (i) the response is the OR over n equal, independent binary channels μ = 1−(1−p)ⁿ; (ii) p(0)=0, p(∞)=1; (iii) p′(0)=1 (fraction identity, one-scale/large-s argument); (iv) the static metric response realizes n = 2 such channels — *then* μ′(0) = n (Lean-certified), the deep spherical matching gives g² = (s/n)g_N, and κ = a0/s = 1/n = 1/2. The probability/CDF reading alone implies none of (i)–(iv): CDF axioms admit every slope m ∈ ℕ; measures with identical CDF and different fluctuation spectra exist (negative control); the OR semantics and the sample space are un-fixed. **Therefore the CDF reading does not carry the kappa derivation and does not specify the gravitational response** — the audited claim's content is confirmed as the exact unresolved item of this branch, and κ = 1/2 remains an adopted input, consistent with k01's outcome 3 for the candidate action class.

**First additional implication needed to transfer to the full theory:** a law for the channel process's joint distributions (or a proof that no such law exists in any action of the candidate class — k01 K1/K2 cover only the static, first-moment sector and say nothing about second moments, so this is a genuinely open question, not a corollary). Without it, the probability reading is a re-description; with it, the fluctuation observable of §3 becomes a genuine prediction. This is the named target of child AS071.C01 (§11).

**No branch repair was imported** to rescue a failed statement. Nothing below is transferred to Q, RAR, MU2, EXP or MONO; the operative filtered-ν_mono target is untouched.

## 8. Bounds, environment, commands

- Prototype: 0.0033 s wall (max resident **18.6 MB**, ru_maxrss on macOS is bytes), 49/49 checks PASS, 0 FAIL, exit 0.
- **Declared bounds:** wall ≤ 120 s, memory ≤ 512 MB, 1 thread.
- **Actually enforced bounds:** wall via `timeout 120` (POSIX, enforced; run used 0.0033 s); threads = 1 by construction (single-threaded CPython, no threaded libraries, no numpy); memory: `resource.setrlimit(RLIMIT_AS/RLIMIT_RSS)` attempted at 512 MB — **macOS does not enforce RLIMIT_AS** (documented OS behavior), so the honest record is: advisory cap plus measured peak 18.6 MB ≪ 512 MB.
- Commands (argv + cwd):
  - `timeout 120 python3 -u AS071_audit.py` in `deepseek_push/astra_spawn_ideas/results/AS071/AS071_r001_deepseek-v4-flash-0731_20260928T112418Z`
  - `lake env lean <abs path>/AS071_or_slope_certificate.lean` in `fable_independent_2026/lean_2026` (compile host only; no files written into it)

## 9. Lean 4 certificate

`AS071_or_slope_certificate.lean` — compiles clean with `lake env lean` (exit 0). Theorems:

1. `or_slope_chain_rule` — d/dY[1−(1−pY)ⁿ]|₀ = n·(1−p0)ⁿ⁻¹·p′ for arbitrary differentiable p.
2. `or_slope_eq_count` — with p(0)=0, p′(0)=1: slope = n (every completion).
3. `corpus_mu_n_slope` — corpus family slope n at 0.
4. `corpus_slope_one`, `corpus_slope_two` — slopes 1 and 2 both occur (CDF-ness does not fix the slope).
5. `corpus_is_or_member` — the corpus family is an OR-class member (p = Y/(1+Y)).

`#print axioms` (unfiltered) for all six theorems: **`[propext, Classical.choice, Quot.sound]`** — subseteq the allowed set, **zero `sorry`**.

## 10. Failed attempts (preserved)

- `AS071_audit.py` v1 (first write): threshold errors, all preserved in git-less history of the file — the v1 run exposed (a) wrong saturation threshold for μ(1e8) (finite-Y deficit is Y⁻ⁿ, not 0), (b) a spurious h⁻ᵏ rescaling of `mp.taylor` output (already series coefficients), (c) naive one-term deep/Newton residuals that ignored the derived next-order terms (a₂ = (n+1)(7n−1)/96 and nY⁻ⁿ⁻¹). The v2 script in this run dir is the corrected, single canonical artifact; its first execution failed three times on mpmath `Fraction`/string-argument conversion — fixed, residuals verified. `audit_err.log` (empty except `/usr/bin/time` stderr) is preserved. These failures are control noise (thresholds), not physics.

## 11. Child proposals (ready specifications; NOT dispatched — no runner available)

**AS071.C01 — "The joint law of the channel process in the candidate action class"** (parent AS071; parent evidence: this run).
- Fingerprint: (action class of k01/PD08-as-written, MU_n branch, covariance-kernel identifiability, finite-dimensional joint distributions of the engagement process, target: does any term of the action pin Cov[ξ(Y₁),ξ(Y₂)] or prove it free?).
- New target equation: derive from the action (or prove absent) a constraint on the two-point kernel; the observable is the σ_g/g_N dispersion formula of §3.
- Controls: (a) verify k01 K1/K2 statement covers only first moments (re-derive, don't cite); (b) negative control: exhibit two kernels with equal marginals admitted by the same Lagrangian sector.
- Dependency: none outside this audit and the pinned sources. Duplicate check: closest seeds — k01 result is an audit of the FIRST-moment sector (no second-moment claim anywhere in SOURCE_MANIFEST sources); no existing task examines response covariance identification. Route stop if the sector is fully first-moment: record "no joint-law content exists in this action class" as the child's conclusive answer and mark kappa = 1/2 as empirical input for this class (matching k01 outcome 3).
- Dispatch state: **not dispatched**; specification for the orchestrator (this worker has no spawn mechanism).

No `claims/` files were created; no shared status file, manifest, ledger or task spec was modified.

## 12. Limitations

- The audit is branch-restricted (CORE coefficient / MU_n statistical response); it says nothing against the physical two-Poisson-channel computation of the linearized metric (PD01 B1), only that its identification with probability channels (L237's two readings) remains unestablished, and that the probability reading adds no dynamical content.
- No empirical verdict is claimed for the dispersion observable (§3): existing galaxy scatter data are not a controlled realization of either measure.
- The negative control covers the demonstrated construction family (global-uniform, independent, block) on a finite grid — a construction, not a theorem that NO measure with identical CDF shares the spectrum; the general identifiability statement follows from first-moment-only coupling, which holds structurally.
- Lean certificates formalize the algebraic slope identities and the OR-membership identity only; covariance computations are numerical (mpmath 50 digits, actual residuals).
- κ = 1/2 remains an adopted input; per STANDING and k01 the a0–Λ relation stays phenomenological for the candidate action class, and the amended thirteen-item target (filtered ν_mono, criterion B) is untouched by this audit.

**Strongest one-line result:** the CDF/probability reading of μ leaves the response's sample space and two-point spectrum free — the slope (hence κ = 1/n) is carried by the physical premises (OR composition, p′(0)=1, channel count), and the missing equation is the channel process's joint law (first-moment operators cannot see it; negative control passes).