#!/usr/bin/env python3
"""Two-flavor QCD LO epsilon-regime zero modes; finite deterministic audit."""
import argparse
import json
from pathlib import Path
import mpmath as mp


def serialize(obj):
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [serialize(v) for v in obj]
    if isinstance(obj, (mp.mpf, mp.mpc)):
        return mp.nstr(obj, 65)
    return obj


def fd1(f, x, h):
    return (f(x-2*h)-8*f(x-h)+8*f(x+h)-f(x+2*h))/(12*h)


def fd2(f, x, h):
    return (-f(x+2*h)+16*f(x+h)-30*f(x)+16*f(x-h)-f(x-2*h))/(12*h*h)


def bessel_z(mu, theta):
    z=2*mu*mp.cos(theta/2)
    if not z:
        return mp.mpf(1)
    return 2*mp.besseli(1,z)/z


def response(mu, theta):
    c, s = mp.cos(theta/2), mp.sin(theta/2)
    z=2*mu*c
    # Entire hypergeometric representation avoids a quotient at theta=pi.
    partition=mp.hyper([], [2], z*z/4)
    if abs(z)<mp.mpf('1e-40'):
        r=z/4-z**3/96
        rp=mp.mpf(1)/4-z*z/32
    else:
        r=mp.besseli(2,z)/mp.besseli(1,z)
        rp=1-r*r-3*r/z
    condensate=c*r                   # per flavor, in units of Sigma
    chiv=mu*c*r/2-mu*mu*s*s*rp      # susceptibility times V
    scalar=2*c*c*rp                 # dC/dm in units Sigma^2 V
    return dict(partition=partition, logz=mp.log(partition), z=z, r=r,
                rprime=rp, condensate_over_Sigma=condensate,
                chi_times_V=chiv, scalar_over_Sigma2V=scalar,
                d_mu_logz=2*condensate,
                energy_over_mSigma=-2*condensate)


def haar(mu, theta):
    z=2*mu*mp.cos(theta/2)
    base=mp.quad(lambda phi: mp.sin(phi)**2*mp.exp(z*mp.cos(phi)),
                 [0,mp.pi/2,mp.pi])
    m1=mp.quad(lambda phi: mp.cos(phi)*mp.sin(phi)**2*mp.exp(z*mp.cos(phi)),
               [0,mp.pi/2,mp.pi])/base
    m2=mp.quad(lambda phi: mp.cos(phi)**2*mp.sin(phi)**2*mp.exp(z*mp.cos(phi)),
               [0,mp.pi/2,mp.pi])/base
    return dict(partition=2*base/mp.pi, mean_cos=m1, variance_cos=m2-m1*m1)


def fixed_nu(mu, nu):
    return mp.besseli(nu,mu)**2-mp.besseli(nu-1,mu)*mp.besseli(nu+1,mu)


def topology_tail_bound(mu, cutoff, order):
    # I_n(mu) <= (mu/2)^n/n! exp(mu^2/(4(n+1))).
    # 0 <= Z_n <= I_n^2. For order 0 or 2, use a geometric upper tail.
    n=cutoff+1
    b=(mu/2)**n/mp.factorial(n)*mp.exp(mu*mu/(4*(n+1)))
    ratio=(mu/(2*(n+1)))**2*((mp.mpf(n+1)/n)**order)
    assert ratio<1
    return 2*n**order*b*b/(1-ratio)


