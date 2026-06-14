#!/usr/bin/env python3
"""
ROUTE 3 [efe_value]: pin the Milky-Way external field g_ext + its uncertainty, propagate
to gamma_cap, and feed the framework-vs-MOND-vs-Newton DR4 forecast.

The EFE caps gamma. g_ext is the single most load-bearing input. We:
  (1) compute g_ext = V_c^2/R0 (radial centripetal) with current best V_c, R0 + uncertainties;
  (2) add the VERTICAL galactic field (Chae's g_0/3 in quadrature) -> the TOTAL effective field;
  (3) propagate (V_c, R0, vertical) -> sigma(g_ext) -> sigma(g_ext/a0) -> sigma(gamma_cap);
  (4) compare that gamma smear to the framework-vs-MOND gap (the discriminator test).
C. Zimmerman machinery / Opus 4.8 Route 3, 2026-06-14. numpy only.
"""
import numpy as np
rng = np.random.default_rng(20260614)

# ---- constants ----
kpc = 3.0857e19  # m
a0_fw, a0_MOND = 9.36e-11, 1.20e-10

# ---- AQUAL anisotropic EFE machinery (mu-form, the rigorous tensor; banked WB_EFE_DERIVATION) ----
# simple mu(x)=x/(1+x); the function Chae/AQUAL fits actually use.
def mu_simple(x):  return x/(1.0+x)
def Lmu_simple(x): return 1.0/(1.0+x)          # d ln mu/d ln x for simple mu = 1/(1+x)
# standard mu(x)=x/sqrt(1+x^2) (the framework's DSSYK-sharp interp)
def mu_std(x):  return x/np.sqrt(1.0+x*x)
def Lmu_std(x): return 1.0/(1.0+x*x)

def gamma_cap_muform(e, which='simple'):
    """Angle-averaged anisotropic AQUAL EFE cap: gamma = (1/3)Gpar/G + (2/3)Gperp/G.
       Gpar/G = 1/[mu(e)(1+Lmu)], Gperp/G = 1/mu(e).   e = g_ext/a0, deep-internal limit."""
    if which=='simple': mu, L = mu_simple(e), Lmu_simple(e)
    else:               mu, L = mu_std(e),    Lmu_std(e)
    Gpar  = 1.0/(mu*(1.0+L))
    Gperp = 1.0/mu
    return (1.0/3.0)*Gpar + (2.0/3.0)*Gperp

print("="*94)
print("STEP 1 — g_ext = V_c(R0)^2 / R0  (radial centripetal field at the solar circle)")
print("="*94)
# current best inputs, with literature spread:
#   R0  = 8.178 +/- 0.013(stat) +/- 0.022(sys) kpc  (GRAVITY 2019, S2 orbit)  -> ~8.178 +/- 0.026
#   V_c at R0: Eilers+2019 229 (formal 0.2, syst ~few); Ou+2024 ~236; GRAVITY-LSR 233 +/- 3
#   -> central V_c = 233 +/- 3, but the FULL literature span is ~229-236 km/s.
R0_c, R0_s   = 8.178*kpc, 0.026*kpc
Vc_c, Vc_s   = 233e3,   4e3       # central 233, sigma 4 km/s (covers 229-236 span at ~1sigma)

g_ext_radial = Vc_c**2 / R0_c
print(f"  V_c(R0) = {Vc_c/1e3:.0f} +/- {Vc_s/1e3:.0f} km/s   (Eilers229 / GRAVITY-LSR233 / Ou236 span)")
print(f"  R0      = {R0_c/kpc:.3f} +/- {R0_s/kpc:.3f} kpc   (GRAVITY 2019, 0.3%)")
print(f"  g_ext(radial) = V_c^2/R0 = {g_ext_radial:.3e} m/s^2")
print(f"                = {g_ext_radial/a0_fw:.3f} a0_fw  = {g_ext_radial/a0_MOND:.3f} a0_MOND")

print("\n" + "="*94)
print("STEP 2 — the VERTICAL field: is the relevant EFE the radial V_c^2/R0, or the TOTAL?")
print("="*94)
# Chae (2023, 2024) uses the TOTAL effective external field, adding the vertical disk field
# g_z in quadrature.  Near the plane the vertical field at ~ the WB scale-height is ~ g_radial/3
# (Chae's adopted "vertical gravity of g0/3"). The EFE magnitude is |g_ext_vec|:
#   g_total = sqrt(g_radial^2 + g_vert^2),  g_vert ~ g_radial/3
# This RAISES g_ext above the bare radial value -> Chae's 2.26e-10 (= 1.9 a0_MOND).
g_vert = g_ext_radial/3.0
g_ext_total = np.sqrt(g_ext_radial**2 + g_vert**2)
print(f"  Chae adopts a vertical field g_z ~ g_radial/3 added in quadrature (his published prescription).")
print(f"  g_vert ~ g_radial/3 = {g_vert:.3e}")
print(f"  g_ext(total) = sqrt(g_rad^2 + g_vert^2) = {g_ext_total:.3e} m/s^2")
print(f"               = {g_ext_total/a0_fw:.3f} a0_fw  = {g_ext_total/a0_MOND:.3f} a0_MOND")
print(f"  -> matches Chae's published g_ext ~ 2.26e-10 (= 1.9 a0_MOND): {g_ext_total:.3e} vs 2.26e-10")
print(f"  The vertical term raises g_ext by {100*(g_ext_total/g_ext_radial-1):.1f}% over bare radial.")
print(f"  DIRECTION NOTE: a LARGER g_ext (the total) Newtonizes MORE -> LOWERS gamma_cap.")
print(f"  The framework's lower a0 + the (larger) total field => e is at its highest -> smallest boost.")

