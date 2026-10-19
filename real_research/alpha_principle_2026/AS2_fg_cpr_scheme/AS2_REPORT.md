# Lane AS2: report

## Verdict: NOT COMPLETED. Gate G-CPR-EH (ii) fails; every other gate passes.

The lane rebuilt the Codello-Percacci-Rahmede (CPR) f(R) flow from scratch. My derived flow equals CPR's published closed form
**exactly**, at orders R^0, R^1 and R^2. It reproduces their n = 2 fixed point and critical exponents to every printed digit.

One frozen check fails. The n = 1 (Einstein-Hilbert) fixed point printed in CPR's Table 1 is missed by 0.33 percent in Lambda~ and
0.37 percent in G~, against a frozen tolerance of 0.1 percent. The frozen rule says any gate failure means NOT COMPLETED.

**No SM fixed point, no f_g\* and no P were computed.** This says nothing about alpha. kappa and Z enter nowhere.

| item | result |
|---|---|
| verdict class | NOT COMPLETED (G-CPR-EH (ii) fails) |
| P (R^2 trial) | not computed |
| P_EH (reference) | not computed |
| f_g\* (R^2) and f_g,EH | not computed |
| fixed points with SM matter | not computed |
| G-MAT | PASS. Scalar, Dirac and 1-form bare S^4 heat kernels equal Vassilevich's a_0, a_2, a_4 (scalar and 1-form also from the S^4 spectra). The assembled full operators equal Christensen-Duff: (1, 1/6, 29/2160), (4, -1/3, 11/2160), (2, -2/3, -31/1080) |
| HK-CPR | PASS. The S^4 coefficients from the spectra equal CPR's table: S (1, 1/6, 29/2160), V (4, 2/3, 43/1080), VT (3, 1/4, -7/1440), TT (5, -5/6, -1/432) |
| G-CPR-EH (i) | PASS. The R^0 and R^1 coefficients of the derived flow equal CPR's closed form 'george' / 725760 exactly (N = 725760 as frozen) |
| G-CPR-R2 (i) | PASS. The R^2 coefficient equals 'george' / 725760 exactly |
| G-CPR-R2 (ii) | PASS. Lambda~* = 0.12936, G~* = 1.56329, g~2* = 1.514408e-3 vs Table 1 (0.1294, 1.5633, 1.514e-3). Exponents 1.376 +- 2.325 i and 26.862 equal Table 2 |
| G-CPR-EH (ii) | **FAIL.** Lambda~* = 0.12927 and G~* = 0.98417 vs Table 1 n = 1 (0.1297, 0.9878); misses of -0.33% and -0.37% against a 0.1% tolerance. g~0* = 5.2261e-3 matches Table 1 (5.226e-3), and the exponents 2.3824 +- 2.1682 i match Table 2 (2.382 +- 2.168 i) |
| G0 | PASS (as in AS1) |
| classifier controls | PASS (CC1-CC5) |
| MUTATE_1 | G-CPR-EH (i) FAILS as required (exit 1) |
| MUTATE_2 | G-CPR-R2 (i) and (ii) FAIL as required (exit 1) |
| MUTATE_3 | the classifier controls FAIL as required (exit 1) |
| f_g stop rule | not reached |

## Why the one gate fails, and what the evidence says (`as2_diag_cpr_n1.out`)

The diagnostic was added after the gate run. It is not a gate and does not change the verdict.

The n = 1 flow I use is CPR's own flow: its R^0 and R^1 coefficients equal their closed form exactly.

* **Its fixed point:** g~ = (5.2261e-3, -20.2143e-3). The only other real root is at Lambda~ = 0.72, which is not admissible.
* **CPR's printed point, Table 1 n = 1:** g~ = (5.226e-3, -20.140e-3).
  * At that point the beta functions are not zero: (1.0e-4, -2.9e-4).
  * The critical exponents there would be 2.380 +- 2.187 i. CPR's own Table 2 lists 2.382 +- 2.168 i, which is what my root gives.

