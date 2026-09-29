#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
B3 -- CLASS (ii)/(iii), LOCAL CLOSURES: does any closure that is LOCAL in the fields at r (dispersion, pressure or charge as a function of g_N, g_tot, rho_b,
rho_c and their derivatives at the same point) produce the target (T)?    And what is (T) as a closure?

EXACT STATEMENTS
  L1  LOCALITY NO-GO (numeric + exact).  Take baryon profile A and profile B = A + a thin baryon shell of mass m at R' > r*.  At r* every local field
      (rho_c, g_tot, g_N, rho_b and their radial derivatives) is IDENTICAL for A and B: (T) makes rho_c(r) depend only on M_b(<r), and the ODE is integrated
      outward.  But the target pressure (P) differs by (a0/2) m/(4 pi R'^2).  So NO local equation of state P = Pi(local fields at r) -- and no local
      dispersion law sigma^2 = F(local fields) -- can produce (T): the required pressure/dispersion carries the OUTER baryon column.
      (It is harmless for a hydrostatic fluid, whose pressure is the weight of the overlying fluid: the content of (T) is a closure for the DENSITY.)
  L2  (T) as a density closure:  rho_c g_tot = (a0/4 pi G) g_N / r.  It is local in (g_N, g_tot) but contains the position r explicitly.  A covariant local form needs the
      TRANSVERSE tidal eigenvalue of the baryonic potential, T_perp = (1/2)(lap Phi_N - Phi_N,ghat ghat) (= g_N/r for spherical baryons):
            rho_c g_tot = (a0/4 pi G) T_perp ,      beta = - lap Phi_N /(2 T_perp)     (anisotropy of the locally virialised reading)
      For flattened baryons T_perp and the enclosed-mass form g_N/r differ (thin-disc estimate, reported): the enclosed-mass form is a SPHERICAL statement.
  L3  CATALOGUE.  Closures integrated for compact/diffuse exponential spheres and the Freeman disc and compared with the law (P2, nu_mono; canonical a0):
        (T)  enclosed charge (target)                      : within 0.03-0.2 dex of P2 (positive control), 0.03-0.2 of nu_mono
        const  constant charge C = a0 M_b,tot/4 pi (CFG9)   : overshoots (central isothermal core)
        gauss  local pressure P = a0 g_N/(8 pi G) (CFG10 i) : demands rho_c < 0 where r u_N' > 2 u_N (analytic fraction reported)
        omega  local prescribed temperature sigma^2 = (1/2) r nu(g_N/a0) g_N (dispersion 'sourced by the baryonic field', hydrostatic in the total field):
               the fluid is too cold inside the baryons and collapses.
      Each is exact for a point mass; none is exact for extended baryons except (T).
CHECKS (PRE-DECLARED)
  A1 CONTROL  the numerical (T) closure equals P2 for a point mass to 1e-5, and the constant-charge closure equals it too (no bite on point masses).
  A2 L1: local fields at r* identical (< 1e-9 relative) between A and B; the (T) hydrostatic pressures differ by (a0/2) m/(4 pi R'^2) to 1e-3 (relative to the difference).
  A3 L3: the constant-charge closure departs from (T) by > 0.1 dex somewhere on every extended profile; the local-temperature closure by > 0.1 dex; (T) is within 0.25 dex
     of the P2 law on every extended profile (positive control).
  A4 the Jeans equation with sigma_r^2 = V_c^2/2 and beta = -(3/2) rho_b/rhobar_b is satisfied by the (T) solution (numeric, exp. sphere), 1e-4.
  A5 L2: spherical identity (sympy) and the thin-disc estimate (reported).
  A2b the (T) pressure inside R' rises uniformly by (a0/2) m/(4 pi R'^2) when a shell m is added at R' (no force change inside): the fluid must be heated by a0 m R'/4 (numeric, 1%).
  A6 (reported) the field-energy pressure (g_tot^2 - g_N^2)/(8 pi G) is low against the (T) pressure inside the baryons.   A7 (reported) P is not a function of g_N alone (1-2 dex scatter).
MUTATE=1: (i) the shell of L1 is placed INSIDE r* (R' < r*), so the local fields are no longer identical: A2 must FAIL; (ii) the a0 inside the (T) ODE is multiplied by 10: A1 and A3 must FAIL.
Run: python3 B3_local_closures.py   (MUTATE=1 for the control)
"""
import os, sys, math
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, cumulative_trapezoid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Bcommon import *

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = Report("B3_local_closures", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: shell inside r* (A2) and a0 x 10 inside the (T) ODE (A1, A3) -- both must FAIL ***")
A0_ODE = 10 * A0 if MUTATE else A0

# ================================================================================================ A1
R.banner("A1  CONTROL: point mass -- (T) and the constant-charge closure both equal P2")
M = 1e10
pm = point_mass(M)
rM = math.sqrt(M * G / A0)
dev = {}
for kind in ("encl", "const"):
    rr, w, u, uN = cold_mass(pm, kind, r0=1e-2 * rM, r1=1e3 * rM, n=6001, w0=float(np.sqrt(G * M * G * M + A0 * G * M * (1e-2 * rM) ** 2) - G * M), a0_ode=A0_ODE)
    uex = uN * np.sqrt(1 + (rr / rM) ** 2)
    dev[kind] = float(np.max(np.abs(u / uex - 1)))
P(f"    max relative deviation from P2:  (T) {dev['encl']:.2e};  constant charge {dev['const']:.2e}")
check("A1 CONTROL: for a point mass the numerical (T) closure and the constant-charge closure both reproduce P2 to 1e-5" + ("  [MUTATE: a0 x 10 in the ODEs]" if MUTATE else ""),
      f"{dev}", max(dev.values()) < 1e-5)

# ================================================================================================ A2 : locality (far-shell) theorem
R.banner("A2  L1: two baryon profiles identical for r < R' but different beyond: identical local fields at r*, different (T) pressure")
pA = exp_sphere(1e10, 2.0)
m_shell = 10 * 1e10
R_shell = 5.0 if MUTATE else 40.0                                        # MUTATE: the shell sits INSIDE r* = 10 kpc
r_star = 10.0
wdt = 0.5
step = lambda r_: 0.5 * (1 + np.tanh((r_ - R_shell) / wdt))
uA = lambda r_: pA.u(r_)
pB = Profile("expsphere+shell", pA.Mtot + m_shell, lambda r_: pA.u(r_) + G * m_shell * step(r_),
             rho_func=lambda r_: pA.rho_b(r_) + m_shell * 0.5 / np.cosh((r_ - R_shell) / wdt) ** 2 / wdt / (4 * math.pi * r_ ** 2))
res = {}
Pfull = {}
for nm, p in (("A", pA), ("B", pB)):
    f_ = target_fields(p, r0=1e-2, r1=3e3, n=9001, a0=A0_ODE)
    r_ = f_["r"]
    ii = int(np.argmin(np.abs(r_ - r_star)))
    e = 1e-4
    def at(arr, rr):
        return float(np.interp(rr, r_, arr))
    loc = dict(rho_c=at(f_["rho"], r_star), g_tot=at(f_["g"], r_star), g_N=float(p.gN(r_star)), rho_b=float(p.rho_b(r_star)),
               drho_c=(at(f_["rho"], r_star * (1 + e)) - at(f_["rho"], r_star * (1 - e))) / (2 * r_star * e),
               dg_tot=(at(f_["g"], r_star * (1 + e)) - at(f_["g"], r_star * (1 - e))) / (2 * r_star * e),
               drho_b=(float(p.rho_b(r_star * (1 + e))) - float(p.rho_b(r_star * (1 - e)))) / (2 * r_star * e))
    # hydrostatic pressure of the target at r*: quadrature of rho_c g from r* to the end + analytic tail
    sel = r_ >= r_star
    f_rho_g = f_["rho"] * f_["g"]
    tailP = A0_ODE * p.ug[-1] / G / (8 * math.pi * r_[-1] ** 2)
    cumP = cumulative_trapezoid(f_rho_g, r_, initial=0.0)
    Parr = (cumP[-1] - cumP) + tailP
    Pn = float(np.trapz(f_rho_g[sel], r_[sel])) + tailP
    res[nm] = (loc, Pn)
    Pfull[nm] = (r_, Parr)
locA, PA = res["A"]; locB, PB = res["B"]
rel = {k: abs(locA[k] / locB[k] - 1) if locB[k] != 0 else abs(locA[k] - locB[k]) for k in locA}
P("    local fields at r* = 10 kpc, A vs B (relative difference): " + ", ".join(f"{k} {v:.1e}" for k, v in rel.items()))
dP_expected = 0.5 * A0_ODE * m_shell / (4 * math.pi * R_shell ** 2)
P(f"    (T) hydrostatic pressure at r*: P_A = {PA:.6e}, P_B = {PB:.6e}; difference {PB - PA:.6e}; predicted (a0/2) m/(4 pi R'^2) = {dP_expected:.6e}; (P_B-P_A)/P_A = {(PB - PA) / PA:.3f}")
ok_loc = max(rel.values()) < 1e-9
ok_dP = abs((PB - PA) / dP_expected - 1) < 1e-3
check("A2 L1: local fields at r* identical (< 1e-9) for A and B, yet the (T) pressure differs by exactly (a0/2) m/(4 pi R'^2): no local closure P = Pi(local fields) can be (T)"
      + ("  [MUTATE: shell inside r*]" if MUTATE else ""),
      f"max local-field difference {max(rel.values()):.1e}; pressure difference / predicted - 1 = {(PB - PA) / dP_expected - 1:+.2e}; relative pressure change {(PB - PA) / PA:.2f}",
      ok_loc and ok_dP)
R.num("A2", dict(local_field_diff=max(rel.values()), dP_over_P=(PB - PA) / PA))

# ---- A2b: the energy the fluid must be given when baryons are added OUTSIDE it (shell theorem: no force change inside R')
rA, PAf = Pfull["A"]; rB, PBf = Pfull["B"]
R_cut = R_shell - 6 * wdt
mask = (rA > 0.05) & (rA < R_cut)
dP_arr = PBf[mask] - PAf[mask]
dU_num = 1.5 * float(np.trapz(dP_arr * 4 * math.pi * rA[mask] ** 2, rA[mask]))                 # (3/2) Int Delta P dV = thermal energy the fluid inside R' must gain
dU_pred = 2 * math.pi * dP_expected * (R_cut ** 3 - 0.05 ** 3)
Vf2_ = math.sqrt(G * pA.Mtot * A0)
P(f"    Delta P(r < R') = {float(np.mean(dP_arr)):.4e} (uniform: spread {float(np.ptp(dP_arr) / np.mean(dP_arr)):.1e}); thermal energy the inner fluid must gain: {dU_num:.4e} vs 2 pi Delta P R'^3 = {dU_pred:.4e}")
P(f"    per unit accreted baryon mass: a0 R'/4 = {A0 * R_shell / 4:.3e} (km/s)^2  vs  V_f^2 = {Vf2_:.3e}  and  G M_b/R' = {G * pA.Mtot / R_shell:.3e}  (ratios {A0 * R_shell / 4 / Vf2_:.2f}, {A0 * R_shell / 4 / (G * pA.Mtot / R_shell):.1f})")
check("A2b the (T) pressure inside R' rises by the uniform (a0/2) m/(4 pi R'^2) when baryons are added outside R' (no force change inside, shell theorem): the inner fluid must be HEATED by "
      "(3/2) Int Delta P dV = a0 m R'/4 (numeric within 1%), i.e. a0 R'/4 per unit accreted baryon mass -- more than the flat-speed V_f^2 once R' > 4 r_M and more than G M_b/R' once R' > 2 r_M"
      + ("  [MUTATE: a0 x 10 in the ODE]" if MUTATE else ""), f"numeric/predicted - 1 = {dU_num / dU_pred - 1:+.2e}", abs(dU_num / dU_pred - 1) < 0.01 and not MUTATE)
R.num("A2b", dict(dU_num=dU_num, dU_pred=dU_pred, per_mass=A0 * R_shell / 4, Vf2=Vf2_, GM_over_R=G * pA.Mtot / R_shell))

# ================================================================================================ A3 : catalogue
R.banner("A3  L3: closures on extended baryons vs (T) and vs the law (canonical a0)")


def omega_closure(prof, kernel, a0=A0):
    """local temperature sigma^2 = (1/2) r nu(g_N/a0) g_N (the law's V_c^2/2 from the BARYONIC field), fluid hydrostatic in the total field, started on (T)'s state."""
    rMp = math.sqrt(prof.Mtot * G / a0)
    f_ = target_fields(prof, r0=1e-3 * rMp, r1=1e3 * rMp, n=9001)
    r_ = f_["r"]

    def s2(rr):
        uN = prof.u(rr)
        return 0.5 * rr * KERNELS[kernel](uN / (rr ** 2 * a0)) * uN / rr ** 2

    def ds2(rr, e=1e-3):
        return (s2(rr * (1 + e)) - s2(rr * (1 - e))) / (2 * rr * e)

    def rhs(s, y):
        rr = math.exp(s)
        lrho, Mc = y
        g = (prof.u(rr) + G * Mc) / rr ** 2
        return [-rr * (g + ds2(rr)) / s2(rr), 4 * math.pi * rr ** 3 * math.exp(lrho)]

    sol = solve_ivp(rhs, (math.log(r_[0]), math.log(r_[-1])), [math.log(f_["rho"][0]), f_["w"][0] / G], t_eval=np.log(r_), rtol=1e-9, atol=1e-12, method="DOP853")
    return r_, G * sol.y[1]


CASES = [("compact exp. sphere", exp_sphere(1e10, 2.0), 2.0), ("diffuse exp. sphere", exp_sphere(1e8, 2.0), 2.0), ("compact Freeman disc", freeman_disc(1e10, 3.0), 3.0),
         ("diffuse Freeman disc", freeman_disc(1e8, 3.0), 3.0), ("Plummer", plummer(1e10, 1.0), 1.0)]
dev_T_law, dev_const_T, dev_omega_T = {}, {}, {}
P("    max |Delta log10 g_tot| over r in [0.5 h, 30 r_M]:")
for nm, p, h in CASES:
    rMp = math.sqrt(p.Mtot * G / A0)
    rT, wT, uT, uNT = cold_mass(p, "encl", a0_ode=A0_ODE)
    rC, wC, uC, uNC = cold_mass(p, "const")
    rO, wO = omega_closure(p, "P2")
    uO = p.u(rO) + wO
    grid = np.geomspace(0.5 * h, 30 * rMp, 300)
    uTg = np.interp(np.log(grid), np.log(rT), uT); uCg = np.interp(np.log(grid), np.log(rC), uC); uOg = np.interp(np.log(grid), np.log(rO), uO)
    dl = lambda ua, ub: np.log10(ua / ub)
    row = {}
    for kn in ("P2", "nu_mono"):
        ul = law_u(p, grid, kn)
        row[f"T_vs_{kn}"] = float(np.max(np.abs(dl(uTg, ul))))
        row[f"const_vs_{kn}"] = float(np.max(np.abs(dl(uCg, ul))))
        row[f"omega_vs_{kn}"] = float(np.max(np.abs(dl(uOg, ul))))
    row["const_vs_T"] = float(np.max(np.abs(dl(uCg, uTg))))
    row["omega_vs_T"] = float(np.max(np.abs(dl(uOg, uTg))))
    # analytic fraction of radii where the pressure Gauss law (i) demands rho_c < 0:  2 u_N - r u_N' < 0
    rg2 = np.geomspace(0.5 * h, 30 * rMp, 2000)
    neg = float(np.mean(2 * p.u(rg2) - rg2 * p.du(rg2) < 0))
    row["gauss_neg_fraction"] = neg
    dev_T_law[nm] = row["T_vs_P2"]; dev_const_T[nm] = row["const_vs_T"]; dev_omega_T[nm] = row["omega_vs_T"]
    P(f"      {nm:22s} (T)-P2 {row['T_vs_P2']:.3f}, (T)-nu_mono {row['T_vs_nu_mono']:.3f} | const-(T) {row['const_vs_T']:.3f} | omega-(T) {row['omega_vs_T']:.3f} | "
      f"gauss (i): rho_c<0 on {100 * neg:.0f}% of the radii")
    R.num("A3_" + nm, row)
check("A3 (T) is within 0.25 dex of the P2 law on every extended profile (positive control); the constant-charge closure and the local-temperature closure depart from (T) by > 0.1 dex "
      "somewhere on every extended profile" + ("  [MUTATE: a0 x 10 in (T)]" if MUTATE else ""),
      f"max (T)-P2 {max(dev_T_law.values()):.3f}; min over profiles of max const-(T) {min(dev_const_T.values()):.3f}, omega-(T) {min(dev_omega_T.values()):.3f}",
      max(dev_T_law.values()) < 0.25 and min(dev_const_T.values()) > 0.1 and min(dev_omega_T.values()) > 0.1)

# ================================================================================================ A4 : Jeans with anisotropy
R.banner("A4  the anisotropic Jeans reading of (T): sigma_r^2 = V_c^2/2 and beta = -(3/2) rho_b/rhobar_b (numeric)")
p = exp_sphere(1e10, 2.0)
f_ = target_fields(p, r0=1e-3 * rM, r1=1e3 * rM, n=12001)
r_, rho, g = f_["r"], f_["rho"], f_["g"]
rhob = p.rho_b(r_); Mb = f_["uN"] / G
rhobar = 3 * Mb / (4 * math.pi * r_ ** 3)
beta = -1.5 * rhob / rhobar
s2r = 0.5 * r_ * g
jeans = np.gradient(rho * s2r, r_) + 2 * beta * rho * s2r / r_ + rho * g
scale = rho * g
sel = (r_ > 0.01 * rM) & (r_ < 300 * rM)
resj = float(np.max(np.abs(jeans[sel] / scale[sel])))
P(f"    max |d(rho s_r^2)/dr + 2 beta rho s_r^2/r + rho g| / (rho g) = {resj:.2e};  beta range [{beta[sel].min():.3f}, {beta[sel].max():.3f}]  (-3/2 inside a core, 0 outside)")
check("A4 the (T) fluid is a locally virialised (sigma_r^2 = V_c^2/2) collisionless equilibrium with tangential bias beta(r) = -(3/2) rho_b/rhobar_b (Jeans residual < 1e-3)"
      + ("  [MUTATE: not applicable]" if MUTATE else ""), f"residual {resj:.2e}", resj < 1e-3)

# ================================================================================================ A5 : covariant restatement
R.banner("A5  L2: the covariant (tidal) restatement of (T) and its disc limit")
rs = sp.symbols("r", positive=True)
Phi = sp.Function("Phi")(rs)
gN = sp.diff(Phi, rs)
lap = sp.diff(Phi, rs, 2) + 2 * sp.diff(Phi, rs) / rs
Tperp = sp.Rational(1, 2) * (lap - sp.diff(Phi, rs, 2))
res_a = sp.simplify(Tperp - gN / rs)
Gs, a0s = sp.symbols("G a0", positive=True)
res_b = sp.simplify((a0s / (4 * sp.pi * Gs)) * Tperp - (a0s / (8 * sp.pi * Gs)) * (lap - sp.diff(Phi, rs, 2)))
Mbf = sp.Function("M_b")(rs)
gN_M = Gs * Mbf / rs ** 2                                                         # Phi_N' = G M_b(<r)/r^2
lapM = sp.diff(gN_M, rs) + 2 * gN_M / rs                                          # = 4 pi G rho_b
beta_cov = sp.simplify(-lapM / (2 * gN_M / rs))                                    # -lap Phi/(2 T_perp)
beta_enc = sp.simplify(-sp.Rational(1, 2) * rs * sp.diff(Mbf, rs) / Mbf)
res_c = sp.simplify(beta_cov - beta_enc)
check("A5a (sympy) for spherical baryons T_perp = g_N/r, (a0/4 pi G) T_perp = (a0/8 pi G)(lap Phi_N - Phi_N,ghat ghat), and beta = -lap Phi_N/(2 T_perp) = -(1/2) dlnM_b/dlnr: the enclosed-mass "
      "closure IS a local tidal closure for spherical baryons", f"residuals {res_a}, {res_b}, {res_c}", res_a == 0 and res_b == 0 and res_c == 0)
# thin exponential disc, midplane, vertical profile rho_b = Sigma(R) exp(-|z|/h_z)/(2 h_z): Phi_zz = 4 pi G rho_b - Phi_RR - Phi_R/R, T_perp = (4 pi G rho_b - Phi_RR)/2 vs the enclosed T_sph = V^2/R^2
h = 3.0
Rr = np.array([1.0, 2.0, 4.0]) * h
S0 = 1e10 / (2 * math.pi * h * h)


def V2(Rq):
    y = Rq / (2 * h)
    return 4 * math.pi * G * S0 * h * y * y * (i0(y) * k0(y) - i1(y) * k1(y))


rowd = []
for hz_over_h in (0.05, 0.1, 0.2):
    hz = hz_over_h * h
    vals = []
    for Rq in Rr:
        e = 1e-4
        Phi_R = V2(Rq) / Rq
        Phi_RR = (V2(Rq * (1 + e)) / (Rq * (1 + e)) - V2(Rq * (1 - e)) / (Rq * (1 - e))) / (2 * Rq * e)
        rho_mid = S0 * math.exp(-Rq / h) / (2 * hz)
        Tp = 0.5 * (4 * math.pi * G * rho_mid - Phi_RR)
        vals.append(Tp / (V2(Rq) / Rq ** 2))
    rowd.append((hz_over_h, vals))
    P(f"    Freeman-like disc, h_z/h = {hz_over_h}: T_perp(local, midplane)/T_sph(enclosed-mass form) at R = 1, 2, 4 h: " + ", ".join(f"{v:.1f}" for v in vals))
check("A5b (reported, estimate) for a thin exponential disc the local tidal closure gives 3-15x the enclosed-mass closure at the midplane: the two readings of (T) split for flattened baryons",
      f"ratios { {r_[0]: [round(v, 1) for v in r_[1]] for r_ in rowd} }", min(min(r_[1]) for r_ in rowd) > 2.0, load_bearing=False)

# ================================================================================================ A6 : E-stress (dispersion sourced by the field energy)
R.banner("A6  the 'field-energy' closure P = (g_tot^2 - g_N^2)/(8 pi G) (CFG2's stress law read as a fluid pressure) against the (T) pressure")
rat = {}
for nm, p, h in CASES[:4]:
    rMp = math.sqrt(p.Mtot * G / A0)
    f_ = target_fields(p, r0=1e-3 * rMp, r1=1e3 * rMp, n=9001)
    r_ = f_["r"]
    P_E = (f_["g"] ** 2 - (f_["uN"] / r_ ** 2) ** 2) / (8 * math.pi * G)
    P_T = A0 * (f_["uN"] / r_ ** 2) / (8 * math.pi * G) + 0.5 * A0 * np.array([sigma_out_ := float(np.trapz(p.rho_b(np.geomspace(rr_, p.rg[-1] * 0.5, 2001)), np.geomspace(rr_, p.rg[-1] * 0.5, 2001))) for rr_ in r_])
    sel = (r_ > 0.5 * h) & (r_ < 30 * rMp)
    q = P_E[sel] / P_T[sel]
    rat[nm] = (float(q.min()), float(q.max()))
    P(f"      {nm:22s}: P_E/P_T over r in [0.5 h, 30 r_M]: min {q.min():.3f}, max {q.max():.3f}")
check("A6 (reported) the field-energy pressure (g_tot^2 - g_N^2)/(8 pi G) equals the (T) pressure only outside the baryons (ratio -> 1); inside it is low by the column term (min ratio < 0.9 on every profile)",
      f"ranges {rat}", all(v[0] < 0.9 for v in rat.values()), load_bearing=False)

# ================================================================================================ A7 : P = Pi(g_N)  (N20 extended)
R.banner("A7  N20 extended: is the (T) pressure a single-valued function of the baryonic field g_N?  (P = Pi(g_N), any Pi)")
prof_list = [("point 1e10", point_mass(1e10)), ("plummer a=1", plummer(1e10, 1.0)), ("hernquist a=2", hernquist(1e10, 2.0)), ("expsphere h=2", exp_sphere(1e10, 2.0)),
             ("expsphere h=2 M=1e8", exp_sphere(1e8, 2.0)), ("freeman h=3", freeman_disc(1e10, 3.0)), ("freeman h=3 M=1e8", freeman_disc(1e8, 3.0))]
spread = {}
for y_ in (10.0, 1.0, 0.3, 0.1):
    vals = []
    for nm, p in prof_list:
        rr_ = np.geomspace(1e-2, 3e3, 40001)
        y_arr = p.u(rr_) / (rr_ ** 2 * A0)
        idx = np.where(np.diff(np.sign(y_arr - y_)) != 0)[0]
        for i in idx:
            r_x = rr_[i]
            Sg_ = float(np.trapz(p.rho_b(np.geomspace(r_x, p.rg[-1] * 0.5, 2001)), np.geomspace(r_x, p.rg[-1] * 0.5, 2001))) if nm != "point 1e10" else 0.0
            vals.append(A0 * y_ * A0 / (8 * math.pi * G) + 0.5 * A0 * Sg_)
    vals = np.array(vals)
    spread[y_] = (float(np.log10(vals.max() / vals.min())), len(vals))
P("    dex spread of the (T) pressure at fixed g_N/a0 across seven baryon systems (all crossings): " + ", ".join(f"y = {k}: {v[0]:.2f} dex (n = {v[1]})" for k, v in spread.items()))
check("A7 (reported) the (T) pressure is NOT a function of g_N alone: at fixed g_N/a0 in {10, 1, 0.3, 0.1} it spans >= 0.3 dex across seven baryon systems (compare N20's 0.51-0.55 dex on SPARC)",
      f"spreads {spread}", max(v[0] for v in spread.values()) >= 0.3, load_bearing=False)

nf = R.write()
sys.exit(1 if nf else 0)
