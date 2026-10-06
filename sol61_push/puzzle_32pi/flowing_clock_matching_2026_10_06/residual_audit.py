"""Independent high-precision original-form ODE evaluation at saved solver states."""
import ast,json,argparse
from pathlib import Path
import mpmath as mp
mp.mp.dps=60
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
base=Path(__file__).resolve().parent
source=base.parent/'flowing_clock_2026_10_06'/'spherical_adm'/'ode.py'
class MathMP:
 exp=staticmethod(mp.exp);log=staticmethod(mp.log);asinh=staticmethod(mp.asinh)
 hypot=staticmethod(lambda x,y:mp.sqrt(x*x+y*y))
 copysign=staticmethod(lambda x,y:abs(x)*(1 if y>=0 else -1))
tree=ast.parse(source.read_text());defs=ast.Module(body=[z for z in tree.body if isinstance(z,ast.FunctionDef)],type_ignores=[])
ns={'math':MathMP(),'K':mp.mpf(1),'H':mp.mpf(1)}
exec(compile(defs,str(source),'exec'),ns)
run=json.loads((base/'runs/main_b/results.json').read_text())
rows=[]
for row in run['runs']:
 errors=[];currents=[];F=[];speed=[]
 for pt in row['samples']:
  r=mp.mpf(str(pt['r']));y=[mp.mpf(str(z)) for z in pt['y']]
  deriv,z=ns['equations'](r,y,mp.mpf('.5'),mp.mpf(1))
  errors.append(max(abs(q-mp.mpf(str(v))) for q,v in zip(deriv,pt['derivative'])))
  currents.append(abs(z['qjr']));F.append(z['F']);speed.append(z['circular_speed2'])
 rows.append({'tol':row['tol'],'states_checked':len(errors),'max_derivative_absolute_difference':float(max(errors)),'max_original_exact_current':float(max(currents)),'min_F':float(min(F)),'circular_speed2_min':float(min(speed)),'circular_speed2_max':float(max(speed))})
assert all(z['max_derivative_absolute_difference']<1e-6 for z in rows), 'Stable equations differ from original highprecision ODE'
assert all(z['min_F']>0 for z in rows), 'Static patch lost'
result={'mpmath_dps':mp.mp.dps,'scope':'Original-form ODE at saved states; no between-node defect or certified integration error bound','checks':rows}
Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
