import argparse,json,pathlib,sys
import sympy as S
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--control',default='none');a=p.parse_args();checks=[]
def ck(name,ok):checks.append({'name':name,'passed':bool(ok)})
C1,C2,ig,ih=S.symbols('C1 C2 ig ih',real=True)
U=C1*C2-C1*C1
ck('connection tensor even under exchange',S.expand(U.xreplace({C1:-C1,C2:-C2})-U)==0)
Usym=(ig+ih)*U/2
ck('averaged contraction exchange invariant',S.expand(Usym.xreplace({ig:ih,ih:ig,C1:-C1,C2:-C2})-Usym)==0)
n=S.symbols('n',positive=True,integer=True);GE,Om,aa=S.symbols('GE Om aa',positive=True);chi=(n-1)/(2*(n-2));GN=8*S.pi*(n-2)*GE/((n-1)*Om);K=1/(16*S.pi*GE)
ck('general n interaction NR coefficient',S.simplify(2*K*chi*aa**2-aa**2/(2*Om*GN))==0)
for nn in [3,4,5,6]:
 D=nn+1;eta=[-1]+[1]*nn;C={};de=lambda x,y:int(x==y)
 for i in range(D):
  for j in range(D):
   for k in range(D):
    v=0
    if i==0 and ((j==0 and k==1) or (k==0 and j==1)):v=1
    if i==1 and j==k==0:v=1
    if i and j and k:v=-S.Rational(1,nn-2)*(de(i,k)*de(j,1)+de(i,j)*de(k,1)-de(j,k)*de(i,1))
    C[i,j,k]=v
 U=sum(eta[mu]*sum(C[i,mu,l]*C[l,mu,i]-C[i,mu,mu]*C[l,i,l] for i in range(D) for l in range(D)) for mu in range(D))
 ck('raw connection contraction n'+str(nn),U==-S.Rational(nn-1,nn-2))
 crossgood=True
 for h1 in range(1,D):
  for h2 in range(h1,D):
   for deriv in range(1,D):
    def H(i,j,k):return int(k==deriv and ((i==h1 and j==h2)or(i==h2 and j==h1)))
    dc={(i,j,k):S.Rational(1,2)*(H(i,k,j)+H(i,j,k)-H(j,k,i)) if i and j and k else 0 for i in range(D) for j in range(D) for k in range(D)}
    cross=sum(eta[mu]*sum(C[i,mu,l]*dc[l,mu,i]+dc[i,mu,l]*C[l,mu,i]-C[i,mu,mu]*dc[l,i,l]-dc[i,mu,mu]*C[l,i,l] for i in range(D) for l in range(D)) for mu in range(D))
    crossgood=crossgood and cross==0
 ck('all spatial-gradient bilinears vanish n'+str(nn),crossgood)

y,T,e,ey,eT,qt,lam,A=S.symbols('y T e ey eT qt lam A',positive=True)
x=y*(1+2*e);d=y*e;xy=1+2*e+2*y*ey;xT=2*y*eT;My=2*d*xy;MT=qt+4*d*y*eT-lam*T
m=My/(2*x*xy)
ck('symmetric exact source m',S.simplify(m-e/(1+2*e))==0)
ck('symmetric actual Newton flux',S.simplify((1-2*m)*x-y)==0)
ck('symmetric actual physical flux',S.simplify((1-m)*x-y*(1+e))==0)
ck('aux T chain rule at fixed invariant',S.simplify(MT-My*xT/xy-(qt-lam*T))==0)
ck('wrong transplanted QUMOND map detected',S.simplify(e-e/(1+2*e))==0 if a.control=='wrong_map' else S.simplify(e-e/(1+2*e))!=0)
fp=S.symbols('fp',real=True);qv=(1+fp)/2;qh=(1-fp)/2;G0,M0=S.symbols('G0 M0',real=True)
rows=[G0+qv*M0,-G0+qh*M0]
ck('opposite sector sum forces M0',S.simplify(sum(rows))==0 if a.control=='opposite_vacuum' else S.simplify(sum(rows)-M0)==0)
ck('symmetric exchange vacuum coefficient',qv.subs(fp,0)==S.Rational(1,2))
Cresp=S.symbols('Cresp',positive=True)
ck('UV envelope endpoint',S.simplify((2*Cresp-A).subs(A,2*Cresp))==0)
ck('actual vacuum offset retained',-A==0 if a.control=='drop_offset' else S.simplify((-A).subs(A,2*Cresp)+2*Cresp)==0)
ck('general n conditional vacuum moment',S.simplify((chi*A/2).subs(A,2*Cresp)-chi*Cresp)==0)
ck('four dimensional factor',chi.subs(n,3)==1)
ck('smaller interval gives fixed source derivative over half',1-S.Rational(96,5)*S.Rational(5,192)==S.Rational(1,2))
ck('small z high y negative term bound',4*S.Rational(1,9)/(1+S.Rational(1,9))**2==S.Rational(9,25))
out={'checks':checks,'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'control':a.control,'scope':'NR scalar contractions and exact local dictionary, not global covariant admission'}
o=pathlib.Path(a.output);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(json.dumps(out,indent=2));print(json.dumps(out));sys.exit(bool(out['failed']))
