import sympy as S
import json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[3]
inputs=['ac2q_postfold_2026_11_06/coupled/JUNCTION_RESULT.md',
        'ac2q_postfold_2026_11_06/DERIVATION.md',
        'action_search_2026_11_05/AC7_charge_switch/README.md']
hashes={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in inputs}
v,ell,T,a,b,s,g,A,z,W,V=S.symbols('v ell T alpha beta s gamma A z W V',real=True)
C=1/S.sqrt(1-v*v);E=S.exp(2*a+2*b);J=S.exp(a+2*b)*A
B=S.exp(-2*a)*s*s*(1-v*v);D=S.exp(-a)*C*(ell+v*T)
F=lambda d:-d+B/2-W-V-g*d*d/2-g*d*B
L=E*F(D)
piP=S.diff(L,ell)
dv=S.exp(-a)*C**3*(v*ell+T)
checks={}
checks['D_v']=S.simplify(S.diff(D,v)-dv)==0
checks['piP']=S.simplify(piP+S.exp(a+2*b)*C*(1+g*(D+B)))==0
piX=-S.diff(L,v)/s
manual=E*(1+g*(D+B))*dv/s+S.exp(2*b)*s*v*(1-2*g*D)
checks['scalar_normal']=S.simplify(piX-manual)==0
piT=S.diff(L,s)-v*S.diff(L,v)/s
manualT=E*(1+g*(D+B))*v*dv/s+S.exp(2*b)*s*(1-2*g*D)
checks['scalar_temporal']=S.simplify(piT-manualT)==0
ell_z=S.exp(a)*z/C-v*T
fz=E*F(z)+J*ell_z
f0z=E*(F(z)+A*z/C)
checks['linear_transform']=S.simplify(fz-f0z+J*v*T)==0
checks['third_derivative_unchanged']=S.simplify(S.diff(fz-f0z,v,3))==0
checks['normal_stress_linear_cancellation']=S.simplify(v*S.diff(fz-f0z,v)-(fz-f0z))==0
checks['scalar_flux_equal_shift']=S.simplify(-S.diff(fz-f0z,v)/s-J*T/s)==0
out={'base':'e50f32a0a7','input_sha256':hashes,'checks':checks,'all_pass':all(checks.values()),
     'scope':'Exact algebra only; regularity and distributional assertions audited in REVIEW.md.'}
print(json.dumps(out,indent=2))
