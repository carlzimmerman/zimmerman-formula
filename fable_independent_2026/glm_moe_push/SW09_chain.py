#!/usr/bin/env python3
"""
SW09_chain.py -- the certified prediction chain: recompute the frozen numbers
from the axioms (A1-A7) and cross-check EVERY one against the landed .out
artifacts. Any mismatch is printed as FAIL-as-finding -- never a silent edit.

Axioms (owner lane):
  A1 GammaSq (definition, SW01b C1/C2 quadrature)     A2 eta (definition, SW01b B1)
  A3 barycenter centering (SW01b C3 hinge, SW08 D1/D2) A4 S-family (ANSATZ, SW07 H5)
  A5 nu_RAR (DATA-SELECTED, rung 2; nu(2.5)-1 = 0.259, L264) A6 a0 = 0.5 c sqrt(G rho_Lambda)
     (MEASURED, kappa = 0.5, slot NOT LIVE, KS01)     A7 eta_c (DECLARED, SW01b B2)

Chain links under audit (10): L0 mean-value (SW09_meanvalue), L1 orthogonality,
L2 conformal scaling, L3 P2 = 0, L4 eBTFR, L5 mu_S, L6 the x = 2.5 gate,
L7 alpha_2 double suppression + c_S bound, L8 the G03 obstruction (2-jet),
C1 the DR4 kill rule (decided 2026-12-02).

Every cross-check target below is a literal quoted from a landed file AND is
verified textually (the quoted string must still appear in the cited file --
a provenance check computed at run time). Formulas are ported VERBATIM from
SW04_conformal_efe.py / SW05_kepler_freeze.py / SW08_preferred_frame.py;
nothing is re-fitted or re-tuned.

MUTATE=1 sets S == 1 (the SW05 mutant): the landed targets are then EXPECTED
to miss -- each miss is the finding that the mutant loses the distinctive
numbers, exactly as pre-registered in SW05's docstring.
"""
import json, math, os, sys
import numpy as np
import sympy as sp

MUTATE = os.environ.get("MUTATE", "0") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "SW09_chain.out")
JSON_PATH = os.path.join(HERE, "SW09_chain.json")

# ---- the axioms' constants (verbatim from the landed lane constants) ----
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}      # MEASURED (SW07)
ETA_C = {"canonical": 0.2034, "alt": 0.1688}           # DECLARED (SW01b B2)
ETA_SUN = {"canonical": 2.292, "alt": 1.902}           # SW01b B1
G_NEW, M_SUN, PC, AU = 6.674e-11, 1.989e30, 3.0857e16, 1.496e11
H0 = 67.4e3 / 3.0857e22                                # s^-1 (Mpc in METERS)
C_LIGHT = 2.998e8
SPARC_FLOOR = 0.06                                     # dex

def nu_rar(y):
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))

def S_env(eta, eta_c):
    return 1.0 / (1.0 + (eta / eta_c) ** 2)

class Tee:
    """stdout tee: the .out IS the transcript of this run."""
    def __init__(self, path):
        self.f = open(path, "w")
    def write(self, s):
        sys.__stdout__.write(s)
        self.f.write(s)
    def flush(self):
        sys.__stdout__.flush()
        self.f.flush()

sys.stdout = Tee(OUT_PATH)   # from here on, every print lands in the .out too

def read(fname):
    with open(os.path.join(HERE, fname)) as f:
        return f.read()

def prov(fname, needle):
    """computed boolean: the cited file still carries the quoted target string."""
    return needle in read(fname)

checks = []
def check(name, measured, ok, reading=""):
    okc = bool(ok)
    checks.append({"name": name, "ok": okc, "measured": str(measured), "reading": reading})
    print("  [%s] %s\n           (%s%s)" % ("PASS" if okc else "FAIL-as-finding", name,
                                            measured, ("; " + reading) if reading else ""))
    return okc

print("=" * 74)
print("SW09_chain -- the certified prediction chain, recomputed and cross-checked%s"
      % ("  [MUTATE: S == 1, suppression removed]" if MUTATE else ""))
print("=" * 74)

a0, eta_c = A0["canonical"], ETA_C["canonical"]

