#!/usr/bin/env python3
"""PAPER57 audit: the built PDF must be newer than the TeX and 6-8 pages long; every quoted number must match the committed lane
outputs (JSON where the number is stored there; otherwise the lane's LEDGER row, README or DERIVATION text); every theorem statement
must match the wording of its lane's DERIVATION / README; the post-hoc disclosures must be present; the in-progress statements must
still be true; no forbidden claim, local path or personal name may appear.
Run: python3 PAPER57_audit.py (exit 0 only if all pass).  Read-only: it opens committed files and the PDF, nothing else."""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.normpath(os.path.join(HERE, "..", "..", "campaign_fresh_gravity"))
TEX = os.path.join(HERE, "PAPER57_cold_sector_structure_2026.tex")
PDF = os.path.join(HERE, "PAPER57_cold_sector_structure_2026.pdf")
F = 0
N = 0


def check(name, ok, msg=""):
    global F, N
    N += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {msg}" if msg else ""))
    F += (not ok)


SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")


def norm(t):
    for a, b in (("ﬁ", "fi"), ("ﬂ", "fl"), ("ﬀ", "ff"), ("ﬃ", "ffi"), ("−", "-"), ("–", "-"), ("—", "-"), ("’", "'"), ("‘", "'"),
                 (" ", " "), ("µ", "μ"), ("∆", "Δ"), ("ϕ", "φ"), ("∑", "Σ"), ("∗", "*"), ("**", ""), ("\\|", "|")):
        t = t.replace(a, b)
    t = t.translate(SUB)
    t = re.sub(r"\s*×\s*", "x", t)                      # 2.2 × 10-16 and 2.2e-16 styles: see sci()
    t = re.sub(r"(?<=\d)\s*-\s*(?=\d)", "-", t)            # ranges split around a dash
    t = re.sub(r"(?<=\w) (?=[,.;:)])", "", t)               # space left before punctuation by a sub/superscript
    t = re.sub(r"\s*±\s*", " ± ", t)
    return re.sub(r"\s+", " ", t)


def nsp(t):
    """formula comparison: drop whitespace, markup and super/subscript marks"""
    t = norm(t).translate(str.maketrans("²³⁴", "234"))
    return re.sub(r"[\s_{}*^\\]", "", t)


def dehyph(t):
    return re.sub(r"([a-z])- ([a-z])", r"\1\2", t)       # words hyphenated by TeX at a line end


def keephyph(t):
    return re.sub(r"([a-z])- ([a-z])", r"\1-\2", t)      # explicit hyphens that fell at a line end


def sci(s):
    """'2.2e-16' -> '2.2x10-16' (how the PDF renders 2.2\\times10^{-16} after norm)"""
    m = re.fullmatch(r"([\d.]+)e([+-]?)0*(\d+)", s)
    return f"{m.group(1)}x10{'-' if m.group(2) == '-' else ''}{m.group(3)}"


J = lambda p: json.load(open(os.path.join(CFG, p)))
LEDGER = open(os.path.join(CFG, "LEDGER.md"), encoding="utf-8").read().splitlines()


def row(lane):
    hits = [l for l in LEDGER if l.startswith(f"| {lane} |")]
    return norm(hits[0]) if hits else ""


_cache = {}


def src(path):
    if path not in _cache:
        _cache[path] = norm(open(os.path.join(CFG, path), encoding="utf-8").read())
    return _cache[path]


# ---------------------------------------------------------------- A. build
check("A1 PDF newer than TeX", os.path.getmtime(PDF) >= os.path.getmtime(TEX))
pages = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", PDF], capture_output=True, text=True, check=True).stdout).group(1))
check("A2 page count 6-8", 6 <= pages <= 8, f"{pages} pages")
raw = [norm(subprocess.run(["pdftotext"] + m + [PDF, "-"], capture_output=True, text=True, check=True).stdout) for m in (["-layout"], [])]
flat = " ||| ".join(raw + [keephyph(x) for x in raw] + [dehyph(x) for x in raw])
flat_ns = nsp(" ".join(raw))
low = flat.lower()
tex = open(TEX, encoding="utf-8").read()


def has(name, s):
    s = norm(s)
    check(name, s in flat, s)


def led(name, lane, s, pdf_s=None):
    """s must be in the lane's LEDGER row AND (s, or its PDF wording pdf_s) in the PDF"""
    r = row(lane)
    s, p = norm(s), norm(pdf_s or s)
    check(name, bool(r) and s in r and p in flat, f"{lane}: '{s}'" + (f" / PDF '{p}'" if pdf_s else "") + ("" if r else " (no LEDGER row)"))


def rd(name, path, s, pdf_s=None, ci=False):
    """s must be in the lane file AND (s, or pdf_s) in the PDF (ci: case-insensitive for both)"""
    s = norm(s)
    t, p, f = src(path), norm(pdf_s or s), flat
    if ci:
        t, p, f, s = t.lower(), p.lower(), low, s.lower()
    check(name, s in t and p in f, f"{path.split('/')[0]}: '{s}'" + (f" / PDF '{pdf_s}'" if pdf_s else ""))


def form(name, path, s, pdf_s=None):
    """a formula: compared with whitespace and markup removed, in the lane file and in the PDF"""
    a, b = nsp(s), nsp(pdf_s or s)
    check(name, a in nsp(src(path)) and b in flat_ns, f"{path.split('/')[0]}: '{a}'" + (f" / PDF '{b}'" if pdf_s else ""))


def lform(name, lane, s, pdf_s=None):
    """a formula in the lane's LEDGER row, compared without whitespace and markup"""
    a, b = nsp(s), nsp(pdf_s or s)
    check(name, a in nsp(row(lane)) and b in flat_ns, f"{lane}: '{a}'" + (f" / PDF '{b}'" if pdf_s else ""))


f2 = lambda x: f"{x:.2f}"
f3 = lambda x: f"{x:.3f}"
R38, R39, R41, R44, R45, R46, R47 = ("CFG938_medium_continuum_eft/README.md", "CFG939_lagrangian_displacement_shell_crossing/README.md",
                                     "CFG941_self_gravity_repair/README.md", "CFG944_gated_tether_ghost_cure/README.md",
                                     "CFG945_gated_tether_satellite_hover/README.md", "CFG946_option2_phantom_not_cold/README.md",
                                     "CFG947_option3_nonlocal_parent/README.md")
D38, D41, D44, D45, D46, D47 = ("CFG938_medium_continuum_eft/DERIVATION.md", "CFG941_self_gravity_repair/DERIVATION.md",
                                "CFG944_gated_tether_ghost_cure/DERIVATION.md", "CFG945_gated_tether_satellite_hover/DERIVATION.md",
                                "CFG946_option2_phantom_not_cold/DERIVATION.md", "CFG947_option3_nonlocal_parent/DERIVATION.md")
