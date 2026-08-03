#!/usr/bin/env python3
r"""mi_algebraic_disc_escape_2026.py -- ESCAPE D: SOLVE THE THEORY THE FRAMEWORK ACTUALLY IS.

THE PROBLEM. `mi_aqual_route_a_refit_2026.py` (L7a) concluded: "ROUTE A DOES NOT ESCAPE LISANTI'S DILEMMA.
ZERO cells clear the 2-sigma box on all five constraints, for either kernel, on either footing, anywhere on
the grid," with a best worst-constraint of 2.07 sigma. But every number there was computed with an AQUAL /
Bekenstein-Milgrom field solver, which is MODIFIED GRAVITY. The framework's commitment is MODIFIED INERTIA,
and outside spherical symmetry MI and AQUAL are DIFFERENT THEORIES. This lane computes the same five Milky Way
observables under the ALGEBRAIC MI law -- g_obs = nu(|g_bar|/a0) g_bar applied to the NEWTONIAN baryonic field
as a pointwise vector map -- and asks whether MI clears the box where AQUAL cannot.

  D1  VALIDATE THE MI PIPELINE. The Newtonian solve against the CLOSED-FORM field of a spherical control; and
      -- the load-bearing one -- the NUMERICAL FLOOR of the whole MI-vs-AQUAL comparison, measured where the
      two theories are provably IDENTICAL (spherical symmetry, where AQUAL integrates to mu(x) x = y exactly).
      Plus Milgrom 2022's monotonicity requirement on x mu(x), verified rather than assumed.
  D2  WHAT MI COSTS, measured not asserted. The algebraic law has NO POTENTIAL in a disc: its acceleration
      field carries a nonzero curl. Quantified EXACTLY on an analytic Miyamoto-Nagai disc (Newtonian control
      closes to ~1e-16), as the specific energy a star gains per closed circuit.
  D3  THE ANCHOR'S OWN GRID, MI and AQUAL side by side -- reproducing L7a's 2.07 from the same procedure.
  D4  *** THE MINIMAX DONE PROPERLY. *** L7a searched a GRID; the question "does ANY configuration clear the
      box" needs an OPTIMISER. Golden section in f_M at each f_R, same 2-parameter family, same extractor.
  D5  SYSTEMATICS: mesh (n = 110 / 150 / 190) and extractor (interpolated vs the anchor's snapped read), both
      priced in sigma on the binding constraint and compared to the MI-vs-AQUAL difference itself.
  D6  IS CLEARING THE BOX A FIT? chi2, dof, p-value, AIC -- because a 2-sigma-per-constraint box is a WEAKER
      test than a joint chi2, and saying so is the honest part.
  D7  THE DEEP QUESTION: is an MI clearance evidence FOR MI over MG, or a less-constrained calculation?

TWO free parameters throughout -- f_M (common stellar-mass scale) and f_R (common scale-length scale) -- the
same family and the same count as L7a, so nothing here is bought with extra freedom. a0 is an INPUT on BOTH
footings, never fitted. NO error bar is widened anywhere in this file; the five constraints are byte-identical
to the anchor's.

Exit 0 = ran and every check held.
"""
from __future__ import annotations

import math
import pathlib
import sys
import time

import numpy as np
from scipy.integrate import quad
from scipy.stats import chi2 as chi2dist

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mi_route_a_kernel import (A0_ALT, A0_CANON, mu as mu_exp, mu_alpha2, mu_simple, nu, nu_alpha2)

ok: list[tuple[bool, str]] = []
T0 = time.time()


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 110)
    print(f"  {t}")
    print("=" * 110)


# ------------------------------------------------------------ the anchor's definitions, verbatim, no re-write
SRCPATH = pathlib.Path(__file__).with_name("mi_aqual_mond_refit_2026.py")
_src = SRCPATH.read_text()
_cut = _src.index('banner("F1')
_G: dict = {"__name__": "anchor_defs"}
exec(compile(_src[:_cut], str(SRCPATH), "exec"), _G)

G, KPC, PC, MSUN, MSUN_PC2 = _G["G"], _G["KPC"], _G["PC"], _G["MSUN"], _G["MSUN_PC2"]
R0 = _G["R0"]
VC, VC_E, KZ, KZ_E = _G["VC"], _G["VC_E"], _G["KZ"], _G["KZ_E"]
MSTAR_P, MSTAR_E = _G["MSTAR_P"], _G["MSTAR_E"]
RDTHIN_P, RDTHIN_E = _G["RDTHIN_P"], _G["RDTHIN_E"]
SIGSTAR_P, SIGSTAR_E = _G["SIGSTAR_P"], _G["SIGSTAR_E"]
solve, densities, mass_of, sigma_of = _G["solve"], _G["densities"], _G["mass_of"], _G["sigma_of"]
chi2f = _G["chi2"]

BOX = 2.0                   # L7's acceptance box, unchanged
KEYS = ("vc", "sd", "mstar", "rd", "sig")
MESHES = ((110, 1.085), (150, 1.060), (190, 1.047))     # (n, growth); the first is the committed one


def nu_simple(y):
    """inverse of mu = x/(1+x): the algebraic boost of the literature's simple kernel."""
    y = np.asarray(y, float)
    return (1.0 + np.sqrt(1.0 + 4.0 / y)) / 2.0


# ------------------------------------------------------------------------------------- the shared extractors
def _zline(arr, zval, Rc, zc):
    """arr(R, z) interpolated in z to zval, returned as a 1-D profile over Rc."""
    return np.array([np.interp(zval, zc, arr[j, :]) for j in range(len(Rc))])


def _read(P, Rc, zc):
    """Return the field magnitudes the two observables need, INTERPOLATED in R for both (the 2026-08-02
    audit's fix), plus the anchor's SNAPPED vertical read so both conventions come off the SAME solve free."""
    gR = np.gradient(P, Rc, axis=0)
    gz = np.gradient(P, zc, axis=1)
    z11 = 1.1 * KPC
    j0 = int(np.argmin(np.abs(Rc - R0)))                      # the anchor's snapped column
    return dict(gR_pl=abs(np.interp(R0, Rc, gR[:, 0])),
                gz_pl=abs(np.interp(R0, Rc, gz[:, 0])),
                gR_11=abs(np.interp(R0, Rc, _zline(gR, z11, Rc, zc))),
                gz_11=abs(np.interp(R0, Rc, _zline(gz, z11, Rc, zc))),
                gR_11s=abs(np.interp(z11, zc, gR[j0, :])),
                gz_11s=abs(np.interp(z11, zc, gz[j0, :])))


BAR: dict = {}


def baryons(fM, fR):
    k = (round(fM, 6), round(fR, 6))
    if k not in BAR:
        comp, rdt = densities(fM, fR)
        BAR[k] = dict(mstar=(mass_of(comp["thin"]) + mass_of(comp["thick"])
                             + mass_of(comp["bulge"])) / MSUN,
                      sigstar=(sigma_of(comp["thin"], R0, 1.1 * KPC)
                               + sigma_of(comp["thick"], R0, 1.1 * KPC)) / MSUN_PC2,
                      rdt=rdt,
                      rho=lambda R, z, c=comp: sum(f(R, z) for f in c.values()))
    return BAR[k]


NEWT: dict = {}
AQ: dict = {}
NS = {"newt": 0, "aqual": 0}