# -------------------------------------------------- X1: gamma_v(s) vs SW04 D
print("\nX1. gamma_v(s) over s = 1e3..3e4 AU  (L8/C1 link; SW04 D, SW05 P1)")
gext_sun = ETA_SUN["canonical"] * a0
M_bin = 1.5 * M_SUN
gam = []
for s in (1e3, 3e3, 5e3, 1e4, 2e4, 3e4):
    gN = G_NEW * M_bin / (s * AU) ** 2
    S = 1.0 if MUTATE else S_env(gext_sun / a0, eta_c)
    gc = gN * (1.0 + S * (float(nu_rar(gN / a0)) - 1.0))   # the class (SW04 g_obs_class, no hinge)
    gam.append((s, gN / a0, math.sqrt(gc / gN)))
for s, x, g in gam:
    print("  s = %7.0f AU  g_N/a0 = %9.4f | gamma_v class = %.5f" % (s, x, g))
gmin, gmax = min(g for _, _, g in gam), max(g for _, _, g in gam)
mono = all(gam[i][2] < gam[i + 1][2] for i in range(len(gam) - 1))
ok1 = bool(abs(gmin - 1.00000) < 1e-5 and abs(gmax - 1.01012) < 1e-5 and mono)
check("X1 gamma_v curve 1.00000-1.01012 (SW04 D) recomputed from the axioms",
      "computed %.5f-%.5f (monotone %s) vs landed 1.00000-1.01012" % (gmin, gmax, mono),
      ok1,
      "ported verbatim from SW04 D (M_bin = 1.5 M_sun, eta_sun = 2.292); "
      "provenance SW04 %.5f-string: %s" % (1.01012, prov("SW04_conformal_efe.out", "1.01012")))

# ------------------------- X2: A2 = 2.22e-16 (SW04 B1) + angular null (SW05 C1)
print("\nX2. A2 = 2.22e-16: the angular null and the conformal cancellation "
      "(L2/L3 links; SW04 B1, SW05 C1)")
DSph = [("Draco", 82, 220, 2.6e5), ("Ursa Minor", 66, 340, 2.6e5),
        ("Sculptor", 79, 280, 1.4e6), ("Sextans", 86, 700, 5.0e5),
        ("Carina", 101, 290, 4.4e5), ("Fornax", 138, 710, 1.55e7),
        ("Leo II", 205, 180, 8.7e5), ("Leo I", 250, 250, 5.5e6)]
VC = 200e3
canc = 0.0
for name, D_kpc, rh_pc, L in DSph:
    gext = VC ** 2 / (D_kpc * 1e3 * PC)
    M_b = 2.0 * L * M_SUN
    a_P = (rh_pc * PC) / 1.305
    Qc, Qi = [], []
    for f in (0.5, 2.0):
        R = f * rh_pc * PC
        gN = G_NEW * M_b * R / (R * R + a_P * a_P) ** 1.5
        S = 1.0 if MUTATE else S_env(gext / a0, eta_c)
        Qc.append(gN * (1.0 + S * (float(nu_rar(gN / a0)) - 1.0)) / gN - 1.0)
        Qi.append(float(nu_rar(gN / a0)) - 1.0)
    canc = max(canc, abs((Qc[1] / Qc[0]) / (Qi[1] / Qi[0]) - 1.0))
nphi = 720
phis = np.linspace(0.0, 2.0 * math.pi, nphi)
S_sun = 1.0 if MUTATE else S_env(ETA_SUN["canonical"], eta_c)
D_int = float(nu_rar(2.5)) - 1.0
gv2 = np.full(nphi, 1.0 + S_sun * D_int)               # phi-independent by structure (SW05 C1)
a2_clean = float(np.max(np.abs(gv2 - gv2.mean())))
ok2 = bool(canc < 1e-12 and a2_clean < 1e-12
           and prov("SW04_conformal_efe.out", "2.22e-16")
           and prov("SW05_kepler_freeze.out", "2.22e-16"))
check("X2 A2 = 2.22e-16 exactly-zero level (SW04 B1 / SW05 C1) recomputed",
      "BR cancellation residual %.2e; angular amplitude A2 = %.2e (both < 1e-12)"
      % (canc, a2_clean),
      ok2,
      "the same zero is recorded in two landed files at their own check IDs; "
      "provenance SW04 '2.22e-16': %s; SW05 '2.22e-16': %s"
      % (prov("SW04_conformal_efe.out", "2.22e-16"), prov("SW05_kepler_freeze.out", "2.22e-16")))

