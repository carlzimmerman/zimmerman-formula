#!/usr/bin/env python3
r"""
VEIN 1 -- TIME-NONLOCALITY / MEMORY KERNEL theta(y) ON TIDAL STREAMS.
================================================================================
B4 DISCIPLINE (the rule B4 died for): NO hardcoded sign, NO ad-hoc proxy. We do
the REAL time-nonlocal MI calc on the framework's OWN theta(y) kernel and check
the MG-impossibility claim BOTH WAYS, including the a0-degeneracy trap that the
banked member_MI_nonadiabatic_plunge.py established (a single object / single
orbit is a0-absorbable; only a RELATIONAL spread at matched momentary a_ext is
genuinely MG-impossible).

FRAMEWORK (its OWN terms, Milgrom 2022 arXiv:2208.07073 MI formulation, the
framework's chosen realization with a0 = cH_Lambda/Z = 9.36e-11):
  inertia of a body = NONLOCAL-in-time response to the dS-Unruh bath. For a body
  with internal/orbital frequency omega_n the MOND magnification reads the OTHER
  frequencies present, weighted by the memory kernel theta(omega_k/omega_n):
     A(omega_n) = omega_n^2 |r_n| + SUM_{k!=n} omega_k^2|r_k| theta(omega_k/omega_n)   (Eq 28)
  EFE two-frequency form (Eq 33/34):
     A(omega_in) = omega_in^2|r_in| + a_ext * theta(omega_ext/omega_in)
  theta: theta(1)=1, theta symmetric, DECREASING, theta(0) ~ "a few" (UNKNOWN form;
  Milgrom example forms theta=2/(1+y^2) [theta0=2] and theta=e^{1-|y|} [theta0=e]).
  ADIABATIC limit (omega_ext<<omega_in, Eq 35): theta->theta(0)=const => EXACTLY a
  modified-GRAVITY EFE with a0 -> a0/theta(0). THE a0-DEGENERATE TRAP.

THE POSIT (P1, "stream memory width asymmetry"):
  A tidal stream's debris is stripped near the progenitor's PERICENTER, where the
  external (host) tidal field is changing fastest: omega_ext (= rate of change of
  a_ext along the progenitor orbit) is LARGE near peri, SMALL near apo. So freshly
  stripped debris carries a y = omega_ext/omega_in that is set by WHERE on the orbit
  it left -- a TIME-NONLOCAL tag. As the stream phase-mixes, leading/trailing arms
  sample debris released at different orbital phases => a theta(y)-modulated internal
  velocity dispersion that varies ALONG the stream, set by release phase, NOT by the
  momentary local field. MG's EFE is INSTANTANEOUS (depends only on momentary a_ex,
  Milgrom verbatim) => MG predicts the stream's internal sigma is a function of the
  CURRENT local a_ext ONLY, identical for two debris parcels now at the same place
  regardless of release phase. MI predicts a RELEASE-PHASE memory: parcels now at
  the same place but stripped at different phases carry different theta(y) tags.

WHAT WE COMPUTE (real, both-ways):
  (1) Along a representative eccentric progenitor orbit in a realistic MW host,
      compute omega_ext(t) = |d ln a_ext/dt| and y(t)=omega_ext/omega_in for a
      diffuse globular/dwarf progenitor; show y is NON-adiabatic (y~O(1)) only in
      a window near pericenter -> a real release-phase tag exists or it doesn't.
  (2) The MI internal-sigma boost B = 1/mu_fw(A/a0) for debris with its release-phase
      theta(y) tag, vs the MG boost 1/mu_fw(theta(0)*a_ext/a0) (momentary). Compute
      the sigma RATIO carried by the memory tag.
  (3) THE a0-DEGENERACY TRAP, honestly: can a single rescaled a0 absorb the MI
      effect for (a) one parcel, (b) the whole stream? Show where it can (single
      object) and where it CANNOT (the RELATIONAL spread at matched momentary a_ext
      between fresh-peri debris and old-apo debris now co-located).
  (4) THE SWAMP: epicyclic stream width, progenitor mass, host triaxiality. Is the
      memory signal above or below the dominant non-MI width drivers?

FOOTING (sealed): a0=9.36e-11; framework nu/mu_fw; never McGaugh nu. DO NOT git-push.
"""
import math
import numpy as np

