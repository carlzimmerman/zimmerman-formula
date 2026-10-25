"""Marginal-error bounds, not a substituted correlated posterior."""
import argparse,csv,json,os,importlib.util
from pathlib import Path
import numpy as np
from astropy.io import fits
from scipy.optimize import brentq

spec=importlib.util.spec_from_file_location('inv','reviews/cold_field_inversion_2026_10_24/invert.py')
inv=importlib.util.module_from_spec(spec); spec.loader.exec_module(inv)
b=inv.base; G,MSUN,PC=b.G,b.MSUN,b.PC
X=np.array([.1,.2,.3,.5,.7,1.])
SELECTIVE=False

def lint(r,y,x): return np.interp(np.log(x),np.log(r),y)
def mint(r,m,x): return np.array([b.loginterp(r,m,v) for v in x])
def lawmass(B,A): return .5*(B+np.sqrt(B*B+4*A*B))
def cold(h,gas,star,A):
    return h-lawmass(gas+star,A) if SELECTIVE else h*h/(h+A)-gas-star

def read(name,mutate=False):
    p=Path('real_research/data/xcop')/name
    with fits.open(p/f'{name}_hydro_mass.fits') as f:
        h=f[1].data.copy(); r500=f[1].header['R500']
    with fits.open(p/f'{name}_fgas_profile.fits') as f:
        gas=f[1].data.copy(); gr500=f[1].header['R500']
    with fits.open(p/f'{name}_mstar.fits') as f: star=f[2].data.copy()
    r=X*r500; hs=mint(h['RADIUS'],h['M_FORW'],r); he=lint(h['RADIUS'],h['EM_FORW'],r)
    gs=mint(gas['RADIUS']*gr500,gas['MGAS'],r)
    ge=np.array([lint(gas['RADIUS']*gr500,gas[k],r) for k in ['MGAS_LO','MGAS_HI']]).T
    ss=mint(star['RADIUS'],star['MSTAR'],r)
    slo=mint(star['RADIUS'],star['MSTAR_LO'],r); shi=mint(star['RADIUS'],star['MSTAR_HI'],r)
    se=np.stack([ss-slo,shi-ss],axis=1)
    if mutate: se=np.stack([slo,shi],axis=1)
    assert np.allclose(se[:,0]+slo,ss,rtol=1e-12), 'stellar bound/error schema identity failed'
    assert np.allclose(shi-se[:,1],ss,rtol=1e-12)
    assert np.all(ge>0) and np.all(se>0) and np.all(he>0)
    models={k:mint(h['RADIUS'],h[k],r) for k in ['M_FORW','M_NFW','M_EIN','M_ISO','M_BUR']}
    return dict(name=name,r=r*1000*PC,h=hs,gas=gs,star=ss,he=he,ge=ge,se=se,models=models)

def bounds(d,A,t,hydro_only=False):
    h,g,s=d['h'],d['gas'],d['star']; he,ge,se=d['he'],d['ge'],d['se']
    if hydro_only: ge=np.zeros_like(ge); se=np.zeros_like(se)
    lo=cold(np.maximum(h-t*he,0),g+t*ge[:,1],s+t*se[:,1],A)
    hi=cold(h+t*he,np.maximum(g-t*ge[:,0],0),np.maximum(s-t*se[:,0],0),A)
    return lo,hi

def feasible(lo,hi):
    witness=np.maximum.accumulate(np.maximum(lo,0))
    return bool(np.all(witness<=hi+1e-12*np.maximum(abs(hi),1))),witness

def repair(d,A,hydro_only):
    def ok(t): return feasible(*bounds(d,A,t,hydro_only))[0]
    if ok(0): t=0.
    else:
        left,right=0.,1.
        while not ok(right): right*=2; assert right<1024
        for _ in range(60):
            mid=(left+right)/2
            if ok(mid): right=mid
            else: left=mid
        t=right
        assert not ok(max(t-1e-7,0))
    lo,hi=bounds(d,A,t+1e-9,hydro_only); passed,mc=feasible(lo,hi); assert passed
    result=dict(t=float(t),Mc_witness=mc.tolist())
    if hydro_only:
        source=mc+d['gas']+d['star']
        hh=mc+lawmass(d['gas']+d['star'],A) if SELECTIVE else .5*(source+np.sqrt(source**2+4*A*source))
        shifts=(hh-d['h'])/d['he']
        assert np.all(abs(shifts)<=t+1e-6)
        assert np.all(np.diff(mc)>=-1) and np.all(mc>=0)
        assert np.all(np.diff(hh)>=0)
        assert np.allclose(cold(hh,d['gas'],d['star'],A),mc,rtol=1e-11,atol=1)
        result.update(H_witness=hh.tolist(),H_shift_error_units=shifts.tolist(),H_fractional_shift=(hh/d['h']-1).tolist())
    return result

