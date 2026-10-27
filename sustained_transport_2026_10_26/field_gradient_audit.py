"""Independent Hamiltonian differences for the continuous force-budget field."""
import argparse,json
from pathlib import Path
import numpy as np
from dynamics import model,load,field
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();m=model();rows=[]
for name,path in [('first','infall_pump_2026_10_25/run_smooth_infall/state.npz'),('late','sustained_transport_2026_10_26/run_continue_second/state.npz')]:
 z=load(path);a,x,cp,c,v=z;f=field(m,z);n=m.n;loc=np.exp(-(m.r*m.rm/100)**4);wl=np.exp(-(m.wr*m.rm/100)**4);phase=np.sin(np.arange(n)*.731+.4);asc=np.sqrt(np.sum(abs(a)**2,axis=0));da=.1*asc[None,:]*np.array([np.sin(np.arange(n)*.13)+1j*phase,np.cos(np.arange(n)*.23)+1j*np.cos(np.arange(n)*.31)])*loc
 d=(da,.1*phase*loc,.001*np.sqrt(m.Z(a))*phase*loc,1e-7*np.sin(m.wr*.71)*wl,1e-7*np.cos(m.wr*.42)*wl)
 pred=float(2*np.real(np.sum(np.conj(d[0])*1j*m.sigma*f[0]))-d[1]@f[2]+d[2]@f[1]-d[3]@(m.wvol*(f[4]+m.gamma*v))+d[4]@(m.wvol*v))
 tests=[]
 for eps in [1e-4,3e-5,1e-5]:
  plus=tuple(y+eps*dy for y,dy in zip(z,d));minus=tuple(y-eps*dy for y,dy in zip(z,d));actual=(m.full_energy(*plus)-m.full_energy(*minus))/(2*eps);tests.append({'epsilon':eps,'derivative':actual,'relative_error':abs(actual-pred)/max(abs(actual),abs(pred),1e-100)})
 rows.append({'state':name,'full_force_prediction':pred,'finite_differences':tests});assert min(x['relative_error'] for x in tests)<1e-5
Path(args.output).write_text(json.dumps({'cases':rows,'interpretation':'Full continuous Hamiltonian vector field used by live acceleration and force budgets agrees with independent energy directional differences; finite floating-point audit.'},indent=2)+'\n');print(rows)
