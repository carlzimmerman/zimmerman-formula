#!/usr/bin/env python3
"""
L155 -- does a DISFORMAL matter coupling built from the clock's foliation normal cure the
gamma = 1 - 2f disease of the conformally coupled MOND scalar (L135) without breaking c_T or alpha_1?

Branch: GR + cuscuton clock (foliation normal n_mu, shift-independent) + MOND scalar phi with
matter metric   gt_{mu nu} = A^2(phi) [ g_{mu nu} + B(phi) n_mu n_nu ],   A = e^{alpha phi}.
Conventions follow L134/L135:  f = G_s/G_N = fifth-force fraction felt by slow orbits,
G_N the measured constant, a0t = a0/f the scale in the action.  Everything is checked
symbolically (sympy) or with explicit numbers; no check uses a literal True.

Parts: A static cure (gamma, f, B explicit) | A2 exact beta and the grad-phi variant |
       B tensor speed c_T vs GW170817 | C preferred-frame alpha_1, alpha_2, alpha_3 |
       D perihelion + the pincer + verdict.
"""
import sympy as sp
import numpy as np

NPASS = NFAIL = 0
def check(label, cond, detail=""):
    global NPASS, NFAIL
    cond = bool(cond)
    NPASS += cond; NFAIL += (not cond)
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}")
    if detail:
        print(f"           ({detail})")
def hdr(s):
    print("\n" + "=" * 100 + "\n" + s + "\n" + "=" * 100)

# constants (SI)
G_SI = 6.674e-11; M_SUN = 1.989e30; AU = 1.496e11; C = 2.998e8
KPC = 3.086e19
A0_FOOTINGS = {"repo canonical 9.36e-11": 9.36e-11, "repo alt 1.13e-10": 1.13e-10}
CASSINI = 2.3e-5          # |gamma - 1|
GW_LO, GW_HI = -3e-15, 7e-16   # c_T/c - 1 (GW170817 / GRB170817A)
ALPHA1_BOUND = 4e-5       # Will 2014 (pulsar / LLR)
ALPHA2_BOUND = 4e-7       # Will 2014 (solar spin alignment)
PERI_GATE = 1e-3          # arcsec / century (L135 gate)

# ------------------------------------------------------------------------------------------------
hdr("PART A -- STATIC WEAK FIELD: effective G for light vs slow orbits under gt = A^2 [g + B n n]")
# ------------------------------------------------------------------------------------------------
al, U, phi, xd, eps = sp.symbols('alpha U phi x_d epsilon', real=True)
# Einstein-frame O(2) metric of a static source (G_* units, U = G_* M / r):  N^2 = 1 - 2U, gamma_ij = (1+2U) d_ij
N2 = 1 - 2*U; gam = 1 + 2*U
A2 = sp.exp(2*al*phi)
# general B(phi) with B(0)=0, B'(0) = 4 alpha x_d  (x_d = 0 pure conformal, x_d = 1 the TeVeS-type cure)
Bp = 4*al*xd
B = Bp*phi
# foliation at rest: n_mu = (-N, 0,0,0)  ->  n_mu n_nu has only the 00 component = N^2
gt00 = A2*(-N2 + B*N2)
gtij = A2*gam
# scalar charge of a static particle: S_m = -m int sqrt(-gt_00) dt  =>  a_T = d/dphi sqrt(-gt_00)|_{phi=0,U=0}
aT = sp.simplify(sp.diff(sp.sqrt(-gt00), phi).subs({phi: 0, U: 0}))
aS = sp.simplify(sp.diff(sp.sqrt(gtij), phi).subs({phi: 0, U: 0}))     # spatial (conformal) coupling
print(f"  a_T (temporal coupling, sources phi) = {aT}     a_S (spatial coupling) = {aS}")
check("A1  the disformal term flips the TEMPORAL coupling only: a_T = alpha(1 - 2 x_d), a_S = alpha",
      sp.simplify(aT - al*(1 - 2*xd)) == 0 and sp.simplify(aS - al) == 0)
