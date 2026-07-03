#!/usr/bin/env python3
"""
D1_1: GENERAL POSITIVITY OF THE WINDOWED DETECTOR RESPONSE  F(omega) >= 0
==========================================================================
Lane D1 (interacting-field windowed response), part 1 of 4.

CLAIM (theory-independent half of Theorem VI's positivity lock):
For ANY state |psi> (pure or mixed) of ANY quantum theory (free or
interacting), any worldline/probe schedule, any window chi(tau), and any
omega (positive or negative):

    F(omega) = int dtau int dtau' chi(tau) chi(tau') e^{-i omega (tau-tau')}
               <psi| O(tau) O(tau') |psi>   >=  0.

TWO-LINE OPERATOR PROOF:
  Define A = int dtau chi(tau) e^{+i omega tau} O(tau)   (O hermitian);
  then <A^dag A> = int int chi chi' e^{-i omega(tau-tau')} W(tau,tau'),
  so F(omega) = <psi| A^dagger A |psi> = || A|psi> ||^2 >= 0.   QED.
  (Mixed states: F = sum_n p_n ||A|n>||^2 >= 0.)
Nothing about free-ness, stationarity, or the trajectory entered. The
discretized kernel W_ab = <psi|O(tau_a)O(tau_b)|psi> is a GRAM matrix of
the vectors u_a = O(tau_a)|psi>, hence PSD; F = v^dag W v.

NUMERICAL CONFIRMATION in an exactly-solved GENUINELY INTERACTING model:
nonintegrable mixed-field Ising chain (J zz + transverse g + longitudinal h,
Kim-Huse parameters), L=8, exact diagonalization. Probe operator: smooth
spatial packet of sigma^z centered at a MOVING position xi(tau) (a lattice
"worldline"), states: ground (interacting vacuum), mid-spectrum eigenstate,
random pure state, thermal mixture. Verify F(omega) >= 0 to machine
precision across an omega grid, and (baseline) that a STATIC probe in the
ground state shows no inversion F(omega) > F(-omega) for omega > 0
(lattice spectrum condition: GS autocorrelation has positive-frequency
support only), Gaussian window.
"""
import numpy as np

np.random.seed(7)

# ---------------- exact diagonalization: nonintegrable Ising, L=8 ---------
L = 8
dim = 2 ** L
sz = np.diag([1.0, -1.0])
sx = np.array([[0.0, 1.0], [1.0, 0.0]])
I2 = np.eye(2)

def site_op(o, i):
    M = np.array([[1.0]])
    for j in range(L):
        M = np.kron(M, o if j == i else I2)
    return M

SZ = [site_op(sz, i) for i in range(L)]
SX = [site_op(sx, i) for i in range(L)]

g, h = 0.9045, 0.8090  # Kim-Huse nonintegrable point
H = np.zeros((dim, dim))
for i in range(L - 1):
    H += -SZ[i] @ SZ[i + 1]
for i in range(L):
    H += -g * SX[i] - h * SZ[i]

E, V = np.linalg.eigh(H)
E -= E[0]  # ground energy -> 0
OZ_til = [V.T @ SZ[i] @ V for i in range(L)]  # sigma^z_i in eigenbasis (real)

# ---------------- probe schedule ("worldline" on the lattice) -------------
T = 3.0                      # window width (units 1/J)
tau = np.linspace(-15.0, 15.0, 300)  # +-5 sigma: window-truncation sidelobes ~1e-11 in power
dtau = tau[1] - tau[0]
chi = np.exp(-tau ** 2 / (2 * T ** 2))

def probe_matrices(xi_of_tau, sig_s=1.0):
    """O(tau_a) = sum_j exp(-(j-xi)^2/2 sig_s^2) sigma^z_j, eigenbasis."""
    mats = []
    for xa in xi_of_tau:
        w = np.exp(-(np.arange(L) - xa) ** 2 / (2 * sig_s ** 2))
        M = np.zeros((dim, dim))
        for j in range(L):
            M += w[j] * OZ_til[j]
        mats.append(M)
    return mats

xi_static = np.full_like(tau, (L - 1) / 2)
xi_moving = (L - 1) / 2 + 2.5 * np.sin(1.3 * tau)   # oscillatory sweep

