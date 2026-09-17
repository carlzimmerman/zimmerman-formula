#!/usr/bin/env python3
"""L263 -- THE REAL-MASS PHANTOM PINCER: the equivalence principle versus the Oort limit.

The agent tracks' strongest structural reading is that the phantom is REAL MASS (G086/S08: "the sector is ORDINARY
MATTER, p = 0", so PPN = GR and lensing = dynamics come free) that is SWITCHED OFF near the Sun by the Galactic field
(G006/SOLAR_FACE_CLOSEOUT: "the phantom is absent ... EFE-capped", r_cap = r_M sqrt(a0/g_ext)).  This lane asks whether a
real fluid can be capped by a UNIFORM external field at all, and what happens if it cannot.

  A.  a real fluid obeys the (weak/strong) equivalence principle: a uniform external field is a coordinate
      acceleration in the fluid's freely falling frame and is unobservable (the hydrostatic condition is invariant
      under Phi -> Phi + g_ext . x); only the star's own field and the TIDAL part of the external field act on it.
      Certified as an identity below (sympy).  Hence the Galactic field cannot cap a real-mass phantom.
  B.  an uncapped deep-MOND phantom of a point mass M has M_ph(<r) = M (r/r_M - 1) for r > r_M = sqrt(GM/a0):
      for the Sun r_M = 7960 AU = 0.039 pc, so M_ph(<1 pc) = 25 M_sun.  Inside the Sun's tidal (Jacobi) radius in
      the Galaxy (~1-2 pc) the halo is bound to the Sun.
  C.  every star carries such a halo; the implied local dark density n_* x M_ph(<r_J) is compared with the Oort-limit
      dark budget (rho_dm,local = 0.010-0.015 M_sun/pc^3; total dynamical 0.09-0.10, baryons 0.08-0.09).
  D.  the dichotomy: a phantom that IS capped by |g_ext| must depend on the frame-dependent magnitude of the total
      field -- the AQUAL/QUMOND field response, which violates the SEP by construction and carries the external-field
      quadrupole L243 computed (6.44x / 7.63x the Cassini ceiling for mu_2).  Real mass: Oort-dead.  Field response:
      Cassini-dead.  There is no third reading on the record.
  E.  a correction to the auditor's own flag of 2026-09-17: Milgrom's exact deep-MOND virial sigma_los^4 = (4/81) G M a0
      RAISES the a0 a dispersion system needs by 81/16 = 5.06 relative to the framework's v = sqrt(2) sigma; it does not
      lower it.  Fornax and Coma computed both ways.

Every check states measurement and threshold; a FAIL is a finding; both a0 footings; no literal-True checks."""
import os, json, math
import sympy as sp

CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
G, MSUN, PC, AU, KMS = 6.674e-11, 1.989e30, 3.0857e16, 1.496e11, 1e3
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
print("L263 -- the real-mass phantom pincer: the equivalence principle versus the Oort limit\n")

# ------------------------------------------------------------------ A. the equivalence-principle identity
print("=" * 100); print("A. a uniform external field is unobservable to a real fluid (the hydrostatic identity)"); print("=" * 100)
x, y, z, gx, gy, gz, rho = sp.symbols('x y z g_x g_y g_z rho', real=True)
Phi = sp.Function('Phi')(x, y, z); p = sp.Function('p')(x, y, z)
X = sp.Matrix([x, y, z]); gext = sp.Matrix([gx, gy, gz])
hydro = lambda Ph: sp.Matrix([sp.diff(p, v) + rho * sp.diff(Ph, v) for v in (x, y, z)])
# in the frame falling freely with the fluid element the external potential -g_ext.x is removed by the frame acceleration:
# the equation of hydrostatic balance written in that frame differs from the lab-frame one by exactly rho * g_ext, which is
# the inertial force of the frame.  The RESIDUAL, star-only equation is identical in both frames.
lab = hydro(Phi - (gext.T * X)[0]); free = hydro(Phi) - rho * gext
check("A1 the hydrostatic equation in the freely falling frame equals the lab-frame equation with the uniform field removed (identity, all components)",
      all(sp.simplify(lab[i] - free[i]) == 0 for i in range(3)),
      "a real fluid's equilibrium around a star depends on the star's field and the tidal field only; |g_ext| does not enter")
# the tidal part that DOES act: |grad g_ext| r at r = 1 pc versus the Sun's own field there
R0, Mgal = 8.2e3 * PC, 1.0e11 * MSUN
g_ext = 2.32e-10; tidal_1pc = g_ext * (1 * PC) / R0 * 2   # order-of-magnitude tidal acceleration across 1 pc (log-potential ~ 2 g/R)
g_sun_1pc = G * MSUN / PC ** 2
print(f"    tidal acceleration across 1 pc from the Galaxy ~ {tidal_1pc:.1e} m/s^2; the Sun's own field at 1 pc = {g_sun_1pc:.1e} m/s^2 (ratio {tidal_1pc/g_sun_1pc:.2f})")
OUT["A"] = dict(tidal_1pc=tidal_1pc, g_sun_1pc=g_sun_1pc)

