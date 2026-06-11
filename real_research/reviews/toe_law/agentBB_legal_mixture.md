# agentBB — THE LEGAL-MIXTURE ESCAPE IS CLOSED: the conformal-balanced positive KL family tops out at baseline +0.023–0.026 dex on the real SPARC RAR (past the pre-registered 0.02 line, both footings, both signs) AND its best fit violates the agentE sun-reflex budget ×21 — a forced-positive VARIANCE PINCER (Σc(x−2)² ≥ ~5 for the band vs ≤ 0.24 for the Sun) with no sweet spot. agentV's boundary theorem hardens to data grade.

*agentBB, 2026-06-11. Task (the pre-registered NNLS follow-up of agentV §5.2 / registry item (v) — THE one
quantitative residue of the kernel-inversion boundary theorem): can a LEGAL (dS-Källén–Lehmann-POSITIVE)
spectral mixture, with the one allowed tuning (conformal balance ∫(x−2)dρ = 0, x = M²/H², which kills the
leading (a₀/a)-level lightcone term — feasible per agentV [E3] J=0), produce an effective μ(a) on the
Deser–Levin family that fits the REAL 175-galaxy SPARC RAR at the survival line, while clearing the banked
solar budgets? Inputs: agentN1 closed-form commutator tail (the atom kernels), agentV [V-A4] probability-measure
response form, the LOCKED SPARC conventions of `mi_f4_sparc_shape_test.py` (unweighted dex scatter primary,
per-function best-Υ on the 0.3–1.2 grid, both a₀ footings), the agentE reflex line (δa☉ ≤ 2.47×10⁻¹⁵ strict /
3.38×10⁻¹⁵ loose) and the pinned Folkner Cassini Saturn-radial bound (≤ 10⁻¹⁴). Artifacts:
`agentBB_legal_mixture.py` → `agentBB_legal_mixture.out` (all numbers below machine-generated there; kernel
cache `agentBB_kernel_cache.npz`). Pre-registered verdicts: ESCAPE-LIVES (legal mixture ≤ baseline+0.0100 dex
AND solar-clean) / ESCAPE-CLOSED (no legal mixture ≤ baseline+0.0200 at either footing OR all SPARC-fitting
mixtures violate solar) / PARTIAL. Raw numbers first; verdict at the end, both ways. Bug log, recorded not
hidden: (i) build v1 fitted the NNLS surrogate to μ_RAR = 1−e^{−√x} — WRONG TARGET: the exact MI inversion of
μ_RAR scores 0.2189 dex (fw), not 0.1950 — the survival-line FUNCTION is ν_McGaugh(y) = 1/(1−e^{−√y}), whose
implied μ (μ_tgt(x) = y/x along x = y·ν(y)) is the correct target; caught by the [REG] gate, §1. (ii) scipy's
NNLS crashed on the heavy balance-penalty row; replaced by the EXACT parameterization of the balanced cone by
light–heavy pairs (every balanced positive measure = positive combination of two-point balanced pairs). (iii)
the response SIGN (agentV §5.2 registry item iv / N2 [C4]: the deficit-channel sign is open in the repo) is
load-bearing here — under the Quinn-anchored sign the family is anti-shaped on the band; BOTH signs run, the
family scored at its better sign throughout.*

## 0. The machinery, pinned

- **Atom kernels** (agentN1 closed form, units H = 1, normalization absorbed into weights):
  K_x(u) = (x−2)·₂F₁(3/2+ν, 3/2−ν; 2; −u/2), ν = √(9/4−x), u = Z−1. Verified: endpoints K_x(0⁺) = x−2 exactly;
  conformal zero at x = 2; MMC anchor x→0 constant tail (₂F₁ ≡ 1.000000 at u = 10⁻⁶, 1, 10⁶); principal-series
  reality max|Im| ≤ 1.8×10⁻²⁵.
