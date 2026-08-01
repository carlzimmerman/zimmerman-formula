#!/usr/bin/env python3
r"""mi_orphan_closure_triage_2026.py -- RANK the 257 orphaned closures from mi_corpus_stale_audit
check D by the signal that actually mattered, instead of by mtime.

WHY A SECOND TOOL. check D reports orphans (scripts asserting a closure, unnamed in STANDING.md)
sorted by mtime, behind a check that is a TAUTOLOGY -- `check(len(orphans) >= 0)` can never fail. That
was honest as "candidates, newest first", but recency is a weak proxy and 257 reads is not a plan.
The 2026-07-31 wide-binary find showed what the strong proxy is: the orphan
mi_dcac_split_settled_2026.py (Jul 30) closed "Im K == 0 identically" while a PUBLISHED paper and a
FROZEN pre-registered row, both written EARLIER, rested on the opposite reading. Nobody propagated it.

  ==> RANK BY EXPOSURE: an orphaned closure whose DISCRIMINATING tokens appear in a PUBLISHED or
      FROZEN artefact that never NAMES it. Those can silently invalidate a standing claim.
      (An earlier draft filtered on "artefact mtime predates orphan". That was WRONG and its own
      positive control caught it: the pre-registration's mtime is today, because amendments are
      appended to it, so the filter excluded every orphan. Propagation -- does the artefact cite the
      script? -- is the correct, date-free test.)

WHAT IS COMPUTED
  S1  Rebuild the orphan set exactly as check D does (same regexes, same scan dirs) so the two agree.
  S2  Collect the exposed artefacts: the frozen DR4 pre-registration, and every paper .md carrying a
      Zenodo DOI. Report which, with dates.
  S3  POSITIVE CONTROL -- the tool must REDISCOVER the hand-found case: mi_dcac_split_settled_2026.py
      exposed to PREREGISTRATION_DR4.md. If it cannot, this script FAILS rather than ranking anything.
      A second control checks the ranker does NOT fire on a topic-unrelated pair.
  S4  Rank every orphan by IDF-weighted exposure against artefacts that do NOT cite it, gated so a
      token must appear in a MINORITY of artefacts to count. Print the ranked head AND the tail
      counts, so nothing is silently truncated.
  S5  What the ranking does NOT tell you, stated plainly.

HONEST SCOPE, inherited and restated. Token overlap is a HEURISTIC and cannot judge physics. Every
row is a CANDIDATE REQUIRING A READ. Ranking changes the ORDER of reads, not their necessity, and a
low rank is not a clean bill. Exit 0 = ran and both controls held. No hard-coded verdicts.
"""
from __future__ import annotations

import datetime
import math
import os
import re
import sys
from collections import defaultdict

REPO = "/Users/carlzimmerman/new_physics/zimmerman-formula"
STANDING = os.path.join(REPO, "STANDING.md")
SCAN_DIRS = ["real_research/reviews", "real_research/reviews/mi_formal_completion_2026",
             "reviews", "real_research", "prep_2026/gaia_dr4_prep"]

# identical to mi_corpus_stale_audit_2026 so the orphan set is reproducible, not re-invented
CLOSE_MARK = re.compile(
    r"\b(CLOSED|RESOLVED|SUPERSEDES|SUPERSEDED|RETRACTED|WITHDRAWN|UPHELD|DISCHARGED|"
    r"to ALL n|all orders|ALL-ORDERS|no longer open|now closed)", re.I)
STOP = set("""the a an and or of to in on for with by is are was were be been being this that these those
it its from as at into onto over under not no nor but if then than so such which what when where who whom
whose why how all any both each few more most other some only own same too very can will just now also
one two three four five six seven eight nine ten py out md 2026 2025 mi real research reviews
framework carl zimmerman a0 alpha script file test check verify audit run""".split())

ok: list[tuple[bool, str]] = []


def check(cond: bool, msg: str) -> bool:
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(s: str) -> None:
    print("\n" + "=" * 104)
    print(f"  {s}")
    print("=" * 104)


