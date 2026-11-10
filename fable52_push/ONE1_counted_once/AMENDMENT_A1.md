# ONE1 AMENDMENT A1 (post hoc; committed alone, after a stopped first run of `one1_kids.py`, before the second run)

Criteria a967a38851. Changes numerics only. No row, statistic, gate, line, tolerance, share, bracket, mutation arm or label
rule changes. Adopts nothing.

## What happened

- The first run of `one1_kids.py` failed two known answers on the neighbour kernel, by small margins:
  - KA7(i), kernel against the point-mass kernel at the band edges: 1.3e-4 against the frozen 1e-4.
  - KA7(ii), centred kernel against the direct projection: 1.4e-3 against the frozen 1e-3.
- Every other known answer that ran passed: KA2 (the lead's table, 0.0034), KA3, KA4, KA6 (KO1 E7 to 2e-15), KA7(iii),
  KA7(iv) (E8's 0.00181 / 0.00165 reproduced with E8's 1,001,712 pairs).
- I stopped the run during the first neighbour scan of the primary reading. **No graded KiDS number (no model R_s, no fitted
  k, no z) had been computed or printed.** The log is kept as `run_one1_kids_firstrun_KA7fail.txt`.

## Cause

- KA7(i): the table held H on rows linear in ln delta; the term 2 ln(delta + 1) at the band's top edge is curved in
  ln delta, and linear interpolation between rows missed it by up to 1.4e-4.
- KA7(ii): the disc mass Q was a trapezoid sum over a fixed s grid with a near-step integrand (the disc edge), worth a few
  tenths of a per cent at small radii.

## Change (code only)

- Q is now the exact inner mass from the cumulative projected mass plus a Gauss-Legendre integral (96 nodes, in a variable
  that removes the square-root ends) across the band where the disc edge cuts the halo.
- Finer tables: 480 rows in delta (was 320), 641 points per half-band (was 241), surface density on 8,000 points.
- The upper half-band is stored minus 2 ln(1 + rho) and that term is added back exactly, so the band's top edge meets the
  analytic branch exactly.
- Checked on the scratch copy before the second run: KA7(i) 1.5e-5, KA7(ii) 8e-6, KA7(iii) +0.0033; four off-centre cases
  agree with a brute-force disc integration to 1e-3 or better.

The second run uses the frozen tolerances unchanged.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
