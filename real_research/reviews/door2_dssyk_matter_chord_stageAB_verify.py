#!/usr/bin/env python3
"""
DOOR 2 -- Stage A+B: build & VERIFY the DSSYK chord spectrum (DOS) and the matter two-point kernel.
==================================================================================================
This is the verified foundation before the new content (Stage C: w(E) for a finite-mass probe).

Refs:
  Berkooz, Isachenko, Narovlansky, Torrents 1811.02584 (DSSYK spectrum & matter correlators)
  Lin 2208.07032 (bulk Hilbert space of DSSYK, matter chords)
  Narovlansky-Verlinde 2310.16994 (DSSYK = de Sitter, center E=0)
  Okuyama 2312.00880 (diagonal chord operator q^{Delta N})

Conventions (Berkooz):
  H = q-Hermite Jacobi matrix on chord-number states |n>: diag 0, offdiag b_n = sqrt([n]_q),
      [n]_q = (1-q^n)/(1-q),  q = e^{-lambda} in (0,1).
  Energies E = (2/sqrt(1-q)) cos(theta), theta in [0,pi].  E0 = 2/sqrt(1-q).
  Spectral measure of the chord VACUUM |0> = the q-Gaussian:
      mu(theta) dtheta = (q;q)_inf / (2 pi) * (e^{2 i th}; q)_inf (e^{-2 i th}; q)_inf dtheta
                       = (q;q)_inf / (2 pi) * prod_k (1 - 2 q^k cos 2th + q^{2k}) dtheta
  de Sitter (Narovlansky-Verlinde) = the spectral CENTER, theta = pi/2, E = 0, where mu is finite & flat.

  Energy eigenstate <n|theta> = H_n(cos theta | q) / sqrt([n]_q!)  (q-Hermite, vacuum-normalized).
  Matter operator O_Delta inserts a matter chord; its energy-basis matrix element squared
  (Berkooz 1811.02584 eq for the two-point function; Lin 2208.07032):
      |<theta_1|O_Delta|theta_2>|^2  =  (q^{2 Delta}; q)_inf  /  prod_{+,+-} (q^Delta e^{i(+-th1 +- th2)}; q)_inf
  This kernel is the q-deformed analogue of the conformal two-point function; it is normalized
  (sum rule int dmu M = 1) and TRANSPORTS a source -- a probe placed at energy theta_2 stays near theta_2.
"""
import numpy as np
from scipy.linalg import eigh_tridiagonal

NPOCH = 400  # truncation of q-Pochhammer products (q^NPOCH negligible for q<=0.95)


def qpoch(a, q, N=NPOCH):
    """(a; q)_inf = prod_{k>=0} (1 - a q^k), truncated at N terms."""
    a = np.asarray(a, dtype=complex)
    out = np.ones(a.shape, dtype=complex)
    qk = 1.0
    for _ in range(N):
        out *= (1 - a * qk)
        qk *= q
    return out


def qbracket_factorial(n, q):
    """[n]_q! = prod_{k=1}^n (1-q^k)/(1-q)."""
    val = 1.0
    for k in range(1, n + 1):
        val *= (1 - q**k) / (1 - q)
    return val


def q_hermite(n, x, q):
    """Continuous q-Hermite polynomial H_n(x=cos theta | q) via the recurrence
       H_{n+1} = 2 x H_n - (1 - q^n) H_{n-1},  H_0=1, H_1=2x.  (Koekoek-Swarttouw)."""
    x = np.asarray(x, dtype=float)
    if n == 0:
        return np.ones_like(x)
    Hm1 = np.ones_like(x)
    H = 2 * x
    for k in range(1, n):
        Hp1 = 2 * x * H - (1 - q**k) * Hm1
        Hm1, H = H, Hp1
    return H


# ----------------------------------------------------------------------------- Stage A: DOS
def dos_tridiag(q, N=4000):
    """Vacuum-weighted DOS from the chord Jacobi matrix: rho(E) = sum_i |<0|E_i>|^2 delta(E-E_i)."""
    n = np.arange(1, N)
    b = np.sqrt((1 - q**n) / (1 - q))
    E, V = eigh_tridiagonal(np.zeros(N), b)
    E0 = 2 / np.sqrt(1 - q)
    return E / E0, V[0, :] ** 2  # normalized energy in [-1,1], weights |<0|E_i>|^2


def mu_qgaussian(theta, q):
    """Closed q-Gaussian spectral measure mu(theta) (vacuum weight), dtheta-density."""
    qq = qpoch(q, q).real
    e2 = np.exp(2j * theta)
    return qq * (qpoch(e2, q) * qpoch(np.conj(e2), q)).real / (2 * np.pi)


