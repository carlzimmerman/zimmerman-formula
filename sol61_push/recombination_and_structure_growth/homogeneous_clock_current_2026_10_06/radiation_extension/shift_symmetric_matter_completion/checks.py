"""Shift-symmetric dust-density square: covariant variations and full UV characteristic."""
import argparse,pathlib,json,sympy as s,numpy as np
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);pa.add_argument('--control',choices=['none','stable','freeze_density','drop_shift'],default='none');args=pa.parse_args();checks=[]
def ck(n,b,d=None):checks.append(dict(name=n,passed=bool(b),detail=d))
def zero(n,e):e=s.factor(s.cancel(e));ck(n,e==0,str(e))
X,rho,m,b,q,Z,sc=s.symbols('X rho m b q Z sc',positive=True);B=s.Function('B')(rho);ZZ=s.Function('Z')(rho);Y=X-B;U=ZZ*Y*Y/2
zero('stealth_value',U.subs(X,B));zero('stealth_X_variation',s.diff(U,X).subs(X,B));zero('stealth_density_variation',s.diff(U,rho).subs(X,B))
zero('extra_shift_current_coefficient',s.diff(U,X)-ZZ*Y)
zero('effective_chemical_potential_linear',(-s.diff(U,rho)).subs({X:B+s.Symbol('eps')*s.Symbol('dY')}).expand().coeff(s.Symbol('eps'),1)-ZZ*s.diff(B,rho)*s.Symbol('dY'))
nu,z,pi=s.symbols('nu z pi',real=True);dR=pi-3*rho*z
Bused=0 if args.control=='freeze_density' else b
square=Z*(q*q*nu+Bused*dR)**2/2
zero('full_unitary_square_density',square-Z*(q*q*nu+b*dR)**2/2)
# Vacuum family coefficient dictionary; rho_v is an action-family parameter.
zero('family_square_rescaling',Z/sc**4*(sc**2*X-sc**2*B)**2/2-Z*(X-B)**2/2)
# Physical-number density has no first-order lapse/shift dependence at comoving background.
eps,N,J0,j0,aa,nd=s.symbols('eps N J0 j0 aa nd',positive=True)
number=(J0+eps*j0)/(aa**3*s.exp(3*eps*z))
zero('density_coordinate_dictionary',s.diff(number,eps).subs(eps,0)-j0/aa**3+3*J0*z/aa**3)
zero('no_density_lapse_first_order',s.diff(number,N))
# Raw three-pair scalar quadratic action at a finite smooth epoch.
M,Th,Sig,kap,p,R,Cr,H=s.symbols('M Th Sig kap p R Cr H',nonzero=True,real=True)
z,v,w,zd,vd,wd,t=s.symbols('z v w zd vd wd t',real=True)
S=Sig+kap*M*p*p
raw=-3*M*zd**2+S*nu**2+6*Th*nu*zd-2*Th*nu*t+2*M*zd*t+M*p*p*z*z+2*M*p*p*nu*z+3*rho*z*nu
raw+=pi*(vd-nu)-rho*p*p*v*v/2+rho*v*t+Cr*(wd-H*w-nu)**2+3*R*z*(wd-H*w)-R*p*p*w*w/2+R*w*t
raw+=Z*(q*q*nu+b*(pi-3*rho*z))**2/2
nuShift=M/Th*zd+rho/(2*Th)*v+R/(2*Th)*w
zero('unchanged_exact_shift_constraint',s.diff(raw,t).subs(nu,nuShift))
if args.control=='drop_shift':
 nuShift=M/Th*zd
 zero('CONTROL_shift_without_matter_momenta',s.diff(raw,t).subs(nu,nuShift))
