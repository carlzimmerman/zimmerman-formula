#!/usr/bin/env python3
"""Check PREDICTIONS_2026_11_07.md: every quoted literal appears in the file and, as given, in the committed source
named beside it (read from origin/main if absent locally). --mutate changes one digit of each source literal; exit 0
only if every mutated literal then fails. Collection only; adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, re, subprocess, sys
MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
DOC = open(os.path.join(HERE, "PREDICTIONS_2026_11_07.md"), encoding="utf-8").read()
CQ2 = "cq_lanes_2026_11_04/CQ2_v3s_dr4_seal/SEALED_PREDICTION.md"
OD = "prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-05_DR4_FORKS.md"
DP2 = "dr4_push_2026_11_05/DP2_n_forecast_triples/README.md"
C689 = "campaign_fresh_gravity/CFG689_native_ruler_bao/cfg689_summary.md"
AT1 = "rebuild_2026_10_22/AT1_a0z_tracking_decision/FROZEN_CRITERIA.md"
AT2 = "rebuild_2026_10_22/AT2_a0z_on_disk_samples/README.md"
V3W = "rebuild_2026_10_22/V3W_v3s_weak_spots/README.md"
V3WC = "rebuild_2026_10_22/V3W_v3s_weak_spots/FROZEN_CRITERIA.md"
# (literal in the doc, source file, literal in that source)
L = [
 ("4.45e-05 canonical", CQ2, "max γ_r − 1 4.45e-05"), ("4.01e-05 alt", CQ2, "max γ_r − 1 4.01e-05"),
 ("1.0019 canonical and 1.0100 alt", CQ2, "1.0019 (0.0200)"), ("1.0019 canonical and 1.0100 alt", CQ2, "1.0100 (0.0068)"),
 ("1.1494 / 1.2081", CQ2, "| 1.1494 |"), ("1.1494 / 1.2081", CQ2, "| 1.2081 |"),
 ("σ_fit = 0.019 √(30000/N)", OD, "σ_fit = 0.019 √(30000/N)"),
 ("γ̂ − 1.000 ≥ 3σ", OD, "γ̂ − 1.000 ≥ 3σ"),
 ("R − 1 ≥ max(0.01, 3σ_R)", OD, "R − 1 ≥ max(0.01, 3σ_R)"),
 ("σ_sys(b) < 0.048 canonical / 0.058 alt", OD, "σ_sys(b) < 0.048 canonical / 0.058 alt"),
 ("1.083 – 1.23", OD, "| 1.083 – 1.23 | **EXCLUDED**"), ("also 1.083", OD, "Medium-first edge 1.083"),
 ("BOTH EXCLUDED", OD, "BOTH EXCLUDED"),
 ("low 7,025 / central 8,039 / high 8,618", DP2, "low 7,025 / central 8,039 / high 8,618"),
 ("| registered 0.0367 | 0.020 | γ̂ ≥ 1.125 |", DP2, "| registered 0.0367 | 0.020 | 0.042 | 1.036 | 1.125 | 0.80 |"),
 ("| registered 0.0367 | 0.0375 | γ̂ ≥ 1.157 |", DP2, "| registered 0.0367 | 0.0375 | 0.053 | **1.004** | 1.157 | **0.40** |"),
 ("| DR3-cal 0.0483 | 0.0375 | γ̂ ≥ 1.184 |", DP2, "| DR3-cal 0.0483 | 0.0375 | 0.061 | **0.978** | 1.184 | **0.12** |"),
 ("| 1.0 | 0.913 | [0.762, 1.027] | 1.761 | 0.055 |", C689, "| 1.0 | 0.913 [0.762, 1.027] | 1.761 [1.733, 1.788] | +0.227 | 0.055 |"),
 ("| 1.5 | 0.942 | [0.706, 1.115] | 2.353 | 0.074 |", C689, "| 1.5 | 0.942 [0.706, 1.115] | 2.353 [2.309, 2.398] | +0.316 | 0.074 |"),
 ("| 2.33 | 0.909 | [0.325, 1.212] | 3.490 | 0.084 |", C689, "| 2.33 | 0.909 [0.325, 1.212] | 3.490 [3.442, 3.540] | +0.453 | 0.084 |"),
 ("RIVAL FAVOURED (|d_R| ≤ 2 and d_T ≥ 3)", AT1, "**RIVAL FAVOURED:** |d_R| ≤ 2 and d_T ≥ 3."),
 ("NEITHER (|d_T| > 3 and |d_R| > 3)", AT1, "**NEITHER:** |d_T| > 3 and |d_R| > 3."),
 ("falsifies the law's a0(z) at that redshift", AT1, "falsifies the law's a₀(z) at that redshift on the measured sample"),
 ("52 (sample, z*) cells, 52 BLOCKED", AT2, "52 (sample, z*) cells, 52 BLOCKED"),
 ("(0.30-0.60 dex) is 4-11x above the largest e_3σ (0.084 dex)", AT2, "(0.30-0.60 dex) is 4-11x above the largest e_3σ (0.084 dex)"),
 ("1.1e-5 / 2.8e-5 / 6.5e-5 /\n1.9e-4 at 30 / 100 / 310 / 2600 kpc", V3W, "1.1e-5 / 2.8e-5 / 6.5e-5 / 1.9e-4 at 30 / 100 / 310 / 2600 kpc"),
 ("FAIL iff D1 is more than 2σ_tot from 1, or D2 is more than\n3σ_tot from 1", V3WC, "FAIL iff D1 is more than 2σ_tot from 1, or D2 is more than 3σ_tot from 1"),
 ("A = 1.129 ± 0.206 (+0.6σ)", V3W, "1.129 ± 0.049 (stat) ± 0.200 (sys) = ± 0.206; **+0.6σ**"),
 ("A = 1.035 ± 0.187 (+0.2σ)", V3W, "1.035 ± 0.045 ± 0.182 = ± 0.187; **+0.2σ**"),
 ("0.974 ± 0.248", V3W, "A = 0.974 ± 0.248"), ("0.890 ± 0.227", V3W, "0.890 ± 0.227; −0.5σ"),
 ("(A = 5.5) is only 1.9σ_tot on D1", V3W, "(A = 5.5) is only 1.9σ_tot on D1"),
 ("0.93–1.33", V3W, "moves A over 0.93–1.33 (canonical)"),
]
ws = lambda t: re.sub(r"\s+", " ", t)
cache = {}
def src(p):
    if p not in cache:
        fp = os.path.join(ROOT, p)
        if os.path.exists(fp):
            cache[p] = ws(open(fp, encoding="utf-8").read())
        else:
            r = subprocess.run(["git", "-C", ROOT, "show", "origin/main:" + p], capture_output=True, text=True)
            cache[p] = ws(r.stdout) if r.returncode == 0 else ""
    return cache[p]
def mutate(lit):
    m = re.search(r"\d", lit)
    return lit if not m else lit[:m.start()] + str((int(m.group()) + 1) % 10) + lit[m.end():]
D = ws(DOC); ok = 0; bad = []
for frag, path, lit in L:
    if MUT:
        if not re.search(r"\d", lit) or ws(mutate(lit)) not in src(path): ok += 1
        else: bad.append(("mutant survived", frag, path))
    elif ws(frag) in D and ws(lit) in src(path): ok += 1
    else: bad.append(("doc" if ws(frag) not in D else "src", frag, path))
rules = [("kappa fitted", "Kappa = 1/2 FITTED" in DOC), ("not closed", "not theory closed" in DOC),
         ("no favouring", "Nothing here says the data favour the framework" in DOC),
         ("never pooled", "never pooled" in DOC), ("no LCDM inputs", "No ΛCDM inputs" in DOC),
         ("no local paths", "/Users/" not in DOC), ("no 'cold dark matter'", "cold dark matter" not in DOC.lower()),
         ("survives not confirmed", 'never "confirmed"' in DOC)]
if not MUT:
    for n, g in rules:
        if g: ok += 1
        else: bad.append(("rule", n, ""))
for b in bad: print("FAIL", *b)
print(f"{ok} of {len(L) + (0 if MUT else len(rules))} checks pass" + (" (mutate)" if MUT else ""))
print("kappa = 1/2 FITTED; not theory closed.")
sys.exit(0 if not bad else 1)
