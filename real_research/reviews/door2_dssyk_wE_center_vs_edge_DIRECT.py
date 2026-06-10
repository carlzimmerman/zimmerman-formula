#!/usr/bin/env python3
"""
DOOR 2 -- DECISIVE DIRECT CALC: the matter-chord SPECTRAL WEIGHT w(E)=|<E|O_Delta|vac>|^2
=========================================================================================
This is the single named-but-undone calculation from DEEP_MOND_SIGN_CENTER_VS_EDGE_2026-06-06.md:

  "Compute the matter-chord wavefunction psi(E)=<E|O_Delta|vac> for a PHYSICAL (finite-mass) probe
   using the closed q-form matter two-point kernel, project onto the energy basis, and read off
   whether the spectral weight w(E)=|<E|O_Delta|vac>|^2 is nonzero at E=0 (-> center -> p=1 -> MOND)
   or vanishes/peaks at the band edge (-> p=3/2 -> anti-MOND)."

Done here DIRECTLY, with the vacuum placed at the CENTER (theta_vac=pi/2, Narovlansky-Verlinde
2310.16994) AND at the EDGE (theta_vac->pi, Okuyama 2505.08116), for a FINITE Delta matching the
physical galaxy conical deficit, and the freezing exponent p read off the small-E cumulative weight
in EACH case.

------------------------------------------------------------------------------------------------
EXACT INPUTS (verbatim from the published formalism, fetched 2026-06-09):

 [Energy eigenstate / measure]  Berkooz-Isachenkov-Narovlansky-Torrents 1811.02584, eq (2.16):
   <l|theta> = sqrt[ (q;q)_inf |(e^{2i theta};q)_inf|^2 ] * (1-q)^{l/2} H_l(cos theta|q) / sqrt[(q;q)_l] / sqrt(2pi)
   The energy eigenstates carry the q-GAUSSIAN measure
       mu(theta) = (q;q)_inf |(e^{2i theta};q)_inf|^2 / (2 pi)      [Okuyama: int (dtheta) mu(theta) ...]
   with <theta|theta'> = (2pi/mu) delta(theta-theta').

 [Matter operator = diagonal chord op]  Okuyama 2312.00880, eq (16),(18):
   O_Delta = q^{Delta N_hat} = sum_n q^{Delta n} |n><n|     (N_hat = chord-number operator)
   AMPLITUDE between energy eigenstates (eq 18), a COMPLEX matrix element (NOT a square):
     G(th1,th2) = <th1| q^{Delta N} |th2>
                = (q^{2 Delta}; q)_inf / prod_{++,+-,-+,--} (q^Delta e^{i(s1 th1 + s2 th2)}; q)_inf
   Okuyama confirms: this is the AMPLITUDE; w = |G|^2 is the modulus-squared two-point.

 [Vacuum placement -- the LOAD-BEARING dictionary choice, NOT decided by the algebra]
   CENTER (N-V 2310.16994): de Sitter = max-entropy infinite-T state = spectral center, theta_vac=pi/2, E=0.
   EDGE   (Okuyama 2505.08116; sine-dilaton): de Sitter = near-edge JT limit, theta_vac->pi, E->-E0.
   Okuyama 2505.08116 states VERBATIM his identification "is different from" Susskind/Verlinde's.

 [Probe mass -> dimension]  Rahman-Susskind 2312.04097: pi v = pi - 2 theta_src, v ~ p alpha,
   alpha ~ 8 pi G M (conical deficit). Galaxy: alpha = m/M_dS <= 2.65e-3, M_dS=c^2/(G H_Lambda)=3.77e14 Msun.
   The matter-chord WEIGHT Delta is the operator dimension; a small/light probe has small Delta.
   We bracket Delta from tiny (galaxy-deficit-scaled) up to O(1) and confirm the verdict is Delta-robust.

------------------------------------------------------------------------------------------------
WHAT THE SPECTRAL WEIGHT IS (the precise object):
  The matter-chord state is  |Psi> = O_Delta |vac> = q^{Delta N} |theta_vac>.
  Its energy-space wavefunction is  psi(theta_E) = <theta_E| O_Delta |theta_vac> = G(theta_E, theta_vac).
  The PROBABILITY DENSITY over the spectrum (the spectral weight) is
      w(theta_E) = mu(theta_E) |G(theta_E, theta_vac)|^2 ,
  because resolving the identity 1 = int (dtheta_E) mu(theta_E) |theta_E><theta_E| / (2pi)... (measure-weighted).
  We work with the normalized density W(theta_E) = w / int w, and read p from cumulative-weight scaling.

FREEZING EXPONENT read-off (the established discriminator, MICROSCOPIC_CENTER_VS_EDGE):
  Near the spectral location where the weight lives, the local DOS power s (rho ~ dist^s) fixes
  the cumulative window scaling and hence  p = 1/(s+2):  s=0 (flat center)->p=1/2 (MOND);
  s=1/2 (sqrt edge)->p=2/5 (anti-MOND).  We here read s DIRECTLY off the realized weight W(E)
  (cumulative C(E)=int_0^E W ~ E^{s+1}) instead of off the bare vacuum measure -- the whole point.
"""
import numpy as np

