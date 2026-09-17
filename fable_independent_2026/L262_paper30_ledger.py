#!/usr/bin/env python3
"""L262 -- THE PAPER30 LEDGER: every number quoted in PAPER30 (the verified ledger of the 2026-09-13..16 agent-swarm
campaign) re-read from the committed registers.  A FAIL here means the paper's number has drifted from the record
(or a register is missing) -- it is a consistency gate on the paper, not a physics test.  The physics verdicts live
in L258 / L260 / L261; this lane prints the tables the paper carries and checks each quoted value against its source.
Run:  python3 fable_independent_2026/L262_paper30_ledger.py"""
import os, re, json, math
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
def rd(rel):
    p = os.path.join(REPO, rel)
    return open(p, errors="replace").read() if os.path.exists(p) else ""
def jl(rel):
    p = os.path.join(REPO, rel)
    return json.load(open(p)) if os.path.exists(p) else None
def near(a, b, tol): return a is not None and b is not None and abs(float(a) - float(b)) <= tol

print("L262 -- PAPER30's numbers re-read from the committed registers\n")

# ---------------------------------------------------------------- section 2: the Lean inventory
print("== section 2: Lean inventory (L261_lean_inventory.json) ==")
inv = jl("fable_independent_2026/L261_lean_inventory.json")
if inv:
    t = inv["total"]; files = inv["files"]
    print(f"    files {t['files']}, theorems {t['theorems']}, exit-0 {t['files_exit0']}, failing {t['files_with_errors']}")
    check("2a paper: 73 files / 848 theorem declarations / 71 exit 0", t["files"] == 73 and t["theorems"] == 848 and t["files_exit0"] == 71)
    check("2b paper: the two failing files are gemini38 Unified and qwen38 Q005",
          set(t["files_with_errors"]) == {"gemini38_flash_push/UnifiedGravitationalTheoryProof.lean", "qwen38_push/lean/Q005_btfr_zero_point.lean"})
    g38 = files.get("gemini38_flash_push/UnifiedGravitationalTheoryProof.lean", {})
    check("2c paper: five gemini38 theorems on sorryAx; 16 errors", len(g38.get("theorems_on_nonstandard_axioms", {})) == 5 and g38.get("n_errors") == 16,
          f"{len(g38.get('theorems_on_nonstandard_axioms', {}))} / {g38.get('n_errors')}")
    l261 = jl("fable_independent_2026/L261_results.json") or {}
    check("2d paper: the 22 named certificate files carry 180 theorem declarations", (l261.get("parts", {}).get("C", {}) or {}).get("n180") == 180)
    lean_all = "".join(rd(os.path.relpath(p, REPO)) for p in [os.path.join(REPO, k) for k in files])
    check("2e paper: `virial_rung4` / `maxentropy_phantom` exist in no file", "virial_rung4" not in lean_all and "maxentropy_phantom" not in lean_all)
    c06 = rd("deepseek_push/lean/C06_horizon_omega.lean")
    check("2f paper: C06 contains `closure_iff_zSq` and `tautological_fixed_point`", "closure_iff_zSq" in c06 and "tautological_fixed_point" in c06)
else:
    check("2 the Lean inventory register exists", False, "run L261_lean_inventory.py")

# ---------------------------------------------------------------- section 3.1: the twelve-decade line
print("\n== section 3.1: the twelve-decade line (Z08 / Z01 / S09) ==")
z08 = rd("deepseek_push/Z08_line_zero.out"); z01 = rd("deepseek_push/Z01_frozen_tilt.out"); s09 = rd("deepseek_push/S09_one_scale.out")
full = re.search(r"= ([\d.]+) x a0_DE\s+\[log10 a0/a0_DE = \+?([\d.-]+) \+- ([\d.]+) dex\]", z08)
zf = re.search(r"a0_DE\s+9\.3619e-11\s+ratio ([\d.]+)\s+z = \+?([\d.-]+) sigma", z08)
paper_ch = {"SPARC": (35, 0.663, -3.41), "HI": (55, 1.194, 0.95), "ATLAS3D": (258, 2.020, 14.37), "GEMS": (36, 1.326, 0.78),
            "dSph": (34, 7.378, 5.00), "CLU": (12, 12.164, 42.21), "GC": (112, 1.401, 1.69)}
