#!/usr/bin/env python3
"""V3W W1: PPN gamma and beta of v3s, derived from the action (static, spherical, weak field, screening in place).

Criteria: FROZEN_CRITERIA.md (committed alone, 37c16dcbaa).
Run:  OMP_NUM_THREADS=1 PYTHONHASHSEED=0 python3 w1_ppn.py          (V3W_MUTATE=1: screening removed, gamma_L -> 0)
Units c = 1. K = 4 pi G. Isotropic gauge ds^2 = -e^{2Phi} dt^2 + e^{-2Psi}(dr^2 + r^2 dOmega^2), P = P_r(r) dr, tau = t.
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing.
"""
import os, sys, json, math, hashlib
import sympy as sp

MUT = os.environ.get("V3W_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
OUT, CHK, RES = [], {}, {"lane": "V3W_v3s_weak_spots", "part": "W1", "criteria": "37c16dcbaa", "mutate": MUT}


def P_(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, detail):
    CHK[name] = bool(ok); RES.setdefault("checks", {})[name] = dict(ok=bool(ok), detail=str(detail))
    P_(f"{name} {'PASS' if ok else 'FAIL'} {detail}")


r, th, t = sp.symbols("r theta t", positive=True)
G, m, a0, Lst, eps, Lam, muK = sp.symbols("G m a0 L_star epsilon Lambda mu_K", positive=True)
K = 4 * sp.pi * G
gL = K * Lst ** 2 / 2
Phi = sp.Function("Phi")(r); Psi = sp.Function("Psi")(r); Pr = sp.Function("P")(r)


def EL(L, f):
    out = sp.diff(L, f) - sp.diff(sp.diff(L, sp.diff(f, r)), r) + sp.diff(sp.diff(L, sp.diff(f, r, 2)), r, 2)
    return out


def Wfun(u):
    return (a0 ** 2 / K) * (-u / a0 - sp.log(1 - u / a0))


# ------------------------------------------------------------ reduced Lagrangian (per 4 pi r^2 dr; sin(theta) divided out)
L_GR = r ** 2 * sp.exp(Phi - Psi) * (sp.diff(Psi, r) ** 2 - 2 * sp.diff(Phi, r) * sp.diff(Psi, r)) / (8 * sp.pi * G)
L_LAM = -r ** 2 * sp.exp(Phi - 3 * Psi) * 2 * Lam / (16 * sp.pi * G)
L_KQ = r ** 2 * sp.exp(Phi - 3 * Psi) * 2 * muK ** 2 * (sp.exp(-Phi) - 1) ** 2 / (16 * sp.pi * G)   # Q = 1/N
Smod = sp.exp(3 * Psi) * sp.diff(r ** 2 * sp.exp(-Psi) * Pr, r) / r ** 2                         # D_i P^i
uP = K * sp.exp(Psi) * Pr                                                                          # K |P|, P_r > 0
gLuse = 0 if MUT else gL
L_P = r ** 2 * sp.exp(Phi - 3 * Psi) * (sp.exp(2 * Psi) * Pr * sp.diff(Phi, r) - Wfun(uP) - gLuse / 2 * Smod ** 2)
RES["action"] = "L = r^2 { e^(Phi-Psi)[Psi'^2 - 2 Phi'Psi']/8piG - e^(Phi-3Psi) 2Lambda/16piG + e^(Phi-3Psi) 2 mu_K^2 (e^-Phi - 1)^2/16piG " \
                "+ e^(Phi-3Psi)[e^(2Psi) P Phi' - W(K e^Psi P) - (gamma_L/2)(D.P)^2] },  D.P = e^(3Psi) r^-2 (r^2 e^-Psi P)'"
P_("V3W W1  PPN gamma/beta of v3s from the action" + ("  [MUTATE: gamma_L = 0]" if MUT else ""))
P_("  " + RES["action"])

# ------------------------------------------------------------ K2: GR part equals sqrt(-g) R from the 4-metric
X = (t, r, th, sp.Symbol("ph"))
gm = sp.diag(-sp.exp(2 * Phi), sp.exp(-2 * Psi), sp.exp(-2 * Psi) * r ** 2, sp.exp(-2 * Psi) * r ** 2 * sp.sin(th) ** 2)
gi = gm.inv()
Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(gm[d, b], X[c]) + sp.diff(gm[d, c], X[b]) - sp.diff(gm[b, c], X[d])) for d in range(4)) / 2)
         for c in range(4)] for b in range(4)] for a in range(4)]
