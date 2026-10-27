"""Finite-temperature mean-field discriminator and charge-resolved tree rates.

This specifies a leading high-temperature Higgs-bath comparison, not a
resummed SM prediction or a cosmological field/kinetic evolution. Only the
SM bath supplies a thermal mass; no equilibrated dark bath is assumed.
"""
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

out = Path(sys.argv[1])
assert out.is_dir()
parent = Path(__file__).parent
previous = json.loads((parent / 'run_003/results.json').read_text())
checks = []

def check(name, value):
    checks.append({'name': name, 'passed': bool(value)})
    assert value, name

mh, vh, mpl = 125., 246., 1.2209e19
lambda_h = mh*mh/(2*vh*vh)
g2, gy, yt = .65, .36, .94
c_h = (3*g2*g2+gy*gy)/16+lambda_h/2+yt*yt/4
tc = math.sqrt(lambda_h*vh*vh/c_h)
lambda_x = 1e-18
ustar, rlambda = .02, 2.
hbarc, gev_g = 1.973269804e-14, 1.7826619216279e-24
sigma_mass_natural = .3*gev_g/hbarc**2

def parameters(m):
    M = 2*m*math.sqrt(1+ustar**2)
    gap = 4*m*m*ustar**2
    rep = math.sqrt(8*math.pi*m**3*sigma_mass_natural)
    g = math.sqrt(rep*gap/rlambda)
    total = rep*(1+1/rlambda)
    # Four final daughters, same simplified Higgs-decay yield as the parent.
    phase = math.sqrt(1-4*M*M/(mh*mh))
    phase_ref = math.sqrt(1-4*previous['portal']['M_GeV']**2/(mh*mh))
    lp = previous['portal']['lambda_HX']*math.sqrt(.001/m*phase_ref/phase)
    return dict(m=m, M=M, gap=gap, rep=rep, g=g, total=total, lp=lp,
                M0sq=M*M-lp*vh*vh/2)

def phase_values(x, T, p):
    # Analytically minimize Higgs invariant t=H^dagger H and daughter
    # invariant n=|Phi|^2 at fixed source amplitude x=|X|. Cubic phase
    # chosen to minimize +g X*Phi^2+h.c. -> -2g x n.
    lp, m, g, total = p['lp'], p['m'], p['g'], p['total']
    t0 = max((lambda_h*vh*vh-c_h*T*T)/(2*lambda_h), 0.)
    t = max((lambda_h*vh*vh-c_h*T*T-lp*x*x)/(2*lambda_h), 0.)
    n = max((2*g*x-m*m)/(2*total), 0.)
    higgs_difference = lambda_h*(t-t0)**2 + max(c_h*T*T-lambda_h*vh*vh, 0.)*t
    # Reference is x=n=0, thermal Higgs at its own minimum.
    value = (higgs_difference + (p['M']**2+lp*(t-vh*vh/2)+lp*T*T/6)*x*x
             +lambda_x*x**4 + (m*m-2*g*x)*n+total*n*n)
    derivative = (2*(p['M']**2+lp*(t-vh*vh/2)+lp*T*T/6)*x
                  +4*lambda_x*x**3-2*g*n)
    return value, derivative, t, n

def cubic_candidates(a, b, c):
    # Positive roots of 4 a x^3 + 2 b x + c=0, a>0, c>=0.
    # For c>0 positive roots require b<0 and negative discriminant.
    assert a > 0 and c >= 0
    if c == 0:
        return [math.sqrt(-b/(2*a))] if b < 0 else []
    if b >= 0:
        return []
    pp, qq = b/(2*a), c/(4*a)
    discriminant = (qq/2)**2+(pp/3)**3
    if discriminant > 0:
        return []  # the sole real root is negative
    amplitude = 2*math.sqrt(-pp/3)
    angle = math.acos(max(-1., min(1., (3*qq/(2*pp))*math.sqrt(-3/pp))))/3
    return [x for x in (amplitude*math.cos(angle-2*math.pi*j/3) for j in range(3)) if x > 0]

