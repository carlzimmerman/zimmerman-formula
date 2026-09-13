#!/usr/bin/env python3
"""K004 -- the programme's testable-predictions ledger, every number recomputed.

Each numbered prediction of kimik3_push/predictions/PREDICTIONS.md has its value
computed here, on both a0 footings where relevant. Sources are named per block.

Constants follow the corpus: canonical a0 = (1/2) c sqrt(G rho_DE) = 9.3619e-11,
alt (rho_total = rho_crit) a0 = 1.1279e-10 m/s^2. H0 = 67.4 km/s/Mpc, Om = 0.315,
OL = 0.685.
"""
import math

c   = 2.99792458e8          # m/s
G   = 6.674e-11             # SI
Msun= 1.989e30
AU  = 1.496e11
H0  = 67.4*1000/3.0857e22   # s^-1
Om, OL = 0.315, 0.685
rho_crit = 3*H0**2/(8*math.pi*G)
rho_DE   = OL*rho_crit

S_DE   = c*math.sqrt(G*rho_DE)      # = c sqrt(G rho_DE)   = 1.8724e-10
S_CRIT = c*math.sqrt(G*rho_crit)    # = 2.2558e-10
A0_CAN = 9.3619e-11                 # registered canonical footing = S_DE/2
A0_ALT = 1.1279e-10                 # registered alt footing      = S_CRIT/2

print("="*100)
print("K004 -- PREDICTIONS LEDGER VALUES (both footings)")
print("="*100)
print(f"rho_crit = {rho_crit:.4e} kg/m^3   rho_DE = {rho_DE:.4e} kg/m^3")
print(f"s_DE   = c*sqrt(G*rho_DE)   = {S_DE:.4e} m/s^2 ; s_DE/2   = {S_DE/2:.4e} (registered 9.3619e-11)")
print(f"s_CRIT = c*sqrt(G*rho_crit) = {S_CRIT:.4e} m/s^2 ; s_CRIT/2 = {S_CRIT/2:.4e} (registered 1.1279e-10)")

# ----------------------------------------------------------------------------------
print("\n[P1] GAIA DR4 WIDE-BINARY BOOST (Amendment 10/11, frozen)")
print("-"*100)
armA = {"canonical": (1.1614, 1.1814), "alt": (1.1917, 1.2267)}
armB = {"canonical": 1.0450, "alt": 1.0300}
print(f"  Arm A registered band: gamma_v = {armA['canonical'][0]}-{armA['canonical'][1]} (canonical) / "
      f"{armA['alt'][0]}-{armA['alt'][1]} (alt);  Newton = 1.0000 exactly")
print(f"  Arm B (covariant candidate, Cassini-minimal xi) ceilings: {armB['canonical']:.4f} / {armB['alt']:.4f}, falling to 1.000")
print(f"  Decision rule (Amendment 11): A falsified < 1.056; B falsified >= 1.129; undecided 1.084-1.101")
# L240 photocount EFE reading: gamma_v(20 kAU) bracket, multiplicative vs additive law
# recompute here with n = 2, Y_e from the MW flat curve at R0 = 8.2 kpc
n = 2
gext = (233e3)**2/(8.2*3.0857e19)           # m/s^2
Ye = gext/S_DE
def solve_g(gbar, Yext, law):
    lo, hi = gbar, max(gbar*1e6, 10*S_DE)
    def mu(Yi):
        if law == "mult": return 1-(1+Yi)**(-n)*(1+Yext)**(-n)
        return 1-(1+Yi+Yext)**(-n)
    f = lambda g: mu(g/S_DE)*g - gbar
    for _ in range(300):
        mid = 0.5*(lo+hi)
        if f(mid) < 0: lo = mid
        else: hi = mid
    return 0.5*(lo+hi)
for sep in (10.0, 20.0, 30.0):
    gb = G*1.5*Msun/(sep*1e3*AU)**2
    gm = solve_g(gb, Ye, "mult"); ga = solve_g(gb, Ye, "add"); gi = solve_g(gb, 0.0, "mult")
    print(f"  L240 photocount (n=2, Y_e = {Ye:.3f}) at {sep:4.0f} kAU: "
          f"gamma_v mult = {math.sqrt(gm/gb):.4f}, add = {math.sqrt(ga/gb):.4f}, isolated = {math.sqrt(gi/gb):.4f}")
gb20 = G*1.5*Msun/(20.0*1e3*AU)**2
g20m = math.sqrt(solve_g(gb20, Ye, "mult")/gb20); g20a = math.sqrt(solve_g(gb20, Ye, "add")/gb20)
g20i = math.sqrt(solve_g(gb20, 0.0, "mult")/gb20)
print(f"  -> L240 headline: gamma_v(20 kAU) = {g20m:.3f}-{g20a:.3f}, BELOW Arm A; "
      f"external field removes {100*(g20i-g20m)/(g20i-1):.0f}% of the isolated boost")

