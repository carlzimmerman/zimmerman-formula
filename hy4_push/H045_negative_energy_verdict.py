#!/usr/bin/env python3
r"""H045 -- THE NEGATIVE ENERGY DENSITY: CROSSING, REACHABILITY, VERDICT.

THE QUESTION (H035 left it open, and it is the sharpest structural test in the
programme).

    H035 measured that on the STATIC branch the scalar's energy density is

        rho_phi = -Lam^4 f(K),    f(0) = -1,  f'(K) = mu_2(sqrt K) > 0,

    which starts at the vacuum value +Lam^4 and FALLS, going negative for
    sqrt(K) above about 1.4.  Four things have to be established:

    (a) where does rho cross zero EXACTLY?
    (b) is that region reachable -- what is K for a real galaxy, at real
        radii, on the phantom solution?
    (c) if reachable, is the theory unstable, and does that falsify it?
    (d) if NOT reachable, prove the domain restriction (a NEW consistency
        condition: physical solutions always have u < u*).

WHAT IS ESTABLISHED HERE (short version -- the numbers are below).

    (a)  u* = 1.22385628142208...   (K* = u*^2 = 1.497824...)
         The crossing is EXACTLY one: f is strictly increasing on (0,inf)
         because f'(u) = 2u*mu_2(u) > 0 there, so rho is strictly decreasing.

    (b)  REACHABLE, AND NOT MARGINALLY.  On the phantom solution the gradient
         parameter is fixed by the algebraic relation

             y(u) := u * mu_2(u) = g_N / (2 a_0)          [spherical, exact]

         so u is a strictly increasing, UNBOUNDED function of g_N.  The
         crossing u* is reached at g_N = 1.9528 a_0, i.e. at

             r* = r_M / sqrt(2 y(u*)) = 0.7157 r_M        [r_M = sqrt(GM/a_0)]

         For M_b = 6e10 Msun that is r* = 6.77 kpc: EVERY radius inside that
         has rho < 0.  The Solar System sits at u ~ 1e12.

    (c)  FATAL AS WRITTEN.  Three independent reasons, all measured below:
           C1  the gradient energy has the WRONG SIGN: P_X = -f' = -mu_2 < 0,
               so rho falls below the vacuum for EVERY K > 0 (not only beyond
               u*), the static energy functional is UNBOUNDED BELOW, and the
               perturbations on the static branch have a negative-definite
               Hamiltonian (G^{00} = -f' < 0, the opposite of a canonical
               scalar).  u* is only where the sickness becomes NEGATIVE.
           C2  H011's "no tachyon" check (S3) used rho = 2Kf' - f, the
               TIMElike-branch density, on a SPACElike branch -- it therefore
               reported d rho/dK > 0 where the branch actually has < 0.
           C3  the density gravitates (it is T^phi_00 in eq. (I)), and it
               predicts a perihelion precession of -90 arcsec/century for
               Mercury, against a residual of 0 +/- 0.04.

    (d)  NOT AVAILABLE -- AND PROVABLY SO.  y(u) = u*mu_2(u) is a strictly
         increasing bijection of [0,inf) onto [0,inf): every u >= 0 is
         realized by some radius of some spherical system.  There is NO
         domain restriction and therefore no consistency condition of the
         hoped-for kind.  This is certified in
         hy4_push/lean/H045_negative_energy.lean as `no_domain_restriction`.

Every check states measurement and threshold separately.  Both a_0 footings.
"""
import math, json
import mpmath as mp

mp.mp.dps = 40

RES, NP_, NF_ = [], 0, 0
def check(n, measured, ok, d="", thr=""):
    global NP_, NF_
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if thr: print(f"         threshold: {thr}")
    if d: print(f"         {d}")
    RES.append({"check": n, "measured": measured, "threshold": thr, "pass": ok})
    if ok: NP_ += 1
    else:  NF_ += 1
    return ok

# ---------------------------------------------------------------- constants
G    = mp.mpf('6.67430e-11')
c    = mp.mpf('2.99792458e8')
MSUN = mp.mpf('1.98892e30')
PC   = mp.mpf('3.0856775814913673e16')
KPC  = 1000*PC
H0   = mp.mpf('67.4e3')/mp.mpf('3.0856775814913673e22')
OML  = mp.mpf('0.685')
RHO_C = 3*H0**2/(8*mp.pi*G)
RHO_L = OML*RHO_C                       # kg/m^3  -- Lam^4 in mass units
LAM4  = RHO_L*c**2                      # J/m^3
FOOT  = {"canonical": mp.mpf('9.3619e-11'), "alternative": mp.mpf('1.1279e-10')}

