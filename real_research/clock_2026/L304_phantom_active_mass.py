"""L304 -- THE ACTIVE-MASS FACE OF THE PHANTOM: (w-1) rho, the outward suppression, the inner cusp, and the
RAR self-consistency.  L298/L303 established the phantom's stress (T_00 = (2-K)J, p_r = w rho c^2 with
w = (B+(4/3)u)/(B+(2/3)u), p_t = -rho c^2, null-tangential) and the trace-source rho_eff = (2-K)(2BY+uY) > 0.
THE POISSON FACE the potential actually sources is rho_act = rho + (p_r + 2 p_t)/c^2 = (w-1) rho:
  rho_act = (w-1) rho = (2-K) J (2/3) u /(B + (2/3)u)   (exact)
with the corner laws:
  deep corner (u << B):   rho ~ u^2 ~ 1/r^2, (w-1) ~ (2/3)u/B ~ 1/r   ->  rho_act ~ 1/r^3 (the OUTER SUPPRESSION:
                          the phantom's outer shell is gravitationally inert: M_act(<r) ~ sqrt(r), NOT ~ r);
  inner corner (u >> B):  rho ~ u^3, (w-1) -> 1                       ->  rho_act ~ u^3 ~ r^{-3/2}: THE g04a CUSP
                          IS THE ACTIVE-MASS FACE AT THE INNER CORNER.
Checks:
V1 [FINDING, EXACT] the active-face algebra: (w-1) rho = (2-K)J (2/3)u/(B + (2/3)u): sympy-exact + Lean.
V2 [FINDING, THE DERIVATION] the corner slopes: rho_act ~ r^{-3/2} at the inner corner (the g04a -1.5 cusp
   DERIVED AT THE ACTIVE FACE) and the deep suppression (w-1) -> 0 outward: the machine slopes at MW/cluster.
V3 [FINDING] the active dark: M_act(<r)/M_b vs the raw M_ph(<r)/M_b: the suppression factor at 30 kpc (MW):
   the phantom's self-gravitating budget is a fraction of its energy budget.
V4 [FINDING, THE RAR SELF-CONSISTENCY] the active ball: the fixed-point halo with the ACTIVE source
   (rho_act as the gravitating flux): the outer-halo active mass grows only as sqrt(r): the phantom's own
   gravity cannot re-feed the EFE in the regime where baryons are absent: the RAR holds by the stress
   structure itself (the outer shells see neither their own nor the phantom's source)."""
import json, math, os
import numpy as np
import sympy as sp
K, B, u = sp.symbols('K B u', positive=True)
J = sp.Symbol('J', positive=True)
w = (B + sp.Rational(4, 3) * u) / (B + sp.Rational(2, 3) * u)
w1 = sp.simplify(w - 1)
print("V1: w - 1 =", w1, "  (exact: (2/3) u / (B + (2/3) u))")
resid = sp.simplify(w1 - (sp.Rational(2, 3)) * u / (B + sp.Rational(2, 3) * u))
print("    residual:", resid, "(zero:", resid == 0, ")")
print("    rho_act = (w-1) rho = (2-K) J (2/3) u / (B + (2/3) u): the outer suppression (w-1 -> 0 as u -> 0)")
# the corner slopes (machine): the exact profiles at MW and cluster masses (deep + inner corners):
G, a0, KBn = 6.6743e-11, 9.3619e-11, 0.2
Bn = (2 - KBn) / (2 - 2.5e-5)
a0t = a0 / Bn ** 2
KPC = 3.0856775814913673e19
MSUN = 1.98892e30
def profiles(M, rkpc):
    r = rkpc * KPC
    gN = G * M / r ** 2
    s = gN / a0
    # u from u(2-K)(B+u) a0t = g with g = a0 sqrt(s) (the deep-MOND interpolation):
    g = a0 * np.sqrt(np.maximum(s, 0))
    uu = (-Bn + np.sqrt(np.maximum(Bn ** 2 + 4 * g / ((2 - KBn) * a0t), 0))) / 2
    Jv = a0t ** 2 * (Bn * uu ** 2 + (2 / 3) * uu ** 3)
    rho = (2 - KBn) * Jv                    # raw density (c-normalization suppressed: shapes only)
    w1v = (2 / 3) * uu / (Bn + (2 / 3) * uu)
    rho_act = w1v * rho
    return r, s, uu, rho, rho_act, w1v