def minimum(T, p):
    lp = p['lp']
    xphi = p['m']**2/(2*p['g'])
    xh = math.sqrt(max(lambda_h*vh*vh-c_h*T*T, 0.)/lp)
    candidates = [0., xphi, xh]
    for occupied_h in (False, True):
        for occupied_phi in (False, True):
            if occupied_h:
                aa = lambda_x-lp*lp/(4*lambda_h)
                bb = p['M']**2+lp*(1/6-c_h/(2*lambda_h))*T*T
            else:
                aa, bb = lambda_x, p['M0sq']+lp*T*T/6
            cc = 0.
            if occupied_phi:
                bb -= p['g']**2/p['total']
                cc = p['g']*p['m']**2/p['total']
            for x in cubic_candidates(aa, bb, cc):
                _, _, t, n = phase_values(x, T, p)
                if (t > 0) == occupied_h and (n > 0) == occupied_phi:
                    candidates.append(x)
    records = [phase_values(x, T, p) for x in candidates]
    index = min(range(len(candidates)), key=lambda j: records[j][0])
    x = candidates[index]
    val, derivative, t, n = records[index]
    curvature_origin = p['M']**2 + lp*(max((lambda_h*vh*vh-c_h*T*T)/(2*lambda_h),0)-vh*vh/2)+lp*T*T/6
    # Independent logarithmic scan only checks the stationary candidate's
    # numerical implementation; it is not the proof of global selection.
    sampled = [phase_values(10**(-8+j*18/1200), T, p)[0] for j in range(1201)]
    check('stationary minimum no higher than log scan m=%g T=%g' % (p['m'], T),
          val <= min([0.]+sampled)+1e-7*max(1.,abs(val)))
    if x > 0 and val < -1e-6:
        norm = max(abs(2*curvature_origin*x), abs(4*lambda_x*x**3), abs(2*p['g']*n),1e-30)
        check('envelope derivative at occupied minimum m=%g T=%g' % (p['m'],T), abs(derivative)/norm < 1e-9)
    return dict(T_GeV=T, x_GeV=x, phi_amplitude_GeV=math.sqrt(n),
                higgs_amplitude_GeV=math.sqrt(2*t),
                potential_difference_GeV4=val, source_curvature_at_origin_GeV2=curvature_origin)

masses = (.00075,.001,.00125,.002,.01)
temperatures = (0.,100.,125.,150.,175.,200.,250.,300.,500.)
phase_rows = []
for mass in masses:
    p = parameters(mass)
    check('positive completed quartic m=%g' % mass, lambda_x > p['lp']**2/(4*lambda_h))
    rows = [minimum(T,p) for T in temperatures]
    check('EW vacuum is zero-temperature global minimum m=%g' % mass, rows[0]['potential_difference_GeV4'] >= -1e-8)
    # A sufficient all-Higgs-background condition: M0sq >= g^2/lambda_tot.
    # Dark quartic and portal tadpole are nonnegative; this condition is
    # stronger than just absence of a tachyon at Phi=X=0.
    sufficient_symmetric = p['M0sq'] >= p['g']**2/p['total']
    if sufficient_symmetric:
        check('sufficient symmetric branch realized in grid m=%g' % mass,
              all(r['potential_difference_GeV4'] >= -1e-8 for r in rows))
    spinodal_high = math.sqrt(-6*p['M0sq']/p['lp']) if p['M0sq'] < 0 else None
    phase_rows.append({'parameters':p, 'sufficient_no_dark_condensate':sufficient_symmetric,
                       'unbroken_Higgs_spinodal_upper_GeV':spinodal_high, 'minima':rows})

