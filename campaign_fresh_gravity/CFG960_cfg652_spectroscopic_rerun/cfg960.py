"""CFG960 (criteria 12896a21d): CFG652's hot-group lensing test with a spectroscopic total-mass census (GAMA G3C v10 members +
GAMA DR4 GKV total-flux stellar masses, G09).

Modes (one process at a time, OMP_NUM_THREADS=1, nice 10; run from this directory):
  CFG960_MODE=K       python3 cfg960.py  -> cfg960_K.out, cfg960_K.json                       (K1-K5)
                      python3 cfg960.py  -> cfg960.out, cfg960_results.json, cfg960_census.json (census, M-PLANT, M-NULL, primary,
                                                                                               V1-V5, F-on-S, S-on-F, M1)
  CFG960_MODE=INJ     python3 cfg960.py  -> cfg960_INJ.out, cfg960_results_INJ.json           (M-INJ, fresh model calls)
  CFG960_MODE=JITTER  python3 cfg960.py  -> cfg960_JITTER.out, cfg960_results_JITTER.json     (model-(a) noise; final qualified label)
Reuse (read-only, by exec of text slices of committed sources; nothing of theirs is imported or written): CFG652 cfg652_test.py
preamble + models block + score block verbatim (WORK and the output directory redirected), CFG922 read_cols / load_bright /
mlim_table / Census (comp), cfg652_model (imported). Work files: _external_data/cfg960_work. Nothing downloaded.
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
os.environ.pop("MUTATE", None); os.environ.pop("POSTHOC", None)
import io, re, csv, json, math, time, shutil, hashlib, tempfile, contextlib, subprocess, resource, warnings
import numpy as np
from scipy.spatial import cKDTree
from scipy.special import erfc
warnings.filterwarnings("ignore", category=RuntimeWarning)
try:
    os.nice(10)
except OSError:
    pass

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
C652 = os.path.join(LANES, "CFG652_hot_group_discriminator"); C922 = os.path.join(LANES, "CFG922_cluster_core_baryon_recheck")
C471 = os.path.join(LANES, "CFG471_kids_split_gama_groups"); C924 = os.path.join(LANES, "CFG924_cfg652_total_flux_rerun")


def _main_checkout():
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
G3CD = next(os.path.join(r, "campaign_fresh_gravity", "_external_data", "cfg471") for r in (REPO, MAINCO)
            if os.path.exists(os.path.join(r, "campaign_fresh_gravity", "_external_data", "cfg471", "G3CGalv10.csv")))
GKVD = os.path.join(EXT, "gama_dr4_gkv")
W652 = os.path.join(EXT, "cfg652_work"); WORK = os.path.join(EXT, "cfg960_work")
MODE = os.environ.get("CFG960_MODE", "MAIN")
TAG = {"K": "_K", "INJ": "_INJ", "JITTER": "_JITTER"}.get(MODE, "")
OUT = open(os.path.join(HERE, "cfg960" + TAG + ".out"), "w")
T0 = time.time()
FEET = ("canonical", "alt"); VK = ("x1", "p02", "m02", "g1", "g4")
VAR = (("x1", 1.0, 2.0), ("p02", 10 ** 0.2, 2.0), ("m02", 10 ** -0.2, 2.0), ("g1", 1.0, 1.0), ("g4", 1.0, 4.0))   # CFG652 models block
SHA_MODEL = "04352d4eec05b2825fd6d89842599f9e0b8149f4e5ea6ac36e404857e80d60d1"
CKMS = 299792.458
G09 = (129.0, 141.0, -2.0, 3.0); BOX652 = (122.0, 150.0, -7.0, 9.0)
W_PRIMARY = 2000.0; W_ANCHOR = 1500.0


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()


def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()


def rss_gb(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)


def cut(txt, a, b):
    assert txt.count(a) == 1, a
    i = txt.index(a); return txt[i:txt.index(b, i)]


# ---- CFG922 slices (bright-sample reader, completeness form) ----
T922 = open(os.path.join(C922, "cfg922.py")).read()
NS922 = dict(os=os, np=np, math=math, cKDTree=cKDTree, erfc=erfc, AMEND="", DATA=DATA, RAP=0.5, __name__="cfg922_slices")
exec(cut(T922, "def read_cols(", "def mlim_table("), NS922)
exec(cut(T922, "def mlim_table(", "def census_652("), NS922)                # mlim_table + Census (comp used via __new__)


def comp_factory(zg, ml):
    """CFG922's Census.comp bound to a given M_lim(z) table (no __init__, so no catalogue tree)."""
    obj = NS922["Census"].__new__(NS922["Census"]); obj.zg, obj.ml = np.asarray(zg, float), np.asarray(ml, float)
    return obj.comp


# ---- CFG652 test: preamble, models block and score block, verbatim ----
F652 = os.path.join(C652, "cfg652_test.py"); T652 = open(F652).read()
MARK_IN = "# ============================================================================================== inputs"
assert T652.count(MARK_IN) == 1
PRE652 = T652.split(MARK_IN)[0]
assert "if MODE ==" not in PRE652 and "json.dump" not in PRE652
os.environ["CFG652_MODE"] = "none"
WLINE = 'WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg652_work"))'
assert PRE652.count(WLINE) == 1
PRE652 = PRE652.replace(WLINE, "WORK = _WORK_OVERRIDE")
MODELS652 = cut(T652, 'if MODE == "models":', "# ============================================================================================== score")
SCORE652 = T652[T652.index('if MODE == "score":'):]
assert MODELS652.count("if MODE ==") == 1 and SCORE652.count("if MODE ==") == 1 and "np.savez" not in SCORE652
sys.path.insert(0, C652)
import cfg652_model as M                                                   # noqa: E402
assert os.path.dirname(os.path.abspath(M.__file__)) == C652
SOURCES = {k: sha(p) for k, p in (("cfg652_test.py", F652), ("cfg652_model.py", os.path.join(C652, "cfg652_model.py")),
                                  ("cfg922.py", os.path.join(C922, "cfg922.py")))}


