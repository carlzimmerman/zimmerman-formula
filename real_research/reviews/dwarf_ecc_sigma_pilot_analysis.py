#!/usr/bin/env python3
r"""
dwarf_ecc_sigma_pilot_analysis.py
================================================================================
PER-DWARF prediction of the framework's NATIVE non-adiabatic-inertia signal.

Framework (its OWN premise, NOT a MOND variant):
  inertia = nonlocal-in-time RESPONSE to the de Sitter cosmic-horizon Unruh bath;
  the bath has ONE clock H_Lambda; a0 = c*H_Lambda/Z = 9.36e-11 m/s^2.

PREDICTION: at fixed pericenter + mass, a radial-PLUNGE MW dwarf runs ~19-28%
HOTTER (internal sigma) than a CIRCULAR one (time-nonlocal inertia reads the
accel HISTORY; plunge sheds adiabatic loading -> deeper deep-MOND). SIGN =
theorem (plunge -> hotter); magnitude theta(y)-hostage (factor ~2).
MODIFIED-GRAVITY-IMPOSSIBLE (MG has instantaneous EFE -> exactly 0 correlation).

FOOTING (sealed): a0 = 9.36e-11; framework's OWN interpolation
  nu(y)   = sqrt(1 + 1/y);   mu_fw(x) = (sqrt(1+4x^2)-1)/(2x).
NEVER McGaugh nu.

This script READS dwarf_ecc_sigma_pilot_data.py (real cited P22/Gaia data) and
for EACH dwarf computes:
  (a) g_in ~ sigma^2/r_half  and  omega_in ~ sigma/r_half;
  (b) g_ext(r_peri) from the MW enclosed-mass rotation curve, and
      omega_ext ~ orbital frequency at pericenter = sqrt(G M(<r_peri)/r_peri^3);
  (c) y = omega_ext / omega_in at pericenter (the non-adiabatic parameter);
  (d) classify: carrier (y >~ 1) vs adiabatic control (y << 1);
  (e) the PREDICTED sigma-boost vs the adiabatic baseline
      (sign fixed: plunge/high-ecc -> hotter; theta(0)=2..e banked range).

BOTH-WAYS / anti-p-hack: pre-specified physics; report the y-distribution and
which dwarfs carry the signal; do NOT manufacture. DO NOT git-push.
================================================================================
"""
import math
import importlib.util
import os

# ---- load the data module by absolute path (cwd-safe) -----------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
_DATA = os.path.join(_HERE, "dwarf_ecc_sigma_pilot_data.py")
spec = importlib.util.spec_from_file_location("dwarf_data", _DATA)
dd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dd)

# ---- framework footing + constants (SI) -------------------------------------
A0     = 9.36e-11               # m/s^2  c*H_Lambda/Z, sealed pure-Lambda de Sitter
CH_LAM = 5.42e-10              # m/s^2
G      = 6.674e-11             # SI
Msun   = 1.989e30             # kg
kpc    = 3.0857e19            # m
km     = 1.0e3
pc     = 3.0857e16            # m

def nu(y):     return math.sqrt(1.0 + 1.0/y)              # framework boost
def mu_fw(x):  return (math.sqrt(1.0 + 4.0*x*x) - 1.0)/(2.0*x)

# theta(y): Milgrom 2022 example forms (theta(1)=1, decreasing, theta(0)~few).
def theta_rational(y): return 2.0/(1.0 + y*y)             # theta(0)=2
def theta_exp(y):      return math.exp(1.0 - abs(y))      # theta(0)=e
THETA0_LO, THETA0_HI = 2.0, math.e                        # banked range

# -----------------------------------------------------------------------------
# MILKY WAY enclosed-mass model (for g_ext, omega_ext at pericenter).
# Use a standard MW rotation-curve enclosed mass. We adopt the widely-used
# spherical-enclosed-mass approximation pinned to two anchors:
#   M(<r) such that v_c(r) ~ flat ~ 220 km/s in the inner disk and the
#   enclosed mass at ~50 kpc ~ 4e11 Msun, ~100 kpc ~ 7e11 Msun (Gibbons+2014,
#   Bland-Hawthorn & Gerhard 2016, Eadie & Juric 2019 are all consistent at the
#   ~30% level in this 20-150 kpc pericenter range). We use a smooth two-anchor
#   power-law M(<r) = M50 * (r/50kpc)^alpha calibrated to (50kpc,4.0e11) and
#   (100kpc,7.0e11) -> alpha = ln(7/4)/ln(2) ~ 0.807. This is the dominant
#   systematic; we CARRY it (report g_ext both at this fiducial and at a +/-30%
#   mass bracket) rather than pretend precision.
# -----------------------------------------------------------------------------
M50_MW   = 4.0e11 * Msun       # enclosed within 50 kpc (Gibbons+2014/BHG2016)
M100_MW  = 7.0e11 * Msun       # enclosed within 100 kpc
ALPHA_MW = math.log(M100_MW/M50_MW) / math.log(100.0/50.0)   # ~0.807

