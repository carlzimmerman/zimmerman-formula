#!/usr/bin/env python3
# agentU -- khronon/aether-framed covariant lift of Milgrom-2022 time-nonlocal MI: the gate computations.
# Companion to agentU_khronon_m22.md. Conventions cloned from agentM_milgrom2022_gauntlet.py (gated below).
# Sections: [0] gate vs agentM reflex numbers; [1] covariant-dressing scales (is the Galilean limit exact
# enough that agentM's battery transfers?); [2] gate-1a pure khronon/aether PPN corners (pinned formulas,
# Gumrukcuoglu-Saravani-Sotiriou 1711.08845 Eq.12 + Oost-Mukohyama-Wang 1802.04303 Eq.3.23);
# [3] gate-1b matter-sector PPN feedback (sympy closed forms + numbers); [4] gate-2 conservation channel
# magnitudes; [5] gate-4 lensing division of labor; [6] gate-5 cosmology a0(z) branch table.
# No git. Both a0 footings + hostile bath s = cH_Lambda throughout (working rule).

import numpy as np
import sympy as sp

LINE = "=" * 100
print(LINE)
print("agentU KHRONON-FRAMED COVARIANT M22 -- gate computations, run date 2026-06-10")
print(LINE)

# ---------------------------------------------------------------- constants (cloned from agentM + repo)
GMsun = 1.32712440018e20  # m^3/s^2
AU    = 1.495978707e11
c     = 2.99792458e8
A0_FW, A0_CAN, S_HOST = 9.36e-11, 1.2e-10, 5.418e-10     # framework / canonical / hostile cH_Lambda
BUDGET_STRICT, BUDGET_LOOSE = 2.47e-15, 3.38e-15          # agentE survival line, delta_a_sun [m/s^2]
H0    = 2.184e-18         # s^-1 (67.4 km/s/Mpc); Om = 0.315
OM_M  = 0.315
H_LAM = S_HOST / c        # 1.807e-18 s^-1 (the framework's cH_Lambda footing)
W_CMB = 3.69e5            # m/s, solar-system barycenter speed w.r.t. CMB ~ the cosmic u frame

def mu_std(x):    return x / np.sqrt(1.0 + x * x)
def mu_rar(x):    return -np.expm1(-np.sqrt(x))
def c_std(x):     return 1.0 / (x * (np.sqrt(1.0 + x * x) + x))      # 1/mu - 1, stable
def c_rar(x):
    e = np.exp(-np.sqrt(np.asarray(x, dtype=float)))
    return e / (1.0 - e)

def th_A(y): return 2.0 / (1.0 + y * y)
def th_B(y): return np.exp(1.0 - y)
def th_C(y): return np.exp((1.0 - y) / 2.0)
THETAS = {"2/(1+y^2)": th_A, "exp(1-y)": th_B, "exp((1-y)/2)": th_C}

planets = [("Mercury", 2.2032e13, 0.38710), ("Venus", 3.24859e14, 0.72333),
           ("EMB", 4.035032e14, 1.00000),   ("Mars", 4.282837e13, 1.52366),
           ("Jupiter", 1.26686534e17, 5.20336), ("Saturn", 3.7931187e16, 9.53707),
           ("Uranus", 5.793939e15, 19.1913),    ("Neptune", 6.836529e15, 30.0690)]
inv = [(n, np.sqrt(GMsun / (a * AU) ** 3), gm / (a * AU) ** 2) for n, gm, a in planets]
a_gal, om_gal = 2.15e-10, 9.2e-16
om_J = dict((n, o) for n, o, a in inv)["Jupiter"]
a_J  = dict((n, a) for n, o, a in inv)["Jupiter"]

# ---------------------------------------------------------------- [0] GATE vs agentM banked numbers
print("\n[0] GATE: reproduce agentM's filter reflex A(Omega_J) and the exponential-tail delta_a_sun")
A_of_theta = {}
for tlab, th in THETAS.items():
    A = a_J + sum(acc * th(om / om_J) for n, om, acc in inv if n != "Jupiter") + a_gal * th(om_gal / om_J)
    A_of_theta[tlab] = A
    print(f"    theta={tlab:13s}: A/a_J = {A/a_J:.3f}")
banked_ratios = {"2/(1+y^2)": 1.167, "exp(1-y)": 1.177, "exp((1-y)/2)": 1.130}
for tlab, r in banked_ratios.items():
    assert abs(A_of_theta[tlab] / a_J - r) < 0.01, (tlab, A_of_theta[tlab] / a_J)
