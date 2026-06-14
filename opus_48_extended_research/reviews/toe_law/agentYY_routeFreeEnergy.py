"""
agentYY — ROUTE 1: the crossed-product FREE ENERGY F(a) along a boost orbit.

THE DECISIVE QUESTION (WW's named next calc):
  Does the dressed type II_1 observer's free energy F(a) = E(a) - T(a) S_gen(a)
  along a boost orbit of proper acceleration a have a genuine thermodynamic EXTREMUM
  (dF/da = 0) or a transition AT a ~ cH = H -- forcing the inertial-transition scale
  from the type II_1 modular thermodynamics WITHOUT phi -- or is F(a) monotone so the
  scale stays external (STRUCTURAL CEILING CONFIRMED)?

UNITS: hbar = c = k_B = 1. cH = H.

BANKED INGREDIENTS (do NOT re-derive; cite):
  - modular temperature on a boost orbit of proper accel a:
        T(a) = sqrt(a^2 + H^2) / (2 pi)            [WW machine-verified Tolman identity]
    (this is T_DL = Tolman blueshift of GH temperature H/2pi; H = surface gravity/dS scale)
  - crossed product (Witten 2112.12828, CLPW 2206.10780):
        dressed modular generator  hat_h = H_mod + q,  q >= 0 = observer clock energy,
        density operator  rho_hat ~ exp(-beta hat_h),  beta = 2pi/kappa = 2pi/H (boost time).
        type II_1: the +q makes the trace FINITE.
  - Witten generalized entropy of the dressed observer (2112.12828 eq for S):
        S_gen = <beta hat_h> + S_out + const   ===   <hat_h>/T + S_QFT
    i.e. the OBSERVER energy contributes  <h_obs>/T  to the generalized entropy, on top of
    the bulk QFT/area entropy S_out.

THE PHYSICS WE MUST GET RIGHT (the central trap, per the task):
  T(a) = sqrt(a^2+H^2)/2pi has dT/da > 0 ALWAYS -- the a~H crossover of T is NOT an extremum
  of T. For F to have an extremum at a~H, the OBSERVER's h_obs / the type II_1 trace must
  supply COMPETING a-dependence. We test exactly that, transparently, for the natural
  crossed-product energy assignments -- and report honestly whether a stationary point lands
  at a~H or whether F is monotone.
"""
import sympy as sp

a, H, q0, S0, beta = sp.symbols('a H q0 S0 beta', positive=True)
pi = sp.pi

print("="*78)
print("agentYY ROUTE 1 -- crossed-product free energy F(a) along a boost orbit")
print("="*78)

# ---------------------------------------------------------------------------
# Modular temperature on the boost orbit (banked, WW Tolman identity)
# ---------------------------------------------------------------------------
T = sp.sqrt(a**2 + H**2) / (2*pi)
dT = sp.diff(T, a)
print("\n[T] modular temperature T(a) = sqrt(a^2+H^2)/2pi")
print("    dT/da =", sp.simplify(dT), "  (positive for all a>0 => crossover, NOT an extremum of T)")
print("    sign check dT/da at a=H/2,H,2H:",
      [sp.N(dT.subs({H:1, a:v})) for v in (sp.Rational(1,2), 1, 2)])

# ---------------------------------------------------------------------------
# The crossed-product thermodynamic objects.
#
# Witten 2112.12828: the dressed (gravitationally constrained) state of the type II_1
# observer algebra is rho_hat ~ exp(-beta hat_h), hat_h = H_mod + q, beta = 2pi/H in
# BOOST time. The generalized entropy is
#       S_gen = <hat_h>/T_boost + S_out + const
# where T_boost = H/2pi is the boost-time KMS temperature, S_out the bulk QFT/area entropy.
#
# On a PROPER-TIME worldline of acceleration a, the SAME flow is re-clocked: the locally
# measured temperature is T(a) = H/(2pi|xi|) = sqrt(a^2+H^2)/2pi (Tolman), and the locally
# measured observer energy is the BLUESHIFTED clock energy  E_obs(a) = <q>/|xi| = <q> T(a)/T_GH
# (energy and temperature blueshift by the SAME Tolman factor 1/|xi| -- this is forced, both
# are 1/time).
#
# So with |xi| = H / sqrt(a^2+H^2) = T_GH/T(a):
#     blueshift factor  B(a) = 1/|xi| = sqrt(a^2+H^2)/H = T(a)/T_GH = 2 pi T(a)/H
# ---------------------------------------------------------------------------
B = sp.sqrt(a**2 + H**2)/H                     # Tolman blueshift 1/|xi|
T_GH = H/(2*pi)
print("\n[B] Tolman blueshift B(a)=1/|xi| =", B, " ; check B = T/T_GH:",
      sp.simplify(B - T/T_GH))

