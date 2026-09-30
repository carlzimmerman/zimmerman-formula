#!/usr/bin/env python3
"""DR4-READY-1, Amendment 18 tooling: the per-seed-set REBUILD of stages E and F of the frozen catalog builder (NEW file; nothing frozen is edited).
Design and controls: SEED_SWEEP_DESIGN_FROZEN.md (be8a6405d), written before this code.  DR3 numbers are code-path tests, never results (Amendment 7(e)).

The frozen builder (catalog_builder/build_catalog.py, sha256 checked before and after every rebuild, never written) draws random numbers in FOUR places, SEED = build_catalog.SEED = 20261202:
  (1) stage E, the shifted realisations: pair_search(..., shift=True, seed=r + 1), per-block seeds seed * 1000 + block        -> build k: r + 1 + 100 k
  (2) stage E, the half-mask:          default_rng(SEED) inside main()'s _e()                                               -> build k: SEED + k
  (3) stage F, the leave-10%-out fold: default_rng(SEED) inside r_chance()                                                  -> build k: SEED + k
  (4) stage G, the velocity-error MC:  vt_error_mc(seed = SEED), a DEFAULT ARGUMENT bound at import                         -> build k: SEED + k, passed EXPLICITLY (driver)
k = 0 is the frozen builder (its own seeds).  The seeds are changed IN MEMORY: the source text of main()'s _e / _f closures and of r_chance is extracted with inspect, given exactly the substitutions
above (each asserted to occur the expected number of times) and executed in a namespace.  Stages A to D are the shared inputs; E and F are written to a per-build directory (gitignored).
Used by seed_sweep.py and the driver's --seed-offset; run directly it prints the seed sets and the builder hash.
Run:  python3 prep_2026/gaia_dr4_prep/dr4_ready_1/seeded_build.py [--k 3]"""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, inspect, json, re, textwrap, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PREP = HERE.parent
REPO = PREP.parents[1]
BUILDER_PATH = PREP / "catalog_builder" / "build_catalog.py"
FROZEN_BUILDER_SHA256 = "46452daf1f2e2521b6e5a892a7a234e6ad063f2fd4f1c7392664f63f99a507ad"      # RELEASE_DAY_CHECKLIST section 3
E_SHIFT_STRIDE = 100                                                                              # stage-E shift seeds r + 1 + 100 k
_B = None


def file_sha256(path=BUILDER_PATH):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def assert_builder_frozen(where, path=BUILDER_PATH, expected=FROZEN_BUILDER_SHA256):
    got = file_sha256(path)
    if got != expected:
        raise RuntimeError(f"the frozen builder's sha256 changed ({where}): {got} != {expected}; stop and find out why (RELEASE_DAY_CHECKLIST section 3)")
    return got


def import_builder():
    """build_catalog imported READ-ONLY after the hash guard."""
    global _B
    if _B is None:
        assert_builder_frozen("before import")
        for p in (str(PREP / "catalog_builder"), str(PREP)):
            if p not in sys.path:
                sys.path.insert(0, p)
        import build_catalog as B
        _B = B
    return _B


def seed_set(k, n_shift=None, B=None):
    """the four seed uses of build k (k = 0: the frozen builder's own seeds)."""
    B = B or import_builder()
    n = B.N_SHIFT if n_shift is None else n_shift
    return dict(k=int(k), SEED=int(B.SEED), n_shift=int(n),
                stage_E_shift_seeds=[r + 1 + E_SHIFT_STRIDE * k for r in range(n)],
                stage_E_block_seed="(r + 1 + %d k) * 1000 + block, block = 0..399" % E_SHIFT_STRIDE,
                stage_E_mask=int(B.SEED + k), stage_F_fold=int(B.SEED + k), stage_G_velocity_mc=int(B.SEED + k))


def seed_sets_disjoint(ks, n_shift=30, n_blocks=400):
    """the per-block stage-E seeds of builds ks: all distinct?  Returns (n_seeds, n_duplicates)."""
    seen, dup = set(), 0
    for k in ks:
        for r in range(n_shift):
            for b in range(n_blocks):
                s = (r + 1 + E_SHIFT_STRIDE * k) * 1000 + b
                dup += s in seen
                seen.add(s)
    return len(ks) * n_shift * n_blocks, dup


def scan_random_sites(path=BUILDER_PATH):
    """every random-draw site of the frozen builder (the guard that the four uses above are all of them)."""
    sites = {"default_rng": [], "seed=r + 1": [], "other": []}
    for i, line in enumerate(Path(path).read_text().splitlines(), 1):
        code = line.split("#")[0]
        if "default_rng(" in code:
            sites["default_rng"].append((i, line.strip()))
        if "seed=r + 1)" in code:
            sites["seed=r + 1"].append((i, line.strip()))
        if re.search(r"np\.random\.(?!default_rng)|RandomState|random\.seed|\.shuffle\(|\.permutation\(", code):
            sites["other"].append((i, line.strip()))
    return sites


def _noop(*a, **k):
    return None