def newt(fM, fR, mesh=0):
    """the NEWTONIAN baryonic field -- ONE linear solve, shared by every footing and every kernel."""
    n, gw = MESHES[mesh]
    k = (round(fM, 6), round(fR, 6), n)
    if k not in NEWT:
        Rc, zc, P = solve(baryons(fM, fR)["rho"], A0_CANON, mu_exp, n=n, growth=gw, newtonian=True)
        NEWT[k] = _read(P, Rc, zc)
        NS["newt"] += 1
    return NEWT[k]


def aqual(fM, fR, a0, mu_k, tag, mesh=0):
    """the AQUAL field solve -- one nonlinear Picard solve per (cell, footing, kernel)."""
    n, gw = MESHES[mesh]
    k = (round(fM, 6), round(fR, 6), round(a0, 18), tag, n)
    if k not in AQ:
        Rc, zc, P = solve(baryons(fM, fR)["rho"], a0, mu_k, n=n, growth=gw)
        AQ[k] = _read(P, Rc, zc)
        NS["aqual"] += 1
    return AQ[k]


def observe(fM, fR, a0, theory, tag, mesh=0, snap=False):
    """The five observables. theory = ('MI', nu_k) or ('AQUAL', mu_k). ONE extractor convention for both
    observables; `snap` reproduces the anchor's nearest-column vertical read off the same solve."""
    b = baryons(fM, fR)
    kind, kern = theory
    if kind == "MI":
        f = newt(fM, fR, mesh)
        gR_pl, gz_pl = f["gR_pl"], f["gz_pl"]
        gR_11, gz_11 = (f["gR_11s"], f["gz_11s"]) if snap else (f["gR_11"], f["gz_11"])
        # the algebraic modified-inertia law as a POINTWISE VECTOR map: a = nu(|g_N|/a0) g_N. The boost is set
        # by the FULL Newtonian magnitude at that point, so nu_vert = nu_rad there identically -- which is the
        # structural difference from AQUAL that this lane is testing.
        aR = float(kern(math.hypot(gR_pl, gz_pl) / a0)) * gR_pl
        az = float(kern(math.hypot(gR_11, gz_11) / a0)) * gz_11
    else:
        f = aqual(fM, fR, a0, kern, tag, mesh)
        aR = f["gR_pl"]
        az = f["gz_11s"] if snap else f["gz_11"]
    return dict(vc=math.sqrt(aR * R0), sd=az / (2 * math.pi * G) / MSUN_PC2,
                mstar=b["mstar"], sigstar=b["sigstar"], rdt=b["rdt"])


def sigmas(o):
    return dict(vc=(o["vc"] - VC) / VC_E, sd=(o["sd"] - KZ) / KZ_E,
                mstar=(o["mstar"] - MSTAR_P) / MSTAR_E, rd=(o["rdt"] - RDTHIN_P) / RDTHIN_E,
                sig=(o["sigstar"] - SIGSTAR_P) / SIGSTAR_E)


def worst(o):
    s = sigmas(o)
    return max(abs(s[k]) for k in KEYS)


def binding(o):
    s = sigmas(o)
    return max(KEYS, key=lambda k: abs(s[k]))


banner("D1  VALIDATING THE MI PIPELINE -- and measuring the NUMERICAL FLOOR of the whole comparison")

RS = 1.0 * KPC
RHO0_S = 5.0e10 * MSUN / (8 * math.pi * RS**3)
rho_sph = lambda R, z: RHO0_S * np.exp(-np.sqrt(R * R + z * z) / RS)


def M_enc(r):
    """closed-form enclosed mass of rho = rho0 exp(-r/Rs)."""
    t = r / RS
    return 4 * math.pi * RHO0_S * RS**3 * (2.0 - math.exp(-t) * (2.0 + 2.0 * t + t * t))


n0, g0 = MESHES[0]
RcN, zcN, PN_s = solve(rho_sph, A0_CANON, mu_exp, n=n0, growth=g0, newtonian=True)
RcA, zcA, PA_s = solve(rho_sph, A0_CANON, mu_exp, n=n0, growth=g0)
gN_s, gA_s = np.gradient(PN_s[:, 0], RcN), np.gradient(PA_s[:, 0], RcA)
RT = (5, 10, 20, 40, 80)
print(f"  spherical control: exponential sphere, M_tot = {M_enc(1e3 * KPC) / MSUN:.3e} Msun, scale 1 kpc")
print(f"  {'R [kpc]':>8}{'g_N(solve)':>13}{'g_N(exact)':>13}{'solve/exact':>13}   "
      f"{'y':>8}{'MI=nu(g_N)g_N':>16}{'AQUAL solve':>14}{'MI/AQUAL':>10}")
print("  " + "-" * 98)
nb, rr = [], []
for Rk in RT:
    gn = abs(np.interp(Rk * KPC, RcN, gN_s))
    ga = abs(np.interp(Rk * KPC, RcA, gA_s))
    ge = G * M_enc(Rk * KPC) / (Rk * KPC) ** 2
    mi = gn * float(nu(gn / A0_CANON))
    nb.append(gn / ge - 1.0)
    rr.append(mi / ga)
    print(f"  {Rk:>8}{gn:>13.5e}{ge:>13.5e}{gn / ge:>13.5f}   {gn / A0_CANON:>8.4f}"
          f"{mi:>16.5e}{ga:>14.5e}{mi / ga:>10.5f}")
nbias = max(abs(x) for x in nb)
check(nbias < 0.03,
      f"D1a the Newtonian solve is validated against a CLOSED-FORM field, not against another solve: for an "
      f"exponential sphere with M(<r) analytic the mesh returns g_N to a worst {100 * nbias:.2f}% over 5-80 kpc. "
      f"This is the pipeline the MI law is applied to, so its accuracy is the accuracy of every MI number below")

FLOOR_G = max(abs(r - 1.0) for r in rr)
FLOOR_SPREAD = max(rr) - min(rr)
FLOOR_VC_SIG = VC * (math.sqrt(1.0 + FLOOR_G) - 1.0) / VC_E
FLOOR_SD_SIG = KZ * FLOOR_G / KZ_E
print(f"""
  In SPHERICAL symmetry the AQUAL field equation integrates to mu(x) x = y exactly, so MI and AQUAL are the
  SAME THEORY there and the last column above is EXACTLY 1.000000 in the continuum. Whatever it is not is the
  numerical floor of this lane's central comparison:
      MI/AQUAL = {np.mean(rr):.5f} mean, spread {FLOOR_SPREAD:.5f} across 5-80 kpc
      => floor = {100 * FLOOR_G:.2f}% in acceleration = {FLOOR_VC_SIG:.2f} sigma on v_c(R0) and """
      f"""{FLOOR_SD_SIG:.2f} sigma on Sigma_dyn.
  Any MI-vs-AQUAL difference below that is numerics, not theory.""")
check(FLOOR_G < 0.05 and FLOOR_SPREAD < 0.01,
      f"D1b the floor is a bounded, radius-INDEPENDENT offset -- {100 * FLOOR_G:.2f}% at worst with only "
      f"{100 * FLOOR_SPREAD:.2f}% of spread over 5-80 kpc -- i.e. a systematic of the two pipelines and not "
      f"noise. It is measured where MI and AQUAL are provably IDENTICAL theories, so it is the right yardstick "
      f"for the disc difference: {FLOOR_VC_SIG:.2f} sigma on v_c, {FLOOR_SD_SIG:.2f} sigma on Sigma_dyn")

