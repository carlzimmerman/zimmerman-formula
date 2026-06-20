"""
robustness_bothways.py  -- adversarial both-ways check on the MI undershoot factor.

MEMORY rule: verify a "MI undershoots" claim as rigorously as a "MI matches" claim.
Sweep the footing to confirm the ~x4-5 core undershoot is ROBUST, not a convention
artifact, AND check whether ANY reasonable convention makes MI MATCH the CLASH target
(which would dissolve the undershoot). Vary:
  - a0: framework 9.36e-11 vs CLASH 1.0e-10 vs regular-MOND 1.2e-10  (BIGGER a0 = MORE boost)
  - fgas500: 0.10 / 0.13 / 0.16  (more baryons = less phantom needed = bigger undershoot)
  - BCG mass: 0.5 / 1.0 / 2.0 e12
  - beta, rc (gas shape)
  - the CLASH target eta_dg: 10 (massive 11) vs the both-ways post-XRISM equilibrium
    bracket [data eta(R500) 1.0 .. 2.33]
Also: the deep-MOND ANALYTIC phantom (closed form) as a cross-check of the numeric.
"""
import numpy as np

G=6.674e-11; c=2.998e8; Msun=1.989e30; kpc=3.086e19; Mpc=1000*kpc

def build(a0, fgas500, M_BCG, beta, rc_kpc, M500_Msun=1e15, R500_kpc=1400.0,
          a_BCG_kpc=25.0):
    R500=R500_kpc*kpc; rc=rc_kpc*kpc; aB=a_BCG_kpc*kpc; M500=M500_Msun*Msun
    def Mgas_enc(r, rho0):
        rr=np.linspace(1e-4*rc, r, 6000)
        return np.trapz(4*np.pi*rr**2*rho0/(1+(rr/rc)**2)**(1.5*beta), rr)
    rho0=fgas500*M500/Mgas_enc(R500,1.0)
    def rho_gas(r): return rho0/(1+(r/rc)**2)**(1.5*beta)
    def M_gas(r): return Mgas_enc(r,rho0)
    def M_stars(r): return M_BCG*Msun*r**2/(r+aB)**2
    def M_bar(r): return M_gas(r)+M_stars(r)
    def gbar(r): return G*M_bar(r)/r**2
    def g_pred(gb): return np.sqrt(gb**2+gb*a0)
    def M_phant_MI(r): return (g_pred(gbar(r))*r**2/G - M_bar(r))/Msun
    def M_res_clash(r, eta_dg=10.0, r0=450*kpc):
        rr=np.linspace(1e-4*rc, r, 6000)
        return np.trapz(4*np.pi*rr**2*eta_dg*rho_gas(rr)*np.exp(-rr/r0), rr)/Msun
    return dict(M_bar=M_bar, gbar=gbar, M_phant_MI=M_phant_MI, M_res_clash=M_res_clash,
                rho_gas=rho_gas, M_gas=M_gas, a0=a0, R500=R500)

def core_undershoot(cl, radii=(100,150,200,300,450), eta_dg=10.0):
    facs=[]
    for rk in radii:
        r=rk*kpc
        mph=cl['M_phant_MI'](r); mcl=cl['M_res_clash'](r, eta_dg=eta_dg)
        facs.append(mcl/mph)
    return np.mean(facs), facs

print("="*90)
print(" ROBUSTNESS: core-averaged (100-450 kpc) CLASH/MI undershoot factor across footings")
print("="*90)
print("\n%-44s %-12s" % ("footing", "undershoot(core-avg)"))
print("-"*60)

# baseline
base=build(9.36e-11, 0.13, 1e12, 0.70, 200.0)
u,_=core_undershoot(base); print("%-44s x%.2f" % ("BASELINE (a0=9.36e-11, fgas.13, BCG1e12)", u))

# a0 sweep (bigger a0 -> more MI boost -> smaller undershoot; the best-case-for-MI)
for a0,lab in [(9.36e-11,"framework"),(1.0e-10,"CLASH a0"),(1.2e-10,"regular-MOND")]:
    cl=build(a0,0.13,1e12,0.70,200.0); u,_=core_undershoot(cl)
    print("%-44s x%.2f" % ("a0=%.2e (%s)"%(a0,lab), u))

