"""Full finite-momentum strict HB piN tensor, source 0712.1294v2."""
from pathlib import Path
import json
import sys
import mpmath as mp

BASE=Path(__file__).resolve().parent
cfg=json.loads((BASE/'FINITE_BAND_INPUTS.json').read_text())
mp.mp.dps=cfg['decimal_digits']
checks=[]

def check(name,ok):
    if not ok:
        raise AssertionError(name)
    checks.append(name)

def amplitudes(r,x,integral=False):
    t=r*r
    h=1-x*x
    v=t*h
    w=-t*x*x
    k=-t
    H=mp.sqrt(1-w)
    D=4*v+k*k
    if integral:
        J=mp.quad(lambda y: 1/mp.sqrt(1+t*y-t*h*y*y),[0,1])
    else:
        I=mp.atan(r/(2*mp.sqrt(h)))+mp.atan(r*(1-2*x*x)/(2*mp.sqrt(h)*H))
        J=I/mp.sqrt(v)
    B1=mp.mpf(3)/2+1/v-(1+1/v)*H-(2+k/v)*J/2
    B2=-(mp.mpf(3)/2+(mp.mpf(1)/2+1/k+1/w)*k/v)-(w*k/D)*(1/v-k/(2*v))+(2-(v/w)*(1-w)+k*w/D)*H/v+(2+3*k/v+k)*J/2
    return B1,(k/v)*B2

for rr in cfg['branch_test_r']:
    for xx in cfg['test_x']:
        r,x=mp.mpf(rr),mp.mpf(xx)
        f=amplitudes(r,x)
        g=amplitudes(r,x,True)
        check('parameter integral '+rr+','+xx,max(abs(a-b) for a,b in zip(f,g))<mp.mpf('1e-45'))

soft=[]
for xx in cfg['test_x']:
    x=mp.mpf(xx)
    r=mp.mpf(cfg['soft_r'])
    b1,b2=amplitudes(r,x)
    expect1=(1-11*x*x)/24
    expect2=mp.mpf(11)/24
    error=max(abs(b1/r**2-expect1),abs(b2/r**2-expect2))
    check('two scalar soft limits '+xx,error<mp.mpf('1e-8'))
    check('no seagull residual '+xx,abs(b1)<r*r)
    soft.append({'x':xx,'r':str(r),'max_scaled_error':mp.nstr(error,35)})

# mp.gauss_quadrature nodes and weights use current arbitrary precision.
def band(a,b,n):
    nodes,weights=mp.gauss_quadrature(n,'legendre')
    total=mp.mpf('0')
    for i in range(n):
        r=(b-a)*nodes[i]/2+(a+b)/2
        inner=mp.mpf('0')
        for j in range(n):
            theta=mp.pi*(nodes[j]+1)/4
            x=mp.sin(theta)
            h=mp.cos(theta)**2
            s1,s2=amplitudes(r,x)
            inner+=weights[j]*h*(-3*s1+h*s2)
        # 2 from angular evenness; theta Jacobian pi/4.
        total+=weights[i]*2*r*inner*mp.pi/2
    return total*(b-a)/2

rows=[]
for entry in cfg['bands']:
    a,b=map(mp.mpf,entry)
    vals=[]
    for n in cfg['quadrature_orders']:
        vals.append(band(a,b,n))
    error=abs(vals[-1]-vals[-2])/max(abs(vals[-1]),mp.mpf('1e-60'))
    check('nested quadrature '+','.join(entry),error<mp.mpf(cfg['relative_convergence_tolerance']))
    leading=9*mp.pi*(b**4-a**4)/64
    rows.append({'a':entry[0],'b':entry[1],'J_by_order':{str(n):mp.nstr(v,45) for n,v in zip(cfg['quadrature_orders'],vals)},'last_relative_change':mp.nstr(error,30),'J_leading_soft':mp.nstr(leading,45),'ratio_to_leading_soft':mp.nstr(vals[-1]/leading,45)})

p={k:mp.mpf(v) for k,v in cfg['source_parameter_decimals'].items()}
pref=p['gA']**2*p['mpi_GeV']**3/(128*mp.pi**4*p['M_GeV']*p['fpi_GeV']**2)
for row in rows:
    row['K_HBpiN']=mp.nstr(pref*mp.mpf(row['J_by_order'][str(cfg['quadrature_orders'][-1])]),45)

# Independent partition identity (shell is separately integrated).
lookup={(row['a'],row['b']):mp.mpf(row['J_by_order'][str(cfg['quadrature_orders'][-1])]) for row in rows}
check('ball equals smaller ball plus shell',abs(lookup[('0','0.5')]-lookup[('0','0.25')]-lookup[('0.25','0.5')])<mp.mpf('1e-35'))
result={'claim':'Complete strict leading HB piN non-Born finite bands, no full mass','checks':checks,'number_checks':len(checks),'soft_checks':soft,'bands':rows,'dimensionful_source_prefactor':mp.nstr(pref,45),'limitations':['Numerical convergence diagnostic, not rigorous quadrature bound','Chiral truncation uncertainty not numerically bounded','No microscopic sea decomposition','No local full-mass matching or UV tail','No alpha or R evaluation']}
out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks':len(checks),'bands':rows},indent=2))
