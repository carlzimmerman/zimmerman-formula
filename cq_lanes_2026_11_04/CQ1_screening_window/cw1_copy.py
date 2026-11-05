#!/usr/bin/env python3
"""CW1: wide-binary curves before Gaia DR4 for the filter forms on record, with the host's Newtonian field in QUMOND's nu.
Criteria da6917883b. OMP_NUM_THREADS=1 python3 -I -B cw1.py [--mutate] [--quick].
Axisymmetric multipole QUMOND solver for a point mass in a uniform external field (units r_M = sqrt(G M / a0), a0 = 1).
kappa = 1/2 FITTED and held fixed; not theory closed."""
import contextlib, hashlib, io, json, math, os, resource, sys, time
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
from scipy.special import erf
from scipy.interpolate import CubicSpline
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); RB = os.path.join(REPO, "rebuild_2026_10_22")
MUT = "--mutate" in sys.argv; QUICK = "--quick" in sys.argv; OUT = []; RES = {}; FAILS = []
def P(s=""): print(s, flush=True); OUT.append(s)
def check(name, ok, msg):
    ok = bool(ok) or MUT; P(f"{name} {'PASS' if ok else 'FAIL'}: {msg}"); RES.setdefault("checks", {})[name] = dict(ok=ok, msg=msg)
    if not ok: FAILS.append(name)
G, MS, AU = 6.6743e-11, 1.98892e30, 1.495978707e11; KAP = 0.5
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; GOBS = (1.778e-10, 1.9e-10, 2.32e-10); GPRI = 1.9e-10; GCAS = 2.32e-10; CEIL = 5.2e-27
S_KAU = np.array([1, 2, 3, 5, 7, 10, 15, 20, 30], float); MASSES = (0.5, 1.0, 1.5, 2.5)
P(f"CW1 (criteria da6917883b){'  [MUTATE: nu = 1]' if MUT else ''}{'  [QUICK]' if QUICK else ''}; kappa = 1/2 FITTED; not theory closed")

# ---------------- nu, its law, the inversion to the Newtonian field ----------------
if MUT:
    nu = lambda y: np.ones_like(np.asarray(y, float)); Gf = lambda y: np.asarray(y, float); dGf = lambda y: np.ones_like(np.asarray(y, float))
else:
    nu = lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300))
    Gf = lambda y: y * nu(y)
    dGf = lambda y: nu(y) - 1 / (2 * np.maximum(y, 1e-300) * np.sqrt(0.25 + 1 / np.maximum(y, 1e-300)))
def eta_newton(gobs, a0):
    eo = gobs / a0; return eo if MUT else brentq(lambda y: float(Gf(y)) - eo, 1e-9, eo)
def fsm(t):
    """Enclosed-mass fraction of a unit Gaussian at radius t (sigma = 1)."""
    t = np.asarray(t, float); out = np.empty_like(t); s = t < 1e-3
    out[~s] = erf(t[~s] / math.sqrt(2)) - math.sqrt(2 / math.pi) * t[~s] * np.exp(-t[~s] ** 2 / 2); out[s] = math.sqrt(2 / math.pi) / 3 * t[s] ** 3; return out

# ---------------- the solver ----------------
def legendre(L, mu):
    Pl = np.zeros((L + 1, mu.size)); dP = np.zeros((L + 1, mu.size)); Pl[0] = 1; dP[0] = 0
    if L >= 1: Pl[1] = mu; dP[1] = 1
    for l in range(1, L):
        Pl[l + 1] = ((2 * l + 1) * mu * Pl[l] - l * Pl[l - 1]) / (l + 1); dP[l + 1] = dP[l - 1] + (2 * l + 1) * Pl[l]
    return Pl, dP
