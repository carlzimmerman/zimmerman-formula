#!/usr/bin/env python3
r"""
MICROSCOPE / WEP vs the de Sitter-Unruh MODIFIED-INERTIA action:  is eta = 0 STRUCTURAL?
=========================================================================================
ROLE in the precision-consistency ledger: the Eotvos parameter at ~1e-15.

SOURCES READ (verbatim, not re-derived here):
  * real_research/papers/MI_FIELD_THEORY_RESULTS_2026.md  Sec. 2.1-2.2, 5.1-5.4, 7.4
        S = S_EH[g] + S_u[g,u,lambda] + S_matter[g,u,psi;K] + S_photon[gtilde]
        S_matter = -(1/2) \int sqrt(-g) rho_m [ s u^mu K(Box_u/a0^2) u_mu ]
        K(z) = (sqrt(1+4z)-1)/(2 sqrt z),   X = |a|^2/a0^2,   u_mu Box_u u^mu = -|a|^2
        "WEP is exact: eta = 0, derived.  ... Machine check: eta < 1e-12 over y in [1e-2,1e2]"
        ledger row N3: "eta = 0 exactly" vs eta_meas = (-1.5 +- 2.3)e-15  -> "pass, 0.65 sigma"
        gate: G(omega) = 1/(1 + i omega/omega_c),  omega_c in [1.78,2.21]e-14 rad/s (canon)
                                                   omega_c in [1.78,1.83]e-14 rad/s (alt)
  * real_research/reviews/mi_cassini_q2_omegac_2026.py   Re G / Im G, Forks A/B/C
        Fork C: "a low-pass gate cannot suppress a DC anomaly at any corner" (Re G(0) = 1).
  * prep_2026/mi_field_theory/matter_coupling_Tmunu.py  Sec. [1a]  (the actual eta "check")

WHAT THIS SCRIPT DOES (three questions, in order):
  (a) STRUCTURE. Is eta = 0 exact-by-construction from S_matter, or only approximate?  Answered by
      identifying WHERE a species label could enter, parametrising each channel, and computing the
      resulting eta -- including the one reading that genuinely WOULD carry composition dependence.
  (b) THE 1e-12 GAP. What is the "residual < 1e-12" actually a residual OF?  (Audited at source.)
  (c) NUMBERS. eta_gated (AC, with the real Re G) and eta_DC (no gate) vs MICROSCOPE, both a0 footings.

CALIBRATION HELD THROUGHOUT (manufacture neither a win nor a deficit):
  * "Suppressed by 10^N, no constraint" is an HONEST result for the AC channel and is reported with N.
  * The DC channel is NOT granted a free pass: every composition handle that could carry the dressing
    is computed from nuclear data and confronted with the published bound.  Where an O(1) coupling is
    excluded, the number of orders is stated.
  * Both a0 footings on every dimensional number.
  * No TOE language.  No "theory closed".  numpy + sympy + mpmath.  Exits 0.
"""
import numpy as np
import sympy as sp
import mpmath as mp

mp.mp.dps = 60

RULE = "=" * 104
def head(s): print("\n" + RULE + "\n" + s + "\n" + RULE)
NCHK = [0, 0]
def check(msg, ok):
    NCHK[0] += 1
    NCHK[1] += bool(ok)
    print(f"   [{'PASS' if ok else 'FAIL':4}] {msg}")
    assert ok, "FAILED: " + msg

# ---------------------------------------------------------------------------------------------------
# 0. CONSTANTS -- framework footings and the cited experimental anchors
# ---------------------------------------------------------------------------------------------------
A0 = {"canon": 9.355e-11,   # a0 = c H_Lambda / Z, Z = sqrt(32 pi/3)   [pure-Lambda footing]
      "alt":   1.13e-10}    # rho_total / c H0 footing

# MICROSCOPE final result: Touboul et al., PRL 129, 121102 (2022); pair = Ti alloy (TA6V) vs Pt alloy (PtRh10)
ETA_CEN, ETA_STAT, ETA_SYST = -1.5e-15, 2.3e-15, 1.5e-15
ETA_TOT = np.hypot(ETA_STAT, ETA_SYST)                  # 1 sigma, stat (+) syst in quadrature
ETA_1SIG = ETA_STAT                                     # the paper's own ledger row uses +-2.3e-15
ETA_2SIG = abs(ETA_CEN) + 2 * ETA_TOT                   # conservative two-sided 2 sigma ceiling

GM_E, R_E, H_ORB = 3.986004418e14, 6.378137e6, 710.0e3  # MICROSCOPE: sun-synchronous, 710 km
R_ORB = R_E + H_ORB
G_ORB = GM_E / R_ORB ** 2                               # the test masses' kinematic acceleration
T_ORB = 2 * np.pi * np.sqrt(R_ORB ** 3 / GM_E)

# EP-signal frequencies actually used in flight: f_EP = f_orb + f_spin.
# [ADOPTED] inertial-pointing (f_spin = 0) and the two spin sessions; the verdict is insensitive
# across this entire decade (shown explicitly in Sec. 5).
F_EP_HZ = {"inertial (f_orb)": 1.0 / T_ORB, "spin V2 (0.925 mHz)": 0.925e-3, "spin V3 (3.11 mHz)": 3.11e-3}

# the framework's own gate window (paper Sec. 5.2) and its own forced corner (Sec. 5.3)
WINDOW = {"canon": (1.78e-14, 2.21e-14), "alt": (1.78e-14, 1.83e-14)}
def OMEGA_C_FORCED(a0): return a0 / (2 * 2.99792458e8)   # a0/2c: the action's OWN memory corner

# galactic external field at the Sun (used by the EFE / Fork-G reading only)
G_EXT_GAL = (233e3) ** 2 / (8.2 * 3.0857e19)             # ~2.15e-10 m/s^2

# ---------------------------------------------------------------------------------------------------
# 1. THE GATE  (form taken verbatim from the paper / the Cassini script -- not adopted by me)
# ---------------------------------------------------------------------------------------------------
def ReG(omega, wc): return 1.0 / (1.0 + (omega / wc) ** 2)
def invert_ReG(S):  return np.sqrt(1.0 / S - 1.0)        # omega/omega_c at which Re G = S

head("1.  THE GATE, AND THE ONE PROPERTY THAT MAKES THIS LEDGER NON-TRIVIAL")
w, wc = sp.symbols("omega omega_c", positive=True)
Gs = 1 / (1 + sp.I * w / wc)
ident = sp.simplify(sp.Abs(Gs) ** 2 - sp.re(sp.expand(sp.simplify(Gs))))
print(f"""
  G(omega) = 1/(1 + i omega/omega_c);   Re G = 1/(1 + (omega/omega_c)^2)  = RETAINED MI amplitude.
  omega_c in [1.78, 2.21]e-14 rad/s (canon) <-> a period of {2*np.pi/2.21e-14/(3.156e7*1e6):.2f}-{2*np.pi/1.78e-14/(3.156e7*1e6):.2f} Myr.
  EVERY MICROSCOPE frequency is 10^10-10^12 times ABOVE that corner, so the AC channel is gated OFF
  by ~20+ orders.  The whole informational value of this lane therefore sits in Fork C:""")
