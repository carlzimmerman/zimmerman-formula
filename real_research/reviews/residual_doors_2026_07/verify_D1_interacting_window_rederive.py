#!/usr/bin/env python3
"""
verify_D1_interacting_window_rederive.py  (ADVERSARIAL VERIFIER, lane D1)
==========================================================================
Independent re-derivation + numerical test of the single most load-bearing
step of lane D1: the Kallen-Lehmann POSITIVE-MIXTURE reduction of the
interacting-vacuum windowed detector response,

    F_int(omega) = int dmu^2 rho(mu^2) F_mu^free(omega),   rho >= 0,

exact at 2nd order in the detector coupling for ANY trajectory + window.

PART A -- solvable interacting-class test (composite operator):
O = :phi^2: of a free massive scalar (m=1) in 1+1D. Its exact vacuum
two-point function is W_c(x) = 2[Delta+_m(x)]^2 -- NOT a free two-point
function; it has a genuine two-particle continuum. KL density derived
INDEPENDENTLY here (no fitted constants):
  2 Delta+^2 = int_{4m^2} dmu^2 rho(mu^2) Delta+_mu,
  CM-frame Jacobian match (2-to-1 branch counting) gives
      rho(mu^2) = 1/(2 pi mu k*),  k* = sqrt(mu^2/4 - m^2)
                = 1/(pi mu^2 beta),  beta = sqrt(1-4m^2/mu^2)  >= 0.
TEST: windowed response on a NON-UNIFORM (burst) trajectory computed two
independent ways:
  Route 1 (direct): pull back W_c(tau_a,tau_b) = 2 Delta+^2 in position
    space (mode integral per pair, e^{-eps.omega} damping) -> double sum.
  Route 2 (mixture): int dmu^2 rho(mu^2) F_mu^free(omega) with the free
    1+1 slice mode-sum (same e^{-eps.Omega} damping: pair energy
    omega1+omega2 EQUALS slice mode energy, so damping matches exactly).
Agreement with no fitted constants validates BOTH the reduction identity
AND the positivity of rho. Then: inversion check on the composite.

PART B -- OPEN attack: free massive 3+1 slices OUTSIDE the lane's grid
(their scan fixed T=1, centered windows, s>=0.05, v0<=0.9, Om<=10,
m in {2,6}). Attack configs: light mass m=0.5; sharp burst s=0.02 at
v0=0.95; chirped drive; SHORT window T=0.3; OFF-CENTER window on a kick;
resonance-tuned oscillation (the lattice free-chain 407x analog, tuned
Om ~ excitation threshold). Any inversion in an UNDRIVEN slice = major.
"""
import numpy as np

m = 1.0
eps = 0.10   # mode damping e^{-eps.omega}; MUST exceed the tau-grid spacing
             # so the (log)^2 coincidence ridge of Delta+^2 is RESOLVED by
             # the discrete double sum (eps << grid gave a constant additive
             # offset ~3e-3 -- a pure discretization artifact, both routes
             # share the same eps so the identity test is exact either way)

# ---------------- PART A ---------------------------------------------------
print("=" * 72)
print("PART A: KL reduction on the solvable composite :phi^2:, 1+1D, m=1")
print("=" * 72)

Ntau = 401
tauA = np.linspace(-4.0, 4.0, Ntau)
dtA = tauA[1] - tauA[0]
TA = 1.0
chiA = np.exp(-tauA ** 2 / (2 * TA ** 2))

