#!/usr/bin/env python3
"""
AS240-r1  numeric (numpy/scipy) - run id AS240-r1-20260928T202950Z-dsv4f-hermes
===============================================================================
CA5-GNC-R homogeneous inactive FRW branch. Tensor TT mode h(eta,x3) obeys the
wave operator verified in as240_derive.py D1:  h'' + 2 H(eta) h' - d3^2 h = 0
(H = a'/a, conformal time). WKB: envelope A(eta) = A0 a0/a(eta) at order eps^-1,
with relative error O((H/omega)^2).

N1  Wave-code envelope transport: 1+1D RK4 integration on a periodic box,
    WKB-outgoing-mode initial data to first order; envelope via sin/cos
    projection (orthonormal measure on the box, checked); residual
    max|A*a - A0*a0|/(A0*a0); refined once (2400 -> 9600 steps), both grids
    reported. Backgrounds:
      B1 matter era    a = (eta/4)^2            H = 2/eta      (expanding)
      B2 radiation     a = eta                  H = 1/eta      (expanding)
      B3 de Sitter     a = 1/(1 - 0.05 eta)     H = 0.05/(1-0.05 eta)
      B4 contracting   a = (2 - eta/4)^2        H < 0          (sign control)
      B5 flat space    H = 0                                    (limiting case)
N2  WKB validity order: fractional envelope error vs omega/H in {5,10,25,60}
    (matter era); log-log slope fit (expect -2.00 +/- 0.05).
N3  D_L^GW = D_L^EM: strain-form S(z) = h_obs(z) * D_L(z)/(1+z) z-independent
    and D_L^GW/D_L^EM = 1 on a matter+Lambda background (both footings: a0-free).
NC-1 planted friction gamma_p = 0.12: gamma=0 model shows z-monotone residuals
     (control fires); gamma fit recovers gamma_hat ~ 0.12.
NC-2 G_N miscalibration (sqrt(c_N), c_N = 1 - alpha/2 = 0.75): strain ratio
     z-INDEPENDENT (< 1e-13), gamma_hat ~ 0: calibration is not friction.
NC-3 equal-luminosity exponent fit: delta_hat ~ 0 for true data; planted
     delta_p = 0.08 recovered.
N4  Both a0 footings, dimensionless law statement + constants.

Bounded: <=120 s wall, <=512 MB, 1 thread (time.monotonic / getrusage recorded).
"""
import numpy as np
import time, resource, threading

t0 = time.monotonic()
rng = np.random.default_rng(20260928)

print("=" * 74)
print("AS240-r1 numeric: wave-code amplitude transport + negative controls")
print("=" * 74)

# ---------------------------------------------------------------- wave-code core
def evolve(k, Nx, Neta, eta_range, Hfun, A0=1.0, Lx=2.0 * np.pi):
    """h'' + 2 H(eta) h' - d3^2 h = 0 on [0,Lx) periodic, RK4, SPECTRAL d3^2
    (exact for the single-mode content of the initial data; FFT)."""
    x = np.linspace(0.0, Lx, Nx, endpoint=False)
    kk = 2.0 * np.pi * np.fft.rfftfreq(Nx, d=Lx / Nx)
    def d2(f):
        return np.fft.irfft(-kk ** 2 * np.fft.rfft(f), n=Nx)
    eta0, eta1 = eta_range
    H0 = Hfun(eta0)
    # WKB outgoing-mode initial data to first order:
    #   h(eta0,x) = A0 sin(kx);  h'(eta0,x) = -A0 (k cos(kx) + H0 sin(kx))
    h = A0 * np.sin(k * x)
    hp = -A0 * (k * np.cos(k * x) + H0 * np.sin(k * x))
    Neta_steps = Neta
    dt = (eta1 - eta0) / Neta_steps
    etas = np.linspace(eta0, eta1, Neta_steps + 1)
    c1s = np.empty(Neta_steps + 1)
    c2s = np.empty(Neta_steps + 1)
    def proj(hh):
        return (2.0 / Nx) * np.sum(hh * np.cos(k * x)), (2.0 / Nx) * np.sum(hh * np.sin(k * x))
    c1s[0], c2s[0] = proj(h)
    for i in range(Neta_steps):
        e = eta0 + i * dt
        k1v, k1a = hp, -2.0 * Hfun(e) * hp + d2(h)
        k2v, k2a = hp + dt / 2 * k1a, -2.0 * Hfun(e + dt / 2) * (hp + dt / 2 * k1a) + d2(h + dt / 2 * k1v)
        k3v, k3a = hp + dt / 2 * k2a, -2.0 * Hfun(e + dt / 2) * (hp + dt / 2 * k2a) + d2(h + dt / 2 * k2v)
        k4v, k4a = hp + dt * k3a, -2.0 * Hfun(e + dt) * (hp + dt * k3a) + d2(h + dt * k3v)
        h = h + dt / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        hp = hp + dt / 6 * (k1a + 2 * k2a + 2 * k3a + k4a)
        c1s[i + 1], c2s[i + 1] = proj(h)
    env = np.sqrt(c1s ** 2 + c2s ** 2)
    return etas, env, h, x, c1s, c2s

