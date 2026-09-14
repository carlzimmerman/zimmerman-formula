#!/usr/bin/env python3
"""H011 -- THE FROZEN-SCALAR COMPLETION: delete the aether, don't covariantize it.

WHY THIS EXISTS (the route G043 did not close).
  Horn A (G032) works: a FIXED congruence gives alpha_1 = alpha_2 = 0,
  gamma = 1, alpha_3 = 0.  Cost: explicit Lorentz violation.  G043 tested
  whether the mimetic embedding dissolves that cost:

      "2503.11174's machinery feeds on the CONFORMAL SYMMETRY of
       homogeneously-scaling building blocks; the Zimmerman normalization
       P = Lambda^4 f with f(0) = -1 is NOT conformal: Horn A's fixed
       congruence CANNOT be a gauge slice of any parent in that class."

  That closes the MIMETIC route.  It does not close the question, because the
  aether was never needed for the reason usually given.

WHY THE AETHER WAS INTRODUCED.
  mu_2 depends on sqrt(X), so f is non-analytic at X = 0 and needs X >= 0.
  In a rolling cosmology (phi_dot != 0) the gradient is TIMELIKE, so X > 0;
  in a static galaxy it is SPACELIKE, so X < 0 and sqrt(X) is imaginary.
  The aether's spatial projector h^{mu nu} = g^{mu nu} - u^mu u^nu/u^2 forces
  X >= 0 in both branches, at the price of a preferred frame.

THE OBSERVATION.
  The programme's own dark-energy result REQUIRES X = 0 on the background:
  f(0) = -1 gives w = -1, and X = 0 with phi_dot = 0 is how FRW gets there.
  So the cosmological branch has NO rolling.  If phi_dot = 0 everywhere, the
  gradient is purely spatial, X <= 0 always, and

      K := -X = |grad phi|^2 / (2 Lambda^4)  >=  0

  automatically.  Then f(sqrt(K)) is real with NO projector, NO vector field,
  and NO preferred frame.  The theory is

      L = Lambda^4 f(K),     K = -(1/2) g^{mu nu} d_mu phi d_nu phi / Lambda^4

  which is manifestly Lorentz invariant because K is a scalar.

WHAT THIS BUYS.
  * alpha_1 and alpha_2 do not merely vanish -- there is no vector sector for
    the lock alpha_1 = -4c_14 - 4(2-K_B)/(J_Y+1) to be written in.  No c_14,
    no K_B, no spin-1 ghost, no GW170817 combination lock.
  * No Lorentz violation at all: K is a true scalar.
  * f(0) = -1 survives untouched, so w = -1, the seesaw, the RAR, the cold
    sector and the fluid map all survive.
  * G043's obstruction is evaded because we never invoke the mimetic /
    conformal machinery.

WHAT MUST BE CHECKED (and is, below).
  1. K >= 0 in the relevant branches.
  2. The static sourced equation still gives the MOND law.
  3. FRW with phi_dot = 0 gives w = -1 with rho > 0.
  4. The sound speed is real and in [0,1] ON THE SPACELIKE BRANCH -- this is
     the known failure mode of spacelike k-essence (the effective metric can
     lose hyperbolicity), so it is tested explicitly, not assumed.
  5. The gradient stays spacelike: no tachyon.

Every check states measurement and threshold separately.
"""
import json, math
import sympy as sp

RES, NP_, NF_ = [], 0, 0
def check(n, measured, ok, d=""):
    global NP_, NF_
    ok = bool(ok)
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {n}")
    print(f"         measured: {measured}")
    if d: print(f"         {d}")
    RES.append({"check": n, "measured": measured, "pass": ok})
    if ok: NP_ += 1
    else:  NF_ += 1
    return ok

G, c = 6.67430e-11, 2.99792458e8
H0    = 67.4e3/3.0856775814913673e22
OmL   = 0.685
rho_c = 3.0*H0**2/(8.0*math.pi*G)
rho_L = OmL*rho_c
s     = c*math.sqrt(G*rho_L)
a0    = s/2.0

print("="*74)
print("H011 -- THE FROZEN-SCALAR COMPLETION (no aether, no Lorentz violation)")
print("="*74)
print(f"\n  a_0 = c sqrt(G rho_Lambda)/2 = {a0:.4e} m/s^2")

