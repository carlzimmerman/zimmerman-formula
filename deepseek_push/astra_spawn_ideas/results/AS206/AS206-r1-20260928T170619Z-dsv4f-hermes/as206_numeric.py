#!/usr/bin/env python3
# AS206 seed -- numeric controls for the metric variation of the intrinsic Laplacian.
# Torus geometry: FFT (spectral) differentiation is exact on band-limited fields, so the
# coordinate definition of Delta_{h+eps k} u is evaluated to machine precision and the
# residual tests the operator identity alone. A coarse second-order FD cross-check (N8)
# confirms the spectral implementation agrees with a conventional finite-difference
# implementation of the same operator definition.
import numpy as np
import sys

PASS = True
def check(cid, name, cond, obs, thr):
    global PASS
    ok = bool(cond)
    PASS = PASS and ok
    print(f"[{'PASS' if ok else 'FAIL'}] {cid} {name}: {obs}  (threshold: {thr})")

rng = np.random.default_rng(20260928)

def trig_field(rng, shape, modes=(1, 2), amp=1.0):
    g = np.zeros(shape, dtype=float)
    for _ in range(6):
        m = rng.integers(modes[0], modes[1] + 1, size=len(shape))
        ph = rng.uniform(0, 2 * np.pi)
        fr = rng.uniform(0.3, 1.0) * amp
        cs = rng.choice([-1, 1], size=1)[0]
        x = np.meshgrid(*[np.arange(n) * 2 * np.pi / n for n in shape], indexing='ij')
        arg = sum(m[k] * x[k] for k in range(len(shape))) + ph
        g += cs * fr * np.cos(arg)
    return g

def grad_spectral(f):
    sh = f.shape; nd = len(sh)
    F = np.fft.rfftn(f)
    out = []
    for d in range(nd):
        k = np.fft.fftfreq(sh[d]) * sh[d]
        K = np.zeros(F.shape)
        sl = [slice(None)] * nd
        sl[d] = slice(0, F.shape[d])
        K[tuple(sl)] = k[:F.shape[d]].reshape([1 if i != d else -1 for i in range(nd)])
        out.append(np.fft.irfftn(1j * K * F, s=sh))
    return out

def hinv_of(h):
    # metric arrays carry the (n,n) matrix axes FIRST; invert those axes only
    return np.moveaxis(np.linalg.inv(np.moveaxis(h, (0, 1), (-2, -1))), (-2, -1), (0, 1))

def det_of(h):
    return np.linalg.det(np.moveaxis(h, (0, 1), (-2, -1)))

def lap_spec(h, u, deriv):
    nd = u.ndim
    det = det_of(h)
    sdet = np.sqrt(det)
    Hi = hinv_of(h)
    Gu = [deriv(u, d) for d in range(nd)]
    W = [np.zeros_like(u) for _ in range(nd)]          # W^i = sqrt(g) g^{ij} d_j u  (vector)
    for i in range(nd):
        for j in range(nd):
            W[i] += sdet * Hi[i, j] * Gu[j]
    S = np.zeros_like(u)
    for i in range(nd):
        S += deriv(W[i], i)                             # div W = d_i W^i
    return S / sdet

def christoffel_num(h, deriv, nd):
    # Gamma^i_{jk}; metric component derivatives are per-component (spatial axes only)
    Gam = {}
    hinv = hinv_of(h)
    for i in range(nd):
        for j in range(nd):
            for l in range(nd):
                s = np.zeros_like(h[0, 0])
                for m in range(nd):
                    # component-wise derivatives: h[a,b] is a pure spatial scalar field
                    s += hinv[l, m] * (deriv(h[m, j], i) + deriv(h[i, m], j) - deriv(h[i, j], m))
                Gam[(i, j, l)] = 0.5 * s
    return Gam

