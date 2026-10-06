#!/usr/bin/env python3
import argparse,json
from pathlib import Path
import sympy as S
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--mutate-log-offset',action='store_true');args=ap.parse_args();out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
r,M,H,eta,eps,Nc,beta,x=S.symbols('r M H eta epsilon Nc beta x',positive=True);N=S.Function('N')(r);B=S.Function('B')(r);V=S.Function('V')(r)
a=S.diff(N,r)/(N*B);U=M*(-3*H**2+6*eta*H**2*S.log(N))
L=M*(N*(B+1/B)+2*r*S.diff(N,r)/B)-M*r*V**2*(S.diff(B,r)/N+B*S.diff(N,r)/N**2)+N*B*r*r*U-2*M*eta*H*B*r*r*V*S.diff(N,r)/N+M*N*B*r*r*(1-eps)*a*a
EL=lambda f:S.diff(L,f)-S.diff(S.diff(L,S.diff(f,r)),r)
vals={N:Nc,B:beta,V:Nc*x*r};eb=S.simplify(EL(B).subs(vals).doit()/M/Nc);en=S.simplify(EL(N).subs(vals).doit()/M/beta);ev=S.simplify(EL(V).subs(vals).doit()/M)
u0=-3*H**2+6*eta*H**2*S.log(Nc);checks=[]
def ck(n,v):checks.append({'name':n,'passed':bool(v)});print(n,v)
ck('constant_lapse_radial_Euler',S.simplify(eb-(1-beta**-2+r*r*(3*x*x+u0)))==0)
ck('constant_lapse_lapse_Euler',S.simplify(en-(1-beta**-2+r*r*(3*x*x+6*eta*H*x+u0+6*eta*H**2)))==0)
ck('constant_lapse_shift_Euler',ev==0)
ck('normalized_vacuum_clock_trace',S.simplify((en-eb)/r**2-6*eta*H*(x+H))==0)
ck('selected_vacuum_unique_lapse',S.simplify((3*x*x+u0).subs(x,-H)-(0 if args.mutate_log_offset else 6*eta*H*H*S.log(Nc)))==0)
ck('exact_flat_deSitter_endpoint',eb.subs({Nc:1,beta:1,x:-H})==0 and en.subs({Nc:1,beta:1,x:-H})==0)
(out/'results.json').write_text(json.dumps({'checks':checks,'scope':'Constant N,B and V=Nxr vacuum ansatz only; no asymptotic decay theorem or on-shell boundary shooting'},indent=2)+'\n');raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
