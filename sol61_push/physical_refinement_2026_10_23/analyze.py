"""Fixed physical apertures and limited Newtonian binding diagnostics."""
import argparse,json
from pathlib import Path
import numpy as np
from radial_v2 import Radial
from radial_cold import Radial as Cold
p=argparse.ArgumentParser();p.add_argument('--output');a=p.parse_args();base=Path(__file__).parent
out={}
for name in ['newton','fine','time','weak','strong','strong_fine','strong_late','cold_control','history2200','small_seed','large_seed']:
 raw=json.loads((base/name/'result.json').read_text());r=raw.get('evolution',raw)
 if r['reason']!='endpoint':
  out[name]=dict(reason=r['reason'],last_completed_step=r['rows'][-1],excluded_from_endpoint_analysis=True);continue
 par=r['parameters'];m=(Cold if name=='cold_control' else Radial)(par['n'],par['amp'],par['zi'],par['size']);f={k:np.array(v) for k,v in r['final'].items()};A=(f['time']/m.ti)**(2/3);H=2/(3*f['time']);dx=A*m.dx;rc,_,_=m.dep(f['xc'],m.mc)
 # Integrate the deposited piecewise-constant physical density, including partial cell volumes.
 edge=np.arange(m.n+1)*m.dx;ap=[]
 for rk in [.16,.3214846542759978,.64,1.28]:
  radius=rk/m.ell;cut=radius/A;weights=np.maximum(0,np.minimum(edge[1:],cut)**3-np.minimum(edge[:-1],cut)**3)/3
  smooth=float(np.sum(rc*weights)*m.M0)
  rr=np.r_[f['xc'],f['xb']]*A;mass=np.r_[m.mc,m.mb];vel=np.r_[f['pc'],f['pb']]/A+H*rr;sel=rr<radius;ix=np.argsort(rr[sel]);rs=rr[sel][ix];ms=mass[sel][ix];vs=vel[sel][ix];kin=.5*np.sum(ms*vs**2);inside=np.cumsum(ms)-ms
  potentials=[-np.sum(ms*(inside+.5*ms)/np.maximum(rs,soft*dx)) for soft in [.5,1,2]]
  ap.append(dict(radius_kpc=rk,cold_mass_deposited_Msun=smooth,shell_count=int(sum(sel)),physical_kinetic=float(kin),self_gravity_floor_half_one_two_cells=[float(u) for u in potentials],newtonian_energy_floor_half_one_two_cells=[float(kin+u) for u in potentials]))
 P=f['P'];c=f['chi'];rcpert=(rc-m.mc.sum()/m.vol.sum())/A**3;e=rcpert-m.div(P)/A
 field=.5*(m.eta*np.sum(m.ev*f['Q']**2)+m.b*np.sum(m.vol*f['V']**2))/A**3+A**3*(np.sum(m.ev*(-abs(P)-np.log1p(-abs(P))))+.5*m.alpha*np.sum(m.vol*(c-1)**2)+.5*m.d*np.sum(m.ev*(m.grad(c)/A)**2)+.5*np.sum(m.vol*e**2/c))
 out[name]=dict(parameters=par,endpoint=r['rows'][-1],apertures=ap,positive_field_energy_whole_box=float(field),scope='Newtonian isolated-shell energy is necessary context only; no full-action binding certificate, background/tidal/tail subtraction or outward flux accounting.')
Path(a.output).write_text(json.dumps(out,indent=2,allow_nan=True)+'\n')
