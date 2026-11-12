#!/usr/bin/env python3
"""EUC4R post-unblinding comparison with EUC4.

Written AFTER euc4r.py and its outputs were committed (dfb9cd3a7e). It imports EUC1's euc1.py and this lane's euc4r.py
as modules (neither main() runs) and reads EUC4's euc4_results.json and euc4_per_lens.csv, to trace every difference
between the two grades. It changes no number of the blind run. kappa = 1/2 FITTED.

    python3 -I euc4r_compare.py
"""
import importlib.util
import json
import math
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
EUC1_PY = os.path.join(ROOT, "EUC1_eclipse_saturation_ceiling", "euc1.py")
EUC4_DIR = os.path.join(ROOT, "EUC4_wide_lenses")
LOG = []


def say(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    LOG.append(s)


def load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


E = load_mod("euc1", EUC1_PY)
R = load_mod("euc4r", os.path.join(HERE, "euc4r.py"))
EXACT_GAMMAINCINV = R.gammaincinv
FT = ("canonical", "alt")
LAWS = ("S", "B")
OUT = {}

# ------------------------------------------------------------------ samples, built by EUC1's own loader
rows, _ = E.load(R.DATA)
Bm, _ = E.select(rows, ("B",))
Am, _ = E.select(rows, ("A",))
bins = {
    "W_B": [r for r in Bm if r["tE"] >= 1.7],
    "secondary_B": [r for r in Bm if 1.3 <= r["tE"] < 1.7],
    "complement_B": [r for r in Bm if r["tE"] < 1.0],
}
mine_csv = pd.read_csv(os.path.join(HERE, "euc4r_lenses.csv"))
for k, smp in bins.items():
    ids_e = {r["id"] for r in smp}
    ids_m = set(mine_csv.loc[mine_csv[k], "unique_identifier"])
    say(f"{k}: EUC1-loader N {len(smp)}, EUC4R N {len(ids_m)}, same identifiers: {ids_e == ids_m}")
edge = {x: sum(1 for r in Bm if r["tE"] == x) for x in (1.0, 1.3, 1.7)}
say("grade-B valid lenses with theta_E exactly at a bin edge:", edge)
OUT["edge_counts"] = {str(k): v for k, v in edge.items()}


# ------------------------------------------------------------------ per-lens b under each machinery
def b_variant(smp, law, a0, msun, bn, dist, engine):
    z, te, re, n, lm = (E.arr(smp, k) for k in ("z", "tE", "te", "n", "lm"))
    if dist == "mine":
        sig, dl = R.sigma_cr_inf(z)
    else:
        dl = E.EUCLID.DA(z)
        sig = E.EUCLID.sigcr(z, E.ZS_INF)
    RE = te * R.ARCSEC * dl
    Re = re * R.ARCSEC * dl
    Ms = 10.0 ** lm * msun
    Mmin = math.pi * RE ** 2 * sig
    if engine == "euc1":
        return E.Engine(RE, Re, n, Ms).solve_b(Mmin, a0, law)
    R.gammaincinv = EXACT_GAMMAINCINV if bn == "exact" else (lambda a, q: E.b_ser(np.asarray(a) / 2.0))
    try:
        return R.Lenses(RE, Re, n, Ms).solve_b(Mmin, a0, law)
    finally:
        R.gammaincinv = EXACT_GAMMAINCINV


steps = [
    ("s0 EUC4R as run", dict(msun=R.MSUN, bn="exact", dist="mine", engine="mine")),
    ("s1 + M_sun 1.98847e30", dict(msun=E.MSUN, bn="exact", dist="mine", engine="mine")),
    ("s2 + series b_n", dict(msun=E.MSUN, bn="series", dist="mine", engine="mine")),
    ("s3 + EUC1 distance grid", dict(msun=E.MSUN, bn="series", dist="euc1", engine="mine")),
    ("s4 + EUC1 400-node engine", dict(msun=E.MSUN, bn="series", dist="euc1", engine="euc1")),
]
say("\n[per-lens b: EUC4R machinery stepped toward EUC1's; max |b(step) - b(EUC1 build)| over all grade-B bins, "
    "both laws, both footings, in dex]")
bE, bstep = {}, {s: {} for s, _ in steps}
for k, smp in bins.items():
    for law in LAWS:
        for ft in FT:
            a0 = R.FOOTINGS[ft]
            eng, z, RE, Re, n, lm = E.build(smp)
            bE[(k, law, ft)] = eng.solve_b(math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF), a0, law)
            for s, kw in steps:
                bstep[s][(k, law, ft)] = b_variant(smp, law, a0, **kw)
OUT["steps"] = {}
for s, _ in steps:
    d = np.concatenate([bstep[s][key] - bE[key] for key in bE])
    flips = sum(int(np.sum((bstep[s][key] > 0.25) != (bE[key] > 0.25))) for key in bE)
    say(f"  {s:28s}: max |db| {np.max(np.abs(d)):.2e}, median db {np.median(d):+.2e}, b > 0.25 flips {flips}")
    OUT["steps"][s] = dict(max_abs=float(np.max(np.abs(d))), median=float(np.median(d)), flips=flips)
