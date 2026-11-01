"""Finite vector-function transcription and supersymmetry identities."""
import argparse,json,math,resource
from pathlib import Path
import functions as F
from master_integrals import I,J


def main(out):
    checks={};rows=[]
    for x,Q2 in [(1.,1.),(.037,.071),(3.2,.7)]:
        def ffs(a,b,c):
            return J(a,Q2)*J(b,Q2)-J(a,Q2)*J(c,Q2)-J(b,Q2)*J(c,Q2)+(a+b-c)*I(a,b,c,Q2)
        # Martin8.31-8.36 divided by g²; x is common massive squared mass.
        parts={'SSS':-x*(.5*I(0,0,x,Q2)+I(0,x,x,Q2)),
               'FFS':ffs(0,x,0)+ffs(0,x,x)+2*ffs(x,x,0),
               'SSV':.5*(F.SSV(0,0,x,Q2)+F.SSV(0,x,x,Q2)),
               'VS':.5*F.VS(x,x,Q2),'VVS':x*F.VVS(x,x,0,Q2),
               'FFV':F.FFV(0,x,x,Q2)}
        scale=sum(abs(v) for v in parts.values())
        err=abs(sum(parts.values()))/max(scale,1e-300)
        checks['broken_SUSY_U1_'+str(x)]=err<2e-12
        # Martin8.37-8.41, massive charged matter in an unbroken gauge group.
        unbroken={'SS':J(x,Q2)**2,'FFS':4*ffs(0,x,x),'SSV':F.SSV(x,x,0,Q2),
                  'FFV':F.FFV(x,x,0,Q2),'barFFV':-x*F.barFFV(x,x,0,Q2)}
        scale2=sum(abs(v) for v in unbroken.values())
        err2=abs(sum(unbroken.values()))/max(scale2,1e-300)
        checks['unbroken_SUSY_U1_'+str(x)]=err2<2e-12
        rows.append({'x':x,'Q2':Q2,'broken_parts':parts,'broken_relative_residual':err,
                     'unbroken_parts':unbroken,'unbroken_relative_residual':err2})
    for name in ['SSV','VVS','FFV','barFFV']:
        fun=getattr(F,name)
        val=fun(.3,.7,.4,.9);rev=fun(.7,.3,.4,.9)
        checks[name+'_symmetry']=abs(val-rev)<2e-12*max(1,abs(val))
    checks['gauge_massless_zero']=F.gauge(0,0,0)==0
    val=F.gauge(.3,.7,.4,.9)
    checks['gauge_permutation']=all(abs(F.gauge(*v,.9)-val)<2e-11*max(1,abs(val)) for v in [(.7,.3,.4),(.4,.7,.3),(.3,.4,.7)])
    result={'claim_id':'TP03_VECTOR_FUNCTIONS','checks':checks,'all_checks_pass':all(checks.values()),
            'cases':rows,'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'scope':'Checks DRbar-prime graph functions, not the full SU5 vertices or kinetic matching.'}
    Path(out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'checks':checks,'peak_rss_bytes_macos':result['peak_rss_bytes_macos']},indent=2))
    assert result['all_checks_pass'],checks

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);main(p.parse_args().out)
