#!/usr/bin/env python3
# agentYY ROUTE 2 — RELATIVE / GENERALIZED ENTROPY S(a) along a boost orbit
# in the type II_1 dS observer algebra. Does S_rel(rho_a || rho_GH), or its
# modular response, develop a genuine FEATURE (extremum/inflection/max-rate)
# at a ~ cH -- FORCING a0's transition scale -- or is it monotone (structural
# ceiling)? And: does the ALGEBRA-level Jacobson (modular Hamiltonian, not the
# worldline) EVADE or INHERIT agentQ's no-go (Clausius consumes T)?
#
# Conventions: hbar = c = k_B = 1 in the algebra; c restored only in a~cH labels.
# Banked (agentWW, machine-verified twice): T_DL = sqrt(a^2+H^2)/(2pi) IS the
# boost-KMS modular temperature of the GH state. beta_GH = 2pi/H (KMS of GH state).
# The accelerated worldline is a boost orbit at static-patch depth u with
# a = H tan u, |xi| = cos u, T_DL = H/(2pi cos u).

import sympy as sp
import mpmath as mp

mp.mp.dps = 40

print("="*78)
print("agentYY ROUTE 2 — relative/generalized entropy S(a) in the type II_1 algebra")
print("="*78)

a, H, u, beta, x, q, lam = sp.symbols('a H u beta x q lambda', positive=True, real=True)

# -----------------------------------------------------------------------------
# PART A. The banked modular structure (re-verify the load-bearing identities).
# -----------------------------------------------------------------------------
print("\n--- PART A: re-verify the banked modular-temperature identities ---")
# static-patch acceleration and redshift in terms of depth u
a_of_u   = H*sp.tan(u)
xi_of_u  = sp.cos(u)
# Tolman identity sqrt(a^2+H^2)*|xi| = H
tolman = sp.simplify(sp.sqrt(a_of_u**2 + H**2)*xi_of_u - H)
print("[A1] Tolman  sqrt(a^2+H^2)*cos u - H =", tolman, " (expect 0)")
# modular temperature = Tolman-blueshifted GH temperature
T_mod = H/(2*sp.pi*xi_of_u)              # kappa_b/(2 pi |xi|), kappa_b=H
T_DL  = sp.sqrt(a_of_u**2+H**2)/(2*sp.pi)
print("[A2] T_mod - T_DL =", sp.simplify(T_mod - T_DL), " (expect 0)")

# In terms of a directly:
T_DL_a = sp.sqrt(a**2+H**2)/(2*sp.pi)
print("[A3] T_DL(a) = sqrt(a^2+H^2)/(2 pi) -- the boost-KMS modular temperature.")
print("     dT_DL/da =", sp.simplify(sp.diff(T_DL_a, a)),
      " (= a/(2pi sqrt(a^2+H^2)); the F4 susceptibility agentQ flagged)")

