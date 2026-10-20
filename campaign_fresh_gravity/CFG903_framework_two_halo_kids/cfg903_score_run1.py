#!/usr/bin/env python3
"""CFG903 stage C (criteria FROZEN_CRITERIA.md bb665cf4f; completeness AMENDMENT_A1.md 26ecb00ce): the framework's catalogue
two-halo term, added to CFG804/CFG902's one-halo D_der, scored with CFG804's own chi2 on B21 Fig. 3 (both footings, never pooled).
CFG804's cfg804.py is exec'd read-only (blob-checked) with CFG902's R1/R2 (declared Msun/h convention) and outputs redirected here.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -u cfg903_score.py          (main)
     CFG903_MUTATE=1 ... cfg903_score.py                               (MUTATE: neighbour M_b x 2, separate outputs)
kappa = 1/2 FITTED; not theory closed.
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import hashlib, json, math, time
import numpy as np
from scipy.integrate import quad
from scipy import stats
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg903_lib as L

MUT = os.environ.get("CFG903_MUTATE") == "1"
SFX = "_MUTATE" if MUT else ""
L.start_watchdog("CFG903 score")
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
CHK = {}
def check(name, ok, msg):
    CHK[name] = bool(ok); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")
FOOTS = ("canonical", "alt")

# ======================================================================== 1. CFG804 exec'd with CFG902 R1/R2 (+ redirect)
SRC = os.path.abspath(os.path.join(L.HERE, "..", "CFG804_catchment_supply_derived", "cfg804.py"))
BLOB = "b1749cb85e224d5a78927a061aa2832126b5b1ec"
raw = open(SRC, "rb").read(); blob = hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()
assert blob == BLOB, f"cfg804.py blob {blob} != {BLOB}"
src = raw.decode()
REPL = [("lMta = logMb - math.log10(f * FB); fn = fret_of(lMta)", "lMta = logMb - math.log10(f * FB) + SHIFT_DEX; fn = fret_of(lMta)"),
        ("abs(lk - 12.30) < 0.01", "abs(lk - (12.30 + SHIFT_DEX)) < 0.01"),
        ('os.path.join(HERE, f"cfg804_results{sfx}.json")', 'os.path.join(OUTDIR, f"cfg903_k1_cfg804exec{sfx}.json")'),
        ('os.path.join(HERE, f"cfg804{sfx}.out")', 'os.path.join(OUTDIR, f"cfg903_k1_cfg804exec{sfx}.out")')]
for a, b in REPL:
    assert src.count(a) == 1, a
    src = src.replace(a, b)
code = compile(src, "cfg804.py[CFG903 R1,R2 + redirect]", "exec")
NS = {}
os.environ.pop("CFG804_MUTATE", None)
for foot in FOOTS:
    sys.argv = [SRC] + (["alt"] if foot == "alt" else [])
    ns = dict(__name__="__main__", __file__=SRC, SHIFT_DEX=L.SHIFT_DEX, OUTDIR=L.HERE)
    try:
        exec(code, ns)
    except SystemExit:
        pass
    NS[foot] = ns
P("")
P("=" * 100)
P(f"CFG903  framework catalogue two-halo term + CFG804/CFG902 one-halo vs KiDS-1000 B21 Fig. 3" + ("   [MUTATE: neighbour M_b x 2]" if MUT else ""))
P("  criteria bb665cf4f, amendment A1 26ecb00ce; kappa = 1/2 FITTED; footings never pooled")
K1a = {}
for foot in FOOTS:
    sfx = "_alt" if foot == "alt" else ""
    ref = json.load(open(os.path.join(L.HERE, "..", "CFG902_cfg804_units_rerun", f"cfg902_results_declared{sfx}.json")))
    mine = json.load(open(os.path.join(L.HERE, f"cfg903_k1_cfg804exec{sfx}.json")))
    worst = 0.0
    for lab in ("primary", "all"):
        for k in ("chi2_B", "chi2_D", "dchi2", "p_D"):
            worst = max(worst, abs(ref[lab][k] - mine[lab][k]) / (abs(ref[lab][k]) if k == "p_D" else 1.0))
        worst = max(worst, max(abs(a - b) for a, b in zip(ref[lab]["logMb"], mine[lab]["logMb"])))
    K1a[foot] = dict(worst=worst, ok=worst <= 1e-9 and ref["cls"] == mine["cls"], ref=ref)
check("K1a exec'd CFG804 (R1/R2) reproduces CFG902 declared JSON", all(v["ok"] for v in K1a.values()),
      ", ".join(f"{f} max |d| {v['worst']:.1e}" for f, v in K1a.items()))

# ======================================================================== 2. neighbour cold-energy kernels (dimensionless, footing-free)
rho3 = lambda s: 1.0 / (2 * math.pi * s * math.sqrt(1 + 4 * s * s))
QG = np.concatenate([np.logspace(-6, math.log10(0.95), 900), np.linspace(0.95, 1.0, 201)[1:]])
XA = np.linspace(-4, 0, 81); UA = np.linspace(-5, math.log10(2.0), 141)       # region A: log xi, log upsilon (xi <= 1)
XB = np.linspace(0, 5, 101); TB = np.linspace(-1, 1, 201)                     # region B: log xi, t = upsilon - xi (xi >= 1)
def sigma_profile(smax):                      # projected truncated law (units M_b / r_M^2), at s = q * smax
    out = np.empty(len(QG))
    for i, q in enumerate(QG):
        R = q * smax; tm = math.sqrt(max(smax * smax - R * R, 0.0))
        out[i] = 2 * quad(lambda t: rho3(math.hypot(R, t)), 0, tm, limit=300)[0] if tm > 0 else 0.0
    return out
def frac_inside(sig, xi, up):                 # fraction of the profile inside a circle of radius xi about a point at offset up (units smax')
    xi = np.atleast_1d(xi); up = np.atleast_1d(up)
    q = QG[None, :]
    with np.errstate(divide="ignore", invalid="ignore"):
        arg = (q * q + 2 * xi[:, None] * (up - xi)[:, None] + ((up - xi) ** 2)[:, None]) / (2 * q * up[:, None])
    arg = np.where(up[:, None] > 0, arg, np.where(q < xi[:, None], -2.0, 2.0))
    phi = np.arccos(np.clip(arg, -1, 1))
    g = sig[None, :] * q * phi
    num = np.sum(0.5 * (g[:, 1:] + g[:, :-1]) * np.diff(QG)[None, :], axis=1)
    gn = sig * QG; den = math.pi * np.sum(0.5 * (gn[1:] + gn[:-1]) * np.diff(QG))
    return num / den
def build_table(sig):
    TA = np.empty((len(XA), len(UA))); TBt = np.empty((len(XB), len(TB)))
    for i, lx in enumerate(XA):
        xi = 10 ** lx; up = 10 ** UA
        v = frac_inside(sig, np.full(len(up), xi), up); v[up >= xi + 1] = 0.0; TA[i] = v
    for i, lx in enumerate(XB):
        xi = 10 ** lx; up = xi + TB
        TBt[i] = frac_inside(sig, np.full(len(up), xi), up)
    return TA, TBt
def F_eval(tab, xi, up):                      # bilinear in the tables; exact limits outside
    TA, TBt = tab
    xi = np.asarray(xi, float); up = np.asarray(up, float); out = np.zeros(np.broadcast(xi, up).shape)
    xi, up = np.broadcast_to(xi, out.shape), np.broadcast_to(up, out.shape)
    lx = np.log10(np.maximum(xi, 1e-300))
    b = xi >= 1.0
    t = up - xi
    inner = b & (t <= -1); out[inner] = 1.0
    mb = b & (t > -1) & (t < 1)
    if mb.any():
        fx = (np.clip(lx[mb], XB[0], XB[-1]) - XB[0]) / (XB[1] - XB[0]); ix = np.minimum(fx.astype(int), len(XB) - 2); wx = fx - ix
        ft = (t[mb] - TB[0]) / (TB[1] - TB[0]); it = np.minimum(ft.astype(int), len(TB) - 2); wt = ft - it
        out[mb] = ((1 - wx) * (1 - wt) * TBt[ix, it] + wx * (1 - wt) * TBt[ix + 1, it] + (1 - wx) * wt * TBt[ix, it + 1] + wx * wt * TBt[ix + 1, it + 1])
    ma = (~b) & (up < xi + 1)
    if ma.any():
        fx = (np.clip(lx[ma], XA[0], XA[-1]) - XA[0]) / (XA[1] - XA[0]); ix = np.minimum(fx.astype(int), len(XA) - 2); wx = fx - ix
        lu = np.log10(np.maximum(up[ma], 10 ** UA[0]))
        fu = (np.clip(lu, UA[0], UA[-1]) - UA[0]) / (UA[1] - UA[0]); iu = np.minimum(fu.astype(int), len(UA) - 2); wu = fu - iu
        out[ma] = ((1 - wx) * (1 - wu) * TA[ix, iu] + wx * (1 - wu) * TA[ix + 1, iu] + (1 - wx) * wu * TA[ix, iu + 1] + wx * wu * TA[ix + 1, iu + 1])
    return out
t0 = time.time()
TABS = {}; SIGS = {}
for N in L.NGRID_NB:
    sm = L.edge_of(float(N))
    for shape, fac in (("P1", 1.0), ("P2", 2.0)):
        sig = sigma_profile(fac * sm); SIGS[(float(N), shape)] = sig; TABS[(float(N), shape)] = build_table(sig)
P(f"\n  kernel tables: {len(TABS)} (N in NGRID u {{1.25,1.5,1.75}}, shapes P1/P2) built in {time.time() - t0:.0f} s")

# K2a: our projected profile reproduces CFG804's one-halo f(X)
ns0 = NS["canonical"]; X = ns0["X"]; worst2a = 0.0
for N in (1.0, 5.5, 10.0):
    sm = L.edge_of(N); f804 = ns0["profile"](sm)
    tab, sig = TABS[(N, "P1")], SIGS[(N, "P1")]
    m = (X >= 0.01) & (X <= 0.95 * sm)
    Mc = (math.sqrt(0.25 + sm * sm) - 0.5) * F_eval(tab, X[m] / sm, np.zeros(m.sum()))
    Sg = np.interp(X[m] / sm, QG, sig)
    fm = Mc / (math.pi * X[m] ** 2) - Sg + 1.0 / (math.pi * X[m] ** 2)
    worst2a = max(worst2a, float(np.max(np.abs(fm / f804[m] - 1))))
check("K2a projected cold profile vs CFG804 profile() (N 1, 5.5, 10)", worst2a <= 5e-3, f"max relative difference {worst2a:.2e} (<= 5e-3)")
# K2b: limits by direct integration, and F(x, 0) vs a refined direct integration
lim = 0.0; dz = 0.0
for N in (1.0, 10.0):
    sig = SIGS[(N, "P1")]
    for xi in (1.0, 3.0, 100.0, 1e4):
        lim = max(lim, abs(float(frac_inside(sig, np.array([xi]), np.array([xi - 1.0]))[0]) - 1), abs(float(frac_inside(sig, np.array([xi]), np.array([xi + 1.0]))[0])))
    for xi in (0.01, 0.1, 0.5, 0.9):
        cum = np.concatenate([[0.0], np.cumsum(0.5 * (sig[1:] * QG[1:] + sig[:-1] * QG[:-1]) * np.diff(QG))])
        direct = float(np.interp(xi, QG, cum) / cum[-1])
        dz = max(dz, abs(float(F_eval(TABS[(N, "P1")], np.array([xi]), np.array([0.0]))[0]) - direct))
check("K2b kernel limits (inside 1, outside 0) and F(x, 0)", lim <= 1e-6 and dz <= 1e-3, f"limits max |d| {lim:.1e} (<= 1e-6); F(x,0) vs direct {dz:.1e} (<= 1e-3)")

# ======================================================================== 3. bin-averaged kernels K[m, d, b] (Msun/pc^2 per Msun of neighbour M_b)
RB = L.B21_EDGES; NBIN = 15
GLX, GLW = np.polynomial.legendre.leggauss(16)
LN1, LN2 = np.log(RB[:-1]), np.log(RB[1:])
RN = np.exp(0.5 * (LN2 - LN1)[:, None] * GLX[None, :] + 0.5 * (LN2 + LN1)[:, None])     # (15, 16) nodes
WN = 0.5 * (LN2 - LN1)[:, None] * GLW[None, :]                                          # d ln R weights
AREA = math.pi * (RB[1:] ** 2 - RB[:-1] ** 2) * 1e12                                    # pc^2
DREP = np.concatenate([[0.0015], np.sqrt(L.D_EDGES[1:-1] * L.D_EDGES[2:])])            # representative d per d bin (Mpc)
def point_I(d):                                   # per unit point mass: [int 2 Theta(d<R)/R dR - Delta M] over each B21 bin
    d = np.asarray(d)[:, None]; R1, R2 = RB[None, :-1], RB[None, 1:]
    return np.where(d < R2, 2 * np.log(R2 / np.maximum(R1, d)), 0.0) - ((d >= R1) & (d < R2))
IB = point_I(DREP)                                                                       # (240, 15)
def kernel(foot, shape, mut=False):
    a0 = L.a0_kms2pc(foot); K = np.empty((L.NM, L.ND, NBIN))
    for c in range(L.NM):
        lm = L.M_CEN[c] + (math.log10(2.0) if mut else 0.0)
        Nc = L.N_of_declared(lm); cold = L.SUP * Nc
        if shape == "P0":
            K[c] = (1 + cold) * IB
        else:
            Ns = float(L.NGRID_NB[np.argmin(np.abs(L.NGRID_NB - Nc))]); sp = L.edge_of(Ns) * (2.0 if shape == "P2" else 1.0)
            rM = math.sqrt(L.Gpc * 10 ** lm / a0) / 1e6; scale = rM * sp                   # Mpc
            tab = TABS[(Ns, shape)]
            up = (DREP / scale)[:, None, None]
            Fn = F_eval(tab, (RN / scale)[None, :, :], up)                                   # (240, 15, 16)
            F1 = F_eval(tab, (RB[:-1] / scale)[None, :], up[:, :, 0]); F2 = F_eval(tab, (RB[1:] / scale)[None, :], up[:, :, 0])
            K[c] = IB + cold * (np.sum(2 * Fn * WN[None], axis=2) - (F2 - F1))
        if mut:
            K[c] *= 2.0
    return K / AREA[None, None, :]
# K2c: synthetic uniform field -> Delta Sigma = 0
k2c = 0.0
for foot in FOOTS:
    Kc = kernel(foot, "P1")
    for lm in (10.5, 12.0):
        c = int(L.mbin_of(np.array([lm]))[0]); ann = math.pi * (L.D_EDGES[1:] ** 2 - L.D_EDGES[:-1] ** 2) * 1e12     # pc^2 per d bin
        sig0 = 1.0; H = sig0 * ann                                                        # Msun per d bin (Sigma0 = 1 Msun/pc^2 of M_b)
        dsig = H @ Kc[c]; tot = sig0 * (1 + L.SUP * L.N_of_declared(L.M_CEN[c]))
        k2c = max(k2c, float(np.max(np.abs(dsig))) / tot)
check("K2c uniform neighbour field gives Delta Sigma = 0 (log M_b 10.5, 12.0; P1; both footings)", k2c <= 2e-3, f"max |DS| / Sigma0 = {k2c:.1e} (<= 2e-3)")

# ======================================================================== 4. histograms -> two-halo vectors
HIST = [np.load(os.path.join(L.WORK, f"cfg903_hist_bin{b + 1}.npz")) for b in range(4)]
SH = (L.ND, L.NM, 2, L.NW, 2)
EIDX = np.where((L.D_EDGES >= 0.05) & (L.D_EDGES <= 3.0))[0]; EX = L.D_EDGES[EIDX]                 # exclusion radii on d-bin edges
WUP = {100: 1, 200: 2, 300: 3, 500: 4, 1000: 5}
def Dsel(b, v, W, mask, sample=None):
    h = HIST[b]; norm = float(h["NORM"][v])
    hl = h["HL"][v].reshape(SH)[:, :, :, :WUP[W], :]; hr = h["HR"][v].reshape(SH)[:, :, :, :WUP[W], :]
    if mask == "M0":
        hl, hr = hl[..., 0], hr[..., 0]
    else:
        hl, hr = hl.sum(axis=-1), hr.sum(axis=-1)
    hl, hr = hl.sum(axis=3), hr.sum(axis=3)                                                 # (d, m, flag)
    if sample == "lens": return hl / norm
    if sample == "random": return hr / norm
    return (hl - hr) / norm
def twoh_table(D, K, excl):
    """D (d, m, flag) -> T_all (15,), T_ex (len(EX), 15): two-halo with exclusion of cells d < EX[e] (flag 1 for E1, both for E2)."""
    G = np.einsum("dmf,mdb->dfb", D, K)                                                    # (d, flag, 15)
    Tall = G.sum(axis=(0, 1))
    if excl == "E0": return Tall, np.repeat(Tall[None], len(EX), axis=0)
    Gx = G[:, 1, :] if excl == "E1" else G.sum(axis=1)
    cum = np.concatenate([np.zeros((1, NBIN)), np.cumsum(Gx, axis=0)])                     # cum[i] = sum over d bins < i
    return Tall, Tall[None, :] - cum[EIDX]
def T_at(Tex, rx):
    lx = np.log(EX); x = math.log(min(max(rx, EX[0]), EX[-1]))
    i = min(int(np.searchsorted(lx, x) - 1), len(EX) - 2); i = max(i, 0); w = (x - lx[i]) / (lx[i + 1] - lx[i])
    return (1 - w) * Tex[i] + w * Tex[i + 1]
VMAP = {"v0": 0, "C0": 1, "C2p": 2, "uniform": 3, "I1": 4, "I2": 5, "I5": 6, "z017": 7}
PRIMARY = dict(v="v0", W=500, mask="M0", excl="E1", shape="P1")
BRACKETS = [("C0 (no completeness)", dict(v="C0")), ("C2' (whole-sum completeness)", dict(v="C2p")),
            ("W300", dict(W=300)), ("W1000", dict(W=1000)), ("I1 (f30 isolation)", dict(v="I1")), ("I2 (physical 3 Mpc)", dict(v="I2")),
            ("I5 (count-matched W 6.1)", dict(v="I5")), ("P0 (point cold energy)", dict(shape="P0")), ("P2 (diffuse cold energy)", dict(shape="P2")),
            ("E0 (no exclusion)", dict(excl="E0")), ("E2 (all within r_x dropped)", dict(excl="E2")), ("uniform weights", dict(v="uniform")),
            ("M1 (masked objects added)", dict(mask="M1"))]
REPORTED = [("W100 (reported)", dict(W=100)), ("W200 (reported)", dict(W=200)), ("v7 z_l >= 0.17 (A1 diagnostic)", dict(v="z017"))]
KCACHE = {}
def getK(foot, shape):
    key = (foot, shape, MUT)
    if key not in KCACHE: KCACHE[key] = kernel(foot, shape, MUT)
    return KCACHE[key]
def T_tables(foot, spec):
    s = dict(PRIMARY); s.update(spec); K = getK(foot, s["shape"])
    return [twoh_table(Dsel(b, VMAP[s["v"]], s["W"], s["mask"]), K, s["excl"]) for b in range(4)]

# ======================================================================== 5. CFG804's chi2 with the two-halo term (fits)
def make_fitter(foot):
    ns = NS[foot]; Y, R, C, model, GRID, ZK, N_of, NG = ns["Y"], ns["R"], ns["C"], ns["model"], ns["GRID"], ns["ZK"], ns["N_of"], ns["NGRID"]
    a0 = ns["a0"]; Gpc = ns["Gpc"]; edge = ns["edge_of"]
    def rx_of(lm):
        N = N_of(lm)[0]; Nn = float(NG[np.argmin(abs(NG - N))]); return edge(Nn) * math.sqrt(Gpc * 10 ** lm / a0) / 1e6
    def chi2(fsel, Lm, idx, T=None):
        yv = np.concatenate([Y[b] for b in range(4)])
        if T is None:
            mv = np.concatenate([model(fsel(Lm[b]), Lm[b], R[b]) for b in range(4)])
        else:
            mv = np.concatenate([model(fsel(Lm[b]), Lm[b], R[b]) + T(b, Lm[b]) for b in range(4)])
        sel = np.concatenate([np.array(idx) + 15 * b for b in range(4)]); r = (yv - mv)[sel]
        if not np.all(np.isfinite(r)): return float("inf")
        with np.errstate(all="ignore"): x2 = float(r @ np.linalg.solve(C[np.ix_(sel, sel)], r))
        return x2 if np.isfinite(x2) else float("inf")
    def fit(fsel, idx, T=None):
        Lm = list(ZK)
        for _ in range(3):
            for b in range(4):
                Lm[b] = float(min(GRID, key=lambda g: chi2(fsel, Lm[:b] + [g] + Lm[b + 1:], idx, T)))
        return Lm, chi2(fsel, Lm, idx, T)
    def Tfun(tabs, amp=1.0):
        cache = {}
        def T(b, lm):
            key = (b, round(lm, 6))
            if key not in cache: cache[key] = amp * T_at(tabs[b][1], rx_of(lm))
            return cache[key]
        return T
    return dict(chi2=chi2, fit=fit, Tfun=Tfun, rx_of=rx_of, fsB=ns["fsB"], fsD=ns["fsD"], prim=ns["prim"], full=ns["full"], N_of=N_of)
FIT = {f: make_fitter(f) for f in FOOTS}
REF902 = {f: K1a[f]["ref"] for f in FOOTS}
SHORT = {f: REF902[f]["all"]["dchi2"] for f in FOOTS}
def classify(d, foot):
    if d <= 4: return "TWO-HALO CLOSES"
    if d <= 0.5 * SHORT[foot]: return "PARTIAL"
    return "DOES NOT CLOSE" + (" (WORSENS)" if d > SHORT[foot] else "")
def score(foot, tabs, both=True, amp=1.0):
    F = FIT[foot]; T = F["Tfun"](tabs, amp); out = {}
    for lab, idx in (("all", F["full"]),) + ((("primary", F["prim"]),) if both else ()):
        Lm, cD = F["fit"](F["fsD"], idx, T); cB = REF902[foot][lab]["chi2_B"]
        out[lab] = dict(chi2_D2h=cD, chi2_B=cB, dchi2=cD - cB, logMb=Lm, rx_Mpc=[F["rx_of"](x) for x in Lm],
                        p=float(stats.chi2.sf(cD, 4 * len(idx) - 4)))
    return out

# K1b: two-halo = 0 reproduces CFG902 through this lane's own fitter
k1b = 0.0
for foot in FOOTS:
    F = FIT[foot]
    for lab, idx in (("all", F["full"]), ("primary", F["prim"])):
        Lm, cD = F["fit"](F["fsD"], idx, F["Tfun"]([(np.zeros(15), np.zeros((len(EX), 15)))] * 4))
        ref = REF902[foot][lab]
        k1b = max(k1b, abs(cD - ref["chi2_D"]), abs((cD - ref["chi2_B"]) - ref["dchi2"]), max(abs(a - b) for a, b in zip(Lm, ref["logMb"])))
check("K1b this lane's D+2h fit with two-halo = 0 reproduces CFG902 (both footings, both radius sets)", k1b <= 1e-9,
      f"max |d| {k1b:.1e}; all radii +{SHORT['canonical']:.2f} / +{SHORT['alt']:.2f}, primary {REF902['canonical']['primary']['dchi2']:+.2f} / {REF902['alt']['primary']['dchi2']:+.2f}")

# ======================================================================== 6. primary, brackets, diagnostics
RES = dict(lane="CFG903", mutate=MUT, criteria="bb665cf4f", amendment="26ecb00ce", checks=CHK, footings={})
Rv = NS["canonical"]["R"][0]
for foot in FOOTS:
    P(f"\n{'-' * 100}\n  FOOTING {foot} (a0 {L.A0[foot]:.4e}); CFG902 reference: all radii {SHORT[foot]:+.2f}, primary {REF902[foot]['primary']['dchi2']:+.2f}")
    FR = dict()
    tabs = T_tables(foot, {})
    sc = score(foot, tabs)
    a, p_ = sc["all"], sc["primary"]
    cls = classify(a["dchi2"], foot)
    P(f"  PRIMARY (I0, W500, C1', P1, E1, unmasked, B21 weights):")
    P(f"    all radii: chi2(D+2h) {a['chi2_D2h']:.2f} (p {a['p']:.2e}) vs chi2_B {a['chi2_B']:.2f} -> dchi2 {a['dchi2']:+.2f}  ==> {cls}")
    P(f"      masses log M_b " + " / ".join(f"{x:.2f}" for x in a["logMb"]) + "; exclusion edges r_x " + " / ".join(f"{1e3 * x:.0f}" for x in a["rx_Mpc"]) + " kpc")
    P(f"    primary R <= 0.31: dchi2 {p_['dchi2']:+.2f} -> {'SUFFICES still' if p_['dchi2'] <= 4 else 'NO LONGER SUFFICES'} (chi2 {p_['chi2_D2h']:.2f})")
    FR["primary"] = dict(score=sc, cls=cls)
    # two-halo vectors at the primary all-radii masses
    Tv = [T_at(tabs[b][1], a["rx_Mpc"][b]) for b in range(4)]
    FR["T2h_primary"] = [t.tolist() for t in Tv]
    P("    two-halo Delta Sigma (Msun/pc^2) at R = " + ", ".join(f"{x:.2f}" for x in Rv[[6, 8, 10, 11, 12, 13, 14]]) + " Mpc:")
    for b in range(4):
        y = NS[foot]["Y"][b]; dmod = NS[foot]["model"](NS[foot]["fsD"](a["logMb"][b]), a["logMb"][b], NS[foot]["R"][b])
        P(f"      bin {b + 1}: 2h " + " ".join(f"{Tv[b][i]:6.3f}" for i in (6, 8, 10, 11, 12, 13, 14)) + "   | data - D_1h " + " ".join(f"{(y - dmod)[i]:6.3f}" for i in (6, 8, 10, 11, 12, 13, 14)))
    # host share and random-only signal
    K = getK(foot, "P1"); hs, ro = [], []
    for b in range(4):
        D = Dsel(b, 0, 500, "M0")
        Gf = np.einsum("dmf,mdb->fb", D, K)
        Tr = np.einsum("dmf,mdb->b", Dsel(b, 0, 500, "M0", "random"), K)
        hs.append(float(Gf[0, 11] / max(Gf.sum(axis=0)[11], 1e-30))); ro.append(Tr.tolist())
    FR["host_share_R1.04_noexcl"] = hs; FR["random_only_T"] = ro
    P("    share of the (unexcluded) 2h at 1.04 Mpc from neighbours MORE massive than the lens: " + " / ".join(f"{x:.2f}" for x in hs))
    P("    random-only signal (mask/edge term, subtracted) at 0.41 / 1.04 / 2.60 Mpc, bin 1-4: " + "; ".join(f"{r[8]:.3f}/{r[11]:.3f}/{r[14]:.3f}" for r in ro))
    if MUT:
        RES["footings"][foot] = FR; continue
    # brackets
    P("  BRACKETS (one at a time; class on all radii; primary-range dchi2):")
    FR["brackets"] = {}
    for lab, spec in BRACKETS + REPORTED:
        s2 = score(foot, T_tables(foot, spec)); c2 = classify(s2["all"]["dchi2"], foot)
        FR["brackets"][lab] = dict(score=s2, cls=c2)
        flag = "" if c2 == cls else "   <== CLASS CHANGES"
        P(f"    {lab:34s} all {s2['all']['dchi2']:+8.2f} -> {c2:28s} primary {s2['primary']['dchi2']:+7.2f}{flag}")
    # jackknife (primary, all radii)
    h0 = [HIST[b] for b in range(4)]; dj = []
    for pt in range(L.NPATCH):
        tj = []
        for b in range(4):
            hl, hr = h0[b]["HJL"].reshape(L.NPATCH, L.ND, L.NM, 2), h0[b]["HJR"].reshape(L.NPATCH, L.ND, L.NM, 2)
            nl, nr = h0[b]["NJL"], h0[b]["NJR"]
            D = (hl.sum(0) - hl[pt]) / (nl.sum() - nl[pt]) - (hr.sum(0) - hr[pt]) / (nr.sum() - nr[pt])
            tj.append(twoh_table(D, K, "E1"))
        dj.append(score(foot, tj, both=False)["all"]["dchi2"])
    dj = np.array(dj); sjk = float(math.sqrt((L.NPATCH - 1) / L.NPATCH * np.sum((dj - dj.mean()) ** 2)))
    near = abs(a["dchi2"] - 4) < 2 * sjk or abs(a["dchi2"] - 0.5 * SHORT[foot]) < 2 * sjk
    FR["jackknife"] = dict(dchi2_delete_one=dj.tolist(), sigma=sjk, near_threshold=bool(near))
    P(f"  JACKKNIFE (50 patches, delete-one, refit): sigma(dchi2_all) = {sjk:.2f}; threshold within 2 sigma: {near}")
    # amplitude scan (reported only)
    AS = np.round(np.arange(0.0, 6.0001, 0.1), 1); dA = []
    for A in AS:
        dA.append(score(foot, tabs, both=False, amp=float(A))["all"]["dchi2"])
    dA = np.array(dA); ib = int(np.argmin(dA)); ok = AS[dA <= 4]
    FR["amp_scan"] = dict(A=AS.tolist(), dchi2=dA.tolist(), A_best=float(AS[ib]), dchi2_best=float(dA[ib]),
                          A_range_le4=[float(ok.min()), float(ok.max())] if len(ok) else None)
    P(f"  AMPLITUDE SCAN (reported only): A_best {AS[ib]:.1f} (dchi2 {dA[ib]:+.2f}); A with dchi2 <= 4: " + (f"{ok.min():.1f}-{ok.max():.1f}" if len(ok) else "none in 0-6"))
    RES["footings"][foot] = FR

# ======================================================================== 7. K3 random halves (primary selection, E1 at CFG902 all-radii masses), MUTATE bite
if not MUT:
    foot = "canonical"; K = getK(foot, "P1"); F = FIT[foot]
    diffs, wts, jk = [], [], np.zeros(L.NPATCH)
    Cd = np.diag(NS[foot]["C"]); sel_out = [i for i in range(15) if Rv[i] >= 0.4]
    tot = 0.0; wsum = 0.0; tj = np.zeros(L.NPATCH); wj = 0.0
    for b in range(4):
        h = HIST[b]; rx = F["rx_of"](REF902[foot]["all"]["logMb"][b])
        hr = h["HR"][0].reshape(SH)[:, :, :, :4, 0].sum(axis=3); ha = h["HA"].reshape(SH)[:, :, :, :4, 0].sum(axis=3)
        nA = float(h["NA"]); nB = float(h["NORM"][0]) - nA
        DA_ = ha / nA - (hr - ha) / nB
        TA_ = T_at(twoh_table(DA_, K, "E1")[1], rx)
        w = 1.0 / Cd[15 * b + np.array(sel_out)]
        tot += float(np.sum(w * TA_[sel_out])); wsum += float(np.sum(w))
        hjr, hja = h["HJR"].reshape(L.NPATCH, L.ND, L.NM, 2), h["HJA"].reshape(L.NPATCH, L.ND, L.NM, 2)
        njr, nja = h["NJR"], h["NJA"]
        for pt in range(L.NPATCH):
            a_ = (hja.sum(0) - hja[pt]) / (nja.sum() - nja[pt]); bb = ((hjr.sum(0) - hjr[pt]) - (hja.sum(0) - hja[pt])) / ((njr.sum() - njr[pt]) - (nja.sum() - nja[pt]))
            tj[pt] += float(np.sum(w * T_at(twoh_table(a_ - bb, K, "E1")[1], rx)[sel_out]))
    mean = tot / wsum; tj /= wsum
    sj = float(math.sqrt((L.NPATCH - 1) / L.NPATCH * np.sum((tj - tj.mean()) ** 2)))
    check("K3 random halves A - B consistent with zero (28 outer points, inverse-variance mean)", abs(mean) <= 3 * sj,
          f"mean {mean:+.4f} Msun/pc^2, sigma_jk {sj:.4f} ({mean / sj:+.2f} sigma)")
    RES["K3"] = dict(mean=mean, sigma_jk=sj)
else:
    main = json.load(open(os.path.join(L.HERE, "cfg903_results.json")))
    bite = {}
    for foot in FOOTS:
        d0 = main["footings"][foot]["primary"]["score"]["all"]["dchi2"]; d1 = RES["footings"][foot]["primary"]["score"]["all"]["dchi2"]
        bite[foot] = dict(primary=d0, mutate=d1, change=d1 - d0, bites=abs(d1 - d0) >= 1.0)
    check("MUTATE neighbour M_b x 2 moves the all-radii dchi2 by >= 1 (both footings)", all(v["bites"] for v in bite.values()),
          ", ".join(f"{f}: {v['primary']:+.2f} -> {v['mutate']:+.2f} ({v['change']:+.2f})" for f, v in bite.items()))
    RES["mutate_bite"] = bite

# ======================================================================== 8. verdict
P(f"\n{'=' * 100}\n  VERDICT" + (" (MUTATE run: not a verdict)" if MUT else ""))
for foot in FOOTS:
    FR = RES["footings"][foot]; c = FR["primary"]["cls"]
    flips = [k for k, v in FR.get("brackets", {}).items() if v["cls"] != c and "reported" not in k and "diagnostic" not in k]
    P(f"  {foot}: {c} (all-radii dchi2 {FR['primary']['score']['all']['dchi2']:+.2f}; CFG902 {SHORT[foot]:+.2f})"
      + ("" if MUT else ("; robust across brackets" if not flips else "; class changes under: " + ", ".join(flips))))
    FR["class_flips"] = flips
P(f"  checks: " + ", ".join(f"{k.split()[0]} {'PASS' if v else 'FAIL'}" for k, v in CHK.items()))
P("  kappa = 1/2 FITTED; footings never pooled; framework-native neighbours (no LCDM halo model); not theory closed.")
RES.update(runtime_s=round(time.time() - L.T0, 1), peak_current_rss_MB=round(L.PEAK_CUR[0] / 1e6, 1))
json.dump(RES, open(os.path.join(L.HERE, f"cfg903_results{SFX}.json"), "w"), indent=1, default=float)
open(os.path.join(L.HERE, f"cfg903_score{SFX}.out"), "w").write("\n".join(OUT) + "\n")
P(f"  runtime {time.time() - L.T0:.0f} s; peak current RSS {L.PEAK_CUR[0] / 1e6:.0f} MB")
sys.exit(0 if all(CHK.values()) else 1)
