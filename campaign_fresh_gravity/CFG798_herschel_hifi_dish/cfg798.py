"""CFG798 -- reach of an archival Herschel/HIFI dish-antenna search from the counted hours.  Criteria: FROZEN_CRITERIA.md.
Input: cfg798_matches.csv (from cfg798_query.py).  Seconds, numpy + stdlib.  CFG798_MUTATE=1: rho -> 0 (separate output).
kappa = 1/2 FITTED; not theory closed.  T_DSB, S, B, duty factor provisional.
"""
import csv, json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG798_MUTATE") == "1"
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


c, kB, eV, MSUN, PC = 2.99792458e8, 1.380649e-23, 1.602176634e-19, 1.989e30, 3.0857e16
rho = 0.0 if MUT else 0.01 * MSUN / PC ** 3
A_GEO, B = 9.6, 1.1e6                     # m^2 (3.5 m primary); WBS noise bandwidth max(0.3, 1.1) MHz
S_LIST, TDSB_LIST = (10.0, 50.0, 1000.0), (80.0, 150.0)
E_CAN = 2.240e-3 * eV                     # J, canonical photon energy

rows = list(csv.DictReader(open(os.path.join(HERE, "cfg798_matches.csv"))))
hours = {}
for key in ("541.7", "595.5"):
    for t in "AB":
        hours[(key, t)] = float(np.sum([float(r["t_int_h"]) for r in rows if r["target_GHz"] == key and r["tier"] == t]))
    hours[(key, "A+B")] = hours[(key, "A")] + hours[(key, "B")]

P("CFG798  Herschel/HIFI archival dish-antenna reach" + ("  [MUTATE rho=0]" if MUT else ""))
# K1: S=1, A=10 m^2, eps=1e-12, no 2/3 -> ARGON03 4.4e7 photons/day
k1_rate = (1e-12) ** 2 * (0.01 * MSUN / PC ** 3) * c ** 3 * 10.0 / E_CAN * 86400
k1 = abs(k1_rate / 4.4e7 - 1) < 0.05
P(f"  K1 rate {k1_rate:.3e}/day vs 4.4e7: {'PASS' if k1 else 'FAIL'}")


def eps_min(t_h, S, Tdsb):
    if t_h <= 0:
        return float("inf")
    Pc = (2 / 3) * rho * c ** 3 * A_GEO / S                 # W per eps^2 (total, both pols)
    sig = kB * (2 * Tdsb) * np.sqrt(B / (t_h * 3600))       # per-pol radiometer noise, T_SSB = 2 T_DSB
    snr_per_eps2 = (Pc / 2) / sig * np.sqrt(2)              # H+V combined
    return float(np.sqrt(5 / snr_per_eps2)) if snr_per_eps2 > 0 else float("inf")


R = {"lane": "CFG798", "mutate": MUT, "K1": bool(k1), "hours": {f"{k}|{t}": v for (k, t), v in hours.items()}, "reach": {}}
P("\n  target  tier  t_int[h]   eps_min(5sig)  S=10 / S=50 / S=1000   (T_DSB 80 K | 150 K)")
for key in ("541.7", "595.5"):
    for t in ("A", "B", "A+B"):
        th = hours[(key, t)]
        cells = []
        for Td in TDSB_LIST:
            e = [eps_min(th, S, Td) for S in S_LIST]
            R["reach"][f"{key}|{t}|T{Td:.0f}"] = dict(zip([f"S{S:.0f}" for S in S_LIST], e))
            cells.append(" / ".join(f"{x:.1e}" for x in e))
        P(f"  {key}  {t:4s} {th:7.2f}    {cells[0]}  |  {cells[1]}")

# frozen verdict: primary case S=50, T_DSB=150 K
def ok(key, t):
    return hours[(key, t)] >= 10.0 and eps_min(hours[(key, t)], 50.0, 150.0) < 4e-9

cleanA = any(ok(k, "A") for k in ("541.7", "595.5"))
reproc = any(ok(k, t) for k in ("541.7", "595.5") for t in ("B", "A+B"))
verdict = "FEASIBLE (clean)" if cleanA else ("FEASIBLE-WITH-REPROCESSING" if reproc else "NOT FEASIBLE")
kill = {k: eps_min(hours[(k, "A+B")], 50.0, 150.0) < 1e-12 for k in ("541.7", "595.5")}
P(f"\n  primary case (S=50, T_DSB=150 K): 541.7 A+B eps_min {eps_min(hours[('541.7', 'A+B')], 50, 150):.1e}, "
  f"595.5 A+B eps_min {eps_min(hours[('595.5', 'A+B')], 50, 150):.1e}")
P(f"  VERDICT: {verdict}   (Tier A hours 541.7/595.5 = {hours[('541.7', 'A')]:.2f}/{hours[('595.5', 'A')]:.2f}; "
  f"Tier B = {hours[('541.7', 'B')]:.2f}/{hours[('595.5', 'B')]:.2f}; threshold 10 h)")
P(f"  kill line 1e-12 reached in primary case: 541.7 {kill['541.7']}, 595.5 {kill['595.5']}")
R.update(verdict=verdict, kill=kill)
if MUT:
    P(f"  MUTATE: eps_min -> {eps_min(10.0, 50.0, 150.0)} ({'bites' if eps_min(10.0, 50.0, 150.0) == float('inf') else 'DID NOT BITE'})")
sfx = "_MUTATE" if MUT else ""
json.dump(R, open(os.path.join(HERE, f"cfg798_results{sfx}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg798{sfx}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if MUT else 0)
