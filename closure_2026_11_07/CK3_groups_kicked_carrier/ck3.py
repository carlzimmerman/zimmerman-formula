#!/usr/bin/env python3
"""CK3 (criteria 753fc90cf4): groups under the kicked collisionless carrier. L388's pooled retention eps(M(<1 Mpc/h))
interpolated to the 20 Lovisari groups (XR13's NFW placement, LCDM-like reference), carrier f = R_c eps of M_b through
the law (KD1 units), graded on UA1's joint posterior: A the slope of eps vs log10 M500 (data need vs prediction),
B the class step with the carrier. v_k 550 (extrapolated, not a run) / 575 / 600; both footings, never pooled.
    python3 ck3.py           -> ck3.json / ck3.out          (KA1-KA3, per-group table, A, B, labels, sensitivities)
    python3 ck3.py --mutate  -> ck3_MUTATE.out              (flat retention: A must fail, else NO POWER)
se2.py exec'd read-only up to its main loop (writes redirected to a temp dir); ua1.py's groups-knob block exec'd
read-only. Env CK3_REPO / CK3_UA1_DIR override the repo root and the UA1 folder (default: this file's place in the repo).
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math, re, ast, io, tempfile, contextlib, builtins, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("CK3_REPO") or os.path.dirname(os.path.dirname(HERE))
UA1D = os.environ.get("CK3_UA1_DIR") or os.path.join(REPO, "closure_2026_11_07", "UA1_fragile_rows")
SE2P = os.path.join(REPO, "closure_2026_11_06", "SE2_step_as_systematics", "se2.py")
L388P = os.path.join(REPO, "real_research", "dark_sector_2026", "L388_linear_gate_pooled_results.json")
MUT = "--mutate" in sys.argv; OUT = []
def P(s=""): print(s, flush=True); OUT.append(s)
RES = dict(lane="CK3", criteria="753fc90cf4", note="kappa = 1/2 FITTED; not theory closed; adopts nothing", KA={}, footings={})
P(f"CK3 groups under the kicked carrier {'MUTATE (flat retention)' if MUT else 'MAIN'}. kappa = 1/2 FITTED; not theory closed; footings never pooled.")

# ------------------------------------------------------------------ SE2 definitions (exec'd read-only up to its main loop)
tmp = tempfile.mkdtemp(prefix="ck3_se2_")
def ropen(path, mode="r", *a, **kw):
    if any(c in mode for c in "wa+"): return builtins.open(os.path.join(tmp, os.path.basename(path)), mode, *a, **kw)
    return builtins.open(path, mode, *a, **kw)
src = builtins.open(SE2P).read(); src = src[:src.index("# ------------------------------------------------------------------ main loop")]
# SE2's own KA1 (the ST1 replay) is not needed for the groups machinery and costs memory; it is stubbed in the exec'd copy
# only (se2.py on disk untouched). CK3's KA2 (array_equal with UA1's posterior) checks the machinery instead.
_k1 = "K1 = ka1_st1();"; assert src.count(_k1) == 1
src = src.replace(_k1, "K1 = dict(n_numeric=0, n_other=0, n_diff=0, ok=True, skipped_by_CK3=True);")
g = {"__file__": SE2P, "__name__": "se2_lib", "open": ropen}
_a = sys.argv; sys.argv = [SE2P]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, "se2_lib", "exec"), g)
sys.argv = _a
# UA1's groups-knob block, verbatim, in the same namespace
usrc = builtins.open(os.path.join(UA1D, "ua1.py")).read()
blk = usrc[usrc.index("# ------------------------------------------------------------------ groups: new knobs"):
           usrc.index("# ------------------------------------------------------------------ pericentre admissibility (A3)")]
g.update(re=re, ast=ast, math=math, np=np, REPO=REPO, RES={})
with contextlib.redirect_stdout(io.StringIO()): exec(compile(blk, "ua1_groups_block", "exec"), g)
UA1J = json.load(builtins.open(os.path.join(UA1D, "ua1.json")))
A0 = g["A0"]; NDRAW = g["NDRAW"]; GRAW = g["GRAW"]; GR = g["GR"]; KPC = g["KPC"]; G = g["G"]; MS = g["MS"]
gl, dlaw, fimf, draw_lam, uni, rngs, summ, SPEC = g["gl"], g["dlaw"], g["fimf"], g["draw_lam"], g["uni"], g["rngs"], g["summ"], g["SPEC"]
K_TO_S = g["K_TO_S"]; nrng, gspec, post_groups2 = g["nrng"], g["gspec"], g["post_groups2"]
SPM = SPEC("main"); GS = gspec("main")
RC = 5.4                                                         # cosmic carrier-to-baryon ratio (resolution; LCDM-like reference)
NAMES = [gp["name"] for gp in GR]; NG = len(NAMES)
LM500 = np.array([math.log10(gp["M5"]) for gp in GR])
KEV, MP = 1.602176634e-16, 1.67262192e-27
LSIG = np.array([math.log10(math.sqrt(gp["kT"] * KEV / (0.6 * MP)) / 1e3) for gp in GR])   # reported only
assert all(GRAW[2 * k][0] == NAMES[k] and GRAW[2 * k + 1][0] == NAMES[k] for k in range(NG))

# ------------------------------------------------------------------ XR13's M500 -> M(<1 Mpc/h), verbatim (LCDM-like reference)
hh = 0.6736; RHO_C0 = 2.775e11 * hh ** 2 / 1e9
c200_dm14 = lambda M200: 10 ** (0.905 - 0.101 * math.log10(M200 / (1e12 / hh)))
def m_1mpch(M500):
    m = lambda x: math.log(1 + x) - x / (1 + x)
    R500 = (3 * M500 / (4 * math.pi * 500 * RHO_C0)) ** (1 / 3)
    M200 = M500 * 1.4
    for _ in range(30):
        c = c200_dm14(M200); r200 = (3 * M200 / (4 * math.pi * 200 * RHO_C0)) ** (1 / 3); rs = r200 / c
        M200 = M500 * m(c) / m(R500 / rs)
    return M200 * m((1000.0 / hh) / rs) / m(c)
M1 = np.array([m_1mpch(gp["M5"]) for gp in GR]); LM1 = np.log10(M1)
nbelow = int((M1 < 6e13).sum())
RES["KA"]["KA3_XR13_placement"] = dict(n_below_6e13=nbelow, ok=nbelow == 5)
P(f"KA3 XR13 placement: {nbelow} of {NG} groups below L388's lowest bin edge 6e13 (XR13: 5) -> {'PASS' if nbelow == 5 else 'FAIL'}")

# ------------------------------------------------------------------ L388 nodes
L388 = json.load(builtins.open(L388P))["numbers"]; SEEDS_L = ("7", "17", "29")
MH = np.concatenate([np.array(L388["halos"][s]["M_lt_1Mpc_h"]) for s in SEEDS_L])
EPS = {t: np.concatenate([np.array(L388["halos"][s]["eps"][t]) for s in SEEDS_L]) for t in ("v575", "v600", "v625", "v650")}
EPS["v550"] = np.clip(2 * EPS["v575"] - EPS["v600"], 0.0, 1.0)      # linear in v_k, NOT A RUN
BINS = ((6e13, 1e14), (1e14, 1.5e14), (1.5e14, 2.5e14), (2.5e14, 1e17))
ka1 = []
for t in ("v575", "v600", "v625", "v650"):
    for b0, b1 in BINS:
        s_ = (MH >= b0) & (MH < b1); mine = float(np.median(EPS[t][s_])); rec = L388["retention_by_mass"][t][f"{b0:.1e}-{b1:.1e}"]
        ka1.append(dict(kick=t, bin=f"{b0:.1e}-{b1:.1e}", mine=mine, n=int(s_.sum()), record=rec[0], n_record=rec[1], diff=mine - rec[0]))
ok1 = all(r["diff"] == 0.0 and r["n"] == r["n_record"] for r in ka1)
RES["KA"]["KA1_L388_bins"] = dict(rows=ka1, ok=ok1)
P(f"KA1 L388 bin retention from per-halo eps vs committed retention_by_mass (16 cells): max |diff| {max(abs(r['diff']) for r in ka1):.1e}, counts equal "
  f"{all(r['n'] == r['n_record'] for r in ka1)} -> {'PASS (difference 0)' if ok1 else 'FAIL'}")

def nodes(idx, t):
    x, y = [], []
    for b0, b1 in BINS:
        s_ = (MH[idx] >= b0) & (MH[idx] < b1)
        if not s_.any(): return None
        x.append(float(np.median(np.log10(MH[idx][s_])))); y.append(float(np.median(EPS[t][idx][s_])))
    return np.array(x), np.array(y)
def interp(lm, xy, below="linear"):
    x, y = xy; out = np.interp(lm, x, y)
    lo = lm < x[0]
    if below == "linear": out[lo] = np.maximum(y[0] + (y[1] - y[0]) / (x[1] - x[0]) * (lm[lo] - x[0]), 0.0)
    else: out[lo] = y[0]
    return out
NB = 2000; rb = np.random.default_rng(3300); BOOT = []
while len(BOOT) < NB:
    idx = rb.integers(0, len(MH), len(MH))
    if all(((MH[idx] >= b0) & (MH[idx] < b1)).any() for b0, b1 in BINS): BOOT.append(idx)
KICKS = ("v550", "v575", "v600"); REPORTED_KICKS = ("v625", "v650")
def ols(x, y):                                                  # slope of y on x along the last axis
    xm = x.mean(-1, keepdims=True); ym = y.mean(-1, keepdims=True)
    return ((x - xm) * (y - ym)).sum(-1) / ((x - xm) ** 2).sum(-1)
def predict(t, below="linear", lm1=LM1):
    full = interp(lm1, nodes(np.arange(len(MH)), t), below)
    bs = np.stack([interp(lm1, nodes(i_, t), below) for i_ in BOOT])         # (NB, 20)
    return full, bs
PRED = {}
for t in KICKS + REPORTED_KICKS:
    full, bs = predict(t); sl = ols(LM500[None], bs)
    PRED[t] = dict(full=full, bs=bs, slope_full=float(ols(LM500, full)), slope_med=float(np.median(sl)),
                   slope_err68=float((np.percentile(sl, 84) - np.percentile(sl, 16)) / 2), slope_bs=sl,
                   slope_sigma_full=float(ols(LSIG, full)), nodes=[list(map(float, v)) for v in nodes(np.arange(len(MH)), t)])
    P(f"prediction {t}{' (extrapolated, not a run)' if t == 'v550' else ''}{' (reported only)' if t in REPORTED_KICKS else ''}: nodes logM1 "
      f"{', '.join(f'{v:.3f}' for v in PRED[t]['nodes'][0])} eps {', '.join(f'{v:.3f}' for v in PRED[t]['nodes'][1])}; groups eps "
      f"{full.min():.3f}-{full.max():.3f}; slope d eps / d log10 M500 = {PRED[t]['slope_full']:+.3f} +- {PRED[t]['slope_err68']:.3f} (68 %, bootstrap)")

# ------------------------------------------------------------------ data side: UA1's joint draws
def ua1_draws(a0, f):
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
def resid(Z, eps_pt, a0, mode="law", rc=RC):
    if mode == "law": return Z["D"] - dlaw(Z["bI"] + rc * eps_pt, Z["gN"], a0)
    return Z["D"] - np.log10((gl(Z["bI"] * Z["gN"], a0) + rc * eps_pt * Z["gN"]) / gl(Z["gN"], a0))   # Newtonian-additive carrier
def step(Z, eps_g, a0, mode="law", rc=RC):                    # eps_g (NDRAW, 20) -> UA1 statistic per draw
    r = resid(Z, np.repeat(eps_g, 2, axis=1), a0, mode, rc)
    return np.median(r[np.arange(NDRAW)[:, None], Z["sel"]], axis=1)
def need(Z, a0, mode="law", rc=RC):
    lo = (0.01 - Z["bI"].reshape(NDRAW, NG, 2).min(-1)) / rc; hi = np.full((NDRAW, NG), 10.0)
    if mode != "law": lo = -0.99 * (gl(Z["bI"] * Z["gN"], a0) / Z["gN"]).reshape(NDRAW, NG, 2).min(-1) / rc
    for _ in range(60):
        mid = 0.5 * (lo + hi); r = resid(Z, np.repeat(mid, 2, axis=1), a0, mode, rc).reshape(NDRAW, NG, 2).mean(-1)
        lo = np.where(r > 0, mid, lo); hi = np.where(r > 0, hi, mid)
    return 0.5 * (lo + hi)
def q(x): return dict(median=float(np.median(x)), lo68=float(np.percentile(x, 16)), hi68=float(np.percentile(x, 84)),
                      lo95=float(np.percentile(x, 2.5)), hi95=float(np.percentile(x, 97.5)))
def c95(x): lo, hi = np.percentile(x, [2.5, 97.5]); return bool(lo <= 0 <= hi)

def grade(Z, a0, f, en, bdat, t, pred_full, pred_bs, mode="law", rc=RC, flat=False):
    pb = pred_bs[np.arange(NDRAW) % NB]                                      # paired bootstrap set per draw
    if flat: pb = np.repeat(pb.mean(1, keepdims=True), NG, axis=1)
    bp = np.zeros(NDRAW) if flat else ols(LM500[None], pb)
    dA = bdat - bp; A_ok = c95(dA); A_power = not c95(bdat)
    sB = step(Z, pb, a0, mode, rc); B_ok = c95(sB)
    lab = "FAIL" if (not B_ok or (A_power and not A_ok)) else ("PASS" if A_power else "NO POWER")
    pmed = np.repeat(np.mean(pred_full, keepdims=True), NG) if flat else pred_full
    inside = int(sum(np.percentile(en[:, k], 2.5) <= pmed[k] <= np.percentile(en[:, k], 97.5) for k in range(NG)))
    return dict(pred_slope_paired=q(bp), A_delta=q(dA), A_pass=A_ok, A_power=A_power, B_step=q(sB), B_pass=B_ok, label=lab, groups_need95_contains_pred=inside)

for f, a0 in A0.items():
    P(f"\n================ [{f}] a0 {a0:.4e}")
    Z = ua1_draws(a0, f); R = {}; RES["footings"][f] = R
    # KA2: eps = 0 reproduces UA1 to 0
    s0 = step(Z, np.zeros((NDRAW, NG)), a0); ref = post_groups2(a0, f, SPM, GS)
    eqa = bool(np.array_equal(s0, ref)); eqj = summ(s0) == UA1J["footings"][f]["cells"]["groups"]["post"]
    RES["KA"][f"KA2_UA1_{f}"] = dict(array_equal=eqa, summary_equals_ua1_json=eqj, ok=bool(eqa and eqj))
    P(f"KA2 eps = 0 vs UA1 post_groups2: array_equal {eqa}; summary == ua1.json {eqj} (median {summ(s0)['median']:+.3f}) -> {'PASS' if eqa and eqj else 'FAIL'}")
    if not all(v["ok"] for v in RES["KA"].values()): P("KA FAILURE: grading stops"); break
    en = need(Z, a0); rb2 = np.random.default_rng(3301 + (0 if f == "canonical" else 1)); gi = rb2.integers(0, NG, (NDRAW, NG))
    bdat = ols(LM500[gi], en[np.arange(NDRAW)[:, None], gi]); bdat_sig = ols(LSIG[gi], en[np.arange(NDRAW)[:, None], gi])
    R["per_group_need"] = {NAMES[k]: dict(log10_M500=float(LM500[k]), log10_M1=float(LM1[k]), log10_sigma_kT=float(LSIG[k]), **q(en[:, k])) for k in range(NG)}
    R["data_slope_vs_log10M500"] = q(bdat); R["data_slope_vs_log10sigma_kT_reported"] = q(bdat_sig)
    P(f"per-group need eps (median, 95 %), ordered by M500:")
    for k in np.argsort(LM500):
        n_ = R["per_group_need"][NAMES[k]]
        P(f"   {NAMES[k]:16s} logM500 {LM500[k]:.3f} logM1 {LM1[k]:.3f}  need {n_['median']:+.3f} [{n_['lo95']:+.3f}, {n_['hi95']:+.3f}]  "
          f"pred 550/575/600 {PRED['v550']['full'][k]:.3f}/{PRED['v575']['full'][k]:.3f}/{PRED['v600']['full'][k]:.3f}")
    qd = R["data_slope_vs_log10M500"]
    P(f"DATA slope d eps_need / d log10 M500: {qd['median']:+.3f}, 68 % [{qd['lo68']:+.3f}, {qd['hi68']:+.3f}], 95 % [{qd['lo95']:+.3f}, {qd['hi95']:+.3f}]"
      f"  (vs log10 sigma_kT, reported: {R['data_slope_vs_log10sigma_kT_reported']['median']:+.3f})")
    R["kicks"] = {}
    for t in KICKS + REPORTED_KICKS:
        pr = PRED[t]; o = grade(Z, a0, f, en, bdat, t, pr["full"], pr["bs"]); fl = grade(Z, a0, f, en, bdat, t, pr["full"], pr["bs"], flat=True)
        sens = dict(flat_below=grade(Z, a0, f, en, bdat, t, *predict(t, "flat")),
                    M1_times_h=grade(Z, a0, f, en, bdat, t, *predict(t, "linear", LM1 + math.log10(hh))))
        o.update(pred_slope=dict(full=pr["slope_full"], median=pr["slope_med"], err68=pr["slope_err68"]), pred_slope_vs_sigma_kT_reported=pr["slope_sigma_full"],
                 flat_MUTATE=fl, sensitivities_reported=sens, extrapolated_not_run=(t == "v550"), reported_only=(t in REPORTED_KICKS))
        R["kicks"][t] = o
        if MUT:
            P(f"  [{t}] FLAT retention eps {pr['full'].mean():.3f}: A delta = b_data 95 % [{fl['A_delta']['lo95']:+.3f}, {fl['A_delta']['hi95']:+.3f}] -> flat "
              f"{'PASSES A: slope test has NO POWER' if fl['A_pass'] else 'FAILS A: slope test has power (MUTATE bites)'}; B step {fl['B_step']['median']:+.3f} "
              f"[{fl['B_step']['lo95']:+.3f}, {fl['B_step']['hi95']:+.3f}] {'pass' if fl['B_pass'] else 'fail'}")
        else:
            P(f"  [{t}{' extrapolated, not a run' if t == 'v550' else ''}{' REPORTED ONLY' if t in REPORTED_KICKS else ''}] pred slope {pr['slope_full']:+.3f} +- {pr['slope_err68']:.3f}; "
              f"A delta (data - pred) {o['A_delta']['median']:+.3f} 95 % [{o['A_delta']['lo95']:+.3f}, {o['A_delta']['hi95']:+.3f}] -> {'pass' if o['A_pass'] else 'FAIL'}"
              f" (power: flat {'fails' if o['A_power'] else 'PASSES'}); B step with carrier {o['B_step']['median']:+.3f} 95 % [{o['B_step']['lo95']:+.3f}, "
              f"{o['B_step']['hi95']:+.3f}] -> {'pass' if o['B_pass'] else 'FAIL'}; groups with pred in need 95 %: {o['groups_need95_contains_pred']}/20  => {o['label']}")
            for nm_, v_ in sens.items():
                P(f"        sensitivity (reported) {nm_}: pred slope {v_['pred_slope_paired']['median']:+.3f} [68 % {v_['pred_slope_paired']['lo68']:+.3f}, {v_['pred_slope_paired']['hi68']:+.3f}]; "
                  f"A delta 95 % [{v_['A_delta']['lo95']:+.3f}, {v_['A_delta']['hi95']:+.3f}] {'pass' if v_['A_pass'] else 'FAIL'}; B {v_['B_step']['median']:+.3f} "
                  f"[{v_['B_step']['lo95']:+.3f}, {v_['B_step']['hi95']:+.3f}] {'pass' if v_['B_pass'] else 'FAIL'}; pred in need 95 % {v_['groups_need95_contains_pred']}/20 => {v_['label']}")
    if not MUT:   # carrier-convention sensitivities at the graded kicks (reported only)
        R["convention_sensitivity_reported"] = {}
        for mode, rc, nm in (("law", 5.36, "R_c 5.36"), ("add", RC, "Newtonian-additive carrier")):
            en2 = en if (mode == "law" and rc == RC) else need(Z, a0, mode, rc)
            b2 = ols(LM500[gi], en2[np.arange(NDRAW)[:, None], gi])
            R["convention_sensitivity_reported"][nm] = {"data_slope": q(b2), **{t: grade(Z, a0, f, en2, b2, t, PRED[t]["full"], PRED[t]["bs"], mode, rc)["label"] for t in KICKS}}
            P(f"  convention (reported) {nm}: data slope {np.median(b2):+.3f}; labels " + ", ".join(f"{t} {R['convention_sensitivity_reported'][nm][t]}" for t in KICKS))
        del en2
    del Z, en

RES["labels"] = {f: {t: RES["footings"][f]["kicks"][t]["label"] for t in KICKS} for f in RES["footings"] if "kicks" in RES["footings"][f]}
RES["predicted_slope"] = {t: dict(full=PRED[t]["slope_full"], err68=PRED[t]["slope_err68"]) for t in KICKS + REPORTED_KICKS}
RES["KA_all"] = all(v["ok"] for v in RES["KA"].values())
RES["peak_rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)
P(f"\nLABELS (A slope, B class step; v550 extrapolated, not a run): {RES.get('labels')}")
P(f"KA all pass: {RES['KA_all']}; peak RSS {RES['peak_rss_GB']:.2f} GB")
P("Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
if MUT:
    open(os.path.join(HERE, "ck3_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
else:
    json.dump(RES, open(os.path.join(HERE, "ck3.json"), "w"), indent=1)
    open(os.path.join(HERE, "ck3.out"), "w").write("\n".join(OUT) + "\n")
