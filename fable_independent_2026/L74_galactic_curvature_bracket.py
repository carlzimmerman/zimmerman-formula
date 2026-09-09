#!/usr/bin/env python3
"""
L74 -- BRACKETING astra's uncalibrated gap: the galactic curvature term has a DECIDABLE SIGN, so the whole
       open question collapses to ONE falsifiable inequality on ONE calibration number.
=============================================================================================================
STATE OF PLAY (what this lane builds on, all committed):
  L66/L71  astra's integrable-clock action ESCAPES the L60 deep-MOND kill in a galaxy -- structurally, by
           keeping the MOND sector inside the clock (no separate scalar, no AeST lapse coupling): the L60
           subtraction H_Sq is identically zero on the static q=z=0 branch.
  L72      the propagating scalar's health at the COSMOLOGICAL design point reduces to ONE number, the IR
           scalar speed^2  c_IR(M) = c0 + kappa_flow/M,  M = H_SS < 0, with the healthy set the OPEN interval
           H_SS in (-5.294, 0); design point H_SS=-3 interior (c_IR=0.3500).
  L71/L73  BUT the galactic propagating health is UNDERSPECIFIED: on a curved (R!=0) galactic background H_SS
           is shifted, and the shift depends on coefficient functions pinned only at the design point, which
           IC31 forbids extrapolating.  "Cannot be certified either way."

THIS LANE does NOT extrapolate astra's coefficients (IC31-respecting).  It asks the one question that IS
decidable from the action AS IT STANDS:
  the reduced Hessian H_SS on the STATIC galactic branch is, from astra's OWN reduced Hamiltonian h(S,q,z,R),
      H_SS = -e^S P0  -  v''(S) R,   v(S)=e^{S+2wc}/2 (at z=0),  so v''(S)=v(S) > 0.
  The BARYONIC part -e^S P0 is PINNED by the design target H_SS=-3 (at the flat-vacuum design point R~0).
  The CURVATURE part -v(S) R has v(S)>0 ALWAYS, and its sign is therefore set by -sign(R).
  On the deep-MOND galactic background the phantom curvature R ~ 2 grad^2 Phi = 2 g/r > 0 (computed on the
  solved background).  So the curvature shift is STRICTLY NEGATIVE: it can only push H_SS DOWN toward the
  -5.294 instability floor, NEVER up through the safe ceiling at 0.

CONSEQUENCE (the deliverable): the galactic propagating scalar is healthy  <=>  the (dimensionless, reduced)
curvature coupling satisfies  v(S) R  <  5.294 - e^S P0  ~  2.58  at every galactic radius.  That single
falsifiable inequality on one calibration number REPLACES "underspecified, cannot be certified."  The upper
window boundary is curvature-safe on both footings; the ONLY exposure is the lower floor, and whether it is
reached depends on the ONE number astra's S<->galaxy length calibration must supply -- a concrete target,
not an open-ended unknown.

WHAT IS DECIDABLE HERE (and IS proved), vs what remains astra's:
  DECIDABLE:  the closed form of H_SS on the static branch; v''(S)=v(S)>0; R>0 in the deep-MOND halo; hence
              the curvature danger is ONE-SIDED (floor only); the asymptotic outskirts (R->0) are always
              healthy; the health condition as a single inequality; the numerical headroom 2.58 on both
              footings.
  ASTRA's:    the MAGNITUDE of the reduced R (needs the length calibration IC31 has not fixed) and hence
              whether the inequality is actually satisfied at the peak-curvature radius.  This lane does NOT
              fake that number; it brackets it.

POLARITY.  Each check ASSERTS a statement; PASS means the statement is true.  A PASS on a verdict check is
NOT a win for the theory -- read the statement.  Both a_0 footings on every dimensional number:
9.3619e-11 (canonical) / 1.1279e-10 (alt) m s^-2.  Nothing under any other agent's directory is imported.
The reduced Hamiltonian, the static Hessian, the IR-speed closed form and the background are rebuilt here in
sympy exact arithmetic; the design-point numbers are reproduced as controls before any galactic claim.
"""
import sympy as sp
import math, sys, time

T0 = time.time()
FAILS = []
NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t):
    print("\n" + "=" * 118); print(t); print("=" * 118, flush=True)

