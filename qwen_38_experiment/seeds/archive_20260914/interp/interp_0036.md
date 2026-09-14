# INTERP 0036 -- seed 0036 (random collision)

## Seed bullets
- B1: torsion of the nu0 window could be measured by the top Yukawa y_t (~0.70).
- B2: continued fraction of m_W/m_Z (0.8814) might set R_dm = 0.387.
- W: what single dimensionless number would BOTH bullets share if true?

## Charitable decoding
"nu0 window torsion" and "R_dm" are framework constructs taken by name as given;
the seed supplies their predicted numbers. Since 0.70 != 0.387, the two bullets
cannot both equal the same raw number. The only consistent single-number reading
is a RATIO channel: one knob, two projections.

## Hypothesis H-0036 (one concrete claim)
A single dimensionless number gamma governs both bullets:
  * projection A (torsion): tau(nu0 window) = y_t ~= 0.70.
  * projection B (dark-matter radius): R_dm = gamma * y_t = 0.387.
The wildcard answer is gamma = R_dm / y_t = 0.387 / 0.70 = 0.553,
identified with the framework constant kappa (0.551 +/- 0.043).
B2 then reads: kappa is ALSO recoverable from the continued fraction of
m_W/m_Z = 0.8814, i.e. a stated CF functional of 0.88147 yields kappa (~0.553)
or R_dm (~0.387).

## Exact test (pre-registered)
1. ARITHMETIC gate: 0.387/0.70 = 0.553 must lie inside kappa's 1-sigma
   [0.508, 0.594]. (PASS: 0.553 is inside.)
2. CF REPRODUCIBILITY: apply the continued fraction of m_W/m_Z = 0.88147
   [0; 1, 7, 2, 3, ...] and test whether ANY standard functional
   (convergent a_n, convergent ratio p_n/p_{n+1}, or depth-<=4 tail) yields a
   value within 2x of 0.387 OR 0.553. Pre-register the functional list now;
   do not add functionals after seeing the result.
3. TORSION READOUT (future): tau(nu0 window) predicted = y_t. Falsifiable when
   a torsion measurement exists.

## Kill conditions
- REFUTED: no standard CF functional (convergent / semiconvergent / depth-<=4
  tail of 0.88147) lands within 2x of 0.387 or 0.553.
- NULL: 0.387/0.70 falls outside kappa's 1-sigma (it does not -- gate passes).
- REFUTED: tau(nu0 window) measured and departs from y_t by > 2 sigma_yt.
- DISCARD: the two numbers are unrelated (no single gamma reconciles within 2x).

## Falsifiability note
The load-bearing, checkable core is test 2: the CF of m_W/m_Z must reproduce a
value near 0.387/0.553 by a pre-registered functional. If it cannot, H-0036
dies regardless of the (currently unmeasured) nu0-window torsion.
Both footings: y_t, m_W/m_Z, R_dm are dimensionless -- no footing dependence.
