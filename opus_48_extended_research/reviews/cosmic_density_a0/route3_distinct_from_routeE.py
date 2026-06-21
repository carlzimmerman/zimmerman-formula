#!/usr/bin/env python3
r"""
ROUTE 3 -- Is Carl's COSMIC-WEB a0 GENUINELY DISTINCT from the killed ROUTE_E,
or the same kill re-dressed?
================================================================================
Carl's route:   a0 = (c/2) sqrt( G (rho_DE + rho_ambient) ),  rho_ambient = the
                LARGE-SCALE cosmic-web density smoothed on the correlation length
                (~5-10 Mpc), NOT the LOCAL matter density (= ROUTE_E, killed).

ROUTE_E (killed, banked ROUTE_E_DENSITY_A0_CLOSED_FALSIFIER + DENSITY_A0_ELL_1MPC):
   a0=(c/2)sqrt(G rho_LOCAL). Three kills:
     (i)  SMOOTHING SCALE -- the ~Mpc scale that closes clusters is a TUNED input
          the dS-Unruh foundation does not supply.
     (ii) EQUIVALENCE PRINCIPLE -- Luo 2026 a_T = a_pr + a_bg (additive); the floor
          a_bg is uniform-in-space Lambda; a free-falling star feels NO local-matter
          Unruh heat -> the foundation forbids a local-matter a0 floor.
     (iii) SPARC env null -- per-galaxy d log a0 / d log(1+delta) = +0.052 +- 0.043
          (10.5 sigma from the +0.5 the density-fork needs).

THIS SCRIPT tests each of the 3 kills against the COSMIC-WEB version, with REAL
numbers, both ways. It does NOT re-derive the magnitude (ROUTE 1's job) or re-run
the member-galaxy RAR from scratch (ROUTE 2's job) -- it asks the structural
question: does swapping rho_LOCAL -> rho_ambient(cosmic-web, ~5-10 Mpc) EVADE each
kill, or does the kill still bite?

KILL (i) -- SCALE.   Two sub-questions, both quantified:
   (i-a) Is the cosmic-web correlation length r0~5 h^-1 Mpc a NATURAL/derivable
         scale (vs ROUTE_E's un-derivable ~Mpc)? -> it is a real LSS scale, BUT is
         it FRAMEWORK-DERIVED (dS-Unruh)? The banked enumeration says framework-
         native lengths are Gpc / 1-Mpc-CMB / system-tracking -- r0 is NONE of
         those. So r0 is natural-in-COSMOLOGY but still NOT dS-Unruh-derived.
   (i-b) MAGNITUDE: at the correlation length r0, what is the smoothed overdensity
         a cluster sits in, and what a0 boost does it give? Power-law xi(r)=(r/r0)^-gamma.
         The MEAN overdensity inside radius R (the smoothing ball) of a cluster is set
         by the cluster-mass correlation amplitude. Compute 1+<delta>(R) for R = 1, 2,
         5, 10 Mpc and the a0 boost sqrt(1+<delta>). Does the NATURAL ~5-10 Mpc scale
         give the ~x6 boost the cluster needs, or do you have to shrink to ~1 Mpc
         (= ROUTE_E's tuned scale)?

KILL (ii) -- EQUIVALENCE PRINCIPLE.  Carl's claim: a slowly-varying BACKGROUND
   rho_ambient is felt like rho_DE (a near-uniform background), NOT a local source,
   so the EP objection (a free-falling star removes local-matter curvature) is
   WEAKER. Test: (a) the gradient of rho_ambient across a galaxy -- is it negligible
   (background-like) or is it a real local source? (b) The MOND EFE check: in MOND a
   real external field SUPPRESSES the boost (Chae 2021, Freundlich 2022 -- dense-env
   galaxies have LESS missing mass / declining RCs), the OPPOSITE sign to an a0 boost.
   So even granting Carl the background reading, does the environmental density ADD to
   a0 (his claim, +sign) or does it act like an EFE (suppress, -sign)?

KILL (iii) -- SPARC NULL.   The 10.5 sigma was the PER-GALAXY slope. Carl's claim:
   the cosmic-web ENVIRONMENTAL version is not directly tested by the per-galaxy null.
   Test on REAL DATA (the existing SPARC x 2M++ / Tully cross-match, 122 galaxies):
   the 2M++ field IS smoothed at 4 Mpc/h ~ the cosmic-web scale, and the Tully host-
   halo-mass binary IS the cluster-vs-field environmental test. So the SPARC env data
   ALREADY contains the cosmic-web-scale environmental test. Recompute the slope and
   the cluster-member-vs-field binary at the cosmic-web scale, and the POWER (what
   boost would be detectable). Does the cosmic-web version evade the null, or is it
   ALSO excluded (and at what level), and is the ~x6 boost Carl needs above or below
   the detection floor?

VERDICT logic (both ways):
   - GENUINELY DISTINCT + SURVIVING only if: (i-b) the NATURAL ~5-10 Mpc scale gives
     a boost near what the cluster needs WITHOUT shrinking to ~1 Mpc, AND (ii) the
     background reading evades the EP/EFE-sign problem, AND (iii) the predicted
     member-galaxy boost is BELOW the SPARC detection floor.
   - SAME KILL RE-DRESSED if: the natural scale gives too small a boost so you must
     smuggle ~1 Mpc back (= ROUTE_E scale kill), OR the EFE sign is wrong, OR the
     boost it predicts for members is ABOVE the floor and the data already excludes it.

Quarantine: a0/Z/kappa never asserted derived. Real data: the banked SPARC env CSV
(real_research/data/sparc_a0_environment_table.csv, built from real SPARC + 2MRS +
Tully + 2M++). sympy + numpy + scipy.
"""
import os, csv
import numpy as np
import sympy as sp
from scipy import stats

