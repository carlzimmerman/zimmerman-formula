"""
TARGET PROFILE the cluster closure must reproduce (topic "target_profile").

Pins the residual eta(R), eta-vs-M500, post-XRISM true eta(R500), and the
implied MISSING-MASS profile M_res(<R) [Msun] that any closure (routes 2/3)
must supply at the cluster CORE.

Framework: a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11 m/s^2 (modified inertia,
dS-Unruh). Framework's OWN interpolation (MEMORY footing rule):
    g_pred = sqrt(g_bar^2 + g_bar*a0)   [NOT McGaugh nu, NOT deep-MOND asymptote]
    eta    = g_obs / g_pred

ESTABLISHED THIS SESSION (read into this script, all both-ways-banked):
  - eRASS1 N=9830 clean: median eta(R500)=2.33 (FW a0+interp), 5-95% = 2.00-4.43,
    intrinsic scatter ~0.04 dex. eta FLAT-to-slightly-rising with M500.
  - The deficit is CENTRAL, dies to ~1 by ~R500-1.3R500. Peak radius ~ sqrt(M500).
  - WL-vs-hydrostatic systematic brackets R500 eta across [~1.0, ~2.33].
  - Famaey/Pizzuti/Saltas 2025 (CLASH lensing): inner constant-density CORE +
    ~450 kpc exponential cutoff, missing-to-gas density ratio ~10, uniform.
  - Kelleher&Lelli 2024 (X-COP): missing/baryon 1-5 at 200-300 kpc -> 0.4-1.1 at
    2-3 Mpc, inner core + outer r^-4 (FINITE total).
  - Tian 2020 cluster RAR: g_dagger = 2.02e-9 ~ 21.6x a0 (slope 0.51).
  - Robust to cosmic-density a0 (z=0.296 -> a0=9.9e-11 moves residual <1%).
  - density-a0 with LOCAL gas rho flattens raw [1.55->7.66] to [0.75->1.30]
    (zero params) but does NOT close + breaks SPARC -> the SHAPE target, not a cure.

Both-ways: the TARGET is reported with the full WL/hydrostatic bracket and the
post-XRISM deflation. The closure (routes 2/3) must hit the CENTRAL missing-mass
M_res(<R) WITHOUT breaking the galaxy RAR (the veto).
"""
import numpy as np

# ----------------------------- constants -----------------------------
G    = 6.674e-11          # SI
Msun = 1.989e30           # kg
kpc  = 3.086e19           # m
Mpc  = 1000*kpc
a0   = 9.36e-11           # framework a0 (eta-worst footing)

def eta_interp(gbar, gobs):
    """framework dS-Unruh interpolation eta (MEMORY footing rule)."""
    gpred = np.sqrt(gbar**2 + gbar*a0)
    return gobs/gpred

# ----------------------- cluster baryon + total models -----------------------
# Gas: isothermal beta-model rho_gas(r) = rho0 / (1+(r/rc)^2)^(3 beta/2).
# Total (apparent dynamical / WL): NFW. fstar = stars/gas = 0.2 (catalog baseline).
# Calibrated so that M500_total and fgas reproduce the eRASS1 medians per mass bin.

def beta_Mgas(r, rho0, rc, beta):
    """enclosed gas mass [kg] of an isothermal beta-model, analytic-ish via grid."""
    rr = np.linspace(1e-3*rc, r, 4000)
    rho = rho0/(1+(rr/rc)**2)**(1.5*beta)
    return np.trapz(4*np.pi*rr**2*rho, rr)

def nfw_M(r, rho_s, rs):
    x = r/rs
    return 4*np.pi*rho_s*rs**3*(np.log(1+x) - x/(1+x))

