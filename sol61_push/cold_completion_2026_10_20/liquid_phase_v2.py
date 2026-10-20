"""Uniform stationary-phase equation of state of the explicit alternative action."""
from pathlib import Path
import json, math, resource, sys
import numpy as np
from scipy.optimize import root

base=Path(__file__).parent
p=json.loads((base/'run_001/results.json').read_text())['parameters']
M=p['M_chi'];a=p['a'];g=p['g'];MX2=p['MX2'];lam=p['lambda']
checks=[]
def check(name,v): checks.append({'name':name,'pass':bool(v)})
def up(h):return M*M*h-3*M*h*h/8+h**3
def upp(h):return M*M-3*M*h/4+3*h*h
def U(h):return M*M*h*h/2-M*h**3/8+h**4/4
def calc(I,h,om):
    D=MX2-4*om*om; A=lam-g*g/D
    b=-g*I/D
    grand=(1-om*om)*I+A*I*I+a*h*I+U(h)
    q=2*om*(I+4*b*b)
    pressure=-grand
    energy=om*q-pressure
    Ap=-8*g*g*om/(D*D)
    J=np.array([[2*A,a],[a,upp(h)]])
    dI,dh=np.linalg.solve(J,-np.array([-2*om+2*Ap*I,0.]))
    db=-g*(dI/D+8*om*I/(D*D))
    dq=2*(I+4*b*b)+2*om*(dI+8*b*db)
    cs2=q/(om*dq)
    return {'I':float(I),'chi':float(h),'X':float(b),'omega':float(om),'pressure':float(pressure),
            'charge_density':float(q),'energy_density':float(energy),'E_over_Q':float(energy/q),
            'long_wavelength_adiabatic_cs2':float(cs2),'dq_domega':float(dq),
            'amplitude_Hessian_eigenvalues':np.linalg.eigvalsh(J).tolist(),
            'D_X':float(D),'grand':float(grand),'dI_domega':float(dI)}
def eq3(z):
    I,h,om=z; A=lam-g*g/(MX2-4*om*om)
    return np.array([(1-om*om)+2*A*I+a*h,(up(h)+a*I)/10000,
                    ((1-om*om)*I+A*I*I+a*h*I+U(h))/50])
# Regression: the previously omitted a*h*I must appear in the grand potential.
ii,hh,ww=25.,-.5,.9
bb=-g*ii/(MX2-4*ww*ww)
Vdirect=ii+MX2*bb*bb+2*g*bb*ii+lam*ii*ii+a*hh*ii+U(hh)
Gdirect=Vdirect-ww*ww*(ii+4*bb*bb)
check('reduced grand equals direct full potential',abs(calc(ii,hh,ww)['grand']-Gdirect)<1e-9)
ee=1e-4
Gp=calc(ii+ee,hh,ww)['grand'];Gm=calc(ii-ee,hh,ww)['grand']
Gprime=(Gp-Gm)/(2*ee)
expected=(1-ww*ww)+2*(lam-g*g/(MX2-4*ww*ww))*ii+a*hh
check('grand I derivative reproduces field equation',abs(Gprime-expected)<1e-7)
s=root(eq3,[48.,-.96,.87],tol=1e-11)
I,h,om=s.x
c=calc(I,h,om)
check('coexistence nonlinear equations',np.max(np.abs(eq3(s.x)))<1e-9)
check('nonzero charged subthreshold state',I>1 and .85<om<1 and c['D_X']>0)
check('zero pressure',abs(c['pressure'])/c['energy_density']<1e-9)
check('energy per charge equals omega at coexistence',abs(c['E_over_Q']/om-1)<1e-9)
check('positive local amplitude Hessian',min(c['amplitude_Hessian_eigenvalues'])>0)
check('positive compressibility and subluminal low-frequency sound',c['dq_domega']>0 and 0<c['long_wavelength_adiabatic_cs2']<1)
rows=[]
for delta in [-1e-3,-1e-5,0,1e-5,1e-3]:
    w=om+delta
    def eq2(z):
        ii,hh=z;A=lam-g*g/(MX2-4*w*w)
        return [(1-w*w)+2*A*ii+a*hh,(up(hh)+a*ii)/10000]
    ss=root(eq2,[I,h],tol=1e-11)
    row=calc(*ss.x,w);rows.append(row)
    check('uniform branch residual '+str(delta),max(abs(v) for v in eq2(ss.x))<1e-9)
eps=1e-5
dP=(rows[3]['pressure']-rows[1]['pressure'])/(2*eps)
dq=(rows[3]['charge_density']-rows[1]['charge_density'])/(2*eps)
check('dP/domega equals charge density',abs(dP/c['charge_density']-1)<1e-5)
check('implicit derivative agrees finite difference',abs(dq/c['dq_domega']-1)<1e-5)
# At chi's low-gradient static minimum h=-(a/M²)I+O(I²), eliminating
# the neutral field contributes -a² I²/(2M²)+a³ I³/(8M^5)+O(I^4).
quartic=lam-a*a/(2*M*M)
sextic=a**3/(8*M**5)
check('neutral-mediated attraction at low density',quartic<0)
check('positive leading saturation term',sextic>0)
check('bound profile omega above candidate bulk coexistence',all(r['omega']>om for r in json.loads((base/'run_001/results.json').read_text())['rows']))
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
check('measured RSS below 1 GB',rss<1_000_000_000)
out={'scope':'Homogeneous classical stationary amplitude and adiabatic Goldstone thermodynamics; no proof of full perturbation stability or relaxation rate.',
     'coexistence':c,'nearby_branch':rows,'finite_difference_dP_domega':dP,'finite_difference_dq_domega':dq,
     'neutral_only_static_effective_V_coefficients':{'I':1,'I_squared':quartic,'I_cubed':sextic,
         'validity':'Low I and slow neutral gradients/time dependence. X exchange is not eliminated in these displayed coefficients; near-resonant X must retain its frequency dependence.'},
     'checks':checks,'n_checks':len(checks),'all_checks_pass':all(z['pass'] for z in checks),'peak_rss_bytes_macos':rss}
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
raise SystemExit(0 if out['all_checks_pass'] else 1)