- **Response** (agentV [V-A4]): E_t[K] = ∫K dν_t, dν_t = (t/2)u^{−1/2}(u+t)^{−3/2}du, t = 2H²/κ².
  Grid: 576 Gauss–Legendre nodes (24/decade, u ∈ [10⁻¹⁶, 10⁸]); measure normalization 1 − Σw ≤ 1.7×10⁻⁸ on the
  band (8.5×10⁻⁴ at the Saturn t = 1.4×10⁻¹⁰); grid-vs-adaptive-quadrature cross-check ≤ 1.1×10⁻⁷ rel including
  the heaviest atom x = 200 (its log-u oscillation rate μ̂ = 14.1 resolved).
- **Effective MI law**: μ_mix(x_acc) = 1 − sign·Σ_j c_j E_{t(α)}[K_{x_j}]/√(1+α²), α = η·x_acc,
  t = 2/(1+α²), η = a₀/cH_Λ = 0.17250 (fw) / 0.22115 (canon) — agentV [F] reproduced. c_j ≥ 0 = KL positivity;
  amplitude free (absorbed); rotation curves by exact numeric inversion μ(g_obs/a₀)·g_obs = g_bar.
- **The legal tuning**: Σc_j(x_j−2) = 0, enforced EXACTLY (pair-cone parameterization + machine rebalance,
  residual ≤ 10⁻¹⁶ rel). The J = 1 condition is NOT imposed — agentV's [X2] identity makes J=0∧J=1 collapse the
  measure to the zero-tail conformal point; its forced value is the solar tail we then measure. Key identity used
  below: **with m₀ = 0, the J=1 moment IS the variance, Σc(x−2)x = Σc(x−2)² > 0 — positive-definite, no
  cancellation available inside the legal cone.**
- **Atoms**: 48 masses x ∈ [0.05, 200] (agentV's LP band extended; boundary pairs at 2±0.01; x < 0.05 = the
  Allen IR corner excluded as in agentV — and its members are shape-degenerate with x = 0.05 anyway).
- **[REG] regression gate** — the locked table reproduced EXACTLY before any new scoring: fw 0.1969 / 0.1950 /
  0.1951 / 0.1984 (fw-shape / McGaugh / simple / F4), canon 0.1968 / 0.1977 / 0.1975 / 0.1980; 175 galaxies,
  3391 points. Deep-MOND analyticity echo on a real atom (x = 8.2): slopes of E(2−ε)−E(2) → 1.0122, 1.0012,
  1.0001 (agentV [D]: analytic, target law needs 0.25 — the flattening theorem bites the real kernels).

## 1. The sign adjudication (new, data-level)

Under **sign +1 (Quinn-anchored: heavy side = deficit)** the family is structurally ANTI-SHAPED for MOND: a
heavy atom's deficit GROWS with acceleration toward its lightcone endpoint (E_t[K_{200}] rises from 14.0 at
t = 2 to 71.8 at t = 0.067, .out [1]) while the RAR needs the deficit to DIE with acceleration. NNLS on the balanced cone returns
the zero mixture (scatter 0.3776 = the bare-Newtonian limit; the positive unbalanced best is 0.2352, carried
entirely by the near-conformal boundary atom). Under **sign −1 (the Link-5 chain-line reading: light side =
deficit)** the family is MOND-capable: light atoms carry slowly-decaying positive deficits. **The inverse
problem therefore resolves agentV's flagged sign AT THE DATA LEVEL: a linear-bath MOND response requires the
light spectral side to be the deficit channel** — the Link-5 chain wording, not the Quinn anchor, is the only
phenomenologically viable assignment (flag for the N-series reconciliation, agentV §5.2 item iv). All legal-family
numbers below are at the better sign (−1); both signs are in the .out.

## 2. The fit (raw numbers; LOCKED conventions, per-mixture best-Υ, both footings)

