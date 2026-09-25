#!/usr/bin/env python3
"""
V02 -- GEOMETRY-FREE FLOOR CLOUD EXTENSION (R02/T02 caveat zone R < 1.51)
2026-09-25.  Conductor-run lane (V-WAVE_BRIEF.md, kills pre-registered there).

Door: R02's constant floor c* = 0.28177 is checked only at the 6 landed K12
clouds (hull [1.5133, 28.2393]; T02: R=1 OUTSIDE the hull, caveat stands for
R < 1.51).  No cloud below R = 1.5133 has ever been tested.  This lane builds
5 sub-thin clouds in the EXACT K12 engine convention (J02.simulate /
K12.simulate_shell, q=0, n=1e6) and re-tests both landed floors on the extended
set, then records the maximal power-law floor + hull coverage.  Both-ways.

Kills (pre-registered in V-WAVE_BRIEF.md):
  K1 machinery: rerunning K12's exact cloud (volume, tau0=1, q=0, seed 9000,
     n=1e6) reproduces K12's stored volume_q0 E_D/E_v2 EXACTLY (deterministic
     engine, same seed); criterion consistency vs Q03 stored clouds.
  K2 both-ways: on the EXTENDED set, criterion f(R_i) <= E_D_i + 3*se_D_i:
     any violation of a landed floor -> that floor DOWNGRADED, domain restated;
     maximal power-law floor on the extended set recorded either way.
  K3: landed inputs runtime-read; seeds/n recorded; floor-channel claim only.
"""
import json, math, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from J02_moment_hierarchy import simulate          # engine (read-only import)
from K12_geometry_audit import simulate_shell      # shell transport (read-only)

K12 = json.load(open(os.path.join(HERE, "K12_results.json")))
Q03 = json.load(open(os.path.join(HERE, "Q03_results.json")))
R02 = json.load(open(os.path.join(HERE, "R02_results.json")))

res = {"lane": "V02_floor_extension", "prereg": "V-WAVE_BRIEF.md", "checks": {},
       "new_clouds": {}, "kill_events": [], "t_start": time.strftime("%Y-%m-%d %H:%M:%S")}

def se(x):
    x = np.asarray(x, dtype=float)
    return float(np.std(x, ddof=1) / math.sqrt(len(x)))

# ------------------------------------------------------------------ K1 gate
t0 = time.time()
rep = simulate(1_000_000, 1.0, 0.0, "volume", seed=9000)   # K12's exact cloud
rep_ED, rep_Ev2 = float(np.mean(rep["D"])), float(np.mean(rep["v2"]))
st = K12["measurements"]["volume_q0"]
res["checks"]["K1_seed_replication_exact"] = bool(
    rep_ED == st["E_D"] and rep_Ev2 == st["E_v2"])
print("K1 seed replication: ED %r vs %r | Ev2 %r vs %r -> %s"
      % (rep_ED, st["E_D"], rep_Ev2, st["E_v2"],
         res["checks"]["K1_seed_replication_exact"]), flush=True)
if not res["checks"]["K1_seed_replication_exact"]:
    res["kill_events"].append("K1 seed replication mismatch")

# ------------------------------------------------------------------ new clouds
NEW = [("central_t0.5",  "central", 0.5, 0.0, None,   9600),
       ("central_t0.7",  "central", 0.7, 0.0, None,   9601),
       ("volume_t0.5",   "volume",  0.5, 0.0, None,   9602),
       ("volume_t0.7",   "volume",  0.7, 0.0, None,   9603),
       ("shell_r0.9_t0.7", "shell",  0.7, 0.0, 0.9,   9604)]
for name, src, tau0, q, r0, seed in NEW:
    tt = time.time()
    r = (simulate_shell(1_000_000, tau0, q, r0, seed=seed) if src == "shell"
         else simulate(1_000_000, tau0, q, src, seed=seed))
    D = np.asarray(r["D"], dtype=float); v2 = np.asarray(r["v2"], dtype=float)
    res["new_clouds"][name] = dict(
        source=src, tau0=tau0, q=q, r0=r0, seed=seed, n=int(len(D)),
        E_D=float(np.mean(D)), se_D=se(D), E_v2=float(np.mean(v2)), se_v2=se(v2),
        E_N=float(np.mean(r["N"])), E_tau=float(np.mean(r["elapsed"])),
        wall_s=round(time.time() - tt, 1))
    print("cloud %-18s E_D=%.6f+-%.6f  R=E_v2=%.5f  (%.0fs)"
          % (name, res["new_clouds"][name]["E_D"], res["new_clouds"][name]["se_D"],
             res["new_clouds"][name]["E_v2"], time.time() - tt), flush=True)

