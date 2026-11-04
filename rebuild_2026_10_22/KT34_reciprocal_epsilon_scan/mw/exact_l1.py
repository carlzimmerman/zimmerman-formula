#!/usr/bin/env python3
"""Enumerate every cell/width plateau in a closed epsilon band, L1 only.

For l the inherited radial-force functional, reciprocity gives
l S* L^-1[-W^-1 G^T W A] = -<G L^-1 S(W^-1 l^T), A>_W.
Thus one dual Poisson solve per width replaces per-cell phantom solves.
"""
import argparse,json,math,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
import scan as E
M=E.M;np=E.np


def radial_functional(g,R):
    lr=np.log(g.rc);r=float(R);theta=math.pi/2
    i=int(np.clip(np.searchsorted(lr,math.log(r))-1,0,g.Nr-2))
    j=int(np.clip(np.searchsorted(g.tc,theta)-1,0,g.Nt-2))
    fr=float(np.clip((math.log(r)-lr[i])/(lr[i+1]-lr[i]),0,1))
    ft=float(np.clip((theta-g.tc[j])/(g.tc[j+1]-g.tc[j]),0,1))
    v=np.zeros(g.n)
    for ir,it,w in [(i,j,(1-fr)*(1-ft)),(i+1,j,fr*(1-ft)),(i,j+1,(1-fr)*ft),(i+1,j+1,fr*ft)]:
        idx=ir*g.Nt+it
        v+=w*(math.sin(g.t2d[idx])*g.Crr.getrow(idx).toarray().ravel()+math.cos(g.t2d[idx])*g.Cth.getrow(idx).toarray().ravel())
    return v


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--refine',type=int,default=2);ap.add_argument('--lmax',type=int,default=48);ap.add_argument('--cut',type=float,default=300);ap.add_argument('--upper',type=float,default=2.5);ap.add_argument('--lower-canonical',type=float,default=.5156064781076973);ap.add_argument('--lower-alt',type=float,default=.5928184097198396);ap.add_argument('--feet',nargs='+',default=list(M.C.A0));args=ap.parse_args()
    start=time.monotonic();cells=E.population();gm=M.gas_mass();out=dict(parameters=vars(args),method='Exact finite width-bin enumeration, linear radial-force dual, unchanged L1 cut',cells=cells,footings={})
    for foot in args.feet:
        cache=E.Cached(foot,args.refine,cells);g=cache.g;sol=cache.sol;lower=getattr(args,'lower_'+foot);upper=args.upper
        radii=[E.rm(c,foot,gm) for c in cells];groups={};cell_counts=np.zeros(len(cells),dtype=int)
        for i,r in enumerate(radii):
            for k in range(math.floor(math.log(lower*r)/.005)-2,math.ceil(math.log(upper*r)/.005)+3):
                lo=max(lower,math.exp(.005*(k-.5))/r);hi=min(upper,math.exp(.005*(k+.5))/r)
                if lo<=hi:groups.setdefault(k,[]).append((i,lo,hi));cell_counts[i]+=1
        assert np.all(cell_counts>=1)
        l=radial_functional(g,M.C.R0);newton_force=cache.coef@(cache.newton@l)
        direct0=sol.evaluate(cache.combine(cache.newton,0))['vc'];test0=math.sqrt(max(newton_force[0],0)*sol.a0*M.C.R0*M.C.PS.KPC)/1e3
        assert abs(direct0-test0)<1e-9
        fout=dict(epsilon_closed_band=[lower,upper],grid=dict(nr=g.Nr,nt=g.Nt),basis_density_verification=cache.verify,newton_functional_error=abs(direct0-test0),n_cells=len(cells),n_width_states=int(sum(cell_counts)),n_distinct_widths=len(groups),cell_width_state_counts=cell_counts.tolist(),width_summaries=[],dual_checks=[],cell_max_vc=[-1.]*len(cells),n_L1_pass_states=0,max_negative_mass_bound=0.,max_mass_relative_error_bound=0.)
        out['footings'][foot]=fout
        for n,(k,group) in enumerate(sorted(groups.items())):
            sig=math.exp(.005*k);S=sol.get_filter(sig,args.lmax,args.cut)
            rb=np.array([S.forward(x) for x in cache.basis]);pb=np.array([sol.LU.newton(x) for x in rb])
            drb=np.array([g.Crr@x for x in pb]);dtb=np.array([g.Cth@x for x in pb])
            u=sol.LU.lu.solve(S.forward(l/g.vol));ur=g.Crr@u;ut=g.Cth@u
            wr=-g.vol*ur;wt=-g.vol*ut
            basis_m=rb@g.vol;basis_n=-np.minimum(rb,0)@g.vol
            source_m=cache.basis@g.vol
            masserr=float(np.max(np.abs(basis_m/source_m-1)))
            fout['max_mass_relative_error_bound']=max(fout['max_mass_relative_error_bound'],masserr)
            maxvc=-1.;maxid=None;maxinterval=None;maxneg=0.;passed=[]
            for i,lo,hi in group:
                dr=cache.combine(drb,i);dt=cache.combine(dtb,i);amp=M.C.nu(np.hypot(dr,dt))-1
                force=newton_force[i]+float(np.dot(wr*dr+wt*dt,amp))
                vc=math.sqrt(max(force,0)*sol.a0*M.C.R0*M.C.PS.KPC)/1e3
                ng=float(cache.coef[i]@basis_n/(cache.coef[i]@basis_m));maxneg=max(maxneg,ng)
                if vc>maxvc:maxvc=vc;maxid=i;maxinterval=[lo,hi]
                fout['cell_max_vc'][i]=max(fout['cell_max_vc'][i],vc)
                if abs(vc-M.C.L.VC_BRIEF)<=M.C.L.VC_BRIEF_LINE and abs(vc-M.C.vE)<=2*M.C.eE:passed.append(dict(index=i,epsilon_interval=[lo,hi],vc=vc))
            if n in (0,len(groups)//4,len(groups)//2,3*len(groups)//4,len(groups)-1):
                i,lo,hi=group[len(group)//2];literal=sol.solve(cells[i],sig,args.lmax,args.cut)['corrected']['vc'];dr=cache.combine(drb,i);dt=cache.combine(dtb,i);amp=M.C.nu(np.hypot(dr,dt))-1
                dual=math.sqrt(max(newton_force[i]+float(np.dot(wr*dr+wt*dt,amp)),0)*sol.a0*M.C.R0*M.C.PS.KPC)/1e3
                err=abs(literal-dual);assert err<1e-7
                fout['dual_checks'].append(dict(k=k,xi=sig,index=i,literal_vc=literal,dual_vc=dual,error=err))
            fout['max_negative_mass_bound']=max(fout['max_negative_mass_bound'],maxneg);fout['n_L1_pass_states']+=len(passed)
            fout['width_summaries'].append(dict(k=k,xi=sig,n_cells=len(group),max_vc=maxvc,max_index=maxid,max_epsilon_interval=maxinterval,max_negative_mass_bound=maxneg,L1_passes=passed))
            if n%20==0 or n==len(groups)-1:
                print(foot,n+1,'/',len(groups),'states',sum(x['n_cells'] for x in fout['width_summaries']),'maxvc',max(x['max_vc'] for x in fout['width_summaries']),'L1passes',fout['n_L1_pass_states'],'elapsed',time.monotonic()-start,flush=True)
                Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False))
        assert sum(s['n_cells'] for s in fout['width_summaries'])==fout['n_width_states']
        fout['max_vc']=max(fout['cell_max_vc']);fout['tail_bound_passed']=fout['max_negative_mass_bound']<=1e-5
        assert fout['max_mass_relative_error_bound']<1e-10
    out['runtime_seconds']=time.monotonic()-start;Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False))

if __name__=='__main__':main()