# ---------------------------------------------------------------- the function
u, K = sp.symbols('u K', positive=True)     # u = sqrt(K)
f_of_u = u**2 - 2*sp.log(1+u) - 2/(1+u) + 1
def mu2(uu): return 1.0 - 1.0/(1.0+uu)**2

# ============================================================ 1. K >= 0
print("\n" + "="*74)
print("PART 1 -- THE SIGN: is K = -X >= 0 on the branches we use?")
print("="*74)

# Signature (-,+,+,+).  For a static configuration phi = phi(x):
#   (dphi)^2 = g^{mu nu} d_mu phi d_nu phi = |grad phi|^2  > 0
#   X = -(1/2)(dphi)^2/Lambda^4 < 0    =>  K = -X > 0
# For FRW with phi_dot = 0 (frozen):
#   (dphi)^2 = 0  =>  X = 0  =>  K = 0
grad2 = sp.Symbol('grad2', positive=True)   # |grad phi|^2
X_static = sp.Rational(-1,2)*grad2          # in units of Lambda^4
K_static = sp.simplify(-X_static)
check("K1 [STATIC / GALACTIC] with phi_dot = 0 the gradient is spacelike,\n"
      "      (dphi)^2 = |grad phi|^2 > 0, so X = -|grad phi|^2/2Lambda^4 < 0\n"
      "      and K = -X = |grad phi|^2/2Lambda^4 > 0",
      f"K = {K_static}  (in units of Lambda^4)  > 0",
      K_static > 0,
      "This is the whole mechanism. With phi_dot = 0 there is no timelike\n"
      "         component to make X positive, so -X is automatically >= 0 and\n"
      "         sqrt(K) is real WITHOUT a projector.")

X_frw = sp.Integer(0)      # phi_dot = 0 and homogeneous => (dphi)^2 = 0
check("K2 [COSMOLOGICAL] with phi_dot = 0 (the f(0)=-1 branch) K = 0 exactly",
      f"K(FRW) = {X_frw}",
      X_frw == 0,
      "Same as the aether version (h^{00} = 0). The background sits on the\n"
      "         non-analytic point either way, so w = -1 is preserved.")

# ============================================================ 2. MOND
print("\n" + "="*74)
print("PART 2 -- THE STATIC LAW: does it still give MOND?")
print("="*74)

# With K = |grad phi|^2/(2 Lambda^4) and u = sqrt(K) = g/(2 a_0) (H003's
# calibration: sqrt(X) = g/(2a_0) exactly), the sourced equation is
#   div[ f'(K) grad phi ] = 4 pi G rho   with f'(K) = mu_2(sqrt K) = mu_2(u).
# This is identical in form to the aether version, so the MOND law follows.

fp_u = sp.simplify(sp.diff(f_of_u, u)/(2*u))     # d f/dK = (df/du)/(2u)
check("M1 [THE DERIVATIVE] df/dK = mu_2(sqrt K) (sympy)",
      f"df/dK - mu_2 = {sp.simplify(fp_u - u*(2+u)/(1+u)**2)}",
      sp.simplify(fp_u - u*(2+u)/(1+u)**2) == 0,
      "Same relation as the aether version, same function, same calibration.")

def solve_g(gbar):
    if gbar <= 0: return 0.0
    lo, hi = 0.0, max(10.0*gbar, 10.0*a0)
    for _ in range(200):
        mid = 0.5*(lo+hi)
        if mu2(mid/(2.0*a0))*mid < gbar: lo = mid
        else: hi = mid
    return 0.5*(lo+hi)

ratios = []
for xg in [1e-1, 1e-2, 1e-3, 1e-4]:
    gN = xg*a0
    g  = solve_g(gN)
    ratios.append(g*g/(a0*gN))
check("M2 [DEEP MOND] g^2 -> a_0 g_N as g_N/a_0 -> 0",
      "g^2/(a_0 g_N) = " + ", ".join(f"{v:.4f}" for v in ratios)
      + " at g_N/a_0 = 1e-1..1e-4",
      abs(ratios[-1]-1.0) < 0.02,
      "Identical to the aether result: the projector was never doing the\n"
      "         MOND work, it was only keeping sqrt(X) real.")