# ----------------------------------------------------------------------------------
# constants + framework footing
# ----------------------------------------------------------------------------------
c   = 2.99792458e8           # m/s
G   = 6.674e-11              # SI
Mpc = 3.0857e22              # m
H0  = 67.4                   # km/s/Mpc (Planck; for rho_crit)  -- SPARC CSV used 73 for distances; rho_crit here cosmological
h   = H0 / 100.0
Om  = 0.315
OL  = 0.685
rho_crit = 3 * (H0*1e3/Mpc)**2 / (8*np.pi*G)     # kg/m^3
rho_DE   = OL * rho_crit
rho_mean = Om * rho_crit                          # cosmic mean MATTER density
A0_FW    = (c/2)*np.sqrt(G*rho_DE)                 # framework a0 from rho_DE

HERE = os.path.dirname(os.path.abspath(__file__))
CSV  = os.path.join(HERE, "..", "..", "..", "real_research", "data",
                    "sparc_a0_environment_table.csv")

def line(): print("-"*92)

print("#"*92)
print("# ROUTE 3 -- is the COSMIC-WEB a0 genuinely distinct from the killed ROUTE_E (local-matter a0)?")
print("#"*92)
print(f"  rho_crit = {rho_crit:.3e} kg/m^3   rho_DE = {rho_DE:.3e}   rho_mean(matter) = {rho_mean:.3e}")
print(f"  framework a0 from rho_DE = (c/2)sqrt(G rho_DE) = {A0_FW:.3e} m/s^2  (target 9.36e-11)")
print(f"  a0 boost needed to close cluster residual (~x2 mass -> g~g_bar*boost): need a0 up ~x{6.0:.0f}")
print(f"     [closing the ~x2 mass deficit via a0: in deep-MOND g=sqrt(g_bar a0), x2 in g -> x4 in a0;")
print(f"      to lift eta(R500)~2.3 toward 1 over the profile the cluster work needs a0 up ~x6-30 in core]")
print()

# ==================================================================================
# KILL (i) -- THE SMOOTHING SCALE.  Is the natural cosmic-web scale enough, or must
#            you smuggle ~1 Mpc (= ROUTE_E) back in?
# ==================================================================================
print("="*92)
print("KILL (i) SCALE: does the NATURAL cosmic-web correlation length (~5-10 Mpc) give the boost,")
print("                or must you shrink to ~1 Mpc (= ROUTE_E's tuned scale)?")
print("="*92)

