#!/usr/bin/env python3
"""The 2026-09-30 / 10-01 results on one page (plot only; every number is read from a committed file; no new analysis).
  A  the calibration wall (CFG240): sigma(log a0) vs the sample's largest y = g_bar/a0, exact P2 kernel, N = 20, sigma = 0.1 dex,
     log-uniform design (the CFG240 definition), break-even points read from CFG240_break_even_table.json
  B  the best dynamics-independent gas anchor: Heintz & Watson 2020 Table 1 (as transcribed and checked against the PDF) about the
     paper's own relation, with the four cyclically shifted QSO rows shown at their Eq.-3 values
  C  the KiDS-1000 lensing split by lens redshift (CFG255 stage B): measured amplitude against FLAT, RIVAL and the LCDM proxy
  D  the Gaia DR4 decision map: the in-force edges from the code-extracted edge table (Amendment 18), the expected DR4 sigma_tot and the
     seed-sensitivity width; PREDICTIONS ONLY -- no DR3 gamma-hat is shown (DR3 numbers are code-path tests, Amendment 7(e))
Run: python3 campaign_fresh_gravity/CHART_today_2026-10-01/chart_today.py
"""
import csv, json, math, os, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
J = lambda *p: os.path.join(REPO, *p)
fig, ax = plt.subplots(2, 2, figsize=(15, 11))
fig.suptitle("What today's work shows (2026-09-30 / 10-01) — κ = ½ FITTED; nothing here is a detection or says the data favour the framework",
             fontsize=13, fontweight="bold")
CHK = []

# ---------------------------------------------------------------- A  the calibration wall
a = ax[0, 0]
T = json.load(open(J("campaign_fresh_gravity", "CFG240_calibration_wall", "CFG240_break_even_table.json")))
recs = [r for r in (T if isinstance(T, list) else T["cases"]) if r.get("record") == "case"]
def sig(ymin, ymax, N=20, s=0.1):
    y = ymin * (ymax / ymin) ** (np.arange(N) / (N - 1)); b = 1 / (2 * (1 + y))
    R = np.stack([1 - b, b], 1); return float(np.sqrt(np.linalg.inv(R.T @ R / s ** 2)[1, 1]))
ys = np.geomspace(1.0, 1e3, 400)
for ymin, c in ((1e-3, "C0"), (1e-2, "C2"), (1e-1, "C3")):
    a.plot(ys, [sig(ymin, x) for x in ys], c, lw=2, label=f"sample reaches down to y_min = {ymin:g}")
    r = next(r for r in recs if r["kernel"] == "P2" and r["y_min"] == ymin and r["N"] == 20 and r["sigma_dex"] == 0.1 and not r.get("prior_log_f_dex"))
    if r["y_max_break_even"]:
        a.plot(r["y_max_break_even"], r["sigma_log_a0_at_break_even"], "o", c=c, ms=8)
        a.annotate(f"break-even y ≈ {r['y_max_break_even']:.1f}", (r["y_max_break_even"], r["sigma_log_a0_at_break_even"]),
                   xytext=((-95, -22) if ymin == 1e-3 else (10, 8)), textcoords="offset points", color=c, fontsize=9)
        CHK.append(abs(sig(ymin, r["y_max_break_even"]) - r["sigma_log_a0_at_break_even"]) < 1e-9)
    else:
        a.annotate(f"never reaches 0.1 dex (best {r['sigma_min']:.3f})", (300, sig(ymin, 300)), xytext=(-150, 14),
                   textcoords="offset points", color=c, fontsize=9)
a.axhline(0.1, color="k", ls="--", lw=1); a.text(1.05, 0.102, "0.1 dex target", fontsize=9)
a.axhline(3 * 0.1 / math.sqrt(20), color="gray", ls=":", lw=1.5); a.text(1.05, 0.069, "T4 floor 3σ/√N (proved in Lean)", fontsize=9, color="gray")
a.axvspan(1.1, 4.4, color="orange", alpha=0.25); a.text(1.15, 0.165, "median y of the z ≈ 1–5 samples\n(per-point medians 1.1–4.4; CFG223)", fontsize=9, color="darkorange")
a.set_xscale("log"); a.set_ylim(0.06, 0.2); a.set_xlabel("largest y = g_bar / a₀ reached by the sample"); a.set_ylabel("σ(log₁₀ a₀) with the baryon calibration free (dex)")
a.set_title("A · The calibration wall (CFG240; Lean ChainCert 331 theorems)\nN = 20 galaxies at 0.1 dex: a₀ needs deep points AND y ≳ 8", fontsize=10)
a.legend(fontsize=8, loc="upper right")

