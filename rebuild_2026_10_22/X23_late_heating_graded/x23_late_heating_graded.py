#!/usr/bin/env python3
"""X23_late_heating_graded: X22's late-heating window graded on X19's classes and the hosted dwarfs, per system.

Frozen criteria: FROZEN_CRITERIA.md (6ec6b89807). X22's hydrostatic profile and CFG946 constants copied verbatim;
X19 / X22 JSON and X1's per-system CSV read-only. One thread, seconds.

    python3 x23_late_heating_graded.py            -> .out, _results.json
    python3 x23_late_heating_graded.py --mutate   -> c_s,need x 2 (K0 must fail), _MUTATE outputs
"""
import csv, json, math, os, resource, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.integrate import quad

T0 = time.time()
MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
RB = os.path.abspath(os.path.join(HERE, ".."))
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.append(s)

# ------------------------------------------------------------------ X22's constants and profile (verbatim)
G_SI, KPC946, MSUN946, PC946 = 6.67430e-11, 3.0856775814913673e19, 1.98847e30, 3.0856775814913673e16
MPC_M = 1e6 * PC946
H0_946 = 67.4e3 / MPC_M
RHOC_946 = 3 * H0_946 ** 2 / (8 * math.pi * G_SI)
OB946 = 0.0493
OC946 = 5.364 * OB946
OM946 = OB946 + OC946
RHOM946 = OM946 * RHOC_946
DTA = 5.55
BCAP = 2.9
def r_ta(Mb_kg):
    return (3 * (OM946 / OB946) * Mb_kg / (4 * math.pi * DTA * RHOM946)) ** (1.0 / 3.0)
def hydro_frac_enclosed(beta, x):          # M_c(<r)/(5.364 M_b) at x = r/r_ta
    ex = 3.0 - beta
    return (1.0 / DTA) * 3.0 / (3.0 - beta) * np.power(np.minimum(x, 1.0), ex)
def law_g(gN, a0):
    gN = np.asarray(gN, float)
    return 0.5 * (gN + np.sqrt(gN * gN + 4.0 * gN * a0))

A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
X19 = json.load(open(os.path.join(RB, "X19_selector_rank_test", "x19_selector_rank_test_results.json")))
X22 = json.load(open(os.path.join(RB, "X22_cosmic_dust_window", "x22_cosmic_dust_window_results.json")))
CS = {f: X22["step2"]["per_footing"][f]["cs_need_kms"] * (2.0 if MUTATE else 1.0) for f in FOOTS}
HCLS = ("MW ultra-faint", "bright M31", "M31 others")
X19_EXTRA = ["Clusters T2", "Clusters T3", "MW ultra-faint", "bright M31", "M31 others"]       # printed in X19 .out (both footings)
X19_NONE = {"canonical": ["SPARC small", "SPARC large", "Groups", "Clusters T1", "MW disc", "LG field", "Crater II", "UMa members", "TDGs", "DF2/DF4"]}
X19_NONE["alt"] = X19_NONE["canonical"][:7] + ["Antlia II"] + X19_NONE["canonical"][7:]   # A1: X19 .out per footing (Antlia II NONE on alt)

def e_pred(Mb_tot_msun, r_m, gN, sigma_kms, a0, cs_kms):
    beta_raw = 2.0 * sigma_kms ** 2 / cs_kms ** 2
    beta = min(beta_raw, BCAP)
    Mb = Mb_tot_msun * MSUN946
    Mc = 5.364 * Mb * float(hydro_frac_enclosed(beta, r_m / r_ta(Mb)))
    gc = G_SI * Mc / r_m ** 2
    return float(np.log10(law_g(gN + gc, a0) / law_g(gN, a0))), beta_raw, beta_raw >= BCAP, gc / gN

def label(z):
    return "EXTRA" if z >= 2 else ("NONE" if z < 1 else "AMBIGUOUS")

