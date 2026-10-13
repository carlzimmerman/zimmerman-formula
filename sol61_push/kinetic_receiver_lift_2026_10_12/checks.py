"""Frozen finite collision/receiver checks; no halo selector or streaming claim."""
from pathlib import Path
import json
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

HERE=Path(__file__).resolve().parent
f=sp.Matrix(sp.symbols('f1:5',positive=True))
B=sp.Matrix(sp.symbols('B1:3',positive=True))
v=sp.Matrix(sp.symbols('v1:5',real=True))
u=sp.Matrix(sp.symbols('u1:3',real=True))
K11,K12,K22=sp.symbols('K11 K12 K22',real=True)
K=sp.Matrix([[K11,K12],[K12,K22]])
C=sp.Matrix([[1,1,0,0],[0,0,1,1]])
rho=C*f+B
Ec=sum(f[i]*v[i]**2/2 for i in range(4))+sum(B[i]*u[i]**2/2 for i in range(2))+(rho.T*K*rho)[0]/2
gf=sp.Matrix([sp.diff(Ec,z) for z in f]); gB=sp.Matrix([sp.diff(Ec,z) for z in B])
assert sp.simplify(gf-sp.Matrix([z*z/2 for z in v])-C.T*K*rho)==sp.zeros(4,1)
assert sp.simplify(gB-sp.Matrix([z*z/2 for z in u])-K*rho)==sp.zeros(2,1)
b=sp.Matrix([-1,-1,1,1])
Dactual=(b.T*gf)[0]
q=sp.symbols('q',real=True)
Dpath=sp.simplify(Dactual.subs(dict(zip(f,f+b*q))))
assert sp.simplify(sp.diff(Dpath,q)-(b.T*C.T*K*C*b)[0])==0
curvature=sp.simplify(sp.diff(Dpath,q).subs({K11:-2,K12:-1,K22:-3}))
assert curvature==-12

phi1,phi2,p1,p2,k,Om,D,pb,gamma=sp.symbols('phi1 phi2 p1 p2 k Om D pb gamma',real=True)
phi=sp.Matrix([phi1,phi2]); Pi=sp.Matrix([p1,p2]); G=sp.Matrix([[0,k],[-k,0]])
g=G*phi
h=p2*g[0]-p1*g[1]
r=sp.Matrix([D*g[1]+p2*pb,-D*g[0]-p1*pb])
assert sp.simplify(h-D*0-k*(Pi.T*phi)[0])==0
assert sp.simplify(h*D+(Pi.T*r)[0])==0
assert sp.simplify(h*pb-(g.T*r)[0])==0
assert sum(b)==0
Pr=-(Pi.T*g)[0]; Hr=((Pi.T*Pi)[0]+Om**2*(phi.T*phi)[0])/2
z=list(phi)+list(Pi); ham=list(Pi)+list(-Om**2*phi)
assert sp.simplify(sum(sp.diff(Hr,zz)*rr for zz,rr in zip(z,ham)))==0
assert sp.simplify(sum(sp.diff(Pr,zz)*rr for zz,rr in zip(z,ham)))==0
a=f[0]*f[1]; bp=f[2]*f[3]; R=a-bp
S=-sum(ff*(sp.log(ff)-1) for ff in f)
aff=(b.T*sp.Matrix([sp.diff(S,ff) for ff in f]))[0]
assert sp.simplify(sp.expand_log(aff,force=True)-sp.expand_log(sp.log(a/bp),force=True))==0
fdot=gamma*h*h*b*R
for i in range(4):
    boundary=sp.simplify(fdot[i].subs({f[i]:0}))
    expected=gamma*h*h*(bp if i<2 else a)
    assert sp.simplify(boundary-expected.subs({f[i]:0}))==0
# Removal of energy reaction and removal of momentum recoil are distinct controls.
assert sp.simplify((gamma*h*h*D*R).subs({gamma:1,k:1,phi1:1,phi2:0,p1:1,p2:1,D:3,f[0]:2,f[1]:2,f[2]:1,f[3]:1}))!=0
rbad=r-pb*sp.Matrix([p2,-p1])
assert sp.simplify(h*pb-(g.T*rbad)[0]-h*pb)==0
assert sp.simplify((h*pb).subs({k:1,phi1:1,phi2:0,p1:1,p2:1,pb:-2}))!=0
reverse_entropy=-gamma*h*h*R*sp.log(a/bp)
assert float(reverse_entropy.subs({gamma:1,k:1,phi1:1,phi2:0,p1:1,p2:1,f[0]:2,f[1]:2,f[2]:1,f[3]:1}))<0
# Previous quadratic entropy has an outward derivative at an empty bin.
bb=np.array([1.,-2.,1.]); oldf=np.array([0.,1.,3.])
oldrate=bb*np.dot(bb,-oldf)
assert oldrate[0]<0
# Previous spatial map moves mass while its declared velocity moment is zero.
oldsp=np.array([2.,1.]); edge=np.array([-1.,1.])
old_spatial_rate=edge*np.dot(edge,-oldsp)
assert np.max(np.abs(old_spatial_rate))>0 and np.all(np.zeros(2)*oldsp==0)
# Exact traveling mode and its minimum-energy identity.
J=G/k
for sign in [-1,1]:
    traveling={p1:sign*Om*(J*phi)[0],p2:sign*Om*(J*phi)[1]}
    assert sp.simplify(h.subs(traveling))==0
    assert sp.simplify(Hr.subs(traveling)**2-(Om/k)**2*Pr.subs(traveling)**2)==0

