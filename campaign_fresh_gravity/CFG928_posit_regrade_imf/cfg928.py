"""CFG928 -- re-grade of CFG921's five excess-selector posits under exactly two declared changes:
  C1  the red-lens fact (Sersic n>2 lens cells, F1 and the LS side of F7) carries CFG926 R5's IMF alpha-sigma correction
      (shift 0.123 + D_red; robustness C1-S SLUGGS ceiling, C1-W CFG850-window equivalent; diagnostic C1-blue),
  C2  clusters are a separate class: every posit graded on the galaxy-scale facts (F5, F6 withheld) and on all facts.
Everything else is CFG921's (forms, inputs, brackets, calibration on the 83 LVD dwarfs, estimators, lenient-corner FAIL rule).
Criteria: FROZEN_CRITERIA.md (ba971914e, committed alone before this script and before any number of this lane).
POST-HOC-MOTIVATED and CONDITIONAL: designed after CFG921's failures and CFG926 R5 were seen; C1 holds only if disc galaxies
stay near Chabrier.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg928.py      (CFG928_KONLY=1 -> K only; CFG928_MUTATE=uncorr|sign -> outputs by mode)
Inputs: cfg921.py exec'd read-only up to its MAIN section (and through it CFG919/914/880/883/687); cfg921_results.json (K1);
cfg926_results.json (R5 numbers).  Nothing downloaded; one core.
kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy, not a particle; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import io, json, math, time, resource, contextlib, builtins, warnings
import numpy as np
from scipy.stats import norm

T0 = time.time()
_REAL_OPEN = builtins.open
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUT = os.environ.get("CFG928_MUTATE", ""); assert MUT in ("", "uncorr", "sign")
KONLY = os.environ.get("CFG928_KONLY", "") == "1"; assert not (KONLY and MUT)
SUF = "_K" if KONLY else (f"_MUTATE_{MUT}" if MUT else "")
for _e in ("CFG921_MUTATE", "CFG921_KONLY", "CFG919_MUTATE", "CFG914_MUTATE", "CFG880_MUTATE", "CFG829_MUTATE", "CFG850_MUTATE",
           "CFG883_MUTATE", "CFG828_MUTATE", "CFG849_MUTATE", "MUTATE"):
    os.environ.pop(_e, None)
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
def rss_mb(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024 if sys.platform == "darwin" else 1024)
def J(*p):
    with _REAL_OPEN(os.path.join(LANES, *p)) as fh: return json.load(fh)
RES = dict(lane="CFG928", criteria="ba971914e", mutate=MUT or None, konly=KONLY, checks={})
def check(name, ok, measured):
    RES["checks"][name] = dict(ok=bool(ok), measured=str(measured))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {measured}")
    return bool(ok)
def jdef(o):
    if hasattr(o, "item"): return o.item()
    if isinstance(o, np.ndarray): return o.tolist()
    return str(o)
def finish(code):
    RES["runtime_s"] = time.time() - T0; RES["peak_rss_mb"] = rss_mb()
    with _REAL_OPEN(os.path.join(HERE, f"cfg928_results{SUF}.json"), "w") as fh: json.dump(RES, fh, indent=1, default=jdef)
    with _REAL_OPEN(os.path.join(HERE, f"cfg928{SUF}.out"), "w") as fh: fh.write("\n".join(OUT) + "\n")
    sys.exit(code)

FOOTS = ("canonical", "alt"); LN10 = math.log(10.0); GAL_WITHHOLD = ("F5", "F6")
P("CFG928  re-grade of CFG921's five posits: C1 IMF-corrected red-lens fact (CFG926 R5), C2 clusters as a separate class"
  + (f"   [MUTATE {MUT}]" if MUT else ("   [K only]" if KONLY else "")))
P("  POST-HOC-MOTIVATED and CONDITIONAL (designed after CFG921 and CFG926 were seen; C1 needs discs near Chabrier)")
P("  kappa = 1/2 FITTED; footings never pooled; criteria ba971914e")

# =====================================================================================================================  K0: CFG921 exec'd read-only
def _ro_open(file, mode="r", *a, **k):
    if any(c in mode for c in "wax+"):
        raise PermissionError(f"CFG928 refuses to write {file!r} from re-executed committed code")
    return _REAL_OPEN(file, mode, *a, **k)
class _Exit(Exception): pass
def _exit(code=0): raise _Exit(code)
def sandbox_exec(path, src, name):
    ns = {"__file__": path, "__name__": name}; buf = io.StringIO(); err = None
    old_open, old_exit = builtins.open, sys.exit
    builtins.open = _ro_open; sys.exit = _exit
    try:
        with contextlib.redirect_stdout(buf), warnings.catch_warnings():
            warnings.simplefilter("ignore")
            exec(compile(src, path, "exec"), ns)
    except BaseException as e:                  # noqa: BLE001 -- reported as a K failure
        err = f"{type(e).__name__}: {e}"
    finally:
        builtins.open = old_open; sys.exit = old_exit
    return ns, buf.getvalue(), err

P("\n=== K-stage")
F921 = os.path.join(LANES, "CFG921_excess_selector_posits", "cfg921.py")
with _REAL_OPEN(F921) as _fh: s921 = _fh.read()
_cut = s921.index("\nSTRUCT = {f: {vk: obs_struct(f, vk) for vk in VARS} for f in FOOTS}")
N, _o921, e921 = sandbox_exec(F921, s921[:_cut], "cfg921_ro")
c921 = N.get("RES", {}).get("checks", {})
k0 = e921 is None and bool(N.get("K_ALL")) and len(c921) >= 7 and all(v["ok"] for v in c921.values())
KOK = [check("K0 cfg921.py exec'd read-only to its MAIN section: its own K1-K7 pass (CFG919's and CFG914's checks through it)", k0,
             f"{sum(v['ok'] for v in c921.values())}/{len(c921)} CFG921 checks pass" + (f"; error {e921}" if e921 else ""))]
if not k0:
    P("  K0 failed: lane stops (criteria section 7)."); RES["class"] = None; finish(2)
build, FLOOR0, FLOOR_V6, GRID = N["build"], N["FLOOR0"], N["FLOOR_V6"], N["GRID"]
lens_set, cells_lens, blockdiag = N["lens_set"], N["N919"]["cells_lens"], N["N919"]["blockdiag"]
grade, obs_facts, gls_ops, dw_pred, lens_central = N["grade"], N["obs_facts"], N["gls_ops"], N["dw_pred"], N["lens_central"]
DWD, CLD, sp_lg, sp_code, SMALL, LARGE = N["DWD"], N["CLD"], N["sp_lg"], N["sp_code"], N["SMALL"], N["LARGE"]
POSITS, FACTS, SG, SHIFT_N2, A0, nu_e, PNAME = N["POSITS"], N["FACTS"], N["SG"], N["SHIFT_N2"], N["A0"], N["nu_e"], N["PNAME"]
LENS_NOM, DELTA, N880 = N["LENS_NOM"], N["DELTA"], N["N880"]
ZTF921 = float(N["ZTF"])
R921 = J("CFG921_excess_selector_posits", "cfg921_results.json")
R926 = J("CFG926_small_reframings_B", "cfg926_results.json")["R5"]

# =====================================================================================================================  this lane's pipeline
BASE = {f: build(f, {}) for f in FOOTS}
def build_shift(f, sh_ls, sh_ld=0.0):
    """CFG919 cells + block covariance with the n>2 (LS) lens block rebuilt at M* shift sh_ls (and LD at sh_ld if non-zero),
    through CFG919's own lens_set + cells_lens; every other block is CFG919's build(f, {}) unchanged"""
    cells, C, _ = BASE[f]; cls = [c["cls"] for c in cells]; out, mats = [], []
    for c in dict.fromkeys(cls):
        ix = [j for j, x in enumerate(cls) if x == c]; assert ix == list(range(ix[0], ix[-1] + 1))
        if c == "LS":
            cc, CC = cells_lens("LS", *lens_set("sph", f, sh_ls), 0.80)
        elif c == "LD" and sh_ld != 0.0:
            cc, CC = cells_lens("LD", *lens_set("disc", f, sh_ld), 0.20)
        else:
            cc, CC = [cells[j] for j in ix], C[np.ix_(ix, ix)]
        out += cc; mats.append(CC)
    return out, blockdiag(mats)

def obs_struct2(f, cells, C, floor, sh_ls, sh_ld=0.0):
    """copy of CFG921's obs_struct with (cells, C, floor, LS shift, LD shift) passed explicitly (K2 proves identity)"""
    Ct = C + floor ** 2 * np.eye(len(cells)); E = np.array([c["E"] for c in cells]); cls = np.array([c["cls"] for c in cells])
    wv = np.array([c["w"] for c in cells]); lgv = np.array([c["lg"] for c in cells]); ops = gls_ops(cells, Ct); S = dict(cells=cells, Ct=Ct, E=E, cls=cls, w=wv, lg=lgv, ops=ops)
    for c in ("DW", "CL"):
        ix = ops[c]["ix"]; x = lgv[ix] - lgv[ix].mean(); X = np.vstack([np.ones(len(ix)), x]).T; Ci = np.linalg.inv(Ct[np.ix_(ix, ix)])
        Cov = np.linalg.inv(X.T @ Ci @ X); S[f"slope_{c}"] = dict(ix=ix, B=(Cov @ X.T @ Ci)[1], se=math.sqrt(Cov[1, 1]))
    iD, iL = ops["DW"]["ix"], ops["LS"]["ix"]; shared = sorted(set(wv[iD]) & set(wv[iL]))
    jD = np.array([iD[list(wv[iD]).index(x)] for x in shared]); jL = np.array([iL[list(wv[iL]).index(x)] for x in shared])
    Cd = np.diag(np.diag(Ct)[jD]) + Ct[np.ix_(jL, jL)]; Ci = np.linalg.inv(Cd); one = np.ones(len(shared)); a = float(one @ Ci @ one)
    S["F7"] = dict(jD=jD, jL=jL, w=(Ci @ one) / a, se=a ** -0.5, windows=shared)
    S["DWCi"] = np.linalg.inv(Ct[np.ix_(iD, iD)])
    S["lens"] = {}
    for cl, key in (("LD", "disc"), ("LS", "sph")):
        shift = sh_ls if cl == "LS" else sh_ld; gbs, go, C_, gl = lens_set(key, f, shift); kk = np.digitize(np.log10(gbs), GRID) - 1; Wl = []
        for i in ops[cl]["ix"]:
            Sx = np.where(kk == wv[i])[0]; Ci_ = np.linalg.inv(C_[np.ix_(Sx, Sx)]); a_ = gl[Sx] @ Ci_ @ gl[Sx]; Wl.append((Sx, (Ci_ @ gl[Sx]) / a_))
        S["lens"][cl] = dict(gbs=gbs, gl=gl, W=Wl, shift=shift)
    S["sparc"] = {}
    for cl, msk in (("SS", SMALL), ("SL", LARGE)):
        idx = np.where(msk)[0]; kk = np.digitize(sp_lg[idx], GRID) - 1; grp = []
        for i in ops[cl]["ix"]:
            sel = idx[kk == wv[i]]; u, inv = np.unique(sp_code[sel], return_inverse=True); grp.append((sel, inv, len(u)))
        S["sparc"][cl] = grp
    D = CLD[f]; kk = np.digitize(D["lr"], GRID) - 1; S["clus"] = [(kk == wv[i]) for i in ops["CL"]["ix"]]
    Dd = DWD[f]; S["dwcell"] = [Dd["k"] == wv[i] for i in ops["DW"]["ix"]]
    return S