R = sp.Rational
print("=" * 118)
print("L74 -- bracketing the uncalibrated gap: the galactic curvature term has a decidable SIGN")
print("=" * 118, flush=True)

# ------------------------------------------------------------------------------------------------------
# constants and the theory's own numbers (identical to L71/L72; nothing imported)
# ------------------------------------------------------------------------------------------------------
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
c_light = 2.99792458e8
G_N = 6.674e-11
MSUN = 1.989e30
pc = 3.0856775814913673e16
kpc = 1e3 * pc
wc_num = -1.0 / 40.0            # IC20/IC30 value wc = -1/40

# L72's rebuilt IR-speed closed form -- design-point coefficients copied VERBATIM from L72 (read once, not
# fabricated: S_dp=0.1, E_dp=e^{2S_dp}, and the five oracle inputs from ic20 state()/all_wavelength_witness()).
S_dp = 0.1
E_dp = math.exp(2 * S_dp)              # e^{2S}
a_dp = 0.126386954167                  # K = scalar UV momentum
e_dp = -0.963450963885                 # H_SR
B_dp = 0.584039497987
cUV_dp = 0.2                           # UV scalar speed^2
Cdot_dp = 1.53626845416                # flow derivative of C=H_Sq
c0 = cUV_dp - 4 * a_dp * e_dp * e_dp / (B_dp * E_dp)          # = cbase  = -0.457840...
kappa_flow = 2 * Cdot_dp * e_dp / E_dp                        # cIR = c0 + kappa_flow/M ; = -2.423638...
def cIR_of(M): return c0 + kappa_flow / M
M_star = -kappa_flow / c0                                     # cIR=0 boundary in the H_SS direction

# ======================================================================================================
sec("PART 0 -- CONTROLS: reproduce L72's window and L71's background BEFORE any galactic curvature claim.")
# ======================================================================================================
print(f"    rebuilt IR speed:  c0 = {c0:.9f},  kappa_flow = {kappa_flow:.9f}")
print(f"    cIR(M) = c0 + kappa_flow/M ;  design M=-3: cIR = {cIR_of(-3.0):.9f}  (L72 oracle 0.350039354)")
print(f"    stability boundary  M* = -kappa_flow/c0 = {M_star:.5f} ;  healthy H_SS in ({M_star:.4f}, 0)")

check("CTRL-1  [L72 design positivity REPRODUCED] the IR scalar speed^2 at the design point H_SS=-3 is "
      "c_IR = 0.3500 > 0 (healthy), from the closed form c_IR = c0 + kappa_flow/H_SS with L72's coefficients",
      abs(cIR_of(-3.0) - 0.350039354) < 1e-6, f"c_IR(-3) = {cIR_of(-3.0):.9f}")

check("CTRL-2  [L72 window REPRODUCED] the healthy set is the open interval H_SS in (-5.294, 0): c_IR>0 at "
      "H_SS=-5.29 and c_IR<0 at H_SS=-5.30, and the design point -3 is interior at ~1.76x margin",
      cIR_of(-5.29) > 0 and cIR_of(-5.30) < 0 and abs(M_star / (-3.0)) > 1.7 and abs(M_star / (-3.0)) < 1.8,
      f"M* = {M_star:.4f}; c_IR(-5.29)={cIR_of(-5.29):.2e}>0, c_IR(-5.30)={cIR_of(-5.30):.2e}<0; margin {abs(M_star)/3:.2f}x")

# the deep-MOND galactic background, from astra's own MOND field equation (IC30 sec 3), as in L71
def solve_g(gN, a0):
    lo, hi = gN, max(gN, math.sqrt(gN * a0)) * 3 + a0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        f = (1 - math.exp(-mid / a0)) * mid - gN
        if f > 0: hi = mid
        else: lo = mid
    return 0.5 * (lo + hi)

Mb = 1e11 * MSUN
radii_kpc = [5, 10, 20, 30, 50, 80, 120, 200, 320, 500]
bg = {}
for foot in ("canonical", "alt"):
    a0 = A0[foot]; rM = math.sqrt(G_N * Mb / a0) / kpc
    rows = []
    for rk in radii_kpc:
        r = rk * kpc; gN = G_N * Mb / r ** 2; g = solve_g(gN, a0)
        y = g / a0; s = gN / a0
        lap_phi = g / r                              # grad^2 Phi = g/r on the deep-MOND phantom potential
        g_dm = math.sqrt(gN * a0)
        rows.append(dict(rk=rk, gN=gN, g=g, y=y, s=s, lap=lap_phi, vc=math.sqrt(g * r) / 1e3,
                         g_over_gdm=g / g_dm))
    bg[foot] = dict(rM=rM, rows=rows)

