#!/usr/bin/env python3
"""
SW03_dSph_eta_sequence.py -- the satellite eta-sequence: second determination of eta_c
(2026-09-17, third swing of the glm_moe lane)

THE IDEA. The classical dSphs sit at Galactocentric distances D = 66--250 kpc, where the
Galactic field is eta(D) = v_c^2/(D a0) ~ 0.05--0.23 -- straddling the declared eta_c
(0.203 canonical / 0.169 alt, SW01b). So their dispersions are a SECOND, INDEPENDENT
determination of eta_c against the Oort-limit value: not tunable -- Oort fixes eta_c from
above, the dwarfs test it.

PRE-REGISTERED GATES (stated before the numbers; M/L_V band [1.5, 3], v_c band [180, 230]
km/s at 60--260 kpc, Sgr excluded as tidally disrupted):

  KILL-A  median |log10 sigma_pred/sigma_obs| > 0.3 dex across the eight classical dSphs at
          the frozen eta_c -> the dwarf channel fails at the declared constant.
  KILL-B  the eta_c implied by the objects that DEMAND suppression (0 < S_req < 1) exceeds
          3x the Oort eta_c -> the dwarfs want LESS suppression than the Oort budget allows
          -> no single eta_c exists -> S(eta) is dead -> KILLED (the two-sided squeeze
          closes; this is the answer-B-shaped statement).
  NOT-DISTINCTIVE  |median residual(SW01-B) - median residual(S = 1)| < 0.1 dex AND the
          implied-eta_c direction is consistent -> the dSph data cannot distinguish this
          class's suppression from no suppression at all; the radial sigma(D) trend is
          MOND-generic EFE. Status stays OPEN, no new prediction claimed (grok rule iii).

HONESTY FRAME (stated up front):
  * The radial trend "inner satellites more suppressed, outer nearly full MOND" is
    STANDARD EFE (eta ~ 1/D), not distinctive. The class-specific content is
    direction-blindness (gamma_v = 1.0010; P2 = 0) and the Oort-squeeze on eta_c.
  * STANDING COST to beat (kimik3 PREDICTIONS.md l.88): "both EFE laws UNDERPREDICT
    classical dSph dispersions (median -0.13 dex at M/L_V = 2 isolated, worse with EFE)".
    This lane must reproduce that number and state it against.
  * Estimator = the record's own (L263 E): deep-MOND virial sigma^4 = (4/81) G M_b a0_eff,
    with the Wolf+2010 estimator (M_dyn = 3 sigma^2 r_h / G) on the observed side -- the
    SAME estimator both sides, so the virial constant cancels in S_req. Per-object Jeans
    (L263 E2) remains the registered confirmatory step; this lane is the screening.
  * eta_c is NOT tuned to the dwarfs. The dwarfs measure it; disagreement = kill.

DATA (embedded, provenance cited): sigma_los from Walker et al. 2009 (The Astronomical
Journal 137, 3100, Table 1); D, r_h(pc), L_V from McConnachie 2012 (AJ 144, 4) as used by
Walker+09. Standard published values, < 1 kB.

MUTATE=1 sets eta_c = 0.5 (5x the Oort value): the Oort-consistency check must FAIL
(rho_dark = 5.8x budget) -- the hinge, mirroring the SW01-A kill.
"""
import json, math, os
import numpy as np
import sympy as sp

MUTATE = os.environ.get("MUTATE", "0") == "1"

A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
ETA_C = {"canonical": 0.2034, "alt": 0.1688}     # declared (SW01b B2), NOT tuned here
ETA_SUN = {"canonical": 2.292, "alt": 1.902}     # SW01b B1
OORT_BUDGET, RHO_PH_UNC = 0.015, 1.92            # Msun/pc^3 (L263 C1)
VC = 200e3                                       # m/s at 60--260 kpc, band [180, 230] km/s
VC_BAND = (180e3, 230e3)
ML_BAND = (1.5, 3.0)                             # M/L_V band, old metal-poor populations
G_NEW, M_SUN, PC = 6.674e-11, 1.989e30, 3.0857e16   # G in SI; 1 pc = 3.0857e16 m
G_PC = 4.302e-3                                  # G in pc Msun^-1 (km/s)^2 -- for the Wolf check

# name, D[kpc], r_h[pc], sigma_los[km/s], L_V[Lsun]  (Walker+09; McConnachie 2012)
DSph = [("Draco", 82, 220, 9.1, 2.6e5), ("Ursa Minor", 66, 340, 9.5, 2.6e5),
        ("Sculptor", 79, 280, 9.2, 1.4e6), ("Sextans", 86, 700, 7.9, 5.0e5),
        ("Carina", 101, 290, 6.6, 4.4e5), ("Fornax", 138, 710, 11.7, 1.55e7),
        ("Leo II", 205, 180, 6.6, 8.7e5), ("Leo I", 250, 250, 9.2, 5.5e6)]

