"""Covariant barotropic host and three spectral-density choices.

Host fields supply a conserved material-label current, not an identified
fermion/cold particle number. Perfect-fluid, fixed-background linear scope.
"""
import json
import math
import sys
from pathlib import Path
import mpmath as mp
import numpy as np
import sympy as s

out=Path(sys.argv[1]);assert out.is_dir();base=Path(__file__).parent
previous=json.loads((base/'one_scale_nodal_flux_run_002/results.json').read_text())
d=abs(previous['filled_sea_energy_over_Q_squared'])
checks=[]
def check(name,b):
    checks.append(dict(name=name,passed=bool(b)));assert b,name

b,N,Vol=s.symbols('b N Vol',positive=True)
R=s.Function('R')
energy=Vol*R(N/Vol)
check('metric-volume pressure identity',s.simplify(-s.diff(energy,Vol)-(N/Vol*s.diff(R(b),b).subs(b,N/Vol)-R(N/Vol)))==0)
epsilon,L,v=s.symbols('epsilon L v',real=True)
bwave=b*s.sqrt((1+epsilon*L)**2-epsilon*epsilon*v*v)
quadratic=s.diff(-R(bwave),epsilon,2).subs(epsilon,0)/2
expected=b*s.diff(R(b),b)*v*v/2-b*b*s.diff(R(b),b,2)*L*L/2
check('longitudinal material-field quadratic action',s.simplify(quadratic-expected)==0)

y,c0,c1,lam,c2,dd=s.symbols('y c0 c1 lam c2 d',positive=True)
healthy=c0+c1*y+lam*y**s.Rational(4,3)+c2*y*y/2
pressure=s.simplify(y*s.diff(healthy,y)-healthy)
trace=s.simplify(-healthy+3*pressure)
check('healthy host trace',s.simplify(trace-(-4*c0-c1*y+c2*y*y))==0)
gap=s.simplify(s.diff(healthy,y)-y*s.diff(healthy,y,2))
check('sound speed below unity identity',s.simplify(gap-(c1+s.Rational(8,9)*lam*y**s.Rational(1,3)))==0)
sea=-dd*y**s.Rational(4,3)
check('material sea radiation pressure',s.simplify(y*s.diff(sea,y)-sea-sea/3)==0)
check('material sea trace zero',s.simplify(-sea+3*(y*s.diff(sea,y)-sea))==0)
check('sea kinetic sign',s.simplify(y*s.diff(sea,y)+s.Rational(4,3)*dd*y**s.Rational(4,3))==0)
check('rest plus sea gradient sign',s.simplify(s.diff(c1*y+sea,y,2)+s.Rational(4,9)*dd*y**(-s.Rational(2,3)))==0)

scale=s.symbols('a',positive=True)
y0=s.symbols('y0',positive=True)
f_a=healthy.subs(y,y0/scale**3)
check('exact homogeneous energy conservation',s.simplify(scale*s.diff(f_a,scale)+3*(y*s.diff(healthy,y)).subs(y,y0/scale**3))==0)
gamma=s.symbols('gamma',real=True)
beta_exponent=s.Rational(1,3)+3*gamma
CT_exponent=s.Rational(2,3)+2*gamma
check('fixed-v single-power incompatibility',s.solve([beta_exponent,CT_exponent],[gamma])==[])

def eos(yy):
    f=1*yy+d*yy**(4/3)+.5*yy*yy
    fp=1+4*d*yy**(1/3)/3+yy
    fpp=4*d*yy**(-2/3)/9+1
    p=yy*fp-f;H=yy*fp
    return dict(y=yy,energy_over_Q2=f,pressure_over_Q2=p,w=p/f,
        enthalpy_over_Q2=H,sound_speed_squared=yy*fpp/fp)
host=[]
for yy in np.geomspace(1e-9,1e3,61):
    row=eos(float(yy));host.append(row)
    check('host positive enthalpy '+str(yy),row['enthalpy_over_Q2']>0)
    check('host subluminal longitudinal sound '+str(yy),0<row['sound_speed_squared']<1)

