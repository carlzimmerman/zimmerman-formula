#!/usr/bin/env python3
"""
Framework vs Maeder SIV -- the decisive, calculation-backed comparison (and what the data say).
==============================================================================================
Carl: "lock this down with more real calculations and evidence." Maeder's Scale-Invariant Vacuum (SIV)
is the closest GEOMETRIC cousin -- it contains MOND and predicts a0 evolves. The question is whether it
is secretly the same physics as a0=(c/2)sqrt(G rho)=cH/Z. Answer, by calculation: NO. They tie a0 to
OPPOSITE cosmological clocks and so predict OPPOSITE z-trends; the current a0(z) data favor the
framework; and a z~3 point is decisive. Literature: SIV a0(z) is Eq.16 of arXiv:2409.11425
(MNRAS-L 535, L13, 2024); 'MOND as a peculiar case of SIV', MNRAS 520, 1447 (2023). Needs numpy.
"""
import numpy as np

Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)                          # framework: a0 prop H(z)
siv = lambda z: (1+z)**-1.5 * ((1-Om)/(1+z)**1.5 + Om)**(-4/3.)  # SIV Eq.16: a0 prop vacuum age


def part1_structural():
    print("="*90); print("PART 1 [STRUCTURAL] -- same physics? NO: opposite cosmological clocks"); print("="*90)
    print("""  framework:  a0 = (c/2) sqrt(G rho_crit),  rho_crit prop H^2  =>  a0 prop H(z).
              matter era H prop 1/t  =>  a0 prop 1/t  =>  a0 was HIGHER in the past (denser/faster).
  SIV:        a0 prop the scale-invariant vacuum term; Eq.16 at high z -> a0 prop (1+z)^-3/2 prop t,
              =>  a0 prop cosmic AGE t  =>  a0 was LOWER in the past (vacuum scale grows with age).
  Both calibrate to the SAME a0 at z=0 (a0~cH/6: framework Z=5.79, SIV 2pi=6.28) -- but the SLOPES are
  equal and OPPOSITE:""")
    print(f"    {'z':>4}{'framework slope':>18}{'SIV slope':>12}   (d ln a0 / d ln(1+z))")
    for z in (1, 2, 3, 4):
        dF = (np.log(E(z+1e-3))-np.log(E(z)))/(np.log(1+z+1e-3)-np.log(1+z))
        dS = (np.log(siv(z+1e-3))-np.log(siv(z)))/(np.log(1+z+1e-3)-np.log(1+z))
        print(f"    {z:>4}{dF:>+18.2f}{dS:>+12.2f}")
    print("""  => the framework anchors a0 to the INSTANTANEOUS expansion/density (H, ~1/t); SIV to the vacuum
     AGE (~t). They are genuinely DIFFERENT theories -- not one with a different O(1) coefficient.\n""")


def part2_evidence():
    print("="*90); print("PART 2 [EVIDENCE] -- fit framework / SIV / constant to the real a0(z) data"); print("="*90)
    # a0 in 1e-10 (z, value, sigma): SPARC z=0 anchor; Varasteanu 2025 z=0.05; MUSE-DARK III 2026 z=0.9
    data = [(0.00, 1.36, 0.20), (0.05, 1.69, 0.13), (0.90, 2.38, 0.11)]
    z = np.array([d[0] for d in data]); a = np.array([d[1] for d in data]); s = np.array([d[2] for d in data])
    print(f"  data: a0(z=0)=1.36+/-0.20 (SPARC), a0(0.05)=1.69+/-0.13 (Varasteanu), a0(0.9)=2.38+/-0.11 (MUSE-DARK)")
    print(f"  {'model':18}{'best A[e-10]':>13}{'chi^2 (2 dof)':>15}{'pred a0(0.9)':>14}")
    res = {}
    for name, f in [("framework E(z)", E), ("constant", lambda z: 1.0), ("SIV (decreasing)", siv)]:
        fz = np.array([f(zi) for zi in z])
        A = np.sum(a*fz/s**2)/np.sum(fz**2/s**2)
        chi2 = np.sum(((a - A*fz)/s)**2); res[name] = chi2
        print(f"  {name:18}{A:>13.2f}{chi2:>15.2f}{A*f(0.9):>14.2f}")
    dchi = res["SIV (decreasing)"] - res["framework E(z)"]
    print(f"""
  => the data RISE (1.36 -> 1.69 -> 2.38). The framework (rise) fits at chi^2~3; constant (flat) and SIV
     (fall) are excluded at chi^2~28 and ~64. Framework is favoured over SIV by dchi^2~{dchi:.0f}.
  HONEST CAVEATS (do not skip): (i) this rests heavily on the single z=0.9 MUSE-DARK point; drop it and
  the lever arm collapses to ~1 sigma (the session's standing caveat). (ii) the framework's own chi^2~3
  is not perfect -- the z=0.05 point sits high (the ~1.7 sigma local-pair M/L systematic). (iii) the SIV
  authors read OTHER compilations as ~flat; the high-z a0 data are sparse and genuinely contested. So:
  SUGGESTIVE and pointing the framework's way, NOT yet decisive.\n""")


def part3_decisive():
    print("="*90); print("PART 3 [DECISIVE TEST] -- z~3 separates all three by ~10x"); print("="*90)
    print(f"  {'z':>4}{'framework E(z)':>16}{'SIV':>10}{'constant':>10}")
    for z in (0, 1, 2, 3, 4):
        print(f"  {z:>4}{E(z):>16.2f}{siv(z):>10.2f}{1.0:>10.1f}")
    print(f"""
  => at z=3: a0(3)/a0(0) = {E(3):.2f} (framework) vs {siv(3):.2f} (SIV) vs 1.0 (constant) -- ~{E(3)/siv(3):.0f}x and
     OPPOSITE-direction spread. The tightened z~3 proposal (~13-16 sigma vs constant on a tight anchor)
     resolves framework-vs-SIV even more cleanly, since SIV sits BELOW constant: distinguishing the
     framework (4.6) from SIV (0.42) is an even larger signal than from constant (1.0).\n""")


def verdict():
    print("="*90); print("VERDICT"); print("="*90)
    print("""  * NOT the same physics: framework ties a0 to H(z) (~1/t), SIV to the vacuum age (~t) -- equal and
    OPPOSITE z-slopes. A genuinely distinct, named geometric rival, sharing only the z=0 value.
  * The current a0(z) data favour the framework's INCREASE (chi^2 3.0) over constant (27.8) and SIV
    (64.3) -- suggestive, single-point-driven, and contested by other compilations. Not decisive.
  * z~3 is decisive and now a 3-WAY discriminator (framework 4.6 / constant 1.0 / SIV 0.42). The
    framework makes the boldest, most falsifiable prediction; SIV the opposite; constant the null.
  * NET GAIN from Carl's question: the distinctive claim sharpens from 'a0 evolves' (shared) to 'a0
    INCREASES as E(z), opposite to the leading geometric competitor', with the data leaning the
    framework's way and a clean decisive test on the table. The framework is now properly situated in,
    and distinguished from, the real geometric-MOND literature.""")
    print("="*90)


def main():
    print("#"*90); print("# FRAMEWORK vs MAEDER SIV -- decisive comparison with real calculations + data"); print("#"*90 + "\n")
    part1_structural(); part2_evidence(); part3_decisive(); verdict()


if __name__ == "__main__":
    main()
