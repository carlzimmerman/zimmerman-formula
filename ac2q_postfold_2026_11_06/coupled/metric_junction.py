"""PF04: direct 4D plane-metric reduction and necessary junction identities."""
import argparse
import json
from pathlib import Path
import sympy as S


def geometric_checks():
    t,x,y,z=S.symbols('t x y z',real=True); coords=(t,x,y,z)
    a=S.Function('alpha')(t,x); b=S.Function('beta')(t,x)
    h=S.Function('theta')(t,x); P=S.Function('P')(t,x)
    g=S.diag(-S.exp(2*a),S.exp(2*a),S.exp(2*b),S.exp(2*b)); inv=g.inv()
    Gamma=[[[S.simplify(sum(inv[i,l]*(S.diff(g[l,j],coords[k])+S.diff(g[l,k],coords[j])-S.diff(g[j,k],coords[l])) for l in range(4))/2)
             for k in range(4)] for j in range(4)] for i in range(4)]
    Ric=S.zeros(4)
    for i in range(4):
        for j in range(4):
            Ric[i,j]=S.simplify(sum(S.diff(Gamma[k][i][j],coords[k])-S.diff(Gamma[k][i][k],coords[j])+
                sum(Gamma[k][i][j]*Gamma[l][k][l]-Gamma[l][i][k]*Gamma[k][j][l] for l in range(4)) for k in range(4)))
    R=S.simplify(sum(inv[i,j]*Ric[i,j] for i in range(4) for j in range(4)))
    box=lambda f:-S.diff(f,t,2)+S.diff(f,x,2)
    dot=lambda f,q:-S.diff(f,t)*S.diff(q,t)+S.diff(f,x)*S.diff(q,x)
    expected_R=S.exp(-2*a)*(-2*box(a)-4*box(b)-6*dot(b,b))
    raw=S.exp(2*a+2*b)*R/2
    reduced=S.exp(2*b)*(2*dot(a,b)+dot(b,b))
    divergence=-S.diff(S.exp(2*b)*(S.diff(a,t)+2*S.diff(b,t)),t)+S.diff(S.exp(2*b)*(S.diff(a,x)+2*S.diff(b,x)),x)
    n=S.exp(-a)*S.Matrix([S.cosh(h),S.sinh(h),0,0])
    e=S.exp(-a)*S.Matrix([S.sinh(h),S.cosh(h),0,0])
    pv=P*e; pcov=g*pv
    nabP=S.Matrix(4,4,lambda i,j:S.diff(pcov[j],coords[i])-sum(Gamma[k][i][j]*pcov[k] for k in range(4)))
    proj=inv+n*n.T
    D=S.simplify(S.trigsimp(sum(proj[i,j]*nabP[i,j] for i in range(4) for j in range(4))))
    expected_D=S.exp(-a)*(S.sinh(h)*S.diff(P,t)+S.cosh(h)*S.diff(P,x)+2*P*(S.sinh(h)*S.diff(b,t)+S.cosh(h)*S.diff(b,x)))
    acc=S.Matrix([sum(n[j]*(S.diff(n[i],coords[j])+sum(Gamma[i][j][k]*n[k] for k in range(4))) for j in range(4)) for i in range(4)])
    PA=S.simplify(S.trigsimp((pv.T*g*acc)[0]))
    expected_PA=P*S.exp(-a)*(S.cosh(h)*S.diff(h,t)+S.sinh(h)*S.diff(h,x)+S.sinh(h)*S.diff(a,t)+S.cosh(h)*S.diff(a,x))
    checks={'four_dimensional_R':S.simplify(R-expected_R)==0,
            'Einstein_integration_by_parts':S.simplify(raw-reduced+divergence)==0,
            'projected_D':S.simplify(S.trigsimp(D-expected_D))==0,
            'acceleration':S.simplify(S.trigsimp(PA-expected_PA))==0}
    return checks,dict(R=str(R),D=str(D),PA=str(PA),reduced_Einstein_over_M2=str(reduced))


def junction_checks(mutate):
    a,b,ax,bx,P,d,v=S.symbols('alpha beta alpha_x beta_x P d v',real=True)
    s,g,M2=S.symbols('s gamma M2',positive=True)
    C=1/S.sqrt(1-v*v); B=S.exp(-2*a)*s*s*(1-v*v)
    D=S.exp(-a)*C*(d+(0 if mutate=='divergence' else 2)*P*bx)
    vol=S.exp(2*a+2*b)
    Lm=vol*(-D+B/2-g*D**2/2-g*D*B)
    Lg=M2*S.exp(2*b)*(2*ax*bx+(2 if mutate=='Einstein' else 1)*bx*bx)
    L=Lm+Lg
    pP=S.diff(L,d); pa=S.diff(L,ax); pb=S.diff(L,bx)
    checks={
       'pi_alpha':S.simplify(pa-2*M2*S.exp(2*b)*bx)==0,
       'pi_beta_current_identity':S.simplify(pb-2*M2*S.exp(2*b)*(ax+bx)-2*P*pP)==0,
       'Einstein_transverse_coefficient':S.simplify(Lg-M2*S.exp(2*b)*(2*ax*bx+bx*bx))==0,
       'pi_P':S.simplify(pP+S.exp(a+2*b)*C*(1+g*(D+B)))==0,
    }
    # Remove the common metric derivative from d using e=d+2P beta_x.
    ell=S.symbols('ell',real=True)
    translated=L.subs(d,ell-2*P*bx)
    pphi=S.diff(L,v)  # proportional to phi_x current at fixed phi_t
    total_H=v*pphi+d*pP+ax*pa+bx*pb-L
    hgrav=Lg
    shifted_H=(v*S.diff(translated,v)+ell*S.diff(translated,ell)-(translated-Lg))
    checks['total_stress_cancellation']=S.simplify(total_H-shifted_H-hgrav)==0
    # Necessary jump matrix: continuous piP and P imply homogeneous metric jump equations.
    jumpmat=2*M2*S.exp(2*b)*S.Matrix([[0,1],[1,1]])
    checks['metric_jump_matrix_invertible']=S.simplify(jumpmat.det()+4*M2*M2*S.exp(4*b))==0
    return checks,dict(pi_alpha=str(pa),pi_beta=str(S.factor(pb)),pi_P=str(S.factor(pP)),
        jump_matrix=str(jumpmat),jump_determinant=str(S.factor(jumpmat.det())),
        total_spatial_H=str(S.factor(total_H)),metric_spatial_H=str(Lg))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True)
    ap.add_argument('--mutate',choices=['none','divergence','Einstein'],default='none');args=ap.parse_args()
    checks,geometry=geometric_checks(); jc,junction=junction_checks(args.mutate);checks.update(jc)
    out=dict(checks=checks,all_pass=all(checks.values()),mutation=args.mutate,geometry=geometry,junction=junction,
      scope='Necessary regular stationary planar corner conditions; not full constrained evolution or all singular measures')
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
    raise SystemExit(0 if out['all_pass'] else 1)


if __name__=='__main__':main()
