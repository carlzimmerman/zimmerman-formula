#!/usr/bin/env python3
"""CFG265_route_recount.py: frozen-criteria P12, the mechanical half of the route recount (the hand half is in the README).
For each of the 25 table rows of the PAPER39 draft (read at 53f374ae2):
  - the lane directory and frozen-criteria file at 53f374ae2;
  - the row's commit exists, and touches the lane;
  - the frozen file's first commit versus the first commit that adds a script (.py) of the lane (the draft says
    "Each route below was given frozen criteria committed before its scripts");
  - the lane README's verdict-word lines (FAIL / NO-GO / UNDEFINED / NOT ADDRESSED / RESTATEMENT / p* / realisable /
    no mechanism / hand-check / post hoc / AMBIGUOUS), and the TEN_DOORS / DOOR11 result-table row for the door;
  - the table's class counts against the prose's 25 / 22 / 2 / 1.
Writes CFG265_route_recount.json. Exit 0 if it completed (discrepancies are printed, never an error exit)."""
import re, os, sys, json, subprocess, collections
from CFG265_common import *

VERD = re.compile(r'(FAIL|NO-GO|no-go|UNDEFINED|NOT ADDRESSED|RESTATEMENT|restatement|p\*|realis\w+|REALIS\w+|no mechanism|NO MECHANISM|hand-check|HAND-CHECK|phase[- ]1|PHASE[- ]1|post hoc|POST HOC|AMBIGUOUS|PASS|KILL|DEAD|binding|BINDING|verdict|VERDICT|scoped)')


def git(*a):
    r = subprocess.run(["git", "-C", REPO] + list(a), capture_output=True)
    return r.stdout.decode("utf-8", "replace").strip(), r.returncode


def first_add(paths_glob):
    """earliest commit (at or before PIN) that adds any path matching; returns (hash, ctime) or (None, None)"""
    out, _ = git("log", PIN, "--diff-filter=A", "--format=%H|%ct", "--", *paths_glob)
    lines = [l for l in out.split("\n") if l]
    if not lines:
        return None, None
    h, t = lines[-1].split("|")
    return h, int(t)


def is_ancestor(a, b):
    _, rc = git("merge-base", "--is-ancestor", a, b)
    return rc == 0


