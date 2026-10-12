"""Declared longer-time continuation; reuse pinned solver without editing it."""
import ast,json
from pathlib import Path
p=Path(__file__).resolve().parent
tree=ast.parse((p/'spherical.py').read_text())
prefix=[]
for node in tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='rows' for t in node.targets):break
    prefix.append(node)
class Longer(ast.NodeTransformer):
    def visit_Constant(self,node):
        if node.value==160:return ast.copy_location(ast.Constant(640),node)
        return node
tree=ast.fix_missing_locations(Longer().visit(ast.Module(body=prefix,type_ignores=[])))
env={'__file__':str(p/'spherical.py')};exec(compile(tree,str(p/'spherical.py'),'exec'),env)
run=env['run'];np=env['np'];checks=env['checks'];check=env['check']
rows=[run(512,2048,.04),run(512,4096,.02),run(1024,4096,.04)]
for r in rows:r['formation']=all(s['force_rms_fractional_error']<=.1 and s['min_force']>=0 for s in r['samples'] if s['time']>=560)
base=np.array(rows[0]['force']);target=np.array(rows[0]['target'])
for label,other in [('refinement',rows[1]),('box',rows[2])]:
    pred=np.interp(rows[0]['r'],other['r'],other['force'])
    check(label+' force',np.linalg.norm(pred-base)/np.linalg.norm(target),.03)
out=dict(rows=rows,checks=checks,all_checks_pass=all(c['passed'] for c in checks))
(p/'spherical_long_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(checks=checks,summaries=[dict(R=r['R'],N=r['N'],formation=r['formation'],late=[s for s in r['samples'] if s['time']>=560]) for r in rows]),indent=2))
assert out['all_checks_pass']
