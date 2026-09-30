"""CFG230 script A (CITATION-AUDIT): audits the frozen hand transcription against the repository.
Checks: (1) every cited commit is a git object; (2) the commit touches the cited lane prefix (combined commits are listed);
(3) every anchor string is present in its cited file; (4) the 5.1 matrix against the gate cells of TEN_DOORS_RESULT / DOOR11_RESULT;
(5) Lean statement names exist at HEAD and at b8d8b1ba5, and the pending batch is still untracked; (6) the section-2.4 candidate
DISAGREEMENTS; (7) class/grade tallies. Main exits 0; every MISS is kept and listed in the README."""
import re, os
import CFG230_common as C
import CFG230_data as D

R = C.Run("CFG230_A_evidence_audit")
R.p("CFG230 A: evidence audit. repo=<repo>")

# ---------------------------------------------------------------- 1-3 commits, lane prefixes, anchors
R.p("\n== 1-2. commits exist and touch the cited lane")
allc = {}
for k, v in list(D.ROWS.items()) + list(D.SUPPORT.items()):
    allc[(k, "lane")] = (v["lane"], v["commit"])
    if v.get("ref") and v.get("refc"):
        allc[(k, "referee")] = (v["ref"], v["refc"])
files_cache = {}
def touched(c):
    if c not in files_cache:
        rc, out = C.git("show", "--name-only", "--format=", c)
        files_cache[c] = out.split() if rc == 0 else None
    return files_cache[c]
seen = set()
for (k, kind), (lane, c) in allc.items():
    if (lane, c) in seen:
        continue
    seen.add((lane, c))
    fl = touched(c)
    if fl is None:
        R.check("CITATION-AUDIT", f"{lane} commit {c} exists", False, "not a git object")
        continue
    hit = [f for f in fl if re.search(rf"(^|/){lane}(_|/|\.|$)", f)]
    R.check("CITATION-AUDIT", f"{lane} @ {c} touches {lane}*", bool(hit), f"({len(hit)} of {len(fl)} paths; rows {k})")
# combined commits (frozen section 2.4)
R.p("\n== combined commits named in the frozen file (2.4)")
for c, want in (("9e4757627", ["CFG120", "CFG123", "CFG124"]), ("b7d41c302", ["CFG122", "CFG109"])):
    fl = touched(c) or []
    got = sorted({m.group(1) for f in fl for m in [re.search(r"(CFG\d+)", f)] if m})
    R.check("CITATION-AUDIT", f"commit {c} holds lanes {want}", all(w in got for w in want), f"lanes present: {got}")
    R.res[f"combined_{c}"] = got

R.p("\n== 3. anchors present in cited files")
n_anch = 0; n_miss = 0
for k, v in list(D.ROWS.items()) + list(D.SUPPORT.items()):
    for f, s in v["anchors"]:
        t = C.read_norm(f)
        n_anch += 1
        ok = t is not None and C.norm(s) in t
        if not ok:
            n_miss += 1
            R.check("CITATION-AUDIT", f"{k}: anchor {s!r} in {os.path.basename(f)}", False, "file missing" if t is None else "string absent")
R.p(f"  anchors checked: {n_anch}, absent: {n_miss}")
R.res["anchors"] = {"checked": n_anch, "absent": n_miss}