class Solver:
    def __init__(s, eta, form, gs=2.0, L=64, nmu=96, per_dec=200, xmin=1e-7, xmax=1e5):
        s.eta, s.form, s.gs, s.L = eta, form, gs, L
        s.u = np.linspace(math.log(xmin), math.log(xmax), int(round(per_dec * math.log10(xmax / xmin))) + 1); s.du = s.u[1] - s.u[0]; s.x = np.exp(s.u)
        s.mu, s.w = np.polynomial.legendre.leggauss(nmu); s.st = np.sqrt(1 - s.mu ** 2); s.Pl, s.dP = legendre(L, s.mu)
        X, M = s.x[:, None], s.mu[None, :]; ST = s.st[None, :]
        s.xi = s.width(X, M)
        f = np.ones_like(X * M) if s.xi is None else fsm(X / s.xi)
        gfr = -X ** -2.0 * f + eta * M; gft = -eta * ST * np.ones_like(X); gm = np.sqrt(gfr ** 2 + gft ** 2); nue = float(nu(eta)); nf = nu(gm)
        Fr = (nf - 1) * gfr - (nue - 1) * eta * M; Ft = -(nf - nue) * eta * ST * np.ones_like(X)
        l = np.arange(L + 1)[None, :]
        with np.errstate(all="ignore"):   # Accelerate BLAS raises spurious FP flags in matmul; finiteness is asserted below
            s.a = (Fr * s.w[None, :]) @ s.Pl.T * (2 * l + 1) / 2
            bb = (Ft * s.w[None, :] * (-ST)) @ s.dP.T
        s.b = np.zeros_like(s.a); s.b[:, 1:] = bb[:, 1:] * (2 * l[:, 1:] + 1) / (2 * l[:, 1:] * (l[:, 1:] + 1))
        assert np.all(np.isfinite(s.a)) and np.all(np.isfinite(s.b)), "non-finite multipole coefficients"
        c = s.a + (l + 1) * s.b; d = s.a - l * s.b; n = s.x.size; lv = np.arange(L + 1)
        A = np.zeros_like(c); B = np.zeros_like(d); q = math.exp(-s.du); qa = q ** (lv + 2); qb = q ** (lv - 1.0)
        A[0] = c[0] / (lv + 2)
        for i in range(n - 1): A[i + 1] = qa * A[i] + 0.5 * s.du * (qa * c[i] + c[i + 1])
        B[-1] = d[-1] / (lv + 1)
        for i in range(n - 2, -1, -1): B[i] = qb * B[i + 1] + 0.5 * s.du * (d[i] + qb * d[i + 1])
        s.gr = s.a - (lv * (lv + 1) / (2 * lv + 1))[None, :] * (A + B); s.ph = (-lv * A + (lv + 1) * B) / (2 * lv + 1)
        s.gself = float(s.gr[0, 1]) if L >= 1 else 0.0   # the uniform l = 1 field at the origin: g_r,1 -> V mu as x -> 0
        s.spl = CubicSpline(s.u, s.gr * s.x[:, None] ** 2, axis=0); s.spl0 = CubicSpline(s.u, s.a[:, 0] * s.x ** 2)
        s.C2 = 0.6 * float(np.trapz(d[:, 2] / s.x, s.u)) if L >= 2 else 0.0   # Phi_2 -> C2 x^2 at the origin
    def width(s, X, M):
        f, eta, gs = s.form, s.eta, s.gs
        if f in ("PQ", "N"): return None
        if f == "E55": return 0.55 * np.ones_like(X * M)
        if f == "HALF": return 0.5 * np.ones_like(X * M)
        if f == "LOC1":
            gq = np.sqrt(X ** -4.0 + eta * eta); dg = np.abs(dGf(gq) * (-2 * X ** -5.0 / gq)); xi = Gf(gq) ** 2 / np.maximum(dg * gs, 1e-300)
            return np.minimum(xi, 1e4) * np.ones_like(M)
        if f == "LOC3":
            g2 = X ** -4.0 + eta * eta - 2 * eta * X ** -2.0 * M; gn = np.sqrt(np.maximum(g2, 1e-300))
            dr = -4 * X ** -5.0 + 4 * eta * X ** -3.0 * M; dt = 2 * eta * X ** -3.0 * np.sqrt(1 - M ** 2); dgn = np.sqrt(dr ** 2 + dt ** 2) / (2 * gn)
            xi = Gf(gn) ** 2 / np.maximum(dGf(gn) * dgn * gs, 1e-300); return np.minimum(xi, 1e4)
        raise ValueError(f)
    def q(s): return 2 * abs(s.C2)                      # KT16's q = |Q2| / (1.5 a0 / r_M), Q2 = 3 C2
    def gamma(s, x, mu):
        """gamma_r = -g_int,r / (G M / r^2) at (x, mu), self-acceleration removed."""
        x = np.atleast_1d(np.asarray(x, float)); mu = np.atleast_1d(np.asarray(mu, float)); uu = np.log(np.clip(x, s.x[0], s.x[-1]))
        y2 = s.spl(uu); Pm, _ = legendre(s.L, mu)        # x^2 g_r,l (cubic in ln x)
        pair = x.size == mu.size
        with np.errstate(all="ignore"): g2 = np.sum(y2 * Pm.T, 1) if pair else y2 @ Pm
        if s.form == "N": return np.ones_like(g2)
        xx = x if pair else x[:, None]; mm = mu if pair else mu[None, :]
        return 1 - g2 + xx ** 2 * s.gself * mm
    def gamma_avg(s, x):
        x = np.asarray(x, float); return np.ones_like(x) if s.form == "N" else 1 - s.spl0(np.log(np.clip(x, s.x[0], s.x[-1])))
    def table(s, xlo=1e-4, xhi=1e4, nx=1601, nm=201):
        tx = np.geomspace(xlo, xhi, nx); tm = np.linspace(-1, 1, nm); return tx, tm, s.gamma(tx, tm)

def interp2(tx, tm, T, x, mu):
    lx = np.log(np.clip(x, tx[0], tx[-1])); fx = (lx - math.log(tx[0])) / (math.log(tx[-1] / tx[0])) * (tx.size - 1); i = np.clip(fx.astype(int), 0, tx.size - 2); a = fx - i
    fm = (np.clip(mu, -1, 1) + 1) / 2 * (tm.size - 1); j = np.clip(fm.astype(int), 0, tm.size - 2); b = fm - j
    return (1 - a) * (1 - b) * T[i, j] + a * (1 - b) * T[i + 1, j] + (1 - a) * b * T[i, j + 1] + a * b * T[i + 1, j + 1]

# ---------------- 1D forms (KT20's formula) ----------------
def gam1d(r, M, a0, ge, xi):
    """KT20 verbatim: r in m, M in kg, ge in nu as given; xi 0 = plain."""
    gN = G * M / r ** 2
    if np.isscalar(xi) and xi <= 0: h = gN
    else: x = r / xi; h = gN * (erf(x / math.sqrt(2)) - math.sqrt(2 / math.pi) * x * np.exp(-x * x / 2))
    return (gN + (nu(np.sqrt(ge * ge + h * h) / a0) - 1) * h) / gN

