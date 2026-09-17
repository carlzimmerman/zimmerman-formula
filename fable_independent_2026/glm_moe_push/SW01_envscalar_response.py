#!/usr/bin/env python3
"""
SW01_envscalar_response.py -- the L264 first gate for the nonlocal class (2026-09-17)

Lane: glm_moe_push (user-created folder for this swing; mirrors the kappa_slot_2026 SW
convention; no commits -- files left for review).

THE CONSTRUCTION (PROPOSER_SW01_envscalar.md): the a0 response is not a local kernel of the
total field but of two nonlocal functionals of the Newtonian field on the Gauss sphere through
the field point:
    Gamma^2 = <|g_N|^2>_ang - |<g_N>_ang|^2       (angular variance: the field's own structure)
    eta     = |<g_N>_ang| / a0                    (the sphere's l=1 component: the environment)
    g_obs   = g_N + S(eta) * (nu_RAR(Gamma/a0) - 1) * g_N,enc,   S(eta) = 1/(1+(eta/eta_c)^2)
A uniform external field is pure l=1 on every sphere centred on the baryons: it enters eta,
never Gamma, and cannot trigger the response by itself.  A bound system's own field carries
angular structure (Gamma > 0) and triggers it.  That is the internal/external asymmetry L264
demands, with the system defined by the flux structure, not a hand-drawn boundary.

Variants (no tuning toward any gate):
  SW01-A  eta_c = 1    -- stress balance: the environment disrupts the condensate when its
                          stress eta^2 a0^2/(8 pi G) exceeds the condensate's own stress
                          scale a0^2/(8 pi G).  No free number.
  SW01-B  eta_c calibrated to the local dark budget (declared measured, the R8 route).

FIRST COMPUTATION (fixed by the 2026-09-17 swarm brief): the response at x = 2.5 for
(a) an isolated point mass and (b) the same mass in a uniform external field of 2.5 a0.
Report the ratio.  If it is < 6.4, stop.

MUTATE=1 breaks one hinge (the environment coupling S) -- the gate check must FAIL.
"""
import json, math, os, sys
import sympy as sp

MUTATE = os.environ.get("MUTATE", "0") == "1"

# ---- constants, stated separately from thresholds ------------------------------
A0 = {"canonical": 9.3619e-11,   # kappa = 1/2, H_Lambda = H0 sqrt(Omega_L) footing
      "alt":       1.1279e-10}   # rho_crit, cH0 footing
H0      = 67.4e3 / 3.0857e22    # s^-1
C_LIGHT = 2.99792458e8          # m/s
OMEGA_L = 0.685
G_NEW   = 6.674e-11
M_SUN   = 1.989e30
AU      = 1.496e11              # m
R0_PC   = 8200.0                # Galactic-centre distance, pc
ETA_X   = 2.5                   # the RAR transition x the brief fixes
RATIO_GATE = 6.4                # the L264 asymmetry gate (0.259/0.04)
Q_CEIL  = 5.2e-27               # Cassini quadrupole ceiling, s^-2 (L243's units)
Q_L243  = 6.44                  # the mu2 vector-capping quadrupole at eta = 2.48, in ceilings
OORT_BUDGET = 0.015             # Msun/pc^3, the local dark budget (L263 C1)
RHO_PH_UNC  = 1.92              # Msun/pc^3, uncapped 0.5-Msun-star phantom density (L263 C)
R_M_SUN_AU  = {"canonical": 7960.0, "alt": 7252.0}   # solar r_M per footing (L263)
NU_RECORD   = 0.259             # nu_RAR(2.5) - 1, the L264 record value
WB_BAND     = (1.16, 1.23)      # the pre-registered Gaia DR4 wide-binary band

checks = []
def check(name, measured, ok, reading=""):
    checks.append({"name": name, "ok": bool(ok), "measured": str(measured), "reading": reading})
    tag = "PASS" if ok else "FAIL"
    print("  [%s] %s" % (tag, name))
    print("           (%s%s)" % (measured, ("; " + reading) if reading else ""))

