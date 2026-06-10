#!/usr/bin/env python3
r"""
INDEPENDENT REDERIVATION #7 -- reconcile my delta-theta/3H~0.05 (Q0~a0) with the finder's ~2e-9.
The discrepancy is a factor ~2e7. Trace it to a single definitional choice and decide who is right.

The finder's table: peak|u|ODE = 1.65e-6 [m/s] (calls u a VELOCITY), theta_tilt = u/L /3H0 ~ 2e-9.
My calc:           u_min (DIMENSIONLESS 4-velocity tilt) = Q0|Phi|/dphi' ~ 3e-7, theta = c*(u/L)/3H0 ~ 0.05.

The factor between them: my u(dimensionless)~3e-7 vs finder's u~1.65e-6 m/s. If finder's u were
ALSO dimensionless 3e-7 and theta=c*u/L, we'd agree. The finder got u~1.6e-6 (calling it m/s) and
theta=u/L (no c). Let me compute u_min BOTH ways from the SAME inputs and see which is the correct
dimensionless tilt.

DEFINITION: A^r is the radial component of the unit 4-velocity A^mu (A.A=-1). It is DIMENSIONLESS.
A^r = (proper radial velocity of the aether)/c. So if the aether 'drifts' at proper speed v_drift,
A^r = v_drift/c. The forced tilt u_min = Q0|Phi|/dphi':
  - Q0 = phibar-dot = dphi/dt has units of (scalar field)/time.
  - dphi' = dphi/dr has units (scalar field)/length.
  - Q0/dphi' has units length/time = VELOCITY. So u_min = (Q0/dphi')*|Phi| has units of velocity!?
That can't be, since A^r is dimensionless. RESOLUTION: in Q = A^mu d_mu phi, the time component is
A^t * d_t phi where d_t = (1/c) d_(ct) if we use x^0=ct, OR A^t carries the c. The cross term is
A^r d_r phi. For Q to be a single scalar, A^t d_t phi and A^r d_r phi must have the SAME units.
  d_t phi [phi/s],  d_r phi [phi/m]. For A^t d_t phi ~ A^r d_r phi:  A^t[1] * [phi/s] vs A^r[1]*[phi/m]
  -> NOT same units unless we use x^0=ct so d_0 phi = (1/c) d_t phi [phi/m]. THEN both are [phi/m]:
     Q = A^t (1/c) dphi/dt + A^r dphi/dr,  both [phi/m].  Q0_eff = (1/c) phibar-dot [phi/m].
  So the cross term is A^r * dphi', and the balance A^r dphi' ~ |Phi| * Q0_eff = |Phi|(phibar-dot/c):
     u_min = |Phi| (phibar-dot/c) / dphi' = |Phi| Q0_eff/dphi'  -- DIMENSIONLESS (both [phi/m]). GOOD.
THE c IS INSIDE Q0_eff. So u_min is dimensionless ~ 3e-7, and delta-theta = c*(u/L) [the spatial-
divergence-to-rate c]. My calc is the consistent one. The finder's u~1.6e-6 'm/s' implicitly used
Q0 WITHOUT the 1/c, making u a velocity, then dropped the c in theta -- the two errors PARTIALLY
offset but not exactly. Let me verify numerically.
"""
import numpy as np
c=2.99792458e8; G=6.674e-11; Msun=1.989e30; kpc=3.0857e19; Mpc=3.0857e22
H0=67.4e3/Mpc; OmL=0.685; Lam=3*OmL*H0**2/c**2; a0=c**2*np.sqrt(Lam/(32*np.pi))
Mb=5e10*Msun; Rd=3*kpc
def Menc(r): x=r/Rd; return Mb*(1-(1+x)*np.exp(-x))
def gbar(r): return G*Menc(r)/r**2
def dphi_p(r): return np.sqrt(a0*np.maximum(gbar(r),1e-30))   # [accel^1/2] = [m/s/sqrt(m)]? check units
def Phin(r): return -(r*np.sqrt(a0*gbar(r)))/c**2

r=10*kpc
Phi=abs(Phin(r))
dp=dphi_p(r)    # = sqrt(a0*gbar), units sqrt((m/s^2)^2)=m/s^2? no: a0,gbar both m/s^2 -> sqrt(product)=m/s^2
print(f"At r=10kpc: |Phi|={Phi:.3e}, dphi'(=sqrt(a0 gbar))={dp:.3e} [m/s^2], gbar={gbar(r):.3e}")

