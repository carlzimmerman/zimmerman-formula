"""Post-production quantum kinetic diagnostics for the Hinf=m source only.

No assumed cold normalization. Uses the saved vacuum occupation spectrum.
Nphi+2 NX is exactly conserved by X <-> Phi Phi; its violation is separately
bounded/diagnosed. Dense high-H source is explicitly outside this calculation.
"""
import json,sys
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid, simpson
from scipy.special import roots_legendre

p=Path(__file__).parent
data=json.loads((p/'physical_spectrum_wkb2_v2_run/results.json').read_text())['rows'][-1]
m=.001;u=.02;M=2*m*np.sqrt(1+u*u);g=2.168e-6;lam=.00881292
Gamma=g*g/(8*np.pi*M)*np.sqrt(1-4*m*m/M**2)
a0=data['a']; H0=m/(1+a0*a0)
phi,X=data['species']; k=np.array(phi['k']); occ=np.array(phi['occupation'])
Nphi=m**3*phi['n_comoving']; NX=m**3*X['n_comoving']; Ntot=Nphi+2*NX
Mpl=2.435e18;gst=106.75
Ta=(90/(np.pi**2*gst))**.25*np.sqrt(Mpl*m)
Sa=2*np.pi**2/45*gst*Ta**3
C=json.loads((p/'neutral_four_to_two_v2_run/results.json').read_text())['loss_coefficient_GeV_minus8']

def occupation(q):
 return np.exp(np.interp(np.log(np.maximum(q,k[0])),np.log(k),np.log(occ)))*((q>=k[0])&(q<=k[-1]))

cc=1+2*u*u;D=np.sqrt(cc*cc-1)
def inverse_rate(a,order,dense):
 # Total of the two charge channels. Identical-incoming symmetry 1/2.
 # R=g^2 m^2/(8 pi^3) int de1 f1 int_[e-,e+] de2 f2.
 logq=np.linspace(np.log(k[0]),np.log(k[-1]),dense)
 q=np.exp(logq); e=np.sqrt(1+(q/a)**2)
 weight=occupation(q)*q*q/(a*a*e)
 # Tail cumulative avoids subtracting a huge IR constant at large k.
 tail=-cumulative_trapezoid(weight[::-1],logq[::-1],initial=0)[::-1]
 def J(q):
  return np.interp(np.log(np.maximum(q,k[0])),logq,tail,left=tail[0],right=0)
 # Resolve the integrable cusp where the partner can be at rest.
 center=a*D
 extra=center*(1+np.r_[-np.geomspace(1e-9,.99,70),np.geomspace(1e-9,2,70)])
 edges=np.unique(np.r_[k,extra[(extra>k[0])&(extra<k[-1])]])
 edges=np.log(edges); nodes,weights=roots_legendre(order)
 q=np.exp((edges[:-1,None]+edges[1:,None])/2+(edges[1:,None]-edges[:-1,None])/2*nodes)
 q1=q/a;e1=np.sqrt(1+q1*q1)
 low=a*np.abs(cc*q1-D*e1);high=a*(cc*q1+D*e1)
 integral=occupation(q)*q*q/(a*a*e1)*(J(low)-J(high))
 value=np.sum(integral*weights*(edges[1:,None]-edges[:-1,None])/2)
 return float(g*g*m*m/(8*np.pi**3)*value)

rates=[]
for count,order,dense in [(121,12,30001),(241,24,60001)]:
 av=np.geomspace(a0,1000,count)
 R=np.array([inverse_rate(a,order,dense) for a in av])
 Ninv=simpson(av**3*R/(m/(1+av**2)),x=np.log(av))
 rates.append(dict(grid=count,events_comoving_GeV3=float(Ninv),
                  weighted_fraction= float(2*Ninv/Ntot)))

