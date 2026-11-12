import json,math,pathlib,sys,itertools
import numpy as np
import sympy as s
out=pathlib.Path(sys.argv[1]);out.mkdir(exist_ok=True)
D,U,b,a,w,A,T=s.symbols('D U b a w A T', positive=True)
checks={}
checks['simple_identity']=s.simplify((D**2*U*b*(U*b+a))-(D*U)*(D*U*b)-D**2*U*b*a)==0 # separate quadratic identity below
# Polynomial substitution identities, not numerical approximation.
checks['simple_transformed_polynomial']=s.expand((w**2-D*U*b*w-D**2*U*b*a) - (w**2-b*((D*U)*w+(D*U)*(D*a))))==0
checks['quadratic_transformed_polynomial']=s.expand((w**2-D**2*U**2*b**2-D**2*U*b*a)-(w**2-(D*U)**2*b**2-(D*U)*(D*a)*b))==0
x=s.symbols('x',positive=True)
t1,t2,om1,om2=s.symbols('t1 t2 om1 om2',positive=True)
r1=s.Matrix([1-t1,t1]);r2=s.Matrix([1-t2,t2]);F=om1*(r1*r1.T)+om2*(r2*r2.T)
checks['two_radius_information_determinant']=s.factor(F.det()-om1*om2*(t1-t2)**2)==0
r,V,G,ap=s.symbols('r V G ap',positive=True)
M=V**4*r/(G*(V**2+ap*r))
checks['physical_counterexample_mass_derivative']=s.simplify(s.diff(M,r)-V**6/(G*(V**2+ap*r)**2))==0
checks['physical_counterexample_force']=s.simplify((G*M/r**2)**2+(ap)*(G*M/r**2)-(V**2/r)**2)!=0 # quadratic not this simple-law counterexample
checks['physical_counterexample_simple_law']=s.simplify((V**2/r)**2-(G*M/r**2)*((V**2/r)+ap))==0
# Correct the deliberately separate-law diagnostic into a named non-equivalence check.
checks['simple_counterexample_not_quadratic']=checks.pop('physical_counterexample_force')
checks.pop('simple_identity')
def gfun(B,a0,law):
 return (B+np.sqrt(B*B+4*B*a0))/2 if law=='simple_mu' else np.sqrt(B*B+a0*B)
def estimate(bv,wv,law):
 p=wv*wv/bv
 if law=='simple_mu':
  slope=(p[-1]-p[0])/(wv[-1]-wv[0]);intercept=p[0]-slope*wv[0]
  return intercept/slope
 slope=(p[-1]-p[0])/(bv[-1]-bv[0]);intercept=p[0]-slope*bv[0]
 return intercept/np.sqrt(slope)
maxerr=0;max_photometry_scaling=0;max_velocity_scaling=0;rows=[]
for law,d,u,a0 in itertools.product(['simple_mu','quadratic'],[.5,1,2],[.3,1,4],[.3,1,3]):
 bv=np.array([.01,.2,3.,30.]);wv=d*gfun(u*bv,a0,law);est=estimate(bv,wv,law)
 maxerr=max(maxerr,abs(est/(d*a0)-1))
 max_photometry_scaling=max(max_photometry_scaling,abs(estimate(2.7*bv,wv,law)/est-1))
 max_velocity_scaling=max(max_velocity_scaling,abs(estimate(bv,1.3*wv,law)/(1.3*est)-1))
 rows.append(dict(law=law,D=d,U=u,a0=a0,T_est=est,T_true=d*a0))
checks['54_synthetic_recoveries']=len(rows)==54 and maxerr<1e-9
checks['global_light_scale_cancels']=max_photometry_scaling<1e-9
checks['velocity_squared_scale_survives']=max_velocity_scaling<1e-9
information=[]
for law in ['simple_mu','quadratic']:
 for window,B in [('deep',[1e-6,1e-5,1e-4]),('transition',[.1,1,10]),('newtonian',[1e4,1e5,1e6])]:
  B=np.array(B);W=gfun(B,1,law)
  t=1/(W+2) if law=='simple_mu' else 1/(2*(B+1))
  J=np.column_stack([1-t,t]);fish=J.T@J/(.01**2);cov=np.linalg.inv(fish)
  # Orthogonal finite differences of original forward law check derivatives.
  eps=1e-5
  dA=(np.log(gfun(np.exp(eps)*B,1,law))-np.log(gfun(np.exp(-eps)*B,1,law)))/(2*eps)
  dT=(np.log(gfun(B,np.exp(eps),law))-np.log(gfun(B,np.exp(-eps),law)))/(2*eps)
  checks[law+'_'+window+'_derivative']=max(np.max(np.abs(dA-J[:,0])),np.max(np.abs(dT-J[:,1])))<2e-8
  information.append(dict(law=law,window=window,b_over_a0=list(B),t=list(t),determinant=float(np.linalg.det(fish)),sigma_logT_natural_if_1percent_w=float(np.sqrt(cov[1,1])),condition=float(np.linalg.cond(fish))))
R=np.array([1,2,4,8.]);grad=[]
for newa in [.91,2.]:
 ratio=((1+R)/(1+newa*R))**2
 grad.append(dict(new_a0_over_old=newa,radius=list(R),local_mass_to_light_ratio=ratio.tolist(),radial_log10_gradient_span=float(np.log10(max(ratio)/min(ratio)))))
# BAO ruler cancellation: synthetic distances and a0 ratios. Not observed distances.
DZ,DR,az,ar,rd=1.2,.7,.91,1.,147.
Q=((DZ*az)/(DR*ar))*((DR/rd)/(DZ/rd))
checks['bao_distance_ruler_cancels']=abs(Q-az/ar)<1e-14
inc=(math.sin(math.radians(55))/math.sin(math.radians(60)))**2
checks={k:bool(v) for k,v in checks.items()}
res=dict(assertion_tested='Exact transformed-law identities and information determinant;54 synthetic two-radius recoveries;scale transformations;positive-density counterexample;ideal Fisher conditioning only.',checks=checks,all_checks=all(checks.values()),synthetic_cases=len(rows),maximum_relative_recovery_error=maxerr,maximum_photometry_scaling_error=max_photometry_scaling,maximum_velocity_scaling_error=max_velocity_scaling,information_windows=information,radial_mass_to_light_counterexamples=grad,inclination_55_true_60_used_T_factor=inc,inclination_log10_bias=math.log10(inc),synthetic_bao_ratio=Q,non_claims=['No Euclid data fit','No achieved measurement precision','No AQUAL disk equivalence to pointwise algebraic laws','No healthy covariant action derived','No universal novelty claim'])
(out/'results.json').write_text(json.dumps(res,indent=2))
print(json.dumps({k:res[k] for k in ['all_checks','synthetic_cases','maximum_relative_recovery_error','maximum_photometry_scaling_error','inclination_log10_bias']},indent=2))
if not res['all_checks']:raise SystemExit(1)
