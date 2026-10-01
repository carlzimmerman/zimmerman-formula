from pathlib import Path
import json,numpy as np,math,hashlib
O=Path(__file__).resolve().parent;p=O/'corrected_statistic_results_model1p5m.json';r=json.loads(p.read_text());out=[]
for x in r['rows']:
 C=np.array(x['model_covariance'])*(x['model_N']/30000+1);d=np.array(x['derivative_lnxi']);h=np.array(x['derivative_lnkappa']);I=np.linalg.inv(C);fx=d@I@d;fh=h@I@h;mix=d@I@h
 out.append(dict(footing=x['footing'],xi=x['xi_pc'],sigma_fixed=1/math.sqrt(fx),sigma_profiled=1/math.sqrt(fx-mix*mix/fh)))
(O/'expected_covariance_sensitivity.json').write_text(json.dumps({'scope':'Expected mock covariance approximated by rescaling paired model-bootstrap covariance from original1.5M-draw population; finite model covariance added. Covariance-estimation sensitivity, not independent-realization coverage.','input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'rows':out},indent=2))
