#!/usr/bin/env python3
"""
Does the de Sitter-Unruh route ESCAPE the circularity?  (the strongest version of the door)
==========================================================================================
[COMPUTED-THIS-RUN]. The dimensional/length critique (freefall_clock_*.py) says t_dyn=t_cosmic
needs a length smuggled in. The de Sitter-Unruh modified-inertia route (Milgrom 1999; the repo's
desitter_unruh_mond.py) claims to get a0~cH and the FULL mu(a) WITHOUT positing a length, from
   T(a) = (hbar/2pi kB c) sqrt(a^2 + (cH)^2),   mu(a) = [sqrt(a^2+(cH)^2)-cH]/a.
If true, that route makes 'a0 ~ where the dynamical response meets the cosmic horizon' RIGOROUS
(a real T, not a length-by-hand). Test exactly what it derives and where the coefficient enters.
"""
import numpy as np
c, G, hbar, kB, Mpc = 2.99792458e8, 6.674e-11, 1.0546e-34, 1.381e-23, 3.0857e22
H0 = 67.4e3/Mpc; cH0 = c*H0
a0_obs = 1.2e-10

def mu(a, H):
    cH=c*H; return (np.sqrt(a**2+cH**2)-cH)/a

print("="*84)
print("(1) Does the Unruh route need a LENGTH by hand?  -- NO. It needs a TEMPERATURE FLOOR.")
print("="*84)
print("  The scale enters as the de Sitter temperature floor T(0)=hbar H/2pi kB (a TEMPERATURE,")
print("  derived from the horizon, Gibbons-Hawking 1977). NOT a length chosen by hand. So the")
print("  length-smuggling critique does NOT apply to this route. The a0 emerges as:")
# deep-MOND limit: mu->a/(2cH), so mu*a=g_N => a^2/(2cH)=g_N => a=sqrt(2cH g_N) => a0=2cH.
print(f"     deep limit mu->a/(2cH): a=sqrt(2cH g_N) => a0 = 2cH = {2*cH0:.2e}  (Z=cH0/a0=0.5)")
print(f"  So THIS route DOES yield a coefficient -- Z=1/2 -- without a length posit. Check it vs data:")
print(f"     a0(Unruh, naive DeltaT) = 2cH0 = {2*cH0:.2e}  vs observed {a0_obs:.2e}  => {2*cH0/a0_obs:.1f}x TOO BIG.")

print()
print("="*84)
print("(2) So the Unruh route PINS a coefficient -- but it is the WRONG one (0.5, i.e. a0~10x obs).")
print("="*84)
print("  The honest reading (matches desitter_unruh_mond.py Part 4):")
print("   - naive DeltaT=T(a)-T(0) inertia  => a0 = 2cH,      Z=0.5   (a0 ~ 13e-10, ~11x too big)")
print("   - Milgrom's careful 1999 deep-MOND/Unruh matching => 2pi a0 = cH, Z=2pi (a0~1.0e-10, GOOD)")
print("   - the difference between Z=0.5 and Z=2pi is the 2pi in the Unruh T=hbar a/2pi kB c and the")
print("     details of HOW you define 'the inertia-producing heat' -- i.e. it is STILL an O(1) that")
print("     depends on the (non-rigorous) prescription for mu. The route does not UNIQUELY fix it.")
# show the 2pi matching gives the good value
print(f"     check: a0 = cH0/(2pi) = {cH0/(2*np.pi):.2e}  vs observed {a0_obs:.2e}  => {cH0/(2*np.pi)/a0_obs:.2f}x  (good)")

print()
print("="*84)
print("(3) Is the Unruh T(a)=sqrt(a^2+(cH)^2)/... ITSELF rigorous, or is the quadrature posited?")
print("="*84)
print("  LITERATURE status of T(a)=(hbar/2pi kB c)sqrt(a^2+(cH)^2):")
print("   - Narnhofer-Peter-Thirring (1996) & Deser-Levin (1997): a UNIFORMLY accelerated detector")
print("     in de Sitter DOES see T proportional to sqrt(a^2+(cH)^2)/2pi. [ESTABLISHED, rigorous QFT")
print("     in curved space] -- so the quadrature is NOT posited; it is a theorem for that geometry.")
print("   - BUT: Milgrom's step 'inertia = response to DeltaT=T(a)-T(0)' is a POSTULATE (modified")
print("     inertia), not derived from QFT. And it is time-LOCAL here, whereas Milgrom's own 1994")
print("     theorem says a real modified-inertia MOND must be time-NONLOCAL => this mu(a) is a")
print("     heuristic toy, not the true theory. [ESTABLISHED that it is heuristic.]")

print()
print("="*84)
print("(4) BOTTOM LINE for the DOOR -- does Unruh make t_dyn=t_cosmic rigorous?")
print("="*84)
print("  PARTIAL UPGRADE, not a rescue:")
print("   + It REMOVES the 'length by hand' objection: the scale enters as a DERIVED temperature")
print("     floor (de Sitter T ~ hbar H), and a0 ~ cH falls out of a genuine (NPT/Deser-Levin)")
print("     curved-space QFT result, not a dimensional gloss. To THAT extent the free-fall-clock")
print("     idea has a real mechanism: the cosmic horizon sets a vacuum TEMPERATURE floor, and")
print("     inertia/dynamics referenced to that floor changes near a~cH. That is more than a0~cH.")
print("   - It does NOT fix the coefficient: the SAME route gives Z=0.5 (naive) or Z=2pi (Milgrom")
print("     matching); the value rides on the non-rigorous 'inertia=DeltaT' prescription. So the")
print("     specific Z=5.789 is STILL unforced; in fact the Unruh route doesn't even PREFER 5.789")
print("     (it likes 2pi). Consistent with COEFFICIENT_DEFINITIVE_VERDICT.")
print("   - The underlying mu(a) is a time-LOCAL toy; Milgrom 1994 proves the real thing is time-")
print("     NONLOCAL. So even the mechanism is provisional.")
print()
print("  REFINED DOOR VERDICT: 'a0 ~ where t_dyn=t_cosmic' is NOT merely a0~cH relabeled IF read as")
print("  the de Sitter-Unruh statement 'the cosmic horizon imposes a vacuum temperature floor T~hbarH,")
print("  and dynamics referred to that floor is modified at a~cH'. That has a real (NPT/Deser-Levin)")
print("  mechanism and is a genuine physical principle at the a0~cH level. BUT (a) it FORCES only")
print("  a0~cH, not the coefficient (gives 0.5 or 2pi, not 5.789); (b) the inertia=DeltaT step is a")
print("  heuristic that violates Milgrom's own time-nonlocality theorem; and (c) the naive version is")
print("  ~10x off in value. So: a principle for the SCALE (~cH) with a real horizon mechanism; a")
print("  COINCIDENCE/POSIT for the coefficient. The premise adds MECHANISM beyond 'a0~cH is automatic',")
print("  but adds NO content that pins Z, and t_dyn=t_cosmic per se (the geometric clock) remains the")
print("  r/mass-dependent, hence non-rigorous, way to SAY a0~cH; the rigorous content lives in the")
print("  TEMPERATURE-floor statement, not the clock-equality statement.")
print("="*84)
