#!/usr/bin/env python3
"""C4_khronon_parent: is the Blanchet-Skordis Khronon theory a covariant parent of the screened theory?

External inputs (BS24 = arXiv:2404.06584v2, BS25 = arXiv:2507.00912v1) were read via WebFetch of the arXiv HTML,
NOT verified on disk; every one used here is re-derived from the quoted action (K1, K7) as a transcription check.
Units c = 1 in the symbolic parts. kappa = 1/2 FITTED. Footings 9.36e-11 / 1.13e-10 m/s^2, never pooled.

Run: OMP_NUM_THREADS=1 nice -n 10 python3 c4_khronon_parent.py      (C4_MUTATE=1 for the mutation run)
"""
import json
import math
import os
import sys
import time

import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq

T0 = time.time()
MUTATE = os.environ.get("C4_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, f"c4_khronon_parent{TAG}.out")
JSON = os.path.join(HERE, f"c4_khronon_parent_results{TAG}.json")

c = 2.99792458e8
AU = 1.495978707e11
PC = 3.0856775814913673e16
KPC = 1e3 * PC
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
LAMBDA = 1.0890e-52  # m^-2, the record's quoted Lambda (D7 / A28 input)

lines, checks, res = [], [], {"mutate": MUTATE}


def log(s):
    print(s)
    lines.append(s)


def check(kid, ok, value, thr):
    checks.append({"id": kid, "pass": bool(ok), "value": str(value), "threshold": thr})
    log(f"{kid} {'PASS' if ok else 'FAIL'} {value} {thr}")


# =============================================================== K1 static weak-field limit of BS24
x, y, z, t = sp.symbols("x y z t", real=True)
X = (t, x, y, z)
eps, G, mu, rho = sp.symbols("epsilon G mu rho", positive=True)
psi = sp.Function("psi")(x, y, z)
phi = sp.Function("phi")(x, y, z)
Jh = sp.Function("Jh")  # J(Y) - J(0), scaled: J(eps^2 Yh) - J0 = eps^2 Jh(Yh)  (a0 = O(eps))

Nl = sp.sqrt(1 + 2 * eps * psi)  # lapse
gmat = sp.diag(-(1 + 2 * eps * psi), *([1 - 2 * eps * phi] * 3))
ginv = gmat.inv()
sqrtg = sp.sqrt(-gmat.det())


def christoffel(gm, gi):
    Gm = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for cc in range(4):
                Gm[a][b][cc] = sp.Rational(1, 2) * sum(
                    gi[a, d] * (sp.diff(gm[d, b], X[cc]) + sp.diff(gm[d, cc], X[b]) - sp.diff(gm[b, cc], X[d]))
                    for d in range(4))
    return Gm


Gam = christoffel(gmat, ginv)


def ricci_scalar(gi, Gm):
    Rs = 0
    for b in range(4):
        for d in range(4):
            if gi[b, d] == 0:
                continue
            Rbd = 0
            for a in range(4):
                Rbd += sp.diff(Gm[a][b][d], X[a]) - sp.diff(Gm[a][b][a], X[d])
                for e in range(4):
                    Rbd += Gm[a][a][e] * Gm[e][b][d] - Gm[a][d][e] * Gm[e][b][a]
            Rs += gi[b, d] * Rbd
    return Rs


def trunc(expr, order=2):
    return sp.series(expr, eps, 0, order + 1).removeO()


R = ricci_scalar(ginv, Gam)
LR = sp.expand(trunc(sqrtg * R))
# khronon tau = t: n_mu = -(1/Q) d_mu t with Q = sqrt(-g^{00}) (Eqs. 1-2), A_mu = n^nu nabla_nu n_mu (Eq. 3)
Q = sp.sqrt(-ginv[0, 0])
n_lo = [-1 / Q, 0, 0, 0]
n_up = [sum(ginv[a, b] * n_lo[b] for b in range(4)) for a in range(4)]
A_lo = []
for m in range(4):
    val = 0
    for nu in range(4):
        cov = sp.diff(n_lo[m], X[nu]) - sum(Gam[l][nu][m] * n_lo[l] for l in range(4))
        val += n_up[nu] * cov
    A_lo.append(sp.simplify(val))
A_res = [sp.simplify(A_lo[i] - sp.diff(sp.log(Nl), X[i])) for i in (1, 2, 3)] + [sp.simplify(A_lo[0])]
# second form of Eq. 3: -q_mu^nu d_nu ln Q
q_mix = sp.eye(4) + sp.Matrix(4, 4, lambda a, b: n_lo[a] * n_up[b])
A_alt = [sp.simplify(-sum(q_mix[m, nu] * sp.diff(sp.log(Q), X[nu]) for nu in range(4)) - A_lo[m]) for m in range(4)]
Y = sp.simplify(sum(ginv[a, b] * A_lo[a] * A_lo[b] for a in range(4) for b in range(4)))
Y2 = sp.simplify(trunc(Y, 2) / eps ** 2)
gradpsi2 = sum(sp.diff(psi, v) ** 2 for v in (x, y, z))
Y_res = sp.simplify(Y2 - gradpsi2)
Kq = mu ** 2 * (Q - 1) ** 2
LK = sp.expand(trunc(sqrtg * 2 * Kq))
# Lagrangian: (1/16piG)[sqrt(-g)R - 2 sqrt(-g)(J - J0) + 2 sqrt(-g) K] + matter (static dust, rho -> eps rho)
Lfull = (LR - 2 * eps ** 2 * Jh(gradpsi2) + LK) / (16 * sp.pi * G) - eps ** 2 * rho * psi
L2 = sp.expand(Lfull).coeff(eps, 2)
L1 = sp.expand(Lfull).coeff(eps, 1)


def var_deriv(L, f):
    """Euler-Lagrange expression dL/df - d_i dL/df_i + d_ij dL/df_ij."""
    out = sp.diff(L, f)
    for v in (x, y, z):
        out -= sp.diff(sp.diff(L, sp.diff(f, v)), v)
    for i, v in enumerate((x, y, z)):
        for w in (x, y, z)[i:]:
            out += sp.diff(sp.diff(L, sp.diff(f, v, w)), v, w)
    return sp.expand(out)


EL_psi = var_deriv(L2, psi)
EL_phi = var_deriv(L2, phi)
lap = lambda f: sum(sp.diff(f, v, 2) for v in (x, y, z))
Jp = sp.Subs(sp.Derivative(Jh(sp.Symbol("_Y")), sp.Symbol("_Y")), sp.Symbol("_Y"), gradpsi2).doit()
sgn = -1 if MUTATE else 1  # mutation: f = 1 - J'
target_psi = lap(phi) + sum(sp.diff(sgn * Jp * sp.diff(psi, v), v) for v in (x, y, z)) + mu ** 2 * psi \
    - 4 * sp.pi * G * rho
cpsi = sp.symbols("c_psi")
# normalise by the rho coefficient
c_val = sp.simplify(EL_psi.coeff(rho) / target_psi.coeff(rho))
r_psi = sp.simplify(sp.expand(EL_psi - c_val * target_psi))
target_phi = lap(psi) - lap(phi)
c_phi = sp.simplify(sp.expand(EL_phi).coeff(sp.diff(psi, x, 2)) / target_phi.coeff(sp.diff(psi, x, 2)))
r_phi = sp.simplify(sp.expand(EL_phi - c_phi * target_phi))
res["K1"] = {"A_minus_dlnN": [str(a) for a in A_res], "A_eq3_second_form": [str(a) for a in A_alt],
             "Y_over_eps2_minus_gradpsi2": str(Y_res), "O_eps1_lagrangian": str(sp.simplify(L1)),
             "EL_psi_norm": str(c_val), "EL_psi_residual": str(r_psi), "EL_phi_norm": str(c_phi),
             "EL_phi_residual": str(r_phi),
             "statement": "div[(1+J'(Y)) grad psi] + mu^2 psi = 4 pi G rho, phi = psi, Y = |grad psi|^2 (BS24 Eqs. 24, 35)"}
ok1 = all(a == 0 for a in A_res) and all(a == 0 for a in A_alt) and Y_res == 0 and r_psi == 0 and r_phi == 0
check("K1", ok1, f"A_i-d_i lnN={[str(a) for a in A_res[:3]]} Y_res={Y_res} EL_psi_res={r_psi} EL_phi_res={r_phi} "
                 f"norm_psi={c_val} norm_phi={c_phi}",
      "all residuals 0 (AQUAL type, f = 1 + J', phi = psi)")

# =============================================================== K2 mu = x/(1+x) exactly
a0, Lam, s = sp.symbols("a0 Lambda s", positive=True)
Ys = sp.symbols("Y", positive=True)
yv = sp.sqrt(Ys) / a0
Jx = Lam - 2 * a0 ** 2 * (yv - sp.log(1 + yv))
f_Jx = sp.simplify(1 + sp.diff(Jx, Ys))
r2a = sp.simplify(f_Jx - yv / (1 + yv))
Jx_s = Jx.subs(Ys, s ** 2)
ser = sp.series(Jx_s, s, 0, 4).removeO()
eq37 = Lam - s ** 2 + sp.Rational(2, 3) / a0 * s ** 3
r2b = sp.simplify(ser - eq37)
lim_large = sp.limit(Jx_s / s, s, sp.oo)
res["K2"] = {"J_x": str(Jx), "f_minus_x_over_1px": str(r2a), "series_minus_eq37": str(r2b),
             "lim_J_over_sqrtY": str(lim_large),
             "reading": "x/(1+x)-exact needs J ~ -2 a0 sqrt(Y) at large Y: outside BS24 Eq.40 / BS25 Eq.4a"}
check("K2", r2a == 0 and r2b == 0, f"f-x/(1+x)={r2a} series-Eq37={r2b} lim J/sqrtY={lim_large}",
      "residuals 0; lim != 0 => outside BS's admissible class")

# =============================================================== K3 clock term = Legendre dual of J
g_, u_, K_, xi = sp.symbols("g u K xi", positive=True)
W = a0 ** 2 / K_ * (-u_ / a0 - sp.log(1 - u_ / a0))
KWp = sp.simplify(K_ * sp.diff(W, u_))  # = u a0/(a0-u)
u_star = sp.solve(sp.Eq(KWp, xi * g_), u_)[0]
L_eff = -g_ ** 2 / (2 * K_) + xi * g_ * u_star / K_ - W.subs(u_, u_star)
L_BS = -(g_ ** 2 + Jx.subs(Ys, g_ ** 2) - Lam) / (2 * K_)
xi_test = 2 if MUTATE else 1
r3 = sp.simplify(sp.expand_log(sp.simplify(L_eff.subs(xi, xi_test) - L_BS), force=True))
gN_xi = g_ - xi * u_star  # from div[(g - xi u) ghat] = K rho
dev2 = float((gN_xi - g_ ** 2 / (g_ + a0)).subs({xi: 2, g_: a0 / 3}).subs(a0, 1))
mu_xi = sp.simplify(1 - xi * u_star / g_)
res["K3"] = {"u_star": str(u_star), "L_eff_minus_L_BS_at_xi": {"xi": xi_test, "residual": str(r3)},
             "gN_minus_law_at_xi2_g_a0over3_in_a0": dev2, "mu_of_xi": str(mu_xi),
             "reading": "in the Khronon, the clock coefficient is absorbed in J: xi = 1 <=> J = J_x given W"}
check("K3", r3 == 0 and abs(dev2 - (-0.55)) < 1e-12,
      f"L_eff-L_BS(xi={xi_test})={r3} dev(xi=2,g=a0/3)={dev2:.12f} a0", "residual 0; A33 K5 value -0.55 a0")

# =============================================================== K4 curl structure off symmetry
X3 = sp.Matrix([x, y, z])
m1, m2 = 1.0, 0.6
x1, x2 = sp.Matrix([0, 0, 0]), sp.Matrix([1.0, 0, 0])
Phi = -m1 / sp.sqrt(((X3 - x1).T * (X3 - x1))[0]) - m2 / sp.sqrt(((X3 - x2).T * (X3 - x2))[0])
gradPhi = sp.Matrix([sp.diff(Phi, v) for v in (x, y, z)])
gmag = sp.sqrt((gradPhi.T * gradPhi)[0])
a0n = 1.0
muf = (gmag / a0n) / (1 + gmag / a0n)
Pst = (1 - muf) * gradPhi  # K P*, K = 1
curl = sp.Matrix([sp.diff(Pst[2], y) - sp.diff(Pst[1], z), sp.diff(Pst[0], z) - sp.diff(Pst[2], x),
                  sp.diff(Pst[1], x) - sp.diff(Pst[0], y)])
pt = {x: 0.4, y: 0.7, z: 0.3}
curl_n = np.array([float(cc.subs(pt)) for cc in curl])
jac = np.array([[float(sp.diff(Pst[i], v).subs(pt)) for v in (x, y, z)] for i in range(3)])
curl_ratio = float(np.linalg.norm(curl_n) / np.linalg.norm(jac))
curl_gradPhi = float(max(abs(float(cc.subs(pt))) for cc in
                         [sp.diff(gradPhi[2], y) - sp.diff(gradPhi[1], z)]))
e2 = json.load(open(os.path.join(ROOT, "doors_push_2026_10_22/E2_field_equation/e2_field_equation_results.json")))
tf = e2["K1c"]["transverse_fraction"]
res["K4"] = {"test_point": [0.4, 0.7, 0.3], "curl_KPstar": curl_n.tolist(), "curl_over_grad": curl_ratio,
             "curl_gradPhi": curl_gradPhi, "E2_transverse_fraction_curl_free_error": tf,
             "khronon_minus_AQUAL": 0,
             "reading": "the khronometric constraint acts on A_i = d_i ln N (curl-free in AQUAL too); the auxiliary "
                        "P* is unconstrained, so the law is AQUAL off symmetry"}
check("K4", curl_ratio > 1e-3, f"|curl P*|/|grad P*|={curl_ratio:.4e} (curl grad Phi={curl_gradPhi:.1e}); "
                               f"E2 curl-free error={tf:.4f}", "> 1e-3")

# =============================================================== K5 pure Khronon cannot screen
c1 = json.load(open(os.path.join(ROOT, "covariant_push_2026_10_22/C1_aest_embedding/c1_aest_embedding_results.json")))
pl = {k: v["ratio_to_bound"] for k, v in c1["K6"].items()}
ok5a = all(v > 1 for v in pl.values())
q2 = {}
for k, v in e2["R1"].items():
    q2[k] = min(v["over_Hees"])
q2_min = {fo: min(v for k, v in q2.items() if k.startswith(fo + "|")) for fo in ("canonical", "alt")}
ok5b = all(v > 1 for v in q2.values())
r_q2 = 7000 * AU
mu2r2 = (r_q2 / (100 * KPC)) ** 2
ok5c = mu2r2 < 1e-6
res["K5"] = {"planet_ratio_to_bound_Jx": pl, "AQUAL_Q2_over_Hees_min_by_row": q2, "Q2_min_by_footing": q2_min,
             "mu2r2_at_7000AU_mu_inv_100kpc": mu2r2}
check("K5", ok5a and ok5b and ok5c,
      f"planets(J_x) min={min(pl.values()):.3e}; Q2/Hees min can={q2_min['canonical']:.3f} "
      f"alt={q2_min['alt']:.3f} (all y_t rows); mu^2 r^2={mu2r2:.2e}",
      "all >1, all >1, <1e-6 => no pure-Khronon J screens (stiffness needed)")

# =============================================================== K6 covariant Khronon + P
P1, P2, P3 = [sp.Function(f"P{i}")(x, y, z) for i in (1, 2, 3)]
P_lo = [0, P1, P2, P3]  # P_0 = N^i P_i = 0 (static, zero shift); n^mu P_mu = 0
P_up = [sum(ginv[a, b] * P_lo[b] for b in range(4)) for a in range(4)]
PA = sp.simplify(sum(P_up[m] * A_lo[m] for m in range(4)))
PA_target = sum(ginv[i, i] * P_lo[i] * sp.diff(sp.log(Nl), X[i]) for i in (1, 2, 3))
r6 = sp.simplify(PA - PA_target)
nP = sp.simplify(sum(n_up[m] * P_lo[m] for m in range(4)))
ratio_L = {f"{L}pc": (L * PC / AU) ** 2 for L in (24, 90)}
res["K6"] = {"PmuAmu_minus_PidilnN": str(r6), "n_dot_P": str(nP), "Lstar_over_1AU_squared": ratio_L}
check("K6", r6 == 0 and nP == 0 and all(v > 1e6 for v in ratio_L.values()),
      f"P.A-P^i d_i lnN={r6} n.P={nP} (L*/AU)^2={ratio_L['24pc']:.3e}/{ratio_L['90pc']:.3e}",
      "residuals 0; >1e6 => P independent field (stiffness non-perturbative)")

# =============================================================== K7 FRW cosmology of BS24
tt = sp.symbols("t", real=True)
Nt = sp.Function("N")(tt)
at = sp.Function("a")(tt)
tau = sp.Function("tau")(tt)
Qs, I0, a_s = sp.symbols("Q I_0 a", positive=True)
Kfun = mu ** 2 * (Qs - 1) ** 2
KQ = sp.diff(Kfun, Qs)
Qt = sp.diff(tau, tt) / Nt
LKt = Nt * at ** 3 * 2 * Kfun.subs(Qs, Qt) / (16 * sp.pi * G)
mom = sp.simplify(sp.diff(LKt, sp.diff(tau, tt)))  # conserved: d/dt mom = 0 (tau cyclic)
r47 = sp.simplify(mom - at ** 3 * KQ.subs(Qs, Qt) / (8 * sp.pi * G))
Qbar = sp.solve(sp.Eq(KQ, I0 / a_s ** 3), Qs)[0]
r53 = sp.simplify(Qbar - (1 + I0 / (2 * mu ** 2 * a_s ** 3)))
rho_K = sp.simplify((-sp.diff(LKt, Nt) / at ** 3).subs(Nt, 1))  # rho = -(1/a^3) dL/dN at N = 1
rho_K = sp.simplify(rho_K.subs(sp.diff(tau, tt), Qs))
p_K = sp.simplify((LKt / (Nt * at ** 3)).subs(Nt, 1).subs(sp.diff(tau, tt), Qs))
rho_Ka = sp.simplify(rho_K.subs(Qs, Qbar).subs(at, a_s))
w0t = I0 / (4 * mu ** 2)
r17 = sp.simplify(rho_Ka - I0 / (8 * sp.pi * G * a_s ** 3) * (1 + w0t / a_s ** 3))
w = sp.simplify((p_K / rho_K).subs(Qs, Qbar))
r57 = sp.simplify(w - w0t / (w0t + a_s ** 3))
# Y on FRW: comoving khronon is geodesic
gF = sp.diag(-Nt ** 2, at ** 2, at ** 2, at ** 2)
XF = (tt, x, y, z)
giF = gF.inv()
GamF = [[[sp.Rational(1, 2) * sum(giF[a, d] * (sp.diff(gF[d, b], XF[cc]) + sp.diff(gF[d, cc], XF[b])
                                              - sp.diff(gF[b, cc], XF[d])) for d in range(4))
          for cc in range(4)] for b in range(4)] for a in range(4)]
nF = [-Nt, 0, 0, 0]
nFu = [sum(giF[a, b] * nF[b] for b in range(4)) for a in range(4)]
AF = [sp.simplify(sum(nFu[nu] * (sp.diff(nF[m], XF[nu]) - sum(GamF[l][nu][m] * nF[l] for l in range(4)))
                      for nu in range(4))) for m in range(4)]
YF = sp.simplify(sum(giF[a, b] * AF[a] * AF[b] for a in range(4) for b in range(4)))
res["K7"] = {"eq47_residual": str(r47), "eq53_residual": str(r53), "BS25_eq17_residual": str(r17),
             "eq57_residual": str(r57), "Y_on_FRW": str(YF), "rho_K(Q)": str(rho_K), "p_K(Q)": str(p_K),
             "abundance": "I0 is the integration constant of the tau shift charge: Omega_K FITTED (initial condition)"}
check("K7", r47 == 0 and r53 == 0 and r17 == 0 and r57 == 0 and YF == 0,
      f"eq47={r47} eq53={r53} eq17={r17} eq57={r57} Y_FRW={YF}", "all 0")


# =============================================================== K8 closure identity
def h_can(yN):
    return 2 * yN / (math.sqrt(yN * yN + 4 * yN) + yN)  # y_N (nu - 1), D7 kernel


def hp_can(yN):
    r = math.sqrt(yN * yN + 4 * yN)
    return ((yN + 2) / r - 1) / 2


def D(yN, yt):
    return h_can(yN) / (1 + (yN / yt) ** 2)


def Dp(yN, yt):
    q = 1 + (yN / yt) ** 2
    return hp_can(yN) / q - h_can(yN) * 2 * yN / yt ** 2 / q ** 2


def F_rec(yt):  # record's closure integral, int D dy_N (D7 F)
    return quad(lambda th: D(yt * math.tan(th), yt) * yt / math.cos(th) ** 2,
                0, math.pi / 2, limit=400, epsabs=1e-13, epsrel=1e-12)[0]


def F_dy(yt):  # int D dy = int D (1 + D') dy_N
    return quad(lambda th: D(yt * math.tan(th), yt) * (1 + Dp(yt * math.tan(th), yt)) * yt / math.cos(th) ** 2,
                0, math.pi / 2, limit=400, epsabs=1e-13, epsrel=1e-12)[0]


ident = {}
mono_min = {}
for yt in (46.0148, 66.3803, 77.876, 140.0):
    a_, b_ = F_rec(yt), F_dy(yt)
    ident[str(yt)] = {"int_D_dyN": a_, "int_D_dy": b_, "rel": abs(a_ - b_) / a_}
    grid = np.logspace(-6, 7, 4000)
    mono_min[str(yt)] = float(min(1 + Dp(v, yt) for v in grid))
ok8a = all(v["rel"] < 1e-6 for v in ident.values())
ok8b = all(v > 0 for v in mono_min.values())
factor = 1.0 if MUTATE else 2.0
yt_new, yt_rec = {}, {}
for lab, Nval in (("canonical_quotedLambda", LAMBDA * c ** 4 / A0["canonical"] ** 2),
                  ("alt_quotedLambda", LAMBDA * c ** 4 / A0["alt"] ** 2), ("kappa_half_32pi", 32 * math.pi)):
    yt_rec[lab] = brentq(lambda Y: F_rec(Y) - Nval, 1e-3, 1e5, xtol=1e-12)
    yt_new[lab] = brentq(lambda Y: factor * F_dy(Y) - Nval, 1e-3, 1e5, xtol=1e-12)
# mutation consistency: without the factor 2 the Khronon closure would be the record's; the frozen pass line
# compares the identity, and the mutation flags (via K8c) that the record's y_t is then reproduced
same_as_record = all(abs(yt_new[k] - yt_rec[k]) / yt_rec[k] < 1e-6 for k in yt_rec)
res["K8"] = {"premise": "J(infinity) = 0 (BS25 Eq. 4a, via WebFetch); J(0) = Lambda (BS25 Eq. 4b)",
             "identity": "Lambda c^4/a0^2 = 2 int_0^inf (y - y_N) dy = 2 F(y_t)", "int_checks": ident,
             "min_dy_dyN": mono_min, "factor_used": factor, "yt_khronon": yt_new, "yt_record": yt_rec,
             "khronon_equals_record": same_as_record}
check("K8", ok8a and ok8b and not same_as_record,
      f"max rel |intDdy-intDdyN|={max(v['rel'] for v in ident.values()):.2e} min dy/dyN="
      f"{min(mono_min.values()):.4f} y_t(khronon) can={yt_new['canonical_quotedLambda']:.4f} "
      f"alt={yt_new['alt_quotedLambda']:.4f} 32pi={yt_new['kappa_half_32pi']:.4f} "
      f"(record {yt_rec['canonical_quotedLambda']:.4f}/{yt_rec['alt_quotedLambda']:.4f}/"
      f"{yt_rec['kappa_half_32pi']:.4f})",
      "rel<1e-6; monotone; Khronon closure (factor 2) differs from record's")

# =============================================================== summary
npass = sum(ch["pass"] for ch in checks)
res.update(checks=checks, n_pass=npass, n_checks=len(checks), runtime_s=round(time.time() - T0, 2),
           verdict="EMBEDS WITH EXTRA TERM" if (not MUTATE and npass == len(checks)) else "see checks")
log(f"C4_KHRONON_PARENT COMPLETE: {npass}/{len(checks)} checks PASS.")
with open(OUT, "w") as fh:
    fh.write("\n".join(lines) + "\n")
with open(JSON, "w") as fh:
    json.dump(res, fh, indent=1, default=str)
sys.exit(0 if npass == len(checks) else 1)