def struct_for(f, sh_ls, floor, sh_ld=0.0):
    cells, C = build_shift(f, sh_ls, sh_ld); return obs_struct2(f, cells, C, floor, sh_ls, sh_ld)

def prec_of(rec, p):
    if p == "P5": return None
    return {(i, "th"): (rec["calib"][s]["theta"], rec["calib"][s]["theta_plus"], rec["calib"][s]["theta_minus"]) for i, s in enumerate(SG)}

def grade_both(p, f, S, obs, mode=None):
    v, se, oDW = obs
    rg = grade(p, f, S, v, se, oDW, mode=mode, withhold=GAL_WITHHOLD)
    ra = grade(p, f, S, v, se, oDW, mode=mode, prec=prec_of(rg, p))
    return rg, ra

def combine(cg, ca):
    if cg == "SURVIVES": return "SURVIVES (all)" if ca == "SURVIVES" else "SURVIVES (galaxy-scale)"
    return cg
def overall(per):
    a, b = per["canonical"], per["alt"]
    if a == b: return a
    if a.startswith("SURVIVES") and b.startswith("SURVIVES"): return "SURVIVES (galaxy-scale)"
    return "UNDERDETERMINED (SPLIT BY FOOTING)"

def F1_at(f, sh, floor=None):
    """GLS class mean (and se) of the n>2 lens cells at M* shift sh (CFG919 cell code; CFG921's GLS on the LS block)"""
    floor = FLOOR0 if floor is None else floor
    c, CE = cells_lens("LS", *lens_set("sph", f, sh), 0.80); E = np.array([x["E"] for x in c]); Ct = CE + floor ** 2 * np.eye(len(c))
    Ci = np.linalg.inv(Ct); one = np.ones(len(c)); a = float(one @ Ci @ one); return float(one @ Ci @ E) / a, a ** -0.5

