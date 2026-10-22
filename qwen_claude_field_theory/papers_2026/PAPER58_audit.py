#!/usr/bin/env python3
"""PAPER58 audit: the built PDF must be newer than the TeX and 5-8 pages long; every quoted number must match the committed
lane outputs of doors_push_2026_10_22/ (the lane's *_results.json where the number is stored there; otherwise the lane's .out,
README, PROVENANCE or the git record); every cited lane commit must exist and touch that lane; the six doors-push errata and
the DSF-21 postulate correction must exist; the pending lanes (D6, D7c, D7d) must be marked pending in the TeX and must
still have no committed result (if a result lands, this audit FAILS until the paper folds it in); citations must match the
record's citation files; no forbidden claim, local path or personal name may appear.
Run: python3 PAPER58_audit.py (exit 0 only if all pass).  Read-only: it opens committed files, git and the PDF, nothing else."""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
DP = os.path.join(ROOT, "doors_push_2026_10_22")
TEX = os.path.join(HERE, "PAPER58_doors_push_2026.tex")
PDF = os.path.join(HERE, "PAPER58_doors_push_2026.pdf")
ZJ = os.path.join(HERE, "PAPER58_doors_push_2026.zenodo.json")
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
                 (" ", " "), ("µ", "μ"), ("∆", "Δ"), ("ϕ", "φ"), ("∗", "*"), ("**", ""), ("\\|", "|")):
        t = t.replace(a, b)
    t = t.translate(SUB)
    t = re.sub(r"\s*×\s*", "x", t)
    t = re.sub(r"(?<=\d)\s*-\s*(?=\d)", "-", t)
    t = re.sub(r"(?<=\w) (?=[,.;:)])", "", t)
    t = re.sub(r"\s*±\s*", " ± ", t)
    return re.sub(r"\s+", " ", t)


def dehyph(t):
    return re.sub(r"([a-z])- ([a-z])", r"\1\2", t)


def keephyph(t):
    return re.sub(r"([A-Za-z])- ([A-Za-z])", r"\1-\2", t)


def sci(x, d):
    """value -> how the PDF renders m\\times10^{e} after norm, e.g. 6.3355x107, 1.6x10-28"""
    m, e = f"{x:.{d}e}".split("e")
    return f"{m}x10{int(e)}"


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, cwd=ROOT)


# ---------------------------------------------------------------- A. build
check("A1 PDF newer than TeX", os.path.getmtime(PDF) >= os.path.getmtime(TEX))
pages = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", PDF], capture_output=True, text=True, check=True).stdout).group(1))
check("A2 page count 5-10", 5 <= pages <= 10, f"{pages} pages")
raw = [norm(subprocess.run(["pdftotext"] + m + [PDF, "-"], capture_output=True, text=True, check=True).stdout) for m in (["-layout"], [], ["-raw"])]
flat = " ||| ".join(raw + [keephyph(x) for x in raw] + [dehyph(x) for x in raw])
low = flat.lower()
tex = open(TEX, encoding="utf-8").read()


def has(name, s):
    s = norm(s)
    check(name, s in flat, s)


def J(lane, fname):
    return json.load(open(os.path.join(DP, lane, fname)))


def get(d, *keys):
    for k in keys:
        d = d[k]
    return d


def num(name, value_str, ctx):
    """value_str is formatted from a committed JSON value; ctx (with {}) is the PDF wording around it"""
    s = norm(ctx.format(value_str))
    check(name, s in flat, s)


def txt(lane, fname):
    return norm(open(os.path.join(DP, lane, fname), encoding="utf-8").read())


def rd(name, lane, fname, s, pdf_s=None):
    """s must be in the lane file AND (s, or pdf_s) in the PDF"""
    s, p = norm(s), norm(pdf_s or s)
    check(name, s in txt(lane, fname) and p in flat, f"{lane}/{fname}: '{s}'" + (f" / PDF '{p}'" if pdf_s else ""))


def outline(lane, fname):
    t = open(os.path.join(DP, lane, fname), encoding="utf-8").read()
    m = re.findall(r"COMPLETE: (\d+)/(\d+) checks PASS", t)
    return f"{m[-1][0]}/{m[-1][1]}" if m else None


f2 = lambda x: f"{x:.2f}"
f3 = lambda x: f"{x:.3f}"
f4 = lambda x: f"{x:.4f}"

# ---------------------------------------------------------------- B. settings
d7 = J("D7_turnoff_yt", "d7_turnoff_yt_results.json")
d7b = J("D7b_cassini_Q2", "d7b_cassini_q2_results.json")
num("B footings (D7b inputs)", f"{sci(d7b['inputs']['a0']['canonical'], 2)} and {sci(d7b['inputs']['a0']['alt'], 2)}", "({} m s-2")
num("B thermal kappa Z/4pi (D7)", f"{d7['numbers']['kappa_thermal']:.6f}", "κ = Z/4π = {}")
num("B Z (D7)", f"{d7['numbers']['Z']:.5f}", "= {})")
c = git("show", "-s", "--format=%s%n%b", "d3e4110528").stdout
check("B DSF-21 postulate correction d3e4110528", "POSTULATE" in c and "1605.07458" in c and "astro-ph/9805346" in c and "d3e4110528" in flat)
th = open(os.path.join(ROOT, "deepseek_push", "DS_FINAL_2026_10_21", "THEORY.md"), encoding="utf-8").read()
check("B Milgrom relation and eq. 5 in the record", "arXiv:1605.07458, eq. 5" in th and "arXiv:1605.07458, eq. 5" in flat)
has("B kappa fitted", "κ = 1 2 is fitted") if "κ = 1 2 is fitted" in flat else has("B kappa fitted", "is fitted; the theory is not closed")

# ---------------------------------------------------------------- C. lane table: checks, verdicts, commits
LANES = {  # lane dir: (out file, table checks, verdict word in README, commits)
    "D1_skew_preflight": ("d1_skew_preflight.out", "10/10", "SCOPED NO-GO", ["1f956de1e8", "ad9bea8355"]),
    "D2_wide_binary_fork": ("d2_wide_binary_fork.out", "7/7", "CRISP FINDING", ["c8960e6424", "c27b941b99"]),
    "D3_cfg960_status": (None, None, "CRISP FINDING", ["77d59a9a38"]),
    "D4_alma_status": ("d4_alma_status.out", "6/6", "CRISP FINDING", ["3537e6f817", "f81efdcf6f"]),
    "D5_kappa_four": ("d5_kappa_four.out", "8/8", "SCOPED NO-GO", ["91ec2c9d07", "962007715e"]),
    "D6_u_mechanism": ("d6_u_mechanism.out", "6/7", "CRISP FINDING", ["3082c43c79", "daf92d2d11", "b21dda1a2d"]),
    "D7c_q2_rar_gate": ("d7c_q2_rar_gate.out", "5/6", "SCOPED NO-GO", ["e9e5349368", "26b5db080f"]),
    "D7d_screened_q2": ("d7d_screened_q2.out", "10/10", "CRISP FINDING", ["a13e418498", "e1ba64cf92", "b26f14bb82"]),
    "E1_input_audit": ("e1_input_audit.out", "6/6", "CRISP FINDING", ["581d52210b", "77a8b2d4a6"]),
    "E2_field_equation": ("e2_field_equation.out", "10/10", "CRISP FINDING", ["021ee82abb", "474050bcd8"]),
    "E3_dwarf_excess": ("e3_dwarf_excess.out", "6/6", "CRISP FINDING", ["5686635887", "c5e4196bb9"]),
    "E4_fitted_three": ("e4_fitted_three.out", "6/6", "CRISP FINDING", ["9cc8fcae21", "9b3dfb1000", "c5a9768e6a"]),
    "E5_parent_logic": ("e5_parent_logic.out", "14/15", "SCOPED NO-GO", ["039c76d2f9", "ab0f5d006c", "08e3c1bfbc"]),
    "D7_turnoff_yt": ("d7_turnoff_yt.out", "11/11", "SCOPED NO-GO", ["f2e0423a60", "a2a07b53d9"]),
    "D7b_cassini_Q2": ("d7b_cassini_q2.out", "7/8", "CRISP FINDING", ["c6a0b6f3c7", "9542a09f54"]),
    "D8_Lstar_value": ("d8_lstar_value.out", "5/5", "CRISP FINDING", ["3327019734", "3d5eb3ead9", "f1da138742", "ce9340ccbc", "95a7ec3a41"]),
    "D8b_sigma_universality": ("d8b_sigma_universality.out", "5/5", "CRISP FINDING", ["97ec7892fa", "8a9f0f1234"]),
    "D9_uv_parent": (None, None, "SCOPED NO-GO", ["bfb93eb61c", "2edcee066c", "7bdd5fee57"]),
    "D9b_A33_multiplier": ("d9b_a33_multiplier.out", "14/14", "SCOPED NO-GO", ["ce12fb3210", "61883a565f"]),
}
for lane, (out, chk, verdict, commits) in LANES.items():
    if out:
        check(f"C {lane} checks {chk} (.out)", outline(lane, out) == chk, f"{outline(lane, out)}")
    if verdict:
        check(f"C {lane} verdict '{verdict}' (README)", verdict in txt(lane, "README.md"))
    for h in commits:
        files = git("show", "--name-only", "--format=", h).stdout
        check(f"C {lane} commit {h} exists, touches lane, cited in PDF", f"doors_push_2026_10_22/{lane}/" in files and h in flat)
