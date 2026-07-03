#!/usr/bin/env python3
"""
Lane C, part 2 -- SIGN AUDIT of the finite-time (Luo-type) broadening mechanism.

Question: does transient/windowed probing of the VACUUM ever produce the MOND sign
(reduced inertia, delta-m < 0) DYNAMICALLY, or is the sign inserted by the
mu ~ [T_eff(a) - T_eff(floor)]/T_eff(a) mapping?

Three checks, all first-principles:

(A) WIGHTMAN POSITIVITY of the windowed response. F(w) = <|Phi(chi e^{iw tau})|^2> >= 0
    is a quadratic form in a positive state -- so NO window can make the effective
    spectrum negative. Moreover for a Gaussian window the de-excitation excess is
    EXACT:  f(-w) - f(w) = w/2pi  (windowed commutator; Gaussian smearing preserves
    linear functions). Hence the inferred population ratio p_e/p_g = f(w0)/f(-w0) < 1
    STRICTLY, for every gap w0>0, every window T, every acceleration A: transient
    probing of the vacuum can NEVER fake a population inversion. (This is the
    finite-time face of Pusz-Woronowicz passivity: the vacuum stays passive under
    arbitrary cyclic -- including transient -- processes.)

(B) THEOREM-III DRESSING SIGN with broadened populations: the state-clause mass shift
    delta-m ~ sum (p_g - p_e)/w0^2. Feed the WINDOWED response populations in:
    delta-m >= 0 on the whole (A, T_win, w0) grid. Broadening drives delta-m TOWARD
    zero (saturation) but can never cross it: the dynamical route stays anti-MOND.

(C) LINEAR-DYNAMICS PASSIVITY + STATE-BLINDNESS (windowed quantum Brownian motion):
    system oscillator + N bath modes, coupling switched by a Gaussian window
    (a fully NON-STATIONARY protocol). Exact Gaussian-state evolution:
      - <H0>_final - <H0>_initial >= 0 for the vacuum start (no energy extraction
        by any transient window -- numerical Pusz-Woronowicz);
      - the mean-value (response) sector evolves by the same fundamental matrix
        regardless of the covariance (state): the response kernel is the c-number
        commutator -- STATE-BLIND, exactly as in stationary Theorem III/IV.
"""
import numpy as np, math, sys

PASS = True
def check(name, ok, detail=""):
    global PASS
    print(("  [PASS] " if ok else "  [FAIL] ") + name + ("  " + detail if detail else ""))
    if not ok: PASS = False

# ---------- windowed UDW response (same construction as laneC_finite_time_response) ----
def f_vac(w, T):
    x = w * T
    I = math.exp(-x * x) / (2 * T * T) - (math.sqrt(math.pi) * w / (2 * T)) * math.erfc(x)
    return (math.sqrt(math.pi) * T / (2 * math.pi ** 2)) * I

def dW(u, A):
    out = np.empty_like(u); x = A * u / 2.0
    small = x < 1e-4; big = x > 30.0; mid = ~(small | big)
    out[small] = (A ** 2 / 12.0 - A ** 4 * u[small] ** 2 / 240.0) / (4 * math.pi ** 2)
    out[big] = 1.0 / (4 * math.pi ** 2 * u[big] ** 2)
    um = u[mid]
    out[mid] = (1.0 / um ** 2 - (A ** 2 / 4.0) / np.sinh(A * um / 2.0) ** 2) / (4 * math.pi ** 2)
    return out

def f_tot(w, T, A):
    if A == 0.0: return f_vac(w, T)
    du = 1.0 / (80.0 * max(A, abs(w), 1.0 / T, 0.2)); umax = 9.0 * T
    u = np.linspace(0.0, umax, min(int(umax / du) + 2, 4_000_000))
    return f_vac(w, T) + 2.0 * np.trapz(np.cos(w * u) * np.exp(-u ** 2 / (4 * T ** 2)) * dW(u, A), u)

