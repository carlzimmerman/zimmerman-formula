# CFG55 — the dynamical stellar-mass test: is the SLUGGS globular-cluster deficit a stellar-mass artefact?

Script: `CFG55_sluggs_dynamical_masses.py` (both footings; about 9 s). Its MUTATE control exits 1 as required. Outputs: `CFG55_sluggs_dynamical_masses.out` / `_results.json`, and the `_MUTATE` pair.

## Why

SLUGGS (CFG38) is the one population where B's derived cold-mass rule beats the bare law. With SLUGGS's own stellar masses, the law under-predicts the outer globular-cluster (GC) dispersions of 19 massive early types by +0.080 dex (3.3σ), and the rule's collapse debris closes the gap.

The standing objection is the stellar mass. CFG33 found that the law needs a stellar M/L of about 0.83–0.90 × Salpeter at σ_e = 200–300 km/s.

Here each model's stellar mass is fixed by the galaxy's own inner stellar kinematics (the ATLAS3D JAM mass inside the half-light sphere), and the same model then predicts the outer GCs. No IMF enters.

## Method (declared before the first run)

- **Machinery:** CFG38's, read-only. That is h50's GC dispersion bins; isotropic Jeans with a γ = 3 tracer; Hernquist stars with SLUGGS's R_e; the outer bins; CFG36's red collapse masses; the conservation form at x_e = 0.40; ν_mono. Hot gas is omitted, as in h50.
- **Dynamical mass:** ATLAS3D JAM (Cappellari+2013 XV), M_JAM = (M/L)_JAM L_r and r_1/2, both moved to the SLUGGS distance.
- **Calibration (CFG33's convention):** half the stars lie inside r_1/2, and the model's total mass there equals M_JAM/2. For the law that is ν(g_N/a₀) M_*/2; for the rule the debris inside r_1/2 is added.
- **Sample:** 16 of CFG38's 19; NGC 1400, NGC 1407 and NGC 3115 lie outside ATLAS3D's declination range. All 16 have JAM quality ≥ 1.

## Result

| | canonical | alt |
|---|---|---|
| **law, JAM-calibrated masses** | **+0.097 ± 0.024 (4.0σ)** | **+0.088 ± 0.024 (3.65σ)** |
| rule, JAM-calibrated masses | +0.046 ± 0.018 (2.6σ) | +0.047 ± 0.018 (2.6σ) |
| law, SLUGGS masses (same 16) | +0.077 (2.75σ) | +0.063 (2.2σ) |
| rule, SLUGGS masses (same 16) | +0.007 (0.4σ) | +0.002 (0.1σ) |

**Controls**
- **C1 passed:** CFG38's committed means reproduced to 1e-9.
- **C2 passed:** CFG33's committed law calibration re-derived with this script's own solver: slope +0.204, and ×0.72 / ×0.83 / ×0.90 at σ = 100 / 200 / 300 km/s (N = 187).
- **C3 failed as declared, and is kept.** h50's R_e differ from R_eff × D by up to 1.2e-5 kpc, against a 1e-6 tolerance. The cause is that h50 rounds the arcseconds-per-radian constant to 206265.0 where this script uses 206264.806, a 1e-6 relative difference; the distances are the same. The solver half of C3 passed exactly.

**Hypotheses**
- **H1 (headline) failed.** Calibrated on its own inner kinematics, the law under-predicts the outer GCs by +0.097 dex (4.0σ). The JAM calibration *lowers* the law's stellar masses (median −0.10 dex against SLUGGS's), because the law's own phantom supplies part of the mass inside r_1/2. So the deficit grows. The IMF objection runs the wrong way.
- **H2 failed.** The rule, calibrated the same way, leaves +0.046 (2.6σ). With SLUGGS's masses it closed the gap; with dynamical masses it closes about half.

**MUTATE** (JAM masses halved): the law's offset moves to +0.216 (9.1σ), and the script exits 1.
- The first MUTATE run crashed. For NGC 7457, the rule's clamped debris alone exceeded its halved JAM mass, so the solver had no root.
- The fix excludes any galaxy the rule cannot calibrate, with a printed note. It does not change the main numbers.

**Reported rows**

| Variant (canonical) | law | rule |
|---|---|---|
| Salpeter population masses | +0.049 (1.8σ) | −0.033 (−1.8σ, over-predicts) |
| Salpeter − 0.25 dex (Chabrier-like) | +0.129 (4.8σ) | +0.078 (4.3σ) |
| calibration with the Hernquist enclosed fraction at r_1/2 (0.28–0.57) instead of ½ | +0.087 (3.8σ) | +0.033 (1.9σ) |
| post hoc, disclosed: without NGC 7457 | +0.096 (3.7σ) | +0.047 (2.5σ) |

NGC 7457 is excluded in the last row because its rule-calibrated mass (10^9.62) lies below Mandelbaum's red range, where the collapse mass is clamped. Its f_ex = 0.57 is an artefact of the clamp.

## Reading

**The deficit survives dynamical stellar masses.** This is the declared reading. Massive early types want mass beyond the law at 5–15 R_e, and not because of the IMF. B's derived rule, calibrated the same way, supplies about half of it: the residual is 2.5–2.6σ, or 1.9σ under the Hernquist convention.

With SLUGGS's population masses the rule looked like a clean fit. With the galaxies' own dynamics it is marginal. Together with the massive passive disks leaning against the rule (CFG41, CFG53), **the rule no longer fits cleanly anywhere among massive passive systems.**

Three of the four worst offenders are X-ray-bright group or cluster centrals: M87 +0.27, NGC 5846 +0.21 and NGC 4374 +0.20 under the JAM-calibrated law. Two systematics remain unmodelled:
- **Hot gas.** It is omitted here as in h50 and CFG38, and is the baryonic component that could move these galaxies. That is the next test.
- **GC orbital anisotropy.** Isotropy is assumed.

κ = ½ and Ω_c h² stay fitted. Nothing here says the theory is closed.


## Corrections from the referee sweep (appended 2026-09-29; no result changed)

- **"Its MUTATE control exits 1 as required" says nothing here.** The main run also exits 1, failing the same three checks (C3, H1 and H2). What the control shows is the statistic moving: with the JAM masses halved, the law's offset goes from +0.097 to +0.216 (9.1σ).
- **Later: the measured hot gas does not change this deficit.**
  - CFG57 (9b071a024) is non-diagnostic: on the seven galaxies with X-ray profiles, the gas moves the law's mean by 0.010 dex.
  - M87's gas beyond its 30-kpc X-ray field is untested.
