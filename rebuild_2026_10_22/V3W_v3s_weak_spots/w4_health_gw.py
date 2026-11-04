#!/usr/bin/env python3
"""V3W W4: stability and GW speed of v3s, rechecked (sympy + small numerics).

Criteria: FROZEN_CRITERIA.md (37c16dcbaa).
W4a: TT tensor modes on a frozen background with uniform lapse gradient A, uniform P0, constant dP and D.P (stiffness included).
W4b/W4c: structural kinetic terms, leaf convexity and the principal-symbol Schur bound (C8 K1) recomputed, dust kinetic sign,
the stiff-side dispersion; record items read with their check status.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 python3 w4_health_gw.py      (V3W_MUTATE=1: gamma_L -> 0)
Geometric units G = c = 1 (K = 4 pi). kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing.
"""
import os, sys, json, math
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp

MUT = os.environ.get("V3W_MUTATE") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REB = os.path.dirname(HERE); ROOT = os.path.dirname(REB)
OUT, CHK = [], {}
RES = {"lane": "V3W_v3s_weak_spots", "part": "W4", "criteria": "37c16dcbaa", "mutate": MUT}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, detail):
    CHK[name] = bool(ok); RES.setdefault("checks", {})[name] = dict(ok=bool(ok), detail=str(detail))
    P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")


P("V3W W4  stability and GW speed of v3s" + ("  [MUTATE: gamma_L = 0]" if MUT else ""))
# ============================================================ W4a: tensor modes
t, x, y, z, eps = sp.symbols("t x y z epsilon", real=True)
a0, K, gLs = sp.symbols("a0 K gamma_L", positive=True)
Ax, Az = sp.symbols("A_x A_z", real=True)                     # background lapse gradient (A_i = d_i ln N)
P0x, P0z = sp.symbols("P0x P0z", real=True)                   # background P (in-plane x, along the wave z)
Gxx, Gxz, Gzx, Gzz, Gyy = sp.symbols("G_xx G_xz G_zx G_zz G_yy", real=True)   # background dP_j/dx_k (frozen, constant)
hp = sp.Function("hp")(t, z); hx = sp.Function("hx")(t, z)
Xc = (x, y, z)
lnN = Ax * x + Az * z
Pj = [P0x + Gxx * x + Gxz * z, Gyy * y, P0z + Gzx * x + Gzz * z]
H = sp.Matrix([[hp, hx, 0], [hx, -hp, 0], [0, 0, 0]])
hmat = sp.eye(3) + eps * H
hinv = sp.Matrix(3, 3, lambda i, j: sp.series(hmat.inv()[i, j], eps, 0, 3).removeO())
sqh = 1 - eps ** 2 * (hp ** 2 + hx ** 2) / 2                    # det h = 1 - eps^2 (hp^2 + hx^2) exactly (TT)
N = 1 + lnN                                                    # frozen background lapse to first order in the gradient (A_i x_i << 1)
Pup = [sum(hinv[i, j] * Pj[j] for j in range(3)) for i in range(3)]
DP = sum(sp.diff(sqh * Pup[i], Xc[i]) for i in range(3)) / sqh
PA = sum(Pup[i] * sp.diff(lnN, Xc[i]) for i in range(3))
s_ = K ** 2 * sum(Pj[i] * Pup[i] for i in range(3))            # u^2 = K^2 |P|^2
s0 = sp.expand(s_.subs(eps, 0)); ds = sp.expand(s_ - s0)
w0, w1, w2 = sp.symbols("w0 w1 w2")                            # W, dW/ds, d2W/ds2 at s0
Wexp = w0 + w1 * ds + w2 * ds ** 2 / 2
gLuse = 0 if MUT else gLs
LP = N * sqh * (PA - Wexp - gLuse / 2 * DP ** 2)
L2 = sp.expand(sp.series(sp.expand(LP), eps, 0, 3).removeO().coeff(eps, 2))
# derivative couplings of h in the P sector at quadratic order
dterms = [sp.diff(hp, t), sp.diff(hp, z), sp.diff(hx, t), sp.diff(hx, z)]
L2s = L2
for i, dt_ in enumerate(dterms):
    L2s = L2s.subs(dt_, sp.Symbol(f"d{i}"))
