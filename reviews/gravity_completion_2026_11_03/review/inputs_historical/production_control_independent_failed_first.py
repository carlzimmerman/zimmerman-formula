"""Independent finite audit of one production boundary; no producer imports."""
import sys, json, math, time, resource
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
sys.dont_write_bytecode = True
ROOT=Path(__file__).resolve().parents[3]
P=ROOT/'reviews/gravity_completion_2026_11_03/production'
MP=2.435e18; HB=6.582119569509066e-25
TG=2.7255*8.617333262145e-14; TN=TG*(4/11)**(1/3)
H0=2.1842852410855023e-18*HB; RC=3*MP**2*H0**2; RX=.265*RC
MPC=3.0856775814913673e22/(299792458*HB); AR=1/1101
KSM=math.pi**2/30*(2+5.25*(4/11)**(4/3))*TG**4
KSM_MIN=math.pi**2/30*10.75*(4/11)**(4/3)*TG**4
C0=math.sqrt(KSM/(3*MP**2)); CMIN=math.sqrt(KSM_MIN/(3*MP**2))
KMAX=1.1*RX*AR+.3*7*math.pi**2/120*TN**4
CPRE=math.sqrt((KSM+KMAX+.05*RC*AR+.685*RC*AR**4)/(3*MP**2))
AI=TG/.02*(4/11)**(1/3)
BASE=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/canonical/run_nearfold/result.json').read_text())['threshold_points'][-1]
SLOPES=BASE['gaugino_log_slopes']['.0025']
def quantities(e,r):
    z=e/.003; mc=BASE['gauginos_GeV']['U1']*z**5
    R=BASE['R_GeV']*z**2; F=BASE['mu_GeV']**2/math.sqrt(31)*z**5
    m=2*mc*r; mi={k:v*z**5 for k,v in BASE['gauginos_GeV'].items()}
    widths={k:d*(SLOPES[k]*mi[k]/(math.sqrt(2)*R))**2*m/(16*math.pi)*max(0,1-4*(mi[k]/m)**2)**1.5 for k,d in [('SU3',8),('SU2',3),('U1',1)]}
    widths['GG']=m**5/(32*math.pi*F**2)
    G=sum(widths.values()); B=widths['U1']/G; tau=HB*16*math.pi*F**2/mc**5
    return mc,m,G,B,mi,widths,tau
def assess(e,r,C):
    mc,m,G,B,mi,widths,tau=quantities(e,r)
    amean=math.sqrt(math.pi*C/(2*G)); n=RX/(2*B*mc)
    # Constant CPRE is an analytic H upper bound, including baryons and Lambda.
    urec=G*(AR**2-AI**2)/(2*CPRE)
    # Exact expectation of min(sqrt(2 C u/G), AR) for Exp(1) u.
    Kfloor=n*m*amean*math.erf(math.sqrt(G*AR**2/(2*C)))
    A=math.sqrt(r*r-1)*math.sqrt(2*C/G)
    def hmax(a):return math.sqrt((KSM/a**4+.05*RC/a**3+.685*RC+KMAX/AR/a**3)/(3*MP**2))
    I=quad(lambda x:math.exp(-2*x)/hmax(math.exp(x)),math.log(AR),0,epsabs=0,epsrel=2e-11)[0]/MPC
    # Integrating only sqrt(u)<=10 avoids a tail approximation; upper p in the
    # velocity denominator yields a lower bound throughout a>=AR.
    L=10.; firstmoment=math.sqrt(math.pi)/2*math.erf(L)-L*math.exp(-L*L)
    fs=A*firstmoment/math.sqrt(1+(A*L/AR)**2)*I
    # Max post-rec path from baryon H floor: below 1e5 Mpc, independent of hidden.
    Dmax=2*(1-math.sqrt(AR))/(H0*math.sqrt(.05)*MPC)
    occupation={}
    for k,g in [('U1',2),('SU3',16),('SU2',6)]:
        pk=math.sqrt(m*m/4-mi[k]**2)
        # f(u) in low-T SM RD, before any blocking or hidden backreaction.
        coef=8*math.pi**2*(widths[k]/G)*n/(g*pk**3)*(G/(2*C0))**1.5
        ublock=brentq(lambda u:coef*math.exp(-u)/math.sqrt(u)-1,1e-16,100)
        occupation[k]={'f_at_u_1':coef/math.e,'early_u_f_equals_1':ublock,'fraction_born_before_f_falls_below_1_RD':-math.expm1(-ublock)}
    return {'e':e,'r':r,'mchi_GeV':mc,'Gamma_GeV':G,'Bchi':B,'Klower_over_Kmax':Kfloor/KMAX,'late_fraction_log_upper':-urec,'FS_positive_integral_lower_Mpc':fs,'residual_path_upper_Mpc':Dmax,'Ward_survival':math.exp(-4.3549488e17/tau),'vacuum_RD_occupation_diagnostic':occupation}
start=time.monotonic()
old=json.loads((P/'run_controls_v2/result.json').read_text())['continuous_energy_lifetime_boundary_control']
original=assess(old['e'],old['sigma_over_2mchi'],C0)
corrected_r=brentq(lambda r:assess(old['e'],r,CMIN)['Klower_over_Kmax']-1,1+1e-8,1.1,xtol=2e-14)
corrected=assess(old['e'],corrected_r,CMIN)
# Direct photon number source: each polarization density enters n1*n2, the
# identical event factor 1/2 cancels the produced number 2, and <s v>=8 E1 E2/3.
photon_C=(2/(2*math.pi**2)*6)**2*(8/3)/(640*math.pi)
data={'claim_id':'GC03_INDEPENDENT_PRODUCTION_CONTROL_AUDIT','Cmin_over_ClowT':CMIN/C0,'Ksm_early_over_Ksm_lowT':KSM_MIN/KSM,'original_boundary_independent':original,'conservative_corrected_boundary_control':corrected,'photon_source_C_independent':photon_C,'photon_source_C_expected':3/(20*math.pi**5),'runtime_seconds':time.monotonic()-start,'peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'One finite boundary control, vacuum-width dilute mother law. Does not establish parameter-space optimum or validity under Pauli blocking/nonabelian medium feedback.'}
Path(sys.argv[1]).write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2))