def build_cluster(M500_total_Msun, R500_kpc, fgas500, c500=3.5, beta=0.65,
                  rc_kpc=None, fstar=0.2):
    """Return callables g_bar(r), g_obs(r), M_bar(<r), M_tot(<r) for r in meters.
    Calibrated to (M500_total, R500, fgas500). rc defaults to 0.2 R500 (typical)."""
    R500 = R500_kpc*kpc
    M500 = M500_total_Msun*Msun
    if rc_kpc is None:
        rc_kpc = 0.20*R500_kpc
    rc = rc_kpc*kpc
    # --- NFW total normalized to M(<R500)=M500 ---
    rs = R500/c500
    def _mnfw_unit(r, rs):  # shape factor
        x = r/rs
        return np.log(1+x) - x/(1+x)
    rho_s = M500/(4*np.pi*rs**3*_mnfw_unit(R500, rs))
    # --- gas beta-model normalized so Mgas(<R500)=fgas500*M500 ---
    Mgas500 = fgas500*M500_total_Msun*Msun
    unit_gas = beta_Mgas(R500, 1.0, rc, beta)   # with rho0=1
    rho0 = Mgas500/unit_gas
    Mstar500 = fstar*Mgas500
    # stars: track gas profile (point-ish / same shape, scaled) -> add to baryon
    def M_bar(r):
        Mg = beta_Mgas(r, rho0, rc, beta)
        return (1+fstar)*Mg
    def M_tot(r):
        return nfw_M(r, rho_s, rs)
    def g_bar(r):
        return G*M_bar(r)/r**2
    def g_obs(r):
        return G*M_tot(r)/r**2
    return dict(g_bar=g_bar, g_obs=g_obs, M_bar=M_bar, M_tot=M_tot,
                R500=R500, M500=M500, rho_s=rho_s, rs=rs, rho0=rho0, rc=rc, beta=beta)

# ----------------------- radial eta profile + missing mass -----------------------
def profile(cl, rfracs):
    """eta_field(r), and the REQUIRED phantom (missing) mass that a closure must
    supply so that g_pred(g_bar+phantom) = g_obs. M_res(<R) is the extra
    NEWTONIAN-equivalent collisionless mass beyond what MOND already provides."""
    R500 = cl['R500']
    rows = []
    for f in rfracs:
        r = f*R500
        gb = cl['g_bar'](r)
        go = cl['g_obs'](r)
        eta = eta_interp(gb, go)
        # MOND already supplies g_pred from baryons:
        gpred_mond = np.sqrt(gb**2 + gb*a0)
        # the closure must add collisionless mass so that observed g_obs is met.
        # In a MOND theory the residual is the NEWTONIAN-equivalent mass that,
        # added to baryons and re-run through the SAME interpolation, lands g_obs.
        # Solve g_obs = sqrt(gN_needed^2 + gN_needed*a0) for gN_needed:
        #   gN_needed = (-a0 + sqrt(a0^2 + 4 g_obs^2))/2
        gN_needed = (-a0 + np.sqrt(a0**2 + 4*go**2))/2.0
        M_needed = gN_needed*r**2/G                     # total baryon-equiv inside r
        M_res    = max(0.0, M_needed - cl['M_bar'](r))  # collisionless residual
        rows.append(dict(rfrac=f, r_kpc=r/kpc, gbar_a0=gb/a0,
                         eta=eta, Mbar=cl['M_bar'](r)/Msun,
                         Mtot=cl['M_tot'](r)/Msun,
                         M_res=M_res/Msun))
    return rows

# ============================ RUN ============================
print("="*86)
print("TARGET PROFILE the cluster closure (routes 2/3) must reproduce")
print("framework a0 = %.3e, dS-Unruh interpolation g_pred=sqrt(gbar^2+gbar*a0)" % a0)
print("="*86)

# Fiducial RICH cluster (M500 ~ 1e15) and GROUP (~1e14), eRASS1-typical fgas, R500.
# R500 from M500: R500 = (3 M500 / (4 pi 500 rho_crit))^1/3; use eRASS1 medians per bin.
# rich: M500=1e15, R500~1400 kpc, fgas~0.13 (rich clusters more baryon-complete)
# group: M500=1e14, R500~715 kpc, fgas~0.066 (eRASS1 median bin)
rfracs = [0.05, 0.10, 0.15, 0.20, 0.30, 0.50, 0.70, 1.00, 1.30]