check("sympy: the 1-pole identity |G|^2 = Re G holds (residual 0)", sp.simplify(ident) == 0)
check("Fork C: Re G(omega=0) = 1 for EVERY omega_c in the window (a low-pass gate cannot "
      "suppress a DC anomaly)", all(abs(ReG(0.0, wcv) - 1.0) < 1e-15
                                    for wcv in (1.78e-14, 2.21e-14, 1e-30, 1e30)))

# ---------------------------------------------------------------------------------------------------
# 2. (b) THE 1e-12 GAP -- audited at source
# ---------------------------------------------------------------------------------------------------
head("2.  (b) WHAT IS THE 'residual < 1e-12' A RESIDUAL OF?   [source audit, load-bearing]")
xs, ys = sp.symbols("x y", positive=True)
K_of_xsq = (sp.sqrt(1 + 4 * xs ** 2) - 1) / (2 * xs)      # mu_fw(x) = K(x^2)
x_phys = ys * sp.sqrt(1 + 1 / ys)                         # x = y nu(y)

# reproduce, line for line, the two checks that matter_coupling_Tmunu.py Sec.[1a] actually runs
residual_sym = sp.simplify(1 + 4 * x_phys ** 2 - (2 * ys + 1) ** 2)
bal = [abs(float((K_of_xsq.subs(xs, x_phys) * x_phys - ys).subs(ys, yv)))
       for yv in (sp.Rational(1, 100), sp.Rational(1, 10), 1, 10, 100)]
eta_AB_as_written = x_phys - x_phys        # <-- verbatim the script's eta check: expression minus itself

print(f"""
  matter_coupling_Tmunu.py Sec.[1a] runs exactly TWO checks.  Reproduced here:

   CHECK 1  "balance mu_fw(x) x = y solved by x = y nu(y) ... residual < 1e-12 over y in [1e-2,1e2]"
            symbolic collapse 1 + 4x^2 - (2y+1)^2 = {residual_sym}   (EXACT, zero)
            float residuals of  K(x^2) x - y  at y = 1e-2 .. 1e2 :  max = {max(bal):.3e}
            -> the "< 1e-12" is a FLOAT TOLERANCE on an ALGEBRAIC INVERSION IDENTITY, and that
               identity is separately proven EXACTLY (symbolic residual is literally 0).

   CHECK 2  "eta = (a_A - a_B)/a_avg = 0 EXACTLY"   is coded as   eta_AB = x_phys - x_phys
            i.e. one expression minus ITSELF.  Value = {eta_AB_as_written}.  It is a TAUTOLOGY:
            it cannot fail for any theory, kernel, or footing, so it verifies nothing about eta.

  CONSEQUENCE, stated plainly (this is a documentation error, not a physics error):
    * the paper's sentence "Machine check: eta < 1e-12" (Sec. 2.2) and MATTER_COUPLING.md line 37
      MIS-ATTRIBUTE Check 1's float tolerance to eta.  1e-12 is NOT a bound on eta and NOT a
      theoretical uncertainty -- it is double-precision noise on a different, exactly-proven identity.
    * so MICROSCOPE does NOT "probe below the theory's own verified precision".  There is no 1e-12
      theory error bar to be 1000x looser than 1e-15.  The comparison is not 1e-12 vs 1e-15 at all.
    * BUT the eta = 0 claim currently has NO discriminating machine verification.  It sits in exactly
      the category the paper says it audited ("two previously tautological checks ... were replaced");
      this one survived the audit.  Sections 3-4 below supply a genuine one.
""")
check("CHECK 1 reproduced: symbolic residual 1+4x^2-(2y+1)^2 is EXACTLY 0", residual_sym == 0)
check("CHECK 1 reproduced: float residual of the balance is at double-precision noise "
      f"(max {max(bal):.1e} <= 1e-12), i.e. the 1e-12 is a TOLERANCE not an eta bound", max(bal) <= 1e-12)
check("CHECK 2 reproduced: the shipped eta check is `x_phys - x_phys` == 0, a TAUTOLOGY "
      "(zero discriminating power)", sp.simplify(eta_AB_as_written) == 0)

# ---------------------------------------------------------------------------------------------------
# 3. (a) WHERE COULD A SPECIES LABEL ENTER?  -- structural analysis of S_matter
# ---------------------------------------------------------------------------------------------------
head("3.  (a) STRUCTURE: the three places a composition label could enter S_matter, enumerated")
print(r"""
  S_matter = -(1/2) \int sqrt(-g) rho_m [ s u^mu K(Box_u/a0^2) u_mu ]  ==  -(1/2) \int sqrt(-g) rho_m W[u,g]

  The term is a PRODUCT of exactly two objects:
      (i)  W[u,g] = s u.K(Box_u/a0^2).u  -- a functional of (u, g, partial u) ONLY.  No matter field
           psi appears in it; expanding K = sum_n c_n (Box_u/a0^2)^n adds only more (u,g) structure at
           every order n, so W is species-blind TO ALL ORDERS in the kernel, not just at leading order.
      (ii) rho_m -- ONE composition-blind scalar, and the SAME rho_m that carries the passive
           gravitational mass (it is the only matter density in the action; T_munu's alpha, beta,
           gamma are all strictly proportional to it, paper Sec. 2.2).

  Therefore in the test-body balance the factor rho_m appears on BOTH sides and cancels identically:
        inertial side  rho_m mu_fw(x) x a0     =     gravitational side  rho_m g_bar
  leaving  mu_fw(x) x = y  -- an equation with NO free parameter that a body could carry.
  This is the structural content of "eta = 0".  It is exact, and it is exact for a reason that is
  checkable rather than asserted: THERE IS NO THIRD OBJECT IN THE TERM.

  Three (and only three) channels could break it.  Each is parametrised and computed below.

   CH-1  AMPLITUDE channel.  the MI DEFORMATION carries a species factor:
              1 - K  ->  (1 + lambda q_A)(1 - K)              [Newtonian limit stays universal]
   CH-2  ARGUMENT channel.  the SCALE inside the kernel is species-dependent:
              a0 -> a0 (1 + lambda q_A)   (equivalently X -> X/(1+lambda q_A)^2)
   CH-3  RESOLUTION channel.  the kernel resolves the body's INTERNAL accelerations, i.e. it is
         applied CONSTITUENT-WISE:  m_I = sum_i m_i K(|a_cm + a_i^int|/a0)   instead of to the
         centre-of-mass worldline.  This is the only channel that is not a bolt-on: it is what a
         modified-INERTIA theory does if |a| is read microscopically.  Section 4.3 computes it.
""")

# --- CH-1 / CH-2: exact two-species solve, then the closed form, then MICROSCOPE ---------------------
lam, q = sp.symbols("lambda q", real=True)
Kx = (sp.sqrt(1 + 4 * xs ** 2) - 1) / (2 * xs)
eq_ch1 = sp.expand(xs * (1 - (1 + lam * q) * (1 - Kx)) - ys)      # CH-1 balance
eq_ch1_l0 = sp.simplify(eq_ch1.subs(lam, 0))
check("CH-1 at lambda=0: the balance equation contains NO species symbol q "
      "(q not in free_symbols) -> the two species solve the IDENTICAL equation",
      q not in eq_ch1_l0.free_symbols and sp.simplify(eq_ch1_l0 - (Kx * xs - ys).expand()) == 0)