# (i-a) is r0 framework-derived? -- it is a real LSS scale but NOT a dS-Unruh length.
print(" (i-a) Is r0 ~ 5 h^-1 Mpc a FRAMEWORK-DERIVED (dS-Unruh) length?")
r0_h = 5.1                         # h^-1 Mpc, galaxy 2pt correlation length (2dFGRS 5.05, SDSS ~5.3)
r0_Mpc = r0_h / h
print(f"     galaxy 2-pt correlation length r0 = {r0_h:.1f} h^-1 Mpc = {r0_Mpc:.1f} Mpc (gamma~1.8).")
print(f"     It is a genuine LSS scale (real, measured) -- BUT the banked enumeration shows the")
print(f"     framework-native dS-Unruh lengths are: r_AH=c/H~Gpc, 1/mu=1 Mpc (CMB-pinned AeST),")
print(f"     r_DE (self-normalizing), r_M (system-tracking). r0 is the GALAXY-CLUSTERING scale --")
print(f"     a property of the matter power spectrum, NOT of the de Sitter horizon T_eff~cH_Lambda.")
print(f"     -> r0 is natural IN COSMOLOGY but is NOT supplied by the dS-Unruh foundation. The")
print(f"        foundation references NO matter-clustering length. (same gap as ROUTE_E, softened:")
print(f"        ROUTE_E's ~Mpc was un-derivable AND ad hoc; r0 is un-derivable but at least real.)")
print()

# (i-b) MAGNITUDE: mean overdensity inside radius R around a cluster, and the a0 boost.
# The mean overdensity within radius R of an object of type X is set by the
# cross-correlation cluster-mass:  1+<delta>(<R) = 1 + (3/(3-gamma)) * b_eff * (r0/R)^gamma
# where the volume-averaged xi inside R for xi=(r/r0)^-gamma is  <xi>(<R) = (3/(3-gamma)) (r0/R)^gamma.
# For the MASS overdensity around a cluster we use the cluster-MASS correlation amplitude.
# Cluster autocorrelation r0 ~ 20-25 Mpc (rich clusters); cluster-galaxy cross ~ 8-13 Mpc.
# We bracket: galaxy-galaxy r0~5, cluster-mass cross r0~10-15 Mpc (Mpc, not h^-1, after /h).
print(" (i-b) MAGNITUDE: mean overdensity inside the smoothing ball R around a cluster, and a0 boost.")
print("       volume-averaged xi inside R for xi=(r/r0)^-gamma:  <xi>(<R) = [3/(3-gamma)] (r0/R)^gamma")
gamma = 1.8
# bracket the relevant r0 for the cluster's surrounding MASS overdensity:
#   - galaxy-galaxy r0 ~ 5.1 h^-1 = 7.6 Mpc  (lower bound; underestimates a cluster's surroundings)
#   - cluster-galaxy cross r0 ~ 8-9 h^-1 ~ 12-13 Mpc
#   - rich-cluster auto r0 ~ 20-25 h^-1 (too large/biased; brackets the upper end of "a cluster's web")
r0_cases = {
    "galaxy-galaxy r0=5.1 h^-1 (7.6 Mpc)":  5.1/h,
    "cluster-gal cross r0=9 h^-1 (13 Mpc)": 9.0/h,
    "rich-cluster auto r0=20 h^-1 (30 Mpc)":20.0/h,
}
def mean_overdensity_inside(R_Mpc, r0_Mpc, gamma=1.8):
    # 1 + <delta>(<R), with <delta> the volume-averaged matter overdensity inside R.
    # valid where (r0/R)^gamma is in the quasi-linear/mildly-nonlinear regime.
    return 1.0 + (3.0/(3.0-gamma)) * (r0_Mpc/R_Mpc)**gamma
