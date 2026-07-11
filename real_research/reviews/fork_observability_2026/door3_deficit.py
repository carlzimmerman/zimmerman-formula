#!/usr/bin/env python3
"""
DOOR 3 -- What does Branch A (modified INERTIA) owe gravitational lensing,
and does anything MINIMAL + non-DM supply it?

Framework-first. Uses the framework's OWN interpolation:
    g_obs = sqrt(g_bar^2 + g_bar * a0)     ->  nu(g_bar) = g_obs/g_bar = sqrt(1 + a0/g_bar)
NOT McGaugh's nu.  a0 both footings: 9.36e-11 (canon) / 1.13e-10 (alt).

Logic of the fork:
  Branch A = modified inertia. MI modifies the equation of motion of MASSIVE
  test bodies; it does NOT modify null geodesics -> light bending is NOT
  sourced by MI.  So if the framework is pure MI, the observed
  gravitational lensing needs a REAL dark mass component.
  The weak-lensing RAR (Brouwer+2017/2021 KiDS; Mistele-McGaugh 2023/2024)
  measures g_obs(g_bar) FROM LENSING and finds it = the dynamical RAR.
  Therefore the required lensing source is real, and its amount is exactly
  the phantom  M_D(r) = M_bar(r) * (nu-1).
  Question: can anything minimal + non-DM (neutrinos / missing baryons /
  a cold relic) supply that phantom profile?

No commits, no Zenodo. exit 0.
"""
import numpy as np

# ---------------------------------------------------------------- constants
G      = 6.674e-11          # m^3 kg^-1 s^-2
Msun   = 1.989e30           # kg
kpc    = 3.0857e19          # m
Mpc    = 1000*kpc
eV     = 1.0                # work in eV for masses where noted
c      = 2.998e8            # m/s

A0 = {'canon': 9.36e-11, 'alt': 1.13e-10}   # m/s^2, both footings

# framework nu (its OWN dS-Unruh interpolation)
def nu(gbar, a0):
    return np.sqrt(1.0 + a0/gbar)           # = g_obs/g_bar, g_obs=sqrt(gb^2+gb a0)

# ---------------------------------------------------------------- fiducial disk
Mbar_disk = 5.0e10*Msun     # baryonic mass
Rd        = 3.0*kpc         # exponential scale length

def Mbar_enc(r):
    """Enclosed baryonic mass, exponential thin disk approximated as
    spherically-enclosed M(<r) = Mtot [1 - (1+r/Rd) exp(-r/Rd)]."""
    x = r/Rd
    return Mbar_disk*(1.0 - (1.0+x)*np.exp(-x))

def gbar_of_r(r):
    return G*Mbar_enc(r)/r**2

# ============================================================================
print("="*78)
print("DOOR 3 -- Branch A (modified inertia) lensing deficit: EXACT required source")
print("="*78)
print(f"Fiducial disk: M_bar = {Mbar_disk/Msun:.2e} Msun, exp scale R_d = {Rd/kpc:.1f} kpc")
print("Framework nu = sqrt(1 + a0/g_bar)   [its own interpolation, NOT McGaugh]")
print()

# radial grid out to 500 kpc
r = np.logspace(np.log10(0.3*kpc), np.log10(500*kpc), 400)

for tag, a0 in A0.items():
    gb = gbar_of_r(r)
    n  = nu(gb, a0)
    MD = Mbar_enc(r)*(n-1.0)          # phantom dark mass M_D = M_bar (nu-1)
    print(f"--- footing {tag}: a0={a0:.3e} m/s^2 ---")
    for rr in [10,50,100,200,500]:
        i = np.argmin(np.abs(r-rr*kpc))
        print(f"  r={rr:4d} kpc: g_bar={gb[i]:.2e}  nu={n[i]:.2f}  "
              f"M_bar={Mbar_enc(r[i])/Msun:.2e}  M_D(phantom)={MD[i]/Msun:.2e} Msun")
    print()

# ---------------------------------------------------------------- rho_D and DeltaSigma
print("-"*78)
print("Required phantom volume density rho_D=(1/4piG) div[(nu-1)g_bar]")
print("and lensing excess surface density DeltaSigma(R) (the WL observable).")
print("Deep-MOND analytic check (point-mass): DeltaSigma = sqrt(M_bar a0 /G)/(4R),")
print("isothermal rho~r^-2, amplitude ~ sqrt(M_bar) == the BTFR/lensing signature")
print("Mistele-McGaugh 2024 MEASURE (indefinitely-flat v, v^4 ~ M_bar).")
print("-"*78)

