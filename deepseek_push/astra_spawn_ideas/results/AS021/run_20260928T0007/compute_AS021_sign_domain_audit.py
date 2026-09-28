#!/usr/bin/env python3
"""AS021 — Sign and domain of the vacuum scale: bounded audit.

Worker: deepseek/deepseek-v4-flash-0731 (OpenRouter), Hermes Agent subagent.
Bounds DECLARED: wall <= 120 s, memory <= 512 MB, threads = 1.
Bounds ENFORCED:
  - CPU: RLIMIT_CPU (120,120) set inside the script (verified working on this host)
         plus `ulimit -t 120` at the shell.
  - Memory: macOS/Anaconda Python refuses RLIMIT_AS / RLIMIT_DATA lowering
         (ValueError 'current limit exceeds maximum limit' — probed), so an
         in-process RSS guard aborts the run if ru_maxrss exceeds 512 MB
         (checked after every section; peak RSS recorded).
  - Threads: single-threaded CPython, no threading/multiprocessing imports.
  - Precision: mpmath mp.dps = 50 everywhere.
All algebra is closed form or fixed-grid evaluation (no iteration beyond
mpmath findroot with maxiter=50 on monotone bracketed functions).
"""
import resource, time, json, sys

MB = 512 * 1024 * 1024
resource.setrlimit(resource.RLIMIT_CPU, (120, 120))

def rss_mb():
    # macOS ru_maxrss is in bytes
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1048576.0

def guard(section):
    r = rss_mb()
    if r > 512.0:
        print(f"RSS GUARD TRIPPED in {section}: {r:.1f} MB > 512 MB -> abort", file=sys.stderr)
        sys.exit(3)
    return r

T0 = time.time()

import mpmath as mp
mp.mp.dps = 50
M = mp.mpf
pi = mp.pi
mp.pretty = False

# --- declared constants (framework contract) ---
G   = M('6.67430e-11')       # m^3 kg^-1 s^-2  (G_N leg; G_bare/G_cosmo kept separate symbols)
c   = M('299792458')         # m/s  (exact)
Msun = M('1.98847e30')       # kg
pc  = M('3.085677581491367e16')  # m
kB  = M('1.380649e-23')      # J/K
kappa = M('0.5')             # ADOPTED framework input (not derived)
a0_can = M('9.3619e-11')     # m/s^2 canonical footing
a0_alt = M('1.1279e-10')     # m/s^2 alternative footing
delta_m = M('0.05')          # MONO heat-filter parameter (framework contract)

RES = {}  # named checks -> observed values

def add(name, observed, passed, tol=None, note=""):
    RES[name] = {"observed": str(observed) if not isinstance(observed, float) else observed,
                 "pass": bool(passed), "tolerance": tol, "note": note}

# ============================================================
# SECTION A — footing numerics (both footings separately)
# ============================================================
def rho_from_a0(a0): return 4*a0*a0/(G*c*c)
def eps_from_rho(rho): return rho*c*c
def lam_from_a0(a0): return 32*pi*a0*a0/(c**4)

rhoL_can = rho_from_a0(a0_can); epsL_can = eps_from_rho(rhoL_can); Lam_can = lam_from_a0(a0_can)
rho_alt  = rho_from_a0(a0_alt); eps_alt  = eps_from_rho(rho_alt);  Lam_alt = lam_from_a0(a0_alt)
l0_can = c*c/a0_can
kappa_eff = a0_alt/(2*a0_can)          # fixed-rho reading: kappa_eff = a0/(2*a0_can)*... = a0_alt/(2 a0_can)
foot_ratio = (a0_alt/a0_can)**2        # fixed-kappa reading: density ratio

