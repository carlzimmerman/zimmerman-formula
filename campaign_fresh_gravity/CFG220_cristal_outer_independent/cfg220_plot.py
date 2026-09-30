#!/usr/bin/env python3
"""CFG220 figure: the six CRISTAL dust-detected discs at the table's outer radius, independent baryon route: the median delta of each law and its 95% bootstrap CI as a function of a
uniform gas-mass offset tau (dex) applied to all six discs (tau = 0 is the dust-based gas mass).  Drawn from the lane's own functions (cfg220_outer_independent.py exec'd read-only
through its definitions; nu_mono, canonical, table_Rout); the fit route's medians are marked at the left edge for reference.
Run: python3 campaign_fresh_gravity/CFG220_cristal_outer_independent/cfg220_plot.py -> cfg220_calibration_scan.png
"""
import os, io, contextlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LANE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(LANE, "cfg220_outer_independent.py")).read()
ns = {"__file__": os.path.join(LANE, "cfg220_outer_independent.py"), "__name__": "x"}
_e = os.environ.pop("MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ------------------------------------------------------------------------------------------------ controls")], "x", "exec"), ns)
rows_for, deltas, KER, DET, med_ci = ns["rows_for"], ns["deltas"], ns["KER"], ns["DET"], ns["med_ci"]
taus = np.round(np.arange(-1.0, 1.0001, 0.02), 2)
res = {law: np.array([med_ci(deltas(rows_for("table_Rout", DET, "ind", tau=float(t), mutate=False), law, "canonical", KER["nu_mono"])) for t in taus]) for law in ("flat", "rival")}
fit = {law: med_ci(deltas(rows_for("table_Rout", DET, "fit", mutate=False), law, "canonical", KER["nu_mono"])) for law in ("flat", "rival")}
fig, ax = plt.subplots(figsize=(11.5, 6.6))
ax.axvspan(-0.25, 0.25, color="0.92", zorder=0)
ax.text(0.0, 0.575, "±0.25 dex: the CFG219 baseline for one sigma\nof the shared gas calibration", ha="center", va="top", fontsize=8.5, color="0.4")
for law, col, lab in (("flat", "#1f6fd1", "flat law"), ("rival", "#d1541f", "rival a₀ ∝ E(z)")):
    ax.plot(taus, res[law][:, 0], color=col, lw=2.6, label=f"median δ, {lab}")
    ax.fill_between(taus, res[law][:, 1], res[law][:, 2], color=col, alpha=0.2, lw=0)
    ax.plot([-0.96], [fit[law][0]], marker="D", color=col, ms=8, mfc="white", mew=2, ls="none", clip_on=False)
ax.plot([], [], marker="D", color="0.3", mfc="white", mew=2, ls="none", label="fit route (authors' M_bary), same six discs (diamonds at the left)")
ax.axhline(0, color="0.15", lw=1.2)
ax.axvline(0, color="0.15", lw=1.0, ls="--")
ax.text(0.01, -0.62, "dust-based\ngas mass", fontsize=8.5, va="bottom")
# class windows read from the lane's frozen class rule
def cls(f, r):
    vf = "C" if f[1] <= 0 <= f[2] else ("O" if f[1] > 0 else "U"); vr = "C" if r[1] <= 0 <= r[2] else ("O" if r[1] > 0 else "U")
    return "FLAT-SUPPORTED" if (vf == "C" and vr == "U") else "RIVAL-SUPPORTED" if (vr == "C" and vf == "O") else "BOTH-CONSISTENT" if (vf == "C" and vr == "C") else "BOTH-DISFAVOURED" if (vf != "C" and vr != "C") else "OTHER"
cl = [cls(res["flat"][i], res["rival"][i]) for i in range(len(taus))]
COL = {"BOTH-CONSISTENT": "#cfd8dc", "FLAT-SUPPORTED": "#c8e6c9", "BOTH-DISFAVOURED": "#ffcdd2", "RIVAL-SUPPORTED": "#ffe0b2", "OTHER": "#eeeeee"}
i0 = 0
for i in range(1, len(taus) + 1):
    if i == len(taus) or cl[i] != cl[i0]:
        ax.axvspan(taus[i0] - 0.01, (taus[i - 1] + 0.01), ymin=0.0, ymax=0.045, color=COL[cl[i0]], zorder=1)
        ax.text((taus[i0] + taus[i - 1]) / 2, -0.685, cl[i0].replace("-", "\n", 1), ha="center", va="center", fontsize=7.6)
        i0 = i
ax.set_xlim(-1.0, 1.0); ax.set_ylim(-0.72, 0.6)
ax.set_xlabel("uniform gas-mass offset τ on all six discs (dex; +0.30 = gas masses ×2)")
ax.set_ylabel("median δ = log₁₀(D_obs / D_pred)")
ax.set_title("CRISTAL, table R_out, independent baryons (SED M★ + dust gas), six detected discs: the verdict is a statement about the gas calibration (CFG220)", fontsize=10.5)
ax.legend(fontsize=8.8, loc="lower left", bbox_to_anchor=(0.01, 0.075)); ax.grid(alpha=0.25)
fig.text(0.01, 0.008, "n = 6; the CI is a galaxy bootstrap (disc-to-disc scatter only). ν_mono, canonical footing. The rival's median stays below 0 at every τ (−0.09 even with no gas); the flat law's is 0 at τ = +0.33.\nAuthor decompositions, not a direct a₀ measurement; κ = ½ fitted.", fontsize=8, color="0.3")
plt.tight_layout(rect=(0, 0.05, 1, 1))
out = os.path.join(LANE, "cfg220_calibration_scan.png")
plt.savefig(out, dpi=150)
print("wrote", os.path.basename(out))
