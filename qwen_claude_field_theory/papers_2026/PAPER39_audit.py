#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PAPER39 audit: every number carried by an audit row is re-read from a COMMITTED file (git HEAD) and checked twice.

For each audited value the script checks that
  (1) the value appears verbatim in its committed source (a regex with one capture group, run over the file as committed at HEAD,
      read with `git show HEAD:<path>`, never the working tree), and
  (2) the value is printed in the .tex block that carries its `% AUDIT: Bnn` tag (the block = the non-comment lines since the
      previous tag).
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
SRC = {
    "STAND": CFG + "STANDING_2026-09-29.md",
    "GAPS": CM + "GAPS_1_2_JOINT_STATUS.md",
    "TEN": CM + "TEN_DOORS_RESULT_2026-09-29.md",
    "TENG": CM + "TEN_DOORS_GATES_2026-09-29.md",
    "D11": CM + "DOOR11_RESULT_2026-09-29.md",
    "RD": CM + "RESEARCH_DIRECTION_2026-09-29.md",
    "VER": CM + "VERIFICATION_REPORTED_ONLY_2026-09-29.md",
    "CFG0": CFG + "CFG0_README.md",
    "R28": CFG + "CFG28_README.md",
    "R230": CFG + "CFG230_requirements_synthesis/CFG230_README.md",
    "R231": CFG + "CFG231_door12_emergent_gravity/README.md",
    "R232": CFG + "CFG232_door13_bimond/README.md",
    "R242": CFG + "CFG242_closure_swing/README.md",
    "R243": CFG + "CFG243_turnaround_dust/README.md",
    "R244": CFG + "CFG244_bound_fluid/README.md",
    "R245": CFG + "CFG245_relaxing_fluid/README.md",
    "R251": CFG + "CFG251_door11D_one_time_pass/README.md",
    "R259": CFG + "CFG259_ufd_variants_rescore/README.md",
    "LEANR": "fable_independent_2026/lean_2026/ChainCert/README.md",
    "LEANV": "fable_independent_2026/lean_2026/ChainCert/verify_chain.out",
}
_cache = {}


def source(key):
    """The file as committed at HEAD (never the working tree)."""
    if key not in _cache:
        r = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + SRC[key]], capture_output=True)
        if r.returncode != 0:
            raise SystemExit(f"cannot read {SRC[key]} at HEAD (not committed?): {r.stderr.decode()[:200]}")
        _cache[key] = r.stdout.decode("utf-8")
    return _cache[key]


def nm(s):
    return s.replace("−", "-")


ROWS = []  # (block, value, file, regex, tex)


def R(b, value, f, rx, tex=None):
    ROWS.append((b, value, f, rx, tex))


