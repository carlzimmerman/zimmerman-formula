#!/usr/bin/env python3
"""SE2 (criteria f49a99a04c): the hot/cold step as systematics, one joint posterior per class.
    python3 se2.py           -> se2.json / se2.out
    python3 se2.py --mutate  -> se2_MUTATE.json / se2_MUTATE.out   (M1 inverted IMF bracket; M2 zero-width priors)
GB1's loaders and gates exec'd read-only; ST1's script exec'd read-only for KA1 (its writes go to a temp dir).
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math, csv, re, io, tempfile, contextlib, builtins
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); CL = os.path.dirname(HERE); REPO = os.path.dirname(CL)
RB = os.path.join(REPO, "rebuild_2026_10_22"); DATA = os.path.join(REPO, "real_research", "data")
MUTATE = "--mutate" in sys.argv; TAG = "se2_MUTATE" if MUTATE else "se2"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(s)
LN10 = math.log(10); NDRAW = 20000

# ------------------------------------------------------------------ GB1, read-only, up to its main block
GBP = os.path.join(CL, "GB1_all_gates_battery", "gb1.py"); src = open(GBP).read()
cut = src.index("# ------------------------------------------------------------------ main")
NS = {"__file__": GBP, "__name__": "gb1_lib"}
_a = sys.argv; sys.argv = [sys.argv[0]]; exec(compile(src[:cut], "gb1_lib", "exec"), NS); sys.argv = _a
A0 = NS["A0"]; LSTAR = NS["LSTAR"]; G = NS["G"]; MS = NS["MS"]; KPC = NS["KPC"]
for k in ("g_sparc", "g_xcop", "g_groups", "g_ell", "g_udg", "g_dsph", "g_kids", "L0", "L1", "delta", "alpha", "groups_pts", "build",
          "udgs", "dsphs", "kids", "R1", "X1R", "LW", "GRADED_D", "DX", "STOT", "K_TO_S", "GR", "XC", "UROWS", "glaw"):
    globals()[k] = NS[k]
GB = json.load(open(os.path.join(CL, "GB1_all_gates_battery", "gb1.json")))
ST1J = json.load(open(os.path.join(CL, "ST1_multi_cause_step", "st1.json")))
RES = dict(tag=TAG, criteria="f49a99a04c", note="kappa = 1/2 FITTED; not theory closed; adopts nothing", footings={}, KA={})
P(f"SE2 step as systematics {'MUTATE' if MUTATE else 'MAIN'}. kappa = 1/2 FITTED; not theory closed; footings never pooled.")

def gl(g, a0): return 0.5 * g + np.sqrt(0.25 * g * g + a0 * g)          # GB1's glaw, vectorised (same formula)
def dlaw(b, gN, a0): return np.log10(gl(b * gN, a0) / gl(gN, a0))         # GB1 delta() for b != 1, F = 1, T = 0

# ------------------------------------------------------------------ KA1: ST1 exec'd read-only, writes redirected
def ka1_st1():
    tmp = tempfile.mkdtemp(prefix="se2_st1_replay_"); captured = {}
    def ropen(path, mode="r", *a, **kw):
        if any(c in mode for c in "wa+"):
            p2 = os.path.join(tmp, os.path.basename(path)); captured[os.path.basename(path)] = p2
            return builtins.open(p2, mode, *a, **kw)
        return builtins.open(path, mode, *a, **kw)
    sp = os.path.join(CL, "ST1_multi_cause_step", "st1.py"); s = builtins.open(sp).read()
    ns = {"__file__": sp, "__name__": "st1_replay", "open": ropen}
    _a = sys.argv; sys.argv = [sp]; buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf): exec(compile(s, "st1_replay", "exec"), ns)
    except SystemExit as e: code = e.code
    else: code = None
    finally: sys.argv = _a
    new = json.load(builtins.open(captured["st1.json"]))
    nd, ns_, diffs = [0], [0], []
    def cmp(a, b, path):
        if isinstance(a, dict) and isinstance(b, dict):
            if set(a) != set(b): diffs.append((path, "keys")); return
            for k in a: cmp(a[k], b[k], path + "/" + str(k))
        elif isinstance(a, list) and isinstance(b, list):
            if len(a) != len(b): diffs.append((path, "len")); return
            for i, (x, y) in enumerate(zip(a, b)): cmp(x, y, path + f"[{i}]")
        elif isinstance(a, bool) or isinstance(b, bool) or isinstance(a, str) or a is None:
            ns_[0] += 1
            if a != b: diffs.append((path, a, b))
        else:
            nd[0] += 1
            if not (a == b or (isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b))): diffs.append((path, a, b))
    cmp(new, ST1J, "")
    return dict(n_numeric=nd[0], n_other=ns_[0], n_diff=len(diffs), diffs=diffs[:10], exit=code, ok=len(diffs) == 0)
K1 = ka1_st1(); RES["KA"]["KA1_ST1_to_0"] = K1
P(f"KA1 ST1 replay (st1.py exec'd read-only, writes redirected): {K1['n_numeric']} numbers + {K1['n_other']} labels vs committed st1.json: "
  f"{K1['n_diff']} differ -> {'PASS (difference 0)' if K1['ok'] else 'FAIL'}")

# ------------------------------------------------------------------ inputs per footing
def lvd_rows():
    o = {}
    for fn in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv", "lvd_dwarf_local_field_distant.csv"):
        p = os.path.join(DATA, "dsph", fn)
        if not os.path.exists(p): continue
        for r in csv.DictReader(open(p)): o.setdefault(r["name"], r)
    return o
LVD = lvd_rows()
def norm(n): n = n.lower().replace("andromeda", "and"); return re.sub(r"[\s()\-_]", "", n)
ALT = {"collins": {}, "mcc": {}}
for l in open(os.path.join(DATA, "dsph", "collins2013_m31_dsph.tsv")):
    if l.startswith("#") or not l.strip(): continue
    c = l.rstrip("\n").split("\t")
    if c[0].strip() in ("recno", "") or c[0].startswith("-"): continue
    try: sv = float(c[18])
    except ValueError: continue
    if sv > 0: ALT["collins"][norm(c[1].strip())] = sv
for r in csv.DictReader(open(os.path.join(DATA, "dsph", "mcconnachie2012_dsph.csv"))):
    try: sv = float(r["sigma*"])
    except ValueError: continue
    if sv > 0: ALT["mcc"][norm(r["Name"])] = sv
ALTCAT = {"bright M31": "collins", "MW classical": "mcc", "LG field": "mcc", "MW ultra-faint": "mcc", "M31 others": "collins"}
VC = {"MW": 200.0, "M31": 230.0}; TAU_LINE = 0.375; PERI = 3 ** (2 / 3)
DCLS = ("bright M31", "MW classical", "LG field", "MW ultra-faint", "M31 others"); GRADED = ("bright M31", "MW classical"); CONTROL = ("LG field",)

def dsph_admiss(f, name, scale=1.0):
    r = NS["X1R"].get((f, name))
    if r is None or r["host"] not in VC: return dict(A1=True, A2=True, tau=None, tc_to=None, host=None if r is None else r["host"])
    Re = float(r["rh_pc"]); sg = float(r["sigma"]); d = float(r["d_host_kpc"]) * 1e3; V = VC[r["host"]]
    GPC = 4.30091e-3; MW_ = 4 * sg ** 2 * Re / GPC; Mh = V ** 2 * d / GPC
    tau = Re / (d * (MW_ / (3 * Mh)) ** (1 / 3)); tc = (4 / 3) * Re / sg; to = 2 * math.pi * d / V
    return dict(A1=bool(tau * scale < TAU_LINE), A2=bool(tc <= 0.1 * to), tau=tau, tc_to=tc / to, host=r["host"])
def udg_admiss(r, a0, scale=1.0):
    Re = float(r["Re_kpc"]) * KPC; sg = float(r["sigma"]) * 1e3; d = float(r["d_mean_kpc"]) * KPC; g = float(r["x_e_dmean"]) * a0
    tau = Re / (d * (4 * sg ** 2 * Re / (3 * g * d * d)) ** (1 / 3)); V = math.sqrt(g * d); tc = (4 / 3) * Re / sg; to = 2 * math.pi * d / V
    return dict(A1=bool(tau * scale < TAU_LINE), A2=bool(tc <= 0.1 * to), tau=tau, tc_to=tc / to)

def se_conv(E, sE):
    n = len(E); return max(float(np.std(E, ddof=1) / math.sqrt(n)), float(math.sqrt(np.sum(np.asarray(sE) ** 2)) / n))

# ------------------------------------------------------------------ prior specs
def SPEC(kind="main"):
    s = dict(lam=(1.0, 1.0, "ge0"), s_sig=(1.0, 0.1), sig_early=(130.0, 210.0), sig_xcop=(250.0, 350.0), sig_grp=(200.0, 300.0),
             fst=(0.0, 1.0), ups=(0.0, 0.30), q=(0.0, 0.5), ul=True, dist=1.0, aniso=1.0, memb=1.0, udg=1.0)
    if kind == "mutate": s["lam"] = (-1.0, 1.0, "le0")
    if kind == "x2":
        s.update(lam=(1.0, 2.0, "ge0"), s_sig=(1.0, 0.2), sig_early=(90.0, 250.0), sig_xcop=(200.0, 400.0), sig_grp=(150.0, 350.0),
                 fst=(0.0, 1.0), ups=(0.0, 0.60), q=(0.0, 1.0), dist=2.0, aniso=2.0, memb=2.0, udg=2.0)
    if kind == "half":   # post-freeze sensitivity (reported): every stated edge read as 2 sigma instead of 1 sigma
        s.update(lam=(1.0, 0.5, "ge0"), s_sig=(1.0, 0.05), sig_early=(150.0, 190.0), sig_xcop=(275.0, 325.0), sig_grp=(225.0, 275.0),
                 fst=(0.25, 0.75), ups=(0.0, 0.15), q=(0.125, 0.375), dist=0.5, aniso=0.5, memb=0.5, udg=0.5)
    if kind.startswith("zero"):   # M2: every knob pinned at the GB1 L0 nominal (Kroupa, Upsilon 2, no gas, no shifts)
        fz = float(kind.split(":")[1]) if ":" in kind else 0.0
        s.update(lam=(0.0, 0.0, "none"), s_sig=(1.0, 0.0), sig_early=(170.0, 170.0), sig_xcop=(300.0, 300.0), sig_grp=(250.0, 250.0),
                 fst=(fz, fz), ups=(0.0, 0.0), q=(0.0, 0.0), ul=False, dist=0.0, aniso=0.0, memb=0.0, udg=0.0)
    return s
def draw_lam(rng, spec, n):
    mu, sd, tr = spec["lam"]
    if sd == 0: return np.full(n, mu)
    x = rng.normal(mu, sd, n)
    for _ in range(200):
        bad = (x < 0) if tr == "ge0" else ((x > 0) if tr == "le0" else np.zeros(n, bool))
        if not bad.any(): break
        x[bad] = rng.normal(mu, sd, bad.sum())
    return x
def uni(rng, lohi, n): lo, hi = lohi; return np.full(n, lo) if hi == lo else rng.uniform(lo, hi, n)
def fimf(sig, rsk): return np.maximum(10 ** (0.38 * np.log10(np.asarray(sig, float) / 200.0) - 0.06) * rsk, 1.0)   # GB1 b_imf: max(alpha R_SK, 1)

SEEDS = {"ellipticals": 101, "KiDS": 102, "X-COP": 103, "groups": 104, "bright M31": 105, "MW classical": 106, "LG field": 107,
         "MW ultra-faint": 108, "M31 others": 109, "Coma UDGs": 110}
def rngs(cls, f): b = SEEDS[cls] * 10 + (0 if f == "canonical" else 1); return np.random.default_rng(b), np.random.default_rng(b + 500000)

# ------------------------------------------------------------------ class posteriors (stat stream and nuisance stream separate)
def post_ell(B, a0, f, spec, nominal=False):
    rs, rn = rngs("ellipticals", f); E = B["E"]; names = sorted({p["name"] for p in E}); gi = np.array([names.index(p["name"]) for p in E])
    D = np.array([p["D"] for p in E]); gN = np.array([p["feat"]["x"] * a0 for p in E])
    sig = np.array([p["feat"]["stars"][0]["sigma"] for p in E]); rsk = np.array([p["feat"]["stars"][0]["rsk"] for p in E])
    sh = np.array([p["feat"]["stars"][0]["share"] for p in E])
    lam = draw_lam(rn, spec, NDRAW); s = rn.normal(spec["s_sig"][0], spec["s_sig"][1], NDRAW) if spec["s_sig"][1] > 0 else np.full(NDRAW, spec["s_sig"][0])
    if nominal: lam = np.zeros(NDRAW); s = np.ones(NDRAW)
    b = 1 + sh[None] * (fimf(sig[None] * s[:, None], rsk[None]) ** lam[:, None] - 1)
    res = D[None] - dlaw(b, gN[None], a0)                                     # (N, 21)
    gm = np.stack([res[:, gi == k].mean(axis=1) for k in range(len(names))], axis=1)   # galaxy means (equal 3 points)
    ix = rs.integers(0, len(names), (NDRAW, len(names)))
    return gm[np.arange(NDRAW)[:, None], ix].mean(axis=1), dict(n=len(names), line=0.15)
def post_kids(B, a0, f, spec, nominal=False):
    rs, rn = rngs("KiDS", f); Ee, Ll = B["K"]; gN = np.array([e["x"] * a0 for e in Ee])
    lam = draw_lam(rn, spec, NDRAW); se = uni(rn, spec["sig_early"], NDRAW)
    if nominal: lam = np.zeros(NDRAW)
    fl = fimf(np.array([60.0]), K_TO_S)[0]                                     # late: Kroupa floor (1.0)
    be = fimf(se, K_TO_S)[:, None] ** lam[:, None] * np.ones((1, len(gN))); bl = fl ** lam[:, None] * np.ones((1, len(gN)))
    dc = (dlaw(be, gN[None], a0) - dlaw(bl, gN[None], a0)).mean(axis=1)
    return (DX - dc) + rs.normal(0, STOT, NDRAW), dict(n=len(gN), line=2 * STOT)
def post_xcop(B, a0, f, spec, nominal=False):
    rs, rn = rngs("X-COP", f); X = B["X"]; nm = [z["name"] for z in XC]; cl = sorted(set(nm)); gi = np.array([cl.index(n) for n in nm])
    D = np.array([p["D"] for p in X]); gN = np.array([p["feat"]["x"] * a0 for p in X]); sh = np.array([p["feat"]["stars"][0]["share"] for p in X])
    lam = draw_lam(rn, spec, NDRAW); sg = uni(rn, spec["sig_xcop"], NDRAW)
    if nominal: lam = np.zeros(NDRAW)
    b = 1 + sh[None] * (fimf(sg, K_TO_S)[:, None] ** lam[:, None] - 1)
    res = D[None] - dlaw(b, gN[None], a0); cm = np.stack([res[:, gi == k].mean(axis=1) for k in range(len(cl))], axis=1)
    ix = rs.integers(0, len(cl), (NDRAW, len(cl)))
    return cm[np.arange(NDRAW)[:, None], ix].mean(axis=1), dict(n=len(cl), line=0.05)
GRAW = []
for gp in GR:
    for p in gp["pts"]: GRAW.append((gp["name"], p["r_kpc"], p["M_gas"], p["M_obs"]))
def groups_res(a0, fst, lam, sg):
    """residual per point under plain law with baryons M_gas (1 + f*) and IMF on the stellar share; arrays (N, 40)."""
    rm = np.array([r for _, r, _, _ in GRAW]) * KPC; Mg = np.array([m for _, _, m, _ in GRAW]); Mo = np.array([m for _, _, _, m in GRAW])
    fst = np.asarray(fst)[:, None]; Mb = Mg[None] * (1 + fst); gN = G * Mb * MS / rm[None] ** 2
    Ml = gl(gN, a0) * rm[None] ** 2 / G / MS; D = np.log10(Mo[None] / Ml); sh = fst / (1 + fst)
    b = 1 + sh * (fimf(np.asarray(sg), K_TO_S)[:, None] ** np.asarray(lam)[:, None] - 1)
    return D - dlaw(b, gN, a0)
def post_groups(B, a0, f, spec, nominal=False, fst_fixed=None):
    rs, rn = rngs("groups", f); gnames = [g for g, _, _, _ in GRAW]; gs = sorted(set(gnames), key=gnames.index)
    lam = draw_lam(rn, spec, NDRAW); sg = uni(rn, spec["sig_grp"], NDRAW); fst = uni(rn, spec["fst"], NDRAW)
    if nominal: lam = np.zeros(NDRAW)
    if fst_fixed is not None: fst = np.full(NDRAW, fst_fixed)
    res = groups_res(a0, fst, lam, sg); pidx = [np.where(np.array(gnames) == g)[0] for g in gs]
    ix = rs.integers(0, len(gs), (NDRAW, len(gs)))
    pts = np.stack(pidx)                                                    # (20, 2)
    sel = pts[ix].reshape(NDRAW, -1)                                        # (N, 40)
    return np.median(res[np.arange(NDRAW)[:, None], sel], axis=1), dict(n=len(gs), line=None)

def dsph_inputs(B, f):
    out = {}
    for c in DCLS:
        rows = []
        for p in B["D"][c]:
            n = p["name"]; x1 = NS["X1R"][(f, n)]; lv = LVD.get(n, {})
            mhi = lv.get("mass_HI", "") or ""; ul = lv.get("mass_HI_ul", "") or ""
            em, ep = lv.get("distance_modulus_em", "") or "", lv.get("distance_modulus_ep", "") or ""
            sd = ((float(em) + float(ep)) / 2 / 5) if (em and ep) else 0.0
            ev = x1.get("Delta[v3 L*floor E-V]", ""); ew = x1.get("Delta[v3 L*floor]", "")
            rows.append(dict(name=n, D=p["D"], x=p["feat"]["x"], Ms=10 ** float(x1["logMstar"]), MHI=(10 ** float(mhi)) if mhi else 0.0,
                             UL=(10 ** float(ul)) if (ul and not mhi) else 0.0, sd_logd=sd, has_dm=bool(em and ep), has_lvd=bool(lv),
                             aniso=abs(float(ev) - float(ew)) if (ev and ew) else None, sig=float(x1["sigma"]),
                             adm=dsph_admiss(f, n), adm_peri=dsph_admiss(f, n, PERI)))
        out[c] = rows
    # anisotropy and membership widths per class
    W = {}; pooled = []
    for c in DCLS:
        an = [r["aniso"] for r in out[c] if r["aniso"] is not None]
        cat = ALT[ALTCAT[c]]; lr = [math.log10(r["sig"] / cat[norm(r["name"])]) for r in out[c] if norm(r["name"]) in cat]
        if c in GRADED + CONTROL: pooled += lr
        W[c] = dict(a_c=float(np.median(an)) if an else 0.0, n_aniso=len(an), memb_lr=lr)
    for c in DCLS:
        lr = W[c]["memb_lr"]; use = lr if len(lr) >= 3 else pooled
        mu = float(np.mean(use)); rms = float(np.sqrt(np.mean(np.square(use)))); W[c].update(m_c=math.sqrt(mu ** 2 + (rms / math.sqrt(len(use))) ** 2),
                                                                                     memb_n=len(lr), memb_pooled=len(lr) < 3, memb_mu=mu, memb_rms=rms)
    return out, W
def post_dsph(c, rows, W, a0, anchor, f, spec, nominal=False, admit=True, dU_override=None):
    rs, rn = rngs(c, f)
    R = [r for r in rows if (r["adm"]["A1"] and r["adm"]["A2"])] if admit else rows
    n = len(R)
    if n == 0: return None, dict(n=0)
    D = np.array([r["D"] for r in R]); gN = np.array([r["x"] * a0 for r in R]); Ms = np.array([r["Ms"] for r in R])
    MHI = np.array([r["MHI"] for r in R]); UL = np.array([r["UL"] for r in R]); sdd = np.array([r["sd_logd"] for r in R])
    dU = rn.normal(spec["ups"][0], spec["ups"][1], NDRAW) if spec["ups"][1] > 0 else np.full(NDRAW, spec["ups"][0])
    q = uni(rn, spec["q"], NDRAW * n).reshape(NDRAW, n)
    mul = (UL[None] * rn.uniform(0, 1, (NDRAW, n))) if spec["ul"] else np.zeros((NDRAW, n))
    gas = 1.33 * (MHI[None] + mul)
    dd = rn.normal(0, 1, (NDRAW, n)) * sdd[None] * spec["dist"]
    da = rn.normal(0, 1, NDRAW) * W[c]["a_c"] * spec["aniso"]; ds = rn.normal(0, 1, NDRAW) * W[c]["m_c"] * spec["memb"]
    if dU_override is not None: dU = np.array(dU_override, float)
    if nominal: dU[:] = 0; q[:] = 0; gas[:] = 0; dd[:] = 0; da[:] = 0; ds[:] = 0
    Bf = 10 ** dU[:, None] + 2 * q * gas / Ms[None]
    Dp = D[None] + 2 * ds[:, None] + da[:, None] - dd - dlaw(Bf, gN[None], a0)
    ix = rs.integers(0, n, (NDRAW, n))
    return np.median(Dp[np.arange(NDRAW)[:, None], ix], axis=1) - anchor, dict(n=n)
def udg_inputs(f, a0):
    rows = [r for r in UROWS if r["footing"] == f]
    for r in rows: r["_adm"] = udg_admiss(r, a0); r["_adm_peri"] = udg_admiss(r, a0, PERI)
    base = R1[f"{f}|S4 v3 dmean L*floor E-W"]
    sk = dict(s_M=base["s_M"], s_A=base["s_A"], s_D=base["s_D"],
              s_aniso=abs(R1[f"{f}|v3 dmean L*floor E-V"]["meanE"] - base["meanE"]),
              s_mem=abs(R1[f"{f}|v3 all 11 Coma dmean L*floor"]["meanE"] - base["meanE"]),
              s_pos=abs(R1[f"{f}|S4 v3 dproj L*floor E-W"]["meanE"] - base["meanE"]))
    return rows, sk, base
def post_udg(rows, sk, f, spec, nominal=False, admit=True):
    rs, rn = rngs("Coma UDGs", f); R = [r for r in rows if r["_adm"]["A1"] and r["_adm"]["A2"]] if admit else rows
    n = len(R)
    if n < 2: return None, dict(n=n)
    E = np.array([float(r["E_v3_dmean"]) for r in R]); sE = np.array([float(r["sE"]) for r in R]); mE = float(E.mean()); se = se_conv(E, sE)
    shift = np.zeros(NDRAW)
    if not nominal:
        on = spec.get("udg_keys", ("s_M", "s_A", "s_D", "s_aniso", "s_mem", "s_pos"))
        for k in ("s_M", "s_A", "s_D", "s_aniso", "s_mem", "s_pos"): shift += rn.normal(0, 1, NDRAW) * sk[k] * spec["udg"] * (1.0 if k in on else 0.0)
    return (mE + shift + rs.normal(0, se, NDRAW)) / LN10, dict(n=n, meanE_ln=mE, se_ln=se)

def summ(x, line=None):
    q = np.percentile(x, [2.5, 16, 50, 84, 97.5]); sd = float(np.std(x))
    d = dict(median=float(q[2]), ci68=[float(q[1]), float(q[3])], ci95=[float(q[0]), float(q[4])], sd=sd, z=float(q[2] / sd) if sd > 0 else float("inf"),
             P_le0=float(np.mean(x <= 0)), contains0=bool(q[0] <= 0 <= q[4]))
    if line is not None: d["P_within_GB1_line"] = float(np.mean(np.abs(x) <= line))
    return d
def lab(post, raw, n, need_n):
    if need_n and n < 5: return "NOT A TEST (admissible N < 5)"
    if raw["contains0"]: return "NOT A TEST (no power: raw stat-only 95 % interval contains 0)"
    return "EXPLAINED" if post["contains0"] else "NOT EXPLAINED"

# ------------------------------------------------------------------ main loop
SPEC_MAIN = SPEC("mutate" if MUTATE else "main"); HOT = ("ellipticals", "KiDS", "X-COP", "groups", "bright M31", "MW classical", "Coma UDGs")
for f, a0 in A0.items():
    S, E, X = build(f, a0); GRp = {0: groups_pts(a0, 0.0), 1: groups_pts(a0, 1.0)}
    st = R1[f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / LN10
    B = dict(f=f, S=S, E=E, X=X, GR=GRp, U=udgs(f, a0), D=dsphs(f, a0), K=kids(a0), sigU=sigU)
    B["rms_L0"] = float(np.sqrt(np.mean([p["D"] ** 2 for p in S])))
    anchor = g_sparc(L0(f, a0), B, a0)[1]["Z"]; c0 = L0(f, a0); stj = ST1J["footings"][f]
    R = dict(anchor=anchor); RES["footings"][f] = R
    P(f"\n================ [{f}] a0 {a0:.4e}  Lstar {LSTAR[f]} pc  SPARC anchor Z {anchor:+.4f}  ({'M1 inverted IMF bracket' if MUTATE else 'main priors'})")
    dsI, W = dsph_inputs(B, f); uR, sk, ubase = udg_inputs(f, a0)

    # ---------------- KA2 / KA3 (main only)
    if not MUTATE:
        k2 = {}
        # ellipticals at lambda = 1, s = 1, all galaxies, no bootstrap
        Dm = np.array([p["D"] for p in E]); gN = np.array([p["feat"]["x"] * a0 for p in E]); s0 = E[0]["feat"]["stars"]
        b = np.array([1 + p["feat"]["stars"][0]["share"] * (fimf(np.array([p["feat"]["stars"][0]["sigma"]]), p["feat"]["stars"][0]["rsk"])[0] - 1) for p in E])
        k2["G4"] = abs(float(np.mean(Dm - dlaw(b, gN, a0))) - stj["G4"]["corrected"])
        Ee, Ll = B["K"]; gk = np.array([e["x"] * a0 for e in Ee])
        k2["G7"] = max(abs((DX - float(np.mean(dlaw(fimf(np.array([float(se_)]), K_TO_S)[0], gk, a0)))) - stj["G7"]["bracket"][str(se_)]["R"]) for se_ in (130, 170, 210))
        Dc = {c: [p for p in B["D"][c] if (dsph_admiss(f, p["name"])["tau"] is None or c not in GRADED) or dsph_admiss(f, p["name"])["tau"] < TAU_LINE] for c in B["D"]}
        ok6, n6 = g_dsph(c0, dict(B, D=Dc), a0)
        k2["G6"] = max(max(abs(n6[c]["median_minus_anchor"] - stj["G6"]["cut"]["num"][c]["median_minus_anchor"]), abs(n6[c]["ci"][0] - stj["G6"]["cut"]["num"][c]["ci"][0]),
                           abs(n6[c]["ci"][1] - stj["G6"]["cut"]["num"][c]["ci"][1])) for c in GRADED_D)
        edge = (st["s_M"] + st["s_A"] + st["s_D"]) / LN10; m5 = st["meanE"] / LN10
        k2["G5"] = max(abs(m5 / sigU - stj["G5"]["Q"]["z"]), abs((m5 - edge) - stj["G5"]["L"]["residual"]))
        xr = groups_res(a0, np.array([0.0]), np.array([0.0]), np.array([300.0]))[0]; xr1 = groups_res(a0, np.array([1.0]), np.array([0.0]), np.array([300.0]))[0]
        gg = g_groups(c0, B, a0)[1]; k2["G3"] = max(abs(float(np.median(xr)) - gg["fst0"]["median_res"]), abs(float(np.median(xr1)) - gg["fst1"]["median_res"]))
        Dx = np.array([p["D"] for p in X]); k2["G2"] = abs(float(np.mean(Dx)) - g_xcop(c0, B, a0)[1]["mean"])
        m2 = max(k2.values()); RES["KA"][f"KA2_{f}"] = dict(per=k2, maxdiff=m2, ok=m2 <= 1e-12)
        P(f"KA2 SE2 machinery at ST1's settings: " + ", ".join(f"{k} {v:.1e}" for k, v in k2.items()) + f" -> {'PASS' if m2 <= 1e-12 else 'FAIL'} (line 1e-12)")
        E9 = np.array([float(r["E_v3_dmean"]) for r in uR]); s9 = np.array([float(r["sE"]) for r in uR])
        k3 = max(abs(float(E9.mean()) - ubase["meanE"]), abs(se_conv(E9, s9) - ubase["se"])); RES["KA"][f"KA3_{f}"] = dict(maxdiff=k3, n=len(uR), ok=k3 <= 1e-12)
        P(f"KA3 9 Coma UDGs from the CSV vs S1 JSON (mean, se): max|d| {k3:.1e} -> {'PASS' if k3 <= 1e-12 else 'FAIL'}")

    # ---------------- admissibility
    adm = {}
    for c in DCLS:
        rr = dsI[c]; keep = [r["name"] for r in rr if r["adm"]["A1"] and r["adm"]["A2"]]
        adm[c] = dict(N=len(rr), N_adm=len(keep), removed_A1=[r["name"] for r in rr if not r["adm"]["A1"]], removed_A2=[r["name"] for r in rr if not r["adm"]["A2"]],
                      no_host_term=[r["name"] for r in rr if r["adm"]["tau"] is None],
                      peri_N_adm=sum(1 for r in rr if r["adm_peri"]["A1"] and r["adm_peri"]["A2"]),
                      tau_max_kept=max([r["adm"]["tau"] for r in rr if r["adm"]["tau"] is not None and r["name"] in keep], default=None),
                      tc_to_max=max([r["adm"]["tc_to"] for r in rr if r["adm"]["tc_to"] is not None], default=None))
    adm["Coma UDGs"] = dict(N=len(uR), N_adm=sum(1 for r in uR if r["_adm"]["A1"] and r["_adm"]["A2"]),
                            removed_A1=[r["name"] for r in uR if not r["_adm"]["A1"]], removed_A2=[r["name"] for r in uR if not r["_adm"]["A2"]],
                            peri_N_adm=sum(1 for r in uR if r["_adm_peri"]["A1"] and r["_adm_peri"]["A2"]),
                            tau=[r["_adm"]["tau"] for r in uR], tc_to=[r["_adm"]["tc_to"] for r in uR])
    R["admissibility"] = adm
    for c, a in adm.items():
        P(f"ADMISSIBILITY {c:15s}: {a['N_adm']}/{a['N']} admissible; removed A1 {', '.join(a['removed_A1']) or 'none'}; A2 {', '.join(a['removed_A2']) or 'none'}"
          + (f"; no host term (kept) {len(a['no_host_term'])}" if a.get("no_host_term") else "") + f"; pericentre reading {a['peri_N_adm']}/{a['N']} (reported)")
    if True:   # per-footing prior widths
        R["dsph_widths"] = {c: dict(a_c=W[c]["a_c"], m_c=W[c]["m_c"], memb_n=W[c]["memb_n"], memb_pooled=W[c]["memb_pooled"], memb_mu=W[c]["memb_mu"], memb_rms=W[c]["memb_rms"],
                                    n_gas_measured=sum(1 for r in dsI[c] if r["MHI"] > 0), n_gas_ul=sum(1 for r in dsI[c] if r["UL"] > 0),
                                    n_no_lvd=sum(1 for r in dsI[c] if not r["has_lvd"]), n_no_dm=sum(1 for r in dsI[c] if not r["has_dm"])) for c in DCLS}
        R["udg_widths_ln"] = sk
        for c in DCLS:
            w = R["dsph_widths"][c]
            P(f"   priors {c:15s}: anisotropy a_c {w['a_c']:.4f} dex (N {W[c]['n_aniso']}); membership m_c {w['m_c']:.4f} dex in log sigma (matched {w['memb_n']}{', pooled' if w['memb_pooled'] else ''}; mu {w['memb_mu']:+.3f} rms {w['memb_rms']:.3f}); "
              f"gas measured {w['n_gas_measured']}, UL {w['n_gas_ul']}; no LVD row {w['n_no_lvd']}, no DM error {w['n_no_dm']}")
        P("   priors Coma UDGs (ln, 1 sigma): " + ", ".join(f"{k} {v:.4f}" for k, v in sk.items()))

    # ---------------- posteriors
    cells = {}
    def run(name, fn_main, fn_raw, need_n, line=None, extra=None):
        xm, im = fn_main(); xr, ir = fn_raw()
        if xm is None: cells[name] = dict(label="NOT A TEST (admissible N < 5)", n=im["n"]); return
        pm = summ(xm, line); pr = summ(xr, line); L = lab(pm, pr, im["n"], need_n)
        cells[name] = dict(post=pm, raw_stat_only=pr, n=im["n"], label=L, **(extra or {}))
    run("ellipticals", lambda: post_ell(B, a0, f, SPEC_MAIN), lambda: post_ell(B, a0, f, SPEC_MAIN, nominal=True), False, 0.15)
    run("KiDS", lambda: post_kids(B, a0, f, SPEC_MAIN), lambda: post_kids(B, a0, f, SPEC_MAIN, nominal=True), False, 2 * STOT)
    run("X-COP", lambda: post_xcop(B, a0, f, SPEC_MAIN), lambda: post_xcop(B, a0, f, SPEC_MAIN, nominal=True), False, 0.05)
    xg, ig = post_groups(B, a0, f, SPEC_MAIN); g0, _ = post_groups(B, a0, f, SPEC_MAIN, nominal=True, fst_fixed=0.0); g1, _ = post_groups(B, a0, f, SPEC_MAIN, nominal=True, fst_fixed=1.0)
    pg = summ(xg); r0 = summ(g0); r1 = summ(g1); raw_g = dict(r0, contains0=bool(r0["contains0"] and r1["contains0"]))
    cells["groups"] = dict(post=pg, raw_stat_only=r0, raw_stat_only_fst1=r1, n=ig["n"], label=lab(pg, raw_g, ig["n"], False))
    for c in DCLS:
        run(c, lambda c=c: post_dsph(c, dsI[c], W, a0, anchor, f, SPEC_MAIN), lambda c=c: post_dsph(c, dsI[c], W, a0, anchor, f, SPEC_MAIN, nominal=True), True)
        x_all, _ = post_dsph(c, dsI[c], W, a0, anchor, f, SPEC_MAIN, admit=False)
        if c in cells and "post" in cells[c]: cells[c]["all_systems_reported"] = summ(x_all)
    run("Coma UDGs", lambda: post_udg(uR, sk, f, SPEC_MAIN), lambda: post_udg(uR, sk, f, SPEC_MAIN, nominal=True), True)
    # widths x2 sensitivity (reported) -- main only
    if not MUTATE:
        S2 = SPEC("x2")
        sens = {"ellipticals": post_ell(B, a0, f, S2)[0], "KiDS": post_kids(B, a0, f, S2)[0], "X-COP": post_xcop(B, a0, f, S2)[0], "groups": post_groups(B, a0, f, S2)[0],
                "Coma UDGs": post_udg(uR, sk, f, S2)[0]}
        for c in DCLS: sens[c] = post_dsph(c, dsI[c], W, a0, anchor, f, S2)[0]
        for k, v in sens.items():
            if v is not None and k in cells and "post" in cells[k]: cells[k]["widths_x2_reported"] = summ(v)
        SH = SPEC("half")
        sens = {"ellipticals": post_ell(B, a0, f, SH)[0], "KiDS": post_kids(B, a0, f, SH)[0], "X-COP": post_xcop(B, a0, f, SH)[0], "groups": post_groups(B, a0, f, SH)[0],
                "Coma UDGs": post_udg(uR, sk, f, SH)[0]}
        for c in DCLS: sens[c] = post_dsph(c, dsI[c], W, a0, anchor, f, SH)[0]
        for k, v in sens.items():
            if v is not None and k in cells and "post" in cells[k]: cells[k]["widths_half_post_freeze"] = summ(v)
        # M2 (zero-width priors at the L0 nominal) reproduce the no-nuisance stat posterior exactly
        m2 = []
        def eq(a, b): return bool(a is not None and b is not None and np.array_equal(a, b))
        Z = SPEC("zero"); Z1 = SPEC("zero:1")
        m2.append(eq(post_ell(B, a0, f, Z)[0], post_ell(B, a0, f, Z, nominal=True)[0])); m2.append(eq(post_kids(B, a0, f, Z)[0], post_kids(B, a0, f, Z, nominal=True)[0]))
        m2.append(eq(post_xcop(B, a0, f, Z)[0], post_xcop(B, a0, f, Z, nominal=True)[0]))
        m2.append(eq(post_groups(B, a0, f, Z)[0], post_groups(B, a0, f, Z, nominal=True, fst_fixed=0.0)[0])); m2.append(eq(post_groups(B, a0, f, Z1)[0], post_groups(B, a0, f, Z1, nominal=True, fst_fixed=1.0)[0]))
        for c in DCLS: m2.append(eq(post_dsph(c, dsI[c], W, a0, anchor, f, Z)[0], post_dsph(c, dsI[c], W, a0, anchor, f, Z, nominal=True)[0]))
        m2.append(eq(post_udg(uR, sk, f, Z)[0], post_udg(uR, sk, f, Z, nominal=True)[0]))
        RES["KA"][f"M2_zero_width_{f}"] = dict(n=len(m2), ok=all(m2)); P(f"M2 zero-width priors reproduce the no-nuisance posteriors: {sum(m2)}/{len(m2)} -> {'HOLDS' if all(m2) else 'FAILS'}")
    # ---------------- post-freeze diagnostic (reported only, labels unchanged): which knobs carry each width
    if not MUTATE:
        DG = {}
        def off(spec, k):
            s2 = dict(spec)
            if k == "IMF": s2["lam"] = (0.0, 0.0, "none")
            elif k == "sigma_scale": s2["s_sig"] = (1.0, 0.0)
            elif k == "sigma_e": s2["sig_early"] = (170.0, 170.0)
            elif k == "Upsilon": s2["ups"] = (0.0, 0.0)
            elif k == "gas": s2["q"] = (0.0, 0.0); s2["ul"] = False
            elif k in ("dist", "aniso", "memb"): s2[k] = 0.0
            return s2
        def only(spec, keep, allk):
            s2 = dict(spec)
            for k in allk:
                if k != keep: s2 = off(s2, k)
            return s2
        def dg(name, fn, allk):
            o = {}
            for k in allk:
                xo = fn(off(SPEC_MAIN, k)); xa = fn(only(SPEC_MAIN, k, allk))
                o[k] = dict(without=summ(xo), alone=summ(xa))
            DG[name] = o
        dg("ellipticals", lambda sp: post_ell(B, a0, f, sp)[0], ("IMF", "sigma_scale"))
        dg("KiDS", lambda sp: post_kids(B, a0, f, sp)[0], ("IMF", "sigma_e"))
        dg("bright M31", lambda sp: post_dsph("bright M31", dsI["bright M31"], W, a0, anchor, f, sp)[0], ("Upsilon", "gas", "dist", "aniso", "memb"))
        o = {}
        for fz in (0.0, 1.0):
            o[f"fst {fz:g}, IMF prior"] = summ(post_groups(B, a0, f, SPEC_MAIN, fst_fixed=fz)[0])
        o["fst U[0,1], Kroupa"] = summ(post_groups(B, a0, f, off(SPEC_MAIN, "IMF"))[0]); DG["groups"] = o
        uk = ("s_M", "s_A", "s_D", "s_aniso", "s_mem", "s_pos"); o = {}
        for k in uk:
            o[k] = dict(without=summ(post_udg(uR, sk, f, dict(SPEC_MAIN, udg_keys=tuple(x for x in uk if x != k)))[0]),
                        alone=summ(post_udg(uR, sk, f, dict(SPEC_MAIN, udg_keys=(k,)))[0]))
        DG["Coma UDGs"] = o
        dUs = np.random.default_rng(777 + (0 if f == "canonical" else 1)).normal(0, SPEC_MAIN["ups"][1], NDRAW)   # one Upsilon_V draw shared by both classes
        xb = post_dsph("bright M31", dsI["bright M31"], W, a0, anchor, f, SPEC_MAIN, dU_override=dUs)[0]
        xf = post_dsph("LG field", dsI["LG field"], W, a0, anchor, f, SPEC_MAIN, dU_override=dUs)[0]
        xb0 = post_dsph("bright M31", dsI["bright M31"], W, a0, anchor, f, SPEC_MAIN, nominal=True)[0]; xf0 = post_dsph("LG field", dsI["LG field"], W, a0, anchor, f, SPEC_MAIN, nominal=True)[0]
        DG["bright M31 minus LG field, shared Upsilon_V"] = dict(joint=summ(xb - xf), raw_stat_only=summ(xb0 - xf0), bright_M31_shared=summ(xb), LG_field_shared=summ(xf))
        R["diagnostic_post_freeze"] = DG
        for nm, o in DG.items():
            if nm.startswith("bright M31 minus"):
                P(f"DIAG (post-freeze, reported) {nm}: raw stat-only {o['raw_stat_only']['median']:+.3f} [{o['raw_stat_only']['ci95'][0]:+.3f},{o['raw_stat_only']['ci95'][1]:+.3f}]; joint {o['joint']['median']:+.3f} [{o['joint']['ci95'][0]:+.3f},{o['joint']['ci95'][1]:+.3f}] (LG field alone with the shared draw {o['LG_field_shared']['median']:+.3f} [{o['LG_field_shared']['ci95'][0]:+.3f},{o['LG_field_shared']['ci95'][1]:+.3f}])"); continue
            if nm == "groups":
                P(f"DIAG (post-freeze, reported) groups: " + "; ".join(f"{k} {v['median']:+.3f} [{v['ci95'][0]:+.3f},{v['ci95'][1]:+.3f}]" for k, v in o.items())); continue
            P(f"DIAG (post-freeze, reported) {nm}: " + "; ".join(f"{k}: without {v['without']['median']:+.3f} [{v['without']['ci95'][0]:+.3f},{v['without']['ci95'][1]:+.3f}], alone {v['alone']['median']:+.3f} [{v['alone']['ci95'][0]:+.3f},{v['alone']['ci95'][1]:+.3f}]" for k, v in o.items()))
    R["cells"] = cells
    for k, v in cells.items():
        if "post" not in v: P(f"CELL {k:15s}: {v['label']} (N {v['n']})"); continue
        p, r = v["post"], v["raw_stat_only"]
        P(f"CELL {k:15s} N {v['n']:3d}: raw (stat only) {r['median']:+.3f} [{r['ci95'][0]:+.3f},{r['ci95'][1]:+.3f}] -> joint {p['median']:+.3f} "
          f"68% [{p['ci68'][0]:+.3f},{p['ci68'][1]:+.3f}] 95% [{p['ci95'][0]:+.3f},{p['ci95'][1]:+.3f}] sd {p['sd']:.3f} z {p['z']:+.2f} P(s<=0) {p['P_le0']:.4f} -> {v['label']}"
          + (f"  | x2 widths {v['widths_x2_reported']['median']:+.3f} [{v['widths_x2_reported']['ci95'][0]:+.3f},{v['widths_x2_reported']['ci95'][1]:+.3f}]" if "widths_x2_reported" in v else "")
          + (f"  | half widths (post-freeze) {v['widths_half_post_freeze']['median']:+.3f} [{v['widths_half_post_freeze']['ci95'][0]:+.3f},{v['widths_half_post_freeze']['ci95'][1]:+.3f}]" if "widths_half_post_freeze" in v else "")
          + (f"  | GB1 line P {p['P_within_GB1_line']:.3f}" if "P_within_GB1_line" in p else ""))
        if "all_systems_reported" in v: P(f"      all systems (no admissibility, reported): {v['all_systems_reported']['median']:+.3f} [{v['all_systems_reported']['ci95'][0]:+.3f},{v['all_systems_reported']['ci95'][1]:+.3f}]")

# ------------------------------------------------------------------ class labels, CMB row, lane label (main) / MUTATE bite
if not MUTATE:
    CL_LAB = {}
    for c in HOT + CONTROL + ("MW ultra-faint", "M31 others"):
        ls = [RES["footings"][f]["cells"][c]["label"] for f in A0]
        CL_LAB[c] = ls[0] if ls[0] == ls[1] else f"SPLIT ({ls[0]} / {ls[1]})"
    RES["class_labels"] = CL_LAB
    P("\nCLASS LABELS (both footings):")
    for c, L in CL_LAB.items(): P(f"   {c:15s} {L}{'  [control]' if c in CONTROL else ('  [reported only, as GB1]' if c not in HOT else '')}")
    # CMB row from the record
    J = lambda *p: json.load(open(os.path.join(CL, *p)))
    kd = J("KD1_unpinned_kq_dust", "kd1.json"); hc = J("HC1_hot_fermion_all_gates", "hc1.json"); hg = J("HC1_hot_fermion_all_gates", "hc1_g9.json")
    ld = J("LD1_late_decaying_cold", "ld1.json"); en = J("EN1_shock_entropy_field", "en1.json"); q3 = J("QX12_triangle", "iter_3_isothermal_sea", "qx12_i3.json")
    q2 = J("QX12_triangle", "iter_2_hot_threshold", "qx12_i2.json")
    keys = []
    keys.append(dict(key="KD1 K(Q) dust, amplitude unpinned (6c7f83ed02)", G9={f: kd["table"][f]["G9a"] for f in A0}, hot={f: f"G2 {kd['table'][f]['G2']}, G3 {kd['table'][f]['G3']}" for f in A0},
                     hot_pass={f: kd["table"][f]["G2"] == "PASS" and kd["table"][f]["G3"] == "PASS" for f in A0}))
    keys.append(dict(key="HC1 thermal fermion 11.14 eV (c207d70254)", G9={f: hg["G9"] for f in A0},
                     hot={f: f"G2 {hc['footings'][f]['HC1']['G2 X-COP']['status']}, G3 {hc['footings'][f]['HC1']['G3 groups']['status']}" for f in A0},
                     hot_pass={f: hc['footings'][f]['HC1']['G2 X-COP']['status'] == "PASS" and hc['footings'][f]['HC1']['G3 groups']['status'] == "PASS" for f in A0}))
    keys.append(dict(key="LD1 late-decaying cold (d7db4e3403)", G9={f: "PASS" if ld["footings"][f]["D1_PASS"] else "FAIL" for f in A0},
                     hot={f: f"cluster f today {ld['footings'][f]['D3_disc_and_cluster_f_today']:.3f} vs X-COP need ~4" for f in A0}, hot_pass={f: False for f in A0}))
    for v in ("V-frac-L", "V-frac-S", "V-dens-L"):
        keys.append(dict(key=f"EN1 shock-entropy field {v} (eae8892550)", G9={f: "FAIL (carried: sigma = 0 before shocks)" for f in A0},
                         hot={f: f"G2 {en[v]['statuses'][f]['G2 X-COP']}, G3 {en[v]['statuses'][f]['G3 groups']}" for f in A0},
                         hot_pass={f: en[v]['statuses'][f]['G2 X-COP'] == "PASS" and en[v]['statuses'][f]['G3 groups'] == "PASS" for f in A0}))
    keys.append(dict(key="QX12 iter_2 host-temperature step (7a1afa9b6b)", G9={f: "NOT GRADED (hot early; needs the QX7 clock switch, itself KILLED)" for f in A0},
                     hot={f: f"label {q2['foot'][f]['label']}" for f in A0}, hot_pass={f: False for f in A0}))
    keys.append(dict(key="QX12 iter_3 isothermal sea (b605c9fd7c)", G9={f: "NOT GRADED" for f in A0},
                     hot={f: f"X-COP pass at {sum(1 for s in q3['scan'][f] if s['X_pass'])} of {len(q3['scan'][f])} c_s0" for f in A0},
                     hot_pass={f: any(s['X_pass'] for s in q3['scan'][f]) for f in A0}))
    keys.append(dict(key="QX3 iter1-iter3 inside the action (0240c8e31d, 602db4263d)", G9={f: "FAIL (iter1, iter3); iter2 PASS shape only with mu_K >= 4e4, galaxies need <= 79" for f in A0},
                     hot={f: "QX2 / QX5: clusters FAIL for every static term" for f in A0}, hot_pass={f: False for f in A0}))
    keys.append(dict(key="QX15 primary CMB, footing + cold component (1013e0362e)", G9={f: "PASS (primary TT/TE/EE, cold component)" for f in A0},
                     hot={f: "the cold component is KD1/QX7's: retained by hosts, QX7 KILLED (KiDS over-predicted); KD1 G2/G3 FAIL" for f in A0}, hot_pass={f: False for f in A0}))
    se1 = [d for d in os.listdir(CL) if d.startswith("SE1")]; se1_res = [d for d in se1 if os.path.exists(os.path.join(CL, d, "RESULT.md"))]
    common = [k["key"] for k in keys if all(str(k["G9"][f]).startswith("PASS") and k["hot_pass"][f] for f in A0)]
    any_hot = [k["key"] for k in keys if any(k["hot_pass"][f] for f in A0)]
    cmb = dict(keys=keys, SE1_on_disk=se1_res, label="COMMON" if common else "SEPARATE", common_keys=common, any_key_passes_hot=any_hot,
               disclosure=("no key in the record passes the hot classes at all, so SEPARATE is the frozen rule's reading, not a proof that two causes exist" if not any_hot else ""))
    RES["CMB_row"] = cmb
    P("\nCMB ROW (record, no re-solve):")
    for k in keys: P(f"   {k['key']:58s} G9 {k['G9']['canonical']}; hot {k['hot']['canonical']} | alt hot {k['hot']['alt']}")
    P(f"   SE1 result on disk: {', '.join(se1_res) or 'none (SE1 not landed when this ran)'}")
    P(f"   -> CMB row: {cmb['label']}" + (f" ({cmb['disclosure']})" if cmb["disclosure"] else ""))
    nonclu = ("ellipticals", "KiDS", "bright M31", "MW classical", "Coma UDGs")
    def L_(c, f): return RES["footings"][f]["cells"][c]["label"]
    clu_ne = all(L_(c, f) == "NOT EXPLAINED" for c in ("X-COP", "groups") for f in A0)
    nonclu_ok = all(L_(c, f) == "EXPLAINED" or L_(c, f).startswith("NOT A TEST") for c in nonclu for f in A0)
    any_ex = any(L_(c, f) == "EXPLAINED" for c in HOT for f in A0)
    remaining = sorted({c for c in HOT for f in A0 if L_(c, f) == "NOT EXPLAINED"}, key=HOT.index)
    if clu_ne and nonclu_ok: LL = "STEP = SYSTEMATICS EXCEPT CLUSTERS AND GROUPS"
    elif any_ex and any(L_(c, f) == "NOT EXPLAINED" for c in nonclu for f in A0): LL = f"STEP = SYSTEMATICS IN PART (remaining: {', '.join(remaining)})"
    elif not any_ex: LL = "STEP STANDS"
    else: LL = f"UNCLASSIFIED by the frozen rule (remaining: {', '.join(remaining)})"
    RES["label"] = LL; RES["remaining"] = remaining
    P(f"\nLANE LABEL: {LL}")
    kaok = all(v["ok"] for v in RES["KA"].values())
    RES["KA_all"] = bool(kaok); P(f"KNOWN ANSWERS (KA1 ST1 to 0, KA2, KA3) + M2: {'ALL PASS' if kaok else 'SOME FAIL'}")
else:
    MJ = json.load(open(os.path.join(HERE, "se2.json")))
    bite = {}
    for f in A0:
        up = {c: RES["footings"][f]["cells"][c]["post"]["median"] - MJ["footings"][f]["cells"][c]["post"]["median"] for c in ("ellipticals", "KiDS", "X-COP", "groups")}
        kmain = MJ["footings"][f]["cells"]["KiDS"]["label"]; kmut = RES["footings"][f]["cells"]["KiDS"]["label"]
        ok = all(v > 0 for v in up.values()) and (kmut == "NOT EXPLAINED" or kmain == "NOT EXPLAINED")
        bite[f] = dict(median_rise=up, KiDS_main=kmain, KiDS_mutate=kmut, ellipticals_main=MJ["footings"][f]["cells"]["ellipticals"]["label"],
                       ellipticals_mutate=RES["footings"][f]["cells"]["ellipticals"]["label"], bites=bool(ok))
        P(f"M1 [{f}] median rise " + ", ".join(f"{k} {v:+.3f}" for k, v in up.items()) + f"; KiDS {kmain} -> {kmut}; ellipticals {bite[f]['ellipticals_main']} -> {bite[f]['ellipticals_mutate']} -> {'BITES' if ok else 'NO BITE'}")
    RES["MUTATE"] = dict(M1=bite, bites=all(v["bites"] for v in bite.values()))
    P(f"MUTATE M1 inverted IMF bracket: {'BITES on both footings' if RES['MUTATE']['bites'] else 'NO POWER'}")
P("kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if (RES.get("KA_all", True) and RES.get("MUTATE", {}).get("bites", True)) else 1)
