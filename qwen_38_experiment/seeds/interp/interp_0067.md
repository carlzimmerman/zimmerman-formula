# Interp 0067 (from seed_0067 -- random collision, read charitably)

## Charitable reading
The seed collides three claims:
* B1: a "pin" quantity X = sqrt(y) c/v (reported range 106-453) hits a *saturation
  bound* that selects the top-quark Yukawa y_t ~ 0.70.
* B2: the boundary-term ratio m_p/m_e = 1836.15 *interpolates* (as one endpoint of a
  framework interpolation) to a transport time t_tr = 690 Gyr.
* WILDCARD: a single framework dimensionless number zeta drives BOTH.

## ONE concrete falsifiable hypothesis
H: There is a single framework dimensionless number zeta* that simultaneously
  (a) saturates the X-pin so that the selected top Yukawa y_t = 0.70, and
  (b) sets the m_p/m_e -> t_tr interpolation so that 1836.15 maps to t_tr = 690 Gyr.
  i.e. y_t and (m_p/m_e, t_tr) are two evaluations of one zeta, not two free fits.

## Exact quantities (pre-registered)
* y_t  = 0.70  (top Yukawa; target -- flag: weak-scale y_t ~ 0.93, so 0.70 needs a
  stated running/convention; a pure rescale of 0.93 is a CONVENTION, not a hit).
* m_p/m_e = 1836.15267 (CODATA proton/electron mass ratio).
* t_tr = 690 Gyr = 2.183e16 s (transport time -- MUST be a framework-defined transport
  time with a stated derivation, else B2 is a fabricated target).
* X = sqrt(y) c/v in [106,453]; y and v must be identified (dimensionless y, velocity v).
* No dimensional number reported here, so both footings (9.3619e-11 / 1.1279e-10) do
  not enter; if the test forces a dimensional a0, evaluate on BOTH footings.

## Exact test
1. From the framework build the two maps f_1(zeta)->y_t and f_2(zeta)->(m_p/m_e, t_tr).
2. Search zeta for the single value zeta* with f_1(zeta*) = 0.70 AND
   f_2(zeta*) reproduces BOTH 1836.15 and 690 Gyr within pre-set tolerances.
3. Pre-register tolerances BEFORE computing (suggested 5% on y_t, 1% on m_p/m_e,
   10% on t_tr). Report the residual of each. Use mm_search.py if it is a search
   (it self-pre-registers FDR); never count a CONVENTION-grade match as a hit.

## What kills it
* REFUTED: the zeta* that saturates X to y_t=0.70 does NOT yield m_p/m_e~1836 and
  t_tr~690 Gyr (or the 690-Gyr interpolation needs a different zeta) -> zeta is not shared.
* NULL: no single zeta fits all three numbers within the pre-set tolerances.
* DISCARD: "690 Gyr" has no framework transport-time derivation (fabricated target),
  or y_t=0.70 is only a convention rescale of 0.93.

## Note
Seed is garbled (random collision); this is the most charitable single-hypothesis
distillation. B2 (690 Gyr) is the weakest link and is the likely kill point.
