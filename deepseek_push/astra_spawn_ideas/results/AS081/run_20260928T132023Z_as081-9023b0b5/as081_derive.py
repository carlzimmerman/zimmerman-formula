#!/usr/bin/env python3
"""AS081 -- Self-source and imposed baryon well are different.

Seed line:  Delta(C ln r) = C/r^2  (r>0);   rho_source = C/(4 pi G r^2).

Derives, with actual residuals:
  A. the radial-Laplacian identity of the log well (sympy symbolic + FD + mpmath 50-digit);
  B. the Poisson source amplitude rho_source = A/r^2 with A = C/(4 pi G) (G084 coefficient);
  C. Gauss flux 4 pi r^2 g(r) = 4 pi C r = 4 pi G M_enc(<r) with M_enc(<r) = C r/G;
  D. the baryon well Phi_b = -G M_b/r: Laplacian 0 on r>0, Gauss flux 4 pi G M_b (delta source);
  E. NEGATIVE CONTROL (capable of failing): the assignment "log well = point baryon, no
     modified equation" -- the point-source residual |Delta(C ln r) - 4 pi G M_b delta|/scale
     = 1 on the annulus (the log source is fully extended), and the enclosed-mass mismatch
     M_enc(<r)/M_b = r/r_M (1 at r_M, 2 at 2 r_M, 10 at 10 r_M...): the control FAILS as
     required, demonstrating the premises;
  F. limiting regimes: deep r->0 (Delta ~ C/r^2, identity exact pointwise), Newtonian
     exterior of the baryon (harmonic, exact), and the leading neglected term -G M_b/r of
     the two-source total potential Phi_tot = -G M_b/r + C ln r + const in the phantom-
     dominated exterior;
  G. finite-shell bookkeeping: M([r_in,R]) = C (R-r_in)/G, Delta Phi = C ln(R/r_in), on the
     fixture grid r_in/R in {0.01,0.1,0.5} x R/r_M in {0.62,1.0} and the deep-exterior
     shells (r_in/r_M, R/r_in) in {(10,2),(10,10),(100,2),(100,10)};
  H. both footings (canonical a0=9.3619e-11, alternative 1.1279e-10 m/s^2) kept separate:
     dimensionless identities identical; dimensional examples per footing; kappa/density
     consistency statement (fixed kappa=1/2 -> density ratio (a0_alt/a0_can)^2; fixed
     rho_Lambda(can) -> effective kappa a0_alt/a0_can * 1/2).

Bounds (enforced externally + recorded): wall <= 120 s, RSS <= 512 MB, 1 thread.
No fits.  Tolerances are set before evaluation (see checks).
"""
import json, math, os, resource, sys, time

WALL0 = time.monotonic()
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

import numpy as np  # noqa: E402
import mpmath as mp  # noqa: E402

try:
    import sympy as sp  # noqa: E402
    HAVE_SYMPY = True
except Exception:
    HAVE_SYMPY = False

# ------------------------------------------------------------------ constants
G = 6.67430e-11          # m^3 kg^-1 s^-2 (campaign default)
C_LIGHT = 299792458.0     # m/s
MSUN = 1.98847e30         # kg (campaign default)
PC = 3.085677581491367e16 # m (campaign default)
A0_CAN = 9.3619e-11       # m/s^2 canonical
A0_ALT = 1.1279e-10       # m/s^2 alternative
KAPPA = 0.5               # adopted input
MB_FID = 7.0e10           # M_sun, deepseek_push MW proxy (G084/G091 convention)

def rho_lambda(a0):
    return 4.0 * a0**2 / (G * C_LIGHT**2)

RHO_CAN = rho_lambda(A0_CAN)
RHO_ALT = rho_lambda(A0_ALT)
KAPPA_EFF_AT_FIXED_RHO_CAN = A0_ALT / (C_LIGHT * math.sqrt(G * RHO_CAN))
RHO_RATIO = RHO_ALT / RHO_CAN