| mixture (sign −1 where relevant) | fw unw dex (Δ base 0.1950) | canon unw dex (Δ base 0.1977) | legal? |
|---|---|---|---|
| **NNLS balanced cone** | **0.2211 (+0.0261)** | 0.2346 (+0.0369) | YES |
| **POLISHED balanced** (Powell on the locked objective; multi-start ×3, 12k evals, confirmed) | **0.2211 (+0.0261)** | **0.2211 (+0.0234)** | YES |
| POLISHED balanced + solar budget enforced | 0.3704 (+0.1754) | 0.3704 (+0.1727) | YES |
| NNLS / POLISHED positive unbalanced (1/a tail) | 0.2205 / 0.2201 (+0.0251) | 0.2311 / 0.2201 | no (and solar ×5×10⁵) |
| signed lstsq control (free signs = illegal) | 0.2048 (+0.0098) | 0.2121 (+0.0144) | no |
| [reference] exact MI inversion of μ_RAR = 1−e^{−√x} | 0.2189 (+0.0239) | 0.2128 (+0.0151) | — |

- **The best LEGAL mixture is 0.2211 dex at BOTH footings — past the pre-registered closed line
  (baseline+0.0200) at both.** Restarts from independent seeds (NNLS, data-median target, single-pair) all land
  on 0.2211 to 1e-4; the convex NNLS surrogate agrees with the real-objective polish — converged, not stuck.
- **The family is effectively one-dimensional in shape**: the single best balanced PAIR (x = 0.05, 2.01)
  already achieves the full 512-pair cone's surrogate residual (0.150 vs 0.1504), and the optimum concentrates
  254 of its 255 total spectral mass at x = 2.01 — the boundary "conformal-derivative" direction, agentV's
  [E3] mass divergence appearing in the data fit (the amplitude wall inherits this ×250 multiplier).
- **Shape autopsy** (fw, .out [8]): the legal optimum is a deep-end PLATEAU μ ≈ 0.18 (vs target 0.048 at
  x = 0.05 — under-deficit ×3.8) followed by an α³-cliff recovery that over-deficits the mid-band (μ = 0.20 vs
  0.51 at x = 1) — the analyticity flattening (agentV §2.2) pulled INTO the band: |Δdex vs McGaugh| > 0.05 for
  ALL y < 10.9. Best-Υ slams to the locked grid floor (0.30) trying to compensate. μ stays positive, μ(x)x
  monotone (mono-viol 0) — the failure is genuinely the SHAPE, not a pathology.
- **Even the ILLEGAL controls cannot reach the survival line cleanly**: free-sign lstsq gets +0.0098 (fw) only
  with a wildly indeterminate measure (|mass| 1.9×10⁸, variance 1.9×10⁷) and a NON-MONOTONE μ(x)x
  (violation 0.78 — a multivalued rotation-curve law, unphysical); the positive unbalanced family bottoms at
  +0.0251 with the fatal 1/α tail. The Deser–Levin response basis itself — analytic in a² with the 1/κ
  prefactor — cannot carry the RAR shape; positivity then costs another +0.016.
- Duality-gap flag (caught by the [REG] gate, worth banking): the exact MI inversion of μ_RAR = 1−e^{−√x}
  scores 0.2189 (fw) — the campaign's 0.1950 survival line belongs to the McGaugh ν-FUNCTION; its implied
  MI-μ has μ(1) = 0.511 (not 0.632). Channel verdicts elsewhere are unaffected (the high-a tail is the same
  exponential class), but "μ_RAR fits SPARC at 0.1950" should be read as ν-form, not MI-μ-form.

## 3. Solar budgets (banked lines; .out [7])

| mixture (fw; canon within 5%) | δa☉ [m/s²] | × strict (2.47e-15) | × loose | δa_Sat | Saturn (1e-14) | tail power |
|---|---|---|---|---|---|---|
| best legal (balanced, 0.2211 dex) | 5.13×10⁻¹⁴ | **20.8 — FAIL** | 15.2 — FAIL | 1.06×10⁻¹⁸ | pass | a^{−2.87} |
| legal forced solar-clean (×1.00 strict) | 2.48×10⁻¹⁵ | 1.00 — pass | pass | 5×10⁻²⁰ | pass | a^{−2.87} |
| positive unbalanced control | 1.36×10⁻⁹ | 5.5×10⁵ — FAIL | FAIL | 1.4×10⁻⁹ | ×1.4×10⁵ FAIL | a^{−1.00} |

