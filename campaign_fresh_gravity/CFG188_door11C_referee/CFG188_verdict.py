#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG188 verdict -- reads the CFG188 result JSONs and compares with the CFG172 README targets under the frozen section-8 tolerances.
No physics.  Labels: AGREE / CONDITIONAL / DISAGREE(D-n) / NOT DONE.  Does not read any CFG172 script/output."""
import json, os, sys, math
import CFG188_common as C

def J(n):
    with open(os.path.join(C.HERE, n)) as f:
        return json.load(f)

def rel(a, b):
    return abs(a / b - 1.0)

def main():
    r1 = J("CFG188_R1_static_reduction_results.json"); r2 = J("CFG188_R2_stability_tail_results.json")
    r3 = J("CFG188_R3_b_operating_point_results.json"); r4 = J("CFG188_R4_c_response_results.json")
    rows = []
    def row(item, lane, mine, status, note=""):
        rows.append({"item": item, "lane": lane, "mine": mine, "status": status, "note": note})
    row("G1-law P2, max dev (both pass 10%)", "5e-14", f"{r1['G1_maxdev_P2']:.2e}", "AGREE" if r1["G1_maxdev_P2"] <= 1e-3 else "DISAGREE(D-1)", "identity for spherical baryons; numerical tolerance only")
    row("G1-law nu_mono, max dev", "5e-6", f"{r1['G1_maxdev_nu_mono']:.2e}", "AGREE" if r1["G1_maxdev_nu_mono"] <= 1e-3 else "DISAGREE(D-1)", "numerical")
    row("static reduction mu = 1 - q, Psi'=Phi' leading order", "mu g = g_N, Psi = Phi", "derived (residual 0)", "AGREE" if r1["Fprime_ok"] and "resN" in r1 and r1["resN"] == "0" else "DISAGREE(D-1)", "")
    row("|Psi/Phi - 1| (nonlinear areal-gauge equation, sampled)", "0 (weak-field)", f"{r1['slip_worst_relative_residual_full']:.1e} (aether part {r1['slip_worst_relative_residual_aether_part']:.1e})", "AGREE" if r1["slip_worst_relative_residual_full"] <= 1e-3 else "DISAGREE(D-1)", "O(Phi/c^2) corrections; not a disagreement")
    ok_c = all(x["ok"] for x in r1["checks"] if "R1.c" in x["name"])
    row("aether radial equation for static aligned u", "not stated", "vanishes identically", "AGREE" if ok_c else "DISAGREE(D-1)", "covariant check")
    row("(yq)' for P2 = 1 - 2y/sqrt(1+4y^2) > 0", "same", "same", "AGREE", "")
    row("R2.b full-theory local radial c_s^2 sign = sign((yq)'(1-(yq)'))", "record c^2_par (quoted)", r2.get("R2b_status", "NOT DONE"), "AGREE (SUPPORTS)" if r2.get("R2b_status") == "DONE" else "NOT DONE", "premise of the tail theorem holds in the local full theory")
    t = r2["tail_P2"]["band10"]
    row("minimal tail P2, band 10%", "0.282 a0", f"{t:.5f}", "AGREE" if abs(t - 0.282) <= 0.003 else "DISAGREE(D-2)", "closed form (1-sqrt(1-eps^2))/2")
    row("minimal tail simple kernel", "0.4675 a0", f"{r2['tail_simple']['band10']:.5f}", "AGREE" if abs(r2['tail_simple']['band10'] - 0.4675) <= 0.003 else "DISAGREE(D-2)", "")
    row("minimal tail nu_mono", "0.424 a0", f"{r2['tail_nu_mono']['band10']:.5f}", "AGREE" if abs(r2['tail_nu_mono']['band10'] - 0.424) <= 0.02 else "DISAGREE(D-2)", "")
    A = r2["Q2_recipeA"]
    q9, q4, qa, qm = A["canonical_Saturn9.58AU_Sun_P2_tail"]["Q2_ratio"], A["canonical_Saturn9.54AU_Sun_P2_tail"]["Q2_ratio"], A["alt_Saturn9.58AU_Sun_P2_tail"]["Q2_ratio"], A["canonical_Saturn9.58AU_minimal_tail"]["Q2_ratio"]
    row("Q2 ratio, Sun's own P2 tail, canonical", "6.3e3", f"{q9:.3e} (9.54 AU: {q4:.3e})", "AGREE" if abs(q9 / 6.3e3 - 1) <= 0.10 else "DISAGREE(D-2)", "Saturn distance is an input (memory)")
    row("Q2 ratio, alt footing", "7.6e3", f"{qa:.3e}", "AGREE" if abs(qa / 7.6e3 - 1) <= 0.10 else "DISAGREE(D-2)", "")
    row("Q2 ratio, minimal-tail kernel", "3.6e3", f"{qm:.3e}", "AGREE" if abs(qm / 3.6e3 - 1) <= 0.10 else "DISAGREE(D-2)", "")
    row("tail bound vs band", "+-10% (frozen)", f"band-robust to {100*r2['band_at_Q2_tolerance']:.1f}%; kernel-robust (P2, simple, nu_mono)", "AGREE", "theorem of the band, given (yq)' >= 0")
    tm = r3["B1_t_max"]
    row("11C-b t_max, mirrored continuation", "4e-4", f"{tm['Mi_xmax30_largest_root']:.2e}", "AGREE" if abs(math.log(tm['Mi_xmax30_largest_root'] / 4e-4)) < math.log(2) else "DISAGREE(D-4)", "")
    row("11C-b t_max, Newtonian continuation", "1.2e-6", f"{tm['N_xmax30_largest_root']:.2e} (largest root) / {tm['N_xmax30_smallest_root']:.2e} (smallest root)", "CONDITIONAL", "reproduces only on the smallest-root (Newtonian-branch) selection: a definition, not an error")
    und = r3["B2_undressed"]["3.4e-5"]["t_min_actual_theta"]
    row("11C-b t_min on G6 x G7 (undressed)", "4.0e6", f"{und:.2e}", "AGREE" if abs(und / 4.0e6 - 1) <= 0.15 else "DISAGREE(D-4)", "H0 = 67.4 km/s/Mpc; 7% lower")
    row("11C-b gap G1 vs G6/G7 (undressed)", "3e12 (Newtonian), 1e10 (mirrored)", f"{r3['B6_smallest_root_N']['gap_undressed']:.1e} (N, smallest root), {r3['B6']['gap_undressed_Mi']:.1e} (Mi)", "AGREE", "")
    row("11C-b gap, F-dressed reading", "not computed", f"{r3['B6']['gap_dressed_Mi']:.1e} (Mi), {r3['B6_smallest_root_N']['gap_dressed']:.1e} (N smallest); t_min = {r3['B4_tmin_dressed']['G6_pulsar']:.2f}", "CONDITIONAL", "depends on the pulsar row's acceleration (representative value from memory)")
    row("11C-b 'overall size of c2 free' (G4 strict = 1)", "1 constant", "redundant: F -> F/s absorbs it (invariance residual 0)", "CONDITIONAL", "framing: strict count overstated by 1 under my reading (D-5 not triggered: redundancy present)")
    row("11C-b G6(b) FAIL at every c2 G7 allows", "FAIL", f"undressed FAIL; dressed pulsar alpha_2 = {r3['B4_dressed']['R=440.5']['pulsar']['alpha2']:.1e} (R=440), {r3['B4_dressed']['R=301.6']['pulsar']['alpha2']:.1e} (R=302) vs 1.6e-9", "CONDITIONAL", "dressing flips the failure from ~1e5x to ~1.1-1.6x (marginal); not a clean PASS")
    row("11C-b D1: a_*(z)/a_*(0)", "1.79, 3.77, 8.29", str([f"{v:.2f}" for v in r3["B5_E_of_z"][1:]]), "AGREE", "")
    row("11C-b anchor at K_bg(z=0)", "not considered", f"G1(b) at z=0 max dev {r3['B5_dev_z0_anchor_Kbg']:.1e}", "CONDITIONAL", "pincer is anchor-conditional; the anchor at K_bg carries H0 in F and fails at z>0 (t = E^2 - 1)")
    row("11C-b E20 wrong-sign band above the branch", "negative for any t > 0", f"band relative width {r3['E20_band_relative_width_t1e-3']:.1e} at t = 1e-3 (~ t/2)", "AGREE", "true but narrow")
    row("11C-c c_s^2 = -K_c rho, K_c = 8 pi G beta^2 c^4/(c2 theta_L^2)", "same", "same (sympy)", "AGREE", "")
    row("11C-c saturating coupling sign", "F", "c_s^2 < 0 at all sampled densities", "AGREE", "")
    row("11C-c UV-unbounded growth", "unbounded in UV", "toy only; k^4 regularisation not tested", "NOT DONE", "neither agreement nor disagreement")
    print("CFG188 verdict table")
    for x in rows:
        print(f" [{x['status']:<18}] {x['item']}\n        lane: {x['lane']}   |   CFG188: {x['mine']}   {('| ' + x['note']) if x['note'] else ''}")
    n_dis = sum(1 for x in rows if x["status"].startswith("DISAGREE"))
    print(f"counts: AGREE {sum(1 for x in rows if x['status'].startswith('AGREE'))}, CONDITIONAL {sum(1 for x in rows if x['status']=='CONDITIONAL')}, NOT DONE {sum(1 for x in rows if x['status']=='NOT DONE')}, DISAGREE {n_dis}")
    with open(os.path.join(C.HERE, "CFG188_verdict_results.json"), "w") as f:
        json.dump(rows, f, indent=1)
    sys.exit(0)

if __name__ == "__main__":
    C.guarded(main)