dsyms = [sp.Symbol(f"d{i}") for i in range(4)]
quad_d = [sp.simplify(sp.diff(L2s, a_, b_)) for a_ in dsyms for b_ in dsyms]
lin_d = [sp.simplify(sp.diff(L2s, a_).subs({d_: 0 for d_ in dsyms})) for a_ in dsyms]
# linear-in-derivative terms c(x) * h * dh = (c/2) d(h^2): a total derivative iff c is constant along that direction
lin_info = []
for i, c_ in enumerate(lin_d):
    lin_info.append(str(sp.simplify(c_)))
no_quad = all(q == 0 for q in quad_d)
P(f"  P-sector O(h^2) coefficients of (dh)(dh): all zero = {no_quad}; of h*(dh): {lin_info}")
# mass terms (at x = y = z = 0, frozen background)
at0 = {x: 0, y: 0, z: 0}
# c(x) h dh/dz = (c/2) d(h^2)/dz = total derivative - (dc/dz/2) h^2: fold into the mass (no derivative coupling survives)
cp = sp.simplify(lin_d[1] / hp); cx = sp.simplify(lin_d[3] / hx)
m_pp = sp.simplify(sp.diff(L2s.subs({d_: 0 for d_ in dsyms}), hp, 2).subs(at0) / 2 - sp.diff(cp, z).subs(at0) / 2)
m_xx = sp.simplify(sp.diff(L2s.subs({d_: 0 for d_ in dsyms}), hx, 2).subs(at0) / 2 - sp.diff(cx, z).subs(at0) / 2)
# GR TT Lagrangian (1/16 pi G)(1/4)(hdot_ij^2 - (dh_ij)^2) = (1/32 pi)(hp_t^2 - hp_z^2) + same for hx  ->  m^2 = -32 pi * coeff
m2p = sp.simplify(-32 * sp.pi * m_pp); m2x = sp.simplify(-32 * sp.pi * m_xx)
RES["W4a"] = dict(m2_plus=str(m2p), m2_cross=str(m2x), derivative_couplings_quadratic_zero=no_quad, linear_derivative_coeffs=lin_info)
P(f"  m_+^2 = {m2p}")
P(f"  m_x^2 = {m2x}")
# the linear-in-derivative terms are total derivatives when their coefficients are constant (frozen background)
lin_total = (lin_d[0] == 0 and lin_d[2] == 0 and not cp.has(hp) and not cp.has(hx) and not cx.has(hp) and not cx.has(hx)
             and not cp.has(t) and not cx.has(t))         # no h * dh/dt; dh/dz only as c(x) h dh/dz (folded into the mass)
check("W4-K1", no_quad and lin_total, "P sector adds no (dh)^2 term and only total-derivative h*dh terms at O(h^2): principal part is GR's, c_T = c exactly")
# GR limit: P sector off -> m^2 = 0
m2_off = sp.simplify(m2p.subs({P0x: 0, P0z: 0, Gxx: 0, Gxz: 0, Gzx: 0, Gzz: 0, Gyy: 0, w0: 0, w1: 0, w2: 0}))
check("W4-K2", m2_off == 0, f"known answer: P = 0 (law off) gives m_+^2 = {m2_off} (0, GR)")
# numbers: Solar-System backgrounds, both footings, scan |p|/a0 in [0, 0.99], direction, add hedgehog gradients at the solar surface
cl = 2.99792458e8; GMs = 1.32712440018e20; PC = 3.0857e16; RSUN = 6.957e8
FOOT = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
kGW = 2 * math.pi * 100.0 / cl
f_m2_ = sp.lambdify((K, gLs, Ax, Az, P0x, P0z, Gxx, Gxz, Gzx, Gzz, Gyy, w0, w1, w2), m2p, "math")
f_m2x_ = sp.lambdify((K, gLs, Ax, Az, P0x, P0z, Gxx, Gxz, Gzx, Gzz, Gyy, w0, w1, w2), m2x, "math")
def Wd(a0v, Kv, uv):                                           # dW/ds, d2W/ds2 at s = u^2 (W(u) = (a0^2/K)[-u/a0 - ln(1 - u/a0)])
    W1 = (a0v / Kv) * uv / (a0v - uv); W2 = (a0v / Kv) * a0v / (a0v - uv) ** 2
    W0 = (a0v ** 2 / Kv) * (-uv / a0v - math.log(1 - uv / a0v))
    return W0, W1 / (2 * uv), (W2 - W1 / uv) / (4 * uv ** 2)
