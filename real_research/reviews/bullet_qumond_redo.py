#!/usr/bin/env python3
"""
The Bullet Cluster, done right (v2): a FAIR QUMOND phantom-mass calculation.
===========================================================================
Carl's challenge: how was the Bullet measured, did it assume local a0, redo it.

MEASUREMENT (what it assumes):
  Clowe+2006 reconstruct the lensing CONVERGENCE kappa(x) model-independently --
  NO assumption about the gravity law or a0. The famous OFFSET (kappa peaks on
  the galaxies, not the dominant X-ray gas) is a geometric fact about where light
  bends. a0 enters only when a THEORY predicts kappa from the baryons. And the
  naive 'MOND gravity is centred on the gas so kappa must peak on the gas' is the
  WRONG prediction: QUMOND phantom mass is a NONLINEAR functional of baryon
  DENSITY, so kappa need not trace baryonic surface density (Angus+2006).

THIS SCRIPT -- an HONEST test of the density-weighting mechanism (Hernandez 2026):
  A FAIR setup: the diffuse GAS dominates the baryonic surface density (as in the
  real Bullet). Then ask: can the QUMOND phantom pull the TOTAL lensing peak onto
  the minor, more-compact GALAXIES? And how sensitive is that to galaxy compactness?
       rho_p = (1/4 pi G) div[ (nu(|grad Phi_N|/a0) - 1) grad Phi_N ],
       nu(x) = 1/2 [1 + sqrt(1 + 4/x)]      (the 'simple' nu, as Hernandez).
  We SCAN the galaxy concentration scale b_gal and report, for each: whether the
  BARYONS alone peak on gas (fairness check), and whether the TOTAL kappa flips
  onto the galaxies. Needs numpy. ~10 s.
"""
import numpy as np

G, Msun, kpc = 6.674e-11, 1.989e30, 3.0857e19
A0 = 1.2e-10

# Masses fixed at Hernandez 2026 ratios: gas 2.23e14 (93%), galaxies 1.70e13 (7%).
# Two galaxy clumps at x=-250,+350 kpc; two gas clumps (ram-slowed, lagging
# toward centre) at x=-120,+170 kpc with BROAD cores so the gas dominates the
# baryonic surface density. We scan the galaxy core scale b_gal.
GAL_M = [1.20e13, 0.50e13];  GAL_X = [-250.0, +350.0]
GAS   = [(1.55e14, -120.0, 200.0), (0.68e14, +170.0, 150.0)]   # (M, x0, b) kpc

