# PAPER49 deposit
- Published 2026-10-20 on the owner's explicit go: DOI 10.5281/zenodo.23501949 (https://zenodo.org/record/23501949), version 1.0.
  Live record checked after publish: one file, 68089 bytes, md5 e421756336cf26297e7fbf92d72e4bc9, identical to the committed PDF.
- Gate: `tectonic PAPER49_why_cold_energy_settles_2026.tex && python3 PAPER49_audit.py && python3 PAPER49_zenodo_publish.py`.
  Audit: ALL PASS (`PAPER49_audit.out`). `PAPER49_AUDIT_MUTATE=1` (W_full in place of W_rem) fails B1–B3 as designed
  (`PAPER49_audit_MUTATE.out`), so the rest-state check bites.
- Built and audited after the CFG654 NC1x 1024³ run ended (chain6 done 10:07) and before chain7's NC2x started; no computation
  ran beside a 1024³ job.
- Changes from the 2026-10-14 draft (stated in the paper's own "Updated before deposit" note):
  - L* floor 5.75 → 24 pc (CFG820, primary sample, canonical L95 = 23.96 pc). Scaled from it: Cassini Q2 ≤ 5e-8 of the bound
    (CFG770's 3.47e-6 at 5.75 pc × (5.75/L*)³), sunward pull GM☉/L*² ≤ 2.4e-16 m s⁻², wide-binary envelope ½(s/L*)² ≤ 5e-5 at
    50 kAU. The unsourced "~2 pc" bending scale is replaced by L*.
  - Own-supply rule removed as excluded (CFG801, Δχ² +197 within 0.31 Mpc); catchment supply instead (THEORY_CANONICAL v2).
  - Shear: +2.03 (old rule) replaced by CFG650 T1x/T2x (−7.70 / −7.18) and the CFG654 native-input rerun on the canonical
    footing (NC1x vs NCS0, Δχ² −10.08, CONSISTENT, as quoted in CFG654 addendum A3). The alt-footing native rerun (NC2x) is queued.
  - Hot-gas prediction: "frozen test queued" replaced by the CFG815 result (fails on all 318 eRASS1 clusters).
  - Dwarf-excess caveat (PAPER55) and "The theory is not closed." added.
- Audit note: check C2 reads the TeX source, because pdftotext puts the "−16" superscript on another line; A1 ties the PDF to
  the TeX.
- The Zenodo metadata file is kept out of git (it carries the author's name), as for PAPER50–54.