def rj(o): return json.loads(json.dumps(o, default=jdef))
def deep_json(a, b, path, mis):
    """max relative numeric difference between a (this lane, JSON round-tripped) and b (reference JSON); mismatches -> mis"""
    if isinstance(b, dict):
        if not isinstance(a, dict) or set(a) != set(b):
            mis.append(f"{path}: keys {sorted(set(a) ^ set(b)) if isinstance(a, dict) else type(a).__name__}"); return math.inf
        return max([deep_json(a[k], b[k], f"{path}.{k}", mis) for k in b] + [0.0])
    if isinstance(b, list):
        if not isinstance(a, list) or len(a) != len(b): mis.append(f"{path}: list"); return math.inf
        return max([deep_json(x, y, f"{path}[{i}]", mis) for i, (x, y) in enumerate(zip(a, b))] + [0.0])
    if isinstance(b, bool) or b is None or isinstance(b, str) or isinstance(a, (bool, str)) or a is None:
        if a != b: mis.append(f"{path}: {a!r} != {b!r}"); return math.inf
        return 0.0
    a_, b_ = float(a), float(b)
    if math.isnan(a_) and math.isnan(b_): return 0.0
    if math.isinf(a_) or math.isinf(b_):
        if a_ != b_: mis.append(f"{path}: {a_} != {b_}"); return math.inf
        return 0.0
    return abs(a_ - b_) / max(1.0, abs(b_))
def deep_np(a, b):
    if isinstance(a, dict):
        if not isinstance(b, dict) or set(a) != set(b): return math.inf
        return max([deep_np(a[k], b[k]) for k in a] + [0.0])
    if isinstance(a, (list, tuple)):
        if not isinstance(b, (list, tuple)) or len(a) != len(b): return math.inf
        return max([deep_np(x, y) for x, y in zip(a, b)] + [0.0])
    if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
        a_, b_ = np.asarray(a), np.asarray(b)
        if a_.shape != b_.shape: return math.inf
        if a_.size == 0: return 0.0
        if a_.dtype.kind in "biuU" or b_.dtype.kind in "biuU": return 0.0 if np.array_equal(a_, b_) else math.inf
        return float(np.max(np.abs(a_.astype(float) - b_.astype(float))))
    if isinstance(a, (str, bool)) or a is None or b is None: return 0.0 if a == b else math.inf
    return abs(float(a) - float(b))

# =====================================================================================================================  K2: lens rebuild + obs_struct copy
k2b, k2s = [], []
for f in FOOTS:
    c0, C0, _ = BASE[f]; c1, C1 = build_shift(f, SHIFT_N2); k2b += [deep_np(c1, c0), deep_np(C1, C0)]
    c0n, C0n, _ = build(f, {"noshift": True}); c1n, C1n = build_shift(f, 0.0); k2b += [deep_np(c1n, c0n), deep_np(C1n, C0n)]
    for vk, sh, fl in (("V0", SHIFT_N2, FLOOR0), ("V6", SHIFT_N2, FLOOR_V6), ("V7", 0.0, FLOOR0)):
        k2s.append(deep_np(struct_for(f, sh, fl), N["obs_struct"](f, vk)))
KOK.append(check("K2 lens rebuild at 0.123 / 0.0 == CFG919 build(f, {}) / build(f, {noshift}) exactly; obs_struct copy == CFG921's (V0, V6, V7), both footings",
                 max(k2b) == 0.0 and max(k2s) <= 1e-12, f"build max |diff| {max(k2b):.1e}; obs_struct max |diff| {max(k2s):.1e}"))