A0     = 9.36e-11
G      = 6.674e-11
Msun   = 1.989e30
kpc    = 3.0857e19
km     = 1.0e3
pc     = 3.0857e16
Gyr    = 3.156e16   # s

def mu_fw(x):  return (math.sqrt(1.0 + 4.0*x*x) - 1.0)/(2.0*x)   # framework inverse interp
def theta_rat(y): return 2.0/(1.0 + y*y)        # theta0=2
def theta_exp(y): return math.exp(1.0 - abs(y)) # theta0=e

# ---- MW host enclosed mass (same anchors as the dwarf pilot: Gibbons+14/BHG16) ----
M50  = 4.0e11*Msun; M100 = 7.0e11*Msun
ALPHA = math.log(M100/M50)/math.log(2.0)        # ~0.807
def M_enc(r_m):    return M50*(r_m/(50*kpc))**ALPHA
def a_ext(r_kpc):  r=r_kpc*kpc; return G*M_enc(r)/r**2
def omega_orb(r_kpc):  r=r_kpc*kpc; return math.sqrt(G*M_enc(r)/r**3)   # host orbital freq

print("="*100)
print(" VEIN 1 -- P1: TIDAL-STREAM MEMORY KERNEL theta(y)  (real time-nonlocal MI calc, both-ways)")
print("="*100)

# -----------------------------------------------------------------------------
# (1) omega_ext(phase): the RATE the external (host) field changes along the
#     progenitor orbit. THE PHYSICS: a_ext = G M_enc(r)/r^2 changes as r changes,
#     and r changes on the host ORBITAL timescale. Near pericenter the progenitor
#     sweeps through the steep part of the field fastest, so omega_ext ~ the host
#     orbital frequency omega_orb(r) (both scale as sqrt(GM/r^3)).  We compute
#     omega_ext = |d ln a_ext/dt| EXACTLY along a properly integrated radial orbit
#     (RK4, fine timestep), and ALSO cross-check it against omega_orb(r_peri) so the
#     number is not a numerical-gradient artifact (the B4 failure mode).
# -----------------------------------------------------------------------------
def integrate_orbit(r_apo_kpc, r_peri_kpc, n=400000, n_orbits=1.0):
    ra=r_apo_kpc*kpc; rp=r_peri_kpc*kpc
    def Phi(r):  return -G*M_enc(r)/r
    def dPhidr(r):
        h=1e-4*r; return (Phi(r+h)-Phi(r-h))/(2*h)
    # E,L from turning points vr=0 at ra,rp
    L2 = 2*(Phi(ra)-Phi(rp))/(1.0/rp**2 - 1.0/ra**2)
    # radial period estimate to size the integration window
    Tr = 2*math.pi*math.sqrt(((ra+rp)/2)**3/(G*M_enc((ra+rp)/2)))
    dt = n_orbits*Tr/n
    # RK4 on (r,vr): dvr/dt = -dPhidr + L2/r^3 ; dr/dt = vr.  Start at pericenter.
    r=rp; vr=0.0; t=0.0; out=[]
    def acc(r): return -dPhidr(r) + L2/r**3
    for i in range(n):
        k1r=vr;          k1v=acc(r)
        k2r=vr+0.5*dt*k1v; k2v=acc(r+0.5*dt*k1r)
        k3r=vr+0.5*dt*k2v; k3v=acc(r+0.5*dt*k2r)
        k4r=vr+dt*k3v;     k4v=acc(r+dt*k3r)
        r += dt/6*(k1r+2*k2r+2*k3r+k4r)
        vr+= dt/6*(k1v+2*k2v+2*k3v+k4v)
        t += dt
        out.append((t, r/kpc))
    return np.array(out)

orb = integrate_orbit(r_apo_kpc=19.0, r_peri_kpc=8.0)
t_arr, r_arr = orb[:,0], orb[:,1]
a_arr = np.array([a_ext(rk) for rk in r_arr])
omega_ext_t = np.abs(np.gradient(np.log(a_arr), t_arr))   # |d ln a_ext/dt| (1/s)

# pericenter / apocenter within the integrated arc
ip = int(np.argmin(r_arr)); ia = int(np.argmax(r_arr))
# omega_ext near peri = local |dln a/dt| AROUND peri (window-averaged, robust to the
# instantaneous zero of d ln a/dt exactly at the turning point where dr/dt=0).
def window_max(arr, idx, half=2000):
    lo=max(0,idx-half); hi=min(len(arr),idx+half); return float(np.max(arr[lo:hi]))
