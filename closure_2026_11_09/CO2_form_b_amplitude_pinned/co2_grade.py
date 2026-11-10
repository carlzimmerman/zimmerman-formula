#!/usr/bin/env python3
"""CO2 (FROZEN_CRITERIA.md 2bd776c60d, AMENDMENT_A1 b6dd6d0641): assemble the rows and the label.
  python3 co2_grade.py   -> co2.json, co2.out      (after co2_fit.py x 2, co2_rows.py, co2_shear.py)
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
RW, SH = (json.load(open(os.path.join(HERE, f))) for f in ("co2_rows.json", "co2_shear.json"))
FOOTS = ("canonical", "alt"); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
TAIL = "for form B as stated, gravity-only S0, nothing ejecting gas beyond R200c; inherited halo list in R"
KA = dict(KA1=RW["KA"]["KA1"]["pass_"], KA2=RW["KA"]["KA2"]["pass_"], KA3=all(v["pass_"] for v in RW["KA"]["KA3"].values()),
          KA4=all(v["pass_"] for v in SH["KA"]["KA4"].values()), KA5=all(v["pass_"] for v in SH["KA"]["KA5"].values()))
MU = {ft: dict(M1=RW["MUTATE"]["M1"][ft]["bites"], M1_rise=RW["MUTATE"]["M1"][ft]["rise"], M2=SH["MUTATE"]["M2"][ft]["bites"], M2_p=SH["MUTATE"]["M2"][ft]["p"],
               M3=SH["MUTATE"]["M3"][ft]["bites"], M3_applies=SH["MUTATE"]["M3"][ft]["applies"]) for ft in FOOTS}
RES = dict(lane="CO2", criteria="2bd776c60d", amendment_A1="b6dd6d0641", note="kappa = 1/2 FITTED; not theory closed; adopts nothing", KA=KA, MUTATE=MU, labels={}, rows={})
P("CO2: form B's amplitude pinned with Planck 2018 low-L EE, against lensing (canonical / alt). kappa = 1/2 FITTED; not theory closed.")
P("Known answers: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in KA.items()))
P("MUTATE: " + "; ".join(f"{ft}: M1 chi2_E +{v['M1_rise']:.1f} {'bites' if v['M1'] else 'NO BITE'}, M2 p {v['M2_p']:.1e} {'bites' if v['M2'] else 'NO BITE'}, "
                         f"M3 {'bites' if v['M3'] else 'NO BITE'}{'' if v['M3_applies'] else ' (not applicable: pinned sigma8 below 0.811)'}" for ft, v in MU.items()))
P("")
P(f"{'row':46s} | {'canonical':40s} | {'alt':40s} | line")
def line(name, fn, ln): P(f"{name:46s} | {fn('canonical'):40s} | {fn('alt'):40s} | {ln}")
F, P1, P2, P3, P4 = RW["fit"], RW["P1"], RW["P2"], RW["P3"], SH["P4"]
line("tau (width along the degeneracy)", lambda f: f"{F[f]['tau']:.4f} +- {F[f]['tau_sigma_along_degeneracy']:.4f} (was {F[f]['unpinned']['tau']:.4f})", "reported")
line("ln 1e10 A_s; cold / baryon", lambda f: f"{F[f]['pars']['lnA']:.4f} (was {F[f]['unpinned']['lnA']:.4f}); {F[f]['cold_to_baryon']:.3f}", "reported")
line("chi2: PA / low-L EE (change from unpinned)", lambda f: f"{F[f]['PA']:.2f} ({F[f]['dPA']:+.2f}) / {F[f]['E']:.2f} ({F[f]['dE']:+.2f})", "reported")
line("P1 pinned fit adequate, Delta_cal'", lambda f: f"{P1[f]['Delta_cal']:+.2f} {P1[f]['status']}", "<= 9")
line("sigma8 (unpinned; S0 engine 0.811)", lambda f: f"{P2[f]['sigma8']:.4f} ({P2[f]['CO1_unpinned']['sigma8']:.4f}); S8 {P2[f]['S8']:.4f}", "reported")
line("P2 PR4 lensing amplitude (data / prediction)", lambda f: f"{P2[f]['A']:.4f} +- {P2[f]['sigma_A']:.4f} ({P2[f]['pull']:+.2f} sigma) {P2[f]['status']}", "|pull| <= 2")
line("   shape chi2; chi2 at A = 1", lambda f: f"{P2[f]['chi2_shape']:.2f}; {P2[f]['chi2_at_A1']:.2f}", "<= 18.48")
line("P3 DESI DR1 f sigma8, chi2 SF / SF+BAO", lambda f: f"{P3[f]['chi2_SF']:.2f} / {P3[f]['chi2_SFB']:.2f} {P3[f]['status']}", "every |pull| <= 2")
line("P4 raw KiDS, S0 x R_tot, own response", lambda f: f"chi2 {P4[f]['chi2']:.2f}, p {P4[f]['p']:.2e} {P4[f]['label']}", "p lines")
line("   constant factor (bracket)", lambda f: f"chi2 {P4[f]['constant_factor']['chi2']:.2f}, p {P4[f]['constant_factor']['p']:.2e}", "bracket")
line("   S0 alone / S0 x R_bar, own response", lambda f: f"{P4[f]['S0_alone']['chi2']:.2f} / {P4[f]['S0_x_R_bar']['chi2']:.2f}", "reported")
line("   KiDS's own best sigma8 for this spectrum", lambda f: f"{SH['scan'][f]['best_sigma8']:.4f} +- {SH['scan'][f]['width_dchi2_1']:.4f} (p {SH['scan'][f]['best_fit']['p']:.3f})", "reported")
line("   pinned minus best, in widths; Delta chi2", lambda f: f"{SH['scan'][f]['pinned_minus_best_in_widths']:+.2f}; {SH['scan'][f]['dchi2_pinned_vs_best']:+.2f}", "reported")
line("   bracket: one 0.06 eV neutrino", lambda f: f"sigma8 {SH['brackets'][f]['one_0p06eV_neutrino']['sigma8']:.4f}, p {SH['brackets'][f]['one_0p06eV_neutrino']['p']:.2e}", "bracket")
line("   bracket: prefactor-0 layout", lambda f: f"chi2 {SH['brackets'][f]['prefactor_0_layout']['chi2']:.2f}, p {SH['brackets'][f]['prefactor_0_layout']['p']:.2e}", "bracket")
line("   bracket: unpinned sigma8, own response", lambda f: f"chi2 {SH['brackets'][f]['unpinned_sigma8_response']['chi2']:.2f}, p {SH['brackets'][f]['unpinned_sigma8_response']['p']:.2e}", "bracket")
line("   DES Y3 pinned (reported)", lambda f: f"chi2 {SH['DES_reported'][f]['pinned']['chi2']:.2f}, p {SH['DES_reported'][f]['pinned']['p']:.3f}", "reported")
P("")
for ft in FOOTS:
    ok = dict(P1=P1[ft]["status"] == "PASS", P2=P2[ft]["status"] == "PASS", P3=P3[ft]["status"] == "PASS"); l4 = P4[ft]["label"]
    if not all(KA.values()) or not (MU[ft]["M1"] and MU[ft]["M2"] and MU[ft]["M3"]): lab = "NO VERDICT"
    elif not ok["P1"]: lab = "PINNED FIT INADEQUATE"
    elif not ok["P2"]: lab = "LENSING ROW FAILS"
    elif not ok["P3"]: lab = "GROWTH ROW FAILS"
    elif l4 == "CONSISTENT": lab = "AMPLITUDE HOLDS"
    elif l4 == "TENSION": lab = "AMPLITUDE IN TENSION WITH RAW KiDS"
    else: lab = "AMPLITUDE EXCLUDED BY RAW KiDS AT 3 SIGMA"
    RES["labels"][ft] = dict(label=lab, rows=ok, P4=l4, tail=TAIL)
    P(f"LABEL {ft}: {lab} ({TAIL}).")
RES["rows"] = dict(fit=F, P1=P1, P2=P2, P3=P3, P4=P4, brackets_rows=RW["brackets"], brackets_shear=SH["brackets"], scan={f: {k: v for k, v in SH["scan"][f].items()} for f in FOOTS},
                   alpha=SH["alpha"], DES_reported=SH["DES_reported"])
json.dump(RES, open(os.path.join(HERE, "co2.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "co2.out"), "w").write("\n".join(OUT) + "\n")
