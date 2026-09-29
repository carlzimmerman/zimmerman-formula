#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
B2 -- CLASS (i): CAN A BAROTROPIC FLUID P = Pi(rho_c) IN GR (WEAK-FIELD LIMIT: NEWTONIAN, N7 of B1) REPRODUCE THE TARGET (T) OF B1?
     Extension of N20 (which treated P = Pi(|g|) and P = Pi(g_N)) to the fluid's own density, and to fluids that feel an extra symmetric force.

EXACT HYPOTHESES.  (a) static, spherical, weak-field; (b) the fluid's stress is barotropic, P = Pi(rho_c), with Pi UNIVERSAL (the same function for every
baryonic system: it may contain G, a0, the fluid's constants m, eps, lambda, but NOT the baryon mass M_b or the baryon profile); (c) the fluid feels
g_felt = g_tot (+ optionally a static extra force, see E3/E4); (d) the fluid density is the target (T).
THEN  Pi'(rho_c) = c_s^2(rho) = rho g_felt / |drho_c/dr|  is fixed pointwise by (T), and must be the SAME function of rho for every system.

RESULTS (all sympy-derived, then checked numerically):
  E1  point mass:  c_s^2 = sqrt(G M a0) (1 + x^2)^(3/2) / (x (1 + 2 x^2)),  x = r/r_M.  At FIXED rho it scales as M^e with
      e(x) = 1/2 - (1/2) [(1+x^2)/(1+2x^2)] dlnS/dlnx in [1/2, 1]  (deep: 1/2 [c_s^2 -> V_f^2/2 = sqrt(G M a0)/2];  Newtonian: 1 [c_s^2 = 4 pi G^2 M rho/a0]);
      a universal EOS needs e = 0.   => EXCLUDED, for every Pi.
  E2  the required effective index Gamma = dln P/dln rho = 2 (1 + x^2)/(1 + 2 x^2) runs from 2 (inside r_M) to 1 (outside): not a polytrope even with a
      system-dependent normalisation K(M_b).
  E3  extra Poisson-type force g_felt = G [a M_b + b M_c]/r^2 (a = 1 + beta_bc, b = 1 + beta_cc; symmetric second-potential couplings): the universality condition
      S_ab(x) = k x sqrt(1+x^2) is unsatisfiable (sympy series); numerically e(x; a, b) never vanishes identically.
  E4  ANY fixed-kernel force linear in M_b, g_x = M_b gamma(r) (plus a fluid self-force beta G M_c/r^2), any kernel gamma: deep regime forces beta = -1,
      gamma = lambda r^-5, Pi ~ rho^3;  the Newtonian regime then forces gamma = -(1 + beta_bc) G/r^2: contradiction (sympy).
  E5  same M_b, different baryon SHAPE (point / Plummer / Hernquist / exp. sphere): c_s^2 at equal rho differs.
CHECKS: E1 e in [0.45, 1.05] over x and numerically over M = 1e8..1e14; E2; E3; E4; E5.
MUTATE=1: the target is replaced by the singular isothermal sphere family with a UNIVERSAL sigma0 (a genuinely barotropic system: c_s^2 = sigma0^2 for every M):
  E1 (e >= 0.45), E2 (Gamma varies) and E5 must FAIL (rc = 1).
