#!/usr/bin/env python3
"""CFG152 M2 (flat FRW, arbitrary a(t), general V): method M2 (routes U and N), controls C1, C2, C3 and H on FRW.

Frozen criteria: ../CFG152_FROZEN_CRITERIA.md (sha256 printed first).  Modes: MUTATE unset (main), a, b, 1.
Writes cfg152_M2_frw[_MUTATE_<mode>].out and ..._results.json next to this file.
"""
import random
import sys

import sympy as sp

import cfg152_common as C
from cfg152_common import A_, LAMB, VF, Mp2, gt, k, t

NAME = "cfg152_M2_frw"
mode = C.get_mode(["main", "a", "b", "1"])
rep = C.Report(NAME, mode)
C.header(rep)
cbox = C.c_box_for(mode)
rep.p(f"c_box = {cbox}   (main run: gt*Mp2/2)")
HEAD = gt / (2 - 3 * gt)
R = rep.results
a = A_(t)
ad, add_ = sp.diff(a, t), sp.diff(a, t, 2)
H = ad / a
Hd = sp.diff(H, t)


def zero_exact(expr, n=30):
    """'exactly': sympy simplify gives 0; else 30 random rational points at 50 digits (a(t) replaced by a random
    polynomial-exponential sample and its derivatives) with |diff| < 1e-40."""
    e = sp.simplify(expr)
    if e == 0:
        return True, "simplify"
    rng = random.Random(152)
    for _ in range(n):
        c1, c2, c3 = (sp.Rational(rng.randint(1, 1000), 1000) for _ in range(3))
        tt = sp.Rational(rng.randint(1, 1000), 100)
        asamp = c1 + c2 * t**2 + sp.exp(c3 * t)
        vals = {gt: sp.Rational(rng.randint(-10**6, 10**6), rng.randint(1, 10**6)) + sp.Rational(1, 7919),
                k: sp.Rational(rng.randint(1, 10**6), rng.randint(1, 10**6)),
                Mp2: sp.Rational(rng.randint(1, 10**6), rng.randint(1, 10**6))}
        v = sp.N(e.subs(a, asamp).doit().subs(t, tt).subs(vals), 50)
        if abs(v) > sp.Float("1e-40"):
            return False, f"nonzero: {e}"
    return True, "30 random points at 50 digits (simplify did not return 0)"


# ------------------------------------------------------------------ 1. expansion
rep.p("\n== 1. brute-force second-order expansion about flat FRW (phi = t, lambda = lamb(t), V = V(t), a(t) arbitrary)")
o = C.expand_action("frw", cbox, log=rep.p)
rep.check("internal: expansion checks (det, R_bar = 6(a''/a + H^2), box phi two ways agree)",
          all(o["checks"].values()), o["checks"], kind="internal")
F = o["fields"]
names = C.FIELD_NAMES                                   # Phi, B, Psi, E, dphi, dlam, h
fl_tx = [F[n] for n in names]
ft = {n: sp.Function(n + "t", real=True)(t) for n in names}
fl_t = [ft[n] for n in names]
idx = {f.func: i for i, f in enumerate(fl_tx)}


def to_t(L, uniform):
    """uniform=True: fields depend on t only (k = 0 part).  uniform=False: F(t,x) -> F(t) cos(kx), x-average."""
    Cc, Ss = sp.symbols("Ccos Ssin")
    trig = [Cc, -Ss, -Cc, Ss]
    rep_ = {}
    for d in L.atoms(sp.Derivative):
        fn = d.expr.func
        if fn not in idx:
            continue
        vc = dict(d.variable_count)
        m_, n_ = vc.get(t, 0), vc.get(C.x, 0)
        f = fl_t[idx[fn]]
        base = sp.diff(f, t, m_) if m_ else f
        rep_[d] = (base if n_ == 0 else 0) if uniform else base * k**n_ * trig[n_ % 4]
    for f in fl_tx:
        rep_[f] = fl_t[idx[f.func]] * (1 if uniform else Cc)
    Ls = sp.expand(L.xreplace(rep_))
    if uniform:
        return Ls
    c2c, c2s, ccs = Ls.coeff(Cc, 2), Ls.coeff(Ss, 2), Ls.coeff(Cc, 1).coeff(Ss, 1)
    resid = sp.expand(Ls - c2c * Cc**2 - c2s * Ss**2 - ccs * Cc * Ss)
    assert resid == 0, "non-quadratic trig structure"
    return sp.expand((c2c + c2s) / 2)


