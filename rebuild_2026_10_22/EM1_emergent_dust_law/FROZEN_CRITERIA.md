# EM1_emergent_dust_law — FROZEN CRITERIA (committed with ASSUMPTION_LEDGER.md, before any script or number)

κ = ½ FITTED. Footings a₀ = 9.3603e-11 (canonical) / 1.1312e-10 m/s² (alt), never pooled. No dark-matter particle (§5
says what the dust's multistreaming requires). Not "theory closed". Nothing here says the data favour the framework.
Compute: one thread, `nice -n 15`, < 1 GB RSS, minutes, beside the live L1 384³ job. No downloads. Other lanes read-only.

## 0. The question

The v3s verdict (`covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md` §6) leaves two roads: a genuinely new
mechanism (PH1_two_phase_cold_energy, another session) or **route E: the cold sector clumps like dust everywhere, there
is no law force, and the RAR is an emergent regularity of where dust sits around baryons.** Route E passes clusters,
growth/CMB, the radiation era, hosted dwarfs and TDGs by construction, because its cold sector is ΛCDM's. This lane asks
the two things route E has not been asked framework-natively:

1. Does dust alone (no abundance matching, no ΛCDM-calibrated stellar-to-halo relation) reproduce SPARC with the SAME
   per-galaxy freedom the law uses (one Υ each)?
2. What survives of the framework's own content, a₀ = κc√(Gρ_Λ)?

The record's ΛCDM versions (CFG476 DMO FAILS 0.205 dex; CFG477 DC14 MARGINAL 0.120; CFG545 s ≤ 0.16; CFG565 g†(z) rises)
used Moster+13 abundance matching and Dutton–Macciò c(M). EM1 replaces both by the record's own refit background and a
SPARC-internal global halo relation.

## 1. Theorem T0 (sympy, in the script)

Route E's galaxy-scale dynamics are Poisson + collisionless dust in FRW: constants {G, H(z), Ω_i} plus each system's own
mass M. Solve for exponents of G^α M^β H^γ with dimensions of acceleration: the solution must be unique and depend on M.
Hence a universal acceleration carrying c to the first power (κc√(Gρ_Λ)) cannot come out of route E's equations; any match
at z = 0 is a coincidence, and κ stops being a constant of nature. PASS iff sympy returns exactly one solution with β ≠ 0.

## 2. Inputs

- SPARC: 175 rotmod files + `SPARC_Lelli2016c.mrt`, P4's loader, mask, weights W, Υ grid 0.30–1.20 step 0.01, bulge 1.4Υ.
- Reference baryonic mass (relation axis only, never fitted): M_b,ref = 0.5 L36 + 1.33 M_HI.
- Backgrounds A (C2 c2b refit) and B (CFG886), parameters from F3 `f3_growth_audit_results.json` K2. CLASS linear P(k),
  σ(M) by top-hat integral, D(z) from CLASS.
- Halo: NFW in M200c; concentration c(M, z) by Bullock+01: c = K (1+z_c)/(1+z), σ(F M, z_c) = 1.686, K = 4, F = 0.01.
- Secondary profile (EXTERNALLY CALIBRATED, reported separately): DC14 (Di Cintio+14) with X = log₁₀(M★/M200),
  M★ = Υ (L36_disk+bulge) (Υ is the galaxy's fitted value), its c boost, X clipped to [−4.1, −1.3] (fraction reported).

## 3. Rows

**R1 (primary, same-freedom RAR).** log₁₀M200 = a + b (log₁₀M_b,ref − 10), one global (a, b) per background, c on the
median Bullock relation (no scatter). g_pred = g_bar(Υ) + g_halo(r). Per galaxy best Υ by P4's weighted mse; pooled
statistic exactly P4's `pooled` rms and median Υ. (a, b) = minimiser of the pooled rms on a ∈ [10.0, 13.5] step 0.02,
b ∈ [0.0, 2.0] step 0.02 (two global fitted constants, declared like κ; edge hit reported). **Line (P4's): rms ≤ 0.110 dex
AND median Υ ∈ [0.50, 0.80].** R1 PASS iff the line holds on both backgrounds. Disclosed flag: fraction of galaxies with
M_b,ref > f_b M200 (f_b = ω_b/(ω_b+ω_c)); if > 10 %, PASS becomes CONDITIONAL. Same-freedom comparison reported:
Δrms = rms_E − rms_law (law per footing, P4's numbers reproduced).

**R1-DC14 (secondary).** As R1 with the DC14 profile. Same line. Labelled EXTERNALLY CALIBRATED (hydro feedback fit).

**R2 (allowed, diagnostic).** Per galaxy free log₁₀M200 on [8, 14] step 0.02 and c × 10^(0.055 k), k = −4…4 (±2σ of dust
c scatter 0.11 dex), M_b,ref ≤ f_b M200 imposed. Reported: rms, median Υ, line. And the scatter the RAR demands of route E:
sd of (log M200_free − R1 relation) over galaxies with interior optima.

**R3 (emergent scale).** On R1's best model (each galaxy at its R1 Υ), pooled points (g_bar, g_pred): fit g† in the law's
form g = g_bar ν_e(g_bar/g†), ν_e from μ = x/(1+x), weighted least squares in log g. Same fit on the data points at the
same Υ. Also per tercile of M_b,ref, and the low-g slope (OLS of log g on log g_bar for g_bar < 1e-11). **Class
EMERGES iff |log g†_model − log a₀| ≤ 0.10 on both footings AND |drift_model − drift_data| ≤ 0.10 dex** (drift =
max − min tercile log g†). Otherwise DOES NOT EMERGE (named part).

**R4 (redshift, the framework's distinctive claim).** Halo characteristic acceleration g₋₂ = G M(<r_s)/r_s² at fixed
M200 = 1e11 and 1e12 M_⊙, ratio z = 2.33 / z = 0 from the same c(M, z) and ρ_crit(z). Framework: a₀(z)/a₀(0) = 1.00
(exact Λ) or 0.91–0.94 (CFG689 native band). **Class DISTINCT iff the ratio lies outside [0.80, 1.25] for both masses
and backgrounds.** Halo-only; the record's feedback estimate (CFG565, ×2.8 at z = 2) is context.

## 4. Overall verdict

- **ROUTE E VIABLE AS DUST**: R1 PASS (or CONDITIONAL by the f_b flag only);
- **ROUTE E NEEDS FEEDBACK**: R1 fails, R1-DC14 passes;
- **ROUTE E FAILS ON SPARC**: both fail.
Plus, whatever the class, the framework-content statement from T0, R3, R4.

## 5. Not computed (stated)

Dust that multistreams is either collisionless matter or a classical wave field (L374, `feedback_no_dark_matter_particle`);
a wave field adds its wave scale as a new constant. Clusters, growth/CMB, radiation era, hosted dwarfs, TDGs: route E
inherits ΛCDM's sector, so these are "pass by construction", not framework results. Solar System: no law force, passes.

## 6. Checks and `--mutate`

`em1_emergent.py` prints `K* PASS/FAIL`, exit 0 iff all pass: **KT** T0; **KP** law reproduction (P4 iso_perUps rms
0.054087 / Υ 0.52 canonical, 0.053718 / 0.44 alt; rms to 1e-4, Υ exact); **KC** own σ8 vs F3 K2 within 1e-3 (A, B);
**KN** NFW and DC14 M(<R200) = M200 to 1e-3; **KH** R1 rms < Newtonian (no halo, own best Υ) rms − 0.05; **KR** RSS < 1 GB.
`--mutate`: halo mass multiplied by 0 → KH must FAIL (exit 1). Outputs `em1_emergent{,_MUTATE}.out`,
`em1_emergent_results{,_MUTATE}.json`.

## 7. Stop rule

No scans beyond the declared grids; (a, b) are fitted globals, declared. Post-result changes go in a dated AMENDMENT.
