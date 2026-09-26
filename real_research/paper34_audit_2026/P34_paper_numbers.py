#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
P34 -- EVERY NUMBER PAPER34 QUOTES, RE-DERIVED FROM THE COMMITTED LANE OUTPUTS.

PAPER34 ("A dark sector the MOND kernel cannot see", qwen_claude_field_theory/papers_2026/PAPER34_kernel_blind_dark_sector_2026.tex)
reports lanes L353-L364, L370-L372 and GP0-GP4.  This script reads each lane's committed results JSON (and, where a number
is printed but not stored, the lane's committed .out) and compares every quoted value with the paper's, at the paper's own
precision (half a unit in the last quoted digit).  Nothing is re-simulated here; the lanes themselves are re-run separately.

It also derives the three numbers the paper adds to the record:
  X1  the KiDS-1000 score of GP4's two window cells against GP2's REALISABLE floor (the best isolated QUMOND lens in one
      uniform external field, given the same freedom in the dark component's surviving halo).  GP2's committed tables give
      the base, the floor and the comparator; GP4's give the cells' scores against L352's acceptance (isolated MOND with a
      free two-halo term).  The repository's summary of GP4 said "about +8" above the floor; the tables give +19 to +21.5.
  X4  the strict S8 floor.  KiDS-Legacy is 0.815 +0.016/-0.021; the lanes took 0.016 as the error (floor 0.767).  With the
      lower error the 3-sigma floor is 0.752, GP4's window cells pass it, and the strict set is then blocked by the forest alone.
  X5  the forest thresholds as thermal-relic masses, with L319's own transfer function, cosmology and k grid.

MUTATE=1 reads the floor the way that summary did -- as the floor's own distance from the Gauss-forbidden comparator,
+8.2/+8.3 -- instead of the floor with the same halo freedom.  X1 must then FAIL (rc = 1).

Run from anywhere:  python3 real_research/paper34_audit_2026/P34_paper_numbers.py      (ROOT=<checkout> audits another checkout)
"""
import os, sys, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("ROOT", os.path.abspath(os.path.join(HERE, "..", "..")))
RR = os.path.join(ROOT, "real_research")
MUTATE = os.environ.get("MUTATE", "0") == "1"
CH, OUT = [], {"lane": "P34", "mutate": MUTATE, "root": "ROOT" if "ROOT" in os.environ else "repo", "checks": {}}


def J(rel):
    return json.load(open(os.path.join(RR, rel)))


def N(rel):
    return J(rel)["numbers"]


def TXT(rel):
    return open(os.path.join(RR, rel)).read()


def near(x, stated, dec):
    """x rounds to the paper's stated value at `dec` decimals (half a unit in the last quoted digit)."""
    return abs(float(x) - float(stated)) <= 0.5 * 10 ** (-dec) + 1e-12


def sci(x, stated):
    """x agrees with a value the paper quotes in scientific notation to its two significant figures."""
    m = float(f"{float(stated):.1e}".split("e")[0])
    e = int(f"{float(stated):.1e}".split("e")[1])
    return abs(float(x) / 10 ** e - m) <= 0.05 + 1e-12


ROWS = []


def row(section, label, computed, stated, ok):
    ROWS.append((section, label, computed, stated, bool(ok)))


def check(name, ok, measured, load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}", flush=True)


def banner(t):
    print("\n" + "=" * 118 + f"\n{t}\n" + "=" * 118, flush=True)


print(__doc__.split("\n\n")[1].strip() if False else "P34 -- every number PAPER34 quotes, re-derived from the committed lane outputs")
if MUTATE:
    print("  *** MUTATE=1: the floor is read as the floor's distance from the comparator (the summary's '+8'); X1 must FAIL ***")
print(f"  auditing: {'ROOT=' + ROOT if 'ROOT' in os.environ else 'this checkout'}")

# ------------------------------------------------------------------------------------------------------------ L353
s = "L353"
n = N("g03_audit_2026/L353_kernel_invisible_dark_component_results.json")
tb = {int(r[0]): r[1] for r in n["N2"]["two_body"]}
row(s, "additive force ratio at 2 r_M", tb[2], 2.54, near(tb[2], 2.54, 2))
row(s, "additive force ratio at 10 r_M", tb[10], 10.5, near(tb[10], 10.5, 1))
row(s, "additive force ratio at 100 r_M", tb[100], 100.5, near(tb[100], 100.5, 1))
row(s, "pair force ratio (all radii) = 1", max(abs(r[2] - 1) for r in n["N2"]["two_body"]), 0.0, max(abs(r[2] - 1) for r in n["N2"]["two_body"]) < 1e-12)
row(s, "numerical residuals < 1e-14", max(n["N1"]["numeric"]["dev_kernel_arg"], n["N1"]["numeric"]["dev_dark"]), 1e-14,
    max(n["N1"]["numeric"]["dev_kernel_arg"], n["N1"]["numeric"]["dev_dark"]) < 1e-14)
row(s, "leak into kernel argument", n["N3"]["leak"], "alpha_c/2", n["N3"]["leak"] == "alpha_c/2")
row(s, "X-COP dark mass / baryons at R500 (median)", n["N4"]["median_dark_over_baryons"], 2.31, near(n["N4"]["median_dark_over_baryons"], 2.31, 2))
wep = [r[2] for r in n["N4"]["xcop_wep"]]
row(s, "dark component feels less acceleration (median, %)", 100 * n["N4"]["median_wep"], 47, near(100 * n["N4"]["median_wep"], 47, 0))
row(s, "... range low (%)", 100 * min(wep), 37, near(100 * min(wep), 37, 0))
row(s, "... range high (%)", 100 * max(wep), 53, near(100 * max(wep), 53, 0))
row(s, "MW unboosted allowance / M_b(6e10)", n["N4"]["MW_unboosted_allowance_Msun"] / 6e10, 0.49, near(n["N4"]["MW_unboosted_allowance_Msun"] / 6e10, 0.49, 2))
t = TXT("g03_audit_2026/L353_kernel_invisible_dark_component.out")
row(s, "universal coupling allows ~1/nu = 0.25 of it", "1/nu = 0.25" in t, True, "1/nu = 0.25" in t)

# ------------------------------------------------------------------------------------------------------------ L354
s = "L354"
n = N("dark_sector_2026/L354_carrier_lagrangian_additive_window_results.json")
strict = {tuple(c) for c in n["W1"]["window"]["strict"]}
row(s, "strict cells", sorted(strict), "{(can,0.8,1400),(can,0.9,1200),(alt,0.8,1400)}",
    strict == {("canonical", 0.8, 1400.0), ("canonical", 0.9, 1200.0), ("alt", 0.8, 1400.0)})
row(s, "alternative cells", len(n["W1"]["window"]["alt"]), 14, len(n["W1"]["window"]["alt"]) == 14)
tab = n["W1"]["table"]
def xrow(key, vk):
    return [r for r in tab[key] if r["vk"] == vk][0]
for key, vk, raw, nt in [("canonical_0.8", 1400.0, 1.13, 1.06), ("canonical_0.9", 1200.0, 1.19, 1.11), ("alt_0.8", 1400.0, 1.18, 1.11)]:
    r = xrow(key, vk)
    row(s, f"X-COP {key} {vk:.0f} raw", r["ratio"], raw, near(r["ratio"], raw, 2))
    row(s, f"X-COP {key} {vk:.0f} non-thermal", r["ratio_nt"], nt, near(r["ratio_nt"], nt, 2))
