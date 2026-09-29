# -*- coding: utf-8 -*-
"""CFG172 verdict -- reads the results JSONs and prints the gate table per sub-variant (no new physics except the inert-window test of sec. 1.2)."""
from cfg172_common import *

def J(n):
    return json.load(open(os.path.join(HERE, n + "_results.json")))
A1, A2, A3, A4, A5, A6, A7, A8 = (J(n) for n in ("CFG172_A1_static_reductions", "CFG172_A2_stability_pincer", "CFG172_A3_ppn_frame", "CFG172_A4_growth",
                                               "CFG172_A5_reaction_energy", "CFG172_A6_b_operating_point", "CFG172_A7_c_response", "CFG172_A8_stress_energy"))
v = lambda J_, k: J_["verdicts"][k]["status"]
# inert-window test for 11C-c beta: G1(full) at 10 x the G3 ceiling
Kc = A7["numbers"]["G3_Kc_ceiling"]
def dev_full(Kfac):
    mx = 0
    for f in FOOT:
        a0 = A0[f]
        for M in MASSES:
            r_, gN = profile_gN(M, "exp", a0)
            tar = nu_p2(gN / a0) * gN
            drho = rho_exp(M, r_) / H_EXP
            mx = max(mx, float(np.max(np.abs((tar + Kfac * Kc * drho) / tar - 1))))
    return mx
d1, d10, d1e3 = dev_full(1.0), dev_full(10.0), dev_full(1000.0)
print(f"11C-c full: G1 deviation with the contact force at 1x / 10x / 1000x the G3 ceiling K_c: {d1:.3f} / {d10:.3f} / {d1e3:.3f}")
beta_inert = (d1e3 <= 0.10)
T = {}
T["11C-a"] = {
 "G1 law": ("PASS", "A1 (max dev 5e-14; declared kernel)"),
 "G1 mechanism": ("P-declared (not M2)", "A1"),
 "G2 (cold ON)": ("FAIL", f"A4 (worst |G_eff/G-1| = {A4['numbers']['G2']['11C-a/-c (P2)']['worst_1sigma']:.0e}; CMB part UNDEFINED)"),
 "G2 (no-cold, labelled)": ("FAIL", "A8 (baryon-only growth ratio %.2f; rho_ae = 0 on FRW)" % A8["numbers"]["nocold_growth"]["ratio"]),
 "G3": ("FAIL", "A5 (reaction PASS by construction; energy 14-240x orbital)"),
 "G4 strict / inert-window": ("FAIL (1 constant: c2) / PASS (0 counted)", "A6, A3 (verdicts invariant over c2 in [5.3e-5, 6.3e-4])"),
 "G5": ("FAIL", f"A2 (Q2/bound = {A2['numbers']['Q2_over_bound_sun_saturn']['Sun@Saturn/P2/canonical']:.1e}; pincer >= {A2['numbers']['pincer_min_tail']['P2']['Q2_over_bound_canonical']:.1e}; kinetic sign PASS; hyperbolicity UNDEFINED)"),
 "G6 (alpha1 lines 3.4e-5 / 3.5e-5 / 2.1e-5)": ("PASS (three alpha1 lines agree)", "A3 (isolated; quoted formulas)"),
 "G7": ("UNDEFINED", "A3 (KM1-modelling: PASS iff c2 >= 2.7e-5..5.3e-5; nonlinear transfer not derived)"),
 "S2": ("PASS", "A8")}
T["11C-b"] = {
 "G1 law": ("FAIL", f"A6 (G1 needs t <= 1.2e-6 [4e-4 mirrored]; G6, G7 need t >= {A3['numbers']['t_min_in_G6G7_allowed_set']:.0e})"),
 "G1 mechanism": ("FAIL", "A6"),
 "G2 (cold ON)": ("FAIL where G1 passes (t <= 1.2e-6); PASS only at t >= ~1e6 where G1 fails", "A4"),
 "G2 (no-cold, labelled)": ("FAIL", "A8 (rho_ae/rho_req = 1e-3..1.6e-2, negative; growth ratio 0.22)"),
 "G3": ("FAIL", "A5 (energy)"),
 "G4 strict / inert-window": ("FAIL (1) / PASS (0 counted: verdicts F for every c2)", "A3, A6"),
 "G5": ("FAIL", "A2 ((y q_eff)' < 0 for t > 0; Q2 tail as 11C-a)"),
 "G6 (alpha1 lines 3.4e-5 / 3.5e-5 / 2.1e-5)": ("FAIL at every c2 the tie allows for G7 (three lines agree; alpha_2 binds)", "A3"),
 "G7": ("FAIL at every c2 the tie allows for G6", "A3"),
 "S2": ("PASS", "A8")}
T["11C-c"] = {
 "G1 law": ("PASS (full, inherited from the a-channel) / FAIL (theta-only)", "A7"),
 "G1 mechanism": ("FAIL", "A7 (no kernel from the coupling; local, linear in M_b)"),
 "G2 (cold ON)": ("FAIL", "A4 (same a-channel as 11C-a)"),
 "G2 (no-cold, labelled)": ("FAIL", "A8"),
 "G3": ("FAIL", f"A5, A7 (reaction PASS only for K_c <= {Kc:.1e}; energy FAIL)"),
 "G4 strict / inert-window": ("FAIL (2: c2, beta) / " + ("PASS (0)" if beta_inert else "FAIL (1 counted: beta)"), "A7, verdict script"),
 "G5": ("FAIL", "A7 (c_s^2 = -K_c rho < 0; c2 < 0 ghost) and A2 (tail)"),
 "G6 (alpha1 lines 3.4e-5 / 3.5e-5 / 2.1e-5)": ("PASS (three alpha1 lines agree)", "A3"),
 "G7": ("UNDEFINED", "A3"),
 "S2": ("PASS with caveat (coupling changes the baryons' mass)", "A8")}
gates = list(T["11C-a"].keys())
out = ["| gate | 11C-a | 11C-b | 11C-c |", "|---|---|---|---|"]
for g_ in gates:
    out.append(f"| {g_} | " + " | ".join(f"{T[k][g_][0]} [{T[k][g_][1]}]" for k in ("11C-a", "11C-b", "11C-c")) + " |")
print("\n".join(out))
json.dump({"table": T, "beta_inert": beta_inert, "G1_full_dev_at_Kc_mult": [d1, d10, d1e3]}, open(os.path.join(HERE, "CFG172_verdict_results.json"), "w"), indent=1, default=str)