# ------------------------------------------------------------------ B. the uncapped solar phantom
print("\n" + "=" * 100); print("B. the uncapped deep-MOND phantom of a point mass: M_ph(<r) = M (r/r_M - 1)"); print("=" * 100)
Mvar, a0v, rv = sp.symbols('M a0 r', positive=True)
G_ = sp.Symbol('G', positive=True)
g_deep = sp.sqrt(G_ * Mvar * a0v) / rv
Mdyn = g_deep * rv ** 2 / G_
rM = sp.sqrt(G_ * Mvar / a0v)
ratio = sp.powsimp(sp.simplify(Mdyn / (Mvar * rv / rM)), force=True)
num_ok = all(abs(float((Mdyn - Mvar * rv / rM).subs({G_: g_, Mvar: m_, a0v: a_, rv: r_}))) < 1e-9 * float((Mvar * rv / rM).subs({G_: g_, Mvar: m_, a0v: a_, rv: r_}))
             for g_, m_, a_, r_ in ((1.0, 2.0, 3.0, 5.0), (6.674e-11, 1.989e30, 9.3619e-11, 3.0857e16), (0.3, 7.0, 0.11, 2.5)))
check("B1 M_dyn(<r) = M r/r_M and M_ph = M (r/r_M - 1) follow from g = sqrt(G M a0)/r (identity: symbolic ratio 1 and three numeric points to 1e-9)",
      sp.simplify(ratio - 1) == 0 or num_ok, f"ratio = {ratio}")
for lab_, a0 in A0.items():
    rMs = math.sqrt(G * MSUN / a0)
    Mph_1pc = (PC / rMs - 1)
    # the Sun's Jacobi radius in the Galactic log potential (v_c = 230 km/s at R0): r_J = R0 (M/(2 M_enc))^(1/3) with M_enc = v_c^2 R0/G
    Menc = (230 * KMS) ** 2 * R0 / G; rJ = R0 * (MSUN / (2 * Menc)) ** (1 / 3)
    Mph_rJ = (rJ / rMs - 1)
    print(f"    {lab_}: r_M(Sun) = {rMs/AU:.0f} AU = {rMs/PC:.4f} pc; M_ph(<1 pc) = {Mph_1pc:.1f} M_sun; Jacobi radius {rJ/PC:.2f} pc -> M_ph(<r_J) = {Mph_rJ:.1f} M_sun")
    OUT.setdefault("B", {})[lab_] = dict(rM_AU=rMs / AU, Mph_1pc=Mph_1pc, rJ_pc=rJ / PC, Mph_rJ=Mph_rJ)
check("B2 an uncapped solar phantom carries more than 10 M_sun inside the Sun's own tidal radius on both footings", all(v["Mph_rJ"] > 10 for v in OUT["B"].values()))

# ------------------------------------------------------------------ C. the local dark density versus the Oort limit
print("\n" + "=" * 100); print("C. every star carries one: the implied local dark density versus the Oort limit"); print("=" * 100)
n_star, m_mean = 0.10, 0.5          # local stellar number density (pc^-3) and mean stellar mass (M_sun), round numbers
rho_dm_local = (0.010, 0.015)        # M_sun/pc^3, the local dark-matter budget from vertical dynamics (Gaia-era)
for lab_, a0 in A0.items():
    rMm = math.sqrt(G * m_mean * MSUN / a0)
    rJm = R0 * (m_mean * MSUN / (2 * Menc)) ** (1 / 3)
    r_half = 0.5 * n_star ** (-1 / 3) * PC                    # half the mean separation: halos overlap beyond this
    r_cut = min(rJm, r_half)
    Mph = m_mean * (r_cut / rMm - 1)
    rho_dark = n_star * Mph
    print(f"    {lab_}: a {m_mean} M_sun star: r_M = {rMm/AU:.0f} AU; cut radius min(r_J = {rJm/PC:.2f} pc, half-separation = {r_half/PC:.2f} pc) = {r_cut/PC:.2f} pc; "
          f"M_ph(<cut) = {Mph:.1f} M_sun; rho_dark = n_* M_ph = {rho_dark:.2f} M_sun/pc^3 vs the Oort dark budget {rho_dm_local[0]}-{rho_dm_local[1]} ({rho_dark/rho_dm_local[1]:.0f}x)")
    OUT.setdefault("C", {})[lab_] = dict(rho_dark=rho_dark, factor_over_budget=rho_dark / rho_dm_local[1])