def f_m2(a0v, Kv, gl, gx, gz, px, pz, *G0):
    uv = Kv * math.hypot(px, pz); d0, d1, d2 = Wd(a0v, Kv, uv)
    return f_m2_(Kv, gl, gx, gz, px, pz, *G0, d0, d1, d2)
def f_m2x(a0v, Kv, gl, gx, gz, px, pz, *G0):
    uv = Kv * math.hypot(px, pz); d0, d1, d2 = Wd(a0v, Kv, uv)
    return f_m2x_(Kv, gl, gx, gz, px, pz, *G0, d0, d1, d2)
W4a = {}
for f, A0 in FOOT.items():
    ag = A0 / cl ** 2; Kn = 4 * math.pi
    worst = 0.0; worst_st = 0.0
    for gname, gb in (("galactic_g=a0", A0), ("Earth_surface_g", 9.81)):
        Ab = gb / cl ** 2
        for Lpc in (21.7, 24.0, 90.0):
            L = Lpc * PC; gl = Kn * L ** 2 / 2
            p_h = GMs / cl ** 2 / L ** 2                         # hedgehog |p| (1/m)
            Gh = p_h / RSUN                                     # its gradient scale at the solar surface (generous)
            for uf in np.linspace(0.03, 0.99, 33):
                for th in np.linspace(0.0, math.pi, 13):
                    p0 = uf * ag
                    Pv0 = (p0 * math.sin(th) / Kn, p0 * math.cos(th) / Kn)
                    for (gx, gz) in ((Ab, 0.0), (0.0, Ab), (Ab / math.sqrt(2), Ab / math.sqrt(2))):
                        G0 = (Gh / Kn, Gh / Kn, Gh / Kn, Gh / Kn, Gh / Kn)
                        v = max(abs(f_m2(ag, Kn, gl, gx, gz, *Pv0, *G0)), abs(f_m2x(ag, Kn, gl, gx, gz, *Pv0, *G0)))
                        v0 = max(abs(f_m2(ag, Kn, 0.0, gx, gz, *Pv0, *G0)), abs(f_m2x(ag, Kn, 0.0, gx, gz, *Pv0, *G0)))
                        worst = max(worst, v); worst_st = max(worst_st, abs(v - v0))
    dv = worst / (2 * kGW ** 2)
    W4a[f] = dict(max_abs_m2=worst, stiffness_part=worst_st, dv_over_c_100Hz=dv)
    P(f"  W4a [{f}]: max |m^2| = {worst:.3e} m^-2 (stiffness part {worst_st:.1e}); dv/c at 100 Hz = {dv:.3e}  (C8 K9: <= 4.5e-43 / 5.4e-43, 5.1e-32 / 6.2e-32)")
RES["W4a_numbers"] = W4a
GW_BAND = (-3e-15, 7e-16)
# ============================================================ W4b/W4c items
# (i) structural: no time derivative of N or P in the v3s action at beta = eta = 0
Nn = sp.Function("N")(t, x); Pt = sp.Function("Pp")(t, x)
structural = "terms J(Y)/P.A - W, (D.P)^2, K(Q) and S_m contain A_i = d_i ln N, P, h_ij and their spatial derivatives only; " \
             "no dN/dt, no dP/dt (beta = eta = 0); tensor kinetic term only from R; khronon kinetic term only via Q in K(Q)"
