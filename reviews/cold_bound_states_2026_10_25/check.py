import argparse,json,math,importlib.util
from pathlib import Path
import numpy as np
import sympy as S
from scipy.linalg import eigh_tridiagonal

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 q,d,z=S.symbols('q d z',real=True);x=1/S.cos(q/2)
 V=10*x**4-24*x**2+14+d*(x-1)
 poly=(d-8)*z+36*z**2+40*z**3+10*z**4
 assert S.expand(poly.subs(z,x-1)-V)==0
 g=(5*d+176)/96*(-1 if a.mutate else 1)
 assert S.simplify(S.diff(V,q,4).subs(q,0)/6-g)==0,'quartic sign mutation'
 gas=[r for r in json.load(open('reviews/cold_filter_reality_2026_10_25/run_fixed/result.json'))['cluster_rows'] if r['HJ']==1.8e-18]
 spec=importlib.util.spec_from_file_location('interface','reviews/cold_filter_interface_2026_10_25/check.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 modes=[]
 for dd in [min(r['d'] for r in gas),100.,max(r['d'] for r in gas)]:
  results=[]
  for L in [15.,20.]:
   bg,_,_=mod.profile(dd,L)
   for dx in [.02,.01]:
    zz=np.arange(-L+dx/2,L,dx);h=mod.HESS(bg(zz),np.where(zz<0,dd,0))
    ev,vec=eigh_tridiagonal(2/dx**2+h,np.full(len(zz)-1,-1/dx**2),select='i',select_range=(0,0))
    lam=float(ev[0]);u=vec[:,0]/math.sqrt(dx)
    assert 0<lam<min(5.76,(dd-8)/4)
    assert abs(sum(u*u)*dx-1)<1e-10
    results.append(dict(L=L,dx=dx,lambda0=lam,inside_norm=float(sum(u[zz<0]**2)*dx)))
  assert max(r['lambda0'] for r in results)-min(r['lambda0'] for r in results)<.01
  modes.append(dict(d=dd,results=results))
 PC=3.085677581491367e16;C=299792458.;G=6.67430e-11
 wunit=C*C/(1500*PC*1000)/(2.4*math.sqrt(5/6));lengthpc=C/wunit/PC
 Dmass=.75*3*(1.8e-18)**2/(8*math.pi*G)
 walls=[]
 for r in gas:
  k=math.sqrt((r['d']-8)/4-5.76)
  ell=lengthpc/k
  walls.append(dict(name=r['name'],inner_X=r['inner_X'],d=r['d'],max_amplitude_length_pc=ell,log10_relative_density_at_1kpc=-2*1000/ell/math.log(10)))
 req=json.load(open('reviews/cold_local_production_2026_10_25/run/result.json'))['rows'];clumps=[]
 for r in req:
  dd=r['gas_d'];m2=(dd-8)/4;gg=(5*dd+176)/96
  # P=K rho_mass^2 in the fixed-source canonical-envelope surrogate.
  K=3*gg*C*C/(8*m2*m2*Dmass)
  R=math.sqrt(math.pi*K/(2*G))/PC/1e6
  eps=gg*r['required_source_over_D']/(m2*m2)
  clumps.append(dict(name=r['name'],model=r['model'],footing=r['footing'],shell=r['shell'],radius_Mpc=R,nonlinear_parameter=eps))
 summary=dict(length_unit_pc=lengthpc,wall_length_pc_range=[min(r['max_amplitude_length_pc'] for r in walls),max(r['max_amplitude_length_pc'] for r in walls)],least_density_log10_at_1kpc=max(r['log10_relative_density_at_1kpc'] for r in walls),polytrope_radius_Mpc_range=[min(r['radius_Mpc'] for r in clumps),max(r['radius_Mpc'] for r in clumps)],nonlinear_parameter_range=[min(r['nonlinear_parameter'] for r in clumps),max(r['nonlinear_parameter'] for r in clumps)],cases_parameter_below_point1=sum(r['nonlinear_parameter']<.1 for r in clumps),cases=303)
 result=dict(summary=summary,modes=modes,walls=walls,clumps=clumps)
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(summary=summary,modes=modes),indent=2))
if __name__=='__main__':main()