check("CH-1 negative control at lambda!=0: q DOES enter the balance (so the test above is "
      "discriminating, not vacuous)", q in sp.expand(eq_ch1.subs(lam, sp.Rational(1, 3))).free_symbols)

def solve_x(y, eps, mode="CH1"):
    """Exact high-precision root of the species-dressed balance.  eps = lambda * q."""
    y, eps = mp.mpf(y), mp.mpf(eps)
    if mode == "CH1":   # x*(1 - (1+eps)(1-K(x))) = y
        f = lambda x: x * (1 - (1 + eps) * (1 - (mp.sqrt(1 + 4 * x ** 2) - 1) / (2 * x))) - y
    else:               # CH-2: K(x/(1+eps)) * x = y  with x = |a|/a0
        f = lambda x: ((mp.sqrt(1 + 4 * (x / (1 + eps)) ** 2) - 1) / (2 * (x / (1 + eps)))) * x - y
    return mp.findroot(f, y + mp.mpf(1) / 2)

def eta_exact(y, dq, lamv, mode="CH1"):
    xA, xB = solve_x(y, lamv * dq / 2, mode), solve_x(y, -lamv * dq / 2, mode)
    return float(2 * (xA - xB) / (xA + xB))

y_micro = {k: G_ORB / v for k, v in A0.items()}
print(f"\n  MICROSCOPE regime:  g_orb = GM_E/(R_E+710km)^2 = {G_ORB:.5f} m/s^2 ,  T_orb = {T_ORB:.0f} s")
for k in A0:
    print(f"    footing {k:<6} a0 = {A0[k]:.4e}  ->  y = g_orb/a0 = {y_micro[k]:.4e} ,  "
          f"MI deformation 1-K = a0/(2 g_orb) = {A0[k]/(2*G_ORB):.4e}")
# closed form vs exact numerics (the genuine verification)
print("\n  CLOSED FORM (derived): at y >> 1 the balance gives  x = y + (1 + lambda q)/2 , hence")
print("      a = g_bar + a0/2 + lambda q a0/2   =>   eta = lambda * Delta_q * a0/(2 g_bar) .")
print("  Verified against the EXACT mp.findroot solve (dps=60), both channels:\n")
print(f"  {'channel':<8}{'footing':<8}{'lambda':>8}{'Delta q':>10}{'eta closed-form':>18}{'eta exact solve':>18}{'rel diff':>12}")
print("  " + "-" * 82)
worst_rel = 0.0
for mode in ("CH1", "CH2"):
    for f_ in ("canon", "alt"):
        for lamv, dqv in ((1.0, 1e-3), (0.1, 7.5e-4)):
            cf = lamv * dqv * A0[f_] / (2 * G_ORB)
            ex = eta_exact(y_micro[f_], dqv, lamv, mode)
            rel = abs(ex / cf - 1)
            worst_rel = max(worst_rel, rel)
            print(f"  {mode:<8}{f_:<8}{lamv:>8.2f}{dqv:>10.2e}{cf:>18.4e}{ex:>18.4e}{rel:>12.2e}")
check(f"closed form eta = lambda Delta_q a0/(2 g) matches the exact numerical solve to "
      f"{worst_rel:.1e} relative, for BOTH channels and BOTH footings", worst_rel < 1e-5)
check("CH-1 and CH-2 give the SAME leading eta (the amplitude and argument channels are "
      "degenerate at y >> 1)", abs(eta_exact(y_micro['canon'], 1e-3, 1.0, 'CH1') /
                                   eta_exact(y_micro['canon'], 1e-3, 1.0, 'CH2') - 1) < 1e-5)
check("lambda = 0 gives eta identically 0 in the exact solve (not by construction: two "
      "independent root-finds subtracted)", eta_exact(y_micro['canon'], 1e-3, 0.0) == 0.0)

# ---------------------------------------------------------------------------------------------------
# 4. COMPOSITION CONTRASTS FROM NUCLEAR DATA -- the actual Pt/Ti numbers
# ---------------------------------------------------------------------------------------------------
head("4.  THE COMPOSITION HANDLES q, computed from nuclear data for the FLIGHT test masses")
M_H, M_N, U_MEV = 1.00782503207, 1.00866491600, 931.494061
# element -> (Z, [(A, atomic mass u, atomic abundance fraction), ...])
ISO = {
    "Ti": (22, [(46, 45.952628, .0825), (47, 46.951758, .0744), (48, 47.947941, .7372),
                (49, 48.947870, .0541), (50, 49.944792, .0518)]),
    "Al": (13, [(27, 26.981539, 1.0)]),
    "V":  (23, [(50, 49.947159, .0025), (51, 50.943960, .9975)]),
    "Pt": (78, [(190, 189.959930, .00012), (192, 191.961035, .00782), (194, 193.962664, .3286),
                (195, 194.964774, .3378), (196, 195.964935, .2521), (198, 197.967876, .0736)]),
    "Rh": (45, [(103, 102.905504, 1.0)]),
}
# MICROSCOPE SUEP test masses: inner = PtRh10 (Pt 90 / Rh 10 wt%), outer = TA6V (Ti 90 / Al 6 / V 4 wt%)
ALLOY = {"PtRh10 (inner)": {"Pt": .90, "Rh": .10}, "TA6V (outer)": {"Ti": .90, "Al": .06, "V": .04}}

def element_handles(el):
    Z, iso = ISO[el]
    mtot = sum(a * m for _, m, a in iso)
    out = dict(B=0.0, ZA=0.0, NZ=0.0, BAR=0.0)
    for A, m, ab in iso:
        wf = ab * m / mtot                                    # mass fraction of this isotope
        B = (Z * M_H + (A - Z) * M_N - m)                      # mass defect in u
        out["B"] += wf * (B / m)                               # nuclear binding energy / rest mass
        out["ZA"] += wf * (Z / m)                              # electrons (charge) per unit mass [1/u]
        out["NZ"] += wf * ((A - 2 * Z) / A)                    # neutron excess (N-Z)/A
        out["BAR"] += wf * (A / m)                             # baryons per unit mass [1/u]
    return out

# ---- the OTHER solar-system ceilings on omega_c, RECOMPUTED here (not quoted) so the ranking in
# ---- Section 8 is derived.  Same inputs as mi_cassini_q2_omegac_2026.py Sec.2/5.
YR = 365.25 * 86400.0
GM_SUN, GM_MOON_HOST, R_MOON, A_SAT = 1.32712440018e20, 3.986004418e14, 3.844e8, 1.43353e12
OMEGA_SAT = 2 * np.pi / (10759.22 * 86400.0)
GDOT_LLR_2SIG, DG_SATURN, BOOST_BOUND_95 = (5.0 + 2 * 9.6) * 1e-15, 7.0e-15, 0.02
def nu_frame(y): return np.sqrt(1.0 + 1.0 / y)
WC_LLR = (GDOT_LLR_2SIG / YR) * (GM_MOON_HOST / R_MOON ** 2) / A0["canon"]
WC_SAT_REACT = OMEGA_SAT * np.sqrt(2 * DG_SATURN / A0["canon"])
WC_Q2 = OMEGA_SAT / np.sqrt(1.0 / (BOOST_BOUND_95 / (nu_frame(G_EXT_GAL / A0["canon"]) - 1)) - 1.0)

