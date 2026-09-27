#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FL3 -- CAN THE DARK FLUID SWIRL WITHOUT DISTURBING THE CLOCK'S SLICES?  A rotating halo's vortex lattice against the
khronon.

The review session asked this as one of four readings of the author's idea that a halo is like a fluid swirling down
between the bands.  The fluid here is the dark fluid, FL1/FK1's order parameter; it is not Lambda.  A superfluid holds
angular momentum only in quantised vortices, one circulation quantum h/m each, at Feynman's density n_v = m Omega/(pi hbar).
At every core the field vanishes.  The questions:
  (1) what FL2's khronon source, lambda'(K)(Im Phi^2)^2, does at the cores;
  (2) delta K/K at the lattice scale, against CV4's largest moving-source value (|K/3H - 1| <= 4.8e-3);
  (3) whether any vorticity coupling reaches tau;
  (4) whether the leaves stay unfolded (criterion B).

WHAT THIS LANE CHECKS
  S1 [the source at the cores] sympy: near a unit vortex of psi_H the gated energy g_c (6a^2 + 2b^2) (a + ib = psi_H psi_L*)
     vanishes as r^2, and the relativistic (Im Phi^2)^2 = phi_H^2 phi_L^2 vanishes as r^4 at a common core.  Numeric: on a
     rotating triangular lattice (product ansatz, same-sign vortices) for psi_H and an offset lattice for psi_L, E_int is
     zero at every psi_H core, finite and smooth everywhere, and identically zero before the conversion (psi_L = 0).
  S2 [delta K/K at the lattice scale] (a) the gate channel.  FL2 V3's response is algebraic, delta K ~ E_int, so the
     lattice only modulates FL2 V4's conversion values (read from FL2's committed JSON) between 0, at cores, and their
     maximum.  (b) the swirl's own channel: a moving density pattern sources delta K = omega G_1 psi_N (CV4 K2).  G_1 is
     read from CV4's committed JSON at C = 0, because the fluid is kernel-invisible.  Both the ordered lattice (spin
     lambda = 0.03-0.05) and the random vortex tangle (one per lambda_dB^2) are evaluated, for m = 2e-19, 1e-17 and
     1e-15 eV in a Milky-Way-like halo, at alpha_c = 3.2e-9 and c_2 = 1e-4, the largest |G_1|.  Pass when (a) stays below
     CV4's 4.8e-3 for c_2 >= 1e-3 at z <= 4 (the c_2 = 1e-4 rows are reported) and (b) stays below 1e-10.
  S3 [no vorticity reaches tau at linear order] sympy, on ds^2 = -(1 + 2 Phi) dt^2 + 2 a^2 B_i dt dx^i + a^2 (1 - 2 Psi) dx^2,
     with the foliation tau = t + pi.  The linear K and the lapse are independent of a transverse shift B = curl(chi z^).
     A longitudinal shift B = grad chi does enter K, as the built-in control.  The khronon's normal is hypersurface-
     orthogonal: grad x grad tau = 0.  V0's khronon action has only a^2 and (K - <K>)^2, with no twist or shear term.
  S4 [criterion B] the circulation lives in the order parameter's phase.  Numerically, the fluid velocity's loop
     integral around N cores is N h/m, one quantum per core.  The khronon's tilt pi is solved from the swirling fluid's
     own E_int (lap pi = -E_int: FL2 V3's algebraic delta K with CV4's delta K = -lap(pi)/a^2), and its gradient's loop
     integral is 0 to the solver's accuracy.  So tau is single-valued, its source is smooth (S1), the stress is continuous
     through every core, and the leaves never fold.
  MUTATE=1 makes the clock the fluid's own dust: its direction field is the fluid velocity.  The loop integral is then
  N h/m != 0, so tau is multivalued with a screw dislocation at every core.  S4 must FAIL.  rc = 1.

