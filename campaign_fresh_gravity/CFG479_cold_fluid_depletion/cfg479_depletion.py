#!/usr/bin/env python3
"""CFG479: cold-fluid normal fraction from the Bogoliubov depletion law -- door C
of the openai/math re-read.

Outside lemma (positive-temperature BEC paper + quantum depletion paper): in the
dilute hard-sphere Bose gas the nonzero-momentum occupation has total mass
8/(3 sqrt(pi)), i.e. the depletion fraction in the thermodynamic limit is

    n_ex/n = (8/3) * sqrt(n a^3 / pi)      (Bogoliubov leading law)

EXACTLY: n_ex/n = (8/(3 sqrt(pi))) * sqrt(n a^3)  [a = scattering length = the
excluded distance between hard-sphere centers; proven taking the thermodynamic
limit before the dilute limit].

Transfer: the two-fluid cold mass has a normal (uncondensed) component whose
size is currently treated as fit output. Door C: in any dilute regime
(n a^3 << 1) the normal fraction is FIXED by the product n a^3:
   nu = (8/(3 sqrt(pi))) * sqrt(n a^3).
With rho_cold = Omega_c rho_crit = const * m * n, the product is
   n a^3 = (rho_cold / m) * a^3.

The dark-sector free parameters are (m, a) -- the mass per cold particle and
its scattering length. If the scalar-field mass scale mu is the natural length
(a ~ hbar/(mu c) -- Compton scale of the khronon), the table below shows what
normal fractions result. If the framework's fitted two-fluid normal fraction
(CFG378/CFG418) falls outside the band at the physical (mu, m), door C closes.

KILL CONDITION: nu_fit outside [nu_min, nu_max] over the physical parameter
range -> the condensate picture of the cold fluid is wrong (door C closed).
"""
import numpy as np

# Fitzpatrick/PDG-style inputs
HC_MeV_m = 197.3269804e-6      # hbar*c in MeV*m  (actually MeV*m): 1.973e-7 MeV m
CC = 299792458.0               # m/s
RHO_CRIT = 1.878e-26           # kg/m^3  (h=0.674)
OMEGA_C = 0.26
RHO_C = OMEGA_C * RHO_CRIT     # kg/m^3

MEV_PER_KG = 5.609e29          # energy equiv.

def norm_frac(a_m, m_ev):
    """nu = (8/(3 sqrt pi)) sqrt( n a^3 ),  n = rho_c / m (kg->eV)."""
    n = RHO_C * MEV_PER_KG / m_ev   # particles per m^3  (m in eV)
    return (8.0/(3.0*np.sqrt(np.pi))) * np.sqrt(n * a_m**3)

def main():
    print("="*72)
    print("CFG479: cold-fluid normal fraction pinned by Bogoliubov depletion")
    print("="*72)
    print(f"rho_cold = {RHO_C:.3e} kg/m^3")
    # parameter map: dark particle mass m and scattering length a
    # rows: mass m (eV), with a = Compton scale of the khronon mass mu
    mu_grid = np.array([4.7e-27, 1e-26, 5e-26, 1e-25])   # eV (khronon band)
    a_grid  = HC_MeV_m / (mu_grid * MEV_PER_KG * CC)     # m  (hbar/(mc))
    m_grid  = np.logspace(-2, 2, 5) * 1e-5               # eV: 1e-7 .. 1e-3 eV
    print(f"\na (Compton of mu): {['%.3e' % a for a in a_grid]} m")
    print(f"\nnormal fraction nu = (8/3)*sqrt(n a^3/pi)  (rows = m in eV, cols = mu):")
    print("m \\ mu   " + "  ".join(f"{mu:.1e}" for mu in mu_grid))
    for m in m_grid:
        row = [norm_frac(a, m) for a in a_grid]
        print(f"{m:.2e}  " + "  ".join(f"{v:6.2e}" for v in row))
    # dilution check: need n a^3 << 1 for the law itself
    print("\ndilution n a^3 grid (must be << 1 for the law to apply):")
    print("m \\ mu   " + "  ".join(f"{mu:.1e}" for mu in mu_grid))
    for m in m_grid:
        row = [RHO_C*MEV_PER_KG/m * a**3 for a in a_grid]
        print(f"{m:.2e}  " + "  ".join(f"{v:6.1e}" for v in row))
    # inverse: the scattering length a REQUIRED to give a target normal fraction
    print("\nrequired scattering length a_req for target normal fraction nu (m):")
    print(f"(a_req = n^{-1/3} * (nu*3*sqrt(pi)/8)^(2/3); n = rho_c/m)")
    print("m \\ nu   " + "  ".join(f"{nu:5.2f}" for nu in (0.05, 0.1, 0.2, 0.3)))
    for m in m_grid:
        n = RHO_C * MEV_PER_KG / m
        row = [(nu*3*np.sqrt(np.pi)/8.0)**(2.0/3.0) / n**(1.0/3.0)
               for nu in (0.05, 0.1, 0.2, 0.3)]
        print(f"{m:.2e}  " + "  ".join(f"{v:8.3g}" for v in row))
    print("READ-OFF: if the two-fluid dark normal fraction is O(0.1-0.3), the "
          "dark-sector scattering length must be ~0.2-2 mm for m~1e-5..1e-3 eV "
          "(table above) -- a macroscopic self-interacting cold sector "
          "(SIDM-like, still far below astrophysical SIDM scales). If the "
          "framework needs nu ~ 0 with microscopic a, depletion is negligible "
          "and the normal component must come from something else (door C "
          "falsifies that route).")
    print("\n" + "-"*72)
    print("Status: formula pinned (8/(3 sqrt pi)); the band is set once (m, mu)")
    print("are identified. If the fitted two-fluid normal fraction disagrees,")
    print("door C closes.")
    print("="*72)

if __name__ == "__main__":
    main()