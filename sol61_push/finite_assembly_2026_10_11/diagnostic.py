"""Instantaneous binding diagnostics; never a permanent-capture classifier."""
import argparse,json
from pathlib import Path
import numpy as np
import experiment as ex

parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
folder=Path(__file__).resolve().parent
record=json.loads((folder/'run_v2/results.json').read_text())
rows=[]
for c in record['cells']:
 R,V,b,w,Q,pos,vel=ex.unpack(np.array(c['final_state']))
 mass=c['eta']/ex.N
 pb,_,_=ex.field(pos-R,b)
 _,_,pc=ex.pairs(pos,mass,c['selfgravity'])
 ee=.5*np.sum((vel-V)**2,axis=1)+pb+pc
 candidates=[]
 if c['selfgravity']:
  for i in range(ex.N):
   for j in range(i):
    sep=np.linalg.norm(pos[i]-pos[j]);dv=vel[i]-vel[j]
    ep=.5*np.dot(dv,dv)-2*mass/np.sqrt(sep*sep+ex.SOFT**2)
    x=(pos[i]+pos[j])/2-R;v=(vel[i]+vel[j])/2-V
    eh=.5*np.dot(v,v)+ex.field(x[None,:],b)[0][0]
    if ep<0 and eh>0 and np.dot(x,v)>0:
     candidates.append(dict(i=i,j=j,separation=float(sep),pair_relative_energy=float(ep),
                            pair_COM_host_energy=float(eh),pair_COM_radius=float(np.linalg.norm(x)),
                            full_particle_energies=[float(ee[i]),float(ee[j])]))
 rows.append(dict(name=c['name'],negative_instantaneous_energies=int(np.sum(ee<0)),
                  radial_range=[float(np.min(np.linalg.norm(pos-R,axis=1))),float(np.max(np.linalg.norm(pos-R,axis=1)))],
                  outbound_pair_candidates=candidates))
Path(args.output).write_text(json.dumps(dict(cells=rows,non_claim='Neither negative parcel/pair energies nor positive host-only COM energies certify permanent binding or escape in the full evolving system'),indent=2)+'\n')
print('recorded',len(rows),'cells')
