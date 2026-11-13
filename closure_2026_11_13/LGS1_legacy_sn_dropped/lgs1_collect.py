"""LGS1 collector: applies the frozen rules of FROZEN_CRITERIA.md to the outputs of lgs1_run.py. Reads JSON only."""
import os, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
C684 = os.path.join(REPO, "campaign_fresh_gravity", "CFG684_bao_cc_sn_robust", "cfg684_results.json")
C689 = os.path.join(REPO, "campaign_fresh_gravity", "CFG689_native_ruler_bao")
ZS684 = ["1.0", "1.5", "2.33"]
ZS689 = ["1.0", "1.2", "1.5", "2.33"]
out = {"lane": "LGS1"}


def load(name):
    p = os.path.join(HERE, name)
    return json.load(open(p)) if os.path.exists(p) else None


# ---------------- part A: CFG684 ----------------
ref = json.load(open(C684))
runs = {s: load(f"lgs1_cfg684_{s}.json") for s in ("full", "des_only", "rand197")}
A = {}


def flat684(o):
    v = [o["dchi2_max"], o["flat_a0_om"]["mean"], o["flat_a0_om"]["sd"]]
    for z in ZS684:
        v += o[z]["rival"] + o[z]["tracking"]
    return np.array(v, float)


if runs["full"] is None:
    A["harness"] = "NOT RUN"
else:
    d = max(float(np.max(np.abs(flat684(runs["full"][c]) - flat684(ref[c])))) for c in ("BAO+DES5", "BAO+DES5+CC"))
    A["harness_max_abs_diff"] = d
    A["harness"] = "PASS" if d <= 1e-6 else "FAIL"
print(f"A. CFG684 harness check (full sample vs committed cfg684_results.json): {A['harness']}"
      + (f"  max |diff| {A['harness_max_abs_diff']:.2e}" if "harness_max_abs_diff" in A else ""))
for s in ("full", "des_only", "rand197"):
    r = runs[s]
    if r is None:
        print(f"   {s}: NOT RUN"); continue
    A[s] = {"n_des5": r["n_des5"]}
    for c in ("BAO+DES5", "BAO+DES5+CC"):
        o = r[c]; f = o["flat_a0_om"]
        A[s][c] = dict(dchi2_max=o["dchi2_max"], degeneracy="BROKEN" if o["dchi2_max"] >= 4 else "NOT BROKEN",
                       flat_a0_om=f["mean"], flat_a0_sd=f["sd"], crossing=f["crossing"],
                       tracking={z: o[z]["tracking"] for z in ZS684}, rival={z: o[z]["rival"] for z in ZS684},
                       e3={z: o[z]["e3"] for z in ZS684})
        print(f"   {s:9s} n={r['n_des5']:5d} {c:12s} dchi2_max {o['dchi2_max']:.2f} ({A[s][c]['degeneracy']})  "
              f"flat-a0 Om {f['mean']:.4f} +- {f['sd']:.4f}  tracking sqrtX(2.33) {o['2.33']['tracking'][0]:.3f}-{o['2.33']['tracking'][1]:.3f}"
              f"  sqrtX(1.5) {o['1.5']['tracking'][0]:.3f}-{o['1.5']['tracking'][1]:.3f}  e3(2.33) {o['2.33']['e3']}")
if A.get("harness") == "PASS":
    for s in ("des_only", "rand197"):
        if s not in A: continue
        lab = {}
        for c in ("BAO+DES5", "BAO+DES5+CC"):
            a, b = A["full"][c], A[s][c]
            shift = b["flat_a0_om"] - a["flat_a0_om"]; comb = float(np.hypot(a["flat_a0_sd"], b["flat_a0_sd"]))
            nested = float(np.sqrt(abs(b["flat_a0_sd"]**2 - a["flat_a0_sd"]**2)))
            lab[c] = dict(om_shift=shift, combined_sd=comb, A2="ROBUST" if abs(shift) <= comb else "LEGACY-DEPENDENT",
                          nested_sd_context=nested, nested_ratio_context=(abs(shift)/nested if nested > 0 else None),
                          A3="FLOOR HOLDS" if b["tracking"]["2.33"][0] > 0 else "FLOOR LOST", A1=b["degeneracy"])
            print(f"   {s} vs full, {c}: Om shift {shift:+.4f} (combined sd {comb:.4f}) -> A2 {lab[c]['A2']};  A1 {lab[c]['A1']};  A3 {lab[c]['A3']}"
                  f"   [context: nested-sample sd {nested:.4f}]")
        A[s]["labels"] = lab
