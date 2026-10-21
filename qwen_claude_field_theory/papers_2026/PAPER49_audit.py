#!/usr/bin/env python3
"""PAPER49 audit: the built PDF must be newer than the TeX, the action's rest state must be the law (and the double-counted
form must not be), every quoted number must match the committed lane outputs, the honesty phrases must be present, and no
forbidden claim or local path may appear.  Run: python3 PAPER49_audit.py (exit 0 only if all pass).
PAPER49_AUDIT_MUTATE=1 swaps W_rem for W_full in the rest-state check; the audit must then FAIL (the check bites).
Gate the deposit on this: build && audit && publish."""
import json, math, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.join(HERE, "..", "..", "campaign_fresh_gravity")
TEX, PDF = os.path.join(HERE, "PAPER49_why_cold_energy_settles_2026.tex"), os.path.join(HERE, "PAPER49_why_cold_energy_settles_2026.pdf")
MUTATE = os.environ.get("PAPER49_AUDIT_MUTATE") == "1"
F = 0
def check(name, ok, msg=""):
    global F
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {msg}" if msg else "")); F += (not ok)
J = lambda p: json.load(open(os.path.join(CFG, p)))
G, C, MSUN, PC, AU = 6.674e-11, 2.99792458e8, 1.98892e30, 3.0857e16, 1.495978707e11
GMSUN, A0 = 1.32712440018e20, 9.3603e-11            # canonical footing
print(f"PAPER49 audit{' (MUTATE: W_full in place of W_rem)' if MUTATE else ''}")

check("A1 PDF newer than TeX", os.path.getmtime(PDF) >= os.path.getmtime(TEX))
txt = subprocess.run(["pdftotext", "-layout", PDF, "-"], capture_output=True, text=True, check=True).stdout
for a, b in (("ﬁ", "fi"), ("ﬂ", "fl"), ("−", "-"), ("–", "-"), ("’", "'"), ("×", "x")): txt = txt.replace(a, b)
flat = re.sub(r"\s+", " ", txt); sq = re.sub(r"\s+", "", txt); sqd = re.sub(r"-\s*\n\s*", "", txt); sqd = re.sub(r"\s+", "", sqd)
def has(name, s):   # whitespace-free match, with and without line-end hyphens, so a line break never fails a check
    k = re.sub(r"\s+", "", s); check(name, k in sq or k in sqd, s)
hasq = has

# B. The action's rest state. Tether balance g_N = R(u); the field equation gives g = g_N + u.
#    W_rem: R(u) = u^2/(a0 - u)  -> must give g_N = g^2/(g + a0) exactly.
#    W_full (double-counted quadratic): R(u) = a0 u/(a0 - u) -> nu -> 2 in deep MOND; this must NOT pass.
def u_of(gN):
    if MUTATE:
        return A0 * gN / (A0 + gN)                    # a0 u/(a0-u) = gN
    return 0.5 * (-gN + math.sqrt(gN * gN + 4 * A0 * gN))   # u^2/(a0-u) = gN
worst = 0.0
for i in range(-60, 41):
    gN = A0 * 10 ** (i / 10); g = gN + u_of(gN)
    worst = max(worst, abs(g * g / (g + A0) - gN) / gN)
check("B1 rest state is g_N = g^2/(g+a0) for 1e-6..1e4 a0", worst < 1e-12, f"worst rel {worst:.1e}")
gN = 1e-4 * A0; nu = (gN + u_of(gN)) / gN
check("B2 nu(g_N = 1e-4 a0) = 100.5", abs(nu - 100.50125) < 1e-4, f"{nu:.5f}"); has("B2 text", "100.5")
check("B3 deep limit V^4 = G M a0 (g -> sqrt(a0 g_N))", abs((gN + u_of(gN)) / math.sqrt(A0 * gN) - 1) < 0.01)
has("B4 a0 = 0.173 c H_inf", f"{0.5 * math.sqrt(3 / (8 * math.pi)):.3f}")
sig = A0 / (math.pi * G) / (MSUN / PC ** 2); check("B5 tether capacity a0/(pi G)", round(sig) == 214, f"{sig:.1f} Msun/pc^2"); has("B5 text", "214")

# C. The stiffness length and what scales with it (CFG820 floor; CFG770 at the old floor 5.75 pc; CFG740 envelope).
L95 = J("CFG820_stiffness_from_globulars/cfg820_results.json")["primary (no Pal 3)|canonical"]["L95"]
check("C1 CFG820 floor rounds to 24 pc", round(L95) == 24, f"{L95:.3f} pc"); has("C1 text window", "[24 pc"); has("C1 text Saturn", "5.75 pc")
pull = GMSUN / (L95 * PC) ** 2; check("C2 sunward pull <= 2.4e-16", pull <= 2.45e-16, f"{pull:.3e}"); check("C2 text (TeX source: pdftotext splits this superscript onto another line; A1 ties the PDF to the TeX)",
      r"2.4\times10^{-16}" in open(TEX).read(), r"2.4\times10^{-16}")
