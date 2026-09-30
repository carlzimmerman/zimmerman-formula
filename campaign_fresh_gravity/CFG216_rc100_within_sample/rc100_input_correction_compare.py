#!/usr/bin/env python3
"""Input-correction comparison for CFG216 / CFG217 / CFG218 (2026-09-29).
The data chat's provenance check (03922e8c7) found 16 of RC100's 100 rows differing from the paper in 17 cells (12 values, 5 names): 7 rows carry log M_bulge in place of
log M_baryon, rows 24 and 90 have small log M_baryon typos, V_c is wrong in rows 43 and 44, f_DM in row 36, names in rows 24, 31, 32, 34 and 96; z, R_e and sigma_0 match.
The three lanes were re-run with RC100_INPUT=corrected (the corrected six-field copy) as append-only runs; the original outputs are kept.  This script reads both sets of
committed JSON / .out files and writes INPUT_CORRECTION_2026-09-29.md with every number that moves.  Nothing is computed from data here.
Run: python3 campaign_fresh_gravity/CFG216_rc100_within_sample/rc100_input_correction_compare.py
"""
import os, sys, json, re
sys.dont_write_bytecode = True

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)


def J(lane, name):
    return json.load(open(os.path.join(CFG, lane, name)))["numbers"]


o16, c16 = J("CFG216_rc100_within_sample", "cfg216_rc100_results.json"), J("CFG216_rc100_within_sample", "cfg216_rc100_corrected_results.json")
o17, c17 = J("CFG217_rc100_attack", "cfg217_attack_results.json"), J("CFG217_rc100_attack", "cfg217_attack_corrected_results.json")
o18, c18 = J("CFG218_signal_vs_systematic", "cfg218_ladder_results.json"), J("CFG218_signal_vs_systematic", "cfg218_ladder_corrected_results.json")
rows = []


def add(lane, what, a, b, fmt="{:+.3f}"):
    f = lambda v: fmt.format(v) if isinstance(v, (int, float)) else str(v)
    moved = "" if f(a) == f(b) else "**moves**"
    rows.append((lane, what, f(a), f(b), moved))


def ci(d, k="slope"):
    return f"{d[k]:+.3f} [{d['lo']:+.3f}, {d['hi']:+.3f}]"


# ---- CFG216
for law in ("flat", "rival"):
    a, b = o16["results"][f"nu_mono|canonical|{law}"], c16["results"][f"nu_mono|canonical|{law}"]
    add("CFG216", f"slope of delta_{law} on z (nu_mono, canonical) [95% CI]", ci(a), ci(b), "{}")
    add("CFG216", f"median delta_{law} [95% CI]", f"{a['med']:+.3f} [{a['mlo']:+.3f}, {a['mhi']:+.3f}]", f"{b['med']:+.3f} [{b['mlo']:+.3f}, {b['mhi']:+.3f}]", "{}")
    for truth in ("flat", "rival"):
        za = (a["slope"] - o16["expected"][truth][law]) / a["sd"]
        zb = (b["slope"] - c16["expected"][truth][law]) / b["sd"]
        add("CFG216", f"z-score of delta_{law}'s slope against '{truth} true'", za, zb, "{:+.2f}")
for truth in ("flat", "rival"):
    add("CFG216", f"expected slopes if {truth} true (delta_flat, delta_rival)",
        f"{o16['expected'][truth]['flat']:+.3f}, {o16['expected'][truth]['rival']:+.3f}", f"{c16['expected'][truth]['flat']:+.3f}, {c16['expected'][truth]['rival']:+.3f}", "{}")
add("CFG216", "primary outcome", o16["outcome_primary"].split(" ")[0], c16["outcome_primary"].split(" ")[0], "{}")
for lab in ("(a) the RC41 subset", "(b) the other galaxies", "(c) g_bar < 3 a0", "(d) table M_bar geometry"):
    for law in ("flat", "rival"):
        a, b = o16["sens"][f"{lab}|{law}"], c16["sens"][f"{lab}|{law}"]
        add("CFG216", f"{lab}, {law}: median | slope", f"{a['med']:+.3f} [{a['mlo']:+.3f}, {a['mhi']:+.3f}] | {ci(a)}", f"{b['med']:+.3f} [{b['mlo']:+.3f}, {b['mhi']:+.3f}] | {ci(b)}", "{}")