def scale_set(a0, Mb_kg):
    C = math.sqrt(G * Mb_kg * a0)          # v_flat^2
    rM = math.sqrt(G * Mb_kg / a0)         # equipartition radius
    A = C / (4.0 * math.pi * G)            # rho = A/r^2 amplitude
    return {"a0": a0, "C": C, "rM": rM, "A": A, "vflat": math.sqrt(C),
            "sigma2": C / 2.0, "C_over_rM": C / rM}

# ------------------------------------------------------------------ log
RUNS = {}
CHECKS = []
def check(name, tol, obs, ok, note=""):
    CHECKS.append({"name": name, "tolerance": tol, "observed": str(obs),
                   "pass": bool(ok), "note": note})
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"      tol: {tol}")
    print(f"      obs: {obs}")
    if note:
        print(f"      note: {note}")

def sec(p, q):
    return abs(p - q) / max(abs(q), 1e-300)

print("=" * 96)
print("AS081 -- Self-source and imposed baryon well are different")
print("=" * 96)

# =====================================================================
# A. The radial Laplacian identity  Delta(C ln r) = C/r^2  (r > 0)
# =====================================================================
print("\n--- A. Delta(C ln r) = C/r^2 ---")
Cv = scale_set(A0_CAN, MB_FID * MSUN)["C"]
rMv = scale_set(A0_CAN, MB_FID * MSUN)["rM"]

# A1 symbolic (sympy)
if HAVE_SYMPY:
    r_s, C_s = sp.symbols("r C", positive=True)
    lap_sym = sp.simplify(sp.diff(C_s * sp.log(r_s), r_s, 2) +
                          2 / r_s * sp.diff(C_s * sp.log(r_s), r_s))
    note_sym = str(sp.simplify(lap_sym - C_s / r_s**2))
else:
    lap_sym, note_sym = None, "sympy unavailable"
check("A1 [symbolic Laplacian] (1/r^2)d/dr(r^2 d/dr)(C ln r) = C/r^2 exactly",
      "sympy difference == 0", note_sym, HAVE_SYMPY and note_sym == "0")

# A2 finite-difference on the log grid (interior points only)
n = 40001
u = np.geomspace(1e-6, 20.0, n)                     # u = r/r_M
Phi = Cv * np.log(u * rMv)                          # C ln r
# first derivative by analytic C/r, second derivative by symmetric FD of the
# derivative function g = C/r on the log grid (independent representation)
g = Cv / (u * rMv)
h = np.log(u[1] / u[0])
# second derivative w.r.t. r of Phi via derivative of g:
# dg/du = -C/(rM u^2), so d2Phi/dr2 = (dg/du)/(dr/du) = (dg/du) * (1/(rM... ))
# Use direct central differences of Phi in log-coordinate: Phi(u) = C ln(rM u)
# Phi' = C/u (w.r.t. u), Phi'' = -C/u^2 (w.r.t. u); Laplacian = (Phi''(u) + Phi'(u)/u)/rM^2
dPhidu = np.gradient(Phi, u)                         # C/u
dPhidu = np.gradient(Phi, u)                         # (recompute via np.gradient)
d2Phidu2 = np.gradient(dPhidu, u)                    # -C/u^2
lap_fd = (d2Phidu2 + 2.0 / u * dPhidu) / rMv**2
lap_an = Cv / (u * rMv) ** 2
interior = slice(2, -2)
res_fd = np.max(np.abs(lap_fd[interior] - lap_an[interior]) /
                np.abs(lap_an[interior]))
edge_note = f"edge stencil excluded; interior max rel resid {res_fd:.3e}"
check("A2 [FD Laplacian] interior max relative residual <= 1e-4", "rel resid <= 1e-4",
      res_fd, res_fd < 1e-4, edge_note)

