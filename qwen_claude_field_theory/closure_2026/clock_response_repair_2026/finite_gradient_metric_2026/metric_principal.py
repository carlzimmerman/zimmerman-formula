#!/usr/bin/env python3
"""Einstein plus two-field principal audit, gamma=0; no assigned ranks.

The geometric principal implication needs a regular on-shell background;
these exact local jets do not construct that background. See REPORT.md.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import sympy as s


def symmetric_variables():
    pairs=[(i,j) for i in range(4) for j in range(i,4)]
    variables=s.symbols(' '.join(f'h{i}{j}' for i,j in pairs),real=True)
    matrix=s.zeros(4)
    for (i,j),value in zip(pairs,variables):
        matrix[i,j]=matrix[j,i]=value
    return pairs,variables,matrix


@lru_cache(maxsize=1)
def einstein():
    c=s.symbols('c',real=True)
    eta=s.diag(-1,1,1,1);xi=s.Matrix([-c,1,0,0]);up=eta*xi
    norm=(xi.T*up)[0]
    pairs,variables,h=symmetric_variables()
    trace=s.trace(eta*h)
    # Linearized Levi-Civita connection -> Ricci -> Einstein; d_mu maps to xi_mu.
    connection=[[[sum(eta[a,d]*(xi[b]*h[d,j]+xi[j]*h[d,b]-xi[d]*h[b,j])
                         for d in range(4))/2 for j in range(4)]
                  for b in range(4)] for a in range(4)]
    Ricci=s.Matrix(4,4,lambda a,b:sum(xi[d]*connection[d][a][b]-
                                      xi[b]*connection[d][a][d] for d in range(4)))
    Einstein=(Ricci-eta*s.trace(eta*Ricci)/2).applyfunc(s.expand)
    E=s.Matrix([Einstein[i,j] for i,j in pairs]).jacobian(variables)
    epsilon=s.Matrix(s.symbols('epsilon0:4',real=True))
    gauge=xi*epsilon.T+epsilon*xi.T
    gauge_map=s.Matrix([gauge[i,j] for i,j in pairs]).jacobian(epsilon)
    constraint=h*up-xi*trace/2
    reduced=(Einstein-(xi*constraint.T+constraint*xi.T)/2+
             eta*(up.T*constraint)[0]/2).applyfunc(s.expand)
    harmonic_identity=(reduced+norm*(h-eta*trace/2)/2).applyfunc(s.expand)
    reduced_matrix=s.Matrix([reduced[i,j] for i,j in pairs]).jacobian(variables)
    return dict(c=c,xi=xi,xi_squared=norm,matrix=E,gauge_map=gauge_map,
                gauge_identity=(E*gauge_map).applyfunc(s.expand),
                harmonic_identity=harmonic_identity,reduced_matrix=reduced_matrix,
                reduced_determinant=s.factor(reduced_matrix.det()))


def metric_ranks():
    r=einstein();out={}
    for label,value in [('spacelike',0),('null',1),('timelike',2)]:
        E=r['matrix'].subs(r['c'],value)
        gauge=r['gauge_map'].subs(r['c'],value)
        rank=E.rank();gauge_rank=gauge.rank()
        out[label]=dict(c=value,einstein_rank=rank,gauge_rank=gauge_rank,
                        kernel_dimension=E.cols-rank,
                        kernel_minus_gauge=E.cols-rank-gauge_rank)
    return out


@lru_cache(maxsize=1)
def matter():
    c,Lambda=s.symbols('c Lambda',real=True)
    Q,b,d,s0=s.symbols('Q b d s0',real=True,nonzero=True)
    # b is the gradient component along k, d its transverse component.
    P,V,PX,PXX,W,WY,WYY=s.symbols('P V PX PXX W WY WYY',real=True)
    sigma,pi=s.symbols('sigma pi',real=True)
    eta=s.diag(-1,1,1,1);xi=s.Matrix([-c,1,0,0])
    pairs,hvars,h=symmetric_variables()
    inv1=-eta*h*eta;inv2=eta*h*eta*h*eta
    u=s.Matrix([s0,0,0,0]);v=s.Matrix([Q,b,d,0])
    du=Lambda*xi*pi;dv=Lambda*xi*sigma
    dot=lambda x,M,y:(x.T*M*y)[0]
    A1=-dot(u,inv1,u)-2*dot(u,eta,du)
    A2=-dot(u,inv2,u)-2*dot(u,inv1,du)-dot(du,eta,du)
    s1=A1/(2*s0);s2=A2/(2*s0)-A1**2/(8*s0**3)
    X1=-dot(v,inv1,v)-2*dot(v,eta,dv)
    X2=-dot(v,inv2,v)-2*dot(v,inv1,dv)-dot(dv,eta,dv)
    D0=-s0*Q
    D1=dot(u,inv1,v)+dot(du,eta,v)+dot(u,eta,dv)
    D2=dot(u,inv2,v)+dot(du,inv1,v)+dot(u,inv1,dv)+dot(du,eta,dv)
    Y1=2*D0*D1/s0**2-D0**2*A1/s0**4-X1
    Y2=(D1**2+2*D0*D2)/s0**2-2*D0*D1*A1/s0**4+\
       D0**2*(A1**2/s0**6-A2/s0**4)-X2
    tr=s.trace(eta*h)
    vol1=tr/2;vol2=tr**2/8-s.trace(eta*h*eta*h)/4
    L0=P-V+s0*W
    L1=PX*X1+s1*W+s0*WY*Y1
    L2=PX*X2+PXX*X1**2/2+s2*W+s1*WY*Y1+s0*(WY*Y2+WYY*Y1**2/2)
    density=s.Poly(s.expand(L2+vol1*L1+vol2*L0),Lambda)
    coeffs={i:density.nth(i) for i in range(density.degree()+1)}
    scalars=[sigma,pi]
    degrees={'metric':-1,'mixed':-1,'scalar':-1}
    for i,value in coeffs.items():
        blocks={'metric':s.hessian(value,hvars),
                'mixed':s.Matrix([s.diff(value,x) for x in hvars]).jacobian(scalars),
                'scalar':s.hessian(value,scalars)}
        for key,matrix in blocks.items():
            if any(s.expand(entry)!=0 for entry in matrix):degrees[key]=i
    leading=coeffs[2]
    scalar=s.hessian(leading,scalars).applyfunc(s.factor)
    C=WY+2*b*b*WYY;F=W-2*Q*Q*C-2*b*b*WY;K=2*PX+4*Q*Q*PXX
    expected=s.Matrix([[K*c*c+8*Q*PXX*b*c-2*PX+4*PXX*b*b+2*s0*C,-2*Q*C],
                       [-2*Q*C,-F/s0]])
    return dict(block_degrees=degrees,leading_metric_free=not any(leading.has(x) for x in hvars),
                scalar_matrix=scalar,scalar_difference=(scalar-expected).applyfunc(s.factor),
                scalar_determinant=s.factor(scalar.det()),
                full_reduced_determinant=s.factor(einstein()['reduced_determinant']*scalar.det()),
                symbols=locals())


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path,required=True)
    args=parser.parse_args();E=einstein();M=matter()
    checks=dict(pure_gauge_annihilated=E['gauge_identity']==s.zeros(10,4),
                harmonic_identity=E['harmonic_identity']==s.zeros(4),
                no_leading_metric_matter_mixing=M['leading_metric_free'],
                previous_scalar_symbol_recovered=M['scalar_difference']==s.zeros(2))
    if not all(checks.values()):raise AssertionError(checks)
    result=dict(checks=checks,computed_metric_ranks=metric_ranks(),
                differential_block_degrees=M['block_degrees'],
                metric_matrix=str(E['matrix']),gauge_map=str(E['gauge_map']),
                reduced_metric_determinant=str(E['reduced_determinant']),
                scalar_matrix=str(M['scalar_matrix']),
                full_reduced_determinant=str(M['full_reduced_determinant']),
                scope='gamma=0 highest differential order; locally orthonormal frame, nonzero spatial covector; two scalar fields and all ten metric components',
                non_claims=['No existence of an on-shell finite-gradient background established',
                            'No nonlinear Dirac closure or finite-frequency stability certificate',
                            'k=0, F=0, null/critical coincidences require separate reductions',
                            'Metric rank-minus-gauge test is a linear principal benchmark, not full gravitational DOF counting'])
    args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if 'matrix' not in k and 'determinant' not in k},indent=2))


if __name__=='__main__':main()
