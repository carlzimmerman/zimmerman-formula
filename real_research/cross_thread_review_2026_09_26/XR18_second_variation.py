#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR18 (b) -- A DE12-TYPE SECOND VARIATION OF THE FULL H_Y ACTION ON GALAXY BACKGROUNDS.  Does any term of FP9's separator
land a k^0 stiffness of the wrong sign on the baryons (or on phi), and what growth does H_Y's own stiffness structure give
against H -- on DE12's 24 host systems, so the numbers compare with DE12 / DE13 / XR15?

WHY.  DE12 (dark_energy_2026/DE12_mond_sector_gate_stiffness.py) showed that a LOCAL region gate f = W(U), once varied as
an action term, is a k^0 negative bulk modulus on edge-layer gas: U reads the local dynamical density (lap(u - v) =
4 pi G rho_b is a constraint), so d^2(B W)/d rho_b^2 = B W'' t_U^2 U_rho^2 is local; Gamma = c_gate k with c_gate
1500-3700 km/s at z = 0.25, 2-5e4 H at k = 1/kpc.  DE13 and XR15 showed no gradient energy and no smoothing repairs it.
FP9 (derivation_chain_2026/FP9_web_galaxy_separator.py, b510eebfe) replaced every local gate by (H_Y): a band-pass on the
chassis and a yield floor in J, both run by the leaf average <K>_h.  This lane asks whether H_Y re-creates DE12's
obstruction anywhere once the WHOLE action is varied.