def ns652(work):
    NS = {"__file__": F652, "__name__": "cfg652_reuse", "_WORK_OVERRIDE": work}
    exec(compile(PRE652, F652, "exec"), NS)
    NS.setdefault("__doc__", T652.split('"""')[1])
    return NS


def score652(work, mut=False, posthoc=False):
    NS = ns652(work); NS["MODE"] = "score"; NS["MUT"] = mut; tmp = tempfile.mkdtemp(prefix="cfg960_score_"); NS["HERE"] = tmp
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
    NS = ns652(work); NS["MODE"] = "models"
    assert os.path.abspath(NS["WORK"]) == os.path.abspath(work) and os.path.abspath(work) != os.path.abspath(W652)
    exec(compile(MODELS652, F652, "exec"), NS)


NS_RC = ns652(W652)["RC"]


def model_row(Mc, Mh, Rx, z, foot, model, fac=1.0, gt=2.0, m1=False):
    """the identical calls of CFG652's models block for one group."""
    if m1:
        o = M.system(Mc, Mh, Rx, z, foot, "a", N=600, hot_as_condensed=True)
    else:
        o = M.system(Mc * fac, Mh, Rx, z, foot, model, N=600, gas_trunc=gt)
    return M.delta_sigma(o["rg"], o["Mbound"], NS_RC, rmax=o["rta"])


I652 = np.load(os.path.join(W652, "cfg652_inputs.npz")); NG = len(I652["z"])
ST = {t: json.load(open(os.path.join(C652, f"cfg652_test_results{t}.json"))) for t in ("", "_MUTATE", "_POSTHOC")}


def write_inputs(work, Mc, Mb, models_from=None):
    os.makedirs(work, exist_ok=True)
    d = {k: I652[k] for k in I652.files}
    Mc = np.asarray(Mc, float); Mb = np.asarray(Mb, float)
    d["Mcond"] = Mc; d["Mbcg"] = Mb; d["fhot"] = d["Mhot"] / (d["Mhot"] + Mc)
    np.savez(os.path.join(work, "cfg652_inputs.npz"), **d)
    shutil.copyfile(os.path.join(W652, "cfg652_esd.npz"), os.path.join(work, "cfg652_esd.npz"))
    if models_from:
        shutil.copyfile(models_from, os.path.join(work, "cfg652_models.npz"))


CACHE = {}


def cache_from_npz(Mc, path):
    MD = np.load(path)
    for i in np.where(Mc > 0)[0]:
        for foot in FEET:
            for vk, fac, gt in VAR:
                for model in "ab":
                    CACHE[(i, foot, model, float(Mc[i] * fac), gt)] = MD[f"{foot}__{vk}__{model}"][i]


def models_x1(work, label, use_cache=True):
    """x1 only (both footings, both models); p02/m02/g1/g4 entries are copies of x1 (declared). Cached by exact inputs."""
    I = np.load(os.path.join(work, "cfg652_inputs.npz")); n = len(I["z"]); out = {}; hits = 0; calls = 0
    for foot in FEET:
        for model in "ab":
            arr = np.full((n, len(NS_RC)), np.nan)
            for i in range(n):
                if I["Mcond"][i] > 0:
                    key = (i, foot, model, float(I["Mcond"][i] * 1.0), 2.0)
                    if use_cache and key in CACHE:
                        arr[i] = CACHE[key]; hits += 1
                    else:
                        arr[i] = model_row(I["Mcond"][i], I["Mhot"][i], I["Rx_kpc"][i], I["z"][i], foot, model); calls += 1
                        if use_cache:
                            CACHE[key] = arr[i].copy()
            for vk in VK:
                out[f"{foot}__{vk}__{model}"] = arr
    np.savez(os.path.join(work, "cfg652_models.npz"), **out)
    P(f"  [{label}] x1 models: {calls} model calls, {hits} cache hits ({time.time() - T0:.0f} s)")


def compare(a, b, path="", acc=None):
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


# =====================================================================================================================
# census engine (CFG652's aperture / annulus / floor structure; galaxy list, redshift window and footprint are arguments)
class Gal:
    def __init__(self, ra, dec, z, m, extra=None):
        self.ra, self.dec, self.z, self.m = (np.asarray(v, float) for v in (ra, dec, z, m))
        self.tree = cKDTree(np.c_[self.ra * np.cos(np.radians(self.dec)), self.dec]); self.extra = extra or {}


def ann_fraction(ra0, de0, th, box, nr=200, na=720):
    """in-box fraction of the 3-6 th annulus on a fixed polar grid (area-weighted), planar metric."""
    r = 3 * th + (np.arange(nr) + 0.5) / nr * 3 * th; a = (np.arange(na) + 0.5) / na * 2 * math.pi
    R, A = np.meshgrid(r, a, indexing="ij"); dd = R * np.sin(A); dra = R * np.cos(A) / math.cos(math.radians(de0))
    ins = (ra0 + dra > box[0]) & (ra0 + dra < box[1]) & (de0 + dd > box[2]) & (de0 + dd < box[3])
    return float((ins * R).sum() / R.sum())


def aperture_inside(ra0, de0, th, box):
    c = math.cos(math.radians(de0))
    return (ra0 - th / c > box[0]) and (ra0 + th / c < box[1]) and (de0 - th > box[2]) and (de0 + th < box[3])


