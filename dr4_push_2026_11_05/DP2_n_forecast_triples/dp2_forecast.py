#!/usr/bin/env python3
"""DP2 Part 1: forecast of the DR4 frozen-cut pair count from the DR3 extract caches (FROZEN_CRITERIA.md section 1).

The registered stage G of catalog_builder/build_catalog.py is re-run from its own functions, imported read-only, on the cached
DR3 stage-F pairs, with the frozen DR4 error scaling (sigma_pm x 0.372, sigma_plx x 0.718). INFORMATION ONLY (owner D8).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -B dp2_forecast.py          -> dp2_forecast.out / dp2_forecast_results.json
     ... python3 -B dp2_forecast.py --mutate                           -> dp2_forecast_MUTATE.out / _results.json
kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import sys
sys.dont_write_bytecode = True
import os, json, csv, socket, hashlib, resource, time

def _no_net(*a, **k):
    raise RuntimeError("network access forbidden in DP2")
socket.socket.connect = _no_net
socket.create_connection = _no_net

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PREP = os.path.join(ROOT, "prep_2026", "gaia_dr4_prep")
CB = os.path.join(PREP, "catalog_builder")
for p in (PREP, CB):
    sys.path.insert(0, p)
import build_catalog as BC            # noqa: E402  read-only
import wide_binary_pipeline as W      # noqa: E402  read-only

EXT = os.path.join(ROOT, "real_research", "data", "widebinaries", "dr3_extract")
MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
OUT = []
RSS_MAX_MB = 4000.0
FROZEN = ["prep_2026/gaia_dr4_prep/wide_binary_pipeline.py", "prep_2026/gaia_dr4_prep/catalog_builder/build_catalog.py",
          "prep_2026/gaia_dr4_prep/catalog_builder/build_report_dr3.json",
          "real_research/data/widebinaries/dr3_extract/wide_binaries_dr3.csv"]


def P(s=""):
    OUT.append(s); print(s, flush=True)


def rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6   # darwin: bytes


def guard(w):
    if rss() > RSS_MAX_MB:
        sys.stderr.write(f"RSS guard {rss():.0f} MB at {w}\n"); os._exit(3)


def hashes():
    return {f: hashlib.sha256(open(os.path.join(ROOT, f), "rb").read()).hexdigest() for f in FROZEN}


h0 = hashes()
t0 = time.time()
P("DP2 Part 1: DR4 N forecast from DR3 caches (INFORMATION ONLY; owner D8). kappa = 1/2 FITTED.")
P(f"frozen pipeline sha256 {h0[FROZEN[0]][:16]}, build_catalog {h0[FROZEN[1]][:16]}, reference CSV {h0[FROZEN[3]][:16]}")
za = np.load(os.path.join(EXT, "stage_A.npz"))
S0 = {k: za[k] for k in za.files if k != "bp_rp"}
del za
F = dict(np.load(os.path.join(EXT, "stage_F.npz")))
AV = dict(np.load(os.path.join(EXT, "AV_sfd98.npz")))
c1, c2 = dict(np.load(os.path.join(EXT, "stage_G_corr.npz"))), dict(np.load(os.path.join(EXT, "stage_G_corr_elbadry.npz")))
sid = np.concatenate([c1["source_id"], c2["source_id"]])
u, iu = np.unique(sid, return_index=True)
CORR = {"source_id": u}
for k in ("parallax_pmra_corr", "parallax_pmdec_corr"):
    CORR[k] = np.concatenate([c1[k], c2[k]])[iu]
P(f"loaded: {len(S0['ra']):,} sources, {len(F['a']):,} stage-F pairs, corr caches cover {len(u):,} stars; peak RSS {rss():.0f} MB")
ref_rows = list(csv.DictReader(open(os.path.join(EXT, "wide_binaries_dr3.csv"))))
REF = set((int(r["source_id1"]), int(r["source_id2"])) for r in ref_rows)
REF_FLOW = json.load(open(os.path.join(CB, "build_report_dr3.json")))["cut_flow"]


def corr_for(ids):
    """Correlations for the given stars; uncovered stars get 0 (counted). Never fetched."""
    ids = np.unique(ids)
    have = np.isin(ids, CORR["source_id"])
    if have.all():
        return CORR, 0
    miss = ids[~have]
    out = {"source_id": np.concatenate([CORR["source_id"], miss])}
    for k in ("parallax_pmra_corr", "parallax_pmdec_corr"):
        out[k] = np.concatenate([CORR[k], np.zeros(len(miss))])
    return out, int(len(miss))


def emulate(fpm, fplx, shrink, seed=BC.SEED, label=""):
    """Registered stage G with errors scaled (fpm, fplx). shrink: pull pair parallaxes to their weighted mean by fplx."""
    S = dict(S0)
    if fpm != 1.0:
        S["pmra_error"] = S0["pmra_error"] * fpm
        S["pmdec_error"] = S0["pmdec_error"] * fpm
    if fplx != 1.0:
        S["parallax_error"] = S0["parallax_error"] * fplx
    if shrink:
        a, b = F["a"], F["b"]
        assert len(np.unique(np.concatenate([a, b]))) == 2 * len(a), "a star sits in two stage-F pairs"
        w1, w2 = S0["parallax_error"][a] ** -2, S0["parallax_error"][b] ** -2
        pw = (w1 * S0["parallax"][a] + w2 * S0["parallax"][b]) / (w1 + w2)
        plx = S0["parallax"].copy()
        plx[a] = pw + fplx * (S0["parallax"][a] - pw)
        plx[b] = pw + fplx * (S0["parallax"][b] - pw)
        S["parallax"] = plx
    extra = {"third": np.zeros(len(F["a"]), bool)}
    pre, _, _ = BC.frozen_cuts(S, F["a"], F["b"], F["R"], extra)
    idx = np.flatnonzero(pre)
    extra["third"][idx] = BC.third_star_flags(S, F["a"][idx], F["b"][idx])
    guard("third")
    pre2, _, tab0 = BC.frozen_cuts(S, F["a"], F["b"], F["R"], extra)
    idx2 = np.flatnonzero(pre2)
    corr, nmiss = corr_for(np.concatenate([S["source_id"][F["a"][idx2]], S["source_id"][F["b"][idx2]]]))
    sig_vt = BC.vt_error_mc(S, F["a"][idx2], F["b"][idx2], F["th"][idx2], corr, seed=seed)
    vc0 = np.sqrt(W.G * (tab0["M1_msun"][idx2] + tab0["M2_msun"][idx2]) * W.MSUN / (tab0["sep_kAU"][idx2] * 1e3 * W.AU)) / 1e3
    vt0 = tab0["v_perp_kms"][idx2] / vc0
    ok = np.zeros(len(F["a"]), bool)
    ok[idx2] = sig_vt <= 0.1 * np.maximum(1.0, vt0 / 2)
    extra["vt_err_ok"] = ok
    extra["AV_ok"] = (AV["av"][F["a"]] < 0.5) & (AV["av"][F["b"]] < 0.5)
    keep, flow, table = BC.frozen_cuts(S, F["a"], F["b"], F["R"], extra)
    pairs = set(zip(table["source_id1"][keep].astype(np.int64).tolist(), table["source_id2"][keep].astype(np.int64).tolist()))
    guard("emulate")
    d = dict(label=label, fpm=fpm, fplx=fplx, shrink=shrink, seed=int(seed), N=int(keep.sum()), flow=flow, n_corr_missing=nmiss,
             vt_pass_frac=float(ok[idx2].mean()), n_vt_input=int(len(idx2)), median_sig_vt=float(np.median(sig_vt)))
    P(f"  [{label}] fpm {fpm:.4f} fplx {fplx:.4f} shrink {shrink} seed {seed}: N = {d['N']:,}; cut-15 input {len(idx2):,}, pass {d['vt_pass_frac']:.3f}, "
      f"median sigma(vt) {d['median_sig_vt']:.4f}; corr-missing stars {nmiss}  ({time.time() - t0:.0f} s, RSS {rss():.0f} MB)")
    P("      flow: " + "; ".join(f"{n} {k:,}" for n, k in flow))
    return d, pairs


RES = dict(lane="DP2 Part 1", mode="MUTATE" if MUT else "main", information_only=True, scenarios={}, checks={})
FPM, FPLX = W.PM_FAC_DR4, W.PLX_FAC_DR4
P(f"frozen DR4 factors (wide_binary_pipeline): sigma_pm x {FPM:.4f}, sigma_plx x {FPLX:.4f}")

if MUT:
    d, _ = emulate(1 / FPM, 1 / FPLX, True, label="MUTATE inverted factors")
    RES["scenarios"]["MUTATE"] = d
    bites = d["N"] <= 5900
    RES["checks"]["K4_mutate_bites"] = bites
    P(f"K4 MUTATE (worse-than-DR3 errors) N = {d['N']:,} <= 5,900: {'BITES' if bites else 'DOES NOT BITE: Part 1 NOT DIAGNOSTIC'}")
else:
    d0, p0 = emulate(1.0, 1.0, False, label="S0 DR3 registered")
    k1 = d0["N"] == 6210 and p0 == REF
    k3 = [list(x) for x in d0["flow"]] == [list(x) for x in REF_FLOW]
    d0b, p0b = emulate(1.0, 1.0, True, label="S0b identity of emulation path")
    k2 = p0b == p0
    P(f"K1 S0 N = 6,210 and pair set == reference CSV: {'PASS' if k1 else 'FAIL'}")
    P(f"K2 S0b (shrink path, factors 1) == S0 pair set: {'PASS' if k2 else 'FAIL'}")
    P(f"K3 S0 cut flow == build_report_dr3.json: {'PASS' if k3 else 'FAIL'}")
    d1, p1 = emulate(FPM, FPLX, False, label="S1 errors-only DR4")
    d2, p2 = emulate(FPM, FPLX, True, label="S2 noise-shrunk DR4 (central)")
    jit = [emulate(FPM, FPLX, True, seed=BC.SEED + j, label=f"S2 seed +{j}")[0]["N"] for j in (1, 2)]
    RES["scenarios"] = dict(S0=d0, S0b=d0b, S1=d1, S2=d2)
    RES["S2_seed_N"] = [d2["N"]] + jit
    RES["checks"].update(K1=k1, K2=k2, K3=k3)
    RES["S2_overlap_with_S0"] = dict(kept_from_dr3=len(p2 & p0), new=len(p2 - p0), lost=len(p0 - p2))
    P(f"S2 vs S0: kept {len(p2 & p0):,} of the DR3 pairs, lost {len(p0 - p2):,}, new {len(p2 - p0):,}; S2 N over 3 MC seeds {RES['S2_seed_N']}")
h1 = hashes()
RES["checks"]["K5_frozen_unchanged"] = h0 == h1
P(f"K5 frozen files unchanged: {'PASS' if h0 == h1 else 'FAIL'}; peak RSS {rss():.0f} MB; {time.time() - t0:.0f} s")
json.dump(RES, open(os.path.join(HERE, f"dp2_forecast{TAG}_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"dp2_forecast{TAG}.out"), "w").write("\n".join(OUT) + "\n")