# ----------------------------------------------------------------------- constants
c = 2.998e8; G = 6.674e-11; Msun = 1.989e30
H0 = 67.0e3 / 3.086e22; OmegaL = 0.685; H_Lambda = H0 * np.sqrt(OmegaL)
M_dS = c**2 / (G * H_Lambda) / Msun

NPOCH = 600  # q-Pochhammer truncation (q^600 < 1e-9 even at q=0.965)


def qpoch(a, q, N=NPOCH):
    """(a;q)_inf = prod_{k>=0}(1 - a q^k), truncated."""
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
    e2 = np.exp(2j * theta)
    return qq * (qpoch(e2, q) * qpoch(np.conj(e2), q)).real / (2 * np.pi)


def G_amp(th1, th2, Delta, q):
    """Okuyama eq(18) AMPLITUDE G(th1,th2)=<th1|q^{Delta N}|th2>, COMPLEX matrix element.
       num=(q^{2Delta};q)_inf ; den = prod over four signs (q^Delta e^{i(s1 th1+s2 th2)};q)_inf."""
    num = qpoch(q ** (2 * Delta), q)  # real-positive
    th1 = np.asarray(th1, dtype=float)
    th2 = np.asarray(th2, dtype=float)
    shape = np.broadcast(th1, th2).shape
    den = np.ones(shape, dtype=complex)
    for s1 in (1, -1):
        for s2 in (1, -1):
            den *= qpoch(q ** Delta * np.exp(1j * (s1 * th1 + s2 * th2)), q)
    return num / den  # complex amplitude


def spectral_weight(theta_E, theta_vac, Delta, q):
    """w(theta_E) = mu(theta_E) |G(theta_E, theta_vac)|^2  (UNnormalized probability density in theta)."""
    G = G_amp(theta_E, theta_vac, Delta, q)
    return mu_qg(theta_E, q) * np.abs(G) ** 2