def vwin(zg, zc, W):
    return np.abs(CKMS * (zg - zc) / (1 + zc)) <= W


def anchor(G, ra0, de0, th, zeF):
    p = [ra0 * math.cos(math.radians(de0)), de0]
    k = np.array(G.tree.query_ball_point(p, 0.5 * th), int)
    if k.size:
        k = k[np.abs(G.z[k] - zeF) <= 0.05 * (1 + zeF)]
    if k.size == 0:
        return np.nan, 0
    zz, mm = G.z[k], G.m[k]
    dv = np.abs(CKMS * (zz[None, :] - zz[:, None]) / (1 + zz[:, None])) <= W_ANCHOR
    cnt = dv.sum(1); msum = (dv * mm[None, :]).sum(1)
    order = np.lexsort((-msum, -cnt)); j = order[0]
    return float(np.median(zz[dv[j]])), int(k.size)


def census(G, zc, win, box_ann, box_in=None, plant=None, idx=None, pos=None):
    """raw census terms per group. win(zg, zc_i) -> mask. pos = (ra, dec, R500_arcmin) arrays (default: the 148 eFEDS groups).
    plant = mass of a galaxy injected into the catalogue at each group centre at zc (M-PLANT; one group at a time)."""
    ra, de, rx = pos if pos is not None else (I652["ra"], I652["dec"], I652["R500_arcmin"])
    n = len(ra); idx = range(n) if idx is None else idx
    out = {k: np.zeros(n) for k in ("net", "bcg", "f_ann", "n_ap", "inside", "sum_ap", "sum_ann")}
    for i in idx:
        if not np.isfinite(zc[i]):
            continue
        th = rx[i] / 60.0; p = [ra[i] * math.cos(math.radians(de[i])), de[i]]
        out["inside"][i] = 1.0 if (box_in is None or aperture_inside(ra[i], de[i], th, box_in)) else 0.0
        if box_in is not None and not out["inside"][i]:
            continue
        if plant is not None:
            Gp = Gal(np.r_[G.ra, ra[i]], np.r_[G.dec, de[i]], np.r_[G.z, zc[i]], np.r_[G.m, plant])
        else:
            Gp = G
        zw = win(Gp.z, zc[i])
        kin = np.array(Gp.tree.query_ball_point(p, th), int); kin = kin[zw[kin]]
        kout = np.array(Gp.tree.query_ball_point(p, 6 * th), int); kout = kout[zw[kout]]
        k3 = np.array(Gp.tree.query_ball_point(p, 3 * th), int); k3 = k3[zw[k3]]
        ann = np.setdiff1d(kout, k3)
        fa = ann_fraction(ra[i], de[i], th, box_ann); out["f_ann"][i] = fa
        bkg = Gp.m[ann].sum() * ((1.0 / (36 - 9)) / fa) if fa > 0 else 0.0
        out["sum_ap"][i] = Gp.m[kin].sum(); out["sum_ann"][i] = Gp.m[ann].sum()
        out["net"][i] = Gp.m[kin].sum() - bkg
        inner = np.array(Gp.tree.query_ball_point(p, 0.2 * th), int); inner = inner[zw[inner]]
        out["bcg"][i] = Gp.m[inner].max() if len(inner) else 0.0
        out["n_ap"][i] = len(kin)
    return out


def assemble(raw, c):
    """M_cond = bcg + c * max(net - bcg, 0) (c = 1: CFG652's max(net, bcg)); M_bcg = bcg."""
    Mc = raw["bcg"] + c * np.maximum(raw["net"] - raw["bcg"], 0.0)
    return np.where(Mc > 0, Mc, 0.0), raw["bcg"].copy()


def mlim(z, logm, mag, lo, hi):
    """CFG922 mlim_table's algorithm with a declared magnitude band."""
    zg = np.round(np.arange(0.03, 0.56, 0.01), 3); s = (mag >= lo) & (mag <= hi) & (logm > 5) & np.isfinite(z)
    zz, mm = z[s], logm[s]; ml = []
    for z0 in zg:
        k = np.abs(zz - z0) <= 0.02; ml.append(float(np.median(mm[k])) if k.sum() >= 20 else np.nan)
    ml = np.array(ml); good = np.isfinite(ml)
    return zg[good], ml[good]


def load_gama():
    """G3CGalv10 x GKV on CATAID (logM* > 5); G3C Z and Rpetro; plus the G3C FoF group table."""
    gk = {}
    for r in csv.DictReader(open(os.path.join(GKVD, "gkv_stellarmass_g09.csv"))):
        try:
            lm = float(r["logmstar"])
        except ValueError:
            continue
        if np.isfinite(lm) and lm > 5:
            gk[int(r["CATAID"])] = lm
    rows = []
    for r in csv.DictReader(open(os.path.join(G3CD, "G3CGalv10.csv"))):
        c = int(r["CATAID"])
        if c in gk:
            rows.append((c, float(r["RA"]), float(r["Dec"]), float(r["Z"]), float(r["Rpetro"]), int(r["GroupID"]), gk[c]))
    A = np.array(rows)
    gal = dict(cataid=A[:, 0].astype(int), ra=A[:, 1], dec=A[:, 2], z=A[:, 3], rpetro=A[:, 4], gid=A[:, 5].astype(int), logm=A[:, 6])
    grp = []
    for r in csv.DictReader(open(os.path.join(G3CD, "G3CFoFGroupv10.csv"))):
        grp.append((int(r["GroupID"]), int(r["Nfof"]), float(r["IterCenRA"]), float(r["IterCenDec"]), float(r["Zfof"])))
    Gt = np.array(grp)
    return gal, dict(gid=Gt[:, 0].astype(int), nfof=Gt[:, 1].astype(int), ra=Gt[:, 2], dec=Gt[:, 3], z=Gt[:, 4]), len(gk)


