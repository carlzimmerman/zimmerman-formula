#!/usr/bin/env python3
"""PAPER57 audit: the built PDF must be newer than the TeX and 6-9 pages long (the update with CFG935 and CFG950-CFG952 needs 9
pages, which is accepted); every quoted number must match the committed
lane outputs (JSON where the number is stored there; otherwise the lane's LEDGER row, README or DERIVATION text); every theorem
statement must match the wording of its lane's DERIVATION / README; the post-hoc disclosures must be present; the lanes the first
draft called "in progress" (CFG935, CFG950-CFG952) must now have LEDGER rows and no in-progress statement may remain; no forbidden
claim, local path or personal name may appear.
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
    return re.sub(r"([A-Za-z])- ([A-Za-z])", r"\1-\2", t)  # explicit hyphens that fell at a line end (also after capitals: CONTROL-LIMITED)


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
check("A2 page count 6-9 (9 accepted for the updated draft)", 6 <= pages <= 9, f"{pages} pages")
raw = [norm(subprocess.run(["pdftotext"] + m + [PDF, "-"], capture_output=True, text=True, check=True).stdout) for m in (["-layout"], [], ["-raw"])]  # -raw keeps super/subscripts inline
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


def lonly(name, lane, s):
    """supporting check: s must be in the lane's LEDGER row (the PDF wording and number are checked elsewhere)"""
    check(name, norm(s) in row(lane), f"{lane} LEDGER: '{norm(s)}'")


def sonly(name, path, s):
    """supporting check: s must be in the lane file (the PDF wording and number are checked elsewhere)"""
    check(name, norm(s) in src(path), f"{path.split('/')[0]}: '{norm(s)}'")


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
form("C dispersion relation", R38, "ω² = γρ₀k² + Kρ₀[R′cos²θ + (R/u)sin²θ] ≥ 0")  # matched in the -raw extraction, superscripts kept
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
# CFG935: energy-conserving repair of the settling (landed after the first draft)
R35, A135 = "CFG935_energy_conserving_settling/README.md", "CFG935_energy_conserving_settling/AMENDMENT_A1_s2_discretisation.md"
r35 = J("CFG935_energy_conserving_settling/cfg935_results.json")
m35 = J("CFG935_energy_conserving_settling/cfg935_results_MUTATE.json")
p35, eth = r35["parts"], r35["parts"]["ETH"]["results"]
check("E CFG935 has a LEDGER row and a README (no longer in progress)", bool(row("CFG935")) and os.path.exists(os.path.join(CFG, R35)))
led("E CFG935 NO REPAIR (frozen)", "CFG935", "NO REPAIR (frozen)", "An energy-conserving repair (CFG935): NO REPAIR")
check("E CFG935 overall and five classes NOT VIABLE (JSON)", r35["overall"] == "NO REPAIR" and len(r35["classes"]) == 5
      and all(v["cls"] == "NOT VIABLE" for v in r35["classes"].values()) and "Five repairs, all NOT VIABLE" in flat)
rd("E CFG935 toy: N = 10000 shells", R35, "1-D spherical shells (N = 10000)", "1-D shell toy (G = a0 = 1, Plummer baryons, the simple law, 104 shells)")
rd("E CFG935 toy: units and baryons", R35, "Units G = a₀ = 1; static Plummer baryons", "G = a0 = 1, Plummer baryons")
rd("E CFG935 law gate |D| <= 0.1", R35, "ON THE LAW iff |D| ≤ 0.1", "(on the law iff |D| ≤ 0.1)")
check("E CFG935 energy theorem +0.165 / +0.532 / -1.60 (JSON)", f3(eth["N|I"]["excess_frac"]) == "0.165" and f3(eth["S2|I"]["excess_frac"]) == "0.532"
      and f2(eth["N|S"]["excess_frac"]) == "-1.60" and "+0.165 of |Elaw" in flat and "against a Jeans-supported law and +0.532" in flat and "+0.532 against the cold S2 ground state" in flat
      and "A cold surplus start carries -1.60" in flat)
led("E CFG935 books every source and sink", "CFG935", "Every repair books all its sources and sinks", "Each books every source and sink")
led("E CFG935 none inside matter brings infall onto the law", "CFG935", "none that keeps the released settling energy inside matter brings an infall start onto the law",
    "None that keeps the released energy inside matter brings an infall start onto the law")
ra1, ra1x = p35["Ra1_I"], p35["Ra1x100_I"]
check("E CFG935 FIX-1: D -0.216, baryon reaction 13 / 125 (JSON)", f3(ra1["D_W2"]) == "-0.216" and round(ra1["baryon_reaction_max"]) == 13 and ra1["lam"] == 10.0
      and round(ra1x["baryon_reaction_max"]) == 125 and ra1x["lam"] == 100.0 and "ends at D = -0.216, with a reaction on the baryons of 13" in flat and "(125 at λ = 100)" in flat)
rd("E CFG935 FIX-1 is the Hamiltonian lambda F", "CFG935_energy_conserving_settling/FROZEN_CRITERIA.md", "R-a(i), Hamiltonian FIX-1: H = K + W_N + λF", "Hamiltonian version of the record's two-sided drift (FIX-1, an energy λF)")
led("E CFG935 S2: exact unique ground state", "CFG935", "the law is S2's exact unique ground state", "has the law as its exact unique ground state")
check("E CFG935 S2: 53% excess, 41% unbound, D -0.271 (JSON)", f"{100 * eth['S2|I']['excess_frac']:.0f}" == "53" and f"{100 * p35['Ra2_I']['fesc_end']:.0f}" == "41"
      and f3(p35["Ra2_I"]["D_W2"]) == "-0.271" and "infall carries 53% of the binding energy as excess; it is shed by unbinding 41% of the supply" in flat
      and "warm remnant sits at D = -0.271" in flat)