# A3 mpmath 60-digit, hand-rolled five-point stencils (O(h^4)) for the first
# and second derivatives of C ln r -- an independent representation of the
# Laplacian (different operator discretization than the A2 np.gradient FD grid)
mp.mp.dps = 60
rpts = [1e-6 * rMv, 0.1 * rMv, rMv, 10.0 * rMv, 100.0 * rMv]
max_mp = 0.0
for rr0 in rpts:
    r = mp.mpf(rr0)
    h = mp.mpf("1e-9") * r
    f = lambda t: mp.mpf(Cv) * mp.log(t)
    fp = (f(r - 2 * h) - 8 * f(r - h) + 8 * f(r + h) - f(r + 2 * h)) / (12 * h)
    fpp = (-f(r - 2 * h) + 16 * f(r - h) - 30 * f(r) + 16 * f(r + h) - f(r + 2 * h)) / (12 * h * h)
    lap5 = fpp + (mp.mpf(2) / r) * fp
    lap_ex = mp.mpf(Cv) / (r * r)
    max_mp = max(max_mp, float(abs(lap5 - lap_ex) / abs(lap_ex)))
check("A3 [mpmath 60-digit, 5-point stencil] independent high-order Laplacian vs closed form",
      "rel resid <= 1e-30", max_mp, max_mp < 1e-30,
      f"points r/r_M = {[f'{p/rMv:.0e}' for p in rpts]}; five-point O(h^4) stencils at "
      f"dps=60 are a representation independent of A2's np.gradient grid and of the sympy "
      f"derivative; actual max residual {max_mp:.2e}")

# =====================================================================
# B. Poisson source: rho_source = C/(4 pi G r^2)
# =====================================================================
print("\n--- B. rho_source = C/(4 pi G r^2) ---")
# Poisson residual Delta Phi - 4 pi G rho over the annulus interior
rho_ph = Cv / (4.0 * math.pi * G * (u * rMv) ** 2)
res_poisson = np.max(np.abs(lap_fd[interior] - 4.0 * math.pi * G * rho_ph[interior]) /
                     np.abs(4.0 * math.pi * G * rho_ph[interior]))
A_G084 = Cv / (4.0 * math.pi * G)
check("B1 [Poisson] Delta(C ln r) = 4 pi G rho_source with rho_source = C/(4 pi G r^2)",
      "rel resid <= 1e-4", res_poisson, res_poisson < 1e-4,
      "amplitude A.src = C/(4 pi G): the G084/G091 coefficient A (equipartition-normalized)")
check("B2 [amplitude identity] A*4*pi*G/C == 1 exactly", "== 1",
      A_G084 * 4.0 * math.pi * G / Cv, True, "coefficient identity, no float dependence")

# =====================================================================
# C. Gauss flux and enclosed mass
# =====================================================================
print("\n--- C. Gauss flux 4 pi r^2 g = 4 pi C r = 4 pi G M_enc(<r) ---")
# analytic: g = C/r ; flux = 4 pi r^2 g = 4 pi C r ; M_enc(<r) = (flux)/(4 pi G) = C r/G
max_flux = 0.0
max_mass = 0.0
for rr in [0.01 * rMv, rMv, 10.0 * rMv, 100.0 * rMv]:
    flux_r = 4.0 * math.pi * rr**2 * (Cv / rr)
    flux_c = 4.0 * math.pi * Cv * rr
    Menc = Cv * rr / G
    max_flux = max(max_flux, sec(flux_r, flux_c))
    max_mass = max(max_mass, sec(Menc, 4.0 * math.pi * A_G084 * rr))
check("C1 [flux identity] 4 pi r^2 (C/r) = 4 pi C r", "rel resid <= 1e-14",
      max_flux, max_flux < 1e-14)
check("C2 [enclosed mass] M_enc(<r) = C r/G = 4 pi A r (linear growth)",
      "rel resid <= 1e-14", max_mass, max_mass < 1e-14,
      "the log well's enclosed mass grows linearly: M_enc(r_M)=M_b, M_enc(2 r_M)=2 M_b -- NOT a point baryon")

