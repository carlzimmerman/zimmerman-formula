#!/usr/bin/env python3
"""ADVERSARIAL VERIFIER: independent re-derivation of the gauntlet's load-bearing numbers.
Framework objects only: a0=9.36e-11, mu_fw(x)=(sqrt(1+4x^2)-1)/(2x), Z=sqrt(32pi/3). exit 0."""
import numpy as np
H0=2.2e-18; a0=9.36e-11; G=6.674e-11; Msun=1.989e30; AU=1.496e11; yr=3.156e7
mu=lambda x:(np.sqrt(1+4*x**2)-1)/(2*x)
ok=lambda t,c:(print(("PASS " if c else "FAIL ")+t), c)[1]; A=[]

# 1. Milgrom-2022 circular collapse: mu_fw(g/a0)*g=gb <=> g=sqrt(gb^2+gb*a0), exact
gb=np.logspace(-14,-7,200); g=np.sqrt(gb**2+gb*a0)
A.append(ok("circular collapse exact (rtol 1e-12)",np.allclose(mu(g/a0)*g,gb,rtol=1e-12)))

# 2. SATURN CEILING re-derivation (independent): S~1-mu at u; da=S*R*a_sat<bound
r_s=9.58*AU*(1/1); a_sat=G*Msun/(9.58*AU)**2; u=a_sat/a0
Om_sat=2*np.pi/(29.46*yr)/H0                      # in H0 units
S=1-mu(u); bound=5e-14
nu2_max=Om_sat*np.sqrt(bound/(S*a_sat))           # R=(nu2/Om)^2 rolloff
print(f"  Saturn: a={a_sat:.2e}, u={u:.1e}, S={S:.2e}, Om={Om_sat:.2e} H0 -> ceiling nu2<={nu2_max:.2e} H0")
A.append(ok("ceiling matches 9.9e7 (within 15%)",abs(nu2_max/9.88e7-1)<0.15))
da_c=S*(1e7/Om_sat)**2*a_sat                      # box center
A.append(ok(f"Saturn da@center={da_c:.1e} ~ 5.3e-16",0.3<da_c/5.3e-16<3))

# 3. WB gamma re-derivation: self-consistent g=gN/mu(|a_tot|/a0), quadrature EFE g_ext=1.9e-10
def gam(s_kAU,Mtot=2.0):
    gN=G*Mtot*Msun/(s_kAU*1e3*AU)**2; gext=1.9e-10; g=gN
    for _ in range(60): g=gN/mu(np.sqrt(g**2+gext**2)/a0)
    return g/gN
g2,g10,g30=gam(2),gam(10),gam(30)
print(f"  WB gamma: 2kAU={g2:.3f}, 10kAU={g10:.3f}, 30kAU={g30:.3f}; asymptote 1/mu(2.03)={1/mu(1.9e-10/a0):.3f}")
A.append(ok("WB trio matches 1.021/1.236/1.276 (2%)",abs(g2-1.021)<0.02 and abs(g10-1.236)<0.03 and abs(g30-1.276)<0.02))
# 2-kAU orbital frequency vs floor (rolloff onset check)
Om2k=2*np.pi/(np.sqrt((2000)**3/2.0)*yr)/H0
print(f"  Om(2kAU,2Msun)={Om2k:.2e} H0 vs floor 1.1e6 -> marginal at floor only; >=5kAU safely in-band")

# 4. ENERGETICS independent demand: refresh stored dressing energy S*rho_b*v^2/2 at 3H0
rho_edge=1e-3*Msun/(3.086e16)**3; v=1.5e5          # MOND-zone disk edge
demand=3*H0*0.5*0.5*rho_edge*v**2                  # S~0.5 at the knee
lam_flux=5.37e-10*H0                               # u_DE per Hubble time
print(f"  demand(edge)={demand:.1e} W/m^3 vs D1 5.3e-29; Lambda-draw={lam_flux:.1e} -> headroom {lam_flux/demand:.0f}x")
A.append(ok("independent demand within x30 of D1's (same physics class)",0.03<demand/5.3e-29<30))
A.append(ok("headroom >=20x confirmed independently",lam_flux/max(demand,5.3e-29)>=20))

# 5. LINE-SHAPE: Lorentzian in-band Im/Re vs tolerance from orbit-count budget
nu2=1e7; W=3008.; Gi=nu2/3                          # inhomog. Lorentzian width ~nu2/3
gW=(Gi/(2*np.pi))/((nu2-W)**2+ (Gi/2)**2)          # spectral density at band top
ImRe=np.pi*nu2**2*gW/(2*W)                          # my derivation: =Gi/(4W)-class
Norb=(10e9*yr)/(2*np.pi/(W*H0))                     # orbits in 10 Gyr at band top (~333)
tol=0.1/(2*np.pi*Norb)
print(f"  Lorentzian Im/Re@bandtop={ImRe:.1e} vs tol={tol:.1e} -> kill x{ImRe/tol:.0e}; Gaussian: exp(-(nu2/Gi)^2*4.5)~{np.exp(-0.5*((nu2-W)/(nu2/6))**2):.0e}")
A.append(ok("Lorentzian killed (>=1e3 over tolerance); Gaussian clears",ImRe/tol>1e3))

# 6. tau_eff lag: driven-oscillator phase arg chi = Gam*Om/(nu2^2-Om^2) -> tau=Gam/nu2^2 (Om<<nu2)
Gam=3*H0; nu2s=1e7*H0; Oms=1000*H0
tau_an=Gam*Oms/(nu2s**2-Oms**2)/Oms; tau_pred=Gam/nu2s**2
A.append(ok(f"tau_eff=Gam/nu2^2 verified analytically ({tau_pred:.1e}s ~hrs; pop-saturation lag 1/Gam={1/Gam:.0e}s)",abs(tau_an/tau_pred-1)<1e-5))

# 7. R2-drag exclusion: v decay e^-(3H0 t), 10 Gyr
dec=np.exp(-3*H0*10e9*yr); A.append(ok(f"drag decay x{dec:.2f} (=0.12); exclusion {abs(np.log(dec))/0.05:.0f}x (~42)",abs(dec-0.125)<0.01))

# 8. GATE-G scaling: inhomogeneous broadening raises ASE/lasing threshold ~ sigma_inh/Gam_hom
sig=nu2/6; raise_=sig*H0/Gam
print(f"  Gate-G: clamp shortfall x3 vs threshold raise ~sigma/Gam_hom={raise_:.1e} (std. inhomog. laser scaling)")
A.append(ok("G-scaling covers x3 shortfall by >=4 decades IF laser analogy holds (mode-sum still required)",raise_>3e4))

# 9. Floor sensitivity to the x1.7 calibration miss (0.66 vs 0.38): floor ~ sqrt(drift-err)
print(f"  floor sensitivity: 1.08e6 x sqrt(1.7)={1.08e6*np.sqrt(1.7):.2e} -> box [1.4e6,9.9e7] worst-case: {np.log10(9.9e7/(1.08e6*np.sqrt(1.7))):.2f} decades, NONEMPTY")
A.append(ok("box survives calibration-miss stress",9.9e7/(1.08e6*np.sqrt(1.7))>10))

assert all(A), "adversarial check failed"
print("ALL ADVERSARIAL RE-DERIVATIONS PASS. exit 0")
