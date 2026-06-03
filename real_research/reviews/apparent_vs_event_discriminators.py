#!/usr/bin/env python3
"""
Can existing data break the apparent-vs-event-horizon degeneracy before z~3? -- the unifying answer.
====================================================================================================
The stress test (stress_test_geometric_origin.py) found that a0=cH/Z's evolution is the APPARENT-horizon
choice, vs the standard EVENT-horizon reading (a0 prop sqrt(Lambda) = CONSTANT). This script asks whether
existing data can decide between them -- and finds the unifying realization that collapses the whole
framework to one question. Needs numpy.
"""
import numpy as np

c, G, Mpc = 2.99792458e8, 6.674e-11, 3.0857e22
H0, Om, OL = 67.4e3/Mpc, 0.315, 0.685
Z = 2*np.sqrt(8*np.pi/3)
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
HL = H0*np.sqrt(OL)


def main():
    print("="*92)
    print("THE UNIFYING REALIZATION")
    print("="*92)
    print("""  The event-horizon reading (a0 prop sqrt(Lambda)) IS the constant-a0 null. So:

      apparent-vs-event horizon  ==  evolving-vs-constant a0  ==  framework-vs-standard-emergent-gravity

  i.e. the STANDARD emergent-gravity prediction (Milgrom a0~c sqrt(Lambda/3), Verlinde de Sitter entropy
  -- the EVENT horizon) is exactly CONSTANT a0. The entire framework reduces to ONE physical question:
  does the MOND scale track the APPARENT (Hubble) horizon [a0 prop H(z), rises] or the EVENT (de Sitter)
  horizon [a0 prop sqrt(Lambda), constant]? That is the whole thing.\n""")

    print("="*92); print("WHICH EXISTING PROBES CAN DECIDE IT? (almost none -- here is why)"); print("="*92)
    rows = [
        ("z=0 a0 value", "they differ only by sqrt(OmL)=%.0f%%, SWAMPED by the unpinned Z (~1 dex) and the 20%% M/L systematic" % ((1-np.sqrt(OL))*100), "NO"),
        ("CMB (linear)", "a0-independent at linear order (delta q00 = 0); both are CMB-safe", "NO"),
        ("linear growth / sigma8", "linear structure growth is a0-free in this framework", "NO"),
        ("BBN, recombination", "a0 acts only at LOW acceleration; the early universe is high-acceleration", "NO"),
        ("EFE / wide binaries (z=0)", "depend on a0(0), which is the SAME for both within systematics", "NO"),
        ("direct a0 at z~0.5-1", "apparent rises (E(0.9)=1.7x), event stays flat -> the z~0.9 point already favors apparent", "WEAKLY (~2sigma)"),
        ("direct a0 at z~3", "apparent %.1e vs event %.1e -- factor ~5, opposite of nothing" % (c*H0/Z*E(3), c*HL/Z), "DECISIVELY"),
    ]
    for probe, why, verdict in rows:
        print(f"  [{verdict:14}] {probe}")
        print(f"      {why}")
    print("""
  => EVERY z=0 and every LINEAR probe is DEGENERATE: a0 only bites at low acceleration, and the two
     horizons agree at z=0 (the sqrt(OmL) gap is smaller than the unpinned coefficient). The ONLY thing
     that separates them is the z-EVOLUTION of a0 -- and only the DIRECT deep-MOND a0 measures it. The
     existing z~0.9 point leans apparent at ~2 sigma; a clean break needs z~1-3 (the proposal).\n""")

    print("="*92); print("THE WHY-NOW COINCIDENCE -- one consideration each way (not decisive)"); print("="*92)
    print(f"  APPARENT: a0(z)/cH(z) = 1/Z = {1/Z:.3f} at EVERY epoch -> NO separate coincidence.")
    print("  EVENT:    a0/cH(z) drops from %.3f (now) to %.3f (z=3) -> a0~cH/6 only NOW (a why-now coincidence),"
          % (np.sqrt(OL)/Z, np.sqrt(OL)/(Z*E(3))))
    print("""            BUT the event side ABSORBS it: Lambda is fundamental and constant, and a0~cH0 now simply
            because we are entering Lambda-domination -- the STANDARD cosmic coincidence, not a new one.
  => the apparent horizon is tidier (no extra coincidence) but assumes a0 tracks the TOTAL (matter+Lambda)
     density -- a stronger, dynamical claim; the event horizon ties a0 to the fundamental Lambda but eats
     the why-now. Aesthetics do not decide; the data do.\n""")

    print("="*92); print("HONEST VERDICT"); print("="*92)
    print("""  * No existing data CLEANLY breaks the apparent-vs-event (= evolving-vs-constant) degeneracy: all
    z=0 and linear probes are degenerate; only the direct intermediate-z a0 distinguishes, and it weakly
    (~2 sigma, single-point, gas-confounded) favors the APPARENT horizon.
  * The deep payoff is conceptual, and it sharpens everything: the z~3 measurement is NOT merely
    'does a0 evolve?' -- it is 'does the IR scale of gravity track the APPARENT or the EVENT horizon?',
    i.e. the framework vs the STANDARD emergent-gravity prediction (which is constant). One number at
    z~3 answers a genuine question about which horizon sets gravity.
  * SIV adds a third answer (a0 DECREASING). So z~3 sorts: apparent/Hubble (rises) | event/Lambda
    (flat, standard) | scale-invariant vacuum (falls). The framework is the rising bet, currently and
    weakly favoured by the data, decisively testable, and theoretically the coincidence-free option.""")
    print("="*92)


if __name__ == "__main__":
    main()
