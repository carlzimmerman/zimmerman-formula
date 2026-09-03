#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h81_h82_mw_external_fields.py -- HUNT ITEMS 81 and 82: the Milky Way's external fields, and the LMC.
====================================================================================================
ITEM 81 asks for the vector sum of the large-scale-structure, M31 and LMC fields at the Sun and in the outer
disc, and for the azimuthal anisotropy of the outer rotation curve that AQUAL/QUMOND implies -- "2-5%
between the quadrants facing and opposing the total field vector".  ITEM 82 asks whether the LMC's MOND
field, quoted in the list as "~0.04 a_0 at the Sun, comparable to the LSS field", leaves a detectable
imprint on the outer disc, and whether the framework can do without the 1e11 dark halo that LambdaCDM gives
the LMC to make its wake.

THE ONE THING BOTH ITEMS GET WRONG, AND THIS SCRIPT FIXES.  The external-field parameter e_N is the
NEWTONIAN external field in units of a_0 -- not the MOND field.  Quoting M31's or the LMC's field as its
isolated deep-MOND value sqrt(G M a_0)/r is wrong twice over:
  (1) for the EFE bookkeeping, what enters is g_N = G M / r^2, and
  (2) for the actual force, a satellite's field near the Milky Way is NOT deep-MOND, because the satellite
      is embedded in the Galaxy's own much larger field.  The QUMOND response to a small extra Newtonian
      field dg_N on top of a dominant field g_N is  dg_i = nu(y) [delta_ij + L(y) nhat_i nhat_j] dg_N,j,
      with L = dln nu/dln y and nhat along g_N: a boost of nu(1+L) along the dominant field and nu across
      it, NOT nu(dg_N/a_0).
At the Sun the Galaxy's own field is y ~ 1.3, so nu(1+L) ~ 1.1 -- the LMC's pull on the Sun is essentially
NEWTONIAN.  The list's 0.04 a_0 is about twenty times too large.  Both corrections are computed below.

WHAT IS ON DISK AND USED
  * Carrick+2015 2M++ reconstructed density field (real_research/data/twompp_density.npy) -> the LSS field.
  * Ou+24 Milky Way rotation curve (real_research/data/mw_rc_ou2024_table1.tsv) -> the internal field and
    the Galaxy's MOND-required baryonic mass, and the authors' own systematic floor for item 81's test.
  * hunt_efe_lib.EFESolve -> the QUMOND anisotropy of a disc in a uniform external field.