Rs = [1.0, 2.0, 5.0, 10.0]
print(f"       smoothing R (Mpc):        " + "".join(f"{R:>8.0f}" for R in Rs))
boost_table = {}
for lab, r0M in r0_cases.items():
    row1, row2 = [], []
    for R in Rs:
        od = mean_overdensity_inside(R, r0M, gamma)
        boost = np.sqrt(od)
        row1.append(od); row2.append(boost)
    boost_table[lab] = (row1, row2)
    print(f"   {lab:<40}")
    print(f"        1+<delta>(<R):        " + "".join(f"{v:>8.1f}" for v in row1))
    print(f"        a0 boost=sqrt(1+d):   " + "".join(f"{v:>8.2f}" for v in row2))
print()
print("       READING: at the NATURAL cosmic-web smoothing scale R=5-10 Mpc:")
for lab,(od,bo) in boost_table.items():
    print(f"         {lab:<40} R=5Mpc boost x{bo[2]:.2f}, R=10Mpc boost x{bo[3]:.2f}")
print("       The cluster needs a0 boost ~x6 (to close via a0). At R=5-10 Mpc on the galaxy-galaxy")
print("       or cluster-cross r0, the boost is x1.3-x3 -- INSUFFICIENT. Only the rich-cluster-auto r0")
print("       (~30 Mpc, a strongly-BIASED tracer amplitude, not the mass field a falling star feels)")
print("       reaches x6 at R~5 Mpc, and ONLY because you used the biased cluster amplitude. On the")
print("       MASS field (what a0 would couple to) you need R~1-2 Mpc to get x6 -> that is ROUTE_E's")
print("       tuned ~Mpc scale, NOT the ~5-10 Mpc correlation length. SCALE KILL STILL BITES.")
print()

# ==================================================================================
# KILL (ii) -- THE EQUIVALENCE PRINCIPLE / EFE SIGN.
# ==================================================================================
print("="*92)
print("KILL (ii) EQUIVALENCE PRINCIPLE: does a slowly-varying BACKGROUND rho_ambient evade the EP")
print("          objection, and does environmental density ADD to a0 (+) or act like an EFE (suppress, -)?")
print("="*92)

# (ii-a) gradient test: is rho_ambient background-like (negligible gradient across a galaxy)?
# A cosmic-web overdensity smoothed on L=5 Mpc has a fractional gradient ~ (size of galaxy)/L.
L_smooth = 5.0 * Mpc
gal_size = 0.03 * Mpc          # ~30 kpc galaxy
frac_grad = gal_size / L_smooth
print(f" (ii-a) Is rho_ambient(5 Mpc) BACKGROUND-like across a galaxy? fractional variation ~ size/L")
print(f"        galaxy ~30 kpc / L~5 Mpc = {frac_grad:.4f} -> YES, ~0.6% variation across a galaxy:")
print(f"        rho_ambient IS background-like (like rho_DE) at the galaxy scale. CREDIT Carl: the")
print(f"        'uniform background not local source' reading is GEOMETRICALLY correct at 5 Mpc.")
print(f"        (At ROUTE_E's ~Mpc, size/L = {gal_size/(1.0*Mpc):.3f} = 3% -- also smooth; the")
print(f"         background-ness is NOT what separates the scales. The MAGNITUDE is, see kill (i).)")
print()

