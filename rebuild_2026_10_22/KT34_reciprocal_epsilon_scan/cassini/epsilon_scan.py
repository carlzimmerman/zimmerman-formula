#!/usr/bin/env python3
"""Scan only the common Gaussian sigma; import the corrected KT33 operator intact."""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import numpy as np
from scipy.optimize import brentq, minimize_scalar

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT/'rebuild_2026_10_22/KT33_reciprocal_filter/cassini/cassini_v2.py'
spec = importlib.util.spec_from_file_location('kt33_cassini_v2', SOURCE)
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)


def evaluate(footing, epsilon, nr, nm, rmin=1e-8, rmax=1e6):
    a0 = model.A0[footing]
    out = model.physical(model.quadrupole(model.GEXT/a0, epsilon, epsilon,
                          nr=nr, nm=nm, rmin=rmin, rmax=rmax), a0)
    out['epsilon'] = float(epsilon)
    return out


def asymptotic_coefficient(footing):
    eta = model.GEXT/model.A0[footing]
    return -1/(45*math.sqrt(math.pi)*eta*math.sqrt(.25+1/eta))


def crossing_brackets(rows, key, level):
    return [[a['epsilon'], b['epsilon']] for a, b in zip(rows, rows[1:])
            if (a[key]-level)*(b[key]-level) < 0]


def sweep(nr, nm):
    widths = np.unique(np.r_[0., 1e-6, 1e-5, np.logspace(-4, 1, 301),
                             np.linspace(.35,.85,101), .5, 100., 1000.])
    archive = json.loads((SOURCE.parent/'run_002/results.json').read_text())
    out = {'mode':'sweep', 'operator':'N rho + S Phi_ph[S rho]',
           'varied_parameter':'sigma_source=sigma_outer=epsilon in units rM',
           'constants':{'a0':model.A0,'GM':model.GM,'GEXT':model.GEXT,'ceiling':model.CEILING},
           'footings':{}, 'checks':{}}
    for foot in model.A0:
        rows = [evaluate(foot,float(e),nr,nm) for e in widths]
        ratios = np.array([r['x_ceiling'] for r in rows])
        extrema = [[rows[i-1]['epsilon'],rows[i]['epsilon'],rows[i+1]['epsilon']]
                   for i in range(1,len(rows)-1)
                   if (ratios[i]-ratios[i-1])*(ratios[i+1]-ratios[i]) < 0]
        baseline = next(r for r in rows if r['epsilon']==.5)
        old = archive['footings'][foot]['arms']['reciprocal']['angular_refinement']
        out['checks'][foot+'|epsilon_half_reproduction'] = {
            'relative_shift':baseline['q_hessian_signed']/old['q_hessian_signed']-1,
            'passed':abs(baseline['q_hessian_signed']/old['q_hessian_signed']-1)<1e-8}
        out['footings'][foot] = {'rows':rows,
            'ceiling_brackets':crossing_brackets(rows,'x_ceiling',1.),
            'sign_brackets':crossing_brackets(rows,'q_hessian_signed',0.),
            'sampled_extremum_brackets':extrema,
            'positive_q_samples':sum(r['q_hessian_signed']>0 for r in rows),
            'large_width_coefficient_q_epsilon_cubed':asymptotic_coefficient(foot),
            'large_width_controls':[{ 'epsilon':r['epsilon'],
                'q_times_epsilon_cubed':r['q_hessian_signed']*r['epsilon']**3,
                'relative_to_asymptotic':r['q_hessian_signed']*r['epsilon']**3/asymptotic_coefficient(foot)-1}
                for r in rows if r['epsilon']>=10]}
        print(foot, 'samples',len(rows),'ceiling_brackets',out['footings'][foot]['ceiling_brackets'],
              'sign_brackets',out['footings'][foot]['sign_brackets'],
              'extrema_count',len(extrema), 'epsilon_half_ratio',baseline['x_ceiling'],flush=True)
    out['all_checks_pass'] = all(x['passed'] for x in out['checks'].values())
    return out


def refine(scan_path):
    sweep_output = json.loads(scan_path.read_text())
    out = {'mode':'refine','source_sweep':str(scan_path),'footings':{},'checks':{}}
    presets = {'root':dict(nr=16000,nm=240),
               'high':dict(nr=40000,nm=800),
               'expanded':dict(nr=60000,nm=1000,rmin=1e-10,rmax=1e7)}
    for foot, scanned in sweep_output['footings'].items():
        found = {'ceiling_roots':[], 'sign_roots':[], 'refined_extrema':[], 'controls':[]}
        for label, key, level in [('ceiling','x_ceiling',1.),('sign','q_hessian_signed',0.)]:
            for bracket in scanned[label+'_brackets']:
                epsilon = brentq(lambda e:evaluate(foot,e,**presets['root'])[key]-level,
                                 *bracket,xtol=1e-12,rtol=1e-13)
                checks = {name:evaluate(foot,epsilon,**args) for name,args in presets.items()}
                delta = 1e-6
                neighbors = [evaluate(foot,epsilon-delta,**presets['high']),
                             evaluate(foot,epsilon+delta,**presets['high'])]
                found[label+'_roots'].append({'epsilon':epsilon,'initial_bracket':bracket,
                                             'checks':checks,'neighbors':neighbors})
                print(foot,label,'root',epsilon,'high_ratio',checks['high']['x_ceiling'],
                      'density_flux',checks['expanded']['flux_density_difference'],flush=True)
                out['checks'][foot+'|'+label+'|'+str(epsilon)] = {
                    'passed':max(abs(r['q_hessian_signed']-checks['expanded']['q_hessian_signed']) for r in checks.values())<2e-7
                              and abs(checks['expanded']['flux_density_difference'])<2e-7,
                    'absolute_q_tolerance':2e-7}
        # At very small epsilon the q curve can be flat to quadrature precision.
        # Refine every detected extremum; retain the bracket and its amplitude.
        rows = scanned['rows']
        lookup = {r['epsilon']:r for r in rows}
        for lo, mid, hi in scanned['sampled_extremum_brackets']:
            # This optimization is a local numerical diagnostic, not a proof.
            is_max = lookup[mid]['x_ceiling']>lookup[lo]['x_ceiling']
            opt = minimize_scalar(lambda e:(-1 if is_max else 1)*evaluate(foot,e,8000,200)['x_ceiling'],
                                  bounds=(lo,hi),method='bounded',options={'xatol':1e-8,'maxiter':80})
            samples = [evaluate(foot,e,16000,400) for e in [lo,float(opt.x),hi]]
            found['refined_extrema'].append({'bracket':[lo,mid,hi],'type':'max' if is_max else 'min',
                                            'optimizer_success':bool(opt.success),'samples':samples})
        for e in [0.,1e-6,1e-4,.01,.1,.2,.25,.3,.5,1.,10.,100.]:
            found['controls'].append(evaluate(foot,e,**presets['high']))
        out['footings'][foot]=found
    out['all_checks_pass']=all(x['passed'] for x in out['checks'].values())
    return out


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--mode',choices=['sweep','refine'],required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--scan',type=Path)
    p.add_argument('--nr',type=int,default=6000)
    p.add_argument('--nm',type=int,default=120)
    args=p.parse_args()
    out=sweep(args.nr,args.nm) if args.mode=='sweep' else refine(args.scan)
    out['interpretation']='Finite deterministic numerical scan, conditional on quadrature; no global no-island proof.'
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    if not out['all_checks_pass']:
        raise SystemExit(1)


if __name__=='__main__':
    main()
