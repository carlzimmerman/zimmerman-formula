#!/usr/bin/env python3
"""
Re-examination: did we actually resolve the Bullet Cluster and the S8 tension?
=============================================================================
Carl's challenge: "if it can't resolve the bullet cluster it is completely
falsified" and "we ran scripts on s8 tension and bullet cluster -- look it up."

We DID run scripts (in ai_slop/). This file adjudicates them with real numbers,
because the question deserves calculation, not assertion. Findings are labelled:
  [HOLDS]      the script's argument survives scrutiny
  [BROKEN]     the script's argument has a specific, identifiable physics error
  [CONTESTED]  a real point, but weaker / more disputed than the script presents
  [NUMEROLOGY] a formula-search coincidence with ~0 evidential weight

Run: python bullet_and_s8_reexamination.py     (needs numpy)
"""
import numpy as np

c   = 2.99792458e8        # m/s
G   = 6.674e-11           # SI
kpc = 3.0857e19           # m
Mpc = 3.0857e22           # m
Gyr = 3.156e16            # s
Myr = 3.156e13            # s
OM, OL = 0.315, 0.685
A0  = 1.2e-10             # m/s^2 today
E   = lambda z: np.sqrt(OM*(1+z)**3 + OL)


# ===========================================================================
def bullet_timescales():
    print("="*78)
    print("PART 1 -- THE BULLET CLUSTER 'non-equilibrium' RESOLUTION")
    print("="*78)
    print("""
  The claim (ai_slop/.../BULLET_CLUSTER_ANALYSIS.md, sec 3.3-4):
    'MOND's phantom mass has a relaxation time t_MOND = sqrt(R/a0) ~ Gyr.
     The collision (t ~ 150 Myr) is faster, so the phantom mass can't track
     the displaced gas -- it stays on the galaxies -> reproduces the offset.'

  This stands or falls on ONE thing: is sqrt(R/a0) the time for the MOND
  FIELD to respond to a moved source? Compute the three relevant times.""")
    z = 0.296
    a0 = A0*E(z)
    R  = 700*kpc                      # system / separation scale
    d_off = 250*kpc                   # gas-lensing offset scale
    v  = 4700e3                       # observed shock velocity (Markevitch 2006)
    v_gas = 2700e3                    # actual gas-bullet speed (Springel&Farrar 2007)

    t_signal = R/c                    # field re-settles on the signal-crossing time
    t_coll   = R/v                    # collision crossing time
    t_coll_g = R/v_gas
    t_dyn    = np.sqrt(R/a0)          # dynamical / free-fall time (the script's 't_MOND')

    print(f"  a0(z=0.296) = {a0:.2e} m/s^2   R = 700 kpc")
    print(f"    t_signal  = R/c           = {t_signal/Myr:7.2f} Myr   <- FIELD response time")
    print(f"    t_collision = R/v(4700)   = {t_coll/Myr:7.2f} Myr")
    print(f"    t_collision = R/v(2700)   = {t_coll_g/Myr:7.2f} Myr")
    print(f"    t_dynamical = sqrt(R/a0)  = {t_dyn/Myr:7.2f} Myr   <- the script's 't_MOND'")
    print(f"    (the .md even mis-took sqrt(2e32)=1.4e16 s for 4.5e16 s -- a 3x sqrt slip)")
    print(f"""
  VERDICT [BROKEN]: the MOND field -- non-relativistic (AQUAL is an ELLIPTIC,
  instantaneous Poisson-type equation: zero time-derivative) or relativistic
  (AeST fields re-settle on the light-crossing time R/c) -- tracks the source
  QUASI-STATICALLY because
        t_signal ({t_signal/Myr:.0f} Myr)  <<  t_collision ({t_coll/Myr:.0f} Myr)   (ratio {t_coll/t_signal:.0f}x).
  sqrt(R/a0) is the DYNAMICAL (orbital/free-fall) time -- how MATTER moves --
  NOT how the FIELD responds to matter. The script swapped one for the other.
  Because the field is quasi-static, the phantom mass sits where the baryons
  ARE at each instant; the baryons are ~80% gas; so the lensing tracks the GAS
  -> the offset problem RETURNS. (And a true lag would freeze a single central
  blob, not two peaks on the two galaxy groups -- it can't even make the shape.)""")
    print(f"""
  Honest other side -- why 'completely falsified' is ALSO too strong:
   [CONTESTED] high collision velocity: 4700 km/s is the SHOCK speed; the gas
        bullet itself is ~2700 km/s (Springel&Farrar 2007), and larger sims
        (Thompson+2015, Kraljic&Sarkar2015) find such speeds rare-but-allowed
        in LCDM. A weak ding on LCDM, not a win for MOND.
   [CONTESTED] Abell 520 'dark core' (Mahdavi+07, Jee+12) is awkward for
        collisionless DM -- but Clowe+2012 disputes it. Unsettled.
   [HOLDS]     relativistic MOND fits the Bullet ONLY by adding ~2 eV neutrinos
        + central dark mass (Angus, Famaey & Zhao 2006): MOND *with* hot DM.
  Net: the cluster mass problem is OLD MOND physics (factor ~2 residual at
  cluster cores, a0~g there). The Bullet is its sharpest image. It is a genuine,
  inherited, UNSOLVED challenge -- not resolved by us, not a clean falsification
  either (MOND patches it with neutrinos, as it always has). Evolving a0 does
  NOT help (z=0.296 -> a0 only +17%).""")