row(s, "S8 (0.8, 1400)", n["S8"]["0.8_1400"], 0.773, near(n["S8"]["0.8_1400"], 0.773, 3))
row(s, "S8 (0.9, 1200)", n["S8"]["0.9_1200"], 0.774, near(n["S8"]["0.9_1200"], 0.774, 3))
t = TXT("dark_sector_2026/L354_carrier_lagrangian_additive_window.out")
t = t[t.index("W1  THE WINDOW"):]                                   # the Newtonian-orbit scan, not the C1 (additive) control
for foot, fd, vk, gal in [("canonical", "0.8", "1400", "+0.022"), ("canonical", "0.9", "1200", "+0.010"), ("alt", "0.8", "1400", "+0.020")]:
    m = re.search(rf"candidate {foot} f_d {fd} v_k {vk}: .*?galaxies max ([+-][0-9.]+) dex -> WINDOW", t)
    row(s, f"galaxies {foot} {fd} {vk}", m.group(1) if m else None, gal, bool(m) and m.group(1) == gal)
c2 = [r for r in n["C2"] if r["vk"] == 1500.0][0]
row(s, "cluster retention at 1500 km/s, Newtonian", c2["cluster_newtonian"], 0.53, near(c2["cluster_newtonian"], 0.53, 2))
row(s, "cluster retention at 1500 km/s, additive", c2["cluster_additive"], 0.77, near(c2["cluster_additive"], 0.77, 2))
l364 = N("g03_audit_2026/L364_replacement_carrier_cosmic_shear_results.json")
def fo364(fd, vk):
    r = [x for x in l364["scan"] if x["fd"] == fd and x["vk"] == vk][0]
    return min(r["t2"], r["t3"])
row(s, "forest T^2 (L364) for (0.8, 1400): strict", fo364(0.8, 1400.0), 0.9954, near(fo364(0.8, 1400.0), 0.9954, 4) and fo364(0.8, 1400.0) >= 0.9952)
row(s, "forest T^2 (L364) for (0.9, 1200): loose only", fo364(0.9, 1200.0), 0.9936, near(fo364(0.9, 1200.0), 0.9936, 4) and 0.9 <= fo364(0.9, 1200.0) < 0.9952)

# ------------------------------------------------------------------------------------------------------------ L355
s = "L355"
n = N("g03_audit_2026/L355_kernel_invisible_kids_results.json")
k2c, k2a = n["K2"]["canonical/linear-theory (16 Mpc)"], n["K2"]["alt/linear-theory (16 Mpc)"]
row(s, "KiDS, baryons-only kernel, canonical", k2c, 233, near(k2c, 233, 0))
row(s, "KiDS, baryons-only kernel, alt", k2a, 241, near(k2a, 241, 0))
k3 = list(n["reading"]["k3_own"].values())
row(s, "with halo + 2-halo, low", min(k3), 120, near(min(k3), 120, 0))
row(s, "with halo + 2-halo, high", max(k3), 145, near(max(k3), 145, 0))
t = TXT("g03_audit_2026/L355_kernel_invisible_kids.out")
rms = {f: float(re.search(rf"{f}\s+linear-theory \(16 Mpc\)\s+: kernel field rms ([0-9.]+) a0", t).group(1)) for f in ("canonical", "alt")}
row(s, "web baryonic field rms, canonical (1e-3 a0)", 1e3 * rms["canonical"], 2.1, near(1e3 * rms["canonical"], 2.1, 1))
row(s, "web baryonic field rms, alt (1e-3 a0)", 1e3 * rms["alt"], 1.7, near(1e3 * rms["alt"], 1.7, 1))
quiet = {f: float(re.search(rf"{f}\s+Brouwer\+21 quiet \(e = 0.003 a0\) : kernel field rms ([0-9.]+) a0", t).group(1)) for f in ("canonical", "alt")}
e7 = [v for k, v in J("switch_audit_2026/BS2_efe_vs_switch_results.json")["checks"].items() if k.startswith("E7")][0]["measured"]
bound = {f: float(re.search(rf"'{f}': 'e <= ([0-9.e-]+)'", e7).group(1)) for f in ("canonical", "alt")}
row(s, "KiDS single-field bound (BS2 E7), canonical/alt", (bound["canonical"], bound["alt"]), (7.2e-5, 5.2e-5), sci(bound["canonical"], 7.2e-5) and sci(bound["alt"], 5.2e-5))
lin = [rms[f] / bound[f] for f in ("canonical", "alt")]
qui = [quiet[f] / bound[f] for f in ("canonical", "alt")]
row(s, "times the bound, linear-theory web", f"{min(lin):.1f}-{max(lin):.1f}", "28-33", near(min(lin), 28, 0) and near(max(lin), 33, 0))
row(s, "times the bound, Brouwer's quiet field", f"{min(qui):.1f}-{max(qui):.1f}", "11-13", near(min(qui), 11, 0) and near(max(qui), 13, 0))

# ------------------------------------------------------------------------------------------------------------ L356
s = "L356"
n = N("dark_sector_2026/L356_construction_highz_price_results.json")
sl = [r["construction"]["slope"] for r in n["H2"]["rows"]]
fd = [r["construction"]["median_fdm"] for r in n["H2"]["rows"]]
row(s, "RC100 inverted slope low", min(sl), 0.090, near(min(sl), 0.090, 3))
row(s, "RC100 inverted slope high", max(sl), 0.120, near(max(sl), 0.120, 3))
row(s, "RC100 f_DM low", min(fd), 0.48, near(min(fd), 0.48, 2))
row(s, "RC100 f_DM high", max(fd), 0.58, near(max(fd), 0.58, 2))
dz = [r["dzp_dex"] for r in n["H3"]]
row(s, "flagship shift low (dex)", min(dz), 0.82, near(min(dz), 0.82, 2))
row(s, "flagship shift high (dex)", max(dz), 1.05, near(max(dz), 1.05, 2))
row(s, "flagship shift, rounded range (dex)", f"{min(dz):.1f}..{max(dz):.1f}", "0.8..1.0", near(min(dz), 0.8, 1) and near(max(dz), 1.0, 1))
t = TXT("dark_sector_2026/L356_construction_highz_price.out")
m = re.search(r"data slope ([-0-9.]+) \+/- ([0-9.]+); r\(z=1, 2, 2.5\) = ([0-9.]+), ([0-9.]+), ([0-9.]+)", t)
row(s, "RC100 data slope", m.group(1) + " +/- " + m.group(2), "-0.112 +/- 0.062", m.group(1) == "-0.112" and m.group(2) == "0.062")
row(s, "survival at z = 2.5", m.group(5), 0.999, m.group(5) == "0.999")
row(s, "converted by z = 2 (%)", 100 * (1 - float(m.group(4))), 0.3, near(100 * (1 - float(m.group(4))), 0.3, 1))
src = TXT("dark_sector_2026/L320_carrier_highz_price_rc100.py")
row(s, "survival fractions are the f_d(0) = 0.8 cell", "p = 2, f_d(0) = 0.8" in src, True, "(p = 2, f_d(0) = 0.8)" in src)

# ------------------------------------------------------------------------------------------------------------ L357
s = "L357"
n = N("dark_sector_2026/L357_virialization_triggered_carrier_results.json")
mins = []
for k, v in n["V1"].items():
    mins.append(min(v["t2"], v["t3"]))
    mins.append(min(v["t2_br"], v["t3_br"]))