# --- D1c Milgrom 2022's condition on an MI theory built at the level of the EOM
xs = np.logspace(-10.0, 8.0, 200001)
mono_x = bool(np.all(np.diff(xs * mu_exp(xs)) > 0))
ys = np.logspace(-10.0, 8.0, 200001)
mono_y = bool(np.all(np.diff(ys * np.asarray(nu(ys))) > 0))
# the closed form, verified numerically rather than asserted:
#   d/ds [ s^2/(1 - e^-s) ] = s e^-s (2 e^s - 2 - s)/(1 - e^-s)^2 ,  with y = s^2
#   h(s) = 2 e^s - 2 - s has h(0) = 0 and h'(s) = 2 e^s - 1 > 0 on s > 0, so h > 0: the map is strictly
#   increasing and y -> y nu(y) is a bijection, i.e. the algebraic law inverts uniquely.
ss = np.logspace(-6.0, 2.0, 400)
Fs = lambda t: t * t / -np.expm1(-t)
hh = 1e-7 * ss
ident = ss * np.exp(-ss) * (2 * np.exp(ss) - 2 - ss) / (-np.expm1(-ss)) ** 2
fd = (Fs(ss + hh) - Fs(ss - hh)) / (2 * hh)
id_err = float(np.max(np.abs(ident / fd - 1.0)))
h_min = float(np.min(2 * np.exp(ss) - 2 - ss))
print(f"""
  Milgrom 2022 (PRD 106, 064060) builds MI at the level of the EQUATION OF MOTION and notes that such theories
  "are not necessarily governed by an action"; what they DO require is that x mu(x) be monotonic so the law
  inverts. Verified for Route A over eighteen decades:
      x mu(x) strictly increasing: {mono_x}       y nu(y) strictly increasing: {mono_y}
      closed-form derivative identity holds to {id_err:.2e};  min of h(s) = 2e^s - 2 - s is {h_min:.2e}""")
check(mono_x and mono_y and id_err < 1e-6 and h_min > 0.0,
      f"D1c ROUTE A SATISFIES MILGROM 2022's REQUIREMENT, verified not assumed: x mu(x) and y nu(y) are both "
      f"strictly increasing over eighteen decades, and the closed form d/ds[s^2/(1-e^-s)] = "
      f"s e^-s (2e^s - 2 - s)/(1-e^-s)^2 reproduces a finite-difference derivative to {id_err:.1e} with "
      f"h(s) = 2e^s - 2 - s > 0. So the exponential kernel IS an admissible MI kernel in Milgrom's sense -- "
      f"which is precisely the sense that does not come with an action")

f_t = newt(1.78, 0.80)
y_pl = math.hypot(f_t["gR_pl"], f_t["gz_pl"]) / A0_CANON
y_11 = math.hypot(f_t["gR_11"], f_t["gz_11"]) / A0_CANON
print(f"\n  the Newtonian y = |g_bar|/a0 that MI reads at (f_M, f_R) = (1.78, 0.80): {y_pl:.4f} in the plane, "
      f"{y_11:.4f} at |z| = 1.1 kpc")
print(f"      -> nu = {float(nu(y_pl)):.4f} and {float(nu(y_11)):.4f};  u = sqrt(y) = {math.sqrt(y_pl):.3f} "
      f"and {math.sqrt(y_11):.3f}, decades below the u ~ 37 float64 saturation")
check(0.2 < y_pl < 20.0 and 0.2 < y_11 < 20.0 and y_11 < y_pl,
      f"D1d both Milky Way observables sit in the kernel's transition region ON THE NEWTONIAN FIELD "
      f"(y = {y_pl:.2f} radial, {y_11:.2f} vertical), with the vertical point at the LOWER y -- so MI's two "
      f"boosts differ between the two evaluation points even though they are identical at any single point, and "
      f"nothing here hides in a saturated limb of the kernel")


banner("D2  WHAT THE MI ESCAPE COSTS -- measured, in energy units, not asserted")

MN_M, MN_A, MN_B = 5.5e10 * MSUN, 2.5 * KPC, 0.3 * KPC


def mn_g(R, z):
    ze = math.sqrt(z * z + MN_B * MN_B)
    zeta = MN_A + ze
    s = math.sqrt(R * R + zeta * zeta)
    return G * MN_M * R / s**3, G * MN_M * zeta * z / (s**3 * ze)


def mn_a(R, z, boost):
    gR, gz = mn_g(R, z)
    b = float(nu(math.hypot(gR, gz) / A0_CANON)) if boost else 1.0
    return b * gR, b * gz


def circulation(R1, R2, z1, z2, boost):
    q = lambda f, a, b: quad(f, a, b, epsabs=0.0, epsrel=1e-12, limit=400)[0]
    return (q(lambda R: mn_a(R, z1, boost)[0], R1, R2) + q(lambda z: mn_a(R2, z, boost)[1], z1, z2)
            - q(lambda R: mn_a(R, z2, boost)[0], R1, R2) - q(lambda z: mn_a(R1, z, boost)[1], z1, z2))


print(f"""  The corpus's 2026-08-01 result stands: for this form class the MI law is NOT VARIATIONAL in a disc
  (three no-goes -- not variational; the u-contraction (v/c)^2-suppressed for generic K; the prefactor IS the
  worldline's Frenet torsion). Here is that cost as a NUMBER rather than a citation. A conservative field has
  zero circulation. The algebraic law a = nu(|g_N|/a0) g_N has curl nu'(|g_N|) (grad|g_N| x g_N), which
  vanishes only when the level surfaces of |g_N| coincide with those of Phi_N -- true in spherical symmetry,
  FALSE in a disc. Measured on an ANALYTIC Miyamoto-Nagai disc (M = 5.5e10 Msun, a = 2.5 kpc, b = 0.3 kpc) so
  the Newtonian control is exact to machine precision and none of this is mesh error:\n""")
print(f"  {'loop (R kpc) x (z kpc)':<26}{'work on one leg':>18}{'Newtonian circ.':>18}{'rel':>9}"
      f"{'MI circulation':>18}{'/leg':>10}{'/(vc^2/2)':>12}")
print("  " + "-" * 111)
CIRC = []
for (R1, R2, z1, z2) in ((7, 9, 0.0, 0.5), (6, 10, 0.0, 1.1), (4, 12, 0.0, 2.0), (2, 20, 0.0, 4.0)):
    cN = circulation(R1 * KPC, R2 * KPC, z1 * KPC, z2 * KPC, False)
    cM = circulation(R1 * KPC, R2 * KPC, z1 * KPC, z2 * KPC, True)
    leg = abs(quad(lambda R: mn_a(R, z1 * KPC, True)[0], R1 * KPC, R2 * KPC,
                   epsabs=0.0, epsrel=1e-12, limit=400)[0])
    CIRC.append((abs(cN) / leg, abs(cM) / leg, cM / (0.5 * VC**2)))
    print(f"  {f'({R1}-{R2}) x ({z1}-{z2})':<26}{leg:>18.4e}{cN:>18.3e}{abs(cN) / leg:>9.1e}"
          f"{cM:>18.4e}{cM / leg:>+10.5f}{cM / (0.5 * VC**2):>+12.2e}")
