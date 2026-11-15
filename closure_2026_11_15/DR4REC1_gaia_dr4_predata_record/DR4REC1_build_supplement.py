#!/usr/bin/env python3
"""DR4REC1: build the archive of the Gaia DR4 pre-data record, as one zip with a manifest.

The archive holds, as committed, every file a reader needs to check what was registered for Gaia DR4 wide binaries
before the data, and to run the scoring on the day: the pre-registration and its amendments, the owner decisions, the
sealed predictions, the release-day tools and their lanes, the registry map and the sources of its other entries, the
decision sheet and the pre-data check of the sealed prediction under the adopted stiffness.

Only tracked files go in, read from the working tree, and the build refuses unless:
  - every listed path exists and is tracked;
  - the working tree copy of every file equals the committed copy (git diff is empty for the listed paths);
  - the committed copy equals origin/main's copy, so the archive is what the public repository holds;
  - no file path or file content of a text file carries a home-directory path.
The zip is deterministic: entries sorted, fixed timestamp, fixed permissions.

  python3 DR4REC1_build_supplement.py          build the zip and the manifest next to this script
  python3 DR4REC1_build_supplement.py --list   print the file list and sizes only

kappa = 1/2 FITTED; footings never pooled; not theory closed. Nothing here says the data favour the framework.
"""
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ZIP = HERE / "DR4REC1_gaia_dr4_predata_archive_2026.zip"
MAN = HERE / "DR4REC1_archive_manifest.json"

# Folders are taken whole (tracked files only); single files are named one by one.
ENTRIES = [
    # the pre-registration, its 22 amendments, the fork-scoring note, the owner decisions, the frozen pipeline and builder
    "prep_2026/gaia_dr4_prep",
    # the release-day lanes DP1 onward: rung, forecast, wrapper and runbook, fetchers, cut-12 wiring, seed mean, path wiring
    "dr4_push_2026_11_05",
    # the sealed prediction of the adopted theory, and the two seals printed beside it as information
    "cq_lanes_2026_11_04/CQ2_v3s_dr4_seal",
    "cw_lanes_2026_11_04/CW1_wide_binary_seal_dr4",
    "finish_2026_11_04/FN6_powerlaw_screening",
    # the fork rows' lane, the R statistic and its seals, the readiness lanes, the kill-line note
    "doors_push_2026_10_22/D2_wide_binary_fork",
    "campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring",
    "campaign_fresh_gravity/CFG740_sealed_wb_slope2",
    "campaign_fresh_gravity/CFG800_wb_2026_scoring",
    "campaign_fresh_gravity/CFG943_dr4_readiness",
    "campaign_fresh_gravity/CFG239_dr4_seed_noise_referee",
    "campaign_fresh_gravity/CFG239_FROZEN_CRITERIA.md",
    "campaign_fresh_gravity/OWNER_DECISION_2026-10-21_DR4_KILL_LINE.md",
    "campaign_fresh_gravity/DR4_OUTCOME_MAP_2026-10-15.md",
    "campaign_fresh_gravity/DR4_R_STATISTIC_CRITERIA_DRAFT_2026-10-15.md",
    # the registry map, the decision sheet, the check of the sealed prediction under the adopted stiffness, this record
    "closure_2026_11_12/DR4MAP_gaia_dr4_registry_map",
    "closure_2026_11_15/DR4DS1_gaia_dr4_decision_sheet",
    "closure_2026_11_15/CQB1_cq2_under_blend",
    # what the check of the sealed prediction pins as inputs, and the stiffness decision it tests
    "action_search_2026_11_05/AC21_smooth_3d/iter_6_fast_decay/form.json",
    "rebuild_2026_10_22/X3_switched_stiffness/x3_switched_stiffness_results.json",
    "closure_2026_11_07/OWNER_DECISION_2026-11-07_ADOPT_PI6_BLEND.md",
    "closure_2026_11_07/PI6_BLEND_ADOPTION_CASE_2026_11_07.md",
    "closure_2026_11_07/QX17D_blend_field_equations",
    # the adoption chain the map quotes, the frozen kill lines, the review and the predictions scorecard
    "finish_2026_11_04/FN1_action_call/OWNER_DECISION_2026-11-04_ADOPT_V3S_SCOPED.md",
    "closure_2026_11_09/OWNER_DECISION_2026-11-09_FINAL_FORM_B.md",
    "closure_2026_11_07/PREDICTIONS_2026_11_07.md",
    "reviews/GAIA_DR4_DEEP_REVIEW_2026-11-05.md",
    "predictions_2026/PREDICTIONS_SCORECARD_2026-11-12.md",
    # the separation-resolved statistic of Amendment 14(c)
    "real_research/cross_thread_review_2026_09_26/XR22_prereg_statistic.py",
    "real_research/cross_thread_review_2026_09_26/XR22_prereg_statistic.out",
    "real_research/cross_thread_review_2026_09_26/XR22_prereg_statistic_MUTATE.out",
    "real_research/cross_thread_review_2026_09_26/XR22_prereg_statistic_results.json",
    "real_research/cross_thread_review_2026_09_26/XR22_prereg_statistic_results_MUTATE.json",
    # the map's other registered entries: information rows and Milky Way rows, none scored for the adopted theory
    "campaign_fresh_gravity/CFG553_sealed_gaia_dr4_predictions",
    "rebuild_2026_10_22/S3_v3_mw_seals",
    "rebuild_2026_10_22/GD1_route_e_mw_dr4",
    "rebuild_2026_10_22/KT20_filter_wide_binaries",
    "deepseek_push/FALSIFIER_MATRIX.md",
    "deepseek_push/PREDICTIONS.md",
    "deepseek_push/DR4_AMENDMENT_12.md",
    "deepseek_push/dr4_scorer.py",
    "glm53_push/G018_dr4_binned_prediction.py",
    # the standing file, for its dated DR4 addendum
    "STANDING.md",
]