def el_expr(L, f, maxo=6):
    """Euler-Lagrange expression sum_m (-1)^m d^m/dt^m dL/d f^(m); one entry per field, never dropped.
    (The first main run used sympy's euler_equations, which silently drops identically-zero equations and so can
    misalign a zip with the field list; it crashed at the dlam/h check.  Replaced here; disclosed in the README.)"""
    res = sp.diff(L, f)
    for m_ in range(1, maxo + 1):
        d = sp.Derivative(f, (t, m_))
        if L.has(d):
            res += (-1)**m_ * sp.diff(sp.diff(L, d), t, m_)
    return sp.expand(res)


def euler_equations(L, fs, var):
    """Drop-in used below: returns objects with .lhs, one per field, in order."""
    class _E:
        def __init__(self, e):
            self.lhs = e
    return [_E(el_expr(L, f)) for f in fs]


# ------------------------------------------------------------------ 2. background equations
rep.p("\n== 2. background equations from the first-order terms (uniform fields)")
L1u = to_t(o["L1"], uniform=True)
bg_fields = [ft["Phi"], ft["Psi"], ft["dphi"], ft["dlam"], ft["h"]]
els = {str(f.func): sp.expand(e.lhs) for f, e in zip(bg_fields, euler_equations(L1u, bg_fields, t))}
for kk, v in els.items():
    rep.p(f"   E[{kk}] = {sp.factor(v)}")
E_Phi, E_Psi = els["Phit"], els["Psit"]
for nm_, ex_ in (("E_Phi", E_Phi), ("E_Psi", E_Psi)):
    assert not ex_.has(sp.Derivative(LAMB(t), t)) and not ex_.has(sp.Derivative(VF(t), t)), nm_
lb, Vs = sp.symbols("lb Vs")
sol = sp.solve([E_Phi.subs({LAMB(t): lb, VF(t): Vs}), E_Psi.subs({LAMB(t): lb, VF(t): Vs})], [lb, Vs], dict=True)
assert len(sol) == 1, sol
lam_sol, V_sol = sp.simplify(sol[0][lb]), sp.simplify(sol[0][Vs])
rep.p(f"   lambda_bar = {lam_sol}")
rep.p(f"   V          = {V_sol}")
R["lambda_bar"], R["V_background"] = str(lam_sol), str(V_sol)
bg = {LAMB(t): lam_sol, VF(t): V_sol}
bianchi = sp.simplify(els["dphit"].subs(bg).doit())
rep.check("internal: the dphi first-order term vanishes identically on the background (Bianchi identity)",
          bianchi == 0, bianchi, kind="internal")
rep.check("internal: dlam and h first-order terms vanish", sp.simplify(els["dlamt"]) == 0 and sp.simplify(els["ht"]) == 0,
          kind="internal")
ok77 = zero_exact(V_sol - (2 - 3 * gt) * Mp2 * (2 * Hd + 3 * H**2) / 2)
rep.check("C2 (CMV eq. 77): 2 H' + 3 H^2 = 2 V / ((2 - 3 gt) M_P^2)", ok77[0], ok77[1], kind="control (literature)")
ok80 = zero_exact(lam_sol - (1 - 3 * gt) * Mp2 * Hd)
rep.check("C2 (CMV eq. 80 with lambda_CFG124 = -lambda_CMV): lambda_bar = (1 - 3 gt) M_P^2 H'", ok80[0], ok80[1],
          kind="control (literature)")

# ------------------------------------------------------------------ 3. second-order Lagrangian of one Fourier mode
rep.p("\n== 3. second-order Lagrangian of one mode cos(kx), x-averaged, background substituted")
L2 = sp.expand(to_t(o["L2"], uniform=False).subs(bg).doit())
hs = sp.expand(sp.diff(L2, ft["h"]).subs(ft["h"], 0))
tens_dec = all(not hs.has(ft[n]) for n in ("Phi", "B", "Psi", "E", "dphi", "dlam"))
rep.check("internal: tensor h decouples from the scalars on FRW", tens_dec, kind="internal")
L2s = sp.expand(L2.subs(ft["h"], 0).doit())
rep.p(f"   scalar Lagrangian has {len(sp.Add.make_args(L2s))} terms")

