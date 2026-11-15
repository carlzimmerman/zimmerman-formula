#!/usr/bin/env python3
"""BCS1 audit: every quoted word in BOUNDED_CLOSURE_STATEMENT.md must appear verbatim in the committed file it cites.

Cited files are read with `git show HEAD:<path>` (paths relative to the repository root); a quotation of a file
as it stood at an earlier commit names that commit, by its id on origin. Text is compared after
removing markdown bold markers, unescaping table pipes and collapsing whitespace, so line wraps do not matter. Checks:
  1. each listed quotation is in its committed file and in the statement;
  2. every double-quoted passage of the statement is covered by a listed quotation (nothing is quoted unchecked);
  3. the row lists the statement gives for the scorecard's words match the scorecard's table;
  4. the statement at the commit the owner's decision of 2026-11-15 names has the sha256 that decision pins;
  5. no home path and no banned name in this folder's files or the two decision files; the statement ends with the
     required line.
Exit 0 only if every check passes. Run: python3 -I -B bcs1_audit.py > bcs1_audit.out

Mutation twin: python3 -I -B bcs1_audit.py --mutate > bcs1_audit_MUTATE.out changes one character of every listed
quotation and must find none of them in its committed file (exit 0 when every mutated quotation is rejected).
"""
import hashlib
import os
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                      check=True).stdout.strip()
HERE = "closure_2026_11_15/BCS1_bounded_closure_statement"
STATEMENT = "BOUNDED_CLOSURE_STATEMENT.md"
END_LINE = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
C14 = "closure_2026_11_14/"
C13 = "closure_2026_11_13/"
C12 = "closure_2026_11_12/"
C11 = "closure_2026_11_11/"
C09 = "closure_2026_11_09/"
CJ1 = C13 + "CJ1_candidate_completion/"
CARD = CJ1 + "SCORECARD.md"
FORM = CJ1 + "COMPLETED_FORM.md"
P72 = "qwen_claude_field_theory/papers_2026/PAPER72_law_with_cold_dark_energy_counted_once_2026"
TEX = P72 + ".tex"
KILL = "closure_2026_11_07/PREDICTIONS_2026_11_07.md"
DR4 = C12 + "DR4MAP_gaia_dr4_registry_map/DR4_MAP.md"
PRED = "predictions_2026/PREDICTIONS_SCORECARD_2026-11-12.md"
OWN = C09 + "OWNER_DECISION_2026-11-09_FINAL_FORM_B.md"
WLJ2 = C14 + "WLJ2_power_and_lensing_amplitude_exact_junction/RESULT.md"

OWNDEC = "closure_2026_11_15/OWNER_DECISION_2026-11-15_BOUNDED_CLOSURE_STATEMENT.md"

DR4DEC = "prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-15_DR4_FORM_B_READING.md"
CARD_AS_WRITTEN = "b3eb4c89b5"  # origin id of the scorecard commit this statement was written against
# the later note of 2026-11-15: the Gaia DR4 gaps, the check under the blend, the DR4 record and the deposit decision
DR4DEC2 = "prep_2026/gaia_dr4_prep/OWNER_DECISION_2026-11-15b_DR4_OPEN_GAPS.md"
CQB1R = "closure_2026_11_15/CQB1_cq2_under_blend/RESULT.md"
DR4REC = "closure_2026_11_15/DR4REC1_gaia_dr4_predata_record/DR4REC1_gaia_dr4_predata_record_2026.zenodo.json"
DEPDEC = "closure_2026_11_15/OWNER_DECISION_2026-11-15b_CLOSURE_STATEMENT_DEPOSIT.md"

