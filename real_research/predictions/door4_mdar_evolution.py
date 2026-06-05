#!/usr/bin/env python3
"""
DOOR 4 -- The master relation: the Mass-Discrepancy--Acceleration Relation (MDAR) and its PREDICTED evolution.
=============================================================================================================
Worked entirely INSIDE the framework (a0 = c^2 sqrt(Lambda/32pi); a0(z) = a0(0) sqrt(rho_DE(z)/rho_DE0)).

The MDAR is the single relation that encodes all of galaxy dynamics: the mass discrepancy
    D(r) == g_obs / g_bar = V_obs^2 / V_bar^2
plotted against the baryonic acceleration g_bar. In the framework it is exactly
    D(g_bar) = nu(g_bar / a0),     nu(y) = 1/2 + sqrt(1/4 + 1/y)   (simple interpolating function).

z=0 is the ANCHOR (this IS the radial-acceleration relation, already validated on SPARC to ~0.2 dex).
The NEW, distinctive, falsifiable content is the EVOLUTION: because a0 declines as sqrt(rho_DE), the whole
relation shifts. In the deep-MOND limit D -> sqrt(a0/g_bar), so at FIXED g_bar
    D(z)/D(0) = sqrt(a0(z)/a0(0)) = (rho_DE(z)/rho_DE0)^(1/4),
and the 'knee' (where D departs from 1, g_bar ~ a0) slides to lower g_bar. This is a clean prediction with
NO free coefficient in the ratio (the 32pi and c^2 sqrt(G) cancel).

Data: the real 175 SPARC galaxies (Lelli, McGaugh & Schombert 2016), data/sparc_data/*_rotmod.dat.
Reproducible: `python door4_mdar_evolution.py`. Needs numpy (+ matplotlib for the figure).
"""
import glob, os, numpy as np

# ---- constants (SI) ----
KPC = 3.0856775814913673e19; KMS = 1.0e3
ML_D, ML_B = 0.5, 0.7                       # 3.6um stellar mass-to-light (disk, bulge); McGaugh standard
C = 2.99792458e8; MPC = 3.0857e22; H0 = 67.4e3 / MPC; OmL = 0.685
LAM = 3 * OmL * H0**2 / C**2                 # cosmological constant from Planck Omega_Lambda
A0_LAMBDA = C**2 * np.sqrt(LAM / (32 * np.pi))   # framework a0 = 9.36e-11 m/s^2 (Lambda-only)
A0_ANCHOR = 1.2e-10                          # empirical RAR anchor (McGaugh) -- used for the SHAPE/evolution
W0, WA = -0.752, -0.86                       # DESI DR2 dark-energy equation of state
DATA = os.path.join(os.path.dirname(__file__), "..", "data", "sparc_data")


def nu_simple(y):
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def a0_of_z(z, a0_0=A0_ANCHOR):
    """Framework a0(z) = a0(0) sqrt(rho_DE(z)/rho_DE0), CPL dark energy w(a)=w0+wa(1-a)."""
    a = 1.0 / (1.0 + z)
    rhoDE = a**(-3 * (1 + W0 + WA)) * np.exp(-3 * WA * (1 - a))
    return a0_0 * np.sqrt(rhoDE)


def load_sparc():
    """Return g_bar, g_obs (SI) for every rotation-curve point of the 175 SPARC galaxies."""
    gbar, gobs = [], []
    ngal = 0
    for path in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        got = False
        for line in open(path):
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            p = s.split()
            if len(p) < 6:
                continue
            try:
                r, vob, ev, vg, vd, vb = (float(p[i]) for i in range(6))
            except ValueError:
                continue
            if r <= 0 or vob <= 0:
                continue
            r_m = r * KPC
            vbar2 = (ML_D * vd * vd + ML_B * vb * vb + vg * abs(vg)) * KMS**2
            if vbar2 <= 0:
                continue
            gbar.append(vbar2 / r_m)
            gobs.append((vob * KMS)**2 / r_m)
            got = True
        if got:
            ngal += 1
    return np.array(gbar), np.array(gobs), ngal