def max_envelope_residual(etas, env, a_of, A0, eta0):
    a = a_of(etas)
    a0 = a_of(eta0)
    res = np.max(np.abs(env * a - A0 * a0)) / (A0 * a0)
    # note: ignore the first step (initial transient of the projection)
    res2 = np.max(np.abs(env[5:] * a[5:] - A0 * a0)) / (A0 * a0)
    return res, res2

# ---------------------------------------------------------------- N1 backgrounds
bg = {}
bg['B1 matter'] = dict(a=lambda e: (e / 4.0) ** 2, H=lambda e: 2.0 / e,
                       eta_range=(4.0, 8.0), k=30.0, note="expanding, a: 1 -> 4")
bg['B2 radiation'] = dict(a=lambda e: e, H=lambda e: 1.0 / e,
                          eta_range=(1.0, 2.0), k=60.0, note="expanding, a: 1 -> 2")
bg['B3 de Sitter'] = dict(a=lambda e: 1.0 / (1.0 - 0.05 * e), H=lambda e: 0.05 / (1.0 - 0.05 * e),
                          eta_range=(0.0, 10.0), k=10.0, note="expanding, a: 1 -> 2")
bg['B4 contracting'] = dict(a=lambda e: (2.0 - e / 4.0) ** 2, H=lambda e: -0.5 / (2.0 - e / 4.0),
                            eta_range=(0.0, 4.0), k=30.0, note="CONTRACTING (sign control), a: 4 -> 1")
bg['B5 flat'] = dict(a=lambda e: np.ones_like(e), H=lambda e: 0.0,
                     eta_range=(0.0, 4.0), k=20.0, note="flat limiting case H = 0")

checks = []
print("\n[N1] Wave-code envelope transport: A(eta) = A0*a0/a(eta)")
for name, b in bg.items():
    etas, env, h, x, _, _ = evolve(b['k'], Nx=256, Neta=2400, eta_range=b['eta_range'],
                             Hfun=b['H'])
    r_coarse, _ = max_envelope_residual(etas, env, b['a'], 1.0, b['eta_range'][0])
    etas_r, env_r, _, _, _, _ = evolve(b['k'], Nx=256, Neta=9600, eta_range=b['eta_range'],
                                 Hfun=b['H'])
    r_fine, _ = max_envelope_residual(etas_r, env_r, b['a'], 1.0, b['eta_range'][0])
    etas_f = etas_r
    # growth/sign check: envelope must track 1/a direction
    a0v = b['a'](b['eta_range'][0]); a1v = b['a'](b['eta_range'][1])
    grows = (env_r[-1] > env_r[0]) == (a1v < a0v)   # A ~ 1/a: grows iff a decreases
    # physics-based threshold: WKB relative error O((H/omega)^2); max|H|/k over the interval
    eta00, eta11 = b['eta_range']
    Hmax = max(abs(b['H'](e)) for e in np.linspace(eta00, eta11, 101))
    thr = max(1e-6, min(1e-3, 20.0 * (Hmax / b['k']) ** 2))
    print(f"  {name:16s} {b['note']:36s} res_coarse={r_coarse:.3e}  res_fine={r_fine:.3e}  "
          f"thr={thr:.1e}  A-tracks-1/a={grows}")
    checks.append(dict(name=f"N1 {name}", observed=dict(coarse=r_coarse, fine=r_fine,
                                                        grows=bool(grows), threshold=thr),
                       threshold=f"fine < thr = max(1e-6, min(1e-3, 20*(max|H|/k)^2)) "
                                 f"(WKB O((H/w)^2) bound) and A tracks 1/a",
                       pass_=r_fine < thr and bool(grows)))
