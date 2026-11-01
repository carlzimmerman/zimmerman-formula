#!/usr/bin/env python3
"""Conditional paired-seed capacity envelope. No legacy pipeline execution/writes."""
import os
for _k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[_k]='1'
import json,math,pathlib,pickle,resource,sys,time
import numpy as np
from scipy.optimize import brentq,minimize_scalar
from measure_pairs import contract
ROOT=pathlib.Path(__file__).resolve().parents[3];RB=ROOT/'rebuild_2026_10_22';HERE=pathlib.Path(__file__).resolve().parent
OUT=pathlib.Path(sys.argv[1]);OUT.mkdir(exist_ok=True,parents=True)
B=lambda x:4*(np.arcsinh(x)-x/np.sqrt(1+x*x))
PK=math.exp(minimize_scalar(lambda l:-float(B(math.exp(l))/math.exp(2*l)),bounds=(-6,12),method='bounded').x)
SAT=0
def solve_r0(M,R,S):
    global SAT
    target=M/(math.pi*S*R*R);peak=float(B(PK)/PK**2)
    if target>peak:SAT+=1;return R/PK
    return R/math.exp(brentq(lambda l:math.log(float(B(math.exp(l))))-2*l-math.log(target),math.log(PK),math.log(1e7),xtol=1e-13))
def fit(q,gh,ups):
    pred=np.log10(np.maximum(q['GB']+gh,1e-300));r=np.where(q['OK'],np.log10(q['GO'])[:,None]-pred,0);w=np.where(q['OK'],q['W'][:,None],0);ws=w.sum(0);sse=(w*r*r).sum(0);i=int(np.argmin(sse/np.maximum(ws,1e-300)))
    return dict(U=float(ups[i]),sse=float(sse[i]),weight=float(ws[i]),iu=i)
def contracted(q,h,S,r0,ups,ge,ms):
    """Solve r_i M0(r_i)(1+F)=r_f[Mb(r_f)+M0(r_i)] directly."""
    R=q['Rm'];rv=h['R200'];M=h['M2'];M0=math.pi*S*r0*r0*B(R/r0)
    Mb=np.maximum.accumulate(np.maximum(q['GB']*R[:,None]**2/ge,0),axis=0)
    Mtot=np.maximum(Mb[-1],(ups*q['L36']+1.33*q['MHI'])*1e9*ms);F=Mtot/M
    # At queried radii Mb is exactly the original cumulative load; the outer extrapolation
    # matters only to the legacy-shell interpolation benchmark.
    low=np.broadcast_to(R[:,None]/(1+F),Mb.shape).copy();hi=np.full(Mb.shape,rv)
    low=np.minimum(low,hi)
    for _ in range(52):
        ri=np.sqrt(low*hi);Mi=math.pi*S*r0*r0*B(ri/r0);f=ri*Mi*(1+F)-R[:,None]*(Mb+Mi);gt=f>0;hi=np.where(gt,ri,hi);low=np.where(gt,low,ri)
    mc=math.pi*S*r0*r0*B(np.sqrt(low*hi)/r0)
    # The legacy evaluator holds cumulative mass beyond its final stored R200.
    mc=np.where(R[:,None]>=rv,M,mc)
    return M0,mc
def legacy(q,h,S,r0,U,ge,ms,n):
    R=q['Rm'];rv=h['R200'];rg=np.geomspace(R[0]*.05,rv,n);mi=math.pi*S*r0*r0*B(rg/r0);ii=int(np.argmin(abs(UPS-U)));mbk=np.maximum.accumulate(np.maximum(q['GB'][:,ii]*R*R/ge,0));mt=max(float(mbk[-1]),(U*q['L36']+1.33*q['MHI'])*1e9*ms)
    bg=np.where(rg<R[0],mbk[0]*(rg/R[0])**2,np.interp(np.log(rg),np.log(R),mbk));o=rg>R[-1]
    if o.any():t=np.clip(np.log(rg[o]/R[-1])/math.log(3),0,1);bg[o]=np.exp(np.log(max(mbk[-1],1e-300))*(1-t)+np.log(mt)*t)
    bg=np.maximum.accumulate(bg);mf,_=contract(rg,bg,mi,mt/h['M2']);return np.interp(np.log(R),np.log(rg),mf)
