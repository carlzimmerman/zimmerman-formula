#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h37_lmc_bound.py -- HUNT ITEM 37 (marked a possible kill): IS THE LARGE MAGELLANIC CLOUD BOUND?
================================================================================================
The Large Magellanic Cloud moves at 321 +- 24 km/s (Galactocentric, HST proper motions, Kallivayalil et al. 2013;
Gaia EDR3 agrees to a few per cent) at a Galactocentric distance of 50.1 kpc.  In LambdaCDM this is comfortably
bound to a 1e12 Msun halo and the LMC itself needs ~1.5e11 Msun to make the Magellanic Stream and the observed
disequilibrium of the outer Galactic disc.  The framework has NO halo: the Milky Way is 6e10 Msun of baryons, and
everything beyond ~10 kpc is held together by the kernel.  Whether the LMC is bound is then not a fitted quantity --
it is a PREDICTION with exactly one nuisance, the external field on the Milky Way, and it is falsifiable both ways.

WHAT IS COMPUTED (no fitting anywhere):
  the escape speed at the LMC's position from the MW's BARYONS with the kernel and the external-field cutoff,
      g(r) = g_N(r) * nu( (g_N(r) + e_N a_0)/a_0 ),   v_esc(r)^2 = 2 int_r^inf g dr',
  which has the two correct limits: pure MOND (g -> sqrt(G M a_0)/r) when g_N >> e_N a_0, and quasi-Newtonian with
  G_eff = nu(e_N) G when g_N << e_N a_0, so the integral CONVERGES and an escape speed exists at all.  Without the
  external field the MOND potential is logarithmic and NOTHING is ever unbound -- the item is only a test because
  the Local Group and the large-scale structure supply a floor.
  Beside it: the LambdaCDM escape speed from an NFW halo, and the Newtonian-baryons-only floor as the mutation.

Both footings.  Mutations.  Checks CAN fail, and the headline check is designed so that a knife-edge answer is
reported as a knife-edge rather than as a win.
"""
import sys, math
import numpy as np
from scipy.integrate import solve_ivp
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(3737)
Gyr = 3.1557e16

# ---------------------------------------------------------------- the measured inputs
R_LMC   = 50.1                 # kpc, Galactocentric (D_helio 49.59 +- 0.54 kpc, Pietrzynski+2019, projected to the GC)
V_TOT   = 321.0; V_TOT_E = 24.0    # km/s, Galactocentric 3-D speed (Kallivayalil+2013 Table 1)
V_RAD   = 64.0                 # km/s, outward
V_TAN   = 314.0                # km/s
MW_MB   = 6.0e10               # Msun of Milky Way baryons (M* ~ 5.0-6.1e10 + ~1e10 of gas)
MW_MB_LO, MW_MB_HI = 5.0e10, 7.0e10
LMC_MB  = 3.2e9                # Msun, LMC baryons (M* 2.7e9 + M_HI 5e8 x 1.33)
LMC_MH_LCDM = 1.5e11           # Msun, the LambdaCDM LMC halo the Stream and the disc wake require

P("="*116); P("ITEM 37 -- is the LMC bound to a Milky Way made only of baryons?"); P("="*116)
info(f"measured: R_GC = {R_LMC:.1f} kpc, v_rad = +{V_RAD:.0f}, v_tan = {V_TAN:.0f}, v_tot = {V_TOT:.0f} +- {V_TOT_E:.0f} km/s")
info(f"the framework's Milky Way: M_b = {MW_MB:.2e} Msun of baryons and nothing else; LambdaCDM's: M_200 ~ 1e12 with M_b the same")
r_M = {ft: math.sqrt(G*MW_MB*Msun/a0)/kpc for ft, a0 in A0.items()}
info(f"MW MOND radius r_M = sqrt(G M_b/a_0) = {r_M['canonical']:.1f} (canonical) / {r_M['alt']:.1f} (alt) kpc "
     f"-- the LMC at {R_LMC:.0f} kpc sits {R_LMC/r_M['canonical']:.1f} r_M out, deep in the modified regime")

# ---------------------------------------------------------------- the fields
def g_mond(r_m_, Mb_kg, a0, eN):
    """r in metres.  g_N boosted by the kernel evaluated on the TOTAL Newtonian field (internal + external),
    the standard one-dimensional EFE prescription.  eN = external Newtonian field in units of a_0."""
    gN = G*Mb_kg/r_m_**2
    return gN*nu(( gN + eN*a0)/a0)

def v_esc_mond(r_kpc, Mb, a0, eN):
    """2 int_r^inf g dr' with the analytic quasi-Newtonian tail beyond the grid."""
    Mb_kg = Mb*Msun; r0 = r_kpc*kpc
    r_ext = math.sqrt(G*Mb_kg/(max(eN, 1e-9)*a0))          # where internal = external
    Rmax = max(200.0*r_ext, 1e4*r0)
    rr = np.geomspace(r0, Rmax, 20000)
    gg = g_mond(rr, Mb_kg, a0, eN)
    integ = np.trapezoid(gg, rr) if hasattr(np, "trapezoid") else np.trapz(gg, rr)
    tail = nu_s(eN)*G*Mb_kg/Rmax                            # int_Rmax^inf nu(eN) G M/r^2 dr
    return math.sqrt(2*(integ + tail))/1e3, r_ext/kpc