add("CFG216", "C2: RC41 galaxies matched by name; median shift (dex)", f"{o16['C2']['n']}; {o16['C2']['median']:+.3f}", f"{c16['C2']['n']}; {c16['C2']['median']:+.3f}", "{}")
# post hoc index (text)
def idx(fn):
    t = open(os.path.join(LANE, fn)).read()
    m = re.search(r"canonical: p = ([-+0-9.]+) \[([-+0-9.]+), ([-+0-9.]+)\] \(sigma ([0-9.]+).*?c = ([-+0-9.]+).*?flat \(p = 0\) is ([0-9.]+) sigma away, the rival \(p = ([0-9.]+)\) ([0-9.]+) sigma", t)
    return m.groups() if m else None
ia, ib = idx("cfg216_posthoc_index.out"), idx("cfg216_posthoc_index_corrected.out")
if ia and ib:
    add("CFG216 post hoc", "a0(z) index p (canonical) [95%], sigma", f"{ia[0]} [{ia[1]}, {ia[2]}], {ia[3]}", f"{ib[0]} [{ib[1]}, {ib[2]}], {ib[3]}", "{}")
    add("CFG216 post hoc", "flat / rival distance in sigma", f"{ia[5]} / {ia[7]}", f"{ib[5]} / {ib[7]}", "{}")

# ---- CFG217
add("CFG217", "RC41 overlap (galaxies found by name)", 38, 41, "{}")
add("CFG217", "C-recon: median |Delta log M*| (dex); accepted?", f"{o17['recon']['median_abs']:.3f}; {o17['recon']['accepted']}", f"{c17['recon']['median_abs']:.3f}; {c17['recon']['accepted']}", "{}")
add("CFG217", "G2: Spearman rho(delta_flat, Delta_prior), p; prior-driven", f"{o17['G2']['rho']:+.2f}, {o17['G2']['p']:.3f}; {o17['G2']['prior_driven']}", f"{c17['G2']['rho']:+.2f}, {c17['G2']['p']:.3f}; {c17['G2']['prior_driven']}", "{}")
for k in o17["G3"]:
    for law in ("flat", "rival"):
        add("CFG217", f"G3 alpha = {k}: slope of delta_{law}", ci(o17["G3"][k][law]), ci(c17["G3"][k][law]), "{}")
add("CFG217", "G5 M1: differential dlogM (dex) that reproduces the flat slope", o17["G5"]["beta_M1"] * 0.3403, c17["G5"]["beta_M1"] * 0.3403, "{:+.3f}")
add("CFG217", "G5 M2: best differential dlogM (dex); chi2 at the best beta", f"{o17['G5']['dlogM_M2']:+.3f}; {o17['G5']['chi2_M2']:.2f}", f"{c17['G5']['dlogM_M2']:+.3f}; {c17['G5']['chi2_M2']:.2f}", "{}")
add("CFG217", "G5 M2: best chi2 within the plausible 0.2 dex", o17["G5"]["chi2_plausible"], c17["G5"]["chi2_plausible"], "{:.2f}")
for law in ("flat", "rival"):
    add("CFG217", f"G7: residual z-slope of delta_{law}", ci(o17["G7"]["res"][law]), ci(c17["G7"]["res"][law]), "{}")
for k in o17["posthoc"]["A_full"]:
    for law in ("flat", "rival"):
        add("CFG217", f"post hoc (A) {k.split(' ')[0]}: slope of delta_{law} (all 100, reconstructed M*)", ci(o17["posthoc"]["A_full"][k][law]), ci(c17["posthoc"]["A_full"][k][law]), "{}")
add("CFG217", "post hoc (B): dlogM that makes the rival slope 0 | the flat slope 0", f"{o17['posthoc']['B']['dlogM_rival_zero']:+.3f} | {o17['posthoc']['B']['dlogM_flat_zero']:+.3f}",
    f"{c17['posthoc']['B']['dlogM_rival_zero']:+.3f} | {c17['posthoc']['B']['dlogM_flat_zero']:+.3f}", "{}")
add("CFG217", "D3 (literal, frozen)", o17["D3"], c17["D3"], "{}")

