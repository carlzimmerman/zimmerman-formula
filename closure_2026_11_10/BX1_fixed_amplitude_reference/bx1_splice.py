#!/usr/bin/env python3
"""BX1 splice files and the reported comparison (FROZEN_CRITERIA.md 21e1c07e9a, sections 5 and 9).
Writes, in KL1's load200 layout (snap.zi / z1 / z0.5 / z0: k, P, D, sigma8), only from runs that finished and passed KA2 (b):
  bx1_splice_pairA_N512.json        (pA + pAi) / 2           graded
  bx1_splice_runA_N512_noinv.json   pA alone (MB2: the twin replaced by the same run)
  bx1_splice_pairB_N512.json        (pB + pBi) / 2           reported
  bx1_splice_pairsAB_N512.json      mean of the four         reported
  bx1_splice_pairA_N256.json, bx1_splice_pairB_N256.json    256^3 pairs (sigma_g fallback, reported)
  bx1_splice_KA5_cfg411.json        CFG411's own spectra through this writer (KA5)
Reported, never graded: the pair mean against CFG411, CFG424, the 100 Mpc/h box raw and R1-corrected (CO2's R1 rule with the
engine's P_lin), on the box's bins below k 0.5, at z 0, 0.5, 1, error = |PbarA - PbarB| / (sqrt(2) Pbar) (512^3 B if present, else
256^3, marked); and P_512 / P_256 for pair A below k 0.5.
  python3 bx1_splice.py     -> the splice files, bx1_compare.json, bx1_compare.out
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math, glob, importlib.util
os.environ["CFG596_RELIEF"] = "0"; os.environ["CFG596_THREADS"] = "1"; sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data")); W = os.path.join(EXT, "bx1_work")
_sp = importlib.util.spec_from_file_location("bx1_pm_lib", os.path.join(HERE, "bx1_pm.py")); ENG = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(ENG)
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
KA = json.load(open(os.path.join(HERE, "bx1_ka.json")))["KA"] if os.path.exists(os.path.join(HERE, "bx1_ka.json")) else {}
ZK = ("zi", "z1", "z0.5", "z0")
def run(job):
    f = glob.glob(os.path.join(W, job, "bx1_*.json"))
    if not f: return None
    J = json.load(open(f[0]))
    if "z0" not in J["snap"]: return None
    if job.startswith("p") and not KA.get(f"KA2_{job}", {}).get("pass_", False): P(f"  {job}: KA2 (b) not passed or not graded -> not used"); return None
    return J
def write(fn, runs, src):
    k = runs[0]["snap"]["z0"]["k"]
    for J in runs: assert J["snap"]["z0"]["k"] == k
    snap = {z: dict(k=runs[0]["snap"][z]["k"], P=np.mean([J["snap"][z]["P"] for J in runs], axis=0).tolist(), D=runs[0]["snap"][z]["D"],
                    sigma8=[J["snap"][z]["sigma8"] for J in runs]) for z in ZK}
    json.dump(dict(lane="BX1", criteria="21e1c07e9a", note="kappa = 1/2 FITTED; not theory closed; adopts nothing", source=src, snap=snap), open(os.path.join(HERE, fn), "w"))
    P(f"  wrote {fn} from {src}")
    return snap
J = {j: run(j) for j in ("pA", "pAi", "pB", "pBi", "fA", "fAi", "fB", "fBi")}
S = {}
if J["pA"] and J["pAi"]: S["A"] = write("bx1_splice_pairA_N512.json", [J["pA"], J["pAi"]], [J["pA"]["tag"], J["pAi"]["tag"]])
if J["pA"]: S["Asingle"] = write("bx1_splice_runA_N512_noinv.json", [J["pA"]], [J["pA"]["tag"]])
if J["pB"] and J["pBi"]: S["B"] = write("bx1_splice_pairB_N512.json", [J["pB"], J["pBi"]], [J["pB"]["tag"], J["pBi"]["tag"]])
if "A" in S and "B" in S: S["AB"] = write("bx1_splice_pairsAB_N512.json", [J[x] for x in ("pA", "pAi", "pB", "pBi")], [J[x]["tag"] for x in ("pA", "pAi", "pB", "pBi")])
if J["fA"] and J["fAi"]: S["A256"] = write("bx1_splice_pairA_N256.json", [J["fA"], J["fAi"]], [J["fA"]["tag"], J["fAi"]["tag"]])
if J["fB"] and J["fBi"]: S["B256"] = write("bx1_splice_pairB_N256.json", [J["fB"], J["fBi"]], [J["fB"]["tag"], J["fBi"]["tag"]])
C411 = json.load(open(os.path.join(EXT, "cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json"))); C424 = json.load(open(os.path.join(EXT, "cfg424_work", "cfg424_S0_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512_seed360.json")))
write("bx1_splice_KA5_cfg411.json", [C411], ["CFG411 " + C411["tag"]])

# ------------------------------------------------------------------ reported comparison
RES = dict(lane="BX1", part="reported comparison (never graded)", criteria="21e1c07e9a", note="kappa = 1/2 FITTED; not theory closed", rows={})
if "A" in S:
    C596 = json.load(open(glob.glob(os.path.join(EXT, "cfg596_work", "P0", "cfg596_*.json"))[0]))["snap"]; K = np.array(C596["z0"]["k"]); m = K < 0.5
    r = np.array(C596["zi"]["P"]) / (C596["zi"]["D"] ** 2 * ENG.P_lin0(K)); w = np.clip(1 - np.log(np.maximum(K, 0.3) / 0.3) / math.log(1.0 / 0.3), 0, 1)
    def on(snap, z):
        k2 = np.array(snap["z0"]["k"]); return np.exp(np.interp(np.log(K), np.log(k2), np.log(np.array(snap[z]["P"]))))
    eS, etag = (S["B"], "512^3 pair B") if "B" in S else ((S["B256"], "256^3 pairs A / B (low resolution)") if "B256" in S else (None, "none"))
    eA = S["A"] if "B" in S else S.get("A256")
    P(f"Pair A (512^3, seed 7101 fixed + inverted) against the record on the 100 Mpc/h box's bins below k 0.5; error = |PbarA - PbarB| / (sqrt 2 Pbar) from {etag}")
    for z in ("z1", "z0.5", "z0"):
        pa = on(S["A"], z); err = (np.abs(on(eA, z) - on(eS, z)) / (math.sqrt(2) * 0.5 * (on(eA, z) + on(eS, z)))) if eS is not None else np.full(len(K), np.nan)
        lin = pa / (S["A"][z]["D"] ** 2 * ENG.P_lin0(K))
        row = dict(k=K[m].tolist(), err=err[m].tolist(), over_CFG411=(pa / on(C411["snap"], z))[m].tolist(), over_CFG424=(pa / on(C424["snap"], z))[m].tolist(),
                   over_L100_raw=(pa / np.array(C596[z]["P"]))[m].tolist(), over_L100_R1=(pa / (np.array(C596[z]["P"]) / r ** w))[m].tolist(), over_linear=lin[m].tolist())
        RES["rows"][z] = row
        P(f"  {z}:  k      " + " ".join(f"{x:7.3f}" for x in K[m]))
        for nm in ("over_CFG411", "over_CFG424", "over_L100_raw", "over_L100_R1", "over_linear", "err"):
            P(f"       {nm:14s}" + " ".join(f"{x:7.3f}" for x in row[nm]))
    if "A256" in S:
        k2 = np.array(S["A"]["z0"]["k"]); m2 = k2 < 0.5; RES["resolution_512_over_256"] = {}
        P("P_512 / P_256, pair A (shared modes), L200 bins below k 0.5:  k " + " ".join(f"{x:.3f}" for x in k2[m2]))
        for z in ("z1", "z0.5", "z0"):
            n2 = min(len(S["A"][z]["P"]), len(S["A256"][z]["P"]))     # same bin edges (n + 0.5) kf; the 256^3 run stops at its own Nyquist
            assert np.allclose(np.array(S["A"][z]["k"])[:n2][m2[:n2]], np.array(S["A256"][z]["k"])[:n2][m2[:n2]], rtol=1e-3)
            q = (np.array(S["A"][z]["P"])[:n2] / np.array(S["A256"][z]["P"])[:n2])[m2[:n2]]; RES["resolution_512_over_256"][z] = dict(k=k2[:n2][m2[:n2]].tolist(), ratio=q.tolist())
            P(f"       {z:5s} " + " ".join(f"{x:.3f}" for x in q))
json.dump(RES, open(os.path.join(HERE, "bx1_compare.json"), "w"), indent=1)
open(os.path.join(HERE, "bx1_compare.out"), "w").write("\n".join(OUT) + "\n")
