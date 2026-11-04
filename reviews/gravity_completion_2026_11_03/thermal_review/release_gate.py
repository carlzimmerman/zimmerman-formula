"""Independent continuity/entropy audit of TH07 hidden vacuum release.

Uses thermal worker only for the declared global potential; all cosmological
constants, inequalities and spectrum-trace CW check are reconstructed here.
"""
import sys, os
sys.dont_write_bytecode = True
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[key] = '1'
import math, json, time, resource
from pathlib import Path
import numpy as np
import mpmath as mp
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent/'thermal'))
import thermal_core as th

MP = 2.435e18
HB = 6.582119569509066e-25
TG0 = 2.7255*8.617333262145e-14
TN0 = TG0*(4/11)**(1/3)
H0 = 2.1842852410855023e-18*HB
RHOC = 3*MP**2*H0**2
RHOCHI = .265*RHOC
AR = 1/1101
RHONU = 7*math.pi**2/120*TN0**4
KMAX = 1.1*RHOCHI*AR + .3*RHONU
GS0 = 43/11
GSI = 106.75
XI = .02
THETA_SM = TG0*(GS0/GSI)**(1/3)
THETA_D = XI*THETA_SM
KSM = math.pi**2/30*GSI*THETA_SM**4

def cw_trace_float(x):
    """Orthogonal trace control using explicit physical masses and dof."""
    bos, nb, ferm, nf = th.arrays(x)
    def f(ms):
        nonzero = ms > 1e-24
        result = np.zeros_like(ms)
        result[nonzero] = ms[nonzero]**2*(np.log(ms[nonzero])-1.5)
        return result
    return float((nb@f(bos)-nf@f(ferm))/(64*math.pi**2))

def gate(vac):
    xv = vac.xv
    mu = float(vac.mu)
    delta_dimensionless = vac.leading(0)-vac.leading(xv)
    dV = float(delta_dimensionless*vac.mu**4)
    assert dV > 0
    amax = (KMAX/dV)**.25
    avac = (KSM/dV)**.25
    td = THETA_D/amax
    tsm = THETA_SM/amax
    hvac = math.sqrt(dV/(3*MP**2))
    hrelease = math.sqrt((dV+KSM/amax**4)/(3*MP**2))
    # An idealized pure-kinetic release minimizes K as a^-2. These are
    # required expansion factors, not a claim that this history exists.
    samples = []
    for frac in (.1, .3, 1., 3., 10.):
        temperature = frac*td
        a = THETA_D/temperature
        over = dV*a**4/KMAX
        r = dV*a**4/KSM
        A = math.sqrt(max(1., over))
        # Exact excursion during canonical free kination + conserved SM RD:
        # r(a)=r_i/A^2 and dphi/dln a=sqrt(6)Mp sqrt[r/(1+r)].
        distance = math.sqrt(6)*MP*(math.asinh(math.sqrt(r))-math.asinh(math.sqrt(r)/A))
        samples.append(dict(TD_GeV=temperature,TD_over_energy_deadline=frac,
                            release_K_over_Kmax=over,vacuum_over_visible=r,
                            required_pure_kination_expansion=A,
                            required_free_kinetic_excursion_GeV=distance,
                            excursion_over_vacuum_R=distance/vac.R))
    cw0 = float(th.cw_mp(mp.mpf(0)))
    cwv = float(th.cw_mp(xv))
    cw0_float = cw_trace_float(0.)
    cwv_float = cw_trace_float(float(xv))
    phi_range = math.sqrt(2)*vac.R
    return dict(kind=vac.kind,mu_GeV=mu,Xv_over_mu=float(xv),R_GeV=vac.R,
                DeltaV_origin_to_preferred_GeV4=dV,
                DeltaV_over_mu4=float(delta_dimensionless),
                DeltaV_fourth_root_GeV=dV**.25,
                latest_release_a=amax,
                minimum_prerelease_TD_GeV_collisionless=td,
                minimum_prerelease_TSM_GeV=tsm,
                minimum_TD_over_mu=td/mu,
                vacuum_domination_a=avac,
                vacuum_domination_TD_GeV=THETA_D/avac,
                H_vac_GeV=hvac,H_at_energy_deadline_GeV=hrelease,
                H_over_preferred_radial_mass=hrelease/vac.ms,
                Hubble_loss_parameter_H_times_phi_over_sqrt_DeltaV=hrelease*phi_range/math.sqrt(dV),
                conservative_local_field_range_GeV=phi_range,
                CW_orthogonal_trace_relative_disagreement=max(abs(cw0_float/cw0-1),abs(cwv_float/cwv-1)),
                CW_origin_dimensionless=cw0,CW_preferred_dimensionless=cwv,
                temperature_examples=samples)

def main(out):
    start=time.monotonic()
    rows = [gate(th.Vacuum(kind)) for kind in ('canonical','protected')]
    hidden_dof_high = 86+60+(7/8)*146
    checks = dict(positive_release=all(r['DeltaV_origin_to_preferred_GeV4']>0 for r in rows),
                  CW_trace_control=all(r['CW_orthogonal_trace_relative_disagreement']<1e-6 for r in rows),
                  high_temperature_entropy_applicable=all(r['minimum_prerelease_TSM_GeV']>100 for r in rows))
    result = dict(claim_id='TH07_INDEPENDENT_RELEASE_ENERGY_GATE',checks=checks,
                  constants=dict(Mp_GeV=MP,H0_GeV=H0,rhoc_GeV4=RHOC,rhochi_GeV4=RHOCHI,
                                 rho_one_nu_today_GeV4=RHONU,a_rec=AR,Kmax_GeV4=KMAX,
                                 g_s_today=GS0,g_s_SM_initial=GSI,xi_initial=XI,
                                 TD_times_a_initial_GeV=THETA_D,TSM_times_a_highT_GeV=THETA_SM,
                                 highT_visible_K_GeV4=KSM,Kmax_over_highT_visible_K=KMAX/KSM,
                                 a_deadline_over_a_vacuum_domination=(KMAX/KSM)**.25,
                                 g_s_hidden_ultrarelativistic=hidden_dof_high),
                  rows=rows,
                  interpretation='Necessary energy gate for isolated release followed by averaged w<=1/3; TD is the pre-release collisionless comoving-temperature label. Origin proxy and global one-loop valley action, not an actual computed thermal bounce or history.',
                  runtime_seconds=time.monotonic()-start,
                  peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    assert all(checks.values())

if __name__=='__main__':main(sys.argv[1])