Rs = 0
for b in range(4):
    for d in range(4):
        if gi[b, d] == 0:
            continue
        Rbd = sum(sp.diff(Gam[a][b][d], X[a]) - sp.diff(Gam[a][b][a], X[d]) + sum(Gam[a][a][e] * Gam[e][b][d] - Gam[a][d][e] * Gam[e][b][a] for e in range(4)) for a in range(4))
        Rs += gi[b, d] * Rbd
sqrtg = sp.exp(Phi - 3 * Psi) * r ** 2                       # sqrt(-g)/sin(theta)
L_R = sp.simplify(sqrtg * Rs / (16 * sp.pi * G))
k2 = [sp.simplify(EL(L_R, f) - EL(L_GR, f)) for f in (Phi, Psi)]
check("W1-K2", all(x == 0 for x in k2), f"EL[sqrt(-g)R/16piG] - EL[ADM reduced GR part] for (Phi, Psi): {k2} (0)")

# ------------------------------------------------------------ K1: law off -> Schwarzschild exactly, gamma = beta = 1
Phis = sp.log((1 - m / (2 * r)) / (1 + m / (2 * r))); Psis = -2 * sp.log(1 + m / (2 * r))
k1 = [sp.simplify(EL(L_GR, f).subs({Phi: Phis, Psi: Psis}).doit()) for f in (Phi, Psi)]
k1 = [sp.simplify(sp.together(x)) for x in k1]
U = m / r
g00 = sp.series(-sp.exp(2 * Phis).subs(m, eps * m), eps, 0, 3).removeO()
grr = sp.series(sp.exp(-2 * Psis).subs(m, eps * m), eps, 0, 2).removeO()
beta_GR = sp.simplify(-g00.coeff(eps, 2) / (2 * U ** 2)); gamma_GR = sp.simplify(grr.coeff(eps, 1) / (2 * U))
check("W1-K1", all(x == 0 for x in k1) and beta_GR == 1 and gamma_GR == 1,
      f"law off: Schwarzschild residuals {k1}; gamma = {gamma_GR}, beta = {beta_GR} (exactly 1)")
RES["K1"] = dict(residuals=[str(x) for x in k1], gamma=str(gamma_GR), beta=str(beta_GR))

# ------------------------------------------------------------ full equations, exact
LT = L_GR + L_LAM + L_KQ + L_P
E_Phi, E_Psi, E_P = [EL(LT, f) for f in (Phi, Psi, Pr)]

# ------------------------------------------------------------ perturbative exterior solution in GM (Lambda = mu_K = 0 here)
p0 = m / Lst ** 2
f2, s2, q2 = sp.Function("phi2")(r), sp.Function("psi2")(r), sp.Function("q2")(r)
phi1 = -m / r + (0 if MUT else p0) * r
psi1 = phi1
P1 = (m / r ** 2 if MUT else p0) / K          # MUTATE: unscreened linear-h solution would be P = Phi'/K (expansion invalid)
sub = {Phi: eps * phi1 + eps ** 2 * f2, Psi: eps * psi1 + eps ** 2 * s2, Pr: eps * P1 + eps ** 2 * q2, Lam: 0, muK: 0}
def order(E, n):
    e = E.subs(sub).doit()
    return sp.simplify(sp.series(e, eps, 0, n + 1).removeO().coeff(eps, n))
o1 = [order(E, 1) for E in (E_Phi, E_Psi, E_P)]
check("W1-K3", all(sp.simplify(x) == 0 for x in o1),
      (f"first order: Phi1 = Psi1 = -m/r, p = K P = m/r^2 (unscreened, linear h; MUTATE) solves (Phi, Psi, P): residuals {o1} (0)" if MUT else
       f"first order: hedgehog Phi1 = Psi1 = -m/r + (m/L*^2) r, p = K P = m/L*^2 solves (Phi, Psi, P) equations: residuals {o1} (0)"))
P_("  first order: the Psi equation is (r^2 (Phi1 - Psi1)')' = 0 with no source -> Psi1 = Phi1 exactly; gamma - 1 = 0 at O(GM)")
o2 = [sp.simplify(sp.expand(order(E, 2))) for E in (E_Phi, E_Psi, E_P)]
for nm, e in zip(("Phi", "Psi", "P"), o2):
    P_(f"  second-order {nm} equation: {e}")
