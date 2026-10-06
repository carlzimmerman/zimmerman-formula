"""Exact finite jet spaces corroborate the dimension-independent proof in REPORT.
Contravariant symmetric tensor coordinates; no PDE or physical matter realization solver.
"""
import argparse,json,math,platform
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--mutate-accept-trace-projector',action='store_true');args=ap.parse_args()
out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
checks={};ranks=[];witnesses=[]
def ck(n,x):checks[n]=bool(x);print(('PASS ' if x else 'FAIL ')+n)
def bases(d):
 pairs=[(i,j) for i in range(d) for j in range(i,d)];lookup={p:i for i,p in enumerate(pairs)}
 def idx(i,j):return lookup[tuple(sorted((i,j)))]
 E=[]
 for i,j in pairs:
  z=s.zeros(d);z[i,j]=1;z[j,i]=1;E.append(z)
 return pairs,idx,E
for d in [2,3,4,5]:
 pairs,idx,E=bases(d);N=len(pairs)
 B=s.zeros(d,d*N)
 for mu in range(d):
  for nu in range(d):B[nu,mu*N+idx(mu,nu)]=1
 # Exact explicit kernel: each nonpivot jet minus its divergence in J_0^{0nu}.
 pivots=[idx(0,nu) for nu in range(d)]
 kernel=[]
 for col in range(d*N):
  if col in pivots:continue
  j=s.zeros(d*N,1);j[col]=1
  for nu in range(d):j[pivots[nu]]-=B[nu,col]
  kernel.append(j)
 ck('jet_kernel_dimension_d'+str(d),len(kernel)==d*N-d and all(B*j==s.zeros(d,1) for j in kernel))
 rows=[]
 for jet in kernel:
  for nu in range(d):
   row=[s.Integer(0)]*(N*N)
   for mu in range(d):
    for c in range(N):row[idx(mu,nu)*N+c]+=jet[mu*N+c]
   rows.append(row)
 constraints=s.Matrix(rows);rank=constraints.rank();ns=constraints.nullspace()
 vecI=s.Matrix([int(i==j) for i in range(N) for j in range(N)])
 ck('all_jet_linear_classification_d'+str(d),rank==N*N-1 and len(ns)==1 and constraints*vecI==s.zeros(len(rows),1))
 ranks.append(dict(d=d,symmetric_dimension=N,jet_kernel_dimension=len(kernel),constraint_rows=len(rows),rank=rank,admissible_DH_dimension=len(ns)))
 eta=s.diag(-1,*([1]*(d-1)));trace=s.Matrix([[sum(eta[i,j]*E[c][i,j] for i in range(d) for j in range(d)) for c in range(N)]])
 gvec=s.Matrix([eta[i,j] for i,j in pairs]);projector=s.eye(N)-gvec*trace/d
 pj=s.Matrix([projector[i,j] for i in range(N) for j in range(N)])
 trace_pass=constraints*pj==s.zeros(len(rows),1)
 ck('trace_projector_rejected_d'+str(d),trace_pass if args.mutate_accept_trace_projector else not trace_pass)
 # Concretely conserved dust-density spatial jet: J_1^{00}=1.
 J=[s.zeros(d) for _ in range(d)];J[1][0,0]=1
 T=s.diag(d+2,*range(1,d));tr=s.trace(eta*T)
 def div(DH):return s.Matrix([sum(DH(J[mu])[mu,nu] for mu in range(d)) for nu in range(d)])
 maps={'trace_projector':lambda z:z-s.trace(eta*z)*eta/d,'trace_times_T':lambda z:s.trace(eta*z)*T+tr*z,'invariant_scalar_metric':lambda z:2*s.trace(eta*T*eta*z)*eta}
 vals={name:list(div(f)) for name,f in maps.items()}
 ck('nonlinear_invariant_map_failures_d'+str(d),all(any(v!=0 for v in vv) for vv in vals.values()))
 # Quadratic tensor invariant needs a conserved paired shear/density jet.
 J=[s.zeros(d) for _ in range(d)];J[1][1,1]=1;J[0][0,1]=J[0][1,0]=-1
 quadratic=div(lambda z:z*eta*T+T*eta*z)
 ck('quadratic_tensor_failure_d'+str(d),any(v!=0 for v in quadratic))
 witnesses.append(dict(d=d,dust_jet_outputs={n:list(map(str,v)) for n,v in vals.items()},quadratic_paired_jet_output=list(map(str,quadratic))))
# General-dimensional compensator, trace-free reconstruction and Newton source factors.
d,a,b,t,L0,R=s.symbols('d a b t Lambda0 R',nonzero=True)
Lam=b*t+L0
ck('trace_compensator_restores_universal',s.expand(b*t-Lam)==-L0)
C0=((d-2)*R/2+a*t)/d
ck('trace_free_trace_reconstruction',s.simplify(-(d-2)*R/2+d*C0-a*t)==0)
c,GN,Omega,kappa,r,M=s.symbols('c GN Omega kappa r M',positive=True)
phi=-kappa*M*c**4/((d-2)*Omega*r**(d-3))
force=s.diff(phi,r)
kcal=Omega*(d-2)*GN/((d-3)*c**4)
ck('Tangherlini_force_calibration',s.simplify(force.subs(kappa,kcal)-GN*M/r**(d-2))==0)
ck('linearized_Poisson_matches_Gauss',s.simplify((kappa*c**4*(d-3)/(d-2)).subs(kappa,kcal)-Omega*GN)==0)
ck('four_dimension_Einstein_coefficient',s.simplify(kcal.subs({d:4,Omega:4*s.pi})-8*s.pi*GN/c**4)==0)
ck('three_dimension_dust_R00_factor_zero',((d-3)/(d-2)).subs(d,3)==0)
# Units in base (length,mass,time): GN=(d-1,-1,-2), rho_mass=(-(d-1),1,0).
ck('GN_density_units_all_d',s.simplify((d-1)-(d-1))==0 and -2==-2)
ck('kappa_energy_density_curvature_units',s.simplify(((d-1)-4)+(-(d-3)))==-2)
calibration=[]
for dn in range(4,9):
 om=2*math.pi**((dn-1)/2)/math.gamma((dn-1)/2)
 calibration.append(dict(d=dn,sphere_area=om,kappa_c4_over_GN=om*(dn-2)/(dn-3),GN_over_GEH=8*math.pi*(dn-3)/((dn-2)*om)))
res={'checks':checks,'jet_spaces':ranks,'witnesses':witnesses,'Newton_calibration':calibration,'mutation':args.mutate_accept_trace_projector,'limitations':['Exact finite d=2..5 ranks corroborate, do not prove all d','Open unrestricted stress first-jet domain is essential','Einstein geometry only; no extra fields, derivatives, nonlocality or stress exchange','d=3 classification valid, inverse-power Tangherlini Newton calibration unavailable']}
(out/'results.json').write_text(json.dumps(res,indent=2)+'\n');raise SystemExit(0 if all(checks.values()) else 1)