def deltaSigma_numeric(a0, Rgrid):
    """Numeric DeltaSigma of the TOTAL (bar+phantom) mass = what lensing sees.
    rho_tot from M_dyn(r)=nu*M_bar(r): rho=(1/4pi r^2) dM_dyn/dr.
    Sigma(R)=2 int_0^inf rho(sqrt(R^2+z^2)) dz ; DeltaSigma=Sigmabar(<R)-Sigma(R)."""
    rr = np.logspace(np.log10(0.05*kpc), np.log10(20*Mpc), 3000)
    Mdyn = nu(gbar_of_r(rr), a0)*Mbar_enc(rr)
    dM   = np.gradient(Mdyn, rr)
    rho  = dM/(4*np.pi*rr**2)
    rho  = np.clip(rho, 0, None)
    from numpy import interp
    def rho_at(x):
        return interp(x, rr, rho, right=0.0)
    z = np.logspace(np.log10(0.02*kpc), np.log10(30*Mpc), 1500)
    Sig=[]; Sbar=[]
    for R in Rgrid:
        s = 2*np.trapz(rho_at(np.sqrt(R**2+z**2)), z)
        Sig.append(s)
    Sig=np.array(Sig)
    # mean within R
    Rf = Rgrid
    Mproj = np.concatenate([[0],np.cumsum(0.5*(Sig[1:]*2*np.pi*Rf[1:]+Sig[:-1]*2*np.pi*Rf[:-1])*np.diff(Rf))])
    Sbar = Mproj/(np.pi*Rf**2)
    return Sbar-Sig

Rg = np.logspace(np.log10(30*kpc), np.log10(2*Mpc), 25)
for tag,a0 in A0.items():
    dS = deltaSigma_numeric(a0, Rg)
    # analytic deep-MOND point-mass amplitude for comparison
    amp = np.sqrt(Mbar_disk*a0/G)/(4*Rg)     # kg/m^2
    tokgm2_to_Msunpc2 = (1.0/Msun)*(3.0857e16**2)   # kg/m^2 -> Msun/pc^2
    print(f"--- footing {tag}: a0={a0:.3e} ---")
    for j in [0,8,16,24]:
        print(f"  R={Rg[j]/kpc:7.1f} kpc: DeltaSigma_numeric={dS[j]*tokgm2_to_Msunpc2:7.3f}  "
              f"analytic(pt-mass deepMOND)={amp[j]*tokgm2_to_Msunpc2:7.3f}  Msun/pc^2")
    print()

print("=> The numeric ESD tracks the sqrt(M_bar) isothermal 1/R law at large R:")
print("   this is EXACTLY the measured weak-lensing RAR (Brouwer+2021 extends the")
print("   RAR 2 dex below rotation curves; Mistele-McGaugh 2024 extend 2.5 dex to")
print("   ~1 Mpc, indefinitely-flat v_c, v^4 ~ M_bar). The lensing RAR = dynamical")
print("   RAR, so the required phantom source is REAL and its amount is M_bar(nu-1).")
print()

# ============================================================================
print("="*78)
print("SUPPLIER TEST -- can anything MINIMAL + non-DM furnish M_D(r)=M_bar(nu-1)?")
print("="*78)

# ---- (a) NEUTRINOS ---------------------------------------------------------
print("\n(a) NEUTRINOS (hot relic)")
h = 0.68
Om = 0.315; OL = 0.685
rho_crit = 1.878e-26*h**2      # kg/m^3
Om_dm = 0.265
for sm in [0.06, 0.10]:        # sum m_nu in eV (normal-hierarchy floor .. loose)
    Om_nu = sm/(93.14*h**2)
    # comoving free-streaming length today (Mpc/h), standard approx
    #   lambda_fs ~ 7.7 (1+z)/sqrt(OL+Om(1+z)^3) * (1 eV/m_nu)  Mpc/h  ; per-species mass
    m_per = sm/3.0
    lam_fs = 7.7*(1.0)/np.sqrt(OL+Om)*(1.0/m_per)      # z=0, Mpc/h
    print(f"  sum m_nu={sm:.2f} eV: Omega_nu={Om_nu:.4f}  (Omega_dm={Om_dm})  "
          f"ratio Om_nu/Om_dm={Om_nu/Om_dm:.4f}")
    print(f"     free-streaming length lambda_fs(z=0) ~ {lam_fs*1000/h/1000:6.0f} Mpc  "
          f"(per-species m={m_per:.3f} eV) -- vs required 0.01-0.5 Mpc scale")