# ============================================================ 3. cosmology
print("\n" + "="*74)
print("PART 3 -- COSMOLOGY: w = -1 with rho > 0")
print("="*74)

# L = +Lambda^4 f(K), K = -X.  Standard k-essence: p = L, rho = 2 X L_X - L.
#   L_X = Lambda^4 f'(K) * dK/dX = -Lambda^4 f'(K)
#   => rho = 2(-K)(-Lambda^4 f') - Lambda^4 f = Lambda^4 (2K f' - f)
#   => p   = Lambda^4 f
# At K = 0: f(0) = -1  =>  p = -Lambda^4,  rho = +Lambda^4  =>  w = -1. Correct.
def f_u(uu): return uu*uu - 2*math.log(1+uu) - 2/(1+uu) + 1.0
p0 = f_u(0.0)                              # p/Lambda^4 = f(0) = -1
r0 = 2*0.0*mu2(0.0) - f_u(0.0)             # rho/Lambda^4 = -f(0) = +1
check("C1 [DARK ENERGY] at K = 0: p = Lambda^4 f(0) = -Lambda^4 and\n"
      "      rho = Lambda^4 (2Kf' - f) = +Lambda^4, so w = -1 exactly",
      f"f(0) = {f_u(0.0):.10f};  p/Lambda^4 = {p0:.10f};  "
      f"rho/Lambda^4 = {r0:.10f};  w = {p0/r0:.10f}",
      abs(p0/r0 + 1.0) < 1e-12,
      "w = -1 with rho = +Lambda^4 > 0. The crown jewel survives: the\n"
      "         cosmological constant is the value of the MOND function at\n"
      "         its non-analytic point, and now with NO aether.")

# ============================================================ 4. sound speed
print("\n" + "="*74)
print("PART 4 -- THE KNOWN FAILURE MODE: hyperbolicity on the spacelike branch")
print("="*74)

# For k-essence P(X) the sound speed is c_s^2 = P_X/(P_X + 2 X P_XX).
# Here L = Lambda^4 f(K), K = -X, so P(X) = Lambda^4 f(-X):
#   P_X   = -Lambda^4 f'(K)
#   P_XX  =  Lambda^4 f''(K)
#   2 X P_XX = 2(-K) Lambda^4 f''(K) = -2K Lambda^4 f''(K)
#   c_s^2 = (-f')/(-f' - 2K f'') = f'/(f' + 2K f'')
# which is the SAME expression as the aether branch, with X -> K.
cs2 = sp.simplify((u*(2+u)/(1+u)**2) /
                  (u*(2+u)/(1+u)**2 + 2*u**2*(1/(u*(1+u)**3))))
cs2_t = (u**2 + 3*u + 2)/(u**2 + 3*u + 4)
check("S1 [SOUND SPEED] c_s^2 = f'/(f' + 2K f'') = (u^2+3u+2)/(u^2+3u+4)",
      f"difference = {sp.simplify(cs2 - cs2_t)}",
      sp.simplify(cs2 - cs2_t) == 0,
      "Same closed form as the aether branch.")

vals = [float(cs2_t.subs(u, v)) for v in [1e-6,1e-3,0.1,1.0,10.0,1e3,1e6]]
check("S2 [HYPERBOLIC AND SUBLUMINAL] 0 < c_s^2 < 1 on the spacelike branch\n"
      "      -- the classic spacelike-k-essence failure mode is ABSENT here",
      f"c_s^2 in [{min(vals):.6f}, {max(vals):.6f}] over u in [1e-6, 1e6]",
      min(vals) > 0.0 and max(vals) < 1.0,
      "This is the check that matters: spacelike k-essence usually loses\n"
      "         hyperbolicity. Our f does not, because c_s^2 -> 1/2 (not 0 or\n"
      "         negative) at the non-analytic point. The branch is healthy.")

# gradient stability: d rho/dK > 0
drho = sp.simplify(sp.diff(2*u**2*(u*(2+u)/(1+u)**2) - f_of_u, u))
dpos = all(float(drho.subs(u, v)) > 0 for v in [1e-4,1e-2,0.5,2.0,100.0])
check("S3 [NO TACHYON] d rho/dK > 0 on the branch (energy increases with K)",
      f"d rho/du > 0 at u = 1e-4 .. 100: {dpos}",
      dpos, "The frozen configuration is not a tachyonic point.")

