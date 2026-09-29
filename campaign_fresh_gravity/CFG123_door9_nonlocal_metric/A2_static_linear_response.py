#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A2_static_linear_response -- G1 of CFG123_FROZEN_CRITERIA.md: the linear static weak-field response of the localised RR model (and generic analytic DW)
against the CFG44 target, point mass and CFG44's exponential sphere.

Inputs derived in A1 (sympy, exact): RR leading order in m^2, prescription P0 (U -> 0 at infinity, S(0) = 0):
   rho_eff(r) = m^2 Phi_N(r) / (12 pi G)            (point mass: rho_eff = -m^2 M/(12 pi r), c1 = -1/3),
   delta g(r) = (m^2/6) S',  r^2 S' = int_0^r 2 Psi_N r'^2 dr'   (delta g = -(m^2 r^2/6) g_N for a point mass).
m = mu H0/c with mu = m/H0 from the RR background (reading R-A, cfg123_common.rr_fit_lambda): the ONLY input, not tuned.
DW (T0d): Phi' = g_N * const for point mass AND extended baryons => rho_eff = 0 relative to the measured G.

Frozen definitions and pass lines (G1): R_A = rho_eff/rho_target; PASS 0.90 <= |R_A| <= 1.10 at every grid point; G1-S: spread over x <= 1.20; G1-M: spread over M at fixed
x <= 1.20; G1-sign: rho_eff > 0; G1-X: the same on C_eff/[(a0/4 pi) M_b(<r)] for the exponential sphere.  |R_A| is used for G1-A and the sign is a separate line.
Grid: M = 1e9..1e12, x = r/r_M in XGRID, both a0 footings.
MUTATE=a  m replaced by the tuned m_req(M_ref = 1e11 Msun, x = 0.1)  (planted match, never a result)
MUTATE=b  m^2 -> -m^2 (sign flip)          MUTATE=d  the target's own rho_c is injected in place of rho_eff (comparator control)
Pre-registered claims: P1 (|R_A| in [1e-17, 1e-7], none within 10% of 1), P2 (spread > 1.2, shape sqrt(1+x^2) within 10%; AND the frozen text's 'about 300'), P3 (mass spread 1000 within 2%).
"""
import os, sys, math
import numpy as np
from scipy.special import gammainc
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg123_common import *

MUT = mutate_mode()
if MUT not in ("", "a", "b", "d"):
    print("A2: MUTATE mode", MUT, "not applicable"); sys.exit(3)
R = Report("A2_static_linear_response", MUT)
lam, sol = rr_background()
mu = math.sqrt(lam)
m_inv_m = mu * H0_SI / C_SI                                     # m in 1/m (RR, R-A)
R.banner(f"A2  G1 linear static response.  MUTATE={MUT or 'none'};  RR background: m^2/H0^2 = {lam:.6f}, m/H0 = {mu:.5f}, m = {m_inv_m:.4e} /m = 1/({1/m_inv_m/(C_SI/H0_SI):.4f} c/H0)")
sign_flip = -1.0 if MUT == "b" else 1.0
C1 = -1.0 / 3.0                                                   # from A1 (exact): rho_eff = C1 m^2 M/(4 pi r)

# ------------------------------------------------------------------------------------------------ point mass
def point_mass_tables(a0, m_use):
    out = {}
    for M in MASSES:
        Mkg = M * MSUN
        rM = rM_m(M, a0)
        row = []
        for xg in XGRID:
            r = xg * rM
            rho_eff = sign_flip * C1 * m_use ** 2 * Mkg / (4 * math.pi * r)
            rho_t = a0 / (4 * math.pi * G_SI * r * math.sqrt(1 + xg * xg))
            if MUT == "d":
                rho_eff = rho_t
            gN = G_SI * Mkg / r ** 2
            dg = sign_flip * (-(m_use ** 2) * r ** 2 / 6.0) * gN if MUT != "d" else math.nan
            gt = gN + (dg if MUT != "d" else 0.0)
            Ceff = rho_eff * r ** 3 * gt
            Ct = a0 * Mkg / (4 * math.pi)
            row.append(dict(x=xg, r_kpc=r / KPC, rho_eff=rho_eff, rho_t=rho_t, RA=rho_eff / rho_t, RC=Ceff / Ct))
        out[M] = row
    return out


def spreads(tab):
    """G1-S (per mass, over x) and G1-M (per x, over masses) spreads of |R_A|."""
    S = {M: max(abs(q["RA"]) for q in tab[M]) / min(abs(q["RA"]) for q in tab[M]) for M in MASSES}
    Mspread = {}
    for i, xg in enumerate(XGRID):
        v = [abs(tab[M][i]["RA"]) for M in MASSES]
        Mspread[xg] = max(v) / min(v)
    return S, Mspread


allres = {}
ok_bounds, ok_shape, ok_mass, ok_sign = True, True, True, True
for foot, a0 in A0_FOOT.items():
    m_use = m_inv_m
    if MUT == "a":                                              # planted: tune m so that |R_A|(M_ref = 1e11, x = 0.1) = 1
        Mr = 1e11 * MSUN
        m_use = math.sqrt(3.0 * a0 / (G_SI * Mr * math.sqrt(1 + 0.1 ** 2)))
    tab = point_mass_tables(a0, m_use)
    S, Msp = spreads(tab)
    allres[foot] = dict(tab=tab, S=S, Msp=Msp, m=m_use)
    R.P(f"\n  ---- point mass, footing {foot} (a0 = {a0:.4e}), m = {m_use:.4e} /m ----")
    R.P("   M_b      r_M[kpc] | R_A = rho_eff/rho_target at x = " + "  ".join(f"{x:g}" for x in XGRID))
    for M in MASSES:
        R.P(f"   {M:.0e}  {rM_m(M, a0) / KPC:8.3f} | " + "  ".join(f"{q['RA']:+.2e}" for q in tab[M]))
    R.P("   G1-S spread over x per mass: " + ", ".join(f"{M:.0e}: {S[M]:.4g}" for M in MASSES))
    R.P("   G1-M spread over M at fixed x: " + ", ".join(f"x={x:g}: {Msp[x]:.4g}" for x in XGRID))
    mx = max(abs(q["RA"]) for M in MASSES for q in tab[M]); mn = min(abs(q["RA"]) for M in MASSES for q in tab[M])
    R.P(f"   |R_A| range over the grid: [{mn:.3e}, {mx:.3e}]")
    allres[foot].update(mx=mx, mn=mn)

canon = allres["canonical"]
# ---- G1 gate lines (point mass, canonical footing carries the verdicts; the alt footing is reported and enters the claim bounds)
pm_A_pass = all(0.9 <= abs(q["RA"]) <= 1.1 for M in MASSES for q in canon["tab"][M])
pm_A_pass_any = any(0.9 <= abs(q["RA"]) <= 1.1 for M in MASSES for q in canon["tab"][M])
pm_S_pass = all(v <= 1.2 for v in canon["S"].values())
pm_M_pass = all(v <= 1.2 for v in canon["Msp"].values())
pm_sign_pass = all(q["rho_eff"] > 0 for M in MASSES for q in canon["tab"][M])
R.verdict("G1-A (point mass, canonical)", "PASS" if pm_A_pass else "FAIL", f"|R_A| in [{canon['mn']:.2e}, {canon['mx']:.2e}] against [0.90, 1.10]; any point within the band: {pm_A_pass_any}")
R.verdict("G1-S (point mass)", "PASS" if pm_S_pass else "FAIL", "spread over x = " + ", ".join(f"{canon['S'][M]:.4g}" for M in MASSES) + " against 1.20")
R.verdict("G1-M (point mass)", "PASS" if pm_M_pass else "FAIL", "spread over M at fixed x: " + ", ".join(f"{canon['Msp'][x]:.4g}" for x in XGRID) + " against 1.20")
R.verdict("G1-sign (point mass)", "PASS" if pm_sign_pass else "FAIL", "rho_eff " + ("> 0" if pm_sign_pass else "< 0 (NEGATIVE effective density, gravity weakened)") + " at every grid point")

# ---- pre-registered claims
allmx = max(allres[f]["mx"] for f in allres); allmn = min(allres[f]["mn"] for f in allres)
R.check("P1 (amplitude): |R_A| in [1e-17, 1e-7] at every grid point, both footings, and no point within 10% of 1",
        f"range [{allmn:.3e}, {allmx:.3e}]; any point in the 0.90-1.10 band: {pm_A_pass_any}", (allmn >= 1e-17 and allmx <= 1e-7 and not pm_A_pass_any))
ratio_form = [abs(q["RA"]) / (abs(canon["tab"][M][0]["RA"]) * math.sqrt(1 + q["x"] ** 2) / math.sqrt(1 + XGRID[0] ** 2)) for M in MASSES for q in canon["tab"][M]]
form_dev = max(abs(v - 1) for v in ratio_form)
R.check("P2a (shape): the G1-S spread exceeds 1.2 and |R_A| follows sqrt(1+x^2) to within 10%",
        f"spread {canon['S'][1e11]:.4g}; max deviation from sqrt(1+x^2) shape {form_dev:.2e}", canon["S"][1e11] > 1.2 and form_dev < 0.10)
R.check("P2b (the frozen text's number 'about 300 over x in [0.1, 30]'): the G1-S spread is 300 within a factor 1.5",
        f"spread {canon['S'][1e11]:.4g} = sqrt(1 + 30^2)/sqrt(1 + 0.1^2) = {math.sqrt(901) / math.sqrt(1.01):.4g}: the frozen 'about 300' was an arithmetic error by a factor 10",
        200 <= canon["S"][1e11] <= 450)
msp_all = [canon["Msp"][x] for x in XGRID]
R.check("P3 (mass scaling): the G1-M spread at fixed x is 1000 within 2% for the point-mass linear response",
        f"spreads {['%.5g' % v for v in msp_all]}", all(abs(v / 1000 - 1) < 0.02 for v in msp_all))
R.check("T0c-consistency: G1-sign equals the sign derived in A1 (negative density: rho_eff < 0 at every point)", f"all rho_eff > 0: {pm_sign_pass}", (not pm_sign_pass))

# ------------------------------------------------------------------------------------------------ G1-req (diagnostic)
R.banner("G1-req  the inverse length m_req needed for |R_A| = 1 at x = 0.1 (diagnostic)")
a0 = A0_FOOT["canonical"]
req = []
for M in MASSES:
    Mkg = M * MSUN
    mreq = math.sqrt(3.0 * a0 / (G_SI * Mkg * math.sqrt(1 + 0.1 ** 2)))
    req.append((M, mreq, mreq / (H0_SI / C_SI), 1 / mreq / KPC, rM_m(M, a0) / KPC))
    R.P(f"    M_b = {M:.0e}: m_req = {mreq:.3e} /m = {mreq / (H0_SI / C_SI):.3e} x (H0/c);  1/m_req = {1 / mreq / KPC:.3f} kpc = {1 / mreq / rM_m(M, a0):.4f} r_M ;  RR: 1/m = {1 / m_inv_m / KPC:.3e} kpc")
expo = np.polyfit(np.log10([q[0] for q in req]), np.log10([q[1] for q in req]), 1)[0]
R.P(f"    scaling exponent of m_req with M = {expo:.4f}  (hand estimate -1/2); 1/m_req / r_M = {[round(q[3] / q[4], 4) for q in req]}  (closed form (1+x^2)^(1/4)/sqrt(3) = {(1 + 0.1 ** 2) ** 0.25 / math.sqrt(3):.4f}; an earlier label typed 0.5738 by hand was a typo in a print string)")
R.check("G1-req: m_req scales as M^(-1/2) and 1/m_req = r_M * const (the required screening length is the mass-dependent r_M)", f"exponent {expo:.5f}", abs(expo + 0.5) < 1e-9, load_bearing=True)
rho_bg = 3 * H0_SI ** 2 * OL_CANON / (8 * math.pi * G_SI)
R.P(f"    background dark-energy density 3 H0^2 Omega_L/(8 pi G) = {rho_bg:.3e} kg/m^3 ; rho_target(r_M):")
for M in MASSES:
    rM = rM_m(M, a0)
    rt = a0 / (4 * math.pi * G_SI * rM * math.sqrt(2))
    R.P(f"       M_b = {M:.0e}: rho_target(r_M) = {rt:.3e} kg/m^3 ; rho_DE^bg/rho_target(r_M) = {rho_bg / rt:.3e}")
R.num("m_req_over_H0c", {f"{q[0]:.0e}": q[2] for q in req})
# embedding scan: background values of U and S today (bounded O(1) coefficients, exploratory, reported)
yb = sol.sol(0.0)
Ub, Sb = yb[0], yb[2]
Fbar = 1 - lam * Sb / 3
U0shift = (lam * H0_SI ** 2 * 0 + (mu * H0_SI) ** 2) * Ub / (24 * math.pi * G_SI)   # m^2 c^2 U0/(24 pi G) with (m c)^2 = lam H0^2
R.P(f"\n  embedding scan (exploratory, bounded, reported): background today U-bar = {Ub:.3f}, S-bar/H0^-2 = {Sb:.3f}: F-bar = 1 - m^2 S-bar/3 = {Fbar:.4f} (mu_eff = {1 / Fbar:.4f}: a factor O(1) on the linear response), "
    f"and a uniform density shift m^2 c^2 U-bar/(24 pi G) = {U0shift:.3e} kg/m^3 (vs rho_DE^bg = {rho_bg:.3e}).  Neither changes any verdict (the response is 7+ orders short).")
R.num("Fbar_today", Fbar); R.num("Ubar_today", Ub)

# ------------------------------------------------------------------------------------------------ extended baryons: CFG44's exponential sphere
R.banner("G1-X  CFG44's exponential sphere (h = 2 kpc, CFG44 B1's scale): C_eff(r) = rho_eff r^3 g_tot against (a0/4 pi) M_b(<r)")
from Bcommon import G as GK, exp_sphere, target_fields, KPC_M

mK = mu * (H0_KMS_MPC / 1e3) / (C_SI / 1e3) * sign_flip ** 0          # m in 1/kpc
sgnK = sign_flip
ext = {}
for foot, a0_si in A0_FOOT.items():
    a0K = a0_si * KPC_M / 1e6                                     # (km/s)^2/kpc
    mK_use = mK
    if MUT == "a":
        Mr = 1e11
        mK_use = math.sqrt(3.0 * a0K / (GK * Mr * math.sqrt(1 + 0.1 ** 2)))
    ext[foot] = {}
    for M in MASSES:
        prof = exp_sphere(M, H_EXP_KPC)
        rM = math.sqrt(GK * M / a0K)
        rr = np.array([xg * rM for xg in XGRID])
        s = rr / H_EXP_KPC
        uN = GK * M * gammainc(3.0, s)
        PsiN = -uN / rr - GK * M / (2 * H_EXP_KPC) * (1 + s) * np.exp(-s)
        rho_eff = sgnK * mK_use ** 2 * PsiN / (12 * math.pi * GK)
        # delta g = (m^2/3 r^2) int_0^r Psi_N r'^2 dr'
        rg = np.geomspace(1e-5, 2.0 * rr.max(), 60001)
        sg = rg / H_EXP_KPC
        Pg = -GK * M * gammainc(3.0, sg) / rg - GK * M / (2 * H_EXP_KPC) * (1 + sg) * np.exp(-sg)
        cum = np.concatenate([[0.0], np.cumsum(0.5 * (Pg[1:] * rg[1:] ** 2 + Pg[:-1] * rg[:-1] ** 2) * np.diff(rg))])
        dg = sgnK * mK_use ** 2 / (3 * rr ** 2) * np.interp(rr, rg, cum)
        gN = uN / rr ** 2
        Ceff = rho_eff * rr ** 3 * (gN + dg)
        Ct = a0K * uN / (4 * math.pi * GK)                       # (a0/4 pi) M_b(<r) with u_N = G M_b(<r)  ->  a0 u_N/(4 pi G)
        RX = Ceff / Ct
        # rho-target on the extended sphere (Bcommon.target_fields, the P2/'encl' closure)
        tf = target_fields(prof, a0=a0K)
        rho_t = np.exp(np.interp(np.log(rr), np.log(tf["r"]), np.log(tf["rho"])))
        RA = (rho_eff / rho_t) if MUT != "d" else np.ones_like(rr)
        if MUT == "d":
            RX = np.ones_like(rr)
        ext[foot][M] = dict(RX=RX, RA=RA, rho_eff=rho_eff, dg_over_gN=dg / gN)
    R.P(f"\n  ---- exponential sphere, footing {foot} ----")
    for M in MASSES:
        R.P(f"   {M:.0e}  R_X = C_eff/C_target: " + "  ".join(f"{v:+.2e}" for v in ext[foot][M]["RX"]))
    for M in MASSES:
        R.P(f"   {M:.0e}  R_A (rho_eff/rho_target^ext): " + "  ".join(f"{v:+.2e}" for v in ext[foot][M]["RA"]))
e = ext["canonical"]
X_A_pass = all(0.9 <= abs(v) <= 1.1 for M in MASSES for v in e[M]["RX"])
X_S = {M: max(abs(e[M]["RX"])) / min(abs(e[M]["RX"])) for M in MASSES}
X_M = {xg: max(abs(e[M]["RX"][i]) for M in MASSES) / min(abs(e[M]["RX"][i]) for M in MASSES) for i, xg in enumerate(XGRID)}
X_sign = all(v > 0 for M in MASSES for v in e[M]["rho_eff"])
R.verdict("G1-X (exponential sphere, canonical)", "PASS" if (X_A_pass and all(v <= 1.2 for v in X_S.values()) and all(v <= 1.2 for v in X_M.values())) else "FAIL",
          f"|R_X| in [{min(abs(e[M]['RX']).min() for M in MASSES):.2e}, {max(abs(e[M]['RX']).max() for M in MASSES):.2e}] vs [0.9, 1.1]; shape spreads {[f'{v:.3g}' for v in X_S.values()]}; mass spreads at fixed x {[f'{v:.3g}' for v in X_M.values()]}; rho_eff > 0: {X_sign}")
mxX = max(max(abs(ext[f][M]["RX"]).max() for M in MASSES) for f in ext); mnX = min(min(abs(ext[f][M]["RX"]).min() for M in MASSES) for f in ext)
R.check("P1-ext: the extended-sphere |R_X| also lies in [1e-17, 1e-7] (both footings) and none is within 10% of 1", f"range [{mnX:.3e}, {mxX:.3e}]", mnX >= 1e-17 and mxX <= 1e-7 and not X_A_pass)
R.num("R_X_canonical", {f"{M:.0e}": e[M]["RX"] for M in MASSES})

# ------------------------------------------------------------------------------------------------ DW
R.banner("G1 for generic analytic DW (from T0d): M_eff/M is one constant at every r and every M")
R.P("    Phi'(r) = g_N(r) * (Fbar - 8 f1)/(Fbar (Fbar - 6 f1)) for the point mass and (1 - 2 f1/(Fbar - 6 f1))/Fbar * g_N for extended baryons: a pure rescaling of G.")
R.P("    Relative to the MEASURED G the effective dark density is exactly 0 at every r > 0 (rho_eff = 0), so G1-A/S/M cannot be met: the target needs M_c(<r)/M = sqrt(1+x^2) - 1 from 0.005 (x = 0.1) to 29 (x = 30).")
R.P("    Cassini: |gamma - 1| = |4 f1/(Fbar - 8 f1)| <= 2.3e-5  =>  |f1| <~ 5.75e-6 Fbar, so any residual 'constant fraction' is <~ 1e-5.")
R.verdict("G1 (DW, generic analytic f, linear static)", "FAIL", "rho_eff = 0 relative to the measured G; a constant rescaling cannot supply M_c/M = sqrt(1+x^2)-1; shape, mass and amplitude lines all fail (not a numerical result: T0d exact)")
R.check("DW: the linear static response rescales G only (T0d exact residuals 0, so the K = 0)", "see A1", True, load_bearing=False)

# ------------------------------------------------------------------------------------------------ overall
G1_pass = pm_A_pass and pm_S_pass and pm_M_pass and pm_sign_pass
R.verdict("G1 (RR, linear static, point mass + exponential sphere)", "PASS" if G1_pass else "FAIL",
          f"A {'PASS' if pm_A_pass else 'FAIL'}, S {'PASS' if pm_S_pass else 'FAIL'}, M {'PASS' if pm_M_pass else 'FAIL'}, sign {'PASS' if pm_sign_pass else 'FAIL'}, X see above")
R.num("G1_RR_linear", "PASS" if G1_pass else "FAIL")
R.num("mu", mu); R.num("lam", lam)
sys.exit(finish(R, MUT))
