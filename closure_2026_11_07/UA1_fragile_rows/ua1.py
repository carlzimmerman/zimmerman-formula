#!/usr/bin/env python3
"""UA1 (criteria 9b5b06f1d5): SE2's two fragile rows -- groups under the full systematic budget (single widths),
Coma UDGs under a symmetric pericentre admissibility cut.
    python3 ua1.py           -> ua1.json / ua1.out           (main + KA0, KA-G, KA-U, KA-beta)
    python3 ua1.py --mutate  -> ua1_MUTATE.json / .out       (MG inverted non-thermal sign; MA inverted admissibility)
se2.py is exec'd read-only (its writes go to a temp dir outside the repo). kappa = 1/2 FITTED; footings never pooled;
not theory closed."""
import os, sys, json, math, csv, re, io, ast, tempfile, contextlib, builtins, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); C7 = os.path.dirname(HERE); REPO = os.path.dirname(C7)
CL = os.path.join(REPO, "closure_2026_11_06"); RB = os.path.join(REPO, "rebuild_2026_10_22")
SE2D = os.path.join(CL, "SE2_step_as_systematics")
MUT = "--mutate" in sys.argv; TAG = "ua1_MUTATE" if MUT else "ua1"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(s)
RES = dict(tag=TAG, criteria="9b5b06f1d5", parent="SE2 f49a99a04c", note="kappa = 1/2 FITTED; not theory closed; adopts nothing", footings={}, KA={})
P(f"UA1 fragile rows {'MUTATE' if MUT else 'MAIN'}. kappa = 1/2 FITTED; not theory closed; footings never pooled.")

# ------------------------------------------------------------------ KA0: exec se2.py read-only, writes redirected; compare to committed se2.json
def exec_se2():
    tmp = tempfile.mkdtemp(prefix="ua1_se2_replay_"); cap = {}
    def ropen(path, mode="r", *a, **kw):
        if any(c in mode for c in "wa+"):
            p2 = os.path.join(tmp, os.path.basename(path)); cap[os.path.basename(path)] = p2
            return builtins.open(p2, mode, *a, **kw)
        return builtins.open(path, mode, *a, **kw)
    sp = os.path.join(SE2D, "se2.py"); src = builtins.open(sp).read()
    ns = {"__file__": sp, "__name__": "se2_replay", "open": ropen}
    _a = sys.argv; sys.argv = [sp]; buf = io.StringIO(); code = None
    try:
        with contextlib.redirect_stdout(buf): exec(compile(src, "se2_replay", "exec"), ns)
    except SystemExit as e: code = e.code
    finally: sys.argv = _a
    return ns, json.load(builtins.open(cap["se2.json"])), code
NSE, NEW, SE2EXIT = exec_se2()
SE2J = json.load(open(os.path.join(SE2D, "se2.json")))
def cmp_tree(a, b):
    nd, no, diffs = [0], [0], []
    def c(a, b, p):
        if isinstance(a, dict) and isinstance(b, dict):
            if set(a) != set(b): diffs.append((p, "keys")); return
            for k in a: c(a[k], b[k], p + "/" + str(k))
        elif isinstance(a, list) and isinstance(b, list):
            if len(a) != len(b): diffs.append((p, "len")); return
            for i, (x, y) in enumerate(zip(a, b)): c(x, y, p + f"[{i}]")
        elif isinstance(a, bool) or isinstance(b, bool) or isinstance(a, str) or a is None:
            no[0] += 1
            if a != b: diffs.append((p, a, b))
        else:
            nd[0] += 1
            if not (a == b or (isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b))): diffs.append((p, a, b))
    c(a, b, ""); return nd[0], no[0], diffs
n0, s0, d0 = cmp_tree(NEW, SE2J)
# Amendment 1 (2026-11-07, post-freeze, disclosed): the leaf CMB_row/SE1_on_disk is SE2's directory listing of SE1 results;
# SE1 landed after SE2 ran, so that listing changed. It is record state, not a computed value. Every other leaf must match exactly.
d0x = [d for d in d0 if d[0] != "/CMB_row/SE1_on_disk"]
RES["KA"]["KA0_SE2_to_0"] = dict(n_numeric=n0, n_other=s0, n_diff=len(d0), n_diff_excl_SE1_listing=len(d0x), diffs=[str(x) for x in d0[:10]],
                                 SE1_listing_now=NEW["CMB_row"]["SE1_on_disk"], SE1_listing_committed=SE2J["CMB_row"]["SE1_on_disk"], se2_exit=SE2EXIT, ok=len(d0x) == 0)
