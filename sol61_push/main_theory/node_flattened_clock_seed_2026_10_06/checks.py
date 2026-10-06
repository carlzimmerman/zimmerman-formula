"""Exact force/relative-block reduction and bounded Fourier response, not full admission."""
import argparse,json
from pathlib import Path
import sympy as s
import numpy as np
from scipy.integrate import solve_ivp,quad
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['omit_time_source','finite_harmonics']);args=ap.parse_args();rows=[]
def eq(name,e):rows.append({'name':name,'passed':s.simplify(e)==0})
def ck(name,b):rows.append({'name':name,'passed':bool(b)})
x,j=s.symbols('x j',real=True);f=s.cos(x)-s.cos(3*x)/9
eq('flattened_seed_gradient',s.expand_trig(s.diff(f,x)+s.Rational(4,3)*s.sin(x)**3))
eq('flattened_antiperiodic_zero_mean',s.expand_trig(f.subs(x,x+s.pi)+f))
cj=(10-15*j*j/(j*j-4)+6*j*j/(j*j-16)-j*j/(j*j-36))/(48*s.pi)
closed=-480/(s.pi*(j*j-4)*(j*j-16)*(j*j-36))
eq('exact_odd_Fourier_coefficient',cj-closed)
eq('first_force_harmonic',closed.subs(j,1)-32/(105*s.pi))
eq('high_frequency_force_tail',s.limit(j**6*closed,j,s.oo)+480/s.pi)
b,H,P,a,K,J=s.symbols('b H P a K J',positive=True);z,zd,nu,q,qd=s.symbols('z zd nu q qd',real=True)
A=-b;D=A*H*H-P;alpha=A*H/D;beta=P/D;Kr=A*P/D;c=K*a**3
L=c*(-A*(zd-H*nu)**2+P*(nu+z)**2)+J*nu
sol=(A*H*zd+P*z+J/(2*c))/D
eq('actual_lapse_with_source',s.diff(L,nu).subs(nu,sol))
# Linear source reduction; source-independent completion square and J^2 do not affect z Euler.
Lred=s.expand(L.subs(nu,sol));linear=s.diff(Lred,J).subs(J,0)
eq('reduced_source_not_bare',linear-alpha*zd-beta*z)
F=J*alpha/a;G=J*(beta-H*alpha)/a
def dt(e):return s.diff(e,a)*H*a+s.diff(e,P)*(-2*H*P)+s.diff(e,J)*(-2*H*J)
R=(b*H*H-P)*(2*b*H*H+P)/(b*H*H+P)**2
candidate=G-dt(F)
if args.control=='omit_time_source':candidate=G
eq('actual_q_source_with_time_derivative',candidate-J/a*R)
t=s.symbols('t',nonnegative=True);Rt=s.factor(R.subs(P,t*b*H*H))
eq('uniform_R_upper',2-Rt-t*(5+3*t)/(1+t)**2)
eq('uniform_R_lower',Rt+1-(3+t)/(1+t)**2)
eq('high_frequency_no_smoothing',s.limit(R,P,s.oo)+1)
eq('positive_Kr_form',Kr-b*P/(b*H*H+P))
# Independent physical-space Fourier quadrature.
coeff_errors=[]
for jj in (1,3,5,7,21,41):
 val=2/np.pi*quad(lambda xx:np.sin(xx)**5*np.cos(xx)*np.cos(jj*xx),0,np.pi,epsabs=2e-12)[0]
 exact=-480/(np.pi*(jj*jj-4)*(jj*jj-16)*(jj*jj-36));coeff_errors.append(abs(val-exact))
ck('Fourier_quadrature_independent',max(coeff_errors)<2e-12)
if args.control=='finite_harmonics':ck('false_force_has_only_seed_modes',abs(float(closed.subs(j,7)))<1e-15)
# Reduced equation y0=q,y1=p=2KaKr qdot, with actual a^-2 force amplitude.
# Geometry H=K=a(t0)=1, eta=1/4=>b=9, B=a0=1; h_j sign retained.
endpoint=[]
for jj in (7,15,31,63,127):
 hj=-480/(np.pi*(jj*jj-4)*(jj*jj-16)*(jj*jj-36))
 def rhs(tt,y):
  aa=np.exp(tt);pp=jj*jj/aa**2;kr=9*pp/(9+pp);r=(9-pp)*(18+pp)/(9+pp)**2;force=-16/(3*aa**2)*hj
  return [y[1]/(2*aa*kr),force/aa*r]
 soln=solve_ivp(rhs,[0,1],[0,0],method='DOP853',rtol=1e-10,atol=1e-15)
 ck('relative_integrator_'+str(jj),soln.success)
 endpoint.append({'j':jj,'force_h':hj,'q1':float(soln.y[0,-1]),'q_over_force':float(soln.y[0,-1]/hj)})
ck('bounded_high_frequency_response',max(abs(r['q_over_force']) for r in endpoint)<3)
# Smooth-flat seed is a proof by derivative estimates, not a sampling test.
result={'checks':rows,'passed':sum(r['passed'] for r in rows),'total':len(rows),'max_fourier_quadrature_error':max(coeff_errors),'relative_response':endpoint,'control':args.control,'scope':'one-sided second-order norm-cube forced relative block only; smooth-flat bump lemma analytic; full sourced mean/tensor/constraints unproved'}
out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'total':result['total'],'failed':[r['name'] for r in rows if not r['passed']]}));raise SystemExit(not all(r['passed'] for r in rows))
