import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',choices=['none','frozen_curvature','erase_volume','half_density'],default='none');args=ap.parse_args();checks=[]
def eq(n,v):v=s.simplify(s.expand(v));checks.append(dict(name=n,passed=v==0,residual=str(v)))
def ck(n,b):checks.append(dict(name=n,passed=bool(b)))
H,K,a,k,t,a0,A=s.symbols('H K a k t a0 A',positive=True);M=2*K;P=k*k/a**2;Lam=3*H**2
z,zd,zdd,nu,nd,ndd,e,ed,b,D=s.symbols('z zd zdd nu nd ndd e ed b D',real=True)
B=b+ed/P
Bsol=-(z+nu)/H
Phi=-(z+H*Bsol);Psi=nu-(zd+nd)/H
on={zd:H*nu,nd:-H*nu,ndd:H*H*nu,zdd:-H*H*nu}
eq('actual_relative_Phi',Phi-nu);eq('actual_relative_Psi_on_EL',Psi.subs(on)-nu)
# For physical g, unsourced mean Bardeen potentials vanish; each is halfrelative.
Ph=nu/2;Ps=nu/2;Pd=nd/2;Pdd=ndd/2;Psd=nd/2
Y=Pd+H*Ps
eq('visible_momentum_geometric_zero',Y.subs(on))
W=(Ph+Ps)/2;eq('visible_Weyl',W-nu/2)
# Full covariant volume variation, then subtract matched individual vacuum.
eps,qg,qh=s.symbols('eps qg qh');ratio=s.sqrt((1+eps*qh)/(1+eps*qg))
ratio1=s.diff(ratio,eps).subs(eps,0).subs(qh,qg-D)
eq('volume_ratio_firstvariation',ratio1+D/2)
rhov=M*Lam*ratio1;pv=-M*Lam*ratio1
eq('actual_volume_density',rhov+M*Lam*D/2);eq('actual_volume_pressure',pv-M*Lam*D/2)
# Quadratic projected interaction varies linearly only through each lapse: grad action K a (gradnu)^2.
# Spatial integration by parts yields EL_ng= -2K a Delta nu = +2K a k²nu.
el_ng=2*K*a*k*k*nu;rhoI=-el_ng/a**3
eq('actual_lapse_gradient_density',rhoI+M*P*nu)
rho=rhov+rhoI;press=pv
candidate_rhov=0 if args.control=='erase_volume' else rhov
candidate_rhoI=-M*P*nu/2 if args.control=='half_density' else rhoI
eq('source_volume_density_retained',candidate_rhov+M*Lam*D/2)
eq('source_gradient_normalization',candidate_rhoI+M*P*nu)
eq('each_vs_relative_source_factor',2*rho+M*Lam*D+2*M*P*nu)
# D=0: geometric scalar Einstein equations against fixed M and matched Lambda.
if args.control=='frozen_curvature':Ph=-z/2;Ps=0;Pd=-zd/2;Pdd=-zdd/2;Psd=0
Y=Pd+H*Ps
rhog=-2*M*(P*Ph+3*H*Y)
eq('actual_Einstein00_density',rhog.subs(on)-rho.subs(D,0))
Rgeom=-6*Pdd-6*H*(Psd+4*Pd)-24*H*H*Ps+2*P*(Ps-2*Ph)
eq('actual_geometric_trace_pressure',Rgeom.subs(on)-(rho-3*press).subs(D,0)/M)
eq('zero_interaction_anisotropic_stress',Ph-Ps)
# Separate on-shell stress conservation, not individual offshell diffeomorphism symmetry.
Dd=s.symbols('Dd');rho_dot=-M*Lam*Dd/2-M*(-2*H*P*nu+P*nd)
eq('energy_residual_with_clock_constraints',rho_dot+3*H*(rho+press)+M*Lam*Dd/2+M*P*(nd+H*nu))
eq('on_shell_dust_conservation',(rho_dot+3*H*(rho+press)).subs({D:0,Dd:0,nd:-H*nu}))
eq('on_shell_pressure_zero',press.subs(D,0))
# Explicit twointegrationconstants including invisible frozen mode.
z0,z1=s.symbols('z0 z1',real=True);zmode=z0+z1*s.exp(-H*t);numode=s.diff(zmode,t)/H
Wmode=numode/2;rho_mode=-M*k*k*s.exp(-2*H*t)*numode
eq('exact_scalar_mode_equation',s.diff(zmode,t,2)+H*s.diff(zmode,t))
eq('frozen_mode_Weyl_invisible',Wmode.subs(z1,0))
eq('frozen_mode_density_invisible',rho_mode.subs(z1,0))
eq('decaying_Weyl_law',s.diff(Wmode,t)+H*Wmode)
eq('comoving_density_constant',s.diff(s.exp(3*H*t)*rho_mode,t))
# Periodic nonzero Fourier mode has signed zero mean, not a positivehomogeneouspopulation.
x=s.symbols('x',real=True);profile=-s.cos(x)
eq('periodic_source_zero_mean',s.integrate(profile,(x,0,2*s.pi)))
ck('periodic_source_both_signs',profile.subs(x,0)<0 and profile.subs(x,s.pi)>0)
# Exact previouslyaudited homogeneous solution carries only vacuum.
n,q,zinf=s.symbols('n q zinf',real=True);zet=zinf-2*s.asinh(q)/n;r=n*zinf+2*s.asinh(q)
eq('homogeneous_volume_trace_constant',r+n*zet-2*n*zinf)
eq('homogeneous_physical_vacuum_factor',s.exp(-(r+n*zet)/2)-s.exp(-n*zinf))
ck('homogeneous_stress_no_dust_scaling',s.diff(s.exp(-n*zinf),q)==0)
# Quadraticcanonicalenergy is a distinct, unvaried secondorderbackground question.
Pi=s.symbols('Pi',real=True);Hcan=H*H*Pi*Pi/(4*K*k*k*s.exp(H*t))
momentum=2*K*k*k*s.exp(H*t)*s.diff(zmode,t)/H**2
eq('canonical_momentum_conserved',s.diff(momentum,t))
eq('density_conserved_momentum_dictionary',rho_mode+H*momentum*s.exp(-3*H*t))
eq('Weyl_conserved_momentum_dictionary',Wmode-H*momentum/(4*K*k*k*s.exp(H*t)))
eq('canonical_energy_coordinate_scaling',s.diff(Hcan,t)+H*Hcan)
ck('canonical_temporal_energy_nonnegative',Hcan.is_nonnegative)
out=dict(passed=sum(r['passed'] for r in checks),total=len(checks),checks=checks,control=args.control,scope='n3 coincident on-shell deS,k>0 finite linear relative scalar; physicalfixedM interactionstress withvacuumsubtraction')
p=Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2));print(json.dumps(dict(passed=out['passed'],total=out['total'],failed=[r for r in checks if not r['passed']])));sys.exit(out['passed']!=out['total'])
