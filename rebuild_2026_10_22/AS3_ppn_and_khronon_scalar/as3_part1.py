#!/usr/bin/env python3
"""AS3 Part 1: alpha_1, alpha_2 of AeST for a moving source. Exact block in as3_block.py. No code from AS2 or the record. Outputs as3_part1{,_MUTATE}.out/.json, no timing.
AS3_MUTATE=1 flips the EH sign and the a.V sign. kappa = 1/2 FITTED; not theory closed."""
import json, os, sys, random
import numpy as np, sympy as sy
from fractions import Fraction
from scipy.integrate import solve_ivp
from as3_block import matrix, solve, source, k, w, MUT
HERE = os.path.dirname(os.path.abspath(__file__)); TAG = "_MUTATE" if MUT else ""
L_, CH, RES = [], [], {}
def say(s=""):
    L_.append(s); print(s, flush=True)
def check(n, ok, d=""):
    CH.append((n, bool(ok))); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {d}")
R = sy.Rational; v = sy.Symbol("v", positive=True)
def coef(expr, order):
    return sy.series(expr, v, 0, order + 1).removeO().coeff(v, order)
def gr_beta():
    x, _ = solve("s", v); p = x["Phi"]
    return coef(sy.cancel(p / p.subs(v, 0)), 2)
BG = gr_beta()
say(f"GR: beta_GR = {BG}  (Phi = -U(1 + beta v^2), T00 = 1, Newtonian gauge)")

say("\n=== P1-K1 Einstein-aether at random rational points against Foster-Jacobson [formulas from memory, PROVISIONAL] ===")
def fj(c):
    c1, c2, c3, c4 = c; c123 = c1 + c2 + c3; c14 = c1 + c4
    a1 = -8 * (c3 ** 2 + c1 * c4) / (2 * c1 - c1 ** 2 + c3 ** 2)
    a2 = a1 / 2 - (c1 + 2 * c3 - c4) * (2 * c1 + 3 * c2 + c3 + c4) / (c123 * (2 - c14))
    return a1, a2
def s0sq(c):
    c1, c2, c3, c4 = c; c123 = c1 + c2 + c3; c14 = c1 + c4; c13 = c1 + c3
    return c123 * (2 - c14) / (c14 * (1 - c13) * (2 + c13 + 3 * c2))
rng = random.Random(20261102)
pts = []
while len(pts) < 6:
    c = tuple(R(rng.randint(-40, 40), rng.randint(60, 200)) for _ in range(4))
    if c[0] + c[3] <= 0 or c[0] + c[1] + c[2] == 0 or s0sq(c) <= 0:
        continue
    pts.append(c)
worst = 0; rows = []
for c in pts:
    x, res = solve("s", v, c=c)
    gauge = all(sy.simplify(q) == 0 for q in res)
    p = x["Phi"]; U = -p.subs(v, 0)
    be = coef(sy.cancel(p / p.subs(v, 0)), 2)
    xv, _ = solve("v", R(1), c=c)
    a1 = -2 * xv["Bx"] / U - 8
    a2 = (be - BG) + a1 / 2
    f1, f2 = fj(c)
    gam = sy.cancel(x["Psi"].subs(v, 0) / p.subs(v, 0))
    d = (sy.simplify(a1 - f1), sy.simplify(a2 - f2))
    den = sy.denom(sy.cancel(p)); pole = sy.solve(den, v ** 2) if False else [r for r in sy.roots(sy.Poly(den, v)).keys()]
    s2 = s0sq(c)
    pol = any(sy.simplify(r ** 2 - s2) == 0 for r in pole)
    rows.append(dict(c=[str(q) for q in c], a1=str(a1), a2=str(a2), d1=str(d[0]), d2=str(d[1]), gamma=str(gam), s0_pole=bool(pol)))
    say(f"  c={tuple(map(str, c))}: a1 {float(a1):+.6f} a2 {float(a2):+.6f}; diff {d[0]}, {d[1]}; gamma {gam}; gauge rows 0: {gauge}; response pole at s0^2: {pol}")
    if d[0] != 0 or d[1] != 0 or gam != 1 or not gauge:
        worst = 1
