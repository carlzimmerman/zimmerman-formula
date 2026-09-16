#!/usr/bin/env python3
"""L261 -- THE 2026-09-13..16 WAVES (Z/S/A/B/C/D-series, "THE LOOP IS CLOSED"), AUDITED ON THEIR OWN NUMBERS.

WHAT IS UNDER REVIEW.  Between 2026-09-13 and 09-16 the deepseek track (with atmos/hy4/glm53/qwen38 siblings)
landed ~440 commits and declared, in deepseek_push/THE_COMPLETE_THEORY.md (C09), D07_derivation_ledger.py and
WAVEBOARD.md rev 32, a complete derivation chain: "the ONE input" a0 = c^2/(Z R_dS) -> sigma^2 -> the phantom ->
the equipartition -> the deep RAR -> the BTFR -> the 12-decade line -> the temperature law -> a DERIVED particle
mass m = 5.09 +- 0.10 keV "from three independent lines" -> the 2.55-keV line and the 0.558-Mpc cut;
"180 theorems / 22 certificates"; "the loop is closed".  This lane tests the load-bearing promotions on the
tracks' own committed scripts and outputs.  It adds no physics; it asks whether the labels are earned.
Every check states the measurement and the threshold separately; a FAIL is a finding; there are no
literal-True conditions.  Where a dimensional number appears both a0 footings are carried.

PARTS
  A  the mass ladder: is the freeze epoch z* = 2.4 measured, or defined from a 5-keV anchor?
  B  the "mass-consistency triangle" (G212): are the three lines independent, are the forest windows
     intervals or lower bounds, can any of the lane's checks fail, and is 5.09 keV inside the forest bound?
  C  the Lean inventory of the enlarged file set (from L261_lean_inventory.py): what compiles, on which
     axioms, whether the 180/22 count reproduces, and what character the certified statements have
  D  the outer-envelope slope "7.7 sigma from NFW's -3": compared at the measured radii or to the asymptote?
  E  the temperature law "0.053 dex on 50 objects": the amplitude vs the scatter (B06's own ratio register)
  F  the 12-decade line at the horizon zero point: the full-sample offset, the frozen-domain tilt, and the
     post-hoc "clean trio" (Z08/G223/S09 on the record)
  G  internal consistency of the 09-16 documents: derived-vs-definition, closed-vs-not-closed, retracted
     lemmas still in the abstract, and the pre-registration files' integrity

INPUTS (all committed, all cited by path): deepseek_push/G132_cap_thermo.py, G163_cosmic_noon.py,
G168_cosmic_noon_mass.py, G212_mass_triangle.py/.out, G093_freedust.py, G184_knee_discriminator.out,
G223_results.json, Z08_results.json, S09_results.json, project_atomos/B06_*.py/.out, THE_COMPLETE_THEORY.md,
MNRAS_ABSTRACT.md, WAVEBOARD.md, hy4_push/H037_*; fable_independent_2026/L261_lean_inventory.json.
Literature (as the tracks themselves cite it in G093): Viel+2013 m_WDM > 3.3 keV (2 sigma); Irsic+2017
m_WDM > 5.3 keV (2 sigma); Villasenor+2024 / Irsic+2024 m_WDM > 5.7 keV (95% CL) -- all LOWER bounds."""
import os, re, json, math, glob, subprocess
import numpy as np
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
EV_J, CLIGHT, KB, T_CMB0 = 1.602176634e-19, 2.99792458e8, 1.380649e-23, 2.72548
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
def rd(rel):
    p = os.path.join(REPO, rel)
    return open(p, errors="replace").read() if os.path.exists(p) else None
def jl(rel):
    p = os.path.join(REPO, rel)
    return json.load(open(p)) if os.path.exists(p) else None

print("L261 -- the 2026-09-13..16 waves ('the loop is closed'), audited on their own numbers\n")

# =====================================================================================================
print("=" * 100); print("PART A -- the mass ladder: where z* = 2.4 comes from (G132 / G163 / G168 / G213)"); print("=" * 100)
g132, g163, g168 = rd("deepseek_push/G132_cap_thermo.py"), rd("deepseek_push/G163_cosmic_noon.py"), rd("deepseek_push/G168_cosmic_noon_mass.py")
m5 = re.search(r"M_5KEV\s*=\s*5000\.0\s*\*\s*EV_J", g132 or "") is not None
zdef = re.search(r"z_eq\s*=\s*T_fid\s*/\s*T_CMB0\s*-\s*1", g132 or "") is not None
mref = re.search(r"M_KEV_REF\s*=\s*5\.0", g163 or "") is not None
admits = "z* is DEFINED by" in (g168 or "")
print(f"    G132: M_5KEV literal 5000 eV -> {m5}; z_eq := T_b(m)/T_CMB0 - 1 -> {zdef};  G163: M_KEV_REF = 5.0 -> {mref}")
print(f"    G168 header: 'z* is DEFINED by T_b(m = 5 keV) = T_CMB' present -> {admits}")
# reproduce the registered z* band from the 5-keV anchor at the two sigma footings
sig = {"G081 (121.44 km/s)": 121.44e3, "registered canonical (119.21 km/s)": 119.21e3}
m_kg = 5000.0 * EV_J / CLIGHT ** 2
zs = {k: m_kg * s ** 2 / KB / T_CMB0 - 1.0 for k, s in sig.items()}
band = (2.3656, 2.4932)   # G213 Z_STAR_BAND, "G132: T_b = 9.1729-9.5205 K at m = 5 keV"
for k, z in zs.items(): print(f"    z*(m = 5 keV, sigma = {k}) = {z:.4f}   (T_b = {m_kg*sig[k]**2/KB:.4f} K)")
dev = max(abs(min(zs.values()) - band[0]), abs(max(zs.values()) - band[1]))
OUT["A"] = dict(zstar_from_5keV=zs, registered_band=band, max_dev=dev)
check("A1 the registered z* band [2.3656, 2.4932] has an origin OTHER than T_b(m = 5 keV) = T_CMB at the two sigma footings "
      "(|z*(5 keV) - band edge| > 0.01 at either edge)", dev > 0.01,
      f"max deviation {dev:.2e}: the band IS the 5-keV anchor; G168 states it ('{'z* is DEFINED by' if admits else 'absent'}'). [FAIL is the finding]")