check("C D8 Stilp run 2/2 (.out)", outline("D8_Lstar_value", "d8_stilp2013.out") == "2/2" and "5/5, 2/2" in flat)
d9 = J("D9_uv_parent", "d9_uv_parent_results.json")
s9 = d9["summary"]
check("C D9 frozen 9/12 + A1 3/3 (JSON)", (s9["frozen_pass"], s9["frozen_total"], s9["A1_pass"], s9["A1_total"]) == (9, 12, 3, 3) and "9/12 + 3/3" in flat
      and not any(d9["checks"][k]["pass"] for k in ("U2", "U4", "U5")))
for lane, mut, want in (("D1_skew_preflight", "d1_skew_preflight_MUTATE.out", "9/10"), ("D2_wide_binary_fork", "d2_wide_binary_fork_MUTATE.out", "6/7"),
                        ("D4_alma_status", "d4_alma_status_MUTATE.out", "5/6"), ("D5_kappa_four", "d5_kappa_four_MUTATE.out", "6/8"),
                        ("D7_turnoff_yt", "d7_turnoff_yt_MUTATE.out", "3/11"), ("D7b_cassini_Q2", "d7b_cassini_q2_MUTATE.out", "3/8"),
                        ("D8_Lstar_value", "d8_lstar_value_MUTATE.out", "4/5"), ("D8_Lstar_value", "d8_stilp2013_MUTATE.out", "1/2"),
                        ("D8b_sigma_universality", "d8b_sigma_universality_MUTATE.out", "4/5"), ("D9_uv_parent", "d9_uv_parent_MUTATE.out", "9/15"),
                        ("D9b_A33_multiplier", "d9b_a33_multiplier_MUTATE.out", "12/14"), ("D6_u_mechanism", "d6_u_mechanism_MUTATE.out", "5/7"), ("D7c_q2_rar_gate", "d7c_q2_rar_gate_MUTATE.out", "3/6"),
                        ("D7c_q2_rar_gate", "d7c_q2_rar_gate_firstrun.out", "4/6"),
                        ("D7d_screened_q2", "d7d_screened_q2_MUTATE.out", "2/4"), ("E1_input_audit", "e1_input_audit_MUTATE.out", "5/6"),
                        ("E2_field_equation", "e2_field_equation_MUTATE.out", "9/10"), ("E3_dwarf_excess", "e3_dwarf_excess_MUTATE.out", "5/6"),
                        ("E4_fitted_three", "e4_fitted_three_MUTATE.out", "5/6"), ("E5_parent_logic", "e5_parent_logic_MUTATE.out", "11/15")):
    check(f"C {lane} mutation run bites ({mut})", outline(lane, mut) == want, f"{outline(lane, mut)}")

# ---------------------------------------------------------------- D. D5 kappa
d5 = J("D5_kappa_four", "d5_kappa_four_results.json")
check("D5 3,900 monomials (JSON K1)", "3900 monomials" in d5["checks"]["K1"]["value"] and "3,900 enumerated monomials" in flat)
check("D5 1/2 not in S1, Z/4pi in S1 (JSON)", d5["angle_T"]["half_in_S1"] is False and d5["angle_T"]["Z4pi_in_S1"] is True and d5["angle_T"]["half_in_S2"] is True)
num("D5 16 constructions (JSON)", str(d5["angle_T"]["n_half_constructions_S2"]), "all {} constructions that give")
check("D5 m=-1/2, q^2=3/32 (JSON K4)", "m=-1/2, q^2=3/32" in d5["checks"]["K4"]["value"] and "q2 = 3/32" in flat)
lee = d5["angle_T"]["lee"]
check("D5 P_cover 1.0000 everywhere (JSON)", all(f4(v["P_cover"]) == "1.0000" for v in lee.values()) and "probability 1.0000" in flat)
num("D5 minimal subclass 11 values (JSON)", str(lee["S1_minimal_CFG493"]["n_vals"]), "the {}-value minimal subclass")
num("D5 a0(2.5)/a0(0) (JSON)", f4(d5["angle_T"]["Hz2p5_over_H0"]), "= {}, the record's rival law")
ft = d5["angle_T"]["footings"]
num("D5 nearest S1 (JSON)", f"{ft['canonical']['nearest_S1']['kappa']:.5f} (canonical) and {ft['alt']['nearest_S1']['kappa']:.5f} (alternative)", "{}")
check("D5 A19 grid (JSON)", [g["R"] for g in d5["angle_A"]["CFG493"]["grid"]] == [1, 2, 3, 4, 8, 12, 16] and "R ∈ {1, 2, 3, 4, 8, 12, 16}" in flat)
b = d5["inputs"]["bands"]["CFG493"]
num("D5 CFG493 band (JSON)", f"{b[0]:.3f} ± {b[1]:.3f}", "κ = {})")
num("D5 5 of 7 within 2 sigma (JSON)", str(d5["angle_A"]["CFG493"]["n_within_2sigma"]), "{} of 7 lie within 2σ")
gz = {g["R"]: g["z"] for g in d5["angle_A"]["CFG493"]["grid"]}
check("D5 R=8 closer than R=4 (JSON)", d5["angle_A"]["CFG493"]["closer_than_R4"] == [8] and f"(-{abs(gz[8]):.2f}σ) is closer than R = 4 (+{gz[4]:.2f}σ)" in flat,
      f"-{abs(gz[8]):.2f} / +{gz[4]:.2f}")
check("D5 verdict CONTRADICTED both bands (JSON)", d5["angle_A"]["CFG493"]["verdict"] == d5["angle_A"]["A81_DE"]["verdict"] == "CONTRADICTED")

# ---------------------------------------------------------------- E. D7 turn-off
n7 = d7["numbers"]
num("D7 2557.4 x B_E (JSON)", f"{n7['K2_1p5AU']['can']['ratio_to_BE']:.1f}", "that is {} times the planetary bound")
num("D7 3087.4 x B_E alt (JSON)", f"{n7['K2_1p5AU']['alt']['ratio_to_BE']:.1f}", "and {} times on the alternative")
check("D7 monopole unchanged < 1e-9 (JSON)", all(abs(n7["K3_EFE"][f]["monopole_ratio"] - 1) < 1e-9 for f in ("can", "alt")) and "less than 10-9" in flat)
num("D7 y_t values (JSON)", f"{n7['yt_quoted']:.4f} (quoted Λ), {n7['yt_32pi']:.4f} (32π), {n7['yt_alt']:.4f} (alternative), {n7['yt_thermal']:.3f} (thermal)", "y_t = {}".replace("y_t", "yt"))
num("D7 band -> kappa (JSON)", f"[{n7['kappa_at_yt140']:.4f}, {n7['kappa_at_yt60']:.4f}]", "κ ∈ {}")
num("D7 Saturn 5.5e-4 (JSON)", sci(n7["K7"]["planets_yt140"]["Saturn"]["ratio"], 1), "signal is {} of its bound")
check("D7 best planet Saturn (JSON)", n7["K7"]["best_planet"] == "Saturn")
num("D7 wide binaries 0.57% (JSON)", f"{100 * n7['K7']['wb_max_frac_dg']:.2f}%", "at most {}")
k10 = d7["checks"][9]["value"]
check("D7 K10 non-monotone (JSON)", "peak y=12.24, u_max=0.8988a0, same u at g=0.8162a0 and 72.9a0" in k10
      and "y = 12.24 with u = 0.899 a0" in flat and "g = 0.816 a0 and 72.9 a0" in flat)
k11 = d7["checks"][10]["value"]
check("D7 K11 0/48, 66.46 off +44% alt (JSON)", "0/48" in k11 and "R*^(1/5)=66.46" in k11 and "alt +44.4%" in k11 and "None of 48 frozen" in flat and "66.46, is off by 44%" in flat)
num("D7 thermal y_t 77.876 vs 77.85/77.944 (JSON)", f"{n7['yt_thermal']:.3f}", "the thermal yt is {}, not 77.85 or 77.944")
check("D7 K5 record values (JSON)", "77.85 and 77.944" in d7["checks"][4]["threshold"])
rd("D7 9.14x stand-in bound", "D7_turnoff_yt", "README.md", "planets pass 9.14×", "planets pass 9.14x")

