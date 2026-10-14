"""One confined pair channel, free mediator resolvent, prescribed optical field."""
import math,json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad,solve_bvp
from scipy.optimize import brentq
from scipy.special import dawsn
from numpy.polynomial.legendre import leggauss
prior=json.loads(Path('sol61_push/muon_nuclear_matching_2026_10_14/run/results.json').read_text())
hc=1.973269804e-7; hb=6.582119569e-16; c=299792458.; ej=1.602176634e-19
m=1.; MR=2.; delta=2e-9; mu=.002; g=1e-20; lam=1e-6
U=prior['stronger_wall_eV']; aSI=.02; a=aSI/hc; Lt=.001/hc
F0=g*(1e12/c)/(ej/hc**3)/math.sqrt(2*MR); h=mu/(2*m*math.sqrt(2*MR))
z0=a*math.sqrt(2*m*U)
x0=brentq(lambda x:x/math.tan(x)+math.sqrt(z0*z0-x*x),math.pi/2+1e-10,math.pi-1e-10,xtol=1e-14)
beta=math.sqrt(z0*z0-x0*x0)
norm=.5-math.sin(2*x0)/(4*x0)+math.sin(x0)**2/(2*beta)
E0=x0*x0/(2*m*a*a)
def v(x):
    x=np.asarray(x);return np.where(x<=1,np.sin(x0*x),math.sin(x0)*np.exp(-beta*np.maximum(x-1,0)))/math.sqrt(norm)
def source(x):
    x=np.asarray(x); t=a*x/(math.sqrt(2)*Lt)
    out=np.ones_like(t);np.divide(dawsn(t),t,out=out,where=t!=0)
    return np.where(x<=1,out,0.)
def nodes(N):
    q,w=leggauss(N); out=[]
    for l,r in [(0,1),(1,1+25/beta)]:out.append((l+(q+1)*(r-l)/2,w*(r-l)/2))
    return np.concatenate([t[0] for t in out]),np.concatenate([t[1] for t in out])
checks=[]
def ck(name,e,t):
    assert e<=t,(name,e,t)
    checks.append(dict(name=name,error=float(e),tolerance=t))
ck('radial_normalization',abs(quad(lambda x:float(v(x))**2,0,1)[0]+math.sin(x0)**2/(2*beta*norm)-1),1e-12)
# BVP independently avoids the diagonal cusp of a direct Green-function double integral.
end=1+25/beta
def solve(C,kind,tol=1e-9):
    mesh=np.unique(np.r_[np.linspace(0,1,501),np.linspace(1,end,101)])
    def rhs(x,y):
        if kind=='source': f=x*source(x)
        else:
            f=np.zeros_like(x);np.divide(v(x)**2,x,out=f,where=x!=0)
        return np.vstack((y[1],C*C*y[0]-f))
    def bc(y0,y1):return np.array([y0[0],y1[1]+C*y1[0]])
    sol=solve_bvp(rhs,bc,mesh,np.zeros((2,len(mesh))),tol=tol,max_nodes=20000)
    # The source is discontinuous at 1. Avoid a discontinuous RHS by computing it via Green quadrature below.
    if not sol.success: raise RuntimeError(sol.message)
    return sol
# Smooth source truncation boundary: solve source only inside then match its decaying continuation.
def source_solution(C,tol):
    def rhs(x,y):return np.vstack((y[1],C*C*y[0]-x*source(x)))
    def bc(y0,y1):return np.array([y0[0],y1[1]+C*y1[0]])
    mesh=np.linspace(0,1,501)
    sol=solve_bvp(rhs,bc,mesh,np.zeros((2,len(mesh))),tol=tol,max_nodes=20000)
    assert sol.success
    return lambda x: np.where(np.asarray(x)<=1,sol.sol(np.minimum(x,1))[0],sol.sol(1)[0]*np.exp(-C*(np.maximum(x,1)-1)))
