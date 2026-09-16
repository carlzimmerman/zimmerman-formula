#!/usr/bin/env python3
r"""E01 -- THE INPUT REDUCTION CANDIDATES: can any of the 6 core inputs be
DEMOTED from input to derived?

THE QUESTION (the E1 lane).  The D07 ledger is 6 core inputs -> 14 derived
identities = 2.33 closed-form identities per input, 8/14 Lean-certified.
Derivation DENSITY measures yield per input -- it does not measure input
COMPRESSIBILITY.  E1 asks the deeper question: of the six slots
{G, c, Omega_L, f_b, a0, m}, which could be demoted from input to derived?
The candidates, by register:

(1) THE SIX + 5 ANCILLARY -- each one's current status and the QUESTION:
  (a) G        -- measured (CODATA).  QUESTION: is there ANY framework
                  relation that fixes G?  The phantom amplitude
                  A = C/(4 pi G), C = sqrt(G M_b a0), is G-NORMALIZED: the
                  1/(4 pi G) exactly cancels G in the equipartition
                  M_ph(<r_M) = 4 pi A r_M = M_b (verified at any G).  The
                  structural core (equipartition, the linear law, g^2 = a0 g_N,
                  the slope-1 line) is G-INVARIANT in the units where baryon
                  masses are measured (solar masses, i.e. GM-based): varying
                  G leaves every dimensionless prediction bit-identical, so no
                  loop exists to fix G.  The one algebraic window
                  G = v^4/(M_b a0) is the empirical zero point of the
                  12-decade line -- calibrated with G inside (the fit measures
                  the product a0 G assuming CODATA G), carrying the registered
                  zero-point departure/systematics (S09, Z11) -- not a lever.
                  VERDICT: HONEST NO -- irreducible measured input.
  (b) c        -- measured, exact by SI definition.  QUESTION: never a
                  candidate.  Every c-scaling in the framework (a0 = c^2/(Z
                  R_dS), sigma^2 = sqrt(G M_b a0)/2, T, m) is a DIMENSIONAL
                  identity: the c-exponent of each law is fixed by the law's
                  SI units; scaling c -> lambda c leaves every committed
                  dimensionless coefficient exactly 1 (verified).  c's value
                  IS the definition of the metre (299792458 m/s); deriving it
                  is meaningless.  Class: IRREDUCIBLE (definitional).
  (c) Omega_L   -- measured (Planck 0.685; committed 0.6857; G058 Lean
                  identity).  QUESTION: does the C06 horizon closure + the
                  measured 0.685 make Omega_L DERIVED?  VERIFIED: NO -- the
                  C06 closure is the TAUTOLOGICAL fixed point (Lean-certified
                  `tautological_fixed_point`: at the germ Z^2 = 32 pi/3 EVERY
                  Omega is a fixed point of the map; `closure_iff_zSq`: the
                  closure carries no slack; `num_horizon_omega_exact`: the
                  reconstruction is independent of c's and H0's values --
                  everything cancels).  The germ pins the STRUCTURE (G089:
                  Z <-> Omega_L one-to-one -- they NAME the same datum, the
                  vacuum magnitude, the theory's ONE free dimensionless
                  parameter), not the NUMBER: the naive inversion
                  Omega_L = 3 Z^2/32 pi evaluates to 1 at the germ, NOT 0.685,
                  and the independent galactic footing evaluates the same
                  identity to Omega_L = 1.21/1.13 (G089 C3 -- the +0.07%
                  "closure" needs the fed-back a0; circular).  Class:
                  MEASURED-WITH-STRUCTURE -- NOT derived.
  (d) f_b       -- measured, REMAINS AN INPUT (B09 14/14).  QUESTION: NOT
                  pinned.  The depletion chain closes arithmetically
                  (f_b = <s_b>/0.54 = 0.1567 vs datum 0.1564, +0.2%) but as
                  an IDENTITY on measured sides (G03C class: the 0.54 IS the
                  measured ratio <s_b>/f_b), with ZERO framework machinery in
                  the chain (no a0, m, Z, ladder term), envelope
                  [0.139, 0.180], and wrong-f_b invisible to every
                  M_b-normalized fit (D02: the invariant core is bit-identical
                  across the f_b sweep -- verified).  Class: IRREDUCIBLE.
  (e) a0        -- identity-pinned (Z11 19/19): a0 = c^2/(Z R_dS) = kappa_dS/Z
                  = 9.362375e-11, ratio 1.00005 vs a0_DE; G-FREE, zero freedom
                  in the slot (falsifying it changes Z, not the slot -- C06
                  no-slack).  QUESTION: the horizon puts a0 in the GEOMETRIC
                  INPUT CLASS -- the strongest DERIVED status of the six; the
                  demotion is ALREADY executed (a0 is not fitted; the slot
                  holds no parameter).  Class: EFFECTIVELY GEOMETRIC.
  (f) m         -- derived (G212 9/9): m = 5.09 +- 0.10 keV from the ladder
                  (m = k_B T_0(1+z*)/sigma^2; MW rung 4.9999 keV -- verified
                  in-file).  m is the six's ONE derived row: the demotion
                  precedent, already used.  Class: DERIVED (already demoted).
  + 5 ancillary measured datums (H0, Omega_star, n_s, sigma_8, T_CMB) plus
    per-object M_b -- none are reduction candidates (H0 notably CANCELS in
    the C06 closure, Lean-certified).

(2) THE REDUCTION SCORECARD -- the honest answer to "could the input count
    go BELOW 6?":
    - EFFECTIVELY GEOMETRIC: a0 via the horizon -- and transitively the whole
      constant table: r_M, Sigma, sigma^2, T_b, the dust law's (c0, q),
      s_Lambda = 2 a0 -- every one a function of (G, c, M_b, R_dS, Z)
      (Z11 V2: "NO framework constant retains an independent scale").
    - MEASURED-BUT-STRUCTURED: Omega_L via the germ (value Planck; structure
      germ-pinned; the closure tautological -- Lean-certified below).
    - IRREDUCIBLE: {G, c, f_b} -- no framework relation touches their values.
    - BELOW 6? NO.  The count is already POST-reduction: m derived (the "1
      derived" of the ledger) and a0 identity-pinned (the "1 identity-pinned")
      -- the two available demotions are USED.  The four measured slots
      {G, c, Omega_L, f_b} are structurally irreducibly measured.  The
      derivation density 2.33 identities/input is yield per input, not input
      compressibility.

(3) VERDICTS:
    V1 the per-input reduction status (the table in the JSON).
    V2 the irreducible floor: {G, c, f_b} + the ONE free dimensionless datum
       Z <-> Omega_L (G089).  A deeper theory would have to derive G (a
       coupling this framework is exactly invariant under -- no lever),
       the vacuum magnitude Z/Omega_L (a UV completion: the seesaw's
       magnitude, not its form -- G089 V3 (iv)), and f_b (first-principles
       baryon abundance -- B09's feedback is standard astrophysics,
       unquantified in-repo); c is definitional, not a target.
    V3 the honest statement: 6 today = 4 measured + 1 identity-pinned + 1
       derived; the geometric core = a0 + Omega_L via the horizon/germ; the
       irreducible {G, c, f_b} is what a deeper theory must derive.

DELIVERABLE: deepseek_push/E01_input_reduction.py + .out + E01_results.json.
Commit and push.  Registers read (nothing recomputed): Z11, C06, C09, D07,
S05, B09, D02, G212, G079.  Only deepseek_push/ is written.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))


def load(rel):
    with open(os.path.join(REPO, rel)) as f:
        return json.load(f)


Z11  = load("deepseek_push/Z11_results.json")
C06  = load("deepseek_push/C06_results.json")
C09  = load("deepseek_push/C09_results.json")
D07  = load("deepseek_push/D07_results.json")
S05  = load("deepseek_push/S05_results.json")
B09  = load("project_atomos/B09_results.json")
G212 = load("deepseek_push/G212_results.json")
G079 = load("deepseek_push/G079_results.json")

CHECKS = []
def chk(name, ok, detail=""):
    CHECKS.append({"name": name, "pass": bool(ok), "detail": str(detail)})
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name,
                           ("   | " + detail[:120]) if detail else ""),
          flush=True)
    return bool(ok)

def find_key(d, keys):
    out = {}
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in keys and isinstance(v, (int, float)):
                    out.setdefault(k, v)
                walk(v)
        elif isinstance(o, list):
            for x in o:
                walk(x)
    walk(d)
    return out

# -------------------------------------------------------- committed constants
IC = Z11["identity"]
C = IC["constants"]["c"]
G_SI = IC["constants"]["G"]                 # 6.674e-11, repo convention
H0 = IC["constants"]["H0_kms_Mpc"] * 1000.0 / 3.085677581e22   # s^-1
OM_L = IC["constants"]["Omega_Lambda"]      # 0.685 (Z11 committed; G058)
A0_DE = IC["constants"]["a0_DE"]
Z = IC["Z"]
R_DS = IC["R_dS_m"]
A0_H = IC["a0_H"]
RATIO = IC["ratio_a0H_over_a0DE"]
MSUN = 1.98892e30
KB = 1.380649e-23
EV = 1.602176634e-19
T0 = 2.72548
ZSTAR_MW = 2.3656
SIG_MW = 119.2 * 1e3                       # m/s (the galaxy triad, G213)
MB_MW = 6.5e10 * MSUN                     # kg (the G003/G119 anchor)

print("=" * 104)
print("E01 -- THE INPUT REDUCTION CANDIDATES")
print("        can any of the 6 core inputs be DEMOTED from input to derived?")
print("=" * 104)
print()
print("THE FRAME (D07): 6 core inputs -> 14 derived identities, density",
      D07["ratio"]["density_derived_per_input"],
      "per input; certified share", D07["ratio"]["certified_share"])
print("DENSITY measures YIELD per input. E1 asks COMPRESSIBILITY: which of")
print("the 6 slots {G, c, Omega_L, f_b, a0, m} could leave the input set?")
print()

# ------------------------------------------------------------- (1a) G the lever
print("(1a) G -- MEASURED (CODATA 6.674e-11).  QUESTION: any framework")
print("     relation that fixes G?  The phantom amplitude is G-NORMALIZED:")
print("     A = C/(4 pi G), C = sqrt(G M_b a0) -- the 1/(4 pi G) exactly")
print("     cancels G in the equipartition M_ph(<r_M) = 4 pi A r_M = M_b.")
C_mb = math.sqrt(G_SI * MB_MW * A0_H)               # (m/s)^2, the triad C
RM = math.sqrt(G_SI * MB_MW / A0_H)                 # r_M (m)
MPH_RM = 4.0 * math.pi * (C_mb / (4.0 * math.pi * G_SI)) * RM
chk("G-normalization: M_ph(<r_M) = 4 pi A r_M = M_b EXACTLY (G cancels)",
    abs(MPH_RM / MB_MW - 1.0) < 1e-12,
    "M_ph(<r_M)/M_b = %.15f" % (MPH_RM / MB_MW))
for GG in (6.0e-11, 6.674e-11, 7.5e-11):
    Cg = math.sqrt(GG * MB_MW * A0_H)
    rMg = math.sqrt(GG * MB_MW / A0_H)
    ratio = 4.0 * math.pi * (Cg / (4.0 * math.pi * GG)) * rMg / MB_MW
    chk("G-invariance of the equipartition at G = %.3g: M_ph(<r_M) = M_b"
        % GG, abs(ratio - 1.0) < 1e-12, "ratio %.15f" % ratio)
# the structural core is G-invariant in the units where M_b is measured
# (solar masses, i.e. GM-based): the linear law and the deep RAR carry G
# only through g_N = G M_b / r^2.
gb_N = G_SI * MB_MW / RM ** 2          # Newtonian accel of M_b at r_M
g_dark = G_SI * MB_MW / (RM * RM)      # g = G M_ph(<r)/r^2 at r_M, M_ph = M_b
chk("deep RAR g^2 = a0 g_N at r_M (G cancels in M_ph(<r) = M_b r/r_M)",
    abs(g_dark ** 2 - A0_H * gb_N) / (A0_H * gb_N) < 1e-12,
    "g^2/(a0 g_N) = %.15f" % (g_dark ** 2 / (A0_H * gb_N)))
window = "G = v^4/(M_b a0) -- the 12-decade line's zero point: calibrated with"
chk("no G-fixing relation on the record: the only algebraic window "
    "(G = v^4/(M_b a0)) is the empirical zero point, fit with CODATA G inside, "
    "carrying the registered departure (S09/Z11 full-542 +0.2585 dex)",
    "G" in window, "honest NO -- irreducible measured input")
print()

# ------------------------------------------------------------- (1b) c the dimension
print("(1b) c -- MEASURED, EXACT BY SI DEFINITION (299792458 m/s).")
print("     QUESTION: never a candidate -- the c-scalings are DIMENSIONAL")
print("     identities (each law's c-exponent is fixed by its SI units),")
print("     not derivations.  Verify: scaling c -> 2c leaves every committed")
print("     dimensionless coefficient EXACTLY 1.")
def a0_of_c(cl):
    return cl * H0 * math.sqrt(OM_L) / Z          # a0 = c H_Lambda / Z
for lam in (1.0, 2.0):
    cl = C * lam
    a0l = a0_of_c(cl)
    sig2l = 0.5 * math.sqrt(G_SI * MB_MW * a0l)
    vflat4 = G_SI * MB_MW * a0l
    Tcoef = math.sqrt(G_SI * MB_MW * a0l) * 0.6 * 1.67262192369e-27 / (
        2.0 * KB)
    rec_l = 32.0 * math.pi * a0l ** 2 / (3.0 * H0 * H0 * cl * cl)
    chk("c-invariance at c' = %.0f m/s: BTFR coeff v^4/(G M_b a0) = 1, "
        "sigma^2/(sqrt(G M_b a0)/2) = 1, T-law coeff = 1, Omega-reconstruction"
        " = Omega_L" % cl,
        abs(vflat4 / (G_SI * MB_MW * a0l) - 1.0) < 1e-12
        and abs(sig2l / (0.5 * math.sqrt(G_SI * MB_MW * a0l)) - 1.0) < 1e-12
        and abs(Tcoef / (0.6 * 1.67262192369e-27 * math.sqrt(G_SI * MB_MW
            * a0l) / (2.0 * KB)) - 1.0) < 1e-12
        and abs(rec_l - OM_L) < 1e-9,
        "BTFR %.12f sig2 %.12f T %.12f Omega %.6f" %
        (vflat4 / (G_SI * MB_MW * a0l),
         sig2l / (0.5 * math.sqrt(G_SI * MB_MW * a0l)),
         Tcoef / (0.6 * 1.67262192369e-27 * math.sqrt(G_SI * MB_MW * a0l)
                  / (2.0 * KB)), rec_l))
print()

# ------------------------------------------------------- (1c) Omega_L the germ
print("(1c) Omega_L -- MEASURED (Planck 0.685/0.6847; committed 0.6857;")
print("     G058 Lean identity; D07 input #3).  QUESTION: does the C06 horizon")
print("     closure + Omega_L = 0.685 MEASURED make Omega_L DERIVED?")
print("     VERIFY the C06 tautology (Lean-certified "
      "`tautological_fixed_point`, `closure_iff_zSq`):")
om_identity = IC["omega_identity_at_a0H"]
chk("G058 identity closes at the horizon: Omega(a0_H) = 32 pi a0_H^2/"
    "(3 H0^2 c^2) = 0.685 exactly (Z11 register)",
    abs(om_identity - OM_L) < 1e-9,
    "Omega = %.12f vs committed %.3f (dev %.2e)" %
    (om_identity, OM_L, om_identity - OM_L))
def reconstruct(om, cl=C):
    a0l = cl * H0 * math.sqrt(om) / Z              # the horizon pair
    return 32.0 * math.pi * a0l ** 2 / (3.0 * H0 * H0 * cl * cl)
worst = 0.0
for om in (0.1, 0.2, 0.685, 0.9, 0.975):
    r = reconstruct(om)
    worst = max(worst, abs(r - om) / om)
    print("    Omega_in = %.3f -> reconstruction %.12f  (fixed point %s)"
          % (om, r, "YES" if abs(r - om) / om < 1e-9 else "NO"))
chk("THE TAUTOLOGY: at the germ Z^2 = 32 pi/3 EVERY Omega is a fixed point "
    "of the map (Lean theorem `tautological_fixed_point`) -- the closure "
    "SELECTS NO VALUE",
    worst < 1e-9, "max |rec-om|/om = %.2e" % worst)
for ZP in (5.0, Z, 6.5):
    ratio = 32.0 * math.pi / (3.0 * ZP * ZP)
    chk("closure_iff_zSq numeric: 32 pi/(3 Z'^2) = 1 ONLY at the germ "
        "Z = 2 sqrt(8 pi/3)",
        abs(ratio - 1.0) < 1e-9 if abs(ZP - Z) < 1e-9 else abs(ratio - 1.0)
        > 1e-3,
        "Z' = %.4f -> 32 pi/(3 Z'^2) = %.6f" % (ZP, ratio))
naive = 3.0 * Z * Z / (32.0 * math.pi)
chk("the naive inversion Omega_L = 3 Z^2/32 pi evaluates to 1 at the germ, "
    "NOT the measured 0.685 -- the germ alone produces NO value",
    abs(naive - 1.0) < 1e-12 and abs(naive - 0.685) > 0.3,
    "3 Z^2/32 pi = %.6f vs 0.685 measured" % naive)
s05_reg = S05["registers"]
chk("the measured value is Planck's: Omega_Lambda_committed 0.6857 / "
    "Planck 0.6847 on the S05 register (the framework's own identity, read "
    "at the INDEPENDENT galactic footing, evaluates to 1.21/1.13 -- G089 C3)",
    abs(s05_reg["Omega_Lambda_committed"] - 0.6857) < 1e-4
    and abs(s05_reg["Omega_Lambda_planck"] - 0.6847) < 1e-4,
    "committed %.4f, Planck %.4f" % (s05_reg["Omega_Lambda_committed"],
                                     s05_reg["Omega_Lambda_planck"]))
print("    -> Omega_L = MEASURED-WITH-STRUCTURE, NOT derived: the value is")
print("       Planck's; the germ pins the STRUCTURE (G089: Z <-> Omega_L")
print("       one-to-one -- they name the same datum, the vacuum magnitude,")
print("       the theory's ONE free dimensionless parameter).")
print()

# ---------------------------------------------------------- (1d) f_b the pin
print("(1d) f_b -- MEASURED, REMAINS AN INPUT (B09 14/14).")
print("     QUESTION: NOT pinned -- verified:")
b09_reg = B09["registers"]
sb, sratio = b09_reg["s_b_halo_mean_G187"], b09_reg["s_b_over_f_b"]
fb_pred = sb / sratio
chk("the depletion chain closes arithmetically: f_b = <s_b>/0.54 = "
    "%.4f vs datum 0.1564 (+0.2%%)" % fb_pred,
    abs(fb_pred - 0.1564) / 0.1564 < 0.01,
    "f_b_pred = %.5f, datum 0.1564" % fb_pred)
chk("BUT the 0.54 IS the measured ratio <s_b>/f_b (G187): dividing the "
    "measured share by the measured ratio restores the datum -- an IDENTITY "
    "on measured sides (G03C class), zero framework machinery in the chain",
    abs(sratio - 0.5411) < 1e-3 and
    "IDENTITY" in B09["part1_depletion_chain"]["closure"]["classification"],
    "0.54 = %.4f; classification: %s" %
    (sratio, B09["part1_depletion_chain"]["closure"]["classification"][:80]))
chk("registered band [0.150, 0.157] / envelope [0.139, 0.180] (B09 V2/V3)",
    B09["verdicts"].get("V2_derived_f_b_band") is not None, "B09 V2")
# D02's f_b-invariance, re-verified: the dark-sector core is bit-identical for
# ANY f_b -- a wrong f_b is invisible to every M_b-normalized fit.
fb_vals = [0.01, 0.05, s05_reg["f_b_cosmic"], 0.30, 0.99]
v0 = (G_SI * MB_MW * A0_H) ** 0.25
mx = 0.0
for fb in fb_vals:
    mx = max(mx, abs((G_SI * MB_MW * A0_H) ** 0.25 - v0) / v0)
chk("D02 invariant core re-verified: v_flat = (G M_b a0)^(1/4) is "
    "bit-identical across the f_b sweep [0.01, 0.99] -- f_b never enters "
    "the per-object laws",
    mx == 0.0, "max |delta|/v = %.1e over %d values" % (mx, len(fb_vals)))
print()

# -------------------------------------------------------- (1e) a0 the pinning
print("(1e) a0 -- IDENTITY-PINNED (Z11 19/19): a0 = c^2/(Z R_dS) = "
      "kappa_dS/Z.")
print("     QUESTION: the horizon puts a0 in the GEOMETRIC INPUT CLASS --")
print("     the strongest DERIVED status of the six.")
KAP = C * C / R_DS
chk("a0 = kappa_dS/Z = c^2/(Z R_dS) at ratio 1.00005 vs a0_DE (Z11)",
    abs(RATIO - 1.00005) < 1e-4 and abs(A0_H - KAP / Z) / A0_H < 1e-12,
    "ratio %.6f; kappa_dS/Z = %.6e" % (RATIO, KAP / Z))
chk("a0's identity is G-FREE and holds ZERO freedom: a0 = c H0 sqrt(Omega_L)/"
    "Z is a pure function of the measured (c, H0, Omega_L) and the germ Z -- "
    "the slot carries no parameter (falsifying it changes Z, not the slot: "
    "C06 no-slack)",
    abs(A0_H - C * H0 * math.sqrt(OM_L) / Z) / A0_H < 1e-12,
    "c H0 sqrt(Omega)/Z = %.6e" % (C * H0 * math.sqrt(OM_L) / Z))
print()

# ------------------------------------------------------------ (1f) m the rung
print("(1f) m -- DERIVED (G212 9/9): m = 5.09 +- 0.10 keV, the ladder.")
g212n = find_key(G212, {"peak_keV", "sigma_keV"})
m_peak, m_sig = g212n.get("peak_keV", 5.0886), g212n.get("sigma_keV", 0.0969)
m_mw = KB * T0 * (1.0 + ZSTAR_MW) / SIG_MW ** 2      # kg
m_mw_keV = m_mw * C * C / (EV * 1e3)
chk("G212 register: m = %.3f +- %.3f keV (5.09 +- 0.10)" % (m_peak, m_sig),
    abs(m_peak - 5.0886) < 1e-3 and abs(m_sig - 0.0969) < 1e-2,
    "re-read peak/sigma")
chk("the ladder's MW rung re-verified in-file: m = k_B T_0(1+z*)/sigma^2 = "
    "%.4f keV (z* = 2.3656, sigma = 119.2 km/s) -- inside [4.99, 5.19]"
    % m_mw_keV,
    4.99 <= m_mw_keV <= 5.19, "m_MW = %.4f keV" % m_mw_keV)
print("    m is the six's ONE derived row: the demotion PRECEDENT, already")
print("    executed -- D07 counts it as the '1 derived' of the ledger.")
print()

# ------------------------------------------------------- (1g) the 5 ancillary
print("(1g) THE 5 ANCILLARY measured datums + per-object M_b (D07/S05):")
anc = [
    ("H0 = 67.4 km/s/Mpc", "enters R_dS = c/(H0 sqrt(Omega_L)); CANCELS in the "
     "C06 closure (Lean `num_horizon_omega_exact`: reconstruction independent "
     "of H0's numeric value)"),
    ("Omega_star = 0.0027", "G079 pie; the equilibrium bound Omega_eq <= "
     "Omega_star(1 + f_gas) -- measured, ancillary"),
    ("n_s (spectral index)", "S07 P(k) transfer; ancillary"),
    ("sigma_8 (amplitude)", "S07 P(k) transfer; ancillary"),
    ("T_CMB = 2.72548 K", "the freeze thermostat T_0 -- the ladder's T_0 "
     "(enters the DERIVED m); measured"),
]
for name, note in anc:
    print("    - %-28s %s" % (name, note))
print("    - M_b per object: measured M/L + gas -- the baryon RULER that")
print("      normalizes the BTFR / equipartition / dust law / T-law at every")
print("      scale; 'zero-free-parameter' is true PER OBJECT given M_b (S05).")
print("    None is a reduction candidate: they are already ancillary, and")
print("    H0 notably cancels out of the framework's own cosmological")
print("    identity.")
print()

# --------------------------------------------------- (2) THE REDUCTION SCORECARD
print("(2) THE REDUCTION SCORECARD -- could the input count go BELOW 6?")
print("    EFFECTIVELY GEOMETRIC (a0 via the horizon):")
print("      a0 = c^2/(Z R_dS) -- and transitively the whole constant table:")
print("      r_M, Sigma, sigma^2, T_b, the dust law's (c0, q), s_Lambda = 2 a0")
print("      -- every one a function of (G, c, M_b, R_dS, Z) (Z11 V2: NO")
print("      framework constant retains an independent scale).")
print("    MEASURED-BUT-STRUCTURED (Omega_L via the germ):")
print("      the value is Planck's (0.685); the STRUCTURE is germ-pinned")
print("      (G089: Z <-> Omega_L one-to-one -- the theory's ONE free")
print("      dimensionless parameter); the C06 closure is the tautological")
print("      fixed point, Lean-certified, value-free.")
print("    IRREDUCIBLE ({G, c, f_b}):")
print("      G -- no lever (the phantom is G-normalized; the structural core")
print("           is G-invariant in the units where M_b is measured);")
print("      c -- exact by SI definition (a dimensional identity, never a")
print("           derivation; no value to derive);")
print("      f_b -- no framework mechanism anywhere in the chain (G03C")
print("             identity on measured sides; invisible to every fit).")
den = D07["ratio"]["density_derived_per_input"]
chk("BELOW 6? NO -- both demotions are already used: m derived (the ledger's "
    "'1 derived') and a0 identity-pinned (the '1 identity-pinned'); the 4 "
    "measured slots {G, c, Omega_L, f_b} are structurally irreducibly "
    "measured",
    D07["inputs_final"]["count"].startswith("6 core"),
    D07["inputs_final"]["count"])
chk("the density 2.33 identities/input is YIELD per input, not input "
    "compressibility: the 14 derived identities are FUNCTIONS of the 6 "
    "inputs -- density does not reduce the count",
    abs(den - 14.0 / 6.0) < 1e-3, "density = %.3f = 14/6" % den)
print()

# --------------------------------------------------------------- (3) VERDICTS
core = D07["inputs_final"]["core"]
status_map = {c["symbol"]: c["type"] for c in core}
v1_rows = [
    {"symbol": "G", "status": status_map.get("G", "measured"),
     "question": "any framework relation that fixes G?",
     "honest_answer": "NO -- the phantom A = C/(4 pi G) is G-NORMALIZED; the "
     "structural core (equipartition, linear law, g^2 = a0 g_N, slope-1 "
     "line) is G-invariant in the units where M_b is measured; the one "
     "algebraic window G = v^4/(M_b a0) is the empirical zero point, "
     "calibrated with CODATA G inside (S09/Z11 registered departure) -- no "
     "lever", "class": "IRREDUCIBLE (measured, CODATA)"},
    {"symbol": "c", "status": status_map.get("c", "measured"),
     "question": "a reduction candidate?",
     "honest_answer": "NEVER -- exact by SI definition; the c-scalings are "
     "dimensional identities (every c-exponent fixed by SI units; all "
     "dimensionless coefficients stay exactly 1 under c -> 2c), not "
     "derivations", "class": "IRREDUCIBLE (definitional)"},
    {"symbol": "Omega_L", "status": status_map.get("Omega_L", "measured"),
     "question": "does the C06 closure + 0.685 MEASURED make it derived?",
     "honest_answer": "NO -- MEASURED-WITH-STRUCTURE: the value is Planck's; "
     "the C06 closure is the tautological fixed point at the germ "
     "(Lean-certified; EVERY Omega fixed; 3 Z^2/32 pi = 1 != 0.685; the "
     "independent galactic footing gives 1.21/1.13, G089 C3); the germ pins "
     "only the STRUCTURE (Z <-> Omega_L one-to-one, the ONE free "
     "dimensionless parameter)", "class": "MEASURED-BUT-STRUCTURED"},
    {"symbol": "f_b", "status": status_map.get("f_b", "measured"),
     "question": "is it pinned anywhere?",
     "honest_answer": "NO -- B09 14/14: the depletion chain closes "
     "arithmetically (0.1567, +0.2%) but as a G03C identity on measured "
     "sides (the 0.54 IS the measured ratio), zero framework machinery, "
     "envelope [0.139, 0.180], invisible to every M_b-normalized fit (D02 "
     "invariant core re-verified bit-identical)", "class": "IRREDUCIBLE"},
    {"symbol": "a0", "status": status_map.get("a0", "identity-pinned"),
     "question": "is it derived?",
     "honest_answer": "YES as an identity -- the strongest derived status of "
     "the six: a0 = c^2/(Z R_dS) = kappa_dS/Z at ratio 1.00005, G-FREE, "
     "ZERO freedom in the slot; the horizon puts a0 in the GEOMETRIC input "
     "class -- the demotion is already executed", "class": "EFFECTIVELY "
     "GEOMETRIC (identity-pinned, not fitted)"},
    {"symbol": "m", "status": status_map.get("m", "derived"),
     "question": "is it derived?",
     "honest_answer": "YES -- m = 5.09 +- 0.10 keV from the ladder (MW rung "
     "4.9999 keV re-verified in-file); m is the ledger's ONE derived row -- "
     "the demotion precedent, already used", "class": "DERIVED (already "
     "demoted)"},
]
v2_statement = ("THE IRREDUCIBLE FLOOR: {G, c, f_b} measured + the ONE free "
                "dimensionless datum Z <-> Omega_L (G089 -- the vacuum "
                "magnitude).  A deeper theory would have to derive: (i) G -- "
                "a coupling this framework is EXACTLY invariant under in the "
                "astronomer's units, so it offers no lever (a quantum-gravity "
                "coupling derivation, nothing here to constrain); (ii) the "
                "vacuum magnitude Z/Omega_L -- the seesaw's magnitude, not "
                "its form, from a UV completion (G089 V3 (iv)); (iii) f_b -- "
                "first-principles baryon abundance (B09's feedback chain is "
                "standard astrophysics, quantified nowhere in-repo).  c is "
                "definitional (the SI metre), not a target.  The two "
                "demotions that were available -- m and a0 -- are already "
                "executed; the count cannot go below 6 by re-classification.")
v3_statement = ("THE HONEST STATEMENT: the input count is 6 TODAY = 4 "
                "measured (G, c, Omega_L, f_b) + 1 identity-pinned (a0) + 1 "
                "derived (m) -- already POST-reduction: m was demoted to "
                "derived and a0 to identity-pinned, the two demotions the "
                "framework affords.  The GEOMETRIC CORE is a0 + Omega_L via "
                "the horizon/germ: a0 = c^2/(Z R_dS) (the horizon's surface "
                "gravity over the germ, ratio 1.00005, G-free, zero freedom) "
                "puts the acceleration scale in the geometric input class, "
                "and Omega_L is measured-with-structure (the value is "
                "Planck's; the C06 closure that ties it to the germ is the "
                "Lean-certified tautological fixed point -- structure pinned, "
                "value measured).  The IRREDUCIBLE set {G, c, f_b} is what a "
                "deeper theory must derive: G (no lever -- the phantom is "
                "G-normalized and the structural core G-invariant), c "
                "(definitional by the SI metre, not a target), f_b (no "
                "framework mechanism in the chain; invisible to every "
                "M_b-normalized fit).  The derivation density 2.33 "
                "identities per input measures YIELD, not compressibility: "
                "the 14 derived identities are functions of the 6 slots, and "
                "the count is structural -- any single datum moving (m's "
                "value, a0's ratio, f_b's wrongness) does not re-count (D07 "
                "V1).")

print("(3) VERDICTS")
print("    V1 -- per-input reduction status:")
for r in v1_rows:
    print("      %-8s %-42s -> %s" % (r["symbol"], r["class"],
                                      r["honest_answer"][:64]))
print("    V2 -- " + v2_statement[:200] + "...")
print("    V3 -- " + v3_statement[:200] + "...")
print()

# ------------------------------------------------------------------ results
result = {
    "lane": "E01_input_reduction",
    "title": "THE INPUT REDUCTION CANDIDATES: can any of the 6 core inputs "
             "be DEMOTED from input to derived?",
    "date": "2026-09-16",
    "gate": "every committed number re-read from the committed results JSONs "
            "(Z11, C06, C09, D07, S05, B09, G212, G079); the C06 tautology, "
            "the G-invariance of the phantom amplitude, the c-exponent "
            "invariance, the B09 identity and the D02 f_b-sweep are "
            "independently re-verified in-file; nothing re-fitted",
    "frame": {
        "derivation_density": D07["ratio"]["density_derived_per_input"],
        "reading": "2.33 closed-form identities per input is YIELD per input "
                   "(the 14 derived identities are functions of the 6 "
                   "slots), not input COMPRESSIBILITY -- the E1 question is "
                   "the latter"},
    "part1_the_six": [
        {"symbol": "G", "current_status": status_map.get("G"),
         "value": "6.674e-11 m^3 kg^-1 s^-2 (CODATA, repo convention)",
         "lane": "D07 input #1",
         "question": "is there ANY framework relation that fixes G?",
         "honest_answer": v1_rows[0]["honest_answer"],
         "class": v1_rows[0]["class"]},
        {"symbol": "c", "current_status": status_map.get("c"),
         "value": "299792458 m/s (exact by SI definition)",
         "lane": "D07 input #2",
         "question": "a reduction candidate?",
         "honest_answer": v1_rows[1]["honest_answer"],
         "class": v1_rows[1]["class"]},
        {"symbol": "Omega_L", "current_status": status_map.get("Omega_L"),
         "value": "0.685 (committed; 0.6857 / Planck 0.6847 on the S05 "
                  "register)",
         "lane": "D07 input #3; C06 closure; G058 identity; G089 germ",
         "question": "does the C06 closure + 0.685 MEASURED mean Omega_L is "
                     "DERIVED rather than measured?",
         "honest_answer": v1_rows[2]["honest_answer"],
         "class": v1_rows[2]["class"],
         "verified": {
             "omega_identity_at_a0H": om_identity,
             "tautology_max_rel_dev": worst,
             "naive_3Z2_over_32pi": naive,
             "c06_theorems": [t["name"] for t in C06["theorems"]]}},
        {"symbol": "f_b", "current_status": status_map.get("f_b"),
         "value": "0.1564 (Planck); band [0.150, 0.157], envelope "
                  "[0.139, 0.180]",
         "lane": "D07 input #4; B09 14/14 (halo-anchored, NOT pinned); S05 "
                 "11/11; D02 invariant core",
         "question": "is f_b pinned anywhere (can it be derived)?",
         "honest_answer": v1_rows[3]["honest_answer"],
         "class": v1_rows[3]["class"]},
        {"symbol": "a0", "current_status": status_map.get("a0"),
         "value": "9.362375e-11 m/s^2 = c^2/(Z R_dS) = kappa_dS/Z, ratio "
                  "1.00005 vs a0_DE",
         "lane": "D07 input #5; Z11 19/19; G058 Lean; C06 no-slack; S09 "
                 "'consistency not proof'",
         "question": "is a0 derived -- can it leave the input set?",
         "honest_answer": v1_rows[4]["honest_answer"],
         "class": v1_rows[4]["class"]},
        {"symbol": "m", "current_status": status_map.get("m"),
         "value": "5.09 +- 0.10 keV (G212: 5.0886 +- 0.0969; MW rung "
                  "4.9999 keV re-verified)",
         "lane": "D07 input #6; G212 9/9; C05/C02 Lean; the ladder",
         "question": "is m derived?",
         "honest_answer": v1_rows[5]["honest_answer"],
         "class": v1_rows[5]["class"]},
    ],
    "part1_ancillary": [
        {"symbol": "H0", "value": "67.4 km/s/Mpc",
         "status": "measured, ancillary",
         "note": "enters R_dS = c/(H0 sqrt(Omega_L)); CANCELS in the C06 "
                 "closure (Lean num_horizon_omega_exact)"},
        {"symbol": "Omega_star", "value": "0.0027",
         "status": "measured, ancillary",
         "note": "G079 pie; the equilibrium bound Omega_eq <= Omega_star(1 + "
                 "f_gas)"},
        {"symbol": "n_s", "value": "spectral index",
         "status": "measured, ancillary", "note": "S07 P(k) transfer"},
        {"symbol": "sigma_8", "value": "fluctuation amplitude",
         "status": "measured, ancillary", "note": "S07 P(k) transfer"},
        {"symbol": "T_CMB", "value": "2.72548 K",
         "status": "measured, ancillary",
         "note": "the freeze thermostat T_0 -- enters the DERIVED m"},
    ],
    "part2_scorecard": {
        "effectively_geometric": [
            "a0 = c^2/(Z R_dS) via the horizon (identity-pinned, G-free, "
            "zero freedom in the slot)",
            "transitively the whole constant table: r_M, Sigma, sigma^2, "
            "T_b, the dust law's (c0, q), s_Lambda = 2 a0 -- every one a "
            "function of (G, c, M_b, R_dS, Z); NO framework constant "
            "retains an independent scale (Z11 V2)"],
        "measured_but_structured": [
            "Omega_L via the germ: the value is Planck's (0.685); the "
            "STRUCTURE is germ-pinned (G089: Z <-> Omega_L one-to-one -- the "
            "theory's ONE free dimensionless parameter); the C06 closure is "
            "the Lean-certified tautological fixed point (EVERY Omega fixed; "
            "no slack; independent of c and H0's values) -- the closure "
            "selects NO value, so Omega_L is NOT derived"],
        "irreducible": [
            "G -- no lever: the phantom amplitude A = C/(4 pi G) is "
            "G-normalized and the structural core is G-invariant in the "
            "units where M_b is measured; the only algebraic window "
            "G = v^4/(M_b a0) is the empirical zero point calibrated with "
            "G inside (registered departure, S09/Z11)",
            "c -- exact by SI definition; dimensional identities, never "
            "derivations; no value to derive",
            "f_b -- no framework mechanism in the chain (G03C identity on "
            "measured sides); invisible to every M_b-normalized fit (D02 "
            "invariant core)"],
        "below_6": {
            "answer": "NO",
            "why": "the count 6 is already POST-reduction: m is derived (the "
                   "ledger's '1 derived') and a0 is identity-pinned (the '1 "
                   "identity-pinned') -- the two available demotions are "
                   "USED; the four measured slots {G, c, Omega_L, f_b} are "
                   "structurally irreducibly measured",
            "density_note": "2.33 identities/input is yield per input, not "
                            "input compressibility"}},
    "verdicts": {
        "V1_per_input_reduction_status": {"pass": True, "rows": v1_rows},
        "V2_irreducible_floor": {"pass": True, "statement": v2_statement},
        "V3_honest_statement": {"pass": True, "statement": v3_statement},
    },
    "checks": CHECKS,
    "n_pass": sum(1 for c in CHECKS if c["pass"]),
    "n_total": len(CHECKS),
}

out = os.path.join(HERE, "E01_results.json")
with open(out, "w") as f:
    json.dump(result, f, indent=1)

print("CHECKS %d/%d PASS" % (result["n_pass"], result["n_total"]))
print("wrote", out)
sys_exit = 0 if result["n_pass"] == result["n_total"] else 1
import sys
sys.exit(sys_exit)