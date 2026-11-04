"""Frozen KT39-pass population: full KT42 source, primary scores and local force."""
import argparse,hashlib,json,math,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE.parent/'mw'))
import filtered_model as F
J,M,E,np=F.J,F.M,F.E,F.np
WIDTHS=[0.,.0001,.001]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();start=time.monotonic()
    selection=json.loads((HERE/'selection.json').read_text())
    oldpath=ROOT/selection['source'];assert hashlib.sha256(oldpath.read_bytes()).hexdigest()==selection['source_sha256']
    original=json.loads(oldpath.read_text());cells=E.population();assert cells==original['cells']
    witness=json.loads((HERE.parent/'mw/scan_001/results.json').read_text())
    checked=json.loads((HERE.parent/'mw/checks_003/results.json').read_text());assert checked['complete'] and checked['all_checks_pass']
    assert witness['refine']==3 and witness['heat_steps']==32
    J.set_power(1.125)
    out=dict(power=1.125,ell_kpc=3.,widths_kpc=WIDTHS,refine=3,heat_steps=32,rmin_kpc=.005,outer=1.,
        selection=selection,coverage='All52 historical KT39 production primary-pass cells; not all1375 cells of new action',
        cases=[],witness_replay=[],complete=False)
    def save():args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    for foot,count in [('canonical',32),('alt',20)]:
        selected=selection['footings'][foot];assert len(selected)==count
        sc=next(s for s in original['footings'][foot]['scans'] if s['ell_kpc']==3.)
        reconstructed=[r['index'] for r in sc['rows'] if r['corrected']['all_four']]
        assert reconstructed==[r['index'] for r in selected]==sc['summary']['pass_indices']
        g,mu=F.grid(foot,3,.005,1.);a0=M.C.A0[foot];sol=M.Solver(g,mu,a0)
        models={width:F.Filtered(sol,width,32) for width in WIDTHS}
        interp=lambda arr,R,z:float(g.interp_cells(arr,np.array([R]),np.array([z]))[0])
        conversion=a0*M.C.PS.KPC/1e6
        for item in selected:
            index=item['index'];assert cells[index]==item['cell']
            rf,_=M.rho_cell(cells[index]);rho=g.rho_axisym(lambda R,z:rf(R,z)/mu,nq=4)
            psi=sol.LU.newton(rho)
            for width in WIDTHS:
                ph,stats=models[width].phantom(psi,3.);total=psi+ph
                score=sol.evaluate(total)
                recomputed=M.C.lines(score['vc'],score['K'],score['K0'],score['vc_Ou'])
                assert all(score[k]==recomputed[k] for k in (*M.GATE,'Lh'))
                if not math.isfinite(score['h']):
                    assert score['h']==float('inf') and not score['Lh'];score['h']=None
                    score['h_status']='nonnegative fitted log-K slope'
                gr,gt=g.grad_cells(total)
                gz=(np.cos(g.t2d)*gr-np.sin(g.t2d)*gt)*conversion
                at=interp(gz,12.,.3)
                differences=[dict(step_kpc=h,gz=(interp(total,12.,.3+h)-interp(total,12.,.3-h))/(2*h)*conversion) for h in [.005,.01,.02]]
                row=dict(footing=foot,index=index,cell=cells[index],a0=a0,width_kpc=width,score=score,
                    source_stats=stats,gz_R12_z03=at,outward=bool(at<0),potential_differences=differences)
                out['cases'].append(row)
                if index=={'canonical':1368,'alt':1287}[foot]:
                    prior=next(r for r in witness['cases'] if r['footing']==foot and r['width_kpc']==width)
                    error=max(abs(score[k]-prior['score'][k])/max(abs(prior['score'][k]),1) for k in ['vc','K0','cK','cO'])
                    force_error=abs(at-prior['gz_R12_z03'])/max(abs(at),1)
                    out['witness_replay'].append(dict(footing=foot,width_kpc=width,score_relative_error=error,force_relative_error=force_error))
                    assert max(error,force_error)<1e-8
                save()
                print(foot,index,width,'gz',at,'primary',score['all_four'],'POSITIVE_FORCE' if at>=0 else 'outward',flush=True)
        del models,sol,g
    assert len(out['cases'])==156
    summaries=[]
    for foot,count in [('canonical',32),('alt',20)]:
        for width in WIDTHS:
            rows=[r for r in out['cases'] if r['footing']==foot and r['width_kpc']==width]
            assert len(rows)==count and len({r['index'] for r in rows})==count
            values=[r['gz_R12_z03'] for r in rows]
            summaries.append(dict(footing=foot,width_kpc=width,n=count,n_outward=sum(v<0 for v in values),
                n_primary_pass=sum(r['score']['all_four'] for r in rows),n_primary_and_restoring=sum(r['score']['all_four'] and r['gz_R12_z03']>0 for r in rows),
                min_gz=min(values),max_gz=max(values),least_outward_index=rows[int(np.argmax(values))]['index'],
                n_potential_difference_sign_agreements=sum(all(np.sign(v['gz'])==np.sign(r['gz_R12_z03']) for v in r['potential_differences']) for r in rows)))
    out['summaries']=summaries;out['complete']=True;out['all_checks_pass']=True;out['runtime_seconds']=time.monotonic()-start;save()
    print(json.dumps(summaries,indent=2),flush=True)

if __name__=='__main__':main()
