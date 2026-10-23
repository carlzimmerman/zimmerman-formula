#!/usr/bin/env python3
"""Z1_successor_design: sympy and small-numeric checks K1-K10 (FROZEN_CRITERIA.md section 2).

Run:  OMP_NUM_THREADS=1 nice -n 15 python3 z1_successor_design.py
      Z1_MUTATE=1 OMP_NUM_THREADS=1 nice -n 15 python3 z1_successor_design.py

Writes z1_successor_design.out / z1_successor_design_results.json (or *_MUTATE.* in MUTATE mode).
Deterministic, no network, no data files. kappa = 1/2 FITTED; footings never pooled.
"""
import json
import os
import sys

import sympy as sp

MUTATE = os.environ.get("Z1_MUTATE", "") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
TAG = "_MUTATE" if MUTATE else ""
OUT = os.path.join(HERE, f"z1_successor_design{TAG}.out")
JSN = os.path.join(HERE, f"z1_successor_design_results{TAG}.json")

lines = []
res = {"mutate": MUTATE, "checks": {}, "numbers": {}}


def say(s=""):
    print(s)
    lines.append(s)


def check(cid, ok, value, threshold):
    res["checks"][cid] = {"pass": bool(ok), "value": str(value), "threshold": str(threshold)}
    say(f"{cid} {'PASS' if ok else 'FAIL'} {value} {threshold}")
    return ok


def _factor_sqrts(e):
    return e.replace(lambda q: q.is_Pow and q.exp == sp.Rational(1, 2),
                     lambda q: sp.sqrt(sp.factor(q.base)))


def is_zero(expr):
    """Exact zero test: simplify; if that fails, factor the radicands of square roots (positive symbols) and retry."""
    if sp.simplify(sp.expand(expr)) == 0:
        return True
    e2 = sp.simplify(_factor_sqrts(sp.together(expr)))
    if e2 == 0:
        return True
    return sp.simplify(sp.powdenest(e2, force=True)) == 0


# ---------------------------------------------------------------------------------------------
# Physical constants and footings (FRAMEWORK-NATIVE; kappa = 1/2 FITTED)
G_SI = 6.67430e-11
MSUN = 1.98847e30
KPC = 3.085677581e19
MPC = 3.085677581e22
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
H0_NATIVE = {"lo": 67.2, "mid": 67.9, "hi": 68.6}   # C2 native range, km/s/Mpc
OMEGA_M_NATIVE = 0.2976                              # CFG886 native (F3 background B)
F_S = 5.364                                          # record supply ratio Omega_c/Omega_b (LCDM-PROCESSED)
say("Z1_successor_design checks" + ("  [MUTATE]" if MUTATE else ""))
say("kappa = 1/2 FITTED; footings canonical 9.3603e-11 / alt 1.1312e-10 m/s^2, never pooled")
say("")

t = sp.symbols("t", real=True)
G, a0, sig, c = sp.symbols("G a_0 sigma c", positive=True)

# ---------------------------------------------------------------------------------------------
# K1: BLT non-relativistic Lagrangian (1D reduction; Pi_hat = +1 for xi > 0)
#   L = 1/2 xdot^2 + s xdot xidot + U(x) + xi U'(x) - W(sigma xi)/sigma
#   BLT (85): xddot - g = -W'(Pi);  BLT (86) without the sigma-gradient term: xiddot - W'(Pi) = xi g'(x)
x = sp.Function("x")(t)
xi = sp.Function("xi")(t)
U = sp.Function("U")
W = sp.Function("W")
s = sp.symbols("s")


def blt_EL(sv):
    L = sp.Rational(1, 2) * x.diff(t) ** 2 + sv * x.diff(t) * xi.diff(t) + U(x) + xi * U(x).diff(x) \
        - W(sig * xi) / sig
    ELx = sp.diff(L.diff(x.diff(t)), t) - L.diff(x)
    ELxi = sp.diff(L.diff(xi.diff(t)), t) - L.diff(xi)
    return L, ELx, ELxi


g_of_x = U(x).diff(x)
Wp = sp.Subs(sp.Derivative(W(sp.Symbol("P")), sp.Symbol("P")), sp.Symbol("P"), sig * xi).doit()


def blt_residuals(sv):
    L, ELx, ELxi = blt_EL(sv)
    sol = sp.solve([ELx, ELxi], [x.diff(t, 2), xi.diff(t, 2)], dict=True)
    if not sol:
        return None, None, L
    sol = sol[0]
    r85 = sp.simplify(sol[x.diff(t, 2)] - (g_of_x - Wp))
    r86 = sp.simplify(sol[xi.diff(t, 2)] - (Wp + xi * g_of_x.diff(x)))
    return r85, r86, L


matches = {}
for sv in (1, -1):
    r85, r86, _ = blt_residuals(sv)
    matches[sv] = (r85 is not None and is_zero(r85) and is_zero(r86))
