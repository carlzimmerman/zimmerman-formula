#!/usr/bin/env python3
"""ZT6_zstar_sparc_supply: Z-star test Z-T6 (SPARC owned supply vs the census budget), as frozen in Z1 TEST_PLAN (0d1959a4f5).

Criteria: FROZEN_CRITERIA.md (63fbb694c7, committed alone first).  kappa = 1/2 FITTED.  Not "theory closed".
Run:   OMP_NUM_THREADS=1 nice -n 15 python3 zt6_sparc_supply.py [--mutate]
"""
import os, sys, io, json, math, contextlib, resource
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(REPO, "real_research", "data")
CFGD = os.path.join(REPO, "campaign_fresh_gravity")
MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
OUTL = []
RES = dict(lane="ZT6_zstar_sparc_supply", criteria="63fbb694c7", mutate=MUT, checks={})
FOOTS = ("canonical", "alt")
G, MSUN, KPC_S = 6.67430e-11, 1.98847e30, 3.0857e19
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
with contextlib.redirect_stdout(io.StringIO()):
    sys.path.insert(0, CFGD)
    import CFG4_common as C4  # noqa: E402
A0 = {f: float(C4.A0[f]) for f in FOOTS}


def P(s=""):
    print(s, flush=True); OUTL.append(str(s))


def check(key, ok, value):
    RES["checks"][key] = dict(ok=bool(ok), value=value); P(f"{key} {'PASS' if ok else 'FAIL'}  {value}")


def f_req(R, Mb, a0):
    rM = math.sqrt(G * Mb * MSUN / ((100.0 if MUT else 1.0) * a0))
    return 0.5 * (-1 + math.sqrt(1 + 4 * (R / rM) ** 2))


# K5: phantom of a point mass under the a0-line equals f_req M_b
Mt, Rt, a0t = 1e10, 30 * KPC_S, A0["canonical"]
gN = G * Mt * MSUN / Rt ** 2; g = 0.5 * (gN + math.sqrt(gN * gN + 4 * gN * a0t))
k5 = abs((g * Rt ** 2 / G / MSUN - Mt) / Mt - f_req(Rt, Mt, a0t)) < 1e-10
check("K5", k5, f"phantom/M_b {(g * Rt ** 2 / G / MSUN - Mt) / Mt:.10f} vs f_req {f_req(Rt, Mt, a0t):.10f}")

# census (CFG947 verbatim formulas and constants)
OM_B, OM_C = 0.02237, 0.1200; FB = OM_B / (OM_B + OM_C); HE = 0.674
DTA0 = float(json.load(open(os.path.join(CFGD, "CFG654_independent_inputs", "cfg654_delta_ta.json")))["D"][0])
RHOM_H = 0.315 * 2.775e11


def fret_of(lM):
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)


def M_ta(R):
    return (4 * math.pi / 3) * R ** 3 * DTA0 * RHOM_H


def N_census(Mb):
    fn = lambda lR: fret_of(math.log10(M_ta(math.exp(lR)))) * FB * M_ta(math.exp(lR)) / HE - Mb
    R = math.exp(brentq(fn, math.log(1e-6), math.log(1e3), xtol=1e-14, rtol=1e-14))
    fr = fret_of(math.log10(M_ta(R)))
    return (1 - FB) / (fr * FB), fr


n3198, _ = N_census(10 ** 10.6)                       # any M_b in the f_r = 0.10 branch
check("KC", abs(n3198 - 53.64) < 0.01, f"N (f_r 0.10 branch) {n3198:.3f} vs CFG953 53.64")

# SPARC
GALS = []
for fn in sorted(os.listdir(os.path.join(DATA, "sparc_data"))):
    if not fn.endswith("_rotmod.dat"):
        continue
    d = np.genfromtxt(os.path.join(DATA, "sparc_data", fn), comments="#")
    if d.ndim != 2 or d.shape[1] < 6:
        continue
    GALS.append(dict(name=fn[:-11], R=d[:, 0], Vobs=d[:, 1], eV=d[:, 2], Vgas=d[:, 3], Vdisk=d[:, 4], Vbul=d[:, 5]))


def vb2(q, ud, ub):
    return np.sign(q["Vgas"]) * q["Vgas"] ** 2 + ud * q["Vdisk"] ** 2 + ub * q["Vbul"] ** 2


