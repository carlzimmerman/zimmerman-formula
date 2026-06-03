#!/usr/bin/env python3
"""
PROJECT 1 (the prize): derive the deep-MOND SIGN from a defensible entropy/DOF correction.
==========================================================================================
The central open problem. MOND needs gravity ENHANCED at low acceleration. This file establishes, with
calculation: (i) the SIGN condition is DOF-FREEZING (not temperature, not a naive entropy power-law);
(ii) freezing gives the deep-MOND sqrt-law AND a0~cH once the freezing scale is the de Sitter
temperature; (iii) the freezing MECHANISM is standard quantum statistics, but the SPECTRUM is posited;
(iv) the precise, unsolved sub-problem that would make it a derivation. No claim that it is solved -- it
is ADVANCED to a sharp demand. Needs numpy + scipy.
"""
import numpy as np
from scipy import integrate

c, G, hbar, kB, Mpc = 2.99792458e8, 6.674e-11, 1.0546e-34, 1.381e-23, 3.0857e22
H0 = 67.4e3/Mpc
a0 = 1.2e-10


def part1_sign():
    print("="*92); print("PART 1 -- the SIGN condition: which modification ENHANCES gravity at low a?"); print("="*92)
    print("""  Holographic screen, bits N = A c^3/(G hbar) = 4S, equipartition Mc^2 = 1/2 N_eff kB T, Unruh
  kB T = hbar a/2pi c. Three modifications, three signs:
    (A) full equipartition  N_eff=N            -> a = GM/r^2                  NEWTON
    (B) DOF FREEZING        N_eff=N(a/a0), a<a0 -> a = sqrt(a0 g_N)            MOND  (enhanced)  <- right
    (C) TEMPERATURE  T->sqrt(a^2+(cH)^2)/2pi in dQ=TdS -> G_eff=G/W->0         ANTI-MOND (clausius_sign)""")
    print("  Sign check of (B), a=sqrt(a0 g_N) vs g_N:")
    for gN in (1e-9, 1e-10, 1e-11):
        print(f"     g_N={gN:.0e}: a={np.sqrt(a0*gN):.2e}  enhanced={np.sqrt(a0*gN) > gN}")
    print("""  => freezing OUT degrees of freedom at low a raises the temperature (hence acceleration) needed to
     hold the energy -> ENHANCED gravity. The deep-MOND sign is DOF-FREEZING. Verified, and it is the
     OPPOSITE of the temperature route. This is the one robust handle on the sign.\n""")


def part2_interpolation_and_scale():
    print("="*92); print("PART 2 -- the full freezing -> the interpolation and a0 = cH"); print("="*92)
    # Debye energy fraction D(x) = (3/x^3) int_0^x t^3/(e^t-1) dt ; x = T_D/T. N_eff/N = D(T_D/T).
    def Debye(x):
        if x < 1e-6: return 1.0
        val, _ = integrate.quad(lambda t: t**3/(np.expm1(t)), 0, x)
        return 3*val/x**3
    TdS = hbar*H0/(2*np.pi*kB)
    a_TD = 2*np.pi*c*kB*TdS/hbar      # acceleration whose Unruh T = T_dS  -> = cH0
    print(f"  Debye temperature = de Sitter temperature T_dS = {TdS:.2e} K  <=>  a0_scale = cH0 = {a_TD:.2e} m/s^2.")
    print(f"  The energy-storing fraction N_eff/N = Debye(T_dS/T(a)) interpolates Newton<->MOND:")
    print(f"     {'a/cH0':>8}{'N_eff/N':>10}{'regime':>14}")
    for r in (10, 1, 0.1, 0.01):
        a = r*c*H0; Ta = hbar*a/(2*np.pi*c*kB); f = Debye(TdS/Ta)
        reg = "Newton" if f > 0.9 else ("transition" if f > 0.2 else "deep MOND")
        print(f"     {r:>8.2f}{f:>10.3f}{reg:>14}")
    print(f"""  => above a0~cH all bits are excited (N_eff~N) -> Newton; below, they freeze (N_eff<N) -> the
     boost a=sqrt(a0 g_N). BOTH the sign and the scale a0~cH come out, the latter forced by T_D=T_dS.
     (The simple linear freezing N_eff/N = a/a0 reproduces the exact sqrt-law; Debye is the smooth version.)\n""")


