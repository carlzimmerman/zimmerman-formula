import argparse,json,pathlib,sys
import sympy as s
import mpmath as mp
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--control',choices=['none','omit_Ty','qumond_transfer','green_normalization'],default='none');args=ap.parse_args()
checks=[];samples=[]
def ck(name,value):checks.append({'name':name,'passed':bool(value)})
y,e,D=s.symbols('y e D',positive=True);mu=1/(1+2*e);xx=y*(1+2*e);xy=2*D-1
ck('stationary_logarithmic_derivative',s.simplify((xx/(y*xy)-1)-(1/(mu*xy)-1))==0)
r,z,h,n=s.symbols('r z h n',positive=True);f=(r*r+z*z/h)**(-(n-2)/2)
ck('anisotropic_Green_harmonic_away_source',s.simplify(s.diff(f,r,2)+(n-2)*s.diff(f,r)/r+h*s.diff(f,z,2))==0)
normal=s.Integer(1) if args.control=='green_normalization' else 1/s.sqrt(h)
ck('Green_flux_charge_jacobian',s.simplify(normal*s.sqrt(h)-1)==0)
ck('physical_half_sum_parallel_n3',s.simplify((1+1/mu)/2-(1+e))==0)
A,H,U,K,lam=s.symbols('A H U K lam',positive=True)
ck('IFT_origin_value',s.Rational(8,7)==s.integrate(4*z**s.Rational(5,2),(z,0,1)))
ck('IFT_first_h_coefficient',s.integrate(-8*z**s.Rational(9,2)/K**2,(z,0,1))==-s.Rational(16,11)/K**2)
ck('u_first_coefficient',s.simplify((-16/(11*K**2))/(4*lam*K**3)/K).subs(lam,8/(7*K**4))==-7/(22*K**2))
HH=2*(1+A*H/2);MU=H**2*(1+A*H)/2
ratio=(MU+1/s.sqrt(HH))/(MU+1)
ck('angular_deficit_coefficient',s.simplify(s.diff(ratio,H).subs(H,0)+A/(4*s.sqrt(2)))==0)
ck('moment_angular_bound',s.simplify((7*s.pi**2/128)/32-7*s.pi**2/4096)==0)
u=s.symbols('u',real=True);q=s.Function('nu')(y);qkernel=1+s.Rational(1,2)*(-s.Rational(1,2))*(1-u*u)
ck('QUMOND_deep_parallel',qkernel.subs(u,1)==1);ck('QUMOND_deep_perpendicular',qkernel.subs(u,0)==s.Rational(3,4))
mp.mp.dps=45

def branch(yy,ll,omit=False):
 yy=mp.mpf(yy);ll=mp.mpf(ll);hh=yy**mp.mpf('.25');K0=(8/(7*ll))**mp.mpf('.25')
 def R(v):return 1/(mp.sqrt(1+yy*v)+mp.sqrt(yy*v))
 def I(u,p):return mp.quad(lambda v:v**mp.mpf('2.5')*R(v)/(u*u+hh*v*v)**p,[0,1])
 lo=K0*mp.mpf('1e-12');hi=K0
 for _ in range(110):
  mid=(lo+hi)/2
  if 4*I(mid,2)>ll:lo=mid
  else:hi=mid
 uu=(lo+hi)/2;TT=uu*yy**mp.mpf('.875');delta=hh/(uu*uu)
 ET=R(1)/(4*uu*uu*(uu*uu+hh)**2*I(uu,3))
 bb=(mp.sqrt(1+yy)-mp.sqrt(yy))/mp.sqrt(yy);ybp=-1/(2*mp.sqrt(yy)*mp.sqrt(1+yy))
 DD=1+(bb+ybp)/(1+delta)-bb*2*delta*(1-(0 if omit else ET))/(1+delta)**2
 ee=bb/(1+delta);mm=1/(1+2*ee);hx=1/(mm*(2*DD-1))
 PP=(1+1/(mm*mp.sqrt(hx)))/2;PA=1+ee;RR=PP/PA
 return dict(y=yy,lam=ll,T=TT,D=DD,mu=mm,h=hx,ratio=RR,ET=ET,stationarity=4*I(uu,2)-ll)
for ll,yy in [('0.001','1e-20'),('0.01','1e-20'),('0.01','1e-12'),('0.01','0.01'),('0.01','1')]:
 v=branch(yy,ll,omit=args.control=='omit_Ty');expected=mp.sqrt(7*v['lam']/8)/(4*mp.sqrt(2));Bhat=(1/mp.sqrt(2)-v['ratio'])/v['y']**mp.mpf('.25')
 ck('stationarity_'+ll+'_'+yy,abs(v['stationarity'])<mp.mpf('1e-28'))
 ck('linear_operator_positive_'+ll+'_'+yy,v['mu']>0 and v['h']>0)
 if yy=='1e-20':
  got=mp.mpf('.75') if args.control=='qumond_transfer' else v['ratio']
  ck('deep_angular_limit_'+ll,abs(got-1/mp.sqrt(2))<mp.mpf('1e-5'))
  ck('actual_Ty_angular_coefficient_'+ll,abs(Bhat/expected-1)<mp.mpf('0.001'))
 samples.append({k:mp.nstr(x,22) for k,x in v.items()}|{'Bhat':mp.nstr(Bhat,22),'B':mp.nstr(expected,22)})
# Independent finite difference of the eliminated response, not fixed-T differentiation.
v0=branch('0.01','0.01');yp=mp.mpf('.01')*(1+mp.mpf('1e-5'));ym=mp.mpf('.01')*(1-mp.mpf('1e-5'))
vp=branch(yp,'0.01');vm=branch(ym,'0.01')
def force(v):return v['y']*(1+((mp.sqrt(1+v['y'])-mp.sqrt(v['y']))/mp.sqrt(v['y']))/(1+(v['y']/v['T'])**2))
fd=(force(vp)-force(vm))/(yp-ym)
ck('total_D_independent_finite_difference',abs(fd/v0['D']-1)<mp.mpf('1e-8'))
out={'passed':sum(c['passed'] for c in checks),'total':len(checks),'checks':checks,'samples':samples,'control':args.control,'scope':'exact constant-field operator identities and seven fixed bounded numerical branch evaluations; not nonlinear/global/cosmological health'}
p=pathlib.Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(out,indent=2));print(json.dumps(out));sys.exit(out['passed']!=out['total'])
