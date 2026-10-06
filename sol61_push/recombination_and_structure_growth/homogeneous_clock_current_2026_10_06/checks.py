import argparse,json
from pathlib import Path
import sympy as s
import mpmath as mp
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--wrong-charge',action='store_true');p.add_argument('--fake-cold-amplitude',action='store_true');args=p.parse_args()
q,c,H,Hs,Xref,M=s.symbols('q c H Hs Xref M',positive=True);n=s.symbols('n',integer=True,positive=True);X=s.symbols('X',positive=True);eta,z,h,D,j=s.symbols('eta z h D j',positive=True)
K=-c*s.log(X/Xref);G=-s.sqrt(2)*c/(n*Hs*s.sqrt(X));J=s.simplify((q*s.diff(K,X)+n*H*q*q*s.diff(G,X)).subs(X,q*q/2));rho=s.simplify(q*J-K.subs(X,q*q/2))
f=(h*h-1)/(2*eta)-(h-1)-s.log(h-1);g=z-s.log(z);jcrit=D*eta*s.exp(eta/2)
checks=[]
def ck(name,ok):checks.append({'name':name,'passed':bool(ok)})
ck('direct_current_general_n',s.simplify(J-2*c*(H/Hs-1)/q)==0)
ck('direct_scalar_density',s.simplify(rho-(c*s.log(q*q/(2*Xref))+2*c*(H/Hs-1)))==0)
Hdot=s.symbols('Hdot',real=True);qdlog=n*H+Hdot/(H-Hs)
ck('scalar_continuity_from_current',s.simplify(2*c*qdlog+2*c*Hdot/Hs+n*H*(2*c*(H/Hs-1)-2*c*qdlog/(n*Hs)))==0)
ck('F_derivative',s.simplify(s.diff(f,h)-h*(1/eta-1/(h-1)))==0)
ck('F_minimum',s.simplify(f.subs(h,1+eta)-(1-eta/2-s.log(eta)))==0)
used=D*eta if args.wrong_charge else jcrit
ck('charge_matches_folds',s.simplify(1+s.log(D/used)-(1-eta/2-s.log(eta)))==0)
v=s.symbols('v',positive=True)
ck('signed_square_root_fold_identity',s.simplify(f.subs(h,1+eta*v)-(1-eta/2-s.log(eta))-(v-s.log(v)-1+eta*(v-1)**2/2))==0)
ck('fold_slope',s.simplify(s.diff(f,h,2).subs(h,1+eta)*(eta/s.sqrt(1+eta))**2-s.diff(g,z,2).subs(z,1))==0)
late_coeff=eta*s.exp(eta/2)
ck('late_charge_normalization',s.simplify(D*late_coeff/jcrit-1)==0)
used_enhancement=s.Integer(6) if args.fake_cold_amplitude else s.exp(eta/2)
ck('late_effective_dust_coefficient',s.simplify(used_enhancement-late_coeff/eta)==0)
mp.mp.dps=60;rows=[]
def L(x):return x-mp.log(x)-1
def solve(ee,zz):
 if zz==1:return 1+ee
 target=L(zz);lo=mp.mpf('1e-100') if zz<1 else mp.mpf(1);hi=mp.mpf(1) if zz<1 else max(mp.mpf(2),zz)
 for _ in range(450):
  mid=(lo+hi)/2;val=L(mid)+ee*(mid-1)**2/2
  if (val>target)==(zz<1):lo=mid
  else:hi=mid
 return 1+ee*(lo+hi)/2
for etext in ['.1','.5','.9']:
 ee=mp.mpf(etext);zzs=[mp.mpf(t) for t in ['1e-8','.01','.9','.999','1','1.001','1.1','100','1e8']];hs=[solve(ee,zz) for zz in zzs]
 res=max(abs(L((hh-1)/ee)+ee*((hh-1)/ee-1)**2/2-L(zz))/(1+L(zz)) for hh,zz in zip(hs,zzs))
 ck('finite_roots_'+etext,res<mp.mpf('1e-45'))
 ck('monotone_history_'+etext,all(a<b for a,b in zip(hs,hs[1:])))
 ck('early_GR_'+etext,abs(hs[-1]**2/(2*ee*zzs[-1])-1)<mp.mpf('.001'))
 ck('late_dust_'+etext,abs((hs[0]-1)/(ee*mp.exp(ee/2)*zzs[0])-1)<mp.mpf('1e-6'))
 rows.append({'eta':etext,'max_scaled_constraint':str(res),'fold_H_over_Hstar':str(1+ee),'late_dust_enhancement':str(mp.exp(ee/2)),'H_over_Hstar':[str(x) for x in hs]})
out={'checks':checks,'summary':{'passed':sum(x['passed'] for x in checks),'total':len(checks)},'histories':rows,'scope':'Dust-only geodesic homogeneous history; no radiation/recombination perturbations or32pi selector'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out['summary']));raise SystemExit(0 if all(x['passed'] for x in checks) else 1)