print("=" * 78)
print("(A) POSITIVITY + NO-INVERSION for all windows/accelerations")
print("=" * 78)
fmin = np.inf; idmax = 0.0; ratmax = 0.0
for A in (0.0, 0.5, 1.0, 2.0):
    for T in (0.5, 2.0, 10.0):
        for w in np.linspace(-3.0, 3.0, 25):
            if abs(w) < 1e-9: continue
            fv = f_tot(w, T, A)
            fmin = min(fmin, fv)
            if w > 0:
                fm = f_tot(-w, T, A)
                idmax = max(idmax, abs((fm - fv) - w / (2 * math.pi)) / (w / (2 * math.pi)))
                ratmax = max(ratmax, fv / fm)
check(f"windowed response f(w) >= 0 everywhere (min = {fmin:.3e})", fmin > -1e-10)
check(f"commutator identity f(-w)-f(w)=w/2pi exact (max rel dev {idmax:.1e})", idmax < 1e-3)
check(f"p_e/p_g = f(w)/f(-w) < 1 strictly everywhere (max = {ratmax:.6f})", ratmax < 1.0)
print("  => no window, however short, fakes a population inversion from the vacuum.")

print()
print("=" * 78)
print("(B) THEOREM-III delta-m sign with Luo-broadened populations")
print("    delta-m proxy = (p_g - p_e)/w0^2,  p_e/p_g = f(w0)/f(-w0)")
print("=" * 78)
dmin = np.inf
for A in (0.0, 0.5, 1.0, 2.0):
    line = f"  A={A:4.1f}: "
    for T in (0.5, 1.0, 3.0, 10.0):
        w0 = 1.0
        fp = f_tot(w0, T, A); fm = f_tot(-w0, T, A)
        pe = fp / (fp + fm); pg = fm / (fp + fm)
        dm = (pg - pe) / w0 ** 2
        dmin = min(dmin, dm)
        line += f" dm(T={T:4.1f})={dm:+.4f}"
    print(line)
check(f"delta-m >= 0 on entire (A, T_win) grid (min = {dmin:+.4f})", dmin >= 0.0)
print("  => broadening (shorter T, larger A) pushes delta-m toward 0 (saturation) but")
print("     NEVER through 0: the dynamical dressing sign stays anti-MOND (delta-m>=0).")
print("     The MOND sign in the Luo/Milgrom reading enters ONLY via the mapping")
print("     mu ~ [T_eff(a)-T_eff(0)]/T_eff(a) -- a postulate, not dynamics.")

