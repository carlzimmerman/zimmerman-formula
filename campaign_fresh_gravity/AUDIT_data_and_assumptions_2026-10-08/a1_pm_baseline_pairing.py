#!/usr/bin/env python3
"""AUDIT A1 (read-only): PM growth lanes CFG414/416/419/422-427/439.
Checks that every run is divided by an S0 built from the SAME initial conditions (same seed, NSEED, box, mesh), by
comparing the z_i snapshot P(k) and sigma8 of run and S0 (the phantom is negligible at z = 49, so identical ICs give
ratios ~1 to round-off; a different realisation gives O(10%) scatter per k-bin).  Also re-derives every headline
max|P-1| from the stored JSON and records the margin to the 0.10 cut, and measures the cost of a seed mismatch
(S0 seed 359 vs S0 seed 360) so the size of any pairing error is known."""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
E = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
S359, S360, S361 = "cfg359_work/cfg359_S0_FLAT_canonical_N256.json", "cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N256_seed360.json", \
    "cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N256_seed361.json"
S512 = "cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json"
T4 = "cfg424_work/cfg424_RES_TA_MIXA_MASSCONS_fret1_"
PAIRS = [  # (lane, run, S0 used by the lane's analysis, reported max|P-1|)
    ("CFG414 can 512", "cfg414_work/cfg414_RES_Rc3_MIXA_X0.4_FLAT_canonical_N512.json", S512, 0.080),
    ("CFG414 alt 512", "cfg414_work/cfg414_RES_Rc3_MIXA_X0.4_FLAT_alt_N512.json", S512, 0.0996),
    ("CFG416 can 512", "cfg416_work/cfg416_RES_Rc3_MIXA_SUPPLY_FLAT_canonical_N512.json", S512, 0.0923),
    ("CFG416 alt 512", "cfg416_work/cfg416_RES_Rc3_MIXA_SUPPLY_FLAT_alt_N512.json", S512, 0.1009),
    ("CFG419 DE can 512", "cfg416_work/cfg416_RES_Rc3_MIXA_SUPPLY_DE_canonical_N512.json", S512, 0.0929),
    ("CFG422 359 can", "cfg414_work/cfg414_RES_Rc3_MIXA_X0.4_FLAT_canonical_N256.json", S359, 0.041),
    ("CFG422 359 alt", "cfg414_work/cfg414_RES_Rc3_MIXA_X0.4_FLAT_alt_N256.json", S359, 0.056),
    ("CFG422 360 can", "cfg414_work/cfg414_RES_Rc3_MIXA_X0.4_FLAT_canonical_N256_seed360.json", S360, 0.040),
    ("CFG422 360 alt", "cfg414_work/cfg414_RES_Rc3_MIXA_X0.4_FLAT_alt_N256_seed360.json", S360, 0.056),
    ("CFG422 361 can", "cfg414_work/cfg414_RES_Rc3_MIXA_X0.4_FLAT_canonical_N256_seed361.json", S361, 0.039),
    ("CFG422 361 alt", "cfg414_work/cfg414_RES_Rc3_MIXA_X0.4_FLAT_alt_N256_seed361.json", S361, 0.051),
    ("CFG410 BASE 359 can", "cfg410_work/cfg410_RES_Rc3_MIXA_FLAT_canonical_N256.json", S359, 0.153),
    ("CFG423 P1 Rc3", "cfg423_work/cfg423_RES_Rc3_MIXA_MASSCONS_fret1_FLAT_canonical_N256.json", S359, 0.042),
    ("CFG423 P2 Rc1", "cfg423_work/cfg423_RES_Rc1_MIXA_MASSCONS_fret1_FLAT_canonical_N256.json", S359, 0.005),
    ("CFG424 can", T4 + "FLAT_canonical_N256.json", S359, 0.027),
    ("CFG424 alt", T4 + "FLAT_alt_N256.json", S359, 0.029),
    ("CFG425 R1 360", T4 + "FLAT_canonical_N256_seed360.json", S360, 0.022),
    ("CFG425 R2 361", T4 + "FLAT_canonical_N256_seed361.json", S361, 0.017),
    ("CFG425 R3 512", T4 + "FLAT_canonical_N512.json", S512, 0.033),
    ("CFG426 DE can", T4 + "DE_canonical_N256.json", S359, 0.029),
    ("CFG426 DE alt", T4 + "DE_alt_N256.json", S359, 0.030),
    ("CFG426 alt 360", T4 + "FLAT_alt_N256_seed360.json", S360, 0.025),
    ("CFG426 alt 361", T4 + "FLAT_alt_N256_seed361.json", S361, 0.023),
    ("CFG427 eps half", T4 + "FLAT_canonical_N256_eps0.0385.json", S359, 0.0273),
    ("CFG427 eps dbl", T4 + "FLAT_canonical_N256_eps0.154.json", S359, 0.0273),
    ("CFG427 MIXB", "cfg424_work/cfg424_RES_TA_MIXB_MASSCONS_fret1_FLAT_canonical_N256.json", S359, 0.0262),
    ("CFG427 HOT1", "cfg424_work/cfg424_RES_TA_HOT1_MASSCONS_fret1_FLAT_canonical_N256.json", S359, 0.0311),
    ("CFG439 alt 512", T4 + "FLAT_alt_N512.json", S512, 0.040),
    ("CFG439 DE can 512", T4 + "DE_canonical_N512.json", S512, 0.034),
]
def load(p): return json.load(open(os.path.join(E, p)))
def ratio(s, s0, kmax=1.0):
    k, P = np.array(s["k"]), np.array(s["P"]); m = k <= kmax
    return P[m] / np.interp(k[m], np.array(s0["k"]), np.array(s0["P"]))