rows = {m.group(1): (int(m.group(2)), float(m.group(3)), float(m.group(4))) for m in
        re.finditer(r"^\s*(SPARC|HI|ATLAS3D|GEMS|dSph|CLU|GC)\s+n=\s*(\d+)\s+mean r [+\d.-]+ \+- [\d.]+\s+a0=[\d.e+-]+ \(([\d.]+) x DE\)\s+z_DE ([+\d.-]+)", z08, re.M)}
print("    channel   n   a0/a0_DE   z");
for k, v in rows.items(): print(f"    {k:8s} {v[0]:4d}   {v[1]:6.3f}   {v[2]:+6.2f}")
check("3.1a paper: slope-fixed zero point 1.814 x a0_DE, +0.2585 +- 0.0288 dex, z = +8.98",
      full and zf and near(full.group(1), 1.814, 0.001) and near(full.group(2), 0.2585, 0.0001) and near(full.group(3), 0.0288, 0.0001) and near(zf.group(2), 8.98, 0.01))
check("3.1b paper: the seven per-channel rows (n, a0/a0_DE, z) match Z08", all(k in rows and rows[k][0] == paper_ch[k][0] and near(rows[k][1], paper_ch[k][1], 0.001) and near(rows[k][2], paper_ch[k][2], 0.01) for k in paper_ch))
span = math.log10(max(v[1] for v in rows.values()) / min(v[1] for v in rows.values())) if rows else None
check("3.1c paper: the channels span 1.26 dex", span is not None and near(span, 1.26, 0.01), f"{span}")
fz = re.search(r"FROZEN \(z\* > 0\)\s*:\s*n =\s*(\d+)\s+slope ([\d.]+) \+- ([\d.]+)[^\n]*\(b-1\)/se \+?([\d.]+)", z01)
anc = re.search(r"ANCOVA\), the frozen-domain slope is b = ([\d.]+) \+- ([\d.]+)", z01)
check("3.1d paper: frozen domain n = 323, slope 1.155 +- 0.029 (+5.35 sigma); ANCOVA 1.298 +- 0.056",
      fz and anc and fz.group(1) == "323" and near(fz.group(2), 1.155, 0.001) and near(fz.group(3), 0.029, 0.001) and near(fz.group(4), 5.35, 0.01) and near(anc.group(1), 1.298, 0.001) and near(anc.group(2), 0.056, 0.001))
noa = re.search(r"WITHOUT the ATLAS3D channel \(n = (\d+)\): a0 = [\d.e+-]+ = ([\d.]+) x a0_DE", s09)
trio = re.search(r"TRIO free slope \(NOT fixed\): b = ([\d.]+) \+- ([\d.]+)", s09)
gb = re.search(r"G131_ten_decade|slope b = 1\.004", rd("deepseek_push/D07_derivation_ledger.out"))
check("3.1e paper: without ATLAS3D 1.644 x a0_DE; the n = 104 trio is SPARC -3.41 / HI +0.95", noa and near(noa.group(2), 1.644, 0.001) and "SPARC   n= 35  mean r -0.0447 +- 0.0131  a0/a0_DE = 0.663  z = -3.41" in s09 and "HI      n= 55  mean r +0.0192 +- 0.0202  a0/a0_DE = 1.194  z = +0.95" in s09)
check("3.1f paper: pooled free slope b = 1.004 +- 0.011, n = 542, rms 0.180 (D07 register)", '"n": 542, "slope": 1.004, "se": 0.0108' in rd("deepseek_push/D07_derivation_ledger.out"))