lonly("E CFG935 S2 (LEDGER)", "CFG935", "infall carries 53% of the binding energy as excess, shed by unbinding 41% of the supply")
check("E CFG935 one-sided: D -0.102 / -0.355 (JSON)", f3(p35["Rb_L"]["D_W2"]) == "-0.102" and f3(p35["Rb_I"]["D_W2"]) == "-0.355"
      and "(D = -0.102 from the settled start, -0.355 on infall)" in flat)
rd("E CFG935 one-sided: heat-driven circulation", R35, "rectifies orbital fluctuations into a heat-driven circulation", "drives a circulation")
led("E CFG935 radiation: gravothermal", "CFG935", "a radiation channel (gravothermal runaway; the record's P field is gapped)", "runs away into gravothermal collapse")
rd("E CFG935 radiation: new gapless field, P gapped", R35, "also needs a new gapless field (P is gapped)", "would need a new gapless field, since the record's own field P is gapped (CFG760-762)")
check("E CFG935 dark-energy partner as frozen: D -0.145 / -0.215 (JSON)", f3(p35["Rd_L"]["D_W2"]) == "-0.145" and f3(p35["Rd_I"]["D_W2"]) == "-0.215"
      and not p35["Rd_L"]["on_law"] and not p35["Rd_I"]["on_law"] and "keeps exact books but ends off the law (D = -0.145 / -0.215)" in flat)
lonly("E CFG935 frozen partner: books exact, off the law", "CFG935", "the dark-energy partner as frozen (books exact, but off the law)")
ph = r35["post_hoc"]
check("E CFG935 post hoc on the law +0.003 / +0.010 (JSON)", f3(ph["PHou_L"]["D_W2"]) == "0.003" and f3(ph["PHou_I"]["D_W2"]) == "0.010"
      and ph["PHou_L"]["on_law"] and ph["PHou_I"]["on_law"] and "(D = +0.003 / +0.010)" in flat)
led("E CFG935 post hoc: no weight, stochastic isotropising bath", "CFG935", "POST HOC (no weight): the dark-energy partner with FIX-2's stochastic isotropising bath IS on the law from both starts",
    "Post hoc, no verdict weight. With the record's stochastic, isotropising bath, the dark-energy partner holds the law from both starts")
led("E CFG935 two reservoirs", "CFG935", "TWO new reservoirs, a dynamical dark-energy partner (an exact Λ cannot exchange energy) and a thermal reservoir at the local Jeans temperature",
    "two new reservoirs: a dynamical dark-energy partner (an exact Λ cannot exchange energy) and a thermal reservoir at the local Jeans temperature")
led("E CFG935 REPAIR NEEDS NEW PHYSICS", "CFG935", "REPAIR NEEDS NEW PHYSICS")
sy = r35["parts"]["PHYS"]["systems"]
ex = {f: [v["E_x_over_Mcat_Phi"] for v in sy[f].values()] for f in ("can", "alt")}
check("E CFG935 excess 0.14-0.40 / 0.16-0.39 of the binding (JSON)", f2(min(ex["can"])) == "0.14" and f2(max(ex["can"])) == "0.40" and f2(min(ex["alt"])) == "0.16"
      and f2(max(ex["alt"])) == "0.39" and "0.14-0.40 (canonical) / 0.16-0.39 (alternative) of each catchment's binding energy" in flat)
lonly("E CFG935 excess (LEDGER)", "CFG935", "excess energy 0.14-0.40 of each catchment's binding")
cz = r35["parts"]["PHYS"]["cosmic"]
check("E CFG935 drho_DE/rho_DE since z = 1 (JSON)", [f"{1e6 * x:.2f}" for x in cz["can"]["drho_DE_over_rhoDE_z1"]] == ["0.80", "1.10"]
      and [f"{1e6 * x:.2f}" for x in cz["alt"]["drho_DE_over_rhoDE_z1"]] == ["0.92", "1.25"] and "0.80-1.10x10-6 / 0.92-1.25x10-6" in flat)
led("E CFG935 allowed and unmeasurable", "CFG935", "allowed and unmeasurable", "allowed, and unmeasurable")
led("E CFG935 energy sink outside matter", "CFG935", "The settled law needs an energy sink outside the matter sector.", "So the settled law needs an energy sink outside the matter sector.")
led("E CFG935 K0 exact", "CFG935", "K0 exact (CFG932's drift test)", "K0 reproduces CFG932's drift test exactly")
check("E CFG935 three MUTATE teeth bite (JSON)", sorted(m35["results"]) == ["M1", "M2", "M3"] and all(v["bites"] for v in m35["results"].values())
      and "all three mutation teeth bite" in flat)
led("E CFG935 A0 pre-result", "CFG935", "A0 e9a824153 pre-result", "CFG935 A0")
led("E CFG935 A2 post-result for R-d", "CFG935", "A2 407e7054b (post-result for R-d)", "CFG935 A2 (post-result for the dark-energy repair)")
rd("E CFG935 A3-A5 post-result compute caps", R35, "A4 / A5 (post-result, compute only)", "A3-A5 (post-result compute caps)"); sonly("E CFG935 A3 post-result", R35, "A3 (post-result, compute only)")
rd("E CFG935 A1 before any valid S2 number", A135, "before any valid R-a(ii) (S2) number exists", "before any valid S2 result")
rd("E CFG935 A1 after failed S2 runs", R35, "The first S2 runs (MUTATE M3, Ra2_I, Ra2_S) reached u = a₀ and returned NaN", "after its first S2 runs failed numerically")
led("E CFG935 not blind", "CFG935", "not blind", "CFG935 and CFG950 froze with hand expectations stated")
stop = src(R35).split("Own processes stopped by hand")[1].split("8. ")[0]
check("E CFG935 four own runs stopped by hand (README)", all(s in stop for s in ("frozen-code Rd_I", "A2 Rd_S", "A2 Rb_S", "the first A2 Rc_L"))
      and "CFG935 stopped four of its own runs by hand" in flat)
