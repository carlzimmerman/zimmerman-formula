#!/usr/bin/env python3
"""
DOES THE DISFORMAL LENSING SOLUTION SURVIVE GW170817? (the referee's BLOCKER, checked honestly)
Framework: light couples to g~ = g + B u_mu u_nu, B = 4(Phi_bar - Phi_MOND)/c^2 (the disformal
strength that gives dark-matter-free lensing). Photons on g~ are SUBLUMINAL vs the gravitational
metric g (and vs gravitons, which stay on g) by fractional (B/2). GW170817 bound: gamma-rays and
GWs from NGC 4993 (D~40 Mpc) arrived within ~1.7 s -> |Delta c|/c < ~1e-15.
Differential photon-vs-graviton delay:  Delta t = (1/c) INT (B/2) dl  along the line of sight.
Compute B along a realistic GW170817 sightline and compare to 1.7 s.
"""
import numpy as np
c=2.998e8; kpc=3.086e19; Mpc=1e3*kpc; G=6.674e-11; Msun=1.989e30; a0=9.36e-11

def nu(gbar): return np.sqrt(1+np.sqrt(1+4*a0/np.maximum(gbar,1e-30)))/np.sqrt(2)

# --- B(r) for a galaxy: B = 4(Phi_bar - Phi_MOND)/c^2 ---
# deep-MOND flat-curve potential Phi_MOND ~ v_c^2 ln(r), Phi_bar ~ -GM/r; the disformal strength
# is set by the ENHANCEMENT. Use the RAR: g_obs=nu*g_bar; the extra potential integrates the extra field.
def B_profile(r, M):
    gbar = G*M/r**2
    n = nu(gbar)
    # extra (MOND) acceleration g_obs-g_bar = (nu-1)*g_bar; extra potential ~ INT (nu-1)g_bar dr'
    # local proxy for B: B ~ 4*(nu-1)*|Phi_bar|/c^2 with |Phi_bar|~GM/r (order-of-magnitude, generous)
    Phi = G*M/r
    return 4*(n-1)*Phi/c**2

# GW170817 sightline: mostly empty IGM (B~0, Phi->0 far from mass) + host NGC 4993 + Milky Way halo.
# Model each galaxy crossing: photon exits/enters through the deep-MOND shell (r ~ 5-100 kpc).
def galaxy_crossing_delay(M, r_in=5*kpc, r_out=100*kpc, N=2000):
    r = np.linspace(r_in, r_out, N)
    B = B_profile(r, M)
    dl = r[1]-r[0]
    dt = np.trapz(B/2, r)/c            # INT (B/2) dl / c  across the shell (one crossing)
    return dt, B.max()

print("="*74)
print("GW170817 DISFORMAL DELAY (photon on g~ vs graviton on g)")
print("="*74)
M_host = 1e11*Msun     # NGC 4993 ~ early-type, M_bar ~ 1e11 Msun
M_mw   = 6e10*Msun     # Milky Way baryonic
dt_host, Bmax_h = galaxy_crossing_delay(M_host)
dt_mw,   Bmax_m = galaxy_crossing_delay(M_mw)
dt_total = dt_host + dt_mw
D = 40*Mpc; t_travel = D/c
print(f"\n host galaxy (NGC 4993, M_bar~1e11 Msun): B_max~{Bmax_h:.2e}, crossing delay ~ {dt_host:.3e} s")
print(f" Milky Way    (M_bar~6e10 Msun):          B_max~{Bmax_m:.2e}, crossing delay ~ {dt_mw:.3e} s")
print(f" IGM (Phi->0 -> B->0): negligible")
print(f"\n TOTAL differential delay Delta_t ~ {dt_total:.3e} s")
print(f" travel time t = D/c = {t_travel:.3e} s ({D/Mpc:.0f} Mpc)")
print(f" fractional |Delta c|/c ~ Delta_t / t = {dt_total/t_travel:.3e}")
print(f"\n GW170817 bound: Delta_t < 1.7 s  AND  |Delta c|/c < ~1e-15")
viol_t = dt_total/1.7
viol_frac = (dt_total/t_travel)/1e-15
print(f" -> Delta_t / 1.7s      = {viol_t:.2e}   ({'PASS' if viol_t<1 else 'VIOLATED by %.0e'%viol_t})")
print(f" -> (Dc/c) / 1e-15      = {viol_frac:.2e}   ({'PASS' if viol_frac<1 else 'VIOLATED by %.0e'%viol_frac})")
print("\n"+"="*74)
print("HONEST READ: B is set by the SAME nu that gives lensing, so it is O(1e-6) in the deep-MOND")
print("shell of a galaxy over ~tens of kpc. The photon-vs-graviton differential vastly exceeds the")
print("GW170817 bound -- this is the TeVeS bimetric problem, and the disformal lensing construction")
print("INHERITS it. The referee was RIGHT: 'passes GW170817 trivially' is FALSE for the photon sector.")
print("(Caveat: exact number depends on the B profile + the true sightline geometry; but the scale is")
print(" ~months of delay per galaxy crossing vs a 1.7s bound -- no plausible geometry rescues 15 orders.)")
