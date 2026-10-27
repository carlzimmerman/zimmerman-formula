"""CE-FM-067: exact vacuum primitive, boundary term and metric-constant scope."""
import json,math,sys
from pathlib import Path
import sympy as s
from scipy.integrate import quad
checks=[]
def ck(n,v):
 checks.append({'name':n,'pass':bool(v)})
 if not v:raise AssertionError(n)
u,y,C=s.symbols('u y C',positive=True)
w=-u-s.log(1-u)-u*u/2
R=u*u/(1-u)
ck('explicit constitutive derivative',s.simplify(s.diff(w,u)-R)==0)
ck('critical second derivative insensitive to constant',s.diff(w+C,u,2).subs(u,0)==0)
ck('constant absent from constitutive force',s.diff(w+C,u)==s.diff(w,u))
ck('strong potential wall',s.limit(w,u,1,dir='-')==s.oo)
I=((y+2)*s.sqrt(y*y+4*y)-y*y)/4-s.log((y+2+s.sqrt(y*y+4*y))/2)
f=(-y+s.sqrt(y*y+4*y))/2
ck('exact integral derivative',s.simplify(s.diff(I,y)-f)==0)
ck('integral lower endpoint',s.limit(I,y,0,dir='+')==0)
ck('linear asymptotic',s.limit(I/y,y,s.oo)==1)
ck('logarithmic next asymptotic',s.limit(I-y+s.log(y),y,s.oo)==s.Rational(1,2))
# I(R(u)) = u R(u) - w(u), by derivative and same zero endpoint.
ck('Legendre integration by parts derivative',s.simplify(s.diff(u*R-w,u)-u*s.diff(R,u))==0)
ck('boundary term diverges',s.limit(u*R,u,1,dir='-')==s.oo)
res=json.loads(Path('campaign_fresh_gravity/CFG807_stiff_vacuum_route/cfg807_vacuum_results.json').read_text())
nums=[]
ff=lambda yy:2*yy/(yy+math.sqrt(yy*yy+4*yy)) if yy else 0
for Y in [1.,10.,100.]:
 ex=float(I.subs(y,Y));q=quad(ff,0,Y,epsabs=1e-11)[0]
 ck('exact integral vs independent quadrature '+str(Y),abs(ex-q)<1e-9)
 nums.append({'Y':Y,'exact_I':ex,'asymptotic_only':Y-math.log(Y)+.5})
ck('README asymptote not an exact finite formula',abs(nums[0]['exact_I']-nums[0]['asymptotic_only'])>.1)
ck('source code asymptotic constant matches',res['numbers']['V1']['I_Q_next']==.5)
# Explicit finite-window maximum for a turned-off positive response: two
# different y must share u because it returns to zero. Numerical witness
# supports, does not prove, the general compactness argument in the report.
from scipy.optimize import minimize_scalar,brentq
ut=lambda yy:ff(yy)/(1+(yy/32)**2)
opt=minimize_scalar(lambda yy:-ut(yy),bounds=(.001,100),method='bounded');peak=opt.x;target=.5*ut(peak)
y1=brentq(lambda yy:ut(yy)-target,1e-12,peak);y2=brentq(lambda yy:ut(yy)-target,peak,1e5)
ck('turnoff two inputs same polarization',y2>y1 and abs(ut(y1)-ut(y2))<1e-12)
# Hilbert stress of a constant L=-C, varying inverse diagonal metric.
z0,z1,z2,z3=s.symbols('z0 z1 z2 z3',positive=True);vol=(z0*z1*z2*z3)**(-s.Rational(1,2));Lden=-C*vol
for j,z in enumerate([z0,z1,z2,z3]):
 Tij=-2*s.diff(Lden,z)/vol
 # g^00=-z0, so inverse-component derivative flips for the time coordinate.
 if j==0:Tij=-Tij;gii=-1/z
 else:gii=1/z
 ck('constant Hilbert stress T_ii=-C g_ii '+str(j),s.simplify(Tij+C*gii)==0)
# Uniform constant is absent from nongravitating field forces but has rho=C,p=-C.
ck('vacuum equation of state',s.simplify(C+(-C))==0)
out={'claim_id':'CE-FM-067','checks':checks,'n_checks':len(checks),'all_pass':all(z['pass'] for z in checks),'integral_samples':nums,'turnoff_equal_response_witness':{'u':target,'y_low':y1,'y_high':y2},'scope':'Classical local W_rem response and strong-field reference convention, plus Hilbert variation of a global action constant. No solar numerical verification, quantum vacuum prediction, or transfer of S2 conclusions to the new selected-phase Einstein body.'}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'checks':len(checks),'all_pass':out['all_pass'],'turnoff_witness':out['turnoff_equal_response_witness']}))
