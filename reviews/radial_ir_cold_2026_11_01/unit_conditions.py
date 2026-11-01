"""Necessary cold-state unit/density/lifetime tests, not cosmological selection."""
import sys
sys.dont_write_bytecode=True
import argparse,json,math,resource,time
from pathlib import Path
import mpmath as mp
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[1]
sys.path.insert(0,str(ROOT/'reviews/three_priorities_2026_11_01/spectrum_pressure'))
from pressure_scan import cw


def main(out):
    start=time.monotonic();mp.mp.dps=65
    h_Js=6.62607015e-34;c=299792458.;G=6.67430e-11;GeV_J=1.602176634e-10
    hbar_Js=h_Js/(2*math.pi);hbar=hbar_Js/GeV_J;hbarc_cm=hbar*c*100
    Mbar=math.sqrt(hbar_Js*c**5/(8*math.pi*G))/GeV_J
    Mpc_m=3.0856775814913673e22;H0_s=67400/Mpc_m;H0=H0_s*hbar
    rhoDE=.685*3*Mbar*Mbar*H0*H0;muDE=(31*rhoDE)**.25
    age_s=13.8e9*365.25*86400
    zmin=mp.mpf('7.367143721278508');mass_controls=[]
    for estr in ['.01','.03']:
        e=mp.mpf(estr);x=zmin/mp.sqrt(31*e);v=mp.sqrt(31)*x
        U=lambda s:cw(x*mp.exp(s),e,e,mp.sqrt(mp.mpf(29)/200)*e)
        us=mp.diff(U,0);uss=mp.diff(U,0,2);m=mp.sqrt(uss/(2*v*v))
        mass_controls.append(dict(e=float(e),mhat=float(m),vhat=float(v),stationarity_over_curvature=float(abs(us/uss)),mass_coefficient=float(m/e**mp.mpf('1.5'))))
    cm=mass_controls[0]['mass_coefficient'];z=float(zmin)
    gm=json.loads((BASE/'gapless_charge/run_003/result.json').read_text())
    assert all(gm['checks'].values())
    ref=next(d for d in gm['cases'] if d['e']==.01 and d['r']==1.)
    cl=abs(ref['groups']['U1']['signed_mass'])/.01**2.5
    es=[.03,.01,.003,.001,.0003,.0001,.00003,1e-5,1e-6,1e-7,1e-8]
    states=[];gas=[];phase=[];de=[]
    for e in es:
        mh=cm*e**1.5;vh=z/math.sqrt(e);gh=mh**3/(64*math.pi*vh*vh)
        lm=cl*e**2.5
        for dens,vel,label in [(.3,.001,'halo_benchmark'),(10.,.0001,'dense_slow_benchmark')]:
            rho=dens*hbarc_cm**3;pauli=(6*math.pi**2*rho/(2*vel**3))**.25
            for alpha in [1e-2,1e-4,1e-6]:
                lower=(rho/(alpha*alpha*mh*mh*vh*vh))**.25;upper=hbar/(age_s*gh)
                states.append(dict(e=e,benchmark=label,alpha_max=alpha,mu_density_min_GeV=lower,mu_phase_width_max_GeV=upper,necessary_interval_open=lower<upper,
                                   DE_fixed_radial_amplitude=math.sqrt(rho)/(muDE*muDE*mh*vh)))
            for target in [1e-6,1e-5,1e-3]:
                mu=target/lm;F2=mu**4/31
                # Leading Goldstino low-energy partial width. Its matching and
                # alternative channels are independently checked in cold_states/.
                width=target**5/(16*math.pi*F2)
                gas.append(dict(e=e,benchmark=label,m_photino_GeV=target,mu_GeV=mu,v_GeV=mu*vh,
                                Goldstino_partial_width_GeV=width,partial_lifetime_s=hbar/width,
                                survives_partial_width_age=hbar/width>age_s,Pauli_min_mass_GeV=pauli,
                                Pauli_density_allowed=target>=pauli,coarse_occupation_fraction=(pauli/target)**4,
                                vacuum_to_DE=(mu/muDE)**4,
                                lightest_tree_gap_ratio=target/(ref['minimum_positive_tree_mass']*math.sqrt(e/.01)*mu)))
        de.append(dict(e=e,mu_DE_GeV=muDE,m_radial_GeV=muDE*mh,m_photino_GeV=muDE*lm,
                       phase_partial_radial_lifetime_s=hbar/(muDE*gh),
                       radial_rho_over_raw_vacuum_at_alpha01=31*1e-4*mh*mh*vh*vh))
    # Dimensionful helicity growth uses actual TP03 matched frequencies;
    # its inverse is an amplitude e-fold time, not a fractional-charge lifetime.
    pp=json.loads((ROOT/'reviews/finite_matching_2026_11_01/run_pressure/result.json').read_text())
    for d in pp['cases']:
        if d['scheme']=='finite_matched' and d['interpolation_nodes']==29 and d['stencil_h']==.0025:
            e=d['e'];om=muDE*math.sqrt(d['boundary']['omega2']);ctheta=5*(29/200)*e*e/(8*math.pi**2);gamma=ctheta*om/2
            phase.append(dict(e=e,variant='raw_vacuum_equals_DE',omega_GeV=om,c_theta=ctheta,
                              amplitude_efold_s=hbar/gamma,growth_over_H0=gamma/H0,
                              unstable_band_kmax_GeV=ctheta*om,
                              minimum_patch_halfwave_m=math.pi*hbar*c/(ctheta*om)))
    checks={'cm_scaling_below_1e-12':abs(mass_controls[0]['mass_coefficient']/mass_controls[1]['mass_coefficient']-1)<1e-12,
            'stationarity_roundoff_below_1e-12':max(x['stationarity_over_curvature'] for x in mass_controls)<1e-12,
            'units_hbar_matches_CODATA':abs(hbar/6.582119569509067e-25-1)<1e-14,
            'radial_intervals_66':len(states)==66,'photino_examples_66':len(gas)==66,
            'phase_growth_examples_2':len(phase)==2,
            'DE_tied_harmonic_density_never_halo_small':all(x['DE_fixed_radial_amplitude']>1 for x in states),
            'some_weaker_coupling_necessary_radial_window':any(x['necessary_interval_open'] for x in states if x['e']<.01),
            'some_photino_partial_lifetime_and_Pauli_window':any(x['survives_partial_width_age'] and x['Pauli_density_allowed'] for x in gas)}
    result=dict(claim_id='TP04_UNITS_NECESSARY_CONDITIONS',checks=checks,all_checks_pass=all(checks.values()),
                constants=dict(hbar_GeV_s=hbar,hbarc_GeV_cm=hbarc_cm,reduced_Mpl_GeV=Mbar,H0_s=H0_s,rho_DE_GeV4=rhoDE,mu_if_raw_vacuum_is_DE_GeV=muDE,required_lifetime_s=age_s),
                mass_controls=mass_controls,photino_mass_coefficient=cl,radial_necessary_windows=states,photino_conditional_examples=gas,DE_tied_examples=de,phase_helicity_growth=phase,
                runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                non_claims=['Passing a partial-width and Pauli test does not prove total lifetime or cosmological viability','Halo distributions and vacuum offsets are not selected','LO radial mass, leading pole photino mass and Goldstino soft limit only','No stimulated/Floquet, thermal, gravity-completion or all-orders bound supplied by this unit check','Helicity amplitude growth is not a fractional charge decay width'])
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=checks,constants=result['constants'],mass_controls=mass_controls,photino_mass_coefficient=cl,phase_helicity_growth=phase),indent=2));assert result['all_checks_pass'],checks

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);main(p.parse_args().out)
