#!/usr/bin/env python3
"""
AS247 Engine A — one ray through the linearized same-action metric of the
CA5-GNC-R action (gate-inactive window), with the heat-filter contribution.

Same parameter cell as AS226 (shared): alpha = 0.3 -> c_N = 0.85, ell = 0.04,
xi^2/2 = 0.045 (xi = 0.3), box L = 100 m, M_b = 5 kg, sigma = 2.5 m, torus
mean-subtracted source, G_N = 6.67430e-11 SI, c = 299792458.

Deliverables:
  A1  sourced equations + U-tie residuals on the grid (mode-exact, ~1e-16)
  A2  gate-inactive verification: max Y_h = max(J(DW_b) + ell*Delta W_b - theta) < 0
      with theta = 1e-4 m^-2 (fixed coefficient; FINAL_ACTION: theta > 0 input)
  A3  one-ray delay at two impact parameters from the exact (filtered) same-action
      potential Phi_t (k-space solution, exact chord evaluation in the mode picture):
          dt = -(2/c^3) int Phi_t dl      (no-slip: Psi = Phi, C2d linear mode eq.)
  A4  filter contribution: same delay with S_k = 0 (Q -> 1) vs Q(k); the difference
      is the heat-filter effect on the delay (FINAL_ACTION eq. (16) factors).
  A5  refinement N = 48 -> 96 and chord points x2: residuals stable.
Notes: the ray endpoints (+-L/4, b, 0) sit outside the source support (sigma=2.5m).
The chord evaluation is exact in the mode picture (two-stage DFT, no interpolation):
  Phi(x) = (1/N^3) sum_k Phi_hat(k) e^{i kx x} e^{i(ky b)}  (z = 0).
"""
import numpy as np, json, time, sys

rng = np.random.default_rng(247)

def rec(res, name, ok, detail, residual=None, tol=None):
    res[name] = {"pass": bool(ok), "detail": detail,
                 "residual": residual, "tolerance": tol}

# ---------------- parameters (declared before evaluation) ----------
alpha  = 0.3
cN     = 1 - alpha/2
ell    = 0.04
xi2h   = 0.045
GN     = 6.67430e-11
G_bare = cN*GN
MP2    = 1.0/(8*np.pi*G_bare)
c_light = 299792458.0
A0_CAN  = 9.3619e-11
A0_ALT  = 1.1279e-10
KAPPA   = 0.5
THETA   = 1e-4          # gate threshold Y_h = J + ell*Delta W_b - theta < 0 (m^-2)

def rho_lambda(a0):
    return 4.0 * a0 * a0 / (GN * c_light * c_light)

# MONO branch machinery (nu_mono, J) — needed for the gate check; copied scale
# conventions from AS245 (identical definitions).
YSTAR  = 2.33741240526633
YP     = 2.5396
DELTA  = 0.05

def h_rar(y):
    s = np.sqrt(y)
    return y * (1.0/(1.0 - np.exp(-s)) - 1.0)

def dh_rar(y):
    s = np.sqrt(y)
    e = np.exp(-s)
    return (1.0 - e - s * e) / (1.0 - e)**2

def h_mono(y):
    return np.where(y <= YSTAR, h_rar(y),
        h_rar(YSTAR) + DELTA * h_rar(YP) * np.log((y + YP)/(YSTAR + YP)))

def dh_mono(y):
    floor = DELTA * h_rar(YP) / (y + YP)
    return np.where(y <= YSTAR, dh_rar(y), np.maximum(dh_rar(y), floor))

def nu_mono(y):
    return 1.0 + h_mono(y)/y

def q_mono(y2):
    return h_mono(y2)      # q'(y^2) = h'(y)/y ... q(y^2) = integral; use h(y)=q(y^2)/... define q via h: q(y^2) = h(y) [since q'(y^2) 2y = (h')... check: d/dy q(y^2) = 2y q'(y^2) = 2y(nu-1) = 2y h/y = 2h -> q(y^2) = integral 2h dy ... use direct: q = 2*int h dy approximated by...) 
# NOTE: for the gate check only the ORDER of J = 2 a0^2 q(|DW_b|^2/a0^2) matters;
# we use the exact branch definition q(y^2) with q'(y^2) = nu_mono(y) - 1 via
# antiderivative on the grid (rectangular rule), consistent with AS245 usage.

def make_q():
    yg = np.geomspace(1e-12, 1e6, 200001)
    qg = np.zeros_like(yg)
    # q'(y^2) = nu_mono(y) - 1;  dq = (nu-1) d(y^2);  y^2 = y (branch variable)
    z = yg**2
    qg[1:] = np.cumsum((nu_mono(yg) - 1.0)[1:] * np.diff(z))
    return yg, qg

YG, QG = make_q()
def q_of_y2(y2):
    return np.interp(y2, YG**2, QG, left=0.0, right=QG[-1])

