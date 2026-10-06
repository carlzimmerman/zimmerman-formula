import argparse,json
from pathlib import Path
import sympy as s
import mpmath as m
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--wrong-parity',action='store_true');a=p.parse_args();checks=[]
def ck(n,b):checks.append({'name':n,'passed':bool(b)})
x=s.symbols('s');r=x-3;ratio=s.Integer(1);total=s.Integer(0)
for n,c in enumerate([12,6,1,2]):
 if n:ratio=s.factor(ratio*-(r+n-1)/(r+n-s.Rational(1,2)))
 total+=c*ratio
ck('four_beta_coefficient_reduction',s.factor(total-20*x*(x-2)/((2*x-5)*(2*x-1)))==0)
for n in range(4):
 ck('reflection_parity_'+str(n),s.trigsimp(1-(-1)**n*(s.cos(s.pi*(x-3+n))-s.sin(s.pi*(x-3+n)))-(1+s.cos(s.pi*x)-s.sin(s.pi*x)))==0)
K=-s.Rational(2,35)*(1+s.cos(s.pi*x)-s.sin(s.pi*x))*s.gamma(x-3)*s.gamma(s.Rational(7,2)-x)/s.sqrt(s.pi)*total
ck('removable_moment_multiplier',s.limit(K,x,s.Rational(1,2))==-4*s.pi/35)
q=s.symbols('q',positive=True);plus=2*q**3+q*q+6*q+12;minus=-2*q**3+q*q-6*q+12
small=-2/(35*q**3)*(plus/s.sqrt(1+q)-minus/s.sqrt(1-q))
large=-2/(35*q**3)*(plus/s.sqrt(1+q)+minus/s.sqrt(q-1))
ck('small_endpoint',s.limit(small/q**2,q,0)==s.Rational(1,10))
v=s.symbols('v',positive=True)
ck('large_endpoint',s.limit(large.subs(q,1/v)/v**s.Rational(7,2),v,0)==-1)
ck('trig_factorization',s.trigsimp(1+s.cos(s.pi*x)-s.sin(s.pi*x)-2*s.cos(s.pi*x/2)*(s.cos(s.pi*x/2)-s.sin(s.pi*x/2)))==0)
m.mp.dps=65
def formula(z):return -m.mpf(2)/35*(1+m.cos(m.pi*z)-m.sin(m.pi*z))*m.gamma(z-3)*m.gamma(m.mpf('3.5')-z)/m.sqrt(m.pi)*20*z*(z-2)/((2*z-5)*(2*z-1))
eps=m.mpf('1e-6');R=m.mpf('1e6');rows=[]
for w in ['.25','1','2']:
 z=m.mpf('.5')-1j*m.mpf(w)
 def low(v):
  q=1-v*v;pp=2*q**3+q*q+6*q+12;mm=-2*q**3+q*q-6*q+12
  return -4*q**(z-1)/(35*q**3)*(v*pp/m.sqrt(1+q)-mm)
 def high(v):
  q=1+v*v;pp=2*q**3+q*q+6*q+12;mm=-2*q**3+q*q-6*q+12
  return -4*q**(z-1)/(35*q**3)*(v*pp/m.sqrt(1+q)+( -mm if a.wrong_parity else mm))
 integral=m.quad(low,[0,m.mpf('.5'),m.sqrt(1-eps)])+m.quad(high,[0,m.mpf('.5'),1,10,100,m.sqrt(R-1)])
 wanted=formula(z);error=abs(integral-wanted)
 ck('bounded_complex_mellin_'+w,error<m.mpf('1e-13'))
 rows.append({'s':str(z),'cutoff_integral':str(integral),'formula':str(wanted),'absolute_difference':str(error)})
ck('tested_fourier_multipliers_nonzero',all(abs(formula(m.mpf('.5')-1j*m.mpf(w)))>m.mpf('1e-10') for w in ['.25','1','2']))
out={'checks':checks,'summary':{'passed':sum(c['passed'] for c in checks),'total':len(checks)},'numeric_rows':rows,'bounds':{'q_min':str(eps),'q_max':str(R),'mp_digits':65},'scope':'Symbolic formula reductions and bounded complex cutoff comparisons; universal injectivity is the written proof, not these samples.'}
Path(a.output).parent.mkdir(parents=True,exist_ok=True);Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['summary']));raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