def fetch_sha(logfile, fname):
    for l in open(logfile):
        if fname in l:
            m = re.findall(r"\b[0-9a-f]{64}\b", l)
            if m:
                return m[-1]
    return None


def bstats(new, old):
    s = (new > 0) & (old > 0); d = np.log10(new[s] / old[s])
    return dict(n=int(s.sum()), median=float(np.median(d)), p16=float(np.percentile(d, 16)), p84=float(np.percentile(d, 84)))


P(f"CFG960 {MODE} (criteria 12896a21d). CFG652 stored sample {NG} groups ({int((I652['Mcond'] > 0).sum())} with M_cond > 0).")
P("  sources sha256: " + ", ".join(f"{k} {v[:12]}" for k, v in SOURCES.items()))
assert SOURCES["cfg652_model.py"] == SHA_MODEL, "cfg652_model.py changed since the CFG652 freeze"

# =====================================================================================================================
if MODE == "K":
    K = {}
    s_gkv = sha(os.path.join(GKVD, "gkv_stellarmass_g09.csv")); w_gkv = fetch_sha(os.path.join(GKVD, "FETCH_LOG.md"), "gkv_stellarmass_g09.csv")
    s_g1 = sha(os.path.join(G3CD, "G3CGalv10.csv")); w_g1 = fetch_sha(os.path.join(C471, "FETCH_LOG.md"), "G3CGalv10.csv")
    s_g2 = sha(os.path.join(G3CD, "G3CFoFGroupv10.csv")); w_g2 = fetch_sha(os.path.join(C471, "FETCH_LOG.md"), "G3CFoFGroupv10.csv")
    K["K1"] = dict(gkv=[s_gkv, w_gkv], g3cgal=[s_g1, w_g1], g3cfof=[s_g2, w_g2], pass_=bool(s_gkv == w_gkv and s_g1 == w_g1 and s_g2 == w_g2))
    P(f"K1 sha256: GKV {s_gkv[:12]} vs log {str(w_gkv)[:12]}; G3CGal {s_g1[:12]} vs {str(w_g1)[:12]}; G3CFoF {s_g2[:12]} vs {str(w_g2)[:12]}"
      f" -> {'PASS' if K['K1']['pass_'] else 'FAIL'}")
    k2 = {}
    for t, mut, ph in (("", False, False), ("_POSTHOC", False, True), ("_MUTATE", True, False)):
        res, _ = score652(W652, mut=mut, posthoc=ph); c = compare(res, ST[t])
        k2[t or "_primary"] = dict(max_abs_chi2=c["chi2"], max_abs_other=c["num"], mismatches=c["mism"][:20],
                                   pass_=bool(c["chi2"] < 1e-6 and c["num"] < 1e-9 and not c["mism"]))
        P(f"K2 score{t or ' (primary)'}: max |d chi2| {c['chi2']:.1e}, max |d other| {c['num']:.1e}, mismatches {len(c['mism'])} -> "
          f"{'PASS' if k2[t or '_primary']['pass_'] else 'FAIL'}")
    K["K2"] = dict(k2, pass_=all(v["pass_"] for v in k2.values()))
    MD = np.load(os.path.join(W652, "cfg652_models.npz")); idx = np.where(I652["Mcond"] > 0)[0]; order = idx[np.argsort(I652["Mcond"][idx])]
    picks = [int(order[int(round(q * (len(order) - 1)))]) for q in (0, 0.2, 0.4, 0.6, 0.8, 1.0)]
    r3 = 0.0
    for i in picks:
        g = (I652["Mcond"][i], I652["Mhot"][i], I652["Rx_kpc"][i], I652["z"][i])
        for foot in FEET:
            for vk, fac, gt in VAR:
                for model in "ab":
                    r3 = max(r3, float(np.nanmax(np.abs(model_row(*g, foot, model, fac=fac, gt=gt) / MD[f"{foot}__{vk}__{model}"][i] - 1))))
            r3 = max(r3, float(np.nanmax(np.abs(model_row(*g, foot, "a", m1=True) / MD[f"{foot}__M1__a"][i] - 1))))
    K["K3"] = dict(groups=picks, maxrel=r3, pass_=bool(r3 < 1e-10))
    P(f"K3 cfg652_model vs stored arrays (groups {picks}, x 22): max rel {r3:.1e} -> {'PASS' if K['K3']['pass_'] else 'FAIL'} ({time.time() - T0:.0f} s)")
    NS922["AMEND"] = ""; B0 = NS922["load_bright"]()
    box = (B0["ra"] > BOX652[0]) & (B0["ra"] < BOX652[1]) & (B0["dec"] > BOX652[2]) & (B0["dec"] < BOX652[3])
    ok = box & (B0["masked"] == 0) & (B0["mmed"] > 5) & np.isfinite(B0["z"])
    Gk = Gal(B0["ra"][ok], B0["dec"][ok], B0["z"][ok], 10 ** B0["mmed"][ok])
    raw = census(Gk, I652["z"], lambda zg, zc: np.abs(zg - zc) <= 0.05 * (1 + zc), BOX652)
    Mc4, Mb4 = assemble(raw, 1.0)
    r4 = max(float(np.max(np.abs(Mc4 - I652["Mcond"]) / np.maximum(I652["Mcond"], 1))), float(np.max(np.abs(Mb4 - I652["Mbcg"]) / np.maximum(I652["Mbcg"], 1))))
    K["K4"] = dict(n=NG, maxrel=r4, f_ann_min=float(raw["f_ann"].min()), pass_=bool(r4 < 1e-9))
    P(f"K4 CFG960 census engine with CFG652's photometric settings vs stored M_cond/M_bcg (N {NG}): max rel {r4:.1e}; f_ann min {raw['f_ann'].min():.6f}"
      f" -> {'PASS' if K['K4']['pass_'] else 'FAIL'}")
    zg9, ml9 = NS922["mlim_table"](B0)[:2]; zgm, mlm = mlim(B0["z"], B0["mmed"], B0["mag"], 19.5, 20.0)
    same_tab = bool(np.array_equal(zg9, zgm) and np.array_equal(ml9, mlm))
    CJ = json.load(open(os.path.join(C922, "cfg922_census.json")))["eRASS1"]; comp = comp_factory(zg9, ml9); r5 = 0.0
    for c in CJ:
        cc, cu, _ = comp(c["z"]); r5 = max(r5, abs(cc / c["c_cen"] - 1), abs(cu / c["c_up"] - 1))
    K["K5"] = dict(mlim_algorithm_identical=same_tab, maxrel=float(r5), n=len(CJ), pass_=bool(same_tab and r5 < 1e-12))
    P(f"K5 CFG922 completeness: my M_lim algorithm == CFG922 mlim_table {same_tab}; Census.comp vs cfg922_census.json c_cen/c_up (N {len(CJ)}): "
      f"max rel {r5:.1e} -> {'PASS' if K['K5']['pass_'] else 'FAIL'}")
    allp = all(v["pass_"] for v in K.values())
    P(f"\nK overall: {'ALL PASS' if allp else 'FAILURES PRESENT'}  ({time.time() - T0:.0f} s; peak RSS {rss_gb():.2f} GB)")
    json.dump(dict(lane="CFG960", criteria="12896a21d", mode="K", sources=SOURCES, K=K, all_pass=allp),
              open(os.path.join(HERE, "cfg960_K.json"), "w"), indent=1, default=float)
    sys.exit(0 if allp else 1)