R40, R48, R49 = ("CFG940_faint_rotators_mcquinn22/README.md", "CFG948_nocapture_vs_udgs/README.md", "CFG949_clusters_untethered/README.md")
TC14, TC16, TC18 = "THEORY_CANONICAL_2026-10-14.md", "THEORY_CANONICAL_2026-10-16.md", "THEORY_CANONICAL_2026-10-18.md"

# ---------------------------------------------------------------- B. setting
rd("B footing canonical", R38, "9.3603e-11", "9.36x10-11"); rd("B footing alt", R38, "1.1312e-10", "1.13x10-10")
rd("B Omega_c/Omega_b measured", TC14, "5.364 (measured)", "5.364, is measured")
rd("B S4 permanently free", TC14, "permanently free"); rd("B simple interpolating function", TC14, "the simple interpolating function; Famaey & Binney 2005", "the simple interpolating function of Famaey & Binney (2005)"); rd("B H-EX working rule", TC16, "H-EX", "H-EX makes the cold share of expelled baryons free")
form("B S2 Lagrangian (W_rem, K, gamma)", TC14, "K W_rem′(u) = u²/(a₀ − u)", "KWrem(u) = u2/(a0 − u)")
rd("B class A: instantaneous shell draw", D44, "instantaneous shell draw"); rd("B class A: zero-sum per catchment", D44, "zero-sum per catchment", "zero-sum source")
rd("B class A: peaks", D44, "around resolved peaks", "around resolved peaks")

# ---------------------------------------------------------------- C. CFG938 covariant parent
r38 = J("CFG938_medium_continuum_eft/cfg938_results.json")
check("C law 2.2e-16 both footings, 43 radii (JSON)", all(r38["K1"][f]["max_rel_vs_law"] < 2.3e-16 and r38["K1"][f]["n"] == 43 for f in ("canonical", "alt"))
      and sci("2.2e-16") in flat and "43 radii" in flat)
rd("C law 2.2e-16 (README)", R38, "2.2e-16", sci("2.2e-16"))
form("C action W_full", R38, "W_full(u) = [−a₀u − a₀² ln(1 − u/a₀)]/K", "Wfull(u) = [−a0u − a20 ln(1 − u/a0)]/K")
for s, p in (("dust background, w = 0 | forced", "Forced. A dust background"), ("rest frame = cosmic frame | forced", "The cosmic frame as the medium's rest frame"),
             ("tether P·∇Φ | forced", "ordinary gravitational coupling"), ("some extra structure for u | forced", "Some extra structure is also forced"),
             ("γ > 0 | forced by well-posedness", "forced by well-posedness"), ("W_full(u) itself | chosen (S2's input)", "(S2's input; κ fitted)"),
             ("that structure = χ + λ, medium-frame constraint | chosen", "a non-propagating potential χ with a multiplier λ"),
             ("stiffness realisation (EoS vs χ-tidal) | chosen", "the stiffness realisation")):
    rd(f"C forced/chosen '{s[:30]}'", D38, s, p)
rd("C 2-form identity", R38, "electric part of the 2-form", "electric part of the 2-form potential")
rd("C u non-local (enclosed mass)", R38, "u = K|P| is an enclosed-mass quantity that no strain function can express", "enclosed-mass quantity that no strain function can express")
rd("C BBN ratio", R38, "ratio 1.3e3-2.3e6 at z = 4e8", "1.3x103-2.3x106 at z = 4x108")
rd("C static stress = CFG660 (derived)", R38, "exactly CFG660's field-aligned stress", "exactly the record's field-aligned stress (CFG660), now derived")
rd("C no drift in the ideal action", R38, "no drift in the ideal action", "The ideal action has no settling drift")
rd("C books: CFG932 omitted E_W", R38, "CFG932 omitted E_W", "the energy books close with the tether energy plus heat, which CFG932")
led("C slip 1.54e-5", "CFG938", "slip ≤ 1.54e-5", sci("1.54e-5"))
check("C slip worst (JSON)", f"{r38['S4']['worst_847']:.2e}" == "1.54e-05")
form("C dispersion relation", R38, "ω² = γρ₀k² + Kρ₀[R′cos²θ + (R/u)sin²θ] ≥ 0", "ω = γρ0k + Kρ0[R cos θ + (R/u) sin θ] ≥ 0")  # PDF text drops the superscripts
led("C sqrt(k) growth cured", "CFG938", "CFG660's √k growth cured", "cures CFG660's")
rd("C inertia margin", R38, "margin 5.9e4-2.5e8", "5.9x104-2.5x108")
form("C inertia condition", D38, "ρ_c c² > D(u)u/K", "ρcc2 > D(u)u/K")
for s, p in (("Extra non-propagating fields χ", "the extra non-propagating fields χ"), ("Matching to S2 only in the longitudinal sector: exact for spherical systems",
             "matching to S2 only in the longitudinal sector, which is exact for spherical systems"), ("Single-stream flow, with ρ_c > 0 everywhere", "single-stream flow")):
    rd(f"C condition '{s[:28]}'", D38, s, p, ci=True)
led("C flag growth a^0.61", "CFG938", "δ ∝ a^0.61", "a0.61"); led("C growth corrected a^0.694 (CFG941)", "CFG941", "a^0.694", "a0.694")
r41 = J("CFG941_self_gravity_repair/cfg941_results.json")
check("C exponents (JSON CFG941 D6)", f"{r41['D6']['n_S6']:.2f}" == "0.61" and f"{r41['D6']['n_full']:.3f}" == "0.694" and abs(r41["D6"]["n_dust"] - 1) < 1e-12)
led("C flag differential free fall", "CFG938", "0.03-0.17 a0", "0.03-0.17 a0")
rr = [v["ratio_to_a0"] for v in r38["S8"]["host_medium_field"].values()]
check("C differential free fall range (JSON)", f"{min(rr):.2f}" == "0.03" and f"{max(rr):.2f}" == "0.17", f"{min(rr):.4f}-{max(rr):.4f}")
sc = {s["gate"]: s["status"] for s in r38["scorecard"]}
check("C scorecard (JSON)", [g for g in sc if sc[g] == "PASS"] == ["A5", "C2"] and [g for g in sc if sc[g] == "CONDITIONAL"] == ["A1", "A2", "B3", "C1"]
      and [g for g in sc if sc[g] == "FAIL"] == ["C3"] and [g for g in sc if sc[g] == "UNTESTED"] == ["A3", "A4", "A6", "B1", "B2", "D1", "D2"])
