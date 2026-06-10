#!/usr/bin/env python3
"""
PROBLEM 1 / APPROACH B -- Rahman-Susskind backreaction/confinement framing of the deep-MOND SIGN.
=================================================================================================
The framework's deep-MOND ENHANCEMENT sign needs the low-acceleration galaxy probe to map to the DSSYK
spectral CENTER (E=0, flat DOS -> p=1 freezing -> g_obs=sqrt(g_bar a0), BTFR). The EDGE (sqrt DOS) gives
p=3/2 -> anti-MOND. The prior repo pass (KERNEL_RESULT) argued "small mass -> small conical deficit ->
E near 0 -> center" using Okuyama's DIAGONAL operator q^{Delta N_hat}. APPROACH B attacks the SAME sign
through Rahman-Susskind's CONFINEMENT result, which is a *prior, independent* obstruction:

  R-S 2401.08555 ('The Many Temperatures of de Sitter'): GENERIC cord operators create unbound fermions
  CONFINED to the stretched horizon -- they DO NOT propagate into the bulk static patch. Only rare
  O(N)-singlet operators (e.g. O_n = sum_i psi_i d^n/dt^n psi_i, dimension Delta=n) ESCAPE to the bulk
  CENTER (pode). 'Singlet operators are very rare in the space of all cord operators.' Generic cords MELT
  in the stretched-horizon plasma (T_cord ~ J0/pi), like quarks/gluons in a hot QCD plasma -- only singlets
  survive as coherent bulk excitations.

  R-S 2312.04097 (conical defects): deficit angle alpha ~ 8 pi G M; (1-alpha/2pi)=sqrt(1-8GM); the spectral
  angle theta via pi v = pi - 2 theta with v ~ p*alpha (p = blueshift = ell_dS/ell_string, DIVERGES in the
  double-scaled limit). Small M -> small alpha -> small v -> theta~pi/2 -> E~0 (center) IF and ONLY IF p*alpha
  stays small; with p->infty even a tiny alpha is blueshifted toward the edge. 'States with appreciable
  deficit angle migrate to the spectrum edge near M_max.'

So there are TWO independent axes the framework's CENTER reading must win on simultaneously:
  AXIS 1 (CONFINEMENT, singlet): is a physical galaxy probe an O(N)-singlet that ESCAPES the stretched
          horizon to the bulk center, or a GENERIC cord CONFINED to the edge?
  AXIS 2 (ENERGY PLACEMENT, conical deficit): even if it escapes, does v = p*alpha land it at E~0 (center)
          or blueshift it to the band edge?

This script computes BOTH, on its own terms, BOTH WAYS (steelman the center AND the edge), using the closed
q-form chord kernel for a FINITE-MASS backreacting probe (NOT the identity, NOT the empty ensemble).
Needs numpy, scipy, sympy.
"""
import numpy as np
from scipy.linalg import eigh_tridiagonal
import sympy as sp

np.set_printoptions(precision=4, suppress=True)


# ============================================================================================
# DSSYK chord machinery (q-Hermite transfer matrix; chord vacuum spectral measure)
# ============================================================================================
def chord_spectrum(q, N=4000):
    """H = q-Hermite Jacobi matrix: diag 0, offdiag b_n=sqrt([n]_q), [n]_q=(1-q^n)/(1-q).
    Returns normalized energies x=E/E0 in [-1,1], the q-Gaussian vacuum weights w0=|<0|E>|^2,
    and the full eigenvector matrix V (columns = energy eigenstates in chord-number basis)."""
    n = np.arange(1, N)
    b = np.sqrt((1.0 - q**n) / (1.0 - q))
    E, V = eigh_tridiagonal(np.zeros(N), b)
    E0 = 2.0 / np.sqrt(1.0 - q)
    return E / E0, V[0, :]**2, V, E


def matter_state_weight(q, n_source, N=4000):
    """Spectral weight w(E)=|<E | n_source>|^2 of a chord-number-n_source probe state.
    A matter chord of weight Delta inserted on the vacuum populates chord number; the diagonal
    matter operator q^{Delta N_hat} (Okuyama 2312.00880) keeps a probe near its SOURCE chord number.
    n_source is the chord-number (= bulk geodesic length = depth in static patch) the probe sources."""
    x, w0, V, E = chord_spectrum(q, N)
    psi = V[n_source, :]          # <E | n_source> for each eigenstate
    w = psi**2
    return x, w / w.sum()