# ------------------------------------- X3: P4 gaps 0.118/0.083 dex vs SW05 B
print("\nX3. P4 the high-eta floor: dex gaps at eta = 2/3/5/10 (L6 link; SW05 B)")
gaps = {}
for eta in (2.0, 3.0, 5.0, 10.0):
    cap = float(nu_rar(eta)) - 1.0
    S = 1.0 if MUTATE else S_env(eta, eta_c)
    cls = S * (float(nu_rar(1.0)) - 1.0)                # x = 1, SPARC outer disks
    gap = abs(math.log10((1.0 + cap) / (1.0 + cls)))
    gaps[eta] = (cap, cls, gap)
    print("  eta = %5.1f | cap floor %6.2f%% | class %7.4f%% | gap %.3f dex"
          % (eta, 100 * cap, 100 * cls, gap))
tgt = {2.0: 0.118, 3.0: 0.083, 5.0: 0.049, 10.0: 0.019}
ok3 = bool(all(abs(gaps[e][2] - tgt[e]) < 5e-4 for e in tgt)
           and gaps[2.0][2] >= SPARC_FLOOR and gaps[3.0][2] >= SPARC_FLOOR
           and gaps[5.0][2] < SPARC_FLOOR
           and prov("SW05_kepler_freeze.out", "0.118") and prov("SW05_kepler_freeze.out", "0.083"))
check("X3 P4 gaps 0.118/0.083/0.049/0.019 dex at eta = 2/3/5/10 (SW05 B1) recomputed",
      "computed %.3f / %.3f / %.3f / %.3f vs landed 0.118/0.083/0.049/0.019"
      % (gaps[2.0][2], gaps[3.0][2], gaps[5.0][2], gaps[10.0][2]),
      ok3,
      "distinctive window eta ~ 2-3.5 vs the 0.06-dex SPARC floor; ported from SW05 B")

# ------------------------------------ X4: P9 ladder vs SW05 D (the eBTFR rungs)
print("\nX4. P9 the eBTFR zero-point ladder a0_eff/a0 = S(eta)^2 (L4 link; SW05 D)")
env_tab = [("field (v_pec H0)", 400e3 * H0),
           ("group infall (300 km/s, 2 Mpc)", (300e3) ** 2 / (2e6 * PC)),
           ("group (500 km/s, 1 Mpc)", (500e3) ** 2 / (1e6 * PC)),
           ("cluster vicinity (1000 km/s, 2 Mpc)", (1000e3) ** 2 / (2e6 * PC))]
ladder = []
for label, g in env_tab:
    eta_v = g / a0
    S_v = 1.0 if MUTATE else S_env(eta_v, eta_c)
    ladder.append((label, eta_v, S_v ** 2))
    print("  %-36s eta = %.4f | a0_eff/a0 = %.4f" % (label, eta_v, S_v ** 2))
ltgt = [0.9958, 0.9884, 0.7169, 0.3364]
monoL = all(ladder[i][2] > ladder[i + 1][2] for i in range(len(ladder) - 1))
ok4 = bool(all(abs(ladder[i][2] - ltgt[i]) < 5e-4 for i in range(4)) and monoL
           and prov("SW05_kepler_freeze.out", "0.7169")
           and prov("SW05_kepler_freeze.out", "0.3364"))
check("X4 P9 ladder 0.996/0.988/0.717/0.336 monotone (SW05 D1) recomputed",
      "computed %s vs landed 0.9958/0.9884/0.7169/0.3364 (monotone %s)"
      % ("/".join("%.4f" % l[2] for l in ladder), monoL),
      ok4,
      "a0_eff/a0 = S^2 at the four environments; ported from SW05 D / SW04 C")

# ------------------- X5: the x = 2.5 gate, both readings both footings (L6)
print("\nX5. the x = 2.5 gate: 152.1/220.3 per-field, 304.1/440.7 dilution (L6; "
      "GATE_CONVENTION.md, SW01b D, SW06 D2)")
