#!/usr/bin/env python3
"""New metric/stress implications of previously derived vacuum scalar constraints."""
import argparse,json,time,platform
from pathlib import Path
import sympy as S
import numpy as np
from scipy.integrate import solve_ivp
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--drop-current',action='store_true');args=ap.parse_args();out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
checks=[]
def ck(n,v,d):checks.append(dict(name=n,passed=bool(v),detail=d));print(('PASS ' if v else 'FAIL ')+n,flush=True)
x,eta,kap=S.symbols('x eta kap',positive=True);z,v,phi,phiv=S.symbols('z v phi phiv');beta=1-eta;g=3*eta**2/beta**2;d=kap/beta**2;f=eta/beta;AA=g+d*x;R=AA/x;gam=(3*g+d*x)/AA;om=f*x/AA
# N=ln a dimensionless time; x_N=-2x. On-shell z_NN=-gam z_N-om z.
DD=lambda expr:S.simplify(-2*x*S.diff(expr,x)+v*S.diff(expr,z)+(-gam*v-om*z)*S.diff(expr,v))
B=-z/beta-R*v;nu=v/beta
Phi=f*z+R*v;Psi=S.simplify(nu+DD(B))
ck('constrained_physical_no_slip',S.simplify(Phi-Psi)==0,'Actual vacuum lapse/shift transfer, including Bdot, not clock acceleration identified as force')
ck('metric_current_transfer_identity',S.simplify(DD(Phi)+Phi-f*v)==0,'Phi_N+Phi=f zeta_N')
Omphi=(2*g+f*x)/AA
ck('exact_metric_potential_equation',S.simplify(DD(DD(Phi))+gam*DD(Phi)+Omphi*Phi)==0,'Observable potential equation from constrained clock dynamics')
# Generic potential derivatives make conservation independent of mode equation.
p0,p1,p2,p3=S.symbols('p0 p1 p2 p3');Dgeneric=lambda expr:S.simplify(-2*x*S.diff(expr,x)+p1*S.diff(expr,p0)+p2*S.diff(expr,p1)+p3*S.diff(expr,p2))
rho=-2*(x*p0+3*(p1+p0));q=0 if args.drop_current else -2*(p1+p0);press=2*(p2+4*p1+3*p0)
ck('operational_energy_conservation',S.simplify(Dgeneric(rho)+3*(rho+press)-x*q)==0,'Einstein-defined scalar stress including response: rho_N+3(rho+p)-x q=0, H=M=1')
ck('operational_momentum_conservation',S.simplify(Dgeneric(q)+3*q+press)==0,'q_N+3q+p=0; omitting current must fail')
ck('Poisson_density_dictionary',S.simplify(rho-3*q+2*x*p0)==0,'D_grav=rho-3Hq=-2M pphysical²Phi, not rest-frame dust density')
res1=S.simplify(1-gam+Omphi);res3=S.simplify(9-3*gam+Omphi)
ck('dust_source_not_free_clock_mode',S.simplify(res1-f*x/AA)==0,'Phi~a^-1 has positive residual f x/AA at all finite nonzero k')
ck('second_pressureless_basis_residual',S.simplify(res3-(2*g+(6*d+f)*x)/AA)==0,'Phi~a^-3 also is not free clock mode')
# Mixture residual polynomial has coefficients C3(6d+f)x0 and C1 f x0+2gC3.
c1,c3,x0,a=S.symbols('c1 c3 x0 a',nonzero=True);mix=c1*a**-1*res1.subs(x,x0/a**2)+c3*a**-3*res3.subs(x,x0/a**2)
ck('pressureless_mixture_polynomial',S.simplify(mix*AA.subs(x,x0/a**2)*a**5-(a*a*(c1*f*x0+2*g*c3)+c3*(6*d+f)*x0))==0,'Positivity 0<eta<1,kap>0,x0>0 gives no nontrivial exactly pressureless free mode on interval')
s=S.symbols('s');mu=eta*beta/kap;Cs=f+d*s
ck('UV_metric_amplitude',S.rem(Cs+kap*s*s/beta**2,s*s+s+mu,s)==0,'On UV root metric amplitude is -kap s²/beta² times zeta')
ck('UV_current_remains_leading',S.limit((-2*(s+1))/(-2*(x+3*(s+1)))*x,x,S.oo)==s+1,'p²q/(Hrho) tends s+1 while pressure/density tends0')
ck('UV_pressure_ratio_small',S.limit(2*(s*s+4*s+3)/(-2*(x+3*(s+1))),x,S.oo)==0,'Small pressure fraction alone does not imply conserved dust')
# Spatial gauge transformation on stationary radial tail b=-beta ell.
lam,rr,ll=S.symbols('lam rr ll',nonzero=True);zz=beta*ll*rr**lam/lam;bb=-beta*ll*rr**lam
ck('radial_to_cosmic_clock_bridge',S.simplify(rr*S.diff(zz,rr)+bb)==0 and S.simplify(lam*zz/beta-ll*rr**lam)==0,'r=a chi, pure spatial shear removal: chi zeta_chi=-b, nu=zeta_N/beta=ell')
ck('shared_radial_temporal_polynomial',S.simplify((lam*lam+lam+eta*beta/kap)-(lam*lam+lam+mu))==0,'Conditional C_lin0 stationary small-r tail is same time-dependent UV scalar mode, not mass mode')
rows=[]
for et in [.2,.5,.8]:
 kk=.99;be=1-et;gg=3*et*et/be**2;dd=kk/be**2;ff=et/be;xinit=1e8;stop=np.log(1e6)
 disc=1-4*et*be/kk;sv=(-1+np.sqrt(disc))/2 if disc>=0 else -.5
 zi=1e-6;vi=sv*zi;ri=gg/xinit+dd;pi=ff*zi+ri*vi;pvi=ff*vi-pi
 solutions=[]
 for tol in [1e-9,3e-10]:
  count=[0];start=time.monotonic()
  def rhs(t,y):
   count[0]+=1
   if count[0]>20000 or time.monotonic()-start>10:raise RuntimeError('declared percase resource cap')
   xx=xinit*np.exp(-2*t);aa=gg+dd*xx;ga=(3*gg+dd*xx)/aa;oo=ff*xx/aa;op=(2*gg+ff*xx)/aa
   return [y[1],-ga*y[1]-oo*y[0],y[3],-ga*y[3]-op*y[2]]
  sol=solve_ivp(rhs,[0,stop],[zi,vi,pi,pvi],method='DOP853',rtol=tol,atol=tol*1e-6,dense_output=True,max_step=.08)
  samples=[]
  for tt in np.linspace(0,stop,81):
   zz,vv,pp,pv=sol.sol(tt);xx=xinit*np.exp(-2*tt);aa=gg+dd*xx;ga=(3*gg+dd*xx)/aa;op=(2*gg+ff*xx)/aa;pvv=-ga*pv-op*pp
   transfer=ff*zz+(gg/xx+dd)*vv;den=-2*(xx*pp+3*(pv+pp));cur=-2*(pv+pp);pressure=2*(pvv+4*pv+3*pp)
   samples.append(dict(N=tt,x=xx,zeta=zz,Phi=pp,transfer=transfer,rho=den,q=cur,pressure=pressure,pressure_fraction=pressure/den if abs(den)>1e-25 else None,current_divergence_fraction=xx*cur/den if abs(den)>1e-25 else None))
  solutions.append(dict(tol=tol,nfev=count[0],success=sol.success,samples=samples,end_state=sol.y[:,-1].tolist()))
 ck('bounded_metric_transfer_eta_'+str(et),all(row['success'] and max(abs(pt['Phi']-pt['transfer']) for pt in row['samples'])<2e-11 for row in solutions),'Independent simultaneous zeta and physical Phi integrations across x1e8..1e-4')
 ck('bounded_tolerance_agreement_eta_'+str(et),max(abs(a-b) for a,b in zip(solutions[0]['end_state'],solutions[1]['end_state']))<2e-11,'Two bounded tolerances, not certified global existence')
 ck('small_pressure_nonzero_transport_eta_'+str(et),all(abs(row['samples'][0]['pressure_fraction'])<1e-6 and abs(row['samples'][0]['current_divergence_fraction'])>.1 for row in solutions),'Actual operational stress shows cold-like pressure but leading current at UV start')
 rows.append(dict(eta=et,kappa=kk,UV_discriminant=disc,runs=solutions))
result=dict(checks=checks,runs=rows,software=dict(python=platform.python_version(),sympy=S.__version__,numpy=np.__version__),mutation=args.drop_current,non_claims=['No matter/radiation background or recombination transfer','No materialcoldidentity or unique initialamplitude','No finitegradient/nonlinear health','No A/H selection'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');raise SystemExit(0 if all(c['passed'] for c in checks) else 1)
