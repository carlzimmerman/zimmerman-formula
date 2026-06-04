#!/usr/bin/env python3
"""
The prefactor consistency condition: Friedmann factor = DSSYK central DOS -- and it lands in the N-V regime.
==========================================================================================================
Carl's observation: a0 = (c/2)sqrt(G rho) = c^2/(2R*) and a0 = cH/(2sqrt(8pi/3)) = cH/Z are the SAME equation,
with Z = 2 sqrt(8pi/3) being EXACTLY the Friedmann conversion sqrt(G rho_crit) <-> H (verified: ratio = 1.000000).
So the coefficient Z is not a free dictionary number -- it is Friedmann. (Whether the two forms agree at all
hinges on WHICH rho: rho_crit/apparent -> rising a0; rho_Lambda/event -> a0 ~ sqrt(rho_DE), constant -- the
horizon revision.)

This sharpens the prefactor problem into a clean CONSISTENCY CONDITION between the two independent derivations
of a0:
  cosmology (Friedmann):   a0 = (c/2) sqrt(G rho_Lambda) = c H_L / Z,  Z = 2 sqrt(8pi/3) ~ 5.79
  micro (equipartition + DSSYK freezing):  a0 = c H_L / s,  s = freezing slope = 2 rho(0) * T_dS
=> for the framework to be self-consistent, the DSSYK freezing slope must EQUAL the Friedmann factor:
        s = Z = 2 sqrt(8pi/3).
This is exactly what a real duality should enforce: the DSSYK and the de Sitter it is dual to are the SAME de
Sitter, so its cosmological Friedmann factor and its microscopic central density of states cannot be independent.

THE TEST (proper q-Gaussian rho(0); the one open input is the T_dS <-> DSSYK-energy map):
  Computing the exact normalized q-Gaussian central density rho(0) ~ 0.38-0.40 (per unit E, band edge =
  2/sqrt(1-q)), the condition s = Z forces  T_dS ~ the DSSYK BAND EDGE  (T_dS/band ~ 0.8-2.1 over q in
  [0.7, 0.95], ~1.2 near q~0.9). And "T_dS at the band edge / the whole spectrum thermal" is PRECISELY the
  Narovlansky-Verlinde regime -- de Sitter = DSSYK at INFINITE (Boltzmann) temperature. So the consistency
  condition lands in exactly the de Sitter dictionary the framework already uses: a non-trivial, mild POSITIVE.

HONEST LIMITS (loud): this is COMPATIBILITY, not closure. T_dS/band ~ 1 is the right order, but (a) the exact
factor and q still need the precise T_dS<->E map (the unsettled center-vs-edge question), and (b) the rho(0)
normalization here is rough. So it is NOT a proof that DSSYK delivers 2 sqrt(8pi/3) -- it is a precise, well-
posed consistency condition that the leading dictionary roughly satisfies. The prefactor problem is now: does
the exact Narovlansky-Verlinde T_dS<->E map give T_dS/band = the value that makes s = 2 sqrt(8pi/3)? A sharp,
specialist question -- not a free parameter, not yet closed. Needs numpy.
"""
import numpy as np

Zf = 2*np.sqrt(8*np.pi/3)


def rho0_qgauss(q, K=4000):
    qq = np.prod(1 - q**np.arange(1, K))
    prod = np.prod((1 + q**np.arange(0, K))**2)
    return qq/(2*np.pi)*prod*np.sqrt(1-q)/2     # density per unit E (band edge = 2/sqrt(1-q))


def main():
    print("#"*92)
    print("# Prefactor consistency: Friedmann factor =? DSSYK central DOS -- lands in the N-V de Sitter regime")
    print("#"*92 + "\n")

    print("="*92); print("(1) Carl's identity: the two a0 forms are ONE equation; Z is Friedmann"); print("="*92)
    c = 2.998e8; G = 6.674e-11; H0 = 67e3/3.086e22
    rho_crit = 3*H0**2/(8*np.pi*G)
    lhs = (c/2)*np.sqrt(G*rho_crit); rhs = c*H0/Zf
    print(f"  (c/2)sqrt(G rho_crit) = {lhs:.4e};  cH0/Z = {rhs:.4e};  ratio = {lhs/rhs:.6f}")
    print(f"  => Z = 2 sqrt(8pi/3) = {Zf:.4f} IS the Friedmann conversion sqrt(G rho_crit)<->H. Not a free number.\n")

    print("="*92); print("(2) The consistency condition: s (DSSYK freezing slope) = Z (Friedmann factor)"); print("="*92)
    print("""  cosmology: a0 = (c/2)sqrt(G rho_L) = c H_L/Z.   micro: a0 = c H_L/s, s = 2 rho(0) T_dS.
  Same de Sitter on both sides => s must equal Z = 2 sqrt(8pi/3). A duality consistency, not a coincidence.\n""")

    print("="*92); print("(3) THE TEST -- the condition forces T_dS ~ the DSSYK band edge (the N-V regime)"); print("="*92)
    print(f"  {'q':>6}{'rho(0)':>10}{'band=2/sqrt(1-q)':>18}{'T_dS for s=Z':>15}{'T_dS/band':>11}")
    for q in (0.70, 0.80, 0.85, 0.90, 0.95):
        r0 = rho0_qgauss(q); band = 2/np.sqrt(1-q); TdS = Zf/(2*r0)
        print(f"  {q:>6.2f}{r0:>10.4f}{band:>18.2f}{TdS:>15.2f}{TdS/band:>11.2f}")
    print("""  => s = Z requires T_dS ~ the band edge (ratio ~1, ~1.2 near q~0.9). "T_dS at the spectral scale / whole
     band thermal" IS the Narovlansky-Verlinde infinite-temperature de Sitter regime. The consistency condition
     lands in exactly the dictionary the framework uses -- a non-trivial, mild POSITIVE.\n""")

    print("="*92); print("VERDICT -- compatible, not closed"); print("="*92)
    print("""  Carl's identity demystifies Z (it is Friedmann) and turns the prefactor into a clean consistency
  condition: the DSSYK freezing slope s = 2 rho(0) T_dS must equal the Friedmann factor Z = 2 sqrt(8pi/3) --
  which a genuine DSSYK = de Sitter duality should enforce (same de Sitter, so its Friedmann factor and its
  central density of states are not independent). The proper q-Gaussian rho(0) ~ 0.39 makes this condition
  require T_dS ~ the DSSYK band edge, i.e. de Sitter at infinite Boltzmann temperature -- PRECISELY the
  Narovlansky-Verlinde regime. So the cosmology side and the microscopic side match in the right regime: a
  mild positive for the whole construction. HONEST: not a closure -- T_dS/band ~ 1 is the right order but the
  exact value (and q) need the precise N-V energy map, and the rho(0) normalization here is rough. The prefactor
  is now a single specialist question -- "does the exact N-V T_dS<->E map make s = 2 sqrt(8pi/3)?" -- a sharp,
  well-posed condition the leading dictionary roughly satisfies, not a free O(1) and not yet a proof.""")
    print("="*92)


if __name__ == "__main__":
    main()