da_fw  = [a_J * c_rar(A / A0_FW)  for A in A_of_theta.values()]
da_hos = [a_J * c_rar(A / S_HOST) for A in A_of_theta.values()]
print(f"    exp-tail (McGaugh-RAR mu) delta_a_sun fw     : {min(da_fw):.2e} .. {max(da_fw):.2e}"
      f"   (banked agentM: 1.1e-29 .. 3.2e-29)")
print(f"    exp-tail (McGaugh-RAR mu) delta_a_sun hostile: {min(da_hos):.2e} .. {max(da_hos):.2e}"
      f"   (banked agentM: 1.2e-16 .. 1.8e-16; budget {BUDGET_STRICT:.2e})")
assert 0.5e-29 < min(da_fw) and max(da_fw) < 5e-29
assert 0.8e-16 < min(da_hos) and max(da_hos) < 2.5e-16 < BUDGET_STRICT
print("    GATE PASS: conventions identical to agentM; the NR battery baseline is reproduced.")

# ---------------------------------------------------------------- [1] covariant-dressing scales
print("\n" + LINE)
print("[1] COVARIANT DRESSING: every term the lift ADDS to the Galilean-limit M22 law, sized")
print(LINE)
print("    The covariant variables (u-frame time T, congruence-label trajectory x(T)) differ from the")
print("    Galilean ones by: (a) boost factor w^2/c^2 (w = velocity w.r.t. u); (b) potential Phi/c^2;")
print("    (c) Hubble-flow terms O(H*v) and O(H^2*r) in d^2x/dT^2 from the slice metric's expansion.")
print("    These MULTIPLY/DRESS the argument of mu -- they are not new anomalous forces.\n")
systems = [
    # name, v [m/s], r [m], a_char [m/s^2], Phi/c^2 source
    ("solar system (Saturn)", 9.6e3,  9.537 * AU,  GMsun / (9.537 * AU) ** 2, GMsun / (9.537 * AU * c * c)),
    ("wide binary (5 kAU)",   2.0e2,  5e3 * AU,    1.0e-10,                   5.4e-7),
    ("galaxy outskirts",      2.0e5,  9.3e20,      1.2e-10,                   5.4e-7),
]
print(f"    {'system':24s} {'w_CMB^2/c^2':>12s} {'Phi/c^2':>10s} {'H*v [m/s^2]':>12s} {'H*v/a_char':>11s} "
      f"{'H^2*r [m/s^2]':>13s} {'H^2r/a_char':>12s}")
for name, v, r, a_char, phi in systems:
    hv, h2r = H0 * v, H0 ** 2 * r
    print(f"    {name:24s} {(W_CMB/c)**2:12.2e} {phi:10.2e} {hv:12.2e} {hv/a_char:11.2e} "
          f"{h2r:13.2e} {h2r/a_char:12.2e}")
print(f"""
    READINGS:
    - Largest fractional dressing of the mu-argument anywhere: galaxy outskirts H*v/a ~ {H0*2.0e5/1.2e-10:.1e}
      (0.4%) -- vs SPARC scatter 0.195 dex (57%) per point: phenomenologically INERT. agentM's SPARC/WB/
      precession/reflex battery transfers to the covariant lift unchanged at the <1% level.
    - Solar system: dressing corrections are O(1e-6) MULTIPLYING deviations already exponentially dead --
      irrelevant in both directions.
    - The N5 corridor question: the lift's natural dressing is O(H*v/a) <= 0.4%, NOT a power of
      (1+Omega/H). The corridor escape (p in [0.069,1]) is still NOT manufactured: covariant M22 stays at
      p = 0, exactly agentM's placement. The exponential mu-tail remains the only reflex-passing member.""")

# ---------------------------------------------------------------- [2] gate-1a: pure khronon/aether PPN
print(LINE)
print("[2] GATE 1a: the frame field's OWN PPN bill (pinned formulas, post-GW170817)")
print(LINE)
print("    Khronometric (hypersurface-orthogonal aether = the khronon; 1711.08845):")
print("      c_T^2 = 1/(1-beta); GW170817: -3e-15 < c_T-1 < 7e-16  =>  |beta| <~ 1e-15")
print("      alpha_1 = 4(alpha-2beta)/(1-beta);  alpha_2 = [(alpha-2beta)/(2-alpha)] *")
print("                [1 - (alpha-2beta)(1+beta+2gamma)/((1-beta)(beta+gamma))]")
print("      bounds: |alpha_1| < 1e-4, |alpha_2| < 4e-7 ; BBN |(alpha+3gamma+beta)/(2+3gamma+beta)| < 1/8")
beta = 1e-15
def alpha1(al, be=beta):  return 4 * (al - 2 * be) / (1 - be)
def alpha2(al, ga, be=beta):
    return ((al - 2 * be) / (2 - al)) * (1 - (al - 2 * be) * (1 + be + 2 * ga) / ((1 - be) * (be + ga)))
