# RF3_cluster_keys_hse_free: ZN3'S X-COP PASS CAN'T BE CHECKED WITHOUT HYDROSTATIC MASSES ON WHAT'S ON DISK. ITS KEYS FAIL NARROWLY ON THE HSE-FREE GAS SCALE AT ONE f★. THE SMOOTH-CORE RULE STILL NEEDS EXTERNAL c_f ON eRASS1'S GAS

Criteria and ledger: `FROZEN_CRITERIA.md`, `ASSUMPTION_LEDGER.md` (e17dcb4e62), committed alone first. Script `rf3.py` (53e1aeeb64; one later fix below). Numbers: `rf3.out`, `rf3_results.json`, `rf3_inputs.json`, `runs/`. Control: `rf3_MUTATE.out`. Post-result, not graded: `rf3_post.py`, `rf3_post.out`.

The grader fix was already done and is cited, not redone: `NZ1_zoom_core_radius/nz1_one_template.py` (b62559a575), `BA2_one_template_reread/README.md` (0d72e260d8). ZN1 and ZN3 grade on one template from the start. No other lane's file was edited.

## Verdicts, as frozen
1. **ZN3's keys: FAILS ON THE HSE-FREE GAS SCALE: G-OUT-M3.** Narrowly, and at one f★ only (below).
2. **X-COP gate without HSE: UNDETERMINED: no clean HSE-free X-COP mass on disk.**
3. **External c_f:** on eRASS1's gas, **only c_f 4 passes** the 15 keys at all four f★, both footings. On X-COP's gas scale **neither c_f rule does**.
4. **No [F★-BAND-DEPENDENT] tag:** ZN3 on X-COP's scale keeps 15 of 15 and the X-COP line from f★ 0.024 to 0.136.
5. **No 5.364:** Ω_c/Ω_b is 5.2715 in every run, script grep empty, no line in the patched text holds it.

## ZN3's HSE question
**X-COP's gas scale itself used a hydrostatic radius.** SM1's +0.111 compares each survey's gas mass at its own R500, and X-COP's R500 is hydrostatic. Read from X-COP's gas profile at eRASS1's R500, the scale is **+0.092** (rows +0.047 to +0.138, rms 0.034).

| ZN3, 15 keys | f★ 0.034 | f★ 0.0615 |
|---|---|---|
| eRASS1's gas | 11, G-OUT-M3 +4.47 | 12, +4.19 |
| HSE-free scale, +0.092 | **14, G-OUT-M3 +2.03** | **15, +1.69** |
| X-COP's scale, +0.111 | 15, +1.46 | 15, G-IN-Mall −1.33 |

G-OUT-M3 reaches 2 at +0.093 dex, so the frozen fail sits on the line. The scale's own SE is 0.015 dex, about ± 0.45 in Z. Post-result: neither SM1 nor this lane converts eRASS1 to X-COP's h. If eRASS1 is at h 0.6774 (from memory, PROVISIONAL), Mgas500 alone would shift the scale by +0.036 dex, with a smaller opposite shift from the radius. So this is a knife edge, not a clean loss. The dependence on the overall gas scale, ZN3's first limit, stands: most of its 3 Z of swing comes from that one number, measured on 5 clusters, none in the lensing sample.

**No raw shear exists for X-COP's clusters.** ZW1215 is the nearest to KiDS DR4, with its first sources at 2.0 R₂₀₀; the rest are at 8.8 or more. So no X-COP shear profile can be measured from what's on disk. The 15 keys are raw shear and HSE-free, but on other clusters.

**X-COP's 7 clusters, labelled brackets only.** Published WL masses are NFW fits, and caustic masses rest on an F_β from ΛCDM N-body runs, so by rule 1 neither can be the graded value. Δ = log₁₀(M_pub/M_model), ZN3, f★ 0.034:

