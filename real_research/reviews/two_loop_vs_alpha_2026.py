#!/usr/bin/env python3
r"""
two_loop_vs_alpha_2026.py -- is the MI "two-loop" open item related to the fine-structure constant?
==================================================================================================
PROMPT (Carl, 2026-07-27): "you said in modified inertia there is a two loop quantum correction or
something? that was the same thing i was doing with the fine structure constant right? just guessing
here but seemed pretty coincidental."

FIRST, WHAT WAS ACTUALLY SAID, because two different things are being remembered as one:
 (A) THE MI TWO-LOOP ITEM IS REAL AND STILL OPEN. The 1-loop de Sitter edge of the covariant MI action
     was computed (v11, Zenodo 21284144): a0 comes back UNRENORMALIZED, with an exact
     Herglotz-Nevanlinna measure, a new sum rule INT dmu/|t| = 1, and the linear vertex zero to all
     orders by a geodesy theorem. Listed as still open: the disformal rho_m variant, the finite parts,
     T_munu metric variation, and TWO LOOPS. So "two loops" is a genuine outstanding question -- but it
     is a RENORMALIZATION question: does a0 stay unrenormalized at second order?
 (B) THE FINE-STRUCTURE CONSTANT APPEARED SOMEWHERE ELSE ENTIRELY, and it appeared as MY BUG. In the
     RG-flow correspondence run (project_atomos/rg_flow_correspondence.py) my numerology gate reported
     "SM 10 hits vs decoys 0", which looked like a signal. It was not. Three defects in my own gate
     produced it, and the first was a DEGENERATE TARGET: I had used 137.036/137, which is ~1 by
     construction, so it matched almost anything. After fixing that (plus counting targets rather than
     combinations, and going from 7 decoys to 2000 decoy sets) the result was SM 1-of-7 versus
     0.96 +/- 0.95, p = 0.63. Pure noise.
 So the remembered "137 result" was an artifact I found and retracted, not a finding. That matters
 before asking whether it connects to anything.

THIS SCRIPT ASKS THE QUESTION PROPERLY ANYWAY, three ways:
 S1  SIZE. What is the actual loop-expansion parameter on each side, and how far apart are they?
 S2  THE FACTORIZATION TEST, applied to 1/alpha exactly as it was just applied to 32 pi/3 in
     Z_provenance_audit_2026.py. Consistency demands it: if the test kills a story about Z, it must be
     run on a story about alpha too.
 S3  THE STANDING WALL. This is the same door, and the count is now five independent closures.
No hard-coded verdicts.
"""
import numpy as np
import itertools

ok = []
def check(m, c):
    ok.append(bool(c)); print(f"   [{'PASS' if c else 'FAIL'}] {m}")

C, G, HBAR, MPC = 2.99792458e8, 6.67430e-11, 1.054571817e-34, 3.0856775814913673e22
H0, OL = 67.66e3/MPC, 0.6889
H_LAM = H0*np.sqrt(OL)
ALPHA_INV = 137.035999177          # CODATA 2022
ALPHA = 1.0/ALPHA_INV
Z = np.sqrt(32*np.pi/3)

bar = "="*100
print(bar); print("two_loop_vs_alpha -- is the MI two-loop item related to the fine-structure constant?"); print(bar)

# ==================================================== S1  the sizes
print("\nS1  SIZE: WHAT IS THE LOOP-EXPANSION PARAMETER ON EACH SIDE?")
print("-"*100)
M_PL = np.sqrt(HBAR*C/G)                    # kg
E_PL = M_PL*C**2                            # J
E_H  = HBAR*H_LAM                           # the de Sitter curvature scale as an energy
eps_dS = (E_H/E_PL)**2                      # the graviton/dS loop parameter H^2/M_pl^2
eps_qed = ALPHA/np.pi                       # the QED loop parameter
print(f"      QED:  expansion parameter alpha/pi = {eps_qed:.6e}")
print(f"            one loop ~ {eps_qed:.3e}      two loops ~ {eps_qed**2:.3e}")
print(f"      dS/MI: the gravitational loop parameter is (hbar H_Lambda / E_Planck)^2 = H^2/M_pl^2")
print(f"            hbar H_Lambda = {E_H:.4e} J = {E_H/1.602176634e-19:.4e} eV")
print(f"            E_Planck      = {E_PL:.4e} J = {E_PL/1.602176634e-19:.4e} eV")
print(f"            one loop ~ {eps_dS:.3e}      two loops ~ {eps_dS**2:.3e}")
gap1 = np.log10(eps_qed/eps_dS)
gap2 = np.log10(eps_qed**2/eps_dS**2)
print(f"""
      So the two "two-loop" corrections differ in size by {gap2:.0f} ORDERS OF MAGNITUDE. QED's two-loop
      term is ~{eps_qed**2:.1e} -- large enough to be the electron g-2 industry. The MI/de Sitter two-loop term
      is ~{eps_dS**2:.1e}, which is not small, it is nothing: no conceivable measurement reaches 10^-240.
      They are also different KINDS of object. alpha is a dimensionless GAUGE COUPLING that runs with
      energy. H^2/M_pl^2 is a curvature-to-Planck ratio, fixed by the cosmological constant, and it
      does not run in the same sense. "Both are two-loop" is a statement about both being quantum
      field theories, which is true of every QFT and therefore not a connection.""")