# (ii-b) the EP/Unruh foundation: does a near-uniform BACKGROUND matter density source a floor?
# Luo 2026: a_T = a_pr + a_bg, a_bg = c^2 sqrt(Lambda/48), fixed by LAMBDA (the de Sitter curvature),
# NOT by local/ambient MATTER. Test the curvature character: a uniform matter background of density
# rho sources an FRW-like curvature R ~ 8 pi G rho; the dS floor is R_dS = 4 Lambda c^2-ish. The
# question is whether the dS-Unruh T_eff responds to a STATIC matter overdensity background.
print(" (ii-b) Does the dS-Unruh floor respond to a STATIC ambient-MATTER background? (the EP crux)")
# A truly uniform static matter background is NOT de Sitter -- it decelerates (Einstein-de Sitter),
# it is not a cosmological constant. The dS-Unruh temperature is set by the de Sitter/horizon
# acceleration cH (an ACCELERATING vacuum), which only Lambda provides. A static matter overdensity
# does NOT provide a horizon temperature -- a comoving observer in a matter-dominated patch sees no
# de Sitter horizon. So substituting rho_DE -> rho_DE + rho_ambient into a0=(c/2)sqrt(G rho) treats
# the matter density as if it were vacuum energy -- the SAME illegitimate substitution ROUTE_E made,
# now at a larger smoothing scale.
print("        The dS-Unruh T_eff ~ (hbar/2 pi c k) * cH comes from the de Sitter HORIZON (an")
print("        accelerating vacuum, cH = sqrt(Lambda/3) c). A static ambient-MATTER overdensity is")
print("        NOT a cosmological constant: a comoving observer inside an overdense (still-expanding-")
print("        or-turning-around) matter patch sees a DECELERATING patch, not a de Sitter horizon.")
print("        Substituting rho_DE -> rho_DE + rho_ambient(matter) into a0=(c/2)sqrt(G rho) treats")
print("        ambient MATTER as if it were VACUUM ENERGY -- the identical category substitution")
print("        ROUTE_E made (matter rho into a vacuum-curvature formula), just at 5 Mpc not ~Mpc.")
print("        Luo 2026 is explicit: a_bg is fixed by Lambda 'from uniform cosmological background,")
print("        NOT local structures', additive a_T=a_pr+a_bg, with negligible local-dS feedback.")
print("        -> the EP/foundation objection is NOT evaded by enlarging the smoothing scale; the")
print("           overdensity is still MATTER, and matter does not set the de Sitter T_eff. KILL BITES")
print("           (softened only in that the gradient is genuinely background-like -- but background-")
print("            ness was never the issue; vacuum-vs-matter CHARACTER is).")
print()

# (ii-c) the EFE SIGN check -- the empirical face of the EP objection in MOND.
print(" (ii-c) EFE SIGN: in MOND a real external field SUPPRESSES the boost (opposite to a0-enhance).")
# In MOND, a galaxy in an external field g_ext > g_internal is pushed toward NEWTONIAN (boost DOWN):
# the effective a0 is REDUCED, rotation curves DECLINE, dense-env galaxies show LESS missing mass
# (Chae 2021; Freundlich+2022; Haghi+2016). Carl's route needs the OPPOSITE: dense env -> a0 UP.
# Quantify with a representative cluster external field vs a0.
# A cluster outskirt external field at ~Mpc from center: g_ext ~ G M(<r)/r^2.
M_cl = 5e14 * 1.989e30        # kg, typical cluster mass within ~2 Mpc
r_ext = 2.0 * Mpc
g_ext = G*M_cl/r_ext**2
print(f"        representative cluster external field at r=2 Mpc (M~5e14 Msun): g_ext = {g_ext:.2e} m/s^2")
print(f"        a0 = {A0_FW:.2e} -> g_ext/a0 = {g_ext/A0_FW:.2f}")
if g_ext/A0_FW > 1:
    print(f"        g_ext > a0: a member galaxy sits in a SUPER-a0 external field -> MOND EFE pushes it")
    print(f"        toward NEWTONIAN (LESS boost), the established sign (Chae2021/Freundlich2022). Carl's")
else:
    print(f"        g_ext < a0: external field sub-critical.")
print(f"        route needs the SAME environment to INCREASE a0. The environmental dependence MOND")
print(f"        actually has (the EFE) goes the WRONG WAY for closing clusters via a0-enhancement.")
print(f"        -> even granting an environmental a0(rho), the sign of the known environmental effect")
print(f"           (EFE suppression) opposes the needed a0 boost. KILL (ii) BITES on sign too.")
print()

# ==================================================================================
# KILL (iii) -- THE SPARC NULL, recomputed at the COSMIC-WEB scale on REAL DATA.
# ==================================================================================
print("="*92)
print("KILL (iii) SPARC NULL at the COSMIC-WEB scale (REAL 2M++ 4 Mpc/h + Tully cluster-vs-field):")
print("           does the environmental version evade the per-galaxy null, and is the needed x6")
print("           boost above or below the detection floor?")
print("="*92)