HANDLE_NAME = {"B": "nuclear binding E / mc^2", "ZA": "charge per mass Z/M [1/u]",
               "NZ": "neutron excess (N-Z)/A", "BAR": "baryon number per mass A/M [1/u]"}
alloy_h = {}
for name, comp in ALLOY.items():
    h = {k: 0.0 for k in ("B", "ZA", "NZ", "BAR")}
    for el, wf in comp.items():
        eh = element_handles(el)
        for k in h:
            h[k] += wf * eh[k]
    alloy_h[name] = h
print(f"\n  {'handle q':<28}{'PtRh10 (inner)':>18}{'TA6V (outer)':>16}{'|Delta q|':>14}")
print("  " + "-" * 78)
DQ = {}
for k in ("B", "ZA", "NZ", "BAR"):
    a_, b_ = alloy_h["PtRh10 (inner)"][k], alloy_h["TA6V (outer)"][k]
    DQ[k] = abs(a_ - b_)
    print(f"  {HANDLE_NAME[k]:<28}{a_:>18.6f}{b_:>16.6f}{DQ[k]:>14.4e}")
check("nuclear binding fraction reproduces the textbook Ti-48 value 9.375e-3 to <1e-4",
      abs((22*M_H + 26*M_N - 47.947941)/47.947941 - 9.3748e-3) < 1e-4)
check("Delta q (binding) is O(1e-3) and Delta q (neutron excess / charge) is O(0.1) -- the Pt/Ti "
      "pair was chosen for exactly this contrast", 3e-4 < DQ["B"] < 3e-3 and DQ["NZ"] > 5e-2)

# ---------------------------------------------------------------------------------------------------
# 5. (c) THE TWO PREDICTIONS: gated (AC) and DC, vs MICROSCOPE
# ---------------------------------------------------------------------------------------------------
head("5.  (c) THE LEDGER LINES -- eta_gated (AC, real Re G) and eta_DC (no gate), both footings")
print(f"""
  MICROSCOPE (Touboul+ 2022, PRL 129:121102), Ti/Pt pair:
      eta = ({ETA_CEN/1e-15:+.1f} +- {ETA_STAT/1e-15:.1f}_stat +- {ETA_SYST/1e-15:.1f}_syst) e-15 ;  sigma_tot = {ETA_TOT:.2e}
      ceilings used:  1 sigma (the paper's own ledger row) |eta| <= {ETA_1SIG:.2e}
                      2 sigma (conservative)               |eta| <= {ETA_2SIG:.2e}

  FRAMEWORK PREDICTION, written action as it stands:  eta = 0 EXACTLY (Sec. 3 above, structural).
  Both channels below therefore report what MICROSCOPE bounds on the DEFORMATION coupling lambda,
  i.e. how much composition-dependence the data still allows -- not a framework deficit.

  [ADOPTED] frequency argument = the same rule the paper uses everywhere else (Cassini script
  ADOPTED #1): the gate is evaluated at the frequency of the MEASURED signal.  For MICROSCOPE the
  EP signal is the projection of the Earth-pointing acceleration on the measurement axis, at
  f_EP = f_orb + f_spin.  A DC-in-inertial-space Earthward MI bias lands in EXACTLY that bin, which
  is why Fork C is the live question here and not an academic one.
""")
print(f"  gate suppression Re G at the EP frequencies, at the window's MOST PERMISSIVE corner:")
print(f"  {'EP mode':<24}{'f_EP [Hz]':>12}{'omega_EP':>12}{'ReG @2.21e-14':>16}{'ReG @1.78e-14':>16}{'ReG @ a0/2c':>14}")
print("  " + "-" * 96)
REG = {}
for nm, f in F_EP_HZ.items():
    om = 2 * np.pi * f
    REG[nm] = (om, ReG(om, 2.21e-14), ReG(om, 1.78e-14), ReG(om, OMEGA_C_FORCED(A0["canon"])))
    print(f"  {nm:<24}{f:>12.4e}{om:>12.4e}{REG[nm][1]:>16.3e}{REG[nm][2]:>16.3e}{REG[nm][3]:>14.3e}")
OM_EP_MIN = min(v[0] for v in REG.values())
REG_MAX = max(v[1] for v in REG.values())          # most permissive suppression over all EP modes
print(f"""
  Most permissive suppression anywhere in the window and over all EP modes: Re G = {REG_MAX:.3e}
  -> the AC channel is gated off by {-np.log10(REG_MAX):.1f} ORDERS.  Reported, not hand-waved.
""")

print("  THE TWO LEDGER LINES (lambda = 1, i.e. an O(1) composition coupling of the MI deformation):\n")
print(f"  {'handle':<26}{'footing':<7}{'1-K':>11}{'eta_DC (lam=1)':>17}{'DC vs bound':>14}"
      f"{'eta_AC gated':>15}{'AC vs bound':>14}{'lambda_max(DC)':>16}")
print("  " + "-" * 122)
LEDGER = []
for k in ("B", "ZA", "NZ"):
    for f_ in ("canon", "alt"):
        defo = A0[f_] / (2 * G_ORB)                  # 1 - K at MICROSCOPE (Fork L, local field)
        eta_dc = DQ[k] * defo                        # lambda = 1
        eta_ac = eta_dc * REG_MAX
        lam_max = ETA_1SIG / eta_dc
        LEDGER.append((k, f_, defo, eta_dc, eta_ac, lam_max))
        print(f"  {HANDLE_NAME[k]:<26}{f_:<7}{defo:>11.3e}{eta_dc:>17.3e}"
              f"{eta_dc/ETA_1SIG:>13.2e}x{eta_ac:>15.3e}{eta_ac/ETA_1SIG:>13.2e}x{lam_max:>16.3e}")
print(f"""
  Reading the columns:  "vs bound" > 1 means EXCLUDED by that factor at 1 sigma; < 1 means allowed.
  lambda_max(DC) = the largest composition coupling the DC channel may carry and still satisfy
  MICROSCOPE at 1 sigma.  The written action has lambda = 0 identically (Sec. 3).
""")

# ---------------------------------------------------------------------------------------------------
# 5b. THE COMMON-MODE DC PIECE: is it visible at all?
# ---------------------------------------------------------------------------------------------------
head("5b.  THE COMMON-MODE DC PIECE -- an extra a0/2 Earthward.  Why MICROSCOPE cannot see it.")
ECC = 5e-3   # MICROSCOPE orbit eccentricity, near-circular (order of magnitude)
for f_ in ("canon", "alt"):
    a0h = A0[f_] / 2
    print(f"    {f_:<6} DC bias = a0/2 = {a0h:.3e} m/s^2 Earthward, COMMON to both masses "
          f"= {a0h/G_ORB:.3e} of g_orb")
    print(f"           differential resolution of MICROSCOPE = eta_1sig * g = {ETA_1SIG*G_ORB:.3e} m/s^2 "
          f"-> the common-mode piece is {a0h/(ETA_1SIG*G_ORB):.2e}x LARGER")
    print(f"           but (a0/2)/g_orb is CONSTANT on a near-circular orbit -> exactly degenerate with "
          f"GM_E; non-degenerate residual ~ 2e * (a0/2g) = {2*ECC*a0h/G_ORB:.2e} (still common mode)")
