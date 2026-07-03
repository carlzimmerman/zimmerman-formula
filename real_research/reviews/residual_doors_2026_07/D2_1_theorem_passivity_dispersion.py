#!/usr/bin/env python3
"""
D2_1 -- THE PASSIVE-ANHARMONIC CORNER: theorem route (lane D2, residual doors 2026-07)

QUESTION: does PASSIVITY alone (not full KMS) force the worldline mass dressing
delta-m >= 0 for a GENERAL anharmonic/structured bath?

SETUP (worldline dressing dispersion relation, derived here and verified numerically):
  H = H_bath + g x B  (x = worldline coordinate, B = any Hermitian bath operator).
  Induced force on the worldline: F_ind(w) = g^2 chi_BB(w) X(w)   [chi: Kubo response,
  convention H' = -f B, d<B> = chi f]. Matching F_ext = -m_eff w^2 X + k_eff X gives
     m_eff(W) = m + g^2 [Re chi(W) - chi(0)] / W^2
             = m + g^2 SUM_{pairs E_m>E_n} 2 (p_n - p_m) |B_nm|^2 / (w_nm (w_nm^2 - W^2))
     delta-m(W->0) = g^2 SUM 2 (p_n - p_m) |B_nm|^2 / w_nm^3      (static dressing)
  (Kramers-Kronig form: delta-m = g^2 (2/pi) Int_0^inf dw Im chi(w) / w^3.)

THEOREM (linear response; ANY bath spectrum incl. anharmonic; ANY stationary passive state):
  A stationary state commutes with H_bath -> common eigenbasis exists. In it
     Im chi(w>0) = pi SUM_{w_mn = w} (p_n - p_m) |B_nm|^2 .
  Passivity (Pusz-Woronowicz: rho passive iff [rho,H]=0 and E_m > E_n => p_n >= p_m)
  makes EVERY Bohr-line weight >= 0, i.e. w Im chi(w) >= 0 for all w. Hence
     (i)  delta-m(0) >= 0                (static dressing: anti-MOND sign, term by term)
     (ii) m_eff(W) >= m for every SUB-GAP drive (W below all populated Bohr lines)
     (iii) m_eff(W) < m is possible ONLY via a populated Bohr line BELOW the drive
           (w_nm < W): the SUB-DRIVE POLE. That is hexad IV/V territory (frequency law
           mu_eff(W), never mu(a/a0); gas clamp) -- not a new door.
  Operational route (no eigenbasis needed): if w0 Im chi(w0) < 0, a weak cyclic drive
  at w0 extracts work at O(f^2), contradicting passivity (which holds at ALL orders,
  Pusz-Woronowicz). KMS is NOT needed: passivity suffices. KMS states additionally obey
  FDT Im chi = pi (1 - e^{-bw}) S(w) (checked below); general passive states are exactly
  the ordered-population states -- the spectral proof covers them all.

This script verifies each step numerically on random anharmonic spectra, runs an
adversarial counterexample search over the passive polytope, and does exact
time-domain work-per-cycle tests (weak AND strong drive, i.e. beyond linear response
for the dissipative channel).

Footing forks printed at the end. Exit 0.
"""
import numpy as np

rng = np.random.default_rng(20260702)

# ---------------------------------------------------------------- helpers
def random_spectrum(N, rng):
    gaps = rng.uniform(0.08, 1.2, N - 1)
    return np.concatenate([[0.0], np.cumsum(gaps)])

def random_B(N, rng):
    X = rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N))
    return (X + X.conj().T) / 2

def passive_p(N, rng):
    return np.sort(rng.dirichlet(np.ones(N)))[::-1]

def dm_static(E, p, B, g=1.0, wmin=1e-9):
    """delta-m(W->0) = g^2 sum_pairs 2 (p_n-p_m)|B_nm|^2 / w^3 (E_m > E_n)."""
    s = 0.0
    N = len(E)
    for n in range(N):
        for m in range(N):
            w = E[m] - E[n]
            if w > wmin:
                s += 2.0 * (p[n] - p[m]) * abs(B[m, n]) ** 2 / w ** 3
    return g * g * s

def dm_at(E, p, B, Om, g=1.0, wmin=1e-9):
    """delta-m(W) = g^2 sum_pairs 2 (p_n-p_m)|B_nm|^2 / (w (w^2 - W^2))."""
    s = 0.0
    N = len(E)
    for n in range(N):
        for m in range(N):
            w = E[m] - E[n]
            if w > wmin:
                s += 2.0 * (p[n] - p[m]) * abs(B[m, n]) ** 2 / (w * (w * w - Om * Om))
    return g * g * s

