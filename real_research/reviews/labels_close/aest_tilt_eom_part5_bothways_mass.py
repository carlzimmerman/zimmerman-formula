#!/usr/bin/env python3
r"""
PROBLEM 2 -- PART 5: BOTH WAYS on the aether mass m_A. The whole theta verdict hinges on the
tilt amplitude A^r = source/m_A^2. Source ~ Q0 varphi' (Part 4). So A^r ~ varphi'/Q0 * (Q0^2/m_A^2).
If m_A = Q0 (SZ value): A^r ~ varphi'/Q0 ~ 4e-5 -> theta SWAMPED.
If m_A >> Q0: A^r suppressed -> theta could be PINNED. What is the LARGEST defensible m_A, and
does any m_A make theta robustly pinned WITHOUT also killing the SZ galaxy-MOND phenomenology?

KEY CONSTRAINT (SZ 2007.00082): the scalar/aether screening mass mu = sqrt(2K2/(2-K_B)) Q0 must
satisfy mu^-1 >~ 1 Mpc for MOND to operate in galaxies. So m_A = mu <~ 1/Mpc = Q0. The mass CANNOT
be made large without screening OUT the MOND behavior (mu^-1 < galaxy size would kill MOND).
=> m_A is BOUNDED ABOVE by ~1/Mpc by the SAME physics that makes AeST a MOND theory. The tilt
   CANNOT be pinned smaller than A^r ~ varphi'/Q0 ~ 4e-5 without breaking galaxy MOND.
This is the both-ways pincer: making the aether stiffer to pin theta destroys the MOND fit.
"""
import numpy as np
c=2.99792458e8; Mpc=3.0857e22; kpc=3.0857e19; H0=67.4e3/Mpc
Z=2*np.sqrt(8*np.pi/3); a0=c*H0/Z
Q0=1.0/Mpc; varphi_p=a0/c**2; L_u=10*kpc
dtheta_per_u=c/(3*H0*L_u); dQ_per_u=varphi_p/Q0

print("="*100)
print("PART 5 -- BOTH WAYS on m_A: can a stiffer aether pin theta? (it kills MOND if it tries)")
print("="*100)
print(f"  source ~ Q0 varphi'; A^r = Q0 varphi'/m_A^2 = (varphi'/Q0)(Q0/m_A)^2")
print(f"  {'m_A (1/length)':>22}{'mu^-1':>12}{'A^r':>12}{'dtheta/3H':>14}{'dQ/Q0':>12}{'  MOND ok?'}")
for label, mA in [("Q0 = 1/Mpc (SZ)", 1.0/Mpc),
                  ("1/(0.3 Mpc)", 1.0/(0.3*Mpc)),
                  ("1/(0.1 Mpc)", 1.0/(0.1*Mpc)),
                  ("1/(10 kpc)=gal", 1.0/(10*kpc)),
                  ("1/(1 kpc)", 1.0/(1*kpc))]:
    Ar = Q0*varphi_p/mA**2
    dth = Ar*dtheta_per_u; dQ = Ar*dQ_per_u
    muinv = 1.0/mA
    mond = "YES" if muinv > 1*Mpc-1 else ("marginal" if muinv>30*kpc else "NO -- MOND screened out")
    print(f"  {label:>22}{muinv/Mpc:>9.3f}Mpc{Ar:>12.2e}{dth:>14.2e}{dQ:>12.2e}   {mond}")
print(f"""
  THE PINCER (both ways):
   * At the SZ mass m_A=Q0=1/Mpc (required for galaxy MOND): A^r~{Q0*varphi_p/Q0**2:.1e},
     dtheta/3H~{Q0*varphi_p/Q0**2*dtheta_per_u:.1f} (theta SWAMPED), dQ/Q0~{Q0*varphi_p/Q0**2*dQ_per_u:.1e} (Q PINNED).
   * To pin theta (dtheta/3H<0.1) you need A^r<{0.1/dtheta_per_u:.1e}, i.e. m_A> {np.sqrt(Q0*varphi_p/(0.1/dtheta_per_u)):.2e}/m
     = 1/({1/np.sqrt(Q0*varphi_p/(0.1/dtheta_per_u))/kpc:.0f} kpc) -- a screening length SHORTER than a galaxy,
     which SCREENS OUT the MOND behavior SZ built the theory to produce. CONTRADICTION.
  => There is NO m_A that pins theta AND keeps galaxy MOND. The MOND requirement mu^-1>~1Mpc CAPS
     the aether stiffness exactly where the sourced tilt gives theta an O(few) wobble. theta is
     structurally exposed; Q is structurally safe. Both-ways CLOSED in favor of: theta SWAMPED, Q PINNED.

  honest caveat: 'theta SWAMPED' means dtheta/3H = O(1)-O(10), i.e. the LOCAL theta is order-unity
  different from 3H -- NOT theta->0 and NOT theta->infinity; it is order-3H but not equal to 3H, so
  a0=(c/3Z)theta would carry an O(1) environmental/sign-uncertain factor. For the RISING carrier
  (already dead at CMB last turn) this is moot. For the DECLINING V(Q) fallback, which rides Q, the
  pinning of Q (~1e-9) is what matters and it is SAFE.\n""")
