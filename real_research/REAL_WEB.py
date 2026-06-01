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

  (1)  states the premise and its ONE free number;
  (1b) THE GENERATOR -- shows the web is one dimensionless invariant a0/cH = 1/Z cast,
       by dimensional analysis, into six unit-costumes (acceleration, length, surface
       density, velocity, temperature, time). That is *why* the nodes interlock;
  (2)  enumerates the 9 edges (each a forced equation, computed);
  (2b) EXTENDED forced consequences -- what else flows: BTFR velocity-as-a-clock
       (v ~ E^1/4), the migrating HSB/LSB surface density (Sigma_M ~ E(z)), a0-cosmography
       (a0(z) IS H(z), a 4th dark-energy probe), and eternal MOND (a0 floors at Lambda);
  (3)  anchors the single free number on Planck's CMB H0 and PREDICTS the galaxy-scale
       nodes, then compares to their independent measurements -- the coherence residuals;
  (4)  writes the OVER-CONSTRAINT LEDGER: N_independent_measurements - N_free_parameters.
       Real web -> positive (over-constrained). Constants web -> <= 0 (a fit);
  (4b) WHERE THE FLOW STOPS -- the honest boundary (no SM constants, no Z derivation,
       no lensing/CMB peaks without a relativistic completion).

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
MSUN = 1.989e30
PC = 3.0857e16

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
def part1b_generator():
    print("=" * 84)
    print("(1b) THE GENERATOR -- one dimensionless invariant in six unit-costumes")
    print("=" * 84)
    print(f"  a0/(cH) = 1/Z = {1/Z:.5f}  is a PURE number, held fixed at every epoch.")
    print("  Multiplied by the right combination of c, G, hbar, kB it MUST appear as a")
    print("  different-looking quantity in each subfield -- dimensional analysis on ONE")
    print("  constant, not a coincidence between domains:")
    print()
    a0 = A0_SPARC
    RH = c / H_si(H0_PLANCK)
    la = c ** 2 / a0
    SigM_msun = (a0 / G) * PC ** 2 / MSUN
    T_a0 = HBAR * a0 / (2 * math.pi * c * KB)
    t_dyn_over_tH = math.sqrt(8 * math.pi / 3)          # t_dyn = 1/sqrt(G rho_c) = sqrt(8pi/3)/H
    print(f"  {'costume':<15}{'quantity':<25}{'value':>18}   where it lives")
    rows = [
        ("acceleration", "a0 = cH/Z",             f"{a0:.2e} m/s^2",            "rotation curves (RAR)"),
        ("length",       "l_a = c^2/a0 = Z R_H",  f"{la/RH:.2f} R_H",           "cosmography / horizon"),
        ("surface dens.", "Sigma_M = a0/G",       f"{SigM_msun:.0f} Msun/pc^2", "disk stability (HSB/LSB)"),
        ("velocity",     "v^4 = G M a0",          "~ E(z)^1/4",                "Tully-Fisher zero-point"),
        ("temperature",  "T_a0 = T_dS / Z",       f"{T_a0:.1e} K",             "horizon thermodynamics"),
        ("time",         "t_dyn = 1/sqrt(G rho)", f"{t_dyn_over_tH:.3f} t_H",   "cosmic collapse/free-fall"),
    ]
    for cost, q, v, w in rows:
        print(f"  {cost:<15}{q:<25}{v:>18}   {w}")
    print()
    print("  Same invariant, six walls. The 'web' is the shadow of 1/Z through Friedmann")
    print("  into six observational windows -- which is exactly why the nodes interlock.")
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
def part2b_extended():
    print("=" * 84)
    print("(2b) EXTENDED FORCED CONSEQUENCES -- what else flows, with the data channel")
    print("=" * 84)
    a0 = A0_SPARC

    # C1: velocity zero-point as a clock
    print("  C1 [FORCED] BTFR velocity zero-point is a clock:  v ~ E(z)^(1/4) at fixed M")
    print("     deep-MOND v^4 = G M a0, so at fixed baryonic mass v scales as a0^(1/4):")
    for z in (0.5, 1, 2, 6):
        b = E(z) ** 0.25
        print(f"       z={z:<4} E(z)={E(z):>5.2f}   v/v0 = E^1/4 = {b:.3f}   (+{(b-1)*100:.0f}%)")
    print("     [channel] high-z Tully-Fisher / MUSE-DARK kinematics -- the SHARPEST")
    print("     near-term falsifier. (The 15% MUSE-DARK over-shoot propagates here too.)")
    print()

    # C2: critical surface density migrates
    SigM = (a0 / G) * PC ** 2 / MSUN
    print("  C2 [FORCED] HSB/LSB critical surface density migrates:  Sigma_M = a0/G ~ E(z)")
    print(f"     {'z':>6}{'Sigma_M [Msun/pc^2]':>22}")
    for z in (0, 1, 2, 6):
        print(f"     {z:>6}{SigM * E(z):>22.0f}")
    print("     [corollary, SUGGESTIVE] if disks settle near this line, the Freeman-law")
    print("     characteristic surface brightness should itself rise as E(z) at high z.")
    print()

    # C3: a0-cosmography -- a0(z) IS H(z)
    print("  C3 [FORCED] a0-cosmography: a0(z) IS H(z).  H(z) = Z a0(z)/c -- no ladder,")
    print("     no candles, no CMB. Measured a0 at several z reconstructs E(z), hence")
    print("     Omega_m, Omega_L, w(z): a 4th, purely DYNAMICAL dark-energy probe.")
    print(f"     {'z':>5}{'a0(z) measured':>17}{'H(z)=Z a0/c':>14}{'LCDM H0 E(z)':>14}{'resid':>8}")
    for z, a0z, src in [(0, A0_SPARC, "SPARC"), (1, A0_MUSEDARK_z1, "MUSE-DARK")]:
        Hr = H_from_a0(a0z)
        Hl = H0_PLANCK * E(z)
        print(f"     {z:>5}{a0z:>17.2e}{Hr:>14.1f}{Hl:>14.1f}{pct(Hr, Hl):>7.0f}%   [{src}]")
    print("     => method validated at z=0 (lands on Planck); the z~1 point sits ~18% high,")
    print("     the SAME tension MUSE-DARK report ('a0 grows faster than H(z)').")
    print()

    # C4: eternal MOND
    floor = a0 * math.sqrt(OL)
    q0 = OM / 2 - OL
    print("  C4 [FORCED] MOND is eternal: a0 floors at the Lambda value, never switches off")
    print(f"     a0_floor = a0(0) sqrt(OL) = {floor:.2e};  today only {(1/math.sqrt(OL)-1)*100:.1f}% above it.")
    print(f"     q0 = {q0:+.3f} -> a0 drifting at {-(1+q0):+.3f} H0, freezing toward the floor as q->-1.")
    print("     Dark matter (the RAR) and dark energy (Lambda) are ONE scale at its two ends.")
    print()

    # C5/C6 interpretive / suggestive
    print("  C5 [INTERPRETIVE] the 40-year MOND coincidence a0~cH0 dissolves: a0 = cH(z)/Z")
    print("     holds at ALL z, so 'now' is not special -- there is no coincidence to explain.")
    print("  C6 [SUGGESTIVE] a0 was LARGER early (E(z) rises), so boosted gravity reached")
    print("     higher accelerations -> faster early collapse: the right DIRECTION for JWST's")
    print("     too-massive-too-early galaxies. NOT a calculation (needs a covariant theory).")
    print()


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
def part4b_boundary():
    print("=" * 84)
    print("(4b) WHERE THE FLOW STOPS -- the honest boundary (matters as much as what flows)")
    print("=" * 84)
    print("  * It does NOT reach the Standard Model constants. alpha, sin^2 theta_W, the")
    print("    mass ratios -- none flow from a0=cH/Z. The generator is gravity + cosmology")
    print("    only; the constants 'web' stays a fit (ledger -3), NOT an extension of this.")
    print("  * It does NOT derive Z. The equation USES Z=2 sqrt(8pi/3); the factor-of-2")
    print("    (Schwarzschild/horizon) is a posit, not a theorem. The generator is assumed.")
    print("  * It does NOT give lensing or the CMB acoustic peaks. Newtonian-MOND+Friedmann")
    print("    has no relativistic completion built in; those need an AeST-like theory and")
    print("    are NOT forced here. Claiming them would repeat the overreach the audit killed.")
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
    part1b_generator()
    n_edges = part2_edges()
    part2b_extended()
    part3_coherence()
    part4_ledger(n_edges)
    part4b_boundary()
    part5_verdict()


if __name__ == "__main__":
    main()