P(f"KA0 SE2 replay (se2.py exec'd read-only, writes redirected; ST1 replay inside): {n0} numbers + {s0} labels vs committed se2.json: "
  f"{len(d0)} differ ({', '.join(d[0] for d in d0) or 'none'}); excluding the SE1 directory listing (Amendment 1): {len(d0x)} differ -> "
  f"{'PASS (difference 0)' if not d0x else 'FAIL'}; se2 exit {SE2EXIT}")

g = NSE  # SE2 namespace (functions, loaders, seeds, priors)
A0 = g["A0"]; NS = g["NS"]; KPC = g["KPC"]; G = g["G"]; MS = g["MS"]; NDRAW = g["NDRAW"]; LN10 = g["LN10"]
gl, dlaw, fimf, draw_lam, uni, rngs, summ, lab = g["gl"], g["dlaw"], g["fimf"], g["draw_lam"], g["uni"], g["rngs"], g["summ"], g["lab"]
SEEDS = g["SEEDS"]; GRAW = g["GRAW"]; GR = g["GR"]; K_TO_S = g["K_TO_S"]; SPEC = g["SPEC"]
VC = g["VC"]; TAU = g["TAU_LINE"]; DCLS = g["DCLS"]; GRADED = g["GRADED"]

# ------------------------------------------------------------------ groups: new knobs
def nrng(cls, f): return np.random.default_rng(9100 + SEEDS[cls] * 10 + (0 if f == "canonical" else 1))
DF_HI = 0.70 / 0.674
def norm_g(n): return re.sub(r"[\s\-\._]", "", n.upper())
_g125 = open(os.path.join(REPO, "deepseek_push", "G125_group_equipartition.py")).read()
E11 = ast.literal_eval(re.search(r"^E11 = (\[.*?^\])", _g125, re.S | re.M).group(1))
E11M = {norm_g(r[0]): r[3] * 1e13 for r in E11}
MATCH = [(gp["name"], gp["M5"], E11M[norm_g(gp["name"])]) for gp in GR if norm_g(gp["name"]) in E11M]
lr = [math.log10(a / b) for _, a, b in MATCH]
if len(lr) >= 3:
    MU_G = float(np.mean(lr)); RMS_G = float(np.sqrt(np.mean(np.square(lr)))); M_G = math.sqrt(MU_G ** 2 + (RMS_G / math.sqrt(len(lr))) ** 2)
else:
    MU_G = RMS_G = float("nan"); M_G = 0.0
RES["groups_dataset_term"] = dict(matched=[m[0] for m in MATCH], log_ratio=lr, mu=MU_G, rms=RMS_G, m_G=M_G, source="Eckmiller+2011 Table 15 via deepseek_push/G125 (UNVERIFIED-in-repo, PROVISIONAL)")
P(f"groups dataset term: {len(MATCH)} matched with Eckmiller+2011 ({', '.join(m[0] for m in MATCH)}); log10(M500 L15/E11) mu {MU_G:+.4f} rms {RMS_G:.4f} -> m_G {M_G:.4f} dex")

def gspec(kind="main"):
    s = dict(bnt=(0.0, 0.20), df=(1.0, DF_HI), cg=(1.0, 1.1), mg=M_G)
    if kind == "zero": s = dict(bnt=(0.0, 0.0), df=(1.0, 1.0), cg=(1.0, 1.0), mg=0.0)
    if kind == "invert": s["bnt"] = (-0.20, 0.0)
    if kind == "sym": s["bnt"] = (-0.20, 0.20)
    if kind == "x2": s = dict(bnt=(0.0, 0.40), df=(1.0, 1 + 2 * (DF_HI - 1)), cg=(1.0, 1.2), mg=2 * M_G)
    return s