print("\n" + "="*78)
print("MODEL A -- the literal Witten generalized entropy, S_gen = <hat_h>/T + S_out")
print("="*78)
# Observer energy (proper, blueshifted): E(a) = q0 * B(a). Bulk entropy S_out = S0 (the
# GH/area entropy A/4G of the cosmological horizon -- an a-INDEPENDENT constant; the horizon
# the observer sees is the SAME dS horizon for every boost orbit).
E_A   = q0 * B
Sgen_A = E_A / T + S0          # <hat_h>/T + S_out   (the literal crossed-product S_gen)
F_A   = E_A - T*Sgen_A
F_A   = sp.simplify(F_A)
dF_A  = sp.simplify(sp.diff(F_A, a))
print("  E(a)      =", sp.simplify(E_A))
print("  S_gen(a)  =", sp.simplify(Sgen_A))
print("  F(a)=E-T S =", F_A)
print("  dF/da      =", dF_A)
sols_A = sp.solve(sp.Eq(dF_A, 0), a)
print("  stationary points dF/da=0 :", sols_A)
# evaluate F monotonicity numerically
fnum = sp.lambdify(a, F_A.subs({H:1, q0:1, S0:1, pi:sp.pi}), 'mpmath')
print("  KEY: <hat_h>/T = E/T is a-INDEPENDENT (E and T blueshift identically) =>")
print("       F(a) = -T(a) S0 = -S0 sqrt(a^2+H^2)/2pi  is MONOTONE-DECREASING, no extremum.")
print("  F at a=0,H,2H,10H:", [sp.N(F_A.subs({H:1,q0:1,S0:1,a:v})) for v in (0,1,2,10)])

print("\n" + "="*78)
print("MODEL B -- proper-energy reading: F is the PROPER free energy, S_gen from the")
print("           BOOST-frame entropy (a-independent), but E,T in proper frame")
print("="*78)
# Here S_gen is the dimensionless ENTROPY (a state quantity, frame-INVARIANT): S_gen = q0/T_GH*?
# Entropy is a pure number (counts states) -> it does NOT blueshift. The boost-frame entropy is
# S_gen^boost = <q>/T_GH + S0 = 2pi q0/H + S0 (a-independent). Proper free energy:
Sgen_B = q0/T_GH + S0          # entropy = frame-invariant pure number (a-independent)
F_B = q0*B - T*Sgen_B          # E_proper - T_proper * S
F_B = sp.simplify(F_B)
dF_B = sp.simplify(sp.diff(F_B, a))
print("  S_gen (invariant) =", sp.simplify(Sgen_B))
print("  F(a) =", F_B)
print("  dF/da =", dF_B)
print("  dF/da factor:", sp.factor(sp.simplify(dF_B*2*pi*H*sp.sqrt(a**2+H**2))))
sols_B = sp.solve(sp.Eq(dF_B,0), a)
print("  stationary points dF/da=0 :", sols_B)
# F_B = B*q0 - T*(q0/T_GH + S0) = q0*B - (T/T_GH)*q0 - T*S0 = q0*B - B*q0 - T*S0 = -T*S0  again!
print("  NOTE: F_B simplifies to", sp.simplify(F_B - (-T*S0)), "+ (-T*S0) => again -T*S0, MONOTONE.")