row(s, "plain trigger: min_z T^2(k=5), low", min(mins), 0.23, near(min(mins), 0.23, 2))
row(s, "plain trigger: min_z T^2(k=5), high", max(mins), 0.57, near(max(mins), 0.57, 2))
row(s, "all minima at z = 2", all(min(v["t2"], v["t3"]) == v["t2"] and min(v["t2_br"], v["t3_br"]) == v["t2_br"] for v in n["V1"].values()), True,
    all(min(v["t2"], v["t3"]) == v["t2"] and min(v["t2_br"], v["t3_br"]) == v["t2_br"] for v in n["V1"].values()))
row(s, "collapsed bias-weighted fraction z = 3 (about half)", n["controls"]["B_z3"], 0.46, near(n["controls"]["B_z3"], 0.46, 2))
g = n["V2"]["galaxies_at_strict_floor"]["cap"]
row(s, "galaxy gate at the strict-forest floor (dex)", max(g["canonical"]["Milky Way"], g["alt"]["Milky Way"]), 0.2, near(max(g["canonical"]["Milky Way"], g["alt"]["Milky Way"]), 0.2, 1))
loose = [r for r in n["D1"] if r["p"] == 0.0 and min(r["t2"], r["t3"]) >= 0.9]
lx = min(min(r["xcop"]["canonical"], r["xcop"]["alt"]) for r in loose)
row(s, "plain trigger at the loose floor: X-COP >= 1.32", lx, 1.32, near(lx, 1.32, 2) and len(loose) > 0)
rc = n["H1"]["rc100"]
row(s, "best gated cell RC100 f_DM", rc["median_fdm"], 0.43, near(rc["median_fdm"], 0.43, 2))
row(s, "best gated cell RC100 slope", rc["slope"], 0.44, near(rc["slope"], 0.44, 2))
row(s, "RC100 data slope, rounded", (round(rc["data_slope"], 2), round(rc["data_err"], 2)), (-0.11, 0.06), near(rc["data_slope"], -0.11, 2) and near(rc["data_err"], 0.06, 2))
row(s, "strict cells", len(n["D2"]["window"]["strict"]), 3, len(n["D2"]["window"]["strict"]) == 3)
row(s, "alternative cells", len(n["D2"]["window"]["alt"]), 17, len(n["D2"]["window"]["alt"]) == 17)
b = [r for r in n["D1"] if r["p"] == 2.0 and r["picture"] == "cleared" and r["x_v0"] == 2000.0 and r["v_k"] == 3000.0][0]
row(s, "best cell forest T^2 >= 0.998", min(b["t2"], b["t3"]), 0.998, min(b["t2"], b["t3"]) >= 0.998)
row(s, "best cell S8", b["S8"], 0.772, near(b["S8"], 0.772, 3))
row(s, "best cell X-COP canonical", b["xcop"]["canonical"], 1.08, near(b["xcop"]["canonical"], 1.08, 2))
row(s, "best cell X-COP alt", b["xcop"]["alt"], 1.13, near(b["xcop"]["alt"], 1.13, 2))
fl = [r["shift_dex"] for r in n["H1"]["flagship"]]
row(s, "gated cell flagship low (dex)", min(fl), 0.77, near(min(fl), 0.77, 2))
row(s, "gated cell flagship high (dex)", max(fl), 0.87, near(max(fl), 0.87, 2))
t = TXT("dark_sector_2026/L357_virialization_triggered_carrier.out")
row(s, "x~ ranges quoted (1e4-1e5; 200-350)", ("1e4-1e5" in t) and ("200-350" in t), True, ("1e4-1e5" in t) and ("200-350" in t))

# ------------------------------------------------------------------------------------------------------------ L358, L362
s = "L358/L362"
n = N("g03_audit_2026/L358_forest_kids_pincer_observable_results.json")
for xc, v in [("2.0", 0.185), ("2.5", 0.174), ("3.0", 0.160)]:
    row(s, f"forest worst at x_c = {xc}", n["worst"][xc], v, near(n["worst"][xc], v, 3))
n2 = N("g03_audit_2026/L362_forest_pincer_convergence_results.json")
row(s, "more particles (B)", n2["worst_x3"]["B"], 0.157, near(n2["worst_x3"]["B"], 0.157, 3))
row(s, "mesh twice as fine (C)", n2["worst_x3"]["C"], 0.191, near(n2["worst_x3"]["C"], 0.191, 3))
row(s, "resolution growth C / L358 fine", n2["worst_x3"]["C"] / n["resolution_x3"]["fine"], 1.2, near(n2["worst_x3"]["C"] / n["resolution_x3"]["fine"], 1.2, 1))
row(s, "50 Mpc/h box alone at x_c = 3", n["resolution_x3"]["coarse"], 0.096, near(n["resolution_x3"]["coarse"], 0.096, 3))

# ------------------------------------------------------------------------------------------------------------ L359
s = "L359"
n = N("g03_audit_2026/L359_vacuum_gated_switch_results.json")
win = [f"{c['p']}/{c['x_c0']}" for c in n["W1"]]
row(s, "window cells", len(win), 8, len(win) == 8)
gated = [k for k in n["K1"] if not k.startswith("0.0/")]
row(s, "gated cells scanned", len(gated), 9, len(gated) == 9)
row(s, "the ninth (2.0/2.5) fails KiDS", n["K1"]["2.0/2.5"]["ok"], False, n["K1"]["2.0/2.5"]["ok"] is False and "2.0/2.5" not in win)
kv = [n["K1"][k]["dchi2"][f] for k in win for f in ("canonical", "alt")]
row(s, "KiDS in the window, low", min(kv), -28.1, near(min(kv), -28.1, 1))
row(s, "KiDS in the window, high", max(kv), -1.0, near(max(kv), -1.0, 1))
fw = [n["F1"][k]["worst"] for k in win]
row(s, "forest worst in the window, low (%)", 100 * min(fw), 0.2, near(100 * min(fw), 0.2, 1))
row(s, "forest worst in the window, high (%)", 100 * max(fw), 8.5, near(100 * max(fw), 8.5, 1))
row(s, "p >= 1 worst (%)", 100 * max(n["F1"][k]["worst"] for k in win if not k.startswith("0.5")), 4.0,
    near(100 * max(n["F1"][k]["worst"] for k in win if not k.startswith("0.5")), 4.0, 1))
p05 = [n["F1"][k]["worst"] for k in win if k.startswith("0.5")]
row(s, "p = 0.5 worst low (%)", 100 * min(p05), 6.5, near(100 * min(p05), 6.5, 1))
row(s, "p = 0.5 worst high (%)", 100 * max(p05), 8.5, near(100 * max(p05), 8.5, 1))
ug = [n["F1"]["0.0/2.0"]["worst"], n["F1"]["0.0/3.0"]["worst"]]
row(s, "ungated forest (%) low", 100 * min(ug), 16, near(100 * min(ug), 16, 0))
row(s, "ungated forest (%) high", 100 * max(ug), 19, near(100 * max(ug), 19, 0))
sg = [v for k in win for v in n["G1"][k]["sigma8"].values() if True]
row(s, "sigma_8 (rms argument)", n["G1"]["1.0/1.5"]["sigma8"]["canonical/rms"], 0.810, near(n["G1"]["1.0/1.5"]["sigma8"]["canonical/rms"], 0.810, 3))
row(s, "every window cell within 2% of 0.811", max(abs(v / 0.811 - 1) for v in sg), 0.02, max(abs(v / 0.811 - 1) for v in sg) <= 0.02)