t1 = J("CFG770_cassini_stiff_action/cfg770_results.json")["checks"]["T1 Cassini Q2 (headline)"]["detail"]
q_old = float(re.search(r"ceiling ([0-9.e+-]+)", t1).group(1)); check("C3 CFG770 Q2 at 5.75 pc", f"{q_old:.1e}" == "3.5e-06", f"{q_old:.3e}")
hasq("C3 text old", "3.5x10-6")
q_new = q_old * (5.75 / L95) ** 3; check("C4 Q2 at the new floor <= 5e-8 (Q2 ~ L*^-3)", q_new <= 5e-8, f"{q_new:.2e}"); hasq("C4 text", "5x10-8")
s = 5e4 * AU / PC; wb = 0.5 * (s / L95) ** 2; check("C5 wide-binary envelope at 50 kAU <= 5e-5", wb <= 5e-5 * 1.05, f"{wb:.2e}"); hasq("C5 text", "5x10-5")
check("C6 CFG740 envelope reproduced at 5.75 pc (8.9e-4)", f"{0.5 * (s / 5.75) ** 2:.1e}" == "8.9e-04")

# D. Shear (CFG650, both footings) and the excluded own-supply edge (CFG801).
r650 = J("CFG650_theory_v2_combined_pm/cfg650_native_results.json")["runs"]
for foot, key in (("canonical", "L100_N1024_canonical"), ("alt", "L100_N1024_alt")):
    d = r650[key]["surveys"]["KiDS"]; dc = [v for k, v in d.items() if "dchi2" in k.lower() and isinstance(v, (int, float))]
    has(f"D1 shear {foot}", f"-{abs(dc[0]):.2f}" if dc else "MISSING")
n1 = J("CFG654_independent_inputs/cfg654_native_results_NC1x.json")
check("D3 native rerun canonical (NC1x vs NCS0) CONSISTENT", n1["foot"] == "canonical" and n1["surveys"]["KiDS"]["class"] == "CONSISTENT"
      and n1["surveys"]["KiDS"]["dchi2"] <= 0, f"{n1['surveys']['KiDS']['dchi2']:.2f}"); has("D3 text", f"-{abs(n1['surveys']['KiDS']['dchi2']):.2f}")
e801 = J("CFG801_settled_edge_vs_kids/cfg801_results.json")["primary R<=0.31 Mpc"]["dchi2"]   # canonical footing file
check("D2 CFG801 edge dchi2 +197", round(e801) == 197, f"{e801:.2f}"); has("D2 text", "+197")

# E. Hot-gas / expelled-gas rule on all 318 eRASS1 clusters (CFG815, canonical, profiles P and F).
mids, zs, core = [], [], []
for prof in ("P", "F"):
    t = J(f"CFG815_hex_erosita_full/cfg815_results_{prof}.json")["T_R"]["s|canonical|EX"]
    mids.append(t["terciles"][1][0]); zs.append(t["terciles"][1][2]); core.append(t["A"]["MID"][0])
check("E1 middle-mass third x1.5-1.6", f"{min(mids):.1f}" == "1.5" and f"{max(mids):.1f}" == "1.6", f"{min(mids):.3f}-{max(mids):.3f}")
check("E2 Z +4.0 to +4.6", f"{min(zs):.1f}" == "4.0" and f"{max(zs):.1f}" == "4.6", f"{min(zs):.2f}-{max(zs):.2f}")
check("E3 core excess 1.1-1.2 with the rule", f"{min(core):.1f}" == "1.1" and f"{max(core):.1f}" == "1.2", f"{min(core):.3f}-{max(core):.3f}")
has("E text range", "1.5-1.6"); has("E text Z", "Z = +4.0 to +4.6"); has("E text core", "1.1-1.2"); has("E text plain", "1.85")

# F. SPARC scatter for the action's law (CFG695, both footings).
s695 = J("CFG695_saturating_vacuum/cfg695_results.json")["numbers"]["S2"]
check("F1 SPARC rms ~0.100 both footings", all(abs(s695[f]["rms"] - 0.100) < 0.0015 for f in ("canonical", "alt")),
      f"{s695['canonical']['rms']:.4f} / {s695['alt']['rms']:.4f}"); has("F1 text", "0.100 dex")