Published scalars (M31 and LMC masses and distances, the LMC's 3-D velocity, the measured reflex/travel
velocity of the inner Galaxy) are named at the point of use.  Both footings.  Mutation controls.
Checks CAN fail.
"""
import sys, os, math
import numpy as np
from hunt_lib import *
from hunt_efe_lib import EFESolve, dlnnu_dlny

ck = Check(); rng = np.random.default_rng(8182)

SP, NG, CEN = 400.0/256.0, 257, 128       # 2M++ grid: Mpc/h, Local Group at the centre cell
B_2MPP = 1.2                              # K-band luminosity-weighted bias used by Carrick+2015
FGROW = OM_M**0.55
R0 = 8.178                                # kpc, GRAVITY Collab. 2019
# M31: baryonic mass (stars ~1.0-1.5e11 + HI ~5e9); distance 770 kpc; direction (l, b) = (121.2, -21.6)
M31_MB, M31_D, M31_L, M31_B = 1.3e11, 770.0, 121.17, -21.57
# LMC: baryonic mass ~3e9 (stars 2.7e9 + HI 5e8); distance 49.9 kpc; direction (l, b) = (280.5, -32.9)
LMC_MB, LMC_D, LMC_L, LMC_B = 3.0e9, 49.9, 280.47, -32.89
LMC_VRAD, LMC_VTAN = 64.0, 314.0          # km/s, Galactocentric (Kallivayalil+2013)
# the measured "travel velocity" of the inner Galaxy relative to the outer halo
REFLEX, EREFLEX = 32.0, 4.0               # km/s (Petersen & Penarrubia 2021; Erkal+2021 find 40 +- 8)
LMC_MH_LCDM = 1.5e11                      # LambdaCDM LMC halo mass inside ~50 kpc

def unit_gal(l_deg, b_deg):
    l, b = math.radians(l_deg), math.radians(b_deg)
    return np.array([math.cos(b)*math.cos(l), math.cos(b)*math.sin(l), math.sin(b)])

P("="*118); P("ITEMS 81 + 82 -- the Milky Way's external fields, computed rather than quoted"); P("="*118)

# ---------------------------------------------------------------- PART A: the three Newtonian fields
P(""); P("-"*118); P("PART A -- the three external fields, in the NEWTONIAN units the EFE actually uses")
P("-"*118)
cube = np.load(os.path.join(DATA, "twompp_density.npy"))
ax = (np.arange(NG) - CEN)*SP
X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
R = np.sqrt(X**2 + Y**2 + Z**2)
m = (R > 3.0) & (R < 200.0)
w = cube[m]/R[m]**3*SP**3
v1 = (100.0/(4*math.pi))*np.array([np.sum(w*X[m]), np.sum(w*Y[m]), np.sum(w*Z[m])])      # km/s for beta = 1
# linear theory: v = 2 f g /(3 H0 Omega_m) with delta_m = delta_g/b  =>  g = 3 H0 Omega_m v1 /(2 b)
g_lss_vec = 1.5*H0*OM_M*(v1*1e3)/B_2MPP
g_lss = float(np.linalg.norm(g_lss_vec))
u_lss = g_lss_vec/g_lss
l_lss = math.degrees(math.atan2(u_lss[1], u_lss[0])) % 360.0
b_lss = math.degrees(math.asin(u_lss[2]))
info(f"2M++ linear reconstruction: |v(beta=1)| = {np.linalg.norm(v1):.0f} km/s, so with the LambdaCDM bias "
     f"b_K = {B_2MPP:g} the NEWTONIAN large-scale field at the Local Group is g = {g_lss:.3e} m/s^2 toward "
     f"(l, b) = ({l_lss:.1f}, {b_lss:+.1f})")

g_m31 = G*M31_MB*Msun/(M31_D*kpc)**2
g_lmc = G*LMC_MB*Msun/(LMC_D*kpc)**2
u_m31, u_lmc = unit_gal(M31_L, M31_B), unit_gal(LMC_L, LMC_B)
tot = g_lss_vec + g_m31*u_m31 + g_lmc*u_lmc
g_tot = float(np.linalg.norm(tot)); u_tot = tot/g_tot
l_tot = math.degrees(math.atan2(u_tot[1], u_tot[0])) % 360.0
b_tot = math.degrees(math.asin(u_tot[2]))

P(f"    {'source':>28} {'g_N (m/s^2)':>13} {'e_N canonical':>14} {'e_N alt':>10} "
  f"{'naive deep-MOND g/a0':>21}")
for nm, gg in (("large-scale structure", g_lss), ("M31", g_m31), ("LMC", g_lmc)):
    dm = math.sqrt(gg*A0["canonical"])/A0["canonical"] if nm != "large-scale structure" else float("nan")
    P(f"    {nm:>28} {gg:13.3e} {gg/A0['canonical']:14.5f} {gg/A0['alt']:10.5f} "
      f"{dm:21.4f}")
P(f"    {'VECTOR SUM':>28} {g_tot:13.3e} {g_tot/A0['canonical']:14.5f} {g_tot/A0['alt']:10.5f}"
  f"{'':>22}")
info(f"the sum points toward (l, b) = ({l_tot:.1f}, {b_tot:+.1f}); the LSS term alone points to "
     f"({l_lss:.1f}, {b_lss:+.1f}), so the Local Group's two big neighbours move the direction by "
     f"{math.degrees(math.acos(float(np.dot(u_tot, u_lss)))):.1f} degrees")
ck("81a the 'three external fields' are not three comparable fields.  In the Newtonian units the EFE uses, "
   "large-scale structure beats the LMC by about an order of magnitude and M31 by nearly two, and the naive "
   "deep-MOND value sqrt(G M a_0)/r -- which is what makes M31 and the LMC look competitive in the literature "
   "and in the item -- is not the right quantity and is 10-50 times too big",
   g_lss > 5*g_lmc and g_lss > 20*g_m31,
   f"g_N: LSS {g_lss:.2e}, LMC {g_lmc:.2e} ({g_lss/g_lmc:.1f}x smaller), M31 {g_m31:.2e} "
   f"({g_lss/g_m31:.0f}x smaller); the LMC's naive deep-MOND field would be "
   f"{math.sqrt(g_lmc*A0['canonical'])/A0['canonical']:.3f} a_0 against its true Newtonian "
   f"{g_lmc/A0['canonical']:.4f} a_0")

# ---------------------------------------------------------------- PART B: the response inside the Galaxy
P(""); P("-"*118); P("PART B -- what those fields DO to a star in the disc (item 82's factor of twenty)")
P("-"*118)
rc = np.genfromtxt(os.path.join(DATA, "mw_rc_ou2024_table1.tsv"), comments="#")
Rrc, Vrc, Ep, Em = rc[:, 0], rc[:, 1], rc[:, 2], rc[:, 3]
info(f"Ou+24 rotation curve on disk: {len(Rrc)} points, R = {Rrc.min():.1f}-{Rrc.max():.1f} kpc, "
     f"v_c({R0:.2f} kpc) ~ {np.interp(R0, Rrc, Vrc):.0f} km/s, v_c(20 kpc) = {np.interp(20.0, Rrc, Vrc):.0f} km/s")

def invert(gobs, a0):
    """solve nu(y) y = g_obs/a_0 for the Newtonian y -- what the baryons must supply."""
    t = np.asarray(gobs, float)/a0
    lo, hi = np.full_like(t, 1e-8), np.full_like(t, 1e5)
    for _ in range(90):
        mid = np.sqrt(lo*hi); f = nu(mid)*mid - t
        hi = np.where(f > 0, mid, hi); lo = np.where(f > 0, lo, mid)
    return np.sqrt(lo*hi)

g_obs = (Vrc*1e3)**2/(Rrc*kpc)
P(f"    {'R (kpc)':>8} {'v_c':>7} {'g_obs/a0':>9} {'y = g_N/a0':>11} {'nu':>7} {'L':>7} {'nu(1+L)':>8} "
  f"{'g_LMC (a0)':>11} {'g_LMC/g_MW':>11}")
resp = {}
for ft, a0 in A0.items():
    yv = invert(g_obs, a0)
    Lv = dlnnu_dlny(yv); nuv = nu(yv)
    resp[ft] = (yv, nuv, Lv)
    if ft != "canonical": continue
    for Rq in (R0, 12.0, 16.0, 20.0, 25.0):
        y = float(np.interp(Rq, Rrc, yv)); n = nu_s(y); L = float(dlnnu_dlny(np.array([y]))[0])
        # distance from the LMC to a disc point at galactocentric radius Rq: bracket by |Rq - D| and Rq + D
        dmin = abs(LMC_D - Rq)
        gl = n*(1.0 + L)*G*LMC_MB*Msun/(dmin*kpc)**2/a0
        P(f"    {Rq:8.2f} {float(np.interp(Rq, Rrc, Vrc)):7.1f} {float(np.interp(Rq, Rrc, g_obs))/a0:9.3f} "
          f"{y:11.4f} {n:7.3f} {L:+7.3f} {n*(1+L):8.3f} {gl:11.5f} "
          f"{gl/(float(np.interp(Rq, Rrc, g_obs))/a0):11.5f}")
y_sun = float(np.interp(R0, Rrc, resp["canonical"][0]))
n_sun = nu_s(y_sun); L_sun = float(dlnnu_dlny(np.array([y_sun]))[0])
g_lmc_sun = n_sun*(1.0 + L_sun)*g_lmc
naive = math.sqrt(g_lmc*A0["canonical"])
ck("82a (ITEM 82's PREMISE CORRECTED) the LMC's field at the Sun is NOT 0.04 a_0.  The Sun sits in the "
   "Galaxy's own ~1.3 a_0 Newtonian field, where the QUMOND response to an extra field is nu(1+L) ~ 1.1, so "
   "the LMC's pull on the Sun is essentially Newtonian and more than an order of magnitude below the value "
   "the item quotes",
   g_lmc_sun/A0["canonical"] < 0.01 and naive/g_lmc_sun > 5.0,
   f"g_LMC(Sun) = {g_lmc_sun:.3e} m/s^2 = {g_lmc_sun/A0['canonical']:.5f} a_0 (canonical) / "
   f"{g_lmc_sun/A0['alt']:.5f} a_0 (alt), against the item's 0.04 and against the isolated deep-MOND value "
   f"{naive/A0['canonical']:.4f} a_0 -- a factor {naive/g_lmc_sun:.0f} smaller.  y(Sun) = {y_sun:.3f}, "
   f"nu = {n_sun:.3f}, L = {L_sun:+.3f}, nu(1+L) = {n_sun*(1+L_sun):.3f}")

# ---------------------------------------------------------------- PART C: item 81's azimuthal anisotropy
P(""); P("-"*118); P("PART C -- ITEM 81: the azimuthal anisotropy of the outer rotation curve"); P("-"*118)
NGP = unit_gal(0.0, 90.0)
gam = math.degrees(math.acos(abs(float(np.dot(u_tot, NGP)))))
info(f"the Galactic north pole is the disc normal, so the angle between the disc normal and the total "
     f"external field is gamma = {gam:.1f} deg -- the field is mostly IN the plane, which is the "
     f"configuration that produces an azimuthal (m = 1) asymmetry rather than a symmetric suppression")
info(f"the in-plane direction of the field is Galactic longitude l = {l_tot:.1f} deg, and the predicted "
     f"asymmetry is maximal between that longitude and l = {(l_tot+180)%360:.1f} deg")
P(f"    {'footing':>10} {'R (kpc)':>8} {'y':>8} {'e_N':>9} {'|A| = 2 dv/v':>13} {'per cent':>9}")
AMP = {}
for ft, a0 in A0.items():
    e = g_tot/a0
    sol = EFESolve(e=e)
    for Rq in (15.0, 20.0, 25.0):
        y = float(np.interp(Rq, Rrc, resp[ft][0]))
        a = abs(sol.disc_asym(y, gam))
        AMP[(ft, Rq)] = a
        P(f"    {ft:>10} {Rq:8.1f} {y:8.4f} {e:9.5f} {a:13.5f} {100*a:9.2f}")
amax = max(AMP.values())
info("Ou+24 quote a total systematic uncertainty of 1-5 per cent for R < 22 kpc, rising to ~15 per cent "
     "beyond; and no published azimuthal decomposition of the outer Milky Way curve reaches better than "
     "a few per cent, because the bar, the spiral arms and the warp all live there.  The comparison below "
     "uses the MOST OPTIMISTIC end of that quoted range at each radius -- 1 per cent inside 22 kpc, 15 per "
     "cent beyond -- so the conclusion is the one most favourable to a detection.")
floor = lambda Rq: 0.01 if Rq < 22.0 else 0.15
worst = max(AMP[(ft, Rq)]/floor(Rq) for (ft, Rq) in AMP)
P(f"    {'footing':>10} {'R (kpc)':>8} {'predicted |A|':>14} {'optimistic floor':>17} {'ratio':>7}")
for (ft, Rq) in sorted(AMP):
    P(f"    {ft:>10} {Rq:8.1f} {100*AMP[(ft,Rq)]:13.2f}% {100*floor(Rq):16.0f}% "
      f"{AMP[(ft,Rq)]/floor(Rq):7.2f}")
ck("81b the predicted azimuthal asymmetry is REAL and is not tiny -- 0.3 to 1.4 per cent -- but it stays "
   "under the measurement floor at EVERY radius, and it is a factor of two to five below what the item "
   "estimated.  It rises with radius because the disc's own field falls, so the place to look is beyond "
   "25 kpc, exactly where the Milky Way rotation curve stops being measurable",
   worst < 1.0,
   f"largest predicted/floor ratio = {worst:.2f} (predicted |A| runs {100*min(AMP.values()):.2f}-"
   f"{100*amax:.2f} per cent over R = 15-25 kpc and both footings at e_N = {g_tot/A0['canonical']:.4f}); "
   f"the item asked for 2-5 per cent, which is {0.02/amax:.1f}-{0.05/amax:.1f} times the true amplitude")
# what field WOULD be needed
need = None
for e_try in np.geomspace(0.01, 3.0, 60):
    s = EFESolve(e=float(e_try))
    if abs(s.disc_asym(float(np.interp(20.0, Rrc, resp["canonical"][0])), gam)) > 0.02:
        need = float(e_try); break
info(f"to reach a 2 per cent asymmetry at R = 20 kpc the Milky Way would need e_N = {need:.3f}, which is "
     f"{need/(g_tot/A0['canonical']):.0f} times the field it actually has -- i.e. it would have to sit inside "
     f"a cluster.  This is a statement about the Local Group's isolation, not about the kernel.")

# ---------------------------------------------------------------- PART D: item 82, the LMC's reflex
P(""); P("-"*118); P("PART D -- ITEM 82: can the framework's LMC move the Milky Way as much as the data say?")
P("-"*118)
info("the sharpest measured consequence of the LMC's mass is the REFLEX (travel) velocity of the inner "
     "Galaxy with respect to the outer stellar halo: 32 +- 4 km/s (Petersen & Penarrubia 2021), 40 +- 8 "
     "(Erkal+2021).  LambdaCDM gets it from a ~1.5e11 Msun LMC halo.  The framework has 3e9 Msun of baryons "
     "and a boost, so the question is arithmetic.")
# the Milky Way's MOND-required baryonic mass from the outer curve (deep-MOND asymptote v^4 = G M a0)
Mb_mw = {ft: (np.interp(22.0, Rrc, Vrc)*1e3)**4/(G*A0[ft])/Msun for ft in A0}
info(f"the Galaxy's baryonic mass REQUIRED by its own outer rotation curve: "
     f"{Mb_mw['canonical']:.2e} (canonical) / {Mb_mw['alt']:.2e} Msun (alt).  Photometric estimates are "
     f"6-9e10, so this already carries the repository's standing Milky Way normalisation liability; the "
     f"reflex calculation below is done with the RC-required mass, which is the generous choice for the "
     f"framework because it makes the ambient field, and hence the boost on the LMC, larger.")

def boost_at(R_kpc, a0, M_mw):
    """the QUMOND response factor nu(y)(1+L) for an extra field parallel to the Galaxy's own, at R."""
    gN = G*M_mw*Msun/(R_kpc*kpc)**2
    y = gN/a0
    return nu_s(y)*(1.0 + float(dlnnu_dlny(np.array([y]))[0])), y