# Q0 candidates: the scalar velocity. In MOND/AeST dphi has units of acceleration (the scalar
# gradient sources acceleration). phibar-dot ~ a0 (dimensionally, the cosmological scalar rate ~ a0).
# Then Q0_eff = phibar-dot / c if we need [accel] to match dphi'[accel]. Let's set Q0 = a0 [accel].
Q0 = a0
# DIMENSIONLESS tilt: u_min = |Phi| * Q0 / dphi'  -- BUT this needs Q0 and dphi' same units (accel). OK both accel.
u_dimless = Phi*Q0/dp
print(f"\nu_min (dimensionless, Q0=a0 [accel], dphi'[accel]) = |Phi|*Q0/dphi' = {u_dimless:.3e}")
# delta-theta/3H WITH the c (spatial divergence of dimensionless tilt -> rate):
L=5*kpc
dtheta_over_3H = c*(u_dimless/L)/(3*H0)
print(f"delta-theta/3H = c*(u/L)/(3H0) = {dtheta_over_3H:.3e}   <- MY consistent number")

# Now the FINDER's path: treat u as velocity = Q0_vel*|Phi|/dphi' with Q0 a VELOCITY.
# If finder used Q0 ~ a0 but in their ODE the source/stiffness made peak|u|~1.6e-6 (m/s), then:
u_finder_ms = 1.65e-6  # from their table
dtheta_finder = (u_finder_ms/L)/(3*H0)   # u/L in 1/s, no c
print(f"\nFINDER path: u={u_finder_ms:.2e} m/s, theta=u/L/3H0 (NO c) = {dtheta_finder:.3e}  <- their number")

print(f"""
RECONCILIATION:
  My u (dimensionless) = {u_dimless:.2e}.  delta-theta/3H = c*u/L/3H0 = {dtheta_over_3H:.2e}.
  Finder u = 1.65e-6 (m/s), theta = u/L/3H0 (no c) = {dtheta_finder:.2e}.
  Ratio my/finder = {dtheta_over_3H/dtheta_finder:.2e}.

  The finder's u in 'm/s' is ~1.65e-6, but my dimensionless u is ~{u_dimless:.1e}; if the finder's u
  were the PROPER VELOCITY of the dimensionless tilt it would be u*c ~ {u_dimless*c:.1e} m/s (~90 m/s),
  NOT 1.65e-6 m/s. The finder's u is too small by ~{u_dimless*c/1.65e-6:.1e}, AND they dropped the c
  in theta (factor {c:.1e}). Net: the finder UNDERSTATED delta-theta/3H by ~{dtheta_over_3H/dtheta_finder:.0e}.

  *** The load-bearing question: is delta-theta/3H ~ 0.05 (mine) or ~2e-9 (finder)? ***
  It hinges on (i) the dimensionless tilt amplitude u_min and (ii) the c-factor. The c-factor I
  confirmed THREE ways (#4b) -- it is REAL. The amplitude u_min = |Phi|*Q0/dphi' with Q0~a0,
  dphi'~sqrt(a0 gbar)~a0 (deep MOND, gbar~a0) gives u_min ~ |Phi| ~ 1e-6 to 1e-7. So:
     delta-theta/3H ~ c*|Phi|/(L*3H0) ~ (c/(3H0 L)) * |Phi| ~ (4.6e25/L)*|Phi|.
  With L~5kpc=1.5e20: (4.6e25/1.5e20)*|Phi| ~ 3e5 * |Phi| ~ 3e5 * 2.5e-7 ~ 0.08.
  => delta-theta/3H ~ 0.05-0.1 for the physical galaxy. NOT 2e-9.
""")
print("HONEST CORRECTED NUMBER: delta-theta/3H (tilt) ~ 0.05-0.1 (Q0~a0), the finder's 2e-9 is wrong")
print("by ~7 orders (dropped the c AND mis-sized u). Still <1 -> within RAR scatter -> theta PINNED,")
print("but the MARGIN is ~5-20x (a0 shifted by ~5-10%), NOT the ~1e9x the finder claimed.")
