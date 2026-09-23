#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L313 -- STOCHASTIC-METRIC RECTIFICATION AS THE PHANTOM: postquantum classical gravity priced on the
framework's own gates (the coefficient, the shape, and lensing = dynamics derived from the Einstein tensor).

WHY THIS LANE.  The repository never engaged the one external theory that claims the framework's central
tie.  Oppenheim & Russo 2024 (arXiv:2402.19459; "OR24") argue that in postquantum classical gravity
(Oppenheim, PRX 13, 041040, 2023) the metric must diffuse, and that the diffusion produces a MOND-scale
term with a0 ~ sqrt(Lambda).  Hertzberg & Loeb 2024 (JCAP 09, 046; arXiv:2404.13037) reply that the
Gaussian mean equation is only del^4 Phi = 4 pi G del^2 rho, so the linear term is not a free solution and
is not MONDian.  The corpus's own no-gos bracket this exactly: 2026-08-09 (rectification needs a
NONLINEARITY -- linear EOMs pass only the first cumulant) and 2026-09-01 / KS01 (quantum graviton noise is
O(hbar), ~1e-124 of what is needed).  Classical metric noise is NOT hbar-suppressed, so it is the one
escape of the hbar-counting theorem.  This lane asks the honest question the swarm never asked:

    If the phantom IS the rectified variance of a stochastic metric, what coefficient does the published
    theory give, and does the rectified source lens the way it attracts?

METHOD (derive the observable from the equations -- the L268/L274 discipline).
  Metric ds^2 = -(1+2 Phi)dt^2 + (1-2 Psi)dx^2 with Phi = Phibar + phi, Psi = Psibar + psi, (phi, psi)
  zero-mean random fields.  Averaging the exact field equations in the short-wavelength limit (the Isaacson /
  Green-Wald regime: correlation length << the scale on which the variance varies), the mean metric obeys
  the LINEAR equations with an effective source 8 pi G T^eff = -<G^(2)[phi,psi]>.  Then, for the static mean,
      dynamics  (lapse)     : lap Phibar          = 4 pi G (rho + rho_eff + (p_r + 2 p_t))
      lensing  (Phi+Psi)/2  : lap (Phibar+Psibar)/2 = 4 pi G (rho + rho_eff + (p_r + 2 p_t)/2)
  so the phantom's lensing/dynamics ratio is set by eps = (p_r+2p_t)/rho_eff alone (sf38 PART A: the only
  weak-field-observable piece of the stress).  The corpus's gate: |eps| < 0.0489 at 1 sigma (sf38, from the
  Brouwer+2021 KiDS-1000 full covariance, sigma(amplitude) = 2.36%).

  The averaged tensors are computed symbolically for one Fourier mode (phase-averaged) and are scalars under
  rotations, so every result holds for ANY directional distribution of the noise, and a mixture of modes
  can never beat the best single mode (ratio of sums >= min ratio when every trace term has one sign).

CONTROLS (must pass before any finding is read):
  C0a Isaacson: a TT plane wave gives -<G^(2)_00> = A^2 k^2/4 = 8 pi G t_00, t_zz = t_00, t_xx = t_yy = 0.
  C0b exact isotropic Schwarzschild: G_mu_nu = 0 numerically (the Einstein routine itself).
  C0c first order: G^(1)_00 = 2 lap psi, trace G^(1)_ij = 2 lap(phi - psi) (static).
  C0d rotation-scalars: the static mode along x and along z give identical <G00> and trace.
  MUTATE=1 drops the Gamma*Gamma terms of the Ricci tensor: C0a/C0b must FAIL (rc != 0); its JSON is
  written to a separate file (feedback: mutation runs write separate outputs).