ctrl = max(c[0] for c in CIRC)
mical = max(c[1] for c in CIRC)
bigE = max(abs(c[2]) for c in CIRC)
check(ctrl < 1e-12 and mical > 1e-3,
      f"D2a *** THE MI FIELD IS NOT CONSERVATIVE IN A DISC, and this is the price of the escape. *** The "
      f"Newtonian control closes to {ctrl:.1e} of one leg's work (machine precision -- it IS a gradient), while "
      f"the algebraic MI field leaves a residual circulation of up to {100 * mical:.2f}% of a leg: a star gains "
      f"up to {100 * bigE:.1f}% of the Galaxy's specific circular kinetic energy per closed circuit in the "
      f"(R, z) plane. No potential, so no energy integral -- and the vertical Jeans analysis that DEFINES the "
      f"73.9 target assumes both. AQUAL has this identically zero by construction")

comp_t = baryons(1.78, 0.80)
Rc_n, zc_n, P_n = solve(comp_t["rho"], A0_CANON, mu_exp, n=n0, growth=g0, newtonian=True)
Rc_a, zc_a, P_a = solve(comp_t["rho"], A0_CANON, mu_exp, n=n0, growth=g0)
gRn, gzn = np.gradient(P_n, Rc_n, axis=0), np.gradient(P_n, zc_n, axis=1)
gRa, gza = np.gradient(P_a, Rc_a, axis=0), np.gradient(P_a, zc_a, axis=1)
at = lambda arr, zz, Rg, zg: abs(np.interp(R0, Rg, _zline(arr, zz, Rg, zg)))
print(f"\n  {'|z| [kpc]':>10}{'AQUAL boost on g_R':>21}{'AQUAL boost on g_z':>21}{'vert/rad':>11}"
      f"{'MI nu (both)':>15}{'MI vert/rad':>13}")
print("  " + "-" * 92)
ANI = []
for zz in (zc_n[0] / KPC, 0.25, 0.5, 1.1, 2.0):
    z_ = zz * KPC
    bR = at(gRa, z_, Rc_a, zc_a) / at(gRn, z_, Rc_n, zc_n)
    bz = at(gza, z_, Rc_a, zc_a) / at(gzn, z_, Rc_n, zc_n)
    ANI.append(bz / bR)
    nuv = float(nu(math.hypot(at(gRn, z_, Rc_n, zc_n), at(gzn, z_, Rc_n, zc_n)) / A0_CANON))
    print(f"  {zz:>10.3f}{bR:>21.5f}{bz:>21.5f}{bz / bR:>11.5f}{nuv:>15.5f}{1.0:>13.5f}")
mix_aq = ((at(gza, 1.1 * KPC, Rc_a, zc_a) / at(gzn, 1.1 * KPC, Rc_n, zc_n))
          / (at(gRa, zc_a[0], Rc_a, zc_a) / at(gRn, zc_n[0], Rc_n, zc_n)))
mix_mi = float(nu(y_11)) / float(nu(y_pl))
print(f"""
  POINTWISE, AQUAL's boost is anisotropic and MI's is exactly isotropic -- but the anisotropy is LARGEST in the
  midplane ({ANI[0]:.4f}), where g_z ~ 0 and it cannot matter, and SMALLEST at |z| = 1.1 kpc ({ANI[3]:.4f}),
  which is where the constraint is actually read. Across the two evaluation points the FIT uses -- v_c at
  (R0, 0) and Sigma_dyn at (R0, 1.1 kpc) -- the ratio is AQUAL {mix_aq:.4f} against MI {mix_mi:.4f}, a
  {100 * (mix_aq / mix_mi - 1):.2f}% difference. That is the entire size of the escape this lane is testing,
  and D1b's numerical floor is {100 * FLOOR_G:.2f}%.""")
check(ANI[0] > ANI[3] > ANI[4] and abs(mix_aq - 1.0) > abs(mix_mi - 1.0),
      f"D2b the structural difference is REAL but small exactly where it is needed: AQUAL's vertical/radial "
      f"boost anisotropy falls monotonically from {ANI[0]:.4f} in the midplane to {ANI[3]:.4f} at |z| = 1.1 kpc "
      f"and {ANI[4]:.4f} at 2 kpc, while MI's is exactly 1 at every point by construction. Over the two points "
      f"the five-constraint fit reads, AQUAL gives {mix_aq:.4f} against MI's {mix_mi:.4f}, so MI predicts a "
      f"~{100 * (mix_aq / mix_mi - 1):.1f}% SMALLER vertical force at the same rotation curve -- the same size "
      f"as the {100 * FLOOR_G:.2f}% numerical floor")


banner("D3  THE ANCHOR'S OWN GRID -- MI and AQUAL side by side, reproducing L7a's 2.07 sigma")

FM = [1.0, 1.3, 1.6, 1.9, 2.2, 2.5, 2.8]
FR = [0.7, 0.8, 0.9, 1.0, 1.1]
CONF = [
    ("Route A, MI algebraic, canon", "exc", ("MI", nu), A0_CANON),
    ("Route A, MI algebraic, ALT", "exa", ("MI", nu), A0_ALT),
    ("Route A, AQUAL field, canon", "exc", ("AQUAL", mu_exp), A0_CANON),
    ("Route A, AQUAL field, ALT", "exa", ("AQUAL", mu_exp), A0_ALT),
]
print(f"""  L7's own procedure, repeated: the coarse grid f_M in {FM}, f_R in {FR}, then a 3x3 half-step
  refinement (df_M = 0.15, df_R = 0.05) around the chi2 best, then min over ALL solved cells of the worst of
  the five constraints.\n""")
print(f"  {'configuration':<32}{'chi2 best cell':>16}{'chi2':>8}{'best-worst cell':>17}"
      f"{'best worst':>12}{'binding':>9}{'in box':>8}")
print("  " + "-" * 104)
GRIDRES = {}
for label, tag, theory, a0 in CONF:
    cells, bb = [], None
    for fM in FM:
        for fR in FR:
            o = observe(fM, fR, a0, theory, tag)
            cells.append((fM, fR, o))
            if bb is None or chi2f(o)[0] < bb[0]:
                bb = (chi2f(o)[0], fM, fR, o)
    for fM in (bb[1] - 0.15, bb[1], bb[1] + 0.15):
        for fR in (bb[2] - 0.05, bb[2], bb[2] + 0.05):
            if fM <= 0 or fR <= 0:
                continue
            o = observe(fM, fR, a0, theory, tag)
            cells.append((fM, fR, o))
            if chi2f(o)[0] < bb[0]:
                bb = (chi2f(o)[0], fM, fR, o)
    wc = min(cells, key=lambda t: worst(t[2]))
    nbox = sum(1 for t in cells if worst(t[2]) <= BOX)
    GRIDRES[label] = (worst(wc[2]), wc, nbox, bb)
    print(f"  {label:<32}{f'({bb[1]:.2f}, {bb[2]:.2f})':>16}{bb[0]:>8.1f}"
          f"{f'({wc[0]:.2f}, {wc[1]:.2f})':>17}{worst(wc[2]):>12.3f}{binding(wc[2]):>9}{nbox:>8}")
