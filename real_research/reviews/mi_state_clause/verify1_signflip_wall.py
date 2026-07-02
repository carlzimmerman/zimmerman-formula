#!/usr/bin/env python3
"""
ADVERSARIAL VERIFIER script 1 -- INDEPENDENT re-derivation of the inversion sign-flip
(load-bearing computation #1), by a DIFFERENT route than the gauntlet (numeric matrix
mechanics + numeric quadrature, not sympy symbolics).

V1  Two-level ghost-free bath: <[B(t),B(0)]> = -2i b^2 (p_g-p_e) sin(w0 t)  (numeric, many t)
V2  chi_R(0) by numeric Abel-regularized quadrature = 2 b^2 (p_g-p_e)/w0
V3  delta_m = 2 b^2 (p_g-p_e)/w0^2  and the EOM (velocity-coupling) route delta_m = lam^2 chi_B(0):
    both carry sign (p_g-p_e): ground/KMS => +, inverted => - (MOND sign). KMS => tanh(bw/2)>0 all T.
V4  Ghost-freedom: total probe(HO) x bath(2-level) Hamiltonian spectrum bounded below (numeric eig).
V5  FREE-FIELD RIGIDITY WALL: truncated boson, [Q(t),Q(0)] = -2i sin(w0 t) * I on the interior
    (c-number; deviation confined to the truncation edge) => response/dissipation kernel is
    STATE-INDEPENDENT: thermal, squeezed-vacuum, and population-INVERTED boson states all give
    the SAME <[Q(t),Q(0)]>. The NOISE kernel <{Q(t),Q(0)}> IS state-dependent (checked):
    pumping a free field pumps noise (heating), never inertia.
V6  The escape-door boundary is ANHARMONICITY: Kerr oscillator commutator is operator-valued
    and its expectation DOES move under population inversion.
V7  Stability threshold: worldline + damped inverted line, poles cross to UHP exactly at
    |delta_m| = m (numeric roots both sides).
Exit 0 = all assertions hold.
"""
import numpy as np
from math import lgamma, log, tanh, cosh

rng = np.random.default_rng(11)
ok = []

# ---------------------------------------------------------------- V1: two-level commutator
w0, b = 1.37, 0.83
H2 = np.diag([0.0, w0])                       # basis [g, e], ghost-free (bounded below)
B  = b*np.array([[0, 1], [1, 0]], complex)

def Bt(t):
    P = np.diag(np.exp(1j*np.diag(H2)*t))     # e^{iHt} (diagonal H)
    return P @ B @ P.conj().T

def C_comm(t, pg, pe):
    rho = np.diag([pg, pe]).astype(complex)
    return np.trace(rho @ (Bt(t) @ B - B @ Bt(t)))

pops = [(1.0, 0.0), (0.73, 0.27), (0.27, 0.73), (0.5, 0.5)]
for t in rng.uniform(0.0, 25.0, 12):
    for (pg, pe) in pops:
        assert abs(C_comm(t, pg, pe) - (-2j*b*b*(pg-pe)*np.sin(w0*t))) < 1e-12
# and the operator itself is prop to sigma_z (STATE-DEPENDENT -- contrast with V5):
K2 = Bt(1.3) @ B - B @ Bt(1.3)
assert np.allclose(K2, -2j*b*b*np.sin(w0*1.3)*np.diag([1.0, -1.0])), "two-level commutator"
ok.append("V1: <[B(t),B(0)]> = -2i b^2 (p_g-p_e) sin(w0 t); operator-valued (prop sigma_z)")

# --------------------------------------------- V2: chi_R(0) by numeric quadrature (Abel)
def chi0_num(pg, pe, eps=0.02, T=1200.0, dt=5e-4):
    t = np.arange(0.0, T, dt)
    integ = 2*b*b*(pg-pe)*np.sin(w0*t)*np.exp(-eps*t)   # i*C(t) is real: 2 b^2 dp sin
    raw = np.trapezoid(integ, t) if hasattr(np, "trapezoid") else np.trapz(integ, t)
    return raw*(w0*w0 + eps*eps)/(w0*w0)                # exact Abel correction -> eps->0 limit

for (pg, pe) in [(0.73, 0.27), (0.27, 0.73)]:
    assert abs(chi0_num(pg, pe) - 2*b*b*(pg-pe)/w0) < 1e-6
ok.append("V2: chi_R(0) = 2 b^2 (p_g-p_e)/w0 (numeric quadrature; matches gauntlet A2)")

# ------------------------------------------------------- V3: delta_m sign, both conventions
dm_theorem = lambda dp: 2*b*b*dp/w0**2      # theorem integrand with rho = b^2 dp delta(w-w0)
lam = 0.31
dm_eom     = lambda dp: lam**2*2*b*b*dp/w0  # m_eff = m + lam^2 chi_B(0), velocity coupling
assert dm_theorem(+0.46) > 0 and dm_eom(+0.46) > 0          # ground/thermal: anti-MOND
assert dm_theorem(-0.46) < 0 and dm_eom(-0.46) < 0          # inverted: MOND sign
for beta in [0.01, 0.3, 1.0, 30.0]:                          # KMS at ANY T: dp = tanh(bw/2) > 0
    Zf = 1 + np.exp(-beta*w0)
    dp = (1 - np.exp(-beta*w0))/Zf
    assert abs(dp - tanh(beta*w0/2)) < 1e-14 and dp > 0
ok.append("V3: delta_m sign = sign(p_g-p_e) in BOTH conventions; KMS => dp=tanh(bw0/2)>0 all T; "
          "inversion (definitionally non-KMS) flips it: MOND sign with ghost-free microphysics")

