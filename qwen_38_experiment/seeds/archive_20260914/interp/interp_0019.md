INTERP 0019 -- from seed_0019 (random collision)

SHARED NUMBER (wildcard answer):
  w = 1 - (m_W/m_Z)^2 = 1 - 0.8814^2 = 1 - 0.77687 = 0.22313
  This IS sin^2(theta_W) (weak-mixing; Z-pole ~0.231).
  It sits ~0.8% from the Cabibbo angle theta_C = 0.2250 rad.
  Conjecture: this ONE w unifies BOTH bullets.

HYPOTHESIS H-0019:
  A single dimensionless number w = sin^2 theta_W = 1 - (m_W/m_Z)^2 ~ 0.223
  simultaneously (i) is the holonomy-interpolant of the binding-epoch wall
  to theta_C, and (ii) sets the quantization of the a0-bump cluster response.

BULLET 1 (binding wall -> Cabibbo):
  Quantities: redshift z = 10.8 (binding-epoch wall), holonomy angle
  Omega(z) of the framework connection, theta_C = 0.2250 rad.
  Claim: Omega(z=10.8) = w ~ 0.2231 = theta_C (within ~0.8%).
  Test: evaluate Omega(z=10.8) from the framework's connection integral over
  the wall; compare the number to 0.2250.
  KILL: |Omega - 0.2250| > 0.05 (>20% rel) => interpolation false.
  Near-miss band 0.01 < |Omega-0.2250| <= 0.05 => REFINE-once, not a hit.

BULLET 2 (m_W/m_Z breaking -> a0-bump):
  Quantities: w = sin^2 theta_W, a0 footings a0 = 9.3619e-11 and
  1.1279e-10 m/s^2, and the a0-bump cluster response R(a) peaked at a0.
  Claim: the breaking fraction w quantizes R(a); a secondary bump sits at
  a = a0 * w (i.e. ~2.09e-11 / ~2.52e-11) OR the envelope normalizes R(a0)=1/w.
  Test: fit R(a) over the cluster; predict bump position/amplitude from w.
  KILL: predicted bump position off by >1x from any measured feature.

UNIFYING KILL: w must hit theta_C (0.2250) to <1% AND predict the a0-bump
feature. Failure of either leg => DISCARD; both legs failing => CONVENTION
at best. (The 0.8% theta_C gap alone is a REFINE-once candidate, not a hit.)

PREREG: any mm_search over w-space runs with --custom FDR; never count a
CONVENTION-grade match as a hit. kappa = 1/2 stays FITTED (0.551+/-0.043),
NOT derived. Report BOTH footings on every dimensional number.
