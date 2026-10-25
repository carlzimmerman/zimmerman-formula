#!/usr/bin/env python3
"""Build the Dark River Tavern Menu page: every Crispy Fried Chicken board tile as a dish, with its data picture.

Reads board_tiles.json (exported from make_status_board.py), captions/col*.json and img/*.png; writes menu.html with
the pictures embedded. Plot-free: it only assembles what the figure scripts made. A tile without a caption is listed
with 'picture not ready' instead of being dropped.
"""
import base64
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
STATUS = {"PASS": ("pass", "Passes"), "COND": ("cond", "Conditional"), "UNDEC": ("undec", "Not decidable yet"),
          "FAIL": ("fail", "Fails"), "OPEN": ("open", "Open"), "STALE": ("open", "Not yet recomputed")}
COURSES = [  # board column -> menu course
    ("Starters", "The chassis: the relativistic theory underneath"),
    ("Mains", "Galaxies"),
    ("House specials", "The excess family, still open"),
    ("From the cellar", "Cosmology and a0 over time"),
    ("Nightcaps", "The deep why and the parent theory"),
]


def esc(s):
    return html.escape(str(s), quote=True)


def load():
    board = json.loads((HERE / "board_tiles.json").read_text())
    caps = {}
    for f in sorted((HERE / "captions").glob("col*.json")):
        for c in json.loads(f.read_text()):
            caps[(c["name"])] = c
    return board, caps


def dish(i, t, cap):
    st = t["st"] if t["st"] in STATUS else "OPEN"
    cls, word = STATUS[st]
    if t.get("was"):
        cls, word = "open", "Not yet recomputed"
    out = [f'<article class="dish" data-st="{cls}" id="d{i}">',
           f'<header class="dish-head"><h3>{esc(t["name"])}</h3><span class="leader" aria-hidden="true"></span>'
           f'<span class="chip {cls}">{word}</span></header>',
           f'<p class="board-note">On the board: {esc(t["note"])}</p>']
    img = HERE / "img" / f'{cap["slug"]}.png' if cap else None
    if cap and img.exists():
        b64 = base64.b64encode(img.read_bytes()).decode()
        out.append(f'<button class="plate" type="button" aria-label="Enlarge the picture for {esc(t["name"])}">'
                   f'<img loading="lazy" src="data:image/png;base64,{b64}" alt="{esc(cap.get("picture", t["name"]))}">'
                   f'</button>')
        out.append('<dl class="recipe">')
        for k, lab in (("data", "On the plate"), ("picture", "How it is plated"), ("why", "Why it " +
                       {"pass": "passes", "fail": "fails", "cond": "is conditional", "undec": "is not decidable yet",
                        "open": "is still open"}[cls])):
            if cap.get(k):
                out.append(f"<dt>{lab}</dt><dd>{esc(cap[k])}</dd>")
        out.append("</dl>")
        srcs = cap.get("sources", [])
        if srcs:
            out.append('<p class="src">Sources: ' + "; ".join(
                f'<code>{esc(s.get("path", ""))}</code>' + (f' @ {esc(s["commit"])}' if s.get("commit") else "")
                for s in srcs) + "</p>")
    else:
        out.append('<p class="pending">Picture not ready yet.</p>')
    out.append(f'<p class="lanes">Lanes: {esc(" / ".join(t["lanes"]))}</p></article>')
    return "\n".join(out)


def main():
    board, caps = load()
    tiles = board["tiles"]
    counts = {}
    for t in tiles:
        k = "open" if t.get("was") else STATUS.get(t["st"], STATUS["OPEN"])[0]
        counts[k] = counts.get(k, 0) + 1
    tally = "".join(f'<button type="button" class="filter chip {k}" data-f="{k}" aria-pressed="false">'
                    f'{w} <b>{counts.get(k, 0)}</b></button>'
                    for k, w in (("pass", "Passes"), ("cond", "Conditional"), ("undec", "Not decidable"),
                                 ("fail", "Fails"), ("open", "Open")))
    body = []
    n = 0
    for c, (course, sub) in enumerate(COURSES):
        items = [t for t in tiles if t["col"] == c]
        body.append(f'<section class="course" aria-labelledby="c{c}"><div class="course-head">'
                    f'<h2 id="c{c}">{course}</h2><p>{esc(sub)} · {len(items)} dishes</p></div><div class="dishes">')
        for t in items:
            n += 1
            body.append(dish(n, t, caps.get(t["name"])))
        body.append("</div></section>")
    page = (HERE / "scripts" / "menu_template.html").read_text()
    page = page.replace("{{TALLY}}", tally).replace("{{COURSES}}", "\n".join(body)).replace("{{N}}", str(len(tiles)))
    (HERE / "menu.html").write_text(page)
    done = sum(1 for t in tiles if t["name"] in caps)
    print(f"menu.html: {len(tiles)} dishes, {done} with pictures, {(HERE / 'menu.html').stat().st_size/1e6:.1f} MB")


if __name__ == "__main__":
    main()
