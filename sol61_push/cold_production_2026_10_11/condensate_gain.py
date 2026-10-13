"""Initial Bose condensate gain for a stipulated dephased produced shell."""
import json,math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
p=Path(__file__).parent;hb=6.582119569e-16
checks=[];rows=[]
def ck(n,b):checks.append(dict(name=n,passed=bool(b)))
for alpha,file in [(1.,'detuned_bogoliubov_run/results.json'),(2.,'alpha2_bogoliubov_run/results.json')]:
    data=json.loads((p/file).read_text());a=data['parameters'];m=a['m_eV'];M=a['M_eV'];eps=a['epsilon'];u=a['u'];ns=a['rho_source_eV4']/M
    D=M*M-4*m*m;kmin=a['lambda_min']/(4*m*m)
    local=[]
    for row in data['rows']:
        K=row['K'];vmax=row['vmax'];nodes,weights=leggauss(K);dv=vmax*weights
        q=np.asarray(row['initial_mode_p_over_m']);F=np.asarray(row['final_pair_fractions'])
        mode_weight=m**3*eps*q*dv/(4*math.pi**2*ns)
        f=F/mode_weight
        # Exact one-particle kinetic energy and Jacobian, leading NR phase-space coefficient.
        E=m*(np.sqrt(1+q*q)-1);dE=m*eps*dv/np.sqrt(1+q*q)
        esum=E[:,None]+E[None,:]
        x=2*m*esum/D
        keff=kmin*(alpha-x/(1-x))
        ck('escort outside populated band '+str((alpha,K,vmax,row['norm_error'])),float(esum.min())>float(E.max()))
        W=(f*dE)[:,None]*(f*dE)[None,:]
        natural_rate=2*m**3/math.pi**3*float(np.sum(keff*keff*W))
        # Constant matrix-element control reduces double integral to square.
        direct=float(np.sum(kmin*kmin*W));factored=kmin*kmin*float(np.sum(f*dE))**2
        ck('constant kernel factorization '+str((alpha,K,vmax,row['norm_error'])),abs(direct/factored-1)<1e-12)
        reconstructed=m**3*eps/(2*math.pi**2)*np.sum(q*dv*f)
        ck('occupation density reconstruction '+str((alpha,K,vmax,row['norm_error'])),abs(reconstructed/(2*ns*np.sum(F))-1)<1e-12)
        # Occupancy dephasing time proxy from weighted rms energy spread, not a derived coherence decay.
        av=float(np.sum(F*E)/np.sum(F));spread=math.sqrt(float(np.sum(F*(E-av)**2)/np.sum(F)))
        out=dict(alpha=alpha,K=K,vmax=vmax,source_charge_fraction=1-row['fraction_at_x200'],max_daughter_mode_occupation=float(f.max()),gain_s_inverse=natural_rate/hb,gain_time_seconds=hb/natural_rate,gain_energy_over_spectral_rms=natural_rate/spread,spectral_rms_eV=spread,H_s_inverse=a['H_eV']/hb,gain_over_H=natural_rate/a['H_eV'],fixed_bath_time_to_mode_occupation_1e6_seconds=math.log1p(1e6)*hb/natural_rate)
        local.append(out);rows.append(out)
    for j in [0,2,3]:ck('rate convergence '+str((alpha,j)),abs(local[j]['gain_s_inverse']/local[1]['gain_s_inverse']-1)<1e-4)
# For a kinetic-equilibrium Bose cloud, epsilon3=epsilon1+epsilon2 implies detailed balance.
for e1,e2,T in [(.2,.4,.7),(.01,.03,.7),(1,2,.7)]:
    f1=1/math.expm1(e1/T);f2=1/math.expm1(e2/T);f3=1/math.expm1((e1+e2)/T)
    gain=f1*f2*(1+f3);loss=(1+f1)*(1+f2)*f3
    ck('equilibrium gain-loss cancellation '+str((e1,e2)),abs(gain/loss-1)<1e-12)
out=dict(rows=rows,checks=checks,all_pass=all(x['passed'] for x in checks),scope='Initial fixed dephased bath, vacuum exterior of narrow produced band, leading nonrelativistic two-body phase space; no depletion, moving sources or anomalous covariance retained',non_claims=['No demonstrated dephasing from the Gaussian state','No condensate fraction or physical volume selected','No extrapolation of exponential gain through bath depletion','No full kinetic or cosmological evolution'])
(p/'condensate_gain_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