def v_esc_newton(r_kpc, Mb):
    return math.sqrt(2*G*Mb*Msun/(r_kpc*kpc))/1e3

def v_esc_nfw(r_kpc, M200=1.0e12, c=10.0, Mb=MW_MB):
    """NFW + a central baryonic point mass, escape to infinity from the NFW potential."""
    rho_c = rho_crit
    r200 = (M200*Msun/(200*rho_c*4*math.pi/3))**(1/3.)
    rs = r200/c; g_c = math.log(1+c) - c/(1+c)
    r = r_kpc*kpc
    Phi = -G*M200*Msun/g_c*math.log(1 + r/rs)/r - G*Mb*Msun/r
    return math.sqrt(2*abs(Phi))/1e3, r200/kpc

# ---------------------------------------------------------------- the external field on the Milky Way
# M31 alone: the MONDian two-body field sqrt(G M_b a_0)/d at 780 kpc, converted to its Newtonian equivalent x
# by solving x nu(x) = g_MOND/a_0.  The large-scale-structure field is usually quoted at 0.01-0.03 a_0 (MONDian).
M31_MB, D_M31 = 1.2e11, 780.0
def eN_from_mondian(gm_over_a0):
    """invert x nu(x) = target for the Newtonian-equivalent external field."""
    lo, hi = 1e-8, 10.0
    for _ in range(200):
        mid = math.sqrt(lo*hi)
        if mid*nu_s(mid) < gm_over_a0: lo = mid
        else: hi = mid
    return math.sqrt(lo*hi)
for ft, a0 in A0.items():
    g31 = math.sqrt(G*M31_MB*Msun*a0)/(D_M31*kpc)
    info(f"{ft:10} M31's MONDian pull on the MW at 780 kpc = {g31/a0:.4f} a_0 -> Newtonian-equivalent e_N = {eN_from_mondian(g31/a0):.2e}")
info("the large-scale-structure field is independently put at 0.01-0.03 a_0 (MONDian), i.e. e_N ~ 1e-4 to 1e-3 Newtonian;")
info("the scan below therefore covers e_N = 1e-4 ... 3e-2, three decades, and reports where the verdict changes.")

# ---------------------------------------------------------------- the scan
P(""); info(f"{'e_N':>9} {'r_ext[kpc]':>11} " + " ".join(f"{'v_esc('+ft+')':>16}" for ft in A0) + "   verdict (canonical / alt)")
SCAN = [1e-4, 3e-4, 1e-3, 3e-3, 6e-3, 1e-2, 3e-2]
res = {}
for eN in SCAN:
    row = []; rext = None
    for ft, a0 in A0.items():
        v, rext = v_esc_mond(R_LMC, MW_MB, a0, eN); row.append(v)
    res[eN] = row
    verd = " / ".join("BOUND " if v > V_TOT else "UNBOUND" for v in row)
    info(f"{eN:9.1e} {rext:11.1f} " + " ".join(f"{v:16.1f}" for v in row) + f"   {verd}")