# scalar solution (Newtonian branch, L134 normalisation): phi = -a_T U
phi_sol = -aT*U
lin = lambda e: sp.series(sp.simplify(e.subs(phi, phi_sol)), U, 0, 2).removeO()
Phit = sp.expand(-(lin(gt00) + 1)/2)      # gt_00 = -(1 + 2 Phit)  -> slow orbits feel Phit
Psit = sp.expand(-(lin(gtij) - 1)/2)      # gt_ij = (1 - 2 Psit)   -> light feels Phit + Psit
GN_over_Gs = sp.simplify(-Phit/U)         # G_N / G_*
gamma_ppn = sp.simplify(Psit/Phit)
f_frac = sp.simplify(aT**2/(1 + aT**2))   # G_s/G_N
print(f"  G_N/G_* = {GN_over_Gs}    gamma = {sp.factor(gamma_ppn)}    f = {f_frac}")
check("A2  x_d = 0 reproduces L135 exactly: G_N = G_*(1+alpha^2), gamma = (1-alpha^2)/(1+alpha^2), gamma-1 = -2f",
      sp.simplify(gamma_ppn.subs(xd, 0) - (1 - al**2)/(1 + al**2)) == 0 and
      sp.simplify((gamma_ppn - 1 + 2*f_frac).subs(xd, 0)) == 0)
roots = sp.solve(sp.numer(sp.together(gamma_ppn - 1)), xd)
print(f"  gamma = 1  <=>  x_d in {roots}")
check("A3  gamma = 1 has exactly two roots: x_d = 1/2 (a_T = 0: scalar DECOUPLES, f = 0, no MOND) and "
      "x_d = 1 (the TeVeS-type cure: a_T = -a_S)", sorted(roots) == [sp.Rational(1, 2), 1])
check("A4  at x_d = 1 the fifth-force fraction is UNCHANGED, f = alpha^2/(1+alpha^2): the cure keeps the MOND "
      "coupling (a0t = a0/f lock untouched) while restoring gamma = 1 for EVERY f",
      sp.simplify(f_frac.subs(xd, 1) - al**2/(1 + al**2)) == 0 and sp.simplify(gamma_ppn.subs(xd, 1) - 1) == 0)
# the exact B: A^2 (1 - B) = A^{-2}  <=>  B = 1 - A^{-4}
Bex = 1 - sp.exp(-4*al*phi)
check("A5  the exact cure is B(phi) = 1 - A^{-4}(phi) = 1 - e^{-4 alpha phi}: a function of phi ALONE (not a "
      "constant, not a function of local acceleration); its linearisation is B' = 4 alpha, i.e. x_d = 1",
      sp.simplify(sp.diff(Bex, phi).subs(phi, 0) - 4*al) == 0 and
      sp.simplify(A2*(1 - Bex) - sp.exp(-2*al*phi)) == 0)
B0 = sp.symbols('B0', real=True)
aT_const = sp.diff(sp.sqrt(-A2*(-N2 + B0*N2)), phi).subs({phi: 0, U: 0})
check("A6  a CONSTANT B cannot cure: with B = B0 the matter metric is -(1-B0) A^2 N^2 dt^2 + A^2 gamma_ij, i.e. the "
      "pure conformal case in a rescaled time unit (a_T/sqrt(1-B0) = alpha), so gamma stays at its x_d = 0 value",
      sp.simplify(aT_const/sp.sqrt(1 - B0) - al) == 0)

# ------------------------------------------------------------------------------------------------
hdr("PART A2 -- EXACT beta for the cured coupling (JNW exterior, L134 map) and the grad-phi variant")
# ------------------------------------------------------------------------------------------------
rho, b, s_, k = sp.symbols('rho b s k', positive=True)
# L134: Einstein exterior ds^2 = -f^s dt^2 + ..., phi = k ln f, f = ((1 - b/4rho)/(1 + b/4rho))^2 in isotropic rho.
fJ = ((1 - b/(4*rho))/(1 + b/(4*rho)))**2
phiJ = k*sp.log(fJ)
# cured matter metric: gt_00 = -A^{-2} f^s  (exact, from A^2(1-B) = A^{-2})
gt00_ex = -sp.exp(-2*al*phiJ)*fJ**s_
ser = sp.series(gt00_ex, b, 0, 3).removeO()
c1 = sp.simplify(ser.coeff(b, 1)*rho); c2 = sp.simplify(ser.coeff(b, 2)*rho**2)
# PPN: gt_00 = -1 + 2 Ut - 2 beta Ut^2  with Ut = c1 b/(2 rho)  =>  beta = -c2 / (2 (c1/2)^2) ... i.e. c2 = -2 beta (c1/2)^2
beta_ex = sp.simplify(-c2/(2*(c1/2)**2))
print(f"  gt_00 = -1 + ({c1}) b/rho + ({c2}) b^2/rho^2 + ...   =>  beta = {beta_ex}")
check("A2-1  beta = 1 EXACTLY for the cured exponential coupling, for every JNW exponent s and scalar charge k "
      "(ln f has no b^2 term, L134 C4), so the cure does not re-open the beta gate", sp.simplify(beta_ex - 1) == 0)