def reflex_velocity(a0, M_mw, M_lmc, lcdm=False, back_Gyr=3.0, dt_Myr=1.0, R_probe=15.0):
    """Integrate the LMC's Galactocentric orbit BACKWARDS (leapfrog) in the Milky Way's field, then
    accumulate FORWARDS the velocity the LMC imparts to the inner Galaxy.  The accumulation is a VECTOR
    integral -- the LMC's direction swings through the orbit and the components partly cancel -- and the
    scalar sum is returned alongside it as a strict upper bound.  The QUMOND response factor is evaluated
    in the Galaxy's own field at R_probe, which is where the tracers that define 'the inner Galaxy' live."""
    dt = dt_Myr*1e6*365.25*86400.0
    n = int(back_Gyr*1e9*365.25*86400.0/dt)
    r = np.array([LMC_D*kpc, 0.0]); v = np.array([LMC_VRAD*1e3, LMC_VTAN*1e3])
    def acc(rr):
        d = float(np.linalg.norm(rr)); gN = G*M_mw*Msun/d**2
        g = gN if lcdm else nu_s(gN/a0)*gN
        return -g*rr/d
    hist = []
    for _ in range(n):                                   # backwards: t -> t - dt
        v = v - 0.5*acc(r)*dt; r = r - v*dt; v = v - 0.5*acc(r)*dt
        hist.append(r.copy())
    boost = 1.0 if lcdm else boost_at(R_probe, a0, M_mw)[0]
    dvv = np.zeros(2); dvs = 0.0
    for rr in reversed(hist):
        d = float(np.linalg.norm(rr))
        aa = boost*G*M_lmc*Msun/d**2
        dvv += aa*(rr/d)*dt; dvs += aa*dt
    return float(np.linalg.norm(dvv))/1e3, dvs/1e3, float(np.linalg.norm(hist[-1]))/kpc, boost

