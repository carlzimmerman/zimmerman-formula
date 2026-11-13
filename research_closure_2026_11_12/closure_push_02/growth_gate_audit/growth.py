#!/usr/bin/env python3
"""Bounded, post-recombination NR growth diagnostic; not a Boltzmann likelihood.

The input is the frozen KD1 parameter record. The principal experiment changes
only the dark self-source from the isolated fluid's 1-kphys^2/mu^2 to the full
polarization value mu^2/(mu^2+kphys^2). It uses pressureless baryons, smooth
radiation in H, a cosmological constant, and explicitly matched initial data.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent
C_KMS = 299792.458
RTOL, ATOL = 2e-11, 2e-12


def cosmology(setting, radiation):
    h = setting['h']
    ob, od = setting['omega_b'] / h**2, setting['omega_d'] / h**2
    return dict(ob=ob, od=od, radiation=radiation,
                vacuum=1-ob-od-radiation, h=h)


def coefficients(lna, par):
    a = np.exp(lna)
    b, d = par['ob'] / a**3, par['od'] / a**3
    rad = par['radiation'] / a**4
    e2 = b+d+rad+par['vacuum']
    drag = 2 - (3*(b+d)+4*rad)/(2*e2)
    return a, drag, 1.5*b/e2, 1.5*d/e2


def source_factor(k, a, mu, model):
    if mu is None or model == 'reference':
        return np.ones_like(k)
    if model == 'polarized':
        return 1/(1+(k/(a*mu))**2)
    if model == 'isolated':
        return 1-(k/(a*mu))**2
    if model == 'wrong_comoving':
        return 1/(1+(k/mu)**2)
    raise ValueError(model)


def initial(zstart, par, ic):
    a = 1/(1+zstart)
    # Exact growing Meszaros solution for pressureless matter + smooth radiation
    # with Lambda=0; Lambda at these initial epochs is negligible, documented.
    if par['radiation']:
        y = a*(par['ob']+par['od'])/par['radiation']
        f = 1.5*y/(1+1.5*y)
    else:
        f = 1.0
    return np.array([1., f, 1., f] if ic == 'equal' else [0., 0., 1., f])


def solve(k, zstart, zouts, mu, par, ic='equal', model='polarized',
          rtol=RTOL, atol=ATOL):
    """Four states per k: baryon density/ln(a) derivative, dark counterparts."""
    k = np.atleast_1d(k).astype(float)
    y0 = np.tile(initial(zstart, par, ic), (len(k), 1))
    def rhs(lna, flat):
        y = flat.reshape(-1, 4)
        a, drag, gb, gd = coefficients(lna, par)
        f = source_factor(k, a, mu, model)
        out = np.empty_like(y)
        out[:, 0], out[:, 2] = y[:, 1], y[:, 3]
        out[:, 1] = gb*y[:, 0] + gd*y[:, 2] - drag*y[:, 1]
        out[:, 3] = gb*y[:, 0] + gd*f*y[:, 2] - drag*y[:, 3]
        return out.ravel()
    times = np.log(1/(1+np.array(zouts)))
    sol = solve_ivp(rhs, [math.log(1/(1+zstart)), float(times[-1])],
                    y0.ravel(), method='DOP853', rtol=rtol, atol=atol,
                    t_eval=times)
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.y.T.reshape(len(zouts), len(k), 4)


def total(y, par):
    return (par['ob']*y[..., 0]+par['od']*y[..., 2])/(par['ob']+par['od'])


def midpoint(k, zstart, zend, mu, par, steps):
    """Separate implementation: assemble a linear matrix and midpoint solve."""
    k = np.atleast_1d(k).astype(float)
    y = np.tile(initial(zstart, par, 'equal'), (len(k), 1))
    grid = np.linspace(-math.log1p(zstart), -math.log1p(zend), steps+1)
    identity = np.eye(4)[None, :, :]
    hstep = grid[1]-grid[0]
    for lo, hi in zip(grid[:-1], grid[1:]):
        a = math.exp((lo+hi)/2)
        e = par['radiation']/a**4 + (par['ob']+par['od'])/a**3 + par['vacuum']
        dl = -(4*par['radiation']/a**4 + 3*(par['ob']+par['od'])/a**3)/(2*e)
        gb, gd = 1.5*par['ob']/a**3/e, 1.5*par['od']/a**3/e
        suppress = (mu*a)**2/((mu*a)**2+k*k)
        mat = np.zeros((len(k), 4, 4))
        mat[:, 0, 1] = mat[:, 2, 3] = 1
        mat[:, 1, 0], mat[:, 1, 2] = gb, gd
        mat[:, 3, 0], mat[:, 3, 2] = gb, gd*suppress
        mat[:, 1, 1] = mat[:, 3, 3] = -(2+dl)
        y = np.linalg.solve(identity-hstep*mat/2,
                            (identity+hstep*mat/2) @ y[..., None])[..., 0]
    return y


def benchmarks(par):
    checks, details = {}, {}
    def check(name, error, limit):
        checks[name] = bool(error <= limit)
        details[name] = dict(error=float(error), limit=limit)
    eds = dict(ob=.16, od=.84, radiation=0., vacuum=0., h=par['h'])
    yy = solve([.1, 2.], 999, [0], None, eds)
    check('EdS_reference_delta_a', np.max(np.abs(yy[0, :, [0, 2]]/1000-1)), 1e-9)
    # Exact pure-dark high-k, zero self-source limit: delta=C1+C2*a^-1/2.
    # mu=0 is evaluated with a positive limiting mu to avoid a floating division.
    pure = dict(eds, ob=0., od=1.)
    yp = solve([1.], 99, [0], 1e-20, pure)[0, 0, 2]
    check('pure_dark_highk_freezes', abs(yp-(3-2/10)), 2e-9)
    # Constant high-k two-component matrix; exact dominant eigenmode exponent.
    fb = eds['ob']; fd = eds['od']
    lam = (fb+math.sqrt(fb*fb+4*fb*fd))/2
    exponent = (-.5+math.sqrt(.25+6*lam))/2
    mat = np.array([[0., 1., 0., 0.], [1.5*fb, -.5, 1.5*fd, 0.],
                    [0., 0., 0., 1.], [1.5*fb, 0., 0., -.5]])
    eigvec = np.array([1., exponent, fb/lam, exponent*fb/lam])
    check('highk_baryon_feedback_eigenmode', np.max(abs(mat@eigvec-exponent*eigvec)), 2e-14)
    details['highk_growing_exponent'] = exponent
    mr = dict(par, vacuum=0.)
    yi = initial(1090, mr, 'equal')[0]
    ym = solve([.2], 1090, [0], None, mr)[0, 0, 0]
    aeq = mr['radiation']/(mr['ob']+mr['od'])
    mes = (1+1.5/aeq)/(1+1.5/1091/aeq)
    check('Meszaros_smooth_radiation', abs(ym/yi/mes-1), 1e-9)
    kvals=np.array([.2*par['h'], 3*par['h'], 20/3, 10.])
    exact=solve(kvals,1090,[0],198.254232363749,par)[0]
    mid1=midpoint(kvals,1090,0,198.254232363749,par,2048)
    mid2=midpoint(kvals,1090,0,198.254232363749,par,4096)
    e1=np.max(abs(mid1/exact-1)); e2=np.max(abs(mid2/exact-1))
    check('independent_midpoint', e2, 4e-6)
    check('midpoint_second_order_ratio', abs(e1/e2-4), .02)
    strict=solve(kvals,1090,[0],198.254232363749,par,rtol=2e-13,atol=2e-14)[0]
    check('DOP853_tolerance_refinement',np.max(abs(strict/exact-1)),1e-9)
    wrong=solve(kvals,1090,[0],198.254232363749,par,model='wrong_comoving')[0]
    details['mutation_wrong_comoving_max_density_ratio_error']=float(np.max(abs(total(wrong,par)/total(exact,par)-1)))
    checks['mutation_wrong_comoving_bites']=details['mutation_wrong_comoving_max_density_ratio_error']>.5
    iso=solve(kvals,1090,[0],198.254232363749,par,model='isolated')[0]
    details['mutation_isolated_max_density_ratio_error']=float(np.max(abs(total(iso,par)/total(exact,par)-1)))
    checks['mutation_isolated_bites']=details['mutation_isolated_max_density_ratio_error']>.5
    details['old_isolated_vs_corrected_z0']=[dict(k=float(k),corrected=float(v),isolated=float(w))
                                           for k,v,w in zip(kvals,total(exact,par),total(iso,par))]
    return checks, details


def bbn_record(foot):
    s, b = foot['setting'], foot['B1']
    h=s['h']; od=s['omega_d']/h**2
    i0=s['I0_Mpc-2']; rad=b['Omega_r']
    a=1/(1+1e5/(8.617333262e-5*2.7255))
    cap=.067
    mub=math.sqrt(od*i0/(4*cap*rad*a*a))
    mua=math.sqrt(i0*.99/(4*.01*(1/3401)**3))
    rows=[]
    for mu in [mua, foot['G9a_jeans']['mu_J'], mub]:
        w0=i0/(4*mu*mu)
        ratio=od*w0/(rad*a*a)
        rows.append(dict(mu=mu,w_z3400=w0/(w0+3401**-3),
                         stiff_over_radiation_at_0p1MeV=ratio,
                         H_over_radiation_only=math.sqrt(1+ratio),
                         max_early_charge_fraction_for_frozen_budget=mu/mub))
    return dict(T_eV=1e5, Tcmb_K=2.7255, a_BBN=a, radiation_budget=cap,
                budget_equivalent_DeltaNeff=cap*(1+.2271*3.046)/.2271,
                mu_B1a=mua,mu_B1b=mub,Omega_d=od,Omega_r=rad,I0=i0,
                exact_current_n_scaling='a^-3',exact_stiff_scaling='a^-6',
                rows=rows,
                matches_record_rel=max(abs(mua/b['mu_B1a']-1),abs(mub/b['mu_B1b']-1)),
                I0_normalization_rel=abs(i0/(3*(100*h/C_KMS)**2*od)-1))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True); args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    kd=json.loads((HERE/'sources/03_kd1.json').read_text())
    allres={}; bbns={}; checks={}; details={}
    for name,foot in kd['footings'].items():
        par=cosmology(foot['setting'],foot['B1']['Omega_r'])
        lowmu=foot['B1']['mu_B1a']; highmu=foot['G9a_jeans']['mu_J']
        ks=np.array([.2*par['h'],.2,1.,3*par['h'],20/3,2*math.pi*par['h']/.42])
        labels=['MK1_0p2h','0p2_per_Mpc','1_per_Mpc','MK1_3h','DT2_20over3',
                'QX3_forest_wavelength_0p42_over_h']
        rows=[]
        for zstart in [1090.,100.]:
            for ic in ['equal','baryon_zero']:
                zouts=[10.,3.,0.]
                ref=solve(ks,zstart,zouts,None,par,ic)
                low=solve(ks,zstart,zouts,lowmu,par,ic)
                high=solve(ks,zstart,zouts,highmu,par,ic)
                for iz,z in enumerate(zouts):
                    tr=total(ref[iz],par)
                    for ik,(k,label) in enumerate(zip(ks,labels)):
                        rlo=total(low[iz,ik],par)/tr[ik]
                        rhi=total(high[iz,ik],par)/tr[ik]
                        rows.append(dict(zstart=zstart,ic=ic,z=z,k_Mpc=float(k),label=label,
                            low_mu=lowmu,high_mu=highmu,low_total_amplitude_ratio=float(rlo),
                            low_total_power_ratio=float(rlo*rlo),high_total_amplitude_ratio=float(rhi),
                            high_total_power_ratio=float(rhi*rhi),
                            low_dark_amplitude_ratio=float(low[iz,ik,2]/ref[iz,ik,2]),
                            low_baryon_amplitude_ratio=float(low[iz,ik,0]/ref[iz,ik,0]),
                            reference_total_amplitude=float(tr[ik])))
                checks[name+f'_positive_ordered_z{zstart}_{ic}']=bool(
                    np.all(low[:,:, [0,2]]>0) and np.all(total(low,par)<=total(high,par)*(1+1e-9))
                    and np.all(total(high,par)<=total(ref,par)*(1+1e-9)))
        # Half-power location is a diagnostic, not a newly invented exclusion.
        grid=np.geomspace(.03,30,121)
        ref=solve(grid,1090,[3.],None,par)
        low=solve(grid,1090,[3.],lowmu,par)
        power=(total(low,par)/total(ref,par))[0]**2
        crossing=np.where(power<=.5)[0]
        bracket=None if not len(crossing) else [float(grid[crossing[0]-1]),float(grid[crossing[0]])]
        np.savez(out/f'{name}_z3_curve.npz',k_Mpc=grid,power_ratio=power,
                 ref=ref,low=low)
        xstart=foot['setting']['I0_Mpc-2']/(2*lowmu**2)*(1091**3)
        astart=1/1091
        e2=(par['ob']+par['od'])/astart**3+par['radiation']/astart**4+par['vacuum']
        ah=astart*(100*par['h']/C_KMS)*math.sqrt(e2)
        allres[name]=dict(parameters=par,rows=rows,halfpower_k_bracket_z3=bracket,
                          max_xbar_from_z1090_low_mu=xstart,
                          min_k_over_aH_start=float(min(ks)/ah),
                          clock_stiff_fraction_of_radiation_start=
                          par['od']*foot['setting']['I0_Mpc-2']/(4*lowmu**2*par['radiation']*astart**2))
        bbns[name]=bbn_record(foot)
        checks[name+'_BBN_exact_record']=bbns[name]['matches_record_rel']<1e-13
        checks[name+'_I0_normalization']=bbns[name]['I0_normalization_rel']<1e-13
    canonical=cosmology(kd['footings']['canonical']['setting'],kd['footings']['canonical']['B1']['Omega_r'])
    more,details=benchmarks(canonical);checks.update(more)
    result=dict(assertion_tested='Post-recombination corrected NR two-fluid transfer ratios and exact unchanged-FRW BBN criterion',
                model='gamma=0, flat gate linear endpoint, smooth radiation background, pressureless baryons',
                parameters_source='KD1 canonical and alt recorded settings; no parameter fit',
                approximation='leading xbar<<1 and k/a>>H; radiation perturbations and recombination transfer absent',
                cosmologies=allres,BBN=bbns,checks=checks,check_details=details,
                all_checks_pass=all(checks.values()))
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(all_checks_pass=result['all_checks_pass'],checks=len(checks),
                         halfpower_k_z3={k:v['halfpower_k_bracket_z3'] for k,v in allres.items()},
                         BBN=bbns),indent=2))
    if not result['all_checks_pass']: raise SystemExit(1)


if __name__=='__main__': main()