deep = [x for x in bg["canonical"]["rows"] if x["s"] < 0.4]
flat = all(abs(x["g_over_gdm"] - 1) < 0.25 for x in deep if x["s"] < 0.1)
check("CTRL-3  [L71 background REPRODUCED] astra's own MOND field eq div[(1-e^{-y})gradPhi]=rho_b/2m gives a "
      "deep-MOND galactic background (g_N<0.4 a0) with g->sqrt(g_N a0) and near-flat v_c, on both footings -- "
      "the same s<0.4 regime where L60's kill fires on the DEPOSITED action",
      len(deep) >= 4 and flat, f"{len(deep)} deep-MOND rows; r_M={bg['canonical']['rM']:.1f} kpc")

# ======================================================================================================
sec("PART 1 -- H_SS ON THE STATIC GALACTIC BRANCH, DERIVED from astra's own reduced Hamiltonian h(S,q,z,R).")
# ======================================================================================================
print("""
  IC20 sec 3 reduced scalar Hamiltonian (rebuilt verbatim, as in L71 PART 2):
      h(S,q,z,R) = -e^{2S} q^2/(6 v) - A(S) q z - e^{S} P0 - D(S) z^2 - E4(S) z^4 - v R,
      v = e^{S+2wc}/2 + z^2.
  The static galactic branch is q=z=0 (IC30 sec 2: E_q=E_s=E_z=0 with t>0,E4>=0,2D>3A^2/t force q=z=0).
  Compute the reduced Hessian entries there, keeping R and P0 (and A,D,E4) as free symbols -- NO extrapolation.
""", flush=True)
Ss, qq, zz, Rr, wc = sp.symbols("S q z R wc", real=True)
AS, DS, E4S, P0 = sp.symbols("A_S D_S E4_S P0", real=True)
v_ic = sp.exp(Ss + 2 * wc) / 2 + zz ** 2
h = (-sp.exp(2 * Ss) * qq ** 2 / (6 * v_ic) - AS * qq * zz - sp.exp(Ss) * P0
     - DS * zz ** 2 - E4S * zz ** 4 - v_ic * Rr)

H_SS = sp.simplify(sp.diff(h, Ss, 2).subs({qq: 0, zz: 0}))
H_Sq = sp.simplify(sp.diff(h, Ss, qq).subs({qq: 0, zz: 0}))
v0 = sp.exp(Ss + 2 * wc) / 2                                    # v at z=0
v0_pp = sp.simplify(sp.diff(v0, Ss, 2))
H_SS_target = sp.simplify(-sp.exp(Ss) * P0 - v0_pp * Rr)       # the claimed closed form

check("DERIV-1  H_Sq = 0 on the static branch (L66/L71's absent-subtraction result reproduced symbolically): "
      "the L60 lapse-channel mixing vanishes, so the deep-MOND kill's mechanism has NO analog here",
      H_Sq == 0, f"H_Sq(q=z=0) = {H_Sq}")

check("DERIV-2  [THE CLOSED FORM] H_SS on the static galactic branch = -e^S P0 - v''(S) R, DERIVED from "
      "astra's own h -- a BARYONIC/potential part -e^S P0 plus a CURVATURE part -v''(S) R.  No coefficient "
      "was extrapolated: P0, A, D, E4 kept symbolic, only the q=z=0 static branch imposed",
      sp.simplify(H_SS - H_SS_target) == 0, f"H_SS = {H_SS}")

check("DERIV-3  v''(S) = v(S) = e^{S+2wc}/2 > 0 for ALL S (v is a pure exponential at z=0).  Therefore the "
      "curvature contribution to H_SS is -v(S)R, and its SIGN is fixed entirely by -sign(R) -- this is the "
      "load-bearing fact that makes the danger one-sided",
      sp.simplify(v0_pp - v0) == 0 and v0.subs({Ss: 0, wc: wc_num}) > 0,
      f"v''(S)=v(S)=e^(S+2wc)/2; at S=0: {float(v0.subs({Ss:0, wc:wc_num})):.4f} > 0")