check("C1 the SEP-respecting real-mass phantom implies a local dark density within the Oort-limit dark budget (factor < 3) on either footing",
      any(v["factor_over_budget"] < 3 for v in OUT["C"].values()),
      f"factors {[round(v['factor_over_budget']) for v in OUT['C'].values()]}x over the budget: the uncapped halos of ordinary stars are excluded by the vertical dynamics of the solar neighbourhood. [FAIL is the finding]")

# ------------------------------------------------------------------ D. the dichotomy
print("\n" + "=" * 100); print("D. the dichotomy: capped by |g_ext| (SEP-violating field response, L243) or real mass (Oort-dead)"); print("=" * 100)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def rd(rel):
    p_ = os.path.join(REPO, rel); return open(p_, errors="replace").read() if os.path.exists(p_) else ""
g086, solar, l243 = rd("deepseek_push/G086_relatvistic_face.out") or rd("deepseek_push/G086_relativistic_face.out"), rd("deepseek_push/SOLAR_FACE_CLOSEOUT.md"), rd("fable_independent_2026/L243_onefunction_cassini_quadrupole.out")
realmass = "ORDINARY MATTER" in g086
capped = ("EFE-capped" in solar) or ("g_ext" in solar)
import re
q2 = re.search(r"canonical (\d+\.\d+)x ceiling", l243)
print(f"    G086: the sector is 'ORDINARY MATTER (p = 0)' -> {realmass};  SOLAR_FACE_CLOSEOUT: the solar phantom is 'EFE-capped' by the Galactic field -> {capped};  L243: the field-response quadrupole = {q2.group(1) if q2 else '?'}x the Cassini ceiling")
check("D1 the record's two properties of the phantom -- real mass (PPN = GR by the SEP) and capped by |g_ext| (the SEP violated) -- are held by the same object",
      not (realmass and capped), "both held: a real fluid cannot be capped by a uniform field (A1), and an uncapped real halo fails the Oort limit (C1); a cappable phantom is a field response and carries L243's quadrupole. NO THIRD READING. [FAIL is the finding]")

# ------------------------------------------------------------------ E. the sigma-conversion correction (auditor's own error, 2026-09-17)
print("\n" + "=" * 100); print("E. correction: Milgrom's deep-MOND virial RAISES the a0 a dispersion system needs (x 81/16 = 5.06); it does not lower it"); print("=" * 100)
systems = {"Fornax dSph (sigma 11.7 km/s, M_b 2e7)": (11.7 * KMS, 2e7 * MSUN), "Coma (sigma 1000 km/s, M_b 2e14)": (1000 * KMS, 2e14 * MSUN)}
for name, (sig, Mb) in systems.items():
    a0_fw = 4 * sig ** 4 / (G * Mb)                # framework: sigma = v/sqrt2, v^4 = G M a0
    a0_mil = (81 / 4) * sig ** 4 / (G * Mb)        # Milgrom 1994 isotropic deep-MOND virial: sigma_los^4 = (4/81) G M a0
    print(f"    {name}: required a0 -- framework conversion {a0_fw/A0['canonical']:.2f} x a0_DE; deep-MOND virial {a0_mil/A0['canonical']:.2f} x a0_DE (ratio {a0_mil/a0_fw:.2f})")
    OUT.setdefault("E", {})[name] = dict(a0_fw=a0_fw / A0["canonical"], a0_mil=a0_mil / A0["canonical"])
check("E1 the deep-MOND virial coefficient multiplies the required a0 by 81/16 = 5.0625 exactly (so the 09-17 flag's direction was wrong)",
      all(abs(v["a0_mil"] / v["a0_fw"] - 81 / 16) < 1e-9 for v in OUT["E"].values()),
      "Fornax at 0.3 x a0_DE (framework) -> 1.5 x (Milgrom): the isolated deep virial puts Fornax near the line; Coma 1.6 -> 8.1 x (the known MOND cluster deficit, ~2.8 in mass)")
check("E2 under BOTH conventions a single a0 places Fornax and Coma on one line within a factor 2", all(abs(math.log10(v["a0_mil"])) < math.log10(2) for v in OUT["E"].values()) or all(abs(math.log10(v["a0_fw"])) < math.log10(2) for v in OUT["E"].values()),
      "no: the dispersion channels are not on one line under either conversion; the per-object Jeans treatment (FIFTY item 3, IDEAS_100 item 1) is required. [FAIL is the finding]")

n, n_pass = len(CH), sum(CH)
print(f"\nL263 COMPLETE: {n_pass}/{n} checks PASS.  VERDICT: the real-mass reading of the phantom is closed by the equivalence principle and the Oort")
print("limit (a real fluid cannot be capped by a uniform field; uncapped, every star carries ~20 M_sun inside its tidal radius, 100x the local dark")
print("budget); the cappable reading is the field response L243 kills.  The two readings the record splices are each dead on its own.")
json.dump(dict(pass_=n_pass, n=n, parts=OUT), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "L263_results.json"), "w"), indent=1, default=str)
