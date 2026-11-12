#!/usr/bin/env python3
"""OUT-5 (BOOTSTRAP CARRIER) -- the symbolic part.

Grades G1, G2, H1-H5 and the known answers KA1-KA5.  Writes out5_sym.out / .json.
Footings graded separately, never pooled.  Adopts nothing.  kappa = 1/2 FITTED.
"""
import json, sys, time
import sympy as sp

T0 = time.time()
OUT = {}
def P(s=""):
    print(s, flush=True)

P("=" * 78)
P("OUT-5 (BOOTSTRAP CARRIER) -- symbolic")
P("kappa = 1/2 FITTED; not theory closed.  Adopts nothing.")
P("=" * 78)

r, a0, G, R, x, v = sp.symbols('r a0 G R x v', positive=True)
g = sp.Function('g')(r)
u = g / a0

# ---------------------------------------------------------------- kernels ----
muS = u / (1 + u)                                  # law S  (kernel of action (A))
muB = (sp.sqrt(1 + 4 * u**2) - 1) / (2 * u)        # law B  (the a0-line)

KERNELS = [("S", muS, "mu = u/(1+u)  [action (A)'s kernel]"),
           ("B", muB, "mu = (sqrt(1+4u^2)-1)/(2u)  [the a0-line g^2=g_N^2+a0 g_N]")]

# ============================================================ G1 / H1 ========
P("\n--- G1 / H1: the pinning is an identity -------------------------------")
P("   Define  rho_b := (1/4piG)(1/r^2) d_r[r^2 mu g]   (the law)")
P("           rho_c := (1/4piG)(1/r^2) d_r[r^2 (1-mu) g]  (the carrier)")
P("   Claim:  rho_c = [(1-mu)/mu] rho_b + [mu' g/(4piG mu)] * partial_s g,")
P("           partial_s g := -dg/dr.   (LOCAL: rho_b, g, partial_s g at one point)")
res_G1 = {}
for nm, m, desc in KERNELS:
    jac = sp.diff(m, g)
    rho_b = sp.diff(r**2 * m * g, r) / (4 * sp.pi * G * r**2)
    rho_c = sp.diff(r**2 * (1 - m) * g, r) / (4 * sp.pi * G * r**2)
    local = ((1 - m) / m) * rho_b + (jac * g / (4 * sp.pi * G * m)) * (-sp.diff(g, r))
    res = sp.simplify(sp.expand(rho_c - local))
    res_G1[nm] = str(res)
    P(f"\n  kernel {nm}: {desc}")
    P(f"    G1 residual          = {res}")
    P(f"    (1-mu)/mu            = {sp.simplify((1-m)/m)}")
    P(f"    mu' g/mu             = {sp.simplify(sp.radsimp(jac*g/m))}")
    P(f"    pinning (local form) = {sp.simplify(local)}")
OUT["G1_residual"] = res_G1
OUT["G1_PASS"] = all(s == "0" for s in res_G1.values())
P(f"\n  G1 (identity, exact): {'PASS' if OUT['G1_PASS'] else 'FAIL'}   residuals {res_G1}")

# --------------------------------------------------------- H4: a0-free ------
P("\n--- H4: the deep-regime pinning contains no a0 -------------------------")
uu = sp.symbols('uu', positive=True)      # u = g/a0
deep = {}
for nm, mm, _desc in KERNELS:
    mm_u = mm.subs(g, uu * a0)            # mu as a function of u alone
    jac_u = sp.diff(mm_u, uu)             # d mu/du  = a0 * d mu/dg
    lim1 = sp.limit(sp.simplify((1 - mm_u) / mm_u * uu), uu, 0)   # ((1-mu)/mu)*(g/a0) -> 1
    lim2 = sp.limit(sp.simplify(jac_u * uu / mm_u), uu, 0)        # (mu' g/mu)          -> 1
    deep[nm] = (str(sp.simplify(lim1)), str(sp.simplify(lim2)))
    P(f"  kernel {nm}:  u->0 :  ((1-mu)/mu) * (g/a0) -> {sp.simplify(lim1)} ;  "
      f"(mu' g/mu) -> {sp.simplify(lim2)}")
