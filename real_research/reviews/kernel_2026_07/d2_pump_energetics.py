#!/usr/bin/env python3
"""
BUREAU D2 / script 2 -- THE PUMP + ENERGETICS GATE, computed head-on, both ways.
Medium: inverted anharmonic ladder, gaps 44-3008 H0 (+ ~1 decade support past edges, script 1),
per-rung inversion held against Gamma >= 3 H0 (R2), for a Hubble time, homogeneously (R3).
Gate: minimum power the pump must process; compare rho_DE, rho_b, CMB/FIRAS, ISM heating, ephemerides.
State clause (DOI 10.5281/zenodo.21139029): thermal/KMS sources CANNOT invert -- the dS horizon is a
thermostat; free fields are state-blind. Fourth Horn (DOI 10.5281/zenodo.21148494) forces the nonlocal kernel.
"""
import numpy as np
ok=True
def chk(name,cond,msg=""):
    global ok; print(("  PASS " if cond else "  FAIL ")+name+("  "+msg if msg else "")); ok = ok and cond

# constants / framework objects
H0=2.2e-18; c=2.998e8; G=6.674e-11; hbar=1.055e-34; kB=1.381e-23
Z=np.sqrt(32*np.pi/3); a0=9.36e-11; HL=Z*a0/c
Gam=3*H0; tH=1/H0; Gyr=3.156e16
rho_c=3*H0**2/(8*np.pi*G); u_DE=0.69*rho_c*c**2; rho_b=0.049*rho_c
Tcmb=2.725; u_CMB=7.566e-16*Tcmb**4; n_gam=4.11e8
T_dS=hbar*HL/(2*np.pi*kB)
print("="*100); print("A  RESERVOIR LEDGER (the only homogeneous, Hubble-persistent reservoirs)"); print("="*100)
print(f"  H_Lambda = Z a0/c = {HL:.2e}/s (={HL/H0:.2f} H0); t_H = {tH/Gyr:.1f} Gyr")
print(f"  u_DE  = {u_DE:.2e} J/m^3 (inert, w=-1)     u_CMB = {u_CMB:.2e} J/m^3 (thermal, 2.725 K)")
print(f"  rho_b c^2 = {rho_b*c**2:.2e} J/m^3            T_dS = {T_dS:.1e} K (KMS thermostat)")
print(f"  max homogeneous draw rate: u_DE*H0 = {u_DE*H0:.2e} W/m^3 ; u_CMB*H0 = {u_CMB*H0:.2e} W/m^3")

print("="*100); print("B  MINIMUM STANDING COST: locked-response energy and its Gamma-leak"); print("="*100)
# bookkeeping posit of ANY dynamical-medium completion: the missing kinetic energy (1-mu) 1/2 m v^2
# is carried by medium excitations phase-locked to each worldline; R2 dissipates it at Gamma>=3H0.
v_gal=2.2e5; fdeep=0.5
P_kg=Gam*0.5*fdeep*v_gal**2
Lam_ISM=1e-33/1.673e-27      # ~1e-26 erg/s per H atom -> W/kg (ISM radiative budget)
print(f"  per unit baryon mass: P = 3H0*(1-mu)v^2/2 = {P_kg:.2e} W/kg (v=220 km/s, (1-mu)=0.5)")
print(f"    vs ISM radiative budget {Lam_ISM:.1e} W/kg -> {P_kg/Lam_ISM*100:.0f}%   vs stellar 1.9e-4 W/kg -> {P_kg/1.9e-4*100:.2f}%")
chk("worldline-side leak below ISM/stellar budgets (heating bound passes)", P_kg<Lam_ISM)
Mb=1.2e41; P_MW=Gam*0.5*fdeep*Mb*v_gal**2; L_MW=9.6e36
print(f"  Milky Way total: {P_MW:.1e} W = {P_MW/L_MW*100:.2f}% of L_MW")
# cosmic-mean locked energy density and pump floor
v_bar=1.5e5; u_lock=rho_b*0.5*0.8*v_bar**2
P_lock=Gam*u_lock
print(f"  cosmic locked density u_lock ~ rho_b*<(1-mu)v^2/2> = {u_lock:.1e} J/m^3;  pump floor P_min = 3H0 u_lock = {P_lock:.1e} W/m^3")
print(f"  headroom vs DE draw: {u_DE*H0/P_lock:.1e}x ;  vs CMB draw: {u_CMB*H0/P_lock:.1e}x")
chk("RAW ENERGY GATE PASSES with >= 6 orders headroom -- NO energetic fifth theorem; do not manufacture one",
    u_DE*H0/P_lock>1e6)