# KP: P4 per-galaxy Upsilon (bulge 1.4 Upsilon) by weighted mse of the isolated law
P4R = {"canonical": 0.054087447879939264, "alt": 0.05371798965550355}
UBEST = {}
okp = True
for f in FOOTS:
    num = den = 0.0; UBEST[f] = {}
    for q in GALS:
        R = q["R"] * KPC_S
        GB = (np.sign(q["Vgas"])[:, None] * q["Vgas"][:, None] ** 2 + UPS[None, :] * q["Vdisk"][:, None] ** 2 + 1.4 * UPS[None, :] * q["Vbul"][:, None] ** 2) * 1e6 / R[:, None]
        GO = (q["Vobs"] * 1e3) ** 2 / R
        OK = (GB > 0) & (GO > 0)[:, None] & (q["Vobs"] > 0)[:, None]
        W = np.where(OK, (1.0 / (np.clip(q["eV"], 1, None) / np.clip(q["Vobs"], 1, None)) ** 2)[:, None], 0.0)
        lgp = np.log10(np.maximum((0.5 + np.sqrt(0.25 + A0[f] / np.maximum(GB, 1e-300))) * GB, 1e-300))
        r = np.where(OK, np.log10(np.where(GO > 0, GO, 1.0))[:, None] - lgp, 0.0)
        mse = (W * r * r).sum(0) / np.maximum(W.sum(0), 1e-300); i = int(np.argmin(mse))
        num += (W[:, i] * r[:, i] ** 2).sum(); den += W[:, i].sum(); UBEST[f][q["name"]] = float(UPS[i])
    okp &= abs(math.sqrt(num / den) - P4R[f]) <= 1e-4
check("KP", okp, "P4 iso_perUps pooled rms reproduced on both footings (per-galaxy Upsilon recovered)")

for f in FOOTS:
    out = {}
    for mode in ("SPS_0.5_0.7", "P4_Upsilon"):
        fr_l, N_l, Mb_l, short_N, short_s = [], [], [], 0, 0
        for q in GALS:
            if mode == "SPS_0.5_0.7":
                v2 = vb2(q, 0.5, 0.7)
            else:
                u = UBEST[f][q["name"]]; v2 = vb2(q, u, 1.4 * u)
            Rl = q["R"][-1] * KPC_S
            Mb = max(v2[-1], 1e-6) * 1e6 * Rl / G / MSUN
            fq = f_req(Rl, Mb, A0[f]); N, _ = N_census(Mb)
            fr_l.append(fq); N_l.append(N); Mb_l.append(Mb)
            short_N += fq > N; short_s += fq > 5.364
        fr_a, N_a, Mb_a = map(np.array, (fr_l, N_l, Mb_l))
        B = float(np.sum(fr_a * Mb_a) / np.sum(N_a * Mb_a))
        out[mode] = dict(B=B, f_req_median=float(np.median(fr_a)), f_req_16_84=[float(v) for v in np.percentile(fr_a, [16, 84])],
                         f_req_max=float(fr_a.max()), n_short_census=int(short_N), n_short_noloss_5364=int(short_s), N=len(fr_a),
                         N_census_median=float(np.median(N_a)))
        P(f"[{f}] {mode}: f_req median {out[mode]['f_req_median']:.2f} (16-84 {out[mode]['f_req_16_84'][0]:.2f}-{out[mode]['f_req_16_84'][1]:.2f}, "
          f"max {out[mode]['f_req_max']:.1f}); census N median {out[mode]['N_census_median']:.1f}; B = {B:.4f}; "
          f"galaxies short vs census {short_N}/{len(fr_a)}, vs no-loss 5.364 {short_s}/{len(fr_a)}")
    out["class"] = "PASS" if out["SPS_0.5_0.7"]["B"] <= 2 else "FAIL"
    RES[f] = out
V = "PASS" if all(RES[f]["class"] == "PASS" for f in FOOTS) else "FAIL"
RES["verdict"] = V
P(f"VERDICT Z-T6: {V} (canonical {RES['canonical']['class']}, alt {RES['alt']['class']})")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
check("KR", rss < 1.0, f"{rss:.2f} GB")
allok = all(v["ok"] for v in RES["checks"].values())
P(f"checks: {'ALL PASS' if allok else 'SOME FAIL'}")
open(os.path.join(HERE, f"zt6_sparc_supply{TAG}.out"), "w").write("\n".join(OUTL) + "\n")
json.dump(RES, open(os.path.join(HERE, f"zt6_sparc_supply_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if allok else 1)