gaq_c, gaq_a = GRIDRES["Route A, AQUAL field, canon"], GRIDRES["Route A, AQUAL field, ALT"]
gmi_c = GRIDRES["Route A, MI algebraic, canon"]
check(abs(gaq_c[0] - 2.07) < 0.03 and abs(gaq_a[0] - 2.21) < 0.03 and gaq_c[2] == 0 and gaq_a[2] == 0,
      f"D3a L7a REPRODUCES from the same procedure and the same solver code: AQUAL Route A on the anchor's grid "
      f"gives a best worst-constraint of {gaq_c[0]:.3f} sigma canonical (published 2.07) and {gaq_a[0]:.3f} ALT "
      f"(published 2.21), with {gaq_c[2]} and {gaq_a[2]} cells in the {BOX:.0f}-sigma box. Everything below is "
      f"therefore a difference of METHOD or of THEORY, not of implementation")
check(gmi_c[0] < gaq_c[0],
      f"D3b on that SAME grid the algebraic MI law gets closer to the box than the AQUAL field solve -- "
      f"{gmi_c[0]:.3f} sigma against {gaq_c[0]:.3f} -- but by only {gaq_c[0] - gmi_c[0]:.3f} sigma, and both "
      f"land on the same (f_M, f_R) cell, which is already a hint that the GRID and not the theory is setting "
      f"these numbers")


banner("D4  *** THE MINIMAX DONE PROPERLY -- an optimiser, not a grid ***")

print(f"""  L7a asked "does ANY solved cell clear the box" and answered over the cells it happened to solve. The
  question it MEANT to ask -- does any (f_M, f_R) in this 2-parameter family clear all five constraints at once
  -- is an OPTIMISATION, and the answer can differ. At fixed f_R the sigmas are monotone in f_M (v_c, Sigma_dyn,
  M_* and Sigma_* all rise with it, R_d is independent of it), so max|sigma| is unimodal in f_M and a golden
  section finds its minimum. f_R is scanned. Still exactly TWO free parameters -- nothing is bought.

  MI is ~40x cheaper than AQUAL (one linear solve, no Picard loop), so MI is optimised on a WIDE bracket with
  many evaluations and its optimum then SEEDS a narrow bracket for AQUAL. Every reported AQUAL optimum is
  checked to be interior to its bracket, so the seeding cannot bias the comparison.\n""")

GR = (math.sqrt(5.0) - 1.0) / 2.0


def golden(fR, a0, theory, tag, lo, hi, nev, mesh, snap):
    W = lambda fm: worst(observe(fm, fR, a0, theory, tag, mesh=mesh, snap=snap))
    a, b = lo, hi
    c, d = b - GR * (b - a), a + GR * (b - a)
    fc, fd = W(c), W(d)
    for _ in range(max(0, nev - 2)):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - GR * (b - a)
            fc = W(c)
        else:
            a, c, fc = c, d, fd
            d = a + GR * (b - a)
            fd = W(d)
    fm = c if fc < fd else d
    return (min(fc, fd), fm, observe(fm, fR, a0, theory, tag, mesh=mesh, snap=snap), b - a)


MI_WIDE, MI_NEV, AQ_HALF, AQ_NEV = (0.45, 6.5), 26, 0.35, 11


def minimax(fR, a0, theory, nu_seed, tag, mesh=0, snap=False):
    """returns (W, fM, o, bracket, seed, interior)"""
    if theory[0] == "MI":
        W, fm, o, brk = golden(fR, a0, theory, tag, MI_WIDE[0], MI_WIDE[1], MI_NEV, mesh, snap)
        return (W, fm, o, brk, float("nan"), MI_WIDE[0] + 0.05 < fm < MI_WIDE[1] - 0.05)
    sd_ = golden(fR, a0, ("MI", nu_seed), tag, MI_WIDE[0], MI_WIDE[1], MI_NEV, mesh, snap)[1]
    W, fm, o, brk = golden(fR, a0, theory, tag, max(0.05, sd_ - AQ_HALF), sd_ + AQ_HALF, AQ_NEV, mesh, snap)
    return (W, fm, o, brk, sd_, abs(fm - sd_) < AQ_HALF - 0.05)


# The f_R ranges are chosen per kernel so that each kernel's optimum is INTERIOR to its own scan -- located
# first with the ~40x cheaper MI evaluator, then handed to AQUAL. Truncating a scan at the side that flatters
# a kernel is exactly the error this corpus has made before, so each list brackets its own minimum on BOTH
# sides and D4e asserts interiority.
FRSCAN = (0.72, 0.76, 0.78, 0.79, 0.80, 0.84)          # Route A: MI minimum near 0.78-0.80
A2FR = (0.62, 0.66, 0.68, 0.70, 0.74)                  # alpha=2: MI minimum near 0.66-0.68
SMFR = (0.76, 0.78, 0.80, 0.84)                        # simple mu
RUNS = [
    ("Route A  MI algebraic  canon", "exc", ("MI", nu), nu, A0_CANON, FRSCAN),
    ("Route A  MI algebraic  ALT  ", "exa", ("MI", nu), nu, A0_ALT, FRSCAN),
    ("Route A  AQUAL field   canon", "exc", ("AQUAL", mu_exp), nu, A0_CANON, FRSCAN),
    ("Route A  AQUAL field   ALT  ", "exa", ("AQUAL", mu_exp), nu, A0_ALT, FRSCAN),
    ("alpha=2  MI algebraic  canon", "a2c", ("MI", nu_alpha2), nu_alpha2, A0_CANON, A2FR),
    ("alpha=2  AQUAL field   canon", "a2c", ("AQUAL", mu_alpha2), nu_alpha2, A0_CANON, A2FR),
    ("alpha=2  AQUAL field   ALT  ", "a2a", ("AQUAL", mu_alpha2), nu_alpha2, A0_ALT, A2FR),
    ("simple   MI algebraic  canon", "smc", ("MI", nu_simple), nu_simple, A0_CANON, SMFR),
    ("simple   AQUAL field   canon", "smc", ("AQUAL", mu_simple), nu_simple, A0_CANON, SMFR),
]
MM, INTERIOR = {}, []
for label, tag, theory, nseed, a0, frs in RUNS:
    best, rows = None, []
    for fR in frs:
        res = minimax(fR, a0, theory, nseed, tag)
        rows.append((fR,) + res)
        INTERIOR.append((label, fR, res[5]))
        if best is None or res[0] < best[1]:
            best = (fR,) + res
    MM[label] = (best, rows)
    fR, W, fm, o, brk, seed, itr = best
    print(f"  {label}:  best over f_R -> (f_M, f_R) = ({fm:.4f}, {fR:.2f})   worst = {W:.4f} sigma "
          f"({binding(o)})   chi2 = {chi2f(o)[0]:.2f}   [{time.time() - T0:.0f}s]")
    for (fRr, Wr, fmr, orr, bk, sdr, itr2) in rows:
        sr = sigmas(orr)
        print(f"        f_R={fRr:.2f}  f_M*={fmr:.4f} (bracket {bk:.5f}{'' if math.isnan(sdr) else f', seed {sdr:.4f}'})"
              f"   vc {sr['vc']:+.3f}  sd {sr['sd']:+.3f}  M {sr['mstar']:+.3f}  Rd {sr['rd']:+.3f}  "
              f"Sg {sr['sig']:+.3f}   WORST {Wr:.4f} ({binding(orr)}){'  <=' if fRr == fR else ''}")