print("\n" + "="*78)
print("MODEL C -- HOSTILE: give the QFT bath an a-dependent thermal entropy S_QFT(T(a))")
print("           (the only way to break the Tolman cancellation). Does an extremum appear?")
print("="*78)
# A genuinely a-dependent S_out: the thermal QFT bath the detector sees has temperature T(a).
# For a d-dim conformal bath S_QFT ~ c_th * T^(d-1) per unit (modular) volume. Most hostile/
# generous: let S_QFT carry an arbitrary power, S_QFT = c_th * (2pi T)^n = c_th*(a^2+H^2)^(n/2).
# E_bath = energy of that bath ~ d/(d? ) -- use the thermodynamic relation for a free thermal
# system: F = E - T S with E = sigma T^(n+1)*Vol, S = (n+1)/n * ... -> but to be model-free we
# directly ask: can ANY F(a) = E(a) - T(a) S(a) built from these blueshift-locked pieces be
# stationary at finite a? Test the conformal bath explicitly.
n, c_th, d = sp.symbols('n c_th d', positive=True)
# Conformal thermal gas in the static patch: S_QFT = c_th * T^n (n = spatial dim of the bath),
# E_QFT = (n) * c_th/(n+? ) ... use the standard F = -(1/(n+1)) * (sigma) T^{n+1}? For a gas
# F_gas = E - T S with E = n*P*V-type. Cleanest: take the EQUATION OF STATE of a conformal gas
# F_gas(T) = - K * T^{n+1}  (K>0), so S = -dF/dT = K(n+1)T^n, E = F+TS = K n T^{n+1}. (standard)
K = sp.symbols('K', positive=True)
Tn = sp.sqrt(a**2+H**2)/(2*pi)
F_gas = -K*Tn**(n+1)                     # conformal-gas free energy at the LOCAL temperature
# Add the constant horizon/area entropy contribution -T*S0 (Model A core) and the a-invariant
# observer term (drops). Total proper free energy:
F_C = -K*Tn**(n+1) - Tn*S0
dF_C = sp.simplify(sp.diff(F_C, a))
print("  F_C(a) = -K T^(n+1) - T S0 ,  T=sqrt(a^2+H^2)/2pi")
print("  dF/da  =", dF_C)
# stationary: dF/da = -[K(n+1)T^n + S0] * dT/da = -[...]*a/(2pi sqrt) ; bracket > 0 always =>
brk = sp.simplify(K*(n+1)*Tn**n + S0)
print("  dF/da = -(K(n+1)T^n + S0) * a/(2pi sqrt(a^2+H^2)); bracket =", brk, " (>0 for all a)")
print("  => dF/da has the sign of -a : MONOTONE-DECREASING for all a>0, NO interior extremum.")
print("  stationary at a=0 only (the boundary, the GH/unaccelerated point), NOT at a~H.")

print("\n" + "="*78)
print("THEOREM (the structural ceiling): why NO crossed-product F(a) is stationary at a~H")
print("="*78)
print("""  Every thermodynamic potential built from the boost-modular data is a function of the
  single state variable T (boost-KMS temperature, Tolman-clocked) -- because the crossed
  product fixes ONE generator (beta=2pi/H, boost) and the worldline enters ONLY through the
  Tolman factor |xi|, i.e. ONLY through T(a). Energy and entropy pieces both blueshift by the
  SAME 1/|xi|, so:
     F(a) = Phi(T(a))   for some Phi.
  Then  dF/da = Phi'(T) * dT/da,  and  dT/da = a/(2pi sqrt(a^2+H^2)) > 0 for ALL a>0,
  vanishing ONLY at a=0. Therefore dF/da=0 at interior a REQUIRES Phi'(T)=0 -- a stationary
  point of the free energy IN TEMPERATURE. But T(a~H) = sqrt(2)H/2pi is just an ordinary
  interior temperature with nothing special about it: H sets the OFFSET inside sqrt(a^2+H^2),
  it does NOT create a zero of Phi'(T). The crossover a~H is where the two TERMS of T are
  comparable -- a feature of T's algebra, NOT a stationary point of any Phi(T).
  => For F(a) to be stationary at a~H, Phi(T) would have to know about H TWICE (once in T(a),
     once to place Phi'=0 exactly at T(sqrt 2 H/2pi)). The crossed product supplies H only
     ONCE (as the modular offset). Hence NO extremum at a~H is forced. STRUCTURAL CEILING.""")

print("\n" + "="*78)
print("HOSTILE LOOPHOLE TEST -- could Phi'(T)=0 at an interior T (turnover), landing a~H?")
print("="*78)
# The ONLY way: two terms of OPPOSITE sign in T with different powers, Phi(T)=A*T^p - C*T^r.
# Then Phi'(T)=0 at T* = (C r/(A p))^{1/(p-r)} -- a stationary T EXISTS. Does it land at a~H?
# It lands at a~H ONLY if the coefficients A,C,p,r are TUNED so that T* = sqrt(2)H/2pi. That
# tuning is an INPUT (you must already know H AND choose A,C). The algebra does NOT supply it.
A_, C_, p_, r_, Tsym = sp.symbols('A C p r Tsym', positive=True)
Phi = A_*Tsym**p_ - C_*Tsym**r_
dPhi_dT = sp.diff(Phi, Tsym)
Tstar = sp.solve(sp.Eq(dPhi_dT, 0), Tsym)
print("  Phi(T)=A T^p - C T^r  => Phi'(T)=0 at T* =", Tstar)
print("  This T* is set by (A,C,p,r) -- FREE coefficients. Demanding T*=T(a=H)=sqrt(2)H/2pi")
print("  is a CONSTRAINT you impose by hand (must input H and tune A/C). NOT algebra-forced.")
print("  => even WITH a turnover, a~H is an INPUT-tuned coincidence, not a derived scale.")
print("     (And the crossed product gives NO such opposite-sign competing term: E>=0, S>=0,")
print("      F=E-TS with S>=0 monotone in T -> F monotone, as Models A-C confirmed.)")