# =====================================================================================================================
if MODE == "MAIN":
    RES = dict(lane="CFG960", criteria="12896a21d", mode="MAIN", sources=SOURCES)
    gal, grp, n_gkv = load_gama()
    G = Gal(gal["ra"], gal["dec"], gal["z"], 10 ** gal["logm"])
    P(f"  census galaxies (G3CGalv10 x GKV, logM* > 5): {len(gal['ra'])} of {n_gkv} GKV rows; G3C FoF groups {len(grp['gid'])}")
    zgG, mlG = mlim(gal["z"], gal["logm"], gal["rpetro"], 19.3, 19.8); compG = comp_factory(zgG, mlG)
    P(f"  GAMA M_lim(z) (median logM* at 19.3 <= r <= 19.8): " + ", ".join(f"z {a:.2f}: {b:.2f}" for a, b in zip(zgG[::5], mlG[::5])))
    zA = np.full(NG, np.nan); nA = np.zeros(NG, int); inG = np.zeros(NG, bool)
    for i in range(NG):
        th = I652["R500_arcmin"][i] / 60.0; inG[i] = aperture_inside(I652["ra"][i], I652["dec"][i], th, G09)
        if inG[i]:
            zA[i], nA[i] = anchor(G, I652["ra"][i], I652["dec"][i], th, I652["z"][i])
    noanc = inG & ~np.isfinite(zA)
    P(f"  footprint: {inG.sum()} of {NG} R_X apertures wholly inside G09; NO ANCHOR {noanc.sum()}; |z_grp - z_eF| percentiles (5/16/50/84/95) "
      f"{np.percentile(np.abs(zA[np.isfinite(zA)] - I652['z'][np.isfinite(zA)]), [5, 16, 50, 84, 95]).round(4).tolist()}")
    cc = np.array([compG(z)[0] if np.isfinite(z) else np.nan for z in zA]); cu = np.array([compG(z)[1] if np.isfinite(z) else np.nan for z in zA])
    P(f"  completeness at z_grp: c_cen median {np.nanmedian(cc):.3f} (16-84% {np.nanpercentile(cc, 16):.3f}-{np.nanpercentile(cc, 84):.3f}); "
      f"c_up median {np.nanmedian(cu):.3f}")
    vw = lambda W: (lambda zg, zc: vwin(zg, zc, W))
    raw = census(G, zA, vw(W_PRIMARY), G09, box_in=G09)
    Mc, Mb = assemble(raw, np.nan_to_num(cc, nan=1.0)); Mc[~np.isfinite(zA)] = 0.0; Mb[~np.isfinite(zA)] = 0.0
    inc = Mc > 0
    P(f"  PRIMARY S-cen: included {inc.sum()} (in G09 {inG.sum()}, no anchor {noanc.sum()}, M_cond = 0 after census {int((inG & np.isfinite(zA) & ~inc).sum())});"
      f" median M_cond {np.median(Mc[inc]):.3e}; M_bcg > 0 {int((Mb > 0).sum())}")
    # ---- M-PLANT and M-NULL (census controls, before any model) ----
    rp = census(G, zA, vw(W_PRIMARY), G09, box_in=G09, plant=1e12, idx=np.where(inc)[0])
    e_net = float(np.max(np.abs(rp["net"][inc] - raw["net"][inc] - 1e12))); bcg_ok = bool(np.all(rp["bcg"][inc] == np.maximum(raw["bcg"][inc], 1e12)))
    mplant = bool(e_net < 1e-9 * 1e12 and bcg_ok)
    P(f"[M-PLANT] 1e12 Msun at each included centre (anchor held): max |net' - net - 1e12| {e_net:.2e}; bcg' == max(bcg, 1e12) {bcg_ok} -> "
      f"{'BITES' if mplant else 'FAIL'}")
    rng = np.random.default_rng(960); NR = 300; pr_ra, pr_de, pr_rx, pr_z = [], [], [], []; ii = np.where(inc)[0]
    while len(pr_ra) < NR:
        j = ii[rng.integers(0, len(ii))]; rx = I652["R500_arcmin"][j]; ra_ = rng.uniform(G09[0], G09[1]); de_ = rng.uniform(G09[2], G09[3])
        if aperture_inside(ra_, de_, rx / 60.0, G09):
            pr_ra.append(ra_); pr_de.append(de_); pr_rx.append(rx); pr_z.append(zA[ii[rng.integers(0, len(ii))]])
    rn = census(G, np.array(pr_z), vw(W_PRIMARY), G09, box_in=G09, pos=(np.array(pr_ra), np.array(pr_de), np.array(pr_rx)))
    mn, se = float(rn["net"].mean()), float(rn["net"].std(ddof=1) / math.sqrt(NR)); mnull = bool(abs(mn) < 3 * se)
    P(f"[M-NULL] {NR} random apertures: mean raw net {mn:.3e} +- {se:.2e} (|mean| < 3 SE: {mnull}); included-group median raw net "
      f"{np.median(raw['net'][inc]):.3e} -> {'PASS' if mnull else 'FAIL'}")
    # ---- variants ----
    VARS = {}
    VARS["V1_nocomp"] = assemble(raw, 1.0)
    VARS["V2_cup"] = assemble(raw, np.nan_to_num(cu, nan=1.0))
    for nm, W in (("V4_w1000", 1000.0), ("V5_w3000", 3000.0)):
        VARS[nm] = assemble(census(G, zA, vw(W), G09, box_in=G09), np.nan_to_num(cc, nan=1.0))
    g3 = Mc.copy(), Mb.copy(); nmatch = 0
    gp = np.c_[grp["ra"] * np.cos(np.radians(grp["dec"])), grp["dec"]]; gtree = cKDTree(gp)
    for i in np.where(inc)[0]:
        th = I652["R500_arcmin"][i] / 60.0; p = [I652["ra"][i] * math.cos(math.radians(I652["dec"][i])), I652["dec"][i]]
        k = np.array(gtree.query_ball_point(p, 0.5 * th), int)
        k = k[vwin(grp["z"][k], zA[i], W_PRIMARY)] if k.size else k
        if k.size == 0:
            continue
        gsel = int(grp["gid"][k[np.argmax(grp["nfof"][k])]]); nmatch += 1
        mem = np.where(gal["gid"] == gsel)[0]
        d = np.hypot(gal["ra"][mem] * np.cos(np.radians(gal["dec"][mem])) - p[0], gal["dec"][mem] - p[1])     # CFG652's planar metric
        mi = mem[d <= th]; mm = 10 ** gal["logm"][mi]; inner = mi[d[d <= th] <= 0.2 * th]
        bcg = float((10 ** gal["logm"][inner]).max()) if inner.size else 0.0
        tot = float(mm.sum()); g3[0][i] = bcg + cc[i] * max(tot - bcg, 0.0); g3[1][i] = bcg
    VARS["V3_g3c"] = g3
    P(f"  V3 G3C membership: {nmatch} of {inc.sum()} included groups matched to a G3C FoF group (others keep the primary value)")
    for nm, (vc, vb) in VARS.items():
        vc[~np.isfinite(zA)] = 0.0
        P(f"  [{nm}] included {int((vc > 0).sum())}; median M_cond {np.median(vc[vc > 0]):.3e}; dlog10 vs primary median "
          f"{bstats(vc, Mc)['median']:+.3f}")
    F = I652["Mcond"]; A1c = np.array([g["Mc_A1c"] for g in json.load(open(os.path.join(C924, "cfg924_census.json")))["groups"]])
    BR = dict(S_vs_F=bstats(Mc, F), S_vs_A1c=bstats(Mc, A1c), V1_vs_F=bstats(VARS["V1_nocomp"][0], F))
    for k, b in BR.items():
        P(f"  [dlog10 {k}] median {b['median']:+.3f} (16-84% {b['p16']:+.3f} / {b['p84']:+.3f}), N {b['n']}")
    json.dump(dict(groups=[dict(i=i, eid=float(I652["eid"][i]), z_eF=float(I652["z"][i]), z_grp=float(zA[i]), n_anchor_cand=int(nA[i]), in_G09=bool(inG[i]),
                                Mhot=float(I652["Mhot"][i]), Mc_F=float(F[i]), Mc_A1c=float(A1c[i]), Mc_S=float(Mc[i]), Mb_S=float(Mb[i]),
                                net=float(raw["net"][i]), bcg=float(raw["bcg"][i]), n_ap=int(raw["n_ap"][i]), f_ann=float(raw["f_ann"][i]),
                                c_cen=float(cc[i]), c_up=float(cu[i]), **{f"Mc_{k}": float(v[0][i]) for k, v in VARS.items()}) for i in range(NG)],
                   mlim=dict(z=zgG.tolist(), logm=mlG.tolist()), brackets=BR, n_included=int(inc.sum()), n_in_G09=int(inG.sum()), n_no_anchor=int(noanc.sum()),
                   M_PLANT=dict(max_err=e_net, bcg_ok=bcg_ok, pass_=mplant), M_NULL=dict(mean=mn, se=se, n=NR, pass_=mnull)),
              open(os.path.join(HERE, "cfg960_census.json"), "w"), indent=1)
    if not (mplant and mnull):
        P("  census MUTATE failed: stopping before any model (lane VOID until fixed and disclosed)"); sys.exit(1)
    # ---- models ----
    wS = os.path.join(WORK, "S"); write_inputs(wS, Mc, Mb)
    P(f"\n  models: primary S-cen (CFG652 models block verbatim, {inc.sum()} groups x 22) ...")
    models652(wS); cache_from_npz(Mc, os.path.join(wS, "cfg652_models.npz"))
    for nm, (vc, vb) in VARS.items():
        w = os.path.join(WORK, nm); write_inputs(w, vc, vb); models_x1(w, nm)
    both = (F > 0) & inc
    write_inputs(os.path.join(WORK, "FONS"), np.where(both, F, 0.0), np.where(both, I652["Mbcg"], 0.0), models_from=os.path.join(W652, "cfg652_models.npz"))
    write_inputs(os.path.join(WORK, "SONF"), np.where(both, Mc, 0.0), np.where(both, Mb, 0.0), models_from=os.path.join(wS, "cfg652_models.npz"))
    # ---- scores ----
    SC = {}
    SC["S_MUTATE"], txtM = score652(wS, mut=True); m1 = SC["S_MUTATE"]["M1"]; m1ok = all(v["ok"] for v in m1.values())
    P("\n[MUTATE M1 on S-cen] " + "; ".join(f"{f[:3]} chi2 (a, relabelled) {m1[f]['chi2_relabelled_a']:.3f} vs (b) {m1[f]['chi2_b']:.3f} -> "
                                             f"{'PASS' if m1[f]['ok'] else 'FAIL'}" for f in FEET))
    SC["S"], txtS = score652(wS); SC["S_POSTHOC"], txtP = score652(wS, posthoc=True)
    for nm in list(VARS) + ["FONS", "SONF"]:
        SC[nm], _ = score652(os.path.join(WORK, nm))
    L = SC["S"]["final"]; lab0 = {f: SC["S"]["verdicts"][f]["x1"]["label"] for f in FEET}
    P("\n==== CFG960 primary (S-cen) ====")
    for foot in FEET:
        for vk in VK:
            c = SC["S"]["verdicts"][foot][vk]
            P(f"  [{foot[:3]}] {vk:4s}: chi2_a {c['a']['chi2']:5.1f} (p {c['a']['p']:.3g}) chi2_b {c['b']['chi2']:5.1f} (p {c['b']['p']:.3g}) "
              f"dchi2(b-a) {c['dchi2_b_minus_a']:+5.1f}; A_out a {c['a']['A_out']:+.3f} +- {c['a']['sA']:.3f}, b {c['b']['A_out']:+.3f} +- {c['b']['sA']:.3f} -> {c['label']}")
    cf = []
    P("  census variants (x1):")
    for nm in VARS:
        r = SC[nm]; labs = {f: r["verdicts"][f]["x1"]["label"] for f in FEET}
        if any(labs[f] != lab0[f] for f in FEET):
            cf.append(nm)
        P(f"    [{nm}] N {r['N_groups']}: " + "; ".join(f"{f[:3]} chi2_a {r['verdicts'][f]['x1']['a']['chi2']:.1f} chi2_b {r['verdicts'][f]['x1']['b']['chi2']:.1f} "
                                                      f"-> {labs[f]}" for f in FEET))
    for nm in ("FONS", "SONF", "S_POSTHOC"):
        r = SC[nm]
        P(f"  [{nm}, no verdict weight] N {r['N_groups']}: " + "; ".join(
            f"{f[:3]} chi2_a {r['verdicts'][f]['x1']['a']['chi2']:.1f} chi2_b {r['verdicts'][f]['x1']['b']['chi2']:.1f} -> {r['verdicts'][f]['x1']['label']}"
            for f in FEET) + f"; final '{r['final']}'")
    rel = {"CFG652": "HOLDS" if L == ST[""]["final"] else "MOVES", "CFG924": "HOLDS" if L == "NOT DIAGNOSTIC (FRAGILE: gas extent)" else "MOVES"}
    P(f"\n  PRIMARY LABEL L: '{L}' (N {SC['S']['N_groups']}); CENSUS-FRAGILE: {('yes: ' + ', '.join(cf)) if cf else 'no'}; vs CFG652 {rel['CFG652']}, "
      f"vs CFG924 {rel['CFG924']}; MUTATE M1 {'PASS' if m1ok else 'FAIL'}  ({time.time() - T0:.0f} s; peak RSS {rss_gb():.2f} GB)")
    for nm, txt in (("S-cen primary", txtS), ("S-cen MUTATE (M1)", txtM), ("S-cen POSTHOC (no weight)", txtP)):
        P(f"\n---- verbatim CFG652 score printout: {nm} ----\n" + txt.rstrip())
    RES.update(L=L, x1_labels=lab0, census_fragile=cf, relation=rel, M1_pass=m1ok, brackets=BR, scores=SC, n_included=int(inc.sum()),
               M_PLANT=mplant, M_NULL=mnull, peak_rss_gb=rss_gb())
    json.dump(RES, open(os.path.join(HERE, "cfg960_results.json"), "w"), indent=1, default=float)
    sys.exit(0)

