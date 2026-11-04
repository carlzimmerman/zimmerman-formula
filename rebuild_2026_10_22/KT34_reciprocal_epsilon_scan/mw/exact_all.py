#!/usr/bin/env python3
"""Exhaust upper MW transition bands using L1 as a necessary early rejection.

All original cells and all width plateaus are enumerated. A width/cell failing
L1 cannot pass all four cuts; every L1 survivor receives the full KT33 solve.
"""
import argparse,json,math,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
import exact_l1 as D
E=D.E;M=D.M;np=D.np


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--refine',type=int,default=2);ap.add_argument('--lmax',type=int,default=96);ap.add_argument('--cut',type=float,default=120);ap.add_argument('--lower-canonical',type=float,default=.3);ap.add_argument('--upper-canonical',type=float,default=.5156064781076973);ap.add_argument('--lower-alt',type=float,default=.44);ap.add_argument('--upper-alt',type=float,default=.5928184097198396);ap.add_argument('--feet',nargs='+',default=list(M.C.A0));args=ap.parse_args()
    start=time.monotonic();cells=E.population();gm=M.gas_mass();out=dict(parameters=vars(args),method='Exact finite width-bin enumeration; L1 dual prefilter then unchanged all-four-cuts evaluation',cells=cells,footings={})
    for foot in args.feet:
        cache=E.Cached(foot,args.refine,cells);g=cache.g;sol=cache.sol;lower=getattr(args,'lower_'+foot);upper=getattr(args,'upper_'+foot)
        assert np.all(cache.coef>=0)
        radii=[E.rm(c,foot,gm) for c in cells];groups={};cell_counts=np.zeros(len(cells),dtype=int)
        for i,r in enumerate(radii):
            for k in range(math.floor(math.log(lower*r)/.005)-2,math.ceil(math.log(upper*r)/.005)+3):
                lo=max(lower,math.exp(.005*(k-.5))/r);hi=min(upper,math.exp(.005*(k+.5))/r)
                if lo<=hi:groups.setdefault(k,[]).append((i,lo,hi));cell_counts[i]+=1
        assert np.all(cell_counts>=1)
        l=D.radial_functional(g,M.C.R0);newton_force=cache.coef@(cache.newton@l)
        f=dict(epsilon_closed_band=[lower,upper],grid=dict(nr=g.Nr,nt=g.Nt),basis_density_verification=cache.verify,coefficient_min=float(np.min(cache.coef)),n_cells=len(cells),n_width_states=int(sum(cell_counts)),n_distinct_widths=len(groups),cell_width_state_counts=cell_counts.tolist(),width_summaries=[],passes=[],max_negative_mass_bound=0.,max_mass_relative_error_bound=0.,dual_full_vc_error_max=0.,full_cut_scores=[],n_full_cut_evaluations=0)
        out['footings'][foot]=f
        for n,(k,group) in enumerate(sorted(groups.items())):
            sig=math.exp(.005*k);S=sol.get_filter(sig,args.lmax,args.cut)
            rb=np.array([S.forward(x) for x in cache.basis]);pb=np.array([sol.LU.newton(x) for x in rb]);drb=np.array([g.Crr@x for x in pb]);dtb=np.array([g.Cth@x for x in pb])
            u=sol.LU.lu.solve(S.forward(l/g.vol));wr=-g.vol*(g.Crr@u);wt=-g.vol*(g.Cth@u)
            basis_m=rb@g.vol;basis_n=-np.minimum(rb,0)@g.vol;source_m=cache.basis@g.vol
            f['max_mass_relative_error_bound']=max(f['max_mass_relative_error_bound'],float(np.max(np.abs(basis_m/source_m-1))))
            count_L1=0;count_pass=0;maxvc=-1.;maxneg=0.
            for i,lo,hi in group:
                dr=cache.combine(drb,i);dt=cache.combine(dtb,i);amp=M.C.nu(np.hypot(dr,dt))-1
                force=newton_force[i]+float(np.dot(wr*dr+wt*dt,amp));vc=math.sqrt(max(force,0)*sol.a0*M.C.R0*M.C.PS.KPC)/1e3
                maxvc=max(maxvc,vc);ng=float(cache.coef[i]@basis_n/(cache.coef[i]@basis_m));maxneg=max(maxneg,ng)
                if not(abs(vc-M.C.L.VC_BRIEF)<=M.C.L.VC_BRIEF_LINE and abs(vc-M.C.vE)<=2*M.C.eE):continue
                count_L1+=1
                pn=cache.combine(cache.newton,i);px=cache.combine(pb,i);ph=sol.phantom(px);q=sol.evaluate(pn+S.adjoint(ph));err=abs(q['vc']-vc)
                f['dual_full_vc_error_max']=max(f['dual_full_vc_error_max'],err);assert err<1e-7
                f['n_full_cut_evaluations']+=1
                # Retain compact scores for every necessary-cut survivor; full
                # profiles for actual all-four passes make review reproducible.
                f['full_cut_scores'].append(dict(index=i,k=k,epsilon_interval=[lo,hi],scores={key:q[key] for key in ('vc','K0','cK','cO','h','D',*M.GATE,'Lh','all_four')}))
                if q['all_four']:
                    count_pass+=1;f['passes'].append(dict(index=i,cell=cells[i],k=k,xi=sig,epsilon_interval=[lo,hi],corrected=q,negative_mass_bound=ng))
            f['max_negative_mass_bound']=max(f['max_negative_mass_bound'],maxneg)
            f['width_summaries'].append(dict(k=k,xi=sig,n_cells=len(group),max_vc=maxvc,max_negative_mass_bound=maxneg,n_L1_pass=count_L1,n_pass=count_pass))
            if n%10==0 or n==len(groups)-1:
                print(foot,n+1,'/',len(groups),'states',sum(x['n_cells'] for x in f['width_summaries']),'full',f['n_full_cut_evaluations'],'passstates',len(f['passes']),'elapsed',time.monotonic()-start,flush=True)
                Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False))
        assert sum(s['n_cells'] for s in f['width_summaries'])==f['n_width_states']
        f['tail_bound_passed']=f['max_negative_mass_bound']<=1e-5
        assert f['max_mass_relative_error_bound']<1e-10
        assert f['tail_bound_passed']
        if f['passes']:
            f['epsilon_pass_supremum']=max(r['epsilon_interval'][1] for r in f['passes']);f['terminal_passes']=[r for r in f['passes'] if r['epsilon_interval'][1]==f['epsilon_pass_supremum']]
            intervals=sorted([r['epsilon_interval'] for r in f['passes']]);merged=[]
            for lo,hi in intervals:
                if merged and lo<=merged[-1][1]:merged[-1][1]=max(merged[-1][1],hi)
                else:merged.append([lo,hi])
            f['pass_interval_union_closed_cover']=merged
    out['runtime_seconds']=time.monotonic()-start;Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False))

if __name__=='__main__':main()
