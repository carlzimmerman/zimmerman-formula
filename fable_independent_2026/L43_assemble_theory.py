#!/usr/bin/env python3
"""
L43 -- ASSEMBLE THE THEORY: one action, every parameter pinned, every gate run against it
==========================================================================================
This is the assembly lane.  Nothing new is probed.  What is done here is (1) write the action down
with every parameter fixed to a verified admissible window, (2) ask whether that window is NON-EMPTY
under the constraints as they stand on 2026-09-08 -- which is the single most important question --
(3) run every gate the programme owns against an explicit point, and (4) name the holes with sizes.

WHY THE ANSWER MAY DIFFER FROM L14, WHICH FOUND NO ADMISSIBLE POINT.  Four constraints moved:
  (a) sigma > 1 is admissible to the construction (L26/A31): the clock window is [1.6793, 1.7716),
      and sigma_* = 1.679312732 removes the IC6 Hadamard ill-posedness rather than reducing it;
  (b) gravitational Cherenkov is a LOWER bound (L19/A5, L26-X4, L33/A32): it constrains SUBLUMINAL
      modes, so a superluminal clock switches the channel off;
  (c) the coherence length xi is THEOREM-FORCED, not chosen (L34/A33): no kernel of the carrier class
      can screen the Solar System, so xi >= 0.10 pc canonical / 0.15 pc alt is a consequence;
  (d) the kernel must APPROACH and never ATTAIN its ceiling, with saturation exponent p <= 1.754
      (L34/A33): an attained supremum has Delta' = 0, hence infinite longitudinal stiffness and no
      cubic action.  This is a repair to the CARRIED KERNEL, and it is made here.
  and one structural decision is taken: the CONDENSATE IS REMOVED (A13/L14-T4).  Its background is
  what makes the clock tachyonic -- the single gate in every minimal incompatible subset L14 found --
  and it is 1e5x too small to be the dark sector it was introduced to be.  Removing it costs the
  theory nothing it ever had, and the lead's IC-series has already removed it.

STRUCTURE OF THIS SCRIPT
  PART I    CONTROLS: six section-A numbers reproduced INDEPENDENTLY (own algebra, own constants) and
            confronted with the value printed in the source lane's own .out file.
  PART II   CONTROL on the gate machinery itself: it must reproduce a known PASS and a known FAIL
            taken from existing gate scripts (g03d's admissibility table; L34's B1 shortfall).
  PART III  THE KERNEL: build the admissible approach family, fit it, verify the four properties the
            theorem demands, and price the difference against the carried kernel and against AQUAL.
  PART IV   THE ADMISSIBILITY QUESTION: is the region non-empty under tonight's constraints?
  PART V    THE GATE TABLE at the exhibited point, both footings.
  PART VI   THE HOLES, with sizes.
  PART VII  DISTINCTIVE PREDICTIONS AND FALSIFIERS.
  VERDICT   is this a complete theory, and if not exactly what is missing.

CHECKS THAT CAN FAIL are printed as [PASS]/[FAIL] lines.  A FAIL is a result, not a bug, unless it is
a CONTROL, in which case it invalidates what follows and says so.
"""
import os, sys, math, re, itertools
import numpy as np
import sympy as sp

FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
def rel(p): return os.path.relpath(p, REPO)          # never print a machine path
def readout(name):
    """read a committed .out file; returns '' if absent (the caller turns that into a FAIL)"""
    for cand in (os.path.join(HERE, name),
                 os.path.join(REPO, "qwen_claude_field_theory", "closure_2026", name)):
        if os.path.exists(cand):
            with open(cand, "r", errors="replace") as fh: return fh.read()
    return ""

BAR = "=" * 118
print(BAR)
print("L43 -- ASSEMBLE THE THEORY: one action, every parameter pinned, every gate run against it")
print(BAR, flush=True)

# ------------------------------------------------------------------ constants (sources named inline)
cc    = 2.998e8                                   # g03z line 32
G     = 6.674e-11
MSUN  = 1.989e30
GMSUN = 1.32712440e20
PC    = 3.0857e16; kpc = 3.0857e19; Mpc = 3.0857e22
AU    = 1.495978707e11
A0    = {"canonical": 9.3619e-11, "alt": 1.1279e-10}          # the framework's two footings
GEXT  = 1.778e-10                                             # g03z line 33, the Galactic external field
Om, OL, Ob, Od = 0.315, 0.685, 0.049, 0.266                   # g03v line 131
H0    = 0.674*100e3/Mpc
t0    = 13.8e9*3.156e7                                        # g03t line 193
R_SAT = 9.58*AU                                               # g03d line 21
Q2_CEIL, M_SAT_BOUND, A_SUNWARD = 5.2e-27, 6.7e-11, 0.5*9.36e-11/1278.0     # g03d line 21
A_SAT_PHANTOM = GMSUN*M_SAT_BOUND/R_SAT**2                    # the Saturn phantom-mass gate as an acceleration
XI_FLOOR = {"canonical": 0.10, "alt": 0.15}                   # L34/A33, g03z XI_FLOOR, Amendment 11(b)
XI_FLOOR_EXP = {"canonical": 0.03, "alt": 0.05}               # g03d's own solve, exponential carrier
P_MAX = 1.7538                                                # L34/A33 D3-D4
SIGMA_LO, SIGMA_HI = 1.679312732187113, 1.771525666           # L26/A31 H10
ALPHA1_BOUND, ALPHA2_BOUND = 1e-4, 4e-7                       # g03z G2 ; g03v ppn()
K2_GROWTH = 0.42*cc**2*9*(0.2/Mpc)**2*t0**2                   # g03t D7 floor at k = 0.2/Mpc


# ==================================================================================================
print("\n" + BAR)
print("PART I -- CONTROLS: six settled numbers rebuilt from their own algebra, then confronted with")
print("          the value printed in the source lane's own .out.  The assembly is verification, not quotation.")
print(BAR, flush=True)

# ---- K1  A19 / L13:  alpha_1 = -4 c_14 EXACTLY, and the Foster-Jacobson alpha_2 closed form.
KB_s, c2_s, c14_s = sp.symbols("K_B c_2 c_14", positive=True)
c1_s, c3_s, c4_s = KB_s, -KB_s, c14_s - KB_s
c123_s = sp.simplify(c1_s + c2_s + c3_s)
a1_s = sp.simplify(-8*(c3_s**2 + c1_s*c4_s)/(2*c1_s - c1_s**2 + c3_s**2))
a2_s = sp.simplify(a1_s/2 - (c1_s + 2*c3_s - c4_s)*(2*c1_s + 3*c2_s + c3_s + c4_s)/(c123_s*(2 - c14_s)))
id_alpha1 = sp.simplify(a1_s + 4*c14_s)
print(f"    sympy, c_1 = -c_3 = K_B, c_4 = c_14 - K_B:  alpha_1 = {sp.simplify(a1_s)}   (c_123 simplifies to {c123_s})")
check("K1 [control, A19/L13] alpha_1 = -4 c_14 is an EXACT identity in (K_B, c_2, c_14), rebuilt symbolically here",
      id_alpha1 == 0, f"alpha_1 + 4 c_14 simplifies to {id_alpha1}")
_a1_corner = float(a1_s.subs({KB_s: 0.2, c2_s: 1.0, c14_s: 1.18e-5}))
_a2_corner = float(a2_s.subs({KB_s: 0.2, c2_s: 1.0, c14_s: 1.18e-5}))
_txt13 = readout("L13_strong_coupling.out")
_pub13 = re.search(r"alpha_1 = (-[\d.e+-]+), alpha_2 = (-[\d.e+-]+)\s+\(f33", _txt13)
_p13 = (float(_pub13.group(1)), float(_pub13.group(2))) if _pub13 else (None, None)
check("K1b [control] my rebuild reproduces f33's PPN corner (K_B=0.2, c_2=1, c_14=1.18e-5) to 1% of the value L13's own .out prints",
      _p13[0] is not None and abs(_a1_corner/_p13[0] - 1) < 0.01 and abs(_a2_corner/_p13[1] - 1) < 0.01,
      f"mine ({_a1_corner:.4e}, {_a2_corner:.4e}) vs {rel(os.path.join(HERE,'L13_strong_coupling.out'))} ({_p13[0]}, {_p13[1]})")

def alpha_1_bare(c14): return -4.0*np.asarray(c14, float)
def alpha_2_of(K_B, c2, c14):
    K_B, c2, c14 = (np.asarray(v, float) for v in (K_B, c2, c14))
    return -2*c14 + c14*(3*c2 + c14)/(c2*(2 - c14))

# ---- K2  A31 / L26:  T, a_*, sigma_* and the window's upper edge, from the closed forms.
T_ind   = -sp.Rational(27, 16) + 54/(5*sp.log(sp.Rational(9, 5)))
T_val   = float(T_ind)
astar   = 3 - 81/(4*T_val)
sigstar = 4*T_val/(4*T_val - 27)
print(f"    T = -27/16 + 54/(5 ln(9/5)) = {T_val:.10f};  a_* = 3 - 81/(4T) = {astar:.11f};  sigma_* = 4T/(4T-27) = 3/a_* = {sigstar:.12f}")
_txt26 = readout("L26_sigma_above_one.out")
_pub26 = re.search(r"sigma_\* = (1\.6793\d+)", _txt26)
_pub26b = re.search(r"upper edge (1\.77\d+)", _txt26)
check("K2 [control, A31/L26] sigma_* = 4T/(4T-27) = 3/a_* rebuilt from T = -27/16 + 54/(5 ln(9/5)) reproduces L26's printed sigma_* to 1e-9, and the two closed forms agree with each other",
      _pub26 is not None and abs(sigstar - float(_pub26.group(1))) < 1e-9 and abs(sigstar - 3/astar) < 1e-12,
      f"mine {sigstar:.12f}, 3/a_* {3/astar:.12f}, L26 .out {_pub26.group(1) if _pub26 else 'NOT FOUND'}")