- **The variance pincer, measured.** The balanced tail obeys δa☉ ∝ Σc(x−2)² exactly (1.03×10⁻¹⁴ per unit
  variance at the fitted shapes, constant to 1.5% across mixtures) — the forced-positive J=1 moment IS the
  solar observable. The band fit demands variance ≈ 5.0; the strict sun line allows ≤ 0.24. **Factor ≈ 21, no
  cancellation possible inside the legal cone** (variance positivity). The pincer curve (.out [7b], fw):

  | allowed budget k × strict | 1.0 | 3.16 | 10 | 31.6 | 100 |
  |---|---|---|---|---|---|
  | best legal scatter (dex) | 0.3707 | 0.3560 | 0.3110 | 0.2211 | 0.2211 |
  | variance used | 0.24 | 0.76 | 2.39 | 5.01 | 5.01 |

  A solar-compliant legal mixture retains a ≤ 4% inertia deficit at the deep end (μ ≥ 0.96) — RAR-blind,
  scatter +0.175. Full SPARC strength is only reached at ≥ 21× the strict reflex budget. **No sweet spot.**
- **Two corrections to agentV §5.2's residue wording, machine-measured**: (i) the balanced residual tail is
  (a₀/a)^{2.84–2.88} — the t·ln t cubic-log class, NOT "(a₀/a)⁴-class"; (ii) "far below the reflex budget"
  holds per unit spectral variance but FAILS at band-fit amplitude — the fit forces variance ≈ 5 ⇒ ×21 over.
  The Saturn radial line, by contrast, is genuinely safe for every balanced mixture (the steeper-than-quadratic
  tail clears it by ≥ 10⁴) — the binding solar constraint is the SUN reflex at x ≈ 2.2×10³, exactly where the
  cubic-log tail has not yet died. (Budget transfer: the agentE line was derived for instantaneous-μ templates;
  agentM showed frozen-vs-instantaneous transfers within ~2% — the ×21 margin is far outside that slack.)

## 4. VERDICT (both ways, full weight)

> **ESCAPE-CLOSED — on BOTH pre-registered arms independently, at both footings, under both sign conventions.**
> (1) No legal (dS-KL-positive, conformal-balanced) mixture reaches baseline+0.02 dex on the real SPARC RAR:
> the family's machine-confirmed optimum is +0.0261 (fw) / +0.0234 (canon) — and even unconstrained-sign
> ILLEGAL combinations of the same response basis only reach +0.0098 with an unphysical multivalued law.
> (2) Every legal mixture that even approaches the band fails the agentE sun-reflex line ×20.9 (strict) /
> ×15.2 (loose), by a FORCED-POSITIVE variance moment with no cancellation escape; enforcing the budget
> collapses the family to a ≤ 4% deficit (scatter +0.175). **agentV's boundary theorem extends from "the exact
> exponential law" to "anything RAR-grade": no linear field-bath in dS-invariant QFT — legal, tuned, or even
> sign-illegal within the same kernel basis — carries the data. Link 5's worldline closure is now data-grade.**

- **Framework-unfavorable reading, full weight:** none of this derives the framework's μ; it closes a rival
  lane. The closure is also convention-robust in the directions Carl's working rule demands: both footings (the
  canonical a₀ = 1.2×10⁻¹⁰ row is marginally MORE favorable to the escape, +0.0234, still past the line), both
  scatter metrics reported, per-mixture best-Υ granted, the optimizer cross-checked by a convex surrogate,
  restarts, and a free-sign ceiling. The honest caveats: 48-atom discretization (but the optimum concentrates
  on a single boundary direction the grid resolves at Δx = 0.01, and the signed control bounds any refinement);
  Powell is not a global-optimality proof (but the binding walls — a²-analyticity at the deep end and variance
  positivity at the solar end — are moment-forced, optimizer-independent); the Υ grid floor 0.30 binds (locked
  convention; the mixture wants lower, i.e., even its best fit is partly an Υ artifact in its own favor).
