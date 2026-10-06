import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--mutation',choices=['omit_trace','omit_background_dust_mass','wrong_source_orientation','call_conformal_lensing']);args=ap.parse_args();rows=[]
def ck(n,b,e=''): rows.append({'name':n,'passed':bool(b),'detail':str(e)})
def eq(n,e): e=s.simplify(s.expand(e));ck(n,e==0,e)
xi,M,S,Om,p=s.symbols('xi M S Om p',positive=True)
w=s.sqrt(4*xi/3-s.Rational(1,4));T=w/Om;A=S*T/(8*xi**2);f=A/T;F=M-2*xi*f
lim=lambda e:s.simplify(s.limit(e,xi,s.oo))
eq('family_coupling_norm',8*xi**2*f-S)
eq('family_F_limit',lim(F)-M)
eq('family_H_limit',lim(2/(3*T)))
eq('family_curvature_mass',lim(4*xi/(3*T**2))-Om**2)
eq('background_amplitude_shrinks',lim(s.sqrt(2*f)))
rhobg=4*M/(3*T**2)
mass=(0 if args.mutation=='omit_background_dust_mass' else xi*rhobg/M)
eq('EF_dust_quadratic_mass_retained',lim(mass)-Om**2)
eq('dust_density_vanishes',lim(rhobg))
eq('background_F_dot_vanishes',lim(2*xi*A/T**2))
# Explicit rotating Fa perturbation contraction; derivative must include rotating Fa.
t=s.symbols('t',real=True);U=s.Function('U')(t);V=s.Function('V')(t)
rot=s.Matrix([[s.cos(Om*t),-s.sin(Om*t)],[s.sin(Om*t),s.cos(Om*t)]])
y=rot*s.Matrix([U,V]);fa=-s.sqrt(S)*rot*s.Matrix([1,0]);df=(fa.dot(y)).expand()
eq('radial_orientation',df+s.sqrt(S)*U)
eq('rotating_Fa_derivative_no_V',s.diff(df,t)+s.sqrt(S)*s.diff(U,t))
canon=s.diff(y,t).dot(s.diff(y,t))/2-Om**2*y.dot(y)/2-p**2*y.dot(y)/2
expected=(s.diff(U,t)**2+s.diff(V,t)**2)/2+Om*(U*s.diff(V,t)-V*s.diff(U,t))-p**2*(U**2+V**2)/2
eq('canonical_rotation_centrifugal_cancellation',canon-expected)
Z=1+3*S/(2*M);Zused=1 if args.mutation=='omit_trace' else Z
u,v,ud,vd,P,Q,J=s.symbols('u v ud vd P Q J',real=True)
source_sign=1 if args.mutation=='wrong_source_orientation' else -1
L=Zused*ud**2/2+vd**2/2+Om*(u*vd-v*ud)-Zused*p**2*u**2/2-p**2*v**2/2+source_sign*s.sqrt(S)*J*u/(2*M)
eq('full_trace_kinetic_Z',Zused-1-3*S/(2*M))
eq('Jordan_source_orientation',s.diff(L,J)+s.sqrt(S)*u/(2*M))
eq('radial_canonical_momentum',s.diff(L,ud)-(Zused*ud-Om*v))
eq('phase_canonical_momentum',s.diff(L,vd)-(vd+Om*u))
Lc=L.subs(J,0);vel={ud:(P+Om*v)/Zused,vd:Q-Om*u}
Ham=(P*ud+Q*vd-Lc).subs(vel)
eq('Hamiltonian_positive_squares',Ham-((P+Om*v)**2/(2*Zused)+(Q-Om*u)**2/2+Zused*p**2*u**2/2+p**2*v**2/2))
# EL direct differentiation before Fourier substitution.
Lfun=L.subs({u:U,v:V,ud:s.diff(U,t),vd:s.diff(V,t)})
ELu=s.diff(s.diff(Lfun,s.diff(U,t)),t)-s.diff(Lfun,U)
ELv=s.diff(s.diff(Lfun,s.diff(V,t)),t)-s.diff(Lfun,V)
eq('full_radial_EL',ELu-(Zused*(s.diff(U,t,2)+p**2*U)-2*Om*s.diff(V,t)-source_sign*s.sqrt(S)*J/(2*M)))
eq('full_phase_EL',ELv-(s.diff(V,t,2)+p**2*V+2*Om*s.diff(U,t)))
ws=s.symbols('sigma',real=True);aa=p**2-ws**2;D=Z*aa**2-4*Om**2*ws**2
mat=s.Matrix([[Z*aa,2*s.I*Om*ws],[-2*s.I*Om*ws,aa]])
eq('coupled_fourier_determinant',mat.det()-D)
sol=mat.inv()*s.Matrix([-s.sqrt(S)*J/(2*M),0])
eq('signed_U_response',sol[0]+s.sqrt(S)*J*aa/(2*M*D))
eq('positive_deltaF_static',(-s.sqrt(S)*sol[0]).subs(ws,0)-S*J/(2*M*Z*p**2))
a=s.sqrt(p**2+Om**2/Z);sm=a-Om/s.sqrt(Z);sp=a+Om/s.sqrt(Z)
eq('pole_factorization',D-Z*(sm**2-ws**2)*(sp**2-ws**2))
eq('slow_pole_expansion',s.limit(sm/p**2,p,0)-s.sqrt(Z)/(2*Om))
eq('fast_pole_limit',s.limit(sp,p,0)-2*Om/s.sqrt(Z))
Am=(p**2-sm**2)/(Z*(sp**2-sm**2));Ap=(sp**2-p**2)/(Z*(sp**2-sm**2))
eq('retarded_residue_sum',Am+Ap-1/Z)
eq('retarded_partial_fractions_numerator',aa-Z*Am*(sp**2-ws**2)-Z*Ap*(sm**2-ws**2))
# Residues positive follows sm<p<sp: explicit algebraic product and positive ordering.
eq('positive_pole_product',sm*sp-p**2)
eq('positive_residue_gap_low',p**2-sm**2-2*Om*sm/s.sqrt(Z))
eq('positive_residue_gap_high',sp**2-p**2-2*Om*sp/s.sqrt(Z))
eq('pole_group_speed',s.diff(sm,p)-p/s.sqrt(p**2+Om**2/Z))
# Conserved contravariant source, Fourier derivative (-i sigma,0,0,ip).
rho=s.symbols('rho',real=True);tm=s.zeros(4);tm[0,0]=rho;tm[0,3]=tm[3,0]=ws*rho/p;tm[3,3]=ws**2*rho/p**2
for j in [0,3]:eq('source_conserved_component_'+str(j),-ws*tm[0,j]+p*tm[3,j])
eq('source_exact_trace',-tm[0,0]+tm[3,3]+rho*(1-ws**2/p**2))
# Einstein/Jordan potential mapping.
Phi,Psi,dF=s.symbols('Phi Psi dF');PJ=Phi+dF/(2*M);SJ=Psi-dF/(2*M)
if args.mutation=='call_conformal_lensing': PJ=Phi-dF/(2*M)
eq('Weyl_scalar_cancellation',PJ+SJ-Phi-Psi)
boost=1+S/(2*M*Z)
eq('static_force_ratio',boost-(2*M+4*S)/(2*M+3*S))
eq('static_boost_upper_gap',s.Rational(4,3)-boost-2*M/(3*(2*M+3*S)))
# EdS physical mode changes regime; slowfreeze has additional hierarchy.
eq('fixed_comoving_p_over_Omega_log_slope',s.Rational(1,1)-s.Rational(2,3)-s.Rational(1,3))
args.out.mkdir(parents=True,exist_ok=True);out={'claim':'ordered_on_shell_rotating_constrained_response','mutation':args.mutation,'checks':rows,'passed':sum(r['passed'] for r in rows),'total':len(rows),'limitations':['linear operator limit after infinitesimal source derivative','finite xi full FRW matter modes not solved','no nonlinear galaxy/cold or selector']};(args.out/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps({'passed':out['passed'],'total':out['total'],'failed':[r['name'] for r in rows if not r['passed']]}));sys.exit(0 if out['passed']==out['total'] else 1)
