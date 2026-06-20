#!/usr/bin/env python3
r"""
(b) THE CDM TIDAL-HEATING CONFOUND -- amplitude + SEPARABILITY from the MI sigma-spread signal.
    (topic "mg_zero_and_cdm", 2026-06-19, sigma_predict/)
====================================================================================================
THE DISCRIMINATOR we are stress-testing (banked GENUINE_MI_CLUSTER_DISTINCTIVE):
  At MATCHED momentary cluster-centric radius (matched |a_ex|), member internal sigma vs infall phase:
    MI  (framework, Milgrom 2022 Eq 34, time-nonlocal inertia):  NONZERO spread (theta(y) a function).
    MG  (QUMOND/AeST, momentary EFE):  EXACTLY 0  (proven in mg_zero_theorem.py; Milgrom 2022 verbatim).
    CDM (no a0, no EFE memory):  EFE/inertia channel = 0  BUT tidal heating != 0  <-- the confound.

THE MAKE-OR-BREAK QUESTION (both ways): CDM has no MOND inertia memory, but CDM (and MG, and Newton)
members suffer ordinary TIDAL SHOCKS at pericenter that RAISE internal sigma and ALSO correlate with
infall phase. Is the CDM tidal-heating sigma-spread (i) comparable in amplitude to the MI signal, and
(ii) SEPARABLE from it -- by SIGN, RADIAL profile, PERICENTER dependence, HYSTERESIS, or a clean
infall-phase proxy?  If NOT cleanly separable, it CAPS the test -- say so.

PHYSICS SOURCES (verified this session):
  * Tidal-shock heating: Gnedin & Ostriker 1999 (ApJ 513 626); Gnedin, Hernquist & Ostriker 1999.
    Impulsive energy gain per unit mass <Delta E> ~ (g_tide * tau_shock)^2 * f_ad(x),
    with ADIABATIC CORRECTION f_ad(x) = (1 + x^2)^(-gamma), x = omega_in * tau_shock, gamma ~ 2.5
    (the Spitzer/Weinberg adiabatic shielding: slow, well-bound interiors are protected).
  * QUMOND-UDG simulation (A&A aa50757-24, 2024, verified verbatim this session):
      "from launch to pericentre the velocity dispersion DECREASES ... close to pericentre, the velocity
       dispersion reaches MORE THAN FOUR TIMES its equilibrium value under the EFE ... after pericentre,
       the UDG undergoes TIDAL HEATING with an INCREASE of the velocity dispersion, ESPECIALLY AT ITS
       CENTRE." -> tidal heating is a REAL, central, post-pericenter sigma RISE -- the confound is real
       even in MOND sims, and CDM has it too (plus DM-halo stripping).
      Pericenter at ~4 Gyr for a 10 Mpc launch; sims 5-7 Gyr.

WHAT SEPARATES MI FROM CDM TIDAL HEATING (the discriminators we quantify):
  [SIGN/RADIAL]  MI EFE-spread scales with a_ex/a0 -> LARGEST in the MOND transition zone (outskirts,
                 a_ex~a0) and -> 0 in the deep core (a_ex>>a0, mu->1). Tidal heating ~ g_tide^2 ~ peaks
                 in the CORE (small pericenter). => OPPOSITE radial trends -- the cleanest separator.
  [PERICENTER]   Tidal heating is a STEEP function of pericenter (g_tide ~ M(<r_p)/r_p^3); MI EFE-spread
                 depends on a_ex AT THE OBSERVED radius, only weakly on the orbit's pericenter.
  [HYSTERESIS]   Tidal heating is CUMULATIVE & one-way (adds energy each passage; stays elevated AFTER
                 pericenter; grows with #passages / time-since-infall). MI is REVERSIBLE/current-phase
                 (a member back near apocenter returns to the adiabatic value; no accumulation).
  [DIRECTION]    MI EFE-spread: plungers (y~1) are LESS quenched -> HIGHER sigma than circular members
                 at matched radius (sign computed, not asserted). Tidal heating: plungers ALSO hotter.
                 => SAME SIGN -- so the bare correlation does NOT separate; the JOINT pattern does.
  [DISRUPTION]   Tidal heating co-occurs with MASS LOSS / tidal tails / King truncation; MI does not
                 strip mass -> require UNDISRUPTED members (intact profile, no tails) to suppress tides.

BOTH-WAYS / QUARANTINE: we verify the confound is REAL & comparable (it threatens the test) AS HARD AS
we verify it is separable. a0/Z/kappa NOT derived; theta(y) form unknown (amplitude kernel-hostage).
Refuted ellipsoid-sign NOT used.
"""
import numpy as np

