"""Lane B, script 2: boundary values of alpha required at high scales to reach alpha^-1(0) = 137.036.
Usage: python3 b2_required_boundary.py [MUTATE]  (MUTATE uses MSSM coefficients in the 'SM does not unify' check; must exit 1)."""
import sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from rg_common import *

MUT = "MUTATE" in sys.argv
fails = []
def chk(tag, ok, msg, gating=True):
    print(("  [PASS] " if ok else ("  [FAIL] " if gating else "  [INFO-FAIL] ")) + tag + "  " + msg)
    if gating and not ok:
        fails.append(tag)
print("MODE:", "MUTATE (MSSM one-loop coefficients used in the unification check)" if MUT else "NORMAL")

# ---------- R1: naive QED-only thresholds 0 -> M_Z
print("\nR1  naive QED-only threshold running from alpha^-1(0) = 137.036 up to M_Z (fermions lighter than M_Z, one loop)")
for setno in (1, 2):
    inv = ALPHA_INV0
    for nm, m, ncq2 in fermions(setno):
        if m < MZ:
            inv -= (2 * ncq2 / (3 * np.pi)) * np.log(MZ / m)
    print(f"    SET ({setno}): alpha^-1(M_Z) = {inv:.3f}  vs measured {ALPHA_INV_MZ}  (gap {inv-ALPHA_INV_MZ:+.3f})")
print("    the gap is the non-perturbative hadronic vacuum polarisation ambiguity; below, the measured alpha^-1(M_Z) is used as the anchor.")

# ---------- R2: SM chain from measured alpha(M_Z)
aY, a2, a3 = alpha_inv_boundaries()
a1 = 0.6 * aY
print(f"\nR2  anchors at M_Z: alpha_Y^-1 = {aY:.3f}, alpha_1^-1(GUT) = {a1:.3f}, alpha_2^-1 = {a2:.3f}, alpha_3^-1 = {a3:.3f};  alpha_em^-1 = alpha_Y^-1 + alpha_2^-1 = {aY+a2:.3f}")
chk("R2a", abs(aY + a2 - ALPHA_INV_MZ) < 1e-9, "alpha_em^-1(M_Z) = alpha_Y^-1 + alpha_2^-1 identity")

# two-loop
bij = np.array([[199 / 50, 27 / 10, 44 / 5], [9 / 10, 35 / 6, 12], [11 / 10, 9 / 2, -26]])
ai = np.array([17 / 10, 3 / 2, 2])
b1l = np.array([41 / 10, -19 / 6, -7])
def rhs(t, y, twoloop=True):
    g = y[:3]; yt = y[3]
    k = 1 / (16 * np.pi**2)
    dg = k * g**3 * b1l
    if twoloop:
        dg = dg + k**2 * g**3 * (bij @ (g**2) - ai * yt**2)
    dyt = k * yt * (4.5 * yt**2 - 8 * g[2]**2 - 2.25 * g[1]**2 - 0.85 * g[0]**2)
    return np.concatenate([dg, [dyt]])
def run_two(M, twoloop=True):
    g0 = np.sqrt(4 * np.pi / np.array([a1, a2, a3]))
    y0 = np.concatenate([g0, [0.94]])
    sol = solve_ivp(rhs, [np.log(MZ), np.log(M)], y0, args=(twoloop,), rtol=1e-11, atol=1e-13)
    g = sol.y[:3, -1]
    return 4 * np.pi / g**2   # alpha_1^-1(GUT), alpha_2^-1, alpha_3^-1

# check that my ODE with twoloop=False reproduces the analytic one-loop
M = 1e16
an = run_oneloop(M)
nu = run_two(M, twoloop=False)
chk("R2b", abs(nu[1] - an[1]) < 1e-6 and abs(nu[0] - 0.6 * an[0]) < 1e-6 and abs(nu[2] - an[2]) < 1e-6, "ODE (one-loop switch) equals the analytic one-loop solution")