# Tremaine-Gunn phase-space bound: min mass to build a galaxy-scale halo
# m_nu^4 >~ ( ... )  -> for a system with sigma, r_c: rough TG dwarf bound ~100 eV
print("  Tremaine-Gunn phase-space bound: packing a galaxy halo (sigma~100 km/s,")
print("  r_c~kpc) from degenerate light fermions needs m_nu >~ tens-hundreds of eV;")
print("  0.06-0.1 eV neutrinos are ~10^3 below that -> phase-space EXCLUDED.")
print("  VERDICT (a): FAIL on BOTH axes -- amount ~100-200x too small AND free-")
print("  streaming length ~300-600 Mpc >> the 10-500 kpc scale where phantom must sit.")

# ---- (b) MISSING / COLD BARYONS -------------------------------------------
print("\n(b) MISSING / COLD BARYONS")
Ob = 0.049
fb = Ob/Om
print(f"  cosmic baryon fraction f_b = Om_b/Om_m = {fb:.3f}")
# Branch A has NO CDM halo, so no M_halo to multiply f_b by. The gravitating
# baryons available to a 5e10 disk = its own stars+gas + CGM (~few x M_star).
# The phantom mass GROWS ~linearly with r (isothermal, unbounded):
for tag,a0 in A0.items():
    for rr in [200,500,1000]:
        rm = rr*kpc
        MD = Mbar_enc(rm)*(nu(gbar_of_r(rm),a0)-1.0)
        print(f"    [{tag}] r={rr:4d} kpc: phantom M_D={MD/Msun:.2e} Msun  "
              f"(= {MD/Mbar_disk:5.1f} x M_bar)")
print("  Generous CGM+missing baryons around a 5e10 disk ~ (1-3)x M_star ~ 1e11 Msun,")
print("  FINITE and declining. The phantom needs mass DIVERGING with radius out to")
print("  ~Mpc (already several x M_bar by 200-500 kpc). Worse, the missing cosmic")
print("  baryons are WHIM/CGM at 1e5-1e7 K -- hot, diffuse, pressure-supported --")
print("  NOT a cold isothermal r^-2 cusp centred on each galaxy scaling as sqrt(M_bar).")
print("  VERDICT (b): FAIL -- neither the AMOUNT (unbounded vs finite) nor the SHAPE")
print("  (hot diffuse vs cold isothermal sqrt(M_bar)) matches.")

# ---- (c) A COLD RELIC THAT CLUSTERS ---------------------------------------
print("\n(c) A COLD RELIC THAT CLUSTERS on 10-500 kpc")
print("  A single cold, clustering relic with rho ~ r^-2 and amount tuned to")
print("  M_bar(nu-1) IS, by construction, particle cold dark matter with a")
print("  MOND-shaped halo. It supplies the lensing -- but it is exactly the dark")
print("  matter the no-DM premise was meant to avoid. 'Fitting' here = CONCEDING DM.")

# ============================================================================
print("\n"+"="*78)
print("VERDICT")
print("="*78)
print("""Nothing MINIMAL + non-DM supplies the required source.
 - neutrinos: FAIL (amount ~100-200x short; free-streaming ~300-600 Mpc; TG phase-space
   excludes them from galaxy halos by ~10^3 in mass).
 - missing/cold baryons: FAIL (phantom mass is unbounded-growing & isothermal
   sqrt(M_bar); real missing baryons are finite, hot, diffuse -- wrong amount AND
   wrong shape).
 - a cold clustering relic: only 'works' by BEING particle dark matter -> concedes DM.

Therefore Branch A (pure modified inertia) OWES a genuine cold, clustering dark
component with the phantom isothermal sqrt(M_bar) profile to bend light -- because
MI does not modify null geodesics and the weak-lensing RAR (= dynamical RAR,
Brouwer 2021 / Mistele-McGaugh 2024) proves the lensing phantom is real.

This is the SYMMETRIC cost of the fork: Branch A buys a clean solar-system pass
but must import real DM for lensing (or hand lensing to Branch B's disformal
dark-energy medium). Both branches are expensive. Result invariant across BOTH
footings (a0=9.36e-11 / 1.13e-10): amounts scale ~sqrt(a0) (~10%), no PASS/FAIL
flips. Honest, not manufactured: this is the well-known MOND weak-lensing burden,
inherited exactly.""")

# machine-checkable assertions (prove-by-moving-the-number)
Om_nu_06 = 0.06/(93.14*h**2)
assert Om_nu_06/Om_dm < 0.01, "neutrino amount should be <1% of DM"
for a0 in A0.values():
    MD200 = Mbar_enc(200*kpc)*(nu(gbar_of_r(200*kpc),a0)-1.0)
    assert MD200 > Mbar_disk, "phantom at 200 kpc must exceed M_bar (unbounded growth)"
print("\n[assertions passed] exit 0")
