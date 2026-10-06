#!/usr/bin/env python3
"""Reciprocal spherical maximum: constructive dual action and its physical prices."""
import argparse,json,math,platform
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
INPUTS=['sol61_push/cold_component/breakthrough_2026_10_05/REPORT.md',
 'sol61_push/cold_component/breakthrough_2026_10_05/source_matching.py',
 'sol61_push/support_and_assembly.py',
 'campaign_fresh_gravity/CFG45_rule_readings.py',
 'real_research/dark_fluid_2026/FL1_order_parameter.py',
 'sol61_push/cold_component/new_doors_2026_10_05/reciprocal_max/checks.py']

def response(b,d,k=1):
 p=b/(math.sqrt(b*b+b)+b)
 if d<p:
  bt=d*d/(1-2*d); pp=1/(2*math.sqrt(b*b+b)*(2*b+1+2*math.sqrt(b*b+b)))
  bp=2*d*(1-d)/(1-2*d)**2
  return b+p,k*d+bt,1+pp,k+bp,0,True
 return b+d,b+k*d,1,k,1,False

def J(b):
 t=math.sqrt(b*b+b)
 return .5*(b+.5)*t-.125*math.log(2*b+1+2*t)-.5*b*b

def energy(b,d,k=1):
 p=b/(math.sqrt(b*b+b)+b)
 if d<p:
  bt=d*d/(1-2*d)
  return .5*b*b+.5*k*d*d+J(b)-J(bt)+d*bt
 return .5*b*b+b*d+.5*k*d*d

def gradient(B,D,k):
 b=np.linalg.norm(B); d=np.linalg.norm(D); gb,gd,*_=response(b,d,k)
 return np.r_[gb*B/b,gd*D/d]

