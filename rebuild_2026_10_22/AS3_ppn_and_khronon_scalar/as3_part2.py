#!/usr/bin/env python3
"""AS3 Part 2: khronon + scalar + (D^2 chi)^2. R0 order disagreement, G-Ost, G-Q2, G-FRW, G-H4. Outputs as3_part2{,_MUTATE}.out/.json, no timing.
16 pi G = 1. Row (unitary gauge): L = sqrt(h) N [R3 + K_ij K^ij - K^2 + Nf(2 a.V - V^2) - wJ V^2 - c (D^2 phi)^2 + 2 K(Q)], Nf = 2, c = L^2, wJ = 2 S. K' = n/2, K'' = 2M/q^2, M = mu^2.
AS3_MUTATE=1 flips the EH sign and the a.V sign. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
import numpy as np, sympy as sy
from scipy.integrate import solve_ivp, quad
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = os.environ.get("AS3_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""; SG = -1 if MUT else 1
L_, CH, RES = [], [], {}
def say(s=""):
    L_.append(s); print(s, flush=True)
def check(n, ok, d=""):
    CH.append((n, bool(ok))); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {d}")
R = sy.Rational
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
LSTAR = {"canonical": 21.7, "alt": 22.9}
GM = 1.32712440018e20; AU = 1.495978707e11; PC = 3.0857e16; Msun = 1.989e30; G = 6.674e-11; HEES = 9e-27; c0 = 299792458.0; MPC = 1e6 * PC

# ---------------------------------------------------------------- exact FRW quadratic action in unitary gauge, then the Stueckelberg map
say("=== R0(c) exact L2 on EdS dust FRW, unitary gauge, real plane wave ===")
e = sy.Symbol("e")
a, H, Hd, k2, q, n, Mm, Nf, wJ, cL = sy.symbols("a H Hd k2 q n M Nf wJ c", positive=True)
al, Bf, ze, zd, ch, chd = sy.symbols("alpha B zeta zetad chi chid")
def unitary_L2():
    # grad products: grad x . grad y -> k2 x y, lap x -> -k2 x. All carried at their true order in e.
    A_, Z, Zd, C, Cd, B_ = e * al, e * ze, e * zd, e * ch, e * chd, e * Bf
    N = 1 + A_
    sqh = a ** 3 * (1 + 3 * Z + sy.Rational(9, 2) * Z ** 2)
    ih2 = (1 - 2 * Z + 2 * Z ** 2) / a ** 2   # h^ij = e^{-2 zeta}/a^2
    DB = ih2 * (-k2 * B_ + k2 * Z * B_)          # D^2 B = e^{-2z} a^-2 (lap B + grad z . grad B)
    Hz = H + Zd
    Kin = (1 - A_ + A_ ** 2) * (-6 * Hz ** 2 + 4 * Hz * DB)
    R3 = -ih2 * (4 * (-k2 * Z) + 2 * k2 * Z ** 2)
    pot = N * R3
    gNV = 2 * Nf * SG * ih2 * k2 * A_ * C                 # N a^i V_i = D^i N D_i phi
    YY = -(Nf + wJ) * N * ih2 * k2 * C ** 2
    st = -cL * N * (k2 * C / a ** 2) ** 2
    Q_dev = (q + Cd - ih2 * k2 * B_ * C) * (1 - A_ + A_ ** 2) - q
    Kq = N * (n * Q_dev + (2 * Mm / q ** 2) * Q_dev ** 2)      # 2K = n dQ + 2 m2 dQ^2, m2 = M/q^2; K(q) = 0 (dust)
    L = sqh * (SG * Kin + SG * pot + gNV + YY + st + Kq)
    L = sy.expand(L)
    return L.coeff(e, 0), L.coeff(e, 1), L.coeff(e, 2)
L0_, L1_, L2_ = unitary_L2()
# tadpoles: linear in alpha, zeta after by parts vanish on the background
tad_al = sy.simplify(L1_.coeff(al)); tad_zd = L1_.coeff(zd); tad_z = L1_.coeff(ze)
rho = n * q
def Ddt(expr):
    """d/dt of a coefficient: a' = a H, H' = Hd, Hd' = 3 H^3 (EdS Hd = -3H^2/2), n' = -3 H n"""
    return sy.diff(expr, a) * a * H + sy.diff(expr, H) * Hd + sy.diff(expr, Hd) * (3 * H ** 3) + sy.diff(expr, n) * (-3 * H * n)
frw = {n: 6 * H ** 2 / q, Hd: -sy.Rational(3, 2) * H ** 2}
if not MUT:
    check("R0c-0 tadpole of alpha vanishes on Friedmann 6 H^2 = rho", sy.simplify(tad_al.subs(n, 6 * H ** 2 / q)) == 0, f"{sy.simplify(tad_al)}")
    tz = sy.simplify((tad_z - Ddt(tad_zd)).subs(frw).subs(k2, 0))     # the linear lap(zeta) term averages to 0 on a plane wave
    check("R0c-1 tadpole of zeta vanishes on 2Hd + 3H^2 = 0", tz == 0, f"{tz}")
else:
    say("  MUTATE: EH sign flipped, tadpole checks expected to fail")
    check("R0c-0 tadpole of alpha vanishes on Friedmann 6 H^2 = rho", sy.simplify(tad_al.subs(n, 6 * H ** 2 / q)) == 0, "")
# Stueckelberg map, Newtonian-gauge fields: alpha = Phi + th_d, zeta = -Psi + H th, B = -th, chi = pi + q th (q' dropped: dust limit, error order H^2/M)
Ph, Ps, Psd, th, thd, pi_, pid = sy.symbols("Phi Psi Psid theta thetad pi pid")
mp = {al: Ph + thd, ze: -Ps + H * th, zd: -Psd + Hd * th + H * thd, Bf: -th, ch: pi_ + q * th, chd: pid + q * thd}
Ln = sy.expand(L2_.subs(mp, simultaneous=True))
pos = [Ph, Ps, th, pi_]; vel = [None, Psd, thd, pid]
syms = [Ph, Ps, th, pi_, Psd, thd, pid]
P_ = sy.Poly(Ln, *syms)
# symmetric splitting: c x y_dot = (c/2)(x y_dot - x_dot y) - (c_dot/2) x y; c x x_dot = -(c_dot/2) x^2
qq = {}                 # no-derivative quadratic coefficient (x, y)
vv = {}                 # (xd, yd)
sk = {}                 # antisym (x, y): c/2 (x yd - xd y)
pidx = {Ps: Psd, th: thd, pi_: pid}
for mon, cf in P_.terms():
    lst = [s for s, m_ in zip(syms, mon) for _ in range(m_)]
    x, y = lst
    d = [s in (Psd, thd, pid) for s in lst]
    if not any(d):
        qq[(x, y)] = qq.get((x, y), 0) + cf
    elif all(d):
        vv[(x, y)] = vv.get((x, y), 0) + cf
    else:
        u, dv = (lst if d[1] else lst[::-1])
        v_ = {Psd: Ps, thd: th, pid: pi_}[dv]
        cd = Ddt(cf)
        qq[(u, v_)] = qq.get((u, v_), 0) - cd / 2
        if u != v_:
            sk[(u, v_)] = sk.get((u, v_), 0) + cf
ix = {Ph: 0, Ps: 1, th: 2, pi_: 3}
vd = {Psd: Ps, thd: th, pid: pi_}
def build_M(w_):
    """Hermitian frozen matrix: L -> f^dag M f for f(t) exp(-i w t) real-wave average."""
    M = sy.zeros(4, 4)
    for (x, y), cf in qq.items():
        M[ix[x], ix[y]] += cf / 2; M[ix[y], ix[x]] += cf / 2
    for (x, y), cf in vv.items():
        i, j = ix[vd[x]], ix[vd[y]]
        M[i, j] += cf * w_ ** 2 / 2; M[j, i] += cf * w_ ** 2 / 2
    for (x, y), cf in sk.items():
        i, j = ix[x], ix[y]
        # c/2 (x yd - xd y): conj(x)(-i w y)(c/2) + conj(i w x... ) -> Hermitian
        M[i, j] += -sy.I * w_ * cf / 2; M[j, i] += sy.I * w_ * cf / 2
    return M
# coefficient table in (Phi, Psi, theta, chi), the unitary variable chi kept
mp2 = {al: Ph + thd, ze: -Ps + H * th, zd: -Psd + Hd * th + H * thd, Bf: -th, ch: pi_, chd: pid}     # pi_ now stands for chi
Ln2 = sy.expand(L2_.subs(mp2, simultaneous=True))
P2 = sy.Poly(Ln2, *syms)
Tb = {}
for mon, cf in P2.terms():
    lst = [s_ for s_, m_ in zip(syms, mon) for _ in range(m_)]
    x, y = lst
    d = [s_ in (Psd, thd, pid) for s_ in lst]
    if d == [False, False]:
        Tb[(x, y)] = Tb.get((x, y), 0) + cf
    elif d[1] and not d[0] and {Psd: Ps, thd: th, pid: pi_}[y] == x:
        Tb[(x, x)] = Tb.get((x, x), 0) - Ddt(cf) / 2           # x x_dot by parts
    else:
        Tb[(x, y)] = Tb.get((x, y), 0) + cf
hand = {(Ps, Ps): 2 * a * k2, (Ph, Ps): -4 * a * k2, (Ph, pi_): 2 * Nf * SG * a * k2 - 4 * Mm / q * a ** 3 * 0, (pi_, pi_): -(Nf + wJ) * a * k2 - cL * k2 ** 2 / a,
        (th, pi_): rho * a * k2 / q, (th, th): -rho * a * k2 / 2, (pi_, thd): 2 * Nf * SG * a * k2}
worst = 0; tabr = {}
for kaH in (300.0, 1000.0):
    Hv = 1 / kaH
    vals = {a: 1, H: Hv, Hd: -1.5 * Hv ** 2, k2: 1, q: 1, n: 6 * Hv ** 2, Mm: 4, Nf: 2, wJ: 1, cL: sy.Rational(1, 2)}
    for key, hv in hand.items():
        fv = float(sy.N(Tb.get(key, 0).subs(vals))) if key in Tb else 0.0
        hvv = float(sy.N(hv.subs(vals)))
        d_ = abs(fv / hvv - 1) if hvv else abs(fv)
        tabr[f"{kaH}|{key}"] = dict(frw=fv, hand=hvv, rel=d_)
        say(f"  k/aH {kaH:6.0f} coefficient {str(key):22s}: exact FRW {fv:+.8g}, hand {hvv:+.8g}, rel diff {d_:.2e}")
        worst = max(worst, d_)
RES["R0_coeffs"] = tabr
check("R0a (a) and (c) agree within 1e-3 at k/aH >= 300, coefficient by coefficient, including -(rho/2) a k2 theta^2, the term the unitary swindle dropped", worst < 1e-3, f"worst rel diff {worst:.3g}")
say("\n=== R0(a) hand Newtonian-limit dispersion ===")
def Gamma2(kk, nv, Mv, Lc2, S=0.0, nu=0.0):
    """Gamma^2 > 0 growth, formula: omega^2 = (n/4)(2k^2/Z - 1), Z = 2M + 4 k^2/D, D = 2(1+S) + c k^2 - nu"""
    D = 2 * (1 + S) + Lc2 * kk ** 2 - nu
    Z = 2 * Mv + 4 * kk ** 2 / D
    return -(nv / 4) * (2 * kk ** 2 / Z - 1)
w_ = sy.Symbol("w", real=True)
# time-dependent check: with k_phys = k/a the reduced L = a^3 [T(k/a) psi_dot^2 - (n/2)(k/a)^2 psi^2], T = 2 p^2 Z/(2 p^2 - Z), p = k/a. Integrate on EdS, compare with delta'' + 2H delta' = 4 pi G rho s delta.
def edS(kmu, a_i=1e-3):
    """k/mu in comoving units at a = 1; time variable x = ln a, H = a^-1.5 in units H0 = 1, n(a) = 6 a^-3"""
    def Tk(a_):
        p2 = (kmu / a_) ** 2; Z = 2 + 2 * p2     # mu = 1, c = 0, nu = 0
        return 2 * p2 * Z / (2 * p2 - Z)
    def f(x, y):
        a_ = math.exp(x); Hh = a_ ** -1.5; Pi, ps, dl = y
        p2 = (kmu / a_) ** 2; n_ = 6 * a_ ** -3
        return [-n_ * p2 * a_ ** 3 * ps / Hh, Pi / (2 * a_ ** 3 * Tk(a_)) / Hh, p2 * ps / Hh]
    def g(x, y):
        a_ = math.exp(x); Hh = a_ ** -1.5; d_, dp = y
        p2 = (kmu / a_) ** 2; s_ = 1 / (1 + p2)
        return [dp, -(2 - 1.5) * dp + 1.5 * s_ * d_]
    # IC: deep dust, psi_dot = Phi const: psi = Phi t, Phi = -1 normalised
    t_i = (2 / 3) * a_i ** 1.5; H_i = a_i ** -1.5
    ps0 = t_i; Pi0 = -6 * (2 / 3) * kmu ** 2 * a_i      # Pi = 2 a^3 T psi_dot = -n a^3 delta: the first integral of the action equation, same IC as the ODE
    so = solve_ivp(f, [math.log(a_i), 0], [Pi0, ps0, (2 / 3) * kmu ** 2 * a_i], method="DOP853", rtol=1e-9, atol=1e-40)
    so2 = solve_ivp(g, [math.log(a_i), 0], [a_i, a_i], method="DOP853", rtol=1e-9, atol=1e-30)
    return so, so2
tdc = {}
for kmu_ in (1e-4, 1e-3, 3e-3, 1e-2):
    so, so2 = edS(kmu_)
    tdc[str(kmu_)] = dict(action_delta=float(so.y[2, -1] / ((2 / 3) * kmu_ ** 2)), ode_delta=float(so2.y[0, -1]))
    say(f"  EdS, k/mu at a = 1 {kmu_:g}: reduced action delta(a = 1)/dust limit {tdc[str(kmu_)]['action_delta']:.5f}; M1 kernel ODE {tdc[str(kmu_)]['ode_delta']:.5f}")
RES["time_dep"] = tdc
check("R0i time-dependent: the row's reduced action on EdS is M1's kernel ODE (delta = int p^2 psi dt), 1e-5", all(abs(v["action_delta"] / v["ode_delta"] - 1) < 1e-5 for v in tdc.values()), f"worst {max(abs(v['action_delta'] / v['ode_delta'] - 1) for v in tdc.values()):.2e}")
gk = Gamma2(0.01, 1e-8, 1.0, 0.0)
check("R0b Gamma^2(k = 0.01 mu)/(4 pi G rho) within 10 % (I3b's line)", abs(gk / (1e-8 / 4) - 1) < 0.1, f"{gk / (1e-8 / 4):.6f}")
kk_ = sy.Symbol("k", positive=True); mu2 = sy.Symbol("mu2", positive=True); c2_ = sy.Symbol("c2", positive=True)
D_ = 2 + c2_ * kk_ ** 2; Z_ = 2 * mu2 + 4 * kk_ ** 2 / D_
s_exact = sy.simplify(1 - 2 * kk_ ** 2 / Z_)
sM1 = mu2 / (kk_ ** 2 + mu2)
check("R0e at c = 0, nu = 0 the kernel is M1's and H1's s = mu^2/(k^2 + mu^2) exactly", sy.simplify(s_exact.subs(c2_, 0) - sM1) == 0, f"{sy.simplify(s_exact.subs(c2_, 0))}")
sH4 = sy.simplify(2 * kk_ ** 2 / Z_ - 2 * kk_ ** 2 / (2 * mu2 + 4 * kk_ ** 2 / (2 + c2_ * kk_ ** 2)))
H4f = kk_ ** 2 / (mu2 + kk_ ** 2 / (1 + c2_ * kk_ ** 2 / 2))
check("R0f at nu = 0, S = 0 the bracket is H4's k^2/chi / (4 pi G) exactly", sy.simplify(2 * kk_ ** 2 / Z_ - H4f) == 0, "the row's scalar pair is v3's pair at nu -> 0")
kcs = sy.Symbol("kc", positive=True)
def kc(mu2v, L2v):
    f = lambda K: (2 + L2v * K) * (K - mu2v) - 2 * K
    return math.sqrt(max(np.roots([L2v, 2 - L2v * mu2v - 2, -2 * mu2v]).real))
kc1 = kc(1.0, (24e-6) ** 2)
check("R0g band edge k_c = 242 mu at mu^-1 = 1 Mpc, L = 24 pc (H1's number), 1e-3", abs(kc1 / (2 / (24e-6) ** 2) ** 0.25 - 1) < 1e-3 and abs(kc1 / 242.7 - 1) < 1e-3, f"k_c {kc1:.2f} mu; formula (2mu^2/L^2)^(1/4) = {(2 / (24e-6) ** 2) ** 0.25:.2f}")

say("\n=== R0(b) as2_indep's committed determinant, then with the missing term ===")
ws, ks, Fs, nn, m2s, NFs, LLs = sy.symbols("w k F n m2 NF L2", positive=True)
def indep_det(add):
    """Re-derived by hand from as2_indep.py's forms: L = quadratic in alpha, B, zeta, chi at Fourier level (real wave). add = coefficient of (grad B)^2."""
    al_, B_, z_, c_ = sy.symbols("al_ B_ z_ c_")
    # L = -6 w^2 z^2 + 4 (w k^2 cross z B) + 2 k^2 z^2 + 4 k^2 al z + 2 NF k^2 al c - (NF + F) k^2 c^2 - L2 k^4 c^2 + 2 m2 |(-i w c - al)|^2 + n cross
    I = sy.I
    idx = 4; M = sy.zeros(4, 4)
    M[2, 2] = -6 * ws ** 2 + 2 * ks ** 2
    M[0, 2] = M[2, 0] = 2 * ks ** 2
    M[1, 2] = 2 * I * ws * ks ** 2; M[2, 1] = -2 * I * ws * ks ** 2  # 4 zeta_dot lap B
    M[0, 3] = M[3, 0] = NFs * ks ** 2
    M[3, 3] = -(NFs + Fs) * ks ** 2 - LLs * ks ** 4 + 2 * m2s * ws ** 2
    M[0, 0] = 2 * m2s
    M[0, 3] += -2 * m2s * (-I * ws); M[3, 0] += -2 * m2s * (I * ws)
    M[1, 3] = M[3, 1] = -nn * ks ** 2 / 2       # -n grad B . grad chi
    M[1, 1] = add * ks ** 2
    return sy.factor(M.det(method="berkowitz"))
