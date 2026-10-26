import argparse,json,subprocess
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True);root=Path(__file__).resolve().parent
subprocess.run(['clang++','-O3','-std=c++17',str(root/'lattice.cpp'),'-o',str(out/'evolve')],check=True)
f=json.load(open(root/'floquet/result.json'));selected={x['index']:x['result'] for x in f['refined']};rows=[]
for i,n,dt in [(173,24,.002),(207,24,.002),(98,24,.002),(98,24,.001),(98,32,.001)]:
 r=selected[i];k=r['peak_k_over_m'] or 1.;name=f'case_{i}_N{n}_dt{dt}';stem=out/name
 subprocess.run([str(out/'evolve'),str(stem),str(r['d']),str(r['amplitude']),str(k),str(n),str(dt),'40','.001'],check=True)
 v=json.load(open(str(stem)+'.json'));s=np.genfromtxt(str(stem)+'.csv',delimiter=',',names=True);late=s[s['time']>=30];T=late['time'][-1]-late['time'][0];mean=lambda key:float(np.trapz(late[key],late['time'])/T)
 # P = P_virial + m²/(2T) [<q q_s>] at endpoints.
 endpoint=(r['d']-8)/4*(late['qp'][-1]-late['qp'][0])/(2*T)
 residual=(mean('pressure')-mean('virial_pressure')-endpoint)/mean('energy')
 v.update(name=name,index=i,N=n,dt=dt,k_over_m=k,d=r['d'],target_E=r['E'],late_P_over_E=mean('pressure')/mean('energy'),late_virial_P_over_E=mean('virial_pressure')/mean('energy'),finite_time_endpoint_over_E=endpoint/mean('energy'),virial_identity_residual=residual)
 assert abs(residual)<.01
 rows.append(v)
(out/'result.json').write_text(json.dumps(dict(scope='Seeded 3D periodic-box dynamics, supplied energy, no abundance or confinement prediction',rows=rows),indent=2)+'\n');print(json.dumps(rows,indent=2))
