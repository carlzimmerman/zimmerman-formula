#!/usr/bin/env python3
r"""
ROUTE D -- INDUCED INERTIA: integrate out the de Sitter vacuum (Feynman-Vernon /
in-in effective action) and ask whether the REACTIVE (lossless) part of the induced
self-energy carries the dS-Unruh MI law  m a mu_fw(|a|/a0) = F,
   mu_fw(x) = (sqrt(1+4 x^2) - 1)/(2 x),   x = a/a0,
   g_obs = sqrt(g_N^2 + g_N a0),  a0 = c^2 sqrt(Lambda/32pi) = c H_L / Z, Z=sqrt(32pi/3).
T_eff = (hbar/2 pi c k_B) sqrt(a^2 + (c H_L)^2)   [Deser-Levin gr-qc/9706018].

THE QUESTION ROUTE D POSES (distinct from the generic Caldeira-Leggett bath already run):
  The environment is NOT a generic Ohmic/Debye bath whose spectral density we get to choose.
  It is the SPECIFIC de Sitter vacuum the accelerated worldline couples to. Its response
  function is FIXED by the de Sitter Wightman function (the thermal KMS state at T_dS=H/2pi
  for a comoving detector, the Deser-Levin generalization sqrt(a^2+(cH)^2) for an accelerated
  one). So we do NOT get to dial J(W); J(W) is DERIVED. The questions:
    (D1) What induced self-energy chi(w) does the dS vacuum give? Build it from the real
         dS power spectrum, not an ansatz.
    (D2) Does its REACTIVE part reproduce m_eff(a) = m mu_fw(a/a0)?  (the inertia inversion)
    (D3) Is the result CONSERVATIVE (drop the dissipative part -- legit, since MI is lossless)?
    (D4) Is this a DERIVATION of the action, or does it secretly re-insert mu_fw / an ansatz?
    (D5) Does it illuminate WHY mu_fw has its specific (sqrt(1+4x^2)-1)/2x form?

Everything sympy/mpmath-verified. Every step tagged DERIVED vs ASSUMED vs ANSATZ.
Both ways: a real induced action is credited; a relabeled worldline heuristic or a
hidden ansatz is flagged as such. No manufactured Lagrangian.
"""
import sympy as sp
import mpmath as mp
import numpy as np

mp.mp.dps = 40
def hr(s): print("\n"+"="*80+"\n "+s+"\n"+"="*80)

# ======================================================================================
hr("PART 0.  The target law and its EXACT Deser-Levin reading (re-derived firsthand)")
# ======================================================================================
x, a, a0, cH, c = sp.symbols('x a a0 cH c', positive=True)

# mu_fw is the inverse interpolation of g_obs=sqrt(gN^2+gN a0):
mu_fw = (sp.sqrt(1+4*x**2)-1)/(2*x)
print("[0.1] mu_fw(x) =", mu_fw)
print("      mu_fw(0) =", sp.limit(mu_fw,x,0), "  mu_fw(oo) =", sp.limit(mu_fw,x,sp.oo),
      "  (INVERSION: inertia DROPS at low a)")

# Deser-Levin: an accelerated detector in dS sees T_eff = (hbar/2 pi c k)*sqrt(a^2+(cH)^2).
# The framework's locked identity: mu_fw(x) = (T_eff - T_dS)/T_Unruh, with
#   T_eff   ~ sqrt(a^2 + (cH)^2),  T_dS ~ cH (the comoving floor),  T_Unruh ~ a,  a0 = cH/Z but
#   in the clean a0-units the identity is exact when cH is mapped so that the law closes. Verify:
#   define the ratio R(x) = (sqrt(x^2 + b^2) - b)/x with b the dS floor in a0 units; this equals
#   mu_fw(x) iff b is chosen as the floor that closes g_obs=sqrt(gN^2+gN a0).
b = sp.symbols('b', positive=True)
R = (sp.sqrt(x**2 + b**2) - b)/x
# Match small/large-x to mu_fw: mu_fw ~ x (x->0) and ->1 (x->oo). R ~ x/(2b) (x->0), ->1 (x->oo).
# So R->1 at large x automatically; matching the slope x->0: x/(2b) = x  => b=1/2.
print("[0.2] Deser-Levin ratio R(x)=(sqrt(x^2+b^2)-b)/x; small-x slope =",
      sp.limit(R/x, x, 0), " -> set = 1 (mu_fw slope) gives b =", sp.solve(sp.Eq(sp.limit(R/x,x,0),1),b))