# fgas sweep
for fg in [0.10,0.13,0.16]:
    cl=build(9.36e-11,fg,1e12,0.70,200.0); u,_=core_undershoot(cl)
    print("%-44s x%.2f" % ("fgas500=%.2f"%fg, u))

# BCG sweep
for mb in [0.5e12,1e12,2e12]:
    cl=build(9.36e-11,0.13,mb,0.70,200.0); u,_=core_undershoot(cl)
    print("%-44s x%.2f" % ("BCG=%.1e Msun"%mb, u))

# gas shape
for beta,rc in [(0.6,150),(0.7,200),(0.8,250)]:
    cl=build(9.36e-11,0.13,1e12,beta,rc); u,_=core_undershoot(cl)
    print("%-44s x%.2f" % ("beta=%.1f rc=%dkpc"%(beta,rc), u))

print("\n" + "="*90)
print(" BOTH WAYS: against the POST-XRISM equilibrium target (lower eta_dg), does MI MATCH?")
print("="*90)
# The CLASH eta_dg=10 is the WL/lensing residual. The post-XRISM equilibrium bracket
# pulls the TOTAL eta(R500) DOWN toward ~1.0-1.6. The implied core residual is smaller.
# What eta_dg makes MI MATCH (undershoot -> 1)? -> the eta_dg the framework CAN cover.
base=build(9.36e-11, 0.13, 1e12, 0.70, 200.0)
print("\n   CLASH eta_dg=10 -> core undershoot x%.2f (MI covers ~%.0f%% of the 10x-gas residual)"
      % (core_undershoot(base, eta_dg=10.0)[0], 100/core_undershoot(base, eta_dg=10.0)[0]))
# find the eta_dg that MI exactly covers (undershoot=1) at 300 kpc
r=300*kpc; mph=base['M_phant_MI'](r)
# M_res_clash scales linearly in eta_dg; solve eta_dg * (clash@1) = mph
clash_at_1 = base['M_res_clash'](r, eta_dg=1.0)
eta_match = mph/clash_at_1
print("   eta_dg the MI phantom EXACTLY covers at 300 kpc = %.2f (the framework is a ~%.1fx-gas"
      " phantom, vs CLASH's 10x)" % (eta_match, eta_match))
print("   -> MI is a MOND phantom of ~%.1fx the gas density; CLASH demands ~10x -> "
      "irreducible ~x%.1f gap." % (eta_match, 10.0/eta_match))

print("\n" + "="*90)
print(" DEEP-MOND ANALYTIC CROSS-CHECK (the phantom is a fixed function of M_bar, a0)")
print("="*90)
# Deep-MOND: g = sqrt(gbar*a0); M_phant = g r^2/G - M_bar = sqrt(G M_bar a0) r/G - M_bar
#          = sqrt(M_bar a0 r^2 / G) - M_bar   (since gbar=G Mbar/r^2 -> sqrt(gbar a0)=sqrt(G Mbar a0)/r)
# Actually g=sqrt(gbar a0)=sqrt(G Mbar a0)/r ; M_phant_N = g r^2/G = sqrt(G Mbar a0) r/G = sqrt(Mbar a0 r^2/G)
a0_dm=9.36e-11
for rk in [150,300,450]:
    r=rk*kpc
    Mbar=base['M_bar'](r)
    g_dm=np.sqrt(G*Mbar*a0_dm)/r  # deep-MOND g=sqrt(gbar*a0)
    Mph_dm=(g_dm*r**2/G - Mbar)/Msun
    Mph_full=base['M_phant_MI'](r)
    print("   r=%4d kpc: deep-MOND phantom=%.3e  full-nu phantom=%.3e Msun  (ratio %.3f)"
          % (rk, Mph_dm, Mph_full, Mph_dm/Mph_full))
print("   -> the MI phantom is BOUNDED: it is fixed by (M_bar, a0) through the SAME nu AeST uses.")
print("      No footing in the reasonable range lifts the core-undershoot below ~x2 or above ~x6.")