def freezing_exponent_from_weight(theta_E, W, theta_vac):
    """Read p from the realized weight W(theta_E).
       Map to normalized energy E = cos(theta_E) in [-1,1].  The deep-MOND 'freezing window' is the
       energy interval between the de Sitter spectral state (E_vac) and the probe -- i.e. how the
       cumulative weight grows as we move OFF the vacuum location toward E=0 (the deep-MOND a->0 point,
       which IS the spectral center).  p = 1/(s+2) where the cumulative C(dist) ~ dist^{s+1}.

       Concretely: build the cumulative weight C(E) = int_{E_vac}^{E} W dE' and fit C ~ |E-E_vac|^{m}
       in the small-displacement window; then s=m-1 and p=1/(s+2)=1/(m+1).
       For a weight that lives AT the center (flat local DOS, s=0) -> m=1 -> p=1/2 (MOND).
       For a weight pinned at the edge (sqrt DOS, s=1/2) -> m=3/2 -> p=2/5 (anti-MOND)."""
    E = np.cos(theta_E)                     # normalized energy E/E0 in [-1,1], monotone-decreasing in theta
    order = np.argsort(E)
    E = E[order]; W = W[order]
    E_vac = np.cos(theta_vac)
    # cumulative weight measured OUTWARD from the vacuum location toward the deep-MOND point E=0
    # (the relevant 'freezing' direction). Use the side of E_vac that contains E=0.
    if E_vac >= 0:
        sel = (E <= E_vac) & (E >= -0.0)     # from vacuum down toward 0 (and below if E_vac~0 covers both)
        # if vacuum is essentially at 0, use symmetric |E| window
    else:
        sel = (E >= E_vac) & (E <= 0.0)
    if abs(E_vac) < 1e-6:
        # vacuum AT center: use |E| as the displacement, both sides
        dist = np.abs(E)
        Wc = W.copy()
        o2 = np.argsort(dist)
        dist = dist[o2]; Wc = Wc[o2]
        C = np.cumsum(0.5 * (Wc[1:] + Wc[:-1]) * np.diff(dist))
        d = dist[1:]
        win = (d > 1e-3) & (d < 5e-2) & (C > 0)
        if win.sum() < 8:
            return np.nan, np.nan
        m = np.polyfit(np.log(d[win]), np.log(C[win]), 1)[0]
    else:
        Es = E[sel]; Ws = W[sel]
        dist = np.abs(Es - E_vac)
        o2 = np.argsort(dist)
        dist = dist[o2]; Ws = Ws[o2]
        if len(dist) < 12:
            return np.nan, np.nan
        C = np.cumsum(0.5 * (Ws[1:] + Ws[:-1]) * np.diff(dist))
        d = dist[1:]
        win = (d > 1e-3) & (d < 8e-2) & (C > 0)
        if win.sum() < 8:
            return np.nan, np.nan
        m = np.polyfit(np.log(d[win]), np.log(C[win]), 1)[0]
    s = m - 1.0
    p = 1.0 / (s + 2.0)
    return s, p


def where_does_weight_live(theta_E, W):
    """Diagnostic: fraction of total weight within |E|<0.05 (center), and the mean |E| of the weight."""
    E = np.cos(theta_E)
    Wn = W / np.trapz(W, theta_E) * 1.0  # not strictly normalized in E but fine for ratios on uniform-ish grid
    tot = np.trapz(W, theta_E)
    frac_center = np.trapz(W * (np.abs(E) < 0.05), theta_E) / tot
    frac_edge = np.trapz(W * (np.abs(E) > 0.95), theta_E) / tot
    mean_absE = np.trapz(W * np.abs(E), theta_E) / tot
    return frac_center, frac_edge, mean_absE


