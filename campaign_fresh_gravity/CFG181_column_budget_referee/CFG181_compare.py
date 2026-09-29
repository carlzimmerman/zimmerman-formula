#!/usr/bin/env python3
# CFG181 PHASE 2 ONLY: diff of the referee's saved results against CFG174's saved results/scripts (opened only after the referee runs were saved).
# Repo resolved from ZF_REPO or by walking up from __file__ / cwd; printed as <repo>.  Exit 0.
import os, sys, json, math, re
sys.dont_write_bytecode = True
from CFG181_common import *
HERE = os.path.dirname(os.path.abspath(__file__))
def find_repo():
    e = os.environ.get("ZF_REPO")
    if e and os.path.isdir(os.path.join(e, "campaign_fresh_gravity")): return e
    for start in (HERE, os.getcwd()):
        p = start
        while True:
            if os.path.isdir(os.path.join(p, "campaign_fresh_gravity")): return p
            q = os.path.dirname(p)
            if q == p: break
            p = q
    return None
repo = find_repo()
if repo is None: print("repo not found (set ZF_REPO)"); sys.exit(2)
L = []
def P(s=""): print(s); L.append(s)
P("repo = <repo>")
d174 = os.path.join(repo, "campaign_fresh_gravity", "CFG174_door11_vacuum_column")
a = json.load(open(os.path.join(d174, "CFG174_vacuum_column_results.json"))); a1 = json.load(open(os.path.join(d174, "CFG174_vacuum_column_results_MUTATE1.json")))
m = json.load(open(os.path.join(HERE, "CFG181_main_results.json"))); m1 = json.load(open(os.path.join(HERE, "CFG181_MUTATE_1_results.json")))
src = open(os.path.join(d174, "CFG174_vacuum_column.py"), encoding="utf-8").read()
rows = []
def row(name, mine, theirs, tol, cls):
    rel = abs(mine - theirs) / abs(theirs); rows.append((name, mine, theirs, rel, rel <= tol, cls))
row("Sigma_M A (Msun/pc2)", m["Q1"]["SigA"], a["Q1"]["canonical"]["Sigma_M_Msun_pc2"], 0.006, "numerical (constants)")
row("Sigma_M B", m["Q1"]["SigB"], a["Q1"]["alt"]["Sigma_M_Msun_pc2"], 0.015, "definition (footing B a0 = 1.1312e-10 there vs 1.13e-10 here)")
row("swept column", m["Q1"]["swept"], a["Q1"]["canonical"]["column_Msun_pc2"], 0.015, "numerical (rho_L: see below)")
row("R A", m["Q1"]["RA"], a["Q1"]["canonical"]["R"], 0.015, "numerical")
row("R B", m["Q1"]["RB"], a["Q1"]["alt"]["R"], 0.015, "definition/numerical (a0 B)")
for z in ("0.85", "1.5", "2.5"):
    row(f"Q3 dex z={z}", m["Q3"][z]["dex"], a["Q3"][z]["dlog_a0"], 0.001, "numerical")
    row(f"Q3 a0~H dex z={z}", m["Q3"][z]["Hdex"], a["Q3"][z]["dlog_a0_H"], 0.001, "numerical")
for lm in ("14", "14.5", "15"):
    mine = m["Q4"]["A"][lm if lm != "14" else "14"] if lm in m["Q4"]["A"] else m["Q4"]["A"][str(float(lm))]
    ca = [e for e in a["Q4"] if e["logM500"] == float(lm) and e["footing"] == "canonical"][0]
    ba = [e for e in a["Q4"] if e["logM500"] == float(lm) and e["footing"] == "alt"][0]
    row(f"Q4 A logM {lm}", mine, ca["steady_over_need"], 0.03, "numerical (rho_crit at H0=67.66 there vs 67.4 here)")
    row(f"Q4 B logM {lm}", m["Q4"]["B"][lm], ba["steady_over_need"], 0.03, "numerical / definition (a0 B)")
    row(f"Q4 swept/need logM {lm}", m["Q4"]["swept"][lm], ca["full_over_need"], 0.03, "numerical")
for n, mi, th, rel, ok, cls in rows: P(f"  {n:28s} mine {mi:9.4f}  CFG174 {th:9.4f}  rel diff {rel*100:5.2f}%  {'within tol' if ok else 'OUT'}   [{cls}]")
lab_mine = {k: v for k, v in m["Q4"]["label"].items()}
lab_them = [0.5 <= e["steady_over_need"] <= 2 for e in a["Q4"] if e["footing"] == "canonical"]
P(f"Q4 label per mass (14, 14.5, 15) mine {list(lab_mine.values())}; CFG174 {lab_them} (all-pass check {all(lab_them)}, reported FAIL)")
mut = {"CFG174 MUTATE1 R canonical": (a1["Q1"]["canonical"]["R"], m1["Q1"]["RA"]), "CFG174 MUTATE1 R alt": (a1["Q1"]["alt"]["R"], m1["Q1"]["RB"])}
for k, (t, mi) in mut.items(): P(f"  {k}: CFG174 {t:.3f}  mine {mi:.3f}  rel {abs(mi-t)/t*100:.2f}%")
P(f"MUTATE1 exit flags: CFG174 load-bearing failures = {sum(1 for c in a1['checks'] if (not c['ok']) and c['lb'])}, mine control bites = {m1['control_bites']}")
# how CFG174 fixed rho_L, H0, a0
rl = float(re.search(r"RHO_L = ([0-9.eE+-]+)", src).group(1)); a0alt = float(re.search(r'"alt": ([0-9.eE+-]+)', src).group(1))
rc = lambda h: 3 * H0_si(h)**2 / (8 * math.pi * G)
P(f"CFG174 hard-coded RHO_L = {rl:.4e}; Omega_L*rho_crit at (67.66, 0.6889) = {0.6889*rc(0.6766):.4e} ({(0.6889*rc(0.6766)/rl-1)*100:+.2f}%); at (67.4, 0.685) = {0.685*rc(0.674):.4e} ({(0.685*rc(0.674)/rl-1)*100:+.2f}%)")
P(f"CFG174 uses H0 = 67.66 / Om = 0.3111 for the age and for R500 (rho_crit) while its RHO_L is the (67.4, 0.685)-type value: a mixed cosmology, 1.4% effect on the swept column if RHO_L were tied to 67.66/0.6889 (numerical, immaterial to every pass line)")
P(f"CFG174 footing B a0 = {a0alt:.4e} (mine 1.13e-10)")
bad = [r for r in rows if not r[4]]
P(f"ROWS OUT OF TOLERANCE: {[r[0] for r in bad]}")
open(os.path.join(HERE, "CFG181_compare.out"), "w").write("\n".join(L) + "\n")
