#!/usr/bin/env python3
"""
GAIA DR4 WIDE-BINARY PRE-REGISTRATION -- framework boost curve (Agent B, 2026-07-02)
====================================================================================
Framework on its OWN terms (de Sitter-Unruh MODIFIED INERTIA):
    a0   = 9.36e-11 m/s^2  (= c H_Lambda / Z, Z = sqrt(32 pi / 3))   [banked]
    nu(y)= sqrt(1 + 1/y),  y = g_bar/a0   i.e.  g_obs = sqrt(g_bar^2 + g_bar a0)
    NOT McGaugh's nu. Judged from its own premises.

External field at the Sun (banked): g_ext,obs ~ 1.9 a0 (= 1.778e-10 m/s^2,
the standard solar-neighborhood value; e.g. McMillan 2017-class Galactic models).

Observable: gamma_v(s) = (RMS relative orbital velocity) / (Newtonian RMS)
at projected separation s, for circular-orbit scaling v ~ sqrt(g r):
    gamma_v = sqrt(g_eff / g_N).
Curves computed on r = s (deprojection r >~ s_proj noted as a caveat; it shifts
the transition ~10-20% in s, not the asymptote).

THREE CURVES:
 (1) Newton: 1 exactly.
 (2) MG / AQUAL-EFE phenomenology: point-field argument y_tot = |y_int + y_ext,N|,
     boost = <nu(y_tot)>_angles. Asymptote -> nu(y_ext,N): the banked MG value
     gamma = 1.137 (velocity ratio; force boost ~1.29).
 (3) Framework MI-EFE, computed PER STAR: each star's acceleration follows the
     framework algebraic law applied to ITS total Newtonian field
         a_i = nu(|g_ext,N + g_i,N|/a0) * (g_ext,N + g_i,N),
     relative acceleration a_rel = a_1 - a_2, angle-averaged over orbit
     orientation. The nu' cross-term along e_ext SUPPRESSES the boost relative
     to MG (this is the MI-distinctive anisotropy). Asymptote -> upper edge of
     the banked band (gamma_v ~ 1.10).
     LOWER EDGE of the band (~1.05): the same dynamical curve passed through a
     crude Banik-style observable dilution (factor 0.5 on the velocity excess,
     from eccentricity/phase/projection marginalization in the v_p/v_c
     statistic). HONESTY FLAG: the per-star algebraic law is a PRESCRIPTION,
     not a completion -- the framework's MI completion is UNWRITTEN (banked
     trichotomy: local=ghost, field=Cassini, nonlocal=anti-MOND). The band is
     therefore a prescription+observable bracket, not a theorem.

A0-DEGENERACY CHECK: rerun MI curve with Milgrom a0 = 1.2e-10 at the SAME
physical g_ext -- shows the curve moves by only ~3% in gamma_v for a 22% move
in a0: DR4 tests the nu+EFE prescription, NOT the value 9.36e-11.

Every number printed here is reproduced by this script; exit 0 on pass.
"""
import numpy as np

G    = 6.674e-11        # m^3 kg^-1 s^-2
MSUN = 1.989e30         # kg
AU   = 1.496e11         # m

A0_FW  = 9.36e-11       # framework canonical (banked; cH_Lambda/Z)
A0_MIL = 1.2e-10        # Milgrom conventional, for the degeneracy check
GEXT_OBS_PHYS = 1.9 * A0_FW   # 1.778e-10 m/s^2, banked physical external field

M_TOT = 1.5 * MSUN      # typical DR4 WB pair (~1.0+0.5 Msun); asymptote is M-independent

def nu(y):
    return np.sqrt(1.0 + 1.0/y)

def y_newt_from_obs(y_obs):
    """Invert g_obs = sqrt(g_N^2 + g_N a0):  y_N^2 + y_N - y_obs^2 = 0."""
    return 0.5*(-1.0 + np.sqrt(1.0 + 4.0*y_obs**2))

NCOS = 4001
COS  = np.linspace(-1.0, 1.0, NCOS)   # isotropic orbit-orientation average

def boost_MG(y_int, y_ext_N):
    """AQUAL-EFE phenomenology: force boost = <nu(|y_int e + y_ext z|)>."""
    yt = np.sqrt(y_int**2 + y_ext_N**2 + 2.0*y_int*y_ext_N*COS)
    return np.mean(nu(yt))

def boost_MI_perstar(y_rel, y_ext_N):
    """Framework per-star algebraic MI law, equal masses (y_star = y_rel/2).
    e_ext = z; internal separation axis at angle theta.
    Star1 Newtonian field: y_ext z + y_s e ; Star2: y_ext z - y_s e.
    a_i = nu(|y_i|) y_i ; force boost = |a1 - a2| / y_rel, angle-averaged."""
    ys = 0.5*y_rel
    s_ = np.sqrt(1.0 - COS**2)
    # components (z, x) in units of a0
    y1z, y1x = y_ext_N + ys*COS,  ys*s_
    y2z, y2x = y_ext_N - ys*COS, -ys*s_
    m1 = np.hypot(y1z, y1x); m2 = np.hypot(y2z, y2x)
    az = nu(m1)*y1z - nu(m2)*y2z
    ax = nu(m1)*y1x - nu(m2)*y2x
    return np.mean(np.hypot(az, ax) / y_rel)