def M_MW_enc(r_m):
    """spherical enclosed MW mass at galactocentric radius r (m)."""
    return M50_MW * (r_m / (50.0*kpc))**ALPHA_MW

def g_ext_MW(r_kpc):
    r = r_kpc*kpc
    return G*M_MW_enc(r)/r**2

def omega_ext_MW(r_kpc):
    """orbital angular frequency at pericenter ~ rate of change of a_ext."""
    r = r_kpc*kpc
    return math.sqrt(G*M_MW_enc(r)/r**3)

# -----------------------------------------------------------------------------
# Per-dwarf internal scales. r_half in pc -> m. sigma in km/s -> m/s.
#   g_in  ~ sigma^2 / r_half     (internal acceleration scale)
#   omega_in ~ sigma / r_half    (internal orbital angular frequency)
# These are the standard order-unity definitions (consistent with Milgrom 2022
# omega_in = v/R and the member_MI_nonadiabatic_plunge.py usage).
# -----------------------------------------------------------------------------
def internal_scales(sigma_kms, r_half_pc):
    sig = sigma_kms*km
    rh  = r_half_pc*pc
    g_in     = sig**2 / rh
    omega_in = sig / rh
    return g_in, omega_in

# -----------------------------------------------------------------------------
# Predicted sigma boost of a PLUNGE (high-ecc, non-adiabatic) vs a CIRCULAR
# (adiabatic) dwarf at MATCHED pericenter + mass.
#
# Adiabatic baseline (circular, Milgrom Eq.35): the EFE enters as theta(0)*a_ex
#   -> internal boost B_circ = 1/mu_fw( (g_in + theta(0)*g_ext) / a0 ).
# Plunge (non-adiabatic, y~1 at pericenter): theta(y)->~theta(1)=1
#   -> B_plunge = 1/mu_fw( (g_in + theta(y)*g_ext) / a0 ).
# Since theta decreasing (theta(0)>theta(1)), the plunge sheds external loading
#   -> LESS EFE suppression -> deeper deep-MOND -> HIGHER boost -> HOTTER.
#   sigma ~ sqrt(boost * g_in * r_half)  =>  sigma ratio = sqrt(B_plunge/B_circ).
# We report the predicted PLUNGE/CIRCULAR sigma ratio for this dwarf's OWN
# (g_in, g_ext, y) -- i.e. "if this same dwarf were instead on a circular orbit
# at the same pericenter, how much colder would it be?" SIGN fixed; magnitude
# spans theta(0)=2..e.
# -----------------------------------------------------------------------------
def predicted_boost(g_in, g_ext, y, theta0_func):
    th0 = theta0_func(0.0)
    thy = theta0_func(y)
    A_circ   = (g_in + th0*g_ext) / A0
    A_plunge = (g_in + thy*g_ext) / A0
    B_circ   = 1.0/mu_fw(A_circ)
    B_plunge = 1.0/mu_fw(A_plunge)
    sig_ratio = math.sqrt(B_plunge / B_circ)
    return sig_ratio, B_circ, B_plunge

# =============================================================================
print("="*118)
print(" DWARF ECC-SIGMA PILOT  --  framework native non-adiabatic-inertia prediction (a0=9.36e-11, framework nu/mu_fw)")
print("="*118)
print(f"  MW enclosed-mass model: M(<r)=4.0e11 Msun*(r/50kpc)^{ALPHA_MW:.3f}  [Gibbons+14 / BHG16 anchors, +/-30% carried]")
print(f"  a0={A0:.3e} m/s^2 ; cH_Lambda={CH_LAM:.3e}; theta(0) banked range = {THETA0_LO:.2f}..{THETA0_HI:.3f} (rational..exp)\n")

