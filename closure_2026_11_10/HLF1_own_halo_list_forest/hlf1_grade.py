#!/usr/bin/env python3
"""HLF1 copy of closure_2026_11_09/CO1_form_b_cosmology_computed/co1_grade.py (CO1 commit 020522140a lineage), unchanged except: input / output
file names carry the halo list HLF1_LIST=inherited|own (HLF1 FROZEN_CRITERIA 123947b9dc, A.3). Original docstring follows.
CO1 (FROZEN_CRITERIA.md 020522140a, AMENDMENT_A1 5e1496298d): assemble the rows and the label from the three parts.
  python3 co1_grade.py   -> co1.json, co1.out      (after co1_hm.py, co1_linear.py, co1_shear.py)
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
LIST = os.environ.get("HLF1_LIST", "inherited")
HM, LIN, SH = (json.load(open(os.path.join(HERE, f))) for f in (f"hlf1_hm_{LIST}.json", f"hlf1_linear_{LIST}.json", f"hlf1_shear_{LIST}.json"))
K = np.array(HM["k"]); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
RES = dict(lane="CO1", criteria="020522140a", amendment_A1="5e1496298d", note="kappa = 1/2 FITTED; not theory closed; adopts nothing; inherited halo list",
           rows={}, labels={}, KA={}, MUTATE={})
P("CO1: form B's cosmology rows, computed (canonical / alt). kappa = 1/2 FITTED; not theory closed; adopts nothing.")
KA = dict(KA1=all(v["pass_"] for v in HM["KA"]["KA1"].values()), KA2=all(v["pass_"] for v in HM["KA"]["KA2"].values()), KA3=HM["KA"]["KA3"]["pass_"],
          KA4=all(v["pass_"] for v in SH["KA"]["KA4"].values()), KA5=LIN["KA"]["KA5"]["pass_"], KA6=all(v["pass_"] for v in LIN["KA"]["KA6"].values()),
          KA7=HM["KA"]["KA7"]["pass_"], KA_limber=all(v["pass_"] for v in LIN["KA"]["KA_limber"].values()))
RES["KA"] = KA
P("Known answers: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in KA.items()))
MU = {}
for ft in ("canonical", "alt"):
    m4 = HM["MUTATE"]["M4"][ft]; rb = np.interp(1.0, K, np.array(HM["primary"][ft]["R_bar"])); stat = float(np.interp(1.0, K, np.array(m4["R_tot"])) / rb)
    MU[ft] = dict(M1=SH["MUTATE"]["M1"][ft]["KiDS"]["bites"], M1_d=SH["MUTATE"]["M1"][ft]["KiDS"]["d"], M2=LIN["MUTATE"]["M2"][ft]["bites"], M2_r_eff=LIN["MUTATE"]["M2"][ft]["r_eff"],
                  M3=LIN["MUTATE"]["M3"][ft]["bites"], M3_Delta=LIN["MUTATE"]["M3"][ft]["Delta_cal"], M4_as_frozen=m4["bites"], M4_as_frozen_rise=m4["rise"],
                  M4_restated_A1=bool(stat - m4["primary"] >= 0.10), M4_restated_stat=stat, M4_primary=m4["primary"])
RES["MUTATE"] = MU
P("MUTATE: " + "; ".join(f"{ft}: M1 KiDS d {v['M1_d']:+.1f} {'bites' if v['M1'] else 'NO BITE'}, M2 r_eff {v['M2_r_eff']:.4f} {'bites' if v['M2'] else 'NO BITE'}, "
                         f"M3 Delta_cal {v['M3_Delta']:+.0f} {'bites' if v['M3'] else 'NO BITE'}, M4 as frozen {v['M4_as_frozen_rise']:+.3f} {'bites' if v['M4_as_frozen'] else 'DOES NOT BITE'}, "
                         f"M4 restated (A1) {v['M4_restated_stat']:.3f} vs {v['M4_primary']:.3f} {'bites' if v['M4_restated_A1'] else 'NO BITE'}" for ft, v in MU.items()))
P("")
P(f"{'row':44s} | {'canonical':38s} | {'alt':38s} | line")
def line(name, fn, ln):
    P(f"{name:44s} | {fn('canonical'):38s} | {fn('alt'):38s} | {ln}")
line("C1 primary CMB, PA chi2 - chi2_cal", lambda f: f"{LIN['C1'][f]['Delta_cal']:+.2f} (chi2 {LIN['C1'][f]['PA']:.2f}) {LIN['C1'][f]['status']}", "<= 9")
line("   cold / baryon at that fit (fitted)", lambda f: f"{LIN['C1'][f]['R_cold_to_baryon']:.3f}", "reported")
line("C2 PR4 lensing amplitude A (data / pred.)", lambda f: f"{LIN['C2'][f]['A']:.4f} +- {LIN['C2'][f]['sigma_A']:.4f} ({LIN['C2'][f]['pull']:+.2f} sigma)", "|pull| <= 2")
line("C2 PR4 lensing shape chi2 (9 bandpowers)", lambda f: f"{LIN['C2'][f]['chi2_shape']:.2f} {LIN['C2'][f]['status']}", "<= 18.48")
line("C3 DESI DR1 f sigma8, chi2 SF / SF+BAO", lambda f: f"{LIN['C3'][f]['chi2_SF']:.2f} / {LIN['C3'][f]['chi2_SFB']:.2f}, max |pull| "
     f"{max(max(abs(r['pull_SF']), abs(r['pull_SFB'])) for r in LIN['C3'][f]['rows']):.2f} {LIN['C3'][f]['status']}", "every |pull| <= 2")
line("   sigma8 at that fit (S0 engine 0.811)", lambda f: f"{LIN['C3'][f]['sigma8']:.4f}", "reported")
line("R_cold at k = 1 / 3 / 5 h/Mpc", lambda f: " / ".join(f"{HM['primary'][f]['R_cold_at'][k]:.3f}" for k in ("1.0", "3.0", "5.0")), "reported")
line("C4 lensing with redistribution, r_eff - 1", lambda f: f"{LIN['C4'][f]['primary']['r_eff'] - 1:+.5f} {LIN['C4'][f]['status']}", f"|.| <= {LIN['C4']['canonical']['line']:.4f}")
line("C5 raw KiDS d_cold (N 104)", lambda f: f"{SH['C5'][f]['d_cold']:+.2f} {SH['C5'][f]['label']}", "klass")
line("   robust: widen2 / noIA / fade / DESI", lambda f: " / ".join(f"{SH['C5'][f]['robust'][k]:+.2f}" for k in ("widen2", "noIA", "fade", "DESI")), "all < 9")
line("   tooth chi2_min (null)", lambda f: f"{SH['C5'][f]['tooth_chi2']:.2f} ({SH['C5'][f]['tooth_null_chi2']:.2f}) {'VISIBLE' if SH['C5'][f]['visible'] else 'NOT VISIBLE'}", ">= 9 visible")
line("   KiDS chi2: S0 / S0 x R_bar / S0 x R_tot", lambda f: f"{SH['C5'][f]['chi2_S0']:.2f} / {SH['C5'][f]['chi2_bar']:.2f} / {SH['C5'][f]['chi2_tot']:.2f}", "reported")
line("   p of the same", lambda f: f"{SH['C5'][f]['p_S0']:.4f} / {SH['C5'][f]['p_bar']:.4f} / {SH['C5'][f]['p_tot']:.4f}", "reported")
line("   KiDS at the fit's own sigma8: chi2, p", lambda f: f"{SH['brackets'][f]['amplitude_sigma8_of_C3']['chi2_tot']:.2f}, p {SH['brackets'][f]['amplitude_sigma8_of_C3']['p_tot']:.1e}", "bracket")
line("   DES Y3 d_cold (N 52; reported)", lambda f: f"{SH['DES_reported'][f]['d_cold']:+.2f} {SH['DES_reported'][f]['label']}", "reported")
P("")
ka_ok = all(KA.values())
for ft in ("canonical", "alt"):
    c = {k: LIN[k][ft]["status"] == "PASS" for k in ("C1", "C2", "C3", "C4")}; c5 = SH["C5"][ft]["label"]; mu = MU[ft]
    mut_frozen = mu["M1"] and mu["M2"] and mu["M3"] and mu["M4_as_frozen"]; mut_A1 = mu["M1"] and mu["M2"] and mu["M3"] and mu["M4_restated_A1"]
    if not ka_ok or not mut_A1: lab = "NO VERDICT"
    elif not (c["C1"] and c["C2"] and c["C3"]): lab = "LINEAR ROW FAILS (" + ", ".join(k for k in ("C1", "C2", "C3") if not c[k]) + ")"
    elif c5 == "EXCLUDED" or not c["C4"]: lab = "REDISTRIBUTION EXCLUDED"
    elif c5 == "TENSION": lab = "ROWS HOLD, REDISTRIBUTION IN TENSION"
    elif c5 == "CONSISTENT": lab = "ROWS HOLD"
    else: lab = "ROWS HOLD ON C1-C4; C5 NOT DIAGNOSTIC"
    RES["labels"][ft] = dict(label=lab + ", with an inherited halo list", rows=c, C5=c5, mutations_bite_as_frozen=bool(mut_frozen), mutations_bite_under_A1=bool(mut_A1),
                             label_if_M4_read_as_frozen="NO VERDICT" if not mut_frozen else lab)
    P(f"LABEL {ft}: {lab}, with an inherited halo list.   (read with M4 as frozen, which did not bite: {RES['labels'][ft]['label_if_M4_read_as_frozen']})")
RES["rows"] = dict(C1=LIN["C1"], C2=LIN["C2"], C3={f: {k: v for k, v in LIN["C3"][f].items()} for f in LIN["C3"]}, C4=LIN["C4"], C5=SH["C5"], DES_reported=SH["DES_reported"],
                   R_cold_at={f: HM["primary"][f]["R_cold_at"] for f in HM["primary"]}, brackets_R_cold_k1={f: {n: b["R_cold_at"]["1.0"] for n, b in HM["brackets"][f].items()} for f in HM["brackets"]},
                   brackets_KiDS_d_cold={f: {n: b["d_cold"] for n, b in SH["brackets"][f].items()} for f in SH["brackets"]}, posthoc=SH.get("posthoc", {}))
json.dump(RES, open(os.path.join(HERE, f"hlf1_rows_{LIST}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"hlf1_rows_{LIST}.out"), "w").write("\n".join(OUT) + "\n")
