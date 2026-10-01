#!/usr/bin/env python3
"""B4.3 -- confrontation: B4's triple points (b4_tp_su2_weight.json, b4_tp_su3_weight.json) through the papers' conversion (per_group of ../B2_lattice_mpp/b2_4_confrontation.py,
inherited unchanged) against lane Y1's Planck-scale couplings (y1_lib read-only).  U(1) untouched (the authors' model; lane B3).
Run:    python3 b4_confrontation.py            exit 0 iff the conversion-reproduction gates pass; verdicts are REPORTED
MUTATE: python3 b4_confrontation.py MUTATE     the SU(2) adjoint Casimir C_adj = N is replaced by 1: the reproduction gate must fail -> exit 1; exit 3 otherwise."""
import sys
sys.dont_write_bytecode = True
import os
import json
import math

HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("Y1_running_precision", "B_rg_asymptotic_safety", "N1_joint_couplings", "U3_invented_uv_boundary", "D_calibration_bar"):
    sys.path.insert(0, os.path.join(HERE, "..", sub))
import y1_lib as L
from b4_tp import per_group

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
MP = 1.22089e19
NGEN = 3
FAILED = []
Y1_REL = (0.0023, 0.00021, 0.0012)


def chk(tag, ok, detail=""):
    if not ok:
        FAILED.append(tag)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


tr = L.run_central(mu_max=1e21)
targets = tr.A(MP)
sig_t = tuple(t * r for t, r in zip(targets, Y1_REL))
print(f"B4.3 confrontation (MUTATE={MUT})")
print(f"  Y1 targets at M_P: 1/alpha = ({targets[0]:.3f}, {targets[1]:.3f}, {targets[2]:.3f}) for (Y, SU(2), SU(3)); 1-sigma ({sig_t[0]:.3f}, {sig_t[1]:.3f}, {sig_t[2]:.3f})")
print("\nReproduction of the papers' conversion at the papers' triple points (gate G-CONV):")
p2 = (per_group(2, 2.4, 0.54, False, MUT), per_group(2, 2.4, 0.54, True, MUT))
p3 = (per_group(3, 5.4, 0.8, False), per_group(3, 5.4, 0.8, True))
print(f"  SU(2) (0.54, 2.4): not exponentiated {p2[0]:.2f} (printed 15.7), exponentiated {p2[1]:.2f} (printed 16.5)")
print(f"  SU(3) (0.8, 5.4):  not exponentiated {p3[0]:.2f} (printed 17.7), exponentiated {p3[1]:.2f} (printed 18.9)  [the papers rounded 25.45 to 25; documented in B1]")
chk("G-CONV1 SU(2) conversion reproduces the printed 15.7 / 16.5 within 0.2", abs(p2[0] - 15.7) < 0.2 and abs(p2[1] - 16.5) < 0.2)
chk("G-CONV2 SU(3) conversion reproduces the printed 17.7 / 18.9 within the documented rounding 0.6", abs(p3[0] - 17.7) < 0.6 and abs(p3[1] - 18.9) < 0.6)
if MUT:
    fired = any(t.startswith("G-CONV1") for t in FAILED)
    print("\nMUTATE CONTROL: C_adj = 1 for SU(2) -> G-CONV1", "FAILS as required (exit 1, the control fires)" if fired else "did NOT fail: CONTROL BROKEN (exit 3)")
    sys.exit(1 if fired else 3)