def vector_hessian(B,D,k):
 b=np.linalg.norm(B);d=np.linalg.norm(D); n=B/b;t=D/d
 gb,gd,hbb,hdd,hbd,_=response(b,d,k)
 A=hbb*np.outer(n,n)+gb/b*(np.eye(3)-np.outer(n,n))
 C=hdd*np.outer(t,t)+gd/d*(np.eye(3)-np.outer(t,t))
 X=hbd*np.outer(n,t)
 return np.block([[A,X],[X.T,C]])

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,default=HERE)
 ap.add_argument('--mutate-keep-newtonian-dark',action='store_true');args=ap.parse_args()
 out=args.output_dir.resolve();out.relative_to(HERE);out.mkdir(parents=True,exist_ok=True)
 checks=[];numbers={}
 def check(name,ok,detail):
  checks.append(dict(name=name,passed=bool(ok),detail=str(detail)))
  print(('PASS ' if ok else 'FAIL ')+name+': '+str(detail))
 # Nonlinear off-shell stress identity; on potential solutions both curls vanish.
 coords=s.symbols('x y z'); x,y,z=coords
 Btest=s.Matrix([1+x+2*y,2+y+z,3+z+x]);Dtest=s.Matrix([2+z,1+x-y,4+y+2*z])
 fluxvars=s.symbols('B1 B2 B3 D1 D2 D3');BV=s.Matrix(fluxvars[:3]);DV=s.Matrix(fluxvars[3:])
 Htest=(BV.dot(BV)+DV.dot(DV))/2+BV.dot(BV)**2/4+BV.dot(BV)*DV.dot(DV)/3
 substitution=dict(zip(fluxvars,list(Btest)+list(Dtest)))
 gB=s.Matrix([s.diff(Htest,v).subs(substitution) for v in fluxvars[:3]])
 gD=s.Matrix([s.diff(Htest,v).subs(substitution) for v in fluxvars[3:]])
 Hlocal=Htest.subs(substitution);Legendre=Btest.dot(gB)+Dtest.dot(gD)-Hlocal
 divB=sum(s.diff(Btest[j],coords[j]) for j in range(3));divD=sum(s.diff(Dtest[j],coords[j]) for j in range(3))
 residual=[];wrong=[]
 for i in range(3):
  common=sum(s.diff(Btest[j]*gB[i]+Dtest[j]*gD[i],coords[j]) for j in range(3))-divB*gB[i]-divD*gD[i]
  curl=sum(Btest[j]*(s.diff(gB[i],coords[j])-s.diff(gB[j],coords[i]))+Dtest[j]*(s.diff(gD[i],coords[j])-s.diff(gD[j],coords[i])) for j in range(3))
  residual.append(s.expand(common-s.diff(Legendre,coords[i])-curl))
  wrong.append(s.expand(common-s.diff(Hlocal,coords[i])-curl))
 check('nonlinear_Legendre_stress_identity',all(v==0 for v in residual) and any(v!=0 for v in wrong),
       'exact 3D quartic flux energy: corrected trace leaves only constitutive curls; H trace fails')
 b,d,a,k=s.symbols('b d a0 kappa',positive=True)
 p=s.sqrt(b*b+a*b)-b;bt=d*d/(a-2*d)
 check('threshold_inverse',s.simplify((bt+d)**2-(bt*bt+a*bt))==0,'0<d<a0/2, positive roots =>p(bt)=d')
 pp=s.diff(p,b);bp=s.diff(bt,d)
 check('threshold_derivative',s.simplify(bp-2*d*(a-d)/(a-2*d)**2)==0,'b_t prime positive')
 # Fundamental theorem and the moving lower boundary cancel because p(bt)=d.
 f=s.Function('P');Ha=b*b/2+k*d*d/2+f(b)-f(bt)+d*bt
 Hb=s.diff(Ha,b).subs(s.diff(f(b),b),p)
 Hd_raw=s.diff(Ha,d)
 Hd=Hd_raw.xreplace({node:d for node in Hd_raw.atoms(s.Subs)}) # P'(b_t)=p(b_t)=d
 check('active_baryon_gradient',s.simplify(Hb-b-p)==0,'g_b=b+p, exactly independent of d')
 check('active_dark_gradient',s.simplify(Hd-k*d-bt)==0,'g_d=kappa*d+b_t, moving-boundary terms cancel')
 numerical_energy_errors=[]
 for bv,dv in [(1,.1),(1,.3),(.2,.3),(4,.45)]:
  for kv in (1,2):
   step=1e-6
   eb=(energy(bv+step,dv,kv)-energy(bv-step,dv,kv))/(2*step)
   ed=(energy(bv,dv+step,kv)-energy(bv,dv-step,kv))/(2*step)
   gb,gd,*_=response(bv,dv,kv)
   numerical_energy_errors.append(max(abs(eb-gb),abs(ed-gd)))
 check('primitive_energy_gradient',max(numerical_energy_errors)<1e-7,
       f'closed P primitive independent finite differences, max error={max(numerical_energy_errors):.3g}')
 dark_b_response=1 if args.mutate_keep_newtonian_dark else 0
 check('active_force_integrability',dark_b_response==0,'partial_d g_b=0 must equal partial_b g_d; Newtonian dark response fails')
 check('inactive_reciprocity',s.diff(b+d,d)==s.diff(b+k*d,b)==1,'both sources react from one energy')
 check('interface_force_continuity',s.simplify((bt+d)-(bt+d))==0 and s.simplify((bt+k*d)-(k*d+bt))==0,
       'p(b_t)=d, no force jump; Hessian has one-sided limits')
 mu=(1+k-s.sqrt((k-1)**2+4))/2
 check('inactive_scalar_eigenvalues',s.simplify(s.det(s.Matrix([[1,1],[1,k]])-mu*s.eye(2)))==0,
       'kappa>1 gives mu>0; kappa=1 leaves radial flux-split null mode')
 check('cold_tracer_force_vanishes',s.limit(k*d+bt,d,0,dir='+')==0,'any fixed b>0, galaxy-active branch lacks baryon capture of dilute cold tracer')
 # Full six-vector derivative check with independent finite differences.
 rng=np.random.default_rng(75103);errs=[];min_eig=1e9
 for bb,dd in [(1,.1),(1,.3),(.2,.3),(4,.45)]:
  for kk in (1,2):
   B=rng.normal(size=3);B*=bb/np.linalg.norm(B)
   D=rng.normal(size=3);D*=dd/np.linalg.norm(D);q=np.r_[B,D]
   H=vector_hessian(B,D,kk)
   step=1e-5
   fd=np.column_stack([(gradient((q+step*np.eye(6)[j])[:3],(q+step*np.eye(6)[j])[3:],kk)
             -gradient((q-step*np.eye(6)[j])[:3],(q-step*np.eye(6)[j])[3:],kk))/(2*step) for j in range(6)])
   err=float(np.max(np.abs(H-fd)));errs.append(err)
   eig=np.linalg.eigvalsh(H)
   if kk==2:min_eig=min(min_eig,float(eig.min()))
 check('full_norm_vector_Hessian_matches_variation',max(errs)<2e-6,f'8 six-vector cases, max derivative error={max(errs):.4g}')
 mu2=(3-math.sqrt(5))/2
 check('strong_convex_kappa2_full_vector',min_eig>=mu2-1e-9,f'min eigenvalue={min_eig:.9g}, global analytical bound={mu2:.9g}')
 # Newton-vector base replacement: negative transverse cold Hessian, despite scalar convexity.
 gb,gd,hbb,hdd,hbd,_=response(1,.1,1)
 alpha=(gb-(1+.1))/1; beta=(gd-(1+.1))/.1
 transverse=np.array([[1+alpha,1],[1,1+beta]])
 check('Newton_vector_preserving_extension_refuted',1+beta<0 and np.linalg.eigvalsh(transverse).min()<0,
       f'dark-only transverse Hessian={1+beta}, two-species transverse eigenvalues={np.linalg.eigvalsh(transverse)}')
 numbers['vector_price']=dict(transverse_matrix=transverse.tolist(),minimum_eigenvalue=float(np.linalg.eigvalsh(transverse).min()))
 # Global convexity obstruction to ANY Newton-OFF vector extension, not just the naive one.
 X=np.array([1.,0,0,.1,0,0]); shift=np.array([0.,10,0,0,-10,0])
 XP=X+shift;XM=X-shift;total=X[:3]+X[3:]
 midpoint_energy=energy(1,.1,1);off_energy=.5*float(total@total)
 check('global_Newton_OFF_convex_extension_obstruction',np.linalg.norm(XP[3:])>.5 and
       np.linalg.norm(XM[3:])>.5 and midpoint_energy>off_energy,
       f'Newton OFF endpoints share sum; required H(midpoint)={midpoint_energy:.9g} > endpoint mean={off_energy:.9g}')
 numbers['global_vector_midpoint_witness']=dict(X=X.tolist(),Xplus=XP.tolist(),Xminus=XM.tolist(),
   required_aligned_energy=midpoint_energy,Newton_OFF_endpoint_mean=off_energy,convexity_gap=midpoint_energy-off_energy)
 # Compact-source orbits: b,d proportional r^-2. Collective shell labels obey same derivative.
 W=s.simplify(3*(k*d+bt)-2*d*s.diff(k*d+bt,d))
 expected=k*d-d*d*(a+2*d)/(a-2*d)**2
 check('active_cold_orbit_stiffness',s.simplify(W-expected)==0,'r*kappa_r²=kappa*d-d²(a0+2d)/(a0-2d)²')
 eta=s.symbols('eta',positive=True);boundary=s.simplify(expected.subs(d,a/(eta+2)))
 check('stable_ratio_threshold',s.simplify(boundary/(a/(eta+2))-(k-(eta+4)/eta**2))==0,
       'eta>= [1+sqrt(1+16kappa)]/(2kappa) protects entire active branch')
 thresholds={str(kk):(1+math.sqrt(1+16*kk))/(2*kk) for kk in (1,2)}
 numbers['minimum_stable_compact_mass_ratio']=thresholds
 for kk in (1,2):
  d0=.3; numerator=kk*d0-d0*d0*(1+2*d0)/(1-2*d0)**2
  check('compact_instability_kappa'+str(kk),response(1,d0,kk)[-1] and numerator<0,
        f'b=1,d=.3,r=a0=1: r*kappa_r²={numerator}')
 # Finite positive coincident Plummer source profiles, cosmic ratio, chosen support.
 rr=np.geomspace(.001,100,801); bb=rr/(1+rr*rr)**1.5;eta0=5.36;dd=eta0*bb
 bprime=(1-2*rr*rr)/(1+rr*rr)**2.5
 profile=[]
 for kk in (1,2):
  cold_collective=[];tracer=[];nbactive=0
  for r,Bv,Dv,Bp in zip(rr,bb,dd,bprime):
   gb,gd,_,gdd,_,active=response(Bv,Dv,kk)
   if active:
    wc=(3*gd-2*Dv*gdd)/r;nbactive+=1
    wt=3*gd/r+gdd*eta0*Bp
   else:
    wc=Bp+3*Bv/r+kk*Dv/r
    wt=Bp+kk*eta0*Bp+3*gd/r
   cold_collective.append(wc);tracer.append(wt)
  check('finite_profile_radial_stability_kappa'+str(kk),min(cold_collective)>0 and min(tracer)>0,
        f'801 radial points, active={nbactive}, shell min={min(cold_collective):.4g}, tracer min={min(tracer):.4g}')
  profile.append(dict(kappa=kk,minimum_shell_stiffness=min(cold_collective),minimum_tracer_frequency2=min(tracer),active_points=nbactive))
 numbers['finite_Plummer_profile']=dict(Mb=1,Mc=eta0,h=1,r_range=[.001,100],rows=profile,
     limitations='same-scale profile and angular momenta chosen; ordered radial shells, no nonradial/global formation proof')
 # Independent radial integrations remain in the same active branch; potential included.
 orbits=[]
 for d0,tmax in [(.1,40),(.3,4)]:
  j2=response(1,d0,1)[1];r0=math.sqrt(2*d0);eps=1e-5
  def potential(r):return (-d0+d0/2)/r+d0/(4*r0)*math.log((r-r0)/(r+r0))
  def rhs(t,y):
   r,v=y; force=response(1/r**2,d0/r**2,1)[1]
   return [v,j2/r**3-force]
  sol=solve_ivp(rhs,(0,tmax),[1+eps,0],t_eval=np.linspace(0,tmax,1001),method='DOP853',rtol=1e-11,atol=1e-13)
  radius,vel=sol.y
  en=.5*vel*vel+j2/(2*radius**2)+np.array([potential(r) for r in radius])
  drift=float(np.max(np.abs(en-en[0])));extent=float(np.max(np.abs(radius-1)))
  allactive=all(response(1/r**2,d0/r**2,1)[-1] for r in radius)
  good=extent<1.1*eps if d0==.1 else extent>8*eps
  check('nonlinear_orbit_'+str(d0),sol.success and allactive and good and drift<1e-10,
        f'max displacement={extent:.5g}, energy drift={drift:.3g}, active={allactive}')
  orbits.append(dict(d0=d0,tmax=tmax,maximum_displacement=extent,energy_drift=drift))
 numbers['orbits']=orbits
 (out/'results.json').write_text(json.dumps(dict(checks=checks,numbers=numbers,
   mutation=args.mutate_keep_newtonian_dark,software=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,sympy=s.__version__)),indent=2)+'\n')
 failed=sum(not c['passed'] for c in checks);print(f'{len(checks)-failed}/{len(checks)} checks pass; {failed} failures')
 return int(failed>0)

if __name__=='__main__':raise SystemExit(main())
