"""Mock Gaia DR4 wide-binary sky for the /wide-binaries page, built with the repo's FROZEN pipeline (imported read-only, nothing re-implemented).

Imports prep_2026/gaia_dr4_prep/wide_binary_pipeline.py and uses its own make_population (Kepler orbits, projection, Gaia DR4-level errors, frozen
cuts folded into the selection), vtilde_of (boost injected at the TRUE 3D acceleration), bin_medians, model_medians and fit_gamma, with the pipeline's
own master-MC size (3,000,000), seed (20261216), bin edges, kappa anchor and N_data (30,000). Both a0 footings are run (one process each).

Per footing it writes (public/data/wb/):
  ensemble_<foot>.json : for each injected gamma_inf (Newton 1.00, the in-force Arm A band floor and top, the MOND benchmark 1.33) K recovered
                         (gamma_hat, sigma_fit) pairs from independent mock catalogs, the bin medians of realization 0 with the model curves, and the
                         sigma(N) scaling at the Arm A band floor.
  pairs_<foot>.bin     : realization 0 of each injection as uint16 pairs (log10 y_proj, vtilde), for the scatter plot.
Nothing here is a measurement; it is the pipeline's own self-test turned into a forecast. The boost is the pipeline's phenomenological injection
(velocity scaling at fixed orbit), not a self-consistent modified-orbit integration.

Usage: python3 ai_slop/website/scripts/build_wb_mock_sky.py canonical|alt [K]
"""
import json, os, sys, time
import numpy as np

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "prep_2026", "gaia_dr4_prep"))
import wide_binary_pipeline as wb                                  # noqa: E402

FOOT = sys.argv[1]
K = int(sys.argv[2]) if len(sys.argv) > 2 else 100
assert FOOT in ("canonical", "alt")
A0 = wb.A0_CAN if FOOT == "canonical" else wb.A0_ALT
OUT = os.path.join(REPO, "ai_slop", "website", "public", "data", "wb")
os.makedirs(OUT, exist_ok=True)
N_DATA, NM, SEED = 30000, 3_000_000, 20261216
SMOKE = os.environ.get('WB_SMOKE') == '1'          # quick wiring test only; writes to a scratch folder, never to the site
if SMOKE:
    NM, K = 400_000, 2
    OUT = os.path.join('/tmp', 'wb_smoke'); os.makedirs(OUT, exist_ok=True)
lo, top = (wb.GAMMA_TARGET, wb.GAMMA_TARGET_TOP) if FOOT == "canonical" else (wb.GAMMA_TARGET_ALT, wb.GAMMA_TARGET_ALT_TOP)
INJ = [("Newton / Arm B", 1.00), ("Arm A band floor", lo), ("Arm A band top", top), ("MOND benchmark", wb.GAMMA_MOND)]
rng = np.random.default_rng(SEED + (0 if FOOT == "canonical" else 1))
t0 = time.time()

def log(*a):
    print(f"[{FOOT} {time.time() - t0:5.0f}s]", *a, flush=True)

pop_m = wb.make_population(NM, rng, dr4=True)
log("master MC pairs after selection:", len(pop_m["s_obs"]))
mod = wb.model_medians(pop_m, A0, wb.GRID, rng)
log("model curves built")
grid = wb.GRID
centres = 0.5 * (wb.EDGES[:-1] + wb.EDGES[1:])

def catalog(n):
    pop = wb.make_population(int(n * 2.7), rng, dr4=True)
    keep = rng.permutation(len(pop["s_obs"]))[:n]
    assert len(pop["s_obs"]) >= n, "population too small for this N"
    return {k: v[keep] for k, v in pop.items()}

def one_fit(pop, ginj):
    vt = wb.vtilde_of(pop, ginj, A0)
    ly = np.log10(pop["g_proj"] / A0)
    med, sig, cnt = wb.bin_medians(ly, vt, boot=200, rng=rng)
    g, sg, chi2, nb, kap = wb.fit_gamma(med, sig, mod, grid)
    return dict(g=float(g), s=float(sg), chi2=float(chi2), nb=int(nb), kappa=float(kap)), ly, vt, med, sig, cnt

