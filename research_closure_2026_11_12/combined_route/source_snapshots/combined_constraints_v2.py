"""Necessary compatibility conditions, not fitted formation predictions.

All imposed hypotheses are labeled in output; no observational likelihood is run.
Usage: python3 combined_constraints.py OUTPUT.json
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

R_COSMIC=5.41
G,MSUN,MPC=6.674e-11,1.989e30,3.0857e22
A0=9.3603e-11


def enhancement(x):
    L=1/(1+x)
    return math.atan(math.sqrt(L))/(x/(1+x)*math.sqrt(L))


def excess(x):
    return enhancement(x)-1


def slope(x):
    """d ln(excess)/d ln x, analytic derivative."""
    t=1/math.sqrt(1+x)
    dlogF=-1/(1+x)-x*t/(2*(1+x))*(1/((1+t*t)*math.atan(t))-1/t)
    return enhancement(x)/excess(x)*dlogF


def fold(Mb,z):
    ratio=float(np.interp(z,[0,1,2,4],[.52,.46,.435,.32]))
    H=67.4e3/MPC*math.sqrt(.315*(1+z)**3+.685)
    return ratio*(2*G*Mb/H**2)**(1/3)


def surrogate_checks(X):
    """Positive finite-mass spherical equilibrium comparison, dimensionless G=Mb=rM=1.

    It is not an AQUAL solution or a field-action completion.
    Extended baryon mass Mb(r)=r^2/(r+b)^2, b=.2 avoids a point-mass energy divergence.
    """
    t=2*X/math.pi
    baryon_scale=.2
    coefficient=2*X/math.pi
    def density(r):
        return coefficient/(4*math.pi*t*r*r*(1+(r/t)**2))
    def cold_mass(r):
        return coefficient*math.atan(r/t)
    def mass(r):
        return cold_mass(r)+r*r/(r+baryon_scale)**2
    def density_curvature_sign(r):
        u2=(r/t)**2
        gamma=2+2*u2/(1+u2)
        dloggamma=4*u2/((1+u2)**2*gamma)
        dm=coefficient/t/(1+u2)+2*baryon_scale*r/(r+baryon_scale)**3
        p=r*dm/mass(r)
        # This positive factor gives d²rho/dPsi² = gamma*rho*r²/(G²M²)*(gamma-1+p-dlngamma).
        return gamma-1+p-dloggamma
    grid=np.geomspace(1e-6,1e6,2001)
    margins=[density_curvature_sign(r) for r in grid]
    total_mass=quad(lambda u: coefficient/(1+u*u),0,np.inf,epsabs=1e-10)[0]
    def pressure(r):
        return quad(lambda u: density(r*math.exp(u))*mass(r*math.exp(u))/(r*math.exp(u)),
                    0,35,epsabs=1e-12,epsrel=1e-9)[0]
    jean_errors=[]
    rows=[]
    for r in [1,10,t,2*t,10*t]:
        h=1e-4
        derivative=(pressure(r*math.exp(h))-pressure(r*math.exp(-h)))/(2*h*r)
        residual=derivative/(-density(r)*mass(r)/r**2)-1
        jean_errors.append(abs(residual))
        rows.append(dict(r_over_rM=r,Mc_over_Mb=cold_mass(r),sigma2_over_GMb_rM=pressure(r)/density(r)))
    assert abs(total_mass/X-1)<1e-12
    assert min(margins)>0
    assert max(jean_errors)<1e-5
    return dict(status="positive equilibrium existence diagnostic; no EFE coupling or formation selection",
                rt_over_rM=t,R95_over_rt=math.tan(.95*math.pi/2),
                total_mass_relative_error=abs(total_mass/X-1),
                minimum_sampled_convexity_margin=min(margins),
                jeans_max_relative_residual=max(jean_errors),rows=rows,
                proof="Analytic convexity for all r>0 is in DERIVATION.md; grid is a cross-check only")


def main():
    target=59.5
    xK=brentq(lambda x:excess(x)-target,1e-5,1,xtol=1e-15)
    xF=xK*((1+2.5)/(1+.3))**1.5
    XF=excess(xF)
    ratio0=(math.sqrt(1)/xF/fold(MSUN,2.5))/(math.sqrt(1)/xK/fold(MSUN,.3))
    growth_min=(ratio0/.56)**6
    rate=slope(xK)*(-1.5) # dlnMc/dlna for constant Mb, imposed x∝a^-3/2.
    # A second history keeps the simple interpolation in the environmental
    # scalar proxy as well. This matching is an extra environment hypothesis,
    # not a general vector solution for the cosmic web.
    yK=xK*xK/(1+xK)
    yF=yK*((1+2.5)/(1+.3))**3
    xF_exact=(yF+math.sqrt(yF*yF+4*yF))/2
    XF_exact=excess(xF_exact)
    ratio_exact=ratio0*xF/xF_exact
    growth_exact=(ratio_exact/.56)**6
    slope_errors=[]
    for x in [.001,xK,.1,1,10]:
        finite=(math.log(excess(x*math.exp(1e-5)))-math.log(excess(x*math.exp(-1e-5))))/2e-5
        slope_errors.append(abs(finite-slope(x)))
    assert max(slope_errors)<1e-8
    rho_cold=.265*3*(67.4e3/MPC)**2/(8*math.pi*G)
    masses=[]
    for mb in [1e9,1e10,1e11]:
        rM=math.sqrt(G*mb*MSUN/A0)
        catchment=(3*target*mb*MSUN/(4*math.pi*rho_cold))**(1/3)
        masses.append(dict(Mb_Msun=mb,RE_kpc=rM/xK/MPC*1000,
                           minimum_initial_baryons_Msun=target/R_COSMIC*mb,
                           minimum_baryons_outside_final_aperture_Msun=(target/R_COSMIC-1)*mb,
                           minimum_comoving_catchment_Mpc=catchment/MPC))
    output={"status":"conditional necessary constraints; theory remains open",
       "matching":{"Xc_excess":target,"F_total":target+1,"x_physical":xK,
                   "y_newtonian":xK*xK/(1+xK),"Fb_over_Fc":R_COSMIC/target,
                   "RE_over_rM":1/xK,"dlnX_dlnx":slope(xK)},
       "history_assumptions":["Fixed physical coherence length and density-contrast/geometric coefficient",
                              "x(z)=x(.3)[(1+z)/1.3]^1.5, imposed deep-environment scaling",
                              "Same progenitor-descendant assignment; same initial reservoir for retention fractions",
                              "Cold mass equals AQUAL asymptotic effective excess (unproved bridge)",
                              "Rsettled=RE (unproved); fold interpolation and proxy bounds imported from G242"],
       "history":{"z_early":2.5,"z_late":.3,"x_early":xF,"Xc_early":XF,
                  "constant_mass_f_ratio":ratio0,"proxy_bound":.56,
                  "minimum_baryon_growth_for_proxy_window":growth_min,
                  "required_cold_growth_at_threshold":growth_min*target/XF,
                  "maximum_early_Fc_if_late_Fc_le_1":XF/(growth_min*target),
                  "fixed_Mb_required_dlnMc_dlna_at_late":rate,
                  "rows":[dict(baryon_growth=g,cold_growth=g*target/XF,
                                proxy_ratio=ratio0*g**(-1/6)) for g in [1,2,3,5]]},
       "exact_scalar_environment_history":{
           "hypotheses":"y scales as (1+z)^3; scalar matching y=x²/(1+x); same fixed coefficient and progenitor mapping",
           "x_early":xF_exact,"y_early":yF,"Xc_early":XF_exact,
           "constant_mass_f_ratio":ratio_exact,
           "minimum_baryon_growth_for_proxy_window":growth_exact,
           "required_cold_growth_at_threshold":growth_exact*target/XF_exact,
           "maximum_early_Fc_if_late_Fc_le_1":XF_exact/(growth_exact*target),
           "fixed_Mb_required_dlnMc_dlna_at_late":-slope(xK)*3*(1+xK)/(2+xK)},
       "minimum_reservoirs_assuming_Fc_le_1":masses,
       "verification":{"slope_derivative_max_absolute_error":max(slope_errors)},
       "positive_equilibrium_comparison":surrogate_checks(target)}
    path=Path(sys.argv[1]);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(output,indent=2,allow_nan=False)+"\n")
    print(json.dumps({k:v for k,v in output.items() if k in {"status","matching","history","exact_scalar_environment_history","verification"}},indent=2))


if __name__=="__main__":
    main()
