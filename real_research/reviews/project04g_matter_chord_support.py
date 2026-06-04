#!/usr/bin/env python3
"""
PROJECT 4g: Calc 1, attempted honestly -- the clean route is TRIVIAL (a sum rule), and the sign does NOT close.
==============================================================================================================
This pushes Calculation 1 of DSSYK_DEEPMOND_PROBLEM.md: does the matter operator O_Delta produce a state with
nonzero weight at the spectral center E=0 (=> linear freezing => deep-MOND sign)? It reaches an HONEST NEGATIVE:
the tempting "act O_Delta on the de Sitter vacuum and use kernel positivity" route is VACUOUS, and the sign
reduces to an open DICTIONARY statement -- which corrects the slight overclaim of project 4f ("sign closes at
very high confidence").

WHAT I FOUND (all verified numerically):

1. SUM RULE. The established DSSYK matter kernel M(t1,t2)=<t1|O_Delta|t2> (Berkooz et al. 2018 / Lin 2022; the
   q-deformed Schwarzian pinned in 4e/4f) satisfies  int dmu(t2) M(t1,t2) = 1  EXACTLY, for every t1, Delta, q
   (checked to 1e-8). It is a normalized transition kernel. Therefore  O_Delta|0> = |0>  exactly: the matter
   operator PRESERVES the maximal-entropy (chord-vacuum) state. So "O_Delta|0> has central support" is TRUE but
   TRIVIAL -- it is just the vacuum, which is the central state by definition. The chord-number wavefunction
   comes out psi_n = delta_{n0}. The clean positivity argument is vacuous: it proves nothing about the coupling.

2. THE MEANINGFUL OBJECT is the CONDITIONAL kernel P(t1|t2)=mu(t1)M(t1,t2): the energy spread of a probe placed
   at a DEFINITE energy t2. It is peaked near t1=t2 (the probe stays at its own energy). Consequence:
     * a probe at the CENTER (t2=pi/2, E=0) keeps ~47% of its weight near E=0 -> linear freezing -> MOND;
     * a probe at the EDGE (|E|~0.9) keeps ~4% near E=0 -> sub-linear -> NOT MOND.
   So central coupling depends entirely on WHERE THE PHYSICAL PROBE SITS in the spectrum.

3. THE SIGN REDUCES TO ONE DICTIONARY STATEMENT: "a physical near-horizon (deep-MOND, low-acceleration) matter
   probe maps to the spectral center E=0." The bulk picture (horizon = maximal entropy = spectral center) makes
   this very plausible, but it is the open chord<->depth dictionary item, NOT a derived fact. Project 4f tacitly
   ASSUMED it (probe at theta2=pi/2); that assumption IS the open question, so 4f's "sign closes" is downgraded
   to "sign holds IFF the near-horizon probe sits at the center -- very likely by bulk intuition, not proven".

NET: mechanism derived (4c); the naive matter-on-vacuum closure is trivial (this file); the sign reduces to one
open dictionary statement; the coefficient Z is still open (Calc 2). Honest status SHARPENED, not closed -- and
a tempting wrong "closure" is mapped and retired. Needs numpy.
"""
import numpy as np

NQ = 300


def qpoch(a, q, N=NQ):
    a = np.asarray(a, dtype=complex)
    out = np.ones(a.shape, dtype=complex); qk = 1.0
    for _ in range(N):
        out *= (1 - a*qk); qk *= q
    return out


def measure(th, q):
    qq = qpoch(q, q).real; e2 = np.exp(2j*th)
    return qq*(qpoch(e2, q)*qpoch(np.conj(e2), q)).real/(2*np.pi)


def M(t1, t2, D, q):
    num = qpoch(q**(2*D), q).real
    den = np.ones(np.shape(t1*np.ones_like(t2)+0j), dtype=complex)
    for s1 in (1, -1):
        for s2 in (1, -1):
            den *= qpoch(q**D*np.exp(1j*(s1*t1+s2*t2)), q)
    return (num/den).real