# ------------------------------------------------------------ the functions
def mu2(u):  return 1 - 1/(1+u)**2                        # f'(K) = mu_2(sqrt K)
def f_of_u(u): return u**2 - 2*mp.log(1+u) - 2/(1+u) + 1  # f, u = sqrt(K)
def rho_st(u): return -f_of_u(u)                          # rho/Lam^4, static
def dfdK(u):  return mu2(u)                               # df/dK
def cs2(u):   return (u**2+3*u+2)/(u**2+3*u+4)            # sound speed^2
def y_map(u): return u*mu2(u)                             # = g_N/(2 a_0)
def fp_u(u):  return 2*u*mu2(u)                           # df/du  (dK/du = 2u)

def solve_u(y):
    """Invert y(u) = u*mu_2(u) = y  (strictly increasing, so unique)."""
    if y <= 0: return mp.mpf(0)
    lo, hi = mp.mpf(0), mp.mpf(max(10.0, 2*float(y)+10))
    for _ in range(300):
        mid = (lo+hi)/2
        if y_map(mid) < y: lo = mid
        else: hi = mid
    return (lo+hi)/2

print("="*78)
print("H045 -- THE NEGATIVE ENERGY DENSITY: CROSSING, REACHABILITY, VERDICT")
print("="*78)
print(f"  rho_Lambda = {mp.nstr(RHO_L,8)} kg/m^3     Lam^4 = {mp.nstr(LAM4,8)} J/m^3")
print(f"  a_0 footings: canonical {mp.nstr(FOOT['canonical'],8)}, "
      f"alternative {mp.nstr(FOOT['alternative'],8)} m/s^2")

# ================================================================ PART (a)
print("\n" + "="*78)
print("PART A -- WHERE DOES rho CROSS ZERO EXACTLY?")
print("="*78)

U_STAR = mp.findroot(f_of_u, mp.mpf('1.22'))
K_STAR = U_STAR**2
Y_STAR = y_map(U_STAR)
print(f"\n  f(u) = u^2 - 2 ln(1+u) - 2/(1+u) + 1,    rho/Lam^4 = -f(u)")
print(f"  f'(u) = 2u*mu_2(u) > 0 for u > 0   =>   f strictly increasing")
print(f"\n  u*      = {mp.nstr(U_STAR, 25)}")
print(f"  K* = u*^2 = {mp.nstr(K_STAR, 25)}")
print(f"  residual f(u*) = {mp.nstr(f_of_u(U_STAR), 5)}")
print(f"  rho(u*)/Lam^4  = {mp.nstr(rho_st(U_STAR), 5)}")

# monotonicity, measured
us = [mp.mpf(v) for v in ['1e-6','0.01','0.1','0.5','1','1.2','1.3','2','10','1e3']]
sl = [fp_u(v) for v in us]
check("A1 [ONE CROSSING] f is strictly increasing on u > 0 (f'(u) = 2u mu_2(u)),\n"
      "      f(0) = -1 and f -> +inf, so rho = -Lam^4 f crosses zero EXACTLY ONCE",
      f"df/du > 0 at all 10 sampled u in [1e-6,1e3]: "
      f"{all(s > 0 for s in sl)}; f(1e-6)={mp.nstr(f_of_u(mp.mpf('1e-6')),6)}, "
      f"f(1e3)={mp.nstr(f_of_u(mp.mpf('1e3')),6)}",
      all(s > 0 for s in sl) and f_of_u(mp.mpf('1e-6')) < 0 < f_of_u(mp.mpf('1e3')),
      "The crossing is unique. The vacuum rho = +Lam^4 is a MAXIMUM along the\n"
      "         gradient direction, not a minimum -- see Part C.",
      thr="df/du > 0 for every u > 0, and f changes sign")

print(f"\n  {'sqrt(K)':>10} {'K':>14} {'f(K)':>14} {'rho/Lam^4':>14} {'c_s^2':>10}")
for v in ['0','0.01','0.1','0.5','1.0','1.2', mp.nstr(U_STAR,8),'1.3','2.0','10']:
    u = mp.mpf(v); K = u*u
    print(f"  {mp.nstr(u,7):>10} {mp.nstr(K,7):>14} {mp.nstr(f_of_u(u),7):>14} "
          f"{mp.nstr(rho_st(u),7):>14} {mp.nstr(cs2(u),5):>10}")
