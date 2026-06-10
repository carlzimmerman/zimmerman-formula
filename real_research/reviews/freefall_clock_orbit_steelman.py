#!/usr/bin/env python3
"""
STEELMAN of the free-fall clock: the ORBITAL form of 't_dyn = t_cosmic'.
========================================================================
[COMPUTED-THIS-RUN]. The previous audit used t_dyn=sqrt(r/a) and showed a=rH^2 (r-dependent).
A defender will say: the RIGHT MOND statement is about a single orbiting test particle, where
t_dyn and a are linked through the SAME orbit, so a IS pinned. Test that fairly, then ask the
only question that matters for the DOOR: does the orbital equality ADD content beyond a0~cH,
and does it FORCE the coefficient Z?

Milgrom's actual heuristic (Milgrom 1983, 1999, 2014):
   For a circular orbit:  a = v^2/r  and  t_dyn = 2 pi r / v  (the orbital period).
   Eliminate v:  v = sqrt(a r),  so  t_dyn = 2 pi sqrt(r/a).
   The 'a0' is where the orbital time at the DEEP-MOND boundary equals the cosmic time 1/H.
   But r is still free -> we need ONE more relation. The honest MOND closure is:
   in deep MOND v is r-INDEPENDENT (flat curve), v^4 = G M a0, so pick the characteristic
   radius where the system transitions: g_N(r_t) = a0 => r_t = sqrt(GM/a0). Plug in.
"""
import numpy as np

c, G, Mpc = 2.99792458e8, 6.674e-11, 3.0857e22
H0 = 67.4e3/Mpc
OmL = 0.685
H_L = H0*np.sqrt(OmL)
cH0, cHL = c*H0, c*H_L
a0_obs = 1.2e-10

print("="*84)
print("STEELMAN 1 -- does the orbital t_dyn=t_cosmic at the MOND radius pin a0, or stay ~cH?")
print("="*84)
# At the transition radius r_t where g_N = a0:  a = a0, v = sqrt(a0 r_t), t_dyn = 2pi sqrt(r_t/a0).
# r_t depends on M, so t_dyn at the knee is MASS-DEPENDENT -> it is NOT universally 1/H.
print("  At the transition radius r_t (g_N=a0): t_dyn = 2pi sqrt(r_t/a0), and r_t=sqrt(GM/a0).")
print("  => t_dyn(knee) = 2pi (GM)^(1/4) a0^(-3/4)  -- depends on M. NOT a universal cosmic time.")
print(f"     {'galaxy M [Msun]':>16}{'r_t [kpc]':>12}{'t_dyn(knee)/t_H':>18}")
for Msun_n in (1e9, 1e10, 1e11, 1e12):
    M = Msun_n*1.989e30
    r_t = np.sqrt(G*M/a0_obs)
    t_dyn = 2*np.pi*np.sqrt(r_t/a0_obs)
    print(f"     {Msun_n:>16.0e}{r_t/(Mpc/1e3):>12.1f}{t_dyn/(1/H0):>18.3f}")
print("  VERDICT: t_dyn at the MOND knee ranges over DECADES across galaxy masses; it is NOT ~1/H")
print("  for any but a single special mass. So 't_dyn=t_cosmic' is NOT a property of the knee of a")
print("  given galaxy. The equality only holds GLOBALLY -- for the whole observable universe as one")
print("  'orbit' (r~c/H, a~cH). That GLOBAL reading is exactly a0~cH again. No new content, no Z.")

print()
print("="*84)
print("STEELMAN 2 -- the deep-MOND-only reading: a0 = where the orbital freq omega hits H")
print("="*84)
# Another defender move: in deep MOND, the orbital frequency omega = v/r = sqrt(a/r)*... actually
# omega = v/r and v=const => omega = v/r DECREASES with r. The LONGEST orbital period (smallest
# omega) at the system's edge R_edge sets a 'slowest clock'. Set omega_min = H.
# omega = sqrt(a0/r)*(g_N/a0)^? ... in deep MOND a=sqrt(a0 g_N), v=(GM a0)^1/4, omega=v/r.
# omega -> H at r_H = v/H = (GMa0)^(1/4)/H. Is the IMPLIED a there ~a0? Check self-consistency:
print("  Deep-MOND: v_flat=(G M a0)^(1/4); orbital omega=v/r falls as 1/r; set omega=H at r_H=v/H.")
print("  The acceleration at that radius is a(r_H)=v^2/r_H = v H. For this to be ~a0 we need vH~a0")
print(f"     {'galaxy M':>12}{'v_flat[km/s]':>14}{'a(omega=H)=vH':>16}{'/a0_obs':>10}")
for Msun_n in (1e9, 1e10, 1e11, 1e12):
    M = Msun_n*1.989e30
    v = (G*M*a0_obs)**0.25
    a_at = v*H0
    print(f"     {Msun_n:>12.0e}{v/1e3:>14.0f}{a_at:>16.2e}{a_at/a0_obs:>10.3f}")
