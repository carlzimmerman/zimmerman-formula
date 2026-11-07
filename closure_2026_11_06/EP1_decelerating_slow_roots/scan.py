"""EP1 witness scan + KA3. AC23 scan.py's roots() executed from AC23's committed file (source up to 'out = {}').
Criteria: CRITERIA.md (d8fc918584). Kappa = 1/2 FITTED; not theory closed. Run from the repo root."""
import itertools, json
from pathlib import Path
import mpmath as mp
D = Path('closure_2026_11_06/EP1_decelerating_slow_roots')
src = Path('action_search_2026_11_05/AC23_fresh_slow_roots/scan.py').read_text().split('\nout = {}')[0]
ns = {'__name__': 'ac23scan'}; exec(compile(src, 'AC23/scan.py[roots]', 'exec'), ns); roots = ns['roots']
out = {}
ac3 = [r for r in json.loads(Path('action_search_2026_11_05/AC3_matter_gradients/evidence/finite_v3/result.json').read_text())['rows']
       if r['epsilon_phi'] == '2']
err = 0.0; wit3 = []
for r in ac3:
    m = roots(r['epsilon_phi'], r['epsilon_m'], r['Lstar'], r['k'])
    with mp.workdps(80):
        for z, y in zip(m['omega2'], r['omega2']):
            err = max(err, float(abs(mp.mpmathify(z) - mp.mpmathify(y)) / max(1, abs(mp.mpmathify(y)))))
    if m['negative_roots'] > 0: wit3.append([r['epsilon_phi'], r['epsilon_m'], r['Lstar'], r['k']])
want = [['2', '.9', '.001', '10'], ['2', '.9', '.001', '100']]
out['KA3'] = dict(n_cells=len(ac3), max_rel_err=err, witnesses=wit3, pass_=bool(err <= 1e-25 and sorted(wit3) == sorted(want) and len(ac3) == 27))
grids = {'A': (['2'], ['0.5', '0.75', '0.97'], ['5e-4', '5e-3', '5e-2'], ['5', '20', '60']),
         'B': (['2'], ['0.85', '0.93'], ['2e-4', '2e-3', '2e-2'], ['8', '40', '150'])}
rows = [roots(*c) for c in itertools.product(*grids['A'])]; out['grid_A'] = rows
wit = [r for r in rows if r['negative_roots'] > 0]
out['grid_B_used'] = len(wit) < 3
if out['grid_B_used']:
    rb = [roots(*c) for c in itertools.product(*grids['B'])]; out['grid_B'] = rb; rows = rows + rb
    wit += [r for r in rb if r['negative_roots'] > 0]
out['prec_agree'] = all(r['prec_err'] < 1e-25 for r in rows)
wit.sort(key=lambda r: r['min_neg_omega2'])
out['n_witnesses_found'] = len(wit); out['witnesses'] = wit[:6]
out['add_AC13_fixtures'] = len(wit) < 3
out['note'] = 'kappa = 1/2 FITTED; not theory closed'
(D / 'witnesses.json').write_text(json.dumps(out, indent=1) + '\n')
print('KA3', out['KA3'], 'prec', out['prec_agree'], 'B used', out['grid_B_used'], 'found', len(wit))
for r in out['witnesses']: print(r['epsilon_phi'], r['epsilon_m'], r['Lstar'], r['k'], r['min_neg_omega2'])