print("""
  So the absolute/common-mode DC piece is invisible to MICROSCOPE for a STRUCTURAL reason, not an
  instrumental one: a constant additive Earthward acceleration at fixed orbital radius is 100%
  absorbable into GM_E, and MICROSCOPE measures a DIFFERENCE.  (Contrast the solar system, where the
  paper's own Sec. 5.1 shows the same a0/2 tail is NOT GM-absorbable because the induced precession
  scales as sqrt(a) across planets -- that is why the ephemerides bite and MICROSCOPE does not.)
  MICROSCOPE's leverage on the DC channel is therefore entirely in its STRUCTURE sector (lambda).
""")

# ---------------------------------------------------------------------------------------------------
# 5c. FORK L vs FORK G -- which acceleration sets the deformation?
# ---------------------------------------------------------------------------------------------------
head("5c.  FORK on the kernel argument (the MICROSCOPE analogue of the Cassini Fork A/B/C)")
def one_minus_K(y):
    y = mp.mpf(y); x = mp.sqrt(y**2 + y); return float(1 - y / x)
defo_L = {f_: one_minus_K(y_micro[f_]) for f_ in A0}
defo_G = {f_: one_minus_K(G_EXT_GAL / A0[f_]) for f_ in A0}
print(f"""
  FORK L [LOCAL, the paper's own reading -- "the body's OWN 4-acceleration"]
      X set by the test mass's total kinematic acceleration g_orb = {G_ORB:.4f} m/s^2
      1 - K = {defo_L['canon']:.4e} (canon) / {defo_L['alt']:.4e} (alt)
      The signal direction IS the Earth-pointing EP direction -> lands in the published f_EP bin.
      This is the CLEAN reading and it owns the verdict.

  FORK G [EFE / external-field, the reading that makes Cassini Q2 dangerous]
      X set instead by the galactic external field g_ext = {G_EXT_GAL:.3e} m/s^2 (y = {G_EXT_GAL/A0['canon']:.2f})
      1 - K = {defo_G['canon']:.4e} (canon) / {defo_G['alt']:.4e} (alt)  -- {defo_G['canon']/defo_L['canon']:.1e}x LARGER
      lambda_max under Fork G (neutron-excess handle, 1 sigma):
          canon {ETA_1SIG/(DQ['NZ']*defo_G['canon']):.3e}    alt {ETA_1SIG/(DQ['NZ']*defo_G['alt']):.3e}
      i.e. an O(1) composition coupling would be excluded by
          {DQ['NZ']*defo_G['canon']/ETA_1SIG:.2e}x  = {np.log10(DQ['NZ']*defo_G['canon']/ETA_1SIG):.1f} orders.
  [ASSUMPTION, WEIGHT REDUCED]  Under Fork G the differential sits along a fixed INERTIAL direction,
  hence at f_spin, not at f_EP = f_orb + f_spin.  The published eta is an f_EP amplitude, so the
  Fork-G number is indicative of the scale, not a literal use of the published bound.  The verdict
  below is quoted on FORK L only.  Recording Fork G because it is the same fork the Cassini lane has.
""")

# ---------------------------------------------------------------------------------------------------
# 6. CH-3: the RESOLUTION channel -- the one reading that genuinely carries composition
# ---------------------------------------------------------------------------------------------------
head("6.  CH-3 THE RESOLUTION CHANNEL -- if the kernel resolved INTERNAL accelerations")
# representative internal accelerations of the constituents of a solid
M_NUC, M_EL = 1.6749e-27, 9.10938e-31
A_NUC = (8.0e6 * 1.602177e-19) / (2.0e-15) / M_NUC     # nuclear force scale: 8 MeV over 2 fm
A_ATOM = (13.6 * 1.602177e-19) / (0.529e-10) / M_EL    # atomic binding: 13.6 eV over a_Bohr
A_PHON = (1.0e13) ** 2 * 1.0e-11                       # Debye phonon: omega^2 * amplitude
print(f"""
  If  m_I = sum_i m_i K(|a_i|/a0)  with |a_i| the CONSTITUENT accelerations, then the body's MI
  deformation is  1 - K_body = (a0/2) <1/|a_i|>  instead of  a0/(2 g_bar).  Representative |a_i|:
       nucleons in nuclei  ~ {A_NUC:.2e} m/s^2   (8 MeV over 2 fm)
       electrons in atoms  ~ {A_ATOM:.2e} m/s^2   (13.6 eV over a_Bohr)
       lattice phonons     ~ {A_PHON:.2e} m/s^2   (Debye omega^2 A)
  Mass is carried by nucleons, so <1/|a_i|> ~ 1/{A_NUC:.1e}:
""")
for f_ in ("canon", "alt"):
    defo_int = A0[f_] / (2 * A_NUC)
    gal_needed = 0.5     # 1-K ~ 0.5 where g_bar ~ a0, i.e. where the RAR lives
    print(f"    {f_:<6} 1-K_body(constituent-wise) = {defo_int:.3e}   vs the {gal_needed:.1f} needed at a galaxy"
          f"  ->  MOND suppressed by {gal_needed/defo_int:.2e}x = {np.log10(gal_needed/defo_int):.1f} ORDERS")
    print(f"           its composition-dependent part (Pt vs Ti internal accel differ by O(30%)): "
          f"eta ~ {0.3*defo_int:.2e}  vs MICROSCOPE {ETA_1SIG:.1e}  ->  {ETA_1SIG/(0.3*defo_int):.1e}x BELOW")
print(f"""
  TWO CONCLUSIONS, both load-bearing for (a):
   1. The constituent-wise reading is RAR-FATAL: it destroys the framework's galactic phenomenology by
      ~{np.log10(0.5/(A0['canon']/(2*A_NUC))):.0f} orders (every galaxy is made of atoms).  The framework is therefore FORCED to the
      centre-of-mass reading -- which is exactly the species-blind one.  eta = 0 is CO-FORCED with the
      RAR; it is not an extra assumption.  That is the strongest form of the structural argument, and
      it is an internal-consistency argument the paper does not currently make.
   2. Even if one granted CH-3, its composition-dependent eta is ~{0.3*A0['canon']/(2*A_NUC):.0e} -- {np.log10(ETA_1SIG/(0.3*A0['canon']/(2*A_NUC))):.0f} orders BELOW
      MICROSCOPE.  So the one channel that would genuinely carry internal structure is unobservable
      by WEP tests anyway: it dies on rotation curves, ~{np.log10(0.5/(A0['canon']/(2*A_NUC))):.0f} orders before MICROSCOPE gets a vote.
""")
check("CH-3 (constituent-wise kernel) is excluded by the RAR itself, by >30 orders",
      0.5 / (A0["canon"] / (2 * A_NUC)) > 1e30)
check("CH-3's composition-dependent eta is >20 orders below MICROSCOPE",
      ETA_1SIG / (0.3 * A0["canon"] / (2 * A_NUC)) > 1e20)