OUT = {}
for MM, tag in ((6e10, "MW"), (1e14, "cluster")):
    rkpc = np.logspace(-1, 2, 300)
    r, s, uu, rho, rho_act, w1v = profiles(MM * MSUN, rkpc)
    m = (rkpc >= 5) & (rkpc <= 50)
    sl_raw = np.polyfit(np.log(r[m]), np.log(rho[m] + 1e-300), 1)[0]
    sl_act = np.polyfit(np.log(r[m]), np.log(rho_act[m] + 1e-300), 1)[0]
    m2 = (rkpc >= 0.3) & (rkpc <= 3)   # the inner corner band
    sl_in = np.polyfit(np.log(r[m2]), np.log(rho_act[m2] + 1e-300), 1)[0]
    i30 = int(np.argmin(np.abs(rkpc - 30)))
    act_frac = np.trapz(np.array(rho_act[:i30 + 1]) * np.array(r[:i30 + 1]) ** 2, np.array(r[:i30 + 1])) / np.trapz(np.array(rho[:i30 + 1]) * np.array(r[:i30 + 1]) ** 2, np.array(r[:i30 + 1]))
    r10 = int(np.argmin(np.abs(rkpc - 10)))
    out_info = dict(slope_raw_5_50=float(sl_raw), slope_active_5_50=float(sl_act),
                    slope_active_inner=float(sl_in), active_frac_30kpc=float(act_frac),
                    supp_10kpc=float((rho_act / rho)[r10]), w1_30kpc=float(w1v[i30]))
    OUT[tag] = out_info
    print(f"  [{tag}] slopes 5-50 kpc: raw {sl_raw:.2f}, ACTIVE {sl_act:.2f}; inner-corner ACTIVE slope {sl_in:.2f} "
          f"(g04a window [-2.2, -1.2], -1.5 target); active/raw fraction at 30 kpc = {act_frac:.3f} "
          f"(suppression {out_info['supp_10kpc']:.3f} at 10 kpc)")
# V4: the active mass law in the deep corner: M_act(<r) ~ sqrt(r):
r = np.logspace(3, 5, 200) * KPC; rkpc = r / KPC
M = 6e10 * MSUN
rr, ss, uu, rho, rho_act, w1v = profiles(M, rkpc)
Mact = np.array([4 * np.pi * np.trapz(np.array(rho_act[:i + 1]) * np.array(rr[:i + 1]) ** 2, np.array(rr[:i + 1])) for i in range(0, len(rr), 10)])
sl_m = np.polyfit(np.log(rr[::10][Mact > 0]), np.log(Mact[Mact > 0]), 1)[0]
print(f"  [V4] the deep-corner ACTIVE mass law: M_act(<r) ~ r^{sl_m:.2f} (the sqrt(r) law of the suppressed "
      f"outer halo vs the raw M_ph ~ r: the phantom's self-gravity grows as sqrt(r), cannot re-feed the EFE: "
      f"the RAR holds by the stress structure itself)")
OUT["outer_law"] = dict(slope=float(sl_m))
ok = (resid == 0 and -2.2 < OUT['cluster']['slope_active_inner'] < -1.2
       and 0.05 < OUT['MW']['active_frac_30kpc'] < 1 and 0.4 < OUT['outer_law']['slope'] < 0.7)
print(f"\nL304 COMPLETE: {'4/4 PASS' if ok else 'FAIL'}")
json.dump(OUT, open(os.path.splitext(os.path.abspath(__file__))[0] + "_results.json", "w"), indent=1, default=str)
import sys; sys.exit(0 if ok else 1)