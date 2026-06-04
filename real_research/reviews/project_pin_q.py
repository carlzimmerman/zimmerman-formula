#!/usr/bin/env python3
"""
Pinning q from the de Sitter entropy REFUTES the microscopic coefficient -- Z is not forced from below.
=====================================================================================================
The last knob between "Z conditional" and "Z forced" was the DSSYK coupling q. The framework's coefficient
relation (from the freezing = band-edge consistency, project_the_wall.py) is
        Z = 4 rho0(q) / sqrt(1-q)     [rho0 = q-Gaussian central density of states],
and Z = 2 sqrt(8pi/3) = 5.79 is reproduced at q ~ 0.925. If q could be pinned independently, Z would be forced.
So we pin it -- from the de Sitter entropy, via Narovlansky-Verlinde.

THE PIN. For dS3, S_dS = (horizon length)/4G = pi R_dS/(2 G3), so R_dS/G3 = 2 S_dS/pi. The NV dictionary gives
R_dS/G_N = 4 pi N/p^2, and the double-scaling coupling is lambda = 2 p^2/N (q = e^{-lambda}). Hence
        lambda = 4 pi^2 / S_dS,    q = exp(-4 pi^2 / S_dS).
This is the standard statement that the SEMICLASSICAL (large) de Sitter is the q->1 limit of DSSYK. q is fixed
by the de Sitter entropy.

THE RESULT (a clean refutation). For our de Sitter, S_dS ~ 1e122, so lambda ~ 4e-121 and q = 1 - 4e-121 (i.e.
q->1). In that limit the framework's relation Z = 4 rho0/sqrt(1-q) ~ (2 rho0/pi) sqrt(S_dS) DIVERGES:
        Z ~ 2.5e60,   a0 = cH/Z ~ 2.6e-70 m/s^2     (observed: 1.2e-10) -- off by ~60 orders of magnitude.
The value Z = 5.79 (a0 ~ 1.2e-10) requires S_dS ~ 520 -- a PLANCK-SCALE de Sitter (R_dS ~ 23 l_P), not ours. So
the s = Z match at q ~ 0.925 was a coincidence at an UNPHYSICAL point; pinning q to the ACTUAL de Sitter breaks
the coefficient relation catastrophically.

CONCLUSION. Pinning q does NOT force Z -- it REFUTES the microscopic (DSSYK band-edge) derivation of the
coefficient. Combined with the deep-geometry finding (the simplest horizon criteria give Z = 1 or 2, and matching
the data needs an extra Friedmann factor that is not uniquely fixed), the coefficient Z = 2 sqrt(8pi/3) is
honestly OPEN -- a natural geometric packaging that fits to ~6%, not derived from below from any direction. What
SURVIVES untouched is the q-INDEPENDENT deep-MOND SIGN: the flat-center density of states gives the sqrt-law and
flat rotation curves (project_center_vs_edge.py) for ANY q, and the center is the data-favored reading. So the
SIGN is solid; only the COEFFICIENT's microscopic derivation fails.

(Possible escape, noted but not demonstrated: if the MOND 'freezing' is governed by a local effective scale with
its own effective coupling, rather than the global de Sitter q, the pin would not apply -- but there is one DSSYK
and one q, so this is unmotivated. Or the freezing temperature is not the band edge -- but then the coefficient
has no microscopic mechanism at all.) Needs numpy.
"""
import numpy as np

c = 2.998e8; H0 = 67e3/3.086e22; cH = c*H0
Zf = 2*np.sqrt(8*np.pi/3)


def rho0(q, K=200000):
    """Central density of states of the q-Gaussian, in log space (robust as q->1)."""
    k1 = np.arange(1, K); k0 = np.arange(0, K)
    ln = (np.sum(np.log1p(-q**k1)) + 2*np.sum(np.log1p(q**k0))
          + np.log(np.sqrt(1-q)/2) - np.log(2*np.pi))
    return np.exp(ln)


def main():
    print("#"*92)
    print("# Pinning q from the de Sitter entropy REFUTES the microscopic coefficient (Z not forced)")
    print("#"*92 + "\n")

    print("="*92); print("THE PIN: lambda = 4 pi^2 / S_dS  =>  q = exp(-4 pi^2 / S_dS)  (semiclassical dS = q->1)"); print("="*92)
    r1 = rho0(0.9999)
    print(f"  rho0(q) -> {r1:.4f} as q->1 (finite).  Z ~ (2 rho0/pi) sqrt(S_dS) in that limit.\n")
    print(f"  {'S_dS':>10}{'q':>17}{'Z':>13}{'a0=cH/Z':>13}{'':>3}")
    for SdS in [5.2e2, 1e4, 1e8, 1e40, 1e122]:
        lam = 4*np.pi**2/SdS
        sq = np.sqrt(1-np.exp(-lam)) if lam > 1e-10 else 2*np.pi/np.sqrt(SdS)
        Z = 4*r1/sq; a0 = cH/Z
        tag = "<- OUR universe" if SdS > 1e100 else ("<- observed a0" if SdS < 1e3 else "")
        print(f"  {SdS:>10.1e}{np.exp(-lam):>17.12f}{Z:>13.2e}{a0:>13.2e}  {tag}")
    print()

    print("="*92); print("THE VERDICT"); print("="*92)
    SdS_target = (Zf*np.pi/(2*r1))**2
    print(f"  Z = 2 sqrt(8pi/3) = {Zf:.2f} (a0 ~ 1.2e-10) requires S_dS ~ {SdS_target:.0f}  =>  R_dS ~ {np.sqrt(SdS_target):.0f} l_P (Planck-scale dS).")
    Z_real = (2*r1/np.pi)*np.sqrt(1e122)
    print(f"  OUR de Sitter S_dS ~ 1e122  =>  Z ~ {Z_real:.1e}  =>  a0 ~ {cH/Z_real:.1e}  (observed 1.2e-10; off ~60 orders).")
    print("""
  => Pinning q does NOT force Z; it REFUTES the DSSYK band-edge derivation of the coefficient (our de Sitter is
     q->1, where Z diverges and a0->0). The q ~ 0.925 that gave Z = 5.79 is a Planck-scale de Sitter, not ours;
     the s = Z match was a coincidence at an unphysical point. With the deep-geometry result (simple criteria
     give Z = 1 or 2; the extra Friedmann factor is not uniquely fixed), the COEFFICIENT is honestly OPEN -- a
     natural geometric packaging fitting to ~6%, not derived from below. The q-INDEPENDENT deep-MOND SIGN
     (flat-center DOS -> sqrt-law -> flat rotation curves) is UNTOUCHED and remains the solid microscopic result.""")
    print("="*92)


if __name__ == "__main__":
    main()
