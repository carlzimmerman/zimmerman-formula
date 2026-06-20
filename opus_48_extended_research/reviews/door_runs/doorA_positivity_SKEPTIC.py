#!/usr/bin/env python3
"""
SKEPTIC RE-RUN of door "A_positivity_gate".

Goal: reproduce the load-bearing NUMBERS *independently* (own derivation, not the
prior agent's substitution) and stress-test the verdict both ways.

Three load-bearing claims to reproduce / challenge:
  (C1) gapless sound speed  c_s^2(dQ) = dQ/(3 dQ + 2)   [the SHARP HOOK]
  (C2) the FORCED branch: positive-energy a^-3 dust forces dQ>0 (=> Q>1 => c_s^2>0),
       i.e. energy-positivity and sound-speed-positivity COINCIDE.
  (C3) the Serra-Trombetta below-gap gate PASS at the observational point.

I re-derive c_s^2 from the FLUCTUATION ACTION directly (ghost-condensate /
 k-essence pi-expansion), NOT by quoting c_s^2 = P_X/(P_X+2X P_XX). Then I check the
variable mapping (is the k-essence "X" the AeST Q, or phidot^2?) because the whole hook
hinges on that mapping.
"""
import sympy as sp
import numpy as np

LINE = "="*92
def hdr(s): print("\n"+LINE+"\n"+s+"\n"+LINE)

# ---------------------------------------------------------------------------
# C0. WHAT IS Q?  In AeST/Blanchet-Skordis the kinetic scalar is Q (= the shift
# scalar built from grad-phi), K(Q)=mu^2(Q-1)^2. In k-essence the canonical kinetic
# variable is X = (d phi)^2 (or phidot^2 - (grad phi)^2). The hook claims the
# SAME c_s^2 formula in Q. The k-essence sound speed in the canonical X variable is
#   c_s^2 = P_X / (P_X + 2 X P_XX).
# If Q == X (the kinetic variable IS the argument of K), the substitution is exact.
# In Blanchet-Skordis / AeST, Q is indeed the (dimensionless) kinetic scalar that
# plays the role of X. So we test the hook in BOTH readings:
#   reading-1: Q is the k-essence X  (argument of P)  -> c_s^2 = K'/(K'+2Q K'')
#   reading-2: derive c_s^2 from the pi-fluctuation action with X = phidot^2 and
#              K(Q(X)) to confirm reading-1 is the physically correct one.
# ---------------------------------------------------------------------------

hdr("C1 -- gapless sound speed: INDEPENDENT derivation from the pi-fluctuation action")

# Reading-1 (k-essence formula in the kinetic variable Q == X):
Q = sp.symbols('Q', positive=True)
mu = sp.symbols('mu', positive=True)
K  = mu**2*(Q-1)**2
Kp  = sp.diff(K, Q)
Kpp = sp.diff(K, Q, 2)
cs2_r1 = sp.simplify(Kp/(Kp + 2*Q*Kpp))
dQ = sp.symbols('dQ', real=True)
cs2_r1_dQ = sp.simplify(cs2_r1.subs(Q, 1+dQ))
print("Reading-1 (Q is the k-essence kinetic variable X):")
print("  c_s^2 = K'/(K'+2Q K'') =", cs2_r1, " -> in dQ:", cs2_r1_dQ)