# ------------------------------------------------------------------------------------------------------------ L360
s = "L360"
n = N("g03_audit_2026/L360_assembled_construction_kids_results.json")
npass = sum(1 for v in n["M2"].values() if v["dchi2"]["canonical"] <= 4 and v["dchi2"]["alt"] <= 4)
row(s, "pairs passing both footings", f"{npass}/{len(n['M2'])}", "70/96", npass == 70 and len(n["M2"]) == 96)
ex = n["M2"]["1.0/1.5/2.0/cleared/2000.0"]["dchi2"]
row(s, "example canonical", ex["canonical"], -23.5, near(ex["canonical"], -23.5, 1))
row(s, "example alt", ex["alt"], -16.8, near(ex["alt"], -16.8, 1))
row(s, "unconverted halo, minimum", min(n["M1"].values()), 231.9, near(min(n["M1"].values()), 231.9, 1))
amps = [v["best_fs"][f][0] for v in n["M2"].values() for f in ("canonical", "alt")]
row(s, "KiDS-preferred amplitude low", min(amps), 0.30, near(min(amps), 0.30, 2))
row(s, "KiDS-preferred amplitude high", max(amps), 0.75, near(max(amps), 0.75, 2))

# ------------------------------------------------------------------------------------------------------------ L361
s = "L361"
n = N("g03_audit_2026/L361_bound_region_kernel_results.json")
row(s, "gap transmission 1/m = 0.2", n["R1"]["transmission"]["0.2"], 9.5e-5, sci(n["R1"]["transmission"]["0.2"], 9.5e-5))
row(s, "gap transmission 1/m = 0.1", n["R1"]["transmission"]["0.1"], 2.8e-9, sci(n["R1"]["transmission"]["0.1"], 2.8e-9))
row(s, "Sun: field correction", n["R2"]["field_correction"], 4e-12, round(n["R2"]["field_correction"] / 1e-12) == 4)
R3 = n["R3"]
def r3(key, f):
    return R3[key]["dchi2"][f]
for key, c, a, dec in [("total field (BS2's construction)", 548, 562, 0), ("baryons only (L353/L355)", 233, 241, 0),
                       ("bound-region kernel, 1/m = 0.1 Mpc (all baryons active)", 0.0, 0.0, 1),
                       ("bound-region kernel, 1/m = 0.2 Mpc (all baryons active)", 0.0, 0.0, 1),
                       ("bound-region kernel, 1/m = 0.3 Mpc (all baryons active)", 0.4, 0.2, 1),
                       ("bound-region kernel, 1/m = 0.5 Mpc (all baryons active)", -11.5, -11.3, 1),
                       ("bound-region kernel, 1/m = 1 Mpc (all baryons active)", 104, 110, 0)]:
    row(s, f"KiDS {key.split(' (')[0] if 'bound' not in key else key.split(' (')[0]} canonical", r3(key, "canonical"), c, near(r3(key, "canonical"), c, dec))
    row(s, f"KiDS {key.split(' (')[0] if 'bound' not in key else key.split(' (')[0]} alt", r3(key, "alt"), a, near(r3(key, "alt"), a, dec))
row(s, "phantom beyond the edge / M_b", n["R5"]["max_phantom_beyond_over_Mb"], 2.5e-7, sci(n["R5"]["max_phantom_beyond_over_Mb"], 2.5e-7))
row(s, "1/m bound (Mpc)", n["R4"]["max_mInv"], 0.5, n["R4"]["max_mInv"] == 0.5)

# ------------------------------------------------------------------------------------------------------------ L363
s = "L363"
n = N("g03_audit_2026/L363_region_kernel_lensing_power_results.json")
hm = {k: max(v.values()) for k, v in n["halo_model"].items()}
obs = [v for k, v in hm.items() if k.startswith("observed")]
mxl = [v for k, v in hm.items() if k.startswith("maximal")]
row(s, "halo model worst R, observed low", min(obs), 2.90, near(min(obs), 2.90, 2))
row(s, "halo model worst R, observed high", max(obs), 4.69, near(max(obs), 4.69, 2))
row(s, "halo model worst R, all baryons low", min(mxl), 4.68, near(min(mxl), 4.68, 2))
row(s, "halo model worst R, all baryons high", max(mxl), 9.18, near(max(mxl), 9.18, 2))
fm = [max(v["R_cons"].values()) for k, v in n["mock"].items() if k.startswith("100 Mpc/bound")]
row(s, "finest mock worst R low", min(fm), 1.53, near(min(fm), 1.53, 2))
row(s, "finest mock worst R high", max(fm), 2.32, near(max(fm), 2.32, 2))

# ------------------------------------------------------------------------------------------------------------ L364
s = "L364"
n = N("g03_audit_2026/L364_replacement_carrier_cosmic_shear_results.json")
red = [v[2] for v in n["R3"].values()]
row(s, "kick reduction low", min(red), 0.46, near(min(red), 0.46, 2))
row(s, "kick reduction high", max(red), 0.54, near(max(red), 0.54, 2))
row(s, "window", n["window"], "none", n["window"] == {"strict": [], "alt": []})
row(s, "blocking counts", n["blocking"], "shear 44, l354 36, kids 24, forest 16, S8 8",
    n["blocking"] == {"l354": 36, "shear": 44, "kids": 24, "forest": 16, "S8": 8})
nm = n["nearest"][0]
row(s, "nearest miss cell", (nm["fd"], nm["vk"], nm["switch"], nm["failing"]), "(0.95, 1200, p=2 x_c0=2, [kids])",
    nm["fd"] == 0.95 and nm["vk"] == 1200.0 and nm["switch"] == "p=2, x_c0=2.0" and nm["failing"] == ["kids"])
row(s, "nearest miss KiDS canonical", nm["kids"]["canonical"], -2.6, near(nm["kids"]["canonical"], -2.6, 1))
row(s, "nearest miss KiDS alt", nm["kids"]["alt"], 6.0, near(nm["kids"]["alt"], 6.0, 1))
row(s, "nearest miss shear", (nm["shear"]["canonical"], nm["shear"]["alt"]), (1.12, 1.17), nm["shear"]["canonical"] == 1.12 and nm["shear"]["alt"] == 1.17)
sc = [r for r in n["scan"] if r["fd"] == 0.95 and r["vk"] == 1200.0][0]
row(s, "nearest miss forest (loose only)", sc["t2"], "<0.9952", 0.9 <= min(sc["t2"], sc["t3"]) < 0.9952)
row(s, "nearest miss S8", sc["S8"], 0.762, near(sc["S8"], 0.762, 3))
ph = n["phantom"]
for key, k, v in [("p=1, x_c0=1.5/canonical", "0.5", 0.04), ("p=1, x_c0=1.5/canonical", "1.0", 0.33),
                  ("p=2, x_c0=2.0/canonical", "0.5", 0.01), ("p=2, x_c0=2.0/canonical", "1.0", 0.10)]:
    row(s, f"phantom own power s^2 {key.split('/')[0]} k={k}", ph[key]["s2"][k], v, near(ph[key]["s2"][k], v, 2))