out["A_cfg684"] = A

# ---------------- part B: CFG689 D5 and TD5F ----------------
B = {}
for mode in ("D5", "TD5F"):
    ref9 = json.load(open(os.path.join(C689, f"cfg689_{mode}.json")))["BAO+SN"]
    Bm = {}
    r9 = {s: load(f"lgs1_cfg689_{mode}_{s}.json") for s in ("full", "des_only")}
    full = r9["full"]["BAO+SN"] if r9["full"] else None
    if full is None:
        Bm["harness"] = "NOT RUN"
    else:
        d = max(float(np.max(np.abs(np.array(full["P1"][z]["sqrtX_q"]) - np.array(ref9["P1"][z]["sqrtX_q"])))) for z in ZS689)
        Bm["harness_max_abs_diff"] = d; Bm["harness"] = "PASS" if d <= 0.005 else "FAIL"
        Bm["nstep_full"] = r9["full"]["nstep"]
    print(f"B. CFG689 {mode} harness check (full sample vs committed): {Bm['harness']}"
          + (f"  max |diff| in sqrtX quantiles {Bm['harness_max_abs_diff']:.2e}" if "harness_max_abs_diff" in Bm else ""))
    base = full if (full is not None and Bm["harness"] == "PASS") else None
    do = r9["des_only"]["BAO+SN"] if r9["des_only"] else None
    if do is None:
        print(f"   {mode} des_only: NOT RUN")
    else:
        Bm["nstep_des_only"] = r9["des_only"]["nstep"]; Bm["K4_ok"] = do["K4"]["ok"]
        Bm["P1_class"] = dict(committed=ref9["P1_class"], des_only=do["P1_class"])
        Bm["P0_class"] = dict(committed=(ref9["P0"] or {}).get("P0_class"), des_only=(do["P0"] or {}).get("P0_class"))
        Bm["P2"] = dict(committed=dict(dchi2=ref9["P2"]["dchi2"], sigma=ref9["P2"]["sigma_equiv"], cls=ref9["P2"].get("P2_class")),
                        des_only=dict(dchi2=do["P2"]["dchi2"], sigma=do["P2"]["sigma_equiv"], cls=do["P2"].get("P2_class")))
        Bm["z"] = {}
        for z in ZS689:
            qa, qb = np.array(ref9["P1"][z]["sqrtX_q"]), np.array(do["P1"][z]["sqrtX_q"])
            stable = (qa[1] <= qb[2] <= qa[3]) and (qb[1] <= qa[2] <= qb[3])
            Bm["z"][z] = dict(committed_68=[qa[1], qa[3]], committed_median=qa[2], des_only_68=[qb[1], qb[3]], des_only_median=qb[2],
                              B1="STABLE" if stable else "SHIFTED", e3_committed=ref9["P1"][z]["e_3sigma"], e3_des_only=do["P1"][z]["e_3sigma"])
            print(f"   {mode} z*={z}: tracking sqrtX 68% committed [{qa[1]:.3f}, {qa[3]:.3f}] med {qa[2]:.3f} | des_only [{qb[1]:.3f}, {qb[3]:.3f}] med {qb[2]:.3f}"
                  f" -> B1 {Bm['z'][z]['B1']};  e_3sigma {ref9['P1'][z]['e_3sigma']} -> {do['P1'][z]['e_3sigma']}")
        Bm["B2"] = "CLASS UNCHANGED" if (Bm["P1_class"]["committed"] == Bm["P1_class"]["des_only"]
                                          and Bm["P0_class"]["committed"] == Bm["P0_class"]["des_only"]) else "CLASS CHANGED"
        print(f"   {mode}: P1 {Bm['P1_class']}  P0 {Bm['P0_class']} -> B2 {Bm['B2']};  P2 {Bm['P2']};  K4 ok {Bm['K4_ok']}")
        if base is None:
            Bm["note"] = "des_only compared with the committed full-sample file; the same-harness full run was not available or failed"
    B[mode] = Bm
out["B_cfg689"] = B
json.dump(out, open(os.path.join(HERE, "lgs1_results.json"), "w"), indent=1, default=float)
print("wrote lgs1_results.json")