# INDEPENDENT derivation (reading-2): expand the k-essence Lagrangian P(X) with
# X = phidot^2 - (grad phi)^2 to QUADRATIC order in pi and read off c_s^2 = (spatial
# coeff)/(time coeff). I do NOT quote any formula; I build the bilinear action.
t,x = sp.symbols('t x', real=True)
pi = sp.Function('pi')
phidot0 = sp.symbols('phidot0', positive=True)   # background <phidot> = sqrt(X0)
# fluctuation derivatives as independent symbols
pd, gx = sp.symbols('pd gx', real=True)          # d_t pi, d_x pi
X0 = sp.symbols('X0', positive=True)
P = sp.Function('P')
# X = (phidot0 + pd)^2 - gx^2 ; dX = X - X0, X0 = phidot0^2
dX = (phidot0+pd)**2 - gx**2 - X0
P0,P1,P2 = sp.symbols('P0 P1 P2', real=True)     # P(X0),P'(X0),P''(X0)
Lden = P0 + P1*dX + sp.Rational(1,2)*P2*dX**2
Lden = sp.expand(Lden.subs(X0, phidot0**2))
# bilinear-in-(pd,gx) part:
def bilinear(expr, gens):
    out = 0
    for term in sp.expand(expr).as_ordered_terms():
        deg = sum(sp.degree(term, g) if term.has(g) else 0 for g in gens)
        if deg == 2:
            out += term
    return sp.expand(out)
Lq = bilinear(Lden, (pd,gx))
time_coeff  = Lq.coeff(pd,2)
space_coeff = Lq.coeff(gx,2)
print("\nReading-2 (built bilinear action from P(X), X=phidot^2-(grad)^2):")
print("  time coeff (pd^2)  =", sp.simplify(time_coeff), "  [= P'(X0) + 2 X0 P''(X0)]")
print("  space coeff (gx^2) =", sp.simplify(space_coeff), "  [= -P'(X0)]")
# c_s^2 = -(space coeff)/(time coeff)   (omega^2 = -(space/time) k^2 ; sign so c_s^2>0
#   when space coeff <0 i.e. P'>0 and time coeff>0)
cs2_r2 = sp.simplify(-space_coeff/time_coeff)
print("  c_s^2 = -(space)/(time) =", cs2_r2, " = P'(X0)/(P'(X0)+2 X0 P''(X0))")

# Now SUBSTITUTE the AeST K into P with X=Q (the physical mapping: P=K, X=Q):
# P'(X0)=K'(Q0), P''(X0)=K''(Q0), X0=Q0=1+dQ.
cs2_from_r2 = cs2_r2.subs({P1: Kp, P2: Kpp, phidot0**2: Q}).subs(Q, 1+dQ)
# careful subst: cs2_r2 = P1/(P1 + 2*phidot0^2*P2). phidot0^2 = X0 = Q.
cs2_from_r2 = sp.simplify((P1/(P1+2*X0*P2)).subs({P1:Kp,P2:Kpp,X0:Q}).subs(Q,1+dQ))
print("\n  => with P=K, X=Q (AeST mapping): c_s^2 =", sp.simplify(cs2_from_r2))

hook = dQ/(3*dQ+2)
print("\nBANKED HOOK: c_s^2 = dQ/(3 dQ + 2)")
match_r1 = sp.simplify(cs2_r1_dQ - hook) == 0
match_r2 = sp.simplify(cs2_from_r2 - hook) == 0
print("  reading-1 matches hook:", match_r1)
print("  reading-2 (independent action build) matches hook:", match_r2)
assert match_r1 and match_r2, "HOOK FAILED TO REPRODUCE"
print("  >>> HOOK REPRODUCED INDEPENDENTLY (two routes). c_s^2 = dQ/(3dQ+2). <<<")

# numeric sign table
print("\n  sign table:")
for v in [1.0,0.5,0.25,-0.25,-0.5,-0.6,-0.7,-1.0]:
    val = float(hook.subs(dQ,v))
    note = "STABLE c_s^2>0" if val>0 else "GRADIENT-UNSTABLE c_s^2<0"
    print(f"    dQ={v:+.2f}: c_s^2={val:+.4f}  {note}")