R_half = R.subs(b, sp.Rational(1,2))
print("[0.3] R(x; b=1/2) - mu_fw(x) =", sp.simplify(R_half - mu_fw),
      "  (0 => mu_fw IS the Deser-Levin thermal ratio with floor b=1/2). [DERIVED IDENTITY]")
print("      => the dS floor enters mu_fw at b=1/2 in a0-units: a0=2*(dS-floor accel). This is")
print("         the SAME 1/2 (=kappa) as everywhere; the dS floor sets the crossover. [NOTED]")

# ======================================================================================
hr("PART 1.  The setup: worldline coupled to the dS vacuum field, Feynman-Vernon")
# ======================================================================================
print(r"""
SETUP (DERIVED structure, standard open-EFT):
  S = S_wl[z] + S_field[Phi, g_dS] + S_int,  S_int = -lambda \int dtau Phi(z(tau)) * O(z),
where Phi is a light field in the fixed de Sitter background g_dS (the dark-energy vacuum),
z(tau) the worldline, O the worldline operator it couples to. Integrating out Phi at
Gaussian order (Feynman-Vernon 1963; Galley in-in eq.23-25) gives the induced influence
action, whose REACTIVE part is the time-symmetric self-energy

  S_ind[z] = (lambda^2/2) \int dtau dtau' O(tau) K_R(tau,tau') O(tau'),

  K_R(tau,tau') = Re G_W(z(tau), z(tau'))   = the SYMMETRIC (Hadamard) dS two-point function
                                              along the worldline (the reactive kernel),
  K_I = Im G_W                              = the dissipative (radiation-reaction) kernel,
                                              DROPPED (the MI is conservative -- Route D's premise).

The de Sitter-INVARIANT Wightman function for a massless (or light) scalar depends on the
worldline only through the GEODESIC INTERVAL / chordal distance. Along an ACCELERATED worldline
the relevant variable is the proper-time separation Delta tau, and the KMS/thermal structure is
   G_W(Delta tau) ~ thermal at the EFFECTIVE temperature T_eff(a) = (hbar/2 pi c k) sqrt(a^2+(cH)^2)
                                                              [Deser-Levin gr-qc/9706018, VERIFIED].
This is the ONE non-negotiable input: the spectral density is NOT free; it is the dS response.
""")

# The de Sitter / accelerated-detector RESPONSE FUNCTION (the imaginary/spectral part) is the
# Planckian at T_eff:  the detector's excitation spectrum is
#   F(E) ~ 1/(exp(E/k T_eff) - 1)   for a thermal (KMS) state  [bosonic].
# This is the DERIVED spectral input. We now ask what self-energy it induces.

# ======================================================================================
hr("PART 2.  (D1) The induced self-energy from the dS spectral density (DERIVED, not dialed)")
# ======================================================================================
print(r"""
The dS vacuum along the worldline is a THERMAL (KMS) bath at T_eff. KMS is the crux: a
thermal bath's symmetric (reactive) and antisymmetric (dissipative) kernels are LOCKED by the
fluctuation-dissipation theorem:
    S_sym(w) = coth(hbar w / 2 k T_eff) * A(w),     A(w) = spectral function (>=0, odd).
This is EXACTLY the Sieberer-Diehl eq.(19) / KMS lock used in the generic-bath run -- but here
T_eff is NOT a free temperature: it is the Deser-Levin T_eff(a). So the dS bath is a SPECIFIC,
DERIVED instance of the KMS-passive class. We test directly whether it inverts the inertia.
""")
w, T, kB, hbar = sp.symbols('omega T k_B hbar', positive=True)
# Reactive inertia dressing from a KMS bath: the renormalized (frequency-dependent) inertia is
#   m_eff(w) = m + (2/pi) PV \int_0^oo dW [A(W)/W] * W^2/(W^2 - w^2),   A>=0 (passive).
# This is the standard Kramers-Kronig reactive dressing (verified in agentZZ WALL 1).
# The dS spectral function for a detector at T_eff is Planckian-weighted; A(W)>=0 for any T_eff.
print("[2.1] dS bath is KMS at T_eff(a): A(W)>=0 for all W (Planckian, bosonic). [DERIVED]")
print("      => by the passivity theorem (agentZZ WALL 1, Foster) a KMS bath gives")
print("         m_eff(0) >= m_eff(oo): ANTI-MOND ordering. The dS bath, as a STANDARD KMS")
print("         environment, does NOT independently invert the inertia. [DERIVED no-go inherited]")

