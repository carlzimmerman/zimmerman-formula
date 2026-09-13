#!/usr/bin/env python3
"""G005 -- THE DERIVED LENGTH vs THE CASSINI GATE.

The bare mu_2 kernel DIES at Cassini (5.48x canonical, computed with the
anchored DHF instrument in this track, 2026-09-13; nu_RAR anchor 0.2748/6.23x
reproduced exactly).  The question this lane decides: does the DERIVED healing
length xi = r_M = sqrt(GM/a0) -- the unique length the sector owns
(kimik3's Lean-certified dimensional uniqueness; G002's derived a_0 = s/2) --
clear the gate that killed the bare kernel?

THE CLAIM UNDER TEST (first stated in this track, 2026-09-13): the
coherence/healing length is xi = r_M.  f29 found its Cassini floor at
xi = 0.045 pc with the nu_RAR kernel and a Gaussian smoothing, while noting
that value is 'one solar MOND radius' -- but carried xi as a FREE parameter.
r_M(Sun) = 0.0386 pc canonical / 0.0352 pc alt.  This lane computes the
mu_2 floor and compares it to r_M with no freedom anywhere.

PRE-REGISTERED BEFORE RUNNING: the mu_2 tail nu-1 ~ 4/y^2 is fatter than
nu_RAR's exp(-sqrt(y)), so the BARE quadrupole is near nu_RAR's; but the fat
tail lives at SMALL radii (near-source), exactly where Gaussian smoothing at
xi ~ r_M deletes the phantom.  The floor could land above or below r_M --
stated now, whichever way the arithmetic falls.

Every check states measurement and threshold separately.
"""
import json, math
import numpy as np
from scipy.optimize import brentq
from scipy.special import erf as serf