rd("E CFG935 density gate misses central collapse", R35, "The frozen D measure cannot see a collapse inside r = 1", "CFG935's density gate misses a collapse inside r = 1")

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

# ---------------------------------------------------------------- K. labelled-domain construction: as first stated (CFG945/947)
form("K H1 action", R45, "Σ_q W(|Dχ_q|)", "W(|Dχ_q|) plus the constraints")  # the PDF text drops the summation sign
led("K one tether per catchment", "CFG945", "one tether per catchment", "one tether per catchment")
rd("K H1 uniform field Delta a = 0", D45, "Δa = 0 in a uniform host field", "falls with its stars (Δa = 0")
rd("K H1 tidal residual", R45, "PASS 1.6e-5 - 2.0e-3", sci("1.6e-5") + " to " + sci("2.0e-3"))
led("K restores gravity between objects", "CFG945", "restores Newtonian gravity BETWEEN distinct collapsed objects", "Newtonian gravity between distinct collapsed objects is restored")
rd("K costs: two labels miss NGC 3198", R45, "miss NGC 3198 by 4.12 / 4.61"); rd("K costs: q < 3.5e-7", R45, "q ≲ 3.5e-7", sci("3.5e-7"))
rd("K costs: no local seeding rule", D45, "No local rule was found", "no local seeding rule was found", ci=True)
rd("K costs: conserved only between label changes", R45, "Energy-momentum conserved only between label changes", "conserved only between label changes", ci=True)
rd("K costs: ghost inherited", D45, "R3θ's ghost is inherited", "inherits R3θ's ghost")
check("K split-galaxy error 8.6% (JSON)", f"{100 * r47['T-L']['canonical|simple|f=0.01']:.1f}" == "8.6" and "8.6% on NGC 3198 at f = 0.01" in flat)
rd("K dipole-free draw", D47, "a dipole-free relocation: the draw's centroid tied to the phantom's at all times", "centroid tied to the phantom's at all times")
form("K 1024^3 run", R47, "a 1024³ run")
check("K CFG950-952 landed (LEDGER rows and READMEs exist) and no in-progress statement remains in the TeX",
      all(row(f"CFG95{i}") for i in "012") and all(os.path.exists(os.path.join(CFG, d, "README.md")) for d in
      ("CFG950_ldt_construction", "CFG951_ldt_mergers_clusters", "CFG952_ldt_engine_design"))
      and not any(s in tex.lower() for s in ("in progress", "under construction", "no result exists", "no ledger result yet", "reserved")))
rd("K engine has no established parent (canonical v3 note)", TC18, "the class-A shear engine has no established physical parent", "its physical parent is not established")
has("K computational result", "computational result of the engine")

# ---------------------------------------------------------------- K2. CFG950: the construction written down and tested
R50, D50 = "CFG950_ldt_construction/README.md", "CFG950_ldt_construction/DERIVATION.md"
r50 = J("CFG950_ldt_construction/cfg950_results.json")
check("K2 CFG950 frozen class / post-hoc A1 class (JSON)", r50["class"] == "NOT CONSISTENT AS SPECIFIED" and r50["class_A1_post_hoc"] == "LDT CONDITIONAL"
      and r50["grades"]["f"] == "FAIL" and r50["grades_A1"]["f"] == "PASS" and r50["grades"]["e"] == "CONDITIONAL" and r50["grades"]["g"] == "CONDITIONAL"
      and all(r50["grades"][k] == "PASS" for k in "abcdhi") and "NOT CONSISTENT AS SPECIFIED under the frozen rule; LDT CONDITIONAL under post-hoc A1" in flat
      and "The construction (CFG950): NOT CONSISTENT AS SPECIFIED" in flat)
led("K2 CFG950 class (LEDGER)", "CFG950", "NOT CONSISTENT AS SPECIFIED under the frozen rule", "NOT CONSISTENT AS SPECIFIED under the frozen rule")
led("K2 CFG950 LDT CONDITIONAL under post-hoc A1", "CFG950", "LDT CONDITIONAL under post-hoc A1")
for s in ("Σ_q mc²n_q", "W_full(u_q) + (3γ/4K²)τ_q²", "λ_q(D_(q)²χ_q − Kmn_q)", "c⁴R/16πG"):
    check(f"K2 CFG950 action term '{s}' (LEDGER)", nsp(s) in nsp(row("CFG950")))
for s in (r"\sum_q mc^2n_q", r"W_{\rm full}(u_q)+\tfrac{3\gamma}{4K^2}\tau_q^2", r"\lambda_q\big(D_{(q)}^2\chi_q-Kmn_q\big)", r"q=0$ unlabelled dust"):
    check(f"K2 CFG950 action term in TeX '{s[:26]}'", s in tex)
led("K2 CFG950 q = 0 unlabelled dust", "CFG950", "q = 0 unlabelled dust", "q = 0 unlabelled dust")
led("K2 CFG950 no theta, no CFG944 ghost", "CFG950", "no θ in the action (no CFG944 ghost)", "There is no θ in the action, so CFG944's ghost does not arise")
rd("K2 CFG950 D-T cancels only own label", R50, "D-T cancels its own label's gravity only", "D-T cancels only a label's own gravity")
led("K2 CFG950 action-less, non-local label sector", "CFG950", "Action-less, non-local label sector", "The label sector is non-local and has no action")
led("K2 CFG950 theta-latch", "CFG950", "θ-latch at first collapse (θ ≤ 0) with contact inheritance within L*", "θ-latch at first collapse (θ ≤ 0) with contact inheritance within L*")
led("K2 CFG950 merge rule", "CFG950", "whole-label ball-domain merge rule (concentric labels tie, T-T)", "a whole-label ball-domain merge rule, forced because concentric labels tie (T-T)")
led("K2 CFG950 re-latch and debris", "CFG950", "one-way tidal re-latch; debris ≤ 3.5e-7", "a one-way tidal re-latch; debris ≤ " + sci("3.5e-7"))
check("K2 CFG950 (a) law 2.2e-16, BTFR 1, edge 454 / 413 kpc (JSON)", all(r50["K1"][f]["max_rel_vs_law"] < 2.3e-16 for f in ("canonical", "alt"))
      and all(abs(r50["a"]["btfr"][f]["numeric"] - 1) < 1e-6 for f in ("canonical", "alt"))
      and round(r50["a"]["a3"]["canonical"]["r_e_kpc"]) == 454 and round(r50["a"]["a3"]["alt"]["r_e_kpc"]) == 413
      and "The NGC 3198 law to " + sci("2.2e-16") + ", the BTFR limit 1 and a label edge at 454 / 413 kpc" in flat)