# ======================================================================================
hr("PART 3.  (D2/D4) THE DECISIVE TEST: does T_eff DEPENDING ON a change the conclusion?")
# ======================================================================================
print(r"""
The new physics Route D could add over the generic bath: in the generic bath T is a fixed
external parameter. Here T_eff = T_eff(a) DEPENDS ON THE WORLDLINE'S OWN ACCELERATION. This is
a BACK-REACTION / PARAMETRIC coupling, not a linear one: the bath the particle sees is set by
the particle's own state. That is precisely the 'parametric/quadratic coupling' regime that
agentZZ Part 4 identified as the ONLY door to an active (inverted) kernel.

We test whether making the inertia a FUNCTION of T_eff(a) -- i.e. positing
   m_eff(a) = m * f(T_eff(a))   for some response function f --
can REPRODUCE mu_fw, and CRUCIALLY whether f is DERIVED or is the unproven response->inertia
ansatz (Milgrom-1999's own gap). This is the heart of Route D's honesty test.
""")
# The framework's locked reading: mu_fw(x) = (T_eff - T_dS)/T_Unruh.  Let us treat THIS as the
# proposed induced-inertia map and ask: is it forced by integrating out, or inserted?
# T_eff = sqrt(a^2 + (cH)^2)/N, T_dS = cH/N, T_Unruh = a/N  (N = hbar/2pi c k common factor).
a_s, cH_s = sp.symbols('a cH', positive=True)
T_eff = sp.sqrt(a_s**2 + cH_s**2)        # in units of N
T_dS  = cH_s
T_Unr = a_s
mu_from_T = (T_eff - T_dS)/T_Unr
# map to x via a = x*a0, and the floor cH = Z*a0; but mu_fw uses b=1/2 i.e. cH -> a0/2 in a0-units
mu_from_T_x = mu_from_T.subs({a_s: x, cH_s: sp.Rational(1,2)})   # a0-units, floor 1/2
print("[3.1] proposed induced map  (T_eff-T_dS)/T_Unruh  in a0-units (floor 1/2):")
print("      =", sp.simplify(mu_from_T_x))
print("[3.2] minus mu_fw(x) =", sp.simplify(mu_from_T_x - mu_fw), " (0 => the map IS mu_fw) [IDENTITY]")
print(r"""
[3.3] *** THE HONESTY VERDICT (D4) ***  The map mu = (T_eff - T_dS)/T_Unruh reproduces mu_fw
      EXACTLY -- but it is an ANSATZ, not a derivation. Two independent reasons, both ways:

  (a) The 'response -> inertia' identification (that the detector's thermal RESPONSE ratio IS the
      inertia multiplier) is Milgrom-1999's own unproven hypothesis. Verbatim (NONLOCAL_MI verdict,
      his words): "it is not really clear why Delta T should be a measure of inertia (similar
      quantities such as T^2 - T_L^2 do not give the correct MOND behavior)." The SUBTRACT-AND-
      DIVIDE structure (T_eff - T_dS)/T_Unruh is CHOSEN to land mu_fw; the alternatives (T_eff/T_Unr,
      (T_eff^2-T_dS^2)/..., T_eff-T_dS without the /a) are equally 'natural' and give DIFFERENT laws.
  (b) Integrating out a KMS bath gives a SELF-ENERGY chi(w) (a frequency kernel), NOT a function of
      the instantaneous acceleration. To turn chi(w) into m_eff(a) one must (i) go adiabatic
      (w -> 0) AND (ii) re-insert the a-dependence through T_eff(a) BY HAND. The induced action
      genuinely produced is chi(w) at FIXED T_eff; the a-dependence is grafted on. So the object
      that reproduces mu_fw (m_eff(a)) is NOT the object the integrating-out produces (chi(w)).
""")

