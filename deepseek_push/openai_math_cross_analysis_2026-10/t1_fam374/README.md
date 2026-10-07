# T1 (family 374): "Sharp One-Third Stability of Brenier Maps" vs the settling problem

Criteria: `FROZEN_CRITERIA.md` (T1, controls C1–C6, MUTATE). Script `t1_fam374_brenier_stability.py` (~40 s CPU). kappa = 1/2 is FITTED. Both a0 footings scored separately, never pooled. No dark-matter particle is added; the cold fluid's mass (5.364 M_b) is an input, not derived. This is not "theory closed". Manuscript: `openai_math/preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/article.pdf`; Lean doc `lean/docs/374.md` certifies Theorem 1.1 (uniform source on compact convex K, targets in fixed compact Y: `||T_mu - T_nu||_{L2(rho)} <= C(K,Y) W2(mu,nu)^{1/3}`, exponent sharp).

## Verdict: TOOL (both footings). Not a forcing result; the explicit 1/3 bound is quantitatively vacuous at the Milky Way scale; the stability that actually holds is exact and linear, and comes from radial monotonicity, not from the theorem.

**Setup (frozen).** M_b = 1e11 Msun point baryons; G = 6.674e-11; Msun = 1.989e30 kg; pc = 3.0857e16 m; phantom target = rho_ph on [r_in, r_out] = [0.5, 818] kpc, normalized, via M_ph(r) = M_b(nu(y)-1), y = G M_b/(a0 r²); 0.1-dex perturbation M_b -> 1.2589 M_b. Source = CFG375 uniform cold-fluid supply ball (M_t = min(M_ph, 5.364 M_b), R_K = 1563.7 kpc); radial monotone settling maps = equal enclosed-mass rearrangement (CFG375 convention). Radial targets + uniform-ball source give the exact identity ||T_mu - T_nu||_{L2} = W2(mu,nu) (verified, C1a).

## Key numbers (canonical / alt footing)

| quantity | canonical | alt |
|---|---|---|
| r_t = sqrt(G M_b/a0) | 12.20 kpc | 11.10 kpc |
| M_ph(r_out) before / after +0.1 dex | 6.653e12 / 7.458e12 Msun | 7.318e12 / 8.205e12 Msun |
| M_ph shift (frozen C6 "~25%") | **+12.10%** | **+12.11%** |
| elasticity d ln M_ph / d ln M_b | 0.496 (deep-MOND √M_b ⇒ 0.5) | 0.496 |
| W2(phantom, perturbed phantom) = map change | **0.4073 kpc** | **0.3719 kpc** |
| deep-MOND response model (1/(e^s−1) = 1/s − 1/2 ⇒ origin at r_t/2) | 0.4298 kpc (measured 0.95×) | 0.3910 (0.95×) |
| C* (Eq. 6.3; K = supply ball, L = r_out, kpc units) | 1.2880e5 kpc = 3.975e24 m | same |
| worst-case bound C*·W2^{1/3} | 9.55e4 kpc | 9.26e4 kpc |
| trivial diameter bound 2L | 1636 kpc | 1636 kpc |
| bound vs trivial (vacuous by) | ×58.4 | ×56.6 |
| **ratio actual map change / worst-case** | **4.27e-6** | **4.02e-6** |
| M_ph(r_in)/M_ph(r_out) (truncation discards) | 3.8e-13 | 3.1e-12 |
| shape perturbation (uniform 5 kpc ball vs point baryons): W2 | 0.026 kpc | 0.024 kpc |

The 0.1-dex baryon error moves the settled map by ~0.4 kpc — 0.05% of r_out. The paper's explicit constant makes the bound ~58× looser than even the trivial 2L bound: the theorem states a true inequality, but with C* fixed the 1/3 power is empty at these scales, and the honest stability content is the identity ||ΔT|| = W2 (exponent 1, linear response).

## Controls (measured vs threshold; all PASS in the main run, rc 0)

