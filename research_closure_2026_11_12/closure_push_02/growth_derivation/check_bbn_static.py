#!/usr/bin/env python3
"""Independent unchanged-FRW proxy and scalar static-bound audit, no driver imports."""
import argparse
import json
from pathlib import Path
import mpmath as mp
import sympy as s

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    mp.mp.dps = 70
    checks = []

    def check(name, passed, **details):
        checks.append(dict(name=name, passed=bool(passed), **details))

    K, mu, n0, a, od, rr, h0, i0 = s.symbols('K mu n0 a Omega_d Omega_r H0 I0', positive=True)
    q = 1+K*n0/(mu**2*a**3)
    rho = mu**2*(q*q-1)/(2*K)
    residual = s.simplify(rho-n0/a**3-K*n0*n0/(2*mu**2*a**6))
    check('exact_FRW_energy_decomposition', residual == 0, residual=str(residual))
    crit = 3*h0*h0/(2*K)
    ratio = K*(od*crit)**2/(2*mu**2*a**6)/(rr*crit/a**4)
    residual = s.simplify(ratio-od*(3*h0*h0*od)/(4*mu**2*rr*a*a))
    check('action_to_radiation_ratio', residual == 0, residual=str(residual))
    d = s.symbols('delta', positive=True)
    I = 3*s.exp(-s.Rational(2,3))-(1-3*s.log(d))*d
    check('moment_derivative', s.simplify(s.diff(I,d)-(2+3*s.log(d))) == 0)
    m = lambda x: mp.mpf(str(x))
    kd = json.loads((HERE/'sources/KD1_inputs.json').read_text())
    match = json.loads((HERE/'sources/matching_results.json').read_text())
    reported = json.loads((HERE/'sources/static_pressure_results.json').read_text())
    backgrounds = {}
    for name, foot in kd['footings'].items():
        par = foot['setting']
        H0 = 100*m(par['h'])/m('299792.458')
        Omega_d = m(par['omega_d'])/m(par['h'])**2
        Omega_r = m(foot['B1']['Omega_r'])
        I0 = m(par['I0_Mpc-2'])
        astar = 1/(1+m('1e5')/(m('8.617333262e-5')*m('2.7255')))
        normal_err = abs(I0/(3*H0**2*Omega_d)-1)
        check(name+'_normalization', normal_err < mp.mpf('1e-13'), relative_error=str(normal_err))
        eps = m('.067')
        bound = mp.sqrt(Omega_d*I0/(4*eps*Omega_r*astar**2))
        bound_err = abs(bound/m(foot['B1']['mu_B1b'])-1)
        check(name+'_frozen_BBN_proxy', bound_err < mp.mpf('1e-13'), relative_error=str(bound_err))
        rows = []
        for mass in [m(foot['B1']['mu_B1a']),m(foot['G9a_jeans']['mu_J']),bound]:
            # Independent direct physical-density reconstruction with K=1.
            critical = 3*H0**2/2
            nc = Omega_d*critical
            direct = nc**2/(2*mass**2*astar**6)/(Omega_r*critical/astar**4)
            formula = Omega_d*I0/(4*mass**2*Omega_r*astar**2)
            check(name+'_direct_density_'+str(mass), abs(direct/formula-1) < m('1e-13'))
            rows.append({'mu':str(mass),'rho_stiff_over_radiation':str(formula)})
        backgrounds[name]={'mu_BBN_proxy':str(bound),'mu_radiation_budget_one':str(bound*mp.sqrt(eps)),
                           'a_proxy':str(astar),'Omega_d':str(Omega_d),'Omega_r':str(Omega_r),'rows':rows}

    inner = next(x for x in match['rows'] if x['mu_Mpc_inverse']==25120 and x['r_over_rM']==1)
    outer = next(x for x in match['rows'] if x['mu_Mpc_inverse']==25120 and x['r_over_rM']==60)
    qi, qo = 1-m(inner['phi_geo']), 1-m(outer['phi_geo'])
    xi = qi-1
    ri, ro = m(inner['r_Mpc']),m(outer['r_Mpc'])
    accel0 = m('9.3603e-11')/m('299792458')**2*m('3.0857e22')
    flux = ro**2*accel0*m(outer['g_over_a0'])/qo**2-ri**2*accel0*m(inner['g_over_a0'])/qi**2
    volume = (ro**3-ri**3)/qi
    def pressure(mass):
        delta = 1/mass**2
        moment = 3*mp.exp(-mp.mpf(2)/3)-(1-3*mp.log(delta))*delta
        return xi**2/(2*qi*(-mp.log1p(-delta)))*moment
    def flux_ratio(mass, Lam):
        return (pressure(mass)-Lam/3)*volume/flux
    caps=[]
    mub = m(backgrounds['canonical']['mu_BBN_proxy'])
    for ref in reported['raw_lapse_necessary_mu_upper_bound']:
        Lam = m(ref['Lambda_Mpc_inverse2'])
        lo,hi = m('198.25'),m('1000')
        for _ in range(240):
            mid=(lo+hi)/2
            if flux_ratio(mid,Lam)>1: hi=mid
            else: lo=mid
        cap=(lo+hi)/2
        err=abs(cap/m(ref['mu_necessary_upper_Mpc_inverse'])-1)
        check('independent_static_cap_Lambda_'+str(Lam),err<m('1e-8'),relative_error=str(err))
        check('no_overlap_frozen_budget_Lambda_'+str(Lam),mub>cap)
        check('no_overlap_budget_one_Lambda_'+str(Lam),mub*mp.sqrt(m('.067'))>cap)
        caps.append({'Lambda':str(Lam),'mu_static_cap':str(cap),'BBN_bound_over_cap':str(mub/cap),
                     'budget_one_bound_over_cap':str(mub*mp.sqrt(m('.067'))/cap),
                     'max_early_charge_fraction_frozen_budget':str(cap/mub),
                     'required_static_flux_ratio_at_BBN_bound':str(flux_ratio(mub,Lam))})
    # Explicit monotonicity witnesses supplement, not replace, the analytic proof.
    sample=[mp.mpf('1.4')*(mp.mpf('1e8')/mp.mpf('1.4'))**(mp.mpf(j)/100) for j in range(101)]
    check('pressure_floor_monotone_grid',all(pressure(y)>pressure(x) for x,y in zip(sample[:-1],sample[1:])))
    out={'passed':all(x['passed'] for x in checks),'checks':checks,'backgrounds':backgrounds,'static_caps':caps,
         'precision_decimal':70,'scope':'Declared .067 radiation gate and unchanged homogeneous charge; specified static target and rectangular concavity domain. No empirical BBN likelihood or universal theory no-go.'}
    Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'passed':out['passed'],'checks':len(checks),'canonical_mu_BBN':backgrounds['canonical']['mu_BBN_proxy'],'largest_static_cap':caps[-1]['mu_static_cap']}))
    if not out['passed']: raise SystemExit(1)


if __name__=='__main__':main()
