"""Distinct local two-field/discrete-velocity prototype; gravity not included."""
from pathlib import Path
import json
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp

HERE=Path(__file__).resolve().parent
P1,P2,g1,g2,D,p,h0,R,Gamma,c=s.symbols('P1 P2 g1 g2 D p h0 R Gamma c',real=True)
Pi=s.Matrix([P1,P2]);gg=s.Matrix([g1,g2])
h=P2*g1-P1*g2
r=s.Matrix([D*g2+P2*p,-D*g1-P1*p])
source=Gamma*h*r*R;J=Gamma*h*h*R
assert s.simplify((Pi.T*source)[0]+D*J)==0
assert s.simplify(-(gg.T*source)[0]+p*J)==0
# A single local scalar needs compatible energy and momentum transfer.
ss,j=s.symbols('scalar_source collision_rate',real=True)
ec=P1*ss+D*j;pc=g1*ss-p*j
assert s.expand(g1*ec-P1*pc-(D*g1+p*P1)*j)==0
assert (D*g1+p*P1).subs({D:1,g1:1,p:1,P1:1})!=0
# Exact local field flux identities, using independent spatial derivatives.
Px=s.Matrix(s.symbols('P1x P2x',real=True));gx=s.Matrix(s.symbols('g1x g2x',real=True))
ERdot=(Pi.T*(c*c*gx+source))[0]+c*c*(gg.T*Px)[0]
ERflux_x=-c*c*((Px.T*gg)[0]+(Pi.T*gx)[0])
assert s.simplify(ERdot+ERflux_x-(Pi.T*source)[0])==0
PRdot=-((c*c*gx+source).T*gg)[0]-(Pi.T*Px)[0]
PRflux_x=(Pi.T*Px)[0]+c*c*(gg.T*gx)[0]
assert s.simplify(PRdot+PRflux_x+(gg.T*source)[0])==0
assert s.simplify((Pi.T*(-source))[0]+D*J)!=0 # source sign mutation
assert s.simplify(-(gg.T*(source-Gamma*h*R*p*s.Matrix([P2,-P1])))[0]+p*J)!=0

vel=np.array([0.,.01,-.02,.01]);ch=np.array([-1.,-1.,1.,1.])
cost=float(ch@(vel*vel/2));recoil=float(ch@vel)
uf=s.Matrix(s.symbols('f1:5',real=True));pp=s.Matrix([P1,P2]);gr=s.Matrix([g1,g2])
rx=uf[0]*uf[1]-uf[2]*uf[3]
localF=s.Matrix.vstack(s.Rational(1,10)*h*h*s.Matrix(ch.astype(int).tolist())*rx,
                       s.Rational(1,10)*h*s.Matrix([s.Rational(str(cost))*g2+P2*s.Rational(str(recoil)),
                                                  -s.Rational(str(cost))*g1-P1*s.Rational(str(recoil))])*rx,
                       s.zeros(2,1))
U=list(uf)+list(pp)+list(gr)
Jac=np.array(localF.jacobian(U).subs(dict(zip(U,[2,2,1,1,.5,0,0,1]))),dtype=float)
A=np.zeros((8,8));A[:4,:4]=np.diag(vel);A[4:6,6:8]=-np.eye(2);A[6:8,4:6]=-np.eye(2)
assert np.array_equal(A,A.T)
growth_bound=float(np.linalg.eigvalsh((Jac+Jac.T)/2).max())
wkb=[]
for wave in [10.,1000.,100000.]:
    growth=float(np.linalg.eigvals(Jac-1j*wave*A).real.max())
    assert growth<=growth_bound+1e-7
    wkb.append({'k':wave,'max_real_growth':growth})

