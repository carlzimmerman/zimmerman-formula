import argparse,json
from pathlib import Path
import sympy as S
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
r,A,g,mu,V,W=S.symbols('r A gamma mu V W', positive=True)
H=r*r/2-V-W+(A*r-1-g*r*r)**2/(2*g); h=S.diff(H,r)
v,a,b,Ps=S.symbols('v a b Pi_s', positive=True)
jN=-(h-mu*A)*b/r+A*Ps/a
TNT=(h-mu*A)*b*v/r
s=S.symbols('s');sig=S.Function('sigma')(s);area=S.Function('a')(s);speed=S.Function('v')(s)
q=2*area*sig/speed
f=(S.diff(area*sig,s)+sig*S.diff(area,s)/2)/area
res=S.expand(speed*(S.diff(q,s)-area*f/speed)/area)
expected=S.diff(sig,s)-(2*S.diff(speed,s)/speed-S.diff(area,s)/(2*area))*sig
inv=S.diff(sig*S.sqrt(area)/speed**2,s)
# Intrinsic covariant divergence D_i S^i_s for induced metric diag(-1,B^2,B^2).
B=S.Function('B')(s);press=S.Function('p')(s)
metric=S.diag(-1,B**2,B**2); inverse=metric.inv();coords=[s,S.Symbol('y'),S.Symbol('z')]
Gamma=[[[sum(inverse[i,l]*(S.diff(metric[l,k],coords[j])+S.diff(metric[l,j],coords[k])-S.diff(metric[j,k],coords[l]))/2 for l in range(3)) for k in range(3)] for j in range(3)] for i in range(3)]
stress=S.diag(-sig,press,press)
div=sum(S.diff(stress[i,0],coords[i]) for i in range(3))+sum(Gamma[i][i][k]*stress[k,0]-Gamma[k][i][0]*stress[i,k] for i in range(3) for k in range(3))
checks={
 'transverse_quartic':S.limit(H/r**4,r,S.oo)==g/2,
 'base_trace_quartic':S.limit((2*H-r*h)/r**4,r,S.oo)==-g,
 'outer_current_stress_identity':S.simplify(TNT+v*jN-v*A*Ps/a)==0,
 'surface_energy_divergence':S.simplify(div+S.diff(sig,s)+2*S.diff(B,s)*(sig+press)/B)==0,
 'coupled_amplitude_equation':S.simplify(res-expected)==0,
 'conserved_amplitude':S.simplify(inv-expected*S.sqrt(area)/speed**2)==0,
 'charge_invariant':S.simplify(q/(speed*S.sqrt(area))-2*sig*S.sqrt(area)/speed**2)==0}
out={'checks':checks,'all_pass':all(checks.values()),'scope':'Exact smooth algebra and intrinsic divergence only; no numerical native layer, singular compactness proof, or global uniqueness claim.'}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(0 if out['all_pass'] else 1)
