#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g06v_adversarial_external_field_prescription_refutation.py
=================================================================================================================
ADVERSARIAL VERIFICATION of the load-bearing claim of g06_local_volume_groups_lambda_edge.py:

  "The external field entering nu's argument must be the BARYONIC Newtonian field, not a LambdaCDM
   velocity-field reconstruction, and this rung's answer reverses if that is wrong."

supported by check E1: direct baryonic sum g_N = 6.02e-15 = 6e-5 a_0 at the Local Group; 2M++ reconstruction
g = 1.161e-12 = 0.0124 a_0; the reconstruction read as the framework's MOND field and inverted through
nu(y) y a_0 = g gives g_N = 1.42e-14, so the two routes "agree to a factor 0.42" against a factor 193 raw.

THIS SCRIPT DOES NOT ASSUME g06 IS WRONG.  It reruns g06's own arithmetic from the same files, then attacks the
INFERENCE on five fronts.  Checks are written so that PASS = g06's claim survives that front and FAIL = it does
not.  Both footings.  Mutation controls at the end.

THE FIVE FRONTS
  A. ARITHMETIC.  Reproduce g_B, g_L and the inversion independently.  If the numbers do not reproduce there is
     nothing to argue about.
  B. LIKE-FOR-LIKE.  g06's g_B is a sum over 2MRS at r > 3 Mpc PLUS the UNGC inside 3 Mpc, and at the Local
     Group the UNGC term is essentially M31 at 0.77 Mpc.  g06's g_L is a sum over the 2M++ grid with the mask
     R > 3 Mpc/h = 4.45 Mpc.  The two sides of E1 therefore do not contain the same volume.  Quantified here.
  C. THE PECULIAR-VELOCITY TIE-BREAK, DONE PROPERLY.  g06 breaks the tie with v ~ g t_0, a relation it itself
     calls "worth a factor of two", and reports 328 km/s (baryonic) and 505 km/s (reconstruction) against the
     CMB dipole's 620 km/s -- "both in the right decade".  Linear theory has an exact relation,
     v = 2 f g / (3 H_0 Omega_m) with f = Omega_m^0.55 (Peebles 1980; Strauss & Willick 1995 eq. 15;
     Carrick, Turnbull, Lavaux & Hudson 2015 use it to fit beta* = 0.431 +- 0.021 against this very dipole).
     Used properly the two routes are NOT symmetric, and the asymmetry runs against g06's reading.
  D. HOW MUCH DOES E1 ACTUALLY CONSTRAIN?  Because the deep-MOND inversion is g_N = g^2/a_0, E1's window
     0.4 < g_B/g_N,inv < 2.5 is a window a factor 6.25 wide on g_B itself.  g06 states its own baryonic sum is
     a LOWER bound (2MRS magnitude-limited, zone of avoidance unmasked, no selection-function weighting).  If a
     realistic completeness correction still passes E1, then E1 certifies nothing at the precision the claim
     needs, and the "factor 0.42 agreement" is not evidence for the prescription.
  E. THE PREMISE, AGAINST THE REPOSITORY'S OWN STANDING.  g06 line 306-307: "In this framework the actual
     matter is BARYONS."  STANDING.md section 5 item 5 says the opposite, in force:
        "'No dark matter' is forfeited.  The framework *has* a dark sector -- the AeST/ghost-condensate
         Q-mode, a gravity mode rather than a particle.  Honest framing: MOND galaxies **plus** a
         no-particle CDM-like sector."
     and STANDING.md section 1 item 3 records, from this repository's own sheet N-body, that "no-CDM MOND
     cosmologies fail the forest" (1000-5000x short) and that "the framework's own derived Hubble floor makes
     MOND irrelevant to linear growth (<= 6%)".  A CDM-like component that clusters, plus a linear regime in
     which MOND is a <= 6% correction, is exactly the regime the 2M++ reconstruction measures.  On the
     framework's OWN committed standing the total clustering matter -- not the baryons alone -- sources the
     Newtonian field at 10-100 Mpc, and g06's R4b then gives the answer.
     This front is a CITATION check against files on disk, not a physics computation, and it is marked as such.

