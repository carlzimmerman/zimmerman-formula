"""Conditional symmetry and response tests; no microscopic RG integration."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--mutate',action='store_true');a=p.parse_args()
n,z=s.symbols('n z',real=True)
checks=[]
def ck(name,expr):
    v=s.factor(s.simplify(expr));checks.append(dict(name=name,passed=v==0,residual=str(v)))
ck('bare_conformal_power',n-(n-1 if a.mutate else n))
ck('compensated_vacuum_weight',n+z-(n+z))
ck('compensated_quadratic_weight',n+z-(n+z-2)-2)
ck('source_density_weight',n-n)
c,G,alpha,lv,k2,k3,t,u1,u2,u3=s.symbols('c G alpha lambda_v k2 k3 minus_sin_phase u1 u2 u3',positive=True)
a0=8*c**2/(3*alpha*k2*k3*t*s.sqrt(u1*u2*u3))
rho=(2 if a.mutate else 1)*lv*c**2/(8*s.pi*G*alpha**2)
kappa=s.simplify(a0/(c*s.sqrt(G*rho)))
expected=8*s.sqrt(8*s.pi)/(3*k2*k3*t*s.sqrt(lv*u1*u2*u3))
ck('vacuum_to_force_ratio',kappa-expected)
ck('vacuum_amplitude_sensitivity',lv*s.diff(kappa,lv)/kappa+s.Rational(1,2))
ck('initial_amplitude_sensitivity',k2*s.diff(kappa,k2)/kappa+1)
ck('phase_sensitivity',t*s.diff(kappa,t)/kappa+1)
ck('common_length_cancels',s.diff(kappa,alpha))
ck('c_G_cancel',s.diff(kappa,c)+s.diff(kappa,G))
# u1+u2<1 so constrained u3>0. Work with kappa squared to avoid branch simplification.
ksq=s.factor(kappa**2).subs(u3,1-u1-u2)
ck('particle_variation_on_cancellation_surface',s.diff(ksq,u1)/ksq-(-1/u1+1/(1-u1-u2)))
delta,gN,A=s.symbols('delta gN A',positive=True)
g=(s.sqrt(A**2*delta**2+4*A*gN)-A*delta)/2
ck('conditional_force_root',delta*g+g**2/A-gN)
ck('lowest_gradient_linear_law',s.limit(g/gN,gN,0)-1/delta)
ck('zero_residual_mond',s.limit(g,delta,0)-s.sqrt(A*gN))
ck('residual_ratio',delta*g/(g*g/A)-delta*A/g)
result=dict(mutated=a.mutate,passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,kappa=str(kappa),scope='operator weights and conditional constitutive relations only; no full Yang-Mills solution or quantum gravity matching')
Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