# (ii) leaf convexity and principal-symbol Schur bound (K = 1 units as C8)
u, A_ = sp.symbols("u a0", positive=True)
Kk = 1
Wl = (A_ ** 2 / Kk) * (-u / A_ - sp.log(1 - u / A_))
g_ = Wl - u ** 2 / (2 * Kk)
gp = sp.simplify(sp.diff(g_, u)); gpp = sp.simplify(sp.diff(g_, u, 2))
ok_gp = sp.simplify(gp - u ** 2 / (Kk * (A_ - u))) == 0
ok_gpp = sp.simplify(gpp - u * (2 * A_ - u) / (Kk * (A_ - u) ** 2)) == 0
check("W4-K3", ok_gp and ok_gpp, f"g = W - u^2/2K: g' = {gp}, g'' = {gpp} (>= 0 on [0, a0))")
import mpmath as mpm
mpm.mp.dps = 40                                                # float64 is conditioned out at gamma_L xi^2 = 1e9 (first execution: 0.99999982)
gl_vals = [0] if MUT else [mpm.mpf("1e-3"), mpm.mpf(1), mpm.mpf("1e3")]
minratio = mpm.inf
for uf in np.linspace(0.0, 0.999, 101):
    uval = mpm.mpf(str(round(float(uf), 6)))
    gpv = uval ** 2 / (1 - uval); gppv = 1 / (1 - uval) ** 2 - 1      # g', g'' (K = a0 = 1), as W4-K3
    for ang in np.linspace(0.0, math.pi / 2, 31):
        ca, sa = mpm.cos(mpm.mpf(ang)), mpm.sin(mpm.mpf(ang))
        for xi in (mpm.mpf("1e-3"), mpm.mpf("0.1"), mpm.mpf(1), mpm.mpf(10), mpm.mpf("1e3")):
            for glv in gl_vals:
                ph = mpm.matrix([[1, 0, 0], [0, 0, 0], [0, 0, 0]]); xh = mpm.matrix([[ca], [sa], [0]])
                xx = xh * xh.T
                Hg = gppv * ph + ((gpv / uval) if uval > 0 else 0) * (mpm.eye(3) - ph)
                Msym = Kk * (mpm.eye(3) - xx) + Hg + glv * xi ** 2 * xx
                lo = min(mpm.mpf(Kk), glv * xi ** 2)
                ev = min(mpm.eigsy(Msym)[0])
                r_ = (ev / lo) if lo > 0 else (mpm.inf if ev > 0 else ev)
                minratio = min(minratio, r_)
minratio = float(minratio)
check("W4-K4", minratio >= 1 - 1e-10, f"principal-symbol Schur complement K(I - xx) + H_g + gamma_L xi xi >= min(K, gamma_L |xi|^2): min ratio {minratio:.12f} over 101 x 31 x 5 x {len(gl_vals)} points, mpmath 40 digits (C8 K1 line >= 1 - 1e-10; C8: 1)")
# (iii) dust kinetic sign
muK, Q = sp.symbols("mu_K Q", positive=True)
Kq = muK ** 2 * (Q - 1) ** 2
kpp = sp.diff(Kq, Q, 2)
check("W4-K5", sp.simplify(kpp - 2 * muK ** 2) == 0, f"K''(Q) = {kpp} > 0 (no khronon ghost at beta = 0, C5's kinetic entry K''a^3/(4H^2 K N^3))")
# (iv) stiff-side dispersion: omega^2 = 4 pi G rho_tau (M_theta - 1 + L*^2 k^2/2), M_theta in [1+x, (1+x)^2]
xs = np.logspace(-4, 4, 81); kk = np.logspace(-4, 4, 81)
Lfac = 0.0 if MUT else 1.0
w2min = min(min((1 + xv) - 1, (1 + xv) ** 2 - 1) + Lfac * kv ** 2 / 2 for xv in xs for kv in kk)
check("W4-K6", w2min > 0, f"stiff side (rho_tau > 0): min over x, k of (M_theta - 1 + L*^2 k^2/2) = {w2min:.3e} > 0 (LEAN switched_stable_where_positive; X3 c^2 = gamma_L(D.P + rho_d) >= 0)")
# record reads
X3 = json.load(open(os.path.join(REB, "X3_switched_stiffness", "x3_switched_stiffness_results.json")))
C5 = json.load(open(os.path.join(ROOT, "covariant_push_2026_10_22", "C5_health", "c5_health_results.json")))
C8 = json.load(open(os.path.join(ROOT, "covariant_push_2026_10_22", "C8_instantaneous", "c8_instantaneous_results.json")))
def okof(J, k):
    for v in J["checks"]:
        if v.get("id") == k:
            return bool(v["pass"])
    return None
