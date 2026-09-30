#!/usr/bin/env python3
"""B2.4 -- confrontation: the papers' own conversion (fixed in B2_PREREGISTRATION.md) applied to B2's OWN lattice values, errors propagated, compared with lane Y1's
Planck-scale couplings; U(1) sensitivity to the inherited model factors.
Inputs (written by the other B2 scripts): b2_1_result.json (U(1) beta_c), b2_2_tp.json and b2_3_tp.json (triple-point analysis of the SU(2), SU(3) scans).
Run:    python3 b2_4_confrontation.py           exit 0 iff the internal conversion-reproduction gates pass; verdicts are REPORTED
MUTATE: python3 b2_4_confrontation.py MUTATE    the SU(2) adjoint Casimir C_adj = N is replaced by 1 in the conversion: the reproduction gate must fail -> exit 1; exit 3 otherwise.
"""
import sys
sys.dont_write_bytecode = True
import os
import json
import math

HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("Y1_running_precision", "B_rg_asymptotic_safety", "N1_joint_couplings", "U3_invented_uv_boundary", "D_calibration_bar"):
    sys.path.insert(0, os.path.join(HERE, "..", sub))
import y1_lib as L

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
PI = math.pi
MP = 1.22089e19
NGEN = 3
FAILED = []
Y1_REL = (0.0023, 0.00021, 0.0012)


def chk(tag, ok, detail=""):
    if not ok:
        FAILED.append(tag)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


def per_group(N, b_adj, b_f, expo, mut=False):
    C_adj, C_f = (1.0 if (mut and N == 2) else N), (N * N - 1) / (2.0 * N)
    full = 4 * PI * (C_adj * b_adj + C_f * b_f) / (N * N - 1)
    a_full = 1.0 / full
    if expo:
        fa, ff = math.exp(-PI * C_adj * a_full), math.exp(-PI * C_f * a_full)
    else:
        fa, ff = 1 - PI * C_adj * a_full, 1 - PI * C_f * a_full
    return 4 * PI * (C_adj * b_adj * fa + C_f * b_f * ff) / (N * N - 1)


tr = L.run_central(mu_max=1e21)
targets = tr.A(MP)
sig_t = tuple(t * r for t, r in zip(targets, Y1_REL))
print(f"B2.4 confrontation (MUTATE={MUT})")
print(f"  Y1 targets at M_P: 1/alpha = ({targets[0]:.3f}, {targets[1]:.3f}, {targets[2]:.3f}) for (Y, SU(2), SU(3)); 1-sigma ({sig_t[0]:.3f}, {sig_t[1]:.3f}, {sig_t[2]:.3f})")

print("\nReproduction of the papers' conversion at the papers' triple points (B1 values; gate):")
p2 = (per_group(2, 2.4, 0.54, False, MUT), per_group(2, 2.4, 0.54, True, MUT))
p3 = (per_group(3, 5.4, 0.8, False), per_group(3, 5.4, 0.8, True))
print(f"  SU(2) (0.54, 2.4): not exponentiated {p2[0]:.2f} (printed 15.7), exponentiated {p2[1]:.2f} (printed 16.5)")
print(f"  SU(3) (0.8, 5.4):  not exponentiated {p3[0]:.2f} (printed 17.7), exponentiated {p3[1]:.2f} (printed 18.9)  [the papers rounded 25.45 to 25; documented in B1: unrounded values are 0.3-0.5 higher]")
chk("G1 SU(2) conversion reproduces the printed 15.7 / 16.5 within 0.2", abs(p2[0] - 15.7) < 0.2 and abs(p2[1] - 16.5) < 0.2)
chk("G1b SU(3) conversion reproduces the printed 17.7 / 18.9 within the documented rounding 0.6", abs(p3[0] - 17.7) < 0.6 and abs(p3[1] - 18.9) < 0.6)
if MUT:
    fired = any(t.startswith("G1 ") for t in FAILED)
    print("\nMUTATE CONTROL: C_adj = 1 for SU(2) -> G1", "FAILS as required (exit 1, the control fires)" if fired else "did NOT fail: CONTROL BROKEN (exit 3)")
    sys.exit(1 if fired else 3)