# =====================================================================================================================  K1: C1 and C2 off -> CFG921 exactly
assert ZTF921 == float(R921["trials"]["z_TF"])
k1max, k1mis, k1n = 0.0, [], 0
CLS921 = {}
for f in FOOTS:
    for vk, sh, fl in (("V0", SHIFT_N2, FLOOR0), ("V6", SHIFT_N2, FLOOR_V6), ("V7", 0.0, FLOOR0)):
        S = struct_for(f, sh, fl); obs = obs_facts(S, f); v, se, oDW = obs
        if vk == "V0":
            k1max = max(k1max, deep_json(rj({k: dict(obs=v[k], se=se[k]) for k in v}), R921["observed"][f], f"observed.{f}", k1mis))
        for p in POSITS:
            rec = grade(p, f, S, v, se, oDW); k1max = max(k1max, deep_json(rj(rec), R921["byfoot"][f][vk][p], f"{f}.{vk}.{p}", k1mis)); k1n += 1
            CLS921[(f, vk, p)] = rec
            if vk == "V0":
                recC = grade(p, f, S, v, se, oDW, withhold=GAL_WITHHOLD, prec=prec_of(rec, p))
                k1max = max(k1max, deep_json(rj(recC), R921["byfoot"][f]["VC_" + p], f"{f}.VC.{p}", k1mis)); k1n += 1
                CLS921[(f, "VC", p)] = recC
_cls_re = {}
for p in POSITS:
    per = {f: CLS921[(f, "V0", p)]["cls"] for f in FOOTS}; ov = per["canonical"] if per["canonical"] == per["alt"] else "UNDERDETERMINED (SPLIT BY FOOTING)"
    ch = [f"{f}:{vk}" for f in FOOTS for vk in ("V6", "V7") if CLS921[(f, vk, p)]["cls"] != per[f]]
    perC = {f: CLS921[(f, "VC", p)]["cls"] for f in FOOTS}; ovC = perC["canonical"] if perC["canonical"] == perC["alt"] else "UNDERDETERMINED (SPLIT BY FOOTING)"
    _cls_re[p] = dict(per_footing=per, overall=ov, fragile=bool(ch), variants_changing=ch, VC_per_footing=perC, VC_overall=ovC,
                      robust_TF={f: CLS921[(f, "V0", p)].get("robust_TF") for f in FOOTS}, decisive={f: CLS921[(f, "V0", p)].get("decisive") for f in FOOTS})
k1max = max(k1max, deep_json(rj(_cls_re), R921["classes"], "classes", k1mis))
RES["K1"] = dict(records_compared=k1n, max_rel_diff=k1max, mismatches=k1mis[:20])
KOK.append(check("K1 C1 and C2 off: CFG921's classes and numbers reproduced (V0, V6, V7, VC records, observed facts, classes block; both footings)",
                 k1max <= 1e-12 and not k1mis, f"{k1n} posit records + observed + classes; max rel diff {k1max:.1e}; mismatches {len(k1mis)}"
                 + (f" (first: {k1mis[0]})" if k1mis else "")))

# =====================================================================================================================  K3: CFG926 numbers through this lane's path
DRED, DBLUE = float(R926["relation"]["D_red"]), float(R926["relation"]["D_blue"])
DS = {f: float(R926["byfoot"][f]["posthoc_sluggs_ceiling"]["D"]) for f in FOOTS}
RW = {}; k3 = []
for f in FOOTS:
    r = R926["byfoot"][f]; w = r["window850"]
    RW[f] = 1.0 - math.log(w["after"]["A_red"]) / math.log(w["before"]["A_red"])
    k3 += [abs(F1_at(f, SHIFT_N2)[0] - r["target_F1"]["obs"]), abs(F1_at(f, SHIFT_N2)[1] - r["target_F1"]["se"]),
           abs(F1_at(f, SHIFT_N2 + DRED)[0] - r["target_F1"]["res"]), abs(F1_at(f, SHIFT_N2 + DS[f])[0] - r["posthoc_sluggs_ceiling"]["F1"]),
           abs(F1_at(f, SHIFT_N2)[0] - R921["observed"][f]["F1"]["obs"])]
KOK.append(check("K3 CFG926 R5 numbers through this lane's path: F1 at 0.123 (obs, se), 0.123 + D_red, 0.123 + SLUGGS D; r_W from window850",
                 max(k3) <= 1e-9, f"max |diff| {max(k3):.1e}; D_red {DRED:.5f}, D_blue {DBLUE:.5f}, SLUGGS D {DS['canonical']:.3f}; "
                 f"r_W {RW['canonical']:.4f} / {RW['alt']:.4f}"))
K_ALL = all(KOK)
P(f"  K-stage {'ALL PASS' if K_ALL else 'FAILED'}  [{time.time() - T0:.0f} s, {rss_mb():.0f} MB]")
RES["K_all"] = K_ALL
if not K_ALL:
    P("  A K-test failed: per criteria section 7 the lane stops; no class is reported."); RES["class"] = None; finish(2)
if KONLY:
    P("  CFG928_KONLY=1: K-stage only (no C1/C2 grading printed)."); finish(0)

# =====================================================================================================================  trials factor (recomputed)
N_T, NF = 20, 11
ZTF = float(norm.isf(0.0027 / 2 / (N_T * NF))); N["ZTF"] = ZTF                     # CFG921's grade reads ZTF from its namespace
RES["trials"] = dict(N_T=N_T, framings=["CFG921 V0", "CFG921 VC", "CFG928 galaxy-scale", "CFG928 all"], n_facts=NF, tests=N_T * NF,
                     z_TF=ZTF, z_TF_CFG921=ZTF921)