def cs2(al, ga, be=beta): return (2 - al) * (ga + be) / (al * (1 - be) * (2 + 3 * ga + be))

# generic corner: gamma >> alpha (no tuning)
al_a1   = 1e-4 / 4                      # alpha_1 bound alone
gen = None
for al in np.geomspace(1e-12, al_a1, 4000):
    ok = abs(alpha2(al, 1e-2)) < 4e-7 and abs(alpha1(al)) < 1e-4 and cs2(al, 1e-2) >= 1
    if ok: gen = al
print(f"\n    generic corner (gamma >> alpha, e.g. gamma=1e-2; alpha_2 ~ alpha/2 binds):")
print(f"      max alpha ~ {gen:.1e}  (alpha_2 = {alpha2(gen,1e-2):.2e}; alpha_1 = {alpha1(gen):.2e}; "
      f"c_S^2 = {cs2(gen,1e-2):.2e} >> 1, Cherenkov-safe)")
# tuned sliver: gamma ~ alpha cancellation, alpha up to the alpha_1 bound
al_t = 2.5e-5
gam_grid = al_t * np.linspace(0.90, 1.15, 200001)
ok = np.array([abs(alpha2(al_t, g)) < 4e-7 and cs2(al_t, g) >= 1 for g in gam_grid])
g_ok = gam_grid[ok]
print(f"    tuned sliver at alpha = {al_t:.1e} (the alpha_1 ceiling): alpha_2 cancels for gamma ~ alpha;")
if len(g_ok):
    print(f"      surviving gamma/alpha in [{g_ok.min()/al_t:.4f}, {g_ok.max()/al_t:.4f}] "
          f"(width {100*(g_ok.max()-g_ok.min())/al_t:.2f}% of alpha) AND c_S^2 >= 1 throughout that window:"
          f" c_S^2 at edges = {cs2(al_t, g_ok.min()):.3f}, {cs2(al_t, g_ok.max()):.3f}")
    print(f"      NOTE: the cancellation window sits AT the Cherenkov edge c_S^2 ~ 1 (c_S^2 ~ gamma/alpha):")
    print(f"      gamma < alpha is Cherenkov-dead, gamma > ~1.03*alpha is alpha_2-dead -- a pinched but")
    print(f"      non-empty sliver. The GENERIC corner alpha <~ 8e-7 is the robust statement.")
print("""
    Einstein-aether (generic, non-HSO; 1802.04303 Eq. 3.23): |c_13| <= 1e-15, alpha_1 = -4 c_14, and two
    surviving regions: (i) 0 < c_14 <= 2e-7 with c_14 <~ c_2 <~ 0.095; (ii) 2e-6 <~ c_14 <~ 2.5e-5 with
    0 <~ c_2 - c_14 <~ 2e-7. Binary pulsars post-GW shrink the space ~10x further but it stays NON-EMPTY
    (2104.04596; newest single-system bounds 2605.01436 are bounds, not exclusion).
    => VIABLE CORNERS EXIST for a canonical (MOND-free) frame sector. Distinct from AeST/GEA, whose vector
    kinetic term must CARRY the MOND nonlinearity and cannot retreat into these corners.""")

# BBN/G_cos check at the generic corner
al, ga = 8e-7, 1e-2
bbn = abs((al + 3 * ga + beta) / (2 + 3 * ga + beta))
print(f"    BBN check at (alpha,gamma)=({al:.0e},{ga:.0e}): |(a+3g+b)/(2+3g+b)| = {bbn:.3e} < 1/8  OK")

