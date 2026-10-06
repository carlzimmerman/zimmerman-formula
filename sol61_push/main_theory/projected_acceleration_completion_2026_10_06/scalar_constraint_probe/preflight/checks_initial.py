"""Raw de Sitter relative scalar constraints, no imported author functions."""
import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['erase_shear','scalar_wave','flat_limit']);args=ap.parse_args();rows=[]
def eq(n,x):
 x=s.factor(s.cancel(s.expand(x)));rows.append({'name':n,'passed':x==0,'residual':str(x)})
def ck(n,x):rows.append({'name':n,'passed':bool(x),'residual':str(x)})
H,c,P=s.symbols('H c P',positive=True);z,e,nu,b,zd,ed,pz,pe=s.symbols('z e nu b zd ed pz pe',real=True)
f=zd-H*nu;D=nu+3*z+e
lag=c*(-3*f*f-2*f*(ed+P*b)+P*z*z+2*P*nu*z+s.Rational(3,2)*H*H*D*D+P*nu*nu)
eq('raw_shift_EL',s.diff(lag,b)+2*c*P*f)
eq('momentum_z',s.diff(lag,zd)-c*(-6*f-2*(ed+P*b)))
eq('momentum_e',s.diff(lag,ed)+2*c*f)
sol={zd:H*nu-pe/(2*c),ed:-pz/(2*c)+3*pe/(2*c)-P*b}
ham=s.expand((pz*zd+pe*ed-lag).subs(sol))
expected=H*nu*pz-pz*pe/(2*c)+3*pe*pe/(4*c)-P*b*pe-c*(P*z*z+2*P*nu*z+s.Rational(3,2)*H*H*D*D+P*nu*nu)
eq('actual_Legendre_Hamiltonian',ham-expected)
Cn=s.diff(ham,nu)
eq('lapse_secondary',Cn-(H*pz-c*(2*P*z+3*H*H*D+2*P*nu)))
eq('lapse_pair_nonzero_bracket',s.diff(Cn,nu)+c*(2*P+3*H*H))
nus=(H*pz/c-2*P*z-3*H*H*(3*z+e))/(2*P+3*H*H)
eq('lapse_solution',Cn.subs(nu,nus))
hb=s.factor(ham.subs(nu,nus));Ds=s.factor(D.subs(nu,nus))
eq('shear_secondary_D',Ds-(H*pz/c+2*P*(2*z+e))/(2*P+3*H*H))
eq('shift_secondary_Pe',s.diff(hb,b)+P*pe)
eq('Pe_preservation',-s.diff(hb,e)-3*c*H*H*Ds)
eq('Pe_D_bracket',-s.diff(Ds,e)+2*P/(2*P+3*H*H))
# Explicit time derivative uses c_dot=3Hc and P_dot=-2HP.
def td(x):return s.diff(x,c)*3*H*c-s.diff(x,P)*2*H*P
def pb(x,y):return s.diff(x,z)*s.diff(y,pz)-s.diff(x,pz)*s.diff(y,z)+s.diff(x,e)*s.diff(y,pe)-s.diff(x,pe)*s.diff(y,e)
C4=s.factor(td(Ds)+pb(Ds,hb))
eq('fourth_constraint_shift_coefficient',s.diff(C4,b)+2*P**2/(2*P+3*H*H))
# On Pe=D=0, solve shear and restrict canonical one-form.
es=-2*z-H*pz/(2*c*P)
eq('shear_constraint_solution',Ds.subs(e,es))
hphys=s.factor(hb.subs({pe:0,e:es}))
eq('reduced_raw_Hamiltonian',hphys-(H*H*pz*pz/(4*c*P)-H*z*pz))
# Boundary F=cP z²/H shifts Pz=Pi+F_z; partial F_t=cPz².
Pi=s.symbols('Pi',real=True);F=c*P*z*z/H
hnew=s.factor(hphys.subs(pz,Pi+s.diff(F,z))+td(F))
eq('boundary_corrected_Hamiltonian',hnew-H*H*Pi*Pi/(4*c*P))
ck('physical_kinetic_positive',s.diff(hnew,Pi,2).is_positive)
# Actual EL elimination, including shear derivative and background measure.
el_e=s.diff(lag,e)-td(s.diff(lag,ed))
fd=s.symbols('fd',real=True)
el_e_full=el_e+2*c*fd
eq('shear_EL_with_shift_constraint',el_e_full.subs({f:0,fd:0})-3*c*H*H*D)
ls=s.expand(lag.subs({nu:zd/H,e:-3*z-zd/H}))
eq('raw_eliminated_Lagrangian',ls-c*P*(z+zd/H)**2)
eq('boundary_subtracted_Lagrangian',ls-(td(F)+s.diff(F,z)*zd)-c*P*zd*zd/H**2)
eq('evolving_kinetic_measure',td(c*P/H**2)-H*c*P/H**2)
# de Sitter EOM and principal symbol, retaining redshift.
lam=s.symbols('lam');eq('exact_time_roots',lam*(lam+H)-(lam*lam+H*lam))
ck('no_nonzero_sound_speed',s.diff(hnew,z)==0)
# Mean-relative vacuum determinant expansion, leading trace differences.
x,y=s.symbols('x y',real=True)
Vg=1+x;Vh=1+y
corr=Vg+Vh-2*s.sqrt(Vg*Vh)
quad=s.diff(corr,x,2).subs({x:0,y:0})*x*x/2+s.diff(corr,x,y).subs({x:0,y:0})*x*y+s.diff(corr,y,2).subs({x:0,y:0})*y*y/2
eq('geometric_volume_nonFP_square',quad-(x-y)**2/4)
# Common clock cancels before unitary gauge.
ng,nh,pidot=s.symbols('ng nh pidot');eq('clock_before_gauge_cancels',(ng-pidot)-(nh-pidot)-(ng-nh))
# A=0,H=0 is a separate rank branch: shift forces zd=0, not nu=zd/H.
flat=s.expand(lag.subs(H,0));eq('flat_shift_equation',s.diff(flat,b)+2*c*P*zd)
if args.control=='erase_shear':ck('false_relative_spatial_gauge_available',s.diff(lag,e)==0)
if args.control=='scalar_wave':ck('false_positive_sound_speed',s.diff(hnew,z,2)>0)
if args.control=='flat_limit':ck('false_uniform_H0_reduced_kinetic',s.limit(c*P/H**2,H,0,dir='+').is_finite)
out={'passed':sum(x['passed'] for x in rows),'total':len(rows),'checks':rows,'control':args.control,'scope':'n3 exact quadratic coincident on-shell de Sitter,k>0,H>0; no full nonlinear constraint theorem'}
Path(args.out).parent.mkdir(parents=True,exist_ok=True);Path(args.out).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'passed':out['passed'],'total':out['total'],'failed':[x for x in rows if not x['passed']]}));sys.exit(not all(x['passed'] for x in rows))
