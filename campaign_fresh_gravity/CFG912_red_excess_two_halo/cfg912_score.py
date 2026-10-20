#!/usr/bin/env python3
"""CFG912 stage C (criteria FROZEN_CRITERIA.md, 96de8091f): the framework's catalogue two-halo term per colour class on B21's
g_bar bins, and how much of the red/blue amplitude split (CFG850) it explains.  Both footings, never pooled.
CFG850's definitions (cfg829 load/amp/nu_e, window, files) and CFG903's kernel definitions (profiles, F2, brute) are exec'd
read-only from their committed sources.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -u cfg912_score.py              (main)
     CFG912_MUTATE=1 ... cfg912_score.py                                  (MUTATE: injected red-only hosts; needs the main JSON)
     CFG912_MUTATE=B ... cfg912_score.py                                  (MUTATE-B, AMENDMENT_A1.md; needs main + MUTATE JSON)
kappa = 1/2 FITTED; not theory closed.
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import hashlib, json, math, time
import numpy as np
from scipy.integrate import quad
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg912_lib as C
L = C.L

MUT = C.MUT_MODE != ""; SFX = C.MUT_SFX                                # A1: CFG912_MUTATE=B -> MUTATE-B
L.start_watchdog("CFG912 score" + SFX)
OUT = []; CHK = {}
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
def check(name, ok, msg):
    CHK[name] = bool(ok); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")
FOOTS = ("canonical", "alt")
LANES = os.path.dirname(C.HERE)
def blob(path):
    raw = open(path, "rb").read(); return hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()

P("=" * 110)
P("CFG912  red/blue isolated-lens split vs the framework's catalogue two-halo term (CFG903 machinery) on B21's g_bar bins"
  + ("   [MUTATE: injected red-only hosts]" if MUT else ""))
P("  criteria 96de8091f; kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled")

# ============================================================== 1. CFG850 definitions (exec'd read-only) and K1
P850 = os.path.join(LANES, "CFG850_red_split_mstar_systematic", "cfg850.py")
for _v in ("CFG850_MUTATE", "CFG829_MUTATE"):
    os.environ.pop(_v, None)
src850 = open(P850).read(); assert src850.count("\nVAR = ") == 1
N850 = {"__file__": P850, "__name__": "cfg850_defs"}
exec(compile(src850.split("\nVAR = ")[0], "cfg850.py[definitions]", "exec"), N850)
load, amp, nu_e, A0, WIN, F850 = N850["load"], N850["amp"], N850["nu_e"], N850["A0"], N850["W"], N850["F"]
G_pc, PCm = N850["M"]["G_pc"], N850["M"]["PCm"]
assert A0 == L.A0
P(f"  cfg850.py blob {blob(P850)[:12]} (definitions exec'd), cfg829.py blob {blob(N850['M']['__file__'])[:12]}")
DATA = {k: load(*F850[k]) for k in ("red", "blue", "sph", "disc")}
GB0 = DATA["red"][0]
for k in DATA:
    assert np.array_equal(DATA[k][0], GB0)
KFILE = np.floor((np.log10(GB0) + 15.0) / C.DLG).astype(int)
assert len(GB0) == 15 and np.array_equal(KFILE, np.arange(15)), "file g_bar not one per nominal bin"
def amp_c(key, foot, sh, dg=None):
    gb, go, Cv = DATA[key]; gbs = gb * 10 ** sh; gl = gbs * nu_e(gbs / A0[foot])
    return amp(gbs, go if dg is None else go - dg, Cv, gl, WIN), gl
def win_idx(sh):
    gbs = GB0 * 10 ** sh; return np.where((gbs >= WIN[0]) & (gbs < WIN[1]))[0]
REF850 = json.load(open(os.path.join(LANES, "CFG850_red_split_mstar_systematic", "cfg850_results.json")))
k1 = 0.0; nrow = 0
for foot in FOOTS:
    for sr, sb in ((0.0, 0.0), (0.123, 0.0), (0.2, 0.0), (0.123, 0.05), (0.2, 0.05)):
        r, _ = amp_c("red", foot, sr); b, _ = amp_c("blue", foot, sb); s, _ = amp_c("sph", foot, sr); d, _ = amp_c("disc", foot, sb)
        mine = dict(A_red=r["A"], A_blue=b["A"], z_colour=(r["A"] - b["A"]) / math.hypot(r["sA"], b["sA"]),
                    A_sph=s["A"], A_disc=d["A"], z_sersic=(s["A"] - d["A"]) / math.hypot(s["sA"], d["sA"]))
        ref = REF850["rows"][f"{foot}|{sr}|{sb}"]
        k1 = max(k1, max(abs(mine[q] - ref[q]) for q in mine)); nrow += 1
check("K1 two-halo = 0 reproduces CFG850's committed rows", k1 == 0.0 and nrow == 10, f"{nrow} rows x 6 quantities, max |d| = {k1:.1e}")
for sh in (0.0, 0.05, 0.123, 0.2):
    assert set(win_idx(sh)) <= set(C.KB.tolist()), sh

# ============================================================== 2. CFG903 kernel definitions (exec'd read-only)
P903 = os.path.join(C.D903, "cfg903_score.py")
s903 = open(P903).read()
ia, ib = s903.index("rho3 = lambda"), s903.index("t0 = time.time()\nPROFS = {}")
N903 = dict(np=np, math=math, quad=quad, __name__="cfg903_kernel_defs")
exec(compile(s903[ia:ib], "cfg903_score.py[kernel definitions]", "exec"), N903)
sigma_profile, prof, F2, brute = N903["sigma_profile"], N903["prof"], N903["F2"], N903["brute"]
P(f"  cfg903_score.py blob {blob(P903)[:12]} (profile / F2 / brute definitions exec'd); cfg903_lib.py blob {blob(os.path.join(C.D903, 'cfg903_lib.py'))[:12]}")
t0 = time.time(); PROFS = {}
for N in L.NGRID_NB:
    sm = L.edge_of(float(N))
    for shape, fac in (("P1", 1.0), ("P2", 2.0)):
        PROFS[(float(N), shape)] = prof(sigma_profile(fac * sm))
P(f"  neighbour profiles: {len(PROFS)} in {time.time() - t0:.0f} s")

COLD = np.array([L.SUP * L.N_of_declared(float(lm)) for lm in C.NM_CEN])
NMC_CEN = 8.5 + 0.2 * (np.arange(C.NNMC) + 0.5)               # jackknife coarse neighbour cells (0.2 dex)
COLD_C = np.array([L.SUP * L.N_of_declared(float(lm)) for lm in NMC_CEN])
def nb_scale(lm, foot, shape):
    Nc = L.N_of_declared(float(lm))
    Ns = float(L.NGRID_NB[np.argmin(np.abs(L.NGRID_NB - Nc))]); sp = L.edge_of(Ns) * (2.0 if shape == "P2" else 1.0)
    return Ns, math.sqrt(L.Gpc * 10 ** lm / L.a0_kms2pc(foot)) / 1e6 * sp                       # CFG903 kernel(): rM * sp (Mpc)
RHO_L = C.rho_Mpc(10 ** C.LM_CEN)

# ============================================================== 3. kernels in x = d / rho_l
XE = {"nom": C.X_of_k(np.arange(5, 15)).astype(float)}                       # X edges of g_5..g_14 (decreasing)
gmid = np.sqrt(GB0[:-1] * GB0[1:])                                            # file-centred g edges (geometric midpoints)
XE["file"] = np.sqrt(C.G_REF / gmid[4:14])                                    # edges of bins 5..13: midpoints (4,5)..(13,14)
DX2 = {t: XE[t][:-1] ** 2 - XE[t][1:] ** 2 for t in XE}                       # (9,) outer^2 - inner^2
XED = {"fine": C.X_EDGES, "coarse": np.minimum(C.XC_EDGES, C.X_EDGES[-1])}
def pt_avg(X1, X2, a, b):                       # area-average over [a, b] of 2 ln(X2/max(X1,x)) 1(x<X2) - 1(X1<=x<X2)
    tot = 0.0; lo, hi = a, min(b, X1)
    if hi > lo: tot += 2 * math.log(X2 / X1) * (hi * hi - lo * lo)
    lo, hi = max(a, X1), min(b, X2)
    if hi > lo: tot += 2 * (hi * hi * math.log(X2 / hi) - lo * lo * math.log(X2 / lo))
    return tot / (b * b - a * a)
IPT = {(et, xt): np.array([[pt_avg(XE[et][j + 1], XE[et][j], XED[xt][i], XED[xt][i + 1]) for i in range(len(XED[xt]) - 1)]
                           for j in range(9)]) for et in XE for xt in XED}
GLN, GLW = np.polynomial.legendre.leggauss(4)
def xnodes(edges):                              # area-uniform Gauss-Legendre nodes in x^2 per bin; weights sum to 1
    a2, b2 = edges[:-1] ** 2, edges[1:] ** 2
    s = 0.5 * (b2 - a2)[:, None] * (GLN[None, :] + 1) + a2[:, None]
    return np.sqrt(s), np.repeat((0.5 * GLW)[None, :], len(a2), axis=0)
XN = {xt: xnodes(XED[xt]) for xt in XED}
SIMP = np.array([1, 4, 2, 4, 2, 4, 2, 4, 2, 4, 1], float) / 30.0              # Simpson, 10 intervals, x (ln X2 - ln X1)
def ext_point(pr, t, Xe, xs):                   # extended (cold) annulus kernel for unit mass at offsets xs (1D array)
    nk = len(Xe) - 1
    lnX = np.array([np.linspace(math.log(Xe[j + 1]), math.log(Xe[j]), 11) for j in range(nk)])
    Xn = np.exp(lnX).ravel(); xs = np.asarray(xs, float)
    act = np.where(xs * t < Xn.max() * t + 1.0)[0]
    Fv = np.zeros((len(Xn), len(xs)))
    for c0 in range(0, len(act), 100):                                       # chunked: F2 transients ~100 MB
        ii = act[c0:c0 + 100]
        Fv[:, ii] = F2(pr, (Xn * t)[:, None], (xs[ii] * t)[None, :])
    Fv = Fv.reshape(nk, 11, len(xs))
    dln = np.log(Xe[:-1]) - np.log(Xe[1:])
    return np.einsum("s,jsx->jx", SIMP, 2 * Fv) * dln[:, None] - (Fv[:, 10, :] - Fv[:, 0, :])
KCACHE = {}
def ext_bin(Ns, shape, t, et, xt):              # bin-averaged extended kernel (9, nx), cached by (shape, N, t, edges)
    key = (Ns, shape, round(math.log10(t), 10), et, xt)
    if key not in KCACHE:
        xn, xw = XN[xt]
        K = ext_point(PROFS[(Ns, shape)], t, XE[et], xn.ravel()).reshape(9, xn.shape[0], xn.shape[1])
        KCACHE[key] = np.einsum("jbn,bn->jb", K, xw)
    return KCACHE[key]
def ext_tensor(foot, shape, et, xt, mask, nm_cen):   # (NLM, nnm, 9, nx) for populated (L, m)
    nx = len(XED[xt]) - 1; T = np.zeros((C.NLM, len(nm_cen), 9, nx))
    for m in range(len(nm_cen)):
        if not mask[:, m].any(): continue
        Ns, sc = nb_scale(nm_cen[m], foot, shape)
        for Lc in range(C.NLM):
            if mask[Lc, m]: T[Lc, m] = ext_bin(Ns, shape, RHO_L[Lc] / sc, et, xt)
    return T

# ============================================================== 4. populated cells (from the neighbour pool, before any histogram)
NBLB = np.load(os.path.join(C.WORK903, "cfg903_stage.npz"))["NB_logMb"]
m_lo, m_hi = int(L.mbin_of(np.array([NBLB.min()]))[0]) - C.NM_OFF, int(L.mbin_of(np.array([NBLB.max()]))[0]) - C.NM_OFF
del NBLB
POP = np.zeros((C.NLM, C.NNM), bool); POP[:, m_lo:m_hi + 1] = True                        # every lens cell x every pool cell
for Lc in (0, C.NLM - 1):                                                                 # K2c cells always computed
    for lmn in (10.5, 12.0):
        POP[Lc, int(L.mbin_of(np.array([lmn]))[0]) - C.NM_OFF] = True
POPC = np.zeros((C.NLM, C.NNMC), bool); POPC[:, m_lo // 4:m_hi // 4 + 1] = True
def acc_member(path, key, out, sign=1.0, first=None, chunk=1 << 20):
    """Add sign x (array 'key' of an .npz) into out, streamed in chunks (no full-size temporary); first = only the first n values."""
    import zipfile
    flat = out.reshape(-1)
    with zipfile.ZipFile(path) as zf, zf.open(key + ".npy") as fp:
        ver = np.lib.format.read_magic(fp)
        shape, fortran, dtype = (np.lib.format.read_array_header_1_0 if ver == (1, 0) else np.lib.format.read_array_header_2_0)(fp)
        n = int(np.prod(shape)) if first is None else int(first)
        assert dtype == np.float64 and not fortran and flat.size == n, (key, shape, flat.size)
        i = 0
        while i < n:
            m = min(chunk, n - i); flat[i:i + m] += sign * np.frombuffer(fp.read(m * 8), dtype=np.float64); i += m
def load_histograms():
    global DH, NNORM, HJ, NJ
    DH = np.zeros(C.SHAPE_MAIN); NNORM = np.zeros(C.NCLS)
    HJ = {s: np.zeros(C.SHAPE_JK) for s in ("lens", "random", "A")}; NJ = {s: np.zeros((L.NPATCH, 3)) for s in ("lens", "random", "A")}
    k0b = []
    for b in range(1, 5):
        p903 = os.path.join(C.WORK903, f"cfg903_hist_bin{b}.npz")
        for s, ref in (("lens", "HL"), ("random", "HR")):
            pth = os.path.join(C.WORK, f"cfg912_hist_bin{b}{SFX}_{s}.npz")
            r0 = np.zeros(L.NCELL); acc_member(p903, ref, r0, first=L.NCELL)                  # CFG903 v0 row (first of 8)
            mine = np.zeros(L.NCELL); acc_member(pth, "H903", mine)
            k0b.append(float(np.max(np.abs(mine - r0))) / float(np.max(np.abs(r0))))
            acc_member(pth, "HM", DH, 1.0 if s == "lens" else -1.0)
            acc_member(pth, "HJ", HJ[s])
            with np.load(pth) as h:
                NJ[s] += h["NJ"]
                if s == "lens": NNORM += h["NNORM"]
                if s == "random": NJ["A"] += h["NJA"]
            if s == "random": acc_member(pth, "HJA", HJ["A"])
    check("K0b this lane's pair loop reproduces CFG903's committed-run v0 histograms (lens + random, 4 bins)", max(k0b) <= 1e-9,
          f"max |d| / max cell = {max(k0b):.1e}")
    P(f"  histograms loaded; current RSS {L.cur_rss() / 1e6:.0f} MB")

ISO = {"I0": (0, 1), "I1": (0,), "I5": (0, 1, 2)}
CUT = {2.0: ((1, 2), (0,)), 2.5: ((2,), (0, 1))}
WSEL = {300: [0], 500: [0, 1], 1000: [0, 1, 2]}
def cls_of(iso, cols):
    return [i * 3 + c for i in ISO[iso] for c in cols]
def excl_w(foot, shift, excl, xt):              # (2, NLM, nx): weights for flag 0 (more massive) / flag 1 (less massive)
    ed = XED[xt]; nx = len(ed) - 1; Wt = np.ones((2, C.NLM, nx))
    if excl == "E0": return Wt
    a0 = L.a0_kms2pc(foot)
    for Lc in range(C.NLM):
        lme = C.LM_CEN[Lc] + shift
        Nn = float(L.NGRID[np.argmin(np.abs(L.NGRID - L.N_of_declared(lme)))])
        xx = L.edge_of(Nn) * math.sqrt(L.Gpc * 10 ** lme / a0) / 1e6 / RHO_L[Lc]
        e = np.empty(nx); e[0] = 1.0 if xx >= ed[1] else 0.0
        e[1:] = np.clip((math.log(xx) - np.log(ed[1:-1])) / (np.log(ed[2:]) - np.log(ed[1:-1])), 0.0, 1.0)
        Wt[1, Lc] = 1.0 - e
        if excl == "E2": Wt[0, Lc] = 1.0 - e
    return Wt
def x_excl(foot, shift):
    out = []
    for Lc in (0, 9, C.NLM - 1):
        lme = C.LM_CEN[Lc] + shift; Nn = float(L.NGRID[np.argmin(np.abs(L.NGRID - L.N_of_declared(lme)))])
        out.append(L.edge_of(Nn) * math.sqrt(L.Gpc * 10 ** lme / L.a0_kms2pc(foot)) / 1e6 / RHO_L[Lc])
    return out
CONV = 4 * G_pc * PCm                                                                     # g_obs per Msun/pc^2 (cfg829)
def to_dg(T, et):
    dsig = C.G_REF / (math.pi * C.G_SI * DX2[et]) * T / C.ESD_UNIT                       # Msun/pc^2 (9,)
    return dsig, CONV * dsig

IEXT = {}
def get_iext(foot, shape, et="nom"):
    key = (foot, shape, et)
    if key not in IEXT:
        t1 = time.time(); IEXT[key] = ext_tensor(foot, shape, et, "fine", POP, C.NM_CEN)
        P(f"    kernel {key}: {time.time() - t1:.0f} s (cache {len(KCACHE)} entries; current RSS {L.cur_rss() / 1e6:.0f} MB)")
    return IEXT[key]
def twoh(foot, shape, excl, shift, cls, wsel, et="nom", host=False):
    D = np.zeros(C.SHAPE_MAIN[1:5])
    for c in cls:
        D += DH[c][..., wsel].sum(axis=-1)
    D /= sum(NNORM[c] for c in cls)
    wt = excl_w(foot, shift, excl, "fine")
    Dw = D[..., 0] * wt[0][..., None] + (0.0 if host else D[..., 1] * wt[1][..., None])          # (NLM, NX, NNM)
    cpt = 1.0 + COLD if shape == "P0" else np.ones(C.NNM)
    T = np.einsum("lxm,m,kx->k", Dw, cpt, IPT[(et, "fine")])
    if shape != "P0":
        T = T + np.einsum("lxm,lmkx->k", Dw * COLD[None, None, :], get_iext(foot, shape, et))
    return to_dg(T, et)

def full15(v9):
    out = np.zeros(15); out[C.KB] = v9; return out
def classify(f, z):
    if f >= 0.80 and z < 2: return "ENVIRONMENT EXPLAINS"
    if f >= 0.20: return "PARTIAL"
    return "NOT ENVIRONMENT" + (" (OPPOSITE SIGN)" if f < 0 else "")
def base(c):
    return c.split(" (")[0]
PRIMARY = dict(iso="I0", cut=2.0, shift=(0.123, 0.0), W=500, shape="P1", excl="E1", edges="nom")
def evaluate(foot, spec, extra=False):
    s = dict(PRIMARY); s.update(spec)
    rc, bc = CUT[s["cut"]]; sr, sb = s["shift"]
    dsr, dgr = twoh(foot, s["shape"], s["excl"], sr, cls_of(s["iso"], rc), WSEL[s["W"]], s["edges"])
    dsb, dgb = twoh(foot, s["shape"], s["excl"], sb, cls_of(s["iso"], bc), WSEL[s["W"]], s["edges"])
    ar, glr = amp_c("red", foot, sr); ab, glb = amp_c("blue", foot, sb)
    arc, _ = amp_c("red", foot, sr, full15(dgr)); abc, _ = amp_c("blue", foot, sb, full15(dgb))
    S0 = ar["A"] - ab["A"]; dAr, dAb = ar["A"] - arc["A"], ab["A"] - abc["A"]; sig = math.hypot(ar["sA"], ab["sA"])
    f = (dAr - dAb) / S0; z = (arc["A"] - abc["A"]) / sig
    R = dict(A_red=ar["A"], A_blue=ab["A"], sA_red=ar["sA"], sA_blue=ab["sA"], split=S0, z0=S0 / sig,
             A_red_corr=arc["A"], A_blue_corr=abc["A"], dA_red=dAr, dA_blue=dAb, f_env=f, z_corr=z, cls=classify(f, z),
             dg_red=dgr.tolist(), dg_blue=dgb.tolist(), dsig_red=dsr.tolist(), dsig_blue=dsb.tolist(),
             win_red=win_idx(sr).tolist(), win_blue=win_idx(sb).tolist(),
             mult_null=(S0 / (dAr - dAb)) if dAr - dAb > 0 else None,
             mult_z2=((S0 - 2 * sig) / (dAr - dAb)) if dAr - dAb > 0 else None)
    if extra:
        R["glaw_red"] = glr.tolist(); R["glaw_blue"] = glb.tolist()
        R["gobs_red"] = DATA["red"][1].tolist(); R["gobs_blue"] = DATA["blue"][1].tolist()
        hr = twoh(foot, s["shape"], s["excl"], sr, cls_of(s["iso"], rc), WSEL[s["W"]], s["edges"], host=True)[1]
        hb = twoh(foot, s["shape"], s["excl"], sb, cls_of(s["iso"], bc), WSEL[s["W"]], s["edges"], host=True)[1]
        R["host_dg_red"] = hr.tolist(); R["host_dg_blue"] = hb.tolist()
        sp, _ = amp_c("sph", foot, sr); dd, _ = amp_c("disc", foot, sb)
        spc, _ = amp_c("sph", foot, sr, full15(dgr)); ddc, _ = amp_c("disc", foot, sb, full15(dgb))
        R["sersic"] = dict(A_sph=sp["A"], A_disc=dd["A"], A_sph_corr=spc["A"], A_disc_corr=ddc["A"],
                           z0=(sp["A"] - dd["A"]) / math.hypot(sp["sA"], dd["sA"]), z_corr=(spc["A"] - ddc["A"]) / math.hypot(sp["sA"], dd["sA"]),
                           f_env=((sp["A"] - spc["A"]) - (dd["A"] - ddc["A"])) / (sp["A"] - dd["A"]))
    return R

# ============================================================== 5. K2 kernel checks (main run only)
if not MUT:
    rng = np.random.default_rng(912); w1 = 0.0
    for _ in range(12):
        N = float(rng.choice([1.0, 10.0])); pr = PROFS[(N, "P1")]; t = 10 ** rng.uniform(-1.3, 0.7)
        j = int(rng.integers(0, 9)); X1, X2 = XE["nom"][j + 1], XE["nom"][j]; x = 10 ** rng.uniform(-2, 1.3)
        lnX = np.linspace(math.log(X1), math.log(X2), 11)
        simp = float(np.sum(SIMP * 2 * F2(pr, np.exp(lnX) * t, np.full(11, x * t)))) * math.log(X2 / X1)
        qv = quad(lambda s_: 2 * float(F2(pr, math.exp(s_) * t, x * t)), math.log(X1), math.log(X2), limit=200, epsabs=1e-10)[0]
        w1 = max(w1, abs(simp - qv) / (2 * math.log(X2 / X1)))
    check("K2a-i annulus integral (Simpson in ln X) vs adaptive quadrature of CFG903 F2 (12 random points)", w1 <= 2e-3,
          f"max |d| / 2 ln(X2/X1) = {w1:.1e} (<= 2e-3); F is evaluated directly with CFG903's F2, no table (see README)")
    t1 = time.time(); w2 = 0.0; GL16, GW16 = np.polynomial.legendre.leggauss(16)
    for (N, t, j, x) in ((10.0, 0.3, 3, 1.1), (10.0, 2.0, 6, 0.7), (1.0, 0.08, 1, 3.0), (1.75, 0.6, 7, 0.2)):
        pr = PROFS[(N, "P1")]; X1, X2 = XE["nom"][j + 1], XE["nom"][j]
        mine = float(ext_point(pr, t, XE["nom"], np.array([x]))[j, 0])
        sn = 0.5 * math.log(X2 / X1) * GL16 + 0.5 * math.log(X1 * X2)
        bF = np.array([brute(pr[0], math.exp(s_) * t, x * t, n=2500) for s_ in sn])
        bk = float(np.sum(0.5 * math.log(X2 / X1) * GW16 * 2 * bF)) - (brute(pr[0], X2 * t, x * t, n=2500) - brute(pr[0], X1 * t, x * t, n=2500))
        w2 = max(w2, abs(mine - bk) / (2 * math.log(X2 / X1)))
    check("K2a-ii annulus kernel vs CFG903's independent brute-force polar F + Gauss-Legendre (4 configurations)", w2 <= 3e-3,
          f"max |d| / 2 ln(X2/X1) = {w2:.1e} (<= 3e-3); {time.time() - t1:.0f} s")
    ar2 = C.X_EDGES[1:] ** 2 - C.X_EDGES[:-1] ** 2; w3 = 0.0
    w3p = float(np.max(np.abs(IPT[("nom", "fine")] @ ar2) / DX2["nom"]))
    for foot in FOOTS:
        for shape in ("P1", "P2"):
            for Lc in (0, C.NLM - 1):
                for lmn in (10.5, 12.0):
                    m = int(L.mbin_of(np.array([lmn]))[0]) - C.NM_OFF; Ns, sc = nb_scale(C.NM_CEN[m], foot, shape)
                    K = ext_bin(Ns, shape, RHO_L[Lc] / sc, "nom", "fine")
                    w3 = max(w3, float(np.max(np.abs(K @ ar2) / DX2["nom"])))
    check("K2c uniform neighbour field gives Delta Sigma = 0 (point part; cold part P1/P2, 2 lens cells x 2 neighbour cells, both footings)",
          max(w3, w3p) <= 2e-3, f"point {w3p:.1e}, cold {w3:.1e} of Sigma0 (<= 2e-3)")

# ============================================================== 5b. kernels precomputed (before the histograms are in memory), then histograms
for foot in FOOTS:
    for shape, et in ((("P1", "nom"),) if MUT else (("P1", "nom"), ("P2", "nom"), ("P1", "file"))):
        get_iext(foot, shape, et)
IEC_ALL = {} if MUT else {foot: ext_tensor(foot, "P1", "nom", "coarse", POPC, NMC_CEN) for foot in FOOTS}
KCACHE.clear()
P(f"  kernels ready; current RSS {L.cur_rss() / 1e6:.0f} MB")
load_histograms()

# ============================================================== 6. primary, brackets, reported variants
BRACKETS = [("ISO-f30 (I1)", dict(iso="I1")), ("ISO-B21n (I5, count-matched)", dict(iso="I5")),
            ("P0 (point cold energy)", dict(shape="P0")), ("P2 (diffuse cold energy)", dict(shape="P2")),
            ("W300", dict(W=300)), ("W1000", dict(W=1000)), ("CUT-2.5", dict(cut=2.5)), ("MSTAR-0 (no M* shift)", dict(shift=(0.0, 0.0)))]
REPORTED = [("shift (+0.20, 0)", dict(shift=(0.2, 0.0))), ("shift (+0.123, +0.05)", dict(shift=(0.123, 0.05))),
            ("E0 (no exclusion; double counts)", dict(excl="E0")), ("E2 (hosts inside r_x dropped too)", dict(excl="E2")),
            ("edges centred on the file g_bar", dict(edges="file"))]
RES = dict(lane="CFG912", mutate=MUT, criteria="96de8091f", checks=CHK, footings={},
           counts=dict(NNORM=NNORM.tolist()))
for foot in FOOTS:
    P(f"\n{'-' * 110}\n  FOOTING {foot} (a0 {L.A0[foot]:.4e}); exclusion edge x_x = r_x / rho_l at lens cells 9.35/10.25/11.05: "
      + "unshifted " + "/".join(f"{v:.2f}" for v in x_excl(foot, 0.0)) + ", +0.123 " + "/".join(f"{v:.2f}" for v in x_excl(foot, 0.123)))
    FR = {}
    pr = evaluate(foot, {}, extra=True); FR["primary"] = pr
    P(f"  PRIMARY (I0, u-r 2.0, shifts +0.123/0, W500, P1, E1, C1', nominal edges):")
    P(f"    A_red {pr['A_red']:.3f} +- {pr['sA_red']:.3f}   A_blue {pr['A_blue']:.3f} +- {pr['sA_blue']:.3f}   split {pr['split']:.3f} ({pr['z0']:.2f} sigma)")
    P(f"    two-halo: dA_red {pr['dA_red']:+.4f}   dA_blue {pr['dA_blue']:+.4f}   -> A_red^corr {pr['A_red_corr']:.3f}, A_blue^corr {pr['A_blue_corr']:.3f}")
    P(f"    f_env = {pr['f_env']:+.3f}   z_corr = {pr['z_corr']:.2f}   ==> {pr['cls']}")
    P(f"    blue law check after the term: (A_blue^corr - 1)/sA = {(pr['A_blue_corr'] - 1) / pr['sA_blue']:+.2f}")
    P(f"    multiplier on (dg_red - dg_blue) for split = 0: {pr['mult_null'] if pr['mult_null'] is None else round(pr['mult_null'], 1)};"
      f" for z_corr = 2: {pr['mult_z2'] if pr['mult_z2'] is None else round(pr['mult_z2'], 1)}")
    P("    per bin (file g_bar | window R/B | two-halo dSigma red / blue [Msun/pc^2] | dg/g_law red / blue | data g_obs/g_law - 1 red / blue | host share red / blue):")
    for i, k in enumerate(C.KB):
        gr, gbl = pr["glaw_red"][k], pr["glaw_blue"][k]
        hsr = pr["host_dg_red"][i] / pr["dg_red"][i] if pr["dg_red"][i] != 0 else float("nan")
        hsb = pr["host_dg_blue"][i] / pr["dg_blue"][i] if pr["dg_blue"][i] != 0 else float("nan")
        P(f"      {GB0[k]:.2e} | {'R' if k in pr['win_red'] else '.'}{'B' if k in pr['win_blue'] else '.'} | {pr['dsig_red'][i]:6.3f} / {pr['dsig_blue'][i]:6.3f} | "
          f"{pr['dg_red'][i] / gr:+.3f} / {pr['dg_blue'][i] / gbl:+.3f} | {pr['gobs_red'][k] / gr - 1:+.3f} / {pr['gobs_blue'][k] / gbl - 1:+.3f} | {hsr:.2f} / {hsb:.2f}")
    se = pr["sersic"]
    P(f"    Sersic split with the colour-proxy vectors (reported): A_sph {se['A_sph']:.3f} -> {se['A_sph_corr']:.3f}, A_disc {se['A_disc']:.3f} -> {se['A_disc_corr']:.3f};"
      f" f_env {se['f_env']:+.3f}, z {se['z0']:.2f} -> {se['z_corr']:.2f}")
    if MUT:
        RES["footings"][foot] = FR; continue
    P("  BRACKETS (one at a time; class by f_env / z_corr):")
    FR["brackets"] = {}
    for lab, spec in BRACKETS:
        r = evaluate(foot, spec); FR["brackets"][lab] = r
        P(f"    {lab:36s} A_r {r['A_red']:.3f} A_b {r['A_blue']:.3f}  dA_r {r['dA_red']:+.4f} dA_b {r['dA_blue']:+.4f}  f_env {r['f_env']:+.3f}  z_corr {r['z_corr']:5.2f}"
          f"  -> {r['cls']}{'   <== CLASS CHANGES' if base(r['cls']) != base(pr['cls']) else ''}")
    P("  REPORTED ONLY (no class weight):")
    FR["reported"] = {}
    for lab, spec in REPORTED:
        r = evaluate(foot, spec); FR["reported"][lab] = r
        P(f"    {lab:36s} A_r {r['A_red']:.3f} A_b {r['A_blue']:.3f}  dA_r {r['dA_red']:+.4f} dA_b {r['dA_blue']:+.4f}  f_env {r['f_env']:+.3f}  z_corr {r['z_corr']:5.2f}  ({r['cls']})")
    RES["footings"][foot] = FR

# ============================================================== 7. jackknife (primary) and K3 (random halves)
if not MUT:
    P(f"\n{'-' * 110}\n  JACKKNIFE (50 patches, delete-one; coarse cells: 5 x-bins = one annulus edge step, 0.2-dex neighbour cells) and K3")
    IPTC = IPT[("nom", "coarse")]
    def jk_dg(Dc, foot, shift, IEC):            # Dc (NLM, NXC, NNMC, 2) normalised
        wt = excl_w(foot, shift, "E1", "coarse")
        Dw = Dc[..., 0] * wt[0][..., None] + Dc[..., 1] * wt[1][..., None]
        T = np.einsum("lxm,kx->k", Dw, IPTC) + np.einsum("lxm,lmkx->k", Dw * COLD_C[None, None, :], IEC)
        return to_dg(T, "nom")[1]
    def amp_pair(foot, dgr, dgb, sr, sb):
        ar, _ = amp_c("red", foot, sr); ab, _ = amp_c("blue", foot, sb)
        arc, _ = amp_c("red", foot, sr, full15(dgr)); abc, _ = amp_c("blue", foot, sb, full15(dgb))
        return ar["A"] - arc["A"], ab["A"] - abc["A"], ar["A"] - ab["A"], math.hypot(ar["sA"], ab["sA"])
    JK = {}
    cols = {"red": (1, 2), "blue": (0,)}; sh = {"red": 0.123, "blue": 0.0}
    Hc = {(s, c): HJ[s][:, list(cols[c])].sum(axis=1) for s in HJ for c in cols}         # (50, NLM, NXC, NNMC, 2)
    Nc = {(s, c): NJ[s][:, list(cols[c])].sum(axis=1) for s in NJ for c in cols}         # (50,)
    del HJ
    for foot in FOOTS:
        IEC = IEC_ALL[foot]
        full = {c: jk_dg(Hc[("lens", c)].sum(0) / Nc[("lens", c)].sum() - Hc[("random", c)].sum(0) / Nc[("random", c)].sum(), foot, sh[c], IEC) for c in cols}
        dAr, dAb, S0, sig = amp_pair(foot, full["red"], full["blue"], 0.123, 0.0)
        fine = RES["footings"][foot]["primary"]
        fd, zd, dd, ff = [], [], [], []
        for p in range(L.NPATCH):
            dg = {}
            for c in cols:
                Dl = (Hc[("lens", c)].sum(0) - Hc[("lens", c)][p]) / (Nc[("lens", c)].sum() - Nc[("lens", c)][p])
                Dr = (Hc[("random", c)].sum(0) - Hc[("random", c)][p]) / (Nc[("random", c)].sum() - Nc[("random", c)][p])
                dg[c] = jk_dg(Dl - Dr, foot, sh[c], IEC)
            a, b_, s0, sg = amp_pair(foot, dg["red"], dg["blue"], 0.123, 0.0)
            dd.append(a - b_); ff.append((a - b_) / s0)
        dd, ff = np.array(dd), np.array(ff)
        sj = lambda v: float(math.sqrt((L.NPATCH - 1) / L.NPATCH * np.sum((v - v.mean()) ** 2)))
        s_dd, s_f = sj(dd), sj(ff)
        near = abs(fine["f_env"] - 0.2) < 2 * s_f or abs(fine["f_env"] - 0.8) < 2 * s_f
        zjk = (fine["A_red_corr"] - fine["A_blue_corr"]) / math.sqrt(sig ** 2 + s_dd ** 2)
        # K3: random halves A - B, window bins of the primary
        def halfdiff(c, p=None):
            hA, nA = Hc[("A", c)], Nc[("A", c)]; hR, nR = Hc[("random", c)], Nc[("random", c)]
            if p is None:
                DA = hA.sum(0) / nA.sum(); DB = (hR.sum(0) - hA.sum(0)) / (nR.sum() - nA.sum())
            else:
                DA = (hA.sum(0) - hA[p]) / (nA.sum() - nA[p]); DB = ((hR.sum(0) - hR[p]) - (hA.sum(0) - hA[p])) / ((nR.sum() - nR[p]) - (nA.sum() - nA[p]))
            v = jk_dg(DA - DB, foot, sh[c], IEC); w = [list(C.KB).index(k) for k in win_idx(sh[c])]
            return float(np.mean(v[w]))
        k3 = {}
        for c in cols:
            m0 = halfdiff(c); mj = np.array([halfdiff(c, p) for p in range(L.NPATCH)]); s3 = sj(mj)
            k3[c] = dict(mean=m0, sigma=s3, ok=abs(m0) <= 3 * s3)
        JK[foot] = dict(coarse_dA_red=dAr, coarse_dA_blue=dAb, coarse_f_env=(dAr - dAb) / S0, sigma_ddA=s_dd, sigma_f_env=s_f,
                        near_boundary=bool(near), z_corr_with_jk=zjk, k3=k3, dd_delete_one=dd.tolist())
        P(f"  [{foot}] coarse full sample: dA_red {dAr:+.4f} dA_blue {dAb:+.4f} f_env {(dAr - dAb) / S0:+.3f} (fine: {fine['dA_red']:+.4f} / {fine['dA_blue']:+.4f} / {fine['f_env']:+.3f})")
        P(f"  [{foot}] sigma_jk(dA_red - dA_blue) = {s_dd:.4f}; sigma_jk(f_env) = {s_f:.3f}; class boundary within 2 sigma: {near}; z_corr with jackknife variance {zjk:.2f}")
        P(f"  [{foot}] K3 random halves A - B (window mean dg, m/s^2): red {k3['red']['mean']:+.2e} +- {k3['red']['sigma']:.2e}, blue {k3['blue']['mean']:+.2e} +- {k3['blue']['sigma']:.2e}")
        RES["footings"][foot]["jackknife"] = JK[foot]
    check("K3 random halves A - B consistent with zero (window mean, red and blue, both footings)",
          all(JK[f]["k3"][c]["ok"] for f in FOOTS for c in ("red", "blue")),
          "; ".join(f"{f} {c} {JK[f]['k3'][c]['mean'] / JK[f]['k3'][c]['sigma']:+.1f} sigma" for f in FOOTS for c in ("red", "blue")))

# ============================================================== 8. MUTATE recovery
if MUT:
    REFJ = json.load(open(os.path.join(C.HERE, "cfg912_results.json")))
    S = np.load(os.path.join(C.WORK903, "cfg903_stage.npz")); CO = np.load(os.path.join(C.WORK, "cfg912_colour.npz"))
    I0a, Wa, Ma = S["L_I0"], S["L_W_B21"], S["L_Mgal"]; col = CO["col3"]; del S
    inj = np.where(I0a & (col >= 1))[0][::C.INJ_EVERY]
    redI0 = I0a & (col >= 1); Nred = float(np.sum(Wa[redI0] * Ma[redI0]))
    assert abs(Nred / sum(NNORM[c] for c in cls_of("I0", (1, 2))) - 1) < 1e-12
    Minj = 10 ** C.INJ_LOGMB; cinj = 1.0 + L.SUP * L.N_of_declared(C.INJ_LOGMB)
    def direct_inj(dinj):                       # exact per-lens annulus kernel of the injected point hosts (P0)
        xl_ = dinj / C.rho_Mpc(Ma[inj]); Xe = XE["nom"]; Hd, Hg = np.zeros(9), np.zeros(9)
        for j in range(9):
            X1, X2 = Xe[j + 1], Xe[j]
            I = np.where(xl_ < X2, 2 * np.log(X2 / np.maximum(X1, xl_)), 0.0) - ((xl_ >= X1) & (xl_ < X2))
            Hd[j] = float(np.sum(Wa[inj] * Minj * cinj * I)) / Nred; Hg[j] = float(np.sum(Wa[inj] * Minj * cinj * np.abs(I))) / Nred
        return to_dg(Hd, "nom")[1], to_dg(Hg, "nom")[1], xl_
    exp_dg, gross_dg, xl = direct_inj(C.INJ_D)
    P(f"\n{'-' * 110}\n  MUTATE: {len(inj):,} injected hosts (log M_b {C.INJ_LOGMB}, d = {C.INJ_D} Mpc, every {C.INJ_EVERY}th I0 red lens); x = d/rho_l in [{xl.min():.2f}, {xl.max():.2f}]")
    okb, okr, frise = True, True, True
    for foot in FOOTS:
        for shape in ("P0", "P1"):
            r = evaluate(foot, dict(shape=shape))
            ref = REFJ["footings"][foot]["primary"] if shape == "P1" else REFJ["footings"][foot]["brackets"]["P0 (point cold energy)"]
            db = float(np.max(np.abs(np.array(r["dg_blue"]) - np.array(ref["dg_blue"]))))
            rec = np.array(r["dg_red"]) - np.array(ref["dg_red"])
            bref = float(np.max(np.abs(np.array(ref["dg_blue"]))))
            okb &= (db == 0.0) if (shape == "P0" or C.MUT_MODE == "A") else (db <= 1e-12 * bref)      # A1: P1 roundoff allowance (B only)
            line = f"    [{foot} {shape}] blue max |d dg| = {db:.1e}; f_env {ref['f_env']:+.3f} -> {r['f_env']:+.3f} ({r['cls']})"
            frise &= r["f_env"] > ref["f_env"]
            if shape == "P0":
                tol = 0.01 * np.abs(exp_dg) + 1e-6 * np.max(np.abs(exp_dg))
                okr &= bool(np.all(np.abs(rec - exp_dg) <= tol))
                line += "; red d dg recovered / direct per bin: " + ", ".join(f"{a:.3e}/{b:.3e}" for a, b in zip(rec, exp_dg))
            P(line)
            RES["footings"].setdefault(foot, {})[shape] = r
    lab = "MUTATE" if C.MUT_MODE == "A" else "MUTATE-B (A1)"
    check(f"{lab} recovered: blue unchanged ({'exactly' if C.MUT_MODE == 'A' else 'P0 exactly, P1 <= 1e-12 rel.'}), P0 red change = direct per-lens computation (<= 1% per bin), f_env rises",
          okb and okr and frise, f"blue {okb}; red recovered {okr}; f_env rises {frise}")
    if C.MUT_MODE == "B":                       # A1 diagnostics for the frozen MUTATE (d = 0.4 Mpc)
        RA = json.load(open(os.path.join(C.HERE, "cfg912_results_MUTATE.json")))
        eA, gA, _ = direct_inj(0.4)
        P("  A1 diagnostics of the frozen MUTATE (host at 0.4 Mpc):")
        for foot in FOOTS:
            m0 = REFJ["footings"][foot]["brackets"]["P0 (point cold energy)"]; mA = RA["footings"][foot]["P0"]
            sr, sb = PRIMARY["shift"]
            arc, _ = amp_c("red", foot, sr, full15(np.array(m0["dg_red"]) + eA)); abc, _ = amp_c("blue", foot, sb, full15(np.array(m0["dg_blue"])))
            ar, _ = amp_c("red", foot, sr); ab, _ = amp_c("blue", foot, sb)
            fd = ((ar["A"] - arc["A"]) - (ab["A"] - abc["A"])) / (ar["A"] - ab["A"])
            recA = np.array(mA["dg_red"]) - np.array(m0["dg_red"])
            rel = np.where(gA > 0, np.abs(recA - eA) / np.where(gA > 0, gA, 1.0), 0.0)
            P(f"    [{foot} P0] f_env with the DIRECT injection {fd:+.4f} vs the pipeline's {mA['f_env']:+.4f}; "
              f"|recovered - direct| / gross per bin: " + ", ".join(f"{v:.2e}" for v in rel))
            RES.setdefault("a1_diag", {})[foot] = dict(f_env_direct=fd, f_env_pipeline=mA["f_env"], rel_to_gross=rel.tolist())

RES["runtime_s"] = round(time.time() - L.T0, 1); RES["peak_current_rss_MB"] = round(L.PEAK_CUR[0] / 1e6, 1)
P(f"\n  checks: " + ", ".join(f"{k.split()[0]} {'PASS' if v else 'FAIL'}" for k, v in CHK.items()))
P(f"  runtime {RES['runtime_s']} s; peak current RSS {RES['peak_current_rss_MB']} MB")
json.dump(RES, open(os.path.join(C.HERE, f"cfg912_results{SFX}.json"), "w"), indent=1, default=float)
open(os.path.join(C.HERE, f"cfg912_score{SFX}.out"), "w").write("\n".join(OUT) + "\n")