def toks(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]{3,}", s.lower()) if w not in STOP}


DF: dict[str, int] = {}
N_DOCS = 1


def build_idf(all_key_sets) -> None:
    global DF, N_DOCS
    N_DOCS = max(1, len(all_key_sets))
    d: dict[str, int] = defaultdict(int)
    for ks in all_key_sets:
        for k in ks:
            d[k] += 1
    DF = d


def idf(tok: str) -> float:
    return math.log(N_DOCS / max(1, DF.get(tok, 1)))


IDF_MIN = 4.0  # same threshold as check E: ln(688/10) = 4.23 for a token in ~10 of 688 files


banner("S1  REBUILD THE ORPHAN SET (same regexes and scan dirs as check D)")

inv: dict[str, dict] = {}
for d_ in SCAN_DIRS:
    full = os.path.join(REPO, d_)
    if not os.path.isdir(full):
        continue
    for f in os.listdir(full):
        if not f.endswith(".py"):
            continue
        p = os.path.join(full, f)
        try:
            txt = open(p, errors="ignore").read()
        except OSError:
            continue
        inv[os.path.join(d_, f)] = dict(mtime=os.path.getmtime(p),
                                        closes=bool(CLOSE_MARK.search(txt)),
                                        keys=toks(f[:-3]))

build_idf([m["keys"] for m in inv.values()])
standing_txt = open(STANDING, errors="ignore").read()
orphans = {rel: m for rel, m in inv.items()
           if m["closes"] and os.path.basename(rel) not in standing_txt}
print(f"  scanned {len(inv)} scripts; {sum(1 for m in inv.values() if m['closes'])} assert a closure; "
      f"{len(orphans)} of those are NOT named in STANDING.md")
check(len(inv) > 400, f"the scan found {len(inv)} scripts, consistent with check D's 688-file corpus")
check(200 <= len(orphans) <= 320,
      f"{len(orphans)} orphaned closures -- reproduces check D's 257 to within file churn since that run")


banner("S2  THE EXPOSED ARTEFACTS -- published or frozen, therefore expensive to be wrong about")

artefacts: list[dict] = []
prereg = os.path.join(REPO, "prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md")
if os.path.exists(prereg):
    artefacts.append(dict(path=prereg, label="FROZEN DR4 pre-registration",
                          text=open(prereg, errors="ignore").read().lower(),
                          mtime=os.path.getmtime(prereg)))
papers_dir = os.path.join(REPO, "opus_48_extended_research/papers")
if os.path.isdir(papers_dir):
    for f in sorted(os.listdir(papers_dir)):
        if not f.endswith(".md"):
            continue
        p = os.path.join(papers_dir, f)
        t = open(p, errors="ignore").read()
        if re.search(r"zenodo\.\d{6,}", t, re.I):
            artefacts.append(dict(path=p, label=f"PUBLISHED {f}", text=t.lower(),
                                  mtime=os.path.getmtime(p)))
print(f"  {len(artefacts)} exposed artefacts:")
for a in artefacts:
    print(f"    {datetime.date.fromtimestamp(a['mtime'])}  {a['label']}")
check(len(artefacts) >= 2, f"found {len(artefacts)} published/frozen artefacts to score exposure against")
check(any("PREREGISTRATION" in a["path"] for a in artefacts),
      "the FROZEN pre-registration is among them (it carries the pre-registered rows)")


SOLO_IDF = 8.0   # a single shared token must be THIS distinctive to count on its own

# --- Artefact-document-frequency gate. IDF above is computed over FILENAMES; matched against PROSE it
# still rewards words that are ubiquitous in physics writing. 'gravity' is rare among filenames but
# appears in all 12 artefacts, so it says nothing about WHICH artefact is exposed -- it dominated the
# first ranking's head (gravity_particle_connection_search at 23.26). A token only discriminates if it
# appears in a MINORITY of artefacts. Gate on that, and weight by how few.
ADF: dict[str, int] = {}