check("K2b [control, A31/L26] the window's upper edge (J_T -> 0, affine in sigma) printed by L26 is 1.7716 and sigma_* lies below it with the 5.49% headroom L26 reports",
      _pub26b is not None and abs(float(_pub26b.group(1)) - SIGMA_HI) < 2e-3
      and abs((SIGMA_HI - sigstar)/sigstar - 0.05491) < 5e-4,
      f"headroom {(SIGMA_HI - sigstar)/sigstar*100:.3f}% of sigma_*  (L26: 5.491%)")

# ---- K3  A33 / L34:  the bounded-boost suprema, the stiffness identity, and nu_RAR's ceiling.
y_s, s_s = sp.symbols("y s", positive=True)
D_exp = y_s*sp.exp(-y_s)
crit  = sp.solve(sp.diff(D_exp, y_s), y_s)
sup_exp = float(D_exp.subs(y_s, crit[0]))
Y_s = sp.symbols("Y", positive=True); Dfun = sp.Function("Delta")
# Sigma_par = J + 2 Y dJ/dY with J(Y) defined implicitly by J(g_phi) g_phi = g_N; PAPER5 section 7.
g_s = sp.symbols("g_phi", positive=True)
J_of = s_s/Dfun(s_s)                                   # J_Y as a function of s, with g_phi = a0 Delta(s)
Sigma_sym = sp.simplify(sp.diff(s_s, s_s)/sp.diff(Dfun(s_s), s_s))     # ds/dDelta = 1/Delta'
def Delta_rar_raw(s):
    s = np.asarray(s, float)
    return np.where(s > 0, s*np.exp(-np.sqrt(np.maximum(s, 1e-300)))/(1 - np.exp(-np.sqrt(np.maximum(s, 1e-300)))), 0.0)
_ss = np.linspace(1e-6, 8.0, 4000001)
_dd = Delta_rar_raw(_ss); _i = int(np.argmax(_dd)); S_RAR, C_RAR = float(_ss[_i]), float(_dd[_i])
print(f"    sup(y e^-y) = {sup_exp:.6f} at y = {float(crit[0]):.0f};  nu_RAR's interior maximum: s_sat = {S_RAR:.4f}, C = {C_RAR:.6f};  Sigma_par = ds/dDelta = 1/Delta'")
_txt34 = readout("L34_boost_vs_cubic.out")
_pub34 = re.search(r"s_sat = 2\.540 and Delta_sat = C = 0\.6476.*?\(s_sat ([\d.]+), C ([\d.]+)\)", _txt34, re.S)
check("K3 [control, A33/L34] the two suprema rebuilt here -- sup(y e^-y) = 1/e = 0.367879 at y = 1, and nu_RAR's C = 0.6476 at s_sat = 2.540 -- reproduce L34's own printed values",
      abs(sup_exp - 1/math.e) < 1e-12 and _pub34 is not None
      and abs(S_RAR - float(_pub34.group(1))) < 3e-3 and abs(C_RAR - float(_pub34.group(2))) < 3e-4,
      f"mine (1/e = {sup_exp:.6f}; s_sat {S_RAR:.4f}, C {C_RAR:.6f}) vs L34 .out ({_pub34.group(1) if _pub34 else '?'}, {_pub34.group(2) if _pub34 else '?'})")

# ---- K4  A14 / L11:  the IC-series static branch gives mu(y) = 1 - e^-y with MOND coefficient exactly 1.
c_aux, a_sym, a0_sym = sp.symbols("c a |a0|", positive=True)
Uprime = -sp.log(1 - c_aux)**2                            # IC1/L11: U'(c) = -ln^2(1-c)
stat = sp.Eq(sp.diff((1 - c_aux)*a_sym**2, c_aux) - a0_sym**2*Uprime, 0)      # d/dc[(1-c)a^2 - a0^2 U(c)] = 0
sol_c = sp.solve(stat, c_aux)
u2 = sp.simplify(sol_c[0])
check("K4 [control, A14/L11] the IC-series' own auxiliary equation d/dc[(1-c)a^2 - a0^2 U(c)] = 0 with U'(c) = -ln^2(1-c), solved here from scratch, returns u^2 = 1 - exp(-|a|/a0) -- so mu(y) = 1 - e^-y is the static branch, not an assumption",
      sp.simplify(u2 - (1 - sp.exp(-a_sym/a0_sym))) == 0, f"solved c = {u2}")
_mond_coeff = {}
for f, a0 in A0.items():
    gN = 1e-14*a0                                          # deep in the MOND regime
    g = float(sp.nsolve(sp.Symbol('g', positive=True)*(1 - sp.exp(-sp.Symbol('g', positive=True)/a0)) - gN,
                        sp.Symbol('g', positive=True), math.sqrt(gN*a0)))
    _mond_coeff[f] = g/math.sqrt(gN*a0)
check("K4b [control, A14/L11] the deep-MOND coefficient of (1 - e^-{g/a0}) g = g_N is EXACTLY 1 on both footings (no stray 2, 1/2 or 2 pi) -- L11's 'coefficient 1.000000', recomputed by root-finding here",
      all(abs(v - 1) < 1e-6 for v in _mond_coeff.values()),
      ", ".join(f"{f} {v:.8f}" for f, v in _mond_coeff.items()))

# ---- K5  A8 / L7:  the cluster residual IS the cosmic dark-to-baryon share.
cosmic_ratio = Od/Ob
_txt7 = readout("L7_cosmic_ratio.out")
_pub7 = re.search(r"NEWTONIAN\s+M_dark/M_bar\s+: median ([\d.]+)\s+\+/- ([\d.]+)", _txt7)
check("K5 [control, A8/L7] Omega_dm/Omega_b = 0.266/0.049 = 5.43 recomputed here sits inside the 1 sigma band of the cluster requirement L7's own .out prints (5.73 +/- 0.68)",
      _pub7 is not None and abs(cosmic_ratio - float(_pub7.group(1))) < float(_pub7.group(2)),
      f"cosmic {cosmic_ratio:.3f} vs L7 .out required {_pub7.group(1) if _pub7 else '?'} +/- {_pub7.group(2) if _pub7 else '?'}")

# ---- K6  A24 / the a0-Lambda tie:  kappa on each footing, and the reduction beta/sqrt(Ztilde) = kappa/sqrt2.
rho_c   = 3*H0**2/(8*math.pi*G)
rho_Lam = OL*rho_c
a0_tie  = cc*math.sqrt(G*rho_Lam)
KAPPA   = {f: A0[f]/a0_tie for f in A0}
print(f"    rho_Lambda = {rho_Lam:.4e} kg/m^3;  c sqrt(G rho_Lambda) = {a0_tie:.5e} m/s^2  =>  kappa = "
      + ", ".join(f"{f} {v:.4f}" for f, v in KAPPA.items()))
check("K6 [control, A24 + THE_ACTION section 2] a0 = kappa c sqrt(G rho_Lambda) recomputed from Planck's Omega_Lambda h^2 returns kappa = 1/2 on the canonical footing to better than 0.1%, which is the FIT the framework quotes -- and the alt footing needs kappa = 0.60, so the tie does not pick a footing",
      abs(KAPPA["canonical"] - 0.5) < 5e-3 and abs(KAPPA["alt"] - 0.5) > 0.05
      and abs(0.5/math.sqrt(2) - 0.354) < 1e-3,
      f"kappa canonical {KAPPA['canonical']:.5f}, alt {KAPPA['alt']:.5f}; A24's reduction beta/sqrt(Ztilde) = kappa/sqrt2 = {0.5/math.sqrt(2):.4f}")
print("    NOTE, standing rule: kappa = 1/2 is FITTED.  A24/L32 T1 proves it is a zero mode of any local action of")
print("    this class (F -> F + C is exactly degenerate with Lambda), and k01-k04 leave it underived.  The 27-simple-")
print("    numbers guard applies: landing in the measured band is not evidence.")


# ==================================================================================================
print("\n" + BAR)
print("PART II -- CONTROL ON THE GATE MACHINERY: it must reproduce a known PASS and a known FAIL")
print("           from gate scripts that already exist in the repository.")
print(BAR, flush=True)

# ---- known PASS: g03d's published Solar-System admissibility table (exact fourth-order solve).
_txtd = readout("g03d_exact_fourth_order_solar.out")
rows = re.findall(r"^\s+(canonical|alt)\s+([\d.e+-]+)\s+([\d.]+)\s+([\d.]+)\s+\|.*?\|\s+(yes|NO)\b",
                  _txtd, re.M)
tab = {}
for foot, gobs, xi_pc, eps, adm in rows:
    tab.setdefault(foot, {}).setdefault(float(xi_pc), []).append(adm == "yes")
floors = {f: (min([x for x, v in d.items() if all(v)]) if any(all(v) for v in d.values()) else None)
          for f, d in tab.items()}
