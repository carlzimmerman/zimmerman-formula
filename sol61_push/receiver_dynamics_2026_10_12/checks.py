"""Declared reduced receiver experiment; not a target-free galaxy mechanism."""
from pathlib import Path
import json
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

q,phi,pi,D,m,A,w=sp.symbols('q phi pi D m A w', real=True)
E=D*q+(pi*pi+w*w*phi*phi)/2
S=-(A-q)**2/2
rhs=sp.Matrix([m*pi*pi*(A-q),pi,-w*w*phi-m*D*pi*(A-q)])
gradE=sp.Matrix([sp.diff(E,x) for x in (q,phi,pi)])
gradS=sp.Matrix([sp.diff(S,x) for x in (q,phi,pi)])
v=sp.Matrix([pi,0,-D]); M=m*v*v.T
L=sp.Matrix([[0,0,0],[0,0,1],[0,-1,0]])
assert sp.simplify((gradE.T*rhs)[0])==0
assert sp.simplify((gradS.T*rhs)[0]-m*pi*pi*(A-q)**2)==0
assert sp.simplify(M*gradE)==sp.zeros(3,1)
assert L*gradS==sp.zeros(3,1)
assert sp.simplify(L*gradE+M*gradS-rhs)==sp.zeros(3,1)
# Exact nonzero potential at rest supplies cubic onset.
q1=rhs[0]; q2=sum(sp.diff(q1,x)*r for x,r in zip((q,phi,pi),rhs))
q3=sp.simplify(sum(sp.diff(q2,x)*r for x,r in zip((q,phi,pi),rhs)))
assert sp.simplify(q3.subs({q:0,pi:0})-2*m*A*w**4*phi**2)==0
broken=sp.Matrix([rhs[0],pi,-w*w*phi])
assert sp.simplify((gradE.T*broken)[0]-D*m*pi*pi*(A-q))==0
reverse=L*gradE-M*gradS
assert sp.simplify((gradE.T*reverse)[0])==0
assert sp.simplify((gradS.T*reverse)[0]+m*pi*pi*(A-q)**2)==0

def evolve(cost,H0,omega=1.,phi0=None,end=400.,points=2001):
    x0=np.array([0.,np.sqrt(2*H0)/omega if phi0 is None else phi0,0.])
    def f(t,x):
        z,p,r=x; y=1-z
        return [r*r*y,r,-omega*omega*p-cost*r*y]
    sol=solve_ivp(f,(0.,end),x0,method='DOP853',rtol=2e-10,atol=2e-12,t_eval=np.linspace(0,end,points))
    assert sol.success,sol.message
    z,p,r=sol.y; H=(r*r+omega*omega*p*p)/2
    Etot=cost*z+H; err=float(np.max(np.abs(Etot-Etot[0]))/max(1.,Etot[0]))
    entropy=-(1-z)**2/2
    assert err<=1e-7,err
    assert z.min()>=-1e-8 and H.min()>=-1e-8
    assert np.diff(z).min()>=-1e-8
    assert np.diff(entropy).min()>=-1e-8
    cap=min(1.,H0/cost) if cost>0 else 1.
    assert z.max()<=cap+1e-8
    return {'D':cost,'H0':float(Etot[0]),'omega':omega,'q_final':float(z[-1]),
            'H_final':float(H[-1]),'energy_error':err,'min_dq':float(np.diff(z).min())}

rows=[evolve(1.,h) for h in [.25,1.,4.]]
assert abs(rows[0]['q_final']-.25)<1e-5
assert 0<1-rows[1]['q_final']<.01
assert abs(rows[2]['q_final']-1)<1e-5
exo=evolve(-1.,.25); assert abs(exo['q_final']-1)<1e-5
zero=evolve(-1.,0.); assert zero['q_final']==0
flat=evolve(1.,0.,omega=0.,phi0=1.); assert flat['q_final']==0
short=evolve(1.,1.,end=.001,points=2)
expected=2*.001**3/3
assert abs(short['q_final']/expected-1)<.002
result={'symbolic':{'energy_identity':True,'entropy_identity':True,
                    'energy_degeneracy':True,'hamiltonian_entropy_degeneracy':True,
                    'full_bracket_identity':True,'cubic_onset':True,
                    'missing_reaction_mutation_detected':True,'reversed_entropy_mutation_detected':True},
        'endothermic':rows,'exothermic':exo,'zero_seed':zero,'flat_at_rest':flat,
        'cubic_onset':{'computed':short['q_final'],'leading':expected},
        'scope':'Reduced dimensionless transfer channel. Endpoint and coefficients imposed; no halo selector or physical rate derived.'}
Path(__file__).with_name('run').joinpath('results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