RES["second_order_equations"] = {nm: str(e) for nm, e in zip(("Phi", "Psi", "P"), o2)}

# solve second order: Psi equation gives D = psi2 - phi2; then Phi and P
Dd = sp.Function("D")(r)
ePsi = sp.simplify(o2[1].subs(s2, f2 + Dd).doit())
solD = sp.dsolve(sp.Eq(ePsi, 0), Dd)
solD = solD.rhs if not isinstance(solD, list) else solD[0].rhs
cs = sorted(solD.free_symbols - {r, m, Lst, G, a0}, key=str)
solD0 = solD.subs({c: 0 for c in cs})                       # regular, decaying homogeneous parts dropped (no Psi source at r = 0)
P_(f"  D = psi2 - phi2 (particular): {sp.simplify(solD0)}")
ePhi = sp.simplify(o2[0].subs(s2, f2 + solD0).doit()); eP = sp.simplify(o2[2].subs(s2, f2 + solD0).doit())
# eliminate by integration: (Phi eq) is a total derivative -> phi2'; then (P eq) is an Euler ODE for q2 alone
C1, C2, C3 = sp.symbols("C1 C2 C3")
ePhi0 = sp.expand(o2[0].subs(s2, f2 + solD0).doit())
dphi = sp.Symbol("dphi")
ePhiL = ePhi0.subs(sp.Derivative(f2, (r, 2)), sp.Symbol("ddphi")).subs(sp.Derivative(f2, r), dphi)
# Phi eq = d/dr[ r^2 (phi2' + D')/K - r^2 q2 ] - src(r)
inner = r ** 2 * (dphi + sp.diff(solD0, r)) / K - r ** 2 * q2
dinner = sp.diff(inner.subs(dphi, sp.Derivative(f2, r)), r)
srcr = sp.simplify(sp.expand(dinner - ePhi0))
k5a = srcr.has(f2) or srcr.has(q2)
srcI = sp.integrate(srcr, r) + C1
phi2p = sp.solve(sp.Eq(inner, srcI), dphi)[0]
eP0 = o2[2].subs(s2, f2 + solD0).doit()
eQ = sp.simplify(eP0.subs(sp.Derivative(f2, r), phi2p).doit())
try:
    qs = sp.dsolve(sp.Eq(eQ, 0), q2)
    qsol = sp.simplify(qs.rhs)
    csy = sorted(qsol.free_symbols - {r, m, Lst, G, a0, C1}, key=str)
    P_(f"  q2 general: {qsol}  (integration constants {csy})")
    phi2p_s = sp.simplify(phi2p.subs(q2, qsol))
    fsol = sp.integrate(sp.expand(phi2p_s), r)
    res2 = [sp.simplify(sp.expand(o2[0].subs({s2: fsol + solD0, f2: fsol, q2: qsol}).doit())),
            sp.simplify(sp.expand(o2[2].subs({s2: fsol + solD0, f2: fsol, q2: qsol}).doit()))]
    fexp = sp.expand(fsol)
    c_r2 = sp.simplify(sum(tm for tm in fexp.as_ordered_terms() if sp.simplify(tm * r ** 2).free_symbols <= {m, G} and not tm.has(sp.log(r))))
    P_(f"  phi2 = {fexp}")
    check("W1-K5", (not k5a) and all(x == 0 for x in res2),
          f"second order solved by integration: residuals (Phi, P) {res2} (0); m^2/r^2 part of phi2: {c_r2} (GR has 0, so beta = 1 iff 0)")
    RES["phi2"] = str(fexp); RES["q2"] = str(qsol); RES["D"] = str(sp.simplify(solD0)); RES["phi2_m2_over_r2_part"] = str(c_r2)
    free = [C1] + list(csy)
    RES["free_homogeneous"] = [str(q) for q in free]
    RES["second_order_solution_found"] = True
except ValueError as exc:
    check("W1-K5", False, f"second-order equations have no solution in the small-p expansion: {exc}")
    RES["second_order_solution_found"] = False
    fsol = qsol = None; free = []

