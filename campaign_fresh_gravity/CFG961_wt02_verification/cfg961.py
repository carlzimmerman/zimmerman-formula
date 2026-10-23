"""CFG961 -- independent check of WT-02 (CFG938 parent on FRW; A5 c_T; cosmic clock) and WT-05 (CFG955/958) against CFG938.

Own sympy derivation from CFG938's action as written (DERIVATION §3.4):
  S = Int sqrt(-g)[c^4 R/16 pi G - m c^2 n - W_full(u) - (3 gamma/4K^2) tau_mn tau^mn + lambda(D_m D^m chi - K m n)] + S_b,
  D_a D_b chi = h_a^c h_b^d nabla_c nabla_d chi, D^2 = h^{mn} nabla_m nabla_n chi, u^2 = h^{mn} d chi d chi.
No WT-02 / WT-05 / CFG938 code is imported.  Criteria: FROZEN_CRITERIA.md (83b04219e).
Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg961.py            -> cfg961.out, cfg961_results.json
      CFG961_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg961.py -> cfg961_MUTATE.out, cfg961_results_MUTATE.json
kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import os, sys, json, math, time, resource, itertools
import numpy as np
import sympy as sp
import mpmath as mp
from sympy.calculus.euler import euler_equations
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("CFG961_REPO") or os.path.dirname(os.path.dirname(HERE))
LANES = os.path.join(REPO, "campaign_fresh_gravity")
MUT = os.environ.get("CFG961_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT, RES = [], {"checks": {}, "mutate": MUT}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def rss_mb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 1e6 if sys.platform == "darwin" else r / 1e3


def guard(where):
    if rss_mb() > 1000:
        P(f"RSS GUARD at {where}: {rss_mb():.0f} MB > 1000 MB; abort"); dump(); sys.exit(3)


def chk(name, ok, detail=""):
    RES["checks"][name] = dict(pass_=bool(ok), detail=detail)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return bool(ok)


def dump():
    RES["runtime_s"] = round(time.time() - T0, 1); RES["peak_rss_MB"] = round(rss_mb(), 1)
    json.dump(RES, open(os.path.join(HERE, f"cfg961_results{TAG}.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, f"cfg961{TAG}.out"), "w").write("\n".join(OUT) + "\n")


sys.path.insert(0, LANES)
import CFG4_common as C4                                                # record footings only
A0 = dict(C4.A0)
FOOTS = ("canonical", "alt")
C_SI, G_SI, MSUN, PC = 299792458.0, 6.67430e-11, 1.98847e30, 3.0856775814913673e16
KPC, MPC = 1e3 * PC, 1e6 * PC
K_SI = 4 * math.pi * G_SI
Ob, RAT, H0KMS = 0.0493, 5.364, 67.4                                    # CFG938's declared cosmological inputs
Oc0, Om0 = Ob * RAT, Ob * (1 + RAT); OL0 = 1 - Om0
H0_SI = H0KMS * 1e3 / MPC
LSTAR = {"24pc": 24 * PC, "1kpc": 1 * KPC}
P(f"CFG961 {'MUTATE' if MUT else 'MAIN'} run; footings {A0}; Omega_c {Oc0:.5f}, Omega_m {Om0:.5f}, H0 {H0KMS}")

# =============================================================================================== truncated eps-series algebra
N_ORD = 2


class S:
    """Truncated power series in epsilon: coefficients q[0..N_ORD]; o = order to which the series is known."""
    def __init__(s, q, o=None):
        s.o = N_ORD if o is None else o
        q = (list(q) + [0] * (N_ORD + 1))[:N_ORD + 1]
        s.q = [sp.expand(v) if k_ <= s.o else sp.S(0) for k_, v in enumerate(q)]

    def _c(s, o): return o if isinstance(o, S) else S([o])
    def val(s): return next((k_ for k_, v in enumerate(s.q) if k_ <= s.o and v != 0), N_ORD + 1)
    def __add__(s, o): o = s._c(o); return S([u + v for u, v in zip(s.q, o.q)], min(s.o, o.o))
    __radd__ = __add__
    def __neg__(s): return S([-v for v in s.q], s.o)
    def __sub__(s, o): return s + (-s._c(o))
    def __rsub__(s, o): return (-s) + o

    def __mul__(s, o):
        o = s._c(o); oo = min(N_ORD, s.o + o.val(), o.o + s.val())
        return S([sum(s.q[i] * o.q[k_ - i] for i in range(k_ + 1)) if k_ <= oo else 0 for k_ in range(N_ORD + 1)], oo)
    __rmul__ = __mul__

    def fn(s, f):
        w = sp.Symbol("w_"); f0 = f(w); f1 = sp.diff(f0, w); f2 = sp.diff(f1, w)
        F0, F1, F2 = [sp.powdenest(sp.simplify(F.subs(w, s.q[0])), force=True) for F in (f0, f1, f2)]
        return S([F0, F1 * s.q[1], F1 * s.q[2] + F2 * s.q[1] ** 2 / 2], s.o)

    def d(s, v): return S([sp.diff(u, v) for u in s.q], s.o)
    def trunc(s, o): return S(s.q, min(o, s.o))


ZS, ONE = S([0]), S([1])


def christoffel(g, gi, X, order=1):
    n_ = len(X)
    dg = [[[g[A][B].d(X[C]) for C in range(n_)] for B in range(n_)] for A in range(n_)]
    G = [[[ZS] * n_ for _ in range(n_)] for _ in range(n_)]
    for A in range(n_):
        for B in range(n_):
            for C in range(n_):
                acc = ZS
                for D in range(n_):
                    if gi[A][D].val() <= N_ORD:
                        acc = acc + gi[A][D] * (dg[D][B][C] + dg[D][C][B] - dg[B][C][D])
                G[A][B][C] = (acc * sp.Rational(1, 2)).trunc(order)
    return G


# =============================================================================================== PART A: FRW linearisation
P("\n==================== A. CFG938 LINEARISED ON FLAT FRW (own derivation) ====================")
t, x, y, z = sp.symbols("t x y z", real=True)
XF = (t, x, y, z)
c, K, m, mb, rL, gam = sp.symbols("c K m m_b rho_L gamma", positive=True)
H, Hd, Xs, Xd, sig, k = sp.symbols("H Hdot X Xdot sigma k")
af = sp.Function("a")(t); chib = sp.Function("chib")(t)
xi, xib, dchi, dlam = [sp.Function(n_)(t, x) for n_ in ("xi", "xib", "dchi", "dlam")]
PhiF, PsiF, BF, EF = [sp.Function(n_)(t, x) for n_ in ("Phi", "Psi", "B", "E")]


def freeze(e):
    e = e.subs(sp.Derivative(af, (t, 4)), 0).subs(sp.Derivative(af, (t, 3)), 0)
    e = e.subs(sp.Derivative(af, (t, 2)), af * (Hd + H ** 2)).subs(sp.Derivative(af, t), af * H)
    e = e.subs(sp.Derivative(chib, (t, 3)), 0).subs(sp.Derivative(chib, (t, 2)), Xd).subs(sp.Derivative(chib, t), Xs)
    return e.subs(af, 1)


def planewave(e, funcs, amps):
    rep = {}
    for d_ in e.atoms(sp.Derivative):
        if d_.expr in funcs:
            p_ = sum(cn for v, cn in d_.variable_count if v == t); q_ = sum(cn for v, cn in d_.variable_count if v == x)
            rep[d_] = sig ** p_ * (sp.I * k) ** q_ * amps[funcs.index(d_.expr)]
    return sp.expand(e.xreplace(rep).xreplace({f_: amps[i] for i, f_ in enumerate(funcs)}))


def EL_each(L, funcs):
    out = []
    for f_ in funcs:
        ee = euler_equations(L, [f_], [t, x])
        out.append(sp.expand(ee[0].lhs - ee[0].rhs) if ee else sp.S(0))
    return out


def label_medium(g, gi, xif):
    phi1 = S([x, -xif])
    J = [phi1.d(x), -phi1.d(t), ZS, ZS]                                 # J^mu ~ eps^{mu a b c} d_a phi1 d_b y d_c z
    Jl = [sum((g[A][B] * J[B] for B in range(4)), ZS) for A in range(4)]
    N2 = -sum((Jl[A] * J[A] for A in range(4)), ZS)
    inv = N2.fn(lambda w: 1 / sp.sqrt(w)); inv = S([v.subs(sp.sqrt(c ** 2), c) for v in inv.q])
    uu = [J[A] * inv for A in range(4)]; ud = [Jl[A] * inv for A in range(4)]
    B11 = sum((gi[A][B] * phi1.d(XF[A]) * phi1.d(XF[B]) for A in range(4) for B in range(4) if gi[A][B].val() <= N_ORD), ZS)
    n = (B11 * gi[2][2] * gi[3][3]).fn(lambda w: sp.sqrt(w)); n = S([sp.powdenest(v, force=True) for v in n.q])
    return uu, ud, n


def chi_sector(g, gi, Gam, uu, ud, sqrtg, mode):
    hup = [[gi[A][B] + uu[A] * uu[B] for B in range(4)] for A in range(4)]
    hmix = [[(ONE if A == B else ZS) + ud[A] * uu[B] for B in range(4)] for A in range(4)]
    hdn = [[g[A][B] + ud[A] * ud[B] for B in range(4)] for A in range(4)]
    chi = S([chib, dchi])
    dch = [chi.d(Xi) for Xi in XF]
    nab = [[chi.d(XF[A]).d(XF[B]) - sum((Gam[C][A][B] * dch[C] for C in range(4)), ZS) for B in range(4)] for A in range(4)]
    DD = [[sum((hmix[A][C] * nab[C][D] * hmix[B][D] for C in range(4) for D in range(4)), ZS) for B in range(4)] for A in range(4)]
    D2 = sum((hup[A][B] * nab[A][B] for A in range(4) for B in range(4)), ZS)
    theta = sum(((sqrtg * uu[A]).d(XF[A]) for A in range(4)), ZS) * sqrtg.fn(lambda w: 1 / w)
    udchi = sum((uu[A] * dch[A] for A in range(4)), ZS)
    D2c = {"asis": D2, "flip": D2 + 2 * theta * udchi, "remove": D2 + theta * udchi}[mode]
    tau = [[DD[A][B] - hdn[A][B] * D2 * sp.Rational(1, 3) for B in range(4)] for A in range(4)]
    tau0_zero = all(sp.expand(tau[A][B].q[0]) == 0 for A in range(4) for B in range(4))
    tau2 = S([0, 0, sum(tau[A][B].q[1] * tau[C][D].q[1] * gi[A][C].q[0] * gi[B][D].q[0] for A in range(4) for B in range(4)
                        for C in range(4) for D in range(4))])
    u2 = sum((hup[A][B] * dch[A] * dch[B] for A in range(4) for B in range(4)), ZS)
    return D2c, tau2, u2, tau0_zero


def frw_system(mode="asis", grav="qs", lam_medium=True):
    """grav: 'off' | 'qs' (frozen quasi-static Newtonian, Phi = Psi) | 'gr' (A1: full scalar sector, Psi, B, Phi, E, baryons, Lambda).
    mode: asis (CFG938) | flip (MU1) | remove (MU2: intrinsic slice Laplacian + explicit rho_bar).  lam_medium False: MU5."""
    g = [[ZS] * 4 for _ in range(4)]; gi = [[ZS] * 4 for _ in range(4)]
    if grav == "gr":
        g[0][0] = S([-c ** 2, -2 * c ** 2 * PsiF])
        g[0][1] = g[1][0] = S([0, c * af * sp.diff(BF, x)])
        g[1][1] = S([af ** 2, af ** 2 * (-2 * PhiF + 2 * sp.diff(EF, x, 2))])
        g[2][2] = g[3][3] = S([af ** 2, -2 * af ** 2 * PhiF])
        det2 = g[0][0] * g[1][1] - g[0][1] * g[0][1]; idet2 = det2.fn(lambda w: 1 / w)
        gi[0][0] = g[1][1] * idet2; gi[1][1] = g[0][0] * idet2; gi[0][1] = gi[1][0] = -g[0][1] * idet2
        gi[2][2] = g[2][2].fn(lambda w: 1 / w); gi[3][3] = g[3][3].fn(lambda w: 1 / w)
        sqrtg = (-det2 * g[2][2] * g[3][3]).fn(lambda w: sp.sqrt(w))
    else:
        Phi = PhiF if grav == "qs" else sp.S(0)
        Pn = S([0, Phi])
        g[0][0] = S([-c ** 2]) * (ONE + 2 * Pn * (1 / c ** 2))
        for i in (1, 2, 3):
            g[i][i] = S([af ** 2]) * (ONE - 2 * Pn * (1 / c ** 2))
        for i in range(4):
            gi[i][i] = g[i][i].fn(lambda w: 1 / w)
        sqrtg = (-(g[0][0] * g[1][1] * g[2][2] * g[3][3])).fn(lambda w: sp.sqrt(w))
    sqrtg = S([sp.powdenest(v, force=True).subs(sp.sqrt(c ** 2 * af ** 6), c * af ** 3) for v in sqrtg.q])
    Gam2 = christoffel(g, gi, XF, order=2 if grav == "gr" else 1)
    Gam = [[[Gam2[A][B][C].trunc(1) for C in range(4)] for B in range(4)] for A in range(4)]
    uu, ud, n = label_medium(g, gi, xi)
    D2c, tau2, u2, tau0_zero = chi_sector(g, gi, Gam, uu, ud, sqrtg, mode)
    lam = S([0, dlam])
    src = (S([K * m]) * n) if lam_medium else S([K * m / af ** 3])
    sub_bg = S([K * m / af ** 3]) if mode == "remove" else ZS
    Lm = sqrtg * (S([-m * c ** 2]) * n - u2 * (1 / (2 * K)) - tau2 * (3 * gam / (4 * K ** 2)) + lam * (D2c - src + sub_bg))
    if grav == "gr":
        _, _, nb = label_medium(g, gi, xib)
        Ric = [[ZS] * 4 for _ in range(4)]
        for B_ in range(4):
            for C_ in range(B_, 4):
                acc = ZS
                for A_ in range(4):
                    acc = acc + Gam2[A_][B_][C_].d(XF[A_]) - Gam2[A_][B_][A_].d(XF[C_])
                    for D_ in range(4):
                        acc = acc + Gam2[A_][A_][D_] * Gam2[D_][B_][C_] - Gam2[A_][C_][D_] * Gam2[D_][B_][A_]
                Ric[B_][C_] = Ric[C_][B_] = acc
        Rs = sum((gi[A_][B_] * Ric[A_][B_] for A_ in range(4) for B_ in range(4) if gi[A_][B_].val() <= N_ORD), ZS)
        Lg = sqrtg * Rs * (c ** 4 / (4 * K)) + sqrtg * (S([-mb * c ** 2]) * nb + S([-rL * c ** 2]))
        Ltot = Lm + Lg
        funcs = [dchi, dlam, xi, xib, PsiF, BF, PhiF, EF]
        L2 = sp.expand(Ltot.q[2])
    else:
        Ltot = Lm
        funcs = [dchi, dlam, xi] + ([PhiF] if grav == "qs" else [])
        L2 = sp.expand(Ltot.q[2] + (-c * af * sp.diff(PhiF, x) ** 2 / (2 * K) if grav == "qs" else 0))
    L1 = sp.expand(Ltot.q[1])
    EL = EL_each(L2, funcs)
    amps = sp.symbols("A_chi A_lam A_xi A_xib A_Psi A_B A_Phi A_E")[:len(funcs)] if grav == "gr" else \
        sp.symbols("A_chi A_lam A_xi A_Phi")[:len(funcs)]
    rows = [planewave(freeze(e), funcs, amps) for e in EL]
    M = sp.Matrix([[r.coeff(A_) for A_ in amps] for r in rows])
    # tadpoles: EL of the O(eps) Lagrangian with Friedmann and S1d
    Xbg = {"asis": -K * m * c ** 2 / (3 * H), "flip": K * m * c ** 2 / (3 * H), "remove": -K * m * c ** 2 / (3 * H)}[mode]
    bgsub = {rL: 3 * H ** 2 / (2 * K) - m - mb, mb: -Hd / K - m} if grav == "gr" else {}
    tad = [sp.simplify(freeze(e).subs(bgsub).subs(bgsub).subs(Xs, Xbg)) for e in EL_each(L1, funcs)]
    if grav == "gr":
        keep_c = [0, 1, 2, 3, 4, 6]                                        # Newtonian gauge: B = E = 0 after variation
        Mg = M[:, keep_c]
        rows6 = [0, 1, 2, 3, 4, 5]                                         # drop the Phi and E rows for the root polynomial
        det = sp.expand(Mg[rows6, :].det(method="berkowitz"))
    else:
        Mg = M; rows6 = list(range(len(funcs)))
        det = sp.expand(M.det(method="berkowitz"))
    sym = sp.simplify(L2.coeff(dlam).coeff(sp.Derivative(dchi, t)))
    return dict(M=M, Mg=Mg, rows6=rows6, det=det, funcs=funcs, amps=amps, L1tad=tad, D2bg=sp.simplify(D2c.q[0]),
                D2lin=sp.simplify(D2c.q[1]), tau0_zero=tau0_zero, u2_2=sp.simplify(u2.q[2]), sym=sym, grav=grav, mode=mode)


def bgvals(zz):
    E2 = Om0 * (1 + zz) ** 3 + OL0
    return dict(E=math.sqrt(E2), Oc=Oc0 * (1 + zz) ** 3 / E2, Om=Om0 * (1 + zz) ** 3 / E2, Ob=Ob * (1 + zz) ** 3 / E2,
                OL=OL0 / E2)


def subs_for(zz, sgnH, Lst, kphys, mode="asis"):
    """units: c = H(z) = K = 1 (K rho in H^2 units); kphys in 1/m, Lst in m.  Rational inputs for exact polynomial roots."""
    b = bgvals(zz); R = lambda v: sp.nsimplify(v, rational=True)
    Hz = H0_SI * b["E"]
    mval = sp.Rational(3, 2) * R(b["Oc"]); mbv = sp.Rational(3, 2) * R(b["Ob"])
    rLv = sp.Rational(3, 2) - mval - mbv                                   # Friedmann imposed exactly (rational arithmetic)
    Hv = sp.Integer(sgnH); Hdv = -(mval + mbv)                             # dH/dt = -K rho_m (both signs of H)
    sgnX = 1 if mode == "flip" else -1
    Xv = sgnX * mval / (3 * Hv); Xdv = -sgnX * mval * (1 + Hdv / (3 * Hv ** 2))
    return {c: 1, K: 1, m: mval, mb: mbv, rL: rLv, gam: R((Lst * Hz / C_SI) ** 2 / 2), H: Hv, Hd: Hdv, Xs: Xv, Xd: Xdv,
            k: R(kphys * C_SI / Hz)}, Hz


def mpq(v):
    v = sp.nsimplify(v) if not v.is_Rational and v.is_real else v
    re_, im_ = sp.re(v), sp.im(v)
    return mp.mpc(mp.mpf(re_.p) / re_.q, mp.mpf(im_.p) / im_.q)


def roots_at(det, sb):
    pol = sp.Poly(sp.expand(det.subs(sb)), sig)
    return mp.polyroots([mpq(cc) for cc in pol.all_coeffs()], maxsteps=800, extraprec=1500)


def equil_smin(A):
    A = mp.matrix(A)
    for _ in range(3):
        for i in range(A.rows):
            nr = mp.sqrt(sum(abs(A[i, j]) ** 2 for j in range(A.cols)))
            if nr > 0:
                for j in range(A.cols):
                    A[i, j] /= nr
        for j in range(A.cols):
            nc = mp.sqrt(sum(abs(A[i, j]) ** 2 for i in range(A.rows)))
            if nc > 0:
                for i in range(A.rows):
                    A[i, j] /= nc
    U, Sv, V = mp.svd_c(A)
    return Sv[Sv.rows - 1] / Sv[0]


def rank_test(sysd, sb, s0):
    Mf = sp.lambdify(sig, sysd["Mg"].subs(sb), "mpmath")
    return [float(equil_smin(Mf(s0 * f))) for f in (1, 1 + 1e-3, 1 - 1e-3)]


mp.mp.dps = 60
KGRID_LEN = [100 * MPC, 30 * MPC, 10 * MPC, 3 * MPC, 1 * MPC, 300 * KPC, 100 * KPC, 30 * KPC, 10 * KPC, 3 * KPC, 1 * KPC,
             300 * PC, 100 * PC, 24 * PC]
CASES = [(0, 1, "24pc"), (0, 1, "1kpc"), (10, 1, "24pc"), (10, 1, "1kpc"), (0, -1, "24pc"), (0, -1, "1kpc"), (10, -1, "24pc"),
         (10, -1, "1kpc")]


def hadamard_scan(sysd, zz, sgnH, Lname, label):
    rows = []
    for Lk in KGRID_LEN:
        sb, Hz = subs_for(zz, sgnH, LSTAR[Lname], 1.0 / Lk, sysd["mode"])
        rts = roots_at(sysd["det"], sb)
        ku = float(sb[k])
        rmax = max(rts, key=lambda r_: mp.re(r_)); mx = float(mp.re(rmax))
        rec = dict(L_over_kpc=Lk / KPC, k_units=ku, maxRe=mx, ratio_to_k2over3=mx / (ku ** 2 / 3), roots=[complex(r_) for r_ in rts])
        if sysd["grav"] == "gr" and (abs(Lk - 24 * PC) < 1 or abs(Lk - MPC) < 1):
            rec["rank_test_smin_at_root_and_pm1e-3"] = rank_test(sysd, sb, rmax)
            rec["rank_smin_over_(H/ck)^2_report_only"] = rec["rank_test_smin_at_root_and_pm1e-3"][0] * ku ** 2
        rows.append(rec)
    top = rows[-4:]
    slope = float(np.polyfit(np.log([r_["k_units"] for r_ in top]), np.log([max(r_["maxRe"], 1e-300) for r_ in top]), 1)[0])
    at1Mpc = [r_ for r_ in rows if abs(r_["L_over_kpc"] - 1000.0) < 1e-6][0]["maxRe"]
    at1kpc = [r_ for r_ in rows if abs(r_["L_over_kpc"] - 1.0) < 1e-9][0]["maxRe"]
    maxall = max(r_["maxRe"] for r_ in rows)
    if abs(slope - 2) <= 0.02 and at1Mpc >= 100:
        lab = "ILL-POSED"
    elif maxall <= 10:
        lab = "WELL-POSED"
    else:
        lab = "UNRESOLVED"
    rk = ""
    rank_ok = True
    if sysd["grav"] == "gr":
        rts_ = [r_.get("rank_test_smin_at_root_and_pm1e-3") for r_ in rows if "rank_test_smin_at_root_and_pm1e-3" in r_]
        rank_ok = all(q[0] <= 1e-6 and min(q[1:]) >= 1e-2 for q in rts_)
        dg_ = [r_["rank_smin_over_(H/ck)^2_report_only"] for r_ in rows if "rank_smin_over_(H/ck)^2_report_only" in r_]
        rk = f"; 8x6 rank test s_min at root / +-1e-3 (1 Mpc, 24 pc): " + "; ".join(f"{q[0]:.1e}/{min(q[1:]):.2f}" for q in rts_) + \
             f" -> {'PASS' if rank_ok else 'FAIL'} [report only: s_min/(H/ck)^2 = " + ", ".join(f"{q:.2f}" for q in dg_) + "]"
    P(f"  {label:34s} z={zz:<3} H{'+' if sgnH > 0 else '-'} L*={Lname:5s}: max Re sigma/|H| at c/k = 100 Mpc, 1 Mpc, 1 kpc, 24 pc = "
      f"{rows[0]['maxRe']:.3e}, {at1Mpc:.3e}, {at1kpc:.3e}, {rows[-1]['maxRe']:.3e}; slope {slope:.4f}; top ratio "
      f"{rows[-1]['ratio_to_k2over3']:.10f} -> {lab}{rk}")
    return dict(rows=rows, slope=slope, label=lab, top_ratio=rows[-1]["ratio_to_k2over3"], rank_ok=rank_ok)


def heat_labels(sysd):
    """sign of the d_t coefficient relative to the -k^2 coefficient in the chi (constraint) and lambda equations."""
    M, funcs = sysd["M"], sysd["funcs"]
    a_chi = sp.expand(M[funcs.index(dlam), 0]); a_lam = sp.expand(M[funcs.index(dchi), 1])
    out = {}
    for name, e in (("chi", a_chi), ("lambda", a_lam)):
        cs = e.coeff(sig, 1); ck2 = e.coeff(sig, 0).coeff(k, 2)
        if cs == 0:
            lab = "NO TIME DERIVATIVE (elliptic)"; root = "none"
        else:
            Dcoef = sp.simplify(ck2 / cs)                                   # forward heat iff D = ck2/cs > 0 at H = +1
            lab = "FORWARD-parabolic for H>0" if sp.simplify(Dcoef.subs(H, 1)) > 0 else "BACKWARD-parabolic for H>0"
            root = str(sp.simplify(-ck2 * k ** 2 / cs))
        out[name] = dict(coef_sigma=str(cs), coef_k2=str(ck2), root_sigma=root, label=lab)
    return out


def run_frw(mode, grav, lam_medium, tagname, cases=None):
    t1 = time.time()
    sysd = frw_system(mode, grav, lam_medium)
    P(f"\n  --- {tagname}: mode={mode}, gravity={grav}, lambda source={'K m n' if lam_medium else 'K rho_bar(t) fixed'} "
      f"(built in {time.time() - t1:.1f} s)")
    P(f"  background D^2 chibar = {sysd['D2bg']}   (S1d needs = K rho_bar); tau vanishes on FRW: {sysd['tau0_zero']}")
    P(f"  linear D^2 chi = {sysd['D2lin']}")
    P(f"  u^2 at O(eps^2) = {sysd['u2_2']}")
    P(f"  tadpoles (EL of the O(eps) Lagrangian, Friedmann + background chibar' used): {sysd['L1tad']}")
    P(f"  symplectic coefficient of dlam * d_t dchi in L2 (P1) = {sysd['sym']}")
    for i, f_ in enumerate(sysd["funcs"]):
        P(f"  EL[{str(f_.func)}] row {tuple(str(a_) for a_ in sysd['amps'])}: " + str([sp.factor(sysd['M'][i, j]) for j in range(len(sysd['amps']))]))
    labs = heat_labels(sysd)
    for nm, v in labs.items():
        P(f"  {nm:6s} equation: d_t coefficient {v['coef_sigma']}, k^2 coefficient {v['coef_k2']}; homogeneous root sigma = "
          f"{v['root_sigma']} -> {v['label']}")
    pol = sp.Poly(sysd["det"], sig)
    P(f"  dispersion polynomial degree in sigma = {pol.degree()}; leading coefficient = {sp.factor(pol.all_coeffs()[0])}")
    out = dict(labels=labs, degree=pol.degree(), lead=str(sp.factor(pol.all_coeffs()[0])), D2bg=str(sysd["D2bg"]),
               D2lin=str(sysd["D2lin"]), sym=str(sysd["sym"]), tadpoles=[str(q) for q in sysd["L1tad"]], scan={})
    for (zz, sg, Ln) in (cases or CASES):
        out["scan"][f"z{zz}|H{'+' if sg > 0 else '-'}|{Ln}"] = hadamard_scan(sysd, zz, sg, Ln, tagname)
        guard("scan")
    return sysd, out


def eigvec(sysd, sb, s0):
    """null vector at root s0, normalised to K dlam = 1 (K = 1 units); uses the root rows; residual on all rows of Mg."""
    Mf = sp.lambdify(sig, sysd["Mg"].subs(sb), "mpmath")
    A = mp.matrix(Mf(s0)); rows6 = sysd["rows6"]
    A6 = mp.matrix([[A[i, j] for j in range(A.cols)] for i in rows6])
    U, Sv, V = mp.svd_c(A6)
    v = [V[V.rows - 1, j].conjugate() for j in range(V.cols)]
    v = [q / v[1] for q in v]
    res = []
    for i in range(A.rows):                                                # relative residual; rows with no weight on v count 0
        den = sum(abs(A[i, j] * v[j]) for j in range(A.cols))
        res.append(abs(sum(A[i, j] * v[j] for j in range(A.cols))) / den if den != 0 else mp.mpf(0))
    return v, res


def p2_report(sysd, nm, cases):
    rec = {}
    names = [str(a_)[2:] for a_ in sysd["amps"]]
    if sysd["grav"] == "gr":
        names = ["chi", "lam", "xi", "xib", "Psi", "Phi"]
    for (Lk, sg) in cases:
        sb, Hz = subs_for(0, sg, LSTAR["24pc"], 1.0 / Lk, sysd["mode"])
        rts = roots_at(sysd["det"], sb); rg = max(rts, key=lambda r_: mp.re(r_))
        v, res = eigvec(sysd, sb, rg)
        kk_ = float(sb[k]); sgv = complex(rg)
        ixi = names.index("xi")
        xi_ = complex(v[ixi]); dc = abs(1j * kk_ * xi_)
        r = dict(c_over_k_kpc=Lk / KPC, sgnH=sg, sigma_over_k2_3=sgv.real / (kk_ ** 2 / 3), delta_c=dc,
                 delta_c_over_natural=dc / (kk_ ** 2 / abs(sgv) ** 2), medium_acc_over_force=abs(sgv ** 2 * xi_) / kk_,
                 A_chi=abs(complex(v[0])), max_row_residual=float(max(res)))
        for pn in ("Phi", "Psi"):
            if pn in names:
                r[f"{pn}_over_Kdlam"] = abs(complex(v[names.index(pn)]))
                r[f"{pn}_x_(ck/H)^2"] = abs(complex(v[names.index(pn)])) * kk_ ** 2
        key = f"{nm}|{Lk / KPC:g}kpc|H{'+' if sg > 0 else '-'}"
        rec[key] = r
        extra = "".join(f"; |{pn}|/|K dlam| = {r[pn + '_over_Kdlam']:.3e} (x (ck/H)^2 = {r[pn + '_x_(ck/H)^2']:.3f})"
                        for pn in ("Phi", "Psi") if pn + "_over_Kdlam" in r)
        P(f"   [{nm}] c/k = {Lk / KPC:g} kpc, H{'+' if sg > 0 else '-'}: sigma/(c^2k^2/3|H|) = {r['sigma_over_k2_3']:.10f}; "
          f"|delta_c|/(k^2/|sigma|^2) = {r['delta_c_over_natural']:.4f}; |sigma^2 xi|/|k K dlam| = {r['medium_acc_over_force']:.4f}; "
          f"|A_chi| = {r['A_chi']:.3e}{extra}; max row residual {r['max_row_residual']:.1e}")
    return rec


RES["A"] = {}
if not MUT:
    sysQ, outQ = run_frw("asis", "qs", True, "AS WRITTEN, quasi-static (frozen primary)")
    sys0, out0 = run_frw("asis", "off", True, "AS WRITTEN, gravity off (frozen secondary)")
    sysG, outG = run_frw("asis", "gr", True, "AS WRITTEN, full GR (A1)")
    RES["A"]["qs"] = outQ; RES["A"]["off"] = out0; RES["A"]["gr"] = outG
    tad_ok = all(sp.simplify(sp.sympify(q)) == 0 for o in (outQ, out0, outG) for q in o["tadpoles"])
    chk("A_tadpoles_vanish", tad_ok, "O(eps) Euler-Lagrange expressions vanish with Friedmann (GR) and S1d chibar' = -K rho c^2/3H")
    # Bianchi: which pairs of rows can be dropped without losing the fast root (A1.2)
    P("\n  A1 Bianchi test: drop two rows of the 8 x 6 Newtonian-gauge system; does the fast root survive?")
    sb, Hz = subs_for(0, 1, LSTAR["24pc"], 1.0 / KPC)
    Mn = sysG["Mg"].subs(sb); kk_ = float(sb[k]); rown = ["lam-eq(vary chi)", "constraint(vary lam)", "Euler medium", "Euler baryon",
                                                          "Hamiltonian(Psi)", "momentum(B)", "trace-ij(Phi)", "anisotropic(E)"]
    bianchi = {}
    for drop in itertools.combinations(range(8), 2):
        rr_ = [i for i in range(8) if i not in drop]
        d_ = sp.expand(Mn[rr_, :].det(method="berkowitz"))
        if d_ == 0:
            bianchi[f"{drop}"] = None; continue
        pol = sp.Poly(d_, sig); rts = mp.polyroots([mpq(cc) for cc in pol.all_coeffs()], maxsteps=800, extraprec=1500)
        mx = max(float(mp.re(r_)) for r_ in rts)
        bianchi[f"{rown[drop[0]]} + {rown[drop[1]]}"] = mx / (kk_ ** 2 / 3)
    for kq, v in bianchi.items():
        P(f"   drop {kq:55s}: max Re root / (c^2k^2/3H) = {v if v is None else f'{v:.8f}'}")
    RES["A"]["bianchi_drop_pairs"] = bianchi

    # ---------------- K-a1: singular H -> 0 limit with X = d_t chibar independent
    P("\n  K-a1 (H -> 0 with X = d_t chibar independent)")
    ka1 = {}
    s_ = sp.Symbol("s")
    for nm, sd in (("grav_off", sys0), ("quasi_static", sysQ)):
        pol = sp.Poly(sd["det"], sig); lead = sp.factor(pol.all_coeffs()[0])
        lead_H0 = sp.factor(lead.subs(H, 0))
        dsub = sp.expand(sd["det"].subs(sig, s_ * k ** 2)); pk = sp.Poly(dsub, k)
        lt = sp.factor(pk.coeff_monomial(k ** pk.degree()))
        fast = sorted([sp.simplify(r_) for r_ in sp.solve(lt, s_) if r_ != 0], key=str)
        d0 = sp.factor(sd["det"].subs({H: 0, Hd: 0, Xs: 0, Xd: 0}))
        dl_ = sp.Symbol("delta_c", positive=True)
        d0c = sp.expand(sp.numer(sp.together(d0.subs(c, 1 / dl_))))
        lowc = min(sp.Poly(d0c, dl_).monoms())[0]
        d0inf = sp.factor(sp.Poly(d0c, dl_).coeff_monomial(dl_ ** lowc))     # c -> infinity (CFG938 S5a is stated there)
        target = sig ** 2 + gam * m * k ** 2 + (K * m if nm == "grav_off" else 0)   # u0 = 0: tether +K rho; with gravity it cancels -K rho
        monic = sp.Poly(d0inf, sig).monic().as_expr()
        degm = sp.Poly(monic, sig).degree()
        rem = sp.simplify(sp.rem(sp.Poly(monic, sig), sp.Poly(target, sig)).as_expr()) if degm == 2 else f"degree {degm} != 2"
        fast_ok = set(fast) == {sp.simplify(-c ** 2 / (3 * H)), sp.simplify(c ** 2 / (3 * H))}
        P(f"   [{nm}] leading coeff {lead}; at H = 0 (X fixed): {lead_H0}")
        P(f"   [{nm}] fast roots sigma = s k^2 at leading order in k: s = {fast} (expected +-c^2/3H: {fast_ok})")
        P(f"   [{nm}] H = X = 0 determinant = {d0}; c -> inf: {d0inf}; remainder vs {target} (static WKB, u0 = 0): {rem}")
        ka1[nm] = dict(lead=str(lead), lead_H0=str(lead_H0), fast=[str(f_) for f_ in fast], fast_ok=fast_ok, det_H0X0=str(d0), rem=str(rem))
        chk(f"K_a1_{nm}", lead_H0 == 0 and fast_ok and rem == 0,
            f"degree drops at H=0 (X fixed): {lead_H0 == 0}; fast roots +-c^2k^2/3H: {fast_ok}; H=X=0 roots = static u0 = 0 result: {rem == 0}")
    RES["A"]["K_a1"] = ka1

    # ---------------- P2
    P("\n  P2: eigenvector of the fastest growing root (normalised K dlam = 1; z = 0, L* = 24 pc)")
    p2 = {}
    p2.update(p2_report(sys0, "grav_off", [(KPC, 1), (MPC, 1), (KPC, -1)]))
    p2.update(p2_report(sysQ, "quasi_static", [(KPC, 1), (MPC, 1)]))
    p2.update(p2_report(sysG, "full_GR", [(KPC, 1), (MPC, 1), (KPC, -1)]))
    RES["A"]["P2"] = p2
    force_in_medium = all(sp.simplify(sd["M"][sd["funcs"].index(xi), 1]) != 0 for sd in (sys0, sysQ, sysG))
    P(f"   medium Euler equation contains d_x(K dlam) (entry {sp.factor(sysG['M'][sysG['funcs'].index(xi), 1])}): {force_in_medium}")
    phys = {nm: all(v["delta_c_over_natural"] > 1e-10 for kq, v in p2.items() if kq.startswith(nm) and v["sgnH"] > 0)
            for nm in ("grav_off", "quasi_static", "full_GR")}
    P2LAB = {nm: ("PHYSICAL" if (ok and force_in_medium) else "MULTIPLIER-ONLY") for nm, ok in phys.items()}
    P(f"   P2 -> {P2LAB}")
    RES["A"]["P2_label"] = P2LAB

    # ---------------- P3
    P("\n  P3: lambda posed with final data -> anticipation tau_k = 3|H|/(c^2 k^2), k = 1/r (z = 0)")
    p3 = {}
    for r_ in (10 * KPC, 1 * MPC, 100 * MPC):
        tau_k = 3 * H0_SI * r_ ** 2 / C_SI ** 2
        p3[f"{r_ / KPC:g}kpc"] = dict(tau_yr=tau_k / 3.15576e7, tau_times_H=tau_k * H0_SI)
        P(f"   r = {r_ / KPC:>8g} kpc: tau_k = {tau_k / 3.15576e7:.3e} yr; tau_k H0 = {tau_k * H0_SI:.3e}; "
          f"growth e-fold time as an IVP = tau_k")
    RES["A"]["P3"] = p3
    guard("A-main")

    # ---------------- K-a2: static flat medium with background gradient u0 z (own derivation) -> CFG938 S5a
    P("\n  K-a2: static medium, uniform background gradient u0 z-hat, WKB (own derivation) vs CFG938 S5a")
    tt, x1, x3 = sp.symbols("tt x1 x3", real=True)
    XS = (tt, x1, sp.Symbol("x2"), x3)
    u0, a0s, th = sp.symbols("u_0 a_0 theta", positive=True)
    xi1 = sp.Function("xi1")(tt, x1, x3); xi3 = sp.Function("xi3")(tt, x1, x3)
    dch2 = sp.Function("dchi2")(tt, x1, x3); dl2 = sp.Function("dlam2")(tt, x1, x3); Ph2 = sp.Function("Phi2")(tt, x1, x3)
    Pn = S([0, Ph2])
    gS = [[ZS] * 4 for _ in range(4)]; giS = [[ZS] * 4 for _ in range(4)]
    gS[0][0] = S([-c ** 2]) * (ONE + 2 * Pn * (1 / c ** 2))
    for i in (1, 2, 3):
        gS[i][i] = ONE - 2 * Pn * (1 / c ** 2)
    for i in range(4):
        giS[i][i] = gS[i][i].fn(lambda w: 1 / w)
    sqS = (gS[0][0] * gS[1][1] * gS[2][2] * gS[3][3]).fn(lambda w: sp.sqrt(-w))
    sqS = S([sp.powdenest(v, force=True).subs(sp.sqrt(c ** 2), c) for v in sqS.q])
    GaS = christoffel(gS, giS, XS, order=1)
    ph = [S([x1, -xi1]), S([XS[2]]), S([x3, -xi3])]
    Jv = []
    for mu in range(4):
        acc = ZS
        for al in range(4):
            for be in range(4):
                for ga in range(4):
                    e4 = sp.LeviCivita(mu, al, be, ga)
                    if e4 != 0:
                        acc = acc + e4 * ph[0].d(XS[al]) * ph[1].d(XS[be]) * ph[2].d(XS[ga])
        Jv.append(acc)
    N2S = -sum((gS[A][A] * Jv[A] * Jv[A] for A in range(4)), ZS)
    invS = N2S.fn(lambda w: 1 / sp.sqrt(w)); invS = S([v.subs(sp.sqrt(c ** 2), c) for v in invS.q])
    uS = [Jv[A] * invS for A in range(4)]; udS = [gS[A][A] * uS[A] for A in range(4)]
    BIJ = [[sum((giS[i][i] * ph[I].d(XS[i]) * ph[Jn].d(XS[i]) for i in range(4)), ZS) for Jn in range(3)] for I in range(3)]
    detB = (BIJ[0][0] * (BIJ[1][1] * BIJ[2][2] - BIJ[1][2] * BIJ[2][1]) - BIJ[0][1] * (BIJ[1][0] * BIJ[2][2] - BIJ[1][2] * BIJ[2][0])
            + BIJ[0][2] * (BIJ[1][0] * BIJ[2][1] - BIJ[1][1] * BIJ[2][0]))
    nS = detB.fn(lambda w: sp.sqrt(w))
    hupS = [[(giS[A][B] if A == B else ZS) + uS[A] * uS[B] for B in range(4)] for A in range(4)]
    hmS = [[(ONE if A == B else ZS) + udS[A] * uS[B] for B in range(4)] for A in range(4)]
    hdS = [[(gS[A][B] if A == B else ZS) + udS[A] * udS[B] for B in range(4)] for A in range(4)]
    chiS = S([u0 * x3, dch2]); lamS = S([0, dl2])
    dcS = [chiS.d(Xi) for Xi in XS]
    nbS = [[chiS.d(XS[A]).d(XS[B]) - sum((GaS[C][A][B] * dcS[C] for C in range(4)), ZS) for B in range(4)] for A in range(4)]
    DDS = [[sum((hmS[A][C] * nbS[C][D] * hmS[B][D] for C in range(4) for D in range(4)), ZS) for B in range(4)] for A in range(4)]
    D2S = sum((hupS[A][B] * nbS[A][B] for A in range(4) for B in range(4)), ZS)
    tauS = [[DDS[A][B] - hdS[A][B] * D2S * sp.Rational(1, 3) for B in range(4)] for A in range(4)]
    tau2S = sum(tauS[A][B].q[1] ** 2 * giS[A][A].q[0] * giS[B][B].q[0] for A in range(4) for B in range(4))
    u2S = sum((hupS[A][B] * dcS[A] * dcS[B] for A in range(4) for B in range(4)), ZS)
    Wfull = lambda w: (-a0s * sp.sqrt(w) - a0s ** 2 * sp.log(1 - sp.sqrt(w) / a0s)) / K   # W_full(u), u = sqrt(u^2)
    WS = u2S.fn(Wfull)
    rho0 = sp.Symbol("rho_0", positive=True)
    LcovS = sqS * (S([-rho0 * c ** 2]) * nS - WS - S([0, 0, tau2S]) * (3 * gam / (4 * K ** 2)) + lamS * (D2S - S([K * rho0]) * nS))
    L2S = sp.expand(LcovS.q[2] - (sp.diff(Ph2, x1) ** 2 + sp.diff(Ph2, x3) ** 2) / (2 * K) * c)
    fS = [dch2, dl2, xi1, xi3, Ph2]
    ELS = [sp.expand(e.lhs - e.rhs) for e in euler_equations(L2S, fS, [tt, x1, x3])]
    ampS = sp.symbols("B_chi B_lam B_1 B_3 B_Phi")
    om = sp.Symbol("omega")
    k1, k3 = k * sp.sin(th), k * sp.cos(th)

    def pwS(e):
        rep = {}
        for d_ in e.atoms(sp.Derivative):
            if d_.expr in fS:
                pt = sum(cn for v, cn in d_.variable_count if v == tt); p1 = sum(cn for v, cn in d_.variable_count if v == x1)
                p3_ = sum(cn for v, cn in d_.variable_count if v == x3)
                rep[d_] = (-sp.I * om) ** pt * (sp.I * k1) ** p1 * (sp.I * k3) ** p3_ * ampS[fS.index(d_.expr)]
        return sp.expand(e.xreplace(rep).xreplace({f_: ampS[i] for i, f_ in enumerate(fS)}))
    MS = sp.Matrix([[pwS(e).coeff(A_) for A_ in ampS] for e in ELS])
    detS = sp.factor(MS.det(method="berkowitz"))
    Dfull = sp.Symbol("u") / (1 - sp.Symbol("u") / a0s)
    uu_ = sp.Symbol("u")
    Rf = Dfull - uu_
    Rp = sp.diff(Rf, uu_)
    w2_938 = gam * rho0 * k ** 2 + K * rho0 * (Rp.subs(uu_, u0) * sp.cos(th) ** 2 + (Rf / uu_).subs(uu_, u0) * sp.sin(th) ** 2)
    # c -> infinity: substitute c = 1/delta and take the leading behaviour
    dl = sp.Symbol("delta", positive=True)
    detc = sp.expand(sp.numer(sp.together(detS.subs(c, 1 / dl))))
    lowest = min(sp.Poly(detc, dl).monoms())[0]
    detinf = sp.factor(sp.Poly(detc, dl).coeff_monomial(dl ** lowest))
    sols = [sp.simplify(s_) for s_ in sp.solve(detinf, om ** 2) if sp.simplify(s_) != 0] if detinf.has(om) else []
    if not sols:
        w2s = sp.Symbol("w2"); sols = [sp.simplify(s_) for s_ in sp.solve(detinf.subs(om, sp.sqrt(w2s)), w2s) if sp.simplify(s_) != 0]
    diff938 = [sp.simplify(s_ - w2_938) for s_ in sols]
    P(f"   c -> inf determinant factor: {detinf}")
    P(f"   nonzero omega^2 roots: {sols}")
    P(f"   CFG938 S5a: omega^2 = {w2_938}")
    ka2 = any(d_ == 0 for d_ in diff938)
    # inertia: coefficient of (d_t xi3)^2 at O(1/c^2) beyond rho0/2
    kin3 = sp.expand(L2S).coeff(sp.Derivative(xi3, tt) ** 2)
    inert_938 = rho0 / 2 * c - (Dfull.subs(uu_, u0) * u0 / (K * c ** 2)) / 2 * c       # times c: sqrt(-g) of t-coordinates
    kdiff = sp.simplify(kin3 - inert_938)
    ka2_in = sp.limit(kdiff * c, c, sp.oo) == 0
    P(f"   kinetic coefficient of (d_t xi_z)^2 (sqrt(-g) = c): {sp.simplify(kin3)}; CFG938 rho0 - D(u0)u0/(K c^2) form: "
      f"{sp.simplify(inert_938)}; difference x c -> {sp.limit(kdiff * c, c, sp.oo)} as c -> inf")
    chk("K_a2_static_dispersion_equals_CFG938_S5a", ka2 and ka2_in,
        f"omega^2 - CFG938 = {diff938}; inertia matches rho0 - D(u0)u0/(K c^2): {ka2_in}")
    RES["A"]["K_a2"] = dict(detinf=str(detinf), roots=[str(s_) for s_ in sols], diff=[str(d_) for d_ in diff938], inertia_ok=ka2_in)
    guard("K_a2")

    # ---------------- K-a3 slip (W-only), CFG847's five point-mass systems
    P("\n  K-a3: slip s = 4 pi G r |p_r| / (c^2 g), p_r = -W_full(u) on the law (W-only rows)")
    REF938 = {"canonical": [1.39e-09, 6.77e-08, 1.40e-07, 5.57e-07, 5.08e-06], "alt": [1.57e-09, 8.00e-08, 1.55e-07, 6.18e-07, 5.79e-06]}
    SYS = [("dwarf", 1e7, 0.3), ("MW disc", 6e10, 10.0), ("MW outer", 6e10, 100.0), ("group", 1e12, 300.0), ("cluster", 1.5e14, 1000.0)]
    MS847, KPC847 = 1.989e30, 3.0857e19                                  # CFG847's constants for its systems (as CFG938)
    ka3 = {}; ok3 = True; worst = 0
    for f_ in FOOTS:
        a0 = A0[f_]
        for (nm, Mb, rk_), ref in zip(SYS, REF938[f_]):
            r_ = rk_ * KPC847; gN = G_SI * Mb * MS847 / r_ ** 2
            g_ = 0.5 * (gN + math.sqrt(gN ** 2 + 4 * gN * a0)); u_ = g_ - gN
            W_ = (-a0 * u_ - a0 ** 2 * math.log(1 - u_ / a0)) / K_SI
            s_ = 4 * math.pi * G_SI * r_ * W_ / (C_SI ** 2 * g_)
            worst = max(worst, s_); ok3 &= abs(s_ / ref - 1) < 0.02
            ka3[f"{f_}|{nm}"] = dict(s=s_, ref938=ref, ratio=s_ / ref, vc_kms=math.sqrt(g_ * r_) / 1e3)
            P(f"   {f_:9s} {nm:9s} v_c {math.sqrt(g_ * r_) / 1e3:7.1f} km/s  s = {s_:.3e}  (CFG938 {ref:.2e}; ratio {s_ / ref:.4f})")
    chk("K_a3_slip_reproduced", ok3 and abs(worst / 5.79e-6 - 1) < 0.02, f"worst s = {worst:.3e} (CFG938 5.79e-6); all rows within 2%: {ok3}")
    RES["A"]["K_a3"] = ka3

    # ---------------- K-a4 NGC 3198 law from own static Euler-Lagrange; theta = 0 on static backgrounds
    P("\n  K-a4: NGC 3198 static law (own EL of E[M_c]) and theta = 0 on a static background")
    rr, Mb_, Mc_ = sp.symbols("r M_b M_c", positive=True)
    Gs, a0s2 = sp.symbols("G a0", positive=True)
    uM = Gs * Mc_ / rr ** 2
    Kk = 4 * sp.pi * Gs
    Wf = (-a0s2 * uM - a0s2 ** 2 * sp.log(1 - uM / a0s2)) / Kk
    Edens = -Gs * (Mb_ + Mc_) ** 2 / (2 * rr ** 2) + 4 * sp.pi * rr ** 2 * Wf     # gamma -> 0 (law limit)
    ELr = sp.simplify(sp.diff(Edens, Mc_))
    P(f"   dE/dM_c = {ELr}  (= 0 -> K W'(u) = g)")
    dat = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat"), comments="#")
    R = dat[:, 0] * KPC; Vg, Vd, Vb = dat[:, 3] * 1e3, dat[:, 4] * 1e3, dat[:, 5] * 1e3
    gNb = (Vg * np.abs(Vg) + 0.61 * Vd * np.abs(Vd) + 0.61 * Vb * np.abs(Vb)) / R
    ELf = sp.lambdify((Mc_, Mb_, rr, Gs, a0s2), ELr, "mpmath")
    ka4 = {}
    for f_ in FOOTS:
        a0 = A0[f_]; dev = 0
        for gn, r_ in zip(gNb, R):
            Mb_v = gn * r_ ** 2 / G_SI
            glaw = 0.5 * (gn + math.sqrt(gn ** 2 + 4 * gn * a0)); Mc_law = (glaw - gn) * r_ ** 2 / G_SI
            McS = mp.findroot(lambda q: ELf(q, Mb_v, r_, G_SI, a0), Mc_law * (1 + 1e-3))
            g_el = G_SI * (Mb_v + float(McS)) / r_ ** 2
            dev = max(dev, abs(g_el / glaw - 1))
        ka4[f_] = dev
        P(f"   {f_:9s}: max |g_EL/g_law - 1| over {len(R)} radii = {dev:.2e}")
    f00, hsp = sp.Function("f00")(x1, x3), sp.Function("hsp")(x1, x3)
    sqst = c * sp.sqrt(f00) * hsp ** sp.Rational(3, 2)                     # static metric -c^2 f dt^2 + h dx^2
    u_static = [1 / (c * sp.sqrt(f00)), 0, 0, 0]                         # medium at rest
    theta_static = sp.simplify(sum(sp.diff(sqst * u_static[A], XS[A]) for A in range(4)) / sqst)
    P(f"   divergence of a static medium 4-velocity (u^mu ~ d_t, metric static) = {theta_static} -> the -theta u.dchi term is absent")
    chk("K_a4_NGC3198_law_unaffected", all(v < 1e-6 for v in ka4.values()) and theta_static == 0,
        f"max dev canonical {ka4['canonical']:.1e}, alt {ka4['alt']:.1e}; theta = 0 on static backgrounds (structural)")
    RES["A"]["K_a4"] = ka4

    # ---------------- (a) class: frozen rule (quasi-static primary) and A1 (full-GR primary)
    def classify(prim, sec, p2lab, kchecks, rank_ok=True):
        scans = list(prim["scan"].values()) + list(sec["scan"].values())
        all_ill = all(s_["label"] == "ILL-POSED" for s_ in scans)
        ratio_ok = all(abs(s_["top_ratio"] - 1) < 0.01 for s_ in scans)
        agree = all(prim["scan"][q]["label"] == sec["scan"][q]["label"] for q in prim["scan"])
        Kall = all(RES["checks"][q]["pass_"] for q in kchecks)
        if not agree or not Kall or not rank_ok:
            cl = "UNDERDETERMINED"
        elif all_ill and ratio_ok:
            cl = "CONFIRMED" if p2lab == "PHYSICAL" else "CONFIRMED BUT NOT PHYSICAL"
        elif all(s_["label"] == "WELL-POSED" for s_ in scans):
            cl = "NOT CONFIRMED"
        else:
            cl = "UNDERDETERMINED"
        return cl, dict(all_ill=all_ill, ratio_ok=ratio_ok, agree=agree, Kall=Kall, rank_ok=rank_ok,
                        labels={q: (prim["scan"][q]["label"], sec["scan"][q]["label"]) for q in prim["scan"]},
                        ratios={q: (prim["scan"][q]["top_ratio"], sec["scan"][q]["top_ratio"]) for q in prim["scan"]})
    kfrozen = ["K_a1_grav_off", "K_a1_quasi_static", "K_a2_static_dispersion_equals_CFG938_S5a", "K_a3_slip_reproduced",
               "K_a4_NGC3198_law_unaffected"]
    kA1 = ["K_a1_grav_off", "K_a2_static_dispersion_equals_CFG938_S5a", "K_a3_slip_reproduced", "K_a4_NGC3198_law_unaffected",
           "A_tadpoles_vanish"]
    CL_F, dF = classify(outQ, out0, P2LAB["quasi_static"], kfrozen)
    rank_ok = all(s_["rank_ok"] for s_ in outG["scan"].values())
    CL_A, dA = classify(outG, out0, P2LAB["full_GR"], kA1, rank_ok)
    P(f"\n  (a) FROZEN-RULE class (quasi-static primary): {CL_F}")
    P(f"      all ILL-POSED {dF['all_ill']}; top ratios within 1% {dF['ratio_ok']}; primary/secondary labels agree {dF['agree']}; "
      f"K tests {dF['Kall']}")
    for q, v in dF["labels"].items():
        P(f"      {q:18s} labels (qs, off) = {v}; top ratios = ({dF['ratios'][q][0]:.6f}, {dF['ratios'][q][1]:.6f})")
    P(f"  (a) A1 class (full-GR primary, post hoc): {CL_A}")
    P(f"      all ILL-POSED {dA['all_ill']}; top ratios within 1% {dA['ratio_ok']}; GR/off labels agree {dA['agree']}; "
      f"K tests {dA['Kall']}; 8x6 rank tests {dA['rank_ok']}")
    for q, v in dA["labels"].items():
        P(f"      {q:18s} labels (GR, off) = {v}; top ratios = ({dA['ratios'][q][0]:.10f}, {dA['ratios'][q][1]:.10f})")
    RES["A"]["class_frozen"] = CL_F; RES["A"]["class_A1"] = CL_A
    RES["A"]["class_detail"] = dict(frozen=dF, A1=dA)
else:
    P("\n  MUTATE (A): MU1 flip, MU2 remove (gravity off and full GR), MU5 multiplier-only control (gravity off)")
    mcases = [(0, 1, "24pc"), (0, -1, "24pc"), (10, 1, "1kpc")]
    res_mu = {}
    bite1 = True; bite2 = True
    for grav in ("off", "gr"):
        s1, o1 = run_frw("flip", grav, True, f"MU1 flip ({grav})", cases=mcases)
        s2, o2 = run_frw("remove", grav, True, f"MU2 intrinsic Laplacian ({grav})", cases=mcases)
        res_mu[f"MU1_{grav}"] = o1; res_mu[f"MU2_{grav}"] = o2
        lab1 = o1["labels"]
        bite1 &= ("BACKWARD" in lab1["chi"]["label"] and "FORWARD" in lab1["lambda"]["label"] and
                  all(v["label"] == "ILL-POSED" for v in o1["scan"].values()))
        S1d_fail = sp.simplify(sp.sympify(o2["D2bg"])) == 0
        bite2 &= all(v["label"] == "WELL-POSED" for v in o2["scan"].values()) and S1d_fail
        P(f"   MU1[{grav}]: chi {lab1['chi']['label']}; lambda {lab1['lambda']['label']}; scans {[v['label'] for v in o1['scan'].values()]}")
        P(f"   MU2[{grav}]: background D^2 chibar = {o2['D2bg']} (S1d fails: {S1d_fail}); scans {[v['label'] for v in o2['scan'].values()]}")
    chk("MU1_flip_swaps_forward_backward_still_illposed", bite1, "chi becomes backward and lambda forward for H > 0; Hadamard still fires")
    chk("MU2_intrinsic_laplacian_wellposed_but_S1d_fails", bite2, "no unbounded root; background needs explicit rho_bar subtraction")
    s5, o5 = run_frw("asis", "off", False, "MU5 gravity off + lambda decoupled from the medium", cases=mcases)
    res_mu["MU5"] = o5
    p5 = p2_report(s5, "MU5", [(KPC, 1)])
    v5 = list(p5.values())[0]
    bite5 = v5["delta_c_over_natural"] < 1e-10 and v5["A_chi"] < 1e-10
    chk("MU5_multiplier_only_control_reads_MULTIPLIER-ONLY", bite5,
        f"growing root sigma/(c^2k^2/3H) = {v5['sigma_over_k2_3']:.6f}; |delta_c|/natural = {v5['delta_c_over_natural']:.2e}; |A_chi| = {v5['A_chi']:.1e}")
    RES["A"]["MUTATE"] = res_mu; RES["A"]["MU5_p2"] = p5
guard("A")

# =============================================================================================== PART B: tensor speed
P("\n==================== B. TENSOR SPEED FROM THE tau-tau TERM ====================")
x0, X1, X2, X3 = sp.symbols("x0 x1 x2 x3", real=True)
XT = (x0, X1, X2, X3)
eps = sp.Symbol("epsilon")
Ap, Ax, kk, ww, thk, V0, U0, PH = sp.symbols("A_p A_x k omega theta_k V_0 u_0 psi", real=True)
nvec = (sp.sin(thk), 0, sp.cos(thk)); e1 = (sp.cos(thk), 0, -sp.sin(thk)); e2 = (0, 1, 0)
phase = kk * (sp.sin(thk) * X1 + sp.cos(thk) * X3) - ww * x0
hij = sp.Matrix(3, 3, lambda i, j: (Ap * (e1[i] * e1[j] - e2[i] * e2[j]) + Ax * (e1[i] * e2[j] + e2[i] * e1[j])) * sp.cos(phase))


def avg_phase(expr, thval=None):
    """average over one period of the wave phase: eliminate x0 in favour of the phase PH, then integrate PH over 2 pi"""
    thv = thk if thval is None else thval
    e = sp.expand(expr).subs(x0, (kk * (sp.sin(thv) * X1 + sp.cos(thv) * X3) - PH) / ww)
    e = e.replace(lambda q: isinstance(q, (sp.sin, sp.cos)), lambda q: q.func(sp.expand(q.args[0])))
    e = sp.expand(e)
    assert not e.has(X1) and not e.has(X3), "phase elimination failed"
    return sp.simplify(sp.integrate(e, (PH, 0, 2 * sp.pi)) / (2 * sp.pi))


def tensor_tau2(Vt, Vz, christ=True, thval=None):
    """<tau_mn tau^mn> at O(eps^2) for the TT wave, medium at rest, chi = Vt x0 + Vz x3 (constant gradient)."""
    gT = sp.zeros(4, 4); gT[0, 0] = -1
    for i in range(3):
        for j in range(3):
            gT[i + 1, j + 1] = (1 if i == j else 0) + eps * hij[i, j]
    if thval is not None:
        gT = gT.subs(thk, thval)
    # Christoffels to O(eps): Gamma^C_AB = (1/2) eta^CD (d_B g_DA + d_A g_DB - d_D g_AB)
    Vlow = [Vt, 0, 0, Vz]
    nab_ = sp.zeros(4, 4)
    if christ:
        for A in range(4):
            for B in range(4):
                acc = 0
                for C in range(4):
                    GCAB = sum(sp.diag(-1, 1, 1, 1)[C, D] * (sp.diff(gT[D, A], XT[B]) + sp.diff(gT[D, B], XT[A]) - sp.diff(gT[A, B], XT[D]))
                               for D in range(4)) / 2
                    acc += GCAB * Vlow[C]
                nab_[A, B] = -acc                                            # d d chi = 0 for linear chi
    # medium at rest: u^mu = (1,0,0,0), h_a^b = delta + u_a u^b -> spatial projector; D_i D_j chi = nabla_i nabla_j chi
    DDt = sp.zeros(4, 4)
    for i in range(1, 4):
        for j in range(1, 4):
            DDt[i, j] = nab_[i, j]
    D2t = sp.expand(sum(DDt[i, i] for i in range(1, 4)))                   # O(eps): delta^ij DD_ij (TT -> 0)
    tau_ = sp.zeros(4, 4)
    for i in range(1, 4):
        for j in range(1, 4):
            tau_[i, j] = sp.expand(sp.diff(DDt[i, j] - gT[i, j] * D2t / 3, eps).subs(eps, 0))
    t2 = sum(tau_[i, j] ** 2 for i in range(1, 4) for j in range(1, 4))
    return avg_phase(t2), sp.simplify(sp.diff(D2t, eps).subs(eps, 0))


# EH quadratic action of the same wave, averaged over a period (computed for theta_k = 0; EH is rotation invariant -- checked at pi/2)
def eh_avg(thval):
    hh = hij.subs(thk, thval)
    gE = sp.zeros(4, 4); gE[0, 0] = -1
    for i in range(3):
        for j in range(3):
            gE[i + 1, j + 1] = (1 if i == j else 0) + eps * hh[i, j]
    eta = sp.diag(-1, 1, 1, 1)
    h4 = (gE - eta) / eps
    giE = eta - eps * eta * h4 * eta + eps ** 2 * eta * h4 * eta * h4 * eta
    Gm = [[[sp.expand(sum(giE[A, D] * (sp.diff(gE[D, B], XT[C]) + sp.diff(gE[D, C], XT[B]) - sp.diff(gE[B, C], XT[D])) for D in range(4)) / 2)
            for C in range(4)] for B in range(4)] for A in range(4)]
    Ric = sp.zeros(4, 4)
    for B in range(4):
        for C in range(4):
            Ric[B, C] = sum(sp.diff(Gm[A][B][C], XT[A]) for A in range(4)) - sum(sp.diff(Gm[A][B][A], XT[C]) for A in range(4)) \
                + sum(Gm[A][A][D] * Gm[D][B][C] for A in range(4) for D in range(4)) - sum(Gm[A][C][D] * Gm[D][B][A] for A in range(4) for D in range(4))
    Rs = sum(giE[B, C] * Ric[B, C] for B in range(4) for C in range(4))
    detg = gE.det()
    sq = sp.sqrt(-detg)
    L = sq * Rs
    L2 = sp.diff(L, eps, 2).subs(eps, 0) / 2
    return avg_phase(L2, thval)


t1 = time.time()
EH0 = eh_avg(0); EH90 = eh_avg(sp.pi / 2)
P(f"  <sqrt(-g) R> at O(eps^2), theta_k = 0: {sp.factor(EH0)};  theta_k = pi/2: {sp.factor(EH90)}  ({time.time() - t1:.1f} s)")
chk("K_b0_EH_normalisation_isotropic", sp.simplify(EH0 - EH90) == 0 and sp.simplify(EH0.subs(ww, kk)) == 0,
    "EH averaged Lagrangian vanishes on omega = k (c = 1) and is rotation invariant")
Lst = sp.Symbol("L", positive=True)
gamS = K * Lst ** 2 / 2
christ_on = not MUT
B = {}; BX = {}
for nm, (Vt, Vz) in {"spatial": (0, U0), "timelike": (V0, 0), "both": (V0, U0)}.items():
    tau2avg, D2lin_t = tensor_tau2(Vt, Vz, christ=True)
    Ltot = EH0 / (4 * K) - 3 * gamS / (4 * K ** 2) * tau2avg              # (c^4/16 pi G) = 1/(4K) at c = 1
    # Ltot = A (omega^2 - k^2) - L*^2 Bq(omega, k): first-order shift omega^2 = k^2 (1 + delta), delta = L*^2 Bq(k, k)/(A k^2)
    W2s = sp.Symbol("W2")
    Acoef = sp.simplify(sp.diff(Ltot.subs(Lst, 0).subs(ww, sp.sqrt(W2s)), W2s))
    Bq = sp.simplify(-sp.diff(Ltot, Lst) / (2 * Lst))
    lin = sp.simplify(Lst ** 2 * Bq.subs(ww, kk) / (Acoef * kk ** 2))
    lin = sp.simplify(sp.expand(lin).subs(sp.cos(thk) ** 2, 1 - sp.sin(thk) ** 2))
    lin = sp.factor(sp.simplify(sp.expand(sp.expand_trig(lin)).subs(sp.cos(thk) ** 2, 1 - sp.sin(thk) ** 2)))
    B[nm] = dict(tau2=str(sp.factor(tau2avg)), dcT2=str(sp.factor(lin)), D2lin=str(D2lin_t))
    BX[nm] = lin
    P(f"  [{nm:8s}] <tau^2> = {sp.factor(tau2avg)};  delta(c_T^2/c^2) to O(L*^2) = {sp.factor(lin)};  O(eps) trace D^2 = {D2lin_t}")
RES["B_symbolic"] = B
C_sp = sp.simplify(BX["spatial"] / (Lst ** 2 * U0 ** 2))
C_tl = sp.simplify(BX["timelike"] / (Lst ** 2 * V0 ** 2))
P(f"  coefficient C (spatial) = {C_sp};  C (timelike) = {C_tl}")
chk("b2_coefficient_1p5_all_angles_and_polarisations", sp.simplify(C_sp - sp.Rational(3, 2)) == 0,
    f"delta(c_T^2/c^2) = {C_sp} L*^2 u0^2/c^4 independent of theta_k, A_p, A_x -> c_T/c - 1 = 0.75 L*^2 u0^2/c^4")
RES["B_coeffs"] = dict(C_spatial=str(C_sp), C_timelike=str(C_tl), both=B["both"]["dcT2"])

# exact FRW check of tau_ij at O(h) with chibar(x0)
aa = sp.Function("a")(x0); chb = sp.Function("chb")(x0); hp = sp.Function("hp")(x0, X3)
gF = sp.diag(-1, aa ** 2 * (1 + eps * hp), aa ** 2 * (1 - eps * hp), aa ** 2)
giF = sp.diag(-1, 1 / (aa ** 2 * (1 + eps * hp)), 1 / (aa ** 2 * (1 - eps * hp)), 1 / aa ** 2)
GF = [[[sum(giF[A, D] * (sp.diff(gF[D, Bq], XT[Cq]) + sp.diff(gF[D, Cq], XT[Bq]) - sp.diff(gF[Bq, Cq], XT[D])) for D in range(4)) / 2
        for Cq in range(4)] for Bq in range(4)] for A in range(4)]
nabF = sp.Matrix(4, 4, lambda A, Bq: sp.diff(chb, XT[A], XT[Bq]) - sum(GF[Cq][A][Bq] * sp.diff(chb, XT[Cq]) for Cq in range(4)))
D2F = sum(giF[i, i] * nabF[i, i] for i in range(1, 4))
tauF11 = sp.simplify(sp.diff(nabF[1, 1] - gF[1, 1] * D2F / 3, eps).subs(eps, 0))
P(f"  exact FRW: tau_11 at O(h) = {tauF11}   (expected -(a^2/2) d_0 h d_0 chibar: the slices' extrinsic curvature x the clock)")
frw_ok = sp.simplify(tauF11 + aa ** 2 / 2 * sp.diff(hp, x0) * sp.diff(chb, x0)) == 0
chk("b_FRW_tau_has_clock_term", frw_ok, "tau_ij = -(a^2/2) h'_ij chibar' on FRW: the TT wave sees the cosmic clock through Gamma^0_ij")

# W, lambda-bar, n: only k-independent (mass-like) terms at O(h^2)
u2T = sum(((sp.eye(3) - eps * hij + eps ** 2 * hij * hij)[i, j]) * [0, 0, U0][i] * [0, 0, U0][j] for i in range(3) for j in range(3))
u2T2 = avg_phase(sp.diff(u2T, eps, 2).subs(eps, 0) / 2); u2T1 = avg_phase(sp.diff(u2T, eps).subs(eps, 0))
P(f"  W sector: <u^2> at O(h) = {u2T1}, O(h^2) = {sp.factor(u2T2)} (no k, omega: a graviton-mass-type term ~ u0^2/c^4)")
mg = (A0["canonical"] / C_SI ** 2)
P(f"    size: m_g ~ u/c^2 <= a0/c^2 = {mg:.2e} 1/m vs LIGO k ~ 2 pi x 100 Hz / c = {2 * math.pi * 100 / C_SI:.2e} 1/m -> negligible")
RES["B_Wterm"] = dict(u2_h1=str(u2T1), u2_h2=str(u2T2))

# numbers
P("\n  (b) numbers: c_T/c - 1 = 0.75 L*^2 V_eff^2 / c^4")
num_b = {}
for f_ in FOOTS:
    for Ln, Lv in LSTAR.items():
        num_b[f"wall|{f_}|{Ln}"] = 0.75 * (Lv * A0[f_] / C_SI ** 2) ** 2
        P(f"   local at the wall (u = a0) {f_:9s} L* = {Ln:5s}: {num_b[f'wall|{f_}|{Ln}']:.3e}")
zs, Ez = 0.0098, (lambda zz: math.sqrt(Om0 * (1 + zz) ** 3 + OL0))
ubar = lambda zz: C_SI * (Oc0 * (1 + zz) ** 3 / Ez(zz) ** 2) * H0_SI * Ez(zz) / 2
Dc = quad(lambda zz: C_SI / (H0_SI * Ez(zz)), 0, zs)[0]
u2avg = quad(lambda zz: ubar(zz) ** 2 * C_SI / (H0_SI * Ez(zz)), 0, zs)[0] / Dc
if MUT:
    u2avg_used = 0.0
    P("   MU4: V0 = 0 (no clock)")
else:
    u2avg_used = u2avg
P(f"   cosmic clock |d_0 chibar| = c Omega_c H / 2 = {ubar(0):.4e} m/s^2 (z = 0) = {ubar(0) / A0['canonical']:.3f} a0 (can) / "
  f"{ubar(0) / A0['alt']:.3f} a0 (alt); path to z = {zs}: D_c = {Dc / MPC:.1f} Mpc, <ubar^2>^(1/2) = {math.sqrt(u2avg):.4e}")
# galaxies (spatial part), point masses, r from 2 kpc to D/2 at each end; cross term with V0 (sign from 'both')
both = BX["both"]
P(f"   general constant gradient: delta(c_T^2/c^2) = {sp.factor(both)}")


def gal_int(Mb, a0, power):
    def u_of(r_):
        gN = G_SI * Mb * MSUN / r_ ** 2; g_ = 0.5 * (gN + math.sqrt(gN ** 2 + 4 * gN * a0)); return g_ - gN
    lo, hi = 2 * KPC, Dc / 2
    pts = np.logspace(math.log10(lo), math.log10(hi), 4000)
    vals = np.array([u_of(r_) ** power for r_ in pts])
    return float(np.trapezoid(vals, pts) if hasattr(np, "trapezoid") else np.trapz(vals, pts))


rows_b = {}
okb3 = True
for f_ in FOOTS:
    a0 = A0[f_]
    for Mb in (1e11, 1e12):
        I2 = 2 * gal_int(Mb, a0, 2)                                     # both ends
        I1 = gal_int(Mb, a0, 1)                                          # one end's int u dl (cross term bound)
        for Ln, Lv in LSTAR.items():
            pref = 0.75 * Lv ** 2 / C_SI ** 4
            clock = pref * u2avg_used
            galt = pref * I2 / Dc
            cross_bound = pref * 2 * math.sqrt(u2avg_used) * I1 / Dc        # one end; equal galaxies cancel exactly
            tot = clock + galt
            ok = (-3e-15 < tot - cross_bound) and (tot + cross_bound < 7e-16)
            okb3 &= ok if Mb == 1e11 or True else True
            rows_b[f"{f_}|Mb{Mb:.0e}|{Ln}"] = dict(clock=clock, galaxies=galt, cross_bound=cross_bound, total=tot, inside_bound=ok)
            P(f"   {f_:9s} M_b {Mb:.0e} L* {Ln:5s}: clock {clock:.3e} + galaxies {galt:.3e} (cross <= {cross_bound:.1e}) = {tot:.3e}"
              f" -> {'inside' if ok else 'OUTSIDE'} (-3e-15, 7e-16)")
Lmax_clock = (C_SI ** 2 / math.sqrt(u2avg)) * math.sqrt(7e-16 / 0.75) / KPC if u2avg_used > 0 else float("inf")
Lmax_wall = {f_: (C_SI ** 2 / A0[f_]) * math.sqrt(7e-16 / 0.75) / KPC for f_ in FOOTS}
line40 = 1.74 * C_SI / Dc
Lmax_40 = (C_SI ** 2 / math.sqrt(u2avg)) * math.sqrt(line40 / 0.75) / KPC
P(f"   L*_max from the full path average (clock-dominated, footing-independent): {Lmax_clock:.3f} kpc; wall worst case "
  f"{Lmax_wall['canonical']:.3f} / {Lmax_wall['alt']:.3f} kpc (can/alt); WT-02 path model 16-33 kpc")
P(f"   sensitivity (no class weight): 7e-16 is 1.74 s over the conservative 26 Mpc; 1.74 s over D_c = {Dc / MPC:.1f} Mpc gives "
  f"{line40:.2e} -> L*_max {Lmax_40:.3f} kpc")
# report only (no class weight; not in the frozen criteria): cross-check of the independent sol61 audit's FRW tensor coefficient
# Q_T = 1 - 3 gamma chidot^2/K = 1 - (gamma rho_c^2/2)/(rho_tot c^2) (a67f9ed9c, RESULT.md), with CFG938's declared T_CMB, N_eff
rho_crit0 = 3 * H0_SI ** 2 / (8 * math.pi * G_SI)
Og = 7.5657e-16 * 2.7255 ** 4 / C_SI ** 2 / rho_crit0; Orad = Og * (1 + 0.22711 * 3.046)
def QT_def(zz, Lv):
    rc = Oc0 * rho_crit0 * (1 + zz) ** 3
    rt = rho_crit0 * (Orad * (1 + zz) ** 4 + Om0 * (1 + zz) ** 3 + OL0)
    return math.pi * G_SI * Lv ** 2 * rc ** 2 / (rt * C_SI ** 2)
def Q_T(zz, Lv):
    return 1 - QT_def(zz, Lv)
qrows = {}
for Ln, Lv in LSTAR.items():
    q4e8 = Q_T(4e8, Lv); q0 = 1 - QT_def(0, Lv); d0 = QT_def(0, Lv)
    zc = math.exp(brentq(lambda lz: Q_T(math.exp(lz) - 1, Lv), math.log(2.0), math.log(1e10)))
    qrows[Ln] = dict(one_minus_Q_T_z0=d0, Q_T_z4e8=q4e8, onepluszQ0=zc)
    P(f"   [report only] 1 - Q_T(z = 0) = {d0:.3e} (= 1.5 (L* ubar/c^2)^2 incl. Lambda in H); Q_T(z = 4e8) = {q4e8:.4f} (sol61 audit: "
      f"{'-1325.4188' if Ln == '24pc' else '-2302809.5030'}); Q_T = 0 at 1 + z = {zc:.3e}   [L* = {Ln}]")
RES["B_QT_sol61_crosscheck"] = qrows
RES["B_numbers"] = dict(local=num_b, path=rows_b, Lmax_clock_kpc=Lmax_clock, Lmax_wall_kpc=Lmax_wall, Dc_Mpc=Dc / MPC,
                        ubar0=ubar(0), u2avg=u2avg, line_at_Dc=line40, Lmax_at_Dc_kpc=Lmax_40)
b1 = sp.simplify(C_sp) != 0
b2 = sp.simplify(C_sp - sp.Rational(3, 2)) == 0
b3 = okb3
if not MUT:
    P(f"\n  (b1) A5 'c_T = c (structural)' wrong: {'CONFIRMED' if b1 else 'NOT CONFIRMED'}")
    P(f"  (b2) size 0.75 L*^2 u^2/c^4: {'CONFIRMED' if b2 else 'NOT CONFIRMED'}")
    P(f"  (b3) GW170817 passes on the full path average at L* = 24 pc and 1 kpc, both footings: {'CONFIRMED' if b3 else 'NOT CONFIRMED'}"
      f"; but the margin is L*_max = {Lmax_clock:.2f} kpc (clock), not 16-33 kpc")
    RES["B_class"] = dict(b1="CONFIRMED" if b1 else "NOT CONFIRMED", b2="CONFIRMED" if b2 else "NOT CONFIRMED",
                          b3="CONFIRMED" if b3 else "NOT CONFIRMED", Lmax_clock_kpc=Lmax_clock)
else:
    tau2nc, _ = tensor_tau2(V0, U0, christ=False)
    chk("MU3_no_Christoffel_gives_cT_equal_c", sp.simplify(tau2nc) == 0, f"<tau^2> without Christoffels = {tau2nc}")
    clock_vals = [v["clock"] for v in rows_b.values()]
    chk("MU4_no_clock_drops_to_galaxy_only", all(cv == 0 for cv in clock_vals) and
        sp.simplify(BX["timelike"].subs(V0, 0)) == 0,
        f"FRW (timelike) correction at V0 = 0: {sp.simplify(BX['timelike'].subs(V0, 0))}; path totals now galaxy-only "
        f"(max {max(v['total'] for v in rows_b.values()):.2e})")
guard("B")

# =============================================================================================== PART C: cosmic clock
P("\n==================== C. THE COSMIC CLOCK ====================")
rate = Oc0 * H0_SI / 2
P(f"  from A: u^2 = |d_x dchi/a + a chibar' xi'/c^2|^2 -> u_v = |chibar'| v / c^2 = (Omega_c H0/2) v = {rate:.4e} s^-1 x v")
cc = {}
for v_ in (30e3, 370e3, 630e3, 1000e3):
    gam_v = 1 / math.sqrt(1 - (v_ / C_SI) ** 2)
    uv = gam_v * rate * v_
    cc[f"{v_ / 1e3:g}"] = dict(u_v=uv, can=uv / A0["canonical"], alt=uv / A0["alt"])
    P(f"   v = {v_ / 1e3:6g} km/s: u_v = {uv:.4e} m/s^2 = {uv / A0['canonical']:.3e} a0 (can) / {uv / A0['alt']:.3e} a0 (alt)")
cval = cc["370"]["can"]
chk("c_number_1p1e-3_at_370", abs(cval / 1.1e-3 - 1) < 0.05, f"u_v/a0 at 370 km/s = {cval:.4e} (canonical); alt {cc['370']['alt']:.3e}")
vis = {}
# SPARC: NGC 3198 outermost point
dat = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat"), comments="#")
Ro = dat[-1, 0] * KPC; gNo = (dat[-1, 3] * abs(dat[-1, 3]) + 0.61 * dat[-1, 4] * abs(dat[-1, 4]) + 0.61 * dat[-1, 5] * abs(dat[-1, 5])) * 1e6 / Ro
for f_ in FOOTS:
    go = 0.5 * (gNo + math.sqrt(gNo ** 2 + 4 * gNo * A0[f_])); uo = go - gNo
    for vk in ("370", "630"):
        r1 = cc[vk]["u_v"] / uo
        vis[f"SPARC|{f_}|{vk}"] = dict(first_order=r1, second_order=r1 ** 2, label="NOT VISIBLE" if r1 < 0.1 * 0.26 else "UNDERDETERMINED")
        P(f"   SPARC NGC 3198 r = {Ro / KPC:.1f} kpc {f_:9s} v {vk}: u_v/u = {r1:.2e} (dipole, cancels in the azimuthal average), "
          f"(u_v/u)^2 = {r1 ** 2:.1e} vs rms 0.10 dex (26%) -> {vis[f'SPARC|{f_}|{vk}']['label']}")
gwb = G_SI * 1.5 * MSUN / (1e4 * 1.495978707e11) ** 2
for vk in ("370", "630"):
    r_ = cc[vk]["u_v"] / gwb
    vis[f"WB|{vk}"] = dict(ratio=r_, label="NOT VISIBLE" if r_ < 0.1 * 0.03 else "UNDERDETERMINED")
    P(f"   wide binary 1.5 Msun at 10 kAU: g = {gwb:.2e}; u_v/g = {r_:.2e} vs DR4 few-% scale -> {vis[f'WB|{vk}']['label']}")
for Ln, Lv in LSTAR.items():
    pull = G_SI * MSUN / Lv ** 2
    a1sig = 3.4e-5 * (370e3 * 30e3 / C_SI ** 2) * G_SI * MSUN / 1.495978707e11 ** 2
    vis[f"SS|{Ln}"] = dict(pull=pull, alpha1_signal=a1sig, ratio=pull / a1sig, label="NOT VISIBLE" if pull / a1sig < 0.1 else "UNDERDETERMINED")
    P(f"   Solar System L* {Ln}: whole tether pull <= GM_sun/L*^2 = {pull:.2e} m/s^2 vs alpha1-bound signal {a1sig:.2e} -> ratio "
      f"{pull / a1sig:.2e} -> {vis[f'SS|{Ln}']['label']}")
H72 = [(1.50e10, 1.67), (3.66e10, 2.07), (6.01e10, 3.44), (9.13e10, 2.77)]       # LEDGER line 38 (h72)
for f_ in FOOTS:
    for vk in ("370", "630", "1000"):
        ratios = []
        for Mb, rend in H72:
            rx = math.sqrt(G_SI * Mb * MSUN * A0[f_]) / cc[vk]["u_v"] / MPC
            ratios.append(rx / rend)
        lab = "NOT VISIBLE" if min(ratios) > 10 else ("VISIBLE" if min(ratios) <= 1 else "UNDERDETERMINED")
        vis[f"KiDS|{f_}|{vk}"] = dict(rx_over_rend=ratios, label=lab)
        P(f"   KiDS h72 {f_:9s} v {vk:>4s}: r_x/r_end = {', '.join(f'{q:.2f}' for q in ratios)} -> {lab}")
P("   linear growth: the clock enters the medium's inertia at O(c^0): factor 1 - K rho_c/(9H^2) = "
  f"{1 - Oc0 / 6:.4f} (z = 0) / {1 - bgvals(10)['Oc'] / 6:.4f} (z = 10) -- the term behind CFG941's a^0.694 (a recorded number; no data test)")
RES["C"] = dict(u_v=cc, visibility=vis)
guard("C")

# =============================================================================================== PART D: WT-05 light checks
P("\n==================== D. WT-05 vs CFG955 / CFG958 (light checks) ====================")
xs_ = sp.Symbol("x", real=True)
fx = sp.Function("f")(xs_); vx = sp.Function("v")(xs_)
integrand = (sp.log(fx) + 1) * sp.diff(vx * fx, xs_) - fx * sp.diff(vx, xs_)
total_der = sp.simplify(integrand - sp.diff(vx * fx * sp.log(fx), xs_))
chk("D1_drift_entropy_identity", total_der == 0, "dS/dt (Boltzmann, position drift) = Int f div v_s exactly (integrand minus d_x[v f ln f] = 0)")
# deficit filling example: rho_c = f_fill rho_ph, div v_s = -alpha tau K (rho_ph - rho_c)
ff = 0.7
xg = np.linspace(-6, 6, 4001); rph = np.exp(-xg ** 2 / 2); rc = ff * rph
dSdt = -np.trapezoid(rc * (rph - rc), xg) if hasattr(np, "trapezoid") else -np.trapz(rc * (rph - rc), xg)
P(f"   deficit filling (rho_c = {ff} rho_ph, alpha tau K = 1): dS/dt = {dSdt:.4f} < 0 -> the drift compresses phase space (WT-05 S6 sign)")


def emden(xmax=400.0):
    def rhs(s, yv): return [yv[1], math.exp(-yv[0]) - 2 * yv[1] / s]
    s0 = 1e-6
    return solve_ivp(rhs, (s0, xmax), [s0 ** 2 / 6, s0 / 3], rtol=1e-11, atol=1e-13, dense_output=True)


sol = emden()
xs_g = np.logspace(-3, math.log10(399), 200000)
Y = sol.sol(xs_g); vv = xs_g * Y[1]; uu2 = xs_g * np.exp(-Y[0]) / Y[1]
i_can = int(np.argmax(vv)); lam_ = (uu2 - 1.5) / vv; i_mic = int(np.argmin(lam_))
P(f"   isothermal sphere: canonical threshold (max beta G M/R) at contrast {math.exp(Y[0][i_can]):.1f}; microcanonical (min E R/G M^2) at "
  f"contrast {math.exp(Y[0][i_mic]):.0f}, lambda = {lam_[i_mic]:.4f}")
chk("D2_isothermal_thresholds_32p1_709", abs(math.exp(Y[0][i_can]) - 32.1) < 0.3 and abs(math.exp(Y[0][i_mic]) - 709) < 5,
    f"{math.exp(Y[0][i_can]):.2f} / {math.exp(Y[0][i_mic]):.1f} (WT-05 K3: 32.12 / 708.6)")
RES["D"] = dict(dSdt_example=dSdt, canonical=math.exp(Y[0][i_can]), micro=math.exp(Y[0][i_mic]))

# =============================================================================================== summary
P("\n==================== SUMMARY ====================")
if not MUT:
    P(f"  (a) frozen-rule class {RES['A']['class_frozen']}; A1 (full GR, post hoc) {RES['A']['class_A1']}")
    P(f"  (b) b1 {RES['B_class']['b1']}; b2 {RES['B_class']['b2']}; b3 {RES['B_class']['b3']} (L*_max {Lmax_clock:.2f} kpc from the clock)")
    kl = {q: v["label"] for q, v in RES["C"]["visibility"].items() if q.startswith("KiDS")}
    P(f"  (c) CONFIRMED (u_v/a0 = {cval:.3e} at 370 km/s); visibility: SPARC/WB/Solar System NOT VISIBLE; KiDS {kl}")
    allK = all(v["pass_"] for q, v in RES["checks"].items())
    P(f"  all checks pass: {allK}")
    for q, v in RES["checks"].items():
        if not v["pass_"]:
            P(f"   failing check: {q}")
    dump(); sys.exit(0)
else:
    mu = {q: v["pass_"] for q, v in RES["checks"].items() if q.startswith("MU")}
    P(f"  MUTATE teeth: {mu}")
    dump(); sys.exit(1 if all(mu.values()) else 2)