# ---------------------------------------------------------------- F. D7b Cassini (unscreened)
V = d7b["verdicts"]
YT = ("60", "66.3803", "77.876", "140")
for foot, lab in (("canonical", "canonical"), ("alt", "alternative")):
    lo = min(V[f"{foot}|{y}"]["min_over_Hees"] for y in YT); hi = max(V[f"{foot}|{y}"]["max_over_Hees"] for y in YT)
    num(f"D7b {foot} x Hees 2sigma over the band (JSON)", f"{lo:.2f}-{hi:.2f}x({lab})", "{}")
    check(f"D7b {foot} FAIL Hees and Park everywhere (JSON)", all(V[k]["Hees"] == "FAIL" and V[k]["Park"] == "FAIL" for k in V if k.startswith(foot + "|")))
num("D7b Hees 2 sigma line (JSON)", sci(d7b["inputs"]["bound_Hees_2sigma"], 1), "({} s-2)")
check("D7b headline 1.7-4x", "fails Cassini by 1.7-4x" in flat)
eff = [e for k in V if not k.endswith("|none") for e in V[k]["turnoff_effect"]]
num("D7b turn-off effect range (JSON)", f"+{100 * min(eff):.2f}% to +{100 * max(eff):.2f}%", "changes Q2 by {}")
check("D7b turn-off raises Q2 (JSON)", min(eff) > 0)
num("D7b max band spread (JSON)", sci(d7b["band"]["max_spread"], 1), "at most {} s-2")
num("D7b 0.052 sigma (JSON)", f"{d7b['band']['max_spread_over_sigma_Hees']:.3f}σ", "{} of Hees")
num("D7b abstract 0.052 sigma (JSON)", f"{d7b['band']['max_spread_over_sigma_Hees']:.3f}σ", "moves Q2 by {}")
e0 = V["canonical|60"]["Q2"][0] / d7b["inputs"]["bound_Hees_2sigma"]
num("D7b E0 most favourable 1.70x (JSON)", f"{min(V[f'canonical|{y}']['Q2'][0] for y in YT) / 9e-27:.2f}xcanonical", "still fails ({})")
check("D7b K1 analytic limit <= 5e-10 (JSON)", max(v["rel"] for v in d7b["K1_analytic_unit_tail"].values()) <= 5e-10 and "reproduced to 5x10-10" in flat)
rd("D7b K3 routes agree 1.1e-3", "D7b_cassini_Q2", "d7b_cassini_q2.out", "K3 PASS max|G/M-1|=1.09e-03", "agree to 1.1x10-3")
num("D7b K5 QUMOND/AQUAL (JSON)", f3(d7b["K5_BN11"]["ratio"]), "our QUMOND value is {} of Blanchet")
k4 = d7b["K4_Desmond_anchors"]
num("D7b K4 anchor ratios (JSON)", f"{k4['1.0']['ratio']:.3f}, {k4['1.5']['ratio']:.3f} and {k4['2.0']['ratio']:.3f}", "|q| is {} of them")
check("D7b 7/8, exit 1 disclosed (JSON)", d7b["checks_pass"] == 7 and d7b["checks_total"] == 8 and "K4 fails as frozen" in flat and "exits 1 (7/8)" in flat)
check("D7b exact limit q = -(16/49) sqrt(e_N) (README)", "q = −(16/49)√e_N" in open(os.path.join(DP, "D7b_cassini_Q2", "README.md"), encoding="utf-8").read() and "q = -(16/49)" in flat)
check("D7b scoped to the unscreened law (A26 law-first)", "unscreened canonical law fails Cassini" in flat and "A26 \"law-first\" reading" in flat.replace("“", '"').replace("”", '"'))


# ---------------------------------------------------------------- F2. D7c unscreened law family vs Q2 and SPARC (result 26b5db080f)
c7 = J("D7c_q2_rar_gate", "d7c_q2_rar_gate_results.json")
check("D7c scope unscreened (JSON)", c7["scope"].startswith("UNSCREENED") and "unscreened law forms only; the screened case is D7d" in flat)
check("D7c no law passes both (JSON)", c7["outcome"].startswith("NO LAW PASSES BOTH") and not any(v["both"] for v in c7["joint"].values()))
fam = c7["families"]
wk = min(min(f["SPARC_passers_worst_cell_Hees_sigma"].values()) for f in fam.values() if f["SPARC_passers_worst_cell_Hees_sigma"])
num("D7c weakest tension (JSON)", f"{wk:.2f}σ", "family is {} (Hees)")
NL = ("L", "Q", "M", "S", "R")
lo = min(c7["Q2"][l][f]["min_over_Hees_upper"] for l in NL for f in ("canonical", "alt")); hi = max(c7["Q2"][l][f]["max_over_Hees_upper"] for l in NL for f in ("canonical", "alt"))
num("D7c named laws range (JSON)", f"{lo:.2f}-{hi:.2f}x", "on both footings: {}")
check("D7c named laws all FAIL Hees and Park (JSON)", all(c7["Q2"][l][f][b] == "FAIL" for l in NL for f in ("canonical", "alt") for b in ("Hees", "Park")))
cn = fam["capacity_n"]
check("D7c capacity: SPARC only n=2, Q2 only n=8 (JSON)", cn["SPARC_pass_members"] == ["n=2"] and cn["Q2_pass_members"] == ["n=8"])
num("D7c n=2 Hees sigma (JSON)", f"{cn['its_Hees_sigma']:.2f}-{cn['its_worstcell_Hees_sigma']:.2f}σ", "fails at {}")
num("D7c n=8 SPARC z (JSON)", f"{cn['its_SPARC_z']:.2f}", "at z = {} (canonical)")
check("D7c beta canonical passers >= 2.5, none alt (JSON)", c7["A1_footing_split_passers"]["canonical"][0] == "beta=2.5" and c7["A1_footing_split_passers"]["alt"] == [] and "β ≥ 2.5" in flat)
ext = c7["A1_beta_alt_E0_extension"]
r_ = [v["alt_E0"] / 9e-27 for v in ext.values()]
num("D7c beta alt-E0 floor (JSON)", f"{min(r_):.2f}-{max(r_):.2f}x", "by {}for β")
ef = c7["efield_dependence_L"]
num("D7c g_e crossings (JSON)", f"{sci(ef['canonical']['Hees']['crossings_ge_total'][0], 2)} (canonical) or {sci(ef['alt']['Hees']['crossings_ge_total'][0], 2)}", "ge ≤ {}")
check("D7c 5/6 checks, K4 3.3e-9 (JSON)", c7["checks_pass"] == 5 and c7["checks_total"] == 6 and f"{c7['K4_numono_rel']:.1e}" == "3.3e-09" and "3.3x10-9" in flat)
rd("D7c A1 post-result round-off (README)", "D7c_q2_rar_gate", "README.md", "check-side round-off", "check-side round-off, fixed post-result")