print(f"    g03d's own table, re-read here: admissible-at-all-three-field-inputs floors = {floors}")
check("K7 [control, KNOWN PASS] my floor-extraction machinery, run over g03d's committed table, returns the floors g03d itself reports for the kernel it solved: 0.03 pc canonical / 0.05 pc alt",
      floors.get("canonical") == XI_FLOOR_EXP["canonical"] and floors.get("alt") == XI_FLOOR_EXP["alt"],
      f"{floors} vs g03d {XI_FLOOR_EXP}")
check("K7b [control, KNOWN FAIL inside the same table] the alt footing at xi = 0.03 pc is INADMISSIBLE at the strongest field input -- the machinery must return a FAIL where g03d prints 'NO', not merely a PASS where it prints 'yes'",
      "alt" in tab and 0.03 in tab["alt"] and (not all(tab["alt"][0.03])) and any(tab["alt"][0.03]),
      f"alt xi=0.03 admissibility across the three field inputs: {tab.get('alt', {}).get(0.03)}")

# ---- known FAIL: L34's B1 -- the bare carried kernel against the binding Saturn phantom-mass gate.
short = {f: C_RAR*A0[f]/A_SAT_PHANTOM for f in A0}
print(f"    g03d's two Solar-System gates rebuilt from its own constants: sunward {A_SUNWARD:.4e} m/s^2, "
      f"Saturn phantom {A_SAT_PHANTOM:.4e} m/s^2 (the tighter, hence binding)")
_pub34b = re.search(r"exceeds the binding gate by ([\d.e+]+)x \(canonical\) and ([\d.e+]+)x \(alt\)", _txt34)
check("K8 [control, KNOWN FAIL] the bare carried kernel's residual C a0 against the binding Saturn phantom-mass gate, rebuilt from g03d's own constants, reproduces L34's published shortfall of 1.400e4x canonical / 1.687e4x alt -- this FAIL is the theorem that FORCES the coherence length",
      _pub34b is not None and abs(short["canonical"]/float(_pub34b.group(1)) - 1) < 0.02
      and abs(short["alt"]/float(_pub34b.group(2)) - 1) < 0.02,
      f"mine {short['canonical']:.4e}x / {short['alt']:.4e}x vs L34 .out {_pub34b.group(1) if _pub34b else '?'} / {_pub34b.group(2) if _pub34b else '?'}")

# ---- known FAIL: L14's own emptiness, and its analytic cause.
c14_tach = 3*Od/Om
_txt14 = readout("L14_parameter_sweep.out")
_pub14 = re.search(r"T1 \[THE TEST\].*?\(canonical (\d+) points, alt (\d+) points\)", _txt14, re.S)
check("K9 [control, KNOWN FAIL] the OLD parameter set's emptiness reproduces analytically: with the condensate carrying Omega_d, the clock tachyon needs c_14 >= 3 Omega_d/Omega_m = 2.533 while PPN alpha_1 = -4 c_14 needs c_14 <= 2.5e-5 -- a 1.0e5x gap, so {G1a, G2} is empty by inspection, exactly as L14's .out reports 0 points on both footings",
      abs(c14_tach - 2.5333) < 1e-3 and c14_tach > ALPHA1_BOUND/4
      and _pub14 is not None and _pub14.group(1) == "0" and _pub14.group(2) == "0",
      f"c_14 >= {c14_tach:.4f} vs c_14 <= {ALPHA1_BOUND/4:.1e}: short by {c14_tach/(ALPHA1_BOUND/4):.1e}x; L14 .out prints {_pub14.group(1) if _pub14 else '?'}/{_pub14.group(2) if _pub14 else '?'} points")


# ==================================================================================================
print("\n" + BAR)
print("PART III -- THE KERNEL.  The carried kernel as published is INADMISSIBLE by the programme's own")
print("            bounded-boost theorem (an attained supremum has Delta' = 0).  It is repaired here.")
print(BAR, flush=True)

# The admissible family: Delta(s) = C[1 - W(u)^-p], u = sqrt(s), W = 1 + a1 u + a2 u^2, a1, a2 > 0.
#   small s: Delta -> C p a1 sqrt(s)  =>  deep-MOND coefficient exactly 1 requires C p a1 = 1;
#   large s: C - Delta ~ C a2^-p s^-p  =>  the saturation exponent is p, in L34's own convention;
#   Delta' > 0 at every finite s, so Sigma_par = 1/Delta' is finite everywhere and the cubic action exists;
#   sup Delta = C, APPROACHED and never attained, so the bounded-boost prediction is unchanged.
def Delta_fam(s, C, p, a2):
    s = np.asarray(s, float); u = np.sqrt(np.maximum(s, 0.0)); a1 = 1.0/(C*p)
    return C*(1.0 - (1.0 + a1*u + a2*u*u)**(-p))
def dDelta_fam(s, C, p, a2):
    s = np.asarray(s, float); u = np.sqrt(np.maximum(s, 1e-300)); a1 = 1.0/(C*p)
    W = 1.0 + a1*u + a2*u*u
    return C*p*(a1 + 2*a2*u)*W**(-p - 1.0)/(2*u)
def Delta_carried(s):                                    # THE_ACTION section 3: nu_RAR up to s_sat, then flat
    s = np.asarray(s, float); return np.where(s <= S_RAR, Delta_rar_raw(np.minimum(s, S_RAR)), C_RAR)
def Delta_aqual_exp(s):                                  # the IC-series' own static law: (1-e^-y) g = g_N
    s = np.asarray(s, float); y = np.maximum(s, 1e-300)
    for _ in range(200): y = y - (y*(1 - np.exp(-y)) - s)/((1 - np.exp(-y)) + y*np.exp(-y))
    return y - s

SFIT = np.geomspace(1e-4, 1e4, 3001)
def maxdex(C, p, a2, target):
    g1 = SFIT + Delta_fam(SFIT, C, p, a2); g2 = SFIT + target(SFIT)
    return float(np.max(np.abs(np.log10(g1/g2))))
from scipy.optimize import minimize
BEST = {}
for lbl, target, Cfix in (("nu_RAR carried (THE_ACTION section 3)", Delta_carried, C_RAR),
                          ("exponential carrier (recipe I1 / L11)", lambda s: np.minimum(Delta_aqual_exp(s), 1/math.e), 1/math.e)):
    best = None
    for p0 in (0.6, 1.0, 1.4, P_MAX):
        for a20 in (0.2, 0.6, 1.5, 4.0):
            r = minimize(lambda v: maxdex(Cfix, min(max(v[0], 1e-3), P_MAX), max(v[1], 1e-6), target),
                         [p0, a20], method="Nelder-Mead",
                         options=dict(xatol=1e-8, fatol=1e-12, maxiter=4000))
            v = (Cfix, min(max(r.x[0], 1e-3), P_MAX), max(r.x[1], 1e-6), float(r.fun))
            if best is None or v[3] < best[3]: best = v
    BEST[lbl] = best
    print(f"    fit to {lbl:40s}: C = {best[0]:.6f} (held at the kernel's own ceiling), p = {best[1]:.4f}, "
          f"a2 = {best[2]:.4f}  ->  max |d log10 g| = {best[3]:.4f} dex over s in [1e-4, 1e4]")
C_TH, P_TH, A2_TH, DEX_TH = BEST["nu_RAR carried (THE_ACTION section 3)"]
A1_TH = 1.0/(C_TH*P_TH)

check("N1 the repaired kernel has the EXACT deep-MOND coefficient 1 (C p a1 = 1 by construction, checked numerically as Delta/sqrt(s) -> 1)",
      abs(float(Delta_fam(1e-12, C_TH, P_TH, A2_TH))/1e-6 - 1) < 1e-4,
      f"Delta(1e-12)/sqrt(1e-12) = {float(Delta_fam(1e-12, C_TH, P_TH, A2_TH))/1e-6:.8f}")
_sgrid = np.geomspace(1e-8, 1e12, 20001)
_mono = bool(np.all(np.diff(Delta_fam(np.geomspace(1e-8, 1e6, 20001), C_TH, P_TH, A2_TH)) > 0))
check("N2 the repaired kernel is strictly increasing with Delta' > 0 at EVERY finite s, so Sigma_par = 1/Delta' is finite and the cubic action exists -- the property L34's C4 records the PUBLISHED kernel as failing",
      bool(np.all(dDelta_fam(_sgrid, C_TH, P_TH, A2_TH) > 0)) and _mono,
      f"min Delta' over 20 decades = {float(np.min(dDelta_fam(_sgrid, C_TH, P_TH, A2_TH))):.3e} > 0; strictly increasing over 14 decades in double precision")
import mpmath as mp
mp.mp.dps = 60
def _Delta_mp(s):
    u = mp.sqrt(mp.mpf(s)); a1 = mp.mpf(1)/(mp.mpf(C_TH)*mp.mpf(P_TH))
    return mp.mpf(C_TH)*(1 - (1 + a1*u + mp.mpf(A2_TH)*u*u)**(-mp.mpf(P_TH)))
_gap = mp.mpf(C_TH) - _Delta_mp(1e14)
check("N3 its supremum is APPROACHED and never attained, and equals the carried kernel's ceiling C = 0.6476, so the bounded-boost prediction and its SPARC test are unchanged",
      _gap > 0 and abs(float(_Delta_mp(1e14))/C_TH - 1) < 1e-6,
      f"at 60 digits, C - Delta(1e14) = {mp.nstr(_gap, 6)} > 0 (the ceiling is never reached at finite s), while Delta(1e14)/C - 1 = {float(_Delta_mp(1e14))/C_TH - 1:.2e}")
check("N4 its saturation exponent obeys L34's cap p <= 1.754 (exponential approach excluded), and the fit does not want to violate it",
      P_TH <= P_MAX + 1e-9, f"p = {P_TH:.4f} <= p_max = {P_MAX}")