P("  => rho_c -> (a0/g) rho_b + partial_s g /(4 pi G): the gradient term carries")
P("     NO a0, so the halo density outside the baryons is invariant under a0 -> lam a0.")
OUT["H4_deep"] = deep
OUT["H4_a0free"] = all(t[1] == "1" for t in deep.values())
P(f"  H4 (a0-free deep pinning): {'PASS' if OUT['H4_a0free'] else 'FAIL'}")

# ============================================================ G2 / H3 ========
P("\n--- G2 / H3: M_c(<R) = [(1-mu)/mu] M_b gives the law, counted once -----")
# law-S field: u_S(x) solves u^2 = y(u+1), y = 1/x^2
uS_x = (1 + sp.sqrt(1 + 4 * x**2)) / (2 * x**2)
# law-B field: u_B(x) = sqrt(1+x^2)/x^2   (from u^2 = y^2 + y, y = 1/x^2)
uB_x = sp.sqrt(1 + x**2) / x**2
res_G2 = {}
for field_nm, uu in (("S", uS_x), ("B", uB_x)):
    mS = uu / (1 + uu)
    mB = (sp.sqrt(1 + 4 * uu**2) - 1) / (2 * uu)
    XS = sp.simplify(sp.radsimp((1 - mS) / mS))
    XB = sp.simplify(sp.radsimp((1 - mB) / mB))
    # the direct ratio g/g_N - 1 = u x^2 - 1
    direct = sp.simplify(uu * x**2 - 1)
    P(f"\n  on the {field_nm}-kernel field  u(x) = {sp.simplify(uu)}")
    P(f"    [(1-mu_S)/mu_S]        = {XS}")
    P(f"    [(1-mu_B)/mu_B]        = {XB}")
    P(f"    direct  u x^2 - 1      = {direct}")
    # ---- exact check 1: the S-kernel ratio against X_S = (sqrt(1+4x^2)-1)/2
    rS = sp.simplify(XS - (sp.sqrt(1 + 4*x**2) - 1)/2)
    # ---- exact check 2 (B-kernel field only): sympy will not denest the radical, so
    #      prove the denesting in two exact steps:
    #        RAD(x) := x^8+6x^6+13x^4+12x^2+4 ;  POLY(x) := x^4+3x^2+2  (>0 for x>0)
    #        (i)  RAD - POLY^2 == 0                (exact)
    #        (ii) substituting sqrt(RAD) -> POLY in (X_B+1)^2 - (1+x^2) gives 0
    rB_sq, sq_ok = "n/a", []
    if field_nm == "B":
        RAD = x**8 + 6*x**6 + 13*x**4 + 12*x**2 + 4
        POLY = x**4 + 3*x**2 + 2
        sq_ok = [str(sp.simplify(sp.expand(RAD - POLY**2)))]
        subbed = sp.expand((XB + 1)**2 - (1 + x**2)).subs(sp.sqrt(RAD), POLY)
        rB_sq = str(sp.simplify(subbed))
    # ---- exact check 3: the matching kernel reproduces the direct ratio
    r_match = sp.simplify((XS if field_nm == "S" else XB) - direct)
    m_expr = sp.expand(((XB if field_nm == "B" else XS) + 1)**2 - (direct + 1)**2)
    if field_nm == "B":
        RAD = x**8 + 6*x**6 + 13*x**4 + 12*x**2 + 4
        POLY = x**4 + 3*x**2 + 2
        m_expr = m_expr.subs(sp.sqrt(RAD), POLY)
    r_match_sq = str(sp.simplify(m_expr))
    # ---- 60-digit numeric confirmation at 8 radii
    ref = (sp.sqrt(1+4*x**2)-1)/2 if field_nm == "S" else (sp.sqrt(1+x**2)-1)
    tgt = XS if field_nm == "S" else XB
    num = max(abs(float((tgt - ref).subs(x, sp.Float(t, 60))))
              for t in (0.5, 1, 2, 5, 10, 20, 50, 100))
    res_G2[field_nm] = dict(XS_minus_XS_ref=str(rS), XB_square=str(rB_sq),
                            perfect_square_residuals=sq_ok,
                            match_direct=str(r_match), match_direct_sq=str(r_match_sq),
                            numeric_max=float(f"{num:.3e}"))
    P(f"    X_S - (sqrt(1+4x^2)-1)/2      = {rS}")
    P(f"    radicand - (x^4+3x^2+2)^2     = {sq_ok}   (the denesting; all 0 => exact)")
    P(f"    (X_B+1)^2 - (1+x^2)           = {rB_sq}   [+ X_B+1 > 0 proves X_B = sqrt(1+x^2)-1]")
    P(f"    matched kernel - direct       = {r_match}")
    P(f"    (matched+1)^2 - (direct+1)^2  = {r_match_sq}")
    P(f"    max |numeric diff|, 60 digits, x in [0.5,100] = {num:.3e}")