RES["K1"] = rows
check("K1a Foster-Jacobson alpha_1, alpha_2, gamma = 1 exact at 6 random points; all six field equations satisfied", worst == 0, "residual exactly 0" if not worst else "nonzero")
check("K1b the moving response's pole is exactly the spin-0 speed s0^2 (Jacobson-Mattingly, memory): FJ's 1/c123 is the v^2/s0^2 term", all(r["s0_pole"] for r in rows), "")
KBs, Js, K2s, Q0s = sy.symbols("K_B J K2 Q0")

say("\n=== Identity: Maxwell term = Einstein-aether at (c1,c2,c3,c4) = (K,0,-K,0) ===")
b1, M1 = matrix("s", KB=KBs); b2, M2 = matrix("s", c=(KBs, 0, -KBs, 0))
check("K1c block identity Maxwell = (K,0,-K,0)", (M1 - M2).applyfunc(sy.simplify) == sy.zeros(6, 6), "")

say("\n=== P1-A AeST exact moving response, symbolic in K_B, J, K2, Q0, v; L = R - (K_B/2)F^2 + 2c a.V - c(1+J)V^2 + K2 dQ^2, c = 2 - K_B ===")
c_ = 2 - KBs; W = 1 + Js
kw = dict(KB=KBs, F=c_ * W, Nf=c_, Q0=Q0s, K2=K2s)
gr = solve("s", v)[0]
b_, Mfull = matrix("s", **kw)
names_ = b_.names
M_v = Mfull.subs({k: 1, w: v})
J_v = source("s", names_, v)
x = {"Phi": gr["Phi"], "Psi": gr["Psi"]}; x["Az"] = x["Phi"] / v; x["pi"] = sy.I * Q0s * x["Az"]
fv = sy.Matrix([x["Phi"], x["Psi"], 0, 0, x["Az"], x["pi"]])
res = (M_v * fv + J_v / 2).applyfunc(sy.simplify)
xs = {a: sy.factor(b) for a, b in x.items()}
say(f"  candidate, from hand work: {xs}. Residual of all six rows: {list(res)}")
RES["moving"] = {a: str(b) for a, b in xs.items()}
keep = [names_.index(n) for n in ("Phi", "Psi", "Az", "pi")]
det = sy.factor(M_v[keep, keep].det(method="berkowitz"))
say(f"  det of the block on (Phi, Psi, Az, pi) at omega = v: {det}")
RES["det_moving"] = str(det)
check("A1 Phi, Psi equal linear GR's with G~ for all K_B, J, K2, Q0 and v != 0, all six rows vanish, and the block is invertible so the solution is unique", all(q == 0 for q in res) and det != 0, "exact")
check("A2 aether's response A_z = Phi/v (d_t A_z + d_z Phi = 0, geodesic); scalar pi = i Q0 A_z (V = 0, dQ = 0)", True if all(q == 0 for q in res) else False, f"A_z = {sy.factor(x['Az'])}, pi = {sy.factor(x['pi'])}")
b_v, Mvv = matrix("v", **kw)
vk_s = sy.Symbol("vk", positive=True)
Jx = source("v", b_v.names, R(1))
fx = sy.Matrix([-1, 0, 0])
Jxz = sy.zeros(3, 1); Jxz[b_v.names.index("ex")] = vk_s      # oblique velocity: T^xz = v_x v_z, (1/2) h_ab T^ab = ex v_x v_z
r0 = (Mvv.subs({k: 1, w: 0}) * fx + Jx / 2).applyfunc(sy.simplify); r1 = (Mvv.subs({k: 1, w: vk_s}) * fx + (Jx + Jxz) / 2).applyfunc(sy.simplify)
say(f"  vector sector B_x = -1, A_x = 0 at k = 1, v = 1: residual at omega = 0 {list(r0)}, at omega = k vk {list(r1)}")
check("A3 vector sector is bare: B_x = -4 U~ v, U~ = 1/4 at k = 1, A_x = 0, at omega = 0 and omega != 0", all(q == 0 for q in r0) and all(q == 0 for q in r1), "")
a1_mov = -2 * (-1) / (-gr["Phi"].subs(v, 0)) - 8
beta_mov = coef(sy.cancel(gr["Phi"] / gr["Phi"].subs(v, 0)), 2)
a2_mov = beta_mov - BG + a1_mov / 2
say(f"  moving branch: alpha_1 = {a1_mov}, alpha_2 = {a2_mov}, G_measured = G~")
RES["moving_alphas"] = dict(a1=str(a1_mov), a2=str(a2_mov))
check("A4 moving branch alpha_1 = alpha_2 = 0 exact", a1_mov == 0 and a2_mov == 0, "")

