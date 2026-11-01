import sys,json,math,resource,argparse,time
sys.dont_write_bytecode=True
from pathlib import Path
from full import calculate


def main(out):
    start=time.monotonic();checks={};rows=[]
    for X,e,Q2 in [(1.,.03,.01),(2.1,.03,.037),(1.,.01,.01)]:
        q=calculate(X,e,e,math.sqrt(29/200)*e,0,Q2,heavy=False)
        norm=sum(v['absolute_sum'] for v in q['diagram_diagnostic'].values())
        rel=abs(q['V2_diagrams_coefficient'])/max(norm,1e-300)
        q['SUSY_V2_relative_residual']=rel
        checks['SUSY_'+str(len(rows))]=rel<2e-9
        checks['controls_'+str(len(rows))]=all(v<2e-8 for v in list(q['model_controls'].values())+list(q['gauge_controls'].values()))
        rows.append(q)
    result={'claim_id':'TP03_ALL_VACUUM_SUSY','checks':checks,'all_checks_pass':all(checks.values()),'cases':rows,
            'runtime_seconds':time.monotonic()-start,'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'scope':'All ten SU5 finite vacuum classes; three f=0 supersymmetric controls, not pressure points.'}
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':checks,'relative_residuals':[r['SUSY_V2_relative_residual'] for r in rows],'runtime':result['runtime_seconds']},indent=2))
    assert result['all_checks_pass'],checks

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);main(p.parse_args().out)