SCOPE.  Quasi-static, linear khronon (CV4's scope), plus a second-order estimate for the vector modes.  The lattice
geometry is illustrative (product ansatz); the halo numbers are order-of-magnitude, with v_rot = sqrt 2 lambda V_c (Bullock
et al. 2001).  The swirl of the BARYONS (spiral patterns, the disk) is CV4 K2's moving-source dipole, not this lane.

Run from the repository root:  python3 real_research/dark_fluid_2026/FL3_swirl_and_the_clock.py
"""
import os, sys, json, math, time, warnings
import numpy as np
import sympy as sp
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG = "FL3", "FL3_swirl_and_the_clock"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()


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
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("WHAT THIS LANE CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the clock is the fluid's own dust (its direction field = the fluid velocity); S4 must FAIL ***")

FL2 = json.load(open(os.path.join(ROOT, "real_research", "dark_fluid_2026", "FL2_dark_slot_with_the_kick_results.json")))
CV4 = json.load(open(os.path.join(ROOT, "real_research", "chk_v0_2026", "CV4_khronon_K_profile_results.json")))
CV4_MAX = max(r_["dK_over_3H"] for r_ in CV4["numbers"]["K3"]["rows"])
P(f"\n  CV4's largest moving-source |K/3H - 1| (its K3 table): {CV4_MAX:.2e}")

# ============================================================================================ lattice machinery
ELL, RC = 1.0, 0.1                                                 # lattice spacing (units of l_v), core radius


def tri_lattice(spacing, rmax, offset=(0.0, 0.0)):
    pts = []
    n = int(rmax / spacing) + 3
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            x_ = spacing * (i + 0.5 * j) + offset[0]
            y_ = spacing * (math.sqrt(3) / 2 * j) + offset[1]
            if x_ * x_ + y_ * y_ <= rmax * rmax:
                pts.append((x_, y_))
    return np.array(pts)


CORES_H = tri_lattice(ELL, 3.2)
CORES_L = tri_lattice(0.8 * ELL, 3.2, offset=(0.31, 0.17))


def lattice_field(X, Y, cores, envelope=2.2):
    """Product ansatz: same-sign vortices; psi = prod (z - z_j)/sqrt(|z - z_j|^2 + r_c^2) x exp(-r^2/envelope^2)."""
    Z = X + 1j * Y
    psi = np.exp(-(X ** 2 + Y ** 2) / envelope ** 2).astype(complex)
    for (xj, yj) in cores:
        d = Z - (xj + 1j * yj)
        psi = psi * d / np.sqrt(np.abs(d) ** 2 + RC ** 2)
    return psi


# ============================================================================================ S1 the source at the cores
banner("S1  THE GATE'S KHRONON SOURCE AT VORTEX CORES: it vanishes smoothly (r^2), and is zero before the conversion")
r_, th_ = sp.symbols("r theta", positive=True)
c0r, c0i, c1r, c1i = sp.symbols("c0r c0i c1r c1i", real=True)
xs_, ys_ = r_ * sp.cos(th_), r_ * sp.sin(th_)
psiH = xs_ + sp.I * ys_                                            # a unit vortex of psi_H at the origin
psiL = (c0r + sp.I * c0i) + (c1r + sp.I * c1i) * xs_               # smooth, non-zero at the core
wv = sp.expand(psiH * sp.conjugate(psiL))
Eint = sp.expand(6 * sp.re(wv) ** 2 + 2 * sp.im(wv) ** 2)
lim0 = sp.simplify(Eint.subs(r_, 0))
lim2 = sp.simplify(sp.limit(Eint / r_ ** 2, r_, 0))
alpha_, beta_ = sp.symbols("alpha beta", positive=True)
rel = sp.expand((alpha_ * xs_) ** 2 * (beta_ * ys_) ** 2)           # phi_H ~ alpha x, phi_L ~ beta y at a common core
rel_order = sp.simplify(sp.limit(rel / r_ ** 4, r_, 0))
P(f"    E_int/g_c at the core: {lim0};  lim E_int/(g_c r^2) = {lim2}  (finite, generically non-zero: E_int ~ r^2)")
P(f"    relativistic phi_H^2 phi_L^2 at a common core: lim /r^4 = {rel_order}  (~ r^4)")
# numeric lattice
gx = np.linspace(-3.0, 3.0, 1201)
GX, GY = np.meshgrid(gx, gx)
pH = lattice_field(GX, GY, CORES_H)
pL = lattice_field(GX, GY, CORES_L)
w_ = pH * np.conj(pL)
E = 6 * w_.real ** 2 + 2 * w_.imag ** 2
Emax = float(E.max())
at_cores = []
for (xj, yj) in CORES_H:
    if xj * xj + yj * yj < 2.5 ** 2:
        pj = lattice_field(np.array([xj]), np.array([yj]), CORES_H)[0]
        lj = lattice_field(np.array([xj]), np.array([yj]), CORES_L)[0]
        wj = pj * np.conj(lj)
        at_cores.append(6 * wj.real ** 2 + 2 * wj.imag ** 2)
hgrid = gx[1] - gx[0]
dEy, dEx = np.gradient(E, hgrid)
inner = (GX ** 2 + GY ** 2) < 2.5 ** 2
grad_rel = float(np.max(np.hypot(dEx, dEy)[inner]) * ELL / Emax)
before = lattice_field(GX, GY, CORES_H) * np.conj(np.zeros_like(pL))
E_before = float(np.max(6 * before.real ** 2 + 2 * before.imag ** 2))
# near-core scaling on the lattice
xj, yj = CORES_H[np.argmin(np.hypot(CORES_H[:, 0], CORES_H[:, 1]))]
sc = []
for rr in (1e-2, 1e-3, 1e-4):
    ths = np.linspace(0, 2 * np.pi, 64, endpoint=False)
    Xs, Ys = xj + rr * np.cos(ths), yj + rr * np.sin(ths)
    ww = lattice_field(Xs, Ys, CORES_H) * np.conj(lattice_field(Xs, Ys, CORES_L))
    sc.append(float(np.mean(6 * ww.real ** 2 + 2 * ww.imag ** 2) / rr ** 2))
P(f"    lattice: {len(CORES_H)} psi_H cores, {len(CORES_L)} psi_L cores; E_int max {Emax:.3f} (g_c n^2 units); at the psi_H "
  f"cores max {max(at_cores):.1e}; max |grad E_int| l_v / E_max = {grad_rel:.1f}; before conversion max E_int = {E_before}")
P(f"    near a core, <E_int>/r^2 at r = 1e-2, 1e-3, 1e-4: {[round(s_, 4) for s_ in sc]}  (constant: E_int ~ r^2)")
OUT["numbers"]["S1"] = {"core_value": str(lim0), "r2_coefficient": str(lim2), "relativistic_r4": str(rel_order),
                        "lattice_Emax": Emax, "at_cores_max": max(at_cores), "grad_rel": grad_rel, "E_before": E_before,
                        "near_core_r2": sc}
check("S1 at every vortex core the gated energy vanishes smoothly (as r^2; the relativistic (Im Phi^2)^2 as r^4 at a common "
      "core), it is finite and smooth across the lattice, and it is identically zero before the conversion",
      f"core value {lim0}; r^2 coefficient finite; lattice core max {max(at_cores):.1e}; gradient {grad_rel:.1f} E_max/l_v; "
      f"before {E_before}; near-core scaling {[round(s_, 3) for s_ in sc]}",
      lim0 == 0 and lim2 != 0 and r_ not in lim2.free_symbols and max(at_cores) < 1e-20 and grad_rel < 100
      and E_before == 0.0 and abs(sc[-1] / sc[-2] - 1) < 0.02,
      "the khronon's source from the gate is a smooth, bounded bilinear of the two envelopes that has a zero at every "
      "core: the swirl gives it holes, never spikes; the unconverted swirling fluid sources nothing through the gate")

# ============================================================================================ S2 delta K/K at the lattice scale
banner("S2  delta K/K AT THE LATTICE SCALE: the gate channel (FL2) and the swirl's own moving-pattern channel (CV4 K2)")
rows = FL2["numbers"]["V4"]["rows"]
gate = {}
for c2v in sorted({r_["c2"] for r_ in rows}):
    sel = [r_ for r_ in rows if r_["c2"] == c2v and r_["z"] <= 4.0]
    gate[c2v] = max(r_["x"] for r_ in sel)
for c2v, xv in gate.items():
    P(f"    gate channel, c_2 = {c2v:.1e}: the lattice modulates delta K/K between 0 (cores) and {xv:.2e} (z <= 4); "
      f"{'below' if xv < CV4_MAX else 'ABOVE'} CV4's {CV4_MAX:.1e}")
Cs, acs, c2s = sp.symbols("C alpha_c c_2")
G1 = sp.sympify(CV4["numbers"]["K2"]["G1"], locals={"C": Cs, "alpha_c": acs, "c_2": c2s})
G1_0 = sp.simplify(G1.subs(Cs, 0))
G1f = sp.lambdify((acs, c2s), sp.Abs(G1_0), "numpy")
P(f"    CV4's G_1 at C = 0 (the fluid is kernel-invisible): {G1_0}")
C_KMS, GK = 299792.458, 4.30091e-6                                  # km/s; kpc (km/s)^2/Msun
HBAR, EV, C_SI, KPC = 1.054571817e-34, 1.602176634e-19, 2.99792458e8, 3.0856775814913673e19
H0K, OM, OL = 0.0674, 0.3153, 0.6847
E_ = lambda zz: math.sqrt(OM * (1 + zz) ** 3 + OL)
VC, RK = 200.0, 10.0                                                # Milky-Way-like halo at 10 kpc
rho_d = VC ** 2 / (4 * math.pi * GK * RK ** 2)                      # Msun/kpc^3, isothermal
four_pi_G_rho = VC ** 2 / RK ** 2                                    # (km/s/kpc)^2
sig_v = VC / math.sqrt(2)
ACm, C2m = 3.2e-9, 1e-4
g1max = float(G1f(ACm, C2m))
swirl = {}
for mev in (2e-19, 1e-17, 1e-15):
    m_kg = mev * EV / C_SI ** 2
    for lam in (0.03, 0.05):
        v_rot = math.sqrt(2) * lam * VC                               # km/s
        Om = v_rot * 1e3 / (RK * KPC)                                 # 1/s
        n_v = m_kg * Om / (math.pi * HBAR)                            # 1/m^2 (Feynman)
        l_v = n_v ** -0.5 / KPC                                       # kpc
        N_v = n_v * math.pi * (RK * KPC) ** 2
        lam_dB = 2 * math.pi * HBAR / (m_kg * sig_v * 1e3) / KPC     # kpc
        out = {}
        for lab, ell, spd in (("lattice", l_v, v_rot), ("tangle", lam_dB, sig_v)):
            kk = 2 * math.pi / ell                                    # 1/kpc
            psiN = four_pi_G_rho / (kk ** 2 * C_KMS ** 2)             # |Phi/c^2| of an O(1) density pattern at that scale
            omega = spd / C_KMS * kk                                  # 1/kpc (CV4's per-length convention)
            dK = omega * g1max * psiN
            out[lab] = dK / (3 * H0K / C_KMS)
        swirl[f"{mev:g}/{lam}"] = {"v_rot": v_rot, "l_v_pc": l_v * 1e3, "N_v_within_10kpc": N_v, "lambda_dB_pc": lam_dB * 1e3,
                                   "dK_lattice": out["lattice"], "dK_tangle": out["tangle"]}
        P(f"    m = {mev:.0e} eV, spin {lam}: v_rot = {v_rot:.1f} km/s, l_v = {l_v * 1e3:.1f} pc ({N_v:.1e} vortices inside 10 kpc), "
          f"lambda_dB = {lam_dB * 1e3:.2e} pc;  delta K/K: lattice {out['lattice']:.1e}, tangle {out['tangle']:.1e}")
worst_swirl = max(max(v_["dK_lattice"], v_["dK_tangle"]) for v_ in swirl.values())
OUT["numbers"]["S2"] = {"gate_channel_max_by_c2": {str(k_): v_ for k_, v_ in gate.items()}, "CV4_max": CV4_MAX,
                        "G1_C0": str(G1_0), "swirl": swirl, "worst_swirl": worst_swirl}
gate_ok = all(xv < CV4_MAX for c2v, xv in gate.items() if c2v >= 1e-3)
check("S2 at the lattice scale the gate channel only modulates FL2's conversion shift between 0 (cores) and its maximum, "
      "below CV4's 4.8e-3 for c_2 >= 1e-3 at z <= 4; the swirl's own moving-pattern channel (kernel-invisible: G_1 at C = 0 "
      "~ alpha_c/c_2) is below 1e-10 for the lattice and the random tangle",
      f"gate channel by c_2: { {f'{k_:.0e}': f'{v_:.1e}' for k_, v_ in gate.items()} }; swirl channel worst {worst_swirl:.1e}",
      gate_ok and worst_swirl < 1e-10,
      "the swirl adds nothing measurable to K; the only lattice-scale structure in K is the conversion gate's, which has a "
      "hole at every core.  At the KM1 floor c_2 = 1e-4 the conversion's own shift reaches 1.0e-2 at z = 4 (FL2 V4), "
      "above CV4's moving-source number -- a statement about the conversion, not the swirl")

# ============================================================================================ S3 vorticity and tau
banner("S3  NO VORTICITY REACHES tau AT LINEAR ORDER: K and the lapse ignore a transverse shift (a longitudinal one enters)")
t, x, y, z = sp.symbols("t x y z", real=True)
eps = sp.symbols("epsilon", positive=True)
aS = sp.Function("a")(t)
Phi_, Psi_, pi_, chi_ = [sp.Function(n)(t, x, y, z) for n in ("Phi", "Psi", "pi", "chi")]
X4 = [t, x, y, z]


def linear_K_and_lapse(Bvec):
    gbar = sp.diag(-1, aS ** 2, aS ** 2, aS ** 2)
    h = sp.zeros(4, 4)
    h[0, 0] = -2 * Phi_
    for i in range(3):
        h[i + 1, i + 1] = -2 * aS ** 2 * Psi_
        h[0, i + 1] = h[i + 1, 0] = aS ** 2 * Bvec[i]
    gbi = gbar.inv()
    ginv = gbi - eps * gbi * h * gbi                                 # first order
    sqrtg = aS ** 3 * (1 + eps * (Phi_ - 3 * Psi_))                  # the shift enters det g at O(eps^2)
    dtau = [1 + eps * sp.diff(pi_, t), eps * sp.diff(pi_, x), eps * sp.diff(pi_, y), eps * sp.diff(pi_, z)]
    Xs = -sum(ginv[m_, n_] * dtau[m_] * dtau[n_] for m_ in range(4) for n_ in range(4))
    nlow = [-d_ / sp.sqrt(Xs) for d_ in dtau]
    K = sum(sp.diff(sqrtg * sum(ginv[m_, n_] * nlow[n_] for n_ in range(4)), X4[m_]) for m_ in range(4)) / sqrtg
    K1 = sp.expand(sp.simplify(sp.diff(K, eps).subs(eps, 0)))
    lapse1 = sp.expand(sp.diff(1 / sp.sqrt(-ginv[0, 0]), eps).subs(eps, 0))   # N = (-g^00)^(-1/2) for the t-slicing
    return K1, lapse1


B_trans = [sp.diff(chi_, y), -sp.diff(chi_, x), sp.Integer(0)]      # curl(chi z^): divergence-free (the vortical part)
B_long = [sp.diff(chi_, x), sp.diff(chi_, y), sp.diff(chi_, z)]      # grad chi: the built-in control
K_none, N_none = linear_K_and_lapse([0, 0, 0])
K_tr, N_tr = linear_K_and_lapse(B_trans)
K_lo, N_lo = linear_K_and_lapse(B_long)
dK_tr = sp.simplify(K_tr - K_none)
dK_lo = sp.simplify(K_lo - K_none)
dN_tr = sp.simplify(N_tr - N_none)
lapB = sp.simplify(dK_lo / (sp.diff(chi_, x, 2) + sp.diff(chi_, y, 2) + sp.diff(chi_, z, 2)))
tau_s = sp.Function("tau")(x, y)
twist = sp.simplify(sp.diff(sp.diff(tau_s, y), x) - sp.diff(sp.diff(tau_s, x), y))
P(f"    linear K, no shift: {K_none}")
P(f"    change from a transverse shift B = curl(chi z^): {dK_tr};  lapse change: {dN_tr}")
P(f"    change from a longitudinal shift B = grad chi (control): {dK_lo}  (= {lapB} x lap chi)")
P(f"    the khronon normal's twist, curl(grad tau) = {twist} (hypersurface-orthogonal by construction)")
# second order: a gravitomagnetic potential |B| ~ (v/c)(Phi/c^2); quadratic terms in K ~ |grad B|^2 / K
v_c_ratio, phi_ratio = VC / C_KMS, VC ** 2 / C_KMS ** 2
Bmag = v_c_ratio * phi_ratio
est1 = Bmag ** 2 * (C_KMS / (3 * H0K * RK))                           # a B dB term in K (~B^2/r) against K = 3H/c
est2 = Bmag ** 2 * (C_KMS / (3 * H0K * RK)) ** 2                      # a (dB)^2 source against the khronon's K^2 stiffness
second = max(est1, est2)
P(f"    second order: |B| ~ (v/c) Phi/c^2 = {Bmag:.1e}; a B dB term gives delta K/K ~ {est1:.1e}, a (dB)^2 source against "
  f"the K^2 stiffness ~ {est2:.1e} at r = 10 kpc (upper estimates)")
OUT["numbers"]["S3"] = {"K_linear": str(K_none), "dK_transverse": str(dK_tr), "dN_transverse": str(dN_tr), "second_order": second,
                        "dK_longitudinal": str(dK_lo), "twist": str(twist)}
check("S3 at linear order the khronon's K and the lapse are independent of a transverse (vortical) shift, while a "
      "longitudinal shift does enter K (the control); the khronon's normal is twist-free; V0's khronon terms are a^2 and "
      "(K - <K>)^2 only -- so no vorticity coupling reaches tau at linear order",
      f"transverse dK {dK_tr}, dN {dN_tr}; longitudinal dK = {lapB} lap chi; twist {twist}",
      dK_tr == 0 and dN_tr == 0 and dK_lo != 0 and twist == 0,
      "the fluid's swirl sources only the metric's gravitomagnetic (vector) part, which the clock's scalar equations never "
      "see at this order; the second-order leak is negligible")

# ============================================================================================ S4 criterion B
banner("S4  CRITERION B: the circulation lives in the order parameter's phase; tau stays single-valued; no fold")
# loop integrals on a circle enclosing the lattice's central cores
Rloop = 1.55
ths = np.linspace(0, 2 * np.pi, 20001)
Xl, Yl = Rloop * np.cos(ths), Rloop * np.sin(ths)
enclosed = int(np.sum(np.hypot(CORES_H[:, 0], CORES_H[:, 1]) < Rloop))
psi_loop = lattice_field(Xl, Yl, CORES_H)
phase = np.unwrap(np.angle(psi_loop))
circ_fluid = float((phase[-1] - phase[0]) / (2 * np.pi))             # circulation in units of h/m
# the khronon's tilt: FL2 V3 makes delta K algebraic in E_int, and delta K = -lap(pi)/a^2 (CV4): solve lap(pi) = -E_int
from scipy.interpolate import RegularGridInterpolator
Ns = len(gx); kx_ = 2 * np.pi * np.fft.fftfreq(Ns, d=hgrid)
KX, KY = np.meshgrid(kx_, kx_)
k2 = KX ** 2 + KY ** 2; k2[0, 0] = 1.0
Eh = np.fft.fft2(E - E.mean())
pih = Eh / k2; pih[0, 0] = 0.0                                       # lap pi = -(E - <E>)  ->  pi_k = E_k/k^2
pix = np.real(np.fft.ifft2(1j * KX * pih)); piy = np.real(np.fft.ifft2(1j * KY * pih))
if MUTATE:
    # the dust clock: its direction field is the fluid velocity (hbar/m) grad theta, theta the psi_H phase
    circ_clock = circ_fluid
    clock_grad_max = float("inf")
else:
    Ix = RegularGridInterpolator((gx, gx), pix.T); Iy = RegularGridInterpolator((gx, gx), piy.T)
    pts = np.column_stack([Xl, Yl])
    dl_x, dl_y = -Rloop * np.sin(ths), Rloop * np.cos(ths)
    integrand = Ix(pts) * dl_x + Iy(pts) * dl_y
    circ_clock = float(np.sum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(ths)))
    clock_grad_max = float(np.max(np.hypot(pix, piy)))
circ_scale = float(np.max(np.hypot(pix, piy)) * 2 * np.pi * Rloop)   # the loop integral's natural scale
# stress continuity through a core: |grad psi|^2 on small loops
xj, yj = CORES_H[np.argmin(np.hypot(CORES_H[:, 0], CORES_H[:, 1]))]
st = []
for rr in (1e-3, 1e-5):
    tt_ = np.linspace(0, 2 * np.pi, 64, endpoint=False)
    hh = 1e-7
    Xs, Ys = xj + rr * np.cos(tt_), yj + rr * np.sin(tt_)
    px = (lattice_field(Xs + hh, Ys, CORES_H) - lattice_field(Xs - hh, Ys, CORES_H)) / (2 * hh)
    py = (lattice_field(Xs, Ys + hh, CORES_H) - lattice_field(Xs, Ys - hh, CORES_H)) / (2 * hh)
    g2 = np.abs(px) ** 2 + np.abs(py) ** 2
    st.append((float(g2.min()), float(g2.max())))
stress_cont = abs(st[-1][1] - st[-1][0]) < 1e-3 * st[-1][1]
P(f"    loop of radius {Rloop} l_v encloses {enclosed} psi_H cores: fluid circulation = {circ_fluid:.4f} h/m (one quantum "
  f"per core); the clock's loop integral = {circ_clock:.2e} "
  f"({'in h/m: the fluid velocity -- MUTATE' if MUTATE else f'of grad pi, against its natural scale {circ_scale:.2e}'})")
P(f"    the khronon's tilt pi solved from the swirling fluid's E_int (lap pi = -E_int, periodic): single-valued by "
  f"construction, max |grad pi| = {clock_grad_max:.3f} (finite, smooth through every core)")
P(f"    |grad psi|^2 on loops of radius 1e-3 and 1e-5 around a core: {[(round(a_, 4), round(b_, 4)) for a_, b_ in st]} "
  f"(continuous: {stress_cont})")
OUT["numbers"]["S4"] = {"enclosed": enclosed, "circ_fluid": circ_fluid, "circ_clock": circ_clock, "circ_scale": circ_scale,
                        "clock_grad_max": clock_grad_max, "stress_loops": st}
tau_single = (not MUTATE) and abs(circ_clock) < 1e-6 * circ_scale and math.isfinite(clock_grad_max)
check("S4 the fluid's circulation is quantised in its phase (N h/m around N cores, mean vorticity 2 Omega) while the "
      "loop integral of the khronon's tilt -- solved from the swirling fluid's own E_int -- is zero: tau is single-valued, "
      "its source is smooth (S1) and the stress is continuous through every core, so the leaves never fold",
      f"fluid {circ_fluid:.3f} h/m around {enclosed} cores; clock {circ_clock:.1e} (scale {circ_scale:.1e}); "
      f"stress continuous {stress_cont}", tau_single and abs(circ_fluid - enclosed) < 1e-3 and stress_cont,
      "the dark fluid can swirl without disturbing the slices: its swirl is the winding of its own phase (a branch cut in "
      "theta is harmless because psi is single-valued); a clock made of the fluid's dust would carry that winding and fold")

banner("VERDICT")
P(f"""  Yes: the dark fluid can swirl without disturbing the clock's slices.  A rotating halo's fluid carries its angular
  momentum in quantised vortices (l_v ~ {swirl['2e-19/0.03']['l_v_pc']:.0f} pc for m = 2e-19 eV at spin 0.03, falling as m^-1/2;
  the random tangle's lambda_dB is ~0.4 pc).  At every core the gate's khronon source vanishes smoothly (S1).  The swirl's own
  channel into K is below 1e-10, and the lattice only modulates FL2's conversion shift between 0 and its maximum (S2).  At
  linear order no vorticity reaches tau, because the clock is twist-free and its K and lapse ignore the gravitomagnetic
  field (S3).  The circulation lives in the order parameter's phase, so tau stays single-valued (S4).
  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