# ------------------------------------------------------------ beta from the exterior metric
# g00 = -exp(2 eps phi1 + 2 eps^2 phi2); U-type piece: phi1 = -U + p0 r; beta U^2 term = coefficient of m^2/r^2
LR = sp.Symbol("LR")
if fsol is not None:
    fs0 = fsol.subs({q: 0 for q in free}).subs(sp.log(r), LR + sp.log(Lst))
    fs0 = sp.expand(sp.expand_log(fs0, force=True))
    g00f = sp.expand(sp.series(-sp.exp(2 * eps * phi1 + 2 * eps ** 2 * fs0), eps, 0, 3).removeO().coeff(eps, 2))
    # pure m^2/r^2 coefficient (beta): terms with no L* and no a0 and r^-2
    g00m = sp.expand(g00f)
    beta_term = sum(tm for tm in g00m.as_ordered_terms() if sp.simplify(tm * r ** 2).free_symbols <= {m} and tm.has(m) and not tm.has(LR))
    beta_v = sp.simplify(-beta_term / (2 * U ** 2)) if beta_term != 0 else sp.Integer(0)
    rem_all = sp.expand(g00m - beta_term)
    rem = sum(tm for tm in rem_all.as_ordered_terms() if tm.has(r) or tm.has(LR))   # r-independent terms: unobservable rescaling of t
    P_(f"  g00 at O(eps^2): {g00m}")
    P_(f"  beta (coefficient of -2 U^2): {beta_v};  non-PPN remainder: {rem}")
    RES["beta"] = str(beta_v); RES["g00_remainder"] = str(rem)
else:
    beta_v, rem = None, None

# ------------------------------------------------------------ 3D: exact Psi source of the P sector, background cross terms
x, y, z = sp.symbols("x y z", real=True)
Ph3 = sp.Function("Phi3")(x, y, z); Ps3 = sp.Function("Psi3")(x, y, z); Pv = [sp.Function(f"Pv{i}")(x, y, z) for i in range(3)]
Xs = (x, y, z)
P2_ = sum(p ** 2 for p in Pv)
u3 = K * sp.exp(Ps3) * sp.sqrt(P2_)
S3 = sp.exp(3 * Ps3) * sum(sp.diff(sp.exp(-Ps3) * Pv[i], Xs[i]) for i in range(3))
L3P = sp.exp(Ph3 - 3 * Ps3) * (sp.exp(2 * Ps3) * sum(Pv[i] * sp.diff(Ph3, Xs[i]) for i in range(3)) - Wfun(u3) - gL / 2 * S3 ** 2)
src = sp.diff(L3P, Ps3) - sum(sp.diff(sp.diff(L3P, sp.diff(Ps3, v)), v) for v in Xs)
src0 = sp.simplify(src.subs(Ps3, 0).doit())
divP = sum(sp.diff(Pv[i], Xs[i]) for i in range(3)); Pd = sum(Pv[i] * sp.diff(Ph3, Xs[i]) for i in range(3))
uu = K * sp.sqrt(P2_); Wp = sp.diff(Wfun(sp.Symbol("w")), sp.Symbol("w")).subs(sp.Symbol("w"), uu)
target = sp.exp(Ph3) * (-Pd + 3 * Wfun(uu) - uu * Wp - gL / 2 * divP ** 2) - sum(sp.diff(gL * sp.exp(Ph3) * divP * Pv[i], Xs[i]) for i in range(3))
k6 = sp.simplify(src0 - target)
check("W1-K6", k6 == 0, f"3D Psi source of the P sector at Psi = 0: e^Phi[-P.grad Phi + 3W - uW' - (gL/2)(div P)^2] - div(gL e^Phi (div P) P): residual {k6} (0)")
P_("  Psi equation (3D): lap(Phi - Psi) = -4 pi G * S_Psi, S_Psi = the source above (+ GR cubic terms, Lambda, mu_K)")

