#!/usr/bin/env python3
"""CFG428 (FROZEN_CRITERIA.md): one Bose field vs CFG383 / CFG474 / CFG479 / Bullet.  CFG428_MUTATE=1 -> Bullet limit x 1e40."""
import os, json, math
MUT = os.environ.get("CFG428_MUTATE", "0") == "1"; SUF = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
hbar, c, eV, kpc = 1.054571817e-34, 2.99792458e8, 1.602176634e-19, 3.0857e19
w474 = json.load(open(os.path.join(HERE, "..", "CFG474_cold_mass_window", "cfg474_window_results.json")))
FB = 0.157; rho = 1.55e-24 * (1 - FB); sv = 1.0e6; tH = 13.8 * 3.156e16
SIGM = 1.0e-4 * (1e40 if MUT else 1.0)                    # 1 cm^2/g in m^2/kg
L, OUT = [], {"mutate": MUT}
def P(s=""): print(s); L.append(s)
def kg(m_eV): return m_eV * eV / c**2
wins = []
def walk(o):
    if isinstance(o, dict):
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        if len(o) == 2 and all(isinstance(x, (int, float)) for x in o) and 0 < o[0] < o[1]: wins.append(tuple(o))
        else:
            for v in o: walk(v)
walk(w474)
P(f"CFG474 windows read: {sorted(set(wins))}")
M383 = (0.62, 0.81, 1.04)
t1 = all(any(lo <= m <= hi for lo, hi in wins) for m in M383); OUT["t1_window"] = t1
P(f"T1 CFG383 m {M383} eV inside a CFG474 window: {t1}")
rows = []
for m in M383:
    mk = kg(m); n = rho / mk
    dep = []
    for nu in (0.05, 0.3):
        a = n ** (-1 / 3) * (3 * math.sqrt(math.pi) * nu / 8) ** (2 / 3); sm = 8 * math.pi * a * a / mk
        dep.append((nu, a, sm / 1e-4))
    amax = math.sqrt(SIGM * mk / (8 * math.pi)); sig = 8 * math.pi * amax ** 2
    occ = n * (2 * math.pi * hbar) ** 3 / (mk ** 3 * (2 * math.pi * sv * sv) ** 1.5)
    t = 1.0 / (n * sig * sv * (1 + occ))
    rows.append(dict(m=m, n=n, dep=dep, a_max=amax, occ=occ, t_relax_Gyr=t / 3.156e16))
    P(f"  m {m:.2f} eV: n {n:.3e} m^-3; depletion a(nu .05/.3) = {dep[0][1]*1e3:.2f}/{dep[1][1]*1e3:.2f} mm -> sigma/m = {dep[0][2]:.2e}/{dep[1][2]:.2e} cm^2/g; "
      f"Bullet a_max {amax:.2e} m; occupation {occ:.2e}; t_relax {t/3.156e16:.3g} Gyr")
dep_dead = min(r["dep"][0][2] for r in rows) > 10 * SIGM / 1e-4
t3 = any(r["t_relax_Gyr"] * 3.156e16 <= tH for r in rows)
OUT.update(rows=rows, t2_depletion_dead=dep_dead, t3_thermal_allowed=t3)
P(f"T2 depletion route DEAD (> 10x Bullet): {dep_dead}")
P(f"T3 thermal route relaxes within t_H at the Bullet limit for some m: {t3}")
P("T4 production: a 0.6-1 eV boson must be non-thermally produced (a thermal relic at this mass is hot dark matter); not computed.")
v = "ONE FIELD VIABLE" if (t1 and t3) else "ONE FIELD DEAD"
OUT["verdict"] = v; P(f"\nVERDICT: {v} (depletion route {'DEAD' if dep_dead else 'alive'})")
open(os.path.join(HERE, f"cfg428_ledger{SUF}.out"), "w").write("\n".join(L) + "\n"); json.dump(OUT, open(os.path.join(HERE, f"cfg428_results{SUF}.json"), "w"), indent=1)