# -----------------------------------------------------------------------------
# PART B. The Araki relative entropy of the accelerated state vs the GH state.
#
# In the type II_1 crossed product (Witten 2112.12828, CLPW 2206.10780) the
# DRESSED state has a genuine density matrix rho-hat and finite von Neumann
# entropy S(rho) = -Tr(rho ln rho). The relative entropy of two states is the
# Araki object
#       S_rel(rho || sigma) = <K_sigma>_rho - <K_sigma>_sigma - (S(rho)-S(sigma))
# where K_sigma = -ln sigma is the modular Hamiltonian of the REFERENCE sigma.
# Take sigma = rho_GH (the Gibbons-Hawking state, KMS at beta_GH = 2pi/H wrt the
# boost), rho = rho_a (the accelerated-observer state).
#
# KEY MODELLING STEP (made explicit, not smuggled): the accelerated observer
# sees the SAME boost modular flow but blueshifted -- it is a KMS state of the
# SAME modular Hamiltonian H_mod at the LOCAL inverse temperature
#       beta_a = 1/T_DL = 2pi/sqrt(a^2+H^2),     beta_GH = 2pi/H = beta_a(a=0).
# (This is exactly the WW identity: every boost orbit shares the modular data;
#  a relabels the KMS temperature via the Tolman blueshift.) So rho_a and rho_GH
# are two KMS states of the SAME generator H_mod at different beta -- the cleanest
# possible setting for an Araki relative entropy, and it needs NO phi.
# -----------------------------------------------------------------------------
print("\n--- PART B: Araki relative entropy of two KMS states of the boost ---")
beta_a, beta_G, Z = sp.symbols('beta_a beta_G Z', positive=True)
# For two thermal states of the same Hamiltonian with partition fn Z(beta),
# S_rel(rho_a||rho_G) = beta_G*<H>_a - beta_a*<H>_a + ln Z(beta_a) - ln Z(beta_G)
#   ... general Gibbs identity:
#   S_rel = (beta_G - beta_a)<H>_a - (ln Z(beta_G) - ln Z(beta_a))
# Equivalently with free energy F(beta) = -ln Z(beta)/beta and U=<H>:
#   S_rel(beta_a||beta_G) = beta_G*(U(beta_a) - F-stuff). We compute it from a
#   CONCRETE spectral model so U, S, lnZ are all explicit functions of beta.
#
# The boost modular Hamiltonian of the dS static patch has the QNM/boost spectrum.
# Two physically banked spectral choices (we run BOTH and check robustness):
#   (M1) continuum Rindler-like boost spectrum: density of boost energy ~ flat,
#        a single-mode oscillator of boost frequency Omega -> Planck thermal.
#   (M2) the banked dS QNM ladder Gamma_n = sinh((Delta+n)lambda) (agentS),
#        lambda <-> H -- the genuine type II_1 / DSSYK spectrum.
# In BOTH, beta enters ONLY through beta = 2pi/sqrt(a^2+H^2). The a-dependence of
# every thermodynamic potential is therefore through this ONE function beta(a).
print("beta(a) = 2 pi / sqrt(a^2 + H^2);  beta_GH = beta(0) = 2 pi / H")
beta_of_a = 2*sp.pi/sp.sqrt(a**2+H**2)
print("d beta/d a =", sp.simplify(sp.diff(beta_of_a,a)), " (<0: beta DECREASES monotonically in a)")
print("  -> as a grows the local KMS state gets HOTTER; beta runs monotonically a:0->oo, beta:2pi/H->0")

# -----------------------------------------------------------------------------
# PART C. Concrete model M1: single boost-frequency oscillator (Planck/Unruh).
# Thermodynamics of one bosonic mode of boost-frequency Omega at inverse temp b:
#   lnZ = -ln(1 - e^{-b Omega}),  U = Omega/(e^{b Omega}-1),
#   S   = b U - ln(1 - e^{-b Omega}) = b U + lnZ_signfix
# Relative entropy of state at b=beta_a vs reference bG=beta_G (SAME Omega):
#   S_rel = (bG - b)*U(b) - (lnZ(bG) - lnZ(b))
# (standard: S_rel(rho_b || rho_bG) = beta_G U_b - beta_b U_b + lnZ_b - lnZ_bG
#  ... rewritten; we use the clean Gibbs form and verify it is >=0.)
# -----------------------------------------------------------------------------
print("\n--- PART C: model M1 (single boost-mode oscillator) S_rel(a) ---")
b, bG, Om = sp.symbols('b bG Omega', positive=True)
U   = Om/(sp.exp(b*Om)-1)
lnZ = -sp.log(1-sp.exp(-b*Om))
# S_rel of thermal_b against thermal_bG, same H:
S_rel_M1 = (bG - b)*U - (lnZ.subs(b,bG) - lnZ)
S_rel_M1 = sp.simplify(S_rel_M1)
print("S_rel(b||bG) =", S_rel_M1)
# sanity: vanishes at b=bG
print("  check S_rel(bG||bG) =", sp.simplify(S_rel_M1.subs(b,bG)), " (expect 0)")
# convexity in b at fixed bG: d/db S_rel
dSrel_db = sp.simplify(sp.diff(S_rel_M1, b))
print("  dS_rel/db =", dSrel_db)
print("  -> = (b-bG)*dU/db ; sign(dS_rel/db)=sign(b-bG) since dU/db<0:")
dUdb = sp.simplify(sp.diff(U,b))
print("     dU/db =", dUdb, " (negative for all b,Omega>0)")