# =====================================================================================================================  C1-W shift (observed lens data only, before any posit is graded)
def solve_dw(f):
    F0 = F1_at(f, SHIFT_N2)[0]; T = (1.0 - RW[f]) * F0
    grid = list(np.arange(0.0, DRED, 0.001)) + [DRED]; prev = 0.0
    for g in grid:
        if F1_at(f, SHIFT_N2 + g)[0] <= T:
            lo, hi = prev, g
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if F1_at(f, SHIFT_N2 + mid)[0] <= T: hi = mid
                else: lo = mid
            F1g = F1_at(f, SHIFT_N2 + hi)[0]
            return dict(D_W=hi, target=T, F1_graded=F1g, jump=abs(F1g - T) > 1e-6, removed_frac=1 - F1g / F0)
        prev = g
    return None
DW = {f: solve_dw(f) for f in FOOTS}
assert all(DW[f] is not None for f in FOOTS)
SCN = {"C1": dict(desc="C1 primary: n>2 shift 0.123 + D_red", sh={f: SHIFT_N2 + DRED for f in FOOTS}, floor=FLOOR0, sh_ld=0.0, weight="CLASS"),
       "C1_V6": dict(desc="C1 + V6 floor 0.10 dex", sh={f: SHIFT_N2 + DRED for f in FOOTS}, floor=FLOOR_V6, sh_ld=0.0, weight="FRAGILE"),
       "C1_V7": dict(desc="C1 + V7 (no CFG667 +0.123: shift D_red alone)", sh={f: DRED for f in FOOTS}, floor=FLOOR0, sh_ld=0.0, weight="FRAGILE"),
       "C1_S": dict(desc="C1-S SLUGGS ceiling: shift 0.123 + 0.130", sh={f: SHIFT_N2 + DS[f] for f in FOOTS}, floor=FLOOR0, sh_ld=0.0, weight="C1-DEPENDENT"),
       "C1_W": dict(desc="C1-W CFG850-window equivalent: shift 0.123 + D_W", sh={f: SHIFT_N2 + DW[f]["D_W"] for f in FOOTS}, floor=FLOOR0, sh_ld=0.0, weight="C1-DEPENDENT"),
       "C1_blue": dict(desc="C1-blue diagnostic (premise broken): n<2 lenses also shifted by D_blue", sh={f: SHIFT_N2 + DRED for f in FOOTS}, floor=FLOOR0,
                       sh_ld=DBLUE, weight="DIAGNOSTIC")}
RES["inputs"] = dict(D_red=DRED, D_blue=DBLUE, D_SLUGGS=DS, r_W=RW, C1_W=DW, scenarios={k: dict(desc=v["desc"], shift_LS=v["sh"], shift_LD=v["sh_ld"],
                     floor_dex=v["floor"] / LN10, weight=v["weight"]) for k, v in SCN.items()})
P(f"\n=== inputs: D_red {DRED:+.5f} dex (CFG926 R5 point value), D_blue {DBLUE:+.5f} (diagnostic only), SLUGGS D {DS['canonical']:+.3f}")
for f in FOOTS:
    d = DW[f]
    P(f"  [{f}] C1-W: r_W {RW[f]:.4f} -> target F1 {d['target']:+.4f}; D_W {d['D_W']:+.5f} dex (graded F1 {d['F1_graded']:+.4f}, removed {d['removed_frac'] * 100:.1f}%"
      f"{', jump at a window edge' if d['jump'] else ''})")
P(f"  trials factor: N_T = {N_T} (5 posits x 4 framings: CFG921 V0, CFG921 VC, CFG928 galaxy-scale, CFG928 all); {N_T * NF} tests; z_TF = {ZTF:.3f} "
  f"(CFG921: {ZTF921:.3f})")

def run_scn(key, mode=None, posits=None):
    sc = SCN[key] if isinstance(key, str) else key; out = {}
    for f in FOOTS:
        S = struct_for(f, sc["sh"][f], sc["floor"], sc["sh_ld"]); obs = obs_facts(S, f); v, se, _ = obs
        out[f] = dict(observed={k: dict(obs=v[k], se=se[k]) for k in v}, n_LS_cells=int(len(S["ops"]["LS"]["ix"])), F7_windows=[int(x) for x in S["F7"]["windows"]], posits={})
        for p in (posits or POSITS):
            rg, ra = grade_both(p, f, S, obs, mode)
            out[f]["posits"][p] = dict(gal=rg, all=ra, combined=combine(rg["cls"], ra["cls"]))
        out[f]["_S"] = S
    return out

def zline(rec, keys=("F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8b", "F9", "F10")):
    if rec.get("reason"): return rec["reason"]
    s = "  ".join(f"{k} {rec['facts'][k]['z']:+.1f}" + ("!" if rec["facts"][k].get("sign_wrong") else "") for k in keys if k in rec["facts"] and "z" in rec["facts"][k])
    if "F8a" in rec["facts"] and "p" in rec["facts"]["F8a"]: s += f"  F8a p {rec['facts']['F8a']['p']:.2g}"
    return s + f"  | joint chi2 {rec['joint_chi2']:.1f}/{rec['joint_dof']} p {rec['joint_p']:.2g}"
def failtxt(rec):
    if rec.get("reason"): return rec["reason"]
    if rec["cls"] != "FAILS": return ""
    fl = ", ".join(f"{k} " + ("SIGN" if v.get("sign_wrong_all") else (f"min|z| {v['min_abs_z']:.2f}" if "min_abs_z" in v else f"max p {v['min_p']:.1e}"))
                   for k, v in rec["failed"].items())
    return f"[{'robust to trials factor' if rec['robust_TF'] else 'local'}; decisive {rec['decisive']}] {fl}"
def strip(out):
    return {f: {k: v for k, v in d.items() if k != "_S"} for f, d in out.items()}

