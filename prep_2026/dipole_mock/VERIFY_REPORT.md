# VERIFY_REPORT — dipole_mock adversarial verification

**Verifier run date:** 2026-07-16
**Target:** `dipole_mock.py` / `dipole_mock_results.json` / `full_run.log` (oriented halo-lensing EFE kill-switch, m=1 phantom-dipole channel)
**Self-reported verdict under review:** NO-GO on both a0 footings (canonical 9.36e-11, alt 1.13e-10); ~2σ MARGINAL at LSST depth.

## VERDICT: **UPHELD** — NO-GO on both footings, with the LSST-depth "MARGINAL" softened to "marginal-at-best (~1.8–2.5σ across seeds, straddling the 2.0 bar)."

No manufactured deficit found. No manufactured win found. Every load-bearing number reproduced independently.

---

## 1. Reproduction

- Fresh run in an isolated scratch copy, **with the template cache deleted** (forcing full template regeneration): exit 0, runtime 178 s.
- Regenerated `dipole_templates.npz`: **bit-identical** to the shipped cache (max rel dev = 0 on S0,S1,S2,K1,K2) → no cache poisoning.
- Regenerated `dipole_mock_results.json`: **0 mismatching numeric fields** vs the shipped JSON (seeds are content-hashed per config; run is deterministic).
- All 9 built-in validations pass at the logged values (iso 1.8e-5, far-field 8.3e-7, FFT 3.4e-6, attractor m=1 = 0, noise-estimator Var ratio 1.009).

## 2. Injected amplitude — independently re-derived (the deflation/inflation traps)