print("\n" + "="*94)
print("STEP 3 — e = g_ext/a0 on each footing, both the bare-radial and total-field choices")
print("="*94)
for label, gext in [("bare radial V_c^2/R0", g_ext_radial), ("TOTAL (Chae, +vertical)", g_ext_total)]:
    e_fw, e_M = gext/a0_fw, gext/a0_MOND
    print(f"\n  {label}:  g_ext={gext:.3e}")
    for which in ('simple','standard'):
        gfw = gamma_cap_muform(e_fw, which)
        gM  = gamma_cap_muform(e_M,  which)
        print(f"    {which:>9s}-mu:  e_fw={e_fw:.3f} -> gamma_cap={gfw:.3f} | "
              f"e_MOND={e_M:.3f} -> gamma_cap={gM:.3f}  | gap(MOND-fw)={gM-gfw:+.3f}")


print("\n" + "="*94)
print("STEP 4 — MONTE-CARLO: propagate (V_c, R0, vertical-fraction) -> sigma(gamma_cap)")
print("="*94)
N = 400000
Vc  = rng.normal(Vc_c, Vc_s, N)
R0  = rng.normal(R0_c, R0_s, N)
# vertical-field fraction f_z: Chae's g_z/g_rad ~ 1/3, but it depends on the WB scale height /
# tracer population. Treat f_z ~ U(0.2, 0.45) (Chae 1/3 central; 0 = pure-radial, ~0.45 = thicker).
fz  = rng.uniform(0.20, 0.45, N)
g_rad_mc = Vc**2 / R0
g_ext_mc = g_rad_mc * np.sqrt(1.0 + fz**2)

for which in ('simple','standard'):
    print(f"\n  --- {which}-mu interpolation ---")
    for footing, a0 in [("framework 9.36e-11", a0_fw), ("MOND 1.20e-10", a0_MOND)]:
        e_mc = g_ext_mc / a0
        g_mc = np.array([gamma_cap_muform(ee, which) for ee in e_mc[:60000]])  # subsample for speed
        med = np.median(g_mc); lo,hi = np.percentile(g_mc,[16,84])
        print(f"    {footing}:  gamma_cap = {med:.3f}  [16-84: {lo:.3f}, {hi:.3f}]  "
              f"sigma_gamma(g_ext)= {(hi-lo)/2:.4f}")

# Now: head-to-head smear vs the framework-MOND gap, simple-mu (the live discriminator interp)
print("\n  ----- THE DECISIVE COMPARISON (simple-mu, the discriminating interp) -----")
e_fw_mc, e_M_mc = g_ext_mc/a0_fw, g_ext_mc/a0_MOND
sub = slice(0,60000)
g_fw = np.array([gamma_cap_muform(ee,'simple') for ee in e_fw_mc[sub]])
g_M  = np.array([gamma_cap_muform(ee,'simple') for ee in e_M_mc[sub]])
gfw_med, gfw_sig = np.median(g_fw), (np.percentile(g_fw,84)-np.percentile(g_fw,16))/2
gM_med,  gM_sig  = np.median(g_M),  (np.percentile(g_M,84)-np.percentile(g_M,16))/2
gap = gM_med - gfw_med
print(f"    framework gamma_cap = {gfw_med:.3f} +/- {gfw_sig:.3f} (g_ext systematic only)")
print(f"    MOND      gamma_cap = {gM_med:.3f} +/- {gM_sig:.3f}")
print(f"    framework-vs-MOND GAP = {gap:.3f}")
print(f"    g_ext smear / gap = {gfw_sig/gap:.2f}  (BOTH a0 share g_ext, so the SHARED smear is")
print(f"      largely COMMON-MODE: it moves fw and MOND TOGETHER, not apart)")
# common-mode check: difference gamma_M - gamma_fw per-draw
dgap = g_M - g_fw
print(f"    per-draw (gamma_MOND - gamma_fw): mean={np.mean(dgap):.3f}  std={np.std(dgap):.4f}  "
      f"(the IRREDUCIBLE part of the gap after g_ext common-mode cancels)")
print(f"    => g_ext uncertainty smears the gap by only +/-{np.std(dgap):.3f} on a {np.mean(dgap):.3f} gap.")

print("\n" + "="*94)
print("STEP 5 — does g_ext uncertainty ALONE smear gamma past the framework-MOND gap?  (the route's both-ways question)")
print("="*94)
print(f"""  framework-MOND gap (simple-mu): {gap:.3f}
  g_ext-induced 1-sigma on framework gamma_cap (V_c,R0,vert): {gfw_sig:.3f}
  ABSOLUTE ratio sigma/gap = {gfw_sig/gap:.2f}  -> if read as independent, g_ext alone ~ {gfw_sig/gap:.1f}x the gap.
  BUT g_ext is COMMON-MODE (same field enters both footings). The gap's irreducible scatter
  from g_ext is only +/-{np.std(dgap):.3f} (={100*np.std(dgap)/np.mean(dgap):.0f}% of the gap). So g_ext does NOT
  by itself wash out framework-vs-MOND; the a0 difference is the gap, g_ext shifts BOTH ends.
  The dominant systematic for the gap is the INTERPOLATION FUNCTION (simple gap {gap:.3f} vs standard gap ~0.03),
  NOT g_ext.""")