def lap_curved_formula(h, k, u, deriv):
    # RHS of the displayed identity: -khat^{ij} D_iD_j u - [D_i khat^{ij} - (1/2) D^j T] D_j u
    nd = u.ndim
    hinv = hinv_of(h)
    det = det_of(h)
    khat = np.einsum('ia...,ab...,bj...->ij...', hinv, k, hinv)     # k^{ij} = h^{ia} h^{jb} k_ab (NOT delta h^{ij})
    T = np.einsum('ij...,ij...->...', hinv, k)                      # tr_h(k)
    Gam = christoffel_num(h, deriv, nd)
    Gu = [deriv(u, d) for d in range(nd)]
    GGu = np.zeros((nd, nd) + u.shape)
    for i in range(nd):
        for j in range(nd):
            GGu[i, j] = deriv(Gu[i], j)
            for l in range(nd):
                GGu[i, j] -= Gam[(i, j, l)] * Gu[l]
    term1 = np.zeros_like(u)
    for i in range(nd):
        for j in range(nd):
            term1 += khat[i, j] * GGu[i, j]
    out = -term1
    for j in range(nd):
        DKj = np.zeros_like(u)
        for i in range(nd):
            DKj += deriv(khat[i, j], i)
            for l in range(nd):
                DKj += Gam[(i, l, j)] * khat[i, l]     # Gamma^j_{i l} khat^{i l}
                DKj += Gam[(i, l, i)] * khat[l, j]     # Gamma^i_{i l} khat^{l j}
        DTj = np.zeros_like(u)
        for m in range(nd):
            DTj += hinv[j, m] * deriv(T, m)            # D^j T
        out -= (DKj - 0.5 * DTj) * Gu[j]
    return out

def lap_wrong_formula(h, k, u, deriv):
    # NEGATIVE CONTROL operator: the -(1/2) D^j tr_h(k) volume term is OMITTED
    nd = u.ndim
    hinv = hinv_of(h)
    khat = np.einsum('ia...,ab...,bj...->ij...', hinv, k, hinv)
    Gam = christoffel_num(h, deriv, nd)
    Gu = [deriv(u, d) for d in range(nd)]
    GGu = np.zeros((nd, nd) + u.shape)
    for i in range(nd):
        for j in range(nd):
            GGu[i, j] = deriv(Gu[i], j)
            for l in range(nd):
                GGu[i, j] -= Gam[(i, j, l)] * Gu[l]
    out = np.zeros_like(u)
    for i in range(nd):
        for j in range(nd):
            out -= khat[i, j] * GGu[i, j]
    for j in range(nd):
        DKj = np.zeros_like(u)
        for i in range(nd):
            DKj += deriv(khat[i, j], i)
            for l in range(nd):
                DKj += Gam[(i, l, j)] * khat[i, l]
                DKj += Gam[(i, l, i)] * khat[l, j]
        out -= DKj * Gu[j]
    return out

eps_vals = np.array([1e-4, 1e-5, 1e-6])
def intercept(R):
    # vectorized per-point linear fit R(eps) = a + b*eps -> intercept a (eps->0 limit)
    R = np.array(R)
    shape = R.shape[1:]
    Rt = R.reshape(3, -1)
    X = np.column_stack([np.ones_like(eps_vals), eps_vals])
    c, *_ = np.linalg.lstsq(X, Rt, rcond=None)
    return c[0].reshape(shape)
def rel(a, b):
    return np.max(np.abs(a - b)) / max(np.max(np.abs(b)), 1e-30)

# ================= N1a: general symmetric k, CURVED 2D torus =================
N = 32
n2 = (N, N)
x2 = np.meshgrid(*[np.arange(n) * 2 * np.pi / n for n in n2], indexing='ij')
h2 = np.empty((2, 2) + n2)
h2[0, 0] = 1.0 + 0.15 * np.cos(x2[1]); h2[1, 1] = 1.0 + 0.15 * np.cos(x2[0])
h2[0, 1] = 0.1 * np.sin(x2[0] + x2[1]); h2[1, 0] = h2[0, 1]
k2 = np.empty((2, 2) + n2)
k2[0, 0] = trig_field(rng, n2); k2[1, 1] = trig_field(rng, n2)
k2[0, 1] = trig_field(rng, n2); k2[1, 0] = k2[0, 1]
u2 = trig_field(rng, n2)
def deriv2(f, d):
    return grad_spectral(f)[d]

