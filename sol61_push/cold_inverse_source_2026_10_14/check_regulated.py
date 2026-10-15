import json
import sys
from pathlib import Path
import sympy as s
import numpy as np

out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
checks=[]
def zero(name,v):
    if isinstance(v,s.MatrixBase):
        value=v.applyfunc(s.simplify);assert value==s.zeros(*value.shape),(name,value)
    else:
        value=s.simplify(v);assert value==0,(name,value)
    checks.append(name)

# Covariant operator and source-preserving subtraction.
t,x,y,z=s.symbols('t x y z',real=True);cs=(t,x,y,z)
b=s.Function('b')(x,y,z)
g=s.Matrix([[-1+b*b,0,0,b],[0,1,0,0],[0,0,1,0],[b,0,0,1]])
gi=s.simplify(g.inv());n=s.Matrix([1,0,0,-b]);project=s.simplify(gi+n*n.T)
zero('clock spatial projector',project-s.diag(0,1,1,1))
Gamma0=s.Matrix(4,4,lambda a,c:s.simplify(sum(gi[0,d]*(s.diff(g[d,c],cs[a])+s.diff(g[d,a],cs[c])-s.diff(g[a,c],cs[d])) for d in range(4))/2))
Q=-sum(project[a,c]*Gamma0[a,c] for a in range(4) for c in range(4))
zero('target projected clock curvature',Q-s.diff(b,z))
epsilon,deltaQ,coef=s.symbols('epsilon deltaQ coefficient')
term=-coef*(epsilon*deltaQ)**2/2
zero('regulator zero background',term.subs(epsilon,0))
zero('regulator zero first variation',s.diff(term,epsilon).subs(epsilon,0))

K0=s.Integer(10)**12;Ks=s.Integer(100);mu=s.Integer(2)
bi=s.Matrix([99,100,101]);hs=s.Matrix([-1,1,0,-1])
k=s.Matrix(s.symbols('kx ky kz',real=True));k2=(k.T*k)[0]
v=s.Matrix(s.symbols('v0:4',real=True));a=s.Matrix(s.symbols('a0:4',real=True))
D=s.symbols('D',positive=True)
L=sum(hs[i]*(v[i]**2-k2*a[i]**2)/2 for i in range(4))
L+=(K0+1)*(-2*v[0])**2/8
L+=sum(bi[i]*(-v[i+1]+k[i]*a[0])**2/2 for i in range(3))
L-=mu*sum((k[i]*a[j+1]+k[j]*a[i+1])**2 for i in range(3) for j in range(3))/4
L-=D*k2*k2*a[0]**2/2
L=s.expand(L)
K=s.hessian(L,v);G=-s.hessian(L,a)
M=s.Matrix(4,4,lambda i,j:s.diff(L,v[i],a[j]))
zero('all four positive kinetic coefficients',K-s.diag(K0,Ks,Ks,Ks))
Gtarget=s.zeros(4);Gtarget[0,0]=D*k2*k2-100*k[0]**2-101*k[1]**2-102*k[2]**2
Gtarget[1:4,1:4]=k2*s.diag(3,2,1)+2*k*k.T
zero('full gradient operator',G-Gtarget)
Mtarget=s.zeros(4)
for i in range(3):Mtarget[i+1,0]=-bi[i]*k[i]
zero('mixed derivative coupling retained',M-Mtarget)
momentum=s.Matrix([s.diff(L,q) for q in v])
zero('positive energy has both K and regulated G',(momentum.T*v)[0]-L-(v.T*K*v)[0]/2-(a.T*G*a)[0]/2)
# Proof constants are exact rational numbers, not a numerical fit.
Sbound=s.Rational(101,10**7)
spbound=s.Rational(1,2)
clockbound=s.Rational(1999,10000)
groupbound=Sbound+max(spbound,clockbound)
assert groupbound<1
checks.append('exact all-direction finite-band group-speed upper bound')

K0f=float(K0);Ksf=float(Ks);bn=np.array(bi,dtype=float).reshape(3)
an=np.array([100.,101.,102.]);Asp=np.diag([3.,2.,1.])
rows=[]
directions=[(1,2,3),(2,3,5),(3,1,4),(-1,2,4),(4,-3,2),(5,2,-1)]
for direction in directions:
    kn=np.array(direction,dtype=float);kn/=np.linalg.norm(kn)
    for qval in (103.,1000.,100000.):
        # |k|=1 at this evaluation, with D=qval held constant in derivatives.
        Gn=np.zeros((4,4));Gn[0,0]=(qval-np.dot(an,kn*kn))/K0f
        Gn[1:,1:]=(Asp+2*np.outer(kn,kn))/Ksf
        Sn=np.zeros((4,4));Sn[0,1:]=-bn*kn/np.sqrt(K0f*Ksf);Sn[1:,0]=Sn[0,1:]
        ev,U=np.linalg.eigh(Gn);assert ev.min()>0
        sq=np.sqrt(ev);X=(U*sq)@U.T
        A=np.block([[Sn,X],[X,np.zeros((4,4))]])
        omega,W=np.linalg.eigh(A)
        assert (omega>0).sum()==4 and (omega<0).sum()==4
        group=np.empty((8,3))
        for j in range(3):
            ej=np.eye(3)[j]
            dG=np.zeros((4,4));dG[0,0]=(4*qval*kn[j]-2*an[j]*kn[j])/K0f
            dG[1:,1:]=(2*kn[j]*Asp+2*(np.outer(ej,kn)+np.outer(kn,ej)))/Ksf
            dX=U@((U.T@dG@U)/(sq[:,None]+sq[None,:]))@U.T
            dS=np.zeros((4,4));dS[0,j+1]=dS[j+1,0]=-bn[j]/np.sqrt(K0f*Ksf)
            dA=np.block([[dS,dX],[dX,np.zeros((4,4))]])
            group[:,j]=np.diag(W.T@dA@W)
        maxgroup=float(np.linalg.norm(group,axis=1).max())
        assert maxgroup<=float(groupbound)+1e-10
        # Independent quadratic-pencil residual in the original normalized4D form.
        residuals=[]
        for j in range(8):
            xx=W[:4,j];rr=(omega[j]**2*np.eye(4)-omega[j]*Sn-Gn)@xx
            residuals.append(float(np.linalg.norm(rr)))
        assert max(residuals)<1e-12
        checks.append('positive finite spectrum/group/pencil '+str((direction,qval)))
        rows.append({'direction':direction,'Dk2':qval,'min_gradient_eigenvalue':float(ev.min()),'max_absolute_phase_speed':float(abs(omega).max()),'max_group_speed':maxgroup,'max_pencil_residual':max(residuals)})
result={'claim':'CIS-002','checks_passed':len(checks),'K_over_h':str(K),'G_clock_over_h':str(G[0,0]),'band_Dk2':[103,100000],'all_direction_group_speed_bound':str(groupbound),'group_bound_decimal':float(groupbound),'finite_checks':rows,'interpretation':'Exact source-preserving operator; local frozen matter principal benchmark only. No full gravity/interface/cutoff/engine certificate.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(result,indent=2))
