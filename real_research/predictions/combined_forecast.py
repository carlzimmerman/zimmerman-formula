#!/usr/bin/env python3
"""
COMBINED FORECAST -- joint statistical reach of the four channels on the a0-evolution law.
==========================================================================================
Synthesis of Doors 1-4. We collapse the whole framework's distinctive content to a SINGLE number and ask how well
the combined data can measure it.

Parametrize the evolution by a strength exponent beta:
        a0(z) = a0(0) * [ rho_DE(z)/rho_DE0 ] ^ (beta/2).
    beta = 1  ->  a0 ~ sqrt(rho_DE)         (THE FRAMEWORK)
    beta = 0  ->  a0 = const                (ordinary MOND -- the null; the framework's distinctive content vanishes)
    beta = 2  ->  a0 ~ rho_DE               (steeper)
The whole empirical question 'does a0 track dark energy?' becomes 'is beta = 1, and is it != 0?'

Each channel's observable O scales as a power of a0:  O ~ a0^p, so  ln O(z)/O(0) = (beta * p / 2) * ln[rho_DE ratio].
    Door 4  MDAR deep-MOND discrepancy  D    ~ a0^(1/2)   p = 1/2
    Door 1  lensing saturated deflection a*  ~ a0^(1/2)   p = 1/2
    Door 3  BTFR rotation speed          V   ~ a0^(1/4)   p = 1/4
    Door 2  dwarf dispersion             sig ~ a0^(1/4)   p = 1/4   (but z=0 only -> anchors, does not test evolution)

Fisher information on beta from N measurements at redshift z with per-measurement precision sigma (in dex of O):
    dlnO/dbeta = (p/2) ln[rho_DE ratio(z)]   ;   F = N * (dlnO/dbeta)^2 / (sigma*ln10)^2
The detection significance of the framework (beta=1) over the null (beta=0) is  nsigma = 1 / sigma(beta) = sqrt(F_total).

KEY HONEST RESULT (falls out of the numbers, not assumed): because rho_DE is nearly constant out to z~1 (it even
peaks near z~0.4), the lever arm ln[rho_DE ratio] is tiny below z~2. ESSENTIALLY ALL the evolution-constraining
power lives at z > 2. The low-z channels (dwarfs, local lensing, the SPARC RAR) do NOT test the evolution -- their
job is to pin a0(0) so the high-z offset is measured against a rock-solid anchor.

This is a FORECAST with explicit, labeled survey assumptions -- not a claim about data in hand. Calibrated against the
independent Monte Carlo (z3_bridge_forecast_mc.py: 30 discs @ z=3, 0.06 dex -> 3 sigma). Reproducible: `python combined_forecast.py`.
"""
import numpy as np

MPC = 3.0857e22; H0 = 67.4e3 / MPC; C = 2.99792458e8; OmL = 0.685
W0, WA = -0.752, -0.86
LN10 = np.log(10.0)


def rho_DE_ratio(z):
    a = 1.0 / (1.0 + z)
    return a**(-3 * (1 + W0 + WA)) * np.exp(-3 * WA * (1 - a))


def lever(z):
    """The evolution lever arm at redshift z: |ln[rho_DE(z)/rho_DE0]|."""
    return abs(np.log(rho_DE_ratio(z)))


def fisher(N, z, sigma_dex, p):
    """Fisher information on beta from N measurements at z, precision sigma_dex (dex), channel power p."""
    dlnO_dbeta = 0.5 * p * np.log(rho_DE_ratio(z))      # natural log
    return N * dlnO_dbeta**2 / (sigma_dex * LN10)**2


