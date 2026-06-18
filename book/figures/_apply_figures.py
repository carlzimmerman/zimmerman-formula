#!/usr/bin/env python3
"""
Apply the book-figures workflow output: write each generating script, render it,
prune any that fail, and insert the sourced caption markdown into its chapter.

Input: JSON file (arg 1) = [{ch_num, file, figures:[{filename, kind, py, caption_md, anchor}]}, ...]
Run from book/figures/ ; chapters live one level up in book/.
"""
import json, os, sys, subprocess, re

FIGDIR = os.path.dirname(os.path.abspath(__file__))   # book/figures
BOOKDIR = os.path.dirname(FIGDIR)                       # book

def render(base, code):
    """Write <base>.py and run it; return (ok, msg). Expects it to save <base>.png."""
    py = os.path.join(FIGDIR, base + '.py')
    with open(py, 'w') as f:
        f.write(code if code.endswith('\n') else code + '\n')
    png = os.path.join(FIGDIR, base + '.png')
    if os.path.exists(png):
        os.remove(png)
    try:
        r = subprocess.run([sys.executable, py], cwd=FIGDIR,
                           capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return False, 'timeout'
    if r.returncode != 0:
        return False, (r.stderr.strip().splitlines() or ['nonzero exit'])[-1]
    if not os.path.exists(png) or os.path.getsize(png) < 1000:
        return False, 'no/empty png produced'
    return True, 'ok'

def insert(text, caption_md, anchor):
    """Insert caption_md as its own block after the paragraph containing anchor,
    else just before '## Summary', else at end."""
    block = '\n\n' + caption_md.strip() + '\n'
    if anchor and anchor != 'END':
        idx = text.find(anchor.strip())
        if idx != -1:
            # end of the paragraph that contains the anchor
            para_end = text.find('\n\n', idx)
            if para_end == -1:
                para_end = len(text)
            return text[:para_end] + block + text[para_end:]
    m = re.search(r'\n## Summary\b', text)
    if m:
        return text[:m.start()] + block + text[m.start():]
    return text.rstrip() + block

def main():
    data = json.load(open(sys.argv[1]))
    summary = {'rendered': 0, 'failed': [], 'chapters': 0, 'figs_total': 0}
    # one chapter at a time
    by_ch = {}
    for entry in data:
        by_ch.setdefault(entry['file'], []).extend(
            [(entry['ch_num'], fig) for fig in entry.get('figures', [])])

    for fname, figs in sorted(by_ch.items(), key=lambda kv: kv[0]):
        chpath = os.path.join(BOOKDIR, fname)
        if not os.path.exists(chpath):
            print('MISSING CHAPTER', fname); continue
        text = open(chpath).read()
        applied = 0
        for ch_num, fig in figs:
            summary['figs_total'] += 1
            base = re.sub(r'\.png$', '', fig['filename'])
            base = re.sub(r'[^A-Za-z0-9_]', '_', base)
            ok, msg = render(base, fig['py'])
            if not ok:
                summary['failed'].append(f"{base}: {msg}")
                continue
            summary['rendered'] += 1
            # make sure the caption points at the sanitized basename
            cap = fig['caption_md'].replace(fig['filename'], base + '.png')
            cap = cap.replace(re.sub(r'\.png$', '.py', fig['filename']), base + '.py')
            text = insert(text, cap, fig.get('anchor', 'END'))
            applied += 1
        if applied:
            with open(chpath, 'w') as f:
                f.write(text)
            summary['chapters'] += 1
        print(f"{fname}: {applied}/{len(figs)} figures inserted")

    print('\n=== SUMMARY ===')
    print(f"rendered {summary['rendered']}/{summary['figs_total']} figures across {summary['chapters']} chapters")
    if summary['failed']:
        print(f"FAILED ({len(summary['failed'])}):")
        for f in summary['failed']:
            print('  -', f)
    json.dump(summary, open(os.path.join(FIGDIR, '_apply_summary.json'), 'w'), indent=2)

if __name__ == '__main__':
    main()
