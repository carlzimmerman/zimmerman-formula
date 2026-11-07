#!/usr/bin/env python3
"""NC4 R7 child (criteria 54784e16e5, section 4): the clump spectrum's f(M500) on the 20 Lovisari groups through CK3's data
side (UA1 joint draws; se2.py exec'd read-only to its main loop, ua1.py's groups-knob block verbatim, writes redirected to a
temp dir). Test A: slope of eps = f / 5.4 vs log10 M500 (95 % of data - prediction contains 0); test B: UA1 class step with
the component (95 % contains 0). Run as a separate process (RSS ~0.9 GB, as CK3).
    python3 nc4_r7.py <out.json> <json: {footing: {"fX":..., "lMX":...}}> <json: [s_f, ...]>
Env NC4_UA1_DIR overrides the UA1 folder (default: the repo's closure_2026_11_07/UA1_fragile_rows).
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, re, ast, io, tempfile, contextlib, builtins, resource, signal
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
UA1D = os.environ.get("NC4_UA1_DIR") or os.path.join(REPO, "closure_2026_11_07", "UA1_fragile_rows")
SE2P = os.path.join(REPO, "closure_2026_11_06", "SE2_step_as_systematics", "se2.py")
OUTP, SPEC_IN, SGRID = sys.argv[1], json.loads(sys.argv[2]), json.loads(sys.argv[3])
RES = dict(KA={}, footings={})
def _term(sig, frm):
    RES["interrupted"] = "SIGTERM"; json.dump(RES, open(OUTP + ".partial", "w"), indent=1); sys.exit(3)
signal.signal(signal.SIGTERM, _term)

# ---- CK3's data side, verbatim construction
tmp = tempfile.mkdtemp(prefix="nc4_se2_")
def ropen(path, mode="r", *a, **kw):
    if any(c in mode for c in "wa+"): return builtins.open(os.path.join(tmp, os.path.basename(path)), mode, *a, **kw)
    return builtins.open(path, mode, *a, **kw)
src = builtins.open(SE2P).read(); src = src[:src.index("# ------------------------------------------------------------------ main loop")]
_k1 = "K1 = ka1_st1();"; assert src.count(_k1) == 1
src = src.replace(_k1, "K1 = dict(n_numeric=0, n_other=0, n_diff=0, ok=True, skipped_by_NC4=True);")
g = {"__file__": SE2P, "__name__": "se2_lib", "open": ropen}
_a = sys.argv; sys.argv = [SE2P]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, "se2_lib", "exec"), g)
sys.argv = _a
usrc = builtins.open(os.path.join(UA1D, "ua1.py")).read()
blk = usrc[usrc.index("# ------------------------------------------------------------------ groups: new knobs"):
           usrc.index("# ------------------------------------------------------------------ pericentre admissibility (A3)")]
g.update(re=re, ast=ast, math=math, np=np, REPO=REPO, RES={})
with contextlib.redirect_stdout(io.StringIO()): exec(compile(blk, "ua1_groups_block", "exec"), g)
UA1J = json.load(builtins.open(os.path.join(UA1D, "ua1.json")))
A0 = g["A0"]; NDRAW = g["NDRAW"]; GRAW = g["GRAW"]; GR = g["GR"]; KPC = g["KPC"]; G = g["G"]; MS = g["MS"]
gl, dlaw, fimf, draw_lam, uni, rngs, summ, SPEC = g["gl"], g["dlaw"], g["fimf"], g["draw_lam"], g["uni"], g["rngs"], g["summ"], g["SPEC"]
K_TO_S = g["K_TO_S"]; nrng, gspec, post_groups2 = g["nrng"], g["gspec"], g["post_groups2"]
SPM = SPEC("main"); GS = gspec("main"); RC = 5.4
NAMES = [gp["name"] for gp in GR]; NG = len(NAMES); LM500 = np.array([math.log10(gp["M5"]) for gp in GR])

def ua1_draws(a0, f):                                    # CK3 verbatim
    rs, rn = rngs("groups", f)
    lam = draw_lam(rn, SPM, NDRAW); sg = uni(rn, SPM["sig_grp"], NDRAW); fst = uni(rn, SPM["fst"], NDRAW)
    rx = nrng("groups", f)
    bnt = uni(rx, GS["bnt"], NDRAW); dfac = uni(rx, GS["df"], NDRAW); cg = uni(rx, GS["cg"], NDRAW); dsh = rx.normal(0, 1, NDRAW) * GS["mg"]
    ix = rs.integers(0, NG, (NDRAW, NG))
    rm = (np.array([r for _, r, _, _ in GRAW]) * KPC)[None] * dfac[:, None]
    Mg = np.array([m for _, _, m, _ in GRAW])[None] * (dfac[:, None] ** 2.5 * cg[:, None])
    Mo = np.array([m for _, _, _, m in GRAW])[None] * (dfac[:, None] / (1.0 - bnt[:, None]) * 10.0 ** dsh[:, None])
    fs = fst[:, None]; Mb = Mg * (1 + fs); gN = G * Mb * MS / rm ** 2
    Ml = gl(gN, a0) * rm ** 2 / G / MS; D = np.log10(Mo / Ml); sh = fs / (1 + fs)
    bI = 1 + sh * (fimf(np.asarray(sg), K_TO_S)[:, None] ** np.asarray(lam)[:, None] - 1)
    sel = np.stack([[2 * k, 2 * k + 1] for k in range(NG)])[ix].reshape(NDRAW, -1)
    return dict(D=D, gN=gN, bI=np.broadcast_to(bI, D.shape).copy(), sel=sel)
def resid(Z, eps_pt, a0): return Z["D"] - dlaw(Z["bI"] + RC * eps_pt, Z["gN"], a0)
def step(Z, eps_g, a0):
    r = resid(Z, np.repeat(eps_g, 2, axis=1), a0)
    return np.median(r[np.arange(NDRAW)[:, None], Z["sel"]], axis=1)
def need(Z, a0):
    lo = (0.01 - Z["bI"].reshape(NDRAW, NG, 2).min(-1)) / RC; hi = np.full((NDRAW, NG), 10.0)
    for _ in range(60):
        mid = 0.5 * (lo + hi); r = resid(Z, np.repeat(mid, 2, axis=1), a0).reshape(NDRAW, NG, 2).mean(-1)
        lo = np.where(r > 0, mid, lo); hi = np.where(r > 0, hi, mid)
    return 0.5 * (lo + hi)
def ols(x, y):
    xm = x.mean(-1, keepdims=True); ym = y.mean(-1, keepdims=True)
    return ((x - xm) * (y - ym)).sum(-1) / ((x - xm) ** 2).sum(-1)
def q(x): return dict(median=float(np.median(x)), lo68=float(np.percentile(x, 16)), hi68=float(np.percentile(x, 84)),
                      lo95=float(np.percentile(x, 2.5)), hi95=float(np.percentile(x, 97.5)))
def c95(x): lo, hi = np.percentile(x, [2.5, 97.5]); return bool(lo <= 0 <= hi)

for f, a0 in A0.items():
    Z = ua1_draws(a0, f); R = {}; RES["footings"][f] = R
    s0 = step(Z, np.zeros((NDRAW, NG)), a0); ref = post_groups2(a0, f, SPM, GS)
    eqa = bool(np.array_equal(s0, ref)); eqj = summ(s0) == UA1J["footings"][f]["cells"]["groups"]["post"]
    en = need(Z, a0); rb2 = np.random.default_rng(3301 + (0 if f == "canonical" else 1)); gi = rb2.integers(0, NG, (NDRAW, NG))
    bdat = ols(LM500[gi], en[np.arange(NDRAW)[:, None], gi])
    RES["KA"][f] = dict(step0=summ(s0), array_equal=eqa, summary_equals_ua1_json=eqj, data_slope=q(bdat))
    R["median_group_lM500"] = float(np.median(LM500)); R["lM500"] = LM500.tolist(); R["names"] = NAMES
    R["per_group_need_eps_median"] = [float(np.median(en[:, k])) for k in range(NG)]
    fX, lMX = SPEC_IN[f]["fX"], SPEC_IN[f]["lMX"]; R["cells"] = {}
    for sf in SGRID:
        fg = np.maximum(fX + sf * (LM500 - lMX), 0.0); eps = fg / RC
        bp = float(ols(LM500, eps)); dA = bdat - bp
        sB = step(Z, np.repeat(eps[None], NDRAW, axis=0), a0)
        A_ok, B_ok = c95(dA), c95(sB)
        R["cells"][f"{sf:.2f}"] = dict(f_groups_min=float(fg.min()), f_groups_max=float(fg.max()), f_at_median=float(fX + sf * (np.median(LM500) - lMX)),
                                       pred_slope_eps=bp, A_delta=q(dA), A_pass=A_ok, B_step=q(sB), B_pass=B_ok, R7_pass=bool(A_ok and B_ok))
    del Z, en
RES["peak_rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
json.dump(RES, open(OUTP, "w"), indent=1)
print("NC4R7 done", RES["peak_rss_GB"])