d0 = indep_det(0); d1 = indep_det(-nn / 2)
say(f"  no term: {d0}")
cj = json.load(open(os.path.join(HERE, "..", "AS2_action_search", "as2_indep.json")))["det"]
syd = sy.sympify(cj, locals={"w": ws, "k": ks, "F": Fs, "n": nn, "m2": m2s, "NF": NFs, "L2": LLs})
check("R0c as2_indep's committed determinant is reproduced by this hand block (up to a constant)", sy.simplify(syd / d0).is_constant(), f"ratio {sy.simplify(syd / d0)}")
say(f"  with -(n/2)(grad B)^2: {d1}")
def g_of(det, kv, nv, mv):
    W = sy.Symbol("W")
    ex = sy.expand(sy.numer(sy.together(det))).subs(ws, sy.sqrt(W))
    p = sy.Poly(ex.subs({ks: kv, nn: nv, m2s: mv, Fs: 0, NFs: 2, LLs: 0}), W)
    rts = np.roots([complex(c) for c in p.all_coeffs()])
    return rts
kv = sy.Float(0.01, 40); nv = sy.Float(1e-8, 40); mv = sy.Integer(1)
r0_ = g_of(d0, kv, nv, mv); r1_ = g_of(d1, kv, nv, mv)
g0_ = max(-z.real for z in r0_); g1_ = max(-z.real for z in r1_)
say(f"  at k = 0.01 mu, n = 1e-8: Gamma^2/(n/4): committed block {g0_ / (1e-8 / 4):.4g}; with the term {g1_ / (1e-8 / 4):.6f}")
RES["R0b"] = dict(committed=float(g0_ / (1e-8 / 4)), repaired=float(g1_ / (1e-8 / 4)))
check("R0d the committed as2_indep block's ratio is about 0 at k = 0.01 mu (I3b's FAIL)", abs(g0_ / (1e-8 / 4)) < 1e-3, f"{g0_ / (1e-8 / 4):.3g}")
check("R0h adding -(n/2)(grad B)^2 restores Gamma^2 -> n/4 within 10 %", abs(g1_ / (1e-8 / 4) - 1) < 0.1, f"{g1_ / (1e-8 / 4):.6f}")