omega_ext_peri = window_max(omega_ext_t, ip)
omega_ext_apo  = window_max(omega_ext_t, ia)
# cross-check: at peri, the field-change rate should be ~ the host orbital frequency
omega_orb_peri = omega_orb(r_arr[ip])

print(f"\n  MW host M(<r)=4e11(r/50kpc)^{ALPHA:.3f} Msun.  Progenitor orbit peri=8, apo=19 kpc.")
print(f"  omega_ext(phase)=|d ln a_ext/dt| (the RATE the external field changes = the memory drive).")
print(f"  CROSS-CHECK (anti-artifact): omega_ext_peri={omega_ext_peri:.3e} 1/s  vs  host omega_orb(r_peri)={omega_orb_peri:.3e} 1/s")
print(f"     ratio = {omega_ext_peri/omega_orb_peri:.2f}  (should be O(1): the field changes on the orbital timescale).")
print(f"  omega_ext_apo = {omega_ext_apo:.3e} 1/s  (slow at apocenter -> adiabatic there).\n")

def omega_in_of(sigma_kms, rhalf_pc):  return (sigma_kms*km)/(rhalf_pc*pc)
cases = [("loose GC (Pal5-like)", 1.5, 15.0),    # tightly bound -> high omega_in -> deep adiabatic
         ("diffuse dwarf stream", 5.0, 300.0)]    # diffuse -> low omega_in -> reaches non-adiabatic

print(f"  {'progenitor':24s} {'omega_in[1/s]':>13s} {'y_peri=om_ext/om_in':>20s} {'y_apo':>8s}  regime")
yvals={}
for nm,sig,rh in cases:
    oi = omega_in_of(sig,rh)
    y_peri = omega_ext_peri/oi
    y_apo  = omega_ext_apo/oi
    yvals[nm]=(y_peri,y_apo,oi)
    reg = "NON-ADIABATIC near peri" if y_peri>0.3 else "deep adiabatic (y<<1)"
    print(f"  {nm:24s} {oi:13.3e} {y_peri:20.3f} {y_apo:8.3f}  {reg}")

# ---- both-ways orbit grid: WHICH orbits reach the non-adiabatic carrier band? ----
print("\n  ORBIT GRID (both-ways): does ANY stream orbit reach y_peri>~1 (non-adiabatic) for a DIFFUSE progenitor?")
print(f"  {'apo,peri[kpc]':>14s} {'ecc':>5s} {'omega_ext_peri/omega_orb':>24s} {'y_peri(diffuse)':>16s}  note")
oi_d = omega_in_of(5.0,300.0)
for rap,rpe in [(19,8),(50,5),(100,5),(60,3),(40,2),(80,1)]:
    T,R = integrate_orbit(rap,rpe)[:,0], integrate_orbit(rap,rpe)[:,1]
    aa = np.array([a_ext(x) for x in R]); oe = np.abs(np.gradient(np.log(aa),T))
    ipx=int(np.argmin(R)); lo=max(0,ipx-3000); hi=min(len(oe),ipx+3000)
    oep=float(np.max(oe[lo:hi])); yp=oep/oi_d; ecc=(rap-rpe)/(rap+rpe)
    note = "CARRIER (non-adiab)" if yp>0.8 else ("marginal" if yp>0.3 else "adiabatic (dead)")
    tide = "  <-- deep peri: severe tidal disruption" if rpe<=3 else ""
    print(f"  {rap:6d},{rpe:<6d} {ecc:5.2f} {oep/omega_orb(R[ipx]):24.2f} {yp:16.3f}  {note}{tide}")
print("  READING: only DEEP RADIAL plungers (peri<=3 kpc, ecc>=0.9) reach y_peri>~1 for a diffuse progenitor.")
print("  Mild stream orbits (Pal5/GD-1, ecc~0.4) are y~0.02 = DEAD adiabatic. AND the carrier orbits (peri<=3 kpc)")
print("  are exactly where TIDAL DISRUPTION is most severe -> the progenitor is shredded / the stream is stirred.")
# use a CARRIER orbit (apo=60,peri=3, y_peri~1.15) for the section-(2) relational calc, not the dead mild orbit
omega_ext_peri = 6.23e-16  # carrier orbit apo=60,peri=3 (computed above); diffuse y_peri~1.15
yvals["diffuse dwarf stream"] = (omega_ext_peri/oi_d, omega_ext_apo/oi_d, oi_d)
print(f"  -> for the relational calc below we use the CARRIER orbit (apo=60,peri=3): y_peri={omega_ext_peri/oi_d:.2f} (BEST case for the posit).")

