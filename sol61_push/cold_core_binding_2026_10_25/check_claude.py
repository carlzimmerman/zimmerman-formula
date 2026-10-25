import hashlib,json,pathlib,subprocess
Q=pathlib.Path(__file__).resolve().parent;ROOT=Q.parents[1];P=ROOT/'reviews/cold_filter_interface_2026_10_25';files=[P/'REPORT.md',P/'check.py',P/'FROZEN_CRITERIA.md',P/'contract.json',P/'run_fixed/result.json',P/'run_fixed/manifest.json',Q/'check_claude.py'];pins={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files};d=json.loads((P/'run_fixed/result.json').read_text());cases=[];errors=[]
for c in d['cases']:
 for domain in c['domains']:
  for w in domain['waves']:
   errors.append(abs(w['R']+w['T']-1))
   if w['p_over_mout']==.001 and domain['L']==20:cases.append(dict(density=c['density_star_over_D'],R=w['R'],T=w['T'],one_minus_R_minus_T=1-w['R']-w['T']))
assert len(cases)==3 and max(errors)<1e-8
out=dict(owner_commit='a40c03c62e',head_when_checked=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),scope=d['scope'],cold_cases=cases,max_flux_defect=max(errors),interpretation='This static fixed-source linear filter reflects/transmits at conserved frequency; it supplies no absorptive energy sink in this approximation. It may regulate loading, but live source recoil/work, actual four-dwarf environments and a same-action bridge are not provided. No filter result is transferred to the conditional CCT wave.',inputs_before=pins,inputs_after={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files});assert out['inputs_before']==out['inputs_after'];(Q/'claude_check.json').write_text(json.dumps(out,indent=2)+'\n');print(cases,max(errors))