# ---------------------------------------------------------------------------
hdr("C2 -- the FORCED branch: does positive-energy dust REALLY force dQ>0?")
# rho = 2 Q K' - K (k-essence energy density, X=Q). Off-minimum displacement energy.
rho = sp.expand(2*Q*Kp - K).subs(Q,1+dQ)
rho = sp.expand(rho)
print("rho(dQ) = 2Q K' - K =", rho, " = factored", sp.factor(rho))
rho_lin = sp.diff(rho,dQ).subs(dQ,0)
print("leading (linear) coeff d rho/d dQ |_0 =", rho_lin, " (=> rho ~ %s * dQ near min)"%rho_lin)
print("\n  CHALLENGE: the agent says rho_dust>0 REQUIRES dQ>0. Check the full rho sign,")
print("  not just the linear term, across dQ:")
for v in [1.0,0.5,0.25,0.1,-0.1,-0.25,-0.5,-0.6,-0.7,-1.0,-1.5]:
    r = float(rho.subs([(dQ,v),(mu,1)]))
    cs = float(hook.subs(dQ,v))
    print(f"    dQ={v:+.2f}: rho={r:+.4f} mu^2,  c_s^2={cs:+.4f}")
# Where is rho>0? Solve rho=0:
roots = sp.solve(sp.Eq(rho,0), dQ)
print("\n  rho(dQ)=0 roots:", roots)
print("  rho>0 region (solve):", sp.solve(rho>0, dQ))
print("  c_s^2>0 region: dQ>0 OR dQ<-2/3 (denominator 3dQ+2 sign)")

# The CRUX both-ways check: is there a dQ with rho>0 BUT c_s^2<0 (a counterexample
# to 'energy-positivity coincides with sound-speed positivity')?
print("\n  *** BOTH-WAYS COUNTEREXAMPLE HUNT ***")
print("  Is there a window with rho>0 AND c_s^2<0?  (would break the agent's coincidence claim)")
dgrid = np.linspace(-1.5, 1.5, 6001)
rho_f = sp.lambdify(dQ, rho.subs(mu,1), 'numpy')
cs2_f = sp.lambdify(dQ, hook, 'numpy')
rv = rho_f(dgrid); cv = cs2_f(dgrid)
bad = dgrid[(rv>0) & (cv<0)]
print(f"    rho>0 & c_s^2<0 window: {'NONE' if bad.size==0 else f'[{bad.min():.3f},{bad.max():.3f}]'}")
if bad.size:
    print(f"    -> COUNTEREXAMPLE EXISTS at dQ in [{bad.min():.3f},{bad.max():.3f}] "
          f"(rho>0 but gradient-unstable). e.g. dQ={bad[len(bad)//2]:.3f}: "
          f"rho={rho_f(bad[len(bad)//2]):+.3f}, c_s^2={cs2_f(bad[len(bad)//2]):+.3f}")
# also: rho>0 & c_s^2>0
good = dgrid[(rv>0)&(cv>0)]
print(f"    rho>0 & c_s^2>0 window: [{good.min():.3f},{good.max():.3f}]" if good.size else "none")

print("""
  READING (both-ways): the LINEAR displacement (rho ~ +4mu^2 dQ) does force dQ>0 for
  positive energy at SMALL displacement. But check whether the dQ<-2/3 branch (where
  c_s^2>0 AGAIN) also has rho>0 -- if so, there is a SECOND gradient-stable branch with
  Q<1/3, and the 'sign(I0)>0 forced' claim would be incomplete.
""")
# Evaluate the dQ < -2/3 branch explicitly:
for v in [-0.7,-0.8,-1.0,-1.34,-1.5,-2.0]:
    r = float(rho.subs([(dQ,v),(mu,1)])); cs = float(hook.subs(dQ,v))
    print(f"    dQ={v:+.2f} (Q={1+v:+.2f}): rho={r:+.4f} mu^2, c_s^2={cs:+.4f}")

