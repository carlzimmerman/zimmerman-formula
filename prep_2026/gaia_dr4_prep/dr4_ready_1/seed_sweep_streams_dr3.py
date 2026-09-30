#!/usr/bin/env python3
"""DR4-READY-1, Amendment 18 tooling: Q-S (which seed stream carries the build-to-build noise) and Q-N (sigma_build against N) of SEED_SWEEP_STREAMS_FROZEN.md (21aeb4e01), committed before this script existed.
DR3 numbers are code-path tests, never results (Amendment 7(e)); NON-SCORING; no verdict words.  OFFLINE (socket guard here; the pipeline CLI fits are subprocesses).  NEW file.
Families (ten builds each, k = 0..9, k = 0 shared): ALL = WP2-gamma's ten builds through the driver (--seed-offset k --stage-dir wp2_gamma_k); G-ONLY = stage F fixed at k = 0's, G seeded SEED + k; EF-ONLY = stage F of build k,
G at the frozen seed.  Every final CSV is fitted by the pipeline's own --catalog run (seed 20261216).  Q-N: the ALL builds' tables restricted to build-independent subsets (bucket = first byte of sha256(str(source_id1)) mod 4).
Run:  python3 prep_2026/gaia_dr4_prep/dr4_ready_1/seed_sweep_streams_dr3.py"""
import sys
sys.dont_write_bytecode = True
import hashlib, json, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import dry_run_driver as D
import seeded_build as SB
import seed_sweep as SS

D.init(False)
B = SB.import_builder()
SB.assert_builder_frozen("streams start")
ext = D.extract_dir("dr3", "primary")
out_dir = ext / "seed_streams"
out_dir.mkdir(exist_ok=True)
T0 = time.time()
LOG = []
WORKERS = 4
SIG_SYS = 0.02


def P(s=""):
    print(s, flush=True); LOG.append(s)


def build(family, k):
    if family == "ALL":
        b, r = D.run("dr3", "primary", "extract-builder", None, False, seed_offset=k, stage_dir=ext / f"wp2_gamma_{k}")
    elif family == "G-only":
        b, r = D.run("dr3", "primary", "extract-builder", None, False, seed_offset=k, stage_dir=None)
    else:
        b, r = D.run("dr3", "primary", "extract-builder", None, False, seed_offset=0, stage_dir=ext / f"wp2_gamma_{k}")
    p = out_dir / f"{family}_k{k}.csv"
    p.write_bytes(b)
    return p, r


def fit_many(jobs):
    """jobs: list of (csv_path, seed) -> list of parsed fits, run WORKERS at a time."""
    with ThreadPoolExecutor(WORKERS) as ex:
        return list(ex.map(lambda j: SS.fit_via_pipeline_cli(j[0], j[1]), jobs))


def sd1(x):
    return float(np.std(np.asarray(x, float), ddof=1))


P("SEED SWEEP STREAMS (DR3 PRIMARY base, N_SHIFT = 30, registered fit path; DR3 numbers are code-path tests, never results)")
# ---------------------------------------------------------------- builds
CSV, REP = {}, {}
for fam in ("ALL", "G-only", "EF-only"):
    for k in range(10):
        if k == 0 and fam != "ALL":
            CSV[(fam, 0)], REP[(fam, 0)] = CSV[("ALL", 0)], REP[("ALL", 0)]
            continue
        CSV[(fam, k)], REP[(fam, k)] = build(fam, k)
SB.assert_builder_frozen("after the builds")
sha = {key: REP[key]["sha256"] for key in CSV}
P(f"  builds done: ALL k = 0 sha256 {sha[('ALL', 0)][:16]} (the reference CSV: {sha[('ALL', 0)].startswith('6fff64d964ebaa72')}); uncovered correlation ids per build (ALL) {[REP[('ALL', k)]['correlations'][0]['n_uncovered'] for k in range(10)]}")
sets = {key: SS.pair_set(CSV[key]) for key in CSV}
FL = {fam: [(len(sets[(fam, 0)] - sets[(fam, k)]), len(sets[(fam, k)] - sets[(fam, 0)])) for k in range(1, 10)] for fam in ("ALL", "G-only", "EF-only")}
CNT = {fam: [REP[(fam, k)]["n_pairs"] for k in range(10)] for fam in ("ALL", "G-only", "EF-only")}
# ---------------------------------------------------------------- Q-S fits
jobs = [(CSV[("ALL", 0)], 20261216)] + [(CSV[(fam, k)], 20261216) for fam in ("ALL", "G-only", "EF-only") for k in range(1, 10)] + [(CSV[("ALL", 0)], 20261216 + j) for j in range(1, 11)]
t = time.time()
fits = fit_many(jobs)
FIT = {("ALL", 0): fits[0]}
i = 1
for fam in ("ALL", "G-only", "EF-only"):
    for k in range(1, 10):
        FIT[(fam, k)] = fits[i]; i += 1