# (committed path, quoted word) or (committed path, quoted word, commit to read the file at)
CHECKS = [
    (DR4DEC2, "Accept all recommended"),
    (CQB1R, "MARGIN HOLDS, UNCHANGED"),
    (DR4REC, "10.5281/zenodo.24248715"),
    (DEPDEC, "Should PAPER72 v1.7 carry the closure statement (BCS1)?"),
    (DEPDEC, "Yes, include it"),
    (DR4DEC, "Which reading should be the headline score for form B on Gaia DR4?"),
    (DR4DEC, "The 11-05 rows"),
    (CARD, "The audit reads 189 of 189."),
    (CARD, "As published, the rise excludes the law on both footings."),
    (CARD, "STILL FAILS [non-cool-core clusters, 0.1-0.5 R500: over-predicts] FRAGILE."),
    (CARD, "STILL FAILS [beta_z HIGH] FRAGILE"),
    (CARD, "182 of 182"),
    (OWNDEC, "Should this stand as the record's closure statement?"),
    (OWNDEC, "Yes, adopt it"),
    (P72 + ".zenodo.json", "10.5281/zenodo.24246863"),
    (CJ1 + "cj1_audit.out", "182 of 182 checks pass", CARD_AS_WRITTEN),
    (P72 + ".zenodo.json", "10.5281/zenodo.24231666"),
    (OWN, "Form B is the form the record closes on."),
    (OWN, "It is chosen as a form, not as a pass."),
    (C12 + "KAP1_kappa_new_routes/RESULT.md", "KAPPA NOT DERIVED"),
    (C12 + "OUT4_kappa_window/RESULT.md", "KAPPA NOT DERIVED (FITTED)"),
    (FORM, "kappa = 1/2 and X = 5.41 are fitted."),
    (FORM, "(The hot branch is a rule, not a solution of the action.)"),
    (TEX, "FAILS at the forest's own redshifts"),
    (TEX, "an independent blind build FAILS (8142/7686)"),
    (CARD, "The full law layout is dead at flux level."),
    (C09 + "PD1_phantom_is_dust/RESULT.md", "PASS: rms 0.0563 (line 0.0660)"),
    (CARD, "A pass of the law, not of rule 6."),
    (C11 + "DW1_desi_dr2_mw_mass/RESULT.md", "9 of 12"),
    (CARD, "The extrapolated M200c fails."),
    (KILL, "Power: weak."),
    (CARD, "Linear content is the cold reference; the share is fitted to the CMB."),
    (CARD, "With fragile power only, and none confirmed by an independent blind re-grade"),
    (CARD, "Canonical: EQUALS THE LAW 14; NOT GRADED FOR THIS FORM 6; NO POWER 8; FAILS 2; PASSES TRIVIALLY 5; "
           "DEPENDS ON AN UNTESTED ASSUMPTION 6; PASSES 3; FAILS ON COVERAGE ONLY 1. Total 45."),
    (CARD, "Alt: EQUALS THE LAW 14; NOT GRADED FOR THIS FORM 6; NO POWER 8; FAILS 2; PASSES TRIVIALLY 5; "
           "DEPENDS ON AN UNTESTED ASSUMPTION 6; PASSES 3; FAILS ON COVERAGE ONLY 1. Total 45."),
    (C14 + "OTA1_outer_share_to_turnaround/RESULT.md", "STILL FAILS / STILL FAILS (canonical / alt)"),
    (CARD, "0.743 / 0.781 and 0.943 / 0.981 dex below"),
    (C14 + "RB2R_blind_low_rows/RESULT_BLIND.md", "LOW ROWS COUNT AGAINST B"),
    (CARD, "Rule 6 does not touch them: form B's fail stays."),
    (C14 + "XJ1_exact_junction_zero_velocity_surface/RESULT.md", "THE HOLD DOES NOT SURVIVE THE EXACT JUNCTION"),
    (C13 + "JNT2_crossing_speed_joint/RESULT.md", "JOINT FAILS ON G2 (coverage)"),
    (C13 + "JNT2R_blind_crossing_speed_joint/RESULT_BLIND.md", "JOINT FAILS ON G2 (coverage)"),
    (C14 + "XJ1R_blind_caustic_junction/RESULT_BLIND.md", "CAUSTIC 3 HOLDS, BLIND, FRAGILE (lam_x0.5)"),
    (C14 + "CSD1_charge_delivery_at_the_caustic/RESULT.md", "SHORT AT CAUSTIC 2 / SHORT AT CAUSTIC 3"),
    (C14 + "BJ1_charge_budget_junction/RESULT.md", "FAILS THE FOREST (caustic 3)"),
    (WLJ2, "the exact junction WORSENS it, on both footings"),
    (TEX, "So far no layout graded here meets all three of"),
    (C09 + "CO2_form_b_amplitude_pinned/RESULT.md", "AMPLITUDE EXCLUDED BY RAW KiDS AT 3 SIGMA"),
    (CARD, "The tension is the one any cold component fitted to the CMB carries, and the split does not relieve it."),
    (TEX, "a consistency check, not a pass"),
    (WLJ2, "ROW FAILS WITH THE EXACT JUNCTION"),
    (PRED, "No registered prediction has come true."),
    (PRED, "41 not yet tested, 20 post-dictions, 14 retired or withdrawn, 17 undecided, 12 failed, 11 consistent but "
           "not distinctive, 0 came true"),
    (FORM, "DPR1 found no dated distinctive prediction for form B as adopted"),
    (FORM, "This is an algebraic speed intersection, not a derivation of a transition"),
    (TEX, "the equations give no answer beyond that moment"),
    (TEX, "The standing state exists."),
    (TEX, "the flow brings one to twelve per cent of the charge, and the action has no other channel in the weak "
          "field"),
    (TEX, "reads NO CANDIDATE on both footings"),
    (FORM, "What is not derived"),
    (KILL, "Screened (medium-first) excluded iff γ̂ − 1.000 ≥ 3σ, and γ̂ is not below the law-first anchor "
           "by ≥ 3σ."),
    (DR4, "A Newtonian sky is survival for the adopted theory, never confirmation."),
    (DR4, "C2. Which registered wide-binary reading belongs to form B?"),
    (TEX, "a census that falls short falsifies it"),
    (C09 + "RB1_form_b_hot_systems/RESULT.md", "1.095 [0.885, 1.259]"),
    (C13 + "EUC17_mask_aperture_mass_reread/RESULT.md", "+0.192 [+0.079, +0.338] / +0.174 [+0.061, +0.322]"),
    (KILL, "RIVAL FAVOURED (|d_R| ≤ 2 and d_T ≥ 3) or NEITHER (|d_T| > 3 and |d_R| > 3) at a powered z*"),
    (KILL, "Nobody, on the present record."),
    (KILL, "FAIL iff D1 is more than 2σ_tot from 1, or D2 is more than 3σ_tot from 1."),
    (TEX, "A SURVIVES is a hit and a KILLED reading counts only after an independent blind re-grade"),
    (TEX, "What would decide the joint now is an equation for what the clock is behind a fold"),
    (CARD, "no data row can grade them; a derivation would."),
    (TEX, "The candidate is NOT ADOPTED. The theory is not closed."),
]

