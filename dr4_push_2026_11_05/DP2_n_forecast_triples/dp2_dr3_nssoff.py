#!/usr/bin/env python3
"""DP2 Part 2.3: decomposition of the DR3 NSS-off probe (+0.075 canonical, D2 A2 table) into NSS-flagged pairs and the
reseeded vtilde-error Monte Carlo (FROZEN_CRITERIA.md section 2.3). DR3 data, NON-SCORING, INFORMATION ONLY (owner D8).
Frozen estimator (wide_binary_pipeline.bin_medians / fit_gamma) and CFG943's frozen model medians, read-only.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 -B dp2_dr3_nssoff.py   -> dp2_dr3_nssoff.out / _results.json
kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import sys
sys.dont_write_bytecode = True
import os, csv, json, socket, hashlib

def _no_net(*a, **k):
    raise RuntimeError("network access forbidden in DP2")
socket.socket.connect = _no_net
socket.create_connection = _no_net

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "prep_2026", "gaia_dr4_prep"))
import wide_binary_pipeline as W     # noqa: E402  read-only

OUT = []
def P(s=""):
    OUT.append(s); print(s, flush=True)

EXT = os.path.join(ROOT, "real_research/data/widebinaries/dr3_extract")
REF = os.path.join(EXT, "wide_binaries_dr3.csv")
VAR = os.path.join(ROOT, "campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/wide_binaries_dr3_variant.csv")
NPZ = os.path.join(ROOT, "campaign_fresh_gravity/CFG943_dr4_readiness/cfg943_model_medians.npz")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
h0 = {p: sha(p) for p in (REF, VAR, NPZ, os.path.join(ROOT, "prep_2026/gaia_dr4_prep/wide_binary_pipeline.py"))}
z = np.load(NPZ)
MODS = {"canonical": (z["can_med"], z["can_sig"]), "alt": (z["alt_med"], z["alt_sig"])}
A0S = {"canonical": W.A0_CAN, "alt": W.A0_ALT}

za = np.load(os.path.join(EXT, "stage_A.npz"))
nss_ids = set(za["source_id"][za["non_single_star"] > 0].tolist())
del za


def rows(p):
    return list(csv.DictReader(open(p)))


def key(r):
    return (int(r["source_id1"]), int(r["source_id2"]))


ref = rows(REF)
var = [r for r in rows(VAR) if float(r["sep_kAU"]) < 30.0]
isn = lambda r: int(r["source_id1"]) in nss_ids or int(r["source_id2"]) in nss_ids
var_nss = [r for r in var if isn(r)]
ref_keys, var_keys = set(map(key, ref)), set(map(key, var))
SETS = {
    "A reference (6,210)": ref,
    "B variant s<30 (NSS-off probe)": var,
    "C = B minus NSS-flagged": [r for r in var if not isn(r)],
    "D = A plus NSS-flagged of B": ref + [r for r in var_nss if key(r) not in ref_keys],
}
P("DP2 2.3: DR3 NSS-off probe decomposition (DR3 data, NON-SCORING, INFORMATION ONLY). kappa = 1/2 FITTED.")
P(f"reference sha256 {h0[REF][:16]}, variant sha256 {h0[VAR][:16]}, model npz {h0[NPZ][:16]}")
P(f"variant s<30: {len(var):,}; NSS-flagged in variant: {len(var_nss)}; NSS-flagged in reference: {sum(isn(r) for r in ref)}; "
  f"variant-only pairs not NSS-flagged (reseed flips in): {len([r for r in var if key(r) not in ref_keys and not isn(r)])}; "
  f"reference pairs missing from variant (reseed flips out): {len(ref_keys - var_keys)}")


def arrays(rs):
    s = np.array([float(r["sep_kAU"]) for r in rs]) * W.KAU
    vp = np.array([float(r["v_perp_kms"]) for r in rs]) * 1e3
    Mt = np.array([float(r["M1_msun"]) + float(r["M2_msun"]) for r in rs])
    return W.G * Mt * W.MSUN / s ** 2, vp / np.sqrt(W.G * Mt * W.MSUN / s)


NB = 30
RES = dict(lane="DP2 2.3", information_only=True, non_scoring=True, n_boot_seeds=NB, sets={}, checks={})
for name, rs in SETS.items():
    gN, vt = arrays(rs)
    RES["sets"][name] = dict(N=len(rs))
    for foot in ("canonical", "alt"):
        gs = []
        for j in range(NB):
            med, sig, cnt = W.bin_medians(np.log10(gN / A0S[foot]), vt, boot=200, rng=np.random.default_rng([2026, 1105, 23, j]))
            g, sg, chi2, nb, kap = W.fit_gamma(med, sig, MODS[foot], W.GRID)
            gs.append((g, sg))
        g = np.array(gs)
        RES["sets"][name][foot] = dict(mean=float(g[:, 0].mean()), sd=float(g[:, 0].std(ddof=1)), sg=float(g[:, 1].mean()))
        P(f"  {foot:9s} {name:34s} N {len(rs):5d}: gamma-hat {g[:, 0].mean():.4f} (bootstrap-seed sd {g[:, 0].std(ddof=1):.4f}), sigma_fit {g[:, 1].mean():.4f}")
for foot in ("canonical", "alt"):
    m = {k[0]: RES["sets"][k][foot]["mean"] for k in SETS}
    d = dict(probe_B_minus_A=m["B"] - m["A"], contamination_B_minus_C=m["B"] - m["C"],
             contamination_D_minus_A=m["D"] - m["A"], reseed_C_minus_A=m["C"] - m["A"])
    RES[f"decomposition_{foot}"] = d
    P(f"  {foot}: probe B-A {d['probe_B_minus_A']:+.4f} = NSS pairs (B-C) {d['contamination_B_minus_C']:+.4f} + reseed (C-A) {d['reseed_C_minus_A']:+.4f}; "
      f"NSS pairs added to A (D-A) {d['contamination_D_minus_A']:+.4f}")
ka = abs(RES["sets"]["A reference (6,210)"]["canonical"]["mean"] - 1.0750) <= 0.03
kb = abs(RES["sets"]["B variant s<30 (NSS-off probe)"]["canonical"]["mean"] - 1.1500) <= 0.03
RES["checks"].update(A_known=ka, B_known=kb, frozen_unchanged=all(sha(p) == v for p, v in h0.items()))
P(f"known answers: A canonical vs 1.0750 (tol 0.03) {'PASS' if ka else 'FAIL'}; B canonical vs 1.1500 (tol 0.03) {'PASS' if kb else 'FAIL'}; "
  f"inputs unchanged {'PASS' if RES['checks']['frozen_unchanged'] else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, "dp2_dr3_nssoff_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "dp2_dr3_nssoff.out"), "w").write("\n".join(OUT) + "\n")
