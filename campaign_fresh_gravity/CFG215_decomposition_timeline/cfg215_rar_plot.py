#!/usr/bin/env python3
"""CFG215 companion figure: the mass discrepancy D = g_obs/g_bar against g_bar/a0 for all four high-z decomposition samples (primary
series: anchored / independent routes), over the local SPARC cloud, with the flat law and the rival a0 ~ H(z) at each sample's redshift.
Reads the lane's pipeline through cfg215_timeline.py (exec'd read-only up to its mock; MUTATE off); SPARC through CFG4_common.load_sparc
with the standard 3.6 micron mass-to-light (disc 0.5, bulge 0.7), quality Q <= 2.  A picture, not a new statistic.
Run: python3 campaign_fresh_gravity/CFG215_decomposition_timeline/cfg215_rar_plot.py  ->  cfg215_D_vs_gbar.png
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
SERIES, K, A0F, E, nu1, G2SI = (ns[k] for k in ("SERIES", "K", "A0F", "E", "nu1", "G2SI"))
A0 = A0F["canonical"]

# local SPARC cloud (record's loader; M/L 0.5 / 0.7; Q <= 2; V_bar^2 > 0; R in kpc)
gal = K.load_sparc()
xs, ys = [], []
for g in gal:
    q = g["meta"]["Q"] if g.get("meta") else 9
    if q > 2:
        continue
    vb2 = g["Vgas"] * np.abs(g["Vgas"]) + 0.5 * g["Vdisk"] * np.abs(g["Vdisk"]) + 0.7 * g["Vbul"] * np.abs(g["Vbul"])
    ok = (vb2 > 0) & (g["R"] > 0) & (g["Vobs"] > 0)
    gb = vb2[ok] / g["R"][ok] * G2SI
    go = g["Vobs"][ok] ** 2 / g["R"][ok] * G2SI
    xs.append(gb / A0); ys.append(go / gb)
xs = np.concatenate(xs); ys = np.concatenate(ys)
sel = (xs > 0.02) & (xs < 60) & (ys > 0.5) & (ys < 40)

fig, ax = plt.subplots(figsize=(11.5, 7.0))
ax.scatter(xs[sel], ys[sel], s=4, color="0.75", alpha=0.35, lw=0, rasterized=True, label=f"local SPARC (z = 0; {int(sel.sum()):,d} radial points, Υ★ 0.5/0.7)")
x = np.geomspace(0.02, 60, 500)
ax.plot(x, [nu1(K.nu_mono, v) for v in x], color="#1f6fd1", lw=2.6, label="flat a₀ (the framework's prediction, any z)")
SAMP = {"MUSE-DARK": ("MUSE-DARK z≈0.9 (SED + H₂ route)", "^", "#2a9d5c"), "RC41": ("Price RC41 z≈1.5 (prior-anchored fit)", "s", "#8e44ad"),
        "NOEMA3D": ("NOEMA3D z≈1.2 (SED + CO)", "D", "#e0a800"), "CRISTAL": ("ALMA-CRISTAL z≈5.2 (SED + dust gas)", "o", "#111111")}
zrep = {}
for smp, rows in SERIES["primary"].items():
    zrep[smp] = float(np.median([r["z"] for r in rows]))
for smp in ("MUSE-DARK", "RC41", "NOEMA3D", "CRISTAL"):
    lab, mk, col = SAMP[smp]
    rows = SERIES["primary"][smp]
    gx = np.array([r["gbar"] / A0 for r in rows]); dy = np.array([r["D"] for r in rows])
    m = (gx > 0.02) & (gx < 60) & (dy > 0.3)
    ax.scatter(gx[m], dy[m], marker=mk, s=44 if smp != "MUSE-DARK" else 16, color=col, alpha=0.9 if smp != "MUSE-DARK" else 0.5,
               edgecolor="white", lw=0.5, zorder=4, label=lab + f" (n = {int(m.sum())})")
for smp, ls, col in (("MUSE-DARK", ":", "#e9a37f"), ("NOEMA3D", "--", "#e0865a"), ("CRISTAL", "-", "#d1541f")):
    z = zrep[smp]
    ax.plot(x, [nu1(K.nu_mono, v / E(z)) for v in x], color=col, lw=2.0, ls=ls, zorder=3,
            label=f"rival a₀ ∝ H(z), at z = {z:.1f} (a₀ ×{E(z):.1f})")
ax.axhline(1.0, color="0.4", lw=1, ls=":")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(0.03, 60); ax.set_ylim(0.3, 40)
ax.set_yticks([0.5, 1, 2, 3, 5, 10, 20, 40]); ax.set_yticklabels(["0.5", "1", "2", "3", "5", "10", "20", "40"])
ax.set_xlabel("baryonic acceleration  g_bar / a₀   (a₀ = 9.36×10⁻¹¹ m s⁻², canonical)", fontsize=11)
ax.set_ylabel("mass discrepancy  D = g_obs / g_bar", fontsize=11)
ax.set_title("author decompositions at z ≈ 0.9–5.2 against the local relation, the flat law and the rival a₀ ∝ H(z)\n"
             "(not a direct a₀ measurement; each sample at its own R_e; CFG215)", fontsize=11.5)
ax.grid(alpha=0.25, which="both")
ax.legend(fontsize=8.3, loc="upper right", framealpha=0.93)
fig.text(0.01, 0.008, "Both laws converge to D → 1 at high g_bar. The high-z samples mostly sit at g_bar ≈ 1–15 a₀: there the z ≈ 1.2 rival differs from the flat law in D by ×1.25 at 1 a₀ and ×1.06 at 10 a₀; "
         "the z ≈ 5 rival by ×2.2 and ×1.4.\nThe mass routes differ by sample (lane README). κ = ½ fitted.", fontsize=8, color="0.3")
plt.tight_layout(rect=(0, 0.05, 1, 1))
out = os.path.join(LANE, "cfg215_D_vs_gbar.png")
plt.savefig(out, dpi=150)
print("wrote", os.path.basename(out), f"; SPARC points plotted {int(sel.sum())}")