# =====================================================================================================================  MUTATE uncorr
if MUT == "uncorr":
    P("\n=== MUTATE uncorr: red lenses back at +0.123 only (C1 off), C2 on; must return CFG921's classes (galaxy-scale = VC, all = V0), no SURVIVES")
    sc = dict(sh={f: SHIFT_N2 for f in FOOTS}, floor=FLOOR0, sh_ld=0.0); out = run_scn(sc); ok_all = True; res = {}
    for f in FOOTS:
        for p in POSITS:
            r = out[f]["posits"][p]; refg = R921["byfoot"][f]["VC_" + p]["cls"]; refa = R921["byfoot"][f]["V0"][p]["cls"]
            ok = (r["gal"]["cls"] == refg) and (r["all"]["cls"] == refa) and not r["combined"].startswith("SURVIVES")
            ok_all &= ok; res[f"{f}|{p}"] = dict(gal=r["gal"]["cls"], all=r["all"]["cls"], combined=r["combined"], ref_VC=refg, ref_V0=refa, ok=ok,
                                                  gal_failed=r["gal"].get("failed"), gal_robust_TF_928=r["gal"].get("robust_TF"))
            P(f"  [{f}] {p}: galaxy-scale {r['gal']['cls']} (CFG921 VC {refg}), all {r['all']['cls']} (CFG921 V0 {refa}) -> combined {r['combined']}  "
              f"{'OK' if ok else 'MISMATCH'}  {failtxt(r['gal'])}")
    RES["mutate_uncorr"] = res; RES["bites"] = bool(ok_all)
    P(f"  MUTATE uncorr {'BITES (CFG921 classes returned, no survivor)' if ok_all else 'DOES NOT BITE'}  [{time.time() - T0:.0f} s, {rss_mb():.0f} MB]")
    finish(1 if ok_all else 0)

# =====================================================================================================================  MUTATE sign
if MUT == "sign":
    P("\n=== MUTATE sign (C1 + C2 on): M1a reversed surplus and M1b sign-flipped predictions (P1-P4), galaxy-scale and all; all 32 must FAIL")
    res = {}; allfail = True; n = 0
    for mode, lab in (("rev", "M1a"), ("flip", "M1b")):
        out = run_scn("C1", mode=mode, posits=("P1", "P2", "P3", "P4"))
        for f in FOOTS:
            for p in ("P1", "P2", "P3", "P4"):
                r = out[f]["posits"][p]
                for fr in ("gal", "all"):
                    n += 1; ok = r[fr]["cls"] == "FAILS"; allfail &= ok
                    res[f"{f}|{p}|{lab}|{fr}"] = dict(cls=r[fr]["cls"], reason=r[fr].get("reason"), decisive=r[fr].get("decisive"))
                P(f"  [{f}] {p} {lab}: galaxy-scale {r['gal']['cls']} ({r['gal'].get('reason') or r['gal'].get('decisive')}), all {r['all']['cls']} "
                  f"({r['all'].get('reason') or r['all'].get('decisive')})")
    RES["mutate_sign"] = res; RES["bites"] = bool(allfail and n == 32)
    P(f"  MUTATE sign {'BITES (all 32 FAIL)' if RES['bites'] else 'DOES NOT BITE'} ({n} cases)  [{time.time() - T0:.0f} s, {rss_mb():.0f} MB]")
    finish(1 if RES["bites"] else 0)

# =====================================================================================================================  MAIN
ALL = {}
P("\n=== observed red-lens facts per scenario (E in ln units; dex = E/ln10)")
for key in SCN:
    ALL[key] = run_scn(key)
    for f in FOOTS:
        o = ALL[key][f]["observed"]
        P(f"  {key:8s} [{f:9s}] F1 {o['F1']['obs']:+.4f} +- {o['F1']['se']:.4f} ({o['F1']['obs'] / LN10:+.4f} dex)  F7 {o['F7']['obs']:+.4f} +- {o['F7']['se']:.4f}  "
          f"F2 {o['F2']['obs']:+.4f} +- {o['F2']['se']:.4f}  | LS cells {ALL[key][f]['n_LS_cells']}, F7 windows {ALL[key][f]['F7_windows']}")
P(f"  (CFG921, uncorrected: F1 {R921['observed']['canonical']['F1']['obs']:+.4f} / {R921['observed']['alt']['F1']['obs']:+.4f}; "
  f"F7 {R921['observed']['canonical']['F7']['obs']:+.4f} / {R921['observed']['alt']['F7']['obs']:+.4f})  [{time.time() - T0:.0f} s, {rss_mb():.0f} MB]")

# ---- stage P: C1 predictions at the calibrated constants (nominal corner)
P("\n=== stage P (C1 primary): each posit's nominal predictions at its calibrated constant (same dwarf calibration as CFG921)")
th_diff = 0.0
for f in FOOTS:
    cen = lens_central("LS", f, LENS_NOM, SCN["C1"]["sh"][f])
    P(f"  [{f}] n>2 central proxy under C1: log M {cen['lm']:.3f}, R_e {cen['Re']:.2f} kpc, v_c {cen['vc']:.1f} km/s, sigma {cen['sig']:.1f} km/s")
    for p in POSITS:
        ra = ALL["C1"][f]["posits"][p]["all"]
        if ra.get("reason"):
            P(f"  [{f}] {p}: {ra['reason']}"); continue
        if p != "P5":
            th_diff = max(th_diff, max(abs(ra["calib"][s]["theta"] - R921["byfoot"][f]["V0"][p]["calib"][str(s)]["theta"]) for s in SG))
        th = ra["calib"][10.0]["theta"] if p != "P5" else None
        P(f"  [{f}] {p} theta {('%.4g' % th) if th else '-':>9}: " + "  ".join(f"{k} {ra['facts'][k]['pred']:+.3f}" for k in FACTS if k in ra["facts"] and "pred" in ra["facts"][k]))
P(f"  calibrated constants identical to CFG921 V0 (dwarf cells unchanged): max |d theta| {th_diff:.1e}")
RES["theta_vs_CFG921_max_diff"] = th_diff