- **Framework-favorable, same weight:** (a) the one named escape from the kernel-inversion theorem is now shut
  with real data — the missing object CANNOT be any spectator dS-invariant field bath at any legal spectral
  content; the surviving mechanism space remains exactly the repo's chosen door (dS-invariance-breaking media:
  khronon-M22 matter sector, agentU), now selected by a data-grade theorem rather than an algebraic one.
  (b) The legal family's failure mode is itself the fingerprint agentV predicted: deep-band flattening
  (μ → 0.18 plateau) + cubic-log tail — the data kill it through exactly the structures the theorem named.
  (c) New small result: the open SIGN flag is data-resolved (light side = deficit channel is the only
  MOND-capable assignment — supports the Link-5 chain-line wording; the Quinn-anchored convention must attach
  to an anti-RAR response and so cannot be the MI mechanism's sign).
- **What would have overturned this** (pre-stated): a balanced mixture within 0.01 dex passing both solar
  lines — the machinery had every freedom to find it (512-pair cone, free amplitude, best-Υ, both signs, both
  footings, solar-constrained polish) and the optimum landed a factor ~21 outside on the solar arm and
  +0.023–0.026 dex past the survival line on the scatter arm simultaneously.
- **Untouched:** the effective law (Link 6) and its ν-form SPARC standing; the lensing partner (Link 7); the
  a₀ kernel phenomenology; agentV's §5.3 named escapes (non-dS-invariant sectors — where the spec lives;
  IR-divergent Allen corner — destroys stationarity; nonlinear couplings — argued, not machine-closed).
- **Registry handoff:** (i) agentV §5.2 residue item (v) can be marked CLOSED-NEGATIVE at data grade; Link 5's
  status line may now read "worldline closure incl. the conformal-balanced legal mixture (agentBB: +0.023–0.026
  dex AND ×21 sun-reflex, pincer-forced)"; (ii) the sign flag (item iv) gets the data-level resolution of §1;
  (iii) two wording corrections to agentV §5.2 (tail power ~(a₀/a)^{2.9}, and the residue is NOT below the
  reflex budget at band amplitude); (iv) the McGaugh ν-vs-MI-μ duality gap (0.2189 vs 0.1950, §2 last bullet) —
  a conventions flag for any future memo that scores "μ_RAR" on SPARC in MI form; (v) watchlist: the deep-RAR
  flattening a_* — for the legal family it sits INSIDE the band (the reason it dies); any surviving mechanism
  must keep it below x ≈ 0.05.

## 5. Anchors
- In-repo: `agentV_kernel_inversion.md` (§5.2 the pre-registered residue; [V-A4]; [X2]; [E3]; [F]),
  `agentN1_nonhuygens_commutator.py` (the closed-form tail and its anchors), `mi_f4_sparc_shape_test.{py,out}`
  (locked SPARC conventions + baselines), `agentM_milgrom2022_gauntlet.{py,md}` (reflex budget form
  δa☉ = a_J·(1/μ−1), budget 2.47/3.38×10⁻¹⁵; frozen-template transfer note), `MI_BATH_TAIL_CONSTRAINT.md`
  (pinned Folkner Cassini Saturn radial < 10⁻¹⁴, via arXiv:1001.3686 §VI), `agentE_solar_reflex.out` (the
  survival line's origin), `DERIVATION_CHAIN.md` Link 5.
- Bros & Moschella (gr-qc/9511019); Hogervorst–Penedones–Vaziri (2107.13871); Loparco et al. (2306.00090) —
  the KL positivity that defines "legal".
- Lawson & Hanson NNLS; Powell (1964) — the solvers; the balanced-cone pair decomposition is elementary
  (every point of {c ≥ 0, q·c = 0} is a positive combination of two-point q-balanced vectors).
