#!/usr/bin/env python3
"""CLS1 main: known answers, necessary windows in mu_K per X-COP cluster, S2 numbers, construction, label.

Usage: python3 -I cls1.py OUT.json [MU1|MU2|MU3]   (a mutation flag writes a MUTATE run; never graded)
See FROZEN_CRITERIA.md. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cls1_lib as L  # noqa: E402

MU_REC = {'TK1 floor': (1e-3, 1e-3), 'groups lo': (0.912, 0.759), 'groups hi': (1.514, 1.380),
          'KiDS cap': (1.00, 0.765), 'MK1 X-COP closest miss': (1.35, 1.26), 'SPARC cap': (7.08, 5.62),
          'background line B1a': (198.25, 198.24), 'Saturn cap': (6.22e3, 6.22e3), 'Jeans line': (2.512e4, 2.512e4),
          'TK1 mu_0': (3e4, 3e4)}
FORM_B_MIN = {'canonical': 198.25, 'alt': 198.24}
LSTAR = {'canonical': 21.7e-3, 'alt': 22.9e-3}   # kpc
RHO_DE = 3*0.69*(70/1000)**2/(8*math.pi*L.G)     # Msun/kpc^3


def known_answers():
    ka = {}
    clusters = L.PRIOR['load']()
    # KA1 (DT2's checks() uses np.trapezoid, absent from this numpy; the same mean is computed here directly)
    flat = [p for cl in clusters.values() for p in cl]
    base = {f: float(np.mean([math.log10(p['M']/(L.law(L.G*p['B']/p['r']**2, L.A0[f])*p['r']**2/L.G)) for p in flat]))
            for f in L.FOOTINGS}
    ka['KA1'] = dict(n_points=len(flat), baseline=base, expected=[0.46749899183464316, 0.4345230963151764],
                     pass_=len(flat) == 35 and abs(base['canonical']-0.46749899183464316) < 1e-6 and
                     abs(base['alt']-0.4345230963151764) < 1e-6)
    rows = [dict(p, Blo=p['B'], Bhi=p['B']) for p in clusters['A2029']]
    b = L.bounds(rows, L.A0['canonical'], 2)
    o = next(t for t in b['triples'] if t['idx'] == [0, 2, 3])
    q_up = o['UP_u']/L.RHO_BG
    ka['KA2'] = dict(Dmin_c2=o['Dmin_c2'], DT3=1.49168e-5, q_upper=q_up, DT3_q=64918.38,
                     rel=[o['Dmin_c2']/1.49168e-5-1, q_up/64918.38-1],
                     pass_=abs(o['Dmin_c2']/1.49168e-5-1) < 1e-4 and abs(q_up/64918.38-1) < 1e-4)
    # KA6: Helmholtz limit, a0 = 0, no baryons, no background: x = x0 sin(mu r)/(mu r)
    mu = 1/100.0; x0 = 1e-9; re = [50.0, 150.0, 250.0, 300.0]
    _, _, _ = None, None, None
    xs = helmholtz_x(mu, x0, re)
    ref = [x0*math.sin(mu*r)/(mu*r) for r in re]
    rel = max(abs(a-b)/x0 for a, b in zip(xs, ref))
    ka['KA6'] = dict(x=xs, ref=ref, max_abs_over_x0=rel, pass_=rel < 1e-6)
    return ka


def helmholtz_x(mu, x0, r_eval, nstep=20000):
    """Same RK4 equations as L.integrate with a0=0, no baryons, no background; returns x at r_eval."""
    a_eff = L.alpha_eff()/mu**2
    r = 1e-3; x = x0; M = 4*math.pi/3*r**3*(x/a_eff)*(1+2*x)
    out = []; h = (max(r_eval)*1.0001 - r)/nstep
    targets = sorted(r_eval); ti = 0

    def f(r, x, M):
        g = L.G*M/r**2
        return -(1+x)*g/L.C**2, 4*math.pi*r*r*(x/a_eff)*(1+2*x)
    for _ in range(nstep):
        k1 = f(r, x, M); k2 = f(r+h/2, x+h/2*k1[0], M+h/2*k1[1]); k3 = f(r+h/2, x+h/2*k2[0], M+h/2*k2[1])
        k4 = f(r+h, x+h*k3[0], M+h*k3[1])
        xn = x+h/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]); Mn = M+h/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        while ti < len(targets) and r+h >= targets[ti]:
            w = (targets[ti]-r)/h; out.append(x+w*(xn-x)); ti += 1
        r, x, M = r+h, xn, Mn
    return out


def planted(data):
    """KA4: a synthetic S1 cluster on A2029's baryons at a planted mu_K and x(1 kpc)."""
    prof = data['A2029']['prof']; rows0 = data['A2029']['rows'][:5]
    a0 = L.A0['canonical']; MU_P = 1.0; mu_p = MU_P/L.KPC_PER_MPC
    re = [p['r'] for p in rows0]
    best = None
    for x0 in np.geomspace(1e-5, 1e-3, 41):
        M, xmin, D = L.integrate(prof, a0, mu_p, np.array([x0]), re)
        if xmin[0] > 0:
            best = (x0, M[0]); break
    x0, Mp = best
    rows = [dict(x=p['x'], r=p['r'], M=float(m), E=0.025*float(m), B=p['B'], Blo=p['B'], Bhi=p['B'])
            for p, m in zip(rows0, Mp)]
    b = L.bounds(rows, a0, 2)
    ivs, _ = L.window(b['triples'])
    inw = L.in_window(ivs, MU_P)
    con = construct(prof, rows, a0, [MU_P], ns=2)
    return dict(mu_planted=MU_P, x0_planted=x0, M_nodes=Mp.tolist(), window=ivs, planted_in_window=inw,
                constructed=con['constructed'], pass_=bool(inw and con['constructed']))