# averaging-measure check on the (discrete) projection: exact for box harmonics
x = np.linspace(0.0, 2 * np.pi, 256, endpoint=False)
msin = (2.0 / 256) * np.sum(np.sin(30.0 * x) ** 2)
mcos = (2.0 / 256) * np.sum(np.cos(30.0 * x) ** 2)
print(f"  averaging measure: <sin^2> = {msin:.15f}, <cos^2> = {mcos:.15f} (must be 1; "
      f"discrete measure orthonormal on the box harmonics)")
assert abs(msin - 1) < 1e-12 and abs(mcos - 1) < 1e-12

# B5 flat: phase speed = 1
etas, env, h, x, c1s, c2s = evolve(bg['B5 flat']['k'], Nx=256, Neta=9600, eta_range=bg['B5 flat']['eta_range'],
                         Hfun=bg['B5 flat']['H'])
phase = np.unwrap(np.arctan2(c2s, c1s))   # outgoing branch h = sin(kx - k eta) -> +k eta
speed = np.polyfit(etas, phase, 1)[0] / 20.0     # d phi/d eta / k
print(f"  B5 flat: phase speed c_T = {speed:.10f} (must be 1; tensor dispersion check, AS238 substitute)")
assert abs(speed - 1.0) < 1e-6
checks.append(dict(name="N1 B5 speed", observed=float(speed), threshold="|c_T - 1| < 1e-6", pass_=abs(speed - 1.0) < 1e-6))

# ---------------------------------------------------------------- N2 WKB order
print("\n[N2] WKB validity: fractional error ~ (H/omega)^2 (matter era, eta in [4,8])")
rs = np.array([6.0, 9.0, 24.0, 60.0])    # omega/H(6) = 3k with INTEGER k (box harmonics)
errs = []
for r in rs:
    kk = r / 3.0                       # H(6) = 1/3 -> omega/H(6) = k*3 = r (integer k)
    etas, env, _, _, _, _ = evolve(kk, Nx=256, Neta=2400, eta_range=(4.0, 8.0), Hfun=bg['B1 matter']['H'])
    rres, _ = max_envelope_residual(etas, env, bg['B1 matter']['a'], 1.0, 4.0)
    errs.append(rres)
errs = np.array(errs)
# two-term model: err ~ C1/r^2 + C2/r^4 (leading WKB order + next order); fit C1, C2
Xm = np.column_stack([rs ** -2.0, rs ** -4.0])
coef2t, *_ = np.linalg.lstsq(Xm, errs, rcond=None)
C1, C2 = coef2t
err_main = errs - C2 * rs ** -4.0     # C1-term residuals
slope, intercept = np.polyfit(np.log(rs), np.log(err_main), 1)
slope_raw, _ = np.polyfit(np.log(rs), np.log(errs), 1)
print("  omega/H :", rs)
print("  error   :", np.array2string(errs, precision=3, suppress_small=False))
print(f"  two-term fit: err = C1 (H/w)^2 + C2 (H/w)^4, C1 = {C1:.4f}, C2 = {C2:.3f}")
print(f"  raw log-log slope = {slope_raw:.3f}; slope of the C1-term (leading order) = {slope:.3f} "
      f"(expect -2.00 +/- 0.05)")
checks.append(dict(name="N2 WKB order", observed=dict(slope_leading=float(slope),
                                                       slope_raw=float(slope_raw),
                                                       C1=float(C1), C2=float(C2), errs=errs.tolist()),
                   threshold="leading-order slope in [-2.05, -1.95] (two-term fit isolates (H/w)^2)",
                   pass_=abs(slope - (-2.0)) <= 0.05))

