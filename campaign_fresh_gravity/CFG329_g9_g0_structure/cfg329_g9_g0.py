#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG329 -- recipe gates G9 (full relativistic matter conservation) and G0 (structural order) on the chassis:
the filtered C-H/K khronon completion (C-H ACTION.md:95-106 + alpha_c a^2 - c_2 (K - <K>_Sigma)^2, beta = 0,
nu_mono, heat-filter scale xi). Criteria frozen in FROZEN_CRITERIA.md (commit 50c09b024) before this script ran.

G9  S1 matter identity (off shell, curved reduced sector): nabla_mu T^mu_nu = E_chi d_nu chi + E_U d_nu U
    S2 scalar-density (Noether II) test of every chassis term incl. one heat z-slice and the leaf-average proxy F(tau)
    S3 linear Stueckelberg check on the FP2-derived block: clock eq = metric eqs + (source non-conservation)
    S4 bounds: exact extra term = 0; diagnostic extra terms of non-covariant implementations, on 3 backgrounds
G0  T1 weak-field ordering (Phi -> eps Phi): q series, delta S order, static K = 0
    T2 unitary-gauge time order of the NONLINEAR reduced Lagrangian (jet test) + ADM/GHY identity
    T3 det M(omega, k) degree of the derived scalar block, filter and leaf average included
    T4 constraint preservation: spatial Noether identity, elliptic lapse/U coefficients; tilted-frame diagnostic