# Leading vacuum decay, justified at the actual decay epoch by redshift.
# H=m/(1+a^2) gives dt/dlog(a)=(1+a^2)/m exactly.
av=np.geomspace(a0,1e7,20001)
time=(np.log(av/a0)+(av*av-a0*a0)/2)/m
survival=np.exp(-Gamma*time)
prob=Gamma*(1+av**2)/m*survival
norm=simpson(prob,x=np.log(av))
mean_a2=simpson(av**2*prob,x=np.log(av))/norm
daughter_k2=u*u*mean_a2
phi_k2=simpson(k**5*occ,x=np.log(k))/simpson(k**3*occ,x=np.log(k))
km=np.array(X['k']);fo=np.array(X['occupation'])
X_k2=simpson(km**5*fo,x=np.log(km))/simpson(km**3*fo,x=np.log(km))
# Isotropic decay boost adds parent comoving momentum squared /4 at leading
# NR order, plus corrections of order u^2 vX^2.
daughter_k2+=X_k2/4
total_k2=(Nphi*phi_k2+2*NX*daughter_k2)/Ntot
Teq=.8e-9;gseq=3.91;aeq=Ta/Teq*(gst/gseq)**(1/3)
vrms=np.sqrt(total_k2)/aeq

# Conservative forward XXbar loss using no decays and H=m/(1+a^2).
sigmav=np.sqrt(1-m*m/M**2)*g**4/(2*np.pi*M**6)
lossXX=sigmav*NX**2/(2*m)*(1/a0+1/(3*a0**3))

# A reference well after all but exp(-50) of X decays, then 100x expansion.
a50=np.interp(50/Gamma,time,av);aref=100*a50
nref=Ntot/aref**3;Href=m/(1+aref*aref)
opt42=C*nref**3/Href/7 # forward loss integral; tiny so no feedback

# Early nonlinear phase scales: these are approximation diagnostics, not
# a theorem controlling every higher-order quantum correlation.
quartic_phase=2*lam*Ntot/(m**3)*(1/a0+1/(3*a0**3))
early_stim_a=1000.
maxfX=max(X['occupation'])
stim_bound=(g*g*D/(2*np.pi*m))*maxfX*(early_stim_a**2-a0*a0)/(2*m)
out=dict(checks=dict(inverse_refinement=abs(rates[0]['events_comoving_GeV3']/rates[1]['events_comoving_GeV3']-1)<.02,
 decay_normalization=abs(norm-1)<1e-8,late_velocity=vrms<1e-10,
 dilute_phase=quartic_phase<1e-4),
 source='Existing Hinf=m=1 MeV vacuum spectrum, both charges; not the high-H lattice source.',
 Gamma_GeV=float(Gamma),inverse_formation=rates,
 leading_final_yield=float(Ntot/Sa),direct_Phi_yield=float(Nphi/Sa),
 leading_abundance_fraction=float((m*Ntot/Sa)/4.37e-10),
 initial_X_weight_fraction=float(2*NX/Ntot),
 leading_final_vrms_at_T_0p8eV=float(vrms),
 mean_decay_scale_factor_squared=float(mean_a2),
 direct_Phi_comoving_k2=float(phi_k2),daughter_comoving_k2=float(daughter_k2),
 XX_loss_fraction_upper_diagnostic=float(lossXX/Ntot),
 late_4to2_loss_fraction_diagnostic=float(opt42),late_reference_a=float(aref),
 integrated_quartic_phase_diagnostic=float(quartic_phase),
 conservative_early_stimulated_events_per_Phi_bound=float(stim_bound),
 assumptions=['Adiabatic post-production particle interpretation and leading Gaussian charge-symmetric state.',
  'Standard visible entropy history; fixed gstar=106.75 in production/decay era, 3.91 for late entropy mapping.',
  'Saved k interval only; omitted IR and UV tails retain prior spectrum uncertainties.',
  'Inverse formation evaluated on the freely redshifting spectrum; the small event fraction checks perturbative feedback.',
  'XX forward diagnostic and late 4-to-2 threshold regime; no claimed full early resonant 3-to-2/4-to-2 collision solution.'],
 conclusion='A controlled leading dilute-branch relic estimate, with computed inverse formation and late number-loss diagnostics. It does not solve the dense high-H source or certify an all-channel nonperturbative error bound.')
out['all_pass']=all(out['checks'].values())
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
sys.exit(0 if out['all_pass'] else 1)