blt_sign = [sv for sv in (1, -1) if matches[sv]]
used_sign = (-blt_sign[0] if (MUTATE and len(blt_sign) == 1) else (blt_sign[0] if blt_sign else None))
r85u, r86u, Lu = blt_residuals(used_sign if used_sign is not None else 1)
reproduces = (r85u is not None and is_zero(r85u) and is_zero(r86u))
H = sp.Matrix([[1, used_sign if used_sign is not None else 1], [used_sign if used_sign is not None else 1, 0]])
detH = H.det()
eigs = [float(e) for e in H.eigenvals().keys()]
res["numbers"]["K1"] = {"signs_reproducing_BLT_85_86": blt_sign, "sign_used": used_sign,
                        "kinetic_hessian_det": str(detH), "kinetic_hessian_eigs": sorted(eigs)}
check("K1", len(blt_sign) == 1 and reproduces and detH < 0,
      f"BLT(85,86) reproduced by s={blt_sign} (used s={used_sign}, residual0={reproduces}); det H={detH}, "
      f"eigs={sorted(round(e, 4) for e in eigs)}",
      "exactly one sign reproduces; det<0")

# ---------------------------------------------------------------------------------------------
# K2: dielectric matching W'(Pi) = g, chi = -4 pi G Pi / g = -1 + g/a0 + O(g^2)
gg = sp.symbols("g", positive=True)
W2, W3, P = sp.symbols("W_2 W_3 Pi", positive=True)
# invert W2 P + W3 P^2/2 = g as a series in g
c1, c2 = sp.symbols("c1 c2")
Pser = c1 * gg + c2 * gg ** 2
eq = sp.expand(W2 * Pser + W3 * Pser ** 2 / 2 - gg)
sol = sp.solve([eq.coeff(gg, 1), eq.coeff(gg, 2)], [c1, c2], dict=True)[0]
chi = sp.expand(sp.series(-4 * sp.pi * G * Pser.subs(sol) / gg, gg, 0, 2).removeO())
match = sp.solve([sp.Eq(chi.coeff(gg, 0), -1), sp.Eq(chi.coeff(gg, 1), 1 / a0)], [W2, W3], dict=True)
ok2 = (len(match) == 1 and is_zero(match[0][W2] - 4 * sp.pi * G)
       and is_zero(match[0][W3] - 32 * sp.pi ** 2 * G ** 2 / a0))
res["numbers"]["K2"] = {"W2": str(match[0][W2]), "W3": str(match[0][W3])}
# BLT Lambda-a0 relation (their Eq. 105, PROVISIONAL): Lambda = 3 alpha^2 (2 pi a0 / c^2)^2  ->  kappa = Z/(4 pi alpha)
alpha, Lam, kap = sp.symbols("alpha Lambda kappa", positive=True)
a0_blt = c ** 2 * sp.sqrt(Lam / 3) / (2 * sp.pi * alpha)
a0_fw = kap * c ** 2 * sp.sqrt(Lam / (8 * sp.pi))       # a0 = kappa c sqrt(G rho_Lambda), rho_Lambda = Lambda c^2/(8 pi G)
kap_of_alpha = sp.solve(sp.Eq(a0_blt, a0_fw), kap)[0]
Z = 2 * sp.sqrt(8 * sp.pi / 3)
okZ = is_zero(kap_of_alpha - Z / (4 * sp.pi * alpha))
res["numbers"]["K2"].update({
    "kappa_of_alpha": str(sp.simplify(kap_of_alpha)),
    "kappa_at_alpha_0.8": float(kap_of_alpha.subs(alpha, sp.Rational(4, 5))),
    "alpha_for_kappa_half": float(sp.solve(sp.Eq(kap_of_alpha, sp.Rational(1, 2)), alpha)[0]),
    "Z_over_4pi": float(Z / (4 * sp.pi))})
check("K2", ok2 and okZ,
      f"W2={match[0][W2]}, W3={match[0][W3]}; kappa=Z/(4 pi alpha): kappa(0.8)="
      f"{res['numbers']['K2']['kappa_at_alpha_0.8']:.4f}, alpha(kappa=1/2)={res['numbers']['K2']['alpha_for_kappa_half']:.4f}",
      "W2=4 pi G and W3=32 pi^2 G^2/a0 unique")

# ---------------------------------------------------------------------------------------------
# K3: BLT linear sector
#  (a) field theory, 1D longitudinal, uniform sigma_bar, delta sigma = 0:
#      Poisson (BLT 90): dg/dX = -4 pi G (rho_b + sigma - d(sigma xi)/dX)  ->  g = 4 pi G sigma_bar xi (+0)
#      anchor: xddot = g - W2 sigma_bar xi  = 0  iff W2 = 4 pi G ; dipole: xiddot = W2 sigma_bar xi (growth rate^2 = 4 pi G sigma_bar)
sb = sp.symbols("sigma_bar", positive=True)
Xs = sp.symbols("X", real=True)
xiX = sp.Function("xiX")(Xs)
gX = 4 * sp.pi * G * sb * xiX
poisson_res = sp.simplify(gX.diff(Xs) - (-4 * sp.pi * G * (-(sb * xiX).diff(Xs))))
anchor = sp.simplify(gX - W2 * sb * xiX)
anchor_zero_iff = sp.solve(sp.Eq(anchor, 0), W2)
okA = is_zero(poisson_res) and len(anchor_zero_iff) == 1 and is_zero(anchor_zero_iff[0] - 4 * sp.pi * G)
#  (b) y = x + xi: L(y, xi) = 1/2 ydot^2 - 1/2 xidot^2 + U(y) - W/sigma + O(xi^2)
y = sp.Function("y")(t)
eps = sp.symbols("epsilon")
# generic analytic potential: quartic with symbolic coefficients (the first-order identity holds term by term)
ucoef = sp.symbols("u0:5")
qv = sp.symbols("q")
U2poly = sum(ucoef[n] * qv ** n for n in range(5))


