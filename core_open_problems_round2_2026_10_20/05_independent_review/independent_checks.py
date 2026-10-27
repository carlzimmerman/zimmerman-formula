"""Exact independent identities; no imported author checks and no sampled modes."""
import json, platform, sys
from pathlib import Path
import sympy as s
checks=[]
def zero(name, expression):
    value=s.simplify(expression)
    assert value==0, (name,value)
    checks.append(name)
K,b,e,g,H,p=s.symbols('K beta eta gamma H p', positive=True)
z,n,v,Y,sg,w,Z=s.symbols('z n v Y sigma w Z', real=True)
A=2+3*b; C=A/(K*b); B=C*K*K
# Direct averaged ADM expansion, including cosmological term and weighted IBP.
adm=-3*A*v*v+2*A*v*Y-b*Y*Y-6*A*H*Y*z+(3*z-n)*(-6*A*H*v+2*A*H*Y)-3*A*H*H*(s.Rational(9,2)*z*z-3*z*n+n*n)
cosmo=-3*A*H*H*(s.Rational(9,2)*z*z+3*z*n)
weighted_ibp=18*A*H*z*v+27*A*H*H*z*z
expected=-3*A*(v-H*n)**2+2*A*(v-H*n)*Y-b*Y*Y
zero('direct ADM expansion after weighted integration',adm+cosmo+weighted_ibp-expected)
L=expected/(4*K)+p*p*z*z/(2*K)+p*p*n*z/K+p*p*n*sg+e*p*p*w*w/2-K*p*p*sg*sg/2-g*p**4*sg*sg/2
L1=s.expand(L.subs(Y,A*(v-H*n)/b))
zero('shift Schur complement',L1-(C*(v-H*n)**2/2+p*p*z*z/(2*K)+p*p*n*(z/K+sg)+e*p*p*w*w/2-K*p*p*sg*sg/2-g*p**4*sg*sg/2))
L2=L1.subs(n,v/H-p*p*(z/K+sg)/(C*H*H))
zero('lapse Schur complement',L2-(e*p*p*w*w/2+p*p*(z/K+sg)*v/H+p*p*z*z/(2*K)-K*p*p*sg*sg/2-g*p**4*sg*sg/2-p**4*(z/K+sg)**2/(2*C*H*H)))
Zd=s.symbols('Zdot')
L3=s.expand(L2.subs({z:K*(Z-sg),v:K*(Zd-w)}))
L3=L3-K*p*p*Z*Zd/H-K*p*p*Z*Z/2
aux=e*p*p*w*w/2-K*p*p*Z*(w+H*sg)/H-g*p**4*sg*sg/2-p**4*Z*Z/(2*C*H*H)
zero('a^3 p^2 integration weight',L3-aux)
L4=aux.subs(Z,-C*K*H*(w+H*sg)/p**2)
zero('auxiliary elimination',L4-(e*p*p*w*w+B*(w+H*sg)**2-g*p**4*sg*sg)/2)
Q=B+e*p*p; V=g*p**4+2*B*H*H
acc=-H*(3*B+e*p*p)*w/Q-V*sg/Q
energy=(Q*w*w+V*sg*sg)/2
Edot=s.diff(energy,p)*(-H*p)+s.diff(energy,sg)*w+s.diff(energy,w)*acc
zero('exact energy dissipation',Edot+H*(3*B+2*e*p*p)*w*w+2*H*g*p**4*sg*sg)
# Frobenius recurrence through power 10, for both indicial roots.
series_records={}
for m in [1,2]:
    coeff={0:s.Integer(1)}
    for j in range(1,11):
        denom=B*(m+j-1)*(m+j-2)
        source=e*(m+j-2)*(m+j-3)*coeff.get(j-2,0)+g/H**2*coeff.get(j-4,0)
        if denom==0:
            zero('resonance compatibility m=1 j=1',source); coeff[j]=s.Integer(0)
        else: coeff[j]=s.factor(-source/denom)
    f=sum(coeff[j]*p**(m+j) for j in coeff)
    residual=s.expand((B+e*p*p)*p*p*s.diff(f,p,2)-2*B*p*s.diff(f,p)+(2*B+g*p**4/H**2)*f)
    for degree in range(m,m+11):zero(f'Frobenius m={m} degree={degree}',residual.coeff(p,degree))
    series_records[str(m)]={str(j):str(coeff[j]) for j in [0,1,2,3,4]}
    recon=-B*H*(-H*p*s.diff(f,p)+H*f)/p**2-K*f
    zero(f'finite future metric limit m={m}',s.limit(recon,p,0)-(0 if m==1 else B*H*H))
# Derivative mixing evaluated on a general TT matrix for k parallel z.
a,c,PL,PX,PY,ik=s.symbols('a c PL PX PY ik')
TT=s.Matrix([[a,c,0],[c,-a,0],[0,0,0]])
P=s.Matrix([PX,PY,PL]); wave=s.Matrix([0,0,ik])
zero('TT contribution to divergence d',-(wave.T*TT*P)[0]+s.trace(TT)*(wave.T*P)[0]/2)
zero('TT contribution to lapse coupling',(wave.T*TT*P)[0])
# Order (L,T1,T2) in shift Hessian.
P=s.Matrix([PL,PX,PY]); S=s.diag(-b/(2*K),1/(4*K),1/(4*K))
D=1+(e*P.T*S.inv()*P)[0]; M=S+e*P*P.T
zero('full 3 by 3 shift determinant',M.det()-S.det()*D)
qd=s.symbols('qd'); yy=e*S.inv()*P*qd/D
for j in range(3):zero(f'full shift equation component {j}',(M*yy-e*P*qd)[j])
zero('full shift kinetic reduction',e*(qd-(P.T*yy)[0])**2/2+(yy.T*S*yy)[0]/2-e*qd*qd/(2*D))
r,ang=s.symbols('r ang',real=True)
zero('angular expression',D.subs({PL:r*s.cos(ang),PX:r*s.sin(ang),PY:0})-(1-2*K*e*r*r/b+(1+2*b)*2*K*e*r*r*s.sin(ang)**2/b))
result={'status':'passed','identity_count':len(checks),'checks':checks,'frobenius_coefficients':series_records,'range':'symbolic identities over real parameters where displayed denominators are nonzero; Frobenius coefficients j=0..10 for m=1,2; no numerical sampling','python':platform.python_version(),'sympy':s.__version__}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'identity_count':len(checks)}))