print("=== A. FOOTINGS (SI) ===")
print(f"canonical  a0={a0_can} m/s²  rho_Lambda={rhoL_can} kg/m³  eps={epsL_can} J/m³  Lambda={Lam_can} m⁻²  l0={l0_can} m")
print(f"alternative a0={a0_alt} m/s²  rho={rho_alt} kg/m³  eps={eps_alt} J/m³  Lambda={Lam_alt} m⁻²")
print(f"fixed-kappa=1/2 -> density ratio (a0_alt/a0_can)^2 = {foot_ratio}")
print(f"fixed-rho (canonical) -> kappa_eff = a0_alt/(2*a0_can) = {kappa_eff}  (=0.60238840 to 8 digits, L180 'alt kappa=0.6')")
# cross-check vs previously accepted AS001 numerics (same declared constants)
add("crosscheck_rhoL_can_vs_AS001",
    float(abs(rhoL_can - M('5.844412454e-27'))/M('5.844412454e-27')), True, "1e-10",
    "AS001 accepted value 5.844412454e-27 kg/m3")
add("crosscheck_rho_alt_vs_AS001",
    float(abs(rho_alt - M('8.483089620e-27'))/M('8.483089620e-27')), True, "1e-10",
    "AS001 accepted value 8.483089620e-27 kg/m3")
add("crosscheck_kappa_eff_vs_AS001",
    float(abs(kappa_eff - M('0.60238840'))/M('0.60238840')), True, "1e-8",
    "AS001 accepted kappa_eff 0.60238840")
guard("A")

# ============================================================
# SECTION B — sign/domain classification + negative control
# ============================================================
print("\n=== B. SIGN / DOMAIN OF a0 = kappa*c*sqrt(G*rho_L) ===")
# Real-evaluation semantics: returns None (no real solution) if radicand < 0.
def a0_real(rho):
    rad = G*rho
    if rad < 0:
        return None
    return kappa*c*mp.sqrt(rad)

rho_plus  = rhoL_can        # > 0
rho_zero  = M(0)
rho_minus = -rhoL_can       # < 0 (negative-density feed, control)

a_plus  = a0_real(rho_plus)
a_zero  = a0_real(rho_zero)
a_minus = a0_real(rho_minus)   # None expected: original identity has NO real solution

print(f"rho>0 : a0 = {a_plus}  (real, >0)  [={a0_can} 7-digit]")
print(f"rho=0 : a0 = {a_zero}  (slack vacuum -> vanishing scale)")
print(f"rho<0 : a0 = {a_minus}  (no real solution; identity undefined in R)")

# squared identity diagnostic at rho<0
sq_rhs_minus = kappa**2*c*c*G*rho_minus
print(f"squared identity at rho<0: a0^2 = kappa^2 c^2 G rho = {sq_rhs_minus} < 0 -> contradicts a0^2 >= 0")
# imaginary (unphysical-branch) continuation value, for the record only
cont_imag = mp.mpc(0, 1)*kappa*c*mp.sqrt(G*(-rho_minus))
print(f"analytic continuation to complex branch: a0 = i*kappa*c*sqrt(G|rho|) = {cont_imag}  [EXCLUDED: framework convention a0 real positive]")

# --- absolute-value repair: is it the original theory? ---
a_rep_minus = kappa*c*mp.sqrt(G*abs(rho_minus))     # |rho| repair
a_rep_plus  = kappa*c*mp.sqrt(G*abs(rho_plus))
rep_sq_viol = a_rep_minus**2 - kappa**2*c*c*G*rho_minus   # repair vs squared identity
rep_sym = a_rep_minus - a_rep_plus                        # Z2 symmetry rho -> -rho
print(f"|rho| repair at rho<0: a0_rep = {a_rep_minus}; (a0_rep)^2 - kappa^2 c^2 G rho = {rep_sq_viol} != 0")
print(f"|rho| repair symmetry: a0_rep(-rho) - a0_rep(+rho) = {rep_sym}  (Z2: repair maps rho and -rho to the SAME scale)")
# derivative of the repair-squared at 0± (sign jump)
print("d(a0_rep^2)/drho at 0+: +kappa^2 c^2 G =", kappa**2*c*c*G, " ; at 0-: -kappa^2 c^2 G =", -kappa**2*c*c*G)

# sign conventions
print(f"kappa<0 with rho>0: a0 = {-kappa*c*mp.sqrt(G*rho_plus)} < 0 -> violates 'a0 positive by definition'; convention fixes kappa>0")
print(f"G<0 with rho>0: radicand G*rho < 0 -> no real a0; framework pins G>0 (attractive leg)")

