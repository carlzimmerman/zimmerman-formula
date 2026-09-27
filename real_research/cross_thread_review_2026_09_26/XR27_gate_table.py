#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR27_gate_table.py -- bookkeeping over XR27's two lanes: per band-pass length L, which EFE systems pass in the chain's law, which of
M*'s failures flip, and whether ONE L passes the EFE-disfavouring samples (cluster infall, LV dwarfs, Coma UDGs) and the
EFE-favouring ones (Crater II, DF2/DF4, the M31 dwarfs, Chae's SPARC signal) together -- or where the pincer sits.
Reads XR27_efe_disfavouring_results.json and XR27_efe_favouring_results.json (the _MUTATE versions under MUTATE=1); computes nothing
physical.  Pass rules are each lane's (XR9's 2-sigma gates for the record's samples; <= 2 sigma for the others).

CHECKS
  T1 the table's per-system pass flags equal each lane's own flags (bookkeeping).
  T2 [load-bearing; MUTATE must fail] THE BAND-PASS ACTS ON THE L-DEPENDENT SYSTEMS: across the scan the cluster slope's flux-form
     worst sigma and Chae's D2 (catalogued geometry) each move by > 1 sigma.  Under MUTATE (the lanes' band-pass wrongly passes the
     external field) both are flat.
  P  (reported) the pass sets per system and class, their intersection, the flips against M*, and the pincer.
