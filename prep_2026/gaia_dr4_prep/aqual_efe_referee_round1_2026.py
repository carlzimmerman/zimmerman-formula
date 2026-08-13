#!/usr/bin/env python3
"""Adversarial referee checks for aqual_efe_full_solve_2026.py (scratch, independent).

R1  closed-form linear tensors (independent hand derivation):
      AQUAL : B_par = nu0,  B_perp = nu0*sqrt(1+Lnu)   [= nu0/sqrt(1+L0)]
      QUMOND: B_par = nu0,  B_perp = nu0*(1+Lnu/2), sphere-avg = nu0*(1+Lnu/3) = (dxdy+2nu0)/3
R2  FFT solve of the linearized anisotropic operator mu0[lap + L0 dz^2]phi = 4pi delta
      -> radial boost vs nu0/sqrt(1+L0 sin^2 th) at three angles.
R3  independent QUMOND check: direct 3D quadrature of the phantom source with the Coulomb
      kernel at transition + saturated radii vs a verbatim copy of the harmonic solver.
R4  AQUAL nonlinear Gauss-law flux: integral of mu(|g|) g . dA over spheres must be -4 pi G M
      at EVERY radius (transition included) -- not explicitly enforced by the Picard scheme.
R5  Picard tail: +150 extra iterations from the converged state; drift of B at transition radii.
R6  x = y nu(y) inversion: monotonicity, round trip, L0 formula vs numerical dln mu/dln x.
"""
import numpy as np

# ---------- verbatim kernel + solver machinery (copied from the target script) ----------
def nu(y):
    y = np.asarray(y, dtype=float)
    s = np.sqrt(np.maximum(y, 1e-300))
    return 1.0 / (1.0 - np.exp(-s))

def dnu_dy(y):
    y = np.asarray(y, dtype=float)
    s = np.sqrt(np.maximum(y, 1e-300))
    u = 1.0 - np.exp(-s)
    du = np.exp(-s) / (2.0 * s)
    return -du / u**2

_YT = np.logspace(-10, 10, 40001)
_XT = _YT * nu(_YT)
assert np.all(np.diff(_XT) > 0)

def y_of_x(x):
    return np.exp(np.interp(np.log(np.asarray(x, float)), np.log(_XT), np.log(_YT)))

def mu_of_x(x):
    return y_of_x(x) / np.asarray(x, float)

NR, NTH, LMAX = 1600, 192, 48
RMIN, RMAX = 1e-3, 3e4
r = np.logspace(np.log10(RMIN), np.log10(RMAX), NR)
lnr = np.log(r)
u_gl, w_gl = np.polynomial.legendre.leggauss(NTH)
sin_th = np.sqrt(1.0 - u_gl**2)
P = np.zeros((LMAX + 1, NTH)); P[0] = 1.0; P[1] = u_gl
for l in range(1, LMAX):
    P[l + 1] = ((2 * l + 1) * u_gl * P[l] - l * P[l - 1]) / (l + 1)
dP = np.zeros_like(P)
for l in range(1, LMAX + 1):
    dP[l] = l * (u_gl * P[l] - P[l - 1]) / (u_gl**2 - 1.0)

def project_l(S):
    return np.einsum("lt,t,rt->lr", P, w_gl, S) * (np.arange(LMAX + 1) + 0.5)[:, None]