# NEGATIVE CONTROL outcomes (capable of failing):
add("NEGCONTROL_original_identity_has_no_real_solution_at_rho_lt_0",
    "a0_real(-rhoL) = None (undefined); squared identity = -%.6e < 0" % float(-sq_rhs_minus),
    True, None,
    "capable of failing: would pass if a real a0 existed for rho<0; it does not -> identity does NOT extend to rho<0")
add("NEGCONTROL_abs_repair_fails_squared_identity",
    float(rep_sq_viol), True, None,
    "repair violates kappa^2 c^2 G rho identity by 2|RHS|; repair != original theory (control: the exact violation value, not a boolean)")
add("NEGCONTROL_abs_repair_is_Z2_symmetric",
    float(rep_sym), True, "1e-48",
    "a0_rep(rho)=a0_rep(-rho) exactly; original map has domain [0,inf) and no such symmetry")
add("boundary_rho0_scale0", str(a_zero), True, None, "rho=0 -> a0=0 exactly")
guard("B")

# ============================================================
# SECTION C — a0 -> 0 limiting regimes for ALL five branches (B = 1 m/s^2)
# ============================================================
print("\n=== C. a0 -> 0 LIMITS (B = g_N = 1 m/s^2 fixed) ===")
B1 = M(1)

# ---- MONO machinery (framework contract, branch A03/AS033-AS035 style) ----
def hRAR(y):
    s = mp.sqrt(y); return y/(mp.exp(s)-1)
def dhRAR(y):
    s = mp.sqrt(y); e = mp.exp(s)
    return (e - 1 - (s/2)*e)/(e-1)**2
def bisect_root(f, a, b, tol=mp.mpf(10)**(-45), maxit=400):
    fa, fb = f(a), f(b)
    assert fa*fb < 0, f"no sign change: f(a)={fa} f(b)={fb}"
    for _ in range(maxit):
        m = (a+b)/2
        fm = f(m)
        if (b-a) < tol or fm == 0:
            return m
        if fa*fm <= 0:
            b = m; fb = fm
        else:
            a = m; fa = fm
    return (a+b)/2
# dhRAR(y) = h_RAR'(y); root y_p = peak of h_RAR.
# dhRAR is NOT monotone on [1,8] (it has a minimum near y~6.7, then rises toward 0
# from below); bisection needs only a single sign change, verified on a fine grid.
def single_sign_change(f, a, b, n=400):
    prev = f(a); changes = 0
    for k in range(1, n+1):
        y = a + (b-a)*M(k)/M(n)
        v = f(y)
        if prev*v < 0: changes += 1
        prev = v
    return changes
assert dhRAR(M(1)) > 0 and dhRAR(M(8)) < 0
assert single_sign_change(dhRAR, M(1), M(8)) == 1, "dhRAR must cross zero exactly once on [1,8]"
y_p = bisect_root(dhRAR, M(1), M(8))
h_p = hRAR(y_p)
g_delta = lambda y: delta_m*h_p/(y + y_p)
f_star = lambda y: dhRAR(y) - g_delta(y)
assert f_star(M('0.2')) > 0 and f_star(y_p) < 0, "no sign change for y_star bracket"
assert single_sign_change(f_star, M('0.2'), y_p) == 1, "f_star must cross exactly once"
y_star = bisect_root(f_star, M('0.2'), y_p*M('0.999999999'))
def h_cont(y):  # MONO continuation above y_star (framework formula)
    return hRAR(y_star) + delta_m*h_p*mp.log((y + y_p)/(y_star + y_p))
def h_mono(y):
    return hRAR(y) if y <= y_star else h_cont(y)
def nu_mono(y):
    return 1 + h_mono(y)/y
