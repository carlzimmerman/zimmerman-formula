#!/usr/bin/env python3
"""
WHERE DOES THE 4 COME FROM?  Dissecting 32pi = 4 x 8pi in a0 = c^2 sqrt(Lambda/32pi).
=====================================================================================
Substituting rho_Lambda = Lambda c^2/(8 pi G) (Einstein) collapses the formula to
        a0 = (c/2) sqrt(G rho_Lambda) = c^2 / (2 L_Lambda),   L_Lambda = c / sqrt(G rho_Lambda).
So:
  * the 8pi is FORCED -- it is Einstein's coupling converting the geometric Lambda into the gravitating density.
  * sqrt(G rho_Lambda) is the vacuum's intrinsic gravitational frequency omega_Lambda (treating dark energy as a
    gravitating fluid) -- the physically-motivated skeleton.
  * the ENTIRE '4' is (1/2)^2, the prefactor kappa in  a0 = kappa * c * sqrt(G rho_Lambda),  with kappa = 1/2.

The whole question is therefore: is kappa = 1/2 legit, logical, and forced? We enumerate the clean physical readings
of kappa, compute the dimensionless Z = cH_Lambda/a0 = sqrt(8pi/3)/kappa each predicts, and check the DATA-allowed
band on kappa. Reproducible: `python factor_of_four.py`. Needs numpy.
"""
import numpy as np

C = 2.99792458e8; G = 6.674e-11; MPC = 3.0857e22
H0 = 67.4e3 / MPC; OmL = 0.685
LAM = 3 * OmL * H0**2 / C**2
RHO_L = LAM * C**2 / (8 * np.pi * G)          # vacuum energy density (kg/m^3)
OMEGA_L = np.sqrt(G * RHO_L)                   # vacuum gravitational frequency sqrt(G rho_Lambda)
H_LAM = C * np.sqrt(LAM / 3)                   # de Sitter rate; note H_Lambda = sqrt(8pi/3) * omega_Lambda
A0 = C**2 * np.sqrt(LAM / (32 * np.pi))        # framework a0
L_LAM = C / OMEGA_L                            # vacuum gravitational length
TAU_L = 1.0 / OMEGA_L                          # vacuum gravitational time
Gyr = 3.156e16


def a0_from_kappa(kappa):
    return kappa * C * OMEGA_L
def Z_from_kappa(kappa):
    return C * H_LAM / a0_from_kappa(kappa)    # = sqrt(8pi/3)/kappa


