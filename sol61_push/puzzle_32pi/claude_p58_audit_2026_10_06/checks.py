import argparse,json,pathlib,math,re
import sympy as s, mpmath as mp
from scipy.optimize import brentq
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['operator','tail','sigma']);args=ap.parse_args(); checks=[]
def ck(n,b,d=None):checks.append(dict(name=n,passed=bool(b),detail=d))
def zero(n,x):x=s.simplify(x);ck(n,x==0,str(x))
z,q,E,R=s.symbols('z q E R',positive=True)
P=2*q**3+q*q+6*q+12;D=-2*q**3+q*q-6*q+12
moments={}
for si,power,sp,sl,expect in [(-s.Rational(1,2),3,-24*z**7/7+12*z**5-50*z**3/3+10*z,-24*z**7/7-12*z**5-50*z**3/3-10*z,-s.Rational(32,147)),(s.Rational(3,2),1,-8*z**3+12*z+2*z/(z*z-1),-8*z**3-12*z+2*z/(z*z+1),-s.Rational(4,7))]:
 zero('plus_primitive_'+str(si),s.diff(sp,z)+2*(z*z-1)**power*P.subs(q,1/(z*z-1)))
 zero('low_primitive_'+str(si),s.diff(sl,z)+2*(z*z+1)**power*D.subs(q,1/(z*z+1)))
 zero('high_primitive_'+str(si),s.diff(sp,z)-2*(1-z*z)**power*D.subs(q,1/(1-z*z)))
 upper=s.limit(sp.subs(z,s.sqrt(1+1/R))+sp.subs(z,s.sqrt(1-1/R)),R,s.oo)
 lower=s.limit(sl.subs(z,s.sqrt(1/E-1))-sp.subs(z,s.sqrt(1/E+1)),E,0,dir='+')
 val=-s.Rational(2,35)*(upper+lower);zero('exact_Mellin_'+str(si),val-expect);moments[str(si)]=str(val)
a,y,nu,df=s.symbols('a y nu df',positive=True)
AA,DD,t=s.symbols('AA DD t')
projected=s.Rational(1,2)+AA*(AA+DD)/(2*(AA+DD-DD*t))
qumond=(AA+1+DD*t)/2
zero('exact_angular_operator_difference',projected-qumond+DD**2*t*(1-t)/(2*(AA+DD-DD*t)))
angular_difference=s.simplify((projected-qumond).subs({AA:3,DD:-1,t:s.Rational(1,2)}))
zero('nontrivial_operator_witness',angular_difference+s.Rational(1,20))
zero('projected_visible_spherical',(y+(2*nu-1)*y)/2-nu*y)
# AQUAL star Born flux correction is twice QUMOND boost; visible half cancels.
zero('Born_source_physical_half',s.Rational(1,2)*2*df-df)
zero('uncut_linear_constant',-s.Rational(9,8)*(-s.Rational(32,147))-s.Rational(12,49))
zero('cutoff_cubic_constant',-s.Rational(9,8)*(-s.Rational(4,7))-s.Rational(9,14))
mp.mp.dps=42
ge=mp.mpf('2.146e-10');GM=4*mp.pi**2*mp.mpf('1.495978707e11')**3/mp.mpf('3.15576e7')**2;T=mp.mpf('128.9153707043');aref=mp.mpf('9.3603e-11')
def F(q):
 p=2*q**3+q*q+6*q+12;d=-2*q**3+q*q-6*q+12
 return -2/(35*q**3)*(p/mp.sqrt(1+q)-mp.sign(1-q)*d/mp.sqrt(abs(1-q)))