def part3_defensibility():
    print("="*92); print("PART 3 -- DEFENSIBILITY: what is standard, what is posited"); print("="*92)
    print("""  STANDARD (not in question):
    * low-temperature freezing of an oscillator bath (heat capacity -> 0 as T->0) is textbook quantum
      statistics -- the SAME physics as a solid's Debye specific heat;
    * the de Sitter horizon HAS a temperature T_dS = hbar H/2pi kB (Gibbons-Hawking, established).
  POSITED (the gap):
    * that the horizon's holographic DOF form an oscillator bath with a DEBYE-LIKE spectrum (a frequency
      cutoff), rather than some other density of states;
    * that the cutoff (Debye temperature) EQUALS T_dS exactly -- this is what pins a0 = cH (vs 2cH, cH/2pi).
  So the deep-MOND sign is OBTAINED from standard statistics APPLIED TO A POSITED SPECTRUM. The mechanism
  is real; the spectrum is the assumption. This is exactly why the problem is 'open' and not 'solved'.\n""")


def part4_open_subproblem():
    print("="*92); print("PART 4 -- the PRECISE open sub-problem (what would make it a derivation)"); print("="*92)
    print("""  DERIVE the horizon DOF spectrum from de Sitter quantum field theory. Concretely: compute the
  DENSITY OF STATES of fields in the de Sitter static patch near the horizon ('t Hooft brick-wall /
  horizon-atmosphere method), and show that (a) it has a low-frequency cutoff that freezes the response
  below T_dS, and (b) the cutoff is T_dS itself (not a free scale). If the Bunch-Davies mode structure
  yields exactly that, the freezing -- and hence the deep-MOND sign AND a0=cH -- becomes a DERIVATION
  rather than a posit. This is a bounded, hard, unsolved calculation in QFT-in-curved-spacetime; it is
  the single concrete thing that would close Project 1. No one has done it. It is the right target.\n""")


def part5_alternatives():
    print("="*92); print("PART 5 -- the alternative route (modified entropy S(A)) -- phenomenological"); print("="*92)
    print("""  Instead of freezing the DOF, one can modify the entropy-area law S(A) directly: Barrow
  S~A^(1+Delta/2), Tsallis S~A^delta, Kaniadakis S~sinh-type. The 2024-2025 entropic-MOND papers fit the
  MOND interpolation this way. BUT: (i) the power (Delta, delta) is FITTED to the data, not derived;
  (ii) the SIGN is convention-sensitive (whether N=4S or N=A/lP^2 is held fixed) -- a subtlety the
  literature does not cleanly resolve; (iii) none of Barrow/Tsallis/Kaniadakis is derived from QG (Barrow
  himself called his a toy fractal-horizon model). So this route REACHES MOND but is phenomenological --
  it does not beat the freezing route on defensibility, and it adds a sign ambiguity. The freezing route
  (Part 1-4), with its standard mechanism and one sharp posited spectrum, is the cleaner target.\n""")


def verdict():
    print("="*92); print("PROJECT 1 VERDICT"); print("="*92)
    print("""  The deep-MOND SIGN is OBTAINABLE and the SCALE is FORCED -- but it is not yet DERIVED:
    * the sign is DOF-FREEZING (verified; the opposite of the temperature route);
    * freezing gives the sqrt-law and a0~cH once the freezing scale = T_dS;
    * the freezing MECHANISM is standard quantum statistics; the SPECTRUM (Debye + T_D=T_dS) is posited;
    * the precise, bounded, unsolved demand that would make it a derivation: compute the de Sitter
      horizon density of states and show it freezes at exactly T_dS ('t Hooft brick-wall in de Sitter).
  Net: Project 1 is not solved, but it is sharpened from 'why does MOND have its sign?' to one concrete
  QFT-in-de-Sitter calculation. That is real progress on the prize, with no fabricated derivation.""")
    print("="*92)


def main():
    print("#"*92); print("# PROJECT 1 -- the deep-MOND sign from a defensible entropy/DOF correction"); print("#"*92 + "\n")
    part1_sign(); part2_interpolation_and_scale(); part3_defensibility(); part4_open_subproblem(); part5_alternatives(); verdict()


if __name__ == "__main__":
    main()