# ================= K1, K2 =================
P("\n== Solver checks")
sv = Solver(0.0, "PQ", L=16); xs = np.array([0.03, 0.3, 1, 3, 30]); e1 = float(np.max(np.abs(sv.gamma(xs, np.array([-0.9, 0, 0.9])) / nu(xs ** -2.0)[:, None] - 1)))
check("K1", e1 <= 1e-6, f"eta = 0 plain QUMOND gamma_r vs nu(x^-2), max rel {e1:.2e} (line 1e-6)")
k2 = {}
for foot, a0 in A0.items():
    eta = eta_newton(GPRI, a0); sv = Solver(eta, "PQ"); ne = float(nu(eta)); Ke = float(-1 / (2 * eta * math.sqrt(0.25 + 1 / eta)) / ne) if not MUT else 0.0
    mus = np.array([-1.0, -0.5, 0.0, 0.5, 1.0]); gnum = sv.gamma(np.array([30.0] * 5), mus); gan = ne * (1 + Ke / 2 * (1 - mus ** 2))
    k2[foot] = float(np.max(np.abs(gnum / gan - 1))); RES.setdefault("K2", {})[foot] = dict(eta_N=eta, nu_e=ne, K_e=Ke, numeric=gnum.tolist(), analytic=gan.tolist(), self_accel=sv.gself)
    P(f"  [{foot}] eta_N {eta:.4f}, nu_e {ne:.4f}, K_e {Ke:+.4f}; x = 30 gamma_r(mu = -1, -.5, 0, .5, 1) " + " ".join(f"{v:.4f}" for v in gnum) + " vs " + " ".join(f"{v:.4f}" for v in gan) + f"; self-acceleration {sv.gself:+.3e} a0")
check("K2", max(k2.values()) <= 0.01, f"deep EFE x = 30 vs nu_e (1 + K_e/2 sin^2), max rel {max(k2.values()):.2e} (line 1 %)")
# Post-result diagnostic (written after K2's first run, not a check): split the x = 30 residual into the part even in mu
# (the linear-response form) and the odd part (second-order lopsidedness, expected to fall as 1/x), at larger x.
for foot, a0 in A0.items():
    eta = eta_newton(GPRI, a0); sv = Solver(eta, "PQ"); ne = float(nu(eta)); Ke = float(-1 / (2 * eta * math.sqrt(0.25 + 1 / eta)) / ne) if not MUT else 0.0; dg = []
    for xx in (30.0, 100.0, 300.0, 1000.0):
        gp, gm_ = sv.gamma(np.array([xx]), np.array([1.0]))[0], sv.gamma(np.array([xx]), np.array([-1.0]))[0]; g0 = sv.gamma(np.array([xx]), np.array([0.0]))[0]
        dg.append(dict(x=xx, even_par=0.5 * (gp + gm_) / ne - 1, perp=g0 / (ne * (1 + Ke / 2)) - 1, odd_par=0.5 * (gp - gm_) / ne))
    RES.setdefault("K2_diag", {})[foot] = dg
    P(f"  K2 diagnostic [{foot}]: " + "; ".join(f"x {r['x']:.0f}: even {r['even_par']:+.1e}, perp {r['perp']:+.1e}, odd {r['odd_par']:+.1e}" for r in dg))

# ================= K3 Cassini against CZ2 =================
K3REF = {"canonical": dict(HALF=1.179, LOC1=0.003948), "alt": dict(HALF=2.97, LOC1=0.02147)}; k3 = []
for foot, a0 in A0.items():
    rM = math.sqrt(G * MS / a0); qp = CEIL / (1.5 * a0 / rM); eta = eta_newton(GCAS, a0)
    for f in ("HALF", "LOC1"):
        xq = Solver(eta, f).q() / qp; k3.append(abs(xq / K3REF[foot][f] - 1)); RES.setdefault("K3", {})[f"{foot}|{f}"] = dict(x_ceiling=xq, cz2=K3REF[foot][f])
        P(f"  K3 [{foot}] {f}: Cassini {xq:.4g} x ceiling (CZ2 {K3REF[foot][f]})")
check("K3", max(k3) <= 0.02, f"Cassini vs CZ2, max rel {max(k3):.2e} (line 2 %)")

# ================= K4 KT20 =================
k20 = json.load(open(os.path.join(RB, "KT20_filter_wide_binaries/kt20.json"))); e4 = 0.0
for foot, a0 in A0.items():
    for m in (1.0, 1.5):
        for ge in (1.9e-10, 2.32e-10):
            r = k20[f"{foot}|M{m}|ge{ge:.3g}"]; ss = np.array(r["s_kAU"]) * 1e3 * AU; xi = 0.55 * math.sqrt(G * m * MS / a0)
            e4 = max(e4, float(np.max(np.abs(gam1d(ss, m * MS, a0, ge, 0.0) / np.array(r["gamma_plain"]) - 1))), float(np.max(np.abs(gam1d(ss, m * MS, a0, ge, xi) / np.array(r["gamma_filter"]) - 1))))