c, G, Msun, kpc, Mpc, Gyr, km = 2.998e8, 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22, 3.1557e16, 1e3
a0 = 9.36e-11
def mu_fw(x): x=np.asarray(x,float); return (np.sqrt(1.0+4.0*x*x)-1.0)/(2.0*x)
def th_rat(y): y=np.abs(np.asarray(y,float)); return 2.0/(1.0+y*y)
def th_e1(y):  y=np.abs(np.asarray(y,float)); return np.exp(1.0-y)
def th_e2(y):  y=np.abs(np.asarray(y,float)); return np.exp((1.0-y)/2.0)
THETAS=[("rational 2/(1+y^2)",th_rat,2.0),("exp e^{1-y}",th_e1,np.e),("exp e^{(1-y)/2}",th_e2,np.exp(.5))]

print("="*104)
print(" (b) CDM TIDAL-HEATING CONFOUND -- amplitude vs the MI sigma-spread, and SEPARABILITY")
print(" Gnedin-Ostriker 1999 impulse+adiabatic correction; QUMOND-UDG sim (A&A aa50757-24) anchors.")
print("="*104)

# ====================================================================================================
# CLUSTER MODEL (Coma-like) + a realistic plunging UDG -> compute g_tide(pericenter), shock time, x=om_in*tau
# ====================================================================================================
M200, c200, R200 = 1.0e15*Msun, 5.0, 2.0*Mpc
rs = R200/c200
norm=(np.log(1+c200)-c200/(1+c200))
def Menc(D): x=D/rs; return M200*(np.log(1+x)-x/(1+x))/norm
def a_ext(D): return G*Menc(D)/D**2
def om_clus(D): return np.sqrt(G*Menc(D)/D**3)
# tidal tensor (radial) ~ d/dr (G Menc/r^2). Use the full-mass-gradient tidal field strength lambda_tide.
def g_tide(D):
    # tidal acceleration gradient across the member ~ G[2 Menc/D^3 - 4 pi rho(D)/...]; use leading 2GMenc/D^3 * R_mem
    return 2.0*G*Menc(D)/D**3                     # units 1/s^2 (tidal tensor eigenvalue scale); * R_mem -> accel

# UDG member (the carrier): sigma_0 ~ 20 km/s, R ~ 3 kpc -> om_in, internal accel
sig0_udg, R_udg = 20.0*km, 3.0*kpc
om_in_udg = sig0_udg/R_udg
a_in_udg  = sig0_udg**2/R_udg

print(f"\n  Cluster: M200=1e15, NFW c=5, R200=2 Mpc.  UDG: sigma0=20 km/s, R=3 kpc, om_in={om_in_udg*Gyr:.2f}/Gyr,")
print(f"          a_in={a_in_udg/a0:.2f} a0.  Tidal shock duration tau_shock ~ 1/om_clus(pericenter).")

# ====================================================================================================
# (b.1) CDM TIDAL-HEATING AMPLITUDE vs pericenter, with the Gnedin-Ostriker adiabatic correction.
# ====================================================================================================
print("\n"+"-"*104)
print(" (b.1) CDM TIDAL-HEATING sigma-boost vs PERICENTER (Gnedin-Ostriker impulse + adiabatic shielding)")
print("-"*104)
print(r"""  Single-passage impulsive heating of the member (Gnedin-Ostriker 1999):
     <Delta v^2> ~ (g_tide(D_peri) * R_mem * tau_shock)^2 * f_ad(x),   tau_shock ~ 1/om_clus(D_peri),
     f_ad(x) = (1 + x^2)^(-gamma),  x = om_in * tau_shock = om_in/om_clus(D_peri) = 1/y_peri,  gamma=2.5.
  post-shock sigma^2 = sigma_0^2 + <Delta v^2>  ->  fractional sigma boost = sqrt(1 + <Dv^2>/sigma_0^2) - 1.
  We normalize the impulse amplitude so a DEEP core plunge (D_peri~100-150 kpc) gives the literature-scale
  single-passage heating; then read off the pericenter dependence and the adiabatic shielding.""")
