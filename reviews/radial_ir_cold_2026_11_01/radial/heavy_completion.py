import sys
sys.dont_write_bytecode=True
import json,math,time,resource
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]

def main(path):
    start=time.monotonic();dyn=json.load(open(HERE/'run_dynamics/result.json'));pp=json.load(open(ROOT/'reviews/finite_matching_2026_11_01/run_pressure/result.json'));rows=[]
    for c in dyn['cases']:
        e=c['e'];v=c['vacuum'][-1];X0=c['X_min'];J0=930*X0*X0/e;shift=-J0*v['m2']/(2*v['A']);vac=dict(relative_mass2_shift=shift,relative_mass_shift=shift/2,corrected_m2=v['m2']*(1+shift))
        d=c['circular_states'][1];r=next(a for a in pp['cases'] if a['e']==e and a['scheme']=='finite_matched' and a['interpolation_nodes']==29 and a['stencil_h']==.0025)['samples'][3];A=d['A'];N=r['Omega_ss'];D=r['fixed_charge_D'];C=r['partial_susceptibility'];q=r['omega2'];gap=D/(2*A);vr=d['vtheta2'];rr=N/D;bb=1-rr;X=X0*1.3;J=930*X*X/e;G=math.sqrt(C*(D-N)/(4*q));eq=q*J/A;es=J*gap/(2*A);et=J*gap/C;em=8*eq*G/C
        def base(x):
            S=(1+vr)*x+1;P=vr*x*(x+rr);disc=max(0,S*S-4*P);return 2*P/(S+math.sqrt(disc))
        def correction(x):
            y=base(x);p=y-x;K1=y-x-rr;K2=y-vr*x;dK1=eq*p+2*eq*y+es*p*p;dK2=et*p*p;dDet=dK1*K2+K1*dK2-em*y*p;der=2*y-(1+vr)*x-1
            return -dDet/der
        cut=-rr;opt=minimize_scalar(base,bounds=(0,cut),method='bounded',options={'xatol':1e-13});optc=minimize_scalar(lambda x:base(x)+correction(x),bounds=(0,cut*(1+1e-7)),method='bounded',options={'xatol':1e-13});g0=math.sqrt(-opt.fun*gap);gc=math.sqrt(-optc.fun*gap);cutshift=-eq+es*cut
        infrared=[dict(k2_over_gap=x,delta_frequency2_over_gap=correction(x),delta_slope=correction(x)/x) for x in (1e-3,1e-5,1e-7)]
        rows.append(dict(e=e,vacuum=vac,charged=dict(J=J,qJ_over_A=eq,Jgap_over_2A=es,Jgap_over_C=et,cutoff_k2_relative_shift=cutshift,Gamma_base=g0,Gamma_corrected=gc,Gamma_relative_shift=gc/g0-1,peak_k2_relative_shift=optc.x/opt.x-1,IR=infrared)))
    checks=dict(two_cases=len(rows)==2,small_expansion_parameters=all(max(abs(r['charged'][k]) for k in ('qJ_over_A','Jgap_over_2A','Jgap_over_C'))<1e-5 for r in rows),vacuum_pole_shift_small=all(abs(r['vacuum']['relative_mass2_shift'])<1e-5 for r in rows),IR_slope_unmodified=all(abs(r['charged']['IR'][-1]['delta_slope'])<abs(r['charged']['IR'][0]['delta_slope'])*1e-3 for r in rows))
    out=dict(claim_id='TP04_COVARIANT_HEAVY_COMPLETION',checks=checks,cases=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,non_claims=['Perturbative low-root reduction of known tree operator, no extra EFTghost mode','No p6/higherloop/nonlocal/gaugevariation completion','No physicalscale or cosmicstate selected'])
    Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