def controls():
    h,A=3.,2.; eps=1e-5
    f=lambda h:h*h/(h+A)
    assert np.isclose((f(h+eps)-f(h-eps))/(2*eps),h*(h+2*A)/(h+A)**2,rtol=1e-9)
    a=np.array([-2.,3.,-4.,1.]); C=np.outer(np.sign(a),np.sign(a))
    assert np.linalg.eigvalsh(C).min()>-1e-12
    assert np.isclose(a@C@a,np.sum(abs(a))**2)
    assert np.array([-2.,2.])@np.ones((2,2))@np.array([-2.,2.])==0
    assert feasible(np.array([1.,2.]),np.array([2.,3.]))[0]
    assert not feasible(np.array([3.,1.]),np.array([4.,2.]))[0]
    assert np.all(np.diff(np.array([1.,2.,3.]))>0)
    return ['mass derivative finite difference','PSD maximum-correlation extremizer','coherent common-error cancellation','positive interval feasibility','infeasible decreasing intervals','positive shell fixture','stellar error semantics','minimal repair bracket','hydro witness bounds and forward map','baseline reproduction']

def main():
    global SELECTIVE
    p=argparse.ArgumentParser(); p.add_argument('--selective',action='store_true'); p.add_argument('--output',required=True); p.add_argument('--mutate',action='store_true'); args=p.parse_args()
    SELECTIVE=args.selective
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    checks=controls();
    if SELECTIVE: checks[-1]='independent selective source and derivative identities'
    old=json.load(open('reviews/cold_field_inversion_2026_10_24/run/result.json'))
    names=sorted({r['name'] for r in old['footings']['canonical']['baseline']['radial']})
    result={'checks':checks,'coupling':'selective Newtonian cold' if SELECTIVE else 'additional AQUAL source','covariance_status':'joint posterior/covariance unavailable in inspected products','footings':{}}
    shellrows=[]; modelrows=[]; repairs=[]
    for footing,a0 in inv.FOOTINGS.items():
        result['footings'][footing]={}
        for name in names:
            d=read(name,args.mutate); A=a0*d['r']**2/(G*MSUN); mc=cold(d['h'],d['gas'],d['star'],A)
            prev=[r['cold_aqual_msun'] for r in old['footings'][footing]['baseline']['radial'] if r['name']==name]
            if not SELECTIVE: assert np.allclose(mc,prev,rtol=1e-11)
            else:
                gb=G*(d['gas']+d['star'])*MSUN/d['r']**2
                reference=d['h']-inv.forward(gb,a0)*d['r']**2/(G*MSUN)
                assert np.allclose(mc,reference,rtol=1e-11)
            deriv=d['h']*(d['h']+2*A)/(d['h']+A)**2
            db=np.ones_like(A)
            if SELECTIVE:
                deriv=np.ones_like(A); B=d['gas']+d['star']
                db=.5*(1+(B+2*A)/np.sqrt(B*B+4*A*B))
                eps=1e-5*B
                finite=(lawmass(B+eps,A)-lawmass(B-eps,A))/(2*eps)
                assert np.allclose(db,finite,rtol=1e-9)
            sigma=np.stack([deriv*d['he'],db*np.max(d['ge'],axis=1),db*np.max(d['se'],axis=1)],axis=1)
            ss=[]
            for i,delta in enumerate(np.diff(mc)):
                # Each component contributes outer minus inner with its physical sign.
                coeff=np.array([-sigma[i,0],sigma[i+1,0],sigma[i,1],-sigma[i+1,1],sigma[i,2],-sigma[i+1,2]])
                maximum=float(np.sum(abs(coeff))); minimum=float(max(0,2*np.max(abs(coeff))-maximum))
                independent=float(np.linalg.norm(coeff)); coherent=float(np.linalg.norm(coeff.reshape(3,2).sum(axis=1)))
                row=dict(footing=footing,name=name,inner_x=float(X[i]),outer_x=float(X[i+1]),delta_Msun=float(delta),sigma_min=minimum,sigma_max=maximum,sigma_independent=independent,sigma_coherent=coherent,negative_size_over_max_sigma=float(-delta/maximum) if delta<0 else 0)
                for t in [1,2,3]:
                    lo,hi=bounds(d,A,t)
                    row[f'box{t}_min']=float(lo[i+1]-hi[i]); row[f'box{t}_max']=float(hi[i+1]-lo[i])
                ss.append(row); shellrows.append(row)
            rh=repair(d,A,True); ra=repair(d,A,False)
            repairs.append(dict(footing=footing,name=name,hydro_only_t=rh['t'],all_marginal_box_t=ra['t']))
            mm=[]
            for model,h in d['models'].items():
                c=cold(h,d['gas'],d['star'],A); q=c/d['gas']
                rr=dict(footing=footing,name=name,model=model,negative_shells=int(np.sum(np.diff(c)<0)),negative_enclosed=int(np.sum(c<0)),Q_inner=float(q[0]),Q_outer=float(q[-1]),Mc=c.tolist())
                mm.append(rr); modelrows.append({k:v for k,v in rr.items() if k!='Mc'})
            result['footings'][footing][name]=dict(shells=ss,hydro_only_repair=rh,all_box_relaxation=ra,models=mm)
            if SELECTIVE:
                # Existing candidate's imposed eta, not selected by this audit.
                eta=1500*PC*1000
                vc=np.sqrt(G*MSUN*(d['gas']+d['star']+mc)/d['r'])
                ratio=(eta/(d['r']*vc))**2
                result['footings'][footing][name]['wave_scale_diagnostic']={
                    'eta_pc_kms':1500,'smooth_gradient_to_gravity_ratio':ratio.tolist(),
                    'eta_over_v_pc':(eta/vc/PC).tolist(),
                    'coherent_selfgravity_length_pc':float(eta**2/(G*mc[-1]*MSUN)/PC),
                    'scope':'smooth gradients on r; not arbitrary excited-mode stress'}
    summary={}
    for footing,cells in result['footings'].items():
        ss=[s for c in cells.values() for s in c['shells']]; neg=[s for s in ss if s['delta_Msun']<0]
        summary[footing]=dict(negative_shells=len(neg),negative_at_all_box1_corners=sum(s['box1_max']<0 for s in neg),negative_at_all_box2_corners=sum(s['box2_max']<0 for s in neg),negative_at_all_box3_corners=sum(s['box3_max']<0 for s in neg),negative_size_over_max_sigma=[s['negative_size_over_max_sigma'] for s in neg],hydro_only_repair_t={n:c['hydro_only_repair']['t'] for n,c in cells.items()},all_box_t={n:c['all_box_relaxation']['t'] for n,c in cells.items()},model_negative_shells={m:sum(x['negative_shells'] for x in modelrows if x['footing']==footing and x['model']==m) for m in d['models']})
    result['summary']=summary
    (out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    b.write_csv(out/'shell_bounds.csv',shellrows); b.write_csv(out/'model_sensitivity.csv',modelrows); b.write_csv(out/'repair_sizes.csv',repairs)
    os.environ.setdefault('MPLCONFIGDIR','/tmp/matched_clumping_mpl')
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(9,5),layout='constrained')
    neg=[r for r in shellrows if r['footing']=='canonical' and r['delta_Msun']<0]
    y=np.arange(len(neg)); val=np.array([r['delta_Msun'] for r in neg])/1e13
    ax.errorbar(val,y,xerr=np.array([r['sigma_max'] for r in neg])/1e13,fmt='o',label='Central value ± maximum linear width')
    for i,r in enumerate(neg): ax.plot([r['box1_min']/1e13,r['box1_max']/1e13],[i+.15,i+.15],color='tab:orange',lw=3)
    ax.plot([],[],color='tab:orange',lw=3,label='Exact ±1 marginal-width box envelope')
    ax.axvline(0,color='black',ls='--'); ax.set_yticks(y,[f"{r['name']}  {r['inner_x']}–{r['outer_x']} R500" for r in neg])
    ax.set(xlabel=r'Added-source shell mass [$10^{13} M_\odot$]',title=('Selective cold' if SELECTIVE else 'AQUAL source')+': canonical sensitivity, not confidence intervals')
    ax.legend(fontsize=8); fig.savefig(out/'shell_uncertainty.png',dpi=180)
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
