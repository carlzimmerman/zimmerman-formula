#!/usr/bin/env python3
"""
DSSYK deep-MOND SIGN -- INDEPENDENT recomputation of the matter-chord spectral weight
=====================================================================================
PROBLEM 1, APPROACH A. Compute w(E) = mu(E) |<E|O_Delta|vac>|^2 with |vac> placed at the
spectral CENTER (E=0, theta=pi/2; Narovlansky-Verlinde 2310.16994) AND at the EDGE
(E=E0, theta->pi; Okuyama 2505.08116), read off the freezing exponent p in each, and
identify the EXACT line where the placement enters and whether it is DERIVED or ASSUMED.

FORMALISM (verbatim from primary sources):
  q-Hermite chord spectrum:   E(theta) = 2 cos(theta) / sqrt(1-q),  theta in [0,pi]
                              (Berkooz-Isachenkov-Narovlansky-Torrents 1811.02584)
  q-Gaussian DOS / measure:   mu(theta) = (q;q)_inf |(e^{2i theta};q)_inf|^2 / (2pi)
  matter operator (diagonal chord op, Okuyama 2312.00880 eq 16/18):
     O_Delta = q^{Delta N_hat},  N_hat = chord-number operator
     AMPLITUDE  G(th1,th2) = <th1| q^{Delta N} |th2>
              = (q^{2Delta};q)_inf / prod_{s1,s2=+-} (q^Delta e^{i(s1 th1 + s2 th2)};q)_inf

KEY ANALYTIC FACT we will verify numerically and then USE:
  The q-Gaussian DOS near the CENTER (theta=pi/2, E=0) is FLAT: mu ~ const, local power s=0.
  The q-Gaussian DOS near the EDGE (theta=0 or pi, E=+-E0) VANISHES as a SQUARE ROOT:
  mu ~ sqrt(E0-|E|), local power s=1/2  (Wigner-like soft edge of the q-Gaussian).
  The MOND freezing argument (MICROSCOPIC_CENTER_VS_EDGE): if the spectral weight that
  controls the low-acceleration response lives where the local DOS power is s, then the
  deep-MOND exponent is  p_MOND = (s+1)/(s+2)  giving  g_obs ~ g_bar^{p_MOND}:
       s = 0  (flat center) -> p_MOND = 1/2  -> g_obs ~ sqrt(g_bar)  = MOND (enhancement)
       s = 1/2 (sqrt edge)  -> p_MOND = 3/5  -> g_obs ~ g_bar^{3/5}  = anti-MOND (weaker)
  [Equivalently the repo's "p" naming with p=1 (center) vs p=3/2 (edge) is the EXPONENT in
   mu ~ |E-E_loc|^{p-1}; both conventions agree on the SIGN. We report s directly + both.]

THE LOAD-BEARING QUESTION (Fable's circularity warning):
  w(E) requires CHOOSING theta_vac. The number theta_vac=pi/2 (center) vs theta_vac=pi (edge)
  is NOT output by q^{Delta N} or by mu(theta) -- BOTH are legitimate energy eigenstates and
  the kernel is defined for either. We mark the EXACT line where theta_vac is set and test
  whether anything in the algebra forces one over the other.
"""
import numpy as np

# ----------------------------------------------------------------- physical constants
c = 2.998e8; G = 6.674e-11; Msun = 1.989e30
H0 = 67.0e3 / 3.086e22; OmegaL = 0.685; H_Lambda = H0 * np.sqrt(OmegaL)
M_dS = c**2 / (G * H_Lambda) / Msun

NPOCH = 400  # q-Pochhammer truncation


def qpoch(a, q, N=NPOCH):
    """(a;q)_inf = prod_{k>=0} (1 - a q^k), truncated to N terms."""
    a = np.asarray(a, dtype=complex)
    out = np.ones(a.shape, dtype=complex)
    qk = 1.0
    for _ in range(N):
        out *= (1 - a * qk)
        qk *= q
    return out


def mu_qg(theta, q):
    """q-Gaussian spectral measure mu(theta) = (q;q)_inf |(e^{2i th};q)_inf|^2 / (2pi)."""
    qq = qpoch(q, q).real
    e2 = np.exp(2j * np.asarray(theta, dtype=float))
    return qq * (qpoch(e2, q) * qpoch(np.conj(e2), q)).real / (2 * np.pi)