N, L = 192, 3000.0*kpc
ax = (np.arange(N) - N//2) * (L/N);  d = L/N
X, Y, Zc = np.meshgrid(ax, ax, ax, indexing='ij')


def components(b_gal_kpc):
    C = [(M*Msun, x0*kpc, b_gal_kpc*kpc, 'gal') for M, x0 in zip(GAL_M, GAL_X)]
    C += [(M*Msun, x0*kpc, b*kpc, 'gas') for (M, x0, b) in GAS]
    return C


def gradPhiN(C):
    gx = np.zeros_like(X); gy = np.zeros_like(X); gz = np.zeros_like(X)
    for (M, x0, b, _) in C:
        dx, dy, dz = X-x0, Y, Zc
        s = (dx*dx+dy*dy+dz*dz+b*b)**1.5
        f = G*M/s; gx += f*dx; gy += f*dy; gz += f*dz
    return gx, gy, gz


def sigma_baryon(C):
    rho = np.zeros_like(X)
    for (M, x0, b, _) in C:
        dx, dy, dz = X-x0, Y, Zc
        rho += 3*M*b*b/(4*np.pi)/(dx*dx+dy*dy+dz*dz+b*b)**2.5
    return np.sum(rho, axis=2)*d


def sigma_phantom(C, a0):
    gx, gy, gz = gradPhiN(C)
    g = np.sqrt(gx*gx+gy*gy+gz*gz)+1e-30
    nu = 0.5*(1.0+np.sqrt(1.0+4.0*a0/g))
    Vx, Vy, Vz = (nu-1)*gx, (nu-1)*gy, (nu-1)*gz
    rho_p = (np.gradient(Vx, d, axis=0)+np.gradient(Vy, d, axis=1)
             + np.gradient(Vz, d, axis=2))/(4*np.pi*G)
    return np.sum(rho_p, axis=2)*d, np.sum(rho_p)*d**3


def run(b_gal, a0=A0):
    C = components(b_gal)
    j0 = N//2; xk = ax/kpc
    Sb = sigma_baryon(C)[:, j0]
    Sp, Mp = sigma_phantom(C, a0)
    Spx = Sp[:, j0]
    St = Sb + Spx
    val = lambda A, xc: A[np.argmin(np.abs(xk-xc))]
    pk_b = xk[np.argmax(Sb)]; pk_t = xk[np.argmax(St)]
    near = lambda x, opts: opts[int(np.argmin([abs(x-o) for o in opts]))]
    onb = 'GAL' if near(pk_b, [-250,350,-120,170]) in (-250,350) else 'GAS'
    ont = 'GAL' if near(pk_t, [-250,350,-120,170]) in (-250,350) else 'GAS'
    Mb = sum(c[0] for c in C)/Msun
    print(f"  b_gal={b_gal:4.0f} kpc | baryon-only kappa peaks on {onb:3s} (x={pk_b:+4.0f}) "
          f"| TOTAL kappa peaks on {ont:3s} (x={pk_t:+4.0f})")
    print(f"            Sig_b:  gal(-250)={val(Sb,-250):.2e}  gas(-120)={val(Sb,-120):.2e}  "
          f"(gas/gal={val(Sb,-120)/val(Sb,-250):.2f})")
    print(f"            Sig_p:  gal(-250)={val(Spx,-250):.2e}  gas(-120)={val(Spx,-120):.2e}  "
          f"(gal/gas={val(Spx,-250)/val(Spx,-120):.2f})  Mphantom/Mbaryon={Mp/Msun/Mb:.2f}")
    return ont


def main():
    print("="*80)
    print("BULLET CLUSTER, DONE RIGHT (v2) -- fair QUMOND test, pure baryons, const a0")
    print("="*80)
    print("  Gas 2.23e14 Msun (93%, diffuse, dominates baryonic Sigma); galaxies 1.70e13")
    print("  (7%, compact). Does the QUMOND phantom flip the lensing peak onto galaxies?\n")
    print("  SCAN over galaxy compactness b_gal (smaller = more point-like):")
    flips = {b: run(b) for b in (40, 70, 100, 150)}
    print()
    # evolution check at the compact end
    print("  EVOLUTION check (b_gal=40): constant a0 vs a0(z=0.296)=+17%:")
    run(40, A0); run(40, A0*np.sqrt(0.315*1.296**3+0.685))
    print("\n"+"="*80); print("HONEST VERDICT"); print("="*80)
    print(f"""  * In every FAIR case (gas dominates the baryonic Sigma, b_gal >= 70 kpc) the
    QUMOND phantom comes out SLIGHTLY HIGHER ON THE GAS (Sig_p gal/gas ~ 0.6-0.8),
    and the total lensing peak STAYS ON THE GAS. The one case that peaks on the
    galaxies (b_gal=40) is a cheat -- there the BARYONIC Sigma already peaks on the
    over-compact galaxies (gas/gal=0.43), so it is baryons, not the phantom.
    => my schematic toy does NOT reproduce a clean pure-baryon offset. The density-
    weighting effect is real but, smoothed to blob-scale galaxies, TOO WEAK to flip
    the peak. I cannot independently certify Hernandez's strong claim.
  * Why the gap with Hernandez 2026: he models galaxies as INDIVIDUAL compact
    sources (each ~10-30 kpc, sharp 1/R phantom spikes) on the REAL beta-model gas;
    my blobs (b_gal>=70) wash those spikes out. His result hinges on that compact
    modelling -- a real but uncertain choice, which is exactly why it is contested
    (arXiv:2605.10022 still finds a residual centred on the galaxies).
  * NET, honestly: the offset is NOT the airtight falsification it is sold as
    (QUMOND nonlinearity gives a genuine offset mechanism, contra my earlier
    'must track the gas / needs neutrinos' -- that was wrong/outdated). But it is
    NOT cleanly resolved either (my toy + the residual literature). It is an OPEN,
    actively CONTESTED problem as of 2026 -- not a clean kill, not a clean win.
  * For THIS framework: a0 evolution is IRRELEVANT (+17% at z=0.296 moves nothing).
    The Bullet is entirely INHERITED constant-a0 MOND. It does not uniquely falsify
    the evolving-a0 idea; it rides on the SAME foundational question already flagged
    as risk #1 -- 'is MOND real?' -- not an independent kill-shot.""")
    print("="*80)


if __name__ == "__main__":
    main()
