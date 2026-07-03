#!/usr/bin/env python3
"""
verify_D2_rederive_final.py -- ADVERSARIAL VERIFIER, lane D2 (final rederivation).

Independent of the lane's scripts AND of the first verifier pass: different bath
(cubic+quartic anharmonicity, NOT pure quartic), different truncation (NF=440,
NK=28), different RNG, different integrator (exact instantaneous-eigh midpoint).

 (1) RE-DERIVE the load-bearing pair-sum
        delta-m = 2 g^2 SUM_{E_m>E_n} (p_n-p_m) |<m|dH/dx|n>|^2 / w_nm^3
     three independent ways and cross-check to machine/percent precision:
       (a) 2nd-order stationary perturbation theory in the displacement
           (E_n(x) curvature route): m_eff = m - d2E/dx2 contributions...
           implemented as the exact Born-Oppenheimer O(v^2) coefficient via
           finite-difference of the Berry/adiabatic force -- here done as
           Kramers-Kronig: delta-m = (2/pi) Int Im chi(w)/w^3 dw over Bohr lines.
       (b) the pair sum itself (formula under test).
       (c) DIRECT DYNAMICAL MEASUREMENT: slow sinusoidal worldline x(t)=A cos(Wt),
           exact unitary evolution, fit the in-phase induced-force quadrature,
           subtract the exact adiabatic static quadrature:
              delta-m_meas = (Fc - Fc_static)/(A W^2).
     Also verify the w^-3 POWER by a two-level gap sweep (log-log slope must be -3)
     and the SIGN by the classical harmonic anchor delta-m = g^2/(w0^2(w0^2-W^2)).

 (2) MOVING-WORLDLINE PASSIVITY PREMISE: is "passive w.r.t. the instantaneous
     Hamiltonian" self-consistent along a trajectory? 1D Schroedinger operators
     have simple spectra (no true crossings), so adiabatic transport preserves the
     population ORDERING -> a state passive for H(x(0)) stays passive for H(x(t)).
     Checked exactly: slow dynamical sweep x: 0 -> 3, project final state onto the
     instantaneous eigenbasis, count ordering violations (must be 0), and confirm
     delta-m(x0) >= 0 at every displacement along the way.

 (3) Truncation independence: NK=28 vs NK=36 and NF=440 vs NF=560 on the
     measured point (the lane caught one NF artifact; check for others).

 (4) Footing forks + galactic-band mapping (both a0 footings).

Exit 0 iff every check passes. Verifier lane; no commit.
"""
import numpy as np

np.seterr(all='ignore')   # Apple-Accelerate spurious FP flags; guarded by asserts
rng = np.random.default_rng(424242)

# ------------------------------------------------------------------ bath: cubic+quartic
NF, NK = 440, 28
LAM4, LAM3, G = 0.7, 0.3, 0.4
aop = np.diag(np.sqrt(np.arange(1, NF)), 1)
qf = (aop + aop.T) / np.sqrt(2.0)
q2 = qf @ qf
H0f = np.diag(np.arange(NF) + 0.5)
Hb_f = H0f + LAM4 * (q2 @ q2) + LAM3 * (q2 @ qf)   # p^2/2+q^2/2 + 0.7 q^4 + 0.3 q^3

def bath_eig(u=0.0, nk=NK, Hfull=Hb_f):
    E, W = np.linalg.eigh(Hfull + u * qf)
    Q = W.T @ qf @ W
    assert np.isfinite(E).all()
    return E[:nk], Q[:nk, :nk]

def thermal(E, T):
    p = np.exp(-(E - E[0]) / T); return p / p.sum()

def dm_pairsum(E, Q, p, g):
    s = 0.0
    for n in range(len(E)):
        for m in range(len(E)):
            w = E[m] - E[n]
            if w > 1e-10:
                s += 2.0 * (p[n] - p[m]) * Q[m, n] ** 2 / w ** 3
    return g * g * s

print("=" * 78)
print("VERIFY_D2_REDERIVE_FINAL -- independent model: 0.7 q^4 + 0.3 q^3, g=0.4")
print("=" * 78)

