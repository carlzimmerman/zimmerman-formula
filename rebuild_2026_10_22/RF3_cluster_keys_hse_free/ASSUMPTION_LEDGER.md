# RF3_cluster_keys_hse_free: ASSUMPTION LEDGER (committed with the criteria)

| input | value or source | class | role |
|---|---|---|---|
| KiDS DR4 shapes, X7's stacks | `X7_cluster_core_significance` | RAW | all 15 keys' measured amplitude |
| KiDS m-bias, n(z) calibration | X7 ledger | SURVEY-CALIBRATION | keys |
| eRASS1 Mgas500 | Bulbul+24 | RAW (X-ray, fit with a β-like form) | gas E |
| eRASS1 M500, R500 | WL-calibrated scaling, in a ΛCDM count fit (Ghirardini+24) | ΛCDM-PROCESSED, labelled | key bins, R500; no clean replacement on disk |
| X-COP gas profiles | Ghirardini+19 files on disk | RAW | gas X, XF, slope |
| Gas slope to r_ta, 2.7774 | GS1 | RAW, extrapolated past x ≈ 1.5–2.1 R500 | every rule |
| SM1 +0.111 dex | SM1 | RAW difference, uses X-COP's hydrostatic R500 | gas X |
| XF | this lane, X-COP gas at eRASS1's R500 | RAW + ΛCDM-PROCESSED radius, no HSE | gas XF |
| f★ 0.034 | CFG408/CFG922 A1 | RAW light + assumed Υ | band |
| f★ 0.0615 | X-COP-7 Ghizzardi+20 | RAW light + assumed Υ | band |
| × 0.7, × 1.7, × 1.3 | from memory | LITERATURE-INPUT, PROVISIONAL | band edges |
| Ω_c/Ω_b, h, Ω_m | GS1 / GC2 native background (`NAT_*` in X73) | FRAMEWORK-NATIVE | fair share, r_ta |
| ZN3 shapes | ng 64 zooms, seeds 1–9 | FRAMEWORK-NATIVE | ZN3 |
| X77 c_f-equivalent table | ng 64 | FRAMEWORK-NATIVE, ε cut (X81) | NAT |
| c_f = 4 | external | LITERATURE-INPUT, EXTERNAL | C4 |
| a₀, κ = ½ fitted | both footings | FRAMEWORK-NATIVE, κ fitted | template, law, NAT and C4 floors |
| template and law | X7/X30 path, one template | STANDARD-MOND-MACHINERY | keys |
| X-COP M_FORW | Ettori+19 | HSE bracket (forward fit, no dark halo form) | bracket only |
| Published WL M200 | Groener+16 compilation | ΛCDM-PROCESSED (NFW fit), bracket | bracket only |
| Published caustic M200 | Rines & Diaferio 06, Rines+13 | ΛCDM-PROCESSED (F_β from N-body), bracket | bracket only |
| LOSVD M200 | Groener+16 compilation | ΛCDM-PROCESSED (NFW Jeans), bracket | bracket only |
| X-ray M200 in Groener+16 | various | HSE bracket | bracket only |

Planck 5.364: absent as a live value (criteria, verdict 5). κ = ½ FITTED; not theory closed.