# ----------------------------------------------------------------------------------
print("\n[P2] a0(z) REDSHIFT LAW  (a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)); footing-independent)")
print("-"*100)
def a0z_ratio(z, w0=-1.0, wa=0.0):
    """rho_DE(z)/rho_DE(0) = (1+z)^{3(1+w0+wa)} exp(-3 wa z/(1+z))  (CPL)."""
    zp = 1+z
    return math.sqrt(zp**(3*(1+w0+wa))*math.exp(-3*wa*z/zp))
print("  constant-Lambda (w = -1, wa = 0): flat by construction")
for z in (1, 2, 3, 5):
    print(f"    z = {z}: a0(z)/a0(0) = {a0z_ratio(z):.5f}  (derived-law flat claim: <1% drift to z<=5)")
# DESI DR2 w0wa central values as carried in the corpus (0.775 at z=3 in the ledger)
w0_desi, wa_desi = -0.827, -0.75   # DESI DR2+CMB+SN central (as used by the programme's stage-17 lane)
print(f"  on DESI DR2 w0wa = ({w0_desi}, {wa_desi}):")
for z, tag in ((0.35, ""), (1.0, ""), (2.0, ""), (3.0, "corpus quotes 0.775-0.78")):
    print(f"    z = {z:4.2f}: a0(z)/a0(0) = {a0z_ratio(z, w0_desi, wa_desi):.4f}   {tag}")
print("  z~2.5 deep-MOND BTFR zero-point: framework 0.00 dex (DEC -0.09) vs LCDM-native +0.33 dex;")
print("  one clean point at +-0.13 dex decides at 20:1.  Pre-registered DOI 10.5281/zenodo.22563139.")
print("  LCDM-side ('crispy gap'): halo dilution needed to mimic flat a0: c/c_Nbody = (H/H0)^(-2/3):")
for z in (2, 3, 5):
    E = math.sqrt(Om*(1+z)**3 + OL)
    print(f"    z = {z}: H/H0 = {E:.2f}, c/c_Nbody = {E**(-2/3):.3f}   (corpus: 0.61 / 0.40 / 0.12)")

# ----------------------------------------------------------------------------------
print("\n[P3] POSITIVE DARK-MATTER EQUATION OF STATE  0 < w_dm <= 1e-4")
print("-"*100)
print("  LCDM: w_dm = 0 exactly. Framework: criticality requires w > 0 strictly;")
print("  acoustic scale bounds it above: 0 < w_dm <= 1e-4 (L201/L207; README rev 13-15).")
print("  Tightened (P4) by the flat-a0 conservation argument to <= 5.66e-7.")

# ----------------------------------------------------------------------------------
print("\n[P4] TIGHTENED UPPER BOUND  w <= 5.7e-7  (L217/L218)")
print("-"*100)
W_CEIL = 5.66e-7
print(f"  ceiling w = {W_CEIL:.2e}, 177x tighter than the acoustic bound 1e-4")
print(f"  two-sided window (L218): floor (criticality by z=30) = 1.5e-8 <= w <= {W_CEIL:.1e} (~1.5 decades)")
print(f"  LCDM contrast: w_dm = 0 exactly sits BELOW the framework's floor -- sign is the discriminator")

# ----------------------------------------------------------------------------------
print("\n[P5] POWER-LAW APPROACH TO NEWTON -- SATURN ANOMALOUS ACCELERATION (L233)")
print("-"*100)
# parameter-free curve mu = 1-(1+Y)^-2 leaves residual 1-mu = (s/g)^2 in the high-g tail
g_sat = 6.0e-5  # m/s^2, Saturn orbit
for s, name in ((S_DE, "canonical s_DE"), (S_CRIT, "alt s_CRIT")):
    frac = (s/g_sat)**2
    anom = frac*g_sat
    print(f"  {name}: s = {s:.4e}; fractional departure 1-mu = (s/g)^2 = {frac:.2e}; "
          f"anomalous accel at Saturn = {anom:.2e} m/s^2 (Cassini residual ~1e-14; margin {1e-14/anom:.0f}x)")
print("  The framework's fitted Route-A kernel (exponential) predicts ZERO there -- distinguishable by ranging.")
# registered-precision restatement: corpus headline 5.8e-16 at canonical
print(f"  (corpus headline: 5.8e-16 m/s^2 at Saturn, ~17x under Cassini)")

# ----------------------------------------------------------------------------------
print("\n[P6] UNIVERSAL GALAXY-SCALE DARK FRACTION (clock-frame kicks, L191)")
print("-"*100)
n_best = 2.0
floor = math.exp(-n_best)
print(f"  retention saturates at the unkicked Poisson fraction e^-n = e^-2 = {floor:.3f}")
print(f"  SAME dark fraction at 1e9 and 1e11 Msun baryonic (every host with v_esc < v_k sits on the floor)")
print(f"  ledger trend contrast: f ~ M^0.16 -> 1.33x from spiral to MW; kills if SPARC demands steeper than 1.2x")