def U2(arg):
    return U2poly.subs(qv, arg)


Ltest = (sp.Rational(1, 2) * x.diff(t) ** 2 + 1 * x.diff(t) * xi.diff(t)
         + U2(x) + xi * sp.diff(U2poly, qv).subs(qv, x))
# substitute x = y - eps*xi, xi -> eps*xi and expand to first order in eps
Lsub = Ltest.subs(xi, eps * xi).doit()
Lsub = Lsub.subs(x, y - eps * xi).doit()
Lexp = sp.series(Lsub, eps, 0, 2).removeO()
target = sp.Rational(1, 2) * y.diff(t) ** 2 - eps ** 2 * sp.Rational(1, 2) * xi.diff(t) ** 2 + U2(y)
# compare through first order in eps (the -xidot^2/2 term is O(eps^2) in this bookkeeping; check it separately)
diff_first = sp.simplify(sp.expand(Lexp - (sp.Rational(1, 2) * y.diff(t) ** 2 + U2(y))))
kin = sp.expand(sp.Rational(1, 2) * (y.diff(t) - xi.diff(t)) ** 2 + (y.diff(t) - xi.diff(t)) * xi.diff(t)
                - (sp.Rational(1, 2) * y.diff(t) ** 2 - sp.Rational(1, 2) * xi.diff(t) ** 2))
okB = is_zero(diff_first) and is_zero(kin)
#  (c) cubic = quadratic at Pi* = 2 W2/W3 ; own field 4 pi G Pi* = a0
Pstar = sp.solve(sp.Eq(W2 * P, W3 * P ** 2 / 2), P)
Pstar = [p for p in Pstar if p != 0][0]
field_star = sp.simplify((4 * sp.pi * G * Pstar).subs({W2: 4 * sp.pi * G, W3: 32 * sp.pi ** 2 * G ** 2 / a0}))
okC = is_zero(field_star - a0)
#  (d) reported: anchor acceleration when the cold field is x*a0 (linear Poisson g = 4 pi G Pi):  xddot = -x g
xx = sp.symbols("x_f", positive=True)
Pi_x = xx * a0 / (4 * sp.pi * G)
Wprime = (W2 * P + W3 * P ** 2 / 2).subs({W2: 4 * sp.pi * G, W3: 32 * sp.pi ** 2 * G ** 2 / a0}).subs(P, Pi_x)
anchor_acc = sp.simplify(4 * sp.pi * G * Pi_x - Wprime)          # = -x^2 a0
ratio = sp.simplify(-anchor_acc / (xx * a0))                       # |xddot| / g = x
res["numbers"]["K3"] = {"anchor_rest_iff_W2": str(anchor_zero_iff), "cubic_threshold_field": str(field_star),
                        "anchor_acc_over_g": str(ratio),
                        "anchor_acc_over_g_at_x_11_14_record": [11, 14]}
check("K3", okA and okB and okC,
      f"(a) anchor at rest iff W2={anchor_zero_iff[0]}; (b) y=x+xi geodesic, xi kinetic -1/2 xidot^2: {okB}; "
      f"(c) cubic=quadratic at 4 pi G Pi={field_star}; (d) |anchor acc|/g = {ratio} (=11-14 at z~1100, X0 MAP L22)",
      "residuals 0; threshold a0")

