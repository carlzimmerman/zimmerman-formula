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


## Corrections after CFG76's independent re-derivation (appended 2026-09-29; no committed number changed)

CFG76 (276c78784) re-derived this lane from independently written code. It reproduced the headline exactly: law +0.09698 (3.99σ) and rule +0.04564 (2.58σ), to 2e-6 per galaxy. It also found four problems, each checked here against this lane's code.

- **The kernel.** The prediction uses h50's plain RAR kernel, ν = 1/(1 − e^{−√y}) (`nu_h`, from h50 through CFG38), not ν_mono as the Method says.
  - ν_mono enters only the calibration (`law_mass`). There it equals the RAR kernel for y < 2.
  - With ν_mono everywhere, the offsets are about 0.001 dex higher (CFG76). The conclusions are unchanged.
- **The distance.** The code rescales M_JAM ∝ D and r_1/2 ∝ D (the `G16` block). That is the dynamical-mass scaling, since (M/L)_JAM ∝ 1/D and L ∝ D².
  - The Method's "M_JAM = (M/L)_JAM L_r and r_1/2, both moved to the SLUGGS distance" reads as L ∝ D² at fixed M/L. The code does not do that.
  - That literal reading gives +0.098 / +0.047 (CFG76's frozen primary).
- **The Salpeter row was undefined.** It takes ATLAS3D's (M/L)_Salp × L_r, moved at fixed M/L (L ∝ D²), and uses it directly as the stellar mass, with no kinematic calibration. That gives law +0.049 and rule −0.033.
  - CFG76 used the same mass as the calibration target in place of M_JAM, and got +0.076 / +0.021.
  - `CFG55_salpeter_definition_check.py` (and its `.out`) reproduces both from this lane's own functions. Neither is an error.
- **Post hoc: the size of the residual rests on the fixed GC density slope, γ = 3.** The 4.0σ and 2.6σ are statistical errors at one slope used for every galaxy. The values below are from CFG76 (`cfg76_posthoc_attack.py`, `posthoc_attack.log`):

| γ | 2.0 | 2.4 | 3.0 | 3.6 |
|---|---|---|---|---|
| law | +0.017 (0.7σ) | +0.053 (2.2σ) | +0.097 (4.0σ) | +0.134 (5.5σ) |
| rule | −0.046 (−2.5σ) | −0.005 (−0.3σ) | +0.046 (2.6σ) | +0.087 (4.9σ) |

  - The law's offset is zero at γ ≈ 1.83, and the rule's at γ ≈ 2.45.
  - Without the four group and cluster centrals (M87, NGC 4365, NGC 4374, NGC 5846; N = 12), the law is at +0.055 (2.7σ) and the rule at +0.026 (1.3σ).
  - Per-galaxy measured GC density slopes would decide this. None are used here.
- **h50 silently drops NGC 720 and NGC 821** (133 GC velocities). It keys galaxies as `NGC0720` but reads the catalogue's `NGC720_…`. This lane's SLUGGS-table key has the same inconsistency.
  - A disclosed re-run goes through this lane's own code: `CFG55_h50_keyfix.py`, with outputs `_H50KEYFIX`. It corrects the keys in memory; h50, CFG38 and this script are unchanged on disk.
  - The JAM sample becomes 17 (NGC 821 added; NGC 720 lies outside ATLAS3D). **Law +0.0996 ± 0.0230 (4.3σ; alt 3.97σ); rule +0.0513 ± 0.0176 (2.9σ; alt 2.9σ).** CFG76's independent code gives +0.100 / +0.053.
  - With SLUGGS masses over 21 galaxies: law +0.0799 and rule +0.0109, against +0.0795 and +0.0066 for the committed 19.
  - In the variant, C1 and C3 fail by construction because the sample changes. The H1 and H2 labels still say "16".
  - h50 itself is left as committed, so every lane that executes it (CFG38, CFG55, CFG57, CFG59, CFG69, CFG71, CFG76) stays reproducible. Correcting h50 in place would change all of them.

**Reading, as qualified:** the deficit survives dynamical stellar masses at γ = 3. Its size depends on γ, and it leans on the group and cluster centrals.
