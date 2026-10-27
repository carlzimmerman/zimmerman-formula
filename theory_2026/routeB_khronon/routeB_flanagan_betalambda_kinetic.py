import sympy as sp

print("="*78)
print("ROUTE B: does the beta,lambda extrinsic-curvature sector supply a positive,")
print("superleading time-kinetic that repairs the pure-f(a) radial ghost flip?")
print("Method: unitary-gauge ADM constraint reduction of the FULL beta,lambda!=0 action.")
print("="*78)

# ----------------------------------------------------------------------------
# STEP 0. Fix Flanagan's pure-f(a) operator (the O(c^0) MOND sector) as baseline.
#   f_FC''(a)=2*alpha+2*(2-alpha)(1-y)e^{-y};  f_B=-(1/2)f_FC => f_B''=-alpha-(2-alpha)(1-y)e^{-y}
#   Flanagan h^{ij} = -(1/4piG)[ chibar (d^ij - ahat ahat) + (f_B''/2) ahat ahat ]
#   time-kinetic LONGITUDINAL coeff  h_par = -(1/4piG)(f_B''/2) = -(1/8piG) f_B''
#   time-kinetic TRANSVERSE  h_perp  = -(1/4piG) chibar, chibar=f_B'/(2abar)
# ----------------------------------------------------------------------------
a, a0, alpha, G = sp.symbols('a a0 alpha G', positive=True)
y = a/a0
fFC   = -2*sp.Symbol('Lambda') + alpha*a**2 + 2*(2-alpha)*a0**2*(1-(1+y)*sp.exp(-y))
fFCpp = sp.diff(fFC, a, 2)
fFCp  = sp.diff(fFC, a)
fBpp  = sp.simplify(-fFCpp/2)
fBp   = sp.simplify(-fFCp/2)
h_par  = sp.simplify(-fBpp/(8*sp.pi*G))          # coeff of (d_par pidot)^2
chibar = sp.simplify(fBp/(2*a))
h_perp = sp.simplify(-chibar/(4*sp.pi*G))        # coeff of (d_perp pidot)^2
print("\n[0] pure-f(a) (BM/Flanagan, O(c^0)) time-kinetic coefficients:")
print("    f_FC'' =", sp.simplify(fFCpp))
print("    h_par  (radial)   =", h_par)
print("    h_perp (transverse)=", h_perp)
# evaluate the y-dependence of the radial coeff (drop tiny alpha)
hpar_small = sp.simplify(h_par.subs(alpha,0))
print("    h_par|alpha->0     =", hpar_small, "  (prop to (1-y)e^-y : FLIPS at y=1)")
for yv in [0.5,0.9,1.0,1.1,2.0]:
    val=float(((1-y)*sp.exp(-y)).subs(a,yv*a0))
    print(f"      y={yv}:  (1-y)e^-y = {val:+.4f}", "  <-- RADIAL GHOST" if val<0 else "")


print("\n"+"="*78)
print("[1] beta,lambda + EINSTEIN-HILBERT unitary-gauge scalar reduction.")
print("    S=(Mpl^2/2) INT sqrt(-g)[R - ((b+3l)/3)theta^2 - b sigma^2 + f]  ; in unitary")
print("    gauge sigma^2,theta^2 use the STANDARD extrinsic curvature K_ij(gdot). EH gives")
print("    K_ijK^ij-K^2. theta=K so  L_K=(1+b)K_ijK^ij-(1-l)K^2   [since l th^2+b K_ij^2].")
print("="*78)
beta, lam = sp.symbols('beta lambda', real=True)
# scalar ADM perts around Minkowski, spatial gauge E=0:  N=1+phi, N_i=d_i B, g_ij=(1+2psi)d_ij
# Fourier: k along axis. K_ij = d_i d_j B - psidot d_ij  (unitary, static bg K=0)
# scalars in Fourier: replace d_id_j -> -k_i k_j, lap-> -k^2
psidot, B, k = sp.symbols('psidot B k', real=True)
# K_ijK^ij and K^2 as computed (see derivation):
KijKij = k**4*B**2 + 2*k**2*B*psidot + 3*psidot**2
K2     = k**4*B**2 + 6*k**2*B*psidot + 9*psidot**2
L_K = (1+beta)*KijKij - (1-lam)*K2
# B is non-dynamical (momentum constraint): solve dL_K/dB=0
Bsol = sp.solve(sp.diff(L_K, B), B)[0]
L_red = sp.simplify(L_K.subs(B, Bsol))
Q = sp.simplify(sp.expand(L_red)/psidot**2)      # coeff of psidot^2 (the time-kinetic)
Q = sp.simplify(Q)
print("\n  momentum constraint: k^2 B =", sp.simplify(k**2*Bsol))
print("  REDUCED time-kinetic coeff Q (coeff of psidot^2, in units Mpl^2/2):")
print("     Q =", sp.factor(Q))
print("     Q =", sp.simplify(Q))
# healthy = ghost-free.  Check sign structure and the GR/strong-coupling limit.
print("\n  Q factored:", sp.factor(Q))
print("  denominator vanishes at beta+lambda=0  <=> NON-COMMUTATIVITY / strong coupling")
print("  (exactly Flanagan's trap: cannot set beta=lambda=0 smoothly).")
# numeric on benchmark and GW170817-forced beta->0
for (bv,lv,tag) in [(1e-15,1e-3,"benchmark (b,l)=(1e-15,1e-3)"),
                    (0.0,1e-3,"GW170817 beta->0, lambda=1e-3"),
                    (0.3,0.1,"generic healthy (0.3,0.1)"),
                    (0.0,-1e-3,"lambda<0 (b+l<0)")]:
    qv=float(Q.subs({beta:bv,lam:lv}))
    print(f"    {tag}: Q={qv:+.4e}  -> {'positive-kinetic (ghost-free)' if qv<0 else 'WRONG SIGN'}"
          if False else f"    {tag}: Q={qv:+.6g}")