WHAT WOULD MAKE THE CLAIM SURVIVE: fronts B, C, D and E all passing.  They do not all pass.
"""
import sys, os, math, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import (Check, P, info, A0, DATA, vizier_tsv, _f, nu, nu_s, G, Msun, Mpc, kpc, H0, OM_M)

ck = Check(); rng = np.random.default_rng(20260903)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))

UPS_K, F_HE, MK_SUN = 0.60, 1.33, 3.27
H0_KMS = H0*Mpc/1e3
B_2MPP = 1.2
SP, NG, CEN = 400.0/256.0, 257, 128
HLIT = 0.674
MW_MSTAR = 5.0e10
R_SEAM, SOFT = 3.0, 0.15
T0 = 4.35e17
V_CMB_LG = 620.0            # km/s, Local Group motion w.r.t. the CMB (Planck 2018 / Kogut+1993: 627 +- 22)
FGROW = OM_M**0.55          # linear growth rate f ~ Omega_m^0.55 (Linder 2005)

# ============================================================================================== FRONT A
P("="*126)
P("A.  ARITHMETIC -- reproduce g06's two Local Group numbers independently before arguing about them")
P("="*126)

def eq2gal(ra, de):
    rap, dep, lncp = math.radians(192.85948), math.radians(27.12825), math.radians(122.93192)
    ra_, de_ = np.radians(ra), np.radians(de)
    b = np.arcsin(np.sin(de_)*math.sin(dep) + np.cos(de_)*math.cos(dep)*np.cos(ra_ - rap))
    l = lncp - np.arctan2(np.cos(de_)*np.sin(ra_ - rap),
                          np.sin(de_)*math.cos(dep) - np.cos(de_)*math.sin(dep)*np.cos(ra_ - rap))
    return np.degrees(l) % 360.0, np.degrees(b)

def gal_cart(ra, de, D):
    l, b = eq2gal(ra, de); lr, br = np.radians(l), np.radians(b)
    return np.array([D*np.cos(br)*np.cos(lr), D*np.cos(br)*np.sin(lr), D*np.sin(br)])

raw = vizier_tsv("ungc_karachentsev2013.tsv")
for x in raw:
    for k in ("Dist", "KLum", "MHI", "Vlg", "Ti1", "_RAJ2000", "_DEJ2000"): x[k] = _f(x[k])
    x["Name"] = x["Name"].strip(); x["MD"] = x["MD"].strip()

rows2 = []
for l in open(os.path.join(DATA, "2mrs_huchra2012.tsv"), encoding="latin-1"):
    if l.startswith("#Table\tJ_ApJS_199_26_table6"): break
    if l.startswith("#") or not l.strip(): continue
    f = l.rstrip("\n").split("\t")
    if len(f) != 4: continue
    try: rows2.append((float(f[0]), float(f[1]), float(f[2]), float(f[3])))
    except ValueError: pass
A2 = np.array(rows2); ra2, de2, cz2, K2 = A2.T
m2 = (cz2 > 350) & (cz2 < 15000)
d2 = cz2[m2]/H0_KMS
LK2 = 10**(0.4*(MK_SUN - (K2[m2] - 5*np.log10(d2*1e6/10))))
l2, b2 = eq2gal(ra2[m2], de2[m2]); lr2, br2 = np.radians(l2), np.radians(b2)
POS2 = np.stack([d2*np.cos(br2)*np.cos(lr2), d2*np.cos(br2)*np.sin(lr2), d2*np.sin(br2)], 1)
MB2 = UPS_K*LK2*1.4
K2u = K2[m2]

UPOS, UMB, UMD, UNM, UD = [], [], [], [], []
for x in raw:
    if not np.isfinite(x["Dist"]): continue
    mb = (UPS_K*10**x["KLum"] if np.isfinite(x["KLum"]) else 0.0) + (F_HE*10**x["MHI"] if np.isfinite(x["MHI"]) else 0.0)
    if x["Name"] == "Milky Way": mb += MW_MSTAR
    if mb <= 0: continue
    UPOS.append(gal_cart(x["_RAJ2000"], x["_DEJ2000"], x["Dist"])); UMB.append(mb)
    UMD.append(x["MD"].upper()); UNM.append(x["Name"].upper()); UD.append(x["Dist"])
UPOS = np.array(UPOS); UMB = np.array(UMB); UMD = np.array(UMD); UNM = np.array(UNM)

def g_bary_parts(pos, own, seam=R_SEAM, mb2=None):
    mb2 = MB2 if mb2 is None else mb2
    d = POS2 - pos; r = np.linalg.norm(d, axis=1); k = r > seam
    far = (G*Msun/Mpc**2)*np.sum((mb2[k]/r[k]**3)[:, None]*d[k], axis=0)
    d = UPOS - pos; r = np.sqrt(np.sum(d*d, axis=1) + SOFT**2)
    k = (r < seam) & (UNM != own) & (UMD != own)
    near = (G*Msun/Mpc**2)*np.sum((UMB[k]/r[k]**3)[:, None]*d[k], axis=0)
    return far, near

cube = np.load(os.path.join(DATA, "twompp_density.npy"))
ax = (np.arange(NG) - CEN)*SP
GX, GY, GZ = np.meshgrid(ax, ax, ax, indexing="ij")
def g_lss_lcdm_vec(pos_mpc, rmin=3.0, dens=None):
    dens = cube if dens is None else dens
    p = np.asarray(pos_mpc, float)*HLIT
    dx, dy, dz = GX - p[0], GY - p[1], GZ - p[2]
    R = np.sqrt(dx*dx + dy*dy + dz*dz); m = (R > rmin) & (R < 200.0)
    w = dens[m]/R[m]**3*SP**3
    v1 = (100.0/(4*math.pi))*np.array([np.sum(w*dx[m]), np.sum(w*dy[m]), np.sum(w*dz[m])])
    return 1.5*H0*OM_M*(v1*1e3)/B_2MPP

def qumond_invert(g_mond, a0):
    lo, hi = 1e-12, 1e3
    for _ in range(200):
        mid = math.sqrt(lo*hi)
        if nu_s(mid)*mid*a0 < g_mond: lo = mid
        else: hi = mid
    return math.sqrt(lo*hi)*a0

far0, near0 = g_bary_parts(np.zeros(3), "MILKY WAY")
gB_vec = far0 + near0
gB = float(np.linalg.norm(gB_vec))
gL_vec = g_lss_lcdm_vec(np.zeros(3)); gL = float(np.linalg.norm(gL_vec))
a0c = A0["canonical"]
gNinv = qumond_invert(gL, a0c)
info(f"reproduced  g_B (2MRS r>3 Mpc + UNGC r<3 Mpc, MW and its own satellites removed) = {gB:.4e} m/s^2 "
     f"= {gB/a0c:.6f} a_0        [g06 quotes 6.024e-15 / 0.00006]")
info(f"reproduced  g_L (2M++ linear reconstruction, mask 3 < R < 200 Mpc/h)             = {gL:.4e} m/s^2 "
     f"= {gL/a0c:.6f} a_0        [g06 quotes 1.161e-12 / 0.01240]")
info(f"reproduced  g_N from inverting g_L through nu(y) y a_0 = g                       = {gNinv:.4e} m/s^2 "
     f"= {gNinv/a0c:.6f} a_0     [g06 quotes 1.422e-14 / 0.00015]")
info(f"the inversion is the deep-MOND square root: g_N = g^2/a_0 gives {gL**2/a0c:.4e}, i.e. "
     f"{100*abs(gL**2/a0c/gNinv - 1):.2f}% from the numeric inversion, so E1's ratio is (g_B a_0)^(1/2)/g_L "
     f"SQUARED and a factor r in g_N is only sqrt(r) in acceleration")
ck("A1 g06's three Local Group numbers reproduce from the same files with independent code.  If this failed the "
   "rest of the audit would be moot",
   abs(gB/6.024e-15 - 1) < 0.02 and abs(gL/1.161e-12 - 1) < 0.02 and abs(gNinv/1.422e-14 - 1) < 0.02,
   f"g_B {gB:.4e} vs 6.024e-15 ({100*(gB/6.024e-15-1):+.2f}%), g_L {gL:.4e} vs 1.161e-12 "
   f"({100*(gL/1.161e-12-1):+.2f}%), g_N,inv {gNinv:.4e} vs 1.422e-14 ({100*(gNinv/1.422e-14-1):+.2f}%)")
ck("A2 and E1's headline ratio reproduces, so the 'factor 0.42' is arithmetically what g06 says it is",
   abs((gB/gNinv)/0.424 - 1) < 0.05, f"g_B/g_N,inv = {gB/gNinv:.4f} against g06's 0.424; the raw factor is "
   f"{gL/gB:.0f} against g06's 193")

# ============================================================================================== FRONT B
P(""); P("="*126)
P("B.  LIKE-FOR-LIKE -- E1's two sides do not contain the same volume, and one of them is M31")
P("="*126)
info(f"g_B splits as  |far (2MRS, r > {R_SEAM} Mpc)| = {np.linalg.norm(far0):.4e}  and  "
     f"|near (UNGC, r < {R_SEAM} Mpc)| = {np.linalg.norm(near0):.4e}")
ang_fn = math.degrees(math.acos(float(np.dot(far0, near0))/(np.linalg.norm(far0)*np.linalg.norm(near0))))
info(f"they are {ang_fn:.0f} degrees apart, so they partly CANCEL: |far + near| = {gB:.4e} is SMALLER than the "
     f"far term alone.  E1's central number is a cancellation residual, not a sum.")
# what is the near term made of?
d = UPOS - np.zeros(3); r = np.sqrt(np.sum(d*d, axis=1) + SOFT**2)
k = (r < R_SEAM) & (UNM != "MILKY WAY") & (UMD != "MILKY WAY")
contrib = (G*Msun/Mpc**2)*UMB[k]/r[k]**2
ordr = np.argsort(-contrib)
P(f"    {'the near term, largest contributors':38} {'D/Mpc':>7} {'g_N (m/s^2)':>13} {'share of |near|':>16}")
for i in ordr[:5]:
    P(f"    {UNM[k][i]:38} {r[k][i]:7.2f} {contrib[i]:13.3e} {contrib[i]/np.linalg.norm(near0):16.2f}")
info(f"g_L's mask starts at R > 3 Mpc/h = {3.0/HLIT:.2f} Mpc, so the 2M++ side contains NOTHING inside "
     f"{3.0/HLIT:.2f} Mpc -- no M31, no Local Group at all.")
far_only = float(np.linalg.norm(far0))
# rebuild g_B on the SAME volume as g_L: 2MRS beyond 4.45 Mpc, nothing nearer
far_match, _ = g_bary_parts(np.zeros(3), "MILKY WAY", seam=3.0/HLIT)
gB_match = float(np.linalg.norm(far_match))
info(f"matched-volume baryonic field (2MRS only, r > {3.0/HLIT:.2f} Mpc, no UNGC term at all) = "
     f"{gB_match:.4e} = {gB_match/a0c:.6f} a_0, ratio to g_N,inv = {gB_match/gNinv:.3f}")
ck("B1 E1 compares like with like.  The claim's central number 6.02e-15 must be the same physical quantity as "
   "the reconstruction it is compared to.  It is not: the baryonic side includes M31 at 0.77 Mpc and the whole "
   "Local Volume, the 2M++ side is masked to R > 3 Mpc/h and contains neither.  This check asserts the two "
   "volumes agree to 20%; it fails, and the direction of the failure is that E1's quoted g_B is a "
   "cancellation residual between an included near term and the far term",
   abs(gB/gB_match - 1) < 0.20, f"g06's g_B = {gB:.3e} (far+near, partly cancelling) against the "
   f"volume-matched g_B = {gB_match:.3e}: a factor {gB_match/gB:.2f}.  Matched, E1's ratio would be "
   f"{gB_match/gNinv:.3f} rather than {gB/gNinv:.3f}")
info("NOTE, AGAINST MY OWN CASE: the volume-matched number moves E1's ratio TOWARD 1, so this front damages the")
info("precision of E1's quoted number without reversing its sign.  It is recorded because the claim quotes")
info("6.02e-15 as 'the direct baryonic sum at the Local Group' and that is not what was compared.")
uB, uL = gB_vec/gB, gL_vec/gL
angBL = math.degrees(math.acos(float(np.clip(np.dot(uB, uL), -1, 1))))
uBm = far_match/gB_match
angBLm = math.degrees(math.acos(float(np.clip(np.dot(uBm, uL), -1, 1))))
lB, bB = math.degrees(math.atan2(uB[1], uB[0])) % 360, math.degrees(math.asin(uB[2]))
lL, bL_ = math.degrees(math.atan2(uL[1], uL[0])) % 360, math.degrees(math.asin(uL[2]))
info(f"directions: baryonic (l,b) = ({lB:.0f}, {bB:+.0f}); 2M++ (l,b) = ({lL:.0f}, {bL_:+.0f}); CMB dipole "
     f"apex for the Local Group is (l,b) ~ (276, +30) (Kogut et al. 1993)")
ck("B2 the two fields point the same way.  E1 compares MAGNITUDES only.  Two vectors of similar length pointing "
   "60 degrees apart are not 'the same field seen two ways'.  Asserts 30 degrees",
   angBL < 30.0, f"g06's g_B is {angBL:.0f} degrees from the 2M++ vector; the volume-matched baryonic vector is "
   f"{angBLm:.0f} degrees from it")

# ============================================================================================== FRONT C
P(""); P("="*126)
P("C.  THE PECULIAR-VELOCITY TIE-BREAK, DONE WITH LINEAR THEORY INSTEAD OF v ~ g t_0")
P("="*126)
info("g06 breaks the tie with v ~ g t_0 and reports 'both routes in the right decade'.  Linear theory fixes the")
info("constant exactly: v = 2 f g / (3 H_0 Omega_m), f = Omega_m^0.55 (Peebles 1980; Strauss & Willick 1995).")
KLIN = 2.0*FGROW/(3.0*H0*OM_M)
info(f"    f = Omega_m^0.55 = {FGROW:.3f}, Omega_m = {OM_M:.4f}, H_0 = {H0*Mpc/1e3:.1f} km/s/Mpc  ->  "
     f"v = {KLIN:.3e} s x g   (g06 used t_0 = {T0:.3e} s, {100*(T0/KLIN-1):+.0f}%)")
v_lcdm = KLIN*gL/1e3
gB_mond = nu_s(gB/a0c)*gB
v_bary = KLIN*gB_mond/1e3
gBm_mond = nu_s(gB_match/a0c)*gB_match
v_barym = KLIN*gBm_mond/1e3
P(f"    {'route':56} {'g_dyn (m/s^2)':>14} {'v_pred (km/s)':>14} {'vs 620':>9}")
P(f"    {'2M++ total-matter Newtonian field, used as the dynamics':56} {gL:14.3e} {v_lcdm:14.0f} "
  f"{v_lcdm/V_CMB_LG:9.2f}")
P(f"    {'baryons only, boosted by the kernel: nu(g_B/a0) g_B':56} {gB_mond:14.3e} {v_bary:14.0f} "
  f"{v_bary/V_CMB_LG:9.2f}")
P(f"    {'... same, on the volume-matched baryonic field':56} {gBm_mond:14.3e} {v_barym:14.0f} "
  f"{v_barym/V_CMB_LG:9.2f}")
ck("C1 the peculiar-velocity cross-check does not favour the reconstruction over the baryons.  g06 offers it as "
   "support for its reading ('both are in the right decade').  Done with the exact linear-theory constant "
   "rather than v ~ g t_0, this asserts the two routes miss the observed 620 km/s by comparable factors.  If it "
   "fails, the one piece of DATA g06 brings to E1 points the other way",
   abs(math.log10(v_lcdm/V_CMB_LG)) > 0.7*abs(math.log10(v_bary/V_CMB_LG)),
   f"2M++ route {v_lcdm:.0f} km/s, off by {100*abs(v_lcdm/V_CMB_LG-1):.0f}%; baryons-through-the-kernel "
   f"{v_bary:.0f} km/s, off by {100*abs(v_bary/V_CMB_LG-1):.0f}% (volume-matched {v_barym:.0f} km/s, "
   f"{100*abs(v_barym/V_CMB_LG-1):.0f}%).  Carrick+2015 fit beta* = 0.431 to this same dipole with this same "
   f"field and reproduce it; the baryons-only route needs g_B a factor "
   f"{(V_CMB_LG/v_bary)**2:.1f} larger to do so")
info("Read plainly: the reconstruction reproduces the Local Group's measured motion to a few per cent -- that is")
info("what Carrick+2015 CALIBRATED it to do -- and the baryons-through-the-kernel route falls short by ~1.7x in")
info("velocity, i.e. ~3x in g_N.  That is inside g06's admitted completeness bound, so it is not a kill; but it")
info("is not support either, and g06 presents it as support.")

# ============================================================================================== FRONT D
P(""); P("="*126)
P("D.  HOW MUCH DOES E1 ACTUALLY CONSTRAIN?  The window is a factor 6.25 wide on g_B")
P("="*126)
lo_w, hi_w = 0.4*gNinv, 2.5*gNinv
info(f"E1 passes for 0.4 < g_B/g_N,inv < 2.5, i.e. g_B anywhere in [{lo_w:.3e}, {hi_w:.3e}] m/s^2 = "
     f"[{lo_w/a0c:.6f}, {hi_w/a0c:.6f}] a_0 -- a factor {hi_w/lo_w:.2f}, or {math.log10(hi_w/lo_w):.2f} dex.")
info("g06 states its baryonic sum is a LOWER bound: 2MRS is magnitude-limited, the zone of avoidance is")
info("unmasked, and no selection-function or 1/Vmax weighting is applied.  Three completeness scalings:")
P(f"    {'assumed correction to g_B':44} {'g_B (m/s^2)':>13} {'E1 ratio':>10} {'E1 verdict':>11}")
for lbl, fac in (("none (g06 as run)", 1.0), ("x2 (mild incompleteness)", 2.0), ("x3 (g06's own R4 bracket)", 3.0),
                 ("x5", 5.0), ("x10", 10.0), ("x0.5 (if 2MRS over-counted)", 0.5)):
    rr = fac*gB/gNinv
    P(f"    {lbl:44} {fac*gB:13.3e} {rr:10.3f} {'PASS' if 0.4 < rr < 2.5 else 'fail':>11}")
ck("D1 E1 is a tight enough test to certify the baryonic sum at the precision the claim needs.  The claim rests "
   "on g_B being ~6e-5 a_0 rather than ~1e-2 a_0, but it is quoted as if E1 pinned the number.  This asserts "
   "that a threefold completeness correction -- the size g06 itself brackets in R4 -- would be DETECTED by E1",
   not (0.4 < 3.0*gB/gNinv < 2.5), f"g_B x3 gives an E1 ratio of {3.0*gB/gNinv:.3f}, which is inside E1's "
   f"[0.4, 2.5] window, so E1 cannot tell the two apart.  E1 admits g_B over "
   f"{math.log10(hi_w/lo_w):.2f} dex")
# a direct, crude completeness probe: how much of the 2MRS luminosity is lost to the flux limit with distance?
zbin = [(5, 20), (20, 40), (40, 70), (70, 100), (100, 150)]
P(f"    {'2MRS shell':>16} {'N':>7} {'median K':>9} {'faintest M_K':>13} {'sum L_K (1e10)':>15} "
  f"{'|g| contribution':>17}")
for a, b in zbin:
    s = (d2 >= a) & (d2 < b)
    if s.sum() < 10: continue
    dd = POS2[s]; rr = np.linalg.norm(dd, axis=1)
    gsh = float(np.linalg.norm((G*Msun/Mpc**2)*np.sum((MB2[s]/rr**3)[:, None]*dd, axis=0)))
    MKf = float(np.nanmax(K2u[s] - 5*np.log10(d2[s]*1e6/10)))
    P(f"    {f'{a}-{b} Mpc':>16} {int(s.sum()):7d} {float(np.median(K2u[s])):9.2f} {MKf:13.2f} "
      f"{float(np.sum(LK2[s]))/1e10:15.1f} {gsh:17.3e}")
info("The faintest galaxy 2MRS still sees at 100-150 Mpc is roughly M_K ~ -24, i.e. several times L*.  The")
info("luminosity actually summed there is therefore a small fraction of the luminosity present, and the")
info("un-weighted sum used for g_B is an underestimate by an amount this script cannot pin down.  That is not a")
info("criticism of g06's honesty -- g06 says so -- it is the reason E1 cannot be load-bearing.")

# ============================================================================================== FRONT E
P(""); P("="*126)
P("E.  THE PREMISE: 'in this framework the actual matter is BARYONS' is retracted by this repository's own")
P("    STANDING.md, and the retraction is exactly on the scales the external field comes from")
P("="*126)
STD = open(os.path.join(ROOT, "STANDING.md"), encoding="utf-8").read()
q_forfeit = "\"No dark matter\" is forfeited"
q_sector  = "MOND galaxies **plus** a\n   no-particle CDM-like sector"
q_forest  = "no-CDM MOND cosmologies fail the forest"
q_linear  = "makes MOND irrelevant to linear growth"
found = {q_forfeit: q_forfeit in STD, q_sector: q_sector.replace("\n  ", " ") in STD.replace("\n  ", " "),
         q_forest: q_forest in STD, q_linear: q_linear in STD}
for q, v in found.items():
    info(f"    STANDING.md contains {'YES' if v else 'NO ':>3}:  \"{q[:88]}\"")
g06src = open(os.path.join(HERE, "g06_local_volume_groups_lambda_edge.py"), encoding="utf-8").read()
prem = "in this framework the actual matter is BARYONS" in g06src
info(f"    g06 asserts the premise verbatim: {'YES' if prem else 'NO'}  "
     f"(\"In this framework the actual matter is BARYONS.\")")
ck("E-A the premise g06 argues from is the repository's live position.  g06's whole prescription argument is "
   "'in QUMOND the external field is the Newtonian field of the actual matter, and in this framework the actual "
   "matter is BARYONS'.  The first clause is right.  This checks the second against STANDING.md, and it fails: "
   "STANDING section 5 item 5 records 'No dark matter is forfeited -- the framework HAS a dark sector, the "
   "AeST/ghost-condensate Q-mode -- MOND galaxies PLUS a no-particle CDM-like sector'",
   not (found[q_forfeit] and prem),
   f"STANDING.md carries the forfeit ({found[q_forfeit]}) and g06 carries the premise ({prem}); they are "
   f"contradictory and the claim inherits the contradiction")
ck("E-B and if the framework's CDM-like sector did NOT cluster on 10-100 Mpc scales, the contradiction would be "
   "harmless -- the external field would still be baryonic.  This checks the repository's own record on that.  "
   "It fails: STANDING records the sheet N-body result that no-CDM MOND cosmologies fall 1000-5000x short of "
   "the Lyman-alpha forest, and that with the framework's own Hubble floor MOND is a <= 6% correction to linear "
   "growth.  A CDM-like component that clusters, in a linear regime where MOND barely matters, is precisely "
   "what a 2M++ velocity-field reconstruction measures",
   not (found[q_forest] or found[q_linear]),
   f"forest clause present: {found[q_forest]}; linear-growth clause present: {found[q_linear]}.  Both present "
   f"means the framework's own committed cosmology sources the 10-100 Mpc Newtonian field with baryons PLUS "
   f"the Q-mode, which is the total clustering matter the reconstruction returns")
info("")
info("CONSEQUENCE, in g06's own currency.  g06's variation table already contains the answer under the label")
info("'2M++ field used raw as g_N (wrong, shown)': median boost 2.215 (+0.345 dex), inside the cluster band,")
info("against the primary 0.817.  That is g06's own R4b, which g06 marks FAIL and explains as a strawman.  On")
info("the repository's own standing it is not a strawman: it is the framework's own dark sector doing what")
info("STANDING says it does.  The intermediate case matters too -- a Q-mode that clusters on supercluster")
info("scales but is dilute inside a 0.2 Mpc group leaves the INTERNAL field baryonic while raising the EXTERNAL")
info("one, and that is exactly the branch R4b computes.")
qm_frac = np.array([0.0, 0.1, 0.25, 0.5, 1.0])
P(""); P(f"    {'external field sourced by baryons + Q-mode':46} {'e_N (a_0)':>11} {'nu(e_N)':>9} "
        f"{'e_N/x_int, median group':>24}")
xint_med = 0.00189   # g06's printed median internal g_bar/a_0 at r_h, canonical footing
for f in qm_frac:
    ge = gB + f*(gNinv*0 + (gL - gB))   # linear ramp from baryons-only to the full total-matter Newtonian field
    P(f"    {f'Q-mode contributes {100*f:3.0f}% of the total-matter field':46} {ge/a0c:11.5f} "
      f"{float(nu(ge/a0c)):9.2f} {ge/a0c/xint_med:24.2f}")
info("At any Q-mode share above ~10% of the total-matter field the external field exceeds the median group's own")
info("internal field and the external-field branch takes over.  The claim needs the share to be essentially ZERO.")

# ============================================================================================== FRONT F
P(""); P("="*126)
P("F.  DOES THE 'RECONSTRUCTION = THE FRAMEWORK'S MOND FIELD' IDENTIFICATION HOLD AWAY FROM THE ORIGIN?")
P("="*126)
info("E1 is evaluated at ONE point.  If the identification is physics it should hold at the 26 group positions")
info("too; if it is a coincidence of the local supercluster it will not.  Both fields recomputed at each group.")
sat = collections.defaultdict(list)
byname = {x["Name"].upper(): x for x in raw}
for x in raw:
    if x["Ti1"] > 0 and x["MD"].upper() in byname and x["MD"].upper() != x["Name"].upper():
        sat[x["MD"]].append(x)
gpos, gname = [], []
for host_name, sats in sorted(sat.items(), key=lambda t: -len(t[1])):
    if len(sats) + 1 < 5: continue
    h = byname[host_name.upper()]
    gpos.append(gal_cart(h["_RAJ2000"], h["_DEJ2000"], h["Dist"])); gname.append(host_name)
P(f"    {'group':14} {'|g_B| (m/s^2)':>14} {'nu(g_B)g_B':>12} {'|g_2M++|':>12} {'ratio':>8} {'angle':>7}")
rats, angs = [], []
for nm, p in zip(gname, gpos):
    fa, ne = g_bary_parts(p, nm.upper())
    vb = fa + ne; gb = float(np.linalg.norm(vb))
    gm = nu_s(gb/a0c)*gb
    vl = g_lss_lcdm_vec(p); gl = float(np.linalg.norm(vl))
    aa = math.degrees(math.acos(float(np.clip(np.dot(vb/gb, vl/gl), -1, 1))))
    rats.append(gm/gl); angs.append(aa)
    P(f"    {nm:14} {gb:14.3e} {gm:12.3e} {gl:12.3e} {gm/gl:8.3f} {aa:7.0f}")
rats = np.array(rats); angs = np.array(angs)
info(f"ratio nu(g_B)g_B / g_2M++ across 26 positions: median {np.median(rats):.3f}, "
     f"16-84% [{np.percentile(rats,16):.3f}, {np.percentile(rats,84):.3f}], full range "
     f"[{rats.min():.3f}, {rats.max():.3f}], spread {np.log10(rats).std():.3f} dex")
info(f"angle between the two vectors: median {np.median(angs):.0f} deg, range {angs.min():.0f} - "
     f"{angs.max():.0f} deg")
ck("F1 the identification 'the reconstruction IS the framework's MOND field' holds away from the Local Group.  "
   "E1 tests it at one point; if it is physics rather than a local coincidence the ratio should be near 1 "
   "everywhere.  Asserts the 26-position median is within a factor 1.6 of 1 AND the scatter is under 0.2 dex",
   0.63 < float(np.median(rats)) < 1.6 and float(np.log10(rats).std()) < 0.2,
   f"median {np.median(rats):.3f}, scatter {np.log10(rats).std():.3f} dex over 26 positions")
ck("F2 and the two vectors point the same way where the identification is claimed to hold.  Asserts a median "
   "angle under 30 degrees",
   float(np.median(angs)) < 30.0, f"median angle {np.median(angs):.0f} degrees, range {angs.min():.0f} - "
   f"{angs.max():.0f}")

# ============================================================================================== FRONT I
P(""); P("="*126)
P("I.  TWO NAMED DEFECTS IN THE CLAIM'S HEADLINE NUMBER, AND ONE COMMITTED SIBLING THAT CONTRADICTS IT")
P("="*126)
info("I.a  The exclusion rule for a group's OWN members is (name != host) AND (main_disturber != host).  The UNGC")
info("     lists the SMC's main disturber as the LMC, not the Milky Way (Karachentsev, Makarov & Kaisina 2013),")
info("     so the SMC survives the filter and is counted as an EXTERNAL perturber of the Milky Way -- at 0.06")
info("     Mpc.  Its larger companion the LMC, whose main disturber IS the Milky Way, is correctly removed.  The")
info("     bookkeeping therefore drops the bigger member of the Magellanic pair and keeps the smaller one.")
smc_i = int(np.where(UNM == "SMC")[0][0])
d_smc = float(np.linalg.norm(UPOS[smc_i]))
g_smc = (G*Msun/Mpc**2)*UMB[smc_i]/(d_smc**2 + SOFT**2)
info(f"     SMC: UNGC distance {d_smc:.3f} Mpc, M_b = {UMB[smc_i]:.2e} Msun, contribution "
     f"{g_smc:.3e} m/s^2 = {g_smc/gB:.2f} x the whole quoted g_B of {gB:.3e}")
# properly exclude everything bound to the Milky Way (inside the Local Group's own turnaround radius)
def g_bary_lgclean(rcut):
    d = POS2 - 0.0; r = np.linalg.norm(d, axis=1); k = r > R_SEAM
    far = (G*Msun/Mpc**2)*np.sum((MB2[k]/r[k]**3)[:, None]*d[k], axis=0)
    d = UPOS; r = np.sqrt(np.sum(d*d, axis=1) + SOFT**2)
    k = (r < R_SEAM) & (r > rcut)
    near = (G*Msun/Mpc**2)*np.sum((UMB[k]/r[k]**3)[:, None]*d[k], axis=0)
    return float(np.linalg.norm(far + near))
P(f"    {'Milky Way satellites removed by a distance cut':46} {'g_B (m/s^2)':>13} {'e_N (a_0)':>11} "
  f"{'E1 ratio':>10}")
for rc in (0.0, 0.3, 0.5, 1.0):
    v = g_bary_lgclean(rc)
    P(f"    {f'exclude UNGC galaxies within {rc:.1f} Mpc of the MW':46} {v:13.3e} {v/a0c:11.6f} "
      f"{v/gNinv:10.3f}")
ck("I1 the group's own members are excluded from its own external field.  The claim's headline number is the "
   "Milky Way group's external field; a Milky Way satellite 60 kpc away must not be in it.  This asserts the "
   "SMC contributes under 10% of g_B",
   g_smc/gB < 0.10, f"the SMC alone contributes {g_smc:.3e} m/s^2, {100*g_smc/gB:.0f}% of the quoted g_B "
   f"{gB:.3e}; removing everything inside 0.3 Mpc of the Milky Way gives g_B = {g_bary_lgclean(0.3):.3e}, a "
   f"factor {g_bary_lgclean(0.3)/gB:.2f}")
info("")
info("I.b  The repository already carries a committed, passing script that uses the OPPOSITE prescription for")
info("     the SAME number.  h81_h82_mw_external_fields.py builds the 2M++ field with the identical code and")
info("     calls it 'the NEWTONIAN large-scale field at the Local Group', tabulating e_N = 0.01240 canonical /")
info("     0.01027 alt, and its check 81a is built on that reading.  g06 cites h81 for the reduction but not")
info("     for the disagreement.  Two committed scripts, one quantity, a factor 193 apart.")
h81 = open(os.path.join(HERE, "h81_h82_mw_external_fields.out"), encoding="utf-8").read()
h81_uses_raw = "large-scale structure     1.161e-12        0.01240" in h81
info(f"     h81_h82_mw_external_fields.out tabulates LSS e_N = 0.01240 as a NEWTONIAN field: "
     f"{'YES' if h81_uses_raw else 'NO'}")
ck("I2 the repository is internally consistent about which field enters nu's argument at the Local Group.  A "
   "prescription that 'must' hold cannot be contradicted by a committed sibling script that passes its own "
   "checks on the opposite reading",
   not h81_uses_raw, f"h81_h82 (committed, passing) uses e_N = 0.01240 at the Local Group; g06 (this rung) uses "
   f"e_N = {gB/a0c:.5f}.  Factor {gL/gB:.0f}.  One of the two is wrong and the repository does not say which")

# ============================================================================================== FOOTINGS
P(""); P("="*126)
P("G.  BOTH FOOTINGS -- does any of this depend on the choice of a_0?")
P("="*126)
P(f"    {'footing':12} {'a_0':>11} {'g_B/a_0':>10} {'g_2M++/a_0':>12} {'g_N,inv':>11} {'E1 ratio':>10} "
  f"{'v_bary (km/s)':>14}")
e1r = {}
for foot, a0 in A0.items():
    gi = qumond_invert(gL, a0); vb_ = KLIN*nu_s(gB/a0)*gB/1e3
    e1r[foot] = gB/gi
    P(f"    {foot:12} {a0:11.3e} {gB/a0:10.6f} {gL/a0:12.5f} {gi:11.3e} {gB/gi:10.3f} {vb_:14.0f}")
ck("G1 both footings, and the audit's verdicts do not turn on a_0",
   abs(math.log10(e1r['canonical']/e1r['alt'])) < 0.15,
   f"E1 ratio {e1r['canonical']:.3f} canonical vs {e1r['alt']:.3f} alt, "
   f"{math.log10(e1r['canonical']/e1r['alt']):+.3f} dex")

# ============================================================================================== MUTATIONS
P(""); P("="*126)
P("H.  MUTATION CONTROLS")
P("="*126)
sh = rng.permutation(len(MB2))
fa_s, ne_s = g_bary_parts(np.zeros(3), "MILKY WAY", mb2=MB2[sh])
gB_s = float(np.linalg.norm(fa_s + ne_s))
ck("M1 mutation -- shuffle the 2MRS baryonic masses across sky positions.  The dipole sum must change: if a "
   "scrambled catalogue gave the same g_B, the far field would be a property of the sky coverage rather than of "
   "where the mass is",
   abs(math.log10(gB_s/gB)) > 0.10, f"shuffled g_B = {gB_s:.3e} against the real {gB:.3e}, "
   f"{math.log10(gB_s/gB):+.3f} dex")
cshuf = cube.copy(); flat = cshuf.ravel(); rng.shuffle(flat)
gL_s = float(np.linalg.norm(g_lss_lcdm_vec(np.zeros(3), dens=flat.reshape(cube.shape))))
ck("M2 mutation -- shuffle the 2M++ density cells.  The reconstruction must collapse toward zero; if it did not, "
   "the 1.16e-12 would be a normalisation artefact rather than a measurement of where the structure is",
   gL_s/gL < 0.2, f"shuffled g_2M++ = {gL_s:.3e} against the real {gL:.3e}, a factor {gL_s/gL:.4f}")
gB_mw = float(np.linalg.norm(sum(g_bary_parts(np.zeros(3), "ZZZ_NOT_A_GALAXY"))))
ck("M3 mutation -- stop excluding the Milky Way's own satellites from its external field.  The number must move, "
   "or the exclusion logic is not doing anything and the 'own group removed' claim is empty",
   abs(math.log10(gB_mw/gB)) > 0.02, f"with no exclusion g_B = {gB_mw:.3e} against {gB:.3e}, "
   f"{math.log10(gB_mw/gB):+.3f} dex")
gL_nomask = float(np.linalg.norm(g_lss_lcdm_vec(np.zeros(3), rmin=1.0)))
ck("M4 mutation -- move the 2M++ inner mask from 3 to 1 Mpc/h.  If the reconstruction's value depended strongly "
   "on where its inner hole is cut, comparing it to a baryonic sum that has no such hole would be meaningless "
   "even in principle.  Asserts it moves by less than 30%",
   abs(gL_nomask/gL - 1) < 0.30, f"mask R > 1 Mpc/h gives {gL_nomask:.3e} against {gL:.3e}, a factor "
   f"{gL_nomask/gL:.3f}")

P(""); P("="*126)
P("VERDICT SUMMARY")
P("="*126)
info("What survives: the QUMOND half of the claim.  In QUMOND the external-field parameter is the Newtonian")
info("field of whatever sources the Newtonian potential -- that half is definitional and correct, and g06's")
info("arithmetic reproduces exactly (A1, A2).")
info("What does not survive: the identification of 'whatever sources the Newtonian potential' with BARYONS")
info("ALONE, on 10-100 Mpc scales, in a framework whose own STANDING.md forfeits 'no dark matter' and records a")
info("clustering CDM-like Q-mode plus a linear regime where MOND is a <= 6% correction (E-A, E-B).  On the")
info("repository's own standing the 2M++ reconstruction is closer to the right g_N,ext than the baryon sum is,")
info("and by g06's own R4b the rung's median boost then moves from 0.817 to 2.215 -- into the cluster band.")
info("What is weaker than advertised: E1 itself.  Its two sides are not the same volume (B1), its supporting")
info("velocity check runs against it once linear theory replaces v ~ g t_0 (C1), and its pass window admits g_B")
info("over 0.80 dex so it cannot certify the number the claim needs (D1).")
sys.exit(ck.done())