def nu_rar(y):
    """The record's RAR kernel: nu = 1/(1 - exp(-sqrt(y))), y = g_bar/a0."""
    return 1.0 / (1.0 - math.exp(-math.sqrt(y)))

def S_env(eta, eta_c):
    return 1.0 / (1.0 + (eta / eta_c) ** 2)

print("=" * 72)
print("SW01 -- the environmental-scalar response: the L264 first gate%s"
      % ("  [MUTATE: the environment coupling S is broken to 1]" if MUTATE else ""))
print("=" * 72)

# ---------------------------------------------------------------- A. controls
print("\nA. controls (both a0 footings; the record's numbers reproduced)")
# sympy identity: a0(kappa=1/2) = c H0 sqrt(3 Omega_L / 8 pi) / 2 exactly
c_, H_, Om_ = sp.symbols("c H Omega_Lambda", positive=True)
a0_sym = c_ * H_ * sp.sqrt(3 * Om_ / (8 * sp.pi)) / 2
a0_rebuilt_canonical = float(a0_sym.subs({c_: C_LIGHT, H_: H0, Om_: OMEGA_L}))
a0_rebuilt_alt = 0.5 * C_LIGHT * H0 * math.sqrt(3 / (8 * math.pi))
rel_can = abs(a0_rebuilt_canonical / A0["canonical"] - 1)
H0_implied = A0["alt"] / (0.5 * C_LIGHT * math.sqrt(3 / (8 * math.pi))) * 3.0857e22 / 1e3
rel_alt = abs(a0_rebuilt_alt / A0["alt"] - 1)
check("A1 a0 canonical rebuilt from (c, H0, Omega_L) at kappa = 1/2",
      "rebuilt %.5e vs record %.4e; rel = %.2e" % (a0_rebuilt_canonical, A0["canonical"], rel_can),
      rel_can < 1e-3, "sympy identity c*H*sqrt(3*Omega_L/8pi)/2; threshold rel < 1e-3")
check("A2 a0 alt footing rebuilt from (c, H0, rho_crit)",
      "rebuilt %.5e vs record %.4e; rel = %.2e" % (a0_rebuilt_alt, A0["alt"], rel_alt),
      rel_alt < 1e-3,
      "[FAIL is the finding] the record's alt number implies H0 = %.1f, not 67.4 -- a "
      "convention/rounding audit item (README rule 5); the gates below are footing-independent "
      "ratios, and the canonical footing rebuilds to %.1e" % (H0_implied, rel_can))

y_ = sp.symbols("y", positive=True)
deep = sp.limit(sp.sqrt(y_) / (1 - sp.exp(-sp.sqrt(y_))), y_, 0, "+")
high = sp.limit(1 / (1 - sp.exp(-sp.sqrt(y_))) - 1, y_, sp.oo)
check("A3 sympy: the kernel's deep limit nu(y)*sqrt(y) -> 1 and high limit nu -> 1",
      "deep = %s, high = %s" % (deep, high),
      sp.simplify(deep - 1) == 0 and sp.simplify(high) == 0,
      "g^2 = a0 g_N in the deep limit; Newton-safe at high field")

D_int = nu_rar(ETA_X) - 1.0
check("A4 control: nu_RAR(2.5) - 1 against the L264 record value 0.259",
      "computed %.4f vs record %.3f" % (D_int, NU_RECORD),
      abs(D_int - NU_RECORD) < 0.002, "threshold |diff| < 0.002")

# ------------------------------------------- B. the fixed first computation
print("\nB. the brief's fixed first computation: response at x = 2.5, isolated vs externally fielded")
S_oort   = OORT_BUDGET / RHO_PH_UNC          # S(2.5) the local dark budget forces
eta_c_B  = ETA_X / math.sqrt(1.0 / S_oort - 1.0)
variants = {"SW01-A (stress balance, eta_c = 1)": eta_c_A if False else 1.0,
            "SW01-B (Oort-calibrated)": eta_c_B}
if MUTATE:
    variants = {k + " [MUTATED: S = 1, hinge broken]": None for k in variants}