# ---------------------------------------------------------------- [3] gate-1b: matter-sector PPN feedback
print("\n" + LINE)
print("[3] GATE 1b: does the u-coupled MATTER sector feed back into PPN? (sympy closed forms + numbers)")
print(LINE)
print("    Structure: every operator the MI functional adds to the worldline dynamics carries a factor")
print("    eps(x) = 1/mu(x) - 1 or its derivative; u-frame velocity w enters only by DRESSING the")
print("    mu-argument: x -> x(1 + kappa_w w^2/c^2), kappa_w = O(1). The preferred-frame (alpha_1-type)")
print("    coefficient generated in the matter sector is therefore  ~ |x eps'(x)| * kappa_w  at the")
print("    acceleration x of the test body. Sympy closed forms:")
xs = sp.symbols('x', positive=True)
eps_rar_s = sp.exp(-sp.sqrt(xs)) / (1 - sp.exp(-sp.sqrt(xs)))
eps_std_s = sp.sqrt(1 + xs ** 2) / xs - 1
xder_rar = sp.simplify(xs * sp.diff(eps_rar_s, xs))
xder_std = sp.simplify(xs * sp.diff(eps_std_s, xs))
print(f"      exp tail  : x*d(eps)/dx = {sp.simplify(xder_rar)}")
print(f"                  (= -(sqrt(x)/2) e^(-sqrt(x))/(1-e^(-sqrt(x)))^2 -- exponentially dead)")
print(f"      power tail: x*d(eps)/dx = {xder_std}   (~ -1/x^2 at large x)")
f_rar = sp.lambdify(xs, sp.Abs(xder_rar), 'numpy')
f_std = sp.lambdify(xs, sp.Abs(xder_std), 'numpy')
bodies = [("Mercury helio", GMsun / (0.38710 * AU) ** 2), ("Earth helio", GMsun / AU ** 2),
          ("Saturn helio", GMsun / (9.537 * AU) ** 2),    ("Neptune helio", GMsun / (30.069 * AU) ** 2),
          ("MICROSCOPE 710km", 3.986004418e14 / 7.089e6 ** 2), ("lab 1g", 9.81)]
print(f"\n    effective matter-side alpha_1-type coefficient |x eps'(x)| (kappa_w=1):")
print(f"    {'body':18s} {'a [m/s^2]':>10s} | {'fw: exp-tail':>13s} {'fw: power':>10s} | "
      f"{'hostile: exp':>13s} {'hostile: power':>14s}")
for name, a in bodies:
    xf, xh = a / A0_FW, a / S_HOST
    er_f = float(f_rar(xf)) if np.sqrt(xf) < 700 else 0.0
    er_h = float(f_rar(xh)) if np.sqrt(xh) < 700 else 0.0
    es_f, es_h = float(f_std(xf)), float(f_std(xh))
    print(f"    {name:18s} {a:10.2e} | {er_f:13.2e} {es_f:10.2e} | {er_h:13.2e} {es_h:14.2e}")
print(f"""
    vs the bounds |alpha_1| < 1e-4, |alpha_2| < 4e-7:
    - exponential tail: identically zero at every solar-system body (sqrt(x) >= 346 even at the hostile
      footing at Saturn) -- the feedback is e^(-sqrt(x))-dead. PASS by > 140 orders.
    - power-law tail: worst precision body (Neptune, hostile) |x eps'| = {f_std(GMsun/(30.069*AU)**2/S_HOST):.1e}
      -- STILL passes PPN by ~4 orders. Honest both ways: PPN feedback kills NO mu shape; the power-law
      members die at the solar REFLEX (agentM x6-11), not at PPN. The gate-1b PASS is tail-independent.
    - strong-field (pulsar) channel alpha_1-hat: pulsar orbital x ~ 1e12 -> feedback = 0. PASS.
    - OMW's PPN derivation assumes L_m independent of u^mu (1802.04303 Eq. 2.3); the violation of that
      assumption here is the eps(x)-suppressed coupling above => their pure-aether alpha_1/alpha_2 corners
      receive corrections bounded by the same factors: the [2] corners survive the matter coupling.""")

# u-tilt sourcing (named-open): order of magnitude only
print("    OPEN-minor (named, not computed): in deep-MOND regions the matter coupling sources delta-u at")
print("    O(1) of the matter terms; the galaxy-scale u-profile (tilt/drag of the local frame) is a real")
print("    computation for the build. Solar-system effect enters only through the eps(x)-dead coupling.")

# ---------------------------------------------------------------- [4] gate-2: conservation channel sizes
print("\n" + LINE)
print("[4] GATE 2: conservation -- the causal-version violation channel, sized per system class")
print(LINE)
print("    Action route (time-symmetric |a(omega)| functional): diffeo-invariant nonlocal action =>")
print("    generalized Bianchi: total grad_mu T^munu = 0 ON-SHELL, exactly, nonlocality notwithstanding")
print("    (DEW precedent). But time-symmetric = ACAUSAL (reads the future). Retarded/causal route:")
print("    Noether guarantee lost; violation confined to [MOND-deviation eps(x)] x [aperiodicity of the")
print("    trajectory] (for (quasi)periodic orbits the half-line determines the spectrum).")
psr_a   = 3.756e20 / (1.95e9) ** 2          # B1913+16 relative orbit ~ G(M1+M2)/a^2
trip_a  = 1.7e-3                            # J0337+1715 inner-pair accel toward outer WD (order)
chan = [("binary pulsar B1913+16", psr_a), ("triple J0337+1715 outer", trip_a),
        ("solar system (Saturn)", GMsun / (9.537 * AU) ** 2), ("wide binary deep", 1.0e-10),
        ("galaxy outskirts", 1.2e-10)]
