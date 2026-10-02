#!/usr/bin/env python3
"""CFG289 step 3: compare the ORIG and FIX re-runs (FROZEN_CRITERIA.md, 80f05e155).

Usage:  python3 campaign_fresh_gravity/CFG289_rc100_csv_bound/cfg289_compare.py <scratch_dir>
For every entry point:
  * ORIG vs the committed outputs (git HEAD): the reproduction control.  Text is compared after dropping run-time lines; JSON after
    dropping time/second/elapsed/runtime keys; binary files byte-for-byte (reported separately: figure metadata is often not stable).
  * FIX vs ORIG: the same normalisation, on every file either run wrote, plus the captured stdout.
  * Pass/fail rows: every line carrying PASS or FAIL is keyed by its text with digits blanked; a key whose status differs is a FLIP.
  * Verdict lines (VERDICT / verdict / reading / classif / outcome / conclusion) that differ are listed in full for review.
Writes, into this lane: <tag>_RC100FIX.diff (FIX vs ORIG, text), copies of the differing FIX text outputs as <name>_RC100FIX.<ext>,
cfg289_compare.out and cfg289_compare_results.json.  The final classification (NUMERIC-MINOR vs VERDICT-MOVES by the 1-sigma rule)
is made by reading these, and is recorded in README.md.
"""
import difflib, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TIME_RE = re.compile(r"(run ?time|elapsed|seconds|wall|took|\(\d+(\.\d+)? ?s\)|\bin \d+(\.\d+)? ?s\b|\d+(\.\d+)? ?s(ec)?\b\s*$|"
                     r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}|timestamp|generated at)", re.I)
VERDICT_RE = re.compile(r"verdict|reading|classif|outcome|conclusion|decision", re.I)
TEXT_EXT = {".out", ".txt", ".md", ".csv", ".json", ".log", ".tex", ".dat", ".tsv"}
lines = []
P = lambda s="": (print(s), lines.append(s))


def norm_text(t):
    return [l.rstrip() for l in t.splitlines() if not TIME_RE.search(l)]


def strip_json(o):
    if isinstance(o, dict):
        return {k: strip_json(v) for k, v in o.items() if not any(x in k.lower() for x in ("time", "second", "elapsed", "runtime"))}
    if isinstance(o, list):
        return [strip_json(x) for x in o]
    return o


def canon(path, data):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        try:
            return json.dumps(strip_json(json.loads(data.decode())), indent=1, sort_keys=True).splitlines()
        except Exception:
            pass
    if ext in TEXT_EXT:
        return norm_text(data.decode(errors="replace"))
    return None   # binary


def head_bytes(rel):
    p = subprocess.run(["git", "-C", REPO, "show", f"HEAD:{rel}"], capture_output=True)
    return p.stdout if p.returncode == 0 else None


def status_map(ls):
    m = {}
    for l in ls:
        if re.search(r"\bPASS\b|\bFAIL\b", l):
            st = "FAIL" if re.search(r"\bFAIL\b", l) else "PASS"
            key = re.sub(r"\bPASS\b|\bFAIL\b", "#", re.sub(r"[-+]?\d+(\.\d+)?(e[-+]?\d+)?", "", l)).strip()
            m.setdefault(key, []).append(st)
    return m