for fam in ("G-only", "EF-only"):
    FIT[(fam, 0)] = FIT[("ALL", 0)]
CTL = fits[i:]
P(f"  {len(fits)} pipeline fits in {time.time() - t:.0f} s ({WORKERS} at a time)")
QS = {}
P("\nQ-S  family     pairs (mean, SD)        one-way flips vs k = 0 (mean)   footing     gamma-hat mean   SD(gamma-hat)   SD/sigma_fit   SD/sigma_tot   kappa range")
for fam in ("ALL", "G-only", "EF-only"):
    fl = float(np.mean([(a + b) / 2 for a, b in FL[fam]]))
    QS[fam] = dict(pairs_mean=float(np.mean(CNT[fam])), pairs_sd=sd1(CNT[fam]), flips_mean_one_way=fl, flips=FL[fam], per_footing={})
    for f in ("canonical", "alt"):
        g = [FIT[(fam, k)][f]["g"] for k in range(10)]
        ms = float(np.mean([FIT[(fam, k)][f]["s"] for k in range(10)]))
        mt = float(np.mean([np.hypot(FIT[(fam, k)][f]["s"], SIG_SYS) for k in range(10)]))
        kap = [FIT[(fam, k)][f]["kappa"] for k in range(10)]
        QS[fam]["per_footing"][f] = dict(gammas=g, sigma_fits=[FIT[(fam, k)][f]["s"] for k in range(10)], sd=sd1(g), mean_sigma_fit=ms, sd_over_sigma_fit=sd1(g) / ms, sd_over_sigma_tot=sd1(g) / mt, kappa_min=min(kap), kappa_max=max(kap))
        P(f"      {fam:8s} {np.mean(CNT[fam]):8.1f} ({sd1(CNT[fam]):5.1f})       {fl:8.1f}                         {f:9s}   {np.mean(g):.4f}         {sd1(g):.4f}        {sd1(g) / ms:.3f}          {sd1(g) / mt:.3f}         {min(kap):.4f}-{max(kap):.4f}")
CTLsd = {f: sd1([c[f]["g"] for c in CTL]) for f in ("canonical", "alt")}
CTLsd_incl = {f: sd1([FIT[("ALL", 0)][f]["g"]] + [c[f]["g"] for c in CTL]) for f in ("canonical", "alt")}
for f in ("canonical", "alt"):
    ms = QS["ALL"]["per_footing"][f]["mean_sigma_fit"]
    P(f"      fit-only control ({f}): k = 0 CSV refitted with 10 other seeds: SD {CTLsd[f]:.4f} = {CTLsd[f] / ms:.3f} of mean sigma_fit (incl. the registered fit: {CTLsd_incl[f]:.4f}); values {[round(c[f]['g'], 4) for c in CTL]}")
for f in ("canonical", "alt"):
    a, g_, e_ = (QS[x]["per_footing"][f]["sd"] for x in ("ALL", "G-only", "EF-only"))
    P(f"      variance shares ({f}; not additive): SD_Gonly^2 / SD_ALL^2 = {g_ ** 2 / a ** 2:.2f}; SD_EFonly^2 / SD_ALL^2 = {e_ ** 2 / a ** 2:.2f}")
# ---------------------------------------------------------------- Q-N
def bucket(sid):
    return hashlib.sha256(str(int(sid)).encode()).digest()[0] % 4


def subset_csv(path, buckets, tag):
    lines = Path(path).read_text().strip().split("\n")
    head = lines[0].split(",")
    i1 = head.index("source_id1")
    sel = [l for l in lines[1:] if bucket(l.split(",")[i1]) in buckets]
    p = out_dir / f"{tag}.csv"
    p.write_text("\n".join([lines[0]] + sel) + "\n")
    return p, len(sel)


