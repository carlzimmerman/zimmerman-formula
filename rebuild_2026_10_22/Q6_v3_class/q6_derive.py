#!/usr/bin/env python3
"""Q6_v3_class step D: v3's linear perturbations on FRW derived from the Khronon action (sympy), the LO system, and the
adiabatic initial conditions in CLASS's synchronous gauge (FROZEN_CRITERIA.md section 4 + AMENDMENT A1).

Action (BS24 = arXiv:2404.06584 Eq. 6, transcribed by C4 via WebFetch, not on disk; c = 1):
  16 pi G L / sqrt(-g) = R - 2 J(Y) + 2 K(Q),  Q = sqrt(-g^{mn} d_m tau d_n tau),  n_m = -d_m tau / Q,
  A_m = n^n nabla_n n_m,  Y = A.A,  K = mu_K^2 (Q - 1)^2 (Eq. 7),  J = J_x (C4 K2).
On FRW Y = O(eps^2), so the second-order action sees J only through J(0) = Lambda (moved to Omega_Lambda) and
j1 = J'(0) (= -1 for J_x).  Extra-sector Lagrangian used here: sqrt(-g) [-2 j1 Y + 2 K(Q)].

Conformal time; perturbations depend on (tau, x):
  g00 = -a^2(1 + e h00), g0x = a^2 e h0x, gxx = a^2(1 + e hxx), gyy = gzz = a^2(1 + e hyy);
  khronon T = Tb(tau) + e vt(tau, x), Tb' = a Qbar.   pi := vt / Tb' (time shift), Psi := h00/2.
Run: OMP_NUM_THREADS=1 nice -n 19 python3 -I q6_derive.py   (Q6_MUTATE=1: exported LO J term with j1 -> -j1; D5 must
FAIL; outputs *_MUTATE.*)
"""
import json
import os
import time

import sympy as sp

