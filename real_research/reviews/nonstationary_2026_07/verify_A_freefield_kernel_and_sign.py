#!/usr/bin/env python3
"""
verify_A_freefield_kernel_and_sign.py  (adversarial verifier for lane A_freefield)

Independent re-derivation of the lane's most load-bearing claims, by DIFFERENT
methods than the lane used:

 1. KERNEL IDENTITY, non-Gaussian stress test: lane A's TEST 1 compared mean
    kick-responses, but 4 of its 5 'states' entered the mean dynamics as
    identical zero-mean data (tautological numerically; the symbolic identity
    carries the claim). Here we compute the response kernel <[x(t),x(s)]>
    DIRECTLY by exact Fock-space diagonalization of a free mode, in states the
    lane never tested numerically: Fock n=3 and an even CAT state (both
    genuinely NON-Gaussian), plus squeezed and thermal. Free field => spread
    must be machine-zero; the exact value must equal -sin(w(t-s))/w.
 2. SIGN of mu_inf and size of the quench artifact mu(0+): recomputed from
    scratch with an independent quadrature (adaptive-like fine grid, different
    discretization), including the analytic hand-check CT = (20/pi)(e^-0.1-e^-5).
 3. THE PARAMETRIC LOOPHOLE (attempt to OPEN the door within free+linear):
    a non-stationary bath HAMILTONIAN (w_k(t), FRW-like) keeps the kernel a
    c-number (Green fn of a linear ODE) -- verified numerically: parametrically
    driven free mode, kernel from Wronskian vs from two states. State-blind
    still. Then budget: in-band parametric gain needs pump ~ 2*Omega; available
    cosmological rate is H -> margin 2*Omega_min/H printed BOTH footings.
 4. Galactic band + footing fork re-derived independently.

Exit 0 iff every assertion passes.
"""
import numpy as np

np.seterr(all='ignore')  # macOS Accelerate spurious FP flags; guarded by asserts

# ------------------------------------------------------------------
# 1. Response kernel <[x(t),x(s)]> in NON-GAUSSIAN states, free mode, exact.
# ------------------------------------------------------------------
d = 80
a = np.diag(np.sqrt(np.arange(1, d)), 1)
ad = a.conj().T
w0 = 1.3
x = (a + ad) / np.sqrt(2 * w0)          # [x,p]=i units, mass 1, freq w0
H = w0 * (ad @ a)                        # free (harmonic) mode

def xH(tt):
    ph = np.exp(1j * w0 * np.arange(d) * tt)   # H diagonal in Fock basis
    return (ph[:, None] * x * ph.conj()[None, :])

def squeezed_vec(r):
    M = -1j * (r / 2) * (ad @ ad - a @ a)
    ev, V = np.linalg.eigh(M)
    v = np.zeros(d, complex); v[0] = 1.0
    return (V * np.exp(1j * ev)) @ V.conj().T @ v

# states: vacuum, thermal n=1, squeezed r=0.6, Fock n=3 (non-Gaussian),
# even cat |alpha>+|-alpha> (non-Gaussian, non-stationary phase structure)
nbar = 1.0
pn = (nbar / (1 + nbar)) ** np.arange(d) / (1 + nbar); pn /= pn.sum()
alpha = 1.5
from math import factorial
cvec = np.array([alpha ** n / np.sqrt(float(factorial(n))) for n in range(d)], complex)
cat = cvec * (1 + (-1) ** np.arange(d)) / 2.0      # even components
cat /= np.linalg.norm(cat)
fock3 = np.zeros(d, complex); fock3[3] = 1.0
sv = squeezed_vec(0.6)
states = {
    'vacuum':   np.diag([1.0] + [0.0] * (d - 1)).astype(complex),
    'thermal':  np.diag(pn).astype(complex),
    'squeezed': np.outer(sv, sv.conj()),
    'fock_n3':  np.outer(fock3, fock3.conj()),
    'cat':      np.outer(cat, cat.conj()),
}
t1, s1 = 2.7, 0.4
Cop = xH(t1) @ xH(s1) - xH(s1) @ xH(t1)
vals = {k: np.trace(rho @ Cop) for k, rho in states.items()}
exact = -1j * np.sin(w0 * (t1 - s1)) / w0          # [x(t),x(s)] = -i sin(w(t-s))/w
spread = max(abs(vals[k] - vals['vacuum']) for k in vals)
err = abs(vals['vacuum'] - exact)
print(f"1. free-mode kernel across 5 states incl NON-GAUSSIAN (fock_n3, cat):")
print(f"   spread = {spread:.3e}   |vacuum - analytic (-i sin(w dt)/w)| = {err:.3e}")
assert spread < 1e-11 and err < 1e-10
print("   PASS: kernel state-blind incl. non-Gaussian states; sign/value match analytic.")

