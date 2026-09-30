import argparse
import itertools
import json
import sympy as s

I=s.eye(2)
x=s.Matrix([[0,1],[1,0]])
y=s.Matrix([[0,-s.I],[s.I,0]])
z=s.diag(1,-1)
pauli=[I,x,y,z]
names=['0','x','y','z']
K=s.kronecker_product
T=K(I,y,y)
C=K(x,y,y)
P=K(x,I,I)
gx,gy=K(z,x,I),K(z,y,I)
mass=[K(z,z,a) for a in (x,y,z)]
def anti(U,A): return U*A.conjugate()*U.H
def parity(A): return P*A*P.H
checks=[]
def check(name,ok): checks.append({'name':name,'passed':bool(ok)})
check('T squared', T*T.conjugate()==s.eye(8))
check('C squared', C*C.conjugate()==s.eye(8))
check('P squared', P*P==s.eye(8))
check('T kinetic odd polarization even',all(anti(T,A)==-A for A in (gx,gy)) and all(anti(T,A)==A for A in mass))
check('C kinetic even polarization odd',all(anti(C,A)==A for A in (gx,gy)) and all(anti(C,A)==-A for A in mass))
check('P kinetic and polarization odd',all(parity(A)==-A for A in [gx,gy]+mass))
allowed_tc=[]
allowed_tcp=[]
scalar_tc=[]
diagonal=True
generators=[K(I,I,a) for a in (x,y,z)]
for indices in itertools.product(range(4),repeat=3):
    A=K(*(pauli[i] for i in indices))
    label=''.join(names[i] for i in indices)
    images=[anti(T,A),anti(C,A),parity(A)]
    diagonal &= all(B==A or B==-A for B in images)
    if images[0]==A and images[1]==-A:
        allowed_tc.append(label)
        if all(A*J==J*A for J in generators): scalar_tc.append(label)
        if images[2]==A: allowed_tcp.append(label)
check('all symmetry operations diagonal in complete Hermitian basis',diagonal)
check('T C P forbid all homogeneous constant perturbations',len(allowed_tcp)==0)
check('opposite cone offsets survive T C and flavor rotations','z00' in scalar_tc)
check('parity excludes opposite offsets',parity(K(z,I,I))==-K(z,I,I))

d,m,v=s.symbols('delta m v',positive=True)
single=-2*d**3/(12*s.pi*v*v)+2*d*m*m/(4*s.pi*v*v)
electron_density=2*(d*d-m*m)/(4*s.pi*v*v)
hole_density=-electron_density
check('compensated pockets have zero total charge',s.simplify(electron_density+hole_density)==0)
check('compensated pockets retain finite quadratic stiffness',s.diff(2*single,m,2)==2*d/(s.pi*v*v))
check('compensated pockets have no cubic below offset',s.diff(2*single,m,3)==0)
parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
result={'passed':all(c['passed'] for c in checks),'checks':checks,'T_C_allowed_basis':allowed_tc,'T_C_flavor_scalar_basis':scalar_tc,'T_C_P_allowed_basis':allowed_tcp}
with open(args.output,'w') as f: json.dump(result,f,indent=2)
print(json.dumps(result))
raise SystemExit(0 if result['passed'] else 1)
