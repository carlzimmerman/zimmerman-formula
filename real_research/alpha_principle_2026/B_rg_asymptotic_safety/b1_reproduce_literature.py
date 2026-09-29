"""Lane B, script 1: reproduce the Harst-Reuter (arXiv:1101.6007) and Eichhorn-Versteegen (arXiv:1709.07252) numbers.
Usage: python3 b1_reproduce_literature.py [MUTATE]   (MUTATE flips the sign of the gravity term; must exit 1)."""
import sys
import numpy as np
from scipy.optimize import fsolve
from rg_common import *

MUT = "MUTATE" in sys.argv
fails = []
def chk(tag, ok, msg, gating=True):
    print(("  [PASS] " if ok else ("  [FAIL] " if gating else "  [NOTE-NOT-REPRODUCED] ")) + tag + "  " + msg)
    if gating and not ok:
        fails.append(tag)

print("MODE:", "MUTATE (gravity-term sign flipped in HR numerics, beta_G sign flipped in E-V)" if MUT else "NORMAL")
sgn = -1.0 if MUT else 1.0

# ---------------- Harst-Reuter ----------------
print("\nHR  Harst-Reuter NGFP2 (Einstein-Hilbert, optimised cutoff Phi11(0)=1, Phi22(0)=1/2)")
B1 = -(24 * 0.5 - 1.0) / (3 * np.pi)
gstar0 = -2 / B1
print(f"    B1(0) = -(24 Phi22 - Phi11)/(3 pi) = {B1:.5f};  g*(lambda0=0) = -2/B1 = {gstar0:.4f}   (paper: 1.71)")
chk("H0", abs(gstar0 - 1.71) / 1.71 < 0.01, f"g* = {gstar0:.4f} vs paper 1.71")

nF = 1
A1 = 2 * nF / (3 * np.pi)
def toy(gstar, nF=1, sign=sgn):
    A = 2 * nF / (3 * np.pi)
    return hr_run([(0.000510999, A)], gstar, 1.0, sign=sign)
u_num = toy(gstar0)
u_cl = hr_closed(A1, gstar0, 1.0, MPL / 0.000510999)
print(f"    n_F=1, g*={gstar0:.4f}: numeric 1/alpha_IR = {u_num:.4f}; closed form (5.6) = {u_cl:.4f}")
chk("H1", abs(u_num - u_cl) / u_cl < 0.005, f"numeric vs closed form rel diff {abs(u_num-u_cl)/u_cl:.2e} (tol 5e-3)")
chk("H2a", abs(u_num - 10.91) / 10.91 < 0.02, f"1/alpha_IR = {u_num:.3f} vs quoted 10.91 (tol 2%)")
u_num2 = toy(0.83)
print(f"    g*=0.83 (quoted lambda0=lambda*): numeric {u_num2:.4f}")
chk("H2b", abs(u_num2 - 10.96) / 10.96 < 0.02, f"1/alpha_IR = {u_num2:.3f} vs quoted 10.96 (tol 2%)")
alpha_star_13 = 9 * 1.0 * gstar0 / 13
chk("H5", abs(alpha_star_13 / np.pi - 0.38) / 0.38 < 0.03, f"alpha*/pi (n_F=13) = {alpha_star_13/np.pi:.4f} vs quoted 0.38")

# SM / MSSM (informational)
for name, A, quoted in (("SM", 41 / (20 * np.pi), 25.7), ("MSSM", 33 / (10 * np.pi), 41.3)):
    u = hr_run([(MZ, A)], gstar0, 1.0, sign=sgn)
    chk("H3-" + name, abs(u - quoted) / quoted < 0.03, f"alpha_1^-1(M_Z) = {u:.2f} vs quoted {quoted} (tol 3%; informational)", gating=False)
print(f"    (measured alpha_1^-1(M_Z) [GUT-normalised, (5/3) alpha_Y] = {0.6*ALPHA_INV_MZ*(1-S2W):.2f}; paper quotes 59.5)")

# H4 sensitivity
gs = np.geomspace(0.1, 10, 9)
us = [toy(g) for g in gs]
print("    sensitivity of 1/alpha_IR (n_F=1) to g* over [0.1,10] (coefficient c g* varies 100x):")
for g_, u_ in zip(gs, us):
    print(f"       g* = {g_:8.3f}   1/alpha_IR = {u_:.4f}")
spread = (max(us) - min(us)) / np.mean(us)
chk("H4", spread < 0.20 if not MUT else spread < 0.20, f"relative spread over 100x in g*: {spread:.3f} (gating < 0.20)")
per_flavour = u_num / nF
nF_needed = ALPHA_INV0 / per_flavour
print(f"    real n_F needed for alpha^-1 = 137.036: {nF_needed:.3f} (n_F = 13 gives {13*per_flavour:.2f}, off by {(13*per_flavour/ALPHA_INV0-1)*100:.2f}%; n_F=12: {12*per_flavour:.2f})")
chk("H4b", min(abs(n * per_flavour / ALPHA_INV0 - 1) for n in range(1, 30)) > 1e-3, "no integer n_F hits 137.036 to 1e-3 in the toy")

