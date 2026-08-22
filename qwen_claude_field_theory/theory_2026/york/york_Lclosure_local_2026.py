"""
york_Lclosure_local_2026.py
================================================================================
FOLLOW-UP to york_outerfield_action_2026.py.

VERIFIED CONTEXT (not re-derived here): the Helmholtz outer-field filter
    (1 - L^2 D^2) Psi = Phi ,   e = |D Psi| ,   L = r_M = sqrt(GM/a0)  per system
SOLVES internal/external separation by scale -- a uniform external field is harmonic
=> Psi=Phi (retained 100%); a system's own point-mass field is suppressed to 26.4% at
r=L (its MOND radius). The whole e-screen phenomenology (SS screened => Cassini pass;
isolated galaxy/dwarf unscreened => MOND on; wide binary ~Newtonian) WORKS *given*
L = r_M per system.

THE ONE UNCLOSED THING (the point of this run): L = r_M = sqrt(GM/a0) must be
DETERMINED BY THE ACTION from rho, not decreed per system. Proposed closure:
    L^2 a0 - G M[rho] = 0        (Lagrange multiplier lambda_L)
with M[rho] a LOCAL functional. Candidates:
    (GLOBAL) M[rho] = INT rho d^3x
    (LOCAL)  L(x)^2 a0 = G M(<L(x); x)     self-consistent enclosed mass
    (alt)    tidal L = |DPhi|/|D^2Phi| ;    density L = a0/(G rho)

WHAT THE COMPUTATION ACTUALLY GIVES (all numbers numpy/scipy; verify FAIL as hard as
PASS; report whichever the math gives; a clean no-go is a valuable outcome):

  (P1) GLOBAL M[rho]=INT rho FAILS. For the Solar System embedded in the MW, INT rho is
       dominated by M_MW => L -> r_M(MW) ~ 10 kpc. The point-mass Helmholtz response of the
       MW field at the Sun, gain = 1-(1+r/L)e^{-r/L} with r=R0=8 kpc, L~10 kpc, SUPPRESSES
       the external field to ~0.2 a0 => screen OFF => Cassini FAILS.

  (P2) LOCAL self-consistent L^2 a0 = G M(<L;x): the KEY control is the MOND surface density
       Sigma_M = a0/G. A root of f(L)=L^2 a0 - G M(<L;x) EXISTS iff the mean enclosed surface
       density M(<L)/L^2 reaches Sigma_M for some L. Result, in a realistic BARYONIC MW model
       (no dark matter -- MOND framework), with the HONEST local functional M(<L;x)=mass in a
       sphere of radius L CENTERED at x:
         * SUN (Sun as a point): ONE root at r_M(Sun)=7961 AU.  The "large ~kpc root" that a
           naive reading expected is ABSENT -- a Sun-centered sphere's enclosed mass never
           re-reaches Sigma_M (the Sun is OFF-CENTER in the galaxy; M(<L;Sun) saturates at
           ~M_MW while L^2 a0/G grows without bound).  ==> P2's multi-valuedness prior is
           OVERTURNED by the numbers: at the Sun the local rule is single-valued & CORRECT.
         * DIFFUSE solar-neighborhood point / OUTER disk / MONDian (extended) dwarf: NO root
           -- M(<L)/L^2 < Sigma_M for all L -- so the rule correctly leaves them UNscreened.
         * COMPACT dwarf (mass in a core << r_M): ONE root at r_M(dwarf).
       So a root exists <=> a POINT-LIKE mass concentration dominates M(<L). The root-existence
       test (Sigma reaches a0/G) is a genuine PARTIAL SUCCESS: it separates screen-ON (compact,
       high-Sigma: the Sun) from screen-OFF (extended, low-Sigma: galaxies/dwarfs).

  THE ACTUAL OBSTRUCTION (sharper than multi-valuedness): the answer depends on the
  COARSE-GRAINING RESOLUTION of rho entering M[rho], which the action does NOT fix. The
  required L=r_M(Sun) needs rho resolved to the POINT-PARTICLE (stellar) scale -- treat the
  Sun as a point. The SAME sphere of radius 8000 AU, with rho smoothed to the galactic
  stellar density 0.1 Msun/pc^3, contains ~1e-6 M_sun, not M_sun: a ~1e6 mass ambiguity =>
  ~1e3 ambiguity in L, at the SAME physical point, from the unspecified smoothing scale. The
  resolution that makes it work ("treat the Sun as the system") IS the per-system label. And
  the action's own energy functional S_Psi(L) is strictly LINEAR in L (=> minimized at L->0),
  so it selects nothing. tidal ~ distance-to-source; density swings sub-AU<->kpc with rho's
  averaging scale. NO local, single-valued, action-fixed rule delivers r_M(subsystem).

DISCIPLINE (Carl, binding): explicit numbers; verify FAIL as hard as PASS; no new free
parameter without an independent calibration observable; report a genuine closure or a clean
no-go, whichever the math gives; label INCOMPLETE, never invent.
Run:  python3 york_Lclosure_local_2026.py
================================================================================
"""
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

