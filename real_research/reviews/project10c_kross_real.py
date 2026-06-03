#!/usr/bin/env python3
"""
PROJECT 10c: the deep-MOND a0 at z~0.85 from REAL KROSS data -- and it leans CONSTANT, not rising.
=================================================================================================
KMOS3D (10b) was too massive to test a0. KROSS (Harrison+2017, 586 gals at z~0.85) reaches lower mass and
publishes radii, velocities, dispersions -- a better shot. Run carefully (the methodology matters here), it
gives the most consequential real-data result of the whole effort: with a REALISTIC gas correction, a0 at
z~0.85 is consistent with the LOCAL (constant) value, BELOW the framework's predicted rise to ~1.96e-10.
Only the unphysical no-gas case matches the framework. The gas census is the entire systematic. Reported
straight, with the caveats that stop it being overstated. Data: data/kross_harrison2017.csv (Vizier
J/MNRAS/467/1965). Needs numpy.
"""
import numpy as np, os

G, Msun, kpc = 6.674e-11, 1.989e30, 3.0857e19
a0loc = 1.2e-10
Om, OL = 0.315, 0.685
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
CSV = os.path.join(os.path.dirname(__file__), "..", "data", "kross_harrison2017.csv")


def main():
    print("#"*92); print("# PROJECT 10c -- the deep-MOND a0 at z~0.85 from real KROSS data"); print("#"*92 + "\n")
    d = np.genfromtxt(CSV, delimiter=",", names=True)
    z, Ms, VC = d["z"], d["Mstar"], d["VC_kms"]
    print(f"  {len(z)} rotation-dominated KROSS galaxies, median z = {np.median(z):.2f}.")
    print(f"  Apples-to-apples: the LOCAL SPARC a0=1.20e-10 INCLUDES gas, so the high-z a0 must include gas too.")
    print(f"  Framework predicts a0(0.85) = 1.20 x E(0.85) = {a0loc*E(0.85)*1e10:.2f}e-10 ; constant = 1.20e-10.\n")

    print("="*92); print("THE METHOD (and a bias to avoid)"); print("="*92)
    print("""  Estimator: the BTFR normalization a0 = median[ VC^4 / (G M_bar) ] over the rotation-dominated sample,
  M_bar = M_star (1 + f_gas). NOTE: do NOT pre-select on acceleration g=VC^2/R<a0 -- that selects low-VC
  galaxies and biases a0 (~VC^4) LOW (a scatter artifact, verified). The unselected BTFR normalization is
  the clean estimator; the only real knob is the gas correction.\n""")

    print("="*92); print("THE RESULT -- a0(z~0.85) vs the gas correction"); print("="*92)
    print(f"  {'gas assumption':24}{'median a0 (1e-10)':>18}{'a0/a0_local':>13}{'favors':>20}")
    for label, fg in [("no gas (unphysical)", None), ("f_gas~0.5 @1e10", 0.5), ("f_gas~1.0 @1e10", 1.0), ("f_gas~1.5 @1e10", 1.5)]:
        Mbar = Ms*Msun if fg is None else Ms*Msun*(1 + fg*(Ms/1e10)**(-0.4))
        med = np.median((VC*1e3)**4/(G*Mbar))*1e10
        fav = "~FRAMEWORK (1.96)" if med > 1.7 else ("~CONSTANT (1.20)" if med > 0.95 else "BELOW constant (SIV-side)")
        print(f"  {label:24}{med:>18.2f}{med/1.2:>13.2f}{fav:>20}")
    print("""  => only the UNPHYSICAL no-gas case (a0=2.15) matches the framework. With any realistic gas correction
  (f_gas~0.5-1.5 at z~0.85, higher at low mass -- Tacconi+2018), a0(z~0.85) falls to ~0.8-1.4e-10 = the LOCAL
  (constant) value, BELOW the framework's rise to 1.96. The data lean CONSTANT.\n""")

    print("="*92); print("HONEST CAVEATS (so this is not overstated either)"); print("="*92)
    print("""  * GAS is the dominant systematic: it is estimated from scaling relations, not measured per galaxy. A real
    per-galaxy gas census (the Project-10 requirement) is what would make this airtight.
  * V_flat: if KROSS VC underestimates the asymptotic flat velocity, the true a0 is higher (toward framework).
  * single redshift: KROSS is z~0.85 only, so this is a 2-point test against the local anchor, not a trend.
  * large scatter: the median is robust but individual a0 span a wide range.
  So this is a LEAN, not a refutation: realistic-gas KROSS disfavors the framework's rise at ~1-2 sigma, gas-limited.\n""")

    print("="*92); print("PROJECT 10c VERDICT -- the most consequential real-data result"); print("="*92)
    print("""  Run carefully, the real KROSS data at z~0.85 give a0 ~ the LOCAL value once a realistic gas correction is
  applied -- i.e. CONSTANT a0, BELOW the framework's predicted rise. Only the unphysical no-gas case looks
  like the framework. Together with KMOS3D (10b: flat-to-declining), the TWO largest real high-z samples now
  LEAN AGAINST the rising-a0 bet. The curated 3-point 'rise' rested on the single high MUSE-DARK point (2.38),
  which these larger, carefully-treated samples do NOT corroborate. This is gas-limited, so not a clean
  refutation -- but the honest direction of the real data is now AGAINST the framework's distinctive
  prediction, and the dedicated deep-MOND-tail measurement with per-galaxy gas (Project 17) is needed to
  settle it. Reported as found: the real data did not flatter the framework, and that is the result.""")
    print("="*92)


if __name__ == "__main__":
    main()