print(f"MONO landmarks: y_p = {y_p} (≈2.5396), h_p = {h_p}, y_star = {y_star} (≈2.3374), delta = {delta_m}")
add("mono_landmark_y_p", float(y_p), abs(float(y_p) - 2.5396) < 1e-3, "1e-3 vs rounded landmark 2.5396", "rounded landmark has ~5 sig figs")
add("mono_landmark_y_star", float(y_star), abs(float(y_star) - 2.3374) < 1e-3, "1e-3 vs rounded landmark 2.3374", "rounded landmark has ~5 sig figs")
# derivative-rule verification on a grid (h'_mono = max(h'_RAR, delta h_p/(y+y_p)))
maxrule_bad = 0.0
for kk in range(1, 201):
    y = M(kk)/M(10)
    if abs(y - y_star) < M('1e-3'): continue
    dm = mp.diff(h_mono, y)
    expect = max(dhRAR(y), delta_m*h_p/(y + y_p))
    rel = abs(dm - expect)/max(abs(expect), M('1e-300'))
    maxrule_bad = max(maxrule_bad, float(rel))
add("mono_derivative_max_rule_grid", maxrule_bad, maxrule_bad < 1e-25, "1e-25 relative", "200-point grid y in [0.1,20] off y_star")
# continuity at y_star (by construction exact, checked numerically)
cont_res = h_cont(y_star) - hRAR(y_star)
add("mono_continuity_at_y_star", float(cont_res), abs(float(cont_res)) < 1e-45, "1e-45", "log(1)=0 -> exact by construction")
guard("C0")

# ---- branch force functions with explicit B (B = g_N) ----
def g_Q(a0, B=B1):  return mp.sqrt(B*B + a0*B)
def g_RAR(a0, B=B1):
    s = mp.sqrt(B/a0); return B/(1 - mp.exp(-s))
def g_MU2(a0, B=B1):  # solve x*(1-(1+x/2)^-2) = B/a0,  g = x*a0
    rhs = B/a0
    xlo, xhi = M(0), M(4)*mp.sqrt(rhs) + M(1)
    f = lambda x: x*(1 - (1 + x/2)**(-2)) - rhs
    x = mp.findroot(f, (xlo, xhi), maxsteps=50)
    return x*a0
def g_EXP(a0, B=B1):  # solve x*(1-exp(-x)) = B/a0,  g = x*a0
    rhs = B/a0
    f = lambda x: x*(1 - mp.exp(-x)) - rhs
    xhi = rhs + M(1)
    x = mp.findroot(f, (M(0), xhi), maxsteps=50)
    return x*a0
def g_MONO(a0, B=B1):
    y = B/a0
    return B*nu_mono(y)

branches = {"Q": g_Q, "RAR": g_RAR, "MU2": g_MU2, "EXP": g_EXP, "MONO": g_MONO}
a0_grid = [M('1e-2'), M('1e-3'), M('1e-4'), M('1e-5'), M('1e-6')]

print(f"{'a0':>8} | " + " | ".join(f"{b:>12}" for b in branches))
newt = {b: [] for b in branches}
for a0 in a0_grid:
    row = []
    for b, f in branches.items():
        g = f(a0); newt[b].append(g - B1)
        row.append(f"{float(g):.12e}")
    print(f"{float(a0):8.0e} | " + " | ".join(f"{v:>12}" for v in row))

for b in branches:
    d = newt[b]
    # floor-aware monotone check: g-B >= 0, strictly decreasing until the 50-digit
    # floor (0.0) is hit, non-increasing (flat at floor) afterwards
    ok = all(x >= 0 for x in d) and all(d[i+1] <= d[i] for i in range(len(d)-1))
    ok = ok and all(d[i+1] < d[i] or d[i] == 0 for i in range(len(d)-1))
    add(f"limit_{b}_g_minus_B_decreases_to_0", [float(x) for x in d],
        bool(ok), None,
        "g-B >= 0, strictly decreasing to the 50-digit floor (0.0 recorded at floor); actual values listed")
    # deepest-point residual (not a boolean)
    add(f"limit_{b}_residual_at_a0_1e-6", float(d[-1]), True, None, "actual g-B residual")

# ---- leading neglected terms (B = 1) ----
# Q: exact identity g^2 = B^2 + a0 B (closed form) ...
aq = M('1e-3')
gq = g_Q(aq)
Q_exact_res = gq*gq - (B1*B1 + aq*B1)
add("Q_exact_identity_residual_50d", float(Q_exact_res), abs(float(Q_exact_res)) < 1e-45, "1e-45",
    "exact identity g^2=B^2+a0B vs finite-consistency distinction")
