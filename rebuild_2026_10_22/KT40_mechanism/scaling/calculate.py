"""Explanatory fixed-law scales and independent leading Solar asymptotics."""
import argparse
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad, simpson

HERE=Path(__file__).resolve().parent
RB=HERE.parents[1]
sys.dont_write_bytecode=True
sys.path.insert(0,str(RB/'KT39_power_curvature/analytic'))
import law
from radial_reference import plummer_fields,radial_force

P=9/8
ELL=3.


def q_closed(z):
    y=np.sqrt(z)
    root=np.sqrt(y*(y+4))
    return z/2+(y+2)*root/2-2*np.log((y+2+root)/2)


def rthird(z):
    qp2=law.Qsecond(z)
    qp3=qp2*(-5/(4*z)-1/(4*np.sqrt(z)*(np.sqrt(z)+4)))
    return (qp3-3*law.Rsecond(z))/z


def solar_integral(eta):
    x=eta*eta
    alpha=1/(2*P)
    def fn(t):
        z=x+t
        return t**alpha*(2*law.Rsecond(z)+x*rthird(z))
    val,err=quad(fn,0,np.inf,epsabs=2e-13,epsrel=2e-11,limit=300)
    # q_B ~ c(eta,p)/lambda, Q2 ~ c(eta,p)*a0/ell.
    factor=-96/5*6**(-2.5)*eta**2
    return factor*val,abs(factor)*err


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    previous=json.loads((RB/'KT39_power_curvature/dwarfs/continuation_001/results.json').read_text())
    solardata=json.loads((RB/'KT39_power_curvature/cassini/adaptive_001/results.json').read_text())
    constants=previous['constants'];G=constants['G'];A0=constants['A0'];KPC=constants['KPC']
    out=dict(power=P,ell_kpc=ELL,constants=constants,checks={},solar={},dwarfs=[],all_checks_pass=False)
    z=np.geomspace(.01,1e10,200)
    out['checks']['closed_Q_relative']=float(np.max(abs(q_closed(z)/law.Q(z)-1)))
    assert out['checks']['closed_Q_relative']<1e-11
    h=1e-4
    fd=(q_closed(z*np.exp(h))-q_closed(z*np.exp(-h)))/(2*h*z)
    out['checks']['Q_derivative_relative']=float(np.max(abs(fd/law.Qprime(z)-1)))
    assert out['checks']['Q_derivative_relative']<2e-8
    maxima=dict(chi_identity=0.,plummer_H_identity=0.,stored_sigma_error=0.,virial_split_error=0.)
    for foot,a0 in A0.items():
        # The Solar lane retains its original Solar mass, not the dwarf unit mass.
        a0si=a0*1e6/KPC;gm_sun=6.6743e-11*1.98892e30
        rm=math.sqrt(gm_sun/a0si)/KPC;eta=2.32e-10/a0si
        lam=ELL/rm
        isolated_cross=6**(P/(6*P-4))*ELL**(2*P/(6*P-4))*rm**((4*P-4)/(6*P-4))
        external_cross=6**(1/6)*ELL**(1/3)*rm**(2/3)*eta**(-1/(3*P))
        coeff,error=solar_integral(eta)
        stored=solardata['footings'][foot]['p1.125|ell3.0']['fine']
        q_asym=coeff/lam
        row=dict(rM_kpc=rm,eta=eta,lambda_=lam,
                 solar_only_chi1_radius_kpc=isolated_cross,
                 external_field_chi1_radius_kpc=external_cross,
                 g_solar_equals_external_radius_kpc=rm/math.sqrt(eta),
                 Q2_over_a0_div_ell_coefficient=coeff,coefficient_quad_error=error,
                 Q2_asymptotic_si=coeff*a0si/(ELL*KPC),q_asymptotic=q_asym,
                 q_stored=stored['q_signed'],qA_stored=stored['q_A_flux'],qB_stored=stored['q_B_flux'],
                 asymptotic_relative_error=abs(q_asym/stored['q_signed']-1),
                 stored_A_to_B=abs(stored['q_A_flux']/stored['q_B_flux']))
        assert row['asymptotic_relative_error']<1e-5
        out['solar'][foot]=row
        stored_rows={r['name']:r for r in previous['cases']['fine']['1.125|3'][foot]}
        for d in previous['sample']:
            a=d['a'];r=np.geomspace(1e-6*a,200*a+40*ELL,2000)
            rho=3/(4*np.pi*a**3)*(1+(r/a)**2)**-2.5
            W=4*np.pi/3*rho*r**3
            for up,index in [(1.,0),(2.,20),(3.,40)]:
                mass=up*d['L']+1.33*d['MHI'];gm=G*mass
                fields=plummer_fields(r,gm,a)
                response=radial_force(r,*fields,ELL,a0,p=P)
                vN=np.pi*gm/(32*a)
                vA=simpson(W*response['A'],x=r)
                vB=simpson(W*(response['phantom']-response['A']),x=r)
                vph=simpson(W*response['phantom'],x=r)
                sig=math.sqrt(vN+vph)
                maxima['stored_sigma_error']=max(maxima['stored_sigma_error'],abs(sig-stored_rows[d['name']]['sigma'][index]))
                maxima['virial_split_error']=max(maxima['virial_split_error'],abs(vA+vB-vph)/max(abs(vph),1e-12))
                alpha=gm/(a*a*a0)
                locals_=[]
                for u in [.5,1.,2.,4.]:
                    rr=a*u;g,gp,gpp=plummer_fields(np.array([rr]),gm,a)
                    rrsp=radial_force(np.array([rr]),g,gp,gpp,ELL,a0,p=P)
                    hh=math.sqrt(float(gp[0]**2+2*(g[0]/rr)**2));L=float(g[0])/hh;y=float(g[0])/a0
                    chi=float(rrsp['s'][0]**P/rrsp['x'][0])
                    expected=(ELL/L)**(2*P)*y**(2*P-2)
                    hsq=(gm/a**3)**2*3*(1+2*u**4)/(1+u*u)**5
                    maxima['chi_identity']=max(maxima['chi_identity'],abs(chi/expected-1))
                    maxima['plummer_H_identity']=max(maxima['plummer_H_identity'],abs(hh*hh/hsq-1))
                    locals_.append(dict(r_over_a=u,g_over_a0=y,L_kpc=L,Lcritical_kpc=ELL*y**((P-1)/P),
                                        chi=chi,s=float(rrsp['s'][0]),z=float(rrsp['z'][0]),
                                        newton=float(g[0]),A=float(rrsp['A'][0]),B_force=float(rrsp['phantom'][0]-rrsp['A'][0]),
                                        total=float(rrsp['total'][0]),plain_total=float(g[0]*law.Qprime(rrsp['x'][0]))))
                out['dwarfs'].append(dict(name=d['name'],footing=foot,upsilon=up,mass_Msun=mass,a_kpc=a,
                    compactness_GM_over_a2a0=alpha,variance_newton=vN,variance_A=vA,variance_B=vB,
                    variance_phantom=vph,sigma=sig,plain_sigma=stored_rows[d['name']]['plain_sigma'][index],
                    observed_sigma=d['obs'],observed_error=d['err'],local=locals_))
    out['checks'].update(maxima)
    assert maxima['chi_identity']<1e-12 and maxima['plummer_H_identity']<1e-12
    assert maxima['stored_sigma_error']<1e-10 and maxima['virial_split_error']<1e-12
    assert len(out['dwarfs'])==144
    out['all_checks_pass']=True
    args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(checks=out['checks'],solar=out['solar'],all_checks_pass=True),indent=2))


if __name__=='__main__':main()
