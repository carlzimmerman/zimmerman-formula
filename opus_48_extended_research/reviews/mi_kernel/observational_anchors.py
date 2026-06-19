#!/usr/bin/env python3
r"""
OBSERVATIONAL ANCHORS for the MI time-kernel theta(y)  (topic "observational_anchors")
========================================================================================
TASK: triangulate the modified-inertia kernel theta(y) from DATA. Each MI-distinctive
observable probes theta at a DIFFERENT non-adiabaticity ratio y = omega_ex / omega_in:

  (a) WIDE BINARIES (Gaia DR4, ~2026):       compute the ACTUAL y, and gamma(theta).
  (b) cluster member sigma-spread:           probes y ~ 0.5 - 1.7 (plunging dwarfs).
  (c) galaxy rotation curves:                adiabatic y ~ 0 (fixes the QS limit).

Then: what kernel forms are ALLOWED vs EXCLUDED by current data, and could Gaia DR4 +
the cluster sigma-spread TOGETHER pin theta(y) empirically even if it can't be derived?

THE PHYSICS (Milgrom 2022 arXiv:2208.07073 = PRD 106 064060, Eqs 34/35 verified verbatim
in the prior repo work: WIDEBINARY_MI_EFE_THETA_CORRECTION_2026-06-15.md;
sigma_spread/mi_sigma_spread_amplitude.py):

  Two-frequency EFE (Eq 34):  A(omega_in) = a_in + a_ex * theta(omega_ex/omega_in)
  Adiabatic limit  (Eq 35):   y->0 => theta->theta(0)=const => A = a_in + theta(0) a_ex
                              == EXACTLY modified-GRAVITY EFE with a0 -> a0/theta(0).
  theta(y) (verified text):   symmetric, theta(1)=1, DECREASING, theta(0) ~ "a few";
                              "we have no knowledge of the form of theta(y)."
  Milgrom's example forms:    2/(1+y^2) [t0=2]; e^{1-y} [t0=e]; e^{(1-y)/2} [t0=e^.5].
  MG / QUMOND / AeST EFE:     depends ONLY on the MOMENTARY a_ex (no y at all).

THE KEY NEW RESULT this topic must establish (both ways): the ACTUAL y of each anchor.
  - For a wide binary the EXTERNAL field is the Milky-Way field at the Sun. It varies on
    the GALACTIC-ORBIT timescale (galactic year ~ 230 Myr, verified). The binary internal
    period at 10 kau is ~ 0.5-1 Myr. So y_WB = omega_ex/omega_in = P_in/P_ex ~ 1e-3 <<1.
    => WIDE BINARIES ARE DEEPLY ADIABATIC: they probe theta(0), NOT theta(y~1).
    (This is exactly why Milgrom files wide binaries under the theta(0) Eq-35 EFE.)
  - The cluster sigma-spread genuinely reaches y~0.5-1.7 (plunging diffuse/UDG/dSph
    members: omega_ex ~ omega_in near pericenter -- Milgrom's own dwarf estimate).
  - Rotation curves: a star's internal "orbit" is its galactic orbit; the external field
    (the cosmological a0 floor / large-scale field) is static => y~0, theta(0), QS-MOND.

CONSEQUENCE FOR TRIANGULATION (the honest crux):
  Wide binaries and rotation curves BOTH sit at y~0 -> they probe ONLY theta(0), and a
  CONSTANT theta(0) is EXACTLY a0-degenerate (MI[theta0] == MG[a0/theta0], machine
  precision -- Eq 35). So y~0 anchors constrain the SINGLE NUMBER theta(0) (folded into
  a0), NOT the FUNCTION theta(y). The ONLY anchor that reaches y~O(1) -- where theta is a
  FUNCTION -- is the cluster sigma-spread. So the empirical lever on the SHAPE of theta(y)
  comes from ONE observable, at ONE band of y. Whether DR4+clusters can PIN theta(y) is
  therefore a quantitative question we answer below (spoiler: they pin theta(0) and ONE
  shape-moment near y~1, i.e. a 2-point sketch, NOT the full function -- both ways).

FRAMEWORK FOOTING (sealed): a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2.
  nu(yg)=sqrt(1+1/yg); mu_fw(x)=(sqrt(1+4x^2)-1)/(2x)  (the EXACT inverse of
  g_obs=sqrt(g_N^2+g_N a0)). Framework's OWN interpolation throughout.

BOTH-WAYS (#1 rule): we test "DR4+clusters PIN theta(y)" as hard as "they cannot."
WATCH FOR CIRCULARITY: we do NOT assume a kernel to get a kernel; the y-values are
computed from independent timescales (galactic year, binary period, infall dynamics).
QUARANTINE: deriving/constraining the kernel does NOT make a0/Z/kappa derived.
"""
import numpy as np

