#!/usr/bin/env python3
"""Extend selected alternative upper-edge checks after two marginal bins failed."""
import argparse,json,math,sys,time
from pathlib import Path
sys.dont_write_bytecode=True
import checks as A
E=A.E;M=A.M;HERE=Path(__file__).resolve().parent
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();start=time.monotonic();tr=json.loads((HERE/'transition_run/results.json').read_text());cells=E.population();gm=M.gas_mass();foot='alt';tf=tr['footings'][foot]
    chosen={(r['index'],r['k']) for r in tf['full_cut_scores'] if r['epsilon_interval'][1]>=.458 and r['scores']['D']<=1.02}
    out=dict(coverage='Selected alternative upper-edge candidates only; no exhaustive finer-grid claim',footing=foot,cases=[])
    for refine,lmax in ((4,160),(5,192),(6,192)):
        g,mu=M.make_grid(M.C.A0[foot],refine,1);sol=M.Solver(g,mu,M.C.A0[foot])
        take=chosen if refine<6 else {(1359,306),(1368,304),(1368,305)}
        for idx,k in sorted(take):
            row=A.evaluated(sol,cells[idx],math.exp(.005*k),lmax,120);r=E.rm(cells[idx],foot,gm)
            out['cases'].append(dict(refine=refine,lmax=lmax,index=idx,k=k,epsilon_plateau=[math.exp(.005*(k-.5))/r,math.exp(.005*(k+.5))/r],row=row))
        out['selected_refine'+str(refine)+'_pass_supremum']=max((r['epsilon_plateau'][1] for r in out['cases'] if r['refine']==refine and r['row']['corrected']['all_four']),default=None)
        print(foot,refine,'sup',out['selected_refine'+str(refine)+'_pass_supremum'],'elapsed',time.monotonic()-start,flush=True);Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False))
    out['runtime_seconds']=time.monotonic()-start;Path(args.output).write_text(json.dumps(out,indent=2,allow_nan=False))
if __name__=='__main__':main()