print("\n" + "="*78)
print("TRANSITION TEST -- is a~H special as a DOMINANT-TERM crossover (even w/o extremum)?")
print("="*78)
# F = E - T S. The crossover a~H is where the two TERMS inside T=sqrt(a^2+H^2)/2pi are equal:
#   Unruh piece a/2pi vs GH piece H/2pi equal at a=H. This IS a real crossover -- but it is the
#   crossover of the TEMPERATURE'S algebra (descriptive), reproduced by the structural identity,
#   NOT a thermodynamic extremum or phase transition of F (no latent heat, no dF/da=0, no
#   discontinuity in any derivative -- everything is smooth/analytic in a^2). Demonstrate:
import mpmath as mp
mp.mp.dps = 30
def Tval(av): return mp.sqrt(av**2+1)/(2*mp.pi)        # H=1
def F_lit(av): return -Tval(av)*1                       # Model A core, S0=1
# second derivative continuity / no singularity at a=1:
for av in [mp.mpf('0.5'), mp.mpf('0.99'), mp.mpf('1'), mp.mpf('1.01'), mp.mpf('2')]:
    d2 = mp.diff(lambda x: F_lit(x), av, 2)
    print(f"   a/H={float(av):4.2f}: F={float(F_lit(av)): .6f}  F''={float(d2): .6f} (smooth, finite, no kink at a=H)")
print("  => a~H is a smooth crossover of T's two terms (DESCRIPTIVE algebra), NOT a")
print("     thermodynamic phase transition: no kink, no jump, no extremum in F. ")

print("\n" + "="*78)
print("FULL DESER-LEVIN with c_chi: does sqrt(a^2 + (c_chi H)^2) change the verdict?")
print("="*78)
cch = sp.symbols('c_chi', positive=True)
T_full = sp.sqrt(a**2 + (cch*H)**2)/(2*pi)
dT_full = sp.simplify(sp.diff(T_full, a))
print("  T_full(a)=sqrt(a^2+(c_chi H)^2)/2pi ; dT/da =", dT_full, " (>0 for all a>0)")
print("  Same structure: F=Phi(T_full), dT_full/da>0 vanishing only at a=0. The crossover")
print("  now sits at a~c_chi H (still an INPUT scale set by H and c_chi). NO extremum forced;")
print("  c_chi only RELABELS the offset inside the sqrt -- it does not create a zero of Phi'.")

print("\n" + "="*78)
print("FINAL VERDICT")
print("="*78)
print("""  F(a) = E(a) - T(a) S_gen(a) built from the type II_1 crossed-product modular data is
  a function of T(a) alone, and T(a) is strictly monotone in a (dT/da=a/(2pi sqrt)>0). Hence:
    * dF/da = 0 has NO interior solution at a~H (Models A,B,C all give F=Phi(T), monotone);
    * the observer-energy term <h_obs>/T is a-INVARIANT (E and T blueshift identically) -- the
      Tolman factor cancels, killing the one piece that could have competed;
    * a~H is the smooth ALGEBRAIC crossover of T's two terms (descriptive), NOT a thermodynamic
      extremum or phase transition of F (no kink, no jump, smooth in a^2);
    * an extremum at a~H would require Phi'(T)=0 to be TUNED to T(a=H) -- the crossed product
      supplies H only ONCE (the modular offset), so it cannot place the zero. NOT FORCED.
  ==> STRUCTURAL CEILING CONFIRMED. The a0 scale (a~cH) stays an EXTERNAL input. The type II_1
      free energy REPRODUCES the crossover algebraically; it does not DERIVE the scale.
      Coefficient quarantine HELD: Z / q=1/4 never asserted (no extremum even lands at a~H to
      probe a coefficient).""")
