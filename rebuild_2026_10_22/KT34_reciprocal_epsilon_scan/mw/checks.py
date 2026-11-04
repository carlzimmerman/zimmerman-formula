#!/usr/bin/env python3
"""Independent population/cut audit, necessary-filter margin, selected refinements."""
import argparse,json,math,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
import exact_l1 as D
E=D.E;M=D.M;np=D.np
HERE=Path(__file__).resolve().parent


def evaluated(sol,cell,sig,lmax,cut):
    row=sol.solve(cell,sig,lmax,cut);rf,_=M.rho_cell(cell);rho=sol.g.rho_axisym(lambda R,z:rf(R,z)/sol.mu,nq=4);S=sol.get_filter(sig,lmax,cut);rx=S.forward(rho)
    mass=float(np.dot(sol.g.vol,rx));negative=float(-np.dot(sol.g.vol,np.minimum(rx,0))/mass)
    row['negative_mass_fraction']=negative;row['source_mass_relative_error']=abs(mass/np.dot(sol.g.vol,rho)-1)
    assert negative<1e-5;assert row['source_mass_relative_error']<1e-10
    return row


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();start=time.monotonic()
    exact=json.loads((HERE/'exact_run/results.json').read_text());tr=json.loads((HERE/'transition_run/results.json').read_text());high=json.loads((HERE/'high_run/results.json').read_text());boundary=json.loads((HERE/'boundary_run/results.json').read_text());cells=E.population();gm=M.gas_mass()
    out=dict(population=len(cells),footings={},outcome='conditional on numerical resolution; exact finite epsilon-state coverage')
    assert tr['cells']==cells and exact['cells']==cells
    for foot in M.C.A0:
        assert exact['footings'][foot]['n_L1_pass_states']==0 and exact['footings'][foot]['tail_bound_passed']
        tf=tr['footings'][foot];assert tf['tail_bound_passed']
        for coll in (high,boundary):
            for scan in coll['footings'][foot]['scans']:
                assert [r['cell'] for r in scan['rows']]==cells
                for row in scan['rows']:
                    q=row['corrected'];rec=M.C.lines(q['vc'],q['K'],q['K0'],q['vc_Ou']);assert all(q[k]==rec[k] for k in (*M.GATE,'Lh'))
                    assert row['xi']==E.width(scan['epsilon'],E.rm(row['cell'],foot,gm))
        f=dict(population_and_cut_checks_passed=True,transition_refinements=[],highband_refinements=[],small_epsilon_diagnostics=[]);out['footings'][foot]=f
        sup=tf['epsilon_pass_supremum'];chosen={(r['index'],r['k']+dk) for r in tf['terminal_passes'] for dk in (-1,0,1)}
        chosen|={(r['index'],r['k']) for r in tf['full_cut_scores'] if r['epsilon_interval'][1]>=sup-.003 and r['scores']['D']<=1.02}
        for refine,lmax in ((2,96),(3,128)):
            g,mu=M.make_grid(M.C.A0[foot],refine,1);sol=M.Solver(g,mu,M.C.A0[foot])
            for idx,k in sorted(chosen):
                row=evaluated(sol,cells[idx],math.exp(.005*k),lmax,120);r=E.rm(cells[idx],foot,gm)
                f['transition_refinements'].append(dict(refine=refine,lmax=lmax,index=idx,k=k,epsilon_plateau=[math.exp(.005*(k-.5))/r,math.exp(.005*(k+.5))/r],row=row))
        # Largest L1 force in the exact band and its broad-kernel upper endpoint.
        lower=exact['footings'][foot]['epsilon_closed_band'][0];best=max(exact['footings'][foot]['width_summaries'],key=lambda x:x['max_vc'])
        g,mu=M.make_grid(M.C.A0[foot],3,1);sol=M.Solver(g,mu,M.C.A0[foot])
        for ep,idx in ((lower,best['max_index']),(2.5,1350)):
            sig=E.width(ep,E.rm(cells[idx],foot,gm))
            for cut in (300,600):
                row=evaluated(sol,cells[idx],sig,96,cut);assert not row['corrected']['L1']
                f['highband_refinements'].append(dict(epsilon=ep,index=idx,refine=3,lmax=96,cut=cut,row=row))
        # Selected low-epsilon witnesses; this does not promote the whole coarse scan.
        low=json.loads((HERE/'low_run/results.json').read_text())['footings'][foot]['scans']
        for ep in ((.15,.25,.3) if foot=='canonical' else (.15,.2,.3,.4,.45)):
            ss=next(s for s in low if s['epsilon']==ep);passes=[r for r in ss['rows'] if r['corrected']['all_four']]
            if not passes:continue
            candidate=min(passes,key=lambda r:r['corrected']['D']);idx=candidate['index'];sig=E.width(ep,E.rm(cells[idx],foot,gm))
            row=evaluated(sol,cells[idx],sig,192,120)
            f['small_epsilon_diagnostics'].append(dict(epsilon=ep,index=idx,refine=3,lmax=192,row=row))
        Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False));print(foot,'refinements finished',time.monotonic()-start,flush=True)
        # Re-evaluate every transition-band dual necessary test and record the
        # closest rejected distance. This audits floating-point prefilter safety.
        cache=E.Cached(foot,2,cells);assert np.all(cache.coef>=0);f['coefficient_min']=float(cache.coef.min());g=cache.g;sol=cache.sol;l=D.radial_functional(g,M.C.R0);nf=cache.coef@(cache.newton@l)
        lower,upper=tf['epsilon_closed_band'];groups={}
        for i,c in enumerate(cells):
            r=E.rm(c,foot,gm)
            for k in range(math.floor(math.log(lower*r)/.005)-2,math.ceil(math.log(upper*r)/.005)+3):
                if max(lower,math.exp(.005*(k-.5))/r)<=min(upper,math.exp(.005*(k+.5))/r):groups.setdefault(k,[]).append(i)
        lo=max(M.C.L.VC_BRIEF-M.C.L.VC_BRIEF_LINE,M.C.vE-2*M.C.eE);hi=min(M.C.L.VC_BRIEF+M.C.L.VC_BRIEF_LINE,M.C.vE+2*M.C.eE)
        expected={(r['index'],r['k']) for r in tf['full_cut_scores']};seen=set();n=0;min_rejected=float('inf');closest=None
        for count,(k,ids) in enumerate(sorted(groups.items())):
            S=sol.get_filter(math.exp(.005*k),96,120);pb=np.array([sol.LU.newton(S.forward(x)) for x in cache.basis]);drb=np.array([g.Crr@x for x in pb]);dtb=np.array([g.Cth@x for x in pb]);u=sol.LU.lu.solve(S.forward(l/g.vol));wr=-g.vol*(g.Crr@u);wt=-g.vol*(g.Cth@u)
            for i in ids:
                dr=cache.combine(drb,i);dt=cache.combine(dtb,i);amp=M.C.nu(np.hypot(dr,dt))-1;force=nf[i]+float(np.dot(wr*dr+wt*dt,amp));vc=math.sqrt(max(force,0)*sol.a0*M.C.R0*M.C.PS.KPC)/1e3;n+=1
                if lo<=vc<=hi:seen.add((i,k))
                else:
                    margin=min(abs(vc-lo),abs(vc-hi))
                    if margin<min_rejected:min_rejected=margin;closest=dict(index=i,k=k,vc=vc)
            if count%30==0:print(foot,'margin audit',count+1,'/',len(groups),'elapsed',time.monotonic()-start,flush=True)
        assert n==tf['n_width_states'];assert seen==expected;assert min_rejected>1e-7
        f['prefilter_audit']=dict(n_states=n,n_survivors=len(seen),min_rejected_boundary_distance_km_s=min_rejected,closest_rejected=closest,full_dual_difference_max=tf['dual_full_vc_error_max'],required_separation_km_s=1e-7,passed=True)
        f['selected_refine3_pass_supremum']=max((r['epsilon_plateau'][1] for r in f['transition_refinements'] if r['refine']==3 and r['row']['corrected']['all_four']),default=None)
        Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False))
    out['passed']=True;out['runtime_seconds']=time.monotonic()-start;Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False))

if __name__=='__main__':main()