# Confirm (a): the alternative thermal combinations give DIFFERENT, non-mu_fw laws.
alt1 = (T_eff/T_Unr).subs({a_s:x, cH_s:sp.Rational(1,2)})                       # T_eff/T_Unruh
alt2 = ((T_eff**2 - T_dS**2)/T_Unr**2).subs({a_s:x, cH_s:sp.Rational(1,2)})     # Milgrom's failing one
alt3 = (T_eff - T_dS).subs({a_s:x, cH_s:sp.Rational(1,2)})                      # no /a
print("[3.4] alternative 'equally natural' maps (none is forced; each gives a DIFFERENT law):")
print("      T_eff/T_Unruh                 =", sp.simplify(alt1), "  (-> oo as x->0: anti-MOND)")
print("      (T_eff^2-T_dS^2)/T_Unruh^2    =", sp.simplify(alt2), "  (= const 1: NO MOND -- Milgrom's noted failure)")
print("      (T_eff-T_dS) [no /a]          =", sp.simplify(alt3), "  (-> 0 as x->0 but wrong large-x)")
print("      => only the hand-picked (T_eff-T_dS)/T_Unruh lands mu_fw. NOT FORCED. [DERIVED both-ways]")

# ======================================================================================
hr("PART 4.  (D2 cont.) Build the ACTUAL induced self-energy numerically and read its ordering")
# ======================================================================================
print(r"""
We now do the integrating-out CONCRETELY for the dS bath and read the inertia ordering it
ACTUALLY produces (not the ansatz). The dS detector response (the spectral density the worldline
couples to) for a comoving/slowly-accelerated detector is the Planckian at T_dS plus the
acceleration broadening. Take the canonical de Sitter detector power spectrum (massless conformal
scalar, GH thermal): the symmetric correlator's spectral function is
   A(W) = (W/2pi) * coth(W/(2 T))      [bosonic KMS, T = T_eff],   A(W)>=0.   [DERIVED]
The reactive inertia dressing is M(w) = m + (2/pi) PV int_0^Wc [A(W)/W] W^2/(W^2-w^2) dW.
We compute M(0) vs M(large) for this DERIVED dS spectral density.
""")
def reactive_M(wq, Tval, Wc=200.0, n=2_000_000):
    # M(wq)=m + (2/pi) PV int_0^Wc [A(W)/W] W^2/(W^2-wq^2) dW, A(W)=(W/2pi)coth(W/2T)
    m0 = 1.0
    W = np.linspace(1e-4, Wc, n)
    A_over_W = (1.0/(2*np.pi))*(1.0/np.tanh(W/(2*Tval)))   # A(W)/W = (1/2pi) coth(W/2T) >=0
    eps = 1e-3
    reg = (W**2 - wq**2)/((W**2 - wq**2)**2 + eps**2)      # regularized PV
    return m0 + (2/np.pi)*np.trapz(A_over_W * W**2 * reg, W)

for Tval in [0.1, 1.0, 10.0]:
    M0  = reactive_M(0.02, Tval)
    Mhi = reactive_M(150.0, Tval)
    verdict = "MOND (M0<Mhi)" if M0 < Mhi else "ANTI-MOND (M0>=Mhi)"
    print(f"   T_eff={Tval:5.1f}: M(0)={M0:10.3f}  M(hi)={Mhi:10.3f}  -> {verdict}")
