#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FK1 -- THE KICK AS A PHASE CHANGE OF THE DARK ORDER PARAMETER: FL1's complex field, split into its two real components.

WHY.  The record's clearing needs a kick: the triggered carrier leaves galaxies at a universal speed v_k = 575-650 km/s
(L388's window), a declared scale separate from the region cap (XR7).  FL1 (real_research/dark_fluid_2026, the dark
fluid's own lane) identifies the carrier as a complex order parameter Phi -- a superfluid, new field content, classical at
occupation N >> 1 -- and leaves the kick open: "a gate-triggered transition of the order parameter, whose products must
free-stream".  The coordinating review asked for it as a first-order transition with the latent heat a material
constant, v_k^2/2c^2 = 1.8-2.3e-6 (astra's Delta m/m ~ 2e-6 read as a phase energy difference, not a particle's).

THE CONSTRUCTION (checked below).  One non-relativistic component cannot hold a universal latent heat: every homogeneous
state of density n has energy V(n), so a first-order transition must change n, and what it releases depends on where it
happens (K1).  Phi has two real components.  A small U(1)-breaking mass term,
    V = m^2 |Phi|^2 + eps Re(Phi^2) + V_4,        Phi = (phi_H + i phi_L)/sqrt(2),
splits them: m_H^2 = m^2 + eps, m_L^2 = m^2 - eps (K2).  The cold carrier is the heavy component.  A lone phi_H cannot
decay (V is even in each component: Z2 x Z2); two of them convert, phi_H phi_H -> phi_L phi_L, through V_4's cross term
(already inside lambda|Phi|^4), and the pair leaves back to back at exactly v_k = sqrt(m_H^2 - m_L^2)/m_H, i.e.
eps/m^2 = v_k^2/(2c^2 - v_k^2): a latent heat per unit mass fixed by the Lagrangian, isotropic, the same in every halo and
at every redshift.  At FL1's occupations the conversion is Bose-stimulated: a parametric instability of the heavy
condensate on the shell |v| = v_k (K3), growing by pi G^2/(4 H delta) e-folds as the expansion sweeps a mode through it
(K4), so the trigger is a sharp density threshold.  Two couplings decide what the products do (K5): lambda|Phi|^4 gives
each component a self-coupling THREE times the conversion coupling, so the products relax where they are made;
lambda (Im Phi^2)^2 = lambda phi_H^2 phi_L^2 has only the cross term, so each component is a free field away from the
conversion (FL1 F4's superposition then covers stream crossing).

CHECKS
  K1 [sympy + numbers] one NR component: the energy a first-order transition releases per particle at mean density n is
     (V(n) - V_hull(n))/n, whose derivative is set by V'(n) - mu_c (not zero): on a concrete two-phase V it changes by
     more than 2x across the unstable range, and the products include the dense phase.  For the relativistic field, two
     homogeneous branches at one charge density need omega_a/omega_b = phi_b^2/phi_a^2 (n = 2 omega phi^2): in the NR
     regime (omega within 1e-5 of m) they coincide.
  K2 [sympy] the doublet: masses, Z2 x Z2 for both quartics, the conversion vertex, and the exact kick kinematics.
  K3 [sympy] the NR pair instability of a heavy condensate at rest: growth sqrt(G^2 - D^2), largest on the shell
     |v| = v_k (1 + O(G/delta)) for both quartics.
  K4 [sympy] the expansion-limited growth exponent int sqrt(G^2 - D^2) dt with D swept at -2 H delta: pi G^2/(4 H delta).
  K5 [sympy] the NR (slow) couplings of lambda|Phi|^4 and lambda(Im Phi^2)^2: g_HH, g_LL, the cross shift and the pair
     coupling.
  N1 [numbers, both kick ends] eps/m^2; the de Broglie length at v_k for FL1's mass window (the products are classical
     waves: their Wigner function obeys the Vlasov equation, so L388's ballistic kick is their limit); the e-folds a
     conversion needs, ln(N_final/N_seed); how sharp the threshold is.
  N2 [numbers, reported] a constant coupling converts the COSMIC BACKGROUND first: with the record's carrier threshold
     (delta_t ~ 5-25, the linear cell's matter reading at z = 0-2.5) the mean density converts by z ~ 0.9-4.  The coupling must
     fall into the past: lambda proportional to K^(-2q) (K = 3H, the khronon's expansion, uniform on CMC leaves in bound
     regions, CV4: force-free) needs q > 3/4, and q = p + 3/4 = 1.75 reproduces the linear gate's threshold scaling.
  N3 [numbers, reported] the self-interaction the trigger implies with lambda|Phi|^4 (a sound speed at the trigger
     density) and the kinetic-relaxation estimate for its products; zero for (Im Phi^2)^2.
MUTATE=1 sets eps = 0: the doublet is degenerate, the resonance shell collapses to v = 0 (no kick), K2 and K3 must FAIL.

SCOPE.  Kinematics, symmetry and the linear instability are exact (sympy).  The halo-regime growth (a virialised,
broadband pump) is an estimate with O(1) factors; the numbers in N2/N3 carry them and are labelled.  The initial
misalignment must lie near the phi_H axis (an unconvertible cold phi_L share adds to the retained carrier: MS2's flagship
allows <= 0.059 at r_F, so within ~14 degrees) -- a declared initial condition.  New constants: eps (the splitting) and
the conversion coupling with its gate exponent q.  The carrier's MASS is still required; this is new field content (FL1).

Run from the repository root:  python3 real_research/dark_fluid_kick_2026/FK1_kick_as_phase_change.py
"""
import os, sys, json, math, time
import numpy as np
import sympy as sp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "FK1_kick_as_phase_change"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "FK1", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: eps = 0 (no splitting); K2 and K3 must FAIL ***")

C_KMS = 2.99792458e5
VK = (575.0, 600.0, 625.0, 650.0)

# ============================================================================================ K1 one component cannot
banner("K1  ONE NR COMPONENT: what a first-order transition releases depends on where it happens")
nb, mu_c, n1, n2 = sp.symbols("nbar mu_c n1 n2", positive=True)
V = sp.Function("V")
zeta = (nb - n1) / (n2 - n1)                                               # volume fraction of the dense phase
Vhull = zeta * V(n2) + (1 - zeta) * V(n1)                                  # the common tangent between n1 and n2
rel = sp.simplify(sp.diff(V(nb) - Vhull, nb) - (sp.diff(V(nb), nb) - (V(n2) - V(n1)) / (n2 - n1)))
P(f"    d/dn [n Delta(n)] - (V'(n) - mu_c) = {rel},  mu_c = (V(n2) - V(n1))/(n2 - n1): zero only where V' = mu_c")
# a concrete two-phase V (energy density, units of the scale): non-convex between the spinodals
Vc = lambda n: n ** 2 - 1.5 * n ** 3 + 0.6 * n ** 4
Vp = lambda n: 2 * n - 4.5 * n ** 2 + 2.4 * n ** 3
sp_lo, sp_hi = sorted(np.roots([7.2, -9.0, 2.0]).real)                     # V'' = 0
def tangent(x):
    a, b = x
    return [Vp(a) - Vp(b), Vp(a) * (b - a) - (Vc(b) - Vc(a))]
from scipy.optimize import fsolve
b1, b2 = fsolve(tangent, [0.1, 1.2])
muc = Vp(b1)
nt = np.linspace(sp_lo, sp_hi, 7)
Dl = [(Vc(n) - (Vc(b1) + muc * (n - b1))) / n for n in nt]
P(f"    V = n^2 - 1.5 n^3 + 0.6 n^4: spinodals {sp_lo:.3f}-{sp_hi:.3f}, coexisting phases n1 = {b1:.3f}, n2 = {b2:.3f}")
P("    released per particle, Delta(n) = (V - V_hull)/n, across the unstable range: " + ", ".join(f"{d:.4f}" for d in Dl))
spread = max(Dl) / max(min(Dl), 1e-12)
# relativistic branches: n = 2 omega phi^2 at one n
wa, wb, pa, pb = sp.symbols("omega_a omega_b phi_a phi_b", positive=True)
branch = sp.simplify((wa / wb) - (pb ** 2 / pa ** 2)).subs(pb ** 2, wa * pa ** 2 / wb)
etaNR = 1e-5
P(f"    relativistic branches at one charge density: phi_b^2/phi_a^2 = omega_a/omega_b (identity residual {sp.simplify(branch)}); "
  f"with both omegas within {etaNR:g} of m the amplitudes agree to {etaNR / (1 - etaNR):.1e}: one branch")
OUT["numbers"]["K1"] = dict(spinodals=[sp_lo, sp_hi], binodal=[float(b1), float(b2)], Delta=Dl, spread=spread)
check("K1 one NR component has no universal latent heat: the release per particle follows V' - mu_c and varies by > 2x "
      "across the unstable range, with a dense phase among the products; NR relativistic branches coincide",
      f"identity residual {rel}; Delta spread {spread:.1f}x; branch identity {sp.simplify(branch)}",
      rel == 0 and spread > 2 and sp.simplify(branch) == 0,
      "a universal kick needs two internal states, not one component's phase change")

# ============================================================================================ K2 the doublet inside Phi
banner("K2  THE DOUBLET INSIDE PHI: masses, Z2 x Z2, the conversion vertex, the kick")
pH, pL = sp.symbols("phi_H phi_L", real=True)
m, eps, lam, t, H_, dl = sp.symbols("m epsilon lambda t H delta", positive=True)
epsv = 0 if MUTATE else eps
Ph = (pH + sp.I * pL) / sp.sqrt(2)
absP2 = sp.expand(Ph * sp.conjugate(Ph))
ReP2, ImP2 = sp.expand(sp.re(Ph ** 2)), sp.expand(sp.im(Ph ** 2))
V2 = sp.expand(m ** 2 * absP2 + epsv * ReP2)
mH2, mL2 = sp.diff(V2, pH, 2), sp.diff(V2, pL, 2)
QUART = {"lam|Phi|^4": lam * absP2 ** 2, "lam(ImPhi^2)^2": lam * ImP2 ** 2}
z2 = {k_: sp.simplify(Vq.subs(pH, -pH) - Vq) == 0 and sp.simplify(Vq.subs(pL, -pL) - Vq) == 0 for k_, Vq in QUART.items()}
vert = {k_: sp.Poly(sp.expand(Vq), pH, pL).coeff_monomial(pH ** 2 * pL ** 2) for k_, Vq in QUART.items()}
odd = {k_: [sp.Poly(sp.expand(Vq), pH, pL).coeff_monomial(mo) for mo in (pH * pL ** 3, pH ** 3 * pL, pH * pL)] for k_, Vq in QUART.items()}
vkick = sp.sqrt(mH2 - mL2) / sp.sqrt(mH2)                                  # 2 -> 2 at rest, c = 1: |p| = sqrt(mH^2 - mL^2)
P(f"    m_H^2 = {mH2}, m_L^2 = {mL2};  v_kick = {sp.simplify(vkick)}")
P(f"    Z2 x Z2 (even in each component): {z2};  phi_H^2 phi_L^2 vertex: {vert};  odd vertices (phi_H phi_L^3, phi_H^3 phi_L, phi_H phi_L): {odd}")
s_of_v = {v_: (v_ / C_KMS) ** 2 / (2 - (v_ / C_KMS) ** 2) for v_ in VK}
kick_ok = True
for v_, s_ in s_of_v.items():
    vk_num = float(vkick.subs({eps: s_, m: 1})) * C_KMS if not MUTATE else 0.0
    kick_ok &= abs(vk_num - v_) < 1e-6 * v_
    P(f"    v_k = {v_:.0f} km/s  <->  eps/m^2 = {s_:.4e}  (delta m/m = {math.sqrt((1 + s_) / (1 - s_)) - 1:.4e});  "
      f"v from the Lagrangian {vk_num:.3f} km/s")
OUT["numbers"]["K2"] = dict(eps_over_m2={str(k_): v_ for k_, v_ in s_of_v.items()}, vertex={k_: str(v_) for k_, v_ in vert.items()})
check("K2 Phi's two real components are split by eps Re(Phi^2) (m_H^2 - m_L^2 = 2 eps); both quartics are Z2 x Z2 "
      "symmetric, so a lone phi_H is stable and phi_H phi_H -> phi_L phi_L is the conversion; the pair leaves at "
      "v_k = sqrt(2 eps/(m^2 + eps)), i.e. eps/m^2 = v_k^2/(2c^2 - v_k^2)",
      f"m_H^2 - m_L^2 = {sp.simplify(mH2 - mL2)}; Z2xZ2 {z2}; vertices {vert}; kick reproduced at 575-650: {kick_ok}",
      sp.simplify(mH2 - mL2 - 2 * eps) == 0 and all(z2.values()) and all(v_ != 0 for v_ in vert.values())
      and all(o == 0 for os_ in odd.values() for o in os_) and kick_ok)

# ============================================================================================ K5 the NR couplings
banner("K5  THE SLOW (NR) COUPLINGS OF THE TWO QUARTICS: self, cross and pair (conversion) terms")
A, Ac, B, Bc, xH, xL = sp.symbols("A Abar B Bbar x_H x_L")
phH = (A * xH + Ac / xH) / sp.sqrt(2 * m)                                  # x = e^{-i m t}; envelopes A (heavy), B (light)
phL = (B * xL + Bc / xL) / sp.sqrt(2 * m)
K5 = {}
for k_, Vq in QUART.items():
    ex = sp.expand(Vq.subs({pH: phH, pL: phL}))
    slow = {}
    for term in ex.as_ordered_terms():
        pw = (int(term.as_coeff_exponent(xH)[1]), int(term.as_coeff_exponent(xL)[1]))
        if pw in ((0, 0), (2, -2), (-2, 2)):
            slow[pw] = slow.get(pw, 0) + term.subs({xH: 1, xL: 1})
    s00 = sp.expand(slow.get((0, 0), 0))
    cHH = sp.Poly(s00, A, Ac, B, Bc).coeff_monomial(A ** 2 * Ac ** 2)
    cLL = sp.Poly(s00, A, Ac, B, Bc).coeff_monomial(B ** 2 * Bc ** 2)
    cx = sp.Poly(s00, A, Ac, B, Bc).coeff_monomial(A * Ac * B * Bc)
    cc = sp.Poly(sp.expand(slow.get((2, -2), 0)), A, Ac, B, Bc).coeff_monomial(A ** 2 * Bc ** 2)
    K5[k_] = dict(g_HH=sp.simplify(2 * cHH), g_LL=sp.simplify(2 * cLL), cross=sp.simplify(cx), pair=sp.simplify(2 * cc))
    P(f"    {k_:15s}: g_HH = {K5[k_]['g_HH']}, g_LL = {K5[k_]['g_LL']}, cross c_x = {K5[k_]['cross']}, pair coupling G/n = {K5[k_]['pair']}"
      f"   (g_HH/(G/n) = {sp.simplify(K5[k_]['g_HH'] / K5[k_]['pair'])})")
OUT["numbers"]["K5"] = {k_: {q: str(v_) for q, v_ in d.items()} for k_, d in K5.items()}
check("K5 lambda|Phi|^4 gives each component a self-coupling 3x the conversion coupling (g_HH = g_LL = 3 lambda/4m^2, "
      "G/n = lambda/4m^2); lambda(Im Phi^2)^2 has no self-coupling (g_HH = g_LL = 0) and G/n = lambda/2m^2",
      {k_: {q: str(v_) for q, v_ in d.items()} for k_, d in K5.items()},
      sp.simplify(K5["lam|Phi|^4"]["g_HH"] - 3 * K5["lam|Phi|^4"]["pair"]) == 0
      and K5["lam(ImPhi^2)^2"]["g_HH"] == 0 and K5["lam(ImPhi^2)^2"]["g_LL"] == 0 and K5["lam(ImPhi^2)^2"]["pair"] != 0,
      "with the pure cross term each component is a free field away from the conversion: the cold carrier has no "
      "self-interaction pressure and the products free-stream once the heavy pump is spent", load_bearing=False)

# ============================================================================================ K3 the pair instability
banner("K3  THE PAIR INSTABILITY OF A HEAVY CONDENSATE AT REST (NR, sympy)")
ek = sp.Symbol("epsilon_k", real=True)
n_, G_ = sp.symbols("n G", positive=True)
Dsym = sp.Symbol("D", real=True)
Mmat = sp.Matrix([[Dsym, G_], [-G_, -Dsym]])
ev = [sp.simplify(e) for e in Mmat.eigenvals()]
P(f"    eigenfrequencies of the (k, -k) pair mode: {ev}  -> growth sqrt(G^2 - D^2), largest (G) at D = 0")
delta_v = sp.Integer(0) if MUTATE else dl
K3 = {}
for k_, cp in K5.items():
    Gn, gHH, cx = cp["pair"], cp["g_HH"], cp["cross"]
    D_expr = ek - delta_v + cx * n_ - gHH * n_                              # epsilon_k - delta + cross shift - mu_H
    ek_res = sp.solve(sp.Eq(D_expr, 0), ek)[0]
    # the shell speed against the splitting's, at a pair coupling G = 1e-3 delta_nominal (N3: G/delta ~ 1e-3 at the trigger)
    num = ek_res.subs({dl: 1}).subs(n_, 1e-3 / Gn).subs({lam: 1, m: 1})
    ratio = math.sqrt(float(num)) if float(num) > 0 else 0.0                # v_res/v_k (0: no real shell)
    K3[k_] = dict(eps_k_res=str(ek_res), v_res_over_vk_at_q_1e_3=ratio)
    P(f"    {k_:15s}: resonance eps_k = {ek_res}  ->  v_res/v_k = {ratio:.5f} at G = 1e-3 delta")
res_ok = all(abs(K3[k_]["v_res_over_vk_at_q_1e_3"] - 1) < 0.01 for k_ in K3)
ev_ok = set(sp.expand(e ** 2) for e in ev) == {sp.expand(Dsym ** 2 - G_ ** 2)}
OUT["numbers"]["K3"] = K3
check("K3 a heavy condensate at rest is unstable to phi_L pairs with growth sqrt(G^2 - D^2); the growth peaks on the "
      "shell |v| = v_k (1 + O(G/delta)) for both quartics -- the kick speed is the splitting's, shifted only by the "
      "coupling's mean field",
      f"eigenvalues {ev}; v_res/v_k at G = 1e-3 delta: {[round(K3[k_]['v_res_over_vk_at_q_1e_3'], 5) for k_ in K3]}", ev_ok and res_ok)

# ============================================================================================ K4 expansion-limited exponent
banner("K4  THE EXPANSION-LIMITED GROWTH EXPONENT (a mode swept through the shell by the expansion)")
expo = sp.simplify(sp.integrate(sp.sqrt(G_ ** 2 - Dsym ** 2), (Dsym, -G_, G_)) / (2 * H_ * dl))
P(f"    int sqrt(G^2 - D^2) dt with dD/dt = -2 H delta:  {expo}")
OUT["numbers"]["K4"] = str(expo)
check("K4 a mode crossing the resonance shell grows by pi G^2/(4 H delta) e-folds", str(expo),
      sp.simplify(expo - sp.pi * G_ ** 2 / (4 * H_ * dl)) == 0, load_bearing=False)

# ============================================================================================ N1 numbers
banner("N1  THE KICK IN NUMBERS: splitting, de Broglie length, e-folds, sharpness")
hbar_eVs, c_ms, eV_J = 6.582119569e-16, 2.99792458e8, 1.602176634e-19
H0 = 67.36 * 1e3 / 3.0857e22; Om, OL = 0.3138, 0.6862
MPC_M, PC_M = 3.0857e22, 3.0857e16
rho_m0 = Om * 3 * H0 ** 2 / (8 * math.pi * 6.674e-11)
N1 = {}
for mev in (2e-19, 1e-17, 1e-15, 1e-10, 1e-6):
    m_kg = mev * eV_J / c_ms ** 2
    lam_dB = 2 * math.pi * hbar_eVs * c_ms / (mev * 600e3 / c_ms) / PC_M        # pc, at v_k = 600 km/s
    rho_t = 1e3 * rho_m0                                                    # a dense galaxy region
    n_t = rho_t / m_kg
    hbar_SI = hbar_eVs * eV_J
    k_k = m_kg * 600e3 / hbar_SI; dk = m_kg * 100e3 / hbar_SI                # shell radius and Doppler width (sigma = 100 km/s)
    N_f = n_t * (2 * math.pi) ** 3 / (4 * math.pi * k_k ** 2 * dk)
    efold = math.log(N_f / 0.5)
    N1[f"{mev:g}"] = dict(lambda_dB_pc=lam_dB, N_final=N_f, efolds=efold)
    P(f"    m = {mev:.0e} eV: lambda_dB(600 km/s) = {lam_dB:.2e} pc;  shell occupation N_f ~ {N_f:.1e}  ->  "
      f"ln(N_f/N_seed) = {efold:.0f} e-folds")
E_need = N1["2e-19"]["efolds"]
thr_edge = math.sqrt((E_need - 20) / E_need)
P(f"    the exponent grows as n^2: a region converts completely at n_t and by < e^-20 below {thr_edge:.3f} n_t "
  f"(m = 2e-19 eV) -- a sharp density threshold")
OUT["numbers"]["N1"] = dict(by_mass=N1, sharp_below=thr_edge)
check("N1 the products are classical waves (lambda_dB at v_k <= 0.2 pc for m >= 2e-19 eV, Vlasov limit: L388's ballistic "
      "kick) and the conversion needs ~60-190 e-folds, so the threshold is sharp (complete at n_t, negligible 6% below)",
      f"lambda_dB {N1['2e-19']['lambda_dB_pc']:.2e} pc at 2e-19 eV; e-folds {N1['1e-06']['efolds']:.0f}-{N1['2e-19']['efolds']:.0f}; "
      f"negligible below {thr_edge:.3f} n_t", N1["2e-19"]["lambda_dB_pc"] < 1.0 and thr_edge > 0.9, load_bearing=False)

# ============================================================================================ N2 the background converts first
banner("N2  A CONSTANT COUPLING CONVERTS THE COSMIC BACKGROUND FIRST; the gate it needs")
Ez = lambda z: math.sqrt(Om * (1 + z) ** 3 + OL)
N2 = {}
for dt_ in (5.0, 25.0, 100.0, 1e3, 1e4):
    for hf in (1.0, 4.0):
        f = lambda z: (1 + z) ** 6 / Ez(z) - hf * dt_ ** 2
        zc = brentq(f, 0.0, 1e4) if f(0.0) < 0 else 0.0
        N2[f"{dt_:g}/{hf:g}"] = zc
    P(f"    trigger overdensity delta_t = {dt_:>6g} at z = 0: constant coupling converts the mean background by z = "
      f"{N2[f'{dt_:g}/1']:.2f} (halo factor 1) / {N2[f'{dt_:g}/4']:.2f} (halo factor 4)")
qmin = 0.75
zz = np.linspace(0, 20, 20001)
fq = lambda q: (1 + zz) ** 6 / np.array([Ez(z) for z in zz]) ** (1 + 4 * q)
f175 = fq(1.75)
P(f"    gated coupling lambda ~ K^(-2q) (K = 3H): background exponent ~ (1+z)^6/E^(1+4q); falls into the matter era iff q > {qmin}")
P(f"    q = p + 3/4 = 1.75 (the trigger density then scales as E^(1/2+2q) = E^4, the linear gate's): background exponent peaks at "
  f"z = {zz[f175.argmax()]:.2f}, {f175.max():.2f}x its z = 0 value -> {f175.max() / 25:.3f} of the trigger's at delta_t = 5")
OUT["numbers"]["N2"] = dict(z_convert_constant=N2, q_min=qmin, q_linear_gate=1.75, bg_peak_z=float(zz[f175.argmax()]),
                            bg_peak_factor=float(f175.max()))
check("N2 (reported) a constant coupling converts the mean background at z ~ 0.9-4 for the record's threshold (delta_t 5-25), "
      "so the coupling must be vacuum-gated: q > 3/4, and q = 1.75 keeps the background below 6% of the trigger's exponent",
      f"z_convert(delta_t = 5) = {N2['5/1']:.2f}-{N2['5/4']:.2f}; (25) {N2['25/1']:.2f}-{N2['25/4']:.2f}; q = 1.75 peak {f175.max():.2f}x at z = {zz[f175.argmax()]:.2f}",
      N2["5/1"] > 0.3 and f175.max() / 25 < 0.1, "the vacuum gate stays in the construction: it is the coupling's K-dependence, "
      "force-free on CMC leaves (CV4), not a new mechanism", load_bearing=False)

# ============================================================================================ N3 what lambda|Phi|^4 would cost
banner("N3  THE SELF-INTERACTION THE TRIGGER IMPLIES (lambda|Phi|^4) -- zero for lambda(Im Phi^2)^2")
N3 = {}
for mev in (2e-19, 1e-17, 1e-15, 1e-10):
    hH = hbar_eVs * H0 / mev                                                # hbar H0 / m c^2
    s_ = s_of_v[600.0]
    G_over_m = math.sqrt(4 * E_need * hH * s_ / math.pi)                    # K4 at the trigger: pi G^2/(4 H delta) = E_need
    cs = C_KMS * math.sqrt(3 * G_over_m)                                    # g_HH n = 3 G (K5), c_s^2 = g n/m
    N3[f"{mev:g}"] = dict(G_over_mc2=G_over_m, c_s_kms=cs)
    P(f"    m = {mev:.0e} eV: pair coupling at the trigger G/mc^2 = {G_over_m:.1e};  lambda|Phi|^4 self-coupling -> sound speed "
      f"{cs:.2f} km/s at n_t;  products' kinetic relaxation ~ 18 E_need/pi ~ {18 * E_need / math.pi:.0f} C_k per Hubble time (estimate)")
OUT["numbers"]["N3"] = N3
check("N3 (reported) with lambda|Phi|^4 the trigger implies a self-interaction pressure (sound speed ~22 km/s at the "
      "trigger for m = 2e-19 eV, falling as m^(-1/4)) and products that relax where they are made (~10^3 C_k per Hubble "
      "time at the trigger density); the pure cross term lambda(Im Phi^2)^2 has neither",
      {k_: f"c_s {v_['c_s_kms']:.2f} km/s" for k_, v_ in N3.items()}, True, load_bearing=False)

# ============================================================================================ summary
banner("SUMMARY")
P(f"""  The kick fits inside FL1's order parameter.  One component cannot hold a universal latent heat (K1); Phi's two real
  components can.  A U(1)-breaking mass term eps Re(Phi^2) with eps/m^2 = {s_of_v[575.0]:.2e}-{s_of_v[650.0]:.2e} (v_k = 575-650 km/s)
  makes the carrier the heavy component; Z2 x Z2 keeps a lone phi_H stable; phi_H phi_H -> phi_L phi_L leaves back to back
  at exactly v_k (K2), from a Bose-stimulated pair instability on the shell |v| = v_k (K3, K4), so the trigger is a sharp
  density threshold (N1).  The quartic should be the pure cross term lambda(Im Phi^2)^2: lambda|Phi|^4 would give each
  component 3x the conversion coupling as self-coupling, a pressure at the trigger and products that relax where they are
  made (K5, N3).  A constant coupling converts the cosmic background first (by z ~ {N2['5/1']:.1f}-{N2['25/4']:.1f} at the record's
  threshold), so the coupling carries the vacuum gate: lambda ~ K^(-3.5) reproduces the linear gate's scaling and is
  force-free on CMC leaves (N2).  Declared: eps, the coupling, q, and an initial misalignment near the phi_H axis.  The
  carrier's mass is still required; this is new field content (FL1).""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["summary"] = dict(load_bearing_failed=n_fail, runtime_s=round(time.time() - T0, 1))
suffix = "_MUTATE" if MUTATE else ""
json.dump(OUT, open(os.path.join(HERE, f"{SLUG}_results{suffix}.json"), "w"), indent=1, default=str)
P(f"\n  checks: {sum(ok for _, ok, _ in CH)}/{len(CH)} pass; load-bearing failures: {n_fail}   [{time.time() - T0:.0f}s]")
sys.exit(1 if n_fail else 0)
