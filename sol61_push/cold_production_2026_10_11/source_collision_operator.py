"""Conservative isotropic 1<->2 Bose reaction operator audit, not production evolution."""
import json,math
from pathlib import Path
import numpy as np
p=Path(__file__).parent
checks=[];rows=[]
def ck(n,b):checks.append(dict(name=n,passed=bool(b)))
def build(D):
    # delta=1, h=1/D, daughter and source kinetic energies h..8.
    N=8*D;h=1/D;out=[]
    for k in range(1,N+1):
        eb=k*h;center=(1+eb)/2;half=math.sqrt(eb)
        pairs=[]
        for i in range(1,N+1):
            j=D+k-i
            if j<i or j>N:continue
            e=i*h
            if abs(e-center)<=half+1e-12:pairs.append((i,j,1. if i==j else 2.))
        if pairs:
            norm=sum(t[2] for t in pairs)
            out.extend((i,j,k,w/norm) for i,j,w in pairs)
    return N,h,np.asarray(out)
for D in [8,16,32]:
    N,h,R=build(D);i=R[:,0].astype(int)-1;j=R[:,1].astype(int)-1;k=R[:,2].astype(int)-1;w=R[:,3]
    ea=h*np.arange(1,N+1);eb=ea.copy()
    # Density of states in arbitrary common natural units m=1, Mkin=2.
    ga=(2.)**1.5*np.sqrt(ea)*h/(4*math.pi**2)
    gb=(4.)**1.5*np.sqrt(eb)*h/(4*math.pi**2)
    coeff=gb[k]*w # Gamma0=1 for dimensionless operator audit.
    ck('per-reaction energy '+str(D),np.max(abs(ea[i]+ea[j]-(1+eb[k])))<1e-14)
    ck('vacuum decay normalization '+str(D),np.max(abs(np.bincount(k,weights=w,minlength=N)-1))<1e-14)
    cos=(ea[i]+ea[j]-2)/(2*np.sqrt(ea[i]*ea[j]))
    ck('physical reaction angle '+str(D),np.max(abs(cos))<1+1e-12)
    maxeq=0
    for T,mu in [(.7,-.1),(2.,-.3)]:
        fa=1/np.expm1((ea-mu)/T);fb=1/np.expm1((1+eb-2*mu)/T)
        forward=fb[k]*(1+fa[i])*(1+fa[j]);back=(1+fb[k])*fa[i]*fa[j]
        maxeq=max(maxeq,float(np.max(abs(forward-back)/np.maximum(forward+back,1e-100))))
    ck('chemical equilibrium detailed balance '+str(D),maxeq<1e-12)
    # Deterministic nonequilibrium positive test cloud, no claim it is the produced cloud.
    fa=.2+30*np.exp(-((ea-.5)/.17)**2);fb=.1+2*np.exp(-eb/.4)
    forward=fb[k]*(1+fa[i])*(1+fa[j]);back=(1+fb[k])*fa[i]*fa[j]
    flux=coeff*(forward-back)
    da=np.bincount(i,weights=flux,minlength=N)+np.bincount(j,weights=flux,minlength=N)
    db=-np.bincount(k,weights=flux,minlength=N)
    scale=np.sum(abs(flux))
    qerr=abs(da.sum()+2*db.sum())/scale
    eerr=abs(np.dot(ea,da)+np.dot(1+eb,db))/(scale*max(1,float(ea.max())))
    entropy=np.sum(flux*np.log(forward/back))
    # Orthogonal entropy derivative via mode entropy gradient.
    ds=np.dot(np.log1p(1/fa),da)+np.dot(np.log1p(1/fb),db)
    ck('total charge derivative '+str(D),qerr<1e-13)
    ck('total excess energy derivative '+str(D),eerr<1e-13)
    ck('nonnegative entropy production '+str(D),entropy>0)
    ck('entropy gradient identity '+str(D),abs(ds/entropy-1)<1e-12)
    # Physical mean and variance of daughter energy for a source with eb=.5.
    sel=k==D//2-1;ii=i[sel];jj=j[sel];ww=w[sel];center=.75
    mean=float(np.sum(ww*(ea[ii]+ea[jj])/2))
    variance=float(np.sum(ww*((ea[ii]-center)**2+(ea[jj]-center)**2)/2))
    rows.append(dict(D=D,reactions=len(R),max_equilibrium_relative_residual=maxeq,charge_derivative_relative_error=qerr,energy_derivative_relative_error=eerr,positive_entropy_production=entropy,source_half_gap_daughter_energy_mean=mean,source_half_gap_daughter_energy_variance=variance,continuum_variance=1/6))
ck('daughter energy variance refinement',abs(rows[-1]['source_half_gap_daughter_energy_variance']-1/6)<abs(rows[0]['source_half_gap_daughter_energy_variance']-1/6))
# Production resolution requirement, without pretending audit grids resolve it.
a=json.loads((p/'alpha2_bogoliubov_run/results.json').read_text())['parameters']
requirement=(a['M_eV']-2*a['m_eV'])/(a['m_eV']*a['epsilon'])
out=dict(rows=rows,delta_over_production_energy_scale=requirement,checks=checks,all_pass=all(c['passed'] for c in checks),scope='Finite energy-grid source conversion operator with exact per-reaction conservation and detailed balance; no time integration, source condensate or daughter condensate',non_claims=['Audit grids do not resolve actual production bandwidth','No coherent-to-kinetic handoff','No actual evolving spectrum or yield','Elastic and condensate operators not yet coupled'])
(p/'source_collision_operator_run/results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2));assert out['all_pass']
