> ⚠️ **AXIS-1 NUMBERS SUPERSEDED (2026-06-10, `agentH_perclass_C.md`).** The "erodes to 5.0σ (u−r) / 2.1σ (Sérsic)"
> survival figures below used a GENERIC concentration bracket whose premise fails when measured: with per-class halo
> properties from our own lens catalog (9 SHMR × c(M,z) configs), the type-differential is ΔlogC ≈ +0.001 dex —
> ~100× smaller and OPPOSITE-SIGNED (split-strengthening, 14/15 bins). **Refined survival: 8.6–9.2σ (u−r), 5.6–6.3σ
> (Sérsic); both axes corroborate; the Sérsic axis is NOT conversion-limited; the exposure HARDENS.** The bracket
> rows below stand as the audit trail of an escape route that was over-generous and is now closed by measurement.

# Lensing-RAR battery — results (LR, on Brouwer+2021's released ESD profiles)

*C. Zimmerman, 2026-06-10. Bound by `lr_preregistration.md` (hostility INVERTED). Ran on the public ESD release
`brouwer2021_rar.tar` (kids.strw.leidenuniv.nl/sci_data; DOI pinned in `lr_data_acquisition.md`), Fig-8 u−r colour split
(`Colorbin_1`=late/u−r<2.5, `Colorbin_2`=early/u−r>2.5) + the 30×30 joint covariance. Scripts: `esd_conversion.py`,
`lr_battery.py` (+`.out`). **This audits the framework's strongest STANDING EXPOSURE and the result is framework-UNFAVOURABLE
— reported at full weight, per the project's #1 rule (a "fails" verified as hard as a "works").**

## Replication — validated point-by-point (stronger than the pre-registered σ gate)
Because Brouwer released the measured profiles, fidelity is checked profile-by-profile, not by a reproduced σ. The early/late
split, computed with the full released covariance: **χ² = 119.9 (15 dof) → 8.8σ**, with **early types above late in all 15/15
g_bar bins**, mean offset **+0.261 dex in g_obs**. Consistent with (and slightly stronger than) Brouwer's "≥6σ"; the exact
number depends on the statistic, but the **direction and point-by-point structure validate exactly**. Early types are
**baryon-deficient** on the RAR (excess g_obs at fixed g_bar) — the direction the gas escape would need to fix.

## Axis 1 — the ESD→g_obs conversion is profile-laden and type-differential
Brouwer convert with the single SIS value **g_obs = 4·G·ΔΣ**. But C ≡ g_obs/(G·ΔΣ) is profile-dependent (`esd_conversion.py`,
validated: point-mass → π, SIS → 4, NFW crosses ~4.0 near R/r_s≈2; realistic R/r_s∈[1,10] → C = 4.33→3.53). Early types are
**more concentrated** → larger effective R/r_s → **smaller C** → lower inferred g_obs. Applying this **differentially**:

| C_early, C_late | Δlog C | split σ |
|---|---|---|
| 4.0, 4.0 (baseline) | 0 | **8.8** |
| 3.53, 4.33 (physical: early x~10 vs late x~1) | −0.089 dex | **5.0** |
| 3.43, 4.76 (aggressive) | −0.142 | 3.0 |
| π, 4.76 (extreme/implausible) | −0.180 | 1.9 |