def construct(prof, rows, a0, mus_mpc, ns, nx=2800):
    re = [p['r'] for p in rows]
    lo = np.array([p['M']-ns*p['E'] for p in rows]); hi = np.array([p['M']+ns*p['E'] for p in rows])
    x0 = np.geomspace(1e-14, 1.0, nx)
    best = None; hits = []
    for mmp in mus_mpc:
        M, xmin, D = L.integrate(prof, a0, mmp/L.KPC_PER_MPC, x0, re)
        ok = np.all((M >= lo) & (M <= hi), axis=1) & (xmin > 0)
        dev = np.max(np.abs(M - 0.5*(lo+hi))/(0.5*(hi-lo)), axis=1)
        dev[~(xmin > 0)] = np.inf
        dev = np.where(np.isfinite(dev), dev, np.inf)   # NaN (overflow at large x0) never counts
        k = int(np.argmin(dev))
        if best is None or dev[k] < best['max_dev_in_halfwidths']:
            best = dict(mu_mpc=mmp, x0=float(x0[k]), max_dev_in_halfwidths=float(dev[k]),
                        M_over_central=(M[k]/np.array([p['M'] for p in rows])).tolist(),
                        dust_over_Mb_outer=float(D[k, -1]/rows[-1]['B']))
        if ok.any():
            hits.append(dict(mu_mpc=mmp, x0=x0[ok].tolist()[:3], n=int(ok.sum())))
    return dict(constructed=bool(hits), hits=hits[:20], best=best)


def s2c_factor(tri, mu_mpc):
    mu = mu_mpc/L.KPC_PER_MPC; worst = None
    for o in tri:
        if not o['UP_active']: continue
        allowed = float(np.log1p(L.x_of_m(o['UP_u'], mu)) - np.log1p(L.x_of_m(o['UP_l'], mu)))
        f = o['Dmin_c2']/allowed if allowed > 0 else math.inf
        if worst is None or f > worst['factor']:
            worst = dict(idx=o['idx'], r=o['r'], required=o['Dmin_c2'], allowed=allowed, factor=f)
    return worst


