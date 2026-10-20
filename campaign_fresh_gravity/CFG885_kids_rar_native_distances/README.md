# CFG885 — the KiDS lensing RAR results without B21's ΛCDM distances

Criteria: `FROZEN_CRITERIA.md` (10838b3c7, committed alone before the script). Run: `python3 cfg885.py` (MUTATE
`CFG885_MUTATE=1`). About 1 minute, one core. Owner block 880–889, agent lane.

**Question.** Brouwer et al. 2021 (B21) turned KiDS shear into excess surface density using distances from flat ΛCDM
(Ω_m 0.2793, H0 70; the ESD columns are in h70 units). Every KiDS lensing lane of the record uses those ESDs as released. Do
CFG829 / 840 / 849 / 850 / 851 survive when the framework-native background replaces B21's?

**How.** At fixed angle g_bar = G M_b/R² does not depend on the distances, because M ∝ D_L², R ∝ D_A and D_L = (1+z)² D_A.
So the g_bar bins and the law stay put. g_obs = 4G·ESD (B21 Eq. 7) has no radius term, so it moves by one factor per point:
T = (h/0.70)/⟨r⟩, where r = Σ_crit,native⁻¹/Σ_crit,B21⁻¹ is averaged over lens–source pairs with B21's weights w_s Σ_crit⁻².
- **Native background:** flat, with constant ρ_DE (flat a0 under the tracking law). Ω_m = 0.3085 ± 0.0075 (CFG682: BAO + SN,
  no CMB). h ∈ {0.674, 0.70, 0.73}, because the framework does not fix H0.
- **Sources:** KiDS-1000 SOM n(z), with B21's cut Z_B > z_l + 0.2. Two treatments of the source redshift were run (S1, S2).
- **Lenses:** photo-z of the record's 181,477-lens reconstruction of B21's sample (L1), or one lens z of 0.15, 0.25 or 0.35
  (L2–L4).
- **Bracket:** 72 points in all. T is applied to g_obs and to the covariance.
- **Code:** each lane's own code is exec'd unchanged, and its classification lines are copied verbatim.

## Result: **SHIFTED, SAME CLASS** (both footings)
At h = 0.70 and Ω_m = 0.3085, the native Ω_m alone raises g_obs by 0.7–1.5%, depending on lens redshift: +0.7% at
z_l 0.15, +1.5% at z_l 0.35. For the reconstructed lens sample it is +1.3% (+0.9% for the dwarf proxy). The unknown H0
dominates. Over the whole bracket T runs from 0.968 to 1.062.

| quantity (canonical) | B21 distances | native range (72 pts) | h 0.70, Ω_m 0.3085, L1 | alt footing range |
|---|---|---|---|---|
| A_blue | 1.016 ± 0.086 | 0.984–1.080 (≤ 0.74σ) | 1.030 | 0.898–0.985 (T=1 0.928) |
| A_red | 1.587 ± 0.076 | 1.536–1.686 (**+1.29σ** at h 0.73) | 1.607 | 1.401–1.538 (T=1 1.448) |
| A_all isolated | 1.439 ± 0.050 | 1.392–1.528 (**+1.80σ** at h 0.73) | 1.457 | 1.270–1.394 (T=1 1.313) |
| A_dwarf lenses | 1.397 ± 0.174 | 1.352–1.484 (≤ 0.50σ) | 1.410 | 1.233–1.353 (T=1 1.274) |
| dwarf ×2.75 excluded (blue) | 20.2σ | 18.4–21.3σ | 19.8σ | 21.3–24.5σ |
| CFG840 min exclusion over variants | 12.2σ | 10.8–13.0σ | 11.9σ | — |
| CFG850 red/blue split (+0.123 dex M★) | 3.98σ | 3.97–3.98σ | 3.97σ | 3.97–3.98σ |
| CFG849 colour split | 4.97σ | 4.95–4.97σ | 4.96σ | 4.95–4.96σ |
| CFG851 b (red, +0.123) | 0.0598 (1σ 0.050–0.070) | 0.0597–0.0598 | 0.0598 | 0.0587–0.0588 |
| CFG851 log g† | −10.05 (1σ −10.58..−9.29) | −10.29..−9.61 (≤ 0.58σ) | −9.95 | −10.92..−10.23 (T=1 −10.67) |
| CFG851 dSph z | +4.41 | +3.91..+4.69 | +4.31 | +4.05..+4.82 |

- **No classification flips at any of the 72 points, on either footing.** The classes that held are CFG829 LAW HOLDS AT LOW g
  (canonical and alt), CFG840 FRAGILE, CFG849 BOTH / DEGENERATE, CFG850 SPLIT SURVIVES and CFG851 DSPHS ABOVE (all four rows).
  CFG829's calibration-window check passes everywhere.
