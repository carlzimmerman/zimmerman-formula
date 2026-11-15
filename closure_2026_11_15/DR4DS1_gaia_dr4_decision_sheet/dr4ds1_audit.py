#!/usr/bin/env python3
"""DR4DS1 audit: every quotation in DR4_DECISION_SHEET.md is checked against the file it is taken from.

Each check asks two things: the quotation is in the sheet, and it is in its source file. Text is compared after
removing markdown asterisks and collapsing runs of whitespace, so a quotation may cross a line break in its source.
Three more checks read the release-day script and the sheet itself.

  python3 dr4ds1_audit.py            the audit
  python3 dr4ds1_audit.py --mutate   the mutation twin: every quotation is altered by one character and every
                                     check must then FAIL (so each check is shown to bite)

Computes nothing, runs no scorer, fetches nothing. Paths are relative to the repository root.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SHEET = HERE / "DR4_DECISION_SHEET.md"

MAP = "closure_2026_11_12/DR4MAP_gaia_dr4_registry_map/DR4_MAP.md"
PREP = "prep_2026/gaia_dr4_prep/"
DP3 = "dr4_push_2026_11_05/DP3_release_day/"
CFG816 = "campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/FROZEN_CRITERIA.md"

QUOTES = [
    (DP3 + "RELEASE_DAY_RUNBOOK_DR4.md", "none can be decided after the data"),
    (PREP + "OWNER_DECISION_2026-11-15_DR4_FORM_B_READING.md",
     "Form B's headline score on Gaia DR4 wide binaries is the 11-05 reading."),
    (PREP + "OWNER_DECISION_2026-11-15_DR4_FORM_B_READING.md",
     "The ruling of 2026-10-22 stands and no scorer is changed."),
    (PREP + "OWNER_DECISION_2026-11-05c_DR4_SEED_MEAN_NSS_OFF.md", "FILED 2026-11-08"),
    (DP3 + "dp3_sigma_sys.py", "OPTIONAL, default off (DP7, draft OWNER_DECISION_2026-11-05c, NOT FILED)"),
    (MAP, "about 70-80 min, 4.0-4.3 GB per fit"),
    (PREP + "OWNER_DECISION_2026-11-05c_DR4_SEED_MEAN_NSS_OFF.md",
     "that is the owner's call on release day, not decided here."),
    (PREP + "OWNER_DECISION_2026-11-05c_DR4_SEED_MEAN_NSS_OFF.md",
     "bias bound ~0.1 pair from the cones' own flag rate"),
    (MAP, "about 39,000 queries, about 47 h serial"),
    (CFG816, "the result is labelled CONTAMINATION-LIMITED, not KILLED"),
    (CFG816, "This makes a kill harder than a literal reading of CFG800"),
    (PREP + "PREREGISTRATION_DR4.md", "(canonical footing decides; alt footing reported)"),
    (PREP + "NOTE_2026-10-22_FORK_SCORING_PRE_DR4.md",
     "Canonical and alt are scored separately, never pooled; each footing gets its own verdict line."),
    (DP3 + "RELEASE_DAY_RUNBOOK_DR4.md",
     "On DR3 (information) it leaves canonical (b) at 0.0375 and moves alt from 0.0412 to 0.0350."),
    (DP3 + "RELEASE_DAY_RUNBOOK_DR4.md", "The RV-screened rung has no implementation anywhere."),
    (PREP + "OWNER_DECISION_2026-11-05b_DR4_D7_D8.md", "Option (a) adopted: σ_sys(b) stays as frozen"),
    (MAP, "the blend decision says labels are unchanged but records no wide-binary re-run"),
    (MAP, "so the record would print a kill and a survival for one result"),
    (PREP + "PREREGISTRATION_DR4.md", "The separation-resolved statistic — registered as the measurement of ξ."),
    (MAP, "no registration exists for the adopted theory"),
    (PREP + "PREREGISTRATION_DR4.md",
     "it is decided on release day, and recorded, whether those tables are also searched"),
    (MAP, "No filed amendment records the new hash."),
    (MAP, "still names Arm A as the DR4 front"),
    (DP3 + "RELEASE_DAY_RUNBOOK_DR4.md", "None of the tools logs in"),
]


def norm(text):
    return re.sub(r"\s+", " ", text.replace("*", "")).strip()


def read(rel):
    return norm((ROOT / rel).read_text(encoding="utf-8"))


def mutated(quote):
    """One character changed, in the middle of the quotation."""
    i = len(quote) // 2
    return quote[:i] + ("#" if quote[i] != "#" else "%") + quote[i + 1:]


def main():
    mutate = "--mutate" in sys.argv
    sheet = norm(SHEET.read_text(encoding="utf-8"))
    cache = {}
    results = []

    for rel, quote in QUOTES:
        if rel not in cache:
            cache[rel] = read(rel)
        q = norm(mutated(quote) if mutate else quote)
        ok = (norm(quote) in sheet) and (q in cache[rel])
        results.append((ok, f"quotation in the sheet and in {rel}: {quote[:60]}"))

    # The release-day script still has no seed-mean step (Q1). The twin looks for a string that is there.
    script = (ROOT / DP3 / "dr4_release_day.sh").read_text(encoding="utf-8")
    absent = ["dp3_sigma_sys.py"] if mutate else ["--nss-off-seed-mean", "dp7_seed_mean"]
    for needle in absent:
        results.append((needle not in script, f"dr4_release_day.sh does not contain {needle}"))
    if not mutate:
        results.append(("dp3_sigma_sys.py" in script, "dr4_release_day.sh calls dp3_sigma_sys.py"))

    # The sheet carries no home path. The twin looks for a string that is there.
    banned = ["DR4DS1"] if mutate else ["/Users/", "/home/"]
    for needle in banned:
        results.append((needle not in SHEET.read_text(encoding="utf-8"), f"the sheet does not contain {needle}"))

    if mutate:
        failed = sum(1 for ok, _ in results if not ok)
        for ok, label in results:
            print(("bites " if not ok else "MISSED") + "  " + label)
        print(f"mutation twin: {failed} of {len(results)} checks fail under the mutation")
        return 0 if failed == len(results) else 1

    passed = sum(1 for ok, _ in results if ok)
    for ok, label in results:
        print(("ok    " if ok else "FAIL  ") + label)
    print(f"audit: {passed} of {len(results)}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