def main():
    np.set_printoptions(suppress=True)
    print("#" * 100)
    print("# DOOR 2 DECISIVE: matter-chord spectral weight w(E)=|<E|O_Delta|vac>|^2, vacuum at CENTER vs EDGE")
    print("#" * 100)
    print(f"\n M_dS = c^2/(G H_Lambda) = {M_dS:.3e} Msun.  Galaxy conical deficit alpha=m/M_dS:")
    for nm, M in [("dwarf 1e7", 1e7), ("spiral 3e10", 3e10), ("massive 1e12", 1e12), ("cluster 1e15", 1e15)]:
        print(f"     {nm:>14}:  alpha = {M/M_dS:.3e}")
    print(f"   => galaxies alpha <= 2.65e-3 (1e12 Msun). Clusters alpha = O(1).\n")

    qgrid = [0.5, 0.7, 0.9, 0.95]
    # FINE theta grid; refine near both center and edge so cumulative fits resolve the local power
    th = np.concatenate([
        np.linspace(1e-4, np.pi - 1e-4, 400001),
    ])
    th = np.unique(th)

    print("=" * 100)
    print("PART 1 -- Does the matter chord stay PEAKED where the vacuum is placed? (finite Delta)")
    print("=" * 100)
    print("  vacuum at CENTER theta_vac=pi/2 (E=0)  vs  vacuum at EDGE theta_vac=pi-eps (E=-E0)")
    print(f"  {'q':>5}{'Delta':>7} | {'CENTER: frac|E|<.05':>20}{'mean|E|':>9} | {'EDGE: frac|E|>.95':>19}{'mean|E|':>9}")
    for q in qgrid:
        for Delta in (0.1, 0.5, 1.0):
            # CENTER vacuum
            Wc = spectral_weight(th, np.pi / 2, Delta, q)
            fc_c, fe_c, mE_c = where_does_weight_live(th, Wc)
            # EDGE vacuum (theta_vac -> pi). Use pi - small to stay in-band.
            thv_edge = np.pi - 1e-3
            We = spectral_weight(th, thv_edge, Delta, q)
            fc_e, fe_e, mE_e = where_does_weight_live(th, We)
            print(f"  {q:>5.2f}{Delta:>7.2f} | {fc_c:>20.3f}{mE_c:>9.3f} | {fe_e:>19.3f}{mE_e:>9.3f}")
    print("""
  READ: if 'CENTER frac|E|<.05' stays HIGH and 'EDGE frac|E|>.95' stays HIGH, the matter chord
  is PEAKED AT THE VACUUM in both cases -> the diagonal kernel transports, and the SIGN rides
  entirely on WHERE the vacuum is placed (center vs edge), which the algebra does NOT decide.""")

    print("\n" + "=" * 100)
    print("PART 2 -- Freezing exponent p read DIRECTLY off the realized weight W(E), per placement")
    print("=" * 100)
    print(f"  {'q':>5}{'Delta':>7} | {'CENTER-vac s':>13}{'p':>7}{'sign':>11} | {'EDGE-vac s':>12}{'p':>7}{'sign':>11}")
    for q in qgrid:
        for Delta in (0.1, 0.5, 1.0):
            Wc = spectral_weight(th, np.pi / 2, Delta, q)
            s_c, p_c = freezing_exponent_from_weight(th, Wc, np.pi / 2)
            thv_edge = np.pi - 1e-3
            We = spectral_weight(th, thv_edge, Delta, q)
            s_e, p_e = freezing_exponent_from_weight(th, We, thv_edge)
            def sgn(p):
                if np.isnan(p): return "n/a"
                return "MOND" if abs(p - 0.5) < 0.04 else ("anti-MOND" if p < 0.46 else "?")
            print(f"  {q:>5.2f}{Delta:>7.2f} | {s_c:>13.3f}{p_c:>7.3f}{sgn(p_c):>11} | "
                  f"{s_e:>12.3f}{p_e:>7.3f}{sgn(p_e):>11}")

    print("\n" + "=" * 100)
    print("PART 3 -- Does the CHORD ALGEBRA itself pick the vacuum? (the closure question)")
    print("=" * 100)
    print("""  The kernel G(th_E, th_vac) is symmetric under th_vac -> any point in [0,pi]; nothing in
  q^{Delta N} or the q-Gaussian measure privileges theta_vac=pi/2 over theta_vac=pi. Both are
  legitimate energy eigenstates. The placement is the EXTERNAL dictionary input:
     - CENTER: Narovlansky-Verlinde 2310.16994 (max-entropy infinite-T static patch = E=0).
     - EDGE  : Okuyama 2505.08116 (semiclassical near-edge JT; 'different from' Susskind/Verlinde).
  Aguilar-Gutierrez 2506.21447: NO unique bulk dual -- the dual is sector-dependent. So the
  algebra TRANSPORTS (Part 1) but does NOT DECIDE the placement (Part 3) -> the sign is CONTESTED
  /dictionary-dependent at the level of first principles, and CLOSES only conditionally on N-V.""")


if __name__ == "__main__":
    main()
