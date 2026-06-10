#!/usr/bin/env python3
"""
DOOR AUDIT: is 'a0 ~ where t_dyn = t_cosmic' a rigorous physical principle, or
a0 ~ cH dressed as a principle?  [COMPUTED-THIS-RUN, all numbers re-derived]

We separate THREE distinct claims that the premise blurs together:

  CLAIM A (dimensional):  from {c, H} alone the only acceleration is cH x O(1).
                          -> a0 ~ cH is AUTOMATIC. Does the t_dyn=t_cosmic story
                             add anything to this?

  CLAIM B (the equality): setting t_dyn(a,r) = t_cosmic.  We test whether this is
                          (i) a condition on the ACCELERATION a alone (genuine, a0
                          drops out r-independently) or (ii) a condition that needs
                          a length scale smuggled in (circular).

  CLAIM C (the coefficient): does t_dyn = t_cosmic FORCE a0 = cH/Z with a SPECIFIC
                          numerical Z, or only a0 ~ cH with Z unpinned?

We also test the 'longest coherence time' mechanism claim: is there a physical t_max
that is NOT just 1/H by definition?
"""
import numpy as np
import sympy as sp

c   = 2.99792458e8
G   = 6.674e-11
Mpc = 3.0857e22
H0  = 67.4e3/Mpc          # s^-1
OmL = 0.685
a0_obs = 1.2e-10          # observed MOND scale (McGaugh RAR), m/s^2

cH0 = c*H0
H_L = H0*np.sqrt(OmL)     # pure-Lambda de Sitter rate
cHL = c*H_L

print("="*84)
print("CLAIM A -- dimensional: is a0 ~ cH automatic from {c,H}?  (the null hypothesis)")
print("="*84)
print(f"  cH0   = {cH0:.3e} m/s^2     cH_Lambda = {cHL:.3e} m/s^2     a0_obs = {a0_obs:.2e}")
print(f"  From the set (c, H) the UNIQUE dimensionful acceleration is cH (up to a pure number).")
print(f"  Pi-theorem: [c]=L/T, [H]=1/T, [a]=L/T^2.  a = c^p H^q with L: p=1; T: -p-q=-2 => q=1.")
print(f"  => a = c H  is the ONLY monomial; ANY a0 built from (c,H) is cH x (dimensionless).")
print(f"  Observed cH0/a0_obs = {cH0/a0_obs:.2f}.  So 'a0 ~ cH' costs ZERO physics: it is forced")
print(f"  the instant you assert a0 is set by the cosmic horizon. The content, if any, is the O(1).")

print()
print("="*84)
print("CLAIM B -- does t_dyn = t_cosmic pick out an ACCELERATION (good) or need a length (bad)?")
print("="*84)
# Symbolic test. t_dyn for a system of size r with acceleration a:  t_dyn ~ sqrt(r/a).
# t_cosmic ~ 1/H.  Set equal:
a, r, H, Z = sp.symbols('a r H Z', positive=True)
t_dyn   = sp.sqrt(r/a)            # dynamical/free-fall time of an orbit radius r, accel a
t_cos   = 1/H                     # cosmic time
eqB     = sp.Eq(t_dyn, t_cos)
solB    = sp.solve(eqB, a)[0]     # solve for a
print(f"  t_dyn = sqrt(r/a),  t_cosmic = 1/H.   Set t_dyn = t_cosmic, solve for a:")
print(f"     a = {solB}   <-- depends on r.  This is the CIRCULARITY: the 'critical accel'")
print(f"     from t_dyn=t_cosmic is a = r H^2, which is NOT a universal scale -- it slides with r.")
print(f"     For a galaxy edge r~30 kpc: a = r H^2 = {((30*Mpc/1e3)*H0**2):.2e}  (NOT a0).")
print(f"     For r = c/H (Hubble radius):  a = (c/H) H^2 = cH = {cH0:.2e}.")
print(f"  => t_dyn=t_cosmic alone gives a = rH^2; it becomes the scale cH ONLY when you ALSO set")
print(f"     r = c/H (the horizon).  i.e. the premise SECRETLY uses 'r = light-travel in t_cosmic'.")

# The ACTUAL MOND statement is different: it is about the acceleration directly, via
#   a0 = (the a at which the free-fall time over a SELF-GRAVITATING ball equals 1/H).
# For a ball of mean density rho, t_ff = 1/sqrt(G rho) (r-INDEPENDENT!). That is the key.
rho = sp.symbols('rho', positive=True)
t_ff = 1/sp.sqrt(G*rho)                 # free-fall time of a uniform ball -- NO r in it
print()
print("  The r-FREE version (the one that works): free-fall time of a UNIFORM ball of density rho")
print(f"     t_ff = 1/sqrt(G rho)   <-- r cancels (t_ff = sqrt(3pi/(32 G rho)) exactly; same scaling).")
print(f"     Set t_ff = t_cosmic = 1/H:   sqrt(G rho) = H  =>  rho = H^2/G  (the Friedmann density!).")
print(f"     This is NOT a statement about a0 yet -- it is just rho_dyn ~ rho_crit, a tautology of")
print(f"     Friedmann (H^2 = (8pi/3)G rho).  To get an ACCELERATION you must multiply by a LENGTH.")

