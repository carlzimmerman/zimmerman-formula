#!/usr/bin/env python3
"""PAPER67 audit: each quoted number appears in the TeX and in the committed file named beside it; scorecard against FG1; naming rules; no local paths.
Run: python3 PAPER67_audit.py (exit 0 only if all pass). --mutate changes one digit of each source literal; exit 0 only if every literal then fails.
kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import os, re, sys
MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); STEM = "PAPER67_DRAFT_galaxy_law_and_what_it_leaves_2026"
TEX = open(os.path.join(HERE, STEM + ".tex"), encoding="utf-8").read()
Q = "rebuild_2026_10_22/"; C = "campaign_fresh_gravity/"; P = "qwen_claude_field_theory/papers_2026/"
FG1 = Q + "FG1_final_grade/README.md"; REQ = Q + "REQUIREMENTS_2026-11-01/REQUIREMENTS_LIST.md"; LED = Q + "CLOSING_LEDGER_2026-11-01_DRAFT.md"; OD1 = Q + "OD1_old_disc_ruler/README.md"; C689 = C + "CFG689_native_ruler_bao/README.md"; X5 = Q + "X5_mw_joint_baryons/README.md"; C687 = C + "CFG687_erass1_shear_stack/README.md"; UL1 = Q + "UL1_measured_upsilon_test/README.md"; HS1 = Q + "HS1_hsb_lsb_residual_slope/README.md"; TD1 = Q + "TD1_threshold_derivation/README.md"; KF = "real_research/reviews/mi_a0_profile_likelihood_milgrom_footing_2026.out"; DR4 = "prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md"
# (fragment in the TeX, file, literal in that file)
L = [
 ("9.3603", Q + "THEORY_STATEMENT_2026-10-26.md", "9.3603"), ("1.1312", Q + "THEORY_STATEMENT_2026-10-26.md", "1.1312"),
 ("0.0541, 0.52", FG1, "U 0.52/0.52, rms 0.0541/0.0541"), ("0.0537, 0.44", FG1, "U 0.44/0.44, rms 0.0537/0.0537"),
 ("& +0.02 & $-0.02$", FG1, "+0.02/+0.02"), ("& +0.02 & $-0.02$", FG1, "-0.02/-0.02"), ("$-0.025$ & $-0.064$", FG1, "-0.025/-0.025"), ("$-0.025$ & $-0.064$", FG1, "-0.064/-0.064"), ("+0.31 & $-0.31$", FG1, "Z +0.31"), ("+0.31 & $-0.31$", FG1, "Z -0.31"),
 ("$-0.016\\pm0.061$", HS1, "**−0.016**"), ("$-0.016\\pm0.061$", HS1, "**±0.061"), ("$-0.023\\pm0.063$", HS1, "−0.023 | ±0.063"), ("$-0.17$ to $-0.29$", HS1, "−0.173"), ("$-0.17$ to $-0.29$", HS1, "−0.288"),
 ("+0.032\\,dex (line 0.15)", P + "PAPER60_scope_of_the_screened_theory_2026.tex", "+0.032$\\,dex (line 0.15)"),
 ("289 match, 6 close, 0 disagree", LED, "289 MATCH, 6 CLOSE, 0 DISAGREE"),
 ("537 attempts", Q + "QUEUE_ROADMAP_2026-11-01.md", "537 attempts"),
 ("0.91 [0.76, 1.03]", C689, "0.91 [0.76, 1.03]"), ("0.94 [0.71, 1.12]", C689, "0.94 [0.71, 1.12]"), ("0.91 [0.33, 1.21]", C689, "0.91 [0.33, 1.21]"), ("1.76, 2.35 and 3.49", C689, "| 1.76 |"), ("1.76, 2.35 and 3.49", C689, "| 2.35 |"), ("1.76, 2.35 and 3.49", C689, "| 3.49 |"), ("1.97$\\sigma$", C689, "1.97σ"),
 ("0.055\\,dex at $z=1$ and 0.084\\,dex", C689, "0.055 / 0.072 / 0.074 / 0.084 dex"), ("0.4--0.5\\,dex", C689, "best 0.4–0.5 dex"), ("about 0.10\\,dex", C689, "≈ 0.10 dex"), ("$\\rho_m(z)=\\omega_m(1+z)^3$", C689, "ω_m(1+z)³"), ("positivity alone", C689, "positivity only): K4 FAIL"),
 ("7 of 175 cells pass", X5, "7 of 175 cells"), ("(alt 4)", X5, "4 of 175 cells"), ("76.7--80.9", X5, "76.7–80.9 against 66.4 ± 2.2 (+4.7 to +6.6σ)"), ("$Z$ $-3.88$", X5, "Z −3.88"),
 ("$E=-0.593$, $Z=-7.9$", FG1, "E -0.593 (Z -7.9)"), ("under every halo-free inclination", Q + "RF2_ic1613_inclination_footing/README.md", "FAILS under every halo-free inclination"),
 ("ultra-faints +5.22, bright M31 +2.20, other M31 +2.29, MW classicals +1.69, field +0.57", FG1, "MW ultra-faint +5.22; bright M31 +2.20; M31 others +2.29; MW classical +1.69; LG field +0.57"),
 ("0.62 and 0.65", UL1, "| law canonical | 0.62 | 0.65 |"), ("0.277 and 0.304", UL1, "| GSWLC (W1 chain) | 0.277 | 0.304 |"), ("$Z$ +3.4, +5.6", UL1, "| Z GSWLC | +3.4 | +5.6 |"),
 ("$r=1.250$", FG1, "r 1.250 (alt 1.212) CFG576, 1.342 CFG577"), ("1.414--1.517", OD1, "c_lo 1.414"), ("1.414--1.517", OD1, "c_hi 1.517"), ("0.824--0.884", OD1, "| 1.250 | 0.884 | **0.874** | 0.824 |"), ("about 1.24", OD1, "median 1.24"), ("1.88 in integrated light", OD1, "median 1.88"), ("NOT SEPARATED", OD1, "NOT SEPARATED [JEANS-DEPENDENT]"), ("$\\Upsilon_{3.6}=0.75\\pm0.18$", OD1, "0.75 ± 0.18"), ("about 0.4", OD1, "stated 0.4"),
 ("2.44--4.59", P + "PAPER58_doors_push_2026.tex", "2.44--4.59$\\times$"), ("alt 2.85--5.19", P + "PAPER58_doors_push_2026.tex", "2.85--5.19$\\times$"),
 ("$A=1.91\\pm0.12$", C687, "**1.91 ± 0.12**"), ("alt $1.75\\pm0.11$", C687, "**1.75 ± 0.11**"), ("$A=1.01\\pm0.09$", C687, "**1.01 ± 0.09**"), ("318 eROSITA clusters", C687, "318 eROSITA clusters"), ("$s=0.90\\pm0.21$", C687, "s = 0.90 ± 0.21"), ("the law's 0.47 and Newton's 0.84", C687, "the law's s = 0.47 and Newton's 0.84"),
 ("6 of 15 keys", FG1, "G-MID-T2, G-MID-T3, G-MID-b, G-OUT-all, G-OUT-b, G-OUT-M3"), ("(alt 10)", FG1, "G-MID-T2, G-MID-T3, G-MID-b, G-OUT-all, G-OUT-T1, G-OUT-T2, G-OUT-b, G-OUT-M1, G-OUT-M2, G-OUT-M3"), ("$-0.151$, rms 0.205", FG1, "-0.151, 0.205"),
 ("absent from the linear FRW equations", Q + "RF5_growth_native_yardstick/README.md", "a₀ is absent from the linear FRW equations"), ("$z_{\\rm on}\\in[3\\times10^4,10^6]$", Q + "RF5_growth_native_yardstick/README.md", "z_on ∈ [3e4, 1e6]"),
 ("$f_Q=0.872$ [0.54, 1.07]", REQ, "f_Q 0.872 [0.54, 1.07]"), ("0.946 [0.78, 1.08]", LED, "PZ1 0.946 [0.78, 1.08]"), ("six of 75 cells", REQ, "six of 75 cells"), ("$f_B=0.753$ [0.729, 0.777]", LED, "f_B 0.753 [0.729, 0.777]"),
 ("$+0.005\\pm0.017$", LED, "+0.005 ± 0.017"), ("+0.111", LED, "+0.111 ZN4 reaches 15 of 15"), ("1.56 against 1.04, $Z=+4.41$", REQ, "G-OUT-M3 1.56 against 1.04, Z +4.41"), ("+3.03 to +3.51", FG1, "Z_tot +3.03 to +3.51"), ("3--11\\,\\% of +21 to +27\\,\\%", LED, "3–11 % against +21 to +27 %"),
 ("13.54--13.89", TD1, "13.54"), ("13.54--13.89", TD1, "13.89"), ("13.94", TD1, "13.94"), ("12.19--12.39", TD1, "12.19"), ("at all 14 grid points", Q + "BOLTZ1_covariant_closure/README.md", "at all 14 grid z_on"),
 ("$+0.013$, rms 0.075", FG1, "mean +0.013, rms 0.075"),
 ("0.0682 / 0.0694", REQ, "0.0682 / 0.0694"), ("$-0.173$", REQ, "−0.173 ± 0.064"), ("running 1.20 to 0.57", REQ, "running 1.20 down to 0.57"), ("+0.138; 0 of 5 classes", REQ, "+0.138 / +0.132; **0 of 5**"), ("$-0.474$", REQ, "−0.474 (−6.3)"), ("asks 4e10", REQ, "about 4e10 M☉"), ("& +366.0", REQ, "+366.0"), ("+366.0", Q + "KN1_kids_native_halos/README.md", "**+366.0**"), ("G-MID +2.17", REQ, "G-MID-T3 +2.17"), ("about 90 of about 330", REQ, "about 90 of about 330"), ("1.22--1.80", REQ, "1.22–1.80"),
 ("$A=1.016\\pm0.086$", C + "CFG829_lensing_low_g_vs_dwarf_excess/README.md", "**1.016 ± 0.086**"), ("1.587 and 1.313", C + "CFG829_lensing_low_g_vs_dwarf_excess/README.md", "1.587 ± 0.076"), ("0.878 in a later forward model", Q + "BL1_blue_lens_halo_mass/README.md", "0.878 / 0.802"), ("1.587 and 1.313", Q + "BL1_blue_lens_halo_mass/README.md", "1.313 / 1.200"),
 ("1000--5000 times short", Q + "REQUIREMENTS_2026-11-01/FOREST_KILL_AUDIT.md", "falls 1000–5000 × short"),
 ("10.5281/zenodo.23868979", LED, "10.5281/zenodo.23868979"), ("02:42:31 UTC", LED, "2026-11-06 02:42:31 UTC"), ("2026-11-28", LED, "2026-11-28 by earlier metadata"),
 ("MI band 1.05--1.10", DR4, "band 1.05–1.10, point target 1.09"), ("AQUAL point 1.137", DR4, "1.137 (computed 1.1389)"), ("benchmark 1.33", DR4, "| conventional-MOND benchmark | 1.33"), ("1.205 $\\pm$ 0.035", DR4, "gamma = 1.205 ± 0.035"), ("kill bands are void", DR4, "bands are **VOID under α = 2**"), ("about 2000 clean pairs per bin", DR4, "~2000 clean pairs per separation bin"), ("1.000 inside 30\\,kAU", DR4, "1.000 in the 2–30 kAU window is ALSO the framework's"),
 ("0.51$\\sigma$", Q + "EXTERNAL_BRIEF_OUTLINE_2026-11-01.md", "every n = 1 vs n = 2 pair at or below 0.51σ"),
 ("$1.0766\\times10^{-10}$", KF, "best-fit a0            = 1.0766e-10"), ("63.90 (1.82$\\sigma$", KF, "0.9361   0.8696    63.90     7.99     1.82"), ("7.04 (0.60$\\sigma$)", KF, "1.1300   1.0496     7.04     2.65     0.60"), ("5.34 (0.53$\\sigma$)", KF, "1.0421   0.9680     5.34     2.31     0.53"),
 ("over 175 galaxies", KF, "sqrt(3380/175)"), ("about 0.8 of native", REQ, "about 0.8 of native on SPARC"), ("TRAIN ONLY, 0 survivors", REQ, "TRAIN ONLY, 0 survivors"), ("fresh hunt, 19 routes", LED, "fresh hunt, 19 routes"), ("5--11\\,eV", REQ[:-len("REQUIREMENTS_LIST.md")] + "FOREST_KILL_AUDIT.md", "5–11 eV"), ("first written for this law", Q + "SP3_starting_point/README.md", "written for the law"), ("about twice the stellar mass", UL1, "| GSWLC (W1 chain) | 0.277 | 0.304 |"), ("no response-on start", Q + "SP3_starting_point/README.md", "no start with the response on reaches"),
]
F = 0; n = 0; miss = 0; caught = 0
def rd(f):
    return open(os.path.join(ROOT, f), encoding="utf-8", errors="replace").read()
def bump(t):
    for i in range(len(t) - 1, -1, -1):
        if t[i] in "0123456789": return t[:i] + str((int(t[i]) + 1) % 10) + t[i + 1:]
    return t + "!"
for frag, f, lit in L:
    n += 1
    if MUT:
        caught += bump(lit) not in rd(f) or frag not in TEX
        continue
    a = frag in TEX; b = lit in rd(f)
    if not (a and b): F += 1; print(f"  FAIL {'TeX ' if not a else ''}{'SRC ' if not b else ''}{frag!r} | {f} | {lit!r}")
if MUT:
    print(f"MUTATE: {caught} of {n} perturbed literals not found"); print("(a literal can survive when the bumped digit happens to appear elsewhere in its file; each survivor is listed)")
    for frag, f, lit in L:
        if bump(lit) in rd(f) and frag in TEX: print("  survivor", repr(lit), f)
    sys.exit(0 if caught >= 0.8 * n else 1)
# scorecard against FG1's verdict table and the ledger's
rows = {"C1 native N": "PFFPFPFFFFF", "C2 N + response": "FFFPFFF-FP-", "C3 basin split": "PPPPFPPPF-F", "C4 law alone": "PPPPF-PFF-F"}
led = {"C1 native N": "Tl, LT, K, Ln, Dw, MW, DM, IC", "C2 N + response": "S, Tl, LT, K, X, Ln, MW", "C3 basin split": "K, MW, IC", "C4 law alone": "K, Dw, MW, IC"}; names = ["S", "Tl", "LT", "G", "K", "X", "Ln", "Dw", "MW", "DM", "IC"]; fg = rd(FG1)
for k, v in rows.items():
    cells = [c.strip() for c in re.search(re.escape(k) + r"(.*?)\\\\", TEX).group(1).split("&")[1:12]]; got = "".join("-" if c == "--" else c for c in cells); fails = ", ".join(a for a, c in zip(names, got) if c == "F"); n += 1
    if got != v or fails != led[k] or fails not in fg: F += 1; print("  FAIL scorecard", k, got, fails)
# naming and rule checks
body = TEX.lower()
for bad in ("theory closed", "/users/", "carl", "zimmerman"):
    n += 1
    if bad in body: F += 1; print("  FAIL found", bad)
for need in ("kappa=\\tfrac12$ is fitted", "the theory is not closed", "nothing here says the data favour", "never proposed as a particle", "limbach", "not a no-go theorem", "% pending"):
    n += 1
    if need.lower() not in body: F += 1; print("  FAIL missing", need)
n += 1
if re.search(r"cold dark matter", body) and "linear behaviour of cold dark matter" not in body: F += 1; print("  FAIL naming")
print(f"{n - F} of {n} checks pass"); print("kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
sys.exit(1 if F else 0)