print("  VERDICT: a(omega=H) = v_flat*H is ~1e-13 to 1e-12, i.e. 0.001-0.05 x a0 -- it is NOT a0,")
print("  and it slides with mass. So 'where the orbital clock equals the cosmic clock' is NOT the")
print("  MOND scale either. The MOND transition (g~a0) and the cosmic-clock crossing (omega~H) are")
print("  DIFFERENT, mass-dependent radii. The premise's identification of them is only ORDER-OF-")
print("  MAGNITUDE and only for the whole horizon -- once more just a0~cH.")

print()
print("="*84)
print("THE DECISIVE LOGICAL TEST -- does t_dyn=t_cosmic => a0=cH/Z, or is it the CONVERSE?")
print("="*84)
print("  Forward question: assume ONLY 'the longest dynamical time a bound system can have is the")
print("  cosmic time t_cosmic ~ 1/H'. Derive a0.")
print("  - t_dyn for a self-gravitating system of mean density rho is t_dyn ~ 1/sqrt(G rho)")
print("    (r-free). t_dyn maximal => rho minimal => rho_min ~ H^2/G (can't be less dense than the")
print("    background and stay bound). So the FAINTEST bound systems have rho ~ rho_crit, t_dyn~1/H.")
print("  - The acceleration internal to such a system: a ~ G rho * r = (H^2) * r. STILL needs r.")
print("    The system's OWN size r is set by its mass: r ~ (M/rho)^(1/3). So a ~ H^2 (M/rho)^(1/3),")
print("    mass-dependent again -- NOT a universal a0.")
print("  CONCLUSION: 't_dyn=t_cosmic' constrains the DENSITY (rho~rho_crit) of the faintest bound")
print("  systems -- a real, correct statement (LSB galaxies sit near rho_crit). But DENSITY is not")
print("  ACCELERATION; the step to a UNIVERSAL a0 needs an extra ingredient (a fixed length, or the")
print("  surface-gravity-of-a-horizon posit) that t_dyn=t_cosmic does NOT supply. Hence:")
print()
print("  *** t_dyn=t_cosmic FORCES a0~cH (via rho~H^2/G + ONE length~c/H), but does NOT force the")
print("      coefficient Z, and does NOT by itself yield a universal acceleration without importing")
print("      the horizon length. It is a0~cH with a physical GLOSS, not a derivation of a0=cH/5.789. ***")

print()
print("="*84)
print("WHAT WOULD MAKE IT MORE THAN a0~cH (the bar, stated so it is fair)")
print("="*84)
print("  The premise would EARN content beyond a0~cH iff EITHER:")
print("   (1) a mechanism FORCES the specific length L=R_*=c/sqrt(Grho) AND the 1/2 (=> Z=2sqrt(8pi/3)),")
print("       distinguishing 5.789 from 2pi/6 by physics, not data. The repo's own COEFFICIENT verdict")
print("       (number-field no-go; Ybar=0 saddle-blindness) says this FAILS in the modified-GRAVITY route.")
print("   (2) the 'longest coherence time' is a SEPARATE physical scale (not 1/H by definition) that")
print("       happens to equal 1/H -- a coincidence to be explained. The de Sitter times that differ")
print("       from 1/H (scrambling ln S, recurrence exp S) give the WRONG a0, so no independent clock")
print("       lands on a0. The only clock that works is 1/H itself => no coincidence to explain, no")
print("       new content.")
print("  Neither holds. => DOOR VERDICT: the free-fall-clock premise is a0~cH dressed as a principle.")
print("  It is PHYSICALLY MOTIVATED and gives the right FORM (incl. the falsifiable a0(z)~sqrt(rho)),")
print("  but it is NOT rigorous as a derivation of the SCALE's coefficient, and the 't_dyn=t_cosmic'")
print("  equality is r/mass-dependent (hence circular) except in the single global horizon reading,")
print("  which is identically a0~cH.")
print("="*84)