# Finite-cutoff determinant under fixed-flux, material, and compensated
# density dependences. Derivatives retain the critical counterterm.
mp.mp.dps=60
Astar=mp.mpf(str(previous['constants']['Astar']))
ch=mp.mpf(str(previous['constants']['ch']));cL=mp.mpf(str(previous['constants']['cLambda']))
P=mp.mpf('0.0001');Q=mp.mpf(1)
exponents={'flux_spectrum':(mp.mpf(0),mp.mpf(0),mp.mpf(0)),
           'material_spectrum':(mp.mpf(1)/3,mp.mpf(1)/3,-mp.mpf(1)/3),
           'compensated_cubic':(mp.mpf(1)/3,mp.mpf(1)/3,-mp.mpf(1)/9)}
def spectral(yy,name):
    aexp,lexp,hexp=exponents[name]
    A=Astar*yy**aexp;cutoff=cL*yy**lexp;h=ch*yy**hexp;gap=h*P
    band=-A*((cutoff*cutoff+gap*gap)**mp.mpf('1.5')-cutoff**3-gap**3)/3
    CT=A*cutoff*gap*gap/2
    ren=band+CT
    return A,h,cutoff,gap,ren,CT
spectra=[]
for name in exponents:
    for yy in (mp.mpf('.01'),mp.mpf(1),mp.mpf(100)):
        A,h,cutoff,fg,ren,CT=spectral(yy,name)
        derivative=yy*mp.diff(lambda t:spectral(t,name)[4],yy)
        derivativeCT=yy*mp.diff(lambda t:spectral(t,name)[5],yy)
        aexp,lexp,hexp=exponents[name]
        beta=A*h**3
        expectedbeta=Astar*ch**3*yy**(aexp+3*hexp)
        check('spectral cubic density exponent '+str((name,yy)),abs(beta/expectedbeta-1)<mp.mpf('1e-45'))
        if name=='flux_spectrum':check('flux density rearrangement zero '+str(yy),derivative==0)
        if name=='material_spectrum':check('material leading rearrangement '+str(yy),abs(derivative/ren+mp.mpf(2)/3)<mp.mpf('.003'))
        if name=='compensated_cubic':
            check('compensated critical counterterm rearrangement '+str(yy),abs(derivativeCT/CT-mp.mpf(4)/9)<mp.mpf('1e-45'))
            check('compensated residual small at tested gap '+str(yy),abs(derivative/ren)<mp.mpf('.001'))
        spectra.append(dict(model=name,y=float(yy),cubic_beta=float(beta),
            quadratic_counterterm_over_P_squared=float(CT/(P*P)),gap_over_cutoff=float(fg/cutoff),
            renormalized_band_energy=float(ren),material_rearrangement_b_dE_db=float(derivative),
            rearrangement_over_renormalized_energy=float(derivative/ren),
            counterterm_rearrangement=float(derivativeCT),
            omitted_counterterm_rearrangement_error=float(-derivativeCT)))

history=[]
for a in (1.,10.,100.):
    yy=a**-3
    check('material acceleration scaling '+str(a),abs((yy**(2/3))/(a**-2)-1)<1e-13)
    history.append(dict(scale_factor=a,y=yy,material_a0_over_initial=a**-2,
        compensated_a0_over_initial=1.,compensated_counterterm_over_initial=yy**(4/9),
        host_w=eos(yy)['w']))
result=dict(host_action='-Integral sqrt(-g) rho(b,Q); b=sqrt(det(g^mu nu partial_mu X^I partial_nu X^J)); material current identically conserved; Q fixed',
    healthy_EOS='rho/Q^2=c0+c1 y+lambda y^(4/3)+c2 y^2/2; selectedc0=0,c1=c2=1,lambda=d; positive host4/3 coefficient before sea=2d',
    negative_sea_coefficient=d,rest_plus_sea_plus_quadratic_gradient_threshold_y=(4*d/9)**1.5,
    host_rows=host,spectral_rows=spectra,history_rows=history,checks=checks,
    non_claims=['No physical identification of material-label current with fermion charge or original cold number','Fluid source b is entropy density in a charged thermodynamic convention; this barotropic material interpretation has separately chosen normalization','No dissipative heating, transverse quantum stability, dilute vacuum phase, full covariant band/metric modes or actual cosmology','Density compensation and healthy host terms are new inputs, not microscopic predictions','No vacuum magnitude, kappa, galaxy fit or novelty closure'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(controls=len(checks),gradient_threshold=result['rest_plus_sea_plus_quadratic_gradient_threshold_y'],spectral_rows=spectra,history_rows=history),indent=2))
