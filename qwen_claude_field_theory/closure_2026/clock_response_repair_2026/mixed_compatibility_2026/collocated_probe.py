#!/usr/bin/env python3
"""Test a single-space clock-rate primitive; never enabled in the main solver."""
import argparse
import json
from pathlib import Path
import numpy as np
from collocated_jet import collocated_primitive, derivative_operator
from integrated_probe import IntegratedEvolution, probe, evolve_probe, BASE


class CollocatedEvolution(IntegratedEvolution):
    primitive=staticmethod(collocated_primitive)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path,required=True)
    parser.add_argument('--points',type=int,nargs='+',default=[129,257,513])
    parser.add_argument('--evolve',action='store_true');parser.add_argument('--dt',type=float,default=.00025)
    args=parser.parse_args();rows=[]
    for n in args.points:
        if args.evolve:
            state,snapshot=evolve_probe(n,args.dt,CollocatedEvolution)
            np.savez_compressed(args.result_file.parent/f'state_{n}.npz',r=np.linspace(0,3,n),state=state)
        else:
            with np.load(BASE/f'fresh_tangency_2026/offset_001/state_{n}.npz') as saved:state=saved['state']
            snapshot=None
        row=probe(n,state,CollocatedEvolution)
        row['snapshot']=snapshot
        row['evolved_with_candidate']=args.evolve
        if args.evolve:
            row['scope']='Fresh candidate evolution; convergence and kinematic consistency must be checked'
        row['operator']=derivative_operator(tuple(np.linspace(0,3,n)))[2]
        rows.append(row)
        args.result_file.write_text(json.dumps(dict(cases=rows,full_theory_status='OPEN'),indent=2)+'\n')
        print(json.dumps(row),flush=True)


if __name__=='__main__':main()