# grad-phi variant: gt = A^2 [ g + Bg dphi dphi ]  -- static phi has only a radial gradient
Bg, r_, m_ = sp.symbols('B_g r m', positive=True)
phis = -al*m_/r_
gt00_g = -A2.subs(phi, phis)*(1 - 2*m_/r_)                                   # untouched by the variant
gtrr_g = A2.subs(phi, phis)*((1 + 2*m_/r_) + Bg*sp.diff(phis, r_)**2)
gtth_g = A2.subs(phi, phis)*(1 + 2*m_/r_)
c00 = sp.simplify(sp.series(gt00_g, m_, 0, 2).removeO().coeff(m_, 1)*r_)
crr = sp.simplify(sp.series(gtrr_g, m_, 0, 2).removeO().coeff(m_, 1)*r_)
cth = sp.simplify(sp.series(gtth_g, m_, 0, 2).removeO().coeff(m_, 1)*r_)
extra = sp.simplify(gtrr_g - gtth_g)
check("A2-2  the grad-phi variant leaves gt_00 untouched (static phi is spacelike, dphi_0 = 0) and adds only "
      "B_g phi'^2 ~ 1/r^4 to g_rr: the 1/r light-orbit split (2f) is NOT touched at O(U), so it cannot cure gamma",
      sp.simplify(c00 - 2*(1 + al**2)) == 0 and sp.simplify(crr - cth) == 0 and
      sp.simplify(extra*r_**4/(Bg*al**2*m_**2) - sp.exp(2*al*phis)) == 0,
      f"O(U) coefficients: gt_00 {c00}, gt_rr {crr}, gt_thth {cth}; anisotropic extra = {extra}")

# ------------------------------------------------------------------------------------------------
hdr("PART B -- TENSOR SPEED: gravitons propagate on g, photons on gt = A^2 [g + B n n]")
# ------------------------------------------------------------------------------------------------
# Tensor kinetic term: the clock action  int [mu_c^2 sqrt(h) - N sqrt(h) V]  and the scalar action  F(h^{ij} d_i phi d_j phi)
# contain h_ij only through sqrt(h) and h^{ij} -- NO derivatives of h_ij.  So neither adds to the graviton kinetic
# operator; the tensor mode is GR's, with c_T = 1 on the light cone of g.  Check the algebra on a TT perturbation:
hTT, kk, om = sp.symbols('h k omega', real=True)
# sqrt(det(delta_ij + h_ij)) for a TT mode h_xy = h_yx = h:  det = 1 - h^2  -> no (d h)^2 term at all
det_TT = sp.det(sp.Matrix([[1, hTT, 0], [hTT, 1, 0], [0, 0, 1]]))
check("B1  the clock's only h_ij dependence is sqrt(h): on a TT mode det = 1 - h^2, no gradient of h appears, so the "
      "clock does not modify the tensor kinetic operator (nor does phi's leaf-projected h^{ij} d phi d phi)",
      sp.simplify(det_TT - (1 - hTT**2)) == 0)
# Light cone of gt: gt_00 = -A^2 (1 - B) N^2,  gt_ij = A^2 gamma_ij  (foliation at rest)  ->  c_gamma^2 = (1 - B) c_T^2
Bsym = sp.symbols('B', real=True)
c_gam_over_cT = sp.sqrt((1 - Bsym))
ratio_cure = sp.simplify(c_gam_over_cT.subs(Bsym, Bex))
check("B2  photon speed / graviton speed = sqrt(1 - B); with the cure B = 1 - A^{-4} this is EXACTLY A^{-2} = e^{-2 alpha phi}: "
      "the SAME factor that flips the temporal coupling is the factor by which the two cones split",
      sp.simplify(ratio_cure - sp.exp(-2*al*phi)) == 0)
