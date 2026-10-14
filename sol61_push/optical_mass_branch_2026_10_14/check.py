"""Conditional eV-scale Gaussian coherent source, natural units internally."""
import json,sys,math
from pathlib import Path
from scipy.integrate import quad
from scipy.special import erf
hc=1.973269804e-7; hb=6.582119569e-16; c=299792458.; ej=1.602176634e-19
m=1.; MR=2.; delta=2e-9; g=1e-20; intensity=1e12
Lt=.001/hc; Lz=1./hc
u=intensity/c/(ej/hc**3); F=g*u/math.sqrt(2*MR)
k0=1/(math.sqrt(2)*Lt); eps=k0*k0/(2*MR); beta=math.sqrt(delta/m)
checks=[]
def ck(name,err,tol):
    assert err<=tol,(name,err,tol)
    checks.append(dict(name=name,error=float(err),tolerance=tol))
def angular(k,lt,lz):
    b=k*k*(lz*lz-lt*lt)
    ratio=2. if b<1e-15 else math.sqrt(math.pi)*erf(math.sqrt(b))/math.sqrt(b)
    return 2*math.pi*math.exp(-lt*lt*k*k)*ratio
def radial_density(k,lt,lz):
    return F*F*lt**4*lz**2*k*k*angular(k,lt,lz)
def shell_rate(k,lt,lz):
    return 2*math.pi*MR/k*radial_density(k,lt,lz)/hb
iso=shell_rate(k0,Lt,Lt)
iso_direct=8*math.pi**2*MR*k0*F**2*Lt**6*math.exp(-Lt*Lt*k0*k0)/hb
ck('isotropic_shell_formula',abs(iso/iso_direct-1),1e-14)
# Resolve the narrow angular peak independently with a scaled coordinate.
for k in [k0/1000,k0,k0*2]:
    b=k*k*(Lz*Lz-Lt*Lt); scale=max(1.,math.sqrt(b))
    num=4*math.pi*math.exp(-Lt*Lt*k*k)/scale*quad(lambda z:math.exp(-b*z*z/scale**2),0,min(scale,12),epsabs=1e-13)[0]
    ck('angular_integral',abs(num/angular(k,Lt,Lz)-1),2e-12)
# Parseval normalization: integral d^3k |Ftilde|^2 = integral d^3x |F|^2.
# Factorized 1D Gaussian integrals avoid a badly conditioned elongated mesh.
left=F*F*Lt**4*Lz**2
for ell in [Lt,Lt,Lz]:
    left*=quad(lambda x:math.exp(-x*x),-10,10,epsabs=1e-13)[0]/ell
right=F*F*math.pi**1.5*Lt*Lt*Lz
ck('Parseval',abs(left/right-1),2e-13)
# Gaussian time pulse, duration tau. Change energy to y=tau*(E-eps).
# N/(sqrt(pi)*tau) tends the stationary shell rate; no decay during pulse.
rate=shell_rate(k0,Lt,Lz)
pulses=[]
for factor in [10,30,100]:
    tau=factor/eps
    def integrand(y):
        energy=eps+y/tau
        if energy<=0:return 0.
        k=math.sqrt(2*MR*energy)
        return radial_density(k,Lt,Lz)*MR/k*math.exp(-y*y)
    avg=2*math.sqrt(math.pi)*quad(integrand,max(-factor,-10),10,epsabs=1e-50,epsrel=1e-10)[0]/hb
    pulses.append(dict(duration_s=tau*hb,rate_per_s=avg,ratio_to_shell=avg/rate))
ck('long_pulse_limit',abs(pulses[-1]['ratio_to_shell']-1),1e-4)
# Exact two-body daughter energy, high precision to resolve neV kinetic energies.
import mpmath as mp
mp.mp.dps=70
mm=mp.mpf(1); mr=2*mm+mp.mpf('2e-9'); pp=mp.mpf(str(k0))
er=mp.sqrt(mr*mr+pp*pp); prest=mp.sqrt(mr*mr/4-mm*mm)
kmin=er/2-pp*prest/mr-mm; kmax=er/2+pp*prest/mr-mm
assert kmin>=0 and kmax<mp.mpf('1e-8')
ck('daughter_energy_sum',float(abs(kmin+kmax-(er-2*mm))),1e-60)
width_gamma=g*g*MR**3/(64*math.pi)
rows=[]
for lam in [1e-6,1e-15]:
    mu=math.sqrt(lam)*MR
    width=mu*mu*beta/(16*math.pi*MR)
    tau=hb/(width+width_gamma); vel=k0/MR*c; length=vel*tau
    fraction=-math.expm1(-.001/length)
    ck('positive_residual_quartic',max(0.,-(lam-mu*mu/(2*MR*MR))),0.)
    rows.append(dict(lambda_rep=lam,mu_eV=mu,Gamma_phi_eV=width,lifetime_s=tau,
                     mean_flight_m=length,fraction_decay_first_mm=fraction,
                     stationary_pairs_first_mm_per_s=rate*fraction*width/(width+width_gamma)))
result=dict(assumptions=dict(m_eV=m,MR_smooth_eV=MR,pair_excess_eV=delta,g_per_eV=g,
    intensity_each_beam_W_per_m2=intensity,source_transverse_sigma_m=.001,source_axial_sigma_m=1.,
    warning='Assigned scalar and effective Gaussian drive; not a solved Maxwell beam geometry or allowed-region certificate'),
    scalar_momentum_eV=k0,drive_excess_eV=eps,scalar_speed_m_per_s=k0/MR*c,
    isotropic_source_rate_per_s=iso,elongated_source_rate_per_s=rate,
    daughter_K_range_eV=[float(kmin),float(kmax)],pulse_checks=pulses,
    decay_cases=rows,checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
