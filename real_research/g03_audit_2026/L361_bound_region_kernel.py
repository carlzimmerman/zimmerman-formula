#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L361 -- THE BOUND-REGION KERNEL: a MOND kernel that reads only its own bound region's baryons, built from an action.

WHY.  Every KiDS-1000 failure of the C-H/K kernel on the record is one mechanism: the kernel's argument contains the
cosmic web's field, and the external-field effect ends each isolated lens's phantom near 0.1 Mpc.
  * total field in the argument: excluded (BS2 +570, BS3 after isolation and 2-halo);
  * baryons-only argument (L353's kernel-invisible construction): still +233 (L355 K2; BS3 +133..+152 beyond 0.3 Mpc);
  * a Yukawa-screened argument with one free length (BK1, lambda ~ 0.7 Mpc): a near miss, +7.7 against the EFE-free
    idealisation, with lambda underivable (BK2) and a growth-vs-KiDS pincer at any constant switch threshold (BK3).
BS3 names the door: "a kernel blind to the large-scale field: one sourced only by the bound region's own matter", which
must still hand the Sun the Galaxy's field (L340 S1).  L359's vacuum-gated switch supplies the bound region.  This lane
builds the kernel on it.

THE CONSTRUCTION (a construction, not a derivation).  f(x) = the gated switch of L359 (1 inside bound regions, 0 in the
inactive web); M^2 = m^2 (1 - f), a screening mass that acts only in the inactive web.  Non-relativistic Lagrangian:
   L = -(rho_b + rho_d) phi - |grad phi|^2/(8 pi G)                                   Newtonian gravity, all matter
       - f rho_b psi - [2 grad psi.grad w + 2 M^2 psi w - a0^2 f Q(|grad w|^2/a0^2) - (1 - f)|grad w|^2]/(8 pi G)
       + f rho_b chi + [|grad chi|^2 + M^2 chi^2]/(8 pi G)          region-local QUMOND minus its Newtonian self-term
  Field equations (derived symbolically in R0):
      lap phi = 4 pi G (rho_b + rho_d);   (lap - M^2) w = 4 pi G f rho_b;   chi = w;
      (lap - M^2) P = div[ f (nu(|grad w|/a0) - 1) grad w ] + M^2 w,   P = psi - chi   (Q'(s) = nu(sqrt s));
  the M^2 w term lives only in the inactive web within ~1/m of a region's edge -- a thin layer that exerts no force inside
  a spherical region and is itself screened outside.
  In-region baryons move in phi + f P (Newtonian from everything + their own region's MOND phantom); web gas and the
  carrier move in phi (Newtonian).  w is sourced only by the region's baryons and cannot cross the inactive web (the
  screening), so no field from outside a bound region enters its kernel -- neither the carrier's nor the web gas's nor
  another region's.  Inside a region there is no screening: the Sun reads the whole Galaxy.  The phantom is in
  divergence form, so it is cancelled at the region's edge (L352 Z1): beyond it, matter weighs its baryons + carrier.
  The one new constant is m, and it enters only through a one-sided bound (the gap must screen); m -> infinity is a
  Dirichlet limit with the same physics.

CHECKS
  R0 the Euler-Lagrange equations of L (sympy; a concrete non-trivial kernel Q, generic f(x), M^2(x)) are the field
     equations above; inside a region (f = 1, M = 0) P is exactly the region's QUMOND phantom.
  R1 DECOUPLING: the uniform (l = 1) w-field of the rest of the universe transmitted into a region (radius R_e) through an
     inactive gap (to R_2) -- exact, modified spherical Bessel functions -- falls as exp[-m (R_2 - R_e)]; an independent
     finite-difference solve controls it.
  R2 THE SUN keeps the Galaxy's field: monopole exact, the l >= 2 image correction ~ (r/R_e)^(2l+1) (L340 S1 needs >= 99.9%).
  R3 KiDS-1000 (L355's machinery, unedited): at the bound-region kernel's own field (transmitted, even with ALL baryons
     counted as active) Delta chi^2 <= +9 against isolated MOND, both footings -- while the total-field and
     baryons-only kernels fail (controls, reproduced) and a source-restricted but unscreened kernel is reported.
  R4 (reported) the bound on m: the largest screening length for which R3 still passes.
  R5 GAUSS per region: the phantom's total mass vanishes beyond the edge (zero monopole -> no large-scale effect; the
     linear growth of L359 G1 is the construction's).
MUTATE=1 removes the construction (the kernel reads the full baryonic field, no screening: L353's kernel): R1 and R3
must FAIL (rc = 1).
SCOPE.  Non-relativistic; f is treated as a prescribed field in R0 (its own variation gives the edge terms of L351/L352);
the relativistic embedding follows L353's auxiliary-field pattern and is not redone; the active-baryon fraction is not
computed (R3 counts all baryons as active, the conservative case); the late-time dynamics of baryons inside active
filaments (their own deep-MOND field) is open.

Run from the repository root:  python3 real_research/g03_audit_2026/L361_bound_region_kernel.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
import sympy as sp
from scipy.special import spherical_in, spherical_kn
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L361_bound_region_kernel"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L361", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: the kernel reads the full baryonic field with no screening (L353's kernel); R1 and R3 must FAIL ***")

# ============================================================================================ R0 the field equations
banner("R0  THE FIELD EQUATIONS FROM THE LAGRANGIAN (sympy, one dimension; a concrete non-trivial Q, generic f(x), M^2(x))")
x = sp.symbols("x", real=True)
G_, a0_, c1, d1 = sp.symbols("G a0 c1 d1", positive=True)
phi, psi, w, chi = [sp.Function(n)(x) for n in ("phi", "psi", "w", "chi")]
rb, rd, f, M2 = [sp.Function(n)(x) for n in ("rho_b", "rho_d", "f", "M2")]
Qc = lambda s: s + c1 * s ** sp.Rational(3, 2) + d1 * sp.log(1 + s)          # a concrete, non-trivial kernel (any smooth Q works)
Qcp = lambda s: 1 + sp.Rational(3, 2) * c1 * sp.sqrt(s) + d1 / (1 + s)       # its derivative Q'(s) (= nu(sqrt s) for a real kernel)
wp = sp.diff(w, x); s_w = wp ** 2 / a0_ ** 2
fe = sp.Integer(1) if MUTATE else f; Me = sp.Integer(0) if MUTATE else M2   # MUTATE: L353's kernel (full baryonic source, no screening)
Lag = (-(rb + rd) * phi - sp.diff(phi, x) ** 2 / (8 * sp.pi * G_)
       - fe * rb * psi - (2 * sp.diff(psi, x) * wp + 2 * Me * psi * w - a0_ ** 2 * fe * Qc(s_w) - (1 - fe) * wp ** 2) / (8 * sp.pi * G_)
       + fe * rb * chi + (sp.diff(chi, x) ** 2 + Me * chi ** 2) / (8 * sp.pi * G_))
EL = {str(v.func): sp.euler_equations(Lag, [v], x)[0].lhs * 4 * sp.pi * G_ for v in (phi, psi, w, chi)}
target = {
    "phi": sp.diff(phi, x, 2) - 4 * sp.pi * G_ * (rb + rd),                                        # lap phi = 4 pi G rho
    "psi": sp.diff(w, x, 2) - Me * w - 4 * sp.pi * G_ * fe * rb,                                     # (lap - M^2) w = 4 pi G f rho_b
    "chi": -(sp.diff(chi, x, 2) - Me * chi - 4 * sp.pi * G_ * fe * rb),                              # chi = w
    "w": sp.diff(psi, x, 2) - Me * psi - sp.diff((fe * Qcp(s_w) + 1 - fe) * wp, x),                  # (lap - M^2) psi = div[(f Q' + 1 - f) grad w]
}
dev = {k_: sp.simplify(sp.expand(EL[k_] - target[k_])) for k_ in target}
# the phantom P = psi - chi on shell (chi = w):  (lap - M^2) P = div[f (Q' - 1) grad w] + M^2 w
Pp = sp.Function("Pph")(x)
phant = sp.simplify(sp.expand(EL["w"].subs(psi, Pp + w).doit()
                              - (sp.diff(Pp, x, 2) - Me * Pp - sp.diff(fe * (Qcp(s_w) - 1) * wp, x) - Me * w)))
for k_ in ("phi", "psi", "w", "chi"):
    P(f"    delta {k_:3s}: residual vs the stated field equation = {dev[k_]}")
P(f"    phantom P = psi - chi: residual vs (lap - M^2) P = div[f (Q' - 1) grad w] + M^2 w  ->  {phant}")
P("    (the M^2 w term lives only in the inactive web, within ~1/m of a region's edge: a thin layer that exerts no force inside a")
P("     spherical region and is itself screened outside; with f = 1, M = 0 the equations are L353's unscreened kernel)")
check("R0 the action's Euler-Lagrange equations are the bound-region field equations: lap phi = 4 pi G rho; (lap - M^2) w = "
      "4 pi G f rho_b; chi = w; (lap - M^2) psi = div[(f Q' + 1 - f) grad w]; so the phantom P = psi - chi obeys "
      "(lap - M^2) P = div[f (nu - 1) grad w] + M^2 w (checked with a concrete non-trivial kernel Q)",
      f"residuals {[str(v_) for v_ in dev.values()]}; phantom residual {phant}",
      all(v_ == 0 for v_ in dev.values()) and phant == 0,
      "in-region baryons couple to phi + f (psi - chi): Newtonian from everything plus their own region's phantom; web gas and "
      "the carrier couple to phi only (and so, by reciprocity, cannot source the phantom)")

# ============================================================================================ R1 decoupling
banner("R1  DECOUPLING: the l = 1 (uniform-field) w-mode transmitted into a region through a screened inactive gap")


def transmission(mInv, Re, R2):
    """exact l = 1 solution: w = A r (r < Re); B i1(m r) + C k1(m r) (Re < r < R2); e r + D/r^2 (r > R2), e = 1.
    Returns A (the uniform field inside per unit external field)."""
    if MUTATE or not np.isfinite(mInv) or mInv <= 0:
        return 1.0                                                   # no screening: the external field enters in full
    m = 1.0 / mInv
    i1, k1 = lambda r: spherical_in(1, m * r), lambda r: spherical_kn(1, m * r)
    di1, dk1 = lambda r: m * spherical_in(1, m * r, derivative=True), lambda r: m * spherical_kn(1, m * r, derivative=True)
    # unknowns [A, B, C, D];  w and w' continuous at Re and R2
    Mx = np.array([[Re, -i1(Re), -k1(Re), 0.0],
                   [1.0, -di1(Re), -dk1(Re), 0.0],
                   [0.0, i1(R2), k1(R2), -1.0 / R2 ** 2],
                   [0.0, di1(R2), dk1(R2), 2.0 / R2 ** 3]])
    rhs = np.array([0.0, 0.0, R2, 1.0])
    # rescale columns B and C to avoid overflow in i1 at large m r
    sB = max(abs(i1(R2)), 1e-300); sC = max(abs(k1(Re)), 1e-300)
    Mx[:, 1] /= sB; Mx[:, 2] /= sC
    sol = np.linalg.solve(Mx, rhs)
    return float(sol[0])


def transmission_fd(mInv, Re, R2, N=40000):
    """independent control: second-order finite differences for w'' + (2/r) w' - 2 w/r^2 - M(r)^2 w = 0 on [Re, 6 R2],
    with the exact interior condition w'(Re) Re = w(Re) (w = A r inside) and the exterior form w = r + D/r^2 at 6 R2."""
    m = 1.0 / mInv; Rmax = 6 * R2
    r = np.linspace(Re, Rmax, N); h = r[1] - r[0]
    Msq = np.where(r < R2, m ** 2, 0.0)
    lo = 1 / h ** 2 - 1 / (r * h); di = -2 / h ** 2 - 2 / r ** 2 - Msq; up = 1 / h ** 2 + 1 / (r * h)
    A = diags([lo[1:], di, up[:-1]], [-1, 0, 1], format="lil"); b = np.zeros(N)
    A[0, :] = 0; A[0, 0] = -1 / h - 1 / Re; A[0, 1] = 1 / h
    A[N - 1, :] = 0; A[N - 1, N - 1] = 1 / h + 2 / Rmax; A[N - 1, N - 2] = -1 / h; b[N - 1] = 3.0
    return float(spsolve(A.tocsr(), b)[0] / Re)


RE, R2G = 1.0, 3.0                                                   # Mpc: a lens region's edge; the nearest other active region (KiDS isolation: 3 Mpc)
MINV = [0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 2.0]
TR = {mi: transmission(mi, RE, R2G) for mi in MINV}
ctrl = transmission_fd(0.3, RE, R2G)
P("    R_e = 1 Mpc, gap to 3 Mpc; transmitted fraction of an external uniform w-field:")
P("      " + ", ".join(f"1/m = {mi:g} Mpc: {TR[mi]:.2e}" for mi in MINV))
P(f"      finite-difference control at 1/m = 0.3 Mpc: {ctrl:.3e}  (exact {TR[0.3]:.3e})")
OUT["numbers"]["R1"] = {"transmission": {str(k_): v_ for k_, v_ in TR.items()}, "bvp_control_0.3": ctrl}
slope = (math.log(TR[0.1]) - math.log(TR[0.2])) / (1 / 0.1 - 1 / 0.2) if not MUTATE else 0.0
check("R1 an inactive gap screens the rest of the universe out of a region's kernel: the transmitted uniform field falls as "
      "exp[-m (R_2 - R_e)] (log-slope ~ -(R_2 - R_e) = -2 Mpc), is < 1e-3 for 1/m <= 0.2 Mpc, and the exact solution matches the "
      "finite-difference control",
      f"T(1/m = 0.2) = {TR[0.2]:.2e}; T(0.1) = {TR[0.1]:.2e}; d ln T/d m = {slope:+.2f} Mpc; BVP/exact at 0.3 Mpc = "
      f"{ctrl / TR[0.3] if TR[0.3] else float('nan'):.4f}",
      (not MUTATE) and TR[0.2] < 1e-3 and abs(slope + (R2G - RE)) < 0.35 and abs(ctrl / TR[0.3] - 1) < 0.02,
      "m -> infinity is the Dirichlet limit: regions decouple exactly")

# ============================================================================================ R2 the Sun
banner("R2  THE SUN KEEPS THE GALAXY'S FIELD (L340 S1): no screening inside the Milky Way's bound region")
r_sun, R_mw = 8.2, 1000.0                                            # kpc; the MW's region edge ~ 1 Mpc (x~ = x_c,eff at delta ~ 3-5)
Md, Rd = 5e10, 2.6                                                   # disc mass and scale length (kpc)
q2_over_M = Rd ** 2                                                  # |quadrupole|/(mass) ~ R_d^2 for an exponential disc (order of magnitude)
img = [(r_sun / R_mw) ** (2 * l + 1) for l in (1, 2, 3)]
rel_q = q2_over_M / r_sun ** 2                                       # the disc's own l = 2 field relative to its monopole at the Sun
corr = rel_q * img[1]
OUT["numbers"]["R2"] = dict(image_factors=img, relative_quadrupole=rel_q, field_correction=corr)
P(f"    the monopole field inside a region is exact for any exterior; image factors (r/R_e)^(2l+1) at the Sun: "
  + ", ".join(f"l={l}: {v:.1e}" for l, v in zip((1, 2, 3), img)))
P(f"    the disc's l = 2 field at the Sun is ~{rel_q:.2f} of its monopole; the image correction to the Galaxy's field is ~{corr:.1e}")
check("R2 the Sun reads the Galaxy's field to better than 99.9% (the Galactic baryons are inside the same bound region, where "
      "the kernel is unscreened; the region's boundary changes the field at the Sun only through images ~ (r/R_e)^(2l+1))",
      f"relative correction {corr:.1e}", corr < 1e-3,
      "wide binaries and satellites keep their host's external field; only fields from OUTSIDE the bound region are removed")

# ============================================================================================ R3 KiDS
banner("R3  KiDS-1000 AT THE KERNEL'S OWN FIELD (L355's stacked-lens machinery, unedited)")
P55 = os.path.join(HERE, "L355_kernel_invisible_kids.py")
L55 = {"__name__": "l355", "__file__": P55}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(P55).read().split("# ============================================================================================ K1 control")[0], L55)
fit55, ES55, FIELDS55, sw55, mx55, Ob55, Om55 = [L55[k] for k in ("fit", "ES", "FIELDS", "stack_weights", "maxwell_e", "Ob", "Om")]
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
W0 = np.zeros(len(ES55)); W0[0] = 1.0
REF = {f_: fit55(f_, W0, 0.0, False)[0] for f_ in A0}
sig = FIELDS55["linear-theory (16 Mpc)"]                                # the web's 3D rms Newtonian field at the lenses (all matter)
FB = Ob55 / Om55
KERN = {"total field (BS2's construction)": 1.0,
        "baryons only (L353/L355)": FB,
        "active baryons only, unscreened (all baryons active)": FB,
        "active baryons only, unscreened (half active)": 0.5 * FB}
for mi in (0.1, 0.2, 0.3, 0.5, 1.0):
    KERN[f"bound-region kernel, 1/m = {mi:g} Mpc (all baryons active)"] = FB * TR[mi]
R3 = {}
for lab, kf in KERN.items():
    d_ = {}
    for f_ in A0:
        wts = sw55(mx55(sig * kf / A0[f_]))
        d_[f_] = fit55(f_, wts, 0.0, False)[0] - REF[f_]
    R3[lab] = dict(kernel_field_rms_a0={f_: sig * kf / A0[f_] for f_ in A0}, dchi2=d_)
    P(f"    {lab:62s}: field rms {sig * kf / A0['canonical']:.2e} a0 -> Delta chi^2 canonical {d_['canonical']:+.1f}, alt {d_['alt']:+.1f}")
OUT["numbers"]["R3"] = R3
own = "bound-region kernel, 1/m = 0.2 Mpc (all baryons active)"
ctrl_fail = R3["total field (BS2's construction)"]["dchi2"]["canonical"] > 100 and R3["baryons only (L353/L355)"]["dchi2"]["canonical"] > 100
check("R3 THE BOUND-REGION KERNEL PASSES KiDS-1000 at its own field: Delta chi^2 <= +9 against isolated MOND on both footings "
      "(1/m = 0.2 Mpc, every baryon counted as active) -- while the total-field and baryons-only kernels fail (> +100, the "
      "record's controls reproduced)",
      f"bound-region: canonical {R3[own]['dchi2']['canonical']:+.1f}, alt {R3[own]['dchi2']['alt']:+.1f}; total field "
      f"{R3['total field (BS2' + chr(39) + 's construction)']['dchi2']['canonical']:+.0f}; baryons only {R3['baryons only (L353/L355)']['dchi2']['canonical']:+.0f}",
      all(v <= 9.0 for v in R3[own]["dchi2"].values()) and ctrl_fail,
      "restricting the source removes the carrier and the web gas; the screened gap removes every other region; what is left "
      "is the isolated phantom that L352/L359/L360 score")

# ============================================================================================ R4 the bound on m
banner("R4  THE ONE NEW CONSTANT: how short must the gap's screening length be?")
passing = [mi for mi in (0.1, 0.2, 0.3, 0.5, 1.0) if all(v <= 9.0 for v in R3[f"bound-region kernel, 1/m = {mi:g} Mpc (all baryons active)"]["dchi2"].values())]
mmax = max(passing) if passing else float("nan")
OUT["numbers"]["R4"] = dict(passing_mInv=passing, max_mInv=mmax)
check("R4 (reported) the construction needs only a one-sided bound on the gap screening length (KiDS passes for every 1/m up "
      "to the bound; m -> infinity is the Dirichlet limit), not a tuned value", f"KiDS passes for 1/m <= {mmax:g} Mpc (tested "
      f"0.1-1 Mpc, 2 Mpc gap)", True, "contrast BK1/BK2: there a finite screening length acts INSIDE the lens and must be derived",
      load_bearing=False)

# ============================================================================================ R5 Gauss per region
banner("R5  GAUSS PER REGION: the switched phantom has zero total mass beyond the region's edge")
Gk = 4.30091727e-6; a0k = 9.3619e-11 * 3.0856775814913673e19 / 1e6          # kpc (km/s)^2/Msun; (km/s)^2/kpc
Mb = 6e10; r = np.geomspace(0.1, 5000.0, 20000); re_ = 1000.0
gN = Gk * Mb / r ** 2
nu = 1.0 / (1.0 - np.exp(-np.sqrt(gN / a0k)))
fstep = 0.5 * (1 - np.tanh((r - re_) / 20.0))
Mph = r ** 2 * fstep * (nu - 1) * gN / Gk                             # phantom mass inside r (flux of f (nu - 1) grad w)
beyond = float(np.max(np.abs(Mph[r > re_ + 200]))) / Mb
inside = float(np.max(Mph)) / Mb
OUT["numbers"]["R5"] = dict(max_phantom_inside_over_Mb=inside, max_phantom_beyond_over_Mb=beyond)
check("R5 the switched phantom is cancelled at the region's edge: beyond it the region weighs its baryons (zero phantom "
      "monopole), so the region-local kernel adds nothing on the scales of linear growth (L359 G1 stands)",
      f"phantom mass inside the edge up to {inside:.1f} M_b; beyond the edge |M_ph|/M_b <= {beyond:.1e}", beyond < 1e-6,
      "the divergence form makes each region's phantom a local redistribution (L352 Z1)", load_bearing=False)

# ============================================================================================ verdict
banner("VERDICT")
P(f"""  THE BOUND-REGION KERNEL IS BUILT.  One action: Newtonian gravity for everything plus a QUMOND kernel whose argument
  w is sourced only by the baryons inside the gated switch's bound region and is screened across the inactive web.  From
  it (R0): in-region baryons feel their own region's phantom on top of Newtonian gravity from everything; web gas and
  the carrier feel Newtonian gravity only.  A 2 Mpc inactive gap transmits {TR[0.2]:.1e} of an external field at 1/m = 0.2 Mpc
  (R1), the Sun keeps the Galaxy's field to {corr:.0e} (R2), and KiDS-1000 at the kernel's own field scores
  {R3[own]['dchi2']['canonical']:+.1f}/{R3[own]['dchi2']['alt']:+.1f} against isolated MOND where the total-field and baryons-only kernels
  score {R3['total field (BS2' + chr(39) + 's construction)']['dchi2']['canonical']:+.0f} and {R3['baryons only (L353/L355)']['dchi2']['canonical']:+.0f} (R3).
  The new constant m needs only 1/m <= {mmax:g} Mpc (R4).  With it, L359's switch and L360's assembled construction are
  scored at the construction's own field.
  OPEN: the relativistic embedding (L353's pattern), the switch's edge dynamics, and baryons inside active filaments at
  late times (their own deep-MOND field).""")
n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}   [{time.time() - T0:.0f}s]")
sys.exit(0 if n_fail == 0 else 1)