del0 = lap_spec(h2, u2, deriv2)
rhs2 = lap_curved_formula(h2, k2, u2, deriv2)
R = [(lap_spec(h2 + ep * k2, u2, deriv2) - del0) / ep for ep in eps_vals]
a_int = intercept(R)
check('N1a', 'general symmetric k, CURVED 2D torus: eps->0 rate equals displayed formula',
      rel(a_int, rhs2) < 1e-8, f'max relative residual = {rel(a_int, rhs2):.3e}', '< 1e-8 (spectral)')

# ================= N1b + N6: 3D torus, general k; curved and flat h =================
# NOTE: the intermediates hinv = h^{-1} and sqrt(det h) are NOT band-limited; their FFT
# derivatives carry a grid-dependent reconstruction error. N=32 shows ~2e-5 relative
# residual for the 3D curved case; the identity check is therefore run at N = 64 where
# the residual is the pure eps-truncation term (verified: fit intercept ~ 1e-9).
N3 = 64
n3 = (N3, N3, N3)
x3 = np.meshgrid(*[np.arange(n) * 2 * np.pi / n for n in n3], indexing='ij')
u3 = trig_field(rng, n3)
def deriv3(f, d):
    return grad_spectral(f)[d]
h3 = np.zeros((3, 3) + n3)
for i in range(3):
    h3[i, i] = 1.0 + 0.1 * trig_field(rng, n3)
h3[0, 1] = h3[1, 0] = 0.08 * trig_field(rng, n3)
h3[0, 2] = h3[2, 0] = 0.08 * trig_field(rng, n3)
h3[1, 2] = h3[2, 1] = 0.08 * trig_field(rng, n3)
k3 = np.zeros((3, 3) + n3)
for i in range(3):
    k3[i, i] = 0.3 * trig_field(rng, n3)
k3[0, 1] = k3[1, 0] = 0.3 * trig_field(rng, n3)
k3[0, 2] = k3[2, 0] = 0.3 * trig_field(rng, n3)
k3[1, 2] = k3[2, 1] = 0.3 * trig_field(rng, n3)

del0_3 = lap_spec(h3, u3, deriv3)
rhs3 = lap_curved_formula(h3, k3, u3, deriv3)
R3 = [(lap_spec(h3 + ep * k3, u3, deriv3) - del0_3) / ep for ep in eps_vals]
a3 = intercept(R3)
check('N1b', 'general symmetric k, 3D torus (curved h): eps->0 rate equals displayed formula',
      rel(a3, rhs3) < 1e-8, f'max relative residual = {rel(a3, rhs3):.3e}', '< 1e-8 (spectral)')

hflat = np.zeros((3, 3) + n3)
for i in range(3):
    hflat[i, i] = 1.0
del0f = lap_spec(hflat, u3, deriv3)
rhsf = lap_curved_formula(hflat, k3, u3, deriv3)
Rf = [(lap_spec(hflat + ep * k3, u3, deriv3) - del0f) / ep for ep in eps_vals]
af = intercept(Rf)
check('N6', 'flat leaf limiting case (h = delta_ij): same identity, connection terms vanish',
      rel(af, rhsf) < 1e-8, f'max relative residual = {rel(af, rhsf):.3e}', '< 1e-8 (spectral)')

# ================= N2 / N2b: conformal specialization =================
sig3 = trig_field(rng, n3, amp=0.25)
kconf = np.zeros((3, 3) + n3)
for i in range(3):
    kconf[i, i] = 2 * sig3
Gus = [deriv3(u3, d) for d in range(3)]
rhsc = -2 * sig3 * del0f + sum(Gus[d] * deriv3(sig3, d) for d in range(3))
Rc = [(lap_spec(hflat + ep * kconf, u3, deriv3) - del0f) / ep for ep in eps_vals]
ac = intercept(Rc)
check('N2', 'conformal k = 2 sig delta, 3D flat: -2 sig Delta u + <grad sig, grad u>',
      rel(ac, rhsc) < 1e-8, f'max relative residual = {rel(ac, rhsc):.3e}', '< 1e-8; grad-term coefficient +1 = (n-2)')

sig2 = trig_field(rng, n2, amp=0.25)
kconf2 = np.empty((2, 2) + n2)
for i in range(2):
    for j in range(2):
        kconf2[i, j] = 2 * sig2 * h2[i, j]          # conformal wrt the CURVED h2: k = 2 sig h (off-diagonal included)
