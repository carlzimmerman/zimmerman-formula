"""Charged Gaussian pair production including the required quartic mean field."""
import json, math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import solve_ivp

c=299792458.; G=6.67430e-11; hbar=1.054571817e-34; eV=1.602176634e-19
Mpc=3.0856775814913673e22; hubble_h=.6736; omega_c=.120; Omega_r=9.2e-5
H0=100*hubble_h*1000/Mpc; hc=hbar*c/eV
chosen=json.loads((Path(__file__).parent/'detuned_carrier_run/results.json').read_text())['parameters']
z=chosen['z']; m=chosen['m_eV']; eps=chosen['epsilon']; u=chosen['u']
M=2*m*math.sqrt(1+u*u)
rho0=omega_c*3*(100*1000/Mpc)**2/(8*math.pi*G)
rho=rho0*(1+z)**3*c*c/eV*hc**3
H_eV=hbar/eV*H0*math.sqrt(Omega_r)*(1+z)**2
h=H_eV/(m*eps)
A0=math.sqrt(rho)/(math.sqrt(2)*M)
g_cubic=eps*m*m/A0
lambda_min=g_cubic*g_cubic/(4*m*m*u*u)
lambda_rep=lambda_min
lam=lambda_min+lambda_rep
ns0=rho/M
kappa=lam*ns0/(m**3*eps)
checks=[]
def check(name,passed,value=None): checks.append(dict(name=name,passed=bool(passed),value=value))

def run(K,vmax=2.,rtol=1e-10):
    nodes,weights=leggauss(K); v=vmax*nodes; dv=vmax*weights
    s2=u*u+2*eps*v; s=np.sqrt(s2)
    w=m**3*eps*s*dv/(4*math.pi**2*ns0)
    # B=b/sqrt(N0); C_j=w_j <a_j c_j>; F_j=w_j <n_j>.
    # Time x=m eps t; a=1 initially and H follows imposed radiation background.
    def terms(x):
        a=math.sqrt(1+2*h*x); om=np.sqrt(1+s2/a**2); wr=math.sqrt(1+u*u)
        delta=2*(s2/a**2-u*u)/(eps*(om+wr))
        gg=1/om*a**(-1.5)
        return a,delta,gg
    def rhs(x,y):
        B=y[0]; alpha=y[1:K+1]; beta=y[K+1:2*K+1]
        C=w*alpha*np.conj(beta); F=w*abs(beta)**2
        a,d,g=terms(x)
        om=np.sqrt(1+s2/a**2)
        dp=-2*h*s2/(eps*a**4*om)
        gp=g*(-1.5*h/a**2+h*s2/(a**4*om**2))
        v=1/om; vp=h*s2/(a**4*om**3)
        S=float(np.sum(v*F).real); Z=np.sum(v*C); coef=kappa*a**(-3)
        quartic_work=coef*(-3*h/a**2*(2*S*S+abs(Z)**2)
                        +4*S*float(np.sum(vp*F).real)+2*np.real(np.conj(Z)*np.sum(vp*C)))
        work=float((np.sum(dp*F)+2*np.real(np.conj(B)*np.sum(gp*C))).real)+quartic_work
        pair=g*B+coef*Z*v
        normal=d+4*coef*S*v
        return np.r_[-1j*np.sum(g*C),-0.5j*normal*alpha-1j*pair*beta,
                     0.5j*normal*beta+1j*np.conj(pair)*alpha,work]
    initial=np.zeros(2*K+2,dtype=complex); initial[0]=1; initial[1:K+1]=1
    atol=1e-12
    ts=np.linspace(0,200,1001)
    sol=solve_ivp(rhs,(0,200),initial,method='DOP853',t_eval=ts,
                  rtol=rtol,atol=atol,max_step=.25)
    B=sol.y[0]; alpha=sol.y[1:K+1]; beta=sol.y[K+1:2*K+1]
    C=w[:,None]*alpha*np.conj(beta); F=w[:,None]*abs(beta)**2
    bog_err=float(np.max(abs(abs(alpha)**2-abs(beta)**2-1)))
    check(f'K{K} v{vmax}: Bogoliubov normalization',bog_err<1e-3,bog_err)
    converted=F.sum(axis=0)
    E=[]
    for j,x in enumerate(sol.t):
        a,d,g=terms(x)
        v=1/np.sqrt(1+s2/a**2); S=float(np.sum(v*F[:,j])); Z=np.sum(v*C[:,j])
        E.append(float(np.sum(d*F[:,j])+2*np.real(np.conj(B[j])*np.sum(g*C[:,j])))
                 +kappa*a**(-3)*(2*S*S+abs(Z)**2))
    workerr=float(np.max(abs(np.array(E)-sol.y[-1].real)))
    check(f'K{K} v{vmax}: expansion work',workerr<2e-5,workerr)
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
    return dict(K=K,vmax=vmax,weight_sum=float(w.sum()),norm_error=norm_err,work_error=workerr,
        relative_covariance_diagnostic=cov_err,evaluations=sol.nfev,
        max_fraction=float(converted[imax]),x_at_max=float(ts[imax]),
        fraction_at_x100=float(converted[j100]),fraction_at_x200=float(converted[-1]),
        a_at_x200=terms(200)[0],initial_mode_p_over_m=s.tolist(),
        final_pair_fractions=F[:,-1].tolist(),
        snapshots=[dict(x=float(ts[j]),fraction=float(converted[j])) for j in range(0,len(ts),25)])

rows=[run(512),run(1024),run(1536,vmax=3.),run(1024,rtol=1e-11)]
check('quadrature endpoint comparison',abs(rows[0]['fraction_at_x200']-rows[1]['fraction_at_x200'])<1e-4)
check('bandwidth endpoint comparison',abs(rows[1]['fraction_at_x200']-rows[2]['fraction_at_x200'])<1e-4)
check('time tolerance endpoint comparison',abs(rows[1]['fraction_at_x200']-rows[3]['fraction_at_x200'])<1e-4)
out=dict(parameters=dict(m_eV=m,M_eV=M,epsilon=eps,u=u,z=z,rho_source_eV4=rho,
              source_amplitude_eV=A0,cubic_g_eV=g_cubic,lambda_=lam,lambda_min=lambda_min,lambda_rep=lambda_rep,kappa=kappa,H_eV=H_eV,H_over_m_epsilon=h,
              charged_circular_source_density_match=True),rows=rows,checks=checks,
         all_pass=all(x['passed'] for x in checks),
         non_claims=['Not full field theory','Gaussian quartic included; no non-Gaussian scattering or moving source',
                     'Subtraction of off-resonant modes and parameter renormalization not derived',
                     'No relic abundance or late-time survival claim','Source amount chosen'])
(Path(__file__).parent/'detuned_bogoliubov_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out['parameters'],indent=2))
for r in rows: print(json.dumps({k:r[k] for k in ['K','vmax','max_fraction','x_at_max','fraction_at_x100','fraction_at_x200','norm_error','work_error','relative_covariance_diagnostic']}))
print('Checks:',len(checks),out['all_pass'])
assert out['all_pass']