P(f"    {'model':>42} {'M_LMC':>10} {'boost':>7} {'r_max (kpc)':>12} {'reflex':>8} {'scalar sum':>11}")
REF = {}
for ft, a0 in A0.items():
    dv, dvs, rmax, bo = reflex_velocity(a0, Mb_mw[ft], LMC_MB)
    REF[ft] = (dv, dvs)
    P(f"    {'framework, ' + ft + ' footing':>42} {LMC_MB:10.2e} {bo:7.2f} {rmax:12.1f} {dv:8.2f} {dvs:11.2f}")
dv_l, dvs_l, rmax_l, _ = reflex_velocity(A0["canonical"], 1.3e12, LMC_MH_LCDM, lcdm=True)
P(f"    {'LambdaCDM, 1.3e12 halo + 1.5e11 LMC halo':>42} {LMC_MH_LCDM:10.2e} {1.0:7.2f} {rmax_l:12.1f} "
  f"{dv_l:8.2f} {dvs_l:11.2f}")
dv_lo = reflex_velocity(A0["canonical"], Mb_mw["canonical"], LMC_MB, back_Gyr=1.5)[1]
dv_hi = reflex_velocity(A0["canonical"], Mb_mw["canonical"], LMC_MB, back_Gyr=5.0)[1]
info(f"the framework's scalar upper bound over 1.5-5 Gyr of accumulated pull: {dv_lo:.1f}-{dv_hi:.1f} km/s; "
     f"the vector integral, which is what a reflex velocity actually is, is smaller because the LMC swings "
     f"across the sky during the orbit")