# ---------------------------------------------------------------- section 3.2: the temperature relation
print("\n== section 3.2: the cluster temperature relation (B06) ==")
b06 = rd("project_atomos/B06_txray_law.out")
med = {m.group(1): float(m.group(2)) for m in re.finditer(r"^\s*(X-COP|HeCS|E11|POOLED)\s+n=\s*\d+\s+median T_pred/T_obs = ([\d.]+) \(identity\)", b06, re.M)}
within = re.search(r"WITHIN-SAMPLE residual \(sample mean removed, n = (\d+)\): pstdev ([\d.]+) / MAD ([\d.]+) dex", b06)
for k, v in med.items(): print(f"    {k:7s} median T_pred/T_obs = {v:.3f}  -> {abs(math.log10(v)):.2f} dex")
check("3.2a paper: medians 0.560 / 0.721 / 0.433, pooled 0.475 (2.1x, 0.32 dex)",
      near(med.get("X-COP"), 0.560, 0.001) and near(med.get("HeCS"), 0.721, 0.001) and near(med.get("E11"), 0.433, 0.001) and near(med.get("POOLED"), 0.475, 0.001) and near(abs(math.log10(med.get("POOLED", 1))), 0.32, 0.01))
check("3.2b paper: within-sample MAD 0.053 dex on n = 50", within and within.group(1) == "50" and near(within.group(3), 0.0531, 0.0001))
check("3.2c paper: B06's F_VIR = 5.664 is M_dyn/M_b", re.search(r"F_VIR\s*=\s*5\.664", rd("project_atomos/B06_txray_law.py")) is not None)

# ---------------------------------------------------------------- section 3.3: the anisotropy
print("\n== section 3.3: the HeCS anisotropy (G203 / G206 / G209 / G170) ==")
g203 = rd("deepseek_push/G203_hecs_commission.out"); g206 = rd("deepseek_push/G206_wojtak_2d.out") or "".join(rd(os.path.relpath(p, REPO)) for p in __import__("glob").glob(os.path.join(REPO, "deepseek_push", "G206_*.out")))
g209 = rd("deepseek_push/G209_beta_profile.out"); g170 = rd("deepseek_push/G170_registry.out")
bw = re.search(r"beta_win\(2-5 R500\) = ([\d.]+) \+- ([\d.]+)", g203)
zr = re.search(r"vs static null 0: z = ([\d.]+) sigma; vs streaming rule 0\.5: z = (-?[\d.]+) sigma", g203)
e2 = re.search(r"inner bins \(E2, PRIMARY\): beta\(0\.5-1\) = (-?[\d.]+) \+- ([\d.]+)", g209)
check("3.3a paper: beta(2-5 R500) = 0.434 +- 0.015; 29.7 sigma from 0; -4.5 sigma from 0.5; '[FAIL] C6'",
      bw and zr and near(bw.group(1), 0.434, 0.001) and near(bw.group(2), 0.015, 0.001) and near(zr.group(1), 29.7, 0.1) and near(zr.group(2), -4.5, 0.1) and "[FAIL] C6" in g203)
check("3.3b paper: G206 2D fit 0.495; G209 E2 inner bin -0.37 +- 0.14", "beta_win(2-5 R500) = 0.495" in g206 and e2 and near(e2.group(1), -0.369, 0.001) and near(e2.group(2), 0.136, 0.001))
check("3.3c paper: the G170 rule registered 'beta(2-5 R500) > 0.5 ... >= 3 sigma'", "> 0.5" in g170 and ">= 3 sigma" in g170 and "beta" in g170)