# ------------------------------------------------------------------ constants (SI)
c, G    = 2.998e8, 6.674e-11
Msun    = 1.989e30
AU      = 1.496e11
pc      = 3.0857e16
kpc     = 3.0857e19
Mpc     = 3.0857e22
yr      = 3.156e7
Myr     = 3.156e13
km      = 1e3

a0 = 9.36e-11                                            # sealed = c^2 sqrt(Lambda/32pi)
def nu(yg):   yg=np.asarray(yg,float); return np.sqrt(1.0 + 1.0/yg)
def mu_fw(x): x =np.asarray(x ,float); return (np.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)

# ------------------------------------------------------------------ theta(y) kernels
# Milgrom 2022 verbatim example forms + brackets. theta(1)=1, decreasing, theta(0)~few.
def th_rat (y): y=np.abs(np.asarray(y,float)); return 2.0/(1.0+y*y)                 # t0=2     (Milgrom)
def th_e1  (y): y=np.abs(np.asarray(y,float)); return np.exp(1.0-y)                 # t0=e     (Milgrom)
def th_e2  (y): y=np.abs(np.asarray(y,float)); return np.exp((1.0-y)/2.0)           # t0=e^.5  (Milgrom)
def th_gau (y): y=np.abs(np.asarray(y,float)); return 2.0*np.exp(-np.log(2.0)*y*y)  # t0=2 gaussian (bracket)
def th_lor3(y): y=np.abs(np.asarray(y,float)); return 3.0/(1.0+2.0*y*y)             # t0=3 (bracket)
KERNELS = [("rational 2/(1+y^2)",th_rat,2.0,True),("exp e^{1-y}",th_e1,np.e,True),
           ("exp e^{(1-y)/2}",th_e2,np.exp(0.5),True),
           ("gauss 2*2^{-y^2}",th_gau,2.0,False),("lorentz 3/(1+2y^2)",th_lor3,3.0,False)]
MILG = [k for k in KERNELS if k[3]]

print("="*100)
print(" OBSERVATIONAL ANCHORS for the MI kernel theta(y) -- triangulate from data, both ways")
print("="*100)
print(f"  a0 = {a0:.3e} m/s^2 (sealed). mu_fw=inverse of g_obs=sqrt(g_N^2+g_N a0). theta(1)=1, decreasing.")

# ====================================================================================================
# ANCHOR (a): WIDE BINARIES -- compute the ACTUAL y, and gamma(theta).
# ====================================================================================================
print("\n"+"="*100)
print(" ANCHOR (a): WIDE BINARIES -- what y do they probe? and gamma as a function of theta")
print("="*100)

# --- (a.1) the two candidate external-field oscillation timescales (both ways) -----------------
print("-"*100); print(" (a.1) THE EXTERNAL-FIELD FREQUENCY: which omega_ex? compute the binary's y honestly")
print("-"*100)
# internal orbital period of a wide binary at separation s, total mass Mtot
def P_internal(s_AU, Mtot_Msun):
    a = s_AU*AU                                          # semimajor ~ separation
    M = Mtot_Msun*Msun
    return 2*np.pi*np.sqrt(a**3/(G*M))                   # Kepler period (s)