Run from the repository root after the two lanes:  python3 real_research/cross_thread_review_2026_09_26/XR27_gate_table.py  (MUTATE=1)
"""
import os, sys, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR27_gate_table"


class _Tee:
    def __init__(self, fh): self.fh = fh; self.so = sys.__stdout__
    def write(self, s): self.so.write(s); self.fh.write(s)
    def flush(self): self.so.flush(); self.fh.flush()


sys.stdout = _Tee(open(os.path.join(HERE, SLUG + ("_MUTATE.out" if MUTATE else ".out")), "w"))
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR27 gate table", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing, "name": name}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")


P(__doc__.split("CHECKS")[0].strip())
sfx = "_results_MUTATE.json" if MUTATE else "_results.json"
A = json.load(open(os.path.join(HERE, "XR27_efe_disfavouring" + sfx)))["numbers"]
B = json.load(open(os.path.join(HERE, "XR27_efe_favouring" + sfx)))["numbers"]
LS = [f"{L:g}" for L in json.load(open(os.path.join(HERE, "XR27_efe_disfavouring" + sfx)))["L_scan"]]
CELLS = ["inf"] + LS + ["H_Y", "H_S"]
CL, DW, UD = A["clusters"], A["dwarfs"], A["udg"]
CR, DF, M3, CHAE = B["crater2"], B["df2_df4"], B["m31"], B["chae"]

row = {}
for c in CELLS:
    s = CL[c]["summary"]
    row[c] = {
        "clusters (record gate)": (s["pass_"], f"{s['sigma_range'][0]:.2f}-{s['sigma_range'][1]:.2f}"),
        "clusters scalar form": (s["pass_scalar"], f"{s['by_form']['sigma_scalar'][1]:.2f}"),
        "clusters flux form": (s.get("pass_flux", False), f"{s['flux_range'][1]:.2f}" if "flux_range" in s else "-"),
        "clusters zero point": (s["zp_pass"], f"{s['zp_range'][1]:.2f}"),
        "LV dwarfs": (DW[c]["pass_"], f"{DW[c]['sigma_range'][0]:.2f}-{DW[c]['sigma_range'][1]:.2f}"),
        "Coma UDGs": (UD[c]["pass_"], f"{UD[c]['worst_central']:.2f}"),
        "Crater II": (CR[c]["pass_"], f"{CR[c]['sigma_range'][0]:.2f}-{CR[c]['sigma_range'][1]:.2f}"),
        "DF2": (DF[c]["NGC1052-DF2"]["pass_"], f"{DF[c]['NGC1052-DF2']['sigma_range'][0]:.1f}-{DF[c]['NGC1052-DF2']['sigma_range'][1]:.1f}"),
        "DF4": (DF[c]["NGC1052-DF4"]["pass_"], f"{DF[c]['NGC1052-DF4']['sigma_range'][0]:.1f}-{DF[c]['NGC1052-DF4']['sigma_range'][1]:.1f}"),
        "M31 dwarfs": (M3[c]["pass_"], f"{M3[c]['z_range'][0]:.1f}-{M3[c]['z_range'][1]:.1f}"),
        "Chae D2 (catalogued)": (CHAE[c]["pass_"], f"{CHAE[c]['3d']['D2']['z']:.1f}"),
        "Chae D2 (any geometry)": (CHAE[c]["pass_any_geometry"], f"{min(CHAE[c][g]['D2']['z'] for g in ('3d', 'collapsed', '3d_full', 'collapsed_full')):.1f}"),
        "Chae D1 (any geometry)": (CHAE[c]["D1_pass_any_geometry"], f"{min(CHAE[c][g]['D1']['z'] for g in ('3d', 'collapsed', '3d_full', 'collapsed_full')):.1f}"),
    }
SYS = list(row["inf"].keys())
DIS = ["clusters (record gate)", "LV dwarfs", "Coma UDGs"]
FAV = ["Crater II", "DF2", "DF4", "M31 dwarfs", "Chae D2 (catalogued)"]
FAV_LENIENT = ["Crater II", "DF2", "DF4", "M31 dwarfs", "Chae D2 (any geometry)"]
DIS_LENIENT = ["clusters flux form", "LV dwarfs", "Coma UDGs"]

P("\n  sigma by cell (worst over the lane's variants unless a range is shown); '*' marks a pass")
P("  " + f"{'cell':>5s} " + " ".join(f"{k[:18]:>18s}" for k in SYS))
for c in CELLS:
    P("  " + f"{c:>5s} " + " ".join(f"{(v[1] + ('*' if v[0] else ' ')):>18s}" for v in row[c].values()))

# M*'s own verdicts (the record's XR9 converged cell for the disfavouring samples; the L -> oo Route-A rows for the favouring ones)
MST = {"clusters (record gate)": (A["C1"]["Mstar_kappa_range"][1] <= 2.0, f"{A['C1']['Mstar_kappa_range'][0]:.2f}-{A['C1']['Mstar_kappa_range'][1]:.2f}"),
       "LV dwarfs": (False, "3.87-4.48"), "Coma UDGs": (False, "4.20-4.35"),
       "Crater II": (CR["Mstar"]["pass_"], f"{CR['Mstar']['sigma_range'][0]:.2f}-{CR['Mstar']['sigma_range'][1]:.2f}"),
       "DF2": (DF["Mstar"]["NGC1052-DF2"]["pass_"], f"{DF['Mstar']['NGC1052-DF2']['sigma_range'][0]:.1f}-{DF['Mstar']['NGC1052-DF2']['sigma_range'][1]:.1f}"),
       "DF4": (DF["Mstar"]["NGC1052-DF4"]["pass_"], f"{DF['Mstar']['NGC1052-DF4']['sigma_range'][0]:.1f}-{DF['Mstar']['NGC1052-DF4']['sigma_range'][1]:.1f}"),
       "M31 dwarfs": (M3["Mstar"]["pass_"], f"{M3['Mstar']['z_range'][0]:.1f}-{M3['Mstar']['z_range'][1]:.1f}"),
       "Chae D2 (catalogued)": (CHAE["Mstar"]["canonical"]["D2"]["z"] <= 2.0 and CHAE["Mstar"]["alt"]["D2"]["z"] <= 2.0,
                                f"{CHAE['Mstar']['canonical']['D2']['z']:.1f}/{CHAE['Mstar']['alt']['D2']['z']:.1f}")}
P("\n  M* (the construction model), same statistics:  " + "; ".join(f"{k}: {v[1]}{'*' if v[0] else ''}" for k, v in MST.items()))

passL = {k: [c for c in LS if row[c][k][0]] for k in SYS}
flips = {k: dict(Mstar=MST[k][0], chain_passing_L=passL[k], at_HY=row["H_Y"][k][0], at_HS=row["H_S"][k][0]) for k in MST}
both = [c for c in LS if all(row[c][k][0] for k in DIS + FAV)]
both_len = [c for c in LS if all(row[c][k][0] for k in DIS_LENIENT + FAV_LENIENT)]
lwin = lambda ks: [c for c in LS if all(row[c][k][0] for k in ks)]
P("\n  pass sets over the scan (L in Mpc):")
for k in SYS:
    P(f"    {k:26s} {passL[k] if passL[k] else 'none'}   (H_Y {'pass' if row['H_Y'][k][0] else 'fail'}, H_S {'pass' if row['H_S'][k][0] else 'fail'})")
P(f"  EFE-disfavouring class (record gates) passes at: {lwin(DIS) or 'none'};  EFE-favouring class (catalogued Chae) at: {lwin(FAV) or 'none'}")
P(f"  both classes, record gates: {both or 'none'};  both, most lenient readings (cluster flux form, Chae in any geometry): {both_len or 'none'}")
# the L-dependent pair: the cluster slope's lenient forms want short L, Chae wants long L
cl_fl, cl_sc, ch_3d, ch_any = passL["clusters flux form"], passL["clusters scalar form"], passL["Chae D2 (catalogued)"], passL["Chae D2 (any geometry)"]
fnum = lambda v: [float(x) for x in v]
pin = dict(cluster_flux_max_L=max(fnum(cl_fl)) if cl_fl else None, cluster_scalar_max_L=max(fnum(cl_sc)) if cl_sc else None,
           chae_catalogued_min_L=min(fnum(ch_3d)) if ch_3d else None, chae_any_min_L=min(fnum(ch_any)) if ch_any else None)
P(f"  THE L-DEPENDENT PAIR: cluster slope passes (flux form) only for L <= {pin['cluster_flux_max_L']} Mpc (scalar form <= {pin['cluster_scalar_max_L']}); "
  f"Chae's D2 passes only for L >= {pin['chae_catalogued_min_L']} Mpc (catalogued geometry; any geometry >= {pin['chae_any_min_L']})")
OUT["numbers"] = dict(table={c: {k: list(v) for k, v in row[c].items()} for c in CELLS}, Mstar={k: list(v) for k, v in MST.items()},
                      pass_L=passL, flips=flips, both_classes=both, both_lenient=both_len, class_disfavouring=lwin(DIS),
                      class_favouring=lwin(FAV), pincer=pin)

# T1 bookkeeping
t1 = all(row[c]["clusters (record gate)"][0] == CL[c]["summary"]["pass_"] and row[c]["LV dwarfs"][0] == DW[c]["pass_"]
         and row[c]["Coma UDGs"][0] == UD[c]["pass_"] and row[c]["Crater II"][0] == CR[c]["pass_"] and row[c]["M31 dwarfs"][0] == M3[c]["pass_"]
         and row[c]["Chae D2 (catalogued)"][0] == CHAE[c]["pass_"] for c in CELLS)
check("T1 the table's pass flags equal each lane's own flags", "consistent" if t1 else "INCONSISTENT", t1)
fl = [CL[c]["summary"]["flux_range"][1] for c in LS]; d2 = [CHAE[c]["3d"]["D2"]["z"] for c in LS]
check("T2 THE BAND-PASS ACTS ON THE L-DEPENDENT SYSTEMS (MUTATE must fail): across the scan the cluster slope's flux-form worst sigma and "
      "Chae's D2 (catalogued) each move by > 1 sigma", f"cluster flux worst {min(fl):.2f}-{max(fl):.2f}; Chae D2 {min(d2):.2f}-{max(d2):.2f}",
      (max(fl) - min(fl)) > 1.0 and (max(d2) - min(d2)) > 1.0)
check("P (reported) ONE L PASSES BOTH CLASSES (record gates)", f"{both or 'none'}", bool(both), load_bearing=False)
nlb = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), nlb
json.dump(OUT, open(os.path.join(HERE, SLUG + sfx), "w"), indent=1)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {SLUG + sfx}")
sys.exit(1 if nlb else 0)