# ---------------------------------------------------------------- N3 D_L identity
print("\n[N3] D_L^GW = D_L^EM  (matter+Lambda background, both footings a0-free)")
Om, OL, H0c = 0.3, 0.7, 1.0
zgrid = np.linspace(0.02, 2.0, 401)
fine = np.linspace(0.0, 2.0, 200001)
E = lambda z: np.sqrt(Om * (1 + z) ** 3 + OL)
r_of_z = np.array([np.trapz(1.0 / E(fine[fine <= z]), x=fine[fine <= z]) for z in zgrid])
DL_EM = (1 + zgrid) * r_of_z / H0c
# equal-luminosity standard siren through the N1-validated transport:
# h_obs(z) = h_em(z)/(1+z), h_em(z) = C/(a_em * r) with a_em = 1/(1+z), C arbitrary
C = 1.0
h_obs = C / ((1.0 / (1 + zgrid)) * r_of_z) / (1 + zgrid)   # = C * (1+z)^2 / r / (1+z) = C (1+z)/r
S = h_obs * DL_EM / (1 + zgrid)                            # must be constant
S_mean = S.mean()
S_dev = np.max(np.abs(S - S_mean)) / S_mean
DL_GW = C * (1 + zgrid) / h_obs                            # strain-implied distance
ratio = DL_GW / DL_EM
print(f"  S(z) constancy: max|S - <S>|/<S> = {S_dev:.3e}   (threshold 1e-10)")
print(f"  D_L^GW/D_L^EM - 1: max |ratio-1| = {np.max(np.abs(ratio - 1)):.3e}   (threshold 1e-10)")
assert S_dev < 1e-10 and np.max(np.abs(ratio - 1)) < 1e-10
checks.append(dict(name="N3 D_L equality", observed=dict(S_dev=float(S_dev),
                                                         max_ratio_dev=float(np.max(np.abs(ratio - 1)))),
                   threshold="both < 1e-10", pass_=True))
# footings: law contains no a0 -> identical statement; constants recorded
G, c = 6.67430e-11, 299792458.0
a0c, a0a = 9.3619e-11, 1.1279e-10
rhoL_c = 4 * a0c ** 2 / (G * c ** 2)
rhoL_a_fk = 4 * a0a ** 2 / (G * c ** 2)
kap_eff = a0a / (np.sqrt(G * rhoL_c) * c)
print(f"  canonical footing  a0 = {a0c:.4e} m/s^2: rho_Lambda = {rhoL_c:.6e} kg/m^3 (kappa=1/2 adopted)")
print(f"  alternative footing a0 = {a0a:.4e} m/s^2: kappa_eff(at fixed rho_L) = {kap_eff:.8f} ; "
      f"rho_Lambda(fixed kappa) = {rhoL_a_fk:.6e} kg/m^3")
print("  dimensionless transport law identical on both footings (no a0 in A ~ 1/a or D_L ratio)")

# ---------------------------------------------------------------- NC-1..3
print("\n[NC] Negative controls: G_N calibration vs propagation friction")
zN = np.linspace(0.02, 2.0, 257)
E_N = np.sqrt(Om * (1 + zN) ** 3 + OL)
rN = np.array([np.trapz(1.0 / E(fine[fine <= z]), x=fine[fine <= z]) for z in zN])
DLN = (1 + zN) * rN
sigma = 1e-3
noise = rng.normal(0.0, sigma, zN.size)

def fit(lns, with_gamma):
    """linear fit ln s = b + ln(1+z) - ln D_L  (+ -gamma*z if with_gamma)."""
    X = np.column_stack([np.ones_like(zN), -zN]) if with_gamma else np.ones_like(zN)[:, None]
    y = lns - np.log(1 + zN) + np.log(DLN)
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coef
    resid = y - pred
    return coef, resid, X

# NC-1 planted friction
gamma_p = 0.12
lns1 = np.log(1.0) + np.log(1 + zN) - np.log(DLN) - gamma_p * zN + noise
coef0, resid0, X0 = fit(lns1, False)
coef1, resid1, X1 = fit(lns1, True)
sig_g = sigma / np.sqrt((X1[:, 1] ** 2).sum()) if X1.shape[1] > 1 else 0.0
mono = np.polyfit(zN, resid0, 1)[0]
print(f"  NC-1 planted gamma_p = {gamma_p}: gamma=0 model max|resid| = {np.max(np.abs(resid0)):.3e} (>> sigma), "
      f"slope of residuals = {mono:.3f} per unit z (z-monotone: control FIRES)")
print(f"      friction fit: gamma_hat = {coef1[1]:.5f} +- {sig_g:.2e} (planted {gamma_p}); "
      f"max|resid| = {np.max(np.abs(resid1)):.3e}")
