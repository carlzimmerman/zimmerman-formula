"""Read-only instrumentation of Qwen's exact paths; no changes to transport/RNG.
Candidate uses seeds42/43, not required contract seeds. Not a complete certificate.
"""
import ast, contextlib, io, json, os, pathlib, tempfile
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parent
source=(ROOT/'candidate.py').read_text()
tree=ast.parse(source)
class CapturePaths(ast.NodeTransformer):
    def visit_Assign(self,node):
        if any(isinstance(t,ast.Name) and t.id=='valid' for t in node.targets):
            return [ast.copy_location(ast.parse('capture(locals())').body[0],node),node]
        return node
code=compile(ast.fix_missing_locations(CapturePaths().visit(tree)),str(ROOT/'candidate.py'),'exec')
checks={}; modes={}
def score(x):
    se=float(np.std(x,ddof=1)/np.sqrt(len(x)))
    return {'mean':float(np.mean(x)),'SE':se,'z':float(np.mean(x)/se)}
with tempfile.TemporaryDirectory() as td:
    inputs=pathlib.Path(td)/'inputs.json';inputs.write_text('{}');os.environ['ORCH_INPUTS']=str(inputs)
    for mode in ('main','positive'):
        captured=[]
        def capture(d):
            captured.append({k: d[k].copy() if isinstance(d[k],(dict,list)) else d[k] for k in ('profile','T_list','Z_list','D_list','Qs_list','Qz_list','n_photons')})
        ns={'__name__':'audit_candidate','capture':capture}
        exec(code,ns);os.environ['ORCH_MODE']=mode
        with contextlib.redirect_stdout(io.StringIO()) as log: ns['main']()
        original=json.loads(log.getvalue());modes[mode]={'original':original,'audit':{}}
        for d in captured:
            p=d['profile'];tag=mode+'_'+p['name'];N=d['n_photons']
            T,Z,D,S,Q=[np.array(d[k],float) for k in ('T_list','Z_list','D_list','Qs_list','Qz_list')]
            checks[tag+'_all_finite_complete']=bool(len(T)==N and np.isfinite([T,Z,D,S,Q]).all())
            checks[tag+'_geometry']=bool(np.all((Z>=-1e-12)&(Z<=1+1e-12)) and np.all(D>=-1e-12))
            R=score((D-p['d'])**2-2*S/3-11*(1-Z**2)/9)
            G=score(Z**2-1-.3*S+.9*Q)
            mean=score(D-p['d'])
            wrong_R=score((T-p['d'])**2-2*S/3-11*(1-Z**2)/9)
            wrong_mean=score(T-p['d'])
            checks[tag+'_paired_residuals']=abs(R['z'])<=5 and abs(G['z'])<=5
            checks[tag+'_mean']=abs(mean['z'])<=5
            # Exactly the same residual/mean tests with T substituted for D.
            wrong_pass=abs(wrong_R['z'])<=5 and abs(G['z'])<=5 and abs(wrong_mean['z'])<=5
            checks[tag+'_real_wrong_observable_rejected']=not wrong_pass
            modes[mode]['audit'][p['name']]={'N':N,'R':R,'G':G,'D_minus_d':mean,'T_substituted_R':wrong_R,'T_minus_d':wrong_mean}
result={'claim':'Finite instrumentation audit, not acceptance of original certificate','checks':checks,'modes':modes,'limitations':['Original seeds42/43 differ from contract','No verified collision-counter atom test','Transport edge cases unresolved','No universal or novelty claim']}
import sys
pathlib.Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"checks_passed":sum(checks.values()),"checks_total":len(checks)}))
assert all(checks.values()),checks