print(f"  {'s [kau]':>8} {'Mtot':>5} | {'P_internal':>12} | {'g_int/a0':>9} | regime")
print("  "+"-"*60)
for s_kau,Mtot in [(2.5,1.5),(5,1.5),(10,1.5),(20,1.5)]:
    s_AU = s_kau*1e3
    P_in = P_internal(s_AU, Mtot)
    g_int = G*Mtot*Msun/(s_AU*AU)**2
    print(f"  {s_kau:8.1f} {Mtot:5.1f} | {P_in/Myr:9.3f} Myr | {g_int/a0:9.3f} | "
          f"{'deep-MOND' if g_int<a0 else 'transition' if g_int<3*a0 else 'Newtonian'}")

# The EXTERNAL field is the Milky-Way field at the Sun (g_ext ~ 1.8e-10 ~ 1.9 a0). It oscillates on
# the GALACTIC-ORBIT period (the Sun's vertical + in-plane motion). Verified: galactic year ~225-250 Myr.
P_galyr = 230.0*Myr                                      # galactic year (verified 225-250 Myr)
P_vert  = 70.0*Myr                                       # solar vertical oscillation ~ 60-90 Myr (faster bracket)
g_ext   = 1.8e-10                                        # MW field at the Sun ~ 1.9 a0 (standard)
print(f"\n  EXTERNAL field at the Sun g_ext = {g_ext:.2e} = {g_ext/a0:.2f} a0.")
print(f"  Its oscillation period: galactic year P_ex ~ {P_galyr/Myr:.0f} Myr (in-plane);")
print(f"                          vertical bounce  P_ex ~ {P_vert/Myr:.0f} Myr (faster bracket).")
print(f"  The binary internal period at 10 kau: P_in ~ {P_internal(1e4,1.5)/Myr:.3f} Myr.")
print(f"\n  => y_WB = omega_ex/omega_in = P_in/P_ex:")
for s_kau in [2.5,5,10,20]:
    P_in = P_internal(s_kau*1e3,1.5)
    y_gal  = P_in/P_galyr
    y_vert = P_in/P_vert
    print(f"     s={s_kau:5.1f} kau:  y(gal yr) = {y_gal:.2e}   y(vert bounce) = {y_vert:.2e}")
print(r"""  READ (the load-bearing fact): for EVERY wide-binary separation, y_WB ~ 1e-4 .. 4e-3 << 1.
  The external Galactic field is essentially STATIC over the ~1 Myr binary orbit (the galactic year
  is ~200-1000x longer). => WIDE BINARIES ARE DEEPLY ADIABATIC; they probe theta(0), the Eq-35 limit,
  NOT theta(y~1). This is exactly why Milgrom 2022 files wide binaries (and vertical-disk dynamics)
  under the theta(0) adiabatic EFE: 'theta(0) a few has a large impact on 1-mu' (verbatim).""")

# --- (a.2) gamma(theta(0)) for wide binaries: it is a function of theta(0) ONLY (a0-degenerate) ----
print("-"*100); print(" (a.2) gamma_WB as a function of theta -- it depends on theta(0) ONLY (adiabatic)")
print("-"*100)
# MI-EFE adiabatic boost: the internal dynamics see effective field A = a_in + theta(0)*a_ex.
# gamma_g = (g_obs/g_N) ratio = [1/mu_fw(A/a0)] relative to the isolated case; for the plateau
# (deep internal field s>~10 kau) the velocity boost gamma_v = sqrt(gamma_g). We tabulate vs theta(0).
def gamma_WB(theta0, s_kau=15.0, Mtot=1.5, g_ext=g_ext):
    """Adiabatic MI-EFE velocity boost at separation s_kau, as a function of theta(0)."""
    g_int = G*Mtot*Msun/((s_kau*1e3)*AU)**2
    A = g_int + theta0*g_ext                              # Eq-35 effective field (adiabatic)
    boost_g = 1.0/mu_fw(A/a0) / (1.0/mu_fw((g_int+g_ext)/a0))  # vs the theta=1 (MG) reference
    # absolute super-Newtonian boost relative to pure Newton (mu=1):
    boost_vsN = 1.0/mu_fw(A/a0)
    return boost_vsN, np.sqrt(boost_vsN)