def poisson_harmonic(S):
    Sl = project_l(S)
    Phi_l = np.zeros_like(Sl)
    dPhi_l = np.zeros_like(Sl)
    for l in range(LMAX + 1):
        f_in = Sl[l] * r**(l + 3)
        f_out = Sl[l] * r**(2 - l)
        I_in = np.concatenate([[0.0], np.cumsum(0.5 * (f_in[1:] + f_in[:-1]) * np.diff(lnr))])
        c_out = np.concatenate([[0.0], np.cumsum(0.5 * (f_out[1:] + f_out[:-1]) * np.diff(lnr))])
        I_out = c_out[-1] - c_out
        Phi_l[l] = -(I_in / r**(l + 1) + I_out * r**l) / (2 * l + 1)
        dPhi_l[l] = -(-(l + 1) * I_in / r**(l + 2) + l * r**(l - 1) * I_out) / (2 * l + 1)
    Phi = np.einsum("lr,lt->rt", Phi_l, P)
    dPhi_dr = np.einsum("lr,lt->rt", dPhi_l, P)
    dPhi_dth_over_r = np.einsum("lr,lt,t->rt", Phi_l, dP, -sin_th) / r[:, None]
    return Phi, dPhi_dr, dPhi_dth_over_r

R2g = r[:, None] ** 2

def gN_components(ge):
    gr = ge * u_gl[None, :] - 1.0 / R2g
    gt = -ge * sin_th[None, :] + np.zeros_like(R2g)
    return gr, gt

def qumond_source(ge):
    gr, gt = gN_components(ge)
    gmag = np.hypot(gr, gt)
    d_dr = (-4.0 / r[:, None] ** 5 + 4.0 * ge * u_gl[None, :] / r[:, None] ** 3) / (2.0 * gmag)
    d_dth_over_r = (2.0 * ge * sin_th[None, :] / R2g) / (2.0 * gmag * r[:, None])
    return -dnu_dy(gmag) * (gr * d_dr + gt * d_dth_over_r)

def solve_qumond(ge):
    S = qumond_source(ge)
    _, dPr, dPt = poisson_harmonic(S)
    g_r_star = -1.0 / R2g - dPr
    g_t_star = -dPt
    return g_r_star, g_t_star

def solve_aqual(ge, n_iter=220, relax=0.55, tol=1e-9, chi0=None):
    x_e = ge * float(nu(ge))
    if chi0 is None:
        g_r_star, g_t_star = solve_qumond(ge)
        chi_r = g_r_star + 1.0 / R2g
        chi_t = g_t_star.copy()
    else:
        chi_r, chi_t = chi0[0].copy(), chi0[1].copy()
    w_bg = 1.0 - mu_of_x(x_e)
    Wr_bg = w_bg * x_e * u_gl[None, :] + np.zeros_like(R2g)
    Wt_bg = -w_bg * x_e * sin_th[None, :] + np.zeros_like(R2g)
    conv = np.inf
    for it in range(n_iter):
        Gr = x_e * u_gl[None, :] - 1.0 / R2g + chi_r
        Gt = -x_e * sin_th[None, :] + chi_t
        gmag = np.hypot(Gr, Gt)
        w = 1.0 - mu_of_x(np.maximum(gmag, 1e-14))
        Wr, Wt = w * Gr - Wr_bg, w * Gt - Wt_bg
        dr_term = np.gradient(R2g * Wr, lnr, axis=0) / (R2g * r[:, None])
        dth_term = -np.gradient(sin_th[None, :] * Wt * np.ones_like(R2g), u_gl, axis=1) / r[:, None]
        T = dr_term + dth_term
        _, dPr, dPt = poisson_harmonic(T)
        dconv = max(np.max(np.abs(dPr - chi_r)) / (np.max(np.abs(chi_r)) + 1e-30),
                    np.max(np.abs(dPt - chi_t)) / (np.max(np.abs(chi_t)) + 1e-30))
        chi_r = (1 - relax) * chi_r + relax * dPr
        chi_t = (1 - relax) * chi_t + relax * dPt
        conv = dconv
        if conv < tol:
            break
    g_r_star = -1.0 / R2g + chi_r
    g_t_star = chi_t
    return g_r_star, g_t_star, conv, it + 1, (chi_r, chi_t)

