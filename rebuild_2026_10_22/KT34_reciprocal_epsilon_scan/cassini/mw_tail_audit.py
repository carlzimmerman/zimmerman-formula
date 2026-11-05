#!/usr/bin/env python3
"""Independent scalar replay of the reviewer's continuum MW upper bound.

Reads stored Newtonian baselines; does not rerun or change a gravity solver.
The analytic force lemma is audited separately, and baseline accuracy remains
a named input. G in the solver and in the assigned width are kept distinct.
"""
import argparse
import ast
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASELINE=ROOT/'rebuild_2026_10_22/KT33_reciprocal_filter/mw/grid_refined_run/results.json'
SOLVER=ROOT/'rebuild_2026_10_22/P4_v3_galaxy_tiles/p4_solver.py'
G_WIDTH=4.30091e-6
KPC_WIDTH=3.0857e19
A0={'canonical':9.3603e-11,'alt':1.1312e-10}
R0=8.122
EPSILON=2.5
L1_LOWER=219.9


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    constants=None
    for node in ast.parse(SOLVER.read_text()).body:
        if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Tuple):
            if [t.id for t in node.targets[0].elts]==['G_SI','MSUN','KPC']:
                constants=ast.literal_eval(node.value)
    assert constants is not None
    GSI,MSUN,KPC=constants
    g_solver=GSI*MSUN/(KPC*1e6)
    correction=math.sqrt(GSI*MSUN/(G_WIDTH*KPC_WIDTH*1e6))
    baseline=json.loads(BASELINE.read_text())
    out={'assertion':'Analytic continuum force bound replay on saved Newtonian baselines, conditional on continuum source mass and baseline error margins.',
         'epsilon_min':EPSILON,'L1_necessary_lower_km_s':L1_LOWER,
         'solver_constants':dict(GSI=GSI,MSUN=MSUN,KPC=KPC,Gk=g_solver),
         'width_constants':dict(Gk=G_WIDTH,KPC=KPC_WIDTH),
         'physical_boost_over_nominal_formula':correction,
         'footings':{},'checks':{}}
    for foot,a0 in A0.items():
        saved=baseline['footings'][foot]
        rows=saved['rows'];gas=saved['checks']['gas_mass']['analytic_full']
        assert len(rows)==1375 and saved['n_tested']==1375
        a0k_solver=a0*KPC/1e6; a0k_width=a0*KPC_WIDTH/1e6
        cases=[]
        for i,row in enumerate(rows):
            mass=row['Mstar']+gas
            rm_width=math.sqrt(G_WIDTH*mass/a0k_width)
            # Exact physical units; independent of the nominal a0*RM identity.
            delta_v2=2*math.sqrt(g_solver*mass*a0k_solver)*R0*R0*math.exp(.005)/(EPSILON*rm_width)**2
            vn=row['newton']['vc']
            cases.append(dict(index=i,cell=row['cell'],nominal_mass=mass,RM_width_kpc=rm_width,
                baseline_vN=vn,nominal_upper_km_s=math.sqrt(vn*vn+delta_v2),
                inflated_upper_km_s=math.sqrt((vn+1)**2+math.sqrt(1.01)*delta_v2),
                quadrature_mass_relative_to_nominal=row['mass']['full_source']/mass-1))
        nominal=max(cases,key=lambda c:c['nominal_upper_km_s'])
        inflated=max(cases,key=lambda c:c['inflated_upper_km_s'])
        out['footings'][foot]={'count':len(cases),'nominal_max':nominal,'inflated_max':inflated,
            'max_mass_relative_discrepancy':max(abs(c['quadrature_mass_relative_to_nominal']) for c in cases),
            'all_nominal_fail_L1':all(c['nominal_upper_km_s']<L1_LOWER for c in cases),
            'all_inflated_fail_L1':all(c['inflated_upper_km_s']<L1_LOWER for c in cases),
            'rows':cases}
        out['checks'][foot+'|both_margins']=out['footings'][foot]['all_nominal_fail_L1'] and out['footings'][foot]['all_inflated_fail_L1']
        print(foot,'nominal upper',nominal['nominal_upper_km_s'],'inflated upper',inflated['inflated_upper_km_s'],flush=True)
    out['all_checks_pass']=all(out['checks'].values())
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    assert out['all_checks_pass']


if __name__=='__main__':main()
