"""PAPER43 figure: forest plot of the Upsilon-robust a0 estimates (p41b, p46, p43, p47) and the random-effects pool (p48), against candidate values.
Numbers are parsed from the committed .out files (sonnet55_push/puzzle_32pi/), not typed in. Writes fig1_paper43_forest.pdf and PAPER43_figures_numbers.json."""
import json, math, os, re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
H = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(H, "..", "..", "sonnet55_push", "puzzle_32pi")
rd = lambda f: open(os.path.join(P, f)).read()
o46, o43, o47, o48, o41b, o42 = (rd(f) for f in ("p46_gas_points_trgb.out", "p43_wallaby_gas_points.out", "p47_little_things_a0.out", "p48_meta_analysis.out",
                                                   "p41b_gas_points_calibration.out", "p42_kernel_on_gas_points.out"))
g = lambda pat, s: re.search(pat, s)
m = {}
x = g(r"TRGB/Cepheid \(f_D 2,3\)\s*:\s*(\d+) galaxies,\s*(\d+) pts;\s*a0 = ([\d.e+-]+) \+- ([\d.]+)%", o46); m["trgb"] = (float(x.group(3)), float(x.group(4)) / 100, int(x.group(1)), int(x.group(2)))
x = g(r"Hubble flow \(f_D 1\)\s*:\s*(\d+) galaxies,\s*(\d+) pts;\s*a0 = ([\d.e+-]+) \+- ([\d.]+)%", o46); m["hf"] = (float(x.group(3)), float(x.group(4)) / 100, int(x.group(1)), int(x.group(2)))
x = g(r"all\s*:\s*(\d+) galaxies,\s*(\d+) pts;\s*a0 = ([\d.e+-]+) \+- ([\d.]+)%", o46); m["all"] = (float(x.group(3)), float(x.group(4)) / 100, int(x.group(1)), int(x.group(2)))
x = g(r"a0 \(gas points, H0 73\) = ([\d.e+-]+) .*\+-([\d.]+)% stat, (\d+) galaxies", o43); y = g(r"gas-dominated points: (\d+) in (\d+) galaxies", o43)
m["wallaby"] = (float(x.group(1)), float(x.group(2)) / 100, int(x.group(3)), int(y.group(1)))
x = g(r"a0 \(all points\) = ([\d.e+-]+) \+- ([\d.]+)%", o47); y = g(r"LITTLE THINGS: (\d+) galaxies .*?; (\d+) points", o47)
m["lt"] = (float(x.group(1)), float(x.group(2)) / 100, int(y.group(1)), int(y.group(2)))
x = g(r"RANDOM-EFFECTS POOLED a0 = ([\d.e+-]+)\s+\(68%: ([\d.e+-]+) - ([\d.e+-]+); \+-([\d.]+)%\)", o48); m["pool"] = (float(x.group(1)), float(x.group(4)) / 100)
m["I2"] = int(g(r"I\^2 = (\d+)%", o48).group(1)); m["Q"] = float(g(r"Q = ([\d.]+)", o48).group(1))
pulls = dict(re.findall(r"^\s+(\S.*?\S)\s+[\d.]+e-1\d: pull ([+-][\d.]+)", o48, re.M)); m["pulls"] = {k: float(v) for k, v in pulls.items()}
m["spread_fcut08"] = float(g(r"fcut 0.8: .*\(spread ([\d.]+)%\)", o41b).group(1))
m["rar_dchi2_U05"] = float(g(r"Upsilon 0.5: .*\| RAR ([+-][\d.]+)", o42).group(1))
json.dump(m, open(os.path.join(H, "PAPER43_figures_numbers.json"), "w"), indent=1)
C1, C2, INK, MUTED = "#2a78d6", "#eb6834", "#1f1f1e", "#6f6e69"
rows = [("SPARC gas points, TRGB/Cepheid", m["trgb"]), ("SPARC gas points, Hubble flow", m["hf"]), ("WALLABY gas points (Hubble flow)", m["wallaby"]),
        ("LITTLE THINGS (authors' M/L)", m["lt"])]
plt.rcParams.update({"font.size": 8.5, "axes.edgecolor": MUTED, "xtick.color": MUTED, "ytick.color": INK, "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(5.8, 3.0))
for i, (lab, v) in enumerate(rows):
    a, s = v[0] * 1e10, v[1]; yv = len(rows) - i
    ax.errorbar(a, yv, xerr=[[a - a * math.exp(-s)], [a * math.exp(s) - a]], fmt="o", color=C1, ms=6, mec="white", mew=1.5, elinewidth=2, capsize=0)
a, s = m["pool"][0] * 1e10, m["pool"][1]
ax.errorbar(a, 0, xerr=[[a - a * math.exp(-s)], [a * math.exp(s) - a]], fmt="D", color=C2, ms=7, mec="white", mew=1.5, elinewidth=2.5, capsize=0)
cands = [(0.8626, "a"), (0.9360, "b"), (1.1312, "c"), (1.20, "d")]
for v, lab in cands:
    ax.axvline(v, color=MUTED, lw=0.8, ls=":")
    ax.text(v, 4.72, lab, va="top", ha="center", fontsize=8, color=INK)
ax.set_yticks(range(0, len(rows) + 1)); ax.set_yticklabels(["random-effects pool"] + [r[0] for r in rows][::-1])
ax.set_xlabel("$a_0$  ($10^{-10}$ m s$^{-2}$)"); ax.set_ylim(-0.6, 4.9); ax.set_xlim(0.4, 2.0)
fig.tight_layout(); fig.savefig(os.path.join(H, "fig1_paper43_forest.pdf")); plt.close(fig)
print(json.dumps(m, indent=1))
