"""Positive generalized Stieltjes spectral-moment / NR-action bounded audit."""
import argparse,json,math
from pathlib import Path
import mpmath as mp
mp.mp.dps=60
p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--mutation',choices=['none','moment_factor','pole_finite','mass_dictionary'],default='none');args=p.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
A=mp.mpf(1);B=8*A/(3*mp.pi);K=B/3;s0=mp.mpf(16);eps=mp.mpf('1e-6');shift=mp.mpf(1);S=(s0**mp.mpf('1.5')+shift/(eps*K))**(mp.mpf(2)/3)
def F(v):
 return mp.betainc(mp.mpf("2.5"),mp.mpf(".5"),0,v/(1+v))
def e(y,s):return B/mp.sqrt(y)*F(s/y)
def de(y,s):
 v=s/y;return -e(y,s)/(2*y)-B*y**(-mp.mpf('1.5'))*v**mp.mpf('2.5')/(1+v)**3
def em(y):return (1-eps)*e(y,s0)+eps*e(y,S)
def dem(y):return (1-eps)*de(y,s0)+eps*de(y,S)
checks=[]
def ck(name,passed,detail):checks.append({'name':name,'passed':bool(passed),'detail':detail})
for y in map(mp.mpf,['.001','.1','1','100','1e6']):
 q=mp.quad(lambda t:B*t**mp.mpf('1.5')/(y+t)**3,[0,s0])
 ck('closed_form_matches_spectral_integral',mp.almosteq(q,e(y,s0),rel_eps=mp.mpf('1e-45')),{'y':str(y),'error':str(q-e(y,s0))})
for alpha in map(mp.mpf,['2.5','3','4']):
 t=mp.mpf('2.3');moment=mp.quad(lambda y:y/(y+t)**alpha,[0,t,mp.inf]);exact=t**(2-alpha)/((alpha-1)*(alpha-2))
 if args.mutation=='moment_factor':exact*=2
 ck('generalized_integral_moment',abs(moment/exact-1)<mp.mpf('1e-28'),{'alpha':str(alpha),'integral':str(moment),'exact':str(exact)})
# Spectral Tonelli moment, separate outer t integration, then numerical y integral.
C0=K*s0**mp.mpf('1.5');Cm=(1-eps)*C0+eps*K*S**mp.mpf('1.5')
Cquad=mp.quad(lambda y:y*em(y),[0,1,s0,S,mp.inf])
ck('analytic_family_shift_exact',abs(Cm-C0-shift)<mp.mpf('1e-45') and abs(Cquad/Cm-1)<mp.mpf('1e-20'),{'C0':str(C0),'Cm':str(Cm),'S':str(S),'quadrature':str(Cquad)})
Y=mp.mpf(10);bound=eps*((3*mp.pi/8)/F(s0/Y)-1)
grid=[mp.power(10,mp.mpf(-10)+mp.mpf(20)*i/180) for i in range(181)]
mins=[mp.inf,mp.inf,mp.inf];max_window=mp.mpf(0)
for y in grid:
 ex=em(y);dx=1+2*ex+2*y*dem(y)
 eigen=[mp.mpf(2),2/(1+2*ex),2/dx]
 mins=[min(a,b) for a,b in zip(mins,eigen)]
 if y<=Y:max_window=max(max_window,abs(ex/e(y,s0)-1))
ck('full_NR_Hessian_eigenblocks_positive_on_grid',all(t>0 for t in mins),{'minima':list(map(str,mins))})
ck('global_D_analytic_bound',1-2*B/mp.sqrt(s0)>0,{'D_lower_bound':str(1-2*B/mp.sqrt(s0))})
ck('finite_window_uniform_relative_tolerance',max_window<=bound and bound<mp.mpf('1e-5'),{'Y':str(Y),'bound':str(bound),'sample_max':str(max_window)})
ck('fixed_deep_amplitude',abs(mp.sqrt(mp.mpf('1e-24'))*em(mp.mpf('1e-24'))/A-1)<mp.mpf('1e-11'),{'limit_approx':str(mp.sqrt(mp.mpf('1e-24'))*em(mp.mpf('1e-24')))})
# Alternating derivatives of the spectral kernel, not high-order finite differences.
for n in range(7):
 y=mp.mpf('.7');der=mp.rf(3,n)*mp.quad(lambda t:B*t**mp.mpf('1.5')/(y+t)**(3+n),[0,s0])
 ck('spectral_complete_monotonicity',der>0,{'order':n,'signed_derivative':str(der)})
# Primitive dictionary exact differential identity m dz -2ye dy =d(2y²e²).
y=mp.mpf('3.1');ex=em(y);der=dem(y);xx=y*(1+2*ex);D=1+2*ex+2*y*der;m=ex/(1+2*ex)
lhs=m*2*xx*D-2*y*ex;rhs=4*y*ex**2+4*y*y*ex*der
ck('same_action_integral_normalization',abs(lhs-rhs)<mp.mpf('1e-50'),{'difference':str(lhs-rhs)})
# Ordinary positive single pole is a sufficient counterexample to finite-vacuum assertion.
t=mp.mpf(2);R=mp.mpf('1e6');pole=R-t*mp.log(1+R/t)
ck('ordinary_positive_pole_divergence_detected',pole>R/2 if args.mutation!='pole_finite' else pole<100,{'partial_C':str(pole),'R':str(R)})
# Legitimate linear Yukawa source dictionary; same y, distinct masses entails distinct r.
y=mp.mpf(1);mu=mp.mpf(1);masses=[1,4];radii=[mp.sqrt(mass/y) for mass in masses];excesses=[(1+mu*r)*mp.exp(-mu*r) for r in radii]
ck('positive_pole_not_universal_acceleration_law',abs(excesses[0]-excesses[1])>.1 if args.mutation!='mass_dictionary' else mp.almosteq(excesses[0],excesses[1]),{'same_y':str(y),'masses':masses,'radii':list(map(str,radii)),'excesses':list(map(str,excesses))})
result={'A':str(A),'s0':str(s0),'S':str(S),'epsilon':str(eps),'C_base':str(C0),'C_mixture':str(Cm),'window_y_max':str(Y),'relative_window_bound':str(bound),'mutation':args.mutation,'checks':checks,'all_passed':all(c['passed'] for c in checks)}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if result['all_passed'] else 1)
