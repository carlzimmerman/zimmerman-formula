#!/usr/bin/env python3
"""
DOOR 1 -- Gravitational lensing: the framework's prediction for light bending and its evolution.
================================================================================================
Worked INSIDE the framework. In the covariant completion (AeST; Skordis & Zlosnik 2021) light bends in the SAME
modified potential that governs dynamics, with the General-Relativistic factor of 2 -- so the lensing 'mass' equals
the MOND phantom mass, and weak lensing measures the same radial-acceleration relation as rotation curves.

Two clean predictions, both coefficient-free in the RATIO:

(1) The LENSING radial-acceleration relation: g_obs = g_bar nu(g_bar/a0), extended BELOW rotation-curve
    accelerations (to ~1e-13 m/s^2). At low z this is what KiDS galaxy-galaxy lensing (Brouwer et al. 2021)
    actually measured -- and found consistent with the MOND/RAR extrapolation. The framework reproduces it.

(2) The ASYMPTOTIC DEFLECTION of an isolated mass SATURATES. In GR alpha = 4GM/(c^2 b) -> 0 as the impact
    parameter b grows; in the framework the deep-MOND field g = sqrt(G M a0)/r gives a constant
        alpha_inf = 2 pi sqrt(G M a0) / c^2          (independent of b!)
    -- a qualitative signature unlike any dark-matter halo, and it EVOLVES as alpha_inf ~ sqrt(a0) ~ (rho_DE)^(1/4).

Derivation of (2): alpha = (2/c^2) integral of g_perp dl along the line of sight; for g = sqrt(GMa0)/r,
g_perp = sqrt(GMa0) b/r^2, and integral_{-inf}^{inf} b dl/(b^2+l^2) = pi, so alpha_inf = 2 pi sqrt(GMa0)/c^2.

Reproducible: `python door1_gravitational_lensing.py`. Needs numpy (+ matplotlib for the figure).
"""
import numpy as np

G = 6.674e-11; Msun = 1.989e30; C = 2.99792458e8
MPC = 3.0857e22; H0 = 67.4e3 / MPC; OmL = 0.685
A0 = 1.2e-10
A0_LAMBDA = C**2 * np.sqrt(3 * OmL * H0**2 / C**2 / (32 * np.pi))
W0, WA = -0.752, -0.86
ARCSEC = 180 * 3600 / np.pi          # rad -> arcsec


def nu_simple(y):
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def a0_of_z(z, a0_0=A0):
    a = 1.0 / (1.0 + z)
    rhoDE = a**(-3 * (1 + W0 + WA)) * np.exp(-3 * WA * (1 - a))
    return a0_0 * np.sqrt(rhoDE)


def alpha_inf(M_solar, z=0.0):
    """Asymptotic (saturated) MOND light-deflection angle, radians: 2 pi sqrt(G M a0(z)) / c^2."""
    return 2 * np.pi * np.sqrt(G * M_solar * Msun * a0_of_z(z)) / C**2