| Method | clusters | Δ median | SE | M_pub against M_FORW, same radius |
|---|---|---|---|---|
| WL (Umetsu+09, Okabe & Umetsu 08) | 1, A2142 | −0.043 | 0.113 | −0.010, +0.016 |
| LOSVD | 3 | +0.017 | 0.054 | +0.017, −0.034, −0.018, −0.166 |
| Caustic, Rines & Diaferio 06, h 0.7 | 3 | −0.335 | 0.020 | −0.259, −0.442, −0.335 |
| Caustic, same, h 1 | 3 | −0.223 | 0.021 | −0.157, −0.356, −0.222 |

Those caustic rows sit far below the hydrostatic masses too, so ZN3's offset there is mostly the caustic-to-HSE gap. The one WL cluster agrees with HSE. The h of those caustic rows isn't stated in what's on disk. Three clusters and one cluster don't test a 0.05 dex line.

**Wider sample, eRASS1 clusters matched to published masses (116 clusters, 303 rows).** These aren't X-COP's clusters. No distance-convention correction. Median Δ ± SE, f★ 0.034, canonical:

| Rule, gas | WL (29) | WL+SL (17) | Caustic (41) | LOSVD (21) |
|---|---|---|---|---|
| ZN3, X-COP's | −0.086 ± 0.027 NOT RESOLVED | −0.146 ± 0.039 OFF, heavy | −0.135 ± 0.048 NOT RESOLVED | +0.135 ± 0.045 NOT RESOLVED |
| ZN3, HSE-free | −0.066 ± 0.027 NOT RESOLVED | −0.126 ± 0.039 NOT RESOLVED | −0.115 ± 0.048 NOT RESOLVED | +0.159 ± 0.045 OFF, light |
| ZN3, eRASS1's | **+0.034 ± 0.028 AT THE LINE** | −0.029 ± 0.041 AT THE LINE | −0.010 ± 0.049 AT THE LINE | +0.281 ± 0.046 OFF, light |
| c_f 4, eRASS1's | −0.083 ± 0.028 NOT RESOLVED | −0.144 ± 0.037 OFF, heavy | −0.148 ± 0.045 OFF, heavy | +0.094 ± 0.041 NOT RESOLVED |
| Native c_f, eRASS1's | −0.127 ± 0.029 OFF, heavy | −0.190 ± 0.039 OFF, heavy | −0.190 ± 0.047 OFF, heavy | +0.064 ± 0.043 NOT RESOLVED |

**This cuts against ZN3's pass, and it's the main thing here.** The published WL and caustic masses put ZN3 at the line on eRASS1's gas, which is where its keys fail by 4.5. On X-COP's scale, where its keys pass, the same masses read it about 0.09 dex too heavy. Either the raw stacked shear and these published masses disagree, or the gas scale that fits one is wrong for the other, or the samples differ. They do differ: mostly massive lensing-selected clusters here. These are brackets, so this reading changes no class. But the pass isn't confirmed by HSE-free masses either. It's in tension with them at about 3 SE on WL.

Post-result: the caustic rows split by source. ZN3 on X-COP's scale is −0.198 ± 0.047 on HeCS and +0.086 ± 0.069 (h 0.7) or +0.208 (h 1) on Rines & Diaferio. On WL there's no redshift trend: −0.064 ± 0.052 below z 0.3, −0.078 ± 0.028 above.

## Keys, both footings
ZN3's keys are the same on alt; there's no a₀ in its halo. Hydrostatic X-COP line (bracket) beside them.

| Rule | gas | f★ 0.024 | 0.034 | 0.0615 | 0.136 | X-COP mean, rms at 0.034 |
|---|---|---|---|---|---|---|
| ZN3 | X-COP's | 15 | 15 | 15 | 15 | −0.004, 0.076 PASS |
| ZN3 | eRASS1's | 10 | 11 | 12 | 13 | same |
| Native c_f | X-COP's | 4 | 4 | 4 | 4 | −0.166, 0.191 FAIL |
| Native c_f | eRASS1's | 12 | 12 | 12 | 10 | same FAIL |
| c_f 4 | X-COP's | 11 | 9 | 8 | 6 | +0.020, 0.146 FAIL |
| c_f 4 | eRASS1's | 15 | 15 | 15 | 15 | same FAIL |