# ---------------------------------------------------------------- 4 matrix vs source gate cells
R.p("\n== 4. matrix vs the gate cells printed in TEN_DOORS_RESULT / DOOR11_RESULT")
def parse_table(path):
    t = open(os.path.join(C.REPO, path), encoding="utf-8").read().splitlines()
    rows = []
    for ln in t:
        if ln.startswith("|") and not ln.startswith("|---") and not ln.startswith("| Door") and not ln.startswith("| Variant"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 6:
                rows.append(cells)
        if ln.startswith("## Binding failure"):
            break
    return rows
def first(cell):
    c = C.norm(cell).strip()
    if c.startswith("p*"): return "p*"
    m = re.match(r"^(F|P|U|N)\b", c)
    return m.group(1) if m else "?"
door_ids = {"1": "D01", "2": "D02", "3": "D03", "4": "D04", "5": "D05", "6": "D06", "7": "D07", "8": "D08", "9": "D09", "10": "D10"}
src = {}
for cells in parse_table(D.CM + "TEN_DOORS_RESULT_2026-09-29.md"):
    m = re.match(r"^(\d+)\b", cells[0])
    if m and m.group(1) in door_ids:
        src[door_ids[m.group(1)]] = [C.norm(x) for x in cells[1:6]]
d11 = {"11A": "D11A", "11B": "D11B", "11C-a": "D11Ca", "11C-b": "D11Cb", "11C-c": "D11Cc"}
for cells in parse_table(D.CM + "DOOR11_RESULT_2026-09-29.md"):
    for key, rid in d11.items():
        if C.norm(cells[0]).startswith(key):
            src[rid] = [C.norm(x) for x in cells[1:6]]
R.p(f"  source rows parsed: {sorted(src)}")
mism = []
def mcell(rid, r):
    return D.MATRIX[rid][D.REQS.index(r)]
for rid, cells in src.items():
    g = [first(x) for x in cells]  # G1..G5
    # G2 -> R05 ; G3 -> R06 ; G4 -> R12 ; G1 -> any of R01/R03/R04 ; G5 -> any of R09/R11
    expectations = []
    if g[0] == "F": expectations.append(("G1 F", any(mcell(rid, r) == "F" for r in ("R01", "R03", "R04"))))
    if g[0] == "p*": expectations.append(("G1 p*", any(mcell(rid, r) == "p*" for r in ("R01", "R03"))))
    for gi, r, nm in ((1, "R05", "G2"), (2, "R06", "G3"), (3, "R12", "G4")):
        gv = g[gi]
        if gv in ("F", "U", "p*"):
            expectations.append((f"{nm} {gv} -> {r}", mcell(rid, r) == gv))
        elif gv == "P":
            expectations.append((f"{nm} P -> {r} in (P,p*)", mcell(rid, r) in ("P", "p*")))
    if g[4] in ("F", "p*", "U"):
        expectations.append((f"G5 {g[4]} -> R09/R11", any(mcell(rid, r) == g[4] for r in ("R09", "R11"))))
    for label, ok in expectations:
        if not ok:
            mism.append((rid, label, cells))
            R.check("CITATION-AUDIT", f"{rid}: matrix vs source cell ({label})", False, f"source cells G1..G5 = {cells}")
R.p(f"  matrix/source mismatches: {len(mism)}")
R.res["matrix_source_mismatches"] = [(a, b) for a, b, _ in mism]
# D11Cd rows from DOOR11_RESULT addendum: G1 F every arm; G2 d1 P trivially, d2 F; G3 d1 P trivially, d2 F; G4 F strict
add = C.read_norm(D.CM + "DOOR11_RESULT_2026-09-29.md")
R.check("CITATION-AUDIT", "11C-d addendum: G1 F in every arm; d2 G2/G3 F; d1 G2/G3 P trivially", all(s in add for s in ("G1 F in every arm", "G2 d1 P trivially", "G3 d1 P trivially, d2 F")), "matrix D11Cd1 R05/R06 p*, D11Cd2 R05/R06 F")

# ---------------------------------------------------------------- 5 Lean
R.p("\n== 5. Lean statement names (committed certificate) and the pending batch")
for f, names in D.LEAN_NAMES.items():
    head = open(os.path.join(C.REPO, D.LEAN_DIR + f), encoding="utf-8").read() if os.path.isfile(os.path.join(C.REPO, D.LEAN_DIR + f)) else ""
    rc, atc = C.git("show", f"b8d8b1ba5:{D.LEAN_DIR}{f}")
    for n in names:
        # Ownership/Theory qualified names appear as ownership_nonlocal etc.
        R.check("CITATION-AUDIT", f"Lean {f}: {n} at HEAD", n in head, "")
        R.check("CITATION-AUDIT", f"Lean {f}: {n} at b8d8b1ba5", rc == 0 and n in atc, "")
R.p("  axioms-only certificate line:")
rc, rd = C.git("show", f"b8d8b1ba5:{D.LEAN_DIR}README.md")
R.check("CITATION-AUDIT", "README at b8d8b1ba5 states 219 theorems, standard axioms only", "219 theorems checked, standard axioms only" in rd, "")
rdn = C.norm(rd)
for lab, s_ in (("pointwise (QUMOND-type) laws only; PDE theories not formalised", "for pointwise (QUMOND-type) laws only; field-equation theories (AQUAL/QUMOND PDEs) are not formalised"),
                ("owned_boost_one near-definitional", "`owned_boost_one` is near-definitional"),
                ("ownership rule is a POSTULATE", "which is a POSTULATE"),
                ("Fluid: P2 point-mass pressure exceeds the cap for r < r_M", "exceeds this cap for r < r_M"),
                ("Gauss: algebra of the solution check; EL derivation not certified", "certified: the algebra of the solution check"),
                ("Exchange: certified as algebra; SK action not certified", "the Schwinger-Keldysh action and its Euler-Lagrange derivation"),
                ("DoorEleven: says nothing about media with w != -1", "says nothing about media with w != -1"),
                ("Profile: only the point mass was constructed", "only the point mass"),
                ("no_single_polytrope needs one extra step for GammaEff", "needs one extra step")):
    R.check("CITATION-AUDIT", f"Lean README (b8d8b1ba5) statement: {lab}", C.norm(s_) in rdn)
rc2, cur = C.git("ls-files", D.LEAN_DIR)
tracked = set(cur.split())
for f in D.LEAN_PENDING:
    tr = (D.LEAN_DIR + f) in tracked
    R.check("CITATION-AUDIT", f"pending module {f} still untracked", not tr, "COMMITTED SINCE: needs an amendment, not counted here" if tr else "untracked/pending")
    R.res[f"pending_{f}_tracked"] = tr

# ---------------------------------------------------------------- 6 candidate disagreements (2.4)
R.p("\n== 6. candidate DISAGREEMENTS of frozen section 2.4")
cf131 = C.read_norm(D.CF + "CFG131_door8_interacting_vacuum/README.md")
cf156 = C.read_norm(D.CF + "CFG156_door8_vacuum_referee/README.md")
fr156 = C.read_norm(D.CF + "CFG156_FROZEN_CRITERIA.md")
a = "32-272x (point mass, exact), 32-353x (exponential sphere" in cf131
b = "The exponential-sphere range (32-353x) is out of scope" in fr156
c = "32.2-271.7" in cf156
R.check("CITATION-AUDIT", "D08 spread: CFG131 README labels 32-272x point mass, 32-353x exponential sphere", a)
R.check("CITATION-AUDIT", "D08 spread: CFG156 frozen criteria declare the 32-353x exponential-sphere range out of scope", b)
R.check("CITATION-AUDIT", "D08 spread: CFG156 reports the point-mass 32.2-271.7", c)
R.p("  VERDICT D08: RECONCILED, not a disagreement: 32-272x is the point mass (referee reproduces 32.17-271.71); 32-353x is the")
R.p("  h = 2 kpc exponential sphere, which the referee did not test. The LEDGER row and TEN_DOORS text quote 32-353x without the")
R.p("  geometry label; the frozen file's R04 line 'differs 32-353x' must read 'point mass 32-272x, exponential sphere 32-353x'.")
R.res["d08_verdict"] = "reconciled: geometry label (point mass 32-272x; exponential sphere 32-353x, referee untested)"
g = C.read_norm(D.CM + "GATES_STATUS_2026-09-29.md")
cf44 = C.read_norm(D.CF + "CFG44_fluid_target/README.md")
R.check("CITATION-AUDIT", "GATES_STATUS row 5.12 still says 'departs by up to 2%'", "departs by up to 2%" in g)
R.check("CITATION-AUDIT", "CFG44 README carries the correction R(x = 1) = 1.46", "R(x = 1) = 1.46" in cf44)
R.check("CITATION-AUDIT", "CFG44 README's own line 9 also still says 'up to 2%' (stale in the body, corrected in the appended section)", "up to 2% in the charge function" in cf44)
R.p("  VERDICT 5.12: DISAGREEMENT CONFIRMED (stale wording); the number 1.46 is recomputed in script C.")
R.res["s512_verdict"] = "stale: GATES_STATUS 5.12 'up to 2%' vs CFG44 correction 1.46"
R.p("  cap-excluded window: which files carry which wording")
wording = {"about one decade": [], "about 11": [], "10⁴–10⁵": []}
scan = [D.CM + f for f in ("GAPS_1_2_JOINT_STATUS.md", "ACTIONS_AND_NOGOS.md", "GATES_STATUS_2026-09-29.md", "CLAIMS_AUDIT_2026-09-29.md", "README.md", "SHARED_VS_SPECIFIC_2026-09-29.md")]
scan += [D.CF + "STANDING_2026-09-29.md", D.CF + "CFG43_fluid_tie/README.md"]
pats = {"one decade": r"one decade", "11x": r"about 11", "1e4-1e5": r"10\^4-10\^5|10⁴-10⁵|10⁴–10⁵|1e4-1e5"}
for f in scan:
    t = open(os.path.join(C.REPO, f), encoding="utf-8", errors="replace").read()
    t = C.norm(t)
    hits = {k: len(re.findall(p, t)) for k, p in pats.items()}
    R.p(f"    {os.path.basename(f)}: {hits}")
    R.res.setdefault("cap_wording", {})[os.path.basename(f)] = hits
gaps = C.read_norm(D.CM + "GAPS_1_2_JOINT_STATUS.md")
cl = C.read_norm(D.CM + "CLAIMS_AUDIT_2026-09-29.md")
R.check("CITATION-AUDIT", "GAPS_1_2 line 13 says the cap covers 'about one decade in mass' (stale)", "about one decade" in gaps)
R.check("CITATION-AUDIT", "CLAIMS_AUDIT correction: window 'about 11x up to 10^4-10^5 in mass'", "from about 11x up to 10^4-10^5 in mass" in cl or "from about 11x up to 10^4-10^5" in cl or ("about 11x up to" in cl))
R.p("  VERDICT cap window: the corrected reading (convention-dependent, about 11x up to 1e4-1e5) is in CLAIMS_AUDIT and the CFG43 README;")
R.p("  GAPS_1_2 line 13 keeps 'about one decade' (stale); the frozen R12(b) wording follows the corrected reading. Not re-derived.")
R.res["cap_window_verdict"] = "GAPS_1_2 stale ('about one decade'); corrected: convention-dependent 11x-1e4..1e5"

# ---------------------------------------------------------------- 7 tallies
R.p("\n== 7. class and grade tallies of the frozen sub-claims")
from collections import Counter
cnt = Counter((cl_, gr) for r in D.REQS for (_, cl_, gr, lb) in D.SUB[r])
R.p("  (class, grade) counts over all sub-claims: " + str(dict(cnt)))
R.res["class_grade_counts"] = {f"{a}|{b}": n for (a, b), n in cnt.items()}
R.check("CITATION-AUDIT", "17 matrix rows, 12 columns, codes in {P,p*,F,U,N}", len(D.MATRIX) == 17 and all(len(v) == 12 and set(v) <= {"P", "p*", "F", "U", "N"} for v in D.MATRIX.values()))
# ---------------------------------------------------------------- 8 amendment-1 facts (pending batch now committed)
R.p("\n== 8. Amendment 1 facts: the pending Lean batch")
rcx, logx = C.git("log", "--format=%h %ad", "--date=short", "-1", "--", D.LEAN_DIR + "Dimension.lean")
R.p("  Dimension.lean first commit line: " + logx.strip())
dim = open(os.path.join(C.REPO, D.LEAN_DIR + "Dimension.lean"), encoding="utf-8").read()
for n in D.LEAN_DIMENSION_NAMES:
    R.check("CITATION-AUDIT", f"Lean Dimension.lean: {n}", n in dim)
vc = open(os.path.join(C.REPO, D.LEAN_DIR + "verify_chain.out"), encoding="utf-8", errors="replace").read()
R.check("CITATION-AUDIT", "verify_chain.out: 281 theorems, 0 non-standard axioms, 0 sorry, PASS", "theorems checked: 281; with non-standard axioms: 0; sorry mentions: 0" in vc and "VERIFY: PASS" in vc)
R.check("CITATION-AUDIT", "Dimension.lean states monomials only (SCOPE line)", "DIMENSIONAL ANALYSIS ON MONOMIALS" in dim)
third = re.findall(r"\(1 ?/ ?3\)|\^\(1/3\)|1 ?/ ?3 :", dim)
R.check("CITATION-AUDIT", "Dimension.lean has no statement of the Newtonian (G,M,H) -> M^(1/3) length", len(third) == 0, f"matches for a 1/3 exponent: {len(third)}; that half of R02a stays grade S")
R.write()