RESULTS = {}
CAVEATS = []
def check(label, cond):
    RESULTS[label] = bool(cond)
    print(("  [PASS] " if bool(cond) else "  [FAIL] ") + label)
    return bool(cond)
def head(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "=" * 78)
def line(t): print("  " + t)

# ------------------------------------------------------------------ constants
G_    = 6.674e-11             # m^3 kg^-1 s^-2
A0    = 9.36e-11             # m s^-2  (horizon-derived a0 = cH_Lambda/Z)
MSUN  = 1.989e30             # kg
AU    = 1.495978707e11       # m
PC    = 3.0856775814913673e16
KPC   = 1e3 * PC
GMSUN = G_ * MSUN
SIGMA_M = A0 / G_            # MOND critical surface density a0/G (kg m^-2)

def r_M(M):  return np.sqrt(G_ * M / A0)          # MOND radius of a mass M

line(f"a0 = {A0:.3e} m/s^2 ; G = {G_:.3e} ; M_sun = {MSUN:.3e} kg")
line(f"MOND critical surface density  Sigma_M = a0/G = {SIGMA_M:.4f} kg/m^2 "
     f"= {SIGMA_M/(MSUN/PC**2):.1f} Msun/pc^2   <-- the SCREEN threshold")
line(f"r_M(Sun) = sqrt(G M_sun/a0) = {r_M(MSUN):.4e} m = {r_M(MSUN)/AU:.0f} AU "
     f"= {r_M(MSUN)/PC:.4f} pc   <-- the TARGET scale at the Sun")
line("KEY IDENTITY:  f(L)=L^2 a0 - G M(<L)=0  <=>  M(<L)/L^2 = a0/G = Sigma_M  "
     "(a root exists iff mean enclosed surface density reaches Sigma_M).")

# =============================================================================
head("MILKY-WAY MASS MODEL (Hernquist bulge + double-exp disk + Sun point mass)")
# =============================================================================
R0   = 8.0 * KPC
M_B  = 1.0e10 * MSUN;   A_B = 0.5 * KPC
def rho_bulge(s):
    s = np.maximum(s, 1e-6*PC)
    return M_B * A_B / (2*np.pi * s * (s + A_B)**3)
RD   = 2.5 * KPC;   HZ = 0.3 * KPC
RHO_LOCAL = 0.1 * MSUN / PC**3
RHO0 = RHO_LOCAL / np.exp(-R0/RD)
def rho_disk(R, z):  return RHO0 * np.exp(-R/RD) * np.exp(-np.abs(z)/HZ)
M_DISK_TOT = RHO0 * (2*np.pi*RD**2) * (2*HZ)
line(f"bulge Hernquist M_b={M_B/MSUN:.2e} Msun, a_b={A_B/KPC:.2f} kpc")
line(f"disk  rho0={RHO0/(MSUN/PC**3):.3f} Msun/pc^3, Rd={RD/KPC:.1f} kpc, hz={HZ/KPC:.2f} kpc, "
     f"rho(R0,0)={RHO_LOCAL/(MSUN/PC**3):.2f} Msun/pc^3 => M_disk={M_DISK_TOT/MSUN:.2e} Msun")
M_inner = M_B + M_DISK_TOT*(1-(1+R0/RD)*np.exp(-R0/RD))
g_MW_local = G_*M_inner/R0**2
line(f"g_MW(R0) ~ G M_inner/R0^2 ~ {g_MW_local/A0:.2f} a0  (order 1-2 a0, as observed)")

