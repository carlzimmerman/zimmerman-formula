import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from record import record
import numpy as np
from scipy.special import erf
from scipy.integrate import quad

def enclosed(x):
    x=np.asarray(x,dtype=float);return np.where(x<1e-3,x*x*(.5-x/3+x*x/8-x**3/30+x**4/144),-np.expm1(-x)-x*np.exp(-x))
def qcas(a0,ge,nr,nm,gaussian=False,null=False):
    u=np.linspace(math.log(1e-7),math.log(1e5),nr);r=np.exp(u);x=r/.5
    if gaussian:
        g=np.empty_like(r);s=x<1e-3;g[s]=math.sqrt(2/math.pi)/3*r[s]/.5**3;g[~s]=(erf(x[~s]/math.sqrt(2))-math.sqrt(2/math.pi)*x[~s]*np.exp(-x[~s]**2/2))/r[~s]**2
    else:g=enclosed(x)/r**2
    mu,w=np.polynomial.legendre.leggauss(nm);m=mu[None,:];g=g[:,None];eta=ge/a0
    y=np.sqrt(eta*eta+g*g+2*eta*g*m);A=np.zeros_like(y) if null else np.sqrt(.25+1/y)-.5
    angular=(A*(eta*(3*m-5*m**3)+g*(1-3*m*m)))@w
    q=abs(1.5*float(np.trapz(angular/r,u)));rM=math.sqrt(6.6743e-11*1.98892e30/a0);Q=1.5*a0/rM*q
    return {'q':q,'Q2':Q,'ratio':Q/5.2e-27,'inner_angular':float(angular[0])}
def calculate():
    mass=quad(lambda x:x*math.exp(-x),0,np.inf,epsabs=1e-12)[0];der=[]
    for x in [.1,1,10]:
        h=1e-5*x;fd=float((enclosed(x+h)-enclosed(x-h))/(2*h));der.append(abs(fd/(x*math.exp(-x))-1))
    common={'mass_normalization':abs(mass-1)<=1e-10,'mass_derivative':max(der)<=1e-6,'mutate_bites':abs(mass*.5-1)>.1}
    feet={}
    for f,a0,ref in [('canonical',9.3603e-11,.480594078612),('alt',1.1312e-10,1.056745464443)]:
        rows={};checks=dict(common);base=qcas(a0,2.32e-10,8000,160,gaussian=True)
        checks['Gaussian_reproduction']=abs(base['ratio']-ref)<=.005
        for branch,ge in [('primary_conditional',2.32e-10**2/(2.32e-10+a0)),('inherited',2.32e-10)]:
            lo=qcas(a0,ge,4000,80);hi=qcas(a0,ge,8000,160);null=qcas(a0,ge,4000,80,null=True)
            delta=abs(hi['ratio']-lo['ratio']);checks[branch+'_convergence']=delta<=.002;checks[branch+'_null']=null['q']<=1e-14
            rows[branch]={'g_Ne':ge,'coarse':lo,'fine':hi,'convergence_difference':delta,'margin':1-hi['ratio'],'numeric_gate':'PASS' if hi['ratio']<=1 else 'FAIL'}
        label='NO VERDICT' if not all(checks.values()) else ('PASS' if rows['primary_conditional']['fine']['ratio']<=1 else 'FAIL')
        feet[f]={'label':label,'branches':rows,'checks':checks,'Gaussian_reference':base,'mass_derivative_max_error':max(der),'mass':mass,'mutate_mass':.5*mass}
    return {'assertion_tested':'point-source Helmholtz smoothing in reduced Cassini quadrature at fixed xi/rM=1/2','label':'NO VERDICT' if any(d['label']=='NO VERDICT' for d in feet.values()) else ('PASS' if all(d['label']=='PASS' for d in feet.values()) else 'FAIL'),'footings':feet,'bounds':{'nr':[4000,8000],'nmu':[80,160],'r_over_rM':[1e-7,1e5],'xi_over_rM':.5,'derivative_x':[.1,1,10]},'checks':[{'name':f+' '+k,'passed':bool(v)} for f,d in feet.items() for k,v in d['checks'].items()],'free_physical_numbers':['kappa=1/2 FITTED'],'residual_risks':['external-field inversion spherical, conditional','point source kernel has central cusp','not a full field equation solve']}
record(__file__,calculate)
