#!/usr/bin/env python3
"""CFG217 figure: how RC100's verdict depends on the differential baryon-mass calibration between z ~ 0.6 and z ~ 2.5.
x: the change applied to the analysis baryon mass at z = 2.5 relative to z = 0.6 (dex), g_bar x 10^(beta log10((1 + z)/2.5)), beta = x / log10(3.5/1.6).
y: the Theil-Sen slope of delta on z, for the flat law and the rival a0 ~ E(z), with 95% bands (500 galaxy resamples per point).
Dotted lines: the slopes each law would show if it were exactly true.  Ticks: the CFG217 gas variants at their ENDPOINT-EQUIVALENT tilt on this axis (regression of each variant's
per-galaxy baryon-mass factor on log10((1 + z)/2.5) x log10(3.5/1.6)).  CORRECTED 2026-09-29 after a referee question: the first version placed the ticks at the variants'
half-median differentials (median factor of the z > z_med half over that of the z <= z_med half, a baseline of about 1.2 in z), which understates the variants' position on
this axis (a baseline of 1.9 in z) by about 1.7; the first-version charts are kept as *_firstrun.png.
Reads the lane's data and functions through cfg217_attack.py (exec'd read-only up to G1; MUTATE off).
Run: python3 campaign_fresh_gravity/CFG217_rc100_attack/cfg217_plot.py -> cfg217_calibration_sensitivity.png
"""
import os, sys, io, math, contextlib
sys.dont_write_bytecode = True
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LANE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(LANE, "cfg217_attack.py")
src = open(path).read()
ns = {"__file__": path, "__name__": "cfg217"}
_e = os.environ.pop("MUTATE", None)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index('R.banner("G2')], "cfg217", "exec"), ns)               # through the G1 block (VAR, the reconstruction), not beyond
if _e is not None:
    os.environ["MUTATE"] = _e
z, gobs0, gbar0, delta_arr, ts, BASE = (ns[k] for k in ("z", "gobs0", "gbar0", "delta_arr", "ts", "BASE"))
DLOG = math.log10(3.5 / 1.6)
rng = np.random.default_rng(7)
NB = 500
n = len(z)
B = rng.integers(0, n, size=(NB, n))
i_, j_ = np.triu_indices(n, 1)


def slopes(zv, dv):
    dx = zv[j_] - zv[i_]
    m = dx != 0
    return float(np.median((dv[j_] - dv[i_])[m] / dx[m]))


xs = np.linspace(-0.6, 0.6, 25)
out = {"flat": [], "rival": []}
for x in xs:
    beta = x / DLOG
    ga = gbar0 * 10 ** (beta * np.log10((1 + z) / 2.5))
    Dv = gobs0 / ga
    for law in ("flat", "rival"):
        d = delta_arr(z, Dv, ga, law)
        pt = slopes(z, d)
        bs = np.array([slopes(z[b], d[b]) for b in B])
        out[law].append((pt, np.percentile(bs, 2.5), np.percentile(bs, 97.5)))
out = {k: np.array(v) for k, v in out.items()}
exp = BASE["exp"]

fig, ax = plt.subplots(figsize=(11.5, 6.8))
ax.axvspan(-0.2, 0.2, color="0.9", zorder=0)
ax.text(0.0, 0.183, "frozen 'plausible' differential (±0.2 dex)", ha="center", fontsize=8.5, color="0.4")
for law, col in (("flat", "#1f6fd1"), ("rival", "#d1541f")):
    ax.plot(xs, out[law][:, 0], color=col, lw=2.4, label=f"δ_{law} slope on z (the data)")
    ax.fill_between(xs, out[law][:, 1], out[law][:, 2], color=col, alpha=0.2, lw=0)
ax.axhline(0, color="0.2", lw=1)
ax.axhline(exp["rival"]["flat"], color="#1f6fd1", ls=":", lw=1.4)
ax.text(0.595, exp["rival"]["flat"] + 0.004, "δ_flat slope if the RIVAL were exactly true", color="#1f6fd1", fontsize=8.5, ha="right")
ax.axhline(exp["flat"]["rival"], color="#d1541f", ls=":", lw=1.4)
ax.text(0.595, exp["flat"]["rival"] - 0.012, "δ_rival slope if the FLAT law were exactly true", color="#d1541f", fontsize=8.5, ha="right")
ax.text(0.595, 0.004, "0 = the law is right", fontsize=8.5, ha="right", color="0.3")
# gas-variant ticks at their ENDPOINT-EQUIVALENT tilt on this axis (regression of log10 factor on log10((1 + z)/2.5) times DLOG), all N galaxies with the reconstructed M*
xz = np.log10((1 + z) / 2.5)
Mfull = 10 ** ns["logMs"]
ticks = {}
for name, f in ns["VAR"].items():
    fac = np.array([(1 + f(zz, m, mu)) / (1 + mu) for zz, m, mu in zip(z, Mfull, ns["mu0"])])
    ticks[name.split(" ")[0]] = float(np.polyfit(xz, np.log10(fac), 1)[0]) * DLOG
LAB = {"V1": "V1 gas fraction\nfixed with z", "V2": "V2 0.5μ", "V3": "V3 2μ", "V4": "V4 0.18μ\n(α_CO 0.8)", "V5": "V5 1.49μ"}
for k, xd in ticks.items():
    if k == "V0":
        continue
    ax.axvline(xd, color="0.55", lw=0.8, ls="--")
    right = k in ("V3", "V4")
    ax.text(xd + (0.004 if right else -0.004), -0.215, LAB[k], rotation=90, fontsize=7.8, va="bottom", ha="left" if right else "right", color="0.35")
ax.axvline(0, color="0.2", lw=1.2, ls="--")
ax.text(0.0, -0.215, "adopted\nTacconi+18", rotation=90, fontsize=7.8, va="bottom", ha="right", color="0.2")
ax.set_xlim(-0.6, 0.6); ax.set_ylim(-0.22, 0.2)
ax.set_xlabel("change applied to the analysis baryon mass at z ≈ 2.5 relative to z ≈ 0.6  (dex)     ← lighter at high z                heavier at high z →", fontsize=10)
ax.set_ylabel("slope of δ = log(D_measured / D_predicted) on z   (per unit z)", fontsize=10.5)
ax.set_title("RC100 (100 discs, z 0.6–2.5): the flat-vs-rival verdict is a measurement of the differential baryon-mass calibration (CFG217)", fontsize=11)
ax.legend(fontsize=9, loc="upper left")
ax.grid(alpha=0.25)
fig.text(0.01, 0.008, "Reading: at the adopted gas scaling (dashed line at 0) the rival's slope is −0.09 (4.9σ from its expectation 0). Lowering high-z baryons by about 0.25 dex (left)\n"
         "brings both slopes to the rival-true expectations; raising them (right) drives BOTH laws negative. The dependence on gas fraction / α_CO is the crux.\n"
         "Author decompositions, not a direct a₀ measurement. κ = ½ fitted.", fontsize=8, color="0.3")
plt.tight_layout(rect=(0, 0.08, 1, 1))
outp = os.path.join(LANE, "cfg217_calibration_sensitivity" + ("_corrected" if os.environ.get("RC100_INPUT", "").strip() == "corrected" else "") + ".png")
plt.savefig(outp, dpi=150)
print("wrote", os.path.basename(outp))