# ---------------------------------------------------------------- section 3.4 / 3.5
print("\n== sections 3.4-3.5: the cluster residual fit (G122) and the outer slope (G184) ==")
g122 = rd("deepseek_push/G122_coherency_decomp.out"); g184 = rd("deepseek_push/G184_knee_discriminator.out")
fit3 = re.search(r"fit \(96 bins, 3 params\): const = (-?[\d.]+), q = [^=]*= (-?[\d.]+), p = [^=]*= \+?(-?[\d.]+);\s+residual rms = ([\d.]+) dex", g122)
check("3.4 paper: c0 = -0.145, q = -0.414, p = 0.990, rms 0.119 dex, 96 bins", fit3 and near(fit3.group(1), -0.145, 0.001) and near(fit3.group(2), -0.414, 0.001) and near(fit3.group(3), 0.990, 0.001) and near(fit3.group(4), 0.119, 0.001))
sl = re.search(r"common weighted mean:\s*(-[\d.]+)\s*\+-\s*([\d.]+)", g184)
check("3.5 paper: -2.404 +- 0.078; NFW in-window -2.0..-2.75; tSZ forecast -2.37 +- 0.09 among the 'instruments'",
      sl and near(sl.group(1), -2.404, 0.001) and near(sl.group(2), 0.078, 0.001) and "1-2 R500 run -2.0..-2.75" in g184 and re.search(r"-2\.37 \+- 0\.09", g184) is not None)

# ---------------------------------------------------------------- section 4: the no-go results
print("\n== section 4: the no-go results ==")
h045 = rd("hy4_push/H045_results.out")
check("4.1 H045: P_X = -mu_2 < 0; u* = 1.2238563; solar surface u/u* = 1.1959e+12; C1/C2 PASS", "P_X = -f'(K) = -mu_2(sqrt K) < 0" in h045 and "u* = 1.2238563" in h045 and "1.1959e+12" in h045 and "[PASS] C1 [WRONG-SIGN GRADIENT ENERGY]" in h045 and "[PASS] C2 [NO GROUND STATE]" in h045)
check("4.1 E02 (deepseek): 'The framework is EFFECTIVE, not fundamental'", "EFFECTIVE, not fundamental" in rd("deepseek_push/E02_quantum_face.out"))
g035 = rd("glm53_push/G035_results.md")
check("4.2 G035: f_esc = 0.37-0.51, r50 = 4.9-10.4 r_M, sigma^2 -> 0.32-0.33, 'must be POSTULATED'", "f_esc = 0.37–0.51" in g035 and "r50 = 4.9–10.4 r_M" in g035 and "0.32–0.33" in g035 and "must be POSTULATED" in g035)
check("4.2 G081 (deepseek): 'G035's KILL' stands", "G035's KILL" in rd("deepseek_push/G081_equilibrium_stability.out"))
g230 = rd("deepseek_push/G230_dmdg_measure.out")
check("4.3 G230: pooled dM/dg index +3.47 +- 0.20 (z = +7.28); KS p = 0.000; 1/5 PASS", "p = +3.47 +- 0.20" in g230 and "z = +7.28" in g230 and "KS p = 0.000" in g230 and "G230 COMPLETE: 1/5 checks PASS" in g230)
g228 = rd("deepseek_push/G228_lomax_maxent.py")
check("4.3 G228: c = 1/2 'CALIBRATED'; three literal-True verdict checks", "CALIBRATED" in g228 and len(re.findall(r"check\(\s*True\s*,|,\s*True\s*,\s*V\d|\"[^\"]*\",\s*True\s*,", g228)) == 3)
n1 = rd("deepseek_moa/N1_maxent_lomax.json")
check("4.3 N1: independent max-entropy selection gives n = 1.85 (deepseek_moa/N1_maxent_lomax.json)", re.search(r"1\.85\d*", n1) is not None, "N1 register not found" if not n1 else "")
g059 = rd("glm53_push/G059_partition_function.out")
check("4.4 G059: kernel share 0.57x / 0.61x; required 0.76; 1/7 PASS", "0.57x" in g059 and "0.61x (alt)" in g059 and "0.76 at 420 kpc" in g059 and "G059 COMPLETE: 1/7 checks PASS" in g059)
mu2 = lambda u: 1.0 - (1.0 + u) ** -2
x = brentq(lambda x: x * mu2(x / 2.0) - 1.0, 1.0, 10.0)
check("4.5 the kernel at r_M: g/g_N = 1.489 -> M_dark(<r_M)/M_b = 0.489", near(x, 1.489, 0.001))
h033 = jl("hy4_push/H033_P1_results.json") or {}
c1 = next((r for r in h033.get("results", []) if r["check"].startswith("C1")), {}); c3 = next((r for r in h033.get("results", []) if r["check"].startswith("C3")), {})
check("4.5 H033_P1: slope +0.2650 +- 0.0377 dex/dex (7.0 sigma) FAIL; 81.2 vs 213.7 (-0.420 dex) FAIL", "+0.2650 +/- 0.0377" in str(c1.get("measured")) and c1.get("pass") is False and "81.2" in str(c3.get("measured")) and "-0.420" in str(c3.get("measured")) and c3.get("pass") is False)
check("4.5 H037: 'H033 RETRACTED ... WRONG by 2.04x'; abstract carries 213.74; capstone 106.882", "WRONG by 2.04x" in rd("hy4_push/H037_results.out") and "a0/(pi G) = 213.74" in rd("deepseek_push/MNRAS_ABSTRACT.md") and "Σ = 106.882" in rd("deepseek_push/THE_COMPLETE_THEORY.md"))
l261 = jl("fable_independent_2026/L261_results.json") or {}
A, B = l261.get("parts", {}).get("A", {}), l261.get("parts", {}).get("B", {})
check("4.6 L261 A: z*(5 keV) band reproduces to < 1e-3; window upper edge = 5 x (121.44/119.21)^2", A.get("max_dev", 1) < 1e-3)
check("4.6 L261 B: G212 9/9 literal-True; W_B = (3.3, 5.7); m = 5.0886 +- 0.0969; 6.3 sigma below 5.7; P(allowed) = 2.3%",
      B.get("literal_true") == 9 and B.get("calls") == 9 and list(B.get("W_B", [])) == [3.3, 5.7] and near(B.get("m", [0])[0], 5.0886, 1e-4) and near(B.get("z_below_57"), 6.31, 0.01) and near(B.get("p_allowed"), 0.023, 0.001))