# ---------------------------------------------------------------- Ostrogradsky
say("\n=== G-Ost: degree in omega, mode pairs, Krein signs ===")
def deg_and_roots(kv, Mv, Lc2, wv, nv, Hv=0.0, F_par=None, rho_ph=0.0, qv=1.0, tp=None):
    """Newtonian-gauge Minkowski or FRW block. Add a static background: rho_ph term -(1/2)rho_ph k2 th^2 and an anisotropic Y. tp = time partner coefficient."""
    Hu = math.sqrt(nv * qv / 6) if nv else (Hv if Hv else 1e-12 * kv)      # Friedmann always: n and H are one quantity
    Ms = build_M(w_).subs({a: 1, H: Hu, Hd: -1.5 * Hu ** 2, k2: kv ** 2, q: qv, n: nv, Mm: Mv, Nf: 2, wJ: wv, cL: Lc2})
    if rho_ph:
        Ms[2, 2] += -sy.Float(rho_ph) * kv ** 2 / 2
    if tp:
        # (box phi + theta Q)^2 at linear order: Xt = -pi_ddot + lap pi + q(Phi_dot + ...) ; here pi and Phi part, theta enters as q lap theta with Q0 and the chi shift
        X = {3: w_ ** 2 - kv ** 2, 0: sy.I * w_ * qv * 0}
        for i, xi in X.items():
            for j, xj in X.items():
                Ms[i, j] += -tp * sy.conjugate(xi) * xj
    ex = sy.expand(Ms.det(method="berkowitz"))
    Pw = sy.Poly(ex, w_)
    cs = [complex(c) for c in Pw.all_coeffs()]
    scale = max(abs(c) for c in cs)
    # strip negligible leading coefficients, Hu -> 0 artefacts
    while len(cs) > 1 and abs(cs[0]) < 1e-14 * scale:
        cs = cs[1:]
    r = np.roots(cs)
    dM = Ms.diff(w_)
    out = []
    for z in r:
        if abs(z.real) < 1e-9 or abs(z.imag) > 1e-7 * max(abs(z), 1e-30):
            continue
        Mz = np.array(Ms.subs(w_, float(z.real)).evalf(30).tolist(), dtype=complex)
        U, s, Vh = np.linalg.svd(Mz)
        vec = Vh[-1].conj()
        dz = np.array(dM.subs(w_, float(z.real)).evalf(30).tolist(), dtype=complex)
        En = (vec.conj() @ dz @ vec).real / (2 * z.real)
        out.append((float(z.real), float(np.sign(En))))
    return len(cs) - 1, r, out
