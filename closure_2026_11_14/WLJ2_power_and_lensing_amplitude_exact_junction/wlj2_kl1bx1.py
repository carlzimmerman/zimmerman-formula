#!/usr/bin/env python3
"""WLJ2 (FROZEN_CRITERIA.md, c3bc2d3871) part 4: G-KL1 and G-BX1 for REF, ADOPT, S2 and the exact-junction cases. COPY of WLJ1's
wlj1_kl1bx1.py (closure_2026_11_13/WLJ1_power_and_lensing_amplitude_with_split/) with only the case list and its order (ADOPT first, for the
known answers), the twin and bracket case (Ec2 in the place of S2) and KA-X2 changed; it reads wlj2_hm.json. WLJ1's docstring follows.
WLJ1 (FROZEN_CRITERIA.md, 03f9823de7) part 4: gates G-KL1 (KL1 Part C: C0 R1 + C2 A3_AD) and G-BX1 (the same gate with BX1's 512^3
pair-A splice) for REF, ADOPT and SPLIT, as BX1's bx1_regrade.py runs them: KL1's kl1c.py up to its "rows (frozen order)" marker and
kl1c_polish.py up to its "RES = dict(" line are executed UNCHANGED from their own folder (never written to), kl1_lib imported from there
with bytecode off; BX1's splice enters through KL1's own load200 (KL1 Part C's R2 rule). The case's gate R is A3_AD x [R_tot,case /
R_tot,ADOPT] (frozen transfer rule; z = 0, held); bracket: additive transfer at f = 2. KL1's make_ctx keeps CO1's R_tot (the gate's
fiducial covariance). The KiDS-Legacy release is untrusted data: run with python3 -I, the release folder passed as an argument.
  OMP_NUM_THREADS=1 nice -n 19 python3 -I -B wlj2_kl1bx1.py <footing> <legacy|deskids|polish> <release folder>
      -> parts/wlj2_kl1bx1_<footing>_<group>.json / .out   (twins TW-B, TW-L in the same file under "twins", copied to *_MUTATE at grading)
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, time
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
KL1 = os.path.join(REPO, "closure_2026_11_10", "KL1_lensing_amplitude_survey_assumptions"); BX1 = os.path.join(REPO, "closure_2026_11_10", "BX1_fixed_amplitude_reference")
FT, GRP, REL = sys.argv[1], sys.argv[2], os.path.abspath(sys.argv[3]); assert GRP in ("legacy", "deskids", "polish")
sys.path.insert(0, KL1)
import numpy as np
T0 = time.time(); LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)
OUTF = os.path.join(HERE, "parts", f"wlj2_kl1bx1_{FT}_{GRP}.json"); os.makedirs(os.path.dirname(OUTF), exist_ok=True)
if GRP in ("legacy", "deskids"):
    src = open(os.path.join(KL1, "kl1c.py")).read(); cut = src.index("# ------------------------------------------------------------------ rows (frozen order)")
    NS = {"__file__": os.path.join(KL1, "kl1c.py"), "__name__": "kl1c_lib"}; sys.argv = [os.path.join(KL1, "kl1c.py"), FT, GRP, REL]
    exec(compile(src[:cut], os.path.join(KL1, "kl1c.py"), "exec"), NS)
    K, PZ0, PZV, load200, run_row, S8, K1, R = (NS[x] for x in ("K", "PZ0", "PZV", "load200", "run_row", "S8_NU", "K1", "R"))
else:
    src = open(os.path.join(KL1, "kl1c_polish.py")).read(); cut = src.index("RES = dict(")
    NS = {"__file__": os.path.join(KL1, "kl1c_polish.py"), "__name__": "kl1c_polish_lib"}; sys.argv = [os.path.join(KL1, "kl1c_polish.py"), FT]
    exec(compile(src[:cut], os.path.join(KL1, "kl1c_polish.py"), "exec"), NS)
    K, PZ0, PZV, K1, G, S8, R, scan_polished = (NS[x] for x in ("K", "PZ0", "PZV", "K1", "G", "S8", "R", "scan_polished"))
    def load200(rel):                                             # copied verbatim from kl1c.py (C0's R2 / R2b rule), as bx1_regrade.py does
        J2 = json.load(open(os.path.join(G["EXT"], *rel))); S2 = J2["snap"]; k2 = np.array(S2["z0"]["k"])
        def splice(z, key):
            p2 = np.exp(np.interp(np.log(K), np.log(k2), np.log(np.array(S2[key]["P"])))); out = PZ0[z].copy(); m = K < 0.5; out[m] = p2[m]; return out
        return {0.0: splice(0.0, "z0"), 0.5: splice(0.5, "z0.5"), 1.0: splice(1.0, "z1")}
PZV["BX1_A"] = load200((os.path.join(BX1, "bx1_splice_pairA_N512.json"),))

# ------------------------------------------------------------------ the cases' gate R (transfer rule)
HM = json.load(open(os.path.join(HERE, "wlj2_hm.json"))); MU = json.load(open(os.path.join(HERE, "wlj2_hm_MUTATE.json")))
W1P = json.load(open(os.path.join(REPO, "closure_2026_11_13", "WLJ1_power_and_lensing_amplitude_with_split", "parts", f"wlj1_kl1bx1_{FT}_{GRP}.json")))
A3 = np.array(R["A3_AD"]); assert len(A3) == len(HM["k"])
RTA = np.array(HM["cases"][f"ADOPT|{FT}|0.0"]["R_tot"])
def rtot(cs):
    if cs == "REF": return np.array(HM["cases"][f"ADOPT|{FT}|0.0"]["R_bar"])
    if cs == "TWL":
        a = HM["cases"][f"Ec2|{FT}|0.0"]; return np.array(a["R_bar"]) * (1 + 2 * (np.array(a["R_cold"]) - 1))
    if cs == "TWB": return np.array(MU["TWB"][f"TWB|{FT}|0.0"]["R_tot"])
    return np.array(HM["cases"][f"{cs}|{FT}|0.0"]["R_tot"])
CASES = ["ADOPT", "REF", "S2", "Ec3", "Ec2", "E0.5", "E0.75", "E1"]; TWINS = ["TWL", "TWB"]; LAST = ["E2"]
for cs in CASES + TWINS + LAST:
    R[f"A3_AD|{cs}"] = A3 * rtot(cs) / RTA
R["A3_AD|Ec2|additive"] = A3 + (rtot("Ec2") - RTA); R["A3_AD|REF|additive"] = A3 + (rtot("REF") - RTA)
P(f"WLJ2 G-KL1 / G-BX1 [{FT}, {GRP}]: target sigma8 {S8:.4f}; transfer factor at k 1 / 3: " + "; ".join(f"{cs} {np.interp(1.0, HM['k'], rtot(cs) / RTA):.5f}/{np.interp(3.0, HM['k'], rtot(cs) / RTA):.5f}" for cs in CASES + TWINS + LAST))

RES = json.load(open(OUTF)) if os.path.exists(OUTF) else dict(lane="WLJ2", criteria="c3bc2d3871", foot=FT, group=GRP, target_sigma8=S8, rows={}, KA={},
                                                              note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
def save(): json.dump(RES, open(OUTF, "w"), indent=1, default=float)
if GRP in ("legacy", "deskids"):
    SNS = ["Legacy"] if GRP == "legacy" else ["DES", "KiDS"]
    BASE = dict(s8=S8, cov=2.0)
    SPEC = []
    for cs in CASES + TWINS + LAST:
        SPEC += [(f"GATE|{cs}", dict(BASE, R=f"A3_AD|{cs}", pz="R1")), (f"GATE_BX1|{cs}", dict(BASE, R=f"A3_AD|{cs}", pz="BX1_A"))]
        if GRP == "legacy" and cs not in TWINS: SPEC += [(f"C3b|{cs}", dict(BASE, R=f"A3_AD|{cs}", pz="R1", c3="b")), (f"C3b_BX1|{cs}", dict(BASE, R=f"A3_AD|{cs}", pz="BX1_A", c3="b"))]
    for cs in ("REF", "ADOPT", "Ec2"):
        SPEC += [(f"GATE_R2|{cs}", dict(BASE, R=f"A3_AD|{cs}", pz="R2")), (f"GATE_R2b|{cs}", dict(BASE, R=f"A3_AD|{cs}", pz="R2b"))]
    for cs in ("REF", "Ec2"):
        SPEC += [(f"GATE|{cs}|additive", dict(BASE, R=f"A3_AD|{cs}|additive", pz="R1")), (f"GATE_BX1|{cs}|additive", dict(BASE, R=f"A3_AD|{cs}|additive", pz="BX1_A"))]
    for name, st in SPEC:
        for sn in SNS:
            key = f"{name}|{sn}"
            if key in RES["rows"]: continue
            o = run_row(sn, st); RES["rows"][key] = o
            m = o["at_target"]
            P(f"  {name:24s} {sn:6s}: chi2 {m['chi2']:.3f} p {m['p']:.3f} {m['label']}; best {o['best_sigma8']:.4f} +- {o['width']:.4f}, gap {o['gap_widths']:+.3f}   [{time.time() - T0:.0f} s]")
            save()
    KLP = json.load(open(os.path.join(KL1, "parts", f"partc_{FT}_{GRP}.json"))); BXP = json.load(open(os.path.join(BX1, "parts", f"bx1_{FT}_{GRP}.json")))
    pairs = [(f"GATE|ADOPT|{sn}", KLP["rows"][f"GATE|{sn}"]) for sn in SNS] + [(f"GATE_BX1|ADOPT|{sn}", BXP["rows"][f"GATE_BX1|{sn}"]) for sn in SNS]
    if GRP == "legacy": pairs += [("C3b|ADOPT|Legacy", KLP["rows"]["C3b_own_prior|Legacy"]), ("C3b_BX1|ADOPT|Legacy", BXP["rows"]["C3b_BX1|Legacy"])]
    pairs += [(f"GATE_R2|ADOPT|{sn}", KLP["rows"][f"GATE_R2|{sn}"]) for sn in SNS] + [(f"GATE_R2b|ADOPT|{sn}", KLP["rows"][f"GATE_R2b|{sn}"]) for sn in SNS]
    for mine, ref in pairs:
        o = RES["rows"][mine]; dg = o["gap_widths"] - ref["gap_widths"]; dc = o["at_target"]["chi2"] - ref["at_target"]["chi2"]
        RES["KA"][mine] = dict(gap=o["gap_widths"], ref_gap=ref["gap_widths"], d_gap=dg, d_chi2=dc, pass_=bool(abs(dg) <= 0.01 and abs(dc) <= 0.01))
        P(f"  KA ADOPT {mine}: gap {o['gap_widths']:.4f} against the stored {ref['gap_widths']:.4f} (d {dg:+.1e}), chi2 d {dc:+.1e} -> {'PASS' if RES['KA'][mine]['pass_'] else 'FAIL'}")
    kx = {}
    for nm in [x for x in RES["rows"] if any(x.startswith(f"{g}|{c}|") for g in ("GATE", "GATE_BX1", "C3b", "C3b_BX1", "GATE_R2", "GATE_R2b") for c in ("REF", "ADOPT", "S2"))]:
        if nm in W1P["rows"]:
            o, w = RES["rows"][nm], W1P["rows"][nm]; kx[nm] = dict(d_gap=o["gap_widths"] - w["gap_widths"], d_chi2=o["at_target"]["chi2"] - w["at_target"]["chi2"],
                                                                   pass_=bool(abs(o["gap_widths"] - w["gap_widths"]) <= 0.01 and abs(o["at_target"]["chi2"] - w["at_target"]["chi2"]) <= 0.01))
    RES["KA_X2"] = kx
    P("  KA-X2 vs WLJ1's stored part: " + "; ".join(f"{k} d_gap {v['d_gap']:+.1e} -> {'PASS' if v['pass_'] else 'FAIL'}" for k, v in kx.items()))
    K1.setP(PZ0)
else:
    for cs in CASES + TWINS + LAST + ["Ec2|additive", "REF|additive"]:
        for pz, nm in (("R1", "GATE"), ("BX1_A", "GATE_BX1")):
            key = f"{nm}|{cs}|DES"
            if key in RES["rows"]: continue
            o = scan_polished(R[f"A3_AD|{cs}"], pz); RES["rows"][key] = o
            P(f"  [{FT}] DES {key:28s} polished: target chi2 {o['target_chi2']:.3f}, p {o['p']:.3f} {o['label']}; best {o['best_sigma8']:.4f} +- {o['width']:.4f}, gap {o['gap_widths']:+.3f}   [{time.time() - T0:.0f} s]")
            save()
    PP = json.load(open(os.path.join(KL1, "parts", f"polish_{FT}.json"))); BXP = json.load(open(os.path.join(BX1, "parts", f"bx1_{FT}_polish.json")))
    for mine, ref in (("GATE|ADOPT|DES", PP["rows"]["GATE"]), ("GATE_BX1|ADOPT|DES", BXP["rows"]["GATE_BX1|DES"])):
        o = RES["rows"][mine]; dg = o["gap_widths"] - ref["gap_widths"]; dc = o["target_chi2"] - ref["target_chi2"]
        RES["KA"][mine] = dict(gap=o["gap_widths"], ref_gap=ref["gap_widths"], d_gap=dg, d_chi2=dc, pass_=bool(abs(dg) <= 0.01 and abs(dc) <= 0.01))
        P(f"  KA ADOPT {mine}: gap {o['gap_widths']:.4f} against the stored {ref['gap_widths']:.4f} (d {dg:+.1e}), target chi2 d {dc:+.1e} -> {'PASS' if RES['KA'][mine]['pass_'] else 'FAIL'}")
    kx = {}
    for nm in [x for x in RES["rows"] if any(x.startswith(f"{g}|{c}|") for g in ("GATE", "GATE_BX1") for c in ("REF", "ADOPT", "S2"))]:
        if nm in W1P["rows"]:
            o, w = RES["rows"][nm], W1P["rows"][nm]; kx[nm] = dict(d_gap=o["gap_widths"] - w["gap_widths"], d_chi2=o["target_chi2"] - w["target_chi2"],
                                                                   pass_=bool(abs(o["gap_widths"] - w["gap_widths"]) <= 0.01 and abs(o["target_chi2"] - w["target_chi2"]) <= 0.01))
    RES["KA_X2"] = kx
    P("  KA-X2 vs WLJ1's stored part: " + "; ".join(f"{k} d_gap {v['d_gap']:+.1e} -> {'PASS' if v['pass_'] else 'FAIL'}" for k, v in kx.items()))
    K1.setP(PZ0)
save()
P(f"done ({time.time() - T0:.0f} s)")
open(OUTF.replace(".json", ".out"), "w").write("\n".join(LOG) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
