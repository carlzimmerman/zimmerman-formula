#!/usr/bin/env python3
"""
THE TOE BOUNDARY, TESTED: is the framework's signature number Z = sqrt(32*pi/3)
structurally reachable from Standard-Model flavor data, or number-field-walled?

A genuine "theory of everything" built on a0 = c^2 sqrt(Lambda/32pi) would need its
signature constant Z (equivalently the a0/cH ratio) to appear in an SM relation --
a mass ratio, a mixing angle, the Koide relation. This script tests, honestly and
falsifiably, whether such a bridge exists at LOW complexity (a real structural link)
or only at absurd height (a numerical coincidence = no bridge).

Method: integer-relation search (PSLQ, mpmath) between Z and the actual SM flavor
observables. PSLQ ALWAYS finds a relation eventually for real numbers; the honest
discriminator is the HEIGHT (max |integer coefficient|) of the smallest relation.
A genuine physical identity has small height (like Koide's 2/3, height 3). A height
of thousands+ means the numbers are structurally unrelated -- the bridge is a mirage.

Also: the number-field obstruction, stated exactly. Z = sqrt(32/3)*sqrt(pi). sqrt(pi)
is transcendental (Lindemann: pi transcendental => sqrt(pi) transcendental). Every SM
flavor observable that anyone derives (Koide Q=2/3, charged-lepton mass ratios as
algebraic roots) lives in the field of algebraic numbers Q-bar. A transcendental
cannot equal an algebraic number, nor satisfy a finite integer relation WITH ONLY
algebraic partners unless the transcendental part cancels -- and pi cannot cancel
against algebraic data. So the bridge is obstructed at the level of number fields,
not merely unfound. The PSLQ height is the empirical face of that theorem.
"""
import mpmath as mp
mp.mp.dps = 60

# ---- the framework's signature number ----
Z   = mp.sqrt(mp.mpf(32)/3 * mp.pi)          # = sqrt(32 pi/3) ~ 5.789
pi  = mp.pi

# ---- actual SM flavor observables (PDG central values) ----
me  = mp.mpf('0.51099895000')   # MeV
mmu = mp.mpf('105.6583755')
mtau= mp.mpf('1776.86')
Koide = (me+mmu+mtau) / (mp.sqrt(me)+mp.sqrt(mmu)+mp.sqrt(mtau))**2   # ~ 0.6667
r_mu_e   = mmu/me            # ~ 206.77
r_tau_mu = mtau/mmu          # ~ 16.82
# Cabibbo angle sin^2, Weinberg angle sin^2 (dimensionless SM inputs) -- PRECISE, not rounded
sin2C = mp.sin(mp.mpf('0.22736'))**2   # theta_C=13.02 deg -> sin^2 ~ 0.05098 (NOT 1/20)
sin2W = mp.mpf('0.231220')             # weak mixing angle (PDG)

def smallest_relation(vals, names, maxcoeff=10**6, require_first_nonzero=False):
    """PSLQ with a height cap. Return (rel, height). If require_first_nonzero, a
       relation whose FIRST coefficient (on Z) is 0 does NOT count as a Z-bridge:
       Z has dropped out, so it is a relation among the OTHER numbers only."""
    rel = mp.pslq(vals, maxcoeff=maxcoeff, maxsteps=10**5)
    if rel is None:
        return None, None
    if require_first_nonzero and rel[0] == 0:
        return ("Z-coeff=0 (spurious: "+str(rel)+")"), None   # Z absent => not a bridge
    height = max(abs(c) for c in rel)
    return rel, height

if __name__ == "__main__":
    print("="*74)
    print("THE TOE BOUNDARY: is Z = sqrt(32 pi/3) reachable from SM flavor data?")
    print("="*74)
    print(f"  Z          = {mp.nstr(Z, 12)}   (= sqrt(32/3)*sqrt(pi), sqrt(pi) transcendental)")
    print(f"  Koide Q    = {mp.nstr(Koide, 12)}   (algebraic target 2/3 = {mp.nstr(mp.mpf(2)/3,12)})")
    print(f"  m_mu/m_e   = {mp.nstr(r_mu_e, 12)}")
    print(f"  m_tau/m_mu = {mp.nstr(r_tau_mu, 12)}")
    print()

    # CALIBRATION: what a REAL small-height identity looks like -- ideal Koide 2/3.
    rel, h = smallest_relation([mp.mpf(2)/3, mp.mpf(1)], ["2/3","1"], maxcoeff=10**4)
    print(f"  CALIBRATION -- ideal Koide 2/3 vs 1: relation {rel}, height {h}")
    print(f"    (a genuine identity 3*(2/3) - 2 = 0 has height ~3. THIS is what a bridge looks like.)\n")

    # THE TEST: does Z bridge to each SM observable at LOW height, with Z actually present?
    print("  BRIDGE TEST -- smallest integer relation [Z, SM, 1] with Z-coeff NONZERO:")
    targets = [("Koide Q", Koide), ("m_mu/m_e", r_mu_e), ("m_tau/m_mu", r_tau_mu),
               ("sin^2 theta_C", sin2C), ("sin^2 theta_W", sin2W)]
    heights = []
    for name, val in targets:
        rel, h = smallest_relation([Z, val, mp.mpf(1)], ["Z", name, "1"],
                                   maxcoeff=10**7, require_first_nonzero=True)
        heights.append(h if h else float('inf'))
        verdict = "NO BRIDGE (Z-coeff 0 or height huge)" if (h is None or h > 1000) \
                  else "*** LOW-HEIGHT Z-LINK -- INVESTIGATE ***"
        print(f"    Z, {name:14s}, 1 : {str(rel):40s} height={h}   {verdict}")
    print()

    # THE OBSTRUCTION, made explicit: strip pi and ask if the ALGEBRAIC part bridges.
    # Z^2 = 32 pi/3 is transcendental; Z^2 * 3/(32) = pi. If any SM number bridged to Z,
    # it would express pi algebraically in flavor data. Test Z vs pi (must be tiny height):
    rel, h = smallest_relation([Z*Z, pi], ["Z^2","pi"], maxcoeff=10**3)
    print(f"  SANITY -- Z^2 vs pi: rel={rel}, height={h}  (must be small: Z^2 = (32/3) pi exactly)")
    print(f"    => Z carries pi. A bridge to algebraic SM data would express pi in flavor")
    print(f"       observables -- impossible (Lindemann). The wall is a NUMBER-FIELD theorem.\n")

    minh = min(heights)
    print("="*74)
    if minh > 1000:
        print(f"VERDICT: NO SM BRIDGE. Smallest Z<->SM relation height = {minh:.3g} (>>3 = a")
        print(f"  physical identity's height). Z is number-field-isolated from SM flavor data:")
        print(f"  Z in Q(sqrt(pi)) (transcendental), flavor observables in Q-bar (algebraic).")
        print(f"  The TOE bridge is WALLED by a theorem, not merely unfound. The framework is")
        print(f"  a complete ONE-parameter theory of the a0 scale -- not a zero-parameter TOE.")
    else:
        print(f"VERDICT: a low-height Z<->SM link exists (height {minh}) -- INVESTIGATE (a real lead).")
    print("="*74)