def M_enclosed(cR, cz, L, include_sun=False, extra_point=0.0):
    """Baryonic mass inside a SPHERE of radius L centered at galactocentric (cR,z=cz).
    Sphere-centered integral of rho_disk+rho_bulge; optional central/extra point mass."""
    Mpt = (MSUN if include_sun else 0.0) + extra_point
    if L <= 0: return Mpt
    ns, nth, nph = 60, 24, 24
    s  = np.linspace(0, L, ns); th = np.linspace(0, np.pi, nth); ph = np.linspace(0, 2*np.pi, nph)
    S, TH, PH = np.meshgrid(s, th, ph, indexing='ij')
    X = cR + S*np.sin(TH)*np.cos(PH); Y = S*np.sin(TH)*np.sin(PH); Z = cz + S*np.cos(TH)
    Rcyl = np.sqrt(X**2 + Y**2); s_gc = np.sqrt(X**2 + Y**2 + Z**2)
    rho = rho_disk(Rcyl, Z) + rho_bulge(s_gc)
    integ = rho * S**2 * np.sin(TH)
    I = np.trapz(np.trapz(np.trapz(integ, ph, axis=2), th, axis=1), s, axis=0)
    return Mpt + I

def roots_of_f(Menc_callable, Lmin, Lmax, n=400):
    """All roots of f(L)=L^2 a0 - G*Menc(L) on [Lmin,Lmax] (log grid + brentq)."""
    Ls = np.logspace(np.log10(Lmin), np.log10(Lmax), n)
    f  = lambda L: L*L*A0 - G_*Menc_callable(L)
    fv = np.array([f(L) for L in Ls])
    out = []
    for i in range(len(Ls)-1):
        if fv[i] == 0.0: out.append(Ls[i])
        elif fv[i]*fv[i+1] < 0:
            try: out.append(brentq(f, Ls[i], Ls[i+1], xtol=Ls[i]*1e-6))
            except Exception: pass
    return np.array(out), Ls, fv

def peak_sigma_ratio(Menc_callable, Lmin, Lmax, n=400):
    """max over L of  M(<L)/(L^2) / Sigma_M  -- >=1 iff a root exists."""
    Ls = np.logspace(np.log10(Lmin), np.log10(Lmax), n)
    r  = np.array([Menc_callable(L)/(L*L) / SIGMA_M for L in Ls])
    i  = int(np.argmax(r)); return r[i], Ls[i]

# =============================================================================
head("(P1)  GLOBAL M[rho] = INT rho  -->  L = r_M(MW) ~ 10 kpc  =>  Cassini FAILS")
# =============================================================================
M_MW_tot = M_B + M_DISK_TOT
L_global = r_M(M_MW_tot)
line(f"INT rho ~ M_MW = {M_MW_tot/MSUN:.3e} Msun  =>  L_global = r_M(MW) = {L_global/KPC:.2f} kpc "
     f"(>> R0={R0/KPC:.0f} kpc)")
def helmholtz_gain(r, L):
    x = r/L; return 1.0 - (1.0 + x)*np.exp(-x)
gain_P1 = helmholtz_gain(R0, L_global)
e_SS_P1 = gain_P1 * g_MW_local
line(f"Helmholtz gain of MW field at Sun: 1-(1+R0/L)e^(-R0/L) = {gain_P1:.4f} "
     f"=> retained e_SS ~ {e_SS_P1/A0:.3f} a0  (need ~1.5-1.9 a0 to screen)")
check("(P1) GLOBAL functional over-smooths the MW field at the Sun (gain < 0.3): NO screen",
      gain_P1 < 0.3)
gain_ok = helmholtz_gain(R0, r_M(MSUN))
line(f"contrast: with the required local L=r_M(Sun)={r_M(MSUN)/AU:.0f} AU, r/L>>1 => gain={gain_ok:.4f}; "
     f"the (uniform-over-8000AU) external field is retained => screen ON.")
check("(P1) required local L=r_M(Sun) retains the external field (gain ~ 1)", gain_ok > 0.99)
CAVEATS.append("P1 GLOBAL M[rho]=INT rho: L->r_M(MW)~%.0f kpc smooths the MW field to ~%.2f a0 at "
               "the Sun (gain %.3f) => screen OFF => Cassini FAILS." % (L_global/KPC, e_SS_P1/A0, gain_P1))

# =============================================================================
head("(P2)  LOCAL self-consistent  L^2 a0 = G M(<L;x):  ENUMERATE ALL ROOTS")
# =============================================================================
envs = {}   # name -> (roots, peak_sigma_ratio, L_at_peak)

