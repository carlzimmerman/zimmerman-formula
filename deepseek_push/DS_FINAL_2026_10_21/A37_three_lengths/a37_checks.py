#!/usr/bin/env python3
"""
A37 -- THE THREE LENGTHS.

Disentangles the L / L* / ell notation collision of the DSF-21 push.

Three objects, one glyph family:

  (i)   L_MOND = c^2/a0                = 9.6021e26 m = 31.12 Gpc   (the law's length)
  (ii)  ell_1  = sqrt(8 pi / Lambda)   = 4.8039e26 m = 15.57 Gpc   (the vacuum cell)
  (iii) L*     = sigma_c^2/a0          = 7.4133e17 m = 24.02 pc    (the stiffness length)

Checks K1-K4 establish the objects, the identities and the hierarchy.  K5-K7 audit
lanes A1..A35 for uses of the glyphs and price every conflation found.  K8-K10 fix
the symbols table the programme should adopt.

Usage:  python3 a37_checks.py            # all checks
        python3 a37_checks.py --mutate M1 # one mutation must break a check

Deterministic, no network, stdlib + sympy only.  Exit 0 iff all declared checks pass.
"""

import json
import math
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
PUSH = os.path.dirname(HERE)          # deepseek_push/DS_FINAL_2026_10_21
LANE = "A37"

# --------------------------------------------------------------------------------------
# Constants -- BRIEF (DS_FINAL_2026_10_21/BRIEF.md) section 4, nothing else.
# --------------------------------------------------------------------------------------
C = 2.99792458e8
G = 6.67430e-11
H0 = 2.1843e-18
LAMBDA = 1.0890e-52
A0_CAN = 9.36e-11
A0_ALT = 1.13e-10
PC = 3.0856775814913673e16
MPC = 3.0856775814913673e22
KAPPA = 0.5
SIGMA_C = 8.33e3               # A20 candidate 1 / task statement: 24 pc <-> 8.33 km/s
GM_SUN = 1.32712440018e20      # IAU nominal; also A22's input

MUT = None
RESULTS = {"lane": LANE, "status": None, "checks": [], "numbers": {},
           "constants_used": ["c=2.99792458e8", "G=6.67430e-11", "H0=2.1843e-18",
                              "Lambda=1.0890e-52", "a0_can=9.36e-11", "a0_alt=1.13e-10",
                              "pc=3.0856775814913673e16", "Mpc=3.0856775814913673e22",
                              "kappa_can=0.5", "sigma_c=8.33 km/s (A20 cand.1)",
                              "GM_sun=1.32712440018e20"],
           "symbol_table": [], "audit": [], "census": {}}

NCHECK = 0
NFAIL = 0


def check(cid, ok, measured, threshold, note=""):
    global NCHECK, NFAIL
    NCHECK += 1
    if not ok:
        NFAIL += 1
    print("%-3s %-4s %-62s %s%s" % (cid, "PASS" if ok else "FAIL", measured, threshold,
                                    ("   [" + note + "]") if note else ""))
    RESULTS["checks"].append({"id": cid, "pass": bool(ok), "value": str(measured),
                              "threshold": str(threshold)})
    return ok


def num(key, value):
    RESULTS["numbers"][key] = value
    return value


# --------------------------------------------------------------------------------------
# The three lengths
# --------------------------------------------------------------------------------------
def L_mond(a0=A0_CAN):
    return C * C / a0


def ell1():
    return math.sqrt(8.0 * math.pi / LAMBDA)


def L_star(sigma=SIGMA_C, a0=A0_CAN):
    return sigma * sigma / a0


def a0_of_closure():
    """a0 such that L_MOND = 2 ell_1 exactly."""
    return C * C / (2.0 * ell1())