check("4.6 G168 header: 'z* is DEFINED by'; G163: 'storying'", "z* is DEFINED by" in rd("deepseek_push/G168_cosmic_noon_mass.py") and "storying" in rd("deepseek_push/G163_cosmic_noon.out").lower())
g093 = rd("deepseek_push/G093_freedust.py")
check("4.6 G093 cites the forest as LOWER bounds 3.3 / 5.3 / 5.7 keV", sorted(float(x) for x in re.findall(r"m_WDM\s*>\s*(\d+\.\d+)\s*keV", g093)) == [3.3, 5.3, 5.7])
H = l261.get("parts", {}).get("H", {})
check("4.7 G152 rules the Omega_Lambda closure CIRCULAR; later docs print 'from a0 alone'; G198 subtracts", any("Omega_Lambda closure" in c for c in H.get("g152_circular", [])) and all(H.get("relabeled_from_a0_alone", [])) and H.get("g198_subtraction"))
check("4.8 the splice: G086 'ORDINARY MATTER ... p = 0' and G234 sourced equation; L243 6.44x", H.get("nofield") and H.get("sourced") and H.get("l243_q2") == "6.44")
I = l261.get("parts", {}).get("I", {})
check("4.9 tSZ windows (-1.7,-0.9) -> (-2.94,-2.14); A85 -3.246 vs -2.596 NEITHER; tilt absent from the matrix",
      I.get("tsz_windows") and I["tsz_windows"][0] and I["tsz_windows"][1] and I.get("a85") and I["a85"][0] == "-3.246" and I["a85"][3] == "NEITHER" and "G223" not in rd("deepseek_push/FALSIFIER_MATRIX.md"))
check("4.9 the pre-registration untouched (L261 G7)", (l261.get("parts", {}).get("G", {}) or {}).get("prereg_commits") == [])

n, n_pass = len(CH), sum(CH)
print(f"\nL262 COMPLETE: {n_pass}/{n} checks PASS (a FAIL = a number in PAPER30 no longer matches its committed register).")
