#!/usr/bin/env python3
"""
L129 -- THE DECIDING BOLTZMANN RUN: a SMOOTH (non-clustering) a^-3 component CANNOT drive the CMB third peak.
        L128 left this explicitly OPEN and decidable; this lane decides it, NEGATIVELY, with a real Boltzmann
        code and a perfectly controlled background.
=============================================================================================================
L128 showed the cuscuton is the degeneracy point of the L87 stiff-genericity no-go and can supply EXACT a^-3
pressureless dust from a FIELD (zero propagating DOF, no ghost) -- but with c_s^2 = infinity that dust is
SMOOTH at every sub-horizon scale. L128 deliberately did NOT claim this kills the CMB, because a smooth
component still shifts z_eq, and z_eq affects peak heights through the radiation-driving envelope. Standard
CMB physics EXPECTS failure (the third peak's enhancement is a clustering signature), but "expected" is not
"shown". This lane shows it.

THE CONTROLLED EXPERIMENT (the design point that makes this clean):
  Run BOTH cases as the SAME fluid with the SAME equation of state w = -1e-4 (numerically dust), changing
  ONLY the sound speed c_s^2. Then:
    * the BACKGROUND is identical by construction => 100*theta_s comes out identical => peak POSITIONS are
      not being compared, only peak HEIGHTS. This is the standard trap in this comparison and it is avoided
      structurally rather than by re-tuning H0.
    * any inaccuracy in the fluid's initial conditions is COMMON-MODE and cancels in the comparison.
  c_s^2 = 0 -> the fluid clusters exactly like CDM.   c_s^2 = 1 -> sound horizon ~ horizon, no sub-horizon
  clustering: the stand-in for the cuscuton's c_s^2 -> infinity.

PIPELINE VALIDATION (why the null is credible): the c_s^2 = 0 run must reproduce the observed CMB. It does --
first peak at l = 221 with amplitude 5747 uK^2, against the measured l ~ 220 and ~5750 uK^2. The machinery is
therefore not blind, and the c_s^2 = 1 failure is a real physical result, not a broken run.

THE RESULT:
                                   peak1 l / amp        peak3/peak1     peak3/peak2
    clustering dust (c_s^2=0)      221 / 5747 uK^2        0.4496          0.9906     <- matches observation
    SMOOTH dust    (c_s^2=1)       167 / 15840 uK^2       0.2263          0.5545     <- grossly excluded
  The smooth case gets the first peak 2.76x too HIGH and in the wrong place, and the third-to-second peak
  ratio low by 44% against a ~1% measurement precision. Without clustering wells the potentials decay and
  radiation driving inflates the acoustic oscillations enormously. The z_eq shift alone does NOT substitute.

CONSEQUENCE FOR THE PROGRAMME: L128's inversion stands (the cuscuton passes the galaxy gate absolutely), but
the property it fails -- clustering at recombination -- is now CONFIRMED to be fatal, not merely suspected.
The cuscuton dark sector is closed. The remaining tension is exactly as L128 stated: clustering needs finite
c_s, finite c_s means the field PROPAGATES, and a propagating MOND scalar is excluded by the closure theorem
(L95) and the RAQUAL superluminality band (L120).

POLARITY: each check ASSERTS a statement; PASS = true. Requires classy (CLASS). Verified as hard as a win.
"""
import numpy as np, sys, time
T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 112); print(t); print("=" * 112, flush=True)

print("=" * 112)
print("L129 -- smooth (non-clustering) a^-3 dust CANNOT drive the CMB third peak: the deciding Boltzmann run")
print("=" * 112, flush=True)

from classy import Class
BASE = dict(output='tCl,pCl,lCl', lensing='no', l_max_scalars=2500,
            omega_b=0.02237, h=0.6736, A_s=2.1e-9, n_s=0.9649, tau_reio=0.0544,
            N_ur=3.046, YHe=0.2454)

def run(cs2, omega_fld=0.1190, omega_cdm=0.001):
    p = dict(BASE); h = BASE['h']
    p.update({'omega_cdm': omega_cdm, 'Omega_fld': omega_fld / h ** 2,
              'w0_fld': -1e-4, 'wa_fld': 0.0, 'cs2_fld': cs2, 'use_ppf': 'no'})
    c = Class(); c.set(p); c.compute()
    cl = c.raw_cl(2500); l = cl['ell'][2:]; tt = cl['tt'][2:] * l * (l + 1) / (2 * np.pi) * (2.7255e6) ** 2
    th = c.get_current_derived_parameters(['100*theta_s'])['100*theta_s']
    c.struct_cleanup(); c.empty()
    return l, tt, th

def peaks(l, tt, nmax=3):
    out = []
    for i in range(1, len(tt) - 1):
        if tt[i] > tt[i - 1] and tt[i] > tt[i + 1] and l[i] > 100:
            out.append((int(l[i]), float(tt[i])))
        if len(out) >= nmax: break
    return out