def run(inputs, precision):
    mp.mp.dps=precision
    checks=[]
    tol=mp.mpf(inputs['sum_tolerance'])
    dtol=mp.mpf(inputs['derivative_tolerance'])
    h=mp.mpf(inputs['finite_difference_step'])
    cutoff=inputs['topology_cutoff']

    def check(label, error, scale=1, tolerance=tol):
        normalized=abs(error)/max(abs(scale),mp.mpf('1e-400'))
        ok=normalized<tolerance
        checks.append(dict(label=label, normalized_error=normalized,
                           tolerance=tolerance, passed=bool(ok)))
        if not ok:
            raise AssertionError('%s: %s >= %s' % (label,normalized,tolerance))

    # Independent SU(2) Haar measure normalization.
    check('Haar normalization',haar(mp.mpf(0),mp.mpf(0))['partition']-1)
    rows=[]
    topology=[]
    for mus in inputs['mu_values']:
        mu=mp.mpf(mus)
        weights=[fixed_nu(mu,n) for n in range(cutoff+1)]
        assert all(w>0 for w in weights)
        zsum=weights[0]+2*mp.fsum(weights[1:])
        q2=2*mp.fsum(n*n*weights[n] for n in range(1,cutoff+1))/zsum
        zero=response(mu,mp.mpf(0))
        check('theta0 topology variance mu='+mus,q2-zero['chi_times_V'],q2)
        check('finite-volume Ward identity mu='+mus,
              zero['chi_times_V']-mu*zero['condensate_over_Sigma']/2,
              zero['chi_times_V'])
        check('topological total probability mu='+mus,
              (weights[0]+2*mp.fsum(weights[1:]))/zero['partition']-1)
        # Independent derivative of each fixed-nu sector and posterior averaging.
        derivatives=[mp.diff(lambda mm: fixed_nu(mm,n),mu) for n in range(cutoff+1)]
        posterior_cond=(derivatives[0]+2*mp.fsum(derivatives[1:]))/(2*zsum)
        check('fixed-nu condensate sum mu='+mus,
              posterior_cond-zero['condensate_over_Sigma'],zero['condensate_over_Sigma'])
        selected=[]
        for n in inputs['topology_mass_derivative_cases']:
            cnu=derivatives[n]/(2*weights[n])
            selected.append(dict(nu=n, probability_each_sign=weights[n]/zsum,
                                 condensate_over_Sigma=cnu,
                                 mu_times_condensate=mu*cnu))
        topology.append(dict(mu=mu, chiV_from_topology=q2,
                             condensate_from_topology=posterior_cond,
                             selected_sectors=selected,
                             partition_absolute_tail_bound=topology_tail_bound(mu,cutoff,0),
                             Q2_numerator_absolute_tail_bound=topology_tail_bound(mu,cutoff,2)))

        for ts in inputs['theta_over_pi']:
            theta=mp.mpf(ts)*mp.pi
            r=response(mu,theta)
            hh=haar(mu,theta)
            label='mu=%s,theta/pi=%s' % (mus,ts)
            check('Haar versus Bessel '+label,hh['partition']-r['partition'],r['partition'])
            check('Bessel versus hypergeometric '+label,bessel_z(mu,theta)-r['partition'],r['partition'])
            fourier=weights[0]+2*mp.fsum(weights[n]*mp.cos(n*theta) for n in range(1,cutoff+1))
            check('fixed-topology Fourier sum '+label,fourier-r['partition'],r['partition'])
            c,s=mp.cos(theta/2),mp.sin(theta/2)
            check('Haar condensate '+label,c*hh['mean_cos']-r['condensate_over_Sigma'])
            haar_chiv=mu*c*hh['mean_cos']/2-mu**2*s*s*hh['variance_cos']
            check('Haar susceptibility '+label,haar_chiv-r['chi_times_V'],1+abs(r['chi_times_V']))
            check('mass derivative '+label,
                  fd1(lambda mm: response(mm,theta)['logz'],mu,h)-r['d_mu_logz'],
                  1+abs(r['d_mu_logz']),dtol)
            check('theta second derivative '+label,
                  -fd2(lambda tt: response(mu,tt)['logz'],theta,h)-r['chi_times_V'],
                  1+abs(r['chi_times_V']),dtol)
            check('scalar derivative '+label,
                  fd1(lambda mm: response(mm,theta)['condensate_over_Sigma'],mu,h)-r['scalar_over_Sigma2V'],
                  1+abs(r['scalar_over_Sigma2V']),dtol)
            check('theta periodicity '+label,response(mu,theta+2*mp.pi)['partition']-r['partition'],r['partition'])
            check('theta reflection '+label,response(mu,-theta)['partition']-r['partition'],r['partition'])
            rows.append(dict(mu=mu,theta_over_pi=mp.mpf(ts),observables=r,
                             topology_fourier_sum=fourier,haar=hh))

    # The canonical Gaussian constant-mode integral and Haar Jacobian.
    pars={k:mp.mpf(v) for k,v in inputs['normalization_tests'].items()}
    sigma,F,mur,m,V=(pars[k] for k in ['Sigma','F','renormalization_mass','m','volume'])
    m2=2*m*sigma/F**2
    mu=m*sigma*V
    n0=mp.sqrt(mp.pi/2)*(mur*F*mp.sqrt(V))**3
    saddle=mp.exp(2*mu)/(2*mp.sqrt(mp.pi)*mu**mp.mpf('1.5'))
    gaussian_exact=mp.exp(2*mu)*(mur**2/m2)**mp.mpf('1.5')
    check('canonical measure matches Gaussian constant mode',n0*saddle-gaussian_exact,gaussian_exact)
    # Derivatives are computed on separately specified measures and group integral.
    d_haar_saddle=-mp.diff(lambda vv: 2*m*sigma*vv-mp.mpf('1.5')*mp.log(m*sigma*vv),V)
    d_measure=-mp.diff(lambda vv: mp.log(mp.sqrt(mp.pi/2)*(mur*F*mp.sqrt(vv))**3),V)
    check('measure cancels Haar 3/(2V) stress',d_haar_saddle+d_measure+2*m*sigma,1)
    matched_energy=-mp.diff(lambda vv: mp.log(mp.sqrt(mp.pi/2)*(mur*F*mp.sqrt(vv))**3)
                           +response(m*sigma*vv,0)['logz'],V)
    formula_energy=-2*m*sigma*response(mu,0)['r']-mp.mpf('1.5')/V
    check('matched exact volume derivative',matched_energy-formula_energy,1)
    # S4 covariance: a mass- and theta-independent W=A V^(3/4) has a
    # metric derivative distinct from W/V. This is a blind-spot diagnostic,
    # not a newly permitted/fitted QCD term.
    kappa=8*mp.pi**2/3
    diagnostic_V=mp.mpf(11)
    diagnostic_c=mp.mpf(1)
    W=lambda vv: mp.mpf(4)/3*diagnostic_c*kappa**mp.mpf('.25')*vv**mp.mpf('.75')
    H=(kappa/diagnostic_V)**mp.mpf('.25')
    check('S4 metric factor for an unspecified normalization',mp.diff(W,diagnostic_V)-diagnostic_c*H,H)

    saddles=[]
    for mus in inputs['saddle_mu_values']:
        uu=mp.mpf(mus)
        rr=response(uu,0)
        ratio=rr['partition']/(mp.exp(2*uu)/(2*mp.sqrt(mp.pi)*uu**mp.mpf('1.5')))
        residual=2*(1-rr['r'])-mp.mpf('1.5')/uu # m Sigma=1,V=mu.
        saddles.append(dict(mu=uu,exact_over_saddle=ratio,
                            mu_times_ratio_correction=uu*(ratio-1),
                            matched_energy_remainder=residual,
                            mu_squared_matched_energy_remainder=uu*uu*residual))
    return dict(precision=precision,case_count=len(rows),topology_count=len(topology),
                checks=checks,all_checks_passed=all(x['passed'] for x in checks),
                rows=rows,topology=topology,saddle_rows=saddles,
                measure_test=dict(N0=n0,gaussian_partition=gaussian_exact,
                                  haar_saddle_stress=d_haar_saddle,
                                  measure_stress=d_measure,
                                  matched_exact_stress=matched_energy,
                                  constant_mode_eigenvalue=m2))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--inputs',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    inputs=json.loads(Path(args.inputs).read_text())
    runs=[run(inputs,p) for p in inputs['precisions_decimal']]
    lo,hi=runs
    errors=[]
    for a,b in zip(lo['rows'],hi['rows']):
        for key in ['partition','logz','condensate_over_Sigma','chi_times_V','scalar_over_Sigma2V']:
            scale=1+abs(b['observables'][key])
            err=abs(a['observables'][key]-b['observables'][key])/scale
            assert err<mp.mpf(inputs['precision_tolerance']),(key,err)
            errors.append(err)
    result=dict(outcome='implementation and finite assertion verified in stated range',
                max_precision_error=max(errors),runs=runs,
                caveat='Analytic topology-tail bounds and repeated precision; no interval certification. No fixed-mass H->0 QCD energy or electromagnetic response inferred.')
    Path(args.output).write_text(json.dumps(serialize(result),indent=2)+'\n')
    print(json.dumps(dict(cases_per_precision=hi['case_count'],
                          checks_per_precision=len(hi['checks']),all_checks_passed=hi['all_checks_passed'],
                          max_precision_error=mp.nstr(max(errors),12)),indent=2))


if __name__=='__main__':
    main()