del0c2 = lap_spec(h2, u2, deriv2)
rhsc2 = -2 * sig2 * del0c2          # (n-2) = 0 in 2D: gradient term drops out
Rc2 = [(lap_spec(h2 + ep * kconf2, u2, deriv2) - del0c2) / ep for ep in eps_vals]
ac2 = intercept(Rc2)
check('N2b', 'conformal k = 2 sig h, CURVED 2D torus: -2 sig Delta u alone (n-2 = 0)',
      rel(ac2, rhsc2) < 1e-8, f'max relative residual = {rel(ac2, rhsc2):.3e}', '< 1e-8')

# ================= N3: XC1 peer-review witness (REVIEW.md lines 100-128) =================
K = 20; b = 0.5; NW = 128
xw = np.arange(NW) * 2 * np.pi / NW
Uw = np.cos(K * xw); Sw = np.cos((K - 1) * xw)
def grad1(f):
    F = np.fft.rfft(f)
    kk = np.fft.fftfreq(NW) * NW
    return np.fft.irfft(1j * kk[:F.shape[0]] * F, n=NW)
delU = -2 * Sw * (-K * K * Uw) + grad1(Sw) * grad1(Uw)
proj_cos1 = 2 * np.abs(np.fft.rfft(delU)[1]) / NW
an1 = (3 * K * K - K) / 2
proj_cos39 = 2 * np.abs(np.fft.rfft(delU)[2 * K - 1]) / NW   # NW/2 = 64 > 39: resolvable
an39 = K * (K + 1) / 2
check('N3', 'XC1 witness: delta Delta[cos(Kx)], sigma = cos((K-1)x): cos-x coefficient = (3K^2-K)/2',
      (proj_cos39 > 0) and abs(proj_cos1 - an1) / an1 < 1e-9,
      f'grid cos-x {proj_cos1:.10f} vs analytic {an1:.10f}; grid cos((2K-1)x) {proj_cos39:.10f} vs {an39:.10f}',
      '< 1e-9 relative (spectral projection)')
coef_review = (3 * K * K - K) / (2 * (K * K - 1)) * (np.exp(-b) - np.exp(-b * K * K))
check('N3c', 'XC1 review Duhamel-weighted coefficient at K = 20, b = 1/2 equals 0.896875',
      abs(coef_review - 0.896875) / 0.896875 < 1e-4,
      f'computed {coef_review:.10f}', 'review value 0.896875; tol 1e-4 relative')

# ================= N4: negative control =================
wrong3 = lap_wrong_formula(h3, k3, u3, deriv3)
check('N4', 'NEGATIVE CONTROL: omitting the volume variation -> wrong operator (3D general k)',
      rel(a3, wrong3) > 0.01, f'max relative deviation from the true variation = {rel(a3, wrong3):.3e}',
      'control MUST fire: deviation > 0.01')
wconf = -2 * Sw * (-K * K * Uw) - 2 * grad1(Sw) * grad1(Uw)          # wrong conf. operator: coeff -2
proj_wrong = 2 * np.abs(np.fft.rfft(wconf)[1]) / NW
check('N4b', 'NEGATIVE CONTROL (conformal, 1D witness): wrong cos-x coefficient = K = 20, not 590',
      abs(proj_wrong - K) < 1e-9 and abs((proj_wrong - an1) / an1) > 0.5,
      f'wrong coefficient {proj_wrong:.6f} vs true (3K^2-K)/2 = {an1:.6f}', 'control fires: 20 vs 590')

# ================= N5: refinement N = 32 -> 64 =================
def run_3d_general(NN):
    nn = (NN, NN, NN)
    r2 = np.random.default_rng(20260928)
    tf = lambda shape: trig_field(r2, shape)
    uu = tf(nn)
    hh = np.zeros((3, 3) + nn)
    for i in range(3):
        hh[i, i] = 1.0 + 0.1 * tf(nn)
    hh[0, 1] = hh[1, 0] = 0.08 * tf(nn); hh[0, 2] = hh[2, 0] = 0.08 * tf(nn); hh[1, 2] = hh[2, 1] = 0.08 * tf(nn)
    kk = np.zeros((3, 3) + nn)
    for i in range(3):
        kk[i, i] = 0.3 * tf(nn)
    kk[0, 1] = kk[1, 0] = 0.3 * tf(nn); kk[0, 2] = kk[2, 0] = 0.3 * tf(nn); kk[1, 2] = kk[2, 1] = 0.3 * tf(nn)
    dv = lambda f, d: grad_spectral(f)[d]
    d0 = lap_spec(hh, uu, dv)
    rr = lap_curved_formula(hh, kk, uu, dv)
    R = [(lap_spec(hh + ep * kk, uu, dv) - d0) / ep for ep in eps_vals]
    return rel(intercept(R), rr)