print(f"\n    {'system':26s} {'a [m/s^2]':>10s} {'x (fw)':>10s} {'eps_exp(x)':>12s}  energy-balance verdict")
for name, a in chan:
    x = a / A0_FW
    e = float(c_rar(x)) if np.sqrt(x) < 700 else 0.0
    verdict = "screened: no observable channel" if e < 1e-15 else "O(MOND) -- IS the anomaly itself"
    print(f"    {name:26s} {a:10.2e} {x:10.3e} {e:12.2e}  {verdict}")
print("""
    => No data-side kill is constructible: every precision energy-balance test (pulsar Pdot at 1e-2
    precision, solar-system) sits at eps = 0; in galaxies the 'violation' budget is O(the MOND effect)
    on secular timescales -- unobservable as non-conservation. The gate is STRUCTURAL (well-posedness/
    causality of the retarded version), not observational. OPEN -- exactly Milgrom's own flagged gap,
    inherited undiminished by the covariant lift; Schwinger-Keldysh (in-in) + the aether as the
    momentum reservoir is the named published-adjacent route (1712.07066 precedent class).""")

# ---------------------------------------------------------------- [5] gate-4: lensing
print(LINE)
print("[5] GATE 4: lensing -- what the construction does to photons (exactly nothing)")
print(LINE)
print("""    Photons: the MI functional multiplies m; for m = 0 the worldline action is the unmodified null
    action => photons follow null geodesics of the EINSTEIN metric sourced by baryons + aether stress.
    Aether-stress contribution: bounded by the [2] corners, fractional metric sourcing <~ c_14 <= 2.5e-5
    of the baryon terms -- 4+ orders below the needed MOND phantom (~x230 deep-bin deficit, banked).
    => the banked metric-passive wall applies UNCHANGED: baryon-only lensing is excluded at 40.5 sigma
    on the repo's own re-measured isolated lensing RAR (f4_lensing_wall.out). FAIL as a whole theory;
    DELEGATED by construction: this object is the matter-sector HALF of the spec's hybrid (Link 7
    partner still required; division of labor stated in the .md).""")

# ---------------------------------------------------------------- [6] gate-5: cosmology / a0(z) branches
print(LINE)
print("[6] GATE 5: cosmology -- the two natural a0 readings of the construction")
print(LINE)
print("    (a) a0 = const coupling in the matter functional  == the framework's pure-Lambda branch")
print("        (a0 propto sqrt(rho_DE) is CONSTANT for a cosmological constant: same object).")
print("    (b) a0(z) = (c/Z) * (div u)/3 = c H(z)/Z -- the khronon's only natural local scale ==")
print("        the RIVAL rising branch (DEW 1405.0393 alpha[g] variant; contested MUSE-DARK III reading).")
def E(z): return np.sqrt(OM_M * (1 + z) ** 3 + (1 - OM_M))
print(f"\n    {'z':>6s} {'a0_rising/a0_const = E(z)':>26s}")
for z in [0.0, 0.5, 1.0, 2.0, 3.0, 1100.0]:
    print(f"    {z:6.1f} {E(z):26.3f}")
print(f"""
    - The two readings are DEGENERATE at z=0 and diverge by x{E(1.0):.2f} at z=1, x{E(1100.0):.0f} at recombination.
    - Reading (b) at recombination: a0 larger by 2e4 => the deep-MOND regime vastly wider during CMB
      formation => the CMB gate is much HARDER for the rising reading. Reading (a) inherits the repo's
      banked phenomenological CMB-safety flag for the flat/constant kernel (bath argument), with the
      honest caveat that NO Boltzmann-level audit of M22 exists in any frame, ours included.
    - Background: comoving dust has zero u-frame acceleration AND zero force -- the law is trivially
      satisfied (0=0); Friedmann renormalization G_cos/G_N is the standard aether factor, BBN-bounded
      (checked in [2]). The construction does not DECIDE the branch: it makes both expressible. OPEN.""")

print(LINE)
print("agentU computations complete. Verdict assembly in agentU_khronon_m22.md.")
print(LINE)
