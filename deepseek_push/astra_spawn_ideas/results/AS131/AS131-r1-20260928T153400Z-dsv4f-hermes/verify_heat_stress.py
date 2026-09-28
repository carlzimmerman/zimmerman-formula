#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AS131 bounded verification -- heat-field metric stress of ACTION (4), FINAL_ACTION.md (CA4-GNC),
heat-constraint block:

    S_heat = (M_P^2 c_N / 2) * ∫ dτ ∫_Σ N√h ∫_0^b dr L(r,x)[∂_r W - Δ_h W],   b = ξ²/2

After spatial integration by parts (closed leaf, no boundary):

    ∫ N√h L Δ_h W = -∫ N√h [ <DL,DW> + L <Dln N,DW> ]              (CORRECT IBP)

The claimed metric stress at fixed lapse N and fixed independent fields W,L:

    δ_h S_heat = (M_P² c_N / 2) ∫dτ ∫dr ∫_Σ N√h Θ^{ij} δh_ij
    Θ^{ij} = ½ h^{ij} B0 - D^{(i}L D^{j)}W - L D^{(i}ln N D^{j)}W
    B0 = L ∂_r W + <DL,DW> + L <Dln N,DW>

All checks are numerically exact on bandlimited witnesses (periodic spectral quadrature
on T^3, Gauss-Legendre x trapezoid on S^2), so the residuals are real computation,
not booleans. Every control is capable of failing; the negative control (discarding the
derivative of N in the integration by parts) is REQUIRED to fail on nonconstant lapse.