# the "cosmic-noon window [5.0, 5.2]" = inverting the G081-footing z* at the canonical sigma
m_inv = [KB * T_CMB0 * (1 + z) / (119.21e3) ** 2 * CLIGHT ** 2 / EV_J / 1e3 for z in band]
ratio = (121.44 / 119.21) ** 2
print(f"    inverting the band at sigma = 119.21 km/s: m = [{m_inv[0]:.3f}, {m_inv[1]:.3f}] keV;  (121.44/119.21)^2 = {ratio:.4f} -> 5 x that = {5*ratio:.3f} keV")
check("A2 the cosmic-noon 'window' [5.0, 5.2] keV is wider than the two-footing identity 5 keV x [1, (121.44/119.21)^2] "
      "(upper edge differs from 5 (sigma_G081/sigma_canon)^2 by > 0.02 keV)", abs(m_inv[1] - 5 * ratio) > 0.02,
      f"upper edge {m_inv[1]:.3f} vs 5 x footing ratio {5*ratio:.3f}: the window's width is the sigma-footing mismatch, not an uncertainty. [FAIL is the finding]")

# =====================================================================================================
print("\n" + "=" * 100); print("PART B -- the mass-consistency triangle (G212): independence, intervals, checks, the forest bound"); print("=" * 100)
g212, g093, g212o = rd("deepseek_push/G212_mass_triangle.py"), rd("deepseek_push/G093_freedust.py"), rd("deepseek_push/G212_mass_triangle.out")
n_true = len(re.findall(r"check\(\s*True\s*,", g212 or ""))
n_calls = len(re.findall(r"^\s*check\(", g212 or "", re.M))
print(f"    G212: check(...) calls = {n_calls}; of these check(True, ...) = {n_true}")
check("B1 G212 contains at least one check whose first argument is a computed condition (not the literal True)",
      n_calls - n_true > 0, f"{n_true}/{n_calls} literal-True: the lane's 9/9 cannot fail. [FAIL is the finding]")
bounds = sorted(float(x) for x in re.findall(r"m_WDM\s*>\s*(\d+\.\d+)\s*keV", g093 or ""))
wb = re.search(r"W_B\s*=\s*\(\s*([\d.]+)\s*,\s*([\d.]+)\s*\)", g212 or "")
W_B = (float(wb.group(1)), float(wb.group(2))) if wb else (None, None)
print(f"    G093 forest constraints as cited by the track: m_WDM > {bounds} keV (all lower bounds);  G212 W_B = {W_B}")
check("B2 G212's forest window W_B is a two-sided interval whose upper edge is NOT one of G093's published LOWER bounds",
      W_B[1] is not None and W_B[1] not in bounds,
      f"W_B upper edge {W_B[1]} keV == the record lower bound m_WDM > {W_B[1]} keV (95% CL): a floor used as a ceiling. [FAIL is the finding]")
mo = re.search(r"JOINT:\s*m\s*=\s*([\d.]+)\s*\+-\s*([\d.]+)\s*keV", g212o or "")
m_pk, m_sg = (float(mo.group(1)), float(mo.group(2))) if mo else (5.0886, 0.0969)
z57, z53 = (max(bounds) - m_pk) / m_sg, (5.3 - m_pk) / m_sg
print(f"    G212 joint m = {m_pk} +- {m_sg} keV;  (5.7 - m)/sigma = {z57:.2f};  (5.3 - m)/sigma = {z53:.2f}")
check(f"B3 the triangle's m = {m_pk} +- {m_sg} keV sits ABOVE the record forest floor m_WDM > {max(bounds)} keV (95% CL) at >= -2 sigma",
      z57 <= 2.0, f"it sits {z57:.1f} sigma BELOW the floor ({z53:.1f} sigma below Irsic+17's 5.3); only Viel+13's 3.3 keV is satisfied. [FAIL is the finding]")
mu_b, s_b = 0.5 * (W_B[0] + W_B[1]), (W_B[1] - W_B[0]) / 4.0   # G212_mass_triangle.py:272, verbatim
p_allowed = 1 - norm.cdf((max(bounds) - mu_b) / s_b)
print(f"    G212's Gaussian for the forest leg: N({mu_b}, {s_b}) -> P(m > {max(bounds)}) = {p_allowed:.3f}")
check("B4 G212's forest likelihood puts >= 50% of its mass in the region the forest ALLOWS (m > record floor)",
      p_allowed >= 0.5, f"{100*p_allowed:.1f}% allowed / {100*(1-p_allowed):.1f}% in the excluded region: the leg is inverted. [FAIL is the finding]")
OUT["B"] = dict(literal_true=n_true, calls=n_calls, forest_lower_bounds=bounds, W_B=W_B, m=[m_pk, m_sg], z_below_57=z57, z_below_53=z53, p_allowed=p_allowed)

# =====================================================================================================
print("\n" + "=" * 100); print("PART C -- the Lean inventory (L261_lean_inventory.json): compiles, axioms, the 180/22 count, the statements"); print("=" * 100)
inv = jl("fable_independent_2026/L261_lean_inventory.json")
if inv is None:
    print("    L261_lean_inventory.json not present -- run fable_independent_2026/L261_lean_inventory.py first (~30 min)")
