"""Absolute-window analysis of declared runs; no model evolution or fitting."""
import argparse
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def combine_histories(runs):
    """Keep the last record at duplicated restart times; retain real sample times."""
    records = {}
    for run in runs:
        for row in run['time_history']:
            if 'enclosed_5pct_mean_density' in row:
                records[float(row['t'])] = row
    return [records[t] for t in sorted(records)]


def absolute_window(history, start, end):
    rows = [row for row in history if start <= row['t'] <= end]
    if len(rows) < 2:
        raise ValueError('requested absolute window has fewer than two real samples')
    return rows


def metrics(rows):
    times = np.array([r['t'] for r in rows])
    density = np.array([r['enclosed_5pct_mean_density'] for r in rows])
    slope = np.polyfit(times-times[0], density, 1)[0]
    return dict(actual_start=float(times[0]), actual_end=float(times[-1]), samples=len(rows),
        density5_relative_span=float(np.ptp(density)/density.mean()),
        density5_relative_slope_over_window=float(slope*(times[-1]-times[0])/density.mean()),
        maximum_kinetic_over_binding=max(r['kinetic_over_abs_gravitational'] for r in rows),
        maximum_hydrostatic_residual=max(r['hydrostatic_residual_rms_over_gravity'] for r in rows),
        minimum_core5_K=min(r['prefix_5pct_min_K'] for r in rows),
        minimum_core5_guard_K=min(r['K_guard_5pct'] for r in rows),
        minimum_all_material_K=min(r['min_all_K'] for r in rows),
        maximum_luminosity=max(r['max_abs_luminosity'] for r in rows))


def passed_settling(row):
    return (row['maximum_kinetic_over_binding'] < 1e-3
            and row['density5_relative_span'] < .02
            and abs(row['density5_relative_slope_over_window']) < .02
            and row['maximum_hydrostatic_residual'] < .02)


def load(name):
    return json.loads((HERE/name/'result.json').read_text())


def energy_bound(runs):
    reference = abs(runs[0]['initial']['total'])
    return sum(r['max_relative_energy_error']*abs(r['initial']['total'])/reference for r in runs)


def analyze():
    prediction = load('isentropic_prediction')['endpoint']
    floors = []
    for n in (32, 64, 128, 256):
        run = load(f'floor_n{n}_t32')
        if run['status'] != 'completed' or run['t_reached'] != 32:
            raise ValueError('a resolution run did not reach its declared endpoint')
        history = combine_histories([run])
        late = metrics(absolute_window(history, 24, 32))
        ancestors = [load(f'conv_n{n}_t8'), run] if n < 128 else [run]
        f = run['final']
        row = dict(N=n, status=run['status'], requested_late_window=[24,32], late=late,
            central_cell_K=f['K_by_cell'][0], central5_minimum_K=f['prefix_5pct_min_K'],
            density1_mean=f['enclosed_1pct_mean_density'], density5_mean=f['enclosed_5pct_mean_density'],
            central_cell_density=f['rho_by_cell'][0], outer_radius=f['outer_radius'],
            half_mass_radius=f['half_mass_radius'],
            minimum_all_K_from_t8=min(r['min_all_K'] for r in history if r['t'] >= 8),
            minimum_core5_K_from_t8=min(r['prefix_5pct_min_K'] for r in history if r['t'] >= 8),
            original_energy_error_bound=energy_bound(ancestors),
            minimum_sampled_entropy_increment=float(np.diff([r['total_entropy'] for r in history]).min()),
            prediction_relative_K_error=(f['K_by_cell'][0]/prediction['K']-1),
            settling_pass=passed_settling(late))
        floors.append(row)
    stability = []
    cases = dict(unperturbed=['steady_n64_t64'],
        compression=['compress_n64_t64','compress_n64_finish'],
        expansion=['expand_n64_t64','expand_n64_finish','bdf_switch_check','bdf_expand_t64'],
        entropy_mode=['entropy_mode_n64_t64'])
    for label,names in cases.items():
        runs = [load(name) for name in names]
        if runs[-1]['status'] != 'completed' or runs[-1]['t_reached'] != 64:
            raise ValueError('a stability chain is incomplete')
        late = metrics(absolute_window(combine_histories(runs),56,64))
        stability.append(dict(case=label, lineage=names,
            attempt_statuses=[r['status'] for r in runs], methods=[r['method'] for r in runs],
            total_recorded_runtime=sum(r['elapsed_seconds'] for r in runs), late=late,
            final_density5=runs[-1]['final']['enclosed_5pct_mean_density'],
            final_core5_min_K=runs[-1]['final']['prefix_5pct_min_K'],
            energy_error_bound_from_prepared_state=energy_bound(runs),
            preparation=runs[0].get('stability_preparation',runs[0].get('preparation')),
            settling_pass=passed_settling(late)))
    tight = load('tight_n256_finish')
    ordinary = load('floor_n256_t32')
    time_check = {}
    for key in ('K','rho','r'):
        a=np.asarray(tight['final_profile'][key]);b=np.asarray(ordinary['final_profile'][key])
        time_check[key+'_maximum_relative_difference']=float(np.max(np.abs(a/b-1)))
    return dict(schema='X48-entropy-transport-analysis-v1', resolution=floors,
        stationary_prediction=prediction, stability=stability, tighter_time_check=time_check,
        finite_checks=dict(all_four_settle=all(r['settling_pass'] for r in floors),
            all_stability_chains_settle=all(r['settling_pass'] for r in stability),
            original_energy_bounds_below_1e_6=all(r['original_energy_error_bound']<1e-6 for r in floors),
            positive_all_material_K_after_t8=all(r['minimum_all_K_from_t8']>0 for r in floors),
            positive_central_K_after_t8=all(r['minimum_core5_K_from_t8']>0 for r in floors),
            tighter_time_check=all(value<1e-6 for value in time_check.values())),
        non_claims=['Finite N=32..256 and t<=64 do not prove a continuum or infinite-time floor',
            'Stationary prediction is conditional on the regular isentropic limiting branch',
            'No cosmological forest realization, nonradial 3D stability or baryonic disc test',
            'Absolute windows retain actual sample times; no invented t24 or t56 observations'])


