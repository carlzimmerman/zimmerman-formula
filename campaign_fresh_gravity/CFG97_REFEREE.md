# CFG97 referee note: CFG41's rule side, which CFG97 could not reproduce, re-derived with independent code

- **Scope.** The orchestrator asked for one headline per lane, re-derived with the referee's own code.
  - CFG97 re-derived CFG41, the 15 Di Teodoro+2023 massive disks. It reproduced the law side to three decimals and the selection-bias Monte Carlo almost exactly.
  - It did **not** reproduce the rule side (the four S0/S0a: −0.105 ± 0.131 dex). That is the open item this note addresses.
- **Script and log:** `CFG97_referee_rule_side.py` and `.out`. It re-implements, independently:
  - the Mandelbaum+2016 interpolation;
  - the 200m → 200c conversion on the Dutton–Macciò NFW;
  - the NFW enclosed mass.
- **Conventions reused from CFG36/h48:** M_h is M_200c; h = 0.674; Ω_m = 0.315; f_b = 0.157; the clip at 5 R_200. These are conventions, not results.

**Why CFG97 missed.** Its consistency test assumed the debris enters as a velocity-squared fraction, v_law²(1 + f) or v_law²/(1 − f). CFG41's `pred()` instead adds it to the acceleration as an NFW enclosed mass at the colour-split collapse mass: v_rule² = v_law² + f_ex (1 − f_b) G M_NFW(<R_flat; M_h)/R_flat.

| four S0/S0a (canonical) | CFG41 | this re-derivation |
|---|---|---|
| v_rule, NGC 1167 / NGC 5790 / UGC 12591 / UGC 12811 (km/s) | 312.7 / 308.5 / 476.4 / 376.1 | 312.68 / 308.53 / 476.35 / 376.03 (max difference 0.07, against CFG41's 0.1 print precision) |
| log M_h (red) | — | 13.314 / 13.314 / 14.083 / 13.511 |
| per-galaxy rule offsets | −0.0312 / −0.0239 / −0.0248 / −0.0362 | the same to 1.1 × 10⁻⁴ dex |
| rule offset, raw → corrected (B = 0.076) | −0.029 → **−0.105** | −0.0290 → **−0.1050** |
| rule-minus-law shift | 0.109 (README) | 0.1088 |
| CFG97's two velocity-squared forms | — | 0.082 and 0.158 dex (CFG97 found 0.082 and 0.159) |

**Verdict:**
- CFG41's rule side reproduces from independent halo code, given CFG41's f_ex.
- CFG97's "not reproduced" came from the functional form it tested, not from an error in CFG41.

**Limits:**
- **f_ex itself is taken from CFG41's committed JSON.** That is the edge-phantom deficit at x_e = 0.40 under the conservation form. It is not re-derived here, and it carries the rule's model content.
- **The ± 0.131 error budget is not re-derived.** Its M* component, 0.127, dominates.
- **The flat radii and v_law are CFG41's printed values.** CFG97 found the flat radius differs in four galaxies, among them NGC 5790 (46.6 vs 50.2 kpc).

κ = ½ stays fitted. Nothing here says the data favour either model, or that the theory is closed.
