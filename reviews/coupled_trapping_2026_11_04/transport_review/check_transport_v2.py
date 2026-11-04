"""Independent finite CT09 transport checks; never evolves/rescues a trajectory."""
import sys
sys.dont_write_bytecode = True
import json, math, resource, time
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.interpolate import CubicSpline

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'reviews/coupled_trapping_2026_11_04'
sys.path.insert(0, str(BASE / 'kinetics'))
from two_species import Two, DEG
from accurate import LocalPotential


def parent_integral(M, m, t, width_over_beta, n):
    """Independent parent momentum/rest-angle integral, physical fC=2 FD."""
    beta = math.sqrt(max(0., 1 - 4*m*m/(M*M)))
    z, w = leggauss(n)
    u, wu = 50*(z+1), 50*w  # P/t in [0,100]
    en = np.sqrt((M/t)**2 + u*u)
    e1 = en[:, None]/2 + beta*u[:, None]*z[None, :]/2
    e2 = en[:, None]-e1
    p1 = np.sqrt(np.maximum(0., e1*e1-(m/t)**2))
    p2 = np.sqrt(np.maximum(0., e2*e2-(m/t)**2))
    f1 = 2*np.exp(-p1)/(1+np.exp(-p1))
    f2 = 2*np.exp(-p2)/(1+np.exp(-p2))
    avg = (f1*f2)@w/2
    return width_over_beta*beta*M*t*t/(2*math.pi**2)*float((wu*u*u/en)@avg)