ost = {}
cases = [("FRW k/aH = 245, in band", dict(kv=1.0, Mv=4.0, Lc2=0.0, wv=0.0, nv=1e-4)),
         ("FRW k/aH = 245, past k_c", dict(kv=1.0, Mv=0.01, Lc2=1.0, wv=0.0, nv=1e-4)),
         ("FRW k/aH = 300, past k_c", dict(kv=1.0, Mv=0.01, Lc2=1.0, wv=0.0, nv=6 * (1 / 300.) ** 2)),
         ("static background S = 1, rho_ph > 0", dict(kv=1.0, Mv=0.01, Lc2=1.0, wv=2.0, nv=1e-4, rho_ph=1e-4))]
okd = True; okk = True
for lab, kw_ in cases:
    d_, r_, K_ = deg_and_roots(**kw_)
    ost[lab] = dict(deg=d_, nroots_nz=int(sum(abs(z) > 1e-9 for z in r_)), krein=K_)
    say(f"  {lab}: degree {d_}; nonzero roots {np.round(r_[np.abs(r_) > 1e-9], 7).tolist()}; (omega, Krein) {K_}")
    okd = okd and d_ <= 4 and ost[lab]["nroots_nz"] <= 2
    okk = okk and all(s_ > 0 for _, s_ in K_)
RES["ost"] = ost
check("Ost1 one nonzero root pair at most in every case, no omega^4 branch", okd, "the determinant's other degree is zero roots of the gauge-free block")
check("Ost2 Krein sign positive on every real root outside the Jeans band", okk, "")
dT, rT, KT = deg_and_roots(kv=1.0, Mv=0.0, Lc2=0.0, wv=0.0, nv=0.0, tp=1.0)
say(f"  control (box phi)^2 partner: degree {dT}; roots {np.round(rT[np.abs(rT) > 1e-9], 5).tolist()}; (omega, Krein) {KT}")
RES["ost_control"] = dict(deg=dT, krein=KT)
check("Ost3 control: the time partner gives higher degree and a negative-Krein real root (record's Ostrogradsky)", dT > max(v["deg"] for v in ost.values()) and any(s_ < 0 for _, s_ in KT), f"degree {dT}, {KT}")
say("  structure: in unitary gauge D^2 phi = h^-1/2 d_i(h^1/2 h^ij d_j phi) has no time derivative, so no phi_ddot and no h_ddot enter (unlike q^{ab} nabla_a nabla_b phi, which is D^2 phi - K Q). Only K(Q) carries phi_dot.")
# tilted slice: speed of the row's mode at large k
cinf = lambda nv, Mv, Lc2: math.sqrt((nv / 4) * 2 / (2 * Mv + 4 / Lc2))
sp_ = cinf(1e-4, 0.01, 1.0)
say(f"  large-k dispersion is omega^2 -> c^2 k^2, not k^4: c^2 = (n/4) 2/(2 mu^2 + 4/L^2); at the test point c = {sp_:.4g}. Hyperbolic with c < 1, so tilted slices have real roots while rho_tau > 0. I1's k^4 and tilt problem is the twisting aether's, absent here (khronon: global time).")
RES["cinf"] = sp_

# ---------------------------------------------------------------- Q2
say("\n=== G-Q2: closed form, two-field equation linear about the external field ===")
GEK = {"E1": 1.9 * 9.36e-11, "E2": 2.2 * 9.36e-11, "E3": 2.6 * 9.36e-11}; GNE = 6.913e-11
def x_of(E_, a0):
    if E_ == "E0":
        y = GNE / a0; return (y + math.sqrt(y * y + 4 * y)) / 2
    return GEK[E_] / a0
def Sperp_par(x):
    h = x / (1 + x); S = x          # S(h) = h/(1 - h) = x; S' = 1/(1-h)^2 = (1+x)^2
    return S, S + h * (1 + x) ** 2, h
def I_ang(Sp, Sa):
    return quad(lambda u: (0.5 - 1.5 * u * u) * math.sqrt(Sp * (1 - u * u) + Sa * u * u), -1, 1, epsabs=1e-12, epsrel=1e-12)[0]
Q2tab = {}
for foot, a0 in FOOT.items():
    for E_ in ("E0", "E1", "E2", "E3"):
        x = x_of(E_, a0); Sp, Sa, h = Sperp_par(x); Ia = I_ang(Sp, Sa)
        for Lpc in (LSTAR[foot], 90.0):
            Lm = Lpc * PC
            Q = math.sqrt(2) * GM / Lm ** 3 * Ia
            hed = GM / Lm ** 2
            Q2tab[f"{foot}|{E_}|{Lpc}"] = dict(x=x, Sperp=Sp, Spar=Sa, h=h, Q2=Q, over_Hees=abs(Q) / HEES, hedgehog_over_he=hed / (h * a0))
            say(f"  {foot:9s} {E_} L {Lpc:5.1f} pc: x {x:.3f} S_perp {Sp:.3f} S_par {Sa:.3f}; Q2 {Q:+.3e} s^-2; |Q2|/Hees {abs(Q) / HEES:.2e}, margin {HEES / abs(Q):.2e}; linear validity hedgehog/h_e {hed / (h * a0):.2e}")
RES["Q2"] = Q2tab
okq = all(v["over_Hees"] < 1 for v in Q2tab.values())
check("Q2a every cell under Hees on both footings", okq, f"worst |Q2|/Hees {max(v['over_Hees'] for v in Q2tab.values()):.2e}")
check("Q2b linear about the external field: hedgehog/h_e < 1e-2 in every cell", all(v["hedgehog_over_he"] < 1e-2 for v in Q2tab.values()), f"worst {max(v['hedgehog_over_he'] for v in Q2tab.values()):.2e}")

