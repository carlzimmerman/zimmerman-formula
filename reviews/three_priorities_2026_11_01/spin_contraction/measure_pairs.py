#!/usr/bin/env python3
"""TP01-SC: independent snapshot reduction; writes only the supplied output directory."""
import os
for _k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_k]='1'
import itertools, json, math, pathlib, resource, sys, time
import numpy as np
from scipy.stats import rankdata

ROOT=pathlib.Path(__file__).resolve().parents[3]
RB=ROOT/'rebuild_2026_10_22'
OUT=pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True,exist_ok=True)
G=4.30091e-9
AG=np.geomspace(.5,60,2001); CG=np.linspace(1,30,581)
BS=lambda x:4*(np.arcsinh(x)-x/np.sqrt(1+x*x))
MU=lambda x:np.log1p(x)-x/(1+x)

def centre(x):
    c=x.mean(0); radius=np.linalg.norm(x-c,axis=1).max()
    while True:
        sel=np.linalg.norm(x-c,axis=1)<radius
        if sel.sum()<100:return c
        c=x[sel].mean(0);radius*=.8

def load(path):
    with np.load(path,allow_pickle=False) as z:
        return z['x'].copy(),z['v'].copy(),float(z['m']),json.loads(str(z['meta']))

def profile(x,m,rho,eps,do_fit=True):
    cen=centre(x);r=np.sort(np.linalg.norm(x-cen,axis=1));n=np.arange(1,len(r)+1)
    ii=np.where(n*m/(4/3*math.pi*r**3)>=18*math.pi**2*rho)[0]
    assert len(ii)>0
    rv=float(r[ii.max()]);rc=max(3*eps,float(r[min(199,len(r)-1)]))
    assert rc<rv/2
    sel=(r>=rc)&(r<=rv);u=r[sel]/rv;y=np.log(n[sel]*m/(n[sel][-1]*m))
    if not do_fit:return dict(centre=cen,r=r,rvir=rv,rconv=rc)
    # Literal discrete objective and grids, independently implemented.
    obj=lambda a:float(np.sum((np.log(BS(a*u)/BS(a))-y)**2))
    a=float(min(AG,key=obj));c=float(min(CG,key=lambda q:float(np.sum((np.log(MU(q*u)/MU(q))-y)**2))))
    eta=4/3*a*a/BS(a);S=eta*18*math.pi**2*rho*rv
    return dict(centre=cen,r=r,rvir=rv,rconv=rc,a=a,c=c,eta=float(eta),S=float(S),nvir=int((r<=rv).sum()),fit_n=int(sel.sum()))

def spin(x,v,m,rv,cen=None,mask=None):
    d=x-(centre(x) if cen is None else cen);rr=np.linalg.norm(d,axis=1);k=rr<rv if mask is None else mask;mv=m*k.sum();vc=v[k].mean(0)
    J=m*np.cross(d[k],v[k]-vc).sum(0);V=math.sqrt(G*mv/rv)
    return float(np.linalg.norm(J)/(math.sqrt(2)*mv*V*rv))

def contract(r,Mb,M0,F):
    lr=np.log(r);rf=r.copy()
    for _ in range(100):
        bm=np.interp(np.log(np.maximum(rf,r[0])),lr,Mb,left=Mb[0],right=Mb[-1])
        rn=r*M0*(1+F)/np.maximum(bm+M0,1e-300);rf=.5*(rf+rn)
    cv=float(np.max(np.abs(rn/rf-1)));rf=np.maximum.accumulate(rf)
    return np.interp(lr,np.log(rf),M0,left=0,right=M0[-1]),cv

def rho_from(meta,z):return meta['Mf']/(4/3*math.pi*meta['qM']**3)*(1+z)**3

def corr(x,y):
    a=rankdata(x);b=rankdata(y);a-=a.mean();b-=b.mean()
    den=math.sqrt(float(a@a)*float(b@b))
    return float(a@b/den) if den else float('nan')

def exact_corr(x,y):
    n=len(x);a=rankdata(x);b=rankdata(y);a-=a.mean();b-=b.mean();den=math.sqrt(float(a@a)*float(b@b));observed=float(a@b/den)
    count=0;total=0;it=iter(itertools.permutations(range(n)))
    while True:
        block=list(itertools.islice(it,8192))
        if not block:break
        vals=b[np.array(block)]@a/den;count+=int((np.abs(vals)>=abs(observed)-1e-12).sum());total+=len(block)
    loo=[corr(np.delete(x,i),np.delete(y,i)) for i in range(n)]
    return dict(rho=observed,p_exact=count/total,extreme=count,permutations=total,loo_range=[min(loo),max(loo)],loo=loo)