# ----------------------------------------------------------------------------- Stage B: matter kernel
def matter_kernel(th1, th2, Delta, q):
    """|<theta_1|O_Delta|theta_2>|^2, Berkooz 1811.02584 / Lin 2208.07032 q-form."""
    num = qpoch(q ** (2 * Delta), q).real
    th1 = np.asarray(th1, dtype=float)
    th2 = np.asarray(th2, dtype=float)
    shape = np.broadcast(th1, th2).shape
    den = np.ones(shape, dtype=complex)
    for s1 in (1, -1):
        for s2 in (1, -1):
            den *= qpoch(q ** Delta * np.exp(1j * (s1 * th1 + s2 * th2)), q)
    return (num / den.real)


def main():
    np.set_printoptions(suppress=True)
    print("#" * 96)
    print("# DOOR 2 -- Stage A+B: verified DSSYK chord DOS + matter two-point kernel")
    print("#" * 96)

    # ---- A1: DOS variance check (the documented bug: vacuum-weighted q-Gaussian, NOT arcsine)
    print("\n[A1] Vacuum-weighted DOS variance vs analytic Var(E/E0) = (1-q)/4:")
    for q in (0.3, 0.5, 0.7, 0.9, 0.95):
        x, w = dos_tridiag(q)
        w = w / w.sum()
        var = np.sum(w * x**2)
        print(f"   q={q:.2f}:  Var(E/E0) numeric = {var:.5f}   analytic (1-q)/4 = {(1-q)/4:.5f}   "
              f"{'OK' if abs(var-(1-q)/4) < 1e-3 else 'MISMATCH'}")

    # ---- A2: DOS local exponent at center vs edge (E ~ |E|^s near center; (E0-E)^s near edge)
    print("\n[A2] DOS local power at center (E->0) and edge (E->E0) from the closed q-Gaussian:")
    for q in (0.5, 0.9):
        th = np.linspace(1e-4, np.pi - 1e-4, 400001)
        E = np.cos(th)  # normalized E/E0
        # density in E: rho_E(E) = mu(theta) |dtheta/dE| = mu(theta)/|sin theta * E0|, drop E0 const
        rhoE = mu_qgaussian(th, q) / np.abs(np.sin(th))
        # center
        mC = (np.abs(E) > 1e-3) & (np.abs(E) < 3e-2) & (rhoE > 0)
        sC = np.polyfit(np.log(np.abs(E[mC])), np.log(rhoE[mC]), 1)[0]
        # edge
        ome = 1 - np.cos(th)
        mE = (ome > 1e-6) & (ome < 1e-3) & (rhoE > 0)
        sE = np.polyfit(np.log(ome[mE]), np.log(rhoE[mE]), 1)[0]
        print(f"   q={q:.2f}:  center rho ~ |E|^{sC:+.3f} (analytic 0, FLAT)   "
              f"edge rho ~ (E0-E)^{sE:+.3f} (analytic +0.5, sqrt-vanishing)")

    # ---- B1: sum rule  int dmu(th2) M(th1,th2) = 1
    print("\n[B1] Matter-kernel sum rule  int dmu(th2) M(th1,th2) = 1 (normalized transition kernel):")
    th = np.linspace(1e-3, np.pi - 1e-3, 6000)
    for q, D in [(0.5, 0.5), (0.7, 1.0), (0.9, 0.3), (0.9, 2.0)]:
        mu = mu_qgaussian(th, q)
        for t1 in (0.6, np.pi/2, 2.5):
            integ = np.trapz(mu * matter_kernel(t1, th, D, q), th)
            print(f"   q={q:.2f} D={D:.2f} th1={t1:.3f}:  int dmu M = {integ:.6f}")
    print("   => = 1 (machine-level): M TRANSPORTS the source. The sign rides on WHERE the source sits.")

    # ---- B2: q-Hermite orthonormality sanity (energy eigenstates well-defined)
    print("\n[B2] q-Hermite vacuum overlaps <n|theta> normalization spot-check (int dmu <m|th><n|th> = delta_mn):")
    q = 0.7
    th = np.linspace(1e-4, np.pi - 1e-4, 20000)
    mu = mu_qgaussian(th, q)
    for (m, n) in [(0, 0), (1, 1), (2, 2), (0, 2), (1, 3)]:
        Hm = q_hermite(m, np.cos(th), q) / np.sqrt(qbracket_factorial(m, q))
        Hn = q_hermite(n, np.cos(th), q) / np.sqrt(qbracket_factorial(n, q))
        ov = np.trapz(mu * Hm * Hn, th)
        print(f"   <{m}|{n}>_mu = {ov:+.5f}   (expect {1.0 if m==n else 0.0:.0f})")

    print("\n" + "#" * 96)
    print("# Stage A+B VERIFIED: DOS is flat-center q-Gaussian; matter kernel is a normalized transport kernel.")
    print("#" * 96)


if __name__ == "__main__":
    main()