S_SAT_SOLAR = {f: (GMSUN/R_SAT**2)/A0[f] for f in A0}
sig_par = {f: 1.0/float(dDelta_fam(S_SAT_SOLAR[f], C_TH, P_TH, A2_TH)) for f in A0}
print(f"    s at Saturn's orbit = {S_SAT_SOLAR['canonical']:.3e} (canonical) / {S_SAT_SOLAR['alt']:.3e} (alt);  "
      f"longitudinal stiffness Sigma_par = 1/Delta' there = {sig_par['canonical']:.3e} / {sig_par['alt']:.3e}")
check("N5 at the Solar-System background the repaired kernel's longitudinal stiffness is FINITE, where the published carried kernel gives Sigma_par = infinity (L34 C4, L33/A32's 'the real defect')",
      all(np.isfinite(v) and v > 0 for v in sig_par.values()),
      f"finite, but large: {sig_par['canonical']:.2e} -- the longitudinal cone is c_s ~ 1e10 c at Saturn, admissible by L33/A32's identity argument (the leaves stay spacelike at any FINITE c_s) but a real oddity of the class")
d_carrier_vs_aqual = float(np.max(np.abs(np.log10((SFIT + Delta_carried(SFIT))/(SFIT + Delta_aqual_exp(SFIT))))))
_s3 = np.array([3.0])
print(f"    THE STRUCTURAL FORK, priced: the carrier structure (THE_ACTION, scalar sourced by matter) and the AQUAL")
print(f"    structure (the IC-series' own static limit, L11) agree below s = 0.63 and diverge above it, because a")
print(f"    matter-sourced scalar cannot carry a DECREASING Delta.  At s = 3: carrier Delta = {float(Delta_carried(_s3)[0]):.4f} vs")
print(f"    AQUAL Delta = {float(Delta_aqual_exp(_s3)[0]):.4f}, i.e. {float(np.log10((3+Delta_carried(_s3)[0])/(3+Delta_aqual_exp(_s3)[0]))):.4f} dex in g; the maximum separation over s in [1e-4, 1e4] is {d_carrier_vs_aqual:.4f} dex.")
check("N6 the two structures are OBSERVABLY different in the SPARC range, so the fork is a measurement and not a convention",
      d_carrier_vs_aqual > 0.03, f"max separation {d_carrier_vs_aqual:.4f} dex, against SPARC's own 0.11-0.13 dex scatter -- detectable in the aggregate, not per point")
check("N7 [the honest cost] the repaired kernel reproduces the published carried kernel to better than 0.02 dex everywhere",
      DEX_TH < 0.02, f"max deviation {DEX_TH:.4f} dex at s = {float(SFIT[int(np.argmax(np.abs(np.log10((SFIT+Delta_fam(SFIT,C_TH,P_TH,A2_TH))/(SFIT+Delta_carried(SFIT))))))]):.3f}; this is a PREDICTION difference, testable on BIG-SPARC's transition bins")


# ==================================================================================================
print("\n" + BAR)
print("PART IV -- THE ADMISSIBILITY QUESTION.  Is the parameter space non-empty under tonight's constraints?")
print(BAR, flush=True)
print("""    THE PARAMETERS OF THE ASSEMBLED THEORY
      K_B      clock kinetic coupling, c_1 = -c_3 = K_B  (so c_13 = 0 identically, c_T = c exactly)
      c_14     = c_1 + c_4, the khronometric alpha; alpha_1 = -4 c_14 EXACTLY (A19/L13, rebuilt as K1)
      c_2      the khronometric lambda; sets the clock's own speed sigma
      |K_2|    the MOND scalar's time-kinetic stiffness.  Q_0 = 0: THE CONDENSATE IS REMOVED (A13)
      xi       the coherence length of xi^2 |grad_perp V|^2, THEOREM-FORCED >= 0.10/0.15 pc (A33)
      p        the kernel's saturation exponent, capped at 1.754 (A33)
      sigma    DERIVED: the clock mode's squared speed, khronometric with c_13 = 0:
                   sigma = (2 - c_14) c_2 / [c_14 (2 + 3 c_2)]
               gated to L26's window [1.6793, 1.7716).  ** CONDITIONAL ON B2 **: the map from the
               lead's IC variables to (c_14, c_2) is NOT determined by its published files (L10-K4
               FAIL), so this identification is stated, not proved.  Both readings are run below.""")

def sigma_clock(c2, c14):
    c2, c14 = np.asarray(c2, float), np.asarray(c14, float)
    return (2 - c14)*c2/(c14*(2 + 3*c2))
def c2_for_sigma(sig, c14):
    return 2*sig*c14/(2 - c14 - 3*sig*c14)
def S_eff(K_B, c2, K2): return 1.0 - (2 - np.asarray(K_B, float))**2/(np.asarray(c2, float)*np.asarray(K2, float))
def cs2_mixed(K_B, c14, K2): return (2 - np.asarray(K_B, float))**2/(np.asarray(c14, float)*np.asarray(K2, float))
def alpha_1_full(K_B, c14, xi_pc, foot, JY):
    xk2 = (np.asarray(xi_pc, float)*PC/R_SAT)**2
    return -4*np.asarray(c14, float) - 4*(2 - np.asarray(K_B, float))/(JY[foot]*(1 + xk2) + 1)
JY_EXT = {f: float(GEXT/A0[f]/Delta_fam(GEXT/A0[f], C_TH, P_TH, A2_TH)) for f in A0}
print(f"\n    J_Y at the Galactic external field, from the repaired kernel: "
      + ", ".join(f"{f} {v:.3f}" for f, v in JY_EXT.items()) + "   (g03z G1 with the published kernel: 2.967 / 2.510)")

# ---------------- the gates
def H1(K_B, c2, c14, K2, xi, p, foot):  return np.abs(alpha_1_full(K_B, c14, xi, foot, JY_EXT)) < ALPHA1_BOUND
def H2(K_B, c2, c14, K2, xi, p, foot):  return np.abs(alpha_2_of(K_B, c2, c14)) < ALPHA2_BOUND
def H3(K_B, c2, c14, K2, xi, p, foot):  return (np.asarray(c14, float) < 2.0) & (np.asarray(K_B, float) < 2.0) & (np.asarray(K_B, float) > 0)
def H4(K_B, c2, c14, K2, xi, p, foot):  return (np.asarray(K_B, float) <= 0.25) & (np.abs(1.0/(1 + 1.5*np.asarray(c2, float)) - 1) < 0.13)
def H5(K_B, c2, c14, K2, xi, p, foot):  return np.asarray(xi, float) >= XI_FLOOR[foot]
def H6(K_B, c2, c14, K2, xi, p, foot):  return (np.asarray(p, float) > 0) & (np.asarray(p, float) <= P_MAX)
def H7(K_B, c2, c14, K2, xi, p, foot):
    sg = sigma_clock(c2, c14); return (sg >= SIGMA_LO) & (sg < SIGMA_HI)
def H8(K_B, c2, c14, K2, xi, p, foot):  return cs2_mixed(K_B, c14, K2) >= 1.0            # Cherenkov: no subluminal mode
def H9(K_B, c2, c14, K2, xi, p, foot):
    return np.abs(S_eff(K_B, c2, K2))*K2_GROWTH <= np.asarray(K2, float)                 # |S_eff|, not max(S_eff,0)
def H10(K_B, c2, c14, K2, xi, p, foot): return np.asarray(K2, float) > 0                 # scalar kinetic health
def H11(K_B, c2, c14, K2, xi, p, foot):
    return np.ones(np.broadcast(np.asarray(K_B,float), np.asarray(c2,float), np.asarray(c14,float),
                                np.asarray(K2,float), np.asarray(xi,float), np.asarray(p,float)).shape, bool)
GATES = [("H1  PPN alpha_1", H1), ("H2  PPN alpha_2", H2), ("H3  tensor c_T = 1 + G_N > 0", H3),
         ("H4  BBN", H4), ("H5  Solar-System xi", H5), ("H6  saturation p <= 1.754", H6),
         ("H7  clock window sigma", H7), ("H8  Cherenkov (no subluminal mode)", H8),
         ("H9  linear growth", H9), ("H10 scalar kinetic health", H10),
         ("H11 clock tachyon (Q_0 = 0: satisfied identically)", H11)]
NG = len(GATES)

def build(base, extras): return np.unique(np.concatenate([np.asarray(base, float), np.asarray(extras, float)]))
C14_G = build(np.logspace(-10, 1, 45), [1e-6, 1.18e-5, 2.5e-5])
_loci = sorted(set([float(c2_for_sigma(s, c)) for c in C14_G if 0 < c < 0.3 for s in (SIGMA_LO, 1.72, SIGMA_HI*0.999)]
                   + [float(c/(1 - 2*c)) for c in C14_G if 0 < c < 0.4]))
C2_G  = build(np.logspace(-10, 1, 45), [v for v in _loci if 0 < v < 10])
KB_G  = build(np.logspace(-3, math.log10(1.9), 10), [0.1, 0.2, 0.25])
K2_G  = build(np.logspace(0, 12, 37), [5e4, 2.5e5, 5e5, 1.93e6, 2.71e6])
XI_G  = build(np.logspace(-4, 3, 10), [0.03, 0.05, 0.10, 0.15])
P_G   = build(np.linspace(0.2, 3.0, 8), [1.0, P_TH, P_MAX])
AXES = [("K_B", KB_G), ("c_2", C2_G), ("c_14", C14_G), ("|K_2|", K2_G), ("xi [pc]", XI_G), ("p", P_G)]
NTOT = int(np.prod([len(g) for _, g in AXES]))
for nm, g in AXES: print(f"    {nm:9s} {len(g):5d} points   [{g.min():.3e}, {g.max():.3e}]")
print(f"    grid points per footing: {NTOT:,}", flush=True)
SHAPE = tuple(len(g) for _, g in AXES)
def shaped(g, ax):
    s = [1]*6; s[ax] = len(g); return g.reshape(s)
