"""Initial inverse-source flux and fixed-bath linewidth diagnostic with exact decay kinematics."""
import json,math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
p=Path(__file__).parent;hb=6.582119569e-16
vac=json.loads((p/'detuned_carrier_run/results.json').read_text())
data=json.loads((p/'alpha2_bogoliubov_run/results.json').read_text());a=data['parameters']
m=a['m_eV'];M=a['M_eV'];gap=M-2*m;eps=a['epsilon'];ns=a['rho_source_eV4']/M
Gamma=1/vac['vacuum_source_lifetime_seconds'];pstar=math.sqrt((M-2*m)*(M+2*m))/2
checks=[];rows=[]
def ck(n,b):checks.append(dict(name=n,passed=bool(b)))
for ri,nquad in [(0,96),(1,192),(2,256),(3,192)]:
    row=data['rows'][ri];K=row['K'];vmax=row['vmax'];nodes,w=leggauss(K);dv=vmax*w
    q=np.asarray(row['initial_mode_p_over_m']);F=np.asarray(row['final_pair_fractions'])
    E=m*(np.sqrt(1+q*q)-1);wm=m**3*eps*q*dv/(4*math.pi**2*ns);occ=F/wm
    # Piecewise linear occupancy interpolation is refined with inherited production grid.
    def f(e):return np.interp(e,E,occ,left=0.,right=0.)
    cloud=2*ns*sum(F);mean=float(np.sum(F*E)/np.sum(F));rms=math.sqrt(float(np.sum(F*(E-mean)**2)/np.sum(F)))
    emax=2*E[-1]-gap
    zn,zw=leggauss(nquad);u=(zn+1)/2;wu=zw/2
    eb=emax*u*u;deb=2*emax*u*wu
    pn=np.sqrt(eb*(2*M+eb));half=pn*pstar/M;center=(gap+eb)/2
    # Integrate only the support intersection to avoid missing the very narrow shell.
    gain=[];relax=[]
    for c,b,d in zip(center,half,eb):
        lo=max(c-b,E[0],gap+d-E[-1]);hi=min(c+b,E[-1],gap+d-E[0])
        if hi>lo:
            ee=(lo+hi)/2+(hi-lo)*zn/2
            pair=float(np.sum(zw*f(ee)*f(gap+d-ee))*(hi-lo)/2)
        else:pair=0.
        lo=max(c-b,E[0]);hi=min(c+b,E[-1])
        if hi>lo:
            ee=(lo+hi)/2+(hi-lo)*zn/2
            single=float(np.sum(zw*f(ee))*(hi-lo)/2)
        else:single=0.
        lab=Gamma*M/(M+d)
        gain.append(lab*pair/(2*b));relax.append(lab*(1+single/b))
    gain=np.asarray(gain);relax=np.asarray(relax)
    density_of_states=pn*(M+eb)/(2*math.pi**2)
    flux_weights=deb*density_of_states*gain
    flux=float(flux_weights.sum());normalized=flux_weights/flux
    energy_width=hb*relax
    frac_recoil=float(np.sum(normalized*(energy_width>eb)))
    frac_band=float(np.sum(normalized*(energy_width>rms)))
    # Exact two-body energy-momentum check at representative angles.
    d=eb[nquad//2];P=pn[nquad//2];ct=.31;et=(M+d)/2+half[nquad//2]*ct
    parallel=(P/2)+(M+d)/M*pstar*ct;perp=pstar*math.sqrt(1-ct*ct)
    ck('boosted daughter mass shell '+str((ri,nquad)),abs((et*et-parallel*parallel-perp*perp)/(m*m)-1)<1e-12)
    rows.append(dict(production_row=ri,K=K,vmax=vmax,quadrature=nquad,source_number_creation_density_per_second=flux,initial_daughter_charge_depletion_rate_s_inverse=2*flux/cloud,initial_depletion_time_seconds=cloud/(2*flux),source_flux_weighted_recoil_eV=float(np.sum(normalized*eb)),source_flux_weighted_width_eV=float(np.sum(normalized*energy_width)),fraction_of_initial_source_flux_with_width_above_recoil=frac_recoil,fraction_of_initial_source_flux_with_width_above_daughter_rms=frac_band,daughter_energy_rms_eV=rms,max_source_recoil_eV=emax,rate_over_H=2*flux/cloud/(a['H_eV']/hb)))
for j in [0,2,3]:ck('initial flux convergence '+str(j),abs(rows[j]['initial_daughter_charge_depletion_rate_s_inverse']/rows[1]['initial_daughter_charge_depletion_rate_s_inverse']-1)<.01)
out=dict(rows=rows,checks=checks,all_pass=all(c['passed'] for c in checks),scope='Fixed dephased daughter bath, initially empty incoherent moving-source modes; exact vacuum decay kinematics and lab time dilation',non_claims=['No valid finite-time frozen-bath depletion prediction','Inferred width is a self-consistency diagnostic, not a computed spectral function','No proof that all off-shell memory effects are small','No evolving condensate or halo'])
(p/'source_initial_width_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
