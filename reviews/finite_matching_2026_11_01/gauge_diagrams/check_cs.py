"""Reduced fixed-X two-loop Callan-Symanzik check, including heavy shift."""
import sys,json,math,time,resource,argparse
sys.dont_write_bytecode=True
from pathlib import Path
import mpmath as mp
from full import calculate,LOOP,ROOT
from improved import reduced_D1_threshold,C2


def main(out):
    start=time.monotonic();mp.mp.dps=55;rows=[];checks={}
    zmin=7.367143721278508
    for e,ratio in [(.03,1.1),(.03,1.3),(.01,1.2)]:
        xmin=zmin/math.sqrt(31*e);X=xmin*ratio;Q2=e/31+(e*xmin)**2
        h=.002
        values=[calculate(X,e,e,math.sqrt(29/200)*e,1.,Q2*math.exp(2*t),True) for t in [-h,0,h]]
        dgraph=(values[2]['V2_diagrams_coefficient']-values[0]['V2_diagrams_coefficient'])/(2*h)
        dred=(values[2]['V2_reduced_coefficient']-values[0]['V2_reduced_coefficient'])/(2*h)
        c=[mp.mpf(e),mp.mpf(e),mp.sqrt(mp.mpf(29)/200)*mp.mpf(e),mp.mpf(1)]
        rhs=-float(reduced_D1_threshold(mp.mpf(X),c,mp.sqrt(Q2))+C2(c))*LOOP**2
        scale=max(abs(rhs),abs(dred),1e-300)
        err=abs(dred-rhs)/scale
        row={'e':e,'X_over_tree_CW_min':ratio,'Q2':Q2,'dlnQ_diagrams_coefficient':dgraph,
             'dlnQ_reduced_coefficient':dred,'CS_required_coefficient':rhs,'relative_error':err,
             'heavy_scale_derivative':dred-dgraph,'central':values[1]}
        rows.append(row)
        checks['CS_'+str(e)+'_'+str(ratio)]=err<2e-5
        print(json.dumps({k:v for k,v in row.items() if k!='central'}),flush=True)
    result={'claim_id':'TP03_REDUCED_CS','checks':checks,'all_checks_pass':all(checks.values()),'cases':rows,
            'runtime_seconds':time.monotonic()-start,'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'scope':'Complete finite two-loop reduced potential at fixed original singlet X, with heavy term counted once. Couplings do not run during Q derivative. Retained X is gauge singlet.'}
    Path(out).write_text(json.dumps(result,indent=2)+'\n');assert result['all_checks_pass'],checks

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);main(p.parse_args().out)