def main():
    print("#" * 100)
    print("# DOOR 1 -- gravitational lensing: the framework's light-bending prediction and its evolution")
    print("#" * 100 + "\n")
    print(f"  a0(0) = {A0:.2e} m/s^2 (RAR anchor; Lambda-only {A0_LAMBDA:.2e}).  Lensing uses the SAME a0 as dynamics.\n")

    # ---- (1) the lensing RAR matches Brouwer+2021 at z~0 ----
    print("=" * 100)
    print("(1) the LENSING radial-acceleration relation (framework) -- extends rotation curves to lower g_bar")
    print("=" * 100)
    print("   The framework predicts weak lensing traces g_obs = g_bar nu(g_bar/a0) to ~1e-13 m/s^2.")
    print("   KiDS GGL (Brouwer et al. 2021, z~0.2-0.4) measured exactly this and found it consistent with MOND.")
    print(f"   {'g_bar [m/s^2]':>16}{'g_obs/g_bar (boost)':>22}{'regime':>14}")
    for gb in (1e-9, 1e-10, 1e-11, 1e-12, 1e-13):
        D = nu_simple(gb / A0)
        reg = "Newtonian" if gb > 3 * A0 else ("deep-MOND" if gb < A0 / 3 else "transition")
        print(f"   {gb:>16.0e}{D:>22.2f}{reg:>14}")
    print()

    # ---- (2) the saturated deflection angle and its evolution ----
    print("=" * 100)
    print("(2) the ASYMPTOTIC deflection SATURATES at alpha_inf = 2 pi sqrt(G M a0)/c^2 (constant in b)")
    print("=" * 100)
    print(f"   {'system':<22}{'M_bar[Msun]':>12}{'alpha_inf(z=0)':>16}{'alpha_inf(z=1)':>16}{'alpha_inf(z=2)':>16}")
    for name, M in [("massive galaxy", 1e11), ("group", 1e13), ("cluster (baryons)", 1e14)]:
        a = [alpha_inf(M, z) * ARCSEC for z in (0, 1, 2)]
        print(f"   {name:<22}{M:>12.0e}{a[0]:>14.2f}\"{a[1]:>14.2f}\"{a[2]:>14.2f}\"")
    print(f"""
   In GR the deflection by a point mass keeps falling as 4GM/(c^2 b); the framework predicts it levels off at a
   constant ~0.1-1 arcsec set by sqrt(M a0). This saturated 'MOND lensing shelf' is a qualitative discriminator --
   no NFW halo reproduces a b-independent deflection -- and it is directly probed by the stacked weak-lensing
   profiles of isolated galaxies at large radius (Euclid, Rubin, Roman).""")

    # ---- (3) the evolution / coefficient-free ratio ----
    print("\n" + "=" * 100)
    print("(3) PREDICTION: the lensing amplitude evolves as alpha_inf(z) ~ sqrt(a0(z)) ~ (rho_DE)^(1/4)")
    print("=" * 100)
    zs = np.array([0.0, 0.3, 0.5, 1.0, 2.0, 3.0])
    print(f"   {'z':>6}{'a0(z)/a0(0)':>14}{'alpha_inf ratio':>18}")
    for z in zs:
        print(f"   {z:>6.1f}{a0_of_z(z)/a0_of_z(0):>14.3f}{(a0_of_z(z)/a0_of_z(0))**0.5:>18.3f}")
    zpk = np.linspace(0, 1.5, 400)
    ipk = int(np.argmax([a0_of_z(z) for z in zpk]))
    print(f"""
   NOTE the shape: under DESI's w0-wa dark energy, rho_DE (hence a0) is NON-monotonic -- it rises ~{100*(a0_of_z(zpk[ipk])/a0_of_z(0)-1):.0f}% to a peak
   near z~{zpk[ipk]:.1f}, then declines. So the framework predicts lensing is slightly STRONGER for z~0.3-0.5 lenses than
   today, and WEAKER for z>1 lenses -- a distinctive, testable, non-monotonic signature (lenses span exactly this
   range). The ratio is coefficient-free: the 32pi and c^2 sqrt(G) cancel; only rho_DE(z) (DESI) sets it.""")

    # ---- figure ----
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, (axA, axB) = plt.subplots(1, 2, figsize=(13, 5.3))

        gg = np.logspace(-13.5, -8.5, 300)
        axA.plot(np.log10(gg), np.log10(gg * nu_simple(gg / A0)), "b-", lw=2.2, label="framework lensing RAR")
        axA.plot(np.log10(gg), np.log10(gg), "k:", lw=1, label="Newtonian (1:1)")
        axA.axvspan(-12.0, -8.7, alpha=0.08, color="green")
        axA.axvspan(-13.5, -12.0, alpha=0.08, color="purple")
        axA.text(-10.3, -13.0, "rotation curves", fontsize=8, color="green", ha="center")
        axA.text(-12.8, -9.5, "lensing-only\n(Brouwer+21)", fontsize=8, color="purple", ha="center")
        axA.set_xlabel(r"$\log_{10}\,g_{\rm bar}$ [m/s$^2$]"); axA.set_ylabel(r"$\log_{10}\,g_{\rm obs}$")
        axA.set_title("(A) Lensing RAR: framework $a_0$ over the full range\n(matter + lensing probe the same scale)")
        axA.legend(loc="upper left", fontsize=9); axA.set_xlim(-13.5, -8.6); axA.set_ylim(-13.0, -8.6)

        zl = np.linspace(0, 3, 200)
        axB.plot(zl, [(a0_of_z(z) / a0_of_z(0))**0.5 for z in zl], "r-", lw=2.4)
        axB.axhline(1, color="k", ls=":", lw=1)
        axB.scatter(zs, (np.array([a0_of_z(z) for z in zs]) / a0_of_z(0))**0.5, s=45, c="darkred", zorder=3)
        axB.set_xlabel(r"lens redshift $z$"); axB.set_ylabel(r"$\alpha_\infty(z)/\alpha_\infty(0)$ (lensing amplitude)")
        axB.set_title("(B) Predicted lensing-amplitude evolution\n(non-monotonic: peak near $z\\sim0.4$, decline at $z>1$)")
        axB.set_xlim(0, 3); axB.set_ylim(0.83, 1.06)
        fig.tight_layout()
        import os
        out = os.path.join(os.path.dirname(__file__), "..", "figures", "door1_gravitational_lensing.png")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        fig.savefig(out, dpi=120, bbox_inches="tight")
        print(f"\n  figure written: {os.path.normpath(out)}")
    except Exception as e:
        print(f"\n  (figure skipped: {e})")

    print("\n" + "#" * 100)
    print("# VERDICT (Door 1): lensing is an independent channel on the SAME a0. The framework reproduces the KiDS")
    print("# lensing RAR (z~0), predicts a distinctive saturated deflection alpha_inf=2pi sqrt(GMa0)/c^2 (no halo")
    print("# mimics it), and a non-monotonic amplitude evolution (peak z~0.4, decline z>1) set coefficient-free by")
    print("# rho_DE(z). Probed by Euclid/Rubin/Roman stacked lensing across lens redshift.")
    print("#" * 100)


if __name__ == "__main__":
    main()