rows = {}
print("\nNon-Abelian rows (conversion fixed in the pre-registration; lattice errors from b4_tp_*.json):")
papers_sig = {"SU2": 0.14, "SU3": 0.15}
b2_prev = {"SU2": (49.89, 0.055), "SU3": (66.69, 0.167)}
for key, N, ti in (("SU2", 2, 1), ("SU3", 3, 2)):
    fn = os.path.join(HERE, f"b4_tp_{key.lower().replace('su', 'su')}_weight.json")
    fn = os.path.join(HERE, f"b4_tp_su{N}_weight.json")
    if not os.path.exists(fn):
        print(f"  {key}: {os.path.basename(fn)} missing -> UNDECIDED"); rows[key] = dict(status="UNDECIDED", why="no analysis file"); continue
    tp = json.load(open(fn))
    if tp.get("status") != "IDENTIFIED":
        print(f"  {key}: triple point NOT identified ({tp.get('why', tp.get('status'))}) -> UNDECIDED"); rows[key] = dict(status="UNDECIDED", why=str(tp.get("why", tp.get("status")))); continue
    pred, pred_n, s_lat, s_inh, frac = tp["inv_expo"], tp["inv_not"], tp["s_lat"], tp["s_inh"], tp["frac_lat"]
    tgt, st = targets[ti], sig_t[ti]
    z = (pred - tgt) / math.sqrt(s_lat ** 2 + s_inh ** 2 + st ** 2)
    zl = (pred - tgt) / math.sqrt(s_lat ** 2 + st ** 2)
    zn = (pred_n - tgt) / math.sqrt(s_lat ** 2 + st ** 2)
    s_tot = math.hypot(s_lat, s_inh)
    gw = tp.get('gw_ok')
    sharper = (frac <= 0.03) and (gw is True)
    verdict = "PASS" if abs(z) <= 2 else "FAIL"
    if verdict == "PASS" and (s_tot / pred > 0.05 or not sharper):
        verdict = "PASS-WEAK"
    prov = "" if gw is True else " [provisional: gate G-W " + ("failed (marginal)" if gw is False else "not verifiable (no production cross-check)") + "; the pre-registered precision claim is not certified]"
    print(f"  {key}: triple point (beta_F, beta_A) = ({tp['bF']:.3f} +- {tp['sF']:.3f}, {tp['bA']:.4f} +- {tp['sA']:.4f})  -> 1/alpha(M_P) = {pred:.2f} +- {s_lat:.2f} (lattice: stat+FSS {tp['s_stat']:.2f}, fit-range {tp['s_fit']:.2f}; {100 * frac:.1f}%) +- {s_inh:.2f} (inherited exp-vs-not); not exponentiated {pred_n:.2f}")
    print(f"        Y1 target {tgt:.3f}: z = {z:+.2f} (with inherited), lattice-only z = {zl:+.2f} (exponentiated) / {zn:+.2f} (not exponentiated)  -> {verdict}{prov}; 3% criterion {'MET' if sharper else 'NOT certified'}; central minus target = {pred - tgt:+.2f} ({100 * (pred - tgt) / tgt:+.1f}%)")
    prev = b2_prev[key]
    print(f"        precision: B4 {100 * frac:.1f}% vs papers {100 * papers_sig[key]:.0f}% vs B2 {100 * prev[1]:.1f}% (B2 central {prev[0]:.2f})")
    for vr in ("win", "mix", "prod"):
        fv = os.path.join(HERE, f"b4_tp_su{N}_weight_{vr}.json")
        if os.path.exists(fv):
            tv = json.load(open(fv))
            if tv.get("status") == "IDENTIFIED":
                print(f"        variant {vr:4s}: triple point ({tv['bF']:.3f} +- {tv['sF']:.3f}, {tv['bA']:.4f} +- {tv['sA']:.4f}); 1/alpha exp {tv['inv_expo']:.2f}, not-exp {tv['inv_not']:.2f}, lattice +- {tv['s_lat']:.2f} ({100 * tv['frac_lat']:.1f}%)")
    if key == "SU3" and tp.get("line1") is not None:
        # robustness: any triple point lies on the I-II line (the nearly flat segment S1, well determined: hot- and cold-start replicas agree there); for beta_F in [0.6, 1.0] it gives
        l1 = tp["line1"]
        vals = [(bf, l1[0] + l1[1] * bf) for bf in (0.6, 0.7, 0.8, 0.9, 1.0)]
        lo_e = min(3 * per_group(3, ba, bf, True) for bf, ba in vals); lo_n = min(3 * per_group(3, ba, bf, False) for bf, ba in vals)
        print(f"        robustness: along the S1 line (beta_A = {l1[0]:.3f} + {l1[1]:.3f} beta_F) for ANY junction at beta_F in [0.6, 1.0] the conversion gives at least 1/alpha_3 = {lo_e:.1f} (exponentiated) / {lo_n:.1f} (not exponentiated), versus the Y1 target {tgt:.2f}")
    rows[key] = dict(status=verdict, pred=pred, pred_not=pred_n, s_lat=s_lat, s_inh=s_inh, z=z, zl=zl, zn=zn, frac=frac, sharper=bool(sharper), off_pct=100 * (pred - tgt) / tgt, bF=tp["bF"], bA=tp["bA"], sF=tp["sF"], sA=tp["sA"])
rows["Y"] = dict(status="UNDECIDED", why="U(1): the authors' model, untouched (lane B3 audits it)")
json.dump(rows, open(os.path.join(HERE, "b4_rows.json"), "w"), indent=1, default=str)
print("\nSUMMARY:")
for k, v in rows.items():
    print(f"  {k}: {v['status']}" + (f" (1/alpha {v['pred']:.2f} +- {v['s_lat']:.2f}[lat] +- {v['s_inh']:.2f}[inh]; z {v['z']:+.2f}; 3% criterion {'MET' if v['sharper'] else 'NOT certified'})" if 'pred' in v else f" ({v.get('why', '')})"))
sys.exit(0 if not FAILED else 1)