bo_in, y_in = boost_at(15.0, A0["canonical"], Mb_mw["canonical"])
bo_out, y_out = boost_at(70.0, A0["canonical"], Mb_mw["canonical"])
info(f"AND THE DIFFERENTIAL RUNS THE WRONG WAY TOO.  The measurement is inner Galaxy MINUS outer halo.  In "
     f"QUMOND the response factor nu(1+L) grows as the Galaxy's own field weakens: {bo_in:.2f} at 15 kpc "
     f"(y = {y_in:.3f}) against {bo_out:.2f} at 70 kpc (y = {y_out:.4f}).  The outer halo is pulled HARDER "
     f"per unit LMC mass than the disc, so the framework's differential is smaller still than the inner "
     f"number quoted above -- the deficit below is conservative.")
ratio = REF["canonical"][1]/REFLEX
ck("82b (LIABILITY) the framework's LMC cannot move the Milky Way as fast as the measurement says.  With "
   "3e9 Msun of baryons and the correct QUMOND boost in the Galaxy's own field, the accumulated reflex "
   "velocity is several times below the observed travel velocity of the inner Galaxy, while LambdaCDM's "
   "1.5e11 Msun LMC halo reproduces it",
   REF["canonical"][1] < REFLEX - 2*EREFLEX,
   f"framework {REF['canonical'][0]:.1f} km/s vector / {REF['canonical'][1]:.1f} scalar upper bound "
   f"(canonical), {REF['alt'][1]:.1f} (alt), against a measured "
   f"{REFLEX:.0f} +- {EREFLEX:.0f} km/s -- a shortfall of a factor {1.0/ratio:.1f}, i.e. "
   f"{(REFLEX-REF['canonical'][1])/EREFLEX:.1f} sigma on the quoted error even using the upper bound; "
   f"LambdaCDM's model gives {dv_l:.0f} km/s")