**Σ_crit (verifier's own scipy.quad integrator, own constants):**

| config | verifier Σ_cr (kg/m²) | mock |
|---|---|---|
| z_l=0.3, z_s=5 (Oria's actual config — the paper uses z_s=5, not 0.8) | 4.466 | 4.47 (0.1% agreement) |
| z_l=0.03 / 0.05 / 0.07, z_s=0.7 (mock low-z) | 29.53 / 18.81 / 14.28 | matches per-lens `Sigma_cr(zl, 0.7)` |

The low-z efficiency penalty (same Σ produces 3.2–6.6x less κ than at Oria's config) is **real physics, correctly applied per lens** — not a deflation device. Single-source-plane z_s=0.7 vs a proper ⟨Σ_cr⁻¹⟩ over a KiDS-like n(z): agreement to 1.3% (mock very slightly optimistic — negligible).

**Template amplitude vs the Oria anchor:** mock κ_min(NGC5055 config) = −2.62e-3 vs paper "order −1e-3" — the mock's injection is **2.6x LARGER than the published value**, i.e. generous toward GO, not deflated toward NO-GO. Verifier's independent recomputation of the same closed form (own code): κ_min = −2.36e-3 (10% agreement; residual = map-scan granularity). Truncating the phantom source at Oria's refined-cube scale (R=200 kpc) gives −1.83e-3, at 500 kpc −2.29e-3 → the gap to the paper is substantially **Oria's finite 400-kpc box** (+ exponential disk vs point mass + 800-pc grid), not an error in the mock. Both directions are bracketed in the mock itself: the pessimistic paper-anchored rescale (`oria_cal_x0.38`) gives S/N ≈ 0.00, the un-rescaled (larger) baseline still fails. Extreme-config ratio 2.73 vs paper ~3 — consistent. a0-proportionality of the template verified to 2e-13 (VAL g), so the canonical/alt footing scaling is exact.

## 3. Shape-noise floor — independently re-derived

Median lens (M=3e10 M_sun, e_N=0.0064, z_l=0.057, canonical a0): r_ef = 80.2 kpc → θ_ref = 1.21 arcmin. Per-annulus σ(a₁) = √2·0.27/√(6.2·area): 0.59 (innermost, cut) down to 0.038 (outermost) — against a peak gt-dipole signal of 2.5e-4. Per-lens S/N ≈ 0.003.

**Independent GLS Fisher forecast (verifier's own lens draw, own cosmology, mock's templates):**

| N (canonical) | verifier σ_A (3-template) | mock sigA_med | verifier expected S/N (=0.886/σ_A) | mock SN_med |
|---|---|---|---|---|
| 1e4 | 3.041 | 3.048 | 0.29 | 0.26 |
| 3e4 | 1.754 | 1.758 | 0.51 | 0.54 |
| 1e5 | 0.964 | 0.963 | 0.92 | 1.03 |
| 3e4 alt footing | 1.598 | 1.603 | — | 0.34 |
| 1e5, n_eff=27 (LSST) | 0.451 | 0.450 | 1.97 | 2.01 |

Match to <1% everywhere; √N scaling internally exact. **Nuisance-marginalization penalty is only 1.10x** (t_M–infall corr −0.36, t_M–gradient corr +0.40) — the NO-GO is NOT manufactured by template degeneracy. The nsrc≥3 inner-bin cut costs only 3% in σ_A — not a deflation device either. Implication of the arithmetic: GO (capped S/N ≥ 3) at KiDS depth needs ~1.1e6 low-z lenses (more than exist at z=0.03–0.07 over 18 000 deg²; supply ≈ 1–2e5); at LSST depth ~2.3e5 — above the plausible all-sky supply.

## 4. Estimator honesty, null, and confound switches

- **No truth labels in the fit** (code read): design matrix X1 = [t_M, t_inf, t_grd] built from in-principle observables only; `dphi` (true PA error), `eps` (true subtraction residual), and `mond_on` enter the DATA only (lines ~481–492), never the fit.
- **Zero-injection null** (LCDM, infall=0, eps=0, N=3e4, 60 realizations): A_M = −0.33 ± 1.74, S/N = −0.19, false-positive(2σ) = 3.3% — recovers zero.
- **Direction-cone dilution applied:** paired on/off test (identical RNG stream, dphi zeroed post-draw): A_M ratio 0.903, S/N ratio 0.903 vs expected ⟨cos δφ⟩ = 0.886. S/N moves UP when cones are perfect, by the right amount.
- **Attractor-shear residual applied:** `t_grd·eps·c1` confirmed in d1; sweeping eps 0→1 leaves A_M unbiased (+1.052→+1.053) — absorbed by its fitted template, cost paid in the 1.10x marginalization penalty. Correct GLS behavior.
- One inflation-side caveat (favors GO, so it only strengthens NO-GO): per-lens template mis-estimation (errors in e_N, M, inc from real catalogs) is not modeled; real S/N would be somewhat lower than the mock's.

## 5. Pre-registered thresholds

- prep_2026 is **not a git repo** — no VCS history to audit; file mtimes show a single build (py+npz 09:31, json+log 09:34).
- Internal evidence against tuning: docstring thresholds (lines 49–54) match the stage-5 verdict code (lines 609–618) exactly; the achieved values sit **nowhere near any boundary** (best capped S/N 0.54 vs GO bar 3.0; baseline 1e5 capped 1.03 vs MARGINAL bar 2.0). You cannot tune a threshold to produce a miss by a factor of 6.
- The one boundary-hugging number — LSST variant 2.007 vs the 2.0 bar — is **outside the formal verdict** (variants don't enter stage 5). Verifier seed re-runs: 1.81 / 2.38 / 1.94 / 2.45 (mean ≈ 2.1). So "MARGINAL at LSST depth" is fair but soft: read it as ~2σ ± 0.3, sometimes under the bar. sign_frac there is 0.93–1.00.
- Nit: the workflow summary described the bar as "sign separation ≥ 3σ"; the script's actual pre-registered gate is sign_frac ≥ 0.95 + LCDM fp ≤ 10% (the ±separation, max +1.35σ at 1e5, is a reported diagnostic). All clauses fail regardless.

## 6. Bottom line

The m=1 phantom dipole is genuine QUMOND physics (closed form validated against Oria Eq 10, the Bilek bicone, and Oria's computed κ maps — the sign is AWAY from the attractor as Bilek claims), and the mock, if anything, injects it at 2.6x the published Oria amplitude. It still lands a factor ~6 below the pre-registered KiDS-depth detection bar at any feasible N, on both a0 footings, with an honest estimator, an honest noise floor, and only a 1.10x nuisance penalty. **NO-GO (both footings) UPHELD; LSST-depth prospect = soft ~2σ marginal, not a detection path at N ≤ 1e5.** The forward path, if any, is LSST-depth sources + pushing the low-z lens sample toward ~2.5e5 (at or beyond the all-sky supply) — or a different observable.

**Verifier artifacts** (scratchpad, session-local): `indep_sigmacrit.py`, `oria_truncation_test.py`, `indep_fisher.py`, `rerun/null_and_variants.py`, `rerun/paired_dilution.py`, `rerun/rerun.log`.