E, Q = bath_eig()
gap = E[1] - E[0]
pT = thermal(E, 1.5)
print(f"[model] first gaps: {E[1]-E[0]:.4f}, {E[2]-E[1]:.4f}, {E[3]-E[2]:.4f} "
      f"(anharmonic: unequal). State: thermal T=1.5 (passive).")

# ---------------------------------------------------------- (1a) KK route
# Im chi(w>0) = pi sum_{lines} (p_n-p_m)|Q_nm|^2 delta(w-w_nm)
# delta-m = g^2 (2/pi) Int Im chi / w^3 = 2 g^2 sum (p_n-p_m)|Q_nm|^2/w^3  -- the KK
# route collapses onto the pair sum ANALYTICALLY; the real independent checks are the
# dispersion at finite W (below) and the direct dynamical measurement (1c).
dm_formula = dm_pairsum(E, Q, pT, G)
print(f"\n[1b] pair-sum formula:            delta-m = {dm_formula:+.6f}")

# finite-W dispersion (independent finite-frequency form; W chosen well sub-gap)
W_meas = 0.20 * gap
def dm_disp(E, Q, p, g, W):
    s = 0.0
    for n in range(len(E)):
        for m in range(len(E)):
            w = E[m] - E[n]
            if w > 1e-10:
                s += 2.0 * (p[n] - p[m]) * Q[m, n] ** 2 / (w * (w * w - W * W))
    return g * g * s
dm_W = dm_disp(E, Q, pT, G, W_meas)
print(f"     dispersion at W=0.2*gap:      delta-m(W) = {dm_W:+.6f} (finite-W reference)")

# ---------------------------------------------------------- (1c) direct measurement
def measure_dm(E, Q, p, g, A, Om, ncyc_ramp=4, ncyc_meas=10, dt=0.004):
    """Exact unitary evolution under H(t)=diag(E) + g A s(t) cos(Om t) Q via
    instantaneous-eigh midpoint exponential. Returns (dm_meas, dE_bath)."""
    nk = len(E)
    H0 = np.diag(E).astype(float)
    Tp = 2 * np.pi / Om
    t_ramp = ncyc_ramp * Tp; T = (ncyc_ramp + ncyc_meas) * Tp
    nst = int(np.ceil(T / dt)); dt = T / nst
    U = np.eye(nk, dtype=complex)
    ts, Fv = [], []
    for k in range(nst):
        tm = (k + 0.5) * dt
        s = np.sin(0.5 * np.pi * tm / t_ramp) ** 2 if tm < t_ramp else 1.0
        f = g * A * s * np.cos(Om * tm)
        d, V = np.linalg.eigh(H0 + f * Q)
        U = (V * np.exp(-1j * d * dt)) @ (V.conj().T @ U)
        tn = (k + 1) * dt
        if tn >= t_ramp:
            qexp = float(np.real(np.einsum('in,in->n', U.conj(), Q @ U)) @ p)
            ts.append(tn); Fv.append(-g * qexp)
    assert np.abs(U.conj().T @ U - np.eye(nk)).max() < 1e-8, "unitarity lost"
    ts = np.array(ts); Fv = np.array(Fv)
    Fc = 2.0 * np.mean(Fv * np.cos(Om * ts))
    # exact adiabatic static reference (transported populations along sorted levels)
    npts = 200
    th = (np.arange(npts) + 0.5) * 2 * np.pi / npts
    Fst = np.empty(npts)
    for j, t in enumerate(th):
        Eu, Wv = np.linalg.eigh(Hb_f + (g * A * np.cos(t)) * qf)
        qd = np.einsum('ij,ij->j', Wv, qf @ Wv)[:len(E)]
        Fst[j] = -g * float(qd @ p)
    Fc_st = 2.0 * np.mean(Fst * np.cos(th))
    dEb = np.real(np.einsum('n,in,i,in->', p, U.conj(), E, U)) - float(p @ E)
    return (Fc - Fc_st) / (A * Om * Om), dEb

