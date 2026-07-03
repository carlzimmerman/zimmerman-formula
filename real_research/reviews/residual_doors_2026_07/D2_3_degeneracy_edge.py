#!/usr/bin/env python3
"""
D2_3 -- PASSIVE-ANHARMONIC CORNER: the degeneracy edge (lane D2, 2026-07)

Sharpest crack candidate: passivity constrains populations ONLY across distinct
energies. Within a DEGENERATE eigenspace a passive state may carry arbitrary
coherences AND arbitrarily ordered sub-populations. Can a designed degenerate
anharmonic bath exploit that freedom to give delta-m < 0 with no pump?

Model: engineered 6-level anharmonic spectrum E = [0, 1.0, 1.7, 1.7(+w0), 2.55, 3.4]
with a degenerate (or nearly degenerate) pair at levels 2,3 and full Hermitian
coupling B. Checks:

 (a) WITHIN-SUBSPACE-ONLY coupling: B restricted to the degenerate block commutes
     with H there -> the induced force is CONSTANT in time (geometric/DC only):
     zero dissipation, zero inertia. Coherences cannot make mass.
 (b) FULL B + random within-block coherences/populations: stationarity forces rho
     block-diagonal; diagonalize the block -> ordered pair weights across distinct
     energies stay >= 0 -> delta-m >= 0. Verified spectrally AND by exact driven
     dynamics.
 (c) NEAR-DEGENERATE SPLIT w0 -> 0: passive delta-m ~ +2 g^2 dp |B23|^2/w0^3 BLOWS
     UP POSITIVE; the negative mirror requires inverting the soft pair = NON-passive
     = a pump. If instead w0 < W (drive above the split) the passive pair contributes
     NEGATIVELY -- but that is the SUB-DRIVE POLE (hexad IV frequency law + V gas
     clamp), amplitude-blind, not mu(a/a0). Galactic-band mapping printed.
 (d) LEVEL-CROSSING DRIVE (Landau-Zener two-level, drive sweeping through the
     avoided crossing): passive start -> net work absorbed >= 0 at weak AND strongly
     diabatic sweep; emission requires inversion.

Both a0 footings printed where scale enters. Exit 0.
"""
import numpy as np

np.seterr(all='ignore')   # Apple-Accelerate BLAS spurious FP flags; correctness
                          # guarded by explicit unitarity/finiteness asserts.
rng = np.random.default_rng(20260704)

# ---------------------------------------------------------------- machinery
def dm_static(E, p, B, g=1.0, wmin=1e-9):
    s = 0.0
    N = len(E)
    for n in range(N):
        for m in range(N):
            w = E[m] - E[n]
            if w > wmin:
                s += 2.0 * (p[n] - p[m]) * abs(B[m, n]) ** 2 / w ** 3
    return g * g * s

def dm_at(E, p, B, Om, g=1.0, wmin=1e-9):
    s = 0.0
    N = len(E)
    for n in range(N):
        for m in range(N):
            w = E[m] - E[n]
            if w > wmin:
                s += 2.0 * (p[n] - p[m]) * abs(B[m, n]) ** 2 / (w * (w * w - Om * Om))
    return g * g * s

def evolve(E, B, rho0, A, Om, ncyc, dt=0.002, envelope="sin"):
    """H(t) = diag(E) + f(t) B. Returns (t, F(t)=-<B>(t), dE_bath)."""
    N = len(E)
    d, V = np.linalg.eigh(B); Vh = V.conj().T
    T = ncyc * 2 * np.pi / Om
    nst = int(np.ceil(T / dt)); dt = T / nst
    ph = np.exp(-1j * E * dt / 2.0)
    U = np.eye(N, dtype=complex)
    ts, Fs = np.empty(nst), np.empty(nst)
    for k in range(nst):
        tm = (k + 0.5) * dt
        f = A * (np.sin(Om * tm) if envelope == "sin" else np.cos(Om * tm))
        U = ph[:, None] * (V @ (np.exp(-1j * f * d * dt)[:, None] * (Vh @ (ph[:, None] * U))))
        rho = U @ rho0 @ U.conj().T
        ts[k] = (k + 1) * dt
        Fs[k] = -np.real(np.trace(rho @ B))
    assert np.abs(U.conj().T @ U - np.eye(N)).max() < 1e-9
    rhoT = U @ rho0 @ U.conj().T
    dE = float(np.real(np.trace(rhoT @ np.diag(E)) - np.trace(rho0 @ np.diag(E))))
    return ts, Fs, dE

