SEED 0025 INTERPRETATION -> H0025

Decipher (charitable):
- Bullet 1: the "EFE-response-tensor torsion" is the ratio tau = 1.4732/0.3674 = 4.0098.
  Claim: tau "quantizes" the proton/electron mass ratio m_p/m_e = 1836.15.
- Bullet 2: the continued fraction of sin^2 theta_W = 0.2312 (convergents 1/4=0.25,
  3/13=0.2308, 43/186=0.2312) sets an electroweak "X-pin" scale X = sqrt(y) c/v in
  [106,453] GeV.
- Wildcard: one dimensionless number shared by BOTH bullets. Note the near-hit that
  motivates the bridge: the CF denominator 186 and m_p/m_e = 1836 (~186*10 = 1860,
  ~1.3% off) -- a charitable candidate link between the two bullets.

Hypothesis H0025 (falsifiable):
There exists ONE dimensionless bridge number b -- drawn from the candidate set
{tau=4.0098, 1/tau, sqrt(tau), CF denominators {4,13,43,186}, and 1836/186~9.87} --
that simultaneously
  (a) reproduces m_p/m_e = 1836.15 as b^p (small integer p), AND
  (b) sets the weak structure so that sin^2 theta_W = 0.2312 and X in [106,453] GeV,
  with an O(1) prefactor. The "shared number" the wildcard asks for is that b.

Concrete test:
1. Scan integers 1<=p,q<=6 over the candidate b set: require b^p within 1% of 1836.15
   and b^q within 1% of 0.2312. (tau^5=1036, tau^6=4154 straddle 1836 with no integer
   p landing on it within 1% -> predicted miss for b=tau; 186*10=1860 is the 1.3% case.)
2. mm_search.py dimensional-bridge: reconstruct 1836.15 from
   {tau, c, G, hbar, m_e, G_F, alpha} with an O(1) prefactor; mm_search pre-registers
   FDR. A bridge that does not survive FDR = REFUTED.
3. X-pin check: form X = sqrt(y) c/v for the y implied by the CF of 0.2312 and check
   X in [106,453]; out-of-band = REFUTED.

Footings on dimensional numbers: 9.3619e-11 / 1.1279e-10.

Kill criteria (what would REFUTE H0025):
- No single b with small-integer p,q hits BOTH 1836.15 and 0.2312 within 1%.
- mm_search FDR-corrected bridge for 1836.15 does not survive -> REFUTED.
- X-pin falls outside [106,453] GeV -> REFUTED.

Note: kappa = 1/2 (0.551+/-0.043) is a FIT, not a derivation -- NOT invoked as support.