out, rows = {}, []
print(f"{'pair':22s} {'zi max|P/P0-1|':>15s} {'zi s8 ratio-1':>14s} {'meta match':>10s} {'z0 max|P-1|':>11s} {'reported':>8s} {'margin to 0.10':>14s}")
for lane, r, s0, rep in PAIRS:
    if not os.path.exists(os.path.join(E, r)): print(f"{lane:22s} MISSING {r}"); continue
    a, b = load(r), load(s0)
    zi = float(np.max(np.abs(ratio(a["snap"]["zi"], b["snap"]["zi"], kmax=99) - 1)))
    s8i = a["snap"]["zi"]["sigma8"] / b["snap"]["zi"]["sigma8"] - 1
    meta = all(a.get(x) == b.get(x) for x in ("np", "mesh", "L", "z_i", "nsteps", "amp"))
    pz = float(np.max(np.abs(ratio(a["snap"]["z0"], b["snap"]["z0"]) - 1)))
    out[lane] = dict(zi_maxdev=zi, zi_s8=s8i, meta_match=meta, z0_pdev=pz, reported=rep, margin=0.10 - pz)
    print(f"{lane:22s} {zi:15.2e} {s8i:14.2e} {str(meta):>10s} {pz:11.4f} {rep:8.4f} {0.10 - pz:+14.4f}")
# cost of a seed mismatch: S0(360)/S0(359) and S0(361)/S0(359) at z0, k<=1
for s in (S360, S361):
    d = float(np.max(np.abs(ratio(load(s)["snap"]["z0"], load(S359)["snap"]["z0"]) - 1)))
    out["seed_mismatch_" + s.split("_")[-1]] = d
    print(f"seed-mismatch cost: S0 {s.split('_')[-1]} / S0 359 at z0: max|P-1| = {d:.3f}")
# is CFG359's S0 (older engine) the same IC as the CFG411+ engines at seed 359? Compare with cfg410 BASE at z_i.
json.dump(out, open(os.path.join(HERE, "a1_pm_baseline_pairing.json"), "w"), indent=1)
