"""AGB1 collector: applies the checks and the frozen words of FROZEN_CRITERIA.md to the outputs of agb1_run.py and
agb1_reread.py. Reads JSON only; fits nothing."""
import os, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
LGS1 = os.path.join(HERE, "..", "LGS1_legacy_sn_dropped")
C684 = os.path.join(REPO, "campaign_fresh_gravity", "CFG684_bao_cc_sn_robust", "cfg684_results.json")
out = {"lane": "AGB1"}


def load(name, folder=HERE):
    p = os.path.join(folder, name)
    return json.load(open(p)) if os.path.exists(p) else None


def w1(d0, d1):
    if d1 >= 9 and d0 < 4: return "AGE BIAS EXCLUDED AT 3 SIGMA"
    if 4 <= d1 < 9 and d0 < 4: return "AGE BIAS DISFAVOURED"
    if d0 >= 9 and d1 < 4: return "AGE BIAS REQUIRED AT 3 SIGMA"
    if 4 <= d0 < 9 and d1 < 4: return "AGE BIAS FAVOURED"
    if d0 < 4 and d1 < 4: return "UNDECIDED"
    return "NEITHER"


def w2(q0, d):
    if d >= 4 and q0 < 0: return "ACCELERATING TODAY"
    if d >= 4 and q0 > 0: return "DECELERATING TODAY"
    return "SIGN NOT SETTLED"


def w3(d):
    if d >= 9: return "NEVER-ACCELERATED EXCLUDED AT 3 SIGMA"
    if d >= 4: return "NEVER-ACCELERATED DISFAVOURED"
    return "NEVER-ACCELERATED ALLOWED"


def fmt_ci(ci):
    return "[" + ", ".join("none" if v is None else f"{v:+.3f}" for v in ci) + "]"


# ---------------- checks ----------------
chk = {}
for k in ("KT", "K1", "K2", "K4", "K3a", "K3b"):
    r = load(f"agb1_{k}.json"); chk[k] = None if r is None else bool(r["passed"])
af = load("agb1_A_full.json")
if af is not None:
    S = af["summary"]
    chk["KA"] = bool(abs(S["A_spline"] - S["A_free"]) <= 0.03 and abs(S["chi2_spline"] - S["chi2_free"]) <= 0.05)
    out["KA"] = dict(A_spline=S["A_spline"], A_free=S["A_free"], chi2_spline=S["chi2_spline"], chi2_free=S["chi2_free"])
else:
    chk["KA"] = None
partA_ok = all(chk[k] is True for k in ("KT", "K1", "K2", "K4", "K3a", "K3b", "KA"))
print("CHECKS (Part A): " + "  ".join(f"{k} {'NOT RUN' if v is None else ('PASS' if v else 'FAIL')}" for k, v in chk.items())
      + f"   -> Part A words {'EVALUABLE' if partA_ok else 'NOT EVALUABLE'}")
for k in ("K1", "K2"):
    r = load(f"agb1_{k}.json")
    if r: print(f"   {k}: Om {r['Om']:.4f}" + (f"  h r_d {r['hrd']:.2f} Mpc" if "hrd" in r else "") + f"  target {r['target']}")
out["checks_A"] = chk; out["partA_evaluable"] = partA_ok


def block(tag, r, forks=True):
    """Summary row of an A-profile run, with the words."""
    if r is None:
        print(f"   {tag}: NOT RUN"); return None
    S = r["summary"]; f = r["free"]
    row = dict(n_sn=r.get("n_sn"), A=S["A_free"], ci68=S["ci68"], ci95=S["ci95"], D_A0=S["D_A0"], D_A1=S["D_A1"],
               W1=w1(S["D_A0"], S["D_A1"]), free=dict(Om=f["Om"], w0=f["w0"], wa=f["wa"], q0=f["q0"], chi2=f["chi2"], edge=f["edge"]))
    if "D_A023" in S: row["D_A023"] = S["D_A023"]
    print(f"   {tag} (n {r.get('n_sn')}): A {S['A_free']:+.3f}  68% {fmt_ci(S['ci68'])}  95% {fmt_ci(S['ci95'])}"
          f"  dchi2(A=0) {S['D_A0']:.2f}  dchi2(A=1) {S['D_A1']:.2f}"
          + (f"  dchi2(A=0.23) {S['D_A023']:.2f}" if "D_A023" in S else "") + f"  -> {row['W1']}")
    if forks and "forks" in r:
        row["forks"] = {}
        for name in ("A0", "A1", "Afree"):
            k = r["forks"][name]; b = k["base"]
            row["forks"][name] = dict(Om=b["Om"], w0=b["w0"], wa=b["wa"], q0=b["q0"], qmin=b["qmin"], z_qmin=b["z_qmin"],
                                      chi2=b["chi2"], chi2_bao=b["chi2_bao"], chi2_sn=b["chi2_sn"], chi2_prior=b.get("chi2_prior"),
                                      hrd=b.get("hrd"), h=b.get("h"), A=b["coef"].get("age"), edge=b["edge"],
                                      D_today=k["D_today"], D_never=k["D_never"], W2=w2(b["q0"], k["D_today"]), W3=w3(k["D_never"]),
                                      never=dict(Om=k["never"]["Om"], w0=k["never"]["w0"], wa=k["never"]["wa"], qmin=k["never"]["qmin"]))
            x = row["forks"][name]
            print(f"      fork {name:5s}: Om {x['Om']:.4f} w0 {x['w0']:+.3f} wa {x['wa']:+.3f} q0 {x['q0']:+.3f} (min q {x['qmin']:+.3f} at z {x['z_qmin']:.2f})"
                  f"  chi2 {x['chi2']:.2f}{'  EDGE ' + str(x['edge']) if x['edge'] else ''}")
            print(f"                  today: dchi2(q0=0) {x['D_today']:.2f} -> {x['W2']};  ever: dchi2(never) {x['D_never']:.2f} -> {x['W3']}")
    return row