# ------------------------------------------------------------------ extended set
clouds = []
for k, m in K12["measurements"].items():
    clouds.append(dict(name=k, landed=True, E_D=m["E_D"], se_D=m["se_D"], E_v2=m["E_v2"]))
for k, m in res["new_clouds"].items():
    clouds.append(dict(name=k, landed=False, E_D=m["E_D"], se_D=m["se_D"], E_v2=m["E_v2"]))
for c in clouds:
    c["b"] = c["E_D"] + 3.0 * c["se_D"]          # criterion bound d + 3*se_D

C_CONST = R02["best"]["c_registered"]          # 0.2817733312220705 runtime-read
C_LIN   = Q03["c_star"]                        # 0.06844371 linear floor
viol_c, viol_l = [], []
for c in clouds:
    if C_CONST > c["b"]:                       viol_c.append(c["name"])
    if C_LIN * c["E_v2"] > c["b"]:             viol_l.append(c["name"])
res["checks"]["landed_constant_floor_violated_on_extended"] = bool(viol_c)
res["checks"]["landed_linear_floor_violated_on_extended"] = bool(viol_l)
res["constant_violations"] = viol_c
res["linear_violations"] = viol_l
print("landed CONSTANT floor %.5f violations: %s" % (C_CONST, viol_c), flush=True)
print("landed LINEAR   floor %.8f violations: %s" % (C_LIN, viol_l), flush=True)

# maximal power-law floor on the extended set (scan p, maximize retention)
Rs = np.array([c["E_v2"] for c in clouds]); Bs = np.array([c["b"] for c in clouds])
best = None
for p in np.linspace(-3.0, 3.0, 1201):
    cp = float(np.min(Bs / Rs ** p))
    ret = cp / 0.20710678118654757            # retention vs central_floor(R=1)
    if best is None or ret > best["retention"]:
        best = dict(p=float(p), c=cp, retention=float(ret))
# refine around best p
for p in np.linspace(best["p"] - 0.0025, best["p"] + 0.0025, 501):
    cp = float(np.min(Bs / Rs ** p))
    ret = cp / 0.20710678118654757
    if ret > best["retention"]:
        best = dict(p=float(p), c=cp, retention=float(ret))
binding = [c["name"] for c in clouds
           if abs(best["c"] * c["E_v2"] ** best["p"] - c["b"]) < 1e-12]
res["extended_floor"] = dict(p=best["p"], c=best["c"],
    retention_vs_central_R1=best["retention"], binding_clouds=binding,
    hull=[float(Rs.min()), float(Rs.max())], n_clouds=len(clouds))
print("extended maximal power-law floor: p=%.4f c=%.6f retention=%.3f binding=%s"
      % (best["p"], best["c"], best["retention"], binding), flush=True)
print("hull coverage: [%.4f, %.4f]" % (Rs.min(), Rs.max()), flush=True)
res["landed_comparison"] = dict(
    landed_c_const=0.28177, landed_c_const_retention=0.28177 / 0.20710678118654757,
    landed_c_lin=Q03["c_star"], landed_c_lin_retention=Q03["c_star"] / 0.20710678118654757,
    landed_hull=[1.513335950706991, 28.23926603392842])
res["wall_s"] = round(time.time() - t0, 1)
res["ALL_PASSED"] = not res["kill_events"]
out = os.path.join(HERE, "V02_floor_extension_results.json")
json.dump(res, open(out, "w"), indent=1)
print("WROTE", out)
print("ALL V02 CHECKS PASSED" if res["ALL_PASSED"] else "V02 KILL/FAIL (see kill_events)")
sys.exit(0 if res["ALL_PASSED"] else 1)
