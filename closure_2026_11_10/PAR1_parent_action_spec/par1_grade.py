"""PAR1 grader: applies FROZEN_CRITERIA.md (51522963e0) and AMENDMENT A1 (427bc818f6) to the outputs.
Run after par1_spec.py (+ MU1-MU3), par1_numbers.py (+ MU4) and the two Lean compiles.
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json

J = lambda f: json.load(open(f))
sp_ = J("par1_spec.json"); nu = J("par1_numbers.json")
mu = {m: J(f"par1_spec_MUTATE_{m}.json") for m in ("MU1", "MU2", "MU3")}
mu4 = J("par1_numbers_MUTATE_MU4.json")
lean = open("compile.txt").read(); leanm = open("compile_MUTATE.txt").read()
G = {}; L = []


def chk(k, ok, note=""):
    G[k] = bool(ok); L.append(f"{k}: {'PASS' if ok else 'FAIL'}" + (f"   [{note}]" if note else ""))


# known answers
chk("KA_S1_LFS1", sp_["S1c_residual_E3_vs_LFS1_form"] == "0" and sp_["S1d_residual_spherical_zero_shift"] == "0"
    and sp_["S1a_net_charge_with_Y0_YR_zero"] == "0", "net zero; Y frozen; E3 form")
chk("KA_S2_EW2", round(sp_["S2_muR_at_eps"], 1) == 12.3 and round(sp_["S2_window_gap_mu_w_over_mu_h"]) == 159
    and sp_["S2_bound_check_residual"] == "0", f"mu R = {sp_['S2_muR_at_eps']}, gap {sp_['S2_window_gap_mu_w_over_mu_h']}")
chk("KA_S3_X14", sp_["S3_residual_vs_X14"] == "0" and sp_["S3_tau_fold_residual"] == "0", "tau_f = w/(K Sigma_b)")
chk("KA_S4_TPA1", sp_["S4_residual_vs_TPA1"] == "0", "K nbar/(1 + k^2/mu_K^2)")
chk("KA_S12_REL1", sp_["S12_REL1_root_residual"] == "0", "runaway root")
KA = all(G[k] for k in G if k.startswith("KA_"))
# MUTATE
chk("MU1_bites", mu["MU1"]["S5_residual_vs_TSCR"] != "0" and mu["MU1"]["S5_minus_omega2_at_A0_is_positive"] is False,
    "Jeans support returns without the polarization charge")
chk("MU2_bites", mu["MU2"]["S8_coeff_D3"] == "0", "Chaplygin: no energy defect")
chk("MU3_bites", eval(mu["MU3"]["S7_model_span_over_half_c0sq_at_10n0"]) > 1, "convex EOS exceeds the span bound")
chk("MU4_bites", mu4["S15_R_at_s0_check"] == 1.0 and all(v is None for k, v in mu4["S15"].items()
                                                        if k.startswith("s_half")), "no fluctuation: R = 1 everywhere")
chk("Lean_main_exit0", lean.strip().endswith("exit 0") and lean.count("depends on axioms: [propext, Classical.choice, Quot.sound]") == 8)
chk("Lean_twin_fails", leanm.strip().endswith("exit 1") and leanm.count(": error") >= 5)
MUT_OK = all(G[k] for k in ("MU1_bites", "MU2_bites", "MU3_bites", "MU4_bites", "Lean_main_exit0", "Lean_twin_fails"))

# spec items used by the branches
S5 = sp_["S5_residual_vs_TSCR"] == "0" and sp_["S5_minus_omega2_at_A0_is_positive"] is True \
    and sp_["S5_kJ2_equals_Kchi_residual"] == "0" and sp_["S5_charge_conservation_residual"] == "0" \
    and sp_["S5_J_second_at_0"] == "1/K"
S6 = "Phi_inf + hbar - Phi" in sp_["S6_h_matched"]
S7 = sp_["S7_model_span_minus_bound"] == "0" and eval(sp_["S7_model_span_over_half_c0sq_at_10n0"]) <= 1 \
    and sp_["S7_P2tau_identity_residual"] == "0"
S8_frozen = sp_["S8_coeff_D3_residual_frozen_sign"] == "0"
S8_A1 = sp_["S8_coeff_D3_residual_A1_sign"] == "0"
S9 = nu["S9_line_depth10_gt_half_cbar2_forest_all"] is True
L0 = "Jg" not in sp_["L0_FRW_charge"]
for k, v in (("S5_TSCR", S5), ("S6_TDEP", S6), ("S7_TSPAN", S7), ("S8_TSHK_as_frozen", S8_frozen),
             ("S8_TSHK_A1", S8_A1), ("S9_TTRI_line", S9), ("Lemma0_FRW", L0)):
    chk(k, v)

out = {"checks": G}
for reading, s8 in (("frozen", S8_frozen), ("A1", S8_A1)):
    br = {}
    for foot in ("canonical", "alt"):
        b = {
            "B0": "EMPTY" if L0 else "OPEN",
            "B-L": "EMPTY" if G["KA_S2_EW2"] else "OPEN",
            "B-Ts": "EMPTY" if (S5 and S6 and S7 and s8 and S9) else "OPEN",
            "B-Tm-fine": "EMPTY" if nu["S15_branch_fine_EMPTY_by_frozen_rule"][foot] else "OPEN",
            "B-Tm-smooth": "OPEN",
        }
        if not (KA and MUT_OK):
            lab = "NO VERDICT"
        elif all(v == "EMPTY" for v in b.values()):
            lab = "CLASS EMPTY"
        else:
            lab = "NO VERDICT"  # an OPEN branch with no member written and graded in this lane
        br[foot] = {"branches": b, "label": lab}
    out[reading] = br
    L.append(f"[{reading}] canonical: {br['canonical']['label']} {br['canonical']['branches']}")
    L.append(f"[{reading}] alt:       {br['alt']['label']} {br['alt']['branches']}")
json.dump(out, open("par1_grade.json", "w"), indent=1)
open("par1_grade.out", "w").write("PAR1 grade (criteria 51522963e0, A1 427bc818f6)\n" + "\n".join(L) +
                                  "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
print("\n".join(L))

# Adopts nothing. kappa = 1/2 FITTED; not theory closed.
