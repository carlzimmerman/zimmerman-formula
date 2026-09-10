#!/usr/bin/env python3
"""Evaluate the ACTUAL nonlinear lapse operator, then discretize it in flux form.

Samples are off-shell neighborhoods of an exact FLRW point, not constructed
inhomogeneous initial data. Mesh positivity is not a continuum enclosure.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import sympy as s
from derive import derive


def main():
    facts,ctx=derive();x=ctx['x'];z=ctx['z']
    U,d,q,A,m=s.symbols('U d q A m',positive=True)
    P=-U*s.log((U-2*d*z)/(U-2*d*q*q))/2
    ell=q*q*m/2
    W=U+2*d*ell*(s.sqrt(1+z/ell)-1)
    h=2/s.sqrt(15);qb=s.Rational(10,11);ab=s.Rational(1,10);mb=s.Rational(1,10)
    mn=s.Rational(109,1120);qn=-qb*mn/(1+mb);un=mn*qb*ab+mb*qn*ab-3*mb*qb*ab
    d_expr=A*U/(2*q*(q*A+U));ub=mb*qb*ab
    dn=(s.diff(d_expr,A)*(-3*A)+s.diff(d_expr,q)*s.Symbol('qn')+s.diff(d_expr,U)*s.Symbol('un')).subs(
        {A:ab,U:ub,q:qb,s.Symbol('qn'):qn,s.Symbol('un'):un})
    Pt=s.diff(P,U)*un*h+s.diff(P,d)*dn*h+s.diff(P,q)*qn*h
    params={U:ub,d:s.Rational(1,200),q:qb,m:mb}
    response={ctx['P']:P.subs(params),ctx['Pt']:Pt.subs(params),ctx['W']:W.subs(params)}
    def specialize(expr):
        substitutions={}
        for atom in expr.atoms(s.Subs):
            if isinstance(atom.expr,s.Derivative) and atom.expr.expr.func in response:
                order=sum(n for _,n in atom.expr.variable_count)
                substitutions[atom]=s.diff(response[atom.expr.expr.func],z,order).subs(z,atom.point[0])
        expr=expr.xreplace(substitutions)
        for fun,value in response.items():
            expr=expr.replace(lambda t:t.func==fun,lambda t:value.subs(z,t.args[0]))
        return expr.subs({ctx['M']:1,ctx['Lam']:s.Rational(7,10),ctx['V']:ub,ctx['Vt']:un*h})
    coefficients=[specialize(ctx['a2']),specialize(ctx['a0'])]
    eps=s.symbols('epsilon',real=True)
    af=eps*s.cos(x);bf=eps*s.sin(x)/2;cf=-af-bf
    momenta=[-2*h+eps*h*s.cos(x),-2*h+eps*h*s.sin(x),-2*h-eps*h*(s.cos(x)+s.sin(x))]
    fields=dict(zip(ctx['coords']+ctx['momenta']+[ctx['Q'],ctx['chi']],
                    [af,bf,cf]+momenta+[qb*(1+eps*s.cos(x)),eps*qb*s.sin(2*x)]))
    jets={}
    for f,value in fields.items():
        for order in range(3):jets[s.diff(f,x,order) if order else f]=s.diff(value,x,order)
    coefficients=[e.xreplace(jets).doit() for e in coefficients]
    fn=s.lambdify((x,eps),coefficients,'numpy',cse=True)
    rows=[]
    for amplitude in (0.,1e-4,1e-3,.01,.05):
        for n in (32,64,128):
            dx=2*np.pi/n;centers=np.arange(n)*dx;edges=centers+dx/2
            a2,a0=fn(centers,amplitude);edge,_=fn(edges,amplitude)
            a2=np.broadcast_to(a2,(n,));a0=np.broadcast_to(a0,(n,));edge=np.broadcast_to(edge,(n,))
            matrix=np.diag(-a0+(edge+np.roll(edge,1))/dx**2)
            for j in range(n):matrix[j,(j+1)%n]-=edge[j]/dx**2;matrix[(j+1)%n,j]-=edge[j]/dx**2
            eig=np.linalg.eigvalsh(matrix)
            if not np.all(np.isfinite(eig)):raise AssertionError('invalid numerical operator')
            rows.append(dict(amplitude=amplitude,mesh=n,min_principal=float(a2.min()),min_mass=float((-a0).min()),
                minimum_eigenvalue=float(eig[0]),three_lowest=eig[:3].tolist(),
                constant_mode_rayleigh=float(np.mean(-a0)),coercivity_sample=bool(a2.min()>0 and (-a0).min()>0),
                mesh_positive=bool(eig[0]>0)))
    # Independent homogeneous Fourier eigenvalues and a negative mass control.
    D=float(ub**2/(qb*ab+ub));B=float(ab/qb*(1+2/mb));mass=9*float(ab)**2*float(h)**2*.5/B
    hom=[r for r in rows if r['amplitude']==0]
    for r in hom:
        if abs(r['minimum_eigenvalue']-mass)>1e-10:raise AssertionError('homogeneous zero-mode gap mismatch')
    n=32;dx=2*np.pi/n;negative_control=-mass+4*D*np.sin(np.pi*np.arange(n)/n)**2/dx**2
    assert negative_control.min()<0
    # The finite-dimensional block identity is not an invented nonlinear rank.
    lam,g1,g2=s.symbols('Delta gamma xi',real=True)
    bracket=s.Matrix([[0,0,0,-lam],[0,0,-lam,g1],[0,lam,0,g2],[lam,-g1,-g2,0]])
    return dict(operator=facts,coefficient_model='exact symbolic operator specialized to the stationary action at a=1',
        grids=rows,homogeneous_mass=mass,homogeneous_gradient=D,negative_control_min=float(negative_control.min()),
        abstract_mode_bracket=str(bracket),abstract_mode_determinant=str(s.factor(bracket.det())),
        abstract_mode_rank=bracket.rank(),
        scope='Off-shell sampled neighborhood and periodic meshes; no certified continuum radius or inhomogeneous constraint-satisfying data',
        full_theory_status='OPEN')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--result-file',type=Path);a=p.parse_args()
    r=main()
    if a.result_file:a.result_file.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:r[k] for k in ('grids','homogeneous_mass','homogeneous_gradient','abstract_mode_determinant','full_theory_status')},indent=2))