# c_T/c - 1 = e^{2 alpha phi} - 1 ~ 2 alpha phi.  With the cure a_T = -alpha, so alpha phi = -(a_T phi) = -Phi_s,
# Phi_s = the scalar's own contribution to the potential (in c^2 units).  => c_T/c - 1 = -2 Phi_s  (f-INDEPENDENT).
Phis = sp.symbols('Phi_s', real=True)
cT_shift = sp.series(sp.exp(2*al*phi) - 1, phi, 0, 2).removeO().subs(phi, -Phis/al)
check("B3  c_T/c - 1 = -2 Phi_s to first order, where Phi_s = a_T phi is the scalar's share of the potential: for "
      "the full cure the tensor-speed shift is locked to the scalar's local potential with NO free coefficient",
      sp.simplify(cT_shift + 2*Phis) == 0)

# --- the number: Phi_s of the Milky Way at the Sun, from the branch's own MOND kernel (exp, L134/L135) --------------
def g_mond_exp(gN, a0):
    """solve mu(g/a0) g = gN, mu(y) = 1 - e^{-y}  (kernel conjugate to the branch's AQUAL F)"""
    g = np.sqrt(gN*a0) + gN
    for _ in range(200):
        y = g/a0; mu = -np.expm1(-y); dmu = np.exp(-y)
        F = mu*g - gN; dF = mu + g*dmu/a0
        g = g - F/dF
    return g
def Phi_s_MW(f, a0, Mb=6e10*M_SUN, R0=8.2*KPC, rout=1e3*KPC, n=4000):
    """scalar potential depth between the Sun and r_out (c^2 units); g_s = g_MOND - (1-f) g_N (L135 decomposition)"""
    r = np.geomspace(R0, rout, n)
    gN = G_SI*Mb/r**2
    gs = g_mond_exp(gN, a0) - (1 - f)*gN
    return np.trapz(gs, r)/C**2
print("\n  Phi_s(Sun) - Phi_s(r_out) of the Milky Way (M_b = 6e10 Msun point mass beyond R0 = 8.2 kpc; the MOND")
print("  phantom potential is the dominant, f-independent part):")
print(f"  {'a0 footing':26s} {'f':>8s} {'r_out':>9s} {'Phi_s/c^2':>12s} {'c_T/c-1':>12s} {'over GW bound':>14s}")
worst = None
for name, a0 in A0_FOOTINGS.items():
    for f in (1.0, 1e-1, 1.2e-3):
        for rout_kpc in (100.0, 1000.0):
            P = Phi_s_MW(f, a0, rout=rout_kpc*KPC)
            shift = -2*P
            over = abs(shift)/abs(GW_LO)
            worst = over if worst is None else min(worst, over)
            print(f"  {name:26s} {f:8.1e} {rout_kpc:7.0f}kpc {P:12.3e} {shift:12.3e} {over:14.2e}x")
check("B4  *** KILL: for the full cure |c_T/c - 1| = 2 Phi_s(MW) >~ 1e-6 on BOTH a0 footings, for every f and "
      "already inside 100 kpc -- against |c_T/c - 1| < 3e-15 (GW170817): at least ~1e8-1e9 over, f-INDEPENDENT ***",
      worst > 1e7, f"smallest violation factor over all rows = {worst:.2e}")
# a partial cure x_d < 1 trades gamma for c_T: at fixed f (kernel floor) show the budget
print("\n  Partial cure at fixed a_T^2 = f/(1-f) (f = 1.2e-3, the kernel-independent Saturn floor of L135), Phi_s = 1e-6:")
f0 = 1.2e-3; aT2 = f0/(1 - f0); PhiS = 1e-6
print(f"  {'x_d':>12s} {'|gamma-1|':>12s} {'Cassini?':>9s} {'|c_T/c-1|':>12s} {'GW?':>5s}")
both_ok = 0
for x in (0.0, 0.5 + 1e-3, 0.9, 0.99, 0.999, 1 - 1e-6, 1 - 1e-9, 1.0):
    # a_T fixed by f; a_S = a_T/(1-2x)  (from a_T = a_S (1-2x));  gamma from Part A
    aTv = -np.sqrt(aT2); aSv = aTv/(1 - 2*x)
    g1 = abs(1 - (1 - aSv*aTv)/(1 + aTv**2))
    # B = B' phi = 4 a_S x phi, phi = Phi_s/a_T  ->  |c_T/c - 1| = |B|/2 = 2 x |a_S/a_T| Phi_s
    ct = 2*x*abs(aSv/aTv)*PhiS
    ok = (g1 < CASSINI) and (ct < abs(GW_LO)); both_ok += ok
    print(f"  {x:12.9f} {g1:12.3e} {'yes' if g1 < CASSINI else 'no':>9s} {ct:12.3e} {'yes' if ct < abs(GW_LO) else 'no':>5s}")
