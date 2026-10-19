#!/usr/bin/env python3
"""PAPER55 audit: the built PDF must be newer than the TeX, every quoted number must match the committed lane outputs, the honesty
phrases must be present, and no forbidden claim or local path may appear.  Run: python3 PAPER55_audit.py (exit 0 only if all pass).
Gate the deposit on this: build && audit && publish."""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.join(HERE, "..", "..", "campaign_fresh_gravity")
TEX, PDF = os.path.join(HERE, "PAPER55_low_acceleration_map_2026.tex"), os.path.join(HERE, "PAPER55_low_acceleration_map_2026.pdf")
F = 0
def check(name, ok, msg=""):
    global F
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {msg}" if msg else "")); F += (not ok)
J = lambda p: json.load(open(os.path.join(CFG, p)))
check("A1 PDF newer than TeX", os.path.getmtime(PDF) >= os.path.getmtime(TEX))
txt = subprocess.run(["pdftotext", "-layout", PDF, "-"], capture_output=True, text=True, check=True).stdout
for a, b in (("ﬁ", "fi"), ("ﬂ", "fl"), ("−", "-"), ("–", "-"), ("’", "'")): txt = txt.replace(a, b)
flat = re.sub(r"\s+", " ", txt)
def has(name, s): check(name, s in flat, s)
r650 = J("CFG650_theory_v2_combined_pm/cfg650_native_results.json")["runs"]
for foot, key in (("canonical", "L100_N1024_canonical"), ("alt", "L100_N1024_alt")):
    d = r650[key]["surveys"]["KiDS"]; dc = [v for k, v in d.items() if "dchi2" in k.lower() and isinstance(v, (int, float))]
    has(f"B shear {foot}", f"{dc[0]:.2f}" if dc else "MISSING")
c29 = J("CFG829_lensing_low_g_vs_dwarf_excess/cfg829_results.json")["canonical|nu_e|blue (u-r<2.5)"]["window"]
has("C blue A", f"{c29['A']:.3f}"); has("C blue sigma", f"{c29['sA']:.3f}"); has("C exclusion", f"{(10 ** 0.44 - c29['A']) / c29['sA']:.1f}")
v40 = J("CFG840_cfg829_robustness/cfg840_results.json")["variants"]; As = [v["A"] for v in v40.values()]
has("D min A", f"{min(As):.3f}"); has("D max A", f"{max(As):.3f}")
ex = min((10 ** 0.44 - v["A"]) / v["sA"] for v in v40.values()); has("D min exclusion", f"{ex:.1f}")
c49 = J("CFG849_structure_vs_colour_lensing/cfg849_results.json")["canonical"]
has("E colour split", f"{c49['d_colour'][0] / c49['d_colour'][1]:.1f}"); has("E Sersic split", f"{c49['d_sersic'][0] / c49['d_sersic'][1]:.1f}")
c50 = J("CFG850_red_split_mstar_systematic/cfg850_results.json")["rows"]
has("F red A corrected", f"{c50['canonical|0.123|0.0']['A_red']:.3f}"); has("F split corrected", f"{c50['canonical|0.123|0.0']['z_colour']:.1f}")
has("F split +0.20", f"{c50['canonical|0.2|0.0']['z_colour']:.1f}")
c51 = J("CFG851_spheroidal_excess_law/cfg851_results.json")["canonical|shift0.123"]
has("G b", f"{c51['cal']['b']:.3f}"); has("G log g_dagger", f"{c51['cal']['lgd']:.2f}"); has("G chi2", f"{c51['cal']['chi2']:.1f}")
has("G chi2 law", f"{c51['cal']['chi2_law']:.1f}"); has("G dSph pred", f"{c51['d_pred']:.3f}"); has("G dSph obs", f"{c51['d_obs']:.3f}")
has("H age rho", f"{J('CFG827_dwarf_age_sfh_ml/cfg827_results.json')['scores']['-1.31']['rho']:+.2f}")
c43 = J("CFG843_mw_vs_m31_satellites/cfg843_results.json")["all"]; has("I host offset", f"{c43['c']:+.3f}")
c45 = J("CFG845_hprim_vs_sparc_dwarfs/cfg845_results.json"); g = c45["galaxies"]
has("J SPARC pred", f"{sum(x['pred'] for x in g) / len(g):+.3f}"); has("J SPARC obs", f"{sum(x['obs'] for x in g) / len(g):+.3f}"); has("J z", f"{abs(c45['D'] / c45['sD']):.1f}")
has("K slip", f"{J('CFG847_lensing_slip_bound/cfg847_results.json')['max_s']:.1e}".replace("e-05", "")[:3])
has("L tides", f"{J('CFG838_satellite_tides/cfg838_results.json')['primary (M31 1.0e11)']['rho']:+.2f}")
has("L peri tides", f"{J('CFG839_pericentre_tides/cfg839_results.json')['primary (M_MW 6e10)']['rho']:+.2f}")
has("M metallicity", f"{J('CFG852_gas_loss_metallicity/cfg852_results.json')['primary']['rho']:+.2f}")
for s in ("fitted", "not closed", "not peer reviewed", "conditional"): has(f"N honesty '{s}'", s)
low = flat.lower()
for bad in ("theory closed", "theory is closed", "data favour the framework", "data favor the framework", "proves the framework", "/users/", "breakthrough"):
    check(f"O forbidden '{bad}' absent", bad not in low)
print(f"\nPAPER55 audit: {'ALL PASS' if F == 0 else f'{F} FAIL'}"); sys.exit(1 if F else 0)
