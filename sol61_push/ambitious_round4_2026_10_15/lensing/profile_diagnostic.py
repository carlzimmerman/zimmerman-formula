"""Post-data falsifiers of linked normalization versus fixed radial shape.
Environmental edge fixed at already fitted D, no physical rescue claim.
"""
import argparse,json
from model import *
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--cache',required=True);p.add_argument('--fit',required=True);a=p.parse_args()
r,y,c=data();chol=np.linalg.cholesky(c);wy=solve_triangular(chol,y.ravel(),lower=True)
cache=np.load(a.cache);eg=cache['edge_grid'];tab=cache['table'];prior=json.loads(Path(a.fit).read_text());d=next(v['refined_fit'] for v in prior['comparisons'] if v.get('model')=='D' and 'refined_fit' in v)
f=Fitter(eg,tab,True);_,ov,tv,bb,edges=f.predict(d['logMb'])

def diagnose(label,design,names):
    wd=solve_triangular(chol,design,lower=True);v,_=nnls(wd,wy);pred=design@v;raw=y.ravel()-pred;wh=solve_triangular(chol,raw,lower=True);pr=np.linalg.solve(c,raw);inv=np.linalg.inv(c)
    return dict(label=label,chi2=float(wh@wh),nominal_dof=48,nominal_p=float(chi2.sf(wh@wh,48)),coefficients=v.reshape(4,3).tolist(),coefficient_order=names,predictions=pred.reshape(4,15).tolist(),residuals=raw.reshape(4,15).tolist(),conditional_pulls=(pr/np.sqrt(np.diag(inv))).reshape(4,15).tolist(),signed_additive_bin_chi2=[float(raw[b*15:(b+1)*15]@pr[b*15:(b+1)*15]) for b in range(4)],chi2_improvement_over_D=d['chi2']-float(wh@wh))

exact=np.zeros((60,12));asym=np.zeros((60,12))
for b,lm in enumerate(d['logMb']):
    sl=slice(15*b,15*(b+1));point=10**lm/(np.pi*(r[b]*1e6)**2)
    exact[sl,3*b]=point;exact[sl,3*b+1]=ov[sl]-point;exact[sl,3*b+2]=tv[sl,b]
    asym[sl,3*b]=1e11/(np.pi*(r[b]*1e6)**2);asym[sl,3*b+1]=1/r[b];asym[sl,3*b+2]=tv[sl,b]
linked=diagnose('Independent nonnegative point and finite-excess normalization; radial shape and environment edge fixed at fitted D',exact,['point_multiplier','finite_excess_multiplier','bias'])
power=diagnose('Independent nonnegative point plus 1/R amplitude; environment edge fixed at fitted D',asym,['point_mass_in_1e11_Msun','ESD_1overR_at_1Mpc','bias'])
# Shape-focused inexpensive falsifier: r_i^2 DeltaSigma decreases iff the
# spherical? This implication is not universal; do not assert it. Instead
# report observed conditional pulls and broad radial groups exactly.
groups={}
for label,fit in [('D',d),('independent_point_excess',linked),('point_plus_1overR',power)]:
    residual=np.array(fit['residuals']).ravel();pr=np.linalg.solve(c,residual)
    groups[label]={}
    for key,mask in [('inner_R_le_0p12',r.ravel()<=.12),('intermediate_0p12_to_0p76',(r.ravel()>.12)&(r.ravel()<=.76)),('outer_R_gt_0p76',r.ravel()>.76)]:
        take=np.flatnonzero(mask);rest=np.flatnonzero(~mask)
        groups[label][key]=dict(signed_additive_chi2=float(residual[take]@pr[take]),nonadditive_conditional_increment=float(residual@pr-residual[rest]@np.linalg.solve(c[np.ix_(rest,rest)],residual[rest])),mean_residual=float(residual[take].mean()))
result=dict(post_data=True,fixed_edges=edges,baseline_D_chi2=d['chi2'],diagnostics=[linked,power],radial_covariance_diagnostics=groups,scope='Diagnostic relaxation only: fixed environmental edges and density shape from fitted D, 12 linear nonnegative coefficients. Nominal p uses n-12 without boundary calibration. Does not identify gas, alter original criteria, or supply a physical profile.')
Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
for v in (linked,power):print(json.dumps({k:v[k] for k in ('label','chi2','nominal_p','coefficients','coefficient_order','chi2_improvement_over_D')}))