rows = []
for d in dd.dwarfs:
    name   = d["name"]
    sigma  = d["sigma_los"]
    rhalf  = d["r_half_pc"]
    rperi  = d["r_peri_lmc"]      # fiducial MW+LMC pericenter (P22 T3)
    rperi_nl = d["r_peri_nl"]
    ecc    = d["ecc_lmc"]
    if sigma is None or rhalf is None or rperi is None:
        rows.append({"name": name, "usable": False, "regime": d["regime"],
                     "carrier_flag": d["carrier"], "conf": d["confidence"]})
        continue

    g_in, omega_in = internal_scales(sigma, rhalf)
    g_ext   = g_ext_MW(rperi)
    omega_ext = omega_ext_MW(rperi)
    y       = omega_ext / omega_in
    # no-LMC pericenter bracket on y
    g_ext_nl = g_ext_MW(rperi_nl) if rperi_nl else None
    omega_ext_nl = omega_ext_MW(rperi_nl) if rperi_nl else None
    y_nl    = (omega_ext_nl/omega_in) if omega_ext_nl else None

    # predicted plunge-vs-circular sigma boost, theta(0)=2 and theta(0)=e
    sr_rat, Bc_r, Bp_r = predicted_boost(g_in, g_ext, y, theta_rational)
    sr_exp, Bc_e, Bp_e = predicted_boost(g_in, g_ext, y, theta_exp)

    # classify by y (the non-adiabatic parameter). carrier: y >~ 1 (reaches the
    # non-adiabatic band where theta is a real function, not theta(0)).
    if y >= 0.8:
        yreg = "CARRIER (non-adiabatic)"
    elif y >= 0.3:
        yreg = "borderline"
    else:
        yreg = "adiabatic control"

    rows.append({
        "name": name, "usable": True, "sigma": sigma, "rhalf_pc": rhalf,
        "rperi": rperi, "ecc": ecc,
        "g_in_a0": g_in/A0, "g_ext_a0": g_ext/A0,
        "omega_in": omega_in, "omega_ext": omega_ext,
        "y": y, "y_nl": y_nl, "yreg": yreg,
        "sig_ratio_rat": sr_rat, "sig_ratio_exp": sr_exp,
        "pred_pct_lo": (min(sr_rat, sr_exp)-1)*100,
        "pred_pct_hi": (max(sr_rat, sr_exp)-1)*100,
        "data_carrier": d["carrier"], "data_regime": d["regime"],
        "conf": d["confidence"],
    })

# ---- main per-dwarf table ----------------------------------------------------
print("-"*118)
print(f"  {'dwarf':18s} {'sig':>4} {'rhalf':>7} {'rperi':>6} {'ecc':>4} | "
      f"{'g_in/a0':>8} {'g_ext/a0':>8} | {'y=we/wi':>8} {'y_nL':>6} | "
      f"{'pred sig boost':>15} | {'y-regime':>22}")
print(f"  {'':18s} {'km/s':>4} {'pc':>7} {'kpc':>6} {'':>4} | "
      f"{'':>8} {'':>8} | {'@peri':>8} {'':>6} | {'plunge/circ %':>15} | {'':>22}")
print("  "+"-"*114)
usable = [r for r in rows if r.get("usable")]
# sort by y descending so carriers float to the top
usable_sorted = sorted(usable, key=lambda r: -r["y"])
for r in usable_sorted:
    ynl = f"{r['y_nl']:.2f}" if r["y_nl"] is not None else "  -  "
    print(f"  {r['name']:18s} {r['sigma']:4.1f} {r['rhalf_pc']:7.0f} "
          f"{r['rperi']:6.1f} {r['ecc']:4.2f} | {r['g_in_a0']:8.3f} {r['g_ext_a0']:8.3f} | "
          f"{r['y']:8.2f} {ynl:>6} | {r['pred_pct_lo']:6.1f}-{r['pred_pct_hi']:5.1f}% | {r['yreg']:>22}")

# unusable
unus = [r for r in rows if not r.get("usable")]
if unus:
    print("\n  (no sigma or no pericenter -> cannot enter test):")
    for r in unus:
        print(f"    {r['name']:18s} [{r['conf']}] regime={r['regime']}")

