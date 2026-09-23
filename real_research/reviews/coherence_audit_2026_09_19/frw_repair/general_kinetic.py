"""Exact constraint reduction on the candidate's own exponential-wall FRW.
No comparison cosmology, no frozen-Q approximation, no adiabatic deletion.
"""
from pathlib import Path
import json,time
import sympy as s
import mpmath as mp

start=time.time(); here=Path(__file__).resolve().parent
d=json.loads((here/'run_adm/equations.json').read_text())
E=[s.sympify(x) for x in d['ODE']];S={k:s.sympify(x) for k,x in d['S'].items()}
t,k,a,Q,F0,F1,F2,c2,c14,KB,beta,xi,Lam=[S[x] for x in ('t','k','a','Q','F0','F1','F2','c2','c14','KB','beta','xi','Lam')]
amps=[s.sympify(x) for x in d['amps']]
ps,bs,fs,us=amps
l,b,f,u,ld,bd,fd,ud,fdd,udd=s.symbols('l b f u ld bd fd ud fdd udd')
av,h,q,j,ep=s.symbols('av H q j ep',nonzero=True,real=True)
cn,cnd=s.symbols('clock_alpha clock_alpha_dot',real=True); c2n=s.symbols('clock_c2',positive=True); kb=s.Rational(1,5)
gc=1+s.Rational(3,2)*c2n
hd=q*j/(4*gc); qd=-3*ep*h; jd=-3*h*j
bg={s.diff(a,t,2):av*(h*h+hd),s.diff(a,t):av*h,
    s.diff(Q,t):qd,s.diff(F0,t):ep*jd,s.diff(F1,t):jd,s.diff(F2,t):jd/ep,
    a:av,Q:q,F0:ep*j,F1:j,F2:j/ep,c2:c2n,c14:cn,KB:kb,beta:(2-kb)/(2-cn),
    Lam:3*gc*h*h-(ep-q)*j/2}
fld={s.diff(fs,t,2):fdd,s.diff(us,t,2):udd,
     s.diff(ps,t):ld,s.diff(bs,t):bd,s.diff(fs,t):fd,s.diff(us,t):ud,
     ps:l,bs:b,fs:f,us:u}
E=[s.factor(z.subs(fld,simultaneous=True).subs(bg,simultaneous=True)) for z in E]
constraints,rhs=s.linear_eq_to_matrix(E[:2],[l,b])
sol=constraints.inv()*rhs
ls,bs0=[s.factor(z) for z in sol]
print('Constraints solved exactly.',round(time.time()-start,3),flush=True)
state=[f,fd,u,ud]
def Dt(z):
    return (s.diff(z,av)*av*h+s.diff(z,h)*hd+s.diff(z,q)*qd+s.diff(z,j)*jd+s.diff(z,cn)*cnd+
            s.diff(z,f)*fd+s.diff(z,fd)*fdd+s.diff(z,u)*ud+s.diff(z,ud)*udd)
dyn=[s.factor(z.subs({ld:Dt(ls),bd:Dt(bs0),l:ls,b:bs0},simultaneous=True)) for z in E[2:]]
mass=s.Matrix(dyn).jacobian([fdd,udd]).applyfunc(s.factor)
rest=s.Matrix(dyn).jacobian(state).applyfunc(s.factor)
assert all(s.factor(x)==0 for x in s.Matrix(dyn)-mass*s.Matrix([fdd,udd])-rest*s.Matrix(state))
assert s.factor(mass[0,1]-mass[1,0])==0
print('Reduced second-order system: 2 fields, symmetric kinetic matrix.',round(time.time()-start,3),flush=True)
print('kinetic entries',[-s.factor(mass[0,0]),-s.factor(mass[0,1]),-s.factor(mass[1,1])],flush=True)
print('det kinetic =',s.factor(mass.det()),flush=True)
record={'mass':s.srepr(mass),'rest':s.srepr(rest),'lapse':s.srepr(ls),'shift':s.srepr(bs0),
        'vars':[s.srepr(z) for z in (av,h,q,j,ep,xi,k,cn,cnd)],'Gc':str(gc),'constraint_det':str(s.factor(constraints.det()))}
(here/'run_general/reduced.json').write_text(json.dumps(record,indent=1))

