#!/usr/bin/env python3
"""UX1_action_class gates. Run: OMP_NUM_THREADS=1 nice -n 15 python3 -W ignore ux1_gates.py ; twin: UX1_MUTATE=1 (same command).
Outputs ux1_gates{,_MUTATE}.out and .json, no timing, so a rerun is byte-identical. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
import numpy as np, sympy as sy
from scipy.integrate import solve_ivp
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import ux1_q2 as U
MUT = os.environ.get("UX1_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
L, CHECKS, RES = [], [], {"lane": "UX1_action_class", "mutate": MUT}
def say(s=""):
    L.append(s); print(s, flush=True)
def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok))); say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

g, gN, a0, al, be, h, m = sy.symbols("g g_N a0 alpha beta h m", positive=True)
LAM = al + be

say("=== A. BIMOND static reduction (Milgrom 2009), derived from L = -[b(grad f)^2 + a(grad fh)^2 - a0^2 M(|grad f*|^2/a0^2)]/8piG - rho f - rho_t fh, f* = f - fh")
gs, gh, gst = sy.symbols("gs gh gst")          # spherical fields g, ghat, g* = g - ghat
rho_t = sy.Symbol("gN_t")                      # twin Newtonian field
mm = sy.Symbol("mm")                           # M'
sg = -1 if MUT else 1                          # mutation m1: flips the difference coupling
sol = sy.solve([be * gs - sg * mm * (gs - gh) - gN, al * gh + sg * mm * (gs - gh) - rho_t], [gs, gh], dict=True)[0]
gs_s, gh_s = sy.simplify(sol[gs]), sy.simplify(sol[gh])
gst_s = sy.simplify(gs_s - gh_s)
s_sym = al * be - mm * LAM
# identities: s g* = a gN - b gN_t ; Lam g = gN + gN_t + a g* ; Lam ghat = gN + gN_t - b g*
i1 = sy.simplify(s_sym * gst_s - (al * gN - be * rho_t))
i2 = sy.simplify(LAM * gs_s - (gN + rho_t + al * gst_s))
i3 = sy.simplify(LAM * gh_s - (gN + rho_t - be * gst_s))
check("A1 s g* = a g_N - b g_Nt", i1 == 0, f"residual {i1}")
check("A2 L g = g_N + g_Nt + a g*", i2 == 0, f"residual {i2}")
check("A3 L ghat = g_N + g_Nt - b g*", i3 == 0, f"residual {i3}")
# law reconstruction with L = 1 (no twin): g = gN + a g*, h = a g*, s = a^2 g/a0, so div[S grad psi] = div F_N with S = h/(a0-h)
lawN = g ** 2 / (g + a0)
fac = (1 if not MUT else 2)                    # mutation m3: drops the factor in the reconstruction
hh = g - lawN
s_law = al ** 2 * lawN / hh / fac
r1 = sy.simplify(s_law - al ** 2 * g / a0)
Sh = h / (a0 - h)
r2 = sy.simplify(Sh.subs(h, hh) - s_law / al ** 2)
check("A4 exact law needs s = a^2 g/a0", r1 == 0, f"residual {r1}")
check("A5 alpha cancels: S(h) = h/(a0-h), h = g - g_N", r2 == 0, f"residual {r2}")
check("A6 h -> a0 as g -> oo (tail) and h -> g as g -> 0", sy.limit(hh, g, sy.oo) == a0 and sy.limit(hh / g, g, 0) == 1, "limits")
say(f"  twin force at L = 1: ghat = g_N - (b/a) h for a baryon source; repulsive when (b/a) h > g_N")

say("\n=== B. BIMOND scalar Y on two metrics: lapse velocities (FRW and static)")
t, x_ = sy.symbols("t x")
def metric(N, A):
    return sy.diag(-N ** 2, A ** 2, A ** 2, A ** 2)
def christoffel(G, X):
    Gi = G.inv()
    return [[[sum(Gi[a, d] * (sy.diff(G[d, b], X[c]) + sy.diff(G[d, c], X[b]) - sy.diff(G[b, c], X[d])) for d in range(4)) / 2
              for c in range(4)] for b in range(4)] for a in range(4)]
y_, z_ = sy.symbols("y z")
X = [t, x_, y_, z_]
Nf, Af, Nh, Ah = [sy.Function(n)(t) for n in ("N", "A", "Nh", "Ah")]
Gg, Gh = metric(Nf, Af), metric(Nh, Ah)
C1, C2 = christoffel(Gg, X), christoffel(Gh, X)
C = [[[C1[a][b][c] - C2[a][b][c] for c in range(4)] for b in range(4)] for a in range(4)]
Gi = Gg.inv()
Y = 0
for mu in range(4):
    for nu in range(4):
        if Gi[mu, nu] == 0:
            continue
        Y += Gi[mu, nu] * (sum(C[gm][mu][lm] * C[lm][nu][gm] for gm in range(4) for lm in range(4))
                           - sum(C[gm][mu][nu] * C[lm][lm][gm] for gm in range(4) for lm in range(4)))
Y = sy.simplify(Y)
vN, vA, vNh, vAh, N_, A_, Nh_, Ah_ = sy.symbols("vN vA vNh vAh N A Nh Ah", real=True)
sub = [(sy.diff(Nf, t), vN), (sy.diff(Af, t), vA), (sy.diff(Nh, t), vNh), (sy.diff(Ah, t), vAh), (Nf, N_), (Af, A_), (Nh, Nh_), (Ah, Ah_)]
Yv = sy.simplify(Y.subs(sub))
dY_vN = sy.simplify(sy.diff(Yv, vN))
expected = sy.simplify(-3 * (vAh / Ah_) * (1 / N_ ** 2 - Ah_ ** 2 / (A_ ** 2 * Nh_ ** 2)) * 1 / N_)
say(f"  FRW Y = {sy.factor(Yv)}")
say(f"  dY/d(Ndot) = {sy.factor(dY_vN)}")
check("B1 Ndot enters Y linearly on FRW, nonzero off proportional cones", sy.simplify(sy.diff(dY_vN, vN)) == 0 and dY_vN != 0,
      "so nonlinear M gives Ndot a kinetic term through M''")
check("B2 dY/dNdot vanishes on equal cones", sy.simplify(dY_vN.subs({Nh_: N_ * Ah_ / A_})) == 0, "bracket 1/N^2 - Ah^2/(A^2 Nh^2)")
# static sign of Y
fx, fh = sy.Function("f")(x_), sy.Function("fh")(x_)
eps = sy.Symbol("eps")
Gs1 = sy.diag(-(1 + 2 * eps * fx), 1 - 2 * eps * fx, 1 - 2 * eps * fx, 1 - 2 * eps * fx)
Gs2 = sy.diag(-(1 + 2 * eps * fh), 1 - 2 * eps * fh, 1 - 2 * eps * fh, 1 - 2 * eps * fh)
C1s, C2s = christoffel(Gs1, X), christoffel(Gs2, X)
Cs = [[[C1s[a][b][c] - C2s[a][b][c] for c in range(4)] for b in range(4)] for a in range(4)]
Gsi = Gs1.inv()
Ys = 0
for mu in range(4):
    for nu in range(4):
        if Gsi[mu, nu] == 0:
            continue
        Ys += Gsi[mu, nu] * (sum(Cs[gm][mu][lm] * Cs[lm][nu][gm] for gm in range(4) for lm in range(4))
                             - sum(Cs[gm][mu][nu] * Cs[lm][lm][gm] for gm in range(4) for lm in range(4)))
Ys2 = sy.simplify(sy.series(Ys, eps, 0, 3).removeO().coeff(eps, 2))
fs = sy.Symbol("fstar_x", real=True)
c_static = sy.simplify(Ys2.subs(sy.diff(fh, x_), sy.diff(fx, x_) - fs) / fs ** 2)
say(f"  static weak-field Y = {c_static} |grad f*|^2")
RES["Y_static_coeff"] = str(c_static)
cval = float(c_static)
# minisuperspace Hessian at sample backgrounds, M'' from the law where Y has the static sign
EH = -6 * be * A_ * vA ** 2 / N_ - 6 * al * Ah_ * vAh ** 2 / Nh_
Mp, Mpp, a0s = sy.symbols("Mp Mpp a0s")
w = sy.sqrt(N_ * Nh_ * A_ ** 3 * Ah_ ** 3)
vs = [vA, vAh, vN, vNh]
Ygrad = [sy.diff(Yv, v) for v in vs]
Hmat = sy.Matrix(4, 4, lambda i, j: sy.diff(EH, vs[i], vs[j]) + 2 * w * (Mp * sy.diff(Yv, vs[i], vs[j]) + Mpp / a0s ** 2 * Ygrad[i] * Ygrad[j]))
fHess = sy.lambdify((al, be, N_, A_, Nh_, Ah_, vN, vA, vNh, vAh, Mp, Mpp, a0s), Hmat, "numpy")
fY = sy.lambdify((N_, A_, Nh_, Ah_, vN, vA, vNh, vAh), Yv, "numpy")
rows = []
bg = dict(N=1.0, A=1.0, Nh=1.3, Ah=0.9, vN=0.02, vA=0.5, vNh=-0.03, vAh=0.4)
for name, (mp, mpp) in {"M'>0 M''<0": (0.1, -0.5), "M'>0 M''>0": (0.1, 0.5), "M'<0 M''<0": (-0.1, -0.5), "M'<0 M''>0": (-0.1, 0.5)}.items():
    Hn = np.array(fHess(0.5, 0.5, bg["N"], bg["A"], bg["Nh"], bg["Ah"], bg["vN"], bg["vA"], bg["vNh"], bg["vAh"], mp, mpp, 1.0), float)
    ev = np.linalg.eigvalsh(0.5 * (Hn + Hn.T))
    rows.append((name, [float(f"{v:.5g}") for v in ev]))
    say(f"  Hessian eig (a, ah, N, Nh velocities), {name}: {rows[-1][1]}")
RES["hessian"] = rows
Y0 = float(fY(bg["N"], bg["A"], bg["Nh"], bg["Ah"], bg["vN"], bg["vA"], bg["vNh"], bg["vAh"]))
say(f"  Y at this FRW point = {Y0:.4g}; static side has sign of {cval:+g}")
RES["Y_FRW_sample"] = Y0
# rank without M'': lapses stay constraints
Hlin = Hmat.subs({Mpp: 0})
fHl = sy.lambdify((al, be, N_, A_, Nh_, Ah_, vN, vA, vNh, vAh, Mp, a0s), Hlin, "numpy")
Hn0 = np.array(fHl(0.5, 0.5, 1.0, 1.0, 1.3, 0.9, 0.02, 0.5, -0.03, 0.4, 0.1, 1.0), float)
rank0 = int(np.linalg.matrix_rank(Hn0, tol=1e-9))
Hn1 = np.array(fHess(0.5, 0.5, 1.0, 1.0, 1.3, 0.9, 0.02, 0.5, -0.03, 0.4, 0.1, -0.5, 1.0), float)
rank1 = int(np.linalg.matrix_rank(Hn1, tol=1e-9))
say(f"  velocity Hessian rank: M'' = 0 -> {rank0}, M'' != 0 -> {rank1}")
RES["rank_linear"], RES["rank_nonlinear"] = rank0, rank1
Hn2 = np.array(fHl(0.5, 0.5, 1.0, 1.0, 1.3, 0.9, 0.02, 0.5, -0.03, 0.4, 0.0, 1.0), float)
rank2 = int(np.linalg.matrix_rank(Hn2, tol=1e-9))
say(f"  no interaction -> rank {rank2}. RUN1's check compared M'' = 0 with M'' != 0, found 3 -> 3 and failed: the cross term Ndot x Ahdot already acts at M' != 0")
RES["rank_noint"] = rank2
check("B3 the interaction raises the velocity rank over two Einstein actions (lapse constraint lost)", rank1 > rank2, f"{rank2} -> {rank1}")
# law's own M on backgrounds with the static sign of Y. M' = (s - ab)/2, M'' = (1/4) dm/d(x^2), m = ab - s, h = a x (a0 = 1), s = a^2 h/(1-h)
def MpMpp(alpha, x):
    hv = alpha * x
    sv = alpha ** 2 * hv / (1 - hv)
    dsdh = alpha ** 2 / (1 - hv) ** 2
    dm_dx2 = -dsdh * alpha / (2 * x)
    return (sv - alpha * (1 - alpha)) / 2, dm_dx2 / 4
rng = np.random.default_rng(20261102)
cnt = {}
minneg = 9
nsamp = 0
for _ in range(4000):
    alpha = rng.choice([0.16, 0.5, 0.84])
    N0, A0, Nh0, Ah0 = np.exp(rng.normal(0, 0.5, 4))
    v = rng.normal(0, 1, 4)
    Yb = float(fY(N0, A0, Nh0, Ah0, v[0], v[1], v[2], v[3]))
    if Yb >= 0:
        continue
    fracc = rng.uniform(0.02, 0.98)                 # h/a0, sets a0 through Y = -2 x^2 a0^2
    x = fracc / alpha
    a0v = math.sqrt(-Yb / 2) / x
    mp_, mpp_ = MpMpp(alpha, x)
    Hb = np.array(fHess(alpha, 1 - alpha, N0, A0, Nh0, Ah0, v[0], v[1], v[2], v[3], mp_, mpp_, a0v), float)
    ev = np.linalg.eigvalsh(0.5 * (Hb + Hb.T))
    tol = 1e-9 * np.max(np.abs(ev))
    neg, pos = int(np.sum(ev < -tol)), int(np.sum(ev > tol))
    cnt[f"neg{neg}_pos{pos}"] = cnt.get(f"neg{neg}_pos{pos}", 0) + 1
    minneg = min(minneg, neg)
    nsamp += 1
say(f"  law's M on {nsamp} random homogeneous backgrounds with Y < 0, alpha in (0.16, 0.5, 0.84): velocity-Hessian signature counts {dict(sorted(cnt.items()))}")
RES["sig_counts"], RES["sig_min_neg"] = cnt, minneg
check("B4 at least two negative directions on every sample, so one constraint leaves at least one negative mode", minneg >= 2, f"min negative {minneg}")

say("\n=== C. K1 Q2: known answer, then the BIMOND equation")
GM = 1.32712440018e20; AU = 1.495978707e11; RSAT = 9.5826 * AU
H_LO, H_HI = -3.0e-27, 9.0e-27
GNE = 6.913e-11
GEK = {"E1": 1.9 * 9.36e-11, "E2": 2.2 * 9.36e-11, "E3": 2.6 * 9.36e-11}
E2 = json.load(open(os.path.join(REPO, "doors_push_2026_10_22/E2_field_equation/e2_field_equation_results.json")))
def yof(e, a):
    if e == "E0":
        return GNE / a
    x = GEK[e] / a
    return x ** 2 / (1 + x)
worst = 0
for foot, a_e2, key in (("canonical", 9.36e-11, "canonical|none"), ("alt", 1.13e-10, "alt|none")):
    for e in ("E0", "E1", "E2", "E3"):
        s = U.Solver("aqual", yof(e, a_e2), r_in=1e-4, r_out=1e4, per_dec=60, Nt=96).solve()
        q = s.q0() * a_e2 ** 1.5 / math.sqrt(GM)
        ref = E2["R1"][key]["cells"][e]["Q2_AQUAL"]
        worst = max(worst, abs(q / ref - 1))
        say(f"  AQUAL {foot} {e}: {q:.4e} vs E2 {ref:.4e}, ratio {q / ref:.4f}, converged {s.converged}")
check("C1 known answer: AQUAL Q2 within 2 % of E2, all eight cells", worst <= 0.02, f"worst {worst:.4f}")
RES["knownanswer_worst"] = worst

def fl(rg, ell=2):
    def rhs(ln, Y_):
        r = np.exp(ln); H = 1 / r ** 2
        Wpp = 1 / U.dk_("bimond", H); S = H / U.k_("bimond", H)
        return [r * Y_[1] / (r ** 2 * Wpp), r * S * ell * (ell + 1) * Y_[0]]
    r0 = rg[0]
    W0 = 1 / U.dk_("bimond", 1 / r0 ** 2)
    so = solve_ivp(rhs, [np.log(r0), np.log(rg[-1])], [r0 ** 3, r0 ** 2 * W0 * 3 * r0 ** 2], t_eval=np.log(rg), rtol=1e-10, atol=1e-30)
    return so.y[0]
rr = np.geomspace(1e-5, 10, 400); ff = fl(rr)
sl = np.gradient(np.log(ff), np.log(rr))
say(f"  regular l=2 branch near the Sun: dln c2/dln r = {sl[np.searchsorted(rr, 1e-3)]:.4f} at 1e-3 r_M, {sl[np.searchsorted(rr, 0.1)]:.4f} at 0.1; so q ~ r, not constant")
check("C2 regular branch is r^3", abs(sl[np.searchsorted(rr, 1e-3)] - 3) < 1e-3, "ODE about the spherical solution")
RMATCH = 0.1
Q = {}
for foot, a in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    unit = a ** 1.5 / math.sqrt(GM)
    rs = RSAT / math.sqrt(GM / a)
    for e in ("E0", "E1", "E2", "E3"):
        b = U.Solver("bimond", yof(e, a), r_in=0.01, r_out=1e3, per_dec=60, Nt=96).solve(maxit=800)
        rb, qq = b.q_of_r()
        cm = -np.interp(RMATCH, rb, qq) * RMATCH ** 2 / 3
        fm, fs = np.interp(np.log(RMATCH), np.log(rr), ff), np.exp(np.interp(np.log(rs), np.log(rr), np.log(ff)))
        cs = cm * fs / fm
        qs = -3 * cs / rs ** 2 * unit
        qpeak = float(np.max(np.abs(qq[rb > 0.03]))) * unit
        Q[f"{foot}|{e}"] = dict(y_e=yof(e, a), r_Saturn=rs, c2_at_0p1=float(cm), Q2_Saturn=float(qs), over_Hees=float(abs(qs) / H_HI), max_abs_q_r_gt_0p03=qpeak, converged=b.converged, last_step=b.step)
        say(f"  K1 {foot} {e}: y_e {yof(e, a):.3f}, c2(0.1 r_M) {cm:.4e}, Q2 at Saturn {qs:.3e} s^-2, |Q2|/Hees line {abs(qs) / H_HI:.4f}, converged {b.converged}, last step {b.step:.1e}")
RES["K1_Q2"] = Q
check("C2b all eight K1 cells met the step test", all(v["converged"] for v in Q.values()), str([k for k, v in Q.items() if not v["converged"]]))
b2 = U.Solver("bimond", yof("E0", 9.3603e-11), r_in=0.03, r_out=1e3, per_dec=80, Nt=128).solve()
rb2, q2 = b2.q_of_r()
cm2 = -np.interp(RMATCH, rb2, q2) * RMATCH ** 2 / 3
ratio = cm2 / Q["canonical|E0"]["c2_at_0p1"]
check("C3 resolution and inner boundary: c2(0.1) stable within 5 %", abs(ratio - 1) < 0.05, f"ratio {ratio:.4f} (80/128, r_in 0.03 vs 60/96, r_in 0.01)")
RES["K1_res_ratio"] = float(ratio)
RES["K1_all_pass_Hees"] = all(v["over_Hees"] <= 1 for v in Q.values())
say(f"  K1 Q2 passes the Hees line in all cells: {RES['K1_all_pass_Hees']}")

say("\n=== D. Exact law's tail and T-B")
xx99 = {"canonical": 22.4, "alt": 18.6}
xv = sy.Symbol("x", positive=True)
for f_, x99 in xx99.items():
    say(f"  {f_}: h(x99)/a0 = {x99 / (1 + x99):.4f}  (M1: anomaly floor 8.96e-11 canonical, 1.07e-10 alt m/s^2; planets 1.0e4-7.7e4 x bounds)")
dh = sy.diff(xv - xv ** 2 / (1 + xv), xv)
check("D1 law's h is monotone in g", sy.simplify(dh - 1 / (1 + xv) ** 2) == 0, f"dh/dx = {sy.simplify(dh)}")
# T-B: h'(g_N) = 1/W''(h) > 0 for any convex W, h' S-form; the bimond dual shows it
HH = np.geomspace(1e-6, 1e8, 2000)
kv = U.k_("bimond", HH)
check("D2 T-B numeric: k(H) rises through the whole range, K1 form", bool(np.all(np.diff(kv) > 0)), f"k from {kv[0]:.3e} to {1 - kv[-1]:.3e} below cap")

say("\n=== E. T-A: spectral kernel")
ks = sy.Symbol("K", positive=True); mu2 = sy.Symbol("mu2", positive=True); w1 = sy.Symbol("w", positive=True)
D = 1 / ks + w1 / (ks + mu2)
dd = sy.simplify(sy.diff(ks * D, ks))
target = w1 * mu2 / (ks + mu2) ** 2
check("E1 d(K D)/dK = sum w mu^2/(K+mu^2)^2 >= 0", sy.simplify(dd - target) == 0, f"{dd}")
wv = -0.5 if MUT else 0.5                      # mutation m2: non-Stieltjes kernel under a positive-weight claim
KK = np.geomspace(1e-3, 1e3, 200)
kD = KK * (1 / KK + wv / (KK + 1.0))
check("E2 sample kernel obeys monotone KD under the positive-weight claim", bool(np.all(np.diff(kD) >= 0)), f"w {wv}")
# screening kernel 1/(K + eps K^2): residues
e1 = sy.Symbol("e1", positive=True)
Dscr = 1 / (ks + e1 * ks ** 2)
pf = sy.apart(Dscr, ks)
say(f"  stiffness kernel 1/(K + e K^2) = {pf}; second pole has negative residue, Ostrogradsky (M1 R2b4, I1)")

say("\n=== F. T-C: k^4 dispersion on tilted slices (extends I1)")
def nonreal(A, v, kp):
    gam = 1 / math.sqrt(1 - v * v)
    # gam^2 (w + v k)^2 = A gam^4 (k + v w)^4, polynomial in w
    W = np.polynomial.polynomial.Polynomial([kp, v])
    P = np.polynomial.polynomial.Polynomial([v * kp, 1.0]) ** 2 * gam ** 2 - A * gam ** 4 * W ** 4
    return int(np.sum(np.abs(np.imag(P.roots())) > 1e-9 * np.abs(P.roots())))
A_ = 1e-4; v_ = 1e-2
kc = 1 / (2 * math.sqrt(A_) * v_)
nr = [(f, nonreal(A_, v_, f * kc)) for f in (0.5, 0.9, 1.5, 3, 10)]
say(f"  A {A_}, tilt {v_}, kappa_c {kc:.1f}; nonreal roots at k/kappa_c: {nr}")
nr0 = [(f, nonreal(A_, 0.0, f * kc)) for f in (0.5, 3, 10)]
check("F1 no nonreal roots on the rest slice; nonreal roots above kappa_c on a tilted slice", all(n == 0 for _, n in nr0 if True) and nr[0][1] == 0 and nr[-1][1] > 0, f"rest {nr0}")

say("\n=== G. K3: galileon scaling cannot give the deep law")
r_, M_, n_ = sy.symbols("r M n", positive=True)
p = 1 / (n_ - 1)
ex_r = 1 - 3 * p                                # phi' ~ r (M/r^3)^(1/(n-1))
sol_n = sy.solve(p - sy.Rational(1, 2), n_)
check("G1 M^(1/2) needs n = 3, then r exponent is -1/2, not -1", sol_n == [3] and ex_r.subs(n_, 3) == -sy.Rational(1, 2), f"n {sol_n}, exponent {ex_r.subs(n_, 3)}")
check("G2 no n gives M^(1/2)/r", sy.solve([p - sy.Rational(1, 2), ex_r + 1], n_, dict=True) == [], "over-determined")

say("\n=== H. K5: a second field completing gamma_L")
Z, c2s, en, gam, K2, W2 = sy.symbols("Z c2s en gam K2 W2", positive=True)
# healthy sigma: L = pi kinetic + sigma kinetic - sigma^2/(2 gam) - sigma k^2 pi-mixing; static stiffness of pi after eliminating sigma
stiff_healthy = Z * c2s * K2 - K2 ** 2 / (en * K2 + 1 / gam)
stiff_wrong = Z * c2s * K2 + K2 ** 2 / (en * K2 + 1 / gam)
check("H1 positive-norm sigma reduces the stiffness at every k", sy.simplify(stiff_healthy - Z * c2s * K2 + K2 ** 2 / (en * K2 + 1 / gam)) == 0, "- k^4/(e k^2 + 1/gam)")
check("H2 the gamma_L sign (+ gam k^4 at small k) is the negative-norm sigma", sy.limit(stiff_wrong - Z * c2s * K2, en, 0) == gam * K2 ** 2, "needs sigma^2 with the wrong sign")

say("\n=== I. K6: mimetic f(box phi) on Minkowski, unitary gauge N = 1")
zd, B, gr2, gm = sy.symbols("zd B gr2 gamma_f", real=True)
Lm = -3 * zd ** 2 + gr2 + 2 * zd * B + gm / 2 * (3 * zd - B) ** 2
Bs = sy.solve(sy.diff(Lm, B), B)[0]
Lr = sy.simplify(Lm.subs(B, Bs))
A_k = sy.simplify(sy.diff(Lr, zd, 2) / 2)
say(f"  reduced L = ({A_k}) zeta_dot^2 + (grad zeta)^2")
check("I1 kinetic coefficient 3 - 2/f''", sy.simplify(A_k - (3 - 2 / gm)) == 0, "A > 0: gradient instability; A < 0: ghost; A = 0: strongly coupled")

say("\n=== J. K7: QUMOND parent: indefinite")
p1, q1, Qf = sy.symbols("p q Qf")
Eq = 2 * p1 * q1 - q1 ** 2 - Qf * q1 ** 2
Hq = sy.hessian(Eq, (p1, q1))
check("J1 det Hessian = -4 for any nu: one negative eigenvalue", sy.simplify(Hq.det()) == -4, f"det {Hq.det()}")

say("\n=== K. K9 original RG: density-only permittivity in vacuum")
eps0 = sy.Symbol("eps0", positive=True)
gRG = M_ / (eps0 * r_ ** 2)
check("K1 vacuum outside the source: g ~ M/r^2, so no sqrt(a0 g_N)", sy.simplify(r_ * sy.diff(gRG, r_) / gRG) == -2, "density-only form; covariant form's gradient dependence not decided")

say("\n=== L. K2: locked FRW, twin dust")
X_, rb_, rd_, ell = sy.symbols("X rho_b rho_d ell", positive=True)
so = sy.solve([be * X_ - rb_, al * X_ - rd_], [X_, rd_], dict=True)[0]
check("L1 locked a = ahat, no vacuum term: rho_d/rho_b = a/b, and with a + b = 1, X = rho_b + rho_d", sy.simplify(so[rd_] - al / be * rb_) == 0 and sy.simplify((so[X_] - (rb_ + so[rd_])).subs(al, 1 - be)) == 0, "dust term in the Friedmann equation of g")
vac = sy.simplify(((be - al) * (rb_ + rd_ + 2 * ell) - (rb_ - rd_)).subs({rd_: al / be * rb_, al: 1 - be}))
say(f"  locking with one shared vacuum term ell: residual = {vac}, nonzero unless ell = 0 or a = b; so a second vacuum number, or unlock at late times")
check("L2 shared vacuum term breaks locking unless a = b", vac != 0, str(vac))
K_, tt, dd0 = sy.symbols("K t d0", positive=True)
dsol = K_ ** 2 * tt ** 4 / 144
check("L3 separation d'' = K sqrt(d) has d = K^2 t^4/144 from d = 0, as well as d = 0", sy.simplify(sy.diff(dsol, tt, 2) - K_ * sy.sqrt(dsol)) == 0, "non-unique at the adiabatic point: no seed protects it")
H0 = 0.675 * 100e3 / 3.0857e22; Om = 0.312
for f_, a in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    Kk2 = a * 1.5 * Om * H0 ** 2
    d = Kk2 * (1 / H0) ** 4 / 144
    say(f"  ESTIMATE {f_}: d = a0 (3/2) Om H0^2 t^4/144 at t = 1/H0, density frozen at today's, weight w/a^2 = 1: {d / 3.0857e22:.3f} Mpc (BOLTZ1's native h, Om)")
    RES[f"sep_Mpc_{f_}"] = d / 3.0857e22

say("")
nf = sum(1 for _, o in CHECKS if not o)
say(f"CHECKS {len(CHECKS) - nf}/{len(CHECKS)} pass. Failed: {[n for n, o in CHECKS if not o]}")
RES["checks"] = CHECKS
open(os.path.join(HERE, f"ux1_gates{TAG}.out"), "w").write("\n".join(L) + "\n")
json.dump(RES, open(os.path.join(HERE, f"ux1_gates{TAG}.json"), "w"), indent=1, default=str, sort_keys=True)
sys.exit(1 if nf else 0)