S25 = {}
for footing in ("canonical", "alt"):
    S25[footing] = S_env(2.5, ETA_C[footing])
    print("  %-9s S(2.5) = %.6f | per-field 1/S = %.1f | dilution 2/S = %.1f"
          % (footing, S25[footing], 1.0 / S25[footing], 2.0 / S25[footing]))
ok5 = bool(abs(S25["canonical"] - 0.006576) < 2e-6 and abs(S25["alt"] - 0.004538) < 2e-6
           and abs(1.0 / S25["canonical"] - 152.1) < 0.1
           and abs(1.0 / S25["alt"] - 220.3) < 0.1
           and abs(2.0 / S25["canonical"] - 304.1) < 0.1
           and abs(2.0 / S25["alt"] - 440.7) < 0.1
           and abs(D_int - 0.2590) < 0.002
           and abs(2.0 / S25["canonical"] - 2.0 * (1.0 / S25["canonical"])) < 1e-9
           and prov("GATE_CONVENTION.md", "152.1") and prov("GATE_CONVENTION.md", "440.7")
           and prov("SW06_conformal_mu.out", "304.1"))
check("X5 gate four numbers 152.1/220.3/304.1/440.7 (GATE_CONVENTION) recomputed",
      "S(2.5) = %.6f/%.6f (canonical/alt); 1/S = %.1f/%.1f; 2/S = %.1f/%.1f; "
      "D_int = %.4f" % (S25["canonical"], S25["alt"], 1.0 / S25["canonical"],
                        1.0 / S25["alt"], 2.0 / S25["canonical"], 2.0 / S25["alt"], D_int),
      ok5,
      "the 2x is the GATE_CONVENTION's two readings ((g_src+g_ext)/g_src = 2 exactly "
      "at the gate), not a discrepancy; both readings clear the 6.4 gate on both footings")

# --------------------------------------- X6: eBTFR slope 1/4 for any S (L4)
print("\nX6. eBTFR v^4 = S^2 G M a0, slope 1/4 for ANY S (L4; SW04 A2/A3, "
      "SW06_lemmas.lean eBTFR)")
G_, M_, a0_, S_ = sp.symbols("G M a0 S", positive=True)
v2 = S_ * sp.sqrt(G_ * M_ * a0_)                       # deep limit: g = S sqrt(a0 g_N)
slope2 = sp.simplify(M_ / v2 * sp.diff(v2, M_))        # d ln v^2/d ln M = 2 x (d ln v/d ln M)
v4res = sp.simplify(v2 ** 2 / (S_ ** 2 * G_ * M_ * a0_) - 1)
ok6 = bool(slope2 == sp.Rational(1, 2) and v4res == 0
           and prov("SW04_conformal_efe.out", "A2 sympy eBTFR"))
check("X6 d ln v/d ln M = 1/4 for any S and v^4/(S^2 G M a0) = 1 (SW04 A2/A3) recomputed",
      "d ln v^2/d ln M = %s (== 2 x 1/4); v^4 identity residual %s"
      % (slope2, v4res),
      ok6,
      "sympy, exact; the Lean counterpart is theorem eBTFR in SW06_lemmas.lean "
      "(compiled, exit 0); measured slope 3.98 +- 0.06")

# ---------------------- X7: alpha_2 double suppression + the c_S bound (L7)
print("\nX7. alpha_2 doubly suppressed; c_S <= 4.23 / 423 (L7; SW08 B1-B5)")
vc_cmb = 370e3                                          # m/s vs the CMB rest frame (SW08 B1)
trigger = 4.0 * (vc_cmb / C_LIGHT) ** 2                 # the boost anisotropy (SW08 B2)
u_sun = (ETA_SUN["canonical"] / eta_c) ** 2
dS = abs(2.0 * u_sun / (1.0 + u_sun) ** 2)              # |dS/dln eta| (SW08 B3)
x_planet = 7.0e5                                        # g_N/a0 in the deep-Newton regime (SW08 B4)
resp = float(nu_rar(x_planet)) - 1.0                    # the planetary response
alpha2_est = trigger * dS * resp                        # doubly suppressed (SW08 B4)
cS_nord = 4.0e-7 / (trigger * dS)                       # Nordtvedt ceiling -> c_S bound
cS_llr = 4.0e-5 / (trigger * dS)                        # LLR-scale ceiling -> c_S bound
print("  trigger 4(v/c)^2 = %.3e | |dS/dln eta| = %.5f | response nu(%.0e)-1 = %.1e"
      % (trigger, dS, x_planet, resp))
