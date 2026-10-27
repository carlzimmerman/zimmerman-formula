"""Temperature table for the proved pole-free source-assisted channel.

Fine/coarse temperature grids are nested; prior independently refined
anchor values are reused by hash, not silently recomputed at lower resolution.
"""
import json
import math
import sys
from pathlib import Path
import numpy as np

out=Path(sys.argv[1]);assert out.is_dir()
base=Path(__file__).parent
path=base/'source_assisted_thermal.py'
text=path.read_text();marker='\ncoarse=Thermal('
assert text.count(marker)==1
ns={'__file__':str(path),'__name__':'cpb_rate_definitions'}
exec(compile(text.split(marker,1)[0],str(path),'exec'),ns)
anchors=json.loads((base/'source_assisted_rate_refined_run_001/results.json').read_text())
m=ns['m'];K=ns['K3zero']
grid=np.geomspace(1e-4,3.,41)
coarse={float(x).hex() for x in grid[::2]}
anchor={row['Tdark_over_m']:row for row in anchors['rows']}
values=sorted(set(map(float,grid))|set(anchor))
kernels={}
rows=[];checks=[]
for ratio in values:
    T=m*ratio;A,B=ns['scaled_densities'](T)
    if ratio in anchor:
        gamma=anchor[ratio]['gamma3_scaled_GeV4'];dims=anchor[ratio]['fine_dimensions']
        origin='prior_refined_anchor';is_coarse=True
    else:
        dims=(40,20,10,20) if ratio<=.3 else ((40,20,18,36) if ratio<=1 else (40,20,26,52))
        if dims not in kernels:kernels[dims]=ns['Thermal'](*dims)
        gamma=kernels[dims].gamma_scaled(T);origin='new_temperature_point'
        is_coarse=ratio.hex() in coarse
    correction=gamma/(K*B*A*A)
    checks.append({'name':'positive thermal correction '+str(ratio),'passed':bool(correction>0)})
    assert correction>0
    row=dict(Tdark_over_m=ratio,T_dark_GeV=T,gamma3_scaled_GeV4=gamma,
             gamma3_over_NR=correction,on_coarse_grid=is_coarse,
             quadrature_dimensions=dims,origin=origin)
    rows.append(row)
    (out/'partial_table.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps({'ratio':ratio,'correction':correction,'origin':origin}),flush=True)
result={'parameters':ns['p'],'NR_event_coefficient_GeVminus5':K,'rows':rows,
        'checks':checks,'scope':'Vacuum tree, common MB temperature, narrow external source; table only for pole-free mixed source-assisted crossing; no full collision hierarchy'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print('Completed %d-point table, %d-point nested coarse grid.'%(len(rows),sum(x['on_coarse_grid'] for x in rows)))