else:
    files = inv["files"]; tot = inv["total"]
    bad = {k: v for k, v in files.items() if v["exit"] != 0}
    print(f"    {tot['files']} files, {tot['theorems']} theorem/lemma declarations, exit-0 files {tot['files_exit0']}, "
          f"theorems on nonstandard axioms {tot['theorems_on_nonstandard_axioms']}")
    for k, v in bad.items(): print(f"      non-zero exit: {k} (exit {v['exit']}, {v['n_errors']} errors): {v['errors'][:2]}")
    check("C1 every tracked certificate in the agent tracks compiles (exit 0)", not bad,
          f"{len(bad)} file(s) fail: {list(bad)}. [FAIL is the finding]")
    q5 = files.get("qwen38_push/lean/Q005_btfr_zero_point.lean")
    check("C2 qwen38 Q005 ('Lean-certified, exit 0, zero sorry' in commit 65ac81130) exits 0",
          q5 is not None and q5["exit"] == 0, f"exit {q5['exit'] if q5 else 'n/a'}; its three #eval/decide checks evaluate to false. [FAIL is the finding]")
    ok_files = {k: v for k, v in files.items() if v["exit"] == 0}
    check("C3 among compiling files, zero theorems rest on axioms outside {propext, Classical.choice, Quot.sound}",
          sum(len(v["theorems_on_nonstandard_axioms"]) for v in ok_files.values()) == 0)
    ledger22 = ["deepseek_push/lean/" + f for f in ("C01_sqrt2_sound", "C02_environment_blind", "C04_proton_rung", "C05_doubleZ", "C06_horizon_omega",
                "C07_gauss_chain", "EQUILIBRIUM_THEORY", "G001_clockmaker_dilemma", "G002_G003_onefunction_phantom", "G007_bimetric",
                "G031_fluid_action", "G036_formal_extras", "G03G_triad", "G083_surface_density", "G090_equivalence", "G201_jump_share")] + \
               ["glm53_push/lean/" + f for f in ("G024_slab", "G039_horn_a_clean", "G039_radial_scatter", "G047_efe_cap", "G055_frozen_scalar", "G058_omega_from_a0")]
    n180 = sum(files[k + ".lean"]["theorems"] for k in ledger22 if k + ".lean" in files)
    print(f"    D07's 22 certificate files -> {n180} theorem declarations (D07 claims 180)")
    check("C4 D07's '180 theorems / 22 certificates' reproduces from the 22 named files", n180 == 180, f"{n180}")
    names = []
    for k in ledger22:
        src = rd(k + ".lean") or ""
        names += re.findall(r"^(?:theorem|lemma)\s+([\w']+)", src, re.M)
    tau = [n for n in names if re.search(r"tautolog|inverse|inversion|_defs$|reexpress", n)]
    num = [n for n in names if re.search(r"^num|interval|decimal|cross_check|numeric", n)]
    print(f"    of the {len(names)} names: {len(num)} numeric-interval checks, {len(tau)} named as inverse/identity/tautology: {tau}")
    OUT["C"] = dict(total=tot, failing=list(bad), n180=n180, numeric=num, tautology_named=tau)
    print("    the certified STATEMENTS: substitution algebra (C04 field_identity: T = mu m_p sigma^2/k_B with sigma^2 substituted), mutual inverses (C02 ladder(freeze(m)) = m;"
          "\n    C04 inversion_identity/inversion_dual), sqrt algebra (C05), decimal intervals (C08 num_*), and C06 closure_iff_zSq: Omega = 32 pi a0^2/(3 H0^2 c^2) <=> Z^2 = 32 pi/3"
          "\n    given a0 := c^2/(Z R_dS), R_dS := c/(H0 sqrt Omega) -- the rung-9 circularity of L258 part A, now as a theorem (and one theorem is named tautological_fixed_point).")

# =====================================================================================================
print("\n" + "=" * 100); print("PART D -- the outer-envelope slope -2.404 +- 0.078, '7.7 sigma from NFW's -3' (G184)"); print("=" * 100)
g184 = rd("deepseek_push/G184_knee_discriminator.out") or ""
mm = re.search(r"common weighted mean:\s*(-[\d.]+)\s*\+-\s*([\d.]+)", g184)
slope, se = (float(mm.group(1)), float(mm.group(2))) if mm else (-2.404, 0.078)
nfw = re.search(r"NFW fits at\s*\n?\s*1-2 R500 run\s*(-[\d.]+)\.\.(-[\d.]+)", g184)
nfw_lo, nfw_hi = (float(nfw.group(1)), float(nfw.group(2))) if nfw else (-2.0, -2.75)
print(f"    measured common mean {slope} +- {se};  G184's own NFW fits at 1-2 R500: {nfw_lo} .. {nfw_hi};  asymptote -3 -> {(slope+3)/se:.1f} sigma")
check("D1 the measured outer slope lies OUTSIDE the range G184 records for the committed NFW fits at the same radii (1-2 R500)",
      not (min(nfw_lo, nfw_hi) <= slope <= max(nfw_lo, nfw_hi)),
      f"{slope} is inside [{min(nfw_lo,nfw_hi)}, {max(nfw_lo,nfw_hi)}]: the 7.7 sigma is against the r >> r_s asymptote, not against NFW where it was measured. [FAIL is the finding]")
OUT["D"] = dict(slope=slope, se=se, nfw_window=[nfw_lo, nfw_hi], sigma_vs_asymptote=(slope + 3) / se)


# =====================================================================================================
print("\n" + "=" * 100); print("PART E -- the temperature law T = mu m_p sqrt(G M_b a0)/(2 k_B): amplitude vs scatter (B06 / A02)"); print("=" * 100)
b06o, b06 = rd("project_atomos/B06_txray_law.out") or "", rd("project_atomos/B06_txray_law.py") or ""
rows = {m.group(1): (float(m.group(2)), float(m.group(3))) for m in
        re.finditer(r"^\s*(X-COP|HeCS|E11|POOLED)\s+n=\s*\d+\s+median T_pred/T_obs = ([\d.]+) \(identity\) / ([\d.]+) \(/2 floor\)", b06o, re.M)}