def side_numbers(rows, a0, f):
    out = []
    lst = LSTAR[f]
    for q, p in enumerate(rows):
        V = 4*math.pi/3*p['r']**3
        Pi = (p['M']+2*p['E'])/V
        g = L.G*p['M']/p['r']**2
        t1 = 2*math.pi*L.G*lst**2*max(Pi, RHO_DE)/L.C**2
        t2 = 2*math.pi*L.G*lst**2*max(Pi, RHO_DE)/(p['r']*g)
        a, b = (q, q+1) if q+1 < len(rows) else (q-1, q)
        Va, Vb = 4*math.pi/3*rows[a]['r']**3, 4*math.pi/3*rows[b]['r']**3
        rhoQ = ((rows[b]['M']-rows[b]['B'])-(rows[a]['M']-rows[a]['B']))/(Vb-Va)
        y = g/a0
        ratio = (1/(1+y))*g*g/(4*math.pi*L.G*rhoQ*L.C**2) if rhoQ > 0 else math.inf
        out.append(dict(r=p['r'], blend_term1=t1, blend_term2=t2, PA_over_rhoQ=ratio))
    return out


def main():
    outp = Path(sys.argv[1]); mut = sys.argv[2] if len(sys.argv) > 2 else None
    if mut: L.MUT[mut] = True
    res = dict(mutation=mut, known_answers={}, rows={}, note=L.Adopts_nothing)
    data_h = L.load(with_hecs=True)
    data = {n: dict(d, rows=[r for r in d['rows'] if not r.get('hecs')]) for n, d in data_h.items()}
    if not mut:
        res['known_answers'] = known_answers()
        res['known_answers']['KA4'] = planted(data)
    res['hecs_info'] = {n: d['info'] for n, d in data_h.items()}
    ka5_worst = 0.0
    for f in L.FOOTINGS:
        a0 = L.A0[f]; R = res['rows'][f] = {}
        for fam, dd in (('HSE', data), ('HSE+HeCS', data_h)):
            for ns in (0, 2):
                key = f'{fam}/{ns}sigma'; R[key] = {}
                for name in L.NAMES:
                    rows = dd[name]['rows']
                    b = L.bounds(rows, a0, ns)
                    ivs, npass = L.window(b['triples'])
                    cf = [L.closed_form_edges(o) for o in b['triples']]
                    mu_hi_cf = min([c['mu_hi'] for c in cf if 'mu_hi' in c], default=math.inf)*L.KPC_PER_MPC
                    mu_lo_cf = max([c['mu_lo'] for c in cf if 'mu_lo' in c], default=0.0)*L.KPC_PER_MPC
                    e = dict(window_per_Mpc=ivs, n_grid_pass=npass, closed_form_lo_hi=[mu_lo_cf, mu_hi_cf],
                             n_UP_active=sum(o['UP_active'] for o in b['triples']),
                             n_LOW_active=sum(o['LOW_active'] for o in b['triples']),
                             record_membership={k: L.in_window(ivs, v[0 if f == 'canonical' else 1])
                                                for k, v in MU_REC.items()},
                             S2c={str(m): s2c_factor(b['triples'], m) for m in (FORM_B_MIN[f], 2.512e4)})
                    # KA5: compare edges with closed form where x small at the edge
                    if ivs and np.isfinite(mu_hi_cf) and mu_lo_cf > 0 and len(ivs) == 1:
                        lo_e, hi_e = ivs[0]
                        xs = [float(L.x_of_m(max(o['UP_u'], o['LOW_l']), lo_e/L.KPC_PER_MPC)) for o in b['triples']]
                        if max(xs) <= 1e-3:
                            d = max(abs(lo_e/mu_lo_cf-1), abs(hi_e/mu_hi_cf-1)); e['KA5_rel'] = d
                            ka5_worst = max(ka5_worst, d)
                    if not ivs and mu_lo_cf > mu_hi_cf:
                        e['empty_by'] = dict(mu_lo_cf=mu_lo_cf, mu_hi_cf=mu_hi_cf, ratio=mu_lo_cf/mu_hi_cf)
                    if not ivs:
                        # nearest approach: max over grid of min margin (scaled) is reported via the edge pair
                        e['strongest_UP'] = min((o for o in b['triples'] if o['UP_active']),
                                                key=lambda o: L.closed_form_edges(o)['mu_hi'], default=None)
                        e['strongest_LOW'] = max((o for o in b['triples'] if o['LOW_active']),
                                                 key=lambda o: L.closed_form_edges(o)['mu_lo'], default=None)
                    if ns == 2 and not mut:
                        e['side'] = side_numbers(rows, a0, f)
                    R[key][name] = e
                # common window
                com = [[1e-6, 1e8]]
                for name in L.NAMES: com = L.intersect(com, R[key][name]['window_per_Mpc'])
                R[key]['_common_window'] = com
                print(f, key, ' '.join(f"{n}:{['%.3g-%.3g' % tuple(w) for w in R[key][n]['window_per_Mpc']] or 'EMPTY'}"
                                       for n in L.NAMES), 'common', com, flush=True)
        # construction (only where a two-error HSE window is non-empty)
        R['construction'] = {}
        if not mut:
            for name in L.NAMES:
                ivs = R['HSE/2sigma'][name]['window_per_Mpc']
                if not ivs: continue
                mus = sorted(set(float(m) for a, bb in ivs for m in np.geomspace(a, bb, 24)))
                R['construction'][name] = construct(data[name]['prof'], data[name]['rows'], a0, mus, 2)
                print(f, 'construct', name, R['construction'][name]['constructed'], R['construction'][name]['best'],
                      flush=True)
    res['KA5_worst_rel'] = ka5_worst
    if not mut:
        res['known_answers']['KA5'] = dict(worst_rel=ka5_worst, pass_=ka5_worst < 1e-3)
    res['label'] = grade(res) if not mut else None
    outp.write_text(json.dumps(res, indent=1, default=float) + '\n')
    print('known answers', {k: v['pass_'] for k, v in res['known_answers'].items()})
    print('label', json.dumps(res['label'], indent=1))