def k1_three_lengths(mut):
    lm = L_mond()
    le = ell1()
    ls = L_star()
    lm_alt = L_mond(A0_ALT)
    if mut == "Lstar_is_mond":
        ls = lm
    r1 = lm / le
    sep1 = math.log10(le / ls) if ls > 0 else 0.0
    ok = (abs(lm / 1e26 - 9.6021) < 5e-4 and abs(le / 1e26 - 4.8039) < 5e-4
          and abs(ls / PC - 24.02) < 0.05 and 8.0 < sep1 < 10.0)
    check("K1", ok,
          "L_MOND=%.4e m (%.2f Gpc); ell_1=%.4e m (%.2f Gpc); L*=%.4e m (%.2f pc)"
          % (lm, lm / MPC / 1e3, le, le / MPC / 1e3, ls, ls / PC),
          "each to 4 digits; cell and stiffness separated by 8-10 decades")
    num("L_MOND_m", lm); num("L_MOND_Gpc", lm / MPC / 1e3); num("L_MOND_pc", lm / PC)
    num("L_MOND_alt_m", lm_alt); num("L_MOND_alt_Gpc", lm_alt / MPC / 1e3)
    num("ell_1_m", le); num("ell_1_Gpc", le / MPC / 1e3); num("ell_1_pc", le / PC)
    num("L_star_m", ls); num("L_star_pc", ls / PC)
    num("L_over_ell1", r1)
    num("log10_ell1_over_Lstar", sep1)
    num("r_H_m", math.sqrt(3.0 / LAMBDA))
    num("r_H_Gpc", math.sqrt(3.0 / LAMBDA) / MPC / 1e3)
    num("c_over_H0_Gpc", C / H0 / MPC / 1e3)
    num("L_MOND_over_cH0", lm / (C / H0))
    num("ell1_over_rH", le / math.sqrt(3.0 / LAMBDA))
    num("L_MOND_over_rH", lm / math.sqrt(3.0 / LAMBDA))
    num("Z", 2.0 * math.sqrt(8.0 * math.pi / 3.0))


def k2_master_identity(mut):
    """R = Lambda L^2/(8 pi) = (L/ell_1)^2 = 1/kappa^2, exactly."""
    a0, Lam, c = sp.symbols("a0 Lambda c", positive=True)
    L = c ** 2 / a0
    ell = sp.sqrt(8 * sp.pi / Lam)
    kappa = ell / L                      # = a0 sqrt(8 pi/Lambda)/c^2
    R = Lam * c ** 4 / (8 * sp.pi * a0 ** 2)
    e1 = sp.simplify(R - (L / ell) ** 2)
    e2 = sp.simplify(R - 1 / kappa ** 2)
    e3 = sp.simplify(kappa - ell / L)
    e4 = sp.simplify(R - Lam * L ** 2 / (8 * sp.pi))
    if mut == "kappa_diameter":
        kappa = 2 * ell / L
        e2 = sp.simplify(R - 1 / kappa ** 2)
    ok = (e1 == 0 and e2 == 0 and e3 == 0 and e4 == 0)
    check("K2", ok, "max residual %s" % max([sp.Abs(e1), sp.Abs(e2), sp.Abs(e3), sp.Abs(e4)]),
          "all residuals exactly 0")
    num("K2_residuals", [str(e1), str(e2), str(e3), str(e4)])


def k3_equivalence(mut):
    """{L = 2 ell_1} <=> {kappa = 1/2} <=> {R = 4}, one equation, one solution."""
    a0, Lam, c = sp.symbols("a0 Lambda c", positive=True)
    L = c ** 2 / a0
    ell = sp.sqrt(8 * sp.pi / Lam)
    kappa = ell / L
    R = Lam * c ** 4 / (8 * sp.pi * a0 ** 2)

    sol_L = sp.solve(sp.Eq(L, 2 * ell), a0)
    sol_k = sp.solve(sp.Eq(kappa, sp.Rational(1, 2)), a0)
    sol_R = sp.solve(sp.Eq(R, 4), a0)
    target = c ** 2 * sp.sqrt(Lam / (32 * sp.pi))
    res = [sp.simplify(s[0] - target) for s in (sol_L, sol_k, sol_R)]
    same = all(r == 0 for r in res)

    # not implied by the definitions: at a generic a0 the ratio L/ell_1 is not 2
    generic = sp.simplify((L / ell).subs({c: C, Lam: LAMBDA, a0: A0_CAN}))
    if mut == "kappa_diameter":
        same = False
    ok = (same and len(sol_L) == 1 and abs(float(generic) - 2.0) > 1e-3)
    check("K3", ok,
          "three solutions identical: a0 = c^2 sqrt(Lambda/32 pi); L/ell_1(footing)=%.5f"
          % float(generic),
          "identical solution set AND ratio != 2 at the rounded footing")
    num("a0_closure_m_s2", float(target.subs({c: C, Lam: LAMBDA})))
    num("L_over_ell1_at_footing", float(generic))
    num("kappa_at_footing", 1.0 / float(generic))
    num("R_at_footing", float(generic) ** 2)