# ---------------------------------------------------------------------------------------------
# K4: static owner limit = v3s AQUAL with mu = x/(1+x)
#   leaf functional density: (a0^2/(4 pi G)) F(|grad psi|/a0) + rho_b psi,  F(y) = y^2/2 - y + ln(1+y), F'(y) = y mu(y)
yv = sp.symbols("y", positive=True)
F = yv ** 2 / 2 - yv + sp.log(1 + yv)
mu = yv / (1 + yv)
okF = is_zero(sp.diff(F, yv) - yv * mu)
convex = sp.simplify(sp.diff(F, yv, 2))                          # (y^2 + 2y)/(1+y)^2 > 0
okConv = sp.simplify(convex - (yv ** 2 + 2 * yv) / (1 + yv) ** 2) == 0
# planar: L = (a0^2/(4 pi G)) F(psi'/a0) + rho psi ; EL: d/dz[ mu(psi'/a0) psi' ] = 4 pi G rho
z = sp.symbols("z", real=True)
psi = sp.Function("psi")(z)
rho = sp.Function("rho")(z)
Fz = F.subs(yv, psi.diff(z) / a0)
Lz = a0 ** 2 / (4 * sp.pi * G) * Fz + rho * psi
ELz = sp.diff(Lz.diff(psi.diff(z)), z) - Lz.diff(psi)
aqual_planar = sp.diff(mu.subs(yv, psi.diff(z) / a0) * psi.diff(z), z) - 4 * sp.pi * G * rho
okP = is_zero(sp.simplify(ELz * 4 * sp.pi * G - aqual_planar))
# spherical: first integral mu(g/a0) g = G M(r)/r^2 = gN  ->  a0-line gN = g^2/(g + a0)
gS, gN = sp.symbols("g_S g_N", positive=True)
first_integral = mu.subs(yv, gS / a0) * gS - gN
a0line = gS ** 2 / (gS + a0) - gN
okS = is_zero(first_integral - a0line)
# muK term of BS24 Eq. 35 removed: nabla.(mu grad psi) + muK^2 psi = 4 pi G rho  ->  at muK = 0 identical
muK = sp.symbols("mu_K", nonnegative=True)
okM = is_zero((aqual_planar + muK ** 2 * psi).subs(muK, 0) - aqual_planar)
res["numbers"]["K4"] = {"F": str(F), "F_second_derivative": str(convex)}
check("K4", okF and okConv and okP and okS and okM,
      f"F'(y)=y mu(y): {okF}; F''={convex}>0: {okConv}; planar EL = AQUAL: {okP}; spherical = a0-line: {okS}; "
      f"BS24 Eq.35 at mu_K=0 = AQUAL: {okM}",
      "all residuals 0")

# ---------------------------------------------------------------------------------------------
# K5: capacity split.  Point-mass owner, exact simple-mu law: M_ph(r) = M_b (nu - 1), nu = 1/2 + sqrt(1/4 + a0/gN)
Mb, r, fs, Ms, Mown = sp.symbols("M_b r f_s M_s M_own", positive=True)
gNr = G * Mb / r ** 2
nu = sp.Rational(1, 2) + sp.sqrt(sp.Rational(1, 4) + a0 / gNr)
Mph = Mb * (nu - 1)
# (a) supply >= demand inside r: total = M_b + M_ph  ->  g = G(M_b+M_ph)/r^2 obeys the a0-line
g_tot = G * (Mb + Mph) / r ** 2
okLaw = is_zero(sp.simplify(g_tot ** 2 / (g_tot + a0) - gNr))
# (b) exact supply radius: M_ph(r_s) = f_s M_b  ->  r_s = r_M sqrt(f_s (f_s + 1)),  r_M = sqrt(G M_b / a0)
rM = sp.sqrt(G * Mb / a0)
rs_exact = rM * sp.sqrt(fs * (fs + 1))
okRs = is_zero(sp.simplify(Mph.subs(r, rs_exact) - fs * Mb))
deep_ratio = sp.limit(rs_exact / (rM * fs), fs, sp.oo)            # -> 1 (deep limit r_s = f_s r_M)
# (c) excess free mass inside an owner of radius R: M_f = f_s M_b - M_ph(R) > 0  iff  R < r_s
Rown = sp.symbols("R", positive=True)
Mf = fs * Mb - Mph.subs(r, Rown)
okEx = is_zero(sp.simplify(Mf.subs(Rown, rs_exact)))              # zero exactly at R = r_s
dMf = sp.simplify(sp.diff(Mf, Rown))                               # < 0: excess falls with R
# (d) supply-rich total: law part + free excess = M_b + f_s M_b  ("debris replacing the law", X2/CFG949)
total_rich = sp.simplify(Mb + Mph.subs(r, Rown) + Mf)
okRich = is_zero(total_rich - (1 + fs) * Mb)
res["numbers"]["K5"] = {"r_s_over_r_M_exact": "sqrt(f_s (f_s+1))",
                        "r_s_over_r_M_at_record_f_s": float(sp.sqrt(F_S * (F_S + 1))),
                        "deep_limit_ratio": str(deep_ratio), "dMf_dR": str(dMf)}
check("K5", okLaw and okRs and deep_ratio == 1 and okEx and okRich,
      f"law where supplied: {okLaw}; r_s = r_M sqrt(f_s(f_s+1)) = {float(sp.sqrt(F_S*(F_S+1))):.4f} r_M at f_s={F_S}: {okRs}; "
      f"deep r_s/(f_s r_M) -> {deep_ratio}; excess zero at R=r_s: {okEx}; rich total = (1+f_s) M_b: {okRich}",
      "identities, residual 0")