check("A2 [THE CROSSING VALUE] rho = 0 at u* = 1.22385628142208 (K* = 1.497824),\n"
      "      with rho > 0 below it and rho < 0 above it",
      f"u* = {mp.nstr(U_STAR,15)}, K* = {mp.nstr(K_STAR,15)}, "
      f"rho(1.2)/Lam^4 = {mp.nstr(rho_st(mp.mpf('1.2')),6)} > 0, "
      f"rho(1.3)/Lam^4 = {mp.nstr(rho_st(mp.mpf('1.3')),6)} < 0",
      rho_st(mp.mpf('1.2')) > 0 > rho_st(mp.mpf('1.3')),
      "H035's 'about 1.4' was a two-point estimate; the true crossing is 1.2239.\n"
      "         c_s^2 stays in (1/2,1) THROUGH the crossing: the zero of rho is\n"
      "         not a change of hyperbolicity, it is a change of SIGN of the energy.",
      thr="rho changes sign exactly at u*, once")

# ================================================================ PART (b)
print("\n" + "="*78)
print("PART B -- IS IT REACHABLE?  K FOR A GALAXY ON THE PHANTOM SOLUTION")
print("="*78)
print("""
  The spherical phantom solution is the algebraic MOND relation
        mu_2(g/(2a_0)) * g = g_N,      g = |grad phi|,  u = g/(2a_0)
  i.e.  y(u) := u * mu_2(u) = g_N / (2 a_0)              (exact, spherical)
  y is strictly increasing, so u is determined by g_N, and u -> inf as g_N -> inf.
""")

rows = {}
for foot, a0 in FOOT.items():
    MB = mp.mpf('6e10')*MSUN
    rM = mp.sqrt(G*MB/a0)
    r_star = mp.sqrt(G*MB/(2*a0*Y_STAR))
    print(f"\n  --- footing {foot}: a_0 = {mp.nstr(a0,8)} m/s^2, "
          f"M_b = 6e10 Msun, r_M = {mp.nstr(rM/KPC,6)} kpc")
    print(f"      crossing radius r* = {mp.nstr(r_star/KPC,6)} kpc "
          f"= {mp.nstr(r_star/rM,6)} r_M   (g_N(r*) = {mp.nstr(2*Y_STAR,6)} a_0)")
    print(f"  {'r[kpc]':>8} {'g_N/a_0':>11} {'u=sqrt(K)':>12} {'K':>14} "
          f"{'rho/Lam^4':>13} {'rho[kg/m3]':>13} {'rho_phan':>11} {'|ratio|':>9}")
    rws = []
    for rk in ['0.1','0.5','1','2','5','8','10','20','50','100']:
        r = mp.mpf(rk)*KPC
        gN = G*MB/r**2
        u = solve_u(gN/(2*a0)); K = u*u
        rho = rho_st(u)*RHO_L
        rphan = mp.sqrt(G*MB*a0)/(4*mp.pi*G*r**2)
        ratio = abs(rho/rphan)
        rws.append((rk, gN/a0, u, K, rho_st(u), rho, rphan, ratio))
        print(f"  {rk:>8} {mp.nstr(gN/a0,6):>11} {mp.nstr(u,7):>12} {mp.nstr(K,7):>14} "
              f"{mp.nstr(rho_st(u),7):>13} {mp.nstr(rho,6):>13} "
              f"{mp.nstr(rphan,5):>11} {mp.nstr(ratio,4):>9}")
    rows[foot] = (rM, r_star, rws)
    # deep-MOND identity check: u -> r_M/(2r) as u -> 0 (asymptotic, so test
    # the CONVERGENCE, not the value at one radius)
    conv = []
    for rk in ['50', '200', '1000']:
        r = mp.mpf(rk)*KPC
        u_exact = solve_u((G*MB/r**2)/(2*a0))
        conv.append((rk, u_exact, (rM/r)/2, abs(u_exact/((rM/r)/2) - 1)))
    check(f"B1 [PHANTOM SOLUTION] the deep-MOND identity u = r_M/(2r) is the\n"
          f"      u -> 0 asymptote of the exact solve (footing {foot}): the\n"
          f"      relative deviation shrinks as r grows (it is O(u) ~ 0.74 u)",
          "; ".join(f"r={c[0]} kpc: u={mp.nstr(c[1],6)} vs {mp.nstr(c[2],6)}, "
                    f"dev={mp.nstr(c[3],4)}" for c in conv),
          all(conv[i][3] > conv[i+1][3] for i in range(len(conv)-1))
          and conv[-1][3] < mp.mpf('0.01'),
          "The calibration u = g/(2a_0) and the phantom solution are consistent:\n"
          "         u(r_M) = 0.745 and u(2 r_M) = 0.394 -- the RAR transition sits\n"
          "         at u ~ 0.4-0.7, comfortably below the crossing u* = 1.2239,\n"
          "         which is why the fits never noticed; but u -> inf inward.",
          thr="deviation decreasing in r and < 1% at r = 1000 kpc")
    neg = [w for w in rws if w[4] < 0]
    check(f"B2 [REACHED IN A GALAXY] rho < 0 somewhere inside the galaxy "
          f"(footing {foot})",
          f"rho < 0 at {len(neg)}/10 sampled radii, out to r = "
          f"{neg[-1][0] if neg else '-'} kpc; r* = {mp.nstr(r_star/KPC,5)} kpc; "
          f"rho/Lam^4 = {mp.nstr(rws[3][4],6)} at 2 kpc, "
          f"{mp.nstr(rws[0][4],6)} at 0.1 kpc",
          len(neg) > 0,
          "NOT MARGINAL: the whole inner galaxy is past the crossing. Note also\n"
          "         that |rho| stays ~1e-3-1e-4 of the phantom density at 1-10 kpc,\n"
          "         which is why this never showed up in the RAR fits -- the static\n"
          "         T_00 is dynamically irrelevant IN THE MOND REGIME.",
          thr="at least one sampled radius with rho < 0")