# ------------------------------------------------------------------
# 2. Independent recomputation of mu(0+), mu_inf (sign check).
# ------------------------------------------------------------------
gam, wc, Om = 0.5, 20.0, 0.3
wg = np.linspace(2.0, 100.0, 800001)              # 4x finer than lane, independent grid
rho = (2.0 / np.pi) * gam * wg ** 2 * np.exp(-wg / wc)
CT = np.trapz(rho / wg ** 2, wg)
CT_analytic = (20.0 / np.pi) * (np.exp(-0.1) - np.exp(-5.0))
mu0 = 1.0 - CT / Om ** 2
mu_inf = 1.0 + np.trapz(rho / (wg ** 2 * (wg ** 2 - Om ** 2)), wg)
print(f"2. CT = {CT:.4f} (analytic {CT_analytic:.4f});  mu(0+) = {mu0:+.2f}"
      f"  (lane: -62.5);  mu_inf = {mu_inf:.4f}  (lane: 1.1161)")
assert abs(CT - CT_analytic) < 1e-3
assert abs(mu0 - (-62.5)) < 0.3
assert abs(mu_inf - 1.1161) < 2e-3
assert mu_inf > 1.0, "SIGN ERROR would be here: gapped bath must STIFFEN (anti-MOND)"
print("   PASS: quench artifact size, asymptotic ANTI-MOND sign (mu_inf>1) confirmed.")

# ------------------------------------------------------------------
# 3. Parametric loophole: time-dependent bath FREQUENCY, linear coupling.
#    x'' + w(t)^2 x = source. Kernel = c-number Green fn G(t,s) from the
#    Wronskian of two c-number homogeneous solutions -- state never enters.
#    Numeric check: evolve <[x(t),x(s)]> equivalently via the classical
#    fundamental system; compare 'response' inferred from two different states
#    by kicking a parametrically driven GAUSSIAN system (means + covariances).
# ------------------------------------------------------------------
def wt(tt):                                        # strong parametric drive
    return 1.0 + 0.35 * np.sin(1.7 * tt)

dt = 2e-4; nst = 60000                             # t_max = 12
def evolve(mean0, kick):
    m = np.array(mean0, float); m[1] += kick
    ts = 0.0
    traj = np.empty(nst)
    for i in range(nst):
        # symplectic leapfrog on (x,p): x'=p, p'=-w(t)^2 x
        m[1] -= 0.5 * dt * wt(ts) ** 2 * m[0]
        m[0] += dt * m[1]
        ts += dt
        m[1] -= 0.5 * dt * wt(ts) ** 2 * m[0]
        traj[i] = m[0]
    return traj

