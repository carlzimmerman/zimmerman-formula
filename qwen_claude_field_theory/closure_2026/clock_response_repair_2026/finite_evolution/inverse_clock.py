#!/usr/bin/env python3
"""Constructive next check: free the clock history instead of tuning a fixed m.

At the r=0 boundary only, solve for dm/dln(a) that cancels BOTH Newtonian-gauge
pressure responses at finite k. A solution is a linear dust limit, not nonlinear
health or MOND completion. The boundary is deliberately not called a stable wave.
"""
import json
import sympy as s


def main():
    a,H,M,A,B,Q,k2,m=s.symbols('a H M2 A B Q k2 m',positive=True)
    mn=s.symbols('dm_dln_a',real=True)
    z, sig=s.symbols('z sigma',real=True)
    C=A/(2*Q*(1+m)); W=m*Q*A
    g=1/(Q*(1+m))
    rates={a:a*H,H:-(1+m)*Q*A/(2*M),A:-3*H*A,Q:-3*H*A/B,
           k2:-2*H*k2,m:H*mn}
    def dt(x):return sum(s.diff(x,v)*d for v,d in rates.items())
    L=-3*a**3*A+2*M*a**3*k2*g
    J=2*M*a**3*k2/Q; F=-J*H*g
    pz=L*sig; ps=J*z+F*sig
    ham=-3*a**3*A**2*sig**2/(4*M)+ps**2/(2*a**3*B)-a**3*M*k2*z**2+a**3*C*k2*sig**2-A*sig*pz/(2*M)
    zd=s.factor((s.diff(ham,sig)+dt(J)*z+dt(F)*sig)/(L-J))
    sd=s.factor((-s.diff(ham,z)-dt(L)*sig)/(L-J))
    alpha=(zd+A*sig/(2*M))/H
    sb=3*A/(2*M*k2)-g; beta=sb*sig
    psi=-z-H*beta
    phi=alpha+dt(sb)*sig+sb*sd
    if s.factor(phi-psi)!=0:raise AssertionError('independent potentials disagree')
    pressure=A*(sd-Q*alpha)-W*alpha+H*(mn*Q*A-3*(1+m)*A**2/B)*beta
    psi_N=s.factor((dt(psi)+s.diff(psi,z)*zd+s.diff(psi,sig)*sd)/H)
    transform=s.Matrix([[s.diff(psi,z),s.diff(psi,sig)],
                        [s.diff(psi_N,z),s.diff(psi_N,sig)]])
    row=s.Matrix([[s.diff(pressure,z),s.diff(pressure,sig)]])
    response=(row*transform.inv()).applyfunc(s.factor)
    equations=[s.fraction(v)[0] for v in response]
    solutions=s.solve(equations,mn,dict=True)
    verified=[]
    for sol in solutions:
        residual=[s.factor(v.subs(sol)) for v in response]
        if any(v!=0 for v in residual):raise AssertionError('inverse response residual')
        verified.append({str(k):str(v) for k,v in sol.items()})
    print(json.dumps(dict(pressure_response=[str(v) for v in response],
                         solved_clock_histories=verified,independent_no_slip_residual=str(s.factor(phi-psi)),
                         domain='r=0 boundary; timelike clock; generic nonsingular finite-k transformation',
                         non_claims=['No nonlinear health or strong-coupling certificate','No MOND closure or empirical fit']),indent=2))


if __name__=='__main__':main()