# ---------------------------------------------------------------------------------------------
# K6: owned fall rate and no host term in the owner's law argument
gh, Mh = sp.symbols("g_host M_h", positive=True)
a_owned = sp.solve(sp.Eq((Mb + Mh) * sp.Symbol("a"), (Mb + Mh) * gh), sp.Symbol("a"))[0]
a_v3 = sp.solve(sp.Eq((Mb + Mh) * sp.Symbol("a"), Mb * gh), sp.Symbol("a"))[0]   # held medium weightless (U1 T3)
a_design = a_v3 if MUTATE else a_owned
okFall = is_zero(a_design - gh)
v3_lag = sp.simplify(a_v3 / gh)
# EFE: v3 (one foliation) law argument |g_int + g_e|; owner frame |g_int|. Deep point mass, x_int = 0.1, x_e = 1:
xi_int, xe = sp.Rational(1, 10), 1
# solve x mu(x) = b for internal Newtonian b with and without the external field (1-D, aligned), simple mu
xs = sp.symbols("xs", positive=True)
# direct: internal Newtonian field b chosen so the isolated owner gives x_int = 0.1
b_iso = float(xi_int ** 2 / (1 + xi_int))
# with an aligned external field: (x+xe) mu(x+xe) = b_iso + b_e, b_e = xe^2/(1+xe)
b_e = xe ** 2 / (1 + xe)
xtot = float(sp.nsolve(xs ** 2 / (1 + xs) - (b_iso + b_e), xs, 1.1))
x_int_efe = xtot - xe
res["numbers"]["K6"] = {"a_owned_over_g": str(sp.simplify(a_owned / gh)), "a_v3_over_g": str(v3_lag),
                        "efe_example": {"x_int_isolated_or_owned": float(xi_int), "x_e": xe,
                                        "x_int_one_foliation": x_int_efe,
                                        "suppression_dex": float(sp.log(x_int_efe / float(xi_int), 10))}}
check("K6", okFall,
      f"design fall rate a/g = {sp.simplify(a_design/gh)} (owned: 1; v3 control: {v3_lag}); "
      f"EFE example x_int 0.1 at x_e 1: one foliation {x_int_efe:.4f} ({res['numbers']['K6']['efe_example']['suppression_dex']:+.3f} dex), owner frame 0.1",
      "a = g exactly")

# ---------------------------------------------------------------------------------------------
# K7: release.  Held medium is at rest in the owner frame (single-stream khronon, v_tau = 0 in static equilibrium).
# Released at rest, its specific energy in the owner's capacity-truncated potential is E = -int_r^inf g dr < 0.
# Closed form for the exact simple-mu point-mass law inside r_s, Newtonian (M_b + f_s M_b) outside.
rr = sp.symbols("rr", positive=True)


def g_law(rv, Mbv, a0v):
    gn = G_SI * Mbv / rv ** 2
    return gn / 2 + (gn ** 2 / 4 + a0v * gn) ** 0.5


import math


def energy_released(rv, Mbv, a0v, fsv, nstep=4000):
    rMv = math.sqrt(G_SI * Mbv / a0v)
    rsv = rMv * math.sqrt(fsv * (fsv + 1))
    if rv >= rsv:
        return -G_SI * (1 + fsv) * Mbv / rv, rsv
    # Simpson in ln r from rv to rsv
    lo, hi = math.log(rv), math.log(rsv)
    n = nstep
    h = (hi - lo) / n
    acc = 0.0
    for i in range(n + 1):
        lr = lo + i * h
        rr_ = math.exp(lr)
        f = g_law(rr_, Mbv, a0v) * rr_
        w = 1 if i in (0, n) else (4 if i % 2 else 2)
        acc += w * f
    integral = acc * h / 3
    return -(integral + G_SI * (1 + fsv) * Mbv / rsv), rsv


grid_ok = True
k7 = {}
for foot, a0v in FOOT.items():
    for label, Mbv in (("dwarf_1e7", 1e7 * MSUN), ("MW_6e10", 6e10 * MSUN), ("cluster_1e14", 1e14 * MSUN)):
        Es = []
        for frac in (0.01, 0.1, 0.5, 0.9, 0.999):
            rMv = math.sqrt(G_SI * Mbv / a0v)
            rsv = rMv * math.sqrt(F_S * (F_S + 1))
            E, _ = energy_released(frac * rsv, Mbv, a0v, F_S)
            Es.append(E)
            grid_ok &= (E < 0)
        k7[f"{foot}|{label}"] = {"E_over_vflat2_at_r/r_s=0.01,0.1,0.5,0.9,0.999":
                                 [e / math.sqrt(G_SI * Mbv * a0v) for e in Es]}
# symbolic sign: g > 0 for every r>0 in the law  ->  integrand positive  ->  E < 0
g_sym = gNr / 2 + sp.sqrt(gNr ** 2 / 4 + a0 * gNr)
okSign = sp.ask(sp.Q.positive(g_sym), sp.Q.positive(G) & sp.Q.positive(Mb) & sp.Q.positive(r) & sp.Q.positive(a0))
res["numbers"]["K7"] = k7
check("K7", bool(okSign) and grid_ok,
      f"g>0 for all r (sympy ask: {okSign}); E<0 on 30 grid points (2 footings x 3 masses x 5 radii): {grid_ok}",
      "E < 0 everywhere inside the owner")

