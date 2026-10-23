#!/usr/bin/env python3
"""C7_aest_class step D + IC: AeST linear perturbations on FRW derived from the covariant action (sympy), and the
adiabatic initial conditions of the extra sector in CLASS's synchronous gauge.

External input SZ21 = arXiv:2007.00082 (newRMONDLett.tex), eq. NT_A_action:
  16 pi G~ L/sqrt(-g) = R - (K_B/2) F_{mn}F^{mn} + 2(2-K_B) J^m d_m phi - (2-K_B) Y - F(Y,Q) - lambda (A.A+1),
  J_m = A^a nabla_a A_m, Q = A^m d_m phi, Y = q^{mn} d_m phi d_n phi, q = g + A A.
Premise P-F: F(Y,Q) = -2K(Q) + (2-K_B) lam_c Y + o(Y) near Y = 0 (lam_c kept symbolic; 0 in all runs).

Conformal time tau; perturbations depend on (tau, x) only (one Fourier direction):
  g00 = -a^2(1 + e h00), g0x = a^2 e h0x, gxx = a^2(1 + e hxx), gyy = gzz = a^2(1 + e hyy);
  phi = pb(tau) + e vphi;  A_x = e d_x alpha;  A_y = A_z = 0;  A_0 from the unit constraint (multiplier eliminated).
Extra-sector stress tensor: T^{mn} = (2/sqrt(-g)) dS_ext/dg_{mn}, read off the metric Euler-Lagrange expressions.

Checks (FROZEN_CRITERIA.md): D0 (constraint, Y on FRW), D1 (background), D2 (SZ21's Newtonian-gauge system),
D3 (gauge map synchronous -> Newtonian), D4 (conservation), IC1-IC3 (adiabatic initial conditions).
Outputs: c7_derive.out, c7_derive_results.json, c7_aest_equations.json (C expressions used by the patch).
Run: OMP_NUM_THREADS=1 nice -n 15 python3 c7_derive.py      (C7_MUTATE=1: one sign flipped in the E equation
used for the code export; D3/IC1 must then fail; outputs *_MUTATE.*)
"""
import json
import os
import time

import sympy as sp