Run: python3 B2_barotropic_nogo.py   (MUTATE=1 for the control)
"""
import os, sys, math
import numpy as np
import sympy as sp
from scipy.optimize import minimize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Bcommon import *

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = Report("B2_barotropic_nogo", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: universal-sigma0 singular isothermal spheres in place of the target -- E1, E2, E5 must FAIL ***")

# ============================================================================================ E1, E2, E3, E4 : sympy
R.banner("E1/E2  SYMPY: required c_s^2, its mass exponent at fixed density, the effective polytropic index (point mass)")
x, A, a_, b_ = sp.symbols("x A a b", positive=True)
rho_x = 1 / (x * sp.sqrt(1 + x ** 2))                       # rho_c / [a0/(4 pi G r_M)]
g_x = sp.sqrt(1 + x ** 2) / x ** 2                          # g_tot / (G M / r_M^2)
# c_s^2 = rho g / |rho'| ; in units of G M / r_M = sqrt(G M a0):
cs2_x = sp.simplify(rho_x * g_x / (-sp.diff(rho_x, x)))
S_x = sp.simplify((1 + x ** 2) ** sp.Rational(3, 2) / (x * (1 + 2 * x ** 2)))
dlnS = sp.simplify(x * sp.diff(sp.log(S_x), x))
dlnx_dlnM = -sp.Rational(1, 2) * (1 + x ** 2) / (1 + 2 * x ** 2)    # fixed rho: rho x sqrt(1+x^2) = rho_M ~ M^-1/2
e_x = sp.simplify(sp.Rational(1, 2) + dlnS * dlnx_dlnM)
Gam_x = sp.simplify(2 * (1 + x ** 2) / (1 + 2 * x ** 2))
Gam_direct = sp.simplify(sp.diff(sp.log(1 / x ** 2), x) / sp.diff(sp.log(rho_x), x))          # P ~ x^-2 (a0 M/(8 pi r^2)):  dlnP/dlnrho
e_lim0 = sp.limit(e_x, x, 0); e_limi = sp.limit(e_x, x, sp.oo)
e_fun = sp.lambdify(x, e_x, "numpy")
xs = np.geomspace(1e-4, 1e4, 4001)
e_num = e_fun(xs)
P(f"    c_s^2/sqrt(G M a0) = {cs2_x};  exponent e(x) = {e_x};  Gamma(x) = {Gam_x}")
P(f"    e(0) = {e_lim0}, e(inf) = {e_limi}; min/max of e over x in [1e-4,1e4]: {e_num.min():.4f}, {e_num.max():.4f}; Gamma direct - claimed = {sp.simplify(Gam_direct - Gam_x)}")
s1 = sp.simplify(cs2_x - S_x)
if MUTATE:
    # universal isothermal spheres: c_s^2 = sigma0^2 independent of M and x: exponent 0, Gamma = 1
    e_num = np.zeros_like(xs); e_lim0 = sp.Integer(0); e_limi = sp.Integer(0)
    Gam_x_fun = lambda xx: np.ones_like(xx)
else:
    Gam_x_fun = sp.lambdify(x, Gam_x, "numpy")
check("E1 (sympy) at FIXED rho the required c_s^2 scales as M^e with e(0) = 1, e(inf) = 1/2 and e in [1/2, 1] for all x: no universal Pi(rho)"
      + ("  [MUTATE: universal sigma0]" if MUTATE else ""),
      f"c_s^2 formula residual {s1}; e(0) = {e_lim0}, e(inf) = {e_limi}; range [{e_num.min():.4f}, {e_num.max():.4f}]",
      s1 == 0 and e_lim0 == 1 and e_limi == sp.Rational(1, 2) and e_num.min() >= 0.45 and e_num.max() <= 1.05)
Gg = Gam_x_fun(xs)
check("E2 (sympy) the required effective index Gamma = dlnP/dlnrho = 2(1+x^2)/(1+2x^2) runs from 2 (x << 1) to 1 (x >> 1): not a polytrope for any K(M_b)"
      + ("  [MUTATE]" if MUTATE else ""), f"Gamma range [{Gg.min():.3f}, {Gg.max():.3f}]; direct-vs-claimed residual {sp.simplify(Gam_direct - Gam_x)}",
      Gg.max() - Gg.min() > 0.9 and sp.simplify(Gam_direct - Gam_x) == 0)

# ---- numeric: exponent at fixed rho from the ODE solutions for M = 1e8 .. 1e14 (and from the closed form)
R.banner("E1 numeric: c_s^2(rho) for point masses of different M (target integrated as an ODE, not the closed form)")
Ms = [1e8, 1e9, 1e10, 1e11, 1e12, 1e13, 1e14]
tabs = {}
for M in Ms:
    p = point_mass(M)
    rM = math.sqrt(M * G / A0)
    if MUTATE:
        rr = np.geomspace(1e-3 * rM, 1e3 * rM, 8001)
        s2 = 1.0e4                                                             # universal sigma0^2 (km/s)^2: rho = s2/(2 pi G r^2), g = 2 s2/r
        rho = s2 / (2 * math.pi * G * rr ** 2); cs2 = np.full_like(rr, s2)
    else:
        f_ = target_fields(p, r0=1e-3 * rM, r1=1e3 * rM, n=8001)
        rho, cs2 = f_["rho"], f_["cs2"]
    tabs[M] = (rho, cs2)
rho_lo = max(t[0].min() for t in tabs.values()); rho_hi = min(t[0].max() for t in tabs.values())
rho_grid = np.geomspace(rho_lo * 1.5, rho_hi / 1.5, 25) if rho_hi > rho_lo * 3 else np.array([])
cs_at = {}
for M, (rho, cs2) in tabs.items():
    order = np.argsort(rho)
    cs_at[M] = np.exp(np.interp(np.log(rho_grid), np.log(rho[order]), np.log(cs2[order])))
lnM = np.log(np.array(Ms))
exps = []
for j in range(len(rho_grid)):
    y = np.log([cs_at[M][j] for M in Ms])
    exps.append(np.polyfit(lnM, y, 1)[0])
exps = np.array(exps)
spread = np.array([max(cs_at[M][j] for M in Ms) / min(cs_at[M][j] for M in Ms) for j in range(len(rho_grid))])
P(f"    common density window: rho in [{rho_grid.min():.2e}, {rho_grid.max():.2e}] Msun/kpc^3 ({len(rho_grid)} points) for M = 1e8..1e14")
P(f"    fitted exponent d ln c_s^2/d ln M at fixed rho: min {exps.min():.3f}, median {np.median(exps):.3f}, max {exps.max():.3f}")
P(f"    ratio c_s^2(M = 1e14)/c_s^2(M = 1e8) at fixed rho: min {spread.min():.2f}, max {spread.max():.2f}  (a universal EOS needs exactly 1)")
check("E1n numeric: at every common density the fitted exponent of the required c_s^2 with M is in [0.45, 1.05] and the M = 1e8 .. 1e14 spread is >= 30x"
      + ("  [MUTATE]" if MUTATE else ""), f"exponent in [{exps.min():.3f}, {exps.max():.3f}]; spread >= {spread.min():.1f}x",
      len(rho_grid) > 0 and exps.min() >= 0.45 and exps.max() <= 1.05 and spread.min() >= 30)
R.num("E1n", dict(exp_min=float(exps.min()), exp_max=float(exps.max()), spread_min=float(spread.min())))

# ---- E1m: the same test with the law's own nu_mono phantom (the SPARC-preferred kernel) as the fluid density
R.banner("E1m  the same test with the nu_mono phantom (fluid density = the law's phantom for nu_mono), point masses of different M")
tabm = {}
for M in Ms:
    p = point_mass(M)
    rM = math.sqrt(M * G / A0)
    r_ = np.geomspace(1e-2 * rM, 1e3 * rM, 6001)
    if MUTATE:
        s2 = 1.0e4
        rho = s2 / (2 * math.pi * G * r_ ** 2); cs2 = np.full_like(r_, s2)
    else:
        e_ = 2e-3
        ul = lambda rr: law_u(p, rr, "nu_mono")
        wph = lambda rr: ul(rr) - p.u(rr)
        dw = (wph(r_ * (1 + e_)) - wph(r_ * (1 - e_))) / (2 * r_ * e_)
        rho = dw / (4 * math.pi * G * r_ ** 2)
        g_ = ul(r_) / r_ ** 2
        dln = np.gradient(np.log(rho), np.log(r_))
        cs2 = g_ * r_ / (-dln)
    tabm[M] = (rho, cs2)
lo_m = max(t[0].min() for t in tabm.values()); hi_m = min(t[0].max() for t in tabm.values())
rgm = np.geomspace(lo_m * 2, hi_m / 2, 25)
csm = {}
for M, (rho, cs2) in tabm.items():
    order = np.argsort(rho)
    csm[M] = np.exp(np.interp(np.log(rgm), np.log(rho[order]), np.log(np.abs(cs2[order]))))
exm = np.array([np.polyfit(np.log(Ms), np.log([csm[M][j] for M in Ms]), 1)[0] for j in range(len(rgm))])
spm = np.array([max(csm[M][j] for M in Ms) / min(csm[M][j] for M in Ms) for j in range(len(rgm))])
P(f"    nu_mono phantom: exponent d ln c_s^2/d ln M at fixed rho in [{exm.min():.3f}, {exm.max():.3f}] (deep 1/2, rising toward the Newtonian side); spread M = 1e8..1e14: min {spm.min():.0f}x, max {spm.max():.0f}x")
check("E1m the nu_mono phantom is no more barotropic than the P2 target: the required c_s^2 scales as M^e with e in [0.45, 1.05] at every common density and spreads >= 30x over M = 1e8 .. 1e14"
      + ("  [MUTATE: universal sigma0]" if MUTATE else ""), f"exponent in [{exm.min():.3f}, {exm.max():.3f}]; spread >= {spm.min():.0f}x", exm.min() >= 0.45 and exm.max() <= 1.05 and spm.min() >= 30)
R.num("E1m", dict(exp_min=float(exm.min()), exp_max=float(exm.max()), spread_min=float(spm.min())))

# ============================================================================================ E3 : symmetric Poisson-type forces
R.banner("E3  barotropic fluid + extra Poisson-type force g_felt = G [a M_b + b M_c]/r^2 (a = 1 + beta_bc, b = 1 + beta_cc)")
S_ab = (a_ + b_ * (sp.sqrt(1 + x ** 2) - 1)) * (1 + x ** 2) / (x * (1 + 2 * x ** 2))
cond = sp.series(sp.simplify(S_ab - sp.Symbol("k") * x * sp.sqrt(1 + x ** 2)), x, 0, 6).removeO()
cond = sp.expand(cond)
coef = {k: sp.simplify(cond.coeff(x, k)) for k in range(-1, 6)}
k_ = sp.Symbol("k")
# order x^-1: a ; order x^1: b/2 - k ; order x^3: ... solve successively
eq_m1 = coef[-1]
sol_a = sp.solve(eq_m1, a_)
P(f"    small-x expansion of S_ab - k x sqrt(1+x^2): coefficients { {k: coef[k] for k in (-1, 0, 1, 2, 3)} }")
# after a = 0:
cond0 = sp.series(sp.simplify((S_ab.subs(a_, 0) - k_ * x * sp.sqrt(1 + x ** 2))), x, 0, 6).removeO()
c1 = sp.simplify(cond0.coeff(x, 1)); c3 = sp.simplify(cond0.coeff(x, 3))
sol_k = sp.solve(c1, k_)
c3_sub = sp.simplify(c3.subs(k_, sol_k[0]))
P(f"    with a = 0: order x^1 gives k = {sol_k}; order x^3 then leaves {c3_sub} (= 0 only if b = 0, i.e. no force at all)")
unsat = (sol_a == [] or sol_a == [0]) and sp.simplify(c3_sub) != 0
# numeric scan of sup_x |e(x; a, b)| over a grid of couplings
e_ab = sp.simplify(sp.Rational(1, 2) - sp.Rational(1, 2) * (1 + x ** 2) / (1 + 2 * x ** 2) * x * sp.diff(sp.log(S_ab), x))
e_ab_f = sp.lambdify((x, a_, b_), e_ab, "numpy")
xs2 = np.geomspace(1e-3, 1e3, 600)
best = (9.0, None)
grid = np.linspace(-1.0, 6.0, 43)
for av in grid:
    for bv in grid:
        if abs(av) < 1e-9 and abs(bv) < 1e-9:
            continue                                                             # g_felt = 0: the fluid does not gravitate (excluded by T4/GR)
        with np.errstate(all="ignore"):
            ev = e_ab_f(xs2, av, bv)
        ev = ev[np.isfinite(ev)]
        if len(ev) < 100:
            continue
        m = float(np.max(np.abs(ev)))
        if m < best[0]:
            best = (m, (av, bv))
res_opt = minimize(lambda v: float(np.nanmax(np.abs(e_ab_f(xs2, v[0], v[1])))), x0=np.array(best[1]), method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-6, maxiter=400))
P(f"    min over (a, b) in [-1, 6]^2 (a = b = 0 excluded) of sup_x |e(x; a, b)|: grid {best[0]:.3f} at (a, b) = {best[1]}; refined {res_opt.fun:.3f} at {np.round(res_opt.x, 3)}")
e_inf_b = sp.limit(e_ab, x, sp.oo)
e_inf_b0 = sp.limit(e_ab.subs(b_, 0), x, sp.oo)
P(f"    deep-regime exponent e(inf; a, b) = {e_inf_b} for b != 0 and {e_inf_b0} for b = 0: the exponent cannot be brought to 0 by ANY choice of (a, b)")
check("E3 (sympy + scan) no symmetric Poisson-type force (any a, b) makes the target barotropic-universal: the condition S_ab = k x sqrt(1+x^2) is unsatisfiable, "
      "and sup_x |e(x;a,b)| stays > 0.05 on the whole coupling scan" + ("  [MUTATE: not applicable, sympy part unchanged]" if MUTATE else ""),
      f"a = 0 branch leaves x^3 coefficient {c3_sub}; e(inf) = {e_inf_b} (b != 0) or {e_inf_b0} (b = 0); min sup|e| = {res_opt.fun:.3f} at (a, b) = {np.round(res_opt.x, 3)}",
      unsat and res_opt.fun > 0.05 and e_inf_b == sp.Rational(1, 2) and e_inf_b0 == sp.Rational(3, 4))

# ============================================================================================ E4 : fixed-kernel linear couplings (any kernel)
R.banner("E4  SYMPY: ANY fixed-kernel force linear in M_b (g_felt = M_b Gam_tot(r) + (1 + beta) G M_c/r^2) on a universal barotropic fluid")
rr_, rho_ = sp.symbols("r rho", positive=True)
beta_ = sp.Symbol("beta", real=True)
lam_ = sp.Symbol("lambda", real=True)
Gt = sp.Function("Gamma_tot")(rr_)                                                 # total baryon -> fluid force kernel (Newton + any extra), G = a0 = 1
# deep regime x >> 1: rho = t/(4 pi r^2), g_tot = t/r, M_c = t r, |rho'|/rho = 2/r, t = sqrt(M) = 4 pi rho r^2  =>  c_s^2 = (r/2) g_felt
t = 4 * sp.pi * rho_ * rr_ ** 2
cs2_deep = sp.expand((rr_ / 2) * ((1 + beta_) * t / rr_ + t ** 2 * Gt))
d1 = sp.expand(sp.diff(cs2_deep, rr_))                                             # universality: d c_s^2/dr = 0 at fixed rho, for ALL rho
Gp = sp.Symbol("Gp")                                                                # Gp = d(r^5 Gamma_tot)/dr
d1_ = sp.expand(d1.subs(sp.Derivative(Gt, rr_), (Gp - 5 * rr_ ** 4 * Gt) / rr_ ** 5))
poly_rho = sp.Poly(d1_, rho_)
coeffs = [sp.simplify(c_) for c_ in poly_rho.all_coeffs()]
sol_beta = sp.solve(coeffs[-2], beta_)                                              # coefficient of rho^1: 4 pi (1 + beta) r = 0
sol_Gp = sp.solve(coeffs[-3], Gp)                                                   # coefficient of rho^2: 8 pi^2 Gp = 0
P(f"    deep regime, d c_s^2/dr = 0 for ALL rho: coefficients of rho^1, rho^2: {coeffs[-2]}, {coeffs[-3]}  =>  beta = {sol_beta}, d(r^5 Gamma_tot)/dr = {sol_Gp}")
cs2_b = sp.simplify(cs2_deep.subs(beta_, -1).subs(Gt, lam_ / rr_ ** 5))
P(f"    => Gamma_tot = lambda r^-5 and c_s^2 = {cs2_b}: a Gamma = 3 polytrope (P ~ rho^3), a force kernel r^-5, and the fluid's own gravity cancelled (beta = -1,")
P("       i.e. G_cc = 0: for a symmetric second potential that needs a WRONG-SIGN (ghost) coupling G_tilde s_c^2 = -G)")
# Newtonian regime x << 1: rho = a0/(4 pi G r) independent of M, |rho'|/rho = 1/r, c_s^2 = r g_felt, g_felt = M lambda r^-5 (self term cancelled)
Mm = sp.Symbol("M", positive=True)
cs2_newt = rr_ * Mm * lam_ / rr_ ** 5
dM_num = sp.expand(sp.diff(cs2_newt, Mm) * rr_ ** 4)                                # must vanish for all r (rho, hence c_s^2, is M-independent at fixed r)
sol_newt = sp.solve(sp.Poly(dM_num, rr_).all_coeffs(), lam_, dict=True) if dM_num != 0 else [{}]
P(f"    Newtonian regime: c_s^2 = r g_felt = M lambda r^-4 must be M-independent at fixed r  =>  lambda = {sol_newt} => g_felt = 0 identically")
contradiction = (sol_beta == [-1]) and (sol_Gp == [0]) and (sol_newt and sol_newt[0].get(lam_, None) == 0)
check("E4 (sympy) a universal barotropic fluid with ANY fixed-kernel force linear in M_b: deep regime forces beta = -1, Gamma_tot = lambda r^-5 (Pi ~ rho^3); the "
      "Newtonian regime then forces lambda = 0, i.e. g_felt = 0 (a fluid that feels no gravity at all): contradiction with H2/GR",
      f"beta = {sol_beta}; d(r^5 Gamma_tot)/dr = {sol_Gp}; Newtonian lambda = {sol_newt}", bool(contradiction))

# ---- E4 inputs verified against the ODE solution: deep regime rho r^2 -> V_f^2/(4 pi G), g_tot r -> V_f^2, |dln rho/dln r| -> 2 ; Newtonian regime rho r -> a0/(4 pi G)
R.banner("E4 inputs: the deep-regime and Newtonian-regime forms used above, checked on the ODE solution")
pM = point_mass(1e10)
rMk = math.sqrt(1e10 * G / A0)
fq = target_fields(pM, r0=1e-3 * rMk, r1=1e4 * rMk, n=8001)
Vf2 = math.sqrt(G * 1e10 * A0)
i_deep = int(np.argmin(np.abs(fq["r"] - 3e3 * rMk))); i_new = int(np.argmin(np.abs(fq["r"] - 3e-3 * rMk)))
d1 = abs(fq["rho"][i_deep] * fq["r"][i_deep] ** 2 * 4 * math.pi * G / Vf2 - 1); d2 = abs(fq["g"][i_deep] * fq["r"][i_deep] / Vf2 - 1); d3 = abs(fq["dln"][i_deep] + 2)
d4 = abs(fq["rho"][i_new] * fq["r"][i_new] * 4 * math.pi * G / A0 - 1); d5 = abs(fq["dln"][i_new] + 1)
P(f"    deep (x = 3e3): |rho r^2 4 pi G/V_f^2 - 1| = {d1:.1e}, |g r/V_f^2 - 1| = {d2:.1e}, |dln rho/dln r + 2| = {d3:.1e};  Newtonian (x = 3e-3): |rho r 4 pi G/a0 - 1| = {d4:.1e}, |dln rho/dln r + 1| = {d5:.1e}")
check("E4i the asymptotic forms fed into E4 (rho = V_f^2/(4 pi G r^2), g r = V_f^2, slope -2 deep; rho = a0/(4 pi G r), slope -1 Newtonian) hold on the ODE solution to 1e-3",
      f"max deviation {max(d1, d2, d3, d4, d5):.1e}", max(d1, d2, d3, d4, d5) < 1e-3, load_bearing=True)

# ============================================================================================ E5 : shape dependence at fixed M
R.banner("E5  same baryonic mass, different baryon SHAPE: c_s^2 at equal rho")
M0 = 1e10
shapes = {"point": point_mass(M0), "plummer(a=1)": plummer(M0, 1.0), "hernquist(a=2)": hernquist(M0, 2.0),
          "expsphere(h=2)": exp_sphere(M0, 2.0), "expsphere(h=20)": exp_sphere(M0, 20.0)}
rM0 = math.sqrt(M0 * G / A0)
curves = {}
for nm, p in shapes.items():
    if MUTATE:
        rr = np.geomspace(1e-3 * rM0, 1e3 * rM0, 8001); s2 = 1.0e4
        rho = s2 / (2 * math.pi * G * rr ** 2); cs2 = np.full_like(rr, s2)
    else:
        f_ = target_fields(p, r0=1e-3 * rM0, r1=1e3 * rM0, n=8001)
        rr, rho, cs2 = f_["r"], f_["rho"], f_["cs2"]
    ok = rr > 3e-3 * rM0                                                         # drop the start-up transient of the ODE
    curves[nm] = (rho[ok], cs2[ok])
ref = curves["point"][0]
# interior-sensitive window: the point-mass density at r = 0.1 r_M ... 20 r_M
ilo, ihi = np.argmin(np.abs(np.log(ref) - np.log(np.interp(20 * rM0, shapes["point"].rg, np.ones_like(shapes["point"].rg)) * 1))), 0
rg_pm = target_fields(shapes["point"], r0=1e-3 * rM0, r1=1e3 * rM0, n=8001) if not MUTATE else None
if MUTATE:
    rho_a, rho_b_ = curves["point"][0][np.argmin(np.abs(np.geomspace(1e-3 * rM0, 1e3 * rM0, 8001)[np.geomspace(1e-3 * rM0, 1e3 * rM0, 8001) > 3e-3 * rM0] - 20 * rM0))], curves["point"][0][np.argmin(np.abs(np.geomspace(1e-3 * rM0, 1e3 * rM0, 8001)[np.geomspace(1e-3 * rM0, 1e3 * rM0, 8001) > 3e-3 * rM0] - 0.1 * rM0))]
else:
    rr_pm = rg_pm["r"]; rho_pm = rg_pm["rho"]
    rho_a = float(np.interp(20 * rM0, rr_pm, rho_pm)); rho_b_ = float(np.interp(0.1 * rM0, rr_pm, rho_pm))
rg = np.geomspace(rho_a, rho_b_, 40)
vals = {}
for nm, c_ in curves.items():
    order = np.argsort(c_[0])
    vals[nm] = np.exp(np.interp(np.log(rg), np.log(c_[0][order]), np.log(c_[1][order]), left=np.nan, right=np.nan))
V = np.array([vals[n] for n in vals])
ratio = np.nanmax(V, axis=0) / np.nanmin(V, axis=0)
P(f"    density window [{rg.min():.2e}, {rg.max():.2e}]; max/min c_s^2 across the five shapes: min {ratio.min():.2f}, median {np.median(ratio):.2f}, max {ratio.max():.2f}")
check("E5 at equal density and equal M_b the required c_s^2 differs between baryon shapes (median max/min >= 1.2): no universal Pi even at fixed baryonic mass"
      + ("  [MUTATE]" if MUTATE else ""), f"median ratio {np.median(ratio):.2f}, max {ratio.max():.2f}", np.median(ratio) >= 1.2)
R.num("E5", dict(ratio_median=float(np.median(ratio)), ratio_max=float(ratio.max())))

# ============================================================================================ what a universal-EOS fluid WOULD give (cost of the class)
R.banner("Cost of class (i): a self-gravitating barotropic fluid with universal sigma0 has V_f = const (BTFR slope 0)")
if not MUTATE:
    rows = []
    for M in (1e8, 1e10, 1e12):
        Vlaw = (G * M * A0) ** 0.25
        s2 = 0.5 * (G * 1e10 * A0) ** 0.5                                       # sigma0^2 tuned so the M = 1e10 system is reproduced
        Vsis = math.sqrt(2 * s2)
        rows.append((M, Vlaw, Vsis, math.log10(Vsis / Vlaw)))
        P(f"    M_b = {M:.0e}: V_f(law) = {Vlaw:6.1f} km/s; universal-isothermal V_f = {Vsis:6.1f} km/s; offset {math.log10(Vsis / Vlaw):+.3f} dex in V (= {4 * math.log10(Vsis / Vlaw):+.2f} dex in g_flat)")
    check("E6 (reported) tuning a universal sigma0 at M_b = 1e10 misses the law's flat speed by 0.5 dex in V at M_b = 1e8 and 1e12 (BTFR slope 4 vs 0)",
          f"offsets {[round(r_[3], 3) for r_ in rows]}", abs(rows[0][3]) > 0.4 and abs(rows[2][3]) > 0.4, load_bearing=False)

nf = R.write()
sys.exit(1 if nf else 0)