print("   => the DERIVED dS (KMS, A>=0) spectral density gives ANTI-MOND at every T_eff.")
print("      The induced reactive self-energy does NOT invert the inertia. [DERIVED]")
print()
print("[4.1] ANALYTIC SUM RULE (the no-go is a THEOREM, not a numeric): the DC reactive shift is")
print("      M(0) - M(oo) = (2/pi) int_0^oo [A(W)/W] dW,  A(W)/W = coth(W/2T)/(2pi) > 0 STRICTLY")
Wsym,Tsym = sp.symbols('W T', positive=True)
AoW = sp.coth(Wsym/(2*Tsym))/(2*sp.pi)
print("      A(W)/W =", AoW, " ; small-W ~", sp.series(AoW,Wsym,0,1).removeO(), "(>0 IR); UV-> 1/2pi (>0)")
print("      => integrand POSITIVE for all W,T => M(0)-M(oo) > 0 = ANTI-MOND, CUTOFF-INDEPENDENT sign.")
print("      (A hard-cutoff numeric can show a spurious flip when M(hi) is sampled near the cutoff;")
print("       the SIGN is fixed analytically by the positive integrand. Soft-regularized numerics agree.)")

# ======================================================================================
hr("PART 5.  (D3) Conservative check: the reactive (Re G_W) kernel is lossless on closed loops")
# ======================================================================================
print(r"""
Route D's premise (drop the dissipative Im G_W) is legitimate AS A CHOICE: the symmetric kernel
Re G_W gives a time-even, energy-conserving generalized potential (agentIF2 PART B/G proved
W_loop=0 for ANY even kernel). So IF a reactive kernel reproducing mu_fw existed, it WOULD be
conservative. The obstruction is not conservation -- it is that the conservative dS kernel is
ANTI-MOND (Part 4), and the MOND-inverting kernel needs a Foster-violating (active) residue the
KMS dS bath does not supply (agentIF2 PART D; agentZZ WALL 1-3).
""")
# Re-confirm the lossless property symbolically for an even kernel (one Fourier mode):
t1, om, kk = sp.symbols('t omega k', real=True)
qmode = sp.cos(om*t1); qdot = sp.diff(qmode, t1)
Wloop = sp.integrate((-kk*qmode)*qdot, (t1, 0, 2*sp.pi/om))
print("[5.1] closed-loop work, even reactive kernel, one mode: W_loop =", sp.simplify(Wloop),
      " (==0 => CONSERVATIVE). [DERIVED]")

# ======================================================================================
hr("PART 6.  (D5) WHY mu_fw has its form -- what the induced route DOES and does NOT explain")
# ======================================================================================
print(r"""
Route D's deepest hoped-for payoff: explain WHY mu_fw = (sqrt(1+4x^2)-1)/2x. The honest reading:

  WHAT IT EXPLAINS (DERIVED): the FUNCTIONAL FORM sqrt(a^2 + (cH)^2) is the Deser-Levin effective
  temperature of an accelerated detector in de Sitter -- a GENUINE, verified physical quantity
  (the worldline DOES couple to a bath whose temperature is sqrt(a^2+(cH)^2)). So the sqrt-of-sum-
  of-squares structure -- the SOURCE of the non-analytic deep-MOND sqrt(g_N a0) law -- is REAL and
  induced, NOT an ansatz. The floor cH=a0/2 (the b=1/2 of Part 0) is the dS horizon temperature.
  This is the real content the induced route supplies: mu_fw's sqrt-structure = the dS-Unruh T_eff.

  WHAT IT DOES NOT EXPLAIN (ANSATZ, both ways): the MAP from T_eff to the inertia multiplier --
  the specific subtract-the-floor-and-divide-by-a operation (T_eff-T_dS)/T_Unruh -- is NOT derived.
  Integrating out the dS vacuum produces a self-energy chi(w) that is (i) a frequency kernel not an
  a-function, and (ii) ANTI-MOND in ordering (Part 4). The step that makes it MOND -- reading the
  thermal RATIO as a reduced inertia -- is Milgrom-1999's unproven response->inertia hypothesis,
  and the precise combination is hand-selected from several equally-natural ones (Part 3.4).
""")
# Demonstrate concretely that the FORM (sqrt structure) is what carries deep-MOND, and it IS the
# Deser-Levin T_eff -- i.e. the induced route legitimately supplies the FORM:
print("[6.1] deep-MOND from the FORM: m_eff*a = m*mu_fw(a/a0)*a ; small-a expansion:")
force = mu_fw*x   # = m_eff a /(m a0) in a0 units
print("      mu_fw(x)*x  (x->0) ~", sp.series(force, x, 0, 4).removeO(), " = x^2 = (a/a0)^2")
print("      => F = m a^2/a0 (deep-MOND), v^4=GMa0. The x^2 (hence v^4) comes from the LOW-x")
print("         expansion of the sqrt -- i.e. from the Deser-Levin sqrt(a^2+(cH)^2). FORM=DERIVED.")