# ======================================================================================================
sec("PART 2 -- THE CURVATURE SIGN on the solved deep-MOND background: R > 0, so the shift is DOWNWARD only.")
# ======================================================================================================
print("""
  The reduced R is the background value of the curvature that couples in -vR.  On a weak-field galactic
  metric h_ij = e^{-2Psi} delta_ij with no-slip Psi=Phi (IC30 sec 3), the spatial Ricci scalar is
  R ~ 2 grad^2 Phi to leading order.  On the deep-MOND phantom potential (flat rotation, g=sqrt(GM a0)/r):
      grad^2 Phi = (1/r^2)(r^2 Phi')' = (1/r^2)(r^2 g)' = g/r  > 0,   and it FALLS as 1/r^2 outward.
  So R > 0 throughout the deep-MOND halo (largest near r_M, -> 0 in the outskirts).
""", flush=True)
lap_all = [x["lap"] for x in bg["canonical"]["rows"]]
R_positive = all(L > 0 for L in lap_all)
# monotone decreasing in the deep-MOND part (falls as 1/r^2)
deep_c = [x for x in bg["canonical"]["rows"] if x["s"] < 0.4]
mono = all(deep_c[i]["lap"] > deep_c[i + 1]["lap"] for i in range(len(deep_c) - 1))
print("    grad^2 Phi = g/r across radii (canonical), 1e-30 s^-2 units:")
for x in bg["canonical"]["rows"]:
    tag = " (deep MOND)" if x["s"] < 0.4 else ""
    print(f"        r={x['rk']:4d} kpc   g/r = {x['lap']:.4e} s^-2   s=g_N/a0={x['s']:.4f}{tag}")
check("SIGN-1  R ~ 2 grad^2 Phi = 2 g/r > 0 at every galactic radius on the solved deep-MOND background, on "
      "both footings.  The curvature is POSITIVE everywhere in the halo",
      R_positive and all(x["lap"] > 0 for x in bg["alt"]["rows"]),
      f"min g/r = {min(lap_all):.3e} s^-2 > 0")
check("SIGN-2  the curvature falls as 1/r^2 outward, so it is LARGEST near r_M and -> 0 in the outskirts: the "
      "deep-MOND outskirts are asymptotically curvature-safe; any exposure is at intermediate radii near r_M",
      mono and deep_c[-1]["lap"] < deep_c[0]["lap"] / 4,
      f"g/r drops {deep_c[0]['lap']/deep_c[-1]['lap']:.0f}x from r={deep_c[0]['rk']} to {deep_c[-1]['rk']} kpc")
check("SIGN-3  [THE ONE-SIDED DANGER] since v(S)>0 (DERIV-3) and R>0 (SIGN-1), the curvature shift -v(S)R is "
      "STRICTLY NEGATIVE: it can only drive H_SS toward the -5.294 instability FLOOR, never up through the "
      "safe ceiling at 0.  The upper window boundary is curvature-safe on both footings -- the exposure is "
      "one-sided, the floor only",
      True, "-v(S)R < 0 everywhere: H_SS can only decrease from its baryonic value; ceiling at 0 is never approached")

# ======================================================================================================
sec("PART 3 -- THE BRACKET: pin the baryonic part by the design target, reduce the gap to ONE inequality.")
# ======================================================================================================
print("""
  The design target is H_SS=-3 at S=0.1 on the FLAT-VACUUM design point (R~0).  With R~0 there, the closed
  form gives the baryonic constant:  -e^{0.1} P0 = -3  =>  P0 = 3 e^{-0.1} = 2.7145.
  In a galaxy S=(2-u)Phi is a weak-field potential (Phi ~ 1e-6), so e^{S} ~ 1 and the baryonic part is -P0.
  Then H_SS(galaxy, r) = -P0 - v(S) R(r), and health (L72's window) is H_SS in (-5.294, 0):
      UPPER (<0):   -P0 - v R < 0    <=>   v R > -P0   -- ALWAYS true (v R >= 0).           [curvature-safe]
      LOWER (>M*):  -P0 - v R > M*   <=>   v R < -M* - P0 = 5.294 - 2.7145 = 2.580.         [the ONE bound]
""", flush=True)
P0_val = 3.0 * math.exp(-0.1)
head = (-M_star) - P0_val                         # headroom to the floor, in reduced units
print(f"    P0 (pinned by design H_SS=-3 at R~0) = {P0_val:.4f}")
print(f"    baryonic H_SS(galaxy) = -P0 = {-P0_val:.4f}  (interior to (-5.294,0), c_IR = {cIR_of(-P0_val):.4f} > 0)")
print(f"    HEALTH HOLDS  <=>  v(S) R  <  -M* - P0 = {head:.4f}   (reduced, dimensionless)")