# ---------------------------------------------------------------- G. D8 / D8b
d8 = J("D8_Lstar_value", "d8_lstar_value_results.json")
p1, p2 = d8["part1"], d8["part2"]
num("D8 A76 c_s at 24 pc (JSON)", f"{p1['cs_24pc_m_s']:.6f}", "({} m/s at 24 pc)")
check("D8 c_s identical to A76 (JSON)", p1["cs_rel_vs_A76"] == 0.0)
num("D8 sigma caps (JSON)", f"σc ≤ {p1['foot']['canonical']['sigma_max_frozen_m_s'] / 1e3:.2f} (canonical) or {p1['foot']['alt']['sigma_max_frozen_m_s'] / 1e3:.2f} km/s", "{}")
num("D8 ratios 4.84 / 4.41 (JSON)", f"{p1['foot']['canonical']['sigma_th_over_sigma_max_frozen']:.2f} and {p1['foot']['alt']['sigma_th_over_sigma_max_frozen']:.2f} times", "by {}")
num("D8 fine floor (JSON)", f"{p2['canonical']['L95_fine_pc']:.3f} / {p2['alt']['L95_fine_pc']:.3f} pc", "roots {}")
num("D8 dchi2 (JSON)", f"{p2['canonical']['thermal']['mu1.22']['dchi2']:.3f} (canonical, by {p2['canonical']['thermal']['mu1.22']['dchi2'] - 3.841:.2f}) and {p2['alt']['thermal']['mu1.22']['dchi2']:.3f}", "Δχ2 = {}")
check("D8 thermal EXCLUDED both footings (JSON)", p2["canonical"]["class_thermal"] == p2["alt"]["class_thermal"] == "EXCLUDED at 95%")
tdg = d8["part3"]["primary_tdg"]["foot"]
num("D8 TDG medians and spread (JSON)", f"{tdg['canonical']['median']:.1f} / {tdg['alt']['median']:.1f} pc with an 84/16 spread of {tdg['canonical']['ratio_84_16']:.2f}", "{}")
st = J("D8_Lstar_value", "d8_stilp2013_results.json")
d8b = J("D8b_sigma_universality", "d8b_sigma_universality_results.json")
num("D8 Stilp median sigma (D8b JSON envelope)", f"{d8b['envelope']['sigma_m2']['median']['sigma_kms']:.2f}", "= {} km/s")
num("D8 Stilp L* and 84/16 (JSON)", f"{st['s_m2']['canonical']['median']:.2f} / {st['s_m2']['alt']['median']:.2f} pc, with 84/16 = {st['s_m2']['canonical']['ratio_84_16']:.3f}", "L⋆ = {}")
check("D8 Stilp one_constant True, class CONSISTENT (JSON)", st["s_m2"]["canonical"]["one_constant"] and st["s_m2"]["alt"]["class"] == "CONSISTENT")
num("D8 sigma_central L* (JSON)", f"{st['s_cen']['canonical']['median']:.1f} / {st['s_cen']['alt']['median']:.1f} pc", "gives {}, below the floor")
check("D8 Stilp provenance ApJ 765, 136", "ApJ 765, 136" in txt("D8_Lstar_value", "PROVENANCE.md") and "ApJ 765, 136 (2013)" in flat)
t1 = d8b["T1"]["sigma_m2"]["SSFR"]
check("D8b T1 FLOOR FAVOURED (JSON)", d8b["T1_verdict"] == "FLOOR FAVOURED" and "FLOOR FAVOURED" in flat)
num("D8b rho, p, alpha (JSON)", f"ρ = +{t1['rho']:.3f}, p = {t1['p_perm']:.3f} against α = {t1['alpha']}", "FAVOURED: {}")
num("D8b slope and CI (JSON)", f"+{t1['slope_ols']:.3f}, 95% CI [+{t1['slope_ci95'][0]:.3f}, +{t1['slope_ci95'][1]:.3f}]", "slope {}")
t2 = d8b["T2"]["sigma_cen"]
num("D8b chi2 / dof (JSON)", f"χ2 = {t2['chi2']:.1f} for {t2['dof']}", "{}")
num("D8b intrinsic scatter (JSON)", f"{t2['sigma_int_kms']:.2f} km/s", "intrinsic scatter {}")
num("D8b noise-only 84/16 (JSON)", f"{d8b['T2']['sigma_m2']['mc_ratio_median']:.2f}", "an 84/16 of {} from noise alone")
shi = d8b["T1"]["sigma_m2"]["SHI"]
num("D8b Sigma_HI (JSON)", f"ρ = +{shi['rho']:.3f}, p = {shi['p_perm']:.4f}", "({})")
ev = d8b["envelope"]["sigma_m2"]["min"]
num("D8b floor reading (JSON)", f"{ev['canonical']:.1f} / {ev['alt']:.1f} pc", "gives {}, below the globular bound")
check("D8b below CFG820 floor both footings (JSON)", ev["canonical"] < d8b["cfg820_floor_pc"]["canonical"] and ev["alt"] < d8b["cfg820_floor_pc"]["alt"])

# ---------------------------------------------------------------- H. D9 / D9b
u6 = d9["numbers"]["U6"]
num("D9 Lambda_LV at 1 AU (JSON)", f"{sci(u6['canonical']['Lambda_LV_min_1AU'], 4)} (canonical) and {sci(u6['alt']['Lambda_LV_min_1AU'], 4)} (alternative)", "{}")
num("D9 abstract 6.3e7 (JSON)", sci(u6["canonical"]["Lambda_LV_min_1AU"], 1), "violation of {} at 1 AU")
p3 = d9["numbers"]["P3"]
num("D9 A33 cone excess at 24 pc (JSON)", f"{sci(p3['24pc_canonical'], 2)} / {sci(p3['24pc_alt'], 2)}", "η = γ is {}")
check("D9 V2/V4/V5 bound checks pass (JSON)", all(d9["checks"][k]["pass"] for k in ("V2", "V4", "V5")) and "1.005015" in d9["checks"]["V5"]["value"])
check("D9 MAP.md exists", os.path.exists(os.path.join(DP, "D9_uv_parent", "MAP.md")) and "MAP.md" in flat)
d9b = J("D9b_A33_multiplier", "d9b_a33_multiplier_results.json")
check("D9b s=2, -0.55 a0 (JSON)", d9b["L1"]["Mlit_s"] == 2 and d9b["L1"]["Mlit_dev_over_a0_at_g_a0_over_3"] == -0.55 and "(s = 2)" in flat and "-0.55 a0" in flat)
ftc = d9b["field_theory_count"]["with_lambda"]
num("D9b 4 second-class, 7 DOF (JSON)", f"{ftc['SC']} second-class constraints and {int(ftc['DOF'])} degrees of freedom", "has {}")
num("D9b growth exponent (JSON)", f"{d9b['T3']['n_Mstar']:.5f}", "(growth a{} in EdS)")
num("D9b NG1 alt MW-M31 (JSON)", f"-{abs(d9b['N1']['values']['F1_MW-M31_alt']['rho_c_min_over_rhobar']):.0f}", "ρc down to {} ρ̄")
check("D9b 14/14 checks True (JSON) and first run 11/14", all(d9b["checks"].values()) and len(d9b["checks"]) == 14
      and outline("D9b_A33_multiplier", "d9b_a33_multiplier_firstrun.out") == "11/14" and "(11/14) is kept" in flat)
check("D9b c2 = 1 for M* (JSON)", d9b["T1"]["c2"]["Mstar"] == "1")

# ---------------------------------------------------------------- I. D1 skew
d1 = J("D1_skew_preflight", "d1_skew_preflight_results.json")
t3 = d1["T3_log_transform"]["table"]["0.5"]
num("D1 log skew at a0/2 (JSON)", f"{t3['n1_log']:.2f} for n = 1, {t3['n2_log']:.2f} for n = 2", "{}")
check("D1 log signs never opposite (JSON)", d1["T3_log_transform"]["log_opposite_fraction_of_window"] == 0.0)
num("D1 background linear skew (JSON)", f"+{d1['T3_log_transform']['lognormal_bg_linear_skew_006dex']:.2f}", "{} from a 0.06 dex background")
sp = d1["SPARC"]
num("D1 SPARC lin skew outside window (JSON)", f"{sp['canonical']['lin']['out_window_skew']:.2f} (canonical) / {sp['alt']['lin']['out_window_skew']:.2f} (alternative)", "{}")
bc = sp["canonical"]["best_case"]
num("D1 best-case signals (JSON)", f"+{bc['n1']['s_obs_lin_mean']:.3f} and {bc['n2']['s_obs_lin_mean']:.3f}", "best-case signals of {}")
rat = [sp[f]["lin"]["out_window_skew"] / abs(sp[f]["best_case"][n]["s_obs_lin_mean"]) for f in ("canonical", "alt") for n in ("n1", "n2")]
num("D1 background/signal 17-51 (JSON)", f"{int(min(rat))}-{round(max(rat))}", "{} times smaller")
dl = d1["T2_dilution"]
num("D1 N_s 93.1 (JSON)", f"{dl['N_s_A2']['1']:.1f}", "N_s = {} normalisation".replace("N_s", "Ns"))
num("D1 x93 / x384 (JSON)", f"{dl['cases']['n1_Ns93']['ratio_vs_K30']:.0f} (n = 1) and {dl['cases']['n2_Ns93']['ratio_vs_K30']:.0f} (n = 2)", "by {}")
check("D1 record K30 13,500 (JSON) and 7,000-13,500 (README)", round(d1["record"]["K30_N3sigma"]) == 13500 and "7,000-13,500" in txt("D1_skew_preflight", "README.md") and "(7,000-13,500 points)" in flat)
check("D1 verdict SCOPED NO-GO (JSON)", d1["verdict"]["verdict"] == "SCOPED NO-GO")

