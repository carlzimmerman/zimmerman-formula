"""CE-FM-009: thermal detailed-balance sign with Bose factors, not a rate calculation."""
import math,json,sys
from pathlib import Path

checks=[]
def check(name,cond,detail):
    checks.append(dict(name=name,passed=bool(cond),detail=detail))
    if not cond:raise AssertionError(name)
def occupation(E,T,mu=0.):return 1/math.expm1((E-mu)/T)
signs=[]
for Tc in (.5,1.,2.):
    for mu in (-1.,-.1,0.):
        for Omega in (.01,.1,1.):
            f1,f2,f3,f4=[occupation(E,Tc,mu) for E in (1.,2.,.9,2.1-Omega)]
            n1,n2=occupation(Omega/3,1.),occupation(2*Omega/3,1.)
            forward=f1*f2*(1+f3)*(1+f4)*(1+n1)*(1+n2)
            reverse=f3*f4*(1+f1)*(1+f2)*n1*n2
            lr=math.log(forward/reverse);expected=Omega*(1-1/Tc)
            check(f'Bose factor ratio Tc={Tc} mu={mu} Omega={Omega}',abs(lr-expected)<1e-12,lr-expected)
            sign=0 if abs(forward/reverse-1)<1e-12 else (1 if forward>reverse else -1)
            required=0 if Tc==1 else (1 if Tc>1 else -1)
            check(f'heat flow sign Tc={Tc} mu={mu} Omega={Omega}',sign==required,sign)
            signs.append(dict(Tc=Tc,mu=mu,Omega=Omega,log_emission_over_absorption=lr,net_sign=sign))

kb_eV=1.380649e-23/1.602176634e-19;c=299792458.;Tgamma=2.72548;Eg=kb_eV*Tgamma
crit=[dict(sigma_km_s=sv,critical_mass_eV=Eg/(1000*sv/c)**2) for sv in (10.,100.,200.,1000.)]
floors=[dict(mass_eV=m,classical_sigma_km_s=c*math.sqrt(Eg/m)/1000) for m in (.62,193.5,1000.,1e6)]
check('critical mass inversion',all(abs(c*math.sqrt(Eg/row['critical_mass_eV'])/1000/row['sigma_km_s']-1)<1e-13 for row in crit),crit)
result=dict(checks=checks,sign_table=signs,Tgamma_K=Tgamma,Tgamma_eV=Eg,critical_classical_mass=crit,
            classical_thermal_speeds=floors,
            scope='Thermal microreversibility sign and classical bath-temperature comparison only; no portal rate, condensate bound, density origin or empirically allowed model.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