# ---------------------------------------------------------------------------------------------------
# 6b. CH-4: WHAT DOES rho_m ACTUALLY DENOTE?  -- the one place MICROSCOPE genuinely bites
# ---------------------------------------------------------------------------------------------------
head("6b.  CH-4 THE rho_m READING -- full matter Lagrangian vs rest-mass proxy.  THE SHARP TEST.")
print(r"""
  The action is written S_matter[g,u,psi;K] but IMPLEMENTED with a prescribed scalar rho_m.  The paper
  itself flags that rho_m is a PROXY (Sec. 4: "the proxy-literal fork (rho_m = m^2 phi^2 taken at face
  value)").  Once psi is resolved into real matter -- nucleons bound by the strong force, electrons
  bound electromagnetically -- there are TWO inequivalent covariant readings of what the dressing W
  multiplies, and they are NOT the same theory:

    READING F [FULL]      W multiplies the WHOLE matter Lagrangian:
                          S = -(1/2)\int sqrt(-g) L_matter[psi,g] W[u,g]
                          Then EVERY form of internal energy -- rest mass, nuclear binding, EM
                          binding, thermal -- is dressed by the same K.  eta = 0 EXACTLY.
    READING R [REST-MASS] W multiplies only a rest-mass / dust term, leaving interaction energies
                          undressed.  Then, with b = B/(mc^2) the binding-energy mass fraction,
                              m_I/m = (1+b) K - b = K - b(1-K)   =>   1 - m_I/m = (1-K)(1+b)
                          i.e. CH-1 with lambda = 1 EXACTLY and q = b.  eta != 0, and its size is
                          set by the framework's own numbers with NO freedom.

  Reading R is not a strawman: it is what you get if the dressing is attached to the mass term of the
  matter action, which is the literal reading of "rho_m [ s u.K.u ]".  MICROSCOPE discriminates them.
""")
b_Pt, b_Ti = alloy_h["PtRh10 (inner)"]["B"], alloy_h["TA6V (outer)"]["B"]
print(f"  {'footing':<8}{'a0/2 [m/s^2]':>14}{'1-K':>12}{'eta_R predicted':>18}"
      f"{'/ 1sig ceiling':>16}{'/ 2sig ceiling':>16}{'tension vs measured':>22}")
print("  " + "-" * 100)
ETA_R = {}
for f_ in ("canon", "alt"):
    defo = A0[f_] / (2 * G_ORB)
    eta_R = (b_Ti - b_Pt) * defo                       # sign: Ti alloy is the MORE-bound one
    ETA_R[f_] = eta_R
    sig_asPub = abs(eta_R - ETA_CEN) / ETA_TOT         # published sign convention eta(Ti,Pt)
    print(f"  {f_:<8}{A0[f_]/2:>14.3e}{defo:>12.3e}{eta_R:>+18.3e}"
          f"{eta_R/ETA_1SIG:>15.2f}x{eta_R/ETA_2SIG:>15.2f}x{sig_asPub:>20.2f} sig")
sig_flip = abs(-ETA_R["canon"] - ETA_CEN) / ETA_TOT
print(f"""
  b(PtRh10) = {b_Pt:.6f} ,  b(TA6V) = {b_Ti:.6f} ,  Delta b = {b_Ti-b_Pt:+.4e}  (TA6V is the MORE-bound alloy)
  Cross-check: the independent "baryons per unit mass" handle gives Delta q = {DQ['BAR']:.4e}, agreeing
  with the binding handle {DQ['B']:.4e} to {abs(DQ['BAR']/DQ['B']-1)*100:.0f}% -- as it must (A/M and 1 - B/M are the same physics).

  SIGN FORK, stated because it changes the significance and I will not pick the flattering one:
      as published  eta(Ti,Pt) = {ETA_CEN:+.1e} , prediction {ETA_R['canon']:+.2e}  ->  {abs(ETA_R['canon']-ETA_CEN)/ETA_TOT:.2f} sigma TENSION
      sign flipped  prediction {-ETA_R['canon']:+.2e}                        ->  {sig_flip:.2f} sigma (no tension)
      magnitude only |eta_R| = {ETA_R['canon']:.2e} is {ETA_R['canon']/ETA_1SIG:.1f}x the 1-sigma ceiling, {ETA_R['canon']/ETA_2SIG:.2f}x the 2-sigma ceiling.

  VERDICT ON CH-4:  Reading R is DISFAVOURED at ~{sig_flip:.1f}-{abs(ETA_R['canon']-ETA_CEN)/ETA_TOT:.1f} sigma (canon) / ~{abs(-ETA_R['alt']-ETA_CEN)/ETA_TOT:.1f}-{abs(ETA_R['alt']-ETA_CEN)/ETA_TOT:.1f} sigma (alt).
  MARGINAL, NOT EXCLUDED.  But it is the ONLY place in this lane where MICROSCOPE reaches the
  framework's own predicted magnitude with zero free parameters -- lambda is not fitted, it is 1 by
  construction in Reading R.  So MICROSCOPE's real physics content here is a STRUCTURAL REQUIREMENT
  on the action's unwritten detail:

      >> the MI dressing's coefficient must be the body's TOTAL MASS-ENERGY (all internal binding
         energies included), not a rest-mass/dust proxy. <<

  *** LABEL CORRECTED 2026-07-25 (cross-lane audit). The sentence above previously read "Reading F
  is required", which is WRONG, and the F-vs-R dichotomy used here is INCOMPLETE. Reading F as
  defined above bundles TWO INDEPENDENT questions, and the sibling clocks lane EXCLUDES one half of
  the bundle by 2.1-3.2 orders (its Reading C2 = "every transition frequency carries the factor
  K(|a|)"), so "F required" collides head-on with "C2 excluded". The resolution is that the two
  questions must be separated:
      (Q1) WHAT does the dressed coefficient DENOTE?   rest mass only  vs  TOTAL mass-energy
      (Q2) WHERE does the dressing ACT?                CoM kinetic term only  vs  also internal dynamics
  Evaluating the full 2x2 against BOTH bounds and BOTH footings (VERIFY_mi_precision_ledger_2026.py
  V4): at the conservative 2-sigma MICROSCOPE ceiling exactly TWO cells survive and BOTH have
  Q2 = CoM-only; at the 1-sigma ceiling exactly ONE survives. So the CLOCKS axis (Q2) is DECISIVELY
  fixed and gate-proof, while the MICROSCOPE axis (Q1) is only DISFAVOURED for rest-mass
  (eta_R = 4.463e-15 = 1.94x the 1-sigma ceiling but only 0.64x the 2-sigma ceiling -- NOT excluded).
  THE UNIQUE JOINT SURVIVOR: "K dresses the CENTRE-OF-MASS inertia, with coefficient = the body's
  TOTAL mass-energy." That is neither F-as-written nor R -- and it is what the paper's own Sec. 2.2
  already says ("rods, clocks, and photons ride g"; rho_m is "the SAME rho_m that carries the passive
  gravitational mass"). So no new posit is needed and the ledger's CONSISTENT verdict SURVIVES; what
  was wrong was only this lane's label. Two of the highest-precision experiments in physics jointly
  pin the matter coupling's structure -- a real result, not a repair. ***

  This is a DC-CHANNEL-ONLY constraint.  Under the gated AC channel it dies with everything else:
  eta_R * Re G = {ETA_R['canon']*REG_MAX:.2e}, i.e. {np.log10(ETA_1SIG/(ETA_R['canon']*REG_MAX)):.0f} orders below the bound, no constraint.  So CH-4 is
  ALSO an independent line on Fork C: a DC channel is admissible only in Reading F.
""")
check("Reading R's eta is a ZERO-PARAMETER prediction of order the MICROSCOPE bound "
      "(within a factor 10 of it), i.e. this test is genuinely at the framework's own scale",
      0.1 < ETA_R["canon"] / ETA_1SIG < 10)