def evaluate(E,tol=1e-9):
    eta=delta-E; assert eta>0
    C=a*math.sqrt(2*MR*eta)
    sol=solve(C,'pair',tol); ss=source_solution(C,tol)
    xs,ws=nodes(320); density=v(xs)**2/xs
    Jself=float(np.dot(ws,density*sol.sol(xs)[0]))
    Jsource=float(np.dot(ws,density*ss(xs)))
    shift=-MR*h*h/(2*math.pi*a)*Jself
    omega=-2*MR*a*a*h*F0*Jsource
    return shift,omega,C,sol,ss
# Opposite-charge contact plus leading nonresonant t-channel R exchange.
contact=(lam-mu*mu/(4*MR*MR))/(4*math.pi*m*m*a**3)*quad(lambda x:float(v(x))**4/(x*x) if x else 0,0,end,points=[1],epsabs=1e-11)[0]
bare=2*E0+contact
energy=brentq(lambda E:E-bare-evaluate(E)[0],bare-1e-11,bare,xtol=1e-22)
shift,omega,C,sol,ss=evaluate(energy)
fine=evaluate(energy,1e-11)
ck('BVP_refinement_self',abs(shift/fine[0]-1),2e-7)
ck('BVP_refinement_source',abs(omega/fine[1]-1),2e-7)
ck('dressed_energy_equation',abs(energy-bare-shift),1e-20)
# Independent Green quadrature at selected radii including the source-free tail.
for X in [.1,.5,1.,end]:
    G=lambda y:(math.exp(-C*abs(X-y))-math.exp(-C*(X+y)))/(2*C)
    val=quad(lambda y:G(y)*y*float(source(y)),0,1,points=[X] if X<1 else None,epsabs=1e-12)[0]
    ck('source_Green_vs_BVP',abs(float(ss(np.array(X)))-val)/max(abs(val),1e-30),3e-7)
# The resolvent's imaginary part is zero below the free mediator continuum.
assert 0<energy<delta and E0<U
# Normalize the dressed state, including its virtual mediator component.
def derivative(step):return (evaluate(energy+step)[0]-evaluate(energy-step)[0])/(2*step)
d1=derivative(1e-12); d2=derivative(1e-13)
ck('residue_derivative_refinement',abs(d1/d2-1),2e-6)
assert d2<0
residue=1/(1-d2); omega_dressed=math.sqrt(residue)*omega
for X in [.2,.7]:
    G=lambda y:(math.exp(-C*abs(X-y))-math.exp(-C*(X+y)))/(2*C)
    val=quad(lambda y:G(y)*float(v(y))**2/y if y else 0,0,end,points=[X,1],epsabs=1e-12)[0]
    ck('pair_Green_vs_BVP',abs(float(sol.sol(X)[0])-val)/abs(val),3e-7)
# Continuum normalization of h reproduces the previously used NR decay width.
p=math.sqrt(m*delta)
ck('h_vacuum_width_normalization',abs((h*h*m*p/(2*math.pi))/(mu*mu*math.sqrt(delta/m)/(16*math.pi*MR))-1),1e-14)
result=dict(sphere_radius_m=aSI,wall_eV=U,single_particle_energy_eV=E0,
    pair_contact_shift_eV=contact,bare_pair_excess_eV=bare,
    virtual_mediator_self_energy_eV=shift,dressed_pair_excess_eV=energy,
    below_mediator_gap_eV=delta-energy,evanescent_length_m=aSI/C,
    pair_component_residue=residue,virtual_mediator_probability=1-residue,
    pair_drive_matrix_element_eV=omega_dressed,pair_drive_angular_frequency_per_s=abs(omega_dressed)/hb,
    perturbative_time_for_probability_001_s=.1*hb/abs(omega_dressed),
    checks=checks,passed=len(checks),scope='Single-pair projection with assumed wall and optical field; no full many-pair or photon-loss calculation')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
