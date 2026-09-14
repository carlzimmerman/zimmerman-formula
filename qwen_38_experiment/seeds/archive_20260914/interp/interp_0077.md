INTERP 0077 -- one falsifiable hypothesis from seed 0077

SEED (charitably):
  B1. A holonomy angle of the 0.108-dex RAR, evaluated at the parameter Ups=0.70,
      is the "shadow" of the top Yukawa y_t ~ 0.70.
  B2. The pi-free mass ratio m_W/m_Z = 0.8814 quantizes the EFE linear-response
      tensor (components 1.4732, 0.3674).
  B3. wildcard: one single dimensionless number shared by B1 and B2.

UNIFYING NUMBER PROPOSED: r = 1.4732/0.3674 = 4.0098 ~ 4.
  Read B1 as a spinorial (SU(2)/4pi, 4-fold) holonomy whose evaluation point
  Ups = 0.70 is the top Yukawa; read B2 as the tensor being quantized to r = 4.
  The single number both bullets share is r ~ 4 (the quantization index), with
  y_t ~ 0.70 as its argument. m_W/m_Z = 0.8814 is the electroweak anchor that
  fixes which representation (r=4) the response tensor sits in.

HYPOTHESIS H (concrete):
  The framework carries ONE coupling, the quantization index r ~ 4, such that
   (a) the RAR holonomy angle evaluated at Ups = 0.70 reduces to y_t = 0.70,
   (b) the EFE response-tensor component ratio = r = 4 (not a free float).

EXACT TESTS:
  T1 (B1): compute RAR holonomy angle theta_hol at Ups = 0.70. PREDICT
      |theta_hol(0.70) - y_t| / y_t < 2 x sigma, y_t = 0.701(2) (EW scale).
  T2 (B2): ratio = 1.4732/0.3674 = 4.0098. PREDICT it sits on the integer 4
      within 2 x sigma (residual 0.0098 < 0.02). Also check 0.3674, 1.4732 are
      integer multiples of y_t/2 (0.35, 1.40): within ~5% (near-miss band, not hit).
  T3 (B3, the wildcard): confirm a SINGLE r ties B1 and B2, i.e. the holonomy
      index equals the tensor quantization index (both = 4), not two coincidences.
  SEARCH: run mm_search.py over {y_t, m_W/m_Z, r, 1.4732, 0.3674}; pre-register FDR.
      A match that is CONVENTION-grade is NOT a hit.

KILL CRITERIA (any one kills H):
  K1. theta_hol(0.70) deviates from y_t by > 2 x sigma.
  K2. tensor ratio deviates from 4 by > 2 x sigma (here 0.25% -- survives).
  K3. the holonomy "shadow" of y_t is reproduced by mm_search as a CONVENTION
      artifact (unit/normalization choice), i.e. not framework-predicted.
  K4. B1 and B2 require two independent r's (wildcard fails: not one number).

NOTE: all quantities dimensionless -> two-footing rule (9.3619e-11 / 1.1279e-10)
inapplicable. kappa = 1/2 remains a FIT (0.551 +/- 0.043), not a derivation; not
invoked here.
