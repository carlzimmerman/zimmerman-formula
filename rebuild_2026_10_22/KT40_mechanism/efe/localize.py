"""Locate the density-weighted physical virial and assess a controlled asymptotic."""
import argparse,json,math,time
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid,simpson,quad
from numpy.polynomial.legendre import leggauss
import calculate as C
I,L=C.I,C.L


def profile(d,foot,eta,upsilon=2.):
    a=d['a'];a0=I.A0[foot];e=eta*a0;p=C.POWER;ell=C.ELL;gm=I.G*(upsilon*d['L']+1.33*d['MHI'])
    r=np.geomspace(1e-6*a,2*(200*a+40*ell),4000);mu,w=leggauss(128)
    rr=r[:,None];mm=mu[None,:]
    g,gp,gpp=I.plummer_fields(rr,gm,a);gt=g/rr
    x=(g*g+e*e+2*g*e*mm)/a0**2;xp=2*(g+e*mm)*gp/a0**2
    s=ell**2*(gp*gp+2*gt*gt)/a0**2;sp=2*ell**2*(gp*gpp+2*gt*(gp/rr-g/rr**2))/a0**2
    z=x+s**p;zp=xp+p*s**(p-1)*sp
    rp=L.Rprime(z);rpp=L.Rsecond(z)
    ar=(L.Rminus1(z)+x*rp)*(g+e*mm)
    D=p*ell**2*s**(p-1)*x*rp
    Dp=p*ell**2*((p-1)*s**(p-2)*sp*x*rp+s**(p-1)*(xp*rp+x*rpp*zp))
    forceB=-Dp*gp-D*(gpp+2*(gp-gt)/rr)
    amean=(ar@w)/2;bmean=(forceB@w)/2;gn=g[:,0]
    weight=4*math.pi/3*I.rho_unit(r,a)*r**3
    terms={'Newton':weight*gn,'A':weight*amean,'B':weight*bmean,'total':weight*(gn+amean+bmean)}
    cumulative={k:cumulative_trapezoid(v,x=r,initial=0) for k,v in terms.items()}
    totals={k:float(simpson(v,x=r)) for k,v in terms.items()}
    radii=[]
    for q in [.5,1,2,3,5,10,20,50]:
        radii.append(dict(radius_over_a=q,radius_kpc=q*a,cumulative_variance={k:float(np.interp(q*a,r,v)) for k,v in cumulative.items()},enclosed_Plummer_mass_fraction=q**3/(1+q*q)**1.5))
    return dict(name=d['name'],footing=foot,eta=eta,upsilon=upsilon,a_kpc=a,total_variance_terms=totals,cumulative=radii,
                minimum_total_radial_monopole=float((gn+amean+bmean).min()))


def asymptotic(d,foot,eta,J):
    a=d['a'];a0=I.A0[foot];gm=I.G*(2*d['L']+1.33*d['MHI']);p=C.POWER;ell=C.ELL
    nu=.5+math.sqrt(.25+1/eta);nup=-1/(2*eta**2*math.sqrt(.25+1/eta))
    normal=(nu+eta*nup/3)*math.pi*gm/(32*a)
    curvature=(p-.5)*(eta*a0)**2*float(L.Rprime(eta*eta))*ell**(2*p)*gm**(2*p-1)*a**(3-6*p)/a0**(2*p)*J
    maxg=2*gm/(3*math.sqrt(3)*a*a)
    s0=3*ell*ell*(gm/a**3)**2/a0**2
    return dict(name=d['name'],footing=foot,eta=eta,upsilon=2,ordinary_linear_EFE_variance=normal,
                curvature_variance=curvature,total_asymptotic_variance=normal+curvature,
                expansion_small_parameters=dict(max_g_over_e=maxg/(eta*a0),max_s_power_over_eta_squared=s0**p/eta**2))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);args=ap.parse_args();start=time.monotonic()
    dwarfs={d['name']:d for d in I.sample()};main=json.loads((C.HERE/'run_001/results.json').read_text());low=json.loads((C.HERE/'low_001/results.json').read_text())
    profiles=[profile(dwarfs['Draco'],'canonical',.01),profile(dwarfs['Fornax'],'canonical',.1)]
    for row,source in zip(profiles,[low,main]):
        original=next(x for x in source['cases']['fine'] if x['name']==row['name'] and x['footing']==row['footing'] and x['eta']==row['eta'])
        error=abs(row['total_variance_terms']['total']-original['variance'][20])/max(abs(original['variance'][20]),1)
        row['relative_reproduction_error']=error;assert error<1e-4
    p=C.POWER
    fn=lambda u:u*u*(3*(1+2*u**4)/(1+u*u)**5)**p
    J,err=quad(fn,0,np.inf,epsabs=1e-11,epsrel=1e-11)
    asym=[]
    for foot in I.A0:
        for name in C.NAMES:
            row=asymptotic(dwarfs[name],foot,3.,J)
            prior=next(r for r in main['cases']['fine'] if r['name']==name and r['footing']==foot and r['eta']==3.)
            row['exact_variance_A_plus_Newton']=prior['variance_Newton'][20]+prior['variance_A'][20]
            row['exact_variance_B']=prior['variance_B'][20];row['exact_variance_total']=prior['variance'][20]
            asym.append(row)
    out=dict(profiles=profiles,asymptotic=dict(J_p=J,quad_absolute_error_estimate=err,rows=asym,
          qualification='Leading external-dominated and curvature-weak expansion; both displayed small parameters must be small. Not substituted for the exact finite-field results.'),
          all_checks_pass=True,runtime_seconds=time.monotonic()-start)
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')

if __name__=='__main__':main()