led("C scorecard (LEDGER, PDF)", "CFG938", "PASS A5, C2; CONDITIONAL A1, A2, B3, C1; FAIL C3 (inherited from the law); UNTESTED A3, A4, A6, B1, B2, D1, D2")
rd("C particle in disguise for the mass", R38, "Particle in disguise: yes, for the mass", "Particle in disguise. Yes for the mass")
led("C no propagating mode", "CFG938", "the tether sector has no propagating mode", "The tether sector has no propagating mode")
check("C class CONDITIONAL, 30/30 checks (JSON)", r38["class"] == "CONDITIONAL" and len(r38["checks"]) == 30)
led("C lane class", "CFG938", "COVARIANT PARENT CONDITIONAL"); led("C 30/30", "CFG938", "30/30 checks", "all 30 checks pass")
led("C A1/A2 post hoc", "CFG938", "both post hoc", "Two post-hoc items are disclosed")
rd("C three flags of equal weight", R38, "three flags of equal weight", "Three flags of equal weight", ci=True)

# ---------------------------------------------------------------- D. CFG939 exact kinematics
r39 = J("CFG939_lagrangian_displacement_shell_crossing/cfg939_results.json")
led("D identity 9e-16", "CFG939", "1-D multi-stream identity to 9e-16", sci("9e-16"))
check("D identity (JSON)", f"{r39['K1c']['max_err_P']:.0e}" == "9e-16")
form("D spherical P_r", R39, "P_r = ρ̄(q³ − r³)/(3r²)", "Pr = ρ̄(q3 − r3)/(3r2)")
form("D force in any stream", "CFG939_lagrangian_displacement_shell_crossing/README.md", "−∇Φ_b + R(K|P|)P̂ − γ∇ρ_c")
led("D phase mixing", "CFG939", "100% of the inner mass crossed, 0.999 of the law at 2 r_M", "100% of the inner mass has crossed")
check("D phase mixing (JSON)", r39["C1"]["crossed_inside5"] == 1.0 and f"{r39['C1']['m2']:.3f}" == "0.999" and "0.999 of the law" in flat)
led("D H-SC premise FALSE", "CFG939", "H-SC premise FALSE", "the H-SC premise is FALSE")
check("D C1 primary 0.949 (JSON)", f"{r39['C1']['m5']:.3f}" == "0.949" and "gives 0.949, outside by 0.001" in flat)
rd("D C1 misses by 0.001", R39, "The primary run gives 0.949, which misses by 0.001", "The primary run gives 0.949, outside by 0.001")
rd("D C1 other runs", R39, "The first run gave 0.966", "The first run gave 0.966"); rd("D C1 A2 runs", R39, "give 0.958 and 0.956, and 0.994 at t = 6000", "0.958, 0.956, and 0.994 at t = 6000")
rd("D C2(a)", R39, "is 0.43-0.52 against a 0.9 bar", "0.43-0.52 against a 0.9 bar")
rd("D not derivable C3 / C1 4 of 5", R39, "NOT DERIVABLE on the analytic test C3 and on C1 in 4 of 5 runs", "not derivable on the analytic test C3 and on C1 in 4 of 5 runs", ci=True)
rd("D unassigned (C1 borderline)", R39, "unassigned by the frozen rules at the primary run (C1 borderline)", "unassigned by the frozen rules (C1 borderline)")
rd("D CFG888's unwritten coupling", R39, "CFG888's unwritten coupling")
h = {k: v for k, v in r39["alignment"]["HSC"].items() if k != "overall"}
check("D MISALIGNS 16/16 (JSON)", len(h) == 16 and all(v["class_"] == "MISALIGNS" for v in h.values()) and "in all 16 cells" in flat)
led("D MISALIGNS (LEDGER)", "CFG939", "MISALIGNS 16/16 cells", "MISALIGNS")
form("D f_crit", R39, "f_crit(x) = 1 − (1−x)(artanh√x − √x)/x^(3/2)", "fcrit(x) = 1 − (1 − x)(artanh")  # PDF text drops the root signs
form("D f_crit tail", R39, "√x)/x^(3/2), x = u/a0", "x)/x3/2, with x = u/a0")
rd("D f_crit deep 2/3, dwarf and MW values", R39, "f_crit = 2/3 in the deep regime (0.673-0.691 at dwarf r½, 0.774 for MW-like)", "This is 2/3 in the deep regime (0.673-0.691 at dwarf r1/2")
has("D f_crit MW-like in PDF", "0.774 for a Milky-Way-like system")
rd("D unbound medium leaves: deficit", R39, "a deficit, not the +0.33 dex excess", "a deficit, not an excess")
a1 = r39["A1_flat_potential"]
check("D flat potential numbers (JSON)", f"{a1['mu_edge_pred']:.5f}" == "-0.01339" and f"{a1['deep_formula']:.5f}" == "-0.01333" and "-0.01339 against -0.01333" in flat)
form("D flat potential formula", R39, "μ = −(2/3)GM_b/R_e")
rd("D no capture escape speeds", R39, "TDGs 21-53 km/s, DF2/DF4 22-23 km/s vs v_rel ≥ 100 km/s", "(21-53 km/s)")
has("D DF2/DF4 escape speed in PDF", "(22-23 km/s) against vrel ≥ 100 km/s")
form("D r_sub", R39, "r_sub = L*²/(4 r_M)", "rsub = L2*/(4rM)")
led("D energy 1.3e-4", "CFG939", "1.3e-4 with crossings", sci("1.3e-4") + " with crossings")
n3 = r39["N3"]["tether"]
check("D energy (JSON)", f"{n3['dE_rel']:.1e}" == "1.3e-04")
check("D 44%, 21.4 of 48.9 (JSON)", round(100 * n3["outbound_unbound_frac"]) == 44 and f"{n3['energy']['mass_outbound']:.1f}" == "21.4"
      and f"{n3['energy']['mass_total']:.1f}" == "48.9" and "44% of the infall mass leaves (21.4 of 48.9" in flat)
led("D leak belongs to class-A drift law", "CFG939", "CFG932's non-conservation belongs to the record's class-A drift law", "belongs to its class-A drift law")
led("D never holds a surplus", "CFG939", "a conservative tether only expels mass and never holds a surplus", "A conservative tether only expels mass and never holds a surplus")
led("D sym 30/30, K 11/11", "CFG939", "sym 30/30; K 11/11", "30/30 symbolic and 11/11 numerical"); check("D K 11/11 (JSON)", r39["K_pass"] == "11/11")
led("D MUTATE 5/5", "CFG939", "MUTATE 5/5 bite", "the five mutation teeth bite"); led("D A2 post hoc", "CFG939", "A2 92e2f0627 POST HOC", "A2 is post hoc")
led("D A1 pre-result", "CFG939", "A1 7dace0a16 pre-result", "A1 was pre-result")

