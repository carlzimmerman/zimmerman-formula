"""CFG689 summary assembler (reads only the committed run JSONs cfg689*.json; no fitting, no new numbers).
Writes cfg689_summary.md: every mode's frozen classes (P0, P1, P2, P3, P4, P5, P6), K checks, MUTATE outcomes and bracket flips,
plus the A2 P2-with-theta* rule, so the README and the canon quote one table. Run: python3 cfg689_summary.py"""
import json, os, glob
HERE = os.path.dirname(os.path.abspath(__file__))
def load(m):
    p = os.path.join(HERE, "cfg689.json" if m == "primary" else f"cfg689_{m}.json")
    return json.load(open(p)) if os.path.exists(p) else None
ORDER = ["primary", "F", "T", "TF", "TD5F", "TU3F", "D5", "U3", "B1", "B2", "B3m", "B3p", "B4m", "B4p", "B5a", "B5b", "B5c", "B6", "B7", "B8",
         "B9", "B10", "B12", "B12c", "M1", "M2", "M3", "M1k", "M2k", "M4"]
LAB = {"primary": "curvature free, Pantheon+ (A1 primary)", "F": "flat (base primary)", "T": "curvature free + theta*", "TF": "flat + theta*",
       "TD5F": "flat + theta*, DES-SN5YR", "TU3F": "flat + theta*, Union3", "D5": "curvature free, DES-SN5YR", "U3": "curvature free, Union3",
       "B1": "BBN omega_b", "B2": "m_nu 0.06 eV", "B3m": "omega_b-omega_c corr -0.5", "B3p": "corr +0.5", "B4m": "cold drain -3%", "B4p": "cold made +3%",
       "B5a": "no CMB omega_c, h 0.680", "B5b": "no CMB omega_c, h 0.700", "B5c": "no CMB omega_c, SH0ES h 0.7304", "B6": "4 nodes",
       "B7": "SN zCMB > 0.03", "B8": "CMB omega sigma x2", "B9": "no CMB, no H0, rho_DE >= 0", "B10": "no Lya", "B12": "NO reconstruction (DR1 pre-recon)", "B12c": "POST-HOC control: DR1 post-recon, same conversion",
       "M1": "MUTATE constant truth (flat)", "M2": "MUTATE vanishing DE (flat)", "M3": "MUTATE r_d x1.02 (flat)", "M1k": "M1, curvature free (reported)",
       "M2k": "M2, curvature free (reported)", "M4": "MUTATE constant truth + theta* (flat)"}
f = lambda x, n=3: "-" if x is None else (f"{x:.{n}f}" if isinstance(x, (int, float)) else str(x))
L = ["# CFG689 summary (assembled by cfg689_summary.py from the run JSONs; criteria 1c237145d + A1 0db6da294 + A2 bb21587be)", "",
     "## Per mode, BAO + SN (tracking sqrt X = a0(z)/a0(0); 68% intervals; P6 = required a0 error for 20:1 vs LCDM's own DM14 law at z 2.5)", "",
     "| mode | setup | P0 Omega_k (class) | P2 dchi2/dof, sigma (class) | sqrtX z1.0 | sqrtX z1.5 | sqrtX z2.33 | P1 class | H0 (68%) | P6 e_20 z2.5 (class) | K4 | flips vs primary |",
     "|---|---|---|---|---|---|---|---|---|---|---|---|"]
missing = []
for m in ORDER:
    r = load(m)
    if r is None: missing.append(m); continue
    if "BAO+SN" not in r:
        if "M3" in r: L.append(f"| M3 | {LAB['M3']} | - | shift {r['M3']['shift_sigma']:.2f} sigma -> {'BITES' if r['M3']['bites'] else 'DOES NOT BITE'} | | | | | | | | |")
        continue
    a = r["BAO+SN"]; p0 = a.get("P0"); p2 = a["P2"]; p1 = a["P1"]; p6 = a.get("P6", {})
    q = lambda z: f"[{p1[z]['sqrtX_q'][1]:.2f}, {p1[z]['sqrtX_q'][3]:.2f}]"
    p0s = "flat" if not p0 else f"{p0['Omega_k_q'][2]:+.3f} [{p0['Omega_k_q'][1]:+.3f}, {p0['Omega_k_q'][3]:+.3f}] ({p0['P0_class']})"
    e20 = p6.get("2.5", {}).get("DM14", {}).get("e20_close") if p6 else None
    fl = r.get("flips"); fls = "-" if not fl else ("P1" if fl["P1"] else "") + (" P2" if fl["P2"] else "") or "none"
    L.append(f"| {m} | {LAB.get(m, m)} | {p0s} | {p2['dchi2']:.2f}/{p2['dof']}, {p2['sigma_equiv']:.2f} ({p2['P2_class']}) | {q('1.0')} | {q('1.5')} | {q('2.33')} | "
             f"{a['P1_class']} | {a['P3']['H0_q'][2]:.2f} [{a['P3']['H0_q'][1]:.2f}, {a['P3']['H0_q'][3]:.2f}] | {f(e20)} ({p6.get('P6_class', '-')}) | "
             f"{'PASS' if a['K4']['ok'] else 'FAIL'} | {fls} |")