checks = []
def check(name, measured, ok, reading=""):
    checks.append({"name": name, "ok": bool(ok), "measured": str(measured), "reading": reading})
    print("  [%s] %s\n           (%s%s)" % ("PASS" if ok else "FAIL", name, measured,
                                           ("; " + reading) if reading else ""))

def nu_rar(y):
    return 1.0 / (1.0 - math.exp(-math.sqrt(y)))

def S_env(eta, eta_c):
    return 1.0 / (1.0 + (eta / eta_c) ** 2)

def median(v):
    s = sorted(v); n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])

print("=" * 72)
print("SW03 -- the satellite eta-sequence: second determination of eta_c%s"
      % ("  [MUTATE: eta_c = 0.5, hinge broken]" if MUTATE else ""))
print("=" * 72)
eta_c_use = {f: (0.5 if MUTATE else ETA_C[f]) for f in A0}

# ---------------------------------------------------------------- A. controls
print("\nA. controls (the record's own numbers, reproduced)")
G_, M_, a0_, r_ = sp.symbols("G M a0 r", positive=True)
rM = sp.sqrt(G_ * M_ / a0_)
check("A1 sympy, L263 B1: M_dyn(<r) = M r / r_M for the deep-MOND force",
      "M_dyn/M - r/r_M = %s" % sp.simplify((sp.sqrt(G_ * M_ * a0_) / r_ * r_ ** 2 / G_) / M_
                                            - r_ / rM),
      sp.simplify((sp.sqrt(G_ * M_ * a0_) / r_ * r_ ** 2 / G_) / M_ - r_ / rM) == 0,
      "threshold: exact")
check("A2 control: nu_RAR(2.5) - 1 = 0.259 (L264)", "computed %.4f" % (nu_rar(2.5) - 1.0),
      abs(nu_rar(2.5) - 1.0 - 0.259) < 0.002, "threshold |diff| < 0.002")
check("A3 control: eta_sun = 2.292 / 1.902 (SW01b B1)",
      "v_c(233 km/s)^2/R_0(8.2 kpc)/a0: %.3f / %.3f" % (233e3 ** 2 / (8.2 * 3.0857e19) / A0["canonical"],
                                                        233e3 ** 2 / (8.2 * 3.0857e19) / A0["alt"]),
      abs(233e3 ** 2 / (8.2 * 3.0857e19) / A0["canonical"] - 2.292) < 0.01,
      "threshold |diff| < 0.01 -- the same numbers SW01b computed (8.2 kpc = 8.2 x 3.0857e19 m)")
# estimator anchor: Fornax isolated, M/L = 2 -- the famous MOND-dSph anchor
Mb_fornax = 2.0 * 1.55e7 * M_SUN
sig_fornax = (4.0 / 81.0 * G_NEW * Mb_fornax * A0["canonical"]) ** 0.25 / 1e3
check("A4 estimator anchor: Fornax isolated (M/L=2) sigma = %.2f km/s vs observed 11.7"
      % sig_fornax,
      "|residual| = %.3f dex" % abs(math.log10(sig_fornax / 11.7)),
      abs(math.log10(sig_fornax / 11.7)) < 0.05,
      "abort-threshold 0.05 dex: the L263-E estimator must reproduce the famous anchor")

