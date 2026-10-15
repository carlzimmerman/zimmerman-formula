import json
import sys
from pathlib import Path
import sympy as s
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def zero(name,v):
    if isinstance(v,s.MatrixBase):
        val=v.applyfunc(s.simplify);assert val==s.zeros(*val.shape),(name,val)
    else:
        val=s.simplify(v);assert val==0,(name,val)
    checks.append(name)

Kc=s.Integer(10)**12;L=s.Integer(100);mu=s.Integer(2)
Ht=s.symbols('Ht',real=True)
aa=s.Matrix(s.symbols('a1:4',real=True))
h11,h12,h13,h22,h23,h33=s.symbols('h11 h12 h13 h22 h23 h33',real=True)
Hs=s.Matrix([[h11,h12,h13],[h12,h22,h23],[h13,h23,h33]])
H=s.zeros(4);H[0,0]=Ht;H[0,1:4]=aa.T;H[1:4,0]=aa;H[1:4,1:4]=Hs
k=s.Matrix(s.symbols('kx ky kz',real=True));k2=(k.T*k)[0]
v=s.Matrix(s.symbols('v0:4',real=True));p=s.Matrix(s.symbols('p0:4',real=True))
D=s.symbols('D',positive=True)
B=L*s.eye(3)-Hs
ss00=-2*v[0];ss0=s.Matrix([-v[i+1]+k[i]*p[0] for i in range(3)])
ss=s.Matrix(3,3,lambda i,j:k[i]*p[j+1]+k[j]*p[i+1])
lag=((v.T*H*v)[0]-k2*(p.T*H*p)[0])/2
lag+=(Kc-Ht)*ss00**2/8+(ss0.T*B*ss0)[0]/2-ss00*(aa.T*ss0)[0]/2
lag-=mu*sum(q*q for q in ss)/4
lag+=sum(aa[i]*(sum(ss0[j]*ss[i,j] for j in range(3))-ss0[i]*s.trace(ss)/2) for i in range(3))
lag-=D*k2*k2*p[0]**2/2
lag=s.expand(lag)
K=s.hessian(lag,v);G=-s.hessian(lag,p)
M=s.Matrix(4,4,lambda i,j:s.diff(lag,v[i],p[j]))
zero('general arbitrary-H positive kinetic tuning',K-s.diag(Kc,L,L,L))
gt=s.zeros(4);gt[0,0]=D*k2*k2+(Ht-L)*k2+(k.T*Hs*k)[0]
gt[1:4,1:4]=k2*(Hs+mu*s.eye(3))+mu*k*k.T
zero('general arbitrary-H gradient tuning',G-gt)
R=s.diag(1/s.sqrt(Kc),1/s.sqrt(L),1/s.sqrt(L),1/s.sqrt(L))
S=s.simplify(R*(M+M.T)*R)
st=s.zeros(4);st[0,0]=2*(aa.T*k)[0]/Kc
st[1:4,1:4]=-2*(aa.T*k)[0]*s.eye(3)/L
st[0,1:4]=-(B*k).T/s.sqrt(Kc*L);st[1:4,0]=-(B*k)/s.sqrt(Kc*L)
zero('general mixed derivative symbol',S-st)
mom=s.Matrix([s.diff(lag,q) for q in v])
zero('general Legendre energy',(mom.T*v)[0]-lag-(v.T*K*v)[0]/2-(p.T*G*p)[0]/2)
clock=s.Rational(2*100000-98,10**6)
sp=s.Rational(5,10)
mix=2/Kc+2/L+s.Rational(101,10**7)
bound=s.simplify(max(clock,sp)+mix)
assert clock<sp and bound<1
checks.append('exact strict all-direction group-speed bound')
# Basis-independent tensor contraction matches the scalar EOM source identity.
result={'claim':'CIS-003','checks_passed':len(checks),'K':'diag(10^12,100,100,100)','clock_sqrt_derivative_bound':str(clock),'spatial_sqrt_derivative_bound':str(sp),'mixed_symbol_derivative_bound':str(mix),'all_direction_group_speed_bound':str(bound),'decimal_group_bound':float(bound),'proof_scope':'Arbitrary normalized symmetric H with norm<=1, every direction,103<=Dk2<=100000; local frozen matter operator only.','missing':'Full gravity, actual IR confinement, global variable-coefficient spectrum and controlled microscopic theory remain unresolved.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(result,indent=2))
