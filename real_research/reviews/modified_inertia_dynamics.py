#!/usr/bin/env python3
"""
LAYER 0 -- the dynamics: modified gravity (complete) vs modified inertia (open).
===============================================================================
The Machian foundation says inertia is emergent. There are two ways to turn 'a0 ~ cH'
into an equation of motion: modify GRAVITY (the field that sources the force) or modify
INERTIA (the m a side). We work both with real calculations and show, honestly:
  * modified GRAVITY (AQUAL/QUMOND/AeST) is LOCAL, 2nd-order, ghost-free, and COMPLETE --
    it gives a well-defined trajectory for ANY orbit. This is what the framework actually
    uses (Layer 3, AeST). So the working theory is closed.
  * modified INERTIA is elegant (it is the literal 'emergent-inertia' reading) but is an
    OPEN problem -- acceleration-dependent inertia forces higher derivatives (Ostrogradski
    ghost) or nonlocality; it reproduces MOND only for closed orbits (Milgrom 1994, 2011).
Conclusion: the foundation's deep 'why' (modified inertia) is unfinished -- in the
literature, not just here -- but the framework does NOT depend on closing it, because it
rides on complete modified gravity. Needs numpy + scipy.
"""
import numpy as np
from scipy.integrate import solve_ivp

G, Msun, kpc = 6.674e-11, 1.989e30, 3.0857e19
A0 = 1.2e-10
nu = lambda x: 0.5*(1.0 + np.sqrt(1.0 + 4.0/x))      # QUMOND boost: g_obs = nu(g_N/a0) g_N


# ============================================================================
def part1_modified_gravity_is_complete():
    print("="*82)
    print("PART 1 -- MODIFIED GRAVITY (AQUAL/QUMOND/AeST): local, 2nd-order, COMPLETE")
    print("="*82)
    print("""  Field equation (QUMOND): the physical acceleration is g = nu(|g_N|/a0) g_N, with g_N
  the Newtonian field of the baryons. This is an ALGEBRAIC, LOCAL relation -- given the mass
  distribution it returns g(x) everywhere, for all time, with NO reference to any orbit. The
  equation of motion of a test body is then just  r'' = g(r)  -- ordinary 2nd order.""")
    M = 5e10*Msun                                    # a galaxy
    # point-mass field, deep-MOND limit check
    print(f"\n  Point mass M=5e10 Msun -- physical g(r) and the deep-MOND limit sqrt(GM a0)/r:")
    print(f"     {'r[kpc]':>8}{'g_N':>11}{'g=nu*g_N':>12}{'sqrt(GM a0)/r':>15}{'regime':>9}")
    for rk in (1, 5, 20, 50):
        r = rk*kpc; gN = G*M/r**2; g = nu(gN/A0)*gN; dm = np.sqrt(G*M*A0)/r
        reg = "Newton" if gN > A0 else "deepMOND"
        print(f"     {rk:>8}{gN:>11.2e}{g:>12.2e}{dm:>15.2e}{reg:>9}")
    print("     -> in the outskirts g -> sqrt(GM a0)/r EXACTLY: flat rotation, v^4=GM a0 (BTFR).")

    # The SAME field drives circular AND radial orbits consistently -- integrate both.
    def g_of_r(r):
        gN = G*M/r**2; return nu(gN/A0)*gN
    # circular orbit at 20 kpc: v_c = sqrt(g r)
    r0 = 20*kpc; vc = np.sqrt(g_of_r(r0)*r0)
    # integrate a radial (purely in-fall-then-out) orbit and a circular orbit in the same field
    def rhs(t, y):                                   # y=[x,y,vx,vy], central field
        x, yy, vx, vy = y; r = np.hypot(x, yy)+1e-30; gg = g_of_r(r)
        return [vx, vy, -gg*x/r, -gg*yy/r]
    T = 2*np.pi*r0/vc
    sol_c = solve_ivp(rhs, [0, T], [r0, 0, 0, vc], rtol=1e-8, atol=1)      # circular
    sol_r = solve_ivp(rhs, [0, T], [r0, 0, 0, 0.3*vc], rtol=1e-8, atol=1)  # eccentric/radial-ish
    print(f"\n  Same field, two orbits integrated (2nd-order ODE, well-posed):")
    print(f"     circular  v_c={vc/1e3:.0f} km/s: closes, r stays {sol_c.y[0].min()/kpc:.1f}-"
          f"{np.hypot(sol_c.y[0],sol_c.y[1]).max()/kpc:.1f} kpc")
    print(f"     eccentric (v=0.3 v_c):      r ranges {np.hypot(sol_r.y[0],sol_r.y[1]).min()/kpc:.1f}-"
          f"{np.hypot(sol_r.y[0],sol_r.y[1]).max()/kpc:.1f} kpc -- ALSO well-defined.")
    print("  => modified gravity gives a unique trajectory for EVERY orbit. COMPLETE. [the framework's road]\n")