# Files allowed to carry a home-directory path, each with its reason. They go in byte for byte.
ALLOW_HOME = {
    "prep_2026/gaia_dr4_prep/wide_binary_pipeline.py":
        "the frozen pipeline, pinned by sha256 in the release-day wrapper; its one default data path (ELBADRY) is an "
        "absolute path of the author's machine and cannot be edited before the data without breaking the pin",
}

# This record's own built files are not put inside its own archive.
SELF = "closure_2026_11_15/DR4REC1_gaia_dr4_predata_record"
TEXT_EXT = {".md", ".py", ".txt", ".json", ".sh", ".out", ".csv", ".tex", ".lean", ".adql", ".toml", ".yaml", ".yml", ".log", ".time"}


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=True).stdout


def resolve():
    tracked = git("ls-files", "-z").split("\0")
    tracked = [p for p in tracked if p]
    tset = set(tracked)
    files = []
    for e in ENTRIES:
        if e in tset:
            files.append(e)
            continue
        under = [p for p in tracked if p.startswith(e + "/")]
        if not under:
            sys.exit(f"REFUSED: listed entry is not a tracked file or folder: {e}")
        files.extend(under)
    files = sorted(set(f for f in files if not f.startswith(SELF + "/")))
    return files


def main():
    files = resolve()
    if "--list" in sys.argv:
        total = sum((ROOT / f).stat().st_size for f in files)
        for f in files:
            print(f)
        print(f"{len(files)} files, {total / 1e6:.2f} MB before compression")
        return 0

    # Untracked files in the listed folders (scratch outputs, ignored data) are not in the archive and are not looked at.
    dirty = git("status", "--porcelain", "--untracked-files=no", "--", *ENTRIES).strip()
    if dirty:
        sys.exit("REFUSED: tracked files under the listed paths differ from the commit:\n" + dirty[:1500])
    git("fetch", "-q", "origin", "main")
    differs = git("diff", "--name-only", "HEAD", "origin/main", "--", *ENTRIES).strip()
    if differs:
        sys.exit("REFUSED: these listed paths are not the same on origin/main (push first):\n" + differs[:1500])

    home = str(Path.home())
    rows = []
    for f in files:
        p = ROOT / f
        blob = p.read_bytes()
        if p.suffix.lower() in TEXT_EXT and home.encode() in blob and f not in ALLOW_HOME:
            sys.exit(f"REFUSED: a home-directory path inside {f}")
        rows.append({"path": f, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    if any(r["path"].startswith("/") or home in r["path"] for r in rows):
        sys.exit("REFUSED: an absolute path in the file list")

    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for r in rows:
            info = zipfile.ZipInfo(r["path"], date_time=(2026, 11, 15, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, (ROOT / r["path"]).read_bytes())

    zblob = ZIP.read_bytes()
    man = {
        "record": "DR4REC1, the Gaia DR4 pre-data record",
        "zip": ZIP.name,
        "count": len(rows),
        "zip_bytes": len(zblob),
        "sha256": hashlib.sha256(zblob).hexdigest(),
        "md5": hashlib.md5(zblob).hexdigest(),
        "uncompressed_bytes": sum(r["bytes"] for r in rows),
        "origin_main": git("rev-parse", "origin/main").strip(),
        "note": "Every file is the tracked copy, equal on the working tree, the local commit and origin/main when built. "
                "origin_main is the public repository's commit at that moment.",
        "home_path_exceptions": ALLOW_HOME,
        "entries": ENTRIES,
        "files": rows,
    }
    MAN.write_text(json.dumps(man, indent=1) + "\n", encoding="utf-8")
    print(f"built {ZIP.name}: {len(rows)} files, {len(zblob) / 1e6:.2f} MB, sha256 {man['sha256'][:16]}..., origin/main {man['origin_main'][:10]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