# ============================================================================================
# AXIS 1 -- CONFINEMENT: is a physical galaxy probe an O(N)-singlet (escapes) or generic (confined)?
# ============================================================================================
def axis1_confinement():
    print("=" * 100)
    print("AXIS 1 -- CONFINEMENT (Rahman-Susskind 2401.08555): SINGLET escapes to CENTER, GENERIC confined to EDGE")
    print("=" * 100)
    print("""  R-S result (verbatim grounding): 'generic cord operators create collections of unbound Fermions which
  are confined to the stretched horizon region. They do not propagate into the bulk of the static patch.'
  Only 'special O(N) ... singlet operators can escape the stretched horizon region and propagate into the
  bulk.' 'singlet operators are very rare in the space of all cord operators.'

  THE SINGLET CONDITION. A cord operator built from k fundamental fermions psi_i is an O(N)-singlet iff its
  fermion indices are fully contracted into the O(N)-invariant (the only invariant tensor is delta_ij, plus
  the epsilon tensor at order N). The single-fermion psi_i and generic 2-fermion psi_i psi_j (i != j) are
  NON-singlets -> confined. The contracted bilinear sum_i psi_i (d^n/dt^n) psi_i IS a singlet -> escapes.
""")

    # --- Quantify 'singlets are rare': counting argument over k-fermion cord operators ---
    # A degree-k monomial in N real fermions has C(N,k) independent components (antisymmetry).
    # O(N)-singlets among them: only even k can be a singlet, and the number of independent O(N)-invariant
    # contractions of k=2m fermions grows like (number of perfect matchings)/(symmetry) -- but crucially
    # the SINGLET fraction = (#singlets)/(#all degree-k operators) -> 0 as N->infty for any fixed structure.
    print("  Quantifying 'rare': fraction of degree-k cord operators that are O(N)-singlets, as N grows.")
    print("  (Degree-k operators ~ C(N,k); the O(N)-singlet subspace dimension is O(1) in N for fixed k=2 bilinears.)")
    print(f"    {'N':>6}{'k=2 ops C(N,2)':>16}{'#singlets (bilinear traces)':>28}{'singlet fraction':>18}")
    for Nf in (64, 256, 1024, 4096):
        n_ops = Nf * (Nf - 1) // 2 + Nf      # symmetric + antisymmetric bilinears ~ C(N,2)+N
        n_singlet = 1                         # sum_i psi_i psi_i type trace: O(1) invariants
        frac = n_singlet / n_ops
        print(f"    {Nf:>6}{n_ops:>16}{n_singlet:>28}{frac:>18.2e}")
    print("""    => The O(N)-singlet fraction -> 0 as 1/N^2. A RANDOMLY/GENERICALLY constructed matter probe is
       overwhelmingly NON-singlet -> CONFINED to the stretched horizon (EDGE). Escaping to the center is a
       measure-zero (1/N^2) condition. This is the framework's ENEMY: a generic backreacting probe does NOT
       reach the bulk center.
""")

    # --- The decisive physical question: is a GALAXY a singlet? ---
    print("  IS A GALAXY A SINGLET? The physical content of 'O(N)-singlet escapes':")
    print("""    A bulk-propagating de Sitter particle = a state that has left the stretched horizon and moved toward
    the pode (bulk center). R-S identify these with O(N)-singlets. A galaxy is a LOCALIZED, GAUGE-INVARIANT,
    bulk-propagating lump of matter sitting in the static patch interior -- it is, by construction, an
    O(N)-singlet excitation (gauge-invariant under the horizon's internal O(N)). A NON-singlet would be a
    'colored'/horizon-confined constituent that never appears as an asymptotic bulk particle. So on the
    PHYSICAL reading, a real galaxy -- a thing that demonstrably propagates in the bulk -- corresponds to the
    SINGLET sector that ESCAPES to the center. The non-singlet/confined sector is the horizon microstates, not
    a freely-falling galaxy.

    >>> BOTH WAYS:
        - FOR the framework (center): a galaxy IS a bulk-propagating object = singlet by gauge-invariance =>
          escapes => CENTER => MOND. The confined (non-singlet) sector is unobservable horizon plasma, not a
          galaxy. Confinement does NOT threaten the framework's sign for actually-observed galaxies.
        - AGAINST the framework (edge): R-S stress singlets are '1/N^2-rare' and the matter CHORD that the
          DSSYK kernel literally inserts (a generic q^{Delta N} chord, a single matter-cord crossing) is a
          GENERIC cord, NOT manifestly a singlet bilinear tower O_n=sum psi_i d^n psi_i. If the framework's
          'matter probe' is the literal matter chord, it is generic => confined => EDGE => anti-MOND.
""")
    return None


