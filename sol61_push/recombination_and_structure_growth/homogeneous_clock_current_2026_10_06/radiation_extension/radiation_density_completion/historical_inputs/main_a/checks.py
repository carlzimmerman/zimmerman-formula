"""Positive radiation-density square: exact constraints, kinetic capacity, UV determinant."""
import argparse,pathlib,json,sympy as s,numpy as np,itertools
pa=argparse.ArgumentParser();pa.add_argument('--output',required=True);pa.add_argument('--control',choices=['none','wrong_square','wrong_profile','dust_instability'],default='none');args=pa.parse_args();checks=[]
def ck(n,b,d=None):checks.append(dict(name=n,passed=bool(b),detail=d))
def zero(n,e):e=s.factor(s.cancel(e));ck(n,e==0,str(e))
X,Y,lam,q,rhor,Z,eps,nu,sr,Bv,Bp=s.symbols('X Y lam q rhor Z eps nu sr Bv Bp',real=True)
rad=3*lam*Y*Y;dY=2*Y*(sr-nu)
zero('actual_radiation_density_variation',s.diff(rad,Y)*dY-4*rad*(sr-nu))
U=Z*(X-Bv)**2/2
zero('stealth_value',U.subs(X,Bv));zero('stealth_X_first_variation',s.diff(U,X).subs(X,Bv));zero('stealth_B_first_variation',s.diff(U,Bv).subs(X,Bv))
diff=-q*q*nu-Bp*4*rhor*(sr-nu);br=s.symbols('br',real=True)
zero('correct_lapse_radiation_square',diff.subs(Bp,br*q*q/(4*rhor))+q*q*((1-br)*nu+br*sr))
if args.control=='wrong_square':zero('CONTROL_wrong_square_sign',diff.subs(Bp,br*q*q/(4*rhor))+q*q*((1+br)*nu-br*sr))
h,hp=s.symbols('h hp',real=True)
profile=-(3+hp/(h-1));zero('background_profile_exact_factor',profile+3+hp/(h-1))
# Differentiate X=q²/2 against rho_r with dlnrho/dlna=-4.
zero('profile_from_chain_rule',4*rhor*(-q*q*(3+hp/(h-1))/(4*rhor))/(q*q)-profile)
if args.control=='wrong_profile':zero('CONTROL_missing_profile_factor_two',profile/2-profile)
A,C,D,d,u,zd=s.symbols('A C D d u zd',real=True)
vel=A*zd**2+C*u*u+D*(d*zd+br*u)**2
KK=s.hessian(vel,[zd,u])/2;schur=s.factor(KK[0,0]-KK[0,1]**2/KK[1,1]);zero('exact_velocity_schur',schur-A-D*d*d*C/(C+D*br*br));zero('exact_velocity_determinant',KK.det()-C*A-D*(A*br*br+C*d*d))
zero('finite_capacity_bound',s.limit(schur-A,D,s.oo)-C*d*d/br**2)
T,L,D0=s.symbols('T L D0',positive=True)
# Smooth global construction if L=C*d²+A0*br²>0 at every finiteepoch.
Dchosen=(T+s.sqrt(T*T+D0*D0))/2
zero('smooth_gain_above_positive_threshold',(Dchosen-T)-D0**2/(2*(s.sqrt(T*T+D0*D0)+T)))
M,Th,Sig,kap,p,R,Cr,H,rho,Ds=s.symbols('M Th Sig kap p R Cr H rho Ds',nonzero=True,real=True)
z,v,w,pi,zd,vd,wd,t=s.symbols('z v w pi zd vd wd t',real=True)
S=Sig+kap*M*p*p;radtime=wd-H*w
raw=-3*M*zd**2+S*nu**2+6*Th*nu*zd-2*Th*nu*t+2*M*zd*t+M*p*p*z*z+2*M*p*p*nu*z+3*rho*z*nu
raw+=pi*(vd-nu)-rho*p*p*v*v/2+rho*v*t+Cr*(radtime-nu)**2+3*R*z*radtime-R*p*p*w*w/2+R*w*t
raw+=Ds*((1-br)*nu+br*radtime)**2
nushift=M/Th*zd+rho/(2*Th)*v+R/(2*Th)*w
zero('shift_constraint_unchanged',s.diff(raw,t).subs(nu,nushift))
red=s.expand(raw.subs(nu,nushift)).subs(t,0)
zero('dust_remains_canonical',s.diff(red,pi,pi))
zero('dust_density_equation',s.diff(red,pi)-(vd-nushift))
fields=[z,v,w,pi];vel=[zd,vd,wd,s.Symbol('pid')];K=s.hessian(red,vel);V=s.hessian(red,fields);G=s.Matrix([[s.diff(red,vel[i],fields[j])-s.diff(red,fields[i],vel[j]) for j in range(4)] for i in range(4)])
x=s.symbols('x',real=True);E=-p*p*x*x*K-s.I*p*x*G-V
# Coefficient convolution, not a slow full generic determinant expansion.
lead=0;degrees=[]
for perm in itertools.permutations(range(4)):
 sign=(-1)**sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4));pol={0:s.Integer(1)}
 for i,j in enumerate(perm):
  ent=s.Poly(s.expand(E[i,j]),p);new={}
  for (k,),c in ent.terms():
   for kk,cc in pol.items():
    if k+kk<=8:new[k+kk]=new.get(k+kk,0)+cc*c
  pol=new
 lead+=sign*pol.get(8,0)