check("K4", e4 <= 1e-10, f"1D form with KT20's observed fields reproduces kt20.json, max rel {e4:.1e}")

# ================= stage 1: curves =================
P("\n== Stage 1: curves (gamma_r; mean of mu = +-1 'par', mu = 0 'perp', mu-average 'avg')")
FORMS = ("PQ", "LOC3", "LOC1", "E55", "HALF"); SOLV = {}
for foot, a0 in A0.items():
    for go in GOBS:
        eta = eta_newton(go, a0)
        for f in FORMS: SOLV[(foot, go, f)] = Solver(eta, f)
CUR = {}
for foot, a0 in A0.items():
    for go in GOBS:
        eta = eta_newton(go, a0); P(f"\n[{foot}] g_obs {go:.4g} -> Newtonian {eta * a0:.4g} m/s^2 (eta_N {eta:.4f})")
        for m in MASSES:
            rM = math.sqrt(G * m * MS / a0); x = S_KAU * 1e3 * AU / rM; P(f"  M {m} Msun, r_M {rM / AU:.0f} AU; s kAU " + " ".join(f"{v:6.0f}" for v in S_KAU))
            for f in FORMS:
                sv = SOLV[(foot, go, f)]; par = 0.5 * (sv.gamma(x, np.ones_like(x)) + sv.gamma(x, -np.ones_like(x))); per = sv.gamma(x, np.zeros_like(x)); avg = sv.gamma_avg(x)
                CUR[f"{foot}|{go:.4g}|M{m}|{f}"] = dict(x=x.tolist(), par=par.tolist(), perp=per.tolist(), avg=avg.tolist())
                if go == GPRI or m == 1.0: P(f"    {f:5s} avg " + " ".join(f"{v:6.3f}" for v in avg) + "   par " + " ".join(f"{v:6.3f}" for v in par[[2, 5, 8]]) + "  perp " + " ".join(f"{v:6.3f}" for v in per[[2, 5, 8]]) + " (3/10/30 kAU)")
            pq = np.array(CUR[f"{foot}|{go:.4g}|M{m}|PQ"]["avg"])
            for f in FORMS[1:]:
                ex = (np.array(CUR[f"{foot}|{go:.4g}|M{m}|{f}"]["avg"]) - 1) / np.maximum(pq - 1, 1e-300); CUR[f"{foot}|{go:.4g}|M{m}|{f}"]["excess_ratio"] = ex.tolist()
                if go == GPRI: P(f"    {f:5s} excess / plain " + " ".join(f"{v:6.2f}" for v in ex))
            # 1D form with the Newtonian field (KT20's table, corrected)
            g1 = {}
            for f, e in (("PQ", 0.0), ("E55", 0.55), ("HALF", 0.5)):
                g1[f] = gam1d(S_KAU * 1e3 * AU, m * MS, a0, eta * a0, e * rM).tolist()
            sv1 = SOLV[(foot, go, "LOC1")]; xi1 = np.array([float(np.interp(math.log(v), sv1.u, np.log(sv1.xi[:, 0]))) for v in x]); hh = x ** -2.0 * fsm(x / np.exp(xi1))
            g1["LOC1"] = ((x ** -2.0 + (nu(np.sqrt(eta ** 2 + hh ** 2)) - 1) * hh) / x ** -2.0).tolist(); CUR[f"{foot}|{go:.4g}|M{m}|1D"] = g1
            if go == GPRI and m in (1.0, 1.5): P("    1D (KT20 form, Newtonian field): " + "; ".join(f"{k} " + " ".join(f"{v:.3f}" for v in np.array(g1[k])[[2, 5, 8]]) for k in g1) + " (3/10/30 kAU)")
RES["curves"] = CUR
# KT20 corrected table (filter excess / plain, 1D, E55) for comparison with KT20's README
P("\nKT20's table corrected (1D, E55 excess / plain, primary field):")
for foot, a0 in A0.items():
    for m in (1.0, 1.5):
        g1 = CUR[f"{foot}|{GPRI:.4g}|M{m}|1D"]; ex = (np.array(g1["E55"]) - 1) / (np.array(g1["PQ"]) - 1); P(f"  [{foot}] M {m}: " + " ".join(f"{v:.2f}" for v in ex))

# ================= DR3 inner shape: KT21's Q =================
P("\n== DR3 inner shape (KT21's Q)")
CSV = os.path.join(REPO, "real_research/data/widebinaries/dr3_extract/wide_binaries_dr3.csv"); d = np.genfromtxt(CSV, delimiter=",", names=True)
s = d["sep_kAU"] * 1e3 * AU; Mt = (d["M1_msun"] + d["M2_msun"]) * MS; vp = d["v_perp_kms"] * 1e3; vt = vp / np.sqrt(G * Mt / s); n = len(s); K = 40; SSYS = 0.020
lg, bg = np.radians(d["l_gal"]), np.radians(d["b_gal"]); GL, GB, GN = -np.sin(lg), -np.sin(bg) * np.cos(lg), np.cos(bg) * np.cos(lg)   # GC direction in (e_l, e_b, LOS)
def orbits3(rng, alpha, m):
    """KT21's orbits() verbatim (same draws, same order) plus the 3D unit vector of the relative position in the orbit-sky frame."""
    e = rng.uniform(0, 1, m) ** (1 / (alpha + 1)); Mn = rng.uniform(0, 2 * math.pi, m); E = Mn.copy()
    for _ in range(60): E = E - (E - e * np.sin(E) - Mn) / (1 - e * np.cos(E))
    r = 1 - e * np.cos(E); x = np.cos(E) - e; y = np.sqrt(1 - e * e) * np.sin(E); vx = -np.sin(E) / r; vy = np.sqrt(1 - e * e) * np.cos(E) / r
    ci = rng.uniform(-1, 1, m); w = rng.uniform(0, 2 * math.pi, m)
    X = x * np.cos(w) - y * np.sin(w); Y = x * np.sin(w) + y * np.cos(w); VX = vx * np.cos(w) - vy * np.sin(w); VY = vx * np.sin(w) + vy * np.cos(w)
    rs = np.hypot(X, Y * ci); vs = np.hypot(VX, VY * ci); si = np.sqrt(1 - ci * ci)
    return rs, vs * np.sqrt(rs), r / rs, X / r, Y * ci / r, Y * si / r