check("B5  no partial cure passes both gates at the kernel floor: curing gamma to Cassini needs x_d = 1 to 2%, "
      "which pins |c_T/c - 1| at 2 Phi_s ~ 1e-6; keeping c_T within 3e-15 needs x_d < ~1e-9, i.e. no cure",
      both_ok == 0, f"rows passing both = {both_ok}")

# ------------------------------------------------------------------------------------------------
hdr("PART C -- PREFERRED FRAME: PPN frame moving at velocity w relative to the foliation (alpha_1, alpha_2, alpha_3)")
# ------------------------------------------------------------------------------------------------
print("  Idealisation (as in L127): foliation rigid = cosmic rest frame; Einstein-frame metric = GR (T^phi_0i = 0,")
print("  T^phi_00 = O(U^2)); source at rest in PPN coordinates; w along x.  All O(w^2 U) and O(w U) terms in gt kept.")
x, y, z, w, m = sp.symbols('x y z w m', real=True)
r = sp.sqrt(x**2 + y**2 + z**2)
gw = 1/sp.sqrt(1 - w**2)
n_lo = sp.Matrix([-gw, gw*w, 0, 0])                       # n_mu = -d_mu tau/|d tau|,  tau = gw (t - w x)
eta = sp.diag(-1, 1, 1, 1)
check("C1  n_mu is unit timelike for every w: eta^{mu nu} n_mu n_nu = -1",
      sp.simplify((n_lo.T*eta*n_lo)[0] + 1) == 0)
# scalar charge in the moving frame: a_T,eff = d/dphi sqrt(-gt_00) at phi = U = 0, with gt_00 = A^2(g_00 + B n_0^2)
gt00_w = A2*((-1 + 2*U) + B*n_lo[0]**2)
aT_eff = sp.simplify(sp.diff(sp.sqrt(-gt00_w), phi).subs({phi: 0, U: 0}))
print(f"  a_T,eff(w) = {aT_eff}")
# leaf-projected scalar: (gw^2 d_x^2 + d_y^2 + d_z^2) phi = 4 pi G_* a_T,eff rho  (h^{ij} = delta^{ij} + n^i n^j)
rc = sp.sqrt(x**2/gw**2 + y**2 + z**2)
phi_w = -aT_eff*m/(gw*rc)
pde = sp.simplify(gw**2*sp.diff(phi_w, x, 2) + sp.diff(phi_w, y, 2) + sp.diff(phi_w, z, 2))
check("C2  phi = -a_T,eff m/(gw r_c), r_c^2 = x^2/gw^2 + y^2 + z^2, solves the leaf Laplacian away from the source",
      pde == 0)
xi = sp.symbols('xi', real=True)
check("C3  normalisation: under x = gw xi the operator becomes isotropic and the source delta^3 picks up 1/gw, so the "
      "charge is a_T,eff/gw -- phi(x = gw xi) is the Coulomb potential of charge a_T,eff/gw",
      sp.simplify(phi_w.subs(x, gw*xi) + (aT_eff/gw)*m/sp.sqrt(xi**2 + y**2 + z**2)) == 0)
# independent cross-check: distance ON THE LEAF between the field point and the source, via an explicit boost
t = sp.symbols('t', real=True)
tl = gw*(t - w*x); xl = gw*(x - w*t)            # leaf coords of the field point (t, x, y, z)
ts = t - w*x                                    # source (at x=0) is on the same leaf when gw*ts = tl
xl_src = gw*(0 - w*ts)
check("C4  Lorentz cross-check: |x_leaf - x_leaf,src|^2 = x^2/gw^2 + y^2 + z^2 exactly (leaf distance is w-contracted)",
      sp.simplify((xl - xl_src)**2 - x**2/gw**2) == 0)
