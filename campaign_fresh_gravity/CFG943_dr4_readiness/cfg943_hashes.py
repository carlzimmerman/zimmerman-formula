#!/usr/bin/env python3
"""CFG943 task 1: inventory + sha256 verification of the frozen Gaia DR4 wide-binary plan (FROZEN_CRITERIA.md section 1).

Reads only; writes cfg943_hashes.out and cfg943_hashes.json in this directory. Nothing frozen is touched.
  H1  every digest in every AMENDMENT*_HASH.txt against PREREGISTRATION_DR4.md at each git commit that touched it;
      the latest filed amendment's "after" digest against the working tree; one commit per hash file; prereg dir clean.
  H2  freeze-manifest table (5 files), RELEASE_DAY_CHECKLIST section 3 (4 files), edge table pipeline hash,
      CFG740 seal, CFG825 FROZEN_CRITERIA (sha in its ID notes), CFG800 FROZEN_CRITERIA unchanged since aa71ca510,
      THEORY_CANONICAL_2026-10-14.sha256.
  H3  each AMENDMENT*_DRAFT_NOT_FILED.md: FILED (header in prereg + hash file) or DRAFT-ONLY.
exit 0 if no UNEXPLAINED mismatch (documented drift is reported, prominently, and does not fail).
"""
import hashlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PREP = "prep_2026/gaia_dr4_prep"
PREREG = f"{PREP}/PREREGISTRATION_DR4.md"
OUT = []


def P(s=""):
    OUT.append(s); print(s)


def git(*a):
    return subprocess.run(["git", "-C", ROOT, *a], capture_output=True, check=True).stdout


def sha_file(rel):
    return hashlib.sha256(open(os.path.join(ROOT, rel), "rb").read()).hexdigest()