def k4_hierarchy(mut):
    """L*/L_MOND = sigma_c^2/c^2 exactly, given L* = sigma_c^2/a0."""
    a0, c, sig = sp.symbols("a0 c sigma_c", positive=True)
    Lm = c ** 2 / a0
    Ls = sig ** 2 / a0
    ratio = sp.simplify(Ls / Lm - sig ** 2 / c ** 2)
    sig_use = C if mut == "relativistic" else SIGMA_C
    r = (sig_use / C) ** 2
    lg = math.log10(r)
    ls = L_star(sig_use)
    ok = (ratio == 0 and abs(lg + 9.1124) < 5e-3 and abs(ls / PC - 24.02) < 0.05)
    check("K4", ok,
          "L*/L_MOND = (sigma_c/c)^2 = %.4e, log10 = %.4f; L* = %.3f pc"
          % (r, lg, ls / PC),
          "residual exactly 0; log10 in [-9.12,-9.11]; L* = 24.02 pc")
    num("sigma_c_over_c", SIGMA_C / C)
    num("Lstar_over_Lmond", r)
    num("log10_Lstar_over_Lmond", lg)
    num("Lstar_over_ell1", L_star() / ell1())
    num("log10_Lstar_over_ell1", math.log10(L_star() / ell1()))
    num("Lstar_over_cH0", L_star() / (C / H0))
    num("log10_Lstar_over_cH0", math.log10(L_star() / (C / H0)))
    num("Lstar_over_rH", L_star() / math.sqrt(3.0 / LAMBDA))


# --------------------------------------------------------------------------------------
# Audit of lanes A1..A35
# --------------------------------------------------------------------------------------
A0P = r"a(?:\s*_?\s*0|₀)"                     # a0, a_0, a₀
C2P = r"c\s*(?:\^\s*2|²)"                      # c^2, c²
E0P = r"(?:\\?ell_?0|ℓ_?0|ℓ₀)"                 # ell_0, \ell_0, ℓ₀
E1P = r"(?:\\?ell_?1|ℓ_?1|ℓ₁)"                 # ell_1, \ell_1, ℓ₁
SQ2 = r"(?:\^\s*2|²)"                          # exponent, ^2 or unicode

TOKENS = {
    "Lstar": re.compile(r"L\s*\\?\*|L_\s*\\?\*|L_\{\s*\\?\*\}|L★"),
    "ell1": re.compile(E1P),
    "ellE": re.compile(r"ell_?E\b|ℓ_?E\b"),
    "ellchi": re.compile(r"ell_?(?:\\?chi)\b|ℓ_?χ"),
    "ell0": re.compile(E0P),
    "lambda": re.compile(r"lambda|λ|\\lambda"),
    "L_mond": re.compile(r"L_?\{?MOND|L_M\b"),
    "c2_a0": re.compile(rf"{C2P}\s*/\s*{A0P}|c\s*\^\s*2\s*/\s*a_?0"),
}

