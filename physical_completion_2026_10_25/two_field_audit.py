import argparse,json
from pathlib import Path
import numpy as np,torch
from scipy.linalg import null_space
from two_field import TwoField
from three_field_solver import finish
from joint import T,RESERVOIR

def audit(m,r):
 n=m.n;v=np.r_[r['mass'],r['v'][n:]];a=T(v).requires_grad_(True);H=torch.autograd.functional.hessian(lambda aa:m.energy(torch.log(aa[:n]),aa[n:]),a).detach().numpy();im=np.where(v[:n]>1e-8)[0];P=np.zeros((3*n,len(im)-1));P[im]=null_space(np.ones((1,len(im))));ix=np.r_[np.arange(n,2*n),2*n+im];Z=np.c_[P,np.eye(3*n)[:,ix]];HH=Z.T@H@Z;ev=np.linalg.eigvalsh(HH);rad=np.array(r['r']);q=np.array(r['q']);i=np.where((q[:-1]-.5)*(q[1:]-.5)<0)[0][-1];dr=rad[i+1]-rad[i];hp=np.pi/2*np.sin(np.pi*v[2*n:]);c=np.zeros(3*n);c[2*n+i]=dr*(.5-q[i+1])/(q[i+1]-q[i])**2*hp[i];c[2*n+i+1]=-dr*(.5-q[i])/(q[i+1]-q[i])**2*hp[i+1];cc=c@Z;k=float(1/(cc@np.linalg.solve(HH,cc))) if ev[0]>0 else None;d=np.r_[v[:n]*np.cos(np.arange(n)),.1*np.sin(np.arange(2*n))];d[:n]-=v[:n]*sum(d[:n])/RESERVOIR;errors=[];caperrors=[]
 for dt in [1e-6,3e-7,1e-7]:
  fd=(m.direct(v+dt*d)[1]-m.direct(v-dt*d)[1])/(2*dt);errors.append(float(max(abs(fd-H@d))/max(1,max(abs(H@d)))));fdc=(m.cap(v+dt*d)-m.cap(v-dt*d))/(2*dt);caperrors.append(float(max(abs(fdc-m.capjac(v)@d))))
 return dict(minimum_active_H=float(ev[0]),relaxed_boundary_stiffness_Eunit_per_kpc2=k,hessian_errors=errors,cap_jacobian_errors=caperrors,active_mass_cutoff=1e-8,matter_phase_angles_included='occupied cells above mass cutoff',vacuum_phase_angles_included='all',qualification='Local radial Hessian, not global stability or dynamics.')
def move(m,r,d):
 n=m.n;rad=np.array(r['r']);edges=[0.]
 for rr in rad:edges.append(2*rr-edges[-1])
 edges=np.array(edges);R=r['scaled_boundary_kpc'];shape=edges/R*np.exp(-((edges-R)/(.25*R))**2);shift=edges+d*shape;mass=np.array(r['mass']);q=np.array(r['q']);parts=[np.maximum(np.diff(np.interp(edges**3,shift**3,np.r_[0,np.cumsum(mass*f)])),0) for f in [q,1-q]];mm=parts[0]+parts[1];qq=np.divide(parts[0],mm,out=np.zeros_like(mm),where=mm>1e-14);mm=np.maximum(mm,1e-12);mm*=RESERVOIR/sum(mm);rr=rad+d*rad/R*np.exp(-((rad-R)/(.25*R))**2);x=np.interp(rad,rr,r['v'][n:2*n]);return np.r_[mm,x,2/np.pi*np.arcsin(np.sqrt(np.clip(qq,0,1)))]
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);m=TwoField(J=30);base=json.loads(Path('physical_completion_2026_10_25/run_two_field/J_30.0.json').read_text());out={'audit':audit(m,base),'recoveries':[]};dest.write_text(json.dumps(out,indent=2)+'\n');assert out['audit']['minimum_active_H']>0 and max(out['audit']['hessian_errors'])<1e-6 and max(out['audit']['cap_jacobian_errors'])<1e-6
for d in [-1.,1.]:
 v=move(m,base,d);assert min(m.cap(v))>0;r=finish(m,v,dest.with_name(f'recovery_{d}.json'),initial_iterations=0,newton_iterations=60);r['displacement']=d;r['radius_change']=r['scaled_boundary_kpc']-base['scaled_boundary_kpc'];out['recoveries'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r.get(k) for k in ['displacement','radius_change','density_KKT_max','gradient_max','scaled_law_error_bound_percent','scaled_density_rebound','optimizer']},flush=True)