# statements about the scorecard's table that carry no quotation: word -> rows the statement lists for it
ROW_LISTS = {
    "FAILS": [20, 36],
    "PASSES": [11, 22, 37],
    "DEPENDS ON AN UNTESTED ASSUMPTION": [8, 15, 19, 27, 28, 40],
    "NO POWER": [6, 7, 9, 10, 17, 18, 25, 35],
    "FAILS ON COVERAGE ONLY": [5],
}
# passages in double quotes that are not quotations of a file (a term being defined)
NOT_QUOTATIONS = {"bounded"}


def norm(text):
    text = text.replace("**", "").replace("\\|", "|")
    return re.sub(r"\s+", " ", text).strip()


def show(path, rev="HEAD"):
    r = subprocess.run(["git", "show", rev + ":" + path], capture_output=True, cwd=ROOT)
    if r.returncode != 0:
        return None
    return r.stdout.decode("utf-8", errors="replace")


def mutate(quote):
    """Change the last letter or digit of the quotation."""
    for i in range(len(quote) - 1, -1, -1):
        ch = quote[i]
        if ch.isdigit():
            return quote[:i] + str((int(ch) + 1) % 10) + quote[i + 1:]
        if ch.isalpha() and ch.isascii():
            return quote[:i] + ("x" if ch.lower() != "x" else "y") + quote[i + 1:]
    return quote + " x"


def main_mutate():
    cache = {}
    out = []
    rejected = 0
    for path, quote, rev in [(c + ("HEAD",))[:3] for c in CHECKS]:
        if (path, rev) not in cache:
            cache[(path, rev)] = show(path, rev)
        src = cache[(path, rev)]
        q = norm(mutate(quote))
        short = q if len(q) <= 70 else q[:67] + "..."
        bites = src is not None and q not in norm(src)
        rejected += bool(bites)
        out.append(("BITES " if bites else "MISSED ") + "\"%s\" not in %s" % (short, path))
    for ln in out:
        print(ln)
    print("%d of %d mutated quotations are rejected" % (rejected, len(CHECKS)))
    print(END_LINE)
    return 0 if rejected == len(CHECKS) else 1


