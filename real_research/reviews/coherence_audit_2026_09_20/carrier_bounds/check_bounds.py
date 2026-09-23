"""Independent kinetic Schur reduction and finite-gradient gate for the repair.

This is an algebraic and local principal-block calculation. It does not derive
the full perturbation action or prove the coupled theory well posed.
"""
from pathlib import Path
import json
import sys
import sympy as s

out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
checks={}
def zero(label,e):
    z=s.simplify(e)
    assert z==0,(label,z)
    checks[label]=True

A,B,E=s.symbols('A B E',positive=True)
H,C,v,u,psi=s.symbols('H C v u psi',real=True)
L=A*(v+H*psi)**2+B*(u-C*psi)**2+E*psi**2
D=A*H**2+B*C**2+E
ps=(B*C*u-A*H*v)/D
zero('lapse_solution',s.diff(L,psi).subs(psi,ps))
reduced=s.factor(L.subs(psi,ps))
K=s.hessian(reduced,(v,u)).applyfunc(s.factor)
expected=s.Matrix([[2*A*(B*C*C+E)/D,2*A*B*H*C/D],
                   [2*A*B*H*C/D,2*B*(A*H*H+E)/D]])
for i in range(2):
    for j in range(2):zero('kinetic_%s%s'%(i,j),K[i,j]-expected[i,j])
zero('kinetic_determinant',K.det()-4*A*B*E/D)

alpha,d,beta,ell2,k2=s.symbols('alpha d beta ell2 k2',positive=True)
P=s.symbols('P',real=True)
LG=alpha*psi**2+2*d*psi*P-d*(beta+ell2*k2)*P**2
Ps=psi/(beta+ell2*k2)
ae=alpha+d/(beta+ell2*k2)
zero('scalar_elimination',LG.subs(P,Ps)-ae*psi**2)
zero('mond_alpha_eff',ae.subs({beta:d/(2-alpha),ell2:0})-2)

# Independent finite-gradient test of the proposed smooth exponent.
y,z,Ac,rho0=s.symbols('y z Ac rho0',positive=True)
mm=1+(Ac-1)/(2*(1+y*y)**s.Rational(1,4))
first=s.diff(mm,y);second=s.diff(mm,y,2)
zero('longitudinal_exponent_derivative',first+2*y*second-
     (Ac-1)*y*(2*y*y-3)/(4*(1+y*y)**s.Rational(9,4)))
m=s.symbols('m',positive=True)
pressure=rho0*s.expm1(m*z)/(2*m) if hasattr(s,'expm1') else rho0*(s.exp(m*z)-1)/(2*m)
pm=s.diff(pressure,m);pmm=s.diff(pressure,m,2)
zero('pressure_m_derivative',pm-rho0*((m*z-1)*s.exp(m*z)+1)/(2*m*m))
zero('pressure_mm_derivative',pmm-rho0*(s.exp(m*z)*((m*z)**2-2*m*z+2)-2)/(2*m**3))
longitudinal=pm.subs(m,mm)*(first+2*y*second)+2*y*pmm.subs(m,mm)*first**2
transverse=pm.subs(m,mm)*first
witness={Ac:9,y:s.sqrt(15),z:s.Rational(1,3),rho0:1}
CL=s.simplify(longitudinal.subs(witness))
CT=s.simplify(transverse.subs(witness))
zero('exact_longitudinal_witness',CL-s.sqrt(15)*(7+10*s.E)/4608)
zero('exact_transverse_witness',CT+s.sqrt(15)/288)
assert float(CL)>0 and float(CT)<0
result={'checks':checks,
 'kinetic_matrix':s.sstr(expected),'kinetic_determinant':s.sstr(4*A*B*E/D),
 'mapping':{'A':'2(3b+2)/b after ADM shift elimination','B':'p_X+2X p_XX',
            'E':'alpha_eff (k/a)^2','C':'sqrt(X)','domain':'b,B,alpha_eff,k,a>0; H real'},
 'mapping_scope':'Independent velocity-core argument using prior ADM geometry and newly verified scalar constraint; full action variation not repeated here.',
 'alpha_eff':s.sstr(ae),
 'finite_gradient':{'definition':'y=Y/Yd, z=log(X/X0), Ac>1, p=rho0[exp(mz)-1]/(2m)',
  'm':s.sstr(mm),'m_y_plus_2y_m_yy':s.sstr(s.factor(first+2*y*second)),
  'exact_witness':'Ac=9, y=sqrt(15), z=1/3, rho0=Yd=1, m=3',
  'carrier_transverse_pressure_curvature':s.sstr(CT),
  'carrier_longitudinal_pressure_curvature':s.sstr(CL),
  'longitudinal_numeric':float(CL),
  'necessary_fixed_clock_spatial_condition':'J_Y+2Y J_YY > p_Y+2Y p_YY for the scalar spatial block of -J(Y)+p(X,Y). This is necessary for positive fixed-clock scalar gradient energy, not sufficient for full coupled health.'},
 'non_claims':['No full nonlinear or finite-wavelength coupled stability theorem.',
               'No claim the local witness lies on a global halo solution.',
               'Positive velocity Hessian does not control spatial principal coefficients.']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print('Independent exact checks:',len(checks))
print('Kinetic determinant:',s.sstr(4*A*B*E/D))
print('Finite-gradient longitudinal curvature:',CL,'=',float(CL))