def evolve(N,kind='main',gamma=.1):
    dx=2*np.pi/N;x=np.arange(N)*dx
    f=np.array([2+.1*np.cos(x),2+.1*np.sin(x),1+.05*np.cos(2*x),1+.05*np.sin(2*x)])
    Pi=np.array([.5*np.cos(x),np.zeros(N)]);g=np.array([-np.sin(x),np.cos(x)])
    if kind=='empty':f[2:]=0
    if kind=='zero':Pi[:]=0;g[:]=0
    if kind=='collinear':Pi[1]=2*Pi[0];g[1]=2*g[0]
    assert np.max(np.abs(g.mean(axis=1)))<1e-12
    initial=np.vstack([f,Pi,g]); y0=initial.ravel()
    def deriv(a):return (np.roll(a,-1,axis=-1)-np.roll(a,1,axis=-1))/(2*dx)
    def rhs(t,y):
        z=y.reshape(8,N);f=z[:4];Pi=z[4:6];g=z[6:]
        cold=np.empty_like(f)
        for i,v in enumerate(vel):
            cold[i]=-v*((f[i]-np.roll(f[i],1))/dx if v>=0 else (np.roll(f[i],-1)-f[i])/dx)
        h=Pi[1]*g[0]-Pi[0]*g[1];R=f[0]*f[1]-f[2]*f[3]
        r=np.array([cost*g[1]+Pi[1]*recoil,-cost*g[0]-Pi[0]*recoil])
        J=gamma*h*h*R
        return np.vstack([cold+ch[:,None]*J,deriv(g)+gamma*h*r*R,deriv(Pi)]).ravel()
    z0=initial;dz0=rhs(0,y0).reshape(8,N)
    mdot=dx*dz0[:4].sum()
    edot=dx*((vel*vel/2)@dz0[:4]+(z0[4:6]*dz0[4:6]).sum(axis=0)+(z0[6:]*dz0[6:]).sum(axis=0)).sum()
    pdot=dx*(vel@dz0[:4]-(dz0[4:6]*z0[6:]+z0[4:6]*dz0[6:]).sum(axis=0)).sum()
    assert max(abs(mdot),abs(edot),abs(pdot))<=1e-10
    sol=solve_ivp(rhs,(0,2),y0,method='DOP853',rtol=2e-10,atol=2e-12,t_eval=np.linspace(0,2,201))
    assert sol.success,sol.message
    z=sol.y.reshape(8,N,-1);f=z[:4];Pi=z[4:6];g=z[6:]
    mass=dx*f.sum(axis=(0,1));coldE=dx*np.einsum('i,ijt->t',vel*vel/2,f)
    waveE=dx*(Pi*Pi+g*g).sum(axis=(0,1))/2
    energy=coldE+waveE
    momentum=dx*(np.einsum('i,ijt->jt',vel,f)-(Pi*g).sum(axis=0)).sum(axis=0)
    errors={'mass':float(np.max(np.abs(mass-mass[0]))),
            'energy_relative':float(np.max(np.abs(energy-energy[0]))/max(1,abs(energy[0]))),
            'momentum':float(np.max(np.abs(momentum-momentum[0])))}
    assert max(errors.values())<=1e-7 and f.min()>=-1e-8
    density_change=float(dx*np.abs(f[:,:,-1].sum(axis=0)-initial[:4].sum(axis=0)).sum())
    assert density_change>1e-8
    h=Pi[1]*g[0]-Pi[0]*g[1];R=f[0]*f[1]-f[2]*f[3]
    maxcollision=float(np.max(np.abs(gamma*h*h*R)))
    if kind in ['zero','collinear'] or gamma==0:assert maxcollision<=1e-12
    if kind=='empty':assert dx*f[2:,:,-1].sum()>1e-8
    return {'N':N,'kind':kind,'gamma_diagnostic':gamma,'errors':errors,
            'minimum_f':float(f.min()),'L1_density_change':density_change,
            'cold_energy_change':float(coldE[-1]-coldE[0]),
            'receiver_energy_change':float(waveE[-1]-waveE[0]),
            'max_collision_rate':maxcollision},z[:,:,-1]

main64,last64=evolve(64);main128,last128=evolve(128)
empty,_=evolve(64,'empty');zero,_=evolve(64,'zero');off,_=evolve(64,gamma=0);collinear,_=evolve(64,'collinear')
diff=float(np.sqrt(np.mean((last64-last128[:,::2])**2)))
result={'symbolic':{'local_energy_mass_momentum_sources':True,'local_flux_identities':True,
                   'single_scalar_compatibility_restriction':True,'source_mutations_detected':True,
                   'constant_symmetric_principal_matrix':True},
        'frozen_background_growth_bound':growth_bound,'WKB_samples':wkb,
        'cases':[main64,main128,empty,zero,off,collinear],
        'two_grid_state_RMS_difference':diff,
        'scope':'Distinct two-local-field 1D discrete-velocity prototype; no gravity, microscopic kernel, action, physical rate or halo selection.'}
HERE.joinpath('local_run/results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