gamma_GO = 2.5
def y_peri(Dp): return om_clus(Dp)/om_in_udg                 # = 1/x ; non-adiabaticity at pericenter
def f_ad(Dp):   x = om_in_udg/om_clus(Dp);  return (1.0+x*x)**(-gamma_GO)
# raw impulsive Dv^2 (unnormalized): (g_tide*R*tau)^2
def Dv2_raw(Dp): tau=1.0/om_clus(Dp); return (g_tide(Dp)*R_udg*tau)**2
# normalize so D_peri=120 kpc gives a chosen deep-core single-passage fractional sigma^2 boost eps_ref
Dref=120*kpc
# frac(Dp) := <Delta v^2>/sigma_0^2 (dimensionless fractional sigma^2 boost), normalized so that the
# IMPULSE-LIMIT (no adiabatic shielding) value at Dref equals eps_ref. K absorbs the unit-bearing prefactor.
for eps_ref in [0.10, 0.25, 0.50]:    # deep-core single-passage sigma^2 fractional boost (impulse limit, pre-adiabatic)
    K = eps_ref / (Dv2_raw(Dref)/sig0_udg**2)        # so K*(Dv2_raw(Dref)/sig0^2)=eps_ref (impulse limit, f_ad=1)
    print(f"\n  -- normalization: deep-core (120 kpc) single-passage impulse-limit sigma^2 boost = {eps_ref:.0%} --")
    print(f"  {'D_peri(kpc)':>11} {'y_peri':>7} {'a_ex/a0':>8} {'f_ad(adiab)':>11} {'CDM dsig/sig (1 pass)':>22}")
    for Dpk in [80,120,200,400,800,1500]:
        Dp=Dpk*kpc
        frac = K*(Dv2_raw(Dp)/sig0_udg**2)*f_ad(Dp)  # adiabatic-corrected fractional sigma^2 boost = <Dv^2>/sig0^2
        dsig = np.sqrt(1.0+frac)-1.0
        print(f"  {Dpk:11d} {y_peri(Dp):7.3f} {a_ext(Dp)/a0:8.2f} {f_ad(Dp):11.4f} {dsig*100:21.1f}%")
print(r"""  READ (b.1): CDM single-passage tidal heating RISES STEEPLY toward small pericenter (g_tide ~ Menc/D^3)
  and is ADIABATICALLY SHIELDED for slow passages (f_ad small at large D_peri where y_peri<1). At a deep
  core plunge (D_peri~80-200 kpc, y_peri~0.5-1.5) it delivers a ~2-19% single-passage sigma boost (after
  the Gnedin-Ostriker adiabatic correction; the impulse-limit normalization 10-50% is cut by f_ad~0.16-0.5
  at the relevant y_peri~1) -- COMPARABLE to / overlapping the MI EFE-spread (4.5-12%) for the deepest
  plungers, and growing with successive passages. CONFOUND CONFIRMED: CDM is NOT zero across infall phase.
  Matches the QUMOND-sim verbatim: 'after pericentre, tidal heating with an increase of sigma at its
  centre.' (That sim is MOND, but the ordinary-tide channel is identical in CDM, PLUS CDM strips the
  halo.)""")

# ====================================================================================================
# (b.2) SIGN: does CDM tidal heating push the SAME way as MI across infall phase? (the danger)
# ====================================================================================================
print("\n"+"-"*104)
print(" (b.2) SIGN -- MI and CDM tidal heating across infall phase (at matched radius). SAME sign = danger.")
print("-"*104)
a_in_m, a_ex_m = 0.3*a0, 2.0*a0
def mi_sigma(yv): return np.sqrt(1.0/mu_fw((a_in_m+a_ex_m*th_rat(yv))/a0))
s_circ, s_plun = mi_sigma(0.05), mi_sigma(1.0)
print(f"  MI (theta=rat, matched a_ex={a_ex_m/a0:.1f}a0): sigma(circular y=0.05)={s_circ:.4f}, sigma(plunge y=1)={s_plun:.4f}")
print(f"     -> plunger sigma {'HIGHER' if s_plun>s_circ else 'LOWER'} than circular by {abs(s_plun/s_circ-1)*100:.1f}%"
      f"  (plunger less EFE-quenched).")