# ------------------------------------------------------------------ 4. route U
rep.p("\n== 4. route U: unitary gauge dphi = E = 0 in the action")


def field_order(e, fset):
    if isinstance(e, sp.Derivative) and e.expr.func in fset:
        return (e.expr.func, dict(e.variable_count).get(t, 0))
    if getattr(e, "func", None) in fset and getattr(e, "args", None) == (t,):
        return (e.func, 0)
    return None


def split(term, fset):
    coef, facs = sp.Integer(1), []
    for fac in sp.Mul.make_args(term):
        base, ex = fac.as_base_exp()
        fo = field_order(base, fset)
        if fo is None:
            coef *= fac
        else:
            facs += [fo] * int(ex)
    return coef, facs


def Dn(fn, m_):
    f = fn(t)
    return f if m_ == 0 else sp.Derivative(f, (t, m_))


def reduce_first_order(L, fset):
    """Integrate by parts until every field factor has at most one time derivative."""
    for _ in range(40):
        L = sp.expand(L)
        new, changed = sp.Integer(0), False
        for term in sp.Add.make_args(L):
            coef, facs = split(term, fset)
            if len(facs) != 2:
                raise ValueError(f"not quadratic: {term}")
            (F1, m1), (F2, m2) = sorted(facs, key=lambda q: -q[1])
            if m1 <= 1:
                new += term
                continue
            changed = True
            if m1 >= m2 + 2:
                new += -Dn(F1, m1 - 1) * sp.diff(coef * Dn(F2, m2), t)
            elif m1 == m2 + 1 and F1 == F2:
                new += -sp.diff(coef, t) / 2 * Dn(F1, m2)**2
            else:
                raise RuntimeError(f"cannot reduce {term}")
        L = new
        if not changed:
            return sp.expand(L)
    raise RuntimeError("no convergence")


def jets(L, fns, maxo=1):
    """Replace field derivatives by jet symbols; return (expr, {symbol: (fn, order)})."""
    syms, rep_ = {}, {}
    for fn in fns:
        for m_ in range(maxo, -1, -1):
            s_ = sp.Symbol(f"{fn.__name__}_{m_}")
            syms[s_] = (fn, m_)
            rep_[Dn(fn, m_)] = s_
    return sp.expand(L.xreplace(rep_)), syms


def route_U(L2s_, label):
    info = {}
    LU = sp.expand(L2s_.subs({ft["dphi"]: 0, ft["E"]: 0}).doit())
    assert not LU.has(sp.Derivative(ft["dlam"], t))
    cdl = sp.expand(sp.diff(LU, ft["dlam"]))
    cphi = sp.diff(cdl, ft["Phi"])
    info["dlam_couples_only_to_Phi"] = (sp.simplify(cdl - cphi * ft["Phi"]) == 0
                                        and not any(cphi.has(ft[n]) for n in names))
    info["dlam_constraint"] = f"({sp.factor(cphi)}) * Phi"
    LU2 = sp.expand(LU.subs({ft["Phi"]: 0, ft["dlam"]: 0}).doit())
    fset = {ft["B"].func, ft["Psi"].func}
    LU3 = reduce_first_order(LU2, fset)
    Bf, Pf = ft["B"].func, ft["Psi"].func
    ex, syms = jets(LU3, [Bf, Pf])
    B0, B1, P0, P1 = sp.symbols("Bt_0 Bt_1 Psit_0 Psit_1")
    Pq = sp.Poly(ex, B0, B1, P0, P1)
    q = {mon: sp.simplify(c_) for mon, c_ in Pq.terms()}

    def qc(**kw):
        mon = tuple(kw.get(s_, 0) for s_ in ("B0", "B1", "P0", "P1"))
        return q.get(mon, sp.Integer(0))
    info["Bdot^2"] = sp.simplify(qc(B1=2))
    info["Bdot*Psidot"] = sp.simplify(qc(B1=1, P1=1))
    info["B_nondynamical"] = info["Bdot^2"] == 0 and info["Bdot*Psidot"] == 0
    # move derivatives off B: c B' B -> -(c'/2) B^2 ; c B' P -> -c' B P - c B P'
    alpha = sp.simplify(qc(B0=2) - sp.diff(qc(B0=1, B1=1), t) / 2)
    beta0 = sp.simplify(qc(B0=1, P0=1) - sp.diff(qc(B1=1, P0=1), t))
    beta1 = sp.simplify(qc(B0=1, P1=1) - qc(B1=1, P0=1))
    g11, g01, g00 = qc(P1=2), qc(P0=1, P1=1), qc(P0=2)
    info.update(alpha=alpha, beta0=beta0, beta1=beta1)
    if alpha == 0:
        info["reduced"] = None
        return info
    A = sp.simplify(g11 - beta1**2 / (4 * alpha))
    Dm = sp.simplify(g01 - beta0 * beta1 / (2 * alpha))
    Cc = sp.simplify(g00 - beta0**2 / (4 * alpha))
    Ceff = sp.simplify(Cc - sp.diff(Dm, t) / 2)
    Pk = sp.Poly(sp.expand(sp.simplify(Ceff)), k)
    info["Ceff_poly_in_k"] = Pk.degree() <= 2 and sp.simplify(Pk.coeff_monomial(k)) == 0
    Gk = sp.simplify(-a**2 * Pk.coeff_monomial(k**2))
    m2 = sp.simplify(-Pk.coeff_monomial(1))
    cs2 = sp.simplify(Gk / A)
    info.update(reduced=True, A=A, Ceff=Ceff, G=Gk, m2=m2, cs2=cs2)
    return info


