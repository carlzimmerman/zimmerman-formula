#!/usr/bin/env python3
"""CFG927 sealed forecast table (FROZEN_CRITERIA.md section 10, commit 8791d53c3): collects cfg927_<PAIR>[_MUTATE].json and
cfg927_noise.json into cfg927_forecast_table.json/md and writes FORECAST_HASH.txt (sha256, `shasum -a 256 -c` format, paths relative to
this directory).  No computation beyond collation.

    OMP_NUM_THREADS=1 nice -n 10 python3 cfg927_table.py
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
PAIRS = [("T1x", "theory-v2 vs CFG596 P0"), ("T2x", "theory-v2 vs CFG596 P0"), ("NC1x", "theory-v2 vs NCS0"),
         ("P1", "CFG596 candidate B (KiDS-EXCLUDED) vs P0")]
GRADED = ["ACT-DR6-like", "SO-baseline-like", "S4-like"]
LMAXES = ["400", "763", "1000", "2000", "3000"]
J = lambda f: json.load(open(os.path.join(HERE, f)))
sha = lambda f: hashlib.sha256(open(os.path.join(HERE, f), "rb").read()).hexdigest()

NZ = J("cfg927_noise.json")
T = dict(lane="CFG927", title="Sealed high-L CMB-lensing discrimination forecast (Fisher, Gaussian covariance, fiducial = control)",
         criteria_commit="8791d53c3", sealed="2026-10-20",
         settings="kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed; a forecast, not "
                  "a measurement; framework-native models only (no LCDM fit, CAMB/CLASS nonlinear spectrum, halofit, HMcode or BAHAMAS)",
         classes="DISCRIMINATING >= 9; MARGINAL 4-9; BLIND < 4; NOT COMPUTABLE if L_max > L_sup (box support cut, FROZEN section 3)",
         scoring_note="if S0 is true the real chi2(F) - chi2(S0) has expectation +dchi2 and sd 2 sqrt(dchi2); if F is true, expectation -dchi2",
         noise_models={nm: dict(NZ["models"][nm]["params"], provenance=NZ["models"][nm]["provenance"]) for nm in NZ["models"]},
         noise_anchors_K7={k: v for k, v in NZ["K7"].items()}, noise_K=dict(K4=NZ["checks"]["K4"]["ok"], K5=NZ["checks"]["K5"]["ok"]),
         pairs={})
for p, desc in PAIRS:
    R, MU = J(f"cfg927_{p}.json"), J(f"cfg927_{p}_MUTATE.json")
    row = dict(description=desc, footing=R["foot"], inputs=R["inputs"], files=R["files"], sha256_inputs=R["sha256"],
               gate_ok=R["gate_ok"], mutate_bites=R["mutate_bites"], flags=R["flags"],
               L_sup=R["support_cut"]["L_sup_label"], support_at=R["support_cut"]["at"],
               cfg917_pr4_realised_dchi2=R["K2"]["stored"]["primary"], pr4_asimov_8_400=R["pr4_asimov_8_400"],
               M2_S4_dchi2_plus_minus_5pct=[MU["M2"]["1.05"]["S4-like"]["pipeline"], MU["M2"]["0.95"]["S4-like"]["pipeline"]],
               cells={}, L_9={}, noise_scan=dict(L=R["noise_scan"]["L"], dT_9=R["noise_scan"]["dT_9"],
                                                 dchi2={k: v["dchi2"] for k, v in R["noise_scan"]["rows"].items()}),
               reading=R["reading"])
    for nm in GRADED + ["CV-limited"]:
        row["cells"][nm] = {hi: dict(L=R["cells"][nm][hi]["L"], dchi2=R["cells"][nm][hi]["dchi2"], class_=R["cells"][nm][hi]["class_"],
                                     robust=R["cells"][nm][hi]["robust"], member_range=R["cells"][nm][hi]["member_range"],
                                     members=R["cells"][nm][hi]["members"], sd_realised=R["cells"][nm][hi]["sd_realised"])
                            for hi in LMAXES}
        row["L_9"][nm] = R["cells"][nm]["L_9"]
    T["pairs"][p] = row
json.dump(T, open(os.path.join(HERE, "cfg927_forecast_table.json"), "w"), indent=1)

f2 = lambda v: f"{v:.2f}" if v < 1000 else f"{v:.0f}"
md = ["# CFG927 sealed forecast table (criteria 8791d53c3; sealed 2026-10-20)", "",
      "Fisher Δχ² between each run's own Limber C_L^φφ and its same-pipeline control (Gaussian covariance, fiducial = control, no data).",
      "Class: D = DISCRIMINATING (≥ 9), M = MARGINAL (4–9), B = BLIND (< 4), NC = NOT COMPUTABLE. `r` = ROBUST across ZHOLD/ZREL/KCUT/KLOW/BG,",
      "`d` = RULE-DEPENDENT (member range in the JSON). L_sup per pair: " + ", ".join(f"{p} {r['L_sup']}" for p, r in T["pairs"].items())
      + f" (max k > 7.98 h/Mpc share at L 8–3000: S0 {max(J(f'cfg927_{p}.json')['support_cut']['max_s_S0'] for p, _ in PAIRS):.4f}, "
      + f"F − S0 {max(J(f'cfg927_{p}.json')['support_cut']['max_s_dX'] for p, _ in PAIRS):.4f}; threshold 0.10).", "",
      "| pair | footing / inputs | model | " + " | ".join(f"L ≤ {h}" for h in LMAXES) + " | L_9 |", "|---|---|---|" + "---|" * len(LMAXES) + "---|"]
ab = {"DISCRIMINATING": "D", "MARGINAL": "M", "BLIND": "B", "NOT COMPUTABLE": "NC"}
for p, row in T["pairs"].items():
    for nm in GRADED + ["CV-limited"]:
        cs = [row["cells"][nm][h] for h in LMAXES]
        txt = [f"{f2(c['dchi2'])} {ab.get(c['class_'], c['class_'])}{'' if c['class_'] == 'NOT COMPUTABLE' else ('r' if c['robust'] else 'd')}" for c in cs]
        lab = nm + (" (context)" if nm == "CV-limited" else "")
        md.append(f"| {p} | {row['footing']} / {row['inputs']} | {lab} (L_min {cs[0]['L'][0]}) | " + " | ".join(txt) + f" | {row['L_9'][nm] or 'none ≤ 3000'} |")
md += ["", "| pair | noise scan Δχ² at L 30–3000, f_sky 0.4, beam 1.4′ (Δ_T in μK-arcmin) | Δ_T for Δχ² = 9 | PR4 8–400 Asimov | CFG917 realised PR4 Δχ² | gate K / MUTATE |",
       "|---|---|---|---|---|---|"]
for p, row in T["pairs"].items():
    sc = ", ".join(f"{k}: {f2(v)}" for k, v in row["noise_scan"]["dchi2"].items())
    d9 = row["noise_scan"]["dT_9"]; d9 = d9 if isinstance(d9, str) else f"{d9:.2f}"
    md.append(f"| {p} | {sc} | {d9} | {row['pr4_asimov_8_400']:.3f} | {row['cfg917_pr4_realised_dchi2']:+.3f} | {'PASS' if row['gate_ok'] else 'FAIL'} / {'bites' if row['mutate_bites'] else 'NO BITE'} |")
md += ["", "Noise models: " + "; ".join(f"{nm} Δ_T {v['dT']}, beam {v['fwhm']}′, CMB ℓ T {v['lmin']}–{v['lmaxT']} / P {v['lmin']}–{v['lmaxP']}, f_sky {v['fsky']} ({v['provenance']})"
                                     for nm, v in T["noise_models"].items()) + ".",
       "K7 anchors (reported): " + "; ".join(f"{k} σ(A) {v['sigma_A_forecast']:.4f}" + (f" vs on-disk {v['sigma_A_published_on_disk']} (ratio {v['ratio']:.2f})" if "ratio" in v else "")
                                             for k, v in T["noise_anchors_K7"].items()) + ".",
       "", "κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed. A forecast is not a measurement."]
open(os.path.join(HERE, "cfg927_forecast_table.md"), "w").write("\n".join(md) + "\n")

files = ["FROZEN_CRITERIA.md", "cfg927_noise.py", "cfg927_forecast.py", "cfg927_table.py", "cfg927_noise.json", "cfg927_noise.out"]
for p, _ in PAIRS: files += [f"cfg927_{p}_MUTATE.json", f"cfg927_{p}_MUTATE.out", f"cfg927_{p}.json", f"cfg927_{p}.out"]
files += ["cfg927_forecast_table.json", "cfg927_forecast_table.md", "../CFG917_cmb_lensing_gate/cfg917_lib.py"]
open(os.path.join(HERE, "FORECAST_HASH.txt"), "w").write("".join(f"{sha(f)}  {f}\n" for f in files))
print("\n".join(md)); print(f"\nFORECAST_HASH.txt: {len(files)} files; table sha256 {sha('cfg927_forecast_table.json')}")
