"""Diagnose warm angular versus energy/Dalitz resolution separately.

Load only the declared definitions before the original coarse-run marker;
do not execute or suppress its failed refinement assertion. Inputs are
pinned by the computation manifest.
"""
import json
import sys
from pathlib import Path

out=Path(sys.argv[1]);assert out.is_dir()
path=Path(__file__).with_name('source_assisted_thermal.py')
source=path.read_text();marker='\ncoarse=Thermal('
assert source.count(marker)==1
namespace={'__file__':str(path),'__name__':'cpb_source_assisted_definitions'}
exec(compile(source.split(marker,1)[0],str(path),'exec'),namespace)
Thermal=namespace['Thermal'];m=namespace['m']
rows=[]
for dims in ((40,20,10,20),(64,32,10,20),(40,20,18,36),(64,32,18,36),(80,40,26,52)):
    kernel=Thermal(*dims)
    for ratio in (1.,3.):
        value=kernel.gamma_scaled(m*ratio)
        row={'dimensions':dims,'Tdark_over_m':ratio,'gamma_scaled_GeV4':value}
        rows.append(row);print(json.dumps(row),flush=True)
(out/'results.json').write_text(json.dumps({'rows':rows,
 'scope':'Resolution experiment, not a new physical approximation or abundance result'},indent=2)+'\n')
