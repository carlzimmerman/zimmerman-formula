#!/usr/bin/env python3
"""
LANE 0 -- THE TARGET for any source-side lensing mechanism in the MI framework.

Framework premises (Carl Zimmerman, de Sitter-Unruh modified inertia):
  nu(y) = sqrt(1 + 1/y),  y = g_bar/a0,  g_obs = nu * g_bar = sqrt(g_bar^2 + g_bar*a0)
  a0 canonical = 9.36e-11 m/s^2 (cH_Lambda/Z);  alt footing = 1.13e-10 m/s^2 (cH0/rho_total)

Because GW170817 forces any lensing enhancement into the ONE shared metric as a
SOURCE, the required effective source is:
  rho_eff(r) = (1/4 pi G) div[(nu-1) g_bar r_hat]
  M_eff(r)   = (r^2/G) (nu-1) g_bar = M_bar(<r) * (nu(y)-1)
Deep MOND: M_eff -> sqrt(a0 M_bar / G) * r  (isothermal-like), scaling ~ sqrt(M_bar).

This script computes the target exactly, both footings:
  (1) rho_eff, M_eff for point mass and exponential disc (Rd=3 kpc), M_bar=1e11 Msun;
      positivity, isothermal limit, sqrt(M_bar) population scaling.
  (2) external-field cutoff radius and TOTAL integrated M_eff per galaxy vs the
      cosmic Omega_dm/Omega_b budget (global consistency of ANY source mechanism).
  (3) Solar system: naked (unscreened) M_eff inside Saturn's orbit vs the
      Pitjev & Pitjeva (2013) ephemeris bound on unmodeled mass (~7.9e-11 Msun).

exit 0 on success; every check asserted.
"""
import numpy as np

# ---------- constants (SI) ----------
G     = 6.674e-11          # m^3 kg^-1 s^-2
Msun  = 1.989e30           # kg
kpc   = 3.0857e19          # m
AU    = 1.4960e11          # m

A0_CANON = 9.36e-11        # m/s^2  (cH_Lambda / Z, canonical)
A0_ALT   = 1.13e-10        # m/s^2  (rho_total / cH0 footing)
FOOTINGS = [("canonical a0=9.36e-11", A0_CANON), ("alt a0=1.13e-10", A0_ALT)]

# Planck-2018-ish budget
OMEGA_DM, OMEGA_B = 0.2607, 0.0490
DM_TO_B = OMEGA_DM / OMEGA_B   # ~5.32

def nu_of_y(y):
    """framework interpolation nu(y) = sqrt(1+1/y)"""
    return np.sqrt(1.0 + 1.0/y)

def g_bar_point(r, Mb):
    return G*Mb/r**2

def Menc_expdisc(r, Mb, Rd):
    """Spherically-averaged enclosed mass of an exponential profile
    (exact for a spherical exponential; ~10-20% approximation for a thin disc --
    fine for a target calculation, caveat noted)."""
    x = r/Rd
    return Mb*(1.0 - (1.0 + x + 0.5*x**2)*np.exp(-x))  # spherical exp: rho ~ e^{-r/Rd}
    # NOTE: for the razor-thin disc the enclosed-mass form is
    # M(1-(1+x)e^{-x}); we carry the spherical form and check sensitivity below.

def Menc_disc_thin(r, Mb, Rd):
    x = r/Rd
    return Mb*(1.0 - (1.0 + x)*np.exp(-x))

def M_eff(r, Menc, a0):
    gb = G*Menc/r**2
    y  = gb/a0
    return Menc*(nu_of_y(y) - 1.0)

def rho_eff(rgrid, Menc_fn, Mb, a0):
    """rho_eff = (1/4piG) (1/r^2) d/dr [ r^2 (nu-1) g_bar ]  = (1/4pi r^2) dM_eff/dr / ... """
    Menc = Menc_fn(rgrid, Mb)
    Me   = M_eff(rgrid, Menc, a0)
    dMe  = np.gradient(Me, rgrid)
    return dMe/(4.0*np.pi*rgrid**2)

print("="*100)
print("LANE 0 -- THE TARGET: rho_eff(r) = (1/4piG) div[(nu-1) g_bar],  M_eff = M_bar(<r)*(nu-1)")
print("="*100)

R_LIST_KPC = [5, 10, 20, 50, 100, 300]
MB11 = 1e11*Msun
RD   = 3.0*kpc