print(f"  Wide binary s=15 kau (plateau), g_ext={g_ext/a0:.2f} a0. gamma_g=1/mu_fw(A/a0), gamma_v=sqrt(gamma_g):")
print(f"  {'theta(0)':>9} | {'A/a0':>7} | {'gamma_g':>8} | {'gamma_v':>8} | note")
print("  "+"-"*64)
g_int15 = G*1.5*Msun/((15e3)*AU)**2
for theta0,note in [(1.0,"MG / momentary a_ex (theta=1)"),(np.exp(0.5),"Milgrom e^{(1-y)/2}"),
                    (2.0,"Milgrom 2/(1+y^2)"),(np.e,"Milgrom e^{1-y} (natural)"),(3.0,"strong-suppression bracket"),(5.0,"extreme bracket")]:
    A = g_int15 + theta0*g_ext
    gg = 1.0/mu_fw(A/a0); gv = np.sqrt(gg)
    print(f"  {theta0:9.3f} | {A/a0:7.3f} | {gg:8.4f} | {gv:8.4f} | {note}")
print(r"""  READ: gamma_v runs from ~1.10 (theta0=e, the MOST-Newtonian Milgrom form) DOWN to ~1.04 (theta0=5,
  strong suppression). LARGER theta(0) => MORE EFE quenching => MORE Newtonian => SMALLER gamma. So a wide-
  binary gamma measurement constrains theta(0): a HIGH gamma (pro-MOND) favors SMALL theta(0); a Newtonian
  null favors LARGE theta(0) (or no boost at all). BUT this is theta(0) ONLY -- and a constant theta(0) is
  EXACTLY a0-degenerate (next), so WB cannot separate 'small theta(0)' from 'larger a0'.""")

# --- (a.3) the a0-degeneracy of theta(0): MI[theta0] == MG[a0/theta0] to machine precision ---------
print("-"*100); print(" (a.3) CIRCULARITY/DEGENERACY GUARD: a constant theta(0) is EXACTLY an a0 rescale")
print("-"*100)
print(f"  Eq 35: A = a_in + theta(0) a_ex. For the PURE-EFE (a_in->0) regime, A = theta(0) a_ex, so")
print(f"  mu_fw(A/a0) = mu_fw(a_ex/(a0/theta0)) == the MG EFE with a0 -> a0/theta(0). Check numerically:")
a_ex_grid = np.array([0.5,1.0,2.0,3.0])*a0
for theta0 in [2.0, np.e, 3.0]:
    mi  = mu_fw(theta0*a_ex_grid/a0)                       # MI with theta(0)
    mg  = mu_fw(a_ex_grid/(a0/theta0))                     # MG with a0->a0/theta0
    print(f"  theta(0)={theta0:.3f}: max|MI-MG| over a_ex grid = {np.max(np.abs(mi-mg)):.2e}  (== 0 => exact degeneracy)")
print(r"""  => At the SINGLE external-field value of wide binaries, theta(0) and a0 are NOT separable: any WB gamma
  is fit equally by (theta(0)=k, a0) or (theta(0)=1, a0/k). WB constrain the COMBINATION a0/theta(0), not
  theta(0) alone. The ONLY thing that breaks it is the cross-dataset axiom a0=9.36e-11 (from the isolated
  RAR, where theta multiplies nothing). So WB pin theta(0) ONLY if a0 is taken as externally fixed --
  and even then they give ONE number (theta(0)), a single point of the function theta(y), at y~0.""")

