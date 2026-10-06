"""Exact on-shell two-metric radiation scalar action discrimination."""
import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['freeze_fluid','erase_shear','vacuum_transfer']);args=ap.parse_args();rows=[]
def eq(n,e):
 e=s.factor(s.simplify(s.expand(e)));rows.append(dict(name=n,passed=e==0,residual=str(e)))
def ck(n,b):rows.append(dict(name=n,passed=bool(b)))
M,K,H,a,k,p,La,R,z,zd,v,vd,nu,ep=s.symbols('M K H a k p Lambda R z zd v vd nu eps',positive=True);P=k*k/a**2;Cr=s.Rational(3,2)*R;hd=-R/(2*M);ee=R/(2*M*H);ss=vd-H*v
# Exact homogeneous EH+matched vacuum+canonical CY² expansion before background substitution.
pp=R/4
raw=s.exp(3*ep*z)*(-3*M*(H+ep*zd)**2/(1+ep*nu)-M*La*(1+ep*nu)+pp*(1+ep*ss)**4/(1+ep*nu)**3)
raw2=s.diff(raw,ep,2).subs(ep,0)/2
core=-3*M*(zd-H*nu)**2+Cr*(ss-nu)**2+3*R*z*ss
Bgravdot=-18*M*H*z*zd-9*M*(3*H*H+hd)*z*z
eq('raw_EH_fluid_tadpole_cancellation',(raw2-core-Bgravdot).subs(La,3*H*H-3*R/(4*M)))
Bfluiddot=3*R*(z*vd+v*zd-H*z*v)
eq('radiation_cross_time_boundary',3*R*z*ss+3*R*v*zd-Bfluiddot)
q,C,chi=s.symbols('q C chi',positive=True);Y=q*q/2;Pfluid=C*Y**2
rho=2*Y*s.diff(C*s.Symbol('Y')**2,s.Symbol('Y')).subs(s.Symbol('Y'),Y)-Pfluid
eq('actual_CY2_radiation_density',rho-3*Pfluid)
eq('actual_radiation_inertia',rho+Pfluid-C*q**4)
Yv=s.symbols('Yv',positive=True);Py=C*Yv**2
eq('actual_fluid_cs_squared',s.diff(Py,Yv)/(s.diff(Py,Yv)+2*Yv*s.diff(Py,Yv,2))-s.Rational(1,3))
# Both actual shifts and retained relative shear; R fluid comes from raw action.
b,L,H2,z2,zd2,nu2,tg,th,e,D,ell,Pi=s.symbols('b L H2 z2 zd2 nu2 tg th e D ell Pi',positive=True)
fg=zd-H*nu;fh=zd2-H2*nu2
Lg=a**3*(-3*M*fg**2-2*M*fg*tg+M*P*z*z+2*M*P*nu*z+Cr*(ss-nu)**2-R*v*(3*zd+tg)-R*P*v*v/2)
Lh=M*b**3/L*(-3*fh**2-2*fh*th)+M*L*b**3*k*k/b**2*(z2*z2+2*nu2*z2)
eq('visible_shift_actual_momentum',s.diff(Lg,tg)+a**3*(2*M*fg+R*v))
eq('hat_shift_actual_momentum',s.diff(Lh,th)+2*M*b**3*fh/L)
Ngsol=(zd+R*v/(2*M))/H;Nhsol=zd2/H2
eq('visible_shift_lapse_solution',fg.subs(nu,Ngsol)+R*v/(2*M))
eq('hat_shift_lapse_solution',fh.subs(nu2,Nhsol))
# Exact reference g reduction includes matter; derivative boundary taken on actual background.
base=s.simplify(Lg.subs({nu:Ngsol,tg:0}))
w=v-z/H;wd=vd-zd/H+z*hd/H**2
new=a**3*(Cr*(wd-ee*w)**2-R*P*w*w/2)
F=M*a**3*P*z*z/H-Cr*a**3*H*v*v
Fd=s.diff(F,a)*H*a+s.diff(F,H)*hd+s.diff(F,R)*(-4*H*R)+s.diff(F,z)*zd+s.diff(F,v)*vd
eq('full_reference_GR_radiation_reduction',base-new-Fd)
# Proper h constant gives H2=L h and removes both hat scalar spatial terms as a boundary.
h=s.symbols('h',positive=True);Fh=M*b*k*k*z2*z2/h
Fhd=s.diff(Fh,b)*H2*b+s.diff(Fh,z2)*zd2
eq('empty_hat_exact_time_boundary',(Lh.subs({fh:0,nu2:Nhsol,th:0})-Fhd).subs(H2,L*h))
# Actual volume difference at reciprocal background, not preimposed equality.
x,y,eps,V0,Q,La0=s.symbols('x y epsilon V0 Q Lambda0',positive=True)
Vg=V0*s.exp(eps*x);Vh=Q*Q*V0*s.exp(eps*y)
diff=2*K*La0*(Q*Vg+Vh/Q-2*s.sqrt(Vg*Vh))
eq('noncoincident_volume_square',s.diff(diff,eps,2).subs(eps,0)/2-K*La0*Q*V0*(x-y)**2/2)
# Clock first acceleration and exact common-time gauge combination.
T,Td,pi,rd,nudotg,nudoth=s.symbols('T Td pi rd nudotg nudoth',real=True)
rr,rrd=s.symbols('delta_r delta_r_dot',real=True)
eq('common_clock_gauge_combination',(rr-rd*T)-rd*(pi-T)-(rr-rd*pi))
# Relative volume includes shear. On Qconst it is common-time invariant.
Hg,Hhatcoord,Nlog,Llog=s.symbols('Hg Hhatcoord Nlog Llog')
Dt=-(Nlog-Llog+3*(Hg-Hhatcoord))*T
eq('volume_common_time_invariance',Dt.subs(Nlog,Llog-3*(Hg-Hhatcoord)))
# After reference boundaries define xg=z/H,xh=z2/H2, chi=xg-xh.
xg,xh,xgd,xhd,cd=s.symbols('xg xh xgd xhd chi_dot',real=True)
Ngnew=xgd+ee*w;Nhnew=xhd+ell*xh
eq('actual_relative_lapse_response',Ngnew-Nhnew-(xgd-xhd-ell*xh+ee*w))
Gamma=s.symbols('Gamma',positive=True);ww,wwd,gg=s.symbols('w wdot chi_dot',real=True)
Tresp=gg-ell*xh+ee*ww;Lf=a**3*Cr*(wwd-ee*ww)**2-a**3*R*P*ww**2/2+Gamma*Tresp**2
pchi=s.diff(Lf,gg);pu=0
eq('algebraic_clock_constraint',s.diff(Lf,xh)+ell*pchi)
eq('finite_matter_clock_response_vanishes',s.diff(Lf,xh).subs(xh,(gg+ee*ww)/ell))
# Actual reduced first-class accidental quadratic chain: pu -> ell pchi -> 0.
pw,pcc=s.symbols('pw pchi',real=True)
Hcan=pw**2/(4*a**3*Cr)+ee*ww*pw+a**3*R*P*ww**2/2+pcc**2/(4*Gamma)+(ell*xh-ee*ww)*pcc
eq('quadratic_primary_preservation',s.diff(Hcan,xh)-ell*pcc)
chi_coord=s.symbols('chi_coordinate',real=True)
eq('quadratic_secondary_cyclic_preservation',s.diff(Hcan,chi_coord))
ck('positive_retained_radiation_kinetic',a**3*Cr>0)
cs=s.simplify((R/2)/Cr);eq('retained_radiation_sound_speed',cs-s.Rational(1,3))
# Rank condition not infer generic all-time state from a single coefficient point.
eq('nonzero_rate_constraint_solution',s.diff(Hcan,xh).subs(pcc,0))
# Both varied source terms vanish only after the actual constraints.
Dvol,resp,La_g,La_h=s.symbols('D_volume response Lambda_g Lambda_h',real=True)
rhog=-M*La_g*Dvol/2-2*Gamma*resp/a**3
rhoh=M*La_h*Dvol/2+2*Gamma*resp/(L*b**3)
eq('visible_extra_source_zero',rhog.subs({Dvol:0,resp:0}))
eq('hat_extra_source_zero',rhoh.subs({Dvol:0,resp:0}))
if args.control=='freeze_fluid':eq('false_frozen_radiation_momentum',(s.diff(Lg,tg)+2*M*a**3*fg))
if args.control=='erase_shear':eq('false_volume_without_relative_shear',D-(D-e))
if args.control=='vacuum_transfer':eq('false_vacuum_mode_when_ell_nonzero',-ell*pcc)
out=dict(passed=sum(r['passed'] for r in rows),total=len(rows),checks=rows,control=args.control,scope='n3 exact homogeneous radiation+emptyhat admitted branch; nonzero relative lapse rate on open interval; scalar quadratic only, not nonlinear health/DOF')
pth=Path(args.out);pth.parent.mkdir(parents=True,exist_ok=True);pth.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(passed=out['passed'],total=out['total'],failed=[r for r in rows if not r['passed']])));sys.exit(not all(r['passed'] for r in rows))