# matter metric to first order in (phi, U), exact in w, then series to O(w^2)
gt00_full = sp.expand((1 + 2*al*phi)*((-1 + 2*U) + Bp*phi*n_lo[0]**2))
gt0x_full = sp.expand((1 + 2*al*phi)*(0 + Bp*phi*n_lo[0]*n_lo[1]))
gt0y_full = sp.expand((1 + 2*al*phi)*(0 + Bp*phi*n_lo[0]*n_lo[2]))
lin1 = lambda e: sum(term for term in sp.Add.make_args(sp.expand(e)) if sp.degree(term, phi) + sp.degree(term, U) <= 1)
g00 = lin1(gt00_full).subs({phi: phi_w, U: m/r})
g0x = lin1(gt0x_full).subs({phi: phi_w, U: m/r})
g0y = lin1(gt0y_full).subs({phi: phi_w, U: m/r})
g00_s = sp.expand(sp.series(g00, w, 0, 3).removeO())
g0x_s = sp.expand(sp.series(g0x, w, 0, 2).removeO())
g0y_s = sp.expand(sp.series(g0y, w, 0, 2).removeO())
aT0 = aT_eff.subs(w, 0)
GNfac = 1 + aT0**2                                  # U_N = GNfac * U_*
check("C5  the w = 0 part of gt_00 is -1 + 2 U_N with U_N = (1 + a_T^2) U_*: the Part-A static result is recovered",
      sp.simplify(g00_s.coeff(w, 0) - (-1 + 2*GNfac*m/r)) == 0)
# read the PPN coefficients (in U_N units):  g_00 ⊃ c_w2U w^2 U_N + c_ij w^i w^j U_N,ij ;  g_0x ⊃ c_wU w U_N + c_wUij w^j U_N,xj
w2part = sp.simplify(g00_s.coeff(w, 2)*r/(GNfac*m))            # = c_w2U + c_ij x^2/r^2
c_w2U = sp.simplify(w2part.subs(x, 0)); c_ij = sp.simplify((w2part - c_w2U)*r**2/x**2)
wpart = sp.simplify(g0x_s.coeff(w, 1)*r/(GNfac*m))             # = c_wU + c_wUij x^2/r^2
c_wU = sp.simplify(wpart.subs(x, 0)); c_wUij = sp.simplify((wpart - c_wU)*r**2/x**2)
c_wUij_y = sp.simplify(g0y_s.coeff(w, 1)*r**3/(GNfac*m*x*y)) if g0y_s != 0 else 0
check("C6  the O(w^2 U) part of gt_00 has exactly the PPN form w^2 U + w^i w^j U_ij (no other angular structure), "
      "and g_0y carries the same w^j U_ij coefficient as g_0x", sp.simplify(w2part - c_w2U - c_ij*x**2/r**2) == 0
      and sp.simplify(wpart - c_wU - c_wUij*x**2/r**2) == 0 and sp.simplify(c_wUij - c_wUij_y) == 0)
# gauge-invariant extraction (t -> t + lambda w^j chi_,j shifts c_wU and c_wUij oppositely; their SUM is invariant)
alpha2 = c_ij
alpha1 = -2*(c_wU + c_wUij)
alpha3 = sp.simplify(alpha1 - alpha2 - c_w2U)
fsym = sp.simplify(aT0**2/(1 + aT0**2))
print(f"  alpha_2 = {sp.factor(alpha2)}   alpha_1 = {sp.factor(alpha1)}   alpha_3 = {alpha3}   (f = {fsym})")
for name, xv in (("pure conformal (x_d = 0)", 0), ("full cure (x_d = 1)", 1)):
    print(f"    {name:26s}: alpha_1 = {sp.factor(alpha1.subs(xd, xv))},  alpha_2 = {sp.factor(alpha2.subs(xd, xv))},"
          f"  alpha_3 = {sp.simplify(alpha3.subs(xd, xv))}")
check("C7  CONSISTENCY: alpha_3 = 0 identically (Lagrangian-based theory), for every alpha and x_d -- the three "
      "independent coefficients (w^2 U, w^i w^j U_ij, and the invariant g_0i sum) close on a conservative PPN metric",
      alpha3 == 0)