def groups_res2(a0, fst, lam, sg, bnt, dfac, cg, dsh):
    rm = (np.array([r for _, r, _, _ in GRAW]) * KPC)[None] * dfac[:, None]
    Mg = np.array([m for _, _, m, _ in GRAW])[None] * (dfac[:, None] ** 2.5 * cg[:, None])
    Mo = np.array([m for _, _, _, m in GRAW])[None] * (dfac[:, None] / (1.0 - bnt[:, None]) * 10.0 ** dsh[:, None])
    fst = np.asarray(fst)[:, None]; Mb = Mg * (1 + fst); gN = G * Mb * MS / rm ** 2
    Ml = gl(gN, a0) * rm ** 2 / G / MS; D = np.log10(Mo / Ml); sh = fst / (1 + fst)
    b = 1 + sh * (fimf(np.asarray(sg), K_TO_S)[:, None] ** np.asarray(lam)[:, None] - 1)
    return D - dlaw(b, gN, a0)
def post_groups2(a0, f, spec, gs_):
    rs, rn = rngs("groups", f); gnames = [x for x, _, _, _ in GRAW]; gs = sorted(set(gnames), key=gnames.index)
    lam = draw_lam(rn, spec, NDRAW); sg = uni(rn, spec["sig_grp"], NDRAW); fst = uni(rn, spec["fst"], NDRAW)
    rx = nrng("groups", f)
    bnt = uni(rx, gs_["bnt"], NDRAW); dfac = uni(rx, gs_["df"], NDRAW); cg = uni(rx, gs_["cg"], NDRAW)
    dsh = rx.normal(0, 1, NDRAW) * gs_["mg"]
    res = groups_res2(a0, fst, lam, sg, bnt, dfac, cg, dsh); pidx = [np.where(np.array(gnames) == x)[0] for x in gs]
    ix = rs.integers(0, len(gs), (NDRAW, len(gs))); sel = np.stack(pidx)[ix].reshape(NDRAW, -1)
    return np.median(res[np.arange(NDRAW)[:, None], sel], axis=1)

# ------------------------------------------------------------------ pericentre admissibility (A3)
Z2 = {(r["footing"], r["name"]): r for r in csv.DictReader(open(os.path.join(RB, "Z2_satellite_systematics", "z2_per_system.csv")))}
KEV, MP = 1.602176634e-16, 1.67262e-27; BETA = dict(kT=8.6, rc=276.0, beta=0.71, mu=0.6)
CB = 3 * BETA["beta"] * BETA["kT"] * KEV / (BETA["mu"] * MP); KPC_C = 3.0857e19
def g_beta(d_kpc):   # S1's Coma beta-model field (s1_v3_hosted_small.py), copied verbatim; KA-beta checks it
    r = d_kpc * KPC_C; rc = BETA["rc"] * KPC_C
    return CB * r / (r * r + rc * rc)
GPC = 4.30091e-3
def dsph_A3(f, name, div=3.0):
    r = NS["X1R"].get((f, name))
    if r is None or r["host"] not in VC: return dict(A3=True, tau_p=None, rp_kpc=None, src="no host term")
    Re = float(r["rh_pc"]); sg = float(r["sigma"]); d = float(r["d_host_kpc"]); V = VC[r["host"]]
    z = Z2.get((f, name)); src = "d/%g" % div; rp = d / div
    if z is not None and z.get("pm") == "True" and z.get("r_peri_kpc") not in ("", None, "nan"):
        rp = float(z["r_peri_kpc"]); src = "Z2 PM"
    if rp > d: rp = d; src += " (capped at d)"
    rpp = rp * 1e3; MW_ = 4 * sg ** 2 * Re / GPC; Mh = V ** 2 * rpp / GPC
    tau = Re / (rpp * (MW_ / (3 * Mh)) ** (1 / 3))
    return dict(A3=bool(tau < TAU), tau_p=tau, rp_kpc=rp, src=src)
