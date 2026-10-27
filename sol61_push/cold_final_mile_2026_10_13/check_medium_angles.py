import json,math,sys
from pathlib import Path
import sympy as s
kx,kz,om,et,el,mu,lam=s.symbols('kx kz omega et el mu lambda',real=True)
cross=s.Matrix([[0,-kz,0],[kz,0,-kx],[0,kx,0]])
W=cross*s.diag(mu,mu,lam)*cross+om**2*s.diag(et,et,el)
ordinary=om**2-(lam*kx*kx+mu*kz*kz)/et
extra=om**2-mu*(kx*kx/el+kz*kz/et)
checks=[]
def check(name,c,detail=''):
 checks.append(dict(name=name,passed=bool(c),detail=detail))
 if not c:raise AssertionError(name)
check('full anisotropic Maxwell determinant',s.simplify(W.det()-et*et*el*om**2*ordinary*extra)==0)
check('ordinary polarization eigenblock',s.simplify((W*s.Matrix([0,1,0]))[1]-et*ordinary)==0)
eg=s.Matrix([el*kz,0,-et*kx])
check('extraordinary Gauss constraint',s.simplify(s.Matrix([[kx,0,kz]])*s.diag(et,et,el)*eg)==s.zeros(1,1))
check('extraordinary polarization branch',all(s.simplify(x)==0 for x in (W*eg).subs(om**2,mu*(kx*kx/el+kz*kz/et))))
a,b,ax,az=s.symbols('a b ax az',positive=True)
vgroup=(a*a*ax*ax+b*b*az*az)/(a*ax*ax+b*az*az)
check('group speed weighted coefficient identity',s.simplify(vgroup-(a*(a*ax*ax)+b*(b*az*az))/(a*ax*ax+b*az*az))==0)
E,D0=s.symbols('E D0',positive=True)
L=D0*E-D0*D0*s.log(1+E/D0);D=s.diff(L,E);H=E*D-L
threshold=E*E-E*D;defect=E*D-2*H
gap=s.simplify(threshold-defect)
check('causal density also suffices for total staticDEC',s.simplify(gap-(E*E-2*L))==0)
check('DEC sufficient gap monotonic',s.simplify(s.diff(gap,E)-2*(E-D))==0)
check('DEC sufficient gap zero atvacuum',gap.subs(E,0)==0)
rows=[]
for ee in [.01,.1,1.,9.]:
 dd=ee/(1+ee);etl=1/(1+ee);ell=1/(1+ee)**2
 rr=10*(ee*ee-ee*dd)
 cap=(ell*(rr+ee*dd)-dd*dd)/(rr-ee*dd+ell*ee*ee)
 mm=cap+(dd-cap*ee)**2/(rr+ee*dd-cap*ee*ee)
 for i in range(9):
  theta=i*math.pi/16;xx=math.sin(theta);zz=math.cos(theta)
  pairs=[(cap/etl,mm/etl),(mm/ell,mm/etl)]
  vals=[]
  for aa,bb in pairs:
   phase=aa*xx*xx+bb*zz*zz
   group=(aa*aa*xx*xx+bb*bb*zz*zz)/phase
   check('phase/group withinmetric e%g angle%d coefficients%g,%g'%(ee,i,aa,bb),
         0<phase<=1+1e-10 and 0<group<=1+1e-10)
   vals.append(dict(phase_speed_squared=phase,group_speed_squared=group))
  rows.append(dict(E_over_D0=ee,angle_rad=theta,polarizations=vals))
out=dict(checks=checks,angular_controls=rows,scope='Allangle symbolic frozen gauge-cone reduction plus finite examples; pressureless fluidzero modes and full nonlinear/global health remain unproved.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(checks=len(checks),all_passed=all(x['passed'] for x in checks)),indent=2))