U = route_U(L2s, "main")
rep.p(f"   dlambda multiplies {U['dlam_constraint']} (so Phi = 0 at linear order)")
rep.check("route U: dlambda couples only to Phi (imposes Phi = 0)", U["dlam_couples_only_to_Phi"], kind="method check")
rep.check("route U: B has no time derivatives after integration by parts (no B'^2, no B'Psi' term)",
          U["B_nondynamical"], f"B'^2: {U['Bdot^2']}; B'Psi': {U['Bdot*Psidot']}", kind="method check")
rep.p(f"   B^2 coefficient alpha = {U['alpha']}; B*Psi: {U['beta0']}; B*Psi': {U['beta1']}")
if U["reduced"]:
    rep.p(f"   reduced: A = {U['A']}")
    rep.p(f"            Ceff (coefficient of Psi^2) = {U['Ceff']}")
    rep.p(f"            G = {U['G']}, m^2 = {U['m2']}, c_s^2 = G/A = {U['cs2']}")
    R["route_U"] = {kk: str(U[kk]) for kk in ("A", "Ceff", "G", "m2", "cs2", "alpha", "beta0", "beta1")}
    rep.check("route U: Ceff is a polynomial a0 + a2 k^2 (no odd or higher powers)", U["Ceff_poly_in_k"],
              kind="method check")
    okc = zero_exact(U["cs2"] - HEAD)
    rep.check("H-a (M2 route U): c_s^2 = gt/(2 - 3 gt) exactly, independent of a, H, H', V", okc[0] and not U["cs2"].has(a),
              f"{U['cs2']} ({okc[1]})")
    ratio = sp.simplify(U["A"] / (-(2 - 3 * gt) / gt))
    rep.check("H-b (M2 route U): A = -(2 - 3 gt)/gt times a positive factor", (not ratio.has(gt)) and bool(ratio.is_positive),
              f"A / (-(2-3gt)/gt) = {ratio}")
    fgm_A = zero_exact(U["A"] - Mp2 * a**3 / 2 * (3 - 2 / gt))
    fgm_C = zero_exact(U["Ceff"] - Mp2 * a / 2 * k**2)
    rep.check("C3 (FGM eq. 24): A = (M_P^2 a^3/2)(3 - 2/gt), Ceff = +(M_P^2 a/2) k^2 (so G = -(M_P^2 a^3/2), m^2 = 0)",
              fgm_A[0] and fgm_C[0], f"A: {fgm_A[1]}; Ceff: {fgm_C[1]}", kind="control (literature)")
else:
    for nm_ in ("route U: reduction", "H-a (M2 route U)", "H-b (M2 route U)", "C3 (FGM eq. 24)"):
        rep.check(nm_, False, "B^2 coefficient vanished; no reduction")

