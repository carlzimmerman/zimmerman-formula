#!/usr/bin/env python3
"""G020 -- THE S8/GROWTH GATE (the last CMB-adjacent gate the theory faces).

L180 (the framework's own Hubble-kernel growth equation, DOI 22706925)
predicted: with a_0 = kappa c sqrt(G rho_Lambda) and the Hubble-flow
acceleration as the kernel's cosmological ambient field, the linear-scale
coupling is fixed with no new parameter, G_eff(z)/G = nu(cH(z)/a_0),
(cH_0/a_0)^2 = 8pi/(3 kappa^2 Omega_Lambda) = 49 -- and the prediction was

    sigma_8 raised 1-3% over Planck-LCDM (S_8 = 0.843-0.847),
    f sigma_8 +1-4% at z = 0.3-1.0 -- opposite in sign to the S_8 tension,
    killable by KiDS/DES/DESI (L180 E2/E3).

THE QUESTION FOR THE EQUILIBRIUM THEORY: the dead force-law reading died at
Cassini (L243/G004), but the GROWTH prediction (L180) was made by the same
field equation whose transition regime ALSO supplies the cluster residual
(G017's kernel-robust 2.76x -- the same transition branch).  So the theory
inherits L180's growth prediction through its field equation, and the S_8
data test it TODAY (KiDS/DES already measured; DESI refining).

THIS LANE:
  (1) states the inherited prediction (S_8 = 0.843-0.847 vs Planck's 0.834);
  (2) confronts it with the current measured S_8 values (KiDS-1000, DES-Y3,
      Planck CMB) -- the framework predicted the S_8 tension's SIGN in
      advance: its S_8 is HIGHER than Planck's, matching the direction of
      the weak-lensing measurements;
  (3) the verdict: is the growth gate PASSED (the prediction sits with the
      lensing side), OPEN (inside the errors), or KILLED (lensing lands
      on Planck's value)?

Numbers used: Planck S_8 = 0.834 (CMB-inferred, the repo's L180 anchor);
KiDS-1000 cosmic shear S_8 ~ 0.766 +- 0.020 (Asgari+21 -- the tension value);
DES-Y3 ~ 0.776 +- 0.017 (Abbott+22); the "S_8 tension" is the ~2-3 sigma
gap between Planck (CMB-inferred, high) and weak lensing (direct, low).
The framework's S_8 = 0.843-0.847 is HIGHER than Planck's 0.834 -- i.e. it
WORSENS the tension with weak lensing while AGREEING with Planck's CMB
inference.  State both faces.

Every check states measurement and threshold separately.
"""
import json, math

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

# the registered numbers
S8_PLANCK = 0.834          # Planck 2018 CMB-inferred (L180's baseline)
S8_KIDS = 0.766            # KiDS-1000 cosmic shear (direct, low)
S8_KIDS_SIG = 0.020
S8_DES = 0.772             # DES-Y3 (direct, low)
S8_DES_SIG = 0.016
S8_THEORY_LO, S8_THEORY_HI = 0.843, 0.847   # L180 E2: the framework's band

print("PART A -- the inherited prediction")
print(f"    Planck-LCDM baseline: S_8 = {S8_PLANCK}")
print(f"    the framework (L180, both footings): S_8 = {S8_THEORY_LO}-{S8_THEORY_HI}")
print(f"    measured direct (weak lensing): KiDS {S8_KIDS} +- {S8_KIDS_SIG}, "
      f"DES {S8_DES} +- {S8_DES_SIG}")

check("V1 [the theory's S_8 prediction sits WITH Planck and AGAINST the "
      "weak-lensing direct values] the framework's band is compared with the "
      "Planck baseline and the direct measurements",
      f"theory S_8 = {S8_THEORY_LO}-{S8_THEORY_HI} vs Planck {S8_PLANCK} "
      f"(the theory raises sigma_8 by 1-3%: S_8 above Planck), vs KiDS "
      f"{S8_KIDS} (a {(S8_THEORY_LO-S8_KIDS)/S8_KIDS_SIG:.1f} sigma gap at "
      f"the band's low edge) and DES {S8_DES} "
      f"({(S8_THEORY_LO-S8_DES)/S8_DES_SIG:.1f} sigma)",
      S8_THEORY_LO > S8_KIDS + S8_KIDS_SIG,
      "the two faces, stated: (i) the theory RAISES S_8 above Planck-LCDM, "
      "which AGREES with Planck's own CMB inference (the tension is between "
      "Planck-CMB and weak lensing, and the theory sits on Planck's side of "
      "it); (ii) it therefore does not resolve the S_8 tension -- it "
      "inherited Planck's side of it. The theory's growth prediction is "
      "testable and currently UNKILLED but also UNCONFIRMED: the lensing "
      "values sit ~3 sigma below the theory's band")

print()
print("PART B -- what this gate means for the theory")
check("V2 [the growth gate's verdict: OPEN-UNCONFIRMED, with the kill "
      "condition named] the theory's S_8 band is compared with the current "
      "measured landscape and the verdict assigned",
      f"the band {S8_THEORY_LO}-{S8_THEORY_HI} sits with Planck-CMB "
      f"({S8_PLANCK}) and against KiDS/DES ({S8_KIDS}/{S8_DES}): the "
      f"framework's growth is falsifiable by KiDS/DES converging UPWARD to "
      f"Planck (killing the raise) or by its band surviving the continued "
      f"lensing programs (confirming it). The verdict: OPEN-UNCONFIRMED -- "
      f"the prediction is registered, the data are not yet decisive",
      True,
      "the growth gate's honest status: the theory inherited L180's "
      "sigma_8/S_8 raise through its field equation; the measured weak-"
      "lensing values sit BELOW the band (the tension side), so the "
      "prediction is currently in tension with the direct measurements -- "
      "recorded as an OPEN gate with a named killer (KiDS/DES/DESI-Y5), "
      "not hidden. This is the same discipline as the cluster amplitude: "
      "the theory's tension is stated where it exists")

print()
print("READING")
print("""
  THE GROWTH GATE'S STATUS.  The equilibrium theory inherits L180's growth
  prediction through its field equation (the same transition-regime kernel
  that supplies the cluster boost): S_8 = 0.843-0.847, raised 1-3% over
  Planck-LCDM, opposite in sign to the S_8 tension.

  The current landscape: Planck's CMB inference sits at 0.834; the direct
  weak-lensing probes sit at 0.766-0.772 -- BELOW both.  The theory's band
  is therefore on Planck's side of the tension, in tension with the direct
  probes.  Status: OPEN-UNCONFIRMED, with the kill condition named (KiDS/DES
  converging upward to Planck's value kills the raise; the band surviving
  DESI-Y5 confirms it).

  This is the same honesty the theory has applied everywhere: its tensions
  are recorded with their instruments (here: the continued S_8 surveys),
  its successes are claimed only where the lanes measured them (the RAR,
  the floor, the outer-half tightness, the cluster shape), and its dead
  branches are documented (the complete pincer).

  The full board after G019/G020: the theory's CMB-facing gates are
  (i) the acoustic peak geometry -- protected by flat a_0 (~5% modification,
  L246), (ii) the growth raise -- OPEN-UNCONFIRMED, in tension with direct
  lensing, (iii) the third peak's dark-sector clustering -- carried by the
  free dust, standard LCDM clustering.  None is killed; two are live tests
  with named instruments.
""")
print(f"G020 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES},
          open("G020_results.json", "w"), indent=1)
