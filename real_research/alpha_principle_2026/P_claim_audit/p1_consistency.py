#!/usr/bin/env python3
"""P1 -- internal consistency of ALPHA_CHAIN_STATUS.md: commit hashes, script names, quoted numbers, counts, the verification note.

Pre-registered in P_PREREGISTRATION.md (protocol item 6).  Read-only: it reads the document, the committed .out files, the scripts and `git log`/`git show`;
it writes nothing.  Exit 0 iff every assertion holds.  Several assertions state an INCONSISTENCY that the audit found (marked FINDING): they hold when the
inconsistency is present, so a later fix of the document or scripts changes the exit code and the report must be revisited.

Run:     PYTHONDONTWRITEBYTECODE=1 python3 p1_consistency.py
CONTROL: PYTHONDONTWRITEBYTECODE=1 python3 p1_consistency.py MUTATE
         (the ONLY trigger is argv[1] == "MUTATE": the document text is altered in memory -- one commit hash changed by a character and the quoted x = 2.85e-122
          changed to 2.95e-122 -- so the hash and the number checks must fail -> exit 1)
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
AP = os.path.abspath(os.path.join(HERE, ".."))                       # alpha_principle_2026
RR = os.path.abspath(os.path.join(AP, ".."))                         # real_research
REPO = os.path.abspath(os.path.join(RR, ".."))
AS = os.path.join(RR, "alpha_schwinger_2026")
LEAN = os.path.join(REPO, "fable_independent_2026", "lean_2026")
MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
FAILS = []


def chk(tag, ok, note=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {note}")
    if not ok:
        FAILS.append(tag)


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, text=True).stdout


def rd(path):
    with open(path) as fh:
        return fh.read()


doc = rd(os.path.join(AP, "ALPHA_CHAIN_STATUS.md"))
if MUT:
    doc = doc.replace("4dc1a546a", "4dc1a546b").replace("2.85e-122", "2.95e-122")

print("== 1. commit hashes")
hashes = sorted(set(re.findall(r"(?<![.\d])(?=[0-9a-f]*[a-f])[0-9a-f]{9}\b", doc)))
print("  hashes in the document:", hashes)
expected_paths = {
    "4dc1a546a": ["alpha_schwinger_2026/ah5_dimensional_obstruction.py"],
    "5db88bfc2": ["alpha_schwinger_2026/ah1_schwinger_ds2.py"],
    "86f3c7a9a": ["fable_independent_2026/lean_2026/AH3_alpha_nogo.lean"],
    "5823f6bfe": ["alpha_schwinger_2026/ah2_induced_current_ds2.py"],
    "0c72bfdec": ["alpha_schwinger_2026/ah4_induced_current_ds4.py"],
    "e39f0bfcc": ["alpha_schwinger_2026/ah6_kaluza_klein.py"],
    "a628e8a66": ["A_wgc_extremal/", "B_rg_asymptotic_safety/", "C_holographic_species/", "E_dynamical_attractor/", "F_kk_stabilization/", "G_topological_anomaly/"],
    "1d23899e6": ["D_calibration_bar/"],
    "190cb6920": ["H_string_heterotic/", "I_selection_consistency/", "J_emergent_condensate/"],
}
for h in hashes:
    kind = git("cat-file", "-t", h).strip()
    files = git("show", "--name-only", "--format=", h)
    ok = kind == "commit" and all(p in files for p in expected_paths.get(h, []))
    chk(f"hash {h} resolves to a commit and touches {expected_paths.get(h, ['(no path expectation)'])[0]}...", ok, f"(type {kind or 'MISSING'})")
chk("all nine hashes of the document have a path expectation", all(h in expected_paths for h in hashes) and len(hashes) == 9)
for tag, h in (("lane M commit", "442b3253e"), ("lane K commit", "087c41203")):
    chk(f"{tag} {h} exists in git log", git("cat-file", "-t", h).strip() == "commit")
msg_1d = git("log", "-1", "--format=%B", "1d23899e6")
chk("the void remark ('within 0.6% of Z') is in lane D's commit message 1d23899e6, as the document says", "within 0.6% of Z" in msg_1d)
last = git("log", "-1", "--format=%h", "--", "real_research/alpha_principle_2026/ALPHA_CHAIN_STATUS.md").strip()
print("  last commit touching the status document:", last)

print("== 2. script and path names quoted in the document")
names = re.findall(r"`([^`]+)`", doc)
for n in names:
    if n.startswith("--") or " " in n:
        continue
    if "." not in n and "/" not in n:
        if n == "no_alpha_from_obs":                                   # a Lean theorem name, not a file
            chk("quoted Lean theorem no_alpha_from_obs is declared in AH3_alpha_nogo.lean", "theorem no_alpha_from_obs" in rd(os.path.join(LEAN, "AH3_alpha_nogo.lean")))
        continue
    cands = [os.path.join(REPO, n), os.path.join(AS, n), os.path.join(AP, n)]
    chk(f"quoted name {n} exists", any(os.path.exists(c) for c in cands))
for lane in "A_wgc_extremal B_rg_asymptotic_safety C_holographic_species D_calibration_bar E_dynamical_attractor F_kk_stabilization G_topological_anomaly " \
            "H_string_heterotic I_selection_consistency J_emergent_condensate K_literature_audit M_red_team".split():
    chk(f"lane directory {lane} exists", os.path.isdir(os.path.join(AP, lane)))
chk("K_literature_audit/K_PREREGISTRATION.md exists (cited for source status)", os.path.exists(os.path.join(AP, "K_literature_audit", "K_PREREGISTRATION.md")))

print("== 3. quoted numbers appear in the cited outputs")
def outp(*parts):
    return rd(os.path.join(*parts))
NUMS = [
    ("2.85e-122", r"2\.85e-122", [(AS, "ah5_dimensional_obstruction.out", r"= 2\.8485e-122")]),
    ("0.124/mu^2", r"0\.124/mu\^2", [(AS, "ah4_induced_current_ds4.out", r"C = 0\.1240")]),
    ("R = 23.41 l_P", r"23\.41 l_P", [(AS, "ah6_kaluza_klein.out", r"= 23\.412475")]),
    ("5.2e17 GeV", r"5\.2e17 GeV", [(AS, "ah6_kaluza_klein.out", r"5\.215e\+17 GeV")]),
    ("electron 1e-21", r"1e-21 of the minimum", [(AS, "ah6_kaluza_klein.out", r"9\.799e-22")]),
    ("n ~ 3.5e61", r"3\.5e61", [(AP, "A_wgc_extremal/a2_dirac_extremal_and_handles.out", r"3\.468e\+61")]),
    ("alpha^-1 ~ 75-77", r"75-77", [(AP, "B_rg_asymptotic_safety/b3_forced_vs_required.out", r"77\.06477"), (AP, "B_rg_asymptotic_safety/b3_forced_vs_required.out", r"75\.21563")]),
    ("alpha^-1 ~ 105 (Planck)", r"alpha\^-1 ~ 105", [(AP, "B_rg_asymptotic_safety/b2_required_boundary.out", r"104\.917")]),
    ("misses by ~1.9x", r"~1\.9x", [(AP, "C_holographic_species/c2_emergence_species.out", r"target/toy = 1\.912"), (AP, "C_holographic_species/c2_emergence_species.out", r"target/toy = 1\.947")]),
    ("1/alpha_em ~ 107", r"~ 107", [(AP, "M_red_team/m4_lane_c_content_and_cutoff.out", r"1/alpha_em = 107\.25")]),
    ("~8.6 extra", r"~8\.6 extra", [(AP, "M_red_team/m4_lane_c_content_and_cutoff.out", r"n_x = 8\.582")]),
    ("cutoff shift 0.6%", r"by 0\.6%", [(AP, "M_red_team/m4_lane_c_content_and_cutoff.out", r"shift 0\.62 %")]),
    ("zeta 6.5e-8", r"6\.5e-8", [(AP, "E_dynamical_attractor/e2_variation_bounds.out", r"6\.504e-08")]),
    ("1+w up to ~0.25", r"~0\.25 at", [(AP, "E_dynamical_attractor/e2_variation_bounds.out", r"w0 =  -0\.752: zeta_max")]),
    ("R ~ 1e30 l_P", r"1e30 l_P", [(AP, "F_kk_stabilization/f1_radion_circle.out", r"1\.028e\+30")]),
    ("~115 decades", r"~115 decades", [(AP, "F_kk_stabilization/f1_radion_circle.out", r"114\.6 decades")]),
    ("104.94", r"104\.94", [(AP, "A_wgc_extremal/a3_inequalities_and_scale.out", r"~ 104\.94"), (AP, "M_red_team/m1_lane_a_running_check.out", r"104\.937")]),
    ("k = 5.12", r"k = 5\.12", [(AP, "M_red_team/m1_lane_a_running_check.out", r"at m_P \(this run\) 5\.1219")]),
    ("Z 12-13% away", r"12-13% away", [(AP, "M_red_team/m1_lane_a_running_check.out", r"13\.02 %"), (AP, "A_wgc_extremal/a3_inequalities_and_scale.out", r"-12\.0 %")]),
    ("f_g to 0.18%", r"0\.18%", [(AP, "M_red_team/m2_lane_b_sign_and_precision.out", r"0\.0018 \(relative\) = 0\.18 %")]),
    ("MM coupling ~1e-121", r"1e-121", [(AP, "M_red_team/m3_ds_gauge_coupling.out", r"1\.519e-121")]),
    ("Gilson 27.8 sigma", r"27\.8 sigma", [(AP, "K_literature_audit/k1_numeric_audit.out", r"27\.8")]),
    ("Gilson 28.695", r"28\.695", [(AP, "K_literature_audit/k1_numeric_audit.out", r"a\* = 28\.69533587")]),
    ("Gilson chance 0.61", r"chance 0\.61", [(AP, "K_literature_audit/k1_numeric_audit.out", r"rounding chance 0\.61")]),
    ("Wyler 3800 sigma", r"3800 sigma", [(AP, "K_literature_audit/K_REPORT_TABLE.md", r"3\.8e\+03")]),
    ("Bleger 3.3e-11, P = 0.90", r"P = 0\.90", [(AP, "K_literature_audit/k1_numeric_audit.out", r"3\.27e-11"), (AP, "K_literature_audit/k1_numeric_audit.out", r"0\.899")]),
    ("bands hundreds to thousands x 1e-3", r"hundreds to thousands", [(AP, "I_selection_consistency/i4_widths_and_verdict.out", r"329"), (AP, "I_selection_consistency/i4_widths_and_verdict.out", r"1678")]),
]
for tag, docre, outs in NUMS:
    in_doc = re.search(docre, doc) is not None
    in_out = all(re.search(pat, rd(os.path.join(base, f))) is not None for base, f, pat in outs)
    chk(f"{tag}: quoted in the document and present in the cited output(s)", in_doc and in_out, f"(doc {in_doc}, out {in_out})")

print("== 4. counts and structure")
rows = [ln for ln in doc.splitlines() if re.match(r"\| [A-J] \|", ln)]
no_der = [ln for ln in rows if "no derivation proposed" in ln]
print(f"  route-table rows: {len(rows)}; rows saying '(no derivation proposed)': {len(no_der)}")
chk("route table has ten rows A-J", len(rows) == 10)
chk("FINDING: row 5 of the chain table says 'Ten independent routes' while row D of the route table proposes no derivation (nine routes plus the bar)",
    "Ten independent routes" in doc and len(no_der) == 1)
lean = rd(os.path.join(LEAN, "AH3_alpha_nogo.lean"))
n_thm = len(re.findall(r"^theorem ", lean, re.M))
n_axprint = len(re.findall(r"^#print axioms", lean, re.M))
chk("AH3 Lean: ten '#print axioms' lines (the document's 'ten theorems'); FINDING: the file declares eleven theorems (obs_rescale is not printed)", n_axprint == 10 and n_thm == 11, f"(theorems {n_thm}, printed {n_axprint})")
chk("AH3 Lean .out lists ten theorems on the standard axioms only", len(re.findall(r"depends on axioms: \[propext, Classical\.choice, Quot\.sound\]", rd(os.path.join(LEAN, "AH3_alpha_nogo.out")))) == 10)
chk("AH3 Lean: no 'sorry' in the file", "sorry" not in re.sub(r"Zero sorry\.", "", lean))

print("== 5. the verification note (mutation-control invocation)")
def src(base):
    return rd(base)
pos, dash, other = [], [], []
for lane in sorted(os.listdir(AP)):
    d = os.path.join(AP, lane)
    if not os.path.isdir(d) or not re.match(r"[A-M]_", lane) or lane[0] == "N":
        continue
    for f in sorted(os.listdir(d)):
        if f.endswith(".py") and f not in ("rg_common.py", "bar_lib.py", "alpha_bar_checker.py"):
            s = src(os.path.join(d, f))
            if "--mutate" in s and "'--mutate'" in s or '"--mutate"' in s:
                dash.append((lane[0], f))
            elif "MUTATE" in s:
                pos.append((lane[0], f))
            else:
                other.append((lane[0], f))
lanes_pos = sorted({l for l, _ in pos})
lanes_dash = sorted({l for l, _ in dash})
print("  lanes using an argv MUTATE:", lanes_pos, "; lanes using --mutate:", lanes_dash, "; scripts with no control flag:", other)
chk("document: 'positional MUTATE for A, B, D, E, G, H, I, J' -- source: A B D E G H I J use MUTATE (B via 'in argv'); FINDING: lane M also uses positional MUTATE (not named)",
    lanes_pos == ["A", "B", "D", "E", "G", "H", "I", "J", "M"])
chk("document: '--mutate for AH scripts and lane F/C' -- source: C, F use --mutate; FINDING: lane K also uses --mutate (not named)", lanes_dash == ["C", "F", "K"])
chk("FINDING: AH5 has no MUTATE control at all (its prereg/commit says 'exact algebra, so no MUTATE control'), yet the note says every control exits 1",
    "MUTATE" not in src(os.path.join(AS, "ah5_dimensional_obstruction.py")) and "mutate" not in src(os.path.join(AS, "ah5_dimensional_obstruction.py")))
ex = {"ah1_schwinger_ds2.py": "sys.exit(0 if not c1_ok else 1)", "ah2_induced_current_ds2.py": "sys.exit(0 if not v1_ok else 1)",
      "ah4_induced_current_ds4.py": "sys.exit(0 if not v1_ok else 1)", "ah6_kaluza_klein.py": "sys.exit(0 if not k1_ok else 1)"}
for f, line in ex.items():
    chk(f"FINDING: {f} --mutate exits 0 when the control works ('{line}'), so 'every control exits 1' is false for it", line in src(os.path.join(AS, f)))
chk("lane K: k2 --mutate-s2 changes nothing (document says so); its docstring says it exits 0 if the survivor set is unchanged",
    "exit 0 if unchanged" in src(os.path.join(AP, "K_literature_audit", "k2_structural_scoring.py")))

print("\nFAILED:", FAILS if FAILS else "none")
sys.exit(1 if FAILS else 0)
