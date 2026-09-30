#!/usr/bin/env python3
"""DR4-READY-1, Amendment 18 tooling: M1-M4 of SEED_SWEEP_MARGINAL_FROZEN.md (3829f98f3), committed before this script existed.  Where does the build-to-build pair flipping come from?
DR3 numbers are code-path tests, never results (Amendment 7(e)); NON-SCORING; no verdict words.  OFFLINE.  NEW file; needs seed_sweep_streams_dr3.py's CSVs (ext/seed_streams/ALL_k*.csv, G-only_k*.csv).
Run:  python3 prep_2026/gaia_dr4_prep/dr4_ready_1/seed_sweep_marginal_dr3.py"""
import sys
sys.dont_write_bytecode = True
import json, time
from collections import Counter
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dry_run_driver as D
import seeded_build as SB
import seed_sweep as SS

D.init(False)
B = SB.import_builder()
SB.assert_builder_frozen("marginal start")
ext = D.extract_dir("dr3", "primary")
sd_dir = ext / "seed_streams"
T0 = time.time()


def fpath(fam, k):
    """the family's k-th final table (k = 0 is shared by the families and was written once, as ALL_k0)."""
    return sd_dir / f"{'ALL' if k == 0 else fam}_k{k}.csv"

LOG = []


def P(s=""):
    print(s, flush=True); LOG.append(s)


P("SEED SWEEP MARGINAL PAIRS (DR3 PRIMARY base, N_SHIFT = 30; DR3 numbers are code-path tests, never results)")
# ---------------------------------------------------------------- M1 inclusion frequency
res = {}
P("\nM1 inclusion frequency over the ten final tables of a family")
for fam in ("ALL", "G-only"):
    sets = [SS.pair_set(fpath(fam, k)) for k in range(10)]
    cnt = Counter(p for s in sets for p in s)
    hist = Counter(cnt.values())
    core, marg = sum(1 for c in cnt.values() if c == 10), sum(1 for c in cnt.values() if 0 < c < 10)
    res[f"M1_{fam}"] = dict(core=core, marginal=marg, ever=len(cnt), histogram={int(k): int(v) for k, v in sorted(hist.items())})
    P(f"  {fam:7s}: core (in all ten) {core:,d}; marginal (in 1 to 9) {marg}; ever {len(cnt):,d}; marginal / mean final size {marg / np.mean([len(s) for s in sets]):.3f}; in-exactly-c-builds histogram {dict(sorted(hist.items()))}")
# ---------------------------------------------------------------- M2 membership against flips
S = dict(np.load(ext / "stage_A.npz"))
sid = S["source_id"]


def candidates(F):
    extra = {"third": np.zeros(len(F["a"]), bool)}
    pre, _, _ = B.frozen_cuts(S, F["a"], F["b"], F["R"], extra)
    idx = np.flatnonzero(pre)
    return {tuple(sorted((int(sid[F["a"][i]]), int(sid[F["b"][i]])))) for i in idx}


Fs = [dict(np.load(ext / f"wp2_gamma_{k}" / "stage_F.npz")) for k in range(10)]
C = [candidates(F) for F in Fs]
fin = [SS.pair_set(fpath("ALL", k)) for k in range(10)]
P("\nM2 cut-13 candidates (pass every cut except A_V, vtilde error and 13) and final flips, build k against k = 0")
rows = []
for k in range(1, 10):
    cin, cout = len(C[k] - C[0]), len(C[0] - C[k])
    fin_, fout = len(fin[k] - fin[0]), len(fin[0] - fin[k])
    rows.append((k, len(C[k]), cin, cout, fout, fin_))
    P(f"  k = {k}: candidates {len(C[k]):,d}; in k only {cin}, in k = 0 only {cout}; FINAL pairs in k = 0 only {fout}, in k only {fin_}")
res["M2"] = dict(rows=rows, mean_membership_difference=float(np.mean([r[2] + r[3] for r in rows])), mean_final_flips=float(np.mean([r[4] + r[5] for r in rows])))
P(f"  mean candidate-membership difference (both ways) {res['M2']['mean_membership_difference']:.1f} against mean final-flip count (both ways) {res['M2']['mean_final_flips']:.1f}")
# ---------------------------------------------------------------- M3 stream alignment
F0 = Fs[0]
n = 2000
a, b, th = F0["a"][:n], F0["b"][:n], F0["th"][:n]
corr = D.offline_correlations(ext, "primary", [])("dr3", np.concatenate([sid[a], sid[b]]), None)
base = np.asarray(B.vt_error_mc(S, a, b, th, corr))
P("\nM3 stream alignment: vt_error_mc on a 2,000-pair slice")
res["M3"] = {}
for pos in (0, 1000, 1999):
    m = np.ones(n, bool); m[pos] = False
    r2 = np.asarray(B.vt_error_mc(S, a[m], b[m], th[m], corr))
    d = np.abs(base[m] - r2)
    res["M3"][f"remove_{pos}"] = dict(changed=int((d > 0).sum()), of=int(m.sum()), median_rel=float(np.median(d / np.maximum(base[m], 1e-12))))
    P(f"  one pair removed at position {pos:4d}: sigma_vt changed for {int((d > 0).sum())} of {int(m.sum())} other pairs; median relative change {np.median(d / np.maximum(base[m], 1e-12)):.3f}")
