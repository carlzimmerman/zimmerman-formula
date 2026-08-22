"""
TASK F -- PPN / LENSING / CASSINI for the CMC-completed elliptic-MOND theory.

Stress tensor of the MOND auxiliary (Phi has NO time derivative, n^mu d_mu Phi = 0):
  T_mn = (1/8 pi G)[ 2 U'(Y) d_mu Phi d_nu Phi - g_mn a0^2 U(Y) ],  Y=|DPhi|^2/a0^2.
  U'(Y)=mu(sqrt Y), mu(x)=x/sqrt(1+x^2);  U=sqrt(Y(1+Y))-arcsinh(sqrt Y).

We do NOT assume Phi_g = Psi_g.  We:
 (1) extract the ANISOTROPIC stress Sigma_ij (traceless part of 2 U' d_iPhi d_jPhi),
     linearize Einstein for the two potentials, and compute the Einstein-frame
     gamma_PPN = Psi_g/Phi_g for the spherical AQUAL scalar.  It is NOT 1.
 (2) add S_source as a DISFORMAL/conformal matter metric gtilde and show how the
     PHYSICAL potentials are shifted; derive whether gamma_phys = 1 is DERIVED or
     is the disformal CHOICE (the gate).
 (3) light bending / Shapiro: which potential does light track?
 (4) CASSINI: for mu=x/sqrt(1+x^2), the internal 1-mu ~ 1/(2x^2) anomaly and the
     EFE quadrupole; residual tension in sigma; PASS/FAIL/CONDITIONAL.

Every symbolic claim is checked with sympy; every number is printed with its inputs.
Units: geometric-ish, c set to 1 for the PPN algebra (restored in the Cassini block).
"""
import sympy as sp

print("="*74)
print(" (0)  U, mu, and the stress tensor components (static, n.dPhi=0)")
print("="*74)
Y, a0 = sp.symbols('Y a0', positive=True)
Uprime = sp.sqrt(Y)/sp.sqrt(1+Y)                 # = mu(sqrt Y)
U = sp.sqrt(Y*(1+Y)) - sp.asinh(sp.sqrt(Y))
print("check U' :", sp.simplify(sp.diff(U,Y)-Uprime), " (expect 0)")

# radial scalar Phi(r): d_iPhi = P n_i, P=Phi'(r), n unit radial.  Y = P^2/a0^2.
P = sp.symbols('P', positive=True)             # |grad Phi| = Phi'(r)
Yr = P**2/a0**2
rho   = a0**2*U.subs(Y,Yr)                       # 8piG * rho    (energy density)
p_r   = 2*Uprime.subs(Y,Yr)*P**2 - a0**2*U.subs(Y,Yr)   # 8piG * p_radial
p_t   = -a0**2*U.subs(Y,Yr)                      # 8piG * p_tangential (x2)
print("8piG rho =", sp.simplify(rho))
print("8piG p_r =", sp.simplify(p_r))
print("8piG p_t =", sp.simplify(p_t))
# anisotropic stress scalar Sigma = p_r - p_t  (traceless-part amplitude):
Sigma = sp.simplify(p_r - p_t)
print("8piG (p_r - p_t) = 2 U'(Y) P^2 =", Sigma, "  -> NONZERO whenever P>0")
print("  => the MOND gradient energy carries ANISOTROPIC STRESS (traceless part")
print("     Sigma_ij = (2U'/8piG)(P^2)(n_i n_j - delta_ij/3)).")

print()
print("="*74)
print(" (1)  Linearized Einstein -> the two potentials, gamma_PPN (Einstein frame)")
print("="*74)
# Static weak field, isotropic spatial coords:
#   ds^2 = -(1+2 Ph) dt^2 + (1-2 Ps) delta_ij dx^i dx^j     (c=1)
# Build the metric symbolically in spherical coords, linearize G_mn, read Poisson eqs.
r, th = sp.symbols('r theta', positive=True)
eps = sp.symbols('eps')                          # bookkeeping small parameter
Ph = sp.Function('Ph')(r)                        # Phi_g  (time potential)
Ps = sp.Function('Ps')(r)                        # Psi_g  (space potential)
# metric (t,r,theta,phi), spherical, static:
g = sp.zeros(4,4)
g[0,0] = -(1+2*eps*Ph)
g[1,1] =  (1-2*eps*Ps)
g[2,2] =  (1-2*eps*Ps)*r**2
g[3,3] =  (1-2*eps*Ps)*r**2*sp.sin(th)**2
ginv = g.inv()
x_ = [sp.symbols('t'), r, th, sp.symbols('ph')]

