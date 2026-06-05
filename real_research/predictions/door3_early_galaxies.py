#!/usr/bin/env python3
"""
DOOR 3 -- Early galaxies (JWST/ALMA): what a0(z) = a0(0) sqrt(rho_DE) predicts for the high-z universe.
======================================================================================================
Worked INSIDE the framework. Dark energy dilutes into the past (under DESI w0-wa, rho_DE peaks near z~0.4 then
falls), so a0 was SMALLER at high z -> the MOND boost was WEAKER -> early galaxies were MORE Newtonian. Concrete,
falsifiable consequences:

(1) BARYONIC TULLY-FISHER OFFSET. V_flat = (G M_bar a0(z))^(1/4), so at fixed baryonic mass a high-z disc rotates
    SLOWER: Delta log V = (1/4) log[a0(z)/a0(0)]. The framework predicts high-z discs fall BELOW the z=0 BTFR.

(2) A SIGN TEST that separates the two readings of the theory:
      * a0 ~ sqrt(rho_DE)   (framework, favored): a0 DECLINES at high z -> discs ~10-20% BELOW the z=0 BTFR.
      * a0 ~ sqrt(rho_total) (Cai-Kim apparent-horizon reading): a0 ~ H(z) RISES steeply -> discs far ABOVE.
    Current high-z disc kinematics (Rizzo+2020, Lelli+2021, de Graaff+2024) sit ~on the z=0 BTFR within errors --
    which already strongly disfavors the rising reading and is mildly consistent-to-tension with the decline.

(3) AN HONEST NON-WIN. A weaker high-z boost means MOND-enhanced structure growth was WEAKER early, so the
    framework does NOT help (mildly hurts) JWST's 'too massive too early' galaxies. Reported, not hidden.

CAVEAT: at z>~2 the CPL dark-energy law is an EXTRAPOLATION beyond where DESI constrains it; the high-z a0 values
inherit that model dependence. Flagged in the table. Reproducible: `python door3_early_galaxies.py`. Needs numpy.
"""
import numpy as np

G = 6.674e-11; Msun = 1.989e30; C = 2.99792458e8; KMS = 1.0e3
MPC = 3.0857e22; H0 = 67.4e3 / MPC; OmL = 0.685; OmM = 0.315
A0 = 1.2e-10
A0_LAMBDA = C**2 * np.sqrt(3 * OmL * H0**2 / C**2 / (32 * np.pi))
W0, WA = -0.752, -0.86


def rho_DE_ratio(z):
    a = 1.0 / (1.0 + z)
    return a**(-3 * (1 + W0 + WA)) * np.exp(-3 * WA * (1 - a))


def a0_sqrtDE(z):
    return A0 * np.sqrt(rho_DE_ratio(z))


def Ez(z):
    return np.sqrt(OmM * (1 + z)**3 + OmL * rho_DE_ratio(z))


def a0_sqrttot(z):
    """The disfavored apparent-horizon reading: a0 ~ sqrt(rho_total) ~ H(z) ~ E(z)."""
    return A0 * Ez(z)