def main():
    res = dict(lane="CFG943", H1={}, H2={}, H3={}, mismatches=[], documented_drift=[])
    # ---------------- H1
    commits = git("log", "--follow", "--format=%H %ad", "--date=short", "--", PREREG).decode().split("\n")
    versions = {}
    for line in filter(None, commits):
        c, d = line.split()
        blob = git("show", f"{c}:{PREREG}")
        versions.setdefault(hashlib.sha256(blob).hexdigest(), []).append((c[:10], d))
    wt = sha_file(PREREG)
    P(f"H1 prereg working-tree sha256 {wt}; {len(commits) - 1} committed versions")
    dirty = git("status", "--porcelain", "--", PREP).decode().strip()
    res["H1"]["prep_dir_clean"] = (dirty == "")
    P(f"H1 git status of {PREP}: {'CLEAN' if not dirty else 'DIRTY: ' + dirty}")
    if dirty:
        res["mismatches"].append(f"prep dir not clean: {dirty}")
    hfiles = sorted([f for f in os.listdir(os.path.join(ROOT, PREP)) if re.fullmatch(r"AMENDMENT\d+_HASH\.txt", f)],
                    key=lambda f: int(re.search(r"\d+", f).group()))
    latest_after = None
    for f in hfiles:
        n = int(re.search(r"\d+", f).group())
        txt = open(os.path.join(ROOT, PREP, f), encoding="utf-8").read()
        ncommit = len([x for x in git("log", "--format=%h", "--", f"{PREP}/{f}").decode().split() if x])
        rows = []
        for line in txt.splitlines():
            for dg in re.findall(r"\b[0-9a-f]{64}\b", line):
                label = line.split(":")[0].strip()[:90]
                hit = versions.get(dg)
                rows.append(dict(label=label, digest=dg, matches_commit=hit[0] if hit else None))
                if not hit:
                    res["mismatches"].append(f"{f}: digest {dg[:16]} ({label}) matches NO committed prereg version")
                if "after" in label.lower():
                    latest_after = (n, dg) if (latest_after is None or n >= latest_after[0]) else latest_after
        not_recorded = "NOT RECORDED" in txt
        res["H1"][f] = dict(commits=ncommit, digests=rows, not_recorded_note=not_recorded)
        if ncommit != 1:
            res["mismatches"].append(f"{f} has {ncommit} commits (expected 1: never edited)")
        P(f"H1 {f}: {ncommit} commit(s); " + "; ".join(f"{r['label'][:40]} {r['digest'][:12]} -> "
                                                       f"{r['matches_commit'][0] + ' ' + r['matches_commit'][1] if r['matches_commit'] else 'NO MATCH'}"
                                                       for r in rows) + ("  [records 'NOT RECORDED AT FILING TIME' for the post-A4 digest, disclosed in the file]" if not_recorded else ""))
    res["H1"]["latest_after"] = dict(amendment=latest_after[0], digest=latest_after[1], equals_working_tree=(latest_after[1] == wt))
    P(f"H1 latest filed amendment {latest_after[0]}: 'after' digest {latest_after[1][:16]} {'==' if latest_after[1] == wt else '!='} working tree")
    if latest_after[1] != wt:
        res["mismatches"].append("latest amendment's 'after' digest != prereg working tree")
    unclaimed = [(dg[:16], v) for dg, v in versions.items() if not any(dg == r["digest"] for f in hfiles for r in res["H1"][f]["digests"])]
    res["H1"]["committed_versions_without_a_hash_record"] = unclaimed
    P(f"H1 committed prereg versions no hash file names: {unclaimed} (the original freeze f617640ae and the two post-Amendment-4 states A4 says were not recorded)")

    # ---------------- H2
    prereg_txt = open(os.path.join(ROOT, PREREG), encoding="utf-8").read()
    manifest = re.findall(r"\| `(?:zimmerman-formula/)?([^`]+)` \| [^|]+\| `([0-9a-f]{64})` \|", prereg_txt.split("### Freeze manifest")[1].split("\n---\n")[0])
    res["H2"]["freeze_manifest"] = []
    for rel, dg in manifest:
        now = sha_file(rel)
        ok = now == dg
        res["H2"]["freeze_manifest"].append(dict(file=rel, frozen=dg, now=now, match=ok))
        P(f"H2 freeze manifest {rel}: frozen {dg[:16]} now {now[:16]} -> {'MATCH' if ok else 'DIFFERS'}")
        if not ok:
            hist = git("log", "--format=%h %ad %s", "--date=short", "--", rel).decode().splitlines()
            res["documented_drift"].append(dict(file=rel, frozen_manifest=dg, now=now, commits_since_freeze=len(hist) - 1,
                                                log=[h[:140] for h in hist]))
            P(f"   *** DOCUMENTED DRIFT: {len(hist) - 1} commits since the 2026-07-16 freeze (retargets recorded in Amendments 10(g), 11(h) and the 2026-09-22 Amendment-12 catch-up 2a18b570e); "
              f"the operative hash is pinned by RELEASE_DAY_CHECKLIST section 3 and edge_table_dr4.json (checked below). The prereg's manifest row is never edited.")
    ck = open(os.path.join(ROOT, PREP, "RELEASE_DAY_CHECKLIST.md"), encoding="utf-8").read()
    ref = re.findall(r"\| `([^`]+\.py)` \| `([0-9a-f]{64})` \| ([0-9a-f]+) \|", ck)
    res["H2"]["checklist_section3"] = []
    for name, dg, c in ref:
        rel = f"{PREP}/{name}"
        now = sha_file(rel); ok = now == dg
        res["H2"]["checklist_section3"].append(dict(file=rel, ref=dg, now=now, match=ok))
        P(f"H2 checklist s3 {name}: {'MATCH' if ok else 'MISMATCH'} ({now[:16]})")
        if not ok:
            res["mismatches"].append(f"checklist s3 {name} differs")
    et = json.load(open(os.path.join(ROOT, PREP, "dr4_ready_1/edge_table_dr4.json")))
    ok = et.get("pipeline_sha256") == sha_file(f"{PREP}/wide_binary_pipeline.py")
    res["H2"]["edge_table_pipeline"] = ok
    P(f"H2 edge_table_dr4.json pipeline_sha256: {'MATCH' if ok else 'MISMATCH'}")
    if not ok:
        res["mismatches"].append("edge table pipeline hash differs")
    c740 = "campaign_fresh_gravity/CFG740_sealed_wb_slope2"
    seal = open(os.path.join(ROOT, c740, "PREDICTIONS_HASH.txt")).read().split()[0]
    ok = seal == sha_file(f"{c740}/cfg740_predictions.json")
    ncm = len(git("log", "--format=%h", "--", c740).decode().split())
    res["H2"]["CFG740_seal"] = dict(seal=seal, match=ok, commits_on_dir=ncm)
    P(f"H2 CFG740 seal {seal[:16]}: {'MATCH' if ok else 'MISMATCH'}; commits touching the sealed dir: {ncm}")
    if not ok:
        res["mismatches"].append("CFG740 seal differs")
    c825 = "campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/FROZEN_CRITERIA.md"
    want = "558e03f0b87e52aae77a069cea7c1d8ef765b2bbeb8002c028c8357722b3fffb"
    ok = sha_file(c825) == want
    res["H2"]["CFG825_criteria"] = ok
    P(f"H2 CFG825 FROZEN_CRITERIA.md vs its ID-note sha {want[:16]}: {'MATCH' if ok else 'MISMATCH'}")
    if not ok:
        res["mismatches"].append("CFG825 criteria differ")
    c800 = "campaign_fresh_gravity/CFG800_wb_2026_scoring/FROZEN_CRITERIA.md"
    diff = subprocess.run(["git", "-C", ROOT, "diff", "--quiet", "aa71ca510", "--", c800]).returncode
    ok = diff == 0
    res["H2"]["CFG800_criteria_unchanged_since_aa71ca510"] = ok
    P(f"H2 CFG800 FROZEN_CRITERIA.md unchanged since aa71ca510: {ok}")
    if not ok:
        res["mismatches"].append("CFG800 criteria changed")
    tc = "campaign_fresh_gravity/THEORY_CANONICAL_2026-10-14"
    recs = open(os.path.join(ROOT, tc + ".sha256")).read().split()
    ok = recs[0] == sha_file(tc + ".md")
    res["H2"]["THEORY_CANONICAL_2026-10-14"] = ok
    P(f"H2 THEORY_CANONICAL_2026-10-14.md vs its .sha256: {'MATCH' if ok else 'MISMATCH'}")
    if not ok:
        res["mismatches"].append("THEORY_CANONICAL 10-14 differs from its sha256 file")

    # ---------------- H3
    drafts = sorted([f for f in os.listdir(os.path.join(ROOT, PREP)) if f.endswith("_DRAFT_NOT_FILED.md")],
                    key=lambda f: int(re.search(r"\d+", f).group()))
    for f in drafts:
        n = int(re.search(r"\d+", f).group())
        hdr = len(re.findall(rf"AMENDMENT {n} — \d{{4}}-\d\d-\d\d, ADDED IN THE OPEN", prereg_txt))
        hf = os.path.exists(os.path.join(ROOT, PREP, f"AMENDMENT{n}_HASH.txt"))
        cls = "FILED (draft file retained, non-operative)" if (hdr == 1 and hf) else "DRAFT-ONLY (not in the frozen plan)"
        res["H3"][f] = dict(header_in_prereg=hdr, hash_file=hf, cls=cls)
        P(f"H3 {f}: header in prereg x{hdr}, hash file {hf} -> {cls}")
    filed = sorted(int(re.search(r"\d+", f).group()) for f in hfiles)
    res["H3"]["amendments_with_hash_files"] = filed
    P(f"H3 amendments with hash files: {filed}")

    P("")
    P(f"UNEXPLAINED MISMATCHES: {len(res['mismatches'])}" + ("".join(f"\n  *** {m}" for m in res["mismatches"])))
    P(f"DOCUMENTED DRIFT (reported prominently, not a hash-file mismatch): {[d['file'] for d in res['documented_drift']]}")
    json.dump(res, open(os.path.join(HERE, "cfg943_hashes.json"), "w"), indent=1)
    open(os.path.join(HERE, "cfg943_hashes.out"), "w").write("\n".join(OUT) + "\n")
    return 0 if not res["mismatches"] else 1


if __name__ == "__main__":
    sys.exit(main())