def Qs(v, y): return math.log(np.median(v[(y >= 2) & (y < 10)])) - math.log(np.median(v[y >= 10]))
k21 = json.load(open(os.path.join(RB, "KT21_filter_wide_binary_dr3_shape/kt21.json"))); DR3 = {}; e5 = 0.0
for foot, a0 in A0.items():
    y = G * Mt / (a0 * s * s); qo = Qs(vt, y); bs = []
    for seed in (11, 12):
        rng = np.random.default_rng(seed); b = []
        for _ in range(2000): i = rng.integers(0, n, n); b.append(Qs(vt[i], y[i]))
        bs.append(float(np.std(b)))
    sig = math.sqrt(bs[0] ** 2 + SSYS ** 2)
    rng = np.random.default_rng(2026110302); idx = np.repeat(np.arange(n), K); _, vN, ratio, ux, uy, uz = orbits3(rng, 1.2, n * K)
    om = np.random.default_rng(2026110402).uniform(0, 2 * math.pi, n * K); mu = (np.cos(om) * ux - np.sin(om) * uy) * GL[idx] + (np.sin(om) * ux + np.cos(om) * uy) * GB[idx] + uz * GN[idx]
    r3 = s[idx] * ratio; Mi = Mt[idx]; yi = y[idx]; x3 = r3 / np.sqrt(G * Mi / a0)
    # K5: KT21 with its observed 1.9e-10 and the 1D form
    pk = dict(Newton=Qs(vN, yi), plain=Qs(vN * np.sqrt(gam1d(r3, Mi, a0, 1.9e-10, 0.0)), yi), filter=Qs(vN * np.sqrt(gam1d(r3, Mi, a0, 1.9e-10, 0.55 * np.sqrt(G * Mi / a0))), yi))
    kr = k21[foot]; e5 = max(e5, abs(qo - kr["Q_obs"]), abs(sig - kr["sigma"]), *[abs(pk[k] - kr["pred"][k]) for k in pk])
    R = dict(Q_obs=qo, sigma=sig, sigma_stat=bs[0], KT21_repro=pk, mu_mean=float(np.mean(mu)), mu_rms=float(np.sqrt(np.mean(mu ** 2))), pred={})
    for go in GOBS:
        eta = eta_newton(go, a0); pr = {"N": Qs(vN, yi)}
        for f in FORMS:
            sv = SOLV[(foot, go, f)]; tx, tm, T = sv.table(); pr[f] = Qs(vN * np.sqrt(np.maximum(interp2(tx, tm, T, x3, mu), 0)), yi)
        e = eta * a0; pr["PQ_1D"] = Qs(vN * np.sqrt(gam1d(r3, Mi, a0, e, 0.0)), yi); pr["E55_1D"] = Qs(vN * np.sqrt(gam1d(r3, Mi, a0, e, 0.55 * np.sqrt(G * Mi / a0))), yi)
        R["pred"][f"{go:.4g}"] = {k: dict(Q_pred=v, z=(qo - v) / sig, label="CONSISTENT" if abs((qo - v) / sig) <= 2 else "TENSION" if abs((qo - v) / sig) <= 3 else "EXCLUDED") for k, v in pr.items()}
    DR3[foot] = R; P(f"[{foot}] Q_obs {qo:+.4f} +- {sig:.4f}; mu over orbits: mean {R['mu_mean']:+.3f}, rms {R['mu_rms']:.3f} (isotropic 0.577)")
    for go in GOBS:
        P(f"  g_obs {go:.4g}: " + "; ".join(f"{k} {v['Q_pred']:+.4f} (z {v['z']:+.2f})" for k, v in R["pred"][f"{go:.4g}"].items()))
check("K5", e5 <= 1e-6, f"KT21 Q_obs, sigma and Q_pred (Newton, plain, filter) reproduced, max abs {e5:.1e}")
RES["DR3"] = DR3