Run from the repository root:  python3 real_research/cq_gravity_2026/L313_cq_rectification_lensing.py
"""
import os, sys, json, math
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L313_cq_rectification_lensing"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L313", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 104); P(t); P("=" * 104)


# ------------------------------------------------------------------------------------------------ inputs
c_SI, G_SI = 2.99792458e8, 6.67430e-11
MPC = 3.0856775814913673e22
H0, OMEGA_L = 67.4, 0.685                       # the corpus's canonical Planck footing
H0_SI = H0 * 1e3 / MPC
HL_SI = H0_SI * math.sqrt(OMEGA_L)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
KAPPA_A, SIG_A = 0.465, 0.076                    # estimator A (BTFR intercept), MNRAS v2
KAPPA_B, SIG_B = 0.55, 0.17                      # estimator B (shape-only), MNRAS v2 corrected
SQ = math.sqrt(8 * math.pi / 3)                  # kappa = SQ * a0/(c H_Lambda)

# the lensing tolerance, read from the committed sf38 source so it cannot drift silently
SF38 = os.path.join(REPO, "qwen_claude_field_theory", "closure_2026", "sf38_lensing_tolerance_2026.py")
SIG_AMP, EPS_TOL = 0.0236, 0.0489
sf38_txt = open(SF38).read() if os.path.exists(SF38) else ""
# the committed lensing-RAR slope below 1e-13 m/s^2 (Brouwer+2021, full covariance), L248
L248 = json.load(open(os.path.join(REPO, "fable_independent_2026", "L248_results.json")))
SLOPE_LOW, SLOPE_ERR = L248["slope_low"], L248["slope_low_err"]

# ------------------------------------------------------------------------------------------------ machinery
t, x, y, z = sp.symbols("t x y z", real=True)
X = [t, x, y, z]
eps = sp.Symbol("eps")
th = sp.Symbol("theta", real=True)


def einstein(g):
    ginv = g.inv()
    n = 4
    Gam = [[[sum(ginv[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d]))
                 for d in range(n)) / 2 for c in range(n)] for b in range(n)] for a in range(n)]
    Ric = sp.zeros(n)
    for b in range(n):
        for c in range(n):
            r = sum(sp.diff(Gam[a][b][c], X[a]) for a in range(n)) - sum(sp.diff(Gam[a][b][a], X[c]) for a in range(n))
            if not MUTATE:
                r += sum(Gam[a][a][d] * Gam[d][b][c] for a in range(n) for d in range(n)) \
                    - sum(Gam[a][c][d] * Gam[d][b][a] for a in range(n) for d in range(n))
            Ric[b, c] = r
    R = sum(ginv[a, b] * Ric[a, b] for a in range(n) for b in range(n))
    return Ric - g * R / 2


def order(expr, k):
    return sp.series(expr, eps, 0, k + 1).removeO().coeff(eps, k)


def phase_avg(e):
    e2 = sp.expand(order(e, 2))
    return sp.simplify(sp.integrate(e2, (th, 0, 2 * sp.pi)) / (2 * sp.pi))


P(__doc__)

# =========================================================================================== 0 controls
banner("0  CONTROLS -- the Einstein routine and the averaging reproduce known results")
A_, k_ = sp.symbols("A k", positive=True)
h = A_ * sp.cos(k_ * (z - t) + th)
G_tt = einstein(sp.diag(-1, 1 + eps * h, 1 - eps * h, 1))
iso = {ij: phase_avg(G_tt[ij]) for ij in [(0, 0), (1, 1), (2, 2), (3, 3)]}
target = A_**2 * k_**2 / 4
okA = (sp.simplify(-iso[(0, 0)] - target) == 0 and sp.simplify(-iso[(3, 3)] - target) == 0
       and sp.simplify(iso[(1, 1)]) == 0 and sp.simplify(iso[(2, 2)]) == 0)
check("C0a Isaacson: TT wave gives 8 pi G t_00 = 8 pi G t_zz = A^2 k^2/4, t_xx = t_yy = 0",
      {k: str(v) for k, v in iso.items()}, okA,
      "the second-order Einstein tensor + phase averaging reproduces the standard GW stress (w = 1/3 isotropised)")

m_ = sp.Symbol("m", positive=True)
r_ = sp.sqrt(x**2 + y**2 + z**2)
gS = sp.diag(-((1 - m_ / (2 * r_)) / (1 + m_ / (2 * r_)))**2, *([(1 + m_ / (2 * r_))**4] * 3))
GS = einstein(gS)
pts = [(0.7, -0.4, 1.1), (2.0, 0.3, -0.5), (-1.3, 1.7, 0.9)]
res = []
for (px, py, pz) in pts:
    sub = {m_: 0.3, x: px, y: py, z: pz}
    res.append(max(abs(float(GS[i, j].subs(sub).evalf())) for i in range(4) for j in range(4)))
check("C0b exact isotropic Schwarzschild satisfies G_mu_nu = 0 (the routine itself)",
      f"max |G| over 3 points = {max(res):.2e}", max(res) < 1e-10)

PHI, PSI = sp.Function("phi")(x, y, z), sp.Function("psi")(x, y, z)
G1 = einstein(sp.diag(-(1 + 2 * eps * PHI), *([1 - 2 * eps * PSI] * 3)))
lap = lambda f: sum(sp.diff(f, v, 2) for v in (x, y, z))
g1_00 = sp.simplify(order(G1[0, 0], 1) - 2 * lap(PSI))
g1_tr = sp.simplify(sum(order(G1[i, i], 1) for i in (1, 2, 3)) - 2 * lap(PHI - PSI))
check("C0c first order: G(1)_00 = 2 lap psi and trace G(1)_ij = 2 lap(phi - psi)",
      f"residuals {g1_00}, {g1_tr}", g1_00 == 0 and g1_tr == 0)

a_, b_, dl = sp.symbols("a b delta", real=True)
om = sp.Symbol("omega", real=True)
kk = sp.Symbol("kk", positive=True)


def mode_tensors(axis, omega=0):
    coord = [x, y, z][axis]
    ph = kk * coord - omega * t + th
    g = sp.diag(-(1 + 2 * eps * a_ * sp.cos(ph)), *([1 - 2 * eps * b_ * sp.cos(ph + dl)] * 3))
    G = einstein(g)
    ginv = g.inv()
    return g, G, ginv


def conv_rho_trace(g, G, ginv):
    """8 pi G rho_eff and 8 pi G (p_r + 2 p_t) under four averaging conventions."""
    mixed = ginv * G
    upper = ginv * G * ginv
    dens = sp.sqrt(-g.det()) * mixed
    out = {}
    out["lower (Einstein-Langevin <G_mn>)"] = (-phase_avg(G[0, 0]), -phase_avg(G[1, 1] + G[2, 2] + G[3, 3]))
    out["mixed <G^m_n>"] = (phase_avg(mixed[0, 0]), -phase_avg(mixed[1, 1] + mixed[2, 2] + mixed[3, 3]))
    out["densitized <sqrt(-g) G^m_n>"] = (phase_avg(dens[0, 0]), -phase_avg(dens[1, 1] + dens[2, 2] + dens[3, 3]))
    out["upper <G^mn>"] = (-phase_avg(upper[0, 0]), -phase_avg(upper[1, 1] + upper[2, 2] + upper[3, 3]))
    return out


gx, Gx, gix = mode_tensors(0)
gz, Gz, giz = mode_tensors(2)
low_x = (-phase_avg(Gx[0, 0]), -phase_avg(Gx[1, 1] + Gx[2, 2] + Gx[3, 3]))
low_z = (-phase_avg(Gz[0, 0]), -phase_avg(Gz[1, 1] + Gz[2, 2] + Gz[3, 3]))
okD = sp.simplify(low_x[0] - low_z[0]) == 0 and sp.simplify(low_x[1] - low_z[1]) == 0
check("C0d rho_eff and p_r+2p_t are rotation scalars (mode along x == mode along z)",
      f"x: {low_x}; z: {low_z}", okD,
      "=> every bound below holds for ANY directional structure of the noise")

if MUTATE:
    # the mutation breaks the Einstein routine itself; the controls must catch it, and nothing downstream is read
    n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    with open(os.path.join(HERE, f"{SLUG}_results_MUTATE.json"), "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    P(f"\n  MUTATE: {n_fail} control(s) failed as required; downstream sections not run")
    sys.exit(0 if n_fail == 0 else 1)

# =========================================================================================== A  OR24
banner("A  THE PUBLISHED COEFFICIENT -- OR24's conditional mean, in the framework's kappa")
beta = sp.Symbol("beta", real=True)
f_beta = (1 - 4 * beta) / (5 - 18 * beta)
# OR24 eq.(20): mu_gamma1 = -(9/2) gamma2 r_max f_beta; eq.(18): -g_tt = 1 - 2GM/r - gamma1 r - gamma2 r^2
# => Phi = -GM/r - gamma1 c^2 r/2 - gamma2 c^2 r^2/2 => a constant inward acceleration a_g = |gamma1| c^2/2.
# gamma2 = Lambda/3 = H_L^2/c^2, r_max = c/H_L (de Sitter radius): a_g/(c H_L) = (9/4) f_beta.
ratio_dS = sp.Rational(9, 4) * f_beta
kap_direct = sp.sqrt(8 * sp.pi / 3) * ratio_dS
k0 = float(kap_direct.subs(beta, 0))
kinf = float(sp.limit(kap_direct, beta, -sp.oo))
OUT["numbers"]["OR24_kappa_direct_beta0"] = k0
OUT["numbers"]["OR24_kappa_direct_beta_minus_inf"] = kinf
zA = (min(k0, kinf) - KAPPA_A) / SIG_A
zB = (min(k0, kinf) - KAPPA_B) / SIG_B
check("A1 OR24 read as a0 := |gamma1| c^2/2 (r_max = de Sitter radius), completely positive beta < 0: "
      "kappa lies in (%.4f, %.4f)" % (k0, kinf),
      f"kappa range {k0:.4f}..{kinf:.4f} vs measured A {KAPPA_A}+/-{SIG_A} (>= {zA:.1f} sigma), "
      f"B {KAPPA_B}+/-{SIG_B} (>= {zB:.1f} sigma)", zA > 5,
      "the published CQ route lands a factor 2.8-3.1 above the measured coefficient")
b_half = sp.solve(sp.Eq(kap_direct, sp.Rational(1, 2)), beta)[0]
OUT["numbers"]["OR24_beta_for_kappa_half"] = float(b_half)
check("A2 kappa = 1/2 requires beta = %.4f: inside OR24's positivity (beta <= 1/3) but OUTSIDE complete "
      "positivity (beta < 0)" % float(b_half), f"beta = {sp.nsimplify(b_half)} = {float(b_half):.5f}",
      0 < float(b_half) < sp.Rational(1, 3),
      "the framework's number is reachable only by giving up the condition OR24 need for positive correlations")
Mg, Gg, ag, rr = sp.symbols("M G a_g r", positive=True)
v2 = Gg * Mg / rr + ag * rr
rstar = sp.solve(sp.diff(v2, rr), rr)[0]
v4min = sp.simplify(v2.subs(rr, rstar)**2)
kap_btfr_inf = sp.limit(4 * kap_direct, beta, -sp.oo)
Zexact = sp.sqrt(sp.Rational(32, 3) * sp.pi)
check("A3 BTFR-matched reading: v^4 at the flattest point = 4 G M a_g exactly; at beta -> -inf the matched "
      "a0 = 2 c H_Lambda, i.e. kappa = Z = sqrt(32 pi/3) (Milgrom 1999 / Deser-Levin, excluded 15.6 sigma)",
      f"v^4_min = {v4min}; kappa_BTFR(beta->-inf) = {kap_btfr_inf} = {float(kap_btfr_inf):.5f}",
      sp.simplify(v4min - 4 * Gg * Mg * ag) == 0 and sp.simplify(kap_btfr_inf - Zexact) == 0)
kH = [k0 * math.sqrt(OMEGA_L), kinf * math.sqrt(OMEGA_L)]
check("A4 r_max = c/H0 (OR24's 'Hubble radius') instead of the de Sitter radius: kappa in (%.3f, %.3f)" % tuple(kH),
      f"still {(kH[0]-KAPPA_A)/SIG_A:.1f} sigma above estimator A", (kH[0] - KAPPA_A) / SIG_A > 5)
gb = sp.Symbol("g_b", positive=True)
slope_const = sp.limit(sp.diff(sp.log(gb + ag), gb) * gb, gb, 0)
zslope = (SLOPE_LOW - float(slope_const)) / SLOPE_ERR
check("A5 SHAPE: a constant extra acceleration gives a lensing-RAR slope d ln g_obs/d ln g_bar -> %s at "
      "g_bar << a_g, vs the committed KiDS slope %.3f +/- %.3f (L248)" % (slope_const, SLOPE_LOW, SLOPE_ERR),
      f"{zslope:.1f} sigma", zslope > 5,
      "independently of the coefficient, a gamma_1 r term is not the deep-MOND law (Hertzberg-Loeb's point, measured)")
R3 = sp.Symbol("R", positive=True)
flux = sp.simplify(4 * sp.pi * R3**2 * sp.diff(2 / R3, R3))
lap_r = sp.simplify(sp.diff(R3**2 * sp.diff(R3, R3), R3) / R3**2)
check("A6 Hertzberg-Loeb: lap r = 2/r and the flux of grad(2/r) is -8 pi, so del^4 r = -8 pi delta^3: the linear "
      "term needs a point source in del^2 rho -- it is not a free homogeneous solution",
      f"lap r = {lap_r}; flux = {flux}", lap_r == 2 / R3 and flux == -8 * sp.pi)

# =========================================================================================== B  lensing
banner("B  DOES A RECTIFIED PHANTOM LENS AS IT ATTRACTS?  (derived from <G^(2)>, gate |eps| < 0.0489 @ 1 sigma)")
ok_sf38 = ("2.36%" in sf38_txt) and ("0.0489" in sf38_txt)
check("B0 the gate is read from the committed sf38 source (sigma_amp = 2.36%, |eps| < 0.0489 at 1 sigma)",
      f"sf38 present: {bool(sf38_txt)}; numbers found: {ok_sf38}", ok_sf38)


def LD(e):          # lensing/dynamics mass ratio of the phantom for eps = (p_r+2p_t)/rho
    return (1 + e / 2) / (1 + e)


def nsig(e):
    return abs(LD(e) - 1) / SIG_AMP


eT = 1.0             # TT noise (C0a): p = rho/3 isotropised -> (p_r+2p_t)/rho = 1
check("B1 GR-COMPLIANT noise (vacuum fluctuations can only be TT waves; Isaacson, Green-Wald): eps = +1, "
      "lensing/dynamics = %.3f -> excluded at %.1f sigma (convention-independent: <delta g . G(1)> = 0 in vacuum)"
      % (LD(eT), nsig(eT)), f"L/D = {LD(eT):.4f}", nsig(eT) > 5,
      "any phantom carried by propagating gravitational-wave energy is dead on KiDS -- incl. every quantum-"
      "graviton bath route, independently of its 1e-124 size")

u, cc = sp.symbols("u c", real=True)
conv = conv_rho_trace(gx, Gx, gix)
norm = b_**2 * kk**2 / 2           # S_psipsi := <|grad psi|^2> = 1
forms = {}
for name, (Rr, Nn) in conv.items():
    Rn = sp.expand(sp.simplify((Rr.subs(sp.cos(dl), cc) / norm).subs(a_, u * b_)))
    Nn2 = sp.expand(sp.simplify((Nn.subs(sp.cos(dl), cc) / norm).subs(a_, u * b_)))
    forms[name] = (Rn, Nn2)
    P(f"    {name:34s}  8piG rho_eff = {Rn}   8piG(p_r+2p_t) = {Nn2}")
OUT["numbers"]["forms"] = {k: [str(v[0]), str(v[1])] for k, v in forms.items()}

RL, NL = forms["lower (Einstein-Langevin <G_mn>)"]
# p_r + 2p_t <= 0: -N = S_phiphi + <|grad(phi - psi)|^2> (in units of S_psipsi)
psd = sp.expand(-NL - (u**2 + (u**2 - 2 * cc * u + 1)))
check("B2a lower-index (Einstein-Langevin): -(p_r+2p_t) 8piG = S_phiphi + <|grad(phi-psi)|^2> >= 0 -- the "
      "rectified stress is NEVER positive", f"residual of the identity = {psd}", psd == 0,
      "static scalar noise always has negative isotropic pressure")
epsL = sp.simplify(NL / RL)
uopt = (sp.sqrt(53) - 5) / 4
e_min = sp.nsimplify(sp.simplify(-epsL.subs({cc: 1, u: uopt})))
e_min_f = float(e_min)
# numerical confirmation of the global minimum over u >= 0, c in [-1, 1] with rho > 0 and rho + (p_r+2p_t) > 0
fR = sp.lambdify((u, cc), RL, "numpy"); fN = sp.lambdify((u, cc), NL, "numpy")
U, C = np.meshgrid(np.linspace(0, 6, 1201), np.linspace(-1, 1, 801))
Rg, Ng = fR(U, C), fN(U, C)
mask = (Rg > 1e-9) & (Rg + Ng > 1e-9)
grid_min = float(np.min(np.abs(Ng[mask] / Rg[mask])))
OUT["numbers"]["lower_min_abs_eps"] = e_min_f
check("B2b lower-index static scalar noise: min |eps| = %.5f (exact at phi = u* psi, u* = (sqrt 53 - 5)/4 = %.4f, "
      "perfectly correlated); grid confirms %.5f" % (e_min_f, float(uopt), grid_min),
      f"min |eps| = {sp.simplify(e_min)} = {e_min_f:.5f}; L/D = {LD(-e_min_f):.4f} -> {nsig(-e_min_f):.2f} sigma "
      f"(first-order sf38 mapping {e_min_f/EPS_TOL:.2f})", abs(grid_min - e_min_f) < 2e-4 and e_min_f > EPS_TOL,
      "a static-noise phantom must LENS >= %.1f%% MORE than it attracts -- a registered sign and floor, "
      "but only %.1f sigma on KiDS today: NOT excluded" % (100 * (LD(-e_min_f) - 1), nsig(-e_min_f)))
eOR = float(epsL.subs({cc: 1, u: 1}))
OUT["numbers"]["OR24_ansatz_eps"] = eOR
check("B2c OR24's single-potential ansatz (phi = psi): eps = %.4f = -1/9, lensing excess %.2f%% (%.1f sigma)"
      % (eOR, 100 * (LD(eOR) - 1), nsig(eOR)), f"eps = {sp.nsimplify(eOR)}", abs(eOR + 1 / 9) < 1e-12)
Rl0 = sp.limit(RL / u**2, u, sp.oo); Nl0 = sp.limit(NL / u**2, u, sp.oo)
check("B2d pure LAPSE noise (psi = 0): rho_eff = 0 and the active source rho + (p_r+2p_t) = -2 S_phiphi < 0 -- "
      "REPULSIVE: noise in the Newtonian potential alone rectifies to ANTI-MOND",
      f"per S_phiphi: 8piG rho = {Rl0}, 8piG(rho+p_r+2p_t) = {Rl0 + Nl0}", Rl0 == 0 and Rl0 + Nl0 < 0)

# convention systematic
rows = {}
for name, (Rn, Nn2) in forms.items():
    fR = sp.lambdify((u, cc), Rn, "numpy"); fN = sp.lambdify((u, cc), Nn2, "numpy")
    Rg, Ng = fR(U, C) * np.ones_like(U), fN(U, C) * np.ones_like(U)
    act = Rg + Ng
    mask = (Rg > 1e-9) & (act > 1e-9)
    rows[name] = {"identically_no_active_mass": bool(sp.simplify(Rn + Nn2) == 0),
                  "min_abs_eps": (float(np.min(np.abs(Ng[mask] / Rg[mask]))) if mask.any() else None)}
OUT["numbers"]["convention_table"] = rows
P("    convention systematic (static scalar noise):")
for k, v in rows.items():
    P(f"      {k:34s} min|eps| = {v['min_abs_eps']}   no-active-mass identity: {v['identically_no_active_mass']}")
spread = [v["min_abs_eps"] for v in rows.values() if v["min_abs_eps"] is not None]
dens_dead = rows["densitized <sqrt(-g) G^m_n>"]["identically_no_active_mass"]
check("B3 CONVENTION SYSTEMATIC: for noise that violates the linear constraint (the CQ case), <G_mn>, <G^m_n>, "
      "<sqrt(-g)G^m_n>, <G^mn> differ at the SAME order as the effect",
      f"min|eps| across conventions = {[round(s, 4) for s in spread]}; densitized: rho + (p_r+2p_t) == 0 "
      f"identically = {dens_dead}", dens_dead and (max(spread) - min(spread)) > 0.05,
      "the lensing of a CQ phantom is NOT fixed by GR averaging: CQ gravity must say which density its noise is "
      "unbiased in (" + "; ".join(f"{k.split(' ')[0]}: " + ("no active mass" if v["identically_no_active_mass"]
      else f"min|eps| {v['min_abs_eps']:.4f}") for k, v in rows.items()) + ") -- the missing theory input, named")

# time-dependent noise, lower convention
gt_, Gt_, git_ = mode_tensors(0, omega=om)
Rt = -phase_avg(Gt_[0, 0]); Nt = -phase_avg(Gt_[1, 1] + Gt_[2, 2] + Gt_[3, 3])
Rt1 = sp.simplify(Rt.subs({a_: b_, sp.cos(dl): 1})); Nt1 = sp.simplify(Nt.subs({a_: b_, sp.cos(dl): 1}))
act_white = sp.limit((Rt1 + Nt1) / om**2, om, sp.oo).subs(b_, 1)
OUT["numbers"]["time_dep_lower"] = [str(Rt), str(Nt)]
check("B4 OR24's Newtonian limit is white in time (no d/dt in the action): phi = psi with omega >> c k gives an "
      "active source -> %s b^2 omega^2 < 0 -- REPULSIVE" % act_white,
      f"8piG rho = {Rt1}; 8piG(p_r+2p_t) = {Nt1}", act_white < 0,
      "taken literally through the full averaged tensor, the published noise pushes the wrong way; the "
      "attractive reading needs quasi-static noise (omega << c k)")

# the mixture window (lower): static optimum + a fast anti-correlated component can null eps
Nfast = sp.simplify((Nt.subs(sp.cos(dl), -1).subs(a_, b_)) / (b_**2 * om**2 / 2))   # per D_psipsi, kk->0 part
Nfast = sp.limit(Nfast.subs(kk, 0), om, sp.oo) if Nfast.has(kk) else Nfast
Rfast = sp.simplify((Rt.subs(sp.cos(dl), -1).subs(a_, b_)).subs(kk, 0) / (b_**2 * om**2 / 2))
Rs, Ns = float(RL.subs({u: uopt, cc: 1})), float(NL.subs({u: uopt, cc: 1}))
Rf, Nf = float(Rfast), float(Nfast)
w0 = -Ns / Nf if Nf != 0 else float("nan")
lo = [w for w in np.linspace(0, 3 * abs(w0) + 1, 30001)
      if (Rs + w * Rf) > 0 and (Rs + w * Rf + Ns + w * Nf) > 0 and nsig((Ns + w * Nf) / (Rs + w * Rf)) <= 1.0]
OUT["numbers"]["mixture_window"] = [min(lo), max(lo)] if lo else None
check("B5 MIXTURE: the static optimum plus a fast anti-correlated (phi = -psi) component nulls p_r+2p_t with "
      "rho > 0 -- lensing = dynamics is REACHABLE, at weight w0 = %.3f (1-sigma window %s)" %
      (w0, f"[{min(lo):.3f}, {max(lo):.3f}]" if lo else "empty"),
      f"per unit S_psipsi: static (rho, trace) = ({Rs:.3f}, {Ns:.3f}); fast per D_psipsi = ({Rf:.1f}, {Nf:.1f})",
      bool(lo) and min(lo) < w0 < max(lo),
      "so lensing does NOT close the CQ class: it constrains the noise spectrum (a two-component structure)")

# =========================================================================================== C  cost
banner("C  WHAT THE CLASS STILL HAS TO SUPPLY -- the amplitude (the variance must BE the phantom)")
Msun, kpc = 1.98892e30, 3.0856775814913673e19
Mb = 6e10 * Msun
dyn_per_S = (Rs + Ns) / (1 + float(uopt)**2)          # 8 pi G (rho + p_r+2p_t) per unit total <|grad|^2>
for fk, a0 in A0.items():
    rM = math.sqrt(G_SI * Mb / a0)
    vf = (G_SI * Mb * a0)**0.25
    rows_c = []
    for fac in (1, 3, 10):
        r = fac * rM
        rho_ph = vf**2 / (4 * math.pi * G_SI * r**2)
        S_req = 8 * math.pi * G_SI * rho_ph * c_SI**2 / dyn_per_S      # m^2 s^-4 (restoring c)
        rows_c.append((fac, math.sqrt(S_req) / (vf**2 / r)))
    OUT["numbers"][f"dg_rms_over_g_{fk}"] = rows_c
    P(f"    {fk:9s} r_M = {rM/kpc:.2f} kpc, v_f = {vf/1e3:.0f} km/s: required delta g_rms / g_obs at "
      + ", ".join(f"{f} r_M = {q:.0f}" for f, q in rows_c))
q_c = OUT["numbers"]["dg_rms_over_g_canonical"][0][1]
vf_c = (G_SI * Mb * A0["canonical"])**0.25
check("C1 to BE the deep-MOND phantom the metric's rms acceleration must exceed the mean field by "
      "sqrt(2/C_act) c/v_f (~%.0f x at r_M): the amplitude law (FRIED_CHICKEN req. 10) moves into the noise "
      "kernel, underived" % q_c,
      f"{q_c:.0f}x at r_M (canonical); identity delta g/g = sqrt(2/C_act) c/v_f with C_act = {dyn_per_S:.4f}",
      abs(q_c / (c_SI / vf_c) - math.sqrt(2 / dyn_per_S)) < 1e-9 and q_c > 100,
      "classical noise escapes the 09-01 hbar-counting theorem, but nothing in CQ fixes D0(x) to track "
      "sqrt(G M_b a0)/r^2, so kappa and the BTFR stay inputs, exactly as in every other route")

# =========================================================================================== verdict
banner("VERDICT")
P(f"""  1. THE PUBLISHED NUMBER: OR24's a0 ~ sqrt(Lambda) holds as a SCALING, but its coefficient is
     kappa = {k0:.2f}-{kinf:.2f} (completely positive beta), >= {zA:.0f} sigma above the measured {KAPPA_A} +/- {SIG_A};
     kappa = 1/2 needs beta = {float(b_half):.4f}, which gives up complete positivity. As a Tully-Fisher
     normaliser it tends to 2 c H_Lambda (Milgrom 1999) at beta -> -inf. Its gamma_1 r term is a constant
     acceleration: lensing-RAR slope 0 vs {SLOPE_LOW:.3f} +/- {SLOPE_ERR:.3f} measured (L248), {zslope:.0f} sigma.
  2. THE CLASS: a phantom made of GR-COMPLIANT fluctuation energy (waves; every quantum graviton bath) is dead
     on lensing at {nsig(eT):.0f} sigma, convention-free. A phantom made of CONSTRAINT-VIOLATING static scalar noise
     (what CQ gravity uniquely allows) is NOT excluded: under the Einstein-Langevin convention it must lens
     >= {100*(LD(-e_min_f)-1):.1f}% MORE than it attracts ({nsig(-e_min_f):.1f} sigma today; OR24's own ansatz
     {100*(LD(eOR)-1):.1f}%, {nsig(eOR):.1f} sigma); a two-component spectrum can null the difference. Pure lapse
     noise and OR24's white-in-time limit rectify to REPULSION.
  3. THE MISSING INPUT, named: CQ gravity does not say which tensor density its noise is unbiased in, and the
     lensing prediction moves at O(1) with that choice. Until it does, the class is open-but-unpriced.
  4. NOTHING HERE DERIVES kappa OR THE AMPLITUDE: the noise must track the phantom (rms ~{q_c:.0f} x the mean
     field at r_M) and D0 is free. A door opened with a price tag and a falsifier, not a closure.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
with open(os.path.join(HERE, outname), "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