# ---------------- Part A ----------------
print("\nPART A - BAO + supernovae, no CMB, template T_S")
A = {s: block(s, load(f"agb1_A_{s}.json")) for s in ("full", "des_only", "rand197", "bao_overlap")}
if A["full"]:
    changed = [s for s in ("des_only", "bao_overlap") if A[s] is None or A[s]["W1"] != A["full"]["W1"]]
    A["second_word"] = "ROBUST" if not changed else "FRAGILE (" + ", ".join(changed) + ")"
    A["W1"] = A["full"]["W1"] + " / " + A["second_word"] if partA_ok else "NOT EVALUABLE"
    print(f"   W1 (full): {A['full']['W1']} / {A['second_word']}" + ("" if partA_ok else "   [checks failed: NOT EVALUABLE; reading only]"))
    if A["rand197"] and A["des_only"]:
        print(f"   control: rand197 gives {A['rand197']['W1']}; des_only gives {A['des_only']['W1']}")
out["A"] = A

# ---------------- reported: template W, legacy offset ----------------
print("\nREPORTED - template T_W (short-delay age history, same 0.030 mag/Gyr)")
out["W"] = {s: block(s, load(f"agb1_W_{s}.json"), forks=False) for s in ("full", "des_only")}
print("\nREPORTED - legacy offset in the place of, and beside, the age template (full sample)")
L = load("agb1_L_full.json")
if L is None:
    print("   NOT RUN")
else:
    so = L["step_only"]
    print(f"   offset alone (A = 0): delta {so['delta']:+.4f} mag (legacy minus DES, same model)  dchi2(delta=0) {so['D_delta0']:.2f}"
          f"  -> w0 {so['step']['w0']:+.3f} wa {so['step']['wa']:+.3f} q0 {so['step']['q0']:+.3f}")
    row = block("A with delta free", L, forks=False); row["delta_at_A_free"] = L["delta_at_A_free"]
    row["step_only"] = dict(delta=so["delta"], D_delta0=so["D_delta0"], w0=so["step"]["w0"], wa=so["step"]["wa"], q0=so["step"]["q0"],
                            Om=so["step"]["Om"])
    print(f"      delta at the A-free minimum {L['delta_at_A_free']:+.4f} mag")
    out["L"] = row

# ---------------- Part C ----------------
print("\nPART C - with DESI's compressed CMB prior (inherited early-universe physics)")
k5 = load("agb1_C_K5.json"); cf = load("agb1_C_full.json"); chkC = {"K5": None if k5 is None else bool(k5["passed"]), "K6": None}
if k5: print(f"   K5: dchi2(w0wa - LCDM) {k5['dchi2']:+.2f} (target -8.0 +- 1.0); BAO + prior alone: w0 {k5['w0wa']['w0']:+.3f} wa {k5['w0wa']['wa']:+.3f}"
             f" q0 {k5['w0wa']['q0']:+.3f}")
if cf is not None:
    b = cf["forks"]["A0"]["base"]; chkC["K6"] = bool(abs(b["w0"] + 0.803) <= 0.040 and abs(b["wa"] + 0.72) <= 0.16)
    print(f"   K6: full, A = 0: w0 {b['w0']:+.4f} (target -0.803 +- 0.040)  wa {b['wa']:+.4f} (target -0.72 +- 0.16)")
partC_ok = all(v is True for v in chkC.values())
print("   CHECKS (Part C): " + "  ".join(f"{k} {'NOT RUN' if v is None else ('PASS' if v else 'FAIL')}" for k, v in chkC.items())
      + f"   -> Part C words {'EVALUABLE' if partC_ok else 'NOT EVALUABLE'}")