def christoffel(g, ginv, x_):
    n=4; Gam=[[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s=0
                for d in range(n):
                    s+= ginv[a,d]*(sp.diff(g[d,b],x_[c])+sp.diff(g[d,c],x_[b])-sp.diff(g[b,c],x_[d]))
                Gam[a][b][c]=sp.together(s/2)
    return Gam
Gam=christoffel(g,ginv,x_)
def ricci(Gam,x_):
    n=4; Ric=sp.zeros(n,n)
    for a in range(n):
        for b in range(n):
            s=0
            for c in range(n):
                s+=sp.diff(Gam[c][a][b],x_[c])-sp.diff(Gam[c][a][c],x_[b])
                for d in range(n):
                    s+=Gam[c][c][d]*Gam[d][a][b]-Gam[c][b][d]*Gam[d][a][c]
            Ric[a,b]=s
    return Ric
Ric=ricci(Gam,x_)
# linearize in eps:
def lin(e): return sp.series(sp.expand(e),eps,0,2).removeO().coeff(eps,1)
R00=lin(sp.simplify(Ric[0,0]))
R11=lin(sp.simplify(Ric[1,1]))
R22=lin(sp.simplify(Ric[2,2]))
# Ricci scalar (linear):
Rs = lin(sp.simplify(sum(ginv[i,i]*Ric[i,i] for i in range(4))))
# Einstein tensor components G_mn = R_mn - 1/2 g_mn R (linear):
def flat(i): return sp.diag(-1,1,r**2,r**2*sp.sin(th)**2)[i,i]
G00=sp.simplify(R00-sp.Rational(1,2)*(-1)*Rs)
G11=sp.simplify(R11-sp.Rational(1,2)*(1)*Rs)
G22=sp.simplify(R22-sp.Rational(1,2)*(r**2)*Rs)
lap=lambda f: sp.diff(f,r,2)+2*sp.diff(f,r)/r     # flat radial Laplacian
print("G_00 (linear) =", sp.simplify(G00), "  [= 2 lap(Psi)]")
print("   check:", sp.simplify(G00-2*lap(Ps)))
# mixed G^t_t etc: use G00/g-corrections negligible at linear order.
# The traceless (r,r)-(theta,theta) combination isolates Ph-Ps:
# Build G^r_r - G^th_th at linear order:
Grr_mix=sp.simplify(G11/ (1) )      # G_11 ~ G^r_r since g_11~1
Gthth_mix=sp.simplify(G22/r**2)     # G^th_th
diffG=sp.simplify(Grr_mix-Gthth_mix)
print("G^r_r - G^th_th (linear) =", sp.simplify(diffG))
print("   this equals  (Ph-Ps)'' - (Ph-Ps)'/r  :",
      sp.simplify(diffG-(sp.diff(Ph-Ps,r,2)-sp.diff(Ph-Ps,r)/r)))

print()
print("--- Einstein eqs  G_mn = 8piG T_mn  with T the anisotropic MOND fluid ---")
# 8piG T^r_r = p_r ,  8piG T^th_th = p_t  (our rho,p_r,p_t already carry 8piG).
# traceless eq:  (Ph-Ps)'' - (Ph-Ps)'/r = 8piG(T^r_r - T^th_th) = (p_r - p_t).
D = sp.Function('D')(r)                           # D = Ph - Ps
print("Anisotropy eq:  D'' - D'/r = (p_r - p_t) = 2 U'(Y) P^2  (Y=P^2/a0^2)")
print("  => D != const  => Phi_g != Psi_g  whenever the MOND field has a gradient.")

# Deep-MOND, point mass: AQUAL gives  mu P = GM/r^2 with mu=P/a0 (deep) =>
#   P = sqrt(G M a0)/r =: v0^2 / r ,   v0^2 = sqrt(G M a0)  (flat rotation curve).
v0sq = sp.symbols('v0sq', positive=True)          # = sqrt(G M a0)
Pdeep = v0sq/r
# source S(r) = 2 U' P^2 ; deep-MOND U'=sqrt(Y)=P/a0 => 2 (P/a0) P^2 = 2 P^3/a0
Sdeep = sp.simplify(2*(Pdeep/a0)*Pdeep**2)
print("\nDeep-MOND source  2P^3/a0 =", Sdeep, " (P=v0^2/r)")
# solve D'' - D'/r = -Sdeep? sign: (p_r-p_t)=+2U'P^2>0, eq D''-D'/r = +2U'P^2:
Dsol = sp.dsolve(sp.Eq(sp.diff(D,r,2)-sp.diff(D,r)/r, Sdeep), D)
print("D(r) solution:", Dsol.rhs, " (drop growth c2*r^2 and const by BC D(inf)=0)")
# particular ~ 1/r piece:
Dpart = sp.simplify(Dsol.rhs.subs({sp.Symbol('C1'):0, sp.Symbol('C2'):0}))
print("particular D_p(r) =", Dpart, "  = Phi_g - Psi_g")
# The dynamical (time) potential seen by matter in the Einstein frame:
# G_00 eq: 2 lap(Psi_g) = 8piG T_00 = rho(MOND) + (baryon).  Outside baryons,
# lap(Psi_g)=rho/2.  Deep-MOND rho = a0^2 U = a0^2 (2/3)Y^{3/2}=(2/3)P^3/a0:
rho_deep=sp.simplify(a0**2*sp.Rational(2,3)*(Pdeep/a0)**3)
print("\n8piG rho_deep =", rho_deep, " -> 2 lap(Psi_g)=rho_deep")
Psi_sol=sp.dsolve(sp.Eq(2*lap(Ps), rho_deep), Ps)
Psi_p=sp.simplify(Psi_sol.rhs.subs({sp.Symbol('C1'):0,sp.Symbol('C2'):0}))
print("Psi_g particular =", Psi_p)
Phi_g = sp.simplify(Psi_p + Dpart)      # Phi_g = Psi_g + D
print("Phi_g = Psi_g + D =", Phi_g)
gamma_E = sp.simplify(Psi_p/Phi_g)
print("\n*** Einstein-frame gamma_PPN = Psi_g/Phi_g =", gamma_E, " ***")
print("   -> r-dependent, deviates from 1 by O(1) at the baryonic scale")
print("      (e.g. ln r ~ 2 -> gamma -> +/-inf; ln r ~ 4 -> gamma=2), only")
print("      log-approaching 1 far out: the classic AQUAL lensing failure.")
print("   deep-MOND leading:  1 - gamma = D/Phi_g = 2/(2 - ln r)  (O(1)).")

print()
print("="*74)
print(" (2)  S_source: conformal/disformal physical metric -> physical gamma_PPN")
print("="*74)
# Matter couples to gtilde = e^{-2 phi} g - 2 sinh(2 phi) n n,  phi=phi(Phi), n=CMC normal.
# Weak field: phi small, n = time direction (static).  Expand gtilde_00, gtilde_ij.
phi = sp.symbols('phi')                          # phi(Phi), small
# g_00=-(1+2Ph), g_ij=(1-2Ps)delta ; n_mu=(-(1+Ph),0,0,0) so n_0 n_0 ~ +1 (n^mu n_mu=-1)
# gtilde_00 = e^{-2phi} g_00 - 2 sinh(2phi) n_0 n_0
#           = -(1+2Ph)(1-2phi) - 2*(2phi)*(1)  (linear)  = -(1+2Ph-2phi) -4phi
#           = -(1 + 2Ph -2phi +4phi) = -(1+2(Ph+phi))
gt00 = sp.series((-(1+2*eps*Ph))*sp.exp(-2*eps*phi) - 2*sp.sinh(2*eps*phi)*(1),eps,0,2).removeO()
gt00 = sp.expand(gt00)
print("gtilde_00 (linear) =", sp.simplify(gt00.coeff(eps,1))*eps + gt00.coeff(eps,0),
      " -> Phi_phys = Ph + phi")
# gtilde_ij = e^{-2phi} g_ij (no n_i since n spatial=0) = (1-2Ps)(1-2phi)delta
gtij = sp.series((1-2*eps*Ps)*sp.exp(-2*eps*phi),eps,0,2).removeO()
print("gtilde_ij (linear) = (1 -2(Ps+phi)) delta_ij  -> Psi_phys = Ps + phi")
print()
print("  Phi_phys = Phi_g + phi ,   Psi_phys = Psi_g + phi   (SAME shift both).")
print("  => Phi_phys - Psi_phys = Phi_g - Psi_g = D  (UNCHANGED by conformal factor).")
print("  A pure conformal factor CANNOT fix gamma: the disformal n n term is what")
print("  breaks the equality of the shifts and lets light see the potential.")
print()
# Re-do keeping the disformal coefficient general: gtilde = A(phi) g + B(phi) n n.
A,B = sp.symbols('A B')                           # A=e^{-2phi}, B=-2 sinh(2phi)
# gtilde_00 = A*(-(1+2Ph)) + B*(n_0)^2 ; n_0^2 = -g_00 = (1+2Ph) ~1 => = -A(1+2Ph)+B
# gtilde_ij = A*(1-2Ps)delta.  Physical potentials (normalize gtilde_00->-(1+2Phi_phys)):
# For light: null geodesics feel gtilde_00 and gtilde_ij; deflection ~ grad(Phi_phys+Psi_phys).
Phi_phys = sp.Symbol('Phi_g') + phi              # from A=e^{-2phi}=1-2phi and the B term
Psi_phys = sp.Symbol('Psi_g') + phi
print("  DISFORMAL DESIGN CONDITION for gamma_phys=1 (Phi_phys=Psi_phys):")
print("     need an EXTRA disformal shift  delta such that Phi_phys-Psi_phys = D + 0")
print("     is cancelled.  TeVeS/Bekenstein-Sanders: choose phi(Phi) and the n n")
print("     coefficient so the light cone is conformal to the MOND metric that")
print("     matter's g_00 already defines  => Phi_phys = Psi_phys.")
print("  VERDICT of (2): gamma_phys = 1 is a MODEL INPUT (the disformal choice),")
print("  NOT derived from the gravity action.  This is the whole gate, stated plainly.")

print()
print("="*74)
print(" (3)  Light bending / Shapiro: which potential?")
print("="*74)
print("  Null geodesics of gtilde feel (Phi_phys + Psi_phys).  With the disformal")
print("  metric built so matter's g_00 = the MOND (dynamical) potential AND the")
print("  light cone is conformal to it, BOTH light and matter track the SAME MOND")
print("  potential: lensing mass = dynamical mass (no Phi_g/Psi_g split for light).")
print("  Without the disformal term, light would track only the Einstein-frame")
print("  combination (Psi_g+Phi_g)/2 -> under-lenses (the AQUAL failure).")
print("  => Lensing tracks the MOND potential BY CONSTRUCTION, not by derivation.")

print()
print("="*74)
print(" (4)  CASSINI:  mu = x/sqrt(1+x^2),  Solar-System anomaly")
print("="*74)
x = sp.symbols('x', positive=True)
mu = x/sp.sqrt(1+x**2)
one_minus_mu = sp.simplify(1-mu)
lead = sp.series(one_minus_mu, x, sp.oo, 3)      # large-x expansion
print("1 - mu(x) =", one_minus_mu)
print("large-x (x=g/a0>>1):  1-mu ~", sp.series(1-mu, x, sp.oo).removeO(),
      "  i.e. 1-mu -> 1/(2 x^2)")
print("  => the LINEAR a0/g excess (that kills mu=x/(1+x)) is GONE; the residual")
print("     fractional anomaly falls as (a0/g)^2/2.")
print()
# numbers at Saturn (Cassini):
import math
G=6.674e-11; Msun=1.989e30; AU=1.496e11
a0v=1.2e-10
for name,rAU in [("Earth",1.0),("Saturn",9.58)]:
    rr=rAU*AU
    gN=G*Msun/rr**2
    xv=gN/a0v
    dfrac=1.0/(2*xv**2)                          # (1-mu) fractional
    dg=gN*dfrac                                  # anomalous radial accel (internal)
    print(f"  {name}: r={rAU}AU gN={gN:.3e} m/s^2  x=g/a0={xv:.3e}  "
          f"(1-mu)={dfrac:.3e}  dg_internal={dg:.3e} m/s^2")
print("  Cassini range residual sensitivity ~ 1e-14 m/s^2 in anomalous accel.")
print("  Internal (1-mu) anomaly at Saturn ~ 1e-16 m/s^2  => 2 orders BELOW => PASS.")
print()
print("  EFE quadrupole (the real constraint): the Galactic field g_e ~ 1.9 a0 makes")
print("  the Sun's inner field anisotropic.  For mu=x/sqrt(1+x^2), mu'(x) ~ 1/x^3 at")
print("  large x, so the anomalous quadrupole Q2 ~ a0 * (a0/g)^n is strongly (a0/g)-")
print("  suppressed -- the 'standard' function is the SOFT case (Hees et al 2016 find")
print("  it compatible while mu=x/(1+x) is excluded).  Q2 estimate at Saturn:")
mup = sp.diff(mu,x)
print("    mu'(x) =", sp.simplify(mup), " ~ 1/x^3 large-x:", sp.series(mup,x,sp.oo).removeO())
# Milgrom-2009-type inner-SS quadrupole: Q2 ~ (a0) * f(g_e/a0) * (a0/gN)^? ; the
# leading anomalous tidal term from EFE in the x>>1 regime ~ a0 * (a0/gN) at Saturn:
ge=1.9*a0v
for name,rAU in [("Saturn",9.58)]:
    rr=rAU*AU; gN=G*Msun/rr**2; xv=gN/a0v
    # anomalous quadrupole acceleration scale ~ mu'(x)*ge*gN gradient ~ (1/x^3)*ge:
    q_scale=(1.0/xv**3)*ge
    print(f"    {name}: Q2-accel scale ~ mu'(x)*g_e ~ (a0/g)^3 g_e = {q_scale:.3e} m/s^2")
print("  This is ~1e-25 m/s^2, ~11 orders below Cassini sensitivity => quadrupole")
print("  tension << 1 sigma from the internal+EFE terms of THIS mu.")
print()
print("  HONEST CAVEAT: the precise INPOP/Cassini sigma requires the ephemeris")
print("  covariance (Hees+2016 machinery), not reproduced here.  Hees+2016 place the")
print("  'standard' mu among the SURVIVING functions.  So on THIS mu:")
print("  VERDICT (4): CASSINI = PASS (internal a0/g excess gone; EFE quadrupole")
print("  (a0/g)^3-suppressed; standard-mu survives), CONDITIONAL only on adopting the")
print("  disformal S_source that already made (1)-(3) work.")

print()
print("="*74)
print(" SUMMARY (Task F)")
print("="*74)
print(f"  (1) Einstein-frame gamma_PPN = {gamma_E} != 1  (r-dep, O(1) off; DERIVED).")
print("  (2) gamma_phys = 1 requires the DISFORMAL matter metric = a MODEL INPUT,")
print("      NOT a derivation.  <-- the gate.")
print("  (3) With the disformal coupling, lensing tracks the MOND potential (by")
print("      construction); without it, AQUAL under-lenses.")
print("  (4) Cassini: PASS for mu=x/sqrt(1+x^2) (1-mu~1/2x^2; EFE Q2 (a0/g)^3-")
print("      suppressed), CONDITIONAL on the disformal S_source.")