# ---- real systems
print("\n" + "="*78)
print("PART B2 -- REAL SYSTEMS: u, rho, AND THE ENCLOSED DEFICIT")
print("="*78)
print("  Outside a source of mass M and radius R:  g = GM/r^2, so")
print("      rho_phi ~ -Lam^4 (g/2a_0)^2 = -A/r^4,   A = Lam^4 (GM)^2/(4 a_0^2)")
print("      M_phi(r) = -4 pi A (1/R - 1/r)   -> a NEGATIVE POINT MASS at r >> R")
print(f"\n  {'system':>10} {'a_0':>10} {'u(surf)':>12} {'rho[surf] kg/m3':>17} "
      f"{'M_phi[kg]':>12} {'M_phi/M':>11}")
sysrows = []
for nm, M, R in [("Sun", MSUN, mp.mpf('6.96e8')),
                 ("Earth", mp.mpf('5.972e24'), mp.mpf('6.371e6')),
                 ("Jupiter", mp.mpf('1.898e27'), mp.mpf('6.9911e7'))]:
    for foot, a0 in FOOT.items():
        gS = G*M/R**2; uS = gS/(2*a0)
        rhoS = -f_of_u(uS)*RHO_L
        A = RHO_L*(G*M)**2/(4*a0**2)
        Mphi = -4*mp.pi*A/R
        sysrows.append((nm, foot, uS, rhoS, Mphi, Mphi/M))
        print(f"  {nm:>10} {foot[:5]:>10} {mp.nstr(uS,6):>12} "
              f"{mp.nstr(rhoS,6):>17} {mp.nstr(Mphi,6):>12} {mp.nstr(Mphi/M,5):>11}")

u_sun = sysrows[0][2]
check("B3 [REACHED, EMPHATICALLY] u exceeds u* by ~12 orders of magnitude in the\n"
      "      Solar System -- the negative-rho region is not an exotic corner",
      f"u(solar surface) = {mp.nstr(u_sun,6)} vs u* = {mp.nstr(U_STAR,8)}; "
      f"ratio = {mp.nstr(u_sun/U_STAR,5)}",
      u_sun/U_STAR > mp.mpf('1e6'),
      "Any system with g_N >~ 2 a_0 is past the crossing: the inner parts of all\n"
      "         galaxies, all stars, all planets.",
      thr="u(solar surface)/u* > 1e6")

# ================================================================ PART (c)
print("\n" + "="*78)
print("PART C -- IS IT AN INSTABILITY, OR AN ACCEPTABLE FEATURE?")
print("="*78)
print("""
  THE DIAGNOSIS.  Write the Lagrangian in the standard k-essence variable
  X = -(1/2)(dphi)^2/Lam^4*Lam^4  (so K = -X/Lam^4 on the spacelike branch):
        L = P(X),   P_X = -f'(K) = -mu_2(sqrt K) < 0.
  A canonical scalar has P_X = +1.  Ours has P_X < 0 for every K > 0.  That is
  the whole issue, and it shows up in three independent places.
""")
print(f"  {'u':>10} {'P_X = -mu_2':>14} {'drho/dK (static)':>18} "
      f"{'c_s^2':>10} {'G^{00} = -fprime':>17}")