say("\n  second implementation: axisymmetric finite differences of S_perp lap chi + (S_par - S_perp) dzz chi - (L^2/2) lap^2 chi = 4 pi GM delta_eps, first-order split, ell = 2 projection")
def fd_Q2(Sp, Sa, Nr=220, Nz=440, Rmax=12.0, eps_=0.05):
    # L = 1, GM = 1. grid: rho in (0, R), z in (-R, R); stretched by sinh
    sinh_grid = lambda s, A: Rmax * np.sinh(A * s) / np.sinh(A)
    A_ = 4.0
    rho_f = sinh_grid(np.linspace(0, 1, Nr + 1), A_)
    r_c = 0.5 * (rho_f[1:] + rho_f[:-1])
    z_f = sinh_grid(np.linspace(-1, 1, Nz + 1), A_)
    z_c = 0.5 * (z_f[1:] + z_f[:-1])
    dr = np.diff(rho_f); dz = np.diff(z_f)
    idx = lambda i, j: i * Nz + j
    N_ = Nr * Nz
    I_, J_, V_ = [], [], []
    def lap_entries(i, j):
        out = []
        ri = r_c[i]
        # radial, flux form
        if i > 0:
            co = rho_f[i] / (ri * dr[i] * (r_c[i] - r_c[i - 1])); out.append((idx(i - 1, j), co)); out.append((idx(i, j), -co))
        if True:
            rhi = r_c[i + 1] if i < Nr - 1 else rho_f[-1] + dr[-1] / 2
            co = rho_f[i + 1] / (ri * dr[i] * (rhi - ri))
            if i < Nr - 1:
                out.append((idx(i + 1, j), co))
            out.append((idx(i, j), -co))
        zp = dzz_entries(i, j)
        return out + zp
    def dzz_entries(i, j):
        out = []
        if j > 0:
            co = 1 / (dz[j] * (z_c[j] - z_c[j - 1])); out.append((idx(i, j - 1), co)); out.append((idx(i, j), -co))
        else:
            co = 1 / (dz[j] * dz[j]); out.append((idx(i, j), -co))
        if j < Nz - 1:
            co = 1 / (dz[j] * (z_c[j + 1] - z_c[j])); out.append((idx(i, j + 1), co)); out.append((idx(i, j), -co))
        else:
            co = 1 / (dz[j] * dz[j]); out.append((idx(i, j), -co))
        return out
    # unknowns chi (0..N_-1), w (N_..2N_-1). eq1: w - lap chi = 0. eq2: S_perp w + (S_par - S_perp) dzz chi - (1/2) lap w = rhs
    rhs = np.zeros(2 * N_)
    for i in range(Nr):
        for j in range(Nz):
            p = idx(i, j)
            I_.append(p); J_.append(N_ + p); V_.append(1.0)
            for q_, c_ in lap_entries(i, j):
                I_.append(p); J_.append(q_); V_.append(-c_)
            I_.append(N_ + p); J_.append(N_ + p); V_.append(Sp)
            for q_, c_ in dzz_entries(i, j):
                I_.append(N_ + p); J_.append(q_); V_.append(Sa - Sp) if False else None
                V_.append(Sa - Sp)
            for q_, c_ in lap_entries(i, j):
                I_.append(N_ + p); J_.append(N_ + q_); V_.append(-0.5 * c_)
            rr2 = r_c[i] ** 2 + z_c[j] ** 2
            rhs[N_ + p] = 4 * math.pi * math.exp(-rr2 / (2 * eps_ ** 2)) / ((2 * math.pi) ** 1.5 * eps_ ** 3)
    return None
def fd_Q2b(Sp, Sa, Nr=160, Nz=320, Rmax=12.0, eps_=0.05):
    A_ = 4.0
    rho_f = Rmax * np.sinh(A_ * np.linspace(0, 1, Nr + 1)) / np.sinh(A_)
    z_f = Rmax * np.sinh(A_ * np.linspace(-1, 1, Nz + 1)) / np.sinh(A_)
    r_c = 0.5 * (rho_f[1:] + rho_f[:-1]); z_c = 0.5 * (z_f[1:] + z_f[:-1])
    dr = np.diff(rho_f); dz = np.diff(z_f)
    N_ = Nr * Nz
    id_ = np.arange(N_).reshape(Nr, Nz)
    # operators as COO
    def ops():
        lapR_i, lapR_j, lapR_v = [], [], []
        dzz_i, dzz_j, dzz_v = [], [], []
        for i in range(Nr):
            if i > 0:
                co = rho_f[i] / (r_c[i] * dr[i] * (r_c[i] - r_c[i - 1]))
                lapR_i += list(id_[i]); lapR_j += list(id_[i - 1]); lapR_v += [co] * Nz
                lapR_i += list(id_[i]); lapR_j += list(id_[i]); lapR_v += [-co] * Nz
            rhi = r_c[i + 1] if i < Nr - 1 else rho_f[-1] + dr[-1] / 2
            co = rho_f[i + 1] / (r_c[i] * dr[i] * (rhi - r_c[i]))
            if i < Nr - 1:
                lapR_i += list(id_[i]); lapR_j += list(id_[i + 1]); lapR_v += [co] * Nz
            lapR_i += list(id_[i]); lapR_j += list(id_[i]); lapR_v += [-co] * Nz
        for j in range(Nz):
            if j > 0:
                co = 1 / (dz[j] * (z_c[j] - z_c[j - 1]))
                dzz_i += list(id_[:, j]); dzz_j += list(id_[:, j - 1]); dzz_v += [co] * Nr
                dzz_i += list(id_[:, j]); dzz_j += list(id_[:, j]); dzz_v += [-co] * Nr
            else:
                dzz_i += list(id_[:, j]); dzz_j += list(id_[:, j]); dzz_v += [-1 / dz[j] ** 2] * Nr
            if j < Nz - 1:
                co = 1 / (dz[j] * (z_c[j + 1] - z_c[j]))
                dzz_i += list(id_[:, j]); dzz_j += list(id_[:, j + 1]); dzz_v += [co] * Nr
                dzz_i += list(id_[:, j]); dzz_j += list(id_[:, j]); dzz_v += [-co] * Nr
            else:
                dzz_i += list(id_[:, j]); dzz_j += list(id_[:, j]); dzz_v += [-1 / dz[j] ** 2] * Nr
        return coo_matrix((lapR_v, (lapR_i, lapR_j)), shape=(N_, N_)).tocsr(), coo_matrix((dzz_v, (dzz_i, dzz_j)), shape=(N_, N_)).tocsr()
    LR, DZ = ops()
    from scipy.sparse import bmat, identity
    Lp = LR + DZ
    Id = identity(N_, format="csr")
    Aop = bmat([[-Lp, Id], [(Sa - Sp) * DZ, Sp * Id - 0.5 * Lp]], format="csc")
    rr2 = (r_c[:, None] ** 2 + z_c[None, :] ** 2)
    rhs = np.zeros(2 * N_)
    rhs[N_:] = (4 * math.pi * np.exp(-rr2 / (2 * eps_ ** 2)) / ((2 * math.pi) ** 1.5 * eps_ ** 3)).ravel()
    sol = spsolve(Aop, rhs)
    chi = sol[:N_].reshape(Nr, Nz)
    # ell = 2 projection on spheres
    from scipy.interpolate import RegularGridInterpolator
    ip = RegularGridInterpolator((r_c, z_c), chi, bounds_error=False, fill_value=None)
    u_, wu = np.polynomial.legendre.leggauss(64)
    res = {}
    for r0 in (0.4, 0.6, 0.8):
        pts = np.column_stack([r0 * np.sqrt(1 - u_ ** 2), r0 * u_])
        chi_v = ip(pts)
        P2 = 0.5 * (3 * u_ ** 2 - 1)
        c2_ = 5 / 2 * np.sum(wu * chi_v * P2)     # chi = sum c_l P_l
        res[r0] = c2_ * 3 / r0 ** 2                # chi_2 = (Q/3) r^2 P2 at small r
    return res
