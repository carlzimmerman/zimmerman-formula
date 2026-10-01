#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PAPER39 audit: every number carried by an audit row is re-read from a COMMITTED file (git HEAD) and checked twice.

For each audited value the script checks that
  (1) the value appears verbatim in its committed source (a regex with one capture group, run over the file as committed at HEAD,
      read with `git show HEAD:<path>`, never the working tree), and
  (2) the value is printed in the .tex block that carries its `% AUDIT: Bnn` tag (the block = the non-comment lines since the
      previous tag).
Three further row kinds (v1.1):
  * derived rows: the tex literal is a stated function of the committed value (a rounding, or 25 - 5), so the printed number
    follows the source;
  * count rows: the committed value is the number of matches of a regex in the source (optionally inside a scope regex);
  * self rows (block B47): the Reproducibility paragraph must state how many rows read the status page, out of how many, and must
    name every source file the rows read.
Exit 0 only if every row matches.  Reports "N of N".
Coverage: only numbers carried by a row below are checked; the tex side is checked anywhere in the tagged block, not in a
particular sentence; numbers quoted only in running text (for example the route counts 25 / 22 / 2 / 1, which are a recount of the
note's own table) and the references' journal data are not checked by this script.

Usage:   python3 PAPER39_audit.py               # main run
         python3 PAPER39_audit.py --mutate      # alters ONE expected value (0.79 -> 0.78, block B30); must exit 1
         python3 PAPER39_audit.py --mutate-tex  # alters ONE tex literal in memory (same row); must exit 1
         python3 PAPER39_audit.py -v            # print every row
Environment: PAPER39_REPO (repo root; default = two levels above this file).
"""
import os, re, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("PAPER39_REPO") or os.path.abspath(os.path.join(HERE, "..", ".."))
TEX = os.path.join(HERE, "PAPER39_closure_map_2026.tex")
CFG = "campaign_fresh_gravity/"
CM = CFG + "closure_map/"
LEAN = "fable_independent_2026/lean_2026/ChainCert/"
# key: (path at HEAD, the label the Reproducibility paragraph must print for it)
SRC = {
    "STAND": (CFG + "STANDING_2026-09-29.md", "STANDING_2026-09-29.md"),
    "GAPS": (CM + "GAPS_1_2_JOINT_STATUS.md", "GAPS_1_2_JOINT_STATUS.md"),
    "TEN": (CM + "TEN_DOORS_RESULT_2026-09-29.md", "TEN_DOORS_RESULT"),
    "TENG": (CM + "TEN_DOORS_GATES_2026-09-29.md", "TEN_DOORS_GATES"),
    "D11": (CM + "DOOR11_RESULT_2026-09-29.md", "DOOR11_RESULT"),
    "VER": (CM + "VERIFICATION_REPORTED_ONLY_2026-09-29.md", "VERIFICATION_REPORTED_ONLY"),
    "WWD": (CM + "WHAT_WOULD_DECIDE_2026-09-29.md", "WHAT_WOULD_DECIDE"),
    "CFG0": (CFG + "CFG0_README.md", "CFG0_README.md"),
    "R28": (CFG + "CFG28_README.md", "CFG28"),
    "R43": (CFG + "CFG43_fluid_tie/README.md", "CFG43"),
    "R63": (CFG + "CFG63_discrimination_forecast/README.md", "CFG63"),
    "R200": (CFG + "CFG200_dr4_merge_band_forecast/README.md", "CFG200"),
    "R230": (CFG + "CFG230_requirements_synthesis/CFG230_README.md", "CFG230"),
    "R231": (CFG + "CFG231_door12_emergent_gravity/README.md", "CFG231"),
    "R232": (CFG + "CFG232_door13_bimond/README.md", "CFG232"),
    "R242": (CFG + "CFG242_closure_swing/README.md", "CFG242"),
    "R243": (CFG + "CFG243_turnaround_dust/README.md", "CFG243"),
    "R244": (CFG + "CFG244_bound_fluid/README.md", "CFG244"),
    "R245": (CFG + "CFG245_relaxing_fluid/README.md", "CFG245"),
    "R251": (CFG + "CFG251_door11D_one_time_pass/README.md", "CFG251"),
    "R253": (CFG + "CFG253_dark_energy_to_cold_mass/README.md", "CFG253"),
    "R259": (CFG + "CFG259_ufd_variants_rescore/README.md", "CFG259"),
    "R265": (CFG + "CFG265_paper39_referee/README.md", "CFG265"),
    "R265RC": (CFG + "CFG265_paper39_referee/CFG265_route_recount.out", "CFG265_route_recount.out"),
    "R265P": (CFG + "CFG265_paper39_referee/CFG265_physics.out", "CFG265_physics.out"),
    "FOOT": ("real_research/reviews/mi_a0_profile_likelihood_milgrom_footing_2026.out",
             "mi_a0_profile_likelihood_milgrom_footing_2026.out"),
    "PRE": ("prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md", "PREREGISTRATION_DR4.md"),
    "EDGE": ("prep_2026/gaia_dr4_prep/dr4_ready_1/edge_table_dr4.json", "edge_table_dr4.json"),
    "P38": ("qwen_claude_field_theory/papers_2026/PAPER38_a0z_calibration_wall_2026.tex", "PAPER38_a0z_calibration_wall_2026.tex"),
    "LEANR": (LEAN + "README.md", "ChainCert/README.md"),
    "LEANV": (LEAN + "verify_chain.out", "verify_chain.out"),
    "LEANF": (LEAN + "Footing.lean", "Footing.lean"),
}
_cache = {}


def source(key):
    """The file as committed at HEAD (never the working tree)."""
    if key not in _cache:
        r = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + SRC[key][0]], capture_output=True)
        if r.returncode != 0:
            raise SystemExit(f"cannot read {SRC[key][0]} at HEAD (not committed?): {r.stderr.decode()[:200]}")
        _cache[key] = r.stdout.decode("utf-8")
    return _cache[key]


def nm(s):
    return s.replace("−", "-")


ROWS = []  # (block, value, file, regex, tex, kind, scope)


def R(b, value, f, rx, tex=None):
    """A value row. `tex` is a literal, or a function of the expected value (a derived row: rounding or subtraction)."""
    ROWS.append((b, value, f, rx, tex, "value", None))


def RC(b, value, f, rx, tex, scope=None):
    """A count row: the committed value is the number of matches of `rx` in the source (inside `scope` if given)."""
    ROWS.append((b, value, f, rx, tex, "count", scope))


def RS(b, what):
    """A self row on the Reproducibility block: `what` is 'stand_count' or 'sources'."""
    ROWS.append((b, what, None, None, None, "self", None))


def rnd(nd, fmt="{}"):
    """Derived literal: the committed value rounded to nd decimals, placed in fmt."""
    return lambda v: fmt.format(f"{float(v):.{nd}f}")


# ---------------------------------------------------------------- B01 abstract
R("B01", "331", "LEANV", r"theorems checked: (331);", "331 theorems")
R("B01", "24", "R265", r"Without it the count is (24) \(22 / 1 / 1\)", "the count is 24")
R("B01", "one to three", "R265", r"Only two items rest on more than the failure of (one to three) scored classes each",
  "one to three scored classes")
R("B01", "0.1200", "STAND", r"Ω h² = (0\.1200) × 10\^−1376\.8", r"0.1200\times10^{-1376.8}")
R("B01", "−1376.8", "STAND", r"Ω h² = 0\.1200 × 10\^(−1376\.8)", r"10^{-1376.8}")
R("B01", "0.791", "STAND", r"n\(t_ff\) = (0\.791)", "n=0.791")
R("B01", "0.99", "STAND", r"against the required (0\.99)\.", "required 0.99")
R("B01", "0.33–0.34", "STAND", r"M\^p with p = (0\.33–0\.34)", "M^{0.33-0.34}")
R("B01", "0.79", "STAND", r"Γτ = (0\.79) \(H_Λ\)", r"\Gamma\tau\le0.79")
R("B01", "4.1–4.2", "STAND", r"against the ≈ (4\.1–4\.2) needed", r"\approx4.1--4.2")
R("B01", "3.5–3.9", "STAND", r"z stays (3\.5–3\.9)σ on both footings", r"3.5--3.9\sigma")
R("B01", "0.28", "R244", r"P\(H2 \| truth b\) = (0\.28)\*\*", "power 0.28")
R("B01", "0.465 ± 0.076", "CFG0", r"measured (0\.465 ± 0\.076) \(BTFR\)", r"0.465\pm0.076")
R("B01", "2 Dec 2026", "STAND", r"Gaia DR4 \((2 Dec 2026)\)", "2 December 2026")
R("B01", "ν_RAR", "D11", r"uses the (ν_RAR) kernel", r"\nu_{\rm RAR}")
R("B01", "2.3–3.7", "R200", r"separation from ownership is (2\.3–3\.7)σ canonical", r"2.3--3.7\sigma")
R("B01", "30,000", "STAND", r"out of ~(30,000) expected", "N=30{,}000")
R("B01", "1.000", "STAND", r"B predicts γ̂ = (1\.000);", r"\hat\gamma=1.000")
# ---------------------------------------------------------------- B02-B06 the law and the gaps
R("B02", "9.36e-11", "R244", r"rounded footings (9\.36e-11) and 1\.13e-10", "canonical 9.36e-11")
R("B02", "1.13e-10", "R244", r"rounded footings 9\.36e-11 and (1\.13e-10)", "alternative 1.13e-10")
R("B02", "0.1003", "STAND", r"the rms is (0\.1003) dex", "0.1003 dex")
R("B02", "0.2755", "STAND", r"Newton's (0\.2755)", "0.2755 for Newton")
R("B02", "0.10", "STAND", r"to the (0\.10) dex that a decisive", "0.10 dex")
R("B03", "0.1200", "R245", r"\(Omega_c h\^2 = (0\.1200)\) is still REQUIRED", r"\Omega_ch^2=0.1200")
R("B03", "4", "TEN", r"^\| (4) superfluid \(CFG122, b7d41c302\)", "doors 4 and 7 scored particle models")
R("B03", "7", "TEN", r"^\| (7) fuzzy DM soliton \(CFG119, 435cb43e9\)", "doors 4 and 7 scored particle models")
R("B04", "44 of 48", "STAND", r"unstable in (44 of 48) cases", "44 of 48 cases")
R("B04", "48 of 48", "STAND", r"stable in (48 of 48) cases", "48 of 48")
R("B04", "0.11–0.24", "STAND", r"edge sits at (0\.11–0\.24) r_ta", "0.11--0.24")
R("B05", "0.065–22.5", "STAND", r"baryons at (0\.065–22\.5) g_law", "0.065--22.5")
R("B05", "23–73", "STAND", r"costs (23–73)× their orbital energy", r"23--73\times")
R("B05", "57–318", "STAND", r"or (57–318)× in B's committed r_ta", r"57--318\times")
R("B05", "54", "GAPS", r"of (54) committed constructions", "54 committed constructions")
R("B05", "D = 0, P = 11, I = 5, X = 27, U = 11", "GAPS", r"\((D = 0, P = 11, I = 5, X = 27, U = 11)\)")
R("B06", "needs a new constant", "R43", r"the natural saturating form (needs a new constant)", "needs a new constant")
R("B06", "11× up to 1e4–1e5", "GAPS", r"corrected value, (11× up to 1e4–1e5)", r"11\times up to 1e4--1e5")
R("B06", "10⁴", "R43", r"against the (10⁴) the BTFR needs", "against the 1e4 the BTFR needs")
# ---------------------------------------------------------------- B07-B08 Lean
R("B07", "331", "LEANV", r"theorems checked: (331);", "331 theorems checked")
R("B07", "0", "LEANV", r"with non-standard axioms: (0);", "0 with non-standard axioms")
R("B07", "0", "LEANV", r"sorry mentions: (0)", r"0 \texttt{sorry} mentions")
R("B07", "47 theorems, 219", "LEANR", r"; (47 theorems, 219) in the library\)", "47 theorems, 219 in the library")
R("B07", "62 theorems, 281", "LEANR", r"; (62 theorems, 281) in the library\)", "62 theorems, 281")
R("B07", "50 theorems, 331", "LEANR", r"; (50 theorems, 331) in the library\)", "50 theorems, 331")
R("B07", "Lean certifies implications from premises, not data", "STAND", r"(Lean certifies implications from premises, not data)\.",
  "Lean certifies implications from premises, not data.")
R("B08", "linear-in-source laws and screened laws", "D11", r"(linear-in-source laws and screened laws) also escape the no-EFE theorem",
  "linear-in-source and screened laws also escape")
R("B08", "3σ/√N", "STAND", r"σ\(log a₀\) ≥ (3σ/√N) with f free", r"\ge3\sigma/\sqrt N")
# ---------------------------------------------------------------- B09 how the routes were frozen; which gates
R("B09", "5 of 25", "R265RC", r"NOT COMMITTED STRICTLY BEFORE THE FIRST SCRIPT: (5 of 25)",
  lambda v: "for %d of the %s" % (int(v.split(" of ")[1]) - int(v.split(" of ")[0]), v.split(" of ")[1]))  # derived: 25 - 5
DOORS5 = "doors 5, 8, 11A, 11D and CFG253"
R("B09", "5", "R265RC", r"^\s+(5) collisional \$f\(E,L\)\$\s+CFG130\s+SAME COMMIT", DOORS5)
R("B09", "8", "R265RC", r"^\s+(8) interacting vacuum\s+CFG131\s+SAME COMMIT", DOORS5)
R("B09", "11A", "R265RC", r"^\s+(11A) inflow\S*\s+CFG171\s+SAME COMMIT", DOORS5)
R("B09", "11D", "R265RC", r"^\s+(11D) one-time pass\S*\s+CFG251\s+SAME COMMIT", DOORS5)
R("B09", "CFG253", "R265RC", r"^\s+dark energy into cold mass\S*\s+(CFG253)\s+SAME COMMIT", DOORS5)
R("B09", "12 of 25", "R265", r"holds for (12 of 25) rows",
  lambda v: "Of the %s rows, %s" % (v.split(" of ")[1], v.split(" of ")[0]))  # derived: the same numbers reordered
R("B09", "G1–G8", "D11", r"^Gates (G1–G8) as in DOOR11_FLOWING_VACUUM_GATES", "G1--G8, with G1 the law")
R("B09", "10", "TENG", r"to within (10)% over x", r"within 10\%")
R("B09", "0.10", "TENG", r"reaction on the baryons ≤ (0\.10) g_law", r"\le0.10 g_{\rm law}")
R("B09", "24", "R265", r"Without it the count is (24) \(22 / 1 / 1\)", "the count is 24")
# ---------------------------------------------------------------- B10-B31 the doors table
R("B10", "sqrt(1000)", "TEN", r"a (sqrt\(1000\)) mass spread", "a sqrt(1000) mass spread")
R("B11", "(1+x)/x", "TEN", r"C_V/C_target=(\(1\+x\)/x)", "=(1+x)/x")
R("B12", "140", "TEN", r"Q\^2/kappa_I >= ~(140)", r"\gtrsim140")
R("B12", "0.16", "TEN", r"<= (0\.16) \(V_U\)", r"\le0.16")
R("B12", "1.2", "TEN", r"/ (1\.2) \(V_B\)", "1.2 from growth")
R("B13", "M^0.33", "TEN", r"turnaround \((M\^0\.33)\)", "M^{0.33}")
R("B13", "4–360", "STAND", r"(4–360) at x ≈ 0\.1 for the spheres", "4--360")
R("B13", "0.05–0.21", "STAND", r"and (0\.05–0\.21) at x ≈ 28", "0.05--0.21")
R("B14", "1.28e-20", "TEN", r"m >= (1\.28e-20) eV", r"1.28\times10^{-20}")
R("B15", "32-353", "TEN", r"differs (32-353)x", r"32--353\times")
R("B16", "10", "TEN", r"negative density ~(10) orders too small", "about 10 orders too small")
R("B17", "0<gt<2/3", "TEN", r"ghost for (0<gt<2/3)", "0<g t<2/3")
R("B18", "16–205", "D11", r"F \(literal medium (16–205)× E_orb\)", r"16--205\times")
R("B19", "1.2e-6", "D11", r"T1 ≤ (1\.2e-6)", r"\le1.2\times10^{-6}")
R("B20", "6.3e3", "D11", r"F \(Q₂ tail (6\.3e3)×\)", r"6.3\times10^3")
R("B21", "1e-6", "D11", r"G1 needs t ≲ (1e-6)", r"t\lesssim10^{-6}")
R("B21", "4e6", "D11", r"G6 and G7 need t ≳ (4e6)", r"t\gtrsim4\times10^6")
R("B22", "96/96", "D11", r"at every radius in (96/96) cells", "96/96 cells")
R("B22", "4e3–9e3", "D11", r"median c_eff (4e3–9e3) km/s", "4e3--9e3 km/s")
R("B22", "37", "D11", r"against a (37) km/s line", "37 km/s line")
R("B23", "15.6", "R251", r"a literal freeze is (15\.6)× short at the edge", r"15.6\times short")
R("B24", "eight", "R231", r"G1 for all (eight) variants", "all eight variants")
R("B24", "6.1e3", "R231", r"Q₂ = (6\.1e3) × the bound", r"6.1\times10^3")
R("B25", "1.10", "R232", r"crosses (1\.10) at x = 0\.483", "crossing 1.10")
R("B25", "0.483", "R232", r"crosses 1\.10 at x = (0\.483)", "x=0.483")
R("B26", "0.791", "STAND", r"n\(t_ff\) = (0\.791)", "=0.791")
R("B26", "0.143", "STAND", r"n\(t_ff\) = 0\.791, minimum (0\.143)", "minimum 0.143")
R("B26", "0.99", "STAND", r"against the required (0\.99)\.", "required 0.99")
R("B27", "0", "R242", r"c_T\^2 = 1 \+ 4 mu/b = (0),", "c_T^2=0")
R("B27", "nullity 2", "STAND", r"determinacy \((nullity 2)\)", "nullity 2")
R("B28", "0.1200", "STAND", r"Ω h² = (0\.1200) × 10\^−1376\.8", r"0.1200\times10^{-1376.8}")
R("B28", "−1376.8", "STAND", r"Ω h² = 0\.1200 × 10\^(−1376\.8)", r"10^{-1376.8}")
R("B28", "2.8–38", "STAND", r"Even at z = 10 it is (2\.8–38)× short", r"2.8--38\times")
R("B29", "0.33–0.34", "STAND", r"M\^p with p = (0\.33–0\.34)", "p=0.33--0.34")
R("B29", "3.0–3.2", "STAND", r"spreads by (3\.0–3\.2)× over", r"3.0--3.2\times")
R("B29", "1.22", "STAND", r"against the (1\.22) allowed", "1.22 allowed")
R("B30", "0.79", "STAND", r"Γτ = (0\.79) \(H_Λ\)", r"\Gamma\tau=0.79")
R("B30", "0.14–0.16", "STAND", r"(0\.14–0\.16) \(a₀/c\)", "0.14--0.16")
R("B30", "0.27–0.33", "STAND", r"or (0\.27–0\.33) \(√\(Gρ_Λ\)\)", "0.27--0.33")
R("B30", "4.1–4.2", "STAND", r"against the ≈ (4\.1–4\.2) needed", r"\approx4.1--4.2")
R("B31", "3", "R253", r"\((3)% of today's cold mass made after recombination\)", r"declared 3\% tolerance")
R("B31", "0.5–1.6", "R253", r"allows only (0\.5–1\.6)% of the cold mass", r"0.5--1.6\%")
R("B31", "1", "R253", r"fails CFG131's (1)% line", r"CFG131's 1\% flat")
# ---------------------------------------------------------------- B32 referees and triage
RC("B32", "9", "TEN", r"[Dd]oor \d+ CFG15\d", lambda v: {"9": "Nine of the ten doors"}.get(v, "<no word for %s>" % v),
   scope=r"(?s)^## Appended note:.*?^- Door 2 \(CFG117\): no referee lane\.")
RC("B32", "6", "TEN", r"CFG15\d", lambda v: {"6": "six of those results"}.get(v, "<no word for %s>" % v),
   scope=r"^- Door 1 CFG151 .*$")
R("B32", "Not re-verified here", "TEN", r"reproducing their headlines.*(Not re-verified here)\.", "not re-verified by the orchestrator")
R("B32", "were not blind to the README numbers", "TEN", r"Referees (were not blind to the README numbers)\.",
  "were not blind to the README numbers")
R("B32", "20", "GAPS", r"scored (20) untested routes", "scored 20 untested routes")
R("B32", "1.3e-3", "GAPS", r"P\(all gates\) ≤ (1\.3e-3) each", r"\le 1.3e-3 each")
# ---------------------------------------------------------------- B33-B38 the reading of the requirements
R("B33", "one to three", "R265", r"Only two items rest on more than the failure of (one to three) scored classes each",
  "one to three scored classes")
R("B33", "Doors 1, 3, 4 and 9", "TEN", r"(Doors 1, 3, 4 and 9) fail for different reasons and are not covered by this reading",
  "doors 1, 3, 4 and 9 fail for other reasons and are not covered by this reading")
R("B33", "−1376.8", "STAND", r"Ω h² = 0\.1200 × 10\^(−1376\.8)", r"0.1200\times10^{-1376.8}")
R("B33", "0.076", "R243", r"over R = 1e-3 to 100 Mpc is (0\.076) against the threshold 1\.276", "0.076")
R("B33", "1.276", "R243", r"over R = 1e-3 to 100 Mpc is 0\.076 against the threshold (1\.276)", "threshold 1.276")
R("B34", "0.791", "STAND", r"n\(t_ff\) = (0\.791)", "=0.791 against 0.99")
R("B34", "5.0", "R242", r"n first reaches 0\.99 at 5\.6 t_dyn = (5\.0) free-fall times", "5.0 free-fall times")
R("B34", "0.16-0.21", "R243", r"only (0\.16-0\.21) first turn around", "0.16--0.21")
R("B35", "5.37 / 5.17", "R245", r"Gamma >= \*\*(5\.37 / 5\.17) H_Lambda\*\*", "5.37 / 5.17")
R("B35", "0.15–0.28", "STAND", r"\((0\.15–0\.28) dex against the 0\.10 line", "0.15--0.28 dex")
R("B35", "1.73, 1.93", "R245", r"\[Gamma_T,min, Gamma_C,max\] = \[(1\.73, 1\.93)\] H_Lambda \(canonical\)", "1.73--1.93")
R("B36", "2.33", "R245", r"R_loc up to (2\.33) for P2", "up to 2.33")
R("B36", "3.16", "R245", r"ratio up to (3\.16) where the owned reading needs 1", "up to 3.16")
R("B37", "1.9e-4", "R242", r"at most (1\.9e-4) of the vacuum energy of its ball", "1.9e-4")
R("B37", "24.8", "STAND", r"CFG243: f\(30\) = (24\.8);", "f(30)=24.8")
R("B37", "1.7", "STAND", r"Lagrangian-volume ledger (1\.7) against 1", "1.7 against 1")
R("B37", "0.30-1.65", "R243", r"\*\*(0\.30-1\.65) at x = 30 in B's committed r_ta\*\*", "0.30--1.65")
R("B38", "4.608e-12", "R230", r"c_s\^2 <= (4\.608e-12)", "4.608e-12")
R("B38", "22.5", "STAND", r"strict G3 reaction is (22\.5) g_law", "22.5")
R("B38", "3.5e3", "R230", r"screening factor >= (3\.5e3)", r"\ge 3.5e3")
R("B38", "0.28205", "R230", r">= (0\.28205) a0", r"\ge 0.28205 a_0")
# ---------------------------------------------------------------- B39-B41 satellites
R("B39", "+0.3245 ± 0.038", "R259", r"\| DV0 \| the committed LVD values \| (\+0\.3245 ± 0\.038) \(3\.77σ\)", r"+0.3245\pm0.038")
R("B39", "3.77", "R259", r"\| DV0 \| the committed LVD values \| \+0\.3245 ± 0\.038 \((3\.77)σ\)", r"3.77\sigma")
R("B39", "0.077", "R28", r"\| (0\.077) dex \| 0\.077 dex \|", "0.077-dex")
R("B39", "3.5–5", "STAND", r"pass window spans (3\.5–5) decades", "3.5--5 decades")
R("B40", "0.005", "R259", r"moves by at most (0\.005) dex", "at most 0.005 dex")
R("B40", "3.5 to 3.9", "R259", r"significance stays (3\.5 to 3\.9)σ", r"3.5 to 3.9\sigma")
R("B40", "8 of 40", "STAND", r"reach only (8 of 40) systems", "8 of 40 systems")
R("B40", "−0.068", "R259", r"median (−0\.068) dex, range", "-0.068 dex")
R("B40", "−0.104", "R259", r"\(median (−0\.104), range", "-0.104 dex")
R("B40", "reported row, not a verdict", "R259", r"weak-binary subsample \((reported row, not a verdict)\)", "reported row, not a verdict")
R("B40", "2.8 / 2.6", "STAND", r"drops to (2\.8 / 2\.6)σ under", r"2.8\sigma/2.6\sigma")
R("B41", "+13.58 / +11.32", "R259", r"\| DV0 \| (\+13\.58 / \+11\.32) \|", "+13.58/+11.32")
R("B41", "+8.60", "R259", r"alt-footing Δχ²_V2 (\+8\.60)", "+8.60")
R("B41", "0.24", "R259", r"sits only (0\.24) above 9", "0.24 above 9")
R("B41", "0.28", "R244", r"P\(H2 \| truth b\) = (0\.28)\*\*", "power is 0.28")
R("B41", "−1.3 to −1.8", "R259", r"without them it is (−1\.3 to −1\.8) at DV0", "-1.3 to -1.8")
R("B41", "33 of the 40", "R244", r"and (33 of the 40) UFDs take the clamped Moster value", "33 of the 40")
# ---------------------------------------------------------------- B42-B43 kappa and 32 pi (B42 also holds "What this implies")
R("B42", "is LambdaCDM there", "R244", r"a bound-core reading that matches LambdaCDM at satellites (is LambdaCDM there)",
  r"is \LambdaCDM there")
R("B42", "0.465 ± 0.076", "CFG0", r"measured (0\.465 ± 0\.076) \(BTFR\)", r"0.465\pm0.076")
R("B42", "0.547 ± 0.175", "CFG0", r"and (0\.547 ± 0\.175) \(distance-free\)", r"0.547\pm0.175")
R("B42", "1.447", "STAND", r"κ = (1\.447), 12\.9σ off", r"\kappa=1.447")
R("B42", "12.9", "STAND", r"κ = 1\.447, (12\.9)σ off", r"12.9\sigma off")
R("B42", "5.34 vs 7.04", "VER", r"\(Δχ² (5\.34 vs 7\.04) alt\)", "5.34, against 7.04 alt")
R("B42", "5.34", "FOOT", r"Milgrom cH0/2pi \(own footing\)\s+1\.0421\s+0\.9680\s+(5\.34)", "5.34, against")
R("B42", "7.04", "FOOT", r"alt footing rho_tot/cH0\s+1\.1300\s+1\.0496\s+(7\.04)", "7.04 alt")
R("B42", "63.90", "FOOT", r"kappa = 1/2\s+\(THE FRAMEWORK\)\s+0\.9361\s+0\.8696\s+(63\.90)", rnd(1, "{} canonical"))  # derived
R("B42", "3H^2/(8 pi G)", "LEANF", r"written as `kappa c sqrt\(G rho\)` with `rho = (3H\^2/\(8 pi G\))`", r"\rho=3H_0^2/(8\pi G)")
R("B42", "sqrt(2/(3 pi))", "LEANR", r"is `kappa = (sqrt\(2/\(3 pi\)\))`", r"\kappa=\sqrt{2/(3\pi)}")
R("B42", "0.4607", "R265P", r"rho = rho_crit = 3H0\^2/\(8 pi G\): kappa = sqrt\(2/\(3 pi\)\) = (0\.4607)",
  rnd(3, r"\sqrt{{2/(3\pi)}}={}"))  # derived
R("B42", "0.5567", "R265P", r"kappa = sqrt\(2/\(3 pi Omega_L\)\) = (0\.5567)", rnd(2, "about {}"))  # derived
R("B43", "0.824", "STAND", r"forces R = G_cosm/G_N < (0\.824)", r"G_N<0.824")
R("B43", "0.98 ± 0.06", "STAND", r"G_BBN/G₀ = (0\.98 ± 0\.06)", r"0.98\pm0.06")
R("B43", "95.4", "STAND", r"G_BBN/G₀ = 0\.98 ± 0\.06 at (95\.4)% for BBN ONLY", r"at 95.4\%")
R("B43", "9", "STAND", r"arXiv:1910\.10730, eq\. \((9)\)", "eq. 9")
R("B43", "constant couplings through BBN", "STAND", r"(constant couplings through BBN), standard radiation and rates",
  "constant couplings through BBN, standard radiation and rates")
R("B43", "1198", "STAND", r"C > (1198) follows", "C>1198")
R("B43", "0.92", "STAND", r"at R ≥ (0\.92)", r"R\ge0.92")
R("B43", "8π", "STAND", r"R\*²Λ = (8π)", r"\Lambda=8\pi")
R("B43", "4", "STAND", r"The rational (4) in Gρ_Λ = 4a₀²", r"G\rho_\Lambda=4a_0^2")
# ---------------------------------------------------------------- B44-B46 what decides
R("B44", "1.000", "STAND", r"B predicts γ̂ = (1\.000);", r"\hat\gamma=1.000")
R("B44", "ν_RAR", "D11", r"uses the (ν_RAR) kernel", r"\nu_{\rm RAR}")
R("B44", "1.1614", "EDGE", r'"name": "Arm A band floor \(Amdt 10\), canonical",\s*"gamma": (1\.1614)', rnd(3, "floor at {}"))  # derived
R("B44", "1.1917", "EDGE", r'"name": "Arm A band floor \(Amdt 10\), alt footing",\s*"gamma": (1\.1917)', rnd(3, "(alt {})"))  # derived
R("B44", "0.02", "STAND", r"frozen σ_sys = (0\.02)", r"\sigma_{\rm sys}=0.02")
R("B44", "8.1", "R63", r"Arm A floor \(1\.1614; alt 1\.1917\) \| 0\.1614 \| 0\.020 \| \*\*(8\.1)\*\*", r"cap is 8.1\sigma")
R("B44", "4,342", "R63", r"\| \*\*(4,342) pairs\*\* \(alt 2,940\)",
  lambda v: "about {:,} pairs".format(round(int(v.replace(",", "")) / 100) * 100))  # derived: rounded to hundreds
R("B44", "30,000", "STAND", r"out of ~(30,000) expected", "30,000 expected")
R("B44", "1.056", "PRE", r"\| 1\.007 – (1\.056) \| falsified \(≥ 3\.8σ_tot\) \|", "below 1.056")
R("B44", "1.056", "EDGE", r'"name": "Arm A falsified below \(Amdt 11\(d\)\)",\s*"gamma": (1\.056)', "below 1.056")
R("B44", "disfavored", "PRE", r"\| 1\.056 – 1\.084 \| (disfavored) \(2\.8–3\.8σ_tot\) \|", "1.056--1.084 as ``disfavored''")
R("B44", "1.063", "R200", r"\| \(a\) P2-merge floor (1\.063) vs ownership \(g_ext 2\.146e-10\)", "1.063--1.102")
R("B44", "1.102", "R200", r"\| \(a\) P2-merge top (1\.102) vs ownership \|", "1.063--1.102")
R("B44", "1.079", "D11", r"alt: 1\.111 / 1\.127 and (1\.079) / 1\.099", "1.079--1.127")
R("B44", "1.127", "D11", r"alt: 1\.111 / (1\.127) and 1\.079 / 1\.099", "1.079--1.127")
R("B44", "2.3–3.7", "R200", r"separation from ownership is (2\.3–3\.7)σ canonical", r"2.3--3.7\sigma")
R("B44", "2.86", "R200", r"and (2\.86) / 3\.59 for 2\.146e-10", rnd(1, "{}--"))  # derived
R("B44", "4.60", "R200", r"\(a\) is 4\.02 / (4\.60) for the primary g_ext", rnd(1, r"--{}\sigma alt"))  # derived
R("B44", "14,000–264,000", "R200", r"it needs (14,000–264,000) pairs for 3σ", "14,000--264,000 pairs")
R("B44", "0.2–1.1", "D11", r"P2-merge vs the chain ceiling: (0\.2–1\.1)σ, never 3σ at any N", r"0.2--1.1\sigma")
R("B44", "1.084", "PRE", r"\| (1\.084) – 1\.23 \| \*\*falsified\*\* \(z_C ≥ 3\) \*\*if\*\* the frozen stability requirements pass",
  r"1.084\le\hat\gamma")
R("B44", "1.23", "PRE", r"\| 1\.084 – (1\.23) \| \*\*falsified\*\* \(z_C ≥ 3\) \*\*if\*\*", r"\hat\gamma\le1.23")
R("B44", "the frozen stability requirements pass", "PRE", r"\*\*if\*\* (the frozen stability requirements pass): every ladder variant",
  "if the frozen stability requirements pass")
R("B45", "survives an unlimited sample", "P38", r"the limit that (survives an unlimited sample) is the absolute calibration",
  "the limit that survives an unlimited sample is the absolute baryon calibration")
R("B45", "statistical power or by the Newtonian regime", "P38", r"also limited by (statistical power or by the Newtonian regime)",
  "statistical power or by the Newtonian regime")
R("B45", "1.2", "P38", r"version 1\.3 \(version (1\.2)'s wording corrections after the independent referee CFG241", "version 1.2")
R("B45", "1.2–1.4", "STAND", r"lower by (1\.2–1\.4) dex", "1.2--1.4 dex")
R("B46", "2.5", "STAND", r"systematic floor \(ultra-faints (2\.5)σ", r"near 2.5\sigma")
R("B46", "0.077", "WWD", r"floors are the Upsilon_V range \((0\.077)\)", "0.077 and")
R("B46", "0.133", "WWD", r"the rule's collapse-mass floor \((0\.133)\)", "0.133 dex")
R("B46", "0.28", "R244", r"P\(H2 \| truth b\) = (0\.28)\*\*", "above 0.28")
# ---------------------------------------------------------------- B47 the Reproducibility block (self rows)
RS("B47", "stand_count")
RS("B47", "sources")
# ---------------------------------------------------------------- B48 the changes paragraph
R("B48", "1 CRITICAL, 3 MAJOR, 19 MINOR, 7 NIT", "R265", r"\*\*(1 CRITICAL, 3 MAJOR, 19 MINOR, 7 NIT)\*\* \(30 findings",
  "1 CRITICAL, 3 MAJOR, 19 MINOR, 7 NIT")
R("B48", "30", "R265", r"7 NIT\*\* \((30) findings", "30 findings")


# ---------------------------------------------------------------- machinery
def norm_tex(s):
    s = s.replace("$", "").replace("\\,", " ").replace("~", " ")
    s = re.sub(r"\s*/\s*", "/", s)
    return re.sub(r"\s+", " ", s)


def default_tex(value):
    return value.replace("–", "--").replace("−", "-")


def tex_blocks(text):
    blocks, cur = {}, []
    for line in text.split("\n"):
        m = re.match(r"\s*% AUDIT: (B\d\d)\s*$", line)
        if m:
            if m.group(1) in blocks:
                raise SystemExit(f"duplicate AUDIT tag {m.group(1)} in the tex")
            blocks[m.group(1)] = norm_tex("\n".join(cur))
            cur = []
        elif not line.lstrip().startswith("%"):
            cur.append(line)
    return blocks


def tag_order(text):
    return re.findall(r"^\s*% AUDIT: (B\d\d)\s*$", text, re.M)


MUTATE_KEY = ("B30", "0.79")


def mutate_index():
    return next(i for i, r in enumerate(ROWS) if (r[0], r[1]) == MUTATE_KEY)


def self_row(what, block):
    """Self rows on the Reproducibility block: the stated status-page share and the named sources must match the rows."""
    if what == "stand_count":
        n_stand = sum(1 for r in ROWS if r[2] == "STAND")
        exp = f"{n_stand} of the {len(ROWS)} rows"
        return exp, exp, exp in block, exp
    used = sorted({r[2] for r in ROWS if r[2]})
    missing = [SRC[k][1] for k in used if SRC[k][1] not in block]
    lit = "every source label" if not missing else "missing: " + ", ".join(missing)
    return "all named", "all named", not missing, lit


def run(mode=None):
    tex_text = open(TEX, encoding="utf-8").read()
    blocks = tex_blocks(tex_text)
    mi = mutate_index()
    results, used = [], set()
    for i, (b, value, f, rx, tex, kind, scope) in enumerate(ROWS):
        used.add(b)
        if kind == "self":
            got, exp, tex_ok, lit = self_row(value, blocks.get(b, ""))
            results.append((f"[{b}] self: {value}", got, got == exp, tex_ok, lit))
            continue
        text = source(f)
        if kind == "count":
            if scope:
                sm = re.search(scope, text, re.M)
                text = sm.group(0) if sm else ""
            got = str(len(re.findall(rx, text, re.M)))
        else:
            m = re.search(rx, text, re.M)
            got = nm(m.group(1)) if m else None
        exp = nm(value)
        label = f"[{b}] {f}: {value}" + ("  (count)" if kind == "count" else "") + ("  (derived)" if callable(tex) else "")
        if i == mi and mode == "value":
            exp = exp.replace("0.79", "0.78")
            label += "  (MUTATED expected value)"
        if callable(tex):
            lit = norm_tex(tex(exp))
        else:
            lit = norm_tex(tex if tex is not None else default_tex(value))
        if i == mi and mode == "tex":
            lit = lit.replace("0.79", "0.78")
            label += "  (MUTATED tex literal)"
        src_ok = got == exp
        tex_ok = lit in blocks.get(b, "")
        results.append((label, got, src_ok, tex_ok, lit))
    orphan = sorted(set(blocks) - used)
    missing = sorted(used - set(blocks))
    order = tag_order(tex_text)
    in_order = order == ["B%02d" % k for k in range(1, len(order) + 1)]
    return results, orphan, missing, in_order


if __name__ == "__main__":
    mode = "value" if "--mutate" in sys.argv else "tex" if "--mutate-tex" in sys.argv else None
    head = subprocess.run(["git", "-C", REPO, "rev-parse", "--short", "HEAD"], capture_output=True).stdout.decode().strip()
    print(f"PAPER39 audit against committed files at HEAD {head}" + (f"   [MUTATE: {mode}]" if mode else ""))
    results, orphan, missing, in_order = run(mode)
    bad = 0
    for label, got, s_ok, t_ok, lit in results:
        ok = s_ok and t_ok
        bad += (not ok)
        if not ok or "-v" in sys.argv:
            why = ("source says %r" % got if not s_ok else "") + ("; not printed in its tex block as %r" % lit if not t_ok else "")
            print(f"  [{'ok ' if ok else 'BAD'}] {label:70s} {why}")
    if orphan:
        print("  note: tex blocks with no audit rows:", ", ".join(orphan))
    if missing:
        print("  BAD: audit rows name blocks absent from the tex:", ", ".join(missing))
        bad += len(missing)
    if not in_order:
        print("  BAD: the AUDIT tags are not B01, B02, ... in text order")
        bad += 1
    n = len(results)
    n_stand = sum(1 for r in ROWS if r[2] == "STAND")
    print(f"  rows reading the status page: {n_stand} of {n}; derived rows: {sum(1 for r in ROWS if callable(r[4]))}; "
          f"count rows: {sum(1 for r in ROWS if r[5] == 'count')}; self rows: {sum(1 for r in ROWS if r[5] == 'self')}")
    print(f"\n{n - bad if bad <= n else 0} of {n} quoted values match their committed sources and their tex blocks")
    if mode:
        print("MUTATE run: %s" % ("FAILED as required (exit 1)" if bad else "DID NOT FAIL -- the audit is not sensitive"))
    sys.exit(1 if bad else 0)