# ---- y-distribution summary --------------------------------------------------
print("\n"+"="*118)
print(" y-DISTRIBUTION (the non-adiabatic parameter y = omega_ext/omega_in at pericenter)")
print("="*118)
ys = [r["y"] for r in usable]
carriers   = [r for r in usable if r["y"] >= 0.8]
borderline = [r for r in usable if 0.3 <= r["y"] < 0.8]
controls   = [r for r in usable if r["y"] < 0.3]
import statistics as st
print(f"  N usable (sigma & ecc & peri)        : {len(usable)}")
print(f"  y range                              : {min(ys):.2f} .. {max(ys):.2f}")
print(f"  y median                             : {st.median(ys):.2f}")
print(f"  CARRIERS (y >= 0.8, non-adiabatic)   : {[r['name'] for r in sorted(carriers,key=lambda r:-r['y'])]}")
print(f"  borderline (0.3 <= y < 0.8)          : {[r['name'] for r in sorted(borderline,key=lambda r:-r['y'])]}")
print(f"  adiabatic controls (y < 0.3)         : {[r['name'] for r in sorted(controls,key=lambda r:-r['y'])]}")

# cross-check against the pre-specified data-file carrier flags
print("\n  CROSS-CHECK vs pre-specified data-file carrier flags:")
for r in usable:
    flagged = "carrier" if r["data_carrier"] else r["data_regime"]
    computed = ("carrier" if r["y"]>=0.8 else ("borderline" if r["y"]>=0.3 else "control"))
    match = "OK" if (("carrier" in flagged)==("carrier"==computed)) else "<-- DIFFERS"
    if "DIFFERS" in match or r["data_carrier"] or computed=="carrier":
        print(f"    {r['name']:18s} data-flag={flagged:12s} y-computed={computed:11s} (y={r['y']:.2f})  {match}")

# ---- predicted-boost summary on the carriers --------------------------------
print("\n"+"="*118)
print(" PREDICTED sigma-BOOST (plunge vs circular at matched pericenter+mass), framework theta(0)=2..e")
print("="*118)
print("  SIGN = theorem: high-y plunge -> HOTTER (sheds adiabatic external loading -> deeper deep-MOND).")
print("  MG/CDM prediction at fixed pericenter = EXACTLY 0 (instantaneous EFE). This is the discriminator.\n")
for r in sorted(carriers+borderline, key=lambda r:-r['y']):
    print(f"    {r['name']:18s} y={r['y']:4.2f}  ecc={r['ecc']:.2f}  "
          f"predicted plunge-vs-circular sigma boost = +{r['pred_pct_lo']:.1f}..+{r['pred_pct_hi']:.1f}%  "
          f"[{r['conf']}]")

print("\n  ADIABATIC CONTROLS (should show ~0 native boost -- built-in null):")
for r in sorted(controls, key=lambda r:-r['y']):
    print(f"    {r['name']:18s} y={r['y']:4.2f}  ecc={r['ecc']:.2f}  "
          f"predicted boost = +{r['pred_pct_lo']:.2f}..+{r['pred_pct_hi']:.2f}%  [{r['conf']}]")

print("\n"+"="*118)
print(" MAGNITUDE CAVEAT (both ways, anti-oversell)")
print("="*118)
print(r"""  The banked HEADLINE '+19-28% hotter' is the y=1 reference: sigma ~ (theta(0)/theta(1))^(1/4)
  with theta(1)=1 and theta(0)=2..e  ->  (2)^0.25=1.19 .. (e)^0.25=1.28  =  +19..28%.
  That compares a y=1 plunge to a y=0 circular dwarf.

  The two carriers reach y = 2.5-3.3 at pericenter (deeper than y=1), and they sit VERY deep in
  deep-MOND (g_in ~ 0.002-0.004 a0). Both effects push the full-mu_fw plunge/circular sigma ratio
  ABOVE the headline (+130..+250% in the table). BUT: (i) y>1 means theta(y) is UNVERIFIED -- Milgrom
  pins only theta(1)=1, theta(0)~few, decreasing; extrapolating theta BELOW 1 for y>1 is kernel-
  hostage, so the >100% magnitudes are NOT reliable numbers. (ii) The SIGN (plunge -> hotter) is the
  theorem and is robust for ALL theta forms. NET: report the SIGN + carrier identity as the result;
  quote the magnitude as '>= the +19-28% headline, theta(y)-hostage above that', NOT as a literal
  +150%. Do not oversell the big number; do not bury that the effect is at-least-headline-large.""")
print("\n"+"="*118)
print(" DONE. (LOCAL pilot, real cited P22/Gaia data, no fabrication, no git-push.)")
print("="*118)
