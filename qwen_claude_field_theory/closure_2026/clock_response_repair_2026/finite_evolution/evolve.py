#!/usr/bin/env python3
"""Finite-k evolution from the coupled-clock quadratic Hamiltonian.

No radiation/baryon hierarchy or empirical likelihood: a sector transfer test,
starting with imposed constant Newtonian potential at a=1e-3, not primordial ICs.
"""
import json
import math
import sys
import sympy as s
import numpy as np
from scipy.integrate import solve_ivp


def derive():
    a,H,M,A,B,Q,k2,m,r=s.symbols('a H M2 A B Q k2 m r',positive=True)
    z, sig=s.symbols('z sigma',real=True)
    K3=s.symbols('KQQQ',real=True)
    # All coefficients belong to the same repaired action/background family.
    den=1+m-r
    C=A*(1+r*(m-1))/(2*Q*den)
    W=m*Q*A
    b_over_U=(1-r)/(Q*den)
    rates={a:a*H,H:-(1+m)*Q*A/(2*M),A:-3*H*A,Q:-3*H*A/B,
           B:-3*H*A*K3/B,k2:-2*H*k2,r:3*H*r*(1-r)}
    def dt(x):return sum(s.diff(x,v)*rate for v,rate in rates.items())
    def equal(x,y):return s.factor(x-y)==0
    checks={}
    def check(name,yes):
        checks[name]=bool(yes)
        if not checks[name]:raise AssertionError(name)

    # Momentum and clock constraints solve p_z=L sigma, p_sigma=J z+F sigma.
    L=-3*a**3*A+2*M*a**3*k2*b_over_U
    J=2*M*a**3*k2/Q
    F=-J*H*b_over_U
    pz=L*sig; ps=J*z+F*sig
    h0=-3*a**3*A**2*sig**2/(4*M)+ps**2/(2*a**3*B)-a**3*M*k2*z**2 \
        +a**3*C*k2*sig**2-A*sig*pz/(2*M)
    omega=s.factor(L-J)
    zd=s.factor((s.diff(h0,sig)+dt(J)*z+dt(F)*sig)/omega)
    sd=s.factor((-s.diff(h0,z)-dt(L)*sig)/omega)
    alpha=s.factor((zd+A*sig/(2*M))/H)
    shift_coeff=3*A/(2*M*k2)-b_over_U
    beta=shift_coeff*sig
    # Independent canonical equations, not just the reduced first-order action.
    check('chi_momentum_equation',equal(sd,ps/(a**3*B)+Q*alpha))
    check('z_momentum_preservation',equal(dt(L)*sig+L*sd,2*a**3*M*k2*(z+alpha)))
    psdot=dt(J)*z+J*zd+dt(F)*sig+F*sd
    expected_psdot=3*a**3*A**2*sig/(2*M)-2*a**3*C*k2*sig+A*pz/(2*M)-3*a**3*H*A*alpha
    check('chi_momentum_preservation',equal(psdot,expected_psdot))
    # Both potentials are reconstructed separately in Newtonian gauge.
    psi=-z-H*beta
    phi=alpha+dt(shift_coeff)*sig+shift_coeff*sd
    check('independently_derived_linear_potentials_agree',equal(phi,psi))
    delta_rho=Q*B*(sd-Q*alpha)
    check('Einstein_comoving_Poisson_identity',equal(delta_rho+3*H*A*sig,-2*M*k2*psi))

    # Evolve dimensionless variables y=(z,w), w=H sigma/Q, with x=ln a.
    w=s.symbols('w',real=True)
    flow=s.Matrix([zd/H,sd/Q+(rates[H]/H**2-rates[Q]/(H*Q))*H*sig/Q]).subs(sig,Q*w/H)
    matrix=s.simplify(flow.jacobian([z,w]))
    prow=s.Matrix([[s.diff(psi,z),s.diff(psi,sig)*Q/H]])
    pder=prow.applyfunc(lambda v:dt(v)/H)+prow*matrix
    pder=pder.applyfunc(s.factor)
    transform=prow.col_join(pder)
    # Evolve the actual potential, avoiding the severely non-normal (z,w) system.
    # The pressure expression is independently reconstructed from the same matter action.
    pressure=A*(sd-Q*alpha)-W*alpha-3*H*(1+m)*A**2*beta/B
    pressure_row=s.Matrix([[s.diff(pressure,z),s.diff(pressure,sig)*Q/H]])
    physical_pressure=(pressure_row*transform.inv()).applyfunc(s.factor)
    hd_over_H2=rates[H]/H**2
    physical=s.Matrix([[0,1],[s.factor(physical_pressure[0]/(2*M*H**2)-3-2*hd_over_H2),
                              s.factor(physical_pressure[1]/(2*M*H**2)-4-hd_over_H2)]])
    # This verifies the pressure-based evolution against the original canonical equations.
    second=(pder.applyfunc(lambda v:dt(v)/H)+pder*matrix)
    residual=second-physical[1:2,:]*transform
    check('pressure_trace_matches_canonical_evolution',all(equal(v,0) for v in residual))
    check('no_unprovided_KQQQ_in_numerical_coefficients',K3 not in physical.free_symbols)
    # Pressureless, vanishing-clock-energy limit; m scales with c_ad^2.
    c, eta=s.symbols('c eta',positive=True)
    cold_matrix=matrix.subs({B:A/(Q*c),m:eta*c}).applyfunc(lambda v:s.simplify(s.limit(v,c,0)))
    cold_psi=prow.subs(m,0)
    cold_pd=s.simplify((cold_psi.applyfunc(lambda v:dt(v)/H)+cold_psi*cold_matrix).subs(m,0))
    # A constant-potential mode must exist in Einstein-de Sitter. This control is
    # derived from the limit, not used to assign the numerical transfer result.
    eds_matrix=s.simplify(cold_matrix.subs(A,3*M*H**2/Q))
    eds_psi=s.simplify(cold_psi.subs(A,3*M*H**2/Q))
    check('cold_EdS_constant_mode_exists',s.factor(eds_matrix.det())==0)
    # Return exact expressions and executable coefficient maps.
    args=(a,H,M,A,B,Q,k2,m,r)
    generic=s.lambdify(args,(physical,prow,pder),'numpy',cse=True)
    # Specialize the exact r=1 control symbolically. Evaluating the unspecialized
    # rational expression there loses powers of tiny m to floating cancellation.
    li=s.lambdify(args,tuple(v.subs(r,1).applyfunc(s.factor) for v in (physical,prow,pder)),'numpy',cse=True)
    def numeric(*values):return li(*values) if values[-1]==1. else generic(*values)
    return dict(checks=checks,flow=str(matrix),psi=str(psi),phi=str(phi),
                symplectic=str(omega),potential_evolution=str(physical),cold_matrix=str(eds_matrix)),numeric