led("K2 CFG950 (b) growth n = 1 exactly", "CFG950", "no labels in the linear regime, growth n = 1 exactly", "no labels in the linear regime and growth n = 1 exactly")
check("K2 CFG950 (b) n = 1 (JSON)", "n = 1.000000000000" in r50["tests"]["b"]["detail"] and abs(r50["K2"]["n_dust"] - 1) < 1e-12)
check("K2 CFG950 (c) satellites 2.0e-3, 18/18 (JSON)", f"{max(r50['c']['eps_max'].values()):.1e}" == "2.0e-03" and "18/18" in r50["tests"]["c"]["detail"]
      and "(Δa/ghost ≤ " + sci("2.0e-3") + ", bound in 18/18)" in flat)
lonly("K2 CFG950 (c) LEDGER", "CFG950", "(Δa/g_host ≤ 2.0e-3, bound 18/18)")
check("K2 CFG950 (d) slip 1.54e-5 (JSON)", f"{r50['d']['s_847']:.2e}" == "1.54e-05" and "slip ≤ " + sci("1.54e-5") + "; a forced edge" in flat)
led("K2 CFG950 (h) edge, (i) EFE 0", "CFG950", "(h) edge forced, no SPARC point beyond it; (i) satellite EFE 0", "a forced edge with no SPARC point beyond it; satellite EFE 0")
check("K2 CFG950 (i) EFE exactly 0 (JSON)", all(v == 0.0 for v in r50["i"]["efe_uniform"].values()))
rd("K2 CFG950 hover and growth flag gone", R50, "The hover (CFG941/945) and the linear-growth flag (CFG938/941) are gone.")
led("K2 CFG950 momentum exact", "CFG950", "momentum exact through every label event", "Momentum is exact through every label event (" + sci("8e-14") + ")")
sonly("K2 CFG950 momentum 8e-14 (README)", R50, "momentum exact through latch, re-latch and merge (8e-14)")
led("K2 CFG950 energy not conserved", "CFG950", "ENERGY is not conserved by any dynamical field at label events", "energy is not conserved by any dynamical field at label events")
ev = r50["e"]["events"]
check("K2 CFG950 assembly 0.17-0.94, merger 0.54-0.70 (JSON)",
      f2(min(ev[f]["rel_lo"] for f in ev)) == "0.17" and f2(max(ev[f]["rel_hi"] for f in ev)) == "0.94"
      and f2(min(ev[f]["merger"][q]["rel_outside_wall"] for f in ev for q in ev[f]["merger"])) == "0.54"
      and f2(max(ev[f]["merger"][q]["rel_outside_wall"] for f in ev for q in ev[f]["merger"])) == "0.70"
      and "injects 0.17-0.94 of |Egrav" in flat and ", and a merger 0.54-0.70. Theorem T-LE" in flat)
lonly("K2 CFG950 assembly/merger (LEDGER)", "CFG950", "assembly injects 0.17-0.94 of |E_grav|")
led("K2 CFG950 T-LE statement", "CFG950", "theorem T-LE: bound cold medium cannot pay the labelling cost", "Theorem T-LE: bound cold medium cannot pay the labelling cost")
tle = r50["T-LE"]
check("K2 CFG950 T-LE Delta > 0 on 1e7-1e15, NGC 3198 (97 km/s)^2 (JSON)",
      all(g["Delta"] > 0 for f in ("canonical", "alt") for g in tle[f]["grid"]) and tle["canonical"]["grid"][0]["Mb"] == 1e7 and tle["canonical"]["grid"][-1]["Mb"] == 1e15
      and round(tle["canonical"]["Delta_NGC"] ** 0.5 / 1e3) == 97 and 96 <= tle["alt"]["Delta_NGC"] ** 0.5 / 1e3 <= 97
      and r50["structural"]["T-LE"] and "Δ ≈ (97 km/s)2 on NGC 3198" in flat)
sonly("K2 CFG950 T-LE (README)", R50, "T-LE: bound cold medium cannot pay (deficit Δ > 0 for M_b 1e7-1e15; NGC 3198 Δ ≈ (97 km/s)²)")
led("K2 CFG950 R-E non-dynamical label energy", "CFG950", "closed only by a non-dynamical label energy (R-E)", "The books close only through R-E, a declared non-dynamical label energy")
check("K2 CFG950 R-E cost <= 1.8e-6, PN ~3e-7 (JSON)", f"{max(ev[f]['RE_cost_max'] for f in ev):.1e}" == "1.8e-06"
      and all(f"{ev[f]['bianchi_PN']:.0e}" == "3e-07" for f in ev) and "(|eL" in flat and "/c2 ≤ " + sci("1.8e-6") + ", post-Newtonian residual" in flat and any(f"residual ∼{sp}{sci('3e-7')})" in flat for sp in ("", " ")))
sonly("K2 CFG950 R-E (README)", R50, "Closed only via R-E (|e_L|/c² ≤ 1.8e-6; PN residual ~3e-7)")
led("K2 CFG950 f3 pinned", "CFG950", "the only FAIL is the f3 toy metric, pinned by the innermost equal-mass shell at every resolution",
    "The frozen merger-toy metric f3 FAILS, pinned at the innermost equal-mass shell at every resolution")