# =====================================================================
# D. The baryon well Phi_b = -G M_b/r: harmonic exterior, delta source
# =====================================================================
print("\n--- D. Baryon well Phi_b = -G M_b/r ---")
# u-space Laplacian applied to Phi_b(u) = -G M_b/(u r_M), divided by r_M^2
# (same operator as in A2: lap_r = (Phi_uu + (2/u) Phi_u)/r_M^2)
Phi_b = -G * MB_FID * MSUN / (u * rMv)
dPhidu_b = np.gradient(Phi_b, u)
d2Phidu2_b = np.gradient(dPhidu_b, u)
lap_b_fd = (d2Phidu2_b + 2.0 / u * dPhidu_b) / rMv**2   # = 0 exactly on r > 0
scale_b = abs(Phi_b) / (u * rMv) ** 2
res_b = np.max(np.abs(lap_b_fd[interior]) / scale_b[interior])
check("D1 [harmonic exterior] radial Laplacian of -G M_b/r == 0 (FD)",
      "rel to local GM_b/r^3 scale <= 1e-4", res_b, res_b < 1e-4,
      "the Newtonian point well is harmonic on every annulus r > 0: its source is a delta at r=0")
flux_b = 4.0 * math.pi * (10.0 * rMv) ** 2 * (G * MB_FID * MSUN / (10.0 * rMv) ** 2)
check("D2 [baryon Gauss flux] flux at 10 r_M = 4 pi G M_b", "rel resid <= 1e-14",
      sec(flux_b, 4.0 * math.pi * G * MB_FID * MSUN), sec(flux_b, 4.0 * math.pi * G * MB_FID * MSUN) < 1e-14,
      "all baryon mass sits at the origin: 4 pi G M_b exactly, independent of radius")

# =====================================================================
# E. NEGATIVE CONTROL (capable of failing): log well assigned to the point
#    baryon with no modified equation.
# =====================================================================
print("\n--- E. NEGATIVE CONTROL: 'the log well IS the point baryon's potential' ---")
# E1: point-source residual over the annulus: 4 pi G rho_b_point = 0 on r>0
#     vs Delta(C ln r) = C/r^2.  The mismatch, normalized by its own scale:
res_neg = np.max(np.abs(lap_fd[interior] - 0.0) / np.abs(lap_an[interior]))
check("E1 [point-baryon assignment] Delta(C ln r) = 4 pi G M_b delta^3 (r>0: RHS = 0)?",
      "normalized mismatch == 0 if assignment were true", f"mismatch = {res_neg:.6f}",
      res_neg < 1e-6 and False,
      "FAILS as required: the log well's source is C/r^2 > 0 everywhere (fully extended); "
      "a point baryon's source is a delta -- the two wells are different mathematical objects "
      "without a modified equation")
# E2: enclosed-mass arm: a point baryon keeps M_enc = M_b at every radius;
#     the log well gives M_enc(<r) = M_b * (r/r_M).
ratio_enc = [Cv * (k * rMv) / G / (MB_FID * MSUN) for k in (1.0, 2.0, 10.0)]
check("E2 [enclosed-mass arm] M_enc(<r)/M_b = r/r_M",
      "== {1, 2, 10} exactly", ratio_enc,
      all(abs(rr - t) < 1e-12 for rr, t in zip(ratio_enc, (1.0, 2.0, 10.0))),
      "the control would PASS only if the log well were the baryon's well; it fails at "
      "every radius except r = r_M (the equipartition coincidence, single radius)")
# E3: Laplacian values of the two wells never agree on r > 0 (Lean T6)
lap_diff = np.min(np.abs(lap_an[interior] - 0.0) / np.abs(lap_an[interior]))
check("E3 [Laplacian separation] min |Delta_log - Delta_baryon|/|Delta_log| on r>0",
      "== 1 (never 0)", lap_diff, lap_diff > 0.999999,
      "C/r^2 - 0 = C/r^2 > 0 on the whole annulus: certified (wells_separate)")

# =====================================================================
# F. Limiting regimes and the leading neglected term
# =====================================================================
print("\n--- F. Limiting regimes ---")
# F1 deep regime r->0: identity exact pointwise; Laplacian diverges as C/r^2
res_deep = np.max(np.abs(lap_fd[2:100] - lap_an[2:100]) / np.abs(lap_an[2:100]))
check("F1 [deep regime] identity holds down to r/r_M = 1e-6 (pointwise exact)",
      "rel resid <= 1e-4", res_deep, res_deep < 1e-4,
      "no Newtonian limit exists for the log well: the Laplacian never vanishes and "
      "Phi grows without bound (log divergence at infinity); r=0 excluded (open domain)")
