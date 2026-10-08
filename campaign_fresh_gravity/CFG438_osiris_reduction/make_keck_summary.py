#!/usr/bin/env python3
"""One-page summary figure of the CFG438 OSIRIS archival reduction (BX442), for an instrument scientist. Reads only committed CFG438 outputs."""
import os, json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt, matplotlib.image as mpimg
H = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(H, "cfg438_bx442_results.json"))); D = json.load(open(os.path.join(H, "cfg438_bx442_DIAG_postfreeze.json")))
fig = plt.figure(figsize=(16, 10.5), dpi=150); fig.patch.set_facecolor("white")
fig.text(0.03, 0.965, "Keck/OSIRIS archival re-reduction of Q2343-BX442 (z = 2.18) — official DRP v6 under GDL", fontsize=17, weight="bold")
fig.text(0.03, 0.937, "KOA lev0 data, programme 2011B (Law et al. 2012). Independent re-reduction for a validation test; not peer reviewed.", fontsize=11, color="#444")
ax = fig.add_axes([0.03, 0.50, 0.94, 0.41]); ax.imshow(mpimg.imread(os.path.join(H, "cfg438_bx442_DIAG_SN3_maps.png"))); ax.axis("off")
ax.set_title("Post-freeze diagnostic maps, all S/N ≥ 3 spaxels (PA fit 146° here; restricted to 1\" of the centre it is 173°, Law 168°): Hα flux, velocity, dispersion, major-axis profile", fontsize=11, loc="left")
s = np.loadtxt(os.path.join(H, "cfg438_bx442_DIAG_SN3_summed_spectrum.txt"))
a2 = fig.add_axes([0.05, 0.08, 0.36, 0.34]); a2.step(s[:, 0], s[:, 1], where="mid", color="#2a78d6", lw=1); a2.fill_between(s[:, 0], -s[:, 2], s[:, 2], color="#bbb", alpha=0.4, step="mid", label="1σ noise")
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
a3 = fig.add_axes([0.45, 0.06, 0.52, 0.38]); a3.axis("off"); y = 0.97
for k, v in rows:
    a3.text(0.0, y, k, fontsize=10.5, weight="bold", va="top"); a3.text(0.27, y, v, fontsize=10, va="top", wrap=True); y -= 0.112 if len(v) > 95 else 0.085
out = os.path.abspath(os.path.join(H, "..", "..", "explainers", "img", "keck_osiris_bx442_summary.png"))
fig.savefig(out, facecolor="white"); print(out)