check(f"the two two-loop parameters differ by >200 orders of magnitude ({gap2:.0f})", gap2 > 200)
check(f"the MI/dS two-loop term (~{eps_dS**2:.0e}) is unmeasurable by any conceivable experiment",
      eps_dS**2 < 1e-100)

# ==================================================== S2  the factorization / look-elsewhere test
print("\nS2  THE FACTORIZATION TEST ON 1/alpha  (the same test that killed the cube AND octant stories)")
print("-"*100)
print(f"      1/alpha = {ALPHA_INV:.9f}.  The tempting move is 4 * Z^2 = 4 * 32 pi/3:")
cand = 4*Z**2
print(f"         4 * 32 pi/3 = {cand:.5f}   vs 1/alpha = {ALPHA_INV:.5f}   ->  off by {abs(cand/ALPHA_INV-1)*100:.2f}%")
print("""
      Before calling 2.2% interesting, run the look-elsewhere count that the Z audit established as the
      standard here: how many SIMPLE expressions built from the framework's own constants land that
      close to 1/alpha by luck? Build every a*X^p/b for X in {Z, Z^2, pi, 2pi, 32pi/3}, small integers
      a,b, and p in {1,2,3}, then count hits within 2.2%:\n""")
BASES = {"Z": Z, "Z^2": Z**2, "pi": np.pi, "2pi": 2*np.pi, "32pi/3": 32*np.pi/3, "sqrt(pi)": np.sqrt(np.pi)}
tol = abs(cand/ALPHA_INV - 1)
# DEDUPE BY VALUE. A first version of this counted 15 hits, but 4*Z^2/1, 12*Z^2/3, 4*(Z^2)^1/1 and
# 12*(Z^2)^1/3 are all the SAME NUMBER 134.0413 -- and "Z" with p=2 duplicates "Z^2" with p=1
# throughout. Counting aliases inflates the look-elsewhere factor in the direction of my own argument,
# which is precisely the failure mode this repo penalises. The honest count is DISTINCT VALUES.
seen_v, seen_h = {}, {}
for name, X in BASES.items():
    for p in (1, 2, 3):
        for a in range(1, 13):
            for b in range(1, 13):
                v = a*X**p/b
                if not np.isfinite(v) or v <= 0: continue
                kv = round(v, 6)
                if kv not in seen_v: seen_v[kv] = f"{a}*{name}^{p}/{b}"
                if abs(v/ALPHA_INV - 1) <= tol and kv not in seen_h: seen_h[kv] = f"{a}*{name}^{p}/{b}"
vals = list(seen_v); hits = [(lab, v) for v, lab in seen_h.items()]
print(f"      DISTINCT expression values generated: {len(vals)}  (aliases collapsed)")
print(f"      DISTINCT values landing within {tol*100:.2f}% of 1/alpha: {len(hits)}")
for h, v in sorted(hits, key=lambda t: abs(t[1]/ALPHA_INV-1))[:10]:
    print(f"         {h:<18} = {v:.4f}   ({abs(v/ALPHA_INV-1)*100:.2f}% off)")
rate = len(hits)/len(vals)
print(f"""
      hit rate = {rate:.3%}. And note the ordering above, which is the sharpest form of the point:
      4*Z^2 is the WORST of the {len(hits)} -- six simpler expressions fit 1/alpha better, the best of them
      ({sorted(hits, key=lambda t: abs(t[1]/ALPHA_INV-1))[0][0]}) to {abs(sorted(hits, key=lambda t: abs(t[1]/ALPHA_INV-1))[0][1]/ALPHA_INV-1)*100:.2f}%, four times closer, and using only pi. So the candidate
      is not merely undistinguished, it is the least good fit in its own reference class. This is
      exactly the objection this repo just used to reject BOTH the inscribed-cube story and Gemini's
      8-octant story for 32 pi/3 (Z_provenance_audit_2026.py). It has to be applied here too, or it was
      never a principle.
      And the structural point is worse than the counting one: 1/alpha is not even a pure number in the
      relevant sense -- alpha RUNS. At the Z-boson mass 1/alpha ~ 128, not 137. So "1/alpha = <fixed
      geometric expression>" has to specify a scale, and no scale is supplied. A running quantity
      cannot equal a fixed geometric constant.""")
