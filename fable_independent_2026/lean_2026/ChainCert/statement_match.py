#!/usr/bin/env python3
"""Statement-match check for ChainCert: does each README claim match the Lean statement it cites?

`verify_chain.sh` proves that the theorems compile on standard axioms. It cannot tell whether a theorem
STATES what the README says it states (a missing premise, a weaker conclusion, a def that is not the
object the prose names). This script closes that gap mechanically, the way the formal-verification
supplement of Craig, arXiv:2610.09093 (sec. 12) pairs its Lean build with a separate correspondence
review:

  1. every identifier the README cites in backticks that names a declaration must resolve to exactly one
     ChainCert declaration (theorem, def, structure); dangling or ambiguous citations FAIL;
  2. every cited declaration must have a review in STATEMENT_MATCH_REVIEW.json whose stored hash equals
     the hash of the CURRENT Lean statement (signature + hypotheses, proof excluded) and of the README
     row text it was reviewed against; a missing or stale review FAILS, so editing a statement or a claim
     forces a re-review;
  3. a review verdict other than MATCH (OVERSTATES, PREMISE-HIDDEN, WRONG-OBJECT, UNDERSTATES) FAILS
     until the README (or the theorem) is corrected and re-reviewed.

Theorems listed in Axioms.lean but cited nowhere in the README are reported (UNCITED), not failed:
they are certified but unadvertised, so no claim can overstate them.

Usage:
  python3 ChainCert/statement_match.py               check; exit 0 iff all pass
  python3 ChainCert/statement_match.py --packets     write STATEMENT_MATCH_PACKETS.json (claim + statement per citation, for reviewers)
  MUTATE=1 python3 ChainCert/statement_match.py      controls: a dangling citation and a perturbed statement MUST both be caught (exit 0 iff both caught)

The review records judgements; this script only enforces that they exist, are current, and say MATCH.
It certifies nothing about the physics.
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
README = HERE / "README.md"
REVIEW = HERE / "STATEMENT_MATCH_REVIEW.json"
PACKETS = HERE / "STATEMENT_MATCH_PACKETS.json"
AXIOMS = HERE / "Axioms.lean"
VERDICTS_OK = {"MATCH"}
VERDICTS_ALL = {"MATCH", "OVERSTATES", "UNDERSTATES", "PREMISE-HIDDEN", "WRONG-OBJECT"}
# backticked README tokens that are not ChainCert declarations, each with its reason (never silently skipped)
NOT_DECLARATIONS = {
    "Classical.choice": "Lean core axiom",
    "Quot.sound": "Lean core axiom",
    "propext": "Lean core axiom",
    "r_led": "a variable name in the Exchange row",
    "sub_eq_iff_eq_add": "Mathlib lemma named in the script note",
}
FILE_RE = re.compile(r"\.(out|sh|lean|txt|json|py|md)$")

DECL_RE = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+)?(?:noncomputable\s+)?"
    r"(theorem|lemma|def|abbrev|structure|instance)\s+([^\s:({\[]+)"
)
NS_RE = re.compile(r"^\s*(namespace|end|section)\b\s*(\S*)")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def h(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def parse_lean():
    """Return {full_name: {module, kind, statement}}; statement = decl text up to its first top-level ':='."""
    decls = {}
    for f in sorted(HERE.glob("*.lean")):
        if f.name in ("Axioms.lean",) or f.name.startswith("_"):
            continue
        mod = f.stem
        lines = f.read_text().splitlines()
        stack = []  # namespace / section stack
        i = 0
        while i < len(lines):
            ln = lines[i]
            m = NS_RE.match(ln)
            if m:
                kw, nm = m.groups()
                if kw in ("namespace", "section"):
                    stack.append((kw, nm))
                elif stack:
                    stack.pop()
                i += 1
                continue
            m = DECL_RE.match(ln)
            if not m:
                i += 1
                continue
            kind, name = m.groups()
            buf = []
            j = i
            fields = []
            if kind == "structure":
                # fields up to the first blank line
                while j < len(lines) and (j == i or lines[j].strip()):
                    buf.append(re.sub(r"--.*$", "", lines[j]))
                    fm = re.match(r"^\s+([^\s:]+)\s*:", lines[j])
                    if j > i and fm:
                        fields.append(fm.group(1))
                    j += 1
            else:
                while j < len(lines):
                    t = lines[j]
                    k = t.find(":=")
                    if k >= 0:
                        buf.append(t[:k])
                        break
                    w = re.search(r"\s(where|\|)\s*$", t)
                    buf.append(t)
                    if w:
                        break
                    j += 1
            ns = ".".join(n for kw, n in stack if kw == "namespace" and n)
            full = f"{ns}.{name}" if ns and not name.startswith(ns + ".") else name
            decls[full] = {"module": mod, "kind": kind, "statement": norm(" ".join(buf)), "fields": fields}
            i = j + 1
    return decls


def readme_rows():
    """Each README table row (and each bullet) is one claim unit; return [(row_text, cited_tokens, modules)]."""
    rows = []
    for ln in README.read_text().splitlines():
        if ln.startswith("|") and not re.match(r"^\|\s*-", ln) and not ln.startswith("| link"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            where = cells[-1] if cells else ""
            mods = set(re.findall(r"`([A-Z][A-Za-z0-9]*)`", where))
            rows.append((norm(ln), re.findall(r"`([^`]+)`", ln), mods))
        elif ln.lstrip().startswith(("-", "*")) or ln.strip():
            rows.append((norm(ln), re.findall(r"`([^`]+)`", ln), set()))
    return rows


def resolve(tok, decls, mods):
    tok = tok.strip()
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.'₀-₉]*", tok):
        return None, "not-an-identifier"
    if tok in decls:
        return [tok], None
    cands = [k for k in decls if k == tok or k.endswith("." + tok)]
    if not cands:
        # a structure field (`hν_deep`, `CandidateB_Action.act`, `chain.hflat`) cites its structure
        head, _, fld = tok.rpartition(".")
        cands = [k for k, d in decls.items() if fld in d.get("fields", [])
                 and (not head or k.endswith(head) or head[0].islower())]
        if cands:
            return cands, "field"  # a premise shared by several structures cites each of them
    if len(cands) > 1 and mods:
        narrowed = [k for k in cands if decls[k]["module"] in mods]
        if narrowed:
            cands = narrowed
    if not cands:
        return [], None
    return cands, None


def collect(decls, rows):
    """citations: {full_name: [row_text,...]}; problems: list of str; module names are not citations."""
    modules = {d["module"] for d in decls.values()}
    cites, problems = {}, []
    for text, toks, mods in rows:
        for t in toks:
            if t in modules or t in ("ChainCert",) or t in NOT_DECLARATIONS or FILE_RE.search(t):
                continue
            r, why = resolve(t, decls, mods)
            if r is None:
                continue
            if r == []:
                # a bare lower-case/underscored token that looks like a theorem name but resolves nowhere
                if "_" in t or "." in t:
                    problems.append(f"DANGLING: `{t}` cited in README resolves to no ChainCert declaration")
                continue
            if len(r) > 1 and why != "field":
                problems.append(f"AMBIGUOUS: `{t}` -> {r}; qualify it in the README")
                continue
            for name in r:
                cites.setdefault(name, [])
                if text not in cites[name]:
                    cites[name].append(text)
    return cites, problems


def key_hash(decl, rows_text):
    return h(decl["statement"] + "\n##\n" + "\n".join(sorted(rows_text)))


def check(decls, rows, review):
    cites, problems = collect(decls, rows)
    stale = missing = bad = 0
    for name, rtexts in sorted(cites.items()):
        kh = key_hash(decls[name], rtexts)
        r = review.get(name)
        if r is None:
            missing += 1
            problems.append(f"UNREVIEWED: {name}")
        elif r.get("hash") != kh:
            stale += 1
            problems.append(f"STALE: {name} (statement or README claim changed since review)")
        elif r.get("verdict") not in VERDICTS_OK:
            bad += 1
            problems.append(f"{r.get('verdict')}: {name} -- {r.get('note','')}")
    listed = set(re.findall(r"^#print axioms (\S+)", AXIOMS.read_text(), re.M))
    uncited = sorted(n for n in listed if n not in cites)
    return cites, problems, uncited, (missing, stale, bad)


def unanchored(decls, rows):
    """table rows that point at a module but name no declaration: their claims cannot be statement-matched"""
    out = []
    for text, toks, mods in rows:
        if not mods or not text.startswith("|"):
            continue
        if not any(resolve(t, decls, mods)[0] for t in toks if t not in mods):
            out.append(text[:90])
    return out


def main():
    decls = parse_lean()
    rows = readme_rows()
    review = json.loads(REVIEW.read_text())["reviews"] if REVIEW.exists() else {}

    if "--packets" in sys.argv:
        cites, problems = collect(decls, rows)
        out = [
            {"name": n, "module": decls[n]["module"], "kind": decls[n]["kind"],
             "statement": decls[n]["statement"], "readme_claims": rt, "hash": key_hash(decls[n], rt)}
            for n, rt in sorted(cites.items())
        ]
        PACKETS.write_text(json.dumps({"packets": out, "citation_problems": problems}, indent=1, ensure_ascii=False))
        print(f"packets: {len(out)} cited declarations; citation problems: {len(problems)} -> {PACKETS.name}")
        for p in problems:
            print("  " + p)
        return 0

    if os.environ.get("MUTATE") == "1":
        caught = 0
        rows_m = rows + [("| mutated | `mutated_claim_does_not_exist` | | `Chain` |", ["mutated_claim_does_not_exist"], {"Chain"})]
        _, p1, _, _ = check(decls, rows_m, review)
        c1 = any("DANGLING: `mutated_claim_does_not_exist`" in p for p in p1)
        cites, _ = collect(decls, rows)
        victim = next((n for n in sorted(cites) if review.get(n, {}).get("hash") == key_hash(decls[n], cites[n])), None)
        c2 = False
        if victim:
            decls_m = dict(decls)
            decls_m[victim] = dict(decls[victim], statement=decls[victim]["statement"] + " (h_extra : True)")
            _, p2, _, _ = check(decls_m, rows, review)
            c2 = any(p.startswith(f"STALE: {victim} ") for p in p2)
        caught = int(c1) + int(c2)
        print(f"MUTATE: dangling citation caught: {c1}; perturbed statement ({victim}) caught as stale: {c2}")
        print("MUTATE: controls PASS (both caught)" if caught == 2 else "MUTATE: controls FAIL")
        return 0 if caught == 2 else 1

    bad_verdicts = [n for n, r in review.items() if r.get("verdict") not in VERDICTS_ALL]
    cites, problems, uncited, (missing, stale, bad) = check(decls, rows, review)
    problems += [f"INVALID-VERDICT: {n}" for n in bad_verdicts]
    print(f"cited declarations: {len(cites)}; reviewed MATCH: {len(cites) - missing - stale - bad}; "
          f"unreviewed: {missing}; stale: {stale}; non-MATCH: {bad}; citation problems: "
          f"{len(problems) - missing - stale - bad - len(bad_verdicts)}")
    print(f"theorems in Axioms.lean not cited in the README (UNCITED, informational): {len(uncited)}")
    un = unanchored(decls, rows)
    print(f"README table rows naming a module but no declaration (UNANCHORED, informational -- not statement-matched): {len(un)}")
    for u in un:
        print("    " + u)
    for p in problems:
        print("  " + p)
    if problems:
        print("STATEMENT-MATCH: FAIL")
        return 1
    print("STATEMENT-MATCH: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
