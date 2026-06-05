#!/usr/bin/env python3
"""
DOOR 5 -- The External-Field Effect (EFE) and its evolution: the signature no dark-matter halo can fake.
=======================================================================================================
Worked INSIDE the framework. The EFE is MOND's most distinctive qualitative prediction: a system's INTERNAL dynamics
depend on the EXTERNAL gravitational field it sits in. When the external field g_ext exceeds a0, the system is driven
quasi-Newtonian even if its own internal field is below a0. This VIOLATES the strong equivalence principle (SEP) --
something a dark-matter halo CANNOT do, because in LCDM a halo's internal dynamics are blind to a uniform external
field. The EFE is already detected at z=0 in SPARC rotation curves (Chae et al. 2020, ~4-5 sigma).

THE DISTINCTIVE, NEW PREDICTION: the EFE threshold is a0(z), which DECLINES at high z. So for a galaxy in a FIXED
environment (fixed g_ext), the EFE strength
        e_N(z) = g_ext / a0(z) = e_N(0) * a0(0)/a0(z) = e_N(0) / sqrt(rho_DE(z)/rho_DE0)
GROWS toward high z. Galaxies that are marginally MONDian today (g_ext ~ a0) are EFE-Newtonized at high z. The EFE
becomes stronger and more prevalent in the early universe -- and because NO halo produces an EFE at all, ANY detected
evolution of the EFE is impossible to mimic with dark matter. This is the cleanest discriminator in the whole suite.

Reproducible: `python door5_external_field_effect.py`. Needs numpy (+ matplotlib for the figure).
"""
import numpy as np

C = 2.99792458e8; G = 6.674e-11; Msun = 1.989e30; MPC = 3.0857e22; KMS = 1e3
H0 = 67.4e3 / MPC; OmL = 0.685
A0 = C**2 * np.sqrt(3 * OmL * H0**2 / C**2 / (32 * np.pi))
W0, WA = -0.752, -0.86


def a0z(z):
    a = 1 / (1 + z); return A0 * np.sqrt(a**(-3 * (1 + W0 + WA)) * np.exp(-3 * WA * (1 - a)))


# representative external fields (in units of a0(0)), from real environments
ENVIRONMENTS = [
    ("isolated field galaxy",   0.03, "cosmic web only"),
    ("loose group member",      0.30, "e.g. typical group galaxy"),
    ("Milky Way satellite",     0.10, "g_ext = V_MW^2/D at ~100 kpc (Door 2)"),
    ("dense group / infalling",  0.80, "marginally MONDian today"),
    ("cluster-outskirt galaxy",  1.50, "already Newtonized at z=0"),
]


def regime(eN):
    return "Newtonized" if eN > 1.0 else ("transition" if eN > 0.5 else "MONDian")