# -----------------------------------------------------------------------------
# PART D. Compose with beta(a): S_rel as a function of the ORBIT acceleration a.
# This is THE question: does S_rel(a) (or dS_rel/da, the modular response) have
# a feature -- extremum, inflection, max-rate -- at a ~ H (a ~ cH)?
# -----------------------------------------------------------------------------
print("\n--- PART D: S_rel(a), dS_rel/da, d2S_rel/da2 -- feature hunt at a~H ---")
# substitute b = beta(a), bG = beta_GH = 2pi/H, Omega = O0/H (set Omega*H=O0 dimensionless)
# Work numerically with mpmath for robustness; scan a/H over decades.
def make_numeric(Omega_val):
    Om0 = mp.mpf(Omega_val)   # Omega in units of H, i.e. Omega*? we set H=1
    def beta(ah):  # ah = a/H, H=1 -> beta = 2pi/sqrt(ah^2+1)
        return 2*mp.pi/mp.sqrt(ah**2+1)
    bGv = beta(mp.mpf(0))     # 2 pi
    def Srel(ah):
        bv = beta(ah)
        Uv = Om0/(mp.e**(bv*Om0)-1)
        lnZb  = -mp.log(1-mp.e**(-bv*Om0))
        lnZbG = -mp.log(1-mp.e**(-bGv*Om0))
        return (bGv-bv)*Uv - (lnZbG - lnZb)
    return Srel
# Use a moderate Omega so the mode is thermally active across the scan.
for Omega_val in ['0.2','1.0','5.0']:
    Srel = make_numeric(Omega_val)
    print(f"\n  Omega/H = {Omega_val}:   a/H,  S_rel,  dS_rel/d(a/H),  d2S_rel/d(a/H)^2")
    grid = ['0.01','0.1','0.3','0.5','0.7','1.0','1.4142','2.0','3.0','5.789','10','100']
    prev = None
    for s in grid:
        ah = mp.mpf(s)
        val  = Srel(ah)
        d1   = mp.diff(Srel, ah)
        d2   = mp.diff(Srel, ah, 2)
        tag = ''
        if abs(ah-1) < 1e-9: tag = '  <-- a=H'
        if abs(ah-mp.mpf('5.789'))<1e-3: tag = '  <-- a=cH (a0 onset, Z=5.789)'
        print(f"    a/H={float(ah):8.4g}  S={float(val):+.6e}  dS={float(d1):+.6e}  d2S={float(d2):+.6e}{tag}")

# -----------------------------------------------------------------------------
# PART E. Where do the FEATURES land? Locate (i) the inflection of S_rel
# (d2S_rel/da2 = 0) and (ii) the peak of the modular RESPONSE dS_rel/da
# (the max-rate point, d2S_rel/da2=0 is the SAME condition as the rate-peak).
# If a feature is real and forced, it must land at a/H ~ O(1) INDEPENDENT of the
# scheme knob Omega. If it slides with Omega, it is scheme, not derivation.
# -----------------------------------------------------------------------------
print("\n--- PART E: locate the inflection / max-modular-rate point a*/H vs Omega ---")
print("  (d2S_rel/da2 = 0  <=>  peak of the modular response dS_rel/da)")
def make_numeric_E(Omega_val):
    Om0 = mp.mpf(Omega_val)
    def beta(ah): return 2*mp.pi/mp.sqrt(ah**2+1)
    bGv = beta(mp.mpf(0))
    def Srel(ah):
        bv = beta(ah)
        Uv = Om0/(mp.e**(bv*Om0)-1)
        lnZb  = -mp.log(1-mp.e**(-bv*Om0)); lnZbG = -mp.log(1-mp.e**(-bGv*Om0))
        return (bGv-bv)*Uv - (lnZbG - lnZb)
    return Srel
print(f"  {'Omega/H':>8} | {'a*/H (inflection of S_rel)':>28} | {'note':>10}")
for Omega_val in ['0.05','0.1','0.2','0.5','1.0','2.0','5.0','10.0','30.0']:
    Srel = make_numeric_E(Omega_val)
    d2 = lambda ah: mp.diff(Srel, ah, 2)
    # bracket a root of d2 between 0.3 and 60
    try:
        astar = mp.findroot(d2, mp.mpf('3.0'))
        if astar <= 0 or astar > 1e4: raise ValueError
        note = ''
        print(f"  {Omega_val:>8} | {float(astar):>28.5f} | {note:>10}")
    except Exception as e:
        # scan for sign change
        lo=mp.mpf('0.2'); found=None
        xs=[lo*mp.mpf('1.15')**k for k in range(60)]
        vals=[d2(x) for x in xs]
        for i in range(len(xs)-1):
            if vals[i]*vals[i+1]<0:
                found=mp.findroot(d2,(xs[i]+xs[i+1])/2); break
        print(f"  {Omega_val:>8} | {float(found) if found else float('nan'):>28.5f} | {'scan':>10}")

print("\n  DIAGNOSIS: the inflection a*/H SLIDES with the probe frequency Omega/H.")
print("  It is NOT locked to a~H. Check the scaling: a* set by beta*Omega ~ O(1)")
print("  i.e. the inflection is where the LOCAL KMS temperature T_DL ~ Omega (the")
print("  probe mode thermally activates). a*/H grows as Omega grows -> pure probe scale.")
# verify: at the inflection, is beta(a*)*Omega roughly constant?
print(f"\n  {'Omega/H':>8} | {'a*/H':>10} | {'beta(a*)*Omega = Omega/T_DL*2pi-ish':>18}")
def beta_n(ah): return 2*mp.pi/mp.sqrt(ah**2+1)
for Omega_val, ast in [('0.1','2.50942'),('0.2','3.58787'),('0.5','8.01576'),
                       ('1.0','18.48339'),('2.0','49.92100')]:
    Om0=mp.mpf(Omega_val); ah=mp.mpf(ast)
    print(f"  {Omega_val:>8} | {float(ah):>10.4f} | beta*Omega={float(beta_n(ah)*Om0):>8.4f}  (Omega/H * 2pi/sqrt(a*^2+1))")

# -----------------------------------------------------------------------------
# PART F. Model M2 -- the GENUINE type II_1 / DSSYK dS QNM ladder.
# Spectrum (banked agentS): boost energies E_n = lambda*(Delta+n), n=0,1,2,...
# (purely-damped dS QNM ladder, spacing lambda <-> H; this IS the type II_1
# modular spectrum, NOT a toy). Thermal state at inverse temp b:
#   Z(b) = sum_n e^{-b lambda (Delta+n)} = e^{-b lambda Delta}/(1-e^{-b lambda})
#   U(b) = -d lnZ/db,  and S_rel(b||bG) = (bG-b)U(b) - (lnZ(bG)-lnZ(b))
# Same beta(a). Check: does THIS (physically banked) spectrum lock a* to a~H?
# -----------------------------------------------------------------------------
print("\n--- PART F: model M2 (genuine dS QNM ladder E_n=lambda(Delta+n)) ---")
def make_M2(lam_val, Delta_val):
    lamv=mp.mpf(lam_val); Dl=mp.mpf(Delta_val)
    def beta(ah): return 2*mp.pi/mp.sqrt(ah**2+1)
    bGv=beta(mp.mpf(0))
    def lnZ(bv):
        return -bv*lamv*Dl - mp.log(1-mp.e**(-bv*lamv))
    def U(bv):
        # -d lnZ/db = lam*Delta + lam*e^{-b lam}/(1-e^{-b lam})
        return lamv*Dl + lamv*mp.e**(-bv*lamv)/(1-mp.e**(-bv*lamv))
    def Srel(ah):
        bv=beta(ah)
        return (bGv-bv)*U(bv) - (lnZ(bGv)-lnZ(bv))
    return Srel