# ---------------------------------------------------------------- B01 abstract
R("B01", "331", "LEANV", r"theorems checked: (331);", "331 theorems")
R("B01", "0.1200", "STAND", r"Ω h² = (0\.1200) × 10\^−1376\.8", r"0.1200\times10^{-1376.8}")
R("B01", "−1376.8", "STAND", r"Ω h² = 0\.1200 × 10\^(−1376\.8)", r"10^{-1376.8}")
R("B01", "0.791", "STAND", r"n\(t_ff\) = (0\.791)", "n=0.791")
R("B01", "0.99", "STAND", r"against the required (0\.99)\.", "required 0.99")
R("B01", "0.33–0.34", "STAND", r"M\^p with p = (0\.33–0\.34)", "M^{0.33-0.34}")
R("B01", "0.79", "STAND", r"Γτ = (0\.79) \(H_Λ\)", r"\Gamma\tau\le0.79")
R("B01", "4.1–4.2", "STAND", r"against the ≈ (4\.1–4\.2) needed", r"\approx4.1--4.2")
R("B01", "3.5–3.9", "STAND", r"z stays (3\.5–3\.9)σ on both footings", r"3.5--3.9\sigma")
R("B01", "0.465 ± 0.076", "CFG0", r"measured (0\.465 ± 0\.076) \(BTFR\)", r"0.465\pm0.076")
R("B01", "2 Dec 2026", "STAND", r"Gaia DR4 \((2 Dec 2026)\)", "2 December 2026")
R("B01", "1.000", "STAND", r"B predicts γ̂ = (1\.000);", r"\hat\gamma=1.000")
# ---------------------------------------------------------------- B02-B06 the law and the gaps
R("B02", "9.36e-11", "R244", r"rounded footings (9\.36e-11) and 1\.13e-10", "canonical 9.36e-11")
R("B02", "1.13e-10", "R244", r"rounded footings 9\.36e-11 and (1\.13e-10)", "alternative 1.13e-10")
R("B02", "0.1003", "STAND", r"the rms is (0\.1003) dex", "0.1003 dex")
R("B02", "0.2755", "STAND", r"Newton's (0\.2755)", "0.2755 for Newton")
R("B02", "0.10", "STAND", r"to the (0\.10) dex that a decisive", "0.10 dex")
R("B03", "0.1200", "R245", r"\(Omega_c h\^2 = (0\.1200)\) is still REQUIRED", r"\Omega_ch^2=0.1200")
R("B04", "44 of 48", "STAND", r"unstable in (44 of 48) cases", "44 of 48 cases")
R("B04", "48 of 48", "STAND", r"stable in (48 of 48) cases", "48 of 48")
R("B04", "0.11–0.24", "STAND", r"edge sits at (0\.11–0\.24) r_ta", "0.11--0.24")
R("B05", "0.065–22.5", "STAND", r"baryons at (0\.065–22\.5) g_law", "0.065--22.5")
R("B05", "23–73", "STAND", r"costs (23–73)× their orbital energy", r"23--73\times")
R("B05", "57–318", "STAND", r"or (57–318)× in B's committed r_ta", r"57--318\times")
R("B05", "54", "GAPS", r"of (54) committed constructions", "54 committed constructions")
R("B05", "D = 0, P = 11, I = 5, X = 27, U = 11", "GAPS", r"\((D = 0, P = 11, I = 5, X = 27, U = 11)\)")
R("B06", "11× up to 1e4–1e5", "GAPS", r"corrected value, (11× up to 1e4–1e5)", r"11\times up to 1e4--1e5")
# ---------------------------------------------------------------- B07-B08 Lean
R("B07", "331", "LEANV", r"theorems checked: (331);", "331 theorems checked")
R("B07", "0", "LEANV", r"with non-standard axioms: (0);", "0 with non-standard axioms")
R("B07", "0", "LEANV", r"sorry mentions: (0)", r"0 \texttt{sorry} mentions")
R("B07", "47 theorems, 219", "LEANR", r"; (47 theorems, 219) in the library\)", "47 theorems, 219 in the library")
R("B07", "62 theorems, 281", "LEANR", r"; (62 theorems, 281) in the library\)", "62 theorems, 281")
R("B07", "50 theorems, 331", "LEANR", r"; (50 theorems, 331) in the library\)", "50 theorems, 331")
R("B07", "Lean certifies implications from premises, not data", "STAND", r"(Lean certifies implications from premises, not data)\.",
  "Lean certifies implications from premises, not data.")
R("B08", "3σ/√N", "STAND", r"σ\(log a₀\) ≥ (3σ/√N) with f free", r"\ge3\sigma/\sqrt N")
# ---------------------------------------------------------------- B09 the shared gates
R("B09", "10", "TENG", r"to within (10)% over x", r"within 10\%")
R("B09", "0.10", "TENG", r"reaction on the baryons ≤ (0\.10) g_law", r"\le0.10 g_{\rm law}")
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
R("B31", "3", "RD", r"at most about (3)% of the cold mass", r"about 3\% of the cold mass")
# ---------------------------------------------------------------- B32 referees and triage
R("B32", "were not blind to the README numbers", "TEN", r"Referees (were not blind to the README numbers)\.",
  "were not blind to the README numbers")