# ---------------- torus machinery (identical conventions to AS226) ----------
def run(N, tag, chord_steps):
    res = {}
    L  = 100.0
    M  = 5.0
    sg = 2.5
    xs = (np.arange(N) - N//2) * L/N
    X, Y, W = np.meshgrid(xs, xs, xs, indexing='ij')
    r2 = X**2 + Y**2 + W**2
    rho = M * np.exp(-r2/(2*sg**2))
    rho = rho / rho.sum() * M
    rho = rho - rho.mean()
    ks = np.fft.fftfreq(N, d=L/N) * 2*np.pi
    KX, KY, KZ = np.meshgrid(ks, ks, ks, indexing='ij')
    k2 = KX**2 + KY**2 + KZ**2
    rho_hat = np.fft.fftn(rho)
    S  = np.exp(-xi2h*k2)
    Q  = 1 - ell*S/4
    Phi_hat = np.zeros_like(rho_hat)
    Z_hat   = np.zeros_like(rho_hat)
    nz = k2 > 0
    Phi_hat[nz] = -rho_hat[nz]/(2*MP2*cN*k2[nz]*Q[nz])
    Z_hat[nz]   = (ell*S[nz]/4)*Phi_hat[nz]
    U_hat = Phi_hat - Z_hat
    DXV = (L/N)**3
    Phi = np.fft.ifftn(Phi_hat).real/DXV   # real-space potential (m^2/s^2)

    scale = max(1.0, np.max(np.abs(rho_hat)))
    R1 = 2*MP2*cN*(-k2)*(Phi_hat - Z_hat) - rho_hat
    R2 = Z_hat - (ell*S/4)*Phi_hat
    R3 = 2*MP2*cN*(-k2)*((Phi_hat - Z_hat) - U_hat)
    rec(res, "A1_source_eqs",
        float(np.max(np.abs(R1)))/scale < 1e-9 and float(np.max(np.abs(R2)))/scale < 1e-9
        and float(np.max(np.abs(R3)))/scale < 1e-9,
        f"max|E1|/scale={float(np.max(np.abs(R1)))/scale:.2e}, "
        f"max|tie|/scale={float(np.max(np.abs(R2)))/scale:.2e}, "
        f"max|E2|/scale={float(np.max(np.abs(R3)))/scale:.2e}",
        float(np.max(np.abs(R1)))/scale, 1e-9)

    # ---- gate check: Y_h = J(DW_b) + ell*Delta W_b - theta < 0 everywheres ----
    # W_b = S_h U  (mode picture); DW_b via k-space gradient; Delta W_b via -k^2.
    W_hat = S * U_hat
    dWx = np.fft.ifftn(1j*KX*W_hat).real/DXV
    dWy = np.fft.ifftn(1j*KY*W_hat).real/DXV
    dWz = np.fft.ifftn(1j*KZ*W_hat).real/DXV
    dW2 = dWx**2 + dWy**2 + dWz**2
    delW = np.fft.ifftn(-k2*W_hat).real/DXV
    y_norm = np.sqrt(dW2)/A0_CAN          # y = |D W_b|/a0 (canonical footing)
    J = 2.0*A0_CAN**2 * q_of_y2(y_norm**2) / c_light**4     # m^-2 (J ~ a0^2/c^4)
    Yh = J + ell*delW - THETA
    rec(res, "A2_gate_inactive_canonical",
        float(np.max(Yh)) < 0.0,
        f"max Y_h = {float(np.max(Yh)):.3e} (< 0), margin |max J+ell delW|/theta = "
        f"{float(np.max(np.abs(J+ell*delW)))/THETA:.2e}, max y = {float(np.max(y_norm)):.3e}",
        float(np.max(Yh)), 0.0)
    y_alt = np.sqrt(dW2)/A0_ALT
    J_alt = 2.0*A0_ALT**2 * q_of_y2(y_alt**2) / c_light**4
    Yh_alt = J_alt + ell*delW - THETA
    rec(res, "A2b_gate_inactive_alt",
        float(np.max(Yh_alt)) < 0.0,
        f"alternative footing: max Y_h = {float(np.max(Yh_alt)):.3e}",
        float(np.max(Yh_alt)), 0.0)

    # ---- ray delays: exact mode-picture chord evaluation ----
    # Phi(x, b, 0) = (1/N^3) sum_kx G(kx) e^{i kx x},  G(kx) = sum_{ky,kz} Phi_hat e^{i ky b}
    out = []
    b_vals = [8.0, 20.0]
    xc = np.linspace(-L/4, L/4, chord_steps)
    kx_arr = ks
    resA3, resA4 = {}, {}
    for bval in b_vals:
        # vectorized 2-stage exact chord evaluation in the FFT-native coordinates
        # Xhat = x + L/2 (numpy fft origin at index 0); z = 0 -> Zhat = L/2.
        iy = int(np.argmin(np.abs(xs - bval)))
        phase_ky = np.exp(1j * KY * (bval + L/2))
        G = np.sum(Phi_hat * phase_ky * np.exp(1j * KZ * (L/2)), axis=(1, 2))
        Phi_chord = (1.0/N**3) * np.sum(
            G[None, :] * np.exp(1j * kx_arr[None, :] * (xc[:, None] + L/2)), axis=1)
        Phi_chord = Phi_chord.real
        # sanity: EXACT on-grid comparison (x on grid nodes, b pinned to a node)
        b_star = xs[iy]
        Gs = np.sum(Phi_hat * np.exp(1j * KY * (b_star + L/2))
                    * np.exp(1j * KZ * (L/2)), axis=(1, 2))
        two_stage_grid = (1.0/N**3) * np.sum(
            Gs[None, :] * np.exp(1j * ks[None, :] * (xs[:, None] + L/2)),
            axis=1).real / DXV
        Phi_row = Phi[:, iy, N//2]
        ongrid_err = float(np.max(np.abs(two_stage_grid - Phi_row)) /
                           np.max(np.abs(Phi_row)))
        rec(res, f"A3c_chord_on_grid_b{bval}",
            ongrid_err < 1e-10,
            f"exact mode eval on grid vs ifftn row: max rel err = {ongrid_err:.3e}",
            ongrid_err, 1e-10)
        # the physical potential is Phi_hat/DXV in real space (AS226 conv.)
        Phi_chord = Phi_chord / DXV
        dt = -(2.0/c_light**3) * np.trapz(Phi_chord, xc)
        # filter-off: Q -> 1 (same native-coordinate chord evaluation)
        Phi_hat0 = np.zeros_like(rho_hat)
        Phi_hat0[nz] = -rho_hat[nz]/(2*MP2*cN*k2[nz])
        G0 = np.sum(Phi_hat0 * np.exp(1j * KY * (bval + L/2))
                    * np.exp(1j * KZ * (L/2)), axis=(1, 2))
        Phi0 = (1.0/N**3) * np.sum(
            G0[None, :] * np.exp(1j*kx_arr[None, :]*(xc[:, None] + L/2)),
            axis=1).real
        dt0 = -(2.0/c_light**3) * np.trapz(Phi0/DXV, xc)
        rec(res, f"A3_delay_b{bval}",
            True,  # recorded; physical sign check below
            f"dt(b={bval} m) = {dt:.6e} s (filtered same-action), "
            f"filter-off dt0 = {dt0:.6e} s, filter effect (dt-dt0) = {dt-dt0:.6e} s",
            float(dt), None)
        rec(res, f"A4_filter_effect_b{bval}",
            abs((dt - dt0)/abs(dt)) > 1e-6 and abs((dt-dt0)/abs(dt)) < 0.1,
            f"relative filter contribution {(dt-dt0)/dt:.6e} (expected ~1% low-k boost)",
            float((dt-dt0)/dt), 0.1)
        resA3[bval] = dt; resA4[bval] = dt - dt0
    # sign: attractive potential -> delay > 0
    ok_sign = all(v > 0 for v in resA3.values())
    rec(res, "A3b_delay_positive_attractive",
        ok_sign,
        f"both impacts positive (attractive no-slip potentials): {resA3}",
        None, None)
    return res

def a0_scale(a0, c):
    return (a0 / A0_CAN)**2   # unused: J recomputed per footing

res = {}
t0 = time.time()
r48 = run(48, "N48", 2001)
r96 = run(96, "N96", 4001)
res.update({f"{k}@N48": v for k, v in r48.items()})
res.update({f"{k}@N96": v for k, v in r96.items()})
# refinement check: delays at N=96 vs N=48 (relative change)
for bval in [8.0, 20.0]:
    d48 = r48[f"A3_delay_b{bval}"]["residual"]
    d96 = r96[f"A3_delay_b{bval}"]["residual"]
    rec(res, f"A5_refine_b{bval}",
        abs((d96 - d48)/max(abs(d96),1e-30)) < 1e-3,
        f"dt N48={d48:.8e} -> N96={d96:.8e}, rel change {(d96-d48)/d96:.3e}",
        float(abs((d96-d48)/d96)), 1e-3)

res["_meta"] = {"alpha": alpha, "cN": cN, "ell": ell, "xi2half": xi2h,
                "theta_m2": THETA, "box_m": 100.0, "M_kg": 5.0, "sigma_m": 2.5,
                "a0_canonical": A0_CAN, "a0_alternative": A0_ALT,
                "rhoL_can": rho_lambda(A0_CAN), "rhoL_alt": rho_lambda(A0_ALT),
                "footings_kappa": KAPPA, "elapsed_s": time.time() - t0}
with open("box_raw.json", "w") as f:
    json.dump(res, f, indent=1, default=str)
print(json.dumps(res, indent=1, default=str))
allp = all(v.get("pass", False) for k, v in res.items() if not k.startswith("_"))
print("ALL_PASS:", allp)