#!/usr/bin/env python3
"""sweep_depth.py -- run the SM-target sweep on an already-built depth-D value set.

Why this exists: grind.run_depth() couples the build to the sweep, and its skeleton provider calls
DN._skeleton_value_nodes lazily -- which at depth 10 means the 8.019e9-sequence b_s=6 layer, ~25 h.
The layer is already cached (parallel_skeleton_layer.py, validated to reproduce DN's value set exactly),
so this driver prepopulates the provider from that cache and calls grind's OWN sweep verbatim.
Nothing about the gate, the FDR multiplicity or the hit predicate is reimplemented.
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, '.')
import numpy as np
import grind as G
import parallel_skeleton_layer as PSL
import exhaust_depthN_forced as DN
from exhaust import build_alphabet
from exhaust_parallel import sm_target_keys

D = int(sys.argv[1]) if len(sys.argv) > 1 else 10
ddir = G.RESULTS / f"depth_{D}"
alpha = build_alphabet()
print(f"[sweep d{D}] loading values ...", flush=True)
values = G._load_values(ddir)
print(f"[sweep d{D}] {len(values):,} distinct values", flush=True)

# prepopulate the provider from the validated cache so it never rebuilds a layer
cache = {}
for (b_s, g_s) in DN.budget_splits(D):
    lay = PSL.load_layer(alpha, b_s)
    if lay is None:
        lay = DN._skeleton_value_nodes(alpha, b_s)
        print(f"  b_s={b_s}: rebuilt (uncached) {len(lay):,}", flush=True)
    else:
        print(f"  b_s={b_s}: CACHED {len(lay):,}", flush=True)
    cache[b_s] = lay
provider = G._make_skeleton_provider(alpha, cache)
meta = json.loads((ddir / "build_meta.json").read_text())

targets = sm_target_keys()          # holdout EXCLUDED -- this is a search
print(f"[sweep d{D}] {len(targets)} targets (holdout excluded): {targets}", flush=True)
(ddir / "targets").mkdir(exist_ok=True)
reports, t0 = [], time.time()
for i, k in enumerate(targets, 1):
    r = G.sweep_target_streamed(alpha, k, values, ddir, provider, meta, verbose=True)
    reports.append(r)
    print(f"  [{i}/{len(targets)}] {k}: hits={r.get('n_hits')} "
          f"CERT={r.get('n_certified')} RELAB={r.get('n_relabeled')}", flush=True)
agg = G._aggregate_reports(reports)
agg.update(depth=D, wall_s=round(time.time()-t0, 1), n_targets=len(targets),
           build=meta.get("build"), mem_cap_gb=G.GRIND_MEM_CAP_GB)
(ddir / "VERDICT.json").write_text(json.dumps(agg, indent=2, default=str))
print("\n" + "="*90)
print(f"DEPTH {D} SWEEP COMPLETE  ({agg['wall_s']}s)")
for kk in ("n_hits", "n_certified", "n_relabeled", "tightest_target", "tightest_rel"):
    if kk in agg: print(f"  {kk} = {agg[kk]}")
cert = agg.get("n_certified", 0)
print("\n  " + ("*** CANDIDATE(S) SURVIVED THE GATE -- assess before believing (read BITS_RULE.py) ***"
                if cert else "CLEAN NULL: zero gate-passing candidates at depth "+str(D)+" (EXHAUSTIVE)"))
print("="*90)