def spec_Q2_r(Sp, Sa, r0, eps_=0.05, kmax=400, Nk=6000):
    """Same quantity at finite r0 from the Fourier form, to compare like with like: chi_2(r0) via the Hankel integral at each u."""
    from scipy.special import spherical_jn
    ku = np.geomspace(1e-4, kmax, Nk)
    u_, wu = np.polynomial.legendre.leggauss(64)
    P2 = 0.5 * (3 * u_ ** 2 - 1)
    a_ = (Sp * (1 - u_ ** 2) + Sa * u_ ** 2)
    vals = []
    for kk in ku:
        D = a_ * kk ** 2 + 0.5 * kk ** 4
        chik = -4 * math.pi * math.exp(-(kk * eps_) ** 2 / 2) / D
        chik2 = 5 / 2 * np.sum(wu * chik * P2)
        vals.append(chik2 * (-1) * spherical_jn(2, kk * r0) * kk ** 2 / (2 * math.pi ** 2))
    return np.trapz(vals, ku) * 3 / r0 ** 2
fdr = {}
okfd = True
for foot, E_ in (("canonical", "E2"), ("alt", "E2"), ("canonical", "E0")):
    x = x_of(E_, FOOT[foot]); Sp, Sa, h = Sperp_par(x)
    r = fd_Q2b(Sp, Sa)
    cmp_ = {r0: spec_Q2_r(Sp, Sa, r0) for r0 in r}
    closed = math.sqrt(2) * I_ang(Sp, Sa)
    fdr[f"{foot}|{E_}"] = dict(closed=closed, fd={str(a_): b_ for a_, b_ in r.items()}, spec={str(a_): b_ for a_, b_ in cmp_.items()})
    say(f"  {foot} {E_}: closed form Q2 L^3/GM {closed:+.5f}; Fourier at r0: {[round(v, 5) for v in cmp_.values()]}; FD at r0 0.4, 0.6, 0.8: {[round(v, 5) for v in r.values()]}")
    for r0 in r:
        okfd = okfd and abs(r[r0] / cmp_[r0] - 1) < 0.02
RES["Q2_fd"] = fdr
x_ = x_of("E2", FOOT["canonical"]); Sp_, Sa_, _h = Sperp_par(x_)
n1_ = spec_Q2_r(Sp_, Sa_, 0.02, eps_=0.002, kmax=4000, Nk=20000); n2_ = spec_Q2_r(Sp_, Sa_, 0.01, eps_=0.001, kmax=8000, Nk=30000); cl_ = math.sqrt(2) * I_ang(Sp_, Sa_)
near = 2 * n2_ - n1_
say(f"  r0 -> 0 limit: Fourier at r0 = 0.02, 0.01 L: {n1_:.5f}, {n2_:.5f}, linear extrapolation {near:.5f}; closed form {cl_:.5f}. Hees's r^2 P2 coefficient is the r0 << L limit; planets sit at r/L < 1e-4, where the finite-r0 term (order r0/ell, ell = L/sqrt(2 S)) is under 1e-3")
fdr["near"] = dict(fourier=near, closed=cl_)
check("Q2e the Fourier form, extrapolated in r0, reaches the closed form within 2 %", abs(near / cl_ - 1) < 0.02, f"{near / cl_:.5f}")
check("Q2c second implementation agrees with the Fourier form within 2 % at each radius", okfd, "FD vs Fourier at finite r0; both tend to the closed form as r0 -> 0")
BOUNDS = {}
for pl, fr24 in (("Mars", 0.173), ("Saturn", 0.035), ("Earth", 0.028)):
    BOUNDS[pl] = fr24
ptab = {}
for foot in FOOT:
    for Lpc in (LSTAR[foot], 90.0):
        for pl, fr24 in BOUNDS.items():
            ptab[f"{foot}|{Lpc}|{pl}"] = fr24 * (24.0 / Lpc) ** 2
    say(f"  planets at hedgehog GM/L^2 ({foot}, L {LSTAR[foot]} pc): Mars {ptab[f'{foot}|{LSTAR[foot]}|Mars']:.3f}, Saturn {ptab[f'{foot}|{LSTAR[foot]}|Saturn']:.3f}, Earth {ptab[f'{foot}|{LSTAR[foot]}|Earth']:.3f} of C6's bounds. Same hedgehog as v3 at this action normalisation (c = L^2)")
RES["planets"] = ptab
check("Q2d planets under C6's bounds at the floors", all(v < 1 for v in ptab.values()), f"worst {max(ptab.values()):.3f}")
say("  note: as2_indep's ODE carried L^2 where the action gives L^2/2. That is its factor 2 below the hedgehog in I4b (1.2e-6 vs 2.4e-6).")

# ---------------------------------------------------------------- FRW
say("\n=== G-FRW (i) background: literal quadratic K, stiff partner; rho = 4 M d + 2 M d^2 with d = (Q - q)/q, in 16 pi G = 1 ===")
Qs = sy.Symbol("Q", positive=True); ms = sy.Symbol("m2", positive=True); qs = sy.Symbol("q0", positive=True)
Kx = ms * (Qs - qs) ** 2
rhoQ = sy.simplify(2 * Qs * sy.diff(Kx, Qs) - 2 * Kx); chg = sy.diff(Kx, Qs)
ds = sy.Symbol("d", positive=True)
r_ = sy.expand(rhoQ.subs(Qs, qs * (1 + ds)))
say(f"  rho(d) = {r_}: dust part {sy.simplify(r_.coeff(ds, 1))} d, stiff part {sy.simplify(r_.coeff(ds, 2))} d^2; with M = m2 q0^2 this does not depend on q0")
check("F1a stiff/dust = d/2, independent of q0", sy.simplify(r_.coeff(ds, 2) / r_.coeff(ds, 1) - sy.Rational(1, 2)) == 0, "")
# need d(a): 4 M d = rho_d(a) (16 pi G units) = 6 H0^2 Omega a^-3 ; omega_d = 0.12 is the abundance as an integration constant [Q6's value, reported]
h100 = 100e3 / MPC  # s^-1 per h
def stiff_over_nu(mu_invMpc, Tmev=1.0, omega_d=0.12):
    a_ = 2.35e-10 * (3.91 / 10.75) ** (1 / 3) / Tmev
    rho_d = 6 * h100 ** 2 * omega_d * a_ ** -3 / c0 ** 2     # 1/m^2
    Mv = (mu_invMpc / MPC) ** 2
    dd = rho_d / (4 * Mv)
    rho_s = 2 * Mv * dd ** 2
    # one neutrino species energy density in 16 pi G units
    GeVm = 1.0
    T_J = Tmev * 1.602e-13
    u = (7 / 8) * 2 * (math.pi ** 2 / 30) * T_J ** 4 / (1.0546e-34 * c0) ** 3    # J/m^3
    rnu = 16 * math.pi * G / c0 ** 4 * u
    return rho_s / rnu, dd
