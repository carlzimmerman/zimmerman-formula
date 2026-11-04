"""Sharper energy-norm passive Floquet bound; immutable v3 inputs retained."""
import sys
sys.dont_write_bytecode=True
from response_api_v3 import *
import time,resource

def sharp_bound(xmid,amplitude):
    m=float(charged_mass(xmid-abs(amplitude)))
    beta=math.sqrt(max(0,1-4*m*m/M**2));factor=144*beta/(32*math.pi*M)
    invsqrt=(U*(1/np.sqrt(WIDTH))[None,:])@U.T
    C=invsqrt@(factor*G)@invsqrt
    epsilon=float(np.linalg.eigvalsh(C).max())
    return dict(relative_form_norm=epsilon,minimum_rate_ratio=max(0,1-epsilon)**2,
                maximum_rate_ratio=(1+epsilon)**2,actual_GammaC_max=factor*G)

def main(out):
    start=time.monotonic();late=json.loads((PRIOR/'kinetics/run_hybrid_bw_001/result.json').read_text())['case']
    measured=json.loads((Path(__file__).resolve().parent/'run_v3checks001/result.json').read_text())
    rows=[]
    for r in measured['rows']:
        h=late['history'][r['history_index']];b=sharp_bound(h['x_minimum'],(h['x_outer']-h['x_inner'])/2)
        rows.append(dict(Tc=r['Tc'],bound=b,measured_local_absorptive_ratio=r['local_absorptive_charged_width_multiplier']))
    checks=dict(sharp_bound_contains_full_FFT=all(x['bound']['minimum_rate_ratio']<=x['measured_local_absorptive_ratio']<=x['bound']['maximum_rate_ratio'] for x in rows),
                positive_width=all(np.linalg.eigvalsh(x['bound']['actual_GammaC_max']).min()>-1e-22 for x in rows))
    result=dict(claim_id='CC10_PASSIVE_CHARGED_WIDTH_ENERGY_NORM_BOUND',checks=checks,rows=rows,
      proof='For periodic L=dt+iδ+Γout/2 and B=ΓC/2>=0, (L+B)δa=−Ba0. Taking real weighted energy gives ||Γout^1/2δa|| <= ||Γout^-1/2 ΓC Γout^-1/2||sup ||Γout^1/2 a0||. Triangle and reverse triangle bound exit-rate ratio by (1±epsilon)^2. This is an operator statement on periodic L2 and survives positive continuum integration.',
      scope='Explicit local on-shell charged absorptive width only; no claim to bound an unspecified dispersive/nonlocal charged selfenergy.',runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(out).write_text(json.dumps(serialize(result),indent=2)+'\n');print(json.dumps(serialize(result)));assert all(checks.values())

if __name__=='__main__':main(sys.argv[1])