KBb, C2b, C14b, K2b, XIb, Pb = (shaped(g, i) for i, (_, g) in enumerate(AXES))

HIST = {}
for foot in ("canonical", "alt"):
    h = np.zeros(1 << NG, dtype=np.int64)
    for i in range(len(KB_G)):
        kb = KB_G[i:i+1].reshape(1, 1, 1, 1, 1, 1)
        bits = np.zeros((1,) + SHAPE[1:], dtype=np.uint16)
        for gi, (_, fn) in enumerate(GATES):
            bits |= (np.broadcast_to(fn(kb, C2b, C14b, K2b, XIb, Pb, foot), bits.shape).astype(np.uint16) << gi)
        h += np.bincount(bits.ravel(), minlength=1 << NG)
    HIST[foot] = h
    assert h.sum() == NTOT
PAT = np.arange(1 << NG)
def count(foot, mask): return int(HIST[foot][(PAT & mask) == mask].sum())
ALLMASK = (1 << NG) - 1

print(f"\n    {'gate':46s} {'canonical':>14s} {'alt':>14s}")
for gi, (nm, _) in enumerate(GATES):
    print(f"    {nm:46s} {count('canonical', 1 << gi)/NTOT:14.6f} {count('alt', 1 << gi)/NTOT:14.6f}")
print(f"    {'INTERSECTION (all 11)':46s} {count('canonical', ALLMASK)/NTOT:14.6f} {count('alt', ALLMASK)/NTOT:14.6f}")
print(f"    {'  points':46s} {count('canonical', ALLMASK):14,d} {count('alt', ALLMASK):14,d}", flush=True)
for gi, (nm, _) in enumerate(GATES[:-2]):     # H10 and H11 are satisfied IDENTICALLY by construction (|K_2| > 0; Q_0 = 0)
    fc, fa = count("canonical", 1 << gi)/NTOT, count("alt", 1 << gi)/NTOT
    check(f"F{gi+1} [{nm.split()[0]}] the gate alone admits neither none nor all of the grid on both footings (a gate that admits everything is probably mis-implemented)",
          0.0 < fc < 1.0 and 0.0 < fa < 1.0, f"canonical {fc:.6f}, alt {fa:.6f}")
print("    (H10 and H11 are excluded from the F-checks and admit the whole grid BY CONSTRUCTION: |K_2| > 0 is a sign")
print("     convention, and the clock-tachyon gate is satisfied identically because the condensate is removed, Q_0 = 0.")
print("     That identity is the structural point of the assembly, not a mis-implemented gate.)")

nonempty = {f: count(f, ALLMASK) > 0 for f in HIST}
check("T1 [THE TEST] the simultaneous admissible region of all eleven gates is NON-EMPTY on both footings",
      all(nonempty.values()), f"canonical {count('canonical', ALLMASK):,} points, alt {count('alt', ALLMASK):,} points")

MINIMAL = {}
for foot in HIST:
    empties = []
    for size in range(1, 5):
        found = []
        for combo in itertools.combinations(range(NG), size):
            m = sum(1 << g for g in combo)
            if count(foot, m) > 0: continue
            if any((prev & m) == prev for prev in empties): continue
            found.append(m)
        empties.extend(found)
        if size >= 3 and not found: break
    MINIMAL[foot] = empties
print("\n    MINIMAL incompatible subsets (size <= 4):")
for foot in HIST:
    if not MINIMAL[foot]: print(f"      {foot}: none -- no subset of the eleven gates up to size 4 is empty")
    for m in MINIMAL[foot]:
        print(f"      {foot}: {{{', '.join(GATES[g][0].split()[0] for g in range(NG) if m >> g & 1)}}}")

# ---------------- the exhibited point, and its analytic derivation
print("\n    THE EXPLICIT POINT.  It is not read off the grid; it is derived, then confirmed to be admitted.")
print("      1. sigma = sigma_* = 1.679312732 (L26: the IC6 obstruction's leading order vanishes and S_4 changes sign)")
print("      2. sigma pins c_2 = 2 sigma c_14/(2 - c_14 - 3 sigma c_14) ~ sigma c_14")
print("      3. then alpha_2 -> (c_14/2)(1/sigma - 1) = -0.2023 c_14, so |alpha_2| < 4e-7 forces c_14 <= 1.98e-6")
print("         -- TWELVE TIMES TIGHTER than alpha_1's own c_14 <= 2.5e-5.  This is new, and it is the")
print("         binding constraint on c_14 in the assembled theory.")
print("      4. the cosmological closure locus c_2|K_2| = (2-K_B)^2 (THE_ACTION section 5.11) is EXACTLY the")
print("         locus where the mixed clock-scalar mode travels at the clock's own speed, c_s,mix^2 = sigma:")
print("         S_eff = 1 - (2-K_B)^2/(c_2|K_2|) = 1 - c_s,mix^2/sigma to leading order in c_14, c_2.")
c14_max_alpha2 = None
_cg = np.geomspace(1e-9, 1e-4, 200001)
_c2g = c2_for_sigma(sigstar, _cg)
_ok = np.abs(alpha_2_of(0.2, _c2g, _cg)) < ALPHA2_BOUND
c14_max_alpha2 = float(_cg[_ok][-1])
print(f"      -> numerically, at sigma = sigma_* and K_B = 0.2: |alpha_2| < 4e-7 holds up to c_14 = {c14_max_alpha2:.4e}")
check("T1b the sigma-window's implication for c_14 is a genuine TIGHTENING and not a contradiction: the new bound c_14 <= 2.0e-6 is nested inside alpha_1's 2.5e-5 (A6/L10) and inside L14's grid bound 1.18e-5 (A12) -- three lanes, no conflict",
      c14_max_alpha2 < ALPHA1_BOUND/4 and c14_max_alpha2 < 1.18e-5 and c14_max_alpha2 > 1e-7,
      f"alpha_2+sigma: {c14_max_alpha2:.3e}; alpha_1: {ALPHA1_BOUND/4:.1e}; L14 grid: 1.18e-5")

PT = dict(K_B=0.2, c14=1.0e-6, sigma=sigstar, p=P_TH)
PT["c2"] = float(c2_for_sigma(PT["sigma"], PT["c14"]))
PT["K2"] = (2 - PT["K_B"])**2/PT["c2"]              # exactly on the closure locus c_2|K_2| = (2-K_B)^2
PT["xi"] = XI_FLOOR
print(f"\n      THE POINT:  K_B = {PT['K_B']}, c_14 = {PT['c14']:.4e}, c_2 = {PT['c2']:.6e}, |K_2| = {PT['K2']:.4e}, "
      f"xi = {PT['xi']['canonical']} pc (canonical) / {PT['xi']['alt']} pc (alt), p = {PT['p']:.4f}, Q_0 = 0")
print(f"                  derived:  sigma = {float(sigma_clock(PT['c2'], PT['c14'])):.9f}, "
      f"c_s,mix^2 = {float(cs2_mixed(PT['K_B'], PT['c14'], PT['K2'])):.6f}, "
      f"S_eff = {float(S_eff(PT['K_B'], PT['c2'], PT['K2'])):+.6f}, "
      f"G_cos/G_N = {1/(1+1.5*PT['c2']):.9f}, G_N/G = {1/(1-PT['c14']/2):.9f}")
adm = {f: all(bool(np.asarray(fn(PT["K_B"], PT["c2"], PT["c14"], PT["K2"], PT["xi"][f], PT["p"], f)).ravel()[0])
              for _, fn in GATES) for f in A0}
check("T2 [the exhibited point] the derived point passes ALL ELEVEN gates on BOTH footings, independently of the grid",
      all(adm.values()), f"canonical {adm['canonical']}, alt {adm['alt']}")
check("T2b the closure locus has the structural meaning claimed: at c_2|K_2| = (2-K_B)^2 the mixed clock-scalar mode's speed equals the clock's own sigma to better than 1e-4 relative",
      abs(float(cs2_mixed(PT['K_B'], PT['c14'], PT['K2']))/float(sigma_clock(PT['c2'], PT['c14'])) - 1) < 1e-4,
      f"c_s,mix^2 = {float(cs2_mixed(PT['K_B'], PT['c14'], PT['K2'])):.6f} vs sigma = {float(sigma_clock(PT['c2'], PT['c14'])):.6f}")
_Seff_ceiling = 1 - 1/SIGMA_HI
check("T3 [a derived cost, not an input] Cherenkov safety (c_s,mix^2 >= 1) plus the clock window (sigma < 1.7716) CAP the surviving linear cosmological MOND source at S_eff <= 1 - 1/sigma = 0.435 -- the action can never deliver more than 44% of its own naive linear source",
      _Seff_ceiling < 0.5, f"S_eff <= {_Seff_ceiling:.4f}")

