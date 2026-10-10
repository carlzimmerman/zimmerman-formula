#!/usr/bin/env python3
"""CFG592 final tables (no new computation): applies the frozen and addendum rules to the stored JSONs and builds the
movement table of ADDENDUM Part A4.  python3 cfg592_final.py -> cfg592_final.out, cfg592_final.json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
L = lambda f: json.load(open(os.path.join(HERE, f)))
FZ, FM, NA, NM, DE = L("cfg592_results.json"), L("cfg592_results_MUTATE.json"), L("cfg592_native_results.json"), L("cfg592_native_results_MUTATE.json"), L("cfg592_de_results.json")
OUT = []; R = {}
def P(s=""): print(s); OUT.append(s)

# ---------------- frozen track: MU2 -> NOT DIAGNOSTIC (criteria section 5/7)
mu2 = {s: FM["mutate_results"][s]["MU2"] for s in ("KiDS", "DES")}
P("FROZEN HMcode track (criteria a3a22a833): MU2 (injected 20% excess at k >= 1 detected) = " + str(mu2) +
  " -> every framework class NOT DIAGNOSTIC by the frozen rule; raw classes below are reported only.")
R["frozen"] = {"MU2": mu2, "controls": {"C1_KiDS": FZ["lcdm"]["KiDS"]["C1_pass"], "C1_DES": FZ["lcdm"]["DES"]["C1_pass"],
               "C2": {s: FZ["controls"]["C2"][s]["pass_"] for s in ("KiDS", "DES")}}, "rows": {}}
for s in ("KiDS", "DES"):
    l = FZ["lcdm"][s]
    P(f"  LCDM {s}: mode A chi2 {l['modeA']['chi2']:.2f} / N {FZ['surveys'][s]['N_data']}; S8 free {l['modeB']['S8']:.4f} [{l['modeB']['S8_lo']:.4f}, {l['modeB']['S8_hi']:.4f}] vs ref {l['S8_ref']:.4f} (C1 {'PASS' if l['C1_pass'] else 'FAIL'})")
for foot in ("canonical", "alt"):
    for m, o in FZ["framework"][foot].items():
        row = {s: dict(dchi2_A=o[s]["dchi2_A"], raw_class_A=o[s]["class_A"], dchi2_B=o[s]["dchi2_B"], raw_class_B=o[s]["class_B"], S8_B=o[s]["modeB"]["S8"],
                       Planck_T=o[s]["Planck_T"], final="NOT DIAGNOSTIC" if not mu2[s] else o[s]["class_A"]) for s in ("KiDS", "DES")}
        R["frozen"]["rows"][f"{foot}|{m}"] = row
        P(f"  {foot:9s} {m:30s} KiDS dchi2 {row['KiDS']['dchi2_A']:+7.2f} (raw {row['KiDS']['raw_class_A']}), DES {row['DES']['dchi2_A']:+6.2f} (raw {row['DES']['raw_class_A']}); "
          f"S8-free dchi2 {row['KiDS']['dchi2_B']:+.2f} / {row['DES']['dchi2_B']:+.2f}, S8 {row['KiDS']['S8_B']:.3f} / {row['DES']['S8_B']:.3f} -> FINAL NOT DIAGNOSTIC")

# ---------------- native track
P("\nFRAMEWORK-NATIVE track (addendum 65fa05a07): PRIMARY set")
R["native"] = {}
for n, r in NA["runs"].items():
    if not r["primary_set"]: continue
    row = {}
    for s, v in r["surveys"].items():
        row[s] = dict(N_kept=v["N_kept"], N_published=v["N_published"], dchi2=v.get("dchi2"), dchi2_noIA=v.get("dchi2_noIA"), robust=v.get("robust"),
                      final=v["class"], NZ2=NM["NZ2"].get(n, {}).get(s), posthoc=v.get("posthoc_support"))
    R["native"][n] = dict(foot=r["foot"], branch=r["branch"], N=r["N"], L=r["L"], k_hi=r["k_hi"], surveys=row)
    P(f"  {n:22s} ({r['foot']}, {r['branch']}, L{r['L']:.0f} N{r['N']}, k <= {r['k_hi']:.2f}): " + "; ".join(
        f"{s} N {x['N_kept']}/{x['N_published']}" + (f", dchi2 {x['dchi2']:+.2f} (no IA {x['dchi2_noIA']:+.2f})" if x["dchi2"] is not None else "") + f" -> {x['final']}"
        for s, x in row.items()))

# ---------------- movement table (Part A4)
P("\nMOVEMENT of the framework's dchi2 under each inherited assumption (numbers from the JSONs)")
mv = {}
for foot, nat in (("canonical", "530_LRcan_L100_N512"), ("alt", "530_LRalt_L100_N512")):
    fr = R["frozen"]["rows"][f"{foot}|PRIMARY"]; nv = NA["runs"][nat]["surveys"]
    w1 = DE["backgrounds"]["w=-1 (As fixed; check vs frozen mode A)"]["framework"][foot]["PRIMARY"]
    dm = DE["backgrounds"]["DESI median"]["framework"][foot]["PRIMARY"]
    for s in ("KiDS", "DES"):
        fc = NA["runs"][nat].get("feedback_context", {}).get(s, {})
        e = {"HMcode x R(k), frozen mode A (225/227 points)": fr[s]["dchi2_A"],
             "same, S8 free": fr[s]["dchi2_B"],
             "HMcode x R(k), DESI w0wa median + a0 tracking": dm[s]["dchi2"],
             "HMcode x R(k), w = -1 via the DE script (check)": w1[s]["dchi2"],
             f"PM-native {nat} (no feedback, IA marg.; {nv[s]['N_kept']} points)": nv[s].get("dchi2"),
             "PM-native, no IA": nv[s].get("dchi2_noIA"),
             "PM-native, boost fade bracket": (nv[s].get("robust") or {}).get("fade"),
             "PM-native, DESI distances": (nv[s].get("robust") or {}).get("DESI"),
             "PM-native, priors x2": (nv[s].get("robust") or {}).get("widen2")}
        for T, x in fc.items(): e[f"PM-native + BAHAMAS T {T} (externally calibrated)"] = x["dchi2"]
        mv[f"{foot}|{s}"] = e
        P(f"  {foot} {s}:")
        for k, v in e.items(): P(f"    {k:62s} {'n/a' if v is None else f'{v:+.2f}'}")
R["movement"] = mv
json.dump(R, open(os.path.join(HERE, "cfg592_final.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg592_final.out"), "w").write("\n".join(OUT) + "\n")
