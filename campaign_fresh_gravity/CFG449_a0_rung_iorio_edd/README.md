# CFG449: gas-dominated a₀ rung via EDD/LVG TRGB and Iorio+2017. RUNG NOT ESTABLISHED: 2 galaxies added, σ grew to 0.090, and a₀ moved 0.12 dex toward the canonical footing

Criteria 128daa833 were committed alone before any script existed. Script: `cfg449_rung.py`, about 2 s. κ = ½ is fitted, never derived; both footings are reported. No DM particle; the cold mass is still required.

**Verdict as frozen.**
- **Verdict sample:** S0 + SR, N = 12 galaxies (131 points). IO is excluded because K0b failed.
- **Result:** a₀ = 8.54e-11, log −10.069 ± 0.090.
- **Status:** NOT ESTABLISHED, since σ is 0.090 > 0.05.
- **K1 passes:** Υ 0.5 → 0.7 moves a₀ by −0.031 dex.
- **C0 passes:** CFG397's anchor reproduces exactly (−9.953 ± 0.071).
- **Comparisons, all consistent within 2σ:**
  - canonical 9.3603e-11: −0.040 dex (−0.4σ);
  - alt 1.1312e-10: −0.122 dex (−1.4σ);
  - PAPER43 8.3e-11: +0.012 dex (+0.1σ).
- **Shift from CFG397:** −0.116 dex. With 12 galaxies this is not significant, and it rests on 2 dwarfs.

| sample | N gal (pts) | a₀ | log a₀ ± boot σ |
|---|---|---|---|
| S0 = CFG397 anchor (C0) | 10 (108) | 1.113e-10 | −9.953 ± 0.071 |
| SR only (DDO 161, UGC 5829) | 2 (23) | 6.09e-11 | −10.215 ± 0.052 |
| **S0 + SR (verdict)** | **12 (131)** | **8.54e-11** | **−10.069 ± 0.090** |
| post-hoc: S0 + SR without e_DM > 0.5 mag | 11 (127) | 8.57e-11 | −10.067 ± 0.091 |

**Task 1, the EDD route.**
- **The EDD table could not be read.** The CMDs/TRGB table (Anand+2021) is not on VizieR and not in the arXiv source. EDD's table display is behind a reCAPTCHA, which I did not bypass.
- **Substitute:** the Karachentsev LVG catalogue's distance list (SAO, updated 2026-07-13). It is a real table and carries the 2016EDD and 2021AJ...162...80A TRGB moduli per galaxy.
- **CF4 still gives no ladder modulus** for any of the 20 galaxies.
- **LVG adds two:**
  - DDO 161: TRGB 28.90 ± 0.09 (Karachentsev+2018). D goes 7.50 → 6.03 Mpc (×0.80).
  - UGC 5829 = DDO 84: TRGB 29.76 ± 1.49 (2023). D goes 8.64 → 8.95. Its ±1.49 mag error makes it a TRGB only in name; dropping it changes nothing (post-hoc row in the table).
- **Five near galaxies have no ladder modulus in LVG:**
  - KK98-251: membership only;
  - UGC 5721 = NGC 3274: brightest stars;
  - UGC 5764 = DDO 83: texture;
  - UGC 7608 = DDO 129: Tully-Fisher;
  - UGC 731 / 891: no LVG entry.
- **The other 13 lie at 12–65 Mpc.** That is beyond the LVG volume and, for most of them, beyond reach of HST TRGB.
- **Why the shift:** DDO 161 drives the −0.12 dex move. Its new TRGB distance is 20% shorter than SPARC's flow distance (CFG397's gas-flow caveat in action).

**Task 2, the Iorio+2017 route.**
- **Data:** the curves exist as real tables in `finalrot.zip`, linked from the second author's site (the paper's own link is dead; MNRAS returned 403). They give V_c (asymmetric-drift corrected) and Σ_HI, but **no mass models**.
- **Frozen IO route:** gas = 1.33 Σ_HI through a thin-disc ring integrator; stars = a Freeman disc from Oh+2015's SED M* and Hunter+2012's R_d.
- **K0b failed:** the integrator test gave 2.74% > 2% at 0.5 R_d. So, per the frozen rule, IO was not run.
  - Post-hoc diagnosis: the error comes from holding Σ flat inside the first sampled ring at R_d/4, not from the integrator. The script's diagnosis lines show 0.38% at R_d/10 sampling, 0.59% at R_d/40, and 0.94% beyond 0.75 R_d at R_d/4.
- **Disclosed post-hoc run** (`--posthoc-io`, separate `_POSTHOC_IO` outputs, never the verdict). Even with K0b ignored, **C2 fails.**
  - At equal distance the IO route sits above SPARC: DDO 154 +0.13, DDO 168 +0.34, WLM +0.25 (joint +0.16 dex).
  - DDO 87 and DDO 126 have no gas-dominated points in SPARC.
  - DDO 50 and NGC 2366 are not in SPARC Q ≤ 2.
  - This is the same sign and size as CFG442's Oh+2015 failure (+0.20). Both LITTLE THINGS reductions give higher a₀ than SPARC for the same dwarfs.
  - IO-only, 6 galaxies: log −10.14 ± 0.24. Report-only.
- **IO exclusions:**
  - DDO 101: TF distance only;
  - DDO 47: no SED M*;
  - DDO 216 and NGC 1569: no gas-dominated points.

**Task 3, BIG-SPARC.** It is **not publicly released.** Only the IAU S392 proceedings (arXiv 2411.13329, 2024) and a 2025 talk exist. There is nothing on arXiv as a data paper, on VizieR or on the SPARC site, as of 2026-10-07. When it is released, it promises about 4000 homogeneous HI curves and mass models (WISE photometry). That is the natural route to N ≫ 20 gas-dominated discs, but distances will still need TRGB/Cepheid matching.

**Disclosed departures:**
- LVG stands in for the captcha-gated EDD table;
- distance errors are not propagated (CFG397's statistic);
- IO gas comes from my own thin-disc integrator, truncated at the last ring;
- IO stars use a V-band R_d;
- the `--posthoc-io` mode and the e_DM ≤ 0.5 sensitivity row are post-hoc and labelled.

**MUTATE** (gas dropped): empty selection detected, exit 1.

**Owner items:**
1. If wanted, download the EDD CMDs/TRGB table by hand (it needs a human captcha) into `_external_data/cfg449/`. It would only matter for the 13 far galaxies, which almost certainly have no TRGB.
2. Two independent LITTLE THINGS reductions (Oh+2015, Iorio+2017) now give a₀ 0.16–0.20 dex above SPARC on the same dwarfs. Which rotation curves are right is a real open question for any dwarf-based a₀ rung.
3. Reaching σ ≤ 0.05 still needs about 10–20 more ladder-distance gas-dominated discs. BIG-SPARC, once released, is the realistic source.

**Files:**
- `data/`: Iorio zip and LVG tables;
- `_external_data/cfg449/`: arXiv sources and the EDD captcha probe (git-ignored);
- outputs: `cfg449_rung.out` / `_results.json` (verdict), `_POSTHOC_IO.*` and `_MUTATE.out`;
- FETCH_LOG.md.
