"""Actual phase-charge pressure on pinned RG U and angular F; no waterbag portal."""
import sys
sys.dont_write_bytecode=True
import json,resource,time
from pathlib import Path
import mpmath as mp
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/quantum_matching_2026_11_01/rg_threshold'))
from improved import evaluate,profile
mp.mp.dps=50

def main(path):
    start=time.monotonic();e=mp.mpf('.03');c=e/31;xs=mp.sqrt(c)/e;rows=[];checks={};errs=[]
    for scheme,eta in [('fixed','1'),('rg1','1'),('rg2log','.5'),('rg2log','1'),('rg2log','2')]:
        eta=mp.mpf(eta)
        U=lambda x:evaluate(x,e,eta=eta,scheme=scheme,steps=32)['U']
        du=lambda x:mp.diff(lambda s:U(x*mp.exp(s)),0)
        x0=mp.findroot(lambda z:du(z*xs)/(c*c),(mp.mpf(7),mp.mpf(8)),tol=mp.mpf('1e-30'),maxsteps=40)*xs
        assert 7<x0/xs<8
        u0=U(x0)
        def point(ratio,steps=32):
            x=x0*ratio;o=profile(x,e,eta=eta,scheme=scheme,steps=steps);us=o['U_s'];uss=o['U_ss'];a=o['a'];ap=o['a_prime'];F=o['F'];D=uss+(a-ap/a)*us;N=uss-(a+ap/a)*us
            A=us/a;du_=o['U']-u0;charge=mp.sqrt(4*F*A);P=A-du_;energy=A+du_
            return dict(X0=x,X0_over_min=ratio,U=o['U'],U_s=us,U_ss=uss,F=F,a=a,a_prime=ap,D=D,N=N,charge_theta=charge,epsilon_ex=energy,P_ex=P,w_ex=P/energy,cs2_IR=N/D,dP_dlnn=2*us*N/(a*D),positive_source=bool(A>0),radially_stable=bool(D>0))
        root=mp.findroot(lambda r:point(r)['N']/(c*c),(mp.mpf('1.12'),mp.mpf('1.3')),tol=mp.mpf('1e-28'),maxsteps=35)
        assert mp.mpf('1.12')<root<mp.mpf('1.5')
        sample=[point(mp.mpf(r)) for r in ('1.0001','1.01','1.05','1.12','1.2','1.3')];boundary=point(root)
        # Direct thermodynamic finite difference; no imported pressure-derivative expression.
        ratio=mp.mpf('1.05');ds=mp.mpf('5e-5');pp=point(ratio*mp.exp(ds));pm=point(ratio*mp.exp(-ds));direct=(pp['P_ex']-pm['P_ex'])/(mp.log(pp['charge_theta'])-mp.log(pm['charge_theta']));error=abs(direct/sample[2]['dP_dlnn']-1);errs.append(error)
        conv=None
        if scheme=='rg2log' and eta==1:
            old=mp.mp.dps;mp.mp.dps=60;q64=point(mp.mpf('1.2'),64);mp.mp.dps=old;q32=sample[4];conv={k:float(abs(q64[k]-q32[k])) for k in ('U_s','U_ss','a','a_prime','cs2_IR')}
        encode=lambda d:{k:(bool(v) if isinstance(v,bool) else float(v)) for k,v in d.items()}
        rows.append(dict(scheme=scheme,eta=float(eta),X0_min=str(x0),phase_boundary_ratio=str(root),samples=[encode(q) for q in sample],boundary=encode(boundary),direct_pressure_relative_error=str(error),central_step_precision_repeat=conv))
        print(json.dumps({k:rows[-1][k] for k in ('scheme','eta','X0_min','phase_boundary_ratio','boundary','direct_pressure_relative_error')},indent=2),flush=True)
    checks={'five_cases':len(rows)==5,'positive_source_samples':all(q['positive_source'] for r in rows for q in r['samples']),'radially_stable_samples':all(q['radially_stable'] for r in rows for q in r['samples']),'direct_pressure_relative_error_below_1e-5':max(errs)<mp.mpf('1e-5'),'canonical_a_identity':max(abs(q['a']-2)+abs(q['a_prime']) for q in rows[0]['samples'])<1e-35,'central_RK_precision_repeat_below_1e-10':max(rows[3]['central_step_precision_repeat'].values())<1e-10}
    result=dict(claim_id='TP02_RG_NATIVE_PHASE',checks=checks,cases=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,non_claims=['F is RG wavefunction contribution without finite angular kinetic matching','U omits finite two-loop remainder and nonperturbative sectors','No selected current, abundance, stable quantum charge or gravity/halo model'])
    Path(path).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(checks,indent=2));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
