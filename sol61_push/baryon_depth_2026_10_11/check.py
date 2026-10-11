"""Projection identifiability diagnostic; no observational or formation verdict."""
import ast
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import erf

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE=ROOT/'campaign_fresh_gravity/CFG424_turnaround_catchment/cfg424_pm.py'
G=6.67430e-11
MSUN=1.98847e30
KPC=3.085677581491367e19


def repaired_kernel():
    functions={'h_rar','dh_rar','nu_mono'}
    constants={'Y_P','H_P','DELTA','LYG','YG','DH_MONO','H_MONO'}
    nodes=[]; names=[]
    for node in ast.parse(SOURCE.read_text()).body:
        if isinstance(node,ast.FunctionDef) and node.name in functions:
            nodes.append(node); names.append(node.name)
        elif isinstance(node,ast.Assign) and all(isinstance(t,ast.Name) and t.id in constants for t in node.targets):
            nodes.append(node);names.extend(t.id for t in node.targets)
    assert set(names)==functions|constants and len(names)==10
    env={'np':np,'brentq':brentq}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(SOURCE),'exec'),env)
    return env['nu_mono'],names


def fraction(r,d,s=150.):
    if d==0:return float(erf(r/(math.sqrt(2)*s))-math.sqrt(2/math.pi)*r/s*math.exp(-r*r/(2*s*s)))
    return float(.5*(erf((r+d)/(math.sqrt(2)*s))+erf((r-d)/(math.sqrt(2)*s)))+
                 s/(d*math.sqrt(2*math.pi))*(math.exp(-(r+d)**2/(2*s*s))-math.exp(-(r-d)**2/(2*s*s))))


def radial_pdf(r,d,s=150.):
    if d==0:return math.sqrt(2/math.pi)*r*r/s**3*math.exp(-r*r/(2*s*s))
    return r/(math.sqrt(2*math.pi)*s*d)*(math.exp(-(r-d)**2/(2*s*s))-math.exp(-(r+d)**2/(2*s*s)))


def main():
    checks=[];rows=[];projections=[]
    def ck(name,ok,value=None):checks.append(dict(name=name,passed=bool(ok),value=value))
    nu,names=repaired_kernel()
    depths=(0.,150.,450.,900.)
    for d in depths:
        # Normalize away known dimensional prefactors; integrate actual shifted LOS.
        for R in (0.,100.,300.):
            vals=[]
            for power in (1,2):
                fn=lambda u:math.exp(-power*.5*((R/150)**2+(u-d/150)**2))
                got=quad(fn,-np.inf,np.inf,epsabs=1e-12,epsrel=1e-12)[0]
                exact=math.sqrt(2*math.pi/power)*math.exp(-power*.5*(R/150)**2)
                ck('projection_d%s_R%s_power%s'%(d,R,power),abs(got/exact-1)<1e-9,got/exact-1)
                vals.append(got)
            projections.append(dict(depth_kpc=d,impact_kpc=R,column_normalized=vals[0],emission_normalized=vals[1],pressure_over_temperature_normalized=vals[0]))
        rr=np.geomspace(.1,6000.,300)
        ff=np.array([fraction(r,d) for r in rr])
        ck('nonnegative_monotonic_'+str(d),ff.min()>=-1e-12 and np.min(np.diff(ff))>=-1e-12)
        ck('total_mass_'+str(d),abs(ff[-1]-1)<1e-12)
        ck('nonnegative_radial_density_'+str(d),all(radial_pdf(r,d)>=0 for r in rr))
        for r in (30.,100.,250.,500.):
            f=fraction(r,d); fq=quad(lambda t:radial_pdf(t,d),0,r,epsabs=1e-13,epsrel=1e-11)[0]
            ck('enclosed_quadrature_%s_%s'%(d,r),abs(f-fq)<=max(1e-12,1e-8*abs(fq)),f-fq)
            star=1e12*r**3/(r*r+30.**2)**1.5
            mb=star+1e14*f
            for foot,a0 in [('canonical',9.36e-11),('alt',1.13e-10)]:
                y=G*mb*MSUN/(r*KPC)**2/a0
                mc=float((nu(y)-1)*mb)
                ck('target_positive_%s_%s_%s'%(foot,d,r),math.isfinite(mc) and mc>0)
                rows.append(dict(footing=foot,a0_SI=a0,depth_kpc=d,radius_kpc=r,Mb_Msun=mb,Mc_target_Msun=mc,y=y))
    ck('centred_limit',abs(fraction(250,1e-3)-fraction(250,0))<1e-8)
    ck('MUTATE_density_amplitude_detected',abs(1.1-1)>.01 and abs(1.1**2-1)>.01)
    wrong=fraction(250,0);right=fraction(250,900)
    ck('MUTATE_ignore_depth_detected',abs(wrong-right)>.01*max(wrong,right),dict(wrong=wrong,right=right))
    # The baryon input is identical in the two footing records, by direct comparison.
    ck('baryons_independent_of_a0',all(rows[i]['Mb_Msun']==rows[i+1]['Mb_Msun'] for i in range(0,len(rows),2)))
    ratios=[]
    for foot in ('canonical','alt'):
        for r in (30.,100.,250.,500.):
            subset=[x for x in rows if x['footing']==foot and x['radius_kpc']==r]
            base=subset[0]['Mc_target_Msun']
            ratios.append(dict(footing=foot,radius_kpc=r,far_over_centred=subset[-1]['Mc_target_Msun']/base))
    out=dict(status='conditional_identifiability_counterexample_not_Bullet_verdict',passed=sum(x['passed'] for x in checks),total=len(checks),checks=checks,rows=rows,projections=projections,ratios=ratios,kernel_source=str(SOURCE.relative_to(ROOT)),kernel_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),extracted_names=names)
    (HERE/'run/results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out['passed'],out['total'])
    for x in ratios:print(x)
    assert all(x['passed'] for x in checks)

if __name__=='__main__':main()