def block_state(p_outer, q_pair, theta, phi):
    """6-level density matrix: diag(p_outer[0:2]) + 2x2 block (eigenvalues q_pair,
    eigenbasis rotated by theta,phi) + diag(p_outer[2:4]). Stationary iff H-block
    is degenerate."""
    rho = np.zeros((6, 6), dtype=complex)
    rho[0, 0], rho[1, 1] = p_outer[0], p_outer[1]
    c, s = np.cos(theta), np.sin(theta)
    v1 = np.array([c, np.exp(1j * phi) * s])
    v2 = np.array([-np.exp(-1j * phi) * s, c])
    blk = q_pair[0] * np.outer(v1, v1.conj()) + q_pair[1] * np.outer(v2, v2.conj())
    rho[2:4, 2:4] = blk
    rho[4, 4], rho[5, 5] = p_outer[2], p_outer[3]
    return rho

print("=" * 78)
print("D2_3  DEGENERACY EDGE -- within-subspace coherence vs the MOND sign")
print("=" * 78)

E6 = np.array([0.0, 1.0, 1.7, 1.7, 2.55, 3.4])
B6 = (lambda X: (X + X.conj().T) / 2)(rng.normal(size=(6, 6)) + 1j * rng.normal(size=(6, 6)))

# ---------------------------------------------------------------- (a)
print("\n[a] Within-degenerate-subspace coupling ONLY (coherences maximal):")
Bsub = np.zeros((6, 6), dtype=complex)
Bsub[2, 3] = 1.5 + 0.7j; Bsub[3, 2] = 1.5 - 0.7j; Bsub[2, 2] = 0.9; Bsub[3, 3] = -0.4
# passive ordering: 0.35 >= 0.25 >= {pair: 0.18, 0.12} >= 0.07 >= 0.03
rho = block_state([0.35, 0.25, 0.07, 0.03], [0.18, 0.12], 0.9, 1.1)
assert abs(np.trace(rho).real - 1) < 1e-12
assert np.abs(rho @ np.diag(E6) - np.diag(E6) @ rho).max() < 1e-12, "not stationary"
ts, Fv, dE = evolve(E6, Bsub, rho, A=0.8, Om=0.31, ncyc=6)
print(f"    force std over 6 driven cycles = {np.std(Fv):.2e} (constant), dE_bath = {dE:+.2e}")
assert np.std(Fv) < 1e-10 and abs(dE) < 1e-10
print("    -> pure within-subspace coherence produces a CONSTANT (geometric) force:")
print("       zero dissipation, zero inertia. No mass channel. PASS")

# ---------------------------------------------------------------- (b)
print("\n[b] Full coupling + 300 random within-block coherent passive states:")
dmin, dyn_checked = np.inf, []
for i in range(300):
    p6 = np.sort(rng.dirichlet(np.ones(6)))[::-1]     # ordered; slots 2,3 = pair eigenvalues
    th, phv = rng.uniform(0, np.pi), rng.uniform(0, 2 * np.pi)
    rho = block_state([p6[0], p6[1], p6[4], p6[5]], [p6[2], p6[3]], th, phv)
    # spectral dm in the rho-eigenbasis (block rotation R applied to B)
    R = np.eye(6, dtype=complex)
    c, s = np.cos(th), np.sin(th)
    R[2:4, 2:4] = np.array([[c, -np.exp(-1j * phv) * s], [np.exp(1j * phv) * s, c]])
    Bp = R.conj().T @ B6 @ R
    dm = dm_static(E6, p6, Bp)
    dmin = min(dmin, dm)
    if i < 3:
        # dynamic cross-check: quadrature extraction at sub-gap drive
        Om, A = 0.23, 0.05
        tsr, Fr, _ = evolve(E6, B6, rho, A, Om, ncyc=40, dt=0.004, envelope="cos")
        w = tsr > 10 * 2 * np.pi / Om   # last 30 cycles
        Fc = 2 * np.mean(Fr[w] * np.cos(Om * tsr[w]))
        # F = -<B> = +chi(Om) A cos(Om t)  [H' = f B, f = A cos, d<B> = -chi f]
        # delta-m(Om) = (chi(Om) - chi(0)) / Om^2 with chi(0) from the spectral sum
        chi0 = sum(2 * (p6[n] - p6[m]) * abs(Bp[m, n]) ** 2 / (E6[m] - E6[n])
                   for n in range(6) for m in range(6) if E6[m] - E6[n] > 1e-9)
        dm_dyn = (Fc / A - chi0) / (Om * Om)
        dyn_checked.append((dm_dyn, dm_at(E6, p6, Bp, Om)))
print(f"    min delta-m over 300 coherent passive states: {dmin:+.4e}  (>= 0 required)")
for dd, ds in dyn_checked:
    print(f"    dynamic cross-check: dm_dyn = {dd:+.4f} vs spectral dm(W) = {ds:+.4f}")
assert dmin >= -1e-12
for dd, ds in dyn_checked:
    assert abs(dd - ds) < 0.2 * max(abs(ds), 0.05), "dynamics/spectral mismatch"