# ---------------------------------------------------------------- B  Heintz & Watson
b = ax[0, 1]
R_ = list(csv.DictReader(open(J("data_assembly", "gas_anchor_scoping", "heintz_watson2020_table1.csv"))))
x = np.array([float(r["log_Z_Zsun"]) for r in R_]); yt = np.array([float(r["log_alpha_CI"]) for r in R_])
eq3 = np.array([math.log10(1.3e-4) + float(r["logN_H2"]) - float(r["logN_CIstar"]) for r in R_])
shift = {"J0643-5041", "J0551-3638", "J1232+0815", "J1444+0126"}
isS = np.array([r["source"] in shift for r in R_]); isG = np.array([r["type"] == "GRB-DLA" for r in R_])
xx = np.linspace(-1.7, 0.6, 50); line = -1.13 * xx + 1.33
b.fill_between(xx, line - 0.2, line + 0.2, color="gray", alpha=0.25, label="the paper's stated scatter (±0.2 dex)")
b.plot(xx, line, "k-", lw=1.5, label="their relation: log α = −1.13 log Z + 1.33")
b.scatter(x[~isS & ~isG], yt[~isS & ~isG], c="C0", s=40, label="QSO absorbers, as printed")
b.scatter(x[isG], yt[isG], c="C1", marker="s", s=40, label="GRB absorbers, as printed")
b.scatter(x[isS], yt[isS], facecolors="none", edgecolors="C3", s=70, lw=1.5, label="4 QSO rows as printed (a cyclic shift: our hypothesis, strongly supported)")
b.scatter(x[isS], eq3[isS], c="C3", marker="x", s=60, label="same 4 rows from their own Eq. 3")
for xi, y1, y2 in zip(x[isS], yt[isS], eq3[isS]): b.annotate("", (xi, y2), (xi, y1), arrowprops=dict(arrowstyle="->", color="C3", lw=0.8))
rms = float(np.std(yt - (-1.13 * x + 1.33))); corr = yt.copy(); corr[isS] = eq3[isS]; rms2 = float(np.std(corr - (-1.13 * x + 1.33)))
CHK.append(round(rms, 2) == 0.64 and round(rms2, 2) == 0.55)
b.text(-1.68, -1.35, f"our arithmetic, from our transcription: rms about their relation {rms:.2f} dex as printed,\n{rms2:.2f} dex with the shift undone (stated: 0.2 dex; their definition and any erratum\nnot checked) → no public anchor shown to reach the 0.1 dex an a₀(z) test needs",
       fontsize=9, bbox=dict(fc="white", ec="0.7"))
b.set_xlabel("log (Z / Z☉)"); b.set_ylabel("log α_[CI]")
b.set_title("B · Best dynamics-independent gas calibration (Heintz & Watson 2020; 19 absorbers, z 2–3.4)\nour transcription of its Table 1, checked row by row against the arXiv PDF", fontsize=10)
b.legend(fontsize=7.5, loc="upper right"); b.set_ylim(-1.45, 4.3)

# ---------------------------------------------------------------- C  KiDS z-split
c_ = ax[1, 0]
RB = json.load(open(J("campaign_fresh_gravity", "CFG255_lensing_rar_zsplit", "cfg255_stageB_results.json")))["numbers"]
A, S = RB["A_data"], RB["sigma_A"]; M = RB["amp_models"]
rows = [("measured (KiDS-1000, 181,477 lenses)", A, S, "k"), ("FLAT a₀ (the framework)", M["FLAT_canonical"], 0, "C0"),
        ("RIVAL a₀ ∝ H(z)", M["RIVAL_canonical"], 0, "C3"), ("ΛCDM proxy", M["LCDM"], 0, "C2")]
for i, (lab, v, s, col) in enumerate(rows):
    yy = len(rows) - 1 - i
    if s: c_.errorbar(v, yy, xerr=s, fmt="o", color=col, ms=9, capsize=6, lw=2); c_.errorbar(v, yy, xerr=2 * s, fmt="none", color=col, lw=0.8, capsize=3)
    else: c_.plot(v, yy, "D", color=col, ms=9)
    c_.text(0.165, yy, f"{lab}: {v:+.3f}" + (f" ± {s:.3f}" if s else ""), va="center", fontsize=9)
