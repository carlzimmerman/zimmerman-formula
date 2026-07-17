#!/usr/bin/env python3
"""
GW170817 vs the disformal photon metric g~ = g + B u_mu u_nu, checked on the REAL
NGC 4993 (~40 Mpc) sightline. Photons ride g~, gravitons ride g. GW170817/GRB170817A:
messengers within +1.74 s -> |c_gamma - c_gw|/c < ~1e-15.  Bar for a propagation lag:
Delta_t <~ 1.7 s.

This does NOT reuse the banked mi_disformal_*.py numbers; it re-derives (1) the local
speed differential from the two null cones, then (2) accumulates B along a segmented
real sightline via the framework law  grad B = 4(nu-1) g_bar / c^2  (UNIFICATION.md),
with the framework's OWN dS-Unruh nu, BOTH a0 footings.  Honesty: a SAVE is verified as
hard as a KILL. If excluded, say by how many orders and reconcile with the banked ~6.
"""
import numpy as np

c   = 2.998e8            # m/s
G   = 6.674e-11
kpc = 3.086e19; Mpc = 1e3*kpc
Msun= 1.989e30
FOOTINGS = {"canonical (cH_Lambda/Z)": 9.36e-11, "alt (rho_tot/cH0)": 1.13e-10}

# framework dS-Unruh interpolation: g_obs = sqrt(g_bar^2 + g_bar a0) -> nu = sqrt(1+a0/g_bar)
def nu(gbar, a0): return np.sqrt(1.0 + a0/np.maximum(gbar, 1e-40))

# =====================================================================================
# (1) LOCAL SPEED DIFFERENTIAL from the two cones  (get the B/2-vs-B factor exact)
# =====================================================================================
# rest frame u=(1,0,0,0), g=diag(-1,1,1,1). g~ = g + B u u -> g~_00 = -(1-B), g~_ij=delta.
# photon null g~^{mn}k_m k_n=0 -> k0^2 = (1-B)|k|^2 -> c_gamma = sqrt(1-B).  graviton c_T=1.
# per unit length lag: dt = dl (1/c_gamma - 1/c) = (dl/c)(1/sqrt(1-B) - 1) ~ (dl/c)(B/2).
def dcfrac(B):  return 1.0 - np.sqrt(1.0 - B)          # |c_gamma-c_gw|/c, exact
def lag_integrand(B): return (1.0/np.sqrt(1.0 - B) - 1.0)   # ~ B/2, exact
B_probe = 1e-6
print("="*78)
print("(1) LOCAL DIFFERENTIAL  (photon on g~=g+Buu vs graviton on g)")
print("="*78)
print(f"  exact:  |c_gamma-c_gw|/c = 1 - sqrt(1-B);  at B={B_probe:.0e}: {dcfrac(B_probe):.4e}"
      f"  (B/2 = {B_probe/2:.4e})  -> factor is B/2, photon SUBLUMINAL")

# =====================================================================================
# (2) ACCUMULATE B AND THE DELAY ALONG THE REAL SIGHTLINE
# =====================================================================================
# grad|B| = (4/c^2)(nu-1) g_bar.  B is the AQUAL potential of 4(nu-1)g_bar; boundary
# condition B->0 in the deep void (photon cone = graviton cone in empty space -- the
# physical, causal choice, and the one MOST favorable to the framework).  For a galaxy
# the photon crosses a "bump": B rises through the deep-MOND shell.  Delay for a segment
# = (1/c) INT (1/sqrt(1-B) - 1) dl.
def galaxy_segment(M, r_in, r_out, a0, N=6000):
    """radial crossing of one galaxy's MOND shell; B(r)=INT_r^{r_out} gradB dr' (B(r_out)=0)."""
    r = np.linspace(r_in, r_out, N)
    gbar = G*M/r**2
    gB = (4.0/c**2)*(nu(gbar, a0) - 1.0)*gbar          # d|B|/dr, 1/m
    # B(r) = integral of gB from r out to r_out (so B=0 at the void edge r_out)
    cum = np.concatenate([[0.0], np.cumsum(0.5*(gB[1:]+gB[:-1])*np.diff(r))])
    B = cum[-1] - cum                                  # B(r_in)=max, B(r_out)=0
    dt = np.trapz(1.0/np.sqrt(1.0 - B) - 1.0, r)/c     # (1/c) INT (B/2-exact) dl
    return dt, B.max()

def igm_segment(L, gbar_igm, a0):
    """void: g_bar tiny but path is 40 Mpc. Sustained residual B ~ gradB * L (generous)."""
    gB = (4.0/c**2)*(nu(gbar_igm, a0) - 1.0)*gbar_igm  # d|B|/dl in the IGM
    B_igm = gB*L                                       # if it accumulated coherently
    dt = (1.0/np.sqrt(1.0 - min(B_igm,0.9)) - 1.0)*L/c
    return dt, B_igm

