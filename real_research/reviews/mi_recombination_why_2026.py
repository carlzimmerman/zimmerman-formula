#!/usr/bin/env python3
r"""mi_recombination_why_2026.py -- WHY does matter recombine when it does?

Carl's question. The naive answer -- "when kT drops below hydrogen's 13.6 eV binding energy" --
is WRONG BY A FACTOR OF ~50, and the reason is one of the nicest facts in cosmology. This computes
the real answer in four escalating steps, each closer to the truth:

  S1  NAIVE: kT = 13.6 eV  ->  T ~ 158,000 K  ->  z ~ 58,000.  Off by ~50x. Why?
  S2  THE PHOTON-TO-BARYON RATIO. There are ~1.6 billion photons per baryon. A blackbody has an
      exponential high-energy TAIL, so even when the AVERAGE photon is far below 13.6 eV, the tail
      still holds enough ionizing photons to keep hydrogen ionized. Recombination waits until the
      TAIL population drops below the baryon density.
  S3  SAHA EQUILIBRIUM, the proper statistical-mechanics answer, including the electron phase-space
      factor. Gives the half-ionization redshift.
  S4  WHY EVEN SAHA IS NOT ENOUGH, and what CAMB/RECFAST actually gives: the 2s->1s two-photon
      bottleneck. Direct recombination to the ground state emits a 13.6 eV photon that promptly
      re-ionizes a neighbour, so net recombination is throttled by a SLOW forbidden transition
      (Lambda_2s1s ~ 8.2 s^-1). This delays and smears last scattering.

AND THE HONEST a0 CONNECTION: none. Recombination is set by ATOMIC physics (13.6 eV, m_e) and the
BARYON ASYMMETRY (eta), not by geometry or by a0. But it matters for the framework anyway, because
the CMB constraint on a0(z) is evaluated AT z_star -- so that constraint inherits z_star from
atomic physics, and it is worth knowing that number is not ours to adjust.

Exit 0 = ran. No hard-coded verdicts.
"""
from __future__ import annotations
import math

KB = 1.380649e-23
HBAR = 1.054571817e-34
H_PL = 6.62607015e-34
ME = 9.1093837015e-31
C = 2.99792458e8
EV = 1.602176634e-19
E_ION = 13.5984 * EV            # hydrogen ground-state binding energy
T_CMB = 2.7255                  # K today
ETA = 6.12e-10                  # baryon-to-photon ratio (Planck/BBN)

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK  ' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 98); print(s); print("=" * 98)


def n_gamma(T):
    """blackbody number density: 16 pi zeta(3) (kT/hc)^3 ... standard 2.404/pi^2 form."""
    return 2.4041 / math.pi**2 * (KB * T / (HBAR * C)) ** 3


def saha_x(T, eta=ETA):
    """Saha ionization fraction x=n_e/n_H from x^2/(1-x) = (1/n_b)(m_e kT/2 pi hbar^2)^{3/2} e^{-E/kT}."""
    n_b = eta * n_gamma(T)
    rhs = (ME * KB * T / (2 * math.pi * HBAR**2)) ** 1.5 * math.exp(-E_ION / (KB * T)) / n_b
    # solve x^2/(1-x) = rhs  ->  x = (-rhs + sqrt(rhs^2+4 rhs))/2
    return (-rhs + math.sqrt(rhs * rhs + 4 * rhs)) / 2