def figure(output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    prediction=load('isentropic_prediction')['endpoint']['K']
    passive=combine_histories([load('n32_D01_t4'),load('n32_D01_t16')])
    gated=combine_histories([load('floor_n256_t32')])
    fig,axes=plt.subplots(1,3,figsize=(13.8,4.15),constrained_layout=True)
    for rows,label,color in [(passive,'Persistent heat transport, N=32','#b35b38'),
                             (gated,'Instability-gated transport, N=256','#177b9b')]:
        t=[r['t'] for r in rows]
        axes[0].plot(t,[r['inner_5pct_min_K'] for r in rows],label=label,color=color,lw=2)
        axes[1].plot(t,[r['enclosed_5pct_mean_density'] for r in rows],color=color,lw=2)
    axes[0].axhline(prediction,color='#333333',ls='--',lw=1,label='Energy-selected equilibrium')
    axes[0].set(xlabel='Time',ylabel=r'Inner 5% minimum $K/K_\star$',title='Central entropy survives')
    axes[1].set(xlabel='Time',ylabel=r'Inner 5% mean $\rho/\rho_q$',title='Contraction stops')
    axes[0].set_xlim(0,32); axes[1].set_xlim(0,32)
    values=[load(f'floor_n{n}_t32')['final']['K_by_cell'][0] for n in (32,64,128,256)]
    axes[2].plot([32,64,128,256],values,'o-',color='#177b9b',lw=1.8)
    axes[2].axhline(prediction,color='#333333',ls='--',lw=1)
    axes[2].set_xscale('log',base=2);axes[2].set_xticks([32,64,128,256],['32','64','128','256'])
    axes[2].set(xlabel='Number of shells',ylabel=r'Central cell $K/K_\star$ at $t=32$',title='Refinement approaches the prediction')
    axes[2].ticklabel_format(axis='y',style='plain',useOffset=False)
    for ax in axes:
        ax.grid(alpha=.18);ax.spines[['top','right']].set_visible(False)
    axes[0].legend(loc='upper right',fontsize=7.3)
    fig.savefig(output,dpi=180)
    plt.close(fig)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--figure',type=Path)
    args=parser.parse_args()
    report=analyze()
    args.output.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    if args.figure:
        figure(args.figure)
    print(json.dumps(report['finite_checks']))
    return 0 if all(report['finite_checks'].values()) else 1


if __name__=='__main__':
    raise SystemExit(main())
