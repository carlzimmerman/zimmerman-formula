import json,sys
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import solve_bvp,simpson,cumulative_trapezoid

checks=[]
def check(name,c,detail=''):
    checks.append(dict(name=name,passed=bool(c),detail=str(detail)))
    if not c:raise AssertionError(name+': '+str(detail))
R,n,a,b,gamma,z,alpha,delta,c2=s.symbols('R n a b gamma z alpha delta c2',positive=True)
M=n*n/R*s.Matrix([[1+R*a/n,1],[1,1]])
K=n*n*s.diag(b,gamma)
poly=s.simplify((K-z*M).det()/M.det())
normalized=s.simplify(poly.subs({a:alpha*n/R,b:c2*alpha/R,gamma:delta*alpha/R}))
target=z*z-(c2+(1+alpha)*delta)*z+c2*alpha*delta
check('unequal-density principal cone',s.simplify(normalized-target)==0,target)
check('unequal-density kinetic determinant',s.simplify(M.det()-n**3*a/R)==0,M.det())

S=5.364;rmin=1e-5
def baryon(x):return np.minimum(x**3,1.)
def components(x,q):
    qq=np.clip(q,0.,S);src=baryon(x)+qq
    root=2*src*x*x/(np.sqrt(src*src+4*src*x*x)+src)
    m=np.minimum(qq+root,S);u=(m-qq)/(x*x)
    return m,u,u/(1-u)
def solve(B,factor,tol):
    Rout=max(100.,factor*B)
    x=np.unique(np.r_[np.geomspace(rmin,Rout,900),1.])
    scale=(576*B**3/S)**(1/3)
    q=S*x**3/(scale**3+x**3)
    force=components(x,q)[2]
    htail=B*(3*(S-q[-1])/Rout**3)**(2/3)
    h=htail+cumulative_trapezoid(force,x,initial=0)[-1]-cumulative_trapezoid(force,x,initial=0)
    def rhs(x,y):return np.array([x*x*(np.maximum(y[1],0)/B)**1.5,-components(x,y[0])[2]])
    def bc(a,z):
        return np.array([a[0]-(max(a[1],0)/B)**1.5*rmin**3/3,z[1]-B*(3*max(S-z[0],0)/Rout**3)**(2/3)])
    sol=solve_bvp(rhs,bc,x,np.array([q,h]),tol=tol,max_nodes=30000)
    check('soft profile B%g outer%g'%(B,factor),sol.success,sol.message)
    return sol,Rout
rows=[]
for B in [1000.,100.,10.,1.]:
    sol,R1=solve(B,100.,5e-7);ref,R2=solve(B,200.,1e-7)
    probes=np.geomspace(rmin,R1,4000);q,h=ref.sol(probes)
    den=(np.maximum(h,0)/B)**1.5
    check('soft reference physical B%g'%B,min(q)>-1e-7 and max(q)<S+1e-7 and min(h)>-1e-8,(min(q),max(q),min(h)))
    change=float(max(abs(sol.sol(probes)[0]-q))/S)
    check('soft boundary sensitivity B%g'%B,change<5e-4,change)
    m,u,force=components(probes,q)
    check('soft carrier admissible B%g'%B,min(np.diff(m))>=-1e-7 and min(u)>=-1e-8 and max(u)<1,(min(u),max(u)))
    interior=m<S-1e-6;g=(baryon(probes)+m)/probes**2
    check('soft carrier force B%g'%B,max(abs((force-g)[interior])/(1+g[interior]))<1e-9,'Algebraic constitutive balance on positive actual support')
    equation=ref.sol(probes,1)-np.array([probes**2*den,-force])
    eq=float(max(np.max(abs(equation[0])/(1+probes**2*den)),np.max(abs(equation[1])/(1+force))))
    check('soft reference residual B%g'%B,eq<2e-5,eq)
    integral=float(simpson(probes**2*den,x=probes));ledger=integral+float(q[0])+float(S-q[-1])
    check('soft reference mass B%g'%B,abs(ledger-S)<2e-4,ledger)
    controls=[]
    for radius in [1.,2.,4.]:
        qq=float(ref.sol(radius)[0]);actual=float(components(np.array([radius]),np.array([qq]))[0][0]);gb=1/radius**2
        goal=(gb+np.sqrt(gb*gb+4*gb))/2
        controls.append(dict(r=radius,reference_mass=qq,actual_mass=actual,force_ratio=(1+actual)/radius**2/goal))
    qout,hout=ref.sol(R2);dout=S-qout
    amplitude=float(dout*R2**3)
    expected=576*B**3
    rows.append(dict(B=B,outer_radii=[R1,R2],nodes=[len(sol.x),len(ref.x)],profile_change_over_S=change,equation_residual=eq,mass_ledger=ledger,far_tail_amplitude=amplitude,asymptotic_amplitude=expected,tail_amplitude_relative_error=abs(amplitude/expected-1),force_controls=controls))
out=dict(checks=checks,cases=rows,scope='Conditional soft-EOS coupled NR BVP with outer power matching; finite checked family, not continuum stability, physical EOS or full causal parent.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
