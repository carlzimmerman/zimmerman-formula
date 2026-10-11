"""Finite exact circular-profile relaxation, not a candidate-B fit or verdict."""
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
PREV=HERE.parent/'native_lensing_2026_10_11/run_v2'


def project(coords, origin):
    a,d=np.deg2rad(np.asarray(coords)).T
    a0,d0=np.deg2rad(origin)
    da=a-a0
    den=np.sin(d0)*np.sin(d)+np.cos(d0)*np.cos(d)*np.cos(da)
    return np.column_stack((np.cos(d)*np.sin(da), np.cos(d0)*np.sin(d)-np.sin(d0)*np.cos(d)*np.cos(da)))/den[:,None]*206264.80624709636


def contrasts(rows):
    features=sorted({r['feature'] for r in rows})
    H=np.zeros((len(rows)-len(features),len(rows)))
    off=0
    for f in features:
        ids=sorted([i for i,r in enumerate(rows) if r['feature']==f],key=lambda i:rows[i]['id'])
        for k in range(1,len(ids)):
            H[off,ids[:k]]=1/math.sqrt(k*(k+1))
            H[off,ids[k]]=-k/math.sqrt(k*(k+1))
            off+=1
    return H


def circular_operator(theta,centres):
    blocks=[]; records=[]
    max_annulus_error=0.
    for ctr in centres:
        dx=theta-ctr
        radii=np.linalg.norm(dx,axis=1)
        if np.any(radii<=0): raise ValueError('Image at a halo centre')
        rr,rank=np.unique(radii,return_inverse=True)
        incidence=(rank[:,None]>=np.arange(len(rr))[None,:]).astype(float)
        # Independent realization: uniform projected annuli lying strictly between probes.
        lower=np.r_[0.,rr[:-1]]
        rin=lower+.25*(rr-lower)
        rout=lower+.75*(rr-lower)
        enclosed=np.clip((radii[:,None]**2-rin[None,:]**2)/(rout[None,:]**2-rin[None,:]**2),0,1)
        max_annulus_error=max(max_annulus_error,float(np.max(np.abs(enclosed-incidence))))
        blocks.append(dx[:,:,None]/radii[:,None,None]**2*incidence[:,None,:])
        records.append(dict(centre=ctr.tolist(),radii=rr.tolist(),rin=rin.tolist(),rout=rout.tolist()))
    return np.concatenate(blocks,axis=2),records,max_annulus_error


def effective(K,H,w):
    return np.einsum('fi,icj->fcj',H,w[:,None,None]*K).reshape(2*len(H),K.shape[2])


def solve(A,b,tolerance=1e-9):
    m,n=A.shape
    ub=np.vstack((np.c_[A,-np.ones(m)],np.c_[-A,-np.ones(m)]))
    rhs=np.r_[b,-b]
    opts=dict(primal_feasibility_tolerance=tolerance,dual_feasibility_tolerance=tolerance)
    fit=linprog(np.r_[np.zeros(n),1.],A_ub=ub,b_ub=rhs,bounds=(0,None),method='highs',options=opts)
    if not fit.success: raise RuntimeError(fit.message)
    x,t=fit.x[:-1],float(fit.x[-1])
    dual=fit.ineqlin.marginals[:m]-fit.ineqlin.marginals[m:]
    # y obeys A^T y<=0 and ||y||_1<=1; b.y is a lower bound on minimax residual.
    residual=A@x-b
    dual_value=float(b@dual)
    cap=t+1e-7
    mass=linprog(np.ones(n),A_ub=np.vstack((A,-A)),b_ub=np.r_[b+cap,-b+cap],
                 bounds=(0,None),method='highs',options=opts)
    if not mass.success: raise RuntimeError(mass.message)
    result=dict(t_min_arcsec=t,primal_violation=float(max(0,np.max(np.abs(residual))-t)),
                dual_column_violation=float(max(0,np.max(A.T@dual))),dual_l1=float(np.sum(np.abs(dual))),
                dual_lower_bound_arcsec=dual_value,duality_gap=float(t-dual_value),
                angular_mass=float(mass.fun),mass_solution_residual=float(np.max(np.abs(A@mass.x-b))),
                n_variables=n,n_constraints=m,tolerance=tolerance,
                positive_annuli=int(np.sum(mass.x>1e-9)))
    return result,mass.x,dual


def efficiency(z,Om,tol=1e-11):
    chi=lambda zz:quad(lambda t:1/math.sqrt(Om*(1+t)**3+1-Om),0,zz,epsabs=tol,epsrel=tol)[0]
    return 1-chi(.296)/chi(z)


