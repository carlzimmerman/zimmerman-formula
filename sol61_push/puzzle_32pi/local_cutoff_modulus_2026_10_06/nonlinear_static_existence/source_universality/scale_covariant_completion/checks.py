import argparse,json,pathlib,sys
import sympy as S
import mpmath as mp
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--control',default='none');a=p.parse_args();checks=[]
def ck(name,ok):checks.append({'name':name,'passed':bool(ok)})
y,T,z,L,beta=S.symbols('y T z L beta',positive=True)
b=S.sqrt(1+1/y)-1;c=b/(1+(y/T)**2);ct=S.diff(c,T);cy=S.diff(c,y)
ck('T derivative positive factor',S.simplify(ct-2*T*y*y*b/(T*T+y*y)**2)==0)
ck('frozen force derivative',S.simplify(1+c+y*cy-(1+(b+y*S.diff(b,y))/(1+z*z)-2*b*z*z/(1+z*z)**2)).subs(T,y/z).simplify()==0)
ck('b plus ybprime positive factor',S.simplify(b+y*S.diff(b,y)-b*b/(2*(b+1)))==0)
ck('restricted stationarity integral coefficient',4*S.integrate(S.Symbol('t')**3,(S.Symbol('t'),y/2,y))==S.Rational(15,16)*y**4)
ck('healthy sufficient threshold',S.Rational(32,15)*9*S.Rational(5,96)==1)
ck('fixed stiffness not scale covariant',L**-2==1 if a.control=='fixed_stiffness' else L**-2!=1)
Ty=S.symbols('Ty',positive=True); Dfull=1+c+y*cy+y*ct*Ty
ck('envelope second derivative retains Ty',S.simplify(Dfull-(1+c+y*cy))==0 if a.control=='drop_Ty' else S.simplify(Dfull-(1+c+y*cy)-y*ct*Ty)==0)
mp.mp.dps=50
# Scale t=T u for quadrature, stable near the endpoint.
def raw(y,T):
 z=y/T
 def bb(u):return 1/(mp.sqrt(1+1/(T*u))+1)/(T*u) if u else mp.mpf(0)
 def qq(u):return 4*T*u**3*bb(u)/(1+u*u)**2 if u else mp.mpf(0)
 qt=mp.quad(qq,[0,min(z,1),z])
 qtt=mp.quad(lambda u:qq(u)*(1-4/(1+u*u))/T,[0,min(z,1),z])
 by=1/(mp.sqrt(1+1/y)+1)/y
 ct=2*T*y*y*by/(T*T+y*y)**2
 cy=-1/(2*y*y*mp.sqrt(1+1/y))/(1+z*z)-2*y*by/T**2/(1+z*z)**2
 lam=qt/T;den=lam-qtt;ty=2*y*ct/den
 D=1+by/(1+z*z)+y*cy+y*ct*ty
 return lam,D,den,ty
w=raw(mp.mpf('3e-8'),mp.mpf('1e-8'))
ck('large lambda actual derivative negative',w[1]>0 if a.control=='large_lambda_healthy' else w[1]<-90)
ck('large lambda minimum still positive Hessian',w[2]>0)
mp.mp.dps=70;w2=raw(mp.mpf('3e-8'),mp.mpf('1e-8'))
ck('two quadrature precisions agree',abs(w[1]-w2[1])<mp.mpf('1e-40'))
# Only four representative admitted-branch points; theorem, not grid, establishes global sign.
mp.mp.dps=30
lam=mp.mpf('.01');samples=[]
for yy in ['1e-5','.01','1','100']:
 yy=mp.mpf(yy);lo=mp.mpf('1e-20');hi=mp.pi/(2*lam)
 for it in range(90):
  mid=mp.sqrt(lo*hi)
  if raw(yy,mid)[0]>lam:lo=mid
  else:hi=mid
 tt=mp.sqrt(lo*hi);rr=raw(yy,tt);samples.append({'y':str(yy),'T':str(tt),'D':str(rr[1])})
 ck('sample admitted force derivative '+str(yy),rr[1]>0)
 ck('sample stationarity residual '+str(yy),abs(rr[0]-lam)<mp.mpf('1e-20'))
result={'checks':checks,'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'control':a.control,'witness':{'lambda':str(w2[0]),'D':str(w2[1]),'auxiliary_Hessian':str(w2[2])},'samples':samples,'scope':'exact identities plus bounded quadrature; analytic inequalities establish global admitted interval'}
o=pathlib.Path(a.output);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(json.dumps(result,indent=2));print(json.dumps(result));sys.exit(bool(result['failed']))