C = {s: block(s, load(f"agb1_C_{s}.json")) for s in ("full", "des_only")}
if C["full"]:
    same = C["des_only"] is not None and C["des_only"]["W1"] == C["full"]["W1"]
    C["second_word"] = "ROBUST" if same else "FRAGILE (des_only)"
    C["W1c"] = C["full"]["W1"] + " / " + C["second_word"] if partC_ok else "NOT EVALUABLE"
    print(f"   W1c (full): {C['full']['W1']} / {C['second_word']}" + ("" if partC_ok else "   [checks failed: NOT EVALUABLE; reading only]"))
out["C"] = C; out["checks_C"] = chkC; out["partC_evaluable"] = partC_ok

# ---------------- Part B: CFG684 ----------------
print("\nPART B - CFG684 and CFG689 re-read with the correction at A = 1 (each against A = 0 of the same sample)")
ZS684 = ["1.0", "1.5", "2.33"]; ZS689 = ["1.0", "1.2", "1.5", "2.33"]; B = {}


def flat684(o):
    v = [o["dchi2_max"], o["flat_a0_om"]["mean"], o["flat_a0_om"]["sd"]]
    for z in ZS684: v += o[z]["rival"] + o[z]["tracking"]
    return np.array(v, float)


h = load("agb1_cfg684_full_A0.json"); ref = json.load(open(C684))
if h is None:
    B["cfg684_harness"] = "NOT RUN"
else:
    d = max(float(np.max(np.abs(flat684(h[c]) - flat684(ref[c])))) for c in ("BAO+DES5", "BAO+DES5+CC"))
    B["cfg684_harness_max_abs_diff"] = d; B["cfg684_harness"] = "PASS" if d <= 1e-6 else "FAIL"
print(f"   CFG684 harness (full, A = 0, vs committed cfg684_results.json): {B['cfg684_harness']}"
      + (f"  max |diff| {B['cfg684_harness_max_abs_diff']:.2e}" if "cfg684_harness_max_abs_diff" in B else ""))
B["cfg684"] = {}
for s in ("full", "des_only"):
    a0 = load(f"lgs1_cfg684_{s}.json", LGS1); a1 = load(f"agb1_cfg684_{s}_A1.json")
    if a0 is None or a1 is None:
        print(f"   CFG684 {s}: NOT RUN"); continue
    B["cfg684"][s] = {}
    for c in ("BAO+DES5", "BAO+DES5+CC"):
        p, q = a0[c], a1[c]; shift = q["flat_a0_om"]["mean"] - p["flat_a0_om"]["mean"]
        comb = float(np.hypot(p["flat_a0_om"]["sd"], q["flat_a0_om"]["sd"]))
        lab = dict(n=a1["n_des5"], om_A0=p["flat_a0_om"]["mean"], sd_A0=p["flat_a0_om"]["sd"], om_A1=q["flat_a0_om"]["mean"],
                   sd_A1=q["flat_a0_om"]["sd"], shift=shift, combined_sd=comb, dchi2_max_A0=p["dchi2_max"], dchi2_max_A1=q["dchi2_max"],
                   A1="DEGENERACY BROKEN" if q["dchi2_max"] >= 4 else "NOT BROKEN",
                   A2="ROBUST" if abs(shift) <= comb else "AGE-DEPENDENT",
                   A3="FLOOR HOLDS" if q["2.33"]["tracking"][0] > 0 else "FLOOR LOST",
                   tracking_A0={z: p[z]["tracking"] for z in ZS684}, tracking_A1={z: q[z]["tracking"] for z in ZS684},
                   e3_A0={z: p[z]["e3"] for z in ZS684}, e3_A1={z: q[z]["e3"] for z in ZS684})
        if B["cfg684_harness"] != "PASS": lab.update(A1="NOT EVALUABLE", A2="NOT EVALUABLE", A3="NOT EVALUABLE")
        B["cfg684"][s][c] = lab
        print(f"   CFG684 {s:8s} {c:12s}: flat-a0 Om {lab['om_A0']:.4f} +- {lab['sd_A0']:.4f} -> {lab['om_A1']:.4f} +- {lab['sd_A1']:.4f}"
              f" (shift {shift:+.4f}, combined sd {comb:.4f}) -> A2 {lab['A2']};  dchi2_max {p['dchi2_max']:.2f} -> {q['dchi2_max']:.2f} A1 {lab['A1']};"
              f"  sqrtX(2.33) {p['2.33']['tracking'][0]:.3f}-{p['2.33']['tracking'][1]:.3f} -> {q['2.33']['tracking'][0]:.3f}-{q['2.33']['tracking'][1]:.3f} A3 {lab['A3']}")

