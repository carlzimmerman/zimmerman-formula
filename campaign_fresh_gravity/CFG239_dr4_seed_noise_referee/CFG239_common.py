"""CFG239 common: repo resolution, hash-guarded scratch mirror of the frozen builder,
array reconstruction (the pair array handed to vt_error_mc), MC runner, CSV writer, fit runner.
DR3 numbers are code-path tests, never results (Amendment 7(e)).  Nothing frozen is edited."""
import os, sys, hashlib, re, csv, subprocess, json, shutil, time
from pathlib import Path
import contextlib
import numpy as np

sys.dont_write_bytecode = True
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
HERE = Path(__file__).resolve().parent
BUILDER_SHA = "46452daf1f2e2521b6e5a892a7a234e6ad063f2fd4f1c7392664f63f99a507ad"
PIPE_SHA = "7c884e0e0a4cb9cb5d6280d558cf64c829974ed14143a90261bd6a6fbf3007c9"
SEED = 20261202
FIT_SEED = 20261216


def find_repo():
    e = os.environ.get("ZF_REPO")
    if e:
        return Path(e)
    p = HERE
    for _ in range(8):
        if (p / "prep_2026" / "gaia_dr4_prep").is_dir():
            return p
        p = p.parent
    raise SystemExit("ZF_REPO not set and repo not found above __file__")


REPO = find_repo()
PREP = REPO / "prep_2026" / "gaia_dr4_prep"
EXT = REPO / "real_research" / "data" / "widebinaries" / "dr3_extract"
WORK = Path(os.environ.get("CFG239_WORK", HERE / "CFG239_work"))   # scratch only, never committed
MIRROR = WORK / "mirror"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rel(p):
    p = Path(p)
    for base, tag in ((REPO, "<repo>"), (HERE, "<scratch>"), (WORK, "<work>")):
        try:
            return tag + "/" + str(p.resolve().relative_to(base.resolve()))
        except Exception:
            pass
    return "<path>/" + p.name


def guard():
    """originals and mirror copies must equal the frozen hashes."""
    a = sha(PREP / "catalog_builder" / "build_catalog.py")
    b = sha(PREP / "wide_binary_pipeline.py")
    assert a == BUILDER_SHA, "frozen builder hash changed"
    assert b == PIPE_SHA, "frozen pipeline hash changed"
    if MIRROR.exists():
        assert sha(MIRROR / "catalog_builder" / "build_catalog.py") == BUILDER_SHA
        assert sha(MIRROR / "wide_binary_pipeline.py") == PIPE_SHA
    return a, b


def make_mirror():
    guard()
    (MIRROR / "catalog_builder").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PREP / "catalog_builder" / "build_catalog.py", MIRROR / "catalog_builder" / "build_catalog.py")
    shutil.copyfile(PREP / "wide_binary_pipeline.py", MIRROR / "wide_binary_pipeline.py")
    guard()


def load_builder():
    make_mirror()
    sys.path.insert(0, str(MIRROR / "catalog_builder"))
    sys.path.insert(0, str(MIRROR))
    import importlib
    B = importlib.import_module("build_catalog")
    assert B.SEED == SEED and Path(B.__file__).resolve().is_relative_to(MIRROR.resolve())
    return B


@contextlib.contextmanager
def patched_rng(factory):
    """monkeypatch np.random.default_rng inside the mirror run only."""
    old = np.random.default_rng
    np.random.default_rng = factory
    try:
        yield
    finally:
        np.random.default_rng = old


NEED = ["source_id", "parallax", "parallax_error", "pmra", "pmdec", "pmra_error", "pmdec_error",
        "pmra_pmdec_corr", "phot_g_mean_mag"]


def build_array(B, stage_f, tag):
    """Reconstruct the pair array handed to vt_error_mc for a given stage-F file (main() lines 603-618).
    Cached in WORK.  Returns dict with compact star table."""
    cache = WORK / f"array_{tag}.npz"
    if cache.exists():
        return dict(np.load(cache, allow_pickle=False))
    t0 = time.time()
    S = dict(np.load(EXT / "stage_A.npz", allow_pickle=False))
    F = dict(np.load(stage_f, allow_pickle=False))
    extra = {"third": np.zeros(len(F["a"]), bool)}
    pre, _, _ = B.frozen_cuts(S, F["a"], F["b"], F["R"], extra)
    idx = np.flatnonzero(pre)
    extra["third"][idx] = B.third_star_flags(S, F["a"][idx], F["b"][idx])
    pre2, _, tab0 = B.frozen_cuts(S, F["a"], F["b"], F["R"], extra)
    idx2 = np.flatnonzero(pre2)
    from wide_binary_pipeline import G as GN, MSUN, AU
    vc0 = np.sqrt(GN * (tab0["M1_msun"][idx2] + tab0["M2_msun"][idx2]) * MSUN
                  / (tab0["sep_kAU"][idx2] * 1e3 * AU)) / 1e3
    vt0 = tab0["v_perp_kms"][idx2] / vc0
    thr = 0.1 * np.maximum(1.0, vt0 / 2)
    z = B.av_sfd98(S, EXT / "AV_sfd98.npz")
    av_ok = ((z["av"][F["a"]] < 0.5) & (z["av"][F["b"]] < 0.5))[idx2]
    a, b, th = F["a"][idx2], F["b"][idx2], F["th"][idx2]
    stars = np.unique(np.concatenate([a, b]))
    m = {s: i for i, s in enumerate(stars.tolist())}
    ac = np.array([m[x] for x in a.tolist()]); bc = np.array([m[x] for x in b.tolist()])
    out = {"a": ac, "b": bc, "th": th, "thr": thr, "av_ok": av_ok, "idx2": idx2,
           "id1": S["source_id"][a], "id2": S["source_id"][b]}
    for c in NEED:
        out["S_" + c] = S[c][stars]
    # full-table columns for the CSV (all F pairs, vt/AV not applied)
    full_extra = dict(extra)
    full_extra["vt_err_ok"] = np.ones(len(F["a"]), bool)
    _, _, table = B.frozen_cuts(S, F["a"], F["b"], F["R"], full_extra)
    for c, v in table.items():
        out["T_" + c] = v
    out["pre2"] = pre2
    # the frozen final set from these cuts when vt ok everywhere (for controls)
    np.savez(cache, **out)
    print(f"  built array {tag}: {len(idx2)} pairs ({time.time()-t0:.0f} s)", flush=True)
    return out