P(f"X23_late_heating_graded  {'MUTATE run (c_s,need x 2)' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings canonical 9.3603e-11 / alt 1.1312e-10 never pooled; field mass, not a particle; not theory closed")
RES = dict(frozen="6ec6b89807", mutate=MUTATE, cs_need=CS, footings={})
checks = []
k0 = abs(CS["canonical"] - 190.014) < 0.01 and abs(CS["alt"] - 201.315) < 0.01
k0 = k0 and abs(X19["E_table"]["canonical|iso"]["SPARC small"]["E"] + 0.046) < 0.0006 \
         and abs(X19["E_table"]["canonical|iso"]["MW ultra-faint"]["E"] - 0.625) < 0.0006
for f in FOOTS:
    ET = X19["E_table"][f"{f}|iso"]
    lab = {c: label(v["Z"]) for c, v in ET.items() if c != "Cosmic background"}
    k0 = k0 and sorted(c for c, l in lab.items() if l == "EXTRA") == sorted(X19_EXTRA) \
              and sorted(c for c, l in lab.items() if l == "NONE") == sorted(X19_NONE[f])
P(f"K0 c_s,need {CS['canonical']:.3f} / {CS['alt']:.3f} km/s; X19 E and L-S label sets reproduced: {'PASS' if k0 else 'FAIL'}")
checks.append(("K0", k0))

# K2: closed form vs quadrature
k2 = max(abs(quad(lambda s: 3.0 / DTA * s ** 2 * s ** (-b), 0, 0.37, limit=200)[0] - float(hydro_frac_enclosed(b, 0.37)))
         for b in (0.0, 1.0, 2.5)) < 1e-8
P(f"K2 closed form vs quadrature (beta 0, 1, 2.5): {'PASS' if k2 else 'FAIL'}"); checks.append(("K2", k2))