OUT["G2_residual"] = res_G2
OUT["G2_PASS"] = (res_G2["S"]["XS_minus_XS_ref"] == "0"
                  and res_G2["B"]["XB_square"] == "0"
                  and res_G2["S"]["match_direct"] == "0"
                  and res_G2["B"]["match_direct_sq"] == "0"
                  and all(s == "0" for v in res_G2.values()
                          for s in v["perfect_square_residuals"])
                  and all(v["numeric_max"] < 1e-40 for v in res_G2.values()))
P(f"\n  G2 (the law, exact): {'PASS' if OUT['G2_PASS'] else 'FAIL'}")

# kernel sensitivity of the demand at FLD1's KiDS radii
P("\n  kernel sensitivity of the DEMAND (both ~ x at large x):")
for xk in (5.8888, 41.9814, 59.998, 98.3168):
    XSv = float(((sp.sqrt(1+4*x**2)-1)/2).subs(x, xk))
    XBv = float((sp.sqrt(1+x**2)-1).subs(x, xk))
    P(f"    x = {xk:9.4f}:  X_S {XSv:8.3f}   X_B {XBv:8.3f}   ratio {XBv/XSv:6.4f}")
OUT["kernel_sensitivity"] = {str(xk): float((sp.sqrt(1+x**2)-1).subs(x,xk)
                                            / ((sp.sqrt(1+4*x**2)-1)/2).subs(x,xk))
                             for xk in (5.8888, 41.9814, 59.998, 98.3168)}

# ============================================================ H5 ============
P("\n--- H5: universality ---------------------------------------------------")
P("  (a) the PINNING at fixed x:  partial_s g = a0 u'(x)/r_M  ∝  a0/v_flat^2")
P("      so rho_pin ∝ v_flat^-2, which is exactly the law's demand scaling")
P("      (M_b ∝ v_flat^4 from v_flat^4 = G M_b a0;  rho_c = M_b X'/(4 pi r^2 r_M)")
def mono_exponent(expr, sym):
    """exponent of a monomial in `sym` (via the log-derivative; exact for monomials)"""
    return sp.simplify(sp.diff(sp.log(sp.simplify(expr)), sym) * sym)

