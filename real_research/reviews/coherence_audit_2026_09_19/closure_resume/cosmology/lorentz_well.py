"""Exact quadratic modification F(Q) -> F(sqrt(Q^2-Y)).

The homogeneous solution and linear canonical momentum are unchanged.
The added quadratic density is a F_Q/(2Q) (P_x)^2. This changes the static
MOND cancellation when F_Q is nonzero; it is not an automatic full repair.
"""
from pathlib import Path
import json
import sympy as s

here=Path(__file__).resolve().parent
d=json.loads((here/'canonical.json').read_text())
old=json.loads((here.parents[1]/'frw_repair/run_verified/general_reduced.json').read_text())
var=[s.sympify(z) for z in d['variables']]
a,h,q,j,ep,xi,k,alpha,ad,b=var
M=s.sympify(old['mass'])
T=s.sympify(d['old_cosmic_to_new_cosmic']);Ti=T.inv().applyfunc(s.factor)
deltaR=s.zeros(2,4);deltaR[1,2]=a*j*k*k/q
deltaAcc=(-M.inv()*deltaR).applyfunc(s.factor)
deltaA=s.zeros(4);deltaA[1,:]=deltaAcc[0,:];deltaA[3,:]=deltaAcc[1,:]
f,fd,u,ud=s.symbols('f fd u ud')
shift=s.sympify(old['shift'])
deltaPsi=(a*s.Matrix([shift]).jacobian([f,fd,u,ud])*deltaA).applyfunc(s.factor)
assert deltaPsi==s.zeros(1,4)
scale=s.diag(1,h,1,1)
deltaN=(scale.inv()*T*deltaA*Ti*scale/h).applyfunc(s.factor)
new=(s.sympify(d['matrix_N'])+deltaN).applyfunc(s.factor)
obs=s.sympify(d['observables'])
# Bardeen Phi uses positions and the shift only, hence is unchanged. The
# trace-free spatial equation also keeps Psi=Phi at this linear order.
d['matrix_N']=s.srepr(new)
d['eps_zero_matrix_N']=s.srepr(new.applyfunc(lambda z:s.factor(s.limit(z,ep,0,dir='+'))))
d['modification']='F(sqrt(Q^2-Y)), timelike scalar gradient Q>0'
d['observable_scope']='Phi_N, density and clock observables unchanged; Psi_N equality follows from unchanged traceless metric equation, not reused acceleration formula.'
(here/'lorentz_canonical.json').write_text(json.dumps(d,indent=1)+'\n')
print('Lorentz-well phase equations built.',flush=True)
print('Changed canonical matrix entries:',sum(1 for z in deltaN if z!=0),flush=True)
print('Bardeen Psi=Phi reconstruction remains exact.',flush=True)
