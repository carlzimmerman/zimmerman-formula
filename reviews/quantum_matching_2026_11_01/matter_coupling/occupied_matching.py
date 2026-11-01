import sys
sys.dont_write_bytecode=True
import json,time,resource,math
from pathlib import Path
import mpmath as mp
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/quantum_matching_2026_11_01/rg_threshold'))
from improved import evaluate
from relaxation import normal_data_reference
mp.mp.dps=50

def main(path):
    start=time.monotonic();e=mp.mpf('.03');xs=mp.sqrt(e/31)/e;cache={};Jlight=1/(16*mp.pi**2)
    def coefficients(lx):
        key=float(lx).hex()
        if key not in cache:
            x=mp.exp(mp.mpf(float(lx)));base=evaluate(x,e,1,'rg2',32);norm=normal_data_reference(x,e)
            get=lambda k:mp.mpf(float(norm[k]))
            ca,cb,ha,hb,fb=map(get,('CWa','CWb','Haa','Hbb','F_b'))
            cache[key]=dict(V=base['U']-(ca*ca/ha+cb*cb/hb)/2,F=base['F']-cb*fb/hb,J=fb*fb/hb,norm=norm,baseU=base['U'],baseF=base['F'])
        return cache[key]
    def stencil(lx,h):
        pts=[coefficients(lx+j*h) for j in (-2,-1,0,1,2)];out=dict(pts[2])
        for key in ('V','F','J'):
            z=[p[key] for p in pts];out[key+'s']=(z[0]-8*z[1]+8*z[3]-z[4])/(12*h);out[key+'ss']=(-z[0]+16*z[1]-30*z[2]+16*z[3]-z[4])/(12*h*h)
        return out
    def point(lx,h,vvac,light=False):
        d=stencil(lx,h);vs,fs,js=d['Vs'],d['Fs'],d['Js'];disc=fs*fs+2*js*vs;assert disc>0
        w=2*vs/(fs+mp.sqrt(disc));assert w>0
        om=mp.sqrt(w);J=d['J']+(Jlight if light else 0);F=d['F'];N=d['Vss']-d['Fss']*w-d['Jss']*w*w/2;C=2*F+6*J*w;mix=-2*om*(fs+js*w);D=N+mix*mix/C;n=2*om*(F+J*w)
        P=F*w+J*w*w/2-d['V']+vvac;E=F*w+3*J*w*w/2+d['V']-vvac;cs=n*N/(om*C*D)
        nd=d['norm'];da=-mp.mpf(nd['CWa'])/mp.mpf(nd['Haa']);db=-(mp.mpf(nd['CWb'])-w*mp.mpf(nd['F_b']))/mp.mpf(nd['Hbb'])
        return dict(X0=float(mp.exp(lx)),omega2=float(w),n=float(n),P_ex=float(P),epsilon_ex=float(E),w_ex=float(P/E),cs2_IR=float(cs),Omega_ss=float(N),fixed_charge_D=float(D),partial_susceptibility=float(C),deltaa_relative=float(da/mp.mpf(nd['a0'])),deltab_relative=float(db/mp.mpf(nd['b0'])),J_heavy=float(d['J']),J_light=float(Jlight if light else 0),light_energy_fraction=float(3*Jlight*w*w/(2*E)) if light else 0,rawP=P,rawn=n,rawcs=cs)
    cases=[];errors=[]
    for hh in (.01,.005,.0025):
        h=mp.mpf(hh);lo=float(mp.log(7*xs));hi=float(mp.log(8*xs));lx0=brentq(lambda l:float(stencil(l,h)['Vs']),lo,hi,xtol=1e-12);vac=coefficients(lx0)['V']
        nfun=lambda ratio:point(lx0+math.log(ratio),h,vac)['Omega_ss']
        boundary=brentq(nfun,1.12,1.35,xtol=1e-11);ratios=(1.01,1.05,1.12,1.2,1.3)
        samp=[point(lx0+math.log(r),h,vac) for r in ratios];bound=point(lx0+math.log(boundary),h,vac);withlight=point(lx0+math.log(boundary),h,vac,True)
        ds=1e-4;plus=point(lx0+math.log(1.05)+ds,h,vac);minus=point(lx0+math.log(1.05)-ds,h,vac);direct=(plus['rawP']-minus['rawP'])/(mp.log(plus['rawn'])-mp.log(minus['rawn']));expected=samp[1]['rawcs']*samp[1]['rawn']*mp.sqrt(samp[1]['omega2']);err=abs(direct/expected-1);errors.append(err)
        clean=lambda d:{k:v for k,v in d.items() if not k.startswith('raw')}
        cases.append(dict(stencil_h=hh,X0_min=float(mp.exp(lx0)),boundary_ratio=boundary,boundary=clean(bound),boundary_with_assumed_gaugino_reservoir=clean(withlight),samples=[dict(X0_over_min=r,**clean(p)) for r,p in zip(ratios,samp)],direct_pressure_relative_error=float(err)))
        print(json.dumps(cases[-1],indent=2),flush=True)
    maxshift=max(max(abs(q['deltaa_relative']),abs(q['deltab_relative'])) for c in cases for q in c['samples'])
    checks={'three_field_stencils':len(cases)==3,'last_two_boundary_ratio_difference_below_1e-4':abs(cases[-1]['boundary_ratio']-cases[-2]['boundary_ratio'])<1e-4,'direct_pressure_error_below_1e-4':max(errors)<mp.mpf('1e-4'),'heavy_relative_shifts_below_01':maxshift<.01,'positive_partial_susceptibility_and_D':all(q['partial_susceptibility']>0 and q['fixed_charge_D']>0 for c in cases for q in c['samples'])}
    out=dict(claim_id='TP02_OCCUPIED_HEAVY_PHASE',checks=checks,cases=cases,max_heavy_relative_shift=maxshift,normal_evaluation_count=len(cache),runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,non_claims=['Known normal heavy relaxation term, not complete finite two-loop/finite kinetic matching','Optional gaugino reservoir is assumed free equilibrium, not selected occupation or all-IR control','No quantum charge lifetime or physical halo/gravity state selected'])
    Path(path).write_text(json.dumps(out,indent=2)+'\n');assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