def main():
    tex, _ = pin_text(TEX_REL)
    E = extract(tex)
    rows = E['rows']
    allf = ls_pin("campaign_fresh_gravity/")
    ten, _ = pin_text("campaign_fresh_gravity/closure_map/TEN_DOORS_RESULT_2026-09-29.md")
    d11, _ = pin_text("campaign_fresh_gravity/closure_map/DOOR11_RESULT_2026-09-29.md")
    out = []
    cls_count = collections.Counter()
    for r in rows:
        cells = [c.strip() for c in r['text'].split('&')]
        route, lanecell, binding, cls = cells[0], cells[1], cells[2], cells[3]
        m = re.match(r'(CFG\d+[A-Z]?),\s*([0-9a-f]{7,})', lanecell)
        lane, commit = m.group(1), m.group(2)
        k = 'no-go' if cls.startswith('no-go') else ('no mechanism' if cls.startswith('no mechanism') else ('realisable' if cls.startswith('realisable') else 'other'))
        cls_count[k] += 1
        dirs = sorted(set(f.split('/')[1] for f in allf if re.match(r'campaign_fresh_gravity/%s_[^/]+/' % lane, f)))
        frozen = [f for f in allf if re.match(r'campaign_fresh_gravity/(%s_FROZEN_CRITERIA\.md|%s_[^/]+/(FROZEN_[A-Z_]+\.md|%s_FROZEN_CRITERIA\.md))$' % (lane, lane, lane), f)]
        ok_commit = git("cat-file", "-e", commit + "^{commit}")[1] == 0
        touched, _ = git("show", "--name-only", "--format=", commit)
        touches = any(('/%s_' % lane) in ('/' + t.split('/', 1)[-1]) or t.startswith('campaign_fresh_gravity/%s_' % lane) for t in touched.split('\n'))
        scripts = ['campaign_fresh_gravity/%s/*.py' % d for d in dirs] + ['campaign_fresh_gravity/%s_*.py' % lane]
        sh, st = first_add(scripts)
        fh, ft = first_add(frozen) if frozen else (None, None)
        if fh and sh:
            if fh == sh:   # full hashes (v1.1 fix: abbreviated hashes of different length made SAME COMMIT read as 'frozen first'; first output kept as CFG265_route_recount_v1_buggy.out)
                order = 'SAME COMMIT (frozen file and first script committed together)'
            elif is_ancestor(fh, sh):
                order = 'frozen first'
            else:
                order = 'SCRIPT FIRST'
        else:
            order = 'NO FROZEN FILE' if not fh else 'no script found'
        # README verdict lines
        rd = None
        for d in dirs:
            for cand in ('campaign_fresh_gravity/%s/README.md' % d, 'campaign_fresh_gravity/%s/%s_README.md' % (d, lane)):
                t, how = pin_text(cand)
                if t is not None and how != 'MISSING':
                    rd = (cand, t); break
            if rd: break
        vlines = []
        if rd:
            for i, ln in enumerate(rd[1].split('\n')[:80]):
                if VERD.search(ln) and len(vlines) < 6:
                    vlines.append('%d: %s' % (i + 1, ln.strip()[:220]))
        door = re.match(r"(\d+[A-Za-z'$\\{}\-]*)", route)
        trow = []
        for src, txt in (('TEN_DOORS_RESULT', ten), ('DOOR11_RESULT', d11)):
            for i, ln in enumerate(txt.split('\n')):
                if ln.startswith('|') and ('(%s,' % lane in ln or '(%s ' % lane in ln or '(%s)' % lane in ln):
                    trow.append('%s:%d: %s' % (src, i + 1, ln.strip()[:260]))
        out.append(dict(route=route, lane=lane, commit=commit, commit_exists=ok_commit, commit_touches_lane=touches, class_label=cls,
                        class_key=k, dirs=dirs, frozen=frozen, frozen_first_commit=fh[:10] if fh else None, first_script_commit=sh[:10] if sh else None, order=order,
                        readme=rd[0] if rd else None, readme_verdict_lines=vlines, result_table_rows=trow, tex_line=r['line']))
    prose = re.search(r'gives (\d+) routes: (\d+) scoped no-gos, two owner-directed', tex)
    counts = dict(total=len(rows), **cls_count)
    print('repo <repo>  tex at', PIN, ' current head', head_commit())
    print('TABLE ROWS:', len(rows), ' class counts from the table:', dict(cls_count))
    print('PROSE COUNT: total %s, scoped no-gos %s, hand-checks two, realisable one' % (prose.group(1), prose.group(2)))
    print('table vs prose agree:', len(rows) == int(prose.group(1)) and cls_count['no-go'] == int(prose.group(2)) and cls_count['no mechanism'] == 2 and cls_count['realisable'] == 1)
    print()
    for o in out:
        print('== %-32s %-8s %s  commit exists %s, touches lane %s | class "%s"' % (o['route'][:32], o['lane'], o['commit'], o['commit_exists'], o['commit_touches_lane'], o['class_label']))
        print('   dirs %s | frozen %s' % (o['dirs'], o['frozen']))
        print('   frozen first commit %s ; first script commit %s ; ORDER: %s' % (o['frozen_first_commit'], o['first_script_commit'], o['order']))
        for t in o['result_table_rows']:
            print('   ' + t)
        print('   README %s' % o['readme'])
        for v in o['readme_verdict_lines']:
            print('      ' + v)
    bad = [o for o in out if o['order'] != 'frozen first']
    print()
    print('ROUTES WHOSE FROZEN FILE WAS NOT COMMITTED STRICTLY BEFORE THE FIRST SCRIPT: %d of %d' % (len(bad), len(out)))
    for o in bad:
        print('   %-30s %-8s %s' % (o['route'][:30], o['lane'], o['order']))
    json.dump(dict(pin=PIN, counts=counts, prose=prose.groups() if prose else None, rows=out), open(os.path.join(HERE, 'CFG265_route_recount.json'), 'w'), indent=1)
    sys.exit(0)


if __name__ == '__main__':
    main()