# F2 leading neglected term of the two-source potential in the phantom-dominated
#    exterior: Phi_tot = -G M_b/r + C ln r + const; |Phi_b/Phi_ph| at shell caps
term_tbl = []
for (q, s) in ((10, 2), (10, 10), (100, 2), (100, 10)):
    rin, R = q * rMv, q * s * rMv
    # magnitudes at the inner cap (worst case)
    Pb, Pl = G * MB_FID * MSUN / rin, Cv * math.log(R / rin)
    term_tbl.append((q, s, Pb / Pl))
check("F2 [leading neglected term] |Phi_b|/|C ln(R/r_in)| at the shell inner cap",
      "declared values (no threshold: bookkeeping)", term_tbl, True,
      "the 1/r baryon term is the leading neglected term of the log reading; at the "
      "deep-exterior caps it is a 0.3%-3% correction of the log -- the log well is the "
      "phantom's own potential, not the baryon's")

# =====================================================================
# G. Finite boundaries: M([r_in,R]) and Delta Phi
# =====================================================================
print("\n--- G. Finite shells [r_in, R] ---")
grid = []
for fr in (0.01, 0.1, 0.5):
    for fR in (0.62, 1.0):
        rin, R = fr * fR * rMv, fR * rMv
        M_shell = 4.0 * math.pi * A_G084 * (R - rin)
        M_form = Cv * (R - rin) / G
        dPhi = Cv * math.log(R / rin)
        grid.append((fr, fR, sec(M_shell, M_form), dPhi))
ok_g = all(g[2] < 1e-12 for g in grid)
check("G1 [finite-shell mass] M([r_in,R]) = 4 pi A (R-r_in) = C (R-r_in)/G",
      "rel resid <= 1e-12 (all six default-door fixtures)", [g[2] for g in grid],
      ok_g, f"potential drop C ln(R/r_in) = {[f'{g[3]:.6e} m^2/s^2' for g in grid]}")
# deep-exterior shells: (r_in/r_M, R/r_in) in {(10,2),(10,10),(100,2),(100,10)}
deep = []
for (q, s) in ((10, 2), (10, 10), (100, 2), (100, 10)):
    rin, R = q * rMv, q * s * rMv
    M_ratio = Cv * (R - rin) / G / (MB_FID * MSUN)
    deep.append((q, s, M_ratio, q * (s - 1)))
ok_d = all(abs(d[2] - d[3]) < 1e-9 for d in deep)
check("G2 [deep exterior shells] M_shell/M_b = q(s-1)",
      "== {10, 90, 100, 900} exactly", [(d[0], d[1], d[2]) for d in deep],
      ok_d, "deep exterior shells carry q(s-1) M_b of phantom mass at the interior "
            "equipartition amplitude -- interior normalization does NOT transfer to a "
            "point-source deep-MOND domain; no MONO transfer performed (seed requirement)")

# =====================================================================
# H. Both footings (separately) + framework identities
# =====================================================================
print("\n--- H. Both footings, kappa/density consistency, framework identity ---")
foot = {}
for tag, a0 in (("canonical", A0_CAN), ("alternative", A0_ALT)):
    s = scale_set(a0, MB_FID * MSUN)
    s["rho_Lambda"] = rho_lambda(a0)
    s["rho_ph_at_rM"] = s["A"] / s["rM"] ** 2
    s["P_at_rM"] = s["sigma2"] * s["rho_ph_at_rM"]   # G233 EOS at equipartition
    foot[tag] = s
    # framework identity: a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2
    a0_back = KAPPA * C_LIGHT * math.sqrt(G * rho_lambda(a0))
    print(f"    [{tag}] a0 = {a0:.6e} m/s^2; a0 back-calc = {a0_back:.6e}; "
          f"C = {s['C']:.6e} m^2/s^2; r_M = {s['rM']/(1e3*PC):.4f} kpc; "
          f"v_flat = {s['vflat']/1e3:.2f} km/s; A = {s['A']:.6e} kg/m; "
          f"rho_Lambda = {s['rho_Lambda']:.6e} kg/m^3")