for label, a0 in FOOTINGS:
    print(f"\n----- FOOTING: {label} -----")
    Miso_per_m = np.sqrt(a0*MB11/G)          # kg per meter, deep-MOND slope
    print(f"deep-MOND isothermal slope sqrt(a0 M/G) = {Miso_per_m:.3e} kg/m "
          f"= {Miso_per_m*kpc/Msun:.3e} Msun/kpc")
    hdr = f"{'r[kpc]':>7} | {'POINT: M_eff[Msun]':>19} {'rho_eff[kg/m^3]':>16} {'Msun/pc^3':>10} | {'DISC: M_eff[Msun]':>18} {'rho_eff[kg/m^3]':>16} | {'iso-limit ratio':>15}"
    print(hdr); print("-"*len(hdr))
    for rk in R_LIST_KPC:
        r = rk*kpc
        # point mass
        gb = g_bar_point(r, MB11); y = gb/a0
        Me_pt = MB11*(nu_of_y(y)-1.0)
        # analytic rho_eff for point mass via fine local grid
        rr = r*np.exp(np.linspace(-1e-3, 1e-3, 5))
        Mes = MB11*(nu_of_y(g_bar_point(rr, MB11)/a0)-1.0)
        rho_pt = np.gradient(Mes, rr)[2]/(4*np.pi*r**2)
        # disc
        Menc = Menc_expdisc(r, MB11, RD)
        Me_d = M_eff(r, Menc, a0)
        Mencs = Menc_expdisc(rr, MB11, RD)
        Mes_d = M_eff(rr, Mencs, a0)
        rho_d = np.gradient(Mes_d, rr)[2]/(4*np.pi*r**2)
        iso = Me_pt/(Miso_per_m*r)
        rho_pt_pc3 = rho_pt/(Msun/(3.0857e16)**3)
        print(f"{rk:>7} | {Me_pt/Msun:>19.4e} {rho_pt:>16.4e} {rho_pt_pc3:>10.2e} | {Me_d/Msun:>18.4e} {rho_d:>16.4e} | {iso:>15.4f}")

    # ---- positivity over a wide grid (point + disc, spherical & thin-disc M(<r)) ----
    rg = np.geomspace(0.05*kpc, 3000*kpc, 4000)
    for name, Mfn in [("point", lambda r, Mb: np.full_like(r, Mb)),
                      ("exp-sph", lambda r, Mb: Menc_expdisc(r, Mb, RD)),
                      ("exp-thin", lambda r, Mb: Menc_disc_thin(r, Mb, RD))]:
        Me = M_eff(rg, Mfn(rg, MB11), a0)
        dMe = np.gradient(Me, rg)
        rho = dMe/(4*np.pi*rg**2)
        assert np.all(rho > -1e-40), f"NEGATIVE rho_eff for {name} at {label}"
        print(f"positivity [{name:8s}]: min rho_eff = {rho.min():.3e} kg/m^3  -> POSITIVE everywhere: {bool(np.all(rho>0))}")

    # ---- deep-MOND isothermal limit ----
    r_far = 2000*kpc
    Me_far = MB11*(nu_of_y(g_bar_point(r_far, MB11)/a0)-1.0)
    ratio = Me_far/(Miso_per_m*r_far)
    print(f"isothermal limit @2 Mpc: M_eff/[sqrt(a0 M/G) r] = {ratio:.5f} (->1 = confirmed)")
    assert abs(ratio-1.0) < 0.05

    # ---- population scaling M_eff ~ sqrt(M_bar) ----
    print("population scaling at r=100 kpc (deep-ish MOND):")
    Mlist = [1e9, 1e10, 1e11, 1e12]
    vals = []
    for M in Mlist:
        Mb = M*Msun
        Me = Mb*(nu_of_y(g_bar_point(100*kpc, Mb)/a0)-1.0)
        vals.append(Me)
        print(f"  M_bar={M:.0e} Msun -> M_eff(100kpc)={Me/Msun:.4e} Msun")
    # successive ratios should approach sqrt(10)=3.162 in deep MOND
    ratios = [vals[i+1]/vals[i] for i in range(3)]
    print(f"  successive M_eff ratios per decade of M_bar: {[f'{x:.3f}' for x in ratios]} (sqrt(10)=3.162)")
    assert abs(ratios[0]-np.sqrt(10)) < 0.15*np.sqrt(10)   # low-mass end = cleanly deep-MOND

    # =====================================================================
    # (2) EXTERNAL-FIELD CUTOFF + GLOBAL BUDGET
    # =====================================================================
    print("\n(2) External-field cutoff + global Omega_dm consistency")
    print(f"    cosmic Omega_dm/Omega_b = {DM_TO_B:.2f}")
    for fext in [0.01, 0.03, 0.10]:
        g_ext = fext*a0
        # saturation when the galaxy's own (MOND) field falls below g_ext:
        #   g_obs ~ sqrt(G M a0)/r = g_ext  ->  r_cut = sqrt(G M a0)/g_ext
        r_cut = np.sqrt(G*MB11*a0)/g_ext
        Me_tot = np.sqrt(a0*MB11/G)*r_cut          # = M_bar * a0/g_ext  (M-independent ratio!)
        ratio_b = Me_tot/MB11
        # conservative variant: cutoff where the BARE field = g_ext
        r_cut_bare = np.sqrt(G*MB11/g_ext)
        Me_tot_bare = np.sqrt(a0*MB11/G)*r_cut_bare  # = M_bar*sqrt(a0/g_ext)
        print(f"    g_ext={fext:.2f} a0: r_cut={r_cut/kpc:8.0f} kpc ({r_cut/kpc/1000:.2f} Mpc) "
              f"-> M_eff_tot/M_bar = a0/g_ext = {ratio_b:6.1f}  "
              f"[bare-field cutoff: r={r_cut_bare/kpc:.0f} kpc, ratio sqrt(a0/g_ext)={Me_tot_bare/MB11:.1f}]")
    print("    NOTE: M_eff_tot/M_bar = a0/g_ext is M_bar-INDEPENDENT (population-uniform).")
    print(f"    Match to Omega_dm/Omega_b={DM_TO_B:.1f} requires g_ext = a0/{DM_TO_B:.1f} = "
          f"{a0/DM_TO_B:.2e} m/s^2 = {1/DM_TO_B:.3f} a0.")
    print("    Typical cosmic-web g_ext ~ 0.01-0.03 a0 -> per-galaxy overshoot x6-x19 vs 5.3;")
    print("    BUT only ~10-20% of cosmic baryons sit in galaxies -> the halo-attached target is")
    print("    ~27-53x per galaxy-baryon; overshoot/undershoot is O(1)-contested, NOT a clean kill.")

    # =====================================================================
    # (3) SOLAR SYSTEM: naked M_eff inside Saturn vs ephemeris bound
    # =====================================================================
    print("\n(3) Solar system (Saturn, r=9.58 AU)")
    r_sat = 9.58*AU
    Msun_kg = 1.989e30
    g_sat = G*Msun_kg/r_sat**2
    y = g_sat/a0
    numo = nu_of_y(y) - 1.0            # ~ a0/(2 g)
    Me_sat = Msun_kg*numo
    danom = numo*g_sat                 # anomalous sunward acceleration ~ a0/2
    PITJEV_BOUND_MSUN = 7.9e-11        # Pitjev & Pitjeva 2013, unmodeled mass < Saturn's orbit
    print(f"    g(Saturn) = {g_sat:.3e} m/s^2, y = g/a0 = {y:.3e}")
    print(f"    nu-1 = {numo:.3e}  (a0/2g = {a0/(2*g_sat):.3e})")
    print(f"    NAKED M_eff(<Saturn) = {Me_sat/Msun:.3e} Msun")
    print(f"    ephemeris bound (Pitjev & Pitjeva 2013): {PITJEV_BOUND_MSUN:.1e} Msun")
    print(f"    -> naked source EXCEEDS the bound by {Me_sat/Msun/PITJEV_BOUND_MSUN:.2e} "
          f"= 10^{np.log10(Me_sat/Msun/PITJEV_BOUND_MSUN):.2f}")
    print(f"    equivalent anomalous acceleration = (nu-1)g = {danom:.3e} m/s^2 (-> a0/2 = {a0/2:.3e}, CONSTANT tail)")
    print("    => ephemeris-safe ONLY if the mechanism is screened by the same nu-saturation")
    print("       (i.e., the source must switch off at g >> a0 FASTER than the framework's")
    print("       power-law tail nu-1 ~ a0/2g, or the MI response must not gravitate there).")
    assert Me_sat/Msun > 1e3*PITJEV_BOUND_MSUN   # the tension is real, both footings