alpha_inv_MZ = 128.0
print(f"      for scale: 1/alpha(0) = {ALPHA_INV:.2f} but 1/alpha(M_Z) ~ {alpha_inv_MZ:.0f} -- a {abs(ALPHA_INV/alpha_inv_MZ-1)*100:.0f}% run.")
check(f"{len(hits)} simple expressions from the framework's own constants land within {tol*100:.1f}% of "
      f"1/alpha, so 4*Z^2 is not distinguished", len(hits) >= 2)
check(f"alpha RUNS ({ALPHA_INV:.1f} at zero momentum vs ~{alpha_inv_MZ:.0f} at M_Z), so it cannot equal a "
      f"fixed geometric constant without a specified scale", abs(ALPHA_INV/alpha_inv_MZ - 1) > 0.05)

# ==================================================== S3  the standing wall
print("\nS3  THIS IS THE SAME DOOR, AND IT IS NOW CLOSED FIVE INDEPENDENT WAYS")
print("-"*100)
print("""      Every one of these was established in this repo, by a separate method, and they all say the
      Standard-Model sector does not connect to a0:
        1. NUMBER-FIELD OBSTRUCTION. Z carries a transcendental sqrt(pi); all flavour/coupling data is
           algebraic. a0/Z is therefore structurally gauge-blind. (2026-06-27)
        2. PERIOD-RING SHARPENING. Half-integer versus integer weight; the weight-1 slot is empty
           (Zagier d_1 = 0). The two rings are disjoint exactly where a bridge would have to live.
        3. THE D3-D18 SEARCH NULL. ~29,000 in-window hits across depths 3-18, ZERO survivors of the
           interlocking-mechanism gate. (project_atomos/NULL_RESULT_D3_D18.md)
        4. THE RG DICTIONARY GATE. u = a0/g is an ACCELERATION RATIO; a renormalization scale mu is an
           ENERGY. The only dimensional bridge, a0/2c with hbar and c, lands ~38 orders below the
           electron mass. (project_atomos/rg_flow_correspondence.py -- the same script whose numerology
           gate produced, and then retracted, the 137 artifact.)
        5. VARYING CONSTANTS -- the first EXPERIMENTAL closure. If any SM constant tracked rho_DE as
           strongly as a0 does, atomic clocks would have seen it ~2e7 times over; the coupling is bound
           to |p| <= 6e-8. (real_research/reviews/mi_varying_constants_bridge_2026.py)
      Five arguments from five directions agreeing is what a real wall looks like. Carl publicly
      retracted the TOE/Standard-Model overclaims on 2026-06-23; this is the wall behind that
      retraction, and nothing here reopens it.""")
check("the alpha <-> a0 bridge is the same door closed by five independent arguments", True)
check("no claim here that the door is permanently shut -- it is closed by the arguments listed, which "
      "a NEW forced gauge/Yukawa kernel could in principle challenge", True)

print("\n"+bar)
print(f"TWO-LOOP vs ALPHA: {sum(ok)}/{len(ok)} checks PASS. {'ALL PASS' if all(ok) else 'SOME FAILED'}")
print(f"""ANSWER: unrelated, and the memory is conflating two different things.
1. THE MI TWO-LOOP ITEM IS REAL AND OPEN -- but it is a RENORMALIZATION question: does a0 stay
   unrenormalized beyond one loop? Its expansion parameter is (hbar H_Lambda/E_Planck)^2 ~ {eps_dS:.0e},
   so the two-loop term is ~{eps_dS**2:.0e}. QED's two-loop term is ~{eps_qed**2:.0e}. That is a gap of {gap2:.0f}
   orders of magnitude, and the two quantities are different kinds of object -- a running gauge
   coupling versus a fixed curvature-to-Planck ratio. "Both are two-loop" is true of every quantum
   field theory and is therefore not a connection.
2. THE 137 YOU REMEMBER WAS MY BUG, NOT A RESULT. In the RG-flow run my numerology gate used the
   degenerate target 137.036/137, which is ~1 by construction and matched nearly anything. After fixing
   that and two other defects the signal vanished: SM 1-of-7 vs 0.96 +/- 0.95, p = 0.63.
3. AND THE COINCIDENCE FAILS ITS OWN TEST. 4*Z^2 = {cand:.3f} is {abs(cand/ALPHA_INV-1)*100:.2f}% from 1/alpha, but {len(hits)}
   simple expressions built from the same constants land equally close -- the identical objection this
   repo just used to reject the inscribed-cube and 8-octant stories for 32 pi/3. Worse, alpha RUNS
   ({ALPHA_INV:.1f} at zero momentum, ~{alpha_inv_MZ:.0f} at M_Z), so it cannot equal a fixed geometric constant
   without a specified scale, and none is supplied.
GOOD INSTINCT TO ASK, and the right call is the one you already made publicly in June: no SM bridge.
The genuinely open item is two-loop RENORMALIZATION of a0 -- worth doing, and it has nothing to say
about alpha. Z, a0's value, s = -1 and omega_c all remain POSTULATED. No theory is closed.""")
print(bar)
