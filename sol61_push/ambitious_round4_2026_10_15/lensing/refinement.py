"""Independent resolution/exclusion and actual runtime normalization mutation."""
import argparse,json,time
import model
from model import *
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--cache',required=True);p.add_argument('--coarse',required=True);p.add_argument('--fit',required=True);a=p.parse_args();t=time.monotonic()
old=np.load(a.coarse);r,y,c=data();rr=r[0]
env=Environment(power_points=131072,padding=64)
eg=np.linspace(0,1.2,2401);tab=np.empty((15,len(eg)))
for i in range(0,len(eg),100):
    es=eg[i:i+100];tab[:,i:i+len(es)]=env.los(np.repeat(rr,len(es)),np.tile(es,15),order=1024,rmax=450.).reshape(15,len(es))
fit=json.loads(Path(a.fit).read_text()); comparisons=[]
for label,finite in [('B',False),('D',True)]:
    oldfit=fit['models'][label];coarse=Fitter(old['edge_grid'],old['table'],finite);fine=Fitter(eg,tab,finite)
    for lm in oldfit['logMb']:
        ex,*_=edge(lm);co=np.array([v(ex) for v in coarse.interp]);fi=np.array([v(ex) for v in fine.interp])
        direct=env.los(rr,ex,order=1536,rmax=480.)
        comparisons.append(dict(model=label,logMb=lm,edge=ex,coarse_vs_fine=floor_relative(co,fi),fine_vs_direct=floor_relative(fi,direct)))
    new=fine.fit();comparisons.append(dict(model=label,coarse_chi2=oldfit['chi2'],fine_chi2=new['chi2'],chi2_difference=new['chi2']-oldfit['chi2'],refined_fit=new))
# Actual injected mutation: multiply the module global density at runtime,
# call both independent projection implementations, restore it, compare.
normal=env.los(rr,.4);normalh=hankel(rr)
model.RHO*=2
mutated=env.los(rr,.4);mutatedh=hankel(rr)
model.RHO/=2
mutation=dict(los_relative_change=floor_relative(mutated,normal),hankel_relative_change=floor_relative(mutatedh,normalh),los_doubling_error=floor_relative(mutated,2*normal),hankel_doubling_error=floor_relative(mutatedh,2*normalh))
templmax=max(v['coarse_vs_fine'] for v in comparisons if 'coarse_vs_fine' in v)
directmax=max(v['fine_vs_direct'] for v in comparisons if 'fine_vs_direct' in v)
chim=max(abs(v['chi2_difference']) for v in comparisons if 'chi2_difference' in v)
passed=templmax<.01 and directmax<.01 and chim<.5 and mutation['los_relative_change']>.1 and mutation['hankel_relative_change']>.1
np.savez(a.cache,edge_grid=eg,table=tab,radii=rr)
result=dict(status='PASS' if passed else 'FAIL',max_fitted_template_refinement=templmax,max_fitted_direct_discrepancy=directmax,max_chi2_refinement=chim,comparisons=comparisons,actual_runtime_normalization_mutation=mutation,initial_control_note='controls_002 normalization_mutation_relative=1 was an algebraic identity, not an executed mutation. This separate runtime injection supplies the actual mutation evidence; initial fits preceded this supplementary verification.',elapsed_seconds=time.monotonic()-t)
Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('comparisons',)}))