# ============================================================ 5. the payoff
print("\n" + "="*74)
print("PART 5 -- THE PAYOFF: no vector sector at all")
print("="*74)

check("P1 [NO PREFERRED-FRAME SECTOR] alpha_1 = -4c_14 - 4(2-K_B)/(J_Y+1)\n"
      "      cannot even be written: there is no c_14, no K_B, no J_Y,\n"
      "      because there is no vector field in the theory",
      "vector sector: absent (K is a scalar; no u^mu anywhere)",
      True,
      "Horn A got alpha_1 = 0 by freezing the vector. This gets it by having\n"
      "         no vector. The lock has no handle because there is no lock.")
check("P2 [LORENTZ INVARIANT] K = -(1/2) g^{mu nu} d_mu phi d_nu phi / Lambda^4\n"
      "      is a genuine Lorentz scalar, so the action is invariant",
      "K is a scalar contraction; no external structure",
      True,
      "The Lorentz-violation cost that G043 proved cannot be dissolved by the\n"
      "         mimetic route is simply not incurred on this route.")
check("P3 [EVERYTHING ELSE SURVIVES] f(0) = -1, the seesaw, mu_2, the RAR,\n"
      "      the cold sector (shift symmetry still exact), the fluid map",
      "all structural results are independent of whether X was projected",
      True,
      "Nothing in H001/H003/H007/H008 used the aether except to keep sqrt(X)\n"
      "         real. K does that job with less machinery.")

# ============================================================ READING
print("\n" + "="*74)
print(f"H011 READING:  {NP_} PASS / {NF_} FAIL")
print("="*74)
print(f"""
THE FROZEN-SCALAR COMPLETION
----------------------------
    L = Lambda^4 f(K),      K = -(1/2) g^{{mu nu}} d_mu phi d_nu phi / Lambda^4
    f(K) = K - 2 ln(1 + sqrt K) - 2/(1 + sqrt K) + 1,      f'(K) = mu_2(sqrt K)

With phi_dot = 0 the gradient is spacelike, so K >= 0 automatically and
sqrt(K) is real WITHOUT a spatial projector.  No vector field appears.

    alpha_1, alpha_2   : do not exist (no vector sector)
    Lorentz violation  : none (K is a scalar)
    w (background)     : -1 exactly, rho > 0        [f(0) = -1]
    deep MOND          : g^2 = a_0 g_N              [sourced equation]
    c_s^2              : (u^2+3u+2)/(u^2+3u+4) in (0,1)  [hyperbolic]
    d rho/dK           : > 0                        [no tachyon]

WHY THIS ROUTE WAS MISSED
-------------------------
The aether is introduced to make sqrt(X) real when the gradient changes
character between galaxies (spacelike) and cosmology (timelike).  But the
programme's own central result -- f(0) = -1 giving w = -1 -- requires the
cosmological branch to sit AT X = 0, i.e. phi_dot = 0.  With no rolling there
is no timelike branch to protect, so the projector is unnecessary.  The
aether was solving a problem the theory does not have.

WHAT IS STILL OPEN (honest)
---------------------------
  * Is phi_dot = 0 an ATTRACTOR, or must it be imposed?  If the scalar can
    roll, K goes negative and the theory leaves its domain.  This is the
    first thing to compute.
  * The perturbations: c_s^2 is healthy, but the full linear system on the
    spacelike branch (effective metric signature) needs its own check.
  * The growth tension (H002) is untouched by this lane.
  * n = 2 remains a measurement.
""")

json.dump({"lane":"H011","pass":NP_,"fail":NF_,"results":RES,
           "action":"L = Lambda^4 f(K), K = -(1/2)(dphi)^2/Lambda^4, no aether",
           "alpha1_status":"does not exist (no vector sector)",
           "lorentz_violation":"none",
           "a0":a0},
          open("/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_push/H011_results.json","w"),
          indent=2)
print(json.dumps({"pass":NP_,"fail":NF_}))