for f in FOOTS:
    a0, cs = A0[f], CS[f]
    IV = X19["intervals"][f"{f}|p16_84"]; ET = X19["E_table"][f"{f}|iso"]
    FR = RES["footings"][f] = {"classes": {}}
    P(f"\n=== [{f}] c_s = {cs:.1f} km/s;  class: sigma  beta  E_pred  E_obs +- s  Z_res  -> grade   (X19 label)")
    fails = []
    for c, iv in IV.items():
        if c == "Cosmic background" or c not in ET:
            continue
        Mb, sig, rho, x = iv["M_b"][2], iv["sigma"][2], iv["rho_b"][2], iv["x"][2]
        gN = x * a0
        rho_si = rho * MSUN946 / PC946 ** 3
        r = 3 * gN / (4 * math.pi * G_SI * rho_si)
        Ep, braw, capd, gcr = e_pred(Mb, r, gN, sig, a0, cs)
        Eo, s = ET[c]["E"], ET[c]["s"]
        zr = (Eo - Ep) / s
        xl = label(ET[c]["Z"])
        grade = "REPRODUCED" if abs(zr) < 2 else ("UNDER" if zr > 0 else "OVER")
        decisive = xl in ("EXTRA", "NONE")
        if decisive and grade != "REPRODUCED":
            fails.append(f"{c} ({grade})")
        zp = Ep / s; lp = label(zp)                                   # A1 (reported only): label-level reading
        if decisive and lp != xl:
            FR.setdefault("A1_label_mismatch", []).append(f"{c} (pred {lp}, X19 {xl})")
        FR["classes"][c] = dict(Z_pred=zp, label_pred=lp, sigma=sig, r_kpc=r / KPC946, r_over_rta=r / r_ta(Mb * MSUN946), beta=braw, captured=capd,
                                gc_over_gN=gcr, E_pred=Ep, E_obs=Eo, s=s, Z_res=zr, grade=grade, x19_label=xl, decisive=decisive)
        P(f"  {c:15s} {sig:7.1f}  {braw:8.3g}{'*' if capd else ' '} {Ep:+.4f}  {Eo:+.3f} +- {s:.3f}  {zr:+6.2f}  -> "
          f"{grade:10s} ({xl}{'' if decisive else ', not decisive'}; r {r / KPC946:.3g} kpc, r/r_ta {r / r_ta(Mb * MSUN946):.3g})")
    P("  (* = CAPTURED: beta at the cap 2.9, graded at the cap as X22)")

    # hosted dwarfs per system
    rows = [r for r in csv.DictReader(open(os.path.join(RB, "X1_hosted_recount", "x1_per_system.csv")))
            if r["footing"] == f and r["cls"] in HCLS]
    ok, eps = 0, []
    for r in rows:
        Mb = 10 ** float(r["logMstar"]); r12 = 4.0 / 3.0 * float(r["rh_pc"]) * PC946
        gN = G_SI * (Mb / 2) * MSUN946 / r12 ** 2
        Ep, braw, capd, _ = e_pred(Mb / 2, r12, gN, float(r["sigma"]), a0, cs)   # M_b(<r12) = M_b/2 normalises M_c's share
        Eo, s = float(r["Delta[iso AQUAL L*0]"]), float(r["sdMC[iso AQUAL L*0]"])
        eps.append(Ep); ok += Ep >= Eo - 2 * s
    FR["hosted_per_system"] = dict(N=len(rows), frac_consistent=ok / len(rows), median_E_pred=float(np.median(eps)),
                                   max_E_pred=float(np.max(eps)))
    P(f"  hosted dwarfs per system: N {len(rows)}; median E_pred {np.median(eps):.2e} dex (max {np.max(eps):.2e}); "
      f"consistent (E_pred >= E_obs - 2s) {ok}/{len(rows)}")
    P("  A1 (post-result, reported only) label-level mismatches: " + (", ".join(FR.get("A1_label_mismatch", [])) or "none"))
    FR["verdict"] = "LATE HEATING REPRODUCES THE PATTERN" if not fails else "LATE HEATING FAILS: " + ", ".join(fails)
    P(f"  VERDICT [{f}]: {FR['verdict']}")

    if f == "canonical":   # K1 limits on one class (SPARC small)
        iv = IV["SPARC small"]; gN = iv["x"][2] * a0; rho_si = iv["rho_b"][2] * MSUN946 / PC946 ** 3
        r = 3 * gN / (4 * math.pi * G_SI * rho_si); Mb = iv["M_b"][2]
        Ep_inf = e_pred(Mb, r, gN, iv["sigma"][2], a0, 1e12)[0]
        Mc0 = 5.364 * Mb * MSUN946 / DTA * (min(r / r_ta(Mb * MSUN946), 1.0)) ** 3
        an = float(np.log10(law_g(gN + G_SI * Mc0 / r ** 2, a0) / law_g(gN, a0)))
        allcap = all(e_pred(v["M_b"][2], 1.0 * KPC946, 1e-11, v["sigma"][2], a0, 1e-6)[2] for c, v in IV.items() if c != "Cosmic background")
        k1 = abs(Ep_inf - an) < 1e-10 and allcap
        P(f"  K1 beta->0 limit {Ep_inf:.3e} vs analytic {an:.3e}; c_s->0 all CAPTURED {allcap}: {'PASS' if k1 else 'FAIL'}")
        checks.append(("K1", k1))

V = {f: RES["footings"][f]["verdict"] for f in FOOTS}
same = [c.split(" (")[0] for c in V["canonical"].split(": ")[-1].split(", ")] == [c.split(" (")[0] for c in V["alt"].split(": ")[-1].split(", ")]
RES["verdict"] = (V["canonical"] if same else "UNDECIDED (footings disagree)")
P(f"\n=== VERDICT (both footings): {RES['verdict']}")
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
checks.append(("K3", rss < 1.0))
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}
n = sum(ok for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.1f} s; peak RSS {rss:.3f} GB")
open(os.path.join(HERE, f"x23_late_heating_graded{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x23_late_heating_graded_results{TAG}.json"), "w"), indent=1)
sys.exit(0 if n == len(checks) else 1)