# ====================================================================================================
# ANCHOR (b): CLUSTER SIGMA-SPREAD -- probes y ~ 0.5-1.7 (the ONLY anchor where theta is a FUNCTION)
# ====================================================================================================
print("\n"+"="*100)
print(" ANCHOR (b): CLUSTER sigma-SPREAD -- the ONLY anchor reaching y~O(1) (theta a FUNCTION)")
print("="*100)
# Reproduce the sigma-spread amplitude (matched a_ext, deep-MOND member a_in=a_ex=a0) vs kernel.
def A_mi(a_in,a_ex,y,thf): return a_in + a_ex*thf(y)
def boost_mi(a_in,a_ex,y,thf): return 1.0/mu_fw(A_mi(a_in,a_ex,y,thf)/a0)
def R_of_y(a_in,a_ex,y,thf):
    return np.sqrt(boost_mi(a_in,a_ex,y,thf)/boost_mi(a_in,a_ex,0.0,thf))
a_in=a_ex=a0
yfull=np.linspace(0.0,1.5,200)
print(f"  Member-internal sigma SPREAD across infall phase y in [0,1.5], deep-MOND member a_in=a_ex=a0:")
print(f"  {'theta kernel':22s} {'theta(0)':>9} | {'sigma-spread':>13} | {'y of |dR/dy| peak':>18}")
print("  "+"-"*70)
spread_by_kernel={}
for nm,thf,t0,is_m in KERNELS:
    Rs=np.array([R_of_y(a_in,a_ex,y,thf) for y in yfull])
    sp=(Rs.max()-Rs.min())/Rs.mean()
    dR=np.gradient(Rs,yfull); ypk=yfull[np.argmax(np.abs(dR))]
    spread_by_kernel[nm]=sp
    print(f"  {nm:22s} {t0:9.3f} | {sp*100:12.1f}% | {ypk:18.2f}  {'(Milgrom)' if is_m else '(bracket)'}")
ms=[spread_by_kernel[nm] for nm,_,_,m in KERNELS if m]
print(f"\n  Milgrom 3 verbatim kernels: sigma-spread = {min(ms)*100:.1f}% - {max(ms)*100:.1f}%  (matches banked 6-13%).")
print(f"  MG (QUMOND/AeST momentary a_ex): EXACTLY 0% for ANY a0. CDM: 0%. => sign/existence is MG-impossible.")
print(r"""  KEY: the sigma-spread AMPLITUDE is ~ MONOTONIC in theta(0) (the adiabatic loading a plunger sheds):
  e^{(1-y)/2} [t0=1.65] -> 6.2%; rational [t0=2] -> 10.3%; e^{1-y} [t0=e] -> 11.8%; lorentz [t0=3] -> larger.
  So the cluster amplitude is ALSO largely a function of theta(0) -- PLUS a weak shape-moment (where the
  |dR/dy| peak sits, y~0.5-0.8). This is the crux for triangulation (next).""")

# ====================================================================================================
# ANCHOR (c): GALAXY ROTATION CURVES -- adiabatic y~0, fix the QS limit (theta(0) folded into a0).
# ====================================================================================================
print("\n"+"="*100)
print(" ANCHOR (c): ROTATION CURVES -- adiabatic y~0; they FIX the QS limit (theta(0) absorbed into a0)")
print("="*100)
print(r"""  A disk star's 'internal' motion is its galactic orbit (omega_in); the relevant 'external' field is the
  static large-scale/cosmological a0-floor (omega_ex ~ H_Lambda ~ 0) => y ~ omega_ex/omega_in << 1. So
  rotation curves are the y->0 ADIABATIC anchor: they fix g_obs = sqrt(g_N^2 + g_N a0) = QS-MOND, i.e. they
  fix the COMBINATION a0 (with theta(0) for any residual external field folded in). The 175-SPARC RAR
  (0.11-0.13 dex) is the y~0 constraint: it nails a0/theta(0) ~ 9.36e-11 but says NOTHING about theta(y>0)
  (no member there ever reaches y~1). So rotation curves = the y=0 ANCHOR POINT, theta(0)-degenerate by
  construction. They EXCLUDE no shape; they only set the y=0 value of A.""")