for label, eta_c in variants.items():
    if MUTATE or eta_c is None:
        S25 = 1.0
    else:
        S25 = S_env(ETA_X, eta_c)
    D_ext = S25 * D_int
    ratio = D_int / D_ext
    check("B[%s] the gate: internal %.4f vs external %.4f departure at x = 2.5; ratio = %.2f"
          % (label.split(" ")[0], D_int, D_ext, ratio),
          "S(2.5) = %.5f; ratio %.2f vs gate 6.4" % (S25, ratio),
          ratio >= RATIO_GATE,
          "(a) isolated point mass: g = nu(2.5) g_N, departure %.4f; (b) same mass in "
          "2.5 a0 uniform field: departure %.4f -- ratio = 1/S(2.5)" % (D_int, D_ext))

# ------------------------------------------- C. Cassini quadrupole
print("\nC. the point-mass quadrupole versus the 5.2e-27 s^-2 ceiling")
# The scalar capping kills the l=2 moment at leading order; the only quadrupole is the
# eta-gradient across the phantom's scale r_M, bound as Q_L243 * (dS/dln eta) * (r_M / R0).
g_sun_10au = G_NEW * M_SUN / (10 * AU) ** 2
for foot in ("canonical", "alt"):
    Gamma_solar = g_sun_10au / A0[foot]
    nu_excess = 1.0 / (1.0 - math.exp(-math.sqrt(Gamma_solar))) - 1.0  # ~e^-sqrt(6.3e7)
    frac_eta = (10 * AU) / (R0_PC * 3.086e16)                          # eta variation across 10 AU
    frac_RM = R_M_SUN_AU[foot] * AU / (R0_PC * 3.086e16)               # eta variation across r_M
    dslope = 2 * (ETA_X / eta_c_B) ** 2 / (1 + (ETA_X / eta_c_B) ** 2)  # dS/dln eta at 2.5
    q_bound = Q_L243 * dslope * frac_RM
    check("C[%s] solar modification at 10 AU is nu(%.2e) - 1 = %.1e; quadrupole bound <= %.2e ceilings"
          % (foot, Gamma_solar, nu_excess, q_bound),
          "Q_bound/Q_ceiling ~ %.2e (eta varies by %.2e across r_M = %.0f AU)"
          % (q_bound, frac_RM, R_M_SUN_AU[foot]),
          q_bound < 1.0,
          "scalar capping: no l=2 moment at leading order; residual = gradient of eta across "
          "the phantom's scale; a0_foot = %.4e" % A0[foot])

# ------------------------------------------- D. the Oort budget (R7, local dark)
print("\nD. the local dark budget: rho_dark = 1.92 * S(2.5) vs 0.015 Msun/pc^3 (L263 C1)")
for label, eta_c in (("SW01-A", 1.0), ("SW01-B", eta_c_B)):
    S25 = S_env(ETA_X, eta_c) if not MUTATE else 1.0
    rho = RHO_PH_UNC * S25
    over = rho / OORT_BUDGET
    check("D[%s] rho_dark = %.4f Msun/pc^3 = %.1fx the Oort budget" % (label, rho, over),
          "%.1fx vs budget (need < 3 per L263 C1)" % over,
          over < 3.0,
          "SW01-A dies here if over; SW01-B is calibrated to the budget by declaration")

# ------------------------------------------- E. wide binaries (R7, the DR4 falsifier)
print("\nE. wide binaries: the stated alternative gamma_v = sqrt(1 + S(2.5)*(nu(2.5)-1))")
for label, eta_c in (("SW01-A", 1.0), ("SW01-B", eta_c_B)):
    S25 = S_env(ETA_X, eta_c) if not MUTATE else 1.0
    gv = math.sqrt(1.0 + S25 * (nu_rar(ETA_X) - 1.0))
    inside = WB_BAND[0] <= gv <= WB_BAND[1]
    check("E[%s] gamma_v = %.4f vs registered band %.2f-%.2f" % (label, gv, WB_BAND[0], WB_BAND[1]),
          "outside the band below (stated alternative); killed at Gaia DR4 if the band confirms",
          not inside,
          "the class's registered alternative; DR4 2026-12-02 decides")