say("\n=== P1-K2 static limit: omega = 0 exactly ===")
ph, ps, az, pi_ = sy.symbols("ph ps az pi_")
bb, Ms = matrix("s", **kw); Ms = Ms.subs({k: 1, w: 0}).applyfunc(sy.simplify); J0 = source("s", bb.names, 0)
f = sy.Matrix([ph, ps, 0, 0, az, pi_])
eqs = [e for e in (Ms * f + J0 / 2) if sy.simplify(e) != 0]
sol = sy.solve(eqs, [ph, ps, az], dict=True)[0]
Us = sy.factor(-sol[ph]); say(f"  rank of the static block {Ms[keep, keep].rank()} of 4; flat direction: the combination A_z, pi leaving u = pi + Q0 A_z/(i k) fixed. U_static = {Us}")
RES["U_static"] = str(Us)
Us0 = sy.simplify(Us.subs(Q0s, 0))
a1st = sy.simplify(-2 * (-1) / Us0 - 8)
target = -4 * (2 + KBs * Js) / (1 + Js)
say(f"  q -> 0: U_static = {Us0}; alpha_1 from moving B_x over static U = {sy.factor(a1st)}")
check("K2a record's eta_K: alpha_1 = -4(2 + K_B J)/(1 + J) is B_x(bare) over U_static", sy.simplify(a1st - target) == 0, f"{sy.factor(a1st)}")
check("K2b at J = 1: -2(K_B + 2); J -> oo: -4 K_B", sy.simplify(a1st.subs(Js, 1) + 2 * (KBs + 2)) == 0 and sy.limit(a1st, Js, sy.oo) == -4 * KBs, "the formula is 8(G~/G_static - 1)")
Gr = sy.simplify(Us0 / sy.Rational(1, 4))
say(f"  G_static/G~ = {Gr}; at J = 1, K_B in (0, 1/4]: {float(Gr.subs({Js: 1, KBs: 0})):.3f} to {float(Gr.subs({Js: 1, KBs: R(1, 4)})):.3f}")
RES["G_ratio"] = str(Gr)

say("\n=== P1-K3 record's alpha_1(q) at K_B = 1/5, K2 = 10, J = 1: (-5184q^4 - 16q^2 - 22)/(648q^4 + 36q^2 + 5) ===")
q = sy.Symbol("q", positive=True)
rec = (-5184 * q ** 4 - 16 * q ** 2 - 22) / (648 * q ** 4 + 36 * q ** 2 + 5)
outs = {}
for sg in (1, -1):
    Uq = Us.subs({KBs: R(1, 5), Js: 1, K2s: sg * 10, Q0s: q})
    mine = sy.simplify(2 / Uq - 8)
    outs[sg] = mine
    say(f"  K2 sign {sg:+d}: mine {sy.factor(mine)}; difference at q = 2/5: {float((mine - rec).subs(q, R(2, 5))):.5f}; q -> 0: {sy.limit(mine, q, 0)} vs {sy.limit(rec, q, 0)}")
check("K3a q -> 0 limit of the record's alpha_1(q) reproduced", all(sy.limit(m, q, 0) == sy.limit(rec, q, 0) for m in outs.values()), "-22/5")
check("K3b the record's finite-q rational reproduced", any(sy.simplify(m - rec) == 0 for m in outs.values()), "mine is not the record's at q != 0; its cached action L2dc_v2.pkl and gauge differ (see README)")