**A physical concentration differential erodes the split 8.8σ → 5.0σ — a real, ~0.09 dex systematic — but does NOT remove it.**
Only an implausible point-mass-early differential kills it. (Same structural flavour as the wide-binary threshold finding: the
measurement's theory-ladenness audited symmetrically — here it cuts ~3.8σ off the exposure, honestly recorded.)

## Axis 2 — the gas escape requires M_gas≈M\* differentially, which eROSITA now disfavours
Closing the (residual) split by adding CGM baryons to early-type g_bar requires a **differential M_gas/M\* ≈ 1.1** (median over
bins; per-bin scattered 0–4, slope-dependent) — **independent convergence on the authors' own "M_gas ≈ M\*" arithmetic.** The
2026 advantage: **eROSITA eRASS stacking (Zhang+2025, Paper III), which postdates Brouwer**, finds **"no significant differences
in the hot CGM X-ray emission" between quiescent (early) and star-forming (late) galaxies BELOW log M\*=11.0** — exactly Brouwer's
M\*<10¹¹ regime. A differential appears only above 10¹¹ (~3× L_X) and is **halo-mass-driven, not intrinsic CGM** (equal at fixed
halo mass). **So the differential M_gas/M\*≈1 the escape needs is ~an order of magnitude above what the data permit here.** The
authors' 2021 hedge ("corrections likely moderate") is now quantified against data they did not have: **the gas escape is disfavoured.**
*Both-ways caveat:* eROSITA traces the **hot** phase only; a cool/warm-gas differential is not directly excluded — but it is not
independently motivated and would itself need to be ~M_gas=M\* differential to work.

## Verdict — **Outcome A: the exposure HARDENS** (with a residual-C caveat)
- baseline **8.8σ** → physical conversion differential **5.0σ** (survives) → gas escape **disfavoured** by eROSITA.
- ⇒ the early/late RAR split **hardens the falsifier AGAINST property-independent modified gravity** — which includes this
  framework, whose force law is universal and type-blind, so it predicts ONE RAR regardless of morphology.
- **Locked wording (per the MICE-vs-BAHAMAS enrichment):** this is an exposure to the **framework**, *not* "ΛCDM confirmed" —
  Brouwer's own simulations (MICE vs BAHAMAS) disagree with each other about the split, so no single dark-matter model is
  validated by it. The honest statement is "property-independent modified gravity cannot make this split; the split is real and
  survives its most plausible systematics."
- **a₀-independent:** the split is type-dependence at *fixed g_bar* (the released x-axis), so it does not involve a₀ at all —
  no binning-scale freedom to appeal to (cf. the WB note's a₀-insensitivity check, here automatic).

## Sérsic-split cross-check (run 2026-06-10, `lr_sersic_crosscheck.py`) — both-ways, moderates the verdict
The second independent morphology axis (threshold n = 2.0, recovered from the covariance bin-edges, as u−r = 2.5 was):
**baseline 5.8σ (χ²=69.1/15), early above late in 15/15 bins, +0.185 dex** — the split's *existence and direction* are
**classification-robust** (both proxies, all bins). **But the conversion-differential erosion is axis-dependent:** the same
physical (C_early, C_late) = (3.53, 4.33) that leaves u−r at 5.0σ leaves Sérsic at **2.1σ** (aggressive → 0.6σ) — and the
n-split is precisely the axis where the conversion systematic is most directly motivated (Sérsic index *is* concentration).
Gas axis a fortiori: closing the Sérsic split needs differential M_gas/M\* ≈ 1.47 (> the u−r 1.09), which eROSITA disfavours.
**Per-axis verdict: u−r = Outcome A (hardens, 5.0σ surviving); Sérsic = Outcome C (partial survival, ~2σ residual,
conversion-limited).** Referee-grade summary line: *the early/late RAR split survives the type-differential ESD→g_obs
conversion systematic at 5.0σ (u−r) / 2.1σ (Sérsic).* Next refinement (not run): per-class C from the actual R/r_s
distributions in the lens catalog — the bracket may be generous to u−r and conservative to Sérsic, or vice versa; noted both ways.

## What remains (does not change the sign, may change the magnitude)
- **Satellite-fraction (Axis 3)** and **full sphericity/profile (Axis 4)** beyond the C-bracket — secondary; the isolation cut
  bounds satellites, and Axis 1 is the leading conversion term.
- **Independent shear re-measurement** (the 16 GB SOM-gold stack) — validates the released profiles from scratch; demoted to
  cross-check per Fable's reorder. (Download stalled at 0.37 GB; restart as the independent track.)

**Bottom line:** the program audited the single strongest piece of standing evidence *against* the framework with the same
pre-registration + hostile discipline that closed the wide binaries — and found it **hardens**. The lensing-RAR early/late split
is real at 8.8σ, survives a physical conversion-factor differential at 5.0σ, and its named CGM-gas escape route is disfavoured by
post-2023 eROSITA. This is the program's most significant framework-unfavourable result, and it is recorded as such.