res32 = run_3d_general(32)
res64 = run_3d_general(64)
check('N5', 'refinement N = 32 -> 64 (3D general k): residual stays below tolerance',
      res32 < 1e-8 and res64 < 1e-8, f'N=32: {res32:.3e}; N=64: {res64:.3e}', '< 1e-8 both')

# ================= N8: coarse-FD cross-check of the operator implementation =================
def lap_fd3(hh, uu):
    NN = uu.shape[0]; dx = 2 * np.pi / NN
    sdet = np.sqrt(det_of(hh))
    Hi = hinv_of(hh)
    def G(f, d):
        return (np.roll(f, -1, axis=d) - np.roll(f, 1, axis=d)) / (2 * dx)
    Gu = [G(uu, d) for d in range(3)]
    W = [np.zeros_like(uu) for _ in range(3)]            # W^i = sqrt(g) g^{ij} d_j u (vector)
    for i in range(3):
        for j in range(3):
            W[i] += sdet * Hi[i, j] * Gu[j]
    out = np.zeros_like(uu)
    for i in range(3):
        out += G(W[i], i)
    return out / sdet

N8N = 64
n8 = (N8N, N8N, N8N)
x8 = np.meshgrid(*[np.arange(n) * 2 * np.pi / n for n in n8], indexing='ij')
r8 = np.random.default_rng(20260928)
def tf8(shape, amp=1.0):
    return trig_field(r8, shape, amp=amp)
h8 = np.zeros((3, 3) + n8)
for i in range(3):
    h8[i, i] = 1.0 + 0.1 * tf8(n8)
h8[0, 1] = h8[1, 0] = 0.08 * tf8(n8); h8[0, 2] = h8[2, 0] = 0.08 * tf8(n8); h8[1, 2] = h8[2, 1] = 0.08 * tf8(n8)
u8 = tf8(n8)
def deriv8(f, d):
    return grad_spectral(f)[d]
val_fd = lap_fd3(h8, u8)
val_sp = lap_spec(h8, u8, deriv8)
check('N8', 'operator-definition cross-check: 2nd-order FD vs spectral Laplacian agree at N=64 (same operator, independent implementations)',
      rel(val_fd, val_sp) < 5e-2, f'max relative difference = {rel(val_fd, val_sp):.3e}', '< 5e-2 (2nd-order FD, mode<=4 fields, h^2-limited)')

# ================= N7: footings (both a0 values, kept separate; SI) =================
G = 6.67430e-11; c = 299792458.0
a0_c = 9.3619e-11; a0_a = 1.1279e-10
rho_c = 4 * a0_c**2 / (G * c**2)
rho_a = 4 * a0_a**2 / (G * c**2)
kappa_eff = a0_a / (c * np.sqrt(G * rho_c))
check('N7', 'footings: canonical rho_L = 5.844412e-27 kg/m^3 at kappa = 1/2; alt kappa_eff = 0.60238840 at fixed rho_L',
      abs(rho_c - 5.844412e-27) / 5.844412e-27 < 1e-6 and abs(kappa_eff - 0.60238840) < 1e-6,
      f'rho_L(can, a0 = 9.3619e-11) = {rho_c:.6e} kg/m^3; rho_L(alt, fixed kappa) = {rho_a:.6e} kg/m^3;'
      f' kappa_eff(alt, fixed rho_L) = {kappa_eff:.8f}',
      'the two footings never share (rho_L, kappa)')

print()
print('ALL NUMERIC CHECKS PASS' if PASS else 'SOME NUMERIC CHECKS FAILED')
sys.exit(0 if PASS else 1)