def evolve_work(E, B, p, A, Om, ncyc, dt):
    """Exact cyclic protocol H(t)=diag(E)+A sin(Om t) B over integer cycles
    (f(0)=f(T)=0 -> cyclic). Returns bath energy change = work pumped in.
    Strang splitting; exact theorem says >= 0 for passive p at ANY amplitude."""
    N = len(E)
    d, V = np.linalg.eigh(B)
    T = 2 * np.pi / Om * ncyc
    nst = int(np.ceil(T / dt))
    dt = T / nst
    U = np.eye(N, dtype=complex)
    ph = np.exp(-1j * E * dt / 2.0)
    Vh = V.conj().T
    with np.errstate(all='ignore'):  # Apple-Accelerate zgemm raises spurious FP flags
        for k in range(nst):
            f = A * np.sin(Om * (k + 0.5) * dt)
            U = ph[:, None] * (V @ (np.exp(-1j * f * d * dt)[:, None] * (Vh @ (ph[:, None] * U))))
    assert np.abs(U.conj().T @ U - np.eye(N)).max() < 1e-9, "unitarity lost"
    # <H0>_final - <H0>_initial for rho0 = diag(p)
    Ef = np.real(np.einsum('n,in,i,in->', p, U.conj(), E, U))
    return Ef - float(p @ E)

print("=" * 78)
print("D2_1  PASSIVE-ANHARMONIC CORNER -- THEOREM ROUTE")
print("=" * 78)

# ------------------------------------------------ PART A: spectral positivity
print("\n[A] Spectral proof check: random anharmonic spectra x random B x random")
print("    passive states. Every Bohr-line weight (p_n-p_m)|B_nm|^2 and the full")
print("    static dressing delta-m must be >= 0.")
min_w, min_dm = np.inf, np.inf
trials = 2000
for _ in range(trials):
    N = int(rng.integers(5, 15))
    E, B, p = random_spectrum(N, rng), random_B(N, rng), passive_p(N, rng)
    for n in range(N):
        for m in range(N):
            if E[m] > E[n] + 1e-12:
                min_w = min(min_w, (p[n] - p[m]) * abs(B[m, n]) ** 2)
    min_dm = min(min_dm, dm_static(E, p, B))
print(f"    {trials} trials: min Bohr-line weight = {min_w:.3e}   min delta-m = {min_dm:.3e}")
assert min_w >= -1e-15 and min_dm >= -1e-12, "PASSIVITY POSITIVITY VIOLATED"
print("    -> w*Im[chi(w)] >= 0 and delta-m >= 0 for ALL passive anharmonic cases. PASS")

# ------------------------------------------------ PART B: adversarial minimum
print("\n[B] Adversarial search: delta-m is LINEAR in p; the passive set is the")
print("    convex hull of uniform-mixtures-over-lowest-k. Min over extreme points:")
worst = np.inf
for _ in range(400):
    N = int(rng.integers(5, 13))
    E, B = random_spectrum(N, rng), random_B(N, rng)
    for k in range(1, N + 1):
        p = np.zeros(N); p[:k] = 1.0 / k
        worst = min(worst, dm_static(E, p, B))
print(f"    global min over 400 systems x all extreme passive states: {worst:.3e}")
assert worst >= -1e-12
# control: relax passivity -> negative dressing trivially available
E2 = np.array([0.0, 0.15, 1.3, 2.1]); B2 = random_B(4, rng)
p_inv = np.array([0.1, 0.6, 0.2, 0.1])          # population inversion on the soft pair
dm_inv = dm_static(E2, p_inv, B2)
print(f"    control (NON-passive, inverted soft pair): delta-m = {dm_inv:+.3e}  (<0 as expected)")
assert dm_inv < 0
print("    -> minimum over passive polytope is 0 (term-by-term); negative dressing")
print("       requires population inversion = a PUMP. PASS")

# ------------------------------------------------ PART C: exact cyclic work
print("\n[C] Exact-dynamics work test (beyond linear response in drive amplitude):")
print("    cyclic drive A sin(Wt) B, integer cycles; passive states must ABSORB")
print("    (dE_bath >= 0) at every amplitude; inverted control may emit.")
wmin_pass, wmax_emit = np.inf, np.inf
for sysid in range(2):
    N = 8
    E, B = random_spectrum(N, rng), random_B(N, rng)
    bohr = E[1] - E[0]
    for Om in [bohr, 0.7 * (E[2] - E[0]), 1.4]:
        for A in [0.02, 0.5, 3.0]:
            for st in range(2):
                p = passive_p(N, rng) if st else np.exp(-E / 1.0) / np.sum(np.exp(-E / 1.0))
                dE = evolve_work(E, B, p, A, Om, ncyc=12, dt=0.004)
                wmin_pass = min(wmin_pass, dE)
            p_bad = np.zeros(N); p_bad[2] = 0.7; p_bad[0] = 0.3   # inverted
            wmax_emit = min(wmax_emit, evolve_work(E, B, p_bad, A, Om, ncyc=12, dt=0.004))