for v in ['1e-6','0.1','0.5','1.0', mp.nstr(U_STAR,8),'2','10','1e6']:
    u = mp.mpf(v)
    # drho/dK on the static branch: rho = -f(K), d/dK = -(df/du)/(2u)
    drho = -fp_u(u)/(2*u) if u > 0 else mp.mpf(0)
    print(f"  {mp.nstr(u,7):>10} {mp.nstr(-mu2(u),7):>14} {mp.nstr(drho,7):>18} "
          f"{mp.nstr(cs2(u),5):>10} {mp.nstr(-mu2(u),7):>17}")

check("C1 [WRONG-SIGN GRADIENT ENERGY] on the branch the framework uses,\n"
      "      P_X = -f' = -mu_2 < 0 for EVERY K > 0, so rho falls below the vacuum\n"
      "      for any gradient at all -- u* is where it turns NEGATIVE, not where\n"
      "      the trouble starts",
      f"P_X = {mp.nstr(-mu2(mp.mpf('0.5')),6)} at u=0.5, "
      f"{mp.nstr(-mu2(mp.mpf('0.01')),6)} at u=0.01; "
      f"rho(0.5)/Lam^4 = {mp.nstr(rho_st(mp.mpf('0.5')),6)} < 1 = rho(0)/Lam^4",
      all(mu2(mp.mpf(v)) > 0 for v in ['0.01','0.5','1','10'])
      and rho_st(mp.mpf('0.5')) < rho_st(mp.mpf(0)),
      "A canonical scalar (f' < 0) has rho RISING with the gradient. Ours falls.\n"
      "         The vacuum K = 0 is a MAXIMUM of the static energy, not a minimum:\n"
      "         delta^2 E = -int (f'/2)|grad psi|^2 < 0.",
      thr="P_X < 0 and rho(u) < rho(0) for every u > 0")

# unbounded below
ub = [rho_st(mp.mpf(v)) for v in ['1e2','1e4','1e6','1e10']]
check("C2 [NO GROUND STATE] rho/Lam^4 -> -inf as K -> inf: the static energy\n"
      "      functional is unbounded below, so the theory has no static ground state",
      "rho/Lam^4 = " + ", ".join(mp.nstr(v,5) for v in ub) +
      " at u = 1e2, 1e4, 1e6, 1e10",
      all(ub[i] > ub[i+1] for i in range(len(ub)-1)) and ub[-1] < 0,
      "This is not fixed by restricting u < u*: it is already true at u = 0.5,\n"
      "         which is where all the successful RAR fits live.",
      thr="monotonically decreasing and diverging to -inf")

# the perturbation Hamiltonian (ghost)
print("\n  THE PERTURBATION SECTOR (why this is a ghost, not a curiosity).")
print("    Quadratic action for a perturbation psi around a static background:")
print("      L2 = (1/2) G^{mu nu} d_mu psi d_nu psi,")
print("      G^{mu nu} = f' g^{mu nu} + (f''/Lam^4) d^mu phi d^nu phi")
print("      G^{00} = -f'  (canonical scalar: -g^{mu nu}, i.e. G^{00} = +1)")
print("      H_psi  = -(1/2) f' psidot^2 - (1/2) G^{ij} d_i psi d_j psi  < 0")
G00, Hpsi = [], []
for v in ['0.01','0.5','1.0','2','10']:
    u = mp.mpf(v)
    fpp = 1/(u*(1+u)**3)                 # f''(K) = d f'/dK
    Gxx = mu2(u) + 2*u*u*fpp             # = f' + 2K f''
    G00.append(-mu2(u)); Hpsi.append((-mu2(u), -Gxx))
    print(f"      u={mp.nstr(u,4):>6}: G^00 = {mp.nstr(-mu2(u),6):>12}, "
          f"G^xx = {mp.nstr(Gxx,6):>12}, H_psi = {mp.nstr(-mu2(u)/2,6)} psidot^2 "
          f"{mp.nstr(-Gxx/2,6)} (grad psi)^2")
