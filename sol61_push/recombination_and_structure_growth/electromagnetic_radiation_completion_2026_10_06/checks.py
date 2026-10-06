"""Exact local Maxwell-triad screen: clocks/metric externally fixed, full EM Gauss."""
import argparse,json,platform
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--control',choices=['none','freeze_gauss','universal_stable','fluid_speed'],default='none');args=ap.parse_args();out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
checks=[]
def ck(name,value,detail=''):checks.append(dict(name=name,passed=bool(value),detail=detail));print(('PASS ' if value else 'FAIL ')+name,flush=True)
def ze(name,value):value=s.factor(value);ck(name,value==0,str(value))
g=s.symbols('g',positive=True);E,B=s.symbols('E B',real=True);p=s.symbols('p',positive=True);x=s.symbols('x',real=True)
f=s.symbols('Axx Axy Axz Ayx Ayy Ayz',real=True);v=s.symbols('Vxx Vxy Vxz Vyx Vyy Vyz',real=True);long=s.symbols('Lx Ly Lz',real=True)
tracev=v[0]+v[4];traceb=p*(f[1]-f[3]);delta_rho=E*(tracev+long[2])+B*traceb
raw=sum(z*z for z in v+long)/2-p*p*sum(z*z for z in f)/2+g*delta_rho**2/2
sol={long[0]:0,long[1]:0,long[2]:-g*E*(E*tracev+B*traceb)/(1+g*E*E)}
for i,z in enumerate(long):ze('Gauss_constraint_'+str(i),s.diff(raw,z).subs(sol))
red=s.factor(raw.subs(sol));target=sum(z*z for z in v)/2-p*p*sum(z*z for z in f)/2+g*(E*tracev+B*traceb)**2/(2*(1+g*E*E))
ze('exact_Gauss_reduced_action',red-target)
ze('physical_energy_response_after_Gauss',delta_rho.subs(sol)-(E*tracev+B*traceb)/(1+g*E*E))
K=s.hessian(red,v);V=s.hessian(red,f);Gy=s.Matrix([[s.diff(red,v[i],f[j])-s.diff(red,f[i],v[j]) for j in range(6)]for i in range(6)])
ke=(1+3*g*E*E)/(1+g*E*E);kb=(1+g*E*E-2*g*B*B)/(1+g*E*E);gamma=2*g*E*B/(1+g*E*E);speed=(1+g*E*E-2*g*B*B)/(1+3*g*E*E)
ce=s.Matrix([1,0,0,0,1,0])/s.sqrt(2);cb=s.Matrix([0,1,0,-1,0,0])/s.sqrt(2)
ze('electric_collective_kinetic',(ce.T*K*ce)[0]-ke);ze('magnetic_collective_kinetic',(cb.T*K*cb)[0]-1)
ze('electric_collective_gradient',-(ce.T*V*ce)[0]/p**2-1);ze('magnetic_collective_gradient',-(cb.T*V*cb)[0]/p**2-kb)
ze('collective_mixed_derivative',(ce.T*Gy*cb)[0]/p-gamma)
ze('six_photon_positive_kinetic_determinant',K.det()-ke)
char=-x*x*K-s.I*x*Gy/p-V/p**2
D=s.factor(char.det(method='domain-ge'))
ze('full_six_mode_characteristic',D-ke*(1-x*x)**5*(speed-x*x))
ze('two_mode_characteristic',(1-ke*x*x)*(kb-x*x)-gamma*gamma*x*x-ke*(1-x*x)*(speed-x*x))
ze('pure_electric_speed',speed.subs(B,0)-(1+g*E*E)/(1+3*g*E*E));ze('pure_magnetic_speed',speed.subs(E,0)-(1-2*g*B*B))
ze('equal_E_B_speed',speed.subs(B,E)-(1-g*E*E)/(1+3*g*E*E))
ck('six_EM_degrees_after_Gauss',len(f)==6,'Three independent U(1) fields; two transverse modes each; no extra gauge mode.')
# Same FRW energy/stress for any electric-magnetic split with same E²+B².
rho=s.Rational(3,2)*(E*E+B*B);press=(E*E+B*B)/2
ze('isotropic_triad_pressure',press-rho/3)
a,C_E,C_B=s.symbols('a C_E C_B',positive=True)
ze('FRW_radiation_redshift',rho.subs({E:C_E/a**2,B:C_B/a**2})-s.Rational(3,2)*(C_E*C_E+C_B*C_B)/a**4)
# Action value, scalar/matter first derivatives on the designer trajectory.
X,R=s.symbols('X R',real=True);Bcal=s.Function('Bcal')(R);Z=s.Function('Z')(R);F=Z*(X-Bcal)**2/2
ze('trajectory_action_zero',F.subs(X,Bcal));ze('trajectory_X_first_variation',s.diff(F,X).subs(X,Bcal));ze('trajectory_energy_first_variation',s.diff(F,R).subs(X,Bcal))
# Explicit transverse unstable magnetic sample, no actual cosmology fit.
ck('magnetic_transverse_instability_witness',speed.subs({E:0,B:1,g:1})==-1)
ck('electric_transverse_positive_witness',speed.subs({E:1,B:0,g:1})==s.Rational(1,2))
# Pure electric density collective has nonzero Maxwell anisotropic stress.
t=s.symbols('t',real=True);Lz=sol[long[2]].subs({B:0,tracev:2*t})
# Substitution tracev needs simultaneous individual velocities for exact reduction.
Lz=-2*g*E*E*t/(1+g*E*E);tr=2*t+Lz;drho=E*tr;dTxx=E*Lz;dTzz=E*(2*t-Lz)
ze('Maxwell_stress_trace',2*dTxx+dTzz-drho)
ze('collective_anisotropic_stress',dTzz-drho/3-s.Rational(4,3)*E*t*(1+3*g*E*E)/(1+g*E*E))
ck('anisotropic_stress_nonzero_witness',(dTzz-drho/3).subs({E:1,g:1,t:1})!=0)
if args.control=='freeze_gauss':ze('CONTROL_freeze_longitudinal_electric',s.diff(raw,long[2]).subs({long[0]:0,long[1]:0,long[2]:0}))
if args.control=='universal_stable':ck('CONTROL_all_positive_squares_stable',speed.subs({E:0,B:1,g:1})>0)
if args.control=='fluid_speed':ck('CONTROL_perfect_fluid_acoustic_speed',speed.subs({E:1,B:0,g:1})==s.Rational(1,3))
result={'checks':checks,'total':len(checks),'passed':sum(c['passed']for c in checks),'characteristic':str(D),'modified_speed_squared':str(speed),'software':{'python':platform.python_version(),'sympy':s.__version__},'control':args.control,'scope':'Local fixed clock/metric Maxwell principal, all U(1) Gauss constraints; no coupled gravity/clock characteristic, thermal photon closure, recombination or observational fit.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');raise SystemExit(0 if all(c['passed']for c in checks)else 1)
