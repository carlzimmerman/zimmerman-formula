#!/usr/bin/env python3
"""Write PREDICTIONS_V3.md from SEALED_V3_MW_DR4.json (every number from the sealed JSON; the hash is checked first)."""
import os
import sys
import json
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
blob = open(os.path.join(HERE, "SEALED_V3_MW_DR4.json"), "rb").read()
sha = hashlib.sha256(blob).hexdigest()
ref = open(os.path.join(HERE, "PREDICTIONS_V3_HASH.txt")).read().split()[0]
assert sha == ref, "hash mismatch"
D = json.loads(blob)
SS = D["inputs"]["s_band"]
sk = [f"{s:.6f}" for s in SS]
c = sk[2]
L = []
w = L.append
w("# v3 sealed Gaia DR4 Milky Way predictions (lane S3_v3_mw_seals)")
w("")
w(f"- **Sealed object:** `SEALED_V3_MW_DR4.json`, SHA-256 `{sha}` (`PREDICTIONS_V3_HASH.txt`). Committed before the DR4 release (2026-12-02).")
w("  Never edit either file after the seal; any change goes into a new, dated file. This is NOT CFG553 (the record's old-model set, untouched).")
w(f"- **Theory:** {D['theory']}.")
w(f"- **Inputs:** {D['inputs']['baryons']}; s band {', '.join(f'{s:.5f}' for s in SS)}; e_N (h81, ΛCDM-processed) {D['inputs']['e_N_h81']}; "
  f"field toward (l, b) = {tuple(D['inputs']['field_direction_lb_deg'])}, γ = {D['inputs']['gamma_deg']}°; R0 = {D['inputs']['R0_kpc']} kpc; "
  f"3-D estimator {D['inputs']['3d']['estimator']} (validated by C5: {D['inputs']['3d']['validated_C5']}).")
w(f"- **Rules after DR4:** {D['rules']}.")
w("- κ = ½ FITTED; footings never pooled; no dark-matter particle; predictions, not results; not theory closed.")
w("")
w("## Headline (census s = 1; band = min–max over the five s values)")
w("")
w("| quantity | footing | v3 (EFE) | v3 isolated | NFW fitted to Ou+24 |")
w("|---|---|---|---|---|")


def band(model, foot, path):
    vals = []
    for s in sk:
        d = D[model][foot][s] if model != "NFW_Ou24" else D[model][s]
        for p in path:
            d = d[p]
        vals.append(d)
    return vals


def fmt(vals, f="{:.1f}"):
    return f"{f.format(vals[2])} ({f.format(min(vals))}–{f.format(max(vals))})"


rows = [("V_c(20 kpc), anticentre wedge [km/s]", ["P2_Vc_anticentre_wedge", "R20"], ["P2_Vc", "R20"], ["P2_Vc", "R20"], "{:.1f}"),
        ("dlnV/dlnR 15–22 kpc", ["P2_slope_15_22"], ["P2_slope_15_22"], ["P2_slope_15_22"], "{:+.3f}"),
        ("dlnV/dlnR 15–27.5 kpc", ["P2_slope_15_27p5"], ["P2_slope_15_27p5"], ["P2_slope_15_27p5"], "{:+.3f}"),
        ("K_z(R0, 1.1)/2πG [M☉ pc⁻²]", ["P3", "Kz_R0_1p1_over_2piG"], ["P3", "Kz_R0_1p1_over_2piG"], ["P3", "Kz_R0_1p1_over_2piG"], "{:.1f}"),
        ("Σ(|z| < 1.1) true column [M☉ pc⁻²]", ["P3", "Sigma_tot_1p1_Msun_pc2"], ["P3", "Sigma_tot_1p1_Msun_pc2"], ["P3", "Sigma_tot_1p1_Msun_pc2"], "{:.1f}"),
        ("ρ_tot(R0, 0) Oort limit [M☉ pc⁻³]", ["P3", "rho_tot_R0_Msun_pc3"], ["P3", "rho_tot_R0_Msun_pc3"], ["P3", "rho_tot_R0_Msun_pc3"], "{:.3f}"),
        ("σ_z(R0≈8, 0), h = 0.30 kpc [km/s]", ["P4_sigma_z_kms", "h0.3", "R8"], ["P4_sigma_z_kms", "h0.3", "R8"], ["P4_sigma_z_kms", "h0.3", "R8"], "{:.1f}"),
        ("V_c(60 kpc), anticentre wedge / in-plane [km/s]", ["P5_Vc_anticentre_wedge", "R60"], ["P5_Vc", "R60"], ["P5_Vc", "R60"], "{:.1f}"),
        ("mean V_c 30–60 kpc [km/s]", ["P5_mean_30_60_wedge"], ["P5_mean_30_60"], ["P5_mean_30_60"], "{:.1f}")]
