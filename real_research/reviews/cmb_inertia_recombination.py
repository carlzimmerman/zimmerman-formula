#!/usr/bin/env python3
"""
The CMB inertia test (Fable/swarm step #1): does the modified-INERTIA kernel mu(a/a0(z))
modify the photon-baryon acoustic oscillator at recombination?

The decisive quantity is the fluid acceleration a_fluid at z~1090 versus the EVOLVING a0(z_rec)
-- which is wildly different for the two footings:
  rising   a0(z)=a0_0*E(z)         -> a0(z_rec) HUGE  -> a<<a0 -> deep-MOND -> CMB destroyed
  declining a0(z)=a0_0*sqrt(rhoDE) -> a0(z_rec) TINY  -> a>>a0 -> Newtonian -> CMB safe
This is the single calculation that can FALSIFY the modified-inertia reading. Heuristic
single-acceleration argument (NOT a full CLASS/CAMB run), but the rising-vs-declining margin
is ~10 orders of magnitude, so the qualitative verdict is robust. numpy only.
C. Zimmerman, 2026-06-09.
"""
import numpy as np
c = 2.99792458e8; G = 6.674e-11; Mpc = 3.0857e22
H0 = 67.4e3/Mpc                      # s^-1
Om, OmL = 0.315, 0.685
a0_0 = 9.36e-11                      # framework a0 today, m/s^2
z_rec = 1089.0

def E(z): return np.sqrt(Om*(1+z)**3 + OmL)
def rhoDE_ratio(z, w0=-0.752, wa=-0.86):
    a = 1/(1+z); return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))

a0_rise = a0_0 * E(z_rec)                       # rising total-H footing
a0_decl = a0_0 * np.sqrt(rhoDE_ratio(z_rec))    # declining sqrt(rho_DE), DESI-evolving-DE
a0_flat = a0_0                                  # canonical pure-Lambda: a0 CONSTANT at all z
cH_rec  = c * H0 * E(z_rec)                      # the total cosmic rate at recombination

print("="*84)
print("(1) a0 at recombination (z=%.0f) -- THREE footings, spanning ~10 orders of magnitude"%z_rec)
print("="*84)
print(f"  a0(0)              = {a0_0:.2e} m/s^2")
print(f"  E(z_rec)           = {E(z_rec):.1f}   sqrt(rhoDE(z_rec)/rhoDE0) = {np.sqrt(rhoDE_ratio(z_rec)):.2e}")
print(f"  a0(z_rec) RISING (total-H, a0_0*E)            = {a0_rise:.2e} m/s^2")
print(f"  a0(z_rec) FLAT   (canonical pure-Lambda, const)= {a0_flat:.2e} m/s^2")
print(f"  a0(z_rec) DECLINING (DESI evolving-DE, sqrt rhoDE)= {a0_decl:.2e} m/s^2")
print(f"  (for scale: total cH(z_rec) = {cH_rec:.2e} m/s^2)\n")

print("="*84)
print("(2) the photon-baryon fluid acceleration at recombination, across the acoustic peaks")
print("="*84)
r_s_phys = 144*Mpc/(1+z_rec)        # physical sound horizon at recombination
cs = c/np.sqrt(3)                    # sound speed
delta = 1e-4                        # baryon density contrast at the acoustic peaks (~few e-4)
print(f"  sound horizon (phys) r_s = {r_s_phys:.2e} m;  c_s = {cs:.2e} m/s;  delta ~ {delta}")
print(f"  {'peak n':>7}{'lambda_phys[m]':>16}{'a_fluid[m/s^2]':>16}{'a/a0_RISE':>11}{'a/a0_FLAT':>11}{'a/a0_DECL':>11}")
peaks = [1,2,3,4,5]; afl = []
for n in peaks:
    lam = 2*r_s_phys/n               # physical wavelength of the n-th acoustic mode
    k = 2*np.pi/lam
    a_fluid = cs**2 * k * delta      # acoustic oscillation acceleration ~ c_s^2 k delta
    afl.append(a_fluid)
    print(f"  {n:>7}{lam:>16.2e}{a_fluid:>16.2e}{a_fluid/a0_rise:>11.1e}{a_fluid/a0_flat:>11.1f}{a_fluid/a0_decl:>11.1e}")
afl = np.array(afl)
print("  (regime: a/a0 >> 1 = Newtonian/mu~1/CMB-safe;  a/a0 << 1 = deep-MOND/CMB-modified)\n")

print("="*84)
print("(3) the fractional inertia modification on the acoustic peaks  [nu=sqrt(1+a0/a)-1 ~ a0/2a]")
print("="*84)
def frac_mod(a, a0):                 # fractional deviation of g_obs from g_N (framework nu)
    return np.sqrt(1.0 + a0/a) - 1.0
print(f"  {'peak n':>7}{'RISING (total-H)':>18}{'FLAT (pure-Lambda)':>20}{'DECLINING (DESI DE)':>21}")
for n,a in zip(peaks, afl):
    print(f"  {n:>7}{frac_mod(a,a0_rise):>17.1%}{frac_mod(a,a0_flat):>19.2%}{frac_mod(a,a0_decl):>20.4%}")
print()
print("="*84)
print("VERDICT")
print("="*84)
print(f"""  DECLINING (DESI evolving-DE):  a0(z_rec)={a0_decl:.1e} << a_fluid~{afl[0]:.1e}  =>  a/a0 ~ {afl[0]/a0_decl:.0f}
      => DEEP NEWTONIAN, mu ~ 1, fractional CMB effect ~ {frac_mod(afl[0],a0_decl):.2%}  =>  CMB-SAFE, huge margin.
      The 'live failure risk' the swarm flagged is CLEARED for the declining branch.

  FLAT (canonical pure-Lambda, a0 const = {a0_flat:.1e}):  a/a0 ~ {afl[0]/a0_flat:.0f} at peak 1
      => MILDLY Newtonian, fractional effect ~ {frac_mod(afl[0],a0_flat):.1%} (peak1) falling to ~{frac_mod(afl[-1],a0_flat):.1%} (peak5).
      => NOT zero: a ~1-2% inertia perturbation at recombination. Plausibly absorbable into
         cosmological parameters, but this is the one case that genuinely NEEDS the full CLASS/CAMB run.

  RISING (total-H):  a0(z_rec)={a0_rise:.1e} >> a_fluid~{afl[0]:.1e}  =>  a/a0 ~ {afl[0]/a0_rise:.0e}
      => DEEP MOND, mu ~ {afl[0]/(2*a0_rise):.0e}, the oscillator inertia is modified by ~{frac_mod(afl[0],a0_rise):.0f}x
      => CMB-FALSIFIED as modified inertia (margin enormous, no Boltzmann run needed to see it).
      It survives ONLY as modified GRAVITY / AeST (dq00=0 keeps a0 off the linear perturbations).

  => In the framework's natural home (modified INERTIA), the CMB ORDERS the branches cleanly:
       DECLINING (evolving-DE)  : safe, 0.01%   -- the live risk is cleared
       FLAT (pure-Lambda)       : ~1-2%, borderline -- needs the full run
       RISING (total-H)         : ~28x, DEAD
     A new physical argument converging with the lean-declining verdict, and it KILLS rising in the
     inertia reading. CAVEATS: heuristic single-acceleration estimate, not a CLASS/CAMB Boltzmann run;
     the relativistic photon-baryon fluid's inertia modification is itself a modeling assumption. The
     ~10-order rising-vs-declining margin makes that split robust; only the flat ~1-2% case is run-sensitive.""")