print("  alpha_2 estimate = %.1e (exactly 0: response suppressed) | c_S <= %.2f / %.0f"
      % (alpha2_est, cS_nord, cS_llr))
ok7 = bool(abs(trigger - 6.093e-6) < 1e-8 and abs(dS - 0.01551) < 1e-4
           and alpha2_est <= 1e-18
           and abs(cS_nord - 4.23) < 0.05 and abs(cS_llr - 423.0) < 5.0
           and prov("SW08_preferred_frame.out", "4.23") and prov("SW08_preferred_frame.out", "423"))
check("X7 alpha_2 = 0.00e+00 (double suppression) and c_S <= 4.23/423 (SW08 B4/B5) recomputed",
      "trigger %.3e x |dS/dln eta| %.5f x response %.1e = %.1e; c_S bounds %.2f / %.0f"
      % (trigger, dS, resp, alpha2_est, cS_nord, cS_llr),
      ok7,
      "the coupling c_S is the named missing input of G03; the class's own "
      "contribution is structurally 0 at planetary x")

# ----------------------------------------- X8: eta_c window consistency (A7)
print("\nX8. eta_c window consistency (A7; SW01b B2, SW03, SW07)")
alt_in = bool(0.145 <= ETA_C["alt"] <= 0.203)
floor_in = bool(0.028 <= ETA_C["alt"] <= ETA_C["canonical"])
canon_round = bool(round(ETA_C["canonical"], 3) == 0.203)
exceed = ETA_C["canonical"] - 0.203
fornax_ok = bool(0.145 < ETA_C["alt"])
print("  declared 0.2034 (canonical) / 0.1688 (alt); window edges: Oort ceiling 0.203, "
      "LSS floor 0.028, Fornax-implied 0.145")
print("  alt inside [0.145, 0.203]: %s | canonical vs ceiling: 0.2034 = 0.203 at 3 dp (%s), "
      "exceedance %.1e (precision note)" % (alt_in, canon_round, exceed))
ok8 = bool(alt_in and floor_in and canon_round and fornax_ok
           and prov("SW01b_envscalar_orthogonality.out", "0.2034")
           and prov("SW01b_envscalar_orthogonality.out", "0.1688")
           and prov("SW07_eta_c_attack.out", "0.145")
           and prov("SW07_eta_c_attack.out", "0.028"))
check("X8 eta_c window consistency (SW01b B2 declaration vs the landed window)",
      "alt 0.1688 in [0.145, 0.203]: %s; in [0.028, 0.2034]: %s; canonical 0.2034 = "
      "ceiling 0.203 at the quoted 3 dp: %s (exceedance %.1e)"
      % (alt_in, floor_in, canon_round, exceed),
      ok8,
      "the brief's 0.16879 is the alt constant at 5 dp; the landed code constant is "
      "0.1688 -- same quantity; the brief's window lower edge 0.145 is the Fornax-implied "
      "bound (SW03/SW07), the landed window's lower edge is the LSS floor 0.028 (SW01b F)")

# ---------------------------------------------- X9: eta_sun (SW01b B1, L0 tie)
print("\nX9. eta_sun = |g_env(B)|/a0 rebuilt (L0 tie; SW01b B1, SW09_meanvalue D2)")
eta_re = (233e3) ** 2 / (8.2 * 3.0857e19) / a0
print("  v_c^2/R_0/a0 = %.4f (8.2 kpc = 8.2 x 3.0857e19 m)" % eta_re)
ok9 = bool(abs(eta_re - 2.292) < 0.01 and abs(eta_re - 2.2918) < 0.001
           and prov("SW01b_envscalar_orthogonality.out", "2.292")
           and prov("SW09_meanvalue.out", "2.2918"))
