#!/usr/bin/env python3
"""Full baryon population for selected constitutive laws; exact dual L1 screen."""
import argparse
import json
import math
import sys
import time
from pathlib import Path
sys.dont_write_bytecode=True
import search as U
M,E,np=U.M,U.E,U.np
import exact_l1 as D
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'response'))
from response import Response, finite_admissibility


class Solver(M.Solver):
    def __init__(self,g,mu,a0,response):
        super().__init__(g,mu,a0);self.response=response

    def phantom(self,pn,mut=False):
        if mut:return np.zeros_like(pn)
        g=self.g;dr,dt=g.grad_cells(pn)
        a=self.response.excess(np.hypot(dr,dt))
        b=-(g.Crr.T@(g.vol*a*dr)+g.Cth.T@(g.vol*a*dt))/g.vol
        return self.LU.lu.solve(b)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True)
    p.add_argument('--refine',type=int,default=2);p.add_argument('--lmax',type=int,default=128)
    args=p.parse_args();start=time.monotonic();cells=E.population();gm=M.gas_mass()
    cases=[('canonical',.25,Response('cutoff',scale=1.5,power=6)),
           ('canonical',.30,Response('cutoff',scale=1.5,power=6)),
           ('canonical',.25,Response('cutoff',scale=1.5,power=4)),
           ('alt',.5,Response('cutoff',scale=1.5,power=6))]
    out=dict(parameters=vars(args),coverage='Full original 1375-cell population per listed model; full cuts only after necessary L1 test',
             cases=[],cells=cells)
    for foot in M.C.A0:
        cache=E.Cached(foot,args.refine,cells);g=cache.g;l=D.radial_functional(g,M.C.R0)
        nf=cache.coef@(cache.newton@l)
        for ff,ep,response in cases:
            if ff!=foot:continue
            sol=Solver(g,cache.mu,M.C.A0[foot],response)
            adm=finite_admissibility(response);assert adm['passed']
            f=dict(footing=foot,epsilon=ep,response=response.metadata,admissibility=adm,
                   full_scores=[],all_vc=[None]*len(cells),max_negative_mass_bound=0.,max_mass_error=0.,
                   dual_full_max_vc_error=0.,min_rejected_L1_margin=float('inf'))
            out['cases'].append(f);groups={}
            for i,c in enumerate(cells):groups.setdefault(E.width(ep,E.rm(c,foot,gm)),[]).append(i)
            low=max(M.C.L.VC_BRIEF-M.C.L.VC_BRIEF_LINE,M.C.vE-2*M.C.eE)
            high=min(M.C.L.VC_BRIEF+M.C.L.VC_BRIEF_LINE,M.C.vE+2*M.C.eE)
            for sig,ids in sorted(groups.items()):
                S=sol.get_filter(sig,args.lmax,120)
                rb=np.array([S.forward(x) for x in cache.basis])
                pb=np.array([sol.LU.newton(x) for x in rb])
                drb=np.array([g.Crr@x for x in pb]);dtb=np.array([g.Cth@x for x in pb])
                u=sol.LU.lu.solve(S.forward(l/g.vol));wr=-g.vol*(g.Crr@u);wt=-g.vol*(g.Cth@u)
                bm=rb@g.vol;bn=-np.minimum(rb,0)@g.vol
                me=float(np.max(np.abs(bm/(cache.basis@g.vol)-1)))
                f['max_mass_error']=max(f['max_mass_error'],me)
                for i in ids:
                    dr=cache.combine(drb,i);dt=cache.combine(dtb,i)
                    amp=response.excess(np.hypot(dr,dt))
                    force=nf[i]+float(np.dot(wr*dr+wt*dt,amp))
                    vc=math.sqrt(max(force,0)*sol.a0*M.C.R0*M.C.PS.KPC)/1e3
                    f['all_vc'][i]=vc
                    ng=float(cache.coef[i]@bn/(cache.coef[i]@bm))
                    f['max_negative_mass_bound']=max(f['max_negative_mass_bound'],ng)
                    if low<=vc<=high:
                        pn=cache.combine(cache.newton,i);px=cache.combine(pb,i)
                        q=sol.evaluate(pn+S.adjoint(sol.phantom(px)))
                        er=abs(q['vc']-vc);f['dual_full_max_vc_error']=max(f['dual_full_max_vc_error'],er)
                        assert er<1e-7
                        f['full_scores'].append(dict(index=i,cell=cells[i],xi=sig,corrected=q,negative_mass_upper_bound=ng))
                    else:
                        margin=min(abs(vc-low),abs(vc-high))
                        f['min_rejected_L1_margin']=min(f['min_rejected_L1_margin'],margin)
            f['n_tested']=len(f['all_vc']);assert all(v is not None for v in f['all_vc'])
            f['max_vc']=max(f['all_vc']);f['n_L1_pass']=len(f['full_scores'])
            good=[r for r in f['full_scores'] if r['corrected']['all_four']]
            f['n_pass']=len(good);f['pass_indices']=[r['index'] for r in good]
            f['n_strict']=sum(r['corrected']['Lh'] for r in good)
            f['best']=min(f['full_scores'],key=lambda r:r['corrected']['D']) if f['full_scores'] else None
            f['numerical_gates_pass']=f['max_negative_mass_bound']<1e-5 and f['max_mass_error']<1e-10 and f['min_rejected_L1_margin']>1e-7
            print(foot,ep,response.name,'passes',f['n_pass'],'max_vc',f['max_vc'],'gates',f['numerical_gates_pass'],'elapsed',time.monotonic()-start,flush=True)
            Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False))
    out['runtime_seconds']=time.monotonic()-start
    Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False))


if __name__=='__main__':main()
