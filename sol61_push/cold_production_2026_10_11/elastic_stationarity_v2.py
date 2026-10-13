"""Stationary local-Maxwellian screen for frozen CFG626 nu_mono cells."""
import ast,json,math
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
p=Path(__file__).parent; root=p.parents[1]
p626=root/'campaign_fresh_gravity/CFG626_kernel_recheck_anisotropic_target'
p544=root/'campaign_fresh_gravity/CFG544_settling_kinetic_consistency/cfg544.py'
def selected(path,names,ns):
    nodes=[n for n in ast.parse(path.read_text()).body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes}==set(names)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),ns)
ns={'np':np}
selected(p626/'cfg626.py',['h_rar','dh_rar','nu_m1_mono'],ns)
y=10**np.linspace(-12,12,240001)
yp=brentq(lambda t:float(ns['dh_rar'](t)),1,5);hp=float(ns['h_rar'](yp))
dh=np.maximum(ns['dh_rar'](y),.05*hp/(y+yp))
hm=float(ns['h_rar'](y[0]))+np.r_[0,np.cumsum(.5*(dh[1:]+dh[:-1])*np.diff(y))]
ns.update(LYG=np.log10(y),H_MONO=hm,nu_m1=ns['nu_m1_mono'])
selected(p544,['Mb_enc','Mph_enc'],ns)
cells=json.loads((p626/'cfg626_results_mono.json').read_text())['cells']
checks=[]; rows=[]
def ck(name,ok):checks.append(dict(name=name,passed=bool(ok)))
def density(M,r,h):
    # fourth-order centred derivative in log r; M'(r)/(4 pi r²)
    return (M(r*np.exp(-2*h))-8*M(r*np.exp(-h))+8*M(r*np.exp(h))-M(r*np.exp(2*h)))/(12*h*4*math.pi*r**3)
r=np.geomspace(.03,.8,201)
for name,c in cells.items():
    M=lambda r:ns['Mph_enc'](c,np.asarray(r))
    m0=float(M(.001));g=(ns['Mb_enc'](c,r)+M(r)-m0)*r/(r*r+.01**2)**1.5
    levels=[]
    for h in [.02,.01]:
        rho=lambda t:density(M,t,h/4)
        slope=(np.log(rho(r*np.exp(-2*h)))-8*np.log(rho(r*np.exp(-h)))+8*np.log(rho(r*np.exp(h)))-np.log(rho(r*np.exp(2*h))))/(12*h)
        s=-r*g/slope
        # If slope<0, smallest max relative hydrostatic residual over a constant s
        # is (smax-smin)/(smax+smin), achieved at harmonic mean of extrema.
        lo,hi=float(s.min()),float(s.max())
        levels.append(dict(h=h,smin=lo,smax=hi,ratio=hi/lo,minimax_fractional_force_residual=(hi-lo)/(hi+lo),best_constant_s=2*lo*hi/(lo+hi),all_density_positive=bool(np.all(rho(r)>0)),all_slopes_negative=bool(np.all(slope<0))))
    a,b=levels
    ck(name+' positive density and decreasing profile',b['all_density_positive'] and b['all_slopes_negative'])
    ck(name+' residual refinement',abs(a['minimax_fractional_force_residual']-b['minimax_fractional_force_residual'])<.005)
    rows.append(dict(cell=name,levels=levels))
# Independent known isothermal profile in a harmonic potential.
g=r; s0=.7
rho=lambda r:np.exp(-r*r/(2*s0))
h=.01
slope=(np.log(rho(r*np.exp(-2*h)))-8*np.log(rho(r*np.exp(-h)))+8*np.log(rho(r*np.exp(h)))-np.log(rho(r*np.exp(2*h))))/(12*h)
ck('harmonic isothermal control',np.max(abs(-r*g/slope/s0-1))<1e-7)
# Streaming residual at one point, independently evaluating derivatives of f.
# f=n (2pi s)^(-3/2) exp(-v²/2s), g points radially inward.
rad=.4;v=np.array([.6,.3,-.2]);gg=.9
n=lambda t:np.exp(-t);s=lambda t:.5+.2*t
f=lambda t,w:n(t)*(2*math.pi*s(t))**(-1.5)*np.exp(-np.dot(w,w)/(2*s(t)))
e=1e-5
stream=v[0]*(f(rad+e,v)-f(rad-e,v))/(2*e)-gg*(f(rad,v+np.array([e,0,0]))-f(rad,v-np.array([e,0,0])))/(2*e)
formula=f(rad,v)*v[0]*(-1-1.5*.2/s(rad)+np.dot(v,v)*.2/(2*s(rad)**2)+gg/s(rad))
ck('streaming polynomial finite difference',abs(stream-formula)<1e-9)
out=dict(checks=checks,all_pass=all(x['passed'] for x in checks),rows=rows,radius_range=[.03,.8],samples=201,scope='Local Maxwellian, zero mean flow, classical dilute elastic collision operator, static softened frozen CFG626 potential; no general nonthermal no-go')
(p/'elastic_stationarity_v2_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