# ------------------------------------------------------------------------------------------------------------ L370
s = "L370"
n = N("merger_infall_2026/L370_boosted_infall_mergers_results.json")
rf = list(n["A_real_fraction"].values())
row(s, "El Gordo phantom share of lensing mass (%) low", 100 * (1 - max(rf)), 39, near(100 * (1 - max(rf)), 39, 0))
row(s, "El Gordo phantom share of lensing mass (%) high", 100 * (1 - min(rf)), 44, near(100 * (1 - min(rf)), 44, 0))
row(s, "El Gordo Delta chi low", n["A3_dchi_2500"]["min"], -0.58, near(n["A3_dchi_2500"]["min"], -0.58, 2))
row(s, "El Gordo Delta chi high", n["A3_dchi_2500"]["max"], -0.12, near(n["A3_dchi_2500"]["max"], -0.12, 2))
b7 = n["B7_sigma"]
core = [v for k in ("cleared_2000", "cap_1000") for v in b7[k].values()]
okc = [v for k in ("intact", "uniform_0.55") for v in b7[k].values()]
row(s, "core-converted Harvey offset low (sigma)", min(core), 1.7, near(min(core), 1.7, 1))
row(s, "core-converted Harvey offset high (sigma)", max(core), 4.0, near(max(core), 4.0, 1))
row(s, "intact / uniform low (sigma)", min(okc), 0.7, near(min(okc), 0.7, 1))
row(s, "intact / uniform high (sigma)", max(okc), 1.3, near(max(okc), 1.3, 1))
t = TXT("merger_infall_2026/L370_boosted_infall_mergers.out")
row(s, "Harvey <beta>", "-0.04 +/- 0.07" in t, True, "<beta> = delta_SI/delta_SG = -0.04 +/- 0.07" in t)
row(s, "best strict cell (cleared_2000) on the NFW-fit estimator (sigma)", b7["cleared_2000"]["fit"], 1.7, near(b7["cleared_2000"]["fit"], 1.7, 1))
offs = re.findall(r"star-carrier equilibrium offset ([0-9.]+) kpc intact, ([0-9.]+) cleared", t)
oi = [float(a) for a, _ in offs]; oc = [float(b) for _, b in offs]
row(s, "star-dark offset, intact (kpc)", f"{min(oi)}-{max(oi)}", "6-11", near(min(oi), 6, 0) and near(max(oi), 11, 0))
row(s, "star-dark offset, core-converted (kpc)", f"{min(oc)}-{max(oc)}", "20-50", near(min(oc), 20, 0) and near(max(oc), 50, 0))
row(s, "checks in the committed output", "11/14" in t, "11/14", "11/14 checks pass" in t)

# ------------------------------------------------------------------------------------------------------------ L371, L372
s = "L371/L372"
t = TXT("merger_infall_2026/L371_harvey_slow_kick_carrier.out")
m = re.search(r"Msun/h\): 1e14 -> ([0-9.]+) .*?; 3e14 -> ([0-9.]+) ", t)
row(s, "L366 retention at 1e14 / 3e14", (m.group(1), m.group(2)), ("0.18", "0.40"), m.group(1) == "0.18" and m.group(2) == "0.40")
mb = N("merger_infall_2026/L371_harvey_slow_kick_carrier_results.json")["mean_beta"]
sig = [(mb[k]["fit"] + 0.04) / 0.07 for k in ("S1_med", "S2_med", "S3_med")]
row(s, "disfavoured at >= 2.1 sigma (fit estimator)", f"{min(sig):.2f}-{max(sig):.2f}", ">= 2.1", near(min(sig), 2.1, 1))
n = N("merger_infall_2026/L372_gated_slow_kick_carrier_results.json")
slow = n["part1"]["cleared|2000.0|750.0"]["xcop"]
row(s, "slow kick X-COP", (round(slow["canonical"]["ratio"], 3), round(slow["alt"]["ratio"], 3)), (1.38, 1.44), near(slow["canonical"]["ratio"], 1.38, 2) and near(slow["alt"]["ratio"], 1.44, 2))
hv = n["harvey"]
row(s, "slow kick passes Harvey, fast fails", (hv["1|cleared|2000.0|750.0"]["ok"], hv["1|cleared|2000.0|3000.0"]["ok"]), (True, False),
    hv["1|cleared|2000.0|750.0"]["ok"] is True and hv["1|cleared|2000.0|3000.0"]["ok"] is False)
row(s, "two-channel window (alt set)", n["window"], "[(alt, 0.25, 750/900/1050)]",
    sorted(map(tuple, n["window"])) == [("alt", 0.25, 750.0), ("alt", 0.25, 900.0), ("alt", 0.25, 1050.0)])

# ------------------------------------------------------------------------------------------------------------ GP1
s = "GP1"
n = N("generated_phantom_2026/GP1_generated_phantom_construction_results.json")
src = [n["N2"][lam]["1.0"]["source_switch"] for lam in n["N2"] if lam in ("2.0", "3.0", "inf")]
row(s, "M_dyn(1 Mpc)/M_b low", min(src), 101, near(min(src), 101, 0))
row(s, "M_dyn(1 Mpc)/M_b high", max(src), 106, near(max(src), 106, 0))
flux = [n["N2"][lam]["1.0"]["flux_switch"] for lam in n["N2"] if lam in ("2.0", "3.0", "inf")]
row(s, "flux switch at 1 Mpc", max(abs(f - 1) for f in flux), 1.0, max(abs(f - 1) for f in flux) < 0.05)
row(s, "Lagrangian asymmetry", n["N3"]["asym"], 1.6e-5, sci(n["N3"]["asym"], 1.6e-5))
row(s, "one-filter (BK1) asymmetry", n["N3"]["asym_bk1_form"], 3.3e-2, sci(n["N3"]["asym_bk1_form"], 3.3e-2))
lb = n["N2_lagrangian_over_bk1"]
l1 = [100 * (1 - lb[l]["1.0"]) for l in ("2.0", "3.0")]
l26 = [100 * (1 - lb[l]["2.6"]) for l in ("2.0", "3.0")]
row(s, "Lagrangian lensing mass lower at 1 Mpc (%)", f"{min(l1):.1f}-{max(l1):.1f}", "6-11", near(min(l1), 6, 0) and near(max(l1), 11, 0))
row(s, "Lagrangian lensing mass lower at 2.6 Mpc (%)", f"{min(l26):.1f}-{max(l26):.1f}", "22-35", near(min(l26), 22, 0) and near(max(l26), 35, 0))
for host, vs1, vs, vf in [("dwarf (M_B 1e9, edge 60 kpc)", 161, 176, 59), ("Milky Way (6e10, 250 kpc)", 352, 402, 165),
                          ("group (1e12, 600 kpc)", 563, 682, 334), ("cluster (1.5e13, 1.8 Mpc)", 667, 954, 657)]:
    h1, h = n["N4"][host]["1.0"], n["N4"][host]["2.0"]
    row(s, f"edge step l = 1 {host.split(' (')[0]}", h1["v_step_kms"], vs1, near(h1["v_step_kms"], vs1, 0))
    row(s, f"edge step l = 2 {host.split(' (')[0]}", h["v_step_kms"], vs, near(h["v_step_kms"], vs, 0))
    row(s, f"v_flat {host.split(' (')[0]}", h["v_flat_kms"], vf, near(h["v_flat_kms"], vf, 0))
n5 = {k: v for k, v in n["N5"].items() if isinstance(v, dict)}
row(s, "density switch metric max", max(v["density_switch_metric"] for v in n5.values()), 2.4e-6, sci(max(v["density_switch_metric"] for v in n5.values()), 2.4e-6))
row(s, "density switch khronon max (%)", 100 * max(max(v["density_switch_khronon"]) for v in n5.values()), 1.5,
    near(100 * max(max(v["density_switch_khronon"]) for v in n5.values()), 1.5, 1))
cv = [v["curvature_switch_metric"] for v in n5.values()]
row(s, "curvature switch low", min(cv), 0.07, near(min(cv), 0.07, 2))
row(s, "curvature switch high", max(cv), 2.3, near(max(cv), 2.3, 1))