check("C8  the leaf-projected (instantaneous) scalar carries alpha_2 = f for EVERY x_d, B or no B: the potential of "
      "a source moving through the leaves is contracted along w (C4), giving a w^i w^j U_ij term in gt_00 through A^2(phi)",
      sp.simplify(alpha2 - fsym) == 0)
check("C9  the disformal term makes the matter metric depend on the foliation velocity: gt_0i = -A^2 B gw^2 w_i = "
      "-4 f U w_i for the cure, so alpha_1 = 8 f x_d (2 x_d - 1)/(...) -> 8 f at x_d = 1 (0 at x_d = 0)",
      sp.simplify(alpha1.subs(xd, 1) - 8*fsym.subs(xd, 1)) == 0 and sp.simplify(alpha1.subs(xd, 0)) == 0)
print("  NOTE (ADM sense): n_mu = (-N,0,0,0) has no shift, so gt_00 = A^2[-N^2(1-B) + N_i N^i]: the clock stays exactly")
print("  shift-independent.  alpha_1 arises not from N^i but from B n_mu n_nu tilting with the foliation velocity.")
print("  CAVEAT (rigid foliation): with the cure, matter sources the cuscuton constraint through T~^{0i} ~ B rho w, and")
print("  phi's leaf projection sources it at O(w (grad phi)^2), against a stiffness mu_c^2 ~ M_pl^2 H^2.  The exact")
print("  alpha values above are conditional on L127's rigid-foliation idealisation; that back-reaction is UNDETERMINED here.")

# ------------------------------------------------------------------------------------------------
hdr("PART D -- PERIHELION AFTER THE CURE, THE PINCER IN f, VERDICT")
# ------------------------------------------------------------------------------------------------
# With beta = gamma = 1 restored, the only orbital anomaly left is the kernel's own tail (L135):
#   g_s = f g_N / mu(y),  y = g_s/a0t ~ f^2 g_N/a0,  dg/g_N = f/expm1(y)  (exp kernel);  near-circular apsidal
#   precession per orbit  = -pi r d(eps)/dr,  eps = dg/g_N.
def eps_tail(r, f, a0):
    """solve the kernel equation mu(y) y a0t = f g_N, mu = 1 - e^{-y}, a0t = a0/f  (L135), then dg/g_N = f/(e^y - 1)"""
    gN = G_SI*M_SUN/r**2; s = f*f*gN/a0
    yv = max(np.sqrt(s), s)
    for _ in range(100):
        e = np.exp(-min(yv, 700.0)); F = (1 - e)*yv - s; dF = (1 - e) + yv*e
        yv = yv - F/dF
        yv = max(yv, 1e-300)
    return f/np.expm1(yv) if yv < 700 else 0.0
def precession_arcsec_cy(a_AU, P_yr, f, a0):
    h = 1e-4; a = a_AU*AU
    de = (eps_tail(a*np.exp(h), f, a0) - eps_tail(a*np.exp(-h), f, a0))/(2*h)     # r d eps/dr
    return abs(-np.pi*de)*(180/np.pi*3600)*(100.0/P_yr)
print(f"  {'a0 footing':26s} {'f':>9s} {'Saturn ''/cy':>14s} {'Mercury ''/cy':>14s}  verdict(1 mas/cy)")
f_floor = {}
for name, a0 in A0_FOOTINGS.items():
    fs = np.geomspace(1e-7, 1, 3000); ok = [precession_arcsec_cy(9.537, 29.46, f, a0) < PERI_GATE and
                                             precession_arcsec_cy(0.387, 0.2408, f, a0) < PERI_GATE for f in fs]
    # smallest f above which the gate is passed for all larger f
    idx = len(fs) - 1
    while idx > 0 and ok[idx - 1]:
        idx -= 1
    f_floor[name] = fs[idx]
    for f in (1.0, 1e-1, 1e-2, 6.1e-3, 1e-3, 1.15e-5, 4e-7):
        pS = precession_arcsec_cy(9.537, 29.46, f, a0); pM = precession_arcsec_cy(0.387, 0.2408, f, a0)
        print(f"  {name:26s} {f:9.2e} {pS:14.3e} {pM:14.3e}  {'PASS' if max(pS, pM) < PERI_GATE else 'FAIL'}")
    print(f"  {name:26s} perihelion floor f >= {f_floor[name]:.3e}")