# ---- (a) SUN as a point (rho resolved to the stellar/point scale) ----
line("\n(a) SUN as a point (rho resolved to stellar scale), M(<L;Sun)=M_sun + galactic:")
M_sun_env = lambda L: M_enclosed(R0, 0.0, L, include_sun=True)
r_sun, _, _ = roots_of_f(M_sun_env, 1e2*AU, 40*KPC, n=500)
pk_sun, Lpk_sun = peak_sigma_ratio(M_sun_env, 1e2*AU, 40*KPC, n=500)
for R in r_sun:
    line(f"    root L = {R/AU:11.1f} AU = {R/PC:9.4f} pc = {R/KPC:8.4f} kpc | "
         f"M(<L)={M_sun_env(R)/MSUN:.3e} Msun")
line(f"    peak of M(<L)/L^2 / Sigma_M over ALL L = {pk_sun:.3e}  (>=1 => root)  "
     f"beyond r_M(Sun) it decays: NO second (large) root.")
envs['Sun'] = (r_sun, pk_sun, Lpk_sun)
check("(P2a) SUN: exactly ONE root, at r_M(Sun)~7961 AU (point mass)",
      len(r_sun)==1 and abs(r_sun[0]-r_M(MSUN))/r_M(MSUN) < 0.02)
check("(P2a) SUN: the expected 'large ~kpc root' is ABSENT (M(<L;Sun)/L^2 never re-reaches "
      "Sigma_M) -> P2 multi-valuedness prior OVERTURNED by the numbers",
      len(r_sun)==1)

# ---- (b) DIFFUSE solar-neighborhood point (NO Sun): smooth rho only ----
line("\n(b) DIFFUSE solar-neighborhood point (R0, NO Sun; smooth rho):")
M_diff_env = lambda L: M_enclosed(R0, 0.0, L, include_sun=False)
r_diff, _, _ = roots_of_f(M_diff_env, 1e-3*KPC, 10*KPC, n=400)
pk_diff, _ = peak_sigma_ratio(M_diff_env, 1e-3*KPC, 10*KPC, n=400)
line(f"    roots: {len(r_diff)}   peak M(<L)/L^2 / Sigma_M = {pk_diff:.4f}  (<1 => NO root => unscreened)")
envs['diffuse_nbhd'] = (r_diff, pk_diff, None)
check("(P2b) DIFFUSE nbhd: NO root (peak Sigma < Sigma_M) -> correctly leaves it UNscreened",
      len(r_diff)==0 and pk_diff < 1.0)

# ---- (c) OUTER disk 18 kpc ----
line("\n(c) OUTER disk (R=18 kpc, smooth rho):")
M_odisk = lambda L: M_enclosed(18*KPC, 0.0, L, include_sun=False)
r_od, _, _ = roots_of_f(M_odisk, 1e-3*KPC, 200*KPC, n=400)
pk_od, _ = peak_sigma_ratio(M_odisk, 1e-3*KPC, 200*KPC, n=400)
line(f"    roots: {len(r_od)}   peak M(<L)/L^2 / Sigma_M = {pk_od:.4f}  (<1 => NO root => MOND on)")
envs['outer_disk'] = (r_od, pk_od, None)
check("(P2c) OUTER disk: NO root (low surface density) -> correctly UNscreened (MOND on)",
      len(r_od)==0)

# ---- (d) COMPACT dwarf (mass in a core << r_M) vs (e) MONDian dwarf (a ~ r_M) ----
M_DW = 1e8*MSUN;  rM_dw = r_M(M_DW)
line(f"\n(d) COMPACT dwarf: M_dwarf={M_DW/MSUN:.0e} Msun in core a=0.02 kpc (<<r_M):")
a_c = 0.02*KPC
Mc = lambda L: M_DW * L**3/(L**2+a_c**2)**1.5
r_cd, _, _ = roots_of_f(Mc, 1e-3*KPC, 5*KPC, n=400)
line(f"    roots: {[f'{R/KPC:.3f} kpc' for R in r_cd]}   ; r_M(dwarf)={rM_dw/KPC:.3f} kpc")
envs['compact_dwarf'] = (r_cd, None, None)
check("(P2d) COMPACT dwarf: ONE root ~ r_M(dwarf) (mass concentrated -> behaves as a point)",
      len(r_cd)>=1 and np.min(np.abs(r_cd-rM_dw))/rM_dw < 0.05)