check("Reading R is disfavoured but NOT excluded by many orders (0.5 sig < significance < 5 sig) -- "
      "reported as marginal, not as a kill", 0.5 < abs(ETA_R["canon"] - ETA_CEN) / ETA_TOT < 5)
check("under the gate, Reading R's eta is >15 orders below the bound (AC channel says nothing)",
      ETA_1SIG / (ETA_R["canon"] * REG_MAX) > 1e15)

# ---------------------------------------------------------------------------------------------------
# 7. GEOMETRIC / NON-COMPOSITIONAL DIFFERENTIALS (the only nonzero DC differential)
# ---------------------------------------------------------------------------------------------------
head("7.  THE ONLY NONZERO DC DIFFERENTIAL: test-mass off-centring (composition-INDEPENDENT)")
DR_OFF = 20e-6      # residual off-centring of the two concentric cylinders' centres of mass (~20 um)
dg = 2 * G_ORB / R_ORB * DR_OFF
for f_ in ("canon", "alt"):
    # d(1-K)/dln|a| = -(1-K) at large y  =>  differential of the deformation
    eta_geo = (A0[f_] / (2 * G_ORB)) * (dg / G_ORB)
    print(f"    {f_:<6} off-centring {DR_OFF*1e6:.0f} um -> delta g = {dg:.2e} m/s^2 -> "
          f"eta_geom = (a0/2g)(dg/g) = {eta_geo:.2e}   ({ETA_1SIG/eta_geo:.1e}x BELOW the bound)")
print("""
  This is the one differential the DC channel produces with lambda = 0 exactly: the two masses sit at
  slightly different |a|, and K is nonlinear.  It is real, it is composition-independent (so it is NOT
  an Eotvos violation), and it is ~8 orders below MICROSCOPE.  No constraint.
""")

# ---------------------------------------------------------------------------------------------------
# 8. THE omega_c INVERSION -- where does MICROSCOPE rank as a constraint on the gate?
# ---------------------------------------------------------------------------------------------------
head("8.  INVERSION -- the omega_c that MICROSCOPE would REQUIRE, vs the paper's window")
print(f"""
  Same procedure as mi_cassini_q2_omegac_2026.py Sec.5: solve eta_ungated * Re G(omega_EP, omega_c)
  = bound for omega_c.  Only meaningful if lambda != 0 (at lambda = 0 there is nothing to suppress and
  MICROSCOPE places NO ceiling on omega_c at all).  Quoted at lambda = 1 as an upper-bounding exercise:
""")
print(f"  {'fork':<8}{'handle':<26}{'eta_ung':>12}{'ReG req':>12}{'omega_c REQ [rad/s]':>22}"
      f"{'vs band top 2.21e-14':>24}{'verdict':>10}")
print("  " + "-" * 116)
rank = {}
for fork, defo in (("L", defo_L["canon"]), ("G", defo_G["canon"])):
    for k in ("B", "NZ"):
        e_ung = DQ[k] * defo
        S_req = ETA_1SIG / e_ung
        if S_req >= 1.0:
            print(f"  {fork:<8}{HANDLE_NAME[k]:<26}{e_ung:>12.3e}{'>1':>12}{'no ceiling':>22}"
                  f"{'--':>24}{'ALLOWED':>10}")
            continue
        wc_req = OM_EP_MIN / invert_ReG(S_req)
        rank[(fork, k)] = wc_req
        print(f"  {fork:<8}{HANDLE_NAME[k]:<26}{e_ung:>12.3e}{S_req:>12.3e}{wc_req:>22.3e}"
              f"{wc_req/2.21e-14:>23.2e}x{'INSIDE' if wc_req >= 2.21e-14 else 'OUTSIDE':>10}")
wc_mic_L, wc_mic_G = rank[("L", "NZ")], rank[("G", "NZ")]
print(f"""
  RANKING of ceilings on omega_c (canon footing).  The first three are RECOMPUTED here from the same
  inputs as mi_cassini_q2_omegac_2026.py Sec.2/5, not quoted:
      LLR Gdot/G secular drift        omega_c <= {WC_LLR:.2e} rad/s   <-- BINDING (sets the band top)
      Saturn reactive delta_g         omega_c <= {WC_SAT_REACT:.2e} rad/s   ({WC_SAT_REACT/WC_LLR:.0f}x looser)
      Cassini Q2 quadrupole (Fork A)  omega_c <= {WC_Q2:.2e} rad/s   ({WC_Q2/WC_LLR:.0e}x looser)
      MICROSCOPE WEP, Fork L, lam=1   omega_c <= {wc_mic_L:.2e} rad/s   ({wc_mic_L/WC_LLR:.0e}x looser)  <-- LOOSEST
      [MICROSCOPE WEP, Fork G, lam=1  omega_c <= {wc_mic_G:.2e} rad/s -- would rank between Saturn and Q2,
       but it is the reduced-weight fork (f_spin bin, not f_EP); recorded, not used.]
  MICROSCOPE adds NO information about the gate corner in its clean (Fork L) reading.  At lambda = 0 --
  the written action -- it places no ceiling on omega_c whatsoever.  Stated so the ledger is not read
  as a hidden constraint.
""")
check("recomputed LLR ceiling reproduces the paper's band top 2.21e-14 to <2%",
      abs(WC_LLR / 2.21e-14 - 1) < 0.02)
check("recomputed Saturn-reactive and Cassini-Q2 ceilings reproduce mi_cassini_q2_omegac_2026.py "
      "(8.27e-11 and 2.26e-09) to <2%",
      abs(WC_SAT_REACT / 8.27e-11 - 1) < 0.02 and abs(WC_Q2 / 2.26e-09 - 1) < 0.02)
check("MICROSCOPE's Fork-L ceiling on omega_c is LOOSER than every other solar-system ceiling "
      "-> it is not a hidden constraint on the gate", wc_mic_L > WC_Q2 > WC_SAT_REACT > WC_LLR)