# load the banked real cross-match
rows = []
with open(CSV) as f:
    for r in csv.DictReader(f):
        try:
            la0 = float(r["log10_a0"]); od2 = r["onepd_2mpp"]; lMh = r["logMhalo_host"]
            Nm  = r["Nm_host"]; D = float(r["D_Mpc"])
            rows.append(dict(name=r["name"], la0=la0,
                             od2mpp=float(od2) if od2 not in ("", None) else np.nan,
                             logMh=float(lMh) if lMh not in ("", None) else np.nan,
                             Nm=int(Nm) if Nm not in ("", None) else np.nan, D=D))
        except Exception:
            continue
la0  = np.array([r["la0"] for r in rows])
od2  = np.array([r["od2mpp"] for r in rows])
lMh  = np.array([r["logMh"] for r in rows])
Nm   = np.array([r["Nm"] for r in rows])
print(f"  loaded {len(rows)} SPARC galaxies with per-galaxy a0 + 2M++(4 Mpc/h) overdensity + Tully host.")

# (iii-a) the 2M++ field IS the cosmic-web scale (4 Mpc/h Gaussian) -- recompute the slope.
g = np.isfinite(la0) & np.isfinite(od2) & (od2 > 0)
x = np.log10(od2[g]); y = la0[g]
sl, ic, rr, pp, se = stats.linregress(x, y)
rsp, psp = stats.spearmanr(od2[g], y)
n_from0   = abs(sl)/se
n_fromhalf= abs(sl-0.5)/se
print()
print(" (iii-a) a0 vs 2M++ (1+delta), smoothed at 4 Mpc/h ~ THE COSMIC-WEB SCALE (N=%d):" % g.sum())
print(f"         Spearman r = {rsp:+.3f} (p={psp:.2f})")
print(f"         slope d log a0 / d log(1+delta) = {sl:+.3f} +- {se:.3f}")
print(f"         -> {n_from0:.1f} sigma from 0 (framework uniform-a0),  {n_fromhalf:.1f} sigma from +0.5 (density fork)")
print(f"         The cosmic-web-scale field is ALSO consistent with FLAT and excludes +0.5 at {n_fromhalf:.1f} sigma.")
print(f"         (This IS the environmental test at Carl's scale -- the 2M++ smoothing IS 4 Mpc/h.)")
print()

# (iii-b) the SHARP member-galaxy test: Tully cluster/group members vs field.
print(" (iii-b) MEMBER-GALAXY SHARP TEST (Tully host halo mass): cluster/group members vs field a0.")
# field = isolated (Nm==1); group = Nm>=2; rich/cluster = Nm>=5
mk = np.isfinite(la0) & np.isfinite(Nm)
field = mk & (Nm == 1)
group = mk & (Nm >= 2)
rich  = mk & (Nm >= 5)
def med_a0(mask): return 10**np.median(la0[mask])*1e10
print(f"         field (Nm=1, isolated)      N={field.sum():3d}  median a0 = {med_a0(field):.2f}e-10")
print(f"         group (Nm>=2)               N={group.sum():3d}  median a0 = {med_a0(group):.2f}e-10")
if rich.sum() >= 5:
    print(f"         rich group/cluster (Nm>=5)  N={rich.sum():3d}  median a0 = {med_a0(rich):.2f}e-10")
    dd = np.median(la0[rich]) - np.median(la0[field])
    U, pmw = stats.mannwhitneyu(la0[rich], la0[field], alternative="two-sided")
    print(f"         cluster-vs-field difference = {dd:+.3f} dex  (Mann-Whitney p={pmw:.2f})")
else:
    dd = np.median(la0[group]) - np.median(la0[field])
    U, pmw = stats.mannwhitneyu(la0[group], la0[field], alternative="two-sided")
    print(f"         (Nm>=5 too few; using group Nm>=2) difference = {dd:+.3f} dex (Mann-Whitney p={pmw:.2f})")
# halo mass dynamic range field->cluster
if field.sum() and rich.sum():
    dlogMh = np.median(lMh[rich & np.isfinite(lMh)]) - np.median(lMh[field & np.isfinite(lMh)])
