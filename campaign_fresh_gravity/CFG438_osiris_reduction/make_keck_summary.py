#!/usr/bin/env python3
"""One-page summary figure of the CFG438 OSIRIS archival reduction (BX442), for an instrument scientist. Reads only committed CFG438 outputs."""
import os, json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt, matplotlib.image as mpimg
H = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(H, "cfg438_bx442_results.json"))); D = json.load(open(os.path.join(H, "cfg438_bx442_DIAG_postfreeze.json")))
fig = plt.figure(figsize=(16, 15), dpi=150); fig.patch.set_facecolor("white")
fig.text(0.03, 0.975, "Keck/OSIRIS archival re-reduction of Q2343-BX442 (z = 2.18) — official DRP v6 under GDL", fontsize=17, weight="bold")
fig.text(0.03, 0.955, "KOA lev0 data, programme 2011B (Law et al. 2012). Independent re-reduction for a validation test; not peer reviewed.", fontsize=11, color="#444")
ax = fig.add_axes([0.03, 0.64, 0.94, 0.275]); ax.imshow(mpimg.imread(os.path.join(H, "cfg438_bx442_DIAG_SN3_maps.png"))); ax.axis("off")
ax.set_title("Post-freeze diagnostic maps, all S/N ≥ 3 spaxels (PA fit 146° here; restricted to 1\" of the centre it is 173°, Law 168°): Hα flux, velocity, dispersion, major-axis profile", fontsize=11, loc="left")
s = np.loadtxt(os.path.join(H, "cfg438_bx442_DIAG_SN3_summed_spectrum.txt"))
a2 = fig.add_axes([0.05, 0.37, 0.40, 0.22]); a2.step(s[:, 0], s[:, 1], where="mid", color="#2a78d6", lw=1); a2.fill_between(s[:, 0], -s[:, 2], s[:, 2], color="#bbb", alpha=0.4, step="mid", label="1σ noise")
for lam, lab in ((6564.61, "Hα"), (6585.27, "[NII]"), (6549.86, "[NII]")):
    a2.axvline(lam * (1 + 2.1765), color="#d03b3b", ls=":", lw=1); a2.text(lam * (1 + 2.1765), a2.get_ylim()[1] * 0.92, lab, color="#d03b3b", fontsize=9, ha="center")
a2.set_xlabel("observed wavelength (Å)"); a2.set_ylabel("summed flux (DRP units)"); a2.set_title(f"Summed spectrum, S/N≥3 spaxels within 1\": S/N {D['D1_summed']['sn']:.1f}", fontsize=11, loc="left"); a2.legend(fontsize=8, loc="upper left")
oh = np.array(R["oh_lines"])
rows = [("Setup", "Kn2, 100 mas, LGS-AO; 40 × 900 s frames (2011-08-23/24), nod pairs; 52 in the paper"),
        ("Reduction", "Subtract frame → channel levels → crosstalk → glitch id → extract (recmat s100714 Kn2_100) → cube → dispersion → mosaic. Cosmic-ray module skipped (Keck advice)."),
        ("GDL port", "Backbone only: 5 compatibility patches (XML callbacks, BIN_DATE, object accessors, a minimal XML DOM). No science module changed."),
        ("Wavelengths", f"{len(oh)} OH lines: centroids within ~0.5 Å (≤10 km/s); instrumental σ ≈ {R['sigma_inst_kms']:.1f} km/s"),
        ("Frozen check vs Law+12", f"line found: FAIL ({R['n_pass']} spaxels at S/N≥5, needed 30; summed S/N {R['summed']['sn']:.1f})"),
        ("", f"kinematic PA: FAIL (203°, fit at bounds) · V_rot: not computable · σ_m: PASS ({R['sigma_m_flux_weighted']:.0f}±{R['sigma_m_err']:.0f} vs 66±6 km/s)"),
        ("Diagnostic (post-freeze)", f"S/N≥3 within 1\": PA {D['D2']['kin']['pa']}° (Law 168°), v {D['D2']['v_p5_p95'][0]:.0f} to +{D['D2']['v_p5_p95'][1]:.0f} km/s (Law ±150), σ_m {D['D2']['sigma_m']:.0f} km/s"),
        ("Open issues", "≈80–100 km/s blueshift vs z = 2.1765 (unresolved); 12 frames missing; no telluric/flux calibration; WCS handedness not independently checked"),
        ("A1689B11 (z = 2.54)", "Kn5 50 mas, 8 object + 5 sky frames (recmat s170529 Kn5_050): no credible detection in the image-plane cube")]
a3 = fig.add_axes([0.05, 0.01, 0.92, 0.26]); a3.axis("off"); y = 0.97
for k, v in rows:
    a3.text(0.0, y, k, fontsize=10.5, weight="bold", va="top"); a3.text(0.20, y, v, fontsize=10, va="top", wrap=True); y -= 0.112 if len(v) > 95 else 0.085
fig.text(0.03, 0.941, "1 · Data quality: is the reduction trustworthy?", fontsize=12.5, weight="bold", color="#2a78d6")
fig.text(0.55, 0.615, "2 · What it means for the framework (a0 at z = 2.18)", fontsize=12.5, weight="bold", color="#2a78d6")
# ---- framework panel: implied a0 for BX442 from the published numbers (CFG437), flat vs a0 ~ H(z)
c = json.load(open(os.path.join(H, "..", "CFG437_bx442_published", "cfg437_results.json")))
a4 = fig.add_axes([0.55, 0.37, 0.42, 0.22]); a4.set_xscale("log")
for lo, hi, col, lab in ((9.36e-11, 1.13e-10, "#1baf7a", "Flat a0 (this framework)"), (9.36e-11 * 3.29, 1.13e-10 * 3.29, "#eda100", "Rival a0 ∝ H(z), z = 2.18")):
    a4.axvspan(lo, hi, color=col, alpha=0.3, label=lab)
for yy, key, col, lab in ((1.0, "A V_c=V_rot", "#2a78d6", "A: rotation only (as in Law+12 M_dyn)"), (0.0, "B asym-drift", "#eb6834", "B: + 71 km/s gas motions as support")):
    r = c[key]; a4.errorbar(r["med"], yy, xerr=[[r["med"] - r["lo"]], [r["hi"] - r["med"]]], fmt="o", color=col, capsize=4, lw=2)
    a4.text(r["lo"], yy + 0.22, lab, color=col, fontsize=9.5)
a4.set_ylim(-0.5, 1.9); a4.set_yticks([]); a4.set_xlim(3e-11, 1e-9); a4.set_xlabel("implied a0 (m/s²), 16–84% range")
a4.set_title("Framework test from published numbers (CFG437): NOT DIAGNOSTIC", fontsize=11, loc="left"); a4.legend(fontsize=8.5, loc="upper right")
fig.text(0.55, 0.305, "Law g = g_N ν(g_N/a0), ν = 1/(1−e^−√y). Inputs: M* 6e10, M_gas 2e10 Msun (SF-law inversion),\nV_rot 234 km/s at 8 kpc (Law+12). The gas-motion choice spans both predictions; one galaxy cannot decide.", fontsize=9, color="#444")
out = os.path.abspath(os.path.join(H, "..", "..", "explainers", "img", "keck_osiris_bx442_summary.png"))
fig.savefig(out, facecolor="white"); print(out)