x3_ok = (sum(bool(v["pass"]) for v in X3["checks"]), len(X3["checks"]))
c5_status = {k: okof(C5, k) for k in ("H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10")}
c8_status = {k: okof(C8, k) for k in ("K1", "K2", "K3", "K4", "K5", "K7", "K8", "K9")}
RES["record"] = dict(C5_checks=c5_status, C8_checks=c8_status, X3_pass=x3_ok)
P(f"  record: C5 checks {c5_status}")
P(f"  record: C8 checks {c8_status}; X3 {x3_ok}")
ITEMS = {
    "W4a c_T = c (principal part)": ("SHOWN", "W4-K1 here (sympy); C8 K9 PASS"),
    "W4a tensor mass terms": ("SHOWN", "W4a numbers here incl. stiffness; C8 K9 PASS"),
    "no time derivative of N, P at beta = eta = 0": ("SHOWN", structural),
    "leaf constraint convex / unique (any background)": ("SHOWN", "W4-K3, W4-K4 here; C8 K1, K3 PASS; LEAN XC2/XC5"),
    "khronon dust kinetic sign": ("SHOWN", "W4-K5 here; C5 kinetic matrix at beta = 0"),
    "C4-literal DOF = 2 tensor + omega = 0 pair, no ghost/unstable (Minkowski, y = 1)": ("SHOWN", "C5 H4 PASS (12 rows, two routes)"),
    "stiff side omega^2 >= 0 (WKB, pointwise)": ("SHOWN", "W4-K6 here; LEAN switched_stable_where_positive; X3 13/13"),
    "galaxy backgrounds, frozen-coefficient WKB (any x)": ("SHOWN", "W4-K6 over x in [1e-4, 1e4] with H4's dispersion; C5 H4 C4-literal rows (Minkowski, y = 1) PASS. C5 H6's 96 failing points are all eta > 0 rows (A33 family), not beta = eta = 0"),
    "soft side (D.P < 0) growth bounded, k-independent": ("SHOWN", "LEAN switched_uniform_bound; H4 0.006-0.20 e-folds; H5 lobes N <= 0.048 / 0.013 / 0.46"),
    "Solar-System background, beta = eta = 0": ("ASSERTED", "never run: C5 H6's 24 Solar-System points are eta > 0 rows and fail WKB validity (g/k >= 40.7); X3 gives D.P > 0 near the Sun (margin >= 1.77e4), so the stiff-side formula holds for k >> 1/AU only; no non-WKB SS-background spectrum on record"),
    "khronon fluid hyperbolic in 3D (c^2 >= 0 shown in 1D only)": ("ASSERTED", "X3 exact barotropic form is 1D; 2D/3D time evolution 'not shown' (V3_FULL_PICTURE 4.7)"),
    "single-stream khronon caustics": ("REPORTED", "X14 generic, not a ghost or gradient instability; a breakdown of the single-stream description"),
}
RES["items"] = {k: dict(status=v[0], source=v[1]) for k, v in ITEMS.items()}
for k, v in ITEMS.items():
    P(f"  [{v[0]:8s}] {k}: {v[1]}")
labels = {}
allk = all(CHK.values())
for f in FOOT:
    dv = W4a[f]["dv_over_c_100Hz"]
    lab_a = "PASS" if (allk and GW_BAND[0] <= -dv and dv <= GW_BAND[1] and CHK["W4-K1"]) else ("UNDECIDED (check failed)" if not allk else "FAIL")
    lab_b = "PASS" if allk else "UNDECIDED (check failed)"
    lab_c = "UNDECIDED: v3s's beta = eta = 0 form was never run on the Solar-System background (C5 H6 tested eta > 0 rows, which fail WKB validity there); X3's D.P > 0 near the Sun makes it stiff-side at WKB level k >> 1/AU; long wavelengths and 3D hyperbolicity not shown"
    labels[f] = dict(W4a=f"{lab_a}: c_T = c exactly in the principal part; |dv/c| <= {dv:.1e} at 100 Hz (GW170817 [-3e-15, 7e-16])",
                     W4b=f"{lab_b}: galaxy backgrounds, linear WKB scope: no ghost, no gradient instability (soft-side growth bounded)",
                     W4c=lab_c)
    for k_, v_ in labels[f].items():
        P(f"W4 [{f}] {k_}: {v_}")
RES["labels"] = labels
n_ok = sum(CHK.values())
P(f"\nW4 COMPLETE: {n_ok}/{len(CHK)} checks PASS")
json.dump(RES, open(os.path.join(HERE, f"w4_health_gw{TAG}.json"), "w"), indent=1, sort_keys=True, default=str)
open(os.path.join(HERE, f"w4_health_gw{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n_ok == len(CHK) else 1)