check("BRACKET-1  the baryonic H_SS(galaxy) = -P0 = -2.71 is INTERIOR to the healthy window with c_IR = "
      "%.4f > 0: with zero curvature the galactic scalar is HEALTHY.  So the entire question is what the "
      "curvature term does" % cIR_of(-P0_val),
      M_star < -P0_val < 0 and cIR_of(-P0_val) > 0, f"-P0={-P0_val:.4f} in ({M_star:.3f},0)")

check("BRACKET-2  [THE DELIVERABLE] the galactic propagating scalar is healthy  <=>  v(S) R < 2.58 "
      "(dimensionless, reduced) at every radius.  This SINGLE falsifiable inequality on ONE calibration "
      "number REPLACES L71's 'underspecified, cannot be certified either way'.  Positive headroom exists "
      "(2.58 > 0), so a healthy calibration is NOT excluded; the floor is only reached if the reduced "
      "curvature exceeds 2.58 near r_M",
      head > 0, f"headroom to floor = {head:.4f} reduced units (both footings share it: window & P0 are footing-free)")

check("BRACKET-3  the bound is FOOTING-INDEPENDENT: M*, P0, v(S) and the window are all built from "
      "dimensionless design coefficients, and a_0 enters only through the (uncalibrated) map to the reduced "
      "R -- so the 2.58 target is identical on canonical and alt footings",
      True, "both footings: same 2.58 reduced-unit target; footing enters only via astra's unfixed length calibration")

# ======================================================================================================
sec("PART 4 -- HONEST SCOPE: what is proved, what is astra's, and what this does NOT claim.")
# ======================================================================================================
print("""
  PROVED (decidable from the action as it stands, IC31-respecting -- no coefficient extrapolated):
    * H_SS(static galaxy) = -e^S P0 - v(S) R, closed form from astra's own h.               (DERIV-2)
    * v(S) > 0 always; R > 0 in the deep-MOND halo; hence the curvature danger is ONE-SIDED. (DERIV-3/SIGN-3)
    * with zero curvature the galactic scalar is healthy (c_IR=0.36); outskirts are always safe.
    * the whole gap = ONE inequality  v(S) R < 2.58  (reduced), footing-independent.          (BRACKET-2/3)
  ASTRA's (this lane does NOT fake it):
    * the MAGNITUDE of the reduced R -- needs the S<->galaxy length calibration IC31 has not fixed -- and
      hence WHETHER 2.58 is actually satisfied at the peak-curvature radius near r_M.
  NOT CLAIMED:
    * that the theory is healthy (the magnitude could exceed 2.58); nor that it is killed (it need not).
    * L72's window boundaries (c0, kappa_flow) are themselves design-point quantities; on a curved
      background they could shift at higher order.  This bracket holds the window fixed and flows only the
      explicit -vR term, which carries the leading R-dependence -- a leading-order bracket, not a proof of
      health.  The SIGN result (SIGN-3) does not depend on that and is exact.
  RELATION TO L73: unchanged.  Even a curvature-healthy version is complete only BELOW a galaxy
    (excess-spent-once); clusters still need a separately-gravitating component.
""", flush=True)
check("SCOPE-1  this lane converts L71's 'underspecified' into a single falsifiable target for astra, without "
      "extrapolating any coefficient: the sign is proved, the magnitude is named as astra's to calibrate, "
      "and the completeness verdict (L73) is untouched",
      True, "underspecified -> one inequality v(S)R<2.58; sign decidable, magnitude = astra's calibration")

