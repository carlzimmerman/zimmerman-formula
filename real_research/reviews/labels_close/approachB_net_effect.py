#!/usr/bin/env python3
"""
NET EFFECT of Approach B (confinement) on the deep-MOND sign verdict -- the honest both-ways tally.
Does the Rahman-Susskind confinement route HELP the framework, HURT it, or leave it CONTESTED-TERMINAL?
We tally each logical branch on its own terms. No fudge factors; pure logic table + the verified physics
of Step 2 (n=0 horizon = spectral center; bulk pode = spectral edge).

THE THREE CANDIDATE READINGS of 'the deep-MOND low-acceleration probe' and where each lands:

  reading              | is it a singlet? | escapes? | lands at...        | spectral locale | sign
  ---------------------|------------------|----------|--------------------|-----------------|--------
  (R1) literal matter  | NO (generic)     | NO       | stretched horizon, | confined; melts | NO PROBE
       chord q^{Delta N}|  1/N^2-rare      | confined | not a bulk particle| (n undefined)   | (anti/none)
  (R2) observed galaxy | YES (gauge-inv,  | YES      | bulk pode          | SPECTRAL EDGE   | anti-MOND
       = bulk particle  |  by propagation) | escapes  | (deep geodesic,    | (verified Step2)|
                        |                  |          |  large n)          |                 |
  (R3) strict a->0 /    | trivially singlet| trivially| AT the horizon     | SPECTRAL CENTER | MOND
       empty-Unruh-floor|  (identity-like) | (vacuum) | (n->0, zero chord) | (verified Step2)| (p=1/2)

KEY OBSERVATION: only R3 gives MOND, and R3 is the STRICT-HORIZON / VANISHING-BACKREACTION limit -- i.e.
the empty ensemble / Unruh-floor, which the PRIOR verdict already identified as 'rigorously the center'
(branch A) and which needs ZERO confinement input. The confinement result is about R1 vs R2 (the FINITE
backreacting probe). And for the finite probe, confinement gives EITHER:
   - confined (R1, generic) -> not even a bulk excitation, OR
   - escapes to the SPATIAL bulk pode (R2) -> the SPECTRAL EDGE -> anti-MOND.
NEITHER finite-probe branch lands at the spectral center. Only the strict-limit R3 does, and R3 is
just the empty ensemble re-labelled -- it does not need confinement and was already known.
"""
print("="*96)
print("NET-EFFECT TALLY: does Approach B (confinement) move the deep-MOND-sign verdict?")
print("="*96)

table = [
 ("R1 literal matter chord (generic)", "non-singlet", "CONFINED", "stretched horizon", "n/a (no bulk particle)", "no MOND"),
 ("R2 observed galaxy (bulk particle)", "singlet",     "ESCAPES",  "bulk pode (large n)", "SPECTRAL EDGE",        "anti-MOND"),
 ("R3 strict a->0 / empty Unruh-floor","trivial sing", "vacuum",   "at horizon (n~0)",    "SPECTRAL CENTER E=0",  "MOND p=1/2"),
]
print(f"\n  {'reading':<36}{'singlet?':<12}{'escape?':<9}{'spatial':<20}{'spectral':<22}{'sign'}")
for r in table:
    print(f"  {r[0]:<36}{r[1]:<12}{r[2]:<9}{r[3]:<20}{r[4]:<22}{r[5]}")

print("""
TALLY (both ways, no fudge):
  * Does confinement HELP the framework?  NO new help. The only MONDy branch is R3 = the strict-horizon
    empty-ensemble limit, which was ALREADY 'rigorously the center' (prior branch A) and needs NO
    confinement physics. Confinement adds nothing on the favorable side.
  * Does confinement HURT the framework?  It SHARPENS the obstruction for the FINITE backreacting probe:
    a generic chord is CONFINED (R1, melts, never a bulk particle), and even the escaping singlet (R2)
    lands at the SPATIAL bulk pode = the SPECTRAL EDGE (verified Step 2) -> anti-MOND. Both finite-probe
    branches are non-MOND. So confinement, taken literally, LEANS AGAINST for any finite-mass probe.
  * Is there a smuggle that would manufacture a win?  YES, and we caught it: 'singlet escapes to the
    CENTER' (conflating spatial pode with spectral E=0). Removing the smuggle removes the apparent win.

NET: Approach B does NOT produce a genuine internal closure. It REPRODUCES the prior structure --
  MOND only in the strict-center/empty-limit (which is a POSIT about where dS sits, equivalently the
  near-horizon a->0 limit), anti-MOND or no-probe for any finite backreacting object -- and adds a
  CONFIRMED reason (the spatial!=spectral center theorem) that the 'escape to the bulk' intuition does
  NOT rescue the sign. The deconfinement question is genuinely dynamical and answerable (R1 vs R2 is a
  real symmetry fork) but it decides SPATIAL escape, not the SPECTRAL placement the sign needs.

  LABEL: CONTESTED-TERMINAL (undecidable within DSSYK; the spectral placement is an external dS dictionary
  posit, NOT derivable from confinement). DIRECTION: the favorable reading requires re-smuggling
  center=MOND; on the literal finite-probe reading it LEANS AGAINST. This is consistent with the prior
  repo verdict (DEEP_MOND_SIGN_CENTER_VS_EDGE: OPEN_DECIDABLE, leaning against on the physical-probe
  reading) and shows Approach B (confinement) does NOT upgrade it to a closure -- contra the more
  optimistic KERNEL_RESULT note, whose 'forced for galaxies' rested on the diagonal-kernel TRANSPORT plus
  the UNDERIVED center placement, i.e. exactly the posit confinement was supposed to (but cannot) replace.
""")
