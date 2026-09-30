"""Shared helpers for parsing LaTeXML arXiv HTML tables (math alttext kept, asymmetric errors, limits, missing entries)."""
import csv, html, os, re
def flat(x):
    x = re.sub(r'<math[^>]*alttext="([^"]*)"[^>]*>.*?</math>', lambda m: " [" + html.unescape(m.group(1)) + "] ", x, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()
def rows(s, tid):
    i = s.index('<table id="%s"' % tid); j = s.index("</table>", i)
    return [[flat(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, flags=re.S)] for r in re.findall(r"<tr[^>]*>(.*?)</tr>", s[i:j], flags=re.S)]
def val(x):
    """(value, err_lo, err_hi, flag) flag in '', '<', '>', 'missing', 'unparsed:...'"""
    x = re.sub(r"\\hphantom\{[^}]*\}", "", x); x = re.sub(r"^(?:0\s+)+(?=[-+\d\[<])", "", x.strip())   # hidden-zero artefacts and \hphantom in some LaTeXML tables
    t = x.replace("[", "").replace("]", "").replace("\\rm", "").replace("\\,", "").replace("−", "-").strip()
    if t in ("", "…", "...", "-", "–", "—"): return (None, None, None, "missing")
    lim = "<" if t.startswith("<") else (">" if t.startswith(">") else ""); t = t.lstrip("<>").strip()
    m = re.match(r"([+-]?\d+\.?\d*)\s*\^\{\s*\+\s*(\d+\.?\d*)\}\s*_\{\s*-\s*(\d+\.?\d*)\}", t)
    if m: return (float(m.group(1)), float(m.group(3)), float(m.group(2)), lim)
    m = re.match(r"([+-]?\d+\.?\d*)\s*\\pm\s*(\d+\.?\d*)", t)
    if m: return (float(m.group(1)), float(m.group(2)), float(m.group(2)), lim)
    m = re.match(r"([+-]?\d+\.?\d*)", t.replace("\\farcs", ".").replace(" ", ""))
    return (float(m.group(1)), None, None, lim) if m else (None, None, None, "unparsed:" + x[:24])
def write(path, data):
    keys = []
    for d in data:
        for k in d:
            if k not in keys: keys.append(k)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows(data)