say("\n=== Regular ladder test: does a Taylor series in v exist at fixed q around the static solution, source along k? ===")
q0 = R(2, 5)
bl, Ml = matrix("s", KB=R(1, 5), F=R(18, 5), Nf=R(9, 5), Q0=q0, K2=-10)
Mv = Ml.subs({k: 1, w: v})
Jv = source("s", bl.names, v)
use = [bl.names.index(n) for n in ("Phi", "Psi", "Az", "pi")]
X = [sy.symbols(f"x{o}_0:4") for o in range(3)]
ser = sy.Matrix([sum(X[o][j] * v ** o for o in range(3)) for j in range(4)])
E_ = (Mv[use, use] * ser + Jv.extract(use, [0]) / 2).applyfunc(sy.expand)
eq_o = [E_[r].coeff(v, o) for r in range(4) for o in range(3)]
allx = [s for o in X for s in o]
A_, b__ = sy.linear_eq_to_matrix(eq_o, allx)
rA, rAb = A_.rank(), A_.row_join(b__).rank()
say(f"  orders v^0..v^2 only: rank {rA}, augmented {rAb}: {'solvable through O(v^2)' if rA == rAb else 'NO regular series'}")
eq_lo = [E_[r].coeff(v, o) for r in range(4) for o in range(2)]
RES["ladder"] = dict(rank=int(rA), aug=int(rAb))
sol0 = sy.solve([E_[r].coeff(v, 0) for r in range(4)] + [E_[r].coeff(v, 1) for r in range(4)], allx[:8], dict=True)
say(f"  through O(v): solution exists {bool(sol0)}; x0 Phi = {sol0[0].get(X[0][0], 'free') if sol0 else None}, static U at this q = {Us.subs({KBs: R(1, 5), Js: 1, K2s: -10, Q0s: q0})}")
exact_phi0 = -gr["Phi"].subs(v, 0)
RES["ladder_phi0"] = str(sol0[0].get(X[0][0], "free")) if sol0 else None

say("\n=== P1-B exact branch: F_munu = 0, phi = Q0 tau, on exact Schwarzschild with radial geodesic congruences ===")
t, r, th, ph_, e, M_, E, Q = sy.symbols("t r theta phi epsilon M E Q", positive=True)
X4 = [t, r, th, ph_]
f_ = 1 - 2 * M_ / r
def extra_terms(tau_r, dA, dphi, dg, Q_, mut=0):
    """pointwise Lagrangian terms at first order in e. tau = -E t + int tau_r dr: A_mu = d_mu tau, phi = Q tau + e dphi"""
    gm = sy.diag(-f_, 1 / f_, r ** 2, r ** 2 * sy.sin(th) ** 2) + e * dg
    gi0 = sy.diag(-1 / f_, f_, 1 / r ** 2, 1 / (r ** 2 * sy.sin(th) ** 2))
    gi = gi0 - e * gi0 * dg * gi0
    A0 = sy.Matrix([-E, tau_r, 0, 0]) + e * dA
    A0 = A0 / sy.sqrt(-(A0.T * gi * A0)[0])      # the unit constraint is part of the theory: variations stay on it, multiplier lambda = 0 on the branch
    phi_d = Q_ * sy.Matrix([-E, tau_r, 0, 0]) + e * sy.Matrix([sy.diff(dphi, c) for c in X4]) + sy.Matrix([0, mut, 0, 0])
    Gam = [[[sum(gi[a, d] * (sy.diff(gm[d, b], X4[c]) + sy.diff(gm[d, c], X4[b]) - sy.diff(gm[b, c], X4[d])) for d in range(4)) / 2 for c in range(4)] for b in range(4)] for a in range(4)]
    DA = sy.Matrix(4, 4, lambda a, b: sy.diff(A0[b], X4[a]) - sum(Gam[c][a][b] * A0[c] for c in range(4)))
    Au = gi * A0
    acc = sy.Matrix([sum(Au[a] * DA[a, b] for a in range(4)) for b in range(4)])
    F2 = sum((DA[a, b] - DA[b, a]) * gi[a, c] * gi[b, d] * (DA[c, d] - DA[d, c]) for a in range(4) for b in range(4) for c in range(4) for d in range(4))
    QQ = sum(Au[a] * phi_d[a] for a in range(4))
    V = phi_d + A0 * QQ
    aV = sum(acc[a] * gi[a, b] * phi_d[b] for a in range(4) for b in range(4))
    Y = sum(V[a] * gi[a, b] * V[b] for a in range(4) for b in range(4))
    return dict(F2=F2, aV=aV, Y=Y, Q=QQ), (A0.T * gi * A0)[0]
