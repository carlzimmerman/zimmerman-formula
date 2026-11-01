import sys,math,json,time,resource,argparse
sys.dont_write_bytecode=True
from pathlib import Path
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'current_matching'))
sys.path.insert(0,str(BASE.parents[1]/'reviews/quantum_matching_2026_11_01/rg_threshold'))
from current import calculate
from relaxation import normal_data
L=16*math.pi**2


def main(out):
    start=time.monotonic();rows=[];checks={}
    for e,ratio in [(.01,1.2),(.03,1.1),(.03,1.3)]:
        xmin=7.367143721278508/math.sqrt(31*e);X=xmin*ratio;g=math.sqrt(29/200)*e;Q2=e/31+(e*xmin)**2;h=.02
        values=[]
        for t in [-h,0,h]:
            qq=Q2*math.exp(2*t);c=calculate(X,e,e,g,1.,qq);nd=normal_data(X,[e,e,g,1.],math.sqrt(qq))
            values.append((c['total'],nd['deltaF_angular']))
        dk=(values[2][0]-values[0][0])/(2*h);dh=(values[2][1]-values[0][1])/(2*h)
        gx=12*e*e/L;gb=(21/20*e*e-10*g*g)/L
        required=2*gx*X*X+60*gb*X*X
        heavy_expected=-300*g*g*X*X/L
        # Normalize a cancellation by its individual diagram sizes. At the
        # critical comparator the analytic required total is exactly zero.
        scale=max(abs(dk)+abs(dh)+abs(required),1e-100)
        err=abs(dk+dh-required)/scale
        eh=abs(dh-heavy_expected)/max(abs(heavy_expected),1e-100)
        checks['combined_'+str(e)+'_'+str(ratio)]=err<2e-7
        checks['heavy_'+str(e)+'_'+str(ratio)]=eh<2e-7
        rows.append(dict(e=e,X_over_tree_CW_min=ratio,graph_dlnQ=dk,heavy_dlnQ=dh,required_dlnQ=required,heavy_expected=heavy_expected,combined_relative_error=err,heavy_relative_error=eh))
    r=dict(claim_id='TP03_CURRENT_PULLBACK_CS',checks=checks,all_checks_pass=all(checks.values()),cases=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
           non_claims=['No finite radial coefficient or higher-current matching','No physical occupation/lifetime selection'])
    Path(out).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));assert r['all_checks_pass'],checks

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);main(p.parse_args().out)