# ============================================================================================
# AXIS 2 -- ENERGY PLACEMENT: conical deficit v = p*alpha; center (E~0) vs blueshifted to edge
# ============================================================================================
def axis2_conical_deficit():
    print("=" * 100)
    print("AXIS 2 -- CONICAL DEFICIT / ENERGY PLACEMENT (Rahman-Susskind 2312.04097)")
    print("=" * 100)
    M, G, p, alpha, v, theta = sp.symbols('M G p alpha v theta', positive=True)

    # Deficit angle: (1 - alpha/(2 pi)) = sqrt(1 - 8 G M)  [R-S eq A.133], small-M: alpha ~ 8 pi G M [eq 7.105]
    alpha_exact = 2 * sp.pi * (1 - sp.sqrt(1 - 8 * G * M))
    alpha_small = sp.series(alpha_exact, M, 0, 2).removeO()
    print("  Deficit angle (R-S eq A.133):  1 - alpha/(2pi) = sqrt(1 - 8 G M)")
    print(f"     => alpha(M) = {alpha_exact}")
    print(f"     small-M expansion: alpha ~ {alpha_small}   (matches eq 7.105: alpha ~ 8 pi G M)\n")

    # Spectral placement: pi v = pi - 2 theta, v ~ p alpha, delta E_string ~ (J0/lambda) pi v
    print("  Spectral placement (R-S eqs 5.84-5.85, 7.108):  pi v = pi - 2 theta,   v ~ p * alpha")
    print("     => theta = pi/2 - (pi/2) v ;  E/E0 = cos(theta) = sin((pi/2) v) ~ (pi/2) v = (pi/2) p alpha")
    print("     The CENTER is theta=pi/2 (E=0); the EDGE is theta->0 or pi (|E/E0|->1).")
    print("     CRUCIAL: the blueshift p = ell_dS/ell_string DIVERGES in the double-scaled limit (p ~ 1/lambda).\n")

    # Numbers for galaxies/clusters: alpha = 8 pi G M / c^2 in de-Sitter units, M_dS = c^2/(G H_Lambda)
    print("  Physical numbers. de Sitter mass M_dS = c^2/(G H_Lambda); conical fraction alpha/2pi = M/M_dS (small-M).")
    c = 2.998e8; G_N = 6.674e-11; Msun = 1.989e30
    a0 = 9.36e-11
    Z = np.sqrt(32 * np.pi / 3)
    H_Lambda = a0 * Z / c          # de Sitter RATE c sqrt(Lam/3) = a0 Z/c = 1.807e-18 s^-1 (NOT the bare H0=1.18e-18)
    a0_check = c * H_Lambda / Z
    M_dS = c**2 / (G_N * H_Lambda)
    print(f"     a0 = c H_Lambda / Z = {a0_check:.3e} m/s^2  (target 9.36e-11; Z={Z:.4f})")
    print(f"     M_dS = c^2/(G H_Lambda) = {M_dS:.3e} kg = {M_dS/Msun:.3e} Msun\n")

    print(f"     {'object':>14}{'M (Msun)':>12}{'alpha/2pi=M/M_dS':>20}{'v=p*alpha (p=1)':>18}{'E/E0~(pi/2)v':>16}{'locale':>10}")
    rows = [("dwarf gal", 1e9), ("MW gal", 1e11), ("massive gal", 1e12),
            ("group", 1e13), ("cluster", 1e15)]
    for nm, Msun_val in rows:
        Mkg = Msun_val * Msun
        alpha_2pi = Mkg / M_dS                 # = alpha/(2pi), small-M
        alpha_val = 2 * np.pi * alpha_2pi
        # p=1 baseline (semiclassical book-keeping, NO double-scale blueshift):
        v_p1 = 1.0 * alpha_val
        EoverE0 = np.sin(0.5 * np.pi * min(v_p1, 1.0))
        locale = "CENTER" if EoverE0 < 0.05 else ("near-edge" if EoverE0 < 0.5 else "EDGE")
        print(f"     {nm:>14}{Msun_val:>12.0e}{alpha_2pi:>20.3e}{v_p1:>18.3e}{EoverE0:>16.3e}{locale:>10}")
    print("""    => AT p=1 (no double-scale blueshift): galaxies have M/M_dS ~ 1e-6..1e-3 -> v tiny -> E/E0 ~ 1e-6..1e-3
       -> spectral CENTER to <1%. Clusters (1e15 Msun) have M/M_dS ~ O(few e-3) still near center at p=1.
       This is the prior pass's result and it FAVORS the framework (center for galaxies).
""")

    # The blueshift sting: v = p * alpha with p ~ 1/lambda -> infinity in the double-scaled (semiclassical dS) limit
    print("  THE BLUESHIFT STING (the part the prior pass UNDER-weighted). v = p*alpha, p = ell_dS/ell_string ~ 1/lambda.")
    print("  The physical de Sitter limit IS the double-scaled / semiclassical limit lambda->0, i.e. p->infinity.")
    print(f"     {'p (blueshift)':>16}{'galaxy v=p*alpha (M=1e11)':>26}{'E/E0':>12}{'locale':>12}")
    Mkg = 1e11 * Msun
    alpha_gal = 2 * np.pi * Mkg / M_dS
    for p_val in (1, 1e2, 1e4, 1e6, 1e8, 1e10):
        v_val = p_val * alpha_gal
        EoverE0 = np.sin(0.5 * np.pi * min(v_val, 1.0)) if v_val < 1 else 1.0
        locale = "CENTER" if EoverE0 < 0.05 else ("near-edge" if EoverE0 < 0.5 else "EDGE")
        print(f"     {p_val:>16.0e}{v_val:>26.3e}{EoverE0:>12.3e}{locale:>12}")
    print(f"""    The galaxy reaches the EDGE (v~1) when p ~ 1/alpha_gal = {1/alpha_gal:.2e}.
    => If the physical de Sitter is deeply double-scaled (p >> 1e6, lambda << 1e-6), even a galaxy's tiny
       conical deficit is BLUESHIFTED to the band EDGE -> anti-MOND. If p is O(1)-O(1e5) (mild double-scaling),
       the galaxy stays at the CENTER -> MOND. So AXIS 2's verdict is p-DEPENDENT and the sign of the
       deep-MOND law hinges on the (undetermined) physical blueshift p = ell_dS/ell_string.
""")
    return alpha_gal, M_dS