R("B32", "20", "GAPS", r"scored (20) untested routes", "scored 20 untested routes")
R("B32", "1.3e-3", "GAPS", r"P\(all gates\) ≤ (1\.3e-3) each", r"\le 1.3e-3 each")
# ---------------------------------------------------------------- B33-B38 the specification
R("B33", "−1376.8", "STAND", r"Ω h² = 0\.1200 × 10\^(−1376\.8)", r"0.1200\times10^{-1376.8}")
R("B33", "0.076", "R243", r"over R = 1e-3 to 100 Mpc is (0\.076) against the threshold 1\.276", "0.076")
R("B33", "1.276", "R243", r"over R = 1e-3 to 100 Mpc is 0\.076 against the threshold (1\.276)", "threshold 1.276")
R("B34", "0.791", "STAND", r"n\(t_ff\) = (0\.791)", "=0.791 against 0.99")
R("B34", "5.0", "R242", r"n first reaches 0\.99 at 5\.6 t_dyn = (5\.0) free-fall times", "5.0 free-fall times")
R("B34", "0.16-0.21", "R243", r"only (0\.16-0\.21) first turn around", "0.16--0.21")
R("B35", "5.37 / 5.17", "R245", r"Gamma >= \*\*(5\.37 / 5\.17) H_Lambda\*\*", "5.37 / 5.17")
R("B35", "0.15–0.28", "STAND", r"\((0\.15–0\.28) dex against the 0\.10 line", "0.15--0.28 dex")
R("B35", "1.7–1.9", "GAPS", r"near (1\.7–1\.9) H_Λ", "1.7--1.9")
R("B36", "2.33", "R245", r"R_loc up to (2\.33) for P2", "up to 2.33")
R("B36", "3.16", "R245", r"ratio up to (3\.16) where the owned reading needs 1", "up to 3.16")
R("B37", "1.9e-4", "R242", r"at most (1\.9e-4) of the vacuum energy of its ball", "1.9e-4")
R("B37", "24.8", "STAND", r"CFG243: f\(30\) = (24\.8);", "f(30)=24.8")
R("B37", "1.7", "STAND", r"Lagrangian-volume ledger (1\.7) against 1", "1.7 against 1")
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
R("B40", "2.8 / 2.6", "STAND", r"drops to (2\.8 / 2\.6)σ under", r"2.8\sigma/2.6\sigma")
R("B41", "+13.58 / +11.32", "R259", r"\| DV0 \| (\+13\.58 / \+11\.32) \|", "+13.58/+11.32")
R("B41", "+8.60", "R259", r"alt-footing Δχ²_V2 (\+8\.60)", "+8.60")
R("B41", "0.24", "R259", r"sits only (0\.24) above 9", "0.24 above 9")
R("B41", "0.28", "R244", r"P\(H2 \| truth b\) = (0\.28)\*\*", "power is 0.28")
R("B41", "-1.3", "R244", r"without P1 Delta = \*\*(-1\.3) \(V1\)", "about -1.3")
R("B41", "33 of the 40", "R244", r"and (33 of the 40) UFDs take the clamped Moster value", "33 of the 40")
# ---------------------------------------------------------------- B42-B43 kappa and 32 pi
R("B42", "0.465 ± 0.076", "CFG0", r"measured (0\.465 ± 0\.076) \(BTFR\)", r"0.465\pm0.076")
R("B42", "0.547 ± 0.175", "CFG0", r"and (0\.547 ± 0\.175) \(distance-free\)", r"0.547\pm0.175")
R("B42", "1.447", "STAND", r"κ = (1\.447), 12\.9σ off", r"\kappa=1.447")
R("B42", "12.9", "STAND", r"κ = 1\.447, (12\.9)σ off", r"12.9\sigma off")
R("B42", "5.34 vs 7.04", "VER", r"\(Δχ² (5\.34 vs 7\.04) alt\)", "5.34 against 7.04 alt")
R("B42", "sqrt(2/(3 pi))", "LEANR", r"is `kappa = (sqrt\(2/\(3 pi\)\))`", r"\kappa=\sqrt{2/(3\pi)}")
R("B43", "0.824", "STAND", r"forces R = G_cosm/G_N < (0\.824)", r"G_N<0.824")
R("B43", "0.98 ± 0.06", "STAND", r"G_BBN/G₀ = (0\.98 ± 0\.06)", r"0.98\pm0.06")
R("B43", "1198", "STAND", r"C > (1198) follows", "C>1198")
R("B43", "0.92", "STAND", r"at R ≥ (0\.92)", r"R\ge0.92")
R("B43", "8π", "STAND", r"R\*²Λ = (8π)", r"\Lambda=8\pi")
R("B43", "4", "STAND", r"The rational (4) in Gρ_Λ = 4a₀²", r"G\rho_\Lambda=4a_0^2")
# ---------------------------------------------------------------- B44-B46 what decides
R("B44", "1.000", "STAND", r"B predicts γ̂ = (1\.000);", r"\hat\gamma=1.000")
R("B44", "1.161", "STAND", r"floor is (1\.161) \(alt 1\.192\)", "is 1.161")
R("B44", "1.192", "STAND", r"floor is 1\.161 \(alt (1\.192)\)", "alt 1.192")
R("B44", "1.084", "STAND", r"γ̂ ≥ (1\.084) kills B", r"\ge1.084")
R("B44", "1.077", "STAND", r"γ̂ ≤ (1\.077) kills the bare law", r"\le1.077")
R("B44", "0.02", "STAND", r"frozen σ_sys = (0\.02)", r"\sigma_{\rm sys}=0.02")
R("B44", "8.1", "STAND", r"the cap is (8\.1)σ", r"8.1\sigma")
R("B44", "4,300", "STAND", r"about (4,300) pairs", "4,300 pairs")
R("B44", "30,000", "STAND", r"out of ~(30,000) expected", "30,000 expected")
R("B44", "1.063–1.127", "STAND", r"\((1\.063–1\.127) over footings", "1.063--1.127")
R("B44", "2.3–3.7", "STAND", r"P2-merge vs ownership: (2\.3–3\.7)σ;", r"2.3--3.7\sigma")
R("B45", "1.2–1.4", "STAND", r"lower by (1\.2–1\.4) dex", "1.2--1.4 dex")
R("B46", "2.5", "STAND", r"systematic floor \(ultra-faints (2\.5)σ", r"near 2.5\sigma")
R("B46", "0.28", "R244", r"P\(H2 \| truth b\) = (0\.28)\*\*", "above 0.28")


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


def run(mode=None):
    tex_text = open(TEX, encoding="utf-8").read()
    blocks = tex_blocks(tex_text)
    mi = mutate_index()
    results, used = [], set()
    for i, (b, value, f, rx, tex) in enumerate(ROWS):
        used.add(b)
        m = re.search(rx, source(f), re.M)
        got = nm(m.group(1)) if m else None
        exp = nm(value)
        label = f"[{b}] {f}: {value}"
        lit = norm_tex(tex if tex is not None else default_tex(value))
        if i == mi and mode == "value":
            exp = exp.replace("0.79", "0.78")
            label += "  (MUTATED expected value)"
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
    print(f"\n{n - bad if bad <= n else 0} of {n} quoted values match their committed sources and their tex blocks")
    if mode:
        print("MUTATE run: %s" % ("FAILED as required (exit 1)" if bad else "DID NOT FAIL -- the audit is not sensitive"))
    sys.exit(1 if bad else 0)