# crossing scale alpha_1 = alpha_2 (one loop)
Lx = (a1 - a2) / ((41 / 10) / (2 * np.pi) - (-19 / 6) / (2 * np.pi))
Mx = MZ * np.exp(Lx)
scales = [("M_Pl,red", MPL_RED), ("M_Planck", MPL), ("M_GUT=2e16", 2e16), ("a1=a2 crossing", Mx)]
print(f"\n    alpha_1 = alpha_2 (SM, one-loop) at M = {Mx:.3e} GeV with alpha^-1 = {a1 - (41/10)/(2*np.pi)*Lx:.3f}")
print("\n    Required boundary values (measured alpha at M_Z, SM content, thresholds as declared):")
print("    scale              M[GeV]      1-loop: aY^-1  a2^-1  a3^-1  aem^-1 | 2-loop: aY^-1  a2^-1  a3^-1  aem^-1 | rel(aem^-1) 2L/1L-1")
table = {}
for nm, M in scales:
    o = run_oneloop(M)
    t = run_two(M, True)
    aY_2 = t[0] / 0.6
    em1 = o[0] + o[1]; em2 = aY_2 + t[1]
    table[nm] = (o, (aY_2, t[1], t[2]), em1, em2)
    print(f"    {nm:16s} {M:10.3e}   {o[0]:7.3f} {o[1]:6.3f} {o[2]:6.3f} {em1:7.3f} |        {aY_2:7.3f} {t[1]:6.3f} {t[2]:6.3f} {em2:7.3f} | {em2/em1-1:+.4f}")
rel = abs(table["M_Planck"][3] / table["M_Planck"][2] - 1)
chk("R2c", rel > 1e-3, f"two-loop shifts alpha_em^-1(M_Planck) by {rel:.4f} > 1e-3: the one-loop required value cannot support a 1e-3 hit claim")

# ---------- R3: unification
print("\nR3  do the three SM couplings meet at one scale? (best scale minimising the max relative spread of alpha_i^-1)")
coef_SM = np.array([41 / 10, -19 / 6, -7.0])
coef_MSSM = np.array([33 / 5, 1.0, -3.0])
coef = coef_MSSM if MUT else coef_SM
def spread(L, c):
    v = np.array([a1, a2, a3]) - c / (2 * np.pi) * L
    return (v.max() - v.min()) / v.mean()
Ls = np.linspace(0, 45, 4501)
sp = [spread(L, coef) for L in Ls]
Lb = Ls[int(np.argmin(sp))]
print(f"    coefficients {'MSSM (control)' if MUT else 'SM'}: best spread {min(sp)*100:.2f}% at M = {MZ*np.exp(Lb):.3e} GeV")
spSM = min(spread(L, coef_SM) for L in Ls)
spMS = min(spread(L, coef_MSSM) for L in Ls)
print(f"    reference: SM best spread {spSM*100:.2f}%; MSSM-coefficient best spread {spMS*100:.2f}% (the MSSM would need unmeasured superpartner thresholds = new free inputs)")
chk("R3", min(sp) > 0.05, f"SM couplings do not unify: best spread {min(sp)*100:.1f}% > 5%")

# ---------- R4: U(1)_em-only toy anchored at M_Z
print("\nR4  U(1)_em-only toy (SM charged fermions, no W, no Higgs; anchored at measured alpha^-1(M_Z)); required alpha^-1 at scales:")
def em_only(M, setno=1):
    inv = ALPHA_INV_MZ
    for nm, m, ncq2 in fermions(setno):
        lo = max(m, MZ)
        if M > lo:
            inv -= (2 * ncq2 / (3 * np.pi)) * np.log(M / lo)
    return inv
emtab = {}
for nm, M in scales:
    emtab[nm] = em_only(M)
    print(f"    {nm:16s} alpha_em^-1(em-only toy) = {emtab[nm]:8.3f}   vs SM one-loop chain {table[nm][2]:8.3f}   ratio {emtab[nm]/table[nm][2]:.3f}")
chk("R4", abs(emtab["M_Planck"] / table["M_Planck"][2] - 1) > 0.05, "required boundary value depends on the assumed charged/gauge content by >5% (it is not a property of the U(1) alone)")

print("\nCHECKS FAILED:", fails if fails else "none")
sys.exit(1 if fails else 0)