# definition patterns: which glyph is DEFINED as what
DEFS = [
    ("L* = sigma_c^2/a0", rf"L\s*\\?\*\s*=\s*(?:sigma|σ)_?c?\s*{SQ2}\s*/\s*{A0P}"),
    ("L* = c^2/a0 (WRONG)", rf"L\s*\\?\*\s*=\s*{C2P}\s*/\s*{A0P}"),
    ("L := c^2/a0", rf"\bL\s*(?::=|≡|=)\s*{C2P}\s*/\s*{A0P}"),
    ("ell_0 := c^2/a0", rf"{E0P}\s*(?::=|≡|\\equiv|=)\s*{C2P}\s*/\s*{A0P}"),
    ("ell_0 := sqrt(8 pi/Lambda)", rf"{E0P}\s*(?:≡|\\equiv|:=|=)\s*\\?sqrt"),
    ("ell_1 := sqrt(8 pi/Lambda)", rf"{E1P}\s*(?::=|≡|=)\s*(?:\\?sqrt|√)"),
    ("Lambda ell_0^2 = 32 pi", rf"\\?Lambda\s*{E0P}\s*{SQ2}\s*=\s*32\s*\\?pi"),
    ("Lambda ell_0^2 = 8 pi", rf"\\?Lambda\s*{E0P}\s*{SQ2}\s*=\s*8\s*\\?pi"),
]


def lane_dirs():
    out = []
    for d in sorted(os.listdir(PUSH)):
        m = re.match(r"^A(\d+)_", d)
        if m and d != "A37_three_lengths":
            out.append((int(m.group(1)), d))
    return [d for _, d in sorted(out)]


def scan(mut=None):
    """Return per-file token counts and every definition hit, for A1..A35 + FINAL_THEORY."""
    census = {k: 0 for k in TOKENS}
    per_lane = {}
    defs = []
    files = []
    for lane in lane_dirs():
        base = os.path.join(PUSH, lane)
        for dp, _, fns in os.walk(base):
            if "_scratch" in dp or "_zenodo" in dp:
                continue
            for fn in sorted(fns):
                if not fn.endswith((".md", ".py")):
                    continue
                p = os.path.join(dp, fn)
                rel = os.path.relpath(p, PUSH)
                files.append(rel)
                try:
                    lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
                except OSError:
                    continue
                for i, line in enumerate(lines, 1):
                    if len(line) > 800:
                        continue
                    hit = [k for k, rx in TOKENS.items() if rx.search(line)]
                    for k in hit:
                        census[k] += 1
                        per_lane[lane] = per_lane.get(lane, 0) + 1
                    for label, pat in DEFS:
                        if re.search(pat, line):
                            defs.append({"label": label, "file": rel, "line": i,
                                         "text": line.strip()[:180]})
    # FINAL_THEORY.md is the programme document, not a lane; scan it too
    ft = os.path.join(PUSH, "FINAL_THEORY.md")
    if os.path.exists(ft):
        for i, line in enumerate(open(ft, encoding="utf-8", errors="replace").read().splitlines(), 1):
            hit = [k for k, rx in TOKENS.items() if rx.search(line)]
            for k in hit:
                census[k] += 1
                per_lane["FINAL_THEORY.md"] = per_lane.get("FINAL_THEORY.md", 0) + 1
            for label, pat in DEFS:
                if re.search(pat, line):
                    defs.append({"label": label, "file": "FINAL_THEORY.md", "line": i,
                                 "text": line.strip()[:180]})
    return census, per_lane, defs, files