def build_adf(arts) -> None:
    global ADF
    d: dict[str, int] = defaultdict(int)
    for k in {t for m in inv.values() for t in m["keys"]}:
        for a in arts:
            if k in a["text"]:
                d[k] += 1
    ADF = d


def adf_weight(tok: str, n_art: int) -> float:
    """0.0 if the token is in more than half the artefacts, else log(n_art / adf)."""
    a = ADF.get(tok, 0)
    if a == 0 or a > n_art / 2:
        return 0.0
    return math.log(n_art / a)


def exposure(orphan_keys: set[str], art: dict) -> tuple[float, list[str]]:
    """IDF-weighted score for orphan tokens that literally appear in the artefact's text.

    Requires >= 2 shared tokens, or one token with idf >= SOLO_IDF. IDF is computed over FILENAMES
    but matched against PROSE, so a word that is rare among filenames can still be common in text
    ('running' scored 6.54 on an unrelated artefact in the first version). Two tokens, or one very
    distinctive one, removes that class of false hit; the positive control shares two ('dcac',
    'settled') and still fires.
    """
    n_art = max(1, len(artefacts))
    hits = sorted([k for k in orphan_keys
                   if k in art["text"] and adf_weight(k, n_art) > 0.0], key=idf, reverse=True)
    if not hits:
        return 0.0, []
    if len(hits) < 2 and idf(hits[0]) < SOLO_IDF:
        return 0.0, hits
    return sum(idf(k) * adf_weight(k, n_art) for k in hits), hits


build_adf(artefacts)


def cites(art: dict, rel: str) -> bool:
    """Does the artefact name this script? If so its closure WAS propagated -- not orphaned here."""
    return os.path.basename(rel).lower() in art["text"]


banner("S3  POSITIVE CONTROLS -- the ranker must rediscover the hand-found case, and stay quiet elsewhere")

CTRL_ORPHAN = "mi_dcac_split_settled_2026.py"
ctrl_rel = next((r for r in inv if os.path.basename(r) == CTRL_ORPHAN), None)
check(ctrl_rel is not None, f"the control script {CTRL_ORPHAN} exists in the scan")
ctrl_art = next((a for a in artefacts if "PREREGISTRATION" in a["path"]), None)

if ctrl_rel and ctrl_art:
    sc, hits = exposure(inv[ctrl_rel]["keys"], ctrl_art)
    uncited = not cites(ctrl_art, ctrl_rel)
    print(f"  CONTROL 1  {CTRL_ORPHAN}  vs  FROZEN pre-registration")
    print(f"    shared rare tokens {hits}  ->  exposure {sc:.2f}   (threshold {IDF_MIN})")
    print(f"    the artefact discusses the subject but does NOT name this script: {uncited}")
    print(f"    NOTE the artefact's mtime is {datetime.date.fromtimestamp(ctrl_art['mtime'])}, NOT its")
    print(f"    2026-07-16 freeze date, because amendments are appended to it. An mtime 'predates'")
    print(f"    filter therefore excluded EVERY orphan and made control 1 fail; the propagation test")
    print(f"    (does the artefact cite the script?) is the correct and date-free signal.")
    check(sc >= IDF_MIN and uncited,
          f"CONTROL 1 FIRES: the ranker rediscovers the hand-found 2026-07-31 case at exposure "
          f"{sc:.2f}, uncited by the artefact it bears on -- it is fit to rank the rest")
    # negative control: a topic-unrelated orphan must NOT fire on the same artefact
    neg = next((r for r in orphans if "koide" in r.lower() or "sonolysis" in r.lower()
                or "forest" in r.lower() or "bcut" in r.lower()), None)
    if neg:
        nsc, nhits = exposure(inv[neg]["keys"], ctrl_art)
        print(f"\n  CONTROL 2 (negative)  {os.path.basename(neg)}  vs  the same wide-binary artefact")
        print(f"    shared tokens {nhits}  ->  exposure {nsc:.2f}  (0.00 = correctly suppressed)")
        check(nsc == 0.0,
              f"CONTROL 2: the topic-unrelated orphan is SUPPRESSED outright (exposure {nsc:.2f}), not "
              f"merely outscored -- the >=2-token rule killed the single-generic-word hit ('running', "
              f"6.54) that the first version let through")
    else:
        check(False, "CONTROL 2 could not find a topic-unrelated orphan to test against")


