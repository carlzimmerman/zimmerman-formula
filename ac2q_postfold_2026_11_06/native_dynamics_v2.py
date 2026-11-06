"""PF03: exact flat planar scalar/polarization currents and frozen-background symbol."""
import argparse
import json
from pathlib import Path
import sympy as S


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True)
    ap.add_argument('--mutate',action='store_true'); args=ap.parse_args()
    a,s,g,H,k=S.symbols('a s gamma H k',positive=True)
    b,u,d,om=S.symbols('b u d omega',real=True)
    r=S.sqrt(a*a-b*b); X=r*r/2; D=(a*d-b*u)/r
    Ls={'on':-D+X-g*D*D/2-2*g*D*X,
        'off':-D+X+2*g*X*X}
    result={};checks={}
    for branch,L in Ls.items():
        bg={a:s,b:0,u:0}
        AA=S.simplify(S.diff(L,a,2).subs(bg))
        BB=S.simplify(-S.diff(L,b,2).subs(bg))
        CC=S.simplify((S.diff(L,a,d)+S.diff(L,b,u)).subs(bg))
        GG=S.simplify(-S.diff(L,d,2).subs(bg))
        expected={'on':(1-2*g*d,1-g*d+d*(1+g*d)/(s*s),(1+g*d-g*s*s)/s,g),
                  'off':(1+6*g*s*s,1+2*g*s*s+d/(s*s),1/s,S.Integer(0))}[branch]
        for name,got,want in zip(['A','B','C','G'],[AA,BB,CC,GG],expected):
            checks[f'{branch}_{name}']=S.simplify(got-want)==0
        checks[f'{branch}_P_no_rest_time_kinetic']=S.simplify(S.diff(L,u,2).subs(bg))==0
        checks[f'{branch}_no_phi_tP_t']=S.simplify(S.diff(L,a,u).subs(bg))==0
        checks[f'{branch}_no_phi_xP_x']=S.simplify(S.diff(L,b,d).subs(bg))==0
        # Fourier matrix of divergence-form EL equations, including +H P in P equation.
        c_used=S.Integer(0) if args.mutate else CC
        mat=S.Matrix([[-AA*om**2+BB*k*k,c_used*om*k],
                      [c_used*om*k,GG*k*k+H]])
        det=S.factor(mat.det())
        W2=S.symbols('W2')
        roots=S.solve(det.subs(om**2,W2),W2)
        predicted=S.factor(BB*k*k/(AA+CC*CC*k*k/(GG*k*k+H)))
        checks[f'{branch}_independent_root']=len(roots)==1 and S.simplify(roots[0]-predicted)==0
        uv2=S.simplify(S.limit(predicted/k**2,k,S.oo))
        uv0=S.simplify(S.limit(predicted,k,S.oo)) if branch=='off' else None
        checks[f'{branch}_no_k4']=S.limit(predicted/k**4,k,S.oo)==0
        if branch=='off':
            checks['off_bounded_uv']=S.simplify(uv0-H*(s*s+2*g*s**4+d))==0
        else:
            expected_uv=g*(s*s-g*d*s*s+d+g*d*d)/(g*s*s*(1-2*g*d)+(1+g*d-g*s*s)**2)
            checks['on_uv']=S.simplify(uv2-expected_uv)==0
        currents={name:str(S.factor(S.diff(L,z))) for name,z in [('Jphi_t',a),('Jphi_x',b),('JP_t',u),('JP_x',d)]}
        result[branch]=dict(L=str(L),currents=currents,A=str(AA),B=str(BB),C=str(CC),G=str(GG),
             determinant=str(det),omega2=str(predicted),uv_omega2_over_k2=str(uv2),uv_omega2=str(uv0))
    ron=S.sympify(result['on']['omega2'],locals={str(z):z for z in (g,s,d,H,k)})
    roff=S.sympify(result['off']['omega2'],locals={str(z):z for z in (g,s,d,H,k)})
    checks['gamma_zero_matches']=S.simplify(ron.subs(g,0)-roff.subs(g,0))==0
    out=dict(checks=checks,all_pass=all(checks.values()),mutate=args.mutate,branches=result,
        scope='Exact flat planar action; frozen background; fixed metric; no global nonlinear or gravitating evolution')
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    raise SystemExit(0 if out['all_pass'] else 1)


if __name__=='__main__':main()