A_meas = 0.05     # weak drive: linear-response regime for the REACTIVE channel
dm_meas, dEb = measure_dm(E, Q, pT, G, A_meas, W_meas)
print(f"[1c] DIRECT measurement (A={A_meas}, W={W_meas:.3f}): "
      f"delta-m_meas = {dm_meas:+.6f}   dE_bath = {dEb:+.2e}")
rel = abs(dm_meas - dm_W) / abs(dm_W)
print(f"     measured vs dispersion-formula: rel. dev = {rel:.2%} "
      f"(finite-W formula is the right comparator)")
assert rel < 0.05, "direct measurement does NOT reproduce the formula"
assert dm_meas > 0 and dm_formula > 0 and dEb >= -1e-9
print("     -> FORMULA, SIGN (+, hardening) and PIPELINE independently CONFIRMED.")

# ---------------------------------------------------------- w^-3 power: gap sweep
print("\n[1d] w^-3 power check: two-level gap sweep, log-log slope of delta-m(w0):")
w0s = np.array([0.25, 0.5, 1.0, 2.0, 4.0])
dms = []
for w0 in w0s:
    E2 = np.array([0.0, w0]); Q2 = np.array([[0.0, 0.8], [0.8, 0.0]])
    p2 = np.array([0.85, 0.15])
    dms.append(dm_pairsum(E2, Q2, p2, 1.0))
slope = np.polyfit(np.log(w0s), np.log(dms), 1)[0]
print(f"     delta-m at w0={list(w0s)}: {['%.4g' % d for d in dms]}")
print(f"     log-log slope = {slope:+.6f}  (must be -3)")
assert abs(slope + 3.0) < 1e-10
# classical harmonic anchor (sign + normalization)
w0, gg, Wq = 1.0, 0.5, 0.3
Eh = np.arange(5) * w0 + 0.5
ah = np.diag(np.sqrt(np.arange(1, 5)), 1); qh = (ah + ah.T) / np.sqrt(2)
ph = np.zeros(5); ph[0] = 1.0
dm_qm = gg * gg * sum(2 * (ph[n] - ph[m]) * qh[m, n] ** 2 /
                      ((Eh[m] - Eh[n]) * ((Eh[m] - Eh[n]) ** 2 - Wq ** 2))
                      for n in range(5) for m in range(5) if Eh[m] - Eh[n] > 1e-12)
dm_cl = gg * gg / (w0 ** 2 * (w0 ** 2 - Wq ** 2))
print(f"     harmonic anchor: quantum {dm_qm:+.6f} vs classical {dm_cl:+.6f} "
      f"(dev {abs(dm_qm-dm_cl):.1e})")
assert abs(dm_qm - dm_cl) < 1e-12

# ---------------------------------------------------------- (2) moving worldline
print("\n[2] MOVING-WORLDLINE PREMISE: does instantaneous passivity survive transport?")
print("    (2a) spectra along x0 in [0,3]: check for level crossings (1D: none allowed)")
min_gap_along = np.inf
for u in np.linspace(0, 3 * G, 61):
    Eu, _ = bath_eig(u)
    min_gap_along = min(min_gap_along, np.diff(Eu).min())
print(f"         min level gap along the sweep: {min_gap_along:.4f} (> 0: NO crossings)")
assert min_gap_along > 1e-3
print("    (2b) exact slow dynamical sweep x: 0 -> 3 over T=600 (half-cosine ramp),")
print("         thermal T=1.5 start; final populations in the INSTANTANEOUS basis:")
nk = NK
H0 = np.diag(E).astype(float)
Tsw, dts = 600.0, 0.01
nst = int(Tsw / dts)
U = np.eye(nk, dtype=complex)
for k in range(nst):
    tm = (k + 0.5) * dts
    x = 3.0 * 0.5 * (1 - np.cos(np.pi * tm / Tsw))
    d, V = np.linalg.eigh(H0 + G * x * Q)
    U = (V * np.exp(-1j * d * dts)) @ (V.conj().T @ U)
assert np.abs(U.conj().T @ U - np.eye(nk)).max() < 1e-8
dfin, Vfin = np.linalg.eigh(H0 + G * 3.0 * Q)
pops_inst = (np.abs(Vfin.conj().T @ U) ** 2) @ pT    # populations in instantaneous basis
viol = sum(1 for i in range(nk - 8) for j in range(i + 1, nk - 8)
           if pops_inst[j] > pops_inst[i] + 1e-6)