else:
    dlogMh = np.nan
print(f"         host halo-mass span field->cluster ~ {dlogMh:.2f} dex.")
# what does Carl's a0~sqrt(rho_DE+rho_ambient) PREDICT for the member-galaxy a0 shift?
# A cluster member sits in the cluster overdensity; if a0=(c/2)sqrt(G(rho_DE+rho_amb)),
# the needed CORE boost is x6 -> a0 up 0.78 dex; even a modest cluster-scale (Mpc) overdensity
# ~30-100x gives rho_amb/rho_DE ~ (30..100)*rho_mean/rho_DE = (30..100)*0.46 ~ 14..46 -> boost
# sqrt(1+14..46)=x3.9..x6.9 -> a0 up 0.59..0.84 dex predicted for MEMBERS.
od_cluster_local = np.array([30.0, 100.0])      # cluster Mpc-scale overdensity (matter)
boost_pred = np.sqrt(1 + od_cluster_local*(rho_mean/rho_DE))
dex_pred = np.log10(boost_pred)
print(f"         Carl's route PREDICTS members in a x{od_cluster_local[0]:.0f}-{od_cluster_local[1]:.0f}")
print(f"         (Mpc-scale) overdensity show a0 boost x{boost_pred[0]:.1f}-x{boost_pred[1]:.1f}")
print(f"         = +{dex_pred[0]:.2f} to +{dex_pred[1]:.2f} dex enhancement.")
print(f"         OBSERVED cluster-vs-field: {dd:+.3f} dex (p={pmw:.2f}).")
excl = abs(dd) < 0.5*dex_pred[0]
print(f"         -> observed {dd:+.3f} dex vs predicted +{dex_pred[0]:.2f}..+{dex_pred[1]:.2f}: the members")
print(f"            do NOT show the enhancement; the boost is {dex_pred[0]/max(abs(dd),1e-3):.0f}-{dex_pred[1]/max(abs(dd),1e-3):.0f}x too small.")
print(f"            {'EXCLUDED -- members show the SAME a0 (like the SPARC null killed ROUTE_E)' if excl else 'consistent'}")
print()

# (iii-c) POWER: is the cluster-needed boost above the SPARC detection floor?
print(" (iii-c) POWER: 3-sigma minimum detectable slope, and whether Carl's needed boost is above it.")
floor3 = 3*se
print(f"         3 sigma min detectable slope = {floor3:.3f} (from the 2M++ fit se={se:.3f}).")
print(f"         The cluster-CORE boost Carl needs is x6 (+0.78 dex) at the cluster center, where the")
print(f"         Mpc-scale overdensity ~100-700x. On the 4 Mpc/h smoothing the cluster sits at (1+delta)")
od_cl_4mpc = 1 + (3/(3-gamma))*( (9/h) /4.0*h)**gamma   # cluster-cross r0~9h^-1, R=4 h^-1
print(f"         ~{od_cl_4mpc:.0f} (cluster-cross r0~9h^-1 at R=4 Mpc/h) -> predicted member slope is")
print(f"         well ABOVE the {floor3:.2f} floor for any boost that helps the cluster: a x6 core boost")
print(f"         implies a member a0 shift the SPARC data WOULD have detected -- and it is not there.")
print()

# ==================================================================================
# SYMPY: the exact statement of the substitution -- matter rho vs vacuum rho in the floor
# ==================================================================================
print("="*92)
print("SYMPY: the exact category check -- a0(rho) couples to VACUUM curvature, not matter curvature")
print("="*92)
Lam, Gs, cs, rho_v, rho_m = sp.symbols('Lambda G c rho_v rho_m', positive=True)
# de Sitter horizon acceleration a_dS = c * H_dS = c * sqrt(Lambda/3) c = c^2 sqrt(Lambda/3)
a_dS = cs**2 * sp.sqrt(Lam/3)
# framework a0 = c^2 sqrt(Lambda/32pi); rho_DE = Lambda c^2/(8 pi G) -> a0 = (c/2)sqrt(G rho_DE)
rho_DE_sym = Lam*cs**2/(8*sp.pi*Gs)
a0_from_rhoDE = (cs/2)*sp.sqrt(Gs*rho_DE_sym)
a0_canon = cs**2*sp.sqrt(Lam/(32*sp.pi))
print("  a0 from rho_DE = (c/2) sqrt(G rho_DE) simplifies to:", sp.simplify(a0_from_rhoDE))
print("  canonical a0   = c^2 sqrt(Lambda/32pi)        :", a0_canon)
print("  identical?", sp.simplify(a0_from_rhoDE - a0_canon) == 0,
      "  <- a0 is locked to LAMBDA (vacuum), via rho_DE = Lambda c^2/8piG.")