# ================= DR4 pipeline injection (read only) =================
P("\n== Frozen DR4 pipeline: gamma_inf it would return (imported read only)")
PIPE = os.path.join(REPO, "prep_2026/gaia_dr4_prep/wide_binary_pipeline.py"); sha = hashlib.sha256(open(PIPE, "rb").read()).hexdigest(); P(f"pipeline SHA-256 {sha}")
sys.path.insert(0, os.path.dirname(PIPE)); import wide_binary_pipeline as wbp; sys.path.pop(0)
assert sys.dont_write_bytecode
rng = np.random.default_rng(20261216); NM = 300_000 if QUICK else 1_000_000; pop_m = wbp.make_population(NM, rng, dr4=True)
with contextlib.redirect_stdout(io.StringIO()):
    MOD = {"canonical": wbp.model_medians(pop_m, wbp.A0_CAN, wbp.GRID, rng), "alt": wbp.model_medians(pop_m, wbp.A0_ALT, wbp.GRID, rng)}
PA0 = {"canonical": wbp.A0_CAN, "alt": wbp.A0_ALT}; ND = 30000; NREAL = 2 if QUICK else 4
def vt_custom(pop, gv):
    vX = (gv * pop['pmx'] + pop['npmx']) * 4.74e3 * (pop['d_obs'] / 1000.); vY = (gv * pop['pmy'] + pop['npmy']) * 4.74e3 * (pop['d_obs'] / 1000.); return np.hypot(vX, vY) / pop['vc_obs']
def draw():
    pop = wbp.make_population(int(ND * 2.7), rng, dr4=True); keep = rng.permutation(len(pop['s_obs']))[:ND]; return {k: v[keep] for k, v in pop.items()}
def fit(foot, vt_d, pop):
    with contextlib.redirect_stdout(io.StringIO()): g, sg, med, sgm, cnt = wbp.run_fit(np.log10(pop['g_proj'] / PA0[foot]), vt_d, MOD[foot], rng, "cw1")
    return g, sg, med
P(f"master population {NM:,} drawn ({len(pop_m['s_obs']):,} after selection; the pipeline uses 3,000,000), N_data {ND:,}, {NREAL} realisations per form")
k6 = []
for gi in (1.00, 1.1614):
    pop = draw(); g, sg, _ = fit("canonical", wbp.vtilde_of(pop, gi, wbp.A0_CAN), pop); tol = max(2 * sg, 0.02); k6.append(abs(g - gi) <= tol); P(f"  K6 inject declared shape {gi:.4f} -> {g:.4f} +- {sg:.4f} (tol {tol:.4f})")
check("K6", all(k6), "pipeline import recovers its own declared shape at 1.00 and 1.1614")
PIPEOUT = {}
for foot, a0 in A0.items():
    PIPEOUT[foot] = {}
    for f in ("N",) + FORMS:
        gs_, med_ = [], []
        for _ in range(NREAL):
            pop = draw(); yt = pop['g_true'] / a0; xt = yt ** -0.5
            gv = np.ones_like(xt) if f == "N" else np.sqrt(np.maximum(SOLV[(foot, GPRI, f)].gamma_avg(xt), 0)); g, sg, med = fit(foot, vt_custom(pop, gv), pop); gs_.append(g); med_.append(med)
        mN = None
        PIPEOUT[foot][f] = dict(gamma_inf=float(np.mean(gs_)), spread=float(np.std(gs_)), each=gs_, bin_median=np.nanmean(np.array(med_), 0).tolist())
    mN = np.array(PIPEOUT[foot]["N"]["bin_median"])
    for f in PIPEOUT[foot]: PIPEOUT[foot][f]["ratio_to_N"] = (np.array(PIPEOUT[foot][f]["bin_median"]) / mN).tolist()
    P(f"[{foot}] bins log10 y_proj edges {wbp.EDGES.tolist()}")
    for f in PIPEOUT[foot]: P(f"  {f:5s} gamma_inf {PIPEOUT[foot][f]['gamma_inf']:.4f} (spread {PIPEOUT[foot][f]['spread']:.4f}); median / Newton per bin " + " ".join(f"{v:.3f}" for v in PIPEOUT[foot][f]["ratio_to_N"]))
RES["pipeline"] = dict(sha256=sha, n_master=NM, n_data=ND, n_real=NREAL, out=PIPEOUT)

# ================= separation labels =================
P("\n== Separation (primary field 1.9e-10)")
def lab(a, b): m = max(a, b); return "SEPARABLE" if m >= 3 else "MARGINAL" if m >= 2 else "NOT SEPARABLE"
SEP = {}
for foot in A0:
    pr = DR3[foot]["pred"][f"{GPRI:.4g}"]; po = PIPEOUT[foot]
    for f in FORMS[1:]:
        dq_p = abs(pr[f]["Q_pred"] - pr["PQ"]["Q_pred"]) / SSYS; dg_p = abs(po[f]["gamma_inf"] - po["PQ"]["gamma_inf"]) / 0.028
        dq_n = abs(pr[f]["Q_pred"] - pr["N"]["Q_pred"]) / SSYS; dg_n = abs(po[f]["gamma_inf"] - po["N"]["gamma_inf"]) / 0.028
        SEP[f"{foot}|{f}"] = dict(vs_plain=dict(dQ=dq_p, dgamma=dg_p, label=lab(dq_p, dg_p)), vs_newton=dict(dQ=dq_n, dgamma=dg_n, label=lab(dq_n, dg_n)))
        P(f"  [{foot}] {f:5s} vs plain: dQ {dq_p:.2f} sigma_sys, dgamma {dg_p:.2f} sigma_tot -> {lab(dq_p, dg_p)};  vs Newton: {dq_n:.2f}, {dg_n:.2f} -> {lab(dq_n, dg_n)}")
    dq = abs(pr["PQ"]["Q_pred"] - pr["N"]["Q_pred"]) / SSYS; dg = abs(po["PQ"]["gamma_inf"] - po["N"]["gamma_inf"]) / 0.028; SEP[f"{foot}|PQ"] = dict(vs_newton=dict(dQ=dq, dgamma=dg, label=lab(dq, dg)))
    P(f"  [{foot}] PQ    vs Newton: {dq:.2f}, {dg:.2f} -> {lab(dq, dg)}")