p1 = parameters(.001)
row200 = next(r for r in phase_rows[1]['minima'] if r['T_GeV']==200)
check('baseline origin unstable in unbroken comparison at 200 GeV', row200['source_curvature_at_origin_GeV2'] < 0)
check('baseline occupied minimum lower at 200 GeV', row200['potential_difference_GeV4'] < 0)
check('both dark amplitudes nonzero at 200 GeV', row200['x_GeV'] > 0 and row200['phi_amplitude_GeV'] > 0)
check('Higgs unbroken at baseline 200 GeV minimum', row200['higgs_amplitude_GeV'] == 0)
growth_h = math.sqrt(-row200['source_curvature_at_origin_GeV2'])/(1.66*math.sqrt(106.75)*200**2/mpl)

# Separate vacuum-mass, monochromatic source-decay CONTROL. A near-threshold
# resting lifetime must be time dilated, even when the cascade yield is
# eventually four. This does not use the finite-T masses computed above.
Tprod=mh/3
Hp=1.66*math.sqrt(106.75)*Tprod*Tprod/mpl
GammaX=p1['g']**2/(8*math.pi*p1['M'])*math.sqrt(1-4*p1['m']**2/p1['M']**2)
gamma_source=mh/(2*p1['M'])
u_source=math.sqrt(gamma_source**2-1)
def optical_depth(r, n=256):
    step=(r-1)/n
    def fn(s): return s*s/math.sqrt(s*s+u_source*u_source)
    acc=fn(1)+fn(r)
    for j in range(1,n): acc+=(4 if j%2 else 2)*fn(1+j*step)
    return GammaX/Hp*step*acc/3
lo,hi=1.,100.
for _ in range(80):
    mid=(lo+hi)/2
    if optical_depth(mid) < 1: lo=mid
    else: hi=mid
rdec=(lo+hi)/2
check('vacuum source decay optical depth one',abs(optical_depth(rdec)-1)<1e-12)
check('source decay independent quadrature refinement',abs(optical_depth(rdec,128)-optical_depth(rdec,256))<1e-12)
check('source not prompt per production Hubble time',GammaX/(gamma_source*Hp)<1)
check('source still relativistic at one decay optical depth',u_source/rdec>100)

# Sufficient mass floor retaining the old abundance-calibrated portal
# scaling and u*, sigma/m, rlambda. Bisection of explicit, not fitted, condition.
def margin(m):
    p=parameters(m)
    return p['M0sq']-p['g']**2/p['total']
lo,hi=.001,.002
for _ in range(90):
    mid=(lo+hi)/2
    if margin(mid) < 0: lo=mid
    else: hi=mid
mass_floor=(lo+hi)/2
check('mass floor brackets change of sufficient condition', margin(mass_floor*.999) < 0 < margin(mass_floor*1.001))

# Sensitivity: conditional high-T comparison only. Vary Higgs curvature
# coefficient .3-.5 and source tadpole coefficient 1/12-1/3.
windows=[]
for ch in (.3,.4,.5):
    for beta in (1/12,1/6,1/3):
        lower=math.sqrt(lambda_h*vh*vh/ch)
        upper=math.sqrt(-p1['M0sq']/(beta*p1['lp']))
        check('nonempty stipulated high-T instability window ch=%g beta=%g' % (ch,beta), upper > lower)
        windows.append({'c_H':ch,'source_thermal_mass_coefficient_over_portal':beta,
                        'T_H_meanfield_GeV':lower,'T_X_spinodal_GeV':upper})

# Same-charge s-channel vs opposite-charge crossed u-channel, tree level.
# Fraction controls at positive rational values establish implementation
# relations, not a substitute for the explicit S-matrix derivation.
cross_exact=[]
for uu in (F(1,2500),F(1,100),F(1,4)):
    for rr in (F(1),F(2),F(4)):
        # Normalize m=lambda_rep=1; Delta=4u^2, g^2=Delta/r.
        delt=4*uu; MM=4*(1+uu); gg=delt/rr; lt=1+1/rr
        same=lt-gg/delt
        opposite=lt-gg/MM
        ratio=2*opposite*opposite
        expected=2*(1+1/(rr*(1+uu)))**2
        check('charge crossed threshold identity uu=%s rr=%s' % (uu,rr), same==1 and ratio==expected)
        cross_exact.append({'u2':str(uu),'rlambda':str(rr),'opposite_over_same':str(ratio)})