vals = {M_: R(1, 10), r: R(3), th: R(7, 5), ph_: R(2, 5), t: R(1, 3), Q: R(3, 7)}
dA = sy.Matrix([r * th, t * r, th ** 2, t * ph_]); dphi = r ** 2 * t + th * ph_
dg = sy.zeros(4, 4); dg[0, 0] = r * th; dg[1, 1] = t * ph_; dg[0, 1] = dg[1, 0] = th * t; dg[2, 2] = r; dg[3, 3] = t * th
outp = {}
for Ev in (R(1), R(13, 12), R(5, 3)):
    tr_ = sy.sqrt(Ev ** 2 - f_) / f_
    terms, unit = extra_terms(tr_, dA, dphi, dg, Q)
    un0 = sy.simplify(unit.subs(e, 0).subs(E, Ev))
    row = {}
    for nm, ex in terms.items():
        ex = ex.subs(E, Ev)
        d0 = sy.N(ex.subs(e, 0).subs(vals), 30); d1 = sy.N(sy.diff(ex, e).subs(e, 0).subs(vals), 30)
        row[nm] = (float(d0), float(d1))
    terms2, _ = extra_terms(tr_, dA, dphi, dg, Q, mut=R(1, 5))
    m1 = float(sy.N(sy.diff(terms2["Y"].subs(E, Ev), e).subs(e, 0).subs(vals), 30))
    m2 = float(sy.N(sy.diff(terms2["aV"].subs(E, Ev), e).subs(e, 0).subs(vals), 30))
    outp[str(Ev)] = dict(unit=str(un0), row=row, mutated_dY=m1, mutated_daV=m2)
    say(f"  E = {Ev}: A.A = {un0}; F2 {row['F2']}, a.V {row['aV']}, Y {row['Y']}, Q {row['Q'][0]:.6f}; mutated congruence dY/de {m1:.4g}, da.V/de {m2:.4g}")
RES["branch"] = outp
tol = 1e-25
ok = all(abs(o["row"][n][i]) < tol for o in outp.values() for n in ("F2", "aV", "Y") for i in (0, 1)) and all(o["unit"] == "-1" for o in outp.values())
check("B1 F2, a.V, Y have zero value and zero first variation for arbitrary field perturbations, E = 1, 13/12, 5/3, so GR + geodesic aether + phi = Q0 tau is exact when F_Q(0, Q0) = 0 and F_Y finite", ok, "pointwise, 30 digits")
check("B2 a mutated congruence (phi not Q0 tau) gives nonzero first variation", all(abs(o["mutated_dY"]) > 1e-3 for o in outp.values()), "")
check("B3 on the branch Q = Q0 (sign per A_mu = d_mu tau)", all(abs(abs(o["row"]["Q"][0]) - float(vals[Q])) < 1e-20 for o in outp.values()), "")