def background(a,m):
    M,Q0,Z,K2,I,Lambda,At=1.,1.,1e-3,0.5,0.1,0.7,1e-4
    A=I/a**3
    zz=math.asinh(A/(2*K2*Z))
    Q=Q0+Z*zz
    B=2*K2*math.cosh(zz)
    # sinh^2/(cosh+1) prevents loss of the small late-time cosh-1 value.
    K=2*K2*Z**2*math.sinh(zz)**2/(math.cosh(zz)+1)
    rho=Q*A-K
    H=math.sqrt(Lambda/3+(1+m)*rho/(3*M))
    r=At/(At+A)
    e=-3*A/B+m*Q**2*A/(2*M*H**2)
    return H,M,A,B,Q,r,e,rho


def evolve(numeric,m,k_over_H0,arm='repair',method='DOP853',rtol=2e-9):
    ai=1e-3
    H0=background(1.,m)[0]
    k=k_over_H0*H0
    def coefficients(x):
        a=math.exp(x)
        H,M,A,B,Q,r,e,rho=background(a,m)
        if e>=0:raise ValueError('background leaves the verified e<0 kinetic region')
        if arm=='LI':r=1.
        mat,pr,pd=numeric(a,H,M,A,B,Q,(k/a)**2,m,r)
        return np.asarray(mat,dtype=float),np.asarray(pr,dtype=float).ravel(),np.asarray(pd,dtype=float).ravel()
    x0=math.log(ai)
    mat,pr,pd=coefficients(x0)
    initial_matrix=np.vstack((pr,pd))
    initial=np.array([-1.,0.])
    grid=np.linspace(x0,0,141)
    sol=solve_ivp(lambda x,y:coefficients(x)[0]@y,(x0,0),initial,method=method,
                  t_eval=grid,rtol=rtol,atol=rtol*1e-3,max_step=0.04)
    if not sol.success:raise RuntimeError(sol.message)
    values=sol.y[0]
    return dict(m=m,k_over_H0=k_over_H0,arm=arm,method=method,rtol=rtol,
                initial_condition='Psi=-1 and dPsi/dln(a)=0 at a=0.001; not primordial adiabatic ICs',
                initial_matrix_condition=float(np.linalg.cond(initial_matrix)),
                potential_final=float(values[-1]),potential_max_abs=float(np.max(np.abs(values))),
                nfev=sol.nfev,curve=values.tolist())


def reference(m):
    # Comparison only: GR pressureless matter+Lambda, matched to the present H.
    # This is not substituted into the candidate evolution equations.
    rho0=background(1.,m)[-1]
    def rhs(x,y):
        matter=(1+m)*rho0*math.exp(-3*x)
        Hp=-1.5*matter/(0.7+matter)
        return [y[1],-(4+Hp)*y[1]-(3+2*Hp)*y[0]]
    sol=solve_ivp(rhs,(math.log(.001),0),[-1.,0.],rtol=1e-11,atol=1e-13,max_step=.02)
    if not sol.success:raise RuntimeError(sol.message)
    return float(sol.y[0,-1])


def main():
    derivation,numeric=derive()
    rows=[]
    for m in (1e-5,1e-3,1.9e-3):
        ref=reference(m)
        for arm in ('repair','LI'):
            for kh in (1.,10.,30.,100.,300.,1000.):
                row=evolve(numeric,m,kh,arm)
                row['reference_potential_final']=ref
                row['potential_ratio_to_matched_GR_dust']=row['potential_final']/ref
                rows.append(row)
                print(json.dumps(dict(m=m,k_over_H0=kh,arm=arm,potential_ratio=row['potential_ratio_to_matched_GR_dust'],nfev=row['nfev'])),file=sys.stderr,flush=True)
    # Cross-method and tighter-tolerance checks on selected long/intermediate/short modes.
    convergence=[]
    for m,kh in ((1e-5,1.),(1e-5,1000.),(1.9e-3,100.)):
        nominal=next(v for v in rows if v['m']==m and v['k_over_H0']==kh and v['arm']=='repair')
        test=evolve(numeric,m,kh,method='Radau',rtol=2e-10)
        err=max(abs(x-y) for x,y in zip(test['curve'],nominal['curve']))
        if err>2e-6*max(1.,test['potential_max_abs']):raise AssertionError('cross-method convergence')
        convergence.append(dict(m=m,k_over_H0=kh,max_abs_potential_difference=err))
    print(json.dumps(dict(derivation=derivation,rows=rows,convergence=convergence,
        scope='Post-initial-time sector evolution only; no radiation, baryons, MOND source or CMB likelihood',
        full_theory_status='OPEN'),indent=2))


if __name__=='__main__':main()