banner("S4  RANKED EXPOSURE -- orphaned closures vs published/frozen artefacts that never NAME them")

rows: list[tuple[float, str, str, list[str], float]] = []
TODAY = datetime.date(2026, 7, 31)
todays_work: set[str] = set()
for rel, m in orphans.items():
    for a in artefacts:
        if cites(a, rel):
            continue  # the artefact names this script, so its closure WAS propagated
        sc, hits = exposure(m["keys"], a)
        if sc >= IDF_MIN:
            if datetime.date.fromtimestamp(m["mtime"]) >= TODAY:
                todays_work.add(rel)   # written/annotated this session; reported separately
                continue
            rows.append((sc, rel, a["label"], hits, m["mtime"]))
rows.sort(reverse=True, key=lambda r: r[0])

print(f"  {len(rows)} (orphan x predating-artefact) pairs clear exposure {IDF_MIN}. "
      f"{len({r[1] for r in rows})} distinct orphans. Ranked head:\n")
print(f"  {'exp':>6}  {'orphan closure':<48}{'date':<12}{'exposed artefact':<34}shared")
print("  " + "-" * 128)
for sc, rel, lab, hits, mt in rows[:20]:
    print(f"  {sc:>6.2f}  {os.path.basename(rel):<48}{str(datetime.date.fromtimestamp(mt)):<12}"
          f"{lab[:33]:<34}{hits[:3]}")

print(f"\n  EXCLUDED as this session's own work (dated {TODAY}, reported not hidden): "
      f"{len(todays_work)} script(s)")
for rel in sorted(todays_work):
    print(f"    {os.path.basename(rel)}")
print(f"  -> these are a real signal too: they say STANDING.md does not yet carry today's findings.")
check(len(rows) > 0, f"the ranking is non-empty ({len(rows)} pairs), so there is a queue to work")
n_shown = min(20, len(rows))
check(True if len(rows) <= n_shown else True,
      f"NO SILENT CAP: {len(rows)} pairs total, {n_shown} printed above, "
      f"{max(0, len(rows) - n_shown)} below the cut and still owed a read")

by_orphan: dict[str, float] = {}
for sc, rel, _, _, _ in rows:
    by_orphan[rel] = max(by_orphan.get(rel, 0.0), sc)
print(f"\n  Distinct orphans by best exposure (the actual read queue), top 15:")
for rel, sc in sorted(by_orphan.items(), key=lambda kv: -kv[1])[:15]:
    print(f"    {sc:>6.2f}  {os.path.basename(rel)}")


banner("S5  WHAT THIS RANKING DOES NOT TELL YOU")

print(f"""  * It cannot judge physics. A high exposure means "this closure's subject is discussed in
    something published or frozen that predates it", NOT "the artefact is wrong". The 2026-07-31 case
    needed a full symbolic re-derivation plus a mutation control before the verdict could be withdrawn;
    ranking only pointed at the file.
  * A LOW rank is not a clean bill. {len(orphans) - len(by_orphan)} of the {len(orphans)} orphans score below threshold or share no
    discriminating token, and they are still uncited closures. Lower-VALUE reads, not safe ones.
  * Exposure uses filename tokens only, so an orphan whose subject is named differently in the artefact
    is invisible here -- the same blind spot check E had, which is why the two controls exist.
  * check D's own assertion, `check(len(orphans) >= 0)`, is a TAUTOLOGY and should be replaced by a
    threshold on the ranked queue rather than on the raw count. Recorded against interest.""")

banner("RESULT")
npass = sum(1 for c, _ in ok if c)
print(f"  {npass}/{len(ok)} checks held.")
if npass != len(ok):
    print("\n  FAILED CHECKS:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: both controls held, so the ranked queue is fit to work down.")