# ---------- R1: closed-form linear tensors ----------
print("=" * 90)
YE = float(y_of_x(1.9))          # canonical closure inversion (script's Y_EXT)
n0 = float(nu(YE))
dxdy = float(n0 + YE * dnu_dy(YE))
L0 = n0 / dxdy - 1.0
Lnu = YE * float(dnu_dy(YE)) / n0
print(f"R1  yE={YE:.5f} nu0={n0:.5f} dxdy={dxdy:.5f} L0={L0:.5f} Lnu={Lnu:.5f}")
print(f"    identity L0 = -Lnu/(1+Lnu): {L0:.6f} vs {-Lnu/(1+Lnu):.6f}")
aq_par, aq_perp = n0, n0 * np.sqrt(1 + Lnu)
qu_par, qu_perp = n0, n0 * (1 + Lnu / 2)
qu_avg = n0 * (1 + Lnu / 3)
print(f"    AQUAL analytic  par {aq_par:.4f} perp {aq_perp:.4f}  (script analytic 1.4732/1.2598)")
print(f"    QUMOND analytic par {qu_par:.4f} perp {qu_perp:.4f} sphavg {qu_avg:.4f}"
      f"  [identity (dxdy+2nu0)/3 = {(dxdy + 2 * n0) / 3:.4f}]  (solver log 1.4717/1.2753/1.3413)")
# AQUAL sphere-avg closed form: nu0/sqrt(L0) * arcsin(sqrt(L0/(1+L0)))
aq_avg = n0 / np.sqrt(L0) * np.arcsin(np.sqrt(L0 / (1 + L0)))
print(f"    AQUAL analytic sphere-avg {aq_avg:.4f}  (solver log 1.3251)")

# ---------- R2: FFT linear anisotropic Green's function ----------
print("=" * 90)
Nf, Lbox = 256, 24.0
dx = Lbox / Nf
k1 = 2 * np.pi * np.fft.fftfreq(Nf, d=dx)
kx = k1[:, None, None]; ky = k1[None, :, None]; kz = k1[None, None, :]
k2a = kx**2 + ky**2 + (1 + L0) * kz**2
k2a[0, 0, 0] = 1.0
mu0 = 1.0 / n0
rho_k = np.ones((Nf, Nf, Nf)) / dx**3 * 0  # placeholder
# delta at origin node: FT of delta = 1 (density units)  => phi_k = -4pi/(mu0*k2a) * 1
phi_k = -4 * np.pi / (mu0 * k2a)
phi_k[0, 0, 0] = 0.0
gz = np.real(np.fft.ifftn(-1j * kz * phi_k)) / dx**3 * dx**3  # -d(phi)/dz... build force = -grad phi
# force components: F = -grad phi -> F_k = -ik phi_k ; inverse FFT (note ifftn includes 1/N^3; the
# delta amplitude 1/dx^3 in density * dx^3 volume factor cancels: source integral = 1)
Fz = np.real(np.fft.ifftn(-1j * kz * phi_k)) / dx**3
Fx = np.real(np.fft.ifftn(-1j * kx * phi_k)) / dx**3
for (ix, iy, iz, lab) in [(0, 0, 16, "par(theta=0)"), (16, 0, 0, "perp(theta=90)"),
                          (12, 0, 12, "theta=45"), (0, 0, 24, "par r=2.25"), (24, 0, 0, "perp r=2.25")]:
    x0 = np.array([ix * dx, iy * dx, iz * dx])
    r0 = np.linalg.norm(x0)
    F = np.array([Fx[ix, iy, iz], 0.0, Fz[ix, iy, iz]])
    # boost = force magnitude toward origin / (1/r0^2); radial component:
    Br = -np.dot(F, x0 / r0) * r0**2
    st2 = (x0[0]**2) / r0**2
    pred = n0 / np.sqrt(1 + L0 * st2)
    print(f"R2  FFT linear boost {lab:15s} r={r0:5.2f}  B={Br:.4f}  analytic={pred:.4f} "
          f" ratio={Br / pred:.4f}")