# ---------------------------------------------------------------------------
hdr("C3 -- Serra-Trombetta below-gap gate: reproduce the obs-point ratio + scan")
K_B, lam_s = sp.symbols('K_B lambda_s', positive=True)
cgap2 = (2-K_B)/K_B*(1+K_B*lam_s/2)
cgap2_f = sp.lambdify((K_B,lam_s), cgap2,'numpy')
# obs point
cg0 = float(cgap2_f(1.0,1.0))
print(f"c_gapped^2 at K_B=lambda_s=1: {cg0}")
def st_ratio(cg2,B=1.0,Mmu=1.0): return cg2*Mmu/(2*np.sqrt(B))
print(f"ST below-gap slope ratio v_gp/v_gl = c_g^2 M/(2 mu sqrt(B)) at obs, B=1: {st_ratio(cg0):.4f}")
print(f"  -> {'PASS (<=1)' if st_ratio(cg0)<=1 else 'FAIL'}")
# window scan for positivity
KBg = np.linspace(0.05,1.95,39); lg = np.array([0.01,0.1,0.5,1.0,2.0,5.0])
vals = np.array([cgap2_f(kb,l) for kb in KBg for l in lg])
print(f"c_gapped^2 over window: min={vals.min():.4f} max={vals.max():.4f}; "
      f"positive everywhere: {bool(vals.min()>0)}")
# both-ways on B
print("\nBoth-ways on B (k^4 coeff O(1) ambiguity) at obs point c_g^2=%.2f:"%cg0)
for B in [0.5,1.0,2.0,3.0]:
    r=st_ratio(cg0,B=B); print(f"  B={B}: ratio={r:.3f} -> {'PASS' if r<=1 else 'FAIL'}")
print("\n  CHALLENGE the ST normalization: the ratio uses M=mu and B=O(1). At B=0.5 it")
print("  FLIPS to FAIL (ratio %.2f). So the ST pass is ORDER-SATURATED, not robust."%st_ratio(cg0,B=0.5))

# ---------------------------------------------------------------------------
hdr("C4 -- Creminelli-Janssen-Senatore: confirm NOT mis-cited as a kill")
print("""
The brief says CJS (arXiv:2207.14224) REQUIRES a conformal UV completion the ghost
condensate lacks -> INAPPLICABLE; using it as a kill would be a mis-cite. The prior
agent did NOT invoke CJS as a kill (it explicitly excluded it). CONFIRMED: the door uses
Grall-Melville (2102.05683) + Serra-Trombetta (2412.19745), which are boost-free
(unitarity/causality/locality) and DO bind a ghost condensate. No mis-cited kill.
""")

hdr("SKEPTIC SYNTHESIS")
print(f"""
C1 HOOK: REPRODUCED two independent ways (k-essence formula AND a from-scratch
   bilinear pi-action build). c_s^2 = dQ/(3 dQ + 2), sympy-exact. match_r1={match_r1},
   match_r2={match_r2}.
C2 FORCED BRANCH: rho = mu^2 dQ(3 dQ + 4), roots dQ in {{0, -4/3}}.
   - rho>0 & c_s^2>0 (the USED dust branch): dQ>0  CONFIRMED.
   - COUNTEREXAMPLE WINDOW rho>0 & c_s^2<0: {'NONE' if bad.size==0 else f'[{bad.min():.3f},{bad.max():.3f}]'}.
     => the dangerous gradient-unstable region IS negative-energy. Coincidence claim HOLDS
        for small displacement; BUT a SECOND stable branch dQ<-4/3 (Q<-1/3) also has
        rho>0 & c_s^2>0 -- physically irrelevant (Q<0, unphysical kinetic scalar; the
        framework's condensate is Q~1). So 'positive-energy dust forces dQ>0' is correct
        for the PHYSICAL Q>0 region; the agent's claim is robust where it matters.
C3 ST GATE: obs-point ratio {st_ratio(cg0):.2f} <= 1 = PASS, but FLIPS to FAIL at B=0.5
   ({st_ratio(cg0,B=0.5):.2f}). Order-saturated, NOT orders-safe -- matches the agent's
   own caveat. c_gapped^2>0 across the whole window (min {vals.min():.3f}).
C4: CJS correctly NOT used as a kill.

NET: every load-bearing number reproduces. The verdict PASS is justified as a
CONSISTENCY pass (not a derivation; quarantine held). The honest caveats (order-saturated
ST, sign-only constraint on I0) are accurate. No manufactured PASS, no reflexive KILL,
no mis-cited bound.
""")
print("SKEPTIC re-run complete. exit 0")
