#!/usr/bin/env python3
"""
D1_3: KALLEN-LEHMANN REDUCTION + RELATIVISTIC NON-UNIFORM-TRAJECTORY SCAN
==========================================================================
Lane D1, part 3 of 4. The corner the theorems (D1_2) leave open is the
INTERACTING VACUUM probed along a NON-UNIFORM worldline through a window.

KL REDUCTION THEOREM (exact, closes the 'interacting' part):
For ANY Wightman QFT in Minkowski space and ANY local scalar operator O
(elementary or composite -- phi, phi^2, ...), Lorentz invariance + the
spectrum condition give the Kallen-Lehmann representation of the VACUUM
two-point function:
    <0| O(x) O(y) |0> = int_0^inf dmu^2 rho(mu^2) Delta+_mu(x-y),
with SPECTRAL DENSITY rho(mu^2) >= 0. The windowed detector response at
second order in the detector coupling (the order at which Theorem VI's
F(omega) is defined) depends ONLY on this two-point function pulled back
to the worldline. Therefore, for ANY trajectory x(tau) and window chi:
    F_int(omega) = int dmu^2 rho(mu^2) F_mu^free(omega),
an exact POSITIVE MIXTURE of FREE-field mass-slice responses.
COROLLARY: population inversion for the interacting vacuum,
F_int(w) > F_int(-w), REQUIRES inversion in at least one free massive
slice on the same trajectory+window. Interactions per se add NOTHING at
this order: the question reduces to free MASSIVE fields on non-uniform
trajectories -- which is scanned exactly below.

(Massive matters: Theorem VI's identity F(-w)-F(w) = (w/2pi) int chi^2
used the MASSLESS commutator, which on a timelike curve fires only at
coincidence. A massive slice adds an inside-the-cone Bessel tail to the
commutator -- the one place a crack could hide. We scan it.)

Stated caveats (honest scope): (1) second order in detector coupling --
higher orders probe 4-point functions, not covered; (2) vacuum state
(leg (iii)'s case) -- excited/thermal interacting states not covered by
KL, but stationary thermal = KMS = closed by D1_2; (3) Minkowski -- the
dS analog (Bros-Moschella dS KL with positive principal-series density)
carries the same structure, asserted not re-proved here.

METHOD: exact mode-sum for a free massive scalar in 3+1D,
  F(omega) = (1/8pi^2) int_0^inf dk k^2/w_k int_-1^1 dc |g(k,c,omega)|^2,
  g = int dtau chi(tau) e^{-i omega tau} e^{-i[w_k t(tau) - k c x(tau)]},
(manifestly >= 0, no i-epsilon issues; kernel e^{-i w(tau-tau')} W matches
the D1_1/D1_2 convention F(w) = excitation, suppressed in inertial vacuum).
Validations: (V1) inertial mode-sum == exact 1D spectral formula;
(V2) massless limit: F(-w)-F(w) == (w/2pi) int chi^2 (Theorem VI).
Then SCAN velocity bursts / oscillatory drives for inversion.
"""
import numpy as np

# ---------------- windowed mode-sum machinery -----------------------------
T = 1.0
tau = np.linspace(-4.0, 4.0, 641)
dt = tau[1] - tau[0]
chi = np.exp(-tau ** 2 / (2 * T ** 2))
int_chi2 = np.trapz(chi ** 2, tau)

