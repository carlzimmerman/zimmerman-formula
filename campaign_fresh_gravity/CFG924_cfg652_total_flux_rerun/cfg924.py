"""CFG924 (criteria 4f4def674): CFG652's hot-group lensing test re-run with CFG922 A1's total-flux census.

Modes (one process at a time, OMP_NUM_THREADS=1, nice 10; run from this directory):
  CFG924_MODE=K       python3 cfg924.py  -> cfg924_K.out, cfg924_K.json                 (K1-K4b)
  CFG924_MODE=MUTATE  python3 cfg924.py  -> cfg924_MUTATE.out, cfg924_results_MUTATE.json (M-INJ end to end)
                      python3 cfg924.py  -> cfg924.out, cfg924_results.json, cfg924_census.json (A1c primary, A1u bracket, M1)
  POST HOC (AMENDMENT_AM1.md, after the frozen M-INJ end-to-end leg failed; before the main run):
  CFG924_MODE=MUTATE_B python3 cfg924.py -> cfg924_MUTATE_B.out, cfg924_results_MUTATE_B.json (M-INJb wiring control)
  CFG924_MODE=JITTER   python3 cfg924.py -> cfg924_JITTER.out, cfg924_results_JITTER.json   (model-(a) noise ensemble; after MAIN)
Reuse (read-only, by exec of text slices of committed sources; nothing of theirs is imported or written): CFG922 read_cols /
load_bright (A1 branch) / census_652 / Census / mlim_table / unit, CFG686's distance slice (K4b only), CFG652 cfg652_test.py
preamble + models block + score block verbatim (WORK and the output directory redirected), cfg652_model (imported).
Work files: _external_data/cfg924_work/{A1c,A1u,SAME,INJ}. Nothing downloaded.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
os.environ.pop("MUTATE", None); os.environ.pop("POSTHOC", None)
import io, json, math, time, shutil, hashlib, tempfile, contextlib, subprocess, resource, warnings
import numpy as np
from scipy.spatial import cKDTree
from scipy.special import erfc
from scipy.interpolate import PchipInterpolator
warnings.filterwarnings("ignore", category=RuntimeWarning)
try:
    os.nice(10)
except OSError:
    pass

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
C652 = os.path.join(LANES, "CFG652_hot_group_discriminator"); C922 = os.path.join(LANES, "CFG922_cluster_core_baryon_recheck")
C686 = os.path.join(LANES, "CFG686_cluster_shear_vs_law"); C687 = os.path.join(LANES, "CFG687_erass1_shear_stack")


def _main_checkout():
    """the main checkout (data and _external_data live beside it; a worktree has neither)."""
    try:
        g = subprocess.run(["git", "-C", REPO, "rev-parse", "--path-format=absolute", "--git-common-dir"], capture_output=True,
                           text=True, check=True).stdout.strip()
        return os.path.dirname(g)
    except Exception:
        return REPO


MAINCO = _main_checkout()
DATA = next(os.path.join(r, "real_research", "data") for r in (REPO, MAINCO)
            if os.path.exists(os.path.join(r, "real_research", "data", "lensing_rar", "KiDS_DR4_brightsample.fits")))
EXT = next(os.path.abspath(os.path.join(r, "..", "_external_data")) for r in (REPO, MAINCO)
           if os.path.isdir(os.path.join(r, "..", "_external_data", "cfg652_work")))
W652 = os.path.join(EXT, "cfg652_work"); WORK = os.path.join(EXT, "cfg924_work")
MODE = os.environ.get("CFG924_MODE", "MAIN")
TAG = {"K": "_K", "MUTATE": "_MUTATE", "MUTATE_B": "_MUTATE_B", "JITTER": "_JITTER"}.get(MODE, "")
OUT = open(os.path.join(HERE, "cfg924" + TAG + ".out"), "w")
T0 = time.time()
FEET = ("canonical", "alt"); VK = ("x1", "p02", "m02", "g1", "g4")
VAR = (("x1", 1.0, 2.0), ("p02", 10 ** 0.2, 2.0), ("m02", 10 ** -0.2, 2.0), ("g1", 1.0, 1.0), ("g4", 1.0, 4.0))   # CFG652 models block
SHA_MODEL = "04352d4eec05b2825fd6d89842599f9e0b8149f4e5ea6ac36e404857e80d60d1"


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()


def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()


def rss_gb(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)


def cut(txt, a, b):
    assert txt.count(a) == 1, a
    i = txt.index(a); return txt[i:txt.index(b, i)]


# ---- CFG922 slices (census code) + CFG686 distance slice ----
T922 = open(os.path.join(C922, "cfg922.py")).read(); T686 = open(os.path.join(C686, "cfg686_shear.py")).read()
NS922 = dict(os=os, np=np, math=math, cKDTree=cKDTree, erfc=erfc, PchipInterpolator=PchipInterpolator, AMEND="", DATA=DATA, RAP=0.5,
             __name__="cfg922_slices")
exec(cut(T686, "# ---- distances from raw DESI DR2 BAO", "# ---- clusters:"), NS922)
exec(cut(T922, "def unit(ra, de):", "# ---- KiDS bright census ----"), NS922)
exec(cut(T922, "def read_cols(", "def mlim_table("), NS922)                 # read_cols + load_bright (with its A1 branch)
exec(cut(T922, "def mlim_table(", "def census_652("), NS922)                # mlim_table + Census
exec(cut(T922, "def census_652(", "# ---- other on-disk brackets ----"), NS922)
census_652 = NS922["census_652"]


def load_bright(amend):
    NS922["AMEND"] = amend
    return NS922["load_bright"]()


# ---- CFG652 test: preamble, models block and score block, verbatim ----
F652 = os.path.join(C652, "cfg652_test.py"); T652 = open(F652).read()
MARK_IN = "# ============================================================================================== inputs"
assert T652.count(MARK_IN) == 1
PRE652 = T652.split(MARK_IN)[0]
assert "if MODE ==" not in PRE652 and "json.dump" not in PRE652     # the preamble alone: it can never run a stage or write a file
os.environ["CFG652_MODE"] = "none"                                       # belt and braces: no CFG652 stage matches this
WLINE = 'WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg652_work"))'
assert PRE652.count(WLINE) == 1
PRE652 = PRE652.replace(WLINE, "WORK = _WORK_OVERRIDE")
MODELS652 = cut(T652, 'if MODE == "models":', "# ============================================================================================== score")
SCORE652 = T652[T652.index('if MODE == "score":'):]
assert MODELS652.count("if MODE ==") == 1 and SCORE652.count("if MODE ==") == 1 and "np.savez" not in SCORE652
sys.path.insert(0, C652)
import cfg652_model as M                                                   # noqa: E402  (this checkout; sha256 checked)
assert os.path.dirname(os.path.abspath(M.__file__)) == C652
SOURCES = {k: sha(p) for k, p in (("cfg652_test.py", F652), ("cfg652_model.py", os.path.join(C652, "cfg652_model.py")),
                                  ("cfg922.py", os.path.join(C922, "cfg922.py")), ("cfg686_shear.py", os.path.join(C686, "cfg686_shear.py")))}


def ns652(work):
    NS = {"__file__": F652, "__name__": "cfg652_reuse", "_WORK_OVERRIDE": work}
    exec(compile(PRE652, F652, "exec"), NS)
    NS.setdefault("__doc__", T652.split('"""')[1])
    return NS


