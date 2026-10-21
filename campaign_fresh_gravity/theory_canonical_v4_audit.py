#!/usr/bin/env python3
"""Audit of THEORY_CANONICAL_2026-10-21_DRAFT.md (canonical v4 draft).

Checks, each printed as PASS/FAIL; exit status 1 on any FAIL:
  H  every 9-character commit hash cited in the draft is a commit in this repo (git cat-file -e <h>^{commit});
  L  every lane ID cited in the draft (CFGnnn or CFGnnn-An) has a LEDGER row, except the declared PENDING
     placeholders, which must have NO row of their own yet, must be named in the stated LEDGER row, and must be
     labelled PENDING in the draft;
  T  each hash in the section 4.4 table appears in that lane's LEDGER row;
  C  each class quoted in the section 4.4 table appears verbatim in that lane's LEDGER row;
  N  each headline number in NUMBERS appears verbatim in the draft AND in the named committed source (the lane's
     LEDGER row(s), else its README, else its results JSON; or the explicit file given);
  W  wording rules (kappa fitted; no positive "theory closed"; no positive "the data favour the framework";
     footings never pooled; no home paths or personal names; PENDING placeholders present).

MUTATE: `--mutate` additionally plants a fake hash, a fake lane ID and a wrong CFG829 number; it exits 1 when all
three are caught (the control bites), as the record's MUTATE runs do by design.

Sources are read from the committed tree (git show HEAD:<path>), never from uncommitted edits.
The draft itself is read from the working tree. Minus signs are normalised (U+2212 -> '-') before matching.
Read-only; single process; small memory. kappa = 1/2 FITTED; not theory closed.
"""
import glob
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DRAFT_NAME = "THEORY_CANONICAL_2026-10-21_DRAFT.md"
REPO = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
CFG_DIR_REL = os.path.relpath(HERE, REPO)  # campaign_fresh_gravity

RESULTS = []


def report(code, ok, msg):
    RESULTS.append(ok)
    print(f"{'PASS' if ok else 'FAIL'} [{code}] {msg}")


def norm(s):
    return s.replace("−", "-")


