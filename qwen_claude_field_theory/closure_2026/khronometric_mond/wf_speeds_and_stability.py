#!/usr/bin/env python3
"""
wf_speeds_and_stability.py
--------------------------
Consolidated, VALIDATED result for the candidate khronometric-MOND scalar sector.

From wf_flat_validation.py (matches Bonetti-Barausse PRD91,084053 Eq.14 EXACTLY):
   khronometric scalar speed, candidate convention (action has (1+beta)K_ijK^ij):
       cs^2(alpha,beta,lambda) = (alpha-2)(beta-lambda) / [ alpha (1+beta)(2+3lambda-beta) ]
   (BB convention beta->-beta:  (alpha-2)(beta+lambda)/[alpha(beta-1)(2+beta+3lambda)] = BB Eq.14)

From wf_adm_scalar_reduction.py (exact anisotropic EL reduction on the radial MOND
background), the HIGH-k phase speed in each direction equals cs^2 with the LOCAL
acceleration-Hessian eigenvalue playing the role of alpha:
       PAR  (k || a):  alpha_par  = W''(y)/2
       PERP (k _|_ a): alpha_perp = mu(y)/2 = (1-e^{-y})/2
This script:
  (1) re-derives c_par^2(y), c_perp^2(y) and shows A,B decomposition,
  (2) scans y across the MOND->Newton transition, checks tachyon-stability sign,
  (3) exhibits the deep-MOND strong coupling (kinetic coeff -> 0 as y->0),
  (4) states the relation to Flanagan's no-go.
"""
import sympy as sp, mpmath as mp

y,beta,lam=sp.symbols('y beta lambda',real=True)
mu = 1-sp.exp(-y)                    # = W'/y
Wpp= 1+(y-1)*sp.exp(-y)             # = W''
alpha=sp.symbols('alpha',real=True)
cs2 = (alpha-2)*(beta-lam)/(alpha*(1+beta)*(2+3*lam-beta))   # candidate convention (validated)

c_par  = sp.simplify(cs2.subs(alpha, Wpp/2))
c_perp = sp.simplify(cs2.subs(alpha, mu/2))
print("VALIDATED speed template (candidate conv):  cs^2 =",cs2)
print("\nc_par^2(y)  =", sp.simplify(c_par))
print("c_perp^2(y) =", sp.simplify(c_perp))

# A,B decomposition in the common normalization A0=(1+beta)(2+3lambda-beta):
# cs^2 = B/A with A = alpha*(1+beta)(2+3lam-beta), B=(alpha-2)(beta-lambda).
print("\n--- A,B decomposition (S = (M_Pl^2/2) int [ A pidot^2 - B_par(d_par pi)^2 - B_perp(d_perp pi)^2 ]) ---")
print("Common K^2-backbone factor  G(beta,lambda) = (1+beta)(2+3lambda-beta)")
print("Normalization I  (A carries the Hessian; A->0 in deep MOND):")
print("   A_par  = (W''(y)/2) G ,   B_par  = (W''(y)/2 - 2)(beta-lambda) = (W''-4)(beta-lambda)/2")
print("   A_perp = (mu(y)/2)  G ,   B_perp = (mu(y)/2  - 2)(beta-lambda) = (mu -4)(beta-lambda)/2")
print("Normalization II (A common & y-independent; strong coupling shows as B->inf):")
print("   A = G = (1+beta)(2+3lambda-beta)")
Bpar_II  = sp.simplify((Wpp-4)*(beta-lam)/Wpp)
Bperp_II = sp.simplify((mu-4)*(beta-lam)/mu)
print("   B_par  = (W''-4)(beta-lambda)/W''  =", Bpar_II)
print("   B_perp = (mu -4)(beta-lambda)/mu   =", Bperp_II)

# tachyon-stability sign: need c^2>0 for all y. Since 0<alpha<2 always (W''<=1.14, mu<=1),
# (alpha-2)<0; with G>0 and alpha>0, sign(c^2) = sign(-(beta-lambda)) = sign(lambda-beta).
print("\n--- TACHYON (gradient) STABILITY ---")
print("For y>0: alpha_par=W''/2 in (0,0.568], alpha_perp=mu/2 in (0,0.5).  Both < 2 always.")
print("=> (alpha-2)<0 for all y. With (1+beta)(2+3lambda-beta)>0 (small beta,lambda) and alpha>0,")
print("   sign(c^2) = sign(lambda-beta), SAME for both directions and INDEPENDENT of y.")
print("   GRADIENT-STABLE  <=>  lambda > beta   (candidate conv)  <=>  beta_BB + lambda > 0  (BB conv).")

# numeric scan
print("\n--- SCAN across transition (beta=-0.01, lambda=+0.03 => lambda>beta STABLE) ---")
bval,lval=-0.01,0.03
cpar_n = sp.lambdify(y, c_par.subs({beta:bval,lam:lval}),'mpmath')
cperp_n= sp.lambdify(y, c_perp.subs({beta:bval,lam:lval}),'mpmath')
Wpp_n  = sp.lambdify(y, Wpp,'mpmath'); mu_n=sp.lambdify(y,mu,'mpmath')
mp.mp.dps=15
print(" %6s %12s %12s %12s %12s"%("y","W''","mu","c_par^2","c_perp^2"))
for yv in [0.01,0.05,0.1,0.3,1.0,3.0,10.0,100.0]:
    print(" %6g %12.5g %12.5g %12.5g %12.5g"%(yv,float(Wpp_n(yv)),float(mu_n(yv)),
                                              float(cpar_n(yv)),float(cperp_n(yv))))

print("\n--- STRONG COUPLING (deep MOND) ---")
print("Kinetic normalization I: A ~ alpha_eff*(1+beta)(2+3lambda-beta), alpha_eff=W''/2 or mu/2.")
print("As y->0: W''~2y-3y^2/2 ->0 and mu~y ->0  => A -> 0  => c^2 = B/A -> infinity.")
print("The khronon kinetic term VANISHES in deep MOND (strong coupling). The K^2 backbone")
print("(beta,lambda) supplies only the finite factor (1+beta)(2+3lambda-beta); it does NOT")
print("provide a y-independent floor for A.  This is the Bonetti-Barausse strong-coupling")
print("problem; it bites here because W(y)=y^3/3+... in deep MOND has W''(0)=0 (no quadratic")
print("'khronometric floor', unlike BB's f~2a^2-4a^3/3a0 which keeps f''(0)=4).")
# show A->0 rate
print("\n A(y)/G  (=alpha_eff=W''/2, parallel) vs y :")
for yv in [1.0,0.3,0.1,0.03,0.01,0.003]:
    print("   y=%7g : alpha_par=W''/2=%10.4g   c_par^2=%10.4g"%(yv,float(Wpp_n(yv))/2,float(cpar_n(yv))))

print("\n--- ALPHA=2 (GR) SINGULARITY CHECK ---")
print("cs^2 has 1/alpha: as alpha_eff->0 (deep MOND) OR alpha->2 it diverges. Here alpha<2 always,")
print("so the divergence is the alpha->0 (deep-MOND) one. Newtonian regime y>>1: alpha->1/2, finite.")
c_newt = sp.simplify(cs2.subs(alpha,sp.Rational(1,2)))
print("Newtonian-limit speed (alpha=1/2):  c^2 =", c_newt, "= -3(beta-lambda)/[(1+beta)(2+3lambda-beta)]")