# ---------------------------------------------------------------------------------------------------
# 9. VERDICT
# ---------------------------------------------------------------------------------------------------
head("9.  VERDICT -- MICROSCOPE / WEP line of the precision-consistency ledger")
lam_L_NZ = ETA_1SIG / (DQ["NZ"] * defo_L["canon"])
lam_L_B = ETA_1SIG / (DQ["B"] * defo_L["canon"])
print(f"""
  (a) IS eta = 0 STRUCTURAL?   YES -- exact, and exact to ALL ORDERS in the kernel expansion.
      Reason, from the action and not asserted: S_matter = -(1/2)\\int sqrt(-g) rho_m W[u,g] is a
      product of exactly two objects -- a functional W of (u,g,partial u) with no matter field in it,
      and ONE composition-blind scalar rho_m which is also the passive gravitational mass.  rho_m
      cancels between the two sides of the balance; every order of K = sum c_n (Box_u/a0^2)^n adds
      only (u,g) structure.  There is no third object in the term for a species label to live in.
      STRENGTHENED (new here): the ONE reading that would carry internal structure -- applying the
      kernel constituent-wise -- is not merely small, it is RAR-FATAL, suppressing MOND by ~40 orders.
      So the framework's own galactic phenomenology FORCES the centre-of-mass, species-blind reading:
      eta = 0 is CO-FORCED with the RAR.
      HONEST CAVEATS (the exactness is conditional on these, all of them framework postulates):
        * the single passive u (one frame, hypersurface-orthogonal) and a single rho_m;
        * a0 species- and environment-independent.  A density- or environment-dependent a0 (the
          BIG-SPARC / rho_local fork already in the corpus) reopens CH-2 and MICROSCOPE then bites.
        * AND THE ONE THAT IS NOT SAFE (Sec. 6b, CH-4): rho_m must denote the FULL matter Lagrangian,
          not a rest-mass/dust proxy.  The action as WRITTEN does not say which.  If the dressing
          leaves nuclear/EM binding energy undressed, eta is a ZERO-PARAMETER prediction
          eta_R = Delta b * a0/(2 g) = {ETA_R['canon']:+.2e} (canon) / {ETA_R['alt']:+.2e} (alt), which is
          {ETA_R['canon']/ETA_1SIG:.1f}x / {ETA_R['alt']/ETA_1SIG:.1f}x the 1-sigma ceiling -> DISFAVOURED at ~{sig_flip:.1f}-{abs(ETA_R['canon']-ETA_CEN)/ETA_TOT:.1f} sigma.
          So eta = 0 is structural GIVEN Reading F, and MICROSCOPE is what forces Reading F.
          That is this lane's one genuine constraint on the theory, and it is not a many-orders
          exclusion -- it is a marginal ~2 sigma preference.  Stated as such.

  (b) THE 1e-12 GAP:  the gap DOES NOT EXIST as stated, and the paper's sentence is wrong.
      The "< 1e-12" is a double-precision FLOAT TOLERANCE on a DIFFERENT check -- the algebraic
      inversion x = y nu(y) of mu_fw(x) x = y -- which is separately proven EXACTLY (symbolic residual
      identically 0).  It is not a bound on eta and not a theoretical uncertainty, so MICROSCOPE does
      NOT probe below the theory's own precision.  BUT the shipped eta check is
      `eta_AB = x_phys - x_phys`, an expression minus itself: a TAUTOLOGY with zero discriminating
      power.  The eta = 0 claim is therefore DERIVED-but-UNVERIFIED as of the current repo state.
      Sections 3-4 here supply the genuine verification (independent two-species root-finds, a
      lambda-injection negative control, and the closed form confirmed at dps=60).
      REQUIRED EDIT: replace "Machine check: eta < 1e-12 over y in [1e-2,1e2]" with "eta = 0 by
      species-blindness of W; the 1e-12 is the float tolerance of the balance-inversion check."

  (c) THE TWO PREDICTIONS (canon / alt):
      GATED (AC):  Re G(omega_EP) <= {REG_MAX:.2e} at the window's most permissive corner
                   -> eta_AC <= {max(l[4] for l in LEDGER):.2e} even at lambda = 1 and the largest handle
                   -> passes MICROSCOPE by {np.log10(ETA_1SIG/max(l[4] for l in LEDGER)):.0f} ORDERS.  NO CONSTRAINT, consistent-by-gating.
                   (This is the honest expected result, reported with its suppression factor.)
      DC (Fork C): eta_DC = 0 EXACTLY in the written action -> "pass at 0.65 sigma" is correct but
                   is a statement about zero, not a test.  The real content is the ceiling on any
                   composition coupling lambda of the MI deformation (1-K = a0/2g = {defo_L['canon']:.2e} at
                   MICROSCOPE):
                        lambda <= {lam_L_B:.2f}    (nuclear binding handle, Delta q = {DQ['B']:.2e})
                        lambda <= {ETA_1SIG/(DQ['ZA']*defo_L['canon']):.2e} (charge-per-mass handle,  Delta q = {DQ['ZA']:.3f})
                        lambda <= {lam_L_NZ:.2e} (neutron-excess handle,   Delta q = {DQ['NZ']:.3f})
                   So: an O(1) composition coupling in the DC channel is EXCLUDED by
                   {1/lam_L_B:.1f}x - {1/lam_L_NZ:.0f}x (i.e. {np.log10(1/lam_L_B):.1f} - {np.log10(1/lam_L_NZ):.1f} orders), handle-dependent.
                   The physically forced instance of lambda = 1 is CH-4 (Reading R): eta_R =
                   {ETA_R['canon']:+.2e} / {ETA_R['alt']:+.2e}, disfavoured at ~{sig_flip:.1f}-{abs(ETA_R['canon']-ETA_CEN)/ETA_TOT:.1f} sigma.  MARGINAL, NOT EXCLUDED.

  DOES MICROSCOPE EXCLUDE THE DC CHANNEL?   NO -- and this is a NULL, not a pass manufactured for it.
      Reason: eta is a DIFFERENTIAL observable and the DC MI dressing is exactly COMMON MODE.  The
      common-mode piece itself (an extra a0/2 = {A0['canon']/2:.2e} m/s^2 Earthward, {A0['canon']/(2*G_ORB):.1e} of g) is
      {A0['canon']/2/(ETA_1SIG*G_ORB):.0e}x above MICROSCOPE's differential resolution but is 100% degenerate with GM_E on a
      near-circular orbit, so it is invisible for a structural reason.  MICROSCOPE therefore cannot
      decide Fork C.  What it DOES do is bound the DC channel's STRUCTURE sector at the 1e-3 - 0.5
      level -- i.e. the DC channel survives MICROSCOPE only in its exactly-universal form, which is
      precisely the form the written action delivers.  That is a real, if modest, independent line on
      Fork C: it says a DC channel is admissible, but not a DC channel that resolves internal structure.

  WHERE THE SHARP TEST IS, if one wants MICROSCOPE to bite on Fork C:  Fork G (the EFE reading that
  makes Cassini Q2 dangerous) has 1-K = {defo_G['canon']:.2e}, {defo_G['canon']/defo_L['canon']:.0e}x larger, and would exclude an O(1)
  coupling by {np.log10(DQ['NZ']*defo_G['canon']/ETA_1SIG):.0f} orders -- but its signal sits at f_spin, not the published f_EP bin, so
  that number is indicative only and is NOT the verdict.

  SCOPE: dynamics sector (S_matter) only.  Nothing here bears on the GW170817-excluded disformal
  photon sector.  No door is claimed closed; both a0 footings carried on every number.
""")
print(RULE)
print(f"mi_microscope_wep_2026.py: {NCHK[1]}/{NCHK[0]} checks passed.")
print(RULE)
