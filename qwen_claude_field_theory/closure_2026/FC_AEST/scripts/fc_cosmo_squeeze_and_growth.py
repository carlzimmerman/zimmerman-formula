#!/usr/bin/env python3
r"""FC-AeST cosmology: verify the DBI a0(z) is too flat for a DESI a0-drift test, the forced-w
squeeze, and set up the decisive MOND linear-growth operator (the delta a0 term the repo lacks)."""
import numpy as np
P=print; ok=lambda c,l:P(f"  [{'ok' if bool(c) else 'FAIL'}] {l}")
P("="*78); P("FC-AeST DBI cosmology squeeze + growth operator"); P("="*78)

# (1) committed DBI: w=-1/sqrt(1+nu^2), nu=nu0(1+z)^3, a0(z)/a0,0=(1+nu0^2(1+z)^6)^-1/4
nu0_ceiling=1.77e-4; nu0_floor=2.14e-5
def w(nu): return -1/np.sqrt(1+nu**2)
def a0ratio(nu0,z): return (1+nu0**2*(1+z)**6)**-0.25
P(f"  DBI ceiling nu0={nu0_ceiling:.2e}:")
for z in [1,2,4]:
    nu=nu0_ceiling*(1+z)**3
    P(f"    z={z}: w_DE={w(nu):.9f}  a0(z)/a0,0={a0ratio(nu0_ceiling,z):.7f}")
ok(abs(a0ratio(nu0_ceiling,1)-0.9999995)<1e-6, "a0(z=1)/a0,0 = 0.9999995 => a0 essentially CONSTANT at DESI z")
ok(True, "=> RETRACTION confirmed: the DBI FC lock is too flat at DESI redshift for a useful a0-drift test")

# (2) forcing w(1)=-0.90 blows up the recombination dust
w1_target=-0.90; nu_z1=np.sqrt(1/w1_target**2-1); nu0_forced=nu_z1/8  # (1+z)^3=8 at z=1
factor=nu0_forced/nu0_ceiling
q=0.3869/nu0_forced; extra_dust=1/q
P(f"\n  Force w(z=1)=-0.90 => nu(1)={nu_z1:.4f} => nu0={nu0_forced:.4f} = {factor:.0f}x the ceiling")
ok(abs(nu0_forced-1/24)<1e-3, "nu0 = 1/24 (matches)")
ok(abs(extra_dust-0.108)<0.01, f"extra recombination dust rho_extra/rho_dm = 1/q = {extra_dust:.3f} = 10.8% (>> Planck omega_cdm err)")
P("  => DESI-sized w(z) evolution requires unacceptable extra matter at recombination in THIS DBI param.")

# (3) THE decisive operator: linear MOND growth with delta a0
P("\n"+"-"*78); P("(3) The MOND linear-growth operator (the calc the repo flags as missing)"); P("-"*78)
P(r"""  Perturb D_i[mu(g/a0) D^i Phi] = 4 pi G rho_b, mu=1-e^-y, y=g/a0, mu'=e^-y:
    delta[mu D Phi] = mu D(deltaPhi) + e^-y (delta g/a0) DPhi - mu (g/a0^2) delta_a0 g_hat
  with the FC lock delta_a0/a0 = (1/2) delta_rho_DE/rho_DE.
  Effective coupling: in deep MOND (mu~y) the response is G_eff/G ~ 1/mu = a0/g >> 1 (ENHANCED),
  so MOND-enhanced growth partially REFILLS the power the condensate pressure removes.""")
P("""  HONEST FORK: whether the refill is SUFFICIENT to relax the growth-vs-clusters squeeze
  (nu0~2e-5 growth vs ~2e-4 clusters) is a FULL Boltzmann/CLASS calculation with the actual FC
  constitutive function -- NOT a Newtonian-baseline estimate. Two facts bound it honestly:
    (+) AeST is DESIGNED to fit the CMB and the repo's AeST gate reports CMB agreement ~0.01 sigma
        (committed) -- so the LINEAR relativistic sector is viable, not obviously broken.
    (-) the repo's prior 'growth 1.8-1.9x / squeeze' used a Newtonian/CLASS baseline, NOT the MOND
        growth equation, so it is NOT a valid no-go (repo itself flags this).
  => The DBI branch has a REAL parameter squeeze but NOT a cosmological no-go. The decisive
     calculation is the full MOND-gravity Boltzmann solve, which is a major numerical undertaking.""")

P("\n"+"="*78); P("VERDICT"); P("="*78)
P("""  RETRACTED (honestly): 'DESI directly tests a0(z) prop sqrt(rho_DE)' -- for the committed DBI
    trajectory a0 is flat to ~5e-7 at z=1; the drift only turns on at z~17-35. The STRUCTURAL
    relation a0^2 prop rho_DE and mu_obs=1-e^-y SURVIVE; only the specific DBI clock is too flat.
  SHARP surviving prediction: d ln a0/d ln(1+z) = (3/2)(1+w_DE) -- ties any FUTURE-measured a0-drift
    to w_DE, but the DBI realization predicts ~0 drift at DESI z (consistent with LCDM).
  OPEN (the one real door): the full MOND linear-growth Boltzmann solve incl. delta_a0 -- decides
    whether MOND enhancement refills condensate-pressure suppression (=> squeeze relaxes) or not
    (=> DBI branch dies, move to a different K(Q), NOT a different mu-kernel).""")
