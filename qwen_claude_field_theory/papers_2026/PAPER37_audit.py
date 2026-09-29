#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PAPER37 audit: every number the note quotes is re-read from a COMMITTED file (git HEAD) and checked twice.

For each audited value the script checks that
  (1) the value appears verbatim in its committed source (a regex with one capture group, run over the file as committed at HEAD), and
  (2) the value is actually printed in the .tex block that carries its `% AUDIT: Bnn` tag (the block = the lines since the previous tag).
A few structural counts (gate rows per group, class tallies) are recomputed from GATES.md and labelled as recounts.
Exit 0 only if every row matches.  Reports "N of N".
A source key whose path starts with "@" is a COMMIT MESSAGE read with `git show -s --format=%B <hash>` (the commit is an ancestor of HEAD);
it is used only where a statement is recorded in a commit message and in no committed file (marked "commit message" in the .tex).

Usage:   python3 PAPER37_audit.py            # main run
         python3 PAPER37_audit.py --mutate   # alters ONE expected value (7.97 / 7.52 -> 7.97 / 7.53); must exit 1
         python3 PAPER37_audit.py --mutate-tex  # alters ONE tex literal; must exit 1
Environment: PAPER37_REPO (repo root; default = two levels above this file if it holds campaign_fresh_gravity, else the path below).
"""
import os, re, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
_default = "/Users/carlzimmerman/new_physics/zimmerman-formula"
_up = os.path.abspath(os.path.join(HERE, "..", ".."))
REPO = os.environ.get("PAPER37_REPO") or (_up if os.path.isdir(os.path.join(_up, "campaign_fresh_gravity")) else _default)
TEX = os.path.join(HERE, "PAPER37_complete_action_obstruction_map_2026.tex")
CFG = "campaign_fresh_gravity/"
SRC = {
    "GATES": CFG + "closure_map/GATES.md",
    "ACT": CFG + "closure_map/ACTIONS_AND_NOGOS.md",
    "LEANC": CFG + "closure_map/LEAN_CATALOGUE.md",
    "STAND": CFG + "STANDING_2026-09-28.md",
    "LED": CFG + "LEDGER.md",
    "R42": CFG + "CFG42_README.md",
    "R43": CFG + "CFG43_fluid_tie/README.md",
    "R44": CFG + "CFG44_fluid_target/README.md",
    "R45": CFG + "CFG45_README.md",
    "R46": CFG + "CFG46_README.md",
    "R50": CFG + "CFG50_tidal_closure/README.md",
    "R51": CFG + "CFG51_README.md",
    "R52": CFG + "CFG52_a0z_feasibility/README.md",
    "R56": CFG + "CFG56_README.md",
    "R48": CFG + "CFG48_gap1_switch/README.md",
    "REF48": CFG + "CFG48_REFEREE.md",
    "R49": CFG + "CFG49_gate_scalar/README.md",
    "REF49": CFG + "CFG49_REFEREE.md",
    "R66": CFG + "CFG66_README.md",
    "R54": CFG + "CFG54_README.md",
    "R55": CFG + "CFG55_README.md",
    "R58": CFG + "CFG58_README.md",
    "R59": CFG + "CFG59_README.md",
    "R60": CFG + "CFG60_dispersion_provenance/CFG60_dispersion_provenance.md",
    "R61": CFG + "CFG61_FROZEN_CRITERIA.md",
    "R63": CFG + "CFG63_discrimination_forecast/README.md",
    "R64": CFG + "CFG64_kernel_robustness/README.md",
    "R65": CFG + "CFG65_README.md",
    "GST": CFG + "closure_map/GATES_STATUS_2026-09-29.md",
    "EQL": CFG + "closure_map/EQUATION_LEDGER_2026-09-28.md",
    "CM0dba": "@0dba13349",
    "CM54b0": "@54b026af4",
    "CH": "fable_independent_2026/lean_2026/ChainCert/README.md",
    "VER": "fable_independent_2026/lean_2026/ChainCert/verify_chain.out",
    "O42": CFG + "CFG42_satellites_rule.out",
    "O44B4": CFG + "CFG44_fluid_target/B4_actions_reciprocity.out",
    "O50D2": CFG + "CFG50_tidal_closure/D2_wellposed_nogo_MUTATE_0.out",
    "O51": CFG + "CFG51_walker_ufd.out",
    "O52P": CFG + "CFG52_a0z_feasibility/pooled.out",
}
_cache = {}


def source(key):
    """The file as committed at HEAD (never the working tree)."""
    if key not in _cache:
        p = SRC[key]
        cmd = ["git", "-C", REPO, "show", "-s", "--format=%B", p[1:]] if p.startswith("@") else ["git", "-C", REPO, "show", "HEAD:" + p]
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode != 0:
            raise SystemExit(f"cannot read {p} at HEAD (not committed?): {r.stderr.decode()[:200]}")
        _cache[key] = r.stdout.decode("utf-8")
    return _cache[key]


def nm(s):
    return s.replace("−", "-")


# ---------------------------------------------------------------- recounts from GATES.md (agent-derived, re-run here)
def gate_rows():
    return [l for l in source("GATES").splitlines() if re.match(r"\| (\d\.\d\d) \|", l)]


def cnt_group(g):
    return str(sum(1 for r in gate_rows() if r.split("|")[1].strip()[0] == str(g)))


def cls_of(r):
    m = re.match(r"(MI|SOFT|CONT|n\.c\.|—)", r.split("|")[-2].strip())
    return m.group(1) if m else "?"


def cnt_class(c):
    return str(sum(1 for r in gate_rows() if cls_of(r) == c))


def cnt_noclass_outside5():
    return str(sum(1 for r in gate_rows() if cls_of(r) == "—" and r.split("|")[1].strip()[0] != "5"))


COUNTS = {
    "g1": lambda: cnt_group(1), "g2": lambda: cnt_group(2), "g3": lambda: cnt_group(3), "g4": lambda: cnt_group(4), "g5": lambda: cnt_group(5),
    "total": lambda: str(len(gate_rows())),
    "MI": lambda: cnt_class("MI"), "SOFT": lambda: cnt_class("SOFT"), "CONT": lambda: cnt_class("CONT"), "NC": lambda: cnt_class("n.c."),
    "NONE": lambda: cnt_class("—"), "NONE_not5": cnt_noclass_outside5,
}

# ---------------------------------------------------------------- the audit table
# R(value, file, regex-with-ONE-capture-group [, tex-literal]) ; C(countname, tex-literal)
# The tex literal defaults to the value with the en dash -> '--' and ' / ' -> '/'.  Both sides are normalised (see norm_tex).
ROWS = []  # (block, value, file, regex, tex, kind)


def R(b, value, f, rx, tex=None):
    ROWS.append((b, value, f, rx, tex, "re"))


def C(b, name, tex):
    ROWS.append((b, None, name, None, tex, "count"))


# B01 abstract
C("B01", "total", "63 gates")
R("B01", "42 of 48", "STAND", r"(42 of 48) harness gates \*\*by recount\*\*")
R("B01", "11", "R43", r"at most about \*\*(11)× in mass", r"11\times")
R("B01", "10⁴", "R43", r"against the (10⁴) the BTFR needs", r"10^4")
R("B01", "+0.325", "STAND", r"move from (\+0\.325) dex \(3\.8σ\)")
R("B01", "-0.06", "STAND", r"to (−0\.06) dex \(−0\.4σ\)")
R("B01", "-2.67", "R42", r"−0\.107 \((−2\.67)σ\)")
R("B01", "117", "CH", r"all (117) theorems", "117 theorems")
R("B01", "2 December 2026", "STAND", r"released (2 December 2026)")
# B02 provenance
R("B02", "9.3603", "GATES", r"canonical a0 = (9\.3603)e-11")
R("B02", "1.1312", "GATES", r"alt a0 = (1\.1312)e-10")
# B03-B08 group counts
C("B03", "g1", "& 24 &"); C("B04", "g2", "& 5 &"); C("B05", "g3", "& 13 &"); C("B06", "g4", "& 8 &"); C("B07", "g5", "& 13 &")
C("B08", "total", "total & 63")
# B09 class tallies
R("B09", "33", "GATES", r"CFG1 has (33) results: 14 MI", "33 results")
R("B09", "14", "GATES", r"33 results: (14) MI", "14 were MI")
R("B09", "11", "GATES", r"14 MI, (11) SOFT", "11 SOFT")
R("B09", "8", "GATES", r"11 SOFT, (8) CONT", "8 CONT")
C("B09", "MI", "MI on 14"); C("B09", "SOFT", "SOFT on 10"); C("B09", "CONT", "CONT on 9"); C("B09", "NC", "on 13, and no class")
C("B09", "NONE", "no class on 17"); C("B09", "g5", "the 13 theory rows"); C("B09", "NONE_not5", "and 4 others")
# B10 harness
R("B10", "52", "GATES", r"(52) rows = 48 scored", "52 rows")
R("B10", "48", "GATES", r"52 rows = (48) scored", "48 are scored")
R("B10", "4", "GATES", r"48 scored \+ (4) \"BUDGET strict", "and 4 are")
R("B10", "0.110", "GATES", r"SPARC rms <= (0\.110) dex", "\\le0.110")
R("B10", "+9", "GATES", r"KiDS d chi\^2 <= (\+9);", "+9")
R("B10", "0.265", "GATES", r"Omega_ph <= Omega_c = (0\.265)")
R("B10", "20%", "GATES", r"X-COP identity within (20%)", r"20\%")
R("B10", "2x", "GATES", r"Bullet > (2x) aperture baryons", r"2\times")
R("B10", "2", "GATES", r"CMB-lensing \|pull\| <= (2) sigma", r"2\sigma")
R("B10", "0.10", "GATES", r"forest deviation <= (0\.10);", r"0.10")
R("B10", "2.0", "GATES", r"every population gate <= (2\.0) sigma", r"2.0\sigma")
R("B10", "2", "GATES", r"fitted (2) \(kappa", "fitted 2")
R("B10", "5", "GATES", r"declared (5) \(nu shape", "declared 5")
R("B10", "1", "GATES", r"tied (1), derived 1", "tied 1")
R("B10", "1", "GATES", r"tied 1, derived (1) \(Solar", "derived 1")
R("B10", "6", "GATES", r"The (6) failing scored rows are 3 distinct", "The 6 failing")
R("B10", "3", "GATES", r"6 failing scored rows are (3) distinct gates x 2 footings", "are 3 distinct")
# B11 count
R("B11", "42 of 48", "STAND", r"(42 of 48) harness gates \*\*by recount\*\*")
R("B11", "1.4–1.7", "STAND", r"\((1\.4–1\.7)×\)")
# B12 1.09
R("B12", "7.97 / 7.52", "GATES", r"FAIL (7\.97 / 7\.52) sigma in the harness")
R("B12", "3.8 / 3.5", "GATES", r"refereed (3\.8 / 3\.5) sigma")
R("B12", "+0.325 / +0.304", "GATES", r"\((\+0\.325 / \+0\.304) dex")
R("B12", "0.077", "GATES", r"\+ (0\.077)-dex floor", "0.077-dex")
# B13 1.15
R("B13", "4.08 / 4.29", "GATES", r"FAIL (4\.08 / 4\.29) sigma \(Chae")
R("B13", "1.7", "GATES", r"P2 (1\.7) \(can\) / 2\.7 \(alt\)", "1.7 (P2, can)")
R("B13", "2.7", "GATES", r"P2 1\.7 \(can\) / (2\.7) \(alt\)", "2.7 (P2, alt)")
R("B13", "2.2", "GATES", r"nu_mono (2\.2) / 3\.0 sigma", "2.2 (")
R("B13", "3.0", "GATES", r"nu_mono 2\.2 / (3\.0) sigma", "3.0 (")
# B14 3.06
R("B14", "0.229 / 0.230", "GATES", r"(0\.229 / 0\.230) \(can\)")
R("B14", "0.264 / 0.266", "GATES", r"(0\.264 / 0\.266) \(alt\) vs 0\.159")
R("B14", "0.159", "GATES", r"\(alt\) vs (0\.159)")
# B15 2.03
R("B15", "1.41 / 1.33", "GATES", r"R500 MARGINAL (1\.41 / 1\.33) \(1\.80 / 1\.49 sigma\)")
R("B15", "1.80 / 1.49", "GATES", r"\((1\.80 / 1\.49) sigma\)")
R("B15", "1.88", "GATES", r"R2500 FAIL (1\.88) \(2\.57")
R("B15", "2.57 / 2.63", "GATES", r"\((2\.57 / 2\.63) sigma\)")
R("B15", "-0.958", "GATES", r"rho = (-0\.958)")
# B16 2.04
R("B16", "3.0-4.8", "GATES", r"\((3\.0-4\.8) sigma high\)", "3.0--4.8")
R("B16", "24.5-72.5", "GATES", r"T = (24\.5-72\.5) vs framework", "24.5--72.5")
R("B16", "26-28", "GATES", r"vs framework (26-28)", "26--28")
# B17 3.07
R("B17", "29.4 / 32.9", "GATES", r"association ownership (29\.4 / 32\.9) \(can")
R("B17", "45.4 / 49.3", "GATES", r"(45\.4 / 49\.3) \(alt")
R("B17", "50.2", "GATES", r"spread S = (50\.2)")
# B18 1.17
R("B18", "1.511 / 1.443", "GATES", r"A = (1\.511 / 1\.443) \(12\.9")
R("B18", "1.116 / 1.047", "GATES", r"B timing orbits: (1\.116 / 1\.047) PASS")
R("B18", "-4.2 / -4.1", "GATES", r"profile (-4\.2 / -4\.1) sigma FAIL")
# B19 1.18
R("B19", "1.70 / 1.58", "GATES", r"= (1\.70 / 1\.58) sigma \(H1 failed\)")
R("B19", "1.91 / 1.79", "GATES", r"\(x(1\.91 / 1\.79)\)")
# B20 1.19
R("B20", "1.5-1.7", "GATES", r"= (1\.5-1\.7) sigma with floor", "1.5--1.7")
R("B20", "6.9-7.8", "GATES", r"; (6\.9-7\.8) sigma statistical", "6.9--7.8")
R("B20", "0.10", "GATES", r"incl\. (0\.10)-dex floor", "0.10-dex")
# B21 1.22
R("B21", "+0.139", "GATES", r"UGC 2487 (\+0\.139) dex")
# B22 marginal passes
R("B22", "1.63/1.24", "GATES", r"LVD (1\.63/1\.24)")
R("B22", "1.44/1.21", "GATES", r"Collins (1\.44/1\.21)")
R("B22", "1.71", "GATES", r"PASS (1\.71) / 1\.71")
R("B22", "1.30", "GATES", r"PASS 0\.11 / (1\.30) \(both")
R("B22", "1.33 / 1.11", "GATES", r"PASS (1\.33 / 1\.11) sigma")
R("B22", "2.30 / 2.08", "GATES", r"Stars only (2\.30 / 2\.08);")
# B23 5.01-5.02
R("B23", "1526-3741", "GATES", r"c_gate (1526-3741) km/s", "1526--3741")
R("B23", "0.25", "GATES", r"3741 km/s at z = (0\.25)", "z=0.25")
R("B23", "37 / 117", "GATES", r"vs gas (37 / 117);")
# B24 CFG40
R("B24", "23", "STAND", r"Ogle\+2019's (23) super spirals", "23 super spirals")
R("B24", "+0.11", "STAND", r"sit (\+0\.11) dex fast")
R("B24", "1.4", "STAND", r"dex fast \((1\.4)σ\)", "1.4\\sigma")
R("B24", "+0.17", "STAND", r"nine fastest at (\+0\.17) dex")
R("B24", "2.06", "STAND", r"\((2\.06)σ\)", "2.06\\sigma")
R("B24", "+0.164", "R56", r"\*\*(\+0\.164) \(2\.34σ\)\*\*", "+0.164")
R("B24", "2.34", "R56", r"\*\*\+0\.164 \((2\.34)σ\)\*\*", "2.34\\sigma")
# B25 T1-T6
R("B25", "0.31, 0.48", "ACT", r"x_e in \[(0\.31, 0\.48)\] r_ta", "0.31,0.48")
R("B25", "0.4", "GATES", r"x_e = (0\.4),", "declared 0.4")
R("B25", "0.12", "ACT", r"Omega_c h\^2 = (0\.12) FITTED", "0.12")
# B26 what exists
R("B26", "24/24", "ACT", r"pole on (24/24) layers")
# B27 Gap 1
R("B27", "1500-3700", "ACT", r"c_gate (1500-3700) vs gas", "1500--3700")
R("B27", "37-117", "ACT", r"vs gas (37-117) km/s", "37--117")
R("B27", "500", "ACT", r"needs >= (500) kpc", "500 kpc")
R("B27", "100", "ACT", r"flagship holds to (100) kpc", "100 kpc")
# B28 Gap 2 target
R("B28", "53.4", "R44", r"a₀/4πG = (53\.4) M☉/pc²")
R("B28", "106.9", "R44", r"CFG2's (106\.9) ceiling")
R("B28", "+0.43", "R44", r"overshoots by (\+0\.43) dex at x = 3")
R("B28", "+0.68", "R44", r"and (\+0\.68) dex at x = 1")
R("B28", "24", "R44", r"PointMass`, (24) theorems", "24 theorems")
R("B28", "3/2", "R44", r"β = −\((3/2)\) ρ_b", r"\tfrac32")
# B29 exclusion table
R("B29", "40", "LED", r"(40) checks, all four MUTATE controls fail", "40 checks")
R("B29", "12", "LED", r"(12) checks, both controls fail", "12 checks")
R("B29", "3 × 10⁻⁴", "R44", r"GR correction ≤ (3 × 10⁻⁴)", r"3\times10^{-4}")
R("B29", "(2x⁴+4x²+1)/(4x⁴+4x²+1)", "R44", r"e = (\(2x⁴\+4x²\+1\)/\(4x⁴\+4x²\+1\))", "(2x^4+4x^2+1)/(4x^4+4x^2+1)")
R("B29", "10³", "R44", r"is ≥ (10³);", "10^3")
R("B29", "+65%", "R44", r"\((\+65%) for a 10 M_b shell", r"+65\%")
R("B29", "40", "R44", r"shell at (40) kpc", "40 kpc")
R("B29", "0.3–1.4", "R44", r"off by (0\.3–1\.4) dex", "0.3--1.4")
R("B29", "3.4", "R44", r"M_λ/M_c up to (3\.4)")
R("B29", "0.11–1.5", "R44", r"reaction on the baryons (0\.11–1\.5) g_law", "0.11--1.5")
R("B29", "1.2-4.2", "O44B4", r"\(inward, (1\.2-4\.2) g_law\)", "1.2--4.2")
R("B29", "1.3", "R50", r"7\.3 and (1\.3) \(M_b", "1.3, 0.54, 0.03")
R("B29", "0.54", "R50", r"3\.1 and (0\.54) \(10", "1.3, 0.54, 0.03")
R("B29", "0.03", "R50", r"0\.23 and (0\.03) \(10", "1.3, 0.54, 0.03")
R("B29", "0.505", "R50", r"\*\*(0\.505) g_tot\*\*")
R("B29", "0.505", "O50D2", r"boundary strength = (0\.505)")
R("B29", "64", "R50", r"differs by ×(64) across", "factor 64")
R("B29", "50 to 3400", "R50", r"but (50 to 3400) at z = 1100", "50--3400")
R("B29", "1100", "R50", r"3400 at z = (1100)", "z=1100")
# B30 survivors
R("B30", "3–15", "R44", r"differ (3–15)×", "3--15")
# B31 tie action
R("B31", "9.3603", "R43", r"= (9\.3603) × 10⁻¹¹ m/s²")
# B32 derived
R("B32", "11", "R43", r"A1_action_field_equations_dof\.py` \((11) checks\)", "11, 5 and 11")
R("B32", "5", "R43", r"A2_frw_flat_a0_and_dust_limit\.py` \((5)\)", "11, 5 and 11")
R("B32", "11", "R43", r"A3_cap_entry_form_and_obstruction\.py` \((11)\)", "11, 5 and 11")
R("B32", "six", "R43", r"all (six) controls fail", "all six controls")
R("B32", "6 × 10⁻¹¹", "R43", r"flat to (6 × 10⁻¹¹) for z", r"6\times10^{-11}")
R("B32", "106.9 / 129.2", "R43", r"\((106\.9 / 129\.2) M☉/pc²\)")
# B33 obstruction
R("B33", "6 × 10⁻³", "R43", r"c_s² = (6 × 10⁻³)", r"6\times10^{-3}")
R("B33", "5–14%", "R43", r"growth is (5–14%) of", r"5--14\%")
R("B33", "2 × 10⁴ to 1 × 10⁷", "R43", r"≥ (2 × 10⁴ to 1 × 10⁷) at k", r"2\times10^4 to 1\times10^7")
R("B33", "0.5–30", "R43", r"at k = (0\.5–30) /Mpc", "0.5--30")
R("B33", "1.08", "R43", r"g₀ = (1\.08) and 1\.04")
R("B33", "1.04", "R43", r"g₀ = 1\.08 and (1\.04)\.")
R("B33", "10⁹ and 3 × 10¹¹", "R43", r"at (10⁹ and 3 × 10¹¹) M", r"10^9 and 3\times10^{11}")
R("B33", "0.08–3.3", "R43", r"ranges over (0\.08–3\.3)", "0.08--3.3")
R("B33", "11", "R43", r"at most about \*\*(11)× in mass", r"11\times")
R("B33", "10⁴", "R43", r"against the (10⁴) the BTFR needs", "10^4")
# B34 referee
R("B34", "2.2e4, 1.8e5, 2.0e6, 1.0e7", "R43", r"ν_min\(k\) = (2\.2e4, 1\.8e5, 2\.0e6, 1\.0e7) at k", r"2.2\times10^4, 1.8\times10^5, 2.0\times10^6, 1.0\times10^7")
R("B34", "0.5, 2, 10, 30", "R43", r"1\.0e7 at k = (0\.5, 2, 10, 30) /Mpc", "0.5, 2, 10, 30")
R("B34", "5–12%", "R43", r"differ by (5–12%), from", r"5--12\%")
R("B34", "1.49–1.50", "R43", r"exponent (1\.49–1\.50)", "1.49--1.50")
R("B34", "0.36 / 0.355", "R43", r"g₀ = (0\.36 / 0\.355) at")
R("B34", "1.06 / 1.04", "R43", r"; (1\.06 / 1\.04) at 20%\)")
R("B34", "50%", "R43", r"suppression beyond (50%) is disallowed", r"50\%")
R("B34", "10⁴–10⁵", "R43", r"reaches (10⁴–10⁵), but", "10^4--10^5")
R("B34", "0.01", "R43", r"F ≥ (0\.01) contradicts", "0.01")
# B35 rule
R("B35", "0.4", "STAND", r"\((0\.4)σ, against the law's 3\.3σ", "0.4\\sigma")
R("B35", "3.3", "STAND", r"against the law's (3\.3)σ deficit", "3.3\\sigma")
R("B35", "11.2", "STAND", r"below log M_\* (11\.2) on the law", "11.2")
# B36-B39 CFG42 table (README and primary .out)
R("B36", "+0.325", "R42", r"\| (\+0\.325) \(3\.77σ\)")
R("B36", "3.77", "R42", r"\+0\.325 \((3\.77)σ\)")
R("B36", "-0.059", "R42", r"\*\*(−0\.059) ± 0\.143")
R("B36", "-0.41", "R42", r"\((−0\.41)σ\)\*\* both")
R("B36", "-0.059", "O42", r"canonical rule: KM median (-0\.059) \(resolved-only")
R("B37", "+0.027", "R42", r"MW classical dSphs \| (\+0\.027) /")
R("B37", "-0.118", "R42", r"\*\*(−0\.118) \(−1\.78σ\)\*\*")
R("B37", "-1.78", "R42", r"\*\*−0\.118 \((−1\.78)σ\)\*\*")
R("B37", "-0.118", "O42", r"MW classical dSph  canonical rule: median (-0\.118) \+- 0\.067")
R("B38", "+0.064", "R42", r"M31 Collins\+13 \| (\+0\.064) /")
R("B38", "-0.024", "R42", r"\| (−0\.024) \(−0\.22σ\)")
R("B38", "-0.22", "R42", r"\| −0\.024 \((−0\.22)σ\)")
R("B39", "+0.044", "R42", r"M31 LVD \| (\+0\.044) /")
R("B39", "-0.107", "R42", r"\*\*(−0\.107) \(−2\.67σ\)\*\*")
R("B39", "-2.67", "R42", r"\*\*−0\.107 \((−2\.67)σ\)\*\*")
R("B39", "-0.107", "O42", r"M31 LVD            canonical rule: median (-0\.107) \+- 0\.040")
# B40 CFG42 text
R("B40", "0.133", "R42", r"is (0\.133) dex")
R("B40", "3 × 10⁸", "R42", r"crosses zero near \*\*(3 × 10⁸)\*\*", r"3\times10^8")
R("B40", "10⁹", "R42", r"clamped at M_halo = (10⁹) M", "10^9")
R("B40", "2 × 10⁸ to 10¹²", "R42", r"from (2 × 10⁸ to 10¹²) passes", r"2\times10^8 to 10^{12}")
R("B40", "3 × 10⁷", "R42", r"masses below about (3 × 10⁷) fail", r"3\times10^7")
R("B40", "3.8", "R42", r"falls from (3\.8) to −0\.4", "3.8 to -0.4")
R("B40", "0.086", "R42", r"error grows from (0\.086) to 0\.143", "0.086 to 0.143")
R("B40", "0.143", "R42", r"error grows from 0\.086 to (0\.143)", "0.086 to 0.143")
R("B40", "33", "R42", r"clamp covers (33) of the 40", "33 of the 40")
R("B40", "1.8–2.7", "R42", r"smaller one in σ \((1\.8–2\.7)σ\)", "1.8--2.7")
# B41 CFG45
R("B41", "66", "R45", r"reproduce (66) committed numbers", "66 committed")
R("B41", "6/7", "R45", r"\*\*(6/7)\*\*", "6/7")
R("B41", "4/7", "R45", r"\*\*6/7\*\* \| (4/7) \|", "4/7")
R("B41", "5/7", "R45", r"gates passed \| (5/7) \|", "5/7")
R("B41", "-2.67", "R45", r"\*\*(−2\.67) \\\| −2\.66\*\*", "-2.67")
R("B41", "36%", "R45", r"moves (36%) of the massive", r"36\%")
R("B41", "0.03", "R45", r"by more than (0\.03) dex", "0.03")
R("B41", "-2.12", "R45", r"\*\*(−2\.12) \\\| −2\.13\*\*", "-2.12")
R("B41", "3.8", "STAND", r"ultra-faints move from \+0\.325 dex \((3\.8)σ\)", "3.8\\sigma")
R("B41", "3.3", "STAND", r"against the law's (3\.3)σ deficit", "3.3\\sigma")
# B42 CFG46
R("B42", "Eight of their twelve", "LED", r"(Eight of their twelve) are scorable")
R("B42", "+0.295", "R46", r"\| (\+0\.295) ± 0\.163 \| \+1\.81")
R("B42", "0.163", "R46", r"\+0\.295 ± (0\.163) \|")
R("B42", "1.81", "R46", r"± 0\.163 \| \+(1\.81)")
R("B42", "+0.206", "R46", r"\| \*\*(\+0\.206) ± 0\.164\*\* \| \+1\.26")
R("B42", "0.164", "R46", r"\*\*\+0\.206 ± (0\.164)\*\* \|")
R("B42", "1.26", "R46", r"0\.164\*\* \| \+(1\.26)")
R("B42", "+0.171", "R46", r"\| \*\*(\+0\.171) ± 0\.172\*\* \| \+0\.99")
R("B42", "0.172", "R46", r"\*\*\+0\.171 ± (0\.172)\*\* \|")
R("B42", "0.99", "R46", r"0\.172\*\* \| \+(0\.99)")
R("B42", "-0.068", "R46", r"\*\*(−0\.068) dex\*\*")
R("B42", "-0.104", "R46", r"\*\*(−0\.104) dex\*\*")
R("B42", "Seven of the eight", "R46", r"\*\*(Seven of the eight) offsets stay positive\*\*", "seven of the eight")
R("B42", "-0.151", "R46", r"\| (−0\.151) ± 0\.129")
R("B42", "-1.17", "R46", r"± 0\.129 \| (−1\.17) \(passes\)")
R("B42", "40", "R46", r"than the (40) \(31 resolved", "against 40")
# B43 CFG51
R("B43", "49,367", "LED", r"\((49,367) rows, 38 systems\)")
R("B43", "38", "LED", r"49,367 rows, (38) systems", "38 systems")
R("B43", "+0.219", "R51", r"\*\*(\+0\.219) ± 0\.089 \(2\.46σ\)\*\*")
R("B43", "0.089", "R51", r"\+0\.219 ± (0\.089) \(")
R("B43", "2.46", "R51", r"± 0\.089 \((2\.46)σ\)\*\*", "2.46")
R("B43", "+0.465", "R51", r"\*\*(\+0\.465) ± 0\.128 \(3\.63σ\)\*\*")
R("B43", "0.128", "R51", r"\+0\.465 ± (0\.128) \(")
R("B43", "3.63", "R51", r"± 0\.128 \((3\.63)σ\)\*\*")
R("B43", "+0.465", "O51", r"cleaned (\+0\.465) \+- 0\.128 \(\+3\.63 sigma\)")
R("B43", "+0.310", "R51", r"\| (\+0\.310) \| \*\*\+0\.219")
R("B43", "+0.730", "R51", r"\| (\+0\.730) \| \*\*\+0\.465")
R("B43", "-0.205", "R51", r"\| (−0\.205) \|")
R("B43", "-0.165", "R51", r"\| (−0\.165) \|")
R("B43", "2.4", "R51", r"alone \((2\.4) km/s\) would put", "2.4 km")
R("B43", "+0.007", "R51", r"Boötes I at (\+0\.007) dex", "+0.007")
R("B43", "7.48", "R51", r"\((7\.48) against 3\.8\)", "7.48")
R("B43", "3.8", "R51", r"\(7\.48 against (3\.8)\)", "literature value of 3.8")
# B44 Lean intro
R("B44", "117", "CH", r"all (117) theorems", "117 theorems")
R("B44", "117", "VER", r"theorems checked: (117);", "117 theorems")
# B45 Lean table
R("B45", "3.76, 3.761", "CH", r"E\(2\.5\) ∈ \((3\.76, 3\.761)\)", "3.76,3.761")
R("B45", "0.3138", "CH", r"Ω_m = (0\.3138)", "0.3138")
R("B45", "24", "R44", r"PointMass`, (24) theorems", "24 theorems")
# B46 corpus stats
R("B46", "137", "LEANC", r"\b(137) files, 116 compile", "137 files")
R("B46", "116", "LEANC", r"137 files, (116) compile", "116 compile")
R("B46", "21", "LEANC", r"116 compile, (21) fail", "21 fail")
R("B46", "9", "LEANC", r"21 fail, (9) real sorry", "9 real")
R("B46", "4", "LEANC", r"9 real sorry in (4) non-certificate", "4 non-certificate")
# B47-B49 DR4
R("B47", "2 December 2026", "STAND", r"released (2 December 2026)")
R("B47", "13, 14 and 15", "STAND", r"Amendments (13, 14 and 15) filed", "13, 14 and 15")
R("B47", "1.16–1.18", "STAND", r"\| (1\.16–1\.18) canonical", "1.16--1.18")
R("B47", "1.19–1.23", "STAND", r"\((1\.19–1\.23) alt\)", "1.19--1.23")
R("B48", "1.000", "STAND", r"\| (1\.000) exactly \|")
R("B48", "1.084", "STAND", r"γ̂ ≥ (1\.084)", "1.084")
R("B49", "1.0725 / 1.0900", "STAND", r"ceiling (1\.0725 / 1\.0900)")
R("B49", "1.157 / 1.174", "STAND", r"γ̂ ≥ (1\.157 / 1\.174)")
# B50 a0(z) and CFG52
R("B50", "+0.334", "GATES", r"ΛCDM-native (\+0\.334) dex")
R("B50", "0.13", "STAND", r"At (0\.13) dex per object", "0.13")
R("B50", "2.57", "STAND", r"is (2\.57)σ from ΛCDM-native", "2.57")
R("B50", "1.5–2.4", "STAND", r"\((1\.5–2\.4)σ if an evolving", "1.5--2.4")
R("B50", "−0.10 to +0.14", "STAND", r"by (−0\.10 to \+0\.14) dex", "-0.10 to +0.14")
R("B50", "0.10", "GATES", r"3 rotators at ±(0\.10) dex", r"3 rotators at \pm0.10")
R("B50", "0.20", "GATES", r"or 4 at ±(0\.20)", r"4 at \pm0.20")
R("B50", "242", "R52", r"Of (242) galaxies", "242 galaxies")
R("B50", "16", "R52", r"only (16) have a prediction gap", "16 have")
R("B50", "14", "R52", r"\(N = (14)\)", "N = 14")
R("B50", "+0.135", "R52", r"⟨Δ_flat⟩ = (\+0\.135)", "+0.135")
R("B50", "-0.037", "R52", r"⟨Δ_rival⟩ = (−0\.037)", "-0.037")
R("B50", "+1.0", "R52", r"is (\+1\.0)σ and", "+1.0")
R("B50", "-0.3", "R52", r"\+1\.0σ and (−0\.3)σ", "-0.3")
R("B50", "2–4", "LED", r"needs (2–4) JWST IFU", "2--4 JWST")
R("B50", "0.1", "LED", r"calibration ≲ (0\.1) dex", "0.1")
R("B50", "2.3", "R52", r"caps the significance near (2\.3)σ", "2.3")
R("B50", "0.2", "R52", r"correlated (0\.2)-dex mass calibration", "0.2-dex")
R("B50", "1.4", "STAND", r"rising a₀ to z ≈ (1\.4)", "1.4")
R("B50", "1.2", "R52", r"MUSE-DARK II at z ≈ (1\.2)", "1.2")

# B51 limitations
R("B51", "42 of 48", "STAND", r"(42 of 48) harness gates \*\*by recount\*\*")
R("B51", "11", "R43", r"at most about \*\*(11)\u00d7 in mass", r"11\times")
R("B51", "a real cosmological constant (a de Sitter horizon)", "STAND", r"assumes \u039b is (a real cosmological constant \(a de Sitter horizon\))", "a real cosmological constant (a de Sitter horizon)")
# B52 never-claim list (copied verbatim from the standing page)
R("B52", "That dark matter is gone. The mass is required.", "STAND", r"- (That dark matter is gone\. The mass is required\.)")
R("B52", "That \u03ba = \u00bd is derived.", "STAND", r"- (That \u03ba = \u00bd is derived\.)", r"That \kappa=\tfrac12 is derived.")
R("B52", "That any data set favours the framework over \u039bCDM.", "STAND", r"- (That any data set favours the framework over \u039bCDM\.)", r"That any data set favours the framework over \LambdaCDM.")
R("B52", "That the theory is closed or complete.", "STAND", r"- (That the theory is closed or complete\.)")
R("B52", "Any Standard Model or theory-of-everything result. That sector is walled, and those claims were publicly retracted.", "STAND", r"- (Any Standard Model or theory-of-everything result\. That sector is walled, and those claims were publicly retracted\.)")
R("B52", "That the Local Group or the budget tension excludes the framework (CFG23, CFG27).", "STAND", r"- (That the Local Group or the budget tension excludes the framework \(CFG23, CFG27\)\.)")

# extra coverage rows
C("B09", "total", "the 63 rows")
R("B10", "0.4", "GATES", r"x_e = (0\.4),", "x_e=0.4")
R("B29", "10\u2078\u201310\u00b9\u2074", "R44", r"M_b = (10\u2078\u201310\u00b9\u2074)", "10^8--10^{14}")
R("B34", "20%", "R43", r"1\.06 / 1\.04 at (20%)\)", r"at 20\%")
R("B34", "5%", "R43", r"\((5%) criterion;", r"5\% criterion")
R("B42", "0.7", "R46", r"\*\*f = (0\.7) \(H2\)\*\*", "f=0.7")
R("B50", "0.3", "R52", r"g_bar < (0\.3) a\u2080", r"<0.3 a_0")

# ======================= rows added in version 1 (lanes CFG48-CFG65, ChainCert Profile, status refresh) =======================
# B01 abstract additions
R("B01", "44 of 48", "R48", r"the local gate fails (44 of 48)", "44 of 48")
R("B01", "48/48", "R48", r"\*\*PASS\*\* second variation \((48/48), both readings\)", "48 of 48")
R("B01", "two new untied constants", "R49", r"needs \*\*(two new untied constants)\*\*", "two new untied constants")
R("B01", "54", "R60", r"TOTAL=(54)", "54 committed constructions")
R("B01", "D=0 P=11 I=5 X=27 U=11", "R60", r"TALLY: (D=0 P=11 I=5 X=27 U=11) TOTAL", "D=0, P=11, I=5, X=27, U=11")
R("B01", "2.6", "R55", r"rule, JAM-calibrated masses \| \+0\.046 ± 0\.018 \((2\.6)σ\) \|", r"2.6\sigma")
R("B01", "all ten", "R59", r"YES only if (all ten) intervals", "ten populations")
R("B01", "empty", "R54", r"PHIBSS sample: (empty),", "PHIBSS sample is empty")
R("B01", "Gap 1 and Gap 2 collapse into one object", "R48", r"(Gap 1 and Gap 2 collapse into one object)", "Gap 1 and Gap 2 reduce to one non-derivable object")
# B53 CFG56 bulge fractions
R("B53", "0.04–0.46", "R56", r"\(r band, (0\.04–0\.46), median 0\.26\)", "0.04--0.46")
R("B53", "0.26", "R56", r"median (0\.26)\)", "median 0.26")
R("B53", "+0.105", "R56", r"\*\*(\+0\.105) ± 0\.063 \(1\.67σ\)\*\*", r"+0.105")
R("B53", "0.063", "R56", r"\*\*\+0\.105 ± (0\.063) \(1\.67σ\)\*\*", r"\pm0.063")
R("B53", "1.67", "R56", r"\*\*\+0\.105 ± 0\.063 \((1\.67)σ\)\*\*", r"1.67\sigma")
R("B53", "1.80", "R56", r"\*\*\+0\.166 ± 0\.092 \((1\.80)σ\)\*\*", r"1.80\sigma")
R("B53", "+0.164", "R56", r"\*\*(\+0\.164) \(2\.34σ\)\*\*", r"+0.164")
R("B53", "2.34", "R56", r"\*\*\+0\.164 \((2\.34)σ\)\*\*", r"2.34\sigma")
R("B53", "0.041 to 0.001", "R56", r"shrinks from (0\.041 to 0\.001) dex", "0.041 to 0.001")
R("B53", "23", "R56", r"f_ex = 0 in all (23)", "in all 23")
R("B53", "+0.132", "R64", r"\| CFG56 \| H2 \| FAIL → FAIL \| \+0\.105 \(1\.67σ\) → (\+0\.132) \(2\.06σ\) \|", "+0.132")
R("B53", "2.06", "R64", r"\| CFG56 \| H2 \| FAIL → FAIL \| \+0\.105 \(1\.67σ\) → \+0\.132 \((2\.06)σ\) \|", r"2.06\sigma")
R("B53", "CFG56 H1", "R64", r"exactly one is kernel-sensitive: (CFG56 H1)\*\*", "H1 itself flips to fail")
# B54 status refresh
R("B54", "Candidate B's gate record has not improved since the freeze. It has sharpened.", "GST", r"\*\*(Candidate B's gate record has not improved since the freeze\. It has sharpened\.)\*\*", "Candidate B's gate record has not improved since the freeze. It has sharpened.")
R("B54", "The one clean pass of B's derived rule (SLUGGS) did not survive dynamical stellar masses.", "GST", r"\*\*(The one clean pass of B's derived rule \(SLUGGS\) did not survive dynamical stellar masses\.)\*\*", "The one clean pass of B's derived rule (SLUGGS) did not survive dynamical stellar masses")
R("B54", "It closes the ultra-faint failure but breaks the classical satellites and the LV field dwarfs.", "GST", r"(It closes the ultra-faint failure but breaks the classical satellites and the LV field dwarfs\.)", "the rule closes the ultra-faint failure but breaks the classical satellites and the Local Volume field dwarfs")
R("B54", "The frozen list, its thresholds and its row ids are not moved.", "GST", r"- (The frozen list, its thresholds and its row ids are not moved\.)", "without moving the list, its thresholds or its ids")
# B68 gap map
R("B68", "Gap 3 partly filled", "GST", r"\*\*(Gap 3 partly filled):\*\*", "partly filled")
R("B68", "reduces to Gap 1's enclosed-mass object", "GST", r"\*\*Gap 2 is a scoped no-go\*\* that (reduces to Gap 1's enclosed-mass object)", "reduces to Gap 1's enclosed-mass object")
R("B68", "Neither owns the hierarchy", "R49", r"(Neither owns the hierarchy)\.", "neither owns the hierarchy")
R("B68", "two untied constants", "R49", r"only by adding (two untied constants) and paying", "two untied constants")
# B55 CFG48 four obstructions
R("B55", "six", "CM0dba", r"Gap 1 attacked in (six) scripts", "six scripts")
R("B55", "GA-GG", "R48", r"\(gates (GA-GG) in `GATES_FROZEN\.md`\)", "GA--GG")
R("B55", "12", "REF48", r"All (12) outputs are identical", "all 12 outputs")
R("B55", "7/7", "REF48", r"— (7/7) reproduced", "7/7")
R("B55", "15-33", "R48", r"\((15-33) M_b\)", "15--33")
R("B55", "3.2e11", "R48", r"= (3\.2e11), 2\.2e12, 1\.4e13 Msun for M_b", r"3.2\times10^{11}")
R("B55", "2.2e12", "R48", r"= 3\.2e11, (2\.2e12), 1\.4e13 Msun for M_b", r"2.2\times10^{12}")
R("B55", "1.4e13", "R48", r"= 3\.2e11, 2\.2e12, (1\.4e13) Msun for M_b", r"1.4\times10^{13}")
R("B55", "Helmholtz", "R48", r"is not the Euler-Lagrange system of any Lagrangian in those fields \((Helmholtz) test fails", "fails the Helmholtz test")
R("B55", "0.06", "R48", r"outward with (0\.06) g_law at x = r/r_M = 0\.3", "0.06")
R("B55", "0.4-0.5", "R48", r"at x = r/r_M = 0\.3, (0\.4-0\.5) at x = 1", "0.4--0.5")
R("B55", "11-22", "R48", r"at x = 1 and (11-22) at x = 30", "11--22")
R("B55", "0.10", "R48", r"\(pass line (0\.10) at every x", "pass line 0.10")
R("B55", "23-50", "R48", r"must supply (23-50) times the baryons' orbital kinetic energy", "23--50")
R("B55", "factor 2", "R48", r"it jumps by a (factor 2) at every merger", "factor 2 at every merger")
R("B55", "a prescribed label", "R48", r"The only causal carrier is (a prescribed label)", "a prescribed label")
# B56 stability result
R("B56", "44 of 48", "R48", r"the local gate fails (44 of 48)", "44 of 48")
R("B56", "48/48", "R48", r"\*\*PASS\*\* second variation \((48/48), both readings\)", "48 of 48")
R("B56", "13.7", "R48", r"would need B multiplied by >= (13\.7)", "13.7")
R("B56", "29/48", "R48", r"negative modes on (29/48): 12/12 at z = 0\.25", "29 of 48")
R("B56", "0.15-3.1", "R48", r"a potential step of (0\.15-3\.1) v_f\^2", "0.15--3.1")
R("B56", "1.7-3.6", "R48", r"phantom-inclusive enclosed mass, (1\.7-3\.6)x larger", "1.7--3.6")
R("B56", "0.11-0.24", "R48", r"sits at (0\.11-0\.24) of CFG4's r_ta", "0.11--0.24")
R("B56", "0.31, 0.48", "R48", r"below B's window \[(0\.31, 0\.48)\]", "0.31,0.48")
R("B56", "stronger", "REF48", r"they get \*(stronger)\* under the committed convention", "stronger under the committed convention")
R("B56", "0/48 and 0/48", "R48", r"were FALSE: (0/48 and 0/48)", "0 of 48 and 0 of 48")
R("B56", "24", "R48", r"on DE12's (24) layers x w in", "24 layers")
# B57 CFG49
R("B57", "1.5 × 10²⁸ to 3.9 × 10²⁸", "R49", r"μ ≥ (1\.5 × 10²⁸ to 3\.9 × 10²⁸) J/m", r"1.5\times10^{28} to 3.9\times10^{28}")
R("B57", "10⁻¹²", "R49", r"m₂ ≥ (10⁻¹²) Pa \(tracking", r"m_2\ge10^{-12}")
R("B57", "−13.5", "R49", r"Φ_χ\(r_F\) = (−13\.5) v_f²", "-13.5")
R("B57", "−44", "R49", r"force (−44) g_MOND", "-44")
R("B57", "−31.8", "R49", r"against DE13's (−31\.8)", "-31.8")
R("B57", "7.7 × 10⁷", "R49", r"Φ_χ\(Sun\) = (7\.7 × 10⁷) v_f²", r"7.7\times10^{7}")
R("B57", "2.3 c", "R49", r"UV speed (2\.3 c)", "2.3c")
R("B57", "10⁻¹⁶", "R49", r"only at m₂ ≲ (10⁻¹⁶),", r"m_2\lesssim10^{-16}")
R("B57", "16 of 24", "R49", r"where (16 of 24) edges are off by more than 10%", "16 of 24")
R("B57", "10%", "R49", r"edges are off by more than (10%)", r"10\%")
R("B57", "0.09", "R49", r"the force is still (0\.09) g_MOND", "0.09")
R("B57", "no μ₀ stabilises all 24", "R49", r"(no μ₀ stabilises all 24)", r"no \mu_0 stabilises all 24")
R("B57", "12/12", "R49", r"\*\*Main runs: A (12/12), C 5/6", "A 12/12")
R("B57", "5/6", "R49", r"C (5/6) \(0 load-bearing failures\)", "C 5/6")
R("B57", "7/8", "R49", r"B (7/8), and its one failure is H2", "B 7/8")
R("B57", "Written by a delegated agent and re-run here in place", "R49", r"(Written by a delegated agent and re-run here in place)", "written by a delegated agent and re-run in place")
# B58 relation to CFG48
R("B58", "Neither owns the hierarchy", "R49", r"(Neither owns the hierarchy)\.", "Neither owns the hierarchy")
R("B58", "scoped no-go for this construction class", "R49", r"It is a (scoped no-go for this construction class)", "scoped no-go for this construction class")
R("B58", "and it says nothing about the nonlocal gates", "R49", r"(and it says nothing about the nonlocal gates) of CFG48", "and it says nothing about the nonlocal gates")
# B59 reduction + CFG60
R("B59", "Gap 1 and Gap 2 collapse into one object", "R48", r"(Gap 1 and Gap 2 collapse into one object)", "Gap 1 and Gap 2 collapse into one object")
R("B59", "the fluid's state is initial data from collapse", "R48", r"of the form \"(the fluid's state is initial data from collapse)\"", "the fluid's state is initial data from collapse")
R("B59", "54", "R60", r"TOTAL=(54)", "54 committed constructions")
R("B59", "D=0 P=11 I=5 X=27 U=11", "R60", r"TALLY: (D=0 P=11 I=5 X=27 U=11) TOTAL", "D=0, P=11, I=5, X=27, U=11")
R("B59", "U=5", "R60", r"picture is D=0, P=11, I=5, X=27, (U=5)", "U=5")
R("B59", "6", "R60", r"Table B (6); the tally counts both", "Table B (6 rows)")
R("B59", "No committed construction is class D.", "R60", r"\*\*(No committed construction is class D\.)", "no committed construction is class D")
R("B59", "scoped NO", "R60", r"The answer is a (scoped NO)", "scoped NO")
R("B59", "122 of 122", "R60", r"expects: (122 of 122) matched", "122 of 122")
# B60 CFG55
R("B60", "16", "R55", r"\*\*Sample:\*\* (16) of CFG38's 19", "16 of CFG38's 19")
R("B60", "+0.097", "R55", r"\*\*(\+0\.097) ± 0\.024 \(4\.0σ\)\*\*", r"+0.097")
R("B60", "0.024", "R55", r"\*\*\+0\.097 ± (0\.024) \(4\.0σ\)\*\*", r"\pm0.024")
R("B60", "4.0", "R55", r"\*\*\+0\.097 ± 0\.024 \((4\.0)σ\)\*\*", r"4.0\sigma")
R("B60", "3.65", "R55", r"\*\*\+0\.088 ± 0\.024 \((3\.65)σ\)\*\*", r"3.65\sigma")
R("B60", "+0.046", "R55", r"rule, JAM-calibrated masses \| (\+0\.046) ± 0\.018 \(2\.6σ\) \|", r"+0.046")
R("B60", "0.018", "R55", r"rule, JAM-calibrated masses \| \+0\.046 ± (0\.018) \(2\.6σ\) \|", r"\pm0.018")
R("B60", "2.6", "R55", r"rule, JAM-calibrated masses \| \+0\.046 ± 0\.018 \((2\.6)σ\) \|", r"2.6\sigma")
R("B60", "+0.007", "R55", r"rule, SLUGGS masses \(same 16\) \| (\+0\.007) \(0\.4σ\)", r"+0.007")
R("B60", "0.4", "R55", r"rule, SLUGGS masses \(same 16\) \| \+0\.007 \((0\.4)σ\)", r"0.4\sigma")
R("B60", "−0.10", "R55", r"\(median (−0\.10) dex against SLUGGS's\)", "-0.10")
R("B60", "Three of the four worst offenders", "R55", r"(Three of the four worst offenders) are X-ray-bright", "three of the four worst offenders")
R("B60", "the rule no longer fits cleanly anywhere among massive passive systems", "R55", r"\*\*(the rule no longer fits cleanly anywhere among massive passive systems)\.\*\*", "the rule no longer fits cleanly anywhere among massive passive systems")
R("B60", "H2 failed", "R55", r"\*\*(H2 failed)\.\*\*", "Both declared hypotheses failed")
R("B60", "C3 failed as declared, and is kept", "R55", r"\*\*(C3 failed as declared, and is kept)\.\*\*", "Control C3 failed as declared")
R("B60", "The IMF objection runs the wrong way.", "R55", r"(The IMF objection runs the wrong way\.)", "the IMF objection runs the wrong way")
# B61 CFG58
R("B61", "2.3 × 10⁷", "R58", r"above M_b ≈ (2\.3 × 10⁷) M☉ \(canonical", r"2.3\times10^7")
R("B61", "1.5 × 10⁷", "R58", r"; (1\.5 × 10⁷) alt\)", r"1.5\times10^7")
R("B61", "13", "R58", r"\*\*LV field dwarfs \(n = (13)\)\*\*", "the 13 LV field dwarfs")
R("B61", "−0.60", "R58", r"\| (−0\.60) \\\| −0\.85 \|", "-0.60")
R("B61", "−3.47", "R58", r"\*\*(−3\.47) \\\| −2\.70\*\*", "-3.47")
R("B61", "−0.85", "R58", r"\| −0\.60 \\\| (−0\.85) \|", "-0.85")
R("B61", "−2.70", "R58", r"\*\*−3\.47 \\\| (−2\.70)\*\*", "-2.70")
R("B61", "0.061", "R58", r"\(change (0\.061) dex;", "0.061")
R("B61", "−1.4", "R58", r"only (−1\.4) \\\| −1\.3σ\)", "-1.4")
R("B61", "2–5 × 10⁻⁹", "R58", r"differs by (2–5 × 10⁻⁹) against a 1 × 10⁻⁹ tolerance", r"2--5$\times10^{-9}$")
R("B61", "1 × 10⁻⁹", "R58", r"against a (1 × 10⁻⁹) tolerance", r"$1\times10^{-9}$")
R("B61", "C1 failed, kept", "R58", r"\*\*(C1 failed, kept)\.\*\*", "Control C1 failed and is kept")
R("B61", "S switches itself off when f_ex = 0", "R58", r"\*\*(S switches itself off when f_ex = 0)\*\*", "switches itself off when")
# B62 kernel (CFG64)
R("B62", "√(1+1/y)", "R64", r"P2 \(ν = (√\(1\+1/y\))", r"\nu=\sqrt{1+1/y}")
R("B62", "about 2σ", "R64", r"CFG14 found P2 disfavoured at (about 2σ)", r"about 2$\sigma$")
R("B62", "0.027", "R64", r"The largest move anywhere is (0\.027) dex and 0\.39σ", "0.027")
R("B62", "0.39", "R64", r"The largest move anywhere is 0\.027 dex and (0\.39)σ", r"0.39$\sigma$")
R("B62", "0.012", "R64", r"ultra-faint lanes move by at most (0\.012) dex", "0.012")
R("B62", "−0.058", "R64", r"rule −0\.059 → (−0\.058); law", r"$-0.059\to-0.058$")
R("B62", "3.90", "R64", r"law \+3\.77σ → \+(3\.90)σ", r"3.90$\sigma$")
R("B62", "22", "R64", r"Of the (22) declared hypotheses exactly one", "the 22 declared hypotheses")
R("B62", "CFG56 H1", "R64", r"exactly one is kernel-sensitive: (CFG56 H1)\*\*", "CFG56 H1")
R("B62", "0.027", "R64", r"crossing the 2σ line by a (0\.027)-dex move", "0.027-dex move")
R("B62", "3.3 × 10⁻⁹", "R64", r"agree to (3\.3 × 10⁻⁹) for y", r"$3.3\times10^{-9}$")
R("B62", "2.3%", "R64", r"and to (2\.3%) up to y = 30", r"2.3\%")
R("B62", "six", "R64", r"error in (six) lanes' docstrings", "six lanes")
R("B62", "self-consistent refit", "R64", r"not a (self-consistent refit)", "self-consistent refit")
R("B62", "C3 failed", "R64", r"\*\*(C3 failed), kept as declared", "failed as declared")
R("B62", "C3b", "R64", r"\*\*(C3b) \(added after seeing C3, disclosed\) passes", "C3b")
R("B62", "exponential RAR", "R64", r"use `hunt_lib\.nu_s`, the (exponential RAR) form", "exponential RAR kernel")
# B63 halo shape (CFG65)
R("B63", "−0.059", "R65", r"\| DM \(committed\) \| (−0\.059) \(", r"$-0.059$")
R("B63", "−0.107", "R65", r"\| DM \(committed\) \| [^|]*\| [^|]*\| (−0\.107) \(", r"$-0.107$")
R("B63", "−0.098", "R65", r"\| A1 Duffy 200m \| (−0\.098) \(", r"$-0.098$")
R("B63", "−0.125", "R65", r"\| A1 Duffy 200m \| [^|]*\| [^|]*\| (−0\.125) \(", r"$-0.125$")
R("B63", "+0.049", "R65", r"\| A2 Duffy 200c \| (\+0\.049) \(", r"$+0.049$")
R("B63", "−0.071", "R65", r"\| A2 Duffy 200c \| [^|]*\| [^|]*\| (−0\.071) \(", r"$-0.071$")
R("B63", "−0.007", "R65", r"\| A3 Duffy relaxed 200c \| (−0\.007) \(", r"$-0.007$")
R("B63", "−0.096", "R65", r"\| A3 Duffy relaxed 200c \| [^|]*\| [^|]*\| (−0\.096) \(", r"$-0.096$")
R("B63", "−0.117", "R65", r"\| C Einasto \| (−0\.117) \(", r"$-0.117$")
R("B63", "−0.124", "R65", r"\| C Einasto \| [^|]*\| [^|]*\| (−0\.124) \(", r"$-0.124$")
R("B63", "+0.284", "R65", r"\*\*B Burkert core\*\* \| \*\*(\+0\.284) \(\+3\.91σ\)\*\*", r"$+0.284$")
R("B63", "3.91", "R65", r"\*\*B Burkert core\*\* \| \*\*\+0\.284 \(\+(3\.91)σ\)\*\*", r"3.91$\sigma$")
R("B63", "−0.006", "R65", r"\*\*(−0\.006) \(−0\.09σ\)\*\*", r"$-0.006$")
R("B63", "−0.09", "R65", r"\*\*−0\.006 \((−0\.09)σ\)\*\*", r"$-0.09\sigma$")
R("B63", "0.75", "R65", r"the ultra-faint offset stays under (0\.75)σ", r"under 0.75$\sigma$")
R("B63", "0.036", "R65", r"moves by at most (0\.036) dex", "0.036")
R("B63", "−1.7", "R65", r"drops to (−1\.7)σ \| −1\.9σ", r"$-1.7\sigma$")
R("B63", "−1.9", "R65", r"drops to −1\.7σ \| (−1\.9)σ", r"$-1.9\sigma$")
R("B63", "0.05", "R65", r"through the (0\.05)-dex clause", "0.05-dex clause")
R("B63", "2.0–2.6", "R65", r"becomes a (2\.0–2\.6)σ under-prediction", "2.0--2.6")
R("B63", "0.55", "R65", r"at least about (0\.55) of the NFW value", "0.55")
R("B63", "0.03–0.3", "R65", r"debris mass at (0\.03–0\.3) kpc", "0.03--0.3")
R("B63", "0.17", "R65", r"Einasto with α = (0\.17)", "0.17")
R("B63", "The debris result is robust to the concentration relation and to an Einasto profile, and it is not robust to a core.", "R65", r"\*\*(The debris result is robust to the concentration relation and to an Einasto profile, and it is not robust to a core\.)", "The debris result is robust to the concentration relation and to an Einasto profile, and it is not robust to a core.")
R("B63", "A cusp", "R65", r"(A cusp) is what closes the ultra-faints and what over-predicts the classical dwarfs; a core removes both", "A cusp closes the ultra-faints and over-predicts the classical dwarfs; a core removes both")
# B64 universal fraction (CFG59)
R("B64", "0.81", "R59", r"SLUGGS \(φ ≥ (0\.81)\)", r"0.81")
R("B64", "0.30", "R59", r"M31 LVD \(φ ≤ (0\.30)\)", r"0.30")
R("B64", "0.51", "R59", r"a gap of (0\.51)\*\* \(alt 0\.46\)", "gap of 0.51")
R("B64", "0.46", "R59", r"a gap of 0\.51\*\* \(alt (0\.46)\)", "alt 0.46")
R("B64", "0.74", "R59", r"MW ultra-faints \| \+3\.77σ \| −0\.41σ \| (0\.74) \|", "0.74")
R("B64", "0.39", "R59", r"MW ultra-faints \| \+3\.77σ \| −0\.41σ \| 0\.74 \| \[(0\.39), 1\]", "from 0.39")
R("B64", "0.39", "R59", r"MW classical dSphs \| \+0\.32σ \| −1\.78σ \| 0\.05 \| \[0, (0\.39)\]", "le0.39")
R("B64", "0.22, 0.30", "R59", r"leaves \[(0\.22, 0\.30)\]", "0.22,0.30")
R("B64", "0.21, 0.22", "R59", r"\(alt \[(0\.21, 0\.22)\]\)", "0.21,0.22")
R("B64", "5 of 5", "R59", r"passes (5 of 5);", "5 of 5")
R("B64", "want about a quarter of the debris and the most massive early types want nearly all of it", "R59", r"(want about a quarter of the debris and the most massive early types want nearly all of it)", "want about a quarter of the debris and the most massive early types want nearly all of it")
R("B64", "stay disjoint for DM, A1, A2, A3 and C", "R65", r"(stay disjoint for DM, A1, A2, A3 and C)", "stay disjoint for DM, A1, A2, A3 and C")
# B45 / B65 Lean additions
R("B45", "no extended profile satisfying both the decay hypothesis and the target was constructed", "CH", r"\*\*(no extended profile satisfying both the decay hypothesis and the target was constructed)", "No extended profile satisfying both the decay hypothesis and the target was constructed")
R("B45", "an isothermal profile witnesses the target without decay, an exponential profile witnesses the decay without a cold fluid", "CH", r"\((an isothermal profile witnesses the target without decay, an exponential profile witnesses the decay without a cold fluid)", "an isothermal profile witnesses the target without decay, an exponential profile witnesses the decay without a cold fluid")
R("B45", "Eddington positivity are numerical", "CH", r"(Eddington positivity are numerical)", "Eddington positivity are numerical")
R("B45", "σ²/(V_c²/2) = 1 + 4πr²Σ_out/M_b", "CH", r"(σ²/\(V_c²/2\) = 1 \+ 4πr²Σ_out/M_b)", r"\sigma^2/(V_c^2/2)=1+4\pi r^2\Sigma_{\rm out}/M_b")
R("B65", "C1_a0_form_iff", "CH", r"\(`(C1_a0_form_iff)`, both directions", r"C1\_a0\_form\_iff")
R("B65", "zero_point_linear_in_kappa", "CH", r"\(`(zero_point_linear_in_kappa)`; it does not mention the limit\)", r"zero\_point\_linear\_in\_kappa")
R("B65", "cap_a0_tie", "CH", r"`(cap_a0_tie)` is an identity; it is not linked to the kernel", r"cap\_a0\_tie")
R("B65", "no_single_polytrope", "CH", r"\(`(no_single_polytrope)` is stated for Γ\(x\)", r"no\_single\_polytrope")
R("B65", "audit found no unsound theorem, no vacuous hypotheses, standard axioms only", "CM54b0", r"(audit found no unsound theorem, no vacuous hypotheses, standard axioms only)", "The audit found no unsound theorem, no vacuous hypotheses, standard axioms only")
R("B65", "0 mismatches", "EQL", r"reported (0 mismatches) in exit codes and check counts", "0 mismatches")
R("B65", "26", "EQL", r"\((26) runs, main and every MUTATE control\)", "26 runs")
R("B65", "rows 1–11", "EQL", r"re-ran (rows 1–11) from a scratch copy", "rows 1--11")
R("B65", "uncommitted at the time of writing", "EQL", r"(uncommitted at the time of writing)", "uncommitted at the time")
# B66 CFG54
R("B66", "73", "R54", r"; (73) galaxies at z ≈ 1\.2 and 2\.2\)", "73 galaxies")
R("B66", "51", "R54", r"\((51) remain\)", "51 remain")
R("B66", "N = 0 of 51", "R54", r"\*\*(N = 0 of 51)\.\*\*", "N=0 of 51")
R("B66", "1.10", "R54", r"at r_v = 1\.31 r_h is (1\.10) \(then", "is 1.10")
R("B66", "4.7", "R54", r"the median is (4\.7) and the maximum", "median 4.7")
R("B66", "1.31", "R54", r"at r_v = (1\.31) r_h is 1\.10", "1.31")
R("B66", "5", "R54", r"\(N ≥ (5), else the lane", r"N\ge5")
R("B66", "0", "R54", r"at 1\.31 r_h \*\*(0)\*\*;", "0 at $1.31")
R("B66", "7", "R54", r"at 2 r_h \*\*(7)\*\*", "7 at $2")
R("B66", "20", "R54", r"at 3 r_h \*\*(20)\*\*", "20 at $3")
R("B66", "31", "R54", r"at 4 r_h \*\*(31)\*\*", "31 at $4")
R("B66", "non-diagnostic", "R54", r"The lane is (non-diagnostic)\.", "non-diagnostic")
R("B66", "MUTATE control is vacuous", "R54", r"\*\*The (MUTATE control is vacuous) here\.\*\*", "MUTATE control is vacuous")
# B67 CFG63 (+CFG61)
R("B67", "65", "R63", r"\((65) citations, C0\)", "65 citations")
R("B67", "4,342", "R63", r"\*\*(4,342) pairs\*\* \(alt 2,940\)", "4,342 pairs")
R("B67", "2,940", "R63", r"\*\*4,342 pairs\*\* \(alt (2,940)\)", "alt 2,940")
R("B67", "30,000", "R63", r"\| (30,000) expected; pipeline built", "30,000 expected")
R("B67", "2.5", "R63", r"\| \*\*(2\.5)\*\* \| \*\*about 5 systems\*\*", "dwarfs 2.5")
R("B67", "2.3", "R63", r"\| \*\*(2\.3)\*\* \| 1 object", "2.3 against")
R("B67", "1.3", "R63", r"\| \*\*(1\.3)\*\* \(1\.7 if", "1.3 against")
R("B67", "1.8", "R63", r"\| (1\.8) \| never \| never \| 20 groups", "R_{500}$ 1.8")
R("B67", "11 of 11", "R63", r"\((11 of 11) checks pass", "11 of 11")
R("B67", "Only Gaia DR4 separates B from anything", "R63", r"(Only Gaia DR4 separates B from anything), and only from the bare MOND-type law", "only Gaia DR4 separates B from anything")
R("B67", "before any CFG61 scoring script exists", "R61", r"\*\*(before any CFG61 scoring script exists)", "before any CFG61 scoring script exists")
# B51 limitations additions
R("B51", "Written by a delegated agent", "R58", r"(Written by a delegated agent)", "were likewise written by a delegated agent")
R("B51", "Written by a delegated agent", "R59", r"(Written by a delegated agent)", "were likewise written by a delegated agent")
R("B51", "Written by a delegated agent", "R64", r"(Written by a delegated agent)", "were likewise written by a delegated agent")
R("B51", "Written by a delegated agent", "R65", r"(Written by a delegated agent)", "were likewise written by a delegated agent")
R("B51", "Written by a delegated agent", "R49", r"(Written by a delegated agent)", "were likewise written by a delegated agent")
R("B51", "re-run by the orchestrating session", "R48", r"(re-run by the orchestrating session)", "re-run by the orchestrating session")
R("B51", "Hot gas", "R55", r"\*\*(Hot gas)\.\*\*", "CFG55 omits hot gas")
R("B51", "Isotropy is assumed", "R55", r"GC orbital anisotropy\.\*\* (Isotropy is assumed)", "assumes isotropic globular clusters")
R("B51", "the gate's own first variation not fed back", "R48", r"(the gate's own first variation not fed back)", "its ball gate's first variation is not fed back")
R("B51", "self-consistent refit", "R64", r"not a (self-consistent refit)", "kernel swap, not a refit")
R("B51", "The table does not say where the velocity is measured", "R54", r"(The table does not say where the velocity is measured)", "a velocity radius the source table does not carry")


# ---- second batch: commits that landed while this version was written (CFG49 referee + process note, CFG65 Duffy check, CFG66)
R("B62", "2.52", "R64", r"\| CFG51 \| H1 \| PASS → PASS \| Boötes I \+2\.46σ → \+(2\.52)σ \|", r"2.52$\sigma$")
R("B63", "match exactly", "R65", r"\*\*(match exactly)\*\*, with pivot", "match exactly")
R("B63", "arXiv:0804.2486", "R65", r"\((arXiv:0804\.2486)", "arXiv:0804.2486")
R("B63", "The published MNRAS version was not compared", "R65", r"(The published MNRAS version was not compared)", "the published MNRAS version was not compared")
R("B63", "1.75", "R65", r"about (1\.75) times A2 at every mass", "1.75 times A2")
R("B63", "convention, not the transcription, is the dominant systematic", "R65", r"so the (convention, not the transcription, is the dominant systematic)", "convention, not the transcription, is the dominant systematic")
R("B63", "A2 and A3 are the consistent rows", "R65", r"(A2 and A3 are the consistent rows)", "A2 and A3 are the consistent rows")
R("B63", "−2.3", "R65", r"and (−2\.3)σ \(A3\)", r"$-2.3\sigma$ (A3)")
R("B63", "A1 is a 200m row applied to a 200c mass", "R65", r"(A1 is a 200m row applied to a 200c mass)", "A1 is a 200m row applied to a 200c mass")
R("B57", "Nine of ten", "REF49", r"\*\*(Nine of ten) outputs are identical to the committed ones", "nine of ten outputs")
R("B57", "0.2500", "REF49", r"\*\*Ratio (0\.2500) on all 32 DE13 layers", "0.2500 on all 32 layers")
R("B57", "3.86 × 10²⁸", "REF49", r"maximum is (3\.86 × 10²⁸) J/m", r"3.86\times10^{28}")
R("B57", "the potential costs", "REF49", r"- (the potential costs)", "the potential costs")
R("B57", "CV6_C's switched-stiffness counts", "REF49", r"- (CV6_C's switched-stiffness counts)", r"CV6\_C's switched-stiffness counts")
R("B57", "CV6_D", "REF49", r"- (CV6_D)\.", r"CV6\_D")
R("B57", "no separate frozen-criteria file", "R49", r"has \*\*(no separate frozen-criteria file)\*\*", "no separate frozen-criteria file")
R("B57", "cannot be verified for this lane", "R49", r"(cannot be verified for this lane)", "cannot be verified for this lane")
R("B57", "below the standard of CFG48", "R49", r"It is (below the standard of CFG48)", "below the standard of CFG48")
R("B57", "declared in the scripts", "R49", r"as \"(declared in the scripts), after exploratory scans\", not as pre-registered", "declared in the scripts, not as pre-registered")
R("B51", "no separate frozen-criteria file", "R49", r"has \*\*(no separate frozen-criteria file)\*\*", "no frozen-criteria file")
R("B51", "The published MNRAS version was not compared", "R65", r"(The published MNRAS version was not compared)", "not the published version")

# B69 CFG66
R("B69", "53", "R66", r"\*\*Q1, Boötes I \((53) cleaned stars", "53 cleaned stars")
R("B69", "2.00", "R66", r"s_cold = (2\.00) km/s", "s_{\\rm cold}=2.00")
R("B69", "5.09", "R66", r"s_hot = (5\.09) \(", "s_{\\rm hot}=5.09")
R("B69", "2.31", "R66", r"improvement over one Gaussian is (2\.31)", "2.31")
R("B69", "0.155", "R66", r"P\(LR ≥ 2\.31\) = (0\.155)", "P=0.155")
R("B69", "+0.222", "R66", r"\*\*(\+0\.222) ± 0\.097 dex \(2\.29σ\)\*\*", r"$+0.222")
R("B69", "0.097", "R66", r"\*\*\+0\.222 ± (0\.097) dex \(2\.29σ\)\*\*", r"\pm0.097")
R("B69", "2.29", "R66", r"\*\*\+0\.222 ± 0\.097 dex \((2\.29)σ\)\*\*", r"2.29\sigma")
R("B69", "+0.202", "R66", r"canonical, (\+0\.202) \(2\.09σ\) alt", "alt $+0.202$")
R("B69", "2.09", "R66", r"canonical, \+0\.202 \((2\.09)σ\) alt", r"2.09\sigma")
R("B69", "−0.072", "R66", r"\*\*Cold-only offset: (−0\.072) ± 0\.203 \(−0\.35σ\)\*\*", r"$-0.072")
R("B69", "0.203", "R66", r"\*\*Cold-only offset: −0\.072 ± (0\.203) \(−0\.35σ\)\*\*", r"\pm0.203")
R("B69", "−0.35", "R66", r"\*\*Cold-only offset: −0\.072 ± 0\.203 \((−0\.35)σ\)\*\*", r"-0.35\sigma")
R("B69", "+0.007", "R66", r"replaces CFG51's \"(\+0\.007)\"", "+0.007")
R("B69", "12", "R66", r"\*\*Q2, Tucana II \((12) cleaned stars", "12 cleaned stars")
R("B69", "0.43", "R66", r"\((0\.43) km/s per half-light radius, position", "0.43")
R("B69", "3.4", "R66", r"an error of about (3\.4) km/s across", "about 3.4")
R("B69", "0.99", "R66", r"\(p = (0\.99), and 0\.99 by", "p=0.99")
R("B69", "+0.464", "R66", r"Offset \*\*(\+0\.464) ± 0\.128 dex \(3\.62σ\)\*\*", r"$+0.464")
R("B69", "3.62", "R66", r"Offset \*\*\+0\.464 ± 0\.128 dex \((3\.62)σ\)\*\*", r"3.62\sigma")
R("B69", "S1 and S2", "R66", r"the MUTATE run fails (S1 and S2) as required", "S1 and S2 as required")
R("B69", "normalisation bug", "R66", r"A (normalisation bug) in the agent's first run", "normalisation bug")
R("B69", "Written by a delegated agent", "R66", r"(Written by a delegated agent)", "written by a delegated agent")


# ---- third batch: coverage of remaining new literals
R("B55", "was written before any script", "R48", r"`GATES_FROZEN\.md` (was written before any script)", "were written before any script")
R("B55", "git cannot order them", "REF48", r"(git cannot order them)", "git cannot order them")
R("B55", "The birth times are consistent", "REF48", r"(The birth times are consistent) with", "birth times are consistent")
R("B62", "10⁻⁴ to 0.1", "R64", r"for y from (10⁻⁴ to 0\.1) \(the ultra-faint regime\)", r"$10^{-4}$ to 0.1")
R("B62", "30", "R64", r"up to y = (30),", "y=30")
R("B66", "3σ", "R54", r"excluding the six (3σ) gas upper limits", r"3$\sigma$ gas upper limits")
R("B67", "1.000", "R63", r"because both predict gamma-hat = (1\.000)", "1.000")

# ---------------------------------------------------------------- machinery
def norm_tex(s):
    s = s.replace("$", "").replace("\\,", " ").replace("~", " ")
    s = re.sub(r"\s*/\s*", "/", s)
    return re.sub(r"\s+", " ", s)


def default_tex(value):
    return value.replace("–", "--").replace("−", "-")


def tex_blocks():
    blocks, cur = {}, []
    for line in open(TEX, encoding="utf-8").read().split("\n"):
        m = re.match(r"% AUDIT: (B\d\d)\s*$", line)
        if m:
            blocks[m.group(1)] = norm_tex("\n".join(cur))
            cur = []
        elif not line.lstrip().startswith("%"):
            cur.append(line)
    return blocks


def run(mutate=None):
    blocks = tex_blocks()
    rows = [r for r in ROWS if r is not None]
    results = []
    used_blocks = set()
    for i, (b, value, f, rx, tex, kind) in enumerate(rows):
        used_blocks.add(b)
        if kind == "count":
            got = COUNTS[f]()
            label = f"[{b}] recount {f}"
            value = got
            src_ok = True
            lit = norm_tex(tex)
            # the recount's own value must be the value printed: it is the number inside the tex literal
            src_ok = re.search(r"\d+", tex).group(0) == got
        else:
            text = source(f)
            m = re.search(rx, text, re.M)
            got = nm(m.group(1)) if m else None
            label = f"[{b}] {f}: {value}"
            exp = nm(value)
            if mutate == "value" and i == mutate_index(rows):
                exp = exp.replace("7.52", "7.53")
                label += "  (MUTATED expected value)"
            src_ok = got == exp
            lit = norm_tex(tex if tex is not None else default_tex(value))
            if mutate == "tex" and i == mutate_index(rows):
                lit = lit + "0"
                label += "  (MUTATED tex literal)"
        tex_ok = lit in blocks.get(b, "")
        results.append((label, value, got, src_ok, tex_ok, lit))
    orphan = sorted(set(blocks) - used_blocks)
    return results, orphan


def mutate_index(rows):
    return next(i for i, r in enumerate(rows) if r[0] == "B12" and r[1] == "7.97 / 7.52")


if __name__ == "__main__":
    mode = "value" if "--mutate" in sys.argv else "tex" if "--mutate-tex" in sys.argv else None
    head = subprocess.run(["git", "-C", REPO, "rev-parse", "--short", "HEAD"], capture_output=True).stdout.decode().strip()
    print(f"PAPER37 audit against committed files at HEAD {head} (repo {REPO})" + (f"   [MUTATE: {mode}]" if mode else ""))
    results, orphan = run(mode)
    bad = 0
    for label, value, got, s_ok, t_ok, lit in results:
        ok = s_ok and t_ok
        bad += (not ok)
        if not ok or "-v" in sys.argv:
            why = ("source says %r" % got if not s_ok else "") + ("; not printed in its tex block as %r" % lit if not t_ok else "")
            print(f"  [{'ok ' if ok else 'BAD'}] {label:60s} {why}")
    if orphan:
        print("  note: tex blocks with no audit rows:", ", ".join(orphan))
    n = len(results)
    print(f"\n{n - bad} of {n} quoted values match their committed sources and their tex blocks")
    if mode:
        print("MUTATE run: %s" % ("FAILED as required (exit 1)" if bad else "DID NOT FAIL -- the audit is not sensitive"))
    sys.exit(1 if bad else 0)
