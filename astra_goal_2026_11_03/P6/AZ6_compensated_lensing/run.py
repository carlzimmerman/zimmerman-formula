import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from record import record
from scipy.integrate import quad

def calculate():
    rows=[]
    for R in [2.,4.]:
        point=1/(math.pi*R*R)-1/R**2/math.pi
        ds=lambda r:2/r**2*quad(lambda s:1.,0,r)[0]-1/r
        sis=ds(R)-ds(1)/R**2;oracle=(1-1/R)/R
        mut=1/(math.pi*R*R)+1/R**2/math.pi
        rows.append({'R':R,'point_U':point,'SIS_U':sis,'SIS_oracle':oracle,'mutate_point_U':mut})
    checks={'point_cancels':all(abs(q['point_U'])<=1e-11 for q in rows),'SIS_known_answer':all(abs(q['SIS_U']-q['SIS_oracle'])<=1e-11 for q in rows),'mutate_bites':all(q['mutate_point_U']>0.01 for q in rows)}
    return {'assertion_tested':'annular compensated projection cancels compact inner mass','label':'NOT EVALUABLE','scope':'P6 observations lack cleared raw inputs','footings':{f:{'label':'NOT EVALUABLE','identity_label':'PASS' if all(checks.values()) else 'NO VERDICT','rows':rows} for f in ['canonical','alt']},'bounds':{'R0':1,'R':[2,4],'point_mass':1,'SIS_amplitude':1},'checks':[{'name':k,'passed':bool(v)} for k,v in checks.items()],'free_physical_numbers':['kappa=1/2 FITTED','slip function and its coefficients unspecified: FITTED if introduced'],'residual_risks':['raw ellipticity/redshift weights not cleared','no metric field equations','existing cosmology-processed ESD not used']}
record(__file__,calculate)
