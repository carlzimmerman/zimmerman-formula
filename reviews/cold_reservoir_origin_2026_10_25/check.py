"""Conditional thermal estimates and controlled gravitational-production spectra."""
import argparse,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import quad,solve_ivp
from scipy.special import zeta

HBAR=1.054571817e-34; KB=1.380649e-23; C=299792458.; G=6.67430e-11
PC=3.085677581491367e16; ETA=1500*PC*1000; EV=1.602176634e-19

def log_sinh(x):
    return x-math.log(2)+math.log(-math.expm1(-2*x))

def occupation(k,tau):
    wi=math.sqrt(k*k+1); wo=math.sqrt(k*k+4)
    diff=3/(wi+wo)
    logn=2*log_sinh(math.pi*tau*diff/2)-log_sinh(math.pi*tau*wi)-log_sinh(math.pi*tau*wo)
    return math.exp(logn)

def ode_mode(k,tau):
    wi=math.sqrt(k*k+1); wo=math.sqrt(k*k+4)
    # An arbitrary common initial phase does not affect occupations.
    y0=np.array([1/math.sqrt(2*wi),-1j*math.sqrt(wi/2)],dtype=complex)
    def rhs(s,y): return [y[1],-(k*k+2.5+1.5*np.tanh(s/tau))*y[0]]
    sol=solve_ivp(rhs,[-16*tau,16*tau],y0,method='DOP853',rtol=2e-10,atol=2e-12)
    assert sol.success
    u,du=sol.y[:,-1]
    beta=math.sqrt(wo/2)*u-1j*du/math.sqrt(2*wo)
    alpha=math.sqrt(wo/2)*u+1j*du/math.sqrt(2*wo)
    W=float(abs(alpha)**2-abs(beta)**2)
    return float(abs(beta)**2),W

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True);ap.add_argument('--mutate',action='store_true')
    args=ap.parse_args(); out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    thermal=[]; m=HBAR/ETA
    for H in [1e-18,1.8e-18,3e-18]:
        T=HBAR*H/(KB*(1 if args.mutate else 2*math.pi))
        sigma=math.sqrt(KB*T/m); x=m*C*C/(KB*T)
        assert math.isclose(x,2*math.pi*C*C/(ETA*H),rel_tol=1e-12),'thermal 2pi mutation'
        assert math.isclose(sigma*sigma,ETA*H/(2*math.pi),rel_tol=1e-12)
        rhoV=3*H*H/(8*math.pi*G)
        pref=m*(m*KB*T/(2*math.pi*HBAR**2))**1.5
        # Independently eliminate m and T algebraically.
        pref2=HBAR*H**1.5/(8*math.pi**3*ETA**2.5)
        assert math.isclose(pref,pref2,rel_tol=1e-12)
        thermal.append(dict(H_s_inv=H,T_K=T,m_eV_c2=m*C*C/EV,sigma_1D_kms=sigma/1000,
            boltzmann_exponent=x,log10_rho_mu0_over_rhoV=math.log10(pref/rhoV)-x/math.log(10),
            log10_rho_excited_saturation_over_rhoV=math.log10(pref*zeta(1.5)/rhoV)))
    modes=[];spectra=[]
    for tau in [.1,.5,2.]:
        for k in [.1,1.,3.]:
            exact=occupation(k,tau); numerical,W=ode_mode(k,tau)
            assert abs(exact-numerical)<2e-10+1e-8*exact,'Bogoliubov spectrum discrepancy'
            assert abs(W-1)<2e-8,'Wronskian drift'
            modes.append(dict(tau=tau,k=k,exact=exact,ODE=numerical,Wronskian=W))
        # a_out=2; number a^3 n = (2pi²)^-1 int k² |beta|² dk, per degree.
        def moments(cut):
            n=quad(lambda k:k*k*occupation(k,tau),0,cut,epsabs=1e-15,epsrel=1e-10)[0]
            v=quad(lambda k:k*k*occupation(k,tau)*k*k/(k*k+4),0,cut,epsabs=1e-15,epsrel=1e-10)[0]
            return n/(2*math.pi**2),math.sqrt(v/n)
        n30,v30=moments(30);n60,v60=moments(60)
        assert abs(n30/n60-1)<1e-7 and abs(v30/v60-1)<1e-7
        spectra.append(dict(tau=tau,comoving_number_per_degree_m_units=n60,
                            final_vrms_over_c=v60,cutoff_relative_number_change=abs(n30/n60-1)))
    # Q/(H rhoV)=3r/(1+r) -> equal logarithmic dilution of both components.
    balances=[]
    for r in [.01,1.,10.]:
        q=3*r/(1+r); dv=-q; dc=-3*r+q
        assert abs(dc-r*dv)<1e-13
        balances.append(dict(r=r,Q_over_HrhoV=q,dlogrho_dloga=-q,w_eff=-1/(1+r)))
    result=dict(scope='conditional reservoir-origin tests, not a selected cosmology',thermal=thermal,
                production_modes=modes,production_spectra=spectra,fixed_ratio_balances=balances,
                checks=['thermal SI and eliminated-variable identities','ODE vs analytic spectrum',
                        'Wronskian','momentum integration cutoff','two-fluid energy balance'])
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