MI_C, MI_A = MM["Route A  MI algebraic  canon"][0], MM["Route A  MI algebraic  ALT  "][0]
AQ_C, AQ_A = MM["Route A  AQUAL field   canon"][0], MM["Route A  AQUAL field   ALT  "][0]
A2_C, A2_A = MM["alpha=2  AQUAL field   canon"][0], MM["alpha=2  AQUAL field   ALT  "][0]
A2MI_C = MM["alpha=2  MI algebraic  canon"][0]
SM_C, SMMI_C = MM["simple   AQUAL field   canon"][0], MM["simple   MI algebraic  canon"][0]
# best tuple layout: (fR, W, fM, o, bracket, seed, interior)
print(f"\n  {'':<32}{'MI algebraic':>16}{'AQUAL field':>16}{'AQUAL - MI':>14}{'clears 2 sigma?':>18}")
print("  " + "-" * 96)
for nm, mi, aq in (("Route A, canonical a0", MI_C, AQ_C), ("Route A, ALT a0", MI_A, AQ_A),
                   ("alpha=2, canonical a0", A2MI_C, A2_C), ("simple mu, canonical a0", SMMI_C, SM_C)):
    both = ("both" if (mi[1] < BOX and aq[1] < BOX) else
            "MI only" if mi[1] < BOX else "AQUAL only" if aq[1] < BOX else "neither")
    print(f"  {nm:<32}{mi[1]:>16.4f}{aq[1]:>16.4f}{aq[1] - mi[1]:>+14.4f}{both:>18}")

check(AQ_C[1] < BOX and gaq_c[0] > BOX,
      f"D4a *** L7a's HEADLINE WAS GRID GRANULARITY, NOT PHYSICS. *** The AQUAL field solve -- the very "
      f"calculation L7a ran -- CLEARS the {BOX:.0f}-sigma box on all five constraints once its two parameters "
      f"are actually optimised: worst constraint {AQ_C[1]:.3f} sigma at (f_M, f_R) = ({AQ_C[2]:.3f}, "
      f"{AQ_C[0]:.2f}) on the canonical footing, against the {gaq_c[0]:.2f} its own grid reported. L7a's "
      f"'ZERO cells clear the box' is a true statement about the cells it solved and a false one about the "
      f"family. This is AGAINST the interest of this lane: the escape it was sent to test is not needed")
check(MI_C[1] < BOX and MI_A[1] < BOX and AQ_A[1] < BOX,
      f"D4b MI clears too, and on both footings, and so does AQUAL on both: MI {MI_C[1]:.3f} / {MI_A[1]:.3f} "
      f"sigma (canon / ALT) against AQUAL's {AQ_C[1]:.3f} / {AQ_A[1]:.3f}. So the question 'does MI clear where "
      f"AQUAL cannot' answers NO -- not because MI fails but because AQUAL succeeds")
dc, da = AQ_C[1] - MI_C[1], AQ_A[1] - MI_A[1]
PRIORS = ("mstar", "rd", "sig")
BIND = {"MI canon": binding(MI_C[3]), "AQUAL canon": binding(AQ_C[3]),
        "MI ALT": binding(MI_A[3]), "AQUAL ALT": binding(AQ_A[3])}
_pri_bound = [k for k, v in BIND.items() if v in PRIORS]
print(f"  binding constraint at each minimax: " + ", ".join(f"{k} -> {v}" for k, v in BIND.items()))
check(abs(dc) < 0.25 and abs(da) < 0.25,
      f"D4c and the separation is a quarter of a sigma at most on either footing: AQUAL minus MI = {dc:+.3f} "
      f"sigma canonical and {da:+.3f} sigma ALT. Part of the reason is visible in the binding constraints "
      f"({', '.join(f'{k}: {v}' for k, v in BIND.items())}): "
      f"{len(_pri_bound)} of the 4 minimax cells are limited by a star-count PRIOR rather than by either data "
      f"constraint, and a prior is a number NEITHER theory computes. Where a prior binds, the MI-vs-AQUAL "
      f"difference cannot help by construction. A difference this size cannot be read as evidence for either "
      f"theory until D5 has priced the systematics")
check(A2_C[1] > AQ_C[1] and A2_A[1] > AQ_A[1],
      f"D4d the kernel comparison survives the granularity fix IN ROUTE A's FAVOUR: the superseded alpha=2 "
      f"kernel minimaxes to {A2_C[1]:.3f} / {A2_A[1]:.3f} sigma (canon / ALT) against Route A's {AQ_C[1]:.3f} / "
      f"{AQ_A[1]:.3f}, so the exponential kernel is still the better Milky Way kernel of the two and the "
      f"solar-system-forced switch still improves this front rather than costing it")
PERT = []
for nm, th in (("Route A  MI algebraic  canon", ("MI", nu)), ("Route A  AQUAL field   canon", ("AQUAL", mu_exp))):
    fR, W, fm = MM[nm][0][0], MM[nm][0][1], MM[nm][0][2]
    lo_ = worst(observe(fm - 0.06, fR, A0_CANON, th, "exc"))
    hi_ = worst(observe(fm + 0.06, fR, A0_CANON, th, "exc"))
    PERT.append((nm, W, lo_, hi_))
    print(f"  minimum audit  {nm}:  W(f_M*) = {W:.4f},  W(f_M* -+ 0.06) = {lo_:.4f} / {hi_:.4f}")
_frint = all(FRSCAN[0] < b[0] < FRSCAN[-1] for b in (MI_C, AQ_C, MI_A, AQ_A))
check(all(w <= lo_ + 1e-9 and w <= hi_ + 1e-9 for _n, w, lo_, hi_ in PERT)
      and all(i for _l, _f, i in INTERIOR) and _frint,
      f"D4e the optima are genuine INTERIOR minima, not bracket or scan ends -- the failure mode that produced "
      f"L7a's 2.07 in the first place: displacing f_M by +-0.06 raises the worst constraint in BOTH directions "
      f"for both theories, all {len(INTERIOR)} golden-section optima are interior to their f_M brackets (so the "
      f"MI seeding of the AQUAL bracket biased nothing), and all four Route A winners have f_R strictly inside "
      f"the scanned {FRSCAN[0]:.2f}-{FRSCAN[-1]:.2f} (winners: MI {MI_C[0]:.2f}/{MI_A[0]:.2f}, AQUAL "
      f"{AQ_C[0]:.2f}/{AQ_A[0]:.2f} for canon/ALT)")


banner("D5  SYSTEMATICS -- mesh and extractor, priced against the MI-vs-AQUAL difference itself")

print(f"""  (a) THE EXTRACTOR. The anchor read Sigma_dyn at the nearest mesh COLUMN in R while reading v_c by
      INTERPOLATION -- a one-sided upward bias the 2026-08-02 audit measured at up to +0.94 sigma. Both
      conventions come off the SAME solves, so the whole minimax can be repeated under the snapped read at
      zero extra solve cost. The interpolated read is the correct one; this is what the choice is worth.\n""")
print(f"  {'configuration':<28}{'interpolated':>14}{'snapped':>10}{'shift':>9}{'clears (interp)':>17}"
      f"{'clears (snap)':>15}")
print("  " + "-" * 94)
SNAP = {}
for label, tag, theory, nseed in (("Route A MI canon", "exc", ("MI", nu), nu),
                                  ("Route A AQUAL canon", "exc", ("AQUAL", mu_exp), nu)):
    bs = None
    for fR in FRSCAN:
        res = minimax(fR, A0_CANON, theory, nseed, tag, snap=True)
        if bs is None or res[0] < bs[0]:
            bs = (res[0], res[1], fR, res[2])
    SNAP[label] = bs
    ref = MI_C[1] if "MI" in label else AQ_C[1]
    print(f"  {label:<28}{ref:>14.3f}{bs[0]:>10.3f}{bs[0] - ref:>+9.3f}"
          f"{('YES' if ref < BOX else 'no'):>17}{('YES' if bs[0] < BOX else 'no'):>15}")
