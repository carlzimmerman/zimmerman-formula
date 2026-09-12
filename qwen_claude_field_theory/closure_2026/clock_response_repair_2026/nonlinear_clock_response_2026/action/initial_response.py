#!/usr/bin/env python3
"""Solve generated mean/2k initial constraints of the unchanged action.

Physical initial jets Kx,Ky,Q are used. Setting dummy N=1,b=0 assigns the
coordinate velocities representing those jets; it does not solve lapse
preservation or predict the subsequent time evolution.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import sys

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import adm_action as adm

UNKNOWN_ORDER = ('mean_K2','mean_deltaQ2','z2_cos2','Kx2_cos2','Ky2_cos2')


def clock_constraint(f,bg,exact=False):
    """Full unitary clock equation, evaluated exactly or through order two.

    E_tau=P_tau-V_tau-W K+2 W_Y Kx Y
          +2 Q[W_Y D²chi+W_YY chi^x partial_x Y].
    No clock-gradient term is omitted: normal-gradient/acceleration terms
    cancel in the divergence of the clock current on the unitary slice.
    """
    g = adm.geometry(f,bg)
    if exact:
        model = adm.sourced_snapshot()[0]
        j = model.jets(0.,g['X'],g['Y'])
        Pt,W,WY,WYY = (j[key] for key in ('P_t','W','W_Y','W_YY'))
    else:
        dX,Y = g['X']-bg['q']**2,g['Y']
        Pt = bg['Pt']+bg['PXt']*dX+bg['PXXt']*dX**2/2
        W = bg['W']+bg['WY']*Y+bg['WYY']*Y**2/2
        WY,WYY = bg['WY']+bg['WYY']*Y,bg['WYY']
    return (Pt-bg['Vt']-W*g['K']+2*WY*g['Kx']*g['Y']
            +2*g['Q']*(WY*g['lap']+WYY*g['gradY']))


@lru_cache(maxsize=1)
def seed_data():
    sys.path.insert(0,str(adm.BASE/'cosmological_bridge_2026'))
    from transfer_evolve import Background,mode_system
    background = Background(.01)
    v = background.at(0.)[0]
    A,_,nrow,zrow,brow,Jrow = mode_system(v,3.)
    u = np.zeros(6); u[0] = 1.; u[1] = (v['H']-A[0,0])/A[0,1]
    n,b = float(nrow@u),float(brow@u)
    zd = v['H']*n-float(Jrow@u)/(2*v['M2'])
    physical = dict(z1=float(zrow@u),sigma1=1.,deltaQ1=float(u[1]),
                    Kx1=zd-3*b-v['H']*n,Ky1=zd-v['H']*n)
    ref = background.model.background(0.)
    jets = background.model.jets(0.,v['q']**2,0.)
    den = ref['U']-2*ref['d']*v['q']**2
    v = dict(v,WYY=jets['W_YY'],PXXXX=48*ref['U']*ref['d']**4/den**4)
    return v,physical


def canonical_fields(response,points=512):
    """Physical free choices: e=0 spatially, sigma2=Q2k=matter2=0,
    mean z2=0 and equal mean Kx2=Ky2. Mean Q2 is solved, not suppressed.
    """
    _,p = seed_data()
    meanK,meanQ,z2,kx2,ky2 = response
    k = 3.
    phase = 2*np.pi*np.arange(points)/points
    c,sn,c2,sn2 = np.cos(phase),np.sin(phase),np.cos(2*phase),np.sin(2*phase)
    zero = np.zeros(points)
    f = {key:adm.Jet([zero,zero,zero]) for names in adm.FIELD_JETS.values() for key in names}
    def put(name,first,second=zero): f[name] = adm.Jet([zero,first,second])
    put('z',p['z1']*c,z2*c2)
    put('zx',-k*p['z1']*sn,-2*k*z2*sn2)
    put('zxx',-k*k*p['z1']*c,-4*k*k*z2*c2)
    put('zd',(p['Kx1']+2*p['Ky1'])*c/3,meanK+(kx2+2*ky2)*c2/3)
    put('zdx',-k*(p['Kx1']+2*p['Ky1'])*sn/3,-2*k*(kx2+2*ky2)*sn2/3)
    put('ed',(p['Kx1']-p['Ky1'])*c/3,(kx2-ky2)*c2/3)
    put('edx',-k*(p['Kx1']-p['Ky1'])*sn/3,-2*k*(kx2-ky2)*sn2/3)
    put('sigma',p['sigma1']*c)
    put('sx',-k*p['sigma1']*sn)
    put('sxx',-k*k*p['sigma1']*c)
    put('sd',p['deltaQ1']*c,meanQ+zero)
    put('sdx',-k*p['deltaQ1']*sn)
    return f,phase


def residual_series(response):
    bg,_ = seed_data()
    f,phase = canonical_fields(response)
    out = adm.constraints(f,bg)
    out['clock'] = clock_constraint(f,bg)
    return out,phase


def five_projections(residual,phase,order=2):
    n,b,c = (residual[name].c[order] for name in ('lapse','shift','clock'))
    return np.array([np.mean(n),np.mean(c),2*np.mean(n*np.cos(2*phase)),
                     2*np.mean(b*np.sin(2*phase)),2*np.mean(c*np.cos(2*phase))])


def exact_residual(response,epsilon):
    bg,_ = seed_data()
    fields,_ = canonical_fields(response)
    f = {key:sum(epsilon**i*coefficient for i,coefficient in enumerate(value.c))
         for key,value in fields.items()}
    exact = adm.sourced_snapshot()[4]
    out = adm.constraints(f,bg,exact)
    out['clock'] = clock_constraint(f,bg,exact=True)
    return out


@lru_cache(maxsize=1)
def run():
    bg,physical = seed_data()
    zero = np.zeros(5)
    initial,phase = residual_series(zero)
    source = five_projections(initial,phase)
    matrix = np.column_stack([five_projections(residual_series(row)[0],phase)-source
                              for row in np.eye(5)])
    response = np.linalg.solve(matrix,-source)
    final,_ = residual_series(response)
    linear_error = max(float(np.max(abs(value.c[1]))) for value in final.values())
    before = max(float(np.max(abs(value.c[2]))) for value in initial.values())
    after = max(float(np.max(abs(value.c[2]))) for value in final.values())
    baseline = exact_residual(response,0.)
    rows = []
    for eps in (.002,.001,.0005):
        positive,negative = exact_residual(response,eps),exact_residual(response,-eps)
        full = {name:float(np.max(abs(positive[name]-baseline[name]))) for name in positive}
        even = {name:float(np.max(abs((positive[name]+negative[name])/2-baseline[name])))
                for name in positive}
        rows.append(dict(epsilon=eps,full_residual=full,even_residual=even,
                         full_max=max(full.values()),even_max=max(even.values())))
    full_orders = [float(np.log2(a['full_max']/b['full_max'])) for a,b in zip(rows,rows[1:])]
    even_orders = [float(np.log2(a['even_max']/b['even_max'])) for a,b in zip(rows,rows[1:])]
    full_error = max(abs(order-3) for order in full_orders)
    even_error = max(abs(order-4) for order in even_orders)
    assert linear_error < 1e-11 and after < 1e-10
    assert full_error < .15 and even_error < .15
    assert abs(response[1]) > 1e-4
    return dict(status='second_order_initial_constraints_solved_in_stated_family',
                response=dict(zip(UNKNOWN_ORDER,map(float,response))),
                physical_first_order=physical,
                source_projection_order=['mean_lapse','mean_clock','cos2_lapse','sin2_shift','cos2_clock'],
                source_projections=source.tolist(),response_matrix=matrix.tolist(),
                matrix_condition=float(np.linalg.cond(matrix)),matrix_determinant=float(np.linalg.det(matrix)),
                linear_constraint_max=linear_error,
                quadratic_constraint_max_before_response=before,
                quadratic_constraint_max_after_response=after,
                projection_residual=(matrix@response+source).tolist(),
                exact_nonlinear_controls=rows,full_residual_orders=full_orders,
                even_residual_orders=even_orders,exact_full_residual_order_min_error=full_error,
                exact_even_residual_order_min_error=even_error,
                background=dict(Q=bg['q'],sbar=bg['sbar'],H=bg['H'],gamma=bg['gamma'],k=3.),
                fixed_free_data=['mean z2=0','mean Kx2=mean Ky2','spatial e2=0',
                                 'sigma2=0','Q2 at 2k=0','all matter field/rate/density order-two perturbations=0'],
                conventions='Physical Kx,Ky,Q prescribed as epsilon series; dummy N=1,b=0 represents these physical initial jets. Mean Q2 is solved. No factorials.',
                non_claims=['Lapse preservation has not been imposed at nonlinear order.',
                            'This does not integrate a nonlinear time evolution.',
                            'Third-order constraints, scalar/metric evolution, and constraint-reduced S4 remain open.',
                            'Numerical solution and residual refinement are conditional float64 evidence, not an interval certificate.'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--result-file',type=Path,required=True)
    args = parser.parse_args()
    result = run()
    args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