T0 = time.time()
MUT = os.environ.get("C7_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = open(os.path.join(HERE, f"c7_derive{TAG}.out"), "w")
RES = {"mutate": MUT}
NPASS = 0
NCHK = 0


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
KB, lamc = sp.symbols("K_B lambda_c", real=True)
a = sp.Function("a")(tau)
pb = sp.Function("pb")(tau)
K0f = sp.Function("K0")(tau)          # K(Qbar(tau))
K1f = sp.Function("K1")(tau)          # K'(Qbar(tau))
K2f = sp.Function("K2")(tau)          # K''(Qbar(tau))
names = ("h00", "h0x", "hxx", "hyy", "vphi", "alpha")
fields = {n: sp.Function(n)(tau, x) for n in names}
h00, h0x, hxx, hyy, vphi, alpha = (fields[n] for n in names)
X = [tau, x, sp.Symbol("y"), sp.Symbol("z")]


def trunc(e, n=2):
    out = 0
    d = e
    for i in range(n + 1):
        out += sp.expand(d.subs(eps, 0)) * eps**i / sp.factorial(i)
        if i < n:
            d = sp.diff(d, eps)
    return sp.expand(out)


P("== C7 step D: AeST linear perturbations from the covariant action (sympy)")
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
chk_det = sp.expand(trunc(sqrtg**2) - trunc(-(g[0, 0] * g[1, 1] - g[0, 1]**2) * g[2, 2] * g[3, 3]))
assert chk_det == 0


def Gam(m, al, be):
    return sp.Rational(1, 2) * sum(gi[m, s] * (sp.diff(g[s, al], X[be]) + sp.diff(g[s, be], X[al])
                                               - sp.diff(g[al, be], X[s])) for s in range(4))


Gm = [[[trunc(Gam(m, al, be)) for be in range(4)] for al in range(4)] for m in range(4)]
Ax = eps * sp.diff(alpha, x)
a01, a02 = sp.symbols("a01 a02")
A0try = -a + eps * a01 + eps**2 * a02
con = trunc(gi[0, 0] * A0try**2 + 2 * gi[0, 1] * A0try * Ax + gi[1, 1] * Ax**2 + 1)
s1 = sp.solve(con.coeff(eps, 1), a01)[0]
s2 = sp.solve(sp.expand(con.coeff(eps, 2).subs(a01, s1)), a02)[0]
A0 = sp.expand(-a + eps * s1 + eps**2 * s2)
Al = [A0, Ax, 0, 0]
Au = [trunc(sum(gi[m, n] * Al[n] for n in range(4))) for m in range(4)]
check("D0_unit", sp.expand(trunc(sum(Au[m] * Al[m] for m in range(4)) + 1)) == 0,
      "A.A + 1 = 0 to O(e^2), A_0 = -a(1 + e h00/2) + O(e^2)", "identically 0")
phi = pb + eps * vphi
dphi = [sp.diff(phi, X[m]) for m in range(4)]
nabA = [[trunc(sp.diff(Au[m], X[al]) + sum(Gm[m][al][b] * Au[b] for b in range(4))) for m in range(4)]
        for al in range(4)]
J = [trunc(sum(Au[al] * nabA[al][m] for al in range(4))) for m in range(4)]
Jdphi = trunc(sum(J[m] * dphi[m] for m in range(4)))
F01 = sp.diff(Al[1], tau) - sp.diff(Al[0], x)
Fl = sp.zeros(4, 4)
Fl[0, 1] = F01
Fl[1, 0] = -F01
F2 = trunc(sum(Fl[m, n] * Fl[r, s] * gi[m, r] * gi[n, s] for m in range(2) for n in range(2)
               for r in range(2) for s in range(2)))
Q = trunc(sum(Au[m] * dphi[m] for m in range(4)))
Y = trunc(sum((gi[m, n] + Au[m] * Au[n]) * dphi[m] * dphi[n] for m in range(4) for n in range(4)))
check("D0_Ybg", sp.expand(trunc(Y, 1)) == 0, "Y^(0) = Y^(1) = 0 on FRW (as C2 K1)", "identically 0")
Q1 = sp.expand(sp.diff(Q, eps).subs(eps, 0))
Q2 = sp.expand(sp.diff(Q, eps, 2).subs(eps, 0) / 2)
Kexp = K0f + K1f * (eps * Q1 + eps**2 * Q2) + K2f * eps**2 * Q1**2 / 2
L = trunc(sqrtg * (-KB / 2 * F2 + 2 * (2 - KB) * Jdphi - (2 - KB) * (1 + lamc) * Y + 2 * Kexp))
L1 = sp.expand(L.coeff(eps, 1))
L2 = sp.expand(L.coeff(eps, 2))
P(f"  action expanded: {len(L2.args)} terms at second order; background Q = {sp.expand(trunc(Q, 0))}")


def EL(Lag, f):
    if not Lag.has(f):
        return sp.Integer(0)
    return sp.expand(sp.euler_equations(Lag, [f], [tau, x])[0].lhs)


bgphi = sp.expand(EL(L1, vphi) + sp.diff(2 * a**3 * K1f, tau))
check("D1_phibar", bgphi == 0, "EL_vphi(L1) = -d(2 a^3 K')/dtau, so a^3 K' = I0 (SZ21)", "residual 0")
Qbar = sp.Symbol("Qbar")
sub_bg = {sp.Derivative(pb, tau): a * Qbar}
rho_bg = sp.expand((-EL(L1, h00) / a**4).subs(sub_bg))
p_bg = sp.expand((EL(L1, hxx) / a**4).subs(sub_bg))
p_bg_y = sp.expand((EL(L1, hyy) / (2 * a**4)).subs(sub_bg))
mom_bg = EL(L1, h0x)
okD1 = (sp.expand(rho_bg - (Qbar * K1f - K0f)) == 0 and sp.expand(p_bg - K0f) == 0
        and sp.expand(p_bg_y - K0f) == 0 and mom_bg == 0)
check("D1_rho_p", okD1, f"8piG~rho = {rho_bg}, 8piG~P = {p_bg}", "Q K' - K and K (SZ21)")

# ---------------------------------------------------------------- linear equations, Fourier, symbolised background
amp = {n: sp.Function(n.upper() + "k")(tau) for n in names}
Ek = sp.exp(sp.I * k * x)
fsub = {fields[n]: amp[n] * Ek for n in names}
Qf = sp.Function("Qb")(tau)
bgsub = {sp.Derivative(pb, (tau, 3)): sp.diff(a * Qf, tau, 2), sp.Derivative(pb, (tau, 2)): sp.diff(a * Qf, tau),
         sp.Derivative(pb, tau): a * Qf}
# symbols for background quantities and their derivative rules
A_, Ap, App, Appp, Qs, k0, k1, k2, k3, k4 = sp.symbols("A Ap App Appp Q Kz Kp Kpp Kppp Kpppp")
Qp_ = -3 * Ap / A_ * k1 / k2          # Qbar' from (a^3 K')' = 0
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
    QD2 = sum(sp.diff(QD1, s_) * DRULE[s_] for s_ in DRULE)
    e = e.subs({sp.Symbol("QD1"): QD1, sp.Symbol("QD2"): QD2})
    return sp.expand(e)


def Dt(e):
    """total tau-derivative: explicit perturbation functions + background chain rule."""
    out = sp.diff(e, tau)
    for s_, d_ in DRULE.items():
        out += sp.diff(e, s_) * d_
    return out


def four(e):
    return sp.expand(sp.expand(e.subs(fsub).doit()) / Ek)


t1 = time.time()
ELk = {n: symb(four(EL(L2, fields[n]))) for n in names}
P(f"  Euler-Lagrange equations, Fourier, background symbolised ({time.time()-t1:.1f}s)")
H00, H0X, HXX, HYY, VP, AL = (amp[n] for n in names)
rho = Qs * k1 - k0           # 8piG~ rho_bar
pp = k0                      # 8piG~ p_bar
sg1 = A_**4 * (H00 + HXX + 2 * HYY) / 2
dT00 = (-ELk["h00"] / A_**2 - sg1 * rho / A_**2) / A_**4
dT0x = (ELk["h0x"] / (2 * A_**2)) / A_**4
dTxx = (ELk["hxx"] / A_**2 - sg1 * pp / A_**2) / A_**4
dTyy = (ELk["hyy"] / A_**2 / 2 - sg1 * pp / A_**2) / A_**4
drho = sp.expand(A_**2 * dT00 + H00 * rho)                 # -dT^0_0
dT0_x = sp.expand(rho * H0X + A_**2 * dT0x)
dTx_x = sp.expand(A_**2 * dTxx + pp * HXX)
dTy_y = sp.expand(A_**2 * dTyy + pp * HYY)
dp = sp.expand((dTx_x + 2 * dTy_y) / 3)
rpth = sp.expand(sp.I * k * dT0_x)
rps = sp.expand(-sp.Rational(2, 3) * (dTx_x - dTy_y))
check("D2_shear", sp.cancel(rps) == 0, f"(rho+p) sigma_aest = {sp.cancel(rps)}", "0 (SZ21: shear eq. as in GR)")

# gauge-general compact forms (h0x = 0 gauges): E = alpha'/a + h00/2, chi = vphi + Q alpha, gam = vphi'/a - Q h00/2
Ed = sp.diff(AL, tau) / A_ + H00 / 2
chid = VP + Qs * AL
gamd = sp.diff(VP, tau) / A_ - Qs * H00 / 2
drho_c = Qs * k2 * gamd - k**2 / A_**2 * (KB * Ed + (2 - KB) * chid)
dp_c = k1 * gamd
rpth_c = k**2 * k1 * VP / A_
okc = all(sp.cancel((u - v).subs(H0X, 0)) == 0 for u, v in ((drho, drho_c), (dp, dp_c), (rpth, rpth_c)))
check("D2_compact", okc, "8piG~ drho = Q K'' gam - (k/a)^2 [K_B E + (2-K_B) chi]; 8piG~ dp = K' gam; "
      "8piG~ (rho+p) theta = k^2 K' vphi / a", "exact (h0x = 0)")
RES["compact"] = {"drho": str(drho_c), "dp": str(dp_c), "rho_plus_p_theta": str(rpth_c)}

# ---------------------------------------------------------------- D2: SZ21 Newtonian gauge
psi, phN = sp.Function("psi")(tau), sp.Function("phiN")(tau)
newt = {H00: 2 * psi, H0X: 0, HXX: -2 * phN, HYY: -2 * phN}


def gauge(e, gs):
    return sp.expand(e.subs(gs).doit())


cad2 = k1 / (Qs * k2)
w = k0 / rho
chi = VP + Qs * AL
EN = sp.diff(AL, tau) / A_ + psi
gamN = sp.diff(VP, tau) / A_ - Qs * psi
lap = -k**2
delta_SZ = (1 + w) / (Qs * cad2) * gamN + lap * (KB * EN + (2 - KB) * chi) / (A_**2 * rho)
check("D2_delta", sp.cancel(gauge(drho, newt) / rho - delta_SZ) == 0,
      "drho/rho = SZ21 eq. delta_field_relation", "residual 0")
check("D2_theta", sp.cancel(gauge(rpth, newt) / (rho + pp) - k**2 * (VP / Qs) / A_) == 0,
      "theta_CLASS = k^2 theta_SZ / a, theta_SZ = vphi/Qbar (eq. theta_field_relation)", "residual 0")
Pi_SZ = cad2 * delta_SZ - cad2 / (A_**2 * rho) * lap * (KB * EN + (2 - KB) * chi)
check("D2_Pi", sp.cancel(gauge(dp, newt) / rho - Pi_SZ) == 0, "dp/rho = SZ21 eq. Pi_delta_E_alpha", "residual 0")

ELphiN = gauge(ELk["vphi"], newt)
ELalN = gauge(ELk["alpha"], newt)
Hc = Ap / A_**2
Edot = Dt(EN) / A_
SZ_E = KB * (Edot + Hc * EN) - k1 * chi + (2 - KB) * (Qs * Pi_SZ / (1 + w) + (Hc + Qs) * chi
                                                      - 3 * cad2 * Hc * Qs * AL)
# SZ_E contains alpha'' only through E-dot; match on the alpha'' coefficient, then the residual must vanish
SZ_E = sp.expand(SZ_E)
cE = sp.cancel(SZ_E.coeff(sp.Derivative(AL, (tau, 2))) / ELalN.coeff(sp.Derivative(AL, (tau, 2))))
residE = sp.cancel(sp.expand(SZ_E - cE * ELalN).subs(lamc, 0))
residE_lam = sp.factor(sp.cancel(sp.expand(SZ_E - cE * ELalN)))
check("D2_Eeq", residE == 0, f"SZ21 E equation = ({cE}) x EL_alpha at lambda_c = 0; residual {residE}",
      "residual 0")
P(f"  with lambda_c != 0 the SZ21 E equation misses: {residE_lam}  (SZ21 writes the lambda_c = 0 case)")
RES["E_eq_lambda_c_term"] = str(residE_lam)

# ---------------------------------------------------------------- CLASS-form system in each gauge
# variables: delta, theta (CLASS), E, alpha (vector potential, A_x = d_x alpha).
de, th, EE, al = (sp.Function(n)(tau) for n in ("delta", "theta", "E", "alv"))


def system(gs, gname):
    """Return (rhs dict for delta', theta', E', alpha', dp/rho expression, substitution map) in gauge gs."""
    h00g = gs.get(H00, 0)
    vp_of = A_ * Qs * th / k**2                       # vphi from theta  (rpth_c / (rho+p), rho+p = Q K')
    # vphi' from delta: drho = rho*delta  =>  gam = (rho delta + (k/a)^2 [K_B E + (2-K_B) chi]) / (Q K'')
    chi_of = vp_of + Qs * al
    gam_of = (rho * de + k**2 / A_**2 * (KB * EE + (2 - KB) * chi_of)) / (Qs * k2)
    vpp_of = A_ * (gam_of + Qs * h00g / 2)            # vphi'
    alp_of = A_ * (EE - h00g / 2)                     # alpha'
    # E' from EL_alpha: solve for alpha''
    ELa = gauge(ELk["alpha"], gs)
    c2 = ELa.coeff(sp.Derivative(AL, (tau, 2)))
    alpp = sp.expand(-(ELa - c2 * sp.Derivative(AL, (tau, 2))) / c2)
    # need vphi'' ? (should not appear)
    assert not alpp.has(sp.Derivative(VP, (tau, 2)))
    # E = alpha'/a + h00/2  =>  E' = alpha''/a - (a'/a^2) alpha' + h00'/2
    Eprime = alpp / A_ - Ap / A_**2 * sp.Derivative(AL, tau) + sp.diff(h00g, tau) / 2
    rep = {sp.Derivative(VP, tau): vpp_of, sp.Derivative(AL, tau): alp_of}
    Eprime = sp.expand(Eprime.subs(rep).subs({VP: vp_of, AL: al}))
    if MUT and gname == "newt":
        # MUTATE: flip the sign of the delta term of E' in the Newtonian system only; D3 must catch it
        Eprime = sp.expand(Eprime - 2 * Eprime.coeff(de) * de)
    dpr = sp.expand((dp_c.subs({sp.Derivative(VP, tau): vpp_of}).subs({VP: vp_of, H00: h00g})) / rho)
    wv = k0 / rho
    ca = k1 / (Qs * k2)
    if gname == "sync":
        hS, etaS = gs["_h"], gs["_eta"]
        dprime = -(1 + wv) * (th + sp.diff(hS, tau) / 2) - 3 * Ap / A_ * (dpr - wv * de)
        tprime = -Ap / A_ * (1 - 3 * ca) * th + k**2 * dpr / (1 + wv)
    else:
        dprime = -(1 + wv) * (th - 3 * sp.diff(phN, tau)) - 3 * Ap / A_ * (dpr - wv * de)
        tprime = -Ap / A_ * (1 - 3 * ca) * th + k**2 * dpr / (1 + wv) + k**2 * psi
    return {"delta": sp.expand(dprime), "theta": sp.expand(tprime), "E": Eprime, "alv": sp.expand(alp_of.subs({}))}, \
        dpr, {"vphi": vp_of, "gam": gam_of, "chi": chi_of}


hS, etaS = sp.Function("h")(tau), sp.Function("eta")(tau)
sync = {H00: 0, H0X: 0, HXX: hS + 4 * etaS, HYY: -2 * etaS, "_h": hS, "_eta": etaS}
syncg = {H00: 0, H0X: 0, HXX: hS + 4 * etaS, HYY: -2 * etaS}
newtg = dict(newt)
t1 = time.time()
SYS_S, DPR_S, AUX_S = system(dict(sync), "sync")
SYS_N, DPR_N, AUX_N = system(dict(newtg), "newt")
P(f"  CLASS-form systems built ({time.time()-t1:.1f}s)")

# ---------------------------------------------------------------- D4: conservation on the shell of the field equations
# delta(tau) := drho/rho evaluated on the fields; its tau-derivative minus the fluid RHS must be a multiple of EL_vphi.


def conservation(gs, gname):
    ELp = gauge(ELk["vphi"], gs)
    h00g = gs.get(H00, 0)
    delta_f = sp.expand(gauge(drho, gs) / rho)
    theta_f = sp.expand(gauge(rpth, gs) / (rho + pp))
    dpr_f = sp.expand(gauge(dp, gs) / rho)
    wv = k0 / rho
    ca = k1 / (Qs * k2)
    if gname == "sync":
        rhs_d = -(1 + wv) * (theta_f + sp.diff(gs[HXX] + 2 * gs[HYY], tau) / 2) - 3 * Ap / A_ * (dpr_f - wv * delta_f)
        rhs_t = -Ap / A_ * (1 - 3 * ca) * theta_f + k**2 * dpr_f / (1 + wv)
    else:
        rhs_d = -(1 + wv) * (theta_f - 3 * sp.diff(phN, tau)) - 3 * Ap / A_ * (dpr_f - wv * delta_f)
        rhs_t = -Ap / A_ * (1 - 3 * ca) * theta_f + k**2 * dpr_f / (1 + wv) + k**2 * psi
    rd = sp.expand(Dt(delta_f) - rhs_d)
    rt = sp.expand(Dt(theta_f) - rhs_t)
    ELa = gauge(ELk["alpha"], gs)
    c_ = rd.coeff(sp.Derivative(VP, (tau, 2))) / ELp.coeff(sp.Derivative(VP, (tau, 2)))
    rd = sp.expand(rd - c_ * ELp)
    ca_ = rd.coeff(sp.Derivative(AL, (tau, 2))) / ELa.coeff(sp.Derivative(AL, (tau, 2)))
    r1 = sp.cancel(sp.expand(rd - ca_ * ELa))
    r2 = sp.cancel(rt)
    return r1, r2


for gs_, gn_ in ((syncg, "sync"), (newtg, "newt")):
    r1, r2 = conservation(gs_, gn_)
    check(f"D4_{gn_}", r1 == 0 and r2 == 0,
          f"{gn_}: d(delta)/dtau - fluid RHS = c1 EL_vphi + c2 EL_alpha (residual {r1}); theta eq. residual {r2}", "0 and 0")

# ---------------------------------------------------------------- D3: gauge map synchronous -> Newtonian
# CLASS: alpha_C = (h' + 6 eta')/(2k^2), psi = alpha_C' + H alpha_C, phi = eta - H alpha_C;
# fields: delta_N = delta_S - 3H(1+w) alpha_C (from rho'/rho), theta_N = theta_S + k^2 alpha_C,
# vector: alpha_N = alpha_S - a alpha_C (A_x shifts by -A0bar d_x T, T = -alpha_C), E_N = E_S (E is F_0x/a).
aC = sp.Function("alC")(tau)        # treat alpha_C as a free function; h' = 2k^2 alpha_C - 6 eta'
Hh = Ap / A_
psi_m = Dt(aC) + Hh * aC
phi_m = etaS - Hh * aC
wv = k0 / rho
dS, tS, ES, aS = (sp.Function(n + "S")(tau) for n in ("d", "t", "E", "a"))
mapN = {de: dS - 3 * Hh * (1 + wv) * aC, th: tS + k**2 * aC, EE: ES, al: aS - A_ * aC}
mapS = {de: dS, th: tS, EE: ES, al: aS}
hprime_rule = {sp.Derivative(hS, tau): 2 * k**2 * aC - 6 * sp.Derivative(etaS, tau)}
d3_ok = True
d3_res = {}
for var in ("delta", "theta", "E", "alv"):
    # LHS: d/dtau of the Newtonian variable written via synchronous variables, using the synchronous equations
    rhsS = {v: SYS_S[n].subs(hprime_rule) for v, n in ((de, "delta"), (th, "theta"), (EE, "E"), (al, "alv"))}
    vN = mapN[{"delta": de, "theta": th, "E": EE, "alv": al}[var]]
    dvN = Dt(vN)
    dvN = dvN.subs({sp.Derivative(dS, tau): rhsS[de].subs(mapS), sp.Derivative(tS, tau): rhsS[th].subs(mapS),
                    sp.Derivative(ES, tau): rhsS[EE].subs(mapS), sp.Derivative(aS, tau): rhsS[al].subs(mapS)})
    # RHS: Newtonian equation evaluated on mapped variables and mapped metric
    rN = SYS_N[var].subs({sp.Derivative(phN, tau): Dt(phi_m), sp.Derivative(psi, tau): Dt(psi_m)})
    rN = rN.subs({psi: psi_m, phN: phi_m}).subs(mapN)
    res = sp.cancel(sp.expand((dvN - rN).subs(hprime_rule).doit()))
    d3_res[var] = str(res)
    d3_ok = d3_ok and res == 0
check("D3_gauge", d3_ok, f"sync system + map = Newtonian system: residuals {d3_res}", "all 0")

# ---------------------------------------------------------------- IC: radiation era, synchronous gauge
P("== IC: adiabatic initial conditions (synchronous gauge, radiation era, leading order in k tau and om tau)")
# CLASS conventions: h = C (k tau)^2 with C = curvature_ini/2; eta = 2C[1 - (5+4fnu)(k tau)^2/(12(15+4fnu))]
# a = a1 tau (1 + om tau/4); H = 1/tau (1 + om tau/4 ...) -> leading: H = 1/tau, a' = a1, a'' = a1 om/2.
C, fnu, om, a1, I0, cc, ww = sp.symbols("C f_nu omega a_1 I_0 c_ad2 w", positive=True)
tt = sp.Symbol("t", positive=True)
hser = C * k**2 * tt**2
etaser = 2 * C * (1 - (5 + 4 * fnu) * k**2 * tt**2 / (12 * (15 + 4 * fnu)))
# frozen background coefficients (Cosh/Exp early times): Q const, w = c_ad2 = c const, K' = I0/a^3,
# K'' = K'/(Q c), K = w (Q K' - K) => K = w Q K'/(1+w); a = a1 t (leading), a' = a1, a'' = 0
abg = a1 * tt
bgv = {A_: abg, Ap: a1, App: 0, Appp: 0, k1: I0 / abg**3, k2: I0 / abg**3 / (Qs * cc),
       k0: ww * Qs * I0 / abg**3 / (1 + ww)}
N_ORD = 8
dco = sp.symbols(f"d0:{N_ORD}")
tco = sp.symbols(f"t0:{N_ORD}")
eco = sp.symbols(f"e0:{N_ORD}")
aco = sp.symbols(f"q0:{N_ORD}")
dser = sum(dco[i] * tt**i for i in range(N_ORD))
tser = sum(tco[i] * tt**i for i in range(N_ORD))
eser = sum(eco[i] * tt**i for i in range(N_ORD))
aser = sum(aco[i] * tt**i for i in range(N_ORD))
serv = {de: dser, th: tser, EE: eser, al: aser}


def ic_eqs(SYS, extra):
    out = {}
    for n_, v_ in (("delta", de), ("theta", th), ("E", EE), ("alv", al)):
        lhs = sp.diff(serv[v_], tt)
        rhs = SYS[n_]
        rhs = rhs.subs({sp.Derivative(hS, tau): sp.diff(hser, tt), sp.Derivative(etaS, tau): sp.diff(etaser, tt)})
        rhs = rhs.subs(extra).subs({hS: hser, etaS: etaser}).subs(serv).subs(bgv).subs(tau, tt)
        out[n_] = sp.expand(lhs - rhs)
    return out


t1 = time.time()
eqs_ic = ic_eqs(SYS_S, {})
P(f"  series equations built ({time.time()-t1:.1f}s)")
# Solve order by order. Regular adiabatic solution: no homogeneous vector modes (alpha, E start at the particular
# solution), delta(0) = theta(0) = 0 (no isocurvature), lowest powers fixed by the metric source.
unk = list(dco) + list(tco) + list(eco) + list(aco)
# collect coefficients of t^n for n up to N_ORD-2 (truncation)
def tpow_terms(e):
    """list of (power of t, coefficient) for a rational expression whose denominator is a monomial in t."""
    if e == 0:
        return []
    num, den = sp.fraction(sp.cancel(sp.together(e)))
    pd = sp.Poly(den, tt)
    assert len(pd.terms()) == 1, f"denominator not a monomial in t: {den}"
    (dp_,), dc = pd.terms()[0]
    pn = sp.Poly(sp.expand(num), tt)
    return [(pw - dp_, sp.expand(cf / dc)) for (pw,), cf in pn.terms() if cf != 0]


byp = {}
for n_, e_ in eqs_ic.items():
    for pw, cf in tpow_terms(e_):
        if pw <= N_ORD - 3:
            byp.setdefault(pw, []).append(cf)
s_ic = {dco[0]: 0, aco[0]: 0}     # adiabatic: no delta isocurvature constant, no constant vector mode
free_set_zero = []
icok = True
for pw in sorted(byp):
    eqp = [sp.expand(e_.subs(s_ic)) for e_ in byp[pw]]
    eqp = [e_ for e_ in eqp if e_ != 0]
    if not eqp:
        continue
    unk_p = sorted({u for e_ in eqp for u in e_.free_symbols if u in unk}, key=str)
    sol_p = sp.solve(eqp, unk_p, dict=True)
    if len(sol_p) != 1:
        icok = False
        P(f"  IC: no unique solution at power {pw}: {eqp}")
        break
    for u, v in sol_p[0].items():
        s_ic[u] = sp.factor(v)
    # any unknown that is still free and of degree <= pw + 1 is a homogeneous mode: set to 0 (adiabatic choice)
    for u in unk_p:
        if u not in s_ic:
            deg = int(str(u)[1:])
            if deg <= pw + 1:
                s_ic[u] = 0
                free_set_zero.append(str(u))
    s_ic = {u: sp.factor(sp.expand(v.subs(s_ic))) if v != 0 else 0 for u, v in s_ic.items()}
P(f"  IC solve order by order: ok={icok}; free coefficients set to 0 (homogeneous modes): {free_set_zero} "
  f"({time.time()-t1:.1f}s)")
RES["IC_free_set_zero"] = free_set_zero


def lead(ser, co):
    terms = [(i, sp.factor(s_ic.get(co[i], co[i]))) for i in range(N_ORD)]
    nz = [(i, c_) for i, c_ in terms if c_ != 0]
    return nz[:2]


def lead_term(co):
    for i in range(N_ORD):
        c_ = s_ic.get(co[i], 0)
        if c_ != 0:
            return c_ * tt**i
    return 0


IC = {"delta": lead(dser, dco), "theta": lead(tser, tco), "E": lead(eser, eco), "alpha": lead(aser, aco)}
for n_, v_ in IC.items():
    P(f"  {n_}: " + "; ".join(f"t^{i}: {c_}" for i, c_ in v_))
RES["IC_sync_leading"] = {n_: [[i, str(c_)] for i, c_ in v_] for n_, v_ in IC.items()}
# IC1: substitute the truncated series (leading + next) back: residual starts >= 1 order above each equation's
# leading term
ic1_ok = icok
ic1_info = {}
if icok:
    trunc_ser = {}
    for v_, co in ((de, dco), (th, tco), (EE, eco), (al, aco)):
        trunc_ser[v_] = lead_term(co)
    for n_, v_ in (("delta", de), ("theta", th), ("E", EE), ("alv", al)):
        lhs = sp.diff(trunc_ser[v_], tt)
        rhs = SYS_S[n_].subs({sp.Derivative(hS, tau): sp.diff(hser, tt),
                              sp.Derivative(etaS, tau): sp.diff(etaser, tt)})
        rhs = rhs.subs({hS: hser, etaS: etaser}).subs(trunc_ser).subs(bgv).subs(tau, tt)
        r = sp.expand(sp.cancel(lhs - rhs))
        ltm = sp.expand(lhs)
        rmin = min(pw for pw, cf in tpow_terms(r)) if r != 0 else 99
        lmin = min(pw for pw, cf in tpow_terms(ltm)) if ltm != 0 else None
        ic1_info[n_] = {"residual_lowest_power": rmin, "lhs_lowest_power": lmin}
        if lmin is not None and rmin <= lmin:
            ic1_ok = False
check("IC1_series", ic1_ok, f"leading-term IC (as coded in CLASS): residual lowest power vs leading power per equation: {ic1_info}",
      "residual power > leading power")
# IC2: dust limit c = w = 0
d_lead = sp.expand(lead_term(dco).subs({cc: 0, ww: 0}))
t_lead = sp.expand(lead_term(tco).subs({cc: 0, ww: 0}))
e_lead = sp.expand(lead_term(eco).subs({cc: 0, ww: 0}))
a_lead = sp.expand(lead_term(aco).subs({cc: 0, ww: 0}))
dg_class = -sp.Rational(2, 3) * C * k**2 * tt**2       # CLASS delta_g leading (= -ktau^2/3 curvature_ini)
ic2 = (sp.expand(d_lead - sp.Rational(3, 4) * dg_class) == 0 and t_lead == 0 and e_lead == 0 and a_lead == 0)
check("IC2_dust", ic2, f"dust limit: delta = {d_lead}, theta = {t_lead}, E = {e_lead}, alpha = {a_lead}",
      "delta = 3/4 delta_g = -C (k t)^2/2, theta = E = alpha = 0")
# generic: delta = (1+w) 3/4 delta_g ; theta = CLASS fld formula with cs2 = c (for w = c)
fld_th = -k * (k * tt)**3 / 4 * cc / (4 - 6 * ww + 3 * cc) * 2 * C
th_lead = sum(s_ic.get(tco[i], 0) * tt**i for i in range(4))
RES["IC_theta_vs_fld_formula_w_eq_c"] = str(sp.simplify((th_lead - fld_th).subs(ww, cc)))
P(f"  theta leading minus CLASS fld formula (w = c_s^2 = c): {sp.simplify((th_lead - fld_th).subs(ww, cc))}")

# IC3: Newtonian IC from the D3 map satisfies the Newtonian equations at the same order
aCser = (sp.diff(hser, tt) + 6 * sp.diff(etaser, tt)) / (2 * k**2)
ic3_ok = icok
ic3_info = {}
if icok:
    Sser = {dS: lead_term(dco), tS: lead_term(tco), ES: lead_term(eco), aS: lead_term(aco)}
    Hser = 1 / tt
    Nser = {de: Sser[dS] - 3 * Hser * (1 + ww) * aCser, th: Sser[tS] + k**2 * aCser, EE: Sser[ES],
            al: Sser[aS] - abg * aCser}
    psis = sp.diff(aCser, tt) + Hser * aCser
    phis = etaser - Hser * aCser
    # frozen coefficients are self-consistent only for w = c_ad2 (w' = 3H(1+w)(w - c_ad2)); both sets obey it
    PSETS = [{C: sp.Rational(1, 2), k: sp.Rational(3, 100), I0: sp.Rational(4, 10**7), Qs: sp.Rational(1, 10),
              a1: sp.Rational(1, 10**4), KB: sp.Rational(1, 2), cc: sp.Rational(1, 10**3), ww: sp.Rational(1, 10**3),
              fnu: sp.Rational(41, 100), lamc: 0},
             {C: sp.Rational(-3, 7), k: sp.Rational(11, 10), I0: sp.Rational(5, 3), Qs: sp.Rational(7, 5),
              a1: sp.Rational(2, 9), KB: sp.Rational(1, 10), cc: sp.Rational(1, 7), ww: sp.Rational(1, 7),
              fnu: sp.Rational(3, 10), lamc: sp.Rational(2, 3)}]
    for n_, v_ in (("delta", de), ("theta", th), ("E", EE), ("alv", al)):
        rmins, lmins = [], []
        for ps in PSETS:
            lhs = sp.diff(Nser[v_].subs(ps), tt)
            rhs = SYS_N[n_].subs({sp.Derivative(phN, tau): sp.diff(phis, tt),
                                  sp.Derivative(psi, tau): sp.diff(psis, tt)})
            rhs = rhs.subs({phN: phis, psi: psis}).subs(Nser).subs(bgv).subs(tau, tt).subs(ps)
            r = sp.cancel(sp.together(lhs - rhs))
            rmins.append(min(pw for pw, cf in tpow_terms(r)) if r != 0 else 99)
            lmins.append(min(pw for pw, cf in tpow_terms(lhs)) if lhs != 0 else None)
        ic3_info[n_] = {"residual_lowest_power": rmins, "lhs_lowest_power": lmins}
        for rm, lm in zip(rmins, lmins):
            if lm is not None and rm <= lm:
                ic3_ok = False
check("IC3_newtonian", ic3_ok, f"Newtonian IC via the D3 map (2 exact rational parameter sets): {ic3_info}", "residual power > leading power")

# ---------------------------------------------------------------- D5: compact forms coded in C equal the derived ones
# chi = phi + Q alpha, phi = a Q theta/k^2, gam = ca2 (rho_hat delta + (k/a)^2 [K_B E + (2-K_B) chi])/K',
# dp/rho = K' gam / rho_hat, E' = -H E + (a/K_B){K' chi - (2-K_B)[gam + (H/a + (1+lam_c) Q) chi - 3 ca2 (H/a) Q alpha]}
rhoh = Qs * k1 - k0
ca2s = k1 / (Qs * k2)
chi_c = A_ * Qs * th / k**2 + Qs * al
gam_c = ca2s * (rhoh * de + k**2 / A_**2 * (KB * EE + (2 - KB) * chi_c)) / k1
Hh_ = Ap / A_
Ep_c = -Hh_ * EE + A_ / KB * (k1 * chi_c - (2 - KB) * (gam_c + (Hh_ / A_ + (1 + lamc) * Qs) * chi_c
                                                     - 3 * ca2s * Hh_ / A_ * Qs * al))
dpr_c = k1 * gam_c / rhoh
d5 = {}
for gname, SYS, DPR in (("sync", SYS_S, DPR_S), ("newt", SYS_N, DPR_N)):
    d5[gname] = (str(sp.cancel(sp.expand(SYS["E"] - Ep_c))), str(sp.cancel(sp.expand(DPR - dpr_c))))
check("D5_cform", all(v == ("0", "0") for v in d5.values()),
      f"C-form E' and dp/rho minus derived (sync, newt): {d5}", "all 0")
# D6: evolution variable chi = phi + Q alpha (gauge-invariant) in place of alpha; with Q alpha = chi - a Q theta/k^2:
#   chi' = a (gam + Q E) - 3 H ca2 (chi - a Q theta/k^2)
#   E'   = -H E + (a/K_B){K' chi - (2-K_B)[gam + (H/a + (1+lam_c) Q) chi - 3 ca2 (H/a)(chi - a Q theta/k^2)]}
CH = sp.Symbol("CHI")
gam_x = ca2s * (rhoh * de + k**2 / A_**2 * (KB * EE + (2 - KB) * CH)) / k1
chip_x = A_ * (gam_x + Qs * EE) - 3 * Hh_ * ca2s * (CH - A_ * Qs * th / k**2)
Ep_x = -Hh_ * EE + A_ / KB * (k1 * CH - (2 - KB) * (gam_x + (Hh_ / A_ + (1 + lamc) * Qs) * CH
                                                    - 3 * ca2s * Hh_ / A_ * (CH - A_ * Qs * th / k**2)))
d6 = {}
for gname, SYS in (("sync", SYS_S), ("newt", SYS_N)):
    chi_e = A_ * Qs * th / k**2 + Qs * al
    dchi = sp.expand(Dt(chi_e).subs({sp.Derivative(th, tau): SYS["theta"], sp.Derivative(al, tau): SYS["alv"]}))
    r1 = sp.cancel(sp.expand(dchi - chip_x.subs(CH, chi_e)))
    r2 = sp.cancel(sp.expand(SYS["E"] - Ep_x.subs(CH, chi_e)))
    d6[gname] = (str(r1), str(r2))
check("D6_chi_form", all(v == ("0", "0") for v in d6.values()),
      f"chi' and E' in (delta, theta, E, chi) minus derived (sync, newt): {d6}", "all 0; no metric term")
# C-form ICs (synchronous; C = curvature_ini/2, c = c_ad2, a1 = a/tau, I0 = K' a^3)
ic_c = {dco: -(1 + ww) / (2 + 3 * cc - 3 * ww) * C * k**2 * tt**2,
        tco: -cc * k**4 * C * tt**3 / ((4 - 3 * cc) * (2 + 3 * cc - 3 * ww)),
        eco: -C * cc * Qs * I0 * k**2 * tt**3 / (4 * KB * a1 * (4 - 3 * cc) * (2 + 3 * cc - 3 * ww)),
        aco: -C * cc * Qs * I0 * k**2 * tt**5 / (20 * KB * (4 - 3 * cc) * (2 + 3 * cc - 3 * ww))}
icc = {str(co[0])[0]: str(sp.simplify(lead_term(co) - v)) for co, v in ic_c.items()}
check("IC_cform", all(v == "0" for v in icc.values()), f"C-form leading ICs minus series: {icc}", "all 0")

# ---------------------------------------------------------------- export the C expressions for the patch
cv = {de: sp.Symbol("delta"), th: sp.Symbol("theta"), EE: sp.Symbol("E"), al: sp.Symbol("alv"),
      sp.Derivative(hS, tau): sp.Symbol("h_prime"), sp.Derivative(etaS, tau): sp.Symbol("eta_prime"),
      sp.Derivative(phN, tau): sp.Symbol("phi_prime"), psi: sp.Symbol("psi"), phN: sp.Symbol("phi"),
      hS: sp.Symbol("h_sync"), etaS: sp.Symbol("eta_sync")}
cmap = {A_: sp.Symbol("a"), Ap: sp.Symbol("a_prime"), Qs: sp.Symbol("Qb"), k0: sp.Symbol("Kz"),
        k1: sp.Symbol("Kp"), k2: sp.Symbol("Kpp"), KB: sp.Symbol("K_B"), lamc: sp.Symbol("lambda_c")}
EXPORT = {}
for gname, SYS, DPR, AUX in (("synchronous", SYS_S, DPR_S, AUX_S), ("newtonian", SYS_N, DPR_N, AUX_N)):
    d = {}
    for n_ in ("E", "alv"):
        d[n_ + "_prime"] = str(sp.collect(sp.expand(SYS[n_].subs(cv).subs(cmap)), [sp.Symbol("delta"),
                               sp.Symbol("theta"), sp.Symbol("E"), sp.Symbol("alv")]))
    d["dp_over_rho"] = str(sp.expand(DPR.subs(cv).subs(cmap)))
    EXPORT[gname] = d
EXPORT["note"] = ("Kz, Kp, Kpp = K, K', K'' at Qbar (CLASS units Mpc^-2, Mpc^-1, 1); a_prime = da/dtau; "
                  "rho_hat = Qb*Kp - Kz = 8piG~ rho_aest; delta' and theta' are the standard fluid equations with "
                  "w = Kz/rho_hat, c_ad2 = Kp/(Qb Kpp), dp/rho as exported; sigma = 0.")
json.dump(EXPORT, open(os.path.join(HERE, f"c7_aest_equations{TAG}.json"), "w"), indent=1)
P("  exported E', alpha', dp/rho for both gauges -> c7_aest_equations.json")
for gname in ("synchronous", "newtonian"):
    for kk, vv in EXPORT[gname].items():
        P(f"  [{gname}] {kk} = {vv}")

RES["elapsed_s"] = round(time.time() - T0, 1)
json.dump(RES, open(os.path.join(HERE, f"c7_derive_results{TAG}.json"), "w"), indent=1)
P(f"C7_DERIVE COMPLETE: {NPASS}/{NCHK} checks PASS.")
OUT.close()
raise SystemExit(0 if NPASS == NCHK else 1)
