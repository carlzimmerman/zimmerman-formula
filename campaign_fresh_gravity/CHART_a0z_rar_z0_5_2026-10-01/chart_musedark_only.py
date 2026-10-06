#!/usr/bin/env python3
"""MUSE-DARK-only a0(z) chart (plot only; every point restates a committed lane).
  route (i)  halo-fitted DC14 masses (a LCDM-model input): CFG262 reading bD (fb24a5922)
  route (ii) SED stars + H2, native; route (iii) SED stars, native: CFG303 noHI primary, reading bD (2d9bdc1b9)
  paper's own fit (MUSE-DARK III, A&A 709 L16): a0(z) = a0(0) + a1 z with a0(0) = 1.0, a1 = 1.59 (1e-10 m s^-2), as read in CFG356
  lines: flat a0 at both footings; the rival a0 proportional to H(z) (Omega_m = 0.315); SPARC 1.2.
kappa = 1/2 fitted.  Routes are never pooled."""
import os, csv, json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.dirname(HERE)
A0, ALT = 9.3603e-11, 1.1312e-10
U = A0 / 1e-10
M262 = [r for r in csv.DictReader(open(os.path.join(CFG, "CFG262_musedark_zthirds_by_route", "cfg262_points_stageB.csv"))) if r["reading"] == "bD"]
M303 = json.load(open(os.path.join(CFG, "CFG303_lcdm_free_inputs", "cfg303_musedark_LCDMFREE_results.json")))
M303 = M303.get("numbers", M303)["rows"]
assert sorted(round(float(r["s_star"]), 2) for r in M262 if r["route"] == "i") == [1.22, 3.05, 4.53]
assert [round(M303[f"noHI (primary)|z{i}-routeiii-bD"]["s"], 2) for i in (1, 2, 3)] == [1.21, 2.11, 0.66]

fig, ax = plt.subplots(figsize=(10, 6.4), dpi=160)
fig.patch.set_facecolor("#fbfbfa"); ax.set_facecolor("#fbfbfa")
z = np.linspace(0, 1.6, 200)
E = np.sqrt(0.315 * (1 + z) ** 3 + 0.685)
ax.fill_between(z, A0 / 1e-10, ALT / 1e-10, color="#2f8f5b", alpha=0.18, lw=0)
ax.plot(z, np.full_like(z, A0 / 1e-10), color="#2f8f5b", lw=2, label="your law: flat a$_0$ (canonical 0.94 / alt 1.13)")
ax.plot(z, np.full_like(z, ALT / 1e-10), color="#2f8f5b", lw=1.2, ls="--")
ax.plot(z, A0 / 1e-10 * E, color="#c4452f", lw=1.8, ls="-.", label="rival: a$_0$ ∝ H(z)")
ax.plot(z, 1.0 + 1.59 * z, color="#555", lw=1.6, ls=":", label="paper's own fit: 1.0 + 1.59 z (halo-fit masses)")
ax.axhline(1.2, color="#999", lw=0.8, ls=(0, (2, 3)))
ax.text(1.58, 1.24, "SPARC 1.2", color="#777", fontsize=8.5, ha="right")
C = "#b0548f"
r1 = sorted([r for r in M262 if r["route"] == "i"], key=lambda r: float(r["z"]))
x = [float(r["z"]) - 0.03 for r in r1]; y = [float(r["s_star"]) * U for r in r1]
ax.plot(x, y, color=C, lw=1, alpha=0.45)
for r, xx, yy in zip(r1, x, y):
    ax.plot([xx, xx], [float(r["stat68_lo"]) * U, float(r["stat68_hi"]) * U], color=C, lw=2.6, alpha=0.45)
ax.scatter(x, y, marker="^", s=60, color=C, alpha=0.45, label="(i) halo-fitted masses (ΛCDM-model input)", zorder=5)
for rt, mk, fc, dx, lab in (("ii", "s", "white", 0.0, "(ii) starlight + molecular gas (native)"),
                            ("iii", "D", "#e3b3d1", 0.03, "(iii) starlight only (native)")):
    rows = [M303[f"noHI (primary)|z{i}-route{rt}-bD"] for i in (1, 2, 3)]
    ok = [r for r in rows if not r["no_root"]]; nr = [r for r in rows if r["no_root"]]
    xs = [r["z"] + dx for r in ok]; ys = [r["s"] * U for r in ok]
    ax.plot(xs, ys, color=C, lw=1.1, ls=(0, (4, 2)) if rt == "ii" else (0, (1, 1.6)))
    for r, xx in zip(ok, xs):
        ax.plot([xx, xx], [max(10 ** r["itv"]["lo68"] * U, 0.13), 10 ** r["itv"]["hi68"] * U], color=C, lw=2.6)
    ax.scatter(xs, ys, marker=mk, s=60, facecolor=fc, edgecolor=C, linewidth=1.5, label=lab, zorder=6)
    for r in nr:
        ax.annotate("", xy=(r["z"] + dx, 0.13), xytext=(r["z"] + dx, 0.2), arrowprops=dict(arrowstyle="-|>", color=C, lw=1.6))
        ax.text(r["z"] + dx + 0.02, 0.17, "no a$_0$: visible mass\nalready exceeds the rotation", fontsize=7.5, color=C, va="center")
ax.set_yscale("log"); ax.set_ylim(0.12, 8); ax.set_xlim(0, 1.6)
ax.set_yticks([0.2, 0.3, 0.5, 1, 2, 3, 5]); ax.set_yticklabels(["0.2", "0.3", "0.5", "1", "2", "3", "5"])
ax.set_xlabel("redshift z"); ax.set_ylabel("implied a$_0$  [10$^{-10}$ m s$^{-2}$]")
ax.set_title("MUSE-DARK only: the a$_0$ rise depends on how the galaxies are weighed", fontsize=12.5, fontweight="bold", loc="left")
ax.legend(fontsize=8.6, loc="upper left", frameon=False)
fig.text(0.01, 0.035, "Points: redshift thirds of the 79-galaxy MUSE-DARK III sample, 68% intervals; routes never pooled. (i) CFG262; (ii)/(iii) CFG303 native inputs; paper fit as read in CFG356.", fontsize=7.4, color="#555")
fig.text(0.01, 0.01, "MUSE-DARK II finds no baryonic Tully-Fisher evolution (0.00 ± 0.06 dex). κ = ½ fitted.", fontsize=7.4, color="#555")
fig.tight_layout(rect=(0, 0.06, 1, 1))
out = os.path.join(HERE, "chart_musedark_only.png"); fig.savefig(out, facecolor=fig.get_facecolor())
print("wrote", os.path.basename(out))
