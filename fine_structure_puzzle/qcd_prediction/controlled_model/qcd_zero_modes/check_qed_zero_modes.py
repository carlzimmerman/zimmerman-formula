#!/usr/bin/env python3
"""LO Dashen operator: independently checked disk and SU2 Haar integrals."""
import argparse
import importlib.util
import json
from pathlib import Path
import mpmath as mp

spec=importlib.util.spec_from_file_location('qcd_zero',Path(__file__).with_name('check_qcd_zero_modes.py'))
qcd=importlib.util.module_from_spec(spec)
spec.loader.exec_module(qcd)


def disk(z,t,moments=True):
    scale=abs(z)
    cuts=[0,mp.mpf('.01'),mp.mpf('.1'),mp.mpf('.5'),1]
    def integrate(f):
        return mp.quad(f,cuts)
    def w(s):
        return mp.exp(-t*s-scale)
    Z=integrate(lambda s: w(s)*mp.besseli(0,z*mp.sqrt(1-s)))
    result=dict(logz=scale+mp.log(Z))
    if not moments:
        return result
    A=integrate(lambda s: w(s)*mp.sqrt(1-s)*mp.besseli(1,z*mp.sqrt(1-s)))/Z
    S=integrate(lambda s: s*w(s)*mp.besseli(0,z*mp.sqrt(1-s)))/Z
    AS=integrate(lambda s: s*w(s)*mp.sqrt(1-s)*mp.besseli(1,z*mp.sqrt(1-s)))/Z
    A2=integrate(lambda s: w(s)*(1-s)/2*(mp.besseli(0,z*mp.sqrt(1-s))
                    +mp.besseli(2,z*mp.sqrt(1-s))))/Z
    result.update(A=A,S=S,At=-(AS-A*S),Az=A2-A*A)
    return result


def independent_haar_logz(z,t):
    # Direct SU2 axis/angle: s=sin(phi)^2(1-n3^2); integrate n3 via 1F1.
    scale=abs(z)
    f=lambda phi: (mp.sin(phi)**2*mp.exp(z*mp.cos(phi)-scale-t*mp.sin(phi)**2)
                    *mp.hyp1f1(mp.mpf('.5'),mp.mpf('1.5'),t*mp.sin(phi)**2))
    value=2/mp.pi*mp.quad(f,[0,mp.pi/4,mp.pi/2,3*mp.pi/4,mp.pi])
    return scale+mp.log(value)


def run(inputs,precision):
    mp.mp.dps=precision
    tol=mp.mpf(inputs['sum_tolerance'])
    dtol=mp.mpf(inputs['derivative_tolerance'])
    h=mp.mpf(inputs['finite_difference_step'])
    checks=[]

    def check(label,error,scale=1,tolerance=tol):
        err=abs(error)/max(abs(scale),mp.mpf('1e-400'))
        ok=err<tolerance
        checks.append(dict(label=label,error=err,tolerance=tolerance,passed=bool(ok)))
        if not ok:
            raise AssertionError('%s: %s >= %s' % (label,err,tolerance))

    rows=[]
    insertions=[]
    for mus in inputs['mu_values']:
        mu=mp.mpf(mus)
        pure=qcd.response(mu,0)
        z=2*mu
        k=2*pure['r']/z
        kp=2*(pure['rprime']/z-pure['r']/z**2)
        atzero=disk(z,0)
        check('first Dashen insertion mu='+mus,atzero['S']-k)
        check('first mixed mass insertion mu='+mus,atzero['At']+kp)
        first_metric=k+z*kp
        check('first metric cancellation identity mu='+mus,first_metric-2*pure['rprime'])
        # V=mu and mSigma=1, e4²C=1 for the derivative coefficient.
        derivative=qcd.fd1(lambda vv: vv*(2*qcd.response(vv,0)['r']/(2*vv)),mu,h)
        check('first metric independent volume derivative mu='+mus,
              derivative-first_metric,1,dtol)
        insertions.append(dict(mu=mu,K=k,Kprime=kp,first_mass_response=-kp,
                               first_chiV_response=-mu*kp/2,
                               metric_response_per_e2C=first_metric))

        for ts in inputs['theta_over_pi']:
            theta=mp.mpf(ts)*mp.pi
            c,s=mp.cos(theta/2),mp.sin(theta/2)
            z=2*mu*c
            for es in inputs['t_values']:
                t=mp.mpf(es)
                d=disk(z,t)
                label='mu=%s,theta/pi=%s,t=%s' % (mus,ts,es)
                check('independent Haar versus disk '+label,
                      independent_haar_logz(z,t)-d['logz'],1+abs(d['logz']))
                if t==0:
                    check('pure-QCD reduction '+label,d['logz']-qcd.response(mu,theta)['logz'])
                if abs(z)<mp.mpf('1e-40'):
                    expected=mp.log(-mp.expm1(-t)/t) if t else mp.mpf(0)
                    check('theta-pi exact disk limit '+label,d['logz']-expected)
                condensate=c*d['A']
                chiv=mu*c*d['A']/2-mu*mu*s*s*d['Az']
                alpha_logz=-t*d['S']
                alpha_cond=c*t*d['At']
                check('finite t charge derivative '+label,
                      t*qcd.fd1(lambda tt: disk(z,tt,False)['logz'],t,h)-alpha_logz,
                      1+abs(alpha_logz),dtol)
                check('finite t mass derivative '+label,
                      qcd.fd1(lambda mm: disk(2*mm*c,t,False)['logz'],mu,h)/2-condensate,
                      1+abs(condensate),dtol)
                check('finite t theta susceptibility '+label,
                      -qcd.fd2(lambda th: disk(2*mu*mp.cos(th/2),t,False)['logz'],theta,h)-chiv,
                      1+abs(chiv),dtol)
                if ts=='0':
                    check('finite t Ward identity '+label,chiv-mu*condensate/2)
                rows.append(dict(mu=mu,theta_over_pi=mp.mpf(ts),t=t,logz=d['logz'],
                                 condensate_over_Sigma=condensate,chi_times_V=chiv,
                                 alpha_derivative_logz=alpha_logz,
                                 alpha_derivative_condensate_over_Sigma=alpha_cond,
                                 mean_charged_coordinate_squared=d['S']))

    saddle=[]
    for mus in inputs['saddle_mu_values']:
        mu=mp.mpf(mus)
        pure=qcd.response(mu,0)
        for ls in inputs['saddle_t_over_mu']:
            lam=mp.mpf(ls)
            t=lam*mu
            d=disk(2*mu,t)
            ratio=mp.exp(d['logz']-pure['logz'])
            saddle.append(dict(mu=mu,t_over_mu=lam,
                exact_EM_over_pure_partition=ratio,
                canonical_charged_pair_ratio=1/(1+lam),
                scaled_ratio=ratio*(1+lam),
                metric_energy_difference_over_mSigma=-2*(d['A']-pure['r'])+lam*d['S'],
                alpha_derivative_logz=d['S']*(-t)))
    return dict(precision=precision,rows=rows,insertions=insertions,saddle_rows=saddle,
                checks=checks,all_checks_passed=all(c['passed'] for c in checks))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--inputs',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    inputs=json.loads(Path(args.inputs).read_text())
    runs=[run(inputs,p) for p in inputs['precisions_decimal']]
    errors=[]
    for a,b in zip(runs[0]['rows'],runs[1]['rows']):
        for key in ['logz','condensate_over_Sigma','chi_times_V','alpha_derivative_logz',
                    'alpha_derivative_condensate_over_Sigma']:
            error=abs(a[key]-b[key])/(1+abs(b[key]))
            assert error<mp.mpf(inputs['precision_tolerance']),(key,error)
            errors.append(error)
    result=dict(outcome='implementation and finite assertion verified in stated range',
                max_precision_error=max(errors),runs=runs,
                caveat='Exact retained LO group integral only. Unknown C and matching N(V,alpha) remain. No full QCD+QED gravitational coefficient or alpha root.')
    Path(args.output).write_text(json.dumps(qcd.serialize(result),indent=2)+'\n')
    print(json.dumps(dict(cases_per_precision=len(runs[-1]['rows']),
                          checks_per_precision=len(runs[-1]['checks']),
                          all_checks_passed=runs[-1]['all_checks_passed'],
                          max_precision_error=mp.nstr(max(errors),12)),indent=2))


if __name__=='__main__':
    main()