perm = np.arange(n)[::-1]
r3 = np.asarray(B.vt_error_mc(S, a[perm], b[perm], th[perm], corr))[np.argsort(perm)]
d = np.abs(base - r3)
res["M3"]["reversed"] = dict(changed=int((d > 0).sum()), of=n, median_rel=float(np.median(d / np.maximum(base, 1e-12))))
P(f"  the same pairs in reversed order: sigma_vt changed for {int((d > 0).sum())} of {n} pairs; median relative change {np.median(d / np.maximum(base, 1e-12)):.3f} (a pair's sigma_vt depends on its position in the array and on the array's membership)")
# ---------------------------------------------------------------- M4 threshold margin
extra = {"third": np.zeros(len(F0["a"]), bool)}
pre, _, _ = B.frozen_cuts(S, F0["a"], F0["b"], F0["R"], extra)
idx = np.flatnonzero(pre)
extra["third"][idx] = B.third_star_flags(S, F0["a"][idx], F0["b"][idx])
pre2, _, tab0 = B.frozen_cuts(S, F0["a"], F0["b"], F0["R"], extra)
idx2 = np.flatnonzero(pre2)
corr2 = D.offline_correlations(ext, "primary", [])("dr3", np.concatenate([sid[F0["a"][idx2]], sid[F0["b"][idx2]]]), None)
from wide_binary_pipeline import G as GN, MSUN, AU
vc0 = np.sqrt(GN * (tab0["M1_msun"][idx2] + tab0["M2_msun"][idx2]) * MSUN / (tab0["sep_kAU"][idx2] * 1e3 * AU)) / 1e3
thr = 0.1 * np.maximum(1.0, (tab0["v_perp_kms"][idx2] / vc0) / 2)
sig = np.array([np.asarray(B.vt_error_mc(S, F0["a"][idx2], F0["b"][idx2], F0["th"][idx2], corr2, seed=B.SEED + k)) for k in range(10)])
r = sig / thr
z = B.av_sfd98(S, ext / "AV_sfd98.npz")
avok = (z["av"][F0["a"][idx2]] < 0.5) & (z["av"][F0["b"][idx2]] < 0.5)
pas = (r <= 1.0)
pfrac = pas.mean(axis=0)
relsd = sig.std(axis=0, ddof=1) / sig.mean(axis=0)
marg = (pfrac > 0) & (pfrac < 1) & avok
pred = float(np.sum((pfrac * (1 - pfrac))[avok]))
obs = float(np.mean([(len(fin_g0 - fin_gk) + len(fin_gk - fin_g0)) / 2 for fin_g0, fin_gk in [(SS.pair_set(fpath("G-only", 0)), SS.pair_set(fpath("G-only", k))) for k in range(1, 10)]]))
res["M4"] = dict(n_pairs_in_mc=int(len(idx2)), median_rel_scatter=float(np.median(relsd)), expected_rel_se=float(1 / np.sqrt(2 * 211)), n_marginal=int(marg.sum()), predicted_one_way_flips=pred, observed_g_only_one_way_flips=obs,
                 marginal_r_range=[float(np.min(r.mean(axis=0)[marg])), float(np.max(r.mean(axis=0)[marg]))])
P(f"\nM4 threshold margin: {len(idx2):,d} pairs enter stage G's MC; ten seeds SEED + k (k = 0..9) on the extract's own stage F")
P(f"  median relative scatter of sigma_vt across the ten seeds {np.median(relsd):.3f} (Gaussian expectation {1 / np.sqrt(2 * 211):.3f})")
P(f"  pairs passing the vtilde-error cut in some seeds and failing in others (and A_V ok): {int(marg.sum())}; their mean r = sigma_vt / threshold ranges {res['M4']['marginal_r_range'][0]:.3f} to {res['M4']['marginal_r_range'][1]:.3f}")
P(f"  model: sum over pairs of p (1 - p), p = the pass fraction over the ten seeds = {pred:.1f} predicted one-way flips between two independent draws; observed G-only one-way flips (mean over k = 1..9) {obs:.1f}")
SB.assert_builder_frozen("marginal end")
P(f"\n{time.time() - T0:.0f} s")
(HERE / "seed_sweep_marginal_dr3.out").write_text("\n".join(LOG) + "\n")
json.dump(res, open(HERE / "seed_sweep_marginal_dr3.json", "w"), indent=1, default=float)
