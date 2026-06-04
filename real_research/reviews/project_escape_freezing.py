#!/usr/bin/env python3
"""
The escape attempt: is there a non-band-edge freezing mechanism that FORCES Z at the real de Sitter? (No -- but.)
================================================================================================================
project_pin_q.py showed the band-edge derivation of Z = 4 rho0(q)/sqrt(1-q) fails when q is pinned to the actual
de Sitter (q->1, where it diverges). The one speculative escape: a DIFFERENT freezing temperature T_freeze that
gives a FINITE Z ~ 5.79 at q->1. We survey every natural scale.

Z = (T_freeze/T_H) * rho0/pi, with rho0 -> 0.399 as q->1. Candidate T_freeze:
  * Gibbons-Hawking T_H (cold horizon):          T_freeze/T_H = 1            -> Z = 0.13  (45x too SMALL)
  * band edge (the failed one):                  T_freeze/T_H = 4pi/sqrt(1-q)-> DIVERGES
  * spectral width:                              T_freeze/T_H = 2pi/sqrt(1-q)-> DIVERGES
  * cord / stretched horizon ~ p*T_H (p~1e61):   T_freeze/T_H ~ 1e61         -> Z ~ 1e60 (absurd)
  * (reverse-engineered T_freeze = 45.5 T_H:      -> Z = 5.79, but NO natural origin -- circular)
=> NO DSSYK-intrinsic freezing scale gives a finite ~5.79. The escape, as a band-/width-/cord-type mechanism,
   FAILS: only a scale chosen to fit Z works, which is circular.

BUT the survey reveals the right answer. At q->1 the DSSYK is the SEMICLASSICAL limit -- it becomes ordinary
(GR) gravity. There, holographic equipartition (Padmanabhan) REPRODUCES the Friedmann equation, so the
coefficient IS the Friedmann factor Z = 2 sqrt(8pi/3) = 5.79 -- but by FITTING the horizon-DOF prefactor to
Bekenstein-Hawking/GR. So the actual-de-Sitter coefficient is NOT the band-edge 1e60; it is the Friedmann 5.79,
recovered through the semiclassical/equipartition limit -- REPRODUCED, not derived.

VERDICT. The escape SAVES the coefficient VALUE (the real-de-Sitter Z is 5.79 via the semiclassical limit, not
the catastrophic 1e60 the band edge gave) but does NOT force it. The band-edge 'derivation' was simply the wrong
physics; the right (semiclassical) mechanism reproduces Z. So the pin-q result is precisely: the band-edge
MECHANISM is refuted, while the coefficient VALUE (Friedmann 2 sqrt(8pi/3)) is fine -- consistent and natural at
the real de Sitter, but reproduced, not forced. This is the field-wide situation (no emergent-gravity framework
derives a0's coefficient from below); we have now confirmed it from both ends -- the band-edge microscopics fail,
and the semiclassical limit only reproduces. The coefficient is honestly closed: natural, consistent, open.
Needs numpy.
"""
import numpy as np

c = 2.998e8; H0 = 67e3/3.086e22; cH = c*H0
Zf = 2*np.sqrt(8*np.pi/3)


def rho0(q, K=200000):
    k1 = np.arange(1, K); k0 = np.arange(0, K)
    return np.exp(np.sum(np.log1p(-q**k1))+2*np.sum(np.log1p(q**k0))+np.log(np.sqrt(1-q)/2)-np.log(2*np.pi))


def main():
    print("#"*94)
    print("# The escape: no non-band-edge freezing scale forces Z at the real de Sitter; the value is Friedmann (reproduced)")
    print("#"*94 + "\n")
    r0 = rho0(0.9999); p_dS = 1.7e26/1.6e-35
    eps = 1e-4  # 1-q for 'at q->1'
    print(f"At the ACTUAL de Sitter q->1 (rho0 -> {r0:.3f}).  Z = (T_freeze/T_H) * rho0/pi:")
    print(f"  {'candidate freezing scale':40}{'T_freeze/T_H':>14}{'Z':>11}{'a0/1.2e-10':>13}")
    for nm, ratio in [("Gibbons-Hawking T_H (cold horizon)", 1.0),
                      ("band edge 4pi/sqrt(1-q) [failed]", 4*np.pi/np.sqrt(eps)),
                      ("spectral width 2pi/sqrt(1-q)", 2*np.pi/np.sqrt(eps)),
                      ("cord/stretched horizon ~ p*T_H", p_dS),
                      ("reverse-engineered to give 5.79", Zf*np.pi/r0)]:
        Z = ratio*r0/np.pi
        print(f"  {nm:40}{ratio:>14.2e}{Z:>11.2e}{cH/Z/1.2e-10:>12.1e}x")
    print()
    print("="*94); print("WHAT ACTUALLY GIVES 5.79 AT q->1"); print("="*94)
    print(f"""  None of the DSSYK-intrinsic scales: T_H is 45x too small, band edge & width DIVERGE, the cord ~1e60. Only a
  reverse-engineered T_freeze = 45.5 T_H gives 5.79 -- circular. The genuine answer: at q->1 DSSYK becomes the
  SEMICLASSICAL (GR) limit, where holographic equipartition reproduces the Friedmann equation, giving
        Z = 2 sqrt(8pi/3) = {Zf:.3f}
  -- by fitting the horizon-DOF prefactor to Bekenstein-Hawking/GR. REPRODUCED, not derived.\n""")

    print("="*94); print("VERDICT"); print("="*94)
    print("""  The escape SAVES the coefficient VALUE -- the real-de-Sitter coefficient is the Friedmann 5.79 (via the
  semiclassical/equipartition limit), NOT the band-edge's catastrophic 1e60 -- but it does NOT force Z. The
  band-edge 'derivation' was the wrong physics; the right (semiclassical) mechanism reproduces the coefficient,
  it does not derive it. So the complete, honest status of the coefficient: Z = 2 sqrt(8pi/3) is consistent and
  natural at the real de Sitter, fits the data to ~6%, and is REPRODUCED, not forced -- confirmed now from both
  ends (band-edge microscopics fail; semiclassical limit only reproduces). The coefficient question is closed:
  natural, consistent, honestly open. The deep-MOND SIGN -- q-independent -- remains the solid microscopic
  result; the empirical decider for the coefficient is a ~6% a0 measurement (2 sqrt(8pi/3)=5.79 vs 2pi=6.28).""")
    print("="*94)


if __name__ == "__main__":
    main()
