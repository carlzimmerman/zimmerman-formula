#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""g03m -- the candidate's dark sector against the cluster residual and KiDS, at the Jeans level.
The dark component is the scalar's Q-sector dust (g03e: rho_phi = Q0 C/a^3, sound speed zero on the homogeneous background since J_Y(0) = 0).
Inside a structure the scalar has a background gradient, and the dust perturbations acquire the kernel's own gradient stiffness: transverse J_Y(Y_loc),
so c_s^2 = 0.42 J_Y/|K_2| (c = 1; the normalisation from f34's small-k branch, c_s^2 = 0.042 at J_Y = 1, K_2 = -10, mixing included).
J_Y = g_N/g_phi from the completed kernel (g03j): exponential below y_tot = 1, saturated scalar force above (p = 0).  Jeans length lambda_J = c_s sqrt(pi/(G rho)).
A structure captures the dust where R/lambda_J > 1.  Representative environments (assumptions, stated): galaxy outskirts where KiDS measures (R = 100 kpc,
y = 0.05, rho = 1e-26 kg/m^3), galaxy core (5 kpc, y = 10, 1e-22), cluster at R500 (1 Mpc, y = 0.5 [the repository's own R500 = 0.33-0.58 a0], 1e-24),
cluster core (100 kpc, y = 5, 1e-23).  The ordering of R/lambda_J across environments is fixed by the kernel and the densities; |K_2| only scales all of
them together (R/lambda_J ~ sqrt|K_2|).  The question: is there a |K_2| window where clusters capture and galaxies do not?  Checks can fail."""
import math, numpy as np, sys
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
G, c, kpc, a0 = 6.6743e-11, 2.998e8, 3.0857e19, 9.3619e-11
KB = 0.2; Y1 = 1 - 1/math.e
def JY(y):
    """transverse stiffness g_N/g_phi of the completed kernel as a function of y = g_N/a0"""
    if y <= Y1:
        from scipy.optimize import brentq
        yt = brentq(lambda t: t*(1 - math.exp(-t)) - y, 1e-12, y + 60); return y/(yt*math.exp(-yt))
    return y/(1/math.e)                                                   # saturated scalar force a0/e (p = 0)
ENV = {"galaxy outskirts (KiDS)": (100*kpc, 0.05, 1e-26), "galaxy core": (5*kpc, 10.0, 1e-22), "cluster R500": (1000*kpc, 0.5, 1e-24), "cluster core": (100*kpc, 5.0, 1e-23)}
print("=" * 100); print("g03m -- dark-sector capture criterion R/lambda_J by environment (candidate kernel, corner K_B = 1/5)"); print("=" * 100)
def ratio(K2abs, R, y, rho):
    cs2 = 0.42*JY(y)/K2abs; cs = c*math.sqrt(cs2); lamJ = cs*math.sqrt(math.pi/(G*rho)); return R/lamJ, cs, lamJ
print(f"  {'environment':26s} {'R':>8s} {'y':>5s} {'J_Y':>8s} {'rho':>8s} | R/lambda_J at |K_2| = 1e6, 1e8, 1e10, 1e12")
tab = {}
for nm, (R, y, rho) in ENV.items():
    vals = [ratio(k, R, y, rho)[0] for k in (1e6, 1e8, 1e10, 1e12)]; tab[nm] = (R, y, rho)
    print(f"  {nm:26s} {R/kpc:6.0f}kpc {y:5.2f} {JY(y):8.3f} {rho:8.1e} | " + " ".join(f"{v:9.3e}" for v in vals))
# the |K_2| at which each environment starts to capture (R/lambda_J = 1): R/lambda_J = sqrt(|K_2|) * A  ->  |K_2|_cap = 1/A^2
K2cap = {nm: 1.0/ratio(1.0, *tab[nm])[0]**2 for nm in ENV}
print("\n  capture threshold |K_2| (R/lambda_J = 1) per environment: " + ", ".join(f"{nm}: {K2cap[nm]:.2e}" for nm in ENV))
order = sorted(ENV, key=lambda n: K2cap[n])
print("  capture order as |K_2| grows: " + " -> ".join(order))
check("J1 the cluster at R500 captures the dust at a smaller |K_2| than the galaxy outskirts where KiDS measures (the kernel's stiffness ordering J_Y(cluster) > J_Y(galaxy) is outweighed by the density and size ratios)",
      K2cap["cluster R500"] < K2cap["galaxy outskirts (KiDS)"], f"cluster R500 {K2cap['cluster R500']:.2e} vs galaxy outskirts {K2cap['galaxy outskirts (KiDS)']:.2e}")
lo, hi = K2cap["cluster R500"], K2cap["galaxy outskirts (KiDS)"]
print(f"\n  WINDOW: for {lo:.2e} < |K_2| < {hi:.2e} (a factor {hi/lo:.1f}) the cluster at R500 captures the scalar dust while the galaxy outskirts do not; galaxy cores capture at |K_2| > {K2cap['galaxy core']:.2e}, cluster cores at |K_2| > {K2cap['cluster core']:.2e}")
check("J2 a window in |K_2| exists (wider than a factor 3) in which clusters at R500 capture the dust and galaxy outskirts do not, so the KiDS-versus-cluster pincer is not automatic for this dark sector at the Jeans level",
      hi/lo > 3, f"factor {hi/lo:.1f}")
check("J3 inside the window galaxy cores never capture the dust (their threshold lies above the window top: the RAR in galaxies is untouched), while cluster cores capture in the window's upper part (|K_2| > 2.5e8): the residual can sit in cluster outskirts or throughout, depending on K_2",
      K2cap["galaxy core"] > hi and lo < K2cap["cluster core"] < hi, f"galaxy core {K2cap['galaxy core']:.2e} > window top {hi:.2e}; cluster core {K2cap['cluster core']:.2e} inside the window")
# consistency with the rest of the corner: f34b's health is K_2-independent in sign; c_s of the MOND scalar branch in the Solar System / wide binaries at |K_2| in the window
K2mid = math.sqrt(lo*hi); cs2_wb = 0.42*JY(1.9*math.exp(-1.9)/(1 - math.exp(-1.9))*0 + 1.9)/K2mid
print(f"  at |K_2| = {K2mid:.1e} (window centre): MOND-scalar sound speed at the Galactic field c_s = {c*math.sqrt(cs2_wb):.1e} m/s (the Bogoliubov branch; irrelevant for statics), a^-6 cosmological correction coefficient 1/(4 K_2) negligible")
print("\n  what this does and does not establish: the ordering is kernel-fixed and the window is a Jeans-level statement with representative densities; the FRACTIONS (KiDS <= 14% around galaxies, clusters 32-46%) need the dust's accretion and virialisation in the candidate's potential wells, which the repository's virialisation front (nbody) left open. Not a solution of the cluster residual; a door that is not shut.")
print(f"\nRESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "\nRESULT: 0 FAIL"); sys.exit(1 if FAILS else 0)