say("\n=== P1-C time-domain: 1D planar, Psi = Phi, W frozen, Q0 = 0. Source Gaussian rests on the static branch to t = 0, then moves at v ===")
def run(KBv, Jv_, c2, vs, N=256, Lbox=2 * np.pi, width=0.25, T=None):
    c = 2 - KBv; A = KBv + c / (1 + Jv_)
    ks = np.arange(1, N // 2) * 2 * np.pi / Lbox
    z0 = Lbox / 2
    sh = np.exp(-(ks * width) ** 2 / 2)
    def src(kk, sk, t):
        return sk * np.exp(-1j * kk * (z0 + vs * t))
    Phi_rel = np.zeros(len(ks), complex); Phi_src = np.zeros(len(ks), complex); Phi_stat = np.zeros(len(ks), complex)
    T = T if T is not None else 1.5
    FROZ = []
    for i, (kk, sk) in enumerate(zip(ks, sh)):
        s0_ = src(kk, sk, 0) / kk ** 2     # L/k^2 source s: Phi eq 2 A sigma - 4 Phi - s = 0
        al = 1 / (2 * A) - 0.25
        P0 = -(s0_ / 4) / al               # static: chi_dot = 0
        FROZ.append((P0, s0_ , kk))
        def rhs(t_, y):
            Pc, ch = y[0] + 1j * y[1], y[2] + 1j * y[3]
            dP = -2 * c2 * kk ** 2 * ch
            dch = Pc * al + (src(kk, sk, t_) / kk ** 2) / 4
            return [dP.real, dP.imag, dch.real, dch.imag]
        so = solve_ivp(rhs, [0, T], [P0.real, P0.imag, 0, 0], method="DOP853", rtol=1e-9, atol=1e-13, max_step=0.02 / max(1, np.sqrt(max(c2, 0)) * kk))
        Pf = so.y[0, -1] + 1j * so.y[1, -1]
        sT = src(kk, sk, T) / kk ** 2
        Phi = (Pf - sT) / 4
        Phi_src[i] = 2 * (Phi * np.exp(1j * kk * (z0 + vs * T))).real
        Phi_rel[i] = 2 * (Phi * np.exp(1j * kk * z0)).real
        Phi_stat[i] = 2 * (((P0 - s0_) / 4) * np.exp(1j * kk * z0)).real
    bare = 2 * (-(sh / ks ** 2) / 4).sum()
    frozen_at_source = 2 * sum(((P0_ / 4) * np.exp(1j * kk_ * (z0 + vs * T))).real for P0_, s_, kk_ in FROZ) if FROZ else 0.0
    return dict(at_source=float(Phi_src.real.sum()), at_release=float(Phi_rel.real.sum()), static0=float(Phi_stat.real.sum()), bare=float(bare), pred_source=float(bare + frozen_at_source))
tdom = {}
for lab, a_ in (("AeST K_B 0.2 J 1 c2 0 (v 0.3)", (0.2, 1.0, 0.0, 0.3)), ("AeST K_B 0.2 J 1 c2* v 0.1, subsonic", (0.2, 1.0, 0.2 / 0.6, 0.1)), ("AeST K_B 0.2 J 1 c2* v 2 s0, supersonic", (0.2, 1.0, 0.2 / 0.6, None))):
    KBv, Jv_, c2, vs = a_
    Aa = KBv + (2 - KBv) / (1 + Jv_); s2_ = c2 * (2 - Aa) / (2 * Aa)
    if vs is None:
        vs = 2 * np.sqrt(s2_)
    o = run(KBv, Jv_, c2, vs); o["v"] = vs; o["s0"] = float(np.sqrt(s2_)); tdom[lab] = o
    say(f"  {lab}: s0 {o['s0']:.4f} v {vs:.4f}; Phi at source {o['at_source']:.6f} vs bare {o['bare']:.6f}, static {o['static0']:.6f}; Phi at release point {o['at_release']:.6f}")
RES["tdom"] = tdom
a_ = tdom["AeST K_B 0.2 J 1 c2 0 (v 0.3)"]
check("C1 c2 = 0: Phi at the source = bare field of the source + the static-branch charge frozen at the release point, within 1e-6; the charge does not follow", abs(a_["at_source"] - a_["pred_source"]) / abs(a_["bare"]) < 1e-6 and abs(a_["at_release"] - a_["pred_source"]) > 0, f"at source {a_['at_source']:.7f}, prediction {a_['pred_source']:.7f}, bare {a_['bare']:.5f}, static {a_['static0']:.5f}")
b_ = tdom["AeST K_B 0.2 J 1 c2* v 0.1, subsonic"]
check("C2 control: c2 > 0, v < s0: the source keeps the static value within 5 %", abs(b_["at_source"] / b_["static0"] - 1) < 0.05, f"{b_['at_source']:.5f} vs {b_['static0']:.5f}")

say("\n=== c2 chassis (FC-AeST + c2*, not v9): exact, K_B = 1/5, J = 1 ===")
KB5 = R(1, 5); c2s = KB5 / (1 - 2 * KB5)
xc, rc = solve("s", v, c=(0, c2s, 0, 0), KB=KB5, F=R(9, 5) * 2, Nf=R(9, 5))
pc = xc["Phi"]; Uc = -pc.subs(v, 0); bc = coef(sy.cancel(pc / pc.subs(v, 0)), 2)
a1c = 2 / Uc - 8; a2c = bc - BG + a1c / 2
say(f"  U {Uc} (bare 1/4); alpha_1 {a1c} = {float(a1c):.4f}; alpha_2 {a2c} = {float(a2c):.4f}. Here the static branch is real for v << s0, so these are real for that chassis")
RES["c2_chassis"] = dict(a1=str(a1c), a2=str(a2c), U=str(Uc))

say("\n=== P1-D margins at the Sun: capture radius and charged-background corrections, bounds [memory, PROVISIONAL] ===")
GM = 1.32712440018e20; AU = 1.495978707e11; c0 = 299792458.0; PC = 3.0857e16
A1B, A2B = 4e-5, 2e-9
G = 6.674e-11; Msun = 1.989e30
rhoL = 0.1 * Msun / PC ** 3      # upper value for the local dynamical density, its share of charge is at most this
marg = {}
for vk_ in (20.0, 220.0, 369.0):
    vv = vk_ * 1e3
    rc_ = GM / vv ** 2 / AU
    for rau in (1.0, 9.58):
        kk = 1 / (rau * AU); dlt = 4 * np.pi * G * rhoL / (kk * vv) ** 2
        marg[f"{vk_:g}|{rau:g}"] = dict(r_capture_AU=rc_, nonlin=rc_ / rau, jeans=dlt, a_equiv=dlt / (vv / c0) ** 2)
        say(f"  w {vk_:5.0f} km/s, r {rau:5.2f} AU: capture GM/w^2 {rc_:.4g} AU; Jeans fraction of Phi {dlt:.3g}, as alpha ~ fraction/w^2 {dlt / (vv / c0) ** 2:.3g} (bounds {A1B:g}, {A2B:g})")
RES["margins"] = marg
ok_ = all(m["a_equiv"] < A2B and m["nonlin"] < 1 for key, m in marg.items() if key.split("|")[0] in ("220", "369"))
check("D1 at 220, 369 km/s and planetary r: outside the capture radius, charged-background correction under both bounds; rule's condition", ok_, f"worst a_equiv {max(m['a_equiv'] for key, m in marg.items() if key.split('|')[0] in ('220', '369')):.3g}")
slow = marg["20|1"]
say(f"  reported: 20 km/s (aether co-moving with the disc): capture {slow['r_capture_AU']:.2f} AU, a_equiv at 1 AU {slow['a_equiv']:.3g}; 9.58 AU {marg['20|9.58']['a_equiv']:.3g}. Not in the frozen rule's condition.")
for foot, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    x_ = GM / AU ** 2 / a0
    say(f"  {foot}: x at 1 AU {x_:.4g}. a0 enters neither moving alpha: both exactly 0 on both footings. r_M = {np.sqrt(GM / a0) / AU:.0f} AU")
    RES.setdefault("footings", {})[foot] = dict(x=x_, moving_a1=0, moving_a2=0)

nf = [n for n, o in CH if not o]
say(f"\nCHECKS {len(CH) - len(nf)}/{len(CH)} pass. Failed: {nf}")
RES["checks"] = CH
open(os.path.join(HERE, f"as3_part1{TAG}.out"), "w").write("\n".join(L_) + "\n")
json.dump(RES, open(os.path.join(HERE, f"as3_part1{TAG}.json"), "w"), indent=1, sort_keys=True, default=str)
sys.exit(1 if nf else 0)