# ------------------------------------------------------------------------------------------------------------ GP2
s = "GP2"
d = J("generated_phantom_2026/GP2_kids_bound_source_kernel_results.json")
n = d["numbers"]
e2 = [v for k, v in d["checks"].items() if k.startswith("E2")][0]["measured"]
row(s, "kernel field median l = 1 (a0)", "7.3e-06" if "'1.0': '7.3e-06'" in e2 else e2, 7.3e-6, "'1.0': '7.3e-06'" in e2)
row(s, "kernel field median l = 2 (a0)", "3.9e-05" if "'2.0': '3.9e-05'" in e2 else e2, 3.9e-5, "'2.0': '3.9e-05'" in e2)
W5 = n["W5"]["observed"]
for lam, c, a in [("1.0", 3.6, 0.6), ("2.0", -14.8, -16.7), ("3.0", -17.9, -18.7)]:
    row(s, f"vs L352 acceptance l = {lam}", (round(W5[lam][0], 2), round(W5[lam][1], 2)), (c, a), near(W5[lam][0], c, 1) and near(W5[lam][1], a, 1))
passing = sorted(float(l) for l, v in W5.items() if l != "inf" and v[0] <= 4 and v[1] <= 4)
row(s, "passes L352 for l = 1-10 Mpc", passing, "[1..10]", passing and min(passing) == 1.0 and max(passing) == 10.0)
W4 = n["W4"]
for lam, c, a in [("1.0", 19.8, 18.6), ("1.5", 5.6, 4.9), ("2.0", 0.7, 0.6), ("3.0", -0.4, 0.4)]:
    cc, aa = W4[f"canonical|{lam}"]["vs_floor_same_fs"], W4[f"alt|{lam}"]["vs_floor_same_fs"]
    row(s, f"vs realisable floor l = {lam}", (round(cc, 2), round(aa, 2)), (c, a), near(cc, c, 1) and near(aa, a, 1))
fsr = [W4[f"{f}|{l}"]["fs"] for f in ("canonical", "alt") for l in ("1.0", "1.5", "2.0", "3.0")]
row(s, "KiDS-wanted halo fraction low", min(fsr), 0.17, near(min(fsr), 0.17, 2))
row(s, "KiDS-wanted halo fraction high", max(fsr), 0.30, near(max(fsr), 0.30, 2))
for f, lo_, hi_ in (("canonical", 103, 133), ("alt", 113, 145)):
    cost = [n["F1"][f"{f}|{l}"]["chi2_fs1"] - n["F1"][f"{f}|{l}"]["chi2_all"] for l in ("1.0", "1.5", "2.0", "3.0")]
    row(s, f"uncleared CDM halo cost low ({f})", min(cost), lo_, near(min(cost), lo_, 0))
    row(s, f"uncleared CDM halo cost high ({f})", max(cost), hi_, near(max(cost), hi_, 0))
row(s, "floor vs comparator", (round(n["R1"]["canonical"]["floor_all"], 2), round(n["R1"]["alt"]["floor_all"], 2)), (8.2, 8.3),
    near(n["R1"]["canonical"]["floor_all"], 8.2, 1) and near(n["R1"]["alt"]["floor_all"], 8.3, 1))

# ------------------------------------------------------------------------------------------------------------ GP3
s = "GP3"
n = N("generated_phantom_2026/GP3_lensing_power_and_growth_results.json")
for key, v in [("canonical|1.0", 1.49), ("canonical|2.0", 2.31), ("canonical|3.0", 2.91), ("alt|1.0", 1.56), ("alt|2.0", 2.48), ("alt|3.0", 3.18)]:
    mx = max(n["L1"][key].values())
    row(s, f"max R(k<=1) {key}", mx, v, near(mx, v, 2))
for lam, v in [("1.0", 0.8), ("2.0", 2.0), ("3.0", 3.1)]:
    row(s, f"growth D(z=0) k=0.2, l={lam} (%)", 100 * n["G1"][lam]["0.2"], v, near(100 * n["G1"][lam]["0.2"], v, 1))
row(s, "GP3's own KiDS-vs-floor at l = 1", tuple(round(x, 2) for x in n["L4"]["1.0"]["kids_vs_floor_with_carrier"]), (19.8, 18.6),
    near(n["L4"]["1.0"]["kids_vs_floor_with_carrier"][0], 19.8, 1) and near(n["L4"]["1.0"]["kids_vs_floor_with_carrier"][1], 18.6, 1))

# ------------------------------------------------------------------------------------------------------------ GP4
s = "GP4"
n = N("generated_phantom_2026/GP4_generated_phantom_plus_kicked_carrier_results.json")
row(s, "control C1", n["C1"], 4e-16, n["C1"] < 1e-15)
row(s, "controls C2, C3", (n["C2"], n["C3"]), (0, 0), n["C2"] == 0 and n["C3"] == 0)
row(s, "window", n["W1"], "strict none; alt (1, 0.9, 1400), (1, 0.95, 1200)",
    n["W1"]["strict"] == [] and sorted(map(tuple, n["W1"]["alt"])) == [(1.0, 0.9, 1400.0), (1.0, 0.95, 1200.0)])
sc = n["scan"]
def cells(lam):
    return [r for r in sc if r["lam"] == lam]
s07 = [r["shear"][f] for r in cells(0.7) for f in ("canonical", "alt")]
k07 = [r["kids"][f] for r in cells(0.7) for f in ("canonical", "alt")]
row(s, "l = 0.7: shear range", f"{min(s07):.2f}-{max(s07):.2f}", "0.99-1.09", near(min(s07), 0.99, 2) and near(max(s07), 1.09, 2) and max(s07) <= 1.2)
row(s, "l = 0.7: KiDS range (fails in every cell)", f"{min(k07):.1f}-{max(k07):.1f}", "20.7-30.6", near(min(k07), 20.7, 1) and near(max(k07), 30.6, 1) and min(k07) > 4)
for lam, lo, hi in [(1.5, 1.45, 1.88), (2.0, 1.89, 2.36)]:
    sv = [r["shear"][f] for r in cells(lam) for f in ("canonical", "alt")]
    kv = [r["kids"][f] for r in cells(lam) for f in ("canonical", "alt")]
    row(s, f"l = {lam}: shear range (fails in every cell)", f"{min(sv):.2f}-{max(sv):.2f}", f"{lo}-{hi}", near(min(sv), lo, 2) and near(max(sv), hi, 2) and min(sv) > 1.2)
    row(s, f"l = {lam}: KiDS passes in every cell", max(kv), "<= 4", max(kv) <= 4)
def cell(lam, fd, vk):
    return [r for r in sc if r["lam"] == lam and r["fd"] == fd and r["vk"] == vk][0]
