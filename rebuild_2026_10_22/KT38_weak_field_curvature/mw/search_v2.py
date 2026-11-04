"""Pilot or full frozen baryon-population generalized-action scan."""
import argparse,json,time,math
from pathlib import Path
import weak_model as J
M,E,np=J.M,J.E,J.np


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path)
    ap.add_argument('--refine',type=int,default=2)
    ap.add_argument('--lengths',type=float,nargs='+',default=[.3,1.,3.,5.,10.])
    ap.add_argument('--indices',type=int,nargs='+')
    ap.add_argument('--feet',nargs='+',default=['canonical','alt'])
    ap.add_argument('--invariants',required=True,type=Path)
    ap.add_argument('--covariance',required=True,type=Path)
    args=ap.parse_args();started=time.monotonic()
    assert json.loads(args.invariants.read_text())['all_checks_pass']
    covariance=json.loads(args.covariance.read_text())
    assert covariance['operator']=='v3' and covariance['all_checks_pass']
    assert all(e>=0 for e in args.lengths)
    cells=E.population();ids=list(range(len(cells))) if args.indices is None else args.indices
    assert len(ids)==len(set(ids)) and all(0<=i<len(cells) for i in ids)
    out=dict(law='P=xQ(z)/z,z=x+s^2,x=g:g,s=ell^2 H:H,Qprime=simple nu(sqrt(z)),Q0=0',
        filter='none; physical Newtonian source unsmoothed',nonfinite_scale_length='h=null with h_status records positive infinity; Lh remains false and all original cuts are evaluated before encoding',parameters={**vars(args),'output':str(args.output),'invariants':str(args.invariants),'covariance':str(args.covariance)},
        population=1375,selected_indices=ids,cells=cells,footings={},outcome='conditional finite-grid variational generalized-action diagnostic')
    for foot in args.feet:
        cache=E.Cached(foot,args.refine,cells);model=J.Generalized(cache.sol)
        f=dict(grid=dict(nr=cache.g.Nr,nt=cache.g.Nt),basis_verification=cache.verify,scans=[])
        out['footings'][foot]=f
        by_length={ell:[] for ell in args.lengths}
        for count,i in enumerate(ids):
            psi=cache.combine(cache.newton,i);fields=model.fields(psi)
            for ell in args.lengths:
                ph,stats=model.phantom(psi,ell,fields=fields)
                q=cache.sol.evaluate(psi+ph)
                recomputed=M.C.lines(q['vc'],q['K'],q['K0'],q['vc_Ou'])
                assert all(q[k]==recomputed[k] for k in (*M.GATE,'Lh'))
                encoded=dict(q)
                if not math.isfinite(q['h']):
                    assert q['h']==float('inf') and not q['Lh']
                    encoded['h']=None
                    encoded['h_status']='positive infinity: fitted log-K slope is nonnegative'
                by_length[ell].append(dict(index=i,cell=cells[i],ell_kpc=ell,corrected=encoded,source_stats=stats))
            if count%100==0:print(foot,count+1,'/',len(ids),'elapsed',time.monotonic()-started,flush=True)
        for ell,rows in by_length.items():
            good=[r for r in rows if r['corrected']['all_four']]
            best=min(rows,key=lambda r:r['corrected']['D'])
            summary=dict(n_tested=len(rows),n_pass=len(good),n_strict=sum(r['corrected']['Lh'] for r in good),
                pass_indices=[r['index'] for r in good],lines={k:sum(r['corrected'][k] for r in rows) for k in (*M.GATE,'Lh')},
                best_D_index=best['index'],best_D=best['corrected']['D'],max_vc=max(r['corrected']['vc'] for r in rows))
            f['scans'].append(dict(ell_kpc=ell,summary=summary,rows=rows))
            print(foot,ell,summary,flush=True)
        args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    out['runtime_seconds']=time.monotonic()-started
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':main()
