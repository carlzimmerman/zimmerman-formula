#!/usr/bin/env python3
"""
Does the framework work with ALL current SPARC + JWST data? An honest ledger.
=============================================================================

Question (Carl): is a0=cH/Z with a0(z)=a0(0)E(z) consistent with everything we have now?
This goes dataset by dataset and marks each: CONSISTENT / TENSION / UNINFORMATIVE, with
the number behind it. The crucial meta-point is stated at the end: consistency is NOT the
same as confirmation, because LCDM is consistent with the same data.

Run: python <thisfile>   (needs numpy)
"""
import numpy as np

c, Mpc = 2.99792458e8, 3.0857e22
OM, OL = 0.315, 0.685
E = lambda z: np.sqrt(OM * (1 + z) ** 3 + OL)
Z = 2 * np.sqrt(8 * np.pi / 3)
A0_OBS = 1.20    # SPARC, in 1e-10 m/s^2


def row(name, pred, obs, status, note):
    print(f"  [{status:13}] {name}")
    print(f"     predicted {pred}   |   observed {obs}")
    print(f"     {note}")


def main():
    print("=" * 84)
    print("CONSISTENCY LEDGER -- the framework vs all current SPARC + JWST data")
    print("=" * 84)

    # 1. SPARC local acceleration scale
    a0_planck = c * (67.4e3 / Mpc) / Z * 1e10
    a0_shoes  = c * (73.0e3 / Mpc) / Z * 1e10
    row("SPARC local a0 (175 galaxies, McGaugh+16)",
        f"cH0/Z = {a0_planck:.2f} (H0=67.4) .. {a0_shoes:.2f} (H0=73)",
        f"{A0_OBS:.2f} +/- 0.26",
        "CONSISTENT",
        "matched within the H0 range -- but note: the coefficient Z is FIT to this, so it is")
    print("     a calibration, not a prediction. The RAR shape itself is inherited standard MOND.\n")

    # 2. the a0(z) evolution (3 points)
    p_fit, p_err = 0.80, 0.17
    nsig_p1 = abs(1.0 - p_fit) / p_err
    row("a0(z) evolution (SPARC, Varasteanu, MUSE-DARK to z=0.9)",
        "p = 1 (a0 ~ E(z))",
        f"p = {p_fit} +/- {p_err}",
        "CONSISTENT",
        f"framework p=1 is {nsig_p1:.1f} sigma from the fit -- consistent. Constant a0 disfavoured,")
    print("     but only ~2 sigma after the inter-method systematic (NOT a detection).\n")

    # 3. BTFR / Faber-Jackson zero-point evolution
    pred_23 = -np.log10(E(2.3))
    row("BTFR/TFR zero-point at z~2.3 (Ubler+17 vs 'no-evolution' results)",
        f"-log10 E(2.3) = {pred_23:.2f} dex",
        "Ubler+17: -0.45 dex; others: ~no evolution to z~3",
        "MIXED",
        "consistent with Ubler (-0.45 vs predicted -0.54, within errors); in tension with the")
    print("     'no significant evolution to z~3' result. The measurements disagree with each")
    print("     other, and the RAR scatter GROWS at z>3 (mild problem for a universal a0).\n")

    # 4. JWST high-z dynamical masses
    row("JWST z>4 dynamical masses (de Graaff+24; 2501.17145)",
        "deep-MOND boost M_dyn/M_bar ~ 2-3",
        "M_dyn/M* ~ 3-100 (sigma-based UPPER LIMITS)",
        "UNINFORMATIVE",
        "sigma-based M_dyn is contaminated by feedback/turbulence/non-equilibrium -> upper limit;")
    print("     cannot refute OR confirm the framework (jwst_2025_data_confront.py).\n")

    # 5. CMB
    row("CMB linear spectra (Planck)",
        "running a0 leaves linear C_l, P(k) exactly invariant (a0 is O(dphi^3); dq^00=0)",
        "Planck: r_s=144.4 Mpc, l_A~301",
        "CONSISTENT",
        "verified: a0 absent from linear perturbations; r_s=144.3, l_A=301.7 recovered. 2nd-order open.\n")

    print("=" * 84)
    print("ANSWER")
    print("=" * 84)
    print("  YES -- the framework is CONSISTENT with all current SPARC + JWST data: nothing in")
    print("  hand refutes it. The local scale is matched, the 3-point a0(z) trend fits p=1, the")
    print("  CMB is safe at linear order, the BTFR is consistent with Ubler, and the high-z")
    print("  dynamical masses are too contaminated to count against it.")
    print()
    print("  BUT 'consistent' is weaker than it sounds, for three honest reasons:")
    print("   1. LCDM is ALSO consistent with every one of these (Magneticum reproduces the")
    print("      apparent-a0 rise) -- so the data do not DISTINGUISH the framework.")
    print("   2. The consistency leans on FITTED or UNINFORMATIVE inputs: the local a0 is the")
    print("      fitted coefficient; the evolution is only ~2sigma; the high-z masses can't test it.")
    print("   3. The one genuinely mixed signal (BTFR evolution + growing scatter) slightly")
    print("      favours LCDM, not the framework.")
    print()
    print("  So: WORKS WITH the data = YES.  CONFIRMED BY the data = NO.  DISTINGUISHED FROM")
    print("  LCDM = NOT YET. It is a viable, unfalsified hypothesis sitting alongside LCDM, not")
    print("  ahead of it -- which is exactly why the clean z>4 extended-rotator test matters.")
    print("=" * 84)


if __name__ == "__main__":
    main()
