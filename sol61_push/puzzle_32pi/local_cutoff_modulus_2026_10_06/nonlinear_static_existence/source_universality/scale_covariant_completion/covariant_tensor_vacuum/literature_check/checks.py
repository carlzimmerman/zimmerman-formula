import argparse,json,pathlib,sys
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--control',default='none');a=p.parse_args();rows=[]
def ck(name,ok):rows.append({'name':name,'passed':bool(ok)})
pt,pz=s.symbols('pt pz',real=True);W=pz*pz-pt*pt
ck('temporal coefficient exact from sqrtW',s.simplify(s.diff(-pt*s.sqrt(W),pt)+(pz*pz-2*pt*pt)/s.sqrt(W))==0)
coeff=pz*pz-2*pt*pt
ck('correct temporal singularity',coeff.subs(pz*pz,pt*pt/2)==0 if a.control=='wrong_singularity' else coeff.subs(pz*pz,2*pt*pt)==0)
t,z=s.symbols('t z',real=True);u=s.sin(t-z)+s.sin(t+z);ut=s.diff(u,t);uz=s.diff(u,z)
R=-(uz*uz-2*ut*ut)*s.diff(u,t,2)-2*ut*uz*s.diff(u,t,z)+(2*uz*uz-ut*ut)*s.diff(u,z,2)
point={t:s.pi/4,z:s.pi/3};res=s.simplify(R.subs(point))
ck('superposition interior hyperbolic Wpositive',s.simplify((uz*uz-ut*ut).subs(point))==1)
ck('opposite superposition actual residual',res==0 if a.control=='linear_superposition' else res==-5/s.sqrt(2))
K=s.symbols('K',positive=True);m=s.symbols('m',real=True);det=s.det(s.diag(K/2,K*(1-2*m)/8)).subs(m,s.Rational(1,2))
ck('critical block not positive definite PF',det>0 if a.control=='apply_PF_theorem' else det==0)
ck('mean tensor still positive',K/2>0)
result={'checks':rows,'passed':sum(r['passed'] for r in rows),'failed':sum(not r['passed'] for r in rows),'control':a.control,'scope':'local source-equation algebra, not paper theorem or numerical propagation certification'}
o=pathlib.Path(a.output);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(json.dumps(result,indent=2));print(json.dumps(result));sys.exit(bool(result['failed']))