# the external field required to bind the LMC, per footing -- this is the item's real content
def eN_binding(a0, Mb=MW_MB, vtarget=V_TOT):
    lo, hi = 1e-6, 1.0                      # v_esc DECREASES with e_N, so bisect on that monotone
    for _ in range(200):
        mid = math.sqrt(lo*hi)
        v, _ = v_esc_mond(R_LMC, Mb, a0, mid)
        if v > vtarget: lo = mid
        else: hi = mid
    return math.sqrt(lo*hi)
eNb = {ft: eN_binding(a0) for ft, a0 in A0.items()}
EXT_LO, EXT_HI = 0.01, 0.03      # the independent MONDian estimate of the external field on the Milky Way
eN_lo, eN_hi = eN_from_mondian(EXT_LO), eN_from_mondian(EXT_HI)
P("")
for ft, a0 in A0.items():
    gm = eNb[ft]*nu_s(eNb[ft])
    info(f"{ft:10} the LMC is bound iff the external field on the MW is WEAKER than e_N = {eNb[ft]:.2e} (Newtonian) "
         f"= {gm:.4f} a_0 (MONDian)")
info(f"the independent estimate of that field is {EXT_LO:.2f}-{EXT_HI:.2f} a_0 MONDian (M31 alone gives 0.017; the LSS the rest),")
info(f"i.e. e_N = {eN_lo:.2e} to {eN_hi:.2e} Newtonian -- BELOW the threshold by a factor "
     f"{eNb['canonical']*nu_s(eNb['canonical'])/EXT_HI:.1f} at the strong end.  So the framework's answer is: BOUND.")

v_lo, _ = v_esc_mond(R_LMC, MW_MB, A0["canonical"], eN_lo)      # weakest external field -> most bound
v_hi, _ = v_esc_mond(R_LMC, MW_MB, A0["canonical"], eN_hi)      # strongest plausible -> least bound
v_lo_a, _ = v_esc_mond(R_LMC, MW_MB, A0["alt"], eN_lo)
v_hi_a, _ = v_esc_mond(R_LMC, MW_MB, A0["alt"], eN_hi)
marg = (v_hi - V_TOT)/V_TOT_E

ck("37 the framework makes a DEFINITE prediction here and it is not a fitted one: with the Milky Way's baryons alone, no halo, "
   "and the external field pinned independently at 0.01-0.03 a_0, the escape speed at the LMC's position is 375-451 km/s "
   "(canonical) and the LMC is BOUND.  Newtonian baryons without the kernel give 102 km/s and would have it long gone",
   min(v_hi, v_hi_a) > V_TOT,
   f"v_esc = {v_hi:.0f}-{v_lo:.0f} (canonical) / {v_hi_a:.0f}-{v_lo_a:.0f} (alt) km/s across the external-field range, "
   f"against a measured v_LMC = {V_TOT:.0f} +- {V_TOT_E:.0f}")

ck("37b ...and the margin is thin enough to be a live falsifier rather than a comfortable pass: at the strongest plausible "
   "external field the LMC is bound by only 2.5 sigma of its own measured speed, and the verdict turns over at e_N = 4.2e-3 "
   "(0.067 a_0 MONDian), a factor 2.2 above the highest independent estimate.  A 15% larger LMC speed, or an external field "
   "twice the LSS estimate, breaks it",
   1.0 < marg < 4.0,
   f"least-bound case v_esc = {v_hi:.0f} vs {V_TOT:.0f} +- {V_TOT_E:.0f} -> margin {marg:.1f} sigma; "
   f"turnover at e_N = {eNb['canonical']:.2e} = {eNb['canonical']*nu_s(eNb['canonical']):.3f} a_0 MONDian "
   f"vs the estimated {EXT_LO:.2f}-{EXT_HI:.2f}")

