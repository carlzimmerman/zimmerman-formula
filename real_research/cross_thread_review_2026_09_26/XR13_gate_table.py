#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR13_gate_table.py -- THE PER-OBJECT DOOR: the scorecard.  Bookkeeping over the three XR13 results files (no new physics):
every gate the task names, M*'s committed number beside the door's, and a verdict -- FLIPS (M* failed, the door passes),
IMPROVES (closer, still failing), PARTWAY, BREAKS (M* passed, the door fails), NEW FAILURE (a test M* did not carry),
UNCHANGED, or RISK (unchanged in the committed model, not established for real systems).

CHECKS
  T1 [load-bearing; MUTATE must fail] the three lanes scored the door (their scored column is the door, and each ran with no
     load-bearing failure).  MUTATE=1 reads the three _MUTATE results files, whose scored columns are M*: T1 must FAIL (rc = 1).
  T2 (reported) the net: gates flipped against gates broken or newly failed.

Run from the repository root, after the three lanes:  python3 real_research/cross_thread_review_2026_09_26/XR13_gate_table.py
"""
import os, sys, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR13_gate_table"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR13 gate table", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")


suf = "_results_MUTATE.json" if MUTATE else "_results.json"
E, L, C = (json.load(open(os.path.join(HERE, f"XR13_door_{k_}{suf}"))) for k_ in ("environment", "local_group", "cosmology"))
P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the three lanes' MUTATE results (scored column = M*, regions merged); T1 must FAIL ***")
scored = all(x_["door_in_scored_column"] for x_ in (E, L, C))
clean = all(x_["n_fail_load_bearing"] == 0 for x_ in (E, L, C))
check("T1 THE THREE LANES SCORED THE DOOR with no load-bearing failure -- MUTATE (their M* columns) must fail",
      f"door in the scored column: {[x_['door_in_scored_column'] for x_ in (E, L, C)]}; load-bearing failures "
      f"{[x_['n_fail_load_bearing'] for x_ in (E, L, C)]}", scored and clean)

en, ln, cn = E["numbers"], L["numbers"], C["numbers"]
rows = []
# (a) cluster-infall BTFR
cm = en["clusters"]["Mstar_kappa_summary"]; cs = en["clusters"]["scored"]
rows.append(("(a) EFE, cluster-infall BTFR slope (N = 314)", f"{cm['sigma_range'][0]:.1f}-{cm['sigma_range'][1]:.1f} sigma",
             f"{cs['sigma_range'][0]:.2f}-{cs['sigma_range'][1]:.2f} sigma; zero point {cs['zp_sigma_range'][1]:.2f} sigma",
             "FLIPS" if cs["sigma_range"][1] < 2 and cm["sigma_range"][1] >= 2 else "no flip"))
# (b) dwarfs
dm = en["dwarfs"]["Mstar_kappa_rows"]; ds = en["dwarfs"]["scored"]; sens = en["dwarfs"]["sensitivity"]
passing = [k_ for k_, v_ in sens.items() if v_["sigma_range"][1] < 2 and k_.startswith("R1/l") and "a_host" not in k_]
rows.append(("(b) EFE, LV dwarfs statistic C (N = 92)", f"{min(v_['sigma'] for v_ in dm.values()):.1f}-{max(v_['sigma'] for v_ in dm.values()):.1f} sigma",
             f"{ds['sigma_range'][0]:.2f}-{ds['sigma_range'][1]:.2f} sigma at l_obj = 1 kpc (passes for l_obj <= "
             f"{max(float(k_.split('/l')[1]) for k_ in passing) if passing else 'none'} kpc; the size rule fails)",
             ("FLIPS (rule-dependent)" if ds["sigma_range"][1] < 2 else "no flip")))
# (c) UDGs
um = en["udg"]["Mstar_kappa_rows"]; us = en["udg"]["scored"]
rows.append(("(c) Coma UDGs (11)", f"{min(v_['sigma'] for v_ in um.values()):.1f}-{max(v_['sigma'] for v_ in um.values()):.1f} sigma",
             f"{us['sigma'][0]:.2f} / {us['sigma'][1]:.2f} sigma at {us['me'][0]:+.2f} / {us['me'][1]:+.2f} dex",
             "FLIPS" if max(us["sigma"]) < 2 else ("IMPROVES, no flip" if max(us["sigma"]) < min(v_["sigma"] for v_ in um.values()) else "no change")))
# (d) LG R_0
sr = ln["scored_R0"]; mr = ln["R0_merged"]
dd = [math.log10(v_ / 0.96) for k_, v_ in sr.items() if k_.endswith("/decay")]
dmg = [math.log10(v_ / 0.96) for k_, v_ in mr.items() if k_.endswith("/decay")]
rows.append(("(d) Local Group R_0 (decay history)", f"{min(dmg):+.2f} to {max(dmg):+.2f} dex",
             f"{min(dd):+.2f} to {max(dd):+.2f} dex" + (" (reading T; reading P about the same)" if L["door_in_scored_column"] else ""),
             "FLIPS" if L["checks"]["G4"]["pass"] else ("PARTWAY, still fails" if max(dd) < max(dmg) - 1e-9 else "no change")))
# the timing
tm = ln["timing"]
vT = [v_["u_today"] for k_, v_ in tm.items() if k_.startswith("door/")]
vP = [v_["u_today"] for k_, v_ in tm.items() if k_.startswith("door reading P/") and v_["u_today"] is not None]
vM = [v_["u_today"] for k_, v_ in tm.items() if k_.startswith("Mstar/") and v_["u_today"] is not None]
vS = (vT + vP) if L["door_in_scored_column"] else vM
rows.append(("MW-M31 timing at 0.78 Mpc (measured -110 km/s)", f"{min(vM):+.0f} to {max(vM):+.0f} km/s (over-predicts; past-flyby escape)",
             f"{min(vS):+.0f} to {max(vS):+.0f} km/s" + (" (readings T and P)" if L["door_in_scored_column"] else ""),
             ("NEW FAILURE" if min(vS) > -110 + 3 * 4.4 else "passes") if L["door_in_scored_column"] else "over-predicts (item 13)"))
# (e) KiDS
kd = cn["kids"]
rows.append(("(e) KiDS-1000 (isolated lenses)", f"{kd['XR9_dchi2']['canonical']:+.1f} / {kd['XR9_dchi2']['alt']:+.1f}",
             f"unchanged in the committed model; a MW-like satellite system's basins cover "
             f"{max(v_['refined'] for v_ in kd['sky_fraction_lost'].values()):.2f} of the host's sky", "UNCHANGED (committed) / RISK"))
# (f) shear
sh = cn["shear"]["table"]
mk = "door" if C["door_in_scored_column"] else "Mstar"
rows.append(("(f) cosmic shear, halo model (two-sided 0.8-1.2)",
             f"{min(sh[f'{f}/Mstar']['min'] for f in ('canonical', 'alt')):.2f}-{max(sh[f'{f}/Mstar']['max'] for f in ('canonical', 'alt')):.2f}",
             f"{min(sh[f'{f}/{mk}']['min'] for f in ('canonical', 'alt')):.2f}-{max(sh[f'{f}/{mk}']['max'] for f in ('canonical', 'alt')):.2f} "
             f"(one-sided R <= 1.2 {'passes' if cn['shear']['one_sided'][mk] else 'fails'})",
             "BREAKS (lower side)" if not cn["shear"]["two_sided"][mk] else "passes"))
# (g) X-COP
xc = cn["xcop"]
sb, sw = (xc["bounds_door"], xc["window_door"]["door_pooled"]) if C["door_in_scored_column"] else (xc["bounds_Mstar"], xc["window_Mstar"])
rows.append(("(g) X-COP (L388 retention, 575-650 km/s)", f"carrier {xc['bounds_Mstar'][0]:.2f}-{xc['bounds_Mstar'][1]:.2f}; window {xc['window_Mstar']}",
             f"carrier {sb[0]:.2f}-{sb[1]:.2f}; window {sw or 'none'} "
             f"(top bin holds {min(v_['eps_top_bin'] for v_ in xc['by_kick'].values()):.2f}-{max(v_['eps_top_bin'] for v_ in xc['by_kick'].values()):.2f})",
             "BREAKS" if not sw else "passes"))
# (h) mergers
mg = cn["mergers_L370"]
hk = "kernel_off" if C["door_in_scored_column"] else "main"
rows.append(("(h) El Gordo (L370)", mg["main"]["A3_el_gordo_dchi"], mg[hk]["A3_el_gordo_dchi"],
             "EASE LOST (back to LCDM's tension)" if hk == "kernel_off" else "unchanged"))
rows.append(("(h) Harvey (L370)", f"intact {mg['main']['B2_intact']}", f"intact {mg[hk]['B2_intact']}; core-decayed "
             f"{mg[hk]['B3_core_decayed']}", "passes if the cluster carrier is intact or uniformly depleted"))
# (i) groups
gr = cn["groups"]
gk = gr["kicks_pass_door"] if C["door_in_scored_column"] else gr["kicks_pass_Mstar"]
rows.append(("(i) groups at 2e13 (item 7)", f"kicks passing {[t for t, v_ in gr['kicks_pass_Mstar'].items() if v_]}",
             f"kicks passing {[t for t, v_ in gk.items() if v_] or 'none'}" + (f"; a step at M_cap (x{min(gr['step_factor_at_Mcap'].values()):.0f}-"
             f"{max(gr['step_factor_at_Mcap'].values()):.0f})" if C["door_in_scored_column"] else ""),
             "BREAKS" if not any(gk.values()) else "passes"))
# unchanged / rule costs
rows.append(("RAR, RC100 (SPARC below M_cap)", "pass", f"unchanged (SPARC max {en['sparc_max_Mb']['Mb']:.1e} Msun)", "UNCHANGED"))
rows.append(("Gaia DR4 wide binaries (the Sun keeps the Galaxy)", "untouched",
             f"untouched (s*(Sun) = {en['solar_neighbourhood_s_star_kpc']['Sun']['canonical']:.2f} kpc < l_obj)", "UNCHANGED"))
i93 = en["item93"]
rows.append(("hunt item 93, outer-halo globulars (M/L_V needed)", f"{i93['control']['canonical'][0]:.2f} (with EFE)",
             f"{i93['by_l_obj']['l1']['joint']['canonical'][0]:.2f} under R1 at 1 kpc (all four separate); unchanged under R2",
             "WORSE under R1"))
gcs = en["mw_globulars_R1"]["by_l_obj"]["l1"]
rows.append(("the object rule (R1 at l_obj = 1 kpc)", "-", f"separates {gcs['n_objects']}/157 Milky Way globulars "
             f"({gcs['n_inside_20kpc']} inside 20 kpc); window {en['l_obj_window_kpc'][0]:.2f}-{en['l_obj_window_kpc'][1]:.2f} kpc",
             "NEW CONSTANT + a type rule"))
P("\n  " + "-" * 116)
for g_, m_, d_, v_ in rows:
    P(f"  {g_:52s} | M*: {m_}\n  {'':52s} | {'door' if scored else 'scored (M*)'}: {d_}\n  {'':52s} | => {v_}")
    P("  " + "-" * 116)
flips = sum(1 for r_ in rows if r_[3].startswith("FLIPS"))
breaks = sum(1 for r_ in rows if r_[3].startswith("BREAKS") or r_[3].startswith("NEW FAILURE") or r_[3].startswith("EASE LOST"))
check("T2 (reported) THE NET: gates the door flips to a pass against gates it breaks or newly fails (the task's gates plus the MW-M31 "
      "timing the partition forces)", f"{flips} flip(s), {breaks} broken or new", True, load_bearing=False)
OUT["numbers"]["rows"] = [dict(gate=r_[0], Mstar=r_[1], door=r_[2], verdict=r_[3]) for r_ in rows]
OUT["numbers"]["net"] = dict(flips=flips, broken_or_new=breaks)
nlb = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), nlb
fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
json.dump(OUT, open(fn, "w"), indent=1)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}")
sys.exit(1 if nlb else 0)