# ---- stage G: grading
P(f"\n=== stage G: grading, galaxy-scale (F5, F6 withheld; joint chi2 F1-F4) and all (joint chi2 F1-F5); lenient-corner FAIL rule; z_TF {ZTF:.3f}")
for key in SCN:
    P(f"  --- {key}: {SCN[key]['desc']}  [{SCN[key]['weight']}]")
    for f in FOOTS:
        for p in POSITS:
            r = ALL[key][f]["posits"][p]
            P(f"    [{f:9s}] {p}: {r['combined']:24s} (galaxy-scale {r['gal']['cls']}, all {r['all']['cls']})  {failtxt(r['gal'])}")
            if key == "C1":
                P(f"        galaxy-scale: {zline(r['gal'])}")
                if r["all"]["cls"] == "FAILS" and r["gal"]["cls"] != "FAILS": P(f"        all: {failtxt(r['all'])}  | {zline(r['all'])}")

# ---- classes
P("\n=== classes (C1 primary; labels from V6/V7 = FRAGILE, C1-S/C1-W = C1-DEPENDENT; C1-blue diagnostic only)")
CLS = {}
for p in POSITS:
    per = {f: ALL["C1"][f]["posits"][p]["combined"] for f in FOOTS}; ov = overall(per)
    frag = [f"{f}:{k}" for k in ("C1_V6", "C1_V7") for f in FOOTS if ALL[k][f]["posits"][p]["combined"] != per[f]]
    dep = [f"{f}:{k}" for k in ("C1_S", "C1_W") for f in FOOTS if ALL[k][f]["posits"][p]["combined"] != per[f]]
    diag = {f: ALL["C1_blue"][f]["posits"][p]["combined"] for f in FOOTS}
    comp = {f: dict(gal=ALL["C1"][f]["posits"][p]["gal"]["cls"], all=ALL["C1"][f]["posits"][p]["all"]["cls"],
                    gal_decisive=ALL["C1"][f]["posits"][p]["gal"].get("decisive"), gal_robust_TF=ALL["C1"][f]["posits"][p]["gal"].get("robust_TF"),
                    all_decisive=ALL["C1"][f]["posits"][p]["all"].get("decisive"), all_robust_TF=ALL["C1"][f]["posits"][p]["all"].get("robust_TF")) for f in FOOTS}
    var = {k: {f: ALL[k][f]["posits"][p]["combined"] for f in FOOTS} for k in SCN}
    CLS[p] = dict(per_footing=per, overall=ov, components=comp, fragile=bool(frag), fragile_by=frag, c1_dependent=bool(dep), c1_dependent_by=dep,
                  by_scenario=var, C1_blue_diagnostic=diag, CFG921=dict(V0=R921["classes"][p]["per_footing"], VC=R921["classes"][p]["VC_per_footing"]))
    P(f"  {p} {PNAME[p]}: canonical {per['canonical']}, alt {per['alt']} -> {ov}"
      + (f"  [FRAGILE: {', '.join(frag)}]" if frag else "") + (f"  [C1-DEPENDENT: {', '.join(dep)}]" if dep else ""))
    P("      by scenario: " + "; ".join(f"{k} {var[k]['canonical']} / {var[k]['alt']}" for k in SCN))
    P(f"      CFG921: V0 {R921['classes'][p]['per_footing']['canonical']} / {R921['classes'][p]['per_footing']['alt']}; "
      f"VC {R921['classes'][p]['VC_per_footing']['canonical']} / {R921['classes'][p]['VC_per_footing']['alt']}")
RES["classes"] = CLS
SURV = [(p, f) for p in POSITS for f in FOOTS if CLS[p]["per_footing"][f].startswith("SURVIVES")]
RES["survivors"] = [f"{p}|{f}" for p, f in SURV]
P(f"  galaxy-scale survivors (posit|footing): {RES['survivors'] if SURV else 'NONE'}"
  + ("  -- 'best of 20 posit-framings tried, post-hoc-motivated, conditional on C1'" if SURV else ""))

# ---- survivors: cluster statement + sealed-prediction numbers (declared UDG inputs; no object data)
def udg_inputs(f, Ms, Re_kpc, Mg):
    """synthetic dwarf entry with CFG914/921 conventions: g_bar = G (M*/2 + M_g,in) / r12^2 (CFG880 constants), r12 = 4/3 R_e,
    sigma_law^2 = r12 g_L / 3, w = (M*/2)/(M*/2 + M_g,in), rho = (M*/2 + M_g,in)/(4 pi r12^3 / 3)"""
    Ms, Mg = np.asarray(Ms, float), np.asarray(Mg, float); r12 = (4.0 / 3.0) * np.asarray(Re_kpc, float) * 1e3
    return udg_from(f, Ms, Mg, r12)
def udg_from(f, Ms, Mg, r12):
    Mb = Ms / 2 + Mg; gb = N880["G"] * Mb * N880["Msun"] / (r12 * N880["PC"]) ** 2; a0 = A0[f]; nu = nu_e(gb / a0); gL = gb * nu
    sl = np.sqrt(r12 * N["PC"] * gL / 3) / 1e3
    return dict(w=(Ms / 2) / Mb, nu=nu, phi=1 - 1 / nu, sl=sl, gb=gb, a0=a0, rho=Mb / (4 * math.pi / 3 * r12 ** 3), r12=r12)
def udg_E(p, th, f, D, sg):
    key = f"__udg_{f}"; DWD[key] = D
    try:
        return dw_pred(p, th, key, sg)
    finally:
        del DWD[key]
