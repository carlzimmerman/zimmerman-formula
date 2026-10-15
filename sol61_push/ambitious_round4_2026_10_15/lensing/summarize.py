import argparse,json,csv,platform
from model import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);root=out.parent
read=lambda run:json.loads((BASE/run/'result.json').read_text())
r,y,c=data();ref=read('refinement_001');fits={v['model']:v['refined_fit'] for v in ref['comparisons'] if 'refined_fit' in v};ex=read('extended_profile_001');common=read('common_size_001');fixed=read('fixed_size_20_001');noex=read('native_noexclusion_001');cache=np.load(BASE/'refinement_001/projection_cache.npz')
invariance=[]
for label,finite in [('B',False),('D',True)]:
    old=Fitter(cache['edge_grid'],cache['table'],finite);scaled=Fitter(cache['edge_grid'],2*cache['table'],finite)
    rr,*_,bb,_=old.predict(fits[label]['logMb']);sr,*_,sb,_=scaled.predict(fits[label]['logMb'])
    invariance.append(dict(model=label,chi2_difference=float(sr@sr-rr@rr),max_doubled_bias_discrepancy=float(abs(2*sb-bb).max())))
blocks={};csvrows=[];models={'B':fits['B'],'D':fits['D'],'Plummer_4_sizes':ex,'Plummer_common_size':common,'Plummer_fixed_20kpc':fixed}
for name,fit in models.items():
    pred=np.array(fit['predictions']).ravel();raw=y.ravel()-pred;pr=np.linalg.solve(c,raw);wh=solve_triangular(np.linalg.cholesky(c),raw,lower=True);inv=np.linalg.inv(c);cond=pr/np.sqrt(np.diag(inv))
    signed=[float(raw[15*b:15*(b+1)]@pr[15*b:15*(b+1)]) for b in range(4)];increments=[]
    for b in range(4):
        rest=np.array([i for i in range(60) if i//15!=b]);increments.append(float(raw@pr-raw[rest]@np.linalg.solve(c[np.ix_(rest,rest)],raw[rest])))
    blocks[name]=dict(chi2=float(raw@pr),signed_additive_bin_chi2=signed,signed_partition_sum=float(sum(signed)),nonadditive_conditional_bin_chi2=increments,whitened_residuals=wh.tolist(),precision_residuals=pr.tolist(),conditional_pulls=cond.reshape(4,15).tolist())
    for b in range(4):
        for i in range(15):
            k=b*15+i;csvrows.append(dict(model=name,bin=b+1,radius_physical_Mpc=r[b,i],observed_ESD=y[b,i],marginal_sigma=math.sqrt(c[k,k]),prediction=pred[k],residual=raw[k],conditional_pull=cond[k],Cholesky_whitened_residual=wh[k],precision_times_residual=pr[k]))
with (root/'predictions_residuals.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(csvrows[0]));w.writeheader();w.writerows(csvrows)
np.savetxt(root/'full_covariance.csv',c,delimiter=',')
mutation=(np.array(noex['models']['D']['biases'])/np.array(fits['D']['biases'])-1)*100
result=dict(baseline_native_h=dict(chi2_B=fits['B']['chi2'],chi2_D=fits['D']['chi2'],dchi2=fits['D']['chi2']-fits['B']['chi2'],D_nominal_p=fits['D']['nominal_p'],relative_gate=True,absolute_gate=False),covariance=covariance_diagnostics(c),radial_arrays_identical=bool(np.array_equal(r,np.tile(r[0],(4,1)))),amplitude_invariance=invariance,exclusion_mutation_D_bias_change_percent=mutation.tolist(),exclusion_mutation_gate=bool(max(abs(mutation))>10),blocks=blocks,verdict='Numerical projection and tested optimization validated; primary finite catchment fails absolute goodness of fit. Self-consistent Plummer source substantially improves fit but fixed/common/four-size diagnostics all miss p>=.01. No empirical or full physical closure.',software_extra=dict(matplotlib=matplotlib.__version__),post_data=True)
out.write_text(json.dumps(result,indent=2)+'\n')
fig,axes=plt.subplots(2,4,figsize=(16,7),sharex='col');colors={'D':'#be4e4e','Plummer_4_sizes':'#167d8d','B':'#777777'}
for b in range(4):
    ax=axes[0,b];ax.errorbar(r[b],y[b],np.sqrt(np.diag(c))[b*15:(b+1)*15],fmt='o',ms=3,color='black',label='KiDS stack')
    for name in ('B','D','Plummer_4_sizes'):
        ax.plot(r[b],models[name]['predictions'][b],label=name.replace('_',' '),color=colors[name]);axes[1,b].plot(r[b],blocks[name]['conditional_pulls'][b],marker='.',color=colors[name],label=name)
    ax.set(xscale='log',yscale='log',title=f'Mass bin {b+1}',ylim=(.08,220));axes[1,b].set(xscale='log',xlabel='R [physical Mpc]',ylim=(-5,4));axes[1,b].axhline(0,color='black',lw=.7)
    for k in (-2,2):axes[1,b].axhline(k,color='#999999',lw=.5,ls=':')
axes[0,0].set_ylabel('DeltaSigma [Msun / pc²]');axes[1,0].set_ylabel('Conditional residual pull');axes[0,0].legend(fontsize=8)
fig.suptitle('Post-data finite catchment test: extended baryon sources improve shape, absolute fit still fails',fontsize=12);fig.tight_layout();fig.savefig(root/'profile_comparison.png',dpi=160);plt.close(fig)
print(json.dumps({k:v for k,v in result.items() if k!='blocks'}))