def score652(work, mut=False, posthoc=False):
    """CFG652's score block verbatim on the files in `work`; returns (results dict, printed text)."""
    NS = ns652(work); NS["MODE"] = "score"; NS["MUT"] = mut; tmp = tempfile.mkdtemp(prefix="cfg924_score_"); NS["HERE"] = tmp
    assert os.path.abspath(NS["HERE"]) != C652 and os.path.abspath(NS["WORK"]) == os.path.abspath(work)
    if posthoc:
        os.environ["POSTHOC"] = "1"
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(SCORE652, F652, "exec"), NS)
        tag = ("_MUTATE" if mut else "") + ("_POSTHOC" if posthoc else "")
        res = json.load(open(os.path.join(tmp, f"cfg652_test_results{tag}.json"))); txt = open(os.path.join(tmp, f"cfg652_test{tag}.out")).read()
    finally:
        os.environ.pop("POSTHOC", None); shutil.rmtree(tmp, ignore_errors=True)
    return res, txt


def models652(work):
    """CFG652's models block verbatim (all variants + M1) on work/cfg652_inputs.npz -> work/cfg652_models.npz."""
    NS = ns652(work); NS["MODE"] = "models"
    assert os.path.abspath(NS["WORK"]) == os.path.abspath(work) and os.path.abspath(work) != os.path.abspath(W652)
    exec(compile(MODELS652, F652, "exec"), NS)


def model_row(Mc, Mh, Rx, z, foot, model, fac=1.0, gt=2.0, m1=False):
    """the identical calls of CFG652's models block for one group."""
    if m1:
        o = M.system(Mc, Mh, Rx, z, foot, "a", N=600, hot_as_condensed=True)
    else:
        o = M.system(Mc * fac, Mh, Rx, z, foot, model, N=600, gas_trunc=gt)
    return M.delta_sigma(o["rg"], o["Mbound"], NS_RC, rmax=o["rta"])


NS_RC = ns652(W652)["RC"]


def models_x1(work, label):
    """x1 only (both footings, both models); p02/m02/g1/g4 entries are copies of x1 (declared: their labels carry no weight)."""
    I = np.load(os.path.join(work, "cfg652_inputs.npz")); n = len(I["z"]); out = {}
    for foot in FEET:
        for model in "ab":
            arr = np.full((n, len(NS_RC)), np.nan)
            for i in range(n):
                if I["Mcond"][i] > 0:
                    arr[i] = model_row(I["Mcond"][i], I["Mhot"][i], I["Rx_kpc"][i], I["z"][i], foot, model)
            for vk in VK:
                out[f"{foot}__{vk}__{model}"] = arr
            P(f"  [{label}] models {foot} x1 {model} done ({time.time() - T0:.0f} s)")
    np.savez(os.path.join(work, "cfg652_models.npz"), **out)


I652 = np.load(os.path.join(W652, "cfg652_inputs.npz"))
ST = {t: json.load(open(os.path.join(C652, f"cfg652_test_results{t}.json"))) for t in ("", "_MUTATE", "_POSTHOC")}


def write_inputs(work, Mc, Mb):
    os.makedirs(work, exist_ok=True)
    d = {k: I652[k] for k in I652.files}
    Mc = np.asarray(Mc, float); Mb = np.asarray(Mb, float)
    d["Mcond"] = Mc; d["Mbcg"] = Mb; d["fhot"] = d["Mhot"] / (d["Mhot"] + Mc)
    np.savez(os.path.join(work, "cfg652_inputs.npz"), **d)
    shutil.copyfile(os.path.join(W652, "cfg652_esd.npz"), os.path.join(work, "cfg652_esd.npz"))