RES["separation"] = SEP

# ================= K7 convergence =================
P("\n== K7 convergence (L 96, n_mu 128)")
k7g, k7q = 0.0, 0.0
for foot, a0 in A0.items():
    eta = eta_newton(GPRI, a0); etc = eta_newton(GCAS, a0)
    for f in FORMS:
        hi = Solver(eta, f, L=96, nmu=128); lo = SOLV[(foot, GPRI, f)]
        for m in MASSES:
            x = S_KAU * 1e3 * AU / math.sqrt(G * m * MS / a0)
            for mm in (-1.0, 0.0, 1.0): k7g = max(k7g, float(np.max(np.abs(hi.gamma(x, mm * np.ones_like(x)) - lo.gamma(x, mm * np.ones_like(x))))))
            k7g = max(k7g, float(np.max(np.abs(hi.gamma_avg(x) - lo.gamma_avg(x)))))
        if f in ("LOC3", "LOC1", "HALF"):
            qa, qb = Solver(etc, f).q(), Solver(etc, f, L=96, nmu=128).q(); k7q = max(k7q, abs(qb / qa - 1) if qa > 0 else 0.0)
check("K7", k7g <= 0.003 and k7q <= 0.02, f"max |d gamma_r| {k7g:.2e} (line 0.003), max Cassini rel {k7q:.2e} (line 2 %)")
# Post-result diagnostic (written after K7's first quick run, not a check): where the K7 difference sits, and whether the
# sealed DR3 Q values move at the higher resolution. The pipeline injection uses only the mu-average (l = 0).
K7D = {}
for foot, a0 in A0.items():
    eta = eta_newton(GPRI, a0); y = G * Mt / (a0 * s * s)
    rng = np.random.default_rng(2026110302); idx = np.repeat(np.arange(n), K); _, vN7, ratio7, ux7, uy7, uz7 = orbits3(rng, 1.2, n * K)
    om7 = np.random.default_rng(2026110402).uniform(0, 2 * math.pi, n * K); mu7 = (np.cos(om7) * ux7 - np.sin(om7) * uy7) * GL[idx] + (np.sin(om7) * ux7 + np.cos(om7) * uy7) * GB[idx] + uz7 * GN[idx]
    x37 = s[idx] * ratio7 / np.sqrt(G * Mt[idx] / a0); yi7 = y[idx]
    for f in FORMS:
        hi = Solver(eta, f, L=96, nmu=128); lo = SOLV[(foot, GPRI, f)]; dd = dict(par=0.0, perp=0.0, avg=0.0)
        for m in MASSES:
            x = S_KAU * 1e3 * AU / math.sqrt(G * m * MS / a0)
            dd["par"] = max(dd["par"], float(np.max(np.abs(0.5 * (hi.gamma(x, np.ones_like(x)) + hi.gamma(x, -np.ones_like(x))) - 0.5 * (lo.gamma(x, np.ones_like(x)) + lo.gamma(x, -np.ones_like(x)))))))
            dd["perp"] = max(dd["perp"], float(np.max(np.abs(hi.gamma(x, np.zeros_like(x)) - lo.gamma(x, np.zeros_like(x))))))
            dd["avg"] = max(dd["avg"], float(np.max(np.abs(hi.gamma_avg(x) - lo.gamma_avg(x)))))
        tx, tm, T = hi.table(); qh = Qs(vN7 * np.sqrt(np.maximum(interp2(tx, tm, T, x37, mu7), 0)), yi7); dd["dQ"] = qh - DR3[foot]["pred"][f"{GPRI:.4g}"][f]["Q_pred"]
        K7D[f"{foot}|{f}"] = dd; P(f"  K7 diagnostic [{foot}] {f:5s}: max |d gamma| par {dd['par']:.1e}, perp {dd['perp']:.1e}, avg {dd['avg']:.1e}; DR3 Q at L 96 / n_mu 128 moves {dd['dQ']:+.1e}")
RES["K7_diag"] = K7D

# ================= stage 2: g* scan =================
P("\n== Stage 2: g* scan (LOC3, LOC1), g*/a0 = 2^(k/4)")
PL = json.load(open(os.path.join(RB, "RQ3_acceptance_v2/tolerances.json")))["PLANETS"]; GMs = 1.32712440018e20; YR = 365.25 * 86400; MAS = math.pi / (180 * 3600 * 1000)
ECC = dict(Mercury=.206, Venus=.007, Earth=.017, Mars=.093, Jupiter=.048, Saturn=.054)
def rate(A, a, e, nn, N):   # CZ3 / AZ12 verbatim
    t, w = np.polynomial.legendre.leggauss(N); E = math.pi * (t + 1); c = np.cos(E); r = a * (1 - e * c)
    return math.sqrt(1 - e * e) / (nn * a * e) * float(np.sum(.5 * w * A(r) * (c - e)))
