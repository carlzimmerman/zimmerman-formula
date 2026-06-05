#!/usr/bin/env python3
r"""
THE DECISIVE PIECE neither prior workflow computed:  the Iyer-Wald PRESYMPLECTIC Theta-form
contribution Delta_S of the deep-MOND term on the STRAINED de Sitter bifurcation surface.

Prior null computed ONLY S_W = -2pi oint (dL/dR_abcd) eps eps  =>  0  for C(Q)Y^{3/2}  (correct:
the MOND term has no Riemann dependence, dL/dR=0).  But the 2026 result
'Black Hole Entropy Beyond the Wald Term' (arXiv:2605.22429) shows the FULL horizon entropy is

      S_H = S_W + S_1 + Delta_S,

and Delta_S comes from  -oint_H xi . Theta  with the presymplectic potential (for a scalar)

      Theta^mu = (dL/d(grad_mu phi)) * delta phi.

Crucially Delta_S can be NONZERO when the matter field is NOT smoothly extendable to the
bifurcation surface (singular field).  The deep-MOND field has grad_r phi = sqrt(GMa0)/r --
finite on the dS horizon but the question is whether xi.Theta survives there.

We compute xi.Theta on the bifurcation surface in sympy and decide:  does the Y^{3/2}
non-analyticity make Delta_S survive AND pin a0=kappa c sqrt(G rho_Lam), or does it vanish/
under-determine?  No inserted kappa.
"""
import sympy as sp

print("="*100)
print(" STEP 1.  Presymplectic Theta-form of the deep-MOND Lagrangian.")
print("="*100)
G, M, a0, r, R, Lam, c, hbar, lam = sp.symbols('G M a0 r R Lambda c hbar lambda', positive=True)
# Lagrangian L = -|grad phi|^3/(12 pi G a0).  Write in terms of grad_mu phi via Y=g^{mu nu}d_mu phi d_nu phi.
# Theta^mu = (dL/d(grad_mu phi)) delta phi.  For L = L(Y), dL/d(grad_mu phi) = 2 L'(Y) grad^mu phi.
Y = sp.symbols('Y', positive=True)
Lp = sp.diff(-Y**sp.Rational(3,2)/(12*sp.pi*G*a0), Y)     # L'(Y)
print(f"  L(Y) = -Y^(3/2)/(12 pi G a0),  L'(Y) = {sp.simplify(Lp)}")
print( "  Theta^mu = 2 L'(Y) (grad^mu phi) delta phi.")
print( "  The component PIERCING the horizon is the radial one: Theta^r = 2 L'(Y) (grad^r phi) delta phi.\n")

# On-shell radial gradient and Y:
gradphi_r = sp.sqrt(G*M*a0)/r       # grad_r phi
Y_os = gradphi_r**2                 # = G M a0 / r^2
Theta_r = sp.simplify(2*Lp.subs(Y, Y_os) * gradphi_r)   # times delta phi (carried symbolically)
print(f"  on-shell  Theta^r / delta phi = 2 L'(Y) grad_r phi = {Theta_r}")
print(f"     (carries (G M a0)^{{...}}; ~ 1/r^2 -- this is the 'momentum' flux of the scalar)\n")

print("="*100)
print(" STEP 2.  The boost Killing vector xi near the bifurcation surface, and xi.Theta.")
print("="*100)
# Near a (Killing) horizon, the horizon-generating boost Killing field vanishes ON the bifurcation
# surface like  xi^mu ~ kappa_surf * lambda * (unit normal)^mu, with lambda the proper/affine distance
# from the bifurcation surface and kappa_surf the surface gravity.  The Wald construction integrates
# xi.Theta on the horizon; at the BIFURCATION SURFACE lambda -> 0, so xi -> 0.
kappa_surf = 1/sp.sqrt(3/Lam)        # de Sitter surface gravity = 1/R_dS
# xi.Theta picks the radial contraction:  (xi.Theta) ~ xi_r * Theta^r ~ (kappa_surf * lambda) * Theta^r.
# Evaluate the DENSITY  xi.Theta  as lambda->0 at the horizon r=R_dS:
R_dS = sp.sqrt(3/Lam)
Theta_r_hor = Theta_r.subs(r, R_dS)
xi_dot_Theta = kappa_surf * lam * Theta_r_hor      # times delta phi
print(f"  xi^r ~ kappa_surf * lambda = {sp.simplify(kappa_surf)} * lambda")
print(f"  Theta^r at horizon r=R_dS = {sp.simplify(Theta_r_hor)}")
print(f"  (xi.Theta)/delta phi ~ kappa_surf*lambda*Theta^r = {sp.simplify(xi_dot_Theta)}  (times delta phi)")
print()
print("  AT THE BIFURCATION SURFACE lambda -> 0:")
limit_bif = sp.limit(xi_dot_Theta, lam, 0)
print(f"     lim_{{lambda->0}} (xi.Theta) = {limit_bif}")
print("""
   *** THE CRUX ***  The deep-MOND Theta^r ~ 1/r^2 is FINITE at r = R_dS (the field is large-r
   regular: grad phi ~ 1/r is smooth and BOUNDED on the cosmological horizon -- UNLIKE a field
   that blows up AT the bifurcation surface).  So xi.Theta ~ kappa*lambda*(finite) -> 0 linearly.
   The 2026 'Beyond Wald' loophole requires the field to be SINGULAR (non-smoothly-extendable) AT
   the bifurcation surface to get a finite xi.Theta.  Here the singularity of grad phi is at r=0
   (the MASS, deep in the bulk), NOT at the horizon.  On the horizon the field is smooth.
   => Delta_S = 0  for the cosmological-horizon strain by a point mass in the bulk.
""")