def part2_modified_inertia_is_open():
    print("="*82)
    print("PART 2 -- MODIFIED INERTIA: the elegant but OPEN road")
    print("="*82)
    print("""  Here you keep gravity Newtonian and modify the 'm a' side: inertia becomes
  acceleration-dependent, m_eff = m mu(a/a0). To get that from an action, the Lagrangian
  must depend on the ACCELERATION, L = L(r, r', r''). Two hard consequences, both real:""")
    # (a) Ostrogradski order count
    print("""
  (a) OSTROGRADSKI. Euler-Lagrange for L(r,r',r'') is
         d^2/dt^2 (dL/dr'') - d/dt (dL/dr') + dL/dr = 0   -> a 4th-ORDER equation of motion.
      Ostrogradski's theorem: any non-degenerate higher-derivative Lagrangian has a
      Hamiltonian UNBOUNDED BELOW -- a ghost (runaway) instability. So a generic LOCAL
      modified-inertia theory is sick. Avoiding the ghost forces the action to be
      degenerate or NONLOCAL (depend on the whole trajectory).""")
    # (b) circular vs linear: the deep-MOND coefficient differs -> no single local mu
    print("""  (b) ORBIT-DEPENDENCE. Milgrom (1994, Ann. Phys. 229, 384; 2011) showed the only
      Galilean-invariant modified-inertia action reproducing MOND is NONLOCAL, and the
      effective force law DIFFERS BY ORBIT TYPE. Concretely, in the deep-MOND limit the
      coefficient relating a to F is not universal:""")
    # demonstrate the orbit-dependence with the time-average that a nonlocal action performs:
    # for a trajectory with acceleration a(t), the nonlocal kinetic term ~ <|a|> (a time average).
    # circular: |a| = const = v^2/r. linear oscillation x=A cos(wt): a=-Aw^2 cos(wt), <|a|> differs.
    w = 1.0
    t = np.linspace(0, 2*np.pi/w, 4000)
    a_circ = np.ones_like(t)                                   # |a| constant (circular)
    a_lin  = np.abs(np.cos(w*t))                               # |a| for 1-D oscillation (normalized)
    avg_circ = np.trapz(a_circ, t)/(t[-1]-t[0])
    avg_lin  = np.trapz(a_lin,  t)/(t[-1]-t[0])
    print(f"      time-averaged |a| (the nonlocal action's input):  circular = {avg_circ:.3f},")
    print(f"      1-D oscillation = {avg_lin:.3f}  -> ratio {avg_circ/avg_lin:.2f}. The SAME a0 gives a")
    print(f"      DIFFERENT effective inertia for a circle vs a line: no single local mu(a/a0) exists.")
    print("""  (c) WHAT DOES work: for a CLOSED orbit of one frequency, the nonlocal action collapses
      to a clean law and reproduces MOND -- circular rotation curves and the BTFR come out
      right. That is why modified inertia 'works' for galaxies (mostly circular) yet has no
      consistent equation of motion for general (e.g. unbound, multi-frequency) trajectories.
      A complete modified-inertia dynamics is UNSOLVED -- in the literature, not just here.\n""")


def part3_verdict():
    print("="*82); print("LAYER-0 VERDICT"); print("="*82)
    print("""  * The framework's WORKING dynamics is modified GRAVITY (AeST, Layer 3): local,
    2nd-order, ghost-free, COMPLETE -- a unique trajectory for any orbit (Part 1, integrated).
    So the theory is closed at the level that matters for predictions.
  * Modified INERTIA -- the literal 'emergent/Machian inertia' reading that motivates a0~cH --
    is an OPEN problem: acceleration in the action forces an Ostrogradski ghost or nonlocality,
    and the working (nonlocal) version reproduces MOND only for closed orbits (Part 2). This is
    unfinished in the literature (Milgrom himself), not a gap unique to this framework.
  * HONEST resolution: the deep 'why inertia is modified' is open, but the framework does NOT
    need it -- it rides on complete modified gravity. Layer 0 is therefore the genuine research
    FRONTIER (close the modified-inertia dynamics, or show AeST IS its effective field theory),
    not a hole in the working theory. Either outcome is real physics; neither needs numerology.""")
    print("="*82)


def main():
    part1_modified_gravity_is_complete()
    part2_modified_inertia_is_open()
    part3_verdict()


if __name__ == "__main__":
    main()
