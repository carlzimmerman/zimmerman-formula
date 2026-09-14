H86 -- "the shared integer is N=30"
Seed 0086 collision (nu0-window resonance -> top Yukawa ~0.70 ;
boundary ratio m_p/m_e = 1836.15 -> quantized shift charge Q0*n).

CHARITABLE DECODE
The wildcard asks for ONE dimensionless number both bullets share.
It is the integer N = 30:
  y_t * sqrt(m_p/m_e) = 0.70 * 42.85035 = 29.995 ~= 30  (off 1.6e-4)
  y_t^2 * (m_p/m_e)  = 0.70^2 * 1836.15 = 899.7 ~= 30^2 = 900
So both bullets reduce to N=30: the window resonance renormalizes a unit
window to y_t = N/sqrt(m_p/m_e), and m_p/m_e sets the shift-charge quantum n=N.

EXACT HYPOTHESIS
  H86a (top Yukawa): at the GUT scale M=1e16 GeV,
       y_t(1e16) = N / sqrt(m_p/m_e) = 30 / 42.85035 = 0.70011
  H86b (charge lattice): m_p/m_e quantizes the shift charge so that
       n = 30, i.e. Q0*n with n=30 is the lattice step, and
       (m_p/m_e)/n = 1836.1526734 / 30 = 61.2051 must be a lattice
       rational of the framework (not a generic float).

EXACT TEST
  1. RG-evolve the top Yukawa with the SM 3-loop beta function from
     m_t=172.5 GeV, v=246.22 GeV up to 1e16 GeV.
     PASS (Pursue) iff |y_t(1e16) - 0.70011| <= 0.030 (the 3-sigma
     running band). FAIL -> REFUTED.
  2. H86b: check 61.2051 against the framework charge-lattice rational
     set. If it is a clean lattice fraction to <1e-3 -> consistent;
     else -> DISCARD H86b only (H86a stands alone).
  Both footings (9.3619e-11 / 1.1279e-10) are N/A: H86 is purely
  dimensionless, so no dimensional anchoring is required.

KILL CONDITIONS
  - REFUTED: y_t(1e16) lies outside [0.670, 0.730].
  - DISCARD: 61.2051 is not a lattice rational AND N=30 is found to be a
    fluke (re-run the O(1)-prefactor pass; if the 29.995 hit dissolves
    under the mm_search analytic-chance baseline, it is a near-miss).
  - NULL: prediction sits inside the running uncertainty, giving no
    decisive discrimination -> record as NULL, not a hit.

HONESTY FLAG
The 29.995 match is within 0.016% but y_t at 1e16 has O(0.03-0.06)
uncertainty, so H86a is likely a NEAR-MISS / NULL. Do not promote as a
hit without the blind referee; grade via mm_search pre-registered FDR.
