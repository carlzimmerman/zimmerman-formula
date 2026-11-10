#!/usr/bin/env python3
"""ONE1 row 6 (FROZEN_CRITERIA.md a967a38851): Coma's diffuse galaxies and the dwarf spheroidals, with no external-field effect
(a member's halo is real mass, laid out as its own isolated halo). Reused graders, read only:
  - Coma UDGs: S1's Coma chain with x_e = 0 (row "S2 AQUAL isolated L*0 E-W", s1_v3_hosted_small_results.json) carried; KA8 = my
    algebraic recomputation of S1's "S1 kernel nu1" row from S1's per-galaxy inputs. Line GB1 G5: |mean| <= 2 sigma_U (gb1.json).
  - dSphs: GB1 G6 for the plain law L0 (LW1 "plain" = isolated nu(g_N), no external field), carried from gb1.json.
  - The halo's end x_t r_M against the readout radius, per system.
    python3 one1_coma.py -> one1_coma.json / one1_coma.out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, json, math, csv
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", "..")); RB = os.path.join(REPO, "rebuild_2026_10_22")
CRIT = "a967a38851"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
G_, MSUN_, PC_ = 6.674e-11, 1.989e30, 3.0857e16; KPC = 1e3 * PC_; R12 = 4.0 / 3.0
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOT = ("canonical", "alt")
ONE = json.load(open(os.path.join(HERE, "one1.json"))); XP = {f: ONE["foot"][f]["X"] for f in FOOT}; XT = {f: math.sqrt(XP[f] * (XP[f] + 1)) for f in FOOT}
def nu1(y): return 0.5 * (1.0 + math.sqrt(1.0 + 4.0 / y))
S1R = json.load(open(os.path.join(RB, "S1_v3_hosted_small", "s1_v3_hosted_small_results.json")))["coma"]
ROWS = list(csv.DictReader(open(os.path.join(RB, "S1_v3_hosted_small", "s1_coma_per_galaxy.csv"))))
GB = json.load(open(os.path.join(REPO, "closure_2026_11_06", "GB1_all_gates_battery", "gb1.json")))["cands"]["L0"]
LW = json.load(open(os.path.join(RB, "LW1_law_scorecard", "lw1_dwarfs.json")))
X1 = {(r["footing"], r["name"]): r for r in csv.DictReader(open(os.path.join(RB, "X1_hosted_recount", "x1_per_system.csv")))}
RES = dict(lane="ONE1", row="6 Coma UDGs and dSphs", criteria=CRIT, note="TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed", foot={}, KA={})
P(f"ONE1 row 6 (criteria {CRIT}). No external field: a member's halo is its own isolated halo, ending at x_t r_M (x_t {XT['canonical']:.2f} / {XT['alt']:.2f}).")
for f in FOOT:
    a0 = A0[f]; F = {}
    # ---- KA8: S1's algebraic isolated-law row from its per-galaxy inputs
    E = []; ends = []
    for r in ROWS:
        if r["footing"] != f: continue
        Ms, Re, sig = float(r["Mstar"]), float(r["Re_kpc"]), float(r["sigma"]); r12 = R12 * Re * KPC; gb = G_ * (Ms / 2) * MSUN_ / r12 ** 2
        sl = math.sqrt(r12 * gb * nu1(gb / a0) / 3) / 1e3; E.append(2 * math.log(sig / sl))
        rM = math.sqrt(G_ * Ms * MSUN_ / a0); ends.append((r["name"], XT[f] * rM / KPC, r12 / KPC, XT[f] * rM / r12))
    mine = float(np.mean(E)) / math.log(10); ref = S1R[f"{f}|S1 kernel nu1 (algebraic)"]["meanE"] / math.log(10)
    RES["KA"][f"KA8 {f}"] = dict(value=mine, ref=ref, ok=bool(abs(mine - ref) <= 1e-3))
    P(f"\n[{f}] KA8 algebraic isolated law over the {len(E)} UDGs: {mine:+.4f} dex vs S1's 'S1 kernel nu1' {ref:+.4f} -> {'PASS' if abs(mine - ref) <= 1e-3 else 'FAIL'}")
    iso = S1R[f"{f}|S2 AQUAL isolated L*0 E-W"]; m = iso["meanE_dex"]; sU = GB[f]["G5 Coma UDGs"]["num"]["sigma_U"]
    st = "PASS" if abs(m) <= 2 * sU else "FAIL"; mn = min(e[3] for e in ends)
    F["UDG"] = dict(status=st, mean_dex=m, sigma_U=sU, line=2 * sU, z_U=m / sU, z_sys_S1=iso["z_sys"], law_with_EFE_GB1=GB[f]["G5 Coma UDGs"]["num"]["mean"],
                    ends=[dict(name=n, end_kpc=a, r12_kpc=b, ratio=c) for n, a, b, c in ends], min_end_over_r12=mn)
    P(f"[{f}] ROW 6a Coma UDGs, no external field (S1 'S2 AQUAL isolated L*0 E-W', carried): mean residual {m:+.3f} dex against GB1's line 2 sigma_U = {2 * sU:.3f} "
      f"({m / sU:+.2f} sigma_U; S1's own z_sys {iso['z_sys']:+.2f}) -> {st}. With the external field (GB1 L0) it was {GB[f]['G5 Coma UDGs']['num']['mean']:+.3f}.")
    P(f"[{f}]   halo end / r_1/2 per UDG: min {mn:.1f} (" + ", ".join(f"{n[:11]} {c:.0f}" for n, a, b, c in ends) + "): every halo reaches far past the readout radius.")
    # ---- dSphs: GB1 G6, L0
    g6 = GB[f]["G6 dSph classes"]; ps = LW["footings"][f]["per_system"]; tr = {}
    for cls in ("bright M31", "MW classical", "LG field"):
        rr = []
        for n, s in ps.items():
            if s["cls"] != cls: continue
            x = X1.get((f, n))
            if x is None: continue
            Ms = 10 ** float(x["logMstar"]); rh = float(x["rh_pc"]) * PC_; rM = math.sqrt(G_ * Ms * MSUN_ / a0); rr.append((n, XT[f] * rM / rh))
        tr[cls] = dict(n=len(rr), min_end_over_rh=min(v for _, v in rr) if rr else None, n_end_inside_rh=sum(v < 1 for _, v in rr), n_end_inside_2rh=sum(v < 2 for _, v in rr))
    ok = all(g6["status"] == "PASS" for _ in [0]); F["dSph"] = dict(status=g6["status"], classes={k: v for k, v in g6["num"].items()}, truncation=tr)
    P(f"[{f}] ROW 6b dSphs, plain isolated law (GB1 G6, L0, carried): {g6['status']}: " + "; ".join(f"{k} {v['median_minus_anchor']:+.3f} [{v['ci'][0]:+.3f}, {v['ci'][1]:+.3f}]"
      + (" contains 0" if v["contains0"] else " EXCLUDES 0") for k, v in g6["num"].items() if v["graded"]))
    P(f"[{f}]   halo end / r_h: " + "; ".join(f"{k}: N {v['n']}, min {v['min_end_over_rh']:.2f}, end inside r_h {v['n_end_inside_rh']}, inside 2 r_h {v['n_end_inside_2rh']}" for k, v in tr.items())
      + ". An end inside the readout radius lowers the prediction and raises a positive residual: the FAIL cannot turn into a pass.")
    F["status"] = "PASS" if (F["UDG"]["status"] == "PASS" and g6["status"] == "PASS") else "FAIL"; RES["foot"][f] = F
RES["KA_all_pass"] = all(v["ok"] for v in RES["KA"].values())
P(f"\nKA8: {'PASS' if RES['KA_all_pass'] else 'FAIL'}"); P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
json.dump(RES, open(os.path.join(HERE, "one1_coma.json"), "w"), indent=1); open(os.path.join(HERE, "one1_coma.out"), "w").write("\n".join(OUT) + "\n")
