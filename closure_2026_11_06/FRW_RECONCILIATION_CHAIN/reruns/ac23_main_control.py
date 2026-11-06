"""Corrected-coefficient rerun of AC23 'main' rows: pol_on=(1-z)^2 instead of (1-2z)^2, z=GS2_PHYS.
Imports AC13 run() unchanged; writes only to the scratch dir given as argv[1]. Run from repo root."""
import importlib.util, json, sys
from pathlib import Path
out = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location('ac13', 'action_search_2026_11_05/AC13_slow_root_closure/ac13.py')
ac13 = importlib.util.module_from_spec(spec); spec.loader.exec_module(ac13)
ac13.OUT = out
old = ac13.POL['main']
ac13.POL["main"] = old  # CONTROL: legacy value
print('pol_on old', repr(old), 'corrected', repr(ac13.POL['main']), flush=True)
W = json.loads(Path('action_search_2026_11_05/AC23_fresh_slow_roots/witnesses.json').read_text())['witnesses']
D = Path('action_search_2026_11_05/AC23_fresh_slow_roots/parts')
rows = []
for w in W:
    c = (w['epsilon_phi'], w['epsilon_m'], w['Lstar'], w['k'])
    for rtol in (1e-9, 1e-11):
        r = ac13.run(c + ('main', rtol, 20.0))
        tag = f"c{c[0]}_{c[1]}_{c[2]}_{c[3]}_main_{rtol:g}_20"
        o = json.loads((D / f"{tag}.json").read_text())
        def last(x, key): return [s[key] for s in x['snaps']]
        d = max(abs(a - b) / max(abs(b), 1e-300) for key in ('max_I', 'max_II', 'detK_over_a6_min')
                for a, b in zip(last(r, key), last(o, key)))
        rows.append(dict(tag=tag, ok=r['ok'], ok_old=o['ok'], max_rel_diff_vs_stored=d))
        print(tag, r['ok'], o['ok'], f"{d:.3e}", flush=True)
json.dump(dict(pol_on_old=old, pol_on_corrected=ac13.POL['main'], rows=rows,
               max_rel_diff=max(r['max_rel_diff_vs_stored'] for r in rows)), open(out / 'summary.json', 'w'), indent=1)