res, pairs = {}, []
for name, ginj in INJ:
    fits = []
    for r in range(K):
        pop = catalog(N_DATA)
        f, ly, vt, med, sig, cnt = one_fit(pop, ginj)
        fits.append(f)
        if r == 0:
            keep = vt < wb.VTCAP
            pairs.append(np.stack([np.clip((ly[keep] + 1.5) / 3.7, 0, 1), np.clip(vt[keep] / wb.VTCAP, 0, 1)], 1))
            first = dict(med=[None if not np.isfinite(x) else float(x) for x in med], sig=[None if not np.isfinite(x) else float(x) for x in sig],
                         cnt=[int(c) for c in cnt], deep=int(((pop["g_proj"] / A0) < 0.3).sum()), fit=f)
    g = np.array([f["g"] for f in fits]); s = np.array([f["s"] for f in fits])
    res[name] = dict(inject=float(ginj), first=first, gamma_hat=[float(x) for x in g], sigma_fit=[float(x) for x in s],
                     mean=float(g.mean()), rms=float(g.std(ddof=1)), mean_sigma=float(s.mean()))
    log(f"inject {ginj:.4f} ({name}): recovered mean {g.mean():.4f} rms {g.std(ddof=1):.4f} mean sigma_fit {s.mean():.4f} over {K} catalogs")

# model curves for the plot: the grid row nearest each injected gamma (these are the pipeline's noise-convolved forward models)
curves = {}
for name, ginj in INJ:
    i = int(np.argmin(np.abs(grid - ginj)))
    curves[name] = dict(gamma=float(grid[i]), med=[None if not np.isfinite(x) else float(x) for x in mod[0][i]])

# sigma(N) at the Arm A band floor, and the separation from Newton in sigma
scaling = []
KN = 20
for n in ((3000, 30000) if SMOKE else (3000, 10000, 30000, 100000, 300000)):
    gs, ss = [], []
    for _ in range(2 if SMOKE else (KN if n <= 100000 else 8)):
        f, *_ = one_fit(catalog(n), lo)
        gs.append(f["g"]); ss.append(f["s"])
    gs, ss = np.array(gs), np.array(ss)
    scaling.append(dict(n=n, mean=float(gs.mean()), rms=float(gs.std(ddof=1)), mean_sigma=float(ss.mean()), reps=len(gs)))
    log(f"N={n}: gamma_hat {gs.mean():.4f} rms {gs.std(ddof=1):.4f} mean sigma_fit {ss.mean():.4f}")

thr = dict(newton=1.0, arm_b=wb.GAMMA_B_PRED, arm_b_sigma=wb.GAMMA_B_PRED_SIG, arm_b_kill=wb.GAMMA_B_KILL, arm_a_falsified_below=wb.GAMMA_A_FALSIFIED_BELOW,
           noverdict_edge=wb.NOVERDICT_EDGE, kappa_window=list(wb.KAPPA_WINDOW), arm_a_floor=lo, arm_a_top=top, mond=wb.GAMMA_MOND)
out = dict(footing=FOOT, a0=A0, y_extN=float(wb.y_extN(A0)), n_data=N_DATA, K=K, master_pairs=int(len(pop_m["s_obs"])), edges=[float(x) for x in wb.EDGES],
           centres=[float(x) for x in centres], vtcap=wb.VTCAP, thresholds=thr, results=res, curves=curves, scaling=scaling, seed=SEED, runtime_s=time.time() - t0,
           pair_ranges=dict(logy=[-1.5, 2.2], vt=[0, wb.VTCAP]), pair_counts=[int(len(p)) for p in pairs],
           pipeline="prep_2026/gaia_dr4_prep/wide_binary_pipeline.py (frozen; imported unchanged)")
json.dump(out, open(os.path.join(OUT, f"ensemble_{FOOT}.json"), "w"))
allp = np.concatenate([np.round(p * 65535).astype("<u2").reshape(-1) for p in pairs])
allp.tofile(os.path.join(OUT, f"pairs_{FOOT}.bin"))
log("done", f"pairs file {allp.nbytes / 1e6:.2f} MB")