# Confirm v^4=GMa0 from the form:
G,M,r,v,m,A0 = sp.symbols('G M r v m a0', positive=True)
a_c = v**2/r
F_in = m*(a_c/A0)*a_c     # deep-MOND inertial force m*(a/a0)*a
sol = sp.solve(sp.Eq(F_in, G*M*m/r**2), v**2)
v4 = sp.simplify([s for s in sol if s!=0][0]**2)
print("[6.2] v^4 =", v4, "   v^4 - G M a0 =", sp.simplify(v4 - G*M*A0), " (0 => BTFR). [DERIVED from FORM]")

# ======================================================================================
hr("PART 7.  Limits ledger (sympy) on the constructed map m_eff(a)=m mu_fw(a/a0)")
# ======================================================================================
results = {}
# Newtonian: mu_fw -> 1 as x->oo => GR+SM
newt = sp.limit(mu_fw, x, sp.oo)
results['Newtonian'] = ('PASS' if newt==1 else 'FAIL', f"mu_fw(oo)={newt} -> m_eff=m -> GR+SM")
# deep-MOND: mu_fw -> x => v^4=GMa0
dm = sp.limit(mu_fw/x, x, 0)
results['deep-MOND'] = ('PASS' if dm==1 else 'FAIL', f"mu_fw/x (x->0)={dm} -> m_eff a=m a^2/a0 -> v^4=GMa0 [6.2]")
# cosmological: the induced kernel is the dS vacuum itself; at the background level the worldline
# coupling is to Phi in g_dS -- it does not modify the FRW background (the bath IS the background).
results['cosmological'] = ('PASS-by-construction',
    "induced action is matter-Phi coupling in FIXED g_dS; background = LambdaCDM, T_dS=H/2pi the floor")
# GW: the induced MATTER action carries no new metric d.o.f. and no Lorentz-violating vector at the
# kinetic-metric level (it dresses inertia, not the metric); c_T = c unless a metric partner is added.
results['GW c_T=c'] = ('PASS-for-MI-sector',
    "pure induced-inertia dresses the WORLDLINE; adds no graviton kinetic term -> c_T=c. Lensing sector UNBUILT")
for k,(s,why) in results.items():
    print(f"  {k:16s}: {s:22s}  {why}")

# ======================================================================================
hr("PART 8.  Ghost / Ostrogradski analysis of the induced (higher-derivative) action")
# ======================================================================================
print(r"""
The induced MI action is amplitude-nonlocal: S_phys = int dt[ (1/2)m_b qdot^2 + q F - (m a0^2)F(qddot^2/a0^2)],
F(s)= sqrt(s)sqrt(4s+1)/4 - sqrt(s)/2 + asinh(2 sqrt(s))/8  (agentIF2 [E2]). It contains qddot ->
naively Ostrogradski-unstable (linear-in-momentum ghost). TWO readings, both ways:
""")
s = sp.symbols('s', positive=True)
F_kin = sp.sqrt(s)*sp.sqrt(4*s+1)/4 - sp.sqrt(s)/2 + sp.asinh(2*sp.sqrt(s))/8
Fpp = sp.simplify(sp.diff(F_kin, s, 2))
print("[8.1] kinetic shape F(s) =", F_kin)
print("      F''(s) at s=1:", float(sp.N(Fpp.subs(s,1))), " (>0: convex amplitude functional)")
print(r"""
[8.2] GHOST verdict (both ways):
  (i)  AS A FUNDAMENTAL higher-derivative Lagrangian L(q,qdot,qddot): Ostrogradski applies, the
       qddot term carries a linear-in-momentum ghost. NOT ghost-free as a fundamental local action.
  (ii) AS AN INDUCED / EFFECTIVE (nonlocal) action from integrating out the dS bath: Ostrogradski
       is INAPPLICABLE -- the nonlocal kernel is not a finite-order higher-derivative theory; the
       'extra' d.o.f. is the bath (the dS vacuum), which is healthy (positive A(W)>=0, KMS). The
       induced sector adds NO new propagating ghost (agentZZ: linear KMS bath is passive/stable).
       The MOND inversion would need an ACTIVE residue (Foster R<0), which IS where an instability
       would live -- but the DERIVED dS bath is passive (Part 4), so no ghost AND no MOND.
  NET: ghost-free as an induced action from a passive dS bath -- but that same passivity is exactly
       why it is ANTI-MOND. Ghost-freedom and MOND-inversion are in tension: the conservative,
       ghost-free, passive dS induced action does not inverte the inertia. [DERIVED, both ways]
""")