def main() -> int:
    banner("S1. THE NAIVE ANSWER, and how badly it fails")
    T_naive = E_ION / KB
    z_naive = T_naive / T_CMB - 1
    print(f"  'recombine when kT = 13.6 eV':  T = {T_naive:.0f} K  ->  z = {z_naive:.0f}")
    print(f"  ACTUAL last scattering:         T ~ 2970 K      ->  z ~ 1090")
    print(f"  the naive answer is off by a factor of {T_naive/2970:.0f} in temperature.")
    check(T_naive / 2970 > 40, "the naive binding-energy estimate is ~50x too hot")

    banner("S2. WHY: there are ~1.6 BILLION photons per baryon, and blackbodies have tails")
    T_rec = 2970.0
    ng = n_gamma(T_rec)
    nb = ETA * ng
    print(f"  baryon-to-photon ratio eta = {ETA:.2e}   ->  {1/ETA:.2e} photons per baryon")
    print(f"  at T = {T_rec:.0f} K:  n_gamma = {ng:.3e} m^-3,  n_baryon = {nb:.3e} m^-3")
    print(f"  mean photon energy ~ 2.7 kT = {2.7*KB*T_rec/EV:.3f} eV  -- far below 13.6 eV")
    print(f"  BUT the fraction of photons above 13.6 eV is ~ exp(-E/kT) = "
          f"{math.exp(-E_ION/(KB*T_rec)):.2e}")
    print(f"  ionizing photons per baryon at 2970 K = (1/eta)*exp(-E/kT) = "
          f"{math.exp(-E_ION/(KB*T_rec))/ETA:.2e}")
    print("  THE POINT: hydrogen stays ionized while there is >~1 ionizing photon per atom.")
    print("  Because photons outnumber baryons a BILLION to one, the exponential tail keeps that")
    print("  supply up long after the AVERAGE photon is harmless. The crossover -- where ionizing")
    print("  photons per baryon falls through 1 -- is at:")
    T_tail = E_ION / (KB * math.log(1 / ETA))
    print(f"    exp(-E/kT) = eta  ->  kT = E/ln(1/eta):  T = {T_tail:.0f} K (z ~ {T_tail/T_CMB-1:.0f})")
    print(f"  That single fact carries us from 158,000 K down to {T_tail:.0f} K -- a factor "
          f"{T_naive/T_tail:.0f}.")
    print(f"  It does NOT get us all the way to 2970 K (at 2970 K the ratio is already ~1e-14,")
    print(f"  i.e. long past the crossover). The remaining factor of ~{T_tail/2970:.1f} comes from")
    print("  S3 (electron phase space) and S4 (the two-photon bottleneck).")
    check(2000 < T_tail < 12000,
          "the photon/baryon tail criterion lands at ~7400 K -- most of the way, not all")

    banner("S3. SAHA EQUILIBRIUM -- the proper answer, with electron phase space")
    print(f"  x^2/(1-x) = (1/n_b) (m_e kT / 2 pi hbar^2)^{{3/2}} exp(-E_ion/kT)")
    print(f"  {'T (K)':>9}{'z':>8}{'kT (eV)':>10}{'x_e (Saha)':>13}")
    for T in (6000, 5000, 4500, 4000, 3700, 3400, 3000, 2700, 2500):
        x = saha_x(T)
        print(f"  {T:>9}{T/T_CMB-1:>8.0f}{KB*T/EV:>10.4f}{x:>13.4f}")
    # find x=0.5
    lo, hi = 2000.0, 8000.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if saha_x(mid) > 0.5: hi = mid
        else: lo = mid
    T_half = 0.5 * (lo + hi)
    print(f"\n  Saha half-ionization (x=0.5):  T = {T_half:.0f} K  ->  z = {T_half/T_CMB-1:.0f}")
    check(3000 < T_half < 5500, "Saha x=0.5 lands near T ~ 3700-4500 K, z ~ 1300-1600")
    print("  Note the transition is SHARP in temperature -- x_e falls from ~1 to ~0 over a narrow")
    print("  range -- because of the exponential. That sharpness is why the CMB is a thin shell")
    print("  and the acoustic peaks are crisp rather than smeared away.")

    banner("S4. WHY SAHA IS STILL NOT THE FINAL ANSWER: the two-photon bottleneck")
    print("  Saha assumes full thermal equilibrium. Real recombination is RATE-LIMITED:")
    print("   * an electron falling DIRECTLY to the 1s ground state emits a 13.6 eV photon, which")
    print("     immediately ionizes a neighbouring atom -- net progress zero.")
    print("   * so atoms must instead reach the ground state via the 2s -> 1s TWO-PHOTON")
    print("     transition, which is FORBIDDEN to first order and therefore slow:")
    print("       Lambda_2s->1s ~ 8.22 s^-1   (vs ~1e8 s^-1 for an allowed transition)")
    print("   * Lyman-alpha photons must also redshift out of resonance to escape.")
    print("  Consequence: recombination FREEZES OUT with a residual ionization x_e ~ 1e-4 - 1e-3")
    print("  rather than going to zero, and last scattering (optical depth = 1) is pushed LATER")
    print("  and SMEARED into a shell of finite thickness (~20 Mpc, Delta z ~ 100).")
    try:
        import camb
        pars = camb.set_params(H0=67.36, ombh2=0.02237, omch2=0.1200, tau=0.0544,
                               ns=0.9649, As=2.1e-9, mnu=0.06)
        res = camb.get_background(pars)
        d = res.get_derived_params()
        print(f"\n  CAMB/RECFAST (the real, rate-limited calculation):")
        print(f"    z_star (last scattering) = {d['zstar']:.2f}   "
              f"T_star = {T_CMB*(1+d['zstar']):.0f} K")
        print(f"    thickness Delta z_star   = {d.get('zdrag', float('nan')) - d['zstar']:+.1f} "
              f"(z_drag - z_star; baryons decouple slightly later)")
        print(f"    r_star (sound horizon)   = {d['rstar']:.2f} Mpc")
        check(1050 < d['zstar'] < 1120, "CAMB/RECFAST z_star ~ 1090, LATER than Saha's ~1400")
        print(f"  So: Saha z ~ {T_half/T_CMB-1:.0f}  ->  RECFAST z_star = {d['zstar']:.0f}. The")
        print(f"  two-photon bottleneck delays it by ~{T_half/T_CMB-1-d['zstar']:.0f} in redshift.")
    except Exception as e:
        print(f"  (CAMB unavailable here: {type(e).__name__}) -- known value: z_star ~ 1090.")

    banner("WHAT ACTUALLY SETS THE RECOMBINATION EPOCH -- and the honest a0 answer")
    print("  Three numbers, none of them cosmological geometry:")
    print(f"   1. E_ion = 13.6 eV     -- ATOMIC physics (m_e alpha^2/2), sets the scale")
    print(f"   2. eta = {ETA:.2e}   -- the BARYON ASYMMETRY, delays it by ~50x")
    print(f"   3. Lambda_2s1s = 8.22 s^-1 -- a FORBIDDEN-transition rate, delays and smears it")
    print("  Expansion rate H(z) enters only by setting how fast the temperature falls (and hence")
    print("  how far the freeze-out overshoots equilibrium) -- it does not set the temperature.")
    print()
    print("  a0 HAS NOTHING TO DO WITH IT. Recombination is atomic physics plus baryogenesis, and")
    print("  a0 is a late-time gravitational scale. Stated plainly rather than forced.")
    print("  BUT IT MATTERS FOR THE FRAMEWORK INDIRECTLY: the CMB constraint on a0(z) is")
    print("  evaluated AT z_star, and z_star is fixed by the three numbers above. So that")
    print("  constraint inherits z_star from atomic physics -- it is not a knob we can turn to")
    print("  make the rising footing survive. That is why the ~52 sigma exclusion is robust:")
    print("  the epoch it is evaluated at is set by 13.6 eV and eta, not by anything adjustable")
    print("  in the framework.")
    print("=" * 98)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