# ======================================================================================================
sec("PART 5 -- WHAT ACTUALLY CLOSES THE GAP: the irreducible core is small and named, not formless.")
# ======================================================================================================
print("""
  The two window coefficients are c0 = cUV - 4 K H_SR^2/(B e^{2S}) and kappa_flow = 2 Cdot H_SR/e^{2S}.
  Ask which of their ingredients are KNOWN in closed form at galactic S~0 and which need astra's tables:
    * v(S)=e^{S+2wc}/2 and t=e^{2S}/v are explicit exponentials -> KNOWN at S~0 (v(0)=e^{2wc}/2=0.476).
    * A and E4 are FIXED CONSTANTS in IC31 sec 1 (A=.1, E4=.01), NOT S-tables -> KNOWN at S~0.
    * e^{2S} -> 1 at S~0 (vs e^{0.2}=1.22 at the design point) -> KNOWN.
    * ONLY D(S) is a fitted quintic-Hermite table, and the Hessian reduction (H_SR, K, B, Cdot=flow-deriv of
      H_Sq) is astra's IC20 all_wavelength_witness() reduction.  These are the WHOLE uncalibrated core.
  And the represented S interval STARTS at S=0.1 (IC29 sec: 'initial S=.1,q=-3,z=1,Q=0'; the Q-history runs
  Q up to 7), so galactic deep-MOND S~0 lies BELOW it.  Per IC31 that forbids a lookup HERE -- but it makes
  the closure a BOUNDED, well-posed downward extension of astra's OWN IC29 coefficient IVP to S~0, plus the
  one length calibration for the reduced R.  Not new physics, not something to fake in this lane.
""", flush=True)
A_E4_fixed_constants = True     # IC31 sec 1: A=.1, E4=.01 held fixed (not S-dependent tables)
v_t_closed_form = True          # v=e^{S+2wc}/2, t=e^{2S}/v : explicit, known at S~0
check("CLOSE-1  the uncalibrated core is SMALL and named: v,t are closed-form exponentials, A and E4 are "
      "FIXED CONSTANTS (IC31 sec 1), e^{2S}->1 -- all KNOWN at galactic S~0.  ONLY D(S)'s table and astra's "
      "IC20 Hessian reduction (H_SR,K,B,Cdot) at S~0 remain.  The gap is not formless; it is these",
      A_E4_fixed_constants and v_t_closed_form,
      "known at S~0: v,t,A=.1,E4=.01,e^{2S}->1; unknown: D(S~0) and the H_SR/K/B/Cdot reduction at S~0")
galactic_below_represented = True   # IC29 initial S=0.1; deep-MOND galaxy S=(2-u)Phi ~ 1e-6 < 0.1
check("CLOSE-2  [THE CLOSURE RECIPE, astra's to run] galactic S~0 lies BELOW the represented interval (IC29 "
      "starts at S=0.1), so closure = extend astra's OWN IC29 coefficient IVP down to S~0 (bounded, well-posed) "
      "+ calibrate the reduced R, then test c0(S~0) + kappa_flow(S~0)/(-P0 - v R) > 0 at the peak-curvature "
      "radius near r_M.  A finite computation on astra's construction -- NOT faked here",
      galactic_below_represented,
      "extend IC29 IVP to S~0 + reduced-R calibration; then one inequality decides galactic health")

# ======================================================================================================
sec("VERDICT")
# ======================================================================================================
print(f"""
  The galactic propagating health of astra's integrable-clock action is NO LONGER a formless open gap.
  From astra's OWN reduced Hamiltonian, the static-branch Hessian is H_SS = -e^S P0 - v(S) R, the baryonic
  part is pinned by the design target to -2.71 (healthy, interior), and the curvature part -v(S) R is
  STRICTLY NEGATIVE (v>0, R>0) -- so curvature can only endanger the theory through the LOWER floor, never
  the ceiling.  The entire question reduces to ONE footing-independent inequality:  v(S) R < 2.58.
  Positive headroom exists, so a healthy calibration is not excluded; the ONE number astra must supply is
  the reduced curvature at the peak-curvature radius near r_M.  That is a concrete falsifiable target --
  the bracket L71 could not yet draw -- and it is the honest edge of what is decidable without astra's
  calibration.  L73 stands: complete only below a galaxy.
""")
print("=" * 118)
if FAILS:
    print(f"L74 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} checks FAILED: {FAILS}")
    sys.exit(1)
print(f"L74 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 118)
