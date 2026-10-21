#!/usr/bin/env python3
"""Assemble a5_zenodo_ledger.json from the cached records + repo probes.

Every row carries:
  id / doi / date / title / version
  relevance      core | peripheral | non_physics
  bears_on       subset of a,b,c,d,e  (a kappa/a0 origin; b medium/saturation;
                 c lensing/GW/PPN/stability; d 24 pc-1 kpc; e prediction/kill)
  claims         verbatim sentences (substrings of the normalised abstract)
                 with the numbers they contain and the categories they hit
  state          integrated_standing | integrated_paper | stale_copy |
                 superseded | only_zenodo | not_applicable
  repo_evidence  DOI files, number probes with hits, mapped paper, mtime
  delta          what the record changes / what is NOT absorbed

Quotes are never retyped: they are selected from the normalised abstract and
re-checked as substrings here, so the ledger cannot drift from the source.
"""
import json
import os
import re
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_zenodo")
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

CANON = ["README.md", "STANDING.md", "FRAMEWORK_EQUATIONS_2026-10-15.md",
         "campaign_fresh_gravity/LEDGER.md", "RETRACTIONS.md",
         "CAMPAIGN_LEDGER.md"]

PERIPHERAL = {
    "19654433", "19666437", "19674179", "19681243", "19683618", "19696766",
    "19720906", "19822806", "19860761", "19864028", "20018005", "20057441",
    "20077566", "20174532", "20174536", "20315552", "20431292", "20669482",
    "21936586",
}

# Records that belong to the constants-numerology bundle the repo explicitly
# retracted (real_research/ZENODO_PUBLICATION_MAP.md): alpha = 4Z^2+3, the
# 36/60/65-constant census, Koide/CKM/PMNS, the 20.6 Gpc topology.
RETRACTED_Z = {
    "19114050", "19123455", "19130292", "19140259", "19142025", "19163583",
    "19199167", "19212718", "19244651", "19272815", "19303555", "19864028",
    "20090210", "20315552", "20528908",
}

NUM = re.compile(r"(?<![\w.])[-+]?(?:\d+(?:\.\d+)?(?:[eE][-+]?\d+)?|\.\d+)")