# ---------------------------------------------------------------- J. D2 wide binaries
d2 = J("D2_wide_binary_fork", "d2_wide_binary_fork_results.json")
num("D2 A24 case (JSON)", f"{d2['R1']['value']:.4f} for A24's case (A24: {d2['R1']['A24']})", "{}")
num("D2 orientation-averaged (JSON)", f"{d2['R1b']['canonical']:.3f} (canonical) / {d2['R1b']['alt']:.3f} (alternative)", "{}")
r3 = d2["R3"]
num("D2 sigma(kappa) (JSON)", f"{r3['sigma_kappa_corrected']:.3f}", "σ(κ) = {}")
num("D2 joint error (JSON)", f"{r3['joint_now']:.3f} → {r3['joint_after_corrected']:.3f}, not {r3['A71_joint_after']:.4f}", "{}")
num("D2 floor 0.048 (JSON)", f"{r3['sigma_kappa_floor_infiniteN']:.3f}", "floor {} at infinite N")
r4 = d2["R4"]
num("D2 DR3 occupancy (JSON)", f"{r4['n_bin_dr3']} of {r4['n_dr3']:,} pairs ({100 * r4['frac_dr3']:.2f}%)", "{}")
num("D2 A24 7.41% (JSON)", f"{100 * r4['frac_loguniform']:.2f}%", "not A24's {}")
gl = d2["R5"]["global"]
zc = sorted(gl[k]["z_floor"] for k in gl if k.endswith("|canonical")); za = sorted(gl[k]["z_floor"] for k in gl if k.endswith("|alt"))
num("D2 global separation (JSON)", f"{zc[0]:.2f}-{zc[-1]:.2f}σ (canonical) and {za[0]:.2f}-{za[-1]:.2f}σ (alternative)", "{}")
r8 = d2["R8"]
num("D2 sigma_sys ceilings (JSON)", f"{r8['canonical|mock']['sigma_sys_ceiling']:.3f} (canonical) / {r8['alt|mock']['sigma_sys_ceiling']:.3f} (alternative)", "exceeds {}")
num("D2 inter-group spread (JSON)", f"{d2['R6']['inter_group']:.3f}", "spread is {}")
r7 = d2["R7"]
num("D2 satellites +1.25 dex (JSON)", f"{r7['n_below']} sub-threshold satellites sit +{r7['median_Delta_EFE_below']:.2f} dex", "the {}")
num("D2 5 of 45 (JSON)", f"{r7['within_0p5']} of {r7['n_below']}", "({} within 0.5 dex)")
check("D2 current data OPEN (JSON)", d2["R6"]["cls"] == "OPEN")
note = open(os.path.join(ROOT, "prep_2026", "gaia_dr4_prep", "NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md"), encoding="utf-8").read()
check("D2 pre-DR4 note 8658130bd0 (file + commit)", "0.054 (canonical)" in note and "does **not** edit `PREREGISTRATION_DR4.md`" in note
      and "prep_2026/gaia_dr4_prep/NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md" in git("show", "--name-only", "--format=", "8658130bd0").stdout and "8658130bd0" in flat)

# ---------------------------------------------------------------- K. D4 ALMA
d4 = J("D4_alma_status", "d4_alma_status_results.json")
sm = d4["summary"]
num("D4 U4 4.34 sigma (JSON)", f"{sm['U4 framework vs R-H, nu_mono (governing kernel)']['max_z_noisefree']:.2f}σ", "U4 reaches {}")
num("D4 GS4 n=1 vs n=2 (JSON)", f"{sm['GS4 n=1 vs n=2']['max_z_noisefree']:.2f}σ", "(≤ {} on every branch)")
check("D4 GS4 never reaches 3 sigma (JSON)", not any(v["reaches_3sigma"] for k, v in sm.items() if k.startswith("GS4") and "reaches_3sigma" in v))
mp = d4["U4_Mstar_propagated"]["canon 9.36e-11|250"]["z_with_Mstar"]
num("D4 propagated separation 0.00 (JSON)", f"{mp:.2f}", "the separation is {}")
cells = json.dumps(d4["R7_quoted"])
check("D4 R7 S/N endpoints in the quoted cells (JSON) and README", all(s in cells for s in ("S/N 0.18", "S/N 0.58", "S/N 0.04", "S/N 0.15"))
      and "0.18–0.58 for U4 and 0.04–0.15 for GS4" in open(os.path.join(DP, "D4_alma_status", "README.md"), encoding="utf-8").read()
      and "S/N 0.18-0.58 (U4) and 0.04-0.15 (GS4)" in flat)
rd("D4 dates", "D4_alma_status", "README.md", "Public 2026-11-06", "public 2026-11-06"); rd("D4 dates GS4", "D4_alma_status", "README.md", "Public 2026-11-28", "public 2026-11-28")
rd("D4 V_c window", "D4_alma_status", "README.md", "about 240-260 km/s", "Vc ≈ 240-260 km/s")
has("D4 one disc excludes no model", "One disc excludes no model")

# ---------------------------------------------------------------- L. D3 CFG960 (read-only lane; README + ledger)
R3 = "D3_cfg960_status"
rd("D3 step 89 of 150", R3, "README.md", "It reached step 89 of 150 (a = 0.19)", "step 89 of 150, a = 0.19")
rd("D3 killed four times", R3, "README.md", "was killed four times by its own frozen abort rule", "killed four times")
rd("D3 footprint 65.2 GB", R3, "README.md", "51.4 / 63.9 / 59.2 / 65.2 GB", "reached 65.2 GB")
rd("D3 estimate 43-47 GB", R3, "README.md", "a peak of 43-47 GB", "estimate of 43-47 GB")
rd("D3 SC2x never started", R3, "README.md", "SC2x (alt) never started", "SC2x (alternative) never started")
rd("D3 stopped 01:01", R3, "README.md", "the chain stopped at 2026-10-22 01:01 local", "2026-10-22 at 01:01 local")
LED = open(os.path.join(ROOT, "campaign_fresh_gravity", "LEDGER.md"), encoding="utf-8").read().splitlines()
r960 = [l for l in LED if l.startswith("| CFG960")]
check("D3 ledger: no CFG960 outcome row yet ('STARTED' only)", any("chain960.sh STARTED" in l for l in r960) and not any(w in l for l in r960 for w in ("killed", "swap rule", "SC1x VOID"))
      and "the ledger row still reads \"STARTED\"" in flat.replace("“", '"').replace("”", '"'))
check("D3 no CFG960 commit after D3", git("log", "--format=%h", "77d59a9a38..HEAD", "--", "campaign_fresh_gravity/CFG960_sctm_engine").stdout.strip() == "")
has("D3 no verdict", "no verdict")


# ---------------------------------------------------------------- L2. D6 retained fraction (result b21dda1a2d)
d6 = J("D6_u_mechanism", "d6_u_mechanism_results.json")
q1 = d6["Q1"]
check("D6 f_P = 1 -> u_P4 = 0 (JSON)", q1["f_P_cluster"] == 1.0 and q1["u_P4_primary"] == 0.0 and "1 - fP = 0" in flat)
num("D6 13.0 sigma (JSON)", f"{q1['z_primary']:.1f}σ", "which is {} below 0.4716")
num("D6 abstract 13.0 sigma (JSON)", f"{q1['z_primary']:.1f}σ", "({} from the record's cluster model")
num("D6 14.6 sigma identity (JSON)", f"{q1['z_identity']:.1f}σ", "it is {} above")
num("D6 v/sigma 1.64 (JSON)", f"{q1['v_over_sigma_needed_primary']:.2f}", "v/σ = {}")
check("D6 slope -1/6 vs record +1/6 (JSON)", q1["slope_deep_symbolic"] == "-1/6" and abs(q1["slope_record_A21"] - 1 / 6) < 1e-12 and q1["T1s"] == "RECORD ERROR"
      and "dln u/dln Mv = -1/6" in flat.replace("d ln", "dln") and "not the record's +1/6" in flat)
