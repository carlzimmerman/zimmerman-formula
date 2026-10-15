import json,sys
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def zero(n,v):
 assert s.simplify(v)==0,(n,s.simplify(v));checks.append(n)
q=s.symbols('q',positive=True);Z,E,zd,ed,alpha,b,Y,yd=s.symbols('Z E zd ed alpha b Y yd',real=True)
lag=-3*zd**2-2*zd*ed+2*zd*b+q*Z**2+2*q*alpha*Z+(3*zd+ed-b)**2/2+(1+q)*alpha**2/2+2*b*b/q-2*(3*Z*Z+2*Z*E+E*E)
asol=s.solve(s.diff(lag,alpha),alpha)[0];bs=s.solve(s.diff(lag,b),b)[0]
zero('lapse',asol+2*q*Z/(1+q));zero('shift',bs-q*(zd+ed)/(q+4))
red=s.factor(lag.subs({alpha:asol,b:bs}));K=s.hessian(red,(zd,ed));G=-s.hessian(red,(Z,E))
f=q+2+2/(q+1);expected=zd**2+2*yd**2/(q+4)-f*Z**2-2*Y**2
zero('diagonal exact action',red.subs({E:Y-Z,ed:yd-zd})-expected)
zero('kinetic determinant',K.det()-8/(q+4));zero('potential determinant',G.det()-8*f)
zero('f derivative',s.diff(f,q)-(1-2/(q+1)**2))
zero('f positive gap',f-q-2-2/(q+1))
# Forq>0:0<2/(q+1)²<2 =>-1<f'<1; vg²=q f'²/f<q/(q+2)<1.
for name,ff,cs2 in [('Y',q+4,1),('vector',q/2+4,s.Rational(1,2)),('tensor',q+4,1)]:
 zero(name+' speed deficit',cs2-q*s.diff(ff,q)**2/ff-4*cs2/ff)
rows=[]
for qq in (s.Rational(1,10**6),s.Rational(1,2),1,10,100,10000):
 kp=K.subs(q,qq);gp=G.subs(q,qq);vg=s.sqrt(q)*s.diff(f,q)/s.sqrt(f)
 for name,v in [('K11',kp[0,0]),('detK',kp.det()),('G11',gp[0,0]),('detG',gp.det())]:
  assert v>0;checks.append(str(qq)+' '+name)
 assert abs(vg.subs(q,qq))<1;checks.append(str(qq)+' speed')
 rows.append({'q':str(qq),'clock_frequency2':float(f.subs(q,qq)),'clock_group_speed_c':float(vg.subs(q,qq))})
result={'claim':'CGR-007','checks_passed':len(checks),'selected_coefficients':{'r':1,'Kc':1,'L':4,'mu':2,'A':1},'scalar_action':str(expected),'clock_frequency2':str(f),'other_scalar_frequency2':'q+4','vector_frequency2':'q/2+4','tensor_frequency2':'q+4','all_q':'positive full reduced exterior energy and allpropagating group speeds<c forq>0','minimum_phase_speed_c':'1/sqrt2, vector branch asymptote; not a generalwall guarantee','samples':rows,'limits':'No finite3Dwall, nonlinear/causal/empirical/engine certificate.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(result,indent=2))