def norm(t):
    t = re.sub(r"<[^>]+>", " ", t)
    for a, b in [("&nbsp;", " "), ("&times;", "x"), ("&sup2;", "2"),
                 ("&sup3;", "3"), ("&minus;", "-"), ("&amp;", "&"),
                 ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'),
                 ("&asymp;", "~"), ("&prop;", "proportional to"),
                 ("&radic;", "sqrt"), ("&pi;", "pi"), ("&rho;", "rho"),
                 ("&Lambda;", "Lambda"), ("&kappa;", "kappa"),
                 ("&sigma;", "sigma"), ("&chi;", "chi"), ("&delta;", "delta"),
                 ("&alpha;", "alpha"), ("&gamma;", "gamma"), ("&mu;", "mu"),
                 ("&nu;", "nu"), ("&Omega;", "Omega"), ("&tau;", "tau"),
                 ("&epsilon;", "epsilon"), ("&ell;", "ell"), ("&mdash;", "-"),
                 ("&ndash;", "-"), ("&plusmn;", "+-"), ("&ge;", ">="),
                 ("&le;", "<="), ("&sim;", "~")]:
        t = t.replace(a, b)
    t = re.sub(r"&#(\d+);", "", t)
    t = re.sub(r"&[a-zA-Z]+;", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def sents(t):
    return [s.strip() for s in re.split(r"(?<=[.;])\s+(?=[A-Z(])", t) if s.strip()]


def cats(s):
    low = s.lower()
    out = []
    if any(k in low for k in ("kappa", "a0", "a_0", "acceleration scale",
                              "dark-energy density", "rho_lambda", "rho_de",
                              "coefficient", "normalis", "normaliz", "de sitter",
                              "unruh", "vacuum energy")):
        out.append("a")
    if any(k in low for k in ("medium", "saturat", "capacity", "dielectric",
                              "polariz", "polaris", "cold energy", "condensate",
                              "superfluid", "elastic", "solid", "tethered",
                              "displacement", "stiffness", "bulk modulus",
                              "sound speed", "interpolat", "quadrature",
                              "kernel", "n = 1", "n=1", "n = 2", "n=2")):
        out.append("b")
    if any(k in low for k in ("lensing", "gw", "gravitational wave", "ppn",
                              "cassini", "shapiro", "stability", "ghost",
                              "instabilit", "preferred frame", "lorentz",
                              "ephemeris", "conformal", "slip", "c_t", "gamma")):
        out.append("c")
    if re.search(r"\b\d+(\.\d+)?\s*(pc|kpc)\b", low):
        out.append("d")
    if any(k in low for k in ("predict", "falsif", "kill", "test", "pre-registered",
                              "forecast", "no-go", "excluded", "excludes",
                              "detect", "discrimin", "upper limit", "sigma",
                              "ppm", "tension", "confin")):
        out.append("e")
    return out


def pick_claims(text, limit=4):
    """Sentences with numbers, ranked by number count then category count."""
    scored = []
    for s in sents(text):
        ns = [m.group(0) for m in NUM.finditer(s)]
        c = cats(s)
        if not ns and not c:
            continue
        if not c:
            continue
        score = (min(len(ns), 6), len(c), min(len(s), 400) / 400)
        scored.append((score, s, ns, c))
    scored.sort(key=lambda x: (-x[0][0], -x[0][1], x[0][2]))
    out, seen = [], set()
    for score, s, ns, c in scored:
        key = s[:60]
        if key in seen:
            continue
        seen.add(key)
        q = s[:600]
        out.append({"quote": q,
                    "numbers": sorted({mm.group(0) for mm in NUM.finditer(q)}),
                    "cats": c})
        if len(out) >= limit:
            break
    out.sort(key=lambda d: text.find(d["quote"]))
    return out


def read_canon():
    txt = {}
    for f in CANON:
        p = os.path.join(REPO, f)
        if os.path.exists(p):
            txt[f] = norm(open(p, errors="ignore").read())
    return txt


def main():
    recs = json.load(open(os.path.join(CACHE, "all_records.json")))
    hits = json.load(open(os.path.join(CACHE, "repo_hits.json")))
    pmap = json.load(open(os.path.join(CACHE, "paper_map.json")))
    manual = {}
    mp = os.path.join(CACHE, "manual.json")
    if os.path.exists(mp):
        manual = json.load(open(mp))
    canon = read_canon()

    # duplicate groups: identical normalised title -> later id wins
    by_title = {}
    for r in recs:
        k = re.sub(r"[^a-z0-9]+", " ", (r["title"] or "").lower()).strip()
        k = re.sub(r"\(working note\)|version \d+(\.\d+)?", "", k).strip()
        by_title.setdefault(k, []).append(r)
    superseded_by = {}
    for k, group in by_title.items():
        if len(group) > 1:
            group = sorted(group, key=lambda r: (r["date"] or "", r["id"]))
            for r in group[:-1]:
                superseded_by[str(r["id"])] = str(group[-1]["id"])

    rows = []
    for r in recs:
        rid = str(r["id"])
        text = norm(r["description"])
        h = hits[rid]
        p = pmap.get(rid, {})
        m = manual.get(rid, {})
        claims = pick_claims(text)
        if not claims:
            # fallback: keep at least one verbatim number-bearing sentence so the
            # row is auditable even when no category keyword matches
            fb = [x for x in sents(text) if any(ch.isdigit() for ch in x)][:2]
            claims = [{"quote": x[:600],
                       "numbers": sorted({mm.group(0) for mm in NUM.finditer(x[:600])}),
                       "cats": cats(x) or ["unclassified"]} for x in fb]
        anchor = m.get("anchor")
        if anchor:
            hit = [x for x in sents(text) if anchor in x]
            if not hit:
                raise SystemExit(f"anchor not found for {rid}: {anchor!r}")
            q = hit[0]
            claims = [{"quote": q, "numbers": sorted({mm.group(0) for mm in NUM.finditer(q)}),
                       "cats": cats(q)}] + [c for c in claims if c["quote"] != q]
        bcats = sorted({c for cl in claims for c in cl["cats"]})

        relevance = m.get("relevance")
        if relevance is None:
            if rid == "10574975":
                relevance = "non_physics"
            elif rid in PERIPHERAL:
                relevance = "peripheral"
            else:
                relevance = "core"

        # ---- state -------------------------------------------------------
        # Rule (documented in report.md):
        #   integrated      >=2 distinctive numbers found in NON-paper repo files
        #                   (scripts, results, ledgers, standing docs)
        #   paper_only      mapped manuscript covers >=70% of numbers, but <2
        #                   numbers appear outside the manuscripts
        #   catalogued_only DOI appears (README table / deposit metadata) but the
        #                   claims do not
        #   superseded      earlier deposit of a later record, or a retracted class
        #   not_applicable  namesake
        ev = h.get("evidence_hits", {}) or {}
        state = m.get("state")
        if state is None:
            if relevance == "non_physics":
                state = "not_applicable"
            elif relevance == "peripheral":
                state = "out_of_scope"
            elif rid in RETRACTED_Z:
                state = "superseded"
            elif rid in superseded_by:
                state = "superseded"
            elif len(ev) >= 2:
                state = "integrated"
            elif p.get("tex_exists") and p.get("probe_total") and \
                    p["probe_present"] >= max(1, 0.7 * p["probe_total"]):
                state = "paper_only"
            elif h["doi_hits"]:
                state = "catalogued_only"
            else:
                state = "only_zenodo"

        # ---- delta -------------------------------------------------------
        delta = m.get("delta")
        if delta is None:
            if state == "not_applicable":
                delta = "Namesake record (Carl Zimmerman, wildlife genetics); no bearing on the programme."
            elif state == "superseded":
                if rid in RETRACTED_Z:
                    delta = ("Part of the constants-numerology bundle the repo retracted "
                             "(real_research/ZENODO_PUBLICATION_MAP.md); the claim is withdrawn, "
                             "not merely unintegrated.")
                elif superseded_by.get(rid):
                    delta = (f"Earlier deposit of {superseded_by[rid]}; this version adds nothing "
                             f"the later record does not carry.")
                else:
                    delta = ("Constants-numerology bundle later retracted in repo "
                             "(real_research/ZENODO_PUBLICATION_MAP.md); kept on the record only.")
            elif state == "integrated":
                delta = (f"{len(ev)} distinctive numbers appear in non-paper repo files "
                         f"({', '.join(sorted({f.split('/')[1] if '/' in f else f for v in ev.values() for f in v})[:3])}); absorbed.")
            elif state == "paper_only":
                delta = (f"Manuscript {p['tex']} carries {p['probe_present']}/{p['probe_total']} of the "
                         f"numbers, but no script or ledger row does; absorbed at publication level only.")
            elif state == "out_of_scope":
                delta = ("Separate claim class (therapeutics / plant / aroma / other field); "
                         "outside the four gravity questions, retained only so the count is complete.")
            elif state == "catalogued_only":
                delta = ("Catalogued by DOI in the repo but no distinctive number of the record "
                         "appears in any script, result or ledger; the claim is not integrated.")
            else:
                delta = ("No repo paper, no DOI citation and none of its distinctive numbers "
                         "found; the claim stands only in the Zenodo record.")

        row = {
            "id": r["id"], "doi": r["doi"], "date": r["date"],
            "title": r["title"], "version": r.get("version"),
            "relevance": relevance,
            "bears_on": m.get("bears_on", bcats),
            "claims": claims,
            "state": state,
            "repo_evidence": {
                "doi_files": [f for f in h["doi_files"] if "DS_FINAL" not in f],
                "paper": p.get("tex"),
                "paper_mtime": (time.strftime("%Y-%m-%d", time.localtime(p["tex_mtime"]))
                                if p.get("tex_mtime") else None),
                "numbers_found": {k: v["n"] for k, v in h["number_hits"].items()},
            },
            "delta": delta,
            "fingerprint": m.get("fingerprint"),
            "test": m.get("test"),
        }
        rows.append(row)

    # hard verification: every quote substring of its abstract
    byid = {r["id"]: norm(r["description"]) for r in recs}
    bad = [(row["id"], cl["quote"][:60]) for row in rows for cl in row["claims"]
           if cl["quote"] not in byid[row["id"]]]
    assert not bad, f"quote drift: {bad[:3]}"

    counts = {}
    for row in rows:
        counts[row["state"]] = counts.get(row["state"], 0) + 1
    bears = {}
    for row in rows:
        for c in row["bears_on"]:
            if c in "abcde" and len(c) == 1:
                bears[c] = bears.get(c, 0) + 1

    ledger = {
        "lane": "A5_zenodo",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source": {
            "api": "https://zenodo.org/api/records?q=creators.name:%22Zimmerman%2C%20Carl%22&sort=newest",
            "reported_total": 178, "fetched": len(recs),
            "query_note": "size capped at 25 unauthenticated; 8 pages fetched",
        },
        "normalization": ("HTML tags stripped; named/numeric entities decoded "
                          "(&nbsp; &times; &sup2; &radic; &pi; ...); whitespace "
                          "collapsed. Quotes are substrings of that normalised text."),
        "counts": {"records": len(rows), **counts},
        "bears_on_counts": bears,
        "records": rows,
    }
    json.dump(ledger, open(os.path.join(HERE, "a5_zenodo_ledger.json"), "w"),
              indent=1, sort_keys=False)
    print(json.dumps({"counts": counts, "bears_on": bears,
                      "records": len(rows)}, indent=1))


if __name__ == "__main__":
    main()