prim = load("primary")
L += ["", "## Primary in detail (curvature free, BAO + Pantheon+)", ""]
if prim:
    a = prim["BAO+SN"]
    L.append("| z* | tracking sqrtX median [68%] | rival E = H/H0 [68%] | closest gap (dex) | e_3sigma (dex) |")
    L.append("|---|---|---|---|---|")
    for z in ("1.0", "1.2", "1.5", "2.33"):
        o = a["P1"][z]; L.append(f"| {z} | {o['sqrtX_q'][2]:.3f} [{o['sqrtX_q'][1]:.3f}, {o['sqrtX_q'][3]:.3f}] | {o['E_q'][2]:.3f} [{o['E_q'][1]:.3f}, {o['E_q'][3]:.3f}] | {o['gap_dex']:+.3f} | {f(o['e_3sigma'])} |")
    L += ["", "Record samples (CFG683 P3 e values): " + "; ".join(f"{k}: S {g['S']:.2f} {g['grade']}" for k, g in a["grades"].items())]
    L += ["", "P6 (LCDM's own emergent-scale laws from the record, 9d40e9c15c; z > 2.33 extrapolated beyond the last BAO node):", "",
          "| z | tracking sqrtX [68%] | DM14: gap close/median, e_20 | D08: gap close/median, e_20 | MAG: gap close/median, e_20 |", "|---|---|---|---|---|"]
    for z in ("2.0", "2.5", "3.25"):
        r6 = a["P6"][z]; cell = lambda law: f"{r6[law]['d_close']:+.3f}/{r6[law]['d_med']:+.3f}, {f(r6[law]['e20_close'])}"
        L.append(f"| {z}{' (extrap.)' if r6['extrapolated'] else ''} | [{r6['sqrtX_q'][1]:.3f}, {r6['sqrtX_q'][3]:.3f}] | {cell('DM14')} | {cell('D08')} | {cell('MAG')} |")
    bw = a["P6"]["3.25"].get("BigWheel_log10B_tracking_over_DM14")
    L += ["", f"Big Wheel (z 3.25, +0.06 +- 0.22 dex, N = 1; reported only): log10 B (tracking / DM14) = {f(bw, 2)}",
          "", f"P3 absolute a0 at kappa = 1/2 by node (median, m/s^2; kappa fitted, not a footing change): " + ", ".join(f"z {z}: {v[2]:.3e}" for z, v in a["P3"]["a0_node_q"].items()),
          "", "P4 (DESI fiducial span, DR1 Table 10): " + f"{prim['P4']['P4_class']}; " + "; ".join(f"{k} a_iso {v['a_iso']:.4f}, a_AP {v['a_AP']:.4f}" for k, v in prim["P4"]["alphas"].items()),
          "", "Checks: " + "; ".join(f"{k} {'PASS' if v['ok'] else 'FAIL'}" for k, v in prim["checks"].items())]
    b = prim.get("BAO")
    if b: L += ["", f"Primary BAO only: P2 {b['P2']['dchi2']:.2f}/{b['P2']['dof']} ({b['P2']['sigma_equiv']:.2f} sigma, {b['P2']['P2_class']}); P1 {b['P1_class']}; P0 {b['P0']['P0_class'] if b.get('P0') else '-'}; H0 {b['P3']['H0_q'][2]:.2f}"]
Fj = load("F")
if Fj and prim:
    sens = Fj["BAO+SN"]["P1_class"] != prim["BAO+SN"]["P1_class"] or Fj["BAO+SN"]["P2"]["P2_class"] != prim["BAO+SN"]["P2"]["P2_class"]
    L += ["", f"Flatness (A1.1): F vs primary -> {'FLATNESS-SENSITIVE' if sens else 'not flatness-sensitive'} "
          f"(P1 {Fj['BAO+SN']['P1_class']} vs {prim['BAO+SN']['P1_class']}; P2 {Fj['BAO+SN']['P2']['P2_class']} vs {prim['BAO+SN']['P2']['P2_class']})"]
T = load("T")
if T and "checks" in T: L += ["", "theta* checks (mode T): " + "; ".join(f"{k} {'PASS' if v['ok'] else 'FAIL'}" for k, v in T["checks"].items())]
U = load("TU3F")
if U and "P2_theta_rule" in U: L += ["", f"P2 with theta* across SN sets (A2.3): {U['P2_theta_rule']['sigma']} -> {U['P2_theta_rule']['P2_theta_class']}"]
L += ["", "## MUTATE (frozen pass rules: M1, M2, M3, M4; M1k/M2k reported)", ""]
for m in ("M1", "M2", "M3", "M4", "M1k", "M2k"):
    r = load(m)
    if r is None: L.append(f"- {m}: missing"); continue
    o = r.get(m, {}); ok = o.get("pass_", o.get("bites"))
    L.append(f"- {m} ({LAB[m]}): {'PASS' if ok else 'FAIL'}  {json.dumps({k: v for k, v in o.items() if k != 'frozen_rule'}, default=str)}")
P5 = os.path.join(HERE, "cfg689_P5.json")
if os.path.exists(P5):
    p5 = json.load(open(P5)); L += ["", f"P5 (framework vs Newtonian same-seed PM power, k <= 0.33 h/Mpc): max|r| {f(p5['max_abs_r'], 4)} x s_NL {p5['s_NL']} = {f(p5['dalpha_NL'], 5)} -> {p5['P5_class']}"]
    for nm, pr in p5["pairs"].items():
        if pr.get("used"): L.append(f"  - {nm}: " + "; ".join(f"{zk} max|r| {v['max_abs']:.4f}" for zk, v in pr["rows"].items() if isinstance(v, dict)))
        else: L.append(f"  - {nm}: not used ({pr.get('why')})")
if missing: L += ["", f"Missing modes (not run or failed): {missing}"]
L += ["", "kappa fitted; cold energy mass required; not theory closed; nothing here says the data favour the framework over LCDM."]
open(os.path.join(HERE, "cfg689_summary.md"), "w").write("\n".join(L) + "\n"); print("\n".join(L))