within = re.search(r"WITHIN-SAMPLE residual \(sample mean removed, n = \d+\): pstdev ([\d.]+) / MAD ([\d.]+) dex", b06o)
for k, (ri, rf) in rows.items(): print(f"    {k:7s} median T_pred/T_obs = {ri} (identity form)  ->  T_obs/T_pred = {1/ri:.2f}  = {abs(math.log10(ri)):.2f} dex off")
print(f"    within-sample residual (each sample's own mean removed): pstdev {within.group(1) if within else '?'} / MAD {within.group(2) if within else '?'} dex  <- the quoted '0.053 dex'")
pooled = rows.get("POOLED", (None, None))[0]
check("E1 the zero-parameter law's UNNORMALIZED pooled amplitude is within 0.1 dex of the data (|log10 median T_pred/T_obs| < 0.1, n = 50)",
      pooled is not None and abs(math.log10(pooled)) < 0.1,
      f"pooled median T_pred/T_obs = {pooled} -> {abs(math.log10(pooled)):.2f} dex ({1/pooled:.1f}x under-prediction): Sanders' 1994/1999 MOND cluster residual, intact. [FAIL is the finding]")
v1 = re.search(r"V1 = dict\(\s*pass_bool=bool\((.*?)\),", b06, re.S)
cond = v1.group(1) if v1 else ""
print(f"    B06 V1 pass_bool: {' '.join(cond.split())}")
check("E2 B06's headline verdict V1 conditions on the AMPLITUDE (median ratio) and not only on scatter",
      any(w in cond for w in ("median", "r_ident", "ratio")) and "pstdev" not in cond.split("and")[0],
      "V1 tests pstdev < 0.067 and within-sample MAD < 0.067 only; the 2.1x miss cannot fail it (F_VIR = 5.664 is M500/M_b, the missing mass relabelled). [FAIL is the finding]")
OUT["E"] = dict(medians=rows, within=[within.group(1), within.group(2)] if within else None, v1_condition=" ".join(cond.split()))

# =====================================================================================================
print("\n" + "=" * 100); print("PART F -- the 12-decade line at the horizon zero point (Z08 / Z01 / S09 / S03)"); print("=" * 100)
z08, z01, s09 = rd("deepseek_push/Z08_line_zero.out") or "", rd("deepseek_push/Z01_frozen_tilt.out") or "", rd("deepseek_push/S09_one_scale.out") or ""
full = re.search(r"a0_line = ([\d.e+-]+) \+- ([\d.e+-]+) \(stat\) = ([\d.]+) x a0_DE\s+\[log10 a0/a0_DE = \+?([\d.-]+) \+- ([\d.]+) dex\]", z08)
zfull = re.search(r"a0_DE\s+9\.3619e-11\s+ratio ([\d.]+)\s+z = \+?([\d.-]+) sigma", z08)
chan = {m.group(1): float(m.group(2)) for m in re.finditer(r"^\s*(SPARC|HI|ATLAS3D|GEMS|dSph|CLU|GC)\s+n=\s*\d+\s+mean r [+\d.-]+ \+- [\d.]+\s+a0=[\d.e+-]+ \(([\d.]+) x DE\)", z08, re.M)}
print(f"    full 542, slope fixed at 1: a0_line = {full.group(3) if full else '?'} x a0_DE, log10 offset +{full.group(4) if full else '?'} +- {full.group(5) if full else '?'} dex, z = {zfull.group(2) if zfull else '?'} sigma")
print(f"    per-channel a0/a0_DE: {chan}")
check("F1 the full-sample slope-fixed zero point sits within 3 sigma of the horizon a0 (|z| < 3)",
      zfull is not None and abs(float(zfull.group(2))) < 3,
      f"z = +{zfull.group(2) if zfull else '?'} (stat); a0_line = {full.group(3) if full else '?'} x a0_DE = an {100*(float(full.group(3))-1):.0f}% amplitude error in a0. [FAIL is the finding]")
span = math.log10(max(chan.values()) / min(chan.values())) if chan else None
check("F2 the seven channels' zero points agree to within 0.5 dex (max/min a0_channel < 10^0.5)", span is not None and span < 0.5,
      f"span {span:.2f} dex: SPARC {chan.get('SPARC')}x .. clusters {chan.get('CLU')}x a0_DE (the MOND cluster deficit and the ETG/dSph offsets, on the record). [FAIL is the finding]")
fz = re.search(r"FROZEN \(z\* > 0\)\s*:\s*n =\s*(\d+)\s+slope ([\d.]+) \+- ([\d.]+)\s+\(b-1\)/se \+?([\d.-]+)", z01)
anc = re.search(r"ANCOVA\), the frozen-domain slope is b = ([\d.]+) \+- ([\d.]+)", z01)
print(f"    Z01 frozen-domain (n = {fz.group(1) if fz else '?'}) slope {fz.group(2) if fz else '?'} +- {fz.group(3) if fz else '?'} ((b-1)/se = {fz.group(4) if fz else '?'});  ANCOVA per-catalog zero points: b = {anc.group(1) if anc else '?'} +- {anc.group(2) if anc else '?'}")
check("F3 the frozen-domain line (the law's own domain, z* > 0) has slope 1 within 3 sigma", fz is not None and abs(float(fz.group(4))) < 3,
      f"(b-1)/se = +{fz.group(4) if fz else '?'}; with per-catalog zero points b = {anc.group(1) if anc else '?'}: the pooled 1.004 is a cross-channel lever arm. [FAIL is the finding]")
noa = re.search(r"WITHOUT the ATLAS3D channel \(n = (\d+)\): a0 = [\d.e+-]+ = ([\d.]+) x a0_DE", s09)
trio = re.search(r"TRIO free slope \(NOT fixed\): b = ([\d.]+) \+- ([\d.]+)", s09)
print(f"    S09: without ATLAS3D (n = {noa.group(1) if noa else '?'}) the line sits at {noa.group(2) if noa else '?'} x a0_DE;  the n = 104 trio's free slope b = {trio.group(1) if trio else '?'} +- {trio.group(2) if trio else '?'}")
check("F4 removing the ATLAS3D channel (S09's stated 56%-of-the-offset resolution) brings the line to the horizon a0 (|log10 ratio| < 0.1 dex)",
      noa is not None and abs(math.log10(float(noa.group(2)))) < 0.1,
      f"{noa.group(2) if noa else '?'} x a0_DE = {math.log10(float(noa.group(2))):.2f} dex: S09's own line 'a MIXED-CATALOG ladder artifact (the ETG/cluster/dSph ENDS)'. The z = -0.20 trio is SPARC (-3.41 sigma) cancelling HI (+0.95). [FAIL is the finding]")