# relativistic-medium momentum floor (script-1 D1 already excludes it; show why it also fails here)
p_mom=rho_b*0.5*v_bar; u_rel=c*p_mom
drain_rel=3*u_rel/u_CMB
print(f"  IF medium were luminal: momentum floor u_inv >= c*rho_b*f*v = {u_rel:.1e} J/m^3 -> CMB-pump drain {drain_rel*100:.0f}% of u_CMB: FIRAS-dead")
print(f"  massive constituents (D1): momentum carried by rest mass, u_inv floor collapses to ~u_lock = {u_lock:.1e} J/m^3")

print("="*100); print("C  QUANTUM FLOOR + LINEWIDTH ENGINEERING"); print("="*100)
om_mid=300*H0; nq=(0.5*0.8*v_bar**2)/(hbar*om_mid)
print(f"  locked quanta per kg at 300 H0: {nq:.1e} -> amplifier (Caves) noise fraction {1/np.sqrt(nq):.1e}: NEGLIGIBLE")
chk("quantum/spontaneous noise NOT a killer (occupations ~1e58/kg)", nq>1e50)
print(f"  Gamma flat = 3H0 demanded across band; RADIATIVE rates scale om^3|x|^2 ~ om^5: span (68.4)^5 = {68.4**5:.1e}")
print("  -> Gamma cannot be radiative; must be COLLISIONAL with the baryon fluid (om-independent, T-odd, R2-compatible)")
print("     side effects: Gamma ~ n_b sigma v varies with environment; only Gamma>=3H0 ON ORBITS is required (POSIT P4)")

print("="*100); print("D  R4 SAFETY (band-limited, gapped medium)"); print("="*100)
for name,om in [("Saturn (Cassini)",2*np.pi/9.3e8),("LLR (Moon)",2.66e-6),("wide binary 5kAU",3.1e5*H0),
                ("PSR timing (~yr)",2e-7),("LIGO",600.0),("lab (Hz)",6.28)]:
    print(f"   {name:20s} omega = {om/H0:.1e} H0 -> above band top by x{om/(3008*H0):.1e}")
print("  gapped lines: Im chi ~ Gamma*Omega/omega_g^4 wings -> dissipative response at Omega >> band falls ~(om_top/Omega)^3")
sup_sat=(3008*H0/(2*np.pi/9.3e8))**3
print(f"  Saturn suppression ~{sup_sat:.0e}; DC (CMB-frame drift 370 km/s): gapped medium has Im chi(0)=0 EXACTLY -> no secular drag")
chk("solar system/LLR/pulsar/LIGO/lab safe by construction (out-of-band + gapped)", sup_sat<1e-15)
print("  NOTE: support extension to ~3e4 H0 (script 1) still x1e4 below Saturn; WB at 3.1e5 H0 above all support -> gamma->1 prediction stands")

print("="*100); print("E  THE PUMP: every candidate, adjudicated"); print("="*100)
print("  requirement: hold n_inv(omega) ~ W_flat/om^2 inverted at EVERY rung, homogeneously, for t_H, at P >= 3H0*u_inv")
# 1 dS horizon
print("  [1] dS horizon: KMS at T_dS={:.1e} K -- a THERMOSTAT cannot invert any medium (state clause, DOI 21139029): KILLED".format(T_dS))
# 2 inert Lambda
print("  [2] inert Lambda (w=-1): no dynamical channel, no work extraction without the (KMS) horizon: KILLED")
# 3 slow-roll coherent drive
for ng in (44,3008):
    sup=10**(-2*(ng-1)*np.log10(2))   # eta=1/2 per-photon amplitude, rate ~ eta^{2(n-1)}
    print(f"  [3] rolling-DE coherent drive (om_d ~ H0): rung {ng} H0 needs {ng}-photon process, suppression ~1e{np.log10(sup):.0f}", end="")
    print(" : KILLED" if ng==3008 else "")
