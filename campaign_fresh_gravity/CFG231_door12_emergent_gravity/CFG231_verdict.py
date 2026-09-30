#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG231_verdict -- reads the results JSONs of A1..A7 and prints the G1-G5 table per variant (PASS / FAIL / UNDEFINED / NOT ADDRESSED; p* = passes only
trivially or by construction), the binding gate per variant, and the G1-as-mechanism flag.  No physics here.
Exit 0 if every input JSON exists and its reproduction controls passed (0 load-bearing failures).
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG231_common as C

OUT = os.environ.get("CFG231_OUT", C.HERE)
R = C.Report("CFG231_verdict")
C.header(R, "CFG231 verdict -- gate table per variant")


def load(slug):
    p = os.path.join(OUT, slug + "_results.json")
    if not os.path.exists(p):
        R.P(f"  MISSING {slug}_results.json"); return None
    return json.load(open(p))


A1, A2, A3, A4, A5, A6, A7 = (load(f"CFG231_A{i}_" + n) for i, n in ((1, "point_mass_algebra"), (2, "sphere_charge_function"), (3, "vector_class"),
                                                                     (4, "cosmology"), (5, "reaction_energy"), (6, "solar_stability"), (7, "normalisation_ledger")))
if not all([A1, A2, A3, A4, A5, A6, A7]):
    R.write(); sys.exit(1)
lbf = {k: d["load_bearing_failures"] for k, d in (("A1", A1), ("A2", A2), ("A3", A3), ("A4", A4), ("A5", A5), ("A6", A6), ("A7", A7))}
R.P(f"  load-bearing control failures per script: {lbf}")
summ = A2["numbers"]["summary"]
split = A2["numbers"]["G1_split_by_norm"]
strict = A2["numbers"]["G1_strict_verdict"]
VARS = ["V0", "V2", "B1", "B2", "B3", "B4", "K3", "K1"]


def g1_cell(v):
    s = summ[v]["HL"]
    parts = [f"{nm.replace('tie_', '')} {s[nm]['n_pass']}/{s[nm]['n']}" for nm in ("shape", "tie_canonical", "tie_alt")]
    txt = ("PASS" if strict[v]["HL"] else "FAIL") + " (strict cells passing, H_Lambda: " + "; ".join(parts) + f"; point {s['shape']['n_point_pass']}/7, sphere {s['shape']['n_sphere_pass']}/7 in N-shape; admissible {s['shape']['adm_all']})"
    return txt


G1P2 = {v: summ[v]["HL"]["shape"]["G1P2_worst"] for v in VARS}
mech = {"V0": "n/a (no scale)", "V2": "n/a (no dark mass)", "B1": "M1 (declared formula)", "B2": "M1 (declared K2)", "B3": "M1 (declared formula + mask)", "B4": "M1 (declared)", "K3": "M1 (declared wall)", "K1": "M1 (declared, = P2 restated); KODE control = M0"}
worstK = A4["numbers"]["G2_with_cold_worst"]
grK2 = A4["numbers"]["growth_ratio_with_cold"]["K2"]
v0g = A4["numbers"]["V0_growth"]
en = A5["numbers"]["energy_range"]
g5 = A6["numbers"]["G5_table"]
q2 = A6["numbers"]["Q2_isolated_sun"]

