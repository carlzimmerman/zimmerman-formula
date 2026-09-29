#!/usr/bin/env python3
"""claims_audit_check.py -- independent mechanical check of campaign_fresh_gravity/closure_map/CLAIMS_AUDIT_2026-09-29.md.

Part V1: every quoted claim row `| line | `quote` | ...` under a document heading is looked up in that file AT HEAD (git show, not the
working tree) and must appear verbatim on the stated line (whitespace-normalised).  Part V2: numbers the audit's evidence table (E1-E16)
attributes to committed lane results are searched for in the cited lane's committed output.  Part V3 (control): a quote with one
character changed, and a number that is not in the output, must be REJECTED by the same code.
Editorial classes (REQUIRES-CORRECTION / SOFTEN / STILL-STANDS) are judgments and are NOT checked here.
Exit 0 = every quote verbatim at the audit's own commit, V2 as far as the audit claims it, and the V3 control behaves (drift at HEAD is reported, not failed).
"""
import re, subprocess, sys, os

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AUDIT = "campaign_fresh_gravity/closure_map/CLAIMS_AUDIT_2026-09-29.md"

def git_show(path, rev="HEAD"):
    r = subprocess.run(["git", "show", f"{rev}:{path}"], cwd=REPO, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None

AUDIT_COMMIT = subprocess.run(["git", "log", "--diff-filter=A", "--format=%h", "-1", "--", "campaign_fresh_gravity/closure_map/CLAIMS_AUDIT_2026-09-29.md"],
                              cwd=REPO, capture_output=True, text=True).stdout.strip()

norm = lambda s: re.sub(r"\s+", " ", s).strip()
doc = git_show(AUDIT)
assert doc, "audit not found at HEAD"

# ---------------- V1: quotes at file:line
cur = None
rows, seen_files = [], {}
for ln in doc.splitlines():
    m = re.match(r"^`([^`]+\.(?:tex|md|py|txt))`", ln)
    if m:
        cur = m.group(1)
    m = re.match(r"^\| (\d+) \| `(.+?)` \| ([^|]*) \| \*\*([A-Z-]+)\*\*", ln)
    if m and cur:
        rows.append((cur, int(m.group(1)), m.group(2), m.group(4)))
print(f"V1: {len(rows)} quote rows parsed under {len({r[0] for r in rows})} documents")
def check_rows(rev):
    bad_, missing_, cache = [], [], {}
    for f, n, q, cls in rows:
        txt = cache.setdefault(f, git_show(f, rev))
        if txt is None:
            missing_.append((f, n)); continue
        lines = txt.splitlines()
        if n > len(lines):
            bad_.append((f, n, q, "line beyond EOF")); continue
        if norm(q) not in norm(lines[n - 1]):
            joined = norm(lines[n - 1] + " " + (lines[n] if n < len(lines) else ""))   # a quote may wrap onto the next line
            if norm(q) not in joined:
                bad_.append((f, n, q, "quote not on that line"))
    return bad_, missing_, cache

bad, missing, seen_files = check_rows("HEAD")
bad_a, missing_a, _ = check_rows(AUDIT_COMMIT)
print(f"    at HEAD              : verbatim {len(rows) - len(bad) - len(missing)} / {len(rows)}   not found {len(bad)}   file missing {len(missing)}")
print(f"    at the audit commit {AUDIT_COMMIT}: verbatim {len(rows) - len(bad_a) - len(missing_a)} / {len(rows)}   not found {len(bad_a)}   file missing {len(missing_a)}")
for f, n, q, why in bad[:10]:
    still_at_audit = not any((f, n) == (b[0], b[1]) for b in bad_a)
    print(f"    HEAD MISMATCH {f.split('/')[-1]}:{n} ({why}); matched at the audit commit: {still_at_audit}")
for f, n in missing[:5]:
    print(f"    MISSING FILE {f} (line {n})")
touched = {f for f, n, q, w in bad}
for f in touched:
    r = subprocess.run(["git", "log", "--format=%h %s", f"{AUDIT_COMMIT}..HEAD", "--", f], cwd=REPO, capture_output=True, text=True).stdout.strip().splitlines()
    print(f"    {f.split('/')[-1]} edited after the audit commit by {len(r)} commits, e.g. {r[-1][:100] if r else '-'}")

# ---------------- V2: evidence-table numbers vs committed lane outputs
CF = "campaign_fresh_gravity/"
CHECKS = [  # (evidence id, output file at HEAD, [strings that must appear], note)
    ("E1", CF + "CFG55_sluggs_dynamical_masses.out", ["+0.097", "0.024", "+0.046"], "CFG55 SLUGGS with own JAM masses"),
    ("E2", CF + "CFG61_kids_colour_split.out", ["28.1", "2.1e-04"], "CFG61 chi2_S = 28.1/7, p = 2.1e-4"),
    ("E3", CF + "CFG67_lcdm_control_kids_split.out", ["6.5", "6.9"], "CFG67 LCDM control chi2 6.5/7, 6.9/7"),
    ("E4a", CF + "CFG59_universal_debris_fraction.out", ["NO"], "CFG59 no universal fraction"),
    ("E5", CF + "CFG58_rule_more_populations.out", ["-3.47", "-2.70"], "CFG58 LV field dwarfs"),
    ("E6a", CF + "CFG66_bootes_tucana_systematics.out", ["+0.219", "+0.465"], "CFG66 Bootes I +0.219 / Tucana II +0.465 (audit rounds to +0.22 / +0.47)"),
    ("E7", CF + "CFG56_super_spirals_bulge.out", ["+0.164"], "CFG56 nine fastest"),
    ("E11", CF + "CFG48_gap1_switch/G6_nonlocal_gate_stiffness.out", ["48"], "CFG48 G6 stability count"),
    ("E13", CF + "CFG47_unruh_matching/CFG47_unruh_matching.out", ["2.894"], "CFG47 kappa_match = sqrt(8pi/3)"),
]
print("\nV2: evidence numbers found in the cited lane's committed output")
missed = 0
for eid, path, needles, note in CHECKS:
    txt = git_show(path)
    if txt is None:
        print(f"    {eid:<4} {path}: FILE MISSING at HEAD"); missed += 1; continue
    absent = [s for s in needles if s not in txt]
    print(f"    {eid:<4} {'OK  ' if not absent else 'ABSENT'} {note}" + ("" if not absent else f"   not found: {absent}"))
    missed += bool(absent)

# ---------------- V3: control
ctl_q = rows[0][2][:-3] + "XYZ" if rows else "x"
f0, n0 = rows[0][0], rows[0][1]
lines0 = seen_files[f0].splitlines()
rej1 = norm(ctl_q) not in norm(lines0[n0 - 1])
rej2 = "999.999-not-a-number" not in (git_show(CHECKS[0][1]) or "")
print(f"\nV3 control: altered quote rejected: {rej1};  absent number rejected: {rej2}")

print(f"\nRESULT: quotes verbatim at the audit commit {len(rows) - len(bad_a) - len(missing_a)}/{len(rows)}, at HEAD {len(rows) - len(bad) - len(missing)}/{len(rows)}; evidence items with an absent number: {missed}; control ok: {rej1 and rej2}")
sys.exit(0 if (not bad_a and not missing_a and not missed and rej1 and rej2) else 1)