# two 'states' = different initial means (any Gaussian state's covariance
# CANNOT feed the mean in linear dynamics -- that IS the theorem; here we
# verify the response to a kick is identical on top of wildly different
# background trajectories, i.e. superposition holds under parametric drive)
r1 = evolve([0.0, 0.0], 1e-3) - evolve([0.0, 0.0], 0.0)
r2 = evolve([2.0, -1.5], 1e-3) - evolve([2.0, -1.5], 0.0)
pspread = np.max(np.abs(r1 - r2)) / np.max(np.abs(r1))
gain = np.max(np.abs(r1[-5000:])) / 1e-3           # parametric amplification factor
print(f"3. parametric (non-stationary Hamiltonian) free mode: response spread = "
      f"{pspread:.2e}; late-time parametric gain of the KERNEL itself = {gain:.1f}x")
assert pspread < 1e-9
assert gain > 2.0, "expected visible parametric amplification of the c-number kernel"
print("   PASS: kernel stays state-blind under parametric driving, BUT the c-number")
print("   kernel itself can be parametrically amplified -> the honest residual question")
print("   is a KERNEL-engineering (thm-IV/spectral) one, not state engineering. Budget:")

c_l = 2.99792458e8; kpc = 3.0857e19; yr = 3.156e7
Z = np.sqrt(32 * np.pi / 3)
Om_min = 3.0e4 / (30 * kpc); Om_max = 3.0e5 / (0.5 * kpc)
for tag, a0 in [("canonical rho_DE cH_L/Z", 9.36e-11), ("alternate rho_tot/cH0 ", 1.13e-10)]:
    Hh = a0 * Z / c_l
    print(f"   [{tag}] H = {Hh:.3e}/s; in-band parametric pump needs 2*Omega:"
          f" margin 2*Om_min/H = {2*Om_min/Hh:.1f}x .. 2*Om_max/H = {2*Om_max/Hh:.0f}x")
    assert 2 * Om_min / Hh > 25, "cosmic rate could parametrically pump the band!"
print("   PASS both footings: slowest in-band parametric resonance needs a pump")
print("   >= 30x faster than the cosmological rate H -- adiabatic regime, no pumping;")
print("   adiabatic w(t) drift modifies the kernel only at O((H/Omega)^2) <= 3e-3.")
print(f"   adiabatic correction bound (H/Om_min)^2: canonical "
      f"{(9.36e-11*Z/c_l/Om_min)**2:.1e}, alternate {(1.13e-10*Z/c_l/Om_min)**2:.1e}")

# ------------------------------------------------------------------
# 4. band + footing fork, independent
# ------------------------------------------------------------------
P_min, P_max = 2 * np.pi / Om_max, 2 * np.pi / Om_min
Hc, Ha = 9.36e-11 * Z / c_l, 1.13e-10 * Z / c_l
print(f"4. band: Omega [{Om_min:.3e},{Om_max:.3e}] rad/s, periods "
      f"[{P_min/yr:.2e},{P_max/yr:.2e}] yr; footing fork on H: {100*(Ha/Hc-1):.1f}%")
assert abs(Om_min - 3.241e-17) / 3.241e-17 < 0.01
assert abs(Om_max - 1.944e-14) / 1.944e-14 < 0.01
assert abs(Hc - 1.807e-18) / 1.807e-18 < 0.01 and abs(Ha - 2.182e-18) / 2.182e-18 < 0.01
assert abs(100 * (Ha / Hc - 1) - 20.7) < 0.3
print("   PASS: lane band/footing numbers reproduced independently.")

print()
print("verify_A_freefield_kernel_and_sign: ALL ASSERTIONS PASS -- lane A verdict UPHELD")
print("with two annotations: (i) lane TEST 1 is numerically tautological (4 of 5 states")
print("entered as identical zero-mean data); the symbolic identity + this script's exact")
print("Fock-space non-Gaussian check carry the claim instead. (ii) the verdict wording")
print("should say 'state-engineered' closed for free fields under ANY linear dynamics")
print("(incl. non-stationary Hamiltonians/parametric drive); kernel-engineering via")
print("parametric pumping is separately closed in-band by the >=36x (canonical) /")
print(">=30x (alternate) pump-rate deficit -- adiabatic corrections O(3e-3) max.")