led("K2 CFG950 (g) CFG938 premises", "CFG950", "(g) CONDITIONAL on CFG938's premises", "Well-posedness is CONDITIONAL on CFG938's premises")
ft = [x["f_theta"] for x in r50["T-theta"]]
check("K2 CFG950 theta-latch labels 47-76% (JSON)", f"{100 * min(ft):.0f}" == "47" and f"{100 * max(ft):.0f}" == "76"
      and "θ-latch labels hold only 47-76% of the engine's catchment mass" in flat)
lonly("K2 CFG950 47-76% (LEDGER)", "CFG950", "θ-latch labels hold only 47-76% of class A's catchment mass")
check("K2 CFG950 satellites' media 41-854x (JSON)", round(min(r50["R1"].values())) == 41 and round(max(r50["R1"].values())) == 854
      and "41-854 times their stars, act as baryons in their hosts' laws" in flat)
lonly("K2 CFG950 41-854x (LEDGER)", "CFG950", "satellites' own-label media (41-854× their stars) act as baryons in their hosts' laws")
st = {}
for s in r50["scorecard"]:
    st.setdefault(s["status"], []).append(s["gate"].split()[0])
check("K2 CFG950 scorecard (JSON)", st["PASS"] == ["A5", "C2"] and st["CONDITIONAL"] == ["A1", "A2", "B3", "C1"] and st["FAIL"] == ["C3"]
      and "B1" in st["UNTESTED"] and "D2" in st["UNTESTED"], json.dumps(st))
led("K2 CFG950 scorecard (LEDGER)", "CFG950", "PASS A5, C2; CONDITIONAL A1, A2, B3, C1; FAIL C3 (inherited from the law); UNTESTED incl. B1 (prescribed labels) and D2 (needs an LDT PM engine, CFG952)",
    "(PASS A5, C2; CONDITIONAL A1, A2, B3, C1; FAIL C3, inherited from the law), with B1 (prescribed labels) and D2 (it needs an LDT engine) UNTESTED")
check("K2 CFG950 K 7/7 (JSON)", r50["K_all"] is True); led("K2 CFG950 K 7/7, MUTATE 6/6 (LEDGER)", "CFG950", "K 7/7; MUTATE 6/6", "K 7/7; MUTATE 6/6 bite")
led("K2 CFG950 A1 post hoc", "CFG950", "A1 fb9af871f POST HOC", "CFG950 A1 (the merger-toy metric f3 replaced after the first main run; the frozen class is reported alongside)")
sonly("K2 CFG950 A1 after first complete main run", "CFG950_ldt_construction/AMENDMENT_A1_post_hoc.md", "Written after the first complete main run")
sonly("K2 CFG950 hand expectations", "CFG950_ldt_construction/FROZEN_CRITERIA.md", "Hand expectations, formed while designing; no script run.")

# ---------------------------------------------------------------- K3. CFG951: mergers and clusters under labels
R51 = "CFG951_ldt_mergers_clusters/README.md"
r51 = J("CFG951_ldt_mergers_clusters/cfg951_results.json")
check("K3 CFG951 FAIL, every variant INCONSISTENT on both footings (JSON)", r51["overall"] == "FAIL" and all(v == "INCONSISTENT" for v in r51["variant_class"].values())
      and all(r51["class_a"][m]["per_footing"] == {"canonical": "INCONSISTENT", "alt": "INCONSISTENT"} for m in ("M1", "M2", "M3"))
      and "Mergers and clusters (CFG951): FAIL" in flat and "All three merge variants are INCONSISTENT on both footings" in flat)
lonly("K3 CFG951 LEDGER class", "CFG951", "LDT MERGERS FAIL - all three merge variants INCONSISTENT on both footings")
rd("K3 CFG951 froze before CFG950", R51, "CFG950 (the formal LDT specification) had not appeared when this lane froze", "CFG951 froze before CFG950 appeared")
rd("K3 CFG951 working statement source", R51, "is taken from CFG945 H1 and CFG947 N1 / M-R", "CFG945 H1 and CFG947 N1 / M-R, with full Newtonian sourcing between labels")
rd("K3 CFG951 post-hoc hypothesis test", R51, "HYPOTHESIS TEST, POST HOC (every target was read before freezing), zero new constants",
   "post-hoc hypothesis test (its targets were read before freezing) with zero new constants")
check("K3 CFG951 no member coalesces (JSON)", all(r51["diagnostics"][f]["M3"]["f_coal_med"] < 1e-6 for f in ("canonical", "alt")))
led("K3 CFG951 members source the host law", "CFG951", "cluster members keep their own-label media (no member coalesces at pericentre)",
    "Cluster members keep their own labelled media (no member coalesces at pericentre), and those media source the host's law")
tr51 = r51["T_R"]
c3, a3_ = tr51["canonical"]["M3"], tr51["alt"]["M3"]
check("K3 CFG951 eRASS1 A_OUTER and Z (JSON)", f"{c3['A']['OUTER'][0]:.3f} ± {c3['A']['OUTER'][1]:.3f}" == "0.556 ± 0.048" and f"{c3['Z_outer']:.1f}" == "-9.3"
      and f"{a3_['A']['OUTER'][0]:.3f} ± {a3_['A']['OUTER'][1]:.3f}" == "0.496 ± 0.043" and f"{a3_['Z_outer']:.1f}" == "-11.9"
      and "AOUTER = 0.556 ± 0.048 (Z = -9.3) / 0.496 ± 0.043 (Z = -11.9)" in flat and "(Z = -9.3 canonical, -11.9 alternative)" in flat)