# ---------------------------------------------------------------- B. per-object
print("\nB. per-object prediction at the frozen eta_c (screening; per-object Jeans is the")
print("   registered confirmatory step per L263 E2 -- the same estimator sits on both sides,")
print("   so the virial constant cancels in S_req)")
rows = []
for name, D_kpc, rh_pc, sig_obs, L in DSph:
    eta = {f: VC ** 2 / (D_kpc * 3.0857e19 * A0[f]) for f in A0}
    eta_band = (min(VC_BAND) ** 2 / (D_kpc * 3.0857e19 * A0["canonical"]),
                max(VC_BAND) ** 2 / (D_kpc * 3.0857e19 * A0["canonical"]))
    S_p = {f: S_env(eta[f], eta_c_use[f]) for f in A0}
    rh, sig = rh_pc * PC, sig_obs * 1e3
    Mb_c = 2.0 * L * M_SUN                                   # central M/L = 2
    x = G_NEW * Mb_c / (rh ** 2 * A0["canonical"])
    nu = nu_rar(x)
    D_pred = 1.0 + S_p["canonical"] * (nu - 1.0)
    a0_eff = D_pred ** 2 * x * A0["canonical"]
    sig_pred = (4.0 / 81.0 * G_NEW * Mb_c * a0_eff) ** 0.25 / 1e3
    # observed side: Wolf+2010, per M/L edge (M_dyn_obs is M/L-independent)
    Mdyn_obs = 3.0 * sig ** 2 * rh / G_NEW
    D_obs_band = tuple(Mdyn_obs / (ml * L * M_SUN) for ml in ML_BAND)
    Sreq_band = tuple((d - 1.0) / (nu - 1.0) for d in D_obs_band)
    # implied eta_c: measurable only where the object DEMANDS suppression (0 < S_req < 1)
    etac_inv = None
    if max(Sreq_band) < 1.0 and min(Sreq_band) > 0:
        etac_inv = eta["canonical"] / math.sqrt(1.0 / max(Sreq_band) - 1.0)
    resid = math.log10(sig_pred / sig_obs)
    rows.append(dict(name=name, D=D_kpc, eta=eta["canonical"], eta_alt=eta["alt"],
                     eta_band=eta_band, S=S_p["canonical"], S_alt=S_p["alt"], x=x, nu=nu,
                     D_pred=D_pred, sig_pred=sig_pred, sig_obs=sig_obs, resid=resid,
                     Sreq=Sreq_band, etac_inv=etac_inv, deep_ok=x < 0.5))
    print("  %-12s D=%3.0f kpc eta=%6.3f S=%5.3f x=%8.5f nu=%6.2f "
          % (name, D_kpc, eta["canonical"], S_p["canonical"], x, nu))
    print("               sigma_pred=%5.2f vs %5.2f km/s -> %+.3f dex | "
          "S_req=[%.2f,%.2f] eta_c_inv=%s"
          % (sig_pred, sig_obs, resid, Sreq_band[0], Sreq_band[1],
             ("%.3f" % etac_inv) if etac_inv else "n/a (no suppression demanded)"))

# ---------------------------------------------------------------- C. gates
print("\nC. the pre-registered gates")
resid_med = median([r["resid"] for r in rows])
check("C1[KILL-A] median residual across the eight dSphs (frozen eta_c, M/L=2)",
      "median = %+.3f dex vs threshold 0.3" % resid_med,
      abs(resid_med) <= 0.3,
      "predicted vs Walker+09 observed; M/L band moves sigma_pred by only +-{:.2f} dex"
      .format(max(abs(math.log10((rows[0]["sig_pred"] * (ML_BAND[1] / 2.0) ** 0.25)
                                  / rows[0]["sig_obs"]) - rows[0]["resid"]) for r in rows[:1])))

clean = [r for r in rows if r["etac_inv"] is not None]
nosup = [r["name"] for r in rows if r["etac_inv"] is None]
if clean:
    etac_med = median([r["etac_inv"] for r in clean])
    oort_etac = ETA_C["canonical"]
    check("C2[KILL-B] eta_c implied by the suppression-demanding objects (%s)"
          % ", ".join(r["name"] for r in clean),
          "median implied eta_c = %.3f vs Oort eta_c = %.3f (ratio %.2f); FAIL if > 3x"
          % (etac_med, oort_etac, etac_med / oort_etac),
          etac_med <= 3.0 * oort_etac,
          "the two-sided squeeze: Oort demands eta_c <= 0.203; the dwarfs' implied value "
          "must not EXCEED it by > 3x (more suppression than Oort needs is safe, less is dead)")
    # C3a: the DECLARED eta_c must stay Oort-consistent -- this is the gate the mutation breaks
    S_decl = S_env(ETA_SUN["canonical"], eta_c_use["canonical"])
    rho_decl = RHO_PH_UNC * S_decl
    check("C3a[HINGE] Oort consistency of the DECLARED eta_c",
          "S(eta_sun) = %.4f -> rho_dark = %.4f Msun/pc^3 (%.1fx budget)"
          % (S_decl, rho_decl, rho_decl / OORT_BUDGET),
          rho_decl / OORT_BUDGET < 3.0,
          "under MUTATE (eta_c = 0.5) this FAILS: 5.8x budget -- the hinge, mirroring the "
          "SW01-A kill; the implied-eta_c check below is mutation-invariant BY DESIGN "
          "(it is data-side)")
    # C3b: the IMPLIED eta_c (data-side) must keep Oort and the LSS gate alive
    S_tight = S_env(ETA_SUN["canonical"], etac_med)
    rho_tight = RHO_PH_UNC * S_tight
    eta_lss = 400e3 * 67.4e3 / 3.0857e22 / A0["canonical"]
    check("C3b Oort+LSS consistency at the implied eta_c",
          "S(eta_sun) = %.4f -> rho_dark = %.4f Msun/pc^3 (%.1fx budget); "
          "S(eta_LSS) = %.4f >= 0.9"
          % (S_tight, rho_tight, rho_tight / OORT_BUDGET, S_env(eta_lss, etac_med)),
          rho_tight / OORT_BUDGET < 3.0 and S_env(eta_lss, etac_med) >= 0.9,
          "the tightened eta_c must keep BOTH standing gates alive (SW01b E1/F)")