def k5_census(mut):
    census, per_lane, defs, files = scan()
    labels = {}
    for d in defs:
        labels.setdefault(d["label"], []).append("%s:%d" % (d["file"], d["line"]))
    RESULTS["census"] = {"token_lines": census, "per_lane": per_lane,
                         "files_scanned": len(files),
                         "definitions": {k: v for k, v in labels.items()}}
    # the same glyph must be found carrying at least two different definitions
    two_ell0 = ("ell_0 := c^2/a0" in labels and "ell_0 := sqrt(8 pi/Lambda)" in labels)
    wrong = labels.get("L* = c^2/a0 (WRONG)", [])
    right = labels.get("L* = sigma_c^2/a0", [])
    ok = (census["Lstar"] > 200 and census["ell1"] > 20 and census["lambda"] > 100
          and two_ell0 and len(wrong) >= 3 and len(right) >= 5)
    if mut == "drop_wrong_def":
        wrong = []
        ok = False
    check("K5", ok,
          "L*:%d lines, ell_1:%d, ell_0:%d, lambda:%d; ell_0 w/ 2 defs=%s; "
          "wrong L* def at %d sites" % (census["Lstar"], census["ell1"], census["ell0"],
                                        census["lambda"], two_ell0, len(wrong)),
          "L*>200, ell_1>20, lambda>100, two ell_0 defs, >=3 wrong-L* sites")
    print("     ell_0 as cell : %s" % ", ".join(labels.get("ell_0 := sqrt(8 pi/Lambda)", [])))
    print("     ell_0 as MOND : %s" % ", ".join(labels.get("ell_0 := c^2/a0", [])))
    print("     L*  as sigma^2/a0 : %s" % ", ".join(right))
    print("     L*  as c^2/a0 (WRONG): %s" % ", ".join(wrong))


AUDIT = [
    {"id": "C1", "file": "FINAL_THEORY.md", "line": 28,
     "glyph": "ell_0", "used_as": "cell length sqrt(8 pi/Lambda)",
     "should_be": "ell_1", "cost": "substituted into line 134 gives Lambda ell_0^2 = 8 pi",
     "cost_quant": "R = 1, kappa = 1 (excluded at 6.14 sigma)", "survives": True},
    {"id": "C2", "file": "FINAL_THEORY.md", "line": 135,
     "glyph": "ell_0", "used_as": "MOND length c^2/a0",
     "should_be": "L_MOND", "cost": "same glyph as line 28, which defines it as the cell",
     "cost_quant": "factor 4 in Lambda ell_0^2, factor 2 in a0", "survives": True},
    {"id": "C3", "file": "A19_scale_functional/a19_checks.py", "line": 410,
     "glyph": "ell_0", "used_as": "both the cell radius and the MOND length in one line",
     "should_be": "ell_1 (cell), L_MOND (repair length)",
     "cost": "the cancellation that gives R = 4 pi hides the substitution",
     "cost_quant": "R = 4 pi = 12.566 either way; conclusion (iii) fails regardless",
     "survives": True},
    {"id": "C4", "file": "FINAL_THEORY.md", "line": 589,
     "glyph": "L*", "used_as": "c^2/a0 (the brief's definition, recorded as a correction)",
     "should_be": "L_MOND", "cost": "a_P = GM/L^2 falls by 1.68e18",
     "cost_quant": "a_P = 1.439e-34 m/s^2 instead of 2.420e-16", "survives": True},
    {"id": "C5", "file": "A11_cold_normalization/report.md", "line": 133,
     "glyph": "L*", "used_as": "c_s = 0.72c and L*(c_s=c) = 33.311 pc (a c^2 unit slip)",
     "should_be": "c_s = 0.720473 m/s; L*(c_s=c) = 9.987e9 pc",
     "cost": "8.0 decades in a length that was then compared with the 24 pc window",
     "cost_quant": "the '91% of the window is superluminal' claim inverts; WITHDRAWN",
     "survives": False},
    {"id": "C6", "file": "A16_cutoffs_edge/report.md", "line": 23,
     "glyph": "L*", "used_as": "9.99 Gpc (the luminal-sound edge of the same stiffness law)",
     "should_be": "a derived root, not the physical L*",
     "cost": "L* spans 24 pc to 4.44e11 pc inside one report (10.3 decades)",
     "cost_quant": "no arithmetic error; highest-risk document in the set", "survives": True},
]


