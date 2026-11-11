#!/usr/bin/env python3
"""BX1 regrade (FROZEN_CRITERIA.md 21e1c07e9a, sections 5-8): KL1 Part C's gate with BX1's fixed-amplitude paired splice.
KL1's scripts are executed UNCHANGED from their source and never written to:
  groups legacy / deskids: kl1c.py up to its "rows (frozen order)" marker (Part B's loader, C3's per-bin alignment, C0's
          load200 / PZV, A2's covariance at the model, run_row, show), with __file__ = KL1's kl1c.py;
  group polish: kl1c_polish.py up to its "RES = dict(" line (AMENDMENT C3's polished DES scan), with KL1's load200 body copied
          verbatim below (it is not in kl1c_polish.py).
kl1_lib is imported from KL1's folder with bytecode writing off. BX1's splices enter as extra PZV entries read through load200
(KL1 Part C's R2 rule: the S0 node replaced for k < 0.5 by the 200 Mpc/h spectrum, log-log interpolated).
Rows: KA4 (R2 = CFG411 reproduces KL1's stored GATE_R2), KA5 (the splice writer, legacy group), GATE_BX1 (pair A, graded),
MB1 (pair A x 0.9 below k 0.5), C3b_BX1 (legacy), and reported splices (pair A run alone, pair B, pairs A + B, 256^3 pairs A / B).
The KiDS-Legacy release is untrusted data: run with python3 -I.
  OMP_NUM_THREADS=1 nice -n 10 python3 -I bx1_regrade.py <footing> <legacy|deskids|polish> <release folder>   -> parts/bx1_<footing>_<group>.json
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, time, io, contextlib
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); KL1 = os.path.abspath(os.path.join(HERE, "..", "KL1_lensing_amplitude_survey_assumptions"))
FT, GRP, REL = sys.argv[1], sys.argv[2], os.path.abspath(sys.argv[3]); assert GRP in ("legacy", "deskids", "polish")
import numpy as np
T0 = time.time(); LOG = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)
OUTF = os.path.join(HERE, "parts", f"bx1_{FT}_{GRP}.json"); os.makedirs(os.path.dirname(OUTF), exist_ok=True)
SPL = {"BX1_A": "bx1_splice_pairA_N512.json", "BX1_Asingle": "bx1_splice_runA_N512_noinv.json", "BX1_B": "bx1_splice_pairB_N512.json",
       "BX1_AB": "bx1_splice_pairsAB_N512.json", "BX1_A256": "bx1_splice_pairA_N256.json", "BX1_B256": "bx1_splice_pairB_N256.json", "KA5_411": "bx1_splice_KA5_cfg411.json"}

if GRP in ("legacy", "deskids"):
    src = open(os.path.join(KL1, "kl1c.py")).read(); cut = src.index("# ------------------------------------------------------------------ rows (frozen order)")
    NS = {"__file__": os.path.join(KL1, "kl1c.py"), "__name__": "kl1c_lib"}; sys.argv = [os.path.join(KL1, "kl1c.py"), FT, GRP, REL]
    exec(compile(src[:cut], os.path.join(KL1, "kl1c.py"), "exec"), NS)
    K, PZ0, PZV, load200, run_row, show, S8_NU, K1 = (NS[x] for x in ("K", "PZ0", "PZV", "load200", "run_row", "show", "S8_NU", "K1"))
else:
    src = open(os.path.join(KL1, "kl1c_polish.py")).read(); cut = src.index("RES = dict(")
    NS = {"__file__": os.path.join(KL1, "kl1c_polish.py"), "__name__": "kl1c_polish_lib"}; sys.argv = [os.path.join(KL1, "kl1c_polish.py"), FT]
    exec(compile(src[:cut], os.path.join(KL1, "kl1c_polish.py"), "exec"), NS)
    K, PZ0, PZV, K1, G, S8_NU, R, scan_polished = (NS[x] for x in ("K", "PZ0", "PZV", "K1", "G", "S8", "R", "scan_polished"))
    def load200(rel):                                             # copied verbatim from kl1c.py (C0's R2 / R2b rule)
        J2 = json.load(open(os.path.join(G["EXT"], *rel))); S2 = J2["snap"]; k2 = np.array(S2["z0"]["k"])
        def splice(z, key):
            p2 = np.exp(np.interp(np.log(K), np.log(k2), np.log(np.array(S2[key]["P"])))); out = PZ0[z].copy(); m = K < 0.5; out[m] = p2[m]; return out
        return {0.0: splice(0.0, "z0"), 0.5: splice(0.5, "z0.5"), 1.0: splice(1.0, "z1")}
    PZV["R2"] = load200(("cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json"))
for key, fn in SPL.items():
    f = os.path.join(HERE, fn)
    if os.path.exists(f): PZV[key] = load200((f,))
if "BX1_A" in PZV: PZV["BX1_A_x09"] = {z: np.where(K < 0.5, 0.9 * v, v) for z, v in PZV["BX1_A"].items()}

RES = json.load(open(OUTF)) if os.path.exists(OUTF) else dict(lane="BX1", criteria="21e1c07e9a", foot=FT, group=GRP, target_sigma8=S8_NU, KA={}, rows={},
                                                              note="kappa = 1/2 FITTED; not theory closed; adopts nothing; gravity-only S0; inherited halo list in R")
RES["splices_present"] = sorted(k for k in PZV if isinstance(k, str) and (k.startswith("BX1") or k == "KA5_411"))
def save():
    json.dump(RES, open(OUTF, "w"), indent=1, default=float)
P(f"BX1 regrade [{FT}, {GRP}]: target sigma8 {S8_NU:.4f}; splices present: {RES['splices_present']}")

if GRP == "legacy" and "KA5_411" in PZV and "KA5" not in RES["KA"]:
    d = max(float(np.max(np.abs(PZV["KA5_411"][z] - PZV["R2"][z]))) for z in PZV["R2"])
    RES["KA"]["KA5"] = dict(max_abs=d, pass_=bool(d == 0.0)); P(f"  KA5 splice writer: load200(my file built from CFG411) - load200(CFG411) max |d| = {d:.1e} -> {'PASS' if d == 0 else 'FAIL'}"); save()

if GRP in ("legacy", "deskids"):
    BASE = dict(s8=S8_NU, R="A3_AD", cov=2.0)                    # KL1 Part C's gate settings (C2 AD; covariance at the model)
    SPEC = [("GATE_R2", dict(BASE, pz="R2")),                    # KA4 first
            ("GATE_BX1", dict(BASE, pz="BX1_A")), ("MB1_x09", dict(BASE, pz="BX1_A_x09"))]
    if GRP == "legacy": SPEC += [("C3b_BX1", dict(BASE, pz="BX1_A", c3="b"))]
    SPEC += [("REP_Asingle", dict(BASE, pz="BX1_Asingle")), ("REP_B", dict(BASE, pz="BX1_B")), ("REP_AB", dict(BASE, pz="BX1_AB")),
             ("REP_A256", dict(BASE, pz="BX1_A256")), ("REP_B256", dict(BASE, pz="BX1_B256"))]
    SNS = ["Legacy"] if GRP == "legacy" else ["DES", "KiDS"]
    KLP = json.load(open(os.path.join(KL1, "parts", f"partc_{FT}_{GRP}.json")))
    for name, st in SPEC:
        if st["pz"] not in PZV: P(f"  {name}: splice {st['pz']} not present, skipped"); continue
        for sn in SNS:
            key = f"{name}|{sn}"
            if key in RES["rows"]: continue
            o = run_row(sn, st); RES["rows"][key] = o; show(name, sn, o)
            if name == "GATE_R2":
                ref = KLP["rows"][f"GATE_R2|{sn}"]; dg = o["gap_widths"] - ref["gap_widths"]; dc = o["at_target"]["chi2"] - ref["at_target"]["chi2"]
                RES["KA"][f"KA4_{sn}"] = dict(gap=o["gap_widths"], ref_gap=ref["gap_widths"], d_gap=dg, d_chi2=dc, pass_=bool(abs(dg) <= 0.01 and abs(dc) <= 0.01))
                P(f"  KA4 {sn}: GATE_R2 gap {o['gap_widths']:.4f} against KL1's {ref['gap_widths']:.4f} (d {dg:+.1e}), chi2 d {dc:+.1e} -> {'PASS' if RES['KA'][f'KA4_{sn}']['pass_'] else 'FAIL'}")
            save()
    K1.setP(PZ0)
else:
    PP = json.load(open(os.path.join(KL1, "parts", f"polish_{FT}.json")))
    SPEC = [("CHECK_R1", "R1"), ("GATE_BX1", "BX1_A"), ("MB1_x09", "BX1_A_x09"), ("REP_R2", "R2"), ("REP_Asingle", "BX1_Asingle"), ("REP_B", "BX1_B"),
            ("REP_AB", "BX1_AB"), ("REP_A256", "BX1_A256"), ("REP_B256", "BX1_B256")]
    for name, pz in SPEC:
        key = f"{name}|DES"
        if key in RES["rows"]: continue
        if pz not in PZV: P(f"  {name}: splice {pz} not present, skipped"); continue
        o = scan_polished(R["A3_AD"], pz); RES["rows"][key] = o
        P(f"  [{FT}] DES {name} polished: target chi2 {o['target_chi2']:.3f} (data {o['target_chi2_data']:.3f}), p {o['p']:.3f} {o['label']}; best {o['best_sigma8']:.4f} +- {o['width']:.4f}, gap {o['gap_widths']:+.2f}   [{time.time() - T0:.0f} s]")
        if name == "CHECK_R1":
            ref = PP["rows"]["GATE"]; RES["KA"]["polish_replay_R1"] = dict(gap=o["gap_widths"], ref=ref["gap_widths"], d=o["gap_widths"] - ref["gap_widths"], reported_only=True)
            P(f"  pipeline check (reported): polished R1 gate {o['gap_widths']:.4f} against KL1 AMENDMENT C3's {ref['gap_widths']:.4f}")
        save()
    K1.setP(PZ0)
P(f"done ({time.time() - T0:.0f} s)")
open(OUTF.replace(".json", ".out"), "a").write("\n".join(LOG) + "\n")