say(f"  log10(1.98847/1.98841) = {math.log10(E.MSUN / R.MSUN):.3e} dex (the M_sun constant alone)")
flip_rows = []
for key in bE:
    m = (bstep["s0 EUC4R as run"][key] > 0.25) != (bE[key] > 0.25)
    for i in np.flatnonzero(m):
        r = bins[key[0]][i]
        flip_rows.append(dict(sample=key[0], law=key[1], footing=key[2], id=r["id"],
                              b_euc4r=float(bstep["s0 EUC4R as run"][key][i]), b_euc1=float(bE[key][i])))
say("  lenses whose b > 0.25 indicator differs between the two machineries:", flip_rows if flip_rows else "none")
OUT["indicator_flips"] = flip_rows

# ------------------------------------------------------------------ the 316 wide lenses of EUC4's per-lens file
e4 = pd.read_csv(os.path.join(EUC4_DIR, "euc4_per_lens.csv"))
wide_ids = {r["id"]: (r, g) for g, smp in (("A", Am), ("B", Bm)) for r in smp if r["tE"] >= 1.7}
say(f"\n[EUC4's per-lens file: {len(e4)} wide lenses; grade-A and grade-B wide lenses by EUC1's loader: {len(wide_ids)}]")
for ft in FT:
    ids = list(e4.unique_identifier)
    smp = [wide_ids[i][0] for i in ids]
    b0 = b_variant(smp, "S", R.FOOTINGS[ft], **steps[0][1])
    d = b0 - e4[f"b_inf_S_{ft}"].to_numpy()
    say(f"  law S {ft}: EUC4R minus EUC4 file (4-decimal rounding): max |db| {np.max(np.abs(d)):.2e}, "
        f"median {np.median(d):+.2e}")

# ------------------------------------------------------------------ bootstrap intervals: generator order
e4res = json.load(open(os.path.join(EUC4_DIR, "euc4_results.json")))["partA"]
e4names = {"W_B": "W_B: theta_E >= 1.7 arcsec (primary)", "secondary_B": "secondary: 1.3 <= theta_E < 1.7",
           "complement_B": "complement: theta_E < 1.0"}
mine_json = json.load(open(os.path.join(HERE, "euc4r.json")))["samples"]


def iv(st):
    return [st["f25"], st["f25_lo"], st["f25_hi"]]


say("\n[f25 intervals: EUC4 as published; EUC4R as run (fresh generator per statistic); EUC1's stats() fed EUC1-build b "
    "with ONE generator shared in EUC4's order (W_B, secondary, complement; S then B; canonical then alt)]")
rng_shared = np.random.default_rng(E.SEED)
OUT["bootstrap"] = {}
all_match = True
for k in bins:
    for law in LAWS:
        for ft in FT:
            pub = e4res[e4names[k]][f"{law}_{ft}"]
            seq = E.stats(bE[(k, law, ft)], rng_shared)
            fresh_e = E.stats(bE[(k, law, ft)], np.random.default_rng(E.SEED))
            mine = mine_json[k][f"{law}_{ft}"]["default_rng"]["f25"]
            same_seq = all(abs(a - b) < 1e-12 for a, b in zip(iv(seq), iv(pub)))
            same_fresh = all(abs(a - b) < 1e-12 for a, b in zip(iv(fresh_e), mine))
            all_match &= same_seq
            say(f"  {k:12s} {law} {ft:9s}: EUC4 {pub['f25']:.4f} [{pub['f25_lo']:.4f}, {pub['f25_hi']:.4f}]  "
                f"EUC4R {mine[0]:.4f} [{mine[1]:.4f}, {mine[2]:.4f}]  shared-stream repro "
                f"{'EXACT' if same_seq else 'differs'}; EUC1 stats() with a fresh generator = EUC4R "
                f"{'EXACT' if same_fresh else 'differs'}")
            OUT["bootstrap"][f"{k}_{law}_{ft}"] = dict(euc4=iv(pub), euc4r=mine, shared_stream_exact=same_seq,
                                                       fresh_generator_equals_euc4r=same_fresh)
say(f"  every EUC4 interval reproduced exactly by the shared-stream order: {all_match}")
OUT["shared_stream_reproduces_all"] = bool(all_match)

# ------------------------------------------------------------------ z_s = 1100 versus a literal infinity (W_B, law S)
say("\n[sensitivity, not a criteria ambiguity in the text (z_s = 1100 is written): W_B law S with z_s = 1e6]")
smp = bins["W_B"]
z, te, re, n, lm = (E.arr(smp, k) for k in ("z", "tE", "te", "n", "lm"))
for zs in (1100.0, 1e6):
    sig, dl = R.sigma_cr_inf(z, zs)
    RE, Re = te * R.ARCSEC * dl, re * R.ARCSEC * dl
    L = R.Lenses(RE, Re, n, 10.0 ** lm * R.MSUN)
    vals = []
    for ft in FT:
        b = L.solve_b(math.pi * RE ** 2 * sig, R.FOOTINGS[ft], "S")
        st = R.boot_stats(b)
        vals.append(st["f25"])
    say(f"  z_s = {zs:g}: f25 canonical {vals[0][0]:.4f} [{vals[0][1]:.4f}, {vals[0][2]:.4f}], "
        f"alt {vals[1][0]:.4f} [{vals[1][1]:.4f}, {vals[1][2]:.4f}]")
    OUT[f"W_B_S_zs_{zs:g}"] = vals

with open(os.path.join(HERE, "euc4r_compare.json"), "w") as f:
    json.dump(OUT, f, indent=1)
with open(os.path.join(HERE, "euc4r_compare.out"), "w") as f:
    f.write("\n".join(LOG) + "\n")