So CPR's Table 1 n = 1 row is inconsistent with their Table 2 n = 1 row and with their closed form. The entries agree with a misprint
of g~1* (-20.214e-3 printed as -20.140e-3) carried into the Lambda~ and G~ columns. Their n = 2 row has no such problem: it is reproduced
to every digit.

This is a diagnosis, not a reprieve. The gate was frozen against the printed n = 1 numbers, so the lane is NOT COMPLETED.

## Why the trial was not computed

The pre-registration says no trial number is a result unless every gate passes.

Beyond that, I deliberately did not compute any SM fixed point, f_g or P in CPR's scheme. A follow-up lane could tie the EH check to
CPR's internally consistent data instead of the misprinted row (the closed form, Table 1 g~0*, and the Table 2 exponents, all of which
already pass here). Such a lane can only be pre-registered blind if no trial number in this scheme exists yet. Any such change of gate
belongs in a NEW pre-registration; it may not be made inside AS2.

## Disclosures

1. **Amendment 1, committed 8ce28c967 before any AS2 script existed or ran.**
   * My pre-registration paraphrase said "every scalar trace omits l = 0, 1".
   * CPR eq. (8) explicitly adds back the two lowest h modes, so the h trace is unprimed. I found this by hand-checking the h block of
     CPR's closed form (+29R^2).
   * Implemented: TT and h traces unprimed; vector traces single-primed; other scalar traces double-primed.
   * That this is the right reading is confirmed after the fact: the R^2 coefficient matches the closed form exactly.
2. **Edits to `as2_common.py` before any run.** I removed a dead line in `em_coeffs` and wrote out the edge-flag rule. "Within 5 percent
   of a domain edge" is read per finite bound: g > 47.5, lambda < -47.5, lambda > 0.475, |b| > 950. It was never exercised, because no
   trial was run.
3. **`as2_gcpr.py` first run crashed** with a NameError (the script used `R` instead of `A.R`) after the HK-CPR check and before any gate
   comparison.
   * Fixed; nothing else changed.
   * First-run output kept as `as2_gcpr_FIRSTRUN.out`, with the traceback path prefix replaced by `<repo>/`.
4. **`as2_diag_cpr_n1.py`** was added after the gate run, as a diagnostic.
5. **Memory.** Each process stayed under 200 MB RSS (G-MAT 122 MB, G-CPR 188 MB). Everything ran single-thread at `nice -n 19`, one
   process at a time, beside the live 1024^3 run.

## What was read

* **CPR 0805.2909:** sections IV.A-C and VII in full, and the S^4 appendix. This was read for AS1 and re-used: eqs. `fofr`,
  `fofrgaugefixing`, `grop`, `xiquadratic`, `scalarpart`, `ghop`, `faerge` (eq. 8), `eq:9`, `mainpart`, `george`, `sigma`; Tables 1-4;
  `taba2`, `taba21`, `taba6`; `vt`, `ttt`; `HKasymp`; `PkI`.
* **Vassilevich hep-th/0306138:** section 4.1 (the beginning and the a_0-a_6 formulae) and section 4.2.2 (free fields and the table of
  (a, b, c, d)). Not read: the rest.
* **E-V 1709.07252:** read for AS1; only the definition of f_g is used. It was not needed, because the trial was not run.
* **Recalled rather than read:** nothing load-bearing. The Dirac spinor curvature Omega = (1/4) R_ijab gamma^a gamma^b is standard, and
  is verified against the Christensen-Duff Dirac entry in G-MAT (ii).

## Files

* `as2_common.py`: the machinery. It imports AS1's `as1_common` and `as1_g1_fg_flat`.
* `as2_gmat.py`, output `.out`.
* `as2_gcpr.py`, outputs `.out`, `_FIRSTRUN.out`, `_MUTATE_1.out`, `_MUTATE_2.out`. Normal mode exits 1: that is the gate outcome.
* `as2_diag_cpr_n1.py`, output `.out`.
* `as2_g0_classifier.py`, outputs `.out`, `_MUTATE_3.out`.

Downloads sit in `as2_scratch/` and are not committed.