vv, rr, aa = sp.symbols('v_v r_r a_a', positive=True)
# pinned density in the deep regime: rho = v^2/(4 pi G r^2), r = x v^2/a0
rho_pin_sym = sp.simplify(vv**2/(4*sp.pi*G*(x*vv**2/aa)**2))
# demanded density: M_b X'/(4 pi r^2 r_M),  M_b = v^4/(G a0),  r_M = v^2/a0,  X' -> 1 deep
rho_dem_sym = sp.simplify((vv**4/(G*aa))/(4*sp.pi*(x*vv**2/aa)**2*(vv**2/aa)))
ratio = sp.simplify(rho_dem_sym/rho_pin_sym)
P(f"      rho_pin(deep) = {rho_pin_sym}   ->  v_flat^{mono_exponent(rho_pin_sym, vv)}")
P(f"      rho_demand    = {rho_dem_sym}   ->  v_flat^{mono_exponent(rho_dem_sym, vv)}")
P(f"      ratio (demand/pinning) = {ratio}  <- a constant: UNIVERSAL")
OUT["H5_pinning_exponent"] = str(mono_exponent(rho_pin_sym, vv))
OUT["H5_demand_exponent"] = str(mono_exponent(rho_dem_sym, vv))
OUT["H5_ratio"] = str(ratio)
OUT["H5_PASS"] = (str(mono_exponent(rho_pin_sym, vv)) == str(mono_exponent(rho_dem_sym, vv))
                  and sp.simplify(sp.diff(ratio, vv)) == 0)
P(f"      H5(a) (universal scaling): {'PASS' if OUT['H5_PASS'] else 'FAIL'}")

P("\n  (b) the SOURCE route:  S = A(tau) F(u,w),  w := Q-1 ~ -Phi/c^2,  w=0 on FRW")
P("      at fixed x: u is kernel-fixed (no galaxy dependence); w ∝ v_flat^2/c^2")
p, q = sp.symbols('p q', integer=True)
vv2 = sp.symbols('V', positive=True)     # v_flat^2
# F ~ u^p w^q  ->  S ∝ (v^2)^{q}   (u^p is x-only)
S_src = vv2**q
S_law = vv2**(-1)                        # law's requirement
P(f"      S_source ∝ (v_flat^2)^{q} ;  S_law ∝ (v_flat^2)^(-1)")
P(f"      profile needs p = 2 (so S ∝ r^-2); amplitude needs q = -1")
P(f"      => p + q = 1, with p >= 0 and q >= 0 required for regularity at (u,w)=(0,0).")
P(f"      Regularity  =>  q >= 0  =>  S ∝ v_flat^(2*{q}) with 2*{q} >= 0, versus -2 required.")
P(f"      The unique monomial that matches is F ∝ u^2/(Q-1): IRREGULAR (blows up as w -> 0).")
OUT["H5_source_needed_q"] = -1
OUT["H5_source_regular_q_min"] = 0
P("      This is VCC1's V5e (eps = 2c^2/v_flat^2, 5.62x spread) as an exact statement.")

# ============================================================ KA ============
P("\n--- known answers ------------------------------------------------------")
KA = {}
# KA1 sqrt(M_sun a0/G) in Msun/kpc
Msun, kpc = sp.Float('1.98847e30'), sp.Float('3.085677581e19')
Gsi = sp.Float('6.674e-11')
for nm, av in (("canonical", sp.Float('9.3603e-11')), ("alt", sp.Float('1.1312e-10'))):
    KA["KA1_" + nm] = float(sp.sqrt(Msun * av / Gsi) / (Msun / kpc))
P(f"  KA1 sqrt(M_sun a0/G): canonical {KA['KA1_canonical']:.1f}, alt {KA['KA1_alt']:.1f} Msun/kpc "
  f"(LFS1 KA4: 25914.5)")
# KA2 mu_K for w(1/3401) = 0.01
a_, I0, mK = sp.symbols('a_ I0 mu_K', positive=True)
w0 = I0/(4*mK**2)
wa = w0/(w0 + a_**3)
sol = [s for s in sp.solve(sp.Eq(wa.subs(a_, sp.Rational(1,3401)), sp.Rational(1,100)), mK)]
KA["KA2_symbolic"] = str(sp.nsimplify(sol[0]))
KA["KA2_value"] = float(sol[0].subs(I0, sp.Float('4.037e-8')))
P(f"  KA2 mu_K solving w(1/3401)=0.01: {KA['KA2_symbolic']} = {KA['KA2_value']:.3f} /Mpc "
  f"(MK1 KA7 / KD1 B1a: 198.254 / 198.245)")