# ---------------------------------------------------------------- E. CFG932 energy books + audit + CFG935
led("E Q1 NON-CONSERVING", "CFG932", "Q1 NON-CONSERVING", "Q1 is NON-CONSERVING")
lform("E energy identity", "CFG932", "d(K+W)/dt = P_drift + P_bath", "d(K + W)/dt = Pdrift + Pbath")
led("E +0.593 and identity 1.9e-3", "CFG932", "ΔW/|W0| +0.593, identity 1.9e-3", sci("1.9e-3"))
has("E +0.593 in PDF", "+0.593")
led("E exact Lambda cannot supply", "CFG932", "which an exact Λ cannot supply", "which an exact Λ cannot supply")
led("E f_ret 0.10", "CFG932", "f_ret 0.10", "fret = 0.10"); led("E retained excess <= 0.001 dex", "CFG932", "r_h ≤ 0.001 dex", "rh of ≤ 0.001 dex")
led("E observed size", "CFG932", "+0.18…+0.39 dex", "+0.18 to +0.39 dex"); led("E ~100x supply", "CFG932", "~100× the record's supply", "about 100 times that supply")
led("E shear = epsilon->0 limit", "CFG932", "the shear pass is H-ELS's ε → 0 limit, not a test of it", "ε → 0 limit of energy-limited settling, not a test of it")
led("E H-ELS post hoc", "CFG932", "H-ELS is POST-HOC", "(H-ELS) is post hoc"); led("E A1 post hoc", "CFG932", "post-hoc A1", "so is the lane's amendment A1")
led("E audit: reproduces", "CFG932-audit", "the CFG932 energy identity and class arithmetic reproduce", "reproduced the energy identity and the class arithmetic")
led("E audit: endpoint-accounting defect", "CFG932-audit", "endpoint-accounting defect")
led("E audit: not an audited window", "CFG932-audit", "not an audited physical window")
led("E audit: Q1/Q2 unaffected", "CFG932-audit", "Q1 (record settling NON-CONSERVING) and the record-supply Q2 finding", "Q1 and the record-supply finding are not affected")
led("E audit: CFG930 verdict stands", "CFG932-audit", "CFG930's independent CONTRADICTED verdict on H-ELS stands", "CONTRADICTED verdict on H-ELS (CFG930) stands")
d35 = os.path.join(CFG, "CFG935_energy_conserving_settling")
check("E CFG935 still in progress (no LEDGER row, no README)", row("CFG935") == "" and "README.md" not in os.listdir(d35)
      and "FROZEN_CRITERIA.md" in os.listdir(d35) and "CFG935, an energy-conserving repair" in flat and "no ledger result yet" in flat)

# ---------------------------------------------------------------- F. Theorem D-T (CFG941)
rd("F D-T assumption: always-on tether", D41, "Take a cold static medium held by any always-on tether force F(u). Its phantom is its own gravitating mass, so g = g_N + u.",
   "A cold static medium is held by any always-on tether force F (u), and its phantom is its own gravitating mass")
form("F D-T F(u)", D41, "F(u) = a₀u/(a₀ − u)", "F(u) = a0u/(a0 − u)")
form("F D-T series", D41, "F = u + u²/a₀", "u + u2/a0")
rd("F D-T deep limit forces linear coefficient 1", D41, "with linear coefficient 1 independent of h₁, h₂, h₃", "the linear coefficient is 1, whatever the higher terms")
check("F D-T BTFR limits (JSON)", r41["DT"]["btfr_limits"] == ["1", "oo", "0"] and "(an acceleration floor)" in flat and "(rescaled Newton)" in flat)
rd("F D-T BTFR limits (DERIVATION)", D41, "1 at c₂ = 1, ∞ at c₂ = ½ (an acceleration floor), and 0 at c₂ = 2 (rescaled Newton)", "0 at c2 = 2 (rescaled Newton)")
form("F D-T self-gravity coefficient", D41, "(1 − c₂)Kρ_c", "(1 − c2)Kρc")
rd("F D-T conclusion", D41, "no linear self-gravity of the settling medium, and no mutual gravity between", "no linear self-gravity of the settling medium and no gravity between tethered components")
led("F D-T statement (LEDGER)", "CFG941", "NO linear self-gravity and NO gravity between tethered components", "no linear self-gravity, and no gravity between tethered components")
led("F diagnosis: not a double count", "CFG941", "not a source double count", "not a double count of the source"); led("F diagnosis: force cancellation", "CFG941", "FORCE cancellation", "force cancellation")
rd("F R2 f_t and x15.6", R41, "f_t ≤ 0.060 ⇒ free mass ×15.6", "ft ≤ 0.060"); has("F x15.6 in PDF", "so the free mass, ×15.6, enters the law's source")
cl41 = r41["classes"]
check("F repair classes (JSON)", all(cl41[k]["cls"] == "NOT REPAIRABLE" for k in ("R1", "R2", "R3n", "R3ell")) and cl41["R3theta"]["cls"] == "PARTIAL")
check("F R3ell windows 4.0-6.7 decades (JSON)", "4.0-6.7 decades" in cl41["R3ell"]["why"] and "4.0-6.7 decades" in flat)
kg = [v["k_ghost_R"] for v in r41["R3theta"]["ghost"].values()]
check("F ghost k_gR range (JSON)", f2(min(kg)) == "0.23" and f2(max(kg)) == "2.19" and "kg R = 0.23-2.19" in flat, f"{min(kg):.4f}-{max(kg):.4f}")
hv = r41["hover"].values()
ra, ts, ed = [v["ratio"] for v in hv], [v["t_sep_Myr"] for v in r41["hover"].values()], [abs(v["efe_dex"]) for v in r41["hover"].values()]
check("F hover 1.02-1.11 (JSON)", f2(min(ra)) == "1.02" and f2(max(ra)) == "1.11" and "Δa/ghost = 1.02-1.11" in flat, f"{min(ra):.4f}-{max(ra):.4f}")
check("F stars leave 9-106 Myr (JSON)", f"{min(ts):.0f}" == "9" and f"{max(ts):.0f}" == "106" and "9-106 Myr" in flat)
check("F EFE 0.10-0.73 dex (JSON)", f2(min(ed)) == "0.10" and f2(max(ed)) == "0.73" and "0.10-0.73 dex of phantom" in flat)
check("F CFG925 R3 not respected (JSON)", r41["CFG925_R3_respected"] is False and "(CFG925 R3) is not respected" in flat)
led("F lane class", "CFG941", "STRUCTURAL OBSTRUCTION"); check("F overall (JSON)", r41["overall"] == "STRUCTURAL OBSTRUCTION")
led("F shear does not transfer", "CFG941", "the T1x/T2x/NC1x shear passes do not transfer", "the T1x/T2x/NC1x shear passes do not transfer")
led("F A1 pre-result", "CFG941", "A1 7c395c866 pre-result", "Amendment A1 was pre-result")

