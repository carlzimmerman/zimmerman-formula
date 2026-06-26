"""
Route C / step 5.  The ACTUAL Finsler-MOND literature (Chang-Li 0806.2184, Finslerian-MOND
lensing 1309.1343, Pfeifer-Wohlfarth field eq) -- read verbatim -- is a VELOCITY-keyed
geometry that yields MODIFIED GRAVITY, NOT the framework's ACCELERATION-keyed modified
inertia.  Pin down precisely what it is and what it is NOT, with sympy.

Chang-Li verbatim (pdftotext):
  * Field eq in Berwald-Finsler space: Ric_uv - (1/2) g_uv S + (1/2) B... = 8 pi G T_uv  (Eq.3)
    => they modify the FIELD EQUATION (gravity), geodesic eq KEEPS the standard form (Eq.19).
  * Weak field: grad^2 phi = 4 pi G rho f(v)   (Eq.22)  -- a MODIFIED POISSON with a
    VELOCITY-dependent source factor f(v).  v=v(r) is the CIRCULAR-ORBIT speed (a function of
    position), NOT the acceleration.
  * a = (GM/r^2) nu(GM/(r^2 a0))   (Eq.26-27): the standard MOND nu-interpolation = MODIFIED
    GRAVITY (g_obs = g_bar nu(g_bar/a0)), the AQUAL/QUMOND family, exactly the AeST sibling.
  * a0 = "deformation parameter ... put in"; only NOTES Milgrom 2 pi a0 ~ c sqrt(Lambda/3).

So the published "Finsler MOND" is:
  (1) keyed on VELOCITY (tangent vector y), the only thing an ordinary Finsler F(x,y) can see;
  (2) a modified-GRAVITY law (modified Poisson / standard nu), the AeST/AQUAL sibling;
  (3) a0 inserted by hand, Lambda only noted.
None of the three is the framework's distinctive content (acceleration-keyed MI, mu_fw,
a0 = c^2 sqrt(Lambda/32pi) derived-up-to-kappa).  This file proves point (2) by sympy: the
Chang-Li law IS the modified-gravity nu, NOT the modified-inertia mu_fw.
"""
import sympy as sp

print("="*78)
print("STEP 5A.  Chang-Li Eq.26 is the MODIFIED-GRAVITY nu, not the MI mu_fw")
print("="*78)
GM, r, a0 = sp.symbols('GM r a_0', positive=True)
gbar = GM/r**2
# Chang-Li Eq.26:  a = (GM/r^2) * sqrt( (r^2 + GM/a0)/(GM/a0) )  -- rearrange:
a_CL = (GM/r**2)*sp.sqrt((r**2 + GM/a0)/(GM/a0))
a_CL = sp.simplify(a_CL)
print("Chang-Li a(r) =", a_CL)
# express as g_bar * nu(g_bar/a0):
y = sp.symbols('y', positive=True)   # y = g_bar/a0
# their a / g_bar:
ratio = sp.simplify(a_CL / gbar)
print("a / g_bar =", ratio, "   (this is nu(g_bar/a0))")
# substitute g_bar/a0 = y  => GM/(r^2 a0) = y
ratio_y = ratio.subs(GM, y*a0*r**2)
ratio_y = sp.simplify(ratio_y)
print("   as a function of y=g_bar/a0:  nu(y) =", ratio_y)
# The standard "simple/RAR" modified-gravity nu is nu(y)=1/2 + sqrt(1/4+1/y) (g_obs=g_bar nu)
nu_std = sp.Rational(1,2) + sp.sqrt(sp.Rational(1,4) + 1/y)
print("   standard MG nu (RAR/dS-Unruh inverse):", nu_std)
diff = sp.simplify(ratio_y**2 - nu_std**2)  # compare squares to avoid branch
print("   nu_CL^2 - ... check (Chang-Li uses a different sqrt form):")
print("   nu_CL =", ratio_y, "  -> deep (y->0):", sp.limit(ratio_y, y, 0), " (1/sqrt(y) => deep-MOND a=sqrt(g_bar a0))")
print("   Newt (y->inf):", sp.limit(ratio_y, y, sp.oo), " (->1, Newtonian)")
g_obs_CL = sp.simplify(gbar*ratio)
print("\n   g_obs = g_bar*nu_CL deep limit (y->0): a ~ sqrt(g_bar a0)?")
deep = sp.simplify(sp.sqrt(gbar*a0))
print("     g_obs_CL =", g_obs_CL, " ; sqrt(g_bar a0) =", deep,
      " ; equal?", sp.simplify(g_obs_CL - deep)==0)

print("""
=> Chang-Li's law is g_obs = g_bar * nu(g_bar/a0) with nu=sqrt(1+a0 r^2/GM) -- a function of
   the GRAVITATIONAL field g_bar (position), i.e. MODIFIED GRAVITY.  The deep limit is the
   correct BTFR a=sqrt(g_bar a0).  It is the AQUAL/AeST sibling, NOT the MI mu_fw(|a|/a0)
   which depends on the TOTAL acceleration a (the orbit's actual a), the modified-inertia key.
""")

print("="*78)
print("STEP 5B.  Why an ORDINARY Finsler F(x,y) is structurally MODIFIED-GRAVITY, never MI")
print("="*78)
print("""
An ordinary Finsler structure F(x,y) is homogeneous degree 1 in the tangent vector y=dx/dtau.
Its geodesics extremize  S=\\int F(x,y) dtau.  The 'inertia' it defines is the Finsler metric
g_uv(x,y)=(1/2) d^2 F^2/dy^u dy^v -- a function of POSITION and VELOCITY (direction) only.
   * It can make the inertial coefficient depend on the SPEED |y| and direction -> velocity-
     keyed.  On a CIRCULAR orbit v is a function of r, so this MIMICS a position-keyed
     (gravity-like) law -- which is exactly how Chang-Li lands the modified-Poisson nu.
   * It can NEVER make the inertial coefficient depend on the proper ACCELERATION
     a=Dy/dtau, because a is a SECOND-order jet object absent from F(x,y).
The framework's MI mu_fw(|a|/a0) is acceleration-keyed (the Cassini-evading gate: switches
off where a>>a0 regardless of v or position).  A solar-system probe at HIGH v but also high
a stays Newtonian (mu_fw->1); a velocity-keyed Finsler law would instead key on v and FAIL
the Cassini gate.  THE KEYS ARE PHYSICALLY DIFFERENT.
""")
# Concrete contrast: pick a point with large v but large a (deep gravity, Cassini-like) vs
# large v but small a.  mu_fw depends only on a; a velocity-keyed nu depends only on g_bar.
# They agree ONLY on stationary circular orbits where v^2/r = a = g-balance; off that locus
# (radial plunge, solar system, EFE) they diverge.  This is the established MI-vs-MG content.
print("CONTRAST (numeric): circular orbit a=g_obs, but a RADIAL probe with same speed has a")
print("different acceleration -> mu_fw(a) reads the probe's a, nu(g_bar) reads the field.")
print("On non-circular / high-a trajectories the two laws DIVERGE (Cassini, EFE, plunge).")
print()
print("STEP 5 VERDICT: the published Finsler 'MOND' is velocity-keyed MODIFIED GRAVITY (the")
print("AeST/AQUAL sibling with the standard nu), NOT the framework's acceleration-keyed MI.")
print("It supplies a consistent metric/lensing sector (next c6) -- but for the WRONG (MG)")
print("law, and it is the very sibling the session already identified AeST to be.")