# ---- CFG218
for s in o18["ladder"]:
    a, b = o18["ladder"][s], c18["ladder"][s]
    if s == "RC100":
        add("CFG218", "RC100: signal | stat band | b_s | S_sys | calibration for S/3", f"{a['S']:.3f} | {a['stat']:.3f} | {a['b']:+.3f} | {a['S_sys']:.3f} | {a['e_needed']:.3f}",
            f"{b['S']:.3f} | {b['stat']:.3f} | {b['b']:+.3f} | {b['S_sys']:.3f} | {b['e_needed']:.3f}", "{}")
        add("CFG218", "RC100 classification", a["cls"], b["cls"], "{}")
    else:
        add("CFG218", f"{s} (unchanged by construction): signal | S_sys", f"{a['S']:.3f} | {a['S_sys']:.3f}", f"{b['S']:.3f} | {b['S_sys']:.3f}", "{}")

def verdict(lo, hi):
    return "CONSISTENT" if lo <= 0 <= hi else ("DISFAVOURED-over" if lo > 0 else "DISFAVOURED-under")


def zs(res, exp, law, truth):
    return (res["results"][f"nu_mono|canonical|{law}"]["slope"] - exp["expected"][truth][law]) / res["results"][f"nu_mono|canonical|{law}"]["sd"]


