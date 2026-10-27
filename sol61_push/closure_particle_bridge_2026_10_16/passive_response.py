"""Finite-time passive amplification controls, not a formed-halo model.

The analytic bound is proved in PASSIVE_RESPONSE_AND_CLOSURE.tex. Numerical
checks sample its assumptions and compare mode expansion with direct ODEs.
"""
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import eigh

out=Path(sys.argv[1]);assert out.is_dir()
checks=[];rows=[]
def check(name,b):
    checks.append(dict(name=name,passed=bool(b)));assert b,name

def response(vals,weights,t):
    # (1-cos(sqrt(lambda)t))/lambda, regular at lambda=0.
    return float(np.dot(weights,.5*t*t*np.sinc(np.sqrt(vals)*t/(2*math.pi))**2))

# Previously proposed critical scalar/polarization quadratic form.
for C,Z,I in ((1.,1.,1.),(.3,2.,.7),(2.,.4,3.)):
    for k in (.03,.3,1.,3.):
        for Pi in (1e-6,.02,.2,2.):
            mat=np.array([[C*k*k,-k],[-k,1/C+Pi]])
            mass=np.diag([Z,I]);vals,vecs=eigh(mat,mass)
            check('positive two-field eigenvalues '+str((C,Z,I,k,Pi)),min(vals)>0)
            weights=vecs[0,:]**2
            strength=1/Z
            check('inertial spectral sum '+str((C,Z,I,k,Pi)),abs(sum(weights)/strength-1)<2e-14)
            static=(1/C+Pi)/(C*k*k*Pi)
            spectral=float(np.dot(weights,1/vals))
            check('static Schur complement '+str((C,Z,I,k,Pi)),abs(spectral/static-1)<2e-8)
            for t in (.001,.1,1.,10.,100.):
                value=response(vals,weights,t)
                check('finite time bound '+str((C,Z,I,k,Pi,t)),0<=value<=strength*t*t/2*(1+1e-14))
            rows.append(dict(C=C,Z=Z,I=I,k=k,Pi=Pi,eigenvalues=vals.tolist(),
                spectral_weights=weights.tolist(),static_response=static,
                response_at_t10=response(vals,weights,10.),
                minimum_time_to_half_static_bound=math.sqrt(Z*static)))

# Independent direct integration, including cross-observable/source pairs.
ode_rows=[]
for j in range(6):
    transform=np.array([[1.,.2*j,-.1],[.1,1.,.15],[.05,-.1,1.]])
    mass=np.diag([.6+.2*j,1.3,2.])
    stiffness=transform.T@np.diag([.01*(j+1),.7,2.])@transform
    a=np.array([1.,-.3,.2]);b=np.array([.4,1.,-.2])
    vals,vecs=eigh(stiffness,mass)
    cross=(a@vecs)*(b@vecs)
    strength=math.sqrt(float(a@np.linalg.solve(mass,a))*float(b@np.linalg.solve(mass,b)))
    times=np.linspace(0,8,41)
    mi=np.linalg.inv(mass)
    def rhs(t,u):return np.r_[u[3:],mi@(b-stiffness@u[:3])]
    sol=solve_ivp(rhs,(0,8),np.zeros(6),rtol=2e-11,atol=1e-13,t_eval=times)
    check('direct ODE success '+str(j),sol.success)
    error=0.
    for t,q in zip(times,sol.y[:3,:].T):
        value=response(vals,cross,t)
        error=max(error,abs(float(a@q)-value)/(1+abs(value)))
        check('cross-observable bound '+str((j,t)),abs(value)<=strength*t*t/2*(1+1e-13)+1e-14)
    check('direct ODE vs spectral '+str(j),error<2e-9)
    ode_rows.append(dict(case=j,max_normalized_ODE_difference=error,inertial_cross_bound=strength))

# Controlled homogeneous fluid surrogate, not the older collisionless
# Vlasov benchmark or a finite, rotating, reacting halo.
G=6.67430e-11;c=299792458.;gev_j=1.602176634e-10
rho=.3*gev_j/c**2*1e6;dispersion=150000.
sound=math.sqrt(5/3)*dispersion
omegaJ=math.sqrt(4*math.pi*G*rho)
year=365.25*86400.;age=10e9*year;pc=3.085677581491367e16
agebound=.5*(omegaJ*age)**2
gas_rows=[]
for a in (1.,1.000001,1.001,1.1,2.,10.):
    mu=a*a-1
    static=None if mu==0 else 1/mu
    step=.5*(omegaJ*age)**2*float(np.sinc(math.sqrt(mu)*omegaJ*age/(2*math.pi)))**2
    check('Jeans finite-age bound '+str(a),0<=step<=agebound*(1+1e-14))
    gas_rows.append(dict(k_over_kJ=a,static_response=static,step_at_10Gyr=step))
result=dict(model='Canonical stable quadratic sectors; zero initial perturbation; bounded source; finite-time theorem. Gas is a separate adiabatic homogeneous fluid surrogate.',
    two_field_rows=rows,cross_ODE_rows=ode_rows,gas=dict(density_kg_m3=rho,
      one_dimensional_dispersion_m_s=dispersion,adiabatic_sound_m_s=sound,
      inverse_Jeans_frequency_Myr=1/omegaJ/(1e6*year),inverse_Jeans_wavenumber_kpc=sound/omegaJ/(1000*pc),
      age_Gyr=10,dimensionless_finite_age_step_bound=agebound,rows=gas_rows),
    checks=checks,non_claims=['No completed nonlinear formation, source-to-mode matching, physical times for unfixed scalar kinetic coefficients, finite halo, medium-mass derivation or metric completion','No universal exclusion of active, preloaded, unstable or nonlinear response','The .02 MB gate and preceding scalar-abundance limits are not changed','No global novelty claim'])
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(controls=len(checks),gas=result['gas'],near_critical=[r for r in rows if r['C']==r['Z']==r['I']==r['k']==1]),indent=2))
