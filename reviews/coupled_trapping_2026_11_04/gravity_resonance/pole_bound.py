"""Independent matrix proof control and favorable pole-depletion comparison."""
import os,sys
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
MP=2.435e18;GST=106.75;GS0=3.909;XI=.02;T0=2.3486541805581e-13;DM=.44e-9


def main(output):
    start=time.monotonic()
    data=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/microphysics/run_pole002/result.json').read_text())
    source=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/run_charged/result.json').read_text())
    G=np.array(data['production_Gram_mu2']);go=np.array(data['Gamma_other_matrix_mu'])
    M=data['Mpole'];m=data['mC'];gi=np.linalg.inv(go)
    maxsigma=2/(m*M*M)*float(np.trace(G@gi))
    rng=np.random.default_rng(20261104)
    controls=[]
    # Hermitian detunings and positive incoming widths need not commute.
    # Normalize to the existing width scale to avoid meaningless PSD residuals.
    scale=float(np.linalg.norm(gi,2)/(M*M))
    for j in range(96):
        raw=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
        H=(raw+raw.conj().T)/2*M*np.linalg.norm(go,2)*10**((j%9-4)/2)
        raw=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
        incoming=(raw@raw.conj().T)*np.linalg.norm(go,2)*10**((j%7-4)/2)
        D=np.linalg.inv(H+1j*M*(go+incoming))
        A=gi/(M*M)-D@go@D.conj().T
        psd=float(min(np.linalg.eigvalsh((A+A.conj().T)/2)))/scale
        sigma=2/m*float(np.trace(G@D@go@D.conj().T).real)
        controls.append(dict(case=j,min_normalized_PSD_eigenvalue=psd,sigma_over_upper=sigma/maxsigma))
    cases=[]
    for old in source['cases']:
        if old['name'] not in ('canonical','protected'):continue
        mu=old['mu_GeV'];mass=m*mu;gate=.1*DM/mass
        for t in (.00466,.003,.001,.0005):
            Tsm=t*mu/XI
            H=math.sqrt(math.pi**2*GST/90)*Tsm*Tsm/MP
            s=2*math.pi**2/45*GST*Tsm**3
            afinal=Tsm/T0*(GST/GS0)**(1/3)
            loss=s/(2*H)*maxsigma/(mu*mu)*(1-1/afinal)
            for initial in (3.74544e-7,1e-8,1e-10):
                lower=1/(1/initial+loss)
                cases.append(dict(kind=old['name'],mu_GeV=mu,m_charged_on_pole_GeV=mass,
                    Tc_start_over_mu=t,T_SM_start_GeV=Tsm,initial_yield=initial,
                    sigma_max_GeVm2=maxsigma/(mu*mu),pole_loss_integral_upper=loss,
                    charged_yield_gate=gate,remaining_yield_lower=lower,
                    lower_over_charged_gate=lower/gate,
                    required_additional_pole_multiplier=(1/gate-1/initial)/loss))
    checks=dict(matrix_width_positive=min(np.linalg.eigvalsh(go))>0,
                input_rest_cross_section=abs(maxsigma/data['sigma_pair_v_at_rest_mu_minus2']-1)<1e-11,
                normalized_matrix_order=min(c['min_normalized_PSD_eigenvalue'] for c in controls)>-1e-10,
                noncommuting_cross_sections_bounded=max(c['sigma_over_upper'] for c in controls)<=1+1e-10,
                protected_ideal_pole_still_above_gate=all(c['remaining_yield_lower']>c['charged_yield_gate'] for c in cases if c['kind']=='protected'))
    result=dict(claim_id='CT09_UNIFORM_COHERENT_POLE_DEPLETION_BOUND',checks={k:bool(v) for k,v in checks.items()},
        sigma_max_mu_minus2=maxsigma,matrix_controls=controls,cases=cases,
        scope='Analytic uniform fixed-coefficient coherent pole bound plus finite cosmological comparisons; ideal permanent alignment, all particles scalar, no returning neutral carriers. Not a sum of every annihilation channel or full finite-temperature selfenergy calculation.',
        runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(checks=result['checks'],sigma_max=maxsigma,runtime_seconds=result['runtime_seconds'],peak_rss_bytes=result['peak_rss_bytes'])))
    assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