def loo_predict(y,features):
    y=np.asarray(y);X=np.column_stack([np.ones(len(y))]+[np.asarray(f) for f in features]);pred=[];base=[]
    for i in range(len(y)):
        k=np.arange(len(y))!=i;coef=np.linalg.lstsq(X[k],y[k],rcond=None)[0];pred.append(float(X[i]@coef));base.append(float(y[k].mean()))
    sse=float(np.sum((y-np.array(pred))**2));sb=float(np.sum((y-np.array(base))**2))
    return dict(pred=pred,sse=sse,baseline_sse=sb,skill=1-sse/sb,rmse=math.sqrt(sse/len(y)))

def main():
    start=time.monotonic();old=json.load(open(RB/'LC1_live_contraction/lc1_results.json'));oldspin=json.load(open(RB/'HS1_hsb_lsb_residual_slope/hs1_spin.json'))['table']['1e12']
    rows=[];checks={};maxfq=maxrl=maxspin=maxc=0.
    for seed in range(1,10):
        tag=f'M1e12_s{seed}_ng64'
        x,v,m,meta=load(RB/'X48_native_cf_zoom/runs'/tag/'snap_zf.npz')
        xn,vn,mn,mnmeta=load(RB/'ZN1_zooms_to_z0/runs'/tag/'snap_z0.00.npz')
        xd,vd,md,mdmeta=load(RB/'LC1_live_contraction/runs'/tag/'snap_z0.00.npz')
        for key in ('M','seed','ng','N','eps','zf','Mf','qM'):
            assert meta[key]==mnmeta[key]==mdmeta[key],(seed,key)
        assert len(x)==len(xn)==len(xd)==meta['N'] and m==mn==md
        p0=profile(x,m,rho_from(meta,meta['zf']),meta['eps']);pn=profile(xn,m,rho_from(meta,0),meta['eps'])
        Md=mdmeta['Md_now'];Msim=m*len(x);f=Md/Msim;Rd=mdmeta['lc1']['Rd_kpc']*.001
        pd=profile(xd,m*(1-f),rho_from(meta,0),meta['eps'])
        lam=spin(x,v,m,p0['rvir']);oldsp=next(q for q in oldspin if q['seed']==seed)
        maxspin=max(maxspin,abs(lam/oldsp['lam']-1));maxc=max(maxc,abs(p0['c']-oldsp['c']))
        rr0=np.linalg.norm(x-p0['centre'],axis=1);ki=rr0<.1*p0['rvir'];L=np.cross(x[ki]-p0['centre'],v[ki]-v[ki].mean(0)).sum(0);axis=L/np.linalg.norm(L)
        axiserr=float(np.max(np.abs(axis-np.array(mdmeta['lc1']['axis']))));assert axiserr<1e-12
        rr=np.array([1,2,3,4,6,8,10])*Rd;Q=np.searchsorted(pd['r'],rr)/np.searchsorted(pn['r'],rr)
        rhoc=3*(100*.6856427)**2/(8*math.pi*G);d=np.arange(1,len(xn)+1)*m/(4/3*math.pi*pn['r']**3);R200=float(pn['r'][np.where(d>=200*rhoc)[0].max()])
        rg=np.geomspace(1e-5,float(pn['r'][-1]),6000);M0=(1-f)*m*np.searchsorted(pn['r'],rg);Mb=Md*(1-Rd/np.sqrt(rg*rg+Rd*Rd));Mf,cv=contract(rg,Mb,M0,Md/(Msim-Md));QB=np.interp(np.log(rr),np.log(rg),Mf)/np.interp(np.log(rr),np.log(rg),M0)
        fq=float(np.median((Q[1:4]-1)/(QB[1:4]-1)));Rlive=pd['S']/pn['S'];ref=old['pairs']['0.00'][tag]
        maxfq=max(maxfq,abs(fq/ref['f_Q']-1));maxrl=max(maxrl,abs(Rlive/ref['R_live']-1))
        row=dict(seed=seed,spin=lam,pre_c=p0['c'],pre_S=p0['S'],pre_eta=p0['eta'],pre_rvir=p0['rvir'],pre_fit_n=p0['fit_n'],pre_rconv=p0['rconv'],no_S=pn['S'],disc_S=pd['S'],no_c=pn['c'],disc_c=pd['c'],R_live=Rlive,f_Q=fq,Q=Q.tolist(),QB=QB.tolist(),R200_no=R200,axis_error=axiserr,contract_conv=cv,N=len(x),Md=Md,Rd_Mpc=Rd,eps=meta['eps'],disc_fit_n=pd['fit_n'])
        rows.append(row);print(f'seed {seed} spin {lam:.6f} c_pre {p0["c"]:.2f} fQ {fq:.4f} Rlive {Rlive:.4f}',flush=True)
        if seed==1:
            rot=np.array([[0,-1,0],[1,0,0],[0,0,1.]])
            shift=np.array([.7,-.4,.2]);boost=np.array([77.,-33.,12.]);xx=x@rot.T+shift;vv=v@rot.T+boost
            lt_adaptive=spin(xx,vv,m,p0['rvir'])
            kk=np.linalg.norm(x-p0['centre'],axis=1)<p0['rvir']
            lt=spin(xx,vv,m,p0['rvir'],cen=p0['centre']@rot.T+shift,mask=kk)
            checks['spin_rigid_motion_relative_error']=abs(lt/lam-1)
            checks['spin_adaptive_boundary_motion_relative_error']=abs(lt_adaptive/lam-1)
            checks['adaptive_boundary_membership_difference']=int(np.sum(kk!=(np.linalg.norm(xx-centre(xx),axis=1)<p0['rvir'])))
            checks['zero_internal_velocity_spin']=spin(x,np.zeros_like(v),m,p0['rvir'])
    checks.update(fQ_reproduction_relative=maxfq,Rlive_reproduction_relative=maxrl,spin_reproduction_relative=maxspin,concentration_reproduction_absolute=maxc)
    r=np.geomspace(.001,1,1000);Mi=r*1e12;Mf,_=contract(r,np.zeros_like(r),Mi,0);checks['zero_baryon_identity_relative']=float(np.max(abs(Mf/Mi-1)))
    a=lambda k:np.array([q[k] for q in rows]);pairs=[('fQ_spin','f_Q','spin'),('fQ_concentration','f_Q','pre_c'),('preS_spin','pre_S','spin'),('noS_spin','no_S','spin'),('discS_spin','disc_S','spin'),('fQ_noS','f_Q','no_S')]
    stats={name:exact_corr(a(xk),a(yk)) for name,xk,yk in pairs};ordered=sorted(stats,key=lambda k:stats[k]['p_exact']);prev=0
    for i,key in enumerate(ordered):prev=max(prev,min(1,(len(ordered)-i)*stats[key]['p_exact']));stats[key]['p_holm']=prev
    xp=np.log10(a('pre_S'));xl=np.log10(a('spin'));xc=np.log10(a('pre_c'));yf=np.log10(a('disc_S'))
    models={'pre_S':[xp],'spin':[xl],'concentration':[xc],'pre_S_spin':[xp,xl],'pre_S_concentration':[xp,xc]}
    predictive={'log_final_S':{k:loo_predict(yf,v) for k,v in models.items()},'f_Q':{k:loo_predict(a('f_Q'),v) for k,v in {'spin':[xl],'concentration':[xc],'spin_concentration':[xl,xc]}.items()}}
    joint=np.log10(a('no_S'))+np.log10(a('R_live'));checks['joint_log_identity_max_abs']=float(np.max(abs(joint-yf)))
    perm=np.roll(a('R_live'),1);checks['permuted_joint_max_change_dex']=float(np.max(abs(np.log10(a('no_S')*perm)-yf)))
    good=(maxfq<1e-6 and maxrl<1e-6 and maxspin<1e-10 and maxc<1e-12 and checks['spin_rigid_motion_relative_error']<1e-8 and checks['zero_internal_velocity_spin']==0 and checks['zero_baryon_identity_relative']<1e-12 and checks['joint_log_identity_max_abs']<1e-12 and checks['permuted_joint_max_change_dex']>.01)
    result=dict(assertion_tested='nine aligned same-seed LC1 snapshot pairs; measured joint response and finite association',n=len(rows),rows=rows,statistics=stats,predictive=predictive,checks=checks,controls_pass=good,medians={k:float(np.median(a(k))) for k in ('spin','pre_c','f_Q','R_live')},scatter_dex={k:float(np.std(np.log10(a(k)),ddof=1)) for k in ('pre_S','no_S','disc_S')},runtime_seconds=time.monotonic()-start,maxrss_platform_units=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (OUT/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(controls_pass=good,checks=checks,statistics=stats,predictive=predictive,scatter_dex=result['scatter_dex']),indent=2),flush=True)
    return 0 if good else 1

if __name__=='__main__':sys.exit(main())