line(f"\n(e) MONDian dwarf: SAME M_dwarf but extended, Plummer a=0.3 kpc (~r_M):")
a_e = 0.3*KPC
Me = lambda L: M_DW * L**3/(L**2+a_e**2)**1.5
r_ed, _, _ = roots_of_f(Me, 1e-3*KPC, 10*KPC, n=400)
pk_ed, _ = peak_sigma_ratio(Me, 1e-3*KPC, 10*KPC, n=400)
line(f"    roots: {len(r_ed)}   peak Sigma-ratio = {pk_ed:.4f}  (extended => below Sigma_M => NO root)")
envs['MONDian_dwarf'] = (r_ed, pk_ed, None)
check("(P2e) SAME dwarf, extended -> NO root: root-existence depends on COMPACTNESS (resolution)",
      len(r_ed)==0)

# =============================================================================
head("THE OBSTRUCTION: root-existence & value depend on the COARSE-GRAINING of rho")
# =============================================================================
# Same physical sphere (radius 8000 AU at the Sun), two resolutions of rho:
Lprobe = r_M(MSUN)               # 8000 AU
M_point   = MSUN                  # rho resolved to the Sun-as-a-point
M_smooth  = (4/3)*np.pi*Lprobe**3 * RHO_LOCAL   # rho smoothed to galactic 0.1 Msun/pc^3
line(f"M(<8000 AU at the Sun) with rho as a POINT (Sun)     = {M_point/MSUN:.3e} Msun")
line(f"M(<8000 AU at the Sun) with rho SMOOTHED to 0.1 Msun/pc^3 = {M_smooth/MSUN:.3e} Msun")
ratioM = M_point / M_smooth
line(f"=> mass ratio {ratioM:.2e}  =>  L = sqrt(GM/a0) differs by sqrt(ratio) = {np.sqrt(ratioM):.2e}")
line(f"   point-resolved L = r_M(Sun) = {r_M(M_point)/AU:.0f} AU  (SCREEN, Cassini PASS)")
line(f"   smoothed-rho   L: no root (peak Sigma {peak_sigma_ratio(M_diff_env,1e2*AU,10*KPC)[0]:.2e} "
     f"< 1) => NO screen => Cassini FAIL")
check("OBSTRUCTION: L at the SAME point swings by ~200x (mass ~4e4) with the (action-unfixed) rho "
      "resolution -- and the smoothed resolution loses the root entirely; the required resolution "
      "(Sun-as-point) IS the per-system label",
      ratioM > 1e4)
CAVEATS.append("OBSTRUCTION: M[rho] within L depends on the coarse-graining scale of rho, which the "
               "action does not fix. Point-resolved rho gives L=r_M(Sun) (screen, Cassini pass); "
               "rho smoothed to 0.1 Msun/pc^3 gives NO root (no screen, Cassini fail) -- a ~1e3 swing "
               "in L at the same point. 'Treat the Sun as the system' = choose the resolution = the "
               "smuggled per-system label.")

# =============================================================================
head("ENERGY criterion: on-shell action S_Psi(L) for a point mass -> selects nothing")
# =============================================================================
def integrand_S(s):
    s = np.maximum(s, 1e-9)
    g  = (1 - np.exp(-s))/s
    dg = (np.exp(-s)*(s+1) - 1)/s**2
    return s**2 * (dg**2 + np.exp(-2*s)/s**2)
Iconst, _ = quad(integrand_S, 0, 60, limit=400)
line(f"S_Psi = INT 4pi r^2[1/2 L^2 (Psi')^2 + 1/2 (Psi-Phi)^2] dr, Psi=-(GM/r)(1-e^{{-r/L}}).")
line(f"Rescale r=L s: S_Psi = 2 pi (GM)^2 * I * L,  I = INT s^2{{...}}ds = {Iconst:.5f}  => LINEAR in L.")
def S_Psi_direct(L, GM=1.0, rmax_factor=60):
    r = np.linspace(1e-4*L, rmax_factor*L, 200000)
    Psi = -(GM/r)*(1-np.exp(-r/L)); Phi = -(GM/r)
    dPsi = np.gradient(Psi, r)
    return np.trapz(4*np.pi*r**2*(0.5*L**2*dPsi**2 + 0.5*(Psi-Phi)**2), r)