# C1 in route U: gt = 0
U0 = route_U(sp.expand(L2s.subs(gt, 0)), "gt=0")
c1u = (U0["B_nondynamical"] and U0["alpha"] == 0 and U0["beta0"] == 0 and U0["beta1"] != 0)
rep.check("C1 (M2 route U, gt = 0, any V): B enters linearly and its equation is Psi' = 0", c1u,
          f"alpha = {U0['alpha']}, B*Psi = {U0['beta0']}, B*Psi' = {U0['beta1']}", kind="control")

# ------------------------------------------------------------------ 5. route N
rep.p("\n== 5. route N: Euler-Lagrange equations of all six scalar fields, then B = E = 0 (Newtonian gauge)")
sc = ["Phi", "B", "Psi", "E", "dphi", "dlam"]
EL = {n: sp.expand(e.lhs) for n, e in zip(sc, euler_equations(L2s, [ft[n] for n in sc], t))}
EL = {n: sp.expand(v.subs({ft["B"]: 0, ft["E"]: 0}).doit()) for n, v in EL.items()}
dp = ft["dphi"]
dpd = sp.diff(dp, t)
sPhi = sp.solve(EL["dlam"], ft["Phi"])
rep.p(f"   dlambda equation: {sp.factor(EL['dlam'])}  ->  Phi = {sPhi}")
okPhi = len(sPhi) == 1 and sp.simplify(sPhi[0] - dpd) == 0
rep.check("route N: the dlambda equation gives Phi = dphi'", okPhi, kind="method check")
EEonly = EL["E"]
rep.p(f"   reported: the E equation alone contains Psi undifferentiated: {EEonly.has(ft['Psi']) and sp.diff(EEonly, ft['Psi']) != 0}; "
      f"contains Phi undifferentiated: {sp.simplify(sp.diff(EEonly, ft['Phi'])) != 0}")
T = sp.expand(3 * EL["E"] / k**2 - EL["Psi"])        # traceless combination 4 a^2 (e_yy - e_xx), from the parametrisation
derivs_psi = [d for d in T.atoms(sp.Derivative) if d.expr == ft["Psi"]]
sPsi = sp.solve(T, ft["Psi"]) if not derivs_psi else []
rep.p(f"   traceless combination 3 E_eq/k^2 - Psi_eq = {sp.factor(T)}")
okPsi = len(sPsi) == 1 and sp.simplify(sPsi[0] - ft["Phi"]) == 0
rep.check("route N: the traceless combination of the E and Psi equations gives Psi = Phi", okPsi, sPsi,
          kind="method check")
sub1 = {ft["Phi"]: dpd, ft["Psi"]: dpd}
EB = sp.expand(EL["B"].subs(sub1).doit())
orders = sorted({dict(d.variable_count).get(t, 0) for d in EB.atoms(sp.Derivative) if d.expr == dp})
rep.p(f"   B (0i) equation after Phi = Psi = dphi': derivative orders of dphi present: {orders}")
c = {m_: sp.simplify(EB.coeff(sp.Derivative(dp, (t, m_))) if m_ > 0 else EB.subs({sp.Derivative(dp, (t, j)): 0 for j in (1, 2, 3, 4)}).coeff(dp))
     for m_ in range(0, 4)}
