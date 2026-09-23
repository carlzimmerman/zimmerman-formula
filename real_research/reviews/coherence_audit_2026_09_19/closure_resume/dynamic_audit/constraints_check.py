from pathlib import Path
import json,sys
import sympy as s
out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
source=Path(__file__).resolve().parent.parents[1]/'frw_repair'/'run_verified'
d=json.loads((source/'equations.json').read_text());r=json.loads((source/'general_reduced.json').read_text())
E=[s.sympify(x) for x in d['ODE']];S={k:s.sympify(x) for k,x in d['S'].items()};t,k,a,Q,F0,F1,F2,c2,c14,KB,beta,xi,Lam=[S[x] for x in ('t','k','a','Q','F0','F1','F2','c2','c14','KB','beta','xi','Lam')]
ps,bs,fs,us=[s.sympify(x) for x in d['amps']];av,h,q,j,ep,xi0,k0,alpha,alphadot=[s.sympify(x) for x in r['vars']];l,b,f,u,ld,bd,fd,ud,fdd,udd=s.symbols('l b f u ld bd fd ud fdd udd')
cn=next(z for z in s.sympify(r['mass']).free_symbols if str(z)=='clock_c2');gc=1+s.Rational(3,2)*cn;hd=q*j/(4*gc)
fld={s.diff(fs,t,2):fdd,s.diff(us,t,2):udd,s.diff(ps,t):ld,s.diff(bs,t):bd,s.diff(fs,t):fd,s.diff(us,t):ud,ps:l,bs:b,fs:f,us:u}
bg={s.diff(a,t,2):av*(h*h+hd),s.diff(a,t):av*h,s.diff(Q,t):-3*ep*h,s.diff(F0,t):-3*ep*h*j,s.diff(F1,t):-3*h*j,s.diff(F2,t):-3*h*j/ep,a:av,Q:q,F0:ep*j,F1:j,F2:j/ep,c2:cn,c14:alpha,KB:s.Rational(1,5),beta:s.Rational(9,5)/(2-alpha),Lam:3*gc*h*h-(ep-q)*j/2}
E=[s.factor(z.subs(fld,simultaneous=True).subs(bg,simultaneous=True)) for z in E]
lapse=s.sympify(r['lapse']);shift=s.sympify(r['shift']);acc=(-s.sympify(r['mass']).inv()*s.sympify(r['rest'])).applyfunc(s.factor);state=s.Matrix([f,fd,u,ud])
def Dt(z):return av*h*s.diff(z,av)+hd*s.diff(z,h)-3*ep*h*s.diff(z,q)-3*h*j*s.diff(z,j)+alphadot*s.diff(z,alpha)+fd*s.diff(z,f)+ud*s.diff(z,u)+fdd*s.diff(z,fd)+udd*s.diff(z,ud)
residual=[s.factor(z.subs({l:lapse,b:shift,ld:Dt(lapse),bd:Dt(shift)},simultaneous=True).subs({fdd:(acc*state)[0],udd:(acc*state)[1]},simultaneous=True)) for z in E]
assert residual==[0,0,0,0]
# Mini-superspace Noether identity independently, before the exponential specialization.
A=s.Function('A')(t);phi=s.Function('phi')(t);N=s.Function('N')(t);FF=s.Function('F');Gc=s.symbols('Gc');LA=-6*Gc*A*s.diff(A,t)**2/N-N*A**3*(FF(s.diff(phi,t)/N)+2*Lam)
def EL(z):return s.diff(LA,z)-s.diff(s.diff(LA,s.diff(z,t)),t)
En=EL(N);Ea=EL(A);Ef=EL(phi)
ward=s.simplify(Ea*s.diff(A,t)+Ef*s.diff(phi,t)-N*s.diff(En,t))
assert ward==0
result={'all_four_original_EL_residuals_zero':True,'minisuperspace_time_reparametrization_Ward_identity_zero':True,'identity':'adot E_a + phidot E_phi - N d(E_N)/dt=0','scope':'Exact rational symbolic tests of the archived ADM equations and reduction; not an independent reconstruction of the full covariant action.'}
(out/'constraints_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