OUT["F"] = dict(full=[full.group(3), full.group(4), zfull.group(2)] if full and zfull else None, channels=chan, frozen_slope=[fz.group(2), fz.group(3)] if fz else None, ancova=[anc.group(1), anc.group(2)] if anc else None, without_atlas3d=noa.group(2) if noa else None)

# =====================================================================================================
print("\n" + "=" * 100); print("PART G -- the 09-16 documents against each other, the retracted lemma, the kernel 'derivation', the pre-registration"); print("=" * 100)
cap, abst, wb = rd("deepseek_push/THE_COMPLETE_THEORY.md") or "", rd("deepseek_push/MNRAS_ABSTRACT.md") or "", rd("deepseek_push/WAVEBOARD.md") or ""
d1, d2 = "from a0 alone" in cap, "inversion of a definition" in abst
print(f"    THE_COMPLETE_THEORY: 'Omega_Lambda = 0.685 from a0 alone (G058, Lean)' -> {d1};  MNRAS_ABSTRACT: 'the +0.07% Omega_Lambda closure is the inversion of a definition' -> {d2}")
check("G1 the capstone and the abstract (same track, same day) agree on whether Omega_Lambda is derived from a0", not (d1 and d2),
      "both present: derived in one, a definition in the other (L258 part A: it is the definition). [FAIL is the finding]")
h037 = rd("hy4_push/H037_results.out") or ""
retr = re.search(r"H033 RETRACTED: Sigma = a_0/\(pi G\) = ([\d.]+) Msun/pc\^2 is WRONG by ([\d.]+)x", h037)
in_abs = re.search(r"a0/\(pi G\) = ([\d.]+) M_sun/pc\^2", abst)
print(f"    hy4 H037: '{retr.group(0) if retr else 'absent'}';  MNRAS_ABSTRACT 'What is new and owned': 'the universal surface density a0/(pi G) = {in_abs.group(1) if in_abs else '?'}'")
check("G2 the abstract's 'new and owned' universal surface density a0/(pi G) is not a lemma a sibling track retracted on SPARC (H037: wrong by 2.04x)",
      not (retr and in_abs), "retracted 09-15 (SPARC log10 Sigma = 1.91 vs 2.33), still in the abstract 09-16. [FAIL is the finding]")
cap_sig = re.search(r"Σ = ([\d.]+) M☉/pc²", cap); 
print(f"    THE_COMPLETE_THEORY Link 1: 'Σ = {cap_sig.group(1) if cap_sig else '?'} M☉/pc²' (= a0/(2 pi G));  abstract: {in_abs.group(1) if in_abs else '?'} (= a0/(pi G))")
check("G3 the capstone and the abstract quote the SAME universal surface density (ratio within 10%)",
      cap_sig is not None and in_abs is not None and abs(float(cap_sig.group(1)) / float(in_abs.group(1)) - 1) < 0.1,
      f"ratio {float(in_abs.group(1))/float(cap_sig.group(1)):.2f}: a factor 2 between two documents of the same closure. [FAIL is the finding]")
lc, nc = "the loop closes" in wb, "not closed as a theory" in cap
print(f"    WAVEBOARD rev 32 'the loop closes' -> {lc};  THE_COMPLETE_THEORY V3 'The theory is not closed as a theory' -> {nc}")
check("G4 the wave board and the capstone agree on closure", not (lc and nc), "both present. [FAIL is the finding]")
g228 = rd("deepseek_push/G228_lomax_maxent.py") or ""
n228 = len(re.findall(r"check\(\s*True\s*,|,\s*True\s*,\s*V\d|\"[^\"]*\",\s*True\s*,", g228))
calib = "CALIBRATED" in g228
g230 = rd("deepseek_push/G230_dmdg_measure.out") or ""
g230s = re.search(r"G230 COMPLETE: (\d+)/(\d+) checks PASS", g230)
print(f"    G228 ('the Lomax from max-entropy: derived, not assumed'): literal-True verdict checks = {n228}; the file says the log-moment c = 1/2 is 'CALIBRATED' -> {calib}")
print(f"    G230 (the distribution reading's own measurement): {g230s.group(0) if g230s else '?'}; V1b pooled dM/dg index +3.47 +- 0.20 vs -2 (z = +7.28), Lomax KS p = 0.000")
check("G5 G228's 'derived, not assumed' rests on computed verdict checks and does not call its exponent calibrated", n228 == 0 and not calib,
      f"{n228} literal-True verdicts; c = 1/2 (=> alpha = 2 => kappa = 1/2) 'CALIBRATED': the textbook log-moment => Lomax fact with the exponent put in by hand. [FAIL is the finding]")
check("G6 the Lomax/distribution reading passes its own shape test (G230 majority PASS)", g230s is not None and int(g230s.group(1)) * 2 > int(g230s.group(2)),
      "1/5: the track's own FAIL, correctly listed in REASSESSMENT_2026-09-16 -- H055/H060/N1 'CANDIDATE TOE PIECE' is not. [FAIL is the finding]")
try:
    gl = subprocess.run(["git", "log", "--since=2026-09-13", "--format=%h", "--", "*PREREGISTRATION_DR4*", "*_HASH.txt"], cwd=REPO, capture_output=True, text=True).stdout.split()
except Exception: gl = ["(git unavailable)"]
print(f"    commits since 2026-09-13 touching PREREGISTRATION_DR4.md or any *_HASH.txt: {gl if gl else 'none'}")
check("G7 the frozen Gaia DR4 pre-registration and its hash files were not modified by the waves", len(gl) == 0, "integrity intact")
OUT["G"] = dict(derived_vs_definition=[d1, d2], sigma_retracted_in_abstract=bool(retr and in_abs), sigma_cap_vs_abs=[cap_sig.group(1) if cap_sig else None, in_abs.group(1) if in_abs else None],
                loop_closes_vs_not_closed=[lc, nc], g228_literal_true=n228, g228_calibrated=calib, g230=g230s.group(0) if g230s else None, prereg_commits=gl)