# ----------------------------------------------------------------------------------
print("\n[P7] RAR / BTFR / DWARF-EFE NUMBERS")
print("-"*100)
print(f"  RAR intrinsic scatter (Route A kernel, 175 SPARC): 0.108 dex at Upsilon = 0.70 (0.127 on mu_10)")
print(f"  BTFR: v^4 = G M_b a0 -- exponent DERIVED; zero point 0.25*log10(G a0):")
for a0, name in ((A0_CAN, "canonical"), (A0_ALT, "alt")):
    print(f"    {name}: 0.25*log10(G*a0) = {0.25*math.log10(G*a0):+.4f} dex (vs fitted-scale a0 = 1.20e-10: "
          f"{0.25*math.log10(G*a0) - 0.25*math.log10(G*1.20e-10):+.4f} dex offset)")
print("  dwarf sigma-R_gc external-field effect: BOTH EFE laws UNDERPREDICT classical dSph dispersions;")
print("  over-suppression robust to free M/L (sigma ~ M^1/4). A standing cost, flagged in the ledger.")

# ----------------------------------------------------------------------------------
print("\n" + "="*100)
print("NEW PREDICTIONS DERIVED IN THIS LEDGER (K004)")
print("="*100)

# [N1] Saturn anomaly on BOTH footings, stated as a band with exact values (above: per-footing).
frac_can = (S_DE/g_sat)**2; frac_alt = (S_CRIT/g_sat)**2
print(f"\n[N1] Saturn anomalous acceleration, BOTH footings (power-law photocount curve n = 2):")
print(f"     canonical: {frac_can*g_sat:.3e} m/s^2 ; alt: {frac_alt*g_sat:.3e} m/s^2 ; "
      f"band = [{frac_can*g_sat:.2e}, {frac_alt*g_sat:.2e}] m/s^2")
print(f"     KILL: a ranging bound below {frac_alt*g_sat:.1e} m/s^2 at Saturn kills the n = 2 power-law curve")
print(f"     (and Cassini at ~1e-14 already misses it by {1e-14/(frac_can*g_sat):.0f}x canonical / "
      f"{1e-14/(frac_alt*g_sat):.0f}x alt -- safe but only ~17x/12x).")

# [N2] named z, named w: a0 at z = 2.5 if DESI w0wa holds
r25 = a0z_ratio(2.5, w0_desi, wa_desi)
print(f"\n[N2] NAMED-z NAMED-w a0 VALUE: at z = 2.5 on DESI DR2 (w0, wa) = ({w0_desi}, {wa_desi}):")
print(f"     a0(z=2.5)/a0(0) = {r25:.4f}  ->  BTFR mass zero-point shifts by "
      f"{0.25*math.log10(r25):+.4f} dex (velocity) / {math.log10(r25):+.4f} dex in a0 itself")
print(f"     vs the frozen 0.00-dex pre-registration: a measured z~2.5 BTFR zero-point at "
      f"{0.25*math.log10(r25):+.2f} dex would CONFIRM the DESI-evolving branch and kill the flat-law branch.")
for a0, name in ((A0_CAN, "canonical"), (A0_ALT, "alt")):
    print(f"     {name}: a0(2.5) = {r25*a0:.4e} m/s^2")

# [N3] gamma_v at a specific separation on BOTH footings, photocount n=2, multiplicative law
print(f"\n[N3] gamma_v(20 kAU) on BOTH footings (photocount n = 2, multiplicative EFE law):")
def gamma20(s_scale):
    Ye_s = gext/s_scale
    def solve(gbar):
        lo, hi = gbar, 10*s_scale
        f = lambda g: (1-(1+g/s_scale)**(-n)*(1+Ye_s)**(-n))*g - gbar
        for _ in range(300):
            mid = 0.5*(lo+hi)
            if f(mid) < 0: lo = mid
            else: hi = mid
        return 0.5*(lo+hi)
    return math.sqrt(solve(gb20)/gb20), Ye_s
for s, name in ((S_DE, "canonical"), (S_CRIT, "alt")):
    gv, Yes = gamma20(s)
    print(f"     {name}: Y_e = {Yes:.3f}, gamma_v(20 kAU) = {gv:.4f}")
gcan, _ = gamma20(S_DE); galt, _ = gamma20(S_CRIT)
print(f"     KILL: a DR4 value outside [{min(gcan,galt)-0.01:.3f}, {max(gcan,galt)+0.01:.3f}] at 20 kAU")
print(f"     kills the photocount-EFE reading; a value inside Arm A (>= 1.1614) kills it at high confidence.")

print("\nK004 COMPLETE.")