Bounds (ACTUALLY enforced): wall <= 120 s (timed; check at end), memory <= 512 MB
(resource.setrlimit RLIMIT_AS soft cap), threads = 1 (env caps + verified).
"""
import os, sys, time, json, resource, threading

# ---- enforce declared bounds *before* importing numerical libs ----
_MEM_BYTES = 512 * 1024 * 1024
try:
    _soft, _hard = resource.getrlimit(resource.RLIMIT_AS)
    _cap = min(_MEM_BYTES, _hard if _hard != -1 else _MEM_BYTES)
    resource.setrlimit(resource.RLIMIT_AS, (_cap, _hard))
    _mem_enforced = True
except Exception as e:
    _mem_enforced = False
    print(f"[bounds] RLIMIT_AS not settable: {e}", flush=True)

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

_t0 = time.time()

import numpy as np
from numpy.fft import fftn, ifftn
from scipy.special import lpmv
from numpy.polynomial.legendre import leggauss

def check(name, got, tol, sign="abs", ref=None):
    """Returns pass/fail with the observed residual. Tolerance in ABSOLUTE residual."""
    res = abs(got)
    ok = res <= tol
    print(f"[check] {name:55s} residual={res:.6e} tol={tol:.1e} -> {'PASS' if ok else 'FAIL'}", flush=True)
    return {"name": name, "residual": float(res), "tol": float(tol), "value": float(got), "pass": bool(ok)}

# ------------------------------------------------------------------ constants
G = 6.67430e-11; c = 299792458.0; M_sun = 1.98847e30; pc = 3.085677581491367e16
a0_can = 9.3619e-11; a0_alt = 1.1279e-10
kappa = 0.5   # adopted input, NOT derived here
rhoL_can = 4.0 * a0_can**2 / (G * c**2)        # rho_Lambda = 4 a0^2/(G c^2) at kappa=1/2
rhoL_alt = 4.0 * a0_alt**2 / (G * c**2)
Lam_can = 32.0 * np.pi * a0_can**2 / c**4      # Lambda = 32 pi a0^2/c^4 (Einstein=scale G)
Lam_alt = 32.0 * np.pi * a0_alt**2 / c**4
GN = G                                        # measured Newton coupling (SI)
alpha = 9.6240479669e-14                      # XC1 window input (illustrative parameter cell)
cN = 1.0 - alpha / 2.0
Gbare = GN / cN                               # FINAL_ACTION sect.5: G_N = G_bare / c_N (derived there)
Gcosmo = cN * GN                              # FINAL_ACTION eq.(18): G_cosm/G_N = c_N
MP2_cN = 1.0 / (8.0 * np.pi * Gbare) * cN     # (M_P^2 c_N) in kg s^2 / m^3 (SI)
print("[constants] rho_Lambda canonical  = %.6e kg/m^3" % rhoL_can, flush=True)
print("[constants] rho_Lambda alternative= %.6e kg/m^3" % rhoL_alt, flush=True)
print("[constants] Lambda canonical/alt   = %.6e / %.6e m^-2" % (Lam_can, Lam_alt), flush=True)
print("[constants] c_N = %.16g  G_bare/G_N = %.16g  G_cosmo/G_N = %.16g" % (cN, Gbare/GN, Gcosmo/GN), flush=True)
print("[constants] (M_P^2 c_N/2) = %.6e kg s^2/m^3 (SI)" % (MP2_cN/2.0), flush=True)

results = {"checks": [], "bounds": {}}

# ==================================================================
# (A) FLAT T^3 FOURIER WITNESS  -- nonconstant lapse, exact spectrum
# ==================================================================
N3 = 64                                   # bandlimits <= ~44 with coefficients <= 1e-40; exact to machine precision
x = (np.arange(N3) * 2.0 * np.pi / N3)
X1, X2, X3 = np.meshgrid(x, x, x, indexing="ij")
sigN = 0.5
Nfield = np.exp(sigN * np.cos(X1))            # NONCONSTANT lapse N = e^{σ}
dlnN1 = -sigN * np.sin(X1)
k1, k2, k3 = 1, 0, 0
q1, q2, q3 = 2, 0, 0
mu = 1.7
W = np.cos(k1 * X1 + k2 * X2 + k3 * X3)
L = np.cos(q1 * X1 + q2 * X2 + q3 * X3)

def spectral_grad(f, axis):
    F = fftn(f)
    kk = np.fft.fftfreq(N3, d=2.0 * np.pi / N3) * 2.0 * np.pi
    sh = [1]*3; sh[axis] = N3
    K = np.reshape(kk, sh)
    return np.real(ifftn(F * (1j * K)))

dW1, dW2, dW3 = spectral_grad(W, 0), spectral_grad(W, 1), spectral_grad(W, 2)
dL1, dL2, dL3 = spectral_grad(L, 0), spectral_grad(L, 1), spectral_grad(L, 2)
d2W = spectral_grad(dW1, 0) + spectral_grad(dW2, 1) + spectral_grad(dW3, 2)  # Δ_δ W
mean = lambda f: f.mean()

# ORIGINAL operator evaluation (the action's own integrand  L(∂_r W - Δ_h W) ):
I_direct = mean(Nfield * L * (mu * W - d2W))
I_correct = mean(Nfield * (mu * L * W + (dL1*dW1 + dL2*dW2 + dL3*dW3)
                           + L * (dlnN1*dW1 + 0.0*dW2 + 0.0*dW3)))
I_wrong = mean(Nfield * (mu * L * W + (dL1*dW1 + dL2*dW2 + dL3*dW3)))   # N-derivative DISCARDED

results["checks"] += [
    check("A1 flat-T3: direct == correct IBP (incl. lapse-gradient)", I_direct - I_correct, 2e-10),
]
r_wrong = I_direct - I_wrong
ok = abs(r_wrong) > 1e-4
results["checks"].append({"name": "A2 NEGATIVE CONTROL flat-T3: wrong IBP must FAIL (residual large)",
                          "residual": float(abs(r_wrong)), "tol": 1e-4, "value": float(r_wrong),
                          "pass": bool(ok)})
print(f"[check] A2 NEGATIVE CONTROL flat-T3: wrong-IBP residual = {abs(r_wrong):.6e} (must be > 1e-4) -> {'PASS' if ok else 'FAIL'}",
      flush=True)
# constant-lapse discrimination: with sigN -> 0 the wrong IBP should PASS (term vanishes)
Nfield0 = np.ones_like(Nfield)
I_direct0 = mean(L * (mu * W - d2W))
I_wrong0 = mean(mu * L * W + (dL1*dW1 + dL2*dW2 + dL3*dW3))
results["checks"].append({"name": "A3 constant-lapse limit: lapse-gradient term vanishes (both agree)",
                          "residual": float(abs(I_direct0 - I_wrong0)), "tol": 2e-10,
                          "value": float(I_direct0 - I_wrong0), "pass": bool(abs(I_direct0 - I_wrong0) <= 2e-10)})
print(f"[check] A3 constant-lapse limit: residual = {abs(I_direct0 - I_wrong0):.6e} -> {'PASS' if abs(I_direct0-I_wrong0)<=2e-10 else 'FAIL'}", flush=True)

# ==================================================================
# (B) CURVED 3-TORUS  -- h_0 = e^{2 σ_h cos x1} δ (Γ ≠ 0), nonconstant lapse
# ==================================================================
sigc = 0.3
sh = np.exp(sigc * np.cos(X1))           # conformal factor of h_0
sqrt_h0 = sh**3
dlns1 = -sigc * np.sin(X1)
W2 = np.cos(1*X1 + 1*X2 + 0*X3)
L2 = np.cos(2*X1 + 1*X2 + 0*X3)          # unit x2 phases: coupling with χ=cos(2x2) yields a nonzero mean
dW2_1, dW2_2, dW2_3 = spectral_grad(W2,0), spectral_grad(W2,1), spectral_grad(W2,2)
dL2_1, dL2_2, dL2_3 = spectral_grad(L2,0), spectral_grad(L2,1), spectral_grad(L2,2)
# Δ_h0 f = e^{-2σ}(Δ_δ f + (n-2) <dσ,df>_δ), n=3 -> + <dσ,df>
d2W2 = spectral_grad(dW2_1,0) + spectral_grad(dW2_2,1) + spectral_grad(dW2_3,2)
lap_h0_W2 = np.exp(-2.0*sigc*np.cos(X1)) * (d2W2 + (dlns1*dW2_1 + 0*dW2_2 + 0*dW2_3))
inner = lambda a1,a2,a3,b1,b2,b3: np.exp(-2.0*sigc*np.cos(X1))*(a1*b1+a2*b2+a3*b3)
dlnN1b = dlnN1
I2_direct = mean(Nfield * sqrt_h0 * L2 * (mu * W2 - lap_h0_W2))
I2_correct = mean(Nfield * sqrt_h0 * (mu*L2*W2 + inner(dL2_1,dL2_2,dL2_3,dW2_1,dW2_2,dW2_3)
                                      + L2*inner(dlnN1b,0,0,dW2_1,dW2_2,dW2_3)))
I2_wrong = mean(Nfield * sqrt_h0 * (mu*L2*W2 + inner(dL2_1,dL2_2,dL2_3,dW2_1,dW2_2,dW2_3)))
results["checks"] += [
    check("B1 curved-T3: direct == correct IBP (Γ present, lapse-gradient present)", I2_direct - I2_correct, 5e-10)]
r2 = I2_direct - I2_wrong
ok = abs(r2) > 1e-3
results["checks"].append({"name":"B2 NEGATIVE CONTROL curved-T3: wrong IBP must FAIL","residual": float(abs(r2)),
                          "tol": 1e-3, "value": float(r2), "pass": bool(ok)})
print(f"[check] B2 NEGATIVE CONTROL curved-T3: wrong-IBP residual = {abs(r2):.6e} (must be > 1e-3) -> {'PASS' if ok else 'FAIL'}", flush=True)

# ==================================================================
# (C) STRESS: conformal family h_ε = e^{2 ε χ} h_0 on the curved torus, FIXED lapse
#     dS/dε|0 from the claimed Θ^{ij}  vs  finite difference (refined once)
# ==================================================================
chi_c = np.cos(0*X1 + 2*X2 + 0*X3)        # cos(2 x2): couples to the W2/L2 phases so the wrong-stress control bites
A0 = inner(dL2_1,dL2_2,dL2_3,dW2_1,dW2_2,dW2_3) + L2*inner(dlnN1b,0,0,dW2_1,dW2_2,dW2_3)
B0 = mu*L2*W2 + A0
def S_eps(eps):
    return mean(Nfield * np.exp(3.0*eps*chi_c) * sqrt_h0 * (mu*L2*W2 + np.exp(-2.0*eps*chi_c)*A0))
def S_eps_orig(eps):
    # original operator: given h0 = e^{2σ(x)}δ with σ = σc cos x1, and h_ε = e^{2εχ}h0,
    # in n=3: Δ_{e^{2f}h} φ = e^{-2f}( Δ_h φ + <df,dφ>_h ), f = εχ:
    #   Δ_{h_ε} W = e^{-2εχ}( Δ_{h0} W + ε <dχ,dW>_{h0} )
    dch = (np.zeros_like(X2), -2.0*np.sin(2.0*X2), np.zeros_like(X2))   # χ = cos(2 x2)
    lap_eps = np.exp(-2.0*eps*chi_c) * (lap_h0_W2
                + eps * inner(dch[0], dch[1], dch[2], dW2_1, dW2_2, dW2_3))
    return mean(Nfield * np.exp(3.0*eps*chi_c) * sqrt_h0 * L2 * (mu*W2 - lap_eps))
eps0 = 1e-6
S0, Sp, Sm = S_eps(0.0), S_eps(eps0), S_eps(-eps0)
S0o, Spo, Smo = S_eps_orig(0.0), S_eps_orig(eps0), S_eps_orig(-eps0)
fd = (Sp - Sm) / (2.0*eps0)                       # O(ε²)-accurate central difference
fd5 = (-S_eps(2*eps0) + 8*S_eps(eps0) - 8*S_eps(-eps0) + S_eps(-2*eps0)) / (12*eps0)
pred = mean(Nfield * sqrt_h0 * chi_c * (3.0*mu*L2*W2 + A0))
pred_wrong = mean(Nfield * sqrt_h0 * chi_c * (3.0*mu*L2*W2 + inner(dL2_1,dL2_2,dL2_3,dW2_1,dW2_2,dW2_3)))
results["checks"] += [
    check("C1 stress conformal: IBP-eval == original-operator eval (ε=+1e-6)", Sp - Spo, 5e-10),
    check("C2 stress conformal: FD dS/dε == Θ^{ij} prediction (central)", fd - pred, 2e-9),
    check("C3 stress conformal: 5-point FD dS/dε == Θ^{ij} prediction", fd5 - pred, 2e-9),
]
r3 = fd - pred_wrong
ok = abs(r3) > 1e-6
results["checks"].append({"name":"C4 NEGATIVE CONTROL stress: wrong stress (no lapse-gradient) must FAIL","residual": float(abs(r3)),
                          "tol": 1e-6, "value": float(r3), "pass": bool(ok)})
print(f"[check] C4 NEGATIVE CONTROL stress: wrong-stress residual = {abs(r3):.6e} (must be > 1e-6) -> {'PASS' if ok else 'FAIL'}", flush=True)

# ==================================================================
# (D) STRESS: anisotropic family  h_ε = diag(1+εχ, 1, 1)  on flat T³ (Γ ≠ 0 for ε ≠ 0)
# ==================================================================
chi_d = np.cos(X2)
def S_aniso(eps):
    r = 1.0 + eps*chi_d
    inv = 1.0/r
    inner_e = inv*dL1*dW1 + dL2*dW2 + dL3*dW3
    lne_e = inv*dlnN1*dW1
    return mean(Nfield * np.sqrt(r) * (mu*L*W + inner_e + L*lne_e))
fdA = (S_aniso(eps0) - S_aniso(-eps0)) / (2*eps0)
# Θ^{ij}δh_ij with δh_11 = χ_d:
B0d = mu*L*W + (dL1*dW1 + dL2*dW2 + dL3*dW3) + L*dlnN1*dW1
predA = mean(Nfield * (0.5*chi_d*B0d - chi_d*dL1*dW1 - chi_d*L*dlnN1*dW1))
results["checks"].append(check("D1 stress anisotropic: FD dS/dε == Θ^{ij} prediction", fdA - predA, 2e-9))

# ==================================================================
# (E) ON-SHELL measure: ∂_r W = Δ_h W  =>  ∫ N√h B0 = 0  and  B0 = div_N(L DW)
# ==================================================================
# on-shell W on flat T^3: W_os = e^{-k² r} cos(k·x) with ∂_r W_os = Δ W_os = -k² W_os
Wos = np.cos(1*X1 + 2*X2 + 0*X3)      # e^{-5 r} factor is a common r-dependent constant (drops)
dWos1, dWos2, dWos3 = spectral_grad(Wos,0), spectral_grad(Wos,1), spectral_grad(Wos,2)
Box = 1.0*np.cos(1*X1 + 2*X2 + 0*X3)  # B0 contains L ∂_r W = L·(-k²)·Wos  (k²=5, μ=-5)
mu_os = -5.0
B0os = mu_os*L*Wos + (dL1*dWos1 + dL2*dWos2 + dL3*dWos3) + L*(dlnN1*dWos1)
intB0 = mean(Nfield * B0os)
divN_LDW = (spectral_grad(Nfield*L*dWos1,0) + spectral_grad(Nfield*L*dWos2,1) + spectral_grad(Nfield*L*dWos3,2))/Nfield
point_res = np.abs(B0os - divN_LDW).max()
results["checks"] += [
    check("E1 on-shell measure: ∫ N√h B0 = 0 (closed leaf)", intB0, 5e-10),
    check("E2 on-shell identity: B0 = div_N(L DW) pointwise (sup norm)", point_res, 5e-9),
]
# off-shell identity: ∫ N√h B0 = ∫ N√h L(∂_r W - Δ_h W)  (W2, curved torus, μ W ≠ Δ W)
B0off = mu*L2*W2 + A0
intB0off = mean(Nfield * sqrt_h0 * B0off)
intcons = mean(Nfield * sqrt_h0 * L2 * (mu*W2 - lap_h0_W2))
results["checks"].append(check("E3 off-shell identity: ∫N√h B0 = ∫N√h L(∂_rW-Δ_hW)", intB0off - intcons, 5e-10))

# ==================================================================
# (F) S² ROUND SPHERE (genuine connection terms), Gauss-Legendre quadrature, REFINED ONCE
#     Δ_h f = (1/sinθ)∂_θ(sinθ ∂_θ f) + (1/sin²θ)∂_φ² f
# ==================================================================
def s2_quad(Nth, Nph):
    # Round sphere: h = dθ² + sin²θ dφ², √h = sinθ, Δ_h f = (1/sinθ)∂_θ(sinθ∂_θ f) + (1/sin²θ)∂_φ² f.
    # Exact mode representation (lpmv includes the Condon-Shortley phase, so
    #   P_l^1(cosθ) = d/dθ P_l(cosθ),  Δ_h P_l(cosθ) = 2cotθ P_l^1 + P_l^2 = -l(l+1)P_l ).
    th, wth = leggauss(Nth); th = np.arccos(th)          # GL on θ ∈ [0,π]
    ph = np.arange(Nph) * 2.0*np.pi / Nph
    TH, PH = np.meshgrid(th, ph, indexing="ij")
    sinth = np.sin(TH); costh = np.cos(TH); coth = costh/sinth
    Wf = lpmv(0, 2, costh)
    Lf = lpmv(0, 3, costh)
    Nf = np.exp(0.4*costh)                                # NONCONSTANT lapse
    dWth = lpmv(1, 2, costh)                              # exact ∂_θ W
    dLth = lpmv(1, 3, costh)                              # exact ∂_θ L
    lapW = 2.0*coth*lpmv(1, 2, costh) + lpmv(2, 2, costh) # exact Δ_h W (operator form)
    # diagnostics: operator must agree with the eigenvalue and the derivative with -3 c s
    assert np.abs(lapW + 6.0*Wf).max() < 1e-10
    assert np.abs(dWth + 3.0*costh*sinth).max() < 1e-10
    innerf = dLth*dWth
    dlnNf = -0.4*sinth
    # Quadrature: ∫₀^π f(θ) dθ with f = sinθ·g(θ) equals ∫_{-1}^1 g(arccos u) du exactly
    # (sinθ cancels the Jacobian), so sample the smooth g(u) at GL nodes.
    gL = 2.0*np.pi * (Nf*Lf*(mu*Wf - lapW)).mean(axis=1) @ wth   # ∫dφ = 2π, GL exact on u
    d1, c1, w1 = gL, \
        2.0*np.pi * (Nf*(mu*Lf*Wf + innerf + Lf*dlnNf*dWth)).mean(axis=1) @ wth, \
        2.0*np.pi * (Nf*(mu*Lf*Wf + innerf)).mean(axis=1) @ wth
    return d1, c1, w1

resS2_coarse = s2_quad(96, 192)
resS2_fine = s2_quad(192, 384)
results["checks"] += [
    check("F1 S2 coarse (96x192): direct == correct IBP", resS2_coarse[0]-resS2_coarse[1], 2e-7),
    check("F2 S2 refined (192x384): direct == correct IBP", resS2_fine[0]-resS2_fine[1], 2e-9),
]
rF = resS2_fine[0] - resS2_fine[2]
ok = abs(rF) > 1e-4
results["checks"].append({"name":"F3 NEGATIVE CONTROL S2: wrong IBP must FAIL","residual": float(abs(rF)),
                          "tol": 1e-4, "value": float(rF), "pass": bool(ok)})
print(f"[check] F3 NEGATIVE CONTROL S2: wrong-IBP residual = {abs(rF):.6e} (must be > 1e-4) -> {'PASS' if ok else 'FAIL'}", flush=True)

# ==================================================================
# bounds record + summary
# ==================================================================
elapsed = time.time() - _t0
maxrss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0 / 1024.0   # MiB
threads = threading.active_count()
results["bounds"] = {
    "declared": {"wall_s": 120, "mem_MB": 512, "threads": 1},
    "enforced": {
        "wall": f"timed; elapsed={elapsed:.2f}s, checked <=120",
        "memory": f"RLIMIT_AS soft cap {_MEM_BYTES//(1024*1024)} MB set; maxrss={maxrss:.1f} MiB measured",
        "threads": f"env caps OMP/OPENBLAS/MKL/NUMEXPR/VECLIB=1; active_count={threads}",
    },
    "elapsed_s": elapsed, "maxrss_MiB": maxrss, "active_threads": threads,
}
ok_wall = elapsed <= 120.0
ok_mem = maxrss <= 512.0
ok_thr = threads <= 1
results["bounds"]["pass"] = bool(ok_wall and ok_mem and ok_thr)
print(f"[bounds] elapsed={elapsed:.2f}s (<=120: {ok_wall})  maxrss={maxrss:.1f} MiB (<=512: {ok_mem})  threads={threads} (<=1: {ok_thr})", flush=True)

npass = sum(1 for c in results["checks"] if c["pass"])
nfail = sum(1 for c in results["checks"] if not c["pass"])
print(f"[summary] checks passed={npass} failed={nfail} bounds_ok={results['bounds']['pass']}", flush=True)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_output.json"), "w") as f:
    json.dump(results, f, indent=2)
sys.exit(0 if (nfail == 0 and results["bounds"]["pass"]) else 1)
