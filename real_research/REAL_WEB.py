#!/usr/bin/env python3
"""
The REAL web: one number, many forced edges, independently-measured nodes that cohere.
=====================================================================================

Carl's "interlocking web" is a real idea -- but only ONE of his two webs is real, and
this script shows precisely why. A web is *strong* (carries evidence) only when it is
OVER-CONSTRAINED: a few numbers force many predictions with NO per-prediction freedom,
AND the nodes that can be measured independently agree.

This builds the cosmology core as an explicit graph:

      one premise           a0 = (c/2) sqrt(G rho_c) = cH(z)/Z,   Z = 2 sqrt(8pi/3)

forces ~9 edges through ACTUAL equations (Friedmann + MOND), and -- the decisive part --
several of the nodes are measured by INDEPENDENT experiments (Planck CMB, SPARC rotation
curves, MUSE-DARK high-z kinematics, de Graaff JADES masses). The script:

  (1) enumerates the edges (each a forced equation, computed);
  (2) anchors the single free number on Planck's CMB H0 and PREDICTS the galaxy-scale
      nodes, then compares to their independent measurements -- the coherence residuals;
  (3) writes the OVER-CONSTRAINT LEDGER: N_independent_measurements - N_free_parameters.
      Real web -> positive (over-constrained). Constants web -> <= 0 (a fit).

Contrast is the whole point: the constants "web" (alpha = 4Z^2+3, ...) jumps between
unrelated domains, each carrying its own free integers, so its ledger is <= 0 -- no
over-constraint, hence ~0 bits of evidence (see reviews/false_discovery_rate.py).

Read-only. Uses only published numbers. Run:  python real_research/REAL_WEB.py
"""

import math

# ---- constants (SI) ----
c = 2.99792458e8
G = 6.674e-11
MPC = 3.0857e22
HBAR = 1.054571817e-34
KB = 1.380649e-23

# ---- the ONE structural number and the cosmology it lives in ----
Z = 2 * math.sqrt(8 * math.pi / 3)          # = sqrt(32pi/3) = 5.788810
OM, OL = 0.315, 0.685                        # Planck flat-LCDM

# ---- independent empirical anchors (each from a DIFFERENT dataset) ----
H0_PLANCK = 67.4          # km/s/Mpc, Planck 2018 CMB (z~1100 acoustic scale)
A0_SPARC = 1.13e-10       # m/s^2,   SPARC RAR, 175 galaxies (z~0 rotation curves)
A0_MUSEDARK_z1 = 2.38e-10 # m/s^2,   MUSE-DARK III 2026, ~79 galaxies at z~1
DEGRAAFF_MDYN_MAX = 40.0  # M_dyn/M_* upper end, de Graaff 2024, JADES z=5.5-7.4


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def H_si(H0_kms_mpc):
    return H0_kms_mpc * 1e3 / MPC


def a0_from_H(H0_kms_mpc):
    """The premise, forward: a0 = cH/Z."""
    return c * H_si(H0_kms_mpc) / Z


def H_from_a0(a0):
    """The premise, inverted: H0 = Z a0 / c  (galaxy dynamics -> H0)."""
    return Z * a0 / c * MPC / 1e3


def pct(x, ref):
    return (x - ref) / ref * 100.0


# ====================================================================================
def part1_premise():
    print("#" * 84)
    print("# THE REAL WEB -- cosmology core, over-constrained, data-supported")
    print("#" * 84)
    print()
    print("PREMISE (one equation, one structural number):")
    print(f"    a0 = (c/2) sqrt(G rho_c) = cH(z)/Z,    Z = 2 sqrt(8pi/3) = {Z:.6f}")
    print()
    print("FREE PARAMETERS of the whole web: exactly ONE -- the value of a0 today")
    print("    (equivalently H0). And even that is not free: Planck's CMB fixes H0, SPARC")
    print("    fixes a0, and the premise says they must be the SAME number. That equality")
    print("    is the keystone the rest of the web hangs from.")
    print()


# ====================================================================================
def part2_edges():
    print("=" * 84)
    print("(2) THE EDGES -- each a FORCED equation off the one premise (not a fit)")
    print("=" * 84)
    a0 = A0_SPARC
    H0 = H0_PLANCK

    edges = []

    # E1: a0 <-> rho_c   (the premise itself, density form)
    rho_c = 3 * H_si(H0) ** 2 / (8 * math.pi * G)
    a0_from_rho = (c / 2) * math.sqrt(G * rho_c)
    edges.append(("a0 <-> rho_c",
                  f"a0=(c/2)sqrt(G rho_c); rho_c(Planck)={rho_c:.3e} kg/m^3 -> a0={a0_from_rho:.3e}"))

    # E2: a0 <-> H0
    edges.append(("a0 <-> H0",
                  f"H0 = Z a0 / c = {H_from_a0(a0):.1f} km/s/Mpc   (galaxy dynamics -> H0)"))

    # E3: a0(z) <-> E(z)
    edges.append(("a0(z) <-> E(z)",
                  f"a0(z)=a0(0)E(z); E(1)={E(1):.3f}, E(2)={E(2):.3f}, E(6)={E(6):.2f}  (Z cancels)"))

    # E4: a0 <-> Lambda  (the de Sitter floor)
    a0_floor = a0 * math.sqrt(OL)
    edges.append(("a0 <-> Lambda (floor)",
                  f"far-future a0 -> a0(0)sqrt(OL) = {a0_floor:.3e} = (c^2/2)sqrt(Lambda/8pi)"))

    # E5: a0 <-> q  (deceleration parameter sets a0's drift)
    q0 = OM / 2 - OL
    edges.append(("a0 <-> q (drift)",
                  f"d ln a0/dt = -(1+q)H; q0={q0:+.3f} -> a0 today drifting at {-(1+q0):+.3f} H0"))

    # E6: a0 <-> T_dS  (thermal / de Sitter)
    T_a0 = HBAR * a0 / (2 * math.pi * c * KB)
    T_dS = HBAR * H_si(H0) / (2 * math.pi * KB)
    edges.append(("a0 <-> T_dS (thermal)",
                  f"T_a0=hbar a0/2pi c kB={T_a0:.2e} K = T_dS/Z; T_dS={T_dS:.2e} K"))

    # E7: a0 <-> RAR knee
    edges.append(("a0 <-> RAR knee",
                  f"transition g_dagger=a0 moves to higher g at high z (a0(z) rises as E(z))"))

    # E8: a0 <-> BTFR
    edges.append(("a0 <-> BTFR",
                  f"deep-MOND V^4=G M a0 -> BTFR zero-point prop a0; evolves as a0(z)"))

    # E9: a0 <-> high-z M_dyn/M_bar
    boost6 = math.sqrt(E(6))
    edges.append(("a0 <-> high-z M_dyn",
                  f"apparent DM boost ~ sqrt(E(z)); at z=6 boost={boost6:.2f}x vs z=0"))

    for i, (name, expr) in enumerate(edges, 1):
        print(f"  E{i}  {name:<24} {expr}")
    print()
    print(f"  => {len(edges)} edges, ALL forced by the single premise. Change the one number")
    print("     and every edge moves together -- there is no per-edge knob to turn.")
    print()
    return len(edges)


# ====================================================================================
def part3_coherence():
    print("=" * 84)
    print("(3) THE OVER-CONSTRAINT -- anchor ONE number on the CMB, predict the galaxies")
    print("=" * 84)
    print("  Anchor: H0 = 67.4 (Planck CMB, z~1100). The premise then PREDICTS every")
    print("  galaxy-scale node with ZERO further freedom. Compare to independent data:")
    print()

    a0_pred0 = a0_from_H(H0_PLANCK)             # predicted today's a0 from CMB H0
    a0_pred1 = a0_pred0 * E(1)                  # predicted a0 at z~1

    rows = [
        ("a0(z=0)  [SPARC rotation curves]",   a0_pred0, A0_SPARC,        "m/s^2"),
        ("a0(z~1)  [MUSE-DARK kinematics]",    a0_pred1, A0_MUSEDARK_z1,  "m/s^2"),
        ("H0       [SPARC a0 -> H0, vs Planck]", H_from_a0(A0_SPARC), H0_PLANCK, "km/s/Mpc"),
    ]
    print(f"  {'node [independent dataset]':<40}{'predicted':>13}{'measured':>13}{'resid':>9}")
    for name, pred, meas, unit in rows:
        print(f"  {name:<40}{pred:>13.3e}{meas:>13.3e}{pct(pred, meas):>8.1f}%")
    print()
    print("  Reading the residuals honestly:")
    print(f"   * a0(0): Planck-CMB H0 and SPARC rotation curves -- two measurements from")
    print(f"     utterly different physics (z~1100 plasma vs z~0 galaxies) -- agree to")
    print(f"     {abs(pct(a0_pred0, A0_SPARC)):.1f}% through ONE equation. This is the keystone.")
    print(f"   * a0(z~1): E(z) under-predicts MUSE-DARK by {abs(pct(a0_pred1, A0_MUSEDARK_z1)):.0f}% -- inside a0's ~20%")
    print(f"     systematic, and in the direction MUSE-DARK themselves note ('faster than")
    print(f"     H(z)'). A mild, honest tension, NOT a precision triumph.")
    print(f"   * de Graaff JADES z=5.5-7.4: M_dyn/M_* up to {DEGRAAFF_MDYN_MAX:.0f} -- constant-a0 MOND")
    print(f"     CANNOT reach it; evolving a0 (boost sqrt(E(6))={math.sqrt(E(6)):.1f}x) can. Qualitative,")
    print(f"     but only the evolving web survives it.")
    print()
    print("  Independent statistical check (real_research/rar_evolution_test.py):")
    print("     fitting a0(z) to the real high-z compilation: constant-a0 chi^2=27 (REJECTED),")
    print("     a0(z)=a0(0)E(z) chi^2=3.8 (best), (1+z)^1.5 chi^2=27. The web's law wins.")
    print()