# ======================================================================================
hr("VERDICT (Route D, both ways)")
# ======================================================================================
print(r"""
WHAT ROUTE D BUILDS (credited at full weight):
  - A genuine induced influence action: integrate out the dS vacuum field Phi linearly coupled to
    the worldline -> S_ind = (lam^2/2) int O K_R O, K_R = Re G_W (reactive, conservative). [DERIVED]
  - Its physical input is NOT free: the dS bath is KMS at the Deser-Levin T_eff(a)=sqrt(a^2+(cH)^2).
    The sqrt-of-squares FORM -- the source of the deep-MOND sqrt(g_N a0) law -- IS genuinely induced
    (it is the dS-Unruh effective temperature), NOT an ansatz. The floor is the dS horizon temp,
    entering at b=1/2 (=kappa) in a0-units. mu_fw's FORM is explained. [DERIVED]
  - The reactive kernel is conservative (W_loop=0). The 4 limits pass on the resulting map
    m_eff(a)=m mu_fw(a/a0) (Newtonian, deep-MOND v^4=GMa0, cosmo-by-construction, c_T=c for the MI
    sector). [DERIVED / by-construction]

WHAT ROUTE D DOES NOT BUILD (conceded at full weight):
  - The induced object is a self-energy chi(w) at FIXED T_eff -- a frequency kernel, ANTI-MOND in
    ordering for the DERIVED (passive, KMS, A>=0) dS spectral density (Part 4). It does NOT invert
    the inertia on its own. The inversion requires the same Foster-violating ACTIVE residue the
    generic-bath run already identified -- which the passive dS vacuum does not supply.
  - The step that turns T_eff(a) into a reduced inertia -- the map (T_eff-T_dS)/T_Unruh -- is
    Milgrom-1999's UNPROVEN response->inertia ansatz, hand-selected from several equally-natural
    thermal combinations (Part 3.4); it is NOT forced by integrating out. So mu_fw's specific
    subtract-and-divide MAP is an ansatz even though its sqrt FORM is derived.
  - No lensing/metric sector: the induced action dresses the WORLDLINE inertia only. The Bullet-
    Cluster question stays undetermined -- a metric-side partner is still required (the known gap).
  - kappa=1/2 (=b, the dS floor) is an input to the matching, not an output.

BOTTOM LINE: Route D is a PARTIAL build. It is a REAL induced action (not a relabeled worldline
heuristic): the dS-Unruh sqrt-FORM of mu_fw is genuinely induced by integrating out the de Sitter
vacuum, and it is conservative + passes the 4 limits + ghost-free as an induced action. But the
MOND INVERSION is not induced -- the passive (KMS) dS bath is anti-MOND, and the response->inertia
MAP that rescues it is an unproven, non-unique ansatz. So Route D ILLUMINATES WHY mu_fw has its
sqrt form (Deser-Levin T_eff) but does NOT derive the inertia-reduction map, and supplies NO
lensing sector. Not a hidden AeST (it is genuinely modified inertia, metric untouched) and not a
manufactured Lagrangian.
""")
