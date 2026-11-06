"""Conditional spectrum, competing clocks and virial thermal checks."""
import argparse,json
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--mutate',action='store_true');args=p.parse_args()
checks={}
def eq(name,lhs,rhs):checks[name]=bool(s.simplify(lhs-rhs)==0)
E,m,theta,rate=s.symbols('E m theta rate',positive=True)
# Soft scalar scattering: mean drift and second moment per unit time.
D1=rate*E*(4*theta-E)/m; D2=2*rate*theta*E**2/m
pdf=E**2*s.exp(-E/theta)/(2*theta**3)
eq('Wien normalization',s.integrate(pdf,(E,0,s.oo)),1)
eq('zero spectral current',D1*pdf-s.diff(D2*pdf,E)/2,0)
eq('mean radiation energy',s.integrate(E*pdf,(E,0,s.oo)),3*theta)
eq('Compton temperature equals material temperature',s.integrate(E**2*pdf,(E,0,s.oo))/(4*s.integrate(E*pdf,(E,0,s.oo))),theta)
beta2,mu=s.symbols('beta2 mu',real=True)
# isotropic target velocity covariance <beta_i beta_j>=theta/m delta_ij;
# |n_out-n_in|^2=2(1-mu), isotropic soft scattering <mu>=0.
eq('Doppler second moment angular average',s.integrate(2*E**2*theta/m*(1-mu)/2,(mu,-1,1)),2*E**2*theta/m)
Ei,Ef=s.symbols('Ei Ef',positive=True)
N=m*(1/Ef-1/Ei)+2*s.log(Ei/Ef)
eq('cold mean closure collision integral',-s.diff(N,Ef),(m+2*Ef)/Ef**2)
clock=(m/Ef-m/Ei+4*s.log(Ei/Ef)+4*(Ei-Ef)/m)/4
eq('cold mean closure time integral',-s.diff(clock,Ef),(m+2*Ef)**2/(4*m*Ef**2))
lam,n,t,R=s.symbols('lam n t R',positive=True)
K=lam**2/(64*s.pi*m*m);sig0=lam**2/(16*s.pi*m*m)
eq('soft scatter to annihilation rate',sig0/K,4)
ndecay=n/(1+n*K*t)
eq('depleting target density',s.diff(ndecay,t),-K*ndecay**2)
Nsoft=4*s.log(1+n*K*t)
eq('integrated soft scatter clock',s.diff(Nsoft,t),sig0*ndecay)
eq('density fraction after scatter exposure',s.exp(-Nsoft/4),ndecay/n)
tau=n*sig0*R;tdiff=tau*R;ta=1/(n*K)
eq('diffusion to annihilation time estimate',tdiff/ta,tau**2/4)
Nc,Na,theta_i,E0=s.symbols('Nc Na theta_i E0',positive=True)
Tf=(s.Rational(3,2)*Nc*theta_i+Na*E0)/(s.Rational(3,2)*Nc+3*Na)
eq('closed cell energy conservation',(s.Rational(3,2)*Nc+3*Na)*Tf,s.Rational(3,2)*Nc*theta_i+Na*E0)
bound=s.symbols('bound',positive=True)
ratio=s.Rational(3,2)*(bound-theta_i)/(E0-3*bound)
eq('cold energy budget threshold',Tf.subs(Na,Nc*ratio),bound)
U=n*m/16
eq('boundary bath pressure ratio',U/(3*n*theta),m/(48*theta))
# One-zone fixed mass virialized object: Etotal=-C*theta, dE/dt=H-L.
C,H,L0,theta0=s.symbols('C H L0 theta0',positive=True)
L=L0*(theta/theta0)**2
rhs=(H-L)/C if args.mutate else (L-H)/C
eq('virial energy conservation',-C*rhs,H-L)
eq('surface cooling thermal eigenvalue',s.diff(rhs,theta).subs(theta,theta0),2*L0/(C*theta0))
M,kap,Tc=s.symbols('M kap Tc',positive=True)
# Ldiff proportional R*T^4/(kappa*rho) and rho proportional M/R^3.
Ldiff=R**4*theta**4/(kap*M)
eq('constant opacity virial diffusion neutral slope',s.diff(Ldiff.subs(R,Tc/theta),theta),0)
result={'checks':checks,'passed':sum(checks.values()),'total':len(checks),'mutation':args.mutate,'scope':'Exact identities for stated closures, not a halo transport simulation.'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
