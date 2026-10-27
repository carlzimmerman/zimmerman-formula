import argparse,json,time
from pathlib import Path
import numpy as np
from live import Live
from initial import initial
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);arg=ap.parse_args();m=Live();a,x,chi,pi,meta=initial(m,'allF_seed');a=a*np.exp(1j*.03*np.sin(np.arange(m.n))[None,:]);x,res,it=m.minimize_alpha(a,chi,x,maxit=300)
# Independent directional derivative of all density forces and alpha forces.
d=(np.cos(np.arange(2*m.n)).reshape(2,m.n)+1j*np.sin(np.arange(2*m.n)*.7).reshape(2,m.n)).astype(complex);d*=1e-3;h=1e-6;E,mu=m.pot(a,x,True);fd=(m.pot(a+h*d,x)-m.pot(a-h*d,x))/(2*h);analytic=2*np.real(np.sum(mu*np.conj(a)*d));err=abs(fd-analytic)/max(abs(fd),1);assert err<1e-6
parts=m.vacuum_parts(a,chi);dirx=np.cos(np.arange(m.n))*1e-3;fdx=(m.alpha_energy(x+h*dirx,parts)-m.alpha_energy(x-h*dirx,parts))/(2*h)
mt,mf,F,co,cross=parts;gx=2*m.beta*m.vol*F*np.sin(4*x)/np.pi**2+m.B*m.vol*np.sin(2*x)+m.J*((mf-mt)*np.sin(2*x)-2*cross*np.cos(2*x));gx[:-1]-=co*np.diff(x);gx[1:]+=co*np.diff(x);ex=abs(fdx-gx@dirx)/max(abs(fdx),1);assert ex<1e-6
# Pointwise spin flow plus field kick preserves total shift charge.
before=sum(abs(a[0])**2);pp=m.J*0.001/m.sigma;aa=a+(np.exp(-1j*pp)-1)*m.alignment(a,x,chi);dm=abs(aa[0])**2-abs(a[0])**2;depos=np.bincount(m.ids,weights=(1-m.frac)*dm,minlength=len(pi))+np.bincount(m.ids+1,weights=m.frac*dm,minlength=len(pi));pn=pi-m.g*depos/m.wvol;charge=float(m.wvol@pn+m.g*(sum(abs(aa[0])**2)-before));norm=float(np.sum(abs(aa)**2)-np.sum(abs(a)**2));assert abs(charge)<1e-12 and abs(norm)<1e-12
allF=json.loads(Path('physical_completion_2026_10_25/run_free_formation/all_F.json').read_text());af=np.array([np.zeros(m.n),np.sqrt(allF['mass'])],complex);Ef=m.energy(af,np.zeros(m.n),chi,pi);allerr=Ef-allF['energy'];assert abs(allerr)<1e-9
out={'potential_directional_error':err,'carrier_directional_error':ex,'local_reaction_charge_error':charge,'local_reaction_mass_error':norm,'allF_energy_reproduction_error':allerr,'initial_seed_energy_minus_allF':m.energy(a,x,chi,pi)-Ef,'initial_meta':meta,'short_runs':[]}
for dt_Myr in [.01,.005,.0025]:
 a,x,chi,pi,_=initial(m,'allF_seed');E0=m.energy(a,x,chi,pi);Q0=m.wvol@pi+m.g*sum(abs(a[0])**2);sink=0;qs=0;start=time.monotonic();maxerr=0;maxq=0;maxres=0
 for i in range(int(round(.5/dt_Myr))):
  a,x,chi,pi,ds,dq,rr=m.step(a,x,chi,pi,dt_Myr/m.tdyn);sink+=ds;qs+=dq;maxres=max(maxres,rr);maxerr=max(maxerr,abs(m.energy(a,x,chi,pi)+sink-E0));maxq=max(maxq,abs(m.wvol@pi+m.g*sum(abs(a[0])**2)+qs-Q0))
 ans={'dt_Myr':dt_Myr,'duration_Myr':.5,'runtime_seconds':time.monotonic()-start,'escaped_energy':sink,'wave_energy':m.diagnostics(a,x,chi,pi)['wave_energy'],'max_energy_ledger_absolute_error':maxerr,'max_shift_charge_error':maxq,'max_alpha_projected_residual':maxres,'final':m.diagnostics(a,x,chi,pi)};out['short_runs'].append(ans);Path(arg.output).write_text(json.dumps(out,indent=2)+'\n');print(ans,flush=True)