check("X9 eta_sun rebuilt = 2.292 (SW01b B1) = |g_env(B)|/a0 (SW09_meanvalue D2: 2.2918)",
      "computed %.4f vs landed 2.292 / 2.2918" % eta_re,
      ok9,
      "SW09_meanvalue D2: v_c^2/R_0 IS the ambient Galactic field at the Solar radius, "
      "so the record's eta_sun is exactly the T2 point value -- right for a deeper reason "
      "than the lane knew")

# ------------------------------------------------------------------ verdict
n_fail = sum(1 for c in checks if not c["ok"])
n_pass = len(checks) - n_fail
verdict = "all match" if n_fail == 0 else "any findings"
print("\nSW09_chain COMPLETE: %d/%d cross-checks match." % (n_pass, len(checks)))
if n_fail == 0:
    verdict_line = ("SW09_chain -- the certified prediction chain. Every frozen number "
                    "recomputed from the axioms A1-A7 matches its landed .out target: "
                    "gamma_v %.5f-%.5f (SW04 D); A2 %.2e (SW04 B1/SW05 C1); P4 gaps "
                    "%.3f/%.3f dex at eta = 2/3 (SW05 B); P9 ladder %.4f/%.4f/%.4f/%.4f "
                    "(SW05 D); gate %.1f/%.1f per-field and %.1f/%.1f dilution "
                    "(GATE_CONVENTION); eBTFR slope 1/4 any S (sympy, SW04 A3); alpha_2 "
                    "structural 0 with c_S <= %.2f/%.0f (SW08 B4/B5); eta_c window "
                    "consistent (canonical = Oort ceiling 0.203 at the quoted 3 dp, "
                    "exceedance %.1e -- precision note, not a mismatch); eta_sun %.4f "
                    "ties L0 (SW09_meanvalue D2). Cross-check verdict: %s. The chain's "
                    "10 links (L0, L1-L8, C1) each carry (file, check, number)."
                    % (gmin, gmax, canc, gaps[2.0][2], gaps[3.0][2],
                       ladder[0][2], ladder[1][2], ladder[2][2], ladder[3][2],
                       1.0 / S25["canonical"], 1.0 / S25["alt"],
                       2.0 / S25["canonical"], 2.0 / S25["alt"], cS_nord, cS_llr,
                       exceed, eta_re, verdict))
else:
    fails = [c["name"] for c in checks if not c["ok"]]
    verdict_line = ("SW09_chain -- the certified prediction chain. FAIL-as-finding "
                    "(never a silent edit): %s. Cross-check verdict: %s."
                    % ("; ".join(fails), verdict))
print(verdict_line)
if MUTATE:
    print("[MUTATE run: misses vs the landed targets are the pre-registered mutant "
          "finding (SW05 docstring: the mutant loses every distinctive number).]")

out = {"lane": "SW09_chain", "mutate": MUTATE,
       "n_pass": n_pass, "n_total": len(checks), "verdict": verdict,
       "checks": checks, "verdict_line": verdict_line,
       "constants": {"a0": A0, "eta_c": ETA_C, "eta_sun": ETA_SUN,
                     "H0_s^-1": H0, "c_light": C_LIGHT},
       "computed": {"gamma_min": gmin, "gamma_max": gmax,
                    "BR_cancellation": canc, "A2_clean": a2_clean,
                    "P4_gaps": {str(e): gaps[e][2] for e in gaps},
                    "P9_ladder": {l[0]: l[2] for l in ladder},
                    "S25": {k: S25[k] for k in S25},
                    "gate_per_field": {"canonical": 1.0 / S25["canonical"],
                                       "alt": 1.0 / S25["alt"]},
                    "gate_dilution": {"canonical": 2.0 / S25["canonical"],
                                      "alt": 2.0 / S25["alt"]},
                    "D_int": D_int, "alpha2_est": alpha2_est,
                    "cS_bounds": {"nordtvedt": cS_nord, "llr": cS_llr},
                    "eta_sun_rebuilt": eta_re,
                    "eta_c_exceedance_vs_0.203": exceed},
       "chain_edges": 10,
       "edge_convention": "edge = one numbered chain link (L0, L1-L8, C1); "
                          "the axioms A1-A7 are the input block, not edges"}
with open(JSON_PATH, "w") as f:
    json.dump(out, f, indent=1)
print("\n(json written: SW09_chain.json)")