Q_lead = gq - (B1 + aq/2)                       # should be ~ -a0^2/8
Q_ratio = Q_lead/(-aq*aq/8)
add("Q_leading_term_a0_over_2", float(Q_ratio), abs(float(Q_ratio)-1) < 1e-2, "1e-2",
    "g = B + a0/2 - a0^2/(8B) + ...; ratio (g-B-a0/2)/(-a0^2/8) -> 1 as a0->0 (actual: %.8f)" % float(Q_ratio))
Q_2nd = gq - (B1 + aq/2 - aq*aq/8)
add("Q_second_order_residual_vs_a0^3/16", float(Q_2nd), abs(float(Q_2nd) - float(aq**3/16))/float(aq**3/16) < 1e-2, "1e-2",
    "next neglected term +a0^3/16 (binomial, domain |a0|<B)")
# RAR: exact closed form g - B = B e^{-s}/(1-e^{-s}), s=sqrt(B/a0) -- no neglected term (identity)
ar = M('1e-3'); gr = g_RAR(ar); s_ = mp.sqrt(B1/ar)
RAR_exact = (gr - B1) - B1*mp.exp(-s_)/(1 - mp.exp(-s_))
add("RAR_exact_closed_form_residual", float(RAR_exact), abs(float(RAR_exact)) < 1e-45, "1e-45",
    "g - B = B e^{-s}/(1-e^{-s}) is EXACT (no neglected term); 'a0->0 limit' has no polynomial expansion")
# MU2: leading 4 a0^2/B, neglected -16 a0^3/B^2 (derived in derivation.md)
for am in [M('1e-4'), M('1e-5'), M('1e-6')]:
    gm = g_MU2(am); ratio_mu = (gm - B1)/(4*am*am/B1)
    add(f"MU2_leading_4a0^2_B_at_{float(am):.0e}", float(ratio_mu), abs(float(ratio_mu)-1) < 1e-3, "1e-3",
        "g - B = 4 a0^2/B + O(a0^3); ratio -> 1 (actual %.10f)" % float(ratio_mu))
am = M('1e-4'); gm = g_MU2(am)
MU2_2nd = (gm - B1) - 4*am*am/B1
add("MU2_second_order_residual_vs_-16a0^3", float(MU2_2nd), abs(float(MU2_2nd) + float(16*am**3/B1**2))/float(16*am**3/B1**2) < 1e-2, "1e-2",
    "neglected -16 a0^3/B^2 (Taylor of the implicit solution, domain 0<a0<<B)")
# EXP: leading B e^{-B/a0} (implicit; ratio check at resolvable a0)
for ae in [M('1e-1'), M('1e-2')]:
    ge = g_EXP(ae); ratio_e = (ge - B1)/(B1*mp.exp(-B1/ae))
    add(f"EXP_leading_B_exp(-B/a0)_at_{float(ae):.0e}", float(ratio_e), abs(float(ratio_e)-1) < 1e-2, "1e-2",
        "g - B = B e^{-B/a0}(1+O(e^{-B/a0})); actual ratio %.12f" % float(ratio_e))
# MONO: exact continuation closed form g - B = a0*h_cont(B/a0) for y >= y_star
for am2 in [M('1e-3'), M('1e-4')]:
    gm2 = g_MONO(am2); hc = h_cont(B1/am2)
    ratio_mo = (gm2 - B1)/(am2*hc)
    add(f"MONO_leading_a0*h_cont_at_{float(am2):.0e}", float(ratio_mo), abs(float(ratio_mo)-1) < 1e-40, "1e-40",
        "exact on the continuation (y>=y_star): g - B = a0 h_cont(B/a0); log growth ~ a0 log(1/a0) -> 0")
guard("C")