# ---------------------------------------------------------------- G. Theorem G (CFG944)
r44 = J("CFG944_gated_tether_ghost_cure/cfg944_results.json")
led("G rank-one second variation", "CFG944", "rank-one second variation"); form("G kinetic coefficient", R44, "ρ₀ + F_θθk²", "ρ0 + Fθθk2")
led("G k_g r on NGC 3198", "CFG944", "k_g r 5e-4-1.2e-2", "5x10-4-1.2x10-2")
rd("G assumption (d)", D44, "ghost freedom at all k", "Ghost freedom at all k", ci=True)
form("G assumption (a)", D44, "L(0, u) = −W(u) + L(0, 0)")
form("G assumption (c-amp)", D44, "L(θ, u) = L(θ, 0)"); rd("G assumption (c) linear", D44, "L(·, 0) linear on the cosmic range", "linear on the cosmic range")
form("G statement", D44, "B ≡ L(0, 0) − T(0) ≥ W(u*)")
rd("G convexity proof", D44, "f(θ) = L(θ, u*) is convex", "one line of convexity")
tg = r44["TheoremG"]
for foot, us, bm, be, ra_ in (("canonical", "0.774", "0.712", "0.0476", "15.0"), ("alt", None, "0.624", "0.0247", "25.3")):
    t = tg[foot]
    ok = f3(t["B_min"]) == bm and f"{t['B_e']:.4f}" == be and f"{t['ratio']:.1f}" == ra_ and (us is None or f3(t["u_star_over_a0"]) == us)
    check(f"G numbers {foot} (JSON)", ok and bm in flat and be in flat and f"({ra_} times)" in flat, f"B {t['B_min']:.4f}, B_e {t['B_e']:.4f}, x{t['ratio']:.2f}")
has("G u* in PDF", "u* = 0.774 a0")
led("G 15-25x", "CFG944", "15-25×", "15-25 times")
check("G c_theta growth bound (JSON)", f"{r44['C1']['c_theta_growth_max']:.1e}" == "8.9e+14" and sci("8.9e14") in flat)
led("G ghost bound 1.6e24", "CFG944", "the ghost bound is ≥ 1.6e24", sci("1.6e24"))
led("G C4 linear field", "CFG944", "15.6 a0 at z = 1100", "15.6 a0 at z = 1100"); led("G z >= 84", "CFG944", "z ≥ 84", "z ≥ 84")
led("G slip caps u_c", "CFG944", "u_c ≤ 0.22 / 0.16 a0", "0.22 / 0.16 a0")
check("G all NOT CURABLE, NO CURE (JSON)", all(v["cls"] == "NOT CURABLE" for v in r44["classes"].values()) and r44["overall"] == "NO CURE" and "NO CURE" in flat)
led("G option 1 closed for local Lagrangians", "CFG944", "closed for local Lagrangians"); led("G no amendments", "CFG944", "no amendments")
rd("G concavity theorem", R44, "concavity theorem", "a concavity theorem")
rd("G scope: rho-dependent extensions open", R44, "ρ-dependent extensions of Theorem G", "ρ-dependent extensions")

# ---------------------------------------------------------------- H. Lemma L-G and theorem T-O2 (CFG946)
r46 = J("CFG946_option2_phantom_not_cold/cfg946_results.json")
rd("H L-G universal force", D46, "Let φ be a field whose gradient is a universal force", "be a field whose gradient is a universal force")
rd("H L-G superposition", D46, "exact uniform-gradient superposition"); form("H L-G phi + b.x", D46, "φ + b·x")
form("H L-G scaling", D46, "A(μ³M, μR) = μ²A(M, R)", "A(μ3 M, μR) = μ2 A(M, R)")
form("H L-G deep law mu^{3/2}", D46, "μ^{3/2}", "μ3/2")
rd("H L-G conclusion", D46, "every sector that does supply it has an EFE", "every sector that does supply it has an external-field effect")
form("H L-G share mu^{1/2}", D46, "μ^{1/2}", "μ1/2")
rd("H L-G examples: AQUAL, QUMOND", R46, "Deep AQUAL and QUMOND fail superposition, so they have an EFE", "and QUMOND fail superposition, so both have an EFE")  # a page break follows "Deep AQUAL"
has("H L-G examples: AQUAL in PDF", "Deep AQUAL")
rd("H L-G examples: Galileon", R46, "A cubic Galileon passes superposition but has no flat regime", "a cubic Galileon passes it but has no flat regime")
for s, p in (("Cold energy is pressureless, universally coupled dust in free fall, with Poisson self-gravity", None),
             ("Every force is universal", "every force is universal"), ("profile-independent deep amplitude", None),
             ("A uniform external field leaves a satellite's internal dynamics unchanged", None), ("No construction satisfies A1-A4", None)):
    rd(f"H T-O2 '{s[:30]}'", D46, s, p, ci=True)
rd("H T-O2 dust x0.5 misses", D46, "misses the law by 0.414 / 0.421", "missing the law by 0.414 / 0.421")
check("H 8 constructions NOT VIABLE, NO-GO (JSON)", len(r46["classes"]) == 8 and all(v["cls"] == "NOT VIABLE" for v in r46["classes"].values())
      and r46["overall"] == "NO-GO (theorem T-O2)" and r46["theorems_pass"] is True)
led("H all 8 NOT VIABLE", "CFG946", "All 8 constructions NOT VIABLE", "All eight constructions are NOT VIABLE")
led("H QUMOND EFE -0.58", "CFG946", "up to −0.58 dex", "up to -0.58 dex"); form("H c2 != 1 law", R46, "g_N = R(u) − (1 − c₂)u")
led("H Galileon", "CFG946", "a Galileon has no deep regime", "A Galileon has no deep regime")
led("H particle in disguise", "CFG946", "a cold collisionless species in every gravitational respect")
led("H D-T' generalises", "CFG946", "D-T′", "D-T′")
rd("H scope: modified inertia", D46, "Modified inertia", "modified inertia", ci=True); rd("H scope: EP charges", D46, "EP-violating charges", "charges that violate the equivalence principle")
rd("H scope: transport length", D46, "25.6 / 26.6 R", "25.6 / 26.6 times its radius")
led("H A1 code/reporting", "CFG946", "A1 23e0a5765 code/reporting, no class change", "Amendment A1 is code and reporting only")