# ===========================================================================
def s8_contradiction():
    print("\n"+"="*78)
    print("PART 2 -- THE S8 TENSION: the framework's OWN theorem forbids the fix")
    print("="*78)
    print("""
  Two S8 scripts were run. Both fail, for independent reasons.

  (A) ai_slop/.../S8_TENSION_Z2_ANALYSIS.py  -- 'evolving a0 suppresses
      late-time structure, lowering sigma8.'  This is the SAME a0(z) that is
      our one distinctive idea. But here it collides head-on with our BEST
      result, the delta-q00 = 0 linear-CMB-safety theorem (Paper II):""")
    print("""      * sigma8 is BY DEFINITION a LINEAR-theory quantity:
          sigma8^2 = (1/2pi^2) INT k^2 P_lin(k) W^2(k*8Mpc/h) dk,  P_lin at z=0.
      * Paper II proves the a0 term (~ Y^{3/2}, Y = q^{mu nu} grad-phi grad-phi)
        has Ybar = 0 on FRW, so its linear variation ~ Ybar^{1/2} delta-Y = 0.
        => a0 is ABSENT from the linear perturbation equations.
      * Therefore the linear growth D(z), hence sigma8, hence S8, are EXACTLY
        the a0-free (≈LCDM) values, for ANY a0(z).""")
    print("""  [BROKEN -- internal contradiction]: a0(z) cannot both leave the linear CMB
  invariant (Paper II, our strongest theorem) AND suppress the linear S8. The
  two claims are mutually exclusive. Whatever makes the CMB safe makes the S8
  'solution' impossible. (Nonlinear MOND turns on at small scales and would
  ADD clustering -- wrong sign for S8 anyway.)""")

    # the numerology part
    Z = 2*np.sqrt(8*np.pi/3)
    cands = [("6/Z", 6/Z), ("CUBE/10 = 0.8", 0.8), ("2/Z", 2/Z), ("sqrt(3/Z^2)", np.sqrt(3/Z**2))]
    print("\n  (A') the 'sigma8 = 6/Z, CUBE/10, ...' part is pure formula-search:")
    for name, val in cands:
        print(f"        {name:16s} = {val:.4f}   (picked to bracket 0.76-0.81)")
    print("  [NUMEROLOGY]: a search that emits 0.76 AND 0.80 'explains' a 2-sig-fig")
    print("  target either way -- ~0 bits, exactly the FDR result of the main review.")

    # the topological-cutoff part, from the saved run
    print("""
  (B) ai_slop/.../s8_power_truncation.py  -- the OTHER mechanism, the 20.6 Gpc
      topological IR cutoff. It honestly ran the real E&H sigma8 integral with a
      hard k_min = 2pi/L_c and REPORTED FAILURE:""")
    print("        power removed by the cutoff : 7.5e-7 %   (k_min=3e-4 Mpc^-1 is")
    print("        far outside the k~0.2 Mpc^-1 band that sets sigma8) -> sigma8 unchanged.")
    print("        Worse: with Omega_m=6/19=0.3158, S8_LCDM=0.831 > Planck 0.811, so the")
    print("        framework's own Omega_m makes the tension ~46% WORSE, not better.")
    print("  [BROKEN]: status FAILED in the script's own results JSON.")


# ===========================================================================
def main():
    bullet_timescales()
    s8_contradiction()
    print("\n"+"="*78)
    print("LEDGER -- re-examination of the two 'resolved' problems")
    print("="*78)
    print("""  BULLET CLUSTER:
    - the 'non-equilibrium phantom mass' resolution is [BROKEN]: it uses the
      dynamical time sqrt(R/a0) as if it were the field-response time; the field
      responds on R/c (~2 Myr << 150 Myr), stays quasi-static, tracks the gas.
    - BUT 'completely falsified' is also wrong: the cluster residual is inherited
      MOND physics, patched (ugly) with ~2 eV neutrinos; velocity & A520 cut both
      ways. Net: a genuine, inherited, UNSOLVED challenge -- not a clean kill.
  S8 TENSION:
    - evolving-a0 suppression is [BROKEN] -- forbidden by our own delta-q00=0
      linear-CMB-safety theorem (a0 absent from linear growth => sigma8 unchanged).
    - the sigma8=6/Z numerology is [NUMEROLOGY]; the 20.6 Gpc IR cutoff is
      [BROKEN] (7e-7% power removed; Omega_m=6/19 makes it 46% worse).
  BOTTOM LINE: neither was resolved. The honest memory is that the scripts
  *attempted* both and (for S8) one even logged its own FAILURE. The Bullet is
  MOND's inherited unsolved problem; the S8 fix is killed by our strongest result.""")
    print("="*78)


if __name__ == "__main__":
    main()