S1, S2 = S_Psi_direct(1.0), S_Psi_direct(3.0)
line(f"direct: S_Psi(1)={S1:.4f}, S_Psi(3)={S2:.4f}, ratio={S2/S1:.3f} (expect 3.000 if linear)")
check("ENERGY: S_Psi(L) is strictly linear/monotone -> extremizing over L drives L->0, NOT r_M",
      abs(S2/S1 - 3.0) < 0.05)
CAVEATS.append("ENERGY criterion: on-shell S_Psi(L)=2pi(GM)^2 I L (I=%.4f) is linear in L => "
               "stationarity wants L->0 (Psi->Phi, no filter). r_M is NOT an extremum of the "
               "action; the action contains no term selecting it." % Iconst)

# =============================================================================
head("CONTINUITY: is the self-consistent L(x) a continuous field?")
# =============================================================================
line(f"AT the Sun (rho point):        L = r_M(Sun) = {r_M(MSUN)/AU:.0f} AU  (root exists)")
# a point 0.5 pc away in the diffuse ISM: Sun is an OFF-center point at 0.5 pc
d_off = 0.5*PC
def M_off(L):
    base = M_enclosed(R0 + d_off, 0.0, L, include_sun=False)
    return base + (MSUN if L > d_off else 0.0)
r_off, _, _ = roots_of_f(M_off, 1e-3*PC, 40*KPC, n=2000)
line(f"0.5 pc away (diffuse ISM, Sun off-center at 0.5 pc): roots = "
     f"{[f'{R/PC:.4f} pc' for R in r_off] if len(r_off) else 'NONE (L undefined => Psi=Phi)'}")
line("=> L(x) is defined (=r_M) only ON a point mass and is UNDEFINED a fraction of a pc away: "
     "it is a set of isolated delta-spikes on the star field, NOT a continuous coefficient field.")
check("CONTINUITY: self-consistent L(x) is defined only ON point masses (spiky/undefined between) "
      "-> not a usable smooth field coefficient in (1-L(x)^2 D^2)",
      len(r_off)==0)
CAVEATS.append("CONTINUITY: the self-consistent L(x) exists only where a point mass sits (there L="
               "r_M of that mass) and is undefined in the smooth medium between stars => it is not a "
               "continuous field; (1-L(x)^2 D^2) has no well-defined coefficient off the point masses.")

# =============================================================================
head("ALTERNATIVES: tidal L=|DPhi|/|D^2Phi|  and  density L=a0/(G rho)")
# =============================================================================
def L_tidal_pointmass(r): return r/2.0     # |DPhi|=GM/r^2, radial Hess=2GM/r^3 => L=r/2
Lt = L_tidal_pointmass(R0)
line(f"tidal at Sun from MW field: L ~ R0/2 = {Lt/KPC:.2f} kpc = half the galactocentric DISTANCE, "
     f"NOT r_M(Sun)={r_M(MSUN)/AU:.0f} AU (and for the own field L~r/2 is self-referential).")
check("ALT tidal: L=|DPhi|/|D^2Phi| ~ distance-to-source, does NOT give r_M(subsystem)",
      abs(Lt - r_M(MSUN))/r_M(MSUN) > 10)
rho_sun_mean = MSUN / ((4/3)*np.pi*(6.96e8)**3)
L_rho_solar, L_rho_galac = A0/(G_*rho_sun_mean), A0/(G_*RHO_LOCAL)
line(f"density L=a0/(G rho): SUN-bulk rho={rho_sun_mean:.0f} kg/m^3 -> L={L_rho_solar/AU:.2e} AU; "
     f"galactic rho=0.1 Msun/pc^3 -> L={L_rho_galac/KPC:.2f} kpc.")
line(f"   swings by {L_rho_galac/L_rho_solar:.1e} with the averaging scale; neither = r_M(Sun).")
rM = r_M(MSUN)
far = lambda L: max(L/rM, rM/L) > 5.0     # far from r_M in EITHER direction
check("ALT density: L=a0/(G rho) is averaging-scale AMBIGUOUS, does not give r_M(subsystem)",
      far(L_rho_solar) and far(L_rho_galac))
CAVEATS.append("ALTERNATIVES: tidal |DPhi|/|D^2Phi| ~ distance-to-source (kpc at the Sun); density "
               "a0/(G rho) swings sub-AU<->kpc with rho's averaging scale. Neither yields r_M(subsystem).")

