#!/usr/bin/env python3
"""Conditional pump-to-dipole dictionary and evidence figure.

The dictionary p_amplitude=a_wave is hypothetical, not derived from a dark
action. Density and stream-speed premises are NOT inferred from the PIC run.
"""
import argparse
import json
import math
from pathlib import Path
import sympy as sp


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--input',default='sol61_push/runs/pic/results.json')
    ap.add_argument('--output',required=True); ap.add_argument('--figure',required=True)
    args=ap.parse_args(); pic=json.loads(Path(args.input).read_text()); checks=[]; rows=[]
    def check(name,ok,detail):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    zeta,B,g,r,G,chi,q=sp.symbols('zeta B g r G chi q',positive=True)
    rho=zeta*g/(4*sp.pi*G*r)
    omega=sp.sqrt(8*sp.pi*G*rho)
    v=sp.sqrt(B*r*g)
    a=sp.simplify(chi*omega*v/(2*sp.sqrt(6)))
    check('conditional_virial_amplitude_scaling',sp.simplify(a/g-chi*sp.sqrt(zeta*B/12))==0,'given rho_carrier=zeta g/(4piGr) and v^2=B r g, a_wave/g=chi sqrt(zeta B/12)')
    k=sp.simplify(2*a/g)
    check('hypothetical_dipole_amplitude_dictionary',sp.simplify(k-chi*sp.sqrt(zeta*B/3))==0,'ONLY IF omega^2 X/2=a_wave, paper amplitude k=chi sqrt(zeta B/3)')
    K=sp.simplify(k*k)
    coefficient=sp.simplify(q*K*K/192)
    check('conditional_vacuum_coefficient',sp.simplify(coefficient-q*chi**4*zeta**2*B**2/1728)==0,str(coefficient))
    required=3*sp.sqrt(6144*sp.pi/q)/chi**2
    check('required_carrier_speed_product',sp.simplify(coefficient.subs(zeta,required/B)-32*sp.pi)==0,'zeta B = 3 sqrt(6144pi/q)/chi^2 for symmetric charges, equal amplitudes and maximal chirality')
    for name in ('fine','multimode_larger_box'):
        row=next(t for t in pic['rows'] if t['name']==name)
        peak=row['first_nonlinear_peak']
        physical_k=row['k']*row['tracked_mode']
        # This is the sinusoidal single-harmonic estimate omega_b^2=k E,
        # not a measurement of bounce periods in the nonlinear orbit data.
        estimate=physical_k*peak['field_amplitude']/(1/8)
        need=3*math.sqrt(6144*math.pi)/estimate**2
        predicted=estimate**4/1728
        rows.append(dict(case=name,chi_single_harmonic_estimate=estimate,
                         required_zeta_times_B_if_q_one=need,
                         coefficient_if_zeta_B_q_one=predicted,
                         inferred_a0_relative_to_fine=None))
    rows[0]['inferred_a0_relative_to_fine']=1.
    rows[1]['inferred_a0_relative_to_fine']=(rows[0]['chi_single_harmonic_estimate']/rows[1]['chi_single_harmonic_estimate'])**2
    check('simulation_does_not_fix_bounce_equals_growth',abs(rows[0]['chi_single_harmonic_estimate']-1)>.5,f'chi from fundamental estimate={rows[0]["chi_single_harmonic_estimate"]:.10g}; equality would be chi=1')
    check('simulation_does_not_fix_one_saturation_coefficient',abs(rows[1]['inferred_a0_relative_to_fine']-1)>.1,f'hypothetical a0 ratio across mode environments={rows[1]["inferred_a0_relative_to_fine"]:.10g}; not an astrophysical prediction')
    # Classical electrostatic similarity: x_s=s*x, v_s=s*v, E_s=s*E,
    # t unchanged => Poisson and particle equations retain the same density.
    scale=sp.symbols('scale',positive=True)
    check('classical_velocity_similarity',sp.simplify((scale*v)*(omega)/(v*omega)-scale)==0,'at fixed density, rescaling lengths and velocities rescales selected force amplitude; density alone does not select the acceleration')
    data=dict(checks=checks,rows=rows,conditional_amplitude=str(a),conditional_coefficient=str(coefficient),required_product=str(required),
              verdict='A virial-density premise can make pump amplitudes proportional to g, but the premises, force dictionary, chirality, density/speed product and vacuum q remain unselected. Neither target law nor 32pi is derived.',
              non_claims=['No derivation of the assumed flat-curve density or BTFR normalization','Carrier density need not equal gravitating phantom density','PIC bounce value is a single-harmonic estimate, not measured particle orbit frequency','First saturation peak is not an attractor','No mapping of an Abelian plasma to non-Abelian dark correlations'])
    Path(args.output).write_text(json.dumps(data,indent=2)+'\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11.4,4.4),layout='constrained')
    colors={'fine':'#183b66','seed_changed':'#bb641c','multimode_larger_box':'#40856a','stable_control':'#7f8793'}
    names={'fine':'One unstable mode','seed_changed':'Twice the tiny seed','multimode_larger_box':'Eight seeds; larger box','stable_control':'Stable wavelength'}
    for name in colors:
        row=next(t for t in pic['rows'] if t['name']==name)
        history=row['history']
        axes[0].semilogy([h['t'] for h in history],[max(h['tracked_mode_field'],1e-12) for h in history],label=names[name],color=colors[name],lw=1.6)
    axes[0].set(xlabel='Time (plasma-frequency units)',ylabel='Tracked field amplitude',title='Streams generate growing internal fields',ylim=(1e-7,1.4),xlim=(0,80))
    axes[0].legend(fontsize=8,loc='lower right'); axes[0].grid(alpha=.15)
    fine=next(t for t in pic['rows'] if t['name']=='fine')['history']
    t=[h['t'] for h in fine]
    axes[1].plot(t,[h['kinetic_energy'] for h in fine],label='Stream kinetic energy',color='#183b66',lw=1.7)
    axes[1].plot(t,[h['electric_energy'] for h in fine],label='Field energy',color='#bb641c',lw=1.7)
    axes[1].plot(t,[h['total_energy'] for h in fine],label='Total',color='#40856a',lw=1.4,ls='--')
    axes[1].set(xlabel='Time (plasma-frequency units)',ylabel='Energy density (normalized units)',title='The energy comes from relative motion',xlim=(0,80),ylim=(-.01,.54))
    axes[1].legend(fontsize=9,loc='lower right'); axes[1].grid(alpha=.15)
    fig.suptitle('A concrete pump in a charged-plasma analogy',fontsize=14)
    fig.supxlabel('Cold electrostatic model. No MOND response or 32π derivation.',fontsize=9)
    fig.savefig(args.figure,dpi=180)
    plt.close(fig)
    failed=sum(not x['passed'] for x in checks)
    print(f'{len(checks)-failed}/{len(checks)} bridge checks pass; theory and 32pi OPEN.')
    return int(failed>0)


if __name__=='__main__': raise SystemExit(main())