# ---------------------------------------------------------------- I. Theorem S (CFG945)
r45 = J("CFG945_gated_tether_satellite_hover/cfg945_results.json")
form("I S hypothesis: force", D45, "f = −∇Φ + F(x, v; σ)")
rd("I S hypothesis: any functional", D45, "may be any functional of fields sourced by the whole system")
rd("I S hypothesis: no label", D45, "There is no membership label.")
form("I S claim", D45, "Δa = g_host + O(v/c*) + δ_cross")
rd("I S leading order", D45, "exact at leading order", "exact at leading order")
rd("I S escapes", R45, "a label, support specific to the stream, O(1) velocity dependence, or a non-stationary medium",
   "a membership label, support specific to the stream, O(1) velocity dependence, or a non-stationary medium")
led("I gate on, 1.017-1.107", "CFG945", "Δa/g_host 1.017-1.107", "1.017-1.107")
b = r45["bound"]
check("I eps_B (JSON)", f3(b["canonical"]["eps_B_k1"]) == "0.344" and f3(b["alt"]["eps_B_k1"]) == "0.317" and "εB = 0.344 (canonical) / 0.317" in flat)
ch = b["canonical"]["c_at_hover_min"]
check("I hover statistic (JSON)", f3(ch[0]) == "-0.355" and f3(ch[1]) == "0.114" and ch[2] == 19 and "-0.355 ± 0.114" in flat and "19 satellites are stripped" in flat)
led("I -3.1 se", "CFG945", "(−3.1 se)", "(-3.1 standard errors)")
check("I delta_c 0.082 (JSON)", f3(b["canonical"]["delta_c"]) == "0.082" and "0.082 dex" in flat)
cl45 = r45["classes"]
check("I classes (JSON)", cl45["H1"]["cls"] == "RESOLVED-WITH-COST" and all(cl45[k]["cls"] == "NOT RESOLVABLE" for k in ("H2", "H3", "H4"))
      and r45["overall"] == "CONDITIONAL" and "RESOLVED-WITH-COST" in flat and "NOT RESOLVABLE" in flat)
rd("I gate crossing 1.4-13.5 Myr", R45, "1.4-13.5 Myr"); rd("I EP violation eta", R45, "η = 0.76-1.04")
led("I A1 post hoc", "CFG945", "A1 8943d188e POST HOC", "A1 is post hoc"); led("I MUTATE exit 3", "CFG945", "MUTATE exit 3", "exits 3")
rd("I M5 toothless", "CFG945_gated_tether_satellite_hover/AMENDMENT_A1_post_hoc.md", "tooth M5, as frozen, did not bite", "toothless")

# ---------------------------------------------------------------- J. CFG947 non-local parents
r47 = J("CFG947_option3_nonlocal_parent/cfg947_results.json")
rd("J retarded: no action principle", R47, "Retarded non-local equations are not Euler-Lagrange equations of any action", "Retarded non-local equations come from no action principle")
rd("J time-symmetric acausal, precursor 1/2", R47, "precursor of ½ the static value", "a precursor of half the static value")
check("J T-M identity 7e-18 (JSON)", f"{r47['T-M']['identity']:.0e}" == "7e-18" and sci("7e-18") in flat)
check("J T-M 0.25 at eps 0.1 (JSON)", f2(r47["T-M"]["R_rel_E8"]["0.1"]) == "0.25" and "(0.25 at dipole fraction ε = 0.1)" in flat)
rd("J T-M pi^2 eps/4", R47, "π²ε/4 of the domain's weight scale", "ε/4 of the domain's weight scale"); form("J T-M pi^2 eps/4 PDF", R47, "π²ε/4", "π2ε/4")
tr = r47["T-R"]
check("J T-R threshold and counts (JSON)", f"{tr['Mb_thr']:.3e}" == "4.815e+10" and tr["sparc_below"] == 128 and tr["sparc_total"] == 175
      and sci("4.815e10") in flat and "128 of 175 SPARC galaxies" in flat)
rd("J NGC 3198 2% below", R47, "just below (2%)", "NGC 3198 sits 2% below the threshold")
hh = r47["h"]["H"]
check("J SPARC rms (JSON)", f3(hh["N2-E"]["canonical"]["rms"]) == "0.257" and f3(hh["N2-E"]["alt"]["rms"]) == "0.262" and f"{hh['N1']['canonical']['rms']:.4f}" == "0.1003"
      and f"{hh['N1']['alt']['rms']:.4f}" == "0.0991" and "0.257 / 0.262 dex rms, against 0.1003 / 0.0991" in flat)
tx = [abs(v) for v in r47["T-X"].values()]
check("J T-X EFE range (JSON)", f2(min(tx)) == "0.10" and f2(max(tx)) == "0.73" and "-0.10 to -0.73 dex on the test dwarfs at 50-250 kpc" in flat, f"{min(tx):.4f}-{max(tx):.4f}")
led("J global QUMOND phantom", "CFG947", "pointwise QUMOND phantom of the GLOBAL retained-baryon field", "pointwise QUMOND phantom of the global retained-baryon field")
led("J CFG478", "CFG947", "excluded by CFG478", "CFG478")
rd("J zero-sum 53.65 M_b", R47, "creates 53.65 M_b of 𝒮 at switch-on", "53.65 Mb"); has("J zero-sum in PDF", "at switch-on")
check("J no hover at monopole order (JSON)", all(v["monopole"] == 0.0 for v in r47["T-F"].values()) and "Δa/ghost = 0 at monopole order" in flat)
led("J escapes D-T", "CFG947", "a parent that changes the SOURCE of gravity escapes theorem D-T", "a parent that changes the source of gravity escapes D-T")
led("J growth a^1", "CFG947", "growth exactly a¹", "Growth is exactly a1"); led("J slip 1.63e-5", "CFG947", "slip ≤ 1.63e-5", sci("1.63e-5"))
re_ = [r["ratio"] for k, v in r47["T-E"].items() for r in v]
check("J forced edge 1.85-9.72 (JSON)", f2(min(re_)) == "1.85" and f2(max(re_)) == "9.72" and "1.85-9.72" in flat)
led("J forced edge (LEDGER)", "CFG947", "×1.85-9.72", "1.85-9.72")
rd("J domains forced", R47, "domains are forced", "so domains are forced")
check("J four NOT VIABLE, NO-GO (JSON)", len(r47["classes"]) == 4 and all(v == "NOT VIABLE" or (isinstance(v, dict) and v.get("cls") == "NOT VIABLE") for v in r47["classes"].values())
      and r47["overall"] == "NO-GO" and all(r47["structural"].values()))
led("J NO-GO for exact parenthood", "CFG947", "NO-GO for exact parenthood"); led("J A1 pre-result", "CFG947", "A1 fad3a6b86 pre-result (T-M falsifier corrected to the relocation term)", "it corrected the T-M falsifier")

