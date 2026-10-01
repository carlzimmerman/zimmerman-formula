#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PAPER38 audit: every number the note quotes is re-read from a COMMITTED file (git HEAD) and checked twice.

For each audited value the script checks that
  (1) the value appears verbatim in its committed source (a regex with one capture group, run over the file as committed at HEAD,
      read with `git show HEAD:<path>`, never the working tree), and
  (2) the value is actually printed in the .tex block that carries its `% AUDIT: Bnn` tag (the block = the non-comment lines since
      the previous tag).
Exit 0 only if every row matches.  Reports "N of N".

Usage:   python3 PAPER38_audit.py               # main run
         python3 PAPER38_audit.py --mutate      # alters ONE expected value (0.64 -> 0.65, block B32); must exit 1
         python3 PAPER38_audit.py --mutate-tex  # alters ONE tex literal in memory (same row); must exit 1
         python3 PAPER38_audit.py -v            # print every row
Environment: PAPER38_REPO (repo root; default = two levels above this file).
"""
import os, re, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("PAPER38_REPO") or os.path.abspath(os.path.join(HERE, "..", ".."))
TEX = os.path.join(HERE, "PAPER38_a0z_calibration_wall_2026.tex")
CFG = "campaign_fresh_gravity/"
SRC = {
    "STAND": CFG + "STANDING_2026-09-29.md",
    "STAND28": CFG + "STANDING_2026-09-28.md",
    "LED": CFG + "LEDGER.md",
    "R213": CFG + "CFG213_dysmalpy_two_sided/README.md",
    "R214": CFG + "CFG214_noema3d_outer/README.md",
    "R215": CFG + "CFG215_decomposition_timeline/README.md",
    "R216": CFG + "CFG216_rc100_within_sample/README.md",
    "R217": CFG + "CFG217_rc100_attack/README.md",
    "R218": CFG + "CFG218_signal_vs_systematic/README.md",
    "R219": CFG + "CFG219_z35_preflight/README.md",
    "R220": CFG + "CFG220_cristal_outer_independent/README.md",
    "R221": CFG + "CFG221_z35_decision_rule/README.md",
    "R222": CFG + "CFG222_lcdm_proxy/README.md",
    "R223": CFG + "CFG223_a0_over_cosmic_time/README.md",
    "O223L": CFG + "CFG223_a0_over_cosmic_time/cfg223_lever.out",
    "R224": CFG + "CFG224_gas_calibration/README.md",
    "R224B": CFG + "CFG224_gas_calibration/README_B.md",
    "R227": CFG + "CFG227_rar_z2_5/README.md",
    "R228": CFG + "CFG228_alma_cubes/README.md",
    "O228P": CFG + "CFG228_alma_cubes/cfg228_preflight.out",
    "R229": CFG + "CFG229_class_m_gold/README.md",
    "O229P": CFG + "CFG229_class_m_gold/cfg229_preflight.out",
    "R238": CFG + "CFG238_gas_calibration_referee/README.md",
    "R255": CFG + "CFG255_lensing_rar_zsplit/README.md",
    "O255A": CFG + "CFG255_lensing_rar_zsplit/cfg255_stageA.out",
    "O255B": CFG + "CFG255_lensing_rar_zsplit/cfg255_stageB.out",
    "GAS": "data_assembly/GAS_ANCHOR_SCOPING_2026-09-30.md",
    "LENS": "real_research/reviews/lensing_rar/A0Z_LENSING_ZBIN_2026.md",
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
R("B01", "2.2", "R213", r"about ×(2\.2) at z ≈ 1\.4", r"\times2.2")
R("B01", "8", "R213", r"and about ×(8) at z ≈ 5", r"\times8")
R("B01", "1.1 to 4.4", "R223", r"these discs sit at g_bar/a₀ = (1\.1 to 4\.4)", "1.1 to 4.4")
R("B01", "−2.5 to −4.8", "R223", r"d log₁₀ s\\\*/d\(baryon dex\) = (−2\.5 to −4\.8)", "-2.5 to -4.8")
R("B01", "0.05", "R223", r"a (0\.05) dex error in D is a factor", "0.05 dex error")
R("B01", "1.5 to 1.8", "R223", r"is a factor (1\.5 to 1\.8) in a₀", "1.5 to 1.8")
R("B01", "0.2–0.7", "STAND", r"prescription bracket \(~(0\.2–0\.7) dex at z ≈ 2\.2\)", r"{\sim}0.2--0.7")
R("B01", "2.2", "STAND", r"prescription bracket \(~0\.2–0\.7 dex at z ≈ (2\.2)\)", r"z\approx2.2")
R("B01", "0.10", "STAND", r"to the (0\.10) dex that a decisive a₀\(z\) test needs", "reaches 0.10")
R("B01", "0.64", "GAS", r"rms about the paper's relation from (0\.64) to 0\.55 dex", "scatters 0.64")
R("B01", "0.2", "GAS", r"[Tt]he claimed (0\.2) dex scatter is still not reproduced", "the 0.2 dex it states")
R("B01", "0.14", "R255", r"\*\*Δχ²_pred = (0\.14) \(canonical\)", "power 0.14")
R("B01", "9", "R255", r"against the (9) required", "against the 9 required")
R("B01", "δ/2", "R255", r"moves the amplitude by (δ/2)", r"\delta/2")
R("B01", "0.10", "R228", r"band were both ≤ (0\.10) dex", r"\le0.10")
R("B01", "2 December 2026", "STAND28", r"released (2 December 2026)")
# ---------------------------------------------------------------- B02 footings
R("B02", "9.3603e-11", "R228", r"canonical (9\.3603e-11) and alt 1\.1312e-10 m/s²", r"9.3603\times10^{-11}")
R("B02", "1.1312e-10", "R228", r"canonical 9\.3603e-11 and alt (1\.1312e-10) m/s²", r"1.1312\times10^{-10}")
R("B02", "1/1.209", "R223", r"the alt footing scales s\\\* by (1/1\.209)", "1/1.209")
# ---------------------------------------------------------------- B03 three readings, the proxy
R("B03", "1.23 / 1.77 / 2.16", "R222", r"F = (1\.23 / 1\.77 / 2\.16) at z = 1 / 2 / 2\.5", "F=1.23, 1.77 and 2.16")
R("B03", "+0.33", "R222", r"\((\+0\.33) dex at 2\.5\)", "+0.33")
R("B03", "4.52", "R222", r"(4\.52) at z = 4\.5", "4.52 at z=4.5")
R("B03", "6.20", "R222", r"(6\.20) at z = 5\.5", "6.20 at z=5.5")
# ---------------------------------------------------------------- B04-B09 signal table
R("B04", "0.20", "R255", r"median z (0\.20) against 0\.40 \(late\)", r"0.20\to0.40")
R("B04", "0.40", "R255", r"median z 0\.20 against (0\.40) \(late\)", r"0.20\to0.40")
R("B04", "+0.018", "R255", r"amplitude change of \*\*(\+0\.018) dex\*\*", "+0.018")
R("B04", "+0.001", "R255", r"the flat law predicts (\+0\.001)", "flat +0.001")
R("B05", "2.2", "R213", r"about ×(2\.2) at z ≈ 1\.4", r"\times2.2")
R("B06", "0.61–2.52", "R216", r"100 massive discs, z (0\.61–2\.52)", "0.61--2.52")
R("B06", "0.000", "R216", r"\| flat \| (0\.000) \| −0\.060 \|", "0.000 if flat")
R("B06", "+0.073", "R216", r"\| rival \| \*\*(\+0\.073)\*\* \| 0\.000 \|", "+0.073 if the rival")
R("B07", "3.4", "R223", r"\(the rival, (3\.4) at z = 2\.3", "3.4 at z=2.3")
R("B07", "0.48", "R223", r"a factor-3 law difference \((0\.48) dex, H\(z\) against flat at z ≈ 2\)", "a factor-3 law difference (0.48 dex) at z\\approx2")
R("B08", "8.69", "R223", r"the H\(z\) expectations \((8\.69) and 8\.84\)", "8.69 and 8.84")
R("B08", "8.84", "R223", r"the H\(z\) expectations \(8\.69 and (8\.84)\)", "8.69 and 8.84")
R("B08", "0.288", "R218", r"\| 9 \| 5\.23 \| \*\*(0\.288)\*\* \|", "0.288 (CRISTAL)")
R("B08", "0.287", "R228", r"Pooled ALPINE6: noise-free signal of H\(z\) against FLAT (0\.287)", "0.287 (ALPINE6)")
R("B08", "0.94", "R224", r"the law separation is (0\.94) dex", "0.94 dex")
R("B09", "4.8", "R229", r"The seven sit at g_bar/a₀ = (4\.8) \(ALESS 122\.1\)", "4.8 to 157")
R("B09", "157", "R229", r"151 to (157) \(ALPAKA 22, 15\)", "4.8 to 157")
R("B09", "0.005 to 0.09", "R229", r"differ by (0\.005 to 0\.09) dex per galaxy", "0.005 to 0.09")
# ---------------------------------------------------------------- B10
R("B10", "0.29", "R218", r"strongest signal\*\* \((0\.29) dex", "0.29 dex")
R("B10", "0.498", "R228", r"\*\*joint outer-band systematic (0\.498)\*\*", "0.498 dex")
# ---------------------------------------------------------------- B11 implied a0
R("B11", "2.2 to 3.8", "R223", r"RC100's 95% intervals are a factor (2\.2 to 3\.8) wide", "2.2 to 3.8")
R("B11", "±0.15", "R223", r"a (±0\.15) dex baryon shift moves s", r"\pm0.15")
R("B11", "0.45 to 4.04", "R223", r"moves s\\\* from (0\.45 to 4\.04) \(quartile 1\)", "0.45 to 4.04")
R("B11", "±0.30", "R223", r"(±0\.30) dex removes it at every point", r"\pm0.30")
# ---------------------------------------------------------------- B12 lever
R("B12", "1.1 to 4.4", "R223", r"these discs sit at g_bar/a₀ = (1\.1 to 4\.4)", "1.1 to 4.4")
R("B12", "0.13 to 0.28", "R223", r"local slope (0\.13 to 0\.28) against 0\.5", "0.13 to 0.28")
R("B12", "0.5", "R223", r"local slope 0\.13 to 0\.28 against (0\.5) in the deep regime", "against 0.5")
R("B12", "1.5 to 1.8", "R223", r"is a factor (1\.5 to 1\.8) in a₀", "1.5 to 1.8")
R("B12", "−2.5 to −4.8", "R223", r"d log₁₀ s\\\*/d\(baryon dex\) = (−2\.5 to −4\.8)", "-2.5 to -4.8")
R("B12", "-2.48", "O223L", r"CR R_out ind\s+6\s+1\.09\s+0\.283\s+(-2\.48)", "-2.48")
R("B12", "-4.83", "O223L", r"RC100 corr Q4\s+27\s+2\.12\s+0\.221\s+(-4\.83)", "-4.83")
R("B12", "0.48", "R223", r"\((0\.48) dex, H\(z\) against flat at z ≈ 2\)", "0.48 dex")
R("B12", "0.05 to 0.10", "R223", r"known to about (0\.05 to 0\.10) dex", "0.05 to 0.10")
R("B12", "2σ", "R223", r"at (2σ), the shared baryon", r"2\sigma")
# ---------------------------------------------------------------- B13 other levers
R("B13", "−1.8", "R228", r"λ = d log₁₀ s\\\*/d\(baryon dex\) = (−1\.8) at the measured pooled root", r"\lambda=-1.8")
R("B13", "−3.3", "R228", r"\((−3\.3) at the nominal s\\\* = 1 in the pre-flight\)", "-3.3 at the nominal")
R("B13", "0.18 to 0.33", "R228", r"moves log₁₀ s\\\* by (0\.18 to 0\.33) dex", "0.18 to 0.33")
R("B13", "0.66", "R228", r"against the (0\.66) dex between the FLAT and PROXY", "0.66")
R("B13", "0.87", "R228", r"and the (0\.87) dex between FLAT and H\(z\)", "0.87")
R("B13", "−2.0", "R229", r"Kernel lever d log₁₀ s\\\*/d\(baryon dex\) = (−2\.0)\*\*", r"\lambda=-2.0")
R("B13", "4.8", "R229", r"nearly flat at y = (4\.8)", "g_{\\rm bar}/a_0=4.8")
R("B13", "−56 to −70", "R229", r"the pre-flight lever at the nominal g_bar is (−56 to −70)", "-56 to -70")
R("B13", "2.8 to 3.5", "R229", r"move log₁₀ a₀ by (2\.8 to 3\.5)", "2.8 to 3.5")
R("B13", "600 to 3,000", "R229", r"\(a factor (600 to 3,000)\)", "600 to 3,000")
# ---------------------------------------------------------------- B14 deep regime
R("B14", "δ/2", "R255", r"moves the amplitude by (δ/2)", r"\delta/2")
# ---------------------------------------------------------------- B15 descriptive counts
R("B15", "7 of the 8", "R223", r"interval of (7 of the 8) figure points", "7 of the 8")
R("B15", "0.065", "R223", r"sits \*\*(0\.065) dex below the interval\*\*", "0.065")
R("B15", "7 / 8 / 8", "R223", r"flat (7 / 8 / 8); ΛCDM proxy", "flat 7/8/8")
R("B15", "5 / 7 / 7", "R223", r"ΛCDM proxy (5 / 7 / 7); H\(z\)", "proxy 5/7/7")
R("B15", "4 / 5 / 7", "R223", r"H\(z\) (4 / 5 / 7); a₀", "4/5/7")
R("B15", "10%", "R223", r"\((10%) of resamples have no root\)", r"10\%")
# ---------------------------------------------------------------- B16-B24 the sample table
R("B16", "0.61–2.52", "R216", r"100 massive discs, z (0\.61–2\.52)", "0.61--2.52")
R("B16", "100", "R216", r"All (100) rows are analysed", "& 100 &")
R("B16", "0.15–0.25", "STAND", r"a differential baryon-mass systematic of about (0\.15–0\.25) dex over z 0\.6–2\.5", "0.15--0.25")
R("B16", "0.6–2.5", "STAND", r"of about 0\.15–0\.25 dex over z (0\.6–2\.5)", "0.6--2.5")
R("B16", "measures the differential baryon calibration, not a₀(z)", "STAND", r"RC100 (measures the differential baryon calibration, not a₀\(z\))", "measures the differential baryon calibration, not a_0(z)")
R("B17", "10", "R213", r"NOEMA3D, (10) galaxies, measured CO gas", "& 10 &")
R("B17", "Both laws are CONSISTENT in every cell, on both mass routes", "R213", r"\*\*(Both laws are CONSISTENT in every cell, on both mass routes)\.\*\*", "both laws CONSISTENT in every cell, on both mass routes")
R("B18", "1.1-1.6", "LED", r"NOEMA3D OUTER-radius test \(z (1\.1-1\.6),", "1.1--1.6")
R("B18", "1 of 10", "R214", r"\*\*Only (1 of 10) galaxies passes the frozen 5% gate", "1 of 10")
R("B18", "5%", "R214", r"passes the frozen (5%) gate", r"5\% gate")
R("B19", "4.4 to 5.7", "R219", r"z (4\.4 to 5\.7)\) from the tables on disk", "4.4--5.7")
R("B19", "12", "R213", r"ALMA-CRISTAL, (12) disks", "12 / 6")
R("B19", "1 dex", "R213", r"Gaussian prior (1 dex) wide", "1-dex prior")
R("B19", "+0.07", "R220", r"The class changes at (\+0\.07) dex", "+0.07")
R("B20", "0.3–5.7", "R215", r"four samples, z ≈ (0\.3–5\.7)", "0.3--5.7")
R("B20", "+0.512", "R215", r"MUSE-DARK (\+0\.512), RC41", "+0.512")
R("B21", "2.0 to 4.4", "R227", r"S1 is at (2\.0 to 4\.4)", "2.0--4.4")
R("B21", "4.4 to 5.7", "R227", r"CRISTAL discs lie at z (4\.4 to 5\.7)", "4.4--5.7")
R("B21", "7 of the 9", "R227", r"(7 of the 9) have g_obs below g_bar", "7 of the 9")
R("B22", "4.2 to 5.5", "R227", r"the ALMA cubes \(z (4\.2 to 5\.5)\) in CFG228", "4.2--5.5")
R("B22", "±0.671", "R228", r"±0\.213 \(inner\) and (±0\.671) dex \(outer", r"\pm0.671")
R("B22", "−0.467", "R228", r"moves the ALPINE6 median δ_FLAT from (−0\.467) \(α = 0\)", "-0.467")
R("B22", "+0.193", "R228", r"to (\+0\.193) \(α = 6\.71, the primary\)", "+0.193")
R("B23", "2.024", "R229", r"\| ALESS 122\.1 \| (2\.024) \|", "2.024--2.935")
R("B23", "2.935", "R229", r"\| ALPAKA 22 \(Gal3\) \| (2\.935) \|", "2.024--2.935")
R("B23", "0.028", "R229", r"Pooled: signal (0\.028), statistical SD 0\.108", "0.028")
R("B23", "0.108", "R229", r"Pooled: signal 0\.028, statistical SD (0\.108)", "0.108")
R("B23", "0.028", "O229P", r"ALL7\s+7\s+0\.108\s+(0\.028) \|", "0.028")
R("B23", "6 of 7", "R229", r"H14 \((6 of 7) NO ROOT\)", "6 of 7")
R("B23", "8.82", "R229", r"s\\\* = (8\.82), a₀ = 8\.25e-10", "8.82")
R("B24", "0.20", "R255", r"median z (0\.20) against 0\.40", "0.20/0.40")
R("B24", "0.40", "R255", r"median z 0\.20 against (0\.40)", "0.20/0.40")
R("B24", "181,477", "R255", r"over (181,477) KiDS-bright lenses", "181,477")
R("B24", "0.14", "R255", r"\*\*Δχ²_pred = (0\.14) \(canonical\)", "power 0.14")
R("B24", "9", "R255", r"against the (9) required", "against 9")
# ---------------------------------------------------------------- B25 reading the table
R("B25", "−0.075", "STAND", r"exact at a differential baryon-mass calibration of (−0\.075) dex", "-0.075")
R("B25", "−0.25", "STAND", r"and the rival at (−0\.25) dex", "at -0.25")
R("B25", "0.18", "STAND", r"The two sit about (0\.18) dex apart", "about 0.18")
R("B25", "±0.06", "STAND", r"known to about (±0\.06) dex, on top of the statistics", r"\pm0.06")
R("B25", "−0.251", "R217", r"\| V1 gas fraction fixed with z \| −0\.148 \| \*\*(−0\.251)\*\*", "-0.251")
R("B25", "−0.211", "R217", r"\| V4 0\.18 μ \(α_CO 0\.8\) \| −0\.129 \| \*\*(−0\.211)\*\*", "-0.211")
R("B25", "+0.106 [−0.138, +0.343]", "R220", r"flat \*\*(\+0\.106 \[−0\.138, \+0\.343\]) CONSISTENT\*\*", "+0.106 [-0.138,+0.343]")
R("B25", "−0.203 [−0.477, +0.029]", "R220", r"rival \*\*(−0\.203 \[−0\.477, \+0\.029\]) CONSISTENT\*\*", "-0.203 [-0.477,+0.029]")
R("B25", "0.35 and 0.47", "R220", r"CRISTAL-11 and -19 are (0\.35 and 0\.47) dex below", "0.35 and 0.47")
R("B25", "Two of seven", "STAND", r"\*\*(Two of seven) have D < 1\*\*", "two of seven")
R("B25", "4.33", "R228", r"ALPINE6 pooled s\\\* = (4\.33)", "s^*=4.33")
R("B25", "4.6", "R228", r"sits nearest the PROXY's (4\.6)", "proxy's 4.6")
R("B25", "4.8", "R229", r"The seven sit at g_bar/a₀ = (4\.8) \(ALESS 122\.1\)", "between 4.8")
R("B25", "157", "R229", r"151 to (157) \(ALPAKA 22, 15\)", "and 157")
R("B25", "0.005 to 0.09", "R229", r"differ by (0\.005 to 0\.09) dex per galaxy", "0.005 to 0.09")
R("B25", "2 SD", "R229", r"below (2 SD) \(0\.16\)", "below 2 SD")
R("B25", "3.7 to 17.9", "R229", r"Envelope over every band corner and variant: \*\*(3\.7 to 17\.9)\*\*", "3.7 to 17.9")
# ---------------------------------------------------------------- B26 forecast lanes
R("B26", "0.02 to 0.11", "R218", r"3σ-equivalent flat-vs-rival separation is (0\.02 to 0\.11) dex", "0.02 to 0.11")
R("B26", "0.092", "R218", r"\| MUSE-DARK \(SED \+ H₂\) \| 109 \| 0\.86 \| (0\.092) \|", "0.092")
R("B26", "0.300", "R218", r"\| \+0\.512 \| (0\.300) \|", "0.300")
R("B26", "0.25", "STAND", r"shared gas-calibration systematic \(τ = (0\.25) dex on gas", "0.25 dex")
R("B26", "0.15", "STAND", r"dex on gas, about (0\.15) on baryons\)", "about 0.15 on baryons")
R("B26", "N ≤ 20", "STAND", r"never reaches 3σ at R_e for (N ≤ 20)", r"N\le20")
R("B26", "0.2", "STAND", r"The shared gas calibration must be known to about (0\.2) dex", "about 0.2 dex")
R("B26", "0.1–0.15", "STAND", r"\(about (0\.1–0\.15) dex on the baryon mass\)", "0.1--0.15")
R("B26", "0.15", "STAND", r"gas masses calibrated to about (0\.15) dex \(half today", "to about 0.15 dex")
R("B26", "50", "STAND", r"and about (50) outer-radius discs", "about 50 outer-radius")
R("B26", "−0.067", "R222", r"slope (−0\.067) against −0\.029 and −0\.092", "-0.067")
R("B26", "−0.029", "R222", r"slope −0\.067 against (−0\.029) and −0\.092", "-0.029")
R("B26", "−0.092", "R222", r"slope −0\.067 against −0\.029 and (−0\.092)", "-0.092")
R("B26", "−0.18", "R222", r"would make it consistent (−0\.18) dex", "-0.18")
R("B26", "−0.07", "R222", r"\(flat (−0\.07), H\(z\) −0\.25\)", "-0.07")
R("B26", "−0.25", "R222", r"\(flat −0\.07, H\(z\) (−0\.25)\)", "-0.25 dex")
# ---------------------------------------------------------------- B27 outside the lane list
R("B27", "fragile and calibration-bound", "STAND", r"is now \"(fragile and calibration-bound)\"", "fragile and calibration-bound")
R("B27", "1.5", "STAND", r"KURVS, z ≈ (1\.5)\.\*\*", r"z\approx1.5")
R("B27", "the data on disk cannot say whether the fitted masses or the SED route are biased.", "STAND", r"H₂; (the data on disk cannot say whether the fitted masses or the SED route are biased\.)", "the data on disk cannot say whether the fitted masses or the SED route are biased.")
R("B27", "MUSE-DARK III's a₀ rise is not recovered on SED M★ + H₂", "STAND", r"\"(MUSE-DARK III's a₀ rise is not recovered on SED M★ \+ H₂);", r"MUSE-DARK III's a_0 rise is not recovered on SED M_\star + H_2")
# ---------------------------------------------------------------- B28 tracer agreement
R("B28", "0.038", "R224", r"SE 0\.018, \*\*K = (0\.038): below", "K=0.038")
R("B28", "78", "R224", r"\(Stripe82, (78) galaxies, CO–dust\)", "78 galaxies")
R("B28", "0.128", "R224", r"SE 0\.044, \*\*K = (0\.128): between", "K=0.128")
R("B28", "14", "R224", r"\[CI\]–dust pooled, N = (14)\)", "(14 galaxies)")
R("B28", "1.6", "R224", r"\*\*z > (1\.6): K is not estimated\.\*\*", r"z\approx1.6")
R("B28", "three", "R224", r"Only (three) galaxies carry stated multi-tracer masses", "only three galaxies")
R("B28", "0.6", "R224", r"The per-galaxy disagreements reach (0\.6) dex", "reach 0.6")
R("B28", "0.67", "R224B", r"lies \*\*(0\.67) dex below Stripe82's OLS relation", "0.67 dex below")
R("B28", "0.21", "R224B", r"and (0\.21) dex below with the slope fixed at \+1", "0.21 to 0.67")
R("B28", "2.2", "R224B", r"disagree at z ≈ (2\.2)\.\*\*", r"z\approx2.2")
# ---------------------------------------------------------------- B29 the referee
R("B29", "145 of 146", "R238", r"(145 of 146) scored lines", "145 of 146")
R("B29", "0.083 to 0.111", "R238", r"catalogue e_logMH2 is (0\.083 to 0\.111) dex per galaxy", "0.083 to 0.111")
R("B29", "Only one of eight cases has a single overlapping L_IR bin", "STAND", r"(Only one of eight cases has a single overlapping L_IR bin)", "one of eight cases has a single overlapping L_{\\rm IR} bin")
R("B29", "3 of 9", "STAND", r"With sample fixed effects, (3 of 9) slopes reach about 3σ", "3 of 9")
R("B29", "21–52%", "STAND", r"The test has (21–52%) power for a real 0\.05 dex change", r"21--52\%")
R("B29", "0.05", "STAND", r"power for a real (0\.05) dex change", "real 0.05")
R("B29", "no drift larger than about 0.08 to 0.12 dex across z = 0 to 2.5", "R238", r"\"(no drift larger than about 0\.08 to 0\.12 dex across z = 0 to 2\.5)\" is what the data say at 80% power", "no drift larger than about 0.08 to 0.12 dex across z = 0 to 2.5")
R("B29", "80%", "R238", r"is what the data say at (80%) power", r"80\% power")
R("B29", "1.09", "STAND", r"(1\.09) dex wide across 30 cells", "1.09")
R("B29", "30", "STAND", r"1\.09 dex wide across (30) cells", "30 cells")
R("B29", "+0.30", "R238", r"under (\+0\.30) dex on all tracers", "+0.30")
# ---------------------------------------------------------------- B30 standing wording
R("B30", "multi-tracer gas is the right route, but its calibration at z ≥ 1.6 is not shown to reach the ~0.1 dex a decisive a₀(z) test needs",
  "STAND", r"\"(multi-tracer gas is the right route, but its calibration at z ≥ 1\.6 is not shown to reach the ~0\.1 dex a decisive a₀\(z\) test needs);",
  r"multi-tracer gas is the right route, but its calibration at z \ge 1.6 is not shown to reach the {\sim}0.1 dex a decisive a_0(z) test needs")
R("B30", "quote the gas band as a prescription bracket (~0.2–0.7 dex at z ≈ 2.2) unless a common-mode anchor exists.",
  "STAND", r"test needs; (quote the gas band as a prescription bracket \(~0\.2–0\.7 dex at z ≈ 2\.2\) unless a common-mode anchor exists\.)",
  r"quote the gas band as a prescription bracket ({\sim}0.2--0.7 dex at z \approx 2.2) unless a common-mode anchor exists.")
# ---------------------------------------------------------------- B31 anchor bottom line
R("B31", "No public route pins the common-mode gas calibration at z >= 1.6 to 0.10 dex.", "GAS",
  r"\*\*(No public route pins the common-mode gas calibration at z >= 1\.6 to 0\.10 dex\.)\*\*",
  r"No public route pins the common-mode gas calibration at z \ge 1.6 to 0.10 dex.")
# ---------------------------------------------------------------- B32 Heintz & Watson
R("B32", "19", "GAS", r"\| (19) \(5 GRB-DLA, 14 QSO-DLA\)", "19 GRB and QSO")
R("B32", "1.962-3.376", "GAS", r"14 QSO-DLA\), z (1\.962-3\.376)", "1.962--3.376")
R("B32", "-1.13", "GAS", r"log alpha_\[CI\] = \((-1\.13)\+-0\.19\)", "-1.13")
R("B32", "1.33", "GAS", r"log\(Z/Zsun\) \+ \((1\.33)\+-0\.21\)", "+1.33")
R("B32", "0.2", "GAS", r"\"scatter (0\.2) dex\" \(paper\)", "stated scatter of 0.2")
R("B32", "0.64", "GAS", r"rms about the paper's relation from (0\.64) to 0\.55 dex", "scatter 0.64")
R("B32", "7 of 19", "STAND", r"(7 of 19) α rows do not follow", "7 of the 19")
R("B32", "0.00", "STAND", r"Three agree to (0\.00) dex", "0.00")
R("B32", "1.00", "STAND", r"off by exactly (1\.00) in the leading digit", "exactly 1.00 in the leading digit")
R("B32", "0.64 to 0.55", "STAND", r"lowers the rms about the paper's relation from (0\.64 to 0\.55) dex", "from 0.64 to 0.55")
R("B32", "0.2", "STAND", r"from 0\.64 to 0\.55 dex, not to the stated (0\.2)\.", "not to the stated 0.2")
R("B32", "Which version the authors fitted cannot be told from the paper.", "STAND", r"(Which version the authors fitted cannot be told from the paper\.)", "Which version the authors fitted cannot be told from the paper")
# ---------------------------------------------------------------- B33 other routes
R("B33", "135", "GAS", r"Milky-Way-like delta_GDR = (135)", "135")
R("B33", "1884", "GAS", r"kappa_H = (1884) kg m-2", "1884")
R("B33", "1.6e-5", "GAS", r"or X_CI = (1\.6e-5) taken from Heintz", r"1.6\times10^{-5}")
R("B33", "0.11-0.15", "GAS", r"RELATIVE scales of CO, \[CI\] and dust to (0\.11-0\.15) dex", "0.11--0.15")
R("B33", "0.14-0.18", "GAS", r"carries (0\.14-0\.18) dex calibration systematics", "0.14--0.18")
R("B33", "0.35-0.7", "GAS", r"-> (0\.35-0\.7) dex\. \*\*That is 3-7 times", "0.35--0.7")
R("B33", "3-7", "GAS", r"\*\*That is (3-7) times the 0\.10 dex target", "3 to 7 times the 0.10")
R("B33", "three", "GAS", r"Only (three) objects with CO \+ \[CI\] \+ dust", "Only three Dunne")
R("B33", "68%", "R238", r"and (68%) of the galaxies violate M\* \+ M_CO \+ M_HI <= M_dyn", r"68\%")
R("B33", "z 2 to 4", "R238", r"Amvrosiadis\+25 \((z 2 to 4);", "z 2--4")
# ---------------------------------------------------------------- B35 KiDS
R("B35", "181,477", "R255", r"over (181,477) KiDS-bright lenses", "181,477")
R("B35", "0.20 against 0.40", "R255", r"median z (0\.20 against 0\.40) \(late\)", "0.20 against 0.40")
R("B35", "0.23 against 0.38", "R255", r"and (0\.23 against 0\.38) \(early\)", "0.23 against 0.38")
R("B35", "+0.018", "R255", r"amplitude change of \*\*(\+0\.018) dex\*\*", "+0.018")
R("B35", "+0.001", "R255", r"the flat law predicts (\+0\.001)", "+0.001")
R("B35", "0.038", "R255", r"combined amplitude is \*\*(0\.038) dex\*\*", "is 0.038")
R("B35", "0.14", "R255", r"\*\*Δχ²_pred = (0\.14) \(canonical\)", "0.14 (canonical)")
R("B35", "0.17", "R255", r"\(canonical\) / (0\.17) \(alt\)\*\*", "0.17 (alternative)")
R("B35", "0.14", "O255A", r"canonical: (0\.14); alt: 0\.17", "0.14 (canonical)")
R("B35", "0.0383", "O255A", r"sigma_A (0\.0383) \(late", "0.038")
R("B35", "19.8", "R255", r"\| zero \| (19\.8) \| 0\.14 \|", "19.8 for zero")
R("B35", "19.2", "R255", r"\| RIVAL \| (19\.2) \| 0\.16 \|", "19.2 for the rival")
R("B35", "15.1", "R255", r"\| ΛCDM proxy \| (15\.1) \| 0\.38 \|", "15.1 for")
R("B35", "p > 0.1", "STAND", r"\(all (p > 0\.1)\)", "p>0.1")
R("B35", "+0.060 ± 0.038", "R255", r"\*\*The amplitude:\*\* (\+0\.060 ± 0\.038) dex", r"+0.060\pm0.038")
R("B35", "+0.0595", "O255B", r"A_data (\+0\.0595) \+- 0\.0383", "+0.060")
R("B35", "p = 0.10", "R255", r"FLAT is still not rejected \((p = 0\.10)\)", "p=0.10")
R("B35", "byte for byte", "LED", r"reproduces every committed JSON (byte for byte)", "byte for byte")
# ---------------------------------------------------------------- B36 walled
R("B36", "δ/2", "R255", r"moves the amplitude by (δ/2)", r"\delta/2")
R("B36", "0.018", "R255", r"The rival's (0\.018) dex therefore needs", "0.018")
R("B36", "0.036", "R255", r"stable to better than (0\.036) dex", "0.036")
R("B36", "0.2 and 0.4", "R255", r"between z ≈ (0\.2 and 0\.4)", r"z\approx0.2 and 0.4")
R("B36", "0.8–1.0", "R255", r"reaching z ≈ (0\.8–1\.0)", r"z\approx0.8--1.0")
R("B36", "0.06–0.09", "R255", r"where the rival's shift is (0\.06–0\.09) dex", "0.06--0.09")
R("B36", "0.02", "R255", r"per-split amplitude error ≲ (0\.02) dex", r"\lesssim0.02")
R("B36", "0.05", "R255", r"demonstrated below about (0\.05) dex", "below about 0.05")
R("B36", "z = 0.5", "R255", r"with stellar masses beyond (z = 0\.5)", "z=0.5")
# ---------------------------------------------------------------- B37 the prior lane
R("B37", "1.309 ± 0.210", "LENS", r"ratio a0\(high\)/a0\(low\) = \*\*(1\.309 ± 0\.210)\*\* \(stat\)", r"1.309\pm0.210")
R("B37", "0.2357", "LENS", r"\| low  \| 0\.10–0\.308  \| (0\.2357) \|", "0.2357")
R("B37", "0.3723", "LENS", r"\| high \| 0\.308–0\.50  \| (0\.3723) \|", "0.3723")
R("B37", "1.083", "LENS", r"rising √ρ_total = E\(z\)\s+\| \+0\.580\s+\| (1\.083)", "1.083")
R("B37", "1.000", "LENS", r"constant w=−1\s+\| \+0\.000\s+\| (1\.000)", "1.000 for a constant")
R("B37", "≥2σ", "LENS", r"\*\*nothing is excluded at (≥2σ)\.\*\*", r"\ge2\sigma")
R("B37", "0.465", "R255", r"differ by (0\.465) dex in mean log M_gal", "0.465")
# ---------------------------------------------------------------- B38 the requirement
R("B38", "0.10", "R228", r"band were both ≤ (0\.10) dex", r"\le0.10")
R("B38", "0.277", "O228P", r"ALPINE6  d = 0\.100: signal (0\.277), SD 0\.084, S 0\.078 -> POSSIBLE", "signal 0.277")
R("B38", "0.078", "O228P", r"ALPINE6  d = 0\.100: signal 0\.277, SD 0\.084, S (0\.078) -> POSSIBLE", "S_{\\max}=0.078")
R("B38", "0.084", "R228", r"S_max 0\.078 \+ 2 × SD (0\.084)\)", "2 SD =0.084")
R("B38", "0.20", "R228", r"and is not at (0\.20) dex", "at 0.20")
R("B38", "0.05 to 0.10", "R223", r"known to about (0\.05 to 0\.10) dex", "0.05 to 0.10")
R("B38", "0.02 to 0.11", "R218", r"3σ-equivalent flat-vs-rival separation is (0\.02 to 0\.11) dex", "0.02 to 0.11")
R("B38", "0.15", "STAND", r"gas masses calibrated to about (0\.15) dex \(half today", "about 0.15 dex on the gas")
R("B38", "50", "STAND", r"and about (50) outer-radius discs", "about 50 discs")
R("B38", "±0.06", "STAND", r"known to about (±0\.06) dex, on top of the statistics", r"\pm0.06")
R("B38", "0.25-dex", "STAND", r"The (0\.25-dex) mass-scale floor caps the test", "0.25-dex")
R("B38", "2.3σ", "STAND", r"caps the test at (2\.3σ) against a₀ ∝ H\(z\)", r"2.3\sigma")
R("B38", "1.3σ", "STAND", r"and (1\.3σ) against ΛCDM-native", r"1.3\sigma")
R("B38", "0.1", "STAND", r"the calibration must reach about (0\.1) dex", "reach about 0.1")
# ---------------------------------------------------------------- B39 what else
R("B39", "5°", "R228", r"inclinations known to (5°) or better", r"5^\circ or better")
R("B39", "4° to 31°", "R228", r"\(here (4° to 31°)\)", r"4^\circ to 31^\circ")
R("B39", "2 R_e", "R228", r"resolved to beyond (2 R_e)", r"2 R_e")
R("B39", "0.05", "R228", r"the intrinsic scatter below about (0\.05) dex", "below about 0.05")
R("B39", "1 to 3", "R228", r"radii at which y is (1 to 3)", "is 1 to 3")
R("B39", "11 to 20", "R229", r"\(y ≈ 3 at (11 to 20) kpc, 1\.3 to 8", "11 to 20 kpc")
R("B39", "1.3 to 8", "R229", r"at 11 to 20 kpc, (1\.3 to 8) × the stated ones", "1.3 to 8 times")
# ---------------------------------------------------------------- B40 Gaia DR4
R("B40", "2 Dec 2026", "STAND", r"\*\*Gaia DR4 wide binaries, (2 Dec 2026)\.\*\*", "2 Dec 2026")
R("B40", "1.000", "STAND", r"B predicts γ̂ = (1\.000); the bare", r"\hat\gamma=1.000")
R("B40", "1.161", "STAND", r"the bare law's floor is (1\.161) \(alt 1\.192\)", "1.161")
R("B40", "1.192", "STAND", r"floor is 1\.161 \(alt (1\.192)\)", "alt 1.192")
R("B40", "0.02", "STAND", r"frozen σ_sys = (0\.02)", r"\sigma_{\rm sys}=0.02")
R("B40", "4,300", "STAND", r"3σ needs about (4,300) pairs", "4,300 pairs")
R("B40", "2,900", "STAND", r"\(alt (2,900)\)", "alt 2,900")
R("B40", "30,000", "STAND", r"out of ~(30,000) expected", "30,000 expected")
R("B40", "1.000", "STAND", r"or Newton, which both predict (1\.000)", "both predict 1.000")
R("B40", "For B it is a survival test, never a confirmation.", "STAND", r"(For B it is a survival test, never a confirmation\.)", "for B it is a survival test, never a confirmation")
# ---------------------------------------------------------------- B41 limitations (wording carried from the lanes)
R("B41", "frozen n_σ was blind to shared calibration", "STAND", r"the (frozen n_σ was blind to shared calibration)", "its frozen one was blind to a shared offset")
R("B41", "≤ 0.10", "R228", r"band were both (≤ 0\.10) dex", r"\le0.10")
# ---------------------------------------------------------------- B42 references (identifiers as the committed files give them)
R("B42", "2609.20926", "R238", r"the (2609\.20926) flags", "2609.20926")
R("B42", "2609.21040", "R238", r"and 18 from the (2609\.21040) flags", "2609.21040")
R("B42", "2307.10412", "GAS", r"Birkin\+23, arXiv:(2307\.10412)", "2307.10412")
R("B42", "1901.06390", "GAS", r"Coogan\+19, arXiv:(1901\.06390)", "1901.06390")
R("B42", "2208.01622", "GAS", r"Dunne\+22, arXiv:(2208\.01622)", "2208.01622")
R("B42", "MNRAS 517, 962", "GAS", r"\((MNRAS 517, 962)\)", "MNRAS 517, 962")
R("B42", "2001.05770", "GAS", r"Heintz & Watson 2020, arXiv:(2001\.05770)", "2001.05770")
R("B42", "ApJL 889, L7", "GAS", r"\((ApJL 889, L7)\)", "ApJL 889, L7")
R("B42", "Nestor Shachar+2023", "R216", r"the RC100 table \((Nestor Shachar\+2023)\)", "Nestor Shachar et al.\\ 2023")
R("B42", "Dutton & Macciò 2014", "R222", r"from (Dutton & Macciò 2014)", "Dutton \\& Macci\\`o 2014")
R("B42", "Brouwer+2021", "LENS", r"validated vs (Brouwer\+2021)\)", "Brouwer et al.\\ 2021")


# ---- coverage rows added after a numeric sweep of the tex blocks
R("B13", "0.05", "R229", r"a (0\.05) dex error in the baryons would move", "a 0.05 dex baryon error")
R("B13", "y > 10", "R229", r"For the five ALPAKA discs and BX610 \((y > 10)\)", "g_{\\rm bar}/a_0>10")
R("B17", "1.4", "R213", r"\*\*z ≈ (1\.4) \(NOEMA3D, 10 galaxies", "{\\approx}1.4")
R("B21", "9", "R227", r"\| S1 Amvrosiadis \| S \| (9) \|", "9 + 6")
R("B21", "6", "R227", r"\| CRISTAL R_e, independent \| L \| (6) \|", "9 + 6")
R("B25", "z ≈ 2.5 relative to z ≈ 0.6", "STAND", r"\((z ≈ 2\.5 relative to z ≈ 0\.6)\)", "between z\\approx0.6 and 2.5")
R("B26", "z > 3.5", "STAND", r"The pooled (z > 3\.5) decision rule", "z>3.5")
R("B29", "0.2–0.7", "STAND", r"ACE's (0\.2–0\.7) dex is a bracket of prescriptions", "0.2--0.7")
R("B29", "an extrapolation", "STAND", r"The fixed-luminosity comparison is (an extrapolation)", "is an extrapolation")

R("B25", "±0.2", "R217", r"both at or beyond the frozen \"plausible\" (±0\.2) dex band", "\\pm0.2 dex plausible band")
R("B26", "13", "R218", r"\*\*About (13) discs\*\* would bring the band", "about 13 discs")
R("B26", "the limit is the gas calibration, not N", "STAND", r"\*\*This supersedes CFG218's \"about 13 discs\":\*\* (the limit is the gas calibration, not N)\.", "the limit is the gas calibration, not N")

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
        m = re.match(r"% AUDIT: (B\d\d)\s*$", line)
        if m:
            if m.group(1) in blocks:
                raise SystemExit(f"duplicate AUDIT tag {m.group(1)} in the tex")
            blocks[m.group(1)] = norm_tex("\n".join(cur))
            cur = []
        elif not line.lstrip().startswith("%"):
            cur.append(line)
    return blocks


MUTATE_KEY = ("B32", "0.64")


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
            exp = exp.replace("0.64", "0.65")
            label += "  (MUTATED expected value)"
        if i == mi and mode == "tex":
            lit = lit.replace("0.64", "0.65")
            label += "  (MUTATED tex literal)"
        src_ok = got == exp
        tex_ok = lit in blocks.get(b, "")
        results.append((label, got, src_ok, tex_ok, lit))
    orphan = sorted(set(blocks) - used)
    missing = sorted(used - set(blocks))
    return results, orphan, missing


if __name__ == "__main__":
    mode = "value" if "--mutate" in sys.argv else "tex" if "--mutate-tex" in sys.argv else None
    head = subprocess.run(["git", "-C", REPO, "rev-parse", "--short", "HEAD"], capture_output=True).stdout.decode().strip()
    print(f"PAPER38 audit against committed files at HEAD {head}" + (f"   [MUTATE: {mode}]" if mode else ""))
    results, orphan, missing = run(mode)
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
    n = len(results)
    print(f"\n{n - bad if bad <= n else 0} of {n} quoted values match their committed sources and their tex blocks")
    if mode:
        print("MUTATE run: %s" % ("FAILED as required (exit 1)" if bad else "DID NOT FAIL -- the audit is not sensitive"))
    sys.exit(1 if bad else 0)