ext_shift = max(SNAP[k][0] - (MI_C[1] if "MI" in k else AQ_C[1]) for k in SNAP)
snap_clears = all(SNAP[k][0] < BOX for k in SNAP)
check(ext_shift > abs(dc),
      f"D5a THE EXTRACTOR CHOICE IS WORTH MORE THAN THE THEORY CHOICE, by a factor of "
      f"{ext_shift / max(abs(dc), 1e-9):.1f}: moving from the interpolated to the anchor's snapped vertical read "
      f"raises the minimaxed worst constraint by up to {ext_shift:+.3f} sigma, against the {dc:+.3f} sigma that "
      f"separates MI from AQUAL on the same footing. Under the snapped read "
      f"{'both still clear the box' if snap_clears else 'the box verdict CHANGES to a MISS'}, so the D4a "
      f"clearance is extractor-sensitive and must always be quoted with the extractor attached")

print(f"\n  (b) THE MESH. The f_R = {AQ_C[0]:.2f} minimax repeated at three resolutions. Outer radii:")
for (n_, g_) in MESHES:
    print(f"        n = {n_:3d}, growth {g_:.3f}  ->  outer radius {0.02 * (g_**n_ - 1) / (g_ - 1):.0f} kpc")
print(f"\n  {'mesh':>10}{'MI worst':>11}{'MI f_M*':>10}{'AQUAL worst':>13}{'AQUAL f_M*':>12}"
      f"{'AQUAL - MI':>13}{'both clear':>12}")
print("  " + "-" * 84)
CONV = []
for mi_idx, (n_, g_) in enumerate(MESHES):
    rm = minimax(AQ_C[0], A0_CANON, ("MI", nu), nu, "exc", mesh=mi_idx)
    ra = minimax(AQ_C[0], A0_CANON, ("AQUAL", mu_exp), nu, "exc", mesh=mi_idx)
    CONV.append((n_, rm[0], ra[0]))
    print(f"  {n_:>10}{rm[0]:>11.4f}{rm[1]:>10.4f}{ra[0]:>13.4f}{ra[1]:>12.4f}{ra[0] - rm[0]:>+13.4f}"
          f"{('YES' if max(rm[0], ra[0]) < BOX else 'NO'):>12}   [{time.time() - T0:.0f}s]")
mesh_drift = max(max(abs(CONV[i][1] - CONV[j][1]), abs(CONV[i][2] - CONV[j][2]))
                 for i in range(len(CONV)) for j in range(len(CONV)))
gaps = [c[2] - c[1] for c in CONV]
check(all(max(c[1], c[2]) < BOX for c in CONV),
      f"D5b the box clearance SURVIVES mesh refinement for both theories: at n = 110 / 150 / 190 the minimaxed "
      f"worst constraint is {CONV[0][1]:.3f} / {CONV[1][1]:.3f} / {CONV[2][1]:.3f} (MI) and {CONV[0][2]:.3f} / "
      f"{CONV[1][2]:.3f} / {CONV[2][2]:.3f} (AQUAL), all below {BOX:.1f}. So D4a is not a coarse-mesh artefact "
      f"-- the granularity that mattered was the (f_M, f_R) SEARCH, not the solver mesh")
check(min(gaps) > 0.0 and max(abs(g) for g in gaps) < 0.25 and mesh_drift > 0.0,
      f"D5c the AQUAL-minus-MI gap is stable in SIGN and small in SIZE across resolutions -- {gaps[0]:+.3f} / "
      f"{gaps[1]:+.3f} / {gaps[2]:+.3f} at n = 110 / 150 / 190, all positive and all under 0.25 sigma -- while "
      f"the worst constraint itself drifts {mesh_drift:.3f} sigma over the same refinement. MI is consistently "
      f"the marginally closer of the two, and consistently by less than the mesh moves the answer")


banner("D6  IS CLEARING THE BOX THE SAME AS FITTING THE GALAXY? -- chi2, dof and p, because it is not")

NPAR, NCON = 2, 5
DOF = NCON - NPAR
ALLC = []
for label, (bst, rows) in MM.items():
    for (fRr, Wr, fmr, orr, bk, sdr, itr) in rows:
        ALLC.append((chi2f(orr)[0], label, fmr, fRr, orr, Wr))
ALLC.sort()
print(f"""  {NCON} constraints, {NPAR} free parameters -> {DOF} effective dof. AIC = chi2 + 2k with the SAME k in
  every row, so Delta AIC = Delta chi2 and no row buys its chi2 with a parameter the others do not have. The
  cells listed are the MINIMAX cells, so their chi2 is an upper bound on each configuration's chi2 minimum.\n""")
print(f"  {'configuration':<32}{'cell':>17}{'chi2':>8}{'chi2/dof':>10}{'p (3 dof)':>11}"
      f"{'worst sigma':>13}{'binding':>9}")
print("  " + "-" * 101)
seen = set()
for c_, label, fmr, fRr, orr, Wr in ALLC:
    if label in seen:
        continue
    seen.add(label)
    print(f"  {label:<32}{f'({fmr:.3f}, {fRr:.2f})':>17}{c_:>8.2f}{c_ / DOF:>10.2f}"
          f"{chi2dist.sf(c_, DOF):>11.4f}{Wr:>13.3f}{binding(orr):>9}")
c_best, l_best = ALLC[0][0], ALLC[0][1]
p_best = float(chi2dist.sf(c_best, DOF))
sig_eq = math.sqrt(float(chi2dist.isf(p_best, 1)))
check(p_best < 0.10,
      f"D6a *** AGAINST INTEREST, AND IT MATTERS: CLEARING THE BOX IS NOT FITTING THE GALAXY. *** The lowest "
      f"joint chi2 anywhere in this run is {c_best:.2f} on {DOF} dof ({l_best.strip()}), i.e. p = {p_best:.4f}, "
      f"a ~{sig_eq:.1f} sigma JOINT tension. A 2-sigma-per-constraint box is a much weaker test than a joint "
      f"chi2 because it ignores how MANY constraints are simultaneously strained, and at these minimax cells "
      f"three or four of the five sit above 1 sigma with correlated signs. The honest statement is 'a "
      f"configuration exists that violates no SINGLE constraint at 2 sigma', not 'the Milky Way is fit'")
mi_c2 = min(c for c, l, *_ in ALLC if l.startswith("Route A  MI"))
aq_c2 = min(c for c, l, *_ in ALLC if l.startswith("Route A  AQUAL"))
check(abs(mi_c2 - aq_c2) < 2.30,
      f"D6b and on chi2 the two theories are formally indistinguishable at the SAME parameter count: "
      f"Delta chi2 = {aq_c2 - mi_c2:+.2f} ({mi_c2:.2f} MI against {aq_c2:.2f} AQUAL) versus the 2.30 that one "
      f"sigma on two joint parameters requires -- and Delta AIC is the same {aq_c2 - mi_c2:+.2f}. Whatever MI "
      f"is worth on this front, it is not worth a sigma")


banner("D7  THE ANSWER TO THE QUESTION ASKED")