print(f"    min dE over passive runs (weak->strong A): {wmin_pass:+.3e}  (>= 0 required)")
print(f"    min dE over inverted-control runs:         {wmax_emit:+.3e}  (<0 shows test has teeth)")
assert wmin_pass >= -1e-7, "passive work positivity violated beyond numerics"
assert wmax_emit < -1e-4
print("    -> Pusz-Woronowicz confirmed non-perturbatively: no work extraction from")
print("       passive anharmonic baths at ANY drive strength. PASS")

# ------------------------------------------------ PART D: where softening CAN live
print("\n[D] m_eff(W) dispersion for a passive bath WITH a soft mode (w1=0.3):")
E3 = np.array([0.0, 0.3, 1.5, 2.4])
B3 = random_B(4, rng)
p3 = np.exp(-E3 / 0.5); p3 /= p3.sum()
for Om in [0.05, 0.15, 0.25, 0.45, 0.8, 1.05]:  # off Bohr lines {0.3,0.9,1.2,1.5,2.1,2.4}
    dm = dm_at(E3, p3, B3, Om)
    tag = "sub-gap: HARDENING (+)" if Om < 0.3 else "above soft line: sub-drive pole, can soften (-)"
    print(f"    W = {Om:4.2f} : delta-m(W) = {dm:+9.4f}   {tag}")
dm_sub = dm_at(E3, p3, B3, 0.15); dm_sup = dm_at(E3, p3, B3, 0.8)
assert dm_sub > 0
print(f"    W-scaling above the pole: delta-m ~ -C/W^2 (FREQUENCY law, amplitude-blind;")
print(f"    linear response is amplitude-independent by construction) -> this is exactly")
print(f"    hexad IV (sub-drive pole / frequency law) + V (gas clamp), NOT mu(a/a0).")

# ------------------------------------------------ PART E: KMS/FDT consistency
print("\n[E] KMS check (passivity does NOT need it, but verify FDT on thermal states):")
beta, E4, B4 = 1.7, random_spectrum(7, rng), random_B(7, rng)
p4 = np.exp(-beta * E4); p4 /= p4.sum()
maxdev = 0.0
for n in range(7):
    for m in range(7):
        w = E4[m] - E4[n]
        if w > 1e-9:
            lhs = (p4[n] - p4[m])                    # Im chi weight / (pi |B|^2)
            rhs = p4[n] * (1 - np.exp(-beta * w))    # (1-e^{-bw}) S weight
            maxdev = max(maxdev, abs(lhs - rhs))
print(f"    max |Imchi_w - (1-e^-bw) S_w| over Bohr lines: {maxdev:.2e}  (FDT holds)")
assert maxdev < 1e-12
print("    Passive-but-not-KMS states (arbitrary ordered p): covered by [A]-[C] directly.")

# ------------------------------------------------ PART F: footing forks
print("\n[F] FOOTING FORKS (where scale enters this corner):")
c = 2.998e8; H0 = 67.4 * 1000 / 3.0857e22; OmL = 0.685
Z = np.sqrt(32 * np.pi / 3)
a0_can = c * H0 * np.sqrt(OmL) / Z
a0_alt = c * H0 / Z
print(f"    Z = sqrt(32pi/3) = {Z:.4f}")
print(f"    a0 canonical (rho_DE, cH_L/Z)  = {a0_can:.3e} m/s^2")
print(f"    a0 alternate (rho_tot, cH0/Z)  = {a0_alt:.3e} m/s^2   (spread {100*(a0_alt/a0_can-1):.1f}%)")
for gbar in [1e-10, 1e-11]:
    fc = 1 / np.sqrt(1 + a0_can / gbar); fa = 1 / np.sqrt(1 + a0_alt / gbar)
    print(f"    required m_eff/m at g_bar={gbar:.0e}: canonical {fc:.3f} | alternate {fa:.3f}"
          f"  (framework nu = sqrt(1+1/y))")
hbar = 1.0546e-34
Olo, Ohi = 3.2e-17, 1.9e-14
print(f"    Galactic band W = [{Olo:.1e}, {Ohi:.1e}] rad/s (footing-INDEPENDENT, kinematic).")
print(f"    A passive sub-drive pole must sit BELOW the band: hbar*w0 < {hbar*Olo:.1e} J"
      f" = {hbar*Olo/1.602e-19:.1e} eV -- and is then clamped by hexad V.")

print("\nVERDICT [D2_1]: passivity alone (no KMS needed) forces w*Imchi >= 0 and")
print("delta-m >= 0 for ANY anharmonic bath in linear response; the only in-band")
print("softening channel is the sub-drive pole = hexad IV/V. No new door here.")
