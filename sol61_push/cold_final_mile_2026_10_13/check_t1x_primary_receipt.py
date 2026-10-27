import json,sys
p='campaign_fresh_gravity/CFG650_theory_v2_combined_pm/'
d=json.load(open(p+'cfg650_native_results.json'));mut=json.load(open(p+'cfg650_native_results_MUTATE.json'));run='L100_N1024_canonical';r=d['runs'][run];n=0
for survey,sv in r['surveys'].items():
 fit=sv['fits']['IA'];assert abs(fit['F']['chi2']-fit['S0']['chi2']-sv['dchi2'])<1e-10;n+=1
 assert abs(1-sv['N_kept']/sv['N_published']-sv['frac_lost'])<1e-12;n+=1
 tooth=mut['T_OWN'][run][survey]
 calculated='CONSISTENT' if tooth and sv['N_kept']>=10 and sv['dchi2']<4 and max(sv['robust'].values())<9 else 'NOT DIAGNOSTIC'
 assert calculated==sv['class'];n+=1
assert 'PENDING' in d['verdict_per_footing']['alt'];n+=1
assert 'NOT EVALUATED' in d['cmb_gate'];n+=1
import math,bisect
base='sol61_push/cold_final_mile_2026_10_13/t1x_input_snapshot/'
pm=json.load(open(base+'cfg650_m1m2m3_RES_canonical_N1024_L100_ns1024_lean.json'));job=json.load(open(base+'job.json'))
assert job['job']=='T1x' and job['spec']['MODS']=='123';n+=1
assert pm['modules']['M1'] and pm['modules']['M2'] and pm['modules']['M3'] and not pm['modules']['M4'];n+=1
assert pm['np']==1024 and pm['foot']=='canonical' and 'z0' in pm['snap'];n+=1
z=pm['snap']['z0'];xx=[math.log(k) for k in z['k']];yy=[g/a for g,a in zip(z['P_grav'],z['P'])]
for label,value in r['B_at'].items():
 v=math.log(float(label));i=bisect.bisect_right(xx,v)-1
 ans=yy[0] if i<0 else yy[-1] if i>=len(xx)-1 else yy[i]+(yy[i+1]-yy[i])*(v-xx[i])/(xx[i+1]-xx[i])
 assert abs(ans-value)<1e-12;n+=1
frb=json.load(open('campaign_fresh_gravity/CFG786_frb_systematics/cfg786_results.json'))
assert frb['cls']=='WEAKENED' and frb['K1'];n+=1
json.dump(dict(checks=n,scope='Raw small PM snapshot job/modules/boost and stored score arithmetic/classes; no PM or likelihood replication',footing=d['verdict_per_footing'],kids=r['surveys']['KiDS']['dchi2']),open(sys.argv[1],'w'),indent=2)