for foot in ("canonical", "alt"):
    for name, pv, pi, pn, f in rows:
        w(f"| {name} | {foot} | {fmt(band('v3', foot, pv), f)} | {fmt(band('v3_isolated', foot, pi), f)} | {fmt(band('NFW_Ou24', foot, pn), f)} |")
w("")
w("Local 'phantom' density at (R0, 0) (dynamical minus baryonic; what a DR4 Jeans analysis would call dark): "
  + "; ".join(f"{foot} {D['v3'][foot][c]['P3']['phantom_mid_GeV_cm3']:.2f} GeV cm⁻³ midplane, {D['v3'][foot][c]['P3']['phantom_shell_GeV_cm3']:.2f} shell average"
              for foot in ("canonical", "alt")) + f"; NFW {D['NFW_Ou24'][c]['P3']['dark_GeV_cm3']:.3f} GeV cm⁻³.")
w("")
w("## P6 (new, v3-specific): azimuthal asymmetry of the in-plane V_c from the external field")
w("")
w("A = 2(V_max − V_min)/(V_max + V_min) over galactocentric azimuth φ (φ measured from the Sun→GC direction toward l = 90°; the anticentre "
  "side is φ = 180°). Isolated v3 predicts A = 0. Rival: 0.")
w("")
w("| R [kpc] | " + " | ".join(f"A {foot}" for foot in ("canonical", "alt")) + " | φ(V_max), φ(V_min) canonical [deg] |")
w("|---|---|---|---|")
for r in ("R15", "R20", "R25", "R30", "R40", "R50", "R60"):
    a = [D["v3"][foot][c]["P6_asymmetry_A"][r] for foot in ("canonical", "alt")]
    w(f"| {r[1:]} | {a[0]:.3f} | {a[1]:.3f} | {D['v3']['canonical'][c]['P6_azimuth_Vmax_deg'][r]:.0f}, {D['v3']['canonical'][c]['P6_azimuth_Vmin_deg'][r]:.0f} |")
w("")
w("## P2 rotation curve, census (km/s; anticentre wedge for v3)")
w("")
w("| R | v3 can | v3 alt | v3 iso can | v3 iso alt | NFW |")
w("|---|---|---|---|---|---|")
for k in D["v3"]["canonical"][c]["P2_Vc_anticentre_wedge"]:
    w(f"| {k[1:]} | {D['v3']['canonical'][c]['P2_Vc_anticentre_wedge'][k]:.1f} | {D['v3']['alt'][c]['P2_Vc_anticentre_wedge'][k]:.1f} | "
      f"{D['v3_isolated']['canonical'][c]['P2_Vc'][k]:.1f} | {D['v3_isolated']['alt'][c]['P2_Vc'][k]:.1f} | {D['NFW_Ou24'][c]['P2_Vc'][k]:.1f} |")
w("")
w("## P1 K_z/(2πG) [M☉ pc⁻²], census, v3 (EFE; vertical quantities from the exact γ = 0 solve) / NFW")
w("")
w("| R | z 0.5 | z 1.1 | z 2.0 |")
w("|---|---|---|---|")
for k in D["v3"]["canonical"][c]["P1_Kz_over_2piG_Msun_pc2"]:
    v = D["v3"]["canonical"][c]["P1_Kz_over_2piG_Msun_pc2"][k]; vn = D["NFW_Ou24"][c]["P1_Kz_over_2piG_Msun_pc2"][k]
    va = D["v3"]["alt"][c]["P1_Kz_over_2piG_Msun_pc2"][k]
    w(f"| {k[1:]} | {v['z0.5']:.1f} / {va['z0.5']:.1f} / {vn['z0.5']:.1f} | {v['z1.1']:.1f} / {va['z1.1']:.1f} / {vn['z1.1']:.1f} | {v['z2.0']:.1f} / {va['z2.0']:.1f} / {vn['z2.0']:.1f} |")
w("(canonical / alt / NFW)")
w("")
w("## Required DR4 precision (CFG553 §4 rule; 3σ)")
w("")
for k, v in D["required_precision"].items():
    w(f"- {k}: F {v['F_central']:.4g} [{v['F_band'][0]:.4g}, {v['F_band'][1]:.4g}], R {v['R_central']:.4g} [{v['R_band'][0]:.4g}, {v['R_band'][1]:.4g}] → {v['required']}")
w("")
w("## Variants (census, EFE γ = 0; envelope only)")
w("")
for k, v in D["variants"].items():
    w(f"- {k}: V20 {v['V20_gamma0']:.1f} km/s, slope 15–27.5 {v['slope_15_27p5_gamma0']:+.3f}, K_z(R0,1.1)/2πG {v['Kz_R0_1p1_over_2piG']:.1f}, V60 {v['V60_gamma0']:.1f}")
open(os.path.join(HERE, "PREDICTIONS_V3.md"), "w").write("\n".join(L) + "\n")
print("PREDICTIONS_V3.md written from the sealed JSON", sha)