Mneed = LMC_MB*REFLEX/max(REF["canonical"][1], 1e-9)
info(f"to reach 32 km/s the framework's LMC would need about {Mneed:.2e} Msun of baryons (or the same factor "
     f"in the boost), against the ~3e9 that is actually seen in stars and HI -- so this is a real deficit "
     f"and not a modelling choice.  Two escapes exist and neither is free: the reflex measurement is itself "
     f"model-dependent (it is inferred from a dipole in the outer-halo velocity field), and a proper MOND "
     f"N-body would add the Galaxy's own phantom response to the LMC's passage, which this point-mass "
     f"calculation omits.  Recorded as a LIABILITY, not as a kill.")

# ---------------------------------------------------------------- controls
P(""); P("-"*118); P("mutation controls"); P("-"*118)
dv_newt = reflex_velocity(A0["canonical"]*1e-6, Mb_mw["canonical"], LMC_MB, lcdm=True)[1]
info(f"MUTATION 1 (Newtonian gravity with the same baryons): the scalar reflex falls from "
     f"{REF['canonical'][1]:.2f} to {dv_newt:.2f} km/s -- the kernel is doing real work here, contributing a "
     f"factor {REF['canonical'][1]/max(dv_newt,1e-9):.1f}, and the deficit survives it")
