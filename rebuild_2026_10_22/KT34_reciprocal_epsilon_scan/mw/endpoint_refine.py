#!/usr/bin/env python3
"""Higher spatial resolution at numerically marginal upper-edge candidates.

This is selected refinement, not an exhaustive fine-grid epsilon/population scan.
"""
import argparse,json,math,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
import checks as A
E=A.E;M=A.M;np=A.np;HERE=Path(__file__).resolve().parent
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();start=time.monotonic();tr=json.loads((HERE/'transition_run/results.json').read_text());cells=E.population();gm=M.gas_mass();out=dict(coverage='Selected all near-edge full-cut survivors and each terminal width neighbor; no exhaustive fine-grid assertion',footings={})
    for foot in M.C.A0:
        tf=tr['footings'][foot];sup=tf['epsilon_pass_supremum'];chosen={(r['index'],r['k']+dk) for r in tf['terminal_passes'] for dk in (-1,0,1)}
        chosen|={(r['index'],r['k']) for r in tf['full_cut_scores'] if r['epsilon_interval'][1]>=sup-.003 and r['scores']['D']<=1.02}
        f=dict(cases=[]);out['footings'][foot]=f
        for refine,lmax in ((4,160),(5,192)):
            g,mu=M.make_grid(M.C.A0[foot],refine,1);sol=M.Solver(g,mu,M.C.A0[foot])
            for idx,k in sorted(chosen):
                row=A.evaluated(sol,cells[idx],math.exp(.005*k),lmax,120);r=E.rm(cells[idx],foot,gm)
                f['cases'].append(dict(refine=refine,lmax=lmax,index=idx,k=k,epsilon_plateau=[math.exp(.005*(k-.5))/r,math.exp(.005*(k+.5))/r],row=row))
            f['selected_refine'+str(refine)+'_pass_supremum']=max((r['epsilon_plateau'][1] for r in f['cases'] if r['refine']==refine and r['row']['corrected']['all_four']),default=None)
            print(foot,'refine',refine,'selected sup',f['selected_refine'+str(refine)+'_pass_supremum'],'elapsed',time.monotonic()-start,flush=True);Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False))
    out['runtime_seconds']=time.monotonic()-start;Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False))
if __name__=='__main__':main()