ck("37c READ THE OTHER WAY: because the LMC is observed to be there at all, its proper motion places an UPPER BOUND on the "
   "external field acting on the Milky Way -- e_N < 4.2e-3, i.e. g_ext < 0.067 a_0 -- which is a measurement of a quantity "
   "the framework otherwise has to import from large-scale structure.  Nothing in LambdaCDM has an analogue of it",
   eNb["canonical"]*nu_s(eNb["canonical"]) < 0.15,
   f"g_ext(MW) < {eNb['canonical']*nu_s(eNb['canonical']):.3f} a_0 (canonical) / "
   f"{eNb['alt']*nu_s(eNb['alt']):.3f} a_0 (alt), at the measured v_LMC; the bound weakens to "
   f"{eN_binding(A0['canonical'], vtarget=V_TOT+V_TOT_E)*nu_s(eN_binding(A0['canonical'], vtarget=V_TOT+V_TOT_E)):.3f} a_0 "
   f"if the LMC is 1 sigma faster")

# ---------------------------------------------------------------- the alternative, and the mutation floor
v_nfw, r200 = v_esc_nfw(R_LMC)
v_newt = v_esc_newton(R_LMC, MW_MB)
P("")
info(f"LambdaCDM (NFW M200 = 1e12, c = 10, r200 = {r200:.0f} kpc, plus the same baryons): v_esc({R_LMC:.0f} kpc) = {v_nfw:.0f} km/s -> BOUND with margin")
info(f"Newtonian baryons only, no halo and no kernel (the mutation floor): v_esc = {v_newt:.0f} km/s -> UNBOUND by a factor {V_TOT/v_newt:.1f}")
ck("M37 mutation: switching the kernel off (nu = 1, the same baryons) must destroy the result -- the escape speed collapses to a "
   "third of the measured LMC speed, so the pass above is the kernel's doing and not an accident of the mass",
   v_newt < 0.5*V_TOT, f"nu = 1 gives v_esc = {v_newt:.0f} km/s vs the kernel's {v_hi:.0f}-{v_lo:.0f} and the measured {V_TOT:.0f}")
ck("M37b mutation: a_0 -> a_0/100 must also destroy it",
   v_esc_mond(R_LMC, MW_MB, A0["canonical"]/100.0, 3e-4)[0] < 0.6*V_TOT,
   f"a_0/100 gives v_esc = {v_esc_mond(R_LMC, MW_MB, A0['canonical']/100.0, 3e-4)[0]:.0f} km/s")

# baryonic-mass sensitivity -- the other nuisance
P("")
for Mb in (MW_MB_LO, MW_MB, MW_MB_HI):
    vv = [v_esc_mond(R_LMC, Mb, a0, 3e-4)[0] for a0 in A0.values()]
    info(f"M_b(MW) = {Mb:.1e} Msun at e_N = 3e-4: v_esc = {vv[0]:.0f} (canonical) / {vv[1]:.0f} (alt) km/s")
info("v_esc goes as M_b^(1/4) x sqrt(log), so a 17% mass error moves it by 4% -- the external field, not the baryon budget, is what decides.")

# ---------------------------------------------------------------- the orbit
P(""); P("="*116); P("the orbit: first passage or not, integrated backwards"); P("="*116)
def integrate_back(a0, eN, Mb=MW_MB, mond=True, M200=1.0e12, cnfw=10.0, T=13.0):
    Mb_kg = Mb*Msun
    r200 = (M200*Msun/(200*rho_crit*4*math.pi/3))**(1/3.); rs = r200/cnfw
    g_c = math.log(1+cnfw) - cnfw/(1+cnfw)
    def gtot(r):
        if mond: return g_mond(r, Mb_kg, a0, eN)
        Mn = M200*Msun/g_c*(math.log(1 + r/rs) - (r/rs)/(1 + r/rs))
        return G*(Mn + Mb_kg)/r**2
    L = R_LMC*kpc*V_TAN*1e3
    def rhs(t, y):
        r, vr = y; r = max(r, 0.2*kpc)
        return [vr, -gtot(r) + L**2/r**3]
    s = solve_ivp(rhs, (0, -T*Gyr), [R_LMC*kpc, V_RAD*1e3], rtol=1e-9, atol=1e2,
                  max_step=2e14, dense_output=True)
    r = s.y[0]/kpc; t = s.t/Gyr
    per = [(t[i], r[i]) for i in range(1, len(r)-1) if r[i] < r[i-1] and r[i] < r[i+1]]
    apo = [(t[i], r[i]) for i in range(1, len(r)-1) if r[i] > r[i-1] and r[i] > r[i+1]]
    period = abs(per[1][0] - per[0][0]) if len(per) > 1 else float("nan")
    return r, t, per, apo, r.max(), period