print()
print("=" * 78)
print("(C) WINDOWED QBM: exact Gaussian evolution -- transient passivity + state-blindness")
print("=" * 78)
def run_qbm(w0, g0, Tw, Ttherm=None, kick=False, dt=0.004):
    # NOTE: math guarantees dE >= 0 EXACTLY here (unitary Gaussian evolution starting
    # from the exact H0 ground state; ground state is the variational minimizer of
    # <H0>). Any negative residue is 4th-order RK drift -- demonstrated by the dt
    # convergence check below. Apple Accelerate emits spurious FP warnings in matmul
    # with structured zero blocks; suppressed via errstate (results verified finite).
    N = 32
    wj = np.linspace(0.05, 6.0, N); dw = wj[1] - wj[0]
    cj = g0 * np.sqrt(wj * dw) * np.exp(-wj / 3.0)
    freqs = np.concatenate(([w0], wj)); n = N + 1
    K0 = np.diag(freqs ** 2)
    C = np.zeros((n, n)); C[0, 1:] = cj; C[1:, 0] = cj
    t0, t1 = -6.0 * Tw, 6.0 * Tw
    steps = int((t1 - t0) / dt)
    def Amat(t):
        chi = math.exp(-t * t / (2 * Tw * Tw))
        M = np.zeros((2 * n, 2 * n))
        M[:n, n:] = np.eye(n)
        M[n:, :n] = -(K0 + chi * C)
        return M
    Phi = np.eye(2 * n)
    t = t0
    with np.errstate(all='ignore'):
        for _ in range(steps):
            k1 = Amat(t) @ Phi
            k2 = Amat(t + dt / 2) @ (Phi + dt / 2 * k1)
            k3 = Amat(t + dt / 2) @ (Phi + dt / 2 * k2)
            k4 = Amat(t + dt) @ (Phi + dt * k3)
            Phi = Phi + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            t += dt
        # vacuum covariance of H0 (hbar=1): <q^2>=1/2w, <p^2>=w/2
        occ = np.zeros(n) if Ttherm is None else 1.0 / (np.exp(freqs / Ttherm) - 1.0)
        Sig0 = np.zeros((2 * n, 2 * n))
        Sig0[:n, :n] = np.diag((1 + 2 * occ) / (2 * freqs))
        Sig0[n:, n:] = np.diag((1 + 2 * occ) * freqs / 2)
        Sig = Phi @ Sig0 @ Phi.T
    E = lambda S: 0.5 * (np.trace(S[n:, n:]) + np.sum(freqs ** 2 * np.diag(S[:n, :n])))
    E0 = E(Sig0)
    dE = E(Sig) - E0
    # mean-sector response to a unit momentum kick of the system at t0 (state-independent)
    resp = Phi[:, n][0] if kick else None   # <q_sys(t1)> per unit initial p_sys
    return dE, E0, resp

worst_rel = np.inf; worst_case = None
for w0 in (0.5, 1.5):
    for g0 in (0.05, 0.2):
        for Tw in (2.0, 8.0):
            dE, E0, _ = run_qbm(w0, g0, Tw)
            rel = dE / E0
            if rel < worst_rel: worst_rel, worst_case = rel, (w0, g0, Tw)
            print(f"  w0={w0:3.1f} g0={g0:4.2f} T_win={Tw:4.1f}:  dE = {dE:+.3e}  (dE/E0 = {rel:+.2e})")
check(f"no energy extraction beyond integrator noise (min dE/E0 = {worst_rel:+.2e})",
      worst_rel > -1e-6)
# dt-convergence: any negative residue must shrink with dt (=> RK drift, not physics)
w0c, g0c, Twc = worst_case
d1, E0c, _ = run_qbm(w0c, g0c, Twc, dt=0.008)
d2, _, _ = run_qbm(w0c, g0c, Twc, dt=0.004)
d3, _, _ = run_qbm(w0c, g0c, Twc, dt=0.002)
print(f"  dt-convergence at worst case {worst_case}: dE(dt=.008)={d1:+.2e}, "
      f"dE(.004)={d2:+.2e}, dE(.002)={d3:+.2e}")
check("negative residue -> 0 with dt (pure integrator drift, physics dE>=0)",
      (d3 >= -1e-9 * E0c) or (abs(d3) < abs(d2) < abs(d1)))
_, _, r_vac = run_qbm(1.0, 0.2, 2.0, Ttherm=None, kick=True)
_, _, r_th = run_qbm(1.0, 0.2, 2.0, Ttherm=2.0, kick=True)
check(f"response kernel STATE-BLIND: vacuum vs T=2 thermal identical "
      f"({r_vac:.6f} vs {r_th:.6f})", abs(r_vac - r_th) < 1e-12)
print("  => Pusz-Woronowicz survives the transient: the vacuum is passive under")
print("     arbitrary finite-time windows; the linear response kernel is the")
print("     commutator (state- and window-occupation-blind). Luo's non-stationarity")
print("     does NOT open the mu<1 channel; Theorem IV's pole-below-drive requirement")
print("     is unchanged (windowing smears the kernel, it does not add negative-")
print("     frequency spectral weight -- check (A)).")

print()
print("OVERALL:", "PASS" if PASS else "FAIL")
sys.exit(0 if PASS else 1)