Worst, c_f 4 on eRASS1's gas: G-OUT-all −1.23 to −1.90, OVER. Native on eRASS1's gas: G-IN-Mall −2.94 to −3.05, then G-MID-T3 −3.60 at f★ 0.136, all OVER. On alt, X74's own list adds the SPARC line for both c_f rules (X78: the law's).

So c_f 4 still passes the keys only on the gas where it fails X-COP's hydrostatic shape, and native c_f is over on both. Grading X-COP on hydrostatic masses and the keys on eRASS1's gas, as earlier lanes did, is the mismatch ZN1 and SM1 flagged.

## Excess, Z = (A − 1)/s, band over f★ 0.024–0.136. No rule enters
| gas | footing | Z_MID, h 0.672 | Z_MID, h 0.686 | A_MID | Z_IN |
|---|---|---|---|---|---|
| eRASS1's | canonical | +3.61 to +3.91 | +4.01 to +4.30 | 1.69–1.89 | +1.01 to +1.30 |
| eRASS1's | alt | +3.14 to +3.45 | +3.54 to +3.85 | 1.55–1.73 | +0.94 to +1.22 |
| X-COP's | canonical | +2.81 to +3.15 | +3.22 to +3.56 | 1.46–1.63 | +0.89 to +1.16 |
| X-COP's | alt | +2.26 to +2.64 | +2.68 to +3.05 | 1.34–1.50 | +0.81 to +1.07 |

The law's core excess stays at every cell. No hydrostatic mass enters it, so it isn't an HSE artefact. It falls with more gas or stars but doesn't close. X11's 5.21 / 5.47 and 4.47 / 4.74 are on statistical errors at f★ 0.20; these use the grader's s, which is larger, so they're not a like-for-like drop.

## Limits
- ZN3 was chosen after ZN1, at ng 64, collisionless, with its thin outer shell. It's not a blind pass.
- eRASS1's M500 and R500 are WL-calibrated inside a ΛCDM count fit, and they set key bins and R500. XF reads gas at that R500. It's free of hydrostatic masses, not of every outside calibration.
- The f★ factors 0.7, 1.7, 1.3 are from memory; no ICL table is on disk.
- K5: the grader's baryons sit below the measured gas + stars at X-COP's rows by 0.27 dex at 0.1 R500, 0.03 at 0.7 R500. No row reaches R500, so K5's frozen test at r ≥ R500 is not directly tested. Baryons are about 15 % of the mass at r₂₀₀, so the bracket rows move little.
- Groener's table has no caustic errors. M₂₀₀ extrapolates or interpolates NFW. SE is from cluster scatter.
- Script fix before any comparison number was read: A1644 has no stellar file and isn't in the grader's 7, so its one row is dropped from the X-COP-7 tables.

## What's needed for a clean X-COP gate
Non-parametric: tabulated tangential shear or aperture masses for these clusters (from memory, PROVISIONAL: CCCP/MENeaCS for some, DES or HSC for others), and CIRS's tabulated caustic profiles with their h (J/AJ/132/1275). Also eRASS1 clusters' own X-COP-style gas profiles, or more than 5 matches, to fix the scale; and an h-consistent restatement of SM1.

## Checks
K1 ZN3 against `zn3_results.json`, |d| 0. K2 c_f 4 against X73, |d| 0, G-OUT-M3 +1.036, +0.733 (BA2 +1.04, +0.73). K3 native against X77's A4 grade, |d| 0. K4 M_h against the grader's rows, |d| 0. Template independent of the rule, |d A_MID| 0. MUTATE (r × 1.5, M_pub × 2): K1 |d| 1.486, X-COP rms 0.076 to 0.224, G-IN-Mall +1.49, Δ +0.301: BITES. 29 grader runs at about 40 s, RSS under 0.65 GB; three workers, one thread, nice 15.

    python3 rf3.py --inputs; python3 rf3.py --run; python3 rf3.py --grade; RF3_MUTATE=1 python3 rf3.py --run; RF3_MUTATE=1 python3 rf3.py --grade

κ = ½ FITTED; c_f EXTERNAL where used; cold dark energy is a gravitating field component, never a particle; not theory closed; nothing here says the data favour the framework.
