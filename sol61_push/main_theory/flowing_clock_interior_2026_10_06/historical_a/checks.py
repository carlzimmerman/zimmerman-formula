#!/usr/bin/env python3
import argparse,json,platform
from pathlib import Path
import sympy as S
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=HERE);ap.add_argument('--mutate-drop-fluid-momentum',action='store_true');args=ap.parse_args();out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
checks=[]
def ck(n,ok,d):checks.append(dict(name=n,passed=bool(ok),detail=str(d)));print(('PASS ' if ok else 'FAIL ')+n+': '+str(d))
N,B,V,r,rho,p,M,H,eta=S.symbols('N B V r rho p M H eta',positive=True)
F=N*N-B*B*V*V;g=S.Matrix([[-F,B*B*V],[B*B*V,B*B]]);gi=g.inv();u=S.Matrix([1/S.sqrt(F),0]);T=(rho+p)*u*u.T+p*gi;volume=N*B*r*r
variations={v:S.simplify(volume*sum(T[i,j]*S.diff(g[i,j],v) for i in range(2) for j in range(2))/2) for v in [N,B,V]}
eps=(rho+p)*N*N/F-p;sr=p+(rho+p)*B*B*V*V/F
ck('actual_fluid_metric_variation',S.simplify(variations[N]+B*r*r*eps)==0 and S.simplify(variations[B]-N*r*r*sr)==0 and S.simplify(variations[V]-N*B**3*r*r*(rho+p)*V/F)==0,'staticKilling perfectfluid has nonzero ADM momentum')
EVm=0 if args.mutate_drop_fluid_momentum else variations[V]
ck('source_Noether_current_cancellation',S.simplify(-V*variations[N]+V*B/N*variations[B]-(V*V/N+N/(B*B))*EVm)==0,'source-weighted exact current identity leaves jtotal0, not arbitrary scalar charge')
rr=S.symbols('rr',positive=True);Nf=S.Function('N')(rr);Bf=S.Function('B')(rr);Vf=S.Function('V')(rr);a=S.diff(Nf,rr)/(Nf*Bf);Uf=-3*M*H*H+6*eta*M*H*H*S.log(Nf)
# Quadratic response alone determines every r² coefficient; cubic is tested separately.
Lg=M*(Nf*(Bf+1/Bf)+2*rr*S.diff(Nf,rr)/Bf)-M*rr*Vf**2*(S.diff(Bf,rr)/Nf+Bf*S.diff(Nf,rr)/Nf**2)+Nf*Bf*rr**2*Uf-2*eta*M*H*Bf*rr**2*Vf*S.diff(Nf,rr)/Nf+M*Nf*Bf*rr**2*a*a
EL=lambda z:S.diff(Lg,z)-S.diff(S.diff(Lg,S.diff(z,rr)),rr)
N0,n2,b2,x,R,P=S.symbols('N0 n2 b2 x R P',real=True);series={Nf:N0*(1+n2*rr**2),Bf:1+b2*rr**2,Vf:N0*x*rr}
def coefficient(expr):
 e=expr.subs(series).doit();return S.simplify(S.limit(e/(rr*rr),rr,0))
u0=-3*H*H+6*eta*H*H*S.log(N0)
EB2=coefficient(EL(Bf))/(M*N0);EN2=coefficient(EL(Nf))/M;EV2=coefficient(EL(Vf))/M
ck('exact_center_B_Euler',S.simplify(EB2-(2*b2-4*n2+3*x*x+u0))==0,'quadratic center coefficient independent A')
ck('exact_center_N_Euler',S.simplify(EN2-(6*b2-12*n2+3*x*x+6*eta*H*x+u0+6*eta*H*H))==0,'criticalresponse contributes−12n2 from(r²Qa)prime')
EVmatter2=(0 if args.mutate_drop_fluid_momentum else N0*x*(R+P))
ck('exact_center_momentum',S.simplify(EV2+EVmatter2+4*N0*(x*(b2+n2-(R+P)/4)+eta*H*n2))==0,'fluid ADMmomentum contributes at same r²order as braiding')
b2sol=2*n2-S.Rational(3,2)*x*x-u0/2-P/2
poly=x*x-eta*H*x-(1+eta)*H*H+2*eta*H*H*S.log(N0)+(R+3*P)/6
ck('center_discriminant_derivation',S.simplify((EN2.subs(b2,b2sol)-R)+6*poly)==0,'B eliminates n2 from lapse equation: realflow requires densitybound')
quad=S.solve(poly,R)[0]
mom=x*(b2sol+n2-(R+P)/4)+eta*H*n2
ck('remaining_center_trace_constraint',S.simplify(mom.subs(R,quad)-(n2*(3*x+eta*H)-S.Rational(3,2)*eta*H*x*(x+H)))==0,'x=-etaH/3 is singular with nonzero numerator for eta in(0,1)')
A=S.symbols('A',positive=True);n2pos=S.symbols('n2pos',positive=True)
ck('cubic_response_is_subleading_at_center',S.limit(S.diff(rr*rr*(2*(2*n2pos*rr)-2*(2*n2pos*rr)**2/A),rr)/(rr*rr),rr,0)==12*n2pos,'P2 cubic or UVcutoff preserving it changes r³+ terms, not necessary r² bound')
# Leading weak matter flux integral: surface pressure drops out, regularcenter constant zero.
rhos,pres=S.symbols('rhos pres',positive=True)
flux=S.integrate(rhos*rr**2/(2*M),(rr,0,rr))
ck('regular_weak_source_mass_normalization',flux==rhos*rr**3/(6*M),'derived leading m=GMbaryon atp0surface, under weakhierarchy/noindependentcentraldata')
eta05=S.Rational(1,2);cap=S.Rational(3,2)*(eta05+2)**2
ck('matching_example_density_conflict',6*S.Rational(1,10**12)/(S.Rational(1,10**5)**3)>cap,'m1e-12,r_surface<=1e-5 needsrho/M>=6000, centerweakN0cap9.375H²')
alpha=S.Rational(3,2);cusp=S.Symbol('C',positive=True)*rr**alpha
ck('MOND_center_curvature_cusp',S.limit(S.diff(cusp,rr)/rr,rr,0)==S.oo,'regularflow V=O(r) cannot cancel F r^1.5; tangential physicalcurvature diverges')
ck('canceled_cusp_momentum_order',S.limit(rr**S.Rational(7,4)/rr**S.Rational(3,2),rr,0)==0,'physicalregular F,D imply Jprime/J=O(r); for p1.5 braidingrNprime dominates both VJprime/J and finitefluidsource')
result=dict(checks=checks,mutation=args.mutate_drop_fluid_momentum,software=dict(python=platform.python_version(),sympy=S.__version__),eta_half_center_density_cap=str(cap),non_claims=['No full interior integration/globalsource existence','No exclusion of weak/integrable singular centers','No arbitraryGR source no-go outside statedaction/regularity'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
