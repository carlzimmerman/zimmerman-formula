"""Transform pinned thermal-root output into entropy-corrected energy controls."""
import sys, json, math, time, resource
from pathlib import Path
from statistics import mean
HERE=Path(__file__).resolve().parent
def main(out):
    start=time.monotonic()
    prior=json.loads((HERE/'run_release_001/result.json').read_text())
    static=json.loads((HERE.parent/'thermal/run_static_001/result.json').read_text())
    c=prior['constants'];theta=c['TD_times_a_initial_GeV'];km=c['Kmax_GeV4']
    gd0=c['g_s_hidden_ultrarelativistic'];zeta3=1.2020569031595942
    n0=3*zeta3/(2*math.pi**2)*theta**3
    can=json.loads((HERE.parent/'canonical/run_highprecision/result.json').read_text())
    pro=json.loads((HERE.parent/'protected/run_export_002/result.json').read_text())
    masses={'canonical':can['candidate']['gauginos_GeV']['U1'],'protected':pro['preferred_row']['photino_GeV']}
    rows=[]
    for point in static['points']:
        spin=next(r for r in point['spins'] if r['name']=='origin')
        near=point['origin_branch'][0]
        false=next(r for r in near['roots'] if r['minimum'])
        # Thermodynamic derivative at the first just-above-spinodal false
        # minimum is a nearby entropy control, not an exactly solved spinodal.
        gs=45/(2*math.pi**2)*false['entropy_thermal_mu3']/near['TD_over_mu']**3
        factor=(gd0/gs)**(1/3)
        a=theta/spin['TD_GeV']
        q=spin['zero_T_excess_GeV4']*a**4/km
        frac=n0*masses[point['kind']]/c['rhochi_GeV4']
        rows.append(dict(kind=point['kind'],spinodal_TD_GeV=spin['TD_GeV'],spinodal_TD_over_mu=spin['TD_over_mu'],
                         spinodal_false_X_over_mu=spin['X_over_mu'],
                         DeltaV_at_spin_GeV4=spin['zero_T_excess_GeV4'],
                         K_release_over_Kmax_collisionless_label=q,
                         near_spinodal_hidden_g_s=gs,
                         near_spinodal_TD_times_a_heating_factor=factor,
                         K_release_over_Kmax_with_nearby_equilibrium_entropy=q*factor**4,
                         release_to_SM_energy_ratio_collisionless=spin['zero_T_excess_over_rhoSM'],
                         release_to_SM_energy_ratio_entropy_corrected=spin['zero_T_excess_over_rhoSM']*factor**4,
                         relativistic_decoupling_photino_number_today_GeV3=n0,
                         relativistic_decoupling_photino_DM_fraction=frac,
                         required_number_enhancement_over_early_relativistic_decoupling=1/frac))
    max_heat=(gd0/2)**(1/3)
    checks=dict(spins_pass_energy_even_max_photon_entropy=all(r['K_release_over_Kmax_collisionless_label']*max_heat**4<1 for r in rows),
                near_spin_gs_physical=all(2<r['near_spinodal_hidden_g_s']<gd0 for r in rows))
    result=dict(claim_id='TH07_SPINODAL_ENTROPY_RELEASE_CONTROL',checks=checks,rows=rows,
                maximal_equilibrium_heating_to_two_photon_degrees=max_heat,
                initial_thermal_hidden_K_GeV4=math.pi**2/30*gd0*theta**4,
                initial_thermal_hidden_K_over_Kmax=math.pi**2/30*gd0*theta**4/km,
                scope='Pinned static-root arithmetic and nearby ideal-gas entropy control; not an equilibrated real-time transition or relic calculation. Decoupling diagnostic assumes two-helicity photino initially in FD equilibrium, conserved comoving number and no dark entropy injection into it.',
                runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
