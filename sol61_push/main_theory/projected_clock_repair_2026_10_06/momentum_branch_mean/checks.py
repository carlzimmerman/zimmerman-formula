"""Actual mixed momentum/decay raw lapse/scale sources and normal averages."""
import argparse,json,sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--control',choices=['forget_covariance','drop_curvature','infer_dust']);ar=ap.parse_args();rows=[]
def eq(n,x):
 x=s.factor(x);rows.append(dict(name=n,passed=x==0,residual=str(x)))
eta,K,a,H,k=s.symbols('eta K a H k',positive=True);D,U,C,Dx,Ux,Cx,Z,Zd,V=s.symbols('D U C Dx Ux Cx Z Zd V',real=True);ep=s.symbols('ep');q=H*(4-3/eta)/2;L=0
for sg in [1,-1]:
 total=D+U;X=2*Z+sg*(total-2*C);Y=2*Z+sg*(C-total);N=s.exp(V+sg*total/2);Xx=sg*(Dx+Ux-2*Cx);Yx=sg*(Cx-Dx-Ux);Yxx=sg*(-k*k*C+k*k*total);shift=sg*(H*Dx+q*Ux)/k**2;shiftx=-sg*(H*D+q*U)
 kx=(H+Zd-sg*H*(D/2+U)-shift*Xx/2-shiftx)/N;ky=(H+Zd+sg*H*(D/2+U)-shift*Yx/2)/N
 R=s.exp(-X)/a**2*(-2*Yxx+Xx*Yx-s.Rational(3,2)*Yx*Yx)
 L+=K*a**3*N*s.exp((X+2*Y)/2)*((1-eta)*(kx*kx+2*ky*ky)-(1-eta/3)*(kx+2*ky)**2+R)
