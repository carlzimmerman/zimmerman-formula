#!/usr/bin/env python3
"""Stage 5: reconcile the previous surname-grep index (182 entries, commit c5fddc2191) with the verified index.

Nothing from the old index is dropped silently: every old entry gets a row in citations/CORRECTIONS.md saying what
the verified index found for that name, and every old page path citations/<slug>/index.md keeps working as a pointer
to the right people. The one old entry that was the repository's own author is removed (own work is not part of an
index of people whose work the repository uses).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CITE_DIR, DATA, REPO, load_json, norm_family, own_author_families, strip_accents  # noqa: E402

OLD_COMMIT = "c5fddc2191"
NOTE = {  # why an old surname count was wrong (checked by hand against the scripts)
    "li": "the old count matched every 'Li' (lithium, HTML <li>, and a dozen different researchers named Li)",
    "fisher": "the old count mixed R. A. Fisher's Fisher information/matrix into J. Richard Fisher's entry",
    "white": "the old count matched the word 'white' (white dwarf, white noise) as well as Simon D. M. White",
    "king": "the old count matched the word 'king' as well as Ivan King",
    "gross": "no 'Andreas Gross' is cited; 'Gross' in the scripts is E. P. Gross (Gross–Pitaevskii) or D. J. Gross",
    "mead": "'Mead' in the scripts is Alexander J. Mead (HMcode), not 'James Mead'",
    "brout": "'Brout' in the scripts is Dillon Brout (Pantheon+), not Robert Brout",
    "rubin": "'Rubin' in the scripts includes David Rubin (Union3) and Donald Rubin (Gelman–Rubin), not only Vera Rubin",
    "hunter": "'Hunter' may be Deidre A. Hunter (LITTLE THINGS) or John D. Hunter (Matplotlib)",
    "lorenz": "'Lorenz' may be Ludvig Lorenz (Lorenz gauge) or Edward Lorenz (Lorenz attractor)",
    "klein": "'Klein' may be Oskar Klein (Klein–Gordon, Kaluza–Klein) or Felix Klein",
    "ting": "the old count matched 'Ting' in unrelated text; Samuel C. C. Ting is not cited by the scripts",
    "yang": "the old count merged several researchers named Yang with C.-N. Yang (Yang–Mills)",
    "singh": "the old count merged several researchers named Singh",
    "mcgaug": "old slug was a truncated alias of McGaugh",
}


def old_rows():
    txt = subprocess.run(["git", "-C", str(REPO), "show", f"{OLD_COMMIT}:CITATIONS.md"], capture_output=True,
                         text=True, check=True).stdout
    rows = []
    for line in txt.splitlines():
        m = re.match(r"\|\s*(.+?)\s*\|\s*(.*?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*\[citations/([^/]+)/\]", line)
        if m:
            rows.append({"name": m.group(1), "aff": m.group(2), "files": int(m.group(3)), "occ": int(m.group(4)),
                         "slug": m.group(5)})
    return rows


def family_of(name: str) -> str:
    n = name.replace("’", "'")
    if n.endswith(" team"):
        return n
    toks = n.split()
    i = len(toks) - 1
    while i > 0 and toks[i - 1].lower() in {"de", "van", "von", "'t", "le", "la", "di", "der", "den"}:
        i -= 1
    return " ".join(toks[i:])


def main():
    people = load_json(DATA / "people.json.gz")
    own = own_author_families()
    by_fam = {}
    for pid, p in people.items():
        by_fam.setdefault(norm_family(p["family"]), []).append(p)
    rows = old_rows()
    table = []
    removed_own = 0
    for r in rows:
        fam = family_of(r["name"])
        nf = norm_family(fam if r["slug"] != "mcgaug" else "McGaugh")
        slug_dir = CITE_DIR / r["slug"]
        if nf in own:
            removed_own += 1
            if slug_dir.exists():
                for f in slug_dir.iterdir():
                    f.unlink()
                slug_dir.rmdir()
            continue
        cands = sorted(by_fam.get(nf, []), key=lambda p: -p["n_files"])
        g_old = strip_accents(r["name"].split()[0]).lower().strip(".")
        exact = [p for p in cands if strip_accents(p["given"]).lower().split(" ")[0].strip(".") == g_old
                 or (len(g_old) == 1 and strip_accents(p["given"]).lower()[:1] == g_old)]
        if r["slug"] == "clearpotential":
            status, main = "was a paper's short name, not a person", None
        elif exact:
            status, main = "confirmed", exact[0]
        elif cands:
            status, main = "corrected: the scripts credit a different person with this surname", None
        else:
            status, main = "not credited: no scanned script uses this person's published work", None
        link = lambda p: f"[{p['display']}](people/{p['id']}.md)" if not p["collab_only"] else p["display"]  # noqa: E731
        now = (f"{link(main)} — {main['n_files']} scripts, {len(main['works'])} works" if main else
               ("; ".join(f"{link(p)} ({p['n_files']})" for p in cands[:4]) if cands else "—"))
        note = NOTE.get(r["slug"], "")
        if r["slug"] == "clearpotential":
            note = "'ClearPotential 2026' is arXiv:2512.09989; its real authors are credited through that paper"
        table.append((r, status, now, note))
        # keep the old URL working as a pointer
        slug_dir.mkdir(exist_ok=True)
        lines = [f"# {r['name']} → moved to the verified index", "",
                 f"This page belonged to the previous surname-count index ({r['files']} files, {r['occ']} word matches, "
                 "all file types). The index now credits people only through verified publications used by the "
                 "scripts — see [how it is built](../README.md).", ""]
        if main:
            lines.append(f"**Now:** {now}.")
        elif cands:
            lines.append("**People with this surname credited by the scripts:**")
            lines.append("")
            for p in cands[:12]:
                lines.append(f"- {link(p).replace('(people/', '(../people/')} — {p['n_files']} scripts")
        else:
            lines.append("**Now:** no scanned script uses this person's published work (the old count came from "
                         "the word appearing in notes, papers or data).")
        if note:
            lines += ["", f"*Why the old count differed:* {note}."]
        lines += ["", "[People A–Z](../people/README.md) · [Corrections to the old index](../CORRECTIONS.md)"]
        (slug_dir / "index.md").write_text("\n".join(lines).replace("](people/", "](../people/") + "\n", encoding="utf-8")
    out = ["# Corrections to the previous citation index", "",
           "The previous index (182 names, commit c5fddc2191) counted surname matches in every file type. The verified "
           "index credits a person only when a scanned script uses a publication they wrote. Every old entry is "
           "listed here with what the verified index found.", "",
           f"Removed: {removed_own} entry for the repository's own author (own work is not part of this index).", "",
           "| old entry | old count (files, all types) | status now | now | why the old count differed |",
           "|---|---:|---|---|---|"]
    for r, status, now, note in sorted(table, key=lambda t: t[0]["name"]):
        out.append(f"| {r['name']} | {r['files']} | {status} | {now} | {note} |")
    (CITE_DIR / "CORRECTIONS.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    c = {}
    for _, s, _, _ in table:
        c[s] = c.get(s, 0) + 1
    print(f"old entries: {len(rows)}; {c}; own-author entries removed: {removed_own}")


if __name__ == "__main__":
    main()