def git_show(rel):
    r = subprocess.run(["git", "-C", REPO, "show", f"HEAD:{rel}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def git_ls(rel_dir):
    r = subprocess.run(["git", "-C", REPO, "ls-tree", "--name-only", "HEAD", rel_dir + "/"],
                       capture_output=True, text=True)
    return r.stdout.split() if r.returncode == 0 else []


# ---------------------------------------------------------------- inputs
with open(os.path.join(HERE, DRAFT_NAME), encoding="utf-8") as fh:
    DRAFT = fh.read()
DRAFT_N = norm(DRAFT)
DRAFT_FLAT = re.sub(r"\s+", " ", DRAFT_N)

LEDGER_TXT = git_show(f"{CFG_DIR_REL}/LEDGER.md")
if LEDGER_TXT is None:
    print("FAIL [setup] LEDGER.md not readable at HEAD")
    sys.exit(1)
LEDGER = {}
for line in LEDGER_TXT.splitlines():
    if line.startswith("| "):
        cells = line.split("|")
        if len(cells) > 2:
            LEDGER.setdefault(cells[1].strip(), []).append(norm(line))


def lane_dirs(lane):
    m = re.match(r"CFG(\d+)", lane)
    if not m:
        return []
    return sorted(os.path.relpath(d, REPO) for d in glob.glob(os.path.join(HERE, f"CFG{m.group(1)}_*"))
                  if os.path.isdir(d))


def lane_texts(lane):
    """(label, text) pairs in priority order: LEDGER rows, README(s), results JSON."""
    out = [(f"LEDGER row {lane}", "\n".join(LEDGER.get(lane, [])))] if lane in LEDGER else []
    for d in lane_dirs(lane):
        t = git_show(f"{d}/README.md")
        if t is not None:
            out.append((f"{d}/README.md", norm(t)))
    for d in lane_dirs(lane):
        for f in git_ls(d):
            if f.endswith(".json"):
                t = git_show(f)
                if t is not None:
                    out.append((f, norm(t)))
    return out


def num_in(num, text):
    pat = r"(?<![0-9.])" + re.escape(norm(num)) + r"(?![0-9])"
    return re.search(pat, text) is not None


# ---------------------------------------------------------------- H: commit hashes
HASH_RE = re.compile(r"(?<![0-9A-Za-z])[0-9a-f]{9}(?![0-9A-Za-z])")
hashes = sorted({h for h in HASH_RE.findall(DRAFT) if re.search(r"[0-9]", h) and re.search(r"[a-f]", h)})
for h in hashes:
    r = subprocess.run(["git", "-C", REPO, "cat-file", "-e", f"{h}^{{commit}}"], capture_output=True)
    report("H", r.returncode == 0, f"commit {h} exists")

# ---------------------------------------------------------------- L: lane IDs
# PENDING placeholders: (LEDGER row that must name them, text that must appear in that row)
PENDING = {
    "CFG924": ("CFG920–929", "CFG924"),
}
lanes = sorted(set(re.findall(r"CFG\d+(?:-A\d+)?", DRAFT)), key=lambda x: (int(re.match(r"CFG(\d+)", x).group(1)), x))
for lane in lanes:
    if lane in PENDING:
        row_id, needle = PENDING[lane]
        report("L", lane not in LEDGER, f"{lane} is PENDING and has no LEDGER row of its own yet (a row means: fill it)")
        report("L", any(needle in r for r in LEDGER.get(row_id, [])), f"{lane} is named in LEDGER row {row_id} ('{needle}')")
        labelled = any(lane in ln and "PENDING" in ln for ln in DRAFT.splitlines())
        report("L", labelled, f"{lane} is labelled PENDING in the draft")
    else:
        report("L", lane in LEDGER, f"{lane} has a LEDGER row")

# ---------------------------------------------------------------- T, C: section 4.4 table
CLASSES = {
    "CFG838": ["NO TIDAL SIGNAL"], "CFG839": ["NO SIGNAL"], "CFG840": ["FRAGILE"], "CFG841": ["NOT DIAGNOSTIC"],
    "CFG842": ["MARGINAL"], "CFG843": ["SAME"], "CFG844": ["SUPPORTS"], "CFG845": ["H-PRIM EXCLUDED"],
    "CFG846": ["NO PATTERN"], "CFG847": ["LENSING = DYNAMICS AT TEST PRECISION"], "CFG848": ["WRONG SIGN", "ILL-POSED"],
    "CFG849": ["BOTH / DEGENERATE"], "CFG850": ["SPLIT SURVIVES"], "CFG851": ["DSPHS ABOVE"], "CFG852": ["NO SIGNAL"],
    "CFG853": ["EXCLUDED"], "CFG854": ["LINEAR SUFFICES"], "CFG855": ["ORDINARY"], "CFG856": ["SPARC-COMPATIBLE ONLY"],
    "CFG857": ["NO SIZE DEPENDENCE"], "CFG858": ["STIFFNESS ONLY SCREENS"], "CFG859": ["OVER-PREDICTS UFDs"],
    "CFG860": ["NOT GAS", "NO LAB CHANNEL"], "CFG861": ["PARTIAL"], "CFG870": ["JOINT FIT HOLDS"],
    "CFG871": ["LAW-LINKED CORE CONSISTENT"], "CFG872": ["FLOOR-LIKE"], "CFG873": ["UNDECIDED (GAS-SENSITIVE)"],
    "CFG874": ["UNDECIDED"], "CFG875": ["UNDECIDED"], "CFG876": ["BROKEN"], "CFG877": ["PARTIAL"],
    "CFG878": ["RECORD BATH EXCLUDED"], "CFG880": ["NOT UNIVERSAL"], "CFG881": ["PARTIAL"],
    "CFG882": ["RETENTION REQUIRES THE GATE"], "CFG883": ["MIXED"], "CFG884": ["CLUMP SHORT, EXTENDED MARGINAL"],
    "CFG885": ["SHIFTED, SAME CLASS"], "CFG886": ["5.364 RECOVERED", "NOT PINNED", "MIXED"],
    "CFG887": ["CFG880 STANDS"], "CFG888": ["LAW SOURCE = BARYONS ONLY", "NOT DERIVED"],
    "CFG889": ["INCONCLUSIVE as frozen", "CLUMP ERODED"], "CFG890": ["NONE WORKS; MASS-LIKE PREFERRED"],
    "CFG892": ["PARTIAL (reached: Carina)"], "CFG902": ["NO CLASS CHANGES"], "CFG903": ["PARTIAL"],
    "CFG909": ["ROBUST"], "CFG912": ["NOT ENVIRONMENT"], "CFG913": ["INFEASIBLE IN THE DECLARED CLASSES"],
    "CFG914": ["NO COMMON ORDERING"], "CFG915": ["CONTRADICTED"], "CFG916": ["CONTRADICTED", "UNDERDETERMINED"],
    "CFG917": ["SAFE ×3", "NOT DIAGNOSTIC", "CONSISTENT ×3"], "CFG918": ["BOUND ENVELOPE EXCLUDED"],
    "CFG919": ["SELECTOR CONTRADICTED", "FRAGILE"], "CFG920": ["UNDERDETERMINED"], "CFG921": ["NONE SURVIVES"],
    "CFG922": ["EXCESS STANDS"], "CFG923": ["CONTRADICTED", "UNDERDETERMINED"], "CFG925": ["NO EFFECT", "WORSENS"],
    "CFG926": ["NO EFFECT", "WORSENS", "PARTIAL", "RESOLVES the red-lens excess"], "CFG927": ["SEALED FORECAST"],
    "CFG928": ["SURVIVES", "FAIL", "UNDERDETERMINED"], "CFG929": ["none resolves it"],
}
sec = DRAFT.split("### 4.4", 1)[1].split("\n## ", 1)[0] if "### 4.4" in DRAFT else ""
report("T", bool(sec), "section 4.4 table found")
table_lanes = []
for ln in sec.splitlines():
    if not ln.startswith("| CFG"):
        continue
    cells = [c.strip() for c in ln.strip().strip("|").split("|")]
    lane, cls, hcell = cells[0], cells[2], cells[-1]
    table_lanes.append(lane)
    if lane in PENDING:
        report("C", "PENDING" in cls, f"{lane} table class reads PENDING")
        continue
    row = "\n".join(LEDGER.get(lane, []))
    hm = HASH_RE.search(hcell)
    if hm:
        report("T", hm.group(0) in row, f"{lane} table hash {hm.group(0)} is in its LEDGER row")
    for key in CLASSES.get(lane, []):
        report("C", key in cls and key in row, f"{lane} class '{key}' in table and in LEDGER row")
    if lane not in CLASSES:
        report("C", False, f"{lane} has no class entry in the audit's CLASSES table")
report("C", all(l in table_lanes for l in [f"CFG{n}" for n in range(913, 930) if n != 924] + ["CFG924"]),
       "section 4.4 lists every lane CFG913 to CFG929")

# ---------------------------------------------------------------- N: headline numbers
# (lane, number as written, source).  source None = lane's LEDGER row(s) -> README -> results JSON;
# "lanefile:<name>" = that committed file inside the lane directory; otherwise a repo-relative committed path.
C = CFG_DIR_REL
NUMBERS = [
    # section 1: law and inputs
    ("CFG650", "9.3603e-11", "lanefile:README.md"), ("CFG650", "1.1312e-10", "lanefile:README.md"),
    ("CFG835", "0.417", None), ("CFG835", "0.095", None), ("CFG835", "0.345", None), ("CFG835", "0.078", None),
    ("CFG835", "0.80", None), ("CFG835", "1.63", None), ("CFG835", "0.68470", None),
    ("CFG886", "5.272", None), ("CFG886", "0.218", None), ("CFG886", "6.122", None), ("CFG886", "0.321", None),
    ("CFG804", "0.10", None),
    ("CFG820", "24.0", None), ("CFG820", "24.7", None), ("CFG821", "22", None),
    ("CFG832", "2.04", None), ("CFG832", "2.14", None), ("CFG832", "0.1023", None), ("CFG832", "0.110", None),
    ("CFG882", "0.5", None), ("CFG889", "1e-2", None), ("CFG889", "105", None), ("CFG889", "148", None),
    ("CFG877", "7.53", None), ("CFG877", "5.3e6", None),
    ("CFG894", "439", None), ("CFG894", "0.20", None),
    ("CFG894", "451", f"{C}/CFG894_kappa_campaign_ledger/KAPPA_ATTEMPTS_LEDGER.md"),
    ("v2", "12/12", f"{C}/THEORY_CANONICAL_2026-10-16.md"),
    ("CFG638", "11/11", None),
    # section 0 / 2 / 3.7: supply and two-halo
    ("CFG903", "100.10", None), ("CFG903", "40.72", None), ("CFG903", "123.12", None), ("CFG903", "52.80", None),
    ("CFG902", "148.7", None), ("CFG902", "100.1", None),
    ("CFG926", "+0.127", None), ("CFG926", "+0.048", None), ("CFG926", "+0.088", None), ("CFG926", "+0.009", None),
    ("CFG926", "2.53", None), ("CFG926", "0.92", None),
    # section 3.1 rotators
    ("CFG828", "+0.05", None), ("CFG828", "0.07", None), ("CFG845", "+0.032", None), ("CFG845", "56", None),
    ("AG4g", "13 of 170", "argon_push/AG4g_galaxy_pull_census/README.md"),
    ("AG4h", "11 of 13", "argon_push/AG4h_pull_systematics/README.md"),
    # section 3.2 lensing
    ("CFG829", "1.016", None), ("CFG829", "0.086", None), ("CFG829", "2.75", None), ("CFG829", "20", None),
    ("CFG840", "0.90", None), ("CFG840", "1.31", None), ("CFG840", "12", None),
    ("CFG885", "18.4", None), ("CFG885", "21.3", None),
    # section 3.3 shear
    ("CFG909", "-0.94", None), ("CFG909", "-11.93", None), ("CFG909", "0.2806", None), ("CFG909", "0.3308", None),
    ("CFG654-A2", "-3.11", None), ("CFG654-A2", "-15.80", None), ("CFG654-A2", "-2.94", None),
    ("CFG654-A2", "144.68", None), ("CFG654-A2", "108", None), ("CFG654-A2", "0.024", None),
    ("CFG654-A2", "154.76", None), ("CFG654-A2", "0.008", None), ("CFG654-A2", "136.6", None),
    ("CFG654-A2", "0.949", None),
    # section 3.4 / 3.5 CMB lensing
    ("CFG917", "-0.0018", None), ("CFG917", "-0.0017", None), ("CFG917", "-0.0016", None),
    ("CFG917", "-0.276", None), ("CFG917", "-0.088", None), ("CFG917", "-0.085", None), ("CFG917", "+1.88", None),
    ("CFG927", "2.2", None), ("CFG927", "29", None), ("CFG927", "35", None), ("CFG927", "0.82", None),
    ("CFG927", "1.00", None), ("CFG927", "45", None), ("CFG927", "78", None), ("CFG927", "700", None),
    ("CFG927", "1000", None), ("CFG927", "2000", None), ("CFG927", "3000", None),
    # section 3.6 slip
    ("CFG847", "2.2e-8", None), ("CFG847", "3e-7", None), ("CFG847", "1.3e-6", None), ("CFG847", "1.9e-5", None),
    # section 3.7 partial
    ("CFG687", "1.01", None), ("CFG687", "0.09", None), ("CFG687", "0.93", None), ("CFG687", "0.08", None),
    ("CFG687", "0.90", None), ("CFG687", "0.21", None), ("CFG687", "0.47", None),
    ("CFG800", "1.15", None), ("CFG800", "1.20", None),
    # section 3.8 CFG689 (numbers from the committed cfg689_summary.md; K9 detail from the LEDGER row)
    ("CFG689", "0.913", "lanefile:cfg689_summary.md"), ("CFG689", "0.762", "lanefile:cfg689_summary.md"),
    ("CFG689", "1.027", "lanefile:cfg689_summary.md"), ("CFG689", "0.925", "lanefile:cfg689_summary.md"),
    ("CFG689", "1.048", "lanefile:cfg689_summary.md"), ("CFG689", "0.942", "lanefile:cfg689_summary.md"),
    ("CFG689", "0.706", "lanefile:cfg689_summary.md"), ("CFG689", "1.115", "lanefile:cfg689_summary.md"),
    ("CFG689", "0.909", "lanefile:cfg689_summary.md"), ("CFG689", "0.325", "lanefile:cfg689_summary.md"),
    ("CFG689", "1.212", "lanefile:cfg689_summary.md"), ("CFG689", "1.761", "lanefile:cfg689_summary.md"),
    ("CFG689", "1.987", "lanefile:cfg689_summary.md"), ("CFG689", "2.353", "lanefile:cfg689_summary.md"),
    ("CFG689", "3.490", "lanefile:cfg689_summary.md"), ("CFG689", "+0.227", "lanefile:cfg689_summary.md"),
    ("CFG689", "+0.272", "lanefile:cfg689_summary.md"), ("CFG689", "+0.316", "lanefile:cfg689_summary.md"),
    ("CFG689", "+0.453", "lanefile:cfg689_summary.md"), ("CFG689", "0.055", "lanefile:cfg689_summary.md"),
    ("CFG689", "0.072", "lanefile:cfg689_summary.md"), ("CFG689", "0.074", "lanefile:cfg689_summary.md"),
    ("CFG689", "0.084", "lanefile:cfg689_summary.md"), ("CFG689", "2.33", "lanefile:cfg689_summary.md"),
    ("CFG689", "11.11/5", "lanefile:cfg689_summary.md"), ("CFG689", "1.97", "lanefile:cfg689_summary.md"),
    ("CFG689", "2.10", "lanefile:cfg689_summary.md"), ("CFG689", "+0.011", "lanefile:cfg689_summary.md"),
    ("CFG689", "-0.037", "lanefile:cfg689_summary.md"), ("CFG689", "+0.059", "lanefile:cfg689_summary.md"),
    ("CFG689", "0.100", "lanefile:cfg689_summary.md"), ("CFG689", "0.0392", "lanefile:cfg689_summary.md"),
    ("CFG689", "0.00039", "lanefile:cfg689_summary.md"), ("CFG689", "3.45", "lanefile:cfg689_summary.md"),
    ("CFG689", "67.70", "lanefile:cfg689_summary.md"), ("CFG689", "67.09", "lanefile:cfg689_summary.md"),
    ("CFG689", "68.31", "lanefile:cfg689_summary.md"), ("CFG689", "9.352e-11", "lanefile:cfg689_summary.md"),
    ("CFG689", "1.24", None), ("CFG689", "9e-6", None),
    ("CFG689", "0.13", "lanefile:HANDOFF_TO_ORCHESTRATOR.md"),
    # section 4 excess family
    ("CFG827", "25", None), ("CFG827", "28", None), ("CFG827", "+0.38", None),
    ("CFG828", "21", None), ("CFG828", "+0.44", None),
    ("CFG843", "+0.055", None), ("CFG843", "0.117", None),
    ("CFG874", "+0.194", None), ("CFG874", "0.077", None), ("CFG874", "-0.100", None), ("CFG874", "0.091", None),
    ("CFG880", "0.380", None), ("CFG884", "6.4e8", None), ("CFG884", "1.67", None), ("CFG925", "+0.48", None),
    ("CFG892", "3.41", None), ("CFG892", "3.48", None), ("CFG892", "3.27", None),
    ("CFG892", "7.81", None), ("CFG892", "7.40", None), ("CFG892", "4.88", None),
    ("CFG850", "+0.123", None), ("CFG850", "4.0", None), ("CFG850", "1.45", None), ("CFG850", "1.02", None),
    ("CFG912", "0.064", None), ("CFG912", "0.067", None), ("CFG811", "+0.013", None), ("CFG811", "+0.280", None),
    ("CFG687", "1.91", None), ("CFG687", "0.12", None), ("CFG687", "1.75", None), ("CFG687", "0.11", None),
    ("CFG922", "2.24", None), ("CFG922", "1.84", None), ("CFG922", "+5.2", None), ("CFG922", "+4.3", None),
    ("CFG922", "0.5", None), ("CFG815", "1.64", None), ("CFG815", "+4.6", None),
    ("CFG916", "1.91", None), ("CFG916", "1.75", None),
    # section 6 dated tests
    ("CFG571", "9.1", None), ("CFG571", "10.7", None), ("CFG571", "8.3", None), ("CFG571", "200", None),
    ("10-14", "1.42", f"{C}/THEORY_CANONICAL_2026-10-14.md"), ("10-14", "2.0", f"{C}/THEORY_CANONICAL_2026-10-14.md"),
    ("10-14", "12-02", f"{C}/THEORY_CANONICAL_2026-10-14.md"),
    ("CFG740", "8.9e-4", None), ("CFG740", "50", None), ("CFG740", "5.754", None), ("CFG820", "17", None),
    ("CFG800", "0.01", None),
    ("CFG672", "1.08", None), ("CFG672", "1.09", None), ("CFG672", "0.3", None),
    ("CFG673", "26.4", None), ("CFG673", "29.6", None), ("CFG673", "29.8", None),
    ("CFG673", "30.8", None), ("CFG673", "31.0", None),
    # section 7 wording
    ("CFG908", "200", None), ("CFG908", "142", None), ("CFG904", "0.4607", None),
]


def resolve(lane, src):
    if src is None:
        return lane_texts(lane)
    if src.startswith("lanefile:"):
        out = []
        for d in lane_dirs(lane):
            t = git_show(f"{d}/{src.split(':', 1)[1]}")
            if t is not None:
                out.append((f"{d}/{src.split(':', 1)[1]}", norm(t)))
        return out
    t = git_show(src)
    return [(src, norm(t))] if t is not None else []


for lane, num, src in NUMBERS:
    in_draft = num_in(num, DRAFT_N)
    hit = None
    for label, text in resolve(lane, src):
        if num_in(num, text):
            hit = label
            break
    ok = in_draft and hit is not None
    where = hit if hit else "NOT FOUND in source"
    report("N", ok, f"{lane} '{num}': draft {'yes' if in_draft else 'NO'}; source {where}")

# ---------------------------------------------------------------- W: wording
report("W", "κ = ½ FITTED" in DRAFT, "draft states 'κ = ½ FITTED'")
bad = [m.start() for m in re.finditer(r"theory closed", DRAFT_FLAT)
       if not re.search(r"(not|never|Never|Not)\W[^.]{0,20}$", DRAFT_FLAT[max(0, m.start() - 24):m.start()])]
report("W", not bad, f"every 'theory closed' is negated ({len(bad)} positive uses)")
bad = [m.start() for m in re.finditer(r"favour the framework", DRAFT_FLAT)
       if not re.search(r"(never|Never|not|Not|Nothing|nothing|cannot)", DRAFT_FLAT[max(0, m.start() - 45):m.start()])]
report("W", not bad, f"every 'favour the framework' is negated ({len(bad)} positive uses)")
report("W", "never pooled" in DRAFT and not re.search(r"footings? (?:are |were )?pooled", DRAFT),
       "footings stated as never pooled")
report("W", not re.search(r"/Users/|/home/", DRAFT), "no home paths")
for ph, h in [("P1. NC2x", "8e1f1763c"), ("P2. CFG928", "82a69be8f"), ("P3. CFG929", "1f1b87ce8")]:
    seg = DRAFT.split(ph, 1)[1][:200] if ph in DRAFT else ""
    report("W", "FILLED" in seg and h in seg, f"placeholder '{ph}' FILLED from {h} (2026-10-21)")
seg = DRAFT.split("P5. CFG924", 1)[1][:200] if "P5. CFG924" in DRAFT else ""
report("W", "PENDING (fill when committed)" in seg, "placeholder 'P5. CFG924' marked 'PENDING (fill when committed)'")
report("W", "max(0.01, 3σ_R)" in DRAFT, "DR4 row states the restated kill line (owner decision 2026-10-21)")
report("W", "P4. CFG689" in DRAFT and "6c064b83a" in DRAFT, "CFG689 placeholder filled from 6c064b83a")

n_pass = sum(RESULTS)
n_fail = len(RESULTS) - n_pass
print(f"\nSUMMARY: {n_pass} PASS, {n_fail} FAIL ({len(hashes)} hashes, {len(lanes)} lane IDs, {len(NUMBERS)} numbers)")

if "--mutate" in sys.argv:
    # Planted errors: each check must reject its plant. Exit 1 when all three are caught (the control bites),
    # as the record's MUTATE runs do by design.
    caught = 0
    r = subprocess.run(["git", "-C", REPO, "cat-file", "-e", "abc123def^{commit}"], capture_output=True)
    caught += r.returncode != 0
    caught += "CFG99999" not in LEDGER
    caught += not any(num_in("1.017", t) for _, t in lane_texts("CFG829"))
    print(f"MUTATE: planted errors caught {caught}/3 (fake hash, fake lane ID, CFG829 1.016 -> 1.017)"
          f" -> {'BITES' if caught == 3 else 'DOES NOT BITE'}")
    sys.exit(1 if caught == 3 else 0)

sys.exit(1 if n_fail else 0)