lonly("K3 CFG951 eRASS1 (LEDGER)", "CFG951", "eRASS1 A_OUTER 0.556 ± 0.048 (Z −9.3) / 0.496 ± 0.043 (Z −11.9)")
check("K3 CFG951 H-MM 0.765 / 0.744 (JSON)", f3(tr51["canonical"]["hmm"]["A"]["OUTER"][0]) == "0.765" and f3(tr51["alt"]["hmm"]["A"]["OUTER"][0]) == "0.744"
      and "H-MM (0.765 / 0.744, CFG726)" in flat)
lonly("K3 CFG951 worse than H-MM", "CFG951", "merger memory worse than CFG726's H-MM")
check("K3 CFG951 every bracket fails eRASS1 OUTER (JSON)", all(c == "INCONSISTENT" for m in ("M1", "M3") for c in r51["class_a"][m]["brackets"].values()))
led("K3 CFG951 brackets (LEDGER)", "CFG951", "every bracket (King r_J truncation, own-domain coupling, ICM-sourced halos) still fails eRASS1 OUTER",
    "Every bracket (King truncation, own-domain coupling, ICM-sourced halos) still fails eRASS1 OUTER")
check("K3 CFG951 A_MID and MID/OUTER (JSON)", f3(c3["A"]["MID"][0]) == "1.213" and f3(a3_["A"]["MID"][0]) == "1.089" and f2(c3["A"]["MID"][0] / c3["A"]["OUTER"][0]) == "2.18"
      and "AMID falls to 1.213 / 1.089 only by overshooting OUTER (MID/OUTER 2.18, against the law's 1.89)" in flat)
lonly("K3 CFG951 MID/OUTER (LEDGER)", "CFG951", "MID/OUTER 2.18, worse than the law's 1.89")
led("K3 CFG951 untethered reading needs a selector", "CFG951", "an untethered-host reading (CFG949) fits but needs a selector LDT does not have",
    "the untethered-host reading (CFG949) fits but needs a selector LDT does not have")
check("K3 CFG951 Bullet classes (JSON)", r51["class_c"] == {"M1": "INCONSISTENT", "M2": "UNDERDETERMINED", "M3": "UNDERDETERMINED"})
led("K3 CFG951 Bullet (LEDGER)", "CFG951", "Bullet: UNDERDETERMINED for two variants (no measured pericentre), INCONSISTENT for instant relabelling",
    "The Bullet is UNDERDETERMINED for two variants (no measured pericentre) and INCONSISTENT for instant relabelling")
jt = [v["variants"][m]["J_max"] for v in r51["toy"].values() for m in v["variants"]]
ja = [v["variants"][m]["J_max"] for v in r51["toy_A1_iso_tau_posthoc"].values() for m in v["variants"]]
check("K3 CFG951 continuity J 1.16-2.34, A1 0.70-1.63 (JSON)", f2(min(jt)) == "1.16" and f2(max(jt)) == "2.34" and f2(min(ja)) == "0.70" and f2(max(ja)) == "1.63"
      and all(v == "INCONSISTENT" for v in r51["class_d"].values()) and "changes by 1.16-2.34 per dynamical time (0.70-1.63 in the post-hoc A1 variant)" in flat)
lonly("K3 CFG951 continuity (LEDGER)", "CFG951", "(d) continuity FAILS for all (phantom changes 0.70-2.34 per dynamical time)")
ud = [r51["udg"][f]["by"]["dmean"]["mean_dE"] for f in ("canonical", "alt")]
check("K3 CFG951 UDG ceiling +0.054 ln, NOT DIAGNOSTIC (JSON; the README quotes 0.054 for 0.0543-0.0545)", abs(min(ud) - 0.054) < 0.0005 and max(ud) < 0.0546
      and all(v == "NOT DIAGNOSTIC" for v in r51["class_e"].values()) and "the ceiling rises by +0.054 in natural log (an upper bound), still not diagnostic" in flat)
lonly("K3 CFG951 UDGs (LEDGER)", "CFG951", "Coma UDGs keep their labels; the ceiling rises by ≤ +0.054 ln (still not diagnostic)")
sonly("K3 CFG951 upper bound", R51, "This is an upper bound")
led("K3 CFG951 core problem", "CFG951", "Inter-label sourcing at full Newtonian strength breaks every multi-label system; dropping it would undo CFG945's restored inter-label gravity.")
led("K3 CFG951 K 9/9, MUTATE bite", "CFG951", "K 9/9 exact; MUTATE all bite", "K 9/9; every tooth bites")
led("K3 CFG951 318 eRASS1", "CFG951", "eRASS1", "On the 318 eRASS1 clusters"); sonly("K3 CFG951 318 clusters (README)", R51, "eRASS1: 318 clusters")
led("K3 CFG951 A1 post hoc", "CFG951", "A1 e633ca969 POST HOC after the first MAIN run", "CFG951 A1 (a reported toy variant after the first main run; no class change)")
sonly("K3 CFG951 A1 no class change", "CFG951_ldt_mergers_clusters/AMENDMENT_A1_post_hoc.md", "Reported only; no class changes")

# ---------------------------------------------------------------- K4. CFG952: an engine for labelled domains
R52 = "CFG952_ldt_engine_design/README.md"
r52 = J("CFG952_ldt_engine_design/cfg952_results.json"); p52 = J("CFG952_ldt_engine_design/cfg952_results_POSTHOC.json")
check("K4 CFG952 SMOKE PARTIAL, grades, K pass (JSON)", r52["class"] == "SMOKE PARTIAL" and r52["grades"] == {"a0": True, "a1": True, "a2": True, "b1": False, "c1": False, "c2": False}
      and r52["K_all_pass"] is True and "An engine for it (CFG952): SMOKE PARTIAL" in flat)