# =====================================================================================================================
R960 = json.load(open(os.path.join(HERE, "cfg960_results.json")))
IS = np.load(os.path.join(WORK, "S", "cfg652_inputs.npz")); McS = IS["Mcond"]
if MODE == "INJ":
    w = os.path.join(WORK, "INJ"); write_inputs(w, McS * 10 ** 0.2, IS["Mbcg"] * 10 ** 0.2); models_x1(w, "M-INJ", use_cache=False)
    res, txt = score652(w); out = {}
    for foot in FEET:
        a, b = res["verdicts"][foot]["x1"], R960["scores"]["S"]["verdicts"][foot]["p02"]
        out[foot] = dict(chi2_a=a["a"]["chi2"], chi2_a_p02=b["a"]["chi2"], chi2_b=a["b"]["chi2"], chi2_b_p02=b["b"]["chi2"], label=a["label"], label_p02=b["label"],
                         ok=bool(abs(a["a"]["chi2"] - b["a"]["chi2"]) < 1e-6 and abs(a["b"]["chi2"] - b["b"]["chi2"]) < 1e-6 and a["label"] == b["label"]))
        P(f"M-INJ [{foot[:3]}] x1 on S x 10**0.2 (fresh calls): chi2_a {a['a']['chi2']:.6f} (primary p02 {b['a']['chi2']:.6f}), chi2_b {a['b']['chi2']:.6f} "
          f"({b['b']['chi2']:.6f}), {a['label']} ({b['label']}) -> {'PASS' if out[foot]['ok'] else 'FAIL'}")
    ok = all(v["ok"] for v in out.values())
    P(f"\nM-INJ overall: {'PASS (end to end exact)' if ok else 'FAIL'}  ({time.time() - T0:.0f} s; peak RSS {rss_gb():.2f} GB)")
    json.dump(dict(lane="CFG960", mode="INJ", M_INJ=out, pass_=ok), open(os.path.join(HERE, "cfg960_results_INJ.json"), "w"), indent=1, default=float)
    sys.exit(0 if ok else 1)