num("D6 numeric slope (JSON)", f"{q1['slope_deep_numeric']:.5f}", "(numerically {})")
M = d6["Q2"]["models"]
num("D6 H-VR u_MID (JSON)", " / ".join(f"{M[f'H-VR|{e}|canonical']['u_MID']:.3f}" for e in ("1.0000", "0.5000", "0.3333")), "uMID = {} on the 318-cluster stack")
num("D6 H-VR within 0.7 sigma (JSON)", f"{max(M[f'H-VR|{e}|canonical']['z_MID'] for e in ('1.0000', '0.5000', '0.3333')):.1f}σ", "within {} of 0.4716")
num("D6 H-VR chi2 (JSON)", " / ".join(f"{M[f'H-VR|{e}|canonical']['chi2']:.1f}" for e in ("1.0000", "0.5000", "0.3333")), "χ2 = {} for 8 degrees of freedom")
num("D6 abstract chi2 39.0 (JSON)", f"{M['H-VR|1.0000|canonical']['chi2']:.1f}", "profile, χ2 = {} for 8 degrees")
check("D6 H-VR and H-1S FAIL both footings (JSON)", all(v == "FAILS" for c in d6["Q2"]["CLASS"].values() for v in c.values()))
num("D6 H-1S range (JSON)", f"{min(M[k]['u_MID'] for k in M if k.startswith('H-1S')):.2f}-{max(M[k]['u_MID'] for k in M if k.startswith('H-1S')):.2f}", "gives uMID = {}")
qa = d6["Q3a"]["measure"]
num("D6 u_gal (JSON)", f"{qa['canonical']['u_gal_min']:.3f} ± {qa['canonical']['sigma']:.3f} (canonical) and {qa['alt']['u_gal_min']:.3f} ± {qa['alt']['sigma']:.3f}", "ugal ≥ {}")
num("D6 u_gal z (JSON)", f"{qa['canonical']['z_vs_0p4716']:.1f}σ / {qa['alt']['z_vs_0p4716']:.1f}σ", "{} above 0.4716")
num("D6 -0.25 dex (JSON)", f"-{abs(qa['canonical']['dlogMb_for_u_0p4716']):.2f}", "a {} dex stellar-mass systematic")
qb = d6["Q3b"]
num("D6 X-COP u (JSON)", f"{qb['frozen']['canonical|b0.0']['u']:.3f} or {qb['frozen']['canonical|b0.3']['u']:.3f}", "give {} depending")
num("D6 X-COP ends 6.1 sigma (JSON)", f"{qb['decircularisation']['canonical']['z_b_ends']:.1f}σ", "differ by {}")
check("D6 X-COP cannot de-circularise (JSON)", not qb["decircularisation"]["canonical"]["ok"] and not qb["decircularisation"]["alt"]["ok"])
num("D6 K3 interior slope (JSON)", f"{d6['Q2']['selfsim']['1.0000']['slope_in']:.3f}", "interior slope is {}")
rd("D6 K4 tolerance loosened (README)", "D6_u_mechanism", "README.md", "K4's tolerance was loosened from 1e-6 to 1e-4 after the run", "K4's tolerance was loosened after the run")
rd("D6 new posit (README)", "D6_u_mechanism", "README.md", "is a new posit. It is not in the action", "(a new posit, not in the action)")


# ---------------------------------------------------------------- W. D7d screened Q2 and wave E (E1-E5)
dd = J("D7d_screened_q2", "d7d_screened_q2_results.json")
R1p = dd["R1_physical"]
check("W D7d passes Hees and Park everywhere (JSON)", all(v["hees"] and v["park"] for v in R1p.values()))
q24 = [R1p[k]["Q2"] for k in R1p if "|24|" in k]; q90 = [R1p[k]["Q2"] for k in R1p if "|90|" in k]
num("W D7d Q2 at 24 pc (JSON)", f"{min(q24) * 1e34:.1f}-{max(q24) * 1e34:.1f}x10-34", "Q2 = {} s-2")
num("W D7d Q2 at 90 pc (JSON)", f"{min(q90) * 1e36:.1f}-{max(q90) * 1e36:.1f}x10-36", "at 90 pc, {}")
oh = [v["over_Hees_upper"] for v in R1p.values()]
num("W D7d fraction of Hees line (JSON)", f"{sci(min(oh), 1)} to {sci(max(oh), 1)}", "That is {} of the Hees line")
num("W D7d abstract 2.5e-8 (JSON)", sci(max(oh), 1), "at most {} of the Hees line")
check("W D7d margin 1e7-1e9 (JSON)", 1e7 <= 1 / max(oh) < 1e8 and 1e9 <= 1 / min(oh) < 1e10 and "passes Cassini by 107-109" in flat)
LC = dd["L_C"]
num("W D7d L*_C upper bounds (JSON)", f"{LC['canonical']['upper_pc']:.3f} pc (canonical) and ≤ {LC['alt']['upper_pc']:.3f} pc", "≤ {}")
num("W D7d abstract threshold (JSON)", f"{LC['canonical']['upper_pc']:.3f} pc (canonical) or {LC['alt']['upper_pc']:.3f} pc", "at most {} (alternative)")
num("W D7d Saturn gate 5.75 pc (JSON)", f"{LC['canonical']['CFG691_Lmin_pc']:.2f} pc", "Saturn monopole ({})")
num("W D7d K4 AQUAL anchor (JSON)", sci(dd["K4_AQUAL_BN11"]["R"], 3), "value ({} against")
check("W D7d 10/10 checks (JSON)", all(v["ok"] for v in dd["checks"].values()) and len(dd["checks"]) == 10)
num("W D7d planet anomaly (JSON)", sci(dd["C2_planets"]["canonical|24|Earth"]["GM_over_L2"], 2), "GM/L2⋆ = {} m s-2")
num("W D7d Mars 0.17 (JSON)", f"{dd['C2_planets']['canonical|24|Mars']['ratio']:.2f}", "(Mars at {} of its bound)")
wb = dd["C1_wide_binary"]["canonical|24"]["gamma_minus_1"]
num("W D7d gamma_v-1 at 24 pc (JSON)", sci(max(wb), 1), "has γv - 1 = {}")
num("W D7d DR4 abstract (JSON)", sci(max(wb), 1), "γv - 1 ≈ {} for a 20 kAU binary")
rd("W D7d 3.0 GB disclosure (README)", "D7d_screened_q2", "README.md", "The main run peaked at **3.0 GB RSS**", "peaked at 3.0 GB")
rd("W D7d hedgehog (README)", "D7d_screened_q2", "README.md", "constant hedgehog GM/L*² r̂", "hedgehog")
e2 = J("E2_field_equation", "e2_field_equation_results.json")
o2 = e2["R1_outcome"]
num("W E2 AQUAL canonical (JSON)", f"{o2['canonical_range'][0]:.2f}-{o2['canonical_range'][1]:.2f}x", "fails by {}")
num("W E2 AQUAL alt (JSON)", f"{o2['alt_range'][0]:.2f}-{o2['alt_range'][1]:.2f}x(alternative)", "and {}")
num("W E2 ratio (JSON)", f"{o2['ratio_range'][0]:.2f}-{o2['ratio_range'][1]:.2f}", "AQUAL/QUMOND is {}")
num("W E2 abstract canonical (JSON)", f"{o2['canonical_range'][0]:.2f}-{o2['canonical_range'][1]:.2f}x", "Cassini Q2 by {}")
check("W E2 D7b FAIL survives (JSON)", o2["outcome"] == "D7b's FAIL SURVIVES")
num("W E2 BN11 1.1% (JSON)", f"{100 * (e2['K3']['ratio_AQUAL'] - 1):.1f}%", "benchmark to {}")
num("W E2 transverse 22% (JSON)", f"{100 * e2['K1c']['transverse_fraction']:.0f}%", "part is {} of the anomalous field")
r2 = e2["R2"]
dl = [abs(r2[k]["delta"]) for k in r2]
num("W E2 gamma_v shift (JSON)", f"{min(dl):.3f}-{max(dl):.3f}", "lowers γv by {}")
num("W E2 gamma_v AQUAL (JSON)", f"{r2['canonical|PREREG_primary']['gamma_AQUAL_anch']:.3f} (canonical) / {r2['alt|PREREG_primary']['gamma_AQUAL_anch']:.3f}", "{} (alternative)")
num("W E2 abstract law-first 1.17 (JSON)", f"{r2['canonical|PREREG_primary']['gamma_AQUAL_anch']:.2f}", "law-first reading γv ≈ {}")
R3e = e2["R3"]; B = ("beta=2.5", "beta=3", "beta=4", "beta=5", "beta=6")
e0 = [R3e[b]["canonical"]["over_Hees"][0] for b in B]
num("W E2 beta canonical E0 (JSON)", f"{min(e0):.2f}-{max(e0):.2f}x", "by {}:")
rr = [R3e[b][f][E]["ratio"] for b in B for f in ("canonical", "alt") for E in ("E0", "E1", "E2", "E3")]
num("W E2 beta AQUAL increase (JSON)", f"{min(rr):.2f}-{max(rr):.2f}", "raises their Q2 by {}")
num("W E2 n=8 alt E3 (JSON)", f"{R3e['n=8']['alt']['over_Hees'][3]:.2f}x", "(alternative E3 cell, {})")
num("W E2 least tense beta=5 (JSON)", f"{e2['R3_outcome']['least_tense'][1]:.2f}x", "worst cell {}")
check("W E2 no-go survives, nobody passes (JSON)", e2["R3_outcome"]["outcome"] == "No-go SURVIVES" and not any(v.get("both") for v in R3e.values() if isinstance(v, dict)))
e1 = J("E1_input_audit", "e1_input_audit_results.json")
s1 = e1["S1"]
num("W E1 native H0 band (JSON)", f"{min(s1['H0_native'].values()):.1f}-{max(s1['H0_native'].values()):.1f} km/s/Mpc", "({}")
num("W E1 canonical shift (JSON)", f"-{abs(s1['shift_vs_canonical_pct'][0]):.1f}% to +{s1['shift_vs_canonical_pct'][1]:.1f}%", "within {} of the canonical")
sb = s1["sigma_below_SH0ES"].values()
num("W E1 sigma below ladder (JSON)", f"{min(sb):.1f}-{max(sb):.1f}σ", "sits {} below the local")
check("W E1 ladder 73.0 +- 1.0 (JSON)", s1["SH0ES_on_disk"] == [73.0, 1.0] and "(73.0 ± 1.0)" in flat)
rd("W E1 43 inputs (README)", "E1_input_audit", "README.md", "43 inputs, each with a class", "43 inputs, each classed")
S5 = e1["S5_D7b_D7c"]
qq = [S5[n]["laws"][b]["max_over_Hees"] for n in ("nat_lo", "nat_c", "nat_hi") for b in S5[n]["passers_primary"]]
zz = [S5[n]["laws"][b]["SPARC_worst_z"] for n in ("nat_lo", "nat_c", "nat_hi") for b in S5[n]["passers_primary"]]
num("W E1 native beta Q2 margins (JSON)", f"{min(qq):.2f}-{max(qq):.2f}", "Q2 of {} of the line")
num("W E1 native beta SPARC z (JSON)", f"{max(zz):.2f} to {min(zz):.2f}", "SPARC z of {}")
num("W E1 within 0.41 of z=-2 (JSON)", f"{max(zz) + 2:.2f}", "within {} of the z = -2 line")
check("W E1 beta>=3 pass at all three native a0, 2.5 at two (JSON)", all({"beta=3", "beta=4", "beta=5", "beta=6"} <= set(S5[n]["passers_primary"]) for n in ("nat_lo", "nat_c", "nat_hi"))
      and sum("beta=2.5" in S5[n]["passers_primary"] for n in ("nat_lo", "nat_c", "nat_hi")) == 2 and all(S5[n]["outcome_native"].startswith("UNDECIDED") for n in ("nat_lo", "nat_c", "nat_hi")))
