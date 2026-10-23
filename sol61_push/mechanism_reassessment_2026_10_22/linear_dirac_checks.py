"""Direct finite-mode Dirac algorithm for A68's unreduced scalar quadratic action."""
import sympy as s
import json,sys
from pathlib import Path
K,eta,beta,gamma,k=s.symbols('K eta beta gamma k',positive=True)
z,sig,n,pz,ps,pn=s.symbols('z sigma n pz ps pn',real=True)
a=(2+3*beta)/(K*beta); b=eta*k*k
qs=[z,sig,n]; psym=[pz,ps,pn]
def PB(f,g):return s.expand(sum(s.diff(f,q)*s.diff(g,p)-s.diff(f,p)*s.diff(g,q) for q,p in zip(qs,psym)))
H0=pz*pz/(2*a)+ps*ps/(2*b)-k*k*z*z/(2*K)+(K*k*k+gamma*k**4)*sig*sig/2
C=k*k*(z/K+sig)
D=s.factor(PB(C,H0))
S=s.factor(PB(C,D))
E=s.factor(PB(D,H0))
F=E+n*S
cs=[pn,C,D,F]
mat=s.Matrix([[PB(f,g) for g in cs]for f in cs])
det=s.factor(mat.det())
H=H0-n*C
checks={'primary_generates_C':s.simplify(PB(pn,H)-C)==0,
 'C_generates_D':s.simplify(PB(C,H)-D)==0,
 'D_generates_lapse_fix':s.simplify(PB(D,H)-F)==0,
 'second_class_determinant':s.simplify(det-S**4)==0,
 'nonzero_pair':s.simplify(S-k**4*(1/(K*K*a)+1/b))==0}
# Pull back the canonical one-form: p_reduced = ps - K pz.
pr=s.symbols('p_reduced',real=True)
sol=s.solve([D,pr-(ps-K*pz)],[pz,ps],dict=True)[0]
Hr=s.factor(H0.subs(z,-K*sig).subs(sol))
Q=K*(2+3*beta)/beta+eta*k*k
expected=pr*pr/(2*Q)+gamma*k**4*sig*sig/2
checks['canonical_reduced_H']=s.simplify(Hr-expected)==0
checks['positive_S']=S.is_positive is True
checks['positive_Q']=Q.is_positive is True
checks['scalar_DOF']=(6-4)//2==1
result={'checks':checks,'all_pass':all(checks.values()),'C':str(C),'D':str(D),'S':str(S),'E':str(E),'dirac_determinant':str(det),'reduced_H':str(Hr),'omega_squared':str(gamma*k**4/Q),'scope':'flat vacuum, nonzero Fourier k, beta eta gamma K positive; nonlinear count not established'}
p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(result,indent=2)+'\n')
for key,ok in checks.items():print(key,'PASS' if ok else 'FAIL')
print('COMPLETE',sum(checks.values()),'/',len(checks))
sys.exit(0 if all(checks.values()) else 1)