# KA3 r_M
for nm, av in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    row = []
    for lmb in (9.4, 10.45, 10.7, 10.9):
        Mb = 10**lmb * 1.98847e30
        row.append(float(sp.sqrt(Gsi*Mb/sp.Float(av)).evalf()/kpc))
    KA["KA3_" + nm] = row
P(f"  KA3 r_M canonical: {['%.3f'%t for t in KA['KA3_canonical']]} kpc (FLD1: 1.934/6.479/8.640/10.877)")
P(f"  KA3 r_M alt      : {['%.3f'%t for t in KA['KA3_alt']]} kpc")
# KA4 deep pinned density == (1/4pi r^2) dM_c/dr  -- an ASYMPTOTIC identity: report the
# relative difference and its 1/x^2 fall-off.
xs_ = sp.symbols('xs_', positive=True)
Mc = sp.Rational(1,2)*(sp.sqrt(1+4*xs_**2)-1)        # in units of M_b, x = r/r_M
rho_from_Mc = sp.diff(Mc, xs_)/(4*sp.pi*xs_**2)      # in units of M_b/r_M^3
rho_from_pin = 1/(4*sp.pi*xs_**2)                    # v_flat^2/(4piG r^2), same units
rel = sp.simplify((rho_from_pin - rho_from_Mc)/rho_from_Mc)
KA["KA4_rel"] = {str(t): float(rel.subs(xs_, sp.Float(t, 40))) for t in (1, 3, 10, 30, 100)}
KA["KA4_series"] = str(sp.series(rel, xs_, sp.oo, 4))
P(f"  KA4 deep rho_pin vs (1/4pi r^2) dM_c/dr  (relative difference):")
for k, v in KA["KA4_rel"].items():
    P(f"      x = {k:>5}: {v:+.4e}")
P(f"      series at x -> oo: {KA['KA4_series']}")
P(f"      (asymptotic: the deep-regime pinning converges to the exact derivative as 1/x^2)")
# KA5 mu_K^match independence
Rmax = sp.symbols('Rmax', positive=True)
mk_match = 1/(r*sp.sqrt(sp.log(Rmax/r)))
P(f"  KA5 mu_K^match(r) = {mk_match}   -- no M_b, no a0, no kernel: exact")
KA["KA5_expr"] = str(mk_match)
OUT["KA"] = KA

# ============================================================ H6 ============
P("\n--- H6: T4 / LFS1 evasion ----------------------------------------------")
P("  T4  : the carrier's charge is rho_c, a distinct variable with its own current;")
P("        it is not D_m[(1+gamma_L Pi_+) P^m]/Q.  The pinning is keyed to g, which")
P("        does NOT vanish on a free-fall boundary (P = 0 there, g != 0), so T4's")
P("        boundary premise has no purchase on it.  [structural + G1]")
P("  LFS1: static clock -- the clock's charge moves by Y dX ~ |Phi|/c^2 ~ 1e-6;")
P("        the carrier's moves at d ln C/dt = d ln M_b/dt (ratio +1).")
OUT["H6_LFS1_ratio_carrier"] = 1.0
OUT["H6_LFS1_ratio_clock"] = [-5.0e-6, -1.0e-8]      # LFS1 A1, measured
P(f"        carrier ratio +1  against LFS1 A1's allowed/demanded {OUT['H6_LFS1_ratio_clock']}")
P(f"        => LFS1's A1 is turned from FAIL to PASS by 2e5 to 1e8.")

OUT["runtime_s"] = round(time.time() - T0, 2)
P(f"\nG1 PASS {OUT['G1_PASS']}   G2 PASS {OUT['G2_PASS']}   H4 PASS {OUT['H4_a0free']}")
P(f"runtime {OUT['runtime_s']} s")
with open("out5_sym.json", "w") as f:
    json.dump(OUT, f, indent=1, default=str)
P("wrote out5_sym.json")