# ------------------------------------------------------------------- V4: ghost-freedom
nho = 30
aho = np.diag(np.sqrt(np.arange(1, nho)), 1)
Hho = np.diag(np.arange(nho) + 0.5)          # Omega = 1
X   = (aho + aho.T)/np.sqrt(2)
Htot = np.kron(Hho, np.eye(2)) + np.kron(np.eye(nho), H2) + 0.15*np.kron(X, np.real(B))
ev = np.linalg.eigvalsh(Htot)
assert ev.min() > 0.4, ev.min()               # bounded below (bare ground 0.5, tiny shift)
ok.append(f"V4: total probe+bath spectrum bounded below (min eig = {ev.min():.4f} > 0): ghost-free")

# ------------------------------------------- V5: free-field rigidity wall (state-blindness)
N = 100
a = np.diag(np.sqrt(np.arange(1.0, N)), 1)
Q0 = a + a.T
def Qt(t):
    return a*np.exp(-1j*w0*t) + a.T*np.exp(1j*w0*t)     # exact Heisenberg, free H

t1 = 1.9
Kb = Qt(t1) @ Q0 - Q0 @ Qt(t1)
tgt = -2j*np.sin(w0*t1)
dev = Kb[:N-1, :N-1] - tgt*np.eye(N-1)
assert np.max(np.abs(dev)) < 1e-12                       # c-number on interior
assert abs(Kb[N-1, N-1] - (-tgt*(N-1))) < 1e-9           # deviation ONLY at truncation edge
ok.append("V5a: [Q(t),Q(0)] = -2i sin(w0 t) * Identity on interior (c-number); "
          "truncation artifact confined to the edge element, = +2i sin(w0 t)(N-1)")

# three very different states, incl. a POPULATION-INVERTED boson ladder:
p_th = np.exp(-0.7*np.arange(N)); p_th /= p_th.sum()
p_inv = np.exp(+0.05*np.arange(N))*(np.arange(N) < 60); p_inv /= p_inv.sum()
r = 0.5
csq = np.zeros(N)
for k in range(N//2):
    lg = k*log(tanh(r)) + 0.5*lgamma(2*k+1) - k*log(2.0) - lgamma(k+1) - 0.5*log(cosh(r))
    csq[2*k] = np.exp(lg)*((-1)**k)
assert abs(np.sum(csq**2) - 1.0) < 1e-12                 # squeezed vacuum normalized
vals = [np.sum(p_th*np.diag(Kb).real) + 1j*np.sum(p_th*np.diag(Kb).imag),
        np.sum(p_inv*np.diag(Kb).real) + 1j*np.sum(p_inv*np.diag(Kb).imag),
        csq @ Kb @ csq]
for v in vals:
    assert abs(v - tgt) < 1e-8, v
ok.append("V5b: <[Q(t),Q(0)]> IDENTICAL for thermal, squeezed-vacuum, and population-INVERTED "
          "boson states => dissipation kernel/delta_m is STATE-INDEPENDENT for a free field with "
          "linear coupling: NO pumping of the dS-Unruh free-field bath can flip the sign")

# noise kernel IS state-dependent (that is all pumping does to a free field):
S_th  = lambda p: np.sum(p*np.diag((Qt(t1) @ Q0 + Q0 @ Qt(t1)).real))
noise_vac = np.zeros(N); noise_vac[0] = 1.0
assert abs(S_th(p_th) - S_th(noise_vac)) > 0.1
ok.append("V5c: the ANTIcommutator (noise) does depend on the state: pumping a free field "
          "pumps NOISE (heating), never the response (inertia)")

# ------------------------------------------------- V6: anharmonicity opens the door
Ekerr = w0*np.arange(N) + 0.3*np.arange(N)*(np.arange(N)-1.0)
phase = np.exp(1j*np.subtract.outer(Ekerr, Ekerr)*t1)
Qk = Q0*phase                                            # Heisenberg for diagonal Kerr H
Kk = Qk @ Q0 - Q0 @ Qk
intr = Kk[:60, :60]
assert np.max(np.abs(intr - (np.trace(intr)/60)*np.eye(60))) > 0.1   # NOT a c-number
e_gnd = np.zeros(N); e_gnd[0] = 1.0
e_inv = np.zeros(N); e_inv[3] = 1.0                       # population moved up the ladder
assert abs(np.sum(e_gnd*np.diag(Kk)) - np.sum(e_inv*np.diag(Kk))) > 1e-3
ok.append("V6: Kerr (anharmonic) commutator is operator-valued and its expectation MOVES under "
          "population transfer: the inversion escape lives EXACTLY in the anharmonic sector")

# ------------------------------------------------- V7: stability threshold |delta_m| = m
gam, m = 0.1, 1.0
for A, want_unstable in [(-0.5, False), (-0.99, False), (-1.01, True), (-1.5, True)]:
    roots = np.roots([1.0, 1j*gam, -(1.0 + A/m)])        # w^2 + i gam w - (w0^2 + A/m), w0=1
    unstable = bool(np.any(roots.imag > 1e-12))
    assert unstable == want_unstable, (A, roots)
ok.append("V7: poles cross to the UHP exactly at |delta_m|=m (delta_m(0)=A/w0^2): deep-MOND "
          "m_eff->0 sits asymptotically AT threshold; linear theory alone cannot hold it there")

print("ALL ASSERTIONS PASSED (verifier 1: sign-flip re-derived independently + rigidity wall)")
for line in ok:
    print(" *", line)