def b(y):return 1/(y*(mp.sqrt(1+1/y)+1))
cache={}
def quadr(a,cut=None,lo='1e-7',hi='1e7'):
 a=mp.mpf(a);eta=ge/a
 e=(mp.sqrt(1+4*eta**2)-1)/2 if cut is None else mp.findroot(lambda e:e*(1+b(e)/(1+(e/cut)**2))-eta,eta)
 f=lambda q:b(e/q)*(1 if cut is None else 1/(1+(e/q/cut)**2))*F(q)/q**mp.mpf('2.5')
 integ=mp.quad(f,[mp.mpf(lo),.1,.5,1,2,10,mp.mpf(hi)])
 return -9*a/(4*mp.sqrt(GM/a))*e**mp.mpf('1.5')*integ
vals=[]
for a0 in ['1e-12','2e-12','5e-12','1e-11','2e-11','4e-11','6e-11','8.32e-11','9.3603e-11','1.13e-10']:
 v=quadr(a0);vals.append((float(a0),float(v)));cache[float(a0)]=float(v)
ck('sampled_Q_monotonic',all(vals[i+1][1]>vals[i][1] for i in range(len(vals)-1)))
qref=quadr(aref);qcut=quadr(aref,T)
ck('p58_reference_independent_integral',abs(qref/mp.mpf('2.195e-26')-1)<mp.mpf('.001'),str(qref))
qrough=quadr(aref,lo='1e-5',hi='1e5');ck('quadrature_truncation_check',abs(qrough/qref-1)<mp.mpf('1e-7'),str(qrough/qref-1))
ck('p57_cutoff_near_reference',abs(qcut/qref-1)<mp.mpf('.003'),str(qcut/qref))
small=mp.mpf('1e-17');qu=quadr(small);qc=quadr(small,T)
cu=mp.mpf(12)/49*mp.sqrt(ge/GM);cc=mp.mpf(9)/14*T*T/(mp.sqrt(GM)*ge**mp.mpf('1.5'))
ck('uncut_small_a_linear',abs(qu/(cu*small)-1)<mp.mpf('1e-5'),str(qu/(cu*small)))
ck('cutoff_small_a_cubic',abs(qc/(cc*small**3)-1)<mp.mpf('1e-5'),str(qc/(cc*small**3)))
# Recompute roots, not p58's coarse log interpolation.
def qfloat(a):
 if a not in cache:cache[a]=float(quadr(a))
 return cache[a]
roots={}
for lab,lim in [('historical1',6e-27),('historical2',9e-27),('historical3',1.2e-26),('updated1',3.4e-27),('updated2',5.2e-27)]:
 aa=brentq(lambda aa:qfloat(aa)-lim,1e-12,6e-11,xtol=1e-18); roots[lab]=dict(a0=aa,kappa=.5*aa/float(aref),Q=qfloat(aa))
 ck('direct_root_'+lab,abs(qfloat(aa)/lim-1)<1e-6)
historicalpull=(float(qref)-3e-27)/3e-27;updatedpull=(float(qref)-1.6e-27)/1.8e-27
ck('historical_6point3_pull',abs(historicalpull-6.3158)<.002)
if args.control=='operator':ck('control_general_QUMOND_equals_projected',angular_difference==0,str(angular_difference))
if args.control=='tail':ck('control_fixed_cutoff_linear_limit',abs(qc/(cu*small)-1)<mp.mpf('.01'),str(qc/(cu*small)))
if args.control=='sigma':ck('control_historical_is_updated_pull',abs(historicalpull-updatedpull)<.01,dict(old=historicalpull,updated=updatedpull))
result=dict(passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,moments=moments,GM=str(GM),Q_reference=str(qref),Q_cutoff=str(qcut),table=vals,roots=roots,historical_pull=historicalpull,updated_pull=updatedpull,asymptotic_constants=dict(uncut=str(cu),cutoff=str(cc)),precision_dps=mp.mp.dps,scope='bounded quadrature/root corroboration; analytic allparameter claims in REPORT; no projected nonlinear BVP rerun')
p=pathlib.Path(args.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(result,indent=2)+'\n');print(f"{result['passed']}/{result['total']}");raise SystemExit(0 if result['passed']==result['total'] else 1)