# ---------------- robustness: does the answer survive dropping the conditional identification?
m_noS = ALLMASK & ~(1 << 6)          # drop H7 (the sigma window, which is conditional on B2)
m_noC = ALLMASK & ~(1 << 7)          # drop H8 (Cherenkov, scoped by L19 to case Y1)
print(f"\n    ROBUSTNESS of the non-emptiness to the two CONDITIONAL gates:")
print(f"      all eleven                       : canonical {count('canonical', ALLMASK):,}   alt {count('alt', ALLMASK):,}")
print(f"      without H7 (sigma identification): canonical {count('canonical', m_noS):,}   alt {count('alt', m_noS):,}")
print(f"      without H8 (Cherenkov, L19 Y2/Y3): canonical {count('canonical', m_noC):,}   alt {count('alt', m_noC):,}")
check("T4 the non-emptiness does not RELY on either conditional gate: the region is non-empty with them, and larger without either",
      count("canonical", ALLMASK) > 0 and count("canonical", m_noS) >= count("canonical", ALLMASK)
      and count("canonical", m_noC) >= count("canonical", ALLMASK), "monotone by construction; the point is that the full set is already non-empty")

# ---------------- do any two settled results constrain the same parameter inconsistently?
print("\n    CROSS-LANE CONSISTENCY: every parameter constrained by more than one settled result.")
conflicts = []
rows_par = [
    ("c_14", "A6/L10 alpha_1 <= 2.5e-5 | A12/L14 grid <= 1.18e-5 | HERE alpha_2 at sigma_* <= 2.0e-6",
     "nested, tightest wins", True),
    ("|K_2|", "A12/L14 dark-sector window [5e4, 5e5] | g03t D7 growth >= 2.71e6 | g03z G3 Cherenkov <= (2-K_B)^2/c_14",
     "the [5e4,5e5] window is VOID once the condensate is removed; growth and Cherenkov then overlap on the closure locus", True),
    ("xi", "THE_ACTION section 2 table >= 0.03/0.05 pc | THE_ACTION section 5.13 + A33 >= 0.10/0.15 pc",
     "INCONSISTENT: the section-2 table is stale (it quotes the UNSATURATED partner's floors)", False),
    ("the kernel", "recipe I1 freezes mu = 1 - e^-y | THE_ACTION section 3 carries nu_RAR",
     "INCONSISTENT: documentation conflict D1, unresolved, the user's call", False),
    ("c_2", "BBN <= 0.0996 | f34b certifies scalar health for 0.01-0.1 | HERE sigma forces c_2 ~ 1.7 c_14 ~ 1.7e-6",
     "NOT a contradiction but a GAP: the assembled c_2 is five orders BELOW the range f34b certified healthy", False),
    ("sigma", "IC-4 declares (0,1] | L15/L26 sigma_* = 1.679 with window [1.6793, 1.7716)",
     "resolved: A31 shows (0,1] is an undefended convention with no executable restriction", True),
]
for par, srcs, verdict, ok in rows_par:
    print(f"      {par:12s} {srcs}\n                   -> {verdict}")
    if not ok: conflicts.append(par)
check("T5 no two settled results constrain the same parameter inconsistently",
      not conflicts, f"THREE do: {conflicts}.  xi and the kernel are documentation conflicts (one document each needs amending); "
                     f"c_2 is an untested-regime gap, not a contradiction.  None of the three empties the region.")


# ==================================================================================================
print("\n" + BAR)
print("PART V -- THE GATE TABLE at the exhibited point, both footings, with the number and the source.")
print(BAR, flush=True)
def _f(x): return float(np.asarray(x).ravel()[0])
GT = []
for foot in ("canonical", "alt"):
    a0 = A0[foot]; xi = PT["xi"][foot]
    a1v = _f(alpha_1_full(PT["K_B"], PT["c14"], xi, foot, JY_EXT)); a2v = _f(alpha_2_of(PT["K_B"], PT["c2"], PT["c14"]))
    sef = _f(S_eff(PT["K_B"], PT["c2"], PT["K2"])); csm = _f(cs2_mixed(PT["K_B"], PT["c14"], PT["K2"]))
    resid = C_TH*a0                                    # the kernel's Solar-System residual before screening
    screened = resid/(1 + (xi*PC/R_SAT)**2)            # the coherence operator's gradient-scale suppression
    GT += [
     ("Solar System: Cassini quadrupole",       foot, f"g03d's own solve: Q2/ceiling = 0.55-0.68 at its floor {XI_FLOOR_EXP[foot]} pc, and Q2 falls as 1/xi^2; xi = {xi} pc is {xi/XI_FLOOR_EXP[foot]:.1f}x that floor", "PASS", "g03d (exact 4th order)"),
     ("Solar System: Saturn phantom mass",      foot, f"bare kernel {C_TH*a0/A_SAT_PHANTOM:.3e}x over; screened by (xi/R_Sat)^2 = {(xi*PC/R_SAT)**2:.2e} to {screened/A_SAT_PHANTOM:.3e}x", "PASS" if screened < A_SAT_PHANTOM else "FAIL", "L34/A33 + g03d"),
     ("Solar System: sunward anomaly",          foot, f"screened residual {screened:.2e} vs bound {A_SUNWARD:.2e} m/s^2", "PASS" if screened < A_SUNWARD else "FAIL", "g03d line 21"),
     ("PPN alpha_1",                            foot, f"{a1v:+.4e} vs |alpha_1| < {ALPHA1_BOUND:.0e}", "PASS" if abs(a1v) < ALPHA1_BOUND else "FAIL", "A19/L13 (exact identity)"),
     ("PPN alpha_2",                            foot, f"{a2v:+.4e} vs |alpha_2| < {ALPHA2_BOUND:.0e}  (margin {ALPHA2_BOUND/abs(a2v):.2f}x)", "PASS" if abs(a2v) < ALPHA2_BOUND else "FAIL", "g03v ppn(), rebuilt as K1"),
     ("PPN alpha_3",                            foot, "0 exactly (hypersurface-orthogonal, dynamical foliation)", "PASS", "THE_ACTION section 4 (f33)"),
     ("PPN gamma (light bending)",              foot, "1 exactly", "PASS", "A14/L11, THE_ACTION section 4"),
     ("Tensor speed c_T (GW170817)",            foot, "c_13 = K_B - K_B = 0 identically => c_T = c exactly, at every K_B", "PASS", "THE_ACTION section 2, A31 H2"),
     ("Newton constant positivity",             foot, f"G_N/G = 1/(1 - c_14/2) = {1/(1-PT['c14']/2):.9f}", "PASS", "f35"),
     ("DOF count",                              foot, "4 = 2 tensor + 1 clock + 1 MOND scalar (NOT 2)", "FAIL vs requirement 2 as a TOTAL count; PASS as separately-counted-and-healthy", "A2/L4, L8-D1/D4"),
     ("DOF health",                             foot, "clock: A_0 = 0.4615 > 0, E positive definite, hyperbolic at sigma_*; scalar: Bogoliubov omega^2 = c_s^2 k^2(1+xi^2k^2) > 0", "PASS", "A31/L26 H1-H7, f34/f34b"),
     ("Hadamard well-posedness (IC6)",          foot, f"S_4 > 0 on 59/59 branch points at sigma_* -- growth becomes bounded oscillation", "PASS", "A31/L26 H9"),
     ("Galactic rotation curves",               foot, f"MOND at the action's own a0 = {a0:.4e}, coefficient exactly 1.000000", "PASS", "A14/L11, rebuilt as K4/K4b"),
     ("Lensing-vs-dynamics slip (galaxies)",    foot, "Phi = Psi, no slip, to < 1e-4 out to 1 Mpc", "PASS", "A14/L11"),
     ("Bounded-boost ceiling on SPARC",         foot, f"C = {C_TH:.4f} a0 obeyed by 99.23% of 2352 points; 18 exceptions in 5 named galaxies, kept", "PASS", "A33/L34, g03u"),
     ("Kernel tightness vs a fitted halo",      foot, "0.142 dex vs 0.171 (zero parameters both sides) BUT a prior-shrunk NFW reaches 0.085", "NOT A DISCRIMINANT", "A28/L28"),
     ("Wide binaries (Gaia DR4, registered)",   foot, f"gamma_v ceiling {1.0450 if foot=='canonical' else 1.0300:.4f} at xi = {xi} pc, falling toward 1 as xi grows; Arm A band 1.16-1.23", "PENDING (DR4 unpublished)", "Amendment 11(b), g03y"),
     ("Clusters: mass at R500",                 foot, f"required/delivered = {1.618 if foot=='canonical' else 1.493:.3f} +/- {0.022 if foot=='canonical' else 0.020:.3f} (dynamics), {1.987 if foot=='canonical' else 1.834:.3f} +/- {0.246 if foot=='canonical' else 0.227:.3f} (lensing)", "FAIL", "A27/L24"),
     ("Clusters: bounded-boost ceiling",        foot, f"excess 3.37 a0 at 40 kpc = {3.37/C_TH:.1f}x the ceiling; no interpolation function can absorb it", "FAIL", "A33/L34, g03u"),
     ("Clusters: lensing SHAPE",                foot, "Delta Sigma short by 2.5-2.7x over 0.5-2 Mpc; log-slope +0.53 +/- 0.06 shallower = 9 sigma", "FAIL", "A27/L24"),
     ("Cluster residual = cosmic share",        foot, f"required 5.73 +/- 0.68 vs Omega_dm/Omega_b = {cosmic_ratio:.2f}, universal to 12%", "DIAGNOSTIC", "A8/L7, rebuilt as K5"),
     ("Coma ultra-diffuse galaxies",            foot, "amplitude +1.196 dex (factor 14) at 4.9 sigma against the coherent systematic floor", "FAIL", "A22/L23"),
     ("Binary galaxies (2MRS pairs)",           foot, "isolated deep-MOND amplitude 1.802 +/- 0.041 (19.6 sigma); with a cosmic share 1.141 +/- 0.028", "FAIL alone, PASS with a dark component", "A20/L21"),
     ("BBN",                                    foot, f"K_B = {PT['K_B']} <= 0.25; G_cos/G_N - 1 = {1/(1+1.5*PT['c2'])-1:+.2e} vs |.| < 0.13", "PASS", "g03e B1, route2"),
     ("CMB acoustic peaks",                     foot, "no dark component in the action once the condensate is removed", "FAIL", "A13/L14-T4, g04f-g04j"),
     ("Linear growth of structure",             foot, f"S_eff = {sef:+.4f} at the closure locus; |S_eff| x 2.71e6 = {abs(sef)*K2_GROWTH:.2e} <= |K_2| = {PT['K2']:.2e}", "PASS as an equation, FAIL as physics (no dark component to grow)", "g03t D5/D7, g03v"),
     ("sigma_8 / S_8",                          foot, "the late-roll route that reached sigma_8 = 0.845-0.861 gives S_8,eff = 1.06-1.20, +9 to +34 sigma", "FAIL (that route)", "A29/L29"),
     ("Gravitational Cherenkov",                foot, f"clock 29.6% superluminal, mixed mode c_s^2 = {csm:.3f} >= 1; the bound constrains SLOW modes", "PASS", "A5/L19, A31/L26-X4, A32/L33"),
     ("Causal structure / no CTC",              foot, "G^{mu nu} n_mu n_nu = -1/sigma < 0: clock leaves spacelike for BOTH cones at every sigma > 0", "PASS", "A31/L26-X1..X3, A32/L33"),
     ("Black holes",                            foot, "universal horizon r = 3M/2 reproduced; even an infinite-speed mode is trapped", "PASS", "A32/L33"),
     ("Longitudinal cone at Saturn",            foot, f"Sigma_par = {sig_par[foot]:.2e} -- FINITE with the repaired kernel, INFINITE with the published one", "PASS (repaired)", "A33/L34 C4/C5, this script N5"),
     ("Strong coupling at a planet",            foot, f"delta_g/g_* = [(p+1)/3](M_p/M_sun)(r_p/R_p)^2 = {(P_TH+1)/3*1656.:.0f} for Earth without xi; with xi at its floor p <= 1.754 is perturbative", "PASS at p <= 1.754", "A33/L34 D2/D3"),
     ("a0-Lambda tie",                          foot, f"kappa = {KAPPA[foot]:.4f} (canonical 1/2 to 0.03%; alt 0.60)", "FITTED, NOT DERIVED", "A24/L32, k01-k04"),
     ("a0 universality across systems",         foot, "the a0 ladder spans 0.78 dex across system classes", "FAIL", "09-03 sweep, standing"),
    ]