def main():
    checks=[]
    def ck(name,ok,value=None): checks.append(dict(name=name,passed=bool(ok),value=value))
    prior=json.loads((PREV/'results.json').read_text())
    rows=prior['gold_rows']; origin=prior['tangent_origin_degrees']
    theta=project([[r['ra'],r['dec']] for r in rows],origin)
    H=contrasts(rows); b=(H@theta).reshape(-1)
    author={s.split()[0]:s.split() for s in (HERE/'sources/bullet_gold_v4.dat').read_text().splitlines() if s.strip() and not s.startswith('#')}
    ck('author_gold_ID_match',set(author)=={r['id'] for r in rows})
    ck('author_gold_position_z_match',all(abs(float(author[r['id']][1])-r['ra'])<=1e-6 and
       abs(float(author[r['id']][2])-r['dec'])<=1e-6 and abs(float(author[r['id']][6])-r['zsys'])<1e-10 for r in rows))
    members={int(s.split()[0]):[float(x) for x in s.split()[1:5]] for s in (HERE/'sources/cluster_members_specz_cat.dat').read_text().splitlines() if s.strip() and not s.startswith('#')}
    local=project([members[i][:2] for i in (1,3,4)],members[1][:2])
    observed=local[1:]*np.array([-1,1])
    reported=np.array([[24.04+.02,29.13+.03],[186.08+.02,49.62+.03]])
    ctrerr=float(np.max(np.abs(observed-reported)))
    ck('BCG_relative_astrometry',ctrerr<.15,ctrerr)
    # Point lens benchmark and sign/efficiency mutants.
    mass_true=1.2; w0=.7; beta=.3
    root=math.sqrt(beta**2+4*w0*mass_true)
    pts=np.array([[(beta+root)/2,0],[(beta-root)/2,0]])
    hs=np.array([[1,-1]])/math.sqrt(2)
    ks,_,annerr=circular_operator(pts,np.zeros((1,2)))
    aa=effective(ks,hs,np.full(2,w0)); bb=(hs@pts).reshape(-1)
    syn,_,_=solve(aa,bb)
    exact=linprog(np.ones(aa.shape[1]),A_eq=aa,b_eq=bb,bounds=(0,None),method='highs')
    ck('point_lens_minimax',syn['t_min_arcsec']<1e-10)
    ck('point_lens_minimum_mass',exact.success and abs(exact.fun-mass_true)<1e-7,float(exact.fun))
    xtrue=np.zeros(ks.shape[2]); xtrue[0]=mass_true
    ck('MUTATE_sign_rejected',np.max(np.abs(-aa@xtrue-bb))>.1)
    ck('MUTATE_omit_efficiency_rejected',np.max(np.abs(effective(ks,hs,np.ones(2))@xtrue-bb))>.1)
    pp=[]; ww=[]; rh=[]
    for i,w in enumerate((.4,.65,.9)):
        be=.2+.1*i; rr=math.sqrt(be**2+4*w*mass_true)
        pp.extend([[(be+rr)/2,0],[(be-rr)/2,0]]); ww.extend([w,w])
        rh.extend([dict(feature=str(i),id=str(i)+'a'),dict(feature=str(i),id=str(i)+'b')])
    pp=np.array(pp); hh=contrasts(rh); kk,_,_=circular_operator(pp,np.zeros((1,2)))
    multi,_,_=solve(effective(kk,hh,np.array(ww)),(hh@pp).reshape(-1))
    ck('multi_efficiency_point_lens',multi['t_min_arcsec']<1e-10)
    outputs=[]; arrays={}
    backgrounds={'native_PM_flat':(.02237+.1200)/.6736**2,'author_context_flat':.3}
    for bg,Om in backgrounds.items():
        w=np.array([efficiency(r['zsys'],Om) for r in rows])
        wt=np.array([efficiency(r['zsys'],Om,1e-13) for r in rows])
        ck('distance_refinement_'+bg,np.max(np.abs(w-wt))<1e-10,float(np.max(np.abs(w-wt))))
        ck('physical_efficiency_'+bg,np.all((w>0)&(w<1)))
        for name,ids in [('three_BCG',[1,3,4]),('six_galaxies',[1,3,4,5,9,10])]:
            centres=project([members[i][:2] for i in ids],origin)
            K,annuli,err=circular_operator(theta,centres)
            ck('exact_annulus_realization_'+bg+'_'+name,err<1e-10,err)
            A=effective(K,H,w)
            sols=[]
            for tol in (1e-9,1e-10):
                res,x,y=solve(A,b,tol)
                ck('LP_primal_dual_%s_%s_%s'%(bg,name,tol),res['primal_violation']<=1e-6 and
                   res['dual_column_violation']<=1e-7 and res['dual_l1']<=1+1e-7 and
                   abs(res['duality_gap'])<=1e-6*max(1,res['t_min_arcsec']) and
                   res['mass_solution_residual']<=res['t_min_arcsec']+1e-7+1e-6,res)
                sols.append(res)
                if tol==1e-10:
                    key=bg+'_'+name
                    arrays[key+'_A']=A; arrays[key+'_x']=x; arrays[key+'_dual']=y
            ck('solver_refinement_'+bg+'_'+name,abs(sols[0]['t_min_arcsec']-sols[1]['t_min_arcsec'])<1e-6)
            Hr=contrasts(rows[::-1]); Kr,_,_=circular_operator(theta[::-1],centres)
            rev,_,_=solve(effective(Kr,Hr,w[::-1]),(Hr@theta[::-1]).reshape(-1),1e-10)
            ck('order_invariance_'+bg+'_'+name,abs(rev['t_min_arcsec']-sols[-1]['t_min_arcsec'])<1e-6)
            outputs.append(dict(background=bg,Omega_m=Om,geometry=name,member_ids=ids,annuli=annuli,solves=sols))
    out=HERE/'run'
    report=dict(status='conditional_round_total_mass_relaxation_not_theory_verdict',
                passed=sum(c['passed'] for c in checks),total=len(checks),checks=checks,cells=outputs,
                mass_unit='arcsec^2 coefficient: 4GM/(c^2 D_l) times radians_to_arcsec^2')
    (out/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    np.savez_compressed(out/'certificates.npz',b=b,theta_arcsec=theta,**arrays)
    print('%d/%d checks'%(report['passed'],report['total']))
    for cell in outputs:
        print(cell['background'],cell['geometry'],json.dumps(cell['solves'][-1]))
    assert all(c['passed'] for c in checks)

if __name__=='__main__': main()