for (fd, vk), (sh, ki, xr, xn, gal, s8, fo) in {
        (0.95, 1200.0): ((1.09, 1.15), (-6.2, -4.6), (0.97, 1.00), (0.92, 0.94), 0.004, 0.762, 0.9917),
        (0.9, 1400.0): ((1.13, 1.19), (-4.8, -2.2), (0.89, 0.92), (0.83, 0.86), 0.010, 0.755, 0.9934)}.items():
    r = cell(1.0, fd, vk)
    row(s, f"({fd}, {vk:.0f}) shear", (round(r["shear"]["canonical"], 3), round(r["shear"]["alt"], 3)), sh, near(r["shear"]["canonical"], sh[0], 2) and near(r["shear"]["alt"], sh[1], 2))
    row(s, f"({fd}, {vk:.0f}) KiDS vs L352", (round(r["kids"]["canonical"], 2), round(r["kids"]["alt"], 2)), ki, near(r["kids"]["canonical"], ki[0], 1) and near(r["kids"]["alt"], ki[1], 1))
    row(s, f"({fd}, {vk:.0f}) X-COP raw", (round(r["xcop"]["canonical"][0], 3), round(r["xcop"]["alt"][0], 3)), xr, near(r["xcop"]["canonical"][0], xr[0], 2) and near(r["xcop"]["alt"][0], xr[1], 2))
    row(s, f"({fd}, {vk:.0f}) X-COP non-thermal", (round(r["xcop"]["canonical"][1], 3), round(r["xcop"]["alt"][1], 3)), xn, near(r["xcop"]["canonical"][1], xn[0], 2) and near(r["xcop"]["alt"][1], xn[1], 2))
    row(s, f"({fd}, {vk:.0f}) galaxies", r["gal"]["canonical"], gal, near(r["gal"]["canonical"], gal, 3))
    row(s, f"({fd}, {vk:.0f}) S8", r["S8"], s8, near(r["S8"], s8, 3))
    row(s, f"({fd}, {vk:.0f}) forest", r["forest"], fo, near(r["forest"], fo, 4))
    row(s, f"({fd}, {vk:.0f}) strict forest short by (%)", 100 * (0.9952 - r["forest"]), "0.2-0.4", 0.15 <= 100 * (0.9952 - r["forest"]) <= 0.45)
    row(s, f"({fd}, {vk:.0f}) strict S8 short by", 0.767 - r["S8"], "0.005-0.012", 0.0045 <= 0.767 - r["S8"] <= 0.0125)
c8 = cells(1.0)
c8 = [r for r in c8 if r["fd"] == 0.8]
sh8 = [r["shear"][f] for r in c8 for f in ("canonical", "alt")]
row(s, "l = 1, f_d(0) = 0.8: shear range (fails)", f"{min(sh8):.2f}-{max(sh8):.2f}", "1.23-1.40", near(min(sh8), 1.23, 2) and near(max(sh8), 1.40, 2) and min(sh8) > 1.2)
row(s, "l = 1, f_d(0) = 0.8: KiDS alt footing (fails)", c8[0]["kids"]["alt"], 4.4, near(c8[0]["kids"]["alt"], 4.4, 1) and c8[0]["kids"]["alt"] > 4)
row(s, "l = 1, f_d(0) = 0.8: strict forest", min(r["forest"] for r in c8), ">= 0.9952", min(r["forest"] for r in c8) >= 0.9952)
fd_fo = {fd: [min(r["t2"], r["t3"]) for r in l364["scan"] if r["fd"] == fd] for fd in (0.8, 0.9, 0.95)}
for fd, lo_, hi_ in ((0.8, 0.9954, 0.9960), (0.9, 0.9934, 0.9943), (0.95, 0.9914, 0.9926)):
    row(s, f"forest across L364's scan, f_d(0) = {fd}", f"{min(fd_fo[fd]):.4f}-{max(fd_fo[fd]):.4f}", f"{lo_}-{hi_}", near(min(fd_fo[fd]), lo_, 4) and near(max(fd_fo[fd]), hi_, 4))
unscr = [r for r in N("dark_sector_2026/L354_carrier_lagrangian_additive_window_results.json")["W1"]["table"]["canonical_0.95"] if r["vk"] == 1200.0][0]["ratio"]
unscr_a = [r for r in N("dark_sector_2026/L354_carrier_lagrangian_additive_window_results.json")["W1"]["table"]["alt_0.95"] if r["vk"] == 1200.0][0]["ratio"]
row(s, "unscreened X-COP (L354/L364) for (0.95, 1200)", (round(unscr, 3), round(unscr_a, 3)), (1.17, 1.22), near(unscr, 1.17, 2) and near(unscr_a, 1.22, 2))
nm = N("generated_phantom_2026/GP4_generated_phantom_plus_kicked_carrier_results_MUTATE.json")
m1 = [r for r in nm["scan"] if r["lam"] == 1.0][0]["shear"]
row(s, "no free streaming: shear at l = 1", (round(m1["canonical"], 2), round(m1["alt"], 2)), (1.49, 1.56), near(m1["canonical"], 1.49, 2) and near(m1["alt"], 1.56, 2))
row(s, "no free streaming: shear fails at every l", min(r["shear"][f] for r in nm["scan"] for f in ("canonical", "alt")), "> 1.2",
    min(r["shear"][f] for r in nm["scan"] if r["lam"] >= 1.0 for f in ("canonical", "alt")) > 1.2)

# ============================================================================================================== REPORT
banner("THE NUMBERS PAPER34 QUOTES, AGAINST THE COMMITTED OUTPUTS")
bad = [r for r in ROWS if not r[4]]
cur = None
for sec, lab, comp, stated, ok in ROWS:
    if sec != cur:
        print(f"  -- {sec}")
        cur = sec
    cs = f"{comp:.4g}" if isinstance(comp, float) else str(comp)
    print(f"     {'ok ' if ok else 'BAD'} {lab}: {cs[:70]}  (paper: {stated})")
check("N1 every quoted number matches the committed lane outputs at the paper's precision", not bad,
      f"{len(ROWS) - len(bad)}/{len(ROWS)} match" + ("" if not bad else f"; mismatches: {[(r[0], r[1]) for r in bad]}"))

# ============================================================================================================== X1
banner("X1  THE NUMBER THIS NOTE ADDS: GP4's window cells against GP2's realisable KiDS floor (same halo freedom)")
g2 = J("generated_phantom_2026/GP2_kids_bound_source_kernel_results.json")["numbers"]
g4 = N("generated_phantom_2026/GP4_generated_phantom_plus_kicked_carrier_results.json")
res = {}
for f in ("canonical", "alt"):
    comparator = g2["reference"][f]["all"]                                     # chi^2 of the Gauss-forbidden comparator
    kernel_alone = comparator + g2["W"][f"observed|{f}|1.0"]["dchi2_all"]         # the l = 1 Mpc kernel, no dark halo
    base = kernel_alone - g2["W5"]["observed"]["1.0"][0 if f == "canonical" else 1]  # L352's base: isolated MOND + 2-halo
    fs_opt = g2["W4"][f"{f}|1.0"]["chi2"]                                         # the l = 1 kernel, halo amplitude free
    floor_fs = fs_opt - g2["W4"][f"{f}|1.0"]["vs_floor_same_fs"]                  # the realisable floor, same halo freedom
    floor_used = (comparator + g2["R1"][f]["floor_all"]) if MUTATE else floor_fs
    for cellkey in ((0.95, 1200.0), (0.9, 1400.0)):
        r = [x for x in g4["scan"] if x["lam"] == 1.0 and x["fd"] == cellkey[0] and x["vk"] == cellkey[1]][0]
        chi2 = base + r["kids"][f]
        res[(f, cellkey)] = {"chi2": chi2, "vs_floor": chi2 - floor_used, "vs_halo_optimum": chi2 - fs_opt,
                             "base": base, "floor_fs": floor_fs, "iso": g2["reference"][f]["iso_all"]}
        print(f"    {f:9s} cell f_d(0) {cellkey[0]}, v_k {cellkey[1]:.0f}: chi^2 {chi2:7.2f} (L352 base {base:6.2f}; isolated MOND "
              f"{g2['reference'][f]['iso_all']:6.2f}); vs the halo-free optimum {chi2 - fs_opt:+5.2f}; "
              f"vs the floor{' (as the summary read it)' if MUTATE else ''} {chi2 - floor_used:+6.2f}")