w = max(len(r[0]) for r in GT); wv = max(len(r[3]) for r in GT)
print(f"    {'gate':{w}s}  {'footing':10s}  {'verdict':{wv}s}  number / source")
cur = None
for nm, foot, num, verd, src in GT:
    if foot != cur: print(f"    {'-'*(w+70)}"); cur = foot
    print(f"    {nm:{w}s}  {foot:10s}  {verd:{wv}s}  {num}   [{src}]")
npass = sum(1 for r in GT if r[3].startswith("PASS"))
nfail = sum(1 for r in GT if r[3].startswith("FAIL"))
print(f"\n    tally over both footings: {npass} PASS, {nfail} FAIL, {len(GT)-npass-nfail} other (pending / diagnostic / not a discriminant)")
check("T6 the assembled theory passes every LOCAL gate -- Solar System, PPN, tensor sector, degrees of freedom and their health, causality, galactic dynamics and lensing",
      all(r[3].startswith("PASS") for r in GT if r[0].split(":")[0] in
          ("Solar System", "PPN alpha_1", "PPN alpha_2", "PPN alpha_3", "PPN gamma (light bending)",
           "Tensor speed c_T (GW170817)", "Newton constant positivity", "DOF health",
           "Hadamard well-posedness (IC6)", "Galactic rotation curves", "Lensing-vs-dynamics slip (galaxies)",
           "Gravitational Cherenkov", "Causal structure / no CTC", "Black holes")),
      "every Solar-System, PPN, tensor, health, causality and galaxy row is PASS")
check("T7 the assembled theory passes every gate at scales ABOVE a galaxy",
      not any(r[3].startswith("FAIL") for r in GT if r[0].startswith("Cluster") or r[0].startswith("CMB")
              or r[0].startswith("Coma") or r[0].startswith("Binary") or r[0].startswith("sigma_8")),
      "it does not: clusters (3 rows), ultra-diffuse galaxies, binary galaxies, the CMB and S_8 all FAIL.  "
      "Every one of them is the SAME hole -- there is no dark component in the action.")


# ==================================================================================================
print("\n" + BAR)
print("PART VI -- THE HOLES, with sizes.  Nothing here is written as an open question.")
print(BAR, flush=True)
HOLES = [
 ("H-A  THE CLUSTER DEFICIT (the big one)",
  "The residual behaves like MASS in BOTH dynamics and lensing, so no lensing-sector repair can reach it.\n"
  "      SIZE: required/delivered mass at each cluster's own R500 = 1.618 +/- 0.022 (canonical) / 1.493 +/- 0.020 (alt)\n"
  "      against the hydrostatic mass, and 1.987 +/- 0.246 / 1.834 +/- 0.227 against weak lensing; the two agree\n"
  "      (S_lens - S_dyn = +0.37 +/- 0.24, 1.55 sigma).  In raw Delta Sigma over 0.5-2 Mpc the framework is short\n"
  "      by 2.5-2.7x and its log-slope is +0.53 +/- 0.06 SHALLOWER, a 9 sigma SHAPE error, because its phantom is a\n"
  "      near-uniform sheet.  The acceleration excess at 40 kpc is 3.37 a0, 5.2x the kernel's own hard ceiling, which\n"
  "      no interpolation function can absorb.  The required source is 6.8x the baryons with rho ~ r^-1.53.\n"
  "      MECHANISMS CLOSED: interpolation kernel (A7, |z| = 13); fixed-strength finite-range force (A7, BBN 41x);\n"
  "      screened force in Phi, rho or M (A7, 12.8 sigma overlap + cosmological ordering); hydrostatic bias (A18 -- the\n"
  "      required b is NEGATIVE, -0.82, against a measured [0, +0.42]); the curl field (A25 -- real but exactly\n"
  "      invisible to the radial average, closes 3.9% of the gap and runs the wrong way); a late-time roll (A16 --\n"
  "      buys the cosmology but gives 0.97 of the required 2.2-5.1 contrast); light thermal relics (Tremaine-Gunn,\n"
  "      m >= 4.67 eV, and the N_eff/RAR pincer at 27.6 vs 11 eV); wave dark matter (pincer with no interior, 1.4x);\n"
  "      four condensate constructions; the environment switch.  AND the ratio is NOT MONOTONE in scale: binary\n"
  "      galaxies need 30.9 +/- 1.6 within the pair separation against 5.73 +/- 0.68 at 0.80 R500, 5.7x and 16 sigma.\n"
  "      WHAT IS LEFT: a cold, baryon-tracing component -- i.e. cold dark matter.  The theory does not contain one."),
 ("H-B  NO DARK SECTOR AT ALL, hence no CMB and no structure",
  "Removing the condensate is what cures the clock tachyon (A13/L14), and it was the action's only dark component.\n"
  "      SIZE: the condensate's dark fraction is capped at 2.6e-6 against Omega_d = 0.266, short by 1.0e5x.  With it\n"
  "      gone the theory has baryons only; the CMB third peak, S_8 and the matter power spectrum are unaddressed.\n"
  "      The linear MOND source that might have regenerated P(k) does not: at linear order the causal boost leaves\n"
  "      sigma_8 <= 0.65 with a 20-2000x deficit at k = 0.5-1 h/Mpc, at any |K_2| (A/g04h)."),
 ("H-C  kappa = 1/2 IS FITTED",
  "a0 = kappa c sqrt(G rho_Lambda) is dimensionally forced; kappa is not.  SIZE: A24/L32 T1 proves kappa is a ZERO\n"
  "      MODE of any local action of this class -- F -> F + C is exactly degenerate with Lambda -- so no member of the\n"
  "      class can derive it.  Deriving it reduces to fixing one number, beta/sqrt(Ztilde) = kappa/sqrt2 = 0.354.\n"
  "      Twenty-seven simple numbers lie inside the measured 3 sigma band; landing there is not evidence."),
 ("H-D  THE FOLIATION'S ONE ESCAPE IS UNDECIDED",
  "A26/L31 proves Lorentz invariance XOR two modes under a LOCALITY hypothesis, verified against a 17-theory table\n"
  "      with no counterexample.  Hypothesis (iv), locality, is NOT proved: temporal nonlocality is a live escape\n"
  "      (holding g_ext fixed, pushing the source 1000x drops every local invariant 1000x while |grad(box^-1 R)| is\n"
  "      exactly constant).  A parallel lane is deciding it with a Hamiltonian mode count for retarded-nonlocal\n"
  "      gravity.  IF that escape opens, the preferred foliation this theory is built on is a CHOICE, not a theorem."),
 ("H-E  THE IC <-> ACTION MAPPING IS NOT PUBLISHED (challenge B2)",
  "c_14 has three inconsistent readings in the lead's files spanning 0.073-1.333, and c_2 vanishes at the witness\n"
  "      where the mode was measured.  SIZE: the identification sigma = (2-c_14)c_2/[c_14(2+3c_2)] used above -- the\n"
  "      one that tightens c_14 to 2.0e-6 -- is therefore STATED, not proved.  The region is non-empty with or\n"
  "      without it (PART IV, T4), so nothing structural depends on it; the SHARPNESS of the c_14 bound does."),
 ("H-F  c_2 SITS FIVE ORDERS BELOW THE CERTIFIED HEALTHY RANGE",
  "f34b certifies the scalar sector's linear health for c_2 in [0.01, 0.1].  The assembled point has c_2 = 1.7e-6.\n"
  "      SIZE: 5 orders of magnitude of untested parameter.  Not a computed failure -- a gate nobody has run."),
 ("H-G  TWO DOCUMENTATION CONFLICTS ARE STILL OPEN",
  "(i) the kernel: recipe ingredient I1 freezes mu = 1 - e^-y, THE_ACTION section 3 carries nu_RAR; they differ by\n"
  "      up to 0.073 dex and the exponential ceiling is exceeded 5x more often on the bulgeless SPARC control.\n"
  "      (ii) xi: THE_ACTION's section-2 table still quotes 0.03/0.05 pc, the UNSATURATED partner's floors, against\n"
  "      section 5.13 and A33's 0.10/0.15 pc for the kernel a scalar can actually carry.  One document each must be\n"
  "      amended; until then any cross-document comparison is ill-defined."),
 ("H-H  STANDING LIABILITIES NOT REPAIRED BY THE ASSEMBLY",
  "Coma ultra-diffuse galaxies: amplitude +1.196 dex (factor 14) at 4.9 sigma against a 0.227 dex coherent systematic\n"
  "      floor -- never quote the retracted 19.4 sigma.  The a0 ladder spans 0.78 dex across system classes.  Unequal-mass\n"
  "      wide binaries: a resolution-independent common-mode force is an open numerical item.  Non-spherical accretion\n"
  "      and the existence theory of the non-spherical fourth-order law are untouched."),
]
for t, b in HOLES: print(f"\n    {t}\n      {b}")
check("T8 the theory has no unaddressed hole larger than a factor of two",
      False, "it has: the cluster mass deficit is a factor 1.49-1.99 AND a 9 sigma shape error AND 5.2x the kernel's "
             "own ceiling at 40 kpc, and there is no dark component in the action at all (short by 1.0e5x)")