if MODE == "JITTER":
    RINJ = json.load(open(os.path.join(HERE, "cfg960_results_INJ.json")))
    MDb = np.load(os.path.join(WORK, "S", "cfg652_models.npz")); J = {f: dict(chi2_a=[], labels=[]) for f in FEET}
    for k in range(1, 5):
        Mc = McS * (1 + k * 1e-12); w = os.path.join(WORK, f"JIT_{k}"); write_inputs(w, Mc, IS["Mbcg"]); out = {}
        for foot in FEET:
            arr = np.full((NG, len(NS_RC)), np.nan)
            for i in range(NG):
                if Mc[i] > 0:
                    arr[i] = model_row(Mc[i], IS["Mhot"][i], IS["Rx_kpc"][i], IS["z"][i], foot, "a")
            for vk in VK:
                out[f"{foot}__{vk}__a"] = arr; out[f"{foot}__{vk}__b"] = MDb[f"{foot}__x1__b"]
        np.savez(os.path.join(w, "cfg652_models.npz"), **out); res, _ = score652(w)
        for foot in FEET:
            J[foot]["chi2_a"].append(res["verdicts"][foot]["x1"]["a"]["chi2"]); J[foot]["labels"].append(res["verdicts"][foot]["x1"]["label"])
        P(f"  [JITTER k={k}] " + "; ".join(f"{f[:3]} chi2_a {J[f]['chi2_a'][-1]:.3f} {J[f]['labels'][-1]}" for f in FEET) + f" ({time.time() - T0:.0f} s)")
    lab0 = R960["x1_labels"]; sens = False
    for foot in FEET:
        ca = np.array(J[foot]["chi2_a"]); J[foot].update(base=R960["scores"]["S"]["verdicts"][foot]["x1"]["a"]["chi2"], mean=float(ca.mean()),
                                                         sd=float(ca.std(ddof=1)), lo=float(ca.min()), hi=float(ca.max()),
                                                         changes=int(sum(l != lab0[foot] for l in J[foot]["labels"])))
        sens |= J[foot]["changes"] > 0
        P(f"JITTER [{foot[:3]}]: chi2_a unjittered {J[foot]['base']:.3f}; jitter mean {J[foot]['mean']:.3f} sd {J[foot]['sd']:.3f} range "
          f"{J[foot]['lo']:.3f}-{J[foot]['hi']:.3f}; label changes {J[foot]['changes']}/4")
    L = R960["L"]; reasons = []
    if not any(L.startswith(x) for x in ("(a) FAVOURED", "(b) FAVOURED", "BOTH EXCLUDED")):
        reasons.append(f"label '{L}'")
    if "FRAGILE" in L:
        reasons.append("FRAGILE")
    if "FOOTING-DEPENDENT" in L:
        reasons.append("FOOTING-DEPENDENT")
    if R960["census_fragile"]:
        reasons.append("CENSUS-FRAGILE (" + ", ".join(R960["census_fragile"]) + ")")
    if sens:
        reasons.append("NOISE-SENSITIVE")
    ctl = dict(M_PLANT=R960["M_PLANT"], M_NULL=R960["M_NULL"], M1=R960["M1_pass"], M_INJ=RINJ["pass_"])
    if not all(ctl.values()):
        reasons.append("a control failed: " + ", ".join(k for k, v in ctl.items() if not v))
    V = f"{L}; " + ("DECISIVE" if not reasons else "NOT DECISIVE (" + "; ".join(reasons) + ")") + \
        f"; vs CFG652 {R960['relation']['CFG652']}, vs CFG924 {R960['relation']['CFG924']}"
    P(f"\n  CFG960 VERDICT: {V}  ({time.time() - T0:.0f} s; peak RSS {rss_gb():.2f} GB)")
    json.dump(dict(lane="CFG960", mode="JITTER", jitter=J, noise_sensitive=sens, controls=ctl, reasons=reasons, verdict=V),
              open(os.path.join(HERE, "cfg960_results_JITTER.json"), "w"), indent=1, default=float)
