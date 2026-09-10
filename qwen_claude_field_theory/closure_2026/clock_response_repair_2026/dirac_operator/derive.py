#!/usr/bin/env python3
"""Exact plane-symmetric functional bracket for the lapse operator.

The metric retains three diagonal components depending on x. This checks the
full variable-coefficient longitudinal operator, not a 3D nonlinear DOF count.
P(X,tau), W(Y,tau) are arbitrary smooth functions in the symbolic calculation.
"""
import argparse
import json
from pathlib import Path
import sympy as s


def derive():
    x,z=s.symbols('x z',real=True)
    a,b,c,pa,pb,pc,Q,chi,N=[s.Function(k)(x) for k in ('a','b','c','pa','pb','pc','Q','chi','N')]
    M,Lam,V,Vt=s.symbols('M2 Lambda V Vtau',real=True)
    vol=s.exp(a+b+c);hxx=s.exp(-2*a);Y=hxx*s.diff(chi,x)**2;X=Q*Q-Y
    P=s.Function('P');W=s.Function('W');Pt=s.Function('Pt')
    pval=P(X);px=s.diff(P(z),z).subs(z,X);pxx=s.diff(P(z),z,2).subs(z,X)
    w=W(Y);wy=s.diff(W(z),z).subs(z,Y);wyy=s.diff(W(z),z,2).subs(z,Y)
    momenta=[pa,pb,pc];coords=[a,b,c];psum=sum(momenta)
    kin=(sum(p*p for p in momenta)-psum**2/2)/(2*M*vol)
    # Compute the spatial Ricci tensor from Christoffels; no prescribed curvature result.
    metric=s.diag(s.exp(2*a),s.exp(2*b),s.exp(2*c));inv=metric.inv()
    def D(f,i):return s.diff(f,x) if i==0 else s.S.Zero
    G=[[[sum(inv[i,l]*(D(metric[l,k],j)+D(metric[l,j],k)-D(metric[j,k],l))/2 for l in range(3))
          for k in range(3)] for j in range(3)] for i in range(3)]
    Ric=s.Matrix(3,3,lambda i,j:s.simplify(sum(D(G[k][i][j],k)-D(G[k][i][k],j)
                 +sum(G[k][i][j]*G[l][k][l]-G[l][i][k]*G[k][j][l] for l in range(3)) for k in range(3))))
    curvature=s.simplify(s.trace(inv*Ric));pot=-M*vol*(curvature-2*Lam)/2
    def EL(expr,f):
        return s.diff(expr,f)-s.diff(s.diff(expr,s.diff(f,x)),x)+s.diff(s.diff(expr,s.diff(f,x,2)),x,2)
    qflow=[s.diff(kin,p)*N for p in momenta]
    pflow=[-EL(N*(kin+pot),f)+N*vol*(pval-V+(2*px*Y if i==0 else 0)) for i,f in enumerate(coords)]
    chi_flow=N*Q
    yflow=-2*Y*qflow[0]+2*hxx*s.diff(chi,x)*s.diff(chi_flow,x)
    density_flow=2*s.diff(N*vol*px*hxx*s.diff(chi,x),x)/vol
    qQflow=(density_flow-2*Q*px*sum(qflow)+2*Q*pxx*yflow)/(2*px+4*Q*Q*pxx)
    qQflow=s.collect(s.expand(qQflow),[N,s.diff(N,x)])
    # Reconstruct the tertiary directly as partial_tau C + {C,H0}.
    h0=-vol*w
    tertiary=vol*(Vt-Pt(X))-sum(qflow[i].subs(N,1)*EL(h0,coords[i]) for i in range(3))-Q*EL(h0,chi)
    tertiary=s.expand(tertiary)
    expected=vol*(Vt-Pt(X))-w*psum/(2*M)-2*wy*Y*(pa-psum/2)/M-2*Q*s.diff(vol*wy*hxx*s.diff(chi,x),x)
    assert s.simplify(tertiary-expected)==0
    flows=dict(zip(coords+momenta+[Q,chi],qflow+pflow+[qQflow,chi_flow]))
    # Fréchet variation of the actual tertiary, retaining every spatial jet.
    delta=s.S.Zero
    for f,df in flows.items():
        for order in range(3):
            jet=f if order==0 else s.diff(f,x,order)
            if tertiary.has(jet):delta+=s.diff(tertiary,jet)*s.diff(df,x,order)
    delta=s.expand(delta)
    a2=s.simplify(s.diff(delta,s.diff(N,x,2)))
    expected2=vol*hxx*(w-2*Q*Q*wy-2*Y*wy-4*Q*Q*Y*wyy)
    mismatch=s.factor((a2-expected2).rewrite(s.exp))
    if mismatch!=0:raise AssertionError('principal mismatch: '+str(mismatch))
    a1=s.simplify(s.diff(delta,s.diff(N,x)))
    a0=s.simplify(s.diff(delta,N))
    assert not any(v.has(N) for v in (a2,a1,a0))
    assert s.simplify((a2-expected2).rewrite(s.exp))==0
    assert s.simplify((a1-s.diff(a2,x)).rewrite(s.exp))==0
    assert s.simplify((delta-a2*s.diff(N,x,2)-a1*s.diff(N,x)-a0*N).rewrite(s.exp))==0
    # Independent geometric construction of the full zeroth-order coefficient.
    kval=[v.subs(N,1) for v in qflow];ktr=sum(kval);Z=kval[0]*Y
    dy=yflow.subs(N,1).doit();dq=qQflow.subs(N,1).doit();dx=2*Q*dq-dy
    rho=2*Q*Q*px-pval+V
    constraint=curvature+ktr*ktr-sum(v*v for v in kval)-2*rho/M-2*Lam
    dk=-curvature-ktr*ktr+(px*(3*Q*Q-Y)-3*pval+3*V)/M+3*Lam+3*constraint/4
    dz=-Ric[0,0]*hxx*Y-ktr*Z-2*kval[0]**2*Y+Y*(px*(Q*Q+Y)-pval+V)/M+Lam*Y \
       +2*kval[0]*hxx*s.diff(chi,x)*s.diff(Q,x)+Y*constraint/4
    J=s.diff(vol*wy*hxx*s.diff(chi,x),x)/vol
    dj=s.diff(vol*(wyy*dy*hxx*s.diff(chi,x)+wy*hxx*s.diff(Q,x)
                   -2*wy*kval[0]*hxx*s.diff(chi,x)),x)/vol+wy*hxx*s.diff(chi,x)*s.diff(ktr,x)
    geometric=vol*(ktr*tertiary/vol-s.diff(Pt(z),z).subs(z,X)*dx+wy*dy*ktr+w*dk
                   -2*wyy*dy*Z-2*wy*dz-2*dq*J-2*Q*dj)
    assert s.simplify((a0-geometric).rewrite(s.exp))==0
    # Homogeneous mode comes from the full operator, not from dividing by k.
    scale,hh,qa,aa,bb,uu=s.symbols('scale H q A B U',positive=True)
    qdot=s.symbols('qdot',real=True)
    mapping=dict(zip(coords,[s.log(scale)]*3))
    mapping.update(dict(zip(momenta,[-2*M*scale**3*hh]*3)));mapping.update({Q:qa,chi:0})
    hom0=a0.subs(mapping,simultaneous=True).doit()
    hom2=a2.subs(mapping,simultaneous=True).doit()
    # SymPy may alpha-rename Subs differentiation variables during simplification.
    # Match function and derivative order, not the spelling of its bound dummy.
    derivative_values={(P,1):aa/(2*qa),(P,2):(bb-aa/qa)/(4*qa**2),
                       (Pt,1):(-3*hh*aa-bb*qdot)/(2*qa),
                       (W,1):aa/(2*qa)-aa*aa/(2*(qa*aa+uu))}
    derivatives={}
    for atom in (hom0+hom2).atoms(s.Subs):
        if isinstance(atom.expr,s.Derivative):
            key=(atom.expr.expr.func,sum(n for _,n in atom.expr.variable_count))
            if key not in derivative_values:raise AssertionError('unprovided homogeneous derivative: '+str(atom))
            derivatives[atom]=derivative_values[key]
    background={P(qa**2):0,Pt(qa**2):-aa*qdot,W(0):uu,V:uu,
                Vt:-aa*qdot-3*hh*uu,Lam:3*hh**2-(qa*aa+uu)/M}
    hom0=s.simplify(hom0.xreplace(derivatives).subs(background))
    hom2=s.simplify(hom2.xreplace(derivatives).subs(background))
    ee=qdot/hh+qa*uu/(2*M*hh**2);ff=bb*ee+3*aa
    mismatch0=s.factor(hom0+3*scale**3*aa*hh**2*ff/bb)
    if mismatch0!=0:raise AssertionError('homogeneous mismatch: '+str(mismatch0))
    assert s.simplify(hom2-scale*uu**2/(qa*aa+uu))==0
    return (dict(spatial_curvature=str(curvature),tertiary=str(s.factor(expected)),
        lapse_second_derivative=str(s.factor(a2)),lapse_first_derivative=str(a1),lapse_mass=str(a0),
        functional_tertiary_matches=True,principal_matches_covariant_clock_symbol=True,
        self_adjoint_first_derivative_identity=True,complete_second_order_operator=True,
        independent_geometric_mass_agrees=True,homogeneous_mass=str(s.factor(hom0)),
        homogeneous_gradient=str(s.factor(hom2)),homogeneous_mass_matches_entropy_chain=True,
        scope='Exact plane-symmetric variable-coefficient operator from functional canonical variations; not all 3D sectors'),
        dict(a2=a2,a0=a0,coords=coords,momenta=momenta,Q=Q,chi=chi,x=x,M=M,Lam=Lam,V=V,Vt=Vt,P=P,Pt=Pt,W=W,z=z))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--result-file',type=Path);a=p.parse_args()
    result,_=derive();data=json.dumps(result,indent=2)+'\n'
    if a.result_file:a.result_file.write_text(data)
    print(json.dumps({k:v for k,v in result.items() if not isinstance(v,str) or k=='scope'}))