else:
    etac_med = None
    check("C2[KILL-B] no object demanded suppression", "eta_c unmeasurable from this sample",
          False, "all eight objects have S_req >= 1: the class predicts suppression the "
                 "dwarfs do not show -> KILL-B fires trivially")
check("C4 objects with S_req >= 1 (the MOND-wide dwarf residual, kimik3's standing cost)",
      "%d of 8: %s" % (len(nosup), ", ".join(nosup)),
      True if nosup else False,
      "these carry the pre-existing MOND-wide underprediction (kimik3: median -0.13 dex at "
      "M/L_V=2 isolated) and cannot measure suppression; excluded from the squeeze, counted "
      "in the residuals")

# the NOT-DISTINCTIVE check: isolated (S = 1) residuals for the same objects
resid_iso = []
for r in rows:
    Mb_c = 2.0 * [L for n, D, rh, s, L in DSph if n == r["name"]][0] * M_SUN
    sig_iso = (4.0 / 81.0 * G_NEW * Mb_c * A0["canonical"]) ** 0.25 / 1e3
    resid_iso.append(math.log10(sig_iso / r["sig_obs"]))
med_iso = median(resid_iso)
delta = abs(resid_med - med_iso)
check("C5[distinctiveness] median residual, isolated S=1: %+.3f dex; SW01-B: %+.3f dex; "
      "delta = %.3f dex (DISTINCTIVE required for any new prediction)"
      % (med_iso, resid_med, delta),
      "delta >= 0.1 dex required; below it the dSph data cannot distinguish this class's "
      "suppression from none at all (the radial sigma(D) trend is MOND-generic EFE)",
      delta >= 0.1,
      "if NOT DISTINCTIVE: status stays OPEN, no new prediction claimed (grok rule iii); "
      "distinctive content remains direction-blindness (gamma_v = 1.0010) and the squeeze")

# ---------------------------------------------------------------- verdict
n_pass = sum(1 for c in checks if c["ok"])
print("\nSW03 COMPLETE: %d/%d checks PASS." % (n_pass, len(checks)))
c1 = next(c for c in checks if c["name"].startswith("C1"))
c2 = next((c for c in checks if c["name"].startswith("C2")), None)
c3a = next((c for c in checks if c["name"].startswith("C3a")), None)
c5 = next(c for c in checks if c["name"].startswith("C5"))
verdict = ("SW03 satellite eta-sequence: median residual %+.3f dex (gate A: %s); implied "
           "eta_c from the suppression-demanding subset = %s (gate B: %s); NOT-DISTINCTIVE "
           "gate: delta vs isolated = %.3f dex -> %s. Standing cost reproduced: isolated "
           "median %+.3f dex vs kimik3's -0.13 dex. eta_c stays Oort-declared; the dwarfs "
           "tighten it from above if the subset is trusted; per-object Jeans (L263 E2) is "
           "the registered confirmatory step. Dated falsifier unchanged: gamma_v(DR4) = "
           "1.0010, 2026-12-02."
) % (resid_med, "PASS" if c1["ok"] else "FAIL",
     ("%.3f" % etac_med) if etac_med else "n/a", "PASS" if (c2 and c2["ok"]) else "FAIL",
     delta, "NOT DISTINCTIVE (OPEN, no new prediction)" if not c5["ok"] else "DISTINCTIVE",
     med_iso)
print(verdict)

out = {"lane": "SW03_dSph_eta_sequence", "mutate": MUTATE,
       "n_pass": n_pass, "n_total": len(checks), "checks": checks, "verdict": verdict,
       "rows": rows,
       "constants": {"a0": A0, "eta_c": ETA_C, "eta_c_used": eta_c_use,
                     "median_residual": resid_med, "median_residual_isolated": med_iso,
                     "eta_c_implied_median": etac_med,
                     "no_suppression_objects": nosup}}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "SW03_dSph_eta_sequence.json"), "w") as f:
    json.dump(out, f, indent=1)
print("\n(json written: SW03_dSph_eta_sequence.json)")