# burst trajectory v(tau) = 0.8 exp(-tau^2/(2*0.3^2))
vA = 0.8 * np.exp(-tauA ** 2 / (2 * 0.3 ** 2))
gamA = 1.0 / np.sqrt(1 - vA ** 2)
tA = np.concatenate([[0], np.cumsum(0.5 * (gamA[1:] + gamA[:-1]) * dtA)])
xA = np.concatenate([[0], np.cumsum(0.5 * ((gamA * vA)[1:] + (gamA * vA)[:-1]) * dtA)])
tA -= tA[Ntau // 2]; xA -= xA[Ntau // 2]

# --- Route 1: direct position-space W_c = 2 Delta+^2 ----------------------
# Delta+(dt,dx) = int_0^inf dk cos(k dx) e^{-i w(k) dt} e^{-eps w} /(2 pi w)
kg, wg = np.polynomial.legendre.leggauss(3000)
kmaxA = 300.0   # e^{-0.1*300} = 1e-13 tail; ~14 nodes per oscillation period
kk = 0.5 * kmaxA * (kg + 1); kwt = 0.5 * kmaxA * wg
wk = np.sqrt(kk ** 2 + m ** 2)
damp = np.exp(-eps * wk) / (2 * np.pi * wk) * kwt

DT = (tA[:, None] - tA[None, :]).ravel()
DX = (xA[:, None] - xA[None, :]).ravel()
Wc = np.zeros(DT.size, dtype=complex)
CH = 2000  # pair chunk
for i0 in range(0, DT.size, CH):
    sl = slice(i0, min(i0 + CH, DT.size))
    ph = np.exp(-1j * np.outer(DT[sl], wk)) * np.cos(np.outer(DX[sl], kk))
    Dp = ph @ damp
    Wc[sl] = 2.0 * Dp ** 2          # <:phi^2::phi^2:> = 2 Delta+^2
Wc = Wc.reshape(Ntau, Ntau)

om_chk = np.array([0.5, 1.0, 2.0, 3.0])

def F_direct(w):
    v = chiA * np.exp(1j * w * tauA) * dtA   # kernel e^{-i w (ta-tb)} W
    return np.real(np.conj(v) @ (Wc @ v))    # v^dag W v (Gram convention
                                             # as in D1_1: F(+w)=excitation)

# --- Route 2: KL mixture with independently derived rho -------------------
def F_slice_1p1(mu, w):
    """free 1+1 mass-mu windowed response on the SAME trajectory, with
    the SAME e^{-eps Omega} damping (pair energy == slice mode energy)."""
    Pg, Pw = np.polynomial.legendre.leggauss(500)
    Pmax = 30.0
    P = Pmax * Pg; Pwt = Pmax * Pw
    Om = np.sqrt(P ** 2 + mu ** 2)
    meas = np.exp(-eps * Om) / (4 * np.pi * Om) * Pwt
    phase = np.exp(-1j * (np.outer(Om, tA) - np.outer(P, xA)))
    g = phase @ (chiA * np.exp(-1j * w * tauA) * dtA)
    return np.sum(meas * np.abs(g) ** 2)

# mu integral: mu = 2m + u^2 kills the integrable 1/beta endpoint
ug, uw = np.polynomial.legendre.leggauss(48)
umax = np.sqrt(16.0 - 2 * m)
uu = 0.5 * umax * (ug + 1); uwt = 0.5 * umax * uw
muA = 2 * m + uu ** 2
kstar = np.sqrt(muA ** 2 / 4 - m ** 2)
rho = 1.0 / (2 * np.pi * muA * kstar)        # INDEPENDENT derivation
dmu2_du = 2 * muA * (2 * uu)                 # dmu^2 = 2 mu dmu, dmu = 2u du

def F_mix(w):
    return np.sum(uwt * dmu2_du * rho *
                  np.array([F_slice_1p1(mu, w) for mu in muA]))

print(f"{'omega':>6s} {'F_direct':>13s} {'F_mixture':>13s} {'rel.diff':>9s}")
ok = True
vals = []
for w in np.concatenate([om_chk, -om_chk]):
    fd, fm = F_direct(w), F_mix(w)
    rd = abs(fd / fm - 1) if abs(fm) > 1e-12 else 0.0
    vals.append((w, fd, fm, rd))
    scale_ok = max(abs(fd), abs(fm)) > 1e-9   # above quadrature floor
    if scale_ok:
        ok &= rd < 3e-2
    print(f"{w:6.1f} {fd:13.6e} {fm:13.6e} {rd:9.2e}")
assert ok, "KL positive-mixture reduction FAILS numerically!"
print("PASS: direct interacting-class response == positive KL mixture of")
print("free slices, NO fitted constants (rho = 1/(pi mu^2 beta) derived")
print("independently). The load-bearing D1_3 reduction step is CORRECT.")

# composite inversion check on the burst
idxA = -np.inf
for w in np.linspace(0.2, 3.0, 15):
    fp, fmm = F_direct(w), F_direct(-w)
    if max(fp, fmm) > 1e-9:
        idxA = max(idxA, (fp - fmm) / max(fp, fmm))
print(f"composite :phi^2: burst inversion index (max over w>0): {idxA: .3e}")
assert idxA < 0, "composite operator inverted on undriven burst?!"

# ---------------- PART B ---------------------------------------------------
print()
print("=" * 72)
print("PART B: OPEN attack -- 3+1 free slices OUTSIDE the lane's grid")
print("=" * 72)

def F31(mm, vfun, T, tau0=0.0, half_range=4.0, Ntau=1201, Nk=300, Nc=24,
        kmax=90.0, omegas=None):
    tau = np.linspace(-half_range, half_range, Ntau)
    dt = tau[1] - tau[0]
    chi = np.exp(-(tau - tau0) ** 2 / (2 * T ** 2))
    v = vfun(tau); assert np.max(np.abs(v)) < 0.965
    gam = 1.0 / np.sqrt(1 - v ** 2)
    t = np.concatenate([[0], np.cumsum(0.5 * (gam[1:] + gam[:-1]) * dt)])
    x = np.concatenate([[0], np.cumsum(0.5 * ((gam * v)[1:] + (gam * v)[:-1]) * dt)])
    t -= t[Ntau // 2]; x -= x[Ntau // 2]
    kg, kw = np.polynomial.legendre.leggauss(Nk)
    k = 0.5 * kmax * (kg + 1); kwt = 0.5 * kmax * kw
    cg, cw = np.polynomial.legendre.leggauss(Nc)
    wkE = np.sqrt(k ** 2 + mm ** 2)
    K = np.repeat(k, Nc); C = np.tile(cg, Nk)
    WE = np.repeat(wkE, Nc)
    meas = (np.repeat(kwt * k ** 2 / wkE, Nc) * np.tile(cw, Nk)) / (8 * np.pi ** 2)
    Fp = np.zeros(len(omegas)); Fm = np.zeros(len(omegas))
    CHK = 2400
    for i0 in range(0, K.size, CHK):
        sl = slice(i0, min(i0 + CHK, K.size))
        B = np.exp(-1j * (WE[sl, None] * t[None, :] -
                          (K * C)[sl, None] * x[None, :])) * (chi * dt)[None, :]
        for j, w in enumerate(omegas):
            e = np.exp(-1j * w * tau)
            Fp[j] += np.sum(meas[sl] * np.abs(B @ e) ** 2)
            Fm[j] += np.sum(meas[sl] * np.abs(B @ e.conj()) ** 2)
    return Fp, Fm

om = np.concatenate([np.linspace(0.1, 4.0, 27), np.linspace(4.5, 12.0, 11)])

# measured excitation floor (inertial m=2, deep tail)
fp0, fm0 = F31(2.0, lambda s: 0 * s, 1.0, omegas=np.array([5.0]))
FLOOR = max(fp0[0], 1e-300)
print(f"measured excitation quadrature floor: {FLOOR:.1e}")

attacks = [
    ("m=0.5 LIGHT, burst v0=0.9 s=0.05, T=1",
     0.5, lambda s: 0.9 * np.exp(-s ** 2 / (2 * 0.05 ** 2)), 1.0, 0.0, 4.0, 1601, 130.0),
    ("m=2, SHARP burst v0=0.95 s=0.02, T=1",
     2.0, lambda s: 0.95 * np.exp(-s ** 2 / (2 * 0.02 ** 2)), 1.0, 0.0, 4.0, 3201, 150.0),
    ("m=2, CHIRP v=0.9 sin(6 tau + 4 tau^2), T=1",
     2.0, lambda s: 0.9 * np.sin(6 * s + 4 * s ** 2), 1.0, 0.0, 4.0, 2401, 130.0),
    ("m=2, burst v0=0.9 s=0.05, SHORT window T=0.3",
     2.0, lambda s: 0.9 * np.exp(-s ** 2 / (2 * 0.05 ** 2)), 0.3, 0.0, 2.0, 1601, 150.0),
    ("m=2, kick 0->0.9 s=0.05, OFF-CENTER window T=0.5 at tau0=+0.5",
     2.0, lambda s: 0.45 * (1 + np.tanh(s / 0.05)), 0.5, 0.5, 3.0, 1601, 150.0),
    ("m=1.2, RESONANT osc v0=0.9 Om=2.6, LONG window T=3",
     1.2, lambda s: 0.9 * np.sin(2.6 * s), 3.0, 0.0, 12.0, 2401, 60.0),
    ("m=3, osc v0=0.9 Om=6.5, T=2 (2-quantum Stokes tuning)",
     3.0, lambda s: 0.9 * np.sin(6.5 * s), 2.0, 0.0, 8.0, 2401, 90.0),
]

worst = -np.inf; worst_cfg = None
for name, mm, vf, T, tau0, hr, Nt, kmx in attacks:
    Fp, Fm = F31(mm, vf, T, tau0=tau0, half_range=hr, Ntau=Nt, kmax=kmx,
                 omegas=om)
    big = np.maximum(Fp, Fm) > 30 * FLOOR
    idx = (Fp[big] - Fm[big]) / np.maximum(Fp[big], Fm[big])
    iw = om[big][np.argmax(idx)]
    print(f"  {name:58s}: max idx = {idx.max(): .3e} (w={iw:5.2f})")
    if idx.max() > worst:
        worst = idx.max(); worst_cfg = name

print(f"\nOPEN-ATTACK global max inversion index: {worst: .3e}  [{worst_cfg}]")
if worst < 0:
    print("NO inversion found in any attack config outside the lane's grid:")
    print("light mass, sharp/fast bursts, chirps, short + off-center windows,")
    print("resonance-tuned oscillations. The lane's free-slice no-inversion")
    print("claim SURVIVES the extended scan (3+1 phase space suppresses the")
    print("lattice-style drive-Stokes gain: emission resonances are never")
    print("blocked in a continuum with k^2 dk measure).")
else:
    print("INVERSION FOUND outside the lane's grid -- the D1_3 'none")
    print("anywhere' claim is grid-limited. Classify (driven vs undriven!)")

print("\nVERIFIER CONCLUSION: KL positive-mixture reduction independently")
print("re-derived and numerically confirmed on a solvable interacting-class")
print("composite (no fitted constants); extended attack scan reported above.")
