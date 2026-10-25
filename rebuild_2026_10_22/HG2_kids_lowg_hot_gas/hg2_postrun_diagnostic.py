"""HG2 POST-RUN DIAGNOSTIC -- not frozen, not graded. Written after the primary D (-0.294) was seen, to find what drives
its sign: the counted hot gas (moves BRIGHT groups up in g_bar) or g_obs itself (radius / richness at fixed sigma)."""
import json
from pathlib import Path
import numpy as np
import hg2_kids_lowg_hot_gas as hg2

hg1 = hg2.hg1
HERE = Path(__file__).resolve().parent
out = []


def say(s):
    print(s, flush=True); out.append(s)


gb, go, C = hg2.load(*hg2.BLUE); ref = hg2.Ref(gb, go, C)
groups, mem = hg1.load_groups(); erass = hg1.load_erass()
rows, _ = hg1.build(groups, mem, erass)
D0, nb, nf = hg1.D_stat(rows, hg2.deltas(rows, ref))
say(f'primary D (repeat) {D0:+.3f}  (BRIGHT {nb} / FAINT {nf})')
nogas = [dict(r, gbar=r['gbar']*0.5*r['mstar']/(0.5*r['mstar'] + r['mgas'])) for r in rows]
Dn, _, _ = hg1.D_stat(nogas, hg2.deltas(nogas, ref))
say(f'BRIGHT hot gas removed from g_bar (stars only in both arms): D {Dn:+.3f}')
bins = {}
for r in rows: bins.setdefault(int(np.floor(np.log10(r['sigma'])/0.1)), {'BRIGHT': [], 'FAINT': []})[r['flag']].append(r)
say('shared bins: median over arm of log g_bar, log g_obs, log r[Mpc], Nm, gas/stars(<r)  BRIGHT | FAINT')
res = {}
for k in sorted(bins):
    v = bins[k]
    if not (v['BRIGHT'] and v['FAINT']): continue
    def m(a, f): return float(np.median([f(r) for r in v[a]]))
    cols = [('lg_gbar', lambda r: np.log10(r['gbar'])), ('lg_gobs', lambda r: np.log10(r['gobs'])),
            ('lg_r', lambda r: np.log10(r['r_mpc'])), ('Nm', lambda r: r['Nm']), ('gas_star', lambda r: r['mgas']/(0.5*r['mstar']))]
    res[k/10] = {a: {c: m(a, f) for c, f in cols} for a in ('BRIGHT', 'FAINT')}
    b, f = res[k/10]['BRIGHT'], res[k/10]['FAINT']
    say(f'  {k/10:.1f}: ' + ' '.join(f'{b[c]:.2f}' for c, _ in cols) + '  |  ' + ' '.join(f'{f[c]:.2f}' for c, _ in cols))
(HERE/'hg2_postrun_diagnostic.out').write_text('\n'.join(out) + '\n')
(HERE/'hg2_postrun_diagnostic.json').write_text(json.dumps(dict(D=D0, D_no_hot_gas=Dn, bins=res), indent=1) + '\n')