# ------------------------------------------------------------------------------------------------ non-Abelian rows
def verdict(pred, s_lat, s_inh, tgt, s_t):
    z = (pred - tgt) / math.sqrt(s_lat ** 2 + s_inh ** 2 + s_t ** 2)
    zl = (pred - tgt) / math.sqrt(s_lat ** 2 + s_t ** 2)
    return z, zl


print("\nNon-Abelian rows (conversion fixed in the pre-registration; lattice errors from b2_2_tp.json / b2_3_tp.json):")
rows = {}
for key, N, fn, ti in (("SU2", 2, "b2_2_tp.json", 1), ("SU3", 3, "b2_3_tp.json", 2)):
    path = os.path.join(HERE, fn)
    if not os.path.exists(path):
        print(f"  {key}: {fn} missing -> UNDECIDED")
        rows[key] = dict(status="UNDECIDED", why="no triple-point analysis file")
        continue
    tp = json.load(open(path))
    if tp.get("status") != "IDENTIFIED":
        print(f"  {key}: triple point NOT identified by B2 ({tp.get('why', '')}) -> UNDECIDED")
        rows[key] = dict(status="UNDECIDED", why=tp.get("why", ""), tp=tp)
        continue
    bF, bA, sF, sA = tp["bF"], tp["bA"], tp["sF"], tp["sA"]
    c_e = NGEN * per_group(N, bA, bF, True)
    c_n = NGEN * per_group(N, bA, bF, False)
    dA = NGEN * (per_group(N, bA + 1e-4, bF, True) - per_group(N, bA - 1e-4, bF, True)) / 2e-4
    dF = NGEN * (per_group(N, bA, bF + 1e-4, True) - per_group(N, bA, bF - 1e-4, True)) / 2e-4
    s_lat = math.hypot(dA * sA, dF * sF)
    s_inh = abs(c_e - c_n)
    z, zl = verdict(c_e, s_lat, s_inh, targets[ti], sig_t[ti])
    frac = s_lat / c_e
    sharper = frac <= 0.03
    s_tot = math.hypot(s_lat, s_inh)
    st = ("PASS" if abs(z) <= 2 else "FAIL")
    if st == "PASS" and (s_tot / c_e > 0.05 or not sharper):
        st = "PASS-WEAK"      # B1 criterion 3: informative only if the total sigma is <= 5% (and, for B2, the lattice-only sigma <= 3%)
    papers_sig = {"SU2": 0.14, "SU3": 0.15}[key]
    worse = frac > papers_sig
    print(f"  {key}: triple point (beta_F, beta_A) = ({bF:.3f}+-{sF:.3f}, {bA:.3f}+-{sA:.3f})  -> 1/alpha(M_P) = {c_e:.2f} +- {s_lat:.2f} (lattice, {100 * frac:.1f}%) +- {s_inh:.2f} (inherited exp-vs-not)  [not-exponentiated {c_n:.2f}]")
    print(f"        Y1 target {targets[ti]:.3f}: z = {z:+.2f} (with inherited), {zl:+.2f} (lattice only)  -> {st}; 3% criterion {'MET' if sharper else 'NOT met'}; central value minus target = {c_e - targets[ti]:+.2f} ({100 * (c_e - targets[ti]) / targets[ti]:+.1f}%)")
    print(f"        lattice-only precision {100 * frac:.1f}% versus the papers' stated {100 * papers_sig:.0f}%: {'WORSE than the papers (the agreement is vacuous)' if worse else 'better than the papers'}")
    rows[key] = dict(status=st, pred=c_e, s_lat=s_lat, s_inh=s_inh, z=z, zl=zl, sharper=sharper, frac=frac, worse_than_papers=bool(worse), off_pct=100 * (c_e - targets[ti]) / targets[ti])

