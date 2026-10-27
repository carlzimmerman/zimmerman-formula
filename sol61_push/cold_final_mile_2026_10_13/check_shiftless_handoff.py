import json,sys
import sympy as s
q,r,L,Kc,mu=s.symbols('q r L Kc mu',positive=True);n=0
def ck(e):
 global n
 assert s.simplify(e)==0;n+=1
K=s.Matrix([[((4/r+6)*q+(6+9*r)*L)/(q-L),L*(3*r+2)/(q-L)],[L*(3*r+2)/(q-L),L*r/(q-L)]])
assert K.subs(L,0)==s.diag(4/r+6,0);n+=1
G=s.Matrix([[-2*q+4*q*q/(r*Kc)+6*r*mu,2*r*mu],[2*r*mu,2*r*mu]])
g=s.simplify(G[0,0]-G[0,1]**2/G[1,1]);ck(g-(-2*q+4*q*q/(r*Kc)+4*r*mu))
ck(g-(4/(r*Kc)*(q-r*Kc/4)**2+r*(4*mu-Kc/4)))
ck(g.subs(q,r*Kc/4)-r*(4*mu-Kc/4))
ck(g.subs({Kc:16*mu,q:4*r*mu}))
w=s.sqrt(g/(4/r+6));v=2*s.sqrt(q)*s.diff(w,q)
ck(s.limit(w/q,q,s.oo)-2/s.sqrt(Kc*(4+6*r)))
ck(s.limit(v/s.sqrt(q),q,s.oo)-4/s.sqrt(Kc*(4+6*r)))
kv=r*L/(q+2*r*L);wv=mu*q/L+2*r*mu
ck(s.limit(kv,L,0));ck(s.limit(kv*wv,L,0)-r*mu)
for kval,sign in [(1,1),(32,0),(64,-1)]:
 assert s.sign((r*(4*mu-Kc/4)).subs({r:1,mu:2,Kc:kval}))==sign;n+=1
json.dump(dict(checks=n,strict_all_q_positive_condition='Kc<16 mu',semidefinite_equality='Kc=16mu has zero at q=4 r mu',high_q_group_speed='4 sqrt(q)/sqrt(Kc(4+6r))',scope='Conditional given homogeneous reduced action; covariant construction, nonlinear constraints, interface and UV not certified'),open(sys.argv[1],'w'),indent=2)