# ---------------------------------------------------------------------------------------------
# K8: linear kernel from the mimetic-dust action (NR limit).  L = -rho [ phidot + |phi'|^2/2 + Phi ]  (rho = multiplier)
#     EL(rho): Hamilton-Jacobi (geodesic); EL(phi): continuity.  Linearise about uniform rho_bar at rest with Poisson.
X1 = sp.symbols("X1", real=True)
phi = sp.Function("phi")(t, X1)
rh = sp.Function("rho")(t, X1)
Phi = sp.Function("Phi")(t, X1)
Lm = -rh * (phi.diff(t) + phi.diff(X1) ** 2 / 2 + Phi)
EL_rho = Lm.diff(rh)                                                   # = -(HJ)
EL_phi = (sp.diff(Lm.diff(phi.diff(t)), t) + sp.diff(Lm.diff(phi.diff(X1)), X1))  # Euler operator for phi
hj = phi.diff(t) + phi.diff(X1) ** 2 / 2 + Phi
cont = rh.diff(t) + (rh * phi.diff(X1)).diff(X1)
okHJ = is_zero(EL_rho + hj)
okCont = is_zero(EL_phi + cont)
# linearise: rho = rb (1 + d), phi = small, velocity v = phi'; Poisson Phi'' = 4 pi G rb d
k, rb, A = sp.symbols("k rho_b A", positive=True)
dlt = sp.Function("d")(t)
# single Fourier mode: d = D(t) cos(kX), phi = F(t) cos(kX)/... ; from continuity: Ddot = k^2 F ; HJ: Fdot = -Phi_k ; Poisson: -k^2 Phi_k = 4 pi G rb D
Dt, Ft = sp.Function("D")(t), sp.Function("Fv")(t)
Phik = -4 * sp.pi * G * rb * Dt / k ** 2
eqs = [sp.Eq(Dt.diff(t), k ** 2 * Ft), sp.Eq(Ft.diff(t), -Phik)]
Dddot = sp.simplify(k ** 2 * eqs[1].rhs)                                # Dddot = k^2 Fdot
s_of_k = sp.simplify(Dddot / (4 * sp.pi * G * rb * Dt))
okS1 = is_zero(s_of_k - 1)
# EdS growing mode in a: delta'' + 3/(2a) delta' - 3/(2a^2) delta = 0  ->  delta = a
aa = sp.symbols("a", positive=True)
dd = sp.Function("dd")(aa)
eds = sp.Eq(dd.diff(aa, 2) + sp.Rational(3, 2) / aa * dd.diff(aa) - sp.Rational(3, 2) / aa ** 2 * dd, 0)
okEdS = is_zero(eds.lhs.subs(dd, aa).doit())
# v3 control: kernel s = mu^2/(k^2 + mu^2) -> 0 at mu_K = 0 for every k > 0 (M1, V3_FULL_PICTURE 4.2)
muk = sp.symbols("muk", nonnegative=True)
s_v3 = muk ** 2 / (k ** 2 + muk ** 2)
res["numbers"]["K8"] = {"s_of_k_design": str(s_of_k), "s_of_k_v3_at_muK_0": str(s_v3.subs(muk, 0)),
                        "EdS_growing_mode": "delta propto a"}
check("K8", okHJ and okCont and okS1 and okEdS,
      f"EL(rho)=HJ: {okHJ}; EL(phi)=continuity: {okCont}; s(k)={s_of_k} for all k; EdS delta propto a: {okEdS}; "
      f"v3 control s(mu_K=0)={s_v3.subs(muk, 0)}",
      "s(k)=1 exactly; delta propto a")

# ---------------------------------------------------------------------------------------------
# K9: retention map (deep limit): an owned system that held M_ph(M_orig) and then lost baryons to M_now keeps all its
# held+released medium (bound, K7).  Inside r, before tidal stripping, the dark mass is >= M_ph,orig(<r).
Mo, Mn = sp.symbols("M_orig M_now", positive=True)
g_obs_deep = sp.sqrt(G * Mo * a0) / r          # lower bound: concentration only raises M(<r)
g_iso_deep = sp.sqrt(G * Mn * a0) / r
dlog = sp.simplify(sp.log(g_obs_deep / g_iso_deep, 10) - sp.log(Mo / Mn, 10) / 2)
okRet = is_zero(sp.simplify(sp.expand_log(dlog, force=True)))
x1_iso = {  # X1_hosted_recount README L74-L80, column "iso AQUAL" (dex in g), canonical / alt
    "MW classical": (0.28, 0.24), "MW ultra-faints": (0.63, 0.59),
    "bright M31 dSphs": (0.25, 0.21), "M31 others": (0.64, 0.59), "LG field, isolated": (0.05, 0.02)}
inv = {}
for cls, (dc, da) in x1_iso.items():
    rc, ra = 10 ** (2 * dc), 10 ** (2 * da)
    inv[cls] = {"canonical": {"M_orig_over_M_now": rc, "implied_lost_fraction": 1 - 1 / rc},
                "alt": {"M_orig_over_M_now": ra, "implied_lost_fraction": 1 - 1 / ra}}