# ---------------- Eichhorn-Versteegen ----------------
print("\nEV  Eichhorn-Versteegen: fixed point of (4.8)-(4.9), SM matter N_D=45/2, N_S=4, N_V=12")
ND, NS, NV = 22.5, 4.0, 12.0
s = -1.0 if MUT else 1.0
def betas(x):
    G, L = x
    d = 1 - 2 * L
    bG = 2 * G + G**2 / (6 * np.pi) * (2 * ND + NS - 4 * NV) - s * G**2 / (6 * np.pi) * (14 + 6 / d + 9 / d**2)
    bL = (-2 * L + G / (4 * np.pi) * (NS - 4 * ND + 2 * NV) + G * L / (6 * np.pi) * (2 * ND + NS - 4 * NV)
          - 3 * G / (2 * np.pi) - 7 * G * L / (3 * np.pi) - 3 * G / (4 * np.pi * d**2) + 7 * G / (4 * np.pi * d))
    return [bG, bL]
roots = set()
for G0 in np.linspace(0.1, 6, 12):
    for L0 in np.linspace(-8, 0.4, 15):
        sol, info, ier, _ = fsolve(betas, [G0, L0], full_output=True)
        if ier == 1 and sol[0] > 1e-6 and abs(1 - 2 * sol[1]) > 1e-3 and np.max(np.abs(betas(sol))) < 1e-9:
            roots.add((round(sol[0], 4), round(sol[1], 4)))
print("    non-Gaussian roots found (G*, Lambda*):", sorted(roots))
Gs = Ls = None
for G_, L_ in sorted(roots):
    if abs(G_ - 2.73) < 0.3 and abs(L_ + 3.76) < 0.5:
        Gs, Ls = G_, L_
chk("E1", Gs is not None and abs(Gs - 2.73) / 2.73 < 0.02 and abs(Ls + 3.76) / 3.76 < 0.02,
    f"fixed point (G*, Lambda*) = ({Gs}, {Ls}) vs paper (2.73, -3.76), tol 2%")
if Gs is not None:
    d = 1 - 2 * Ls
    fg = Gs * (1 - 4 * Ls) / (4 * np.pi * d**2)
    gY_star = 4 * np.pi * np.sqrt(6 * fg / 41)
    bY = 41 / 6
    def gIR(gstar, k=173.0):
        inv = 1 / gstar**2 + bY / (8 * np.pi**2) * np.log(MPL / k)
        return 1 / np.sqrt(inv)
    g173 = gIR(gY_star)
    print(f"    f_g = {fg:.5f}; g_Y* = {gY_star:.4f}; g_Y(173 GeV) = {g173:.4f}")
    chk("E2", abs(gY_star - 1.05) / 1.05 < 0.02 and abs(g173 - 0.487) / 0.487 < 0.02,
        f"g_Y* = {gY_star:.4f} (paper 1.05), g_Y(173) = {g173:.4f} (paper 0.487)")
    # required f_g
    aY_mz = ALPHA_INV_MZ * (1 - S2W)
    aY_mt = aY_mz - bY / (2 * np.pi) * np.log(173.0 / MZ)
    g_meas = np.sqrt(4 * np.pi / aY_mt)
    print(f"    measured g_Y(173 GeV) from alpha(M_Z), sin^2 theta_W, SM one-loop = {g_meas:.4f} (paper: 0.358)")
    inv_target = 1 / g_meas**2 - bY / (8 * np.pi**2) * np.log(MPL / 173.0)
    gstar_req = 1 / np.sqrt(inv_target)
    f_req = bY * gstar_req**2 / (16 * np.pi**2)
    print(f"    required g_Y* = {gstar_req:.4f}; required f_g = {f_req:.6f} = {f_req*np.pi**2:.4f}/pi^2 (paper: 0.096/pi^2 = {0.096/np.pi**2:.6f})")
    chk("E3", abs(f_req * np.pi**2 - 0.096) / 0.096 < 0.03, f"f_g,req pi^2 = {f_req*np.pi**2:.4f} vs 0.096 (tol 3%)")
    # elasticity
    eps = 1e-4
    lo, hi = f_req * (1 - eps), f_req * (1 + eps)
    gi = lambda f: gIR(4 * np.pi * np.sqrt(6 * f / 41))
    el = (np.log(gi(hi)) - np.log(gi(lo))) / (np.log(hi) - np.log(lo))
    print(f"    elasticity d ln g_Y(173)/d ln f_g at f_req = {el:.4f}")
    prec = 1e-3 / (2 * el)   # alpha ~ g^2 => d alpha/alpha = 2 el df/f
    print(f"    for alpha_Y to 1e-3 need f_g to relative {prec:.4f}; published-truncation f_g = {fg:.4f} is {fg/f_req:.2f}x the required value")
    chk("E3b", fg / f_req > 2, f"published-truncation f_g exceeds the required one by {fg/f_req:.2f}x (so g_Y(173) overshoots by {(g173/g_meas-1)*100:.0f}%)")
    print("    per arXiv:2508.03563 f_g is regulator/gauge dependent; f_g = 0 is possible with some regulators; with SM matter no PMS point was found.")

# E4: g_2 has no interacting FP
print("\nE4  SU(2): beta_2 = -b g^3/(16 pi^2) - f g with b = 19/6 > 0 (asymptotic freedom) and f >= 0")
import sympy as sp
g, f = sp.symbols("g f", real=True)
sol = sp.solve(sp.Eq(-sp.Rational(19, 6) * g**3 / (16 * sp.pi**2) - f * g, 0), g)
real_roots_pos_f = [r for r in sol if r.subs(f, 0.05).is_real]
print("    roots at f = 0.05:", [sp.N(r.subs(f, 0.05)) for r in sol])
chk("E4", len(real_roots_pos_f) == 1 and sp.simplify(real_roots_pos_f[0]) == 0, "only g_2 = 0 is a real fixed point for f >= 0: no predictive interacting FP for SU(2)")

print("\nCHECKS FAILED:" , fails if fails else "none")
sys.exit(1 if fails else 0)
