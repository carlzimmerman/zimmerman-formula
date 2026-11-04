import sys, json, hashlib, pathlib, platform, subprocess, time
import sympy as s
start=time.monotonic()
root=pathlib.Path('/Users/carlzimmerman/new_physics/zimmerman-formula')
out=pathlib.Path('/private/tmp/particle_field_audit_20261103')
# CP-slice exact Kähler inverse for one matter field and one modulus. No imported repo implementation.
n,H,P,Q,z,W,u=s.symbols('n H P Q z W u', real=True, nonzero=True)
Y=H-z*z/n; DH=P*P-H*Q
K=s.Matrix([[n*(P*P-Y*Q)/Y**2,-P*z/Y**2],[-P*z/Y**2,H/Y**2]])
DW=s.Matrix([-n*P*W/Y,u+z*W/Y])
exact=(DW.T*K.inv()*DW)[0]-3*W**2
stated=Y*u**2+(n-3)*W**2+Y*Q*(z*u-n*W)**2/(n*DH)
no_scale=s.factor(exact-stated)
# Canonical microscopic linear-W0 term from the actual real D-flat action.
x,a,b,h,lam,f,w0,eta=s.symbols('x a b h lam f w0 eta',real=True)
w=f*x-15*h*x*a*a+15*lam*a*a*b+w0
B=(f-15*h*a*a+x*w*eta)**2+30*a*a*(h*x-lam*b-w*eta)**2+30*(lam*a*a/2+b*w*eta)**2-3*w*w*eta
mixed=s.expand(B).coeff(eta,1).coeff(w0,1)
# Cartesian phase/radial cubic in canonical coordinates.
R,sg,aa=s.symbols('R sg aa',positive=True)
U=s.Function('U'); rr=s.sqrt((R+sg/s.sqrt(2))**2+aa*aa/2)
cubic=s.simplify(s.diff(U(rr),sg,aa,aa).subs({sg:0,aa:0}))
expected=(s.diff(U(R),R,2)-s.diff(U(R),R)/R)/(2*s.sqrt(2)*R)
# Hard-loop radial integral, using general D-dimensional Euclidean integral identity.
coeff=s.gamma(s.Rational(3,2))/s.gamma(s.Rational(7,2))
# Capped isothermal Jeans equation: a uniform positive rho at fixed dispersion cannot be equilibrium at g>0.
r,rho_cap,sigma,g=s.symbols('r rho_cap sigma g',positive=True)
jeans_residual=s.diff(rho_cap*sigma**2,r)+rho_cap*g
checks={
'protected_CP_1matter_inverse_metric_identity':no_scale==0,
'canonical_linear_W0_coefficient':s.simplify(mixed+4*f*x)==0,
'cartesian_radial_phase_cubic':s.simplify(cubic-expected)==0,
'hard_loop_integral_coefficient':coeff==s.Rational(4,15),
'capped_isothermal_Jeans_residual_nonzero':jeans_residual==rho_cap*g,
}
# Inspect actual current finite results, without executing scientific pipelines.
paths=[
'PHYSICS_CLAUDE_HANDOFF_2026-11-01.md',
'reviews/gravity_vacuum_production_2026_11_01/canonical_gravity/DERIVATION.md',
'reviews/gravity_vacuum_production_2026_11_01/canonical_gravity/shape.py',
'reviews/gravity_vacuum_production_2026_11_01/canonical_gravity/run_shape/result.json',
'reviews/gravity_vacuum_production_2026_11_01/protected_gravity/STATUS.md',
'reviews/gravity_vacuum_production_2026_11_01/production/STATUS.md',
'reviews/radial_ir_cold_2026_11_01/gapless_charge/gaugino_threshold.py',
'reviews/radial_ir_cold_2026_11_01/gapless_charge/decay_bound/DERIVATION.md',
'reviews/radial_ir_cold_2026_11_01/combine_loss_v2.py',
'reviews/radial_ir_cold_2026_11_01/run_loss_v2/result.json',
'rebuild_2026_10_22/HF1_hybrid_fermion/hf1_fermion.py',
'rebuild_2026_10_22/HF1_hybrid_fermion/hf1_g1.py',
'rebuild_2026_10_22/HF1_hybrid_fermion/hf1_g1_results.json',
'rebuild_2026_10_22/HF1_hybrid_fermion/README.md',
'real_research/yang_mills_layer_2026_10_28/correlation_c2/SHARED_EDGE_OPERATOR.md',
'real_research/yang_mills_layer_2026_10_28/correlation_c2/SHARED_EDGE_WEAK_GAP.md',
'real_research/yang_mills_layer_2026_10_28/correlation_c2/LOOP_GAP.md',
'real_research/yang_mills_layer_2026_10_28/correlation_c2/TORUS_FLUX_SCOPE.md',
'real_research/yang_mills_layer_2026_10_28/correlation_c2/WEIGHTED_RESOLVENT.md',
]
pins={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths}
shape=json.loads((root/paths[3]).read_text())
hf=json.loads((root/'rebuild_2026_10_22/HF1_hybrid_fermion/hf1_g1_results.json').read_text())
res={'command':'python3 -B /private/tmp/particle_field_audit_20261103/independent_checks.py','independent_of_repo_implementation':True,'checks':checks,'results':{'canonical_tadpole_W0_over_Mp2':str(mixed),'protected_CP_identity_residual':str(no_scale),'cubic':str(cubic),'hard_loop_integral_times_16pi2_M3':str(coeff),'capped_Jeans_residual':str(jeans_residual),'canonical_shape':{k:shape[k] for k in ['t_phase_closure','t_fold','mu_fold_e003_GeV','mchi_at_fold_e003_GeV','old_benchmark_force_over_max']},'HF1_label':hf['label']},'software':{'python':sys.version,'sympy':s.__version__,'platform':platform.platform()},'runtime_seconds':time.monotonic()-start,'input_sha256':pins,'git_head_observed':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'scope':'Tiny independent symbolic checks and stored-result inspection. No repo scientific run, fit, or numerical scan reproduced. One-matter CP no-scale identity does not independently check complex full-spectrum completion.'}
(out/'independent_checks_result.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({k:res[k] for k in ['checks','results','runtime_seconds','git_head_observed']},indent=2))
