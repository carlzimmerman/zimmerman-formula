"""Exact exponential-coupling energy identities and a homogeneous control.

No galaxy/cosmology fit; no continuum gravity well-posedness assertion.
"""
import argparse
import json
import sys
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    checks = {}

    def exact(name, value):
        residual = s.simplify(s.expand(value))
        assert residual == 0, (name, residual)
        checks[name] = {'passed': True, 'residual': str(residual)}

    t, x = s.symbols('t x', real=True)
    z = s.Function('z')(t, x)
    u = s.Function('u')(t, x)
    v = s.Function('v')(t, x)
    m, lam, M, om, cz = s.symbols('m lam M om cz', positive=True)
    A, B = s.exp(z), s.exp(-z)
    potential = m*m*(u*u+v*v)/2 + lam*(u*u+v*v)**2/4
    kinetic = (s.diff(u,t)**2+s.diff(v,t)**2)/2
    spatial = (s.diff(u,x)**2+s.diff(v,x)**2)/2
    energy = A*kinetic+B*(spatial+potential)
    eu = s.diff(A*s.diff(u,t),t)-s.diff(B*s.diff(u,x),x)+B*s.diff(potential,u)
    ev = s.diff(A*s.diff(v,t),t)-s.diff(B*s.diff(v,x),x)+B*s.diff(potential,v)
    flux = B*(s.diff(u,t)*s.diff(u,x)+s.diff(v,t)*s.diff(v,x))
    exact('carrier_energy_exchange',s.diff(energy,t)-s.diff(flux,x)
          -s.diff(u,t)*eu-s.diff(v,t)*ev+s.diff(z,t)*energy)
    ez = M*M*(s.diff(z,t,2)-cz*cz*s.diff(z,x,2)+om*om*z)-energy
    ze = M*M*(s.diff(z,t)**2+cz*cz*s.diff(z,x)**2+om*om*z*z)/2
    zflux = M*M*cz*cz*s.diff(z,t)*s.diff(z,x)
    exact('total_variational_energy_identity',s.diff(energy+ze,t)-s.diff(flux+zflux,x)
          -s.diff(u,t)*eu-s.diff(v,t)*ev-s.diff(z,t)*ez)
    jt=A*(u*s.diff(v,t)-v*s.diff(u,t))
    jx=-B*(u*s.diff(v,x)-v*s.diff(u,x))
    exact('phase_current_identity',s.diff(jt,t)+s.diff(jx,x)-u*ev+v*eu)

    N,Z,K,W,raw=s.symbols('N Z K W raw',positive=True)
    L=N*(s.exp(Z)*K/N**2-s.exp(-Z)*W)
    rho=s.exp(Z)*K/N**2+s.exp(-Z)*W
    exact('lapse_density_equals_Z_source',-s.diff(L,N)-rho)
    exact('Z_variation_equals_lapse_density',s.diff(L,Z)/N-rho)
    exact('first_order_linear_subtraction',s.diff(L,Z).subs(Z,0)/N-(K/N**2+W))
    # A bounded gate composed with kinetic energy need not preserve positivity.
    vel=s.symbols('vel',real=True)
    kk=vel**2/2
    composed=s.exp(1/(2*(1+(kk-1)**2)))*kk
    hessian=s.simplify(s.diff(composed,vel,2).subs(vel,s.sqrt(2)))
    exact('negative_composed_gate_Hessian_control',hessian+s.exp(s.Rational(1,2)))

    q1,q2,r,Z,p1,p2,pr,pZ=s.symbols('q1 q2 r Z p1 p2 pr pZ',real=True)
    mass,mu,lam,eta,M,om=s.symbols('mass mu lam eta M om',positive=True)
    R2=q1*q1+q2*q2
    V=mass*mass*R2/2+mu*mu*r*r/2+lam*(R2**2+r**4)/4-eta*R2*r*r/2
    exact('positive_quartic_decomposition',V-mass*mass*R2/2-mu*mu*r*r/2
          -(lam-eta)*(R2**2+r**4)/4-eta*(R2-r*r)**2/4)
    HD=(p1*p1+p2*p2+pr*pr)/2+V
    H=pZ*pZ/(2*M*M)+M*M*om*om*Z*Z/2+s.exp(-Z)*HD
    pairs=[(q1,p1),(q2,p2),(r,pr),(Z,pZ)]

    def pb(f,g):
        return sum(s.diff(f,q)*s.diff(g,p)-s.diff(f,p)*s.diff(g,q) for q,p in pairs)

    charge=q1*p2-q2*p1
    exact('homogeneous_energy_conservation',pb(H,H))
    exact('homogeneous_dark_proper_energy_conservation',pb(HD,H))
    exact('homogeneous_charge_conservation',pb(charge,H))
    exact('homogeneous_carrier_exchange',pb(s.exp(-Z)*HD,H)+(pZ/M**2)*s.exp(-Z)*HD)
    exact('homogeneous_gate_backreaction',-s.diff(H,Z)+M*M*om*om*Z-s.exp(-Z)*HD)
    exact('seedless_transition_is_invariant',s.diff(V,r).subs(r,0))
    exact('transition_curvature',s.diff(V,r,2).subs(r,0)-(mu*mu-eta*R2))

    pars={mass:1.,mu:.2,lam:2.,eta:1.,M:1.,om:3.}
    qvars=[q1,q2,r,Z,p1,p2,pr,pZ]
    vector=[s.diff(H,p) for _,p in pairs]+[-s.diff(H,q) for q,_ in pairs]
    rhs=s.lambdify((t,qvars),s.Matrix(vector).subs(pars),'numpy')
    hfun=s.lambdify((qvars,),H.subs(pars),'numpy')
    dfun=s.lambdify((qvars,),HD.subs(pars),'numpy')
    jfun=s.lambdify((qvars,),charge,'numpy')
    rows=[]
    for seed in [0.,.01]:
        init=np.array([1.4,0.,seed,0.,0.,.6,0.,0.])
        sol=solve_ivp(lambda tt,yy:np.asarray(rhs(tt,yy)).reshape(-1),[0,40],init,
                      method='DOP853',rtol=2e-11,atol=2e-12,t_eval=np.linspace(0,40,1001))
        assert sol.success,sol.message
        en=np.asarray(hfun(sol.y));de=np.asarray(dfun(sol.y));ch=np.asarray(jfun(sol.y))
        err=float(np.max(np.abs(en/en[0]-1)))
        derr=float(np.max(np.abs(de/de[0]-1)))
        jerr=float(np.max(np.abs(ch/ch[0]-1)))
        bound=float(np.sqrt(2*en[0])/3)
        assert max(err,derr,jerr)<1e-8,(err,derr,jerr)
        assert np.max(np.abs(sol.y[3]))<=bound*(1+1e-8)
        if seed==0:assert np.max(np.abs(sol.y[2]))==0
        else:assert np.max(np.abs(sol.y[2]))>.05
        rows.append({'seed':seed,'energy_error_relative':err,'proper_energy_error_relative':derr,
                     'charge_error_relative':jerr,'max_gate':float(np.max(np.abs(sol.y[3]))),
                     'gate_energy_bound':bound,'max_radiation_amplitude':float(np.max(np.abs(sol.y[2]))),
                     'final_radiation_amplitude':float(sol.y[2,-1]),
                     'initial_H':float(en[0]),'initial_HD':float(de[0]),'initial_charge':float(ch[0])})
    out={'checks':checks,'homogeneous_controls':rows,'passed':True,
         'software':{'python':sys.version,'sympy':s.__version__,'numpy':np.__version__,'scipy':scipy.__version__},
         'scope':'Exact identities and two 0<=t<=40 homogeneous classical-field trajectories; no fit',
         'non_claims':['No common gravitational constraint closure','No continuum global existence theorem',
                       'No automatic classical seed','No derived irreversible decay rate or kick',
                       'No particle population or transport calibration']}
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'exact_checks':len(checks),'homogeneous_controls':len(rows),'passed':True,'controls':rows}))


if __name__=='__main__':main()