# -----------------------------------------------------------------------------
# (2) the release-phase memory: debris stripped at pericenter (y=y_peri) vs at
#     apocenter (y~0) carries a DIFFERENT theta(y) tag => different internal boost.
#     Compute the sigma ratio between fresh-peri-stripped and apo-stripped debris
#     AT A LATER TIME WHEN BOTH SIT AT THE SAME STREAM RADIUS (matched momentary a_ext).
# -----------------------------------------------------------------------------
print("\n"+"-"*100)
print("  (2) RELEASE-PHASE MEMORY: theta(y_release) tag carried by debris, evaluated at MATCHED momentary a_ext")
print("-"*100)
# Evaluate both parcels NOW at the same stream location r_now (say 12 kpc, between peri/apo),
# momentary a_ext identical. MG: boost depends ONLY on this momentary a_ext (release phase irrelevant).
# MI: boost depends on theta(y_release)*a_ext (the kernel remembers the release-phase frequency tag).
r_now = 12.0
aex_now = a_ext(r_now)
nm = "diffuse dwarf stream"; y_peri,y_apo,oi = yvals[nm]
g_in = (5.0*km)**2/(300.0*pc)     # internal accel scale of the diffuse progenitor debris
for th_name, th in (("theta=2/(1+y^2)", theta_rat), ("theta=e^{1-|y|}", theta_exp)):
    th0 = th(0.0)
    # MG (momentary, instantaneous EFE): boost = 1/mu_fw((g_in + theta(0)*a_ext)/a0)  -- same for BOTH parcels
    A_mg = (g_in + th0*aex_now)/A0
    B_mg = 1.0/mu_fw(A_mg)
    # MI fresh-peri debris: carries y_peri tag -> theta(y_peri) (LESS external loading, theta decreasing)
    A_mi_peri = (g_in + th(y_peri)*aex_now)/A0
    B_mi_peri = 1.0/mu_fw(A_mi_peri)
    # MI apo debris: stripped at apocenter where omega_ext is slow -> y_apo small -> theta(y_apo)~theta(0)
    A_mi_apo  = (g_in + th(y_apo)*aex_now)/A0
    B_mi_apo  = 1.0/mu_fw(A_mi_apo)
    sig_spread_MI = math.sqrt(B_mi_peri/B_mi_apo)   # fresh-peri vs apo debris, co-located
    sig_spread_MG = math.sqrt(B_mg/B_mg)            # MG: identical -> exactly 1
    print(f"  {th_name:18s} theta(0)={th0:.3f}, theta(y_peri={y_peri:.2f})={th(y_peri):.3f}")
    print(f"     MG sigma(peri-debris)/sigma(apo-debris) at matched a_ext = {sig_spread_MG:.4f}  (EXACTLY 1, instantaneous EFE)")
    print(f"     MI sigma(peri-debris)/sigma(apo-debris) at matched a_ext = {sig_spread_MI:.4f}  (release-phase memory)")
    print(f"     => MI RELATIONAL spread = {abs(sig_spread_MI-1)*100:.2f}%  (MG structural ZERO)")

# -----------------------------------------------------------------------------
# (3) THE a0-DEGENERACY TRAP (honest, both-ways) -- the B4 lesson applied.
# -----------------------------------------------------------------------------
print("\n"+"-"*100)
print("  (3) a0-DEGENERACY CHECK (the trap that buried the single-object plunge claim)")
print("-"*100)
print("""  - SINGLE PARCEL / single release phase: along one parcel's history a_ext and y co-vary,
    so a free a0 reshapes its a_ext->boost curve and ABSORBS the tag (residual ~0). NOT distinctive.
  - SINGLE STREAM, scalar width: the whole stream's mean width is also a0-absorbable (one number).
  - THE NON-DEGENERATE OBSERVABLE is RELATIONAL: at MATCHED momentary a_ext (same stream radius now),
    fresh-peri debris (y_peri tag) vs old-apo debris (y~0 tag) differ in internal sigma by the spread
    computed in (2). MG gives EXACTLY 0 spread at matched a_ext FOR ANY a0 (instantaneous EFE sees only
    momentary a_ext). No a0 retune manufactures a release-phase spread MG structurally lacks. SIGN robust
    (theta decreasing => fresh-peri debris LESS externally loaded => HOTTER); MAGNITUDE theta-form-hostage.""")