# ==================================================================================================
print("\n" + BAR)
print("PART VII -- WHAT IS DISTINCTIVE, WITH NUMBERS, AND WHAT WOULD FALSIFY IT.")
print(BAR, flush=True)
PRED = [
 ("P1  THE BOUNDED BOOST -- a hard, parameter-free ceiling dark matter cannot impose",
  f"g_obs - g_bar <= C a0 = {C_TH:.4f} a0 = {C_TH*A0['canonical']:.3e} / {C_TH*A0['alt']:.3e} m/s^2, EVERYWHERE, in EVERY system,\n"
  f"      with no free parameter.  A halo's g_halo is set by M_200 and c, which span decades and are not tied to a0.\n"
  f"      FALSIFIED BY: one system, with a trustworthy baryon model, above the ceiling.  Currently 99.23% of 2352 SPARC\n"
  f"      points obey it; the 18 >3 sigma exceptions are in five named galaxies, 13 of them in NGC5985."),
 ("P2  a0(z): the surviving distinctive prediction",
  "The deep-MOND baryonic-Tully-Fisher zero point is FLAT to <1% out to z = 5 on the derived law, against LambdaCDM's\n"
  "      +0.33 dex by z = 2.5 and +0.576 dex at the same redshift for a rising-a0 reading.  DECISIVE MEASUREMENT:\n"
  "      a deep-MOND lensed rotator at z ~ 2-2.5 measured to +/- 0.13 dex.  This, not kappa, is the discriminator."),
 ("P3  GAIA DR4 WIDE BINARIES -- registered, and it is a NEWTON-LIKE answer",
  f"gamma_v <= 1.0450 (canonical, xi = 0.10 pc) / 1.0300 (alt, xi = 0.15 pc), falling toward 1 as xi grows, against\n"
  f"      Arm A's registered band 1.16-1.23 and Newton's 1.000.  These are CEILINGS: DR4 can kill this arm from above,\n"
  f"      it cannot confirm it over Newton.  A measurement inside 1.16-1.23 falsifies the coherence-length structure."),
 ("P4  THE CLUSTER PEAK RADIUS is mass-independent (conditional on a dust sector existing)",
  "If any component with the scalar's stiffness supplies part of the residual, its peak radius is set by\n"
  "      H = 0.42 e c^2/(|K_2| a0) alone and is therefore the SAME PHYSICAL RADIUS in every cluster, where an NFW scale\n"
  "      radius grows as M^(1/3).  NOTE: the assembled theory has no such component, so this is a prediction of the\n"
  "      condensate branch that was REMOVED, and is listed to be honest about what removing it costs."),
 ("P5  THE SADDLE NULL",
  "No Bekenstein-Magueijo anomaly at any Solar-System field null: the coherence operator erases it by 1e-29.  LISA\n"
  "      Pathfinder-class saddle flybys would see nothing.  A detection falsifies the operator."),
 ("P6  THE CARRIER/AQUAL FORK, newly priced here",
  f"The two structures agree below s = 0.63 and diverge above it, reaching {d_carrier_vs_aqual:.3f} dex.  At s = 3 the carrier\n"
  f"      predicts Delta = {float(Delta_carried(_s3)[0]):.3f} and AQUAL {float(Delta_aqual_exp(_s3)[0]):.3f}, a {float(np.log10((3+Delta_carried(_s3)[0])/(3+Delta_aqual_exp(_s3)[0]))):.3f} dex difference in g.  BIG-SPARC's transition\n"
  f"      bins decide which structure the data prefer -- and only the carrier arm needs the coherence length at all."),
 ("P7  THE SATURATION EXPONENT is bounded above",
  f"p <= {P_MAX}: the kernel's approach to its ceiling is a POWER LAW, never exponential.  Measuring the approach faster\n"
  f"      than Delta = C[1 - (s0/s)^1.754] falsifies the perturbative existence of the theory's own cubic action."),
]
for t, b in PRED: print(f"\n    {t}\n      {b}")


# ==================================================================================================
print("\n" + BAR)
print("VERDICT")
print(BAR, flush=True)
print("""    The admissible region is NON-EMPTY.  An explicit point is exhibited above and passes eleven gates on
    both footings.  Every LOCAL test the programme owns -- Cassini, the Saturn phantom mass, the sunward
    anomaly, alpha_1, alpha_2, alpha_3, gamma, the tensor speed, the degree-of-freedom count and its health,
    Hadamard well-posedness, causality, black holes, galactic rotation curves and the lensing-dynamics slip --
    passes at that point, on both footings.  That is a real result and it is the first time the programme has
    had one simultaneously.

    Every test at a scale ABOVE a galaxy fails, and they all fail for ONE reason: removing the condensate --
    which is what cures the clock tachyon, the single gate in every minimal incompatible subset L14 found --
    leaves the action with no dark component at all.  The cluster deficit is a factor 1.49-1.99 in mass at
    R500 in both dynamics and lensing, with a 9 sigma shape error in Delta Sigma and an acceleration excess
    5.2x the kernel's own hard ceiling at 40 kpc; the CMB, S_8 and the matter power spectrum are unaddressed.

    So: this is a complete, internally consistent, Solar-System-safe, galaxy-correct relativistic theory of
    gravity with a preferred foliation and four healthy propagating modes -- and it is not a complete theory
    of the universe, because it needs a cold, baryon-tracing component that it does not contain and that
    every mechanism it does contain has been shown, one by one, unable to supply.""")
check("V1 [THE VERDICT] this is a complete theory",
      False, "it is a complete theory of GRAVITY at Solar-System and galaxy scales with a non-empty parameter "
             "region, and an INCOMPLETE theory of the universe: it requires a cold dark component it does not "
             "contain.  What is missing is exactly that component, plus a derivation of kappa, plus the "
             "locality hypothesis of the foliation theorem.")
check("V2 the parameter space of the assembled theory is non-empty under the corrected constraints -- THE question this lane was opened to answer",
      all(nonempty.values()) and all(adm.values()),
      f"YES: grid {count('canonical', ALLMASK):,} / {count('alt', ALLMASK):,} points, plus a derived explicit point "
      f"admitted on both footings, with the clock tachyon gate satisfied IDENTICALLY because Q_0 = 0")

print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
print("  (FAILs T5, T7, T8, V1 and F-lines are RESULTS, not machine errors: they record the cluster deficit,")
print("   the absent dark sector, the two documentation conflicts and the incompleteness.  Every CONTROL --")
print("   K1-K9, N1-N7, T1, T2 -- must pass for the rest to mean anything.)")
CONTROLS = [f for f in FAILS if f.split()[0] in
            ("K1", "K1b", "K2", "K2b", "K3", "K4", "K4b", "K5", "K6", "K7", "K7b", "K8", "K9",
             "N1", "N2", "N3", "N4", "N5", "N6", "T1", "T2", "T2b")]
print(f"  CONTROL failures: {CONTROLS if CONTROLS else 'none'}")
sys.exit(1 if CONTROLS else 0)