da, db = o16["sens"]["(d) table M_bar geometry|flat"], c16["sens"]["(d) table M_bar geometry|flat"]
material = [
    "**Conclusions unchanged:** CFG216's outcome is W-flat in both runs; CFG217's literal D3 is ATTACK-BROKEN (the same power artefact) in both; CFG218's classification of RC100 is 'marginal' in both, "
    "and the calibration needed for S/3 is 0.040 dex in both.",
    f"**CFG216 slopes (nu_mono, canonical):** delta_flat {ci(o16['results']['nu_mono|canonical|flat'])} to {ci(c16['results']['nu_mono|canonical|flat'])}; delta_rival "
    f"{ci(o16['results']['nu_mono|canonical|rival'])} to {ci(c16['results']['nu_mono|canonical|rival'])}. All within 0.003.",
    f"**The 5.5 sigma and 4.9 sigma from the rival's expected slopes become {abs(zs(c16, c16, 'flat', 'rival')):.2f} and {abs(zs(c16, c16, 'rival', 'rival')):.2f}** "
    f"(from {abs(zs(o16, o16, 'flat', 'rival')):.2f} and {abs(zs(o16, o16, 'rival', 'rival')):.2f}); the distances from the flat expectations move from {abs(zs(o16, o16, 'flat', 'flat')):.2f} and "
    f"{abs(zs(o16, o16, 'rival', 'flat')):.2f} to {abs(zs(c16, c16, 'flat', 'flat')):.2f} and {abs(zs(c16, c16, 'rival', 'flat')):.2f}.",
    f"**CFG216 variant (d), which uses the M_bar column that was wrong in 9 rows:** the flat median goes from {da['med']:+.3f} [{da['mlo']:+.3f}, {da['mhi']:+.3f}] "
    f"({verdict(da['mlo'], da['mhi'])}) to {db['med']:+.3f} [{db['mlo']:+.3f}, {db['mhi']:+.3f}] ({verdict(db['mlo'], db['mhi'])}), and the flat slope from {ci(da)} to {ci(db)} "
    "(its CI now excludes 0 on the negative side). This is the biggest mover.",
    "**CFG216 by z-half (from the .out files):** the low-z half's flat median goes from +0.041 to +0.061; the high-z half is unchanged.",
    "**RC41 overlap:** 38 to 41 galaxies matched (the corrected names). The RC41 subset's flat median is +0.041 [+0.001, +0.099] (was +0.041 [+0.004, +0.109]).",
    f"**CFG217 G2 (prior-driven f_DM) flips from 'no' to 'yes' by the frozen line:** Spearman rho {o17['G2']['rho']:+.2f} (p = {o17['G2']['p']:.3f}) to {c17['G2']['rho']:+.2f} (p = {c17['G2']['p']:.3f}). "
    "The z-slope after removing the Delta_prior dependence stays near zero (+0.014 [-0.027, +0.069]).",
    f"**CFG217 C-recon is still rejected** ({o17['recon']['median_abs']:.3f} to {c17['recon']['median_abs']:.3f} dex against the 0.15 line), so G1 still runs on the 41-galaxy overlap only and the literal D3 is unchanged.",
    f"**CFG217 mock:** the best chi2 within the plausible 0.2 dex is {o17['G5']['chi2_plausible']:.2f} to {c17['G5']['chi2_plausible']:.2f} (still above the frozen 2); the differential mis-scaling that reproduces the flat slope moves "
    f"{o17['G5']['beta_M1'] * 0.3403:+.3f} to {c17['G5']['beta_M1'] * 0.3403:+.3f} dex, and the calibration that makes the rival slope exactly 0 stays at {o17['posthoc']['B']['dlogM_rival_zero']:+.3f} to {c17['posthoc']['B']['dlogM_rival_zero']:+.3f} dex.",
    "**CFG217 post hoc gas variants:** V2's rival deficit crosses from 2.99 sigma to 3.1 sigma, so the 'survives' flag for V2 goes from NO to YES (borderline either way); V1 and V4 still reverse the result.",
    f"**CFG218 RC100 row:** the statistical band {o18['ladder']['RC100']['stat']:.3f} to {c18['ladder']['RC100']['stat']:.3f} dex; b_s {o18['ladder']['RC100']['b']:+.3f} to {c18['ladder']['RC100']['b']:+.3f} dex; "
    f"S_sys {o18['ladder']['RC100']['S_sys']:.3f} to {c18['ladder']['RC100']['S_sys']:.3f}.",
    "**CFG216 post hoc index:** p = -0.72 [-1.49, +0.14] to -0.71 [-1.52, +0.15] (canonical); the rival is 4.7 sigma away (was 4.8); flat 1.7 sigma in both.",
]
md = ["# RC100 input correction: CFG216 / CFG217 / CFG218 re-run (2026-09-29)", "",
      "**Why.** The data chat's provenance check (03922e8c7) compared `real_research/data/rc100_nestorshachar2023_table3.csv` with the paper's Table 3 and found 16 rows differing in 17 cells "
      "(12 values, 5 names). Seven rows carry log M_bulge where log M_baryon belongs (58, 62, 63, 65, 77, 93, 95), rows 24 and 90 have small log M_baryon typos, V_c is wrong in rows 43 and 44, "
      "f_DM in row 36, and names in rows 24, 31, 32, 34 and 96. z, R_e and σ₀ match in all 100. I re-derived the difference list independently and it agrees cell for cell.", "",
      "**What was run.** The three lanes' scripts with `RC100_INPUT=corrected`, which reads `data_assembly/rc100_provenance/rc100_table3_six_fields_paper_values.csv`. "
      "The default (uncorrected) runs still reproduce the committed outputs, which are kept. The corrected outputs are `*_corrected*`. "
      "**The corrected file lacks no column the lanes used** (name, z, log M_bar, R_e, f_DM, V_c, σ₀); it lacks the original's derived columns (g_Re, a0 columns, deepMOND flag), which were not used.", "",
      "**Which cells enter which lane.**", "",
      "- The primary statistic of CFG216 and CFG217's baseline use z, R_e, V_c and f_DM only. V_c rows 43 and 44 and f_DM row 36 enter them.",
      "- M_bar enters only CFG216's variant (d), CFG217's M★ reconstruction (C-recon, G1's reconstruction, G2 through Δ_prior) and CFG218's b_RC100.",
      "- The names enter the RC41-overlap matching (38 of 41 before; 41 of 41 now).", "",
      "## What moves materially", ""] + ["- " + m for m in material] + ["",
      "## Every quantity compared (\"moves\" marks any difference in the printed value, including third-decimal noise)", "",
      "| lane | quantity | original | corrected | |", "|---|---|---|---|---|"]
for r in rows:
    md.append("| " + " | ".join(x.replace("|", "/") if i == 1 else x for i, x in enumerate(r)) + " |")
open(os.path.join(LANE, "INPUT_CORRECTION_2026-09-29.md"), "w").write("\n".join(md) + "\n")
print("\n".join(f"{r[0]:14s} {r[1][:88]:88s} | {r[2][:44]:44s} | {r[3][:44]:44s} {r[4]}" for r in rows))