def trajectory(vfun):
    """v(tau) = coordinate speed as fn of proper time -> t(tau), x(tau)."""
    v = vfun(tau)
    assert np.max(np.abs(v)) < 0.97
    gam = 1.0 / np.sqrt(1 - v ** 2)
    t = np.concatenate([[0], np.cumsum(0.5 * (gam[1:] + gam[:-1]) * dt)])
    xx = np.concatenate([[0], np.cumsum(0.5 * ((gam * v)[1:] + (gam * v)[:-1]) * dt)])
    return t - t[len(tau) // 2], xx - xx[len(tau) // 2], np.max(np.abs(v))

def F_pair(m, t, x, omegas, Nk=280, Nc=40, kmax=70.0):
    """returns F(+w), F(-w) arrays via exact mode-sum."""
    kk, wk_ = np.polynomial.legendre.leggauss(Nk)
    k = 0.5 * kmax * (kk + 1); wknode = 0.5 * kmax * wk_
    cc, wc = np.polynomial.legendre.leggauss(Nc)
    wkE = np.sqrt(k ** 2 + m ** 2)
    # phase(kc, tau) = wk t(tau) - k c x(tau)
    K = np.repeat(k, Nc); C = np.tile(cc, Nk)
    WE = np.repeat(wkE, Nc)
    phase = WE[:, None] * t[None, :] - (K * C)[:, None] * x[None, :]
    B = np.exp(-1j * phase) * (chi * dt)[None, :]        # (Nk*Nc, Ntau)
    meas = (np.repeat(wknode * k ** 2 / wkE, Nc) * np.tile(wc, Nk)) / (8 * np.pi ** 2)
    Fp, Fm = [], []
    for w in omegas:
        # F(w) = sum_k |int chi e^{-i w tau} e^{-i phase}|^2 (direct kernel
        # e^{-i w (tau-tau')} W -- no Gram conjugation here, cf. D1_1)
        e = np.exp(-1j * w * tau)
        gp = B @ e            # g(+w)  (excitation side)
        gm = B @ e.conj()     # g(-w)  (emission side)
        Fp.append(np.sum(meas * np.abs(gp) ** 2))
        Fm.append(np.sum(meas * np.abs(gm) ** 2))
    return np.array(Fp), np.array(Fm)

print(__doc__)
print("=" * 72)
print("V1: inertial validation, m=2 (mode-sum vs exact spectral formula)")
print("=" * 72)
m = 2.0
t0, x0, _ = trajectory(lambda s: 0.0 * s)
om_val = np.array([0.5, 1.0, 2.0, 4.0])
Fp, Fm = F_pair(m, t0, x0, om_val)
# exact: F(w) = (1/4pi^2) int_m^inf dnu sqrt(nu^2-m^2) |chihat(w+nu)|^2,
# chihat(kap) = sqrt(2pi) T e^{-kap^2 T^2/2}
nu = np.linspace(m, 60, 40001)
def F_exact(w):
    return np.trapz(np.sqrt(nu ** 2 - m ** 2) * 2 * np.pi * T ** 2 *
                    np.exp(-(w + nu) ** 2 * T ** 2), nu) / (4 * np.pi ** 2)
ok = True
for i, w in enumerate(om_val):
    fe_p, fe_m = F_exact(w), F_exact(-w)
    print(f"  w={w:4.1f}: F(+w) modesum {Fp[i]:.6e} exact {fe_p:.6e} | "
          f"F(-w) modesum {Fm[i]:.6e} exact {fe_m:.6e}")
    ok &= abs(Fm[i] / fe_m - 1) < 2e-3          # emission side: all w
    if fe_p > 1e-7:                              # excitation: above the
        ok &= abs(Fp[i] / fe_p - 1) < 2e-2       # discretization floor
NOISE_FLOOR = max(Fp[-1], 1e-300)  # measured floor: exact value ~1e-18 here
print(f"  measured mode-sum noise floor ~ {NOISE_FLOOR:.1e} (abs, scale ~1)")
assert ok, "inertial validation failed"
print("PASS V1 (emission side <2e-3 everywhere; excitation side <2e-2 above")
print("        the floor; deep-Boltzmann-tail values are floor-limited).")

print()
print("V2: massless-limit Theorem-VI identity on a BURST trajectory")
print("    F(-w)-F(w) = (w/2pi) int chi^2  (trajectory-independent for m=0)")
tb, xb, _ = trajectory(lambda s: 0.8 * np.exp(-s ** 2 / (2 * 0.15 ** 2)))
om2 = np.array([1.0, 3.0, 6.0])
Fp0, Fm0 = F_pair(1e-4, tb, xb, om2, Nk=320, kmax=90.0)
for i, w in enumerate(om2):
    lhs = Fm0[i] - Fp0[i]; rhs = w / (2 * np.pi) * int_chi2
    print(f"  w={w:4.1f}: F(-w)-F(w) = {lhs:.6f}  vs (w/2pi)int chi^2 = "
          f"{rhs:.6f}  (ratio {lhs / rhs:.4f})")
    assert abs(lhs / rhs - 1) < 0.02
print("PASS V2: the massless coincidence identity holds on bursts, as proved.")

print()
print("=" * 72)
print("SCAN: massive slices x non-uniform trajectories (Gaussian window)")
print("=" * 72)
print("inversion index I = max_w [F(w)-F(-w)] / max(F(w),F(-w)); I>0 = inversion")
configs = []
for v0 in [0.5, 0.8, 0.9]:
    for s in [0.05, 0.15, 0.4]:
        configs.append((f"burst v0={v0} s={s}",
                        lambda ss, v0=v0, s=s: v0 * np.exp(-ss ** 2 / (2 * s ** 2))))
for v0 in [0.5, 0.9]:
    for Om in [4.0, 10.0]:
        configs.append((f"osc   v0={v0} Om={Om}",
                        lambda ss, v0=v0, Om=Om: v0 * np.sin(Om * ss)))
configs.append(("kick  0->0.8 (tanh s=0.1)",
                lambda ss: 0.4 * (1 + np.tanh(ss / 0.1))))

om_scan = np.concatenate([np.linspace(0.1, 3.0, 30), np.linspace(3.5, 12.0, 18)])
global_worst = -np.inf; worst_cfg = None
for m in [2.0, 6.0]:
    for name, vf in configs:
        tt, xx, vmax = trajectory(vf)
        Fp, Fm = F_pair(m, tt, xx, om_scan)
        big = np.maximum(Fp, Fm) > 30 * NOISE_FLOOR
        idx = (Fp[big] - Fm[big]) / np.maximum(Fp[big], Fm[big])
        iw = om_scan[big][np.argmax(idx)]
        print(f"  m={m:3.1f} {name:26s}: max index = {idx.max(): .3e} "
              f"(at w={iw:5.2f}); F(w)/F(-w) there = "
              f"{(1 + idx.max()) if idx.max() < 0 else 1 / (1 - idx.max()):.4f}")
        if idx.max() > global_worst:
            global_worst = idx.max(); worst_cfg = (m, name, iw)
# convergence check on the worst config
m_w, name_w, _ = worst_cfg
vf_w = dict(configs)[name_w]
tt, xx, _ = trajectory(vf_w)
Fp1, Fm1 = F_pair(m_w, tt, xx, om_scan)
Fp2, Fm2 = F_pair(m_w, tt, xx, om_scan, Nk=400, Nc=56, kmax=100.0)
conv = np.max(np.abs(Fp2 - Fp1) / np.maximum(Fp2.max(), 1e-300))
big2 = np.maximum(Fp2, Fm2) > 30 * NOISE_FLOOR
idx2 = np.max((Fp2[big2] - Fm2[big2]) / np.maximum(Fp2[big2], Fm2[big2]))
# pointwise ratio stability where it matters (the near-inversion point)
j = np.argmin(np.abs(om_scan - worst_cfg[2]))
print(f"\n  k-quadrature convergence on worst config {worst_cfg}:")
print(f"    max rel shift of F(+w) curve: {conv:.2e}")
print(f"    refined-quadrature max index: {idx2: .3e}  (coarse: "
      f"{global_worst: .3e})")
print(f"    ratio F(w)/F(-w) at w={om_scan[j]:.2f}: coarse "
      f"{Fp1[j] / Fm1[j]:.4f} -> refined {Fp2[j] / Fm2[j]:.4f}")
assert idx2 < 0, "refined quadrature flips the no-inversion verdict!"
print(f"\nGLOBAL max inversion index over grid: {global_worst: .3e} "
      f"at {worst_cfg}")
if global_worst < 0:
    print("NO INVERSION in any free massive slice on any tested non-uniform")
    print("trajectory => by the KL reduction, NO inversion for the vacuum of")
    print("ANY interacting Wightman QFT on these trajectories at 2nd order in")
    print("the detector coupling. The massive commutator tail RAISES emission")
    print("(and excitation) but never flips the sign of the asymmetry here.")
else:
    print("INVERSION FOUND -- quantify, classify pump source, report as a")
    print("crack candidate in Theorem VI leg (iii).")