# ------------------------------------------------------------------------------------------------ U(1)
print("\nU(1) row: what B2 could and could not test.")
u1p = os.path.join(HERE, "b2_1_result.json")
if os.path.exists(u1p):
    u1 = json.load(open(u1p))
    bc, sbc = u1["beta_c"], u1["sigma"]
    print(f"  B2 measured Wilson beta_c(inf) = {bc:.5f} +- {sbc:.5f}  (papers use 1.0106)")
else:
    bc, sbc = 1.0106, float("nan")
    print("  b2_1_result.json missing; using the papers' 1.0106")


def alpha_cont(dg, bcr):
    x = dg / (bcr + dg)
    return 0.20 - 0.24 * x ** 0.39


print("  Conversion (hep-ph/9607278 eq (139)): alpha_cont = 0.20 - 0.24 (Dgamma/(beta_c+Dgamma))^0.39; 1/alpha_Y(M_P) = enhancement x 1/alpha_cont")
print("  (i) sensitivity to beta_c: Dgamma = 0.05615, enhancement 6.662 (the papers' starred row):")
for b in (1.0100, 1.0106, 1.0111, bc):
    ac = alpha_cont(0.05615, b)
    print(f"      beta_c = {b:.5f}: 1/alpha_cont = {1 / ac:.4f}, 1/alpha_Y = {6.662 / ac:.2f}")
if not math.isnan(sbc):
    d = 6.662 * (1 / alpha_cont(0.05615, bc + sbc) - 1 / alpha_cont(0.05615, bc - sbc)) / 2
    print(f"      => the lattice input beta_c contributes +-{abs(d):.4f} to 1/alpha_Y (negligible); the value is set by the INHERITED factors below")
print("  (ii) sensitivity to the inherited factors (Dgamma_eff model, enhancement 6 ... 8.04); Y1 target 1/alpha_Y = %.3f:" % targets[0])
print("      Dgamma   1/alpha_cont | 1/alpha_Y for enhancement = 6.0   6.662   8.04")
for dg in (0.0, 0.02, 0.04, 0.05615, 0.081, 0.11):
    ic = 1 / alpha_cont(dg, 1.0106)
    print(f"      {dg:6.4f}   {ic:7.3f}      | {6.0 * ic:7.2f}   {6.662 * ic:7.2f}   {8.04 * ic:7.2f}")
# the Dgamma that would give exactly the Y1 target for enhancement 6.662
lo, hi = 1e-5, 0.5
for _ in range(80):
    mid = 0.5 * (lo + hi)
    if 6.662 / alpha_cont(mid, 1.0106) < targets[0]:
        lo = mid
    else:
        hi = mid
print(f"  With the papers' enhancement 6.662, agreement with the Y1 target 1/alpha_Y = {targets[0]:.2f} requires Dgamma_eff = {lo:.4f}; the papers' modelled values are 0.056 to 0.081 (starred rows), 0.060 to 0.109 (all Wilson rows). A shift of Dgamma_eff by 0.01 moves 1/alpha_Y by {6.662 * (1 / alpha_cont(lo + 0.01, 1.0106) - 1 / alpha_cont(lo, 1.0106)):.1f}; the enhancement 6 -> 8.04 moves it by a factor 1.34.")
print("  => the U(1) pass in B1 rests on Dgamma_eff and the enhancement interpolation (the authors' Z2/Z3 discrete-subgroup and monopole models); B2 cannot test those: UNDECIDED (precision criterion NOT met: the lattice input is not the dominant uncertainty).")
rows["Y"] = dict(status="UNDECIDED", why="inherited Dgamma_eff and enhancement model not testable here")

json.dump(rows, open(os.path.join(HERE, "b2_4_rows.json"), "w"), indent=1, default=str)
print("\nSUMMARY:")
for k, v in rows.items():
    print(f"  {k}: {v['status']}" + (f" (1/alpha {v['pred']:.2f} +- {v['s_lat']:.2f}[lat] +- {v['s_inh']:.2f}[inh]; z {v['z']:+.2f}; 3% criterion {'MET' if v['sharper'] else 'NOT met'})" if 'pred' in v else f" ({v.get('why', '')})"))
sys.exit(0 if not FAILED else 1)