ratio_opposite=2*(1+1/(rlambda*(1+ustar**2)))**2
ratio_mixture=(1+ratio_opposite)/2
rate_old=previous['collisionless_control']['Gamma_elastic_over_H']

def simpson_angle(fn,n):
    step=2/n
    acc=fn(-1)+fn(1)
    for i in range(1,n): acc+=(4 if i%2 else 2)*fn(-1+i*step)
    return step*acc/3

angular=[]
for up in (0.,.00025,.003,.01,.05):
    p=p1; momentum=p['m']*up; ss=4*(p['m']**2+momentum**2)
    def eff(ct): return p['total']-p['g']**2/(p['M']**2+2*momentum**2*(1+ct))
    integ=simpson_angle(lambda ct: eff(ct)**2,128)
    integ2=simpson_angle(lambda ct: eff(ct)**2,256)
    sigma_opp=integ/(2*math.pi*ss)
    sigma_same0=p['rep']**2/(8*math.pi*p['m']**2)
    check('crossed angle quadrature agrees u=%g' % up, abs(integ/integ2-1)<1e-12)
    check('crossed channel finite and positive u=%g' % up, sigma_opp > 0 and math.isfinite(sigma_opp))
    angular.append({'p_over_m':up,'sigma_opposite_over_same_threshold':sigma_opp/sigma_same0})
check('crossed threshold numerical normalization', abs(angular[0]['sigma_opposite_over_same_threshold']/ratio_opposite-1)<1e-13)

result={
 'verdict':'High-T comparison finds baseline dark-origin instability; a different mass point avoids that sufficient obstruction; crossed elastic channel strengthens collision screen',
 'SM_comparison_inputs':dict(lambda_H=lambda_h,g2=g2,gY=gy,yt=yt,c_H=c_h,T_H_meanfield_GeV=tc,lambda_X=lambda_x),
 'baseline_200GeV':row200, 'baseline_growth_over_H_at_200GeV':growth_h,
 'vacuum_source_decay_control':dict(Tprod_GeV=Tprod,GammaX_rest_GeV=GammaX,
              GammaX_time_dilated_over_H_at_production=GammaX/(gamma_source*Hp),
              a_over_ap_at_optical_depth_one=rdec,T_GeV_at_optical_depth_one=Tprod/rdec,
              source_p_over_M_at_optical_depth_one=u_source/rdec),
 'mass_floor_GeV_sufficient_no_dark_condensate':mass_floor,
 'phase_rows':phase_rows,'thermal_coefficient_sensitivity':windows,
 'scattering':dict(opposite_over_same_threshold=ratio_opposite,
                   neutral_mixture_over_old_screen=ratio_mixture,
                   neutral_mixture_Gamma_over_H_1keV_control=rate_old*ratio_mixture,
                   exact_threshold_cases=cross_exact,angular_checks=angular),
 'checks':checks,
 'non_claims':['Thermal comparison is leading high-T mean field, not a resummed physical phase diagram',
               'No equilibrated dark bath or dark thermal masses assumed',
               'Field minima are not dynamical production histories or relic yields',
               'Mass floor is conditional on abundance-calibrated portal scaling; not an observed particle bound',
               'Charge scattering is vacuum tree level; no inclusive near-pole Boltzmann solution',
               'No derivation of galaxy law, kappa, abundance, dark energy or global novelty']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('checks','phase_rows')},indent=2))
print('All %d bounded controls passed.' % len(checks))
