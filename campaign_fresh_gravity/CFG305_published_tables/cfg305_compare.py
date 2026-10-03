#!/usr/bin/env python3
"""CFG305 step 3: compare the ORIG and FIX re-runs (a parametrised copy of CFG289's cfg289_compare.py; FROZEN_CRITERIA.md, 82dfcc1b3).

Usage:  python3 campaign_fresh_gravity/CFG305_published_tables/cfg305_compare.py <scratch_dir> <O|C>
ORIG = the CORRECTED CSV, FIX = the PUBLISHED CSV (cfg305_rerun.py).  For every entry point:
  * ORIG vs the reproduction reference: group O -- CFG289's FIX copy <name>_RC100FIX.<ext> where one exists (mirror paths normalised),
    otherwise the committed file (git HEAD); group C -- the committed file, and the captured stdout against the committed file named in
    the manifest (stdout_ref).  Text is compared after dropping run-time lines; JSON after dropping time/second/elapsed/runtime keys;
    binary files byte-for-byte (reported separately: figure metadata is often not stable).
  * FIX vs ORIG: the same normalisation, on every file either run wrote, plus the captured stdout.
  * Pass/fail rows: every line carrying PASS or FAIL is keyed by its text with digits blanked; a key whose status differs is a FLIP.
  * Verdict lines (VERDICT / verdict / reading / classif / outcome / conclusion) that differ are listed in full for review.
  * group O only: MUTATE vs FIX for the MUTATE entries (L323, cfg216_rc100.py); the planted change must show up (frozen).
Writes, into this lane: [C_]<tag>_PUBFIX.diff (FIX vs ORIG, text), copies of the differing FIX text outputs as [C_]<name>_PUBFIX.<ext>
(group C outputs carry the prefix C_), cfg305_compare_<group>.out and cfg305_compare_<group>_results.json.  The final classification
(NUMERIC-MINOR vs VERDICT-MOVES by the 1-sigma rule) is made by reading these, and is recorded in README.md.
"""
import difflib, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
L289 = os.path.join(REPO, "campaign_fresh_gravity", "CFG289_rc100_csv_bound")
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


def mnorm(b, zf):
    """replace a mirror's own path (and its parent run dir) by placeholders"""
    return b.replace(zf.encode(), b"<mirror>").replace(os.path.dirname(zf).encode(), b"<base>")


def ref_bytes(group, rel):
    """the reproduction reference: group O -> CFG289's FIX copy where one exists, else HEAD; group C -> HEAD"""
    if group == "O":
        base, ext = os.path.splitext(os.path.basename(rel))
        p = os.path.join(L289, f"{base}_RC100FIX{ext}")
        if os.path.exists(p):
            return open(p, "rb").read(), "CFG289 FIX copy"
    b = head_bytes(rel)
    return b, ("committed" if b is not None else None)