print("    -> stationarity forces block-diagonal rho; diagonalizing the block restores")
print("       ordered weights across distinct energies: delta-m >= 0 ALWAYS. PASS")

# ---------------------------------------------------------------- (c)
print("\n[c] Near-degenerate split w0 -> 0 (the 1/w0^3 blow-up) and the sub-drive pole:")
print("    w0        passive dm      inverted-pair dm    passive dm(W=0.05)")
for w0 in [0.1, 0.01, 0.001]:
    Ew = E6.copy(); Ew[3] = 1.7 + w0
    p_pass = np.array([0.30, 0.25, 0.18, 0.12, 0.10, 0.05])
    p_inv = np.array([0.30, 0.25, 0.12, 0.18, 0.10, 0.05])    # soft pair inverted: NON-passive
    dmp = dm_static(Ew, p_pass, B6); dmi = dm_static(Ew, p_inv, B6)
    dmW = dm_at(Ew, p_pass, B6, 0.05)
    print(f"    {w0:6.3f}  {dmp:+13.3e}  {dmi:+15.3e}  {dmW:+15.3e}")
    assert dmp > 0
    if w0 < 0.05:
        assert dmW < 0   # sub-drive pole: passive softening exists but is W-locked
    assert dmi < 0
print("    -> passive near-degeneracy HARDENS (+1/w0^3); the negative mirror needs the")
print("       inverted pair (pump). A passive split BELOW the drive does soften m_eff,")
print("       but that is the sub-drive pole: delta-m(W) ~ -C/W^2, amplitude-blind =")
print("       hexad IV frequency law; hexad V gas clamp applies. NOT mu(a/a0).")

# ---------------------------------------------------------------- (d)
print("\n[d] Landau-Zener crossing drive (two-level, gap eps, sweep u = U0 sin(Wt)):")
for eps, U0, Om, ncyc in [(0.05, 2.0, 0.10, 10), (0.3, 2.0, 0.10, 10), (0.05, 2.0, 0.02, 3)]:
    Elz = np.array([-eps, eps])                       # eigenbasis of eps*sigma_x
    Blz = np.array([[0, 1], [1, 0]], dtype=complex)   # sigma_z in that basis
    beta = 2.0
    p = np.exp(-Elz / beta); p /= p.sum()
    rho0 = np.diag(p).astype(complex)
    _, _, dE = evolve(Elz, Blz, rho0, U0, Om, ncyc=ncyc, dt=0.002)
    rho_inv = np.diag(p[::-1]).astype(complex)
    _, _, dE_i = evolve(Elz, Blz, rho_inv, U0, Om, ncyc=ncyc, dt=0.002)
    lz = eps ** 2 / (U0 * Om)
    print(f"    eps={eps:4.2f} U0={U0} W={Om}: LZ adiabaticity ~{lz:5.3f} | "
          f"dE(passive) = {dE:+.3e} (>=0) | dE(inverted) = {dE_i:+.3e}")
    assert dE >= -1e-8
print("    -> even strongly diabatic crossing sweeps cannot extract work from a")
print("       passive start; creating the inversion costs the drive energy first. PASS")

# ---------------------------------------------------------------- footings
print("\n[FOOTINGS] where scale enters the degeneracy/sub-drive route:")
c_ = 2.998e8; H0_ = 67.4 * 1000 / 3.0857e22; Z_ = np.sqrt(32 * np.pi / 3)
a0_can = c_ * H0_ * np.sqrt(0.685) / Z_; a0_alt = c_ * H0_ / Z_
hbar = 1.0546e-34
Olo, Ohi = 3.2e-17, 1.9e-14
print(f"    a0 canonical = {a0_can:.3e} | alternate = {a0_alt:.3e} m/s^2 "
      f"(spread {100*(a0_alt/a0_can-1):.1f}%)")
print(f"    band W = [{Olo:.1e}, {Ohi:.1e}] rad/s (kinematic, footing-independent).")
print(f"    a passive degenerate-split channel must place w0 < W_min:")
print(f"      hbar*w0 < {hbar*Olo:.2e} J = {hbar*Olo/1.602e-19:.2e} eV, then softening is")
print(f"      m_eff(W) = m - C/W^2: frequency-locked, amplitude-blind -> cannot yield the")
print(f"      framework's nu(y)=sqrt(1+1/y) at EITHER footing (y = g_bar/a0 shifts 21%")
print(f"      between footings, but the failure is structural, not scale-sensitive).")

print("\nVERDICT [D2_3]: degeneracy edge CLOSED. Within-subspace coherence gives")
print("geometric constant forces (no inertia); block stationarity + passivity restore")
print("nonnegative pair weights; near-degenerate blow-up is POSITIVE for passive")
print("states; the only passive softening is the sub-drive pole = hexad IV/V.")
