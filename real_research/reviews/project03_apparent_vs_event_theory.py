#!/usr/bin/env python3
"""
PROJECT 3: settle apparent-vs-event horizon THEORETICALLY -- the theory half of the z~3 test.
=============================================================================================
The whole framework reduces to one question (apparent_vs_event_discriminators.py): does a0 track the
APPARENT/Hubble horizon R_A=c/H [a0 prop H(z), RISES -- the framework] or the EVENT/de Sitter horizon
R_dS=c/(H0 sqrt(OmL)) [a0 prop sqrt(Lambda), CONSTANT -- standard Milgrom/Verlinde]? The z~3 measurement
decides it empirically. This file asks whether THEORY already leans one way, using rigorous FRW horizon
thermodynamics (Cai-Kim 2005; Wang-Gong-Abdalla 2006). The honest finding: theory is NOT neutral -- it
LEANS to the apparent horizon (the framework) -- but it is a lean, not a proof. Needs sympy.
"""
import sympy as sp


def part1_caikim():
    print("="*92); print("PART 1 -- [verified] the first law holds on the APPARENT horizon -> Friedmann (Cai-Kim 2005)"); print("="*92)
    t = sp.symbols('t'); G = sp.symbols('G', positive=True)
    H = sp.Function('H')(t); rho = sp.Function('rho')(t); p = sp.Function('p')(t)
    RA = 1/H; A = 4*sp.pi*RA**2; S = A/(4*G); T = 1/(2*sp.pi*RA)
    Hd = sp.solve(sp.Eq(sp.simplify(T*sp.diff(S, t)), A*(rho+p)*H*RA), sp.diff(H, t))[0]
    print(f"""  Apply dQ = T dS on the apparent horizon R_A = c/H (flat FRW), with the Hayward-Kodama temperature
  T = 1/(2 pi R_A) and S = A/4G. The matter energy flux dQ = A(rho+p)H R_A gives:
        Hdot = {sp.simplify(Hd)}
  -- EXACTLY the second Friedmann/Raychaudhuri equation. So the apparent horizon is a genuine
  thermodynamic boundary: its first law IS the cosmological field equation. (Verified symbolically here;
  this is the foundational Cai-Kim result, ~thousands of citations.)\n""")


def part2_event_fails():
    print("="*92); print("PART 2 -- the EVENT horizon does NOT satisfy the laws in a general FRW"); print("="*92)
    print("""  * The event horizon R_eh = a(t) int_t^inf dt'/a(t') is TELEOLOGICAL -- it depends on the ENTIRE
    FUTURE history, so it is not a locally-defined thermodynamic boundary at all.
  * Wang, Gong & Abdalla (2006): the first law and the GENERALIZED SECOND LAW hold on the apparent
    horizon but BREAK DOWN on the event horizon in an accelerating FRW universe.
  * The event horizon exists only because LambdaCDM happens to asymptote to de Sitter; it is the
    ASYMPTOTIC (final) horizon, not the instantaneous one.
  => As a boundary whose thermodynamics yields the dynamics, the apparent horizon is privileged; the
     event horizon is not a consistent local thermodynamic surface.\n""")


def part3_implication():
    print("="*92); print("PART 3 -- the implication for a0"); print("="*92)
    print("""  The framework's premise is that a0 comes from the cosmic horizon's THERMODYNAMICS (Unruh-/GH-
  temperature ~ horizon surface gravity). Part 1-2 say the thermodynamically consistent cosmic horizon is
  the APPARENT one, R_A=c/H, whose temperature ~hbar H/2pi RISES with z. So IF a0 is set by horizon
  thermodynamics, it tracks the apparent horizon and a0 prop H(z) -- the framework's rising bet. This is
  the strongest THEORETICAL argument the framework has for its one distinctive prediction, and it is not
  ad hoc: it falls out of the same Cai-Kim thermodynamics that yields Friedmann.\n""")


def part4_honest_counter():
    print("="*92); print("PART 4 -- the honest counter (why it is a LEAN, not a proof)"); print("="*92)
    print("""  The standard emergent-gravity reading (Milgrom a0 ~ c sqrt(Lambda/3); Verlinde's de Sitter
  entropy) ties a0 to the EVENT/de Sitter horizon -- and it rests on a DIFFERENT, internally-consistent
  premise: that a0 is set by the FUNDAMENTAL IR CUTOFF of the theory, which is the asymptotic de Sitter
  radius (Lambda is a true constant of nature), NOT by the instantaneous horizon thermodynamics. On that
  premise a0 prop sqrt(Lambda) = constant, and 'a0 ~ cH0 today' is just the ordinary cosmic coincidence
  (we are entering Lambda-domination). Nothing in thermodynamics forbids taking Lambda as the fundamental
  scale. So:
    * a0 from INSTANTANEOUS horizon thermodynamics  -> apparent horizon -> RISES (framework). [Cai-Kim]
    * a0 from the ASYMPTOTIC/fundamental IR cutoff   -> event horizon    -> CONSTANT (standard).
  The two differ in what they take as primitive (the instantaneous thermal state vs the fundamental
  Lambda). Theory tilts to the first -- it is the one that satisfies the laws locally -- but cannot kill
  the second.\n""")


def verdict():
    print("="*92); print("PROJECT 3 VERDICT"); print("="*92)
    print("""  Theory is NOT neutral on the framework's distinctive bet -- it LEANS to the apparent horizon:
    * rigorous FRW thermodynamics (Cai-Kim) is consistent ONLY on the apparent horizon R_A=c/H; the
      event horizon fails the first/second law and is teleological;
    * so 'a0 from horizon thermodynamics' (the framework's own premise) FORCES the apparent horizon
      -> a0 prop H(z), rising. That is real theoretical support, from the same physics that gives Friedmann.
  BUT it is a lean, not a proof: the constant-a0/event-horizon reading rests on a different, consistent
  premise (Lambda as the fundamental IR cutoff). The premises -- instantaneous thermal state vs
  fundamental Lambda -- cannot be separated by theory alone. The z~3 measurement separates them empirically.
  Net: the framework's rising-a0 is now the THEORETICALLY FAVORED option (given its own premise), not just
  the falsifiable one. The single best move to harden this: derive a0 directly from the apparent-horizon
  Unruh temperature in a way the event horizon cannot reproduce -- then theory would do more than lean.""")
    print("="*92)


def main():
    print("#"*92); print("# PROJECT 3 -- apparent vs event horizon, settled as far as theory allows"); print("#"*92 + "\n")
    part1_caikim(); part2_event_fails(); part3_implication(); part4_honest_counter(); verdict()


if __name__ == "__main__":
    main()