led("K4 CFG952 no production run", "CFG952", "DESIGN + 64³ smoke tests only, no production run", "smoke-tested in a separate 643 toy; no production run was made")
sn = r52["a"]["snapshots"].values()
check("K4 CFG952 purity 1.0, E4 EFE -0.114 dex (JSON)", all(v["purity_s"] == 1.0 and v["purity_H"] == 1.0 for v in sn) and f3(min(v["E4_EFE_dex"] for v in sn)) == "-0.114"
      and "persist through infall (purity 1.0)" in flat and "has an EFE of up to -0.114 dex in the toy" in flat)
lonly("K4 CFG952 own-domain phantom EFE-free (LEDGER)", "CFG952", "the own-domain phantom is EFE-free (a0-a2 PASS; the engine's E4 shows −0.114 dex EFE in the toy)")
check("K4 CFG952 draw book 81 / 6.5 post hoc (JSON)", round(r52["b"]["DIPSLAVE"]["book"]["max_B_over_I"]) == 81 and f"{p52['PH_b']['book']['max_B_over_I']:.1f}" == "6.5"
      and "(book residual 81; 6.5 under the post-hoc fallback)" in flat)
lonly("K4 CFG952 draw INFEASIBLE (LEDGER)", "CFG952", "the momentum-slaved positive draw is INFEASIBLE (book residual 81, 6.5 post hoc - a capacity limit of the non-local formulation)")
has("K4 CFG952 capacity limit in PDF", "a capacity limit of the non-local formulation")
c52 = r52["c"]
check("K4 CFG952 merge blend 0.025 / 2.77, peak 0.94 / 0.053 (JSON)", f3(c52["J_trigger"]) == "0.025" and f2(p52["PH_c_INSTANT"]["J_trigger"]) == "2.77"
      and f2(c52["max_J"]) == "0.94" and f3(p52["PH_c_RAMP"]["max_J"]) == "0.053" and c52["max_zs"] > 1e-12
      and "cuts the jump at the trigger to 0.025 (instant relabelling: 2.77), but its peak per-step change, 0.94 as frozen and 0.053 post hoc, exceeds the frozen 0.03 line" in flat)
lonly("K4 CFG952 merger continuity (LEDGER)", "CFG952", "merger continuity FAILS as frozen (blend 0.025 at the trigger vs 2.77 instant")
sonly("K4 CFG952 frozen max J 0.94 (README)", R52, "RAMP: max J_Φ 0.94 (line 0.03)")
check("K4 CFG952 M-R does not fire (JSON)", all(t_["mr1_bound_A"] > 0.99 for t_ in c52["triggers"]) and "and zero-sum breaks on failed Newton steps. CFG947's merge rule" in flat and "never fires in equal-mass mergers. The engine's effective RMIN" in flat)  # a page break may fall inside the sentence
lonly("K4 CFG952 M-R (LEDGER)", "CFG952", "CFG947's merge rule never fires in equal-mass mergers")
th = r52["EST"]["thresholds"]
eff, ctl = th["CFG947_inputs_effective_node_1024"], th["CFG947_inputs_R0.78125 (control: 4.815e10)"]
check("K4 CFG952 effective RMIN 1.0471 Mpc/h -> 2.19e11 Msun, x4.5 (JSON)", f"{eff['R']:.4f}" == "1.0471" and f"{eff['M_b_ret_Msun']:.2e}" == "2.19e+11"
      and f"{eff['M_b_ret_Msun'] / ctl['M_b_ret_Msun']:.1f}" == "4.5" and f"{ctl['M_b_ret_Msun']:.3e}" == "4.815e+10"
      and "effective RMIN at 10243 equal to 1.0471 Mpc/h" in flat and "Mb,ret ≥ " + sci("2.19e11") in flat and "4.5 times CFG947's continuous figure" in flat)
lonly("K4 CFG952 RMIN (LEDGER)", "CFG952", "the law acts only on systems with retained baryons ≥ 2.19e11 M☉ (4.5× CFG947's figure); 256³ validation cannot reproduce this")
has("K4 CFG952 256^3 in PDF", "a 2563 validation cannot reproduce this")
has("K4 CFG952 abstract RMIN", "only above " + sci("2.19e11"))
led("K4 CFG952 1024^3 cost 17-18 h", "CFG952", "1024³ cost ≈ 17-18 h per footing at ≲ 5000 labels", "(17-18 h per footing at ≲ 5000 labels)")
led("K4 CFG952 prereg NOT frozen", "CFG952", "Pre-registration draft for an LDT 1024³ run written, NOT frozen", "its pre-registration is drafted, not frozen")
led("K4 CFG952 A1 pre-result, A2 post hoc", "CFG952", "A1 7a3ade021 pre-result; A2 4141650f1 post hoc", "CFG952 A2 (a reported fallback stage after the main results; no grade change)")
sonly("K4 CFG952 A2 no grade change", "CFG952_ldt_engine_design/AMENDMENT_A2_post_hoc.md", "Nothing in this amendment can move a grade")
check("K4 CFG952 post-hoc reading: c1 not explained (JSON)", p52["reading_merge_transition"] == "c1's frozen failure NOT explained by the fallback artefact")

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
for s in ("CFG938 A1", "CFG939 A2", "CFG945 A1", "CFG946 A1", "CFG932 A1", "CFG940 A1", "CFG948 A1", "CFG949 A1", "CFG939 A1, CFG941 A1, CFG947 A1", "CFG944 has none",
          "CFG935 A2 (post-result for the dark-energy repair), A3-A5 (post-result compute caps) and its post-hoc runs (no verdict weight)",
          "CFG950 A1", "CFG951 A1", "CFG951 as a whole is a post-hoc hypothesis test", "CFG952 A2",
          "Pre-result amendments: CFG935 A0, CFG939 A1, CFG941 A1, CFG947 A1, CFG952 A1", "CFG935 A1 is an implementation fix"):
    has(f"M disclosure '{s[:60]}'", s)
