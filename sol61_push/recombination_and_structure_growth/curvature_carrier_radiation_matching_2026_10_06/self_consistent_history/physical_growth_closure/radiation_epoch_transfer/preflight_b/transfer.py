"""Bounded backward ideal-fluid transfer on actual nonminimal carrier background."""
import importlib.util,pathlib,argparse,json,sys
import numpy as np
from scipy.integrate import solve_ivp
parent=pathlib.Path(__file__).resolve().parent.parent
sp=importlib.util.spec_from_file_location('audited_growth',parent/'growth.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',choices=['none','drop_trace','erase_carrier'],default='none');args=ap.parse_args()
checks=[];records=[]
def ck(n,v,detail=None):checks.append(dict(name=n,passed=bool(v),detail=detail))
def project(x,b,z,xi,k):
 z=z.copy();z[4]=0;v=g.rows(x,b,z,xi,k);unit=z*0;unit[4]=1
 slope=g.rows(x,b,unit,xi,k)['C00'];z[4]=-v['C00']/slope
 return z,slope
for xi,aend in [(100,.0098),(1000,.002)]:
 b=g.bg.initial(xi);u=g.bg.quantities(0,b,xi);k=10*u['H'];zseeds=[];meta=[]
 for mode in ['phase','dust','radiation']:
  z=np.zeros(9)
  if mode=='phase':z[2]=-b[1]*u['H'];z[3]=b[0]*u['H']
  elif mode=='dust':z[5]=1
  else:z[7]=1
  z,slope=project(0,b,z,xi,k);zseeds.append(z);meta.append(dict(mode=mode,slope=slope))
 y0=np.r_[b,np.array(zseeds).ravel()];grid=np.unique(np.r_[np.linspace(0,np.log(aend),101),np.log(.01)])[::-1];curves=[]
 def fun(x,y):
  bb=y[:5];uu=g.bg.quantities(x,bb,xi);zs=y[5:].reshape(3,9)
  return np.r_[g.bg.rhs(x,bb,xi),np.array([g.rows(x,bb,z,xi,k,args.control=='drop_trace')['dzdt']/uu['H'] for z in zs]).ravel()]
 for method in ['DOP853','Radau']:
  def jac(x,y):
   eps=1e-22;return np.column_stack([np.imag(fun(x,np.array(y,dtype=complex)+1j*eps*np.eye(len(y))[j]))/eps for j in range(len(y))])
  kw=dict(jac=jac) if method=='Radau' else {}
  sol=solve_ivp(fun,(0,np.log(aend)),y0,method=method,rtol=1e-9,atol=1e-12,t_eval=grid,**kw)
  ck(f'solver_{xi}_{method}',sol.success and sol.nfev<60000 and len(sol.t)==len(grid),dict(nfev=sol.nfev,message=sol.message))
  vals=[];defect=0.;chargeerr=0.;fmin=1.;q0=u['Q'];cwe=0.;stressres=0.
  for x,y in zip(sol.t,sol.y.T):
   bb=y[:5];uu=g.bg.quantities(x,bb,xi);fmin=min(fmin,uu['F']);chargeerr=max(chargeerr,abs(uu['Q']/q0-1));modes=[]
   for j,z in enumerate(y[5:].reshape(3,9)):
    v=g.rows(x,bb,z,xi,k,args.control=='drop_trace');defect=max(defect,abs(v['C00'])/(1e-24+v['constraint_scale']))
    cwe=max(cwe,abs(v['CW']-v['C00'])/(1e-24+v['constraint_scale']))
    denom=2*uu['F']*v['p2'];wd=-uu['rho_d']*v['dust_comoving']/denom
    wr=(-uu['rho_r']*z[7]+4*uu['H']*uu['rho_r']*z[8])/denom
    wc=(-v['deltaE']-6*uu['H']*(bb[2]*z[0]+bb[3]*z[1])+6*uu['H']**2*v['deltaF']-3*uu['Fdot']*v['Z'])/denom
    if args.control=='erase_carrier':wc=0.
    stressres=max(stressres,abs(v['W']-wd-wr-wc)/(1e-24+abs(v['W'])+abs(wd)+abs(wr)+abs(wc)))
    rhoc=-2*(v['p2']*v['Phi']+3*uu['H']*v['Z'])-uu['rho_d']*z[5]-uu['rho_r']*z[7]
    pc=(uu['rho_d']*z[5]+rhoc-v['deltaR'])/3
    modes.append(dict(mode=meta[j]['mode'],W=float(v['W']),dust_comoving=float(v['dust_comoving']),radiation_density=float(z[7]),W_dust=float(wd),W_radiation=float(wr),W_carrier=float(wc),delta_rho_carrier_EH=float(rhoc),delta_p_carrier_EH=float(pc),entropy_d_r=float(z[5]-.75*z[7]),W_at_unit_evolved_dust=float(v['W']/v['dust_comoving']) if abs(v['dust_comoving'])>1e-12 else None))
   vals.append(dict(a=float(np.exp(x)),F=float(uu['F']),H=float(uu['H']),radiation_over_dust=float(uu['rho_r']/uu['rho_d']),carrier_fraction=float(uu['rho_carrier']/(3*uu['H']**2)),modes=modes))
  ck(f'positive_F_{xi}_{method}',fmin>0,fmin);ck(f'charge_{xi}_{method}',chargeerr<2e-6,chargeerr)
  ck(f'Hamiltonian_{xi}_{method}',defect<2e-5,defect);ck(f'Weyl_identity_{xi}_{method}',cwe<1e-10,cwe)
  ck(f'actual_source_decomposition_{xi}_{method}',stressres<2e-5,stressres)
  ie=np.argmin(abs(sol.t-np.log(.01)));eq=vals[ie]
  if method=='DOP853':
   xe=sol.t[ie];be=sol.y[:5,ie];ue=g.bg.quantities(xe,be,xi);T=1/ue['H'];lam=1.
   def adiabatic(x,bb,T):
    uu=g.bg.quantities(x,bb,xi);H=uu['H'];Td=lam-(H+uu['Fdot']/uu['F'])*T;qd=-3*H*bb[2:4]-xi*uu['R']*bb[:2]
    return np.r_[-bb[2:4]*T,-qd*T-bb[2:4]*Td,H*T-lam,3*H*T,T,4*H*T,T],Td
   za,Td=adiabatic(xe,be,T);va=g.rows(xe,be,za,xi,0.);eps=1e-22;bd=g.bg.rhs(xe,be,xi)
   zad=np.imag(adiabatic(xe+1j*eps,be+1j*eps*bd,T+1j*eps*Td/ue['H'])[0])/eps*ue['H']
   err=float(np.linalg.norm(zad-va['dzdt'])/(1+np.linalg.norm(zad)))
   ck(f'exact_k0_adiabatic_rows_{xi}',err<1e-9,err)
   ck(f'exact_k0_adiabatic_constraint_{xi}',abs(va['C00'])/(1+va['constraint_scale'])<1e-10)
   zp,slope=project(xe,be,za,xi,k);vp=g.rows(xe,be,zp,xi,k)
   ck(f'finite_k_adiabatic_preparation_constraint_{xi}',abs(vp['C00'])/(1+vp['constraint_scale'])<1e-10)
   ck(f'finite_k_adiabatic_equal_ordinary_entropy_{xi}',abs(zp[5]-.75*zp[7])<1e-12 and zp[6]==zp[8])
   records.append(dict(kind='adiabatic_preparation',xi=xi,a=.01,p_over_H=float(k/.01/ue['H']),k0_row_error=err,Phi_change=float(zp[4]-za[4]),constraint_slope=float(slope),early_growing_member='not fixed: integral lower boundary/constant unavailable'))
  ck(f'equality_reached_{xi}_{method}',abs(eq['radiation_over_dust']-1)<1e-12 and eq['F']>0)
  ww=[m['W_at_unit_evolved_dust'] for m in eq['modes']]
  ck(f'different_W_same_evolved_dust_{xi}_{method}',all(v is not None for v in ww) and max(ww)-min(ww)>1e-8,ww)
  # Effective EH carrier pressure is an operational Newton-gauge stress perturbation, not material rest pressure.
  ck(f'phase_not_exact_zero_pressure_{xi}_{method}',abs(eq['modes'][0]['delta_p_carrier_EH'])>1e-12)
  records.append(dict(xi=xi,method=method,nfev=sol.nfev,Fmin=fmin,constraint_max=defect,charge_error=chargeerr,decomposition_error=stressres,equality=eq,endpoint=vals[-1],samples=vals))
  amp=np.linalg.norm(b[:2]);sc=np.tile(np.array([amp,amp,amp*u['H'],amp*u['H'],1,1,1/u['H'],1,1/u['H']]),3)
  curves.append(sol.y[5:]/sc[:,None])
 diff=float(np.max(np.linalg.norm(curves[0]-curves[1],axis=0)/(1+np.linalg.norm(curves[0],axis=0))))
 ck(f'independent_solver_{xi}',diff<3e-5,diff);records[-1]['solver_error']=diff
out=dict(passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,records=records,control=args.control)
p=pathlib.Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2));print(json.dumps(dict(passed=out['passed'],total=out['total'],failures=[c for c in checks if not c['passed']],summaries=[{k:v for k,v in r.items() if k!='samples'} for r in records])));sys.exit(out['passed']!=out['total'])
