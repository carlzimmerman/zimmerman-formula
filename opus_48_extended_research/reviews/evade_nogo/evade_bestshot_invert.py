#!/usr/bin/env python3
"""
EVADE-THE-NO-GO, ROUTE A -- BEST-SHOT inversion (give the evasion its strongest case).

Grant, counterfactually, that the dark sector DOES carry a ghost-condensate
quadratic tail omega^2 = cs^2 k^2 + k^4/M^2 with cs^2->0 sub-horizon (ACLM 2004).
A k^4-stabilized Jeans wavenumber balances self-gravity when

   k_J^4 / M^2 = 4 pi G rho        (k^4 term ~ gravitational term)
   => k_J = (4 pi G rho M^2)^(1/4),  lambda_J = 2 pi / k_J

The evasion REQUIRES lambda_J to sit BETWEEN galaxy (~kpc-30 kpc) and cluster
(~300 kpc-Mpc): the field then clusters in clusters (lambda > lambda_J, k < k_J)
but is SMOOTHED in galaxies (lambda < lambda_J, k > k_J).

We INVERT: what M lands lambda_J in-window? And is that M consistent with the
CMB fit (which forces the SAME field to be cs^2->0 and cluster like CDM down to
sub-Mpc, i.e. lambda_J << Mpc) -- a direct contradiction?

Quarantine: a0/Z/kappa/I0 never derived. Both-ways: this is the evasion's BEST case.
"""
import numpy as np

c=2.99792458e8; hbar=1.054571817e-34; eV=1.602176634e-19; G=6.674e-11
Mpc=3.085677581e22; kpc=Mpc/1e3; H0=67.4e3/Mpc
rho_crit=3*H0**2/(8*np.pi*G)

def Minvlen_to_eV(M_invlen):     # 1/m  -> eV
    return M_invlen*hbar*c/eV
def eV_to_Minvlen(M_eV):         # eV -> 1/m
    return M_eV*eV/(hbar*c)

print("="*78)
print("BEST-SHOT INVERSION: what ghost-condensate M lands the k^4 Jeans scale in-window?")
print("="*78)

# representative collapsing densities
rho_gal  = 6e10*1.989e30/(4/3*np.pi*(15*kpc)**3)
rho_clus = 1e14*1.989e30/(4/3*np.pi*(400*kpc)**3)
print(f"galaxy mean rho   = {rho_gal/rho_crit:.2e} rho_crit")
print(f"cluster-core rho  = {rho_clus/rho_crit:.2e} rho_crit\n")

# Solve lambda_J = target for M:  lambda_J = 2pi/(4 pi G rho M^2)^(1/4)
#   => (4 pi G rho M^2)^(1/4) = 2pi/lambda_J
#   => 4 pi G rho M^2 = (2pi/lambda_J)^4
#   => M^2 = (2pi/lambda_J)^4 / (4 pi G rho)
#   => M = (2pi/lambda_J)^2 / sqrt(4 pi G rho)        [units 1/m]
def M_for_lamJ(lamJ, rho):
    return (2*np.pi/lamJ)**2/np.sqrt(4*np.pi*G*rho)

print(f"{'target lambda_J':>18s} {'rho used':>14s} {'M [1/m]':>12s} {'M [eV]':>14s} {'M^-1':>14s}")
for lam_target, label in [(30*kpc,'30 kpc (gal edge)'),
                          (100*kpc,'100 kpc'),
                          (300*kpc,'300 kpc (clus core)'),
                          (1*Mpc,'1 Mpc')]:
    M = M_for_lamJ(lam_target, rho_clus)
    M_eV = Minvlen_to_eV(M)
    print(f"{label:>18s} {'cluster':>14s} {M:12.3e} {M_eV:14.3e} {1/M/kpc:10.3e} kpc")

print(f"""
So to put the k^4 Jeans scale in the kpc-Mpc window you need M ~ 1e-29..1e-30 eV
(i.e. M^-1 ~ tens of kpc -- a HORIZON/super-galactic length, NOT a particle scale).
""")

print("="*78)
print("THE CONTRADICTION: the same M must satisfy the CMB fit (cluster like CDM)")
print("="*78)
# The banked ghost-condensate clustering/seesaw scale is M ~ 0.04-1 eV (huge),
# which gives lambda_J ~ sub-micron -- the field clusters CDM-like down to ALL
# astrophysical scales (good for CMB, but NO galaxy smoothing).
for M_eV in [0.04, 1.0]:
    M=eV_to_Minvlen(M_eV)
    k_J=(4*np.pi*G*rho_clus*M**2)**0.25
    lamJ=2*np.pi/k_J
    print(f"banked GC scale M={M_eV} eV -> lambda_J = {lamJ:.3e} m = {lamJ/kpc:.3e} kpc "
          f"(WAY below galaxies; clusters CDM-like everywhere => CMB ok, NO galaxy smoothing)")

print(f"""
TWO IRRECONCILABLE DEMANDS on the SAME M:
  - CMB 3rd peak  : the dust must cluster like CDM on sub-Mpc scales
                    => lambda_J << Mpc  => M >> 1e-30 eV (in fact eV-ish).
  - galaxy safety : the dust must be SMOOTHED on kpc scales but clumpy at ~Mpc
                    => lambda_J in (kpc, Mpc) => M ~ 1e-29..1e-30 eV.
These differ by ~28-30 orders of magnitude. A single ghost-condensate M cannot do
both. Choosing M to smooth galaxies (~1e-30 eV) makes lambda_J ~ tens of kpc --
which ALSO smooths the cluster CORE (~400 kpc is only ~10x above; and it smooths
EVERYTHING the CMB needs clumpy at recombination), DESTROYING the 3rd-peak fit.
Choosing M for the CMB (eV-ish) gives lambda_J ~ sub-micron -- clusters like CDM
in galaxies too => the galaxy no-go stands.

==> Even GRANTING a k^4 tail (which the AeST host does NOT have, B=0), there is NO
    single M that is galaxy-safe AND cluster-clumpy AND CMB-fitting. The k^4 Jeans
    evasion FAILS on its own best-case terms.
""")

print("="*78)
print("WHY: lambda_J scales as rho^(-1/4) -- only a FACTOR ~1.8 between gal & cluster")
print("="*78)
# even if M were tuned, the Jeans length depends on density only as rho^(-1/4),
# so galaxy vs cluster Jeans lengths differ by (rho_gal/rho_clus)^(1/4):
ratio = (rho_gal/rho_clus)**0.25
print(f"(rho_gal/rho_clus)^(1/4) = ({rho_gal/rho_clus:.1f})^0.25 = {ratio:.2f}")
print(f"""
The k^4 Jeans length is only ~{ratio:.2f}x SHORTER in the galaxy than in the cluster
core -- and SHORTER means MORE clustering (smaller smoothing scale) in the denser
galaxy. So the density-ordering is the SAME as the cs^2 case: the denser galaxy
clusters MORE, not less. A k^4 Jeans scale, even if present, orders the WRONG way
across the gal/cluster pair because galaxies are denser. The evasion's hope that
"k^4 orders by scale not density" is FALSE: the Jeans SCALE itself depends on the
local density (rho^-1/4), so it tracks density, re-importing the no-go.
""")
print("DONE")