def entropy(ff):
    good=ff>0
    return -np.sum(np.where(good,ff*(np.log(np.maximum(ff,1e-300))-1),0),axis=0)

def run(name,vel,ff,field='rest'):
    vel=np.array(vel,dtype=float); init=np.array(ff,dtype=float)
    cost=float(np.dot(vel*vel/2,np.array(b,dtype=float).ravel()))
    recoil=float(np.dot(vel,np.array(b,dtype=float).ravel()))
    ph=[np.sqrt(6.),0.]; pp=[0.,0.]
    if field=='zero': ph=[0.,0.]
    if field=='traveling':ph=[1.,0.];pp=[0.,1.]
    y0=np.r_[init,ph,pp]; ch=np.array(b,dtype=float).ravel()
    def rhs(t,y):
        ff=y[:4]; ph=y[4:6]; pp=y[6:8]; gg=np.array([ph[1],-ph[0]])
        hh=pp[1]*gg[0]-pp[0]*gg[1]
        rr=np.array([cost*gg[1]+pp[1]*recoil,-cost*gg[0]-pp[0]*recoil])
        rate=ff[0]*ff[1]-ff[2]*ff[3]
        return np.r_[.05*hh*hh*ch*rate,pp,-ph+.05*hh*rr*rate]
    sol=solve_ivp(rhs,(0,100),y0,method='DOP853',rtol=2e-10,atol=2e-12,t_eval=np.linspace(0,100,2001))
    assert sol.success,sol.message
    ff=sol.y[:4];ph=sol.y[4:6];pp=sol.y[6:8]
    N=ff.sum(axis=0); cold=np.dot(vel*vel/2,ff)
    Hrnum=(pp*pp+ph*ph).sum(axis=0)/2
    # Collision-local cold/baryon gravitational energy remains constant.
    # Include a one-cell symmetric kernel -1 and baryon mass 2 in the diagnostic.
    grav=-(N+2)**2/2
    energy=cold+grav+Hrnum
    Pfield=-(pp[0]*ph[1]-pp[1]*ph[0]); momentum=np.dot(vel,ff)+Pfield
    eerr=float(np.max(np.abs(energy-energy[0]))/max(1,abs(energy[0])))
    nerr=float(np.max(np.abs(N-N[0])));perr=float(np.max(np.abs(momentum-momentum[0])))
    ent=entropy(ff);ds=float(np.min(np.diff(ent)))
    floor=float(np.min(Hrnum-np.abs(Pfield)))
    assert eerr<=1e-7 and nerr<=1e-7 and perr<=1e-7
    assert ff.min()>=-1e-8 and ds>=-1e-8 and floor>=-1e-8
    shift=float(np.max(np.abs(ff[:,-1]-init)))
    if field=='zero':assert shift==0
    if field=='traveling':assert shift<=1e-7
    if name=='import':assert cold[-1]>cold[0]+1e-6 and Hrnum[-1]<Hrnum[0]-1e-6
    if name=='export':assert cold[-1]<cold[0]-1e-6 and Hrnum[-1]>Hrnum[0]+1e-6
    if name=='empty':assert min(ff[2,-1],ff[3,-1])>0
    if name=='recoil':assert abs(Pfield[-1]-Pfield[0])>1e-6
    return {'case':name,'D':cost,'cold_momentum_increment':recoil,'final_f':ff[:,-1].tolist(),
            'cold_energy_change':float(cold[-1]-cold[0]),'receiver_energy_change':float(Hrnum[-1]-Hrnum[0]),
            'receiver_momentum_change':float(Pfield[-1]-Pfield[0]),'energy_relative_error':eerr,
            'mass_error':nerr,'momentum_error':perr,'minimum_f':float(ff.min()),
            'minimum_sampled_entropy_increment':ds,'minimum_receiver_energy_above_momentum_floor':floor}

rows=[run('import',[-1,1,-2,2],[2,2,1,1]),run('export',[-1,1,-2,2],[1,1,2,2]),
      run('recoil',[0,1,-2,1],[2,2,1,1]),run('empty',[-1,1,-2,2],[1,1,0,0]),
      run('zero',[-1,1,-2,2],[2,2,1,1],'zero'),run('traveling',[-1,1,-2,2],[2,2,1,1],'traveling')]
result={'symbolic':{'full_matter_gradients':True,'state_dependent_channel_cost':True,
                   'example_D_path_curvature':int(curvature),'energy_mass_momentum_degeneracies':True,
                   'canonical_field_energy_momentum':True,'inward_boundary_closure':True,
                   'reaction_sign_controls':True,'old_positivity_counterexample':oldrate.tolist(),
                   'old_spatial_streaming_counterexample':old_spatial_rate.tolist(),
                   'traveling_wave_inactivity':True},'runs':rows,
        'scope':'Local finite collision and one Fourier momentum direction. Not spatial kinetic transport, a parent action, microphysics, or a halo selector.'}
HERE.joinpath('run/results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