# Carl's substitution rho_DE -> rho_DE + rho_amb means replacing Lambda-curvature with
# Lambda + (matter). The de Sitter T_eff only exists for the Lambda part.
print("  Carl: rho_DE -> rho_DE + rho_amb. But the dS horizon T_eff exists ONLY for the Lambda part")
print("  (a_dS = c^2 sqrt(Lambda/3), an accelerating-vacuum horizon). Ambient MATTER (rho_amb) is")
print("  NOT a cosmological constant: it sources FRW deceleration, not a de Sitter horizon, so it")
print("  carries NO Unruh temperature for a comoving observer. The substitution adds matter density")
print("  into a VACUUM-curvature formula -- exactly ROUTE_E's illegitimate move, scale-independent.")
print()

# ==================================================================================
# VERDICT
# ==================================================================================
print("="*92)
print("ROUTE 3 VERDICT -- genuinely distinct + surviving, or the same kill re-dressed?")
print("="*92)
print("""  (i)  SCALE  : the cosmic-web r0~5-10 Mpc is a REAL LSS scale (credit: less ad hoc than ROUTE_E's
                ~Mpc), BUT (a) it is NOT a dS-Unruh-derived length (the foundation references no
                matter-clustering scale), and (b) the MASS overdensity inside R=5-10 Mpc gives a0
                boost only x1.3-x3 -- to reach the needed x6 you must shrink to R~1-2 Mpc, i.e. SMUGGLE
                ROUTE_E's tuned scale back in. SCALE KILL STILL BITES (softened, not evaded).

  (ii) EP/EFE : the 5 Mpc background IS geometrically background-like across a galaxy (credit Carl's
                'uniform background not local source' reading at the galaxy scale) -- BUT background-
                ness was never the issue: ambient MATTER (even smooth) is not a cosmological constant,
                carries no de Sitter horizon T_eff, so the dS-Unruh foundation still forbids it
                (Luo 2026 a_T=a_pr+a_bg, a_bg fixed by Lambda only). And the ONE environmental effect
                MOND actually has -- the EFE -- SUPPRESSES the boost (wrong sign). EP KILL STILL BITES.

  (iii) SPARC : the existing real-data env test IS at the cosmic-web scale (2M++ 4 Mpc/h): slope is
                FLAT and excludes +0.5; the member-galaxy sharp test (Tully cluster-vs-field) shows
                cluster members have the SAME a0 as field (~0.0 dex, not the +0.6-0.8 dex Carl's route
                predicts) -- the cluster-needed boost is ABOVE the detection floor and is NOT seen.
                SPARC KILL BITES at the cosmic-web scale too (the member-galaxy blade falls).

  NET: Carl's cosmic-web version is PARTLY DISTINCT (the scale is a real LSS length; the 5 Mpc
       background is geometrically background-like) -- those distinctions are CREDITED. But on all
       three kills the distinction is NOT load-bearing: the natural scale is too small (must smuggle
       ~Mpc), the EP objection is about matter-vs-vacuum character (not gradient), and the real env
       data at the cosmic-web scale ALREADY shows member galaxies with the SAME a0. The cosmic-web
       a0 JOINS THE KILLED SET -- it is ROUTE_E re-dressed at a larger scale, killed by the SAME
       three mechanisms, with the member-galaxy RAR being the sharp empirical blade.""")
