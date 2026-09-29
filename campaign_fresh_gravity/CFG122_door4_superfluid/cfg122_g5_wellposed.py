#!/usr/bin/env python3
"""CFG122 G5.1 (ghost / gradient stability) -- second variation of the coupled system about the static solution in spherical symmetry (sympy), in the regions X > 0 and X < 0.
   L = P(X) - (alpha Lam/M_Pl) phi rho_b,  X = mu + phi_t - m Phi - (grad phi)^2/(2m);  perturb phi = phi0(r) + psi(r, t):
   L2 = (1/2) P_XX (psi_t - v.grad psi)^2 - P_X (grad psi)^2/(2m)   (v = grad phi0/m; Phi-perturbations and the linear coupling do not enter the principal part)
   kinetic coefficient K_t = P_XX, radial dispersion (omega - k v)^2 = c_s^2 k^2 with c_s^2 = P_X/(m P_XX).
   MUTATE=b: P(|X|) (even in X) instead of P = X sqrt|X|  -- the frozen control 'G5.1 must flip to well-posed'.
Run: python3 cfg122_g5_wellposed.py"""
import os, sys, math
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg122_common import Report

MUT = os.environ.get("MUTATE", "")
R = Report("cfg122_g5_wellposed")
P, check = R.P, R.check
m, Lam, k, v = sp.symbols("m Lambda k v", positive=True)
Xp = sp.symbols("Xp", positive=True)         # a positive number standing for |X|
c0 = 2 * Lam * (2 * m) ** sp.Rational(3, 2) / 3


R.banner(f"G5.1 second variation  (MUTATE={MUT!r})")
out = {}
for region in ("pos", "neg"):
    if region == "pos":
        X = Xp
    else:
        X = -Xp
    if MUT == "b":
        Pe = c0 * Xp ** sp.Rational(3, 2)                       # P(|X|) = c0 |X|^(3/2) on both sides
        # derivatives w.r.t. X (X = +-Xp): d/dX = +-d/dXp
        s = 1 if region == "pos" else -1
        PX = s * sp.diff(Pe, Xp)
        PXX = sp.diff(Pe, Xp, 2)
    else:
        Pe = c0 * Xp ** sp.Rational(3, 2) if region == "pos" else -c0 * Xp ** sp.Rational(3, 2)
        s = 1 if region == "pos" else -1
        PX = s * sp.diff(Pe, Xp)
        PXX = sp.diff(Pe, Xp, 2)
    PX, PXX = sp.simplify(PX), sp.simplify(PXX)
    cs2 = sp.simplify(PX / (m * PXX))
    kin_sign = sp.sign(PXX)
    out[region] = (PX, PXX, cs2)
    P(f"  region {'X > 0' if region == 'pos' else 'X < 0'}:  n = P_X = {PX};  K_t = P_XX = {PXX};  c_s^2 = P_X/(m P_XX) = {cs2}")
# well-posedness rule: K_t > 0 and c_s^2 > 0 and n > 0
wp = {}
for region, (PX, PXX, cs2) in out.items():
    wp[region] = dict(n_positive=bool(sp.simplify(PX) .is_positive), kinetic_positive=bool(sp.simplify(PXX).is_positive), cs2_positive=bool(sp.simplify(cs2).is_positive))
    P(f"    {region}: density n > 0: {wp[region]['n_positive']};  kinetic P_XX > 0: {wp[region]['kinetic_positive']};  c_s^2 > 0: {wp[region]['cs2_positive']}")
R.num("wellposed", wp)
# elliptic growth rate in the ill-posed case: omega^2 = -|c_s^2| k^2 -> Gamma = |c_s| k
pos_ok = all(wp["pos"].values())
neg_ok = all(wp["neg"].values())
check("G5.1a  region X > 0 is well-posed (n > 0, K_t > 0, c_s^2 > 0)  [positive control: the harness can see a healthy region]", str(wp["pos"]), pos_ok)
check("G5.1b  region X < 0 (the gradient-dominated, MOND-carrying region) is well-posed", str(wp["neg"]), neg_ok, load_bearing=False)
if MUT == "b":
    P("  MUTATE=b: the even P(|X|) removes the sign change of P_XX at X < 0 (K_t > 0) but P_X < 0 there (n < 0, negative DM density) and c_s^2 = P_X/(m P_XX) is still negative:"
      " the frozen control 'G5.1 must flip to well-posed' is checked below.")
R.verdict("G5.1-wellposed(X>0)", "PASS" if pos_ok else "FAIL", "healthy for X > 0: P_XX > 0, c_s^2 = 2X/m")
R.verdict("G5.1-wellposed(X<0)", "PASS" if neg_ok else "FAIL",
          "the gradient-dominated (MOND-carrying) regime X<0 has P_XX<0 and c_s^2 = 2X/m < 0: L2 = -(1/2)(|P_XX| psi_t^2 + (P_X/m) psi'^2), omega^2 = -|c_s^2| k^2: elliptic, growth rate Gamma = |c_s| k unbounded in k (Hadamard ill-posed)" if not neg_ok else "well-posed")
# numbers: growth rate of the X<0 instability at the galaxy: |c_s|^2 = 2|X|/m; deep regime |X| = sqrt(D) at r_M => |X| = alpha M_Pl a0/(2m)
from cfg122_common import a0_nat, MPL, KPC_EV, GYR_EV, HBAR_EV_S
a0n = a0_nat("canonical")
P("  size of the instability in the gradient regime at r_M: |X| = alpha M_Pl a0/(2 m), |c_s|^2 = alpha M_Pl a0/m^2 (c = 1); growth rate Gamma = |c_s| k")
for mm, aa in ((1.0, 1.0), (0.01, 1.0), (1.0, 100.0)):
    cs = math.sqrt(aa * MPL * a0n / mm ** 2)
    kpc_rate = cs / KPC_EV * (1.0 / (HBAR_EV_S)) * 3.15576e13     # rate for a 1/kpc mode in 1/Myr: |c_s| k [eV] / hbar
    P(f"    m = {mm:g} eV, alpha = {aa:g}: |c_s| = {cs:.3e} c = {cs * 299792.458:.4g} km/s; a mode of wavelength 2 pi kpc grows as exp({kpc_rate:.3g} t/Myr)")
    R.num(f"cs_growth_m{mm}_a{aa}", dict(cs_over_c=cs, rate_per_Myr_at_k_1_over_kpc=kpc_rate))
if MUT == "b":
    R.verdict("G5.1", "PASS" if (wp["neg"]["kinetic_positive"] and wp["neg"]["cs2_positive"] and wp["neg"]["n_positive"]) else "FAIL",
              "MUTATE=b control: does the even P(|X|) flip G5.1 to well-posed?  (frozen expectation: yes)")
else:
    R.verdict("G5.1", "PASS" if (pos_ok and neg_ok) else "FAIL", "the MOND-carrying regime (X<0) is ill-posed; the healthy regime (X>0) carries the linear fifth force, not the MOND force (see cfg122_g1_plane.py G5.1 rows)")
nf, gf = R.write()
sys.exit(1 if (nf or gf) else 0)