- **C1 (cube sharpness, Prop 2.2):** a = 0.4, b = 0.2. W2² = 0.016000000000000004 (LP; target 0.016, tol 2%) ✓; ||T_mu−T_nu||² = 0.116139 vs 0.116 (MC, N = 2,000,000, seed 374, tol 2%) ✓. Cube ratios: |ΔT|/W2 = 2.69 (amplification); |ΔT|/W2^{1/3} = 0.679, asymptoting to ~0.63 as a↓0 (exponent 1/3 sharp only against α > 1/3).
- **C2 (adversarial vs smooth at equal W2 = √0.016):** atom map change 0.3408 > smooth radial pair 0.1265 ×1.01 ✓ (smooth pair: uniform 3-balls radii 1 and 1.1633, |ΔT| = W2). The 1/3 bound is sharp only adversarially.
- **C6 (scaling):** M_ph(r_out) shift +12.10% / +12.11% ∈ [10%, 33%] ✓ both footings. Declared window brackets the deep-MOND √M_b response (12.9%) and the linear response (25.9%); the frozen "~25%" is the naive linear reading — the measured elasticity 0.496 (deep-MOND, exactly 1/2) is reported honestly.
- **C1a (radial identity):** direct MC map-change² (2e6 samples, seed 3740) = W2² grid integral to 7.5e-4 rel (tol 2%) ✓ both footings.
- **C1b (deep-MOND W2/scale relation — the C1-adjacent check):** W2 ∈ [0.75, 1.25] × r_t(√1.2589−1)/(2√3) = 0.4298 (canon) / 0.3910 (alt) kpc: measured 0.4073 / 0.3719 ✓. The declared model was corrected during development: nu−1 = 1/(e^s − 1) = 1/s − 1/2 + …, so the phantom's effective inner origin is r_t/2, not r_t; the naive 1/s − 1 form over-predicts W2 by 2.1× (recorded in docstring and JSON as `deepMOND_pred_naive`).
- **C3 (base rate):** family F (891 distinct values) 1%-window share at T = 1/√(32π) = 0.224% ∈ [0.1%, 0.6%] ✓, consistent with the record ~0.2–0.3%.
- **MUTATE** (`T1_FAM374_MUTATE=1`, outputs `*_MUTATE`): perturbed target replaced by an uncorrelated gaussian blob (σ = 200 kpc, same mass). Declared flip: **C1b FAILS on both footings** (W2 = 142.5 / 142.4 kpc vs window [0.32, 0.54]) — rc 1 ✓. C1, C2, C6, C1a, C3 pass as declared (pure geometry / phantom-intrinsic; the radial identity holds for any radial target).

## T1a — does Theorem 1.1 extend to the settling problem?

- **No change of variables exists:** the L2(ρ) norm and W2 are not covariant under source rearrangements; the uniform-source hypothesis is structural, not cosmetic.
- **The uniform source is ESSENTIAL (any-power counterexample, verified):** source supported on the switching band {|x1| ~ a} (density zero on a positive-volume set) keeps |ΔT| = O(1) while W2 → 0 as a → 0: ratio |ΔT|/W2^{1/3} diverges ∝ a^{−1/2} (2.01 → 5.64 in the sweep). No W2^β bound holds for such sources. The manuscript's own extensions (Delalande–Mérigot, Duke 172:17: L2-map order W1^{1/6}, sources bounded above and below on convex domain; Divol–Niles-Weed–Pooladian, IMRN 2025: W2^{1/3}, regular sources + nondegenerate targets) still need a bounded-below source — our CFG375 fiction (uniform supply ball) is exactly this hypothesis.
- **Target truncation is required and harmless:** the phantom is not compactly supported (M_ph ∝ r deep-MOND, total mass diverges), so r_out = 818 kpc truncation + normalization are required for a probability target. With point baryons there is NO 1/r² cusp at r = 0: rho_ph → 0 in the Newtonian interior (peak near 2.4 kpc, 1/r² tail at r ≫ r_t); the freeze's unbounded-cusp picture is the deep-MOND idealization (its mass inside r_in would be 4.1e9 Msun vs the actual 2.5 Msun). M_ph(r_in)/M_ph(r_out) = 1e-13 — the inner cut discards nothing. C(K,Y) depends on the truncation only through L = r_out in the 28 L² P_K/|K| term: relative C* sensitivity ~6.5e-6 across L ∈ [0.5, 1.5]·r_out; C* is set by the source body (12d(1+√162)² R_K²).
- **Shape errors (T1b reconsideration):** a baryon-distribution shape error at fixed mass (5 kpc uniform ball vs point) moves the phantom by W2 = 0.026 kpc — the profile response is first-order and linear; the 1/3 exponent is the wrong stability statement for smooth radial profiles (their true response is |ΔT| = W2, exponent 1, and W2 itself scales with the perturbation, not its cube root).

## Screen (Q1–Q3)

- **Q1:** does it derive a0? **No** — a0 never appears; κ = 1/2 stays fitted.
- **Q2:** coefficient forced or chosen? **N/A** — no framework constant is produced; the stability constant C*(K,Y) is manuscript-side, not a framework quantity.
- **Q3:** base-rate null — **N/A** (no candidate constant); C3 reports the 1%-window share 0.224% (record ~0.2–0.3%), consistent with nothing being special.

## Honest bottom line

Theorem 1.1 bounds nothing the framework needs, and it forces nothing. Under the declared fictions (uniform supply-ball source, truncated normalized targets) its explicit constant is ~58× looser than the trivial bound 2L at the MW scale, and ~1e5× looser than the actual map change. What the lane established empirically: the settled profile of the MW-like host is stable to 0.1-dex baryon errors at the 0.4 kpc level (~0.05% of r_out) on both footings, because radial monotonicity makes the map change exactly W2 and W2 itself is a first-order, √M_b-scaled response (elasticity 0.496 confirmed). That stability is real physics of the framework's own profiles — it is not supplied by the one-third theorem. The cold fluid's mass is still required; the settling force (CFG60/CFG373/CFG381) stays open.

Files: `t1_fam374_brenier_stability.py`, `t1_fam374.out`, `t1_fam374_results.json` (main, rc 0), `t1_fam374_MUTATE.out`, `t1_fam374_results_MUTATE.json` (MUTATE, rc 1 as declared).