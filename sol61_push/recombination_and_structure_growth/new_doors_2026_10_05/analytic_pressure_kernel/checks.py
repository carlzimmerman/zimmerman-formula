import argparse
import json
import math
from pathlib import Path
from scipy.integrate import quad


def kernel(a, ad):
    return math.log(a / ad) - 2 * (1 - math.sqrt(ad / a))


def run():
    checks = []
    def check(name, ok, detail):
        checks.append({'name': name, 'passed': bool(ok), 'detail': detail})
    ad, hm = 0.02, 1.7
    for a in (0.03, 0.1, 0.5):
        for amplitude, initial_u, coefficient in ((0.3, 0.7, 0.01), (2.0, -0.2, -0.02)):
            u = initial_u + 2 * coefficient * amplitude / hm * (math.sqrt(a) - math.sqrt(ad))
            uq = initial_u + quad(lambda s: coefficient * amplitude / hm / math.sqrt(s), ad, a, epsabs=1e-12)[0]
            delta = 2 * initial_u / hm * (1 / math.sqrt(ad) - 1 / math.sqrt(a)) + 2 * coefficient * amplitude / hm**2 * kernel(a, ad)
            dq = quad(lambda s: (initial_u + 2 * coefficient * amplitude / hm * (math.sqrt(s) - math.sqrt(ad))) / (hm * s**1.5), ad, a, epsabs=1e-12)[0]
            check('quadrature U and Delta', abs(u-uq)<1e-10 and abs(delta-dq)<1e-10, {'a':a, 'coefficient':coefficient, 'errors':[u-uq,delta-dq]})
    q, v2, a1, a2 = 0.003, 0.2, 0.04, 0.3
    slopes = []
    for k, amplitude, initial_u in ((2.,0.4,1.3),(5.,3.0,-7.)):
        coeff = q*k**4-v2*k**2
        def u(a):
            return initial_u + 2*coeff*amplitude/hm*(math.sqrt(a)-math.sqrt(ad))
        stat = hm*(u(a2)-u(a1))/(2*amplitude*(math.sqrt(a2)-math.sqrt(a1))*k**2)
        slopes.append(stat)
        check('epoch statistic cancels initial mode and amplitude', abs(stat-(q*k*k-v2))<1e-12, {'k':k,'statistic':stat})
    qfit = (slopes[1]-slopes[0])/(25-4)
    vfit = qfit*4-slopes[0]
    check('two k recover wave and gas coefficients', abs(qfit-q)<1e-12 and abs(vfit-v2)<1e-12, {'Q':qfit,'v0_squared':vfit})
    check('mutation missing k squared rejected', abs((q*5**2-v2)-slopes[1])<1e-12 and abs((q-v2)-slopes[1])>0.01, {'wrong_statistic':q-v2,'correct':slopes[1]})
    mpc = 3.085677581491367e22
    hbar = 1.054571817e-34
    evkg = 1.782661921627898e-36
    h0 = 67.36*1000/mpc
    hm_si = h0*math.sqrt(0.315)
    mass_ev = 2e-20
    q_si = hbar*hbar/(4*(mass_ev*evkg)**2)
    benchmarks = []
    for k_mpc in (0.1,1.,100.,1000.):
        eps = q_si*(k_mpc/mpc)**4/(hm_si**2*ad)
        correction = 2*q_si*(k_mpc/mpc)**4/hm_si**2*kernel(0.5,ad)/0.5
        benchmarks.append({'k_per_Mpc':k_mpc,'epsilon_at_ad':eps,'relative_Delta_over_growing_delta_at_a05':correction,'born_frequency_small':eps<0.1})
    check('large scale tiny and very small scale Born failure', benchmarks[0]['epsilon_at_ad']<1e-12 and benchmarks[-1]['epsilon_at_ad']>1, benchmarks)
    return {'claim':'EdS Born relative pressure kernel', 'checks':checks,'all_passed':all(c['passed'] for c in checks),'benchmarks':benchmarks,'constants':{'H0_km_s_Mpc':67.36,'Omega_m':0.315,'mass_eV_c2':mass_ev,'a_d':ad,'hbar_SI':hbar,'Mpc_metres':mpc,'eV_c2_kg':evkg},'non_claims':['Not exact recombination transfer evolution','Not cold identity or mass inference','No applicability where Born corrections are large']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = run()
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'all_passed':result['all_passed'],'checks':len(result['checks']),'benchmarks':result['benchmarks']}))
    raise SystemExit(0 if result['all_passed'] else 1)
