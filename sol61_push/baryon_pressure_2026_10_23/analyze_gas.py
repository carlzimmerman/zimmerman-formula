import argparse,json
from pathlib import Path
import numpy as np
from hydro_v2 import Hydro
p=argparse.ArgumentParser();p.add_argument('--output');p.add_argument('--names',nargs='+',required=True);a=p.parse_args();base=Path(__file__).parent;out={}
for name in a.names:
 r=json.loads((base/name/'result.json').read_text());pa=r['parameters'];m=Hydro(pa['n'],pa['amp'],ratio=pa['ratio']);f=r['final'];U=np.array(f['U']);xc=np.array(f['xc']);pc=np.array(f['pc']);A=(f['time']/m.ti)**(2/3);H=2/(3*f['time']);rho,v,p,cs=m.primitive(U);T=p/rho/m.kT
 rho_unit=m.M0*1.98847e30/(4*np.pi*(m.ell*3.085677581491367e19)**3);rhophys=rho*rho_unit/A**3;nH=.76*rhophys/1.67262192369e-27/1e6;npart=rhophys/(1.22*1.67262192369e-27)/1e6
 # Galli & Palla1998 A7, low-density H-H2 cooling coefficient; estimate only on eligible cells.
 logT=np.log10(np.clip(T,10,1e4));Lam=10**(-103+97.59*logT-48.05*logT**2+10.80*logT**3-.9032*logT**4);valid=(T>=10)&(T<=1e4)&(nH<=100)&(T>2.725*1101/A)
 tff=np.sqrt(3*np.pi/(32*6.67430e-11*rhophys));cool=[]
 for fh2 in [1e-6,1e-4,1e-3]:
  tc=1.5*npart*1.380649e-16*T/(fh2*nH*nH*Lam)
  idx=int(np.argmin(np.where(valid,tc/tff,np.inf)))
  cool.append(dict(fH2_per_H=fh2,min_tcool_over_gas_freefall=float(tc[idx]/tff[idx]) if np.any(valid) else None,T_at_min=float(T[idx]),nH_at_min=float(nH[idx]),tcool_Myr=float(tc[idx]/(365.25*86400*1e6))))
 # Isolated Newtonian aperture energy: cold shells + gas cell masses, includes gas internal energy.
 aps=[]
 for rk in [.16,.3214846542759978,.64,1.28]:
  rad=rk/m.ell;rs=xc*A;rg=m.r*A;selc=rs<rad;selg=rg<rad;rr=np.r_[rs[selc],rg[selg]];mass=np.r_[m.mc[selc],(rho*m.vol)[selg]];vel=np.r_[(pc/A+H*rs)[selc],(v+H*rg)[selg]];ix=np.argsort(rr);rr=rr[ix];mass=mass[ix];vel=vel[ix];Tkin=.5*np.sum(mass*vel**2);thermal=np.sum(m.vol[selg]*p[selg]/(m.gamma-1));inside=np.cumsum(mass)-mass
  energies=[float(Tkin+thermal-np.sum(mass*(inside+.5*mass)/np.maximum(rr,soft*A*m.dx))) for soft in [.5,1,2]]
  aps.append(dict(radius_kpc=rk,newtonian_energy_with_gas_thermal=energies,kinetic=float(Tkin),thermal=float(thermal)))
 out[name]=dict(reason=r['reason'],endpoint=r['rows'][-1],nH_max_cm3=float(max(nH)),cooling_estimates=cool,newtonian_apertures=aps,scope='Instantaneous optically thin low-density fixed-abundance diagnostic, no chemical evolution or guaranteed cooling history; Newtonian energy omits field terms and external/tidal/flux accounting.')
Path(a.output).write_text(json.dumps(out,indent=2)+'\n')