res["numbers"]["K9"] = {"identity": "Delta log10 g >= (1/2) log10(M_orig/M_now)", "inversion_of_X1_iso_AQUAL": inv}
check("K9", okRet,
      "Delta log g = 1/2 log(M_orig/M_now) (deep, lower bound); X1 iso-AQUAL residuals need lost fractions "
      + ", ".join(f"{k_}: {v['canonical']['implied_lost_fraction']:.2f}/{v['alt']['implied_lost_fraction']:.2f}"
                  for k_, v in inv.items()),
      "identity residual 0")

# ---------------------------------------------------------------------------------------------
# K10: supply-crossing baryon mass M_x: r_s(M_b) = R_own(M_b), with M_tot = (1 + f_s) M_b = (4 pi/3) Delta rho_ref R^3
#      M_x = [3 (1+f_s) / (4 pi Delta rho_ref)]^2 a0^3 / [f_s (f_s+1) G]^3
DR = sp.symbols("Delta_rho", positive=True)
Mx_sym = (3 * (1 + fs) / (4 * sp.pi * DR)) ** 2 * a0 ** 3 / (fs * (fs + 1) * G) ** 3
R_of_M = (3 * (1 + fs) * Mb / (4 * sp.pi * DR)) ** sp.Rational(1, 3)
okMx = is_zero(sp.simplify((rM * sp.sqrt(fs * (fs + 1))).subs(Mb, Mx_sym) ** 6 - R_of_M.subs(Mb, Mx_sym) ** 6))


def rho_crit(h0):
    H = h0 * 1e3 / MPC
    return 3 * H ** 2 / (8 * math.pi * G_SI)


k10 = {}
finite = True
for foot, a0v in FOOT.items():
    for hk, h0 in H0_NATIVE.items():
        rc = rho_crit(h0)
        for conv, Drho in (("200rho_c", 200 * rc), ("18pi2_rho_m_EdS", 18 * math.pi ** 2 * OMEGA_M_NATIVE * rc)):
            Mx = (3 * (1 + F_S) / (4 * math.pi * Drho)) ** 2 * a0v ** 3 / (F_S * (F_S + 1) * G_SI) ** 3
            finite &= (Mx > 0 and math.isfinite(Mx))
            k10[f"{foot}|H0={h0}|{conv}"] = Mx / MSUN
# tercile forecast (no lensing data): baryons = M_gas500 / (1 - 0.15)
terc = {"T1": 3.3e12, "T2": 1.17e13, "T3": 2.92e13}
tf = {}
for foot, a0v in FOOT.items():
    rc = rho_crit(H0_NATIVE["mid"])
    for tn, mg in terc.items():
        mb = mg / 0.85 * MSUN
        rMv = math.sqrt(G_SI * mb / a0v)
        rsv = rMv * math.sqrt(F_S * (F_S + 1))
        out = {"M_b_Msun": mb / MSUN, "r_M_kpc": rMv / KPC, "r_s_Mpc": rsv / MPC}
        for conv, Drho in (("200rho_c", 200 * rc), ("18pi2_rho_m_EdS", 18 * math.pi ** 2 * OMEGA_M_NATIVE * rc)):
            R = (3 * (1 + F_S) * mb / (4 * math.pi * Drho)) ** (1 / 3)
            # excess free fraction of the supply inside R (exact point-mass law)
            gn = G_SI * mb / R ** 2
            nuv = 0.5 + math.sqrt(0.25 + a0v / gn)
            excess = (F_S - (nuv - 1)) / F_S
            out[conv] = {"R_own_Mpc": R / MPC, "supply_rich": R < rsv, "free_excess_fraction_of_supply": excess,
                         "total_over_law_at_R": (1 + F_S) / nuv if R < rsv else 1.0}
        tf[f"{foot}|{tn}"] = out
# galaxy-scale supply radius for f_s (record ratio) -- owned supply is formation-dependent; reported only
gal = {}
for foot, a0v in FOOT.items():
    for label, mbv in (("dwarf_1e8", 1e8), ("MW_6e10", 6e10)):
        rMv = math.sqrt(G_SI * mbv * MSUN / a0v)
        gal[f"{foot}|{label}"] = {"r_M_kpc": rMv / KPC, "r_s_kpc_at_f_s_5.364": rMv * math.sqrt(F_S * (F_S + 1)) / KPC}
# reported diagnostics (no verdict weight; added before the first committed run):
# (a) design / law enclosed-mass ratio beyond r_s for the tercile medians (point-mass baryons, f_s = 5.364)
for foot, a0v in FOOT.items():
    for tn, mg in terc.items():
        mb = mg / 0.85 * MSUN
        rsv = math.sqrt(G_SI * mb / a0v) * math.sqrt(F_S * (F_S + 1))
        rat = {}
        for Rm in (0.5, 1.0, 2.0, 3.0):
            R = Rm * MPC
            gn = G_SI * mb / R ** 2
            nuv = 0.5 + math.sqrt(0.25 + a0v / gn)
            design = nuv if R <= rsv else (1 + F_S)
            rat[f"{Rm}Mpc"] = design / nuv
        tf[f"{foot}|{tn}"]["design_over_law_enclosed"] = rat