mu_need = None
lo, hi = 1.0, 1e12
for _ in range(80):
    md = math.sqrt(lo * hi)
    if stiff_over_nu(md)[0] > 0.5:
        lo = md
    else:
        hi = md
mu_need = hi
say(f"  dN_eff <= 0.5 at 1 MeV needs mu >= {mu_need:.3g} /Mpc = {mu_need / 0.7:.3g} h/Mpc at h = 0.7 [record Q6: 1.84e8 h/Mpc]. Omega_d h^2 = 0.12 is the abundance as an integration constant, Q6's number, read as that")
RES["bbn_mu_need_perMpc"] = mu_need
check("F1b reproduces Q6's BBN line within a factor 2", 0.5 < mu_need / 0.7 / 1.84e8 < 2, f"{mu_need / 0.7:.3g} vs 1.84e8 h/Mpc")
fbg = {}
for mu_ in (0.03, 0.1, 10.0, 411 * 0.7, ):
    so, dd = stiff_over_nu(mu_)
    fbg[str(mu_)] = dict(stiff_over_neutrino=so, d=dd)
    say(f"  mu {mu_:8.3f} /Mpc: at 1 MeV stiff/one neutrino {so:.3g} (line 0.5), d {dd:.3g}: {'FAIL' if so > 0.5 else 'pass'}")
RES["bbn"] = fbg
check("F1c literal quadratic K at mu <= 411 h/Mpc has a radiation era at BBN (a real gate result if it fails)", all(v["stiff_over_neutrino"] <= 0.5 for v in fbg.values()), "dN_eff line")
say("  DBI K (BS25): same background function of K only, so Q7's result carries: dN_eff equiv 4e-6 to 7e-6 [REC Q7], and X4's forest door [REC].")

say("\n=== G-FRW (ii) growth with the row's kernel ===")
try:
    from classy import Class
    has_class = True
except Exception:
    has_class = False
c2b = json.load(open(os.path.join(REPO, "covariant_push_2026_10_22", "C2_aest_cosmology", "c2b_native_cmb_results.json")))["P5"]["lcdm_refit"]
wb_, wc_, th_, lnA_, ns_, tau_ = c2b["params"]; hA = c2b["chi2"]["H0"] / 100.0
Om, Ob = (wb_ + wc_) / hA ** 2, wb_ / hA ** 2
say(f"  Known answer uses M1's own record background and P(k), parameters from C2's JSON: a record reproduction only, not a yardstick and no statement about any fit. CLASS available: {has_class}")
Or_ = 4.18e-5 / hA ** 2
def Ek(a_):
    return math.sqrt(Om * a_ ** -3 + Or_ * a_ ** -4 + (1 - Om - Or_))
def growth_ratio(kk, mu_h, Lc_=0.0, a_i=1e-3):
    kk = np.asarray(kk, float); n_ = len(kk); OK = Om - Ob
    def s_of(a_, mu_):
        if mu_ is None:
            return np.ones(n_)
        x2 = (kk / (a_ * mu_)) ** 2
        return 1 / (1 + x2)
    def go(mu_):
        def rhs(x, st):
            a_ = math.exp(x); E_ = Ek(a_); d_ = -(1.5 * Om * a_ ** -3 + 2 * Or_ * a_ ** -4) / E_ ** 2
            dens = 1.5 * a_ ** -3 / E_ ** 2 * 1.0
            db, gb, dk, gk = st[:n_], st[n_:2 * n_], st[2 * n_:3 * n_], st[3 * n_:]
            sb = dens * (Ob * db + OK * dk); sk = dens * (Ob * db + OK * dk * s_of(a_, mu_))
            return np.concatenate([gb, -(2 + d_) * gb + sb, gk, -(2 + d_) * gk + sk])
        so = solve_ivp(rhs, [math.log(a_i), 0.0], np.full(4 * n_, a_i), method="DOP853", rtol=1e-7, atol=1e-12)
        y = so.y[:, -1]
        return (Ob * y[:n_] + OK * y[2 * n_:3 * n_]) / Om
    return go(mu_h) / go(None)
KS = np.geomspace(1e-4, 50.0, 1500); KT = np.geomspace(1e-3, 3.0, 36)
W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
if has_class:
    cc = Class(); cc.set({"omega_b": wb_, "omega_cdm": wc_, "h": hA, "ln10^{10}A_s": lnA_, "n_s": ns_, "tau_reio": tau_, "N_ur": 3.044, "T_cmb": 2.7255, "output": "mPk", "P_k_max_h/Mpc": 60.0, "z_max_pk": 4.0}); cc.compute()
    Pk = np.array([cc.pk_lin(q_ * hA, 0.0) for q_ in KS]) * hA ** 3
    sig = lambda P: math.sqrt(np.trapz(P * W8(KS * 8.0) ** 2 * KS ** 2, KS) / (2 * math.pi ** 2))
    def s8r(mu_h):
        T = growth_ratio(KT, mu_h); Tf = np.interp(np.log(KS), np.log(KT), T, left=T[0], right=T[-1])
        return sig(Pk * Tf ** 2) / sig(Pk)
    ka_ = s8r(14.8)
    check("F2a M1's 0.391 at 14.8 h/Mpc reproduced within 2 % [record parameters]", abs(ka_ / 0.391 - 1) < 0.02, f"{ka_:.4f}")
    gt = {}
    for lab, mu_h in (("0.03 /Mpc S4 guard", 0.03 / hA), ("0.1 /Mpc S4 guard", 0.1 / hA), ("14.8 h/Mpc BS24 cap", 14.8), ("411 h/Mpc", 411.0)):
        r8 = s8r(mu_h); gt[lab] = r8
        say(f"  {lab}: sigma8 ratio {r8:.4f} (line 0.95, margin {r8 / 0.95:.3g})")
    RES["sigma8"] = gt
    check("F2b growth pass line 0.95 at the galaxy-allowed mu", gt["0.03 /Mpc S4 guard"] >= 0.95 and gt["0.1 /Mpc S4 guard"] >= 0.95, f"{gt['0.03 /Mpc S4 guard']:.4f}, {gt['0.1 /Mpc S4 guard']:.4f}")
    say(f"  X4's ODE numbers 0.0757, 0.0817 [REC], full Boltzmann 0.0032, 0.0052 [REC]. a0 is absent at linear order: both footings identical; S4's guard holds on both [REC].")
else:
    check("F2a CLASS available for M1's known answer", False, "")
say("  static mass term in this row: Phi = chi(1 + S~), chi = -Source/(4[k^2 S~ - M(1 + S~)]), S~ = S + L^2 k^2/2: same form as H2 and S4, so the guard's physics carries; a re-grade on lensing data is not done here.")
gs = []
for nm, r_kpc, v_kms in (("MW 100 kpc", 100.0, 200.0), ("1 Mpc", 1000.0, 200.0)):
    gv = (v_kms * 1e3) ** 2 / (r_kpc * 1e3 * PC)
    for foot, a0 in FOOT.items():
        x_ = gv / a0; mu_p = math.sqrt(x_) / (r_kpc * 1e-3)
        gs.append(f"{nm} {foot}: pole at mu = {mu_p:.2f} /Mpc")
