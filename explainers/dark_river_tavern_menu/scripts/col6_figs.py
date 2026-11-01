"""Course 'Tonight's specials': route E, version N, as of 1 November 2026. Nine pictures, captions/col6.json, board_tiles_route_e.json.

Plot and read only. Every number is read from a committed lane file (JSON or .out), and the numbers named in the course's brief are
asserted against those files, so a mismatch stops the script instead of reaching a caption. Thresholds are the lanes' frozen lines:
Upsilon 0.50-0.80 and rms <= 0.110; tilt <= 0.15; 15 keys |Z| <= 2; X-COP |mean| <= 0.05, rms <= 0.10; LITTLE THINGS |median E| <= 0.10;
groups verdict CONSISTENT, |Z| <= 2. Status colour is never better than the lane's own verdict. Run: python3 -I scripts/col6_figs.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import menu_style as ms  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

R = ms.ROOT
L = "rebuild_2026_10_22/"
HERE = Path(__file__).resolve().parents[1]
F = dict(
    nr2=L + "NR2_low_mass_ng80/nr2_results.json", nr2d=L + "NR2_low_mass_ng80/nr2_draws.json", nr2b=L + "NR2_low_mass_ng80/nr2_bins.json",
    nr2r=L + "NR2_low_mass_ng80/README.md",
    nr3=L + "NR3_ur1_on_nr2/nr3_MEDIAN_results.json", nr3l=L + "NR3_ur1_on_nr2/nr3_LOW_results.json", nr3h=L + "NR3_ur1_on_nr2/nr3_HIGH_results.json",
    nr3s=L + "NR3_ur1_on_nr2/nr3_results.json", nr3r=L + "NR3_ur1_on_nr2/README.md",
    zn4=L + "ZN4_cluster_resolution/zn4_results.json", zn4r=L + "ZN4_cluster_resolution/README.md",
    gs4=L + "GS4_pointed_gas_offset/gs4_results.json", gs4r=L + "GS4_pointed_gas_offset/README.md",
    rf3=L + "RF3_cluster_keys_hse_free/README.md",
    lc1=L + "LC1_live_contraction/lc1.out", lc1r=L + "LC1_live_contraction/README.md",
    nr4=L + "NR4_low_mass_requirement/nr4.out", nr4r=L + "NR4_low_mass_requirement/README.md", nr4j=L + "NR4_low_mass_requirement/nr4_results.json",
    dr1=L + "DR1_density_term_law/dr1_offline.json", dr1g=L + "DR1_density_term_law/dr1_g005_f034.json", dr1r=L + "DR1_density_term_law/README.md",
    dr3=L + "DR3_thin_disc_monopole/dr3_PRIMARY_results.json", dr3s=L + "DR3_thin_disc_monopole/dr3_results.json", dr3r=L + "DR3_thin_disc_monopole/README.md",
    dr7=L + "DR7_fragments/dr7_MEDIAN_results.json", dr7s=L + "DR7_fragments/dr7_results.json", dr7r=L + "DR7_fragments/README.md",
    dr9=L + "DR9_fountain_coupling/dr9_results.json", dr9a=L + "DR9_fountain_coupling/AMENDMENT_A1.md", dr9r=L + "DR9_fountain_coupling/README.md",
    cp1=L + "CP1_complementarity_phase_closure/cp1_MEDIAN_results.json", cp1s=L + "CP1_complementarity_phase_closure/cp1_results.json",
    cp1o=L + "CP1_complementarity_phase_closure/cp1.out", cp1r=L + "CP1_complementarity_phase_closure/README.md",
)
J = {k: json.load(open(R / v)) for k, v in F.items() if v.endswith(".json")}
T = {k: (R / v).read_text() for k, v in F.items() if not v.endswith(".json")}
A, B = "A_c2b_refit", "B_cfg886_bg"
BINS = ["20-60", "60-100", "100-150", "150-200", "200-250", "250-400"]
OK, BAD, SOFT = ms.STATUS["PASS"], ms.STATUS["FAIL"], ms.BAND
CAP, TILES = [], []


def near(a, b, tol=0.0051):
    assert abs(a - b) <= tol, (a, b)


def commit(path):
    out = subprocess.run(["git", "-C", str(R), "log", "-1", "--format=%h", "--", path], capture_output=True, text=True)
    return out.stdout.strip() or "uncommitted"


def add(slug, name, status, note, lanes, data, picture, why, numbers, keys):
    assert all(c not in why + data + picture for c in ("theory closed.", "dark matter")), slug
    CAP.append(dict(slug=slug, name=name, status=status, data=data, picture=picture, why=why,
                    numbers=[dict(what=w, value=v, file=F[k]) for w, v, k in numbers],
                    sources=[dict(path=F[k], commit=commit(F[k])) for k in keys]))
    TILES.append(dict(col=6, name=name, st=status, note=note, note_label="Tonight", lanes=lanes, was=None))


# The runs every dish leans on
M, LO, HI = (J[k]["runs"] for k in ("nr3", "nr3l", "nr3h"))
OFF, BL = M["EM1|off"], M["EM1|blum"]
UA = lambda r: r["sparc"][A]["U"]  # noqa: E731
UB = lambda r: r["sparc"][B]["U"]  # noqa: E731
X_LAB = [b.replace("-", "–") for b in BINS]

# ---------------------------------------------------------------- 1 SPARC line
draws = J["nr2d"]
nd, npass = len(draws), sum(d["line"] for d in draws)
nhigh = sum(1 for d in draws if not d["line"] and max(d["U"]) > 0.80)
nlow = sum(1 for d in draws if not d["line"] and min(d["U"]) < 0.50)
assert (nd, npass, nhigh, nlow) == (40, 24, 16, 0)
assert J["nr2"]["verdict"] == "ALL-NG80 PASSES [NOISE-LIMITED]"
near(UA(OFF), 0.75); near(UB(OFF), 0.76)
bins = J["nr2b"]["bins"]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 5), gridspec_kw=dict(width_ratios=[1.15, 1], wspace=0.26))
for a in (a1, a2):
    a.axhspan(0.50, 0.80, color=SOFT, zorder=0)
    a.set_ylim(0.2, 1.3)
a1.plot(range(6), [bins[b]["U"] for b in BINS], "o-", color=ms.DATA)
for i, b in enumerate(BINS):
    a1.annotate(f'{bins[b]["U"]:.2f}\nn {bins[b]["n"]}', (i, bins[b]["U"]), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=8.5)
a1.axhline(UA(OFF), color=ms.MUTED, ls="--", lw=1)
a1.text(-0.3, UA(OFF) + 0.01, f"sample median {UA(OFF):.2f}", fontsize=8.5, color=ms.MUTED)
a1.text(-0.3, 0.515, "frozen window 0.50–0.80", fontsize=8.5, color=ms.MUTED)
a1.set_xticks(range(6), X_LAB, fontsize=8.5); a1.set_xlim(-0.4, 5.4)
a1.set_xlabel("V_flat bin, km/s"); a1.set_ylabel("Υ, median in bin (background A)")
us = sorted(draws, key=lambda d: d["U"][0])
a2.scatter(range(nd), [d["U"][0] for d in us], c=[OK if d["line"] else BAD for d in us], s=26, zorder=3)
a2.set_xlabel("40 draws of the three η medians, sorted"); a2.set_ylabel("Υ, sample median (background A)")
a2.text(1, 1.17, f"{npass} of {nd} draws on the line\n{nhigh} off on the high side, {nlow} low", fontsize=9.5, color=ms.INK)
ms.finish(fig, "c6_01_sparc_line_n", "COND", "SPARC line, version N", f"CONDITIONAL. Υ {UA(OFF):.2f} / {UB(OFF):.2f} on the line, NOISE-LIMITED: {npass} of {nd} seed draws stay on it",
          "NR2_low_mass_ng80/nr2_results.json, nr2_draws.json, nr2_bins.json")
add("c6_01_sparc_line_n", "SPARC line, version N", "COND",
    f"Υ {UA(OFF):.2f} / {UB(OFF):.2f}, NOISE-LIMITED, {npass} of {nd} draws. Not a pass.", ["NR2", "NR3"],
    "175 SPARC galaxies against version N: the a0 law's sector kept apart from a cold dark energy halo whose core comes from native zooms, with η measured at ng 80 at 10¹⁰, 10¹¹ and 10¹² solar masses, nine seeds each. One Υ per galaxy; the line is median Υ in 0.50–0.80 and rms at most 0.110, on both backgrounds.",
    "Left: median Υ in each V_flat bin with the frozen window shaded; the window grades the sample median, not each bin. Right: the sample median Υ for each of 40 draws that resample all three η medians together, green on the line, red off it.",
    f"The lane's own label is ALL-NG80 PASSES [NOISE-LIMITED], and this dish does not print it as a pass. Seed noise alone takes the median off the line: {nhigh} of {nd} draws land above 0.80, none below 0.50, and 40 draws is a coarse estimate of seed scatter only. The median also hides a run of Υ with V_flat, from {bins['20-60']['U']:.2f} in dwarfs (the top of the Υ grid) to {bins['150-200']['U']:.2f} at 150–200 km/s, so the tilt reads {OFF['sparc'][A]['tilt']:+.2f} against the 0.15 line. The same runs fail cluster keys G-IN-all, G-MID-T3 and G-IN-Mall, all over.",
    [("Υ A / B, rms A / B", f"{UA(OFF):.2f} / {UB(OFF):.2f}, {OFF['sparc'][A]['rms']:.4f} / {OFF['sparc'][B]['rms']:.4f}", "nr3"),
     ("draws on the line; high; low", f"{npass} of {nd}; {nhigh}; {nlow}", "nr2d"), ("frozen verdict", J["nr2"]["verdict"], "nr2")],
    ["nr2", "nr2d", "nr2b", "nr2r", "nr3"])

# ---------------------------------------------------------------- 2 Groups
g = OFF["groups"]
near(g["Z"], 1.47); assert g["verdict"] == "CONSISTENT"
rows = [("EM1, no response (version N)", OFF["groups"], True), ("EM1 + Blumenthal", BL["groups"], True),
        ("Fair share at r200, no response", M["FAIR200|off"]["groups"], False), ("Fair share at r_ta, no response", M["FAIRTA|off"]["groups"], False)]
fig, ax = plt.subplots(figsize=(8, 4.3))
ax.axvspan(-2, 2, color=SOFT, zorder=0)
for i, (lab, gg, main) in enumerate(rows[::-1]):
    ax.plot(gg["Z"], i, "o", ms=10 if main else 7, color=OK if gg["verdict"] == "CONSISTENT" else ms.MUTED, zorder=3)
    ax.annotate(f'{gg["Z"]:+.2f}  {gg["verdict"]}', (gg["Z"], i), xytext=(9, -3), textcoords="offset points", fontsize=9)
ax.set_yticks(range(4), [r[0] for r in rows[::-1]], fontsize=9.5)
ax.set_xlim(-3, 8); ax.set_ylim(-0.6, 3.6)
ax.set_xlabel("Z of the 63 groups' mean (log σ measured − log σ predicted); shaded |Z| ≤ 2")
fig.subplots_adjust(left=0.30)
ms.finish(fig, "c6_02_groups_n", "PASS", "Groups, version N", f"PASSES. Z {g['Z']:+.2f}, verdict {g['verdict']}, on EM1's mass line", "NR3_ur1_on_nr2/nr3_MEDIAN_results.json, NR2_low_mass_ng80/nr2.out")
add("c6_02_groups_n", "Groups, version N", "PASS", f"Z {g['Z']:+.2f}, CONSISTENT.", ["NR3", "NR2"],
    f"{g['N']} galaxy groups: measured velocity dispersion against the dispersion version N predicts. Mean difference {g['mean']:+.3f} dex, total error {g['tot']:.3f} dex.",
    "A Z scale with |Z| ≤ 2 shaded. The large green dot is version N; below it the same groups under the same machinery with other mass rules, for scale.",
    f"Version N's mean sits {g['Z']:+.2f} error bars from the measurement, inside the line, and adding the response barely moves it ({BL['groups']['Z']:+.2f}). It reads {g['Z']:+.2f} at every input in NR2's band, because the groups don't depend on the low-mass η. The pass belongs to EM1's mass line: the fair-share mass rows read {M['FAIR200|off']['groups']['Z']:+.2f} and {M['FAIRTA|off']['groups']['Z']:+.2f}, NOT DIAGNOSTIC. Groups are one gate of several, in a lane whose overall label answers a different question.",
    [("Z, verdict", f"{g['Z']:+.2f}, {g['verdict']}", "nr3"), ("Z, EM1 + Blumenthal", f"{BL['groups']['Z']:+.2f}", "nr3"), ("N, mean, total error", f"{g['N']}, {g['mean']:+.3f}, {g['tot']:.3f}", "nr3")],
    ["nr3", "nr3r", "nr2"])

# ---------------------------------------------------------------- 3 Cluster keys on measured gas
Z4 = J["zn4"]["runs"]
meas, meas2, xg = Z4["f* 0.034, gas +0.005"], Z4["f* 0.0615, gas +0.005"], Z4["f* 0.034, X-COP's gas"]
KEYS = list(meas["cells"]["h0672"])
zv = lambda run, k, h="h0672": run["cells"][h][k]["Z"]  # noqa: E731
over = lambda run: [k for k in KEYS if abs(zv(run, k)) > 2 or abs(zv(run, k, "h0686")) > 2]  # noqa: E731
assert len(KEYS) == 15 and len(over(meas)) == 3 and len(over(meas2)) == 3 and len(over(xg)) == 0
near(zv(meas, "G-OUT-M3"), 4.41); near(zv(meas2, "G-OUT-M3"), 4.13)
gs = J["gs4"]["primary"]
near(gs["med"], 0.005, 0.001); near(gs["se"], 0.017, 0.001)
assert "+0.111" in T["zn4r"] and "+0.005 ± 0.017" in T["gs4r"]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 5.6), gridspec_kw=dict(width_ratios=[2.5, 1], wspace=0.28))
a1.axvspan(-2, 2, color=SOFT, zorder=0)
for i, k in enumerate(KEYS[::-1]):
    a1.plot(zv(xg, k), i, "o", mfc="none", mec=ms.MUTED, ms=7, label="gas +0.111, unsupported" if i == 0 else None)
    v = zv(meas, k)
    a1.plot(v, i, "o", color=BAD if k in over(meas) else ms.DATA, ms=7, zorder=3, label="measured gas +0.005" if i == 0 else None)
    if k in over(meas):
        a1.annotate(f"{v:+.2f}", (v, i), xytext=(7, -3), textcoords="offset points", fontsize=8.5, color=BAD)
a1.set_yticks(range(15), KEYS[::-1], fontsize=8)
a1.set_xlim(-3, 6); a1.set_xlabel("Z, measured − predicted, f★ 0.034, h 0.672; shaded |Z| ≤ 2")
a1.legend(loc="upper right", fontsize=8, frameon=True, facecolor="white", edgecolor="none", handletextpad=0.3, borderpad=0.2)
a2.axhline(J["gs4"]["line"], color=ms.MODEL, ls="--", lw=1)
a2.text(0.5, J["gs4"]["line"] - 0.002, f'needed +{J["gs4"]["line"]:.3f}', ha="center", va="top", fontsize=8.5, color=ms.MODEL)
a2.errorbar([0.5], [gs["med"]], yerr=[gs["se"]], fmt="o", color=ms.DATA, capsize=4)
a2.text(0.5, gs["med"] + gs["se"] + 0.005, f'GS4 +{gs["med"]:.3f} ± {gs["se"]:.3f}\n{gs["n"]} clusters', ha="center", fontsize=8.5)
a2.plot([0.5], [0.111], "o", mfc="none", mec=ms.MUTED, ms=7)
a2.text(0.5, 0.116, "+0.111, five massive\nclusters", ha="center", fontsize=8.5, color=ms.MUTED)
a2.set_xlim(0, 1); a2.set_xticks([]); a2.set_ylim(-0.03, 0.15); a2.set_ylabel("gas offset, dex")
ms.finish(fig, "c6_03_cluster_keys_gas", "FAIL", "Cluster keys on measured gas", f"FAILS. 12 of 15 keys, G-OUT-M3 {zv(meas,'G-OUT-M3'):+.2f} / {zv(meas2,'G-OUT-M3'):+.2f} at f★ 0.034 / 0.0615",
          "ZN4_cluster_resolution/zn4_results.json; GS4_pointed_gas_offset/gs4_results.json")
add("c6_03_cluster_keys_gas", "Cluster keys on measured gas", "FAIL", f"12 of 15, G-OUT-M3 {zv(meas,'G-OUT-M3'):+.2f} / {zv(meas2,'G-OUT-M3'):+.2f}. Fifteen of 15 only on a gas scale the data don't support.", ["ZN4", "GS4"],
    "Fifteen stacked weak-lensing keys on eRASS1 clusters against the native z = 0 profile at ng 80 (six seeds at each of 10¹⁴ and 10¹⁵), with gas masses on the measured scale. GS4 measured that scale on 45 clusters against published Chandra and XMM gas masses.",
    "Left: Z for each key, filled on the measured gas (+0.005), hollow on +0.111, with |Z| ≤ 2 shaded. Right: the gas offset itself, GS4's measurement with its error, the +0.093 the pass needs, and the +0.111 from five massive clusters.",
    f"On the gas that was measured, {', '.join(over(meas))} go over 2. ZN4's frozen verdict was CONVERGED and its class graded on +0.111 only, where 15 of 15 keys pass; that is a statement about resolution, and the measured +0.005 ± 0.017 is over 5 standard errors below the needed offset. The hollow points are shown as a scale the data don't support, not as a result. This is the native profile's path; version N's own path also has 12 of 15, with other keys ({', '.join(OFF['keys']['bad'])}) failing, and the two aren't comparable.",
    [("keys, worst, f★ 0.034", f"12 of 15, G-OUT-M3 {zv(meas,'G-OUT-M3'):+.2f}", "zn4"), ("keys, worst, f★ 0.0615", f"12 of 15, G-OUT-M3 {zv(meas2,'G-OUT-M3'):+.2f}", "zn4"),
     ("on +0.111, f★ 0.034", f"15 of 15, G-OUT-M3 {zv(xg,'G-OUT-M3'):+.2f}", "zn4"), ("gas offset", f"+{gs['med']:.3f} ± {gs['se']:.3f}", "gs4")],
    ["zn4", "zn4r", "gs4", "gs4r", "nr3"])

# ---------------------------------------------------------------- 4 X-COP
xn, xN = xg["xcop"], OFF["xcop"]
near(xn["mean"], 0.013, 0.001); near(xn["rms"], 0.075, 0.001); near(xN["mean"], -0.160, 0.001); near(xN["rms"], 0.186, 0.001)
assert xn["mean"] == meas["xcop"]["mean"]
assert "UNDETERMINED" in T["rf3"]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 5), gridspec_kw=dict(width_ratios=[1.4, 1], wspace=0.28))
xs = list(xn["by_x"])
a1.axhspan(-0.05, 0.05, color=SOFT, zorder=0)
a1.axhline(0, color=ms.MUTED, lw=0.8)
a1.plot(xs, [xn["by_x"][k] for k in xs], "o-", color=OK, label="native z = 0 profile (ZN4)")
a1.plot(xs, [xN["by_x"][k] for k in xs], "s-", color=BAD, label="version N's path (NR3, EM1, off)")
a1.set_xlabel("x = r/R500 bin"); a1.set_ylabel("log (M hydrostatic / M model), dex")
a1.legend(fontsize=8.5, loc="lower left")
a1.text(4.05, 0.056, "shading: the |mean| ≤ 0.05 line, drawn\nfor scale; it grades all 35 rows", ha="right", fontsize=8, color=ms.MUTED)
a1.set_ylim(-0.26, 0.11)
a2.add_patch(plt.Rectangle((-0.05, 0), 0.10, 0.10, color=SOFT, zorder=0))
a2.plot(xn["mean"], xn["rms"], "o", color=OK, ms=9)
a2.annotate(f'native\n{xn["mean"]:+.3f}, {xn["rms"]:.3f}', (xn["mean"], xn["rms"]), xytext=(10, 12), textcoords="offset points", fontsize=9)
a2.plot(xN["mean"], xN["rms"], "s", color=BAD, ms=9)
a2.annotate(f'version N\n{xN["mean"]:+.3f}, {xN["rms"]:.3f}', (xN["mean"], xN["rms"]), xytext=(10, -14), textcoords="offset points", fontsize=9)
a2.set_xlim(-0.22, 0.12); a2.set_ylim(0, 0.24); a2.set_xlabel("mean, dex"); a2.set_ylabel("rms, dex")
ms.finish(fig, "c6_04_xcop_two_profiles", "COND", "X-COP, two profiles", "CONDITIONAL. Native passes on hydrostatic masses only; N's path fails. Different profiles",
          "ZN4_cluster_resolution/zn4_results.json; NR3_ur1_on_nr2/nr3_MEDIAN_results.json")
add("c6_04_xcop_two_profiles", "X-COP, two profiles", "COND", f"Native {xn['mean']:+.3f}, {xn['rms']:.3f}, hydrostatic masses only. N's path {xN['mean']:+.3f}, {xN['rms']:.3f}, fails.", ["ZN4", "NR3", "RF3"],
    "Seven X-COP clusters, 35 rows at x ≤ 0.75: hydrostatic mass against baryons plus model mass. One row of results for the native z = 0 profile at ng 80, one for version N's path.",
    "Left: mean residual in each x bin for both paths. Right: the two paths in the mean and rms plane, with the frozen box |mean| ≤ 0.05, rms ≤ 0.10 shaded.",
    f"These are different profiles, so the two rows are not an improvement of one over the other and shouldn't be read as a trend. The native profile lands inside the box at {xn['mean']:+.3f}, {xn['rms']:.3f}, but the gate is built from hydrostatic masses and RF3 found no clean hydrostatic-free X-COP mass on disk, so without them this is UNDETERMINED. Version N's path misses at {xN['mean']:+.3f}, {xN['rms']:.3f}. Hence conditional: the pass belongs to one path and rests on one kind of mass. Native reads the same at either gas scale because X-COP's line uses its own gas.",
    [("native mean, rms", f"{xn['mean']:+.3f}, {xn['rms']:.3f}", "zn4"), ("version N mean, rms", f"{xN['mean']:+.3f}, {xN['rms']:.3f}", "nr3"), ("X-COP without hydrostatic masses", "UNDETERMINED", "rf3")],
    ["zn4", "zn4r", "nr3", "rf3"])

# ---------------------------------------------------------------- 5 LITTLE THINGS
near(OFF["lt"][A], 0.153, 0.001); near(OFF["lt"][B], 0.147, 0.001)
rows = [("MEDIAN, no response (version N)", OFF), ("NR2 band low, no response", LO["EM1|off"]), ("NR2 band high, no response", HI["EM1|off"]), ("MEDIAN, EM1 + Blumenthal", BL)]
fig, ax = plt.subplots(figsize=(8, 4.3))
ax.axvspan(-0.10, 0.10, color=SOFT, zorder=0)
for i, (lab, r) in enumerate(rows[::-1]):
    for t, mk in ((A, "o"), (B, "s")):
        ax.plot(r["lt"][t], i + (0.1 if t == A else -0.1), mk, color=BAD if abs(r["lt"][t]) > 0.10 else OK, ms=8, zorder=3)
    ax.annotate(f'{r["lt"][A]:+.3f} / {r["lt"][B]:+.3f}', (max(r["lt"][A], r["lt"][B]), i), xytext=(12, -3), textcoords="offset points", fontsize=9)
ax.set_yticks(range(4), [r[0] for r in rows[::-1]], fontsize=9.5)
ax.set_xlim(-0.12, 0.33); ax.set_ylim(-0.6, 3.6)
ax.set_xlabel("median E (circle background A, square B); shaded |E| ≤ 0.10")
fig.subplots_adjust(left=0.30)
ms.finish(fig, "c6_05_little_things_n", "FAIL", "LITTLE THINGS, version N", f"FAILS. Median E {OFF['lt'][A]:+.3f} / {OFF['lt'][B]:+.3f} at the median η, line 0.10", "NR3_ur1_on_nr2/nr3_MEDIAN_results.json, nr3_LOW_results.json, nr3_HIGH_results.json")
add("c6_05_little_things_n", "LITTLE THINGS, version N", "FAIL", f"{OFF['lt'][A]:+.3f} / {OFF['lt'][B]:+.3f} at NR3 MEDIAN, off.", ["NR3"],
    "LITTLE THINGS dwarfs against version N with no response, on both backgrounds. Baryons are a point mass inside R_max, by hand, as stated in UR1's criteria.",
    "A scale of median E with |E| ≤ 0.10 shaded; one row per input, circle and square for the two backgrounds, red outside the line.",
    f"At NR2's median η version N's dwarfs read {OFF['lt'][A]:+.3f} / {OFF['lt'][B]:+.3f}, outside the 0.10 line on both backgrounds. NR2's high band does read {HI['EM1|off']['lt'][A]:+.3f} / {HI['EM1|off']['lt'][B]:+.3f}, but a band run reaching a line isn't a pass: that is NR2's upper band, ρ at p84. Adding the response at the median, {BL['lt'][A]:+.3f} / {BL['lt'][B]:+.3f}, still fails.",
    [("MEDIAN off", f"{OFF['lt'][A]:+.3f} / {OFF['lt'][B]:+.3f}", "nr3"), ("LOW off", f"{LO['EM1|off']['lt'][A]:+.3f} / {LO['EM1|off']['lt'][B]:+.3f}", "nr3l"), ("HIGH off", f"{HI['EM1|off']['lt'][A]:+.3f} / {HI['EM1|off']['lt'][B]:+.3f}", "nr3h"),
     ("MEDIAN, Blumenthal", f"{BL['lt'][A]:+.3f} / {BL['lt'][B]:+.3f}", "nr3")],
    ["nr3", "nr3l", "nr3h", "nr3r"])

# ---------------------------------------------------------------- 6 Live contraction + 7's cell table
lc = T["lc1"].split("z 0.00:")[1]
RD = [float(v) for v in re.search(r"r/R_d \[(.*?)\]", lc).group(1).split(",")]
QL = [float(v) for v in re.search(r"Q live\s+(.*)", lc).group(1).split()]
QB = [float(v) for v in re.search(r"Q Blumenthal\s+(.*)", lc).group(1).split()]
QG = [float(v) for v in re.search(r"Q Gnedin\s+(.*)", lc).group(1).split()]
mq = re.search(r"f_Q \(Blumenthal\) ([\d.]+) \[([\d.]+), ([\d.]+)\]", lc)
fq, fql, fqh = (float(mq.group(i)) for i in (1, 2, 3))
near(fq, 0.872, 0.0005); near(UA(BL), 0.35); near(UB(BL), 0.36)
CELL = {}
for m_, f_, ua, ub, rms, tA, tB, grp, ltA, ltB, bn, tail in re.findall(
        r"^\s+([\d.]+) ([\d.]+): ([\d.]+)/([\d.]+) ([\d.]+) ([+-][\d.]+)/([+-][\d.]+) ([+-][\d.]+) ([+-][\d.]+)/([+-][\d.]+) \[(.*?)\] (.*)$", T["nr4"], re.M):
    CELL[(float(m_), float(f_))] = dict(ua=float(ua), ub=float(ub), rms=float(rms), tA=float(tA), tB=float(tB), z=float(grp), ltA=float(ltA), ltB=float(ltB),
                                        bins=[float(v) for v in bn.split(",")], gates=re.findall(r"'(\w+)'", tail), clears=tail.startswith("CLEARS"))
assert len(CELL) == 36
c87 = CELL[(1.0, 0.87)]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 5), gridspec_kw=dict(wspace=0.26))
for y, lab, c, mk in ((QL, "live zoom, gravity only", ms.DATA, "o"), (QB, "Blumenthal", BAD, "s"), (QG, "Gnedin", "#7a5195", "^")):
    a1.plot(RD, y, mk + "-", color=c, label=lab, ms=5)
a1.axvspan(2, 4, color=SOFT, zorder=0)
a1.text(3, 3.55, "f_Q read here", ha="center", fontsize=8.5, color=ms.MUTED)
a1.axhline(1, color=ms.MUTED, ls="--", lw=1)
a1.set_xlabel("r / R_d, disc grown in a 10¹² zoom, z = 0"); a1.set_ylabel("Q, cold mass with disc / without")
a1.legend(fontsize=8.5, loc="center right")
a1.text(10, 3.05, f"f_Q {fq:.3f} [{fql:.2f}, {fqh:.2f}]\nline 0.8", ha="right", fontsize=9.5)
a2.axhspan(0.50, 0.80, color=SOFT, zorder=0)
a2.plot(range(6), [OFF["sparc"][A]["bins"][b] for b in BINS], "o-", color=ms.MUTED, label=f"no response, Υ {UA(OFF):.2f}")
a2.plot(range(6), c87["bins"], "^-", color="#7a5195", label=f"f 0.87, Υ {c87['ua']:.2f} / {c87['ub']:.2f}")
a2.plot(range(6), [BL["sparc"][A]["bins"][b] for b in BINS], "s-", color=BAD, label=f"f 1, Blumenthal, Υ {UA(BL):.2f} / {UB(BL):.2f}")
a2.axhline(0.30, color=ms.MUTED, ls=":", lw=1); a2.text(-0.2, 0.255, "grid floor 0.30", fontsize=8, color=ms.MUTED)
a2.set_xticks(range(6), X_LAB, fontsize=8); a2.set_ylim(0.2, 1.3)
a2.set_xlabel("V_flat bin, km/s"); a2.set_ylabel("Υ in bin (A); shaded window 0.50–0.80"); a2.legend(fontsize=8.5, loc="upper right")
ms.finish(fig, "c6_06_live_contraction", "FAIL", "Live contraction", f"FAILS. Gravity contracts as Blumenthal says (f_Q {fq:.3f}); with it on, EM1 reads Υ {UA(BL):.2f} / {UB(BL):.2f}, off the line",
          "LC1_live_contraction/lc1.out; NR3_ur1_on_nr2/nr3_MEDIAN_results.json; NR4_low_mass_requirement/nr4.out")
add("c6_06_live_contraction", "Live contraction", "FAIL", f"f_Q {fq:.3f}; EM1 + Blumenthal Υ {UA(BL):.2f} / {UB(BL):.2f}.", ["LC1", "NR3", "NR4"],
    "A disc grown in a live zoom at 10¹² solar masses, nine same-seed pairs with and without the disc, Newtonian, gravity only, no feedback, one mass. Then SPARC's line with the response on, on version N's inputs.",
    "Left: the measured contraction Q with radius against the Blumenthal and Gnedin formulas, with the band where f_Q is read. Right: Υ by V_flat with no response, at the measured strength f 0.87, and at full Blumenthal.",
    f"LC1's frozen grade is a success of the test, STRONG and BLUMENTHAL HOLDS: the cold fluid contracts about as the formula says. This dish is red because of what that does to SPARC: EM1 + Blumenthal reads Υ {UA(BL):.2f} / {UB(BL):.2f}, and at the map cell nearest the measured strength, f 0.87, {c87['ua']:.2f} / {c87['ub']:.2f}, both off the 0.50 line. NR3's label is SIGN FLIP YES, AMPLITUDE FAILS [NOISE-LIMITED]. The 150–250 km/s bins sit at 0.30–0.39 whatever the low-mass η does, so low-mass η can't close it. Feedback isn't in this test, and it says what gravity alone does: that's the wall a mechanism would have to overcome.",
    [("f_Q, z = 0", f"{fq:.3f} [{fql:.2f}, {fqh:.2f}]", "lc1"), ("EM1 + Blumenthal, Υ", f"{UA(BL):.2f} / {UB(BL):.2f}", "nr3"), ("m 1, f 0.87, Υ", f"{c87['ua']:.2f} / {c87['ub']:.2f}", "nr4"), ("NR3 verdict", J["nr3s"]["verdict"], "nr3s")],
    ["lc1", "lc1r", "nr3", "nr3s", "nr3r", "nr4"])

# ---------------------------------------------------------------- 7 Requirement map
assert J["nr4j"]["verdict"] == "NOT DECIDED" and J["nr4j"]["clear"] == [[1.5, 0]]
assert [k for k, v in CELL.items() if v["clears"]] == [(1.5, 0.0)]
ms_, fs_ = sorted({k[0] for k in CELL}), sorted({k[1] for k in CELL})
mc = re.search(r"lowest m needs eta ([\d.]+), ([\d.]+) vs seed max ([\d.]+), ([\d.]+)", T["nr4"])
e10, e11, s10, s11 = (float(mc.group(i)) for i in range(1, 5))
K2K3 = re.search(r"K2 (\S+) K3 (\S+);", T["nr4"]).groups()
assert "only for m >= 1" in re.sub(r"≥", ">=", T["nr4r"]) or "m ≥ 1" in T["nr4r"]
AB = {"line": "Υ", "tilt": "tilt", "lt": "LT"}
fig, ax = plt.subplots(figsize=(9, 5.8))
G = np.array([[len(CELL[(m, f)]["gates"]) for f in fs_] for m in ms_])
for i, m in enumerate(ms_):
    for j, f in enumerate(fs_):
        c = CELL[(m, f)]
        col = "#cfe6d8" if c["clears"] else {1: "#eceff1", 2: "#d9dee2", 3: "#c3cad0"}[len(c["gates"])]
        ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor=col, edgecolor="white", lw=1.5))
        ax.text(j + 0.5, i + 0.62, f'{c["ua"]:.2f}', ha="center", va="center", fontsize=11, weight="bold" if c["clears"] else "normal", color=ms.INK)
        ax.text(j + 0.5, i + 0.27, "clears SPARC side" if c["clears"] else "fails " + ", ".join(AB[g] for g in c["gates"]), ha="center", va="center", fontsize=6.8, color=ms.INK if c["clears"] else ms.MUTED)
ax.add_patch(plt.Rectangle((fs_.index(0.87), 0), 1, 6, fill=False, edgecolor=ms.INK, lw=1.5, ls="--"))
ax.text(fs_.index(0.87) + 0.5, 6.12, "LC1 measured f_Q 0.87", ha="center", fontsize=8, color=ms.INK)
ax.set_xlim(0, 6); ax.set_ylim(0, 6); ax.grid(False)
ax.set_xticks(np.arange(6) + 0.5, [f"{f:g}" for f in fs_]); ax.set_yticks(np.arange(6) + 0.5, [f"{m:g}" for m in ms_])
ax.tick_params(length=0)
ax.set_xlabel("f, net response strength, FITTED"); ax.set_ylabel("m, low-mass η multiplier, FITTED (m < 1 not mapped)")
fig.subplots_adjust(top=0.76, left=0.09, right=0.98)
ms.finish(fig, "c6_07_requirement_map", "OPEN", "The requirement map", "NOT DECIDED as frozen. One cell of 36 clears the SPARC side, η above every seed; only m ≥ 1 is mapped", "NR4_low_mass_requirement/nr4.out, nr4_results.json, README.md")
add("c6_07_requirement_map", "The requirement map", "OPEN", "NOT DECIDED as frozen; one cell of 36 clears, η above every seed. Only m ≥ 1 mapped.", ["NR4", "NR3"],
    "A grid of 36 cells on SPARC, groups and LITTLE THINGS: m multiplies the low-mass η, f scales the response. Both are FITTED: this is a requirement map, never a rule.",
    "A heat map, m by f: each cell shows Υ (background A) and which gates it fails. Darker is more gates failed; the green cell clears the SPARC side. The dashed column is LC1's measured strength.",
    f"The label is NOT DECIDED because frozen checks K2 and K3 missed 1e-6, at {K2K3[0]} and {K2K3[1]}, so grey is the right colour. Read as a map, the one clearing cell is no net response with η × 1.5, which needs η(10¹⁰), η(10¹¹) of {e10} and {e11}, above every seed ({s10}, {s11}). Audit note: the grid starts at m 1, so 'no m reaches 0.50 at f 0.87' holds only for m ≥ 1; NR3's LOW, about m 0.67 / 0.60 at f 1, reads Υ {UA(LO['EM1|blum']):.2f} / {UB(LO['EM1|blum']):.2f} and fails tilt and LITTLE THINGS there. One cell on a 6 by 6 grid isn't a measured region, and it doesn't address clusters.",
    [("verdict; clearing cells", f"{J['nr4j']['verdict']}; m 1.5, f 0", "nr4j"), ("K2, K3", f"{K2K3[0]}, {K2K3[1]}", "nr4"), ("η needed vs seed max", f"{e10}, {e11} vs {s10}, {s11}", "nr4"), ("m 1, f 0.87, Υ", f"{c87['ua']:.2f} / {c87['ub']:.2f}", "nr4")],
    ["nr4", "nr4j", "nr4r", "nr3l"])

# ---------------------------------------------------------------- 8 Doors
d1 = J["dr1"]["sparc"]["R1|c1"]["canonical"]
d3 = J["dr3"]["runs"]["DR3|blum"]["sparc"][A]
d7 = J["dr7"]["rows"]["EM1|blum|cap"]["sparc"][A]
d9 = J["dr9"]["rows"]
cp = J["cp1"]["primary"]["R1"]["sparc"][A]
near(d1["U"], 0.41); near(d3["U"], 0.33); near(d7["U"], 0.41); near(d9["RET_FIT"]["U"][0], 0.70); near(cp["U"], 0.43)
assert J["dr3s"]["labels"]["blum"] == "NOT HALVED, MOVES" and J["dr7s"]["verdict"] == "BITES, FAILS [NOISE-LIMITED]"
assert J["dr9"]["verdict"] == "FAILS AT ALL THREE" and J["cp1s"]["verdict"].startswith("NOT DECIDED") and not J["cp1s"]["checks"]["K4"]
near(J["dr9"]["mutate_frozen_dU"], 0.02, 1e-6)
assert "SPARC BREAKS, CLUSTERS NOT REACHED" in T["dr1r"] and "NOT DECIDED" in T["dr9a"]
door = [("DR1 density term, R1 c1", d1["U"], "SPARC BREAKS, CLUSTERS NOT REACHED", d1["tilt"], BAD),
        ("DR3 disc monopole, Blumenthal", d3["U"], "NOT HALVED, MOVES", d3["tilt"], BAD),
        ("DR7 phase-space cap", d7["U"], "BITES, FAILS [NOISE-LIMITED]", d7["tilt"], BAD),
        ("DR9 coupling, C from CM1", d9["RET_CM1"]["U"][0], "FAILS AT ALL THREE; strictly NOT DECIDED", d9["RET_CM1"]["tilt"][0], BAD),
        ("DR9 coupling, C ceiling 1", d9["RET_C1"]["U"][0], "same lane; undoes the response, tilt, LT fail", d9["RET_C1"]["tilt"][0], "#d98a80"),
        ("DR9 coupling, C FITTED", d9["RET_FIT"]["U"][0], "same lane; fitted, tilt, LT fail", d9["RET_FIT"]["tilt"][0], "#d98a80"),
        ("CP1 mix, R1", cp["U"], "NOT DECIDED; galaxies fail Υ", cp["tilt"], ms.STATUS["UNDEC"])]
fig, ax = plt.subplots(figsize=(10, 5.4))
ax.axvspan(0.50, 0.80, color=SOFT, zorder=0)
ax.axvline(0.50, color=ms.INK, lw=1.2)
ax.axvline(UA(BL), color=ms.MUTED, ls=":", lw=1.2)
ax.text(UA(BL) - 0.004, 6.62, f"EM1 + Blumenthal {UA(BL):.2f}", ha="right", fontsize=8, color=ms.MUTED)
ax.text(0.505, 6.62, "0.50 line", fontsize=8, color=ms.INK)
for i, (lab, u, verd, tilt, c) in enumerate(door[::-1]):
    ax.plot(u, i, "o", ms=10, color=c, zorder=3)
    ax.text(0.86, i, f"Υ {u:.2f}, tilt {tilt:+.2f}\n{verd}", va="center", fontsize=8)
ax.set_yticks(range(len(door)), [d[0] for d in door[::-1]], fontsize=9)
ax.set_xlim(0.25, 1.32); ax.set_ylim(-0.6, 6.95); ax.set_xticks(np.arange(0.3, 0.81, 0.1))
ax.set_xlabel("Υ reached, SPARC sample median, canonical, background A; shaded window 0.50–0.80")
fig.subplots_adjust(left=0.24, right=0.99)
ms.finish(fig, "c6_08_doors_today", "FAIL", "The doors tried today", "FAILS. No graded row clears Υ, tilt and LITTLE THINGS; DR9 reaches the line only where they fail",
          "dr1_offline.json; dr3_PRIMARY_results.json; dr7_MEDIAN_results.json; dr9_results.json; cp1_MEDIAN_results.json")
add("c6_08_doors_today", "The doors tried today", "FAIL", f"Υ reached: DR1 {d1['U']:.2f}, DR3 {d3['U']:.2f}, DR7 {d7['U']:.2f}, CP1 {cp['U']:.2f}; DR9 {d9['RET_FIT']['U'][0]:.2f} only with its C large, tilt fails.", ["DR1", "DR3", "DR7", "DR9", "CP1"],
    "Five of the doors tried on 1 November, each graded on SPARC by its own frozen criteria, each read from its own result files. DR1 is a density term on the law, with no cold dark energy at all; the other four sit on version N's path. CP1 breaks the rule that a0 stays out of the cold sector, on purpose.",
    "Each door's sample median Υ against the 0.50 line and the window, with the lane's own label and tilt beside it. DR9 takes three rows, for its three normalisations of C. The dotted line is the contracted baseline, EM1 + Blumenthal.",
    f"Every door's primary row stays below 0.50 except DR9's. DR9's frozen rows read {d9['RET_CM1']['U'][0]:.2f} with C from the measured channel, {d9['RET_FIT']['U'][0]:.2f} with C FITTED ({J['dr9']['constants']['RET_FIT']/J['dr9']['constants']['RET_CM1']:.1f} × that channel) and {d9['RET_C1']['U'][0]:.2f} at the ceiling C = 1, and every row on the line fails tilt (+{d9['RET_FIT']['tilt'][0]:.2f} / +{d9['RET_FIT']['tilt'][1]:.2f} at the fitted one) and LITTLE THINGS. Its label is FAILS AT ALL THREE, but its frozen mutation check missed, moving Υ exactly 0.02 against 'more than 0.02', and the replacement check was written after the rows were seen, so strictly that run is NOT DECIDED. CP1 is NOT DECIDED because K4 failed; inside it galaxies fail on Υ {cp['U']:.2f}, while a report-only reading, R2, passes the galaxy block on canonical at 0.53 by counting the cold at weight χ²_clust, matches no source term and fails on alt at 0.45. The chip is red for the set: nothing here clears, and the two NOT DECIDED rows are labelled as that, not as fails.",
    [("DR1 R1 c1", f"Υ {d1['U']:.2f}, tilt {d1['tilt']:+.2f}", "dr1"), ("DR3 Blumenthal", f"Υ {d3['U']:.2f}, tilt {d3['tilt']:+.2f}", "dr3"), ("DR7 cap", f"Υ {d7['U']:.2f}, tilt {d7['tilt']:+.2f}", "dr7"),
     ("DR9 C_CM1, C 1, C_FIT", f"Υ {d9['RET_CM1']['U'][0]:.2f}, {d9['RET_C1']['U'][0]:.2f}, {d9['RET_FIT']['U'][0]:.2f}", "dr9"), ("DR9 frozen MUTATE ΔΥ", f"{J['dr9']['mutate_frozen_dU']:.2f}, missed", "dr9"), ("CP1 R1", f"Υ {cp['U']:.2f}, tilt {cp['tilt']:+.2f}", "cp1")],
    ["dr1", "dr1r", "dr3", "dr3s", "dr3r", "dr7", "dr7s", "dr7r", "dr9", "dr9a", "dr9r", "cp1", "cp1s", "cp1o", "cp1r"])

# ---------------------------------------------------------------- 9 Law, comparison
lc, la = J["dr1"]["sparc"]["R1|c0"]["canonical"], J["dr1"]["sparc"]["R1|c0"]["alt"]
xc, xa = J["dr1"]["xcop"]["R1|c0"]["canonical"], J["dr1"]["xcop"]["R1|c0"]["alt"]
gc, ga = J["dr1g"]["R1|c0|canonical"], J["dr1g"]["R1|c0|alt"]
near(lc["rms"], 0.054, 0.0005); near(lc["U"], 0.52); near(lc["tilt"], 0.02)
panels = [("Υ", lc["U"], la["U"], (0.50, 0.80), (0.3, 0.9)), ("rms, dex", lc["rms"], la["rms"], (0, 0.110), (0, 0.13)), ("|tilt|", abs(lc["tilt"]), abs(la["tilt"]), (0, 0.15), (0, 0.2)),
          ("X-COP |mean|, dex", abs(xc["mean"]), abs(xa["mean"]), (0, 0.05), (0, 0.55)), ("G-OUT-M3 Z", gc["Z"]["h0672"]["G-OUT-M3"], ga["Z"]["h0672"]["G-OUT-M3"], (0, 2), (0, 6))]
fig, axs = plt.subplots(1, 5, figsize=(10, 4.4), gridspec_kw=dict(wspace=0.62))
for ax, (lab, c_, a_, (lo, hi), yl) in zip(axs, panels):
    ax.axhspan(lo, hi, color=SOFT, zorder=0)
    for x, v, m_ in ((0, c_, "o"), (1, a_, "s")):
        ax.plot(x, v, m_, ms=9, color=OK if lo <= v <= hi else BAD, zorder=3)
        ax.annotate(f"{v:.2f}" if lab != "rms, dex" else f"{v:.3f}", (x, v), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=8.5)
    ax.set_xticks([0, 1], ["can.", "alt"]); ax.set_xlim(-0.6, 1.6); ax.set_ylim(*yl); ax.set_title(lab, fontsize=9.5)
    ax.grid(False)
    if lab == "|tilt|":
        ax.set_yticks([0, 0.05, 0.10, 0.15, 0.20])
fig.subplots_adjust(left=0.05, right=0.99)
ms.finish(fig, "c6_09_law_comparison", "COND", "The law on the same gates (comparison dish, not route E)", f"COMPARISON, CONDITIONAL. rms {lc['rms']:.3f}, Υ {lc['U']:.2f}, tilt {lc['tilt']:+.2f} on canonical; clusters fail",
          "DR1_density_term_law/dr1_offline.json, dr1_g005_f034.json (baseline R1 c0)")
add("c6_09_law_comparison", "The law on the same gates (comparison dish, not route E)", "COND", f"Comparison, not route E: rms {lc['rms']:.3f}, Υ {lc['U']:.2f}, tilt {lc['tilt']:+.2f}, clusters fail.", ["DR1"],
    "The plain a0 law with no halo and no cold dark energy, DR1's baseline row (c = 0): SPARC, X-COP and the 15 keys on gas +0.005, f★ 0.034. κ = ½ is FITTED. The two footings aren't pooled.",
    "Five small panels, each with the gate's window shaded: Υ, rms, tilt, X-COP's mean, and the worst heavy-cluster key, on the canonical (circle) and alt (square) footing.",
    f"This dish is here for reference only, so route E's dishes can be read against the same gates; it's a different theory path, not a result of route E, and nothing here says the data favour either. On the canonical footing the law's SPARC gates hold; on alt its Υ {la['U']:.2f} falls under 0.50. Clusters fail on both: X-COP {xc['mean']:+.3f}, {xc['rms']:.3f}, and {gc['n']} of 15 keys with G-OUT-M3 {gc['Z']['h0672']['G-OUT-M3']:+.2f}. Groups read Z {gc['groups']['Z']:+.2f}.",
    [("canonical rms, Υ, tilt", f"{lc['rms']:.4f}, {lc['U']:.2f}, {lc['tilt']:+.2f}", "dr1"), ("alt rms, Υ, tilt", f"{la['rms']:.4f}, {la['U']:.2f}, {la['tilt']:+.2f}", "dr1"), ("X-COP canonical", f"{xc['mean']:+.3f}, {xc['rms']:.3f}", "dr1"), ("keys, G-OUT-M3", f"{gc['n']} of 15, {gc['Z']['h0672']['G-OUT-M3']:+.2f}", "dr1g")],
    ["dr1", "dr1g", "dr1r"])

(HERE / "captions" / "col6.json").write_text(json.dumps(CAP, ensure_ascii=False, indent=1) + "\n")
(HERE / "board_tiles_route_e.json").write_text(json.dumps(dict(course="Tonight's specials", subtitle="Route E, version N, as of 1 November 2026", tiles=TILES), ensure_ascii=False, indent=1) + "\n")
print(len(CAP), "dishes:", [(c["slug"], c["status"]) for c in CAP])