# =====================================================================================================
print("\n" + "=" * 100); print("PART H -- the L258 (09-15) findings F1-F4 against the 09-16 documents: fixed, acknowledged, relabeled, or carried?"); print("=" * 100)
g152 = jl("deepseek_push/G152_results.json") or {}
circ = []
def _walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "CIRCULAR_ruled_out" and isinstance(v, list): circ.extend(v)
            _walk(v)
    elif isinstance(o, list):
        for x in o: _walk(x)
_walk(g152)
clo = rd("deepseek_push/THEORY_CLOSURE_2026-09-16.md") or ""
meth = rd("deepseek_push/MNRAS_METHODS.md") or ""
own_circ = any("Omega_Lambda closure" in str(c) for c in circ)
print(f"    G152 (09-16 01:04) lists as CIRCULAR_ruled_out: {[str(c)[:60] for c in circ][:4]} ...")
print(f"    THEORY_CLOSURE (05:06) 'from a0 alone' -> {'from a0 alone' in clo}; MNRAS_METHODS 'key certified identities' carries the Omega_Lambda closure -> {'from a0 alone' in meth}")
check("H1 (F1) once the track's own inventory ruled the Omega_Lambda closure CIRCULAR, no later 09-16 document re-prints it as 'from a0 alone'",
      not (own_circ and ("from a0 alone" in clo or "from a0 alone" in cap or "from a0 alone" in meth)),
      "G152 -> CIRCULAR at 01:04; THEORY_CLOSURE 05:06, THE_COMPLETE_THEORY 14:55, MNRAS_METHODS: 'from a0 alone (G058, Lean)'. RELABELED. [FAIL is the finding]")
g198 = rd("deepseek_push/G198_total_dust.py") or ""
sub = re.search(r"Omega_dust\w*\s*=\s*Omega_dm\s*-\s*Omega_eq\w*", g198)
print(f"    G198_total_dust.py: '{sub.group(0) if sub else 'absent'}'  -> the 'equilibrium + dust = 1.000 of Omega_dm' is x + (Omega_dm - x)")
check("H2 (F3) 'equilibrium + dust = 1.000 x Omega_dm' is computed from something other than Omega_dust := Omega_dm(Planck) - Omega_phantom",
      sub is None, "it is that subtraction; Planck's Omega_dm fed back (L258 A3). The 1.72 v_flat double count (L258 B3) is mentioned nowhere. CARRIED. [FAIL is the finding]")
lean_all = " ".join(rd(f) or "" for f in [os.path.relpath(x, REPO) for x in glob.glob(os.path.join(REPO, "*_push", "lean", "*.lean")) + glob.glob(os.path.join(REPO, "*_push", "*.lean")) + glob.glob(os.path.join(REPO, "deepseek_moa", "lean", "*.lean"))])
c1c2 = ("virial_rung4" in lean_all, "maxentropy_phantom" in lean_all)
g03g = rd("deepseek_push/lean/G03G_triad.lean") or ""
prem = re.search(r"sg2\s*:=\s*Real\.sqrt\s*\(G\s*\*\s*Mb\s*\*\s*a0\)\s*/\s*2", g03g) is not None
print(f"    the registered entrance certificates C1 'virial_rung4' / C2 'maxentropy_phantom' exist in any .lean -> {c1c2};  G03G sigma_virial_half DEFINES sg2 := sqrt(G Mb a0)/2 -> {prem}")
check("H3 (F2) at least one of the 'five routes' to sigma^2 = sqrt(G M_b a0)/2 is a Lean certificate that does not take sigma^2 = C/2 or rho ~ r^-2 as a hypothesis or definition",
      any(c1c2), "C1/C2 absent; G03G proves (x/2)/x = 1/2 from the definition; G084 inputs sigma^2 = C/2 and outputs gamma = 2; G091 inputs rho = A/r^2 and says it is the same statement as hydrostatic balance. RELABELED. [FAIL is the finding]")
g086 = rd("deepseek_push/G086_relativistic_face.out") or ""; g234 = rd("deepseek_push/G234_ontology_closeout.md") or ""; l243 = rd("fable_independent_2026/L243_onefunction_cassini_quadrupole.out") or ""
nofield = "ORDINARY MATTER" in g086 and "p = 0" in g086
sourced = "4πG rho_b" in g234 or "4 pi G rho_b" in g234
q2 = re.search(r"canonical (\d+\.\d+)x ceiling", l243)
print(f"    G086/S08 (PPN face): the sector is 'ORDINARY MATTER (barotropic dust: p = 0)' -> {nofield};  G234 (ontology): the phantom is the Gauss-map charge of 'div[f'(K) grad phi] = 4 pi G rho_b' -> {sourced};  L243: that mu_2 field's EFE quadrupole = {q2.group(1) if q2 else '?'}x the Cassini ceiling")
check("H4 (F4) the 09-16 lanes give ONE account of what produces the RAR: either a sourced mu_2 field (then L243's quadrupole is inherited) or no field (then GR + a prescribed halo)",
      not (nofield and sourced), f"both: 'no field force' for Cassini, 'the sourced field's charge' for the RAR -- L258 C2's splice, now inside one track; the {q2.group(1) if q2 else '6.44'}x stands. CARRIED. [FAIL is the finding]")
OUT["H"] = dict(g152_circular=[str(c)[:80] for c in circ], relabeled_from_a0_alone=["from a0 alone" in clo, "from a0 alone" in cap, "from a0 alone" in meth], g198_subtraction=sub.group(0) if sub else None, c1c2_exist=c1c2, g03g_defines_premise=prem, nofield=nofield, sourced=sourced, l243_q2=q2.group(1) if q2 else None)

