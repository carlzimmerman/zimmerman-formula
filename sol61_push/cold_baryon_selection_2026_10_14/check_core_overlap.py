"""Does a spatially active cluster core contain stars without hot gas?"""
import ast
import json
import sys
from pathlib import Path
import numpy as np
from astropy.io import fits

checks=[]
def check(name,cond):
    ok=bool(cond)
    checks.append(dict(name=name,passed=ok))
    if not ok:
        raise AssertionError(name)

src=Path('qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/cluster_audit.py')
tree=ast.parse(src.read_text())
names=['radius_kpc','loginterp','load_cluster']
nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
check('three existing read-only profile functions found',len(nodes)==3)
DATA=Path('real_research/data/xcop')
env=dict(np=np,fits=fits,DATA=DATA)
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),'exec'),env)
rows=[]
excluded=[]
for directory in sorted(DATA.iterdir()):
    if not directory.is_dir():
        continue
    c=env['load_cluster'](directory.name)
    if not c['has_star']:
        excluded.append(dict(cluster=c['name'],reason='No stellar profile; no imputation'))
        continue
    for radius in [50.,100.,200.]:
        gas=float(env['loginterp']([radius],c['rg'],c['mg'])[0])
        star=float(env['loginterp']([radius],c['rs'],c['ms'])[0])
        if not np.isfinite(gas+star):
            excluded.append(dict(cluster=c['name'],radius_kpc=radius,reason='Outside measured profile ranges; no extrapolation'))
            continue
        check('both source masses positive '+c['name']+' '+str(radius),gas>0 and star>0)
        rows.append(dict(cluster=c['name'],radius_kpc=radius,
                         enclosed_hot_gas_Msun=gas,enclosed_stellar_Msun=star,
                         hot_over_stellar=gas/star,hot_fraction_of_baryon_source=gas/(gas+star)))
check('nonempty directly profiled overlap sample',len(rows)>0)
summaries={}
for radius in [50.,100.,200.]:
    group=[r for r in rows if r['radius_kpc']==radius]
    if group:
        vals=np.array([r['hot_over_stellar'] for r in group])
        summaries[str(int(radius))]=dict(clusters=len(group),hot_over_stellar_median=float(np.median(vals)),
                                        hot_over_stellar_min=float(np.min(vals)),hot_over_stellar_max=float(np.max(vals)))
out=dict(checks=checks,rows=rows,summaries=summaries,excluded=excluded,
         result='Spatially active spherical cores containing the listed stellar apertures also contain the tabulated hot gas; a universal active-region vertex cannot simply omit that gas.',
         limitations=['Inherited published X-COP gas and stellar profile products, not a new raw X-ray or lensing analysis',
                      'No missing-star imputation or out-of-range extrapolation',
                      'No active/core radius or carrier phase inferred; apertures are declared diagnostics',
                      'Not a no-go for non-spherical, clumpy, time-dependent or state-selective interactions',
                      'Cluster total stellar profiles are not silently interpreted as individual BCG profiles'])
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(checks=len(checks),all_passed=all(x['passed'] for x in checks),summaries=summaries),indent=2))
