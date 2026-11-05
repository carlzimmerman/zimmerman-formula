import pathlib,json,math
D=json.loads(pathlib.Path('law_snapshot.json').read_text()); rows=[]
for foot,v in D['footings'].items():
 r=v['rows']['A30']; x=r['value']; d=r['measured']; assert d==56
 t=1.0; acc=t
 for k in range(1,28): t*=x/2/k; acc+=t
 exact=math.exp(-x/2)*acc
 normal=math.erfc(abs(r['Z'])/math.sqrt(2))
 rows.append(dict(footing=foot,chi2=x,dof=d,p_chi2_exact=exact,p_normal_used=normal,ratio=exact/normal))
result=dict(outcome='RQ3 converts chi-square to a moment-normal Z before applying Gaussian tails; this is not an exact calibrated p-value',rows=rows,non_claims=['56 dof and covariance calibration accepted for this arithmetic audit','Candidate rejection may survive corrected probabilities'])
pathlib.Path('p_run/result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