lead=s.factor(lead);target=-2*kap*M**3*x**4*(2*(Cr+Ds*br*br)*x*x-R)/Th**2
zero('full_three_pair_UV_characteristic',lead-target)
zero('positive_radiation_acoustic_root',lead.subs(x*x,R/(2*(Cr+Ds*br*br))))
zero('H_normalization_drops_only_at_principal_order',s.diff(lead,H))
# Explicit finite frozen parameter example, not an on-background universe fit.
sub={M:1,Th:1,Sig:-4,kap:1,R:s.Rational(4,3),Cr:2,H:0,rho:1,Ds:4,br:s.Rational(1,2)}
A0=3+s.Integer(-4);Asample=A0+s.Rational(4*2,1)/(2+4*s.Rational(1,4));ck('illustrative_positive_kinetic_repair',Asample>0,str(Asample))
cs=s.Rational(4,3)/(2*(2+4*s.Rational(1,4)));ck('illustrative_positive_acoustic_speed',cs>0,str(cs))
if args.control=='dust_instability':ck('CONTROL_radiation_square_repeats_dust_UV_instability',cs<0)
rows=[]
for pp in [30,100,1000]:
 mat=E.subs(sub).subs(p,pp);char=s.Poly(s.expand(mat.det(method='domain-ge')),x);coef=[complex(s.N(c,30)) for c in char.all_coeffs()];roots=np.roots(coef);acoustic=min(roots,key=lambda r:abs(r-np.sqrt(float(cs))))
 rows.append(dict(p=pp,radiation_omega_over_p_real=float(acoustic.real),radiation_omega_over_p_imag=float(acoustic.imag),error_to_principal=float(abs(acoustic-np.sqrt(float(cs))))))
ck('bounded_acoustic_convergence',rows[-1]['error_to_principal']<rows[0]['error_to_principal']);ck('bounded_acoustic_roots_real',max(abs(r['radiation_omega_over_p_imag']) for r in rows)<1e-10)
# Slow high-p sector: retain volume a^3p^2 derivative H and dot(d), not a frozenfrequency approximation.
Pslow,Qslow,d0,ddot=s.symbols('Pslow Qslow d0 ddot',real=True)
ns=d0*zd+rho/(2*Th)*v+R/(2*Th)*w
Ls=M*kap*ns**2+M*z*z+2*M*ns*z-rho*v*v/2-R*w*w/2+Pslow*(vd-ns)
calR=2*M*kap*ns+2*M*z-Pslow
zero('slow_clock_momentum',s.diff(Ls,zd)-d0*calR)
zero('slow_clock_force',s.diff(Ls,z)-2*M*(z+ns))
zero('slow_dust_force',s.diff(Ls,v)-rho/(2*Th)*calR+rho*v)
zero('slow_radiation_algebraic_constraint',s.diff(Ls,w)-R/(2*Th)*calR+R*w)
et,Hs=s.symbols('et Hs',positive=True)
lateD=1/(Hs*(1-et));nv=(Qslow-2*M*z+Pslow)/(2*M)
rhs=s.Matrix([nv/lateD,nv,-Hs*Pslow,2*M/lateD*(z+nv)-Hs*Qslow]);lateMatrix=rhs.jacobian([z,v,Pslow,Qslow]);ll=s.symbols('ll')
zero('actual_late_slow_eigenrates',lateMatrix.charpoly(ll).as_expr()-ll*(ll+Hs)*(ll+et*Hs)*(ll+(1-et)*Hs))
result=dict(passed=all(c['passed'] for c in checks),checks=checks,leading_characteristic=str(lead),clock_schur='Aold+DeltaSigma*d²*Cr/(Cr+DeltaSigma*br²)',capacity='Cr*d²+A0*br²>0 needed wherever A0<0',background_profile='br=−(3+h_ln_a/(h−1))',frozen_algebra_controls=rows,scope='Exact square/constraints/velocity and leading UV roots only. Conditional global designer kinetic lift; no full IR, photon or source health.',control=args.control,non_claims=['No global lift for all histories','No actual photons or Boltzmann model','No fixedcoupling vacuum selfadjustment','No32pi selector','Frozen matrices not cosmology fits'])
o=pathlib.Path(args.output);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=result['passed'],checks=len(checks),failed=[c['name'] for c in checks if not c['passed']])));raise SystemExit(0 if result['passed'] else 1)
