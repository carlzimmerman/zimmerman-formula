#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG319 -- THE SLOWLY MOVING BLACK HOLE (gate G11's named condition) FOR THE FILTERED C-H/K CHASSIS.
Criteria frozen and committed first: campaign_fresh_gravity/CFG319_moving_black_hole/FROZEN_CRITERIA.md (5c8f4d640).

Chassis (CFG291/CFG318 map): alpha = c14 = alpha_c, beta = c13 = 0, lambda = c2 = c_2; window L340 P1.
Scope: TEST-KHRONON LIMIT -- the khronon on fixed Schwarzschild (ingoing EF, M = 1). The metric response (O(alpha)
outside the boundary layer of width ~0.61 M/c_S around the universal horizon, O(lambda) mixing inside it) is not
included. Stationary O(v) l = 1 perturbation: T = v + H(r) + v F(r) cos(theta), F -> -r (khronon moving at -v).

DERIVED HERE (sympy): the angle-integrated quadratic Lagrangian L2 = sum S_ij F^(i) F^(j) from
sqrt(-g)[-lambda K^2 - beta K_mn K^mn + alpha a.a] (covariant, with beta) and, separately, without the beta term (C8);
the linear operators dK and d(a.a); the static background equations from the reduced Lagrangian.
NUMERICS (cfg319_lib.py): truncated-power-series local-Taylor marching at 30+ digits; Frobenius series at the spin-0
horizon r_S and at the universal horizon r_UH; matching of the r_S-regular space with the no-r^3 space; UH options.

CFG319_MUTATE=1: the UH boundary condition is set WRONG (the s+ mode is declared admissible). The independent gradient
check on the marched solution must catch it (rc = 1). Outputs carry _MUTATE.
Run from anywhere:  python3 campaign_fresh_gravity/CFG319_moving_black_hole/cfg319_moving_bh.py
"""
import os, sys, json, math, time, pickle
import multiprocessing as mpr
import mpmath as mp
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import cfg319_lib as LB
from cfg319_lib import T

MUTATE = os.environ.get("CFG319_MUTATE", "0") == "1"
SLUG = "cfg319_moving_bh"
SUFFIX = "_MUTATE" if MUTATE else ""
P = lambda *a: print(*a, flush=True)
CH = []
OUT = {"lane": "CFG319", "mutate": MUTATE, "frozen_criteria_commit": "5c8f4d640", "checks": {}, "numbers": {}}
T0 = time.time()
DPS = 30
mp.mp.dps = DPS


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reading)'} {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 112); P(t); P("=" * 112)


def rel(p):
    return os.path.relpath(p, REPO)


# ================================================================================================ D1 symbolic
def derive_covariant(with_beta=True):
    """EF covariant computation; returns M_ij (r eliminated), dK, d(a.a) operator coefficients, static pieces."""
    _t = time.time()
    _lg = lambda m: P(f"      [derive {'beta' if with_beta else 'no-beta'}] {m} {time.time() - _t:.0f}s")
    v, r, th, ph, eps = sp.symbols('v r theta phi epsilon')
    al, la, be = sp.symbols('alpha lambda beta')
    Y, W = sp.symbols('Y W', positive=True)          # outside the UH: Y = -u.chi > 0, W = -u^r > 0
    Y1, W1 = sp.symbols('Y1 W1')
    P1, P2 = sp.symbols('P1 P2'); f0, f1, f2 = sp.symbols('f0 f1 f2'); c, s = sp.symbols('c s')
    e = 1 - 2 / r
    X = [v, r, th, ph]
    g = sp.Matrix([[-e, 1, 0, 0], [1, 0, 0, 0], [0, 0, r**2, 0], [0, 0, 0, r**2 * sp.sin(th)**2]]); gi = g.inv()
    Hf = sp.Function('H')(r); Ff = sp.Function('F')(r)
    Tk = v + Hf + eps * Ff * sp.cos(th)
    dT = [sp.diff(Tk, x) for x in X]
    n2 = -sum(gi[i, j] * dT[i] * dT[j] for i in range(4) for j in range(4))
    Nl = 1 / sp.sqrt(n2)
    ud = [-d * Nl for d in dT]
    uu = [sum(gi[i, j] * ud[j] for j in range(4)) for i in range(4)]
    sqrtg = r**2 * sp.sin(th)
    K = sum(sp.diff(sqrtg * uu[i], X[i]) for i in range(4)) / sqrtg
    dlnN = [sp.diff(sp.log(Nl), x) for x in X]
    udl = sum(uu[i] * dlnN[i] for i in range(4))
    a_d = [dlnN[i] + ud[i] * udl for i in range(4)]
    a2 = sum(gi[i, j] * a_d[i] * a_d[j] for i in range(4) for j in range(4))
    KK = sp.Integer(0)
    if with_beta:
        Gam = [[[sp.simplify(sum(gi[a_, d] * (sp.diff(g[d, b_], X[c_]) + sp.diff(g[d, c_], X[b_]) - sp.diff(g[b_, c_], X[d]))
                                 / 2 for d in range(4))) for c_ in range(4)] for b_ in range(4)] for a_ in range(4)]
        Du = [[sp.diff(ud[nu], X[mu]) - sum(Gam[rho][mu][nu] * ud[rho] for rho in range(4)) for nu in range(4)] for mu in range(4)]
        Kdd = [[Du[mu][nu] + ud[mu] * a_d[nu] for nu in range(4)] for mu in range(4)]
        KK = sum(gi[m1, m2] * gi[n1, n2] * Kdd[m1][n1] * Kdd[m2][n2] for m1 in range(4) for m2 in range(4)
                 for n1 in range(4) for n2 in range(4) if gi[m1, m2] != 0 and gi[n1, n2] != 0)

    def alg(ex):
        ex = ex.subs({Ff.diff(r, 2): f2}).subs({Ff.diff(r): f1}).subs({Ff: f0})
        ex = ex.subs({Hf.diff(r, 2): P2}).subs({Hf.diff(r): P1})
        ex = ex.subs({sp.sin(2 * th): 2 * sp.sin(th) * sp.cos(th), sp.cos(2 * th): 2 * sp.cos(th)**2 - 1,
                      sp.cot(th): sp.cos(th) / sp.sin(th), sp.tan(th): sp.sin(th) / sp.cos(th)})
        return ex.subs({sp.cos(th): c, sp.sin(th): s})
    P1v = -1 / (Y * (Y + W))                      # H' for the static khronon, regular at the Killing horizon
    P2v = sp.diff(P1v, Y) * Y1 + sp.diff(P1v, W) * W1

    def bg(ex):
        return ex.subs({P2: P2v}).subs({P1: P1v})
    _lg('geometry built')
    K0 = bg(alg(K.subs(eps, 0))); a20 = bg(alg(a2.subs(eps, 0))); KK0 = bg(alg(KK.subs(eps, 0)))
    K1 = bg(alg(sp.diff(K, eps).subs(eps, 0))); K2 = bg(alg(sp.diff(K, eps, 2).subs(eps, 0))) / 2
    A1 = bg(alg(sp.diff(a2, eps).subs(eps, 0))); A2 = bg(alg(sp.diff(a2, eps, 2).subs(eps, 0))) / 2
    KK2 = bg(alg(sp.diff(KK, eps, 2).subs(eps, 0))) / 2 if with_beta else sp.Integer(0)
    L2 = r**2 * (-la * (K1**2 + 2 * K0 * K2) - be * KK2 + al * A2)
    _lg('second-order pieces')
    rsub = 2 / (1 - Y**2 + W**2)
    M = {}
    for i, fi in enumerate((f0, f1, f2)):
        for j, fj in enumerate((f0, f1, f2)):
            if j < i:
                continue
            mij = sp.diff(L2, fi, fj) * (sp.Rational(1, 2) if i == j else 1)
            mij = sp.together(mij.subs(s**2, 1 - c**2)); num, den = sp.fraction(mij)
            num = sp.expand(sp.expand(num).subs(s**2, 1 - c**2)); num = sp.expand(num.subs(s, sp.sqrt(1 - c**2)))
            pc = sp.Poly(num, c)
            while den.has(c):
                fac = [ff for ff, mm in sp.factor_list(den)[1] if ff.has(c)][0]
                q, rem = sp.div(pc, sp.Poly(fac, c))
                assert rem.is_zero, 'non-polynomial angular dependence'
                pc = q; den = sp.cancel(den / fac)
            Ic = sp.integrate(pc.as_expr(), (c, -1, 1))
            M[str((i, j))] = sp.factor(sp.cancel(sp.together((Ic / den).subs(r, rsub))))
            _lg(f'M{(i, j)}')
    ops = None
    static = {'K0': K0, 'a20': a20, 'KK0': KK0}
    return M, ops, static, (r, Y, W, Y1, W1, al, la, be)


def derive_ops():
    """Linear operators dK and d(a.a) of the O(v) khronon perturbation, derived directly with the static khronon
    written through Y(r): H' = -1/(Y (Y + W)), W = sqrt(Y^2 - e), for which -g^{mn} dT0 dT0 = 1/Y^2 exactly."""
    v, r, th, ph, eps = sp.symbols('v r theta phi epsilon', positive=True)
    Yf = sp.Function('Y')(r); Ff = sp.Function('F')(r)
    e = 1 - 2 / r
    Wf = sp.sqrt(Yf**2 - e)
    Hp = -1 / (Yf * (Yf + Wf))
    X = [v, r, th, ph]
    g = sp.Matrix([[-e, 1, 0, 0], [1, 0, 0, 0], [0, 0, r**2, 0], [0, 0, 0, r**2 * sp.sin(th)**2]]); gi = g.inv()
    dT = [1, Hp + eps * Ff.diff(r) * sp.cos(th), -eps * Ff * sp.sin(th), 0]
    n2 = -sum(gi[i, j] * dT[i] * dT[j] for i in range(4) for j in range(4))
    n20Y2 = sp.simplify(n2.subs(eps, 0) * Yf**2)
    assert n20Y2 == 1, n20Y2
    n21 = sp.diff(n2, eps).subs(eps, 0)
    Nl = Yf * (1 - eps * Yf**2 * n21 / 2)                     # exact through O(eps)
    ud = [-d * Nl for d in dT]
    uu = [sum(gi[i, j] * ud[j] for j in range(4)) for i in range(4)]
    sqrtg = r**2 * sp.sin(th)
    K = sum(sp.diff(sqrtg * uu[i], X[i]) for i in range(4)) / sqrtg
    lnN = sp.log(Yf) + sp.log(1 - eps * Yf**2 * n21 / 2)
    dlnN = [sp.diff(lnN, x) for x in X]
    udl = sum(uu[i] * dlnN[i] for i in range(4))
    a_d = [dlnN[i] + ud[i] * udl for i in range(4)]
    a2 = sum(gi[i, j] * a_d[i] * a_d[j] for i in range(4) for j in range(4))
    Y, W, Y1 = sp.symbols('Y W Y1', positive=True); Y2 = sp.Symbol('Y2')
    f0, f1, f2 = sp.symbols('f0 f1 f2')

    def tosym(ex):
        ex = ex.subs({Ff.diff(r, 2): f2}).subs({Ff.diff(r): f1}).subs({Ff: f0})
        ex = ex.subs({Yf.diff(r, 2): Y2}).subs({Yf.diff(r): Y1}).subs({Yf: Y})
        return ex.subs(sp.sqrt(Y**2 - e), W)
    out = {}
    for nm, Q in (('K1', K), ('A1', a2)):
        Q1 = tosym(sp.diff(Q, eps).subs(eps, 0)) / sp.cos(th)
        co = [sp.factor(sp.cancel(sp.together(sp.diff(Q1, f).subs(r, 2 / (1 - Y**2 + W**2))))) for f in (f0, f1, f2)]
        assert not any(z.has(th) or z.has(Y2) for z in co), (nm, co)
        num = {Y: sp.Rational(3, 5), Y1: sp.Rational(1, 7), f0: sp.Rational(2, 3), f1: sp.Rational(-5, 11), f2: sp.Rational(3, 13)}
        rnum = sp.Rational(31, 10); num[W] = sp.sqrt(num[Y]**2 - (1 - 2 / rnum))
        lhs = sp.N(Q1.subs(r, rnum).subs(num), 40); rhs = sp.N(sum(cc * f for cc, f in zip(co, (f0, f1, f2))).subs(num), 40)
        assert abs(lhs - rhs) < 1e-30 * (1 + abs(lhs)), (nm, lhs, rhs)
        out[nm] = co
    return out


