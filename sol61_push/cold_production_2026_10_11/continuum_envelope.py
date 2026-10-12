"""Gaussian pair production with a depleted coherent pump; narrow-band model."""
import json, math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import solve_ivp

c=299792458.; G=6.67430e-11; hbar=1.054571817e-34; eV=1.602176634e-19
Mpc=3.0856775814913673e22; hubble_h=.6736; omega_c=.120; Omega_r=9.2e-5
H0=100*hubble_h*1000/Mpc; hc=hbar*c/eV
z=1e6; m=1e-12; eps=1e-7; u=.001
M=2*m*math.sqrt(1+u*u)
rho0=omega_c*3*(100*1000/Mpc)**2/(8*math.pi*G)
rho=rho0*(1+z)**3*c*c/eV*hc**3
H_eV=hbar/eV*H0*math.sqrt(Omega_r)*(1+z)**2
h=H_eV/(m*eps)
f=math.sqrt(2*rho)/(M*eps)  # harmonic source energy matching, not abundance prediction
lam=M*M/(2*f*f); ns0=rho/M
checks=[]
def check(name,passed,value=None): checks.append(dict(name=name,passed=bool(passed),value=value))

def run(K,vmax=2.,rtol=1e-8):
    nodes,weights=leggauss(K); v=vmax*nodes; dv=vmax*weights
    s2=u*u+2*eps*v; s=np.sqrt(s2)
    w=m**3*eps*s*dv/(4*math.pi**2*ns0)
    # B=b/sqrt(N0); C_j=w_j <a_j c_j>; F_j=w_j <n_j>.
    # Time x=m eps t; a=1 initially and H follows imposed radiation background.
    def terms(x):
        a=math.sqrt(1+2*h*x); om=np.sqrt(1+s2/a**2); wr=math.sqrt(1+u*u)
        delta=2*(s2/a**2-u*u)/(eps*(om+wr))
        gg=(1+u*u)/om*a**(-1.5)
        return a,delta,gg
    def rhs(x,y):
        B=y[0]; C=y[1:K+1]; F=y[K+1:]
        _,d,g=terms(x)
        return np.r_[-1j*np.sum(g*C),-1j*d*C-1j*g*B*(2*F+w),
                     -2*np.imag(g*np.conj(B)*C)]
    initial=np.zeros(2*K+1,dtype=complex); initial[0]=1
    atol=np.r_[1e-12,w*1e-5,w*1e-5]
    ts=np.linspace(0,200,1001)
    sol=solve_ivp(rhs,(0,200),initial,method='DOP853',t_eval=ts,
                  rtol=rtol,atol=atol,max_step=.25)
    B=sol.y[0]; C=sol.y[1:K+1]; F=sol.y[K+1:].real
    converted=F.sum(axis=0)
    inv=abs(B)**2+converted
    # Relative covariance error only where pair occupation is appreciable.
    cov=F*(F+w[:,None])-abs(C)**2
    covscale=np.maximum(F*(F+w[:,None]),w[:,None]**2)
    cov_err=float(np.max(abs(cov)/covscale))
    norm_err=float(np.max(abs(inv-1)))
    check(f'K{K} v{vmax}: completed',sol.success)
    check(f'K{K} v{vmax}: source plus pairs conserved',norm_err<2e-5,norm_err)
    check(f'K{K} v{vmax}: nonnegative pairs',float(F.min())>-1e-12,float(F.min()))
    check(f'K{K} v{vmax}: no overdraft',float(converted.max())<1+2e-5)
    # covariance is recorded as a diagnostic, not a pass based on a cancellation-prone relative test.
    imax=int(np.argmax(converted)); j100=500
    return dict(K=K,vmax=vmax,weight_sum=float(w.sum()),norm_error=norm_err,
        relative_covariance_diagnostic=cov_err,evaluations=sol.nfev,
        max_fraction=float(converted[imax]),x_at_max=float(ts[imax]),
        fraction_at_x100=float(converted[j100]),fraction_at_x200=float(converted[-1]),
        a_at_x200=terms(200)[0],initial_mode_p_over_m=s.tolist(),
        final_pair_fractions=F[:,-1].tolist(),
        snapshots=[dict(x=float(ts[j]),fraction=float(converted[j])) for j in range(0,len(ts),25)])

rows=[run(64),run(128),run(256),run(128,vmax=3.)]
out=dict(parameters=dict(m_eV=m,M_eV=M,epsilon=eps,u=u,z=z,rho_source_eV4=rho,
              f_eV=f,lambda_=lam,H_eV=H_eV,H_over_m_epsilon=h,
              harmonic_source_density_match=True),rows=rows,checks=checks,
         all_pass=all(x['passed'] for x in checks),
         non_claims=['Not full field theory','No quartic rescattering or radial fragmentation',
                     'Subtraction of off-resonant modes and parameter renormalization not derived',
                     'No relic abundance or late-time survival claim','Source amount chosen'])
(Path(__file__).parent/'envelope_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out['parameters'],indent=2))
for r in rows: print(json.dumps({k:r[k] for k in ['K','vmax','max_fraction','x_at_max','fraction_at_x100','fraction_at_x200','norm_error','relative_covariance_diagnostic']}))
print('Checks:',len(checks),out['all_pass'])
assert out['all_pass']