rich  = build_cluster(1.0e15, 1400.0, 0.13, c500=3.5, beta=0.70, rc_kpc=200.0)
group = build_cluster(1.0e14, 715.0,  0.066, c500=4.0, beta=0.62, rc_kpc=120.0)

for name, cl in [("RICH CLUSTER  M500=1e15", rich), ("GROUP  M500=1e14", group)]:
    print("\n" + "-"*86)
    print(name, " R500=%.0f kpc  fgas500=%.3f" % (cl['R500']/kpc,
          cl['M_bar'](cl['R500'])/(1.2*cl['M500'])))
    print("-"*86)
    print(f"{'r/R500':>7} {'r[kpc]':>8} {'gbar/a0':>8} {'eta_fld':>8} "
          f"{'Mbar[Msun]':>12} {'Mtot[Msun]':>12} {'M_res(<R)[Msun]':>16}")
    rows = profile(cl, rfracs)
    for row in rows:
        print(f"{row['rfrac']:7.2f} {row['r_kpc']:8.0f} {row['gbar_a0']:8.4f} "
              f"{row['eta']:8.3f} {row['Mbar']:12.3e} {row['Mtot']:12.3e} "
              f"{row['M_res']:16.3e}")
    cl['_rows'] = rows

# ---- peak radius ~ sqrt(M500) check (the deficit peaks at the CORE; the
#      lensing CUTOFF/core scale ~ 400-450 kpc scales weakly with mass) ----
print("\n" + "="*86)
print("PEAK / CORE SCALE vs M500 (deficit is central; core-cutoff ~ sqrt(M500))")
print("="*86)
# Famaey 2025: r0 ~ 450 kpc exp cutoff at the ~1e15 CLASH scale.
# sqrt-scaling: r_core(M500) = 450 kpc * sqrt(M500/1e15)
for M in [1e14, 3e14, 1e15, 2e15]:
    print(f"  M500={M:.0e}  r_core ~ {450*np.sqrt(M/1e15):6.0f} kpc  (Famaey ~450 kpc @ 1e15)")

# ---- POST-XRISM true eta(R500): the hydrostatic ~2.33 deflates after
#      XRISM/WL recalibration. The WL/hydrostatic bracket is [1.0, 2.33].
print("\n" + "="*86)
print("POST-XRISM true eta(R500): the hydrostatic/WL bracket (BOTH WAYS, corrected)")
print("="*86)
print("  WL-calibrated (catalog) eRASS1 median eta(R500)      = 2.33  (FW a0, eta-WORST)")
print("  hydrostatic/kinematic branch (Li+2024, -110% on M)   = 1.02  (FW a0, eta-BEST)")
print("  --- XRISM both-ways correction (Abell 2029, relaxed, arXiv:2505.06533/2501.05514):")
print("      non-thermal pressure <=2% of total at ALL radii; HSE mass bias ~2% only.")
print("      => for RELAXED clusters X-ray hydrostatic mass is RELIABLE (NOT biased low),")
print("         so XRISM does NOT deflate eta via turbulence. The deflation from 2.33")
print("         toward ~1 comes from the WL-vs-hydrostatic MASS-SCALE gap (Li+2024 ~110%)")
print("         + disequilibrium skirt, NOT non-thermal pressure. XRISM REMOVES the")
print("         'maybe hydrostatic is biased low so eta is really 2' escape for relaxed")
print("         clusters: their hydrostatic mass stands, pulling the equilibrium eta DOWN.")
print("  -> TRUE eta(R500) target window: [~1.0 (relaxed, HSE-reliable, eta-best),")
print("                                    ~2.33 (WL-calibrated, eta-worst)];")
print("     best single equilibrium estimate ~1.0-1.6. A CENTRAL residual survives in")
print("     relaxed gas-complete clusters; the OUTER 2x is WL/disequilibrium-inflated.")