def derive_static():
    r = sp.Symbol('r', positive=True); al, la, be = sp.symbols('alpha lambda beta')
    from sympy.calculus.euler import euler_equations
    e = 1 - 2 / r
    Yf = sp.Function('Y')(r); Wf = sp.sqrt(Yf**2 - e)
    Kf = -sp.diff(r**2 * Wf, r) / r**2
    KKf = sp.diff(Wf, r)**2 + 2 * Wf**2 / r**2
    L = r**2 * (-la * Kf**2 - be * KKf + al * sp.diff(Yf, r)**2)
    E = euler_equations(L, [Yf], r)[0].lhs
    Y, Y1, Y2, W = sp.symbols('Y Y1 Y2 W')
    Ex = E.subs(sp.diff(Yf, r, 2), Y2).subs(sp.diff(Yf, r), Y1).subs(Yf, Y)
    Ex = sp.together(Ex.subs(sp.sqrt(Y**2 - e), W)); num = sp.expand(sp.numer(Ex))

    def redW(ex):
        p = sp.Poly(ex, W); out = 0
        for (k,), cc in p.terms():
            out += cc * (Y**2 - e)**(k // 2) * W**(k % 2)
        return sp.expand(out)
    A = sp.factor(redW(num.coeff(Y2, 1))); B = sp.factor(redW(sp.expand(num - num.coeff(Y2, 1) * Y2)))
    assert not A.has(W) and not B.has(W)
    Wg = sp.Function('W')(r); Yg = sp.sqrt(e + Wg**2)
    Kg = -sp.diff(r**2 * Wg, r) / r**2; KKg = sp.diff(Wg, r)**2 + 2 * Wg**2 / r**2
    Ew = euler_equations(r**2 * (-la * Kg**2 - be * KKg + al * sp.diff(Yg, r)**2), [Wg], r)[0].lhs
    W0, W1, W2 = sp.symbols('W0 W1 W2')
    W2sol = sp.factor(sp.simplify(sp.solve(Ew.subs(sp.diff(Wg, r, 2), W2).subs(sp.diff(Wg, r), W1).subs(Wg, W0), W2)[0]))
    W2sol = W2sol.subs({W0: sp.Symbol('W'), W1: sp.Symbol('W1')})
    return A, B, W2sol


# ================================================================================================ point pipeline
def run_point(task):
    """Full pipeline at one (alpha, lambda, beta). Returns a dict of numbers (strings for mp values)."""
    name, a, l, b, opt, sym = task
    mp.mp.dps = opt.get('dps', DPS)
    N = opt.get('N', 30); rho = mp.mpf(opt.get('rho', '0.25')); xf = mp.mpf(opt.get('x0frac', '0.25'))
    R0 = mp.mpf(10) ** opt.get('log10R0', 6); r_m = mp.mpf(6)
    t0 = time.time()
    md = LB.Model(sym, a, l, b)
    cS = mp.sqrt(md.lb / md.a)
    C0 = 3 * mp.sqrt(3) / 4
    U1 = lambda rr: mp.diff(lambda q: mp.sqrt(1 - 2 / q + C0**2 / q**4), rr)

    cache_in, cache_out = {}, {}

    def inner_shot(d):                                # depends on d only (cached)
        key = mp.nstr(d, mp.mp.dps)
        if key not in cache_in:
            rS = mp.mpf(1.5) + d / cS
            YS, Y1 = md.regular_data(rS, U1(rS))
            bi, _, fi, _ = LB.march(md, rS, r_m, [YS, Y1], None, 'Y', N, rho, with_X=False, singular_start=(YS, Y1))
            cache_in[key] = LB.to_W(r_m, *bi) if fi == 'Y' else bi
        return cache_in[key]

    def outer_shot(C):                                # depends on C only (cached)
        key = mp.nstr(C, mp.mp.dps)
        if key not in cache_out:
            bo, _, fo, _ = LB.march(md, R0, r_m, [C / R0**2, -2 * C / R0**3], None, 'W', N, rho, with_X=False)
            cache_out[key] = LB.to_W(r_m, *bo) if fo == 'Y' else bo
        return cache_out[key]

    def shots(d, C):
        bi = inner_shot(d); bo = outer_shot(C)
        return [bi[0] - bo[0], bi[1] - bo[1]]
    # coarse scan in d for a starting point, then Newton in (d, C)
    d = mp.mpf(opt.get('d_guess', '0.6')); C = C0 + mp.mpf('1e-3') / cS
    if 'd_scan' in opt:
        best = None
        for dd in opt['d_scan']:
            try:
                f = shots(mp.mpf(dd), C)
                if best is None or abs(f[1]) < best[0]:
                    best = (abs(f[1]), mp.mpf(dd))
            except Exception:
                pass
        d = best[1]
    hstep = mp.mpf(10) ** (-mp.mp.dps // 3)
    nrm = lambda f: max(abs(f[0]), abs(f[1]))
    f = shots(d, C)
    for it in range(80):                              # Newton with backtracking
        fd = shots(d + hstep, C); fC = shots(d, C + hstep)
        J = mp.matrix([[(fd[0] - f[0]) / hstep, (fC[0] - f[0]) / hstep], [(fd[1] - f[1]) / hstep, (fC[1] - f[1]) / hstep]])
        st = mp.lu_solve(J, mp.matrix([-f[0], -f[1]]))
        tstep = mp.mpf(1); improved = False
        for _ in range(30):
            try:
                fn = shots(d + tstep * st[0], C + tstep * st[1])
                if nrm(fn) < nrm(f):
                    improved = True
                    break
            except Exception:
                pass
            tstep /= 2
        if not improved:                              # at the precision floor: keep the current (d, C)
            break
        gain = nrm(f) / nrm(fn)
        d += tstep * st[0]; C += tstep * st[1]; f = fn
        if nrm(f) < mp.mpf(10) ** (-mp.mp.dps + 10) or (nrm(f) < mp.mpf('1e-17') and gain < 4):
            break                                     # converged, or only noise-level gains left
        if nrm(f) < mp.mpf(10) ** (-mp.mp.dps + 6) or max(abs(tstep * st[0]), abs(tstep * st[1])) < mp.mpf(10) ** (-mp.mp.dps + 8):
            break
    bg_resid = max(abs(z) for z in shots(d, C))
    rS = mp.mpf(1.5) + d / cS
    YS, Y1S = md.regular_data(rS, U1(rS))
    YtS, _ = md.bgY_series_rS(rS, YS, Y1S, N)
    static_exp = md.static_exponent_rS(rS, YS, Y1S)
    SS, bgS = md.S_series(rS, Yt=YtS)
    bS, shS, dropS = LB.theta_form(LB.scalar_coeffs(SS), 1, x_check=mp.mpf('0.25') * mp.mpf('0.61') / cS)
    rootsS = LB.indicial_roots(bS)
    # universal horizon: march inward, then Newton on local series
    dS_est = mp.mpf('0.61') / cS
    r = rS - min(mp.mpf('0.9') * dS_est, (rS - 1) * mp.mpf('0.5'))
    y, _, _, _ = LB.march(md, rS, r, [YS, Y1S], None, 'Y', N, rho, with_X=False, singular_start=(YS, Y1S))
    for it in range(20):
        Yt = md.bgY_series(r, y[0], y[1], N)
        dx = mp.findroot(lambda xx: Yt(xx), -y[0] / y[1], tol=mp.mpf(10) ** (-2 * mp.mp.dps + 20), verify=False)
        y = [Yt(dx), Yt.deriv()(dx)]; r = r + dx
        if abs(y[0]) < mp.mpf(10) ** (-mp.mp.dps + 6):
            break
    rU, YU1 = r, y[1]
    dS = rS - rU
    YtU = md.bgY_series(rU, 0, YU1, N)
    SU, bgU = md.S_series(rU, Yt=YtU)
    bU, shU, dropU = LB.theta_form(LB.scalar_coeffs(SU), 4, x_check=dS * xf)
    rootsU = [mp.re(z) for z in LB.indicial_roots(bU)]
    W0 = mp.sqrt(-(1 - 2 / rU))
    # closed form of the UH exponents: s(s+1)(2 y1^2 s^2 + 2 y1^2 s - (W0^2+1)^2) = 0
    spl = (-1 + mp.sqrt(1 + 2 * (W0**2 + 1)**2 / YU1**2)) / 2
    closed = sorted([-1 - spl, mp.mpf(-1), mp.mpf(0), spl])
    x0 = dS * xf
    # Frobenius solutions
    Rp, Rm = [], []
    for s in (0, 1, 2):
        f, _ = LB.frob(bS, mp.mpf(s), N)
        Rp.append(LB.ostro_from_F(SS, LB.frob_derivs(mp.mpf(s), f, x0), x0))
        Rm.append(LB.ostro_from_F(SS, LB.frob_derivs(mp.mpf(s), f, -x0), -x0))
    Xp = [[Rp[c][i] for c in range(3)] for i in range(4)]; Xm = [[Rm[c][i] for c in range(3)] for i in range(4)]
    modes = sorted(rootsU)
    Phi, fU = [], []
    for s in modes:
        f, res = LB.frob(bU, s, N)
        fU.append((s, f, res))
        Phi.append(LB.ostro_from_F(SU, LB.frob_derivs(s, f, x0), x0))
    PhiM = mp.matrix([[Phi[c][i] for c in range(4)] for i in range(4)])
    # marches
    bo, Xo, fo, no = LB.march(md, rS + x0, r_m, [YtS(x0), YtS.deriv()(x0)], Xp, 'Y', N, rho)
    bi, Xi, fi, ni = LB.march(md, rS - x0, rU + x0, [YtS(-x0), YtS.deriv()(-x0)], Xm, 'Y', N, rho)
    bgU_check = abs(bi[0] - YtU(x0))
    W0R, W1R = C / R0**2, -2 * C / R0**3
    WtR = md.bgW_series(R0, W0R, W1R, N)
    SR, _ = md.S_series(R0, Wt=WtR)
    d_ = lambda t: t.deriv()
    Iin = []
    for p in (1, 0, -2):
        Ft = T([mp.binomial(p, k) * R0**(p - k) for k in range(T.N)])
        p2 = 2 * (SR[(2, 0)] * Ft + SR[(2, 1)] * d_(Ft) + SR[(2, 2)] * d_(d_(Ft)))
        p1 = 2 * (SR[(1, 0)] * Ft + SR[(1, 1)] * d_(Ft) + SR[(1, 2)] * d_(d_(Ft))) - d_(p2)
        Iin.append([Ft.c[0], d_(Ft).c[0], p1.c[0], p2.c[0]])
    XI0 = [[Iin[c][i] for c in range(3)] for i in range(4)]
    bl, XI, fl, nl = LB.march(md, R0, r_m, [W0R, W1R], XI0, 'W', N, rho)
    bom = bo if fo == 'W' else LB.to_W(r_m, *bo); blm = bl if fl == 'W' else LB.to_W(r_m, *bl)
    bg_match = max(abs(bom[0] - blm[0]), abs(bom[1] - blm[1]))
    # Hamiltonian check (C6): symplectic products of the R solutions at the start and at r_m
    om0 = [LB.omega(Rp[i], Rp[j]) for (i, j) in ((0, 1), (0, 2), (1, 2))]
    om1 = [LB.omega([Xo[k][i] for k in range(4)], [Xo[k][j] for k in range(4)]) for (i, j) in ((0, 1), (0, 2), (1, 2))]
    om_dev = max(abs(o1 - o0) for o0, o1 in zip(om0, om1)) / max(abs(o) for o in om0)
    # matching R x I at r_m
    Mx = mp.matrix(4, 6)
    for i in range(4):
        for c in range(3):
            Mx[i, c] = Xo[i][c]; Mx[i, 3 + c] = -XI[i][c]
    sc = [mp.sqrt(mp.fsum(Mx[i, c]**2 for i in range(4))) for c in range(6)]
    Ms = mp.matrix(4, 6)
    for i in range(4):
        for c in range(6):
            Ms[i, c] = Mx[i, c] / sc[c]
    U_, Sv, V = mp.svd_r(Ms, full_matrices=True)
    null = [[V[k, c] / sc[c] for c in range(6)] for k in (4, 5)]

    def at_UH(vec):
        Xn = mp.matrix([mp.fsum(Xi[i][c] * vec[c] for c in range(3)) for i in range(4)])
        return LB.solve_scaled(PhiM, Xn)
    cU = [at_UH(vv) for vv in null]; Bc = [vv[3] for vv in null]
    i_sm, i_m1, i_0, i_sp = 0, 1, 2, 3          # modes sorted: s-, -1, 0, s+

    def option(kill):
        Ml = mp.matrix([[cU[0][kill], cU[1][kill]], [Bc[0], Bc[1]]])
        w = mp.lu_solve(Ml, mp.matrix([0, -1]))
        amps = [cU[0][i] * w[0] + cU[1][i] * w[1] for i in range(4)]
        Xm_ = [mp.fsum(Xo[k][c] * (null[0][c] * w[0] + null[1][c] * w[1]) for c in range(3)) for k in range(4)]
        Xn_ = [mp.fsum(Xi[k][c] * (null[0][c] * w[0] + null[1][c] * w[1]) for c in range(3)) for k in range(4)]
        return amps, Xm_, Xn_
    ampC, XCm, XCn = option(i_sm)
    ampCp, XCpm, XCpn = option(i_sp)
    # UH mode classification (section 3): powers of dK, d(a.a) and their radial gradients
    kk, aa = md.ops_series(bgU)

    def scalars(s, f, x):
        Fk = LB.frob_derivs(s, f, x, 4)
        kv = [t(x) for t in kk]; kd = [t.deriv()(x) for t in kk]
        av = [t(x) for t in aa]; ad = [t.deriv()(x) for t in aa]
        dK = kv[0] * Fk[0] + kv[1] * Fk[1] + kv[2] * Fk[2]
        gK = kd[0] * Fk[0] + (kv[0] + kd[1]) * Fk[1] + (kv[1] + kd[2]) * Fk[2] + kv[2] * Fk[3]
        dA = av[0] * Fk[0] + av[1] * Fk[1] + av[2] * Fk[2]
        gA = ad[0] * Fk[0] + (av[0] + ad[1]) * Fk[1] + (av[1] + ad[2]) * Fk[2] + av[2] * Fk[3]
        return dK, gK, dA, gA
    cls = []
    x1, x2 = x0 * mp.mpf('1e-4'), x0 * mp.mpf('1e-6')
    for (s, f, res) in fU:
        q1 = scalars(s, f, x1); q2 = scalars(s, f, x2)
        pw = [mp.log(abs(q1[k]) / abs(q2[k])) / mp.log(x1 / x2) if q1[k] != 0 and q2[k] != 0 else mp.inf for k in range(4)]
        xFsmooth = abs((s + 1) - mp.nint(s + 1)) < mp.mpf('1e-8') and s + 1 >= -mp.mpf('1e-8')
        tolp = mp.mpf('-0.02')
        bounded = pw[0] > tolp and pw[2] > tolp
        grads_bounded = pw[1] > tolp and pw[3] > tolp
        integrable = min(pw[1], pw[3]) > -1
        if xFsmooth and bounded and grads_bounded:
            kind = 'regular'
        elif bounded and integrable:
            kind = 'weakly singular'
        else:
            kind = 'strongly singular'
        cls.append({'s': mp.nstr(s, 12), 'pow_dK': mp.nstr(pw[0], 6), 'pow_gradK': mp.nstr(pw[1], 6),
                    'pow_dA': mp.nstr(pw[2], 6), 'pow_gradA': mp.nstr(pw[3], 6), 'xF_smooth': bool(xFsmooth),
                    'kind': kind, 'log_free': all(abs(rr_) < mp.mpf(10) ** (-mp.mp.dps // 3) for _, rr_ in res)})
    # gradient coefficient of the unit s+ mode (for breakdown radii): gradA ~ g x^p
    s_p, f_p, _ = fU[i_sp]
    qq = scalars(s_p, f_p, x2)
    p_gA = mp.mpf(cls[i_sp]['pow_gradA']); g_gA = abs(qq[3]) / x2**p_gA
    # background grad(a.a) at the UH: a.a = Y'^2 there (h^rr = Y^2)
    Y2U = YtU.c[2] * 2
    grad_aa_bg = abs(2 * YU1 * Y2U)
    # independent divergence check on the marched option-C solution: march it inward toward the UH
    xa, xb = x0 * mp.mpf('1e-2'), x0 * mp.mpf('1e-3')
    _, XCa, _, _ = LB.march(md, rU + x0, rU + xa, [YtU(x0), YtU.deriv()(x0)], [[z] for z in XCn], 'Y', N, rho)
    _, XCb, _, _ = LB.march(md, rU + xa, rU + xb, [YtU(xa), YtU.deriv()(xa)], XCa, 'Y', N, rho)

    def gradA_from_X(X, x):
        Sv = {k: v(x) for k, v in SU.items()}
        Fv = [X[0][0], X[1][0], LB.F2_from_ostro(Sv, [X[i][0] for i in range(4)])]
        # F''' from differentiating the F'' relation numerically along the series: use the local mode expansion
        cvec = LB.solve_scaled(mp.matrix([[LB.ostro_from_F(SU, LB.frob_derivs(s, f, x), x)[i] for (s, f, _) in fU]
                                          for i in range(4)]), mp.matrix([X[i][0] for i in range(4)]))
        tot = [mp.fsum(cvec[j] * LB.frob_derivs(fU[j][0], fU[j][1], x, 4)[k] for j in range(4)) for k in range(4)]
        av = [t(x) for t in aa]; ad = [t.deriv()(x) for t in aa]
        return ad[0] * tot[0] + (av[0] + ad[1]) * tot[1] + (av[1] + ad[2]) * tot[2] + av[2] * tot[3], cvec
    gA_a, cva = gradA_from_X(XCa, xa); gA_b, cvb = gradA_from_X(XCb, xb)
    growth = abs(gA_b) / abs(gA_a)
    # exterior: option C dK at r_m and the C - C' difference
    Ym = LB.to_Y(r_m, *bom)
    Tm = md.bgY_series(r_m, Ym[0], Ym[1], 6)
    Sm, bgm = md.S_series(r_m, Yt=Tm)
    km, _ = md.ops_series(bgm)
    Smv = {k: v(0) for k, v in Sm.items()}
    F2C = LB.F2_from_ostro(Smv, XCm); F2Cp = LB.F2_from_ostro(Smv, XCpm)
    dK_C = km[0](0) * XCm[0] + km[1](0) * XCm[1] + km[2](0) * F2C
    dK_Cp = km[0](0) * XCpm[0] + km[1](0) * XCpm[1] + km[2](0) * F2Cp
    out = {
        'name': name, 'alpha': str(md.a), 'lambda': str(md.l), 'beta': str(md.b), 'cS_testkhronon': mp.nstr(cS, 10),
        'd': mp.nstr(d, 15), 'C': mp.nstr(C, 15), 'rS': mp.nstr(rS, 15), 'rUH': mp.nstr(rU, 15), 'dS': mp.nstr(dS, 10),
        'dS_cS': mp.nstr(dS * cS, 10), 'YU1': mp.nstr(YU1, 12), 'bg_resid': mp.nstr(bg_resid, 3),
        'bg_match_rm': mp.nstr(bg_match, 3), 'bgU_check': mp.nstr(bgU_check, 3), 'static_exp_rS': mp.nstr(static_exp, 6),
        'rootsS': [mp.nstr(z, 10) for z in rootsS], 'dropped_rS': mp.nstr(dropS, 3), 'dropped_UH': mp.nstr(dropU, 3), 'rootsU': [mp.nstr(z, 14) for z in modes],
        'rootsU_closed': [mp.nstr(z, 14) for z in closed],
        'rootsU_dev': mp.nstr(max(abs(x_ - y_) for x_, y_ in zip(sorted(modes), closed)), 3),
        'rootsS_dev': mp.nstr(max(abs(mp.re(x_) - y_) + abs(mp.im(x_)) for x_, y_ in zip(sorted(rootsS, key=lambda z: mp.re(z)), [0, 1, 1, 2])), 3),
        'sv_RI': [mp.nstr(z, 5) for z in Sv], 'steps': [no, ni, nl], 'omega_dev': mp.nstr(om_dev, 3),
        'optC': [mp.nstr(z, 12) for z in ampC], 'optCp': [mp.nstr(z, 12) for z in ampCp],
        'sing_ratio_C': mp.nstr(abs(ampC[i_sp]) * dS**modes[i_sp] / max(abs(ampC[i_0]), abs(ampC[i_m1]) / dS), 6),
        'sing_ratio_Cp': mp.nstr(abs(ampCp[i_sm]) * dS**modes[i_sm] / max(abs(ampCp[i_0]), abs(ampCp[i_m1]) / dS), 6),
        'classes': cls, 'p_gradA_splus': mp.nstr(p_gA, 8), 'g_gradA_splus': mp.nstr(g_gA, 8),
        'grad_aa_bg_UH': mp.nstr(grad_aa_bg, 8),
        'marched_gradA_growth_x10': mp.nstr(growth, 8),
        'marched_splus_amp_a': mp.nstr(cva[i_sp], 10), 'marched_splus_amp_b': mp.nstr(cvb[i_sp], 10),
        'dK_rm_C': mp.nstr(dK_C, 10), 'dK_rm_Cp': mp.nstr(dK_Cp, 10), 'proxy_r2dK_C': mp.nstr(r_m**2 * dK_C, 10),
        'F_rm_C': mp.nstr(XCm[0], 14), 'F_rm_Cp': mp.nstr(XCpm[0], 14),
        'ext_diff_C_Cp': mp.nstr(abs(XCm[0] - XCpm[0]) / abs(XCm[0]), 6),
        'time_s': round(time.time() - t0, 1), 'opt': {k: v for k, v in opt.items() if k != 'd_scan'},
    }
    return out


def run_point_safe(task):
    try:
        return run_point(task)
    except Exception as exc:                          # recorded, never hidden
        import traceback
        return {'name': task[0], 'error': repr(exc), 'traceback': traceback.format_exc()}


# ================================================================================================ controls (serial)
def control_alpha0(sym, lam=mp.mpf('0.05')):
    """C1: the alpha = 0 stealth solution (dK = 0) on the exact maximal slicing; checked against the alpha = 0
    4th-order Ostrogradsky system."""
    N = 30
    md = LB.Model(sym, 0, lam, 0)
    C0 = 3 * mp.sqrt(3) / 4

    def Useries(r0):
        T.N = N
        r = T.var(r0)
        return (r - mp.mpf(1.5)) * LB.tsqrt(r * r + r + mp.mpf(3) / 4) / (r * r)
    rU = mp.mpf(1.5)
    Ut = Useries(rU)
    _, bgt = md.S_series(rU, Yt=Ut)
    kk, _ = md.ops_series(bgt)
    # 2nd-order sub-equation k2 F'' + k1 F' + k0 F = 0
    b2, sh2, _ = LB.theta_form([kk[0], kk[1], kk[2]], 3, order=2)
    roots2 = [mp.re(z) for z in LB.indicial_roots(b2)]
    sp_ = max(roots2)
    f, res = LB.frob(b2, sp_, N)
    x0 = mp.mpf('0.1')
    F = [LB.frob_derivs(sp_, f, x0, 2)]

    def march2(r0, r1, Fv):
        r = mp.mpf(r0); r1 = mp.mpf(r1); y = list(Fv)
        while r < r1:
            Ut_ = Useries(r)
            _, bgt_ = md.S_series(r, Yt=Ut_)
            k_, _ = md.ops_series(bgt_)
            # F'' = -(k1 F' + k0 F)/k2 as a linear first-order system
            inv = k_[2].inv()
            A = [[T.const(0), T.const(1)], [-k_[0] * inv, -k_[1] * inv]]
            Xc = [[[y[0]], [y[1]]]]
            for k in range(N - 1):
                nxt = [mp.mpf(0), mp.mpf(0)]
                for i in range(2):
                    for j in range(2):
                        nxt[i] += mp.fsum(A[i][j].c[k - m] * Xc[m][j][0] for m in range(k + 1))
                Xc.append([[nxt[0] / (k + 1)], [nxt[1] / (k + 1)]])
            Rc = min(LB.radius(inv), r * mp.mpf('0.9'), (r - mp.mpf(1.5)) * mp.mpf('0.9'))
            h = min(mp.mpf('0.25') * Rc, r1 - r)
            y = [mp.fsum(Xc[k][0][0] * h**k for k in range(N)), mp.fsum(Xc[k][1][0] * h**k for k in range(N))]
            r += h
        return y
    Fa = march2(rU + x0, 3, F[0])
    Fb = march2(3, 5, Fa)
    Fc = march2(5, 1000, Fb)
    Fd = march2(1000, 4000, Fc)
    ratio = (Fd[0] / 4000) / (Fc[0] / 1000)
    # 4th-order consistency: Ostrogradsky vector of the stealth at r = 3 marched with the alpha = 0 system to r = 5

    def ostro_at(r0, Fv):
        Ut_ = Useries(r0)
        S, bgt_ = md.S_series(r0, Yt=Ut_)
        k_, _ = md.ops_series(bgt_)
        kv = [t(0) for t in k_]; kd = [t.deriv()(0) for t in k_]
        F2 = -(kv[1] * Fv[1] + kv[0] * Fv[0]) / kv[2]
        F3 = -(kd[1] * Fv[1] + kv[1] * F2 + kd[0] * Fv[0] + kv[0] * Fv[1] + kd[2] * F2) / kv[2]
        return LB.ostro_from_F(S, [Fv[0], Fv[1], F2, F3], mp.mpf(0))
    X3 = ostro_at(mp.mpf(3), Fa)
    Ut3 = Useries(mp.mpf(3))
    _, X5, _, _ = LB.march(md, 3, 5, [Ut3(0), Ut3.deriv()(0)], [[z] for z in X3], 'Y', N, mp.mpf('0.25'))
    X5s = ostro_at(mp.mpf(5), Fb)
    dev4 = max(abs(X5[i][0] - X5s[i]) / max(abs(z) for z in X5s) for i in range(4))
    return {'roots2': [mp.nstr(z, 14) for z in roots2], 'sqrt2m1': mp.nstr(mp.sqrt(2) - 1, 14),
            'root_dev': mp.nstr(abs(sp_ - (mp.sqrt(2) - 1)), 3), 'F_over_r_1000': mp.nstr(Fc[0] / 1000, 12),
            'F_over_r_ratio_4000_1000': mp.nstr(ratio, 12), 'dev_4th_order': mp.nstr(dev4, 3),
            'res_flags': [(n, mp.nstr(v, 3)) for n, v in res]}


def control_toy():
    """C3: L = (1/2)(D phi)^2, D phi = ((r^2-2r) phi')' - 2 phi; the regular, no-r^3, normalised solution is phi = r - 1."""
    N = 30
    rho = mp.mpf('0.25')

    def S_toy(r0):
        T.N = N
        r = T.var(r0)
        a_ = r * r - 2 * r; b_ = 2 * r - 2; c_ = T.const(-2)
        h = mp.mpf('0.5')
        S = {(2, 2): a_ * a_ * h, (1, 2): a_ * b_ * h, (0, 2): a_ * c_ * h, (1, 1): b_ * b_ * h, (0, 1): b_ * c_ * h, (0, 0): c_ * c_ * h}
        for (i, j) in list(S):
            S[(j, i)] = S[(i, j)]
        return S

    def march_toy(r0, r1, X):
        r = mp.mpf(r0); r1 = mp.mpf(r1); sgn = 1 if r1 > r else -1
        while (r1 - r) * sgn > 0:
            S = S_toy(r)
            Rc = min(LB.radius(S[(2, 2)].inv()), abs(r - 2) * mp.mpf('0.9'), abs(r) * mp.mpf('0.9'))
            h = min(rho * Rc, abs(r1 - r)) * sgn
            X = LB.eval_X(LB.X_series(LB.A_series(S), X), h); r += h
        return X
    S2 = S_toy(mp.mpf(2))
    b, sh, _ = LB.theta_form(LB.scalar_coeffs(S2), 2)
    roots = LB.indicial_roots(b)
    x0 = mp.mpf('0.5')
    R = []
    for s in (0, 1):
        f, _ = LB.frob(b, mp.mpf(s), N)
        R.append(LB.ostro_from_F(S2, LB.frob_derivs(mp.mpf(s), f, x0), x0))
    XR = march_toy(2 + x0, 6, [[R[c][i] for c in range(2)] for i in range(4)])
    R0 = mp.mpf(10)**6
    S0 = S_toy(R0); d = lambda t: t.deriv(); Iin = []
    for p in (1, 0, -2):
        Ft = T([mp.binomial(p, k) * R0**(p - k) for k in range(N)])
        p2 = 2 * (S0[(2, 0)] * Ft + S0[(2, 1)] * d(Ft) + S0[(2, 2)] * d(d(Ft)))
        p1 = 2 * (S0[(1, 0)] * Ft + S0[(1, 1)] * d(Ft) + S0[(1, 2)] * d(d(Ft))) - d(p2)
        Iin.append([Ft.c[0], d(Ft).c[0], p1.c[0], p2.c[0]])
    XI = march_toy(R0, 6, [[Iin[c][i] for c in range(3)] for i in range(4)])
    M = mp.matrix(4, 5)
    for i in range(4):
        for c in range(2):
            M[i, c] = XR[i][c]
        for c in range(3):
            M[i, 2 + c] = -XI[i][c]
    sc = [mp.sqrt(mp.fsum(M[i, j]**2 for i in range(4))) for j in range(5)]
    Ms = mp.matrix(4, 5)
    for i in range(4):
        for j in range(5):
            Ms[i, j] = M[i, j] / sc[j]
    U_, S_, V = mp.svd_r(Ms, full_matrices=True)
    nv = [V[4, j] / sc[j] for j in range(5)]
    phi6 = (XR[0][0] * nv[0] + XR[0][1] * nv[1]) / nv[2]
    return {'roots': [mp.nstr(z, 10) for z in roots], 'phi6': mp.nstr(phi6, 18), 'dev': mp.nstr(abs(phi6 - 5), 3)}


# ================================================================================================ main
if __name__ == "__main__":
    P(__doc__.strip())
    if MUTATE:
        P("\n  *** MUTATE=1: the s+ mode at the universal horizon is DECLARED ADMISSIBLE (wrong boundary condition); the "
          "independent gradient check must catch it (rc = 1) ***")
    L340F = os.path.join(REPO, "real_research", "g03_audit_2026", "L340_filtered_khronon_completion_results.json")
    C318F = os.path.join(REPO, "campaign_fresh_gravity", "CFG318_strong_field_bh", "cfg318_strong_field_bh_results.json")
    L340 = json.load(open(L340F)); C318 = json.load(open(C318F))
    AMIN, AMAX = L340["numbers"]["P1"]["alpha_c_min"], L340["numbers"]["P1"]["alpha_c_max"]
    LMIN, LMAX = L340["numbers"]["P1"]["c2_min"], L340["numbers"]["P1"]["c2_max"]
    ACEN, LCEN = math.sqrt(AMIN * AMAX), math.sqrt(LMIN * LMAX)
    P(f"\n  inputs ({rel(L340F)}): alpha_c in [{AMIN:.6e}, {AMAX:.3e}], c_2 in [{LMIN:.6e}, {LMAX:.6e}]")
    P(f"  CFG318 dipole: min s_crit/alpha_c = {C318['numbers']['dipole']['min_scrit_over_alpha']:.4e}")
    OUT["numbers"]["inputs"] = {"alpha_c": [AMIN, AMAX], "c2": [LMIN, LMAX], "centre": [ACEN, LCEN],
                                "sources": [rel(L340F), rel(C318F)]}

    # ---------------------------------------------------------------- D1 symbolic
    banner("D1  SYMBOLIC: angle-integrated quadratic Lagrangian (covariant, with beta), dK and d(a.a) operators, static equations")
    t1 = time.time()
    Mcov, _, stat, syms = derive_covariant(with_beta=True)
    ops = derive_ops()
    P(f"    covariant derivation with beta: {time.time() - t1:.0f} s")
    P(f"    S22 = M(2,2) = {Mcov['(2, 2)']}")
    Mnb, ops_nb, stat_nb, _ = derive_covariant(with_beta=False)
    P(f"    beta-free derivation: {time.time() - t1:.0f} s total")
    A_st, B_st, W2_st = derive_static()
    P(f"    static Y-form: A = {A_st}")
    r_, Y_, W_, Y1_, W1_, al_, la_, be_ = syms
    # C8: beta = 0 reduction, and the static pieces vs the covariant ones (numerically, at random points)
    dev8 = mp.mpf(0); devst = mp.mpf(0)
    import random
    random.seed(319)
    for _ in range(4):
        rv = mp.mpf(random.uniform(1.6, 9)); Yv = mp.mpf(random.uniform(0.2, 0.95)); Y1v = mp.mpf(random.uniform(-0.5, 0.5))
        ev = 1 - 2 / rv
        if Yv**2 - ev <= 0:
            Yv = mp.sqrt(ev) + mp.mpf('0.1')
        Wv = mp.sqrt(Yv**2 - ev); W1v = (Yv * Y1v - 1 / rv**2) / Wv
        sb = {Y_: Yv, W_: Wv, Y1_: Y1v, W1_: W1v, al_: mp.mpf('0.013'), la_: mp.mpf('0.07'), be_: 0}
        for k in Mcov:
            x1 = sp.N(Mcov[k].subs(sb), DPS); x2 = sp.N(Mnb[k].subs(sb), DPS)
            dev8 = max(dev8, abs(mp.mpf(str(x1)) - mp.mpf(str(x2))) / (abs(mp.mpf(str(x2))) + mp.mpf('1e-40')))
        sbr = dict(sb); sbr[r_] = rv
        K0v = mp.mpf(str(sp.N(stat['K0'].subs(sbr), DPS))); KK0v = mp.mpf(str(sp.N(stat['KK0'].subs(sbr), DPS)))
        a20v = mp.mpf(str(sp.N(stat['a20'].subs(sbr), DPS)))
        devst = max(devst, abs(K0v - (-2 * Wv / rv - W1v)), abs(KK0v - (W1v**2 + 2 * Wv**2 / rv**2)), abs(a20v - Y1v**2))
    check("C8 beta = 0 reduction: the covariant S_ij at beta = 0 equal the beta-free derivation (4 random points); the static "
          "K, K_mn K^mn, a.a match the reduced forms K = -2W/r - W', K.K = W'^2 + 2W^2/r^2, a.a = Y'^2",
          f"max rel dev {mp.nstr(dev8, 3)}; static {mp.nstr(devst, 3)}", dev8 < mp.mpf('1e-20') and devst < mp.mpf('1e-20'))
    SYM = {'M': {k: str(v) for k, v in Mcov.items()}, 'K1': [str(z) for z in ops['K1']], 'A1': [str(z) for z in ops['A1']],
           'A_static': str(A_st), 'B_static': str(B_st), 'W2_static': str(W2_st)}
    OUT["numbers"]["symbolic"] = {'S22': str(Mcov['(2, 2)']), 'dK_ops': SYM['K1'], 'daa_ops': SYM['A1'],
                                  'A_static': SYM['A_static'], 'B_static': SYM['B_static'], 'W2_static': SYM['W2_static']}
    P(f"    dK = k0 F + k1 F' + k2 F'': k0 = {ops['K1'][0]}, k2 = {ops['K1'][2]}")

    # ---------------------------------------------------------------- tasks
    banner("RUNS  W5 window points, alpha ladder (lambda = 0.05), RB2019 control point (beta = 0.01), C5 refinement")
    W5 = [("W5 corner a_max l_min", AMAX, LMIN), ("W5 corner a_max l_max", AMAX, LMAX), ("W5 corner a_min l_min", AMIN, LMIN),
          ("W5 corner a_min l_max", AMIN, LMAX), ("W5 centre", ACEN, LCEN)]
    def _dps(a, l):                                   # deep in the window (c_S > 1e4, boundary layer < 1e-4 M) use 40 digits
        return 40 if math.sqrt(l / a) > 1e4 else DPS
    tasks = [(nm, repr(a), repr(l), '0', {'d_guess': '0.61', 'dps': _dps(a, l)}, SYM) for nm, a, l in W5]
    if not MUTATE:
        tasks += [(f"ladder a={a}", a, '0.05', '0', {'d_guess': '0.6'}, SYM) for a in ('1e-3', '1e-4', '1e-5', '1e-6', '1e-7')]
        tasks += [("C2 RB2019 (0.02, 0.01, 0.1)", '0.02', '0.1', '0.01',
                   {'d_scan': [str(0.05 * k) for k in range(2, 30)]}, SYM)]
        tasks += [("C5 refined a_max l_min", repr(AMAX), repr(LMIN), '0',
                   {'d_guess': '0.61', 'N': 40, 'rho': '0.15', 'x0frac': '0.1666666666666666666667', 'log10R0': 8}, SYM)]
    nproc = min(len(tasks), max(1, (os.cpu_count() or 2) - 2))
    P(f"    {len(tasks)} runs on {nproc} processes")
    with mpr.get_context("spawn").Pool(nproc) as pool:
        async_c1 = pool.apply_async(control_alpha0, (SYM,)) if not MUTATE else None
        async_c3 = pool.apply_async(control_toy, ()) if not MUTATE else None
        results = []
        for res_ in pool.imap_unordered(run_point_safe, tasks, chunksize=1):
            results.append(res_)
            P(f"    finished: {res_['name']} ({'FAILED' if 'error' in res_ else str(res_.get('time_s')) + ' s'})")
        c1 = async_c1.get() if async_c1 else None
        c3 = async_c3.get() if async_c3 else None
    OUT["numbers"]["runs"] = {r_['name']: r_ for r_ in results}
    failed = [r_ for r_ in results if 'error' in r_]
    for r_ in failed:
        P(f"\n    -- {r_['name']}: RUN FAILED: {r_['error']}\n{r_['traceback']}")
    results = [r_ for r_ in results if 'error' not in r_]
    R = {r_['name']: r_ for r_ in results}
    check("RUNS all point runs completed", f"{len(failed)} failed: {[r_['name'] for r_ in failed]}", not failed)
    for r_ in results:
        P(f"\n    -- {r_['name']}: alpha={float(r_['alpha']):.4e} lambda={float(r_['lambda']):.4e} beta={r_['beta']} "
          f"c_S(test)={r_['cS_testkhronon']} ({r_['time_s']} s)")
        P(f"       r_S = {r_['rS']}, r_UH = {r_['rUH']}, (r_S - r_UH) c_S = {r_['dS_cS']}, C = {r_['C']}")
        P(f"       exponents r_S {r_['rootsS']} (dev {r_['rootsS_dev']}); UH {r_['rootsU']} (closed-form dev {r_['rootsU_dev']})")
        P(f"       bg resid {r_['bg_resid']}, bg match {r_['bg_match_rm']}, bg UH check {r_['bgU_check']}, Omega dev {r_['omega_dev']}, "
          f"static r_S exponent {r_['static_exp_rS']}, steps {r_['steps']}")
        P(f"       sv[R|I] {r_['sv_RI']}")
        P(f"       option C  (r_S regular, s- removed): c[s-, -1, 0, s+] = {r_['optC']}   singular/regular at r~dS: {r_['sing_ratio_C']}")
        P(f"       option C' (r_S regular, s+ removed): c[s-, -1, 0, s+] = {r_['optCp']}   singular/regular at r~dS: {r_['sing_ratio_Cp']}")
        for cl in r_['classes']:
            P(f"       UH mode s = {cl['s']:>16s}: dK ~ x^{cl['pow_dK']}, grad dK ~ x^{cl['pow_gradK']}, d(a.a) ~ x^{cl['pow_dA']}, "
              f"grad d(a.a) ~ x^{cl['pow_gradA']}, xF smooth {cl['xF_smooth']}, log-free {cl['log_free']} -> {cl['kind']}")
        P(f"       marched option-C solution toward the UH: |grad d(a.a)| grows x{r_['marched_gradA_growth_x10']} per decade "
          f"(s+ amplitude {r_['marched_splus_amp_a']} -> {r_['marched_splus_amp_b']})")
        P(f"       exterior r = 6M: F_C = {r_['F_rm_C']}, F_C' = {r_['F_rm_Cp']} (rel diff {r_['ext_diff_C_Cp']}); "
          f"r^2 dK_C = {r_['proxy_r2dK_C']}")

    # ---------------------------------------------------------------- controls
    banner("CONTROLS")
    ok_c1 = ok_c2 = ok_c3 = True
    if c1 is not None:
        P(f"    C1 alpha = 0: maximal-slicing sub-equation exponents {c1['roots2']} (sqrt2 - 1 = {c1['sqrt2m1']}); "
          f"F/r at r = 1000: {c1['F_over_r_1000']}, ratio F/r (4000 vs 1000) = {c1['F_over_r_ratio_4000_1000']}; "
          f"4th-order consistency dev {c1['dev_4th_order']}")
        ok_c1 = check("C1 alpha = 0: the stealth (dK = 0) solution exists (regular UH exponent sqrt2 - 1 to 1e-10, F ~ A r at large r, "
                      "A != 0, normalisable to -r with no r^3) and solves the alpha = 0 4th-order Ostrogradsky system (< 1e-12)",
                      f"root dev {c1['root_dev']}; F/r ratio {c1['F_over_r_ratio_4000_1000']}; 4th-order dev {c1['dev_4th_order']}",
                      float(c1['root_dev']) < 1e-10 and abs(float(c1['F_over_r_ratio_4000_1000']) - 1) < 1e-3
                      and abs(float(c1['F_over_r_1000'])) > 1e-3 and float(c1['dev_4th_order']) < 1e-12)
        OUT["numbers"]["C1"] = c1
    if c3 is not None:
        ok_c3 = check("C3 injection (toy L = (D phi)^2/2): exponents at r = 2 are {0, 0, 1, 1}; the regular, no-r^3, normalised "
                      "solution phi = r - 1 is recovered at r = 6 to 1e-12", f"roots {c3['roots']}; phi(6) = {c3['phi6']}",
                      float(c3['dev']) < 1e-12 and all(abs(float(mp.re(mp.mpc(z))) - t) < 1e-6 for z, t in zip(c3['roots'], [0, 0, 1, 1])))
        OUT["numbers"]["C3"] = c3
    if not MUTATE:
        rb = R.get("C2 RB2019 (0.02, 0.01, 0.1)", {'optC': ['nan'] * 4, 'optCp': ['nan'] * 4, 'sing_ratio_C': '0', 'sing_ratio_Cp': '0'})
        ok_c2 = check("C2 RB2019's point (0.02, 0.01, 0.1), beta included: no fully regular solution (both options keep a non-zero bad "
                      "amplitude) and the r_S-regular option is singular at the universal horizon (qualitative reproduction)",
                      f"option C s+ amp {rb['optC'][3]} (ratio {rb['sing_ratio_C']}); option C' s- amp {rb['optCp'][0]} (ratio {rb['sing_ratio_Cp']})",
                      float(rb['sing_ratio_C']) > 1e-6 and float(rb['sing_ratio_Cp']) > 1e-6)
    pts = [R[nm] for nm, _, _ in W5 if nm in R]
    allruns = [r_ for r_ in results]
    ok_c4 = check("C4 Frobenius: the leading coefficient vanishes to order 1 at r_S and 4 at the UH; UH exponents equal the closed form s(s+1)(2 y1^2 s^2 + 2 y1^2 s - (W0^2+1)^2) = 0 to 1e-10; r_S "
                  "exponents {0, 1, 1, 2} to 1e-6; the static r_S exponent is 0 (all runs)",
                  f"max UH dev (beta = 0 runs) {max(float(r_['rootsU_dev']) for r_ in allruns if float(r_['beta']) == 0):.1e}; max r_S dev "
                  f"{max(float(r_['rootsS_dev']) for r_ in allruns):.1e}; max |static exp| {max(abs(float(r_['static_exp_rS'])) for r_ in allruns):.1e}; "
                  f"zero orders (1 at r_S, 4 at UH) confirmed: dropped <= {max(max(float(r_['dropped_rS']), float(r_['dropped_UH'])) for r_ in allruns):.1e}",
                  all((float(r_['rootsU_dev']) < 1e-10 or float(r_['beta']) != 0) and float(r_['rootsS_dev']) < 1e-6
                      and abs(float(r_['static_exp_rS'])) < 1e-6 and float(r_['dropped_rS']) < 1e-12 and float(r_['dropped_UH']) < 1e-12
                      for r_ in allruns),
                  "the UH closed form is the beta = 0 one; the beta = 0.01 control run is exempt from that comparison only")
    ok_c6 = check("C6 Hamiltonian structure: symplectic products of the marched r_S-regular solutions constant to 1e-12 relative (all runs)",
                  f"max dev {max(float(r_['omega_dev']) for r_ in allruns):.1e}", all(float(r_['omega_dev']) < 1e-12 for r_ in allruns))
    ok_c7 = check("C7 background: two-sided matching residual < 1e-15; inward march vs UH series < 1e-14; r_m match of the O(v) "
                  "marches < 1e-14 (all runs)",
                  f"max resid {max(float(r_['bg_resid']) for r_ in allruns):.1e}, UH {max(float(r_['bgU_check']) for r_ in allruns):.1e}, "
                  f"r_m {max(float(r_['bg_match_rm']) for r_ in allruns):.1e}",
                  all(float(r_['bg_resid']) < 1e-15 and float(r_['bgU_check']) < 1e-14 and float(r_['bg_match_rm']) < 1e-14 for r_ in allruns))
    ok_c5 = True; c5_rel = None
    if not MUTATE:
        base = R.get("W5 corner a_max l_min"); ref = R.get("C5 refined a_max l_min")
        c5_rel = float('inf') if (base is None or ref is None) else None
    if not MUTATE and c5_rel is None:
        c5_rel = max(abs(float(base['optC'][3]) / float(ref['optC'][3]) - 1), abs(float(base['optCp'][0]) / float(ref['optCp'][0]) - 1))
        ok_c5 = check("C5 numerics at (alpha_max, lambda_min): c_s+ (option C) and c_s- (option C') change < 1e-3 relative under "
                      "N 30->40, rho 0.25->0.15, x0 dS/4->dS/6, R0 1e6->1e8", f"max rel change {c5_rel:.2e}", c5_rel < 1e-3,
                      "if this fails the amplitudes are readings and the verdict rests on the qualitative structure (frozen)",
                      load_bearing=False)
    elif not MUTATE:
        check("C5 numerics at (alpha_max, lambda_min)", "a run is missing", False, load_bearing=False)

    # ---------------------------------------------------------------- classification and verdict
    banner("VERDICT INPUTS  (frozen rule, section 5)")
    def kinds(r_):
        return {cl['s']: cl['kind'] for cl in r_['classes']}
    full_regular, optC_ok, splus_kind = [], [], []
    for r_ in pts:
        cl = r_['classes']
        k_sm, k_m1, k_0, k_sp = [c_['kind'] for c_ in cl]
        if MUTATE:
            k_sp = 'regular'                         # the WRONG boundary condition
        bad_C = float(r_['sing_ratio_C']) if k_sp != 'regular' else 0.0
        full_regular.append(bad_C < 1e-8 and k_m1 == 'regular' and k_0 == 'regular')
        optC_ok.append(k_m1 == 'regular' and k_0 == 'regular' and k_sp in ('regular', 'weakly singular'))
        splus_kind.append(k_sp)
        P(f"    {r_['name']}: UH kinds [s-, -1, 0, s+] = {[k_sm, k_m1, k_0, k_sp]}; option C singular/regular ratio "
          f"{r_['sing_ratio_C']} -> fully regular: {full_regular[-1]}; option C admissible: {optC_ok[-1]}")
    # independent divergence check on the marched solution (catches a wrong UH boundary condition)
    marched_div = [float(r_['marched_gradA_growth_x10']) > 1.5 for r_ in pts]
    if MUTATE:
        contradiction = any(fr and md_ for fr, md_ in zip(full_regular, marched_div))
        check("MUTATE: the bookkeeping (s+ declared admissible) claims a fully regular moving BH, but the independent check on the "
              "marched option-C solution finds grad d(a.a) diverging toward the UH -> contradiction flagged",
              f"bookkeeping regular {full_regular}; marched divergence {marched_div}", not contradiction,
              "required to FAIL in MUTATE (rc = 1)")
    # dipole: proxy x 10 against s_crit (CFG318 formula)
    def c0sq(a, l):
        return l * (2 - a) / (a * (2 + 3 * l))
    def Cdip(a, l):
        return 4 / (3 * c0sq(a, l)**1.5 * a * (2 - a))
    dip = []
    for r_ in pts:
        a_, l_ = float(r_['alpha']), float(r_['lambda'])
        scrit = math.sqrt(1e-4 * 32 / (5 * Cdip(a_, l_)))
        prox = abs(float(r_['proxy_r2dK_C']))
        dip.append((r_['name'], prox, scrit, 10 * prox < scrit))
        P(f"    dipole {r_['name']}: |r^2 dK| proxy = {prox:.3e}, x10 = {10 * prox:.3e} vs s_crit = {scrit:.3e} -> "
          f"{'pass' if 10 * prox < scrit else 'FAIL'} (proxy: the test-khronon limit has no metric response)")
    ok_dip = all(d_[3] for d_ in dip)
    # physical character: breakdown radii for M = 10 Msun, v = 1e-3
    Mkm = 14.77; vv = 1e-3
    phys = []
    for r_ in pts:
        p_ = float(r_['p_gradA_splus']); g_ = float(r_['g_gradA_splus']); c_ = abs(float(r_['optC'][3])); bgA = float(r_['grad_aa_bg_UH'])
        a_ = float(r_['alpha'])
        x_k = (bgA / (vv * c_ * g_))**(1 / p_) if p_ < 0 else float('nan')
        x_R = (1.0 / (a_ * vv * c_ * g_))**(1 / p_) if p_ < 0 else float('nan')
        phys.append({'name': r_['name'], 'x_khronon_nonlinear_M': x_k, 'x_khronon_nonlinear_m': x_k * Mkm * 1e3,
                     'x_curvature_order1_M': x_R, 'x_curvature_order1_m': x_R * Mkm * 1e3,
                     'rS_minus_rUH_M': float(r_['dS']), 'r_UH_M': float(r_['rUH']), 'r_S_M': float(r_['rS'])})
        P(f"    {r_['name']}: r_UH = {float(r_['rUH']):.9f} M, r_S - r_UH = {float(r_['dS']):.3e} M (inside r = 2M); for 10 Msun, v = 1e-3: "
          f"khronon gradient order-one at x < {x_k:.2e} M ({x_k * Mkm * 1e3:.2e} m); curvature order-one (alpha v amplitude) at x < "
          f"{x_R:.2e} M ({x_R * Mkm * 1e3:.2e} m)")
    OUT["numbers"]["physical"] = phys
    OUT["numbers"]["dipole"] = [{'name': n_, 'proxy': p_, 's_crit': s_, 'pass': ok_} for n_, p_, s_, ok_ in dip]

    load_ok = all(ok for _, ok, lb in CH if lb) if not MUTATE else all(ok for nm, ok, lb in CH if lb and not nm.startswith("MUTATE"))
    if not load_ok:
        verdict = "OPEN"
    elif all(full_regular) and ok_dip:
        verdict = "PASS"
    elif (not any(full_regular)) and all(optC_ok) and ok_dip:
        verdict = "CONDITIONAL"
    elif not all(optC_ok) or not ok_dip:
        verdict = "KILL"
    else:
        verdict = "OPEN"                             # mixed regular / non-regular across W5 (not anticipated by the rule)
    OUT["verdict"] = verdict
    OUT["numbers"]["verdict_inputs"] = {"full_regular": full_regular, "optC_admissible": optC_ok, "splus_kind": splus_kind,
                                        "marched_divergence": marched_div, "dipole_pass": ok_dip, "C5_rel_change": c5_rel}
    banner(f"VERDICT (frozen rule): {verdict}")
    if verdict == "CONDITIONAL":
        P("    No fully regular slowly moving BH at any W5 point. The r_S-regular solution (option C) is regular everywhere on")
        P("    (r_UH, inf) including r_S and r = 2M; its only singular content is the s+ mode ON the universal horizon: dK and")
        P("    d(a.a) bounded, their gradients diverging integrably (khronon stress-energy ~ alpha v x^(s+ - 1)).")
        P("    Owner flag: under RB2019/FHB2021's 'regular everywhere except r = 0' criterion this reads KILL.")
    npass = sum(1 for _, ok, _ in CH if ok)
    P(f"\n{npass}/{len(CH)} checks pass")
    OUT["checks_summary"] = f"{npass}/{len(CH)}"
    OUT["runtime_s"] = round(time.time() - T0, 1)
    with open(os.path.join(HERE, f"{SLUG}_results{SUFFIX}.json"), "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    rc = 0 if all(ok for _, ok, lb in CH if lb) else 1
    sys.exit(rc)