# =====================================================================================================
print("\n" + "=" * 100); print("PART I -- the sibling tracks' kills vs the capstone; the boundary's factor 2; the cluster law; the registered rules"); print("=" * 100)
from scipy.optimize import brentq
h045 = rd("hy4_push/H045_results.out") or ""; e02 = rd("deepseek_push/E02_quantum_face.out") or ""
ghost = "[PASS] C1 [WRONG-SIGN GRADIENT ENERGY]" in h045 and "[PASS] C2 [NO GROUND STATE]" in h045
eff = "EFFECTIVE, not fundamental" in e02
one_scalar = "One scalar: a shift-symmetric scalar field carrying our gravity" in cap
print(f"    hy4 H045: the frozen-scalar action L = Lambda^4 f(K) has P_X = -mu_2 < 0 (wrong-sign gradient energy, no ground state) -> {ghost};  deepseek E02 (latest lane): 'The framework is EFFECTIVE, not fundamental' -> {eff};  capstone section 6: 'One scalar ... carrying our gravity' -> {one_scalar}")
check("I1 the capstone's 'one scalar field carrying our gravity' is not an action the sibling track falsified (H045 ghost) and the track's own latest lane conceded (E02)",
      not (ghost and eff and one_scalar), "all three present: the paper set presents a field theory whose action is ghost-ridden by its own record. IGNORED. [FAIL is the finding]")
g035 = rd("glm53_push/G035_results.md") or ""; g081 = rd("deepseek_push/G081_equilibrium_stability.out") or ""
kill = "must be POSTULATED" in g035 and "G035's KILL" in g081
five = "five routes" in cap
print(f"    glm53 G035 attractor test: 'The temperature must be POSTULATED' -> {'must be POSTULATED' in g035};  deepseek G081: 'G035's KILL ... stands' -> {'G035' in g081};  capstone Link 2: 'derived ... by five routes' -> {five}")
check("I2 the capstone's 'sigma^2 derived by five routes' cites or rebuts the sibling's dynamical KILL of that temperature (G035) with a committed run",
      not (kill and five and "G035" not in cap), "G035 uncited in the capstone; the rebuttal (G111 relaxation N-body) is an unrun spec. IGNORED. [FAIL is the finding]")
# the boundary's factor 2: the committed kernel g mu_2(g/2a0) = g_N at r_M (g_N = a0) vs the 'exact equipartition' M_ph(<r_M) = M_b
mu2 = lambda u: 1.0 - (1.0 + u) ** -2
x = brentq(lambda x: x * mu2(x / 2.0) - 1.0, 1.0, 10.0)
frac = x - 1.0
print(f"    at r_M (g_N = a0) the committed kernel gives g/g_N = {x:.4f} -> M_dark(<r_M)/M_b = {frac:.3f} (hy4 H037: 0.489, Sigma = a0/(2 pi G) = 106.9);  the 'Lean-certified equipartition' says M_ph(<r_M) = M_b (1.000, Sigma = a0/(pi G) = 213.7)")
check("I3 the equipartition M_ph(<r_M) = M_b (Link 4, 'exact to 2.2e-16') agrees within 10% with the dark mass the committed mu_2 kernel puts inside r_M",
      abs(frac - 1.0) < 0.1, f"{frac:.3f} vs 1.000: a factor {1/frac:.2f} at the one boundary -- the same factor as Sigma 213.7 vs 106.9 (G3) and H037's retraction (G2). [FAIL is the finding]")
fm = rd("deepseek_push/FALSIFIER_MATRIX.md") or ""; g223 = rd("deepseek_push/G223_line_scatter.out") or ""
tilt = re.search(r"FROZEN \(z\* > 0\)\s*:\s*n =\s*323\s+slope ([\d.]+) \+- ([\d.]+)[^\n]*\(b-1\)/se \+?([\d.]+)", g223)
print(f"    G223: frozen-domain slope {tilt.group(1) if tilt else '?'} +- {tilt.group(2) if tilt else '?'} ((b-1)/se = +{tilt.group(3) if tilt else '?'});  FALSIFIER_MATRIX mentions G223 -> {'G223' in fm}; 'Unexplained fires: ZERO' -> {'Unexplained fires: ZERO' in fm}")
check("I4 every registered > 3 sigma departure is entered in the falsifier matrix that reports 'zero unexplained fires' (the 5.35-sigma frozen-domain tilt)",
      tilt is not None and not (float(tilt.group(3)) > 3 and "G223" not in fm), "not entered; the matrix's 20 rows also omit the -4.4 sigma window rule, the +8.98 sigma full-sample zero point, the 7-sigma Sigma mass dependence (H033_P1), the cluster break FAIL (D036/G160) and the escalated sag (G049). [FAIL is the finding]")
h033 = jl("hy4_push/H033_P1_results.json") or {}
g237 = rd("deepseek_push/G237_selfpredicted_falsifier.md") or ""
print(f"    H033_P1 (SPARC, 171 curves): pass {h033.get('pass')} / fail {h033.get('fail')} -- Sigma measured 81 vs 213.7 Msun/pc^2 (-0.42 dex), M_b-dependence 7 sigma;  G237 registers a Sigma kill ('M_b NOT cancelling') -> {'M_b NOT cancelling' in g237};  matrix cites H033 -> {'H033' in fm}")
check("I5 the Sigma = a0/(pi G) kill G237 registers is scored against the SPARC measurement that meets it (H033_P1)", not (h033.get("fail", 0) > 0 and "M_b NOT cancelling" in g237 and "H033" not in fm),
      "registered, met, not scored. [FAIL is the finding]")
cio = [f for f in glob.glob(os.path.join(REPO, "deepseek_push", "*")) if os.path.isfile(f) and f.endswith((".md", ".out", ".py")) and "Ciocan" in (rd(os.path.relpath(f, REPO)) or "")]
l143 = rd("fable_independent_2026/L143_a0z_prediction_and_tests.out") or ""
print(f"    the one direct a0(z) measurement in the repo (MUSE, Ciocan et al.: a1 = +1.59 +- 0.105 per unit z, RISING; L143) cited in deepseek_push -> {len(cio)} files")
check("I6 the cosmic-noon freeze picture (a0 flat for z < 2.4) confronts the repo's one direct a0(z) measurement (MUSE, rising)", len(cio) > 0 or "Ciocan" not in l143,
      "uncited; L143 registers '> 3 sigma either sign kills the flat law'. IGNORED. [FAIL is the finding]")