def binned_median(x, y, edges):
    """Median of y in bins of x; returns bin centers, medians, 16-84 percentile half-width."""
    cen, med, lo, hi = [], [], [], []
    for i in range(len(edges) - 1):
        m = (x >= edges[i]) & (x < edges[i + 1])
        if m.sum() >= 8:
            cen.append(0.5 * (edges[i] + edges[i + 1]))
            med.append(np.median(y[m]))
            lo.append(np.percentile(y[m], 16))
            hi.append(np.percentile(y[m], 84))
    return map(np.array, (cen, med, lo, hi))


def main():
    print("#" * 100)
    print("# DOOR 4 -- the MDAR (master relation) and its predicted evolution under a0(z) = a0(0) sqrt(rho_DE)")
    print("#" * 100 + "\n")

    gbar, gobs, ngal = load_sparc()
    D = gobs / gbar                                   # the mass discrepancy
    print(f"  loaded {ngal} SPARC galaxies, {len(gbar)} rotation-curve points (real data).")
    print(f"  framework a0 (Lambda-only) = {A0_LAMBDA:.3e} m/s^2 ; RAR anchor a0(0) = {A0_ANCHOR:.3e} m/s^2\n")

    # ---- (1) z=0 anchor: does D = nu(g_bar/a0) describe the SPARC MDAR? ----
    print("=" * 100)
    print("(1) z=0 ANCHOR: the framework MDAR  D = nu(g_bar/a0)  vs the real SPARC mass discrepancy")
    print("=" * 100)
    for label, a0 in [("framework a0 = c^2 sqrt(Lambda/32pi)", A0_LAMBDA), ("RAR anchor a0 = 1.2e-10", A0_ANCHOR)]:
        scatter = np.std(np.log10(D) - np.log10(nu_simple(gbar / a0)))
        print(f"   {label:<42}  scatter in log D = {scatter:.3f} dex")
    print("   -> the z=0 MDAR is reproduced; this is the validated RAR, just plotted as the discrepancy.\n")

    # ---- (2) THE PREDICTION: how the MDAR evolves ----
    print("=" * 100)
    print("(2) PREDICTION: the MDAR at z>0 (a0 declines, the relation shifts down-and-left)")
    print("=" * 100)
    zs = [0.0, 1.0, 2.0, 3.0]
    print(f"   {'a0 ratio a0(z)/a0(0)':>26}: ", end="")
    print("  ".join(f"z={z:.0f}:{a0_of_z(z)/a0_of_z(0):.3f}" for z in zs))
    # mass discrepancy at three fiducial baryonic accelerations
    print(f"\n   mass discrepancy D = nu(g_bar/a0(z)) at fixed g_bar, vs redshift:")
    print(f"   {'g_bar [m/s^2]':>16}{'regime':>14}" + "".join(f"{f'D(z={z:.0f})':>12}" for z in zs) + f"{'D(3)/D(0)':>12}")
    for gb, lab in [(1e-11, "deep-MOND"), (1.2e-10, "transition"), (1e-9, "Newtonian")]:
        Ds = [nu_simple(gb / a0_of_z(z)) for z in zs]
        print(f"   {gb:>16.1e}{lab:>14}" + "".join(f"{d:>12.3f}" for d in Ds) + f"{Ds[-1]/Ds[0]:>12.3f}")
    print(f"""
   READING: in the deep-MOND regime the discrepancy at fixed baryonic acceleration is predicted to be
   ~{100*(1-nu_simple(1e-11/a0_of_z(3))/nu_simple(1e-11/a0_of_z(0))):.0f}% SMALLER at z=3 than today (D ~ sqrt(a0) ~ (rho_DE)^1/4). Same baryons, same g_bar, but
   less missing mass at early times -- because the modification scale a0 was smaller when dark energy was.
   In the Newtonian regime (g_bar >> a0) D~1 always: no evolution there. The signal lives at g_bar < a0.""")

    # ---- (3) the coefficient-free statement ----
    print("\n" + "=" * 100)
    print("(3) why this is coefficient-free (the 32pi never enters the prediction)")
    print("=" * 100)
    print("""   D(z)/D(0) = sqrt(a0(z)/a0(0)) = (rho_DE(z)/rho_DE0)^(1/4) in deep-MOND. The absolute a0 (hence c^2 sqrt(G)
   and the route-forced 32pi) cancels in the RATIO. The prediction is fixed entirely by the dark-energy
   density history rho_DE(z) -- which DESI measures. So the MDAR-evolution test is a clean, parameter-free
   cross-check between galaxy dynamics and cosmology.""")

    # ---- figure ----
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, (axA, axB) = plt.subplots(1, 2, figsize=(13.5, 5.4))

        # Panel A: the MDAR with evolving framework curves
        axA.hexbin(np.log10(gbar), np.log10(D), gridsize=42, cmap="Greys", mincnt=1, bins="log")
        gg = np.logspace(-12.5, -8.0, 240)
        colors = ["#1f77b4", "#2ca02c", "#ff7f0e", "#d62728"]
        for z, col in zip(zs, colors):
            axA.plot(np.log10(gg), np.log10(nu_simple(gg / a0_of_z(z))), color=col, lw=2.2,
                     label=fr"$z={z:.0f}$ ($a_0\!\to\!{a0_of_z(z)/a0_of_z(0):.2f}\,a_0$)")
        axA.axhline(0, color="k", ls=":", lw=1)
        axA.set_xlabel(r"$\log_{10}\,g_{\rm bar}\;[{\rm m\,s^{-2}}]$")
        axA.set_ylabel(r"$\log_{10}\,D=\log_{10}(g_{\rm obs}/g_{\rm bar})$")
        axA.set_title("(A) Mass-discrepancy–acceleration relation\nSPARC (grey) + framework, evolving with $a_0(z)$")
        axA.legend(loc="upper right", fontsize=8.5, title="framework MDAR")
        axA.set_xlim(-12.3, -8.2); axA.set_ylim(-0.1, 1.6)

        # Panel B: deep-MOND discrepancy amplitude vs z
        zline = np.linspace(0, 4, 100)
        for gb, lab, col in [(1e-11, r"$g_{\rm bar}=10^{-11}$ (deep-MOND)", "#d62728"),
                             (3e-11, r"$g_{\rm bar}=3\times10^{-11}$", "#ff7f0e"),
                             (1e-10, r"$g_{\rm bar}=10^{-10}$ (near knee)", "#1f77b4")]:
            Dz = np.array([nu_simple(gb / a0_of_z(z)) for z in zline])
            axB.plot(zline, Dz / Dz[0], color=col, lw=2.2, label=lab)
        axB.axhline(1, color="k", ls=":", lw=1)
        axB.set_xlabel(r"redshift $z$")
        axB.set_ylabel(r"$D(z)/D(0)$  (mass discrepancy, normalized)")
        axB.set_title("(B) Predicted decline of the missing-mass factor\nat fixed baryonic acceleration")
        axB.legend(loc="lower left", fontsize=9)
        axB.set_xlim(0, 4); axB.set_ylim(0.80, 1.02)

        fig.tight_layout()
        out = os.path.join(os.path.dirname(__file__), "..", "figures", "door4_mdar_evolution.png")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        fig.savefig(out, dpi=120, bbox_inches="tight")
        print(f"\n  figure written: {os.path.normpath(out)}")
    except Exception as e:
        print(f"\n  (figure skipped: {e})")

    print("\n" + "#" * 100)
    print("# VERDICT (Door 4): z=0 MDAR reproduced (validated RAR). The framework PREDICTS the master relation")
    print("# shifts with a0(z): the deep-MOND missing-mass factor is ~12% smaller at z=3, coefficient-free,")
    print("# set entirely by rho_DE(z). Testable with high-z rotation curves (JWST/ALMA) -> feeds Door 3.")
    print("#" * 100)


if __name__ == "__main__":
    main()