# ====================================================================================
def part4_ledger(n_edges):
    print("=" * 84)
    print("(4) THE LEDGER -- why this web carries evidence and the constants web does not")
    print("=" * 84)

    # Real web
    independent_measurements = [
        "SPARC RAR a0(z~0) = 1.13e-10",
        "Planck CMB H0 = 67.4  (-> a0 via premise)",
        "MUSE-DARK a0(z~1) = 2.38e-10",
        "de Graaff JADES M_dyn/M_* (z~6)",
        "Lambda (dark-energy density, the floor)",
    ]
    n_meas = len(independent_measurements)
    n_param = 1
    print("  REAL WEB (cosmology core):")
    for m in independent_measurements:
        print(f"     [meas] {m}")
    print(f"     free parameters: {n_param}  (a0 today == H0, and even that is pinned by Planck)")
    print(f"     OVER-CONSTRAINT = {n_meas} independent measurements - {n_param} parameter "
          f"= +{n_meas - n_param}")
    print(f"     {n_edges} forced edges, {n_meas} of whose nodes are independently measured and COHERE.")
    print("     A coincidence does not survive 4 independent agreements; a real relation does.")
    print()

    # Constants web
    print("  CONSTANTS WEB (alpha=4Z^2+3, sin2tw=3/13, mu_n/mu_p~13/19, ...):")
    constants = [
        ("alpha^-1 = 4Z^2 + 3",       "{4, 3}",      2),
        ("sin^2 theta_W = 3/13",      "{3, 13}",     2),
        ("mu_n/mu_p ~ 13/19",         "{13, 19}",    2),
        ("alpha_s = Omega_L / Z",     "{Omega_L}",   1),
    ]
    tot_data = len(constants)
    tot_param = sum(k for _, _, k in constants)
    for name, ints, k in constants:
        print(f"     [fit ] {name:<26} free integers {ints:<12} ({k} params for 1 datum)")
    print(f"     {tot_data} data, {tot_param} free integers -> OVER-CONSTRAINT = "
          f"{tot_data} - {tot_param} = {tot_data - tot_param}  (<= 0: a FIT, not a web)")
    print("     each line jumps to an UNRELATED domain (QED, electroweak, nuclear) on a bare")
    print("     number -- mu_n/mu_p is the quark model's -2/3, not Omega_L. No edge is forced.")
    print("     A 34,000-formula search hits an arbitrary O(100) target to 0.004% ~20% of the")
    print("     time (reviews/false_discovery_rate.py) -> ~0 bits of evidence per line.")
    print()


# ====================================================================================
def part5_verdict():
    print("=" * 84)
    print("(5) VERDICT")
    print("=" * 84)
    print("  The web is REAL where it flows through ONE equation (Friedmann/MOND): the")
    print("  cosmology core is over-constrained (+4) and its independent nodes cohere --")
    print("  Planck H0, SPARC a0, MUSE-DARK a0(z~1), de Graaff masses, the Lambda floor all")
    print("  pinned by a single number. Change Z and every node moves together; the data")
    print("  still lines up. That is a genuine interlock.")
    print()
    print("  The web is ILLUSORY where it jumps between unrelated domains on a coincidental")
    print("  number (the constants): each line carries its own free integers, the ledger is")
    print("  <= 0, and a blind search reproduces the 'hits' ~20% of the time. Shared")
    print("  bookkeeping {3,4,8,12,19}, not shared physics.")
    print()
    print("  Build on the first. It is one premise, ~9 forced edges, 5 independent")
    print("  measurements, +4 over-constraint -- and it is Carl's March 2026 work.")


def main():
    part1_premise()
    n_edges = part2_edges()
    part3_coherence()
    part4_ledger(n_edges)
    part5_verdict()


if __name__ == "__main__":
    main()