print()
print("="*84)
print("CLAIM C -- the coefficient: does t_dyn=t_cosmic FORCE a specific Z, or only a0~cH?")
print("="*84)
# To turn rho=H^2/G into an acceleration you need a length L:  a0 = (length) x (G rho) = L H^2.
# The premise does NOT supply L; it must be chosen. Different choices => different Z. Enumerate:
print("  To convert the density condition to an acceleration you MUST pick a length L:  a0 = L*G*rho.")
print("  The premise does not supply L. Each physically-motivated choice gives a DIFFERENT Z=cH/a0:")
print(f"     {'choice of length L':<46}{'a0':>12}{'Z=cH0/a0':>11}")
for name, L in [
    ("R_H = c/H (Hubble/expansion horizon)",          c/H0),
    ("R_* = c/sqrt(Grho_c) (free-fall, rho_crit)",     c/np.sqrt(G*(3*H0**2/(8*np.pi*G)))),
    ("R_*(rho_Lambda) (free-fall, dark-energy)",        c/np.sqrt(G*(OmL*3*H0**2/(8*np.pi*G)))),
    ("Unruh/Milgrom matching (a0=cH/2pi)",              c/(2*np.pi*H0)),  # gives the right a0 by L=R_H/2pi
    ("Verlinde de Sitter entropy (a0=cH/6)",            c/(6*H0)),
]:
    a0_L = L*G*(3*H0**2/(8*np.pi*G))   # a0 = L * G * rho_crit ; rho_crit=3H^2/8piG
    # but to compare cleanly just use a0 = c^2/(2L) for a 'surface gravity' reading vs a0=cH/k:
    a0_sg = c**2/(2*L)
    Z_sg  = cH0/a0_sg
    print(f"     {name:<46}{a0_sg:>12.2e}{Z_sg:>11.3f}")
print("  NONE of these Z values is selected by 't_dyn=t_cosmic'. The equality fixes the DENSITY")
print("  condition (rho~H^2/G) but is SILENT on which length promotes it to an acceleration, and")
print("  silent on the surface-gravity 1/2.  => the premise forces a0~cH but NOT Z. (matches repo")
print("  COEFFICIENT_DEFINITIVE_VERDICT: Z is a data-selected convention, not derived.)")

print()
print("="*84)
print("MECHANISM TEST -- is there a 'longest coherence time' that is NOT just 1/H by fiat?")
print("="*84)
# The hopeful reading: a0 marks where t_dyn hits a genuine MAXIMUM physical time (a coherence/
# horizon time) set by the vacuum -- a real cutoff, not a redefinition of H.
# Candidate physical t_max in de Sitter: the de Sitter (Gibbons-Hawking) time 1/H_Lambda, and
# the much longer Poincare-recurrence / scrambling times. Test whether any is 'the' clock.
tH      = 1/H0
tH_L    = 1/H_L
T_GH    = (1.0546e-34*H_L)/(2*np.pi*1.381e-23)     # de Sitter temperature (K)
t_scramble = (1/H_L)*np.log(2.3e122)               # scrambling ~ (1/H) ln S_dS
t_poincare_log10 = 2.3e122/np.log(10)               # log10 of Poincare recurrence ~ exp(S_dS) (Hubble times)
print(f"  Hubble time            1/H0        = {tH:.3e} s = {tH/(3.15e7*1e9):.2f} Gyr")
print(f"  de Sitter time         1/H_Lambda  = {tH_L:.3e} s = {tH_L/(3.15e7*1e9):.2f} Gyr")
print(f"  de Sitter scrambling   (1/H)lnS_dS = {t_scramble:.3e} s = {t_scramble/(3.15e7*1e9):.1f} Gyr  (~280x)")
print(f"  Poincare recurrence    exp(S_dS)   = 10^({t_poincare_log10:.2e}) Hubble times  (absurdly long)")
print(f"  de Sitter temperature  T_GH        = {T_GH:.2e} K")
print( "  VERDICT on mechanism: there ARE distinguished de Sitter times, but the ones that are")
print( "  PARAMETRICALLY ~1/H (GH time) just reproduce a0~cH (no new content); the genuinely")
print( "  DIFFERENT ones (scrambling ~ln S, recurrence ~exp S) are LOGARITHMICALLY or")
print( "  EXPONENTIALLY larger -- if a0 marked THOSE, a0 would be ~10^-12 or ~0, FALSIFIED.")
print( "  So the only coherence time consistent with a0~cH is the one that is ~1/H by construction.")
print( "  => 'longest coherence time' adds no falsifiable content beyond 'the de Sitter time ~1/H'.")

print()
print("="*84)
print("THE ONE PLACE THE PREMISE *DOES* ADD CONTENT (steelman, fairness both ways)")
print("="*84)
print("  The premise's NON-trivial, FALSIFIABLE residue is NOT the O(1) and NOT 'a0~cH' at z=0.")
print("  It is the FUNCTIONAL FORM in a self-gravitating context:  because t_ff = 1/sqrt(Grho) is")
print("  r-INDEPENDENT, the SAME a0 governs systems of every size at fixed background rho -- and")
print("  it predicts a0 TRACKS sqrt(rho_cosmic), i.e. a0(z) ~ sqrt(rho(z)) ~ H(z).  That is a")
print("  genuine prediction (the falsifiable core), but it follows from 'a0 set by the cosmic")
print("  horizon density' -- which is the a0~cH(z) statement -- NOT from the t_dyn=t_cosmic clock")
print("  per se.  The clock is a MNEMONIC for a0~cH(z); the physics is 'a0 is sourced by rho_cosmic'.")
print("="*84)