def main():
    print("#" * 100)
    print("# WHERE DOES THE 4 COME FROM?  a0 = (c/2) sqrt(G rho_Lambda) = c^2/(2 L_Lambda);  4 = (1/2)^2")
    print("#" * 100 + "\n")
    print(f"  rho_Lambda     = {RHO_L:.3e} kg/m^3   (~{RHO_L/1.67e-27:.1f} H-atoms/m^3, the dark-energy density)")
    print(f"  omega_Lambda   = sqrt(G rho_Lambda) = {OMEGA_L:.3e} /s   (tau = 1/omega = {TAU_L/Gyr:.0f} Gyr)")
    print(f"  L_Lambda       = c/omega_Lambda     = {L_LAM:.3e} m   (~{L_LAM/(C*Gyr*1e9/1e9):.0f} Gly)")
    print(f"  H_Lambda       = sqrt(8pi/3)*omega  = {H_LAM:.3e} /s   (so the 8pi/3 lives in H, not in a0)")
    print(f"  framework a0   = (c/2) omega_Lambda = {A0:.3e} m/s^2\n")

    # exact identities that fix the meaning of the 1/2
    print("=" * 100)
    print("(1) the 1/2 in three exactly-equivalent, physical statements")
    print("=" * 100)
    print(f"   a0 * tau_Lambda = {A0*TAU_L/C:.3f} c   ->  a0 reaches c/2 in one vacuum gravitational time 1/sqrt(G rho_L).")
    print(f"   a0 = c^2/(2 L_Lambda)              ->  a0 is the SURFACE-GRAVITY of the vacuum length L_Lambda (the universal 1/2).")
    print(f"   a0 = (1/2) c omega_Lambda          ->  half the 'vacuum light-frequency' product c*omega.")
    print("   The 1/2 is the standard free-fall / surface-gravity prefactor; equivalently the '4' can be read as the")
    print("   Bekenstein-Hawking 1/4 if a0 emerges from de Sitter horizon entropy (S=A/4) -- same number, deeper story.\n")

    # candidate readings of kappa
    print("=" * 100)
    print("(2) clean physical readings of the prefactor kappa in a0 = kappa * c * sqrt(G rho_Lambda)")
    print("=" * 100)
    readings = [
        ("FRAMEWORK: free-fall / surface-gravity 1/2", 0.5,            "a0=c^2/2L; reaches c/2 in a vacuum time"),
        ("no prefactor (kappa=1)",                     1.0,            "the bare a0 = c sqrt(G rho_L) -- EXCLUDED"),
        ("Jeans scale  a0 = c^2/lambda_J",             1/np.sqrt(np.pi), "lambda_J = c sqrt(pi/G rho) -> kappa=1/sqrt(pi)"),
        ("thermal 2pi (Marongwe-Kauffman a0=cH_L/2pi)", None,         "a0=c H_Lambda/2pi -> kappa=sqrt(6)/(3 sqrt(pi)), Z=2pi"),
    ]
    print(f"   {'reading':<46}{'kappa':>8}{'-> Z':>8}{'a0 [m/s^2]':>14}   note")
    A0_TH = C * H_LAM / (2 * np.pi)               # thermal a0 with the PURE-Lambda de Sitter rate H_Lambda (consistent w/ kappa def)
    for name, kap, note in readings:
        if kap is None:
            kap = A0_TH / (C * OMEGA_L); a0v = A0_TH
        else:
            a0v = a0_from_kappa(kap)
        print(f"   {name:<46}{kap:>8.3f}{Z_from_kappa(kap):>8.2f}{a0v:>14.2e}   {note}")
    A0_MK_H0 = C * H0 / (2 * np.pi)               # reference only: SAME formula with the MEASURED H0 (full LCDM) -> different footing
    print(f"   {'  [ref] same formula with measured H0 (full LCDM)':<46}"
          f"{A0_MK_H0/(C*OMEGA_L):>8.3f}{C*H_LAM/A0_MK_H0:>8.2f}{A0_MK_H0:>14.2e}   a0=cH0/2pi (the value MK actually quote)")
    print()

    # data band on kappa
    print("=" * 100)
    print("(3) what kappa does the DATA allow? (a0 measured within the interpolating-function systematic)")
    print("=" * 100)
    for lab, a0o in [("simple-mu best fit", 9.1e-11), ("McGaugh RAR", 1.20e-10),
                     ("low a0 edge", 9.0e-11), ("high a0 edge", 1.30e-10)]:
        print(f"   {lab:<22} a0={a0o:.2e}  ->  kappa={a0o/(C*OMEGA_L):.3f}   Z={C*H_LAM/a0o:.2f}")
    klo, khi = 9.0e-11 / (C * OMEGA_L), 1.30e-10 / (C * OMEGA_L)
    print(f"\n   DATA-ALLOWED BAND: kappa in [{klo:.2f}, {khi:.2f}].")
    print(f"   -> EXCLUDES kappa=1 (no prefactor). INCLUDES 1/2={0.5:.2f} (low edge, matches simple-mu)")
    print(f"      and 1/sqrt(pi)={1/np.sqrt(np.pi):.2f} (central); the consistent thermal {A0_TH/(C*OMEGA_L):.2f} sits just below the band.\n")

    print("=" * 100)
    print("(4) VERDICT -- is the 4 legit, logical, explainable?")
    print("=" * 100)
    print(f"""   LEGIT:       Yes. The 4 is NOT arbitrary -- it is (1/2)^2 from a0=(c/2)sqrt(G rho_L), and the DATA REQUIRES a
                prefactor near 1/2 (it excludes the no-prefactor value kappa=1, where a0 would be {a0_from_kappa(1):.1e},
                ~2x too large). So a factor of order 4 must be there; it is data-confirmed, not invented.
   LOGICAL:     Yes. The 1/2 is the universal free-fall / surface-gravity prefactor: a0 = c^2/(2 L_Lambda), the
                'surface gravity' of the vacuum gravitational length L_Lambda = c/sqrt(G rho_Lambda); equivalently
                a0 brings a particle to c/2 in one vacuum free-fall time. (Or, holographically, the 4 is the
                Bekenstein-Hawking 1/4 of the de Sitter horizon entropy -- the same number with a deeper origin.)
   FORCED?:     Not uniquely, at the ~10% level. kappa=1/2 sits at the LOW edge of the data band [{klo:.2f},{khi:.2f}];
                the central value mildly prefers kappa~0.56 (the Jeans 1/sqrt(pi)=0.56); the thermal 2pi reading, taken
                consistently with H_Lambda, instead lands at kappa=sqrt(6)/(3 sqrt(pi))~0.46 (Z=2pi), just below the band.
                These differ from 1/2 by <~15%, below the interpolating-function systematic, so the data cannot
                separate them. Pinning the 4 EXACTLY requires committing to a specific covariant theory: AeST fixes it
                through the normalization of its free function C(Q) (currently inserted), and Marongwe-Kauffman's
                quantum gravity forces the thermal 2pi instead. THAT choice is the genuine open frontier.
   BOTTOM LINE: the 4 = (1/2)^2 is a legitimate, explainable free-fall/Bekenstein-Hawking prefactor, data-selected to
                be ~1/2 -- well-motivated and not numerology -- but its last ~10-15% (exactly 4 vs ~3.3) awaits a
                first-principles dynamical normalization, and it cancels entirely in the coefficient-free bridge.""")
    print("#" * 100)


if __name__ == "__main__":
    main()