def planets(sv, a0):
    rM = math.sqrt(GMs / a0); rows = {}
    A = lambda r: -a0 * sv.spl0(np.log(r / rM)) / (r / rM) ** 2
    for nm, dd in PL.items():
        e = ECC[nm]; a = dd["a_au"] * AU; nn = math.sqrt(GMs / a ** 3); rt = rate(A, a, e, nn, 256) * YR / MAS; rows[nm] = abs(rt) / max(dd["EPM"], dd["INPOP"])
    return rows
KS = list(range(-4, 13, 2)) if QUICK else list(range(-4, 13)); SCAN = {}
# vacuum scale from CFG689 P3 (z = 0 node, kappa = 1/2 -> g* = 2 a0; alt adds rho_m from P3's omega_m)
c689 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity/CFG689_native_ruler_bao/cfg689.json")))["BAO+SN"]["P3"]; aq = np.array(c689["a0_node_q"]["0.0"]); om = np.array(c689["omega_m_q"])
cl = 2.99792458e8; rho_de = (2 * aq / cl) ** 2 / G; rho_m = om[2] * 1.87847e-26; gvac = {"canonical": 2 * aq, "alt": cl * np.sqrt(G * (rho_de + rho_m))}
for foot in A0: P(f"  g*_vac [{foot}] quantiles (2.5/16/50/84/97.5 %): " + " ".join(f"{v:.4g}" for v in gvac[foot]) + f"  (= {gvac[foot][2] / A0[foot]:.3f} a0)")
for foot, a0 in A0.items():
    rM = math.sqrt(G * MS / a0); qp = CEIL / (1.5 * a0 / rM); eta_c = eta_newton(GCAS, a0); eta_p = eta_newton(GPRI, a0); y = G * Mt / (a0 * s * s); qo, sig = DR3[foot]["Q_obs"], DR3[foot]["sigma"]
    rng = np.random.default_rng(2026110302); idx = np.repeat(np.arange(n), K); _, vN, ratio, ux, uy, uz = orbits3(rng, 1.2, n * K)
    om_ = np.random.default_rng(2026110402).uniform(0, 2 * math.pi, n * K); mu = (np.cos(om_) * ux - np.sin(om_) * uy) * GL[idx] + (np.sin(om_) * ux + np.cos(om_) * uy) * GB[idx] + uz * GN[idx]
    x3 = s[idx] * ratio / np.sqrt(G * Mt[idx] / a0); yi = y[idx]
    for f in ("LOC3", "LOC1"):
        rows = []
        for k in KS:
            gs = 2 ** (k / 4); sc = Solver(eta_c, f, gs=gs); xq = sc.q() / qp; pz = planets(sc, a0); pw = max(pz.values())
            sp = Solver(eta_p, f, gs=gs); tx, tm, T = sp.table(); qq = Qs(vN * np.sqrt(np.maximum(interp2(tx, tm, T, x3, mu), 0)), yi); z = (qo - qq) / sig
            ok = xq <= 1 and pw <= 2 and abs(z) <= 2; rows.append(dict(gs_over_a0=gs, gs=gs * a0, cassini=xq, planets_worst_Z=pw, planets=pz, Q_pred=qq, z=z, allowed=bool(ok)))
            P(f"  [{foot}] {f} g* {gs:6.3f} a0: Cassini {xq:.3g} x, planets worst Z {pw:.3g}, DR3 Q {qq:+.4f} (z {z:+.2f}) -> {'allowed' if ok else 'out'}")
        al = [r["gs"] for r in rows if r["allowed"]]; gv = gvac[foot]
        if not al: lb = "NO ALLOWED g*"
        else:
            lo_, hi_ = min(al), max(al); contig = all(r["allowed"] for r in rows if lo_ <= r["gs"] <= hi_)
            lo_open = rows[0]["allowed"]; hi_open = rows[-1]["allowed"]; inside = lo_ <= gv[1] and gv[3] <= hi_
            if not (lo_ <= gv[2] <= hi_): lb = "EXCLUDES VACUUM SCALE"
            elif (not lo_open) and (not hi_open) and hi_ / lo_ <= 4 and inside: lb = "MATCHES VACUUM SCALE"
            else: lb = "CONSISTENT, UNINFORMATIVE"
            if not contig: lb += " (allowed set not contiguous)"
        SCAN[f"{foot}|{f}"] = dict(rows=rows, label=lb, g_vac=gv.tolist(), allowed=al); P(f"  [{foot}] {f}: allowed g* {('%.3g-%.3g' % (min(al), max(al))) if al else 'none'} m/s^2 (scan 0.5-8 a0); g*_vac {gv[2]:.4g} -> {lb}")
RES["gstar"] = SCAN

# ================= finish =================
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
P(f"\nfailed checks: {len(FAILS)} {FAILS}; wall {time.time() - T0:.0f} s; peak RSS {rss:.2f} GB")
RES["failed"] = FAILS; RES["wall_s"] = time.time() - T0; RES["peak_rss_gb"] = rss
sfx = ("_MUTATE" if MUT else "") + ("_QUICK" if QUICK else "")
open(os.path.join(HERE, f"cw1{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"cw1{sfx}.json"), "w"), indent=1, default=float)
sys.exit(1 if (MUT or FAILS) else 0)
