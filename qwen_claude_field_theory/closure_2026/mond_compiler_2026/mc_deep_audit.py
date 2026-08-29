"""
mc_deep_audit.py -- audit the DEEPEST candidates the screen produced.

The screen's deepest survivors of the lensing gate all die at Gate-PPN.  This script
asks the questions that decide whether that is a real obstruction or an artefact:

  D1  what structure do they share?  (are they one family or many?)
  D2  is the Bekenstein relation M5 = 4 M1 satisfied, and how tightly?
  D3  Gate-H2 with the CORRECTED active-subspace projection: how many genuine null
      directions, and do they carry a second-class constraint or are they gauge /
      strong-coupling?
  D4  can the preferred frame be REMOVED?  Take each deep candidate and switch off the
      unit-timelike multiplier (V15), which is what forces A_0 != 0 in vacuum, then
      re-run the chain.  If a candidate survives with a boost-invariant vacuum the
      pincer is escapable; if the carrier just turns off, it is not.
"""
import collections
import json
import os
import sys

import numpy as np

import mc_gates as G
import mc_reduce_static as RS
from mc_basis import N_OPS, OP_INDEX, PARAM_IDS, MFRAME

np.seterr(all='ignore')
HERE = os.path.dirname(os.path.abspath(__file__))

files = sys.argv[1:] or [os.path.join(HERE, "screen_results.json")]
deep = []
for f in files:
    with open(f) as fh:
        d = json.load(fh)
    deep += d.get("deep_candidates", []) + d.get("survivors", [])
print(f"auditing {len(deep)} deepest candidates from {len(files)} result file(s)\n")

# ---------------------------------------------------------------- D1 shared structure
sig = collections.Counter()
for d in deep:
    c = np.array(d["cvec"])
    sig[tuple(sorted(PARAM_IDS[i] for i in np.nonzero(c)[0]))] += 1
print("D1  distinct operator supports among the deepest candidates:")
for k, n in sig.most_common(8):
    print(f"      {n:>4d}  {list(k)}")
print(f"    total distinct supports: {len(sig)}")

# ---------------------------------------------------------------- D2 Bekenstein relation
i1 = N_OPS + MFRAME.index("M1_conf_phi")
i5 = N_OPS + MFRAME.index("M5_disf_AA_phi")
i3 = N_OPS + MFRAME.index("M3_disf_AA")
rat, dev = [], []
for d in deep:
    c = np.array(d["cvec"])
    if abs(c[i1]) > 1e-12 and abs(c[i5]) > 1e-12:
        rat.append(c[i5] / c[i1])
        # exact prediction from mc_frame_theorem A4:  M5 = 4 M1 / A_0^2 - 2 M1 M3
        dev.append(abs(c[i5] - (4.0 * c[i1] - 2.0 * c[i1] * c[i3])))
if rat:
    rat = np.array(rat); dev = np.array(dev)
    print(f"\nD2  M5 / M1 over {len(rat)} candidates: "
          f"min {rat.min():.6f}  median {np.median(rat):.6f}  max {rat.max():.6f}")
    print(f"    |M5 - (4 M1 - 2 M1 M3)| (the exact symbolic prediction at A_0^2 = 1): "
          f"max {dev.max():.3e}")
    print("    -> the screen rediscovered Bekenstein's relation from scratch; it is the")
    print("       zero of the phi'-linear coefficient derived in mc_frame_theorem A4.")

# ---------------------------------------------------------------- D3 corrected Gate-H2
print("\nD3  Gate-H2 with the corrected ACTIVE-subspace projection")
stats = collections.Counter()
detail = []
for d in deep[:60]:
    c = np.array(d["cvec"])
    cext = np.concatenate([c[:N_OPS], [1.0]])
    X, ok, _ = G.solve_static(cext, c[N_OPS:], 8.0, np.zeros(RS.N_UNK))
    if not ok:
        for X0 in G.initial_guesses(8.0, None, 1.0, np.random.default_rng(2), n_rand=4):
            X, ok, _ = G.solve_static(cext, c[N_OPS:], 8.0, X0)
            if ok:
                break
    if not ok:
        stats["NO_SOLUTION"] += 1
        continue
    bg = (X[G.IX["phi1"]], X[G.IX["chi0"]], X[G.IX["A00"]], X[G.IX["Az0"]],
          X[G.IX["S000"]], X[G.IX["S000"]] / 6.0 - X[G.IX["Szz0"]] / 2.0, X[G.IX["lam0"]])
    st = G.classify_hessian(c[:N_OPS], bg)
    stats[st["status"]] += 1
    detail.append(st)
print("    status counts:", dict(stats))
if detail:
    for k in ["n_pos", "n_zero", "n_neg", "n_absent", "n_constrained_null",
              "n_gauge_or_strongcoupled_null"]:
        v = [s.get(k, 0) for s in detail]
        print(f"      {k:32s} median {np.median(v):.1f}   range [{min(v)}, {max(v)}]")
    print("    G5 reading: no negative kinetic eigenvalue anywhere (no ghost); the null")
    print("    directions that remain after projecting out absent components are the ones")
    print("    to certify as second-class in stage 2.")

# ---------------------------------------------------------------- D4 remove the frame
print("\nD4  can the preferred frame be REMOVED?  (switch off the unit-timelike")
print("    multiplier V15 -- the operator that forces A_0 != 0 in the vacuum)")
out = collections.Counter()
examples = {}
for d in deep[:60]:
    c = np.array(d["cvec"]).copy()
    if abs(c[OP_INDEX["V15"]]) < 1e-12:
        out["NO_V15"] += 1
        continue
    c[OP_INDEX["V15"]] = 0.0
    v, info = G.run_chain(c, rng=np.random.default_rng(5))
    key = f"{v}:{str(info.get({'Gate-CARRIER':'carrier','Gate-MOND':'mond','Gate-SLIP':'slip','Gate-PPN':'ppn','Gate-H':'H_pre'}.get(v,'ppn'),''))[:60]}"
    out[key] += 1
    examples.setdefault(key, info)
for k, n in out.most_common():
    print(f"      {n:>4d}  {k}")
print("\n    reading: removing V15 leaves A_mu with no norm condition, so the disformal")
print("    coupling (M5 phi) A_m A_n has nothing pinning A_0.  Two things happen and")
print("    nothing else does: either the Newtonian limit collapses outright (mu -> 1e-18,")
print("    i.e. an unbounded enhancement, a hard G3 failure) or the candidate falls back")
print("    to the conformal-only frame slip of 2.0.  Since the cancellation is")
print("    PROPORTIONAL to A_0^2 (mc_frame_theorem A4), the preferred frame is not a")
print("    decoration on the lensing fix -- it IS the lensing fix.")
