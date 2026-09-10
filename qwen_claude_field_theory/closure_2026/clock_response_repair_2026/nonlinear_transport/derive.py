#!/usr/bin/env python3
"""Inhomogeneous principal symbol and Hamiltonian-transport gate for the SAME action.

Local inertial metric, timelike tau gradient, chi=Q t+g x at the event.
Explicit clock dependence contributes lower differential order and is frozen.
No nonlinear global DOF count or empirical rejection is inferred from this gate.
"""
import argparse
import json
from pathlib import Path
import sympy as s


def derive():
    Q,g,A,B,C,Cq,Cqq,U=s.symbols('Q g A B C Cq Cqq U',real=True)
    pt,px,st,sx,ep,pa,sa,v=s.symbols('pt px st sx ep pa sa v',real=True)
    norm=s.sqrt((1+ep*pt)**2-ep**2*px**2)
    qe=((1+ep*pt)*(Q+ep*st)-ep*px*(g+ep*sx))/norm
    ye=-(Q+ep*st)**2+(g+ep*sx)**2+qe**2
    density=U*norm+A*(qe-Q)+B*(qe-Q)**2/2-(C+Cq*(qe-Q)+Cqq*(qe-Q)**2/2)*ye
    l2=s.expand(s.diff(density,ep,2).subs(ep,0)/2)
    symbol=s.hessian(l2.subs({pt:-v*pa,px:pa,st:-v*sa,sx:sa}),(pa,sa))
    determinant=s.factor(symbol.det())
    # Independent gradient Hessian of the unexpanded density, not its Taylor polynomial.
    tt,tx,ct,cx=s.symbols('tau_t tau_x chi_t chi_x',real=True)
    wn=s.sqrt(tt**2-tx**2); qn=(tt*ct-tx*cx)/wn
    yn=-ct**2+cx**2+qn**2
    cn=(A+B*(qn-Q))**2/(2*(qn*(A+B*(qn-Q))+U))
    exact=U*wn+A*(qn-Q)+B*(qn-Q)**2/2-cn*yn
    cv=A**2/(2*(Q*A+U))
    def dq(x):return s.diff(x,Q)+B*s.diff(x,A)
    coeff={C:cv,Cq:dq(cv),Cqq:dq(dq(cv))}
    base={tt:1,tx:0,ct:Q,cx:g}
    hess=s.Matrix(4,4,lambda i,j:s.factor(s.diff(exact,(tt,tx,ct,cx)[i],(tt,tx,ct,cx)[j]).subs(base)))
    embedding=s.Matrix([[-v,0],[1,0],[0,-v],[0,1]])
    independent=embedding.T*hess*embedding
    assert all(s.factor(x)==0 for x in independent-symbol.subs(coeff))
    # Functional bracket of H[N]=integral N E(P,Y), P=F_Q, E=P Q-F.
    # The Legendre identities E_P=Q and E_Y=-F_Y follow by implicit differentiation.
    x=s.symbols('x',real=True)
    N=s.Function('N')(x); M=s.Function('M')(x)
    W=s.Function('W')(x); q=s.Function('q')(x); ch=s.Function('chi')(x)
    raw=-s.diff(N*W*s.diff(ch,x),x)*M*q+N*q*s.diff(M*W*s.diff(ch,x),x)
    assert s.simplify(raw-q*W*s.diff(ch,x)*(N*s.diff(M,x)-M*s.diff(N,x)))==0
    defect=-A+2*C*Q+Cq*g**2
    effective_B=B-Cqq*g**2
    cubic=s.Poly(determinant,v).coeff_monomial(v**3)
    assert s.factor(cubic-2*g*effective_B*defect)==0
    defect0=s.factor(defect.subs(g,0).subs(coeff))
    D=U-Q*A+2*C*Q**2
    assert s.factor(defect0+A*U/(Q*A+U))==0
    assert s.factor(D.subs(coeff)-U**2/(Q*A+U))==0
    # Rescale w=g v to isolate the singular fast root as g tends to zero.
    w=s.symbols('w',real=True)
    rescaled=s.cancel(g**2*determinant.subs(v,w/g).subs(coeff))
    leading=s.factor(s.limit(rescaled,g,0))
    leading_expected=s.factor(B*w**2*(2*defect0*w-D.subs(coeff)))
    assert s.factor(leading-leading_expected)==0
    wfast=-U/(2*A)
    assert s.factor(leading.subs(w,wfast))==0
    fast_derivative=s.factor(s.diff(leading,w).subs(w,wfast))
    # Exact event in the previously constructed profile: a=1, m=.1, R_Lambda=7, L=29.
    point={Q:s.Rational(10,11),A:s.Rational(1,10),B:s.Rational(726,725),U:s.Rational(1,110)}
    det_point=s.factor(determinant.subs(coeff).subs(point))
    rows=[]
    for ratio in (s.Rational(1,1000),s.Rational(1,100),s.Rational(1,10)):
        gv=ratio*point[Q]
        poly=s.Poly(det_point.subs(g,gv),v)
        rows.append(dict(gradient_over_Q=str(ratio),roots=[str(r) for r in s.nroots(poly,n=40,maxsteps=200)],
                         effective_B=str(effective_B.subs(coeff).subs(point).subs(g,gv)),
                         clock_and_chi_timelike=bool(gv**2<point[Q]**2)))
    witness=s.Poly(det_point.subs(g,point[Q]/100),v).clear_denoms()[1].primitive()[1]
    if witness.LC()<0:witness=-witness
    assert witness.eval(-6)<0<witness.eval(-5)
    # Actual transport principal matrix in the real (cos,sin) basis.
    j,k=s.symbols('j k',real=True)
    transport=s.Matrix([[0,2*j*k],[-2*j*k,0]])
    return dict(local_quadratic=str(l2),principal_symbol=str(symbol),determinant=str(determinant),
        independently_expanded_gradient_Hessian_agrees=True,velocity_Hessian_rank=s.hessian(l2,(pt,st)).rank(),
        principal_polynomial_degree=s.Poly(determinant,v).degree(),cubic_coefficient=str(s.factor(cubic)),
        homogeneous_polynomial=s.factor(determinant.subs(g,0).subs(coeff)).__str__(),
        Hamiltonian_defect_at_Y0=str(defect0),rescaled_limit=str(leading),
        fast_root_scaled=str(wfast),fast_root_derivative=str(fast_derivative),
        rational_witness_coefficients=[str(c) for c in witness.all_coeffs()],
        witness_values={'minus6':str(witness.eval(-6)),'minus5':str(witness.eval(-5))},numerical_checks=rows,
        transport_symbol=str(transport),transport_rank=transport.rank(),
        transverse_or_zero_symbol_rank=transport.subs(k,0).rank(),
        scope='Frozen local principal characteristic, exact action coefficients; no full nonlinear Dirac count or global background-existence theorem',
        full_theory_status='OPEN; this explicit branch fails the unrestricted metric-cone principal-symbol gate')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--result-file',type=Path);a=p.parse_args()
    result=derive();encoded=json.dumps(result,indent=2)+'\n'
    if a.result_file:a.result_file.write_text(encoded)
    print(encoded)