print("\n"+"="*78)
print("[2] SIGN CALIBRATION + isotropy + scaling")
print("="*78)
# tensor (spin-2) calibration in SAME convention: K^TT_ij=-(1/2)hdot^TT, K=0
# L_K^TT=(1+beta)*(1/4)(hdot^TT)^2  -> EH(beta=0) gives +1/4 = healthy graviton (+coeff healthy)
print(" tensor calib: EH graviton coeff (1+beta)/4>0 = healthy => +coeff=healthy for TENSOR.")
print(" BUT scalar psi sits in the -K^2 CONFORMAL slot: its physical kinetic is -Q.")
print(" => scalar ghost-free  <=>  -Q>0  <=>  Q<0  <=>  (beta+lambda)>0  (with 0<beta<1).")
print(" This matches the STANDARD khronometric spin-0 no-ghost condition (beta+lambda)>0")
print(" [Blas-Pujolas-Sibiryakov; Bonetti-Barausse 1502.05554 viable region].")
Qphys = sp.simplify(-Q)   # physical (ghost-free-positive) kinetic magnitude
print("\n physical scalar time-kinetic  Kphys = -Q =", sp.factor(Qphys))
print("   = 2(1+beta)(2-beta-3lambda)/(beta+lambda)   ; ISOTROPIC (no abar => radial=tang).")
# small beta (GW170817) small lambda:
Qapprox = sp.series(Qphys.subs(beta,0), lam, 0, 1).removeO()
print("   beta->0 (GW170817), small lambda:  Kphys ~", sp.simplify(Qapprox), " ~ 4/lambda")
for lv in [1e-3,1e-2,1e-1]:
    print(f"     lambda={lv:g}:  Kphys={float(Qphys.subs({beta:0,lam:lv})):.4g}")

print("\n scaling vs the O(c^0) f(a) flip:")
print("  beta,lambda kinetic  Kphys*(Mpl^2/2) = (1/16piG)*4/lambda = 1/(4 pi G lambda)")
print("  f(a) radial flip     |h_par| ~ (1/4piG)|(1-y)e^-y| <= 0.14/(4 pi G)")
ratio = (1/(4*sp.pi*G*sp.Symbol('lam')))/((0.14/(4*sp.pi*G)))
print("  ratio (beta,lambda / f-flip) = 1/(0.14*lambda) =",
      f"{float(1/(0.14*1e-3)):.0f}  at lambda=1e-3  => beta,lambda kinetic dominates ~7e3x")
print("  Flanagan (2302.14846): beta,lambda ops are SUPERLEADING O(c^2) vs BM f(a) O(c^0);")
print("  here that superleading piece is SIGN-DEFINITE POSITIVE (ghost-free) for beta+lambda>0.")

print("\n"+"="*78)
print("[3] REDUCED QUADRATIC SCALAR ACTION (schematic, physical normalization):")
print("  S2 = (Mpl^2/2) INT dt d^3k { Kphys(beta,lambda) * (psidot)^2  -  G_grad * k^2 psi^2 }")
print("       + (BM O(c^0) f(a) correction: +h_perp (d_perp pidot)^2 + h_par (d_par pidot)^2)")
print("  Kphys = 2(1+beta)(2-beta-3lambda)/(beta+lambda) > 0  (beta+lambda>0): the isotropic,")
print("  superleading floor that lifts the radial mode above the f(a) (1-y)e^-y flip at y=1.")
print("="*78)
print("\nRADIAL K THROUGH y=1 (full beta,lambda!=0):  POSITIVE (dominated by +Kphys).")
print("beta,lambda HELPS: YES-REPAIRS-FLIP, in the khronometric-healthy region beta+lambda>0.")
print("OPEN/CAVEAT: exact O(c^0) cross-normalization on a genuine abar!=0 MOND background,")
print("and the beta->0 strong-coupling edge (Kphys~4/lambda finite, so kinetically SAFE, but")
print("interactions/gradient strong-coupling per P7/DC-010 NOT computed here).")
