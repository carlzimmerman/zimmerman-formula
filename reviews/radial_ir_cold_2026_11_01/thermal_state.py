"""Conditional free FD relic: density, velocities and comoving travel distance.

The initial relic distribution is stipulated, not produced by this script.
The Goldstino width is partial; all candidate channels remain in cold_states/.
"""
import sys
sys.dont_write_bytecode=True
import json,math,argparse,time,resource
from pathlib import Path
import numpy as np
from scipy.special import roots_laguerre,zeta
from scipy.integrate import quad
BASE=Path(__file__).resolve().parent


def main(out):
    start=time.monotonic();u=json.loads((BASE/'run_units/result.json').read_text());assert u['all_checks_pass']
    c=u['constants'];hbar=c['hbar_GeV_s'];H0=c['H0_s'];rhoC=c['rho_DE_GeV4']/.685;rhocold=.265*rhoC
    GeV_J=1.602176634e-10;kB=1.380649e-23/GeV_J;Tgamma=2.7255*kB;Tnu=(4/11)**(1/3)*Tgamma
    Om=.315;Or=Om/3401.;OL=1-Om-Or;aeq=Or/Om;I2=1.5*float(zeta(3));cm=u['mass_controls'][0]['mass_coefficient'];cl=u['photino_mass_coefficient']
    cases=[];controls=[]
    for m in [1e-6,1e-5,1e-4,1e-3]:
        T=(4*math.pi**2*rhocold/(3*2*float(zeta(3))*m))**(1/3)
        values=[]
        for order in [64,128]:
            x,w=roots_laguerre(order);f=w/(1+np.exp(-x));norm=float(np.dot(f,x*x))
            def mean_v(a):
                r=m*a/T
                return float(np.dot(f,x**3/np.sqrt(x*x+r*r)))/norm
            def mean_v2(a):
                r=m*a/T
                return float(np.dot(f,x**4/(x*x+r*r)))/norm
            def E(a):return math.sqrt(Or/a**4+Om/a**3+OL)
            # Relativistic contribution before a_min is bounded analytically.
            amin=1e-15
            integral,error=quad(lambda t:mean_v(math.exp(t))/(math.exp(t)*E(math.exp(t))),math.log(amin),0,epsabs=1e-13,epsrel=2e-9,limit=180)
            early=amin/math.sqrt(Or)
            Mpc=3.0856775814913673e22
            length=(integral+early)*299792458/(H0*Mpc)
            vals=dict(order=order,normalization_error=abs(norm/I2-1),vmean_today=mean_v(1),vrms_today=math.sqrt(mean_v2(1)),vmean_equality=mean_v(aeq),vrms_equality=math.sqrt(mean_v2(aeq)),free_streaming_Mpc=length,quad_estimate_Mpc=error*299792458/(H0*Mpc),early_distance_bound_Mpc=early*299792458/(H0*Mpc))
            values.append(vals)
        diff=abs(values[0]['free_streaming_Mpc']/values[1]['free_streaming_Mpc']-1)
        controls.append(dict(m_GeV=m,quadrature_order_relative_FS_difference=diff,normalization_error=max(q['normalization_error'] for q in values)))
        bath=[]
        for heating in [1.,2.,3.]:
            # 12 massless gauge bosons (24 polarizations), phase1, Goldstino2.
            geff=25+7/8*2
            dn=4/7*geff*(heating*T/Tnu)**4
            bath.append(dict(temperature_ratio_to_relic=heating,assumed_massless_geff=geff,Delta_Neff=dn))
        for e in [.003,.001]:
            mh=cl*e**2.5;mu=m/mh;v=mu*7.367143721278508/math.sqrt(e);F2=mu**4/31
            gamma=m**5/(16*math.pi*F2)
            row=dict(m_GeV=m,e=e,mu_GeV=mu,v_GeV=v,T_relic_today_GeV=T,T_relic_over_Tnu=T/Tnu,number_density_GeV3=rhocold/m,
                     Goldstino_partial_lifetime_s=hbar/gamma,partial_survival_age_fraction=math.exp(-c['required_lifetime_s']*gamma/hbar),
                     relic_dynamics=values[-1],bath_assumptions=bath,
                     cold_velocity_benchmark=values[-1]['vrms_equality']<1e-4,
                     free_streaming_below_1kpc_benchmark=values[-1]['free_streaming_Mpc']<.001)
            cases.append(row)
    checks={'eight_conditional_states':len(cases)==8,'FD_normalization_below_1e-12':max(x['normalization_error'] for x in controls)<1e-12,
            '64_128_free_streaming_difference_below_2e-5':max(x['quadrature_order_relative_FS_difference'] for x in controls)<2e-5,
            'all_partial_lifetimes_exceed_age':all(x['Goldstino_partial_lifetime_s']>c['required_lifetime_s'] for x in cases),
            '100keV_and_1MeV_cold_by_velocity':all(x['cold_velocity_benchmark'] for x in cases if x['m_GeV']>=1e-4),
            'some_sub_kpc_free_streaming_states':any(x['free_streaming_below_1kpc_benchmark'] for x in cases),
            'unheated_bath_below_01_DeltaNeff':all(x['bath_assumptions'][0]['Delta_Neff']<.1 for x in cases if x['m_GeV']>=1e-5)}
    result=dict(claim_id='TP04_CONDITIONAL_FD_RELIC',checks=checks,all_checks_pass=all(checks.values()),cases=cases,controls=controls,
                cosmology=dict(H0_s=H0,Omega_m=Om,Omega_c=.265,Omega_r=Or,Omega_Lambda=OL,z_equality=3400,T_CMB_K=2.7255),
                runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                non_claims=['FD relic is an initial distribution, not derived freezeout/reheating/production','Partial Goldstino lifetime does not bound other decay channels','Free-streaming travel distance is not a Boltzmann transfer-function or observational exclusion','Hidden bath temperature/entropy heating assumed; no derived thermal history','Standard Einstein-background cosmology and independent vacuum normalization are conditional'])
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=checks,controls=controls,selected=[dict(m_GeV=q['m_GeV'],e=q['e'],tau=q['Goldstino_partial_lifetime_s'],v_eq=q['relic_dynamics']['vrms_equality'],FS_Mpc=q['relic_dynamics']['free_streaming_Mpc'],DeltaNeff=q['bath_assumptions'][0]['Delta_Neff']) for q in cases]),indent=2));assert result['all_checks_pass'],checks

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);main(p.parse_args().out)