def udg_A3(r, div=3.0):
    Re = float(r["Re_kpc"]) * KPC; sg = float(r["sigma"]) * 1e3; rpk = float(r["d_mean_kpc"]) / div; rp = rpk * KPC; gp = g_beta(rpk)
    tau = Re / (rp * (4 * sg ** 2 * Re / (3 * gp * rp * rp)) ** (1 / 3))
    return dict(A3=bool(tau < TAU), tau_p=tau, rp_kpc=rpk, src="d_mean/%g (no orbit on disk)" % div)

def with_adm(rows, kind, keyfn, invert=False):
    """rows copied; kind 'dsph' uses r['adm'], 'udg' uses r['_adm']; admissible = A1 & A2 & A3 (or its complement)."""
    out = []
    for r in rows:
        a = r["adm"] if kind == "dsph" else r["_adm"]; a3 = keyfn(r)["A3"]
        ok = bool(a["A1"] and a["A2"] and a3)
        if invert: ok = not ok
        r2 = dict(r); na = dict(a); na["A1"] = ok; na["A2"] = True
        if kind == "dsph": r2["adm"] = na
        else: r2["_adm"] = na
        out.append(r2)
    return out

# ------------------------------------------------------------------ per footing
MJ = json.load(open(os.path.join(HERE, "ua1.json"))) if MUT else None
SPM = SPEC("main")
for f, a0 in A0.items():
    S, E, X = g["build"](f, a0); GRp = {0: g["groups_pts"](a0, 0.0), 1: g["groups_pts"](a0, 1.0)}
    st = g["R1"][f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / LN10
    B = dict(f=f, S=S, E=E, X=X, GR=GRp, U=g["udgs"](f, a0), D=g["dsphs"](f, a0), K=g["kids"](a0), sigU=sigU)
    B["rms_L0"] = float(np.sqrt(np.mean([p["D"] ** 2 for p in S])))
    anchor = g["g_sparc"](g["L0"](f, a0), B, a0)[1]["Z"]
    dsI, W = g["dsph_inputs"](B, f); uR, sk, ubase = g["udg_inputs"](f, a0)
    se2c = SE2J["footings"][f]["cells"]; R = dict(anchor=anchor); RES["footings"][f] = R
    P(f"\n================ [{f}] a0 {a0:.4e}  SPARC anchor Z {anchor:+.4f}")
    cells = {}

    # ---------------- groups
    xg0 = g["post_groups"](B, a0, f, SPM)[0]
    if not MUT:
        xz = post_groups2(a0, f, SPM, gspec("zero")); eqz = bool(np.array_equal(xz, xg0)); sz = summ(xz)
        eqj = (sz == se2c["groups"]["post"])
        RES["KA"][f"KA-G_{f}"] = dict(array_equal_SE2=eqz, summary_equals_se2_json=eqj, ok=bool(eqz and eqj))
        P(f"KA-G budget zeroed vs SE2 groups: posterior array_equal {eqz}; summary == se2.json {eqj} -> {'PASS' if eqz and eqj else 'FAIL'}")
    xg = post_groups2(a0, f, SPM, gspec("main"))
    raw0 = summ(g["post_groups"](B, a0, f, SPM, nominal=True, fst_fixed=0.0)[0]); raw1 = summ(g["post_groups"](B, a0, f, SPM, nominal=True, fst_fixed=1.0)[0])
    rawg = dict(raw0, contains0=bool(raw0["contains0"] and raw1["contains0"]))
    pg = summ(xg); cells["groups"] = dict(post=pg, raw_stat_only=raw0, raw_stat_only_fst1=raw1, n=20, label=lab(pg, rawg, 20, False), SE2_post=se2c["groups"]["post"])
    if not MUT:
        cells["groups"]["widths_x2_reported"] = summ(post_groups2(a0, f, SPEC("x2"), gspec("x2")))
        cells["groups"]["symmetric_bnt_reported"] = summ(post_groups2(a0, f, SPM, gspec("sym")))
        for k in ("bnt", "df", "cg", "mg"):   # one new knob alone on top of SE2's budget (reported)
            sp_ = gspec("zero"); sp_[k] = gspec("main")[k]; cells["groups"][f"SE2_plus_{k}_only_reported"] = summ(post_groups2(a0, f, SPM, sp_))
    else:
        xi = post_groups2(a0, f, SPM, gspec("invert")); pi = summ(xi); mmain = MJ["footings"][f]["cells"]["groups"]["post"]["median"]
        cells["groups_MG_inverted_bnt"] = dict(post=pi, n=20, label=lab(pi, rawg, 20, False), drop=mmain - pi["median"], bites=bool(mmain - pi["median"] >= 0.03))

    # ---------------- admissibility with A3
    adm = {}
    for c in DCLS:
        rows = dsI[c]; a3 = {r["name"]: dsph_A3(f, r["name"]) for r in rows}; a35 = {r["name"]: dsph_A3(f, r["name"], 5.0) for r in rows}
        keep = [r["name"] for r in rows if r["adm"]["A1"] and r["adm"]["A2"] and a3[r["name"]]["A3"]]
        adm[c] = dict(N=len(rows), N_SE2=sum(1 for r in rows if r["adm"]["A1"] and r["adm"]["A2"]), N_adm=len(keep),
                      removed_A3=[r["name"] for r in rows if r["adm"]["A1"] and r["adm"]["A2"] and not a3[r["name"]]["A3"]],
                      n_PM_pericentre=sum(1 for v in a3.values() if v["src"].startswith("Z2")),
                      N_adm_ceiling_d5_reported=sum(1 for r in rows if r["adm"]["A1"] and r["adm"]["A2"] and a35[r["name"]]["A3"]),
                      tau_p={k: v["tau_p"] for k, v in a3.items()})
    u3 = {r["name"]: udg_A3(r) for r in uR}; u35 = {r["name"]: udg_A3(r, 5.0) for r in uR}
    adm["Coma UDGs"] = dict(N=len(uR), N_SE2=sum(1 for r in uR if r["_adm"]["A1"] and r["_adm"]["A2"]),
                            N_adm=sum(1 for r in uR if r["_adm"]["A1"] and r["_adm"]["A2"] and u3[r["name"]]["A3"]),
                            removed_A3=[r["name"] for r in uR if r["_adm"]["A1"] and r["_adm"]["A2"] and not u3[r["name"]]["A3"]],
                            kept=[r["name"] for r in uR if r["_adm"]["A1"] and r["_adm"]["A2"] and u3[r["name"]]["A3"]],
                            N_adm_ceiling_d5_reported=sum(1 for r in uR if r["_adm"]["A1"] and r["_adm"]["A2"] and u35[r["name"]]["A3"]),
                            tau_now={r["name"]: r["_adm"]["tau"] for r in uR}, tau_p={k: v["tau_p"] for k, v in u3.items()})
    R["admissibility"] = adm
    for c, a in adm.items():
        P(f"ADMISSIBILITY {c:15s}: SE2 {a['N_SE2']}/{a['N']} -> with A3 {a['N_adm']}/{a['N']}; removed by A3: {', '.join(a['removed_A3']) or 'none'}"
          + (f"; PM pericentres used {a['n_PM_pericentre']}" if "n_PM_pericentre" in a else "") + f"; ceiling d/5 (reported) {a['N_adm_ceiling_d5_reported']}")
    if not MUT:
        # Amendment 2 (2026-11-07, post-freeze, disclosed): S1 divided by its own rounded a0 (9.3603e-11 / 1.1312e-10); the SE2/GB1
        # namespace carries the full-precision record a0 (QX5). KA-beta is evaluated with S1's a0; the A3 cut uses g_beta, no a0.
        A0S1 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
        kb = max(abs(g_beta(float(r["d_mean_kpc"])) / A0S1[f] - float(r["x_e_dmean"])) for r in uR)
        kbr = max(abs(g_beta(float(r["d_mean_kpc"])) / a0 - float(r["x_e_dmean"])) for r in uR)
        RES["KA"][f"KA-beta_{f}"] = dict(maxdiff=kb, maxdiff_with_record_a0=kbr, record_a0=a0, ok=kb <= 1e-12)
        P(f"KA-beta g_beta(d_mean)/a0_S1 vs S1 x_e_dmean: max|d| {kb:.1e} -> {'PASS' if kb <= 1e-12 else 'FAIL'} (with the record's full-precision a0 {a0:.10e}: {kbr:.1e}; Amendment 2)")
        # post-freeze sensitivity (reported only, decides nothing): Coma survivors vs the assumed pericentre fraction, and each UDG's break-even
        sens = {}
        for dv in (1.5, 2.0, 2.5, 3.0, 4.0, 5.0):
            sens[str(dv)] = sum(1 for r in uR if r["_adm"]["A1"] and r["_adm"]["A2"] and udg_A3(r, dv)["A3"])
        be = {}
        for r in uR:
            lo, hi = 1.0, 50.0
            if udg_A3(r, hi)["A3"]: be[r["name"]] = None; continue
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if udg_A3(r, mid)["A3"]: lo = mid
                else: hi = mid
            be[r["name"]] = lo
        R["coma_peri_sensitivity_post_freeze"] = dict(N_adm_vs_d_over_rp=sens, breakeven_d_over_rp=be)
        P("   (post-freeze, reported) Coma admissible N vs d_mean/r_p: " + ", ".join(f"{k} -> {v}" for k, v in sens.items())
          + "; break-even d/r_p per UDG: " + ", ".join(f"{k[:11]} {v:.2f}" for k, v in sorted(be.items(), key=lambda kv: kv[1])))
        P("   Coma tau now -> tau at d_mean/3: " + ", ".join(f"{r['name'][:11]} {r['_adm']['tau']:.3f}->{u3[r['name']]['tau_p']:.3f}" for r in uR))

    # ---------------- KA-U: A3 off reproduces SE2 cells
    if not MUT:
        oku = []
        for c in DCLS:
            xm, im = g["post_dsph"](c, dsI[c], W, a0, anchor, f, SPM)
            if xm is not None and "post" in se2c[c]: oku.append(summ(xm) == se2c[c]["post"])
        xm, _ = g["post_udg"](uR, sk, f, SPM); oku.append(summ(xm) == se2c["Coma UDGs"]["post"])
        RES["KA"][f"KA-U_{f}"] = dict(n=len(oku), ok=all(oku)); P(f"KA-U A3 off reproduces SE2 dSph/UDG cells: {sum(oku)}/{len(oku)} -> {'PASS' if all(oku) else 'FAIL'}")

    def grade(c, invert=False):
        if c == "Coma UDGs":
            rows = with_adm(uR, "udg", lambda r: u3[r["name"]], invert)
            xm, im = g["post_udg"](rows, sk, f, SPM); xr, _ = g["post_udg"](rows, sk, f, SPM, nominal=True)
            n = im["n"]
            if xm is None or n < 5: return dict(label="NOT A TEST (admissible N < 5)", n=n)
            pm, pr = summ(xm), summ(xr); o = dict(post=pm, raw_stat_only=pr, n=n, label=lab(pm, pr, n, True))
            if not MUT and not invert:
                o["widths_x2_reported"] = summ(g["post_udg"](rows, sk, f, SPEC("x2"))[0])
            return o
        rows = with_adm(dsI[c], "dsph", lambda r: dsph_A3(f, r["name"]), invert)
        xm, im = g["post_dsph"](c, rows, W, a0, anchor, f, SPM); n = im["n"]
        if xm is None or n < 5: return dict(label="NOT A TEST (admissible N < 5)", n=n)
        xr, _ = g["post_dsph"](c, rows, W, a0, anchor, f, SPM, nominal=True); pm, pr = summ(xm), summ(xr)
        return dict(post=pm, raw_stat_only=pr, n=n, label=lab(pm, pr, n, True))
    for c in ("Coma UDGs",) + DCLS:
        cells[c] = grade(c)
        if MUT: cells[c + " [MA inverted]"] = grade(c, invert=True)
    if MUT:
        mc = MJ["footings"][f]["cells"]["Coma UDGs"]; ic = cells["Coma UDGs [MA inverted]"]
        cells["MA_bite"] = dict(main_label=mc["label"], inverted_label=ic["label"], inverted_n=ic["n"], bites=bool(ic["n"] > 0 and ic["label"] != mc["label"]))
    R["cells"] = cells
    for k, v in cells.items():
        if k == "MA_bite":
            P(f"MA [{f}] Coma main {v['main_label']} -> inverted (N {v['inverted_n']}) {v['inverted_label']} -> {'BITES' if v['bites'] else 'NO BITE'}"); continue
        if "post" not in v: P(f"CELL {k:28s} N {v['n']:3d}: {v['label']}"); continue
        p, r = v["post"], v.get("raw_stat_only")
        s = (f"CELL {k:28s} N {v['n']:3d}: " + (f"raw {r['median']:+.3f} [{r['ci95'][0]:+.3f},{r['ci95'][1]:+.3f}] -> " if r else "")
             + f"joint {p['median']:+.3f} 68% [{p['ci68'][0]:+.3f},{p['ci68'][1]:+.3f}] 95% [{p['ci95'][0]:+.3f},{p['ci95'][1]:+.3f}] sd {p['sd']:.3f} P(s<=0) {p['P_le0']:.4f} -> {v['label']}")
        if "SE2_post" in v: s += f"  | SE2 {v['SE2_post']['median']:+.3f} [{v['SE2_post']['ci95'][0]:+.3f},{v['SE2_post']['ci95'][1]:+.3f}]"
        if "drop" in v: s += f"  | median drop vs main {v['drop']:+.3f} -> {'BITES' if v['bites'] else 'NO BITE'}"
        P(s)
        for kk in [x for x in v if x.endswith("_reported")]:
            q = v[kk]; P(f"      {kk:34s} {q['median']:+.3f} [{q['ci95'][0]:+.3f},{q['ci95'][1]:+.3f}]{'  contains 0' if q['contains0'] else ''}")

# ------------------------------------------------------------------ labels
FO = list(A0)
def CLL(c): ls = [RES["footings"][f]["cells"][c]["label"] for f in FO]; return ls[0] if ls[0] == ls[1] else f"SPLIT ({ls[0]} / {ls[1]})"
if not MUT:
    RES["class_labels"] = {c: CLL(c) for c in ("groups", "Coma UDGs") + DCLS}
    P("\nCLASS LABELS (both footings; graded: groups, Coma UDGs; symmetric cut also graded on bright M31 and MW classical):")
    for c, L in RES["class_labels"].items(): P(f"   {c:15s} {L}{'  [control]' if c == 'LG field' else ('  [reported only]' if c in ('MW ultra-faint', 'M31 others') else '')}")
    drop = lambda L: L == "EXPLAINED" or L.startswith("NOT A TEST")
    gd = all(drop(RES["footings"][f]["cells"]["groups"]["label"]) for f in FO); ud = all(drop(RES["footings"][f]["cells"]["Coma UDGs"]["label"]) for f in FO)
    RES["rows_dropped"] = dict(groups=gd, coma=ud)
    RES["reading"] = ("BOTH ROWS DROP: residue = X-COP + CMB lensing" if gd and ud else
                      f"rows that drop: {', '.join(k for k, v in (('groups', gd), ('Coma UDGs', ud)) if v) or 'none'}; rows that stand: {', '.join(k for k, v in (('groups', gd), ('Coma UDGs', ud)) if not v) or 'none'}")
    P(f"\nREADING: {RES['reading']}")
    RES["KA_all"] = all(v["ok"] for v in RES["KA"].values()); P(f"KNOWN ANSWERS (KA0, KA-G, KA-U, KA-beta): {'ALL PASS' if RES['KA_all'] else 'SOME FAIL'}")
else:
    mg = all(RES["footings"][f]["cells"]["groups_MG_inverted_bnt"]["bites"] for f in FO); ma = all(RES["footings"][f]["cells"]["MA_bite"]["bites"] for f in FO)
    RES["MUTATE"] = dict(MG_bites=mg, MA_bites=ma)
    P(f"\nMUTATE MG (inverted non-thermal sign): {'BITES on both footings' if mg else 'NO BITE'}; MA (inverted admissibility): {'BITES on both footings' if ma else 'NO BITE'}")
pk = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss; pk = pk / 1e9 if sys.platform == "darwin" else pk / 1e6
RES["peak_rss_GB"] = pk; P(f"peak RSS {pk:.3f} GB")
P("kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