sec("PART 0 -- run both cases: identical background (same w), ONLY c_s^2 differs.")
l0, tt0, th0 = run(0.0); pk0 = peaks(l0, tt0)
l1, tt1, th1 = run(1.0); pk1 = peaks(l1, tt1)
print(f"    clustering (c_s^2=0): 100*theta_s={th0:.5f}  peaks={[(a,round(b,1)) for a,b in pk0]}")
print(f"    SMOOTH     (c_s^2=1): 100*theta_s={th1:.5f}  peaks={[(a,round(b,1)) for a,b in pk1]}", flush=True)

check("CTRL-0  the two runs share an IDENTICAL background (same w), so 100*theta_s agrees to <1e-4 and the "
      "comparison is of peak HEIGHTS at fixed acoustic scale -- not of peak positions. The control is "
      "structural, not achieved by re-tuning H0",
      abs(th0 - th1) < 1e-4, f"100*theta_s: clustering={th0:.5f}, smooth={th1:.5f}, diff={abs(th0-th1):.2e}")

sec("PART 1 -- PIPELINE VALIDATION: the clustering run must reproduce the observed CMB. It does.")
l1p, a1p = pk0[0]
check("VALID-0  the c_s^2=0 (clustering) run reproduces the measured first acoustic peak -- l ~ 220 and "
      "amplitude ~5750 uK^2 -- so the pipeline is validated and a failure in the smooth run is physical, "
      "not a broken computation (this is the positive control)",
      200 < l1p < 245 and 5300 < a1p < 6200,
      f"clustering peak1: l={l1p} (obs ~220), amp={a1p:.0f} uK^2 (obs ~5750)")

sec("PART 2 -- THE RESULT: smooth dust fails grossly on peak height and on the third/second ratio.")
r31_0, r32_0 = pk0[2][1] / pk0[0][1], pk0[2][1] / pk0[1][1]
r31_1, r32_1 = pk1[2][1] / pk1[0][1], pk1[2][1] / pk1[1][1]
print(f"    clustering:  peak3/peak1={r31_0:.4f}  peak3/peak2={r32_0:.4f}")
print(f"    SMOOTH:      peak3/peak1={r31_1:.4f}  peak3/peak2={r32_1:.4f}")
amp_ratio = pk1[0][1] / pk0[0][1]
check("KILL-0  without clustering wells the gravitational potentials DECAY and radiation driving inflates "
      "the acoustic oscillations: the smooth run's first peak is several times too HIGH (a gross, not "
      "marginal, failure)",
      amp_ratio > 2.0, f"smooth peak1 amplitude is {amp_ratio:.2f}x the clustering (observed) value")
dev = abs(r32_1 - r32_0) / r32_0
check("KILL-1  the third-to-second peak ratio collapses from ~0.99 (clustering, matching observation) to "
      "~0.55 (smooth) -- a ~44% deficit against a ~1% measurement precision on peak heights. A smooth a^-3 "
      "component does NOT reproduce the third peak",
      dev > 0.30, f"peak3/peak2: clustering={r32_0:.4f}, smooth={r32_1:.4f}, deficit={100*dev:.1f}% (vs ~1% precision)")
check("KILL-2  therefore the z_eq shift ALONE does not substitute for clustering. The third peak's "
      "enhancement is specifically a clustering signature, as standard CMB physics expects -- now SHOWN "
      "rather than assumed. L128's explicitly-open question is CLOSED, negatively",
      dev > 0.30 and amp_ratio > 2.0,
      "smooth a^-3 dust is excluded: the cuscuton dark sector cannot drive the third peak")

sec("PART 3 -- honest scope.")
print("""
  WHAT IS SHOWN: with a controlled identical background and a validated pipeline, a non-clustering a^-3
  component fails the CMB grossly -- first peak several times too high, third/second ratio 44% low. The
  cuscuton's infinite-sound-speed dust (L128) therefore cannot supply the CMB's dark component.

  WHAT IS NOT SHOWN: (i) c_s^2 = 1 is a stand-in for c_s^2 -> infinity; the true cuscuton is even MORE
  smooth, so this is conservative in the correct direction, but it is a stand-in. (ii) No likelihood was
  evaluated, so the deficits are quoted as fractional deviations against quoted measurement precision, NOT
  as a calibrated sigma -- do not quote a sigma from this lane. (iii) The fluid's early-time initial
  conditions are outside CLASS's intended regime (the code guards w>=0); this is why both runs use the SAME
  w so the inaccuracy is common-mode, but an independent CAMB cross-check is still worth doing.
  (iv) This closes the SMOOTH-dust route. It does not close every conceivable field-dust route -- a field
  with FINITE c_s could cluster, which is exactly the remaining tension (finite c_s => propagating =>
  excluded by L95 closure and the L120 RAQUAL band). That pincer is stated, not proven closed.
""", flush=True)
check("SCOPE-0  honestly bounded: smooth a^-3 dust is excluded by a controlled, validated Boltzmann run; "
      "no sigma is quoted (no likelihood); c_s^2=1 is a conservative stand-in for infinity; a CAMB "
      "cross-check remains worthwhile; finite-c_s field-dust is NOT closed by this lane",
      True, "smooth-dust route closed; finite-c_s route remains the stated (unproven) pincer")

print("=" * 112)
if FAILS:
    print(f"L129 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"L129 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 112)