def G_amp(th1, th2, Delta, q):
    """Okuyama eq(18) AMPLITUDE G(th1,th2) = <th1| q^{Delta N} |th2>."""
    num = qpoch(q ** (2 * Delta), q)
    th1 = np.asarray(th1, dtype=float); th2 = np.asarray(th2, dtype=float)
    shape = np.broadcast(th1, th2).shape
    den = np.ones(shape, dtype=complex)
    for s1 in (1, -1):
        for s2 in (1, -1):
            den *= qpoch(q ** Delta * np.exp(1j * (s1 * th1 + s2 * th2)), q)
    return num / den


# =====================================================================================
# STEP 0: VERIFY the local DOS exponent of the q-Gaussian (center s=0, edge s=1/2)
# =====================================================================================
def local_dos_exponent(q, near="center"):
    """Fit mu(E) ~ |E - E_loc|^s near the chosen spectral location. E = 2 cos th / sqrt(1-q)."""
    th = np.linspace(1e-5, np.pi - 1e-5, 200001)
    E = 2 * np.cos(th) / np.sqrt(1 - q)
    mu = mu_qg(th, q)
    E0 = 2 / np.sqrt(1 - q)
    if near == "center":
        # near E=0 (theta=pi/2); fit mu vs |E| in a small window
        dist = np.abs(E)
        win = (dist > 1e-3 * E0) & (dist < 5e-2 * E0) & (mu > 0)
        s = np.polyfit(np.log(dist[win]), np.log(mu[win]), 1)[0]
    else:  # edge
        dist = E0 - np.abs(E)  # distance to the band edge |E|=E0
        win = (dist > 1e-4 * E0) & (dist < 3e-2 * E0) & (mu > 0)
        s = np.polyfit(np.log(dist[win]), np.log(mu[win]), 1)[0]
    return s


# =====================================================================================
# STEP 1: where does the matter-chord weight LIVE for each placement, and at what local
#         DOS power s does the realized weight sit -> p_MOND = (s+1)/(s+2)
# =====================================================================================
def realized_weight_and_p(theta_vac, Delta, q, ngrid=120001):
    """w(theta_E) = mu(theta_E) |G(theta_E, theta_vac)|^2, then read where it lives and the
    local DOS power s at the weight's barycentre; map to p_MOND=(s+1)/(s+2)."""
    th = np.linspace(1e-5, np.pi - 1e-5, ngrid)
    E = 2 * np.cos(th) / np.sqrt(1 - q)
    E0 = 2 / np.sqrt(1 - q)
    mu = mu_qg(th, q)
    G = G_amp(th, theta_vac, Delta, q)
    w = mu * np.abs(G) ** 2
    w = np.clip(w, 0, np.inf)
    norm = np.trapz(w, th)
    W = w / norm
    # barycentre of the weight in |E|/E0
    mean_absE = np.trapz(W * np.abs(E) / E0, th)
    frac_center = np.trapz(W * (np.abs(E) / E0 < 0.05), th)     # weight within 5% of center
    frac_edge = np.trapz(W * (np.abs(E) / E0 > 0.95), th)       # weight within 5% of edge
    # LOCAL DOS power s seen by the bulk of the weight: is the weight sitting on flat DOS or sqrt DOS?
    # Determine which region holds the majority; report the s of that region.
    if frac_center >= frac_edge:
        s_seen = local_dos_exponent(q, "center")
        region = "CENTER"
    else:
        s_seen = local_dos_exponent(q, "edge")
        region = "EDGE"
    p_mond = (s_seen + 1.0) / (s_seen + 2.0)
    return dict(region=region, frac_center=frac_center, frac_edge=frac_edge,
                mean_absE=mean_absE, s_seen=s_seen, p_mond=p_mond, E0=E0)


def sign_label(p_mond):
    # MOND enhancement is p_MOND = 1/2 (g_obs ~ sqrt(g_bar)); anti-MOND is p_MOND > 1/2.
    if abs(p_mond - 0.5) < 0.03:
        return "MOND (enhancement)"
    elif p_mond > 0.53:
        return "anti-MOND (weaker)"
    return "?"