check("C3 [GHOST] the perturbations on the static branch have a NEGATIVE-definite\n"
      "      Hamiltonian: G^{mu nu} has the OPPOSITE signature to a canonical\n"
      "      scalar, while c_s^2 = f'/(f'+2Kf'') stays in (1/2,1)",
      f"G^00 = -f' < 0 and G^xx = f'+2Kf'' > 0 at every sampled u; "
      f"c_s^2 in ({mp.nstr(min(cs2(mp.mpf(v)) for v in ['1e-6','0.5','1','1e6']),4)},"
      f"{mp.nstr(max(cs2(mp.mpf(v)) for v in ['1e-6','0.5','1','1e6']),4)})",
      all(g < 0 for g in G00) and all(h[1] < 0 for h in Hpsi),
      "HYPERBOLICITY IS NOT HEALTH. The mode propagates (c_s^2 > 0, so H011's S2\n"
      "         is correct) but carries NEGATIVE energy, so the background can decay\n"
      "         into graviton + scalar pairs without bound.",
      thr="G^00 < 0 and G^ij > 0 (opposite of canonical)")

# H011's S3 used the wrong branch
print("\n  WHY THIS WAS MISSED: H011 check S3 ('no tachyon') differentiated")
print("    rho = 2Kf' - f, which is the TIMELIKE-branch density. The framework's")
print("    branch is SPACELIKE, where rho = -f. The two disagree in sign:")
print(f"    {'u':>8} {'d(2Kfprime-f)/dK':>20} {'d(-f)/dK':>16}")
for v in ['0.01','0.5','1','2']:
    u = mp.mpf(v)
    d_tl = mp.diff(lambda uu: 2*uu**2*mu2(uu) - f_of_u(uu), u)/(2*u)
    d_st = -fp_u(u)/(2*u)
    print(f"    {mp.nstr(u,4):>8} {mp.nstr(d_tl,7):>20} {mp.nstr(d_st,7):>16}")
check("C4 [H011 S3 USED THE WRONG BRANCH] d rho/dK > 0 is true for the timelike\n"
      "      density 2Kf'-f and FALSE for the spacelike density -f that the\n"
      "      framework actually uses -- H011's 'no tachyon' pass does not apply",
      "signs: timelike +/+/+/+ vs spacelike -/-/-/- at u = 0.01,0.5,1,2",
      all(mp.diff(lambda uu: 2*uu**2*mu2(uu)-f_of_u(uu), mp.mpf(v)) > 0
          for v in ['0.01','0.5','1','2'])
      and all(-fp_u(mp.mpf(v)) < 0 for v in ['0.01','0.5','1','2']),
      "The static configuration is ANISOTROPIC (p_r = Lam^4(f-2Kf') != p_t = Lam^4 f),\n"
      "         so H034's perfect-fluid assignment rho = 2Kf'-f, p = f is not valid\n"
      "         on it. H035 got the signs right; H034/H011 did not.",
      thr="opposite signs for the two branch densities, both computed")

# ================================================================ PART C2: gravity
print("\n" + "="*78)
print("PART C5 -- IT GRAVITATES: THE SOLAR SYSTEM TEST")
print("="*78)
print("""  T^phi_00 = rho_phi enters the Newtonian limit as
        lap Phi = 4 pi G (rho_b + rho_phi/c^2),
  so the deficit is a real, repulsive source.  With rho_phi = -A/r^4 outside
  the source, M_phi(r) = -4 pi A (1/R - 1/r): a constant NEGATIVE point mass
  (degenerate with GM) plus a NON-DEGENERATE +4 pi A/r term, i.e. an extra
  radial acceleration  dg = +beta/r^3  with beta = 4 pi G A.
  A 1/r^3 radial perturbation dg = +beta/r^3 (outward) shifts the perihelion by
        dw = -pi beta / (GM a (1-e^2))   per orbit   (retrograde).""")

a0 = FOOT["canonical"]
A_sun = RHO_L*(G*MSUN)**2/(4*a0**2)
beta  = 4*mp.pi*G*A_sun
AU    = mp.mpf('1.495978707e11')
out = []
for nm, a_m, e, norb in [("Mercury", mp.mpf('5.7909e10'), mp.mpf('0.2056'),
                          mp.mpf('415.2')),
                         ("Earth",   AU, mp.mpf('0.0167'), mp.mpf('100.0')),
                         ("Mars",    mp.mpf('2.2794e11'), mp.mpf('0.0934'),
                          mp.mpf('53.2'))]:
    dw = -mp.pi*beta/(G*MSUN*a_m*(1-e**2))           # rad / orbit
    dwcy = dw*norb*mp.mpf('206264.806')              # arcsec / century
    out.append((nm, dwcy))
    print(f"      {nm:>8}: d omega = {mp.nstr(dwcy,6):>10} arcsec/century")
