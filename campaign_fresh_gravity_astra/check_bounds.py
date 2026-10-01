"""Independent algebraic/numerical checks of AFG-003, plus false-rule controls."""
import argparse
import json
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    report=json.loads((HERE/'run_transition_001/results.json').read_text())
    evidence=[]
    for row in report['rows']:
        E,q=row['E'],row['mean_B_over_a0_today']
        if row['kernel']=='Q':
            bound=(q+E)/(q+1)
            # For the lognormal, Var(B)=q²(expm1(S)), from independent identity.
            prediction=bound+q*np.expm1(row['exact_log_variance'])/(q+1)
            assert abs(prediction/row['intrinsic_line_m4_over_m2_squared']-1)<1e-8
        else:
            bound=E*(-np.expm1(-np.sqrt(q)))**2/q
        assert row['intrinsic_line_m4_over_m2_squared']>=max(1.,bound)-1e-8
        evidence.append(dict(z=row['z'],q=q,kernel=row['kernel'],lower_bound=float(max(1.,bound)),
                             actual_K=row['intrinsic_line_m4_over_m2_squared']))
    y=np.logspace(-12,8,10001)
    R=y/(-np.expm1(-np.sqrt(y)))
    assert np.all(R>=np.sqrt(y)*(1-1e-14))
    def fr(x): return x/(-np.expm1(-np.sqrt(x)))
    # Deliberately false extension of Q concavity to the R branch.
    jensen_gap=float(.5*(fr(9.)+fr(11.))-fr(10.))
    assert jensen_gap>0
    first=json.loads((HERE/'run_002/results.json').read_text())['checks']
    # Deliberately wrong sign for variance correction must not pass closure.
    wrong=float(first['naive_mean_a0_ratio']-first['variance_correction'])
    assert abs(wrong-1)>.1
    out=dict(checkpoint='AFG-003',bounds=evidence,
             controls=dict(false_R_concavity_jensen_gap=jensen_gap,
                           wrong_sign_variance_inferred_a0=wrong),
             finite_checks='24 transition cases; 10001 point R lower-bound check; two deliberately false-rule controls.',
             scope='Self-review; universal inequalities rely on the written proofs, not on sampled checks.')
    (args.out/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__': main()