THE ACTION VARIED (FP9's (H_Y) on FP7's root; per 1/16 pi G, c = 1, alpha = a0/c^2):
  R - 2 Lambda + alpha_c a^2 - c_2 (K - <K>_h)^2 + (2 - alpha_c) h^mn (2 a_m - D_m chi) D_n chi - 2 alpha^2 J_Y(Y)
  + 2 lambda (n.d phi)^2 + heat pair (W_0 = phi; chi = W_b - W_B = (S_xi - S_L) phi, B = L^2/2) + S_m[g],
  J_Y = J_P2(Y) + 2 y_th sqrt(Y),  y_th = y_Lambda Omega_L(<K>_h)^(-p'),  L = L_Lambda Omega_L(<K>_h)^(n/2);
  headline cell L_Lambda = 2.46 Mpc, n = 2, y_Lambda = 7.78e-8, p' = 4.  Both footings a0 = 9.3603e-11 / 1.1312e-10 m/s^2.

METHOD.
 (1) THE WKB ORDER COUNT (sympy, exact in the frozen-coefficient planar reduction).  A baryon perturbation delta rho e^{ikx}
     on a static background; the constraint-slaved first-order responses are solved exactly:
       delta Phi_N = -4 pi G_N delta rho/k^2,  C_theta delta phi'' = 4 pi G h delta rho  ->  delta phi = -4 pi G h delta rho/(C k^2),
       delta chi = h delta phi,  delta Phi = delta Phi_N + delta chi,  delta lap Phi = 4 pi G A delta rho,  A = G_N/G + h^2/C_theta,
     with C_theta = C_L (along g) or C_T (across), h the band-pass gain at k; <K>_h's perturbation is 0 at k != 0 and its
     second order is ~ (delta Psi)^2 ~ k^-4.  Every term's second-order energy density is written out, the responses
     inserted, and the k^0 coefficient taken as k -> oo at fixed h.  The same engine, with DE12's gate term -B W(t(U))
     inserted (U reading the local dynamical density), must return DE12's S = B W'' t_U^2 U_rho^2 (control K1).
 (2) THE EXACT RADIAL (l = 0) SECTOR (spherical perturbations are exact in a spherical background).  The reduced
     (on-shell) energy of a spherical system under H_Y's static law is
       E[M] = -Int G M^2/(2 r^2) dr - Int (r^2 a0^2/G) Q(y_bp) dr + Int 4 pi r^2 rho e(rho) dr,
       y_bp = G M_bp/(a0 r^2),  M_bp = enclosed mass of (S_xi - S_L) rho,  Q' = x(y) = x_P2(y - y_th) above the yield, 0 below;
     its gradient is FP9's law (control K2), its second variation for radial displacements xi (delta M = -4 pi r^2 rho xi)
       V2 = (1/2) Int 4 pi r^2 (c_s^2/rho) delta rho^2 dr - (1/2) Int (G/r^2) [delta M^2 + Q''(y_bp) delta M_bp^2] dr,
     Q'' = dx/dy (the longitudinal MOND susceptibility, = 1/C_L^phi: it DIVERGES as (y - y_th)^(-1/2) at the yield surface and
     is 0 in the plug).  Kinetic T = (1/2) Int 4 pi r^2 rho xi'^2 dr; growth Gamma^2 = -min eig(K, M).  The singular weight is
     integrated exactly per cell (Int Q'' dr = Int dx/(dy_bp/dr)); the yield is also regularised (J_eps: y_th sqrt(Y + eps^2))
     to test eps -> 0.  Backgrounds: DE12's 24 host systems (z = 0.25, 1, 2.5, 4; M_b = 1e10, 1e11, 1e12; both footings) with
     DE12's gas profile rho_b = f_b(rho_NFW + rho_bar) and FP9's point-mass band-passed field; the domain brackets H_Y's own
     transition, the yield surface r_Y: [max(r_Y/3, 1 kpc), 3 r_Y].

PRE-DECLARED (written into this file before its first full run).  Exploratory runs made BEFORE these were written are
disclosed in XR18_README.md: a scratch map of r_Y and the local dx/dy on DE12's 24 hosts (it showed the divergent
susceptibility and local pressureless rates of ~20-60 H at 1 kpc from r_Y), and 1-D prototypes for part (a).
 H1 [load-bearing] No term of the full H_Y action (EH, Lambda, alpha_c a^2, c_2 (K - <K>_h)^2 with the leaf average, the
    chassis with the band-pass, J_Y with y_th(<K>_h), phi's inertia, the heat pair with L(<K>_h), matter) has a k^0 part:
    the baryons' k^0 coefficient is c_s^2/rho_b (the gas alone, positive), and the phi-phi block has no k^0 (mass) term.
 H2 [load-bearing] DE12's own convention on the same 24 hosts (WKB growth at k = 1/kpc, 1e6 K gas, over the whole profile
    1 kpc - 20 Mpc, the susceptibility window-averaged over 1/k): Gamma(1/kpc) = 0 for H_Y on all 24 (DE12's gate: 1.3e3 -
    4.9e4 H).
 H3 [load-bearing] The exact radial sector of H_Y around each yield surface, gas at 1e6 K and 1e5 K: the maximum growth
    rate is converged (grid doubling < 5%; the regularised yield at eps/sqrt(y_th) = 1e-3 and 1e-4 within 5% of eps = 0), and
    the yield raises it over plain band-passed P2 (FP9's route (i), no yield) on the same domain by less than a factor 2.
 H4 [load-bearing; the adversarial case] Cold (pressureless) matter at the yield surface: the growth rate of the most
    localised radial mode grows with resolution as Gamma ~ d_min^(-p), p in [0.20, 0.30] (the (y - y_th)^(-1/2)
    susceptibility averaged over the mode: Gamma^2 ~ 4 pi G rho (s d)^(-1/2)), for d_min from 3 kpc down to 40 xi, and
    saturates (d_min = xi/3 vs xi/10 within 10%) once the xi filter is resolved: BOUNDED by xi, but resolution-dependent in
    any code that does not resolve xi (a particle-mesh run).
The writer's expectation: H1, H2 pass by derivative-order counting (H_Y reads only first derivatives and leaf averages);
H3 passes; H4 holds.

CHECKS
  K1 CONTROL (DE12): this lane's WKB engine with DE12's gate term inserted returns S = B W'' t_U^2 U_rho^2 identically
     (sympy), and on DE12's own profiles (transition() loaded unedited, definitions only) reproduces DE12's committed
     c_gate_max and Gamma(1/kpc)/H on all 24 galaxy layers (relative deviation <= 1e-12).
  K1b the AQUAL-form amplification A = G_N/G + h^2/C_L^phi equals DE12's QUMOND-form A_par = nu + y nu' at h = 1,
     G_N = G (the duality C_L^phi = 1/C_L^Q), and A_perp = nu (sympy + numbers).
  K2 CONTROL: the reduced energy's gradient is FP9's law: the exact derivative of E[M] with respect to a test shell's radius
     (band-pass and yield included) gives the force of FP9's spherical H_Y law (FP6's phantom() with FP9's yield hook, exec'd
     read-only) to 2e-3 (FP6's own grid) and FP6's algorithm at 20x resolution to 1e-4 (1e11: z = 2.5 both footings, z = 0.25).
  K3 CONTROL: the discrete radial operator reproduces the analytic Jeans rate Gamma^2 = 4 pi G rho (1 + Q'') - c_s^2 k^2 on a
     uniform test medium (constant Q'') to 2%.
  B1 = H1.   B2 = H2.   B3 = H3.   B4 = H4 (kept exactly as declared and as run).
  B4b [ADDED AFTER B4's first run -- a MUTATE run; B4 does not depend on MUTATE -- and written before its own first run]:
     B4's domain maximum is, at z >= 2.5 and coarse d_min, an interior dense-gas mode, so its fit mixed two regimes; B4b isolates
     the surface mode (layer |r - r_Y| <= max(30 d_min, 10 xi)): p in [0.20, 0.30] on all 24 hosts over 40 xi <= d_min <=
     min(1 kpc, 0.01 r_Y), and saturation within 10% between xi/3 and xi/10.
  B5 (reported) H_Y's exact radial growth on DE12's OWN layers (the t in (0,1) band +- 30%), 1e6 K gas, against DE12's gate
     (2e4-5e4 H at 1/kpc) and XR15's smoothed residual (1.1-2.8 H).
  B6 (reported) the heat pair's metric coupling (the leafwise Laplacian's h_ij dependence): its second variation is
     O(k^-1 Phi/c^2); its size relative to the gas term at k = 1/kpc.
  Development record (disclosed in XR18_README.md): the first (MUTATE) run (i) finite-differenced K2's TOTAL energy, which was
  quadrature noise (up to 10%) -- K2 now uses the exact derivative; (ii) located r_Y by linear interpolation on DE12's grid
  (~1e-7 relative error, coarser than B4's finest d_min), which blurred B4's saturation -- r_Y is now a brentq root; (iii) showed
  B4's domain maximum is an interior dense-gas mode at z >= 2.5 and coarse d_min -- B4b was added (B4 kept as declared).  After
  the first recorded main run only the VERDICT text changed (it now prints B4b's numbers and says what B4's failure rests on,
  and the pass count counts every check); MUTATE and main were then re-run in that order.
MUTATE=1 inserts DE12's local density-read gate into H_Y (the term -B W(t(U)), U reading lap Phi/(4 pi G), with DE12's
profiles on DE12's layers): B1 and B2 must FAIL (a negative k^0 term; Gamma(1/kpc) up to DE12's values), and B3's
convergence must fail (a UV-growing, grid-limited mode).  rc = 1.

SCOPE.  Frozen background, fluid gas (isothermal), point-mass baryons for the MOND field (DE12's convention), the l = 0
sector exact, the planar WKB count for the order statement.  No particle-mesh run.  kappa = 1/2 is FITTED (Z = 5.7888).

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR18_second_variation.py
"""
import os, sys, io, json, math, time, contextlib, warnings
os.environ.setdefault("OMP_NUM_THREADS", "2"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
import numpy as np
import sympy as sp
from scipy.linalg import eigh
from scipy.special import erf
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR18_second_variation"
T0 = time.time()
_OUTF = open(os.path.join(HERE, SLUG + ("_MUTATE.out" if MUTATE else ".out")), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); _OUTF.write(s + "\n"); _OUTF.flush()


CH, OUT = [], {"lane": "XR18b", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}" if (ok or not MUTATE) else
          f"         reading (written for the unmutated theory; this MUTATE run fails the check):  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 112); P(t); P("=" * 112)


def el():
    return f"[{time.time() - T0:.0f} s]"


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: DE12's local density-read gate is inserted into H_Y -- B1, B2 and B3 must FAIL ***")

# ============================================================================================ machinery (read-only)
FP9 = os.path.join(REPO, "real_research", "derivation_chain_2026", "FP9_web_galaxy_separator.py")
_src9 = open(FP9).read()
_cut9 = _src9.index('\nbanner("K  CONTROLS')
NS9 = {"__file__": FP9, "__name__": "fp9_machinery"}
_old = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(_src9[:_cut9], FP9, "exec"), NS9)
finally:
    if _old is None:
        os.environ.pop("MUTATE", None)
    else:
        os.environ["MUTATE"] = _old
M6 = NS9["M6"]
A0 = dict(NS9["A0"])
FOOTS = ("canonical", "alt")
x_P2, OmL_z, L_phys, LL_of, y_th_z = NS9["x_P2"], NS9["OmL_z"], NS9["L_phys"], NS9["LL_of"], NS9["y_th_z"]
gfrac = M6["gfrac_smooth"]; shell_frac = M6["shell_frac"]; MPCm = M6["MPCm"]; G6 = M6["G6"]
HEAD = dict(n=2.0, L25=1.3, pp=4.0, y25=1e-6)
LLh = LL_of(HEAD["L25"], HEAD["n"]); FLh = (HEAD["y25"], HEAD["pp"], NS9["YIELD"])
XI_PC = {"canonical": 0.0243, "alt": 0.0268}                           # FP7's AQUAL Solar-System floors on xi (R7f)

P12 = os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness.py")
D12 = {"__name__": "de12", "__file__": P12}
_s12 = open(P12).read()
_head = _s12.split("# ============================================================================================ C1 the amplification")[0]
_trans = _s12.split("# ============================================================================================ the transitions")[1].split(
    "# ============================================================================================ G1 G2 the budget")[0]
_trans = _trans.split('banner("C2')[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec((_head + _trans).replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), D12)
transition, Wd, CS, KPC, MS, G12, Hz12 = D12["transition"], D12["Wd"], D12["CS"], D12["KPC"], D12["MS"], D12["G"], D12["Hz"]
nu_of, ynup_of = D12["nu_of"], D12["ynup_of"]
R12 = json.load(open(os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness_results.json")))["numbers"]
GAL = [(z, Mb, f) for z in (0.25, 1.0, 2.5, 4.0) for Mb in (1e10, 1e11, 1e12) for f in FOOTS]
KEY = lambda z, Mb, f: f"{z}/{Mb:.0e}/{f}"
P(f"\n  machinery: FP9 exec'd read-only up to its CONTROLS banner (FP6 inside it); DE12's transition() definitions only; "
  f"a0 = {A0['canonical']:.4e} / {A0['alt']:.4e}; H_Y headline L_Lambda = {LLh:.3f} Mpc, n = 2, y_th(0.25) = 1e-6, p' = 4   {el()}")

# ============================================================================================ the WKB engine (sympy)
banner("K1  CONTROL + B1: THE WKB ORDER COUNT OF THE FULL ACTION (sympy), and DE12's gate term as the control")
k, h, Gs, rho, cs, Cth, GNG, ac, lam, Gam, c2k, cl, Qk, Kd, gB, rhoph, LamC = sp.symbols(
    "k h G rho c_s C_theta G_N_over_G alpha_c lambda Gamma c_2 c Q_K Kdiff gbar rho_ph Lambda_c", positive=True)
Bg, W1s, W2s, tU, Umax, Aamp, Urr = sp.symbols("B W1 W2 t_U U_max A U_rhorho", real=True)
# first-order responses per unit delta rho (plane wave along the background field for C_L, across it for C_T)
dPhiN = -4 * sp.pi * Gs * GNG / k ** 2
dphi = -4 * sp.pi * Gs * h / (Cth * k ** 2)
dchi = h * dphi
dPhi = dPhiN + dchi
dlapPhi = -k ** 2 * dPhi                                       # = 4 pi G A delta rho
A_expr = sp.simplify(dlapPhi / (4 * sp.pi * Gs))
dL = sp.Integer(1)                                              # the heat multiplier's response: delta L = delta rho (chassis source)
# second-order energy densities e^(2) per |delta rho|^2 (the second-order Taylor term with the first-order responses inserted)
TERMS = {
    "gas (rho e(rho), isothermal)": cs ** 2 / (2 * rho),
    "matter coupling rho Phi (bilinear)": dPhi,
    "EH + alpha_c a^2 + chassis (Psi = Phi branch): (2 - a_c)|grad(Phi - chi)|^2/(16 pi G)":
        ((2 - ac) / (16 * sp.pi * Gs)) * k ** 2 * dPhiN ** 2,
    "J_Y on phi (C_theta = C_L or C_T of J_Y, y_th(<K>_h) inside): C |grad dphi|^2/(8 pi G)":
        (Cth / (8 * sp.pi * Gs)) * k ** 2 * dphi ** 2,
    "phi's inertia 2 lambda (n.dphi)^2 (growth rate Gamma)": -(lam / (8 * sp.pi * Gs * cl ** 2)) * Gam ** 2 * dphi ** 2,
    "khronon c_2 (K - <K>_h)^2 (delta K ~ 3 Gamma delta Psi/c^2)": (c2k * cl ** 2 / (16 * sp.pi * Gs)) * (3 * Gam * dPhi / cl ** 3) ** 2,
    "Lambda sqrt(-g) (delta^2 sqrt(-g) ~ (delta Phi/c^2)^2)": (LamC / (16 * sp.pi * Gs)) * (dPhi / cl ** 2) ** 2,
    "leaf average: Q d^2<K>_h via y_th(<K>_h), L(<K>_h) (k != 0: first order 0; second ~ (K - <K>)(delta Psi/c^2)^2)":
        Qk * Kd * (dPhi / cl ** 2) ** 2,
    "heat pair's metric coupling: -2 delta L [2 dPsi lap W - grad dPsi.grad W]/c^2 (lap W ~ 4 pi G rho_ph, |grad W| ~ g_ph)":
        -2 * dL * (2 * dPhi * 4 * sp.pi * Gs * rhoph + sp.sqrt(k ** 2) * dPhi * gB) / cl ** 2,
}
GATE_TERM = ("DE12's gate: -B W(t(U)), U reading lap Phi/(4 pi G) (the local dynamical density)",
             -sp.Rational(1, 2) * Bg * (W2s * tU ** 2 * (Umax * A_expr) ** 2 + W1s * tU * Urr))
USE = dict(TERMS)
if MUTATE:
    USE[GATE_TERM[0]] = GATE_TERM[1]
qv = sp.Symbol("q", positive=True)


def k_order(expr):
    """leading power of k as k -> oo (at fixed h) and the k^0 coefficient."""
    e = sp.simplify(expr.subs(k, 1 / qv))
    if e == 0:
        return (-sp.oo, sp.Integer(0))
    lead = sp.series(e, qv, 0, 6).removeO()
    lead = sp.expand(lead)
    pw = min(sp.Poly(lead, qv).monoms())[0] if lead.has(qv) else 0
    k0 = sp.simplify(lead.coeff(qv, 0)) if lead.has(qv) else sp.simplify(lead)
    return (-pw, k0)


rows = []
k0_total = sp.Integer(0)
for nm, ex in USE.items():
    order, k0 = k_order(ex)
    rows.append((nm, order, k0))
    k0_total += k0
k0_total = sp.simplify(k0_total)
for nm, order, k0 in rows:
    P(f"    {nm:118s} leading k-order {str(order):>4s};  k^0 coefficient {k0}")
# the full k^-2 (Jeans) coefficient of H_Y's terms, and the phi-phi block's mass term
jeans = sp.simplify(sum(sp.limit(ex * k ** 2, k, sp.oo) for nm, ex in TERMS.items() if nm.startswith(("matter", "EH", "J_Y"))).subs(GNG, 2 / (2 - ac)))
jeans_ok = sp.simplify(jeans - (-2 * sp.pi * Gs * (2 / (2 - ac) + h ** 2 / Cth))) == 0
# phi's own quadratic form: J_Y and chassis give only k^2 (gradients); a mass term would need d^2 L/d phi^2 != 0
phiS, phx, pht, Phx, ysth, alS = sp.symbols("phi phi_x phi_t Phi_x y_th alpha", real=True)
YS = phx ** 2 / alS ** 2
JY = -sp.log(1 - 2 * sp.sqrt(YS)) / 4 - sp.sqrt(YS) / 2 - YS / 2 + 2 * ysth * sp.sqrt(YS)
L_phi_block = (-(2 - ac) * (Phx - h * phx) ** 2 - 2 * alS ** 2 * JY + 2 * lam * pht ** 2) / (16 * sp.pi * Gs)
mass_phi = sp.diff(L_phi_block, phiS, 2)
P(f"    A (the amplification in delta lap Phi = 4 pi G A delta rho) = {A_expr};  H_Y's k^-2 coefficient per |delta rho|^2: {jeans} "
  f"(= -2 pi G A: {jeans_ok});  phi-phi mass term d^2 L/d phi^2 = {mass_phi}")
# K1: the gate term's k^0 coefficient is DE12's S, identically; then DE12's numbers on its own profiles
order_g, k0_g = k_order(GATE_TERM[1])
S_engine = sp.simplify(-2 * k0_g)
S_de12 = Bg * (W2s * tU ** 2 * (Umax * A_expr) ** 2 + W1s * tU * Urr)
k1_sym = sp.simplify(S_engine - S_de12) == 0 and order_g == 0
S_fun = sp.lambdify((Bg, W1s, W2s, tU, Umax, Aamp, Urr), Bg * (W2s * tU ** 2 * (Umax * Aamp) ** 2 + W1s * tU * Urr), "numpy")
k1rows, k1dev = {}, 0.0
for (z, Mb, f) in GAL:
    tr = transition(z, Mb, f, 0.25)
    m = (tr["t"] > 0) & (tr["t"] < 1)
    _, W1, W2 = Wd(tr["t"])
    Umx = 4 * math.pi * G12 / (tr["H"] ** 2 * tr["xce"])
    Sper = S_fun(tr["B"], W1, W2, 1 / (2 * 0.25), Umx, nu_of(tr["y"]), 0.0)
    Spar = S_fun(tr["B"], W1, W2, 1 / (2 * 0.25), Umx, nu_of(tr["y"]) + ynup_of(tr["y"]), 0.0)
    cg = np.sqrt(np.maximum(tr["rho_b"] * np.maximum(Sper, 0), tr["rho_b"] * np.maximum(Spar, 0)))
    cmax = float(np.max(cg[m]))
    gam = (1 / KPC) * math.sqrt(max(cmax ** 2 - CS["1e6K"] ** 2, 0.0)) / tr["H"]
    ref = R12["budget"][KEY(z, Mb, f)]
    dv = max(abs(cmax / ref["c_gate_max"] - 1), abs(gam / ref["Gamma_over_H"] - 1))
    k1dev = max(k1dev, dv)
    k1rows[KEY(z, Mb, f)] = dict(c_gate=cmax, Gamma_over_H=gam, ref=ref["c_gate_max"], ref_G=ref["Gamma_over_H"])
P(f"    gate term through the engine: leading k-order {order_g}, k^0 coefficient -S/2 with S == DE12's B[W'' t_U^2 U_rho^2 + "
  f"W' t_U U_rhorho]: {k1_sym};  on DE12's profiles: c_gate_max " + ", ".join(
      f"{kk}: {v['c_gate'] / 1e3:.0f}" for kk, v in list(k1rows.items())[:6]) + " ... km/s")
check("K1 CONTROL (DE12): this lane's WKB engine, given DE12's gate term -B W(t(U)) with U reading the local dynamical density "
      "lap Phi/(4 pi G), returns its k^0 coefficient as DE12's S = B[W'' t_U^2 U_rho^2 + W' t_U U_rhorho] identically, and on "
      "DE12's own profiles (definitions loaded unedited) reproduces DE12's committed c_gate_max and Gamma(1/kpc)/H on all 24 layers",
      f"symbolic identity {k1_sym}; max relative deviation over 24 layers {k1dev:.1e} (e.g. z = 0.25/1e10/can "
      f"{k1rows['0.25/1e+10/canonical']['c_gate'] / 1e3:.1f} vs {k1rows['0.25/1e+10/canonical']['ref'] / 1e3:.1f} km/s)",
      k1_sym and k1dev <= 1e-12)
OUT["numbers"]["K1"] = k1rows
# K1b the two forms of the amplification
yv = np.logspace(-6, 3, 400)
xq = x_P2(yv)
CLphi = 2 * xq * (1 - xq) / (1 - 2 * xq) ** 2
A_aqual = 1.0 + 1.0 / CLphi
A_qumond = np.sqrt(1 + 1 / yv) + yv * (-0.5 * (1 + 1 / yv) ** -0.5 / yv ** 2)       # d(y nu_P2)/dy
k1b = float(np.max(np.abs(A_aqual / A_qumond - 1)))
check("K1b the AQUAL-form amplification A = G_N/G + h^2/C_L^phi equals the QUMOND-form A_par = d(y nu)/dy (DE12's nu + y nu') "
      "at h = 1, G_N = G (the duality C_L^phi = 1/C_L^Q), P2 kernel, y = 1e-6..1e3",
      f"max relative deviation {k1b:.1e}", k1b < 1e-8)
b1_gas_only = sp.simplify(k0_total - cs ** 2 / (2 * rho)) == 0
b1_neg = [nm for nm, order, k0 in rows if k0 != 0 and not nm.startswith("gas")]
check("B1 [H1, pre-declared] NO k^0 TERM IN THE FULL H_Y ACTION: every term's second variation (EH, Lambda, alpha_c a^2, "
      "c_2 (K - <K>_h)^2, the chassis with the band-pass, J_Y with y_th(<K>_h), phi's inertia, the heat pair with L(<K>_h), matter) "
      "is O(k^-1) or smaller except the gas's own c_s^2/rho_b; the phi-phi block has no mass term; the Jeans coefficient is "
      "-2 pi G A with A = G_N/G + h^2/C_theta",
      f"k^0 total per |delta rho|^2: {k0_total} (gas only: {b1_gas_only}); other terms with a k^0 part: {b1_neg or 'none'}; "
      f"Jeans form {jeans_ok}; phi mass {mass_phi}",
      b1_gas_only and not b1_neg and jeans_ok and mass_phi == 0,
      "DE12's obstruction needs a term that reads a SECOND derivative of a constraint-slaved potential (the local density); H_Y's "
      "separators read first derivatives (grad phi, a = grad ln N) and leaf averages only, so the only k^0 stiffness is pressure")
OUT["numbers"]["B1"] = {"rows": [(nm, str(o), str(c)) for nm, o, c in rows], "k0_total": str(k0_total), "A": str(A_expr)}
P(f"    {el()}")

# ============================================================================================ H_Y backgrounds on DE12's hosts
Z_N = HEAD["n"]


def hy_host(z, Mb, foot, r):
    """H_Y's point-mass background on the radial grid r [m]: y_N, y_bp, y_th, x (the yield law), L(z) [m]."""
    a0 = A0[foot]
    Lz = L_phys(LLh, Z_N, 1 / (1 + z)) * MPCm
    yth = y_th_z(FLh, z)
    yN = G6 * Mb * MS / (r ** 2 * a0)
    ybp = yN * (1 - gfrac(r / Lz))
    return dict(yN=yN, ybp=ybp, yth=yth, L=Lz, a0=a0)


def x_yield(y, yth, eps=0.0, plain=False):
    """the scalar's field x for band-passed field y: yield law (eps = 0 exact), regularised yield (eps > 0), plain P2."""
    y = np.asarray(y, float)
    if plain:
        return x_P2(y)
    if eps == 0.0:
        return x_P2(np.maximum(y - yth, 0.0))
    lo = np.zeros_like(y); hi = np.full_like(y, 0.4999999)
    for _ in range(90):
        mid = 0.5 * (lo + hi)
        F = mid ** 2 / (1 - 2 * mid) + yth * mid / np.sqrt(mid ** 2 + eps ** 2)
        up = F > y
        hi = np.where(up, mid, hi); lo = np.where(up, lo, mid)
    return 0.5 * (lo + hi)


def cum_Q2(r, yfun, yth, eps=0.0, plain=False, nsub=16):
    """X(r) = Int_r0^r Q''(y_bp) dr' with the singular weight integrated exactly per sub-interval: dX = dx/(dy_bp/dr) dr
    (exact where y_bp is linear across a sub-interval); yfun(r) gives the band-passed field."""
    rs = np.concatenate([np.linspace(a, b, nsub, endpoint=False) for a, b in zip(r[:-1], r[1:])] + [r[-1:]])
    ys = yfun(rs)
    xs = x_yield(ys, yth, eps, plain)
    dy = np.diff(ys); dx = np.diff(xs)
    ok = np.abs(dy) > 0
    w = np.where(ok, dx / np.where(ok, dy, 1.0), 0.0) * np.diff(rs)
    Xs = np.concatenate([[0.0], np.cumsum(np.abs(w))])
    return np.interp(r, rs, Xs)


def r_yield(r, ybp, yth, yfun=None):
    """the outermost radius where the band-passed field falls through the yield; with yfun given, refined to machine precision
    by brentq on the exact field (the geometric clustering near the surface and the d/r_Y fits need it)."""
    above = ybp > yth
    if not above.any() or above.all():
        return float("nan")
    j = np.where(above)[0][-1]
    if yfun is not None:
        from scipy.optimize import brentq as _bq
        return float(_bq(lambda rr: float(yfun(np.array([rr]))[0]) - yth, r[j], r[j + 1], xtol=1e-15 * r[j], rtol=1e-15))
    return float(r[j] + (yth - ybp[j]) * (r[j + 1] - r[j]) / (ybp[j + 1] - ybp[j]))


# ============================================================================================ B2 DE12's convention
banner("B2  DE12's CONVENTION ON THE SAME 24 HOSTS: WKB growth at k = 1/kpc, 1e6 K gas, whole profile 1 kpc - 20 Mpc")
kW = 1 / KPC
b2 = {}
for (z, Mb, f) in GAL:
    tr = transition(z, Mb, f, 0.25)
    r = tr["r"]; H = tr["H"]
    bg = hy_host(z, Mb, f, r)
    hk = 1 - math.exp(-0.5 * (kW * bg["L"]) ** 2)
    X = cum_Q2(r, lambda rr_: hy_host(z, Mb, f, rr_)["ybp"], bg["yth"])
    Xm = np.interp(r - 0.5 / kW, r, X); Xp = np.interp(r + 0.5 / kW, r, X)
    Qwin = (Xp - Xm) * kW                                              # window-averaged Q'' over 1/k
    A = 1 + hk ** 2 * Qwin
    g2 = 4 * math.pi * G6 * tr["rho_b"] * A - CS["1e6K"] ** 2 * kW ** 2
    if MUTATE:                                                         # DE12's gate k^0 term on its own layer
        _, W1, W2 = Wd(tr["t"])
        Umx = 4 * math.pi * G12 / (H ** 2 * tr["xce"])
        Spar = S_fun(tr["B"], W1, W2, 2.0, Umx, nu_of(tr["y"]) + ynup_of(tr["y"]), 0.0)
        Sper = S_fun(tr["B"], W1, W2, 2.0, Umx, nu_of(tr["y"]), 0.0)
        g2 = g2 + tr["rho_b"] * np.maximum(np.maximum(Spar, Sper), 0) * kW ** 2
    gmax = float(np.sqrt(max(np.max(g2), 0.0))) / H
    g2_1e5 = 4 * math.pi * G6 * tr["rho_b"] * A - CS["1e5K"] ** 2 * kW ** 2
    g2_1e5N = 4 * math.pi * G6 * tr["rho_b"] - CS["1e5K"] ** 2 * kW ** 2
    rY = r_yield(r, bg["ybp"], bg["yth"])
    b2[KEY(z, Mb, f)] = dict(Gamma_over_H=gmax, Gamma_1e5K=float(np.sqrt(max(np.max(g2_1e5), 0.0))) / H,
                             Gamma_1e5K_Newton=float(np.sqrt(max(np.max(g2_1e5N), 0.0))) / H,
                             r_max_1e5K_kpc=float(r[np.argmax(g2_1e5)] / KPC), r_Y_kpc=rY / KPC,
                             Qwin_max=float(np.max(Qwin)), DE12=R12["budget"][KEY(z, Mb, f)]["Gamma_over_H"])
for kk, v in b2.items():
    P(f"    {kk:22s}: r_Y = {v['r_Y_kpc']:8.1f} kpc; max window-averaged Q'' {v['Qwin_max']:9.1f}; Gamma(1/kpc)/H: 1e6 K {v['Gamma_over_H']:.3g}, "
      f"1e5 K {v['Gamma_1e5K']:.3g} (Newton only {v['Gamma_1e5K_Newton']:.3g}; its max at r = {v['r_max_1e5K_kpc']:.1f} kpc)   "
      f"(DE12's gate: {v['DE12']:.2e})")
b2_ok = all(v["Gamma_over_H"] == 0.0 for v in b2.values())
check("B2 [H2, pre-declared] DE12's CONVENTION: H_Y's WKB growth at k = 1/kpc for 1e6 K gas is ZERO on all 24 hosts over the whole "
      "profile (1 kpc - 20 Mpc, the yield surface included, its susceptibility averaged over the 1 kpc window), against DE12's "
      "gate at 1.3e3 - 4.9e4 H",
      f"max Gamma(1/kpc)/H over 24 hosts: {max(v['Gamma_over_H'] for v in b2.values()):.3g} (1e5 K gas, reported: max "
      f"{max(v['Gamma_1e5K'] for v in b2.values()):.3g} at {max(b2, key=lambda q: b2[q]['Gamma_1e5K'])}; the same gas with Newton only: "
      f"max {max(v['Gamma_1e5K_Newton'] for v in b2.values()):.3g})", b2_ok,
      "the 1e5 K column is the gas's own (MOND-amplified) Jeans growth, a k^-2 gravity term at the printed radius, not a gate term")
OUT["numbers"]["B2"] = b2
P(f"    {el()}")

# ============================================================================================ K2 the reduced energy's gradient
banner("K2  CONTROL: the reduced energy E[M] has FP9's spherical law as its gradient (test-shell finite differences)")
_cut_hook = M6["cutfac"]


def Q_yield(D):
    D = np.maximum(D, 0.0); s = np.sqrt(D * D + D)
    return (2 * D + 1) / 4 * s - np.log(2 * D + 1 + 2 * s) / 8 - D * D / 2


def dE_dshell(Mb, a0, Lm, yth, r_sh, rY):
    """the exact derivative of E_ph = -Int (r^2 a0^2/G) Q(y_bp) dr with respect to a test shell's radius, per unit shell mass
    (minus the force): a0 x(y_bp(r_sh)) + a0 Int x(y_bp(r)) d shell_frac(r, r_sh, L)/d r_sh dr  (xi -> 0)."""
    rr = np.geomspace(1e-5 * rY, 60 * rY, 400001)
    yy = G6 * Mb * (1 - gfrac(rr / Lm)) / (a0 * rr ** 2)
    xx = x_P2(np.maximum(yy - yth, 0.0))
    hh = 1e-5 * r_sh
    dK = (shell_frac(rr, np.array([r_sh + hh]), Lm) - shell_frac(rr, np.array([r_sh - hh]), Lm)) / (2 * hh)
    integ = a0 * xx * dK
    return a0 * float(np.interp(r_sh, rr, xx)) + float(np.sum(0.5 * (integ[1:] + integ[:-1]) * np.diff(rr)))


def fp6_hires(Mb, a0, Lm, yth, r_sh):
    """FP6's phantom algorithm (raw phantom, shell-smoothed output filter) on a 20x finer grid, at one radius."""
    RGh = np.geomspace(1e-6, 200, 20001) * MPCm; RGMh = np.sqrt(RGh[1:] * RGh[:-1])
    yv_ = G6 * Mb * (1 - gfrac(RGh / Lm)) / (a0 * RGh ** 2)
    Mraw = a0 * x_P2(np.maximum(yv_ - yth, 0.0)) * RGh ** 2 / G6
    Ms = np.sum(shell_frac(np.array([r_sh])[:, None], RGMh[None, :], Lm)[0] * np.diff(Mraw)) + Mraw[0] * gfrac(np.array([r_sh]) / Lm)[0]
    return G6 * (float(np.interp(r_sh, RGh, Mraw)) - Ms) / r_sh ** 2


k2 = {}
for (z, f) in ((2.5, "canonical"), (2.5, "alt"), (0.25, "canonical")):
    Mb = 1e11 * MS; a0 = A0[f]
    Lm = L_phys(LLh, Z_N, 1 / (1 + z)) * MPCm; yth = y_th_z(FLh, z)
    Mph = M6["phantom"](Mb, a0, Lm, yth, NS9["YIELD"])
    rY = r_yield(M6["RG"], G6 * Mb * (1 - gfrac(M6["RG"] / Lm)) / (a0 * M6["RG"] ** 2), yth)
    for fr in (0.2, 0.5, 0.8):
        rsh = fr * rY
        k2[f"{z}/{f}/{fr}"] = (dE_dshell(Mb, a0, Lm, yth, rsh, rY), G6 * np.interp(rsh, M6["RG"], Mph) / rsh ** 2,
                               fp6_hires(Mb, a0, Lm, yth, rsh))
k2dev = max(abs(a / b - 1) for a, b, c_ in k2.values())
k2hi = max(abs(a / c_ - 1) for a, b, c_ in k2.values())
P("    phantom acceleration at the test shell (energy derivative / FP9's law on FP6's grid / FP6's algorithm at 20x resolution): "
  + ", ".join(f"{kk}: {a:.6e} / {b:.6e} / {c_:.6e}" for kk, (a, b, c_) in k2.items()))
check("K2 CONTROL: the reduced energy's gradient IS FP9's spherical H_Y law -- the exact derivative of E[M] with respect to a test "
      "shell's radius (band-pass and yield inside Q(y_bp)) gives the phantom acceleration of FP6's phantom() with FP9's yield hook "
      "(the output band-pass is the input's adjoint), 1e11 at z = 2.5 (both footings) and z = 0.25, three radii inside r_Y",
      f"max relative deviation vs FP6's grid {k2dev:.1e} (that grid's own error); vs FP6's algorithm at 20x resolution {k2hi:.1e}",
      k2dev < 2e-3 and k2hi < 1e-4,
      "a first run finite-differenced the TOTAL energy and was dominated by quadrature noise (up to 10%); replaced by the exact "
      "derivative before the recorded runs (disclosed in XR18_README.md)")
OUT["numbers"]["K2"] = {kk: list(v) for kk, v in k2.items()}
P(f"    {el()}")


# ============================================================================================ the radial operator
def radial_operator(r, rho, Q2w, cs2, band, cold_xi=None, gate_S=None):
    """K and M of V2 = (1/2) xi.K.xi, T = (1/2) xi'.M.xi' on nodes r (xi = 0 at both ends).
    Q2w: per-node integral of Q'' over the dual cell; band: (Lm) the S_L part of the band-pass; cold_xi: xi [m] for the S_xi part
    (None: xi -> 0); gate_S: per-cell DE12 negative stiffness S (MUTATE)."""
    n = len(r)
    w = np.zeros(n); w[1:-1] = 0.5 * (r[2:] - r[:-2]); w[0] = 0.5 * (r[1] - r[0]); w[-1] = 0.5 * (r[-1] - r[-2])
    Pm = -4 * math.pi * r ** 2 * rho                                   # delta M = Pm xi
    rc = 0.5 * (r[1:] + r[:-1]); dr = np.diff(r); rhoc = np.sqrt(rho[1:] * rho[:-1])
    Dm = np.zeros((n - 1, n)); Dm[np.arange(n - 1), np.arange(n - 1)] = -1; Dm[np.arange(n - 1), np.arange(1, n)] = 1
    # band-passed enclosed-mass perturbation: dM_bp = (F_xi - F_L) D dM, F_x[i, c] = shell_frac(r_i, r_c, x)
    FL = shell_frac(r[:, None], rc[None, :], band) if band else np.zeros((n, n - 1))
    if cold_xi:
        Fx = shell_frac(r[:, None], rc[None, :], cold_xi)
    else:
        Fx = (r[:, None] >= rc[None, :]).astype(float)
    Bmat = (Fx - FL) @ Dm                                             # dM_bp = Bmat dM  (Fx D = I for xi -> 0)
    KN = -np.diag(w * G6 / r ** 2 * Pm ** 2)
    BP = Bmat @ np.diag(Pm)
    KM = -(BP.T * (Q2w * G6 / r ** 2)) @ BP
    # pressure: delta rho_c = -(d(r^2 rho xi)/dr)/r_c^2
    Drho = (Dm * (r ** 2 * rho)[None, :]) / (rc ** 2 * dr)[:, None] * (-1)
    Kp = Drho.T @ np.diag(4 * math.pi * rc ** 2 * dr * cs2 / rhoc) @ Drho if cs2 > 0 else 0.0
    K = KN + KM + Kp
    if gate_S is not None:
        K = K - Drho.T @ np.diag(4 * math.pi * rc ** 2 * dr * gate_S) @ Drho
    Mm = np.diag(4 * math.pi * r ** 2 * rho * w)
    return K[1:-1, 1:-1], Mm[1:-1, 1:-1]


def growth(K, Mm):
    ev = eigh(K, Mm, eigvals_only=True, subset_by_index=[0, 0])[0]
    return math.sqrt(max(-ev, 0.0))


# K3: a uniform test medium with constant Q'' -- the analytic Jeans rate
rho_t, Q2c, cs_t = 1e-25, 30.0, 2e4
Lbox = 400 * KPC; r0t = 2e4 * KPC
rt = np.linspace(r0t, r0t + Lbox, 801)
wt = np.zeros(len(rt)); wt[1:-1] = 0.5 * (rt[2:] - rt[:-2]); wt[0] = wt[-1] = 0.5 * (rt[1] - rt[0])
Kt, Mt = radial_operator(rt, np.full(len(rt), rho_t), Q2c * wt, cs_t ** 2, None)
g_num = growth(Kt, Mt)
k1_ = math.pi / Lbox
g_an = math.sqrt(4 * math.pi * G6 * rho_t * (1 + Q2c) - cs_t ** 2 * k1_ ** 2)
check("K3 CONTROL: the discrete radial operator gives the analytic Jeans rate Gamma^2 = 4 pi G rho (1 + Q'') - c_s^2 k^2 for a "
      "uniform shell of constant Q'' (lowest mode k = pi/L, far from the centre)",
      f"numerical {g_num:.5e} vs analytic {g_an:.5e} s^-1 (rel {abs(g_num / g_an - 1):.1e})", abs(g_num / g_an - 1) < 0.02)


def host_grid(z, Mb, foot, N=300, Ng=120, dmin_rel=1e-4, lo_fac=1 / 3, hi_fac=3.0, dmin_abs=None):
    """nodes on [max(r_Y lo_fac, 1 kpc), r_Y hi_fac]: uniform in ln r (N) + geometric clustering on both sides of r_Y (Ng each)."""
    tr = transition(z, Mb, foot, 0.25)
    rr = tr["r"]; bg = hy_host(z, Mb, foot, rr)
    rY = r_yield(rr, bg["ybp"], bg["yth"], yfun=lambda q: hy_host(z, Mb, foot, q)["ybp"])
    ra, rb = max(rY * lo_fac, 1.0 * KPC), rY * hi_fac
    base = np.geomspace(ra, rb, N)
    dmin = dmin_abs if dmin_abs else dmin_rel * rY
    dl = np.geomspace(dmin, 0.5 * (rY - ra), Ng); dr_ = np.geomspace(dmin, 0.5 * (rb - rY), Ng)
    r = np.unique(np.concatenate([base, rY - dl, rY + dr_, [rY]]))
    r = r[(r >= ra) & (r <= rb)]
    rho = np.exp(np.interp(np.log(r), np.log(rr), np.log(tr["rho_b"])))
    return r, rho, rY, tr


def node_Q2w(r, z, Mb, foot, eps=0.0, plain=False):
    """per-node integral of Q'' over the node's dual cell (singular weight integrated exactly)."""
    bg = hy_host(z, Mb, foot, r)
    edges_ = np.concatenate([[r[0]], 0.5 * (r[1:] + r[:-1]), [r[-1]]])
    re = np.unique(np.concatenate([edges_, r]))
    X = cum_Q2(re, lambda rr_: hy_host(z, Mb, foot, rr_)["ybp"], bg["yth"], eps, plain)
    Xe = np.interp(edges_, re, X)
    return np.diff(Xe), bg


# ============================================================================================ B3 gas around the yield surfaces
banner("B3  THE EXACT RADIAL SECTOR AROUND EACH YIELD SURFACE: gas at 1e6 K and 1e5 K, convergence, yield vs plain P2")
b3 = {}
for (z, Mb, f) in GAL:
    row = {}
    for T_lab in ("1e6K", "1e5K"):
        cs2 = CS[T_lab] ** 2
        res = {}
        for tag, (N, Ng, eps_r, plain) in {"base": (300, 120, 0.0, False), "fine": (600, 240, 0.0, False),
                                          "eps1e-3": (300, 120, 1e-3, False), "eps1e-4": (300, 120, 1e-4, False),
                                          "plainP2": (300, 120, 0.0, True), "newton": (300, 120, 0.0, None)}.items():
            r, rho, rY, tr = host_grid(z, Mb, f, N=N, Ng=Ng)
            if plain is None:
                Q2w = np.zeros(len(r)); bg = hy_host(z, Mb, f, r)
            else:
                Q2w, bg = node_Q2w(r, z, Mb, f, eps=eps_r * math.sqrt(y_th_z(FLh, z)), plain=plain)
            gS = None
            if MUTATE:
                rc = 0.5 * (r[1:] + r[:-1])
                _, W1, W2 = Wd(tr["t"])
                Umx = 4 * math.pi * G12 / (tr["H"] ** 2 * tr["xce"])
                Sg = S_fun(tr["B"], W1, W2, 2.0, Umx, nu_of(tr["y"]) + ynup_of(tr["y"]), 0.0)
                gS = np.maximum(np.interp(rc, tr["r"], Sg), 0.0)
            K, Mm = radial_operator(r, rho, Q2w, cs2, bg["L"], gate_S=gS)
            res[tag] = growth(K, Mm) / tr["H"]
        conv_grid = abs(res["fine"] / max(res["base"], 1e-300) - 1) if res["base"] > 0 else (0.0 if res["fine"] == 0 else 1.0)
        conv_eps = max(abs(res["eps1e-3"] / max(res["base"], 1e-300) - 1), abs(res["eps1e-4"] / max(res["base"], 1e-300) - 1)) if res["base"] > 0 else 0.0
        ratio = res["base"] / res["plainP2"] if res["plainP2"] > 0 else (0.0 if res["base"] == 0 else float("inf"))
        row[T_lab] = dict(res, conv_grid=conv_grid, conv_eps=conv_eps, ratio_vs_P2=ratio, r_Y_kpc=rY / KPC)
    b3[KEY(z, Mb, f)] = row
    v6, v5 = row["1e6K"], row["1e5K"]
    P(f"    {KEY(z, Mb, f):22s} r_Y {v6['r_Y_kpc']:8.1f} kpc | 1e6 K: H_Y {v6['base']:.3g} (fine {v6['fine']:.3g}, eps {v6['eps1e-3']:.3g}/"
      f"{v6['eps1e-4']:.3g}), plain P2 {v6['plainP2']:.3g}, Newton {v6['newton']:.3g} | 1e5 K: H_Y {v5['base']:.3g} (fine {v5['fine']:.3g}), "
      f"plain P2 {v5['plainP2']:.3g}, Newton {v5['newton']:.3g}  [Gamma/H]")
conv_g = max(v[t]["conv_grid"] for v in b3.values() for t in v)
conv_e = max(v[t]["conv_eps"] for v in b3.values() for t in v)
ratio_max = max(v[t]["ratio_vs_P2"] for v in b3.values() for t in v)
gmax3 = max(v[t]["base"] for v in b3.values() for t in v)
check("B3 [H3, pre-declared] THE EXACT RADIAL SECTOR AROUND EACH YIELD SURFACE (24 hosts, gas at 1e6 K and 1e5 K): the maximum "
      "growth rate is converged under grid doubling (< 5%) and under the regularised yield eps/sqrt(y_th) = 1e-3, 1e-4 vs eps = 0 "
      "(< 5%), and the yield raises it over plain band-passed P2 on the same domain by less than a factor 2",
      f"max grid change {conv_g:.1%}; max eps change {conv_e:.1%}; max H_Y/plain-P2 ratio {ratio_max:.2f}; max Gamma/H {gmax3:.3g}",
      conv_g < 0.05 and conv_e < 0.05 and ratio_max < 2.0)
OUT["numbers"]["B3"] = b3
P(f"    {el()}")

# ============================================================================================ B4 cold matter
banner("B4  COLD (PRESSURELESS) MATTER AT THE YIELD SURFACE: growth vs resolution, and the xi filter's cap")
DMINS_PC = (3000.0, 1000.0, 300.0, 100.0, 30.0, 10.0, 3.0, 1.0, 0.3, 0.1)
b4 = {}
for (z, Mb, f) in GAL:
    xi_m = XI_PC[f] * KPC / 1e3
    rows4 = {}
    for dpc in DMINS_PC + (XI_PC[f], XI_PC[f] / 3, XI_PC[f] / 10):
        r, rho, rY, tr = host_grid(z, Mb, f, N=160, Ng=90, dmin_abs=dpc * KPC / 1e3, lo_fac=0.5, hi_fac=2.0)
        Q2w, bg = node_Q2w(r, z, Mb, f)
        K, Mm = radial_operator(r, rho, Q2w, 0.0, bg["L"], cold_xi=xi_m)
        rows4[dpc] = growth(K, Mm) / tr["H"]
    d_fit = np.array([d for d in DMINS_PC if d >= 40 * XI_PC[f]])
    g_fit = np.array([rows4[d] for d in d_fit])
    p_fit = -float(np.polyfit(np.log(d_fit), np.log(g_fit), 1)[0])
    sat = abs(rows4[XI_PC[f] / 10] / rows4[XI_PC[f] / 3] - 1)
    b4[KEY(z, Mb, f)] = dict(rates={str(kk): v for kk, v in rows4.items()}, p=p_fit, sat=sat, G_xi=rows4[XI_PC[f]], G_1kpc=rows4[1000.0])
    P(f"    {KEY(z, Mb, f):22s}: Gamma/H at d_min = 3 kpc {rows4[3000.0]:.3g}, 1 kpc {rows4[1000.0]:.3g}, 10 pc {rows4[10.0]:.3g}, "
      f"0.1 pc {rows4[0.1]:.3g}, xi {rows4[XI_PC[f]]:.3g}, xi/10 {rows4[XI_PC[f] / 10]:.3g}; fitted p = {p_fit:.3f}; saturation {sat:.1%}")
ps = [v["p"] for v in b4.values()]; sats = [v["sat"] for v in b4.values()]
check("B4 [H4, pre-declared] COLD MATTER AT THE YIELD SURFACE: Gamma ~ d_min^(-p) with p in [0.20, 0.30] for d_min from 3 kpc to "
      "40 xi on every host (the divergent susceptibility (y - y_th)^(-1/2) averaged over the mode), saturating (xi/3 vs xi/10 "
      "within 10%) once the xi filter is resolved -- bounded by xi, resolution-dependent below it",
      f"p in [{min(ps):.3f}, {max(ps):.3f}]; saturation change max {max(sats):.1%}; Gamma(xi)/H in [{min(v['G_xi'] for v in b4.values()):.3g}, "
      f"{max(v['G_xi'] for v in b4.values()):.3g}]; Gamma(1 kpc)/H in [{min(v['G_1kpc'] for v in b4.values()):.3g}, "
      f"{max(v['G_1kpc'] for v in b4.values()):.3g}]",
      min(ps) >= 0.20 and max(ps) <= 0.30 and max(sats) < 0.10,
      "cold matter is the adversarial case: pressure (gas) or dispersion (stars, a wave field's quantum pressure) caps the mode "
      "width; a PM run with CDM-like particles is capped only by its cell size")
OUT["numbers"]["B4"] = b4
P(f"    {el()}")

# ---- B4b [ADDED AFTER B4's first run, which was a MUTATE run (B4 does not depend on MUTATE); written before its own first run].
#      B4 measured the maximum over the whole [r_Y/2, 2 r_Y] domain, which at z >= 2.5 is an interior dense-gas mode at coarse
#      d_min; B4b isolates the SURFACE mode: the eigenproblem on the layer |r - r_Y| <= max(30 d_min, 10 xi) (xi = 0 at its
#      ends), 60 nodes per side geometric from d_min.  Pre-declared: p in [0.20, 0.30] on all 24 hosts, fitted over
#      d_min in [40 xi, min(1 kpc, 0.01 r_Y)]; saturation Gamma(xi/3) vs Gamma(xi/10) within 10%.
banner("B4b [added after B4's first run] THE SURFACE MODE ISOLATED: cold matter on the layer |r - r_Y| <= max(30 d_min, 10 xi)")
DM_B = (1000.0, 300.0, 100.0, 30.0, 10.0, 3.0, 1.0)
b4b = {}
for (z, Mb, f) in GAL:
    xi_pc = XI_PC[f]; xi_m = xi_pc * KPC / 1e3
    tr = transition(z, Mb, f, 0.25)
    bgf = hy_host(z, Mb, f, tr["r"]); rY = r_yield(tr["r"], bgf["ybp"], bgf["yth"], yfun=lambda q: hy_host(z, Mb, f, q)["ybp"])
    rates = {}
    for dpc in DM_B + (xi_pc / 3, xi_pc / 10):
        dm = dpc * KPC / 1e3
        half = max(30 * dm, 10 * xi_m)
        if half >= 0.5 * rY:
            continue
        dd = np.geomspace(dm, half, 60)
        r = np.unique(np.concatenate([rY - dd[::-1], [rY], rY + dd]))
        rho = np.exp(np.interp(np.log(r), np.log(tr["r"]), np.log(tr["rho_b"])))
        Q2w, bg = node_Q2w(r, z, Mb, f)
        K, Mm = radial_operator(r, rho, Q2w, 0.0, bg["L"], cold_xi=xi_m)
        rates[dpc] = growth(K, Mm) / tr["H"]
    dfit = np.array([d for d in DM_B if 40 * xi_pc <= d <= min(1000.0, 0.01 * rY / KPC * 1e3) and d in rates])
    p_b = -float(np.polyfit(np.log(dfit), np.log([rates[d] for d in dfit]), 1)[0]) if len(dfit) >= 3 else float("nan")
    sat_b = abs(rates[xi_pc / 10] / rates[xi_pc / 3] - 1) if (xi_pc / 3 in rates and xi_pc / 10 in rates) else float("nan")
    b4b[KEY(z, Mb, f)] = dict(rates={str(k_): v for k_, v in rates.items()}, p=p_b, n_fit=len(dfit), sat=sat_b,
                             G_xi10=rates.get(xi_pc / 10, float("nan")))
    P(f"    {KEY(z, Mb, f):22s}: surface-mode Gamma/H at d_min = " + ", ".join(f"{k_:.3g} pc {v:.3g}" for k_, v in rates.items())
      + f"; p = {p_b:.3f} ({len(dfit)} points); saturation {sat_b:.1%}")
pb = [v["p"] for v in b4b.values()]; sb = [v["sat"] for v in b4b.values()]
check("B4b [added after B4's first run; pre-declared before its own] THE SURFACE MODE ISOLATED (cold matter, xi filter on): "
      "Gamma ~ d_min^(-p), p in [0.20, 0.30] on all 24 hosts (fit over 40 xi <= d_min <= min(1 kpc, 0.01 r_Y)), saturating "
      "within 10% between d_min = xi/3 and xi/10",
      f"p in [{np.nanmin(pb):.3f}, {np.nanmax(pb):.3f}] (hosts with a fit: {sum(np.isfinite(pb))}); saturation max {np.nanmax(sb):.1%}; "
      f"Gamma(xi/10)/H in [{np.nanmin([v['G_xi10'] for v in b4b.values()]):.3g}, {np.nanmax([v['G_xi10'] for v in b4b.values()]):.3g}]",
      all(np.isfinite(pb)) and np.nanmin(pb) >= 0.20 and np.nanmax(pb) <= 0.30 and all(np.isfinite(sb)) and np.nanmax(sb) < 0.10)
OUT["numbers"]["B4b"] = b4b
P(f"    {el()}")

# ============================================================================================ B5 on DE12's own layers
banner("B5  (reported) H_Y's exact radial growth on DE12's OWN layers (t in (0,1) +- 30%), 1e6 K gas")
b5 = {}
for (z, Mb, f) in GAL:
    tr = transition(z, Mb, f, 0.25)
    m = (tr["t"] > 0) & (tr["t"] < 1)
    ra, rb = tr["r"][m][0] * 0.7, tr["r"][m][-1] * 1.3
    r = np.geomspace(ra, rb, 500)
    rho = np.exp(np.interp(np.log(r), np.log(tr["r"]), np.log(tr["rho_b"])))
    Q2w, bg = node_Q2w(r, z, Mb, f)
    K, Mm = radial_operator(r, rho, Q2w, CS["1e6K"] ** 2, bg["L"])
    b5[KEY(z, Mb, f)] = growth(K, Mm) / tr["H"]
P("    " + ", ".join(f"{kk}: {v:.3g}" for kk, v in b5.items()) + "  [Gamma/H]")
check("B5 (reported) H_Y on DE12's own layers: the exact radial growth rate against DE12's gate (2e4 - 5e4 H at 1/kpc) and XR15's "
      "smoothed residual (1.1 - 2.8 H)", f"max {max(b5.values()):.3g} H, median {float(np.median(list(b5.values()))):.3g} H", True,
      load_bearing=False)
OUT["numbers"]["B5"] = b5

# ============================================================================================ B6 the heat pair's metric coupling
ratio_heat = []
for (z, Mb, f) in GAL:
    tr = transition(z, Mb, f, 0.25)
    bg = hy_host(z, Mb, f, tr["r"])
    gph = A0[f] * x_yield(bg["ybp"], bg["yth"])
    Aloc = 1 + np.minimum(1 / np.maximum(2 * np.sqrt(np.maximum(bg["ybp"] - bg["yth"], 1e-30)), 1e-30), 1e6)
    e_heat = 8 * math.pi * G6 * Aloc * gph / (kW * D12["L52"]["c"] ** 2)      # 2 k |dPhi| g/c^2 per |delta rho|^2, |dPhi| = 4 pi G A/k^2
    e_gas = CS["1e6K"] ** 2 / (2 * tr["rho_b"])
    ratio_heat.append(float(np.max(e_heat / e_gas)))
check("B6 (reported) the heat pair's metric coupling (the leafwise Laplacian depends on h_ij): its second variation is "
      "O(k^-1 g_ph/c^2) -- post-Newtonian and below the k^0 order; at k = 1/kpc its size relative to 1e6 K gas pressure",
      f"max ratio {max(ratio_heat):.1e}", max(ratio_heat) < 1e-6, load_bearing=False)
OUT["numbers"]["B6"] = max(ratio_heat)

# ============================================================================================ verdict
nlb = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
_ok = {k_: OUT['checks'][k_]['pass'] for k_ in ('B1', 'B2', 'B3', 'B4', 'B4b')}
_pf = {k_: ('PASS' if v else 'FAIL') for k_, v in _ok.items()}
_t12 = ("DE12's mechanism is absent from H_Y: the WKB count of the full action finds no k^0 term except the gas's own pressure"
        if _ok['B1'] else "the WKB count finds a k^0 term beyond the gas's own pressure (DE12's mechanism present)")
_t2 = ("DE12's convention (k = 1/kpc, 1e6 K) gives zero growth on all 24 hosts" if _ok['B2']
       else "DE12's convention (k = 1/kpc, 1e6 K) gives NONZERO growth")
_t3 = ("gas growth stays bounded and converged" if _ok['B3'] else "gas growth is NOT bounded/converged as declared")
_t4 = (f"cold matter grows faster the finer it is resolved, Gamma ~ d_min^(-1/4), up to the xi filter: the isolated surface mode has "
       f"p = {np.nanmin(pb):.3f}-{np.nanmax(pb):.3f} and reaches {np.nanmin([v['G_xi10'] for v in b4b.values()]):.3g}-"
       f"{np.nanmax([v['G_xi10'] for v in b4b.values()]):.3g} H at xi" if _ok['B4b'] else
       f"the isolated cold-matter surface mode does NOT follow d_min^(-1/4) as declared (p = {np.nanmin(pb):.3f}-{np.nanmax(pb):.3f})")
_t4d = (f"B4 as declared ({_pf['B4']}) fitted the whole domain's maximum, which at z >= 2.5 and d_min >= 1 kpc is an interior "
        f"dense-gas mode (p down to {min(v['p'] for v in b4.values()):.3f})" if not _ok['B4'] else f"B4 as declared: {_pf['B4']}")
P(f"""  (b) {_t12} (B1: {_pf['B1']}), and {_t2} (B2: {_pf['B2']}).
      H_Y's yield surfaces carry a divergent longitudinal susceptibility, Q'' = dx/dy ~ (y - y_th)^(-1/2): it enters the baryons'
      k^-2 (Jeans) term; {_t3} (B3: {_pf['B3']}; max {gmax3:.3g} H); {_t4} (B4b: {_pf['B4b']});
      {_t4d}.
  Not 'closed'.  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nlb}.  Time {time.time() - T0:.0f} s.""")
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"  wrote {os.path.basename(fn)}")
_OUTF.close()
sys.exit(1 if nlb else 0)