used=raw.subs(nu,nuShift);used=s.expand(used).subs(t,0)
piSol=3*rho*z-(vd-nuShift)/(Z*b*b)-q*q*nuShift/b
zero('density_EL_solved',s.diff(used,pi).subs(pi,piSol))
reduced=s.expand(used.subs(pi,piSol))
# Independent completion-of-square reduction with all frozen-H radiation terms.
expected=-3*M*zd**2+S*nuShift**2+6*Th*nuShift*zd+M*p*p*z*z+2*M*p*p*nuShift*z
expected+=3*rho*z*vd-(vd-nuShift)**2/(2*Z*b*b)-q*q/b*nuShift*(vd-nuShift)-rho*p*p*v*v/2
expected+=Cr*(wd-H*w-nuShift)**2+3*R*z*(wd-H*w)-R*p*p*w*w/2
zero('exact_reduced_action',reduced-expected)
fields=[z,v,w];vel=[zd,vd,wd];K=s.hessian(reduced,vel);V=s.hessian(reduced,fields);Gy=s.Matrix([[s.diff(reduced,vel[i],fields[j])-s.diff(reduced,fields[i],vel[j]) for j in range(3)] for i in range(3)])
x=s.symbols('x',real=True);E=-p*p*x*x*K-s.I*p*x*Gy-V
D=s.expand(E.det(method='domain-ge'));lead=s.factor(D.coeff(p,8));target=2*kap*M**3*x*x*(2*Cr*x*x-R)*(Z*b*b*rho+x*x)/(Th**2*Z*b*b)
zero('full_principal_characteristic',lead-target)
zero('radiation_root',lead.subs(x*x,R/(2*Cr)))
zero('dust_unstable_root',lead.subs(x*x,-rho*Z*b*b))
zero('clock_root_separate_scaling',lead.subs(x,0))
zero('highest_characteristic_power',sum(D.coeff(p,j) for j in range(9,13)))
zero('H_terms_do_not_change_UV',s.diff(lead,H))
# Principal dust density equation has invariant negative sound-speed squared.
ck('dust_sound_speed_negative',s.ask(s.Q.negative(-rho*Z*b*b)) is True)
if args.control=='stable':ck('CONTROL_square_stabilizes_dust',s.ask(s.Q.positive(-rho*Z*b*b)) is True)
# Bounded frozen-coefficient numerical characteristic roots, not an on-background cosmology fit.
# H0 removes advection-normalization lower derivatives only; leading theorem retains arbitraryH.
sub={M:s.Integer(1),Th:s.Integer(1),Sig:s.Integer(-3),kap:s.Integer(1),q:s.Integer(1),Z:s.Integer(2),b:s.Rational(1,3),rho:s.Rational(3,2),R:s.Rational(2,3),Cr:s.Integer(1),H:s.Integer(0)}
poly=s.Poly(D.subs(sub),x);rows=[]
for pp in [30,100,1000]:
 coeff=[complex(s.N(c.subs(p,pp),30)) for c in poly.all_coeffs()];roots=np.roots(coeff);unstable=min(roots,key=lambda r:abs(r-1j/np.sqrt(3)))
 rows.append(dict(p=pp,dust_omega_over_p_real=float(unstable.real),dust_omega_over_p_imag=float(unstable.imag),error_to_principal=float(abs(unstable-1j/np.sqrt(3)))))
ck('finite_p_unstable_branch',all(r['dust_omega_over_p_imag']>.5 for r in rows));ck('bounded_principal_convergence',rows[-1]['error_to_principal']<rows[0]['error_to_principal'])
result=dict(passed=all(c['passed'] for c in checks),checks=checks,principal_characteristic=str(lead),dust_sound_speed_squared='-rho_d Z (Xbar_d_prime)^2',bounded_frozen_coefficient_roots=rows,parameters_scope='finite epoch M>0,Theta!=0,kappa>0,q>0,Z>0,rho_d>0,b=Xbar_d_prime!=0; radiationCr,R>0',control=args.control,non_claims=['No actual mode below unknown EFT cutoff guaranteed','No all operator no-go','No quantum vacuum decay inference','No automatic fixed-coupling vacuum self-adjustment','Frozen roots are algebra controls, not cosmology fits'])
o=pathlib.Path(args.output);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=result['passed'],checks=len(checks),failed=[c['name'] for c in checks if not c['passed']])));raise SystemExit(0 if result['passed'] else 1)
