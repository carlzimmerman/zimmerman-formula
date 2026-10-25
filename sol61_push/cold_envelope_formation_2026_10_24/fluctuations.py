"""Exact finite-window quadratic identity for saved monopole shell Hamiltonians."""
import json,pathlib,hashlib,numpy as np
P=pathlib.Path(__file__).resolve().parent;tags=['draco_L12_long','draco_escape_long','sextans_L24_long','sextans_escape','sextans_escape_long'];files=[pathlib.Path(__file__)]+[P/'runs'/f'{t}.json' for t in tags]
def hashes():return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
before=hashes();out=[]
for tag in tags:
 q=json.loads((P/'runs'/f'{tag}.json').read_text());r=np.array(q['radial_grid']);T=q['history'][-1]['t'];tail=[h for h in q['history'] if h['t']>=max(24.,.75*T)];shell=np.array([np.diff(np.r_[0,h['cdf']]) for h in tail]);mean=shell.mean(axis=0)
 def pot(s):return -np.cumsum(s)/r-(np.cumsum((s/r)[::-1])[::-1]-s/r)
 def W(s):return .5*float(np.sum(s*pot(s)))
 ws=np.array([W(s) for s in shell]);wbar=W(mean);var=float(ws.mean()-wbar);direct=float(np.mean([W(s-mean) for s in shell]));assert abs(var-direct)<1e-12 and var<1e-12
 wf=np.array([h['E']-h['K'] for h in tail]);anis=float(np.mean(wf-ws));assert anis<1e-9
 scale=q['physical']['Munit_Msun']*q['physical']['Vunit_kms']**2
 out.append({'tag':tag,'scope':'finite-window variation includes secular mass loss; monopole contribution only, not a stationary stochastic noise model','time_window':[tail[0]['t'],tail[-1]['t']],'mean_total_mass_fraction':float(np.mean([h['M'] for h in tail])),'monopole_mean_W_code':float(ws.mean()),'W_of_mean_monopole_code':wbar,'monopole_correlation_W_code':var,'direct_delta_density_W_code':direct,'monopole_correlation_W_Msun_kms2':var*scale,'mean_nonspherical_W_code':anis,'monopole_correlation_over_abs_mean_E':abs(var)/abs(np.mean([h['E'] for h in tail]))})
after=hashes();assert before==after;(P/'fluctuations.json').write_text(json.dumps({'scope':'coarse-graining energy audit, not new dissipation or stellar-heating result','inputs_before':before,'inputs_after':after,'results':out},indent=2)+'\n')
for row in out:print(row['tag'],'correlation/E',row['monopole_correlation_over_abs_mean_E'],'nonspherical_W',row['mean_nonspherical_W_code'])
