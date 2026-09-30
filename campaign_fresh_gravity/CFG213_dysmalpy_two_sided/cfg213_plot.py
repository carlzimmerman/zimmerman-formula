#!/usr/bin/env python3
"""CFG213 figure: the z ~ 5 (ALMA-CRISTAL) mass discrepancy against the flat-a0 prediction and the rival a0 ~ H(z).
Reads the lane's own inputs through cfg213_two_sided.py (exec'd read-only up to its bins, MUTATE off); draws nothing new.
Left: D = g_obs/g_bar at R_e,disk against g_bar/a0 (canonical footing, nu_mono), fit route (filled) and SED + dust-gas
route (open), with the two laws' curves.  Right: the median log(D_obs/D_pred) with 95% bootstrap CIs, per law and variant.
Run: python3 campaign_fresh_gravity/CFG213_dysmalpy_two_sided/cfg213_plot.py  ->  cfg213_z5_predictions_vs_results.png
"""
import os, sys, io, math, contextlib
sys.dont_write_bytecode = True
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LANE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(LANE, "cfg213_two_sided.py")).read()
ns = {"__file__": os.path.join(LANE, "cfg213_two_sided.py"), "__name__": "cfg213"}
_e = os.environ.pop("MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("BINS = {")], "cfg213", "exec"), ns)
if _e is not None:
    os.environ["MUTATE"] = _e
galaxy_rows, deltas, K, A0F, E, med_ci, cr, EXCL, KER = (ns[k] for k in ("galaxy_rows", "deltas", "K", "A0F", "E", "med_ci", "cr",
                                                                           "EXCL", "KER"))
A0 = A0F["canonical"]
nu = K.nu_mono
prim = [g for g in cr if g["id"] not in EXCL]
fit = galaxy_rows("Z5", prim)
route = {r["id"]: r for r in galaxy_rows("Z5", prim, route=True)}
excl = galaxy_rows("Z5", [g for g in cr if g["id"] in EXCL])
cls = {g["id"]: g["cls"] for g in cr}

fig, (ax, bx) = plt.subplots(1, 2, figsize=(14.5, 6.4), gridspec_kw=dict(width_ratios=[1.35, 1]))
x = np.geomspace(0.5, 40, 400)
ax.plot(x, [float(nu(np.array([v]))[0]) for v in x], color="#1f6fd1", lw=2.6, label="flat a₀ (the framework's prediction)")
zlo, zhi = min(r["z"] for r in fit), max(r["z"] for r in fit)
lo = [float(nu(np.array([v / E(zlo)]))[0]) for v in x]
hi = [float(nu(np.array([v / E(zhi)]))[0]) for v in x]
ax.fill_between(x, lo, hi, color="#d1541f", alpha=0.18, lw=0)
ax.plot(x, [float(nu(np.array([v / E(5.0)]))[0]) for v in x], color="#d1541f", lw=2.2, ls="--",
        label=f"rival a₀ ∝ H(z) (×{E(5.0):.1f} at z = 5; band z {zlo:.2f}–{zhi:.2f})")
ax.axhline(1.0, color="0.45", lw=1, ls=":", label="Newton, no extra mass (D = 1)")
for r in fit:
    xb, D = r["gbar"] / A0, r["D"]
    c = "#111111" if cls[r["id"]] == "Best Disk" else "#6a3d9a"
    ax.scatter([xb], [D], s=70, color=c, zorder=5, edgecolor="white", lw=0.8)
    ax.annotate(r["id"], (xb, D), textcoords="offset points", xytext=(6, 5), fontsize=9, color=c)
    if r["id"] in route:
        rr = route[r["id"]]
        ax.plot([xb, rr["gbar"] / A0], [D, rr["D"]], color="0.55", lw=0.9, zorder=3)
        ax.scatter([rr["gbar"] / A0], [rr["D"]], s=62, facecolor="none", edgecolor=c, lw=1.4, zorder=4)
for r in excl:
    ax.scatter([r["gbar"] / A0], [r["D"]], marker="x", s=55, color="0.6", zorder=4)
    ax.annotate(r["id"] + "×", (r["gbar"] / A0, r["D"]), textcoords="offset points", xytext=(4, 6), fontsize=7.5, color="0.5")
ax.scatter([], [], s=70, color="#111111", label="CRISTAL Best Disk, authors' fit (filled)")
ax.scatter([], [], s=70, color="#6a3d9a", label="CRISTAL Disk, authors' fit (filled)")
ax.scatter([], [], s=62, facecolor="none", edgecolor="0.3", label="same disc with SED M★ + dust gas (open)")
ax.scatter([], [], marker="x", s=55, color="0.6", label="09, 15: excluded (curve ≠ table)")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(0.5, 40); ax.set_ylim(0.3, 9)
ax.set_yticks([0.5, 1, 1.5, 2, 3, 5, 8]); ax.set_yticklabels(["0.5", "1", "1.5", "2", "3", "5", "8"])
ax.set_xlabel("baryonic acceleration at R_e,disk,  g_bar / a₀   (a₀ = 9.36×10⁻¹¹ m s⁻², canonical)", fontsize=10.5)
ax.set_ylabel("mass discrepancy  D = g_obs / g_bar = 1/(1 − f_DM)", fontsize=10.5)
ax.set_title("z ≈ 4.4–5.7 (ALMA-CRISTAL): your flat-a₀ prediction (blue) vs the rival (orange) vs the discs", fontsize=11.5)
ax.text(0.02, 0.03, "authors' fits (filled): rival predicts too much hidden mass\n  (median −0.16 dex, 95% CI excludes 0); flat +0.05 (borderline)\n"
        "SED M★ + dust gas (open): both consistent; 23b drops below D = 1\n  (SED + gas baryons exceed the fitted total)", transform=ax.transAxes,
        fontsize=8.4, va="bottom", bbox=dict(boxstyle="round", fc="white", ec="0.7", alpha=0.93))
ax.legend(fontsize=8.6, loc="upper right", framealpha=0.92)
ax.grid(alpha=0.25, which="both")

# right: median log(D_obs/D_pred) with 95% CIs
cells = []
for law, colr in (("flat", "#1f6fd1"), ("rival", "#d1541f")):
    for kname in ("nu_mono", "P2"):
        for foot in ("canonical", "alt"):
            for alpha in (3.36, 1.68):
                rows = galaxy_rows("Z5", prim, alpha=alpha)
                m, l, h = med_ci(deltas(rows, law, foot, KER[kname]), ("plot", law, kname, foot, alpha))
                cells.append((f"{law} · {kname} · {foot[:5]} · α{alpha}", m, l, h, colr, False))
    rows = galaxy_rows("Z5", prim, route=True)
    m, l, h = med_ci(deltas(rows, law, "canonical", K.nu_mono), ("plot", law, "route"))
    cells.append((f"{law} · SED+gas route (n=9) · ν_mono · canon.", m, l, h, colr, True))
ys = np.arange(len(cells))[::-1]
for yv, (lab, m, l, h, colr, is_route) in zip(ys, cells):
    bx.plot([l, h], [yv, yv], color=colr, lw=2.2, alpha=0.55 if is_route else 1)
    bx.scatter([m], [yv], color=colr, s=36, zorder=3, facecolor="white" if is_route else colr, edgecolor=colr, lw=1.5)
bx.axvline(0, color="0.2", lw=1)
bx.set_yticks(ys); bx.set_yticklabels([c[0] for c in cells], fontsize=8)
bx.set_xlabel("median log₁₀(D_measured / D_predicted), 95% CI\n< 0: law predicts too much hidden mass;  > 0: too little", fontsize=9.5)
bx.set_title("verdicts per variant (0 inside the bar = consistent)", fontsize=11)
bx.grid(alpha=0.25, axis="x")
fig.text(0.01, 0.008, "CFG213 (committed). The discs' baryonic masses come from the authors' DysmalPy fits (prior 1 dex wide), so the verdict is ROUTE-DEPENDENT:\n"
         "with SED + dust-gas masses both laws are consistent.  κ = ½ fitted.  Not a claim that the data favour the framework.",
         fontsize=8.3, color="0.3")
plt.tight_layout(rect=(0, 0.05, 1, 1))
out = os.path.join(LANE, "cfg213_z5_predictions_vs_results.png")
plt.savefig(out, dpi=150)
print("wrote", os.path.basename(out))