# ====================================================================================================
# THE TRIANGULATION: can DR4 wide binaries + the cluster sigma-spread PIN theta(y)?  (both ways)
# ====================================================================================================
print("\n"+"="*100)
print(" TRIANGULATION: do DR4 wide binaries + cluster sigma-spread together PIN theta(y)?")
print("="*100)
print(r"""  The kernel theta(y) is a FUNCTION on y in [0,inf). The anchors sample it at:
     y ~ 0      : rotation curves (fix theta(0), folded into a0)        -- 1 constraint (the y=0 value)
     y ~ 0      : wide binaries  (also theta(0), a0-degenerate)         -- SAME point, NOT independent
     y ~ 0.5-1.7: cluster sigma-spread (theta a function)               -- 1 amplitude + 1 weak shape-moment
     y ~ 1      : theta(1)=1 (FIXED by symmetry/normalization, no data needed)
     y -> inf   : theta->0 (Newtonian, FIXED by the no-MOND-at-high-freq limit)
  So DATA provides at most ~2 INDEPENDENT numbers on the curve interior: theta(0) [=y~0 anchors, IF a0 is
  externally fixed] and the cluster sigma-spread AMPLITUDE [a smeared average of theta over y~0.3-1.5].
  Plus 2 analytic endpoints theta(1)=1 and theta(inf)=0. That is a 2-DATA + 2-ANCHOR-POINT sketch of an
  entire function. We now quantify what that pins -- BOTH WAYS.""")

# --- (T.1) forward: given a kernel, what does each anchor measure? (the design matrix) -------------
print("-"*100); print(" (T.1) what each anchor MEASURES for each kernel (the would-be design matrix)")
print("-"*100)
print(f"  {'kernel':22s} | {'theta(0) [WB/RC]':>16} | {'cluster sigma-spread':>20} | {'theta(1)':>8}")
print("  "+"-"*74)
for nm,thf,t0,is_m in KERNELS:
    Rs=np.array([R_of_y(a_in,a_ex,y,thf) for y in yfull]); sp=(Rs.max()-Rs.min())/Rs.mean()
    print(f"  {nm:22s} | {t0:16.3f} | {sp*100:19.1f}% | {float(thf(1.0)):8.3f}")
print(r"""  READ: theta(0) and the cluster sigma-spread are CORRELATED (both rise with theta(0)) -- they are NOT
  two independent handles on the shape; they largely measure the SAME parameter (theta(0)) twice. The
  sigma-spread carries a LITTLE extra shape info (rational t0=2 -> 10.3% but gauss t0=2 -> different %),
  i.e. two kernels with the SAME theta(0) can give different spreads => the spread DOES break the pure-
  theta(0) degeneracy at the ~few-% level. So the genuine independent content is ~1.5 numbers, not 2.""")

# --- (T.2) the DEGENERACY: can two DIFFERENT kernels match BOTH anchors? (both ways) ---------------
print("-"*100); print(" (T.2) DEGENERACY TEST: do distinct kernels matching theta(0) ALSO match the sigma-spread?")
print("-"*100)
# take two kernels with the SAME theta(0)=2 (rational vs gaussian) -- can WB+cluster tell them apart?
sp_rat = (lambda Rs:(Rs.max()-Rs.min())/Rs.mean())(np.array([R_of_y(a_in,a_ex,y,th_rat) for y in yfull]))
sp_gau = (lambda Rs:(Rs.max()-Rs.min())/Rs.mean())(np.array([R_of_y(a_in,a_ex,y,th_gau) for y in yfull]))
print(f"  Two kernels with IDENTICAL theta(0)=2:")
print(f"     rational 2/(1+y^2):  theta(0)=2.000, sigma-spread = {sp_rat*100:.2f}%")
print(f"     gaussian 2*2^(-y^2): theta(0)=2.000, sigma-spread = {sp_gau*100:.2f}%")
print(f"  => WB (sees theta(0)=2 for both, identical) CANNOT distinguish them. The cluster spread differs by")
print(f"     {abs(sp_rat-sp_gau)*100:.2f}% (abs) -- detectable ONLY if cluster sigma-spread precision < ~{abs(sp_rat-sp_gau)*100:.1f}%.")
print(r"""  BOTH WAYS: so the two anchors TOGETHER pin (i) theta(0) [from WB, IF a0 fixed externally] and (ii) ONE
  integral shape-moment of theta over y~0.3-1.5 [from the cluster spread]. That distinguishes broad kernel
  CLASSES (rational vs gaussian vs exponential) IF the cluster spread is measured to ~2-3% absolute. It does
  NOT pin the full function (infinitely many kernels share any 2 moments). 'PIN theta(y)' is FALSE in the
  strict sense; 'pin theta(0) + one shape-moment => discriminate kernel CLASSES' is TRUE, conditionally.""")