fRb, Wb, fmb, ob = MI_C[0], MI_C[1], MI_C[2], MI_C[3]
sb = sigmas(ob)
print(f"""  (a) DONE. The five observables were computed under the algebraic MI law -- a = nu(|g_bar|/a0) g_bar as
      a POINTWISE VECTOR map on the Newtonian baryonic field, direction by direction, the boost set by the
      full Newtonian magnitude at each point -- on the anchor's own baryons, priors and chi2, with the same
      two free parameters as L7a and one interpolated extractor for both observables.

  (b) DOES MI CLEAR THE BOX WHERE AQUAL CANNOT?   NO -- because AQUAL clears it too.
        MI algebraic  : {MI_C[1]:.3f} sigma canonical (f_M, f_R = {fmb:.3f}, {fRb:.2f}),  {MI_A[1]:.3f} sigma ALT
        AQUAL field   : {AQ_C[1]:.3f} sigma canonical (f_M, f_R = {AQ_C[2]:.3f}, {AQ_C[0]:.2f}),  {AQ_A[1]:.3f} sigma ALT
        L7a's published AQUAL number was 2.07, reproduced here as {gaq_c[0]:.3f} ON ITS OWN GRID (D3a).
      The 2.07 was the granularity of an (f_M, f_R) grid whose finest step was 0.15 in f_M -- not a property
      of the theory. Optimise the same two parameters and the AQUAL calculation L7a already ran comes in at
      {AQ_C[1]:.3f} sigma. So the escape this lane was sent to test is not needed, and it is not the escape.
      MI's own best cell: v_c {sb['vc']:+.3f}s, Sigma_dyn {sb['sd']:+.3f}s, M_* {sb['mstar']:+.3f}s,
      R_d {sb['rd']:+.3f}s, Sigma_* {sb['sig']:+.3f}s, chi2 {chi2f(ob)[0]:.2f} on {DOF} dof.

  (c) WHAT MI COSTS, stated not buried. The corpus's 2026-08-01 result stands: for this form class the MI law
      is NOT VARIATIONAL in a disc (not variational; the u-contraction (v/c)^2-suppressed for generic K; the
      prefactor IS the worldline's Frenet torsion). Route A's kernel DOES satisfy Milgrom 2022's condition for
      an MI theory written at the level of the EOM -- x mu(x) strictly monotonic, verified in D1c over eighteen
      decades -- and Milgrom is explicit that such theories "are not necessarily governed by an action". That
      admissibility is real, and it is also the whole cost. D2a measures the consequence: a circulation of up
      to {100 * mical:.2f}% of a leg's work, i.e. up to {100 * bigE:.1f}% of the Galaxy's specific circular
      kinetic energy gained per closed circuit in the (R, z) plane, with the Newtonian control closing to
      {ctrl:.0e}. No potential, so no energy integral -- and the vertical Jeans analysis that DEFINES the 73.9
      target assumes both. AQUAL has this identically zero.

  (d) IS AN MI CLEARANCE EVIDENCE FOR MI OVER MG?   NEITHER -- and not for the reason the brief anticipated.
      It is NOT "a theory that fits because it is harder to solve properly": MI is EASIER to solve (one linear
      Newtonian solve, no Picard iteration) and its boost is MORE rigid than AQUAL's, not less -- exactly
      isotropic at every point, with no curl field free to redistribute force. MI adds no freedom: same two
      parameters, and D6b gives Delta chi2 = {aq_c2 - mi_c2:+.2f}. What it is instead is UNRESOLVED. The
      MI-minus-AQUAL difference on the binding constraint is {dc:.3f} sigma canonical and {da:+.3f} sigma ALT,
      against a numerical floor of {FLOOR_VC_SIG:.2f} sigma measured where the two theories are provably
      identical (D1b), an extractor systematic of {ext_shift:.3f} sigma (D5a) and a mesh drift of
      {mesh_drift:.3f} sigma (D5c). The Milky Way vertical/radial front does not discriminate modified inertia
      from modified gravity at achievable accuracy, so an MI clearance here would buy no evidence even if
      AQUAL had failed -- and AQUAL did not fail.""")

check(FLOOR_VC_SIG > abs(dc) and ext_shift > abs(dc),
      f"D7a the closing arithmetic, asserted so it can fail: the MI-vs-AQUAL separation of {abs(dc):.3f} sigma "
      f"is smaller than the numerical floor ({FLOOR_VC_SIG:.2f} sigma, D1b) AND smaller than the extractor "
      f"systematic ({ext_shift:.3f} sigma, D5a); the mesh drift is {mesh_drift:.3f} sigma for comparison. "
      f"MI-vs-MG is UNDECIDED on this front in the direction of 'cannot tell', not 'they agree'")


banner("SCOPE AND CAVEATS")
print(f"""   * NO error bar was widened, and none was tightened. The five constraints are the anchor's, byte for
     byte: v_c(R0) = 233.1e3 +- 3.0e3 m/s and Sigma_dyn(|z| < 1.1 kpc) = 73.9 +- 6.0 Msun/pc^2 as DATA;
     M_* = 54.3e9 +- 5.7e9 Msun, R_d,thin = 2.6 +- 0.52 kpc and Sigma_* = 38.0 +- 4.0 Msun/pc^2 as PRIORS.
     Nothing here clears because a systematic was stretched. Note which way the one available widening would
     go: the +-3.0 on v_c is McMillan's STATISTICAL error and this corpus's own compilation is +-4.0, which
     would be MORE permissive -- the HARDER number is the one in force throughout.
   * TWO free parameters, the anchor's own (f_M, f_R), so the parameter count of every number above equals
     L7a's exactly. The improvement over L7a came from OPTIMISING two parameters, not from adding any; D6
     reports chi2, chi2/dof, p and the (identical) AIC penalty so a reader can check that.
   * a0 was an INPUT throughout, both footings, never fitted: canonical {A0_CANON:.4e} and ALT {A0_ALT:.4e}.
   * The MI law is applied to the Newtonian field of the SAME baryons with the boost set by the full local
     |g_bar|. The alternative reading -- boosting each component by nu of that component alone -- is NOT the
     modified-inertia EOM (mu(|a|/a0) a = -grad Phi_N depends on |a|) and is not used anywhere here.
   * NOT tested, and each could move this: the ANISOTROPIC effective inertia of MI (the vertical restoring
     force on a star already in circular motion is a transverse response, not the mean acceleration used
     above); Milgrom's NONLOCAL momentum-conserving MI models rather than the algebraic limit; the full
     rotation curve rather than v_c(R0) alone; thin and thick discs freed separately; R0 and the gas freed;
     the external-field effect.
   * The circulation in D2a is exact for a Miyamoto-Nagai disc, which is not the McMillan mass model. It
     demonstrates that the pathology exists and measures its scale, not its precise Galactic value.
   * D3a reproduces L7a from the anchor's own procedure, so the disagreement with L7a's HEADLINE is a
     disagreement about the SEARCH, not about the solver, the baryons, the priors or the kernel.""")

banner("RESULT")
npass = sum(1 for t, _ in ok if t)
print(f"  {npass}/{len(ok)} checks held.   [{time.time() - T0:.0f}s; {NS['aqual']} AQUAL solves, "
      f"{NS['newt']} Newtonian solves]")
if npass != len(ok):
    print("\n  FAILED:")
    for t, m in ok:
        if not t:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: the algebraic MI law solved on the anchor's Milky Way, both footings, a0 an input, against an "
      "AQUAL comparator run on the same mesh, the same baryons and the same extractor.")