def corr_dict(ids_needed):
    z = dict(np.load(EXT / "stage_G_corr.npz"))
    have = np.isin(ids_needed, z["source_id"])
    n_unc = int((~have).sum())
    if n_unc:
        miss = np.unique(ids_needed[~have])
        z = {"source_id": np.concatenate([z["source_id"], miss]),
             "parallax_pmra_corr": np.concatenate([z["parallax_pmra_corr"], np.zeros(len(miss))]),
             "parallax_pmdec_corr": np.concatenate([z["parallax_pmdec_corr"], np.zeros(len(miss))])}
    return z, n_unc


class MC:
    """Stage-G Monte Carlo runner on a compact array; calls the frozen vt_error_mc unchanged."""
    def __init__(self, B, arr):
        self.B = B
        self.S = {c: arr["S_" + c] for c in NEED}
        self.a, self.b, self.th = arr["a"], arr["b"], arr["th"]
        self.thr, self.av_ok = arr["thr"], arr["av_ok"]
        self.id1, self.id2 = arr["id1"], arr["id2"]
        ids = np.concatenate([self.id1, self.id2])
        self.corr, self.n_unc = corr_dict(ids)
        self.arr = arr

    def run(self, seed, sel=None, n_trials=212):
        sel = np.arange(len(self.a)) if sel is None else sel
        return self.B.vt_error_mc(self.S, self.a[sel], self.b[sel], self.th[sel], self.corr,
                                  n_trials=n_trials, seed=seed)

    def final_mask(self, sig):
        return self.av_ok & (sig <= self.thr)


# --------------------------------------------------------------- CSV + fit
def write_csv(arr, mask, path):
    """builder's own CSV format (columns = list(table), csv.writer default formatting)."""
    T = {k[2:]: v for k, v in arr.items() if k.startswith("T_")}
    cols = list(T)
    idx2 = arr["idx2"]
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for j in np.flatnonzero(mask):
            i = idx2[j]
            w.writerow([T[c][i] for c in cols])


FITRE = re.compile(r"catalog \[(a0 canonical|a0 alt footing)\]\s+gamma_inf = ([0-9.+-]+) \+- ([0-9.]+)\s+"
                   r"\(chi2/bin=([0-9.]+), bins=(\d+), kappa=([0-9.]+)\)")


def parse_fit(text):
    out = {}
    for m in FITRE.finditer(text):
        key = "can" if "canonical" in m.group(1) else "alt"
        out[key] = dict(g=float(m.group(2)), s=float(m.group(3)), chi2=float(m.group(4)),
                        bins=int(m.group(5)), kappa=float(m.group(6)))
    if set(out) != {"can", "alt"}:
        raise RuntimeError("fit parser: footing line missing")
    return out


def run_fit(csv_path, seed=FIT_SEED):
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1",
               PYTHONDONTWRITEBYTECODE="1")
    for attempt in range(4):      # a pipeline process can be killed under memory pressure; the fit is deterministic, so a retry is exact
        r = subprocess.run([sys.executable, "-B", str(MIRROR / "wide_binary_pipeline.py"), "--catalog",
                            str(csv_path), "--seed", str(seed)], capture_output=True, text=True, env=env,
                           cwd=str(WORK))
        # the pipeline exits 1 when ITS OWN synthetic self-test (injection recovery gate) fails for that fit seed;
        # the catalogue lines are still printed, so the exit code is recorded, not treated as a crash
        try:
            res = parse_fit(r.stdout)
            res["gate_ok"] = (r.returncode == 0)
            return res, r.stdout
        except RuntimeError:
            pass
        time.sleep(5 + 10 * attempt)
    raise RuntimeError(f"pipeline failed rc={r.returncode}: " + r.stderr[-400:])


def pair_keys(arr, mask):
    return set(zip(arr["id1"][mask].tolist(), arr["id2"][mask].tolist()))


def sd(x):
    x = np.asarray(x, float)
    return float(np.std(x, ddof=1)) if len(x) > 1 else float("nan")


class Tee:
    def __init__(self, path):
        self.f = open(path, "w")
    def __call__(self, *a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        self.f.write(s + "\n"); self.f.flush()


def jdump(obj, path):
    Path(path).write_text(json.dumps(obj, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)))
