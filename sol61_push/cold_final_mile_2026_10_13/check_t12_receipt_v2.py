import json,sys
p='campaign_fresh_gravity/CFG650_theory_v2_combined_pm/'
d=json.load(open(p+'cfg650_native_results_T12.json'));mut=json.load(open(p+'cfg650_native_results_T12_MUTATE.json'));run='L100_N1024_canonical';r=d['runs'][run];n=0
for survey,sv in r['surveys'].items():
 fit=sv['fits']['IA'];assert abs(fit['F']['chi2']-fit['S0']['chi2']-sv['dchi2'])<1e-10;n+=1
 assert abs(1-sv['N_kept']/sv['N_published']-sv['frac_lost'])<1e-12;n+=1
 tooth=mut['T_OWN'][run][survey]
 calculated='CONSISTENT' if tooth and sv['N_kept']>=10 and sv['dchi2']<4 and max(sv['robust'].values())<9 else 'NOT DIAGNOSTIC'
 assert calculated==sv['class'];n+=1
assert 'PENDING' in d['verdict_per_footing']['alt'];n+=1
assert 'NOT EVALUATED' in d['cmb_gate'];n+=1
json.dump(dict(checks=n,scope='Stored-score arithmetic and relative classifier only; not rerun of simulation or likelihood',footing=d['verdict_per_footing']),open(sys.argv[1],'w'),indent=2)