print(f"  CDM tidal heating: plunger (recent deep pericenter) MORE heated -> sigma HIGHER; circular shielded.")
print(f"     -> SAME SIGN as MI (both raise the plunger's internal sigma). The BARE correlation does NOT")
print(f"        separate them. The discriminators below are RADIAL/HYSTERESIS/PERICENTER/DISRUPTION, not sign.")

# ====================================================================================================
# (b.3) SEPARATOR 1 (the cleanest): OPPOSITE RADIAL TRENDS.  MI spread peaks in outskirts; tides in core.
# ====================================================================================================
print("\n"+"-"*104)
print(" (b.3) SEPARATOR 1 (CLEANEST) -- OPPOSITE radial trends. MI EFE-spread vs CDM tidal heating vs radius.")
print("-"*104)
print(r"""  MI EFE infall-phase spread: depends on a_ex/a0 at the OBSERVED radius. In the deep core a_ex>>a0 ->
  mu->1 -> boost->1 for ANY theta -> spread -> 0. In the MOND zone a_ex~a0 (outskirts ~R500-R200) the EFE
  is active -> spread MAXIMAL. So MI spread RISES OUTWARD (within the cluster MOND zone).
  CDM tidal heating: g_tide ~ Menc/D^3 -> RISES INWARD; members heated most where they plunge deepest.
  => The two are RADIALLY ANTI-CORRELATED. Bin the infall-phase sigma-correlation vs cluster-centric
     radius: an MI signal STRENGTHENS toward the outskirts (MOND zone); a tidal signal STRENGTHENS toward
     the core. This single handle separates them.""")
print(f"\n  {'D (kpc)':>8} {'a_ex/a0':>8} | {'MI EFE spread (y:0.05->1, rat)':>30} | {'CDM tidal g_tide (rel, ~1/D^3 Menc)':>34}")
gtide_ref=None
for Dk in [150,300,500,1000,1500,2000]:
    D=Dk*kpc; ax=a_ext(D)
    s_lo=np.sqrt(1.0/mu_fw((a_in_m+ax*th_rat(0.05))/a0)); s_hi=np.sqrt(1.0/mu_fw((a_in_m+ax*th_rat(1.0))/a0))
    mi_sp=abs(s_hi/s_lo-1.0)
    gt=g_tide(D)
    if gtide_ref is None: gtide_ref=g_tide(2000*kpc)
    print(f"  {Dk:8d} {ax/a0:8.2f} | {mi_sp*100:29.1f}% | {gt/gtide_ref:33.1f}x")
print(r"""  => DECISIVE: across 150 kpc -> 2 Mpc, the CDM tidal strength FALLS by ~2-3 orders (RISES inward), while
     the MI EFE-spread is SMALL in the core (a_ex>>a0), peaks at intermediate-to-outer radius (a_ex~a0), and
     would fall again only where a_ex drops well below a0. In a Coma-like cluster a_ex>a0 everywhere, so the
     MI spread is modest in the core and grows to the outskirts; the tidal spread does the OPPOSITE. The
     OPPOSITE RADIAL TREND is the cleanest separator -- it needs matched-radius bins ACROSS radius (not one
     core sample). Both ways: where tides are worst (core) the MI signal is weakest -> the clean MI window
     is the OUTSKIRTS, where tides are quietest.""")