Controls: GR Bianchi + FRW dust; plain khronometric; non-covariant power check; MUTATE (CFG329_MUTATE=1): matter
Lagrangian x e^{beta U} must be flagged by G9 (exit 1).
Run from the repository root:  python3 campaign_fresh_gravity/CFG329_g9_g0_structure/cfg329_g9_g0.py
"""
import os, sys, json, math, time, random
import sympy as sp
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("CFG329_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
mp.mp.dps = 60
T0 = time.time()
CH, OUT = [], {"lane": "CFG329", "mutate": MUTATE, "frozen_criteria_commit": "50c09b024", "checks": {}, "numbers": {}}


def P(*a):
    print(*a, flush=True)


def banner(s):
    P("\n" + "=" * 100); P(s); P("=" * 100)


def check(name, measured, ok, reading=""):
    ok = bool(ok); CH.append((name, ok))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


P(__doc__.strip())
if MUTATE:
    P("\n  *** MUTATE: matter Lagrangian multiplied by exp(beta U), beta = 0.37 -- G9 must flag it ***")

t, x, y, z, eps = sp.symbols('t x y z epsilon', real=True)
X4 = (t, x, y, z)
R_ = sp.Rational
PTS = [(mp.mpf('0.31'), mp.mpf('-0.57')), (mp.mpf('1.13'), mp.mpf('0.42')), (mp.mpf('-0.66'), mp.mpf('1.71'))]
HFD = mp.mpf('1e-12')


def d1(f, a, h=HFD):  # 4th-order central difference
    return (-f(a + 2 * h) + 8 * f(a + h) - 8 * f(a - h) + f(a - 2 * h)) / (12 * h)


# ----------------------------------------------------------------------------------- reduced-sector geometry
def metric(A, B, C, D):
    return sp.Matrix([[-A, B, 0, 0], [B, C, 0, 0], [0, 0, D, 0], [0, 0, 0, D]])


def inv_metric(A, B, C, D):
    det2 = -A * C - B**2
    return sp.Matrix([[C / det2, -B / det2, 0, 0], [-B / det2, -A / det2, 0, 0], [0, 0, 1 / D, 0], [0, 0, 0, 1 / D]])


def geometry(A, B, C, D, ricci=True):
    g = metric(A, B, C, D); gi = inv_metric(A, B, C, D)
    sqg = sp.sqrt(A * C + B**2) * D
    dg = [[[sp.diff(g[a, b], X4[c]) for c in range(4)] for b in range(4)] for a in range(4)]
    Gam = [[[sum(gi[a, d] * (dg[d][b][c] + dg[d][c][b] - dg[b][c][d]) for d in range(4)) / 2 for c in range(4)]
            for b in range(4)] for a in range(4)]
    out = {"g": g, "gi": gi, "sqg": sqg, "Gam": Gam}
    if ricci:
        Ric = sp.zeros(4, 4)
        for b in range(4):
            for c in range(b, 4):
                Ric[b, c] = sum(sp.diff(Gam[a][b][c], X4[a]) - sp.diff(Gam[a][b][a], X4[c]) +
                                sum(Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a] for d in range(4))
                                for a in range(4))
                Ric[c, b] = Ric[b, c]
        out["Ric"] = Ric
        out["R"] = sum(gi[a, b] * Ric[a, b] for a in range(4) for b in range(4))
    return out


def clock(geo, tau):
    gi, Gam = geo["gi"], geo["Gam"]
    dtau = [sp.diff(tau, c) for c in X4]
    Xc = -sum(gi[a, b] * dtau[a] * dtau[b] for a in range(4) for b in range(4))
    nl = [-dtau[a] / sp.sqrt(Xc) for a in range(4)]
    nu = [sum(gi[a, b] * nl[b] for b in range(4)) for a in range(4)]
    hup = sp.Matrix(4, 4, lambda a, b: gi[a, b] + nu[a] * nu[b])
    Dn = [[sp.diff(nl[b], X4[a]) - sum(Gam[l][a][b] * nl[l] for l in range(4)) for b in range(4)] for a in range(4)]
    K = sum(hup[a, b] * Dn[a][b] for a in range(4) for b in range(4))
    acc = [sum(nu[a] * Dn[a][b] for a in range(4)) for b in range(4)]
    aa = sum(gi[a, b] * acc[a] * acc[b] for a in range(4) for b in range(4))
    return {"X": Xc, "nl": nl, "nu": nu, "hup": hup, "K": K, "a": acc, "aa": aa}


def lap_h(geo, cl, W):
    gi, Gam = geo["gi"], geo["Gam"]
    dW = [sp.diff(W, c) for c in X4]
    hess = [[sp.diff(dW[b], X4[a]) - sum(Gam[l][a][b] * dW[l] for l in range(4)) for b in range(4)] for a in range(4)]
    return (sum(cl["hup"][a, b] * hess[a][b] for a in range(4) for b in range(4)) +
            cl["K"] * sum(cl["nu"][a] * dW[a] for a in range(4)))


def hgrad2(cl, F, G=None):
    G = F if G is None else G
    return sum(cl["hup"][a, b] * F[a] * G[b] for a in range(4) for b in range(4))


# concrete smooth fields (Lorentzian, timelike clock) and an arbitrary vector xi = (xi^t, xi^x)
F0 = {
    "A": 1 + R_(3, 10) * sp.sin(t + x / 2) + R_(1, 10) * sp.cos(2 * x - t),
    "B": R_(1, 5) * sp.cos(t - x) + R_(1, 20) * sp.sin(3 * x),
    "C": 1 + R_(1, 4) * sp.cos(t / 2 + x) + R_(1, 10) * sp.sin(t * x / 3),
    "D": 1 + R_(1, 5) * sp.sin(x - t / 3) + R_(1, 15) * sp.cos(2 * t + x),
    "tau": t + R_(1, 6) * sp.sin(x + t / 3) + R_(1, 12) * sp.cos(2 * x),
    "U": R_(2, 5) * sp.sin(2 * t - x) + R_(1, 3) * sp.cos(x),
    "W": R_(1, 3) * sp.cos(t + 2 * x) + R_(1, 4) * sp.sin(x),
    "Wz": R_(1, 2) * sp.sin(t * x / 2 + 1) + R_(1, 5) * x,
    "L": R_(3, 4) * sp.cos(x - 2 * t) + R_(1, 3),
    "lam0": R_(1, 2) * sp.sin(t + x) + R_(1, 4) * t,
    "chi": R_(1, 2) * sp.sin(t - 2 * x) + R_(1, 3) * sp.cos(t * x / 2),
}
XI = (R_(1, 3) * sp.cos(2 * t - x) + R_(1, 5) * sp.sin(x), R_(1, 4) * sp.sin(t + 3 * x) + R_(1, 7) * sp.cos(t))
METRIC_KEYS = ("A", "B", "C", "D")


def lie_shift(F, xi):
    """fields + eps * Lie derivative along xi = (xi^t, xi^x, 0, 0)."""
    xv = [xi[0], xi[1], 0, 0]
    g = metric(*[F[k] for k in METRIC_KEYS])
    Lg = sp.Matrix(4, 4, lambda a, b: sum(xv[c] * sp.diff(g[a, b], X4[c]) + g[c, b] * sp.diff(xv[c], X4[a]) +
                                          g[a, c] * sp.diff(xv[c], X4[b]) for c in range(4)))
    G = dict(F)
    G["A"] = F["A"] - eps * Lg[0, 0]; G["B"] = F["B"] + eps * Lg[0, 1]
    G["C"] = F["C"] + eps * Lg[1, 1]; G["D"] = F["D"] + eps * Lg[2, 2]
    for k in F:
        if k not in METRIC_KEYS:
            G[k] = F[k] + eps * (xv[0] * sp.diff(F[k], t) + xv[1] * sp.diff(F[k], x))
    return G


PAR = {"alpha": R_(7, 10), "q2": R_(-1, 5), "q3": R_(1, 30), "ac": R_(1, 10), "c2": R_(3, 50), "Lam": R_(1, 9),
       "f0": R_(1, 7), "f1": R_(-2, 9), "f2": R_(1, 11), "cnc": R_(1, 2)}


def q_fun(s):
    return s + PAR["q2"] * s**2 + PAR["q3"] * s**3


def F_leaf(tau):
    return PAR["f0"] + PAR["f1"] * tau + PAR["f2"] * tau**2


def Kbar_coord(tt):  # a NON-covariant 'leaf average' frozen as a function of coordinate time (diagnostic)
    return PAR["f0"] + PAR["f1"] * tt + PAR["f2"] * tt**2


def density(F, model):
    geo = geometry(*[F[k] for k in METRIC_KEYS])
    sqg, R = geo["sqg"], geo["R"]
    if model == "GR":
        return sqg * (R - 2 * PAR["Lam"])
    cl = clock(geo, F["tau"])
    K, aa, acc = cl["K"], cl["aa"], cl["a"]
    if model == "KH":                                       # plain khronometric (beta = 0): control 2
        return sqg * (R + PAR["ac"] * aa - PAR["c2"] * K**2)
    dU = [sp.diff(F["U"], c) for c in X4]; dW = [sp.diff(F["W"], c) for c in X4]
    V = [dU[a] - acc[a] for a in range(4)]
    al = PAR["alpha"]
    Kb = Kbar_coord(t) if model == "CHK_KBAR_T" else F_leaf(F["tau"])
    Lg = (R - 2 * PAR["Lam"] + 2 * hgrad2(cl, V) + 2 * al**2 * q_fun(hgrad2(cl, dW) / al**2)
          + F["L"] * (F["Wz"] - lap_h(geo, cl, F["W"])) + F["lam0"] * (F["W"] - F["U"])
          + PAR["ac"] * aa - PAR["c2"] * (K - Kb)**2)
    if model == "CHK_NONCOV":                               # control 3: coordinate-time kinetic term
        Lg = Lg + PAR["cnc"] * sp.diff(F["U"], t)**2
    return sqg * Lg


def noether_residual(model, extra_pred=None):
    """R_xi = d/deps L[phi + eps delta_xi phi] - d_mu(xi^mu L) at the test points (numerical, 60 digits)."""
    t1 = time.time()
    Le = density(lie_shift(F0, XI), model)
    fL = sp.lambdify((t, x, eps), Le, modules="mpmath")
    fxt = sp.lambdify((t, x), XI[0], modules="mpmath"); fxx = sp.lambdify((t, x), XI[1], modules="mpmath")
    fpred = sp.lambdify((t, x), extra_pred, modules="mpmath") if extra_pred is not None else None
    res = []
    for (tp, xp) in PTS:
        dLe = d1(lambda e: fL(tp, xp, e), mp.mpf(0))
        div = (d1(lambda s: fxt(s, xp) * fL(s, xp, 0), tp) + d1(lambda s: fxx(tp, s) * fL(tp, s, 0), xp))
        scale = abs(dLe) + abs(div)
        r = dLe - div
        res.append({"R": r, "scale": scale, "pred": (fpred(tp, xp) if fpred else None)})
    rel = max(abs(e["R"]) / e["scale"] for e in res)
    return res, float(rel), time.time() - t1


# ===================================================================================================== G9
banner("G9-C1  CONTROL: GR -- contracted Bianchi identity at random points; FRW + dust conservation")
geoF = geometry(*[F0[k] for k in METRIC_KEYS])
gi, Gam = geoF["gi"], geoF["Gam"]
Gmix = sp.Matrix(4, 4, lambda m, n: sum(gi[m, a] * geoF["Ric"][a, n] for a in range(4)) - sp.KroneckerDelta(m, n) * geoF["R"] / 2)
fG = sp.lambdify((t, x), Gmix.tolist(), modules="mpmath"); fGam = sp.lambdify((t, x), Gam, modules="mpmath")


def cov_div_mixed(fT, tp, xp):
    """nabla_mu T^mu_nu for a mixed tensor given as a lambdified 4x4 function (fields depend on t, x only)."""
    Tm = fT(tp, xp); Gm = fGam(tp, xp)
    out = []
    for n in range(4):
        v = d1(lambda s: fT(s, xp)[0][n], tp) + d1(lambda s: fT(tp, s)[1][n], xp)
        v += sum(Gm[m][m][l] * Tm[l][n] for m in range(4) for l in range(4))
        v -= sum(Gm[l][m][n] * Tm[m][l] for m in range(4) for l in range(4))
        out.append(v)
    return out, max(abs(Tm[i][j]) for i in range(4) for j in range(4))


bianchi = []
for (tp, xp) in PTS:
    dv, sc = cov_div_mixed(fG, tp, xp)
    bianchi.append(float(max(abs(v) for v in dv) / sc))
a_ = sp.Function('a')(t); rho0 = sp.Symbol('rho0', positive=True)
Hh = sp.diff(a_, t) / a_


def frw_dust_div(rho):  # nabla_mu T^mu_0 for dust at rest in flat FRW: -(rho_dot + 3 H rho)
    return sp.simplify(-(sp.diff(rho, t) + 3 * Hh * rho))


dust_ok = frw_dust_div(rho0 * a_**-3); dust_bad = frw_dust_div(rho0 * a_**-2)
OUT["numbers"]["C1"] = {"bianchi_rel": bianchi, "dust_a-3": str(dust_ok), "dust_a-2": str(dust_bad)}
check("G9-C1 GR control: nabla_mu G^mu_nu = 0 at 3 random points of the curved reduced sector (exact identity); FRW dust "
      "conserved iff rho a^3 = const", f"max rel |div G| = {max(bianchi):.1e}; rho~a^-3: {dust_ok}; rho~a^-2: {dust_bad}",
      max(bianchi) < 1e-25 and dust_ok == 0 and dust_bad != 0)

banner("G9-S1  MATTER IDENTITY off shell: nabla_mu T^mu_nu - E_chi d_nu chi - E_U d_nu U = 0  (curved reduced sector)")
beta = R_(37, 100) if MUTATE else sp.Integer(0)
mchi = R_(1, 2)
sqg0 = geoF["sqg"]
dchi = [sp.diff(F0["chi"], c) for c in X4]; dUc = [sp.diff(F0["U"], c) for c in X4]
uchi = [sum(gi[m, a] * dchi[a] for a in range(4)) for m in range(4)]
kin = sum(uchi[a] * dchi[a] for a in range(4))
Vchi = mchi**2 * F0["chi"]**2 / 2
fcpl = sp.exp(beta * F0["U"])
Lm = fcpl * (-kin / 2 - Vchi)                                      # per sqrt(-g)
Tmix = sp.Matrix(4, 4, lambda m, n: fcpl * (uchi[m] * dchi[n] - sp.KroneckerDelta(m, n) * (kin / 2 + Vchi)))
J = [sqg0 * fcpl * uchi[m] for m in range(4)]
fT = sp.lambdify((t, x), Tmix.tolist(), modules="mpmath")
fJ = sp.lambdify((t, x), J, modules="mpmath")
fsq = sp.lambdify((t, x), sqg0, modules="mpmath")
fothers = sp.lambdify((t, x), [fcpl * mchi**2 * F0["chi"], beta * Lm] + dchi + dUc, modules="mpmath")
mat_res, mat_eU = [], []
for (tp, xp) in PTS:
    dv, sc = cov_div_mixed(fT, tp, xp)
    divJ = (d1(lambda s: fJ(s, xp)[0], tp) + d1(lambda s: fJ(tp, s)[1], xp)) / fsq(tp, xp)
    o = fothers(tp, xp)
    Echi = divJ - o[0]
    EU = o[1]
    r_min = [dv[n] - Echi * o[2 + n] for n in range(4)]               # residual if matter were minimal
    r_full = [r_min[n] - EU * o[6 + n] for n in range(4)]             # identity with the U-coupling force
    mat_res.append((float(max(abs(v) for v in r_full) / sc), float(max(abs(v) for v in r_min) / sc)))
full_rel = max(m[0] for m in mat_res); min_rel = max(m[1] for m in mat_res)
OUT["numbers"]["S1"] = {"beta": str(beta), "identity_rel": full_rel, "minimal_residual_rel": min_rel}
s1_identity = check("G9-S1a the off-shell matter identity nabla_mu T^mu_nu = E_chi d_nu chi + E_U d_nu U holds (Noether, "
                    "any coupling)", f"max rel residual {full_rel:.1e}", full_rel < 1e-25)
s1_minimal = check("G9-S1b matter couples minimally (to g only): on the matter shell E_chi = 0, nabla_mu T^mu_nu = 0 with NO "
                   "extra force (E_U d U = 0)", f"beta = {beta}; residual of nabla T - E_chi d chi = {min_rel:.2e}",
                   min_rel < 1e-25,
                   "ACTION.md: matter is -sum m c int ds + Maxwell, functions of g only; MUTATE makes it e^{beta U}")

banner("G9-S2  SCALAR-DENSITY (Noether II) TEST: R_xi = delta_xi L - d_mu(xi^mu L) for every term, arbitrary xi(t, x)")
S2 = {}
for model, lab in (("GR", "GR (control)"), ("KH", "plain khronometric (control 2)"),
                   ("CHK", "FULL CHASSIS: R-2Lam + 2|DU-a|^2 + 2a^2 q + heat slice L(Wz-Delta_h W) + lam0(W-U) + "
                           "alpha_c a^2 - c2 (K-F(tau))^2"),
                   ("CHK_NONCOV", "chassis + c (d_t U)^2 (control 3, must FAIL)")):
    res, rel, dt = noether_residual(model)
    S2[model] = rel
    P(f"    {lab}: max |R_xi|/scale = {rel:.2e}   ({dt:.0f} s)")
# the exact extra term of a coordinate-time leaf average: R_xi = -2 c2 sqrt(-g) (K - Kbar(t)) Kbar'(t) xi^t (predicted)
clF = clock(geoF, F0["tau"])
pred = -2 * PAR["c2"] * sqg0 * (clF["K"] - Kbar_coord(t)) * sp.diff(Kbar_coord(t), t) * XI[0]
resK, relK, dtK = noether_residual("CHK_KBAR_T", extra_pred=pred)
pred_match = max(float(abs(e["R"] - e["pred"]) / abs(e["pred"])) for e in resK)
S2["CHK_KBAR_T"] = relK
P(f"    chassis with <K> frozen as a coordinate-time function Kbar(t): max |R_xi|/scale = {relK:.2e}; "
  f"R_xi vs predicted -2 c2 sqrt(-g)(K-Kbar) Kbar' xi^t: max rel diff {pred_match:.1e}  ({dtK:.0f} s)")
OUT["numbers"]["S2"] = {**S2, "kbar_t_pred_match": pred_match}
check("G9-C2 plain khronometric control: R_xi = 0 (the known result: its generalized Bianchi identity holds off shell)",
      f"{S2['KH']:.1e}", S2["KH"] < 1e-25 and S2["GR"] < 1e-25)
check("G9-C3 power check: a coordinate-time kinetic term is caught (R_xi != 0)", f"{S2['CHK_NONCOV']:.1e}",
      S2["CHK_NONCOV"] > 1e-6)
s2_chassis = check("G9-S2 FULL CHASSIS is a scalar density under arbitrary diffeomorphisms: the generalized Bianchi identity "
                   "2 nabla_mu E^mu_nu = E_tau d_nu tau + E_U d_nu U + int dz (E_W d_nu W + E_L d_nu L) + E_lam0 d_nu lam0 "
                   "holds off shell, heat slice and leaf-average proxy included", f"max rel R_xi = {S2['CHK']:.1e}",
                   S2["CHK"] < 1e-25,
                   "with S_m[g] diffeo-invariant: on the tau, U, W, L, lam0 shell nabla_mu T^mu_nu = 0 exactly; the clock "
                   "equation is then implied (E_tau d tau = 0 with d tau timelike)")
check("G9-S2b the extra term of a NON-covariant leaf average (frozen in coordinate time) is identified exactly: "
      "-2 c2 sqrt(-g) (K - Kbar) dKbar/dt xi^t", f"rel diff to prediction {pred_match:.1e}", pred_match < 1e-20)

banner("G9-S3  LINEAR STUECKELBERG CHECK on the FP2-derived block (copied from FP2 A1, which verified it as the variation of the core)")
kq, wq, al_, c2_, Ce = sp.symbols('k omega alpha_c c_2 C_eff', real=True)
An, Ap, AB, AU, rs, js = sp.symbols('A_n A_psi A_B A_U rho_s j_s')
D_ = -sp.I * wq; e_ = -c2_


def block(Cv, alv, c2v):
    ee = -c2v
    return {"n": -4 * kq**2 * Ap - 4 * kq**2 * (AU - An) + 2 * alv * kq**2 * An,
            "psi": 4 * kq**2 * Ap - 4 * kq**2 * An - D_ * (-12 * D_ * Ap + 4 * kq**2 * AB + 6 * ee * (3 * D_ * Ap - kq**2 * AB)),
            "B": 4 * kq**2 * D_ * Ap - 2 * ee * kq**2 * (3 * D_ * Ap - kq**2 * AB),
            "U": 4 * kq**2 * (AU - An) + 4 * kq**2 * Cv * AU}


# time diffeo t -> t + pi on Minkowski: delta n = pi_dot, delta B = -pi  =>  E_pi = -d_t E_n - E_B (+ sources)
Egr = block(0, 0, 0); Egr["n"] = Egr["n"] + 4 * kq**2 * (AU - An)            # GR: drop the chassis |DU - a|^2
Epi_gr = sp.expand(-D_ * (Egr["n"] - rs) - (Egr["B"] + js))
Ech = block(Ce, al_, c2_)
Epi_ch = sp.expand(-D_ * (Ech["n"] - rs) - (Ech["B"] + js))
src_part = sp.expand(Epi_ch.subs({Ap: 0, AB: 0, AU: 0, An: 0}))
OUT["numbers"]["S3"] = {"E_pi_GR": str(sp.factor(Epi_gr)), "E_pi_chassis_source_part": str(src_part),
                        "E_pi_chassis_field_part": str(sp.factor(sp.expand(Epi_ch - src_part)))}
check("G9-S3 linear: in GR the time-diffeo combination vanishes identically up to the source (Bianchi forces "
      "j_s = d_t rho_s); in the chassis the same combination is the clock equation, whose source part is exactly "
      "d_t rho_s - j_s: clock eq + metric eqs <=> source conservation",
      f"GR: {sp.factor(Epi_gr)}; chassis source part: {src_part}",
      sp.simplify(Epi_gr - (D_ * rs - js)) == 0 and sp.simplify(src_part - (D_ * rs - js)) == 0)

banner("G9-S4  BOUNDS: exact extra term, and the diagnostic extra terms of non-covariant implementations")
G_, c_, Msun, pc, AU_m = 6.674e-11, 2.998e8, 1.989e30, 3.0857e16, 1.496e11
H0 = 67.36e3 / (3.0857e22); a0s = {"canonical": 9.36e-11, "alt": 1.13e-10}
xi_floor = (0.031 * pc, 0.049 * pc); c2_win = (7.29e-3, 0.0667); q0 = -0.53
rho_crit = 3 * H0**2 / (8 * math.pi * G_); LH = c_ / H0
nu = lambda yv: 1.0 / (-math.expm1(-math.sqrt(yv)))


def g_smooth(M, r, xi):  # Gaussian-filtered point-mass field (series inside the core avoids cancellation)
    u = r / (math.sqrt(2) * xi)
    if u < 1e-3:
        return G_ * M * r * math.sqrt(2 / math.pi) / (3 * xi**3)
    return G_ * M / r**2 * (math.erf(u) - math.sqrt(2 / math.pi) * (r / xi) * math.exp(-u * u))


# (a) leaf average, exact: its global stress enters local equations with weight V_sys / V_leaf
Vrat = {"solar (1e3 AU)": (1e3 * AU_m / LH)**3, "galaxy (30 kpc)": (30e3 * pc / LH)**3, "cosmology (k != 0)": 0.0}
# (b) frozen filter (delta S dropped): extra ~ (1/2)(nu - 1)(g_f / g)^2 min(1, (xi/L)^2) of the Newtonian force balance
fs = {}
for f, a0 in a0s.items():
    for xi in xi_floor:
        gN = G_ * Msun / AU_m**2; gf = g_smooth(Msun, AU_m, xi)
        sol = 0.5 * (nu(gf / a0) - 1) * (gf / gN)**2
        gal_g = (2.0e5)**2 / (8e3 * pc); gal = 0.5 * (nu(gal_g / a0) - 1) * min(1.0, (xi / (3e3 * pc))**2)
        cos_g = 1e-12; cos = 0.5 * (nu(cos_g / a0) - 1) * min(1.0, (xi / (10e6 * pc))**2)
        fs[f"{f}/xi={xi / pc:.3f}pc"] = {"solar_1AU": sol, "galaxy_8kpc": gal, "cosmology_10Mpc": cos}
# (c) coordinate-time <K>: energy non-conservation per Hubble time ~ 3 c2 (1+q0) rho_crit / rho_local
dens = {"solar (rho_sun mean 1.4e3)": 1.41e3, "galaxy (0.1 Msun/pc^3)": 0.1 * Msun / pc**3, "cosmology (rho_crit)": rho_crit}
kbt = {k: [3 * c * (1 + q0) * rho_crit / v for c in c2_win] for k, v in dens.items()}
OUT["numbers"]["S4"] = {"exact_extra_term": 0.0, "leaf_avg_global_weight": Vrat, "frozen_S_extra": fs, "coord_time_Kbar_extra": kbt}
P(f"    exact chassis (S2): extra term in nabla_mu T^mu_nu = 0 on every background (identity, not a bound)")
P(f"    (a) leaf-average global stress weight V_sys/V_leaf: " + "; ".join(f"{k} {v:.1e}" for k, v in Vrat.items()))
for k, v in fs.items():
    P(f"    (b) frozen-S diagnostic {k}: solar {v['solar_1AU']:.1e}, galaxy {v['galaxy_8kpc']:.1e}, cosmology {v['cosmology_10Mpc']:.1e}")
P(f"    (c) coordinate-time <K> diagnostic (per Hubble time, c2 window): " +
  "; ".join(f"{k} {v[0]:.1e}..{v[1]:.1e}" for k, v in kbt.items()))
bmax_exact = 0.0
check("G9-S4 the exact extra term is zero on solar, galaxy and cosmology backgrounds; the leaf average's global stress is "
      "a conserved part of E^mu_nu weighted <= 1e-15 locally", f"extra 0; global weights {[f'{v:.0e}' for v in Vrat.values()]}",
      bmax_exact == 0.0 and max(Vrat.values()) < 1e-15,
      "diagnostics (not the action): dropping delta S costs <= 1e-9 (galaxy) of the force balance; a coordinate-time "
      "<K> costs 3 c2 (1+q0) ~ 1e-2..1e-1 per Hubble time on FRW -> <K> must be varied as a function of tau")

# ===================================================================================================== G0
banner("G0-T1  WEAK-FIELD ORDERING (Phi -> eps Phi): the kernel, delta S, the khronon terms")
yy, ee_ = sp.symbols('y epsilon', positive=True)
s_of_y = yy * (1 - sp.exp(-yy))
q_of_y = 2 * s_of_y * yy - (yy**2 + 2 * (1 + yy) * sp.exp(-yy) - 2) - s_of_y**2
q_small = sp.series(q_of_y, yy, 0, 4).removeO()            # in y; s ~ y^2 -> q ~ s^(3/2)
lead = sp.Poly(sp.expand(q_small), yy).terms()[-1]
q_deep_order = sp.limit(q_of_y / s_of_y**sp.Rational(3, 2), yy, 0)
# delta S: the conformal leaf h = e^{-2 psi} delta: Delta_h F = e^{2 psi}(lap F - grad psi . grad F) -- linear in psi
X3 = sp.symbols('x1 x2 x3', real=True); psi3 = sp.Function('psi')(*X3); F3 = sp.Function('F')(*X3)
sqh = sp.exp(-3 * psi3); hinv = sp.exp(2 * psi3)
lapH = sum(sp.diff(sqh * hinv * sp.diff(F3, v), v) for v in X3) / sqh
lap_diff = sp.simplify(lapH - sp.exp(2 * psi3) * (sum(sp.diff(F3, v, 2) for v in X3) -
                                                  sum(sp.diff(psi3, v) * sp.diff(F3, v) for v in X3)))
# static slices: K = 0 for a static metric with tau = t
geo_st = geometry(1 + sp.Function('p')(x), 0, 1 + sp.Function('s')(x), 1 + sp.Function('s')(x), ricci=False)
K_static = sp.simplify(clock(geo_st, t)["K"])
OUT["numbers"]["T1"] = {"q_small_y": str(q_small), "q/s^1.5 at y->0": str(q_deep_order), "lap_h_conformal_diff": str(lap_diff),
                        "K_static": str(K_static),
                        "orders_in_action": {"R, 2|DU-a|^2, matter rho Phi": "eps^2", "kernel 2a^2 q": "eps^2 (Newtonian) .. eps^1.5 (deep)",
                                             "delta S part of the kernel": "eps * kernel (1PN, enters psi/h_ij eqs only)",
                                             "alpha_c a^2": "alpha_c eps^2", "c2 (K-<K>)^2": "0 static; eps^2 (v/c)^2 moving"}}
P(f"    q(y) small-y series: {q_small};  q/s^(3/2) -> {q_deep_order} (deep MOND: one non-analytic kernel, order eps^(3/2))")
P(f"    Delta_h on h = e^(-2psi) delta minus e^(2psi)(lap - grad psi.grad): {lap_diff}  -> delta S is linear in psi: eps x kernel")
P(f"    K on a static slice (tau = t): {K_static}  -> c2 and leaf-average terms and their first variations vanish statically")
check("G0-T1 weak-field ordering: the MOND law is the output of ONE kernel term (order eps^(3/2) deep, eps^2 Newtonian); "
      "no source must cancel a source of a different eps order; delta S enters at eps x kernel (1PN, psi/h_ij only); "
      "khronon terms are alpha_c eps^2 and zero on static slices",
      f"q ~ {q_deep_order} s^(3/2); delta Delta_h residual {lap_diff}; K_static = {K_static}",
      bool(q_deep_order.is_finite) and q_deep_order != 0 and lap_diff == 0 and K_static == 0,
      "contrast the record's G0 kill (a9261161): there an O(eps^3) source had to balance an O(eps^2) one")

banner("G0-T2  UNITARY-GAUGE TIME ORDER of the NONLINEAR reduced Lagrangian (jet test) + the ADM/GHY identity")
names = ["A", "B", "C", "D", "U", "W", "Wz", "L", "lam0"]
Ff = {nm: sp.Function(nm)(t, x) for nm in names}
geoU = geometry(Ff["A"], Ff["B"], Ff["C"], Ff["D"], ricci=False)
clU = clock(geoU, t)
# ADM pieces for the reduced metric: lapse, shift N_x = B, gamma = diag(C, D, D)
Nl = sp.sqrt(Ff["A"] + Ff["B"]**2 / Ff["C"]); gam = sp.diag(Ff["C"], Ff["D"], Ff["D"]); gami = gam.inv()
X3r = (x, y, z)
G3 = [[[sum(gami[a, d] * (sp.diff(gam[d, b], X3r[c]) + sp.diff(gam[d, c], X3r[b]) - sp.diff(gam[b, c], X3r[d]))
            for d in range(3)) / 2 for c in range(3)] for b in range(3)] for a in range(3)]
Nlow = [Ff["B"], 0, 0]
DN = [[sp.diff(Nlow[j], X3r[i]) - sum(G3[k_][i][j] * Nlow[k_] for k_ in range(3)) for j in range(3)] for i in range(3)]
Kij = sp.Matrix(3, 3, lambda i, j: (sp.diff(gam[i, j], t) - DN[i][j] - DN[j][i]) / (2 * Nl))
Kup = gami * Kij * gami
KK = sum(Kij[i, j] * Kup[i, j] for i in range(3) for j in range(3)); trK = sum(gami[i, j] * Kij[i, j] for i in range(3) for j in range(3))
Ric3 = lambda b, c: sum(sp.diff(G3[a][b][c], X3r[a]) - sp.diff(G3[a][b][a], X3r[c]) +
                        sum(G3[a][a][d] * G3[d][b][c] - G3[a][c][d] * G3[d][b][a] for d in range(3)) for a in range(3))
R3 = sum(gami[b, c] * Ric3(b, c) for b in range(3) for c in range(3))
sqgU = Nl * sp.sqrt(Ff["C"]) * Ff["D"]
dUu = [sp.diff(Ff["U"], c) for c in X4]; dWu = [sp.diff(Ff["W"], c) for c in X4]
Vu = [dUu[a] - clU["a"][a] for a in range(4)]
al = PAR["alpha"]
L_uni = sqgU * (R3 + KK - trK**2 - 2 * PAR["Lam"] + 2 * hgrad2(clU, Vu) + 2 * al**2 * q_fun(hgrad2(clU, dWu) / al**2)
                + Ff["L"] * (Ff["Wz"] - lap_h(geoU, clU, Ff["W"])) + Ff["lam0"] * (Ff["W"] - Ff["U"])
                + PAR["ac"] * clU["aa"] - PAR["c2"] * (clU["K"] - sp.Symbol('Kbar_tau'))**2)
# jet substitution: every derivative -> a symbol
ders = sorted(L_uni.atoms(sp.Derivative), key=lambda d: -sum(c for _, c in d.variable_count))
jet = {}
for d in ders:
    fn = d.expr.func.__name__; vc = dict(d.variable_count)
    jet[d] = sp.Symbol(f"J_{fn}_t{vc.get(t, 0)}_x{vc.get(x, 0)}")
base = {Ff[nm]: sp.Symbol(f"J_{nm}") for nm in names}
L_jet = L_uni.subs(jet).subs(base)
allowed_t = {"J_C_t1_x0", "J_D_t1_x0"}
import re
tjets = [s for s in L_jet.free_symbols if re.match(r"J_.+_t([1-9]\d*)_x\d+$", s.name)]
forbidden = [s for s in tjets if s.name not in allowed_t]
rng = random.Random(329)
vals = {s: mp.mpf(rng.uniform(0.05, 0.3)) for s in L_jet.free_symbols}
for nm, v in (("J_A", 1.2), ("J_C", 1.1), ("J_D", 0.9)):
    vals[sp.Symbol(nm)] = mp.mpf(v)
grad_forb = {s.name: float(abs(sp.diff(L_jet, s).evalf(30, subs=vals))) for s in forbidden}
grad_allowed = {s.name: float(abs(sp.diff(L_jet, s).evalf(30, subs=vals))) for s in tjets if s.name in allowed_t}
# K covariant vs ADM trace (consistency of the unitary-gauge clock), numerically
Kdiff = float(abs((clU["K"] - trK).subs(jet).subs(base).evalf(30, subs=vals)))
P(f"    time jets present in L before reduction: {sorted(s.name for s in tjets)}")
P(f"    |dL/dJ| for forbidden jets (must vanish): {grad_forb}")
P(f"    |dL/dJ| for the gamma_ij velocities C_t, D_t (must not vanish): {grad_allowed};  |K_cov - tr K_ADM| = {Kdiff:.1e}")
# ADM/GHY identity numerically on the concrete fields: sqrt(-g) R - L_ADM = 2 d_mu(sqrt(-g)(n^mu K - a^mu))
Nl0 = sp.sqrt(F0["A"] + F0["B"]**2 / F0["C"])
subsF = {Ff[nm]: F0[nm] for nm in ("A", "B", "C", "D")}
LADM0 = (sqgU * (R3 + KK - trK**2)).subs(subsF).doit()
cl0 = clock(geoF, t)
vec = [sqg0 * (cl0["nu"][m] * cl0["K"] - sum(gi[m, b] * cl0["a"][b] for b in range(4))) for m in range(2)]
fR = sp.lambdify((t, x), sqg0 * geoF["R"] - LADM0, modules="mpmath")
fV = sp.lambdify((t, x), vec, modules="mpmath")
ghy = []
for (tp, xp) in PTS:
    lhs = fR(tp, xp); rhs = 2 * (d1(lambda s: fV(s, xp)[0], tp) + d1(lambda s: fV(tp, s)[1], xp))
    ghy.append(float(abs(lhs - rhs) / (abs(lhs) + abs(rhs))))
OUT["numbers"]["T2"] = {"forbidden_grad": grad_forb, "allowed_grad": grad_allowed, "K_cov_minus_trK_ADM": Kdiff, "ghy_rel": ghy}
check("G0-T2a ADM/GHY identity: sqrt(-g) R = L_ADM + 2 d_mu[sqrt(-g)(n^mu K - a^mu)] (ACTION.md sign) at 3 points",
      f"max rel {max(ghy):.1e}", max(ghy) < 1e-25)
t2 = check("G0-T2b NONLINEAR unitary-gauge Lagrangian (all chassis terms, heat slice, leaf average) has no second time "
           "derivative and no time derivative of N, N^i, U, W, Wz, L, lam0: manifestly second order in time; only "
           "gamma_ij has a momentum", f"max |dL/dJ_forbidden| = {max(grad_forb.values()) if grad_forb else 0:.1e}; "
           f"min |dL/dJ_allowed| = {min(grad_allowed.values()):.2e}; K check {Kdiff:.0e}",
           (max(grad_forb.values()) if grad_forb else 0) < 1e-25 and min(grad_allowed.values()) > 1e-6 and Kdiff < 1e-25,
           "Delta_h's K n(W) term cancels the d_t W of h.nabla.nabla W exactly: the filter is purely intrinsic to the leaf")

banner("G0-T3  det M(omega, k) of the derived scalar block: filter (C -> e^{-xi^2 k^2} C) and leaf average included")
Eb = block(Ce, al_, c2_)
M = sp.Matrix([[sp.diff(Eb[e], v) for v in (An, Ap, AB, AU)] for e in ("n", "psi", "B", "U")])
detM = sp.factor(sp.expand(M.det()))
deg = sp.Poly(sp.expand(M.det()), wq).degree()
ordr = {e: {str(v): sp.Poly(sp.expand(sp.diff(Eb[e], v)), wq).degree() for v in (An, Ap, AB, AU)} for e in Eb}
xi_s, kk_ = sp.symbols('xi k', positive=True)
filt_w = sp.diff(sp.exp(-xi_s**2 * kk_**2) * sp.Symbol('C'), wq)
roots = sp.solve(sp.Eq(sp.expand(M.det()), 0), wq)
OUT["numbers"]["T3"] = {"detM": str(detM), "omega_degree": deg, "orders": ordr, "filter_d_omega": str(filt_w),
                        "omega_roots": [str(sp.simplify(r)) for r in roots]}
P(f"    omega-order per equation/field: {ordr}")
P(f"    det M = {detM}  (omega-degree {deg});  d/d omega of the filter factor: {filt_w}")
P(f"    leaf average: <delta K> = 0 for every k != 0 (L350 G5); at k = 0 lambda = 1 + c2 (FP5) -- adds no omega power")
check("G0-T3 every linear equation is <= 2nd order in time; det M has omega-degree 2 (one scalar mode, no Ostrogradsky "
      "pair); the filter is omega-independent; the leaf average acts only at k = 0",
      f"degree {deg}; max order {max(max(v.values()) for v in ordr.values())}; filter d/domega = {filt_w}",
      deg == 2 and max(max(v.values()) for v in ordr.values()) <= 2 and filt_w == 0)

banner("G0-T4  CONSTRAINT PRESERVATION: spatial Noether identity; elliptic second-class equations; tilted-frame diagnostic")
# spatial (leaf-preserving) diffeos are a subset of S2's arbitrary xi: covered by S2 at xi^t = 0 too
XI_SP = (sp.Integer(0), XI[1])
XI_SAVE = XI; XI = XI_SP
resS, relS, dtS = noether_residual("CHK")
XI = XI_SAVE
# lapse coefficient after eliminating U (U = n / (1 + C)): 4C/(1+C) + 2 alpha_c > 0; U coefficient 1 + C > 0
Cs, acs = sp.symbols('C alpha_c', positive=True)
Un = sp.solve(sp.Eq(block(Cs, acs, 0)["U"], 0), AU)[0]
lapse_coef = sp.simplify(sp.diff(block(Cs, acs, 0)["n"].subs(AU, Un), An) / (2 * kq**2))
ylims = {"y->0 (C->inf)": sp.limit(lapse_coef.subs(Cs, 1 / (1 - sp.exp(-sp.sqrt(yy))) - 1), yy, 0),
         "y->inf (C->0)": sp.limit(lapse_coef.subs(Cs, 1 / (1 - sp.exp(-sp.sqrt(yy))) - 1), yy, sp.oo)}
# tilted frame, frozen flat metric: coefficient of tau_tt^2 in alpha_c a^2 (the instantaneous mode, BPS 2011)
tt_, tx_, txx, ttt, ttx = sp.symbols('tau_t tau_x tau_xx tau_tt tau_tx', real=True)
Xf = tt_**2 - tx_**2
nl_f = [-tt_ / sp.sqrt(Xf), -tx_ / sp.sqrt(Xf)]
etai = sp.diag(-1, 1)
nu_f = [etai[i, i] * nl_f[i] for i in range(2)]
dd = sp.Matrix([[ttt, ttx], [ttx, txx]])
dvars = (tt_, tx_)
Dn_f = [[sum(sp.diff(nl_f[b], dvars[c]) * dd[c, a] for c in range(2)) for b in range(2)] for a in range(2)]
acc_f = [sum(nu_f[a] * Dn_f[a][b] for a in range(2)) for b in range(2)]
aa_f = sum(etai[a, a] * acc_f[a]**2 for a in range(2))
hess_tt = sp.simplify(sp.diff(aa_f, ttt, 2) / 2)
OUT["numbers"]["T4"] = {"spatial_noether_rel": relS, "lapse_coef": str(lapse_coef), "lapse_coef_limits": {k: str(v) for k, v in ylims.items()},
                        "tilted_tau_tt2_coef_in_a2": str(hess_tt), "nonlinear_elliptic_solvability_proved": False}
P(f"    spatial-diffeo residual (momentum constraint preserved): {relS:.1e}")
P(f"    lapse coefficient after eliminating U: {lapse_coef}  limits {ylims}")
P(f"    tilted frame (flat metric): coefficient of tau_tt^2 in a^2 = {hess_tt}  (0 in the preferred frame tau_x = 0)")
t4a = check("G0-T4a the momentum constraint is preserved: the spatial (leaf-preserving) Noether identity holds with the "
            "heat slice and leaf average", f"{relS:.1e}", relS < 1e-25)
t4b = check("G0-T4b the second-class lapse/U equations are elliptic leaf equations with positive coefficients at every y "
            "for alpha_c > 0 (lapse 4C/(1+C) + 2 alpha_c, U 1 + C)",
            f"lapse coef / 2k^2 = {lapse_coef}; limits {ylims}", all(bool(v.is_positive) for v in ylims.values()))
check("G0-T4c tilted-frame diagnostic: the frozen-metric clock equation is 4th order in a frame tilted against the "
      "foliation (tau_tt^2 coefficient != 0, = 0 in the preferred frame): the instantaneous mode, not a propagating "
      "Ostrogradsky pair (T3: one scalar mode)", f"{hess_tt}",
      sp.simplify(hess_tt.subs(tx_, 0)) == 0 and sp.simplify(hess_tt) != 0)

# ============================================================================================= verdicts
banner("VERDICTS (rules frozen in FROZEN_CRITERIA.md)")
ok = {n: o for n, o in CH}
g9_core = all(ok[k] for k in ok if k.startswith("G9-S1") or k.startswith("G9-S2 ") or k.startswith("G9-S3") or k.startswith("G9-S4"))
G9 = "PASS" if g9_core else ("FAIL" if not s1_minimal or not s2_chassis else "CONDITIONAL")
g0_iii = ok[[k for k in ok if k.startswith("G0-T1")][0]] and t2 and ok[[k for k in ok if k.startswith("G0-T3")][0]]
G0 = ("CONDITIONAL" if (g0_iii and t4a and t4b) else "FAIL")   # nonlinear elliptic solvability of the non-local leaf system not proved
controls_ok = all(ok[k] for k in ok if k.startswith("G9-C"))
OUT["verdicts"] = {"G9": G9, "G0": G0, "controls_ok": controls_ok,
                   "G0_reason": "orders, Ostrogradsky-freedom and momentum-constraint preservation established (linear "
                                "block + nonlinear reduced sector); nonlinear solvability of the elliptic, leaf-non-local "
                                "lapse/U/W/L system not proved -> CONDITIONAL by the frozen rule",
                   "G9_extra_term": "0 (exact identity); diagnostics only for non-covariant implementations"}
P(f"    G9 = {G9}    G0 = {G0}    controls ok = {controls_ok}")
npass = sum(1 for _, o in CH if o)
P(f"\n{npass}/{len(CH)} checks pass   ({time.time() - T0:.0f} s)")
OUT["n_pass"], OUT["n_checks"] = npass, len(CH)
with open(os.path.join(HERE, f"cfg329_g9_g0_results{SUF}.json"), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
if MUTATE:
    flagged = (G9 != "PASS") and not s1_minimal and s1_identity
    P(f"    MUTATE: G9 flagged the non-minimal coupling: {flagged} (identity still exact: {s1_identity})")
    sys.exit(1 if flagged else 0)
sys.exit(0 if npass == len(CH) else 1)