def main(scratch, group):
    MO = json.load(open(os.path.join(scratch, f"{group}_ORIG", "manifest.json")))
    MF = json.load(open(os.path.join(scratch, f"{group}_FIX", "manifest.json")))
    zo, zfx = MO["mirror"], MF["mirror"]
    PFX = "C_" if group == "C" else ""
    P(f"CFG305 compare, group {group}: ORIG substituted {MO['substituted']}; FIX substituted {MF['substituted']}")
    P(f"  sha256 (original path / CORRECTED path / paper-values): ORIG {[v[:16] for v in MO['sha256'].values()]}; FIX {[v[:16] for v in MF['sha256'].values()]}")
    out = dict(group=group, entries=[], orig_substituted=MO["substituted"], fix_substituted=MF["substituted"], sha256_orig=MO["sha256"], sha256_fix=MF["sha256"])
    runs_f = {r["tag"]: r for r in MF["runs"]}
    for ro in MO["runs"]:
        s = ro["script"]
        tag = ro["tag"]
        rf = runs_f.get(tag)
        e = dict(script=s, tag=tag, rc_orig=ro["rc"], rc_fix=rf["rc"] if rf else None, orig_vs_committed=[], fix_vs_orig=[], flips=[],
                 verdict_lines=[], binary_diffs=[], symlink_writes=ro["symlink_targets_written"] + (rf["symlink_targets_written"] if rf else []))
        # ORIG vs the reproduction reference
        for rel in ro["changed"]:
            new = open(os.path.join(zo, rel), "rb").read().replace(zo.encode(), b"<mirror>").replace(scratch.encode(), b"<scratch>")
            old, src_ = ref_bytes(group, rel)
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
                e["orig_vs_committed"].append(dict(file=rel, status="DIFFERS", reference=src_, n_lines=len(d), sample=d[:6]))
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
            # CFG305: normalise the two mirrors' own paths before comparing (CFG289's compare did not; disclosed)
            bo, bf = mnorm(bo, zo), mnorm(bf, zfx)
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
                open(os.path.join(HERE, f"{PFX}{base}_PUBFIX{ext}"), "w").write(txt)
        so_raw = open(os.path.join(scratch, f"{group}_ORIG", "logs", f"{tag}.stdout")).read()
        so = norm_text(mnorm(so_raw.encode(), zo).decode(errors="replace"))
        sf = norm_text(mnorm(open(os.path.join(scratch, f"{group}_FIX", "logs", f"{tag}.stdout"), "rb").read(), zfx).decode(errors="replace")) if rf else []
        if ro.get("stdout_ref"):
            ref_ = head_bytes(ro["stdout_ref"])
            a_ = norm_text(ref_.decode(errors="replace")) if ref_ is not None else None
            b_ = norm_text(so_raw.replace(zo, "<mirror>"))
            if a_ is None:
                e["orig_vs_committed"].append(dict(file=f"<stdout> vs {ro['stdout_ref']}", status="new (not tracked at HEAD)"))
            elif a_ != b_:
                d = [l for l in difflib.unified_diff(a_, b_, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))]
                e["orig_vs_committed"].append(dict(file=f"<stdout> vs {ro['stdout_ref']}", status="DIFFERS", reference="committed", n_lines=len(d), sample=d[:6]))
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
            open(os.path.join(HERE, f"{PFX}{tag}_PUBFIX.diff"), "w").write(body)
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
        P(f"\n{tag}  ({s})\n  rc ORIG {ro['rc']} / FIX {rf['rc'] if rf else '-'};  ORIG vs committed: {repro};  provisional: {cls}")
        for x in e["orig_vs_committed"]:
            P(f"    ORIG-vs-reference {x['file']}: {x['status']}" + (f" [{x['reference']}]" if x.get('reference') else "") + (f" ({x['n_lines']} lines) e.g. {x['sample'][:2]}" if x.get("sample") else ""))
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
    # ---- MUTATE vs FIX (group O; frozen: L323 must differ, else the substitution path is dead and the lane is void)
    if group == "O" and os.path.exists(os.path.join(scratch, "O_MUTATE", "manifest.json")):
        MM = json.load(open(os.path.join(scratch, "O_MUTATE", "manifest.json")))
        zm = MM["mirror"]
        P(f"\nMUTATE vs FIX (row 50 log M_baryon +0.30 dex; substituted {MM['substituted']})")
        out["mutate"] = []
        for rm in MM["runs"]:
            rf = runs_f[rm["tag"]]
            nd = 0
            for rel in sorted(set(rm["changed"]) | set(rf["changed"])):
                pm, pf = os.path.join(zm, rel), os.path.join(zfx, rel)
                if not (os.path.exists(pm) and os.path.exists(pf)):
                    continue
                a, b = canon(rel, mnorm(open(pf, "rb").read(), zfx)), canon(rel, mnorm(open(pm, "rb").read(), zm))
                if a is None:
                    continue
                nd += sum(1 for l in difflib.unified_diff(a, b, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---")))
            so_ = norm_text(mnorm(open(os.path.join(scratch, "O_FIX", "logs", f"{rm['tag']}.stdout"), "rb").read(), zfx).decode(errors="replace"))
            sm_ = norm_text(mnorm(open(os.path.join(scratch, "O_MUTATE", "logs", f"{rm['tag']}.stdout"), "rb").read(), zm).decode(errors="replace"))
            nd += sum(1 for l in difflib.unified_diff(so_, sm_, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---")))
            out["mutate"].append(dict(tag=rm["tag"], rc=rm["rc"], differing_lines=nd, differs=nd > 0))
            P(f"  {rm['tag']}: rc {rm['rc']}; MUTATE vs FIX differing lines {nd} -> {'DIFFERS (the planted change shows up)' if nd else 'NO DIFFERENCE'}")
        l323 = [m for m in out["mutate"] if m["tag"].startswith("L323")]
        out["mutate_pass"] = bool(l323 and l323[0]["differs"])
        P(f"  [{'PASS' if out['mutate_pass'] else 'FAIL'}] MUTATE: the planted change shows up in L323's output (frozen; else the lane is void)")
    scrub = lambda t: t.replace(zo, "<mirror>").replace(zfx, "<mirror>").replace(scratch, "<scratch>")
    open(os.path.join(HERE, f"cfg305_compare_{group}_results.json"), "w").write(scrub(json.dumps(out, indent=1)))
    open(os.path.join(HERE, f"cfg305_compare_{group}.out"), "w").write(scrub("\n".join(lines) + "\n"))


if __name__ == "__main__":
    main(os.path.abspath(sys.argv[1]), sys.argv[2])