def hs_stat(rows,tag):
    good=[r for r in rows if r['hs_eligible'] and r['delta'] is not None];x=np.array([r['logSB'] for r in good]);y=np.array([r['delta'] for r in good]);xc=x-x.mean();b=float(xc@(y-y.mean())/(xc@xc));rng=np.random.default_rng(20261101);ix=rng.integers(0,len(x),(10000,len(x)));xx=x[ix];yy=y[ix];xx-=xx.mean(1)[:,None];yy-=yy.mean(1)[:,None];bb=np.sum(xx*yy,axis=1)/np.sum(xx*xx,axis=1);sig=float(np.diff(np.percentile(bb,[16,84]))[0]/2)
    return dict(n=len(x),b=b,sigma=sig,Z=b/sig,flat=abs(b)<=2*sig,mean=float(y.mean()),rms=float(np.sqrt(np.mean(y*y))))
def summary(rows):
    U=np.array([r['U'] for r in rows]);rr=math.sqrt(sum(r['sse'] for r in rows)/sum(r['weight'] for r in rows));bins={}
    for lo,hi in ((20,60),(60,100),(100,150),(150,200),(200,250),(250,400)):
        k=[r for r in rows if r['quality_eligible'] and lo<=r['vf']<=hi];bins[f'{lo}-{hi}']=dict(n=len(k),median_U=float(np.median([r['U'] for r in k])))
    return dict(n=len(rows),median_U=float(np.median(U)),rms=rr,line=bool(.50<=np.median(U)<=.80 and rr<=.110),bins=bins,HS1=hs_stat(rows,None))