def main(scratch):
    MO = json.load(open(os.path.join(scratch, "ORIG", "manifest.json")))
    MF = json.load(open(os.path.join(scratch, "FIX", "manifest.json")))
    zo, zfx = MO["mirror"], MF["mirror"]
    P(f"CFG289 compare: ORIG csv sha256 {MO['csv_sha256'][:16]}, FIX csv sha256 {MF['csv_sha256'][:16]}")
    out = dict(entries=[])
    runs_f = {r["script"]: r for r in MF["runs"]}
    for ro in MO["runs"]:
        s = ro["script"]
        rf = runs_f.get(s)
        tag = os.path.splitext(os.path.basename(s))[0]
        e = dict(script=s, rc_orig=ro["rc"], rc_fix=rf["rc"] if rf else None, orig_vs_committed=[], fix_vs_orig=[], flips=[],
                 verdict_lines=[], binary_diffs=[], symlink_writes=ro["symlink_targets_written"] + (rf["symlink_targets_written"] if rf else []))
        # ORIG vs committed
        for rel in ro["changed"]:
            new = open(os.path.join(zo, rel), "rb").read()
            old = head_bytes(rel)
            if old is None:
                e["orig_vs_committed"].append(dict(file=rel, status="new (not tracked at HEAD)"))
                continue
            a, b = canon(rel, old), canon(rel, new)
            if a is None:
                if old != new:
                    e["binary_diffs"].append(dict(file=rel, which="ORIG vs committed"))
                continue
            if a != b:
                d = [l for l in difflib.unified_diff(a, b, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))]
                e["orig_vs_committed"].append(dict(file=rel, status="DIFFERS", n_lines=len(d), sample=d[:6]))
        # FIX vs ORIG (files + stdout)
        files = sorted(set(ro["changed"]) | set(rf["changed"] if rf else []))
        difftxt = []
        allo, allf = [], []
        for rel in files:
            po, pf = os.path.join(zo, rel), os.path.join(zfx, rel)
            bo = open(po, "rb").read() if os.path.exists(po) and not os.path.islink(po) else None
            bf = open(pf, "rb").read() if os.path.exists(pf) and not os.path.islink(pf) else None
            if bo is None or bf is None:
                e["fix_vs_orig"].append(dict(file=rel, status="written by one run only"))
                continue
            a, b = canon(rel, bo), canon(rel, bf)
            if a is None:
                if bo != bf:
                    e["binary_diffs"].append(dict(file=rel, which="FIX vs ORIG"))
                continue
            allo += a
            allf += b
            if a != b:
                d = list(difflib.unified_diff(a, b, fromfile=f"ORIG/{rel}", tofile=f"FIX/{rel}", lineterm="", n=0))
                difftxt += d
                nd = sum(1 for l in d if l[:1] in "+-" and not l.startswith(("+++", "---")))
                e["fix_vs_orig"].append(dict(file=rel, status="DIFFERS", n_lines=nd))
                base, ext = os.path.splitext(os.path.basename(rel))
                txt = bf.decode(errors="replace").replace(zfx, "<mirror>").replace(scratch, "<scratch>")
                open(os.path.join(HERE, f"{base}_RC100FIX{ext}"), "w").write(txt)
        so = norm_text(open(os.path.join(scratch, "ORIG", "logs", f"{tag}.stdout")).read())
        sf = norm_text(open(os.path.join(scratch, "FIX", "logs", f"{tag}.stdout")).read()) if rf else []
        if so != sf:
            d = list(difflib.unified_diff(so, sf, fromfile=f"ORIG/stdout:{tag}", tofile=f"FIX/stdout:{tag}", lineterm="", n=0))
            difftxt += d
            e["fix_vs_orig"].append(dict(file="<stdout>", status="DIFFERS",
                                         n_lines=sum(1 for l in d if l[:1] in "+-" and not l.startswith(("+++", "---")))))
        allo += so
        allf += sf
        mo, mf = status_map(allo), status_map(allf)
        for k in sorted(set(mo) | set(mf)):
            if mo.get(k) != mf.get(k):
                e["flips"].append(dict(row=k[:200], orig=mo.get(k), fix=mf.get(k)))
        vo = [l for l in allo if VERDICT_RE.search(l)]
        vf = [l for l in allf if VERDICT_RE.search(l)]
        if vo != vf:
            e["verdict_lines"] = [l for l in difflib.unified_diff(vo, vf, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))][:40]
        if difftxt:
            body = "\n".join(difftxt) + "\n"
            body = body.replace(zo, "<mirror>").replace(zfx, "<mirror>").replace(scratch, "<scratch>")
            open(os.path.join(HERE, f"{tag}_RC100FIX.diff"), "w").write(body)
        # provisional class (the frozen 1-sigma judgement is made on the diffs, in README.md)
        if ro["rc"] in ("TIMEOUT",) or (rf and rf["rc"] in ("TIMEOUT",)) or rf is None:
            cls = "NOT-RUN"
        elif ro["rc"] != (rf["rc"] if rf else None) and not e["fix_vs_orig"]:
            cls = "CHECK (rc differs)"
        elif not e["fix_vs_orig"]:
            cls = "UNCHANGED"
        elif e["flips"] or e["verdict_lines"] or ro["rc"] != rf["rc"]:
            cls = "CANDIDATE VERDICT-MOVES"
        else:
            cls = "NUMERIC (judge vs 1 sigma)"
        repro = "reproduces" if not any(x.get("status") == "DIFFERS" for x in e["orig_vs_committed"]) else "NOT-REPRODUCIBLE"
        e["provisional"] = cls
        e["orig_reproduction"] = repro
        out["entries"].append(e)
        P(f"\n{s}\n  rc ORIG {ro['rc']} / FIX {rf['rc'] if rf else '-'};  ORIG vs committed: {repro};  provisional: {cls}")
        for x in e["orig_vs_committed"]:
            P(f"    ORIG-vs-committed {x['file']}: {x['status']}" + (f" ({x['n_lines']} lines) e.g. {x['sample'][:2]}" if x.get("sample") else ""))
        for x in e["fix_vs_orig"]:
            P(f"    FIX-vs-ORIG {x['file']}: {x['status']}" + (f" ({x['n_lines']} lines)" if x.get("n_lines") else ""))
        for x in e["flips"]:
            P(f"    FLIP {x['orig']} -> {x['fix']}: {x['row']}")
        for l in e["verdict_lines"][:12]:
            P(f"    verdict-line {l[:220]}")
        for x in e["binary_diffs"]:
            P(f"    binary differs ({x['which']}): {x['file']}")
        if e["symlink_writes"]:
            P(f"    *** symlink targets written (run void): {e['symlink_writes']}")
    scrub = lambda t: t.replace(zo, "<mirror>").replace(zfx, "<mirror>").replace(scratch, "<scratch>")
    open(os.path.join(HERE, "cfg289_compare_results.json"), "w").write(scrub(json.dumps(out, indent=1)))
    open(os.path.join(HERE, "cfg289_compare.out"), "w").write(scrub("\n".join(lines) + "\n"))


if __name__ == "__main__":
    main(os.path.abspath(sys.argv[1]))