# ------------------------------------------- F. BTFR slope (sympy, internal branch untouched)
print("\nF. the BTFR slope from the deep limit")
G_, M_, a0_, r_ = sp.symbols("G M a0 r", positive=True)
v2 = sp.sqrt(G_ * M_ * a0_)                          # circular orbit: v^2 = g r, g = sqrt(GM a0)/r
v4 = v2 ** 4                                          # = (GMa0)^2
check("F1 v = (GMa0)^(1/4) exactly => d ln v / d ln M = 1/4 (BTFR slope 4.0)",
      "v^4/(GMa0)^2 = %s" % sp.simplify(v4 / (G_ * M_ * a0_) ** 2),
      sp.simplify(v4 / (G_ * M_ * a0_) ** 2 - 1) == 0,
      "measured 3.98 +- 0.06: the internal branch is untouched by S")

# ------------------------------------------- G. ghost / honesty
print("\nG. ghost and honesty findings")
check("G1 ghost: Hamiltonian bounded below as a quadratic-form theorem",
      "OPEN -- no new propagating dof (algebraic nonlocal law), but the theorem is not written",
      False,
      "deferred finding, not a kill; the action formulation is the open lane (G03-class)")
check("G2 honesty: eta_c(SW01-B) has a second independent derivation",
      "declared measured from the Oort budget; no second derivation exists",
      False,
      "the 08-09 near-miss rule (README rule 4): reported as declared, not derived")

# ---------------------------------------------------------------- verdict
n_pass = sum(1 for c in checks if c["ok"])
print("\nSW01 COMPLETE: %d/%d checks PASS." % (n_pass, len(checks)))
verdict = (
    "SW01-A (stress balance, eta_c = 1) -- %s\n"
    "SW01-B (Oort-calibrated) -- %s\n"
    "KILLS SURVIVED: L264 local no-go (the response is nonlocal in the l=1 projection); L263 "
    "real-mass pincer (the phantom is a field response, scalar-capped); L243's quadrupole does "
    "not apply to scalar capping (it bounds vector capping).\n"
    "THE KILL IT WOULD DIE BY: an external-field effect detected at the AQUAL level -- a real "
    "Solar-System EFE quadrupole, or Gaia DR4 wide-binary gamma_v inside 1.16-1.23 -- kills "
    "every candidate in this class. Second door: satellites at eta >~ 1 showing deep-MOND "
    "dispersions (per-object Jeans per L263 E decides).\n"
    "STATUS: SW01-A %s; SW01-B %s."
) % (
    "KILLED by the Oort budget (rho_dark = %.2f Msun/pc^3, %.1fx over)" % (RHO_PH_UNC * S_env(ETA_X, 1.0), RHO_PH_UNC * S_env(ETA_X, 1.0) / OORT_BUDGET) if not MUTATE else "mutation mode",
    "standing, with declared calibration and pre-registered falsifiers",
    "KILLED" if not MUTATE else "MUTATION VERIFIED (gate fails as required)",
    "OPEN with falsifiers: (1) gamma_v(DR4) = %.4f vs band 1.16-1.23, 2026-12-02; (2) any AQUAL-level EFE detection; (3) satellites at eta >~ 1 with deep-MOND sigma" % math.sqrt(1 + S_oort * (nu_rar(ETA_X) - 1)),
)
print(verdict)

out = {"lane": "SW01_envscalar_response",
       "mutate": MUTATE,
       "n_pass": n_pass, "n_total": len(checks),
       "checks": checks, "verdict": verdict,
       "constants": {"a0": A0, "eta_c_A": 1.0, "eta_c_B": eta_c_B, "S_oort": S_oort,
                     "ratio_gate": RATIO_GATE, "D_int": D_int,
                     "D_ext_A": D_int * S_env(ETA_X, 1.0), "D_ext_B": D_int * S_oort,
                     "ratio_A": 1.0 / S_env(ETA_X, 1.0), "ratio_B": 1.0 / S_oort,
                     "gamma_v_B": math.sqrt(1 + S_oort * (nu_rar(ETA_X) - 1.0))}}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "SW01_envscalar_response.json"), "w") as f:
    json.dump(out, f, indent=1)
print("\n(json written: SW01_envscalar_response.json)")