say("  own estimate, pole k^2 S = mu^2 at r: " + "; ".join(gs) + ". So mu <~ 0.1 /Mpc on either footing, in line with S4.")

say("\n=== G-FRW (iii) the nu door: nu = n/(2 Q0^2) enters D = 2(1 + S) + L^2 k^2 - nu ===")
say(f"  at nu > 2 the bracket has a pole at k^2 = mu^2 (nu - 2)/2 (Z = 0, kinetic term through zero): k^2 -> that value gives |Gamma^2| -> infinity. At fixed k, nu falling as a^-3 crosses 2: a singular crossing for every k < mu. To stay at nu < 2 back to T = 1 MeV needs Q0^2 > rho(1 MeV)/4, and then today nu <= 2 (1.67e-10)^3 = {2 * (1.67e-10) ** 3:.2g}: no effect on growth. Door closed by C_k > 0 for all history.")
RES["nu_today_max"] = 2 * (1.67e-10) ** 3
Hs_ = 1e-3; qs_ = Hs_ * math.sqrt(3) / 100; nu_t = 3 * Hs_ ** 2 / qs_ ** 2
_, rn_, _k = deg_and_roots(kv=1.0, Mv=0.0, Lc2=0.0, wv=0.0, nv=6 * Hs_ ** 2 / qs_, qv=qs_)
gn_ = max(abs(z.imag) for z in rn_) ** 2; prd = (6 * Hs_ ** 2 / 4) * (nu_t / 2)
check("F3a the nu term in the exact FRW block at nu = 1e4, M = 0: Gamma^2 = (rho/4)(nu/2), 2 % (frozen coefficients; friction is order q/H = 0.017)", abs(gn_ / prd - 1) < 0.02, f"{gn_:.6g} vs {prd:.6g}")
say("\n=== G-FRW (iv) C7's runaway ===")
say("  C7 attributes it to a tachyonic vector pair, rate^2 ~ 8 pi G rho/K_B. This row has K_B = 0 and no transverse aether: the khronon has A_i = gradient, and V_i is a gradient. The only vector is the constrained metric shift. So that mechanism has no field here. Whether any other runaway exists needs a full Boltzmann run with this row's terms: NOT RUN, ND.")

# ---------------------------------------------------------------- H4
say("\n=== G-H4 negative charge ===")
def h4gam(kk, rho_tau, S, Lc2):
    return Gamma2(kk, rho_tau, 0.0, Lc2, S=S)
rhoneg = -1e-6
gh = h4gam(1e3, rhoneg, 0.0, 1.0)
# 16 pi G = 1: rho16 = 16 pi G rho so 2 pi G |rho| = |rho16|/8
gh4 = (1.0 * 1e3) ** 2 * abs(rhoneg) / 8
check("H1 Gamma^2 = |rho_tau| L^2 k^2/8 = L^2 k^2 2 pi G |rho|: H4's rate, 1e-6", abs(gh / gh4 - 1) < 1e-6, f"{gh:.6g} vs {gh4:.6g}")
ph_ = deg_and_roots(kv=1.0, Mv=0.0, Lc2=1.0, wv=0.0, nv=0.0, rho_ph=-1e-4)
say(f"  exact block with rho_ph = -1e-4 on theta, n = 0, M = 0, L = k: roots {np.round(ph_[1][np.abs(ph_[1]) > 1e-9], 7).tolist()}; hand sqrt(|rho| L^2 k^2/8) = {math.sqrt(1e-4 / 8):.7f}")
okex = any(abs(abs(z.imag) - math.sqrt(1e-4 / 8)) < 1e-6 for z in ph_[1])
check("H2 the exact block gives the same growth rate for the phantom charge on the khronon", okex, "the phantom rides the khronon; the kinetic term is -(rho/2) w^2 from 2 Nf V.(w.grad)w")
kp = sy.Symbol("x"); say("  rho_tau < 0 in this row's own static field: deep field, S = h/a0, gives div(|h| h) = 0 in vacuum, the same equation as deep AQUAL for chi. At a two-body saddle h = b(-rho, 2z): on the axis div h = -2b < 0; in the plane div h = +b. So the negative lobes exist on the axis analytically.")
b_ = sy.Symbol("b", positive=True); xs_, zs_ = sy.symbols("r_ z_", positive=True)
hv = sy.Matrix([-b_ * xs_, 2 * b_ * zs_]); hm = sy.sqrt(hv.dot(hv))
residual = sy.simplify((sy.diff(hm * hv[0] * xs_, xs_) / xs_ + sy.diff(hm * hv[1], zs_)))
dh_axis = sy.simplify(-(hv[1] / hm * sy.diff(hm, zs_)).subs(xs_, 0))
say(f"  check of the sign, -h_hat.grad|h| on the axis at leading order = {dh_axis} (b-field not an exact solution; leading-order argument)")
H4j = json.load(open(os.path.join(HERE, "..", "H4_v3_saddle_stability", "h4_v3_saddle_stability_results.json")))
h4t = {}
G_astro = 4.30091e-3   # pc (km/s)^2 / Msun
kmspc_to_perGyr = 1022.7
for lab, r_can, r_alt, life in (("MW-M31 saddle", 6.2e-7, 6.8e-7, 10.0), ("LMC-MW", 1.0e-4, 1.1e-4, 2.0)):
    for foot, rho_ in (("canonical", r_can), ("alt", r_alt)):
        Lpc = LSTAR[foot]
        for lam in (1.0, 100.0):
            kk = 2 * math.pi / lam
            Gam = Lpc * kk * math.sqrt(2 * math.pi * G_astro * rho_) * kmspc_to_perGyr   # per Gyr
            Sdeep = 0.01
            Gsw = math.sqrt(4 * math.pi * G_astro * rho_ * Sdeep) * kmspc_to_perGyr
            h4t[f"{lab}|{foot}|{lam}"] = dict(rate_perGyr=Gam, efolds=Gam * life, switched_efolds=Gsw * life)
            say(f"  {lab} {foot} rho {rho_:.2g} Msun/pc^3 [H4 README, same deep equation] lambda {lam:g} pc, L {Lpc} pc: e-folds in {life:g} Gyr literal {Gam * life:.3g}; with the switch, at S = 0.01, {Gsw * life:.3g}")
RES["H4"] = h4t
check("H3 literal row well posed where rho_tau < 0 (a real gate result if it fails)", False, "Gamma grows linearly in k without a cap, as H4; the row inherits it")
say(f"  a dust buffer would need n >= |rho_ph|: 6.2e-7 Msun/pc^3 is 15x the mean matter density scale (about 4e-8), so not generic. Switched (max(D^2 phi, 0))^2: bounded rate as above, the record's X3 cure carried by the same algebra; not re-proved for this row's two separate flows (phantom on w, dust on u). The switch is REPORTED, not the row.")
say("  H5-type flow reading: the phantom is transported by the khronon, so the static lobes are states this flow may not reach. Not evaluated here.")

nf = [n_ for n_, o in CH if not o]
say(f"\nCHECKS {len(CH) - len(nf)}/{len(CH)} pass. Failed: {nf}")
RES["checks"] = CH
open(os.path.join(HERE, f"as3_part2{TAG}.out"), "w").write("\n".join(L_) + "\n")
json.dump(RES, open(os.path.join(HERE, f"as3_part2{TAG}.json"), "w"), indent=1, sort_keys=True, default=str)
sys.exit(1 if nf else 0)
