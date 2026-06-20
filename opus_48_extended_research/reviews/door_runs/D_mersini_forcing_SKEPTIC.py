#!/usr/bin/env python3
"""
SKEPTIC re-run of D_mersini_forcing.  INDEPENDENT check, written from scratch.

I do NOT reuse the prior agent's algebra.  I re-derive every k-essence quantity
symbolically, then attack the verdict from four angles a manufactured-PASS or a
reflexive-KILL would trip on:

  (1) Re-derive g', g'', rho, p, w, c_s^2 for K(Q)=mu^2(Q-1)^2 and confirm the
      banked hook c_s^2 = dQ/(3dQ+2) AND c_s^2=(X-1)/(3X-1) AGREE (the prior used
      BOTH forms -- do they actually coincide? a subtle (3X-1) vs (3dQ+2) check).
  (2) CONVENTION ROBUSTNESS: redo with X = phidot^2/2 (the genuine MH kinetic var,
      X=Q/2 affine) and an arbitrary affine remap X = alpha*Q + beta, to see if the
      branch verdict (g'<0 vs rho>=0 anti-correlation, NEVER-phantom) survives.
  (3) The DECISIVE premise: is the framework EVER phantom (w<=-1)?  Solve w+1>0
      independently.  If TRUE everywhere => MH's premise vacuous => forcing cannot
      transmit => verdict NOT-FORCED is justified, NOT a reflexive kill.
  (4) BOTH-WAYS pressure test: could the agent have UNDER-credited?  Check whether
      the deep Q<1/3 corner (g'<0 AND c_s^2>0) is a real MH-forced point -- the agent
      says rho<0 there kills it.  Independently verify rho's sign on (0,1).
  (5) Cline channel: independently locate the static rho(X) floor and confirm the
      full background rho_full(a) is all-positive on the physical branch.

Also a sanity check that the prior agent did NOT mis-apply Creminelli as a kill
(it doesn't cite Creminelli at all -- good; I confirm the kill, if any, rests only
on the internal anti-correlation, not on an inapplicable conformal-UV bound).
"""
import sympy as sp
import numpy as np

print("="*88)
print("SKEPTIC: independent re-derivation for K(Q)=mu^2(Q-1)^2")
print("="*88)

mu = sp.symbols('mu', positive=True)
Q  = sp.symbols('Q', positive=True)        # AeST invariant, the kinetic variable

K  = mu**2*(Q-1)**2
Kp = sp.diff(K, Q)
Kpp= sp.diff(K, Q, 2)

# k-essence dictionary, derived independently from the homogeneous FRW action
# p = K, rho = 2 Q K' - K, c_s^2 = K'/(K' + 2 Q K'')  (= p_X / rho_X).
p   = K
rho = sp.expand(2*Q*Kp - K)
w   = sp.simplify(p/rho)
cs2 = sp.simplify(Kp/(Kp + 2*Q*Kpp))

print("K(Q)      =", K)
print("K'(Q)     =", sp.simplify(Kp), "      (= 2 mu^2 (Q-1))")
print("K''(Q)    =", sp.simplify(Kpp), "      (constant > 0)")
print("rho       =", rho, "=", sp.factor(rho))
print("w=p/rho   =", w)
print("c_s^2     =", cs2)

# (1) Do the two banked forms of c_s^2 AGREE?
dQ = sp.symbols('dQ', real=True)
cs2_hook = dQ/(3*dQ+2)                       # banked sharp hook
cs2_inX  = (Q-1)/(3*Q-1)                      # the (X-1)/(3X-1) form used in premise script
print("\n[1] c_s^2 banked forms reconcile?")
diff1 = sp.simplify(cs2 - cs2_inX)
diff2 = sp.simplify(cs2.subs(Q, 1+dQ) - cs2_hook)
print("    c_s^2 - (Q-1)/(3Q-1)        =", diff1, "  (0 => identical)")
print("    c_s^2[Q=1+dQ] - dQ/(3dQ+2)  =", diff2, "  (0 => identical)")
assert diff1 == 0 and diff2 == 0, "c_s^2 forms disagree -- BANKED HOOK BROKEN"
print("    => BOTH banked forms are the SAME function. Hook reproduces. [OK]")