okN = sp.simplify(c[3]) == 0 and sp.simplify(c[2]) != 0
P1_ = sp.simplify(c[1] / c[2]) if okN else None
P0_ = sp.simplify(c[0] / c[2]) if okN else None
rep.p(f"   normalised: dphi'' + ({P1_}) dphi' + ({P0_}) dphi = 0")
R["route_N"] = {"P1": str(P1_), "P0": str(P0_)}
if okN:
    ok81a = zero_exact(P1_ - H)
    ok81b = zero_exact(P0_ - (HEAD * k**2 / a**2 + Hd))
    rep.check("C2 (CMV eq. 81): my route-N equation is dphi'' + H dphi' + (c_s^2 k^2/a^2 + H') dphi = 0 times f(t)",
              ok81a[0] and ok81b[0], f"H term: {ok81a[1]}; dphi term: {ok81b[1]}", kind="control (literature)")
    PkN = sp.Poly(sp.expand(P0_), k)
    cs2N = sp.simplify(a**2 * PkN.coeff_monomial(k**2))
    restN = sp.simplify(PkN.coeff_monomial(1) - Hd)
    okc = zero_exact(cs2N - HEAD)
    rep.check("H-a (M2 route N): c_s^2 (gradient coefficient of the dphi equation) = gt/(2 - 3 gt) exactly",
              okc[0] and not cs2N.has(a), f"{cs2N} ({okc[1]}); rest of dphi coefficient minus H' = {restN}")
    R["route_N"]["cs2"] = str(cs2N)
    ok82 = zero_exact(cs2N - HEAD)
    rep.check("C2 (CMV eq. 82): c_s^2 = gamma/(2 - 3 gamma) with gamma_CMV = gt", ok82[0], cs2N, kind="control (literature)")
    # C1 route N at gt = 0
    c1n = zero_exact(P0_.subs(gt, 0) - Hd)[0] and zero_exact(P1_.subs(gt, 0) - H)[0]
    rep.check("C1 (M2 route N, gt = 0, any V): dphi'' + H dphi' + H' dphi = 0 (no gradient term)", c1n, kind="control")
    # consistency of the other equations
    red = {2: sp.expand(-P1_ * dpd - P0_ * dp)}
    for n_ in range(3, 7):
        nxt = sp.expand(sp.diff(red[n_ - 1], t))
        nxt = sp.expand(nxt.subs(sp.Derivative(dp, (t, 2)), red[2]))
        red[n_] = nxt
    sdl = sp.solve(sp.expand(EL["Phi"].subs(sub1).doit()), ft["dlam"])
    cons = {}
    for nm_ in ("Psi", "E", "dphi"):
        ex_ = EL[nm_].subs(sub1).doit()
        if sdl:
            ex_ = ex_.subs(ft["dlam"], sdl[0]).doit()
        ex_ = sp.expand(ex_)
        for n_ in range(6, 1, -1):
            ex_ = ex_.subs(sp.Derivative(dp, (t, n_)), red[n_])
        cons[nm_] = sp.simplify(ex_)
    rep.p(f"   dlambda from the Phi equation: {len(sdl)} solution(s)")
    rep.check("route N: the Psi, E and dphi equations are then satisfied (consistency)",
              len(sdl) == 1 and all(v == 0 for v in cons.values()), cons, kind="method check")
else:
    for nm_ in ("C2 (CMV eq. 81)", "H-a (M2 route N)", "C2 (CMV eq. 82)", "C1 (M2 route N)", "route N consistency"):
        rep.check(nm_, False, "route N did not give a second-order dphi equation")

# ------------------------------------------------------------------ 6. H-c windows (M2 route U)
rep.p("\n== 6. H-c windows from route U (A and c_s^2), solved exactly as sets")
if U["reduced"]:
    Re = sp.S.Reals
    Ag = sp.simplify(U["A"].subs({Mp2: 1}).subs(a, 1))
    cg = sp.simplify(U["cs2"])
    ghost = sp.Intersection(sp.solveset(Ag < 0, gt, Re), sp.solveset(cg > 0, gt, Re))
    grad = sp.Intersection(sp.solveset(Ag > 0, gt, Re), sp.solveset(cg < 0, gt, Re))
    healthy = sp.Intersection(sp.solveset(Ag > 0, gt, Re), sp.solveset(cg > 0, gt, Re))
    rep.check("H-c (M2): ghost set is exactly 0 < gt < 2/3", ghost == sp.Interval.open(0, sp.Rational(2, 3)), ghost)
    rep.check("H-c (M2): gradient-unstable set is exactly gt < 0 or gt > 2/3",
              grad == sp.Union(sp.Interval.open(-sp.oo, 0), sp.Interval.open(sp.Rational(2, 3), sp.oo)), grad)
    rep.check("H-c (M2): ghost-free and gradient-stable set is empty", healthy == sp.S.EmptySet, healthy)
    bgcoef = sp.simplify(V_sol / (Mp2 * (2 * Hd + 3 * H**2) / 2))
    rep.p(f"   background coefficient V / (M_P^2 (2H' + 3H^2)/2) = {bgcoef} (vanishes at gt = 2/3 in the main run)")
    R["windows_M2"] = {"ghost": str(ghost), "gradient": str(grad), "healthy": str(healthy)}
else:
    for nm_ in ("H-c (M2) ghost", "H-c (M2) gradient", "H-c (M2) healthy"):
        rep.check(nm_, False, "no reduced form")

rc = rep.finish()
sys.exit(rc)