print("\n" + "="*100)
print("LANE 0 SUMMARY")
print("="*100)
print("""
TARGET CONFIRMED (both footings):
  * rho_eff > 0 everywhere (point, spherical-exp, thin-disc M(<r)) -- a physical source is possible.
  * deep-MOND: M_eff -> sqrt(a0 M_bar/G) * r exactly (isothermal); rho_eff ~ 1/r^2.
  * population scaling M_eff ~ sqrt(M_bar) per decade (3.16x) -- kills ANY fixed-amount mechanism.
  * M_eff(100 kpc; 1e11 Msun) = 7.25e11 Msun (canonical), 8.06e11 (alt): the required
    'phantom' mass EQUALS M_bar already at ~21 kpc (nu=2 radius, r=sqrt(3GM/a0)) and
    grows ~linearly outward -- a big, extended, galaxy-anchored source is mandatory.
  * EFE cutoff at ~1-4 Mpc (g_ext=0.01-0.03 a0); TOTAL M_eff/M_bar = a0/g_ext, mass-independent;
    global budget lands within ~x2-x6 of Omega_dm/Omega_b once the galaxy baryon fraction is
    counted -- an O(1)-honest budget, neither clean pass nor clean kill.
  * Solar system: the NAKED target source inside Saturn = 6-9e-7 Msun vs ephemeris ~8e-11 Msun
    -> over by ~3.9-4.0 ORDERS; and the framework nu has a CONSTANT a0/2 ~ 4.7e-11 m/s^2
    acceleration tail. ANY viable source mechanism MUST inherit nu's high-g screening AND
    beat the a0/2 tail (a known marginal zone for simple-nu families).
""")
print("EXIT 0")