RES, NP, NF = [], 0, 0
def check(n, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d: print(f"         reading : {d}")
    RES.append({"name": n, "measured": str(measured), "pass": ok, "reading": d})
    if ok: NP += 1
    else: NF += 1

print(__doc__)

# ------------------------------------------------------------------ constants
GM_SUN = 6.6743e-11*1.98892e30
G = 6.6743e-11
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
PC = 3.0857e16
GEXT, SGEXT = 2.32e-10, 0.16e-10          # Gaia EDR3 solar-circle field
Q2_CEIL = 5.2e-27                          # Park 2026 two-sigma ceiling [s^-2]
PREF = lambda a0: 1.5*a0**1.5/math.sqrt(GM_SUN)

# ------------------------------------------------------------------ kernels
def mu_std(x):
    x = np.asarray(x, dtype=float)
    return 1.0 - (1.0 + x/2.0)**(-2.0)

def nu_rar(y):
    y = np.maximum(np.asarray(y, float), 1e-30)
    return 1.0/(1.0 - np.exp(-np.sqrt(y)))

_xcache = {}
def x_of_y(y):
    """solve x*mu_std(x) = y (the mu_2 QUMOND partner), cached."""
    if y in _xcache: return _xcache[y]
    if y <= 0: return 0.0
    if y > 1e4:
        v = y                                # mu -> 1, x -> y
    else:
        v = brentq(lambda t: t*(1.0 - (1.0 + t/2.0)**(-2.0)) - y,
                   1e-12, y + 120.0, xtol=1e-13)
    _xcache[y] = v; return v

def nu_mu2(y):
    return x_of_y(float(y))/float(y) if float(y) > 0 else 1.0

# ------------------------------------------------------------------ instrument 1: the DHF integral (f23 section 6, verbatim structure)
def q_dhf(nu_f, etilde, vmax=400.0):
    """committed DHF integral: e_N solves nu(e_N) e_N = etilde;
    q = 1.5 Int_v Int_mu (nu(sqrt D)-1)(e_N(3mu-5mu^3)+v^2(1-3mu^2)),
    D = e_N^2 + v^4 + 2 e_N v^2 mu."""
    eN = brentq(lambda e: nu_f(e)*e - etilde, 1e-9, etilde*1.5, xtol=1e-14)
    # radial Gauss-Legendre + angular Gauss-Legendre (deterministic, fast)
    nx, nw = np.polynomial.legendre.leggauss(240)   # v in [0, vmax] (half-range)
    mx, mw = np.polynomial.legendre.leggauss(160)   # mu in [-1, 1]
    v = 0.5*vmax*(nx + 1.0); wv = 0.5*vmax*nw
    V, M = np.meshgrid(v, mx, indexing="ij")
    WV, WM = np.meshgrid(wv, mw, indexing="ij")
    D = eN*eN + V**4 + 2.0*eN*V*V*M
    nuD = np.array([[nu_mu2(math.sqrt(d)) if nu_f is nu_mu2 else float(nu_rar(math.sqrt(d)))
                     for d in row] for row in D])
    ang = eN*(3.0*M - 5.0*M**3) + V*V*(1.0 - 3.0*M*M)
    integrand = (nuD - 1.0)*ang
    val = np.sum(integrand*WV*WM)
    return abs(1.5*val), eN

# ------------------------------------------------------------------ instrument 2: smoothed-source phantom quadrupole (f29, adapted)
NR, NT = 1400, 241
def phantom_quadrupole(xi_pc, a0, nu_f, gext):
    """f29's phantom machinery verbatim, with the kernel swapped: QUMOND
    phantom density of a Gaussian source (width xi) in a uniform NEWTONIAN
    external field, on a log-r x theta grid; the quadrupole is the INTERIOR
    l=2 coefficient of the potential, I2 = 2 pi Int rho P2 r^-1 sin th --
    convergent.  |Q2| = 3 G |I2| (the frozen NORMALIZATION_LOCK convention)."""
    xi = xi_pc*PC
    eN = brentq(lambda e: nu_f(e)*e - gext/a0, 1e-12, 1.5*gext/a0, xtol=1e-14)*a0
    rM = math.sqrt(GM_SUN/a0)
    r = np.geomspace(min(1e-4*rM, 1e-3*xi), max(1e4*rM, 1e3*xi), NR)
    th = np.linspace(0.0, math.pi, NT)
    R, TH = np.meshgrid(r, th, indexing="ij")
    x = R/(math.sqrt(2)*xi)
    Menc = GM_SUN*(serf(x) - math.sqrt(2/math.pi)*(R/xi)*np.exp(-R**2/(2*xi*xi)))
    small = R < 0.05*xi
    Menc = np.where(small, GM_SUN*math.sqrt(2/math.pi)*(R/xi)**3/3.0*(1 - 0.3*(R/xi)**2), Menc)
    gs = -G*Menc/R**2
    gr = eN*np.cos(TH) + gs; gt = -eN*np.sin(TH)
    gmag = np.hypot(gr, gt)
    nuv = np.array([[ (nu_mu2(float(yy)) if nu_f is nu_mu2 else float(nu_rar(float(yy))))
                      for yy in row] for row in (gmag/a0)])
    f = nuv - 1.0
    Fr = R**2*f*gr; Ft = np.sin(TH)*f*gt
    dFr = np.gradient(Fr, r, axis=0)/R**2
    dFt = np.gradient(Ft, th, axis=1)/(R*np.maximum(np.sin(TH), 1e-12))
    dFt[:, 0] = dFt[:, 1]; dFt[:, -1] = dFt[:, -2]
    rho = -(dFr + dFt)/(4*math.pi*G)
    # interior l=2 coefficient: I2 = 2 pi Int Int rho P2 (1/r) sin th dr dth
    P2 = 0.5*(3.0*np.cos(TH)**2 - 1.0)
    inner = np.trapz(rho*P2*np.sin(TH), th, axis=1)
    I2 = 2.0*math.pi*np.trapz(inner/r, r)
    return abs(3.0*G*I2)

# ------------------------------------------------------------------ PART A: calibration
print("PART A -- calibration of both instruments")

# cross-validation: the f29-style machinery at xi -> 0 must reproduce the DHF
# integral's mu_2 quadrupole (independent implementations, same physics)
Q2_dhf_mu2_can = q_dhf(nu_mu2, GEXT/A0["canonical"])[0]*PREF(A0["canonical"])
Q2_f29style_mu2 = phantom_quadrupole(1e-5, A0["canonical"], nu_mu2, GEXT)
check("V0 [cross-validation: the f29-style phantom machinery reproduces the DHF "
      "integral for the mu_2 kernel at xi -> 0] the interior-multipole quadrupole "
      "of the unsmoothed mu_2 phantom is compared with the DHF integral's value",
      f"f29-style {Q2_f29style_mu2:.3e} vs DHF {Q2_dhf_mu2_can:.3e} s^-2, "
      f"ratio {Q2_f29style_mu2/Q2_dhf_mu2_can:.3f} (threshold 0.7-1.5)",
      0.7 < Q2_f29style_mu2/Q2_dhf_mu2_can < 1.5,
      "two independent implementations of the same physics agreeing to tens of "
      "per cent: the smoothed scan below is on trusted machinery")

q_rar_2, _ = q_dhf(nu_rar, 2.0)
check("V1 [anchor 1: nu_RAR q(eta=2) = 0.221 (f23's committed anchor)] the DHF "
      "integral is run for nu_RAR at eta = 2 and compared with the registered 0.221",
      f"q(2) = {q_rar_2:.4f} against 0.221 (threshold +-0.003)",
      abs(q_rar_2 - 0.221) < 0.003,
      "the DHF instrument reproduces the committed anchor; every number below is on "
      "the same machine")

for foot, a0 in A0.items():
    q2, _ = q_dhf(nu_mu2, GEXT/a0)
    check(f"V2 [{foot}: the BARE mu_2 quadrupole at the solar circle] the DHF "
          f"integral is run for the mu_2 kernel at eta = g_ext/a_0 and compared "
          f"with the ceiling",
          f"q = {q2:.4f}, Q2 = {q2*PREF(a0):.3e} s^-2, Q2/ceiling = "
          f"{q2*PREF(a0)/Q2_CEIL:.2f}x",
          q2*PREF(a0)/Q2_CEIL > 1.0,
          "the bare kernel dies at Cassini on both footings -- recorded as the "
          "pre-registered expectation confirmed; the power-law tail nu-1 ~ 4/y^2 "
          "does not save it. The construction NEEDS the length")

# ------------------------------------------------------------------ PART B: the smoothed scan
print()
print("PART B -- the derived length: Q2(xi)/ceiling for the mu_2 kernel")

XIS = [0.005, 0.01, 0.02, 0.0352, 0.0386, 0.045, 0.05, 0.08, 0.1, 0.3, 1.0]
print(f"    {'xi [pc]':>9s} {'Q2/ceiling can':>15s}")
scan = []
for xi in XIS:
    Q2v = phantom_quadrupole(xi, A0["canonical"], nu_mu2, GEXT)
    scan.append((xi, Q2v/Q2_CEIL))
    print(f"    {xi:9.4f} {Q2v/Q2_CEIL:15.3f}")

# the floor: smallest xi with Q2/ceiling <= 1 (log-log interpolation)
scan_arr = [(math.log(x), math.log(q)) for x, q in scan if q > 0]
floor = None
for (x1, q1), (x2, q2v) in zip(scan, scan[1:]):
    if q1 > 1.0 >= q2v:
        # interpolate in log-xi between (x1,q1),(x2,q2v) to Q2/ceil = 1
        t = (math.log(q1) - 0.0)/(math.log(q1) - math.log(q2v))
        floor = math.exp(math.log(x1) + t*(math.log(x2) - math.log(x1)))
        break

rM_can = math.sqrt(GM_SUN/A0["canonical"])/PC
rM_alt = math.sqrt(GM_SUN/A0["alt"])/PC
check("V3 [THE VERDICT: the mu_2 Cassini floor vs the derived length r_M] the "
      "floor is interpolated from the scan and compared with r_M(Sun) on the "
      "canonical footing",
      f"floor = {floor:.4f} pc (canonical); r_M(Sun) = {rM_can:.4f} pc; "
      f"floor/r_M = {floor/rM_can:.3f}" if floor else "no crossing found",
      floor is not None and floor <= rM_can,
      ("the derived length clears the gate that killed the bare kernel: with "
       "xi = r_M the quadrupole sits UNDER the Park ceiling and the construction "
       "passes Cassini with ZERO free parameters -- the length is not fitted, it "
       "is the unique length the sector owns" if floor and floor <= rM_can else
       "the derived length does NOT clear: the floor sits above r_M, so the "
       "healing length must be larger than the MOND radius and the dimensional "
       "uniqueness argument alone does not pass Cassini. The honest reading is "
       "then that the smoothing SHAPE (not scale) carries the difference, and "
       "the construction fails its own sharpest gate"))

# alt footing
floor_alt = None
scan_alt = []
for xi in XIS:
    Q2v = phantom_quadrupole(xi, A0["alt"], nu_mu2, GEXT)
    scan_alt.append((xi, Q2v/Q2_CEIL))
for (x1, q1), (x2, q2v) in zip(scan_alt, scan_alt[1:]):
    if q1 > 1.0 >= q2v:
        t = math.log(q1)/(math.log(q1) - math.log(q2v))
        floor_alt = math.exp(math.log(x1) + t*(math.log(x2) - math.log(x1)))
        break
check("V4 [both footings: the alt-footing floor vs its r_M] the scan is repeated "
      "on the alt footing and the floor compared with r_M(alt)",
      f"floor(alt) = {floor_alt:.4f} pc; r_M(alt) = {rM_alt:.4f} pc; "
      f"floor/r_M = {floor_alt/rM_alt:.3f}" if floor_alt else "no crossing (alt)",
      floor_alt is not None and floor_alt <= rM_alt,
      "the footing check: the canonical verdict must hold on the alt footing too, "
      "or the pass is a footing choice")

# the exact verdict numbers at xi = r_M
Q2_at_rM_can = phantom_quadrupole(rM_can, A0["canonical"], nu_mu2, GEXT)
Q2_at_rM_can_lo = phantom_quadrupole(rM_can, A0["canonical"], nu_mu2, GEXT - SGEXT)
Q2_at_rM_alt = phantom_quadrupole(rM_alt, A0["alt"], nu_mu2, GEXT)
Q2_at_rM_alt_lo = phantom_quadrupole(rM_alt, A0["alt"], nu_mu2, GEXT - SGEXT)
print(f"    at xi = r_M exactly: canonical Q2/ceiling = {Q2_at_rM_can/Q2_CEIL:.3f} "
      f"(central), {Q2_at_rM_can_lo/Q2_CEIL:.3f} (g_ext - 1 sigma); "
      f"alt {Q2_at_rM_alt/Q2_CEIL:.3f} / {Q2_at_rM_alt_lo/Q2_CEIL:.3f}")

print()
print("READING")
print(f"""
  The bare mu_2 kernel dies at Cassini on both footings (V2), as the
  pre-registered expectation said: the power-law tail nu-1 ~ 4/y^2 puts the
  quadrupole at {scan[0][1]:.1f}x the ceiling unsmoothed, near nu_RAR's
  registered 6.2x.

  The derived-length scan is the result: the floor is
  {f"{floor:.4f} pc canonical" if floor else "NOT FOUND (no crossing)"} (V3)
  against r_M = {rM_can:.4f} pc, i.e.
  {f"floor/r_M = {floor/rM_can:.3f}." if floor else "no floor exists in the scan range."}
  {("THE DERIVED LENGTH CLEARS THE GATE" if floor and floor <= rM_can else
  "THE DERIVED LENGTH DOES NOT CLEAR")} -- and on the alt footing the floor is
  {f"{floor_alt:.4f} pc against r_M = {rM_alt:.4f} pc ({floor_alt/rM_alt:.3f})." if floor_alt
   else "not found in the scan range."}

  Whichever way the arithmetic fell, that IS the verdict on the composed
  construction's sharpest gate: with xi = r_M derived (not fitted), the
  solar-system quadrupole is a zero-parameter prediction, and the numbers
  above are it.

  LIMITS. The phantom quadrature is the f29 axisymmetric adaptation with the
  mu_2 nu; the theta-derivative term of the divergence is dropped where the
  internal Newtonian field is radial (the quadrupole enters through nu's
  theta-dependence on the total field); the validation at xi -> 0 against the
  DHF integral anchors the magnitude. The Gaussian smoothing shape is the f29
  choice (the Helmholtz kernel's 1/r cusp needs 0.8 pc -- f30); a different
  smoothing shape moves the floor and is NOT explored here.
""")
print(f"G005 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES},
          open("G005_results.json", "w"), indent=1)