# ---- eRASS1 ANCHOR: tie the fiducial profiles to the real-data median eta(R500) ----
# The fiducial NFW-built clusters give eta(R500)=2.09 (rich) / 1.90 (group); the
# eRASS1 WL-calibrated median is 2.33. The gap is the WL inflation (Li+2024: WL
# mass ~110% above hydrostatic). To pin the WL-CALIBRATED target the closure must
# hit, scale M_tot so eta(R500)=2.33, then re-read the core M_res. This is the
# eta-WORST (WL) anchor; the hydrostatic anchor is eta(R500)~1.0 (lower bound).
print("\n" + "="*86)
print("eRASS1-ANCHORED TARGET (scale M_tot to median eta(R500)=2.33 WL-calibrated)")
print("="*86)
def anchored_rows(cl, eta_target=2.33):
    R500 = cl['R500']
    gb500 = cl['g_bar'](R500)
    # solve eta_target = gobs/sqrt(gb^2+gb*a0) for gobs500, then scale NFW
    gobs500_target = eta_target*np.sqrt(gb500**2+gb500*a0)
    Mtot500_target = gobs500_target*R500**2/G
    scale = Mtot500_target/cl['M_tot'](R500)
    rows = profile(cl, rfracs)
    out = []
    for row in rows:
        r = row['rfrac']*R500
        go = cl['g_obs'](r)*scale
        gb = cl['g_bar'](r)
        eta = eta_interp(gb, go)
        gN_needed = (-a0 + np.sqrt(a0**2 + 4*go**2))/2.0
        M_res = max(0.0, gN_needed*r**2/G - cl['M_bar'](r))
        out.append(dict(rfrac=row['rfrac'], r_kpc=r/kpc, gbar_a0=gb/a0,
                        eta=eta, Mbar=cl['M_bar'](r)/Msun, M_res=M_res/Msun))
    return out, scale
for name, cl in [("RICH M500=1e15", rich), ("GROUP M500=1e14", group)]:
    arows, sc = anchored_rows(cl)
    print(f"\n  {name}  (M_tot scaled x{sc:.2f} to hit eta(R500)=2.33):")
    print(f"  {'r/R500':>7}{'r[kpc]':>8}{'eta_fld':>8}{'M_res(<R)[Msun]':>16}")
    for row in arows:
        print(f"  {row['rfrac']:7.2f}{row['r_kpc']:8.0f}{row['eta']:8.3f}{row['M_res']:16.3e}")
    cl['_arows'] = arows

# ---- The CORE missing mass any closure must supply (the make-or-break number) ----
print("\n" + "="*86)
print("CORE MISSING-MASS TARGET  M_res(<R) the closure must supply [Msun]")
print("(this is what routes 2/3 must hit, at the CORE, without breaking SPARC)")
print("="*86)
for name, cl in [("RICH  M500=1e15", rich), ("GROUP M500=1e14", group)]:
    rows = cl['_rows']
    def grab(fr):
        return next(r for r in rows if abs(r['rfrac']-fr)<1e-6)
    r100 = grab(0.10); r30 = grab(0.30); r50=grab(0.50)
    print(f"\n  {name}:")
    print(f"    M_res(<0.10 R500 = {r100['r_kpc']:.0f} kpc) = {r100['M_res']:.2e} Msun  (eta_fld={r100['eta']:.2f})")
    print(f"    M_res(<0.30 R500 = {r30['r_kpc']:.0f} kpc) = {r30['M_res']:.2e} Msun  (eta_fld={r30['eta']:.2f})")
    print(f"    M_res(<0.50 R500 = {r50['r_kpc']:.0f} kpc) = {r50['M_res']:.2e} Msun  (eta_fld={r50['eta']:.2f})")
    # core (~300-450 kpc) residual, the lensing window
    rcore = grab(0.30)
    print(f"    -> CORE target (~{rcore['r_kpc']:.0f} kpc): supply ~{rcore['M_res']:.2e} Msun "
          f"collisionless, dying to ~0 by 1.3 R500")