def patched_stage_functions(B, S, keep, D, sigma18_dir, k, n_shift=None):
    """(run_E, run_F) for seed set k: main()'s own closures, re-seeded in memory."""
    n = B.N_SHIFT if n_shift is None else n_shift
    src = inspect.getsource(B.main)
    # ---- stage E
    i0, i1 = src.index("    def _e():"), src.index("    E = cached(")
    e_text = textwrap.dedent(src[i0:i1])
    assert e_text.count("seed=r + 1)") == 1 and e_text.count("np.random.default_rng(SEED)") == 1, "stage-E anchor strings changed in the builder"
    e_text = e_text.replace("seed=r + 1)", "seed=r + 1 + %d * K_SEED)" % E_SHIFT_STRIDE).replace("np.random.default_rng(SEED)", "np.random.default_rng(SEED + K_SEED)")
    nsE = dict(np=np, SEED=B.SEED, K_SEED=int(k), N_SHIFT=int(n), orient=B.orient, pair_search=B.pair_search, S=S, keep=keep, CHANCE_MODE=B.CHANCE_MODE, print=_noop)
    exec(compile(e_text, "build_catalog.py::_e (re-seeded)", "exec"), nsE)
    # ---- r_chance (stage F's fold)
    rc_text = textwrap.dedent(inspect.getsource(B.r_chance))
    assert rc_text.count("np.random.default_rng(SEED)") == 1, "r_chance anchor string changed in the builder"
    rc_text = rc_text.replace("np.random.default_rng(SEED)", "np.random.default_rng(SEED + K_SEED)")
    nsR = dict(np=np, SEED=B.SEED, K_SEED=int(k), kde_density=B.kde_density)
    exec(compile(rc_text, "build_catalog.py::r_chance (re-seeded)", "exec"), nsR)
    # ---- stage F
    j0, j1 = src.index("    def _f():"), src.index("    F = cached(")
    f_text = textwrap.dedent(src[j0:j1])
    nsF = dict(np=np, sigma18_map=B.sigma18_map, ext=Path(sigma18_dir), D=D, S_KDE_AU=B.S_KDE_AU, features=B.features, S=S, sigma18_at=B.sigma18_at, N_SHIFT=int(n),
               r_chance=nsR["r_chance"], print=_noop)
    exec(compile(f_text, "build_catalog.py::_f", "exec"), nsF)

    def run_E():
        return nsE["_e"]()

    def run_F(E):
        nsF["E"] = E
        return nsF["_f"]()
    return run_E, run_F


def load_shared(ext):
    """the stage A to D inputs of the build in `ext` (shared by every seed set)."""
    ext = Path(ext)
    S = dict(np.load(ext / "stage_A.npz"))
    keep = np.flatnonzero(np.load(ext / "stage_B.npz")["n_nbr"] <= 30)
    D = dict(np.load(ext / "stage_D.npz"))
    return S, keep, D


def rebuild_EF(ext, work, k, n_shift=None, reuse=False):
    """stages E and F of seed set k from the shared A to D inputs of `ext`; written to work/stage_E.npz and work/stage_F.npz.  Returns (E, F, seconds)."""
    B = import_builder()
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    if reuse and (work / "stage_F.npz").exists() and (work / "stage_E.npz").exists():
        return dict(np.load(work / "stage_E.npz")), dict(np.load(work / "stage_F.npz")), 0.0
    t0 = time.time()
    assert_builder_frozen("before the rebuild of seed set %d" % k)
    S, keep, D = load_shared(ext)
    run_E, run_F = patched_stage_functions(B, S, keep, D, Path(ext), k, n_shift)
    E = run_E()
    np.savez(work / "stage_E.npz", **E)
    F = run_F(E)
    np.savez(work / "stage_F.npz", **F)
    assert_builder_frozen("after the rebuild of seed set %d" % k)
    return E, F, time.time() - t0


def seed_list(K=10, n_shift=None, B=None, K_G=100):
    """the pre-registered seed list of Amendment 18 (draft rev 2) with the builder's hash: a pure function of the rule, to be committed BEFORE the data are opened.
    G-only sweep (sigma_build): build k = 1..K_G re-seeds ONLY stage G, SEED + k, passed explicitly (stages A-F are the primary's).  Full E-G rebuilds (confirmation): build k = 1..K re-seeds the stage-E shifts
    r + 1 + 100 k and the stage-E mask, the stage-F fold and stage G with SEED + k.  k = 0 is the frozen builder in both."""
    B = B or import_builder()
    return dict(about="Amendment 18 (draft rev 2, NOT FILED) seed list: G-only sweep k = 1..K_G (stage G seed SEED + k, explicit); full E-G rebuilds k = 1..K (stage-E shifts r + 1 + 100 k; stage-E mask, stage-F fold and stage G SEED + k); k = 0 is the frozen builder",
                builder_sha256=assert_builder_frozen("seed list"), SEED=int(B.SEED), n_shift=int(B.N_SHIFT if n_shift is None else n_shift), K=int(K), K_G=int(K_G), fit_seed=20261216,
                fit_only_control_seeds=[20261216 + j for j in range(1, max(K, 50) + 1)], g_only_stage_G_seeds=[int(B.SEED) + k for k in range(1, K_G + 1)],
                seed_sets=[seed_set(k, n_shift, B) for k in range(K + 1)])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=1)
    ap.add_argument("--write-list", default=None, help="write the seed list for k = 0..K to this JSON file and exit")
    ap.add_argument("--K", type=int, default=10, help="full E-G rebuilds k = 1..K")
    ap.add_argument("--K-G", type=int, default=100, help="G-only builds k = 1..K_G")
    a = ap.parse_args()
    B = import_builder()
    if a.write_list:
        Path(a.write_list).write_text(json.dumps(seed_list(a.K, None, B, a.K_G), indent=1) + "\n")
        print("wrote", a.write_list)
        sys.exit(0)
    print("builder sha256", assert_builder_frozen("print"))
    print(json.dumps(seed_set(a.k, B=B), indent=1)[:1500])
    print("per-block stage-E seeds of builds 0..10 at N_SHIFT 30: (n, duplicates) =", seed_sets_disjoint(range(11)))
    print("random-draw sites of the builder:", json.dumps(scan_random_sites(), indent=1)[:1200])