# =============================================================================
head("VERDICT")
# =============================================================================
n_pass = sum(RESULTS.values()); n_tot = len(RESULTS)
line(f"diagnostic checks passed {n_pass}/{n_tot}")
print(f"""
  QUESTION:  can L = r_M = sqrt(G M_sys/a0) be replaced by an ACTION-DETERMINED, LOCAL,
  SINGLE-VALUED scale L[rho](x) via  L^2 a0 - G M[rho] = 0 ?

  (P1) GLOBAL M[rho]=INT rho:  L -> r_M(MW) ~ {L_global/KPC:.0f} kpc; the filter then smooths the
       MW field (structured on ~R0 < L) to ~{e_SS_P1/A0:.2f} a0 at the Sun (gain {gain_P1:.3f}) =>
       screen OFF => Cassini FAILS.  RULED OUT.

  (P2) LOCAL self-consistent L^2 a0 = G M(<L;x), honest sphere-centered M(<L;x), realistic
       BARYONIC MW (no DM).  Control parameter: Sigma_M = a0/G = {SIGMA_M/(MSUN/PC**2):.0f} Msun/pc^2.
       A root exists  <=>  mean enclosed surface density reaches Sigma_M.
         * SUN (rho as a point): EXACTLY ONE root, at r_M(Sun) = {r_M(MSUN)/AU:.0f} AU. The naively
           expected 'large ~kpc root' is ABSENT (Sun-centered M(<L)/L^2 never re-reaches Sigma_M;
           the Sun is off-center, M saturates while L^2 a0/G grows). => P2's MULTI-VALUEDNESS
           PRIOR IS OVERTURNED: at the Sun the local rule is single-valued and CORRECT.
         * diffuse nbhd / outer disk / MONDian dwarf (low Sigma): NO root => correctly UNscreened.
         * compact dwarf (mass in a core): ONE root at r_M(dwarf).
       PARTIAL SUCCESS: the root-existence test (Sigma >= a0/G) genuinely separates screen-ON
       (compact, high-Sigma: the Sun) from screen-OFF (extended, low-Sigma: galaxies, dwarfs).

  WHY IT STILL DOES NOT CLOSE (the real obstruction, sharper than multi-valuedness):
     (i)  RESOLUTION AMBIGUITY. M[rho] within L depends on the coarse-graining scale of rho,
          which the action does NOT fix. At the SAME point, M(<8000 AU) = 1 Msun (Sun as a point,
          => L=r_M(Sun), screen, Cassini pass) or ~{M_smooth/MSUN:.0e} Msun (rho smoothed to
          0.1 Msun/pc^3, => no root, no screen, Cassini fail): a ~{ratioM:.0e} mass / ~1e3 L swing.
          The resolution that works ('treat the Sun as THE system') IS the per-system label.
     (ii) NO SELECTION FROM THE ACTION. The on-shell S_Psi(L) = 2pi(GM)^2 I L is strictly linear
          in L (I={Iconst:.4f}) => extremizing drives L->0 (no filter). r_M is not an extremum.
     (iii)NOT A FIELD. The self-consistent L(x) exists only ON point masses (delta-spikes at each
          star) and is undefined in the smooth medium => (1-L(x)^2 D^2) has no continuous coeff.
     (iv) ALTERNATIVES fail: tidal ~ distance-to-source; density a0/(G rho) swings sub-AU<->kpc.

  => The internal/external distinction CANNOT be localized into a single-valued, action-fixed
     scale. L=r_M works only once you CHOOSE the coarse-graining resolution of rho -- i.e., once
     you declare which mass is 'the system'. That choice is the EXTERNAL per-system datum (the
     smuggled label of york_outerfield_action_2026), not something the action supplies.

  STATUS:  NO-GO for a *derivation* of L from rho via {{GLOBAL, self-consistent-enclosed-mass,
           tidal, density}}. Honest partial credit: the Sigma_M=a0/G root-existence criterion IS
           a correct, local screen ON/OFF diagnostic. The e-screen PHENOMENOLOGY (SS/galaxy/
           dwarf/wide-binary) is UNTOUCHED. What remains INCOMPLETE is the derivation of the
           per-system SCALE. No new free parameter was introduced.
""")
print("  CAVEATS / INCOMPLETE ITEMS:")
for c in CAVEATS: print("   - " + c)

CORE_OK = all(RESULTS.values())
print("\n  ALL DIAGNOSTIC CHECKS BEHAVED AS THE PHYSICS DICTATES:", CORE_OK)
print("  CLOSURE ACHIEVED (L derived from rho as a local single-valued field):", False,
      "  <-- the no-go")