s1z = [S5[n]["laws"][b]["S1_worst_z"] for n in ("nat_lo", "nat_c", "nat_hi") for b in S5[n]["passers_primary"]]
num("W E1 S1 still against (JSON)", f"{max(s1z):.2f}", "(z ≤ {})")
c8 = e1["S3_S4_CFG820"]
num("W E1 D8 flip native (JSON)", f"{c8['record (nu_RAR+EFE, Ups 1.6)']['native_lo']['dchi2_thermal']:.2f}", "native a0 ({}, allowed)")
num("W E1 D8 flip M/L (JSON)", f"{c8['Ups_V -0.2 dex']['canonical']['dchi2_thermal']:.2f}", "M/L ({})")
num("W E1 D6 u_gal flip (JSON)", f"{e1['S6_D6']['u_gal_sps_full']['-0.2']['canonical']['u']:.3f}, +{e1['S6_D6']['u_gal_sps_full']['-0.2']['canonical']['z_vs_0p4716']:.1f}σ", "ugal = {}")
num("W E1 u at native h (JSON)", f"{e1['S6_D6']['u_MID_variants']['native h (A46_3pt) + native a0']:.3f}", "becomes {}")
rd("W E1 four flips (README)", "E1_input_audit", "README.md", "Most verdicts survive clean substitution. Four do not", "Four do not survive clean substitution")
rd("W E1 alt is a LCDM import (README)", "E1_input_audit", "README.md", "The alt footing is a ΛCDM import", "it is a pure ΛCDM import")
e4 = J("E4_fitted_three", "e4_fitted_three_results.json")
c4 = e4["Lstar"]["CFG820"]
num("W E4 native floor (JSON)", f"{c4['canonical']['N1_native']:.2f} pc (canonical) / {c4['alt']['N1_native']:.2f} pc", "floor is {}")
num("W E4 recipe floor (JSON)", f"{c4['canonical']['N2_native_plus_EFE_recipe']:.2f} / {c4['alt']['N2_native_plus_EFE_recipe']:.2f} pc", "recipe kept, {}")
num("W E4 M/L span (JSON)", f"{c4['canonical']['N1_ups_minus']:.1f}-{c4['canonical']['N1_ups_plus']:.1f} pc", "spans {} (canonical)")
num("W E4 abstract floor (JSON)", f"{c4['canonical']['N1_native']:.2f} pc, {c4['canonical']['N1_ups_minus']:.1f}-{c4['canonical']['N1_ups_plus']:.1f} pc", "native floor {}")
num("W E4 thermal native dchi2 (JSON)", f"{c4['canonical']['dchi2_N1_at_thermal']:.2f} / {c4['alt']['dchi2_N1_at_thermal']:.2f}", "Δχ2 = {}.")
num("W E4 dSph ceiling 22.0 (JSON)", f"{e4['Lstar']['CFG821_native']['canonical']['L95_up']:.1f} pc", "stays {}")
kc = e4["kappa"]["record_and_clean"]["canonical"]["BAO+BBN (CFG886 T2a)"]
num("W E4 clean a0 (JSON)", sci(kc["a0"], 3), "give a0 = {} m s-2")
num("W E4 clean kappa (JSON)", f"{kc['kappa']:.3f} ± {kc['sigma']:.3f} (canonical), a shift of -{abs(kc['shift_sigma']):.2f}σ", "κ = {}")
check("W E4 kappa ROBUST both (JSON)", e4["kappa"]["record_and_clean"]["canonical"]["line"] == e4["kappa"]["record_and_clean"]["alt"]["line"] == "kappa ROBUST")
num("W E4 dlnu/dlna0 (JSON)", f"+{e4['u']['canonical']['dlnu_dlna0']:.2f}", "d ln u/d ln a0 = {}")
pr = e4["post_result_reported_only"]
num("W E4 u at galaxy a0, post-result (JSON)", f"{pr['u_native_at_clean_a0'][0]:.3f} ± {pr['u_native_at_clean_a0'][1]:.3f}", "uMID = {} (post-result, reported only)")
num("W E4 a0-carried error (JSON)", f"{pr['u_sys_canonical']['from_a0_error']:.3f}", "into u ({})")
num("W E4 abstract u 0.433 (JSON)", f"{pr['u_native_at_clean_a0'][0]:.3f}", "({} at the galaxy-measured")
sv = e4["jacobian"]["singular_values"]
num("W E4 Jacobian (JSON)", f"rank {e4['jacobian']['rank']}, singular values {sv[0]:.2f}, {sv[1]:.2f}, {sv[2]:.2f}", "(Jacobian {})")
e3 = J("E3_dwarf_excess", "e3_dwarf_excess_results.json")
A = e3["A"]
num("W E3 clean excess (JSON)", f"+{A['canonical|clean primary (Arroyo free-f)']['median']:.2f} ± {A['canonical|clean primary (Arroyo free-f)']['sd']:.2f}", "{} dex above Newton")
num("W E3 worst clean (JSON)", f"+{A['canonical|WORST-CLEAN W (Ups4,f0.7,lower sigma,UL drop)']['median']:.2f} ± {A['canonical|WORST-CLEAN W (Ups4,f0.7,lower sigma,UL drop)']['sd']:.2f}", "({} in the worst")
sd_ = e3["A_above_screened_diag"]
num("W E3 gap above screened (JSON)", f"+{sd_['canonical|L*24']['median_Delta']:.2f} ± {sd_['canonical|L*24']['sd']:.2f} dex", "sit {} above the screened prediction")
num("W E3 abstract gap (JSON)", f"+{sd_['canonical|L*24']['median_Delta']:.2f} ± {sd_['canonical|L*24']['sd']:.2f} dex", "sit {} above its prediction")
num("W E3 alt gap (JSON)", f"+{sd_['alt|L*24']['median_Delta']:.2f}", "(alternative {})")
num("W E3 90 pc gap (JSON)", f"+{sd_['canonical|L*90']['median_Delta']:.2f} dex", "and {} at")
num("W E3 screened boost (JSON)", f"10{sd_['canonical|L*24']['median_log_B']:.2f}", "median boost of {} over Newton")
Bq = e3["B"]
num("W E3 q census (JSON)", f"q = {Bq['canonical|primary L*24 f_ret0.10']['median_q']:.2f}", "must hold {}")
num("W E3 q census-free (JSON)", f"q = {Bq['canonical|L*24 f_ret1 (census-free)']['median_q']:.1f}, a shortfall of +{Bq['canonical|L*24 f_ret1 (census-free)']['log_median_q']:.2f} dex", "census-free, {}")
check("W E3 UNDECIDABLE both (JSON)", all(v.startswith("UNDECIDABLE") for v in e3["B_class"].values()) and "UNDECIDABLE on both footings" in flat)
check("W E3 A-SURVIVES both (JSON)", e3["A"]["canonical|class"]["cls"] == e3["A"]["alt|class"]["cls"] == "A-SURVIVES")
e5 = J("E5_parent_logic", "e5_parent_logic_results.json")
check("W E5 S3 trough <= 8.869e-4 (JSON)", "8.869e-04" in e5["checks"]["S3"]["value"] and "at most 8.9x10-4" in flat)
num("W E5 L*crit MW-M31 (JSON)", f"{e5['numbers']['fiducials']['F1_MW-M31_canonical_Lcrit_pc'] / 1e3:.1f} kpc", "LCRIT≈ {}".replace("LCRIT≈ ", "L⋆ ≈ "))
check("W E5 frozen E1 fails, E1b passes (JSON)", e5["checks"]["E1"]["ok"] is False and e5["checks"]["E1b"]["ok"] is True and sum(v["ok"] for v in e5["checks"].values()) == 14)
check("W E5 N1 positivity, T1 gamma-independent (JSON)", e5["checks"]["N1"]["ok"] and e5["checks"]["T1"]["ok"] and "L_XX(law)" in e5["checks"]["N1"]["value"])
rd("W E5 open classes (README)", "E5_parent_logic", "README.md", "Open classes: foliated U(1) under criterion B", "Open classes: a foliated U(1)")