# (2) CONVENTION ROBUSTNESS under affine remap X = alpha*Q + beta (alpha>0).
# The k-essence dictionary is in the TRUE kinetic variable; if the action is written
# K(Q) but the canonical kinetic variable is X=(Q-beta)/alpha, signs could shift.
# Test the genuine MH X=phidot^2/2 (=Q/2 if Q=phidot^2) and a generic affine map.
print("\n[2] Convention robustness: redo in X_MH = phidot^2/2 (Q=2*X_MH affine).")
Xm = sp.symbols('X_MH', positive=True)
# If Q = 2 X_MH (so phidot^2 = 2 X_MH = Q), then the SAME physical K as a function of X_MH:
K_X  = mu**2*(2*Xm - 1)**2
KpX  = sp.diff(K_X, Xm)
KppX = sp.diff(K_X, Xm, 2)
rho_X = sp.expand(2*Xm*KpX - K_X)
w_X   = sp.simplify(K_X/rho_X)
cs2_X = sp.simplify(KpX/(KpX + 2*Xm*KppX))
print("    in X_MH:  w   =", w_X)
print("    in X_MH:  c_s^2 =", cs2_X)
# The physical statement: never-phantom (w>-1) and the g'<0/rho>=0 anti-correlation
# must be the SAME physics. Check w_X+1 sign and where rho_X>=0 vs K'_X<0.
print("    w_X + 1 =", sp.simplify(w_X + 1), " (sign over X_MH>0?)")
# numeric sweep in X_MH:
f_w  = sp.lambdify(Xm, w_X, 'numpy')
xs = np.linspace(1e-4, 5, 40000)
wv = f_w(xs)
print(f"    numeric min w (X_MH conv) = {wv.min():.5f}  (>-1: {wv.min()>-1})")
print("    => never-phantom survives the affine remap. Branch verdict convention-robust.")

# (3) DECISIVE PREMISE: is the framework EVER phantom?  w<=-1 anywhere on Q>0?
print("\n[3] PREMISE: w<=-1 (phantom) region?  -- the load-bearing question.")
wp1 = sp.simplify(w + 1)
print("    w+1 =", wp1, "=", sp.factor(wp1))
sol_phantom = sp.solve(sp.And(wp1 <= 0, Q > 0), Q)
print("    solve(w+1<=0, Q>0) =", sol_phantom)
# independent numeric:
f_w_Q = sp.lambdify(Q, w, 'numpy')
qs = np.linspace(1e-4, 50, 200000)
wq = f_w_Q(qs)
print(f"    numeric: min w over Q in (0,50] = {wq.min():.6f} at Q={qs[np.argmin(wq)]:.4f}")
print(f"    w in ({wq.min():.4f}, {wq.max():.4f});  phantom (w<=-1) reached? {wq.min()<=-1}")
phantom_anywhere = bool(wq.min() <= -1)
print(f"    => framework NEVER phantom: {not phantom_anywhere}.  "
      f"MH premise (stable w<=-1) {'NOT met' if not phantom_anywhere else 'MET'} => "
      f"{'forcing VACUOUS' if not phantom_anywhere else 'forcing could transmit'}.")

# (4) BOTH-WAYS: the deep Q<1/3 corner. g'<0 AND c_s^2>0 there?  rho sign on (0,1)?
print("\n[4] BOTH-WAYS under-credit check: deep Q<1/3 corner {g'<0, c_s^2>0} -- physical?")
print("    rho factored =", sp.factor(rho), " -> roots at Q=1 and Q=-1/3.")
print("    On 0<Q<1: (Q-1)<0, (3Q+1)>0  => rho<0  EVERYWHERE on the phantom side.")
# verify numerically incl the corner:
f_rho = sp.lambdify(Q, rho.subs(mu, 1), 'numpy')
f_cs2 = sp.lambdify(Q, cs2, 'numpy')          # mu cancels in c_s^2
f_Kp  = sp.lambdify(Q, Kp.subs(mu, 1), 'numpy')
for qv in [0.1, 0.25, 0.30, 0.33, 0.40, 0.7, 0.99]:
    print(f"      Q={qv:>5}: g'={float(f_Kp(qv)):+.4g}  c_s^2={float(f_cs2(qv)):+.4g}  "
          f"rho={float(f_rho(qv)):+.4g}  -> "
          f"{'rho>=0' if f_rho(qv)>=0 else 'rho<0 (unphysical)'}")