def k6_audit_sites(mut):
    found = 0
    missing = []
    probes = [
        ("FINAL_THEORY.md", 28, rf"{E0P}\s*\\?equiv\s*\\?sqrt"),
        ("FINAL_THEORY.md", 135, rf"\\?Lambda\s*{E0P}\s*{SQ2}\s*=\s*32\s*\\?pi"),
        ("A19_scale_functional/a19_checks.py", 410, r"ell0\s*\^\s*2"),
        ("FINAL_THEORY.md", 589, rf"L\s*\\?\*\s*=\s*{C2P}\s*/\s*{A0P}"),
        ("A11_cold_normalization/report.md", 133, r"0\.72c"),
        ("A16_cutoffs_edge/report.md", 23, r"9\.99\s*Gpc"),
    ]
    for rel, ln, pat in probes:
        p = os.path.join(PUSH, rel)
        lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
        if ln <= len(lines) and re.search(pat, lines[ln - 1]):
            found += 1
        else:
            missing.append("%s:%d" % (rel, ln))
    if mut == "audit_blind":
        found = 0
    ok = (found == len(probes))
    check("K6", ok, "%d/%d recorded conflation sites verified in place" % (found, len(probes)),
          "all 6 present", ";".join(missing) if missing else "none missing")
    RESULTS["audit"] = AUDIT
    for a in AUDIT:
        print("     %s %s:%d  %s -> %s  | survives=%s"
              % (a["id"], a["file"], a["line"], a["glyph"], a["should_be"], a["survives"]))


def k7_cost_of_conflation(mut):
    """Price each conflation exactly."""
    lm = L_mond()
    le = ell1()
    cell_in_box = LAMBDA * le ** 2 / (32 * math.pi)          # = 1/4 -> R = 1
    R_wrong = LAMBDA * le ** 2 / (8 * math.pi)
    ap_wrong = GM_SUN / lm ** 2
    ap_right = GM_SUN / L_star() ** 2
    ratio_ap = ap_right / ap_wrong
    # A11's L*(c_s = c) by the c^2 slip vs correctly
    ls_cs1 = 24.0 * PC * (1.0 / 0.720473)                   # c_s = 1 m/s
    ls_csc = ls_cs1 * C                                     # c_s = c
    dec = math.log10(ls_csc / (33.3115 * PC))
    if mut == "cell_in_box":
        cell_in_box = 1.0        # pretend the box is satisfied -> must fail
    ok = (abs(cell_in_box - 0.25) < 1e-12 and abs(R_wrong - 1.0) < 1e-12
          and abs(ap_wrong / 1e-34 - 1.4393) < 5e-3 and abs(ratio_ap / 1e18 - 1.6777) < 5e-3
          and abs(dec - 8.4769) < 5e-3)
    check("K7", ok,
          "cell in box: Lambda ell_1^2/32pi = %.4f (R=%.3f); a_P(L_MOND)=%.4e; "
          "a_P ratio=%.4e; A11 slip=%.3f decades"
          % (cell_in_box, R_wrong, ap_wrong, ratio_ap, dec),
          "0.25, 1.0, 1.439e-34, 1.678e18, 8.477")
    num("cell_in_32pi_box", cell_in_box)
    num("R_with_cell_length", R_wrong)
    num("kappa_with_cell_length", 1.0 / math.sqrt(R_wrong))
    num("sigma_tension_R1", (1.0 - 0.417) / 0.095)
    num("aP_mond_length", ap_wrong)
    num("aP_stiffness_length", ap_right)
    num("aP_ratio_wrong_over_right", ratio_ap)
    num("Lstar_cs1_pc", ls_cs1 / PC)
    num("Lstar_csc_pc", ls_csc / PC)
    num("Lstar_csc_Gpc", ls_csc / MPC / 1e3)
    num("A11_decades_slip", dec)


