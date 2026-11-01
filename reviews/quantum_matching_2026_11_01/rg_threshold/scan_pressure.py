import json,sys,resource,time
from pathlib import Path
import mpmath as mp
from scipy.optimize import brentq
from improved import evaluate,profile
mp.mp.dps=50

def num(X,e,eta,scheme,step=mp.mpf('.002')):
    vs=[evaluate(mp.mpf(X)*mp.exp(j*step),e,eta,scheme)['U'] for j in (-2,-1,0,1,2)]
    return ((vs[0]-8*vs[1]+8*vs[3]-vs[4])/(12*step),
            (-vs[0]+16*vs[1]-30*vs[2]+16*vs[3]-vs[4])/(12*step**2))

def root(fun,lo,hi):
    flo=fun(lo);fhi=fun(hi)
    if flo*fhi>0:return None
    return mp.mpf(brentq(lambda x:float(fun(mp.mpf(x))),float(lo),float(hi),xtol=1e-12,rtol=2e-12))

def main(path,e_string):
    e=mp.mpf(e_string);xbase=mp.mpf('7.3671437212785083116194388754783235351121768')*mp.sqrt(e/31)/e
    choices=[('fixed',1),('rg1',1),('rg2',.5),('rg2',1),('rg2',2),('rg2log',.5),('rg2log',2)]
    results=[];errors=[];start=time.monotonic()
    for scheme,eta in choices:
        row={'scheme':scheme,'eta':eta,'e':float(e)}
        fn=lambda x:num(x,e,eta,scheme)
        xmin=root(lambda x:fn(x)[0],xbase*mp.mpf('.7'),xbase*mp.mpf('1.3'))
        if xmin is None:row['status']='minimum_not_bracketed';results.append(row);continue
        xp=root(lambda x:fn(x)[1]-3*fn(x)[0],xmin*mp.mpf('1.01'),xmin*mp.mpf('1.6'))
        xr=root(lambda x:fn(x)[1]+2*fn(x)[0],xmin*mp.mpf('1.5'),xmin*mp.mpf('2.5'))
        pmin=profile(xmin,e,eta,scheme);B=pmin['U_ss']/9
        row.update(status='roots_found' if xp is not None and xr is not None else 'partial_roots',
                   X_min=float(xmin),X_min_over_TP01=float(xmin/xbase),U_min=float(pmin['U']),Bcurv=float(B),
                   Q_at_min=float(pmin['Q']),F_at_min=float(pmin['F']),
                   critical_ratio_drift_at_min=float(pmin.get('critical_ratio_drift',0)))
        u0,uu0=fn(xmin);errors.extend([abs(u0-pmin['U_s']),abs(uu0-pmin['U_ss'])])
        if xp is not None:
            pp=profile(xp,e,eta,scheme);us=pp['U_s'];uss=pp['U_ss'];wss=2*us+uss;s=mp.log(xp/xmin)
            dens=(us*mp.exp(2*s)/(3*B))**(mp.mpf(3)/5) if us>0 and B>0 else mp.nan
            row.update(X_pressure=float(xp),X_pressure_over_min=float(xp/xmin),
                       rho_over_rhostar_pressure=float(dens),boundary_U_s=float(us),boundary_Wss=float(wss),
                       boundary_compressibility_residual=float(uss-3*us))
            uf,uuf=fn(xp);errors.extend([abs(uf-us),abs(uuf-uss)])
        if xr is not None:row['X_radial_over_min']=float(xr/xmin)
        witness=xmin*mp.mpf('1.2');p=profile(witness,e,eta,scheme)
        us=p['U_s'];uss=p['U_ss'];wss=2*us+uss
        dP=5*us*(uss-3*us)/(9*wss)
        row['witness_at_1p2']={'U_s':float(us),'Wss':float(wss),'Uss_minus3Us':float(uss-3*us),
                              'dP_dlnrho':float(dP),'positive_source':bool(us>0),'radial_stable':bool(wss>0),
                              'negative_compressibility':bool(dP<0),'a':float(p['a']),'a_prime':float(p['a_prime'])}
        uf,uuf=fn(witness);errors.extend([abs(uf-us),abs(uuf-uss)])
        results.append(row)
    central=next((r for r in results if r['scheme']=='rg2' and r['eta']==1 and 'X_min'in r),None)
    refine=None
    if central:
        xx=mp.mpf(central['X_min']);a=evaluate(xx,e,1,'rg2',32);b=evaluate(xx,e,1,'rg2',64)
        refine={'U_abs_difference':float(abs(a['U']-b['U'])),'F_relative_difference':float(abs(a['F']/b['F']-1))}
    checks={'seven_recorded_schemes':len(results)==7,
            'independent_derivative_abs_errors_below_1e-13':max(errors)<mp.mpf('1e-13'),
            'all_found_pressure_boundaries_positive_source':all(r.get('boundary_U_s',1)>0 for r in results),
            'all_found_pressure_boundaries_radially_stable':all(r.get('boundary_Wss',1)>0 for r in results),
            'RK_refinement_U_abs_below_1e-20':refine is not None and refine['U_abs_difference']<1e-20}
    summary={'claim_id':'TP02_WEAK_PRESSURE','e':float(e),'checks':checks,'schemes':results,
             'max_independent_derivative_abs_error':float(max(errors)),'RK_refinement':refine,
             'runtime_seconds_observed':time.monotonic()-start,'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             'non_claims':['Unknown finite reduced two-loop potential remains; scale variation is not its bound',
                           'Old waterbag exp2s portal only; native phase source tested separately',
                           'F has RG angular metric only, no finite kinetic threshold matching',
                           'Finite roots near inherited branch do not classify all stationary branches']}
    Path(path).write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2));assert all(checks.values()),checks

if __name__=='__main__':main(sys.argv[1],sys.argv[2])
