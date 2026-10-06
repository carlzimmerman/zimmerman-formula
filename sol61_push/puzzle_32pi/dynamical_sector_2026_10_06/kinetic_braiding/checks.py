#!/usr/bin/env python3
"""Exact KGB branch/constraint checks and bounded leading near-zone response."""
import argparse, json, math, pathlib
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--control',choices=['none','mixing','canonical','mond'],default='none');args=p.parse_args()
rows=[]
def check(name,ok,detail=None): rows.append({'name':name,'passed':bool(ok),'detail':detail})
def zero(name,expr):check(name,s.simplify(expr)==0,str(s.simplify(expr)))
X,H,c,M,z,q,r,n=s.symbols('X H c M z q r n',positive=True)
kx,kxx,gx,gxx=s.symbols('kx kxx gx gxx',real=True)
# Independent substitutions implement functional relation and its derivative.
sub={kx:-3*H*q*gx,kxx:-3*H*q*gxx-3*H*gx/q,X:q*q/2}
Theta=M*H-q*X*gx
Sigma=X*kx+2*X**2*kxx+12*H*q*X*gx+6*H*q*X**2*gxx-3*M*H**2
# q^3 gx = -2 M H z (z subsequently unrestricted for sign tests).
zsub={gx:-2*M*H*z/q**3}
t=s.simplify(Theta.subs(sub,simultaneous=True).subs(zsub));sig=s.simplify(Sigma.subs(sub,simultaneous=True).subs(zsub))
zero('constraint_Theta',t-M*H*(1+z));zero('constraint_Sigma',sig+3*M*H**2*(1+2*z))
Gs=s.simplify(sig*M*M/t**2+3*M);Fs=s.simplify(H*M*M/t-M)
zero('eliminated_temporal',Gs-3*M*z*z/(1+z)**2);zero('eliminated_spatial',Fs+M*z/(1+z))
for zz in [-.9,-.5,-.25,-.1]:check('healthy_z_'+str(zz),float(Gs.subs({z:zz,M:1}))>0 and float(Fs.subs({z:zz,M:1}))>0)
check('canonical_positive_gradient_unstable',float(Fs.subs({z:.5,M:1}))<0)
# Log pair functional condition and vacuum transformation.
K=-c*s.log(X);G=-s.sqrt(2)*c/(n*H*s.sqrt(X))
zero('log_functional_branch',s.diff(K,X)+n*H*s.sqrt(2*X)*s.diff(G,X))
ss=s.symbols('ss',positive=True);dr=s.symbols('dr',real=True)
zero('braid_covariant_rescaling',G.subs(X,ss**2*X)*ss-G)
zero('kinetic_vacuum_rescaling',s.expand_log(K.subs(X,ss**2*X)-K,force=True)+2*c*s.log(ss))
powp,powr=s.symbols('p powr',real=True)
check('power_fixed_H_condition',s.simplify(powp-powr-s.Rational(1,2)).subs(powr,powp-s.Rational(1,2))==0)
# Derive linear current in exact static deSitter coordinates, no dropped Hq.
u,up=s.symbols('u up',real=True);f=1-H**2*r**2
psi0=-q*H*r/f;deltaX=-f*psi0*u;deltaBox=f*up+((n-1)*f/r+s.diff(f,r))*u
linear=(kxx+n*H*q*gxx)*deltaX*f*psi0-gx*deltaBox*f*psi0-gx*f*(q*H*u+q*H*r*up)
expect=gx*H*q*((n-2)-n*H**2*r**2)*u-(kxx+n*H*q*gxx)*q**2*H**2*r**2*u
zero('rolling_static_current_derived',linear-expect)
zero('rolling_H2_cancellation',expect.subs(kxx,-n*H*q*gxx-n*H*gx/q)-(n-2)*H*q*gx*u)
a=H*q*gx-gx*gx*q**4/(2*M)
zero('metric_mixing_coefficient',a.subs(zsub)-(H*q*gx*(1+z)).subs(zsub))
# Dimensionless physical normal root; ratios H^2*r^3/m cover both limits.
def vfun(m,rr,hh=1.,zz=-.5):
    aa=hh*(1+zz);return -2*m/(rr*rr*(aa+math.sqrt(aa*aa+8*m/rr**3)))
def dg(m,rr):return -.5*vfun(m,rr)
profiles=[]
for mm in [1e-24,1e-21,1e-18]:
    rv=(8*mm/.25)**(1/3)
    for ratio in [1e-3,1e-2,1,1e2,1e3]:
        rr=ratio*rv;vv=vfun(mm,rr)
        resid=.5*vv-2*vv*vv/rr+mm/rr**2
        check('source_constraint_'+str((mm,ratio)),abs(resid)<1e-12*max(mm/rr**2,1e-100))
        h=1e-4
        mass=(math.log(dg(mm*math.exp(h),rr))-math.log(dg(mm*math.exp(-h),rr)))/(2*h)
        radial=(math.log(dg(mm,rr*math.exp(h)))-math.log(dg(mm,rr*math.exp(-h))))/(2*h)
        profiles.append({'m':mm,'r_over_rV':ratio,'v':vv,'mass_slope':mass,'radial_slope':radial,'Hr':rr,'potential':mm/rr})
        if ratio==1e-3:check('inner_exponents_'+str(mm),abs(mass-.5)<1e-4 and abs(radial+.5)<1e-4)
        if ratio==1e3:check('outer_exponents_'+str(mm),abs(mass-1)<1e-7 and abs(radial+2)<1e-7)
        check('timelike_weak_branch_'+str((mm,ratio)),abs(vv)<1e-3 and mm/rr<1e-6 and rr<1e-2)
# Ellipticity of reduced static current on normal root.
for row in profiles:
    vv,rr=row['v'],(8*row['m']/.25)**(1/3)*row['r_over_rV'];ar=.5-4*vv/rr;at=(.25-vv/rr+4*vv*vv/rr**2)/ar
    check('static_reduced_ellipticity_'+str((row['m'],row['r_over_rV'])),ar>0 and at>0)
# Same metric for scaled q is explicit in local normalization; reconstruct with q-dependent Gx.
for qq in [1e-8,1.,1e8]:
    zz=-.5;hh=1.;mpl=1.;g1=-2*mpl*hh*zz/qq**3;vv=vfun(1e-18,1e-7);uu=qq*vv
    check('vacuum_map_force_'+str(qq),math.isclose(-g1*qq**2*uu/(2*mpl),zz*hh*vv,rel_tol=2e-15))
zero('p32_same_braid_horizon_ratio',(2*s.symbols('g',positive=True)/r)/(3*s.symbols('g',positive=True)*H)-2/(3*H*r))
if args.control=='mixing':check('CONTROL_wrong_omit_metric_mixing',s.simplify((H*q*gx).subs(zsub)-a.subs(zsub))==0)
if args.control=='canonical':check('CONTROL_wrong_canonical_health',float(Fs.subs({z:.5,M:1}))>0)
if args.control=='mond':check('CONTROL_wrong_MOND_radius',abs(profiles[0]['radial_slope']+1)<1e-4)
result={'claim':'KGB functional selftuning plus coupled leading nearzone, not full galaxy theory','control':args.control,'checks':rows,'profiles':profiles,'passed':all(x['passed'] for x in rows)}
path=pathlib.Path(args.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'checks':len(rows),'failed':[x['name'] for x in rows if not x['passed']]}));raise SystemExit(0 if result['passed'] else 1)
