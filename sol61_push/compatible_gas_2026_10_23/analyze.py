import sys,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from gas_v4 import Gas,rates
base=Path(__file__).parent
names=['crossing_base','crossing_time','crossing_fine','ultra','no_molecules','fewer_molecules','late','small','smooth']
summary={};data={}
for name in names:
 p=base/name/'result.json'
 if not p.exists():continue
 r=json.loads(p.read_text());data[name]=r;par=r['parameters'];m=Gas(par['n'],par['amp'],par['size'],par['ratio'],par['fmol'],visc=par['visc']);y=np.array(r['final']['state']);t=r['final']['time'];A=(t/m.ti)**(2/3);xc,pc,b,pb,P,Q,c,V,u,w,h=m.unpack(y);faces,vol,rb=m.gasgrid(b);nh=.76*m.mgas/vol/A**3*m.runit/1.67262192369e-27/1e6;T=(m.gamma-1)*u/m.kT;idx=np.argmax(nh);low,lte,L=rates(T,nh)
 d=r['rows'][-1].copy();d['gas_r001_volume_kpc']=float((3*np.interp(.001*m.cumm[-1],m.cumm,faces**3/3))**(1/3)*A*m.ell);d.update(reason=r['reason'],densest_cell_T=float(T[idx]),densest_cell_ncrit=float(lte[idx]/low[idx]),gas_r001_in_field_cells=d['gas_r001_volume_kpc']/d['field_cell_kpc'],fixed_gas_mass_Msun=float(.001*sum(m.mgas)*m.M0),max_abs_defect=r['max_absolute_defect']);summary[name]=d
 if name in ['crossing_fine','late']:
  derivative,diag,dt=m.eval(t,y);target=derivative[-2]+derivative[-1];checks=[]
  for fraction in [.001,.0003,.0001]:
   eps=dt*fraction;fd=(m.eval(t+eps,y+eps*derivative)[1]['energy']-m.eval(t-eps,y-eps*derivative)[1]['energy'])/(2*eps);checks.append(dict(eps=eps,relative=abs(fd-target)/max(abs(target),1e-20)))
  d['late_energy_derivative_checks']=checks
 d['gas_mass_deposition_error']=float(abs(sum(rb*m.vol)/sum(m.mgas)-1))
 rc=m.dep(xc,m.mc)[0];d['central_cold_cell_mass_Msun']=float(rc[0]*m.vol[0]*m.M0);d['central_cold_delta']=float(rc[0]/(m.fc*m.J)-1);d['peak_nH_over_local_ncrit']=d['nHmax']/d['densest_cell_ncrit']
fig,axes=plt.subplots(2,2,figsize=(10,7),constrained_layout=True)
for name,color in [('crossing_base','C0'),('crossing_fine','C1'),('ultra','C2')]:
 if name not in data:continue
 r=data[name];par=r['parameters'];m=Gas(par['n']);y=np.array(r['final']['state']);A=(r['final']['time']/m.ti)**(2/3);faces,vol,rb=m.gasgrid(y[m.sl[2]]);centers=.75*np.diff(faces**4)/np.diff(faces**3)*A*m.ell;nh=.76*m.mgas/vol/A**3*m.runit/1.67262192369e-27/1e6
 axes[0,0].loglog(centers*1000,nh,color=color,label='N='+str(m.n));axes[0,0].axvline(A*m.dx*m.ell*1000,color=color,linestyle=':',alpha=.6)
 axes[0,1].semilogx(centers*1000,(m.gamma-1)*y[m.sl[8]]/m.kT,color=color)
for name in ['crossing_fine','late','no_molecules','fewer_molecules']:
 if name not in data:continue
 rows=data[name]['rows'];z=np.array([d['z'] for d in rows]);keep=z<14;z=z[keep];mass=np.array([sum(d['mass_0.3214846542759978'].values()) for d in rows])[keep];nh=np.array([d['nHmax'] for d in rows])[keep]
 axes[1,0].plot(z,mass/1e6,label=name);axes[1,1].semilogy(z,nh,label=name)
axes[0,0].set(xlabel='Physical gas radius [pc]',ylabel='Hydrogen density [cm^-3]',title='z=8; dotted lines: fixed field-cell size');axes[0,0].legend();axes[0,1].set(xlabel='Physical gas radius [pc]',ylabel='Temperature [K]',title='Prescribed molecular abundance = 0.001')
axes[1,0].set(xlabel='Redshift',ylabel='Mass inside 0.3215 kpc [million Msun]',title='Continuing accretion, not an identified remnant');axes[1,0].invert_xaxis();axes[1,0].legend(fontsize=7)
axes[1,1].set(xlabel='Redshift',ylabel='Maximum nH [cm^-3]',title='Central density depends on cooling and resolution');axes[1,1].invert_xaxis()
fig.savefig(base/'profiles.png',dpi=170)
json.dump(summary,open(sys.argv[1],'w'),indent=2);print(json.dumps({k:{q:v[q] for q in ['reason','z','nHmax','densest_cell_T','gas_r001_kpc','gas_r001_in_field_cells','defect']} for k,v in summary.items()},indent=2))