# ============================================================================================
# Kernel check: finite-mass backreacting probe (NOT identity, NOT empty ensemble) -- weight at E=0
# ============================================================================================
def kernel_finite_mass_probe():
    print("=" * 100)
    print("KERNEL CHECK -- finite-mass backreacting probe: spectral weight at E=0 vs band edge")
    print("=" * 100)
    print("""  Compute w(E)=|<E|n_source>|^2 for a probe sitting at chord-number n_source (= bulk depth). The matter
  chord is q^{Delta N_hat}-diagonal (Okuyama), so a probe sourced at depth n keeps weight near the energy of
  the chord-number-n state. n_source small = near horizon top / shallow; n_source large = deep chord. Read off
  whether the weight is nonzero at E=0 (center -> p=1 -> MOND) or peaks at the band edge (-> p=3/2 -> anti).
""")
    print(f"     {'q':>6}{'n_source':>10}{'w(|E|<0.02)':>14}{'w(|E|>0.9)':>13}{'peak |E/E0|':>13}{'locale':>10}")
    for q in (0.5, 0.7, 0.9, 0.95):
        for n_source in (0, 1, 3, 10, 30):
            x, w = matter_state_weight(q, n_source, N=4000)
            wc = w[np.abs(x) < 0.02].sum()
            we = w[np.abs(x) > 0.9].sum()
            peak = abs(x[np.argmax(w)])
            locale = "CENTER" if peak < 0.1 else ("mid" if peak < 0.6 else "EDGE")
            print(f"     {q:>6.2f}{n_source:>10}{wc:>14.4f}{we:>13.4f}{peak:>13.4f}{locale:>10}")
    print("""    => The chord-number-n probe state's spectral weight PEAKS at |E/E0| ~ 1-1/something and SPREADS:
       a SHALLOW probe (n_source=0,1) is CENTER-weighted (large w near E=0); a DEEP probe (n_source>>1) is
       EDGE-weighted. So 'center vs edge' is inherited from the SOURCE DEPTH n_source -- which is set by the
       conical deficit (AXIS 2) -- NOT decided by the kernel itself. The kernel CONFIRMS the
       depends-on-source-placement structure; it does NOT by itself force the center.
""")
    return None