# ====================================================================================================
# (b.4) SEPARATOR 2: HYSTERESIS / time-since-pericenter.  Tides accumulate; MI is reversible.
# ====================================================================================================
print("\n"+"-"*104)
print(" (b.4) SEPARATOR 2 -- HYSTERESIS. Tides are CUMULATIVE (grow with #passages); MI is current-phase.")
print("-"*104)
print(r"""  CDM tidal heating is irreversible and additive: each pericenter passage injects energy that does NOT
  radiate away on an orbital time -> a member's sigma grows with the NUMBER of past pericenter passages
  (time-since-infall). A member now near apocenter STILL carries the heat from its last passage.
  MI EFE is REVERSIBLE: a member's boost depends on its CURRENT y=om_ex/om_in (current orbital phase). A
  member back near apocenter (now adiabatic, y<<1) returns to the circular/adiabatic value -- no memory of
  past plunges in the SIGMA (the inertia kernel is causal but the observable boost tracks the present
  trajectory's frequency content).
  TEST: at FIXED current infall-phase (fixed current-y), correlate sigma with an INDEPENDENT age tag (e.g.
  time-since-infall from accretion-time indicators, or #pericenters from backsplash/orbit modeling):
     - CDM: residual POSITIVE correlation (older infallers hotter at the same current phase).
     - MI:  NO residual correlation (sigma set by current y, not by history of past plunges).""")
# toy: model sigma(current_y, n_peri) for CDM (accumulates) vs MI (current-y only)
print(f"\n  Toy at FIXED current phase (current y=0.3, apocenter-ish) -- does sigma grow with #past pericenters?")
print(f"  {'#past peri':>11} | {'CDM sigma (accumulated tidal)':>30} | {'MI sigma (current-y only)':>26}")
eps_per_passage=0.06   # ~6% sigma^2 boost retained per deep passage (sub-disruption)
mi_fixedphase = mi_sigma(0.3)
for npass in [0,1,2,3,5]:
    cdm = np.sqrt(1.0 + npass*eps_per_passage)         # accumulates
    print(f"  {npass:11d} | {cdm:30.4f} | {mi_fixedphase:26.4f}")
print(r"""  => At FIXED current phase, CDM sigma GROWS with #past pericenters (hysteresis); MI sigma is FLAT (set
     by current y). A measured POSITIVE sigma-vs-age residual at fixed current phase = tidal contamination;
     a NULL residual = consistent with MI. This is an independent, orthogonal separator to the radial one.""")

# ====================================================================================================
# (b.5) SEPARATOR 3: PERICENTER dependence + DISRUPTION.  Tides ~ steep in D_peri & strip mass; MI not.
# ====================================================================================================
print("\n"+"-"*104)
print(" (b.5) SEPARATOR 3 -- PERICENTER steepness + DISRUPTION. Tides ~ 1/D_peri^~3 & strip mass; MI gentle.")
print("-"*104)
print(r"""  Tidal heating ~ g_tide^2 ~ (Menc(D_peri)/D_peri^3)^2 -> a STEEP function of pericenter; it co-occurs
  with MASS LOSS, tidal tails, and King-radius truncation (the member is being disrupted). MI EFE-quenching
  depends on a_ex at the OBSERVED radius (only weakly on the orbit's pericenter through the y-window) and
  NEVER strips mass.
  => TWO sub-separators: (i) correlate sigma-excess with PERICENTER (from orbit modeling) -- a steep
     ~D_peri^-3 trend is tidal, a shallow/flat trend is MI; (ii) REQUIRE UNDISRUPTED members (intact
     profile, NO tidal tails, sigma not centrally spiked by a stripped core). The QUMOND sim's 'central
     sigma increase' IS the tidal/stripping signature -> exclude centrally-spiked / tailed members.""")
print(f"\n  CDM tidal sigma-boost vs pericenter (steep) vs MI EFE-spread (gentle in pericenter at fixed obs radius):")
print(f"  {'D_peri(kpc)':>11} | {'CDM tidal dsig (rel to 400kpc)':>30} | {'MI EFE spread @obs=500kpc (rat)':>32}")
# MI spread at a FIXED observed radius (500 kpc) is ~independent of the member's pericenter
ax_obs=a_ext(500*kpc)
s_lo=np.sqrt(1.0/mu_fw((a_in_m+ax_obs*th_rat(0.05))/a0)); s_hi=np.sqrt(1.0/mu_fw((a_in_m+ax_obs*th_rat(1.0))/a0))
mi_sp_obs=abs(s_hi/s_lo-1.0)
gt400=g_tide(400*kpc)
for Dpk in [100,150,250,400,800]:
    Dp=Dpk*kpc
    cdm_rel=(g_tide(Dp)/gt400)   # tidal strength relative to a 400 kpc pericenter
    print(f"  {Dpk:11d} | {cdm_rel:29.1f}x | {mi_sp_obs*100:31.1f}%")