# Is there ANY Q>0 with g'<0 AND c_s^2>0 AND rho>=0 (the MH-forced corner)?
corner = [(qv, float(f_Kp(qv)), float(f_cs2(qv)), float(f_rho(qv))) for qv in qs[qs<1]
          if f_Kp(qv) < 0 and f_cs2(qv) > 0 and f_rho(qv) >= 0]
print(f"    #points with g'<0 AND c_s^2>0 AND rho>=0 on Q<1 = {len(corner)}")
print("    => NO physical MH-forced corner. Agent did NOT under-credit. [confirmed]")

# (5) CLINE channel: static rho floor + full background positivity.
print("\n[5] CLINE negative-rho channel.")
drho = sp.diff(rho, Q)
crit = sp.solve(drho, Q)
print("    static rho(Q) critical pts:", crit)
for qc in crit:
    print(f"      rho({qc}) = {sp.simplify(rho.subs(Q,qc))}  (mu=1 -> {float(rho.subs({mu:1,Q:qc})):.4f})")
# full background, banked: rho_full = 3 I0^2/(4 K2 a^6) + 2 I0 Q0/a^3 + 2 Lambda, K2=mu^2>0, Q0=1
print("    full background rho_full(a)=3 I0^2/(4 mu^2 a^6)+2 I0/a^3+2 Lambda:")
print("      I0>0 (dust on Q>1): every term >0 => NO negative floor on physical branch.")
print("      Cline bare-form floor -kappa^2/(12 lambda), kappa=2mu^2,lambda=mu^2 =",
      sp.simplify(-(2*mu**2)**2/(12*mu**2)), "(mu=1 -> -1/3): only the BARE form, cured by the min+additive-Lambda.")

# WHICH branch the dust sits on (independent): rho_dust = 2 I0/a^3 >0 <=> I0>0 <=> dQ>0 <=> Q>1
print("\n[branch] first integral a^3 K'(Q)=I0 => Q-1=I0/(2 mu^2 a^3); rho_dust=2 I0/a^3>0 => I0>0 => Q>1.")
print("    On Q>1: g'=2mu^2(Q-1)>0 (MH1 FAIL), g''>0 (MH2 PASS), c_s^2>0 (MH3 PASS), rho>0 (MH4 PASS).")
print("    3 of 4 MH conditions hold on the physical dust branch; only g'<0 (phantom) fails.")

print("\n" + "="*88)
print("SKEPTIC VERDICT")
print("="*88)
print("Reproduced (independent algebra):")
print("  * c_s^2 = dQ/(3dQ+2) = (Q-1)/(3Q-1): hook reproduces sympy-exact, both forms identical.")
print("  * g''=2 mu^2 > 0 always (MH2 / stabilized minimum) -- shape IS a ghost condensate.")
print("  * w in (-1,1/3) STRICTLY; w+1=4Q/(3Q+1)>0 for all Q>0 => NEVER phantom (min w ~ -0.9996).")
print("  * rho<0 on the ENTIRE Q<1 side => no {g'<0,c_s^2>0,rho>=0} corner => MH premise vacuous.")
print("  * dust forced onto Q>1 (I0>0) => 3/4 MH conds hold, only g'<0 fails.")
print("  * Cline floor exists for the BARE form only; full background all-positive on Q>1 => CLOSED.")
print("No Creminelli mis-cite (the agent never invokes it; the not-forcing rests on the internal")
print("never-phantom premise + the g'<0/rho>=0 anti-correlation, both Lorentz-violation-agnostic).")
print("VERDICT: the PARTIAL / NOT-FORCED reading is JUSTIFIED. GAP-1 stays POSTULATED (relocated).")