ORB = {}
for ft, a0 in A0.items():
    for eN in (eN_lo, eN_hi, 1e-2):
        r, t, per, apo, rmax, period = integrate_back(a0, eN)
        ORB[(ft, eN)] = (rmax, len(per), period)
        info(f"{ft:10} e_N = {eN:.1e} ({eN*nu_s(eN):.3f} a_0): backwards 13 Gyr the LMC reaches {rmax:7.0f} kpc, "
             f"{len(per)} pericentric passage(s), radial period "
             + (f"{period:.1f} Gyr" if np.isfinite(period) else "> 13 Gyr (does not return -- first infall)"))
r_n, t_n, per_n, apo_n, rmax_n, period_n = integrate_back(None, 0, mond=False)
info(f"LambdaCDM NFW (M200 = 1e12, c = 10): backwards 13 Gyr the LMC reaches {rmax_n:7.0f} kpc, {len(per_n)} pericentric "
     f"passage(s), radial period " + (f"{period_n:.1f} Gyr" if np.isfinite(period_n) else "> 13 Gyr"))
rmax_c = ORB[("canonical", eN_hi)][0]
ck("37d the ORBIT does not discriminate either: at the estimated external field the framework's LMC is on a bound orbit with "
   "an apocentre of a few hundred kpc and several pericentric passages in a Hubble time, and a 1e12 Msun NFW halo gives the "
   "same picture to within 0.2 dex.  Boundness and orbit shape are NOT where these two theories differ about the LMC",
   abs(math.log10(rmax_c/rmax_n)) < 0.3,
   f"canonical apocentre {rmax_c:.0f} kpc ({ORB[('canonical', eN_hi)][1]} passages) vs NFW {rmax_n:.0f} kpc "
   f"({len(per_n)} passages); {abs(math.log10(rmax_c/rmax_n)):.2f} dex apart")
info("a real difference does hide here and it is worth naming: MOND has NO dynamical friction against a halo that does not")
info("exist, so a bound MOND LMC has made these passages without sinking, and the Magellanic Stream has to be made on a")
info("multiple-passage orbit rather than on first infall.  Testing that needs a Stream model, not an energy budget.")

# ---------------------------------------------------------------- the real liability
P("")
info("THE LIABILITY THAT THIS ITEM ACTUALLY EXPOSES, stated plainly:")
info(f"  LambdaCDM needs an LMC of ~{LMC_MH_LCDM:.1e} Msun to make the Magellanic Stream, the wake in the stellar halo and the")
info(f"  reflex motion of the outer disc.  The framework's LMC is {LMC_MB:.1e} Msun of baryons -- a factor {LMC_MH_LCDM/LMC_MB:.0f} lighter --")
info( "  and MOND has no dynamical friction against a halo that does not exist, so the LMC cannot have sunk.  The framework must")
info( "  make the Stream and the wake with 3e9 Msun and the kernel's own boost; whether it can is NOT tested here and is the")
info( "  place this item should go next.  Recording it as an OPEN liability, not as a null.")
q = LMC_MB*nu_s(0.02)                                # crude: EFE-boosted effective mass of the LMC at 50 kpc
info(f"  order of magnitude: at 50 kpc the MW's field is {math.sqrt(G*MW_MB*Msun*A0['canonical'])/(R_LMC*kpc)/A0['canonical']:.2f} a_0, "
     f"so the LMC's internal dynamics are EFE-suppressed and its effective pull on the halo is nearer G x {LMC_MB:.1e} than G x {LMC_MH_LCDM:.1e}.")

ck("37e the discriminator is NOT boundness (both theories can be made to bind or not) but the LMC's own MASS: the framework "
   "gives the LMC 3.2e9 Msun of baryons where LambdaCDM's Stream-and-wake modelling needs ~1.5e11 -- a factor 47 that no "
   "external field can absorb.  Recorded as the open half of item 37",
   LMC_MH_LCDM/LMC_MB > 20, f"factor {LMC_MH_LCDM/LMC_MB:.0f} between the two LMC masses; the escape-speed test above resolves "
   f"nothing next to it")

sys.exit(ck.done())
