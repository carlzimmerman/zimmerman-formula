"""Transport predictions checked against independent photon histories.

The simulator is the earlier continuous-flight implementation. It is not
changed to enforce the new spatial generator identity or the lag-width band.
"""
from pathlib import Path
import json
import math
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import sympy as sp
from transport import simulate, paired_z


def z_of_mean(values, expected):
    return paired_z(values-expected)


def main():
    # Backward generator: LF = c*mu*dF/dr, L(r.mu)=c-c*kappa*r.mu.
    r, mu, c, a, q = sp.symbols('r mu c a q', real=True)
    kappa = a*(1+q*r**2)
    F = a*r**2 + a*q*r**4/2
    assert sp.simplify(c*mu*sp.diff(F,r)+2*c-2*c*kappa*r*mu-2*c) == 0
    # The physical width-lag bracket is equivalent to a nonnegative boundary term.
    d, b = sp.symbols('d b', nonnegative=True)
    width2 = 4*d**2+4*b*d
    assert sp.expand(width2-4*d**2) == 4*b*d
    assert sp.expand(4*d*(d+1)-width2) == 4*d-4*b*d

    rows=[]
    cases=[(.03,0.,'central'),(.1,0.,'central'),(.3,0.,'central'),
           (1.,0.,'central'),(3.,0.,'central'),(10.,0.,'central'),
           (30.,0.,'central'),(1.,3.,'central'),(10/34,99.,'central'),
           (1.,0.,'volume')]
    for i,(tau0,q,source) in enumerate(cases):
        sample=simulate(60000,tau0,q,0.,source,9212700+i)
        lag=sample['delay']; v2=sample['v']**2
        dmean=float(lag.mean()); wmean=float(v2.mean())
        dse=float(lag.std(ddof=1)/math.sqrt(len(lag)))
        radial_tau=tau0*(1+q/3)
        prediction=tau0*(.5+q/4)
        row=dict(tau0=tau0,density_gradient=q,source=source,
            radial_tau=radial_tau,photons=len(lag),seed=9212700+i,
            lag_prediction=prediction,lag_measured=dmean,lag_standard_error=dse,
            measured_width_squared=wmean,mean_N=float(sample['n'].mean()),
            width_to_N_z=paired_z(v2-2*sample['n']))
        assert abs(row['width_to_N_z']) < 6
        if source=='central':
            row['radial_identity_z']=z_of_mean(lag,prediction)
            assert abs(row['radial_identity_z']) < 6
            exit_mu=sample['time']-lag
            assert exit_mu.min() >= -1e-12 and exit_mu.max() <= 1+1e-12
            row['mean_exit_mu']=float(exit_mu.mean())
            lower_residual=wmean-4*dmean*dmean
            lower_influence=(v2-wmean)-8*dmean*(lag-dmean)
            lower_se=float(lower_influence.std(ddof=1)/math.sqrt(len(lag)))
            row['uniform_band_lower_residual_z']=lower_residual/lower_se
            if q==0:
                # Checks involving the spatial model, the spectral model, and both.
                row['compensator_z']=paired_z(sample['n']-tau0*sample['time'])
                row['closure_z']=paired_z(v2-tau0*tau0-2*tau0*exit_mu)
                assert abs(row['compensator_z']) < 6
                assert abs(row['closure_z']) < 6
                upper_residual=4*dmean*(dmean+1)-wmean
                upper_influence=(8*dmean+4)*(lag-dmean)-(v2-wmean)
                upper_se=float(upper_influence.std(ddof=1)/math.sqrt(len(lag)))
                row['uniform_band_upper_residual_z']=upper_residual/upper_se
                assert lower_residual >= -6*lower_se
                assert upper_residual >= -6*upper_se
            elif q==99:
                # Deliberate falsification of extending the uniform bound to all profiles.
                assert lower_residual < -6*lower_se
                row['uniform_band_incorrectly_extended']='REFUTED by this radial profile'
                row['wrong_uniform_lag_z']=z_of_mean(lag,radial_tau/2)
                assert abs(row['wrong_uniform_lag_z']) > 6
        else:
            row['wrong_central_source_lag_z']=z_of_mean(lag,tau0/2)
            assert abs(row['wrong_central_source_lag_z']) > 6
        rows.append(row)

    kb=1.380649e-23; me=9.1093837139e-31; light=299792458.
    au=149597870700.; day=86400.
    R=941*au; T=1e4; W=2000e3
    s=math.sqrt(kb*T/me)
    sigma=W/(math.sqrt(2)*math.log(2))
    x=sigma/s
    lo=(R/light)*(math.sqrt(1+x*x)-1)/2
    hi=(R/light)*x/2
    min_amplitude=max(0.,1-2*math.pi*hi/(200*day))
    radius_needed=(.9*200*day/(2*math.pi))*2*light*s/sigma
    result=dict(status='proved conditional transport bound; finite numerical cross-checks',
        examples=dict(radius_AU=941,temperature_K=T,full_Laplace_FWHM_kms=2000,
            predicted_mean_lag_days=[lo/day,hi/day],
            amplitude_floor_at_200_rest_days=min_amplitude,
            necessary_radius_AU_for_tenfold_suppression=radius_needed/au),
        rows=rows,photons=sum(row['photons'] for row in rows),
        non_claims=['No observed LRD exclusion','No global novelty claim',
            'Uniform-density lag-width bound is not valid for arbitrary radial profiles',
            'No identification of scattering radius with continuum photosphere'],
        versions=dict(python=sys.version,numpy=np.__version__,sympy=sp.__version__))
    Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['examples'],indent=2))
    for row in rows:
        print(row['source'],row['tau0'],row['density_gradient'],
              'lag',row['lag_measured'],'prediction',row['lag_prediction'],
              'z',row.get('radial_identity_z',row.get('wrong_central_source_lag_z')))
    print('Completed photons:',result['photons'])


if __name__=='__main__':
    main()
