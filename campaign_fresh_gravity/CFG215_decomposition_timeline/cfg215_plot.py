#!/usr/bin/env python3
"""CFG215 figure: the decomposition delta(z) timeline.  Reads the lane's own pipeline through cfg215_timeline.py (exec'd read-only up to
its route-mixing mock; MUTATE off); nothing new is scored.  Solid = primary series (anchored / independent routes), open + dashed = fit-route
series (never pooled with the primary).  Dotted markers: where each law's delta would land if the OTHER law were exactly true.
Run: python3 campaign_fresh_gravity/CFG215_decomposition_timeline/cfg215_plot.py  ->  cfg215_delta_vs_z.png
"""
import os, sys, io, math, contextlib
sys.dont_write_bytecode = True
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LANE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(LANE, "cfg215_timeline.py")
src = open(path).read()
ns = {"__file__": path, "__name__": "cfg215"}
_e = os.environ.pop("MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index('R.banner("ROUTE-MIXING MOCK')], "cfg215", "exec"), ns)
if _e is not None:
    os.environ["MUTATE"] = _e
SERIES, TABLE, K, A0F, E, nu1, deltas_rows, gbar_of_gobs, LAWS = (ns[k] for k in ("SERIES", "TABLE", "K", "A0F", "E", "nu1", "deltas_rows",
                                                                                   "gbar_of_gobs", "LAWS"))
COL = {"flat": "#1f6fd1", "rival": "#d1541f"}
fig, ax = plt.subplots(figsize=(11.5, 6.6))
ax.axhline(0, color="0.15", lw=1.2)
ax.text(0.57, 0.012, "0 = the law is right", fontsize=8.5, ha="left", color="0.3")


def where_if_true(rows, truth):
    """median delta_flat / delta_rival per sample if `truth` were exactly right (g_obs held fixed, baryons from that law's inversion)"""
    out = {"flat": [], "rival": []}
    for r in rows:
        gobs = r["D"] * r["gbar"]
        a0t = A0F["canonical"] * (E(r["z"]) if truth == "rival" else 1.0)
        gt = gbar_of_gobs(gobs, a0t, K.nu_mono)
        for law in LAWS:
            a0 = A0F["canonical"] * (E(r["z"]) if law == "rival" else 1.0)
            out[law].append(math.log10((gobs / gt) / nu1(K.nu_mono, gt / a0)))
    return {k: float(np.median(v)) for k, v in out.items()}


zs = {}
for sname, style in (("primary", dict(ls="-", fill=True)), ("fit-route", dict(ls="--", fill=False))):
    for law in LAWS:
        xs, ys, lo, hi = [], [], [], []
        for smp, rows in SERIES[sname].items():
            if sname == "fit-route" and smp.startswith("RC41"):
                continue                                   # RC41's primary IS its anchored fit: drawn once, in the primary series
            t = TABLE[(sname, smp, law, "nu_mono", "canonical")]
            zmed = float(np.median([r["z"] for r in rows]))
            zs[smp.split(" ")[0]] = zmed
            dx = (1.0 + (0.035 if law == "rival" else -0.035)) * (1.05 if sname == "fit-route" else 1.0)
            xs.append(zmed * dx); ys.append(t["med"]); lo.append(t["med"] - t["lo"]); hi.append(t["hi"] - t["med"])
        o = np.argsort(xs)
        xs, ys, lo, hi = (np.array(v)[o] for v in (xs, ys, lo, hi))
        ax.errorbar(xs, ys, yerr=[lo, hi], fmt="o" if style["fill"] else "s", color=COL[law], mfc=COL[law] if style["fill"] else "white",
                    mew=1.6, ms=8 if style["fill"] else 7, lw=1.8 if style["fill"] else 1.2, capsize=3, ls=style["ls"], alpha=1 if style["fill"] else 0.75,
                    label=f"{law} · {'primary series (anchored / independent routes)' if style['fill'] else 'fit-route series (never pooled)'}")
# where each law lands if the other were exactly true (per-sample medians, primary series' g_obs)
for truth, law, mk in (("flat", "rival", "x"), ("rival", "flat", "+")):
    pts = []
    for smp, rows in SERIES["primary"].items():
        pts.append((float(np.median([r["z"] for r in rows])), where_if_true(rows, truth)[law]))
    pts.sort()
    ax.plot([p[0] for p in pts], [p[1] for p in pts], mk + ":", color=COL[law], ms=10, mew=2, lw=1.1, alpha=0.9,
            label=f"{law}'s δ if the {truth} law were exactly true")
for smp, z in zs.items():
    ax.annotate({"MUSE-DARK": "MUSE-DARK\n(GalPaK3D, 109)", "RC41": "RC41\n(41)", "NOEMA3D": "NOEMA3D\n(10)", "CRISTAL": "CRISTAL\n(9 / 12)"}[smp],
                (z, 0.455), ha="center", va="top", fontsize=8.5, color="0.35")
ax.set_xscale("log")
ax.set_xlim(0.55, 6.5); ax.set_ylim(-0.62, 0.47)
ax.set_xticks([0.6, 0.8, 1, 1.5, 2, 3, 5]); ax.set_xticklabels(["0.6", "0.8", "1", "1.5", "2", "3", "5"])
ax.set_xlabel("sample median redshift", fontsize=11)
ax.set_ylabel("median δ = log₁₀( D_measured / D_predicted )  at R_e,   95% CI\n< 0: law predicts too much hidden mass;  > 0: too little", fontsize=10)
ax.set_title("author decompositions, not a direct a₀ measurement:  δ(z) for the flat law and the rival a₀ ∝ H(z)\n"
             "(ν_mono, canonical footing; CFG215)", fontsize=11.5)
ax.grid(alpha=0.25, which="both")
ax.legend(fontsize=8.3, loc="lower left", framealpha=0.93, ncol=1)
fig.text(0.01, 0.008, "Route mixing: MUSE-DARK's fitted disc masses sit 0.5 dex below SED + gas and drift with z; CRISTAL's prior is 1 dex wide; RC41 is anchored at 0.2 dex; NOEMA3D has\n"
         "measured CO. The route-mixing mock in the lane shows these biases alone can produce across-sample slopes larger than the rival's expected drift. κ = ½ fitted.",
         fontsize=8, color="0.3")
plt.tight_layout(rect=(0, 0.06, 1, 1))
out = os.path.join(LANE, "cfg215_delta_vs_z.png")
plt.savefig(out, dpi=150)
print("wrote", os.path.basename(out))
