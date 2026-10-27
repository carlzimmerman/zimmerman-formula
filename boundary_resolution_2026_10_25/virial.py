import argparse,json
from pathlib import Path
import numpy as np,torch
from compact import Compact
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=[]
for source in ['run_compact/checkpoint_0_0.3.json','run_regularized/recover_0.5_-1.0.json']:
 r=json.loads((Path(__file__).parent/source).read_text());m=Compact(domain=12,beta=r['beta'],K=r['K'],charge=0,L=r['density_stiffness_length_kpc'],eta=r['eta'],sigma=r['surface_tension'],eps=r['chemical_epsilon'],h=r['fine_spacing_kpc']);m.ell2=(r['ell_kpc']/m.rm)**2;n=m.n;mass=np.array(r['mass']);x=np.array(r['v'][n:]);q=np.sin(np.pi*x/2)**2;rr=m.r.numpy();vol=m.vol.numpy();u=m.A.numpy()@(mass*q);gd=m.A.numpy()@mass;w,F=[z.numpy() for z in m.functions(torch.tensor(u))];Fp=u*(2-u)/(1-u)**2;s=np.sin(np.pi*x)**2/np.pi**2;M=sum(mass);MT=mass@q;tt=m.tt.numpy();tw=m.tw.numpy();ut=MT*tt**2;wt=m.functions(torch.tensor(ut))[0].numpy();uf=(u[1:]+u[:-1])/2;Ff=uf*uf/(1-uf);Fpf=uf*(2-uf)/(1-uf)**2;rf=m.rf.numpy();dr=m.dr.numpy();rho=mass/vol;gb=rr/(rr*rr+m.b*m.b)**1.5;amp=np.sqrt(rho);ww=np.diff(amp)-m.eta*(amp[1:]+amp[:-1])/2*np.diff(q);dq=np.diff(q);reg=m.delta*dr;sqrt=np.sqrt(dq*dq+reg*reg);soft=dq*dq/(sqrt+reg);t=np.clip((rho-.001)/.002,0,1);Sp=30*t*t*(1-t)**2/.002
 V=dict(response=float(sum(vol*(3*w-2*u*u/(1-u)))+sum(tw*(3*wt-2*ut*ut/(1-ut))/tt**4)),barrier=float(m.beta*.95*sum(vol*s*(3*F-2*u*Fp))),phase_stiffness=float(.5*m.ell2*sum(rf*rf/dr*(Ff-2*uf*Fpf)*np.diff(x)**2)),self_gravity=float(.5*sum(vol*gd*gd)+.5*M*M/m.R),baryons=float(sum((-vol*gb*gd)*(2-3*rr*rr/(rr*rr+m.b*m.b)))+M*m.R*m.R/(m.R*m.R+m.b*m.b)**1.5),gas=float(-3*m.K*sum(vol*(rho*(1-q))**(5/3))),material_stiffness=float(-(m.L/m.rm)**3*sum(rf*rf/dr*ww*ww)),surface=float(m.sigma*sum(rf*rf*soft*(2-reg/sqrt))),chemical=float(3*m.eps*sum(mass*q*rho*Sp)))
 old={key:getattr(m,key) for key in ['r','vol','dr','rf','A','grav','phib','R','tt','tw']}
 def E(scale):
  m.r=old['r']*scale;m.vol=old['vol']*scale**3;m.dr=old['dr']*scale;m.rf=old['rf']*scale;m.A=old['A']/scale**2;m.grav=old['grav']/scale;m.phib=-1/torch.sqrt(m.r*m.r+m.b*m.b);m.R=old['R']*scale;m.tt=old['tt']/scale;m.tw=old['tw']/scale
  ans=float(m.energy(torch.tensor(np.log(mass)),torch.tensor(x)))
  for key,value in old.items():setattr(m,key,value)
  return ans
 analytic=sum(V.values());checks=[]
 for h in [1e-5,1e-6]:
  fd=(E(1+h)-E(1-h))/(2*h);err=abs(fd-analytic)/max(1,abs(fd));assert err<1e-5;checks.append(dict(step=h,finite_difference=fd,error=err))
 out.append(dict(source=source,components_dE_dloglambda=V,total=analytic,relative_virial_residual=abs(analytic)/sum(abs(z) for z in V.values()),checks=checks,qualification='Finite-grid geometry dilation and component identity; not exact stationarity or continuum proof.'))
Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