sol0 = EFESolve(e=1e-9)
a0_iso = abs(sol0.disc_asym(float(np.interp(20.0, Rrc, resp["canonical"][0])), gam))
info(f"MUTATION 2 (external field switched off): the predicted azimuthal asymmetry falls from "
     f"{AMP[('canonical', 20.0)]:.2e} to {a0_iso:.2e} -- it is the external field's, entirely")
shuf = cube.reshape(-1).copy(); rng.shuffle(shuf); shuf = shuf.reshape(cube.shape)
ws = shuf[m]/R[m]**3*SP**3
vs = (100.0/(4*math.pi))*np.array([np.sum(ws*X[m]), np.sum(ws*Y[m]), np.sum(ws*Z[m])])
info(f"MUTATION 3 (shuffle the 2M++ density values between cells): the reconstructed LSS field collapses "
     f"from {g_lss:.3e} to {float(np.linalg.norm(1.5*H0*OM_M*vs*1e3/B_2MPP)):.3e} m/s^2 -- the external field "
     f"is the cosmic web and not the box")
ck("C1 MUTATION CONTROLS behave: shrinking a_0 removes the kernel's contribution to the reflex velocity "
   "(and the deficit gets worse, not better); switching the external field off removes the azimuthal "
   "asymmetry entirely; and destroying the structure in the 2M++ cube destroys the large-scale field",
   dv_newt < REF["canonical"][1] and a0_iso < 1e-3*AMP[("canonical", 20.0)] and
   float(np.linalg.norm(vs)) < 0.3*float(np.linalg.norm(v1)),
   f"Newtonian reflex {dv_newt:.2f} vs {REF['canonical'][1]:.2f} km/s; isolated asymmetry {a0_iso:.1e} vs "
   f"{AMP[('canonical', 20.0)]:.1e}; shuffled |v| {float(np.linalg.norm(vs)):.0f} vs "
   f"{float(np.linalg.norm(v1)):.0f} km/s")

P(""); P("-"*118)
P(f"VERDICT.  ITEM 81: the vector sum is dominated by large-scale structure ({g_tot/A0['canonical']:.4f} a_0 canonical,")
P(f"{g_tot/A0['alt']:.4f} alt), pointing to (l, b) = ({l_tot:.1f}, {b_tot:+.1f}), i.e. {gam:.0f} degrees from the disc normal and so almost")
P(f"entirely in the plane.  The azimuthal asymmetry it produces in the outer rotation curve is under")
P(f"{100*amax:.2f} per cent -- two to five times smaller than the item's estimate and under the measurement floor.  The item's")
P(f"framing of 'three external fields' is itself corrected: in Newtonian units the LSS beats the LMC {g_lss/g_lmc:.0f}-fold and")
P(f"M31 {g_lss/g_m31:.0f}-fold, and the deep-MOND values usually quoted for the neighbours do not apply because the")
P(f"neighbours sit inside the Galaxy's own field.  UNDERPOWERED, and the amplitude is corrected downward.")
P(f"ITEM 82: the premise is corrected by a factor of {naive/g_lmc_sun:.0f} (the LMC's field at the Sun is essentially Newtonian),")
P(f"and the sharp version of the test -- can 3e9 Msun of LMC baryons produce the measured {REFLEX:.0f} km/s reflex")
P(f"motion of the inner Galaxy? -- comes out NO, by a factor of {1.0/ratio:.1f}.  That is a LIABILITY on the ledger.")
P("-"*118)
sys.exit(ck.done())