g122 = rd("deepseek_push/G122_coherency_decomp.out") or ""; d03 = rd("deepseek_push/D03_dust_inversion.py") or ""
fit3 = re.search(r"fit \(96 bins, 3 params\): const = (-?[\d.]+), q = [^=]*= (-?[\d.]+), p = [^=]*= \+?(-?[\d.]+)", g122)
qmeas = re.search(r"Q_MEAS\s*=\s*(-?[\d.]+)", d03)
print(f"    G122: 'fit (96 bins, 3 params): const = {fit3.group(1) if fit3 else '?'}, q = {fit3.group(2) if fit3 else '?'}, p = {fit3.group(3) if fit3 else '?'}' (OLS on 12 X-COP clusters x 8 radii);  D03 inverts with Q_MEAS = {qmeas.group(1) if qmeas else '?'} (not the 'derived' -1/3)")
check("I7 the 'zero-parameter dust law' c_dust = c0 (M/8e14)^q (r/R500)^p has at least one of (c0, q, p) that is not an OLS fit to the same 12 clusters",
      not (fit3 and qmeas and abs(float(qmeas.group(1)) - float(fit3.group(2))) < 0.01), "all three fitted (G122:129); 'derived' q = -1/3 (0.52 sigma on +-0.157) never enters the law; the dust amount 'remains an INPUT (G110 P7)'. [FAIL is the finding]")
g170 = rd("deepseek_push/G170_registry.out") or ""; g203 = rd("deepseek_push/G203_hecs_commission.out") or ""
rule = "beta_win > 0.5 at >= 3 sigma (G170 rule)" in g203
zr = re.search(r"vs streaming rule 0\.5: z = (-?[\d.]+) sigma", g203)
print(f"    G170 registered the streaming rule beta(2-5 R500) > 0.5 at >= 3 sigma; G203 measured 0.434 +- 0.015: '[FAIL] C6 [streaming rule]' -> {'[FAIL] C6' in g203}, z vs 0.5 = {zr.group(1) if zr else '?'};  capstone: 'anisotropy beta 0.03 -> 0.56 measured' among the closed sectors")
check("I8 the registered anisotropy rule (beta > 0.5 at >= 3 sigma, G170) passed on the HeCS data", rule and zr is not None and float(zr.group(1)) > -3,
      f"z = {zr.group(1) if zr else '?'}: the pre-registered prediction FAILED; the '31 sigma' kills beta = 0, which nothing predicts, and 0.434 is the Hansen-Moore LCDM value, never compared. [FAIL is the finding]")
prop = rd("deepseek_push/TSZ_PROPOSAL.md") or ""; amend = rd("deepseek_push/TSZ_AMENDMENT.md") or ""; z06 = rd("deepseek_push/Z06_tsz_pull.out") or ""
w1 = re.search(r"Sample-median slope in \((−?-?[\d.]+), (−?-?[\d.]+)\)", prop); w2 = re.search(r"sample pass window is \((−?-?[\d.]+), (−?-?[\d.]+)\)", amend)
a85 = re.search(r"A85\s+map\(ACT DR6\+Planck y-map\)\s+(-[\d.]+)\s+(-[\d.]+)\s+(-?[\d.]+)\s+(\w+)", z06)
print(f"    tSZ: proposal pass window {w1.groups() if w1 else '?'} (G129, 00:30) -> amendment pass window {w2.groups() if w2 else '?'} (G177, 02:52, before the map at 11:38);  first real cluster A85: slope {a85.group(1) if a85 else '?'} vs pred {a85.group(2) if a85 else '?'} -> '{a85.group(4) if a85 else '?'}' (the framework's own branch label)")
check("I9 the tSZ pass window used for scoring is the one registered in the proposal", w1 is not None and w2 is not None and w1.groups() == w2.groups(),
      "rewritten pre-data (the old kill line -2 now inside the pass window); the 47.8 sigma is a synthetic forecast; A85 sits in the NEITHER branch at forecast errors. [FAIL is the finding]")
OUT["I"] = dict(ghost=ghost, effective_conceded=eff, one_scalar=one_scalar, g035_kill=kill, kernel_frac_at_rM=frac, tilt=tilt.groups() if tilt else None, h033=[h033.get("pass"), h033.get("fail")], ciocan_cites=len(cio), fit3=fit3.groups() if fit3 else None, q_meas=qmeas.group(1) if qmeas else None, beta_z=zr.group(1) if zr else None, tsz_windows=[w1.groups() if w1 else None, w2.groups() if w2 else None], a85=a85.groups() if a85 else None)

# =====================================================================================================
n, n_pass = len(CH), sum(CH)
print("\n" + "=" * 100)
print(f"L261 COMPLETE: {n_pass}/{n} checks PASS.  Every FAIL is a finding: the 09-13..16 waves certify algebra, define the mass they")
print("derive (5.09 keV from a 5-keV anchor, 6.3 sigma below the forest floor they cite), grade scatter where the amplitude misses (T-law 2.1x,")
print("the line 1.81x a0 at 9 sigma), compare to an asymptote, fit the 'zero-parameter' dust law, fail their own registered beta rule, rewrite")
print("the tSZ window pre-data, and carry a ghost-ridden action, a killed temperature, a retracted lemma and a factor 2 at the one boundary")
print("between their own documents.  What stands: the Lean algebra compiles (bar Q005 and the gemini38 file), the pre-registration is intact,")
print("and the honest FAILs the tracks themselves recorded (G230, G059, G035, H037, H045, S03, G203 C6, D036) are on the record.")
json.dump(dict(checks_pass=n_pass, checks=n, parts=OUT), open(os.path.join(HERE, "L261_results.json"), "w"), indent=1, default=str)