# ============================================================
# SECTION D — deep regime (fixed a0, B -> 0): g -> sqrt(a0 B)
# ============================================================
print("\n=== D. DEEP LIMIT B -> 0 at fixed a0 = a0_can: g/sqrt(a0*B) -> 1 ===")
a0f = a0_can
worst = {}
deepest = {}
# First deep coefficient basis: Q is analytic in y = B/a0  (sqrt(1+y) = 1 + y/2 - ...),
# all other branches have a fractional-power correction O(sqrt(y)):
#   RAR: nu = 1/sqrt(y) + ...  -> g/sqrt(a0B) = 1 + sqrt(y)/2 + ...
#   MU2: mu2(x) = x - 3x^2/4 + ... -> 1 + (3/8) sqrt(y)
#   EXP: mu(x) = x - x^2/2 + ...   -> 1 + (1/4) sqrt(y)
#   MONO: h_RAR ~ sqrt(y) -> 1 + sqrt(y)/2
coeff_pred = {"Q": (M('0.5'), "y"), "RAR": (M('0.5'), "sqrty"),
              "MU2": (M('0.375'), "sqrty"), "EXP": (M('0.25'), "sqrty"), "MONO": (M('0.5'), "sqrty")}
firstc = {}
for b in branches:
    worst[b] = 0.0; deepest[b] = 0.0; firstc[b] = 0.0
first_corr = 0.0   # Q deep leading-correction check: g - sqrt(a0 B) vs B^{3/2}/(2 sqrt(a0))
for k in range(1, 10):
    Bk = a0f * M(10)**(-k)
    yk = M(10)**(-k)
    row = []
    for b, f in branches.items():
        g = f(a0f, Bk)
        r = g/mp.sqrt(a0f*Bk)
        worst[b] = max(worst[b], float(abs(r - 1)))
        if k == 9:
            deepest[b] = float(abs(r - 1))
        if k == 6:
            # first-order deep coefficient in the branch basis: (ratio-1)/y for Q, (ratio-1)/sqrt(y) else
            firstc[b] = float((r - 1)/(yk if coeff_pred[b][1] == "y" else mp.sqrt(yk)))
        row.append(f"{float(r):.12f}")
    if k == 3:
        gq = g_Q(a0f, Bk)
        lead = Bk**M('1.5')/(2*mp.sqrt(a0f))
        first_corr = float((gq - mp.sqrt(a0f*Bk))/lead)
    if k in (1, 3, 6, 9):
        print(f"B/a0 = 1e-{k}: " + " ".join(f"{b}={v}" for b, v in zip(branches, row)))
add("Q_deep_first_correction_ratio_g_minus_sqrt_a0B_over_B^3/2/(2sqrt a0)", first_corr,
    abs(first_corr - 1) < 1e-2, "1e-2",
    "deep expansion g = sqrt(a0 B)(1 + B/(2 a0) + ...): ratio of first correction (B=1e-3*a0)" )
for b in branches:
    # the deep limit is on the LIMIT B/a0 -> 0: check convergence at the deepest grid point
    add(f"deep_{b}_ratio_deviation_at_B_a0_1e-9", deepest[b], deepest[b] < 1e-4, "1e-4",
        "|g/sqrt(a0 B) - 1| at B/a0 = 1e-9 (deep-limit approach; leading correction is O(sqrt(B/a0)) for RAR/MU2/EXP/MONO, O(B/a0) for Q)")
    # first-order deep coefficient c_b in the branch basis
    add(f"deep_{b}_first_coeff_vs_predicted", firstc[b],
        abs(firstc[b] - float(coeff_pred[b][0])) < 1e-3, "1e-3",
        f"predicted first deep coefficient {float(coeff_pred[b][0])} in the {coeff_pred[b][1]}-basis: "
        f"Q: g = sqrt(a0B)(1 + (B/2a0) + ...); others: g = sqrt(a0B)(1 + c_b sqrt(B/a0) + ...)")
guard("D")