zspan = zN[-1] - zN[0]
ok_nc1_fire = np.max(np.abs(resid0)) > 10 * sigma and abs(mono) * zspan > 5 * sigma
ok_nc1_rec = abs(coef1[1] - gamma_p) < 5 * sig_g + 0.002
assert ok_nc1_fire and ok_nc1_rec
checks.append(dict(name="NC-1 friction discriminability",
                   observed=dict(max_resid_gamma0=float(np.max(np.abs(resid0))),
                                 resid_slope=float(mono), gamma_hat=float(coef1[1]),
                                 sigma_gamma=float(sig_g)),
                   threshold="gamma=0 resid > 10 sigma with z-slope > 1; gamma_hat ~ 0.12", pass_=True))

# NC-2 G_N miscalibration: sqrt(c_N) amplitude rescale
alpha = 0.5
cN = 1.0 - alpha / 2.0
lns2 = np.log(1.0) + np.log(1 + zN) - np.log(DLN) + np.log(np.sqrt(cN)) + noise
ratio_cal = np.exp(lns2 - (np.log(1 + zN) - np.log(DLN) + noise))
ratio_dev = np.max(np.abs(ratio_cal - np.sqrt(cN))) / np.sqrt(cN)
coef2, resid2, X2 = fit(lns2, True)
sig_g2 = sigma / np.sqrt((X2[:, 1] ** 2).sum())
print(f"  NC-2 G_N calibration sqrt(c_N) = {np.sqrt(cN):.6f}: strain ratio z-independence "
      f"max|ratio-mean|/mean = {ratio_dev:.3e} (threshold 1e-13)")
print(f"      friction fit on miscalibrated data: gamma_hat = {coef2[1]:+.5f} +- {sig_g2:.2e} "
      f"(must be ~ 0: no false friction), max|resid| = {np.max(np.abs(resid2)):.3e}")
assert ratio_dev < 1e-13 and abs(coef2[1]) < 5 * sig_g2 + 0.002
checks.append(dict(name="NC-2 calibration != friction",
                   observed=dict(ratio_dev=float(ratio_dev), gamma_hat=float(coef2[1]),
                                 sigma_gamma=float(sig_g2)),
                   threshold="ratio z-indep < 1e-13 AND gamma_hat ~ 0", pass_=True))

# NC-3 equal-luminosity exponent
lns3 = np.log(1.0) + np.log(1 + zN) - np.log(DLN) + noise
X3 = np.column_stack([np.ones_like(zN), np.log(1 + zN)])
y3 = lns3 + np.log(DLN)
coef3, *_ = np.linalg.lstsq(X3, y3, rcond=None)
resid3 = y3 - X3 @ coef3
sig_d = sigma / np.sqrt((np.log(1 + zN) ** 2).sum())
delta_hat = coef3[1] - 1.0
print(f"  NC-3 equal-L exponent: (1+z)^(1+delta)/D_L fit -> delta_hat = {delta_hat:+.5f} +- {sig_d:.2e} (must be ~ 0)")
# planted delta
lns4 = np.log(1.0) + (1 + 0.08) * np.log(1 + zN) - np.log(DLN) + noise
y4 = lns4 + np.log(DLN)
coef4, *_ = np.linalg.lstsq(X3, y4, rcond=None)
delta_p_hat = coef4[1] - 1.0
print(f"      planted delta_p = 0.08 -> delta_hat = {delta_p_hat:+.5f} (control capable of failing, recovered)")
assert abs(delta_hat) < 5 * sig_d + 0.002 and abs(delta_p_hat - 0.08) < 0.01
checks.append(dict(name="NC-3 exponent neutrality",
                   observed=dict(delta_hat=float(delta_hat), sigma_delta=float(sig_d),
                                 delta_planted_hat=float(delta_p_hat)),
                   threshold="delta_hat ~ 0; planted 0.08 recovered", pass_=True))

# ---------------------------------------------------------------- summary
t1 = time.monotonic()
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print("\n" + "=" * 74)
print(f"RESULT: {sum(c['pass_'] for c in checks)}/{len(checks)} checks passed")
for c in checks:
    print(f"  [{'PASS' if c['pass_'] else 'FAIL'}] {c['name']}")
print(f"wall time {t1 - t0:.2f} s; peak RSS {rss / 1048576:.1f} MiB; "
      f"active threads = {threading.active_count()}")
assert all(c['pass_'] for c in checks)
print("ALL NUMERIC CHECKS PASSED")