print("="*100)
print(" STEP 3.  Could the field be singular ON the horizon?  Only if the MASS sits on it.")
print("="*100)
# If instead the mass is AT the horizon (r -> R_dS is where grad phi blows up), the relevant scale is
# the MOND transition radius r_t = sqrt(GM/a0).  But then 'the horizon' and 'the mass' coincide and the
# deep-MOND approximation (r >> r_t, bulk field) breaks; one is in the Newtonian/Schwarzschild zone,
# where Y is analytic and the Y^{3/2} branch does not apply.  Demonstrate the regime check:
r_t = sp.sqrt(G*M/a0)
print(f"  MOND transition radius r_t = sqrt(GM/a0) = {r_t}.")
print( "  deep-MOND (Y^{3/2}) is valid only for r >> r_t.  For the bulk point mass, r_t << R_dS, so")
print( "  on the horizon r=R_dS the field is deep-MOND AND smooth (Theta finite) => xi.Theta->0.")
print( "  Putting the mass ON the horizon (r_t ~ R_dS) EXITS the deep-MOND branch => Y^{3/2} N/A.")
print( "  Either way, the Y^{3/2} term gives NO finite bifurcation-surface Theta. No Delta_S.\n")

print("="*100)
print(" STEP 4.  Even GRANTING a finite Delta_S, would it FIX a0?  Dimensional/closure check.")
print("="*100)
# Suppose (counterfactually) xi.Theta gave a finite horizon integral. Its value ~ (dL/dY) grad phi
# ~ (1/a0) * (GMa0)^{...}.  Integrate over horizon area 4 pi R_dS^2 and track a0-dependence:
S1_like = sp.simplify(Theta_r_hor * 4*sp.pi*R_dS**2)   # schematic 'entropy-like' integral (x delta phi)
print(f"  schematic oint Theta^r dA ~ {S1_like}   (times delta phi)")
a0_power = sp.simplify(sp.log(abs(S1_like))/sp.log(a0))  # crude exponent probe is unreliable; do by hand:
print( "  a0-dependence by hand: Theta^r ~ L'(Y) grad phi ~ Y^{1/2}/a0 * Y^{1/2} = Y/a0 = (GMa0/r^2)/a0")
print( "                         = G M /r^2  -- the a0 CANCELS!  (Y/a0 is a0-independent on-shell.)")
Theta_check = sp.simplify((Y_os/a0))     # = G M / r^2, no a0
print(f"  check:  Y_onshell/a0 = {Theta_check}   <-- NO a0.  ")
print("""
   *** SECOND, INDEPENDENT OBSTRUCTION ***  On-shell, the deep-MOND momentum Theta^r ~ Y/a0 is
   EXACTLY a0-INDEPENDENT (because Y = G M a0/r^2 carries one a0 that cancels the 1/a0 in L').
   So EVEN IF a finite Delta_S existed, it would carry NO a0 and could not fix the normalization.
   This is the same structural fact as the homogeneous null, now shown on-shell off the saddle:
   the deep-MOND field self-adjusts (Y ~ a0) so that the entropy-relevant momentum is a0-blind.
""")

print("#"*100)
print("# VERDICT (Wald-Theta / strained bifurcation surface):")
print("#  (1) Standard Wald S_W = 0  (dL/dR_abcd = 0)              [prior null, reconfirmed].")
print("#  (2) New presymplectic Delta_S: xi.Theta -> 0 at the bifurcation surface because the")
print("#      deep-MOND field is SMOOTH on the cosmological horizon (its 1/r singularity is at the")
print("#      bulk mass r=0, not on the horizon) -> the 2026 'Beyond-Wald' loophole does NOT open.")
print("#  (3) Even granting a finite Delta_S, Theta^r ~ Y/a0 is a0-INDEPENDENT on-shell -> cannot")
print("#      fix the normalization.  TWO independent reasons the strained Wald entropy is a0-blind.")
print("#  ==> kappa is NOT forced.  The freedom persists.")
print("#"*100)