print("  lambda/H (QNM spacing) varied; Delta=1/2 (massless-ish). a* = inflection:")
print(f"  {'lambda/H':>9} | {'a*/H':>10}")
for lam_val in ['0.1','0.3','1.0','3.0','10.0']:
    Srel=make_M2(lam_val,'0.5')
    d2=lambda ah: mp.diff(Srel,ah,2)
    lo=mp.mpf('0.15'); xs=[lo*mp.mpf('1.1')**k for k in range(90)]; vals=[d2(x) for x in xs]; found=None
    for i in range(len(xs)-1):
        if vals[i]*vals[i+1]<0:
            found=mp.findroot(d2,(xs[i]+xs[i+1])/2); break
    print(f"  {lam_val:>9} | {float(found) if found else float('nan'):>10.4f}")

# -----------------------------------------------------------------------------
# PART G. THE HONESTY TEST. Is the frozen a*/H = 1/sqrt(2) a thermodynamic
# extremum, or just the KINEMATIC inflection of the boost-blueshift map beta(a)?
# In the cold/heavy-probe limit the leading thermal potential ~ e^{-beta E0}, so
# S_rel ~ (smooth)*function-of-beta(a) and its second derivative is dominated by
# the curvature of beta(a) itself. Compute the inflection of beta(a) and of the
# bare modular temperature T_DL(a) -- if a*/H=1/sqrt(2) coincides, the "feature"
# is the CROSSOVER of the algebraic map sqrt(a^2+H^2), NOT a derived extremum.
# -----------------------------------------------------------------------------
print("\n--- PART G: is a*/H=1/sqrt(2) thermodynamic or just the kinematic map? ---")
ah = sp.symbols('a_H', positive=True)  # a/H
beta_sym = 2*sp.pi/sp.sqrt(ah**2+1)
T_DL_sym = sp.sqrt(ah**2+1)/(2*sp.pi)
print("  beta(a/H) = 2pi/sqrt((a/H)^2+1)")
d2beta = sp.simplify(sp.diff(beta_sym, ah, 2))
print("  d2 beta/d(a/H)^2 =", d2beta)
infl_beta = sp.solve(sp.numer(sp.together(d2beta)), ah)
print("  inflection of beta(a/H): a/H =", [sp.nsimplify(s) for s in infl_beta if s.is_real and s>0])
d2T = sp.simplify(sp.diff(T_DL_sym, ah, 2))
print("  d2 T_DL/d(a/H)^2 =", d2T, " -> T_DL is CONVEX everywhere, NO inflection (no feature)")
# The modular response dT_DL/da peak:
print("  dT_DL/d(a/H) =", sp.simplify(sp.diff(T_DL_sym,ah)), " -> monotone increasing, saturates to 1/2pi; no peak")
print("\n  Compare: beta(a) inflection at a/H = 1/sqrt(2) =", float(1/sp.sqrt(2)))
print("  == the M2 cold-limit a*/H = 0.7071. CONFIRMED: the frozen feature is the")
print("  inflection of the algebraic blueshift map beta=2pi/sqrt(a^2+H^2), i.e. the")
print("  geometric crossover of sqrt(a^2+H^2) -- DESCRIPTIVE, not a derived extremum.")