- **What moves ≥ 1σ:** A_all (up to +1.80σ) and A_red (up to +1.29σ). Both happen only at h = 0.73. At h = 0.70 every tracked
  amplitude moves ≤ 0.54σ, and at h = 0.674 ≤ 0.94σ. The excess of red and early-type lenses grows with H0: A_red runs from
  1.54 at h 0.674 to 1.69 at h 0.73. It never comes close to vanishing. Blue lenses stay within 1σ of the law throughout.
- **The splits do not move.** T is almost the same for red and blue lenses: their lens-z distributions differ by ≤ 0.1% in T.
  So the CFG849 and CFG850 split significances are unchanged to 0.01σ.
- **g† ≈ a0 flag: DISTANCE-DEPENDENT.** log g† − log a0 runs from −0.26 to +0.42 dex (canonical, M★-corrected). g† sits above
  every data point, so log g† shifts by log10(T)/b ≈ 17 log10 T. Its own 1σ, computed here for the first time, is wide: 1.3 dex.
  So the "onset near a0" coincidence in CFG851 was never sharp, and it is not a distance-robust statement.
- **Dwarf exclusion:** the dwarfs' ×2.75 stays excluded by isolated late types at ≥ 18σ. Across CFG840's variants and the full
  distance bracket it is ≥ 10.8σ. That replaces CFG840's "≥ 12σ" when the distances float.
- **B21's fiducial Ω_m (reported only):** moving it over 0.25–0.32 changes T(all) by 0.995–1.026 at h 0.70. No flips.

## Controls
- **K1 PASS:** with T ≡ 1 the driver reproduces every committed number in the five lanes' results JSON exactly (max |Δ| = 0),
  and every class string.
- **K2 PASS:** comoving distance matches the analytic Einstein–de Sitter form (≤ 1e-8) and pure Λ (exact). The pair ratio r
  matches astropy (independent code) to 2e-10. The radiation term changes T by < 1e-4 (7e-5). Two lines are code-path sanity
  checks only, not physics evidence: T(native = fiducial) = 1, and the g_bar identity, which holds by construction.
- **K3 PASS:** 5 SOM n(z) bins; 181,477 lenses (93,398 / 88,079 by type, as CFG61 C3).
- **MUTATE (T ≡ 1.3) BITES:** every A scales ×1.3 exactly. CFG829 blue flips LAW HOLDS → INTERMEDIATE (both footings), so the
  class is CHANGED as required. The CFG849/850 splits and classes are unchanged. CFG851 b is unchanged, and log g† shifts by
  log10(1.3)/b within 0.05 dex.

## Disclosures
- **Proxies.** Each lens subset is approximated:
  - blue/red use the reconstruction's LePhare u−r 2.0 label, not B21's 2.5;
  - disc/spheroid use the colour proxies, since there are no Sérsic indices on disk;
  - B21's dwarfs are taken as logM < 10, since B21's cut is not in the repo;
  - GAMA uses the KiDS all-lens z distribution.

  These enter only through the lens-z distribution. The spread across L1 subsets is ≤ 0.53% in T (dwarfs 1.009 vs blue
  1.013 at h 0.70), and the single-z envelope L2–L4 brackets them.
- **Source n(z).** The KiDS-1000 cosmic-shear SOM n(z) stands in for B21's source n(z). The Z_B cut is applied with Z_B uniform
  inside each tomographic bin. S1 and S2 differ by ≤ 1e-4 in T.
- **Selections not redone.** B21's selections are defined in fiducial units: isolation radius, mass and colour bin edges, and
  the 0.03–3 Mpc range. Native distances move radii by ≲ 0.02 dex and M★ by ≲ 0.03 dex. This is not modelled, because stacked
  public files cannot be re-selected.
- **Fiducial Ω_m source.** The fiducial Ω_m 0.2793 is confirmed only through the record's reading of B21 Sect. 3 (FP18, FP21).
  Hence the envelope above.
- **Hand expectations that missed.** MUTATE expected CFG851's dSph z at ≈ 2.5–3; it came out 2.35 canonical and 2.45 alt
  (DSPHS ABOVE held, as expected). The unshifted-mass CFG851 rows flipped to UNIFIED under MUTATE, and CFG829 alt flipped to
  INTERMEDIATE. Neither flip was predicted in the criteria, and both are consistent with +0.114 dex.
- **Nothing post-hoc.** The script was run once in each mode after the freeze, with no edits between runs.
- **Assumption.** Lensing is assumed to trace the dynamical g, as in CFG801–805.

κ = ½ fitted; cold energy mass required; not theory closed. Removing a ΛCDM input cannot favour the framework over ΛCDM.