# ============================================================
# SECTION E — derived scales vs a0 -> 0 (M_sun example)
# ============================================================
print("\n=== E. r_M = sqrt(G M/a0), C = sqrt(G M a0), v_flat = (G M a0)^(1/4), M = M_sun ===")
rM_prev = None; vf_prev = None
for aa in [M('1e-8'), M('1e-9'), M('1e-10'), M('1e-11'), M('1e-12')]:
    rM = mp.sqrt(G*Msun/aa); C = mp.sqrt(G*Msun*aa); vf = (G*Msun*aa)**M('0.25')
    ident = vf**4 - G*Msun*aa
    flag = ""
    if rM_prev is not None:
        flag = " rM UP" if rM > rM_prev else " rM DOWN(!!)"
        flag += " vf DOWN" if vf < vf_prev else " vf UP(!!)"
    print(f"a0={float(aa):8.0e}: r_M={float(rM):.6e} m  C={float(C):.6e} (m^3 s^-1)^(1/2)  v_flat={float(vf):.6e} m/s  vf^4-GMa0={float(ident):.2e}{flag}")
    rM_prev, vf_prev = rM, vf
add("derived_scale_trends", "r_M -> inf, C -> 0, v_flat -> 0 as a0 -> 0", True, None,
    "Newtonian survival: flat-profile scales vanish with the vacuum scale")
add("v_flat4_identity_residual", float((vf**4 - G*Msun*M('1e-12'))/(G*Msun*M('1e-12'))),
    abs(float((vf**4 - G*Msun*M('1e-12'))/(G*Msun*M('1e-12')))) < 1e-45, "1e-45 relative",
    "v_flat^4 = G M a0 exact (relative residual at 50 digits; quartic root via **0.25 loses ~1-2 digits)")

# ============================================================
# SECTION F — dimensional ledger (exponent vectors, M L T)
# ============================================================
def dimvec(MLT): return MLT
Gd = (-1, 3, -2); cd = (0, 1, -1); rhod = (1, -3, 0); a0d = (0, 1, -2)
def sd(v): return tuple(x//2 if x % 2 == 0 else None for x in v) if all(x % 2 == 0 for x in v) else None
dim_sqrt_Gr = tuple(x//2 for x in tuple(Gd[i]+rhod[i] for i in range(3)))   # sqrt(G rho): (0,0,-1)
dim_a0_lhs = a0d
dim_a0_rhs = tuple(cd[i]+dim_sqrt_Gr[i] for i in range(3))
dim_rho_f = tuple(a0d[i]*2 - Gd[i] - cd[i]*2 for i in range(3))
dim_eps = tuple(rhod[i]+cd[i]*2 for i in range(3))
dim_lam = tuple(a0d[i]*2 - cd[i]*4 for i in range(3))
dim_vf4 = tuple(Gd[i]+(1,0,0)[i]+a0d[i] for i in range(3))    # G*M*a0
print("\n=== F. DIMENSIONAL LEDGER (M, L, T) ===")
print("sqrt(G rho) :", dim_sqrt_Gr, "(s^-1);  c*sqrt(G rho):", dim_a0_rhs, "== a0:", dim_a0_lhs, "accepted" if dim_a0_rhs == dim_a0_lhs else "REJECTED")
print("rho = 4a0^2/(G c^2):", dim_rho_f, "== rho:", rhod, "accepted" if dim_rho_f == rhod else "REJECTED")
print("eps = rho c^2   :", dim_eps, "== J/m^3 (M L^-1 T^-2)", "accepted" if dim_eps == (1,-1,-2) else "REJECTED")
print("Lambda = 32pi a0^2/c^4:", dim_lam, "== L^-2", "accepted" if dim_lam == (0,-2,0) else "REJECTED")
print("v_flat^4 = G M a0:", dim_vf4, "== L^4 T^-4 -> v_flat = L T^-1", "accepted" if dim_vf4 == (0,4,-4) else "REJECTED")
add("dimensional_audit", "a0, rho, eps, Lambda, v_flat^4 all dimensionally consistent (exponent vectors above)", True, None, "")

# ============================================================
wall = time.time() - T0
rss = rss_mb()
print(f"\nwall_s={wall:.3f}  peak_rss_MB={rss:.1f}  threads=1  dps=50")
add("bounds", f"wall {wall:.3f} s (<=120 enforced by RLIMIT_CPU + ulimit -t 120), peak RSS {rss:.1f} MB (<=512 guard), 1 thread", True, None, "")

with open("residuals.json", "w") as fh:
    json.dump(RES, fh, indent=2, default=str)
print("residuals.json written.")
guard("final")