def main(out):
    start = time.monotonic()
    stat = json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal_kinetic/run_stationary_002/result.json').read_text())
    spins = json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal/run_static_001/result.json').read_text())
    point, spin = stat['points'][1], spins['points'][1]['spins'][0]
    pole = math.sqrt(.006/.003**2-2/(31*.003))
    M = math.sqrt(.006)
    kernel_rows, conv_rows, initial_count_rows = [], [], []
    # All kernel comparisons retain the implementation's interpolated partial
    # width/beta. Only its cell construction/integration is under examination.
    for bins in (24, 32, 64, 128):
        model = Two(point, spin, bins=bins, orbitn=16)
        exact_I2 = 1.8030853547393915
        initial_count_rows.append(dict(bulk_bins=bins, discrete_I2=model.norm, exact_FD_I2=exact_I2, relative_error=model.norm/exact_I2-1))
        for dx, t in ((-.001,.0005),(-.00001,.00002),(-.000001,.00001)):
            x = pole+dx
            mass = .003/2*math.sqrt(x*x+2/(31*.003))
            i = min(max(0,int(np.searchsorted(model.sx,x)-1)),len(model.sx)-2)
            alpha = min(1,max(0,(x-model.sx[i])/(model.sx[i+1]-model.sx[i])))
            coeff = 0.
            # Remove every nonconstant parent, leaving actual pole data only.
            saved = model.scalar
            model.scalar = []
            for row in saved:
                rr = dict(row)
                rr['parents'] = [[mm,ww] for mm,ww in row['parents'] if abs(mm-M)<1e-8]
                model.scalar.append(rr)
            for row,fac in ((model.scalar[i],1-alpha),(model.scalar[i+1],alpha)):
                for mm,ww in row['parents']:
                    beta_row = math.sqrt(max(0,1-4*row['mS']**2/mm**2))
                    if beta_row>1e-10 and mm>2*mass:
                        coeff += fac*ww/beta_row
            K = model.scalar_kernel(x,t)
            numerical = DEG/(4*math.pi**2)*float(model.f0@(K@model.f0))
            ref256 = parent_integral(M,mass,t,coeff,256)
            ref512 = parent_integral(M,mass,t,coeff,512)
            kernel_rows.append(dict(bulk_bins=bins,x=x,Tc=t,
                discrete_gamma=numerical,parent_gamma_512=ref512,
                relative_error=numerical/ref512-1,
                reference_256_vs_512=ref256/ref512-1,
                coefficient_width_over_beta=coeff,
                symmetry_error=float(np.max(abs(K-K.T))),
                minimum_kernel_entry=float(K.min())))
            model.scalar = saved
        if bins==32:
            for x,t in ((.1,.004),(3.,.004),(3.8375,.004),(5.,.001),(25.4,.0005),(25.4,.00001)):
                A, events = model.conversion(x,t)
                F = float(model.mass(x)); S = .003/2*math.sqrt(x*x+2/(31*.003))
                ma,mb = max(F,S),min(F,S)
                a = 0 if F>S else 1
                n = model.n
                gamma = float(np.interp(x,model.rx,[r['gauge_channels_total_over_mu' if a==0 else 'reverse_gauge_channels_total_over_mu'] for r in model.sources]))
                energies = np.r_[np.sqrt(F*F+(t*model.q)**2),np.sqrt(S*S+(t*model.q)**2)]
                moment = -(energies@A)[a*n:(a+1)*n]
                exact = gamma*(ma*ma-mb*mb)/(2*ma)
                off = A.copy(); np.fill_diagonal(off,0.)
                fd = model.W*model.f0/model.norm
                conv_rows.append(dict(x=x,Tc=t,parent='F' if a==0 else 'S',
                    column_sum_absolute_max=float(np.max(abs(A.sum(axis=0)))),
                    min_offdiagonal=float(off.min()),
                    all_parent_cell_energy_errors=(moment/exact-1).tolist() if exact else [],
                    FD_weighted_energy_error=float(fd@moment/exact-1) if exact else 0.,
                    smallest_emission_energy_rate=float(moment.min()),
                    exact_emission_energy_rate=exact))
    profile = json.loads((BASE/'gravity_resonance/run_leading001/result.json').read_text())['packet']
    r = profile['global_profile']
    original = CubicSpline(r['grid'],r['V0_origin_subtracted_mu4'],bc_type=((1,r['origin_force']),(2,0)))
    local = LocalPotential(original,profile['local_profile'])
    joins = []
    for sign in (-1,1):
        x = local.x0+sign*.0018
        joins.append(dict(x=x,polynomial_minus_spline=[float(np.polyval(np.polyder(local.co,k),x-local.x0)-(original(x,k)-(local.ref if k==0 else 0.))) for k in range(3)]))
    pole_data=json.loads((BASE/'microphysics/run_pole002/result.json').read_text())
    leading=[]
    for name in ('run_leading_two_001','run_leading_fine_001'):
        c=json.loads((BASE/'kinetics'/name/'result.json').read_text())['case']
        h=c['history'][-1];q=np.array(c['q_centers']);edges=np.array(c['q_edges']);W=np.diff(edges**3)/3;f=np.array(c['final_f_S_number_normalization']);wn=W*f;wn/=wn.sum()
        t=h['Tc_over_mu'];mu=c['mu_GeV'];H=math.sqrt(math.pi**2*106.75/90)*t*t*mu/(2.435e18*.02**2);omega=H/h['H_over_oscillation'];m=pole_data['mC'];g=np.array(pole_data['Gamma_other_eigenvalues_mu']);amp=(h['x_outer']-h['x_inner'])/2;dm=.003*pole/(2*math.sqrt(pole*pole+2/(31*.003)))
        leading.append(dict(run=name,number_survival=h['survival'],Y_charged=h['Y_charged'],rho_rest_over_s_GeV=h['Y_charged']*m*mu,q_RMS=float(np.sqrt(wn@(q*q))),omega_over_mu=omega,
            Gamma_over_omega=(g/omega).tolist(),lifetime_in_orbital_periods=(omega/(2*math.pi*g)).tolist(),
            rms_single_particle_kinetic_energy_over_mu=float(t*t*(wn@(q*q))/(2*m)),
            amplitude_detuning_over_mu=2*dm*amp,
            sweep_rate_abs_at_pole_over_mu2=2*dm*amp*omega,
            diagnostic_sweep_over_Gamma2=(2*dm*amp*omega/(g*g)).tolist(),
            occupancy_max=float(2*f.max()),energy_ledger_error=h['energy_ledger_error']))
    result=dict(assertion_tested='Independent static kernel benchmark; conversion generator/moment controls; matched-leading join and lifetime diagnostics only.',
        initial_count_cases=initial_count_rows,kernel_cases=kernel_rows,conversion_cases=conv_rows,potential_join_cases=joins,leading_cases=leading,
        checks=dict(kernel_nonnegative=all(r['minimum_kernel_entry']>=0 for r in kernel_rows),kernel_symmetric=all(r['symmetry_error']==0 for r in kernel_rows),
            independent_parent_integral_repeat=bool(max(abs(r['reference_256_vs_512']) for r in kernel_rows)<.001),
            conversion_count_columns=max(r['column_sum_absolute_max'] for r in conv_rows)<1e-20,
            conversion_positive_offdiagonal=min(r['min_offdiagonal'] for r in conv_rows)>=0),
        runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        scope='No new trajectory, no restoration of missing channels/statistics, no dynamical resonance solution. Diagnostic timescales are not a computed memory kernel.')
    Path(out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(checks=result['checks'],kernel_max_relative_error=max(abs(r['relative_error']) for r in kernel_rows),runtime_seconds=result['runtime_seconds'],peak_rss_bytes=result['peak_rss_bytes_macos'])))
    assert all(result['checks'].values())


if __name__=='__main__':
    main(sys.argv[1])