# ---------------------------------------------------------------- K. labelled-domain construction
form("K H1 action", R45, "Σ_q W(|Dχ_q|)", "W(|Dχ_q|) plus the constraints")  # the PDF text drops the summation sign
led("K one tether per catchment", "CFG945", "one tether per catchment", "one tether per catchment")
rd("K H1 uniform field Delta a = 0", D45, "Δa = 0 in a uniform host field", "falls with its stars (Δa = 0)")
rd("K H1 tidal residual", R45, "PASS 1.6e-5 - 2.0e-3", sci("1.6e-5") + " to " + sci("2.0e-3"))
led("K restores gravity between objects", "CFG945", "restores Newtonian gravity BETWEEN distinct collapsed objects", "Newtonian gravity between distinct collapsed objects is restored")
rd("K costs: two labels miss NGC 3198", R45, "miss NGC 3198 by 4.12 / 4.61"); rd("K costs: q < 3.5e-7", R45, "q ≲ 3.5e-7", sci("3.5e-7"))
rd("K costs: no local seeding rule", D45, "No local rule was found", "No local seeding rule was found")
rd("K costs: conserved only between label changes", R45, "Energy-momentum conserved only between label changes", "conserved only between label changes", ci=True)
rd("K costs: ghost inherited", D45, "R3θ's ghost is inherited", "inherits R3θ's ghost")
check("K split-galaxy error 8.6% (JSON)", f"{100 * r47['T-L']['canonical|simple|f=0.01']:.1f}" == "8.6" and "8.6% on NGC 3198 at f = 0.01" in flat)
rd("K dipole-free draw", D47, "a dipole-free relocation: the draw's centroid tied to the phantom's at all times", "centroid tied to the phantom's at all times")
form("K 1024^3 run", R47, "a 1024³ run")
res = [l for l in LEDGER if l.startswith("| CFG950–959 |")]
rv = norm(res[0]) if res else ""
check("K CFG950-952 reservation text", "label assignment at collapse" in rv and "momentum-conserving source" in rv and "PM-engine implementation design" in rv
      and "label assignment at collapse" in flat and "momentum-conserving source" in flat)
ldt = [d for d in os.listdir(CFG) if d.startswith(("CFG950", "CFG951", "CFG952")) and os.path.isdir(os.path.join(CFG, d))]
ldt_files = sorted(f for d in ldt for f in os.listdir(os.path.join(CFG, d)))
check("K CFG950-952 still under construction (no LEDGER rows; lane dirs, if any, hold no README or results)",
      all(row(f"CFG95{i}") == "" for i in "012") and not any(f.startswith("README") or "result" in f.lower() for f in ldt_files)
      and "under construction; no result exists" in flat, f"dirs {ldt}, files {ldt_files}")
rd("K engine has no established parent (canonical v3 note)", TC18, "the class-A shear engine has no established physical parent", "its physical parent is not established")
has("K computational result", "computational result of the engine")

# ---------------------------------------------------------------- L. data confrontations
r40 = J("CFG940_faint_rotators_mcquinn22/cfg940_results.json")
check("L CFG940 lane class (JSON)", r40["lane_class"] == "NOT DIAGNOSTIC (DATA)" and "BRACKET-DEPENDENT" in r40["secondary_class"]
      and "NOT DIAGNOSTIC (DATA) on both footings" in flat and "BRACKET-DEPENDENT" in flat)
m40 = r40["main"]
for est, foot in (("A", "canonical"), ("A", "alt"), ("B", "canonical"), ("B", "alt")):
    v = m40[f"WS|{est}|{foot}|V0"]
    check(f"L CFG940 {est} {foot} (JSON)", v["N"] == 25 and f"{v['mean']:.3f} ± {v['se']:.3f}" in flat, f"{v['mean']:.3f} ± {v['se']:.3f}")
led("L CFG940 lowest g_bar", "CFG940", "lowest 10^-11.71 A / 10^-11.96 B, DDO 154", "10-11.71"); has("L CFG940 lowest B", "10-11.96")
led("L CFG940 single-point 0.18 dex", "CFG940", "runs 0.18 dex low under A", "runs 0.18 dex low under A")
rd("L CFG940 D values", R40, "D = +0.438 ± 0.122", "+0.438 ± 0.122 (A)"); rd("L CFG940 D values B", R40, "+0.318 ± 0.108", "+0.318 ± 0.108 dex (B)")
led("L CFG940 ~+0.2 dex", "CFG940", "only ~+0.2 dex", "only about +0.2 dex"); led("L CFG940 above Newton", "CFG940", "All 25 above Newton", "All 25 are above Newton")
led("L CFG940 A1 post hoc", "CFG940", "A1 bda93d8db POST HOC", "CFG940 A1"); rd("L McQuinn citation", "CFG940_faint_rotators_mcquinn22/FROZEN_CRITERIA.md", "ApJ 940, 8", "ApJ 940, 8 (2022)")
r48 = J("CFG948_nocapture_vs_udgs/cfg948_results.json")
check("L CFG948 class and Q2 (JSON)", r48["class"] == {"canonical": "NOT DIAGNOSTIC", "alt": "NOT DIAGNOSTIC"} and r48["Q2"] == {"canonical": "PREDICTED", "alt": "PREDICTED"}
      and "NOT DIAGNOSTIC (CONTROL-LIMITED) on both footings" in flat and "PREDICTED only technically" in flat)
check("L CFG948 ceiling (JSON)", f"{r48['E_ceil']:.4f}" == "0.0176" and "+0.0176 in natural log (0.008 dex)" in flat)
pc, pa = r48["byfoot"]["canonical"]["primary"], r48["byfoot"]["alt"]["primary"]
check("L CFG948 observed means (JSON)", pc["N"] == 9 and f"+{pc['mean_Eobs']:.3f} / +{pa['mean_Eobs']:.3f}" in flat)
check("L CFG948 z with sys (JSON)", f"+{pc['z_up']:.2f} / +{pa['z_up']:.2f}" in flat); check("L CFG948 z stat only (JSON)", f"+{pc['z_stat_up']:.2f} / +{pa['z_stat_up']:.2f}" in flat)
check("L CFG948 Newton excluded 5.45 (JSON)", f"{abs(pc['z_low']):.2f}" == "5.45" and f"{abs(pa['z_low']):.2f}" == "5.45" and "EXCLUDED at 5.45σ" in flat)
rd("L CFG948 0.008 dex", R48, "(0.008 dex)"); rd("L CFG948 9 of 9", R48, "9 of 9 above the law", "all nine above the law")
led("L CFG948 gas fraction 0.81", "CFG948", "median gas fraction 0.81"); led("L CFG948 DF2/DF4", "CFG948", "+0.40 / −0.30", "+0.40 / -0.30")
led("L CFG948 FRAGILE", "CFG948", "FRAGILE"); led("L CFG948 MUTATE power limit", "CFG948", "MUTATE fails as a systematics power limit (declared)", "fails as a power limit")
led("L CFG948 needs S4/H-EX", "CFG948", "S4/H-EX made real and derivable", "S4 or H-EX made real and derivable")
led("L CFG948 A1 post hoc", "CFG948", "A1 523a09954 post hoc", "CFG948 A1")
r49 = J("CFG949_clusters_untethered/cfg949_results.json")["main"]
bp = r49["B0_primary"]
check("L CFG949 primary corner (JSON)", f"{bp['A']['MID'][0]:.3f} ± {bp['A']['MID'][1]:.3f}" == "1.011 ± 0.063" and f"{bp['A']['OUTER'][0]:.3f} ± {bp['A']['OUTER'][1]:.3f}" == "1.047 ± 0.089"
      and f3(bp["s"]) == "0.661" and bp["cls"]["label"] == "EXPLAINS" and "AMID = 1.011 ± 0.063" in flat and "AOUTER = 1.047 ± 0.089" in flat and "slope is 0.661" in flat)