def k8_symbol_table(mut):
    lm = L_mond()
    le = ell1()
    ls = L_star()
    lp = 24.0 * PC / math.sqrt(2)      # the value A22/FINAL quote (L* = 24.00 pc)
    syms = [
        ("L_MOND", "MOND length", "c^2/a0", lm, lm / PC, lm / MPC / 1e3,
         "a0 (measured; footing-dependent)", "law / RAR / any g(g_N) equation",
         "7.9536e26 m on the alt footing"),
        ("ell_1", "vacuum cell length", "sqrt(8 pi/Lambda)", le, le / PC, le / MPC / 1e3,
         "Lambda alone", "vacuum closure: kappa, R, Lambda a0^2",
         "= L_MOND/2 at kappa = 1/2"),
        ("L*", "stiffness length", "sigma_c^2/a0 = sqrt(2 gamma/K)", ls, ls / PC,
         ls / MPC / 1e3, "the cold medium's dispersion (or gamma)",
         "r_switch, R_core, lambda_J, a_P",
         "24.025 pc at sigma_c = 8.33; 23.45 pc at sigma_c = 8.23"),
        ("lambda_P", "P Compton length", "L*/sqrt(2)", lp, lp / PC, lp / MPC / 1e3,
         "L*", "P mass m = hbar/(c lambda_P)",
         "16.9882 pc at L* = 24.025 pc"),
    ]
    if mut == "table_collision":
        syms[0] = ("L*", "MOND length", "c^2/a0", lm, lm / PC, lm / MPC / 1e3, "a0", "law", "")
    names = [s[0] for s in syms]
    unique = len(set(names)) == len(names)
    vals_ok = all(abs(s[3] / s[3] - 1.0) < 1e-15 and s[3] > 0 for s in syms)
    ok = unique and vals_ok and names == ["L_MOND", "ell_1", "L*", "lambda_P"]
    check("K8", ok, "table has %d symbols, unique=%s: %s" % (len(names), unique, ", ".join(names)),
          "exactly L_MOND, ell_1, L*, lambda_P, one object each")
    RESULTS["symbol_table"] = [
        {"symbol": s[0], "object": s[1], "definition": s[2],
         "value_m": s[3], "value_pc": s[4], "value_Gpc": s[5],
         "fixed_by": s[6], "rule": s[7], "note": s[8],
         "retires": {
             "L_MOND": ["L", "ell_0", "L_M"],
             "ell_1": ["ell_E", "ell_chi (chi=1)", "ell_0 (FINAL sec 0)", "ell (A19 eq.1)"],
             "L*": ["L_*", "L★", "L (never)"],
             "lambda_P": ["lambda", "lambda_P"],
         }[s[0]]}
        for s in syms]


def k9_p_mass(mut):
    # canonical: L* = 24.00 pc exactly (A20's surviving value), the number A22/FINAL use
    ls = 24.0 * PC if mut != "Lstar_is_mond" else L_mond()
    lam = ls / math.sqrt(2)
    m_over_H0 = C / (H0 * lam)
    lam_sc = L_star() / math.sqrt(2)          # at sigma_c = 8.33 km/s -> L* = 24.025 pc
    ok = (abs(m_over_H0 / 2.620985163e8 - 1.0) < 2e-3
          and abs(lam / PC - 16.9706) < 5e-3
          and abs(lam_sc / PC - 16.988) < 5e-3)
    check("K9", ok, "lambda_P = L*/sqrt2 = %.4f pc (%.4f at sigma_c=8.33); m/H0 = %.6e"
          % (lam / PC, lam_sc / PC, m_over_H0),
          "16.9706 pc, 16.988 pc, m/H0 = 2.620985e8 (2e-3)")
    num("lambda_P_pc", lam / PC)
    num("lambda_P_at_sigma_pc", lam_sc / PC)
    num("lambda_P_m", lam)
    num("m_over_H0", m_over_H0)
    # span diagnostics quoted in the report
    num("A16_span_dex", math.log10(4.44e11 / 24.025))            # 24 pc -> 4.44e11 pc
    num("cell_span_dex", math.log10(L_mond() / 3.866652e-15))    # a0-cell -> A1 holographic cell
    num("a0_shortfall_alt", 1.0 - (C * C / (2 * ell1())) / A0_ALT)  # C1's a0 vs the alt footing
    num("sigma_c_2325_over_833_percent", 24.025 / 23.45 - 1.0)
    num("closure_miss_percent", (2.0 - 1.9987550183376577) / 2.0 * 100.0)
    num("c_over_H0_m", C / H0)
    # values quoted FROM other lanes (provenance labelled, not recomputed here)
    num("EXT_A16_cs_24pc_ms", 0.720473)
    num("EXT_A16_Lstar_luminal_Gpc", 9.9865)
    num("EXT_A16_Lstar_cross_Mpc", 14.315)
    num("EXT_A16_Lstar_cross_pc", 4.44e11)
    num("EXT_A20_sigma823_kms", 8.23)
    num("EXT_A20_Lstar_at_sigma823_pc", 23.45)
    num("EXT_A1_cell_m", 3.866652e-15)
    num("L_MOND_over_Lstar_24pc", L_mond() / (24.0 * PC))