# V. v1.1 correction, wording fixed in v1.2 (lanes AG6C, AG7): every number read from the lanes' own outputs and JSON
AG6 = os.path.join(HERE, "..", "..", "argon_push", "AG6C_relativistic_completion")
so = open(os.path.join(AG6, "ag6c_s0_saddle.out")).read(); sj = json.load(open(os.path.join(AG6, "ag6c_s0_saddle_results.json")))["numbers"]["fiducials"]
C02 = float(re.search(r"mid-plane C\(R = 0\.2\) : (-?[0-9.]+) \(h\) vs (-?[0-9.]+) \(h/2\)", so).group(2))
rb = float(re.search(r"rhobar_c = 5\.364 Omega_b rho_crit = ([0-9.e+-]+)", so).group(1))
r1 = C02 * sj["F1_MW-M31_canonical"]["unit_kg_m3"] / rb; r2 = C02 * sj["F2_cluster_pair_canonical"]["unit_kg_m3"] / rb
check("V1 converged R = 0.2d densities from AG6C (F1, F2 canonical)", f"{r1:.0f}" == "-89" and f"{r2:.0f}" == "-33", f"{r1:.1f} / {r2:.1f} rhobar")
has("V1 text -89", "-89"); has("V1 text -33", "-33")
col = lambda ks: [f"{v:.1f}" for v in sorted((sj[k]["Sigma_unsuppliable_Msun_pc2"] for k in ks), reverse=True)]   # numeric: least negative first
c1 = col(("F1_MW-M31_canonical", "F1_MW-M31_alt")); c2 = col(("F2_cluster_pair_canonical", "F2_cluster_pair_alt"))
check("V2 unsuppliable columns from AG6C JSON", c1 == ["-1.9", "-2.1"] and c2 == ["-4.6", "-5.1"], f"F1 {c1}, F2 {c2}")
has("V2 text F1 dip depth", f"{c1[0][1:]} to {c1[1][1:]}"); has("V2 text F2 dip depth", f"{c2[0][1:]} to {c2[1][1:]}")   # v1.2 quotes depths (positive)
m = re.search(r"negative region: R in \[([0-9.]+), ([0-9.]+)\], z in \[([0-9.]+), ([0-9.]+)\]", so)
check("V3 pancake extent from AG6C (R <= 0.43 d, |z| <= 0.05 d)", f"{float(m.group(2)):.2f}" == "0.43" and f"{float(m.group(4)):.2f}" == "0.05", m.group(0))
for t in ("Correction (v1.1, 2026-10-20; wording fixed in v1.2, 2026-10-21)", "Prediction: no saddle dip", "v1.2 note", "Working note, v1.2"):
    has(f"V4 text '{t}'", t)
mc = re.search(r"negative part ([-+0-9.]+), net ([-+0-9.]+)", so)
cn, cnet = float(mc.group(1)), float(mc.group(2))
check("V5 AG6C net column through the saddle is positive (negative part, net)", cnet > 0 and f"{cn:.3f}" == "-0.206" and f"{cnet:+.3f}" == "+0.016", mc.group(0))
has("V5 text negative part", "-0.206"); has("V5 text net", "+0.016")
AG7 = os.path.join(HERE, "..", "..", "argon_push", "AG7_saddle_trough_preflight"); r7 = json.load(open(os.path.join(AG7, "ag7_results.json")))
pr = [r["SN_strip"] for r in r7["rows"] if r["Mb"] == 10 ** 11.3 and r["d_hMpc"] == 8.23]
check("V6 AG7 primary strip S/N below 1 on both footings; ~12x pairs for 3 sigma", len(pr) == 2 and max(pr) < 1 and round(r7["N3"] / 23000) == 12 and not r7["mutate"],
      f"S/N {[round(x, 2) for x in pr]}, N3/N {r7['N3'] / 23000:.1f}, reading {r7['reading']}")
has("V6 text S/N", "S/N below 1"); has("V6 text pairs", "about twelve times as many pairs"); has("V6 text ref", "arXiv:1702.08485")

# G-H. Honesty and forbidden phrases; stale statements must be gone.
for p in ("fitted", "not closed", "not peer reviewed", "conditional", "is excluded by KiDS-1000"): has(f"G honesty '{p}'", p)
low = flat.lower()
for bad in ("theory closed", "theory is closed", "data favour the framework", "data favor the framework", "proves the framework",
            "/users/", "breakthrough", "[5.75 pc", "4.2x10-15", "frozen test is queued", "+2.03"):
    k = bad.replace(" ", ""); check(f"H forbidden/stale '{bad}' absent", bad not in low and k not in sq.lower() and k not in sqd.lower())
print(f"\nPAPER49 audit: {'ALL PASS' if F == 0 else f'{F} FAIL'}"); sys.exit(1 if F else 0)