def main():
    print("#" * 102)
    print("# COMBINED FORECAST -- joint reach of the four channels on the evolution strength beta (1=framework, 0=null)")
    print("#" * 102 + "\n")

    # ---- calibration check against the independent MC ----
    F = fisher(30, 3.0, 0.06, p=0.25)
    print(f"  CALIBRATION: 30 BTFR discs @ z=3, 0.06 dex (p=1/4)  ->  {np.sqrt(F):.1f} sigma on beta")
    print(f"               (independent Monte Carlo z3_bridge_forecast_mc.py gives ~3 sigma -- consistent.)\n")

    # ---- the lever arm: where the signal lives ----
    print("=" * 102)
    print("(1) THE LEVER ARM |ln(rho_DE ratio)| -- the evolution signal is negligible below z~2")
    print("=" * 102)
    print(f"   {'z':>6}{'rho_DE(z)/rho_DE0':>20}{'lever arm':>12}{'BTFR offset (beta=1)':>22}")
    for z in (0.4, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0):
        off = (rho_DE_ratio(z)**0.125 - 1) * 100       # BTFR V offset: V ~ a0^(1/4), a0 ~ rho_DE^(1/2) -> V ~ rho_DE^(1/8)
        print(f"   {z:>6.1f}{rho_DE_ratio(z):>20.3f}{lever(z):>12.3f}{off:>20.1f}%")
    print("   -> a BTFR survey at z=5 is worth ~(lever_5/lever_3)^2 = "
          f"{(lever(5.0)/lever(3.0))**2:.1f}x as many galaxies at z=3. Fewer, higher-z discs win.\n")

    # ---- per-channel forecast at plausible survey depths ----
    print("=" * 102)
    print("(2) PER-CHANNEL reach (each alone), with explicit, labeled survey assumptions")
    print("=" * 102)
    channels = [
        ("Door 3  BTFR (high-z discs)",      0.25, 50, 3.5, 0.06, "JWST/ALMA resolved kinematics, z~3-4"),
        ("Door 4  resolved RAR (high-z)",    0.50, 30, 3.0, 0.12, "full rotation-curve RAR at z~3 (p=1/2, but noisier)"),
        ("Door 1  lensing amplitude",        0.50,  6, 1.0, 0.05, "stacked weak lensing in z-bins, z~0.3-1 (small lever)"),
        ("Door 2  dwarf dispersions",        0.25, 30, 0.0, 0.10, "z=0 only -> ANCHOR, no evolution lever"),
    ]
    print(f"   {'channel':<32}{'p':>5}{'N':>5}{'z':>6}{'sig(dex)':>10}{'sigma(beta)':>13}{'n_sigma':>9}")
    Ftot = 0.0
    for name, p, N, z, sig, note in channels:
        F = fisher(N, z, sig, p) if z > 0 else 0.0
        Ftot += F
        sb = (1 / np.sqrt(F)) if F > 0 else np.inf
        ns = np.sqrt(F)
        print(f"   {name:<32}{p:>5.2f}{N:>5d}{z:>6.1f}{sig:>10.2f}{sb:>13.2f}{ns:>9.1f}")
    print(f"   {'-'*92}")
    print(f"   {'COMBINED (Fisher sum)':<32}{'':>5}{'':>5}{'':>6}{'':>10}{1/np.sqrt(Ftot):>13.2f}{np.sqrt(Ftot):>9.1f}")
    print(f"\n   note: dwarfs and local lensing add ~0 to the EVOLUTION constraint (small/zero lever) but pin a0(0).")
    print(f"   The combined reach is carried by the high-z channels; the low-z ones make the anchor exact.\n")

    # ---- scenarios: current -> near-term -> decisive ----
    print("=" * 102)
    print("(3) SCENARIOS for the make-or-break high-z BTFR channel (Door 3)")
    print("=" * 102)
    print(f"   {'scenario':<40}{'N':>5}{'z':>6}{'sig':>7}{'n_sigma':>9}{'verdict':>16}")
    for name, N, z, sig in [
        ("existing samples (z~1-2.5, small lever)", 28, 2.0, 0.08, ),
        ("near-term: 30 discs @ z~3",              30, 3.0, 0.07, ),
        ("JWST/ALMA campaign: 60 @ z~3-4",         60, 3.5, 0.06, ),
        ("decisive: 40 @ z~3 + 25 @ z~5",          None, None, None),
    ]:
        if N is None:
            F = fisher(40, 3.0, 0.06, 0.25) + fisher(25, 5.0, 0.06, 0.25)
        else:
            F = fisher(N, z, sig, 0.25)
        ns = np.sqrt(F)
        verdict = "DISCOVERY" if ns >= 5 else ("evidence" if ns >= 3 else ("hint" if ns >= 2 else "insufficient"))
        Nstr = "40+25" if N is None else str(N); zstr = "3 & 5" if z is None else f"{z:.1f}"
        print(f"   {name:<40}{Nstr:>5}{zstr:>6}{('0.06' if sig is None else f'{sig:.2f}'):>7}{ns:>9.1f}{verdict:>16}")
    print(f"""
   READING: the existing resolved high-z disc samples sit mostly at z~1-2.5, where the predicted offset is only a
   few percent -- below current per-galaxy precision, so they cannot yet test the law (consistent with them lying
   ~on the z=0 BTFR). The decisive move is REDSHIFT, not just number: ~25 clean discs at z~5 (BTFR offset ~13%) plus a
   z~3 anchor sample reach 5 sigma. This is squarely within JWST/NIRSpec + ALMA reach this decade.""")

    # ---- figure ----
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, (axA, axB) = plt.subplots(1, 2, figsize=(13, 5.3))
        zl = np.linspace(0.05, 6, 200)
        axA.plot(zl, [lever(z) for z in zl], "b-", lw=2.4)
        axA.fill_between(zl, 0, [lever(z) for z in zl], where=(zl < 2), color="grey", alpha=0.15)
        axA.text(1.0, 0.05, "negligible\nlever z<2", fontsize=9, ha="center", color="0.35")
        axA.set_xlabel("redshift $z$"); axA.set_ylabel(r"evolution lever arm $|\ln(\rho_{\rm DE}(z)/\rho_{\rm DE,0})|$")
        axA.set_title("(A) where the constraining power lives\n(all of it is at $z>2$)")
        axA.set_xlim(0, 6); axA.set_ylim(0, 1.2)

        for z, col, lab in [(3.0, "#2ca02c", "discs @ z=3"), (4.0, "#ff7f0e", "discs @ z=4"), (5.0, "#d62728", "discs @ z=5")]:
            Ns = np.arange(5, 120)
            ns = [np.sqrt(fisher(N, z, 0.06, 0.25)) for N in Ns]
            axB.plot(Ns, ns, color=col, lw=2.2, label=lab)
        axB.axhline(3, color="k", ls=":", lw=1); axB.axhline(5, color="k", ls="--", lw=1)
        axB.text(110, 3.15, "evidence", fontsize=8, ha="right"); axB.text(110, 5.15, "discovery", fontsize=8, ha="right")
        axB.set_xlabel("number of high-z BTFR discs ($\\sigma=0.06$ dex)"); axB.set_ylabel(r"$n_\sigma$ on $\beta$ (framework vs null)")
        axB.set_title("(B) BTFR reach vs sample size and redshift\n(redshift beats number)")
        axB.legend(loc="upper left", fontsize=9); axB.set_xlim(5, 120); axB.set_ylim(0, 8)
        fig.tight_layout()
        import os
        out = os.path.join(os.path.dirname(__file__), "..", "figures", "combined_forecast.png")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        fig.savefig(out, dpi=120, bbox_inches="tight")
        print(f"\n  figure written: {os.path.normpath(out)}")
    except Exception as e:
        print(f"\n  (figure skipped: {e})")

    print("\n" + "#" * 102)
    print("# VERDICT (combined): the whole distinctive claim reduces to one number, beta (1=framework, 0=ordinary MOND).")
    print("# Honest structural fact: rho_DE is ~flat below z~2, so ALL evolution power is at z>2 -- the low-z channels")
    print("# anchor a0(0), the high-z BTFR/RAR test beta. Reach: ~30 discs @ z=3 -> 3 sigma; ~25 @ z=5 + anchor -> 5 sigma.")
    print("# The roadmap to proof is high-z resolved kinematics, and REDSHIFT buys more than sample size.")
    print("#" * 102)


if __name__ == "__main__":
    main()