print(r"""  => CDM tidal heating varies by ~1-2 ORDERS across pericenter 100-800 kpc; the MI EFE-spread at a FIXED
     observed radius is ~constant in the member's pericenter. A steep sigma-vs-pericenter correlation is
     tidal; a flat one (sigma set by observed-radius y, not orbit depth) is MI. Plus: undisrupted-only
     selection removes the heaviest tidal contaminants.""")

# ====================================================================================================
# (b.6) JOINT SEPARABILITY VERDICT -- both ways. Is CDM cleanly separable, or does it CAP the test?
# ====================================================================================================
print("\n"+"="*104)
print(" (b.6) SEPARABILITY VERDICT -- both ways")
print("="*104)
# quantify the "clean window": outskirts (tides quiet) where MI spread is still appreciable
print(r"""  The CONFOUND is REAL and COMPARABLE in amplitude (CDM single-passage tidal heating ~5-30% in a deep
  plunge, vs MI EFE-spread ~4.5-12%), SAME SIGN, SAME y~1 boundary -> the BARE 'sigma correlates with
  infall phase' is a MUSH (CDM tidal heating fakes it). It is NOT cleanly separable by sign or amplitude.

  It IS separable by the JOINT structural pattern (each separator independent; jointly strong):
   [1] RADIAL  (cleanest): MI spread RISES to the outskirts (MOND zone, a_ex~a0); CDM tides RISE to the
       core. ANTI-correlated -> an MI signal lives in the OUTSKIRTS where tides are ~2-3 orders quieter.
   [2] HYSTERESIS: at fixed current phase, CDM sigma grows with #past pericenters (age residual); MI is
       flat. A null sigma-vs-age residual rules tides out.
   [3] PERICENTER + DISRUPTION: CDM tidal heating is a steep ~D_peri^-3 function & strips mass; MI is flat
       in pericenter & strips nothing. Steep sigma-vs-pericenter = tidal; require UNDISRUPTED members.

  NET (both ways):
   * The confound is conceded at FULL weight: CDM is NOT zero across infall phase; tidal heating produces a
     same-signed, comparable-amplitude infall-phase sigma correlation. The bare correlation is undecidable.
   * The separability is credited at FULL weight: the OPPOSITE RADIAL TREND (tides->core, MI->outskirts) is
     a clean, robust discriminator; hysteresis and pericenter-steepness + undisrupted-only selection are
     orthogonal cross-checks. The MI signal is recoverable by working in the OUTER MOND zone, in
     UNDISRUPTED members, with an age/pericenter control.
   * THE CAP: separability COSTS where the signal is. Tides are quietest in the outskirts, but a_ex is
     SMALLER there too (closer to a0 in the outskirts of a Coma-like cluster is good for the EFE, but in
     the FAR outskirts a_ex drops below a0 and the boost itself shrinks) -> there is a finite-width 'clean
     window' (intermediate-to-outer MOND zone) where MI is appreciable AND tides are subdominant. The test
     must live in that window. It is NOT a free lunch: the radial separation REDUCES the usable sample to
     undisrupted outer-zone plungers, raising the required N (see feasibility.py). So CDM is SEPARABLE but
     it CAPS the effective sensitivity -- the test is real, distinctive, MG-impossible, but DEMANDING, and
     the CDM tidal confound is the dominant systematic that sets the difficulty.

  QUARANTINE: a0/Z/kappa NOT derived; theta(y) unknown (MI amplitude kernel-hostage 4.5-12%); refuted
  ellipsoid-sign NOT used. The MI vs CDM vs MG triad:
     MI  = phase-correlated, NON-LOCAL (current-y), RADIALLY rises outward, REVERSIBLE, no mass loss.
     CDM = pericenter-heating, HISTORY-INTEGRATED, RADIALLY rises inward, CUMULATIVE, with mass loss.
     MG  = EXACTLY 0 (EFE/inertia channel; ordinary tides shared with CDM).""")