table = {}
for v in VARS:
    row = {}
    row["G1"] = (g1_cell(v), "A2")
    row["G1_P2"] = (f"{'PASS' if G1P2[v] < 0.1 else 'FAIL'} (worst |g/g_P2 - 1| = {G1P2[v]:.3g})", "A2")
    row["G1_mech"] = (mech[v], "A1 (M2 attempts), A2 (C8)")
    if v in ("K1", "K3", "B2", "B1", "B3", "B4"):
        gk = "K2" if v in ("B1", "B2", "B3", "B4") else v
        row["G2"] = (f"FAIL (with-cold; quasi-static Delta_tot up to {max(w[1] for k_, w in worstK.items() if k_.startswith(gk)):.3g}; growth ratio {min(A4['numbers']['growth_ratio_with_cold'][gk]):.3g}-{max(A4['numbers']['growth_ratio_with_cold'][gk]):.3g}); no-cold UNDEFINED; CMB UNDEFINED", "A4")
    elif v == "V0":
        row["G2"] = (f"FAIL on growth ratio ({v0g['growth_ratio']:.3f}), literal |G_eff/G-1| line P ({v0g['Delta_tot']:.3f}); Delta_b = 1; no-cold, CMB UNDEFINED", "A4")
    else:
        row["G2"] = ("p* (modification ~ 1e-6; nothing to test); no-cold, CMB UNDEFINED", "A3.4, A4")
    row["G3_reaction"] = ("p* (potential force, by construction)", "A5")
    if v in ("K1", "K3", "B2"):
        key = {"K1": "K1", "K3": "K3", "B2": "K2"}[v]
        lo = min(en[f"{key}|point"][0], en[f"{key}|sphere"][0]); hi = max(en[f"{key}|point"][1], en[f"{key}|sphere"][1])
        row["G3_energy"] = (f"FAIL (energy/orbital energy {lo:.3g} to {hi:.3g} over 1e10-1e12 Msun, both r_ta conventions)", "A5")
    elif v in ("B1", "B3"):
        row["G3_energy"] = ("UNDEFINED (no action); under the K2 vector reading FAIL (12.6-15.3 point mass, 3.9-7.1 sphere)", "A5")
    elif v == "V2":
        row["G3_energy"] = ("FAIL as its own field (as K1: 3.4-6.3); dark mass negative", "A5")
    elif v == "V0":
        row["G3_energy"] = (f"mixed (sphere {en['V0|sphere'][0]:.2g}-{en['V0|sphere'][1]:.2g}; point mass cutoff-dominated 1e3)", "A5")
    else:
        row["G3_energy"] = ("UNDEFINED (no action)", "A5")
    from_ledger = A7["numbers"]["ledger"][v]["strict"]
    row["G4"] = (from_ledger, "A7")
    gg = g5[v] if v in g5 else g5["K2"]
    row["G5"] = (f"Q2(a) {gg['Q2_sun']}; Q2(b) {gg['Q2_MW']}; stability {gg['stability']}; gamma {gg['gamma']}", "A3, A6")
    table[v] = row

R.banner("Gate table per variant (H_Lambda primary; the H0 reading is in A2/A7 outputs).  p* = passes only trivially or by construction.")
for v in VARS:
    R.P(f"\n  === {v} ===")
    for g, (txt, src) in table[v].items():
        R.P(f"    {g:12s} [{src}]: {txt}")

R.banner("Binding gate per variant")
bind = {
    "V0": "G1 (no acceleration scale: R = 0 on the point mass) and G5 (the attractive sign is a ghost)",
    "V2": "G1 (dark mass ~1e-6 of the needed and negative)",
    "B1": "G1 (point mass R = (1+x)/x; spheres R up to 18.5)",
    "B2": "G1 (R = (1+x)/x on the point mass; spheres up to 11)",
    "B3": "G1 (R = 0 inside x = 0.577; the gate that repairs the Solar System)",
    "B4": "G1 admissibility (negative dark mass for x < 1; R = 1 alone would pass on the point mass)",
    "K3": "G1 (R = 1 + 1/sqrt(1+4x^2), in band only for x >= 4.98)",
    "K1": "G1 strict on the exponential spheres (R up to 2.3) and on the alt footing (a_V/a0 = 0.7985), and independently G5 (Q2 6.1e3 x the bound); G1-P2 passes only because K1 IS P2",
}
for v in VARS:
    R.P(f"  {v:3s}: {bind[v]}")

R.banner("G1 as a derived mechanism (M2), the flag the orchestrator asked for")
anyG1 = [v for v in VARS if strict[v]["HL"] or strict[v]["H0"]]
R.P(f"  variants passing G1 strict (any H): {anyG1 or 'NONE'}.  Variants graded M2: NONE (A1.2: no derivation of the constitutive function; K1 is P2 restated).")
R.P("  => nothing passes G1; nothing requires the independent re-derivation of section 7 for a pass. (The independent re-derivation asked for a 'pass' is therefore not triggered; a referee re-run of the no-go headlines is what remains useful.)")
R.num("table", {v: {g: t for g, (t, s) in row.items()} for v, row in table.items()})
R.num("binding", bind)
R.num("G1_pass_variants", anyG1)
nf = sum(lbf.values())
R.P(f"\n  total load-bearing control failures across A1..A7: {nf}")
R.write()
sys.exit(0 if nf == 0 else 1)
