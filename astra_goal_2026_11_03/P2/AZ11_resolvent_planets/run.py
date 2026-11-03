import sys,math,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from record import record
import numpy as np
from scipy.special import gammainc
ROOT=Path(__file__).resolve().parents[3]
TOL='rebuild_2026_10_22/RQ3_acceptance_v2/tolerances.json'
def mono(h,e,a0,n=160,null=False):
    mu,w=np.polynomial.legendre.leggauss(n); y=np.sqrt(h*h+e*e+2*h*e*mu)/a0
    nu=np.zeros_like(y) if null else 1/(y*(np.sqrt(.25+1/y)+.5))
    return float(.5*np.sum(w*nu*(h+e*mu)))
def calculate():
    table=json.loads((ROOT/TOL).read_text())['PLANETS'];feet={};GM=1.32712440018e20;AU=149597870700.
    for f,a0 in [('canonical',9.3603e-11),('alt',1.1312e-10)]:
        xi=.5*math.sqrt(GM/a0);e=2.32e-10**2/(2.32e-10+a0);y=e/a0
        oracle=.5+math.sqrt(.25+1/y)-1-1/(6*y*math.sqrt(.25+1/y))
        small=mono(e*1e-4,e,a0)/(e*1e-4);err=abs(small/oracle-1)
        rows=[]
        for name,d in table.items():
            r=d['a_au']*AU;gb=GM/r**2;h=gb*gammainc(3,r/xi);sigma=d['dg_tight']*max(d['EPM'],d['INPOP'])/min(d['EPM'],d['INPOP'])
            v=mono(h,e,a0);low=mono(h,e,a0,80);mut=mono(gb,e,a0);null=mono(h,e,a0,null=True)
            rows.append({'planet':name,'A':v,'sigma':sigma,'Z':abs(v)/sigma,'margin':2-abs(v)/sigma,'old_tight_ratio':abs(v)/d['dg_tight'],'convergence':abs(v-low)/sigma,'mutate_Z':abs(mut)/sigma,'null':null})
        checks={'linear_known_answer':err<=1e-6,'null':all(abs(q['null'])<=1e-25 for q in rows),'angular_convergence':max(q['convergence'] for q in rows)<=1e-5,'central_force':abs(float(gammainc(3,1e-6))/(1e-6**3/6)-1)<=1e-5,'mutate_bites':max(q['mutate_Z'] for q in rows)>10}
        label=('PASS' if max(q['Z'] for q in rows)<=2 else 'FAIL') if all(checks.values()) else 'NO VERDICT'
        feet[f]={'label':label,'scope':'C1 point-radius diagnostic only; not full ephemeris verdict','rows':rows,'checks':checks,'linear_response':small,'linear_oracle':oracle,'relative_linear_error':err}
    return {'assertion_tested':'Gauss-law monopole of squared-resolvent source compared to frozen planetary diagnostic','label':'FAIL' if all(d['label']=='FAIL' for d in feet.values()) else 'NO VERDICT','footings':feet,'bounds':{'planets':list(table),'angular_orders':[80,160],'xi_over_rM':.5,'linear_test_h_over_e':1e-4},'checks':[{'name':f+' '+k,'passed':bool(v)} for f,d in feet.items() for k,v in d['checks'].items()],'free_physical_numbers':['kappa=1/2 FITTED'],'residual_risks':['constant-force ephemeris conversion applied to point-radius diagnostic; A1 restricts interpretation','uncomputed orbital multipoles','external-field spherical conversion conditional']}
record(__file__,calculate,[TOL,'prep_2026/planetary_doors/BOUNDS.md','astra_goal_2026_11_03/P2/AZ11_resolvent_planets/AMENDMENTS.md'])