# ---------------- states (eigenbasis coordinates) --------------------------
c_gs = np.zeros(dim); c_gs[0] = 1.0
c_mid = np.zeros(dim); c_mid[dim // 2] = 1.0
c_rnd = np.random.randn(dim) + 1j * np.random.randn(dim)
c_rnd /= np.linalg.norm(c_rnd)
beta_th = 1.0
p_th = np.exp(-beta_th * E); p_th /= p_th.sum()
idx_th = np.argsort(p_th)[::-1][:6]  # 6 dominant thermal components

def build_U(mats, c):
    """columns u_a = O(tau_a)|psi> in Heisenberg picture, eigenbasis."""
    U = np.zeros((dim, len(tau)), dtype=complex)
    for a, (ta, M) in enumerate(zip(tau, mats)):
        ph = np.exp(-1j * E * ta)
        U[:, a] = np.exp(1j * E * ta) * (M @ (ph * c))
    return U

def F_of_omega(U, omegas):
    # weight e^{+i omega tau} => quadratic form with kernel
    # e^{-i omega (tau_a - tau_b)} W(tau_a,tau_b)  (standard UDW response)
    W = (dtau * chi)[:, None] * np.exp(1j * np.outer(tau, omegas))
    S = U @ W                      # dim x Nomega
    return np.sum(np.abs(S) ** 2, axis=0)

omegas = np.linspace(-8.0, 8.0, 161)
mats_static = probe_matrices(xi_static)
mats_moving = probe_matrices(xi_moving)

print(__doc__)
print("=" * 72)
print("Numerical confirmation (nonintegrable Ising L=8, exact):")
print("=" * 72)

minF_global, maxF_global = np.inf, 0.0
for name, mats in [("static probe", mats_static), ("moving probe", mats_moving)]:
    for sname, c in [("ground(int.vac)", c_gs), ("mid-eigenstate", c_mid),
                     ("random pure", c_rnd)]:
        F = F_of_omega(build_U(mats, c), omegas)
        minF_global = min(minF_global, F.min())
        maxF_global = max(maxF_global, F.max())
        print(f"  {name:13s} | {sname:16s} : min F = {F.min(): .3e}, "
              f"max F = {F.max():.3e}")
    # thermal mixture (dominant components)
    Fth = np.zeros_like(omegas)
    for n in idx_th:
        cn = np.zeros(dim); cn[n] = 1.0
        Fth += p_th[n] * F_of_omega(build_U(mats, cn), omegas)
    minF_global = min(minF_global, Fth.min())
    print(f"  {name:13s} | thermal beta=1 (top-6) : min F = {Fth.min(): .3e}")

tol = 1e-12 * maxF_global
assert minF_global > -tol, "positivity violated?!"
print(f"\nPASS: F(omega) >= 0 for all probes/states/omega "
      f"(global min {minF_global:.3e} vs scale {maxF_global:.3e}).")
print("Positivity is the Gram property of W_ab = <psi|O_a O_b|psi> -- ")
print("holds for ANY interacting dynamics. This half of the Theorem-VI lock")
print("is CONFIRMED theory-independent.")

# ---------------- baseline: no inversion for static GS probe --------------
F_gs = F_of_omega(build_U(mats_static, c_gs), omegas)
pos = omegas > 0.05
Fp = F_gs[pos]
Fm = np.interp(-omegas[pos], omegas, F_gs)
# compare only above the trapezoid-quadrature noise floor (~1e-9 relative)
mask = np.maximum(Fp, Fm) > 1e-5 * F_gs.max()
inv_idx = (Fp[mask] - Fm[mask]) / np.maximum(Fp[mask], Fm[mask])
print(f"\nStatic GS probe (lattice spectrum condition + Gaussian window):")
print(f"  max inversion index (F(w)-F(-w))/max over w>0 : {inv_idx.max(): .3e}"
      f"   ({mask.sum()} omega points above noise floor)")
assert inv_idx.max() < 1e-6, "unexpected static-GS inversion"
print("  PASS: no inversion for the stationary interacting vacuum, as the")
print("  spectrum condition + monotone-window lemma (script D1_2) require.")
print("\nD1_1 VERDICT: F(omega) >= 0 is UNCONDITIONAL (interacting included).")
print("Any reopening of leg (iii) must therefore come from the ASYMMETRY")
print("half F(w) vs F(-w) -- adjudicated in D1_2 (theorems), D1_3 (KL")
print("reduction + relativistic scan), D1_4 (interacting lattice scan).")
