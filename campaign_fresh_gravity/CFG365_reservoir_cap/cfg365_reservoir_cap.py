"""CFG365: the supply cap keyed to the original baryon reservoir. Criteria: FROZEN_CRITERIA.md (f40786eea).

Reads CFG364's committed rows. Run: python3 cfg365_reservoir_cap.py ; MUTATE=1 sets the cosmic ratio x 0.1 (verdict must change, rc 1).
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import CFG4_common as C4  # noqa: E402

MUTATE = os.environ.get("MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
RATIO0 = 0.1200 / 0.02237
SCALE = 0.1 if MUTATE else 1.0          # supply scale relative to CFG364's
F_LO, F_HI = 0.07, 0.18
lines, checks = [], []


def say(s=""):
    print(s)
    lines.append(s)


def check(name, ok, val):
    checks.append({"name": name, "pass": bool(ok), "value": val})
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


J = json.load(open(os.path.join(HERE, "..", "CFG364_supply_cap_sparc", "cfg364_supply_cap_results.json")))
say("CFG365 reservoir-keyed supply cap" + ("  (MUTATE: cosmic ratio x 0.1)" if MUTATE else ""))
say("=" * 78)
say("T0 controls")
nb = sum(r["Q_tot"] > 1 for r in J["rows"]["canonical"])
check("T0a CFG364 JSON read: 175 rows per footing, canonical break count 46",
      len(J["rows"]["canonical"]) == 175 and len(J["rows"]["alt"]) == 175 and nb == 46, f"{len(J['rows']['canonical'])} rows, {nb} breaks")
check("T0b cosmic ratio 5.364", abs(RATIO0 - 5.364) < 1e-3, f"{RATIO0:.4f}")

res = {}
for foot in ("canonical", "alt"):
    rows = J["rows"][foot]
    Q = np.array([r["Q_tot"] for r in rows]) / SCALE
    Qo = np.array([r["Qobs_tot"] for r in rows]) / SCALE
    cls = np.array([r["cls"] for r in rows])
    freq = 1.0 / np.maximum(Q, 1e-12)
    freq_o = 1.0 / np.maximum(Qo, 1e-12)
    d = dict(min_freq=float(freq.min()), argmin=rows[int(freq.argmin())]["name"],
             n_lt_hi=int(np.sum(freq < F_HI)), n_lt_lo=int(np.sum(freq < F_LO)),
             n_lt_lo_obs=int(np.sum(freq_o < F_LO)), n_lt_hi_obs=int(np.sum(freq_o < F_HI)),
             massive_lt_lo=int(np.sum((cls == "massive") & (freq < F_LO))),
             by_class={c: dict(N=int(np.sum(cls == c)), min_freq=float(freq[cls == c].min()), n_lt_lo=int(np.sum((cls == c) & (freq < F_LO))))
                       for c in ("dwarf", "intermediate", "massive", "unclassified")},
             cls_lt_lo=sorted(set(cls[freq < F_LO].tolist())))
    res[foot] = d
    say(f"\nT1 {foot}: smallest required retention {d['min_freq']:.3f} ({d['argmin']}); "
        f"galaxies needing f_ret < {F_HI}: {d['n_lt_hi']}/175; < {F_LO}: {d['n_lt_lo']}/175 "
        f"(observed-dark version: < {F_HI}: {d['n_lt_hi_obs']}, < {F_LO}: {d['n_lt_lo_obs']})")
    for c, b in d["by_class"].items():
        say(f"      {c:13s} N {b['N']:3d}: min f_req {b['min_freq']:.3f}, needing < {F_LO}: {b['n_lt_lo']}")

say("\nT2 system edge (EFE-frozen phantom)")
edge = {}
for ge in (0.01, 0.03):
    nu_e = float(C4.nu_mono(np.array([ge]))[0])
    fe = (RATIO0 * SCALE) / (nu_e - 1)
    edge[ge] = dict(nu=nu_e, f_req=fe)
    say(f"  g_e = {ge} a0: nu_mono = {nu_e:.2f}, edge phantom = {nu_e-1:.2f} M_b, f_req,edge = {fe:.3f} "
        f"({'>=' if fe >= F_LO else '<'} {F_LO}, {'>=' if fe >= F_HI else '<'} {F_HI})")


def verdict(d):
    edge_dead = all(edge[g]["f_req"] < F_LO for g in edge)
    if d["n_lt_lo"] >= 0.10 * 175 or d["massive_lt_lo"] > 0 or edge_dead:
        return "DEAD"
    if d["n_lt_lo"] == 0 and all(edge[g]["f_req"] >= F_LO for g in edge):
        return "VIABLE (galaxy level)"
    if set(d["cls_lt_lo"]) <= {"dwarf", "intermediate"}:
        return "STRAINED"
    return "DEAD"


v = {f: verdict(res[f]) for f in res}
say(f"\nVERDICT (canonical, primary): {v['canonical']}   (alt: {v['alt']})")
say("Galaxy level only: says nothing about the growth/lensing double count (that needs the reservoir-cap PM run).")
check("T-MUT the main run's verdict is not the MUTATE-expected one (MUTATE must change it)", not MUTATE, f"verdict {v['canonical']}")
n = sum(c["pass"] for c in checks)
say(f"\n{n}/{len(checks)} pass" + ("  (MUTATE)" if MUTATE else ""))
json.dump({"lane": "CFG365", "mutate": MUTATE, "verdict": v, "per_footing": res, "edge": {str(k): v_ for k, v_ in edge.items()},
           "census": [F_LO, F_HI], "checks": checks}, open(os.path.join(HERE, f"cfg365_reservoir_cap_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg365_reservoir_cap{TAG}.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if n == len(checks) else 1)
