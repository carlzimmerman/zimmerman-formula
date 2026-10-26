"""Post-hoc snapshot packing diagnostic; not a population prediction."""
import json, math
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parent
units=json.loads((root/'run/result.json').read_text())
requirements=json.loads((root.parent/'cold_local_production_2026_10_25/run/result.json').read_text())['rows']
masses=json.loads((root.parent/'cold_rapid_assembly_2026_10_25/run/result.json').read_text())['cluster_mass_requirements']
req=np.array([r['required_source_over_D'] for r in requirements])
rows=[]
for meta in json.loads((root/'followup/result.json').read_text())['rows']:
 name=meta['name'];s=np.genfromtxt(root/f'followup/{name}_state.csv',delimiter=',',names=True);r,q,p=[s[k] for k in ('r','q','p')];dx=meta['dx'];d=meta['d'];bg=2*math.asin(math.sqrt(1/6)) if d==0 else 0
 z=np.sin(q/2)**2/(np.cos(q/2)*(1+np.cos(q/2)))
 U=10*((z+1)**2-1.2)**2 if d==0 else (d-8)*z+36*z*z+40*z**3+10*z**4
 vol=((r+dx/2)**3-(r-dx/2)**3)/3;cell=vol*(p*p/2+U)
 face=.5*(r[:-1]+dx/2)**2*np.diff(q)**2/dx
 cell[:-1]+=face/2;cell[1:]+=face/2;cell[-1]+=meta['R']**2*(bg-q[-1])**2/dx;cell*=4*math.pi
 assert abs(cell.sum()/meta['final_energy']-1)<1e-9
 core=cell[r<10];E=core.sum();assert abs(E/meta['final_core_energy']-1)<1e-9
 index=np.searchsorted(np.cumsum(core),.9*E);radius=(index+1)*dx
 # Count the entire core mass per R90 volume: optimistic for non-overlap packing.
 density=E/(4*math.pi/3*radius**3);mass=E*units['mass_unit_Msun'];fill=req/density
 rows.append(dict(name=name,snapshot_time=1000,core_energy=E,core_mass_Msun=mass,R90_pc=radius*units['length_unit_pc'],optimistic_density_over_D=density,required_filling_min=float(fill.min()),required_filling_max=float(fill.max()),rows_requiring_overlap=int(sum(fill>1)),required_count_min=min(x['Mc_R500_Msun'] for x in masses)/mass,required_count_max=max(x['Mc_R500_Msun'] for x in masses)/mass))
result=dict(scope='Final-time R90 packing proxy, assigning all core mass to its R90 volume. Energy-to-source matching remains conditional; no cluster population dynamics.',requirement_count=len(req),required_density_range=[float(req.min()),float(req.max())],rows=rows)
(root/'packing_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
