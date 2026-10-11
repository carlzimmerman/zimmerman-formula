"""Independent HTML table quality extraction; sources immutable."""
import collections
import re
from pathlib import Path


def audit():
    here=Path(__file__).resolve().parent
    html=(here/'sources/rihtarsic_v2.html').read_text()
    base,seen={},{}
    for row in re.findall(r'<tr\b[^>]*>(.*?)</tr>',html,re.S):
        cells=re.findall(r'<td\b[^>]*>(.*?)</td>',row,re.S)
        if len(cells)!=8:
            continue
        ident=re.sub('<[^>]+>','',cells[0]).strip()
        m=re.fullmatch(r'([KN]\d+)[a-z]?\.\d+',ident)
        if not m:
            continue
        markers=re.findall(r'class="ltx_text">([gsb])</span>',cells[6])
        if m[1] not in base:
            if not markers:
                raise ValueError('No initial galaxy quality for '+ident)
            base[m[1]]=markers[-1].upper()
        if ident in seen:
            raise ValueError('Duplicate HTML image')
        seen[ident]=markers[-1].upper() if markers else base[m[1]]
    lines=(here.parent/'cluster_projection_2026_10_11/sources/tablea1.dat').read_text().splitlines()
    raw={s[:6].strip():s[71] for s in lines}
    return dict(same_all_rows=len(seen)==199 and seen==raw,
                html_counts=dict(collections.Counter(seen.values())),
                cds_counts=dict(collections.Counter(raw.values())))