dg_1au = beta/AU**3
print(f"\n      extra radial acceleration at 1 AU (non-degenerate part): "
      f"{mp.nstr(dg_1au,6)} m/s^2")
print(f"      degenerate part: d(GM)/GM = "
      f"{mp.nstr(-4*mp.pi*A_sun/mp.mpf('6.96e8')/MSUN,6)}")
print(f"      GM variation Earth->Mars (1.0 -> 1.52 AU): "
      f"{mp.nstr(4*mp.pi*A_sun*(1/AU - 1/mp.mpf('2.2794e11'))/MSUN,6)} fractional")
check("C5 [FALSIFIED BY THE SOLAR SYSTEM] the framework predicts -90\n"
      "      arcsec/century of extra Mercury perihelion precession, against an\n"
      "      observed residual of 0 +/- 0.04 arcsec/century after GR",
      f"d omega(Mercury) = {mp.nstr(out[0][1],6)} arcsec/century "
      f"(Earth {mp.nstr(out[1][1],5)}, Mars {mp.nstr(out[2][1],5)}); "
      f"dg(1 AU) = {mp.nstr(dg_1au,5)} m/s^2",
      abs(out[0][1]) > mp.mpf('1.0'),
      "THE MAGNITUDE, NOT THE SIGN, IS THE PROBLEM. Flipping the scalar's kinetic\n"
      "         sign (the unique minimal repair, L -> -Lam^4[f(K)+2], which keeps\n"
      "         f(0) = -1 and the scalar field equation but gives P_X = +mu_2 > 0)\n"
      "         gives +90 arcsec/century -- equally excluded. The framework needs\n"
      "         the scalar to SCREEN at high acceleration, and it has no such\n"
      "         mechanism: mu_2 -> 1 there, which is the opposite of decoupling.",
      thr="|d omega| > 1 arcsec/century vs bound 0.04")

# ================================================================ PART (d)
print("\n" + "="*78)
print("PART D -- IS THERE A DOMAIN RESTRICTION THAT SAVES IT?  (NO)")
print("="*78)
print("""  The hoped-for escape: physical solutions always have u < u*, so the
  negative region is unreachable.  That requires the map
        y(u) = u mu_2(u) = g_N/(2 a_0)
  to be BOUNDED above by y(u*) on the physical domain.  It is not:
""")
print(f"  {'u':>10} {'y(u) = u mu_2(u)':>18} {'y(u) - (u - 1/4)':>20}")
ys, diffs = [], []
for v in ['0','0.5','1', mp.nstr(U_STAR,8),'2','10','1e3','1e6','1e12']:
    u = mp.mpf(v); yv = y_map(u)
    ys.append(yv); diffs.append(yv - (u - mp.mpf('0.25')))
    print(f"  {mp.nstr(u,7):>10} {mp.nstr(yv,7):>18} {mp.nstr(yv-(u-mp.mpf('0.25')),7):>20}")
mono = all(ys[i] < ys[i+1] for i in range(len(ys)-1))
check("D1 [NO CEILING] y(u) = u mu_2(u) = u - u/(1+u)^2 is strictly increasing on\n"
      "      [0,inf) and UNBOUNDED: y(u) >= u - 1/4 (since 4u <= (1+u)^2), so for\n"
      "      every target u there is a radius r = sqrt(GM/(2 a_0 y(u))) that\n"
      "      realizes it.  NO domain restriction exists.",
      f"y strictly increasing over u in [0,1e12]: {mono}; "
      f"y(u) - (u-1/4) >= 0 at all sampled u: {all(d >= 0 for d in diffs)}; "
      f"y(1e12) = {mp.nstr(ys[-1],6)}",
      mono and all(d >= 0 for d in diffs),
      "This is the negative of (d): the 'new consistency condition' cannot be\n"
      "         established because the set of realized u is ALL of [0,inf).\n"
      "         Certified in Lean: `no_domain_restriction`, `y_strictMono`.",
      thr="y strictly increasing AND y(u) >= u - 1/4 for all u >= 0")
