# Y1_pmedium_flavor — FROZEN CRITERIA (committed alone with ASSUMPTION_LEDGER.md, before any script or number)

Lane `rebuild_2026_10_22/Y1_pmedium_flavor/`. Written 2026-10-23. Rules: `rebuild_2026_10_22/BRIEF.md`,
`doors_push_2026_10_22/BRIEF.md`. κ = ½ FITTED. Footings a₀ = 9.3603e-11 (canonical) and 1.1312e-10 m/s² (alt), scored
separately, never pooled. Never "theory closed"; never "the data favour the framework". Nothing in `sol61_push/` is edited.

Goal: score the "P-medium" flavor (Codex's reduced preferred-frame action) on the status-board tiles, so the coordinator
can hand per-tile verdicts to the board agent. This lane does NOT edit `explainers/make_flavor_boards.py`.

## 0. The flavor and the action scored

**Recipe (two lines).** Newtonian gravity ∇²Φ = 4πG(δρ_b + δρ_c) on all matter, plus a cold collisionless medium that
also feels h = e/χ, where e = δρ_c − ∇·P is the mismatch between the cold density and the divergence of a saturating
polarization P (W = −|P| − ln(1−|P|), force P/(1−|P|)), and χ is a stiffening scalar (α(χ−1)²/2 + d|∇χ|²/2); baryons
feel Φ only. Preferred frame, imposed EdS background; η = .005, b = d = .125, α = .005, ℓ₀ = 0.440422 kpc; a₀ via units.

**Action scored.** XP-20261023 (`sol61_push/expanding_polarization_2026_10_23/DERIVATION.md`, sha256 29d3e7a0…), in
code units (length ℓ₀, acceleration a₀, time t₀ = √(ℓ₀/a₀), density a₀/(4πGℓ₀), mass M₀ = a₀ℓ₀²/G):

  S = ∫dt { Σ m A²|ẋ|²/2 + (1/4π)∫d³x A³ [ η|Ṗ|²/2 + bχ̇²/2 − |DΦ|²/2 − Φ(δρ_b+δρ_c) − W(|P|) − e²/(2χ)
        − α(χ−1)²/2 − d|Dχ|²/2 ] },   e = δρ_c − D·P,  D = A⁻¹∇,

with its 3D discretization SE-20261023 (`sol61_push/spatial_expansion_2026_10_23/DERIVATION.md`, efd0511c…) and the
homogeneous extension `MINISUPERSPACE.md` (766616a0…). Parameter values and sources are in ASSUMPTION_LEDGER.md §A.
The static limit is A = 1. No covariant parent, metric sector or tensor modes are part of this action (XP DERIVATION
"It is NOT a uniquely derived covariant parent"); this lane scores the action as written and never supplies one.

## 1. Tiles: method, frozen line, class rule

Classes: PASS / CONDITIONAL / FAIL / NOT DECIDABLE / NOT COMPUTABLE (with what is missing). A reuse of another lane's
pipeline is allowed only after a check shows the equation it solves is this flavor's (stated per tile).

### Y-T1 Gravity-wave speed; binary pulsars
- Method: the action's field content (sympy): list every field; check for a tensor metric perturbation h_ij.
- Rule: no tensor sector ⇒ **NOT COMPUTABLE** (missing: a metric sector / covariant completion).
- Reported, no class weight: in a minimal-coupling completion (GR + these fields, no curvature couplings, no aether
  kinetic term), (i) the (P, χ) stress vanishes on the vacuum/FRW-mean state P = 0, χ = 1, e = 0 (sympy: energy density
  and its first derivatives zero there) ⇒ c_T = c on those backgrounds; (ii) baryons do not appear in the P or χ
  equations ⇒ no scalar/vector dipole channel from a baryonic binary.
- The record's CFG938 / WT-02 / CFG961 statements (c_T ≠ c, FRW ill-posed) are re-checked against THIS action, not assumed.

### Y-T2 Health and well-posedness
- H1 (Minkowski, any admissible background, frozen coefficients): 2000 random backgrounds with ρ_c, ρ_b ∈ [0, 1e4],
  |P₀| ∈ [0, .985], χ₀ ∈ [0.1, 1e3], e₀ ∈ [−1e3, 1e3] (code units), random directions; k = 1e0 … 1e8. Build the
  Hermitian quadratic form for (cold ξ, baryon ξ, P, χ). **Line: max growth rate Γ(k) ≤ √(ρ_c+ρ_b)·(1+1e-6) for every
  background and k** (Jeans-bounded; no ghost; no gradient instability), and the potential Hessian minus gravity is PSD.
- H2: principal speeds at k = 1e8: fast P mode ω²/k² = (ρ_c + 1/η)/χ₀ and χ mode d/b, numeric vs formula ≤ 1e-6.
- H3 (FRW): the linearized XP one-mode equations (EdS, z = 1100 → 0) for k = 0.01 … 1000 Mpc⁻¹: retained cold and total
  amplitude ≤ the dust reference (1 + 1e-6) at every k, and non-increasing in k (no Hadamard growth at high k).
- Rule: **PASS** iff H1–H3 pass (scope stated: reduced, non-covariant action). FAIL if any line fails.
- H4's saddle maps are used only if this action has a fluid with negative density; the ledger records why or why not.

### Y-T3 Static galaxy limit → SPARC RAR
- R1 (sympy): on the support of a zero-dispersion (T = 0) static cold medium, Φ + h = μ_c. Show the static equations
  reduce to ∇·[μ(|∇Φ|/a₀)∇Φ] = 4πGρ_b + χ(μ_c − Φ)/ℓ₀² with μ(x) = x/(1+x) and χ ≥ 1 (minimum principle).
- R2 (reproduction): my own SPARC loader and the algebraic AQUAL law with one Υ per galaxy reproduce P4's
  `iso_perUps` rms (canonical 0.05409) to ≤ 2e-4 and its median Υ (0.52) exactly.
- R3 (bound validation): a nonlinear spherical T = 0 solver (Φ, h, P algebraic, χ by a Yukawa Green's function,
  iterated) on 3 SPARC galaxies × 4 central amplitudes: the first zero of h obeys r₁ ≤ πℓ₀ and the support ends inside
  the analytic bound R_s (README derivation); outside it the field is exactly Newtonian.
- Score (T = 0 branch, the only static state fixed without a cold distribution function): on SPARC points with r > R_s,
  g_pred = g_N,b(Υ) + G M_c / r², Υ ∈ [0.30, 1.20] (step 0.01) and M_c ≥ 0 free per galaxy; P4's CFG4-weighted rms of
  log₁₀(g_obs/g_pred) and median Υ. **Line (P4 T1): rms ≤ 0.110 dex and median Υ ∈ [0.50, 0.80], each footing.**
- Rule: if the static equations leave the cold distribution undetermined given the baryons (DF freedom), the tile is
  **NOT COMPUTABLE** (missing: the cold distribution's history), with the T = 0 branch's P4 class attached. If R1 showed
  the cold distribution fixed by the baryons, the tile class would be the score's class.

### Y-T4 Solar System / Cassini
- Gates (CFG3_solar_system.py L21, L67; D7d/C6): cold mass inside Saturn's orbit (9.58 AU) < 6.7e-11 M☉; sunward anomaly
  at 1 AU < 3.66e-14 m/s²; Cassini Q₂ < 9.0e-27 s⁻² (Hees 2014; Park 2026 5.2e-27 reported).
- Branch S-a: ambient collisionless cold medium at the Sun, ρ_loc = 0.013 and 0.1 M☉/pc³ (×8 generous), dispersion
  σ ≥ 100 km/s (gravitational focusing factor 1 + v_esc²/σ²); Q₂ bounded by (4πG/3)ρ (full anisotropy).
- Branch S-b: a T = 0 cold atmosphere bound to the Sun (static solution of the action): analytic lower bound on its
  mass inside r, M(<r) ≥ (a₀r²/G)(1 − a₀/g_N) where h ≥ 0, plus one solver example.
- Rule: **PASS** iff S-a and S-b pass all gates on both footings; **CONDITIONAL** iff S-a passes and S-b fails (the
  verdict then rests on no captured T = 0 atmosphere; the conservative no-capture condition v_rel > V_esc is evaluated
  and stated); **FAIL** iff S-a fails.

### Y-T5 Hosted dwarf satellites; TDGs and NGC 1052-DF2/DF4
- D1 (reproduction): U1's dust-free (B0 = Newtonian) TDG statistic (n = 6, r̄ = +0.0546, se 0.1144, U1 results JSON) to
  ≤ 1e-3 and DF2/DF4 B0 r = +0.30 / −0.24 ln to ≤ 0.01, from the raw on-disk inputs with my own code.
- Equation check before reuse: this action's baryons feel Φ only (Newton) ⇒ a cold-free system's prediction is exactly
  B0. A system holds cold medium only if it can bind it; the conservative capture condition (v_rel vs V_esc) is stated.
- TDG/DF2 tile rule: **PASS** iff B0 is within 2σ (TDGs |r̄| < 2se; DF2, DF4 each |r| < 2σ_obs) and the cold-free state
  follows from the action plus a conservative no-capture argument; **CONDITIONAL** if B0 passes but cold-free is only a
  history assumption; **FAIL** if B0 fails.
- Satellites (S1 statistic, bootstrap median of log₁₀(g_obs/g_pred), 4000 resamples, seed 23): the cold-free branch is
  scored (Newton); held cold cores have no derived masses (W1: no certified core) ⇒ **NOT COMPUTABLE** unless a
  diagnostic shows no satellite can hold the needed core. Diagnostic (T = 0 branch, reported): for each S1 satellite the
  pure-cold T = 0 core that gives its g_obs at r_h; its support radius r_s against its Jacobi radius
  r_J = (G M_tot d/(2 g_host))^{1/3} with g_host = x_e,mid a₀; fraction with r_J ≥ r_s. If that fraction is 0 on both
  footings, the T = 0 branch is FAIL (attached to the NOT COMPUTABLE class).
- Contrast stated: U1's theorem T3 (held dust weightless in v3) is checked against this action's cold coupling.

### Y-T6 Cluster cores
- Rule: F1's statistic is computed only if this action has a static cluster prediction independent of the cold
  distribution; otherwise **NOT COMPUTABLE** (missing: the cold profile). The cold-free Newtonian floor (F1 README L46-L47: A_MID 9.8 ± 0.6)
  and the T = 0 support bound are reported.

### Y-T7 Linear growth
- G1 (Codex reproduction): my own integrator of XP's one-mode equations (exact averaged W, EdS, z = 1100 → 0, amplitude
  1e-6, three field preparations) reproduces `growth/result.json` retained_total at k = 0.1, 1 Mpc⁻¹ to ≤ 2e-5 absolute.
- G2 (F3 machinery reproduction): my own two-fluid ODE + CLASS P(k) reproduces F3 K4's BSK2-kernel σ8 ratios at
  μ = 1100 h/Mpc on background A (0.993 from a_i = 1e-3, 0.861 from 1e-4; F3 README L98) to ≤ 0.003.
- G3 (equation identity, sympy): the quasi-static (η → 0, χ = 1) limit of XP's cold equation is F3's BSK2 kernel
  s = 1/(1 + x²), x = k/(aμ), with μ = 1/ℓ₀ (comoving), i.e. the cold self-gravity fraction S = 1/(1 + (kℓ₀/a)²).
- Score: σ8 ratio to the dust limit with S, on F3's backgrounds A and B, from a_i = 1e-3 and 1e-4 (ΛCDM-processed
  background and abundance, as for F3's ΛCDM/dust-limit rows). Finite-inertia correction at k = 1 Mpc⁻¹ (EdS, ratio of
  G1's retained values to the quasi-static value) reported per footing.
- **Line (F3 K5): σ8 within 5 % of the dust limit (ratio ≥ 0.95).** PASS iff met from both a_i on both backgrounds;
  CONDITIONAL iff met only from a_i = 1e-3; FAIL iff met from neither.

## 2. Overall reading (frozen form)
One line: which v3 FAIL tiles this flavor turns to PASS ("fixes"), and which v3 PASS/COND tiles become FAIL or NOT
COMPUTABLE ("loses"), using the v3 column as printed by `explainers/make_status_board.py` TILES (read-only).

## 3. Script, checks, MUTATE
- `y1_pmedium_flavor.py` prints `K# PASS value threshold` per check, ends `Y1_PMEDIUM_FLAVOR COMPLETE: N/M checks PASS.`,
  exit 0 iff all pass; writes `y1_pmedium_flavor.out`, `y1_pmedium_flavor_results.json`. Deterministic, no network.
- `--mutate` plants three defects and must break ≥ 1 check: (M1) d → −d in H1 (χ gradient energy reversed);
  (M2) the e²/(2χ) term removed from the static T = 0 solver (exact tether, the law) in R3; (M3) the h-force removed
  from the growth equations (S = 1) in G1. Writes `*_MUTATE.out`, `*_results_MUTATE.json`; exit 1.
- Compute: `OMP_NUM_THREADS=1 nice -n 15`, one thread, < 2 GB RSS, minutes. Anything long gets a README ENQUEUE block
  (priority 230–239, `compute_queue/JOB_CONTRACT.md`), not enqueued by this lane.