def main():
    global UPS
    start=time.monotonic();C=pickle.load(open(RB/'SL1_symbolic_law_search/cache/sl1_cache.pkl','rb'));nr=json.load(open(RB/'NR2_low_mass_ng80/nr2_results.json'));pairs=json.load(open(HERE/'run_002/results.json'))['rows'];gals=C['gals'];co=C['const'];ge=co['GE'];ms=co['MSUNE'];UPS=C['UPS'];I5=int(np.argmin(abs(UPS-.5)));KPC=co['MPCE']/1e3
    cat={}
    for line in open(ROOT/'real_research/data/SPARC_Lelli2016c.mrt'):
        p=line.split()
        if len(p)<18:continue
        try:cat[p[0]]=dict(sb=float(p[10]),rd=float(p[11]))
        except ValueError:pass
    valid=sorted([q for q in gals if cat.get(q['name'],{}).get('sb',0)>0],key=lambda q:(cat[q['name']]['sb'],q['name']))
    seeds=sorted(pairs,key=lambda p:p['spin'],reverse=True);assignment={q['name']:min(8,int(i*9/len(valid))) for i,q in enumerate(valid)}
    pairs=seeds;sf=np.array([p['no_S'] for p in pairs]);sf/=np.median(sf);fq=np.array([p['f_Q'] for p in pairs]);fmed=float(np.median(fq))
    modes=('NR1_baseline','NR2_baseline','NR2_median_response','paired_mean_force','paired_perfect_inverse_spin','ranked_scatter_no_response','ranked_response_permuted')
    allrows={t:{m:[] for m in modes} for t in ('A_c2b_refit','B_cfg886_bg')};bench=[];checks={}
    for tag in allrows:
        for ig,q in enumerate(gals):
            h=q['halo'][tag];M=h['M2'];rv=h['R200'];R=q['Rm'];Mt=M/ms/co['FC'];lg=math.log10(Mt);ratio=1.
            if lg<12:
                eta=21.53*10**float(np.interp(lg,[10,11,12],[math.log10(nr['r10']),math.log10(nr['r11']),0]));ratio=eta/h['eta']
            S=h['S']*ratio;r0=solve_r0(M,rv,S);m0=math.pi*S*r0*r0*B(R/r0)
            hn=ge*m0/R**2;h1=ge*math.pi*h['S']*h['r0']**2*B(R/h['r0'])/R**2
            zero,contracted0=contracted(q,h,S,r0,UPS,ge,ms);median=ge*(zero[:,None]+fmed*(contracted0-zero[:,None]))/R[:,None]**2
            comp=[];comp0=[];permuted=[]
            for j in range(9):
                sj=S*sf[j];rj=solve_r0(M,rv,sj);mz,mc=contracted(q,h,sj,rj,UPS,ge,ms);comp.append(ge*(mz[:,None]+fq[j]*(mc-mz[:,None]))/R[:,None]**2);comp0.append(ge*mz/R**2);permuted.append(ge*(mz[:,None]+fq[(j+1)%9]*(mc-mz[:,None]))/R[:,None]**2)
            mean=np.mean(comp,axis=0);jj=assignment.get(q['name']);ranked=mean if jj is None else comp[jj];rank0=np.mean(comp0,axis=0) if jj is None else comp0[jj];rankp=np.mean(permuted,axis=0) if jj is None else permuted[jj]
            data=dict(NR1_baseline=h1[:,None],NR2_baseline=hn[:,None],NR2_median_response=median,paired_mean_force=mean,paired_perfect_inverse_spin=ranked,ranked_scatter_no_response=rank0[:,None],ranked_response_permuted=rankp)
            qeligible=bool(q['Q']<=2 and q['inc']>=30);hsel=qeligible and 60<=q['vf']<=120;ct=cat.get(q['name']);ok=q['OK'][:,I5];r2=2*ct['rd'] if ct else None;ins=bool(ct and ct['sb']>0 and ok.sum()>=2 and R[ok].min()/KPC<=r2<=R[ok].max()/KPC)
            for name,gh in data.items():
                z=fit(q,gh,UPS);delta=None
                if ins:
                    v=np.sqrt(np.maximum((q['GB'][:,I5]+gh[:,0 if gh.shape[1]==1 else I5])*R,0))/1e3;delta=float(np.interp(math.log(r2),np.log(R[ok]/KPC),v[ok]/np.sqrt(q['GO'][ok]*R[ok])*1e3-1))
                z.update(name=q['name'],vf=float(q['vf']),quality_eligible=qeligible,hs_eligible=hsel,delta=delta,nonpositive_graded_accelerations=int(np.sum((q['GB']+gh<=0)&q['OK'])),logSB=math.log10(ct['sb']) if ct and ct['sb']>0 else None,seed_assigned=None if jj is None else pairs[jj]['seed']);allrows[tag][name].append(z)
            if tag=='A_c2b_refit' and ig<3:
                exact=contracted0[:,I5]
                for n in (300,1200):
                    leg=legacy(q,h,S,r0,.5,ge,ms,n);rel=float(np.max(abs(exact/leg-1)));bench.append(dict(galaxy=q['name'],n_shells=n,max_mass_relative_error=rel));print('benchmark',bench[-1],flush=True)
            if ig%40==0:print(tag,ig,'/',len(gals),flush=True)
    sums={t:{m:summary(r) for m,r in d.items()} for t,d in allrows.items()}
    checks['NR1_max_U_difference']=max(abs(sums[t]['NR1_baseline']['median_U']-C['NR1_sparc']['canonical'][t][0]) for t in sums)
    checks['NR1_max_rms_difference']=max(abs(sums[t]['NR1_baseline']['rms']-C['NR1_sparc']['canonical'][t][1]) for t in sums)
    checks['NR2_max_U_difference']=max(abs(sums[t]['NR2_baseline']['median_U']-nr['runs']['MEDIAN'][t][0]) for t in sums)
    checks['NR2_max_rms_difference']=max(abs(sums[t]['NR2_baseline']['rms']-nr['runs']['MEDIAN'][t][1]) for t in sums)
    checks['benchmark_1200_max_mass_relative_error']=max(b['max_mass_relative_error'] for b in bench if b['n_shells']==1200)
    checks['permutation_mean_delta_change']=max(abs(sums[t]['paired_perfect_inverse_spin']['HS1']['mean']-sums[t]['ranked_response_permuted']['HS1']['mean']) for t in sums)
    good=checks['NR1_max_U_difference']<1e-9 and checks['NR1_max_rms_difference']<1e-9 and checks['NR2_max_U_difference']<=.005 and checks['NR2_max_rms_difference']<1e-5 and checks['benchmark_1200_max_mass_relative_error']<.005 and checks['permutation_mean_delta_change']>1e-5
    result=dict(assertion_tested='conditional one-mass paired-seed capacity envelope; no measured galaxy spins',controls_pass=good,checks=checks,summary=sums,rows=allrows,benchmarks=bench,seed_order=[q['seed'] for q in pairs],S_factors=sf.tolist(),f_Q=fq.tolist(),saturations=SAT,runtime_seconds=time.monotonic()-start,maxrss_platform_units=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (OUT/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(dict(controls_pass=good,checks=checks,summary=sums),indent=2),flush=True);return 0 if good else 1
if __name__=='__main__':sys.exit(main())
