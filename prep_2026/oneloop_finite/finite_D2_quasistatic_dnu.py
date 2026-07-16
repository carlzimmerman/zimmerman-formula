#!/usr/bin/env python3
r"""
finite_D2_quasistatic_dnu.py -- ONE-LOOP FINITE PART, DIAGRAM D2 (CW on quasistatic bg)
=======================================================================================
Framework (its OWN terms): dS-Unruh MODIFIED INERTIA, K(z)=(sqrt(1+4z)-1)/(2 sqrt z),
  W = u.K(Box_u/a0^2)u a LOCAL multiplication operator on phi, s=-1, ownn nu(y)=sqrt(1+1/y),
  y=g_bar/a0, a0=cH_Lambda/Z. rho_m=m^2 phi^2 is a STATED proxy.

On the QUASISTATIC accelerated background the frame is NOT comoving: W = W(y) != 0. This is
the ONE channel where a genuine y-dependent finite correction delta-nu(y) can live (D1 was
shape-uniform: finite_D1_selfenergy.py). Object:
    V_CW(M^2(y)),   M^2(y) = m^2(1 + sW(y)) = m^2(1 - W(y))   (s=-1),
the Coleman-Weinberg potential of the LOCAL loop mass on the accelerated background.

THIS SCRIPT (exit 0, sympy + mpmath; no hard-coded check(True)):
  [1] V_CW and its mu-INDEPENDENT nonanalytic piece (m^4/64pi^2)(1+sW)^2 ln(1+sW).
  [2] Condition N (Newtonian anchor y*=1e11) absorbs the LINEAR-in-W piece (renormalizes
      c_W / rho_m). The RESIDUAL leading shape deformation is proportional to W^2 -- a GENUINE
      shape deformation (NOT absorbable by a single normalization). Coefficient computed.
  [3] The two HONESTY FORKS for the MAGNITUDE (declared in SETUP 2.5), computed with real
      numbers, both footings:
        Fork P (proxy-literal rho_m=m^2 phi^2): loop/tree ~ (m^4/64pi^2)/rho_m -> catastrophic;
               the honest reading indicts the PROXY (vacuum gravitating through K), not the
               framework -- it is the CC problem imported through the vertex.
        Fork C (composite / normal-ordered rho_m = connected rest-mass density of real dust):
               loop/tree ~ (1/16pi^2) max[(q0/m)^2,(H/m)^2,T/m] -> compute; unobservable.
  [4] delta-nu(y): fractional shape deformation = [fork prefactor] x [bounded O(1) y-shape].
      The observability verdict is MAP-INDEPENDENT (set by the prefactor); a representative
      bounded W(y)=1/(1+y) is used ONLY to draw the shape, labeled as such.
  [5] y*-anchor-window spread (1e10..1e13) as the anchor-systematic; both footings.
Scheme-independent vs -dependent flagged inline. No 'proves/validates' language.
"""
import sympy as sp
import mpmath as mp
import sys
mp.mp.dps = 40
PASS = True
def check(name, cond):
    global PASS
    print(f"   [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond: PASS = False
def section(t):
    print("\n" + "#"*94); print("# " + t); print("#"*94)

# =====================================================================================
section("[1] V_CW ON THE QUASISTATIC BACKGROUND; mu-INDEPENDENT NONANALYTIC PIECE")
# =====================================================================================
m, mu, W = sp.symbols('m mu W', positive=True)
s = -1
M2 = m**2*(1 + s*W)                                  # local loop mass on quasistatic bg
VCW = (M2**2/(64*sp.pi**2))*(sp.log(M2/mu**2) - sp.Rational(3,2))
print(" V_CW(M^2(y)) with M^2 = m^2(1 - W)  (s=-1):")
sp.pprint(sp.simplify(VCW))
# split into mu-dependent (analytic, absorbable) and mu-INDEPENDENT nonanalytic parts:
#   ln(M^2/mu^2) = ln(m^2/mu^2) + ln(1 - W)
lnsplit = sp.log(M2/mu**2) - (sp.log(m**2/mu**2) + sp.log(1 + s*W))
check("ln(M^2/mu^2) = ln(m^2/mu^2) + ln(1+sW) exactly (mu-part factorizes off the W-part)",
      sp.simplify(lnsplit) == 0)
V_muindep = sp.simplify((M2**2/(64*sp.pi**2))*sp.log(1 + s*W))     # the mu-INDEPENDENT nonanalytic piece
V_mudep   = sp.simplify(VCW - V_muindep)
print(f"\n mu-INDEPENDENT nonanalytic piece  V_ni = (m^4/64pi^2)(1+sW)^2 ln(1+sW):")
sp.pprint(V_muindep)
check("mu-independent nonanalytic piece = (m^4/64pi^2)(1-W)^2 ln(1-W) (the sharp delta-nu candidate)",
      sp.simplify(V_muindep - (m**4/(64*sp.pi**2))*(1-W)**2*sp.log(1-W)) == 0)

# =====================================================================================
section("[2] CONDITION N absorbs LINEAR-in-W; RESIDUAL leading deformation ~ W^2")
# =====================================================================================
print(r"""
 Condition N (Newtonian anchor): the tree coupling is -(1/2)rho_m s W (LINEAR in W). Any
 loop piece LINEAR in W renormalizes rho_m/c_W and is absorbed at y* -- it CANNOT deform nu.
 The genuine deformation is the part of V_ni that is NONLINEAR in W. Taylor-expand the
 mu-independent nonanalytic piece in W:""")
x = sp.symbols('x')                    # x = sW = -W
Vni_x = ((1+x)**2*sp.log(1+x))         # (m^4/64pi^2) factored out; x=sW
ser = sp.series(Vni_x, x, 0, 4).removeO()
print(f"  (1+sW)^2 ln(1+sW) = {sp.expand(ser)}  + O(W^4)   [x = sW = -W]")
c_lin  = ser.coeff(x, 1)
c_quad = ser.coeff(x, 2)
print(f"   linear coeff (absorbed by condition N)     = {c_lin}")
print(f"   quadratic coeff (RESIDUAL shape deformation)= {c_quad}")
check("linear-in-W coefficient = 1 (single power, fully absorbed by the Newtonian anchor)",
      c_lin == 1)
check("residual leading deformation is QUADRATIC in W with coefficient 3/2 "
      "(genuine shape channel: NOT absorbable by one normalization)", c_quad == sp.Rational(3,2))
# residual finite deformation of the effective Lagrangian, s^2=1:
dL_res = sp.simplify((m**4/(64*sp.pi**2))*c_quad*W**2)     # (3 m^4/128 pi^2) W^2
print(f"\n RESIDUAL mu-independent finite deformation: dL_res = {dL_res}  (= 3 m^4 W^2/128 pi^2)")
print(" This is the D2 shape-deforming piece. Its SIGN is fixed (positive), its MAGNITUDE is")
print(" set by the fork below. It is quadratic in W -> vanishes at exact dS (W=0), as it must.")

# =====================================================================================
section("[3] THE TWO HONESTY FORKS (magnitude), real numbers, both footings")
# =====================================================================================
c_light = 2.998e8
hbar    = 1.0546e-34
FOOT = [("canonical a0=cH_L/Z", 9.36e-11, 1.808e-18),
        ("alt      a0=cH0/Z  ", 1.13e-10, 2.184e-18)]
# matter: proton (the framework's own rest-mass carriers)
m_p_kg = 1.6726e-27
m_p_invs = m_p_kg*c_light**2/hbar        # Compton angular frequency (1/s)
rho_m_gal = 1e-21                         # kg/m^3, representative galactic baryon density
print(f" proton m = {m_p_invs:.3e} 1/s;  representative galactic rho_m = {rho_m_gal:.0e} kg/m^3")
for lab,a0v,Hv in FOOT:
    q0 = a0v/c_light                      # frame frequency scale (1/s)
    T_dS = Hv/(2*sp.pi)                   # dS temperature as a frequency
    # Fork P: loop coefficient (m^4/64pi^2) as an ENERGY DENSITY vs tree rho_m.
    #   (m c^2)^4/(64 pi^2 (hbar c)^3 ... ) -- in mass-density units: use m^4 -> (m_p c^2)^4/(hbar^3 c^5)
    E_p = m_p_kg*c_light**2               # proton rest energy (J)
    loop_energy_density = (E_p**4)/(64*float(sp.pi)**2*(hbar*c_light)**3)/c_light**2  # kg/m^3
    forkP_ratio = loop_energy_density/rho_m_gal
    # Fork C: connected-fluctuation suppression. The DERIVATIVE/CURVATURE expansion parameters
    # are the power-law suppressions (q0/m)^2 and (H/m)^2. The dS-THERMAL contribution for a
    # heavy field (m >> T_dS) is EXPONENTIALLY (Boltzmann) suppressed exp(-m/T), NOT the power
    # T/m -- listing T/m as a power was the wrong estimate; the physical thermal factor underflows.
    therm = mp.e**(-m_p_invs/float(T_dS))         # exp(-m/T): ~0 for m>>T (heavy matter)
    supp = max((q0/m_p_invs)**2, (Hv/m_p_invs)**2)  # power-law (derivative/curvature) suppressions
    forkC = (1.0/(16*float(sp.pi)**2))*supp
    print(f"\n {lab}: a0={a0v:.3e}, H={Hv:.3e}, q0=a0/c={q0:.3e} 1/s")
    print(f"   Fork P (proxy-literal):  loop/tree ~ {forkP_ratio:.3e}   (CATASTROPHIC -> indicts the PROXY)")
    print(f"   Fork C (composite dust): (q0/m)^2={ (q0/m_p_invs)**2:.2e}, (H/m)^2={(Hv/m_p_invs)**2:.2e}, "
          f"thermal exp(-m/T)={mp.nstr(therm,3)} (underflow)")
    print(f"                            loop/tree ~ (1/16pi^2)*max[(q0/m)^2,(H/m)^2] = {forkC:.3e}   (UNOBSERVABLE)")
check("Fork P is catastrophic (>>1): the m^2 phi^2 proxy lets vacuum gravitate through K "
      "= CC problem imported through the vertex; a statement about the PROXY, not the framework",
      loop_energy_density/rho_m_gal > 1e20)
check("Fork C (physical, composite rho_m) is suppressed by (1/16pi^2) x max[(q0/m)^2,(H/m)^2] "
      "<= ~1e-84 (thermal exp(-m/T) underflows): unobservable in ANY regime (deep-MOND, RAR "
      "curvature, wide binaries all >70 dex below)",
      (1.0/(16*float(sp.pi)**2))*max((q0/m_p_invs)**2,(Hv/m_p_invs)**2) < 1e-78)

# =====================================================================================
section("[4] delta-nu(y): fractional shape deformation = [fork prefactor] x [O(1) y-shape]")
# =====================================================================================
print(r"""
 delta-nu(y)/nu(y) = (fork prefactor) x (bounded O(1) shape function of y). The prefactor is
 the [3] number; the y-SHAPE comes from the residual W^2 relative to the tree W. The verdict
 is MAP-INDEPENDENT (fixed by the prefactor). Representative bounded interpolation (LABELED
 illustration, consistent with |W|<=1, W(0)=1 deep-MOND, W(inf)=0 Newtonian): W(y)=1/(1+y).""")
def nu_tree(y):  return mp.sqrt(1 + 1/mp.mpf(y))
def Wy(y):       return 1/(1 + mp.mpf(y))              # representative bounded W(y) (illustration)
# shape function: residual deformation of the inertia ~ d(W^2)/relative to tree d(W); take S(y)=W(y)
# (leading residual W^2 gives fractional dnu ~ prefactor*W(y), bounded in (0,1])
qq = (9.36e-11/2.998e8)/m_p_invs
prefactorC = (1.0/(16*float(sp.pi)**2))*max(qq**2,(1.808e-18/m_p_invs)**2)
print(f"\n  {'y':>8s} {'nu_tree(y)':>12s} {'W(y)':>10s} {'delta-nu/nu (Fork C)':>22s}")
for y in [1e-2, 1e-1, 1.0, 1e1, 1e3, 1e11]:
    frac = prefactorC*float(Wy(y))
    print(f"  {y:8.0e} {float(nu_tree(y)):12.5f} {float(Wy(y)):10.5f} {frac:22.3e}")
check("delta-nu(y) is a COMPUTABLE bounded shape x a prefactor; in the physical Fork C the "
      "fractional deformation is <=~1e-80 at ALL y -- the first quantum correction to the MOND "
      "interpolation exists but is unobservable", prefactorC*float(Wy(1e-2)) < 1e-78)

# =====================================================================================
section("[5] y*-ANCHOR WINDOW SPREAD + BOTH FOOTINGS")
# =====================================================================================
print(r"""
 Moving the Newtonian anchor y* within 1e10..1e13 shifts delta-nu by O(delta-nu(y*)) (second
 order in the correction), exactly parallel to the a0-footing fork. Since delta-nu(y*<=1e10)
 <=~1e-80, the anchor-systematic is ~1e-80^2 -- utterly negligible; the verdict is anchor-
 and footing-invariant.""")
spread = []
for lab,a0v,Hv in FOOT:
    qy = (a0v/c_light)/m_p_invs
    pf = (1.0/(16*float(sp.pi)**2))*max(qy**2,(Hv/m_p_invs)**2)
    dv_at_ystar = [pf*float(Wy(ys)) for ys in [1e10,1e11,1e12,1e13]]
    spread.append(max(dv_at_ystar))
    print(f"  {lab}: max delta-nu across y* window = {max(dv_at_ystar):.2e}; "
          f"anchor-systematic ~ {max(dv_at_ystar)**2:.2e}")
check("anchor-window spread and footing spread both <=~1e-80 (nothing flips; the finite D2 "
      "delta-nu is a real but structurally-unobservable channel in the physical fork)",
      all(sv < 1e-78 for sv in spread))

print(r"""
 SCHEME FLAGS: the (m^4/64pi^2)(1+sW)^2 ln(1+sW) NONANALYTIC piece is mu-INDEPENDENT
 (scheme-independent) -- its W^2 residual is the genuine prediction. The ABSORBABLE linear
 piece and the analytic mu-dependent part run into c_W (fixed by condition N) and c_WW (an
 UNPINNED Wilson coefficient, no tree counterpart -- reported, not invented). So the ONLY
 scheme-independent observable is the W^2 nonanalytic deformation, and it is (Fork C)
 unobservable / (Fork P) a statement about the proxy's domain of validity.""")
print("="*94)
print(f" D2 RESULT: {'ALL CHECKS PASS' if PASS else 'A CHECK FAILED'}")
print("="*94)
sys.exit(0 if PASS else 1)