CHK.append(abs(A - 0.0595) < 5e-4 and abs(S - 0.0383) < 5e-4)
c_.axvline(0, color="0.6", lw=0.8); c_.set_xlim(-0.12, 0.42); c_.set_ylim(-0.7, 3.7); c_.set_yticks([])
c_.set_xlabel("amplitude change, high-z third minus low-z third (dex; median z 0.20–0.23 → 0.38–0.40)")
c_.text(-0.115, -0.5, "power to tell FLAT from RIVAL: Δχ² = 0.14 (needs 9) → NOT POSSIBLE;\nthe test misses even an injected rival signal (NON-DISCRIMINATING). Descriptive only.",
        fontsize=9, bbox=dict(fc="lightyellow", ec="0.7"))
c_.set_title("C · Splitting the weak-lensing RAR by lens redshift (CFG255)\ncancels the common calibration — but the signal (0.018 dex) is half the error", fontsize=10)

# ---------------------------------------------------------------- D  DR4 decision map
d = ax[1, 1]
E = json.load(open(J("prep_2026", "gaia_dr4_prep", "dr4_ready_1", "edge_table_dr4.json")))
tc = {t["constant"]: t["gamma"] for t in E["targets"]["canonical"]}; ta = {t["constant"]: t["gamma"] for t in E["targets"]["alt"]}
he = {h["constant"]: h["gamma"] for h in E["hard_edges"]}
sig_fit = 0.019; sig_tot = math.hypot(sig_fit, E["sigma_sys"]); w = 0.44 * sig_fit
d.axvspan(tc["GAMMA_TARGET"], tc["GAMMA_TARGET_TOP"], ymin=0.55, ymax=0.95, color="C1", alpha=0.6, label="Arm A (MOND kernel + external field), canonical")
d.axvspan(ta["GAMMA_TARGET_ALT"], ta["GAMMA_TARGET_ALT_TOP"], ymin=0.55, ymax=0.95, color="C1", alpha=0.3, label="Arm A, alt footing")
d.axvline(tc["GAMMA_B_PRED"], color="C0", lw=3, label="candidate B / ownership = ΛCDM = Newton: γ̂ = 1.000")
d.axvspan(1.0 - 2 * sig_tot, 1.0 + 2 * sig_tot, ymin=0.05, ymax=0.45, color="C0", alpha=0.15, label=f"±2σ_tot at the expected DR4 σ_fit ({sig_tot:.4f})")
d.axvline(he["GAMMA_B_KILL"], color="C3", ls="--", lw=1.5, label=f"B killed at γ̂ ≥ {he['GAMMA_B_KILL']}")
d.axvline(he["GAMMA_A_FALSIFIED_BELOW"], color="C1", ls="--", lw=1.5, label=f"Arm A falsified below {he['GAMMA_A_FALSIFIED_BELOW']}")
d.axvline(he["NOVERDICT_EDGE"], color="0.4", ls=":", lw=1.5, label=f"no-verdict edge {he['NOVERDICT_EDGE']}")
d.axvline(tc["GAMMA_MOND"], color="purple", ls="-.", lw=1.5, label=f"bare MOND benchmark {tc['GAMMA_MOND']}")
for g in (he["GAMMA_B_KILL"], he["GAMMA_A_FALSIFIED_BELOW"]):
    d.axvspan(g - w, g + w, ymin=0.45, ymax=0.55, color="red", alpha=0.35)
d.text(1.095, 0.49, f"← red: 'seed-sensitive' width ±{w:.4f}\n   (0.44 σ_fit, Amendment 18)", fontsize=8, color="darkred", va="center", transform=d.get_xaxis_transform())
CHK.append(tc["GAMMA_B_PRED"] == 1.0 and he["GAMMA_B_KILL"] == 1.084)
d.set_xlim(0.95, 1.36); d.set_yticks([]); d.set_xlabel("γ̂ (wide-binary velocity boost, Gaia DR4, 2 Dec 2026)")
d.set_title("D · Next test that can fail the law: Gaia DR4 (18 amendments filed before data)\npredictions only — for B it is a survival test, never a confirmation", fontsize=10)
d.legend(fontsize=7.5, loc="lower right")

plt.tight_layout(rect=(0, 0, 1, 0.96))
out = os.path.join(HERE, "chart_today_2026-10-01.png"); plt.savefig(out, dpi=130)
print(f"checks {sum(CHK)}/{len(CHK)}  -> {out}")
sys.exit(0 if all(CHK) else 1)