def main():
    print("#" * 102)
    print("# DOOR 3 -- early galaxies: a0(z) = a0(0) sqrt(rho_DE) and the high-z universe")
    print("#" * 102 + "\n")
    print(f"  a0(0) = {A0:.2e} m/s^2 (anchor; Lambda-only {A0_LAMBDA:.2e}). High-z a0 DECLINES (dark energy dilutes).\n")

    # ---- (1) a0(z) to high z, both readings ----
    print("=" * 102)
    print("(1) a0(z): framework (sqrt rho_DE, declining) vs the disfavored rising reading (sqrt rho_total)")
    print("=" * 102)
    print(f"   {'z':>5}{'a0_DE/a0(0)':>13}{'a0_tot/a0(0)':>14}{'BTFR dlogV (DE)':>17}{'V/V0 (DE)':>11}{'note':>16}")
    for z in (0.0, 0.4, 1.0, 2.0, 3.0, 4.2, 6.0, 10.0):
        rDE = a0_sqrtDE(z) / A0
        rTO = a0_sqrttot(z) / A0
        dlogV = 0.25 * np.log10(rDE)
        note = "DESI-constrained" if z <= 2 else "EXTRAPOLATION"
        print(f"   {z:>5.1f}{rDE:>13.3f}{rTO:>14.2f}{dlogV:>17.3f}{10**dlogV:>11.3f}{note:>16}")
    print()

    # ---- (2) the BTFR-offset sign test ----
    print("=" * 102)
    print("(2) the BTFR-offset SIGN TEST (the cleanest high-z discriminator)")
    print("=" * 102)
    for z in (4.2, 6.0):
        vDE = (a0_sqrtDE(z) / A0)**0.25
        vTO = (a0_sqrttot(z) / A0)**0.25
        print(f"   z={z:>4}: framework predicts V/V(z=0 BTFR) = {vDE:.3f}  ({100*(vDE-1):+.0f}%, BELOW);"
              f"  rising reading = {vTO:.3f}  ({100*(vTO-1):+.0f}%, far ABOVE)")
    print(f"""
   A disc of fixed baryonic mass is predicted to rotate ~{100*(1-(a0_sqrtDE(4.2)/A0)**0.25):.0f}% slower at z=4.2 and ~{100*(1-(a0_sqrtDE(6.0)/A0)**0.25):.0f}% slower at z=6 than
   its z=0 BTFR twin. The measured high-z discs (Lelli+2021's z=4.2 thin disc; ALMA/JWST kinematics) sit close to
   the z=0 BTFR within their errors -- which EXCLUDES the rising sqrt(rho_total) reading (it predicts discs
   ~50-60% too fast) and leaves the framework's mild decline as the viable option, pending tighter data.""")

    # ---- (3) the honest non-win for JWST massive-early galaxies ----
    print("\n" + "=" * 102)
    print("(3) HONEST NON-WIN: the declining a0 does NOT help JWST's 'too massive too early' galaxies")
    print("=" * 102)
    print(f"""   MOND speeds up early structure growth via its enhanced effective gravity. But the framework makes that
   enhancement WEAKER at high z (a0(z=10)/a0(0) ~ {a0_sqrtDE(10)/A0:.2f}), so it works AGAINST, not for, the rapid early
   assembly JWST sees. A constant- or rising-a0 MOND would help more here. The framework's distinctive content
   (declining a0) is a liability for this particular puzzle -- stated plainly, because it is true.""")

    # ---- (4) the transition radius moves out ----
    print("\n" + "=" * 102)
    print("(4) STRUCTURAL prediction: the MOND transition radius r_t = sqrt(G M / a0) moves OUTWARD at high z")
    print("=" * 102)
    M = 1e10 * Msun
    for z in (0.0, 2.0, 4.2):
        rt = np.sqrt(G * M / a0_sqrtDE(z)) / (MPC / 1e3)   # kpc
        print(f"   z={z:>4}: r_t(10^10 Msun) = {rt:.1f} kpc  -> inner discs are MORE baryon-dominated (more Newtonian) early")
    print("   So high-z galaxies should look more 'maximal-disc'/Newtonian in their inner regions -- testable kinematically.")

    # ---- figure ----
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, (axA, axB) = plt.subplots(1, 2, figsize=(13, 5.3))
        zl = np.linspace(0, 8, 300)
        axA.plot(zl, [a0_sqrtDE(z) / A0 for z in zl], "b-", lw=2.4, label=r"framework $a_0\propto\sqrt{\rho_{\rm DE}}$ (declining)")
        axA.plot(zl, [a0_sqrttot(z) / A0 for z in zl], "r--", lw=2.0, label=r"rising reading $a_0\propto\sqrt{\rho_{\rm tot}}$ (disfavored)")
        axA.axvspan(2, 8, alpha=0.07, color="grey"); axA.text(5, 0.5, "extrapolation\nbeyond DESI", fontsize=8, ha="center", color="0.4")
        axA.axhline(1, color="k", ls=":", lw=1)
        axA.set_xlabel("redshift $z$"); axA.set_ylabel(r"$a_0(z)/a_0(0)$"); axA.set_yscale("log")
        axA.set_title("(A) the two readings diverge at high z\n(the sign of the high-z BTFR offset decides)")
        axA.legend(loc="upper left", fontsize=9); axA.set_xlim(0, 8)

        axB.plot(zl, [(a0_sqrtDE(z) / A0)**0.25 for z in zl], "b-", lw=2.4, label="framework prediction")
        axB.axhline(1, color="k", ls=":", lw=1, label="z=0 BTFR")
        axB.scatter([4.2], [(a0_sqrtDE(4.2) / A0)**0.25], s=60, c="navy", zorder=3)
        axB.annotate("Lelli+2021\nz=4.2 disc regime", (4.2, (a0_sqrtDE(4.2) / A0)**0.25), fontsize=8,
                     xytext=(2.6, 0.90), textcoords="data")
        axB.set_xlabel("redshift $z$"); axB.set_ylabel(r"$V_{\rm flat}(z)/V_{\rm flat}(z{=}0)$ at fixed $M_{\rm bar}$")
        axB.set_title("(B) predicted BTFR offset: high-z discs rotate slower\n(fixed baryons, $V\\propto a_0^{1/4}$)")
        axB.legend(loc="lower left", fontsize=9); axB.set_xlim(0, 8); axB.set_ylim(0.7, 1.05)
        fig.tight_layout()
        import os
        out = os.path.join(os.path.dirname(__file__), "..", "figures", "door3_early_galaxies.png")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        fig.savefig(out, dpi=120, bbox_inches="tight")
        print(f"\n  figure written: {os.path.normpath(out)}")
    except Exception as e:
        print(f"\n  (figure skipped: {e})")

    print("\n" + "#" * 102)
    print("# VERDICT (Door 3): the framework predicts high-z discs ~10-20% BELOW the z=0 BTFR (fixed baryons), a sign")
    print("# that EXCLUDES the rising sqrt(rho_total) reading and is the make-or-break z~3-6 deep-MOND test. Honest")
    print("# non-win: declining a0 does NOT help (mildly hurts) JWST's massive-early-galaxy puzzle. z>2 is an")
    print("# extrapolation of the DE law -- flagged. This door IS the decisive measurement (JWST/ALMA kinematics).")
    print("#" * 102)


if __name__ == "__main__":
    main()
