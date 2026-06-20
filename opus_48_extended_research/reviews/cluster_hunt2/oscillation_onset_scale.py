#!/usr/bin/env python3
"""
ROUTE B, decisive sub-calc: WHERE does the AeST mu^2*Phi enhancement turn on?

Durakovic-Skordis 2312.00889 Eq.(2.42): the oscillation/enhancement onset scale
    r_C ~ (1/3) * ( 18 r_hat_M / mu^2 * 1/(1+3|Delta|) )^(1/3)
with r_hat_M = lam_s rM/(1+lam_s) ~ rM (lam_s->inf), and
    rM = sqrt(G_N M / a0)   (the MOND radius, Eq.2.41).

The RAR PEAK (enhancement above MOND) and the gas COMPRESSION both happen
*after the MOND limit occurs* and are governed by the mu^2*Phi term, which
"becomes important at very large distances away from sources" (their text,
Eq.2.33 discussion). The screening length is 1/mu.

If r_C >> 420 kpc (the core), the enhancement is in the OUTSKIRTS and cannot
close the core undershoot -> AeST's core undershoot is FINAL.
If r_C <~ 420 kpc for some viable mu, the enhancement reaches the core.

But 1/mu is ALSO constrained: the mu^2*Phi term must NOT spoil galaxy rotation
curves (it adds an oscillatory/antigravity force at r > 1/mu). The banked value
1/mu = 3-97 Mpc comes from the AeST CMB/cosmology fit. We test both the banked
range AND an aggressive small-1/mu push to see what it would TAKE.
"""
import numpy as np

G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.086e19
Mpc  = 1000.0*kpc
a0   = 9.36e-11

def rM(M):  # MOND radius
    return np.sqrt(G*M/a0)

def r_C(M, inv_mu, Delta=0.0, lam_s=np.inf):
    """oscillation onset radius, Eq.2.42 (vacuum estimate)."""
    rm = rM(M)
    rhat = (lam_s/(1+lam_s))*rm if np.isfinite(lam_s) else rm
    mu2_phys = (1.0/inv_mu)**2
    # Eq.2.42 uses dimensionless mu_hat^2 = mu^2 rM^2; reconstruct physical:
    # r_C ~ (1/3) ( 18 rhat / (mu_hat^2/rM^2) * 1/(1+3|Delta|) )^(1/3)
    #     = (1/3) ( 18 rhat rM^2 / mu_hat^2 ... )  -- keep it physical:
    # Eq is dimensionless in r/rM; restore: r_C/rM = (1/3)(18 r_hat/rM /mu_hat^2 ...)^(1/3)
    mu_hat2 = mu2_phys*rm**2
    rc_over_rM = (1.0/3.0)*(18.0*(rhat/rm)/mu_hat2 * 1.0/(1.0+3.0*abs(Delta)))**(1.0/3.0)
    return rc_over_rM*rm

if __name__ == "__main__":
    print("="*70)
    print("AeST enhancement ONSET scale r_C  vs the 420 kpc cluster core")
    print("="*70)
    R_core = 420.0*kpc

    print("\nRich cluster M=1e15 Msun:  rM = %.2f Mpc"%(rM(1e15*Msun)/Mpc))
    print("%-14s %-14s %-14s %-10s"%("1/mu [Mpc]","r_C [Mpc]","r_C/420kpc","reaches core?"))
    for M in [1e15*Msun]:
        for inv_mu in [0.1*Mpc,0.3*Mpc,1.0*Mpc,3.0*Mpc,10.0*Mpc,30.0*Mpc,97.0*Mpc]:
            rc = r_C(M, inv_mu)
            print("%-14.2f %-14.3f %-14.2f %-10s"%(
                inv_mu/Mpc, rc/Mpc, rc/R_core,
                "YES" if rc<R_core else "no (outskirts)"))

    print("\nBanked AeST CMB-fit screening length: 1/mu = 3-97 Mpc")
    print("  => r_C(1/mu=3 Mpc)  = %.2f Mpc = %.1f x core"%(
        r_C(1e15*Msun,3*Mpc)/Mpc, r_C(1e15*Msun,3*Mpc)/R_core))
    print("  => r_C(1/mu=97 Mpc) = %.2f Mpc = %.1f x core"%(
        r_C(1e15*Msun,97*Mpc)/Mpc, r_C(1e15*Msun,97*Mpc)/R_core))

    # What 1/mu would push r_C INTO the core?
    from scipy.optimize import brentq
    f = lambda log_invmu: r_C(1e15*Msun, 10**log_invmu) - R_core
    try:
        sol = brentq(f, np.log10(0.01*Mpc), np.log10(200*Mpc))
        print("\n1/mu needed to put r_C = 420 kpc:  1/mu = %.3f Mpc"%(10**sol/Mpc))
    except Exception as e:
        print("brentq:", e)