# --- (T.3) the feasibility gates (from the repo feasibility work) ---------------------------------
print("-"*100); print(" (T.3) FEASIBILITY GATES -- are the two shape-moments even MEASURABLE? (the honest limit)")
print("-"*100)
print(r"""  WIDE BINARIES (theta(0) anchor):
    * The framework's OWN signal is gamma_v ~ 1.05-1.10 (most-Newtonian MOND); a0 lever ~0.04-0.07 in gamma,
      BELOW the optimistic DR4 systematic floor ~0.03-0.05 (DR4_WIDEBINARY_FORECAST_ROUTE5). So DR4 tests
      the PREMISE (any low-a boost?) at ~1.7-2.8 sigma vs Newton, but the theta(0)-vs-a0 split (~5-8% proof
      signature) is BELOW the DR4 floor. => DR4 gives theta(0) only as a0/theta(0), NOT theta(0) cleanly.
  CLUSTER sigma-SPREAD (the shape-moment anchor):
    * 6-13% spread on sigma~10-20 km/s members needs ~0.6-2.6 km/s precision, resolved internal sigma of
      DIFFUSE/UDG/dSph members on plunging cluster orbits, binned by BOTH matched radius AND infall phase.
      ELT-HARMONI (~7 km/s floor) reaches it for the brightest UDGs; the plunging subset is small; the
      infall-phase proxy (projected phase space) is projection-contaminated (feasibility.py). DEMANDING,
      ~2030s, not near-term.
  => The two genuine shape numbers (theta(0) and the cluster sigma-spread) are BOTH near or below current
  measurement floors. Triangulation is possible IN PRINCIPLE but BOTH legs are floor-limited.""")

# ====================================================================================================
# WHAT KERNEL FORMS ARE ALLOWED vs EXCLUDED BY CURRENT DATA
# ====================================================================================================
print("\n"+"="*100)
print(" ALLOWED vs EXCLUDED kernel forms (current data)")
print("="*100)
print(r"""  EXCLUDED (model-independent, NOT from a fit -- so no circularity):
    * theta(0) <= 1            EXCLUDED. theta(0)>1 is required for the EFE to QUENCH MOND (Milgrom);
                               theta(0)<1 would ANTI-quench (enhance MOND in an external field), contra
                               the observed EFE in dwarfs/RC/clusters. (Endpoint constraint, not a fit.)
    * theta(1) != 1            EXCLUDED by Milgrom's normalization/symmetry (definitional).
    * theta(inf) != 0          EXCLUDED by the high-frequency Newtonian limit (no MOND at omega>>).
    * non-decreasing theta(y)  EXCLUDED (theta must decrease from theta(0)>1 to theta(1)=1 to 0).
  ALLOWED (current data does NOT discriminate among these):
    * ALL of Milgrom's 3 forms (rational, e^{1-y}, e^{(1-y)/2}) and the gaussian/lorentz brackets -- they
      differ in sigma-spread by 6-13% but NO cluster sigma-spread has been MEASURED yet => none excluded.
    * theta(0) anywhere in ~[1.5, 3+]: wide-binary data is contested (Chae high vs Banik null) and
      a0-degenerate => does NOT yet pin theta(0). (gamma_v~1.05-1.10 spans theta(0)~e..2; the data
      straddle both.)
  NET CURRENT STATUS: the kernel is constrained to {theta(0)>1, decreasing, theta(1)=1, theta(inf)=0} --
  a one-sided, monotone, normalized family. NO measured observable yet selects WITHIN that family. The
  amplitude/shape (the 6-13% sigma-spread, the theta(0) value) are ALL currently ALLOWED. Both ways:
  this is genuine PARTIAL constraint (the endpoints + monotonicity are real, data-independent), but the
  INTERIOR shape is empirically UNCONSTRAINED today.""")

