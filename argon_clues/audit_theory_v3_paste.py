"""argon_clues: arithmetic audit of the pasted 'free u=0 cold energy from untethered hot gas' mechanism (paste 12)."""
import math
nu=lambda y:0.5*(1+math.sqrt(1+4/y))
R0=4.80; fcond=0.16; fhot=0.84
print('nu_s(y=0.18)=%.3f (paste 2.91)'%nu(0.18))
for cv in (0.5,0.6,0.7,0.8,0.95,1.0):
    r=(1+(nu(0.18)-1)*fcond+cv*fhot*R0)/nu(0.18); print('cluster ratio vs containment c_vir=%.2f: %.3f'%(cv,r))
print('   paste uses c_vir=0.95 (assumed; NFW containment inside R500 is ~0.6-0.75); c_vir needed for x1.80: %.3f'%(((1.80*nu(0.18)-1-(nu(0.18)-1)*fcond)/(fhot*R0))))
print('   record: CFG745 needed C = k*M_hot with k = 2.9-3.6 (fit to X-COP); k/R0 = %.2f-%.2f; the pasted k=R0 needs containment 0.60-0.75 not 0.95'%(2.9/R0,3.6/R0))
# outer slope
w_free,w_tet,w_b=fhot*R0*0.95,(nu(0.18)-1)*fcond,1.0
tot=w_free+w_tet+w_b; a=(w_free*1.0+w_tet*0.47+w_b*1.0)/tot
print('shear slope, mass-weighted (free slope 1, tethered 0.47, baryons 1): %.3f ; paste weights 0.80/0.20 -> 0.894 are not the mass fractions (free share %.2f, tethered %.2f)'%(a,w_free/tot,w_tet/tot))
# ETG
for f in (0.2,0.45,0.5,0.9): print('ETG: dlog10(1+f), f=%.2f -> %.3f dex (paste claims +0.28 with f=0.45-0.5; +0.28 needs f=%.2f)'%(f,math.log10(1+f),10**0.28-1))
print('   eROSITA/CFG746-sealed M_hot(<100kpc)=1.1-1.6e10 vs M*=6.3e10 (log M* 10.8): f_hot = %.2f-%.2f, not 0.45-0.5'%(1.1e10/6.3e10,1.6e10/6.3e10))
# UFD budget
print('UFD: nu_s at 25 pc ~12 (paste) vs total native cold supply R0=4.8 (+1 baryon): the law phantom (nu-1)=11 already exceeds 4.8 -> CFG336 mass-budget fail; adding a FREE core of ~4.6 M_star on top violates it further')
print('   coincidence 0.5*log10(4.8)=%.3f dex vs +0.33: sigma^2 ~ M reading; the same paste uses sigma ~ M^(1/4) elsewhere (0.17 dex) -> reading chosen post hoc; record: binary-corrected excess +0.295+-0.163 (1.8 sigma), not 3.8'%(0.5*math.log10(4.8)))
# BH cavitation radius
G=6.6743e-11; Ms=1.98847e30; a0=9.36e-11; pc=3.0857e16; Ls=5.75*pc
for M in (1e8,6.5e9):
    rs=math.sqrt(G*M*Ms/a0); print('r_sat(%.1e)=%.0f pc ; r_cav=(r_sat L*^2)^(1/3)=%.1f pc (only an estimate: the stiffness ODE was not solved)'%(M,rs/pc,(rs*Ls**2)**(1/3)/pc))
print('P5: Delta Omega_DE = 0.0493*0.564*6.84 = %.3f (ok) but 6.84 back-solved; and desi_conversion_test.py already EXCLUDES this psi/anchoring against the DESI DR2 CPL bands.')