SUBS = {1550: [(0,), (1,), (2,), (3,)], 3100: [(0, 1), (2, 3)]}
QN = {}
jobs, keys = [], []
for n_nom, subsets in SUBS.items():
    for si, bk in enumerate(subsets):
        for k in range(10):
            p, n = subset_csv(CSV[("ALL", k)], bk, f"sub{n_nom}_{si}_k{k}")
            jobs.append((p, 20261216)); keys.append((n_nom, si, k, n))
    p0, _ = subset_csv(CSV[("ALL", 0)], subsets[0], f"sub{n_nom}_0_k0")
    for j in range(1, 11):
        jobs.append((p0, 20261216 + j)); keys.append((n_nom, "ctl", j, None))
t = time.time()
sf = fit_many(jobs)
P(f"\n  Q-N: {len(sf)} pipeline fits in {time.time() - t:.0f} s")
for n_nom, subsets in SUBS.items():
    per_sub = {f: [] for f in ("canonical", "alt")}
    for si in range(len(subsets)):
        idx = [i for i, kk in enumerate(keys) if kk[0] == n_nom and kk[1] == si]
        for f in ("canonical", "alt"):
            g = [sf[i][f]["g"] for i in idx]
            ms = float(np.mean([sf[i][f]["s"] for i in idx]))
            per_sub[f].append((sd1(g), ms, float(np.mean([keys[i][3] for i in idx]))))
    cidx = [i for i, kk in enumerate(keys) if kk[0] == n_nom and kk[1] == "ctl"]
    QN[n_nom] = {}
    for f in ("canonical", "alt"):
        sds = [x[0] for x in per_sub[f]]
        pooled = float(np.sqrt(np.mean(np.square(sds))))
        ms = float(np.mean([x[1] for x in per_sub[f]]))
        cs = sd1([sf[i][f]["g"] for i in cidx])
        QN[n_nom][f] = dict(N_mean=float(np.mean([x[2] for x in per_sub[f]])), sd_per_subset=sds, pooled_sd=pooled, mean_sigma_fit=ms, ratio=pooled / ms, fit_only_sd=cs, fit_only_ratio=cs / ms)
        P(f"  N ~ {n_nom:5d} (mean N {QN[n_nom][f]['N_mean']:.0f}; {len(subsets)} disjoint subsets) {f:9s}: SD over ten builds per subset {[round(x, 4) for x in sds]}; pooled {pooled:.4f}; mean sigma_fit {ms:.4f}; SD/sigma_fit {pooled / ms:.3f}; fit-only control SD {cs:.4f} ({cs / ms:.3f})")
for f in ("canonical", "alt"):
    a = QS["ALL"]["per_footing"][f]
    QN.setdefault(6200, {})[f] = dict(N_mean=QS["ALL"]["pairs_mean"], sd_per_subset=[a["sd"]], pooled_sd=a["sd"], mean_sigma_fit=a["mean_sigma_fit"], ratio=a["sd_over_sigma_fit"], fit_only_sd=CTLsd[f], fit_only_ratio=CTLsd[f] / a["mean_sigma_fit"])
    P(f"  N ~  6200 (mean N {QS['ALL']['pairs_mean']:.0f}; the ALL family)                {f:9s}: SD {a['sd']:.4f}; mean sigma_fit {a['mean_sigma_fit']:.4f}; SD/sigma_fit {a['sd_over_sigma_fit']:.3f}; fit-only control SD {CTLsd[f]:.4f} ({CTLsd[f] / a['mean_sigma_fit']:.3f})")
P("\n  Reading rule (declared before the run): the ratio SD/sigma_fit is reported at each N; no extrapolation to DR4's N (about 30,000) is stated as a measurement; ten builds give an SD with a relative error of about 24% per subset.")
SB.assert_builder_frozen("streams end")
P(f"\n{time.time() - T0:.0f} s")
(HERE / "seed_sweep_streams_dr3.out").write_text("\n".join(LOG) + "\n")
json.dump(dict(QS=QS, QN={str(k): v for k, v in QN.items()}, fit_only_control=dict(sd=CTLsd, sd_incl_registered=CTLsd_incl), csv_sha256={f"{a}_{b}": v for (a, b), v in sha.items()},
               uncovered_correlation_ids={f"{fam}_{k}": REP[(fam, k)]["correlations"][0]["n_uncovered"] for fam in ("ALL", "G-only", "EF-only") for k in range(10)}, seconds=round(time.time() - T0, 1)),
          open(HERE / "seed_sweep_streams_dr3.json", "w"), indent=1, default=float)