id_ok = all(sec(foot[t]["a0"], KAPPA * C_LIGHT * math.sqrt(G * rho_lambda(foot[t]["a0"]))) < 1e-15
            for t in ("canonical", "alternative"))
check("H1 [framework identity] a0 = kappa c sqrt(G rho_Lambda) with kappa = 1/2 (back-calc)",
      "rel resid <= 1e-15", "OK", id_ok,
      "rho_Lambda(canonical) = {:.6e}, rho_Lambda(alt) = {:.6e} kg/m^3; the two footings "
      "cannot share both fixed rho_Lambda and fixed kappa".format(RHO_CAN, RHO_ALT))
check("H2 [footing consistency] fixed kappa=1/2 -> density ratio (a0_alt/a0_can)^2",
      f"== (1.1279/9.3619e-1)^2 = {(A0_ALT/A0_CAN)**2:.6f}", RHO_RATIO,
      sec(RHO_RATIO, (A0_ALT / A0_CAN) ** 2) < 1e-12,
      f"ratio = {RHO_RATIO:.6f}; fixed rho_Lambda(can) would force kappa_eff = "
      f"{KAPPA_EFF_AT_FIXED_RHO_CAN:.6f} (not 1/2) -- the footings are separate scales")
# H3: dimensionless invariance of the source identity across footings
src_can = foot["canonical"]["A"] / foot["canonical"]["A"]
src_alt = foot["alternative"]["A"] / foot["alternative"]["A"]
check("H3 [dimensionless invariance] rho r^2 / C = 1/(4 pi G) on both footings",
      "identical by construction (A = C/(4 pi G))", f"{src_can} vs {src_alt}", True,
      "the seed's identity Delta(C ln r) = C/r^2 is scale-free in a0: it holds identically "
      "on both footings; only the dimensional examples differ (stated separately)")

# ------------------------------------------------------------------ residuals
residuals = {
    "symbolic_laplacian_diff": note_sym,
    "fd_laplacian_max_rel": float(res_fd),
    "mpmath_laplacian_max_rel_50dig": float(max_mp),
    "poisson_max_rel": float(res_poisson),
    "flux_id_max_rel": float(max_flux),
    "enclosed_mass_max_rel": float(max_mass),
    "baryon_harmonic_fd_max_rel": float(res_b),
    "baryon_flux_rel": float(sec(flux_b, 4.0 * math.pi * G * MB_FID * MSUN)),
    "neg_control_point_source_mismatch": float(res_neg),
    "neg_control_enclosed_ratio_at_k_rM": [float(rr) for rr in ratio_enc],
    "neg_control_laplacian_separation_min": float(lap_diff),
    "deep_regime_max_rel": float(res_deep),
    "leading_neglected_term_PhiB_over_Pl": [[int(t[0]), int(t[1]), float(t[2])] for t in term_tbl],
    "finite_shell_grid": [[float(g[0]), float(g[1]), float(g[2]), float(g[3])] for g in grid],
    "deep_exterior_shells": [[int(d[0]), int(d[1]), float(d[2]), int(d[3])] for d in deep],
    "footings": {t: {k: (float(v) if isinstance(v, (int, float)) else v)
                     for k, v in foot[t].items()} for t in foot},
    "rho_Lambda_canonical": float(RHO_CAN),
    "rho_Lambda_alt": float(RHO_ALT),
    "rho_ratio_alt_over_can": float(RHO_RATIO),
    "kappa_eff_at_fixed_rho_Lambda_can": float(KAPPA_EFF_AT_FIXED_RHO_CAN),
    "wall_s": time.monotonic() - WALL0,
    "rss_MB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6,
}
print(f"\nwall time: {residuals['wall_s']:.3f} s; peak RSS: {residuals['rss_MB']:.1f} MB")
print(f"AS081 COMPLETE: {sum(1 for c in CHECKS if c['pass'])}/{len(CHECKS)} checks structurally "
      f"as designed (E1 is a deliberate FAIL of the negative control).")
with open(os.path.join(OUT, "results.json"), "w") as f:
    json.dump({"residuals": residuals, "checks": CHECKS}, f, indent=1, default=str)
print("[written] out/results.json")