# 4 galactic
print("  [4] galactic feedback/local dynamics: scale = local Omega not cH_Lambda/Z; vanishes in dSphs; R3 killed (pump hunt)")
# 5 relic, no pump
drift=Gam/np.log(10)*Gyr    # dex per Gyr of lookback
print(f"  [5] RELIC inversion, no pump: decays e^-3H0 t -> a0 drift +{drift:.3f} dex/Gyr lookback")
d_sparc=drift*(137*3.0857e22/c)/Gyr    # 137 Mpc light travel
print(f"      SPARC internal spread (D<=137 Mpc): {d_sparc:.3f} dex < 0.079 budget: NOT excluded by SPARC")
for z,tlb in [(0.5,5.2),(1.0,7.9),(2.0,10.4)]:
    print(f"      z={z}: +{drift*tlb:.2f} dex (x{10**(drift*tlb):.1f})", end="")
print("\n      sign matches contested MUSE-DARK III 'rising a0'; magnitude LARGE; BUT a0 becomes an initial condition --")
print("      BREAKS the framework's own a0 = cH_Lambda/Z constancy: OFF-CANON branch (fork below)")
# 6 CMB-cycled multilevel
sig=Gam/(n_gam*c)
dep_frac=hbar*om_mid/(2.82*kB*Tcmb)
drain=3*u_lock/u_CMB
print(f"  [6] CMB-cycled multilevel (4-level optical pumping; dS horizon = cold sink):")
print(f"      thermodynamically LEGAL: T_CMB/T_dS = {Tcmb/T_dS:.1e} Carnot gap; cycling >= 3H0 needs sigma_abs ~ {sig:.1e} m^2 (Thomson=6.7e-29)")
print(f"      per-cycle rung deposit fraction hbar om_rung/hbar om_CMB ~ {dep_frac:.1e}")
print(f"      NET CMB drain over t_H at the u_lock floor: 3 u_lock/u_CMB = {drain:.1e} of u_CMB vs FIRAS |dU/U| <~ 5e-5:")
print(f"      -> CMB-peak-band version PINCHED (x{drain/5e-5:.0f} over FIRAS at MINIMUM drain)")
uRJ=8*np.pi*kB*Tcmb*(6e10)**3/(3*c**3)
print(f"      radio-tail version (pump line <60 GHz): drain/u_RJ = {3*u_lock/uRJ*100:.2f}% vs ~1-10% radio-background bounds: SURVIVES ~1 order")
print("      BUT the architecture is a POSIT-STACK: a new field with a ~30-order internal hierarchy (1e-4 eV pump line +")
print("      1e-33 eV ladder), engineered branching into ~1e6 rungs with n_inv ~ W_flat/om^2, collisional Gamma: NOT known physics")

print("="*100); print("F  GAIN-CLAMP / ASE SELF-CONSISTENCY (the undecided cliff)"); print("="*100)
print("  an inverted cosmological medium amplifies its own propagating in-band collective modes (mirrorless ASE);")
print("  inversion clamps when amplification rate ~ mode escape/redshift rate ~ H0; required response rate = Gamma = 3H0.")
print(f"  clamp scale / demand scale = H0/3H0 = 0.33: SAME ORDER -- cannot be decided at bureau resolution;")
print("  if the clamp lands BELOW demand: deep-edge normalization fails band-wide (a clean kill); if AT demand:")
print("  it would EXPLAIN the exact |dm|->m edge (P2 for free). DECISIVE FOLLOW-UP COMPUTATION.")

print("="*100); print("G  BOTH-WAYS FORK TABLE (non-negotiable #4)"); print("="*100)
print("  BRANCH A (canonical, a0 = cH_Lambda/Z = 9.36e-11 CONSTANT): a pump is REQUIRED forever.")
print("     [1]-[4] killed on state/selectivity/R3; ONLY [6] survives, as a 3-deep posit-stack pinched by FIRAS")
print("     to its radio-tail variant. NO known-physics pump. Energetics does NOT kill it (B: 6-8 orders headroom).")
print("  BRANCH B (relic, decaying): NO pump needed; PREDICTS a0(z) rising as e^{3H0 t_lb} (+0.09 dex/Gyr);")
print("     survives SPARC (0.04 dex internal), sign-compatible with contested MUSE rise, testable at z~0.1-0.5;")
print("     but a0 is then an initial condition -- the cH_Lambda/Z identity and R3-by-construction are FORFEIT.")
print("  Neither branch yields the expected energetic fifth theorem; the gate that remains is EXISTENCE/SELECTIVITY,")
print("  not power. The honest name for [6]: 'a pump can be written down; none is known.'")
assert ok, "one or more checks FAILED"
print("ALL CHECKS PASSED (d2_pump_energetics)")
