"""Independent exact algebra of the prospective shared-phase action; no Lean yet."""
from pathlib import Path
import json
import sympy as s
HERE=Path(__file__).resolve().parent
R,u,a,X0,rho0,m,f=s.symbols('R u a X0 rho0 m f',real=True)
e,sg,st,sx,et,ex=s.symbols('bookkeeping sigma sigmadot sigmax etadot etax',real=True)
r=R+e*sg
X=((u+e*et)**2-(e*ex)**2)/2
P=-rho0+a*(X-X0)**2/2
U=m*m*(r-f)**2/2
L=((e*st)**2-(e*sx)**2)/2+r*r*X+P-U
B=R*R+a*(u*u/2-X0);K=B+a*u*u;C=2*R*u;mu2=m*m-u*u
l1=s.expand(L).coeff(e,1);l2=s.expand(L).coeff(e,2)
expected=st*st/2-sx*sx/2-mu2*sg*sg/2+K*et*et/2-B*ex*ex/2+C*sg*et
checks=[]
def zero(name,expr):
 residual=s.factor(expr)
 checks.append({'name':name,'passed':residual==0,'residual':str(residual)})
zero('linear radial source requires actual background relation',l1-((m*m*f-mu2*R)*sg+B*u*et))
zero('complete quadratic action with radial and phase mixing',l2-expected)
ps,pi=s.symbols('p_sigma Pi',real=True)
zero('canonical radial momentum',s.diff(l2,st)-st)
zero('canonical phase momentum',s.diff(l2,et)-(K*et+C*sg))
velocity={st:ps,et:(pi-C*sg)/K}
H=s.factor((ps*st+pi*et-l2).subs(velocity))
Hexpected=ps*ps/2+(pi-C*sg)**2/(2*K)+mu2*sg*sg/2+sx*sx/2+B*ex*ex/2
zero('actual Legendre transform completed square',H-Hexpected)
omega,k,z=s.symbols('omega k frequency_squared',real=True)
matrix=s.Matrix([[k*k+mu2-omega*omega,s.I*C*omega],[-s.I*C*omega,B*k*k-K*omega*omega]])
disp=(omega*omega-(k*k+mu2))*(K*omega*omega-B*k*k)-C*C*omega*omega
zero('Fourier determinant coupling sign',s.expand(matrix.det())-disp)
# Independent generic polynomial parameters, avoiding framework parameter circularity.
Kg,Bg,Cg,Mg,q=s.symbols('K B C mu_squared wave_squared',real=True)
poly=Kg*z*z-(Kg*(q+Mg)+Bg*q+Cg*Cg)*z+Bg*q*(q+Mg)
D=s.discriminant(poly,z)
sos=(Kg*(q+Mg)-Bg*q)**2+2*Cg*Cg*(Kg*(q+Mg)+Bg*q)+Cg**4
zero('real-root discriminant decomposition',D-sos)
zero('zero-wave roots',poly.subs(q,0)-z*(Kg*z-Kg*Mg-Cg*Cg))
# F(s,q)=0 implicit slope at massless root.
zero('small-wave implicit sound slope',(-s.diff(poly,q)/s.diff(poly,z)).subs({q:0,z:0})-Bg*Mg/(Kg*Mg+Cg*Cg))
# Exact homogeneous stress of the original prospective action, not rotating H.
Xb=u*u/2;Pb=-rho0+a*(Xb-X0)**2/2;Ub=m*m*(R-f)**2/2
original_pressure=R*R*Xb+Pb-Ub
original_density=R*R*Xb+2*Xb*a*(Xb-X0)-Pb+Ub
zero('original background stress differs from rotating energy',original_density+original_pressure-u*u*B)
assert all(row['passed'] for row in checks)
result={'status':'PROSPECTIVE_ACTION_MATHEMATICAL_CHECK_ONLY','checks':checks,'check_count':len(checks),'all_passed':True,
 'conditions_not_derived':['actual background mu_squared*R=m^2*f','K>0 for invertible healthy phase momentum','B>=0 for gradient positivity','mu_squared>0 for radial quadratic positivity','physical existence/admission of the proposed action'],
 'dispersion_notes':{'polynomial':'K*s^2-[K(q+mu2)+Bq+C^2]*s+Bq(q+mu2)','gap_squared':'mu2+C^2/K','implicit_massless_sound_slope':'B*mu2/(K*mu2+C^2)','background_rho_plus_p':'u^2*B'},
 'scope':'Exact quadratic expansion/Legendre/Fourier algebra of the supplied prospective action. No gravity, actual coupling admission, irreversible transfer, empirical fit, or Lean implementation.'}
(HERE/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'all_passed':True,'check_count':len(checks)},indent=2))