T0 = time.time()
MUT = os.environ.get("Q6_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = open(os.path.join(HERE, f"q6_derive{TAG}.out"), "w")
RES = {"mutate": MUT}
NPASS = NCHK = 0


def P(*a):
    s = " ".join(str(v) for v in a)
    print(s, flush=True)
    OUT.write(s + "\n")
    OUT.flush()


def check(name, ok, value, threshold):
    global NPASS, NCHK
    NCHK += 1
    NPASS += bool(ok)
    P(f"{name} {'PASS' if ok else 'FAIL'} {value} {threshold}")
    RES[name] = {"pass": bool(ok), "value": str(value), "threshold": str(threshold)}


tau, x, eps, k = sp.symbols("tau x epsilon k", real=True)
j1 = sp.Symbol("j_1", real=True)
a = sp.Function("a")(tau)
Tb = sp.Function("Tb")(tau)
K0f, K1f, K2f = (sp.Function(n)(tau) for n in ("K0", "K1", "K2"))   # K, K', K'' at Qbar(tau)
names = ("h00", "h0x", "hxx", "hyy", "vt")
fields = {n: sp.Function(n)(tau, x) for n in names}
h00, h0x, hxx, hyy, vt = (fields[n] for n in names)
X = [tau, x, sp.Symbol("y"), sp.Symbol("z")]


def trunc(e, n=2):
    out = 0
    d = e
    for i in range(n + 1):
        out += sp.expand(d.subs(eps, 0)) * eps**i / sp.factorial(i)
        if i < n:
            d = sp.diff(d, eps)
    return sp.expand(out)


P("== Q6 step D: v3 (Khronon + J_x + BS K(Q)) linear perturbations from the action (sympy)")
gb = sp.diag(-a**2, a**2, a**2, a**2)
dg = sp.zeros(4, 4)
dg[0, 0] = -a**2 * h00
dg[0, 1] = dg[1, 0] = a**2 * h0x
dg[1, 1] = a**2 * hxx
dg[2, 2] = dg[3, 3] = a**2 * hyy
g = gb + eps * dg
gbi = gb.inv()
M1 = gbi * dg
gi = (gbi - eps * M1 * gbi + eps**2 * M1 * M1 * gbi).applyfunc(sp.expand)
sqrtg = trunc(a**4 * sp.sqrt((1 + eps * h00) * (1 + eps * hxx) * (1 + eps * hyy)**2 + eps**2 * h0x**2), 2)
assert sp.expand(trunc(sqrtg**2) - trunc(-(g[0, 0] * g[1, 1] - g[0, 1]**2) * g[2, 2] * g[3, 3])) == 0


def Gam(m, al, be):
    return sp.Rational(1, 2) * sum(gi[m, s] * (sp.diff(g[s, al], X[be]) + sp.diff(g[s, be], X[al])
                                               - sp.diff(g[al, be], X[s])) for s in range(4))


Gm = [[[trunc(Gam(m, al, be), 1) for be in range(4)] for al in range(4)] for m in range(4)]
T = Tb + eps * vt
dT = [sp.diff(T, X[m]) for m in range(4)]
Xq = trunc(-sum(gi[m, n] * dT[m] * dT[n] for m in range(4) for n in range(4)))
Qb0 = sp.diff(Tb, tau) / a
u_ = sp.expand(Xq / Qb0**2 - 1)
assert u_.subs(eps, 0) == 0
Q = trunc(Qb0 * (1 + u_ / 2 - u_**2 / 8))                      # sqrt(1+u) to O(e^2)
nl = [trunc(-dT[m] / Q, 1) for m in range(4)]
nu = [trunc(sum(gi[m, n] * nl[n] for n in range(4)), 1) for m in range(4)]
chk_unit = sp.simplify(trunc(sum(nu[m] * nl[m] for m in range(4)), 1) + 1)
nab = [[trunc(sp.diff(nl[m], X[n_]) - sum(Gm[l][n_][m] * nl[l] for l in range(4)), 1) for m in range(4)]
       for n_ in range(4)]
A = [trunc(sum(nu[n_] * nab[n_][m] for n_ in range(4)), 1) for m in range(4)]
A0 = [sp.simplify(Am.coeff(eps, 0)) for Am in A]
A1 = [sp.expand(Am.coeff(eps, 1)) for Am in A]
Yfull = trunc(sum(gi[m, n] * A[m] * A[n] for m in range(4) for n in range(4)))
Y01 = [sp.simplify(Yfull.coeff(eps, 0)), sp.simplify(Yfull.coeff(eps, 1))]
Y2 = sp.expand(Yfull.coeff(eps, 2))
# J_x about Y = 0: a0 enters first at Y^(3/2)
a0s, Ys, Lam = sp.symbols("a_0 Y Lambda", positive=True)
ysym = sp.sqrt(Ys) / a0s
Jx = Lam - 2 * a0s**2 * (ysym - sp.log(1 + ysym))
Jser = sp.expand(sp.series(Jx, Ys, 0, 2).removeO())
s_ = sp.Symbol("s", positive=True)                       # s = sqrt(Y)
Jser_s = sp.expand(sp.series(Jx.subs(Ys, s_**2), s_, 0, 4).removeO())
c0, c2, c3 = Jser_s.coeff(s_, 0), Jser_s.coeff(s_, 2), Jser_s.coeff(s_, 3)
okD0 = (chk_unit == 0 and all(v == 0 for v in A0) and all(v == 0 for v in Y01) and sp.simplify(c0 - Lam) == 0
        and sp.simplify(c2 + 1) == 0 and Jser_s.coeff(s_, 1) == 0 and c3.has(a0s) and not c2.has(a0s))
check("D0_a0_absent", okD0, f"n.n=-1; A^(0)={A0}; Y^(0),Y^(1)={Y01}; J_x = {c0} + ({c2}) Y + ({sp.simplify(c3)}) Y^(3/2) + ...",
      "A^(0)=Y^(0)=Y^(1)=0; J(0)=Lambda, J'(0)=-1 free of a0; a0 first at Y^(3/2)")
RES["J_x_series"] = str(Jser_s)

Q1 = sp.expand(Q.coeff(eps, 1))
Q2 = sp.expand(Q.coeff(eps, 2))
Kexp = K0f + K1f * (eps * Q1 + eps**2 * Q2) + K2f * eps**2 * Q1**2 / 2
L = trunc(sqrtg * (-2 * j1 * eps**2 * Y2 + 2 * Kexp))
L1 = sp.expand(L.coeff(eps, 1))
L2 = sp.expand(L.coeff(eps, 2))
P(f"  action expanded: {len(L2.args)} terms at second order")


def EL(Lag, f):
    if not Lag.has(f):
        return sp.Integer(0)
    return sp.expand(sp.euler_equations(Lag, [f], [tau, x])[0].lhs)


bgvt = sp.expand(EL(L1, vt) + sp.diff(2 * a**3 * K1f, tau))
Qbar = sp.Symbol("Qbar")
sub_bg = {sp.Derivative(Tb, tau): a * Qbar}
rho_bg = sp.expand((-EL(L1, h00) / a**4).subs(sub_bg))
p_bg = sp.expand((EL(L1, hxx) / a**4).subs(sub_bg))
p_bg_y = sp.expand((EL(L1, hyy) / (2 * a**4)).subs(sub_bg))
okD1 = (bgvt == 0 and sp.expand(rho_bg - (Qbar * K1f - K0f)) == 0 and sp.expand(p_bg - K0f) == 0
        and sp.expand(p_bg_y - K0f) == 0 and EL(L1, h0x) == 0 and not L1.has(j1))
check("D1_background", okD1, f"EL_vt(L1) = -d(2a^3K')/dtau; 8piG rho = {rho_bg}; 8piG p = {p_bg}; J absent from L1",
      "a^3 K' = I0; Q K' - K; K; no J (G_cosmo = G)")

# ---------------------------------------------------------------- Fourier, symbolised background
amp = {n: sp.Function(n.upper() + "k")(tau) for n in names}
Ek = sp.exp(sp.I * k * x)
fsub = {fields[n]: amp[n] * Ek for n in names}
Qf = sp.Function("Qb")(tau)
bgsub = {sp.Derivative(Tb, (tau, 3)): sp.diff(a * Qf, tau, 2), sp.Derivative(Tb, (tau, 2)): sp.diff(a * Qf, tau),
         sp.Derivative(Tb, tau): a * Qf}
A_, Ap, App, Appp, Qs, k0, k1, k2, k3, k4 = sp.symbols("A Ap App Appp Q Kz Kp Kpp Kppp Kpppp")
Qp_ = -3 * Ap / A_ * k1 / k2                     # Qbar' from (a^3 K')' = 0
DRULE = {A_: Ap, Ap: App, App: Appp, Qs: Qp_, k0: k1 * Qp_, k1: k2 * Qp_, k2: k3 * Qp_, k3: k4 * Qp_}


def symb(e):
    e = sp.expand(e.subs(bgsub).doit())
    for n_ in (3, 2, 1):
        e = e.subs(sp.Derivative(Qf, (tau, n_)), sp.Symbol(f"QD{n_}"))
    e = e.subs({sp.Derivative(a, (tau, 3)): Appp, sp.Derivative(a, (tau, 2)): App, sp.Derivative(a, tau): Ap})
    e = e.subs({sp.Derivative(K2f, tau): k3 * sp.Symbol("QD1"), sp.Derivative(K1f, tau): k2 * sp.Symbol("QD1"),
                sp.Derivative(K0f, tau): k1 * sp.Symbol("QD1")})
    e = e.subs({a: A_, Qf: Qs, K0f: k0, K1f: k1, K2f: k2})
    QD1 = Qp_
    QD2 = sum(sp.diff(QD1, s__) * DRULE[s__] for s__ in DRULE)
    e = e.subs({sp.Symbol("QD1"): QD1, sp.Symbol("QD2"): QD2})
    return sp.expand(e)


def Dt(e):
    out = sp.diff(e, tau)
    for s__, d_ in DRULE.items():
        out += sp.diff(e, s__) * d_
    return out


def four(e):
    return sp.expand(sp.expand(e.subs(fsub).doit()) / Ek)


t1 = time.time()
ELk = {n: symb(four(EL(L2, fields[n]))) for n in names}
P(f"  Euler-Lagrange equations, Fourier, background symbolised ({time.time() - t1:.1f}s)")
H00, H0X, HXX, HYY, VT = (amp[n] for n in names)
rho = Qs * k1 - k0                 # 8piG rho_bar
pp = k0                            # 8piG p_bar
sg1 = A_**4 * (H00 + HXX + 2 * HYY) / 2
dT00 = (-ELk["h00"] / A_**2 - sg1 * rho / A_**2) / A_**4
dT0x = (ELk["h0x"] / (2 * A_**2)) / A_**4
dTxx = (ELk["hxx"] / A_**2 - sg1 * pp / A_**2) / A_**4
dTyy = (ELk["hyy"] / A_**2 / 2 - sg1 * pp / A_**2) / A_**4
drho = sp.expand(A_**2 * dT00 + H00 * rho)
dT0_x = sp.expand(rho * H0X + A_**2 * dT0x)
dTx_x = sp.expand(A_**2 * dTxx + pp * HXX)
dTy_y = sp.expand(A_**2 * dTyy + pp * HYY)
dp = sp.expand((dTx_x + 2 * dTy_y) / 3)
rpth = sp.expand(sp.I * k * dT0_x)
rps = sp.expand(-sp.Rational(2, 3) * (dTx_x - dTy_y))
Hc = Ap / A_
# Xi = Psi - pi' - H pi, pi = vt/(a Q): gauge-invariant acceleration potential; A_x = d_x Xi
PI = VT / (A_ * Qs)
Xi = sp.expand(H00 / 2 - Dt(PI) - Hc * PI)
A1x_k = symb(four(A1[1]))
okXi = sp.cancel(A1x_k - sp.I * k * Xi) == 0
gam = symb(four(Q1))                                                    # delta Q
okgam = sp.cancel(gam - (-Qs * Xi + Qp_ * PI)) == 0
drho_c = Qs * k2 * gam + 2 * j1 * k**2 / A_**2 * Xi
dp_c = k1 * gam
rpth_c = k**2 * k1 * Qs * PI                                           # = k^2 K' vt / a
okc = all(sp.cancel(u - v) == 0 for u, v in ((drho, drho_c), (dp, dp_c), (rpth, rpth_c)))
check("D2_shear", sp.cancel(rps) == 0, f"(rho+p) sigma = {sp.cancel(rps)}", "0")
check("D2_compact", okc and okXi and okgam,
      "A_x = i k Xi, Xi = Psi - pi' - H pi; dQ = -Q Xi + Q' pi; 8piG drho = Q K'' dQ + 2 j1 (k/a)^2 Xi; "
      "8piG dp = K' dQ; 8piG (rho+p) theta = k^2 K' Q pi (all gauges, h0x kept)", "exact")
# fluid form: rest-frame sound speed
cs2 = Qs * k1 / (Qs**2 * k2 - 2 * j1 * k**2 / A_**2)
ca2 = k1 / (Qs * k2)
drest = drho_c + 3 * Hc * rpth_c / k**2
okfl = (sp.cancel(dp_c - (cs2 * drest - 3 * Hc * ca2 * rpth_c / k**2)) == 0
        and sp.cancel(drest + (Qs**2 * k2 - 2 * j1 * k**2 / A_**2) * Xi) == 0)
check("D2_fluid", okfl, "8piG drho_rest = -(Q^2 K'' - 2 j1 k^2/a^2) Xi; dp = cs2 drho_rest - 3H ca2 (rho+p) theta/k^2, "
      "cs2 = Q K'/(Q^2 K'' - 2 j1 k^2/a^2), ca2 = K'/(Q K'')", "exact: a fluid fixed by (delta, theta), no shear")
RES["cs2"] = str(cs2)
RES["compact"] = {"drho": str(drho_c), "dp": str(dp_c), "rho_plus_p_theta": str(rpth_c), "Xi": str(Xi)}

# ---------------------------------------------------------------- CLASS-form systems (exact, and LO) in each gauge
de, th = (sp.Function(n)(tau) for n in ("delta", "theta"))
psi, phN = sp.Function("psi")(tau), sp.Function("phiN")(tau)
hS, etaS = sp.Function("h")(tau), sp.Function("eta")(tau)
syncg = {H00: 0, H0X: 0, HXX: hS + 4 * etaS, HYY: -2 * etaS}
newtg = {H00: 2 * psi, H0X: 0, HXX: -2 * phN, HYY: -2 * phN}
wv = k0 / rho
MU2 = sp.Symbol("mu2", positive=True)
cs2_LO = k1 / (2 * MU2 - 2 * j1 * k**2 / A_**2)                       # Q -> 1, K'' = 2 mu^2


def Pi_of(model, d_, t_):
    if model == "exact":
        return cs2 * (d_ + 3 * Hc * (1 + wv) * t_ / k**2) - 3 * Hc * ca2 * (1 + wv) * t_ / k**2
    return cs2_LO * (d_ + 3 * Hc * t_ / k**2)


def system(model, gname):
    w_ = wv if model == "exact" else 0
    c_ = ca2 if model == "exact" else 0
    Pi = Pi_of(model, de, th)
    if gname == "sync":
        mc, me = sp.diff(hS, tau) / 2, 0
    else:
        mc, me = -3 * sp.diff(phN, tau), k**2 * psi
    dprime = -(1 + w_) * (th + mc) - 3 * Hc * (Pi - w_ * de)
    tprime = -Hc * (1 - 3 * c_) * th + k**2 * Pi / (1 + w_) + me
    return {"delta": sp.expand(dprime), "theta": sp.expand(tprime)}


SYS = {(m, gn): system(m, gn) for m in ("exact", "LO") for gn in ("sync", "newt")}


# D4: conservation on the shell of the vt equation (exact system), both gauges
def conservation(gs, gname):
    ELv = sp.expand(ELk["vt"].subs(gs).doit())
    delta_f = sp.expand(drho.subs(gs).doit() / rho)
    theta_f = sp.expand(rpth.subs(gs).doit() / (rho + pp))
    Pi_f = sp.expand(dp.subs(gs).doit() / rho)
    if gname == "sync":
        mc, me = sp.diff(gs[HXX] + 2 * gs[HYY], tau) / 2, 0
    else:
        mc, me = -3 * sp.diff(phN, tau), k**2 * psi
    rhs_d = -(1 + wv) * (theta_f + mc) - 3 * Hc * (Pi_f - wv * delta_f)
    rhs_t = -Hc * (1 - 3 * ca2) * theta_f + k**2 * Pi_f / (1 + wv) + me
    out = []
    for lhs, rhs in ((Dt(delta_f), rhs_d), (Dt(theta_f), rhs_t)):
        r = sp.expand(lhs - rhs)
        cv = r.coeff(sp.Derivative(VT, (tau, 2)))
        if cv != 0:
            r = sp.expand(r - sp.cancel(cv / ELv.coeff(sp.Derivative(VT, (tau, 2)))) * ELv)
        out.append(sp.cancel(r))
    return out


for gs_, gn_ in ((syncg, "sync"), (newtg, "newt")):
    r1, r2 = conservation(gs_, gn_)
    check(f"D4_{gn_}", r1 == 0 and r2 == 0, f"{gn_}: continuity and Euler residuals on the shell of EL_vt: {r1}, {r2}",
          "0 and 0")


# D3: gauge map synchronous -> Newtonian, exact and LO systems
aC = sp.Function("alC")(tau)
psi_m = Dt(aC) + Hc * aC
phi_m = etaS - Hc * aC
dS, tS = sp.Function("dS")(tau), sp.Function("tS")(tau)
hprime_rule = {sp.Derivative(hS, tau): 2 * k**2 * aC - 6 * sp.Derivative(etaS, tau)}
d3 = {}
for model in ("exact", "LO"):
    w_ = wv if model == "exact" else 0
    mapN = {de: dS - 3 * Hc * (1 + w_) * aC, th: tS + k**2 * aC}
    mapS = {de: dS, th: tS}
    res = []
    for var, v_ in (("delta", de), ("theta", th)):
        dvN = Dt(mapN[v_])
        dvN = dvN.subs({sp.Derivative(dS, tau): SYS[(model, "sync")]["delta"].subs(hprime_rule).subs(mapS),
                        sp.Derivative(tS, tau): SYS[(model, "sync")]["theta"].subs(hprime_rule).subs(mapS)})
        rN = SYS[(model, "newt")][var].subs({sp.Derivative(phN, tau): Dt(phi_m), sp.Derivative(psi, tau): Dt(psi_m)})
        rN = rN.subs({psi: psi_m, phN: phi_m}).subs(mapN)
        res.append(sp.cancel(sp.expand((dvN - rN).subs(hprime_rule).doit())))
    d3[model] = [str(r) for r in res]
check("D3_gauge", all(v == ["0", "0"] for v in d3.values()), f"sync system + fluid map = Newtonian system: {d3}",
      "all 0 (exact and LO)")

# D4_LO: LO conserves its own T (fluid form with w = 0) -- equivalent to covariance of Pi_LO: delta_rest invariant
drest_N = sp.expand((de + 3 * Hc * th / k**2).subs({de: dS - 3 * Hc * aC, th: tS + k**2 * aC}) - (dS + 3 * Hc * tS / k**2))
check("D4_LO", drest_N == 0, f"LO pressure is c_s,LO^2 delta_rest with delta_rest gauge-invariant (residual {drest_N}); "
      "fluid equations with w = c_a^2 = 0 conserve T exactly", "0")

# D8: LO = exact at leading order in eps (quadratic K)
e_ = sp.Symbol("varepsilon", positive=True)
quad = {Qs: 1 + e_, k0: MU2 * e_**2, k1: 2 * MU2 * e_, k2: 2 * MU2, k3: 0, k4: 0}
cs2_q = sp.simplify(cs2.subs(quad))
lim_cs = sp.simplify(sp.limit(cs2_q / cs2_LO.subs(k1, 2 * MU2 * e_), e_, 0))
w_q = sp.simplify(wv.subs(quad))
ca_q = sp.simplify(ca2.subs(quad))
okD8 = lim_cs == 1 and sp.limit(w_q / e_, e_, 0) == sp.Rational(1, 2) and sp.limit(ca_q / e_, e_, 0) == 1
check("D8_LO_limit", okD8, f"quadratic K: cs2/cs2_LO -> {lim_cs}; w = {w_q} ~ e/2; ca2 = {ca_q} ~ e (e = Qbar - 1)",
      "cs2/cs2_LO -> 1; w, ca2 = O(e)")

# D5: quasi-static sub-horizon limit -> F3's kernels (khronon net self-force / Newtonian self-force)
# Euler (Newtonian gauge, sub-horizon): theta' = -H theta + k^2 Pi + k^2 psi; Poisson k^2 psi = -(a^2/2) 8piG drho_tot
# self part: s = 1 - k^2 cs2 / (a^2 8piG rho / 2) with 8piG rho = K' at LO
cs2_exp = cs2_LO
if MUT:
    cs2_exp = k1 / (2 * MU2 + 2 * j1 * k**2 / A_**2)                  # MUTATE: j1 -> -j1 in the J term
s_k = sp.simplify(1 - k**2 * cs2_exp / (A_**2 * k1 / 2))
s_bsk2 = A_**2 * MU2 / (k**2 + A_**2 * MU2)
s_jeans = 1 - k**2 / (A_**2 * MU2)
okD5 = sp.simplify(s_k.subs(j1, -1) - s_bsk2) == 0 and sp.simplify(s_k.subs(j1, 0) - s_jeans) == 0
check("D5_kernels", okD5, f"LO self-force kernel s = {sp.factor(s_k)}: j1=-1 -> {sp.factor(s_k.subs(j1, -1))}; "
      f"j1=0 -> {sp.factor(s_k.subs(j1, 0))}", "BSK2 a^2mu^2/(k^2+a^2mu^2) and Jeans 1-k^2/(a^2mu^2) exactly")

# D6: dust limit K'' -> infinity at fixed K' (any j1): cs2, ca2 -> 0; the background w -> 0 because K -> 0, Q -> const
lim6 = [sp.limit(cs2.subs(k2, sp.Symbol("Kinf")), sp.Symbol("Kinf"), sp.oo),
        sp.limit(ca2.subs(k2, sp.Symbol("Kinf")), sp.Symbol("Kinf"), sp.oo),
        sp.limit(cs2_LO.subs(MU2, sp.Symbol("Kinf")), sp.Symbol("Kinf"), sp.oo)]
check("D6_dust", all(v == 0 for v in lim6), f"K''->inf: cs2 -> {lim6[0]}, ca2 -> {lim6[1]}, cs2_LO -> {lim6[2]} "
      "(j1 symbolic); with K -> 0 the system is CDM's", "all 0")

# D7: Minkowski (a = 1, Qbar = 1, K = K' = 0): the khronon mode has omega = 0
mink = {A_: 1, Ap: 0, App: 0, Appp: 0, Qs: 1, k0: 0, k1: 0}
ELm = sp.expand(ELk["vt"].subs({H00: 0, H0X: 0, HXX: 0, HYY: 0}).doit().subs(mink))
om = sp.Symbol("omega")
disp = sp.factor(sp.expand(ELm.subs(VT, sp.exp(-sp.I * om * tau)).doit() / sp.exp(-sp.I * om * tau)))
okD7 = ELm.coeff(VT) == 0 and sp.expand(disp.subs(om, 0)) == 0 and sp.expand(sp.diff(disp, om).subs(om, 0)) == 0
check("D7_minkowski", okD7, f"EL_vt (Minkowski) = {ELm}; dispersion {disp}", "omega = 0 double root (non-propagating)")

# ---------------------------------------------------------------- IC: LO, synchronous gauge, radiation era
# D10 (A2): LO's rest-frame sound speed is superluminal where eps > 1; LOB's (literal) is not; super-horizon frequency
cs2_lob = (1 + e_) * 2 * MU2 * e_ / ((1 + e_)**2 * 2 * MU2 + 2 * k**2 / A_**2)       # exact quadratic K, j1 = -1
cs2_lo = 2 * MU2 * e_ / (2 * MU2 + 2 * k**2 / A_**2)
bound = sp.simplify(e_ / (1 + e_) - cs2_lob)                                          # >= 0
lo_k0 = sp.limit(cs2_lo, k, 0)
Xs, ths = sp.Function("X")(tau), sp.Function("thv")(tau)
csym = sp.Symbol("c_s2", positive=True)
# X = delta + 3 H theta/k^2 with the LOB/LO fluid (w = 0): X' = -theta - h'/2 + 3(H' - H^2) theta/k^2 (c_s^2 drops out)
dX = sp.expand(SYS[("LO", "sync")]["delta"] + 3 * (Dt(Hc) * th + Hc * SYS[("LO", "sync")]["theta"]) / k**2)
dX_expected = -th - sp.diff(hS, tau) / 2 + 3 * (Dt(Hc) - Hc**2) * th / k**2
okX = sp.simplify(dX - dX_expected) == 0
okD10 = (sp.simplify(bound.subs(k, 0) - e_**2 / ((1 + e_) * (1 + e_))) == 0 or sp.simplify(bound.subs(k, 0)) == 0) and \
    all(sp.N(bound.subs({e_: ev, k: kv, A_: 1, MU2: 1})) >= 0 for ev in (0.01, 1, 100) for kv in (0, 0.5, 30)) and \
    sp.simplify(lo_k0 - e_) == 0 and okX
check("D10_superluminal", okD10, f"LOB cs2 <= eps/(1+eps) (bound - cs2 = {sp.factor(bound)}); LO cs2(k->0) = {lo_k0}; "
      "X' = -theta - h'/2 + 3(H'-H^2)theta/k^2 (no cs2) => super-horizon omega^2 = 3(H^2-H')cs2",
      "LOB subluminal; LO -> eps (> 1 early); identity exact")

# ---------------------------------------------------------------- IC: LOB, synchronous gauge, radiation era (A2)
P("== IC (A2): LOB, synchronous gauge, radiation era, leading order, c_s^2 = s frozen at tau_ini (w = 0)")
C, fnu, sS = sp.symbols("C f_nu s", positive=True)
tt = sp.Symbol("t", positive=True)
hser = C * k**2 * tt**2
etaser = 2 * C * (1 - (5 + 4 * fnu) * k**2 * tt**2 / (12 * (15 + 4 * fnu)))


def gdm_res(dS_, tS_, cs_, gauge="sync", psi_=0, phi_=0):
    Hh = 1 / tt
    Pi = cs_ * (dS_ + 3 * Hh * tS_ / k**2)
    if gauge == "sync":
        rd = sp.diff(dS_, tt) - (-(tS_ + sp.diff(hser, tt) / 2) - 3 * Hh * Pi)
        rt = sp.diff(tS_, tt) - (-Hh * tS_ + k**2 * Pi)
    else:
        rd = sp.diff(dS_, tt) - (-(tS_ - 3 * sp.diff(phi_, tt)) - 3 * Hh * Pi)
        rt = sp.diff(tS_, tt) - (-Hh * tS_ + k**2 * Pi + k**2 * psi_)
    return sp.expand(rd), sp.expand(rt)


def by_power(e):
    out = {}
    for term in sp.Add.make_args(sp.expand(e)):
        c_, p_ = term.as_coeff_exponent(tt)
        out[p_] = out.get(p_, 0) + c_
    return out


def lowpow(e):
    bp = {p_: c_ for p_, c_ in by_power(e).items() if sp.simplify(c_) != 0}
    return min(bp) if bp else 99


# series solve (s constant): delta = sum d_i t^i, theta = sum t_i t^i, adiabatic (no constant delta)
N_ORD = 5
dco = sp.symbols(f"d0:{N_ORD + 1}")
tco = sp.symbols(f"t0:{N_ORD + 1}")
dser = sum(dco[i] * tt**i for i in range(N_ORD + 1))
tser = sum(tco[i] * tt**i for i in range(N_ORD + 1))
rd, rt = gdm_res(dser, tser, sS)
eqs = []
for bp in (by_power(rd), by_power(rt)):
    eqs += [sp.expand(c_) for p_, c_ in bp.items() if p_ <= 2]
sol = sp.solve(eqs + [dco[0]], list(dco[:4]) + list(tco[:4]), dict=True)
assert len(sol) == 1, sol
sl = sol[0]
d_l = sp.factor(sl.get(dco[2], 0)) * tt**2
t_l = sp.factor(sl.get(tco[3], 0)) * tt**3
lower = {str(u): str(sl.get(u, 0)) for u in (dco[1], tco[0], tco[1], tco[2])}
P(f"  series (s const): delta = {d_l} + ..., theta = {t_l} + ...; lower coefficients {lower}")
RES["IC_LOB_series"] = {"delta": str(d_l), "theta": str(t_l), "lower_coefficients": lower}
r1d, r1t = gdm_res(d_l, t_l, sS)
ic1 = {"delta": (lowpow(r1d), lowpow(sp.diff(d_l, tt))), "theta": (lowpow(r1t), lowpow(sp.diff(t_l, tt)))}
check("IC1_series", all(r > l for r, l in ic1.values()) and all(v == "0" for v in lower.values()),
      f"(residual lowest power, lhs lowest power): {ic1}", "residual power > leading power; no lower terms")
# IC_fld: CLASS's fluid formula (1004.5509) with w = 0, cs2 = s; C = curvature_ini s2^2/2, delta_g = -2/3 C (k t)^2
d_fld = -(k * tt)**2 / 4 * (4 - 3 * sS) / (4 + 3 * sS) * 2 * C
t_fld = -k * (k * tt)**3 / 4 * sS / (4 + 3 * sS) * 2 * C
check("IC_fld", sp.simplify(d_fld - d_l) == 0 and sp.simplify(t_fld - t_l) == 0,
      f"coded IC delta = 3/4 delta_g (4-3s)/(4+3s), theta = -k (k tau)^3 s/(4(4+3s)) curvature_ini: residuals "
      f"{sp.simplify(d_fld - d_l)}, {sp.simplify(t_fld - t_l)}", "0, 0")
check("IC2_dust", sp.simplify(d_l.subs(sS, 0) + C * k**2 * tt**2 / 2) == 0 and t_l.subs(sS, 0) == 0,
      f"s = 0: delta = {d_l.subs(sS, 0)}, theta = {t_l.subs(sS, 0)}", "CDM: -C k^2 t^2/2 (= 3/4 delta_g), 0")
aCser = (sp.diff(hser, tt) + 6 * sp.diff(etaser, tt)) / (2 * k**2)
dN = d_l - 3 / tt * aCser
tN = t_l + k**2 * aCser
psis = sp.diff(aCser, tt) + aCser / tt
phis = etaser - aCser / tt
rNd, rNt = gdm_res(dN, tN, sS, "newt", psis, phis)
ic3 = {"delta": (lowpow(rNd), lowpow(sp.diff(dN, tt))), "theta": (lowpow(rNt), lowpow(sp.diff(tN, tt)))}
check("IC3_newtonian", all(r > l for r, l in ic3.values()), f"(residual, lhs) lowest powers: {ic3}",
      "residual power > leading power")
ic_c7 = sp.simplify(d_l + C * k**2 * tt**2 / 2) == 0 and t_l == 0
P(f"IC_C7 (reported, A2) {'PASS' if ic_c7 else 'FAIL'} C7's block (w = c_a^2 = 0): delta = -C k^2 t^2/2, theta = 0 vs "
  f"LOB delta {d_l}, theta {t_l}; equal only at s = 0 -> IC block replaced (A2.2)")
RES["IC_C7_reported"] = {"pass": bool(ic_c7)}

# ---------------------------------------------------------------- C forms coded in the patch (must equal derived)
# C: rho_hat = Q*Kp - Kz; w = Kz/rho_hat; ca2 (background); cs2 = Q*Kp/(Q*Q*Kpp - 2*j1*k2/a/a) (LIT),
#    Kp/(Kpp - 2*j1*k2/a/a) (LO, Kpp = 2 mu^2); Pi = cs2*(delta + 3*H*(1+w)*theta/k2) - 3*H*ca2*(1+w)*theta/k2
Kpp_c = sp.Symbol("Kpp")
Pi_C_lit = cs2 * (de + 3 * Hc * (1 + wv) * th / k**2) - 3 * Hc * ca2 * (1 + wv) * th / k**2
Pi_C_lo = (k1 / (2 * MU2 - 2 * j1 * k**2 / A_**2)) * (de + 3 * Hc * th / k**2)
okC = (sp.cancel(Pi_C_lit - Pi_of("exact", de, th)) == 0 and sp.cancel(Pi_C_lo - Pi_of("LO", de, th)) == 0)
check("D9_cform", okC, "C-form Pi (LIT, LO) minus derived", "0")
EXPORT = {"cs2_exact": str(cs2), "ca2": str(ca2), "w": str(wv), "cs2_LO": str(cs2_exp),
          "cs2_LOB": "(1+eps)*Kp/((1+eps)^2*Kpp - 2*j1*k^2/a^2), eps = Kp/Kpp (quadratic K: Q = 1 + eps), Kpp = 2 mu^2",
          "IC": "delta = 3/4 delta_g (1+w)(4-3 cs2)/(4-6w+3 cs2); theta = -k (k tau)^3 cs2/(4(4-6w+3 cs2)) curvature_ini s2^2",
          "Pi_exact": "cs2*(delta + 3*H*(1+w)*theta/k^2) - 3*H*ca2*(1+w)*theta/k^2",
          "Pi_LO": "cs2_LO*(delta + 3*H*theta/k^2)",
          "fluid": "delta' = -(1+w)(theta + metric_continuity) - 3H(Pi - w delta); "
                   "theta' = -H(1-3ca2) theta + k^2 Pi/(1+w) + metric_euler; sigma = 0",
          "note": "Kz, Kp, Kpp = K, K', K'' at Qbar (Mpc^-2; Q dimensionless); Kpp = 2 mu_K^2 (quadratic K); "
                  "j1 = J'(0) (-1 for J_x); H = a'/a conformal; units 8piG = 1 in rho_hat = Q Kp - Kz."}
json.dump(EXPORT, open(os.path.join(HERE, f"q6_equations{TAG}.json"), "w"), indent=1)
RES["export"] = EXPORT
RES["elapsed_s"] = round(time.time() - T0, 1)
json.dump(RES, open(os.path.join(HERE, f"q6_derive_results{TAG}.json"), "w"), indent=1)
P(f"Q6_DERIVE COMPLETE: {NPASS}/{NCHK} checks PASS.")
OUT.close()
raise SystemExit(0 if NPASS == NCHK else 1)
