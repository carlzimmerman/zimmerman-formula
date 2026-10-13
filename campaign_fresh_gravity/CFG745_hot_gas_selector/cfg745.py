"""CFG745: hot-gas selector C = k M_hot. Criteria: FROZEN_CRITERIA.md (4f2fa30ea).
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".
Run:  python3 cfg745.py      (CFG745_MUTATE=1: state-blind C = k M_b; exit 1 iff it fails groups)
"""
import os, sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES); sys.path.insert(0, LANES)
import CFG4_common as C4  # noqa: E402
MUT = os.environ.get("CFG745_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
lines = [__doc__.strip()]
def P_(s): print(s); lines.append(s)
c624 = json.load(open(os.path.join(LANES, "CFG624_no_cold_energy", "cfg624_static_results.json")))["G2"]["rows"]
aud = json.load(open(os.path.join(REPO, "qwen_claude_field_theory", "closure_2026", "cluster_measurement_audit_2026", "results.json")))["rows"]
nu_s = lambda y: 0.5 * (1 + math.sqrt(1 + 4 / y))
FOOT_KEY = {"canonical": "canonical|nu_mono", "alt": "alt|nu_mono"}
SIG = 0.010 / 0.31
CFG580 = {"canonical": {"req": 0.8, "fb": {0.1: 1.86, 0.3: 1.12, 1.0: 0.62}}, "alt": {"req": 0.55, "fb": {0.1: 1.07, 0.3: 0.64, 1.0: 0.36}}}
res, consistent = {}, True
for f in C4.FOOTS:
    rows = c624[FOOT_KEY[f]]["per_cluster"]
    resid = []
    for c in rows:
        ar = [a for a in aud if a["cluster"] == c["name"] and a["footing"] == f and abs(a["r_kpc"] - c["r_kpc"]) < 1]
        y = ar[0]["g_baryon_over_a0"]
        ratio = nu_s(y) / float(C4.nu_mono(np.array([y]))[0])
        resid.append((c["M_hse"] - c["M_NCE"] * ratio) / c["M_b"])
    P_(f"\n{f}: per-cluster resid (simple mu) median {np.median(resid):.3f} (range {min(resid):.2f}-{max(resid):.2f}); n {len(resid)}")
    res[f] = {"resid_median": float(np.median(resid))}
    for fh in (0.85, 0.95):
        fh_eff = 1.0 if MUT else fh
        k = float(np.median(resid)) / fh_eff
        f_grp = 1.0 if MUT else 0.08
        d = {nu: math.log10(1 + k * f_grp / nu) for nu in (1.6, 3.7)}
        okg = [v <= 2 * SIG for v in d.values()]
        h2 = "PASS" if all(okg) else ("TENSION" if any(okg) else "FAIL")
        req = CFG580[f]["req"]; mh = req / k
        allowed = {z: fb * req for z, fb in CFG580[f]["fb"].items()}
        h3 = "NOT EXCLUDED" if any(mh <= a for a in allowed.values()) else "EXCLUDED"
        res[f][str(fh)] = dict(k=k, group_shift=d, H2=h2, M_hot_req_over_Mstar=mh, allowed=allowed, H3=h3)
        consistent &= (h2 != "FAIL") and (h3 == "NOT EXCLUDED")
        P_(f"    f_hot,cl {fh}: k = {k:.3f};  H2 groups shift {d[1.6]:+.3f} (nu 1.6) / {d[3.7]:+.3f} (nu 3.7) dex vs 2 sigma {2 * SIG:.3f}: {h2};  "
           f"H3 early types need M_hot = {mh:.3f} M* vs eROSITA-allowed {', '.join(f'{a:.2f}' for a in allowed.values())} M* (Z 0.1/0.3/1): {h3}")
if MUT:
    fails = all(res[f][str(fh)]["group_shift"][3.7] > 2 * SIG for f in C4.FOOTS for fh in (0.85, 0.95))
    P_(f"\nMUTATE: state-blind selector fails groups at nu 3.7: {fails}"); rc = 1 if fails else 0
else:
    res["verdict"] = "SELECTOR CONSISTENT (two constants; hot gas around early types unmeasured)" if consistent else "SELECTOR INCONSISTENT"
    P_(f"\nVERDICT: {res['verdict']}"); rc = 0
    json.dump(res, open(os.path.join(HERE, "cfg745_results.json"), "w"), indent=1, default=str)
open(os.path.join(HERE, f"cfg745{TAG}.out"), "w").write("\n".join(lines) + "\n"); sys.exit(rc)
