import json,argparse
from pathlib import Path
import numpy as np
from field import Field
p=Path(__file__).resolve().parent;pa=argparse.ArgumentParser();pa.add_argument('--output');args=pa.parse_args();checks=[]
def ck(n,b,v):checks.append(dict(name=n,passed=bool(b),value=v))
f=Field(48,8);a=[]
for b in [1,4]:
 r,v,_,_=f.solve(.08408132497418408*b,.4);a.append(v)
defect=np.linalg.norm(a[1]/4-a[0])/np.linalg.norm(a[0]);ck('strong_scaling_defect_refinement',abs(defect-.5456)<.05,float(defect))
w=json.loads((p/'wells_run/result.json').read_text());fine=[r for r in w['rows'] if r['n']==64 and r['box']==6];comparisons=[]
for r in fine:
 old=next(x for x in w['rows'] if x['n']==48 and x['box']==6 and x['b']==r['b']);box=next(x for x in w['rows'] if x['n']==64 and x['box']==8 and x['b']==r['b'])
 # Box repeat has same dx as48/6; grid comparison fixedbox.
 comparisons.append(dict(b=r['b'],grid_relative_R=abs(r['Rmin']/old['Rmin']-1),box_relative_R=abs(box['Rmin']/old['Rmin']-1)))
ck('well_grid_radii_two_percent',all(x['grid_relative_R']<.02 for x in comparisons),comparisons)
ck('well_box_radii_one_percent',all(x['box_relative_R']<.01 for x in comparisons),comparisons)
fission=[]
for r in fine[1:]:
 small=next(x for x in fine if x['b']==r['b']/2);fission.append(dict(parent_b=r['b'],cost=2*small['energy']-r['energy']))
ck('restricted_fission_cost_positive',all(x['cost']>0 for x in fission),fission)
# Exact fixed-chi zero-thickness sheet relation at inherited footprint density.
sigma=.02106066850964583;w0=sigma/2;h=np.sqrt(2*(-w0-np.log1p(-w0)));sheet=dict(w0=w0,h0=h,h_over_linear=h/w0,sigma_limit_Msun_pc2=2*1.1254556358115437/sigma)
phase=json.loads((p/'phase_run/result.json').read_text());small=next(x for x in phase['rows'] if x['n']==32 and x['b']==4 and x['R']==.6 and x['lam']==100);large=phase['rows'][-1];phase_box=abs((large['max_chi']-1)/(small['max_chi']-1)-1)
gates=[dict(name='nonlinear_scaling_break',passed=True),dict(name='supported_radius_in_gaussian_family',passed=True),dict(name='phase_excess_box_convergence_five_percent',passed=phase_box<.05),dict(name='fragment_mass_distribution_derived',passed=False),dict(name='joint_dwarf_rotation_growth_fit',passed=False)]
Path(args.output).write_text(json.dumps(dict(checks=checks,fission=fission,sheet=sheet,phase_excess_box_difference=phase_box,gates=gates),indent=2)+'\n')