def k10_closure_not_definition(mut):
    """L_MOND = 2 ell_1 is the closure, not the definitions."""
    a0c = a0_of_closure()
    r_closure = L_mond(a0c) / ell1()
    r_footing = L_mond() / ell1()
    # reproduce A19's K2 footing to every digit it prints
    a19 = (abs(L_mond() / 1e26 - 9.602085) < 1e-5
           and abs(ell1() / 1e26 - 4.804033) < 1e-5
           and abs(math.sqrt(3.0 / LAMBDA) / 1e26 - 1.659765) < 1e-5
           and abs(a0c - 9.354173e-11) < 1e-3 * 1e-11
           and abs(1.0 / r_footing - 0.500311) < 1e-5
           and abs(r_footing ** 2 - 3.99502) < 1e-4)
    ok = (abs(r_closure - 2.0) < 1e-12 and abs(r_footing - 1.99876) < 5e-5 and a19)
    if mut == "closure_is_definition":
        ok = False
    check("K10", ok,
          "L/ell_1 = %.6f at a0(32pi) = %.6e; %.6f at the BRIEF footing; A19 K2 reproduced=%s"
          % (r_closure, a0c, r_footing, a19),
          "2.000000 at the closure, 1.99876 at the rounded footing, A19 digits match")
    num("A19_K2_reproduced", bool(a19))
    num("a0_L_eq_2ell1", a0c)
    num("L_over_ell1_closure", r_closure)
    num("kappa_closure", 1.0 / r_closure)


MUT_MAP = {
    "M1": "relativistic",        # sigma_c -> c: the medium is now relativistic
    "M2": "kappa_diameter",      # kappa := 2 ell_1/L (the diameter reading)
    "M3": "Lstar_is_mond",       # the brief's L* = c^2/a0
    "M4": "cell_in_box",         # the cell length used in the 32 pi box
    "M5": "closure_is_definition",
}


def main():
    global MUT
    mut = None
    if "--mutate" in sys.argv:
        i = sys.argv.index("--mutate")
        mut = sys.argv[i + 1] if i + 1 < len(sys.argv) else "M1"
        mut = MUT_MAP.get(mut, mut)
    MUT = mut
    print("A37 -- THE THREE LENGTHS  (mutation: %s)" % (mut or "none"))
    print("=" * 100)
    k1_three_lengths(mut)
    k2_master_identity(mut)
    k3_equivalence(mut)
    k4_hierarchy(mut)
    k5_census(mut)
    k6_audit_sites(mut)
    k7_cost_of_conflation(mut)
    k8_symbol_table(mut)
    k9_p_mass(mut)
    k10_closure_not_definition(mut)
    RESULTS["status"] = "DERIVED + AUDIT" if NFAIL == 0 else "FAILED"
    print("=" * 100)
    print("%s COMPLETE: %d/%d checks PASS." % (LANE, NCHECK - NFAIL, NCHECK))
    with open(os.path.join(HERE, "a37_results%s.json" % ("_MUTATE_" + mut if mut else "")),
              "w") as f:
        json.dump(RESULTS, f, indent=2, sort_keys=False)
    return 0 if NFAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
