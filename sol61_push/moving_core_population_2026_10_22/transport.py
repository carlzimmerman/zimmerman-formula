import ast,json,argparse
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,solve_bvp,quad
import sympy as s
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);args=pa.parse_args();p=Path('sol61_push/moving_core_population_2026_10_22');prev=Path('sol61_push/compact_surplus_2026_10_22')
tree=ast.parse((prev/'checks.py').read_text());exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['interior','exterior']],type_ignores=[]),str(prev/'checks.py'),'exec'))
dw=json.loads((prev/'dwarf_run2/result.json').read_text())['rows'][0];main=json.loads((p/'run/result.json').read_text());sc=dw['s_center'];edge=dw['edge_pc']/440.4221297174536
ins,_=interior(sc,0,0,1e-11)
def inside(x):
 Q,h=ins.sol(x);z=Q/x**2;y=(z+np.sqrt(z*z+4*z))/2;yp=(h-2*z/x)/(y*(2+y)/(1+y)**2)
 return y/(1+y),yp/(1+y)**2
we=inside(edge)[0];q=ins.sol(edge)[0];z=q/edge**2;mh=edge**2*(z+np.sqrt(z*z+4*z))/2
vals=[]
for offset,tol in [(30,1e-7),(40,1e-8)]:
 ex=exterior(edge,we,0,offset,tol)
 jin=quad(lambda x:x*x*inside(x)[1]**2+2*inside(x)[0]**2,1e-10,edge,epsabs=1e-10)[0]
 def integrand(x):
  h,w=ex.sol(x);wp=-2*w/x-h
  return x*x*wp*wp+2*w*w
 jout=quad(integrand,edge,edge+offset,epsabs=1e-10)[0];vals.append(jin+jout)
checks=[]
def ck(n,b,v):checks.append(dict(name=n,passed=bool(b),value=str(v)));print(n,b,v)
ck('field_inertia_repeat',abs(vals[0]/vals[1]-1)<1e-5,vals)
coeff=vals[1]/(3*mh);imax=main['inventory']['inertial_excess_fraction_max'];eta_max=imax/coeff
k,ell=s.symbols('k ell',positive=True);deriv=s.diff(1/(1+k*k*ell*ell),k)
ck('no_finite_fastest_fragmentation_mode',s.simplify(deriv+2*k*ell**2/(1+k*k*ell*ell)**2)==0,deriv)
cluster=main['clusters'][0];mass=cluster['mass_median'];b=cluster['b_median_Mpc']*1e6;rho=3*mass/(4*np.pi*b**3);rc=dw['edge_pc'];m=dw['mass_Msun'];N=rho*(4*np.pi/3)*rc**3/m
G=4.30091727e-3;rr=1e4;m10=4*np.pi/3*rho*rr**3;vf=np.sqrt(1+G*m10/(rr*200**2))-1
heat=8*np.pi*G**2*m*.01*np.log(2000/(2*rc))/200*1022.712165 # (km/s)^2/Gyr
ck('dilute_cluster_centres',0<cluster['filling_median']<.01,cluster['filling_median'])
ck('small_mean_force_not_central_occupancy',vf<.1 and N<.01,dict(speed_fraction=vf,mean_core_count=N))
out=dict(checks=checks,J=vals[1],m_dimensionless=mh,inertia_coefficient=coeff,eta_rho_scale_max_99growth=eta_max,cluster_density_Msun_pc3=rho,mean_mass_inside_dwarf_edge=m*N,mean_N_inside_dwarf_edge=N,Poisson_probability_at_least_one=-np.expm1(-N),mass_inside_10kpc=m10,speed_fraction_at_10kpc_200kms=vf,illustrative_distant_total_velocity_diffusion_kms2_per_Gyr=heat)
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