def grade(res):
    lab = {}
    kas = all(v['pass_'] for v in res['known_answers'].values())
    for f in L.FOOTINGS:
        R = res['rows'][f]['HSE/2sigma']
        side = [s for n in L.NAMES for s in R[n]['side']]
        blend = max(max(s['blend_term1'], s['blend_term2']) for s in side)
        pa = max(s['PA_over_rhoQ'] for s in side)
        nonempty = [n for n in L.NAMES if R[n]['window_per_Mpc']]
        cons = res['rows'][f]['construction']
        ncons = [n for n in L.NAMES if n in cons and cons[n]['constructed']]
        common = R['_common_window']
        # form B admissible reading: mu >= 198.25
        mB = FORM_B_MIN[f]
        nonempty_B = [n for n in L.NAMES if L.intersect(R[n]['window_per_Mpc'], [[mB, 1e8]])]
        if not kas or blend > 1e-6 or pa > 1e-3:
            label = 'NO VERDICT'
        elif not nonempty:
            label = 'NO STATE'
        else:
            common_cons = None
            if len(ncons) == 7:
                sets = [set(round(h['mu_mpc'], 12) for h in cons[n]['hits']) for n in L.NAMES]
                common_cons = set.intersection(*sets)
            label = 'STATE EXISTS' if common_cons else 'STATE EXISTS-PARTIAL'
        labelB = 'NO STATE' if (kas and blend <= 1e-6 and pa <= 1e-3 and not nonempty_B) else \
            ('NO VERDICT' if not kas else 'STATE EXISTS-PARTIAL or better (see windows)')
        lab[f] = dict(label=label, n_nonempty_window=len(nonempty), nonempty=nonempty, common_window=common,
                      n_constructed=len(ncons), constructed=ncons, blend_max=blend, PA_over_rhoQ_max=pa,
                      known_answers_pass=kas, form_B_reading=labelB, nonempty_at_form_B_mu=nonempty_B)
    return lab


if __name__ == '__main__':
    main()

# Adopts nothing. kappa = 1/2 FITTED; not theory closed.