# ---------------------------------------------------------------- M. errata and record corrections
er = git("log", "--format=%h %s", "--grep=ERRATA (doors push", "--fixed-strings").stdout.split("\n")
er = [l for l in er if l.strip()]
want = {"f775a7e6c5": "D1", "e1fd7be4dc": "D5", "3c11f5d2e0": "D7", "9e6fbbbfcd": "D8", "c749c5007d": "D2", "05a3bfdb73": "D9"}
check("M exactly six doors-push errata commits", len(er) == 6, f"{len(er)}")
for h, lane in want.items():
    check(f"M erratum {h} ({lane}) exists and is cited", any(l.startswith(h) and f"ERRATA (doors push {lane})" in l for l in er) and h in flat)

# ---------------------------------------------------------------- N. pending lanes (D6, D7c, D7d)
for lane in ("D6_u_mechanism", "D7c_q2_rar_gate", "D7d_screened_q2", "E1_input_audit", "E2_field_equation", "E3_dwarf_excess", "E4_fitted_three", "E5_parent_logic"):
    check(f"N {lane} README committed and folded in", git("ls-files", "--error-unmatch", f"doors_push_2026_10_22/{lane}/README.md").returncode == 0)
check("N no PENDING placeholder left", "% PENDING" not in tex and "): pending" not in flat)
lanes_now = sorted(d for d in os.listdir(DP) if os.path.isdir(os.path.join(DP, d)))
covered = set(LANES) | {"D7d_screened_q2"}
check("N every doors-push lane directory is covered by the paper", set(lanes_now) <= covered, f"uncovered: {sorted(set(lanes_now) - covered)}")
check("N D2 pre-DR4 note AMENDMENT A1 (AQUAL) folded in", "## AMENDMENT A1 (2026-10-22, pre-data, append-only)" in note and "σ_sys < 0.048 (canonical) / < 0.058 (alt)" in note
      and "prep_2026/gaia_dr4_prep/NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md" in git("show", "--name-only", "--format=", "ee621a0898").stdout
      and "ee621a0898" in flat and "below 0.048 (canonical) / 0.058 (alternative)" in flat)
check("N coordinator's screening estimate absent", all(s not in flat for s in ("S ≈ 3", "screening S", "3x10-6 at r", "3x10-6 at rM")))

# ---------------------------------------------------------------- O. citations against the record
CIT = os.path.join(ROOT, "citations")
bib = open(os.path.join(CIT, "REFERENCES.bib"), encoding="utf-8").read()


def bibentry(key):
    m = re.search(r"@\w+\{" + re.escape(key) + r",(.*?)\n\}", bib, re.S)
    return m.group(1) if m else ""


e = bibentry("Desmond2024")
check("O Desmond, Hees & Famaey 2024 (bib)", "{Desmond}, Harry and {Hees}, Aurélien and {Famaey}, Benoit" in e and "530" in e and "1781-1795" in e and "10.1093/mnras/stae955" in e
      and "H. Desmond, A. Hees, B. Famaey, MNRAS 530, 1781 (2024)" in flat)
e = bibentry("Hees2014")
check("O Hees et al. 2014 (bib)", "89" in e and "102002" in e and "A. Hees, W. M. Folkner, R. A. Jacobson, R. S. Park, PRD 89, 102002 (2014)" in flat)
e = bibentry("Park2026")
check("O Park et al. 2026 (bib)", "114" in e and "024066" in e and "R. S. Park et al., PRD 114, 024066 (2026)" in flat)
e = bibentry("Milgrom1999")
check("O Milgrom 1999 (bib)", "253" in e and "astro-ph/9805346" in open(os.path.join(CIT, "works", "milgrom-1999-the-modified-dynamics-as-a-vacuum-effect.md"), encoding="utf-8").read()
      and "Phys. Lett. A 253, 273 (1999) (astro-ph/9805346)" in flat)
e = bibentry("Cookson2026")
check("O Cookson et al. 2026 (bib)", "547" in e and "stag342" in e and "S. A. Cookson et al., MNRAS 547, stag342 (2026)" in flat)
e = bibentry("Lelli2015")
check("O Lelli et al. 2015 (bib)", "584" in e and "A113" in e and "F. Lelli et al., A&A 584, A113 (2015)" in flat)
check("O Blanchet & Novak 2011 (bib)", "1105.5815" in bibentry("Blanchet2011c") and "L. Blanchet, J. Novak, arXiv:1105.5815 (2011)" in flat)
check("O SPARC, Milgrom 1983, QUMOND DOIs in bib", all(d in bib for d in ("10.3847/0004-6256/152/6/157", "10.1086/161130", "10.1111/j.1365-2966.2009.16184.x"))
      and "AJ 152, 157 (2016)" in flat and "ApJ 270, 365 (1983)" in flat and "MNRAS 403, 886 (2010)" in flat)

# ---------------------------------------------------------------- P. zenodo metadata, honesty, forbidden, names
z = json.load(open(ZJ))["metadata"]
ids = {r["identifier"] for r in z["related_identifiers"]}
check("P zenodo related identifiers (PAPER49 v1.2, 55, 56, 57)", {"10.5281/zenodo.23533323", "10.5281/zenodo.23482936", "10.5281/zenodo.23532875", "10.5281/zenodo.23532885"} <= ids)
check("P never the PAPER57 duplicate 23532894", "23532894" not in json.dumps(z) and "23532894" not in tex)
check("P zenodo metadata: working paper, CC-BY, fitted kappa, not closed", z["publication_type"] == "workingpaper" and z["license"] == "cc-by-4.0"
      and "fitted" in z["description"] and "not closed" in z["description"] and "unscreened" in z["description"])
for s in ("PAPER49 v1.2 (doi:10.5281/zenodo.23533323)", "PAPER55 (doi:10.5281/zenodo.23482936)", "PAPER56 (doi:10.5281/zenodo.23532875)", "PAPER57 (doi:10.5281/zenodo.23532885)"):
    has(f"P companion '{s[:24]}'", s)
for s in ("fitted", "the theory is not closed", "not peer reviewed", "never pooled", "post-result", "AI-assisted", "Anthropic's Claude", "not a particle",
          "a postulate", "No covariant parent is established", "The owner's programme", "The screened theory is the one version that passes both Cassini and the galactic law"):
    has(f"P honesty '{s}'", s)
zl = z["description"].lower()
for bad in ("theory closed", "theory is closed", "data favour the framework", "data favor the framework", "proves the framework", "breakthrough",
            "framework fails cassini", "the framework fails", "kappa is derived", "κ is derived", "/users/", "gmail", "dark matter particle", "dark-matter particle"):
    check(f"P forbidden '{bad}' absent", bad not in low and bad not in tex.lower() and bad not in zl)
check("P no home path in TeX", "/Users/" not in tex and "~/" not in tex)
gu = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True, cwd=HERE).stdout.split()
body = low.split("abstract", 1)[-1]
check("P no personal name (repo user) in PDF body, TeX body or zenodo description", all(w.lower() not in body and w.lower() not in tex.lower() and w.lower() not in zl
                                                                                    for w in gu if len(w) >= 3), f"{len(gu)} name parts checked")

print(f"\nPAPER58 audit: {N - F}/{N} PASS" + ("" if F == 0 else f", {F} FAIL"))
sys.exit(1 if F else 0)
