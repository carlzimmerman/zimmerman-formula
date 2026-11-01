import json,sys,time,resource
from pathlib import Path
import mpmath as mp
from scipy.optimize import brentq
from improved import evaluate,profile
from relaxation import normal_data
mp.mp.dps=50

def values(X,e):
    b=evaluate(X,e,1,'rg2');n=normal_data(b['X_running'],b['couplings'],b['Qm'])
    return b['U']+mp.mpf(str(n['deltaU_vac'])),mp.mpf(str(n['deltaU_vac'])),n

def stencil(fn,X,step):
    vs=[fn(X*mp.exp(i*step)) for i in (-2,-1,0,1,2)]
    return ((vs[0]-8*vs[1]+8*vs[3]-vs[4])/(12*step),(-vs[0]+16*vs[1]-30*vs[2]+16*vs[3]-vs[4])/(12*step**2))

def main(path):
    start=time.monotonic();rows=[];errors=[]
    for es in ['.01','.03','.05','.1']:
        e=mp.mpf(es);base=mp.mpf('7.3671437212785083116194')*mp.sqrt(e/31)/e
        fn=lambda x:values(x,e)[0]
        ds=lambda x,step=mp.mpf('.005'):stencil(fn,mp.mpf(x),step)
        rt=lambda fun,a,b:mp.mpf(brentq(lambda x:float(fun(mp.mpf(x))),float(a),float(b),xtol=2e-9,rtol=2e-11))
        xmin=rt(lambda x:ds(x)[0],base*mp.mpf('.7'),base*mp.mpf('1.3'))
        xp=rt(lambda x:ds(x)[1]-3*ds(x)[0],xmin*mp.mpf('1.01'),xmin*mp.mpf('1.6'))
        us0,uss0=ds(xmin);us,uss=ds(xp);B=uss0/9;den=(us*(xp/xmin)**2/(3*B))**(mp.mpf(3)/5)
        repeat=[]
        for xx in [xmin,xp,xmin*mp.mpf('1.2')]:
            a,b=ds(xx);aa,bb=ds(xx,mp.mpf('.01'));repeat.append(max(abs(a-aa),abs(b-bb)))
        w=xmin*mp.mpf('1.2');du,duu=ds(w);wss=2*du+duu;dP=5*du*(duu-3*du)/(9*wss)
        baseline=profile(w,e,1,'rg2');dadd,ddadd=stencil(lambda xx:values(xx,e)[1],w,mp.mpf('.0025'))
        composite=max(abs(du-baseline['U_s']-dadd),abs(duu-baseline['U_ss']-ddadd));errors.append(composite)
        v,add,normal=values(w,e)
        rows.append({'e':float(e),'X_min':float(xmin),'X_min_over_TP01':float(xmin/base),
                     'X_pressure_over_min':float(xp/xmin),'rho_over_rhostar_pressure':float(den),
                     'boundary_U_s':float(us),'boundary_Wss':float(2*us+uss),'Bcurv':float(B),
                     'witness_at_1p2':{'U_s':float(du),'Wss':float(wss),'dP_dlnrho':float(dP),
                                      'positive_source':bool(du>0),'radial_stable':bool(wss>0),'negative_compressibility':bool(dP<0),
                                      'deltaU_vac':float(add),'deltaF_over_F0':normal['deltaF_angular']/normal['F0']},
                     'max_step_repeat_abs_difference':float(max(repeat)),'composed_derivative_abs_difference':float(composite)})
    checks={'four_weak_trials':len(rows)==4,'composed_derivative_error_below_1e-12':max(errors)<mp.mpf('1e-12'),
            'coarse_fine_repeat_below_1e-12':max(r['max_step_repeat_abs_difference'] for r in rows)<1e-12,
            'positive_source_stable_pressure_boundaries':all(r['boundary_U_s']>0 and r['boundary_Wss']>0 for r in rows)}
    out={'claim_id':'TP02_RELAXED_PRESSURE','checks':checks,'cases':rows,'runtime_seconds_observed':time.monotonic()-start,
         'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'non_claims':['Finite heavyrelax subset only, not full finite2loop matching','Oldwaterbag coupling is comparator',
                       'Nativephase occupied E²term is a separate matching problem','Direct finite potential/kinetic diagrams uncomputed']}
    Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1])