def main():
    lines = []
    ok_all = True

    def report(ok, msg):
        nonlocal ok_all
        ok_all = ok_all and bool(ok)
        lines.append(("PASS " if ok else "FAIL ") + msg)

    with open(os.path.join(ROOT, HERE, STATEMENT), encoding="utf-8") as fh:
        raw = fh.read()
    stmt = norm(raw)

    cache = {}
    for path, quote, rev in [(c + ("HEAD",))[:3] for c in CHECKS]:
        if (path, rev) not in cache:
            cache[(path, rev)] = show(path, rev)
        src = cache[(path, rev)]
        q = norm(quote)
        short = q if len(q) <= 70 else q[:67] + "..."
        where = path if rev == "HEAD" else "%s at %s" % (path, rev)
        if src is None:
            report(False, "src   %s: not committed" % where)
            continue
        report(q in norm(src), "src   \"%s\" in %s" % (short, where))
        if quote.startswith("Alt: "):
            continue  # the statement prints the canonical line and says the alt line is the same
        report(q in stmt, "here  \"%s\" in %s" % (short, STATEMENT))

    # every double-quoted passage in the statement is covered by a listed quotation
    listed = [norm(c[1]) for c in CHECKS]
    for passage in re.findall(r"\"([^\"]+)\"", stmt):
        p = passage.strip()
        if p in NOT_QUOTATIONS:
            continue
        covered = any(p in q or q in p for q in listed)
        short = p if len(p) <= 70 else p[:67] + "..."
        report(covered, "cover \"%s\" is a listed quotation" % short)

    # the scorecard's table: completed-form word per row
    card = cache.get((CARD, "HEAD")) or show(CARD)
    rows = {}
    for ln in (card or "").splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|", ln)
        if m:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 6:
                rows[int(m.group(1))] = cells[5]
    report(len(rows) == 45, "scorecard table has 45 rows (found %d)" % len(rows))
    for word, want in ROW_LISTS.items():
        got = sorted(r for r, w in rows.items() if w == word)
        report(got == want, "rows that read %s in the scorecard are %s (statement lists %s)" % (word, got, want))
        for r in want:
            report(re.search(r"\b%d\b" % r, stmt) is not None, "row %d is named in the statement" % r)

    # the adopted text is the one the owner's decision pins
    dec = cache.get((OWNDEC, "HEAD")) or show(OWNDEC) or ""
    m = re.search(r"committed in ([0-9a-f]{10}) \(on origin ([0-9a-f]{10})\), sha256 ([0-9a-f]{64})", norm(dec))
    if m is None:
        report(False, "the owner's decision names a commit, its origin id and a sha256 for the adopted text")
    else:
        got = "unreadable"
        for rev in (m.group(2), m.group(1)):  # the origin id first: a clone of origin has no local-only id
            r = subprocess.run(["git", "show", "%s:%s/%s" % (rev, HERE, STATEMENT)], capture_output=True, cwd=ROOT)
            if r.returncode == 0:
                got = hashlib.sha256(r.stdout).hexdigest()
                break
        report(got == m.group(3), "the statement at %s has the sha256 the owner's decision pins" % rev)

    # folder hygiene
    for name in (HERE + "/" + STATEMENT, HERE + "/bcs1_audit.py", OWNDEC, DR4DEC):
        with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
            t = fh.read()
        low = t.lower()
        bad = [s for s in ("/" + "users/", "/" + "private/", "cold " + "dark matter", "cdm" + "-like") if s in low]
        report(not bad, "%s: no home path and no banned name (found: %s)" % (name, bad or "none"))
    report(raw.rstrip().splitlines()[-1] == END_LINE, "%s ends with the required line" % STATEMENT)

    for ln in lines:
        print(ln)
    passed = sum(1 for ln in lines if ln.startswith("PASS"))
    print("%d of %d checks pass" % (passed, len(lines)))
    print(END_LINE)
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main_mutate() if "--mutate" in sys.argv[1:] else main())
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