def main():
    print("#" * 102)
    print("# DOOR 5 -- the External-Field Effect (EFE) and its evolution: the SEP-violating, halo-proof signature")
    print("#" * 102 + "\n")
    print(f"  a0(0) = {A0:.2e} m/s^2. EFE strength e_N = g_ext/a0(z). Threshold for quasi-Newtonian: e_N > 1.\n")

    # ---- (1) z=0 baseline ----
    print("=" * 102)
    print("(1) z=0 EFE regimes (already detected in SPARC, Chae et al. 2020 ~4-5 sigma)")
    print("=" * 102)
    print(f"   {'environment':<26}{'g_ext/a0(0)':>13}{'regime':>13}   note")
    for name, eN0, note in ENVIRONMENTS:
        print(f"   {name:<26}{eN0:>13.2f}{regime(eN0):>13}   {note}")
    print()

    # ---- (2) THE distinctive prediction: EFE strengthens toward high z ----
    print("=" * 102)
    print("(2) PREDICTION: e_N(z) = g_ext/a0(z) GROWS at high z (a0 declines) -> EFE stronger & more prevalent early")
    print("=" * 102)
    zs = (0.0, 1.0, 2.0, 3.0)
    print(f"   {'environment':<26}" + "".join(f"{f'e_N(z={z:.0f})':>12}" for z in zs) + f"{'regime z=0->3':>22}")
    for name, eN0, note in ENVIRONMENTS:
        eNs = [eN0 * A0 / a0z(z) for z in zs]
        print(f"   {name:<26}" + "".join(f"{e:>12.2f}" for e in eNs) + f"{regime(eNs[0])+' -> '+regime(eNs[-1]):>22}")
    boost = A0 / a0z(3.0)
    print(f"""
   READING: at fixed environment the EFE strength is {boost:.2f}x larger at z=3 than today (e_N ~ 1/a0 ~ 1/sqrt(rho_DE)).
   The 'dense group / infalling' class CROSSES from MONDian (0.80) to Newtonized ({0.80*boost:.2f}) by z=3 -- a population of
   galaxies that look dark-matter-dominated locally should look BARYON-dominated (EFE-quenched) at high z.""")

    # ---- (3) why this is halo-proof ----
    print("\n" + "=" * 102)
    print("(3) why NO dark-matter halo can mimic this (the cleanest discriminator)")
    print("=" * 102)
    print("""   In LCDM the strong equivalence principle holds: a halo's internal dynamics are independent of a uniform
   external field. So (a) the EFE itself and (b) ANY redshift evolution of it are forbidden for dark matter. A
   detection of EFE evolution -- isolated vs grouped galaxies of identical baryons diverging MORE at high z -- would
   be impossible to reproduce with halos. The framework predicts exactly this, coefficient-free (e_N ratio ~ 1/sqrt(rho_DE)).""")

    # ---- (4) the observable ----
    print("\n" + "=" * 102)
    print("(4) the observable: the outer-rotation-curve downturn deepens at high z for grouped galaxies")
    print("=" * 102)
    print("""   MOND-with-EFE predicts the outer rotation curve declines below the flat value once g_ext dominates; the
   downturn amplitude grows monotonically with e_N. Since e_N grows ~36% by z=3 at fixed environment, grouped
   high-z discs should show DEEPER outer downturns than their z=0 analogs -- a measurement for JWST/ALMA resolved
   kinematics of group galaxies, and a 5th independent leg of the same sqrt(rho_DE) law.""")

    # ---- figure ----
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8.2, 5.6))
        zl = np.linspace(0, 4, 200)
        cols = ["#1f77b4", "#2ca02c", "#9467bd", "#ff7f0e", "#d62728"]
        for (name, eN0, _), col in zip(ENVIRONMENTS, cols):
            ax.plot(zl, [eN0 * A0 / a0z(z) for z in zl], color=col, lw=2.2, label=f"{name} (e₀={eN0})")
        ax.axhline(1.0, color="k", ls="--", lw=1.3)
        ax.text(0.05, 1.04, "EFE threshold e_N=1 (quasi-Newtonian above)", fontsize=8.5)
        ax.axhspan(1.0, 3.0, alpha=0.06, color="red"); ax.axhspan(0, 1.0, alpha=0.06, color="blue")
        ax.set_xlabel("redshift $z$"); ax.set_ylabel(r"EFE strength $e_N = g_{\rm ext}/a_0(z)$")
        ax.set_title("Door 5: the EFE strengthens toward high z (a₀ declines)\nthe SEP-violating signature no dark-matter halo can produce")
        ax.legend(loc="upper left", fontsize=8.5); ax.set_xlim(0, 4); ax.set_ylim(0, 2.4)
        fig.tight_layout()
        import os
        out = os.path.join(os.path.dirname(__file__), "..", "figures", "door5_external_field_effect.png")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        fig.savefig(out, dpi=120, bbox_inches="tight")
        print(f"\n  figure written: {os.path.normpath(out)}")
    except Exception as e:
        print(f"\n  (figure skipped: {e})")

    print("\n" + "#" * 102)
    print("# VERDICT (Door 5): the EFE is MOND's SEP-violating, halo-proof signature -- detected at z=0 (Chae+2020).")
    print(f"# Distinctive new prediction: e_N ~ 1/sqrt(rho_DE) grows ~{100*(A0/a0z(3)-1):.0f}% by z=3, so the EFE strengthens early and")
    print("# marginal galaxies cross to Newtonized. ANY detected EFE evolution is impossible for dark matter. 5th channel.")
    print("#" * 102)


if __name__ == "__main__":
    main()
