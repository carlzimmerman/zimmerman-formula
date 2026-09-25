#!/usr/bin/env python3
"""
W03 -- WALLABY DR2 ARBITRATION-CARD FEASIBILITY AUDIT (N05/U02 open door)
2026-09-25.  Conductor-run lane (W-WAVE_BRIEF.md, kills pre-registered there).

Door: U02's refreshed card -- SPARC-deficit 5sig attribution needs 1656 deep
rings; cross-channel 5sig difference needs n = 232 NEW deep rings per channel.
Does WALLABY DR2 (data2/, on disk, UNTRACKED) supply the deep-band rings?
FEASIBILITY AUDIT ONLY -- no a0_eff measured, no physics claim (K3).

Definitions fixed BEFORE counting (W-WAVE_BRIEF.md):
  deep band: log10(g_bar/a0) < -0.7, a0 = 9.3619e-11 m/s^2
  z = 1420.405752 MHz/freq - 1 (kinematic catalogue); distance dist_h (Mpc,
  source catalogue, Hubble flow) fallback (c/70)*z
  g_bar = Vrot_model^2 / R_phys; R_phys = Rad_arcsec*(pi/180/3600)*D_Mpc*3.0856775814913673e22
  ring counts if: deep AND Vrot_model > 3*e_Vrot_model AND Inc_model >= 30
Kills:
  K1 machinery: recompute U02 F2 SPARC N (1e-9) and F3 n=232 (1e-9).
  K2 both-ways: N_res >= 232 -> CROSS-CHANNEL-FEASIBLE; >= 1656 -> also
     SPARC-SIDE-FEASIBLE; else INFEASIBLE (shortfall + blocker recorded).
  K3: feasibility card only.
"""
import csv, json, math, os, time

HERE = os.path.dirname(os.path.abspath(__file__))
A0 = 9.3619e-11
C_KMS = 299792.458
res = {"lane": "W03_wallaby_card", "prereg": "W-WAVE_BRIEF.md",
       "checks": {}, "t_start": time.strftime("%Y-%m-%d %H:%M:%S")}
def rec(name, ok, detail):
    res["checks"][name] = {"pass": bool(ok), "detail": detail}
    print("  [%s] %s   %s" % ("PASS" if ok else "FAIL", name, detail), flush=True)

# ------------------------------------------------------------------- K1 gate
U02 = json.load(open(os.path.join(HERE, "U02_arbitration_refresh_results.json")))
s1s, s1m = U02["f1"]["sigma1_sparc"], U02["f1"]["sigma1_mightee"]
ds, dm = U02["f3"]["delta_sparc_a0E"], U02["f3"]["delta_mightee_a0E"]
f2 = (5.0 * s1s / ds) ** 2
n3 = math.ceil((5.0 * math.sqrt(s1s ** 2 + s1m ** 2) / abs(dm - ds)) ** 2)
ok2 = abs(f2 - U02["f2"]["recompute_sparc"]) < 1e-9
ok3 = n3 == U02["f3"]["n_per_channel_5sig"]
rec("K1_recompute_F2_1e-9", ok2, "%.10f vs %.10f" % (f2, U02["f2"]["recompute_sparc"]))
rec("K1_recompute_F3_1e-9", ok3, "n=%d vs stored %d" % (n3, U02["f3"]["n_per_channel_5sig"]))

# ------------------------------------------------------------- WALLABY census
kpath = os.path.join(HERE, "data2", "wallaby_dr2_kinematic_catalogue.tsv")
spath = os.path.join(HERE, "data2", "wallaby_dr2_source_catalogue.tsv")
dist_by_name = {}
with open(spath) as fh:
    for row in csv.DictReader(fh, delimiter="\t"):
        try:
            dist_by_name[row["name"]] = (float(row["z"]), float(row["dist_h"]))
        except (KeyError, ValueError):
            pass
print("source catalogue: %d rows with (z, dist_h)" % len(dist_by_name), flush=True)

n_gal = 0; n_rings_tot = 0; deep_rings = 0; deep_gals = set()
blocked = {"no_dist": 0, "qflag": 0, "low_inc": 0, "low_sn": 0, "parse": 0}
per_gal = []
with open(kpath) as fh:
    for row in csv.DictReader(fh, delimiter="\t"):
        n_gal += 1
        try:
            freq = float(row["freq"])
            z = 1420.405752e6 / freq - 1.0
            dist = dist_by_name.get(row["name"], (None, None))[1]
            if dist is None or not (dist > 0):
                dist = (C_KMS / 70.0) * z * (1 + z)  # fallback Hubble flow
                blocked["no_dist"] += 1
            inc = float(row["Inc_model"])
            qflag = float(row["QFlag_model"])
            rad = [float(x) for x in row["Rad"].split(",") if x.strip()]
            vrot = [float(x) for x in row["Vrot_model"].split(",") if x.strip()]
            ev = [float(x) for x in row["e_Vrot_model"].split(",") if x.strip()]
        except (ValueError, KeyError):
            blocked["parse"] += 1
            continue
        if qflag != 0.0:
            blocked["qflag"] += 1; continue
        if inc < 30.0:
            blocked["low_inc"] += 1; continue
        n_deep_here = 0
        for R, v, ev_ in zip(rad, vrot, ev):
            n_rings_tot += 1
            if v <= 3.0 * ev_:
                blocked["low_sn"] += 1; continue
            R_m = R * (math.pi / 180.0 / 3600.0) * dist * 3.0856775814913673e22
            if R_m <= 0: continue
            gbar = (v * 1000.0) ** 2 / R_m
            if math.log10(gbar / A0) < -0.7:
                n_deep_here += 1; deep_rings += 1
        if n_deep_here:
            deep_gals.add(row["name"])
            per_gal.append(dict(name=row["name"], z=round(z, 4), dist_mpc=round(dist, 2),
                                inc=inc, deep_rings=n_deep_here, rings=len(rad)))
res["census"] = dict(
    n_gal_rows=n_gal, rings_total=n_rings_tot, deep_rings=deep_rings,
    deep_galaxies=len(deep_gals), blockers=blocked,
    sample_gals_with_deep=per_gal[:12])
print("galaxies: %d rows | rings: %d | DEEP rings: %d in %d galaxies"
      % (n_gal, n_rings_tot, deep_rings, len(deep_gals)), flush=True)
print("blockers: %s" % blocked, flush=True)

# ------------------------------------------------------------- K2 both-ways
N_RES = deep_rings
verdict = ("CROSS-CHANNEL-FEASIBLE + SPARC-SIDE-FEASIBLE" if N_RES >= 1656
           else "CROSS-CHANNEL-FEASIBLE" if N_RES >= 232
           else "INFEASIBLE")
rec("K2_wallaby_feasibility", True,
    "N_res=%d vs n_diff=232 (cross-channel) and 1656 (SPARC side) -> %s"
    % (N_RES, verdict))
res["verdict"] = verdict
res["card_targets"] = dict(n_diff=n3, n_sparc=U02["f2"]["N_sparc_5sig"])

ok = all(v["pass"] for v in res["checks"].values())
res["exit"] = 0 if ok else 1
json.dump(res, open(os.path.join(HERE, "W03_wallaby_card_results.json"), "w"), indent=1)
print("WROTE W03_wallaby_card_results.json", flush=True)
print("ALL W03 CHECKS PASSED" if ok else "W03 CHECKS FAILED", flush=True)
raise SystemExit(0 if ok else 1)
