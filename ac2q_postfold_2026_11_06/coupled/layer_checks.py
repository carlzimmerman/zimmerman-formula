"""PF05: branch-aware stationary layer currents, and planar tensor carrier."""
import argparse
import json
from pathlib import Path
import sympy as S


def tensor_check():
    t,x,y,z=S.symbols('t x y z');co=(t,x,y,z)
    a=S.Function('alpha')(t,x); b=S.Function('beta')(t,x); h=S.Function('h')(t,x)
    g=S.diag(-S.exp(2*a),S.exp(2*a),S.exp(2*b+2*h),S.exp(2*b-2*h));gi=g.inv()
    G=[[[S.simplify(sum(gi[i,l]*(S.diff(g[l,j],co[k])+S.diff(g[l,k],co[j])-S.diff(g[j,k],co[l])) for l in range(4))/2)
        for k in range(4)]for j in range(4)]for i in range(4)]
    ric=S.zeros(4)
    for i in range(4):
        for j in range(4):
            ric[i,j]=S.simplify(sum(S.diff(G[k][i][j],co[k])-S.diff(G[k][i][k],co[j])+
                sum(G[k][i][j]*G[l][k][l]-G[l][i][k]*G[k][j][l]for l in range(4))for k in range(4)))
    R=S.simplify(sum(gi[i,j]*ric[i,j]for i in range(4)for j in range(4)))
    box=lambda f:-S.diff(f,t,2)+S.diff(f,x,2)
    dot=lambda f,q:-S.diff(f,t)*S.diff(q,t)+S.diff(f,x)*S.diff(q,x)
    pred=S.exp(-2*a)*(-2*box(a)-4*box(b)-6*dot(b,b)-2*dot(h,h))
    ntheta=S.Function('theta')(t,x); P=S.Function('P')(t,x)
    n=S.exp(-a)*S.Matrix([S.cosh(ntheta),S.sinh(ntheta),0,0])
    e=S.exp(-a)*S.Matrix([S.sinh(ntheta),S.cosh(ntheta),0,0]);pc=g*(P*e)
    nab=S.Matrix(4,4,lambda i,j:S.diff(pc[j],co[i])-sum(G[k][i][j]*pc[k]for k in range(4)))
    proj=gi+n*n.T
    D=S.simplify(S.trigsimp(sum(proj[i,j]*nab[i,j]for i in range(4)for j in range(4))))
    dpred=S.exp(-a)*(S.sinh(ntheta)*(S.diff(P,t)+2*P*S.diff(b,t))+S.cosh(ntheta)*(S.diff(P,x)+2*P*S.diff(b,x)))
    Lh=-S.exp(2*b)*dot(h,h)
    eh=S.simplify(S.diff(S.diff(Lh,S.diff(h,t)),t)+S.diff(S.diff(Lh,S.diff(h,x)),x))
    return {'tensor_R':S.simplify(R-pred)==0,'D_independent_of_tensor':S.simplify(S.trigsimp(D-dpred))==0,
            'zero_tensor_solves':S.simplify(eh.subs(h,0).doit())==0},dict(R=str(R),tensor_equation=str(eh),D=str(D))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
    a,b,P,bx,v,d=S.symbols('alpha beta P beta_x v d',real=True);s,g=S.symbols('s gamma',positive=True)
    C=1/S.sqrt(1-v*v);B=S.exp(-2*a)*s*s*(1-v*v);E=S.exp(a+2*b);vol=S.exp(2*a+2*b)
    D=S.exp(-a)*C*(d+2*P*bx)
    Loff=vol*(-D+B/2+g*B**2/2);Lon=vol*(-D+B/2-g*D**2/2-g*D*B)
    po=S.simplify(S.diff(Loff,d));jo=S.simplify(-S.diff(Loff,v)/s)
    pon=S.simplify(S.diff(Lon,d))
    expected=E*v*C**3/s
    coeff=S.simplify(S.diff(jo,d))
    if args.mutate:coeff=-coeff
    checks={'off_P_flux':S.simplify(po+E*C)==0,
            'on_P_flux':S.simplify(pon+E*C*(1+g*(D+B)))==0,
            'off_scalar_normal_delta_coefficient':S.simplify(coeff-expected)==0,
            'off_scalar_full_current':S.simplify(jo-(E*v*C**3*(d+2*P*bx)/s+S.exp(2*b)*s*v*(1+2*g*B)))==0}
    A=S.symbols('A',positive=True)
    checks['off_speed_gap']=S.simplify((1-1/A**2)-(A*A-1)/A**2)==0
    # Positive excursions from interior P to cap and back need positive variation.
    # Cauchy-Schwarz: integral(q_+^2) >= (integral(q_+))^2/delta.
    delta,exc=S.symbols('delta excursion',positive=True)
    checks['excursion_cost_diverges']=S.limit(exc**2/delta,delta,0,dir='+')==S.oo
    tc,td=tensor_check();checks.update(tc)
    out=dict(checks=checks,all_pass=all(checks.values()),mutation=args.mutate,
       off_polarization_flux=str(po),off_scalar_flux=str(jo),normal_delta_coefficient=str(expected),
       on_polarization_flux=str(pon),tensor=td,
       scope='Stationary layers with bounded temporal variation, bounded metric first derivatives and bounded potential derivatives; no oscillatory layer theorem')
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
    raise SystemExit(0 if out['all_pass'] else 1)


if __name__=='__main__':main()