L+=-12*K*H*H*a**3*s.exp(V+3*Z)+K*a*s.exp(V+Z)*s.cosh(D+U-2*C)*(Dx+Ux)**2
jets=[D,U,C,Dx,Ux,Cx];sub={Z:0,Zd:0,V:0}
def co(e):return s.expand(s.series(e.subs(sub).subs({j:ep*j for j in jets}),ep,0,3).removeO()).coeff(ep,2)
def dt(e):return H*a*s.diff(e,a)-H*sum(j*s.diff(e,j) for j in [D,Dx])-2*H*sum(j*s.diff(e,j) for j in [U,Ux])
d,u,c=s.symbols('d u c',real=True);p=k*k/a**2;b=3*(1-eta)/eta
avgmap={D**2:d*d/2,U**2:u*u/2,C**2:c*c/2,D*U:d*u/2,D*C:d*c/2,U*C:u*c/2,Dx**2:k*k*d*d/2,Ux**2:k*k*u*u/2,Cx**2:k*k*c*c/2,Dx*Ux:k*k*d*u/2,Dx*Cx:k*k*d*c/2,Ux*Cx:k*k*u*c/2}
def avg(e):return s.expand(e).subs(avgmap)
JV=avg(co(s.diff(L,V)));JZ=avg(co(s.diff(L,Z))-dt(co(s.diff(L,Zd))))
jv=K*a**3*(H*H*d*d+(2-3/eta)*H*H*u*u+p*c*c)/2
jz=K*a**3*(H*H*d*d-(2-3/eta)*H*H*u*u+p*c*c)/2
eq('raw_mean_lapse_source',JV-jv);eq('raw_mean_scale_source',JZ-jz)
eq('no_raw_decay_momentum_cross',s.diff(s.diff(JV,d),u))
eq('no_raw_decay_frozen_cross',s.diff(s.diff(JV,d),c))
# Linear branch reconstructed from full reduced constraints.
z=c-u-d;nu=u+d;fd=H*u;tt=-3*H*u/eta;ee=2*(d+u)-3*c;ed=-2*H*d-4*H*u
shift_beta=H*(2*d+(4-3/eta)*u)/p
eq('actual_f_branch',2*H*u+H*d-H*nu-fd)
eq('actual_shift_branch',tt+3*fd/eta)
eq('actual_volume_branch',nu+3*z+ee)
eq('actual_shift_and_shear_reconstruction',ed+p*shift_beta-tt)
Arel=-b;kr=b*p/(b*H*H+p)
eq('actual_relative_lapse_branch',((Arel*H*(2*H*u+H*d)+p*z)/(Arel*H*H-p)-nu).subs(u,c*p/(b*H*H)))
qrel=a*z;qdot=H*a*(c+u)
Pi=2*K*a*kr*qdot
eq('actual_conserved_momentum_normalization',(Pi-2*K*k*k*c/H).subs(u,c*p/(b*H*H)))
# Exact normal trace, including the nonzero first-order covariance.
N=s.exp((D+U)/2);vol=s.exp(-(D+U)/2);shift=(H*Dx+q*Ux)/k**2
num=3*H+H*(D/2+U)+shift*(Dx+Ux)/2+H*D+q*U
T=num/(3*N)
T1=s.expand(s.series(T.subs({j:ep*j for j in jets}),ep,0,3).removeO()).coeff(ep,1)
T2=co(T)
eq('normal_first_order_not_zero',T1+b*H*U/6)
geo=avg(T2-(D+U)*T1/2)
wantgeo=H*(eta*d*d+6*(1-eta)*d*u+(6-7*eta)*u*u)/(48*eta)
eq('actual_proper_volume_covariance',geo-wantgeo)
F0=-JV/(24*K*a**3*H)
DH=s.factor(F0+geo)
wantDH=-p*c*c/(48*H)+b*H*u*u/16+b*H*d*u/24
eq('actual_normal_mean_correction',DH-wantDH)
eq('surviving_interference_a3',s.diff(s.diff(DH,d),u)-b*H/24)
# Homogeneous mean trace source consistency using u_dot=-2Hu,d_dot=-Hd.
def dtamp(e):return H*a*s.diff(e,a)-H*d*s.diff(e,d)-2*H*u*s.diff(e,u)
eq('homogeneous_lapse_constraint',24*K*a**3*H*F0+JV)
eq('homogeneous_scale_constraint',24*K*a**3*(dtamp(F0)+3*H*F0)+JZ)
# Raw intrinsic R with the actual spatial measure.
X=D+U-2*C;Y=C-D-U;Xx=Dx+Ux-2*Cx;Yx=Cx-Dx-Ux;Yxx=-k*k*(C-D-U)
R=s.exp(-X)/a**2*(-2*Yxx+Xx*Yx-s.Rational(3,2)*Yx*Yx)
R1=s.expand(s.series(R.subs({j:ep*j for j in jets}),ep,0,3).removeO()).coeff(ep,1)
Rbar=avg(co(R)-(D+U)*R1/2)
eq('actual_intrinsic_curvature_average',Rbar-p*(c-d-u)**2/4)
variance=b*b*H*H*u*u/8;sigbar=3*H*H*u*u/(4*eta*eta)
# Direct action lapse variation. rho=-ELlogN/(N sqrtgamma).
lg,lh,gg,gh,gamg,gamh,hg,hh,gx,gxx=s.symbols('lg lh gg gh gamg gamh hg hh gx gxx',real=True)
vvol=s.exp((lg+lh)/2)*s.sqrt(gamg*gamh);havg=(hg+hh)/2
Lg=K*vvol*havg*(gg-gh)**2
# Symbolic functional loglapse row at fixed spatialmetrics, include derivative of volume.
dxLg=lambda expr:s.diff(expr,lg)*gg+s.diff(expr,lh)*gh+s.diff(expr,gg)*gx+s.diff(expr,gh)*gxx
ELlg=s.diff(Lg,lg)-dxLg(s.diff(Lg,gg))
eq('actual_loglapse_functional_derivative',ELlg-(K*vvol*havg*(gg-gh)**2/2-2*K*dxLg(vvol*havg*(gg-gh))))
# Actual conformal metric trace while holding the OTHERmetric fixed.
zconf=s.symbols('zconf');conf=K*vvol*s.exp(s.Rational(3,2)*zconf)*(hg*s.exp(-2*zconf)+hh)/2*(gg-gh)**2
ptr=s.diff(conf,zconf).subs(zconf,0)/(3*vvol)
eq('actual_gradient_pressure_variation',ptr.subs({hg:1/a**2,hh:1/a**2})-K*(gg-gh)**2/(6*a**2))
NN,ggam,stilde=s.symbols('N sqrtgamma shear_tilde',positive=True)
Lshear=-eta*K*ggam*stilde**2/NN
rhoder=-s.diff(Lshear,NN)/ggam
eq('actual_shear_lapse_variation',rhoder+eta*K*stilde**2/NN**2)
peq=(s.diff(s.exp(3*zconf)*Lshear,zconf).subs(zconf,0))/(3*NN*ggam)
eq('actual_shear_pressure_variation',peq-rhoder)
# Each log lapse: volumehalf gradientminus2div; at admitted Vg=Vh its leading divergence is2K/a²nu_xx.
rho_first=2*K*(-k*k*(D+U))/a**2
rho_second=-K*(Dx+Ux)**2/(2*a*a)
rhog=avg(rho_second-(D+U)*rho_first/2)
eq('actual_gradient_energy_measure',rhog-K*p*(d+u)**2/4)
# sigma_g1²=2/3 (t_rel/2)²; backgroundshearzero, so secondfields cannot change order2 density.
siglocal=s.Rational(2,3)*(tt/2)**2
sigavg=siglocal/2
eq('actual_shear_average',sigavg-sigbar)
rhos=-eta*K*sigavg
rho=rhog+rhos
wantedrho=K*p*(d+u)**2/4-3*K*H*H*u*u/(4*eta)
eq('actual_normal_interaction_density',rho-wantedrho)
# Conformal spatial trace: gradientδZg=(3/2Havg−hg)K v gradnu² =>p=Kgrad²/(6a²); sheartrace p=rhos.
pressure=K*p*(d+u)**2/12+rhos
eq('pressure_trace_from_action',pressure-(rhog/3+rhos))
# Einstein average with individual M=2K; not an effective-FRW Friedmann substitution.
constraint=Rbar/2+6*H*DH+variance/3-sigbar/2-rho/(2*K)
eq('actual_averaged_Einstein_constraint',constraint.subs(u,c*p/(b*H*H)))
eq('full_geometry_cross_has_only_faster_density_power',s.diff(s.diff((Rbar/2+6*H*DH).subs(u,c*p/(b*H*H)),d),c)-p*p/(4*b*H*H))
eq('dust_scaled_geometry_cross_cancel',-p*c*d/4+6*H*(p*c*d/(24*H)))
# Time powers: direct sourceinterferencePdu scalesa^-5, normalH PCd scalesa^-3.
a_ref,d0=s.symbols('a_ref d0',positive=True)
eq('actual_density_cross_timepower', (K*p*d*u/2).subs({d:d0/a,u:c*p/(b*H*H)})-K*k**4*c*d0/(2*b*H*H*a**5))
# Controls falsify physically different quantities.
candidate=geo if ar.control!='forget_covariance' else avg(T2)
eq('control_keeps_normal_measure_covariance',candidate-wantgeo)
candidate=constraint if ar.control!='drop_curvature' else constraint-Rbar/2
eq('control_keeps_intrinsic_constraint_piece',candidate.subs(u,c*p/(b*H*H)))
candidate=0 if ar.control!='infer_dust' else p*c*d/(24*H)
eq('control_does_not_identify_expansion_cross_as_density',candidate)
out=dict(passed=sum(x['passed'] for x in rows),total=len(rows),checks=rows,control=ar.control,scope='mixed aligned Fourier linear scalar branch, actual quadratic homogeneousmeanEuler/actionstress/preferrednormalaverages; no complete secondorder regularfamily or abundance/selector')
pth=Path(ar.out);pth.parent.mkdir(parents=True,exist_ok=True);pth.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(passed=out['passed'],total=out['total'],failed=[x['name'] for x in rows if not x['passed']])));sys.exit(not all(x['passed'] for x in rows))