check("L CFG949 corners 6/4/30, FRAGILE (JSON)", r49["B0_counts"] == {"PARTIAL": 4, "FAILS": 30, "EXPLAINS": 6} and r49["robustness"] == "FRAGILE"
      and "only 6 of 40 corners EXPLAIN (4 PARTIAL, 30 FAIL)" in flat)
cc = r49["core_cyl05"]
check("L CFG949 core masses (JSON)", f"{cc['B0_minus_law_median']['canonical']:.1e}" == "2.9e+13" and f"{cc['B0_minus_law_median']['alt']:.1e}" == "2.1e+13"
      and f"{cc['CFG922_needed']['canonical']:.1e}" == "2.4e+13" and f"{cc['CFG922_needed']['alt']:.1e}" == "2.0e+13"
      and f"{sci('2.9e13')} / {sci('2.1e13')}" in flat and f"{sci('2.4e13')} / {sci('2.0e13')}" in flat)
check("L CFG949 class both footings (JSON)", all(r49["class"][f]["B0"] == "EXPLAINS" and r49["class"][f]["robustness"] == "FRAGILE" for f in ("canonical", "alt")))
led("L CFG949 law values", "CFG949", "1.91 / 1.75 and 1.01 / 0.93"); led("L CFG949 MID/OUTER", "CFG949", "MID/OUTER 0.97 vs the law's 1.89", "0.97, against the law's 1.89")
led("L CFG949 slope observed", "CFG949", "0.896 ± 0.209 (law 0.466", "0.896 ± 0.209 (law 0.466)"); led("L CFG949 318 eRASS1", "CFG949", "318 eRASS1")
led("L CFG949 x2-3 short", "CFG949", "×2-3 short", "2-3 times short"); led("L CFG949 x1.4-2.2", "CFG949", "×1.4-2.2", "1.4-2.2 times")
led("L CFG949 78%", "CFG949", "78% of the primary gas budget"); led("L CFG949 inner x1.55", "CFG949", "over-predicted ×1.55", "1.55 times")
led("L CFG949 K 6/7", "CFG949", "K 6/7 frozen (K5 off by 0.69% in ungraded inner bins)", "one is off by 0.69% in ungraded inner bins")
led("L CFG949 post hoc, zero constants", "CFG949", "POST HOC, zero fitted constants", "post hoc, zero fitted constants")
check("L CFG949 untether rule", "needs a rule that untethers clusters but not galaxies" in row("CFG949").lower() and "needs a rule that untethers clusters but not galaxies" in flat)
led("L CFG949 tethered regime", "CFG949", "tethered (galaxy) regime")
rd("L CFG949 footing-independent", R49, "B0 contains no a0", "This contains no a0, so it is footing-independent")

# ---------------------------------------------------------------- M. disclosures, companion, honesty, forbidden, names
for s in ("CFG938 A1", "CFG939 A2", "CFG945 A1", "CFG946 A1", "CFG932 A1", "CFG940 A1", "CFG948 A1", "CFG949 A1", "CFG939 A1, CFG941 A1, CFG947 A1", "CFG944 has none"):
    has(f"M disclosure '{s}'", s)
kept = ("CFG938_medium_continuum_eft/cfg938_firstrun_S3efail.out", "CFG939_lagrangian_displacement_shell_crossing/cfg939_firstrun_dt0005.out",
        "CFG939_lagrangian_displacement_shell_crossing/cfg939_secondrun_dt00125.out", "CFG945_gated_tether_satellite_hover/cfg945_MUTATE_firstrun_M5toothless.out",
        "CFG945_gated_tether_satellite_hover/cfg945_main_attempt1_killed_pointstars.out", "CFG946_option2_phantom_not_cold/cfg946_firstrun_npbool.out",
        "CFG947_option3_nonlocal_parent/cfg947_firstrun_TLcheck.out", "CFG949_clusters_untethered/cfg949_K_RUN1.out", "CFG949_clusters_untethered/cfg949_RUN1_acceptbug.out")
check("M superseded runs disclosed and kept on disk", all(os.path.exists(os.path.join(CFG, k)) for k in kept) and "Superseded runs are kept" in flat)
rd("M CFG944 text-only edits", R44, "Three output strings were changed", "reworded three output strings after its first full run; no number changed")
rd("M CFG949 graded numbers unchanged", R49, "Every graded number is identical", "(graded numbers unchanged)")
has("M companion PAPER56", "PAPER56"); has("M companion PAPER55", "PAPER55")
for s in ("fitted", "the theory is not closed", "not peer reviewed", "never pooled", "post hoc", "Post-hoc", "not established", "AI-assisted",
          "Anthropic's Claude", "not a particle", "computational result"):
    has(f"M honesty '{s}'", s)
for bad in ("theory closed", "theory is closed", "data favour the framework", "data favor the framework", "proves the framework", "breakthrough",
            "/users/", "gmail", "dark matter particle", "λcdm", "lcdm", "hmcode", "bahamas"):
    check(f"M forbidden '{bad}' absent", bad not in low and bad not in tex.lower())
check("M no home path in TeX", "/Users/" not in tex and "~/" not in tex)
gu = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True, cwd=HERE).stdout.split()
check("M no personal name (repo user) in PDF or TeX", all(w.lower() not in low and w.lower() not in tex.lower() for w in gu if len(w) >= 3), f"{len(gu)} name parts checked")

print(f"\nPAPER57 audit: {N - F}/{N} PASS" + ("" if F == 0 else f", {F} FAIL"))
sys.exit(1 if F else 0)