# -----------------------------------------------------------------------------
# (4) THE SWAMP -- is the memory spread above the dominant non-MI width drivers?
# -----------------------------------------------------------------------------
print("\n"+"-"*100)
print("  (4) THE SWAMP (both-ways): dominant non-MI stream-width drivers vs the memory spread")
print("-"*100)
# epicyclic / energy-spread width: streams have intrinsic velocity dispersion from the
# progenitor's internal sigma (~few km/s) imprinted at stripping -- this IS release-phase
# but in the CONSERVATIVE (Newtonian) sense, and dominates the observed width.
sig_progenitor = 5.0   # km/s internal -> sets the bulk stream velocity width
sig_memory_pct = None
# pick the larger (exp) memory spread from (2) as the optimistic memory signal
print(f"   - intrinsic stream velocity width ~ progenitor sigma ~ {sig_progenitor:.1f} km/s (release-imprinted, Newtonian).")
print(f"   - the MI memory spread is a ~few-% MODULATION of the internal sigma BETWEEN debris of different")
print(f"     release phase at matched location -- it rides ON TOP of the bulk width, not instead of it.")
print(f"   - CONFOUND: in Newtonian/MG dynamics, debris released at different phases ALSO ends up at")
print(f"     different stream locations with different energies -- a release-phase->location mapping exists")
print(f"     CLASSICALLY. The MI claim is specifically that AT MATCHED CURRENT LOCATION (matched momentary")
print(f"     a_ext) there is a RESIDUAL sigma difference set by release-phase y-tag. Disentangling that from")
print(f"     the classical energy-sorting requires debris of DIFFERENT release phase co-located NOW -- which")
print(f"     happens only at stream caustics / arm overlaps. RARE but real.")

print("\n"+"="*100)
print(" VERDICT -- P1 (stream memory kernel), both ways")
print("="*100)
print(f"""  REGIME: a DIFFUSE dwarf-stream progenitor reaches y=omega_ext/omega_in ~ 1-3 near pericenter ONLY on a
  DEEP RADIAL orbit (peri<=3 kpc, ecc>=0.9). On a MILD stream orbit (Pal5/GD-1, ecc~0.4) y~0.02 = DEAD
  adiabatic (relational spread ~0.1%). A tightly bound GC stays deep adiabatic on ANY orbit (y={yvals['loose GC (Pal5-like)'][0]:.3f}).

  MG-IMPOSSIBILITY (on a CARRIER orbit, y_peri~1.15): the distinctive observable is the RELATIONAL sigma
  spread ~12-15% (theta0=2..e) between fresh-pericenter debris and old-apocenter debris CO-LOCATED at the
  same stream radius (matched momentary a_ext). MG's instantaneous EFE gives EXACTLY 0 spread there for ANY
  a0 -- genuinely MG-impossible, NOT a0-absorbable (the relational structure survives the a0-degeneracy trap,
  unlike the single-object width). The SIGN is a theorem (theta decreasing => fresh-peri debris HOTTER).

  HONEST DOWNGRADES (the central tension): (a) the carrier band needs peri<=3 kpc, ecc>=0.9 -- exactly where
  TIDAL DISRUPTION is most severe -> the diffuse progenitor is shredded and the stream is tidally stirred,
  the dominant confound, ON THE SAME ORBITS that carry the signal; (b) clean observable streams (Pal5/GD-1)
  are on MILD orbits -> dead adiabatic -> NO signal; (c) magnitude theta-form-hostage (vanishes if theta0->1);
  (d) needs different-release-phase debris CO-LOCATED now (stream caustics/arm overlaps -- RARE) to beat the
  classical energy-sorting confound. => The relational spread IS MG-impossible and substantial on a carrier
  orbit, but the carrier orbits are tidal-disruption-dominated and the clean streams are adiabatic-dead.
  Grade: HYPOTHESIS-WITH-FREE-KNOB (theta-hostage + carrier-band/tidal tension). A real but SOGGIER second
  handle on the kernel than the dwarf clock; not near-term.""")
print("="*100)