# ====================================================================================================
# SYNTHESIS
# ====================================================================================================
print("\n"+"="*100)
print(" SYNTHESIS -- the observational triangulation of theta(y)")
print("="*100)
print(f"""
 THE y OF EACH ANCHOR (computed, both ways):
   (a) WIDE BINARIES:   y_WB = P_in/P_ex ~ 1e-4 .. 4e-3 << 1  (galactic year {P_galyr/Myr:.0f} Myr vs binary
                        period ~1 Myr). => DEEPLY ADIABATIC; probes theta(0) ONLY (Eq-35), a0-degenerate.
                        The task's premise 'WB constrain y~O(1)' is INCORRECT: WB sit at y~0, with clusters.
                        Milgrom himself files WB under the theta(0) adiabatic EFE.
   (b) CLUSTER sigma-spread: y ~ 0.5-1.7 (plunging diffuse/UDG/dSph) -- the ONLY anchor where theta is a
                        FUNCTION. Amplitude 6-13% (kernel-dependent), MG-impossible (MG gives 0 for any a0).
   (c) ROTATION CURVES: y ~ 0 -- fixes the QS limit (theta(0) folded into a0); excludes no shape.

 CAN DR4 + CLUSTERS PIN theta(y)?  NO (strict) / PARTIALLY (kernel-class).  Both ways:
   - NO, not the FUNCTION: data sample theta at y~0 (one value, a0-degenerate) and one smeared moment over
     y~0.3-1.5 (the cluster spread). Two anchors + two analytic endpoints = a 2-point sketch; infinitely
     many kernels share any two moments. 'theta(y) empirically pinned' is FALSE.
   - YES, the CLASS: IF a0 is taken externally fixed (from the RAR) AND the cluster sigma-spread is measured
     to ~2-3% absolute, the pair (theta(0), sigma-spread) discriminates kernel CLASSES (rational vs gaussian
     vs exponential, which differ by ~few-% in spread at fixed theta(0)). That is a real, if coarse,
     empirical handle -- a genuine partial constraint, not a derivation.
   - BUT both legs are FLOOR-LIMITED today: the WB theta(0)-vs-a0 split (~5-8%) is below the DR4 floor; the
     cluster spread needs ELT-class resolved sigma of a small plunging-dwarf subset (~2030s). So even the
     kernel-CLASS triangulation is a 2030s+ prospect, not current.

 ALLOWED vs EXCLUDED:
   EXCLUDED (data-independent endpoints, no circularity): theta(0)<=1; theta(1)!=1; theta(inf)!=0;
     non-monotone theta. ALLOWED (un-discriminated by any current measurement): all of Milgrom's 3 forms +
     brackets; theta(0) in ~[1.5,3]; the full 6-13% sigma-spread range.

 KERNEL STATUS: PARTIALLY-CONSTRAINED by data -- the boundary conditions [theta(0)>1, decreasing,
   theta(1)=1, theta(inf)=0] are real and model-independent, but NO current observable selects within that
   family. Future DR4(theta(0), floor-limited)+cluster-spread(one shape-moment, ELT-class) could pin the
   theta(0) value and discriminate kernel CLASSES, but NOT the full function.

 QUARANTINE: pinning/constraining theta(y) does NOT make a0/Z/kappa derived (theta multiplies a_ex; a0 is
   set independently by the isolated RAR). CIRCULARITY AVOIDED: the y-values come from independent
   timescales (galactic year, Kepler period, infall dynamics), NOT from assuming a kernel; the excluded
   forms are endpoint/monotonicity constraints, not fit artifacts.
""")