def compare(a, b, path="", acc=None):
    """recursive comparison of two result trees: max abs numeric diff (chi2 keys separately) and non-numeric mismatches."""
    if acc is None:
        acc = dict(num=0.0, chi2=0.0, mism=[])
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                acc["mism"].append(f"{path}/{k}: missing"); continue
            compare(a[k], b[k], f"{path}/{k}", acc)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            acc["mism"].append(f"{path}: len {len(a)} vs {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            compare(x, y, f"{path}[{i}]", acc)
    elif isinstance(a, bool) or isinstance(b, bool) or isinstance(a, str) or isinstance(b, str) or a is None or b is None:
        if a != b:
            acc["mism"].append(f"{path}: {a!r} vs {b!r}")
    else:
        x, y = float(a), float(b)
        d = 0.0 if (math.isnan(x) and math.isnan(y)) else abs(x - y)
        if math.isnan(d):
            acc["mism"].append(f"{path}: nan vs number"); d = 0.0
        key = "chi2" if "chi2" in path.rsplit("/", 1)[-1] else "num"
        acc[key] = max(acc[key], d)
    return acc


def coverage(B):
    """A1 footprint coverage mirrored on CFG652's apertures: all bright rows in the G09 box (any z / mask / mass), planar metric,
    count inside R_X over (count in 3-6 R_X) / 27."""
    box = (B["ra"] > 122) & (B["ra"] < 150) & (B["dec"] > -7) & (B["dec"] < 9)
    t = cKDTree(np.c_[B["ra"][box] * np.cos(np.radians(B["dec"][box])), B["dec"][box]])
    cov = np.zeros(len(I652["z"])); nap = np.zeros(len(cov), int); nann = np.zeros(len(cov), int)
    for i in range(len(cov)):
        th = I652["R500_arcmin"][i] / 60.0; p = [I652["ra"][i] * math.cos(math.radians(I652["dec"][i])), I652["dec"][i]]
        n1, n3, n6 = (int(t.query_ball_point(p, r * th, return_length=True)) for r in (1, 3, 6))
        nap[i], nann[i] = n1, n6 - n3
        cov[i] = n1 / ((n6 - n3) / 27.0) if n6 > n3 else 0.0
    return cov, nap, nann


def footprint(Mc, Mb, cov, upper):
    """A1 footprint step: < 0.5 NOT MEASURED (median / 84th-pct M_cond/M_hot x M_hot; median BCG share), 0.5-1 divided by coverage."""
    Mc = Mc.copy(); Mb = Mb.copy(); Mh = I652["Mhot"]; meas = cov >= 0.5; part = meas & (cov < 1.0)
    Mc[part] /= cov[part]; Mb[part] /= cov[part]
    ref = meas & (Mc > 0); rat = Mc[ref] / Mh[ref]; r_use = float(np.percentile(rat, 84) if upper else np.median(rat))
    share = float(np.median(Mb[ref] / Mc[ref]))
    for i in np.where(~meas)[0]:
        Mc[i] = r_use * Mh[i]; Mb[i] = share * Mc[i]
    return Mc, Mb, dict(n_not_measured=int((~meas).sum()), n_partial=int(part.sum()), ratio_used=r_use, ratio_median=float(np.median(rat)),
                        ratio_p84=float(np.percentile(rat, 84)), bcg_share=share, n_ref=int(ref.sum()))


def apply_flux(B0, fs, cap):
    """CFG922 A1's correction line on MASS_MED: brighten only; cap (mag) None = uncapped."""
    v = B0["mmed"] > 5; d = np.minimum(fs, 0.0) if cap is None else np.clip(fs, -cap, 0.0)
    B = dict(B0); B["mmed"] = np.where(v, B0["mmed"] - 0.4 * d, B0["mmed"]); B["ok"] = (B["mmed"] > 5) & np.isfinite(B["z"])
    return B


def bracket_stats(Mnew, Mold):
    s = (Mnew > 0) & (Mold > 0); d = np.log10(Mnew[s] / Mold[s]); med = float(np.median(d))
    cls = "BRACKET EXCEEDED (HIGH)" if med > 0.2 else ("BRACKET EXCEEDED (LOW)" if med < -0.2 else "BRACKET COVERS")
    return dict(n=int(s.sum()), median=med, p16=float(np.percentile(d, 16)), p84=float(np.percentile(d, 84)), frac_gt_0p2=float(np.mean(d > 0.2)),
                frac_lt_0=float(np.mean(d < 0)), max=float(d.max()), min=float(d.min()), cls=cls)


P(f"CFG924 {MODE} (criteria 4f4def674). CFG652 stored sample {len(I652['z'])} groups ({int((I652['Mcond'] > 0).sum())} with M_cond > 0).")
P(f"  sources sha256: " + ", ".join(f"{k} {v[:12]}" for k, v in SOURCES.items()))
assert SOURCES["cfg652_model.py"] == SHA_MODEL, "cfg652_model.py changed since the CFG652 freeze"

# =====================================================================================================================
if MODE == "K":
    K = {}
    # K1: frozen census reproduces CFG652's stored masses
    B0 = load_bright("")
    Mc, Mb = census_652(B0, I652["ra"], I652["dec"], I652["z"], I652["R500_arcmin"])
    r1 = max(float(np.max(np.abs(Mc - I652["Mcond"]) / np.maximum(I652["Mcond"], 1))), float(np.max(np.abs(Mb - I652["Mbcg"]) / np.maximum(I652["Mbcg"], 1))))
    K["K1"] = dict(n=int(len(Mc)), maxrel=r1, align_maxdiff_deg=B0["align_maxdiff_deg"], pass_=bool(r1 < 1e-9))
    P(f"K1 census F vs CFG652 stored M_cond/M_bcg (N {len(Mc)}): max rel {r1:.1e}; bright/LePhare RA alignment {B0['align_maxdiff_deg']:.1e} deg"
      f" -> {'PASS' if K['K1']['pass_'] else 'FAIL'}"); del B0
    # K2: CFG652's verbatim score block on its own stored work files reproduces its stored JSONs
    k2 = {}
    for t, mut, ph in (("", False, False), ("_POSTHOC", False, True), ("_MUTATE", True, False)):
        res, _ = score652(W652, mut=mut, posthoc=ph); c = compare(res, ST[t])
        k2[t or "_primary"] = dict(max_abs_chi2=c["chi2"], max_abs_other=c["num"], mismatches=c["mism"][:20], final=res["final"],
                                   pass_=bool(c["chi2"] < 1e-6 and c["num"] < 1e-9 and not c["mism"]))
        P(f"K2 score{t or ' (primary)'}: max |d chi2| {c['chi2']:.1e}, max |d other| {c['num']:.1e}, mismatches {len(c['mism'])}; final '{res['final']}'"
          f" -> {'PASS' if k2[t or '_primary']['pass_'] else 'FAIL'}")
    K["K2"] = dict(k2, pass_=all(v["pass_"] for v in k2.values()))
    # K3: model engine reproduces the stored model arrays for 6 groups
    MD = np.load(os.path.join(W652, "cfg652_models.npz")); idx = np.where(I652["Mcond"] > 0)[0]; order = idx[np.argsort(I652["Mcond"][idx])]
    picks = [int(order[int(round(q * (len(order) - 1)))]) for q in (0, 0.2, 0.4, 0.6, 0.8, 1.0)]
    r3 = 0.0; nanok = True
    for i in picks:
        g = (I652["Mcond"][i], I652["Mhot"][i], I652["Rx_kpc"][i], I652["z"][i])
        for foot in FEET:
            for vk, fac, gt in VAR:
                for model in "ab":
                    new = model_row(*g, foot, model, fac=fac, gt=gt); old = MD[f"{foot}__{vk}__{model}"][i]
                    nanok &= bool(np.array_equal(np.isnan(new), np.isnan(old))); r3 = max(r3, float(np.nanmax(np.abs(new / old - 1))))
            new = model_row(*g, foot, "a", m1=True); old = MD[f"{foot}__M1__a"][i]; r3 = max(r3, float(np.nanmax(np.abs(new / old - 1))))
        P(f"   K3 group {i} (M_cond {I652['Mcond'][i]:.3e}) done; running max rel {r3:.1e} ({time.time() - T0:.0f} s)")
    K["K3"] = dict(groups=picks, maxrel=r3, nan_pattern_equal=nanok, sha256=SOURCES["cfg652_model.py"], pass_=bool(r3 < 1e-10 and nanok))
    P(f"K3 cfg652_model vs stored arrays (6 groups x 22): max rel {r3:.1e}; NaN pattern equal {nanok} -> {'PASS' if K['K3']['pass_'] else 'FAIL'}")
    # K4a/K4b: CFG922's A1 census reproduces its stored values
    B1 = load_bright("A1"); R922 = json.load(open(os.path.join(C922, "cfg922_results_A1.json")))["A1"]
    fsg = B1["fluxscale"][B1["ok"]]; got = [float(np.median(fsg)), float(np.percentile(fsg, 16)), float(np.percentile(fsg, 84))]
    want = [R922["fluxscale_median"]] + list(R922["fluxscale_p16_p84"]); d4a = max(abs(a - b) for a, b in zip(got, want))
    K["K4a"] = dict(got=got, stored=want, maxabs=d4a, pass_=bool(d4a < 1e-12))
    P(f"K4a A1 fluxscale median / p16 / p84 {np.round(got, 6).tolist()} vs CFG922 {np.round(want, 6).tolist()}: max abs {d4a:.1e} -> {'PASS' if K['K4a']['pass_'] else 'FAIL'}")
    PC7 = np.load(os.path.join(C687, "cfg687_percluster.npz")); CJ = json.load(open(os.path.join(C922, "cfg922_census_A1.json")))["eRASS1"]
    CEN = NS922["Census"](B1); r4 = 0.0
    for i in range(len(PC7["ra"])):
        c = CEN.run(PC7["ra"][i], PC7["dec"][i], PC7["z"][i])
        for k in ("net_med", "net_sup", "sig_sup", "coverage"):
            r4 = max(r4, abs(c[k] - CJ[i][k]) / max(abs(CJ[i][k]), 1.0))
    K["K4b"] = dict(n=int(len(PC7["ra"])), maxrel=float(r4), pass_=bool(r4 < 1e-9))
    P(f"K4b CFG922 Census under A1 vs cfg922_census_A1.json (N {len(PC7['ra'])}; net_med, net_sup, sig_sup, coverage): max rel {r4:.1e}"
      f" -> {'PASS' if K['K4b']['pass_'] else 'FAIL'}")
    allp = all(v["pass_"] for v in K.values())
    P(f"\nK overall: {'ALL PASS' if allp else 'FAILURES PRESENT'}  ({time.time() - T0:.0f} s; peak RSS {rss_gb():.2f} GB)")
    json.dump(dict(lane="CFG924", criteria="4f4def674", mode="K", sources=SOURCES, K=K, all_pass=allp),
              open(os.path.join(HERE, "cfg924_K.json"), "w"), indent=1, default=float)
    sys.exit(0 if allp else 1)

# =====================================================================================================================
if MODE == "MUTATE":
    RES = dict(lane="CFG924", criteria="4f4def674", mode="MUTATE", sources=SOURCES)
    B0 = load_bright(""); Bp = apply_flux(B0, np.full(len(B0["mmed"]), -0.5), cap=1.0)         # planted x10^0.2, masked / footprint off
    Mc, Mb = census_652(Bp, I652["ra"], I652["dec"], I652["z"], I652["R500_arcmin"]); del B0, Bp
    s = I652["Mcond"] > 0
    rc = float(np.max(np.abs(Mc[s] / (10 ** 0.2 * I652["Mcond"][s]) - 1))); sb = I652["Mbcg"] > 0
    rb = float(np.max(np.abs(Mb[sb] / (10 ** 0.2 * I652["Mbcg"][sb]) - 1)))
    zero_ok = bool(np.all(Mc[~s] == 0) and np.all(Mb[~sb] == 0))
    P(f"M-INJ census: planted fluxscale -0.5 mag -> M_cond / (10^0.2 F) max rel {rc:.1e} (N {s.sum()}), M_bcg {rb:.1e} (N {sb.sum()}); zeros stay zero {zero_ok}")
    w = os.path.join(WORK, "INJ"); write_inputs(w, Mc, Mb); models_x1(w, "M-INJ")
    res, txt = score652(w); inj = {}
    for foot in FEET:
        a, b = res["verdicts"][foot]["x1"], ST[""]["verdicts"][foot]["p02"]
        inj[foot] = dict(chi2_a=a["a"]["chi2"], chi2_a_stored_p02=b["a"]["chi2"], chi2_b=a["b"]["chi2"], chi2_b_stored_p02=b["b"]["chi2"],
                         label=a["label"], label_stored_p02=b["label"],
                         ok=bool(abs(a["a"]["chi2"] - b["a"]["chi2"]) < 1e-6 and abs(a["b"]["chi2"] - b["b"]["chi2"]) < 1e-6 and a["label"] == b["label"]))
        P(f"M-INJ [{foot[:3]}] planted x1: chi2_a {a['a']['chi2']:.6f} (stored p02 {b['a']['chi2']:.6f}), chi2_b {a['b']['chi2']:.6f} "
          f"(stored p02 {b['b']['chi2']:.6f}), label {a['label']} (stored {b['label']}) -> {'PASS' if inj[foot]['ok'] else 'FAIL'}")
    ok = bool(rc < 1e-9 and rb < 1e-9 and zero_ok and all(v["ok"] for v in inj.values()))
    RES["M_INJ"] = dict(census_maxrel_Mcond=rc, census_maxrel_Mbcg=rb, zeros_stay_zero=zero_ok, score=inj, pass_=ok, N_groups=res["N_groups"])
    P(f"\nM-INJ overall: {'BITES (planted +0.2 dex reproduces CFG652 p02 end to end)' if ok else 'FAIL'}  ({time.time() - T0:.0f} s; peak RSS {rss_gb():.2f} GB)")
    P("\n---- verbatim CFG652 score printout on the planted masses ----\n" + txt)
    json.dump(RES, open(os.path.join(HERE, "cfg924_results_MUTATE.json"), "w"), indent=1, default=float)
    sys.exit(0 if ok else 1)

# =====================================================================================================================
def p02_check(res, label):
    out = {}
    for foot in FEET:
        a, b = res["verdicts"][foot]["x1"], ST[""]["verdicts"][foot]["p02"]
        out[foot] = dict(chi2_a=a["a"]["chi2"], chi2_a_stored_p02=b["a"]["chi2"], chi2_b=a["b"]["chi2"], chi2_b_stored_p02=b["b"]["chi2"],
                         label=a["label"], label_stored_p02=b["label"],
                         ok=bool(abs(a["a"]["chi2"] - b["a"]["chi2"]) < 1e-6 and abs(a["b"]["chi2"] - b["b"]["chi2"]) < 1e-6 and a["label"] == b["label"]))
        P(f"{label} [{foot[:3]}] planted x1: chi2_a {a['a']['chi2']:.6f} (stored p02 {b['a']['chi2']:.6f}), chi2_b {a['b']['chi2']:.6f} "
          f"(stored p02 {b['b']['chi2']:.6f}), label {a['label']} (stored {b['label']}) -> {'PASS' if out[foot]['ok'] else 'FAIL'}")
    return out


if MODE == "MUTATE_B":
    # AM1 M-INJb: the exact float operation CFG652 used for its p02 inputs; tests the CFG924 wiring end to end
    RES = dict(lane="CFG924", criteria="4f4def674", amendment="AM1 (post hoc)", mode="MUTATE_B", sources=SOURCES)
    Mc = I652["Mcond"] * 10 ** 0.2; Mb = I652["Mbcg"] * 10 ** 0.2
    w = os.path.join(WORK, "INJB"); write_inputs(w, Mc, Mb); models_x1(w, "M-INJb")
    MD, MJ = np.load(os.path.join(W652, "cfg652_models.npz")), np.load(os.path.join(w, "cfg652_models.npz")); k = I652["Mcond"] > 0
    arr_rel = max(float(np.nanmax(np.abs(MJ[f"{f}__x1__{m}"][k] / MD[f"{f}__p02__{m}"][k] - 1))) for f in FEET for m in "ab")
    P(f"M-INJb per-group arrays vs stored p02 arrays (131 groups, both footings, both models): max rel {arr_rel:.1e}")
    res, txt = score652(w); inj = p02_check(res, "M-INJb")
    ok = bool(arr_rel < 1e-9 and all(v["ok"] for v in inj.values()))
    RES["M_INJb"] = dict(array_maxrel=arr_rel, score=inj, pass_=ok, N_groups=res["N_groups"])
    P(f"\nM-INJb overall: {'PASS (wiring exact)' if ok else 'FAIL'}  ({time.time() - T0:.0f} s; peak RSS {rss_gb():.2f} GB)")
    P("\n---- verbatim CFG652 score printout on the M-INJb masses ----\n" + txt)
    json.dump(RES, open(os.path.join(HERE, "cfg924_results_MUTATE_B.json"), "w"), indent=1, default=float)
    sys.exit(0 if ok else 1)

if MODE == "JITTER":
    # AM1 model-noise ensemble: model (a) with M_cond x (1 + k 1e-12), k = 1..4; model (b) unjittered; x1 cell, both footings
    RES = dict(lane="CFG924", criteria="4f4def674", amendment="AM1 (post hoc)", mode="JITTER", sources=SOURCES)
    R924 = json.load(open(os.path.join(HERE, "cfg924_results.json")))
    BASE = {"F": (W652, ST[""]), "A1c": (os.path.join(WORK, "A1c"), R924["scores"]["A1c"])}
    J = {}
    for nm, (bw, bres) in BASE.items():
        I = np.load(os.path.join(bw, "cfg652_inputs.npz")); MDb = np.load(os.path.join(bw, "cfg652_models.npz")); n = len(I["z"])
        J[nm] = {f: dict(chi2_a=[], chi2_b=[], labels=[], A_out_a=[], base_chi2_a=bres["verdicts"][f]["x1"]["a"]["chi2"],
                         base_label=bres["verdicts"][f]["x1"]["label"]) for f in FEET}
        for k in range(1, 5):
            Mc = I["Mcond"] * (1 + k * 1e-12); w = os.path.join(WORK, f"JIT_{nm}_{k}"); write_inputs(w, Mc, I["Mbcg"]); out = {}
            for foot in FEET:
                arr = np.full((n, len(NS_RC)), np.nan)
                for i in range(n):
                    if Mc[i] > 0:
                        arr[i] = model_row(Mc[i], I["Mhot"][i], I["Rx_kpc"][i], I["z"][i], foot, "a")
                for vk in VK:
                    out[f"{foot}__{vk}__a"] = arr; out[f"{foot}__{vk}__b"] = MDb[f"{foot}__x1__b"]
            np.savez(os.path.join(w, "cfg652_models.npz"), **out)
            res, _ = score652(w)
            for foot in FEET:
                c = res["verdicts"][foot]["x1"]; J[nm][foot]["chi2_a"].append(c["a"]["chi2"]); J[nm][foot]["chi2_b"].append(c["b"]["chi2"])
                J[nm][foot]["labels"].append(c["label"]); J[nm][foot]["A_out_a"].append(c["a"]["A_out"])
            P(f"  [JITTER {nm} k={k}] " + "; ".join(f"{f[:3]} chi2_a {J[nm][f]['chi2_a'][-1]:.3f} chi2_b {J[nm][f]['chi2_b'][-1]:.3f} {J[nm][f]['labels'][-1]}"
                                                  for f in FEET) + f" ({time.time() - T0:.0f} s)")
        for foot in FEET:
            d = J[nm][foot]; ca = np.array(d["chi2_a"])
            d.update(mean=float(ca.mean()), sd=float(ca.std(ddof=1)), lo=float(ca.min()), hi=float(ca.max()),
                     label_changes=int(sum(l != d["base_label"] for l in d["labels"])))
            P(f"JITTER {nm} [{foot[:3]}]: chi2_a unjittered {d['base_chi2_a']:.3f}; jitter mean {d['mean']:.3f} sd {d['sd']:.3f} range {d['lo']:.3f}-{d['hi']:.3f};"
              f" labels {sorted(set(d['labels']))} (changes vs unjittered {d['label_changes']}/4)")
    sens = any(J[nm][f]["label_changes"] > 0 for nm in J for f in FEET)
    qual = {}
    for key, c in R924["cells"].items():
        foot = key.split("|")[0]; sdm = max(J["F"][foot]["sd"], J["A1c"][foot]["sd"]); dca = c["chi2_a"][1] - c["chi2_a"][0]
        qual[key] = dict(status=c["status"], dchi2_a=dca, noise_2sd=2 * sdm,
                         flag=("WITHIN MODEL NOISE" if (c["status"] == "MOVES" and abs(dca) < 2 * sdm) else ""))
    V = R924["verdict"] + ("; NOISE-SENSITIVE" if sens else "") + ("; a cell move WITHIN MODEL NOISE" if any(q["flag"] for q in qual.values()) else "")
    P("\n  cell dchi2_a (A1c - F) vs 2 x jitter sd: " + "; ".join(f"{k} {q['dchi2_a']:+.2f} (2sd {q['noise_2sd']:.2f}){' ' + q['flag'] if q['flag'] else ''}"
                                                        for k, q in qual.items()))
    P(f"\n  CFG924 VERDICT with AM1 noise qualification: {V}  ({time.time() - T0:.0f} s; peak RSS {rss_gb():.2f} GB)")
    RES.update(jitter=J, noise_sensitive=sens, cells=qual, verdict_qualified=V)
    json.dump(RES, open(os.path.join(HERE, "cfg924_results_JITTER.json"), "w"), indent=1, default=float)
    sys.exit(0)

# =====================================================================================================================
# MAIN: A1c (primary), A1u (bracket), same-sample, POSTHOC; MUTATE M1 on A1c
RES = dict(lane="CFG924", criteria="4f4def674", mode="MAIN", sources=SOURCES)
B0 = load_bright(""); B1 = load_bright("A1")
McF, MbF = census_652(B0, I652["ra"], I652["dec"], I652["z"], I652["R500_arcmin"])
assert np.array_equal(McF, I652["Mcond"]) or float(np.max(np.abs(McF - I652["Mcond"]) / np.maximum(I652["Mcond"], 1))) < 1e-9
Bchk = apply_flux(B0, B1["fluxscale"], cap=1.0); idm = float(np.max(np.abs(Bchk["mmed"] - B1["mmed"]))); del Bchk
P(f"  A1 identity: CFG922 load_bright(A1) MASS_MED vs the A1 correction line on the unamended column: max abs {idm:.1e} dex")
cov, nap, nann = coverage(B0)
Mc1, Mb1 = census_652(B1, I652["ra"], I652["dec"], I652["z"], I652["R500_arcmin"])
B1u = apply_flux(B0, B1["fluxscale"], cap=None); B1u["masked"] = np.zeros_like(B1u["masked"])
Mcu, Mbu = census_652(B1u, I652["ra"], I652["dec"], I652["z"], I652["R500_arcmin"])
fsg = B1["fluxscale"][B1["ok"]]; del B0, B1, B1u
McC, MbC, fpC = footprint(Mc1, Mb1, cov, upper=False); McU, MbU, fpU = footprint(Mcu, Mbu, cov, upper=True)
P(f"  census done ({time.time() - T0:.0f} s); coverage quartiles {np.percentile(cov, [0, 25, 50, 75]).round(2).tolist()}; footprint A1c {fpC}; A1u {fpU}")
nF, nC, nU = int((McF > 0).sum()), int((McC > 0).sum()), int((McU > 0).sum())
enter = np.where((McF <= 0) & (McC > 0))[0].tolist(); leave = np.where((McF > 0) & (McC <= 0))[0].tolist()
BR = dict(A1c=bracket_stats(McC, McF), A1u=bracket_stats(McU, McF), A1c_before_footprint=bracket_stats(Mc1, McF))
P(f"  M_cond > 0: F {nF}, A1c {nC}, A1u {nU}; entering A1c {len(enter)}, leaving {len(leave)}")
for k, b in BR.items():
    P(f"  [BRACKET {k}] dlog10 M_cond vs F: median {b['median']:+.3f} (16-84% {b['p16']:+.3f} / {b['p84']:+.3f}), frac > 0.2 {b['frac_gt_0p2']:.2f}, "
      f"frac < 0 {b['frac_lt_0']:.2f}, N {b['n']} -> {b['cls']}")
P(f"  medians: M_cond F {np.median(McF[McF > 0]):.3e}, A1c {np.median(McC[McC > 0]):.3e}, A1u {np.median(McU[McU > 0]):.3e}; "
  f"M_bcg > 0: F {(MbF > 0).sum()}, A1c {(MbC > 0).sum()}, A1u {(MbU > 0).sum()}")
CENSUS = dict(groups=[dict(eid=float(I652["eid"][i]), z=float(I652["z"][i]), Mhot=float(I652["Mhot"][i]), Mc_F=float(McF[i]), Mb_F=float(MbF[i]),
                           Mc_A1c_prefoot=float(Mc1[i]), Mc_A1c=float(McC[i]), Mb_A1c=float(MbC[i]), Mc_A1u_prefoot=float(Mcu[i]), Mc_A1u=float(McU[i]),
                           Mb_A1u=float(MbU[i]), coverage=float(cov[i]), n_ap=int(nap[i]), n_ann=int(nann[i]),
                           status="not measured" if cov[i] < 0.5 else ("partial" if cov[i] < 1 else "measured")) for i in range(len(cov))],
              footprint=dict(A1c=fpC, A1u=fpU), n_pos=dict(F=nF, A1c=nC, A1u=nU), entering=enter, leaving=leave, brackets=BR,
              fluxscale_bright_ok=dict(median=float(np.median(fsg)), p16=float(np.percentile(fsg, 16)), p84=float(np.percentile(fsg, 84))),
              a1_identity_maxabs_dex=idm)
json.dump(CENSUS, open(os.path.join(HERE, "cfg924_census.json"), "w"), indent=1)
P(f"  wrote cfg924_census.json (peak RSS so far {rss_gb():.2f} GB)")
wC, wU, wS = (os.path.join(WORK, k) for k in ("A1c", "A1u", "SAME"))
write_inputs(wC, McC, MbC); write_inputs(wU, McU, MbU)
same = (McF > 0) & (McC > 0); write_inputs(wS, np.where(same, McC, 0.0), np.where(same, MbC, 0.0))
P(f"\n  models: A1c (CFG652 models block verbatim, {nC} groups x 22) ...")
models652(wC); shutil.copyfile(os.path.join(wC, "cfg652_models.npz"), os.path.join(wS, "cfg652_models.npz"))
P(f"  models: A1u (x1 only, {nU} groups x 4) ...")
models_x1(wU, "A1u")
# ---- scores (MUTATE M1 first) ----
SC = {}
SC["A1c_MUTATE"], txtM = score652(wC, mut=True)
m1 = SC["A1c_MUTATE"]["M1"]; m1ok = all(v["ok"] for v in m1.values())
P("\n[MUTATE M1 on A1c] " + "; ".join(f"{f[:3]} chi2 (a, relabelled) {m1[f]['chi2_relabelled_a']:.3f} vs (b) {m1[f]['chi2_b']:.3f} -> {'PASS' if m1[f]['ok'] else 'FAIL'}" for f in FEET))
SC["A1c"], txtC = score652(wC); SC["A1c_POSTHOC"], txtP = score652(wC, posthoc=True)
SC["A1u"], txtU = score652(wU); SC["SAME"], txtS = score652(wS)
# ---- CFG924 classification ----
S0 = ST[""]; cells = {}
P("\n==== CFG924 cell level (A1c vs CFG652 stored) ====")
for foot in FEET:
    for vk in VK:
        o, n_ = S0["verdicts"][foot][vk], SC["A1c"]["verdicts"][foot][vk]
        cells[f"{foot}|{vk}"] = dict(old=o["label"], new=n_["label"], status="HOLDS" if o["label"] == n_["label"] else "MOVES",
                                     chi2_a=(o["a"]["chi2"], n_["a"]["chi2"]), chi2_b=(o["b"]["chi2"], n_["b"]["chi2"]),
                                     A_out_a=(o["a"]["A_out"], n_["a"]["A_out"]), A_out_b=(o["b"]["A_out"], n_["b"]["A_out"]),
                                     sA=(n_["a"]["sA"], n_["b"]["sA"]), dchi2_b_minus_a=(o["dchi2_b_minus_a"], n_["dchi2_b_minus_a"]),
                                     p=(n_["a"]["p"], n_["b"]["p"]))
        c = cells[f"{foot}|{vk}"]
        P(f"  [{foot[:3]}] {vk:4s}: chi2_a {c['chi2_a'][0]:5.1f} -> {c['chi2_a'][1]:5.1f} (p {c['p'][0]:.3g}); chi2_b {c['chi2_b'][0]:5.1f} -> {c['chi2_b'][1]:5.1f} "
          f"(p {c['p'][1]:.3g}); dchi2(b-a) {c['dchi2_b_minus_a'][0]:+5.1f} -> {c['dchi2_b_minus_a'][1]:+5.1f}; A_out a {c['A_out_a'][0]:+.3f} -> {c['A_out_a'][1]:+.3f} "
          f"+- {c['sA'][0]:.3f}, b {c['A_out_b'][0]:+.3f} -> {c['A_out_b'][1]:+.3f} +- {c['sA'][1]:.3f}; {c['old']} -> {c['new']}: {c['status']}")
fin_old, fin_new = S0["final"], SC["A1c"]["final"]
u_lab = {f: SC["A1u"]["verdicts"][f]["x1"]["label"] for f in FEET}
u_ok = all(u_lab[f] == S0["verdicts"][f]["x1"]["label"] for f in FEET)
if fin_new != fin_old:
    VERDICT = f"CFG652 VERDICT MOVES ({fin_old} -> {fin_new})"
elif not u_ok:
    VERDICT = "HOLDS AT CENTRAL, MOVES AT UPPER (BRACKET-DEPENDENT)"
else:
    VERDICT = "CFG652 VERDICT HOLDS"
n_moves = sum(c["status"] == "MOVES" for c in cells.values())
P(f"\n  A1u (x1 only; FRAGILE not evaluated): " + "; ".join(
    f"{f[:3]} chi2_a {SC['A1u']['verdicts'][f]['x1']['a']['chi2']:.1f} chi2_b {SC['A1u']['verdicts'][f]['x1']['b']['chi2']:.1f} "
    f"A_out a {SC['A1u']['verdicts'][f]['x1']['a']['A_out']:+.3f} b {SC['A1u']['verdicts'][f]['x1']['b']['A_out']:+.3f} -> {u_lab[f]}" for f in FEET))
for nm in ("SAME", "A1c_POSTHOC"):
    r = SC[nm]
    P(f"  [{nm}, no verdict weight] N {r['N_groups']}: " + "; ".join(
        f"{f[:3]} chi2_a {r['verdicts'][f]['x1']['a']['chi2']:.1f} chi2_b {r['verdicts'][f]['x1']['b']['chi2']:.1f} dchi2 {r['verdicts'][f]['x1']['dchi2_b_minus_a']:+.1f}"
        f" -> {r['verdicts'][f]['x1']['label']}" for f in FEET) + f"; final '{r['final']}'")
sp, sp0 = SC["A1c"]["split"], S0["split"]
P(f"  [split, no weight] D_obs {sp['Dobs']:+.3f} +- {sp['sD']:.3f} (CFG652 {sp0['Dobs']:+.3f}); pred (a) {sp['Dpred_canonical_a']:+.3f}/{sp['Dpred_alt_a']:+.3f}, "
  f"(b) {sp['Dpred_canonical_b']:+.3f}/{sp['Dpred_alt_b']:+.3f}; M2 shuffle median {sp['M2_shuffle_median']:+.3f} (killed {sp['M2_trend_killed']})")
P(f"\n  CFG652 stored final: '{fin_old}' (N {S0['N_groups']}); A1c final: '{fin_new}' (N {SC['A1c']['N_groups']}); cells moved {n_moves}/10; "
  f"MUTATE M1 {'PASS' if m1ok else 'FAIL'}")
P(f"  BRACKET: A1c {BR['A1c']['cls']} (median {BR['A1c']['median']:+.3f} dex); A1u {BR['A1u']['cls']} (median {BR['A1u']['median']:+.3f} dex)")
P(f"\n  CFG924 VERDICT: {VERDICT}")
P(f"  ({time.time() - T0:.0f} s; peak RSS {rss_gb():.2f} GB)")
for nm, txt in (("A1c (primary)", txtC), ("A1c MUTATE (M1)", txtM), ("A1c POSTHOC (no weight)", txtP), ("A1u x1 bracket", txtU), ("SAME sample (no weight)", txtS)):
    P(f"\n---- verbatim CFG652 score printout: {nm} ----\n" + txt.rstrip())
RES.update(verdict=VERDICT, cells=cells, n_cells_moved=n_moves, final_old=fin_old, final_new=fin_new, A1u_x1_labels=u_lab, M1_pass=m1ok,
           brackets=BR, n_pos=dict(F=nF, A1c=nC, A1u=nU), entering=enter, leaving=leave, footprint=dict(A1c=fpC, A1u=fpU), scores=SC,
           peak_rss_gb=rss_gb())
json.dump(RES, open(os.path.join(HERE, "cfg924_results.json"), "w"), indent=1, default=float)
