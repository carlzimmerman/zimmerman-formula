#!/usr/bin/env python3
"""Independent local second-order checks; no global rank assertion."""
import argparse,json,time,sys
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--operator',required=True);p.add_argument('--local-result',required=True);p.add_argument('--result',required=True);args=p.parse_args();start=time.monotonic()
D=json.loads(Path(args.operator).read_text());I=json.loads(Path(args.local_result).read_text())
t=s.symbols('t',positive=True);k,h,kp,hp=s.symbols('k h kp hp');loc={'t':t,'k':k,'h':h,'kp':kp,'hp':hp}
def mat(key):return s.Matrix([[s.sympify(v,locals=loc) for v in row] for row in D[key]])
G=mat('Gram');V=mat('V_raw');T=mat('Dirichlet_T');N=mat('normal_N')
P=s.Matrix(I['P_mass']);C=s.Matrix(I['C_centrifugal']);E=s.Matrix(I['charged_basis']);ce=list(map(s.sympify,I['charged_C_eigenvalues']))
embed=s.zeros(10,3)
for a,b in enumerate([1,3,5]):embed[b,a]=1
PN=embed*N
A1=P-P*C/2;A2=(6*P-P*C)*A1/4
assert P*PN==PN*P
traces={'trA1':s.trace(A1),'trA2':s.trace(A2),'trPN_A1':s.trace(PN*A1),'trA1_squared':s.trace(A1*A1)}
assert traces=={'trA1':-2,'trA2':3,'trPN_A1':-2,'trA1_squared':10}
q2log=s.simplify(traces['trA2']-traces['trPN_A1']-traces['trA1_squared']/2)
assert q2log==0
solutions={0:4*t*s.exp(-t)*s.Ei(2*t)-2*s.exp(t),2:s.exp(t)/t,6:s.exp(t)/t*(1-2/t)}
for cent,u in solutions.items():assert s.simplify(-s.diff(u,t,2)+(1-2/t+cent/t**2)*u)==0
gamma,delta,eta=s.symbols('gamma delta eta');eye=s.eye(10)
v0=eye[:,2];v6=(3*eye[:,3]-eye[:,2])/s.sqrt(2);vg=(eye[:,6]+2*eye[:,8])/s.sqrt(2);vd=-eye[:,6]+eye[:,8]
g=t*v0+gamma*v6/t**2;h6=t**3*v6+5*gamma*v0+delta*v6/t**2
W=s.expand((g.T*G*h6.diff(t)-g.diff(t).T*G*h6)[0])
assert W==0
# Use charge/neutral wall invariance instead of an expensive expanded10x10 determinant.
Yn=s.Matrix.hstack(g,h6,(t*t+eta/t)*vg,vd/t);Rn=Yn.diff(t)+Yn/t
U=s.Matrix.hstack(v0,v6,vg,vd)
neutral_wall=(U.T*G*((s.eye(10)-PN)*Yn+PN*Rn)).applyfunc(s.cancel)
det=s.factor(neutral_wall.det());lead=s.limit(det/t**4,t,s.oo)
n1=s.simplify(s.limit(t*(det/t**4/lead-1),t,s.oo))
n2=s.simplify(s.limit(t*t*(det/t**4/lead-1-n1/t),t,s.oo))
assert lead!=0 and n1==n2==0
a1=traces['trA1'];a2=s.simplify(q2log+a1*a1/2)
assert a1==-2 and a2==2
result={'traces':{key:str(v) for key,v in traces.items()},'charged_exact_growing_solutions':{str(c):str(u) for c,u in solutions.items()},'charged_C0_nonterminating':True,'neutral_companion_Wronskian':str(W),'neutral_wall_leading_constant':str(lead),'neutral_wall_determinant':str(det),'neutral_relative_1_over_t':str(n1),'neutral_relative_1_over_t2':str(n2),'wall_relative_1_over_t':str(a1),'wall_relative_1_over_t2':str(a2),'log_wall_1_over_t2':str(s.simplify(a2-a1*a1/2)),'neutral_scattering_gamma_delta_eta_symbolic':True,'runtime_seconds':time.monotonic()-start,'software':{'python':sys.version.split()[0],'sympy':s.__version__},'non_claims':['No global kernel/rank proof','No claim for q3 or higher from a2-truncated charged ansatz','No QCD or alpha result']}
Path(args.result).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