# (b) minimum owned supply ratio for which the law is untruncated out to R: f(f+1) = (R/r_M)^2
def f_req(R_over_rM):
    return 0.5 * (-1 + math.sqrt(1 + 4 * R_over_rM ** 2))
freq = {f"R/r_M={q}": f_req(q) for q in (5, 10, 20, 50, 100)}
# (c) Coma UDGs: field HI-rich UDG median gas fraction 0.81 (CFG948, LEDGER L704) -> predicted lower bound
coma_pred = 0.5 * math.log10(1 / (1 - 0.81))
# (d) crossing mass for a dwarf-like owned supply ratio f = 100 (200 rho_c, H0 67.9)
rc = rho_crit(H0_NATIVE["mid"])
mx100 = {foot: (3 * 101 / (4 * math.pi * 200 * rc)) ** 2 * a0v ** 3 / (100 * 101 * G_SI) ** 3 / MSUN
         for foot, a0v in FOOT.items()}
res["numbers"]["reported"] = {"f_req_for_untruncated_law": freq,
                              "coma_udg_predicted_dex_lower_bound_from_gas_fraction_0.81": coma_pred,
                              "coma_udg_observed_isolated_law_excess_dex_S1_L8": 0.33,
                              "M_x_Msun_at_owned_supply_f_100_200rho_c": mx100}
res["numbers"]["K10"] = {"M_x_Msun": k10, "tercile_forecast": tf, "galaxy_supply_radius": gal}
check("K10", okMx and finite,
      "M_x [Msun] canonical H0 67.9: 200rho_c {:.3g}, 18pi2rho_m {:.3g}; alt: {:.3g}, {:.3g}".format(
          k10["canonical|H0=67.9|200rho_c"], k10["canonical|H0=67.9|18pi2_rho_m_EdS"],
          k10["alt|H0=67.9|200rho_c"], k10["alt|H0=67.9|18pi2_rho_m_EdS"]),
      "closed form residual 0; finite, positive; footings separate")

# ---------------------------------------------------------------------------------------------
say("")
say("Tercile forecast (no lensing data; X2 catalogue gas medians / 0.85; f_s = 5.364 record input):")
for key, v in tf.items():
    say(f"  {key}: M_b {v['M_b_Msun']:.3g} Msun, r_M {v['r_M_kpc']:.0f} kpc, r_s {v['r_s_Mpc']:.3f} Mpc; "
        + "; ".join(f"{cv}: R {v[cv]['R_own_Mpc']:.3f} Mpc, rich={v[cv]['supply_rich']}, "
                    f"excess {v[cv]['free_excess_fraction_of_supply']:+.2f}, total/law {v[cv]['total_over_law_at_R']:.2f}"
                    for cv in ("200rho_c", "18pi2_rho_m_EdS")))
say("Design/law enclosed mass beyond r_s (reported):")
for key, v in tf.items():
    say(f"  {key}: " + ", ".join(f"{kk} {vv:.2f}" for kk, vv in v["design_over_law_enclosed"].items()))
say("Galaxy supply radii at f_s = 5.364 (owned supply is formation-dependent; reported only):")
for key, v in gal.items():
    say(f"  {key}: r_M {v['r_M_kpc']:.1f} kpc, r_s {v['r_s_kpc_at_f_s_5.364']:.1f} kpc")

say("Minimum owned supply ratio for an untruncated law out to R (f(f+1) = (R/r_M)^2): "
    + ", ".join(f"{k_} -> {v:.1f}" for k_, v in freq.items()))
say(f"Coma UDGs (reported): lower-bound excess from gas fraction 0.81 = {coma_pred:+.3f} dex; S1 isolated-law excess +0.33 dex")
say("M_x at owned supply f = 100 (200 rho_c): " + ", ".join(f"{k_} {v:.3g} Msun" for k_, v in mx100.items()))
npass = sum(1 for v in res["checks"].values() if v["pass"])
ntot = len(res["checks"])
say("")
if MUTATE:
    bit = (not res["checks"]["K1"]["pass"]) and (not res["checks"]["K6"]["pass"])
    say(f"MUTATE {'BITES: K1 and K6 FAIL as required' if bit else 'DID NOT BITE (K1/K6 still pass)'}")
    res["mutate_bites"] = bit
say(f"Z1_SUCCESSOR_DESIGN COMPLETE: {npass}/{ntot} checks PASS.")
res["summary"] = {"pass": npass, "total": ntot}

with open(OUT, "w") as fh:
    fh.write("\n".join(lines) + "\n")
with open(JSN, "w") as fh:
    json.dump(res, fh, indent=1, sort_keys=True, default=str)

if MUTATE:
    sys.exit(1)
sys.exit(0 if npass == ntot else 1)