# path self-check (added, no class weight): the 83 LVD dwarfs' own (M*, M_g,in, r12) through udg_from reproduce CFG921's inputs
_pc = []
for f in FOOTS:
    D = DWD[f]; U = udg_from(f, D["Ms"], D["Mg"], D["r12"])
    _pc += [float(np.max(np.abs(U["gb"] / D["gb"] - 1))), float(np.max(np.abs(U["sl"] / D["sl"] - 1))), float(np.max(np.abs(U["w"] - D["w"]))),
            float(np.max(np.abs(U["rho"] / D["rho"] - 1)))]
    for p in ("P2", "P3", "P4"):
        th = ALL["C1"][f]["posits"][p]["all"]["calib"][10.0]["theta"]
        if th: _pc.append(float(np.max(np.abs(udg_E(p, th, f, U, 10.0) - dw_pred(p, th, f, 10.0)))))
RES["udg_path_selfcheck_max"] = max(_pc)
P(f"\n  UDG path self-check (added, no class weight): LVD dwarfs through the synthetic-entry path reproduce CFG921's g_bar, sigma_law, w, rho and "
  f"E_pred (P2-P4) to {max(_pc):.1e}")

MS_L, RE_L = (3e7, 1e8, 3e8), (1.5, 2.5, 4.0)
SEAL = {}
if SURV:
    P("\n=== survivors: cluster statement and sealed-prediction numbers (target: pressure-supported UDGs; declared inputs; E vs the isolated nu_e law)")
for p, f in SURV:
    ra = ALL["C1"][f]["posits"][p]["all"]; F5, F6 = ra["facts"]["F5"], ra["facts"]["F6"]
    cal = ra["calib"]; th, thp, thm = cal[10.0]["theta"], cal[10.0]["theta_plus"], cal[10.0]["theta_minus"]
    clus = dict(F5_pred=F5["pred"], F5_obs=F5["obs"], F5_se=F5["se"], F5_z=F5["z"], F5_min_abs_z=F5["min_abs_z"], supply_E=F5["obs"] - F5["pred"],
                supply_g_factor=math.exp(F5["obs"] - F5["pred"]), F6_pred=F6["pred"], F6_obs=F6["obs"], F6_se=F6["se"], F6_z=F6["z"],
                supply_slope=F6["obs"] - F6["pred"], all_class=ra["cls"], all_decisive=ra.get("decisive"), all_robust_TF=ra.get("robust_TF"))
    _ths = "no constant" if th is None else f"theta {th:.5g} (theta+ {thp:.5g}, theta- {thm:.5g})"
    P(f"  [{f}] {p}: {_ths}; clusters predicted F5 {F5['pred']:+.2e} (obs {F5['obs']:+.3f} +- {F5['se']:.3f}, "
      f"z {F5['z']:+.2f}), slope F6 {F6['pred']:+.2e} (obs {F6['obs']:+.3f} +- {F6['se']:.3f}) -> a separate cluster explanation must supply "
      f"E {clus['supply_E']:+.3f} (x{clus['supply_g_factor']:.2f} in g) rising {clus['supply_slope']:+.3f} per dex g_bar")
    rows = []
    Ms_g, Re_g = np.meshgrid(MS_L, RE_L, indexing="ij"); Ms_v, Re_v = Ms_g.ravel(), Re_g.ravel()
    Dfree = udg_inputs(f, Ms_v, Re_v, np.zeros_like(Ms_v)); Dgas = udg_inputs(f, Ms_v, Re_v, Ms_v / 2)
    Ef, Efp, Efm = (udg_E(p, t if t is not None else th, f, Dfree, 10.0) for t in (th, thp, thm))
    Eg = {sg: udg_E(p, cal[sg]["theta"], f, Dgas, sg) for sg in SG if (sg in cal and (cal[sg]["theta"] or p == "P5"))}
    for i in range(len(Ms_v)):
        rows.append(dict(Mstar=float(Ms_v[i]), Re_kpc=float(Re_v[i]), log_gbar=float(np.log10(Dfree["gb"][i])), sigma_law=float(Dfree["sl"][i]),
                         E_free=float(Ef[i]), E_free_dex=float(Ef[i] / LN10), s_pred=float(abs(Efp[i] - Efm[i]) / 2), sigma_pred_star=float(Dfree["sl"][i] * math.exp(Ef[i] / 2)),
                         gas_log_gbar=float(np.log10(Dgas["gb"][i])), gas_sigma_law=float(Dgas["sl"][i]), E_gas={str(sg): float(Eg[sg][i]) for sg in Eg}))
    # sigma_law grid (gas-free, deep regime summary): E as a function of sigma_law alone at fixed phi from the representative set
    SEAL[f"{p}|{f}"] = dict(theta=th, theta_plus=thp, theta_minus=thm, theta_by_sigma_g={str(sg): cal.get(sg, {}).get("theta") for sg in SG}, clusters=clus, udg_rows=rows)
    P(f"      UDG sealed numbers ({p}, {f}; gas-free primary, M_g,in = M*/2 variant at sigma_g 6/10/20):")
    P(f"      {'M*':>8} {'R_e':>5} {'lg gbar':>8} {'s_law':>6} {'E_free':>8} {'(dex)':>7} {'+-':>6} {'s_*pred':>7} | {'E_gas(6)':>8} {'E_gas(10)':>9} {'E_gas(20)':>9}")
    for r in rows:
        P(f"      {r['Mstar']:8.1e} {r['Re_kpc']:5.1f} {r['log_gbar']:8.3f} {r['sigma_law']:6.2f} {r['E_free']:+8.4f} {r['E_free_dex']:+7.4f} {r['s_pred']:6.4f} "
          f"{r['sigma_pred_star']:7.2f} | " + " ".join(f"{r['E_gas'].get(str(sg), float('nan')):+9.4f}" for sg in SG))
RES["sealed_numbers"] = SEAL
RES["scenarios"] = {k: strip(v) for k, v in ALL.items()}
P(f"\n  runtime {time.time() - T0:.0f} s, peak RSS {rss_mb():.0f} MB")
finish(0)