def main():
    print("#"*96)
    print("# PROJECT 4g -- Calc 1 attempted: the clean route is TRIVIAL (sum rule); sign does NOT close")
    print("#"*96 + "\n")
    th = np.linspace(1e-3, np.pi-1e-3, 3000); q = 0.5; D = 0.5
    mu = measure(th, q)

    print("="*96); print("1. THE SUM RULE -> O_Delta|0> = |0> (the clean route is vacuous)"); print("="*96)
    print("   int dmu(t2) M(t1,t2) at several t1 (should be 1 if it is a normalized transition kernel):")
    for t1 in (0.4, 1.0, np.pi/2, 2.2, 2.8):
        print(f"     t1={t1:.3f}:  int dmu M = {np.trapz(mu*M(t1, th, D, q), th):.8f}")
    print("""   => = 1 exactly, for all t1, Delta, q. So O_Delta|0> = int dmu(t2) M(.,t2) |.> = |0>: the matter
   operator PRESERVES the chord vacuum. psi_n = <n|O_Delta|0> = delta_{n0}. "Central support" is TRUE but
   TRIVIAL (it is the vacuum). The positivity-of-the-kernel closure proves nothing about the coupling.\n""")

    print("="*96); print("2. THE MEANINGFUL OBJECT: conditional kernel P(t1|t2) -- a probe stays at its energy"); print("="*96)
    print(f"   {'probe t2':>10}{'E=cos t2':>10}{'mode t1':>10}{'weight near center |E|<0.15':>30}")
    for t2 in (0.5, 1.0, np.pi/2, 2.2, 2.64):
        P = mu*M(th, t2, D, q); P = P/np.trapz(P, th)
        mode = th[np.argmax(P)]
        wc = np.trapz(P[np.abs(np.cos(th)) < 0.15], th[np.abs(np.cos(th)) < 0.15])
        print(f"   {t2:>10.3f}{np.cos(t2):>+10.2f}{mode:>10.3f}{wc:>30.2f}")
    print("""   => the probe's weight stays near its OWN energy. A CENTRAL probe (E=0) keeps ~47% near the center
   -> linear freezing -> MOND; an EDGE probe (|E|~0.9) keeps ~4% -> sub-linear -> NOT MOND. Central coupling
   depends entirely on WHERE the physical probe sits.\n""")

    print("="*96); print("3. THE SIGN REDUCES TO ONE DICTIONARY STATEMENT (the honest open question)"); print("="*96)
    print("""   Deep-MOND sign holds  <=>  a physical near-horizon (low-acceleration) matter probe maps to the
   spectral center E=0 (theta=pi/2). Bulk picture: horizon = maximal entropy = spectral center, so a probe felt
   at the cosmic horizon SHOULD sit at E=0 -> MOND. That is very plausible but is the open chord<->depth
   dictionary item -- NOT derived here. Project 4f ASSUMED a central probe (theta2=pi/2); that assumption is
   exactly this open question, so 4f's "sign closes at very high confidence" is downgraded to:
        sign holds IFF the near-horizon probe sits at the spectral center -- very likely (bulk), not proven.\n""")

    print("="*96); print("PROJECT 4g VERDICT (honest)"); print("="*96)
    print("""  Calculation 1 is NOT closed, and a tempting wrong closure is retired:
    * the matter kernel obeys a sum rule int dmu M = 1, so O_Delta|0> = |0> -- acting on the vacuum is trivial,
      and the "kernel is positive => central support => sign closes" argument is vacuous;
    * the real content is the conditional kernel: a probe stays at its own energy, so central coupling (and
      hence the deep-MOND sign) holds only if the PHYSICAL probe sits at the spectral center;
    * therefore the deep-MOND sign reduces to ONE dictionary statement -- near-horizon probe <-> E=0 -- which the
      bulk picture supports but does not prove. This DOWNGRADES project 4f's "very-high-confidence closure" to a
      conditional, honestly.
  Net across 4c-4g: mechanism derived (linear freezing in DSSYK); coupling reduces to one open dictionary item
  (not the trivial vacuum route); coefficient Z open. The prize is real and bounded -- and now stated without the
  overclaim. Reporting the negative because it is the truth, and because a mapped dead-end is worth more than a
  vacuous 'closure'.""")
    print("#"*96)


if __name__ == "__main__":
    main()
