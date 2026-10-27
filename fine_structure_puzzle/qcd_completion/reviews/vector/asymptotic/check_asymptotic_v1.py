#!/usr/bin/env python3
"""Independent asymptotic-channel and wall calculation from immutable Cartesian V."""
import argparse,json,time,sys
from pathlib import Path
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--operator',required=True);p.add_argument('--result',required=True);args=p.parse_args()
start=time.monotonic();d=json.loads(Path(args.operator).read_text())
t=s.symbols('t',positive=True);k,h,kp,hp=s.symbols('k h kp hp');c0=s.symbols('c0');loc={'t':t,'k':k,'h':h,'kp':kp,'hp':hp}
def mat(key):return s.Matrix([[s.sympify(q,locals=loc) for q in row] for row in d[key]])
G=mat('Gram');V=mat('V_raw');T=mat('Dirichlet_T');N=mat('normal_N')
Va=V.subs({k:0,kp:0,h:1-1/t,hp:1/t**2}).applyfunc(s.cancel)
P=Va.applyfunc(lambda q:s.limit(q,t,s.oo))
C=(t*t*(Va-P+2*P/t)).applyfunc(s.cancel)
assert all(s.cancel(v)==0 for v in P*P-P)
assert all(s.cancel(v)==0 for v in P*C-C*P)
assert all(s.cancel(v)==0 for v in G*P-(G*P).T)
assert all(s.cancel(v)==0 for v in G*C-(G*C).T)
charged=[];ceigs=[];neutral=[];neigs=[]
for eigen,mult,vecs in sorted(C.eigenvects(),key=lambda q:q[0]):
 for vec in vecs:
  for dst,proj,evs in [(charged,P,ceigs),(neutral,s.eye(10)-P,neigs)]:
   q=proj*vec
   for old in dst:q-=old*(old.T*G*q)[0]
   if all(s.simplify(v)==0 for v in q):continue
   q=q.applyfunc(s.simplify);q=s.simplify(q/s.sqrt((q.T*G*q)[0]))
   dst.append(q);evs.append(eigen)
E=s.Matrix.hstack(*charged);Z=s.Matrix.hstack(*neutral)
assert E.cols==6 and Z.cols==4
assert s.simplify(E.T*G*E)==s.eye(6)
assert s.simplify(Z.T*G*Z)==s.eye(4)
bcharged=[s.simplify(1-v/2) for v in ceigs]
# Neutral channel choices fixed by the independently known translation and Wronskian.
e=s.eye(10);v0=e[:,2];v2=e[:,3]-e[:,2]/3
vtr=-e[:,6]+e[:,8];vg=e[:,6]+2*e[:,8]
for v,ev in [(v0,0),(v2,6),(vtr,2),(vg,2)]:
 assert P*v==s.zeros(10,1) and C*v==ev*v
assert (vtr.T*G*vg)[0]==0
# Factor e^t/t from each of the six charged columns before the boundary determinant.
Yc=E*s.diag(*[1+b/t for b in bcharged])
Rc=E*s.diag(*[1+b/t-b/t**2 for b in bcharged]) # u'+u/t, divided by e^t/t
Yn=s.Matrix.hstack((t+c0)*v0,t*t*vg,t**3*v2,vtr/t)
Rn=Yn.diff(t)+Yn/t
F=(T*Yc).row_join(T*Yn).col_join((N*Rc).row_join(N*Rn))
det=s.factor(F.det())
lead=s.simplify(s.limit(det/t**4,t,s.oo))
nextc=s.simplify(s.limit(t*(det/t**4/lead-1),t,s.oo))
assert lead!=0
result={'P_mass':[[str(v) for v in row] for row in P.tolist()],'C_centrifugal':[[str(v) for v in row] for row in C.tolist()],'charged_C_eigenvalues':[str(v) for v in ceigs],'neutral_C_eigenvalues':[str(v) for v in neigs],'charged_growing_1_over_t':[str(v) for v in bcharged],'charged_trace_first_correction':str(sum(bcharged)),'charged_basis':[[str(v) for v in row] for row in E.tolist()],'neutral_basis':[[str(v) for v in row] for row in Z.tolist()],'scaled_wall_determinant':str(det),'scaled_wall_leading_constant':str(lead),'scaled_wall_t_power':4,'full_boundary_t_power':-2,'vector_ratio_t_power':-22,'first_relative_wall_correction':str(nextc),'c0_definition':'neutral L0 column (t+c0)*B2 after charged-growing amplitudes removed; other growing neutral columns t2*(B6+2B8),t3*(B3-B2/3), translation (-B6+B8)/t','hypotheses':['charged-growing connection rank6','neutral-growing quotient rank3 with one L2 kernel, proportional to translation','standard asymptotic basis with non-growing charged kernel admits neutral free-power expansions','any deduction c0=0 requires a separate regular gauge-gradient/scalar-positivity argument'],'runtime_seconds':time.monotonic()-start,'software':{'python':sys.version.split()[0],'sympy':s.__version__},'non_claims':['This local asymptotic matrix calculation does not establish global connection ranks','No finite-radius fit','No QCD or alpha conclusion']}
Path(args.result).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({key:result[key] for key in ['charged_C_eigenvalues','neutral_C_eigenvalues','charged_growing_1_over_t','charged_trace_first_correction','scaled_wall_leading_constant','scaled_wall_t_power','first_relative_wall_correction','runtime_seconds']},indent=2))