def curves(a0, gext_phys, mtot):
    y_ext_obs = gext_phys / a0
    y_ext_N   = y_newt_from_obs(y_ext_obs)
    s_kAU = np.array([1., 2., 3., 5., 7., 10., 15., 20., 30.])
    r = s_kAU * 1e3 * AU
    y_rel = G*mtot/(r**2) / a0
    gv_MG = np.array([np.sqrt(boost_MG(y, y_ext_N))       for y in y_rel])
    gv_MI = np.array([np.sqrt(boost_MI_perstar(y, y_ext_N)) for y in y_rel])
    gv_MI_low = 1.0 + 0.5*(gv_MI - 1.0)   # crude observable dilution (lower edge)
    # asymptotes (y_rel -> 0)
    asy_MG = np.sqrt(boost_MG(1e-6, y_ext_N))
    asy_MI = np.sqrt(boost_MI_perstar(1e-6, y_ext_N))
    return dict(y_ext_obs=y_ext_obs, y_ext_N=y_ext_N, s=s_kAU, y_rel=y_rel,
                MG=gv_MG, MI=gv_MI, MI_low=gv_MI_low, asy_MG=asy_MG, asy_MI=asy_MI)

fw  = curves(A0_FW,  GEXT_OBS_PHYS, M_TOT)
mil = curves(A0_MIL, GEXT_OBS_PHYS, M_TOT)

# analytic cross-check of the MI asymptote: nu(yE)*(1 + L/3), L = -1/(2(yE+1))
yE = fw['y_ext_N']; L = -1.0/(2.0*(yE+1.0))
asy_analytic = np.sqrt(nu(yE)*(1.0 + L/3.0))

r_trans = np.sqrt(G*M_TOT/A0_FW) / (1e3*AU)   # g_N,int = a0 crossing, kAU

print("="*78)
print("GAIA DR4 WIDE-BINARY PRE-REGISTRATION -- framework curve (locked 2026-07-02)")
print("="*78)
print(f"a0 (framework)        = {A0_FW:.3e} m/s^2   nu(y)=sqrt(1+1/y)")
print(f"g_ext observed        = {GEXT_OBS_PHYS:.3e} m/s^2 = {fw['y_ext_obs']:.3f} a0 (banked 1.9)")
print(f"g_ext Newtonian       = {fw['y_ext_N']:.4f} a0   (quadratic inversion)")
print(f"M_tot = {M_TOT/MSUN:.2f} Msun ; g_N,int = a0 at r = {r_trans:.2f} kAU (transition scale ~ sqrt(M))")
print()
hdr = f"{'s [kAU]':>8} {'g_N,int/a0':>11} {'Newton':>7} {'MI low(obs-dil)':>16} {'MI dyn(upper)':>14} {'MG/AQUAL':>9}"
print(hdr); print("-"*len(hdr))
for i, s in enumerate(fw['s']):
    print(f"{s:8.0f} {fw['y_rel'][i]:11.3f} {1.0:7.3f} {fw['MI_low'][i]:16.3f} "
          f"{fw['MI'][i]:14.3f} {fw['MG'][i]:9.3f}")
print()
print(f"Asymptotes (s->inf):  MI dynamical gamma_v = {fw['asy_MI']:.4f} "
      f"(analytic check {asy_analytic:.4f}); diluted = {1+0.5*(fw['asy_MI']-1):.4f}")
print(f"                      MG/AQUAL     gamma_v = {fw['asy_MG']:.4f} (banked 1.137)")
print()
print("A0-DEGENERACY (same physical g_ext, Milgrom a0=1.2e-10):")
print(f"  MI asymptote: framework a0 -> {fw['asy_MI']:.3f} ; Milgrom a0 -> {mil['asy_MI']:.3f}"
      f"   (22% a0 shift -> {100*abs(mil['asy_MI']-fw['asy_MI']):.1f}% gamma_v shift)")
print(f"  MG asymptote: framework a0 -> {fw['asy_MG']:.3f} ; Milgrom a0 -> {mil['asy_MG']:.3f}")
print(f"  => Milgrom-a0 MI ({mil['asy_MI']:.3f}) ~ framework-a0 MG lower range: prescriptions")
print(f"     and a0 values interleave; DR4 constrains nu+EFE physics, NOT a0=9.36e-11.")
print()

# ---- assertions: lock the banked numbers ----
assert abs(fw['asy_MG'] - 1.137) < 0.005, "MG asymptote drifted off banked 1.137"
assert 1.095 < fw['asy_MI'] < 1.105,      "MI dynamical asymptote off banked upper edge 1.10"
assert 1.045 < 1+0.5*(fw['asy_MI']-1) < 1.055, "diluted edge off banked lower edge 1.05"
assert abs(fw['asy_MI'] - asy_analytic) < 2e-3, "numeric vs analytic MI asymptote mismatch"
assert abs(fw['y_ext_N'] - 1.4647) < 0.002
print("ALL ASSERTIONS PASS (banked band + MG value reproduced from the framework's own nu).")
