#!/usr/bin/env python3
r"""
INDEPENDENT REDERIVATION #8 -- BOTH WAYS on the load-bearing ratio Q0/dphi', which sets u_min and
hence delta-theta/3H. I must not let MY 'finder understated it' correction be a manufactured deficit
any more than the finder's tiny number be a manufactured win. Bound Q0/dphi' physically.

PHYSICAL SCALES (geometric/natural units where all of A^mu d_mu phi are accelerations):
  - dphi' (galactic): the scalar gradient that sources MOND. In deep MOND |∇φ| ~ sqrt(a0 g_bar).
    At the disk g_bar ~ a0 (the MOND regime!), so dphi' ~ sqrt(a0*a0) = a0. So dphi' ~ a0.
  - Q0 (cosmological): phibar-dot, the rate of the rolling cosmological scalar. In AeST the scalar's
    temporal gradient Q sits near Q0 (the dust-well minimum). The dust energy density 8piG rho_dust
    ~ K(Q) curvature * (Q-Q0)... The natural cosmological rate is Q0 ~ (cosmological accel) ~ cH0 or
    ~ a0 (since a0 ~ cH0/Z, same order). So Q0 ~ a0 to cH0 -- the SAME order as dphi'.

  => Q0/dphi' ~ O(1) to O(Z~6). NOT a huge ratio. So u_min ~ |Phi| * O(1-6) ~ 1e-6, dimensionless.
  This is the regime I used. delta-theta/3H ~ c|Phi|/(3H0 L) * (Q0/dphi') ~ 0.05 * O(1-6).

BOTH WAYS -- the two extremes:
"""
import numpy as np
c=2.99792458e8; G=6.674e-11; Msun=1.989e30; kpc=3.0857e19; Mpc=3.0857e22
H0=67.4e3/Mpc; OmL=0.685; Lam=3*OmL*H0**2/c**2; a0=c**2*np.sqrt(Lam/(32*np.pi))
Z=2*np.sqrt(8*np.pi/3)

print(f"a0={a0:.3e}, cH0={c*H0:.3e}, cH0/Z={c*H0/Z:.3e} (=a0 check), 3H0={3*H0:.3e}")
print(f"c/(3H0) = {c/(3*H0):.3e} m = {c/(3*H0)/kpc:.3e} kpc\n")

Mb=5e10*Msun; Rd=3*kpc
def Menc(r): x=r/Rd; return Mb*(1-(1+x)*np.exp(-x))
def gbar(r): return G*Menc(r)/r**2
def dphip(r): return np.sqrt(a0*np.maximum(gbar(r),1e-30))
def Phin(r): return -(r*np.sqrt(a0*gbar(r)))/c**2

print(f"{'r[kpc]':>8}{'gbar/a0':>10}{'dphi/a0':>10}{'|Phi|':>12}")
for rk in (5,10,20,30):
    r=rk*kpc
    print(f"{rk:>8}{gbar(r)/a0:>10.2f}{dphip(r)/a0:>10.2f}{abs(Phin(r)):>12.2e}")

print(f"""
  Confirmed: dphi'/a0 ~ 0.3-1 across the disk (deep-MOND, gbar~a0). So dphi' ~ a0.
""")

print("BOTH WAYS on delta-theta/3H = (c/(3H0 L)) * |Phi| * (Q0/dphi'):")
print(f"  {'Q0':>14}{'Q0/dphi'+chr(39):>12}{'u_min':>12}{'delta-theta/3H':>18}{'verdict':>12}")
r=10*kpc; Phi=abs(Phin(r)); dp=dphip(r); L=5*kpc
pref = c/(3*H0*L)
for Q0,lab in [(0.1*a0,'0.1a0'),(a0,'a0'),(c*H0,'cH0'),(Z*a0,'Z*a0~cH0')]:
    ratio=Q0/dp; u=Phi*ratio; dth=pref*Phi*ratio
    v='PINNED' if dth<0.1 else ('MARGINAL' if dth<1 else 'SWAMPED')
    print(f"  {Q0:>14.2e}{ratio:>12.2f}{u:>12.2e}{dth:>18.2e}{v:>12}")

print(f"""
  HONEST BOUNDED RESULT (delta-theta/3H, the THETA carrier, tilt contribution, WITH the c-factor):
    Q0~0.1a0 : ~0.01   PINNED
    Q0~a0    : ~0.10   PINNED (borderline; ~10% a0 shift, within RAR scatter ~29%)
    Q0~cH0   : ~0.7    MARGINAL (order-1; could approach swamping)
  The physical range Q0~(0.1-1)a0 gives delta-theta/3H ~ 0.01-0.1 -> theta PINNED with a MODEST
  margin (factor ~3-30), the a0 shift ~1-10%. NOT the 1e8-1e9 margin the finder claimed (c-factor +
  amplitude error). NOT swamped either (would need Q0 >> a0, away from the dust-well scale).

  So: the finder's PINNED verdict for the THETA carrier SURVIVES, but the MARGIN is ~10x not ~1e9x,
  and the corrected delta-theta/3H is ~0.1 (Q0~a0), not ~1e-8. The tilt is a real ~few-to-10%
  environmental perturbation on a0 -- a TESTABLE signature, sitting inside RAR scatter, not a kill.
""")

print("="*90)
print("DECISIVE BOTH-WAYS on the SCALAR carrier delta-Q/Q0 (which the energy minimizes to ~0):")
print("="*90)
print("""  My rederivation #2/#2b: Q(u_min)=Q0 EXACTLY (energy minimizes K(Q)=(1/2)K2(Q-Q0)^2 at Q=Q0).
  So delta-Q/Q0 -> 0 at the forced minimum (even tighter than the finder's |Phi|). The scalar carrier
  Q is PINNED HARDER than claimed -- this is the strongest single result and it is reading-independent
  (an algebraic identity: the tilt is the free direction the energy uses to reach the dust-well bottom).
  Both-ways: to UN-pin Q you must push the aether to virial tilt u~v/c, away from the stable minimum
  (U''=K2 dphi'^2>0) -- forbidden by the convex well. Confirmed.""")
