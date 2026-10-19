"""FSP-U2: inverse top/bottom calibration, reduced SM only. No alpha input."""
import argparse, json, math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares

p=argparse.ArgumentParser()
p.add_argument('--output',required=True)
a=p.parse_args()
d=json.loads(Path('fine_structure_puzzle/uv_selection/inverse_inputs.json').read_text())
pi=math.pi
loop=16*pi*pi
by=41/6
mt=d['mt_GeV']
target=np.array([d['y_t_mt'],d['y_b_mt']])
# Independent weak and strong couplings, converted mZ -> mt at the model's order.
bnon=np.array([-19/6,-7.])
kinv=np.array([d['alpha_2_inverse_mz'],d['alpha_3_inverse_mz']])/(4*pi)-bnon/(8*pi*pi)*math.log(mt/d['mz_GeV'])

def prediction(params, cross, span=4000.,rtol=2e-10, method='DOP853'):
    fg,v=np.exp(params)
    gy2star=loop*fg/by
    fy=3/(8*pi*pi)*(v+gy2star/72)
    T=math.log(cross/mt)
    kT=kinv-bnon*T/(8*pi*pi)
    def gauge(t,grav):
        if grav:
            kn=bnon/(loop*fg)+(kT-bnon/(loop*fg))*np.exp(2*fg*(t-T))
            return gy2star,1/kn
        return 1/(1/gy2star+by*(T-t)/(8*pi*pi)),1/(kinv-bnon*t/(8*pi*pi))
    def fun(grav):
        def rhs(t,ylog):
            yt2,yb2=np.exp(2*ylog)
            gy2,gn=gauge(t,grav)
            common=2.25*gn[0]+8*gn[1]
            return np.array([4.5*yt2+1.5*yb2-17/12*gy2-common,4.5*yb2+1.5*yt2-5/12*gy2-common])/loop-(fy if grav else 0)
        return rhs
    uv=np.log(np.sqrt([v+gy2star/3,v]))
    s1=solve_ivp(fun(True),(T+span,T),uv,method=method,rtol=rtol,atol=rtol/100,max_step=20)
    assert s1.success
    s2=solve_ivp(fun(False),(T,0),s1.y[:,-1],method=method,rtol=rtol,atol=rtol/100,max_step=1)
    assert s2.success
    return {'yt_yb':np.exp(s2.y[:,-1]),'gY_mt':math.sqrt(gauge(0,False)[0]),'fg':fg,'fy':fy,'yb_UV_squared':v,'gY_UV':math.sqrt(gy2star)}

def fit(cross,start=None):
    start=np.log([.009,1e-7]) if start is None else start
    def residual(p): return np.log(prediction(p,cross)['yt_yb']/target)
    opt=least_squares(residual,start,bounds=(np.log([.0005,math.exp(-40)]),np.log([.1,math.exp(-2)])),xtol=1e-11,ftol=1e-11,gtol=1e-11,diff_step=1e-4,max_nfev=80)
    center=prediction(opt.x,cross)
    variants=[prediction(opt.x,cross,span,rtol) for span,rtol in [(2000.,2e-10),(4000.,2e-11)]]
    orthogonal=prediction(opt.x,cross,4000.,2e-10,method='Radau')
    eps=1e-4
    J=np.column_stack([(residual(opt.x+eps*np.eye(2)[j])-residual(opt.x-eps*np.eye(2)[j]))/(2*eps) for j in range(2)])
    assert opt.success and max(abs(residual(opt.x)))<1e-6
    assert max(np.max(np.abs(v['yt_yb']/center['yt_yb']-1)) for v in variants)<1e-6
    algorithm_change=float(np.max(np.abs(orthogonal['yt_yb']/center['yt_yb']-1)))
    assert algorithm_change<1e-6
    out={k:(v.tolist() if isinstance(v,np.ndarray) else float(v)) for k,v in center.items()}
    out.update({'crossover_GeV':cross,'residual_log':residual(opt.x).tolist(),'evaluations':opt.nfev,'jacobian_log_y_vs_log_parameters':J.tolist(),'jacobian_determinant':float(np.linalg.det(J)),'jacobian_singular_values':np.linalg.svd(J,compute_uv=False).tolist(),'cutoff_tolerance_max_relative_change':max(float(np.max(np.abs(v['yt_yb']/center['yt_yb']-1))) for v in variants),'Radau_vs_DOP853_max_relative_change':algorithm_change})
    return out,opt.x

central,params=fit(d['planck_GeV'])
sensitivity,_=fit(d['other_crossover_GeV_for_sensitivity_only'],params)
out={'model':d['model'],'target_yukawas':target.tolist(),'g2_g3_mt':np.sqrt(1/kinv).tolist(),'alpha_or_hypercharge_numerical_input':False,'central':central,'crossover_sensitivity_only':sensitivity,'interpretation':'Two Yukawa data do locally fix two parameters and yield gY in this reduced model; this is a correlated prediction conditional on all stated model and matching assumptions, not an absolute derivation of alpha.'}
Path(a.output).parent.mkdir(parents=True,exist_ok=True)
Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