check("D2 [THE CROSSING IS ORDINARY] the crossing sits at g_N = 1.9528 a_0,\n"
      "      i.e. r = 0.7157 r_M -- INSIDE every galaxy, not at its edge",
      f"y(u*) = {mp.nstr(Y_STAR,10)} => g_N = {mp.nstr(2*Y_STAR,8)} a_0; "
      f"r* = {mp.nstr(rows['canonical'][1]/KPC,6)} kpc for 6e10 Msun "
      f"(r_M = {mp.nstr(rows['canonical'][0]/KPC,6)} kpc)",
      Y_STAR < mp.mpf('2'),
      "r* is where the RAR is still deep in its transition -- u*(r_M) = 0.74 < u*.\n"
      "         So even the 'transition radius' of the framework is below the\n"
      "         crossing, and everything interior to it is above.",
      thr="y(u*) < 2, i.e. r* > r_M/sqrt(4) = r_M/2")

# ================================================================ READING
print("\n" + "="*78)
print(f"H045 READING:  {NP_} PASS / {NF_} FAIL")
print("="*78)
print(f"""
THE NEGATIVE ENERGY DENSITY: VERDICT
------------------------------------
 (a) CROSSING      u* = {mp.nstr(U_STAR,16)}   (K* = {mp.nstr(K_STAR,16)})
                   Unique: f is strictly increasing (f' = 2u mu_2 > 0), so
                   rho = -Lam^4 f crosses zero once and only once.
                   H035's "about 1.4" -> 1.2239.

 (b) REACHABLE     YES.  On the phantom solution y(u) = u mu_2(u) = g_N/(2a_0),
                   so u >= u*  <=>  g_N >= {mp.nstr(2*Y_STAR,6)} a_0
                              <=>  r <= {mp.nstr(rows['canonical'][1]/KPC,5)} kpc
                   for M_b = 6e10 Msun (0.7157 r_M).  Solar surface: u ~ 1e12.
                   EVERY galaxy's interior, every star, every planet.

 (c) FATAL         The negative rho is the visible tip of a WRONG-SIGN gradient
                   energy: P_X = -mu_2 < 0 for every K > 0.  Consequences:
                     * rho < rho_vacuum for ANY gradient (not just u > u*);
                     * static energy unbounded below, no ground state;
                     * perturbations are ghosts (H_psi < 0) although c_s^2 > 0;
                     * it gravitates: -90 arcsec/century of Mercury perihelion
                       precession against a 0 +/- 0.04 residual.
                   H011's S3 "no tachyon" pass used the timelike-branch density
                   and does not apply to the branch the framework uses.
                   The action L = +Lam^4 f(K), K = +(1/2)(dphi)^2/Lam^4,
                   f' = mu_2 > 0  IS FALSIFIED.

 (d) NO ESCAPE     y(u) is a strictly increasing bijection [0,inf) -> [0,inf):
                   every u is realized.  There is NO domain restriction, hence
                   no new consistency condition.  (Lean: no_domain_restriction.)

WHAT SURVIVES.  The empirical spine is untouched: a_0, the shape of mu_2, the
RAR, the r^-2 phantom with coefficient 1, the seesaw -- none of them used the
static T_00 (the table shows |rho_phi| ~ 1e-3-1e-4 of the phantom density at
1-10 kpc, which is why it never mattered for the fits; H035 already separated
the dark mass from the static T_00).  What dies is THIS ACTION.
The unique minimal repair that keeps f(0) = -1 and the scalar field equation
(II) is L -> -Lam^4[f(K)+2], giving P_X = +mu_2 > 0 and rho = Lam^4(f+2) > 0.
It too predicts 90 arcsec/century, so the repair must ALSO add high-acceleration
SCREENING (K-mouflage / Vainshtein type): the calibration u = g/(2a_0) cannot
survive to g >> a_0.  That is the concrete next test.
""")

json.dump({"lane": "H045", "pass": NP_, "fail": NF_, "results": RES,
           "u_star": mp.nstr(U_STAR, 20), "K_star": mp.nstr(K_STAR, 20),
           "y_star": mp.nstr(Y_STAR, 20),
           "gN_at_crossing_over_a0": mp.nstr(2*Y_STAR, 12),
           "r_star_over_rM": mp.nstr(rows['canonical'][1]/rows['canonical'][0], 10),
           "reachable": True,
           "falsified": True,
           "reason": "P_X = -mu_2 < 0 (wrong-sign gradient energy); ghost; "
                     "solar-system precession -90 arcsec/cy vs 0+/-0.04",
           "domain_restriction_exists": False,
           "verdict": "the frozen-scalar action L = +Lam^4 f(K) is falsified; "
                      "the phenomenology survives and needs a screened parent"},
          open("/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_push/"
               "H045_results.json", "w"), indent=2)
print(json.dumps({"pass": NP_, "fail": NF_}))