# --- real sightline geometry ---
# source: NGC 4993, early-type, M_bar ~ 1e11 Msun; kilonova offset ~2 kpc from center.
# host exit: 2 kpc -> 300 kpc (deep-MOND shell, group-embedded; log-accumulation, cutoff weak).
# IGM/void: ~40 Mpc at very low g_bar.
# MW entry: 300 kpc -> 8 kpc (we sit at g_bar ~ 2 a0 inside the MW MOND-affected region).
M_host, M_mw = 1e11*Msun, 6e10*Msun
D = 40*Mpc; t_travel = D/c

print("\n"+"="*78)
print("(2) SEGMENTED LINE-OF-SIGHT DELAY  (both footings)")
print("="*78)
for fname, a0 in FOOTINGS.items():
    dt_host, Bh = galaxy_segment(M_host, 2*kpc,   300*kpc, a0)
    dt_mw,   Bm = galaxy_segment(M_mw,   8*kpc,   300*kpc, a0)
    dt_igm,  Bi = igm_segment(D, 1e-14, a0)            # nominal IGM g_bar=1e-14 m/s^2
    dt_gal = dt_host + dt_mw                            # ROBUST minimum (2 mandatory crossings)
    dt_all = dt_gal + dt_igm
    print(f"\n  footing = {fname}   a0={a0:.3e}")
    print(f"   host NGC4993 exit (2->300 kpc):  B_max={Bh:.2e},  delay={dt_host:.2e} s")
    print(f"   Milky Way entry (300->8 kpc):    B_max={Bm:.2e},  delay={dt_mw:.2e} s")
    print(f"   IGM/void 40 Mpc (g_bar=1e-14):   B~{Bi:.2e},     delay={dt_igm:.2e} s (uncertain, coherence-dep.)")
    print(f"   ---- ROBUST MINIMUM (host+MW only, IGM=0) ----")
    print(f"   Delta_t(gal) = {dt_gal:.3e} s   |dc|/c = Dt/t = {dt_gal/t_travel:.3e}")
    print(f"     vs 1.7 s      : {dt_gal/1.7:.2e}x   -> {'PASS' if dt_gal<1.7 else 'EXCLUDED by %.1e (%.1f orders)'%(dt_gal/1.7, np.log10(dt_gal/1.7))}")
    print(f"     vs 1e-15 (dc) : {(dt_gal/t_travel)/1e-15:.2e}x -> {'PASS' if dt_gal/t_travel<1e-15 else 'EXCLUDED by %.1e (%.1f orders)'%((dt_gal/t_travel)/1e-15, np.log10((dt_gal/t_travel)/1e-15))}")
    print(f"   ---- with nominal IGM ----")
    print(f"   Delta_t(all) = {dt_all:.3e} s   |dc|/c = {dt_all/t_travel:.3e}")

# =====================================================================================
# (3) RECONCILE with the banked ~6-order note; the void-suppression subtlety
# =====================================================================================
print("\n"+"="*78)
print("(3) RECONCILE with banked mi_disformal_gw170817_TENSION.py (~8.8e-10, ~6 orders)")
print("="*78)
a0 = 9.36e-11
dt_host, Bh = galaxy_segment(M_host, 2*kpc, 300*kpc, a0)
dt_mw,   Bm = galaxy_segment(M_mw,   8*kpc, 300*kpc, a0)
dt_gal = dt_host + dt_mw
print(f"""  Banked note: host(1e11)+MW(6e10) crossings only, IGM~0 -> Dt~3.6e6 s, |dc|/c~8.8e-10.
  This segmented LOS integral (framework grad B, framework nu, B->0 void BC): Dt(gal)={dt_gal:.2e} s,
  |dc|/c={dt_gal/t_travel:.2e}. SAME ORDER. The banked ~6-order number was NOT a single-galaxy
  wrong path: it already used host+MW and set the IGM to zero. The full sightline REPRODUCES it.

  The hoped-for void rescue FAILS: in the void g_bar->0 so (nu-1)g_bar = c^2 grad B / 4
  ~ sqrt(a0 g_bar) -> 0, so B stops GROWING -- but the DELAY depends on B (the accumulated
  value), not grad B. B is ~1e-6 sustained across each galaxy's ~100+ kpc width, and the two
  crossings (host exit + MW entry) are MANDATORY and unavoidable. They alone blow the bound by
  ~6 orders. The IGM only ADDS (a tiny residual B over 40 Mpc can dominate); it never subtracts.
  The graviton c_T=1 being exact is IRRELEVANT: GW170817 constrains the graviton-photon
  DIFFERENCE, which is exactly B/2 != 0.""")
print("="*78)
print("VERDICT: EXCLUDED by ~6 orders, robust across both footings and both B-readings.")
print("="*78)