check("D1  after the cure (gamma = beta = 1) Saturn+Mercury pass the 1 mas/cy gate for f >~ 6e-3 on both footings "
      "(same floor as L135 P4-5: the cure removes gamma, it does not move the kernel tail)",
      all(4e-3 < v < 1e-2 for v in f_floor.values()), "; ".join(f"{k}: {v:.3e}" for k, v in f_floor.items()))
# the pincer: ceilings from the preferred-frame parameters (Part C), floors from the tail
f_cap_a2 = ALPHA2_BOUND            # alpha_2 = f  (both cases)
f_cap_a1 = ALPHA1_BOUND/8          # alpha_1 = 8 f (cure)
f_cap_gamma_nocure = CASSINI/2     # L135
print("\n  gate                                   ceiling on f     floor on f")
print(f"  gamma (Cassini), NO cure               {f_cap_gamma_nocure:12.3e}")
print(f"  gamma (Cassini), full cure             {1.0:12.3e}   (removed)")
print(f"  alpha_2 = f  < {ALPHA2_BOUND:.0e} (any x_d)         {f_cap_a2:12.3e}")
print(f"  alpha_1 = 8f < {ALPHA1_BOUND:.0e} (cure)           {f_cap_a1:12.3e}")
for name in A0_FOOTINGS:
    print(f"  Saturn+Mercury perihelion, {name:24s}                  {f_floor[name]:12.3e}")
print(f"  PPN validity at Saturn (L135 P2-3)                       {7.43e-3:12.3e}")
gap_cure = min(f_floor.values())/min(f_cap_a1, f_cap_a2)
gap_nocure = min(f_floor.values())/min(f_cap_gamma_nocure, f_cap_a2)
check("D2  *** THE WINDOW IS EMPTY WITH THE CURE: alpha_2 = f caps f at 4e-7 (alpha_1 = 8f at 5e-6), the perihelion "
      "floors it at ~6e-3: gap >~ 1e4 (rigid-foliation idealisation) ***", gap_cure > 1e3,
      f"floor/ceiling = {gap_cure:.2e} (cure), {gap_nocure:.2e} (no cure; L135 had 529 from gamma alone)")
check("D3  the c_T kill (Part B) needs no PPN assumption at all: it is set by the Galaxy's MOND potential and the "
      "GW170817 path, independent of f, of the kernel and of the foliation's rigidity",
      worst > 1e7 and abs(float(cT_shift.subs(Phis, 1e-6))) > 1e3*abs(GW_LO))

hdr("VERDICT")
print("""  NO.  No B closes the light/orbit split without violating c_T:
   (a) the unique cure is B = 1 - A^{-4}(phi) (function of phi alone, x_d = 1): gamma = 1, beta = 1, f untouched;
       a constant B is a unit choice; a B(X) tracking acceleration would have to scale as M^{1/2} X^{1/4} (source-dependent).
   (b) it makes photons ride A^2[g + B n n] while gravitons ride g: c_T/c - 1 = -2 Phi_s = -(1-3)e-6 from the
       Milky Way's own MOND potential, ~1e9 x the GW170817 bound, for every f -- the amount that cures gamma IS the
       amount that splits the cones (partial cures: Cassini needs x_d = 1 to 2%, GW needs x_d < 2e-9).
   (c) no new N^i dependence, but B n n tilts with the foliation velocity: alpha_1 = 8f (cure);  and the leaf-
       projected scalar carries alpha_2 = f with or without B (rigid-foliation idealisation, alpha_3 = 0 verified).
   (d) perihelion passes only for f >~ 6e-3 (both footings) -- against alpha_2/alpha_1 ceilings 4e-7 / 5e-6.
  The conformally (or disformally) coupled MOND scalar is DEAD in the Solar System.  Structural change required:
  matter and gravitons must share ONE metric (no A(phi), no B), so the MOND boost must enter the gravitational
  field equations linearly -- a kinetic mixing of phi with the metric potential (AeST-type Phi = Phi_N + phi from
  the field equations, not from the matter coupling).  That is the L139 architecture, with its own alpha_1 debt.""")
print(f"\n  CHECKS: {NPASS} PASS, {NFAIL} FAIL")