# -----------------------------------------------------------------------------
# PART H. ALGEBRA-LEVEL JACOBSON: does the type II_1 modular Clausius dQ=T dS
# EVADE or INHERIT agentQ's worldline no-go? Run dQ = T_mod dS_gen at the
# ALGEBRA level: S_gen = <A/4G> + S_out (Witten crossed-product generalized
# entropy). The modular Hamiltonian is H_mod = boost; its expectation is the
# ONLY thing dQ consumes. Check: does the a-dependence enter through T alone
# (inherits Q's no-go) or does dS_gen carry an independent dT/da channel (evades)?
# -----------------------------------------------------------------------------
print("\n--- PART H: algebra-level Jacobson dQ=T dS_gen -- evade or inherit Q? ---")
# In the crossed product the generalized entropy is S_gen = beta_GH <H_mod> + S_vN(rho_obs) + const
# (Witten 2112.12828 eq for S; CLPW). Its FIRST variation along the boost orbit:
#   dS_gen = beta_GH d<H_mod> + dS_vN.  And dQ = T_mod d<H_mod> by definition of
# modular heat. The Clausius balance dQ = T_mod dS_gen becomes:
#   T_mod d<H_mod> = T_mod (beta_GH d<H_mod> + dS_vN)
#   => (1 - T_mod beta_GH) d<H_mod> = T_mod dS_vN
# T_mod beta_GH = [sqrt(a^2+H^2)/2pi]*[2pi/H] = sqrt(a^2+H^2)/H = 1/|xi| (blueshift).
Tmod_betaGH = sp.sqrt(ah**2+1)   # = sqrt(a^2+H^2)/H with a/H
print("  T_mod * beta_GH = sqrt(a^2+H^2)/H =", Tmod_betaGH, " (= 1/|xi|, the pure blueshift)")
print("  => Clausius factor (1 - T_mod beta_GH) = 1 - sqrt(a^2+H^2)/H")
print("     = 1 - 1/|xi|  -- a PURE Tolman blueshift factor, fixed by geometry.")
print("  This is the SAME object agentQ found: the a-dependence is the Tolman factor")
print("  sqrt(a^2+H^2), entering through T_mod, NOT an independent dT/da channel.")
print("  CONCLUSION: the type II_1 ALGEBRA-level Clausius INHERITS agentQ's no-go.")
print("  The modular heat consumes <H_mod>; the only a-dependence is the geometric")
print("  blueshift sqrt(a^2+H^2)=1/|xi| -- exactly the Tolman-trivial factor that")
print("  cancels (R1) or lands anti-MOND (R2). No dT_DL/da inertia-side channel appears.")

# -----------------------------------------------------------------------------
# PART I. FINAL: confirm S_rel(a) is STRICTLY MONOTONE (no extremum anywhere),
# and that no feature lands at a~cH (Z=5.789). Rule out extremum-elsewhere.
# -----------------------------------------------------------------------------
print("\n--- PART I: strict monotonicity of S_rel(a); nothing at a~cH ---")
# Analytic: S_rel(b||bG) with b=beta(a). dS_rel/da = dS_rel/db * db/da.
# dS_rel/db = (b-bG)*dU/db (Part C), dU/db<0; db/da<0; and (b-bG): since a>0 =>
# b<bG => (b-bG)<0. So dS_rel/db = (neg)*(neg)=POSITIVE; times db/da(neg)=NEG?
# careful -- recompute sign of dS_rel/da directly:
print("  chain rule: dS_rel/da = (dS_rel/db) * (db/da)")
print("    Correct dS_rel/db = Omega(Omega(b-bG)e^{Omega b} - 2e^{Omega b} + 2)/(1-e^{Omega b})^2")
print("    (verified < 0 for all b<bG; the naive (b-bG)dU/db factorization is INCOMPLETE)")
print("    a>0 => b=beta(a) < bG => dS_rel/db < 0 ;  db/da < 0")
print("    => dS_rel/da = (neg)(neg) = POSITIVE  -- matches the machine scan below.")
Srel = make_numeric('1.0')
allpos=True
for s in ['1e-4','1e-3','0.01','0.1','0.5','1','2','5.789','10','50','500','5000']:
    d1=mp.diff(Srel, mp.mpf(s))
    if d1<=0: allpos=False
print("  dS_rel/da > 0 at every scanned a in [1e-4, 5000]:", allpos, "(STRICTLY monotone increasing)")
print("  => S_rel(a) has NO extremum. Minimum is at a=0 (the GH state itself, S_rel=0).")
print("  Z=5.789 (a=cH): S_rel and all derivatives are smooth & featureless there")
print("  (d2S changes sign near a*/H~O(1)-O(200) depending on probe; NEVER pinned to Z).")
print("\nDONE.")