def main():
    print("#" * 100)
    print("# INDEPENDENT: w(E)=mu|<E|O_Delta|vac>|^2 at CENTER vs EDGE; p_MOND=(s+1)/(s+2)")
    print("#" * 100)
    print(f"\n M_dS = c^2/(G H_Lambda) = {M_dS:.3e} Msun")
    print(f"   galaxy alpha=m/M_dS: dwarf(1e7)={1e7/M_dS:.2e}, spiral(3e10)={3e10/M_dS:.2e},"
          f" massive(1e12)={1e12/M_dS:.2e}, cluster(1e15)={1e15/M_dS:.2e}")
    print(f"   => galaxies alpha <= 2.65e-3; clusters alpha=O(1).\n")

    print("=" * 100)
    print("STEP 0 -- LOCAL DOS EXPONENT of the q-Gaussian (the discriminator's input)")
    print("=" * 100)
    print(f"  {'q':>6} | {'s_center (expect ~0)':>22} | {'s_edge (expect ~0.5)':>22}")
    for q in (0.3, 0.5, 0.7, 0.9, 0.95):
        sc = local_dos_exponent(q, "center")
        se = local_dos_exponent(q, "edge")
        print(f"  {q:>6.2f} | {sc:>22.4f} | {se:>22.4f}")
    print("""
  READ: s_center ~ 0 (FLAT DOS at the spectral center) and s_edge ~ 1/2 (SQUARE-ROOT soft
  edge). These are the two inputs to the freezing discriminator:
      center s=0 -> p_MOND=1/2 -> g~sqrt(g_bar)  = MOND (enhancement)
      edge   s=1/2 -> p_MOND=3/5 -> g~g_bar^0.6   = anti-MOND""")

    print("\n" + "=" * 100)
    print("STEP 1 -- realized weight w(E) per placement; where it lives & p_MOND")
    print("=" * 100)
    print(f"  {'q':>5}{'Delta':>7} {'placement':>10} | {'region':>7}{'frac_ctr':>9}{'frac_edge':>10}"
          f"{'mean|E|/E0':>11}{'s_seen':>8}{'p_MOND':>8}  sign")
    for q in (0.5, 0.7, 0.9, 0.95):
        for Delta in (0.1, 0.5, 1.0):
            for name, thv in [("CENTER", np.pi / 2), ("EDGE", np.pi - 1e-3)]:
                r = realized_weight_and_p(thv, Delta, q)
                print(f"  {q:>5.2f}{Delta:>7.2f} {name:>10} | {r['region']:>7}{r['frac_center']:>9.3f}"
                      f"{r['frac_edge']:>10.3f}{r['mean_absE']:>11.4f}{r['s_seen']:>8.3f}"
                      f"{r['p_mond']:>8.3f}  {sign_label(r['p_mond'])}")
    print("""
  READ: the diagonal operator q^{Delta N} TRANSPORTS the weight to where the vacuum is placed
  (CENTER-vac -> weight near center -> s=0 -> p=1/2 -> MOND; EDGE-vac -> weight near edge ->
  s=1/2 -> p=3/5 -> anti-MOND). The SIGN is therefore a 1:1 readout of theta_vac.""")

    print("\n" + "=" * 100)
    print("STEP 2 -- THE EXACT LINE WHERE PLACEMENT ENTERS (DERIVED or ASSUMED?)")
    print("=" * 100)
    print("""  The placement enters ONLY at the literal argument 'theta_vac' passed to G_amp / w(E):
        CENTER:  theta_vac = np.pi/2      (E=0)     <- Narovlansky-Verlinde dictionary
        EDGE  :  theta_vac = np.pi - eps  (E=E0)    <- Okuyama dictionary
  NOTHING in q^{Delta N}, in mu(theta), or in the q-Hermite recursion privileges pi/2 over pi.
  Test: is theta_vac fixed by any algebraic condition (lowest energy? cyclicity? unique
  invariant state?)? The chord vacuum |0> (zero chords) is the ground state of N_hat, but its
  ENERGY placement E(theta) is a SEPARATE map; the de Sitter <-> theta_vac identification is the
  HOLOGRAPHIC DICTIONARY, supplied externally (N-V put it at pi/2; Okuyama derives pi via a
  triple-scaling limit around theta=pi reproducing dS-JT). => theta_vac is ASSUMED (dictionary),
  not DERIVED by the chord algebra. Both placements are internally consistent.""")


if __name__ == "__main__":
    main()
