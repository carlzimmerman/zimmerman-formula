#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
E2 -- the HT vacuum current around a static point mass (Schwarzschild-de Sitter) and CFG44's exponential sphere: does the vacuum flow converge
on / pass through matter, what is its (gauge-invariant) flux through a sphere around the galaxy in terms of M_b(<r), does the metric respond,
and how much 'compaction' would the owner's picture need.

Equations used (derived in E1):  nabla_m t^m = 1 - P/rho_vac  (P = the cap fluid's pressure; 0 for dust baryons);  T^m ~ T^m + d_n omega^{mn}.
The gauge-invariant statement is the integrated divergence = the 4-volume per unit Killing time inside the areal sphere R:
      Phi_inv(R) = Int_0^R 4 pi r^2 e^{alpha+beta} (1 - P/rho_vac) dr        ('river gauge' flux; the clock gauge has zero flux, same physics)

Hypotheses: static, spherical; weak field inside extended matter (GR correction <= 3e-4, CFG44); the cold fluid is CFG43's cap fluid holding
CFG44's hydrostatic target pressure P(r) = (a0/4 pi) Int_r^inf M_b(<r') r'^-3 dr' (the target EXCEEDS P_cap inside r_M, so the true CFG43
fluid's contribution is bounded by eps; both are reported); P2 kernel primary, nu_mono reported (CFG44 Bcommon, read-only); both footings.

MUTATE=1  the baryons are made Lambda-dependent (m -> m Lambda^beta_b, beta_b = 1): the divergence gains + beta_b rho_b/rho_vac, so the point-mass
          flux is no longer M-independent (E2-SdS-FLUX must fail).
"""
import os
import sys
import math
import numpy as np
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import E_common as C

R = C.Run("E2_static_flow_point_mass_sphere")
P, check = R.P, R.check
M = C.MUTATE
P(__doc__)
P("MUTATE mode = %d  (0 = dust baryons, Lambda-independent as in CFG43; 1 = baryon masses proportional to Lambda, beta_b = 1)" % M)
B = C.import_bcommon()

# ============================================================================================ A: point mass (SdS), exact
R.banner("A  POINT MASS (Schwarzschild-de Sitter, exact): the river-gauge current and its flux; the static test-body acceleration")
t, r, th = sp.symbols('t r theta', positive=True)
m_, L0, rv, bb = sp.symbols('m Lambda0 rho_vac beta_b', positive=True)
f = 1 - 2 * m_ / r - L0 * r ** 2 / 3
g_sds = sp.diag(-f, 1 / f, r ** 2, r ** 2 * sp.sin(th) ** 2)
sqrtg = r ** 2 * sp.sin(th)                                          # sin(theta) >= 0 on [0, pi]
det_ok = sp.simplify(-g_sds.det() - sqrtg ** 2) == 0                 # -det g = (r^2 sin theta)^2 exactly, for every m and Lambda
# river gauge: T^r(r) sin(theta) with d_r T^r = sqrt(-g) * S; S = 1 (dust), or 1 + beta_b rho_b/rho_vac with rho_b = M delta^3 (MUTATE=1)
Mb = sp.Symbol('M_b', positive=True)
Tr_river = r ** 3 / 3 * sp.sin(th) + (bb * Mb / (4 * sp.pi * rv) * sp.sin(th) if M == 1 else 0)
div_ok = sp.simplify(sp.diff(Tr_river, r) - sqrtg * 1) == 0          # away from r = 0
t_r = sp.simplify(Tr_river / sqrtg)
Flux = sp.integrate(sp.integrate(Tr_river, (th, 0, sp.pi)), (sp.Symbol('ph'), 0, 2 * sp.pi))
dFlux_dM = sp.simplify(sp.diff(Flux, m_) + sp.diff(Flux, Mb))
indep = det_ok and div_ok and dFlux_dM == 0
check("E2-SdS-FLUX", "SdS has sqrt(-g) = r^2 sin(theta) EXACTLY, so the static river-gauge vacuum current around a point mass is t^r = r/3 and its flux per unit "
      "Killing time through the areal sphere r is 4 pi r^3/3, independent of the mass: the vacuum current passes through a point mass as if it were not there",
      "sqrt(-g) = r^2 sin(theta): %s; div (r>0) = sqrt(-g): %s; t^r = %s; flux = %s; d flux/dM = %s" % (det_ok, div_ok, t_r, Flux, dFlux_dM), indep,
      "MUTATE=1: with Lambda-dependent baryons the current carries + beta_b M_b/rho_vac through every sphere" if M == 1 else
      "(the invariant statement: the 4-volume inside an areal sphere per unit Killing time is (4 pi/3) r^3 for every M)")
# the static test body's acceleration in SdS: d^2 r/d tau^2 = -Gamma^r_tt (dt/dtau)^2 = -f'/2  (c = 1, m = GM)
acc = sp.simplify(-sp.diff(f, r) / 2)
acc_ok = sp.simplify(acc - (-m_ / r ** 2 + L0 * r / 3)) == 0
check("E2-NORESP", "a test body released at rest in SdS accelerates at d^2r/dtau^2 = -GM/r^2 + Lambda c^2 r/3: Newton plus the repulsive Lambda term, with NO term "
      "from the vacuum current (T^m is absent from the metric equations, E1-NOMETRIC)", "d^2r/dtau^2 = %s" % acc, acc_ok,
      "the committed dark-energy current is locally unobservable: its only physical content is the divergence (fixed) and one global number")

# ============================================================================================ B: exponential sphere, GR volume distortion
R.banner("B  CFG44's EXPONENTIAL SPHERE (dust, weak field): the only M-dependence of the 4-volume is GR's own volume distortion")
h_, G_, c_, Mx = sp.symbols('h G c M', positive=True)
rho_exp = Mx / (8 * sp.pi * h_ ** 3) * sp.exp(-r / h_)
rp = sp.Symbol('rp', positive=True)
apb = -(G_ / c_ ** 2) * sp.integrate(4 * sp.pi * rp * rho_exp.subs(r, rp), (rp, r, sp.oo))     # alpha + beta inside (weak field)
apb_cf = sp.simplify(apb + G_ * Mx * (r + h_) * sp.exp(-r / h_) / (2 * h_ ** 2 * c_ ** 2)) == 0
Dinf = sp.simplify(-sp.integrate(4 * sp.pi * r ** 2 * apb, (r, 0, sp.oo)))
Dinf_ok = sp.simplify(Dinf - 16 * sp.pi * G_ * Mx * h_ ** 2 / c_ ** 2) == 0
Mr2 = sp.integrate(4 * sp.pi * r ** 4 * rho_exp, (r, 0, sp.oo))
gen_ok = sp.simplify(Dinf - 4 * sp.pi * G_ * Mr2 / (3 * c_ ** 2)) == 0
# numbers (the r-integral in closed form, lambdified once)
Rsym = sp.Symbol('Rsym', positive=True)
Iclosed = sp.lambdify((Rsym, h_), sp.simplify(sp.integrate(rp ** 2 * (rp + h_) * sp.exp(-rp / h_), (rp, 0, Rsym))), 'math')
fr_max = {}
for Mb_ in (1e9, 1e10, 1e11, 1e12):
    MM = Mb_ * C.MSUN
    rM = math.sqrt(C.G_SI * MM / C.A0["canonical"])
    for lab, hh in (("h=0.5rM", 0.5 * rM), ("h=3kpc", 3 * C.KPC_M)):
        x = np.geomspace(0.1, 30, 400)
        rr = x * rM
        s = rr / hh
        # D(R) = -Int_0^R 4 pi r^2 (alpha+beta) dr, closed form of the r-integral (sympy below re-checks one value)
        Dfun = lambda R_: (2 * math.pi * C.G_SI * MM / (hh ** 2 * C.C_SI ** 2)) * Iclosed(R_ / hh, 1.0) * hh ** 4
        vals = [Dfun(float(R_)) / (4 * math.pi * float(R_) ** 3 / 3) for R_ in rr]
        fr_max["%.0e %s" % (Mb_, lab)] = max(vals)
worst = max(fr_max.values())
check("E2-GR-DEFICIT", "inside dust, alpha + beta = -(G/c^2) Int_r^inf 4 pi r' rho_b dr' (exp sphere: -G M (r+h) e^{-r/h}/(2 h^2 c^2)); the 4-volume deficit outside "
      "the matter is D = 4 pi G M <r^2>/(3 c^2) (= 16 pi G M h^2/c^2 for the exp sphere): GR's volume distortion, fractionally ~ GM/(R c^2)",
      "closed form: %s; D(inf) = 16 pi G M h^2/c^2: %s; = 4 pi G M<r^2>/(3c^2): %s; max fractional deficit over x in [0.1,30], 1e9-1e12 Msun, both h: %.2e"
      % (apb_cf, Dinf_ok, gen_ok, worst), apb_cf and Dinf_ok and gen_ok and worst < 1e-4,
      "a 1e-6-level GR effect, linear in M, falling as R^-3: nothing of the MOND form sqrt(M)/r")
R.num("GR_deficit_max_fraction", fr_max)

# ============================================================================================ C: the cap fluid's divergence deficit in terms of M_b(<r)
R.banner("C  WITH CFG43's CAP FLUID AT CFG44's TARGET PRESSURE: the divergence deficit (1/rho_vac c^2) Int P dV in terms of M_b(<r)")
a0s, rr_, Mf = sp.symbols('a0 rr M_f', positive=True)
Mbf = sp.Function('M_b')
Pt = (a0s / (4 * sp.pi)) * sp.Integral(Mbf(rp) / rp ** 3, (rp, r, sp.oo))
lhs = sp.diff(sp.Rational(4, 3) * sp.pi * r ** 3 * Pt + (a0s / 3) * sp.Integral(Mbf(rp), (rp, 0, r)), r)
ibp_ok = sp.simplify((lhs - 4 * sp.pi * r ** 2 * Pt).doit()) == 0
Ppm = a0s * Mf / (8 * sp.pi * r ** 2)
pm_int = sp.integrate(4 * sp.pi * rp ** 2 * Ppm.subs(r, rp), (rp, 0, r))
pm_ok = sp.simplify(pm_int - a0s * Mf * r / 2) == 0
kap, rhoF = sp.symbols('kappa rho_F', positive=True)
xx = sp.Symbol('x', positive=True)
frac = (pm_int / rv) / (sp.Rational(4, 3) * sp.pi * r ** 3)                                   # c = 1 in this line
frac_x = sp.simplify(frac.subs({a0s: kap * sp.sqrt(G_ * rhoF), r: xx * sp.sqrt(G_ * Mf / (kap * sp.sqrt(G_ * rhoF)))}))
frac_ok = sp.simplify(frac_x - 3 * kap ** 2 / (8 * sp.pi) * (rhoF / rv) / xx ** 2) == 0
# numbers: fraction at x = 0.1, 1, 30 (canonical rho_F = rho_L; alt rho_F = rho_crit), and the cap bound eps
fr = {}
for foot in ("canonical", "alt"):
    q = C.RHO_FOOT[foot] / C.RHO_L
    fr[foot] = {"x=0.1": 3 * C.EPS * q / 0.01, "x=1": 3 * C.EPS * q, "x=3": 3 * C.EPS * q / 9, "x=30": 3 * C.EPS * q / 900}
# exp sphere: direct integral vs the formula (numerical, canonical)
MM = 1e11 * C.MSUN
a0 = C.A0["canonical"]
rM = math.sqrt(C.G_SI * MM / a0)
hh = 0.5 * rM
from scipy.integrate import quad
from scipy.special import gammainc
Mb_r = lambda x_: MM * gammainc(3.0, x_ / hh)
Pt_num = lambda x_: (a0 / (4 * math.pi)) * quad(lambda y: Mb_r(y) / y ** 3, x_, 400 * rM, limit=400)[0] + (a0 / (4 * math.pi)) * MM / (2 * (400 * rM) ** 2)
Rt = 3 * rM
direct = quad(lambda y: 4 * math.pi * y * y * Pt_num(y), 1e-6 * rM, Rt, limit=200)[0]
formula = (4 * math.pi / 3) * Rt ** 3 * Pt_num(Rt) + (a0 / 3) * quad(Mb_r, 0, Rt, limit=200)[0]
num_ok = abs(direct / formula - 1) < 1e-4
exp_frac = formula / (C.RHO_L * C.C_SI ** 2) / (4 * math.pi * Rt ** 3 / 3)
check("E2-CAP-FLUX", "Int_0^r 4 pi r'^2 P dr' = (4 pi/3) r^3 P(r) + (a0/3) Int_0^r M_b(<r') dr' for ANY M_b (the flux deficit in terms of M_b(<r)); point mass: a0 M r/2, "
      "i.e. a fraction 3 eps (rho_foot/rho_L)/x^2 of the volume; CFG43's cap P <= eps rho_vac c^2 bounds it by eps = %.4f" % C.EPS,
      "identity (sympy, arbitrary M_b): %s; point mass a0 M r/2: %s; fraction = 3 kappa^2/(8 pi x^2): %s; exp sphere (1e11, h = 0.5 r_M) direct/formula - 1 = %.1e, "
      "fraction at x = 3: %.4f; point-mass fractions (canonical) %s" % (ibp_ok, pm_ok, frac_ok, direct / formula - 1, exp_frac,
                                                                        {k: round(v, 5) for k, v in fr["canonical"].items()}),
      ibp_ok and pm_ok and frac_ok and num_ok,
      "the ONLY place the committed action lets matter 'compact' the vacuum current: a <= 1 percent change of its divergence inside the cap fluid, zero in baryons. "
      "Locally P_target/(rho_vac c^2) = eps/x^2, so at the TARGET pressure the divergence 1 - eps/x^2 would reverse sign inside x = sqrt(eps) = %.4f; "
      "CFG43's cap (P <= eps rho_vac c^2) forbids that, which is the same fact as CFG43's obstruction (the target needs P/P_cap = 1/x^2 > 1 inside r_M)" % math.sqrt(C.EPS))
R.num("cap_flux_fraction", fr)
R.num("cap_flux_fraction_expsphere_1e11_x3", exp_frac)

# ============================================================================================ D: compaction needed vs available; the active-mass sign
R.banner("D  HOW MUCH 'COMPACTION' THE PICTURE WOULD NEED (cross-check of CFG176 Q1f): rho_phantom/rho_Lambda, and the sign of a compacted w = -1 medium")
rhoL_kpc = C.RHO_L / (C.MSUN / C.KPC_M ** 3)                 # Msun/kpc^3
table = {}
for foot in ("canonical", "alt"):
    a0k = C.A0[foot] * C.KPC_M / 1e6                          # (km/s)^2/kpc
    for kern in ("P2", "nu_mono"):
        for Mb_ in (1e9, 1e10, 1e11, 1e12):
            rMk = math.sqrt(B.G * Mb_ / a0k)
            for lab, prof in (("point", B.point_mass(Mb_)), ("exp h=0.5rM", B.exp_sphere(Mb_, 0.5 * rMk)), ("exp h=3kpc", B.exp_sphere(Mb_, 3.0))):
                x = np.geomspace(0.05, 60, 3000)
                rr = x * rMk
                u = B.law_u(prof, rr, kern, a0=a0k)
                w = u - prof.u(rr)
                rho_ph = np.gradient(w, rr) / (4 * math.pi * B.G * rr ** 2)
                sel = (x >= 0.1) & (x <= 30)
                ratio = rho_ph[sel] / rhoL_kpc
                table["%s %s %.0e %s" % (foot, kern, Mb_, lab)] = (float(ratio.min()), float(ratio.max()))
# point-mass P2 analytic cross-check at x = 1: rho_c = a0/(4 pi G r_M sqrt 2)
a0 = C.A0["canonical"]
rM = math.sqrt(C.G_SI * 1e11 * C.MSUN / a0)
an = a0 / (4 * math.pi * C.G_SI * rM * math.sqrt(2)) / C.RHO_L
lo = min(v[0] for v in table.values())
hi = max(v[1] for v in table.values())
P("  rho_phantom/rho_Lambda over x in [0.1, 30]  (min, max):")
for k, v in table.items():
    if "canonical P2" in k or ("alt P2" in k and "point" in k):
        P("    %-40s %9.3g  %9.3g" % (k, v[0], v[1]))
P("  point mass P2 canonical 1e11 at x = 1, analytic a0/(4 pi G r_M sqrt2)/rho_L = %.4g" % an)
check("E2-COMPACTION", "to BE the law's phantom, the vacuum would have to reach rho_ph/rho_Lambda >> 1 everywhere in x in [0.1, 30] for 1e9-1e12 Msun "
      "(both kernels, both footings, point mass and exp spheres); the committed action's Lambda is a global constant, so its actual compaction is exactly 1",
      "needed range %.3g .. %.3g (min over all rows > 1: %s); available: 1 (d_m Lambda = 0, E1-FIELD)" % (lo, hi, lo > 1), lo > 1,
      "scales as M^-1/2 at fixed x; the full table is in the results JSON")
R.num("compaction_needed", table)
# active gravitational mass of a perfect fluid at rest, weak field: R_00 = 8 pi G (T_00 - g_00 T/2) => source rho + 3p/c^2
rho_s, p_s = sp.symbols('rho p', real=True)
gdiag = sp.diag(-1, 1, 1, 1)
Tdn = sp.diag(rho_s, p_s, p_s, p_s)                       # T_mu nu at rest, c = 1, signature (-,+,+,+)
Ttr = sum(sp.Matrix(gdiag).inv()[i, i] * Tdn[i, i] for i in range(4))
src = sp.simplify(Tdn[0, 0] - gdiag[0, 0] * Ttr / 2)
act_ok = sp.simplify(src - (rho_s + 3 * p_s) / 2) == 0
act_vac = sp.simplify(2 * src.subs(p_s, -rho_s))
need_neg = all(-0.5 * v[0] < -1 for v in table.values())
check("E2-ACTIVE", "the focusing (attraction) a medium exerts on free-falling matter is R_mn u^m u^n = 8 pi G (T_mn - g_mn T/2) u^m u^n = 4 pi G (rho + 3p) at rest "
      "(Raychaudhuri; sympy: T_00 - g_00 T/2 = (rho + 3p)/2); for a w = -1 medium rho + 3p = -2 rho: COMPACTING the Lambda-vacuum DEFOCUSES (repels).  To mimic "
      "the phantom's focusing with a w = -1 medium the local vacuum energy would have to DROP by rho_ph/2, i.e. go negative by 10^%.1f - 10^%.1f rho_Lambda "
      "(and a w = -1 medium cannot be inhomogeneous at all without an energy exchange: nabla(rho g) = 0 forces d rho = 0, cf. CFG176 1b)"
      % (math.log10(0.5 * lo), math.log10(0.5 * hi)),
      "(rho+3p)/2 identity: %s; w = -1: rho + 3p = %s; required delta rho_vac/rho_Lambda < -1 in every row: %s" % (act_ok, act_vac, need_neg),
      act_ok and act_vac == -2 * rho_s and need_neg,
      "so under Addendum 2 (no rest mass) the flow's boost must come from a non-vacuum stress (w > -1/3) or a non-metric coupling; E3/E4 test the minimal one")

P("")
P("  THE FLOW AROUND A GALAXY, AS DERIVED:  the flux through a sphere is a gauge choice (any value, E1-SPLIT); the gauge-invariant 4-volume per unit Killing")
P("  time inside the areal sphere R is  (4 pi/3) R^3  -  4 pi G M <r^2>/(3 c^2) [GR, R outside the matter]  -  [(4 pi/3) R^3 P(R) + (a0/3) Int_0^R M_b dr]/(rho_vac c^2)")
P("  [cap fluid at the target pressure; <= eps (4 pi/3) R^3].  Nothing in the metric responds to it; baryons do not source it.")
R.finish()
