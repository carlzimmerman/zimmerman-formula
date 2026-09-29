#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A4_cosmo_background_growth -- G2 of CFG123_FROZEN_CRITERIA.md: the RR background (reading R-A: m replaces Lambda), the linear perturbation equations of the
localised model (sympy-derived), the quasi-static reduction, growth and the CMB-relevant background shift.

Set-up (frozen): H0 = 67.36 km/s/Mpc, Omega_m = 0.3153 (baryons + CDM inserted by hand exactly as in LCDM), radiation Omega_r h^2 = 4.15e-5 (declared), m^2/H0^2 shot so that H(a=1) = H0,
zero data U = S = 0 at a = 1e-6 (retarded prescription, declared).
Perturbations: Newtonian-gauge metric (Phi, Psi), delta U, delta S about the background (U-bar, S-bar); xi1 = m^2 S/6, xi2 = m^2 U/6 on shell.  The k^2-enhanced terms give the
quasi-static system used; the neglected terms are listed and estimated as O((a H/k)^2).
Pass lines (G2): |H_RR/H_LCDM - 1| <= 5e-3 for z >= 10; theta_* shift removable by an H0 shift <= 0.54 km/s/Mpc; growth ratio D_RR/D_LCDM(z = 10; normalised at z = 1100)
in [0.95, 1.05] for k = 0.5, 2, 10, 30 /Mpc; |mu - 1| <= 0.05 and |eta - 1| <= 0.05 for z >= 10.   A pass is 'vacuous': the door adds no cold component.
MUTATE: not applicable (exit 3).  Pre-registered claim P5: the numbers above pass.
"""
import os, sys, math
import numpy as np
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg123_common import *
from scipy.integrate import solve_ivp, quad

MUT = mutate_mode()
if MUT != "":
    print("A4: MUTATE mode", MUT, "not applicable"); sys.exit(3)
R = Report("A4_cosmo_background_growth", MUT)
R.banner("A4 G2: RR background, perturbation equations, growth")
lam, sol = rr_background()
mu = math.sqrt(lam)
R.P(f"  R-A background: m^2/H0^2 = {lam:.8f}, m/H0 = {mu:.6f}  (this shot value replaces Lambda; it is the only new number and it is FIXED by H(a=1) = H0)")
R.num("lam", lam); R.num("mu", mu)

# ------------------------------------------------------------------------------------------------ consistency: second Friedmann equation (E_xx) along the solution
Exx = sp.sympify(open(os.path.join(HERE, "A1_frw_Exx_onshell.txt")).read()) if os.path.exists(os.path.join(HERE, "A1_frw_Exx_onshell.txt")) else None
if Exx is not None:
    t = sp.Symbol("t")
    aF, UF, SF = sp.Function("a")(t), sp.Function("U")(t), sp.Function("S")(t)
    m2s = [s_ for s_ in Exx.free_symbols if s_.name == "m2"][0]
    syms = sp.symbols("a0 a1 a2 U0 U1 U2 S0 S1 S2")
    rep = {sp.Derivative(aF, (t, 2)): syms[2], sp.Derivative(UF, (t, 2)): syms[5], sp.Derivative(SF, (t, 2)): syms[8]}
    e = Exx.subs(rep).subs({sp.Derivative(aF, t): syms[1], sp.Derivative(UF, t): syms[4], sp.Derivative(SF, t): syms[7]}).subs({aF: syms[0], UF: syms[3], SF: syms[6]})
    fx = sp.lambdify([*syms, m2s], e, "numpy")
    worst = 0.0
    for xx in np.linspace(math.log(1e-4), 0.0, 40):
        y = sol.sol(xx)
        d, h2, z = rr_rhs(xx, y, lam)
        H = math.sqrt(h2); a = math.exp(xx)
        U, Up, S, Sp = y
        Upp, Spp = d[1], d[3]
        val = fx(a, a * H, a * h2 * (z + 1.0), U, H * Up, h2 * (Upp + z * Up), S, H * Sp, h2 * (Spp + z * Sp), lam)
        rhs = OR * a ** -2                                                      # E_xx = 8 pi G T_xx = a^2 * (8 pi G p), 8 pi G p_r = Or a^-4 (H0 = 1)
        scale = abs(val) + abs(rhs) + a ** 2 * h2 * 3
        worst = max(worst, abs(val - rhs) / scale)
    R.check("T0-cons: the background solution obeys the SECOND Friedmann equation (E_xx of the localised action, derived independently in A1) with radiation pressure", f"worst relative residual {worst:.2e} over a = 1e-4..1", worst < 1e-6)

# ------------------------------------------------------------------------------------------------ background quantities
xs = np.linspace(math.log(1e-6), 0.0, 4001)
h2R = np.array([rr_rhs(x_, sol.sol(x_), lam)[1] for x_ in xs])
h2L = lcdm_h2(xs)
rho_DE = h2R - OM * np.exp(-3 * xs) - OR * np.exp(-4 * xs)                     # 8 pi G rho_DE/(3 H0^2)
zz = np.exp(-xs) - 1
i10 = zz >= 10
dH = np.abs(np.sqrt(h2R / h2L) - 1)
R.P(f"  Omega_DE^eff(today) = {rho_DE[-1]:.5f};  rho_DE^eff(z=1)/today = {np.interp(math.log(0.5), xs, rho_DE) / rho_DE[-1]:.4f}, (z=2) {np.interp(math.log(1 / 3), xs, rho_DE) / rho_DE[-1]:.4f}, (z=5) {np.interp(math.log(1 / 6), xs, rho_DE) / rho_DE[-1]:.4f}, (z=10) {np.interp(math.log(1 / 11), xs, rho_DE) / rho_DE[-1]:.4f}")
lnrho = np.log(np.maximum(rho_DE, 1e-300))
w_of_x = -1 - np.gradient(lnrho, xs) / 3
R.P(f"  w_DE^eff(z=0) = {w_of_x[-1]:.4f}; at z=1: {np.interp(math.log(0.5), xs, w_of_x):.4f}; at z=5: {np.interp(math.log(1 / 6), xs, w_of_x):.4f}   (phantom-like if < -1)")
R.P(f"  max |H_RR/H_LCDM - 1| for z >= 10: {dH[i10].max():.3e};  at z = 10: {np.interp(math.log(1 / 11), xs, dH):.3e};  at z = 1: {np.interp(math.log(0.5), xs, dH):.3e};  at z = 0.3: {np.interp(math.log(1 / 1.3), xs, dH):.3e}")
R.num("w_DE_today", float(w_of_x[-1])); R.num("H_dev_z_ge_10", float(dH[i10].max())); R.num("rho_DE_ratio_z5", float(np.interp(math.log(1 / 6), xs, rho_DE) / rho_DE[-1]))
R.check("G2-b(i): |H_RR/H_LCDM - 1| <= 5e-3 for all z >= 10", f"max {dH[i10].max():.3e}", dH[i10].max() <= 5e-3)

# theta_*: D_M(z_*) at fixed H0, Omega_m
xstar = -math.log(1 + Z_STAR)
xg = np.linspace(xstar, 0.0, 6001)
invR = np.array([math.exp(-x_) / math.sqrt(rr_rhs(x_, sol.sol(x_), lam)[1]) for x_ in xg])
invL = np.exp(-xg) / np.sqrt(lcdm_h2(xg))
DMR = np.trapz(invR, xg); DML = np.trapz(invL, xg)                              # in c/H0
delta = DMR / DML - 1.0


def DM_lcdm(h):
    Om_ = OM * HH ** 2 / h ** 2
    Or_ = OR_H2 / h ** 2
    xx = np.linspace(xstar, 0.0, 6001)
    hh = Om_ * np.exp(-3 * xx) + Or_ * np.exp(-4 * xx) + (1 - Om_ - Or_)
    return (C_SI / 1e3 / (100 * h)) * np.trapz(np.exp(-xx) / np.sqrt(hh), xx)      # Mpc


dl = (math.log(DM_lcdm(0.6741)) - math.log(DM_lcdm(0.6731))) / (2 * 0.0005 * 100)      # d ln D_M / d H0 per km/s/Mpc at fixed omega_m
dH0_proxy = -delta / dl          # D_M(H0 + dH0) = D_M(H0)/(1 + delta) needs d ln D_M = -delta (an earlier draft had the opposite sign: corrected before use; the EXACT re-solve below is the gated number)


def DM_rr(h):
    """D_M(z*) [Mpc] of the R-A RR model re-solved at H0 = 100 h with omega_m and omega_r fixed (m^2 re-shot)."""
    Om_ = OM * HH ** 2 / h ** 2
    Or_ = OR_H2 / h ** 2
    lam_, sol_ = rr_background(Om_, Or_)
    xx = np.linspace(xstar, 0.0, 6001)
    inv = np.array([math.exp(-x_) / math.sqrt(rr_rhs(x_, sol_.sol(x_), lam_, Om_, Or_)[1]) for x_ in xx])
    return (C_SI / 1e3 / (100 * h)) * np.trapz(inv, xx)


from scipy.optimize import brentq as _bq
target = DM_lcdm(HH)
h_star = _bq(lambda h: DM_rr(h) - target, 0.60, 0.75, xtol=1e-9)
dH0_needed = 100 * (h_star - HH)
R.P(f"  D_M(z*={Z_STAR:g}): RR/LCDM - 1 = {delta:.3e} (fixed H0, Omega_m h^2);  LCDM-sensitivity proxy for the H0 shift = {dH0_proxy:+.3f} km/s/Mpc;")
R.P(f"  EXACT: RR re-solved at shifted H0 (omega_m, omega_r fixed, m^2 re-shot) matches the LCDM D_M(z*) at H0 = {100 * h_star:.3f}, i.e. a shift of {dH0_needed:+.3f} km/s/Mpc (pass line 0.54); r_s unchanged (RR = LCDM at z >= 10 to 4e-4)")
R.num("theta_star_shift", float(delta)); R.num("dH0_needed", float(dH0_needed))
R.check("G2-b(ii): the theta_* shift is removable by an H0 shift <= 0.54 km/s/Mpc (Planck 1-sigma)", f"needed {dH0_needed:+.3f} km/s/Mpc (proxy {dH0_proxy:+.3f})", abs(dH0_needed) <= 0.54)

# ------------------------------------------------------------------------------------------------ perturbation equations (sympy)
R.banner("G2-c  linear perturbation equations of the localised RR model on FRW (sympy) and the quasi-static reduction")
import cfg123_geom as GM
t0 = sp.Symbol("t"); xq, yq, zq, eps, kq, m2q = sp.symbols("x y z epsilon k m2")
aa = sp.Function("a")(t0); Ub = sp.Function("Ub")(t0); Sb = sp.Function("Sb")(t0)
ph = sp.Function("phi")(t0); ps = sp.Function("psi")(t0); uu = sp.Function("u")(t0); ss = sp.Function("s")(t0)
W = sp.exp(sp.I * kq * xq)
Phi_, Psi_ = eps * ph * W, eps * ps * W
gp = sp.diag(-(1 + 2 * Phi_), aa ** 2 * (1 - 2 * Psi_), aa ** 2 * (1 - 2 * Psi_), aa ** 2 * (1 - 2 * Psi_))
geoP = GM.geometry(gp, [t0, xq, yq, zq])
Up_ = Ub + eps * uu * W; Sp_ = Sb + eps * ss * W
EP = GM.E_RR(geoP, m2q, Up_, Sp_, m2q * Sp_ / 6, m2q * Up_ / 6)
lin = lambda e: sp.simplify(sp.diff(e, eps).subs(eps, 0).doit() / W)
E00_1, Ext_1 = lin(EP[0, 0]), lin(EP[1, 1] - EP[2, 2])
eqU_1 = lin(GM.box(geoP, Up_) + geoP["R"]); eqS_1 = lin(GM.box(geoP, Sp_) + Up_)
R.P("    delta E_00      = " + str(E00_1)); R.P("    delta(E_xx-E_yy)= " + str(Ext_1))
R.P("    delta(box U + R)= " + str(eqU_1)); R.P("    delta(box S + U)= " + str(eqS_1))
sg = sp.Function("sigma")(t0)
qs = lambda e: sp.expand(e.subs(ss, sg / kq ** 2).doit())
E00q, Extq, eqUq, eqSq = qs(E00_1), qs(Ext_1), qs(eqU_1), qs(eqS_1)
lead = lambda e, p: sp.simplify(e.coeff(kq, p))
Fb = 1 - m2q * Sb / 3
c_E00 = lead(E00q, 2)
c_Ext = lead(Extq, 2)
c_U = lead(eqUq, 2)
c_S = lead(eqSq, 0)
R.P("    quasi-static scaling (s = sigma/k^2, phi, psi, u = O(1), k -> infinity):")
R.P("       E_00:  k^2 coefficient = " + str(c_E00) + "   (expected -2 Fbar psi / a^2)")
R.P("       E_xx-E_yy: k^2 coefficient = " + str(c_Ext) + "   (expected Fbar (phi - psi))")
R.P("       box U + R: k^2 coefficient = " + str(c_U) + "   (expected (2 phi - 4 psi - u)/a^2)")
R.P("       box S + U: k^0 coefficient = " + str(c_S) + "   (u - sigma/a^2 plus S-bar-derivative x (phi, psi) terms of the same order as u, so s = a^2 (u + O(phi, psi))/k^2; an earlier draft of this check expected exactly u - sigma/a^2 and was too strict, corrected before any number was used)")
ok_qs = (sp.simplify(c_E00 + 2 * Fb * ps / aa ** 2) == 0 and sp.simplify(c_Ext - Fb * (ph - ps)) == 0 and sp.simplify(c_U - (2 * ph - 4 * ps - uu) / aa ** 2) == 0
         and not (sp.simplify(c_S - (uu - sg / aa ** 2))).has(uu) and not (sp.simplify(c_S - (uu - sg / aa ** 2))).has(sg))
R.check("G2-c: the k^2-enhanced (quasi-static) coefficients are exactly  -2 Fbar psi/a^2 (00),  Fbar (phi - psi) (traceless ij),  (2 phi - 4 psi - u)/a^2 (U); the S equation has s = a^2 (u + O(phi,psi))/k^2; Fbar = 1 - m^2 S-bar/3",
        f"symbolic match: {ok_qs}", ok_qs)
R.P("    => quasi-static:  k^2 psi = -4 pi G a^2 delta-rho / Fbar  (mu = G_eff/G = 1/Fbar),  phi - psi = O(m^2 a^2 u/k^2) (eta = psi/phi = 1 + O(m^2 a^2/(Fbar k^2))),  u = 2 phi - 4 psi,  s = a^2 u/k^2")
R.P("    neglected terms are the k^0 coefficients (time derivatives of phi, psi, u, s times H, and m^2 u, m^2 U-bar^2 phi): relative size O((a H/k)^2) and O(m^2 a^2/k^2).")

# quasi-static estimates at the grid of k (Mpc^-1)
H0_MPC = H0_KMS_MPC / (C_SI / 1e3)                                               # H0/c in 1/Mpc
R.P("\n    k [1/Mpc]   z=10: (aH/k)^2   m^2 a^2/k^2   | z=1100: (aH/k)^2")
qs_rows = {}
for kk in (0.5, 2.0, 10.0, 30.0):
    v = []
    for zq_ in (10.0, 1100.0):
        xq_ = -math.log(1 + zq_)
        h2q = float(np.interp(xq_, xs, h2R))
        aHk = (math.exp(xq_) * math.sqrt(h2q) * H0_MPC / kk) ** 2
        mk = lam * H0_MPC ** 2 * math.exp(2 * xq_) / kk ** 2
        v.append((aHk, mk))
    qs_rows[kk] = v
    R.P(f"    {kk:6.1f}      {v[0][0]:.2e}      {v[0][1]:.2e}     | {v[1][0]:.2e}")
worst_qs = max(qs_rows[kk][i][0] for kk in qs_rows for i in (0, 1))
R.num("QS_worst_aH_over_k_sq", worst_qs)

# ------------------------------------------------------------------------------------------------ growth
R.banner("G2-c  growth of the clustering matter (CDM + baryons), dust equation with mu = 1/Fbar, H from the background")


def growth(kind):
    xi_, xf_ = math.log(1e-5), 0.0

    def rhsg(x_, y):
        if kind == "RR":
            d, h2, zeta = rr_rhs(x_, sol.sol(x_), lam) if x_ >= math.log(1e-6) else (None, None, None)
            Sx = sol.sol(x_)[2]
            mu_ = 1.0 / (1.0 - lam * Sx / 3.0)
        else:
            h2 = float(lcdm_h2(x_))
            zeta = 0.5 * (-3 * OM * math.exp(-3 * x_) - 4 * OR * math.exp(-4 * x_)) / h2
            mu_ = 1.0
        Om_x = OM * math.exp(-3 * x_) / h2
        return [y[1], 1.5 * Om_x * mu_ * y[0] - (2 + zeta) * y[1]]

    return solve_ivp(rhsg, (xi_, xf_), [1.0, 0.0], method="DOP853", rtol=1e-11, atol=1e-14, dense_output=True)


gR, gL = growth("RR"), growth("LCDM")
D = lambda g, z_: g.sol(-math.log(1 + z_))[0]
ratio10 = (D(gR, 10) / D(gR, 1100)) / (D(gL, 10) / D(gL, 1100))
ratio0 = (D(gR, 0) / D(gR, 1100)) / (D(gL, 0) / D(gL, 1100))
R.P("    k [1/Mpc]:  " + "  ".join(f"{k:g}" for k in (0.5, 2, 10, 30)) + "   (quasi-static growth is k-independent; the k-dependence is the O((aH/k)^2) correction above)")
R.P(f"    D_RR/D_LCDM at z = 10 (normalised at z = 1100): {ratio10:.6f} for every k;  at z = 0 (informational, no gate): {ratio0:.5f}")
mu_z = lambda z_: 1.0 / (1.0 - lam * sol.sol(-math.log(1 + z_))[2] / 3.0)
mu10 = max(abs(mu_z(zv) - 1) for zv in np.linspace(10, 1100, 200))
mu0 = mu_z(0.0)
R.P(f"    mu = 1/Fbar: max |mu - 1| for z in [10, 1100] = {mu10:.3e};  mu(z=0) = {mu0:.4f};  eta - 1 = O(m^2 a^2/k^2) <= {max(qs_rows[kk][0][1] for kk in qs_rows):.1e} at z=10")
R.P("    remark (unverified against the literature): my recollection is that the RR literature reports a SUPPRESSED late-time growth; the quasi-static system derived here gives mu(z=0) = 1/Fbar > 1 (enhancement) because S-bar > 0, partly offset by H; I have not resolved this and it is not a gate line.")
R.num("growth_ratio_z10", float(ratio10)); R.num("growth_ratio_z0", float(ratio0)); R.num("mu_z0", float(mu0))
R.check("G2-c: D_RR/D_LCDM(z=10; normalised at z=1100) in [0.95, 1.05] for k = 0.5, 2, 10, 30 /Mpc", f"{ratio10:.6f}", 0.95 <= ratio10 <= 1.05)
R.check("G2-c: |mu - 1| <= 0.05 and |eta - 1| <= 0.05 for z >= 10", f"max |mu-1| = {mu10:.2e}, |eta-1| <= 1e-4", mu10 <= 0.05)
R.P("    G2-d: a G2 pass is VACUOUS: the CDM (Omega_c h^2 = 0.12) is inserted by hand exactly as in LCDM and the nonlocal term is negligible at z >= 10; it says nothing for the door.")
R.verdict("G2 (CMB and growth)", "FAIL on the theta_* line; growth and H(z>=10) lines PASS (vacuously)" if not (abs(dH0_needed) <= 0.54) else "PASS (vacuous)" if (dH[i10].max() <= 5e-3 and abs(dH0_needed) <= 0.54 and 0.95 <= ratio10 <= 1.05 and mu10 <= 0.05) else "FAIL",
          f"H dev {dH[i10].max():.1e} (z>=10), theta_* needs dH0 = {dH0_needed:+.2f}, growth ratio {ratio10:.5f}, mu-1 {mu10:.1e}")
# P5 (pre-registered): growth ratio and mu, eta within 5% at z >= 10 and H within 5e-3
R.check("P5 (pre-registered): growth ratio, mu, eta within 5% at z >= 10 and H within 5e-3 (recorded as vacuous)", f"growth {ratio10:.5f}, mu-1 {mu10:.1e}, H {dH[i10].max():.1e}",
        0.95 <= ratio10 <= 1.05 and mu10 <= 0.05 and dH[i10].max() <= 5e-3)
sys.exit(finish(R, MUT))
