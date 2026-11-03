import sys,math,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from record import record
import numpy as np
from scipy.special import gammainc
ROOT=Path(__file__).resolve().parents[3]
TOL='rebuild_2026_10_22/RQ3_acceptance_v2/tolerances.json'
ECC=dict(Mercury=.206,Venus=.007,Earth=.017,Mars=.093,Jupiter=.048,Saturn=.054)
GM=1.32712440018e20;AU=149597870700.;YR=365.25*86400;MAS=math.pi/(180*3600*1000)
def rate(A,a,e,n,N):
    t,w=np.polynomial.legendre.leggauss(N);E=math.pi*(t+1);c=np.cos(E);r=a*(1-e*c)
    return math.sqrt(1-e*e)/(n*a*e)*float(np.sum(.5*w*A(r)*(c-e)))
def monopole(r,a0,N,null=False):
    xi=.5*math.sqrt(GM/a0);ge=2.32e-10**2/(2.32e-10+a0)
    h=GM/r**2*gammainc(3,r/xi);mu,w=np.polynomial.legendre.leggauss(N);H=h[:,None];m=mu[None,:]
    y=np.sqrt(H*H+ge*ge+2*H*ge*m)/a0
    nu=np.zeros_like(y) if null else 1/(y*(np.sqrt(.25+1/y)+.5))
    return .5*np.sum(w[None,:]*nu*(H+ge*m),axis=1)
def calculate():
    tab=json.loads((ROOT/TOL).read_text())['PLANETS'];feet={}
    for f,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
        rows=[];errors=[];mut=[]
        for name,d in tab.items():
            e=ECC[name];a=d['a_au']*AU;n=math.sqrt(GM/a**3);root=math.sqrt(1-e*e)
            for fn,oracle in [(lambda r:np.ones_like(r),-root),(lambda r:r,-1.5*root),(lambda r:1/r**2,0.)]:
                errors.append(abs(rate(fn,1,e,1,256)-oracle))
            t,w=np.polynomial.legendre.leggauss(256);bad=float(np.sum(.5*w*np.cos(math.pi*(t+1))));mut.append(abs(bad+root))
            coarse=rate(lambda r:monopole(r,a0,80),a,e,n,128)*YR/MAS
            fine=rate(lambda r:monopole(r,a0,160),a,e,n,256)*YR/MAS
            null=rate(lambda r:monopole(r,a0,80,True),a,e,n,128)*YR/MAS
            linear=rate(lambda r:monopole(np.array([a]),a0,160)[0]*r/a,a,e,n,256)*YR/MAS
            sig=max(d['EPM'],d['INPOP']);z=abs(fine)/sig
            rows.append({'planet':name,'eccentricity':e,'a_au':d['a_au'],'rate_mas_year':fine,'linear_approx_mas_year':linear,'Z_EPM':abs(fine)/d['EPM'],'Z_INPOP':abs(fine)/d['INPOP'],'Z_generous':z,'margin':2-z,'refinement_Z':abs(fine-coarse)/sig,'null':null})
        checks={'three_known_answers':max(errors)<=1e-10,'mutation_bites':min(mut)>.5,'convergence':max(r['refinement_Z'] for r in rows)<=1e-5,'Newtonian_null':max(abs(r['null']) for r in rows)<=1e-12}
        lab=('PASS' if max(r['Z_generous'] for r in rows)<=2 else 'FAIL') if all(checks.values()) else 'NO VERDICT'
        feet[f]={'label':lab,'rows':rows,'checks':checks,'known_answer_max_error':max(errors),'mutate_min_error':min(mut)}
    return {'assertion_tested':'secular precession from exact squared-resolvent radial monopole on six eccentric orbits','label':'FAIL' if all(v['label']=='FAIL' for v in feet.values()) else 'NO VERDICT','footings':feet,'bounds':{'orbit_orders':[128,256],'angular_orders':[80,160],'eccentricities':ECC,'planets':list(tab)},'checks':[{'name':f+' '+k,'passed':bool(v)} for f,d in feet.items() for k,v in d['checks'].items()],'free_physical_numbers':['kappa=1/2 FITTED'],'residual_risks':['monopole only, orbital multipoles/parameter covariances uncomputed','external Galactic field conversion remains conditional']}
record(__file__,calculate,[TOL,'prep_2026/planetary_doors/BOUNDS.md','prep_2026/planetary_doors/laneR_bounds_compute.py'])