vf = [v["vs_floor"] for v in res.values()]
check("X1 GP4's window cells sit +19 to +21.5 above the realisable KiDS floor with the same halo freedom (not '+8'): every cell, "
      "both footings, between +17 and +22", all(17 <= x <= 22 for x in vf), f"{min(vf):+.1f} .. {max(vf):+.1f}")
row("X1", "window cells vs floor, low", min(vf), 19.1, near(min(vf), 19.1, 1))
row("X1", "window cells vs floor, high", max(vf), 21.5, near(max(vf), 21.5, 1))
opt = [v["vs_halo_optimum"] for k, v in res.items() if k[1] == (0.95, 1200.0)]
check("X2 (reported) the (0.95, 1200) cell's fixed halo lies within 0.5 in chi^2 of the free-amplitude optimum GP2 W4 scores",
      all(0 <= x <= 0.5 for x in opt), f"{min(opt):+.2f} .. {max(opt):+.2f}", load_bearing=False)
x1rows = [r for r in ROWS if r[0] == "X1"]
check("X1b the paper's quoted X1 range matches", all(r[4] for r in x1rows), [(r[1], round(r[2], 2)) for r in x1rows])
base_iso = [abs(v["base"] - v["iso"]) for v in res.values()]
check("X3 (reported) L352's base in this machinery is isolated MOND to < 0.1 in chi^2 (the two-halo term barely helps)",
      max(base_iso) < 0.1, f"max |base - isolated| = {max(base_iso):.3f}", load_bearing=False)
OUT["X1"] = {f"{k[0]}|{k[1][0]}|{k[1][1]:.0f}": v for k, v in res.items()}

# ============================================================================================================== X4
banner("X4  THE STRICT S8 FLOOR: KiDS-Legacy is 0.815 +0.016/-0.021 (Wright et al. 2025, arXiv:2503.19441, abstract)")
S8_C, S8_UP, S8_DN = 0.815, 0.016, 0.021                   # KiDS-Legacy; the lanes (L319 l.186) took 0.016 as the error
floor_rec, floor_low = S8_C - 3 * S8_UP, S8_C - 3 * S8_DN
print(f"    record's floor 0.815 - 3 x 0.016 = {floor_rec:.3f};  with the lower error 0.815 - 3 x 0.021 = {floor_low:.3f}")
win = [x for x in g4["scan"] if x["lam"] == 1.0 and (x["fd"], x["vk"]) in ((0.95, 1200.0), (0.9, 1400.0))]
strict_c = []
only_forest = []
for x in g4["scan"]:
    o = x["ok"]["strict"]
    rest = o["shear"] and o["kids"] and o["xcop"] and o["gal"] and x["S8"] >= floor_low
    if rest and o["forest"]:
        strict_c.append((x["lam"], x["fd"], x["vk"]))
    if rest and not o["forest"]:
        only_forest.append((x["lam"], x["fd"], x["vk"]))
print(f"    GP4 window cells' S8: {[round(x['S8'], 4) for x in win]}; strict window with the corrected floor: {strict_c}; "
      f"cells failing only the strict forest: {only_forest}")
nm364 = [x for x in l364["scan"] if x["fd"] == 0.95 and x["vk"] == 1200.0][0]["S8"]
check("X4 with KiDS-Legacy's lower error the strict S8 floor is 0.752 (not 0.767): GP4's window cells and L364's nearest miss pass it, "
      "no cell of GP4's scan passes the strict set, and the cells that fail only the strict forest are exactly the two window cells",
      near(floor_low, 0.752, 3) and near(floor_rec, 0.767, 3) and all(x["S8"] >= floor_low for x in win) and nm364 >= floor_low
      and strict_c == [] and sorted(only_forest) == [(1.0, 0.9, 1400.0), (1.0, 0.95, 1200.0)],
      f"floor {floor_low:.3f}; window S8 {[round(x['S8'], 4) for x in win]}; L364 nearest {nm364:.4f}; strict {strict_c}; forest-only {only_forest}")

# ============================================================================================================== X5
banner("X5  THE FOREST THRESHOLDS AS THERMAL-RELIC MASSES (L319's transfer function, cosmology and k grid)")
import numpy as np
from scipy.optimize import brentq
h_, omb_, omc_ = 0.6736, 0.02237, 0.1200                     # L319 lines 66-68
Om_ = (omb_ + omc_) / h_ ** 2
K_H = np.geomspace(0.02, 30.0, 44)                            # L319 line 91
k5 = K_H[int(np.argmin(np.abs(K_H - 5.0)))]
def T2_wdm(k, m):                                             # L319's T2_wdm (Viel et al. 2005)
    a = 0.049 * m ** -1.11 * (Om_ / 0.25) ** 0.11 * (h_ / 0.7) ** 1.22; nu_ = 1.12
    return (1 + (a * k) ** (2 * nu_)) ** (-10 / nu_)
m_of = lambda t: brentq(lambda m: T2_wdm(k5, m) - t, 0.05, 100.0)
mw = {c: m_of(x["forest"]) for c, x in zip(("0.95/1200", "0.9/1400"), sorted(win, key=lambda x: -x["fd"]))}
eq = {"k5": k5, "T2_5.3keV": T2_wdm(k5, 5.3), "loose_0.9_keV": m_of(0.9), "window_keV": mw}
print(f"    k = {k5:.2f} h/Mpc; T^2(5.3 keV) = {eq['T2_5.3keV']:.5f}; loose 0.9 <-> {eq['loose_0.9_keV']:.2f} keV; "
      f"window cells {', '.join(f'{c}: {v:.2f} keV' for c, v in mw.items())}")
for lab, comp, st, ok in [("forest k grid point", round(k5, 2), 4.62, near(k5, 4.62, 2)),
                          ("T^2 of the 5.3 keV relic there", round(eq["T2_5.3keV"], 4), 0.9952, near(eq["T2_5.3keV"], 0.9952, 4)),
                          ("loose threshold relic (keV)", round(eq["loose_0.9_keV"], 2), 1.5, near(eq["loose_0.9_keV"], 1.5, 1)),
                          ("window cell (0.95, 1200) relic (keV)", round(mw["0.95/1200"], 2), 4.3, near(mw["0.95/1200"], 4.3, 1)),
                          ("window cell (0.9, 1400) relic (keV)", round(mw["0.9/1400"], 2), 4.7, near(mw["0.9/1400"], 4.7, 1))]:
    row("X5", lab, comp, st, ok)
x5 = [r for r in ROWS if r[0] == "X5"]
check("X5 the forest thresholds as thermal relics: 5.3 keV <-> T^2 = 0.9952 at k = 4.62 h/Mpc; the loose 0.9 is 1.5 keV; the window cells "
      "are 4.3 and 4.7 keV", all(r[4] for r in x5), [(r[1], r[2]) for r in x5])
OUT["X4"] = {"floor_record": floor_rec, "floor_lower_error": floor_low, "strict_window": strict_c, "forest_only": only_forest}
OUT["X5"] = eq
OUT["rows"] = [{"section": r[0], "label": r[1], "computed": str(r[2]), "paper": str(r[3]), "ok": r[4]} for r in ROWS]

banner("VERDICT")
nlb = sum(1 for _, ok, lb in CH if lb and not ok)
print(f"  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nlb}")
fn = os.path.join(HERE, "P34_paper_numbers_results" + ("_MUTATE" if MUTATE else "") + ".json")
if "ROOT" not in os.environ:
    json.dump(OUT, open(fn, "w"), indent=1, default=str)
    print(f"  wrote {os.path.basename(fn)}")
sys.exit(1 if nlb else 0)
