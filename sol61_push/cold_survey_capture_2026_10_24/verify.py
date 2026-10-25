"""Check raw-input pins, analytic Jeans limits and orbit ledgers."""
import json, math, hashlib
import numpy as np
from numpy.polynomial.legendre import leggauss
import survey as s

r=json.loads((s.HERE/'survey_results.json').read_text())
receipt=json.loads((s.HERE/'survey_receipt.json').read_text())
assert receipt['input_hashes']==s.hashes()
assert receipt['result_hash']==hashlib.sha256((s.HERE/'survey_results.json').read_bytes()).hexdigest()
d=s.load();assert r['selected_ids']==d['ids']
a=500.;M=1e7;xx,ww=leggauss(96);theta=(xx+1)*math.pi/4;ww*=math.pi/4
R=a*np.tan(theta);force=lambda x:s.G*M*x/(x*x+a*a)**1.5
expected=math.pi*s.G*M/(32*a)
errors={}
for beta in [0.,-.5]:
    projected=s.projection(R,a,force,beta)
    moment=float(np.sum(ww*2*np.sin(theta)*np.cos(theta)*projected))
    errors[str(beta)]=abs(moment/expected-1)
assert max(errors.values())<5e-4
# This absolute normalization rejects a doubled gravitational contribution.
assert abs(2*moment/expected-1)>.9
cap=json.loads((s.HERE/'capture_results.json').read_text())
cr=json.loads((s.HERE/'capture_receipt.json').read_text())
for name,h in cr['hashes'].items():assert hashlib.sha256((s.ROOT/name).read_bytes()).hexdigest()==h
assert cr['result_hash']==hashlib.sha256((s.HERE/'capture_results.json').read_bytes()).hexdigest()
assert max(v['max_post_impulse_energy_drift'] for v in cap['stellar_response'])<1e-4
for model in cap['models']:
    eb=model['final_cold_virial_energy_per_mass']
    for z in model['no_net_external_work_wave_energy_budget']:
        q=z['escaped_over_final_mass']
        if q is None:continue
        ei=z['v_infinity']**2/2;eo=z['v_out_infinity']**2/2
        assert abs((1+q)*ei-eb-q*eo)<1e-8
        q_bad=(ei-eb)/eo # mutation: forget incoming energy of the escaped mass
        assert abs((1+q_bad)*ei-eb-q_bad*eo)>1e-3
assert all(v['optimizer_success'] for v in r['continuous_best']+r['robust']+r['mass_profiles'])
out=dict(status='self-review checks passed; not observational/model validation',global_virial_relative_errors=errors,
    absolute_double_gravity_mutation_rejected=True,selected_ids_match=True,source_hashes_match=True,
    wave_energy_mass_ledger_verified=True,missing_incoming_escape_energy_mutation_rejected=True,
    failed_grid_optimizer_count=sum(not v['optimizer_success'] for v in r['results']),
    peak_RSS_survey_bytes=receipt['peak_RSS_bytes_macos'],peak_RSS_capture_bytes=cr['peak_RSS_bytes_macos'])
(s.HERE/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