print(f"         ordering violations (edge-excluded): {viol}  "
      f"top pops: {np.array2string(pops_inst[:5], precision=4)}")
assert viol == 0, "adiabatic transport BROKE passivity -- premise fails"
print("    (2c) delta-m(x0) >= 0 at every displacement (transported thermal state):")
dm_along = []
for u in np.linspace(0, 3 * G, 13):
    Eu, Qu = bath_eig(u)
    dm_along.append(dm_pairsum(Eu, Qu, pT, G))   # transported pops = same ordered list
print("         " + "  ".join(f"{d:+.4f}" for d in dm_along))
assert min(dm_along) > 0
print("    -> 1D no-crossing + adiabatic transport preserves ordering: the premise")
print("       HOLDS for adiabatic worldlines. Finite-speed reordering (LZ) costs the")
print("       drive energy first (checked in D2_3[d]) = a pump, not a passive channel.")

# ---------------------------------------------------------- (3) truncation independence
print("\n[3] Truncation independence of the measured point:")
E36, Q36 = bath_eig(0.0, 36)
p36 = thermal(E36, 1.5)
dm36 = dm_disp(E36, Q36, p36, G, W_meas)
a2 = np.diag(np.sqrt(np.arange(1, 560)), 1); qq = (a2 + a2.T) / np.sqrt(2)
Hb2 = np.diag(np.arange(560) + 0.5) + LAM4 * (qq @ qq @ qq @ qq) + LAM3 * (qq @ qq @ qq)
E560, W560 = np.linalg.eigh(Hb2)
Q560 = (W560.T @ qq @ W560)[:NK, :NK]
dm560 = dm_disp(E560[:NK], Q560, thermal(E560[:NK], 1.5), G, W_meas)
print(f"     dm(NF=440,NK=28) = {dm_W:+.6f} | dm(NK=36) = {dm36:+.6f} | "
      f"dm(NF=560) = {dm560:+.6f}")
assert abs(dm36 - dm_W) < 5e-3 * abs(dm_W) + 1e-6
assert abs(dm560 - dm_W) < 1e-4 * abs(dm_W) + 1e-9
print("     -> no truncation artifact at the verifier's settings.")

# ---------------------------------------------------------- (4) footings + band
print("\n[4] FOOTING FORKS + galactic band:")
c_ = 2.998e8; H0c = 67.4e3 / 3.0857e22; Z_ = np.sqrt(32 * np.pi / 3)
a0_can = c_ * H0c * np.sqrt(0.685) / Z_
a0_alt = c_ * H0c / Z_
print(f"     Z = {Z_:.4f}; a0 canonical (rho_DE) = {a0_can:.3e} m/s^2; "
      f"alternate (rho_tot) = {a0_alt:.3e} (spread {100*(a0_alt/a0_can-1):.1f}%)")
Olo, Ohi = 3.2e-17, 1.9e-14
print(f"     band W = [{Olo:.1e}, {Ohi:.1e}] rad/s. Sub-gap hardening theorem covers the")
print(f"     band iff all populated bath gaps > W_hi = {Ohi:.1e} rad/s (hbar*W_hi ="
      f" {1.0546e-34*Ohi/1.602e-19:.1e} eV -- any lab/astro bath satisfies this).")
print(f"     A passive softening pole must sit BELOW {Olo:.1e} rad/s"
      f" (< {1.0546e-34*Olo/1.602e-19:.1e} eV) -> hexad IV/V clamp. Footing shift moves y")
print(f"     by 21% but the sign theorem is scale-FREE: verdict footing-independent.")

print("\nVERIFIER-FINAL VERDICT: pair-sum formula (sign, w^-3, normalization) and the")
print("instantaneous-passivity premise independently CONFIRMED on a different")
print("anharmonic model, truncation, and integrator. delta-m >= 0 for passive baths")
print("in the adiabatic/sub-gap regime stands.")