kept = ("CFG938_medium_continuum_eft/cfg938_firstrun_S3efail.out", "CFG939_lagrangian_displacement_shell_crossing/cfg939_firstrun_dt0005.out",
        "CFG939_lagrangian_displacement_shell_crossing/cfg939_secondrun_dt00125.out", "CFG945_gated_tether_satellite_hover/cfg945_MUTATE_firstrun_M5toothless.out",
        "CFG945_gated_tether_satellite_hover/cfg945_main_attempt1_killed_pointstars.out", "CFG946_option2_phantom_not_cold/cfg946_firstrun_npbool.out",
        "CFG947_option3_nonlocal_parent/cfg947_firstrun_TLcheck.out", "CFG949_clusters_untethered/cfg949_K_RUN1.out", "CFG949_clusters_untethered/cfg949_RUN1_acceptbug.out",
        "CFG935_energy_conserving_settling/parts/preA1_Ra2_I.json", "CFG935_energy_conserving_settling/parts/preA2_Rd_L.json",
        "CFG950_ldt_construction/cfg950_firstrun_f3frozen.out", "CFG951_ldt_mergers_clusters/cfg951_RUN1_toyartefact.out",
        "CFG952_ldt_engine_design/cfg952_MUTATE_firstrun_rssguard.out", "CFG952_ldt_engine_design/cfg952_firstrun_LINcrash.out",
        "CFG952_ldt_engine_design/cfg952_POSTHOC_firstrun_nanbeta.out", "CFG952_ldt_engine_design/cfg952_POSTHOC_secondrun_bracket.out")
check("M superseded runs disclosed and kept on disk", all(os.path.exists(os.path.join(CFG, k)) for k in kept) and "Superseded runs are kept" in flat
      and "CFG935's pre-A1 and pre-A2 records, the first main runs of CFG950 and CFG951, and CFG952's killed first mutation run, crashed first main run and two failed post-hoc attempts" in flat)
rd("M CFG944 text-only edits", R44, "Three output strings were changed", "reworded three output strings after its first full run; no number changed")
rd("M CFG949 graded numbers unchanged", R49, "Every graded number is identical", "(graded numbers unchanged)")
has("M companion PAPER56", "PAPER56"); has("M companion PAPER55", "PAPER55")
has("M lane list updated", "CFG947, CFG950, CFG951, CFG952 (structural); CFG932, CFG935 and the ledger row CFG932-")
rd("M citation eRASS1 (CFG687 criteria)", "CFG687_erass1_shear_stack/FROZEN_CRITERIA.md", "Bulbul+2024, VizieR J/A+A/685/A106", "E. Bulbul et al., A&A 685, A106 (2024)")
lei = norm(open(os.path.join(HERE, "..", "..", "real_research", "data", "alfalfa_huds_leisman2017.tsv"), encoding="utf-8").read(3000))
check("M citation Leisman et al. ApJ 842, 133 (VizieR header of the record's table)", "J/ApJ/842/133" in lei and "Leisman+, 2017" in lei
      and "L. Leisman et al., ApJ 842, 133 (2017)" in flat)
rd("M citation Coma UDG table (CFG948)", R48, "the Coma table (Freundlich+2022", "J. Freundlich et al., A&A 658, A26 (2022) (Coma UDGs)")
# ---- deposit-prep citation pass (2026-10-21). Journal references verified against the publisher DOI records (Crossref):
#   Freundlich+22 10.1051/0004-6361/202142060; Giblin+21 10.1051/0004-6361/202038850; Lelli+15 10.1051/0004-6361/201526613;
#   van Dokkum+18 10.1038/nature25767; van Dokkum+19 10.3847/2041-8213/ab0d92; SPARC 10.3847/0004-6256/152/6/157;
#   Milgrom 83 10.1086/161130; Bekenstein & Milgrom 84 10.1086/162570; Milgrom 10 10.1111/j.1365-2966.2009.16184.x;
#   Famaey & Binney 05 10.1111/j.1365-2966.2005.09474.x; Bulbul+24 10.1051/0004-6361/202348264; Leisman+17 10.3847/1538-4357/aa7575;
#   McQuinn+22 10.3847/1538-4357/ac9285. PAPER55 = 10.5281/zenodo.23482936 (public Zenodo record).
for s in ("B. Giblin et al., A&A 645, A105 (2021) (KiDS-1000 shear", "F. Lelli et al., A&A 584, A113 (2015) (tidal dwarfs)",
          "P. van Dokkum et al., Nature 555, 629 (2018) and ApJL 874, L5 (2019) (DF2, DF4", "F. Lelli, S. McGaugh, J. Schombert, AJ 152, 157 (2016)",
          "M. Milgrom, ApJ 270, 365 (1983)", "J. Bekenstein, M. Milgrom, ApJ 286, 7 (1984)", "M. Milgrom, MNRAS 403, 886 (2010)",
          "B. Famaey, J. Binney, MNRAS 363, 603 (2005)", "K. B. W. McQuinn et al., ApJ 940, 8 (2022)", "PAPER55 (doi:10.5281/zenodo.23482936)"):
    has(f"M citation '{s[:48]}'", s)
tdg = norm(open(os.path.join(HERE, "..", "..", "real_research", "data", "tidal_dwarfs", "PROVENANCE.md"), encoding="utf-8").read())
check("M citation Lelli et al. 2015 matches the record's TDG table provenance", "Lelli et al. 2015, A&A 584, A113" in tdg)
check("M CFG655 holds the DF2/DF4 dispersions cited", "Danieli+2019" in src("CFG655_ngc1052_trail_supply/README.md") and "Shen+2023" in src("CFG655_ngc1052_trail_supply/README.md"))
check("M CFG948 used the Lelli+15 TDGs and CFG655's DF2/DF4 table", "the Lelli+15 TDG table" in src(R48) and "CFG655's DF2/DF4 table" in src(R48))
check("M CFG686 shear is KiDS-1000 SOM-gold", "KiDS-1000 SOM-gold" in src("CFG686_cluster_shear_vs_law/FROZEN_CRITERIA.md"))
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