# ---------- solve QUMOND + AQUAL once (canonical) ----------
print("=" * 90)
gq_r, gq_t = solve_qumond(YE)
Bq = -gq_r * R2g
ga_r, ga_t, cv, itn, chi = solve_aqual(YE)
Ba = -ga_r * R2g
i300 = np.argmin(np.abs(r - 300.0))
print(f"solved: AQUAL conv {cv:.2e} in {itn} iters")
print(f"  sat axes AQUAL  par {Ba[i300, np.argmax(u_gl)]:.4f} perp {Ba[i300, np.argmin(np.abs(u_gl))]:.4f}"
      f"  sphavg {0.5 * np.dot(Ba[i300], w_gl):.4f}")
print(f"  sat axes QUMOND par {Bq[i300, np.argmax(u_gl)]:.4f} perp {Bq[i300, np.argmin(np.abs(u_gl))]:.4f}"
      f"  sphavg {0.5 * np.dot(Bq[i300], w_gl):.4f}")

# ---------- R3: independent QUMOND direct quadrature ----------
print("=" * 90)
S = qumond_source(YE)
NPHI = 192
phi_g = (np.arange(NPHI) + 0.5) * (2 * np.pi / NPHI)
dphi = 2 * np.pi / NPHI
dlnr = np.diff(lnr).mean()
# cell weights: r^3 dlnr * w_gl * dphi  (volume in log-r shells x gauss x phi)
rho_p = r[:, None] * np.sqrt(1 - u_gl[None, :]**2)   # cylindrical radius of source pts
z_p = r[:, None] * u_gl[None, :]
Wcell = (r**3 * dlnr)[:, None] * w_gl[None, :] * dphi
SW = S * Wcell                                        # [NR, NTH]

def quad_boost(r0, th0):
    x0 = np.array([r0 * np.sin(th0), 0.0, r0 * np.cos(th0)])
    acc = 0.0
    for ph in np.array_split(phi_g, 8):
        cph = np.cos(ph)[None, None, :]
        sph = np.sin(ph)[None, None, :]
        dxs = x0[0] - rho_p[:, :, None] * cph
        dys = x0[1] - rho_p[:, :, None] * sph
        dzs = x0[2] - z_p[:, :, None]
        d2 = dxs**2 + dys**2 + dzs**2
        d3 = d2 * np.sqrt(d2)
        mask = d2 > (0.03 * r0)**2
        # radial (toward x0-hat) component of (x0 - x')/|d|^3
        proj = (dxs * x0[0] + dys * x0[1] + dzs * x0[2]) / r0
        acc += np.sum(np.where(mask, SW[:, :, None] * proj / d3, 0.0))
    # dPhi/dr(x0) along r0-hat of chi' = Poisson(S):  grad chi' = +(1/4pi) int S (x0-x')/|d|^3
    dPr_quad = acc / (4 * np.pi)
    return 1.0 + r0**2 * dPr_quad                     # B = -g_r_star r^2 = 1 + r^2 dPr

print("R3  independent QUMOND direct quadrature vs harmonic solver:")
from scipy.interpolate import RegularGridInterpolator
th_grid = np.arccos(u_gl)[::-1]
Bq_i = RegularGridInterpolator((np.log(r), th_grid), Bq[:, ::-1], bounds_error=True)
for r0 in (0.5, 1.0, 2.0, 5.0, 300.0):
    for th0 in (1e-3, np.pi / 3, np.pi / 2 - 1e-6):
        th_eval = min(max(th0, th_grid[0]), th_grid[-1])
        Bh = float(Bq_i([np.log(r0), th_eval]))
        Bd = quad_boost(r0, th_eval)
        print(f"    r={r0:7.1f} th={np.degrees(th_eval):5.1f}deg  harmonic {Bh:.4f}  quadrature {Bd:.4f}"
          f"  diff {Bd - Bh:+.4f} ({(Bd / Bh - 1) * 100:+.2f}%)")

