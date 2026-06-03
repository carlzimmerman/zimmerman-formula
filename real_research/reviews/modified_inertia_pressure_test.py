#!/usr/bin/env python3
"""
PRESSURE-TEST: modified inertia (Unruh) as the engine for a0=cH/Z -- strengths AND the real breaks.
==================================================================================================
After the de Sitter-complexity engine failed its first real calculation (dssyk_cv_elastic_attempt.py),
modified inertia is the BEST-FITTING engine for the scaling law. So pressure-test it like an adversary:
verify what it genuinely gets right, then attack it where it is weakest, with calculation. Honest
verdict at the end -- it is a successful phenomenology, not a derivation. Needs numpy (+ SPARC for the fit).
"""
import numpy as np, glob, os

c, Mpc = 2.99792458e8, 3.0857e22
H0 = 67.4e3/Mpc
kpc = 3.0857e19


def part1_what_it_gets_right():
    print("="*94); print("PART 1 [PASS] -- what modified inertia genuinely gets right"); print("="*94)
    print("""  Premise (Milgrom 1999 / Deser-Levin 1997): an accelerated detector in de Sitter sees Unruh
  temperature T(a)=(hbar/2pi c kB) sqrt(a^2+(cH)^2). Inertia from DT=T(a)-T(0) gives
       g_N = sqrt(a^2+(cH)^2) - cH    <=>    g_obs = sqrt(g_bar^2 + g_bar a0).
   * SIGN: deep limit a = sqrt(2cH g_N) > g_N  -> gravity ENHANCED below a0 = MOND (right sign).
   * SHAPE: the sqrt(g^2+g a0) interpolation, fixed (no shape freedom).
   * EVOLUTION: a0 ~ cH so a0(z)=a0(0)E(z) is automatic, coefficient-free -- the framework's L3 for free.
   This is a real, genuine engine: it gives the scale, the sign, the shape, and the evolution.\n""")


def part2_coefficient_unpinned():
    print("="*94); print("PART 2 [WEAK] -- the coefficient is scheme-dependent (unpinned), like every route"); print("="*94)
    for name, a0 in [("naive DeltaT  (a0 = 2cH)", 2*c*H0), ("Milgrom careful (a0 = cH/2pi)", c*H0/(2*np.pi)),
                     ("observed a0", 1.2e-10)]:
        print(f"     {name:30} a0 = {a0:.3e}   ({a0/1.2e-10:.2f}x observed)")
    print("""  => the DERIVED coefficient ranges from 2cH (11x too big) to cH/2pi (spot on) depending on the
  matching scheme. Modified inertia does NOT pin a0 either; you still fit it. Same O(1) problem.\n""")


def part3_data_fit():
    print("="*94); print("PART 3 [PASS, but fit-not-predict] -- SPARC RAR"); print("="*94)
    DATA = os.path.join(os.path.dirname(__file__), "..", "data", "sparc_data")
    ML_D, ML_B = 0.5, 0.7
    gb, go, w = [], [], []
    for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        try: d = np.genfromtxt(f, comments="#")
        except Exception: continue
        if d.ndim != 2 or d.shape[1] < 6: continue
        R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
        Rm = R*kpc; Vbar2 = np.sign(Vgas)*Vgas**2 + ML_D*Vdisk**2 + ML_B*Vbul**2
        g_b = Vbar2*1e6/Rm; g_o = (Vobs*1e3)**2/Rm
        ok = (g_b > 0) & (g_o > 0) & np.isfinite(g_b) & np.isfinite(g_o) & (Vobs > 0)
        fr = np.clip(eV, 1, None)/np.clip(Vobs, 1, None)
        gb += list(g_b[ok]); go += list(g_o[ok]); w += list(1/fr[ok]**2)
    gb, go, w = np.array(gb), np.array(go), np.array(w)
    mi = lambda gb, a0: np.sqrt(gb**2 + gb*a0)
    grid = np.linspace(0.4e-10, 3e-10, 600)
    s = [np.sqrt(np.sum(w*(np.log10(go)-np.log10(mi(gb, a)))**2)/np.sum(w)) for a in grid]
    i = int(np.argmin(s))
    print(f"  modified-inertia shape fits SPARC at {s[i]:.3f} dex (error-weighted), best-fit a0={grid[i]*1e10:.2f}e-10.")
    print(f"  Best fit of the SHAPE is excellent -- but a0 is FIT ({grid[i]*1e10:.2f}e-10), not predicted (2cH={2*c*H0*1e10:.0f}e-10).\n")


def part4_the_real_breaks():
    print("="*94); print("PART 4 [THE REAL ATTACKS] -- where modified inertia actually breaks"); print("="*94)
    print("""  W1 [PREMISE is a posit]. 'Unruh radiation provides the inertial reaction force' is Milgrom's
     HYPOTHESIS, not established physics. The Unruh effect is real; its ROLE in inertia is not derived
     (no one has shown the Unruh bath back-reacts to give the inertial force). So the engine's foundation
     is a posit -- exactly like the entropy route's posited entropy modification. Better data fit, NOT
     better derived.

  W2 [NON-LOCALITY + closed-orbit theorem -- the structural break]. Modified inertia is fundamentally
     NON-LOCAL: the inertia depends on the whole trajectory (its frequency content), not the instantaneous
     acceleration. Consequences (Milgrom 1994, 'nonstandard inertia'):
       - a theory tuned to give MOND for CIRCULAR orbits makes DIFFERENT predictions for non-circular
         (radial, eccentric) orbits -- the 'closed-orbit' tension. Rotation curves (circular) are fit; the
         same theory's predictions for dispersions / the EFE / solar-system higher-order effects need not
         match, and need not agree with modified-GRAVITY MOND.
       - there is NO complete LOCAL action: any local higher-derivative inertia carries an Ostrogradski
         ghost; the non-local version evades ghosts but has no standard Lagrangian and is hard to make
         fully predictive (energy/momentum conservation require care).
     This is a genuine incompleteness, not a detail: modified inertia is a successful RULE for rotation
     curves without a complete, local, predictive dynamics behind it.\n""")


def verdict():
    print("="*94); print("VERDICT -- modified inertia, scored honestly"); print("="*94)
    print("""  STRENGTHS: the best-FITTING engine for a0=cH/Z -- it delivers the sign, the sqrt-law, the RAR at
  0.105 dex, and (uniquely cleanly) the EVOLUTION a0(z)=a0(0)E(z) coefficient-free.
  WEAKNESSES: the coefficient is unpinned (2cH...cH/2pi, you fit a0); the PREMISE (Unruh->inertia) is a
  posit, not established; and it is NON-LOCAL with NO complete local action and a closed-orbit tension.

  SO, FOR THE FRAMEWORK: modified inertia is the best DATA engine for the scaling law and gives the
  evolution for free -- but it is a successful PHENOMENOLOGY, not a derivation, and it lacks a complete
  dynamics. The complementary trade: modified GRAVITY (the entropy/Debye route -> AeST) is worse-fitting
  in detail but has a complete covariant ACTION (clean_slate_field_theory.py derives ~80% of it) and the
  right sign. Neither is 'derived'; they fail differently:
       modified INERTIA  : best fit + evolution free, but non-local / no action / premise posited.
       modified GRAVITY  : complete action (AeST), right sign, but modification posited / fit a0.
  The honest reading is that a0=cH/Z is a parametrization that BOTH can power, each at a specific cost --
  and that the deep-MOND derivation is unsolved on every route (established_paths_to_mond.py). Modified
  inertia is the engine to QUOTE for the data and the evolution; modified gravity is the engine to BUILD
  for a covariant theory. That is the honest division of labor, with no route oversold.""")
    print("="*94)


def main():
    print("#"*94); print("# MODIFIED INERTIA (Unruh) AS THE ENGINE -- adversarial pressure-test"); print("#"*94 + "\n")
    part1_what_it_gets_right(); part2_coefficient_unpinned(); part3_data_fit(); part4_the_real_breaks(); verdict()


if __name__ == "__main__":
    main()
