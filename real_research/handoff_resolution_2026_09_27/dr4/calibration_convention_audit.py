from pathlib import Path
import json,numpy as np,math,hashlib
O=Path(__file__).resolve().parent;p=O/'corrected_statistic_results_model1p5m.json';r=json.loads(p.read_text());rows=[]
for x in r['rows']:
 C=np.array(x['joint_covariance']);d=np.array(x['derivative_lnxi']);h=np.ones(9);I=np.linalg.inv(C);f=d@I@d-(d@I@h)**2/(h@I@h)
 rows.append(dict(footing=x['footing'],xi=x['xi_pc'],sigma_pre_noise_velocity_scale=x['joint_anchor']['profiled_sigma'],sigma_post_median_scale=1/math.sqrt(f)))
(O/'calibration_convention_results.json').write_text(json.dumps({'scope':'Same joint covariance; compare explicitly proposed orbital velocity scaling before noise with frozen-estimator-style multiplicative scaling of medians. Log-median derivative for latter is exactly one.','input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'rows':rows},indent=2))