# ------------------------------------------------------------ numbers: bounds at the Solar System (both footings)
GMs = 1.32712440018e20; cl = 2.99792458e8; AU = 1.495978707e11; PC = 3.0857e16
mgeo = GMs / cl ** 2
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
XE_MIN = {"canonical": 1.305, "alt": 1.146}       # D7b E0 x_e (smallest Galactic field, largest 1/x_e)
LST = [21.7, 24.0, 50.0, 90.0]
CASS = (2.1e-5, 2.3e-5); BAND = (CASS[0] - 2 * CASS[1], CASS[0] + 2 * CASS[1]); LLR = 1e-4
R_CUT = 1000 * PC
num = {}
for f, A in FOOT.items():
    ag = A / cl ** 2
    rows = {}
    for Lpc in LST:
        L = (Lpc if not MUT else 1e-6) * PC
        pfrac = GMs / L ** 2 / A                                  # |p|/a0 of the isolated hedgehog (MUTATE: saturates)
        pfrac = min(pfrac, 1.0)
        out = {}
        for nm, rr in (("Mercury", 0.387 * AU), ("1AU", AU), ("Cassini_10AU", 10 * AU)):
            g_rem_bg = 2 * ag * rr * (1 + 1 / XE_MIN[f]) * (1 + math.log(R_CUT / rr))      # background cross terms, worst-case Green's bound
            g_rem_iso = 2 * mgeo * rr * abs(math.log(rr / L)) / L ** 2 + 10 * (rr / L) ** 4      # exact isolated D term + homogeneous allowance
            if rem is not None and not MUT:
                b_iso = abs(float(rem.subs({m: mgeo, Lst: L, a0: ag, G: 1, LR: math.log(rr / L), r: rr}).evalf())) / (2 * (mgeo / rr) ** 2) + 10 * (rr / L) ** 4
            else:
                b_iso = float("nan")
            g_rem_lam = 1.0890e-52 * rr ** 2                                                   # GR + Lambda, as in GR
            out[nm] = dict(gamma_rem=g_rem_bg + g_rem_iso + g_rem_lam, bg=g_rem_bg, iso=g_rem_iso, lam=g_rem_lam, beta_iso=b_iso)
        rows[f"{Lpc:g}"] = dict(p_over_a0=pfrac, **out)
    num[f] = rows
RES["bounds"] = num
P_("")
P_("  Bounds (gamma - 1 remainder = |Phi - Psi|/U; beta remainder at Mercury = 2 x gamma remainder + isolated non-PPN):")
labels = {}
for f in FOOT:
    for Lpc in LST:
        row = num[f][f"{Lpc:g}"]
        gC = row["Cassini_10AU"]["gamma_rem"]; bM = 2 * row["Mercury"]["bg"] + row["Mercury"]["beta_iso"]
        row["beta_rem_Mercury"] = bM
        P_(f"  {f:9s} L*={Lpc:5.1f} pc: |p|/a0 = {row['p_over_a0']:.2e}; |gamma-1| <= {gC:.2e} at 10 AU "
           f"(bg {row['Cassini_10AU']['bg']:.1e}, iso {row['Cassini_10AU']['iso']:.1e}, Lambda {row['Cassini_10AU']['lam']:.1e}); "
           f"|beta-1| <= {bM:.2e} at Mercury")
k4 = all(num[f][f"{Lpc:g}"]["p_over_a0"] <= 1e-4 for f in FOOT for Lpc in LST)
check("W1-K4", k4, f"expansion validity |p|/a0 <= 1e-4 at every L* (max {max(num[f][f'{L:g}']['p_over_a0'] for f in FOOT for L in LST):.2e})")

ppn_ok = all(c_ for c_ in CHK.values())
for f in FOOT:
    gmax = max(num[f][f"{L:g}"]["Cassini_10AU"]["gamma_rem"] for L in LST)
    bmax = max(num[f][f"{L:g}"]["beta_rem_Mercury"] for L in LST)
    gam_dev = 0.0 + gmax; bet_dev = (abs(float(beta_v) - 1) if beta_v is not None else float("nan")) + bmax
    gpass = BAND[0] <= -gmax and gmax <= BAND[1]
    bpass = bet_dev <= LLR
    if not ppn_ok:
        lab = "UNDECIDED (a W1 check failed)"
    elif gpass and bpass:
        lab = f"PASS: gamma - 1 = 0 at O(GM), |remainder| <= {gmax:.1e} (band [{BAND[0]:.1e}, {BAND[1]:.1e}]); beta = {beta_v}, |remainder| <= {bmax:.1e} (<= 1e-4)"
    else:
        lab = f"FAIL: gamma remainder {gmax:.1e}, beta deviation {bet_dev:.1e}"
    labels[f] = lab
    P_(f"  W1 [{f}]: {lab}")
RES["labels"] = labels
n_ok = sum(CHK.values())
P_(f"\nW1 COMPLETE: {n_ok}/{len(CHK)} checks PASS")
json.dump(RES, open(os.path.join(HERE, f"w1_ppn{TAG}.json"), "w"), indent=1, sort_keys=True, default=str)
open(os.path.join(HERE, f"w1_ppn{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n_ok == len(CHK) else 1)