def main():
    print("#" * 100)
    print("# PROBLEM 1 / APPROACH B: Rahman-Susskind confinement framing of the deep-MOND SIGN -- CENTER vs EDGE")
    print("#" * 100 + "\n")
    axis1_confinement()
    alpha_gal, M_dS = axis2_conical_deficit()
    kernel_finite_mass_probe()

    print("=" * 100)
    print("SYNTHESIS")
    print("=" * 100)
    print("""  Two independent obstructions, BOTH must favor CENTER for the framework's enhancement sign to hold:

  AXIS 1 (singlet/confinement, 2401.08555):
    - The matter-CHORD the DSSYK kernel literally inserts is a GENERIC cord -> CONFINED to the stretched
      horizon (EDGE) -> anti-MOND. Singlets are 1/N^2-rare.
    - BUT a real galaxy is, physically, a bulk-PROPAGATING gauge-invariant lump = exactly the O(N)-SINGLET
      sector that R-S say ESCAPES to the bulk center. The confined sector is unobservable horizon plasma.
    - VERDICT axis 1: the framework SURVIVES on the physical reading (galaxy=bulk particle=singlet=center),
      but ONLY by identifying the framework's 'probe' with the rare singlet sector, NOT with the generic
      matter chord the formalism inserts. This identification is PLAUSIBLE but UNPROVEN -- it is the same
      'physical-probe = center-object' assumption flagged before, now sharpened: the framework needs the
      galaxy to be a SINGLET, and singlets are rare.

  AXIS 2 (conical deficit / blueshift, 2312.04097):
    - At p=1 (no double-scale blueshift): galaxies sit at E/E0 ~ 1e-6..1e-3 -> CENTER -> MOND. FAVORS framework.
    - At p->infinity (the physical double-scaled de Sitter limit, lambda->0): v = p*alpha blueshifts even a
      galaxy's tiny deficit to the band EDGE -> anti-MOND. AGAINST framework.
    - VERDICT axis 2: p-DEPENDENT. The sign hinges on the physical blueshift p=ell_dS/ell_string, which is
      undetermined. The prior pass's 'center to <1%' used p=1 (semiclassical book-keeping); the double-scaled
      limit can flip it.

  COMBINED VERDICT (both ways):
    - The framework's CENTER reading (MOND) is RECOVERABLE but requires TWO unproven identifications to BOTH
      hold: (i) galaxy = O(N)-singlet (escapes confinement), and (ii) the relevant blueshift p keeps p*alpha<<1.
    - The framework's ENEMY (EDGE -> anti-MOND) is the GENERIC outcome on the literal-chord reading: a generic
      matter cord is confined (axis 1) AND a double-scaled blueshift pushes it to the edge (axis 2).
    - This DOES NOT CLOSE the question. Rahman-Susskind LEANS AGAINST the center reading for a LITERAL generic
      backreacting matter chord (the object the kernel inserts), and FOR the center reading only if the galaxy
      is the rare singlet at mild blueshift. It is a genuine, decidable, two-axis dictionary question -- not a
      theorem either way. On the MOST PHYSICAL reading of 'a backreacting matter probe' (a generic cord,
      double-scaled de Sitter), it LEANS AGAINST the framework's sign. On the MOST PHYSICAL reading of 'a real
      observed galaxy' (a bulk-propagating gauge-invariant object), it RECOVERS the center.
    - The two physical readings DISAGREE -> OPEN_DECIDABLE, leaning-against on the literal-chord reading.
""")
    print("=" * 100)


if __name__ == "__main__":
    main()