# ---------- R4: AQUAL nonlinear Gauss flux at every radius ----------
print("=" * 90)
x_e = YE * n0
Gr = x_e * u_gl[None, :] - 1.0 / R2g + chi[0]
Gt = -x_e * sin_th[None, :] + chi[1]
gmag = np.hypot(Gr, Gt)
mu_g = mu_of_x(np.maximum(gmag, 1e-14))
flux = -0.5 * np.einsum("rt,t->r", mu_g * Gr, w_gl) * 4 * np.pi * r**2 / (4 * np.pi)
# flux of grad Phi = -g:  ratio to GM=1
sel = (r > 0.02) & (r < 2000.0)
worst = np.max(np.abs(flux[sel] - 1.0))
iw = np.argmax(np.abs(flux[sel] - 1.0))
print(f"R4  AQUAL Gauss flux  max |flux/4piGM - 1| = {worst:.4f} at r = {r[sel][iw]:.3f}")
for r0 in (0.05, 0.3, 1.0, 3.0, 10.0, 100.0, 1000.0):
    i0 = np.argmin(np.abs(r - r0))
    print(f"    r={r0:8.2f}  flux/(4 pi G M) = {flux[i0]:.4f}")
qflux = -0.5 * np.einsum("rt,t->r", nu(np.hypot(*gN_components(YE))) * gN_components(YE)[0]
                         - 0 * Gr, w_gl) * r**2  # not used; QUMOND flux differs (curl field)

# ---------- R5: Picard tail drift ----------
print("=" * 90)
ga2_r, ga2_t, cv2, itn2, chi2c = solve_aqual(YE, n_iter=150, chi0=chi)
Ba2 = -ga2_r * R2g
print(f"R5  Picard +150 extra iters: conv {cv:.2e} -> {cv2:.2e}")
for r0 in (0.5, 1.0, 5.0, 300.0):
    i0 = np.argmin(np.abs(r - r0))
    j_par, j_perp = np.argmax(u_gl), np.argmin(np.abs(u_gl))
    print(f"    r={r0:6.1f}  dB_par = {Ba2[i0, j_par] - Ba[i0, j_par]:+.5f}"
          f"  dB_perp = {Ba2[i0, j_perp] - Ba[i0, j_perp]:+.5f}"
          f"  (B_par {Ba2[i0, j_par]:.4f}, B_perp {Ba2[i0, j_perp]:.4f})")

# ---------- R6: inversion checks ----------
print("=" * 90)
xs = np.logspace(-4, 4, 2001)
ys = y_of_x(xs)
rt = np.max(np.abs(ys * nu(ys) / xs - 1.0))
print(f"R6  round trip max |y nu(y)/x - 1| = {rt:.2e}")
eps = 1e-4
L0_num = (np.log(mu_of_x(1.9 * (1 + eps))) - np.log(mu_of_x(1.9 * (1 - eps)))) / (2 * eps)
print(f"    L0 numeric dln mu/dln x at x=1.9: {L0_num:.5f}  vs formula {L0:.5f}")
dxdy_chk = np.gradient(_XT, _YT)
print(f"    min d(x)/dy over table = {dxdy_chk.min():.3e}  (monotonic: {np.all(np.diff(_XT) > 0)})")

# ---------- bonus: orientation-median sanity at saturation ----------
uu = np.linspace(-1 + 1e-9, 1 - 1e-9, 200001)
Bsat = n0 / np.sqrt(1 + L0 * (1 - uu**2))
print(f"    saturated AQUAL: median_u sqrt(B) = {np.median(np.sqrt(Bsat)):.4f}, "
      f"sphere-mean sqrt = {np.sqrt(0.5 * np.trapz(Bsat, uu)):.4f}, sqrt(nu0) = {np.sqrt(n0):.4f}")
print("=" * 90)
print("done")
