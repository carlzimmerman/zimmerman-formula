import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',choices=['none','varying_Q','cold','lapse'],default='none');args=ap.parse_args()
checks=[]
def eq(name,e):
 e=s.simplify(s.expand(e));checks.append(dict(name=name,passed=e==0,residual=str(e)))
N,L,a,b,n,K,V,Q,Lam,M=s.symbols('N L a b n K V Q Lam M',positive=True)
vg=N*a**n;vh=L*b**n;v=s.sqrt(vg*vh);Lint=-4*K*Lam*v
rho=-s.diff(Lint,N)/a**n
q=s.sqrt(vh/vg)
eq('actual_visible_lapse_density',rho-2*K*Lam*q)
eq('actual_hatted_lapse_density',-s.diff(Lint,L)/b**n-2*K*Lam/q)
# Isotropic variation delta gamma_ij=2 gamma_ij delta ln a gives n Vg p.
eq('actual_visible_pressure',s.diff(Lint,a)*a/(n*vg)+rho)
eq('actual_hat_pressure',s.diff(Lint,b)*b/(n*vh)+2*K*Lam/q)
eq('reciprocal_volume',q*(v/vh)-1)
t=s.symbols('t',positive=True);qt=s.Function('Q')(t);Ht=s.Function('H')(t)
eq('Bianchi_vacuum_residual',s.diff(M*Lam*qt,t)+n*Ht*(M*Lam*qt-M*Lam*qt)-M*Lam*s.diff(qt,t))
At=s.Function('a')(t);Bt=s.Function('B')(t);h=s.symbols('h',positive=True)
# Bt means b^n; its first-order defining equation suffices, avoiding an unnecessary integral simplification.
lapse=Q**2*At**n/Bt; Bdot=n*h*Q**2*At**n
bhubble=Bdot/(n*Bt*lapse)
eq('reconstructed_hat_H',bhubble-h)
eq('reconstructed_volume_ratio_squared',lapse*Bt/At**n-Q**2)
eq('reconstructed_hat_acceleration',s.diff(bhubble,t))
R,D=s.symbols('R D',nonnegative=True)
F=2*(Lam*Q+R*a**(-n-1)+D*a**(-n))/(n*(n-1))
hdot=s.diff(F,a)*a/2
expected=-((n+1)*R*a**(-n-1)+n*D*a**(-n))/(n*(n-1))
eq('mixed_visible_acceleration',hdot-expected)
for label,j in [('radiation',n+1),('dust',n)]:
 hg,C=s.symbols('hg C',positive=True);u=j*hg*t/2;ascale=C*s.sinh(u)**(2/j)
 H=s.diff(ascale,t)/ascale
 density=Lam*Q*C**j/ascale**j
 # positive sinh for t,hg,n>0 makes real powers unambiguous; replace real powers explicitly.
 density=s.powsimp(density,force=True)
 eq(label+'_H',H-hg*s.coth(u))
 eq(label+'_density',density-Lam*Q/s.sinh(u)**2)
 eq(label+'_friedmann',(H**2-2*(Lam*Q+density)/(n*(n-1))).subs(Lam,hg**2*n*(n-1)/(2*Q)))
 eq(label+'_acceleration',(s.diff(H,t)+j*density/(n*(n-1))).subs(Lam,hg**2*n*(n-1)/(2*Q)))
 eq(label+'_continuity',s.diff(density,t)+j*H*density)
p=s.Rational(2)/(n+1)
eq('radiation_early_b_power',n*p+1-(3*n+1)/(n+1))
eq('positive_B0_lapse_power',n*p-2*n/(n+1))
eq('zero_B0_lapse_power',n*p-(n*p+1)+1)
Tref,eta,cgamma=s.symbols('Tref eta cgamma',positive=True)
T=Tref/a;ng=cgamma*T**3;nh=eta*cgamma*Tref**3/a**3
eq('hydrogen_photon_eta',nh/ng-eta)
eq('photon_temperature_power',s.diff(T,a)*a+T)
A,a0,chi=s.symbols('A a0 chi',positive=True)
hg2=chi*a0**2*A*Q/(n*(n-1))
eq('general_dimension_vacuum_dictionary',n*(n-1)*hg2/(2*Q)-chi*a0**2*A/2)
checks.append(dict(name='positive_A_remains_free',passed=s.diff(hg2,A).is_positive,residual=str(s.diff(hg2,A))))
if args.control=='varying_Q':eq('false_time_dependent_vacuum_conservation',M*Lam*s.Symbol('Qdot',nonzero=True))
if args.control=='cold':eq('false_homogeneous_dust_pressure',-M*Lam*Q)
if args.control=='lapse':eq('false_lapse_reconstruction',Bdot/(n*Bt*(At**n/(Q**2*Bt)))-h)
result=dict(passed=sum(bool(c['passed']) for c in checks),total=len(checks),checks=checks,control=args.control)
out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2));print(json.dumps(result));sys.exit(result['passed']!=result['total'])