# ---------------- Part B: CFG689 ----------------
hh = load("agb1_cfg689_TD5F_des_only_A0.json"); h0 = load("lgs1_cfg689_TD5F_des_only.json", LGS1)
if hh is None or h0 is None:
    B["cfg689_harness"] = "NOT RUN"
else:
    d = max(float(np.max(np.abs(np.array(hh["BAO+SN"]["P1"][z]["sqrtX_q"]) - np.array(h0["BAO+SN"]["P1"][z]["sqrtX_q"])))) for z in ZS689)
    B["cfg689_harness_max_abs_diff"] = d; B["cfg689_harness"] = "PASS" if d <= 0.005 else "FAIL"
print(f"   CFG689 harness (TD5F, des_only, A = 0, vs LGS1's committed file): {B['cfg689_harness']}"
      + (f"  max |diff| {B['cfg689_harness_max_abs_diff']:.2e}" if "cfg689_harness_max_abs_diff" in B else ""))
B["cfg689"] = {}
for mode in ("D5", "TD5F"):
    B["cfg689"][mode] = {}
    for s in ("full", "des_only"):
        a0 = load(f"lgs1_cfg689_{mode}_{s}.json", LGS1); a1 = load(f"agb1_cfg689_{mode}_{s}_A1.json")
        if a0 is None or a1 is None:
            print(f"   CFG689 {mode} {s}: NOT RUN"); B["cfg689"][mode][s] = "NOT RUN"; continue
        p, q = a0["BAO+SN"], a1["BAO+SN"]; m = dict(nstep=a1["nstep"], K4_ok=q["K4"]["ok"], z={})
        ev = B["cfg689_harness"] == "PASS" and q["K4"]["ok"] and a1["nstep"] == 60000
        for z in ZS689:
            qa, qb = np.array(p["P1"][z]["sqrtX_q"]), np.array(q["P1"][z]["sqrtX_q"])
            stable = (qa[1] <= qb[2] <= qa[3]) and (qb[1] <= qa[2] <= qb[3])
            m["z"][z] = dict(A0_68=[qa[1], qa[3]], A0_median=qa[2], A1_68=[qb[1], qb[3]], A1_median=qb[2],
                             B1=("STABLE" if stable else "SHIFTED") if ev else "NOT EVALUABLE",
                             e3_A0=p["P1"][z]["e_3sigma"], e3_A1=q["P1"][z]["e_3sigma"])
            print(f"   CFG689 {mode:4s} {s:8s} z*={z}: tracking sqrtX 68% [{qa[1]:.3f}, {qa[3]:.3f}] med {qa[2]:.3f} -> [{qb[1]:.3f}, {qb[3]:.3f}] med {qb[2]:.3f}"
                  f" -> B1 {m['z'][z]['B1']};  e_3sigma {p['P1'][z]['e_3sigma']:.3f} -> {q['P1'][z]['e_3sigma']:.3f}")
        cls0 = (p["P1_class"], (p["P0"] or {}).get("P0_class")); cls1 = (q["P1_class"], (q["P0"] or {}).get("P0_class"))
        m["P1_class"] = dict(A0=cls0[0], A1=cls1[0]); m["P0_class"] = dict(A0=cls0[1], A1=cls1[1])
        m["B2"] = ("CLASS UNCHANGED" if cls0 == cls1 else "CLASS CHANGED") if ev else "NOT EVALUABLE"
        m["P2"] = dict(A0=dict(dchi2=p["P2"]["dchi2"], sigma=p["P2"]["sigma_equiv"], cls=p["P2"].get("P2_class")),
                       A1=dict(dchi2=q["P2"]["dchi2"], sigma=q["P2"]["sigma_equiv"], cls=q["P2"].get("P2_class")))
        m["H0_q"] = dict(A0=p["P3"]["H0_q"], A1=q["P3"]["H0_q"])
        print(f"   CFG689 {mode:4s} {s:8s}: B2 {m['B2']} (P1 {cls0[0]} -> {cls1[0]}; P0 {cls0[1]} -> {cls1[1]});"
              f"  P2 {p['P2']['dchi2']:.2f} ({p['P2']['sigma_equiv']:.2f} sigma, {p['P2'].get('P2_class')}) -> {q['P2']['dchi2']:.2f}"
              f" ({q['P2']['sigma_equiv']:.2f} sigma, {q['P2'].get('P2_class')});  native H0 {p['P3']['H0_q'][2]:.2f} -> {q['P3']['H0_q'][2]:.2f};  K4 ok {q['K4']['ok']}")
        B["cfg689"][mode][s] = m
out["B"] = B
json.dump(out, open(os.path.join(HERE, "agb1_results.json"), "w"), indent=1, default=float)
print("\nwrote agb1_results.json")
