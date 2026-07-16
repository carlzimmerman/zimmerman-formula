#!/usr/bin/env python3
"""
ledger_fork_context.py -- fork-prediction context columns for the high-z TFR
DATA_LEDGER (Lane D). Reuses the footing-locked a0(z) machinery of
prep_2026/btfr_forecast_audit/btfr_forecast_check.py (banked anchors re-asserted
here so the ledger's prediction columns cannot silently drift from the bank).

CONVENTION (matches the observational ledger): Delta_b = zero-point offset
ALONG THE MASS AXIS at fixed velocity, relative to z=0, in dex.
Deep-MOND BTFR:  M_bar = v^4 / (G a0)  ->  Delta_b = -log10( a0(z)/a0(0) ).

FOOTINGS (run both, per the working rule):
  CANONICAL: a0 = cH_Lambda/Z = 9.36e-11,  a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0))
             -> EXACTLY 0 under pure Lambda (w=-1); mildly POSITIVE Delta_b at
             high z under the DESI DR2 CPL best fit (w0=-0.752, wa=-0.86).
  ALT:       a0 ~ cH(z)/Z (rho_total/cH0 branch, 1.13e-10 at z=0)
             -> a0 ratio = E(z), Delta_b = -log10 E(z) < 0 (RISING a0).

LCDM-DEGENERACY REFERENCE (mandatory check): the standard halo-scaling drift
of the TFR zero-point, Delta_b_LCDM = -log10[ E(z) * (Dc(z)/Dc(0))^(1/2) ]
(Mo, Mao & White 1998 scaling as used by Ubler+17 / Jeanneau+26; Dc = Bryan &
Norman 1998 virial overdensity). NOTE: this is the same functional family as
the ALT footing (-log10 E(z)) -- the alt branch is LCDM-degenerate at ALL z.

ACCELERATION DILUTION (honesty column): the deep-MOND lever dlnM/dln a0 = -1
holds only for g_bar << a0. From the framework's OWN interpolation
g_obs = sqrt(g_bar^2 + g_bar a0) (dS-Unruh), at fixed g_obs:
    dln g_bar / dln a0 = -x/(2+x),   x = a0/g_bar,
so a sample observed at accelerations g_bar ~ (2-7) a0 carries only 7-20% of
the deep-MOND signal. Per-sample x is estimated from typical v and the radius
of the velocity measurement (order-of-magnitude; carried as a systematic).

Exit 0; asserts only reproduce banked anchors.
"""
import numpy as np

# ---------------- cosmology (identical to banked script) ----------------
Om, OL = 0.315, 0.685
W0_DR2, WA_DR2 = -0.752, -0.86      # banked DESI DR2 CPL best fit

def f_DE(z, w0=W0_DR2, wa=WA_DR2):
    z = np.asarray(z, dtype=float)
    return (1 + z) ** (3 * (1 + w0 + wa)) * np.exp(-3 * wa * z / (1 + z))

def E_z(z, w0=W0_DR2, wa=WA_DR2):
    return np.sqrt(Om * (1 + np.asarray(z, dtype=float)) ** 3 + OL * f_DE(z, w0, wa))

def a0_ratio_canonical(z):   # sqrt(rho_DE ratio)
    return np.sqrt(f_DE(z))

def a0_ratio_alt(z):         # E(z)
    return E_z(z)

def dlogM(a0_ratio):         # mass-axis zero-point offset (deep-MOND)
    return -np.log10(a0_ratio)

# banked anchors (must reproduce, not inputs)
r3 = float(a0_ratio_canonical(3.0))
assert abs(r3 - 0.74) < 0.01, r3
assert abs(0.25 * np.log10(r3) - (-0.033)) < 0.001          # dlogV(z=3) canonical
assert abs(0.25 * np.log10(a0_ratio_alt(3.0)) - 0.164) < 0.003  # dlogV(z=3) alt
assert np.allclose(np.sqrt(f_DE([1, 2, 3], w0=-1.0, wa=0.0)), 1.0)  # pure-Lambda const
print("[OK] banked anchors reproduced (a0(3)/a0(0)=%.3f; dlogV(3): canon -0.033, alt +0.164)" % r3)

# ---------------- LCDM halo-scaling reference ----------------
def Delta_c(z):
    """Bryan & Norman 1998 virial overdensity (flat LCDM, x = Omega_m(z)-1)."""
    z = np.asarray(z, dtype=float)
    Ez2 = Om * (1 + z) ** 3 + OL          # pure-Lambda E^2 for the LCDM reference
    Omz = Om * (1 + z) ** 3 / Ez2
    x = Omz - 1
    return 18 * np.pi ** 2 + 82 * x - 39 * x ** 2

def dlogM_lcdm(z):
    """Halo-defining-quantities drift: M ~ v^3 / [H(z) sqrt(Dc(z))] at fixed v."""
    Ez = np.sqrt(Om * (1 + np.asarray(z, float)) ** 3 + OL)   # LCDM E(z)
    return -np.log10(Ez * np.sqrt(Delta_c(z) / Delta_c(0.0)))

# cross-check against Jeanneau+26: the [H sqrt(Dc)]^-1 term = -0.34 dex at z~1
chk = float(dlogM_lcdm(1.0))
assert abs(chk - (-0.34)) < 0.03, chk
print("[OK] LCDM halo-term at z=1 = %.3f dex (Jeanneau+26 quote: -0.34)" % chk)

# ---------------- acceleration dilution ----------------
A0 = 9.36e-11  # m/s^2, canonical
KPC = 3.0857e19  # m

def dilution(v_kms, R_kpc):
    """x/(2+x), x=a0/g_bar with g_bar ~ g_obs v^2/R demoted via the framework nu.
    We estimate g_bar from g_obs by inverting g_obs = sqrt(g_bar^2+g_bar*a0)."""
    g_obs = (v_kms * 1e3) ** 2 / (R_kpc * KPC)
    # invert: g_bar = (-a0 + sqrt(a0^2 + 4 g_obs^2))/2
    g_bar = 0.5 * (-A0 + np.sqrt(A0 ** 2 + 4 * g_obs ** 2))
    x = A0 / g_bar
    return g_bar / A0, x / (2 + x)

# per-sample typical (v, R at velocity measurement) -- order of magnitude
samples = [
    # label,                     z_eff, v_kms, R_kpc
    ("Ubler+17 KMOS3D z~0.9",     0.9, 200.0, 6.6),   # vcirc,max ~2.2Rd, Rd~3kpc
    ("Ubler+17 KMOS3D z~2.3",     2.3, 210.0, 5.5),
    ("Tiley+16/19 KROSS z~0.9",   0.9, 130.0, 5.0),
    ("Jeanneau+26 MUSE-DARK z~1", 0.9,  90.0, 4.5),   # low-mass lensed, v(1.8-2Re)
    ("Straatman+17 ZFIRE z~2.2",  2.2, 200.0, 5.0),
    ("Amvrosiadis+25 DSFG z~2.4", 2.4, 400.0, 8.0),   # massive DSFGs, v(2Re)
    ("Turner+17 KDS z~3.5",       3.5, 100.0, 2.5),
    ("Danhaive+26 FRESCO z~5",    5.0, 120.0, 1.0),   # v_circ(Re), Re~1kpc
]

print()
print("%-30s %5s | %8s %8s %8s | %7s %8s | %s" % (
    "sample", "z", "canonCPL", "canonLam", "ALT", "LCDM", "g/a0", "dilution"))
print("-" * 110)
rows = []
for label, z, v, R in samples:
    dc = float(dlogM(a0_ratio_canonical(z)))
    da = float(dlogM(a0_ratio_alt(z)))
    dl = float(dlogM_lcdm(z))
    gr, dil = dilution(v, R)
    rows.append((label, z, dc, da, dl, gr, dil))
    print("%-30s %5.2f | %+8.3f %+8.3f %+8.3f | %+7.3f %8.1f | %5.2f  (alt diluted: %+.3f)"
          % (label, z, dc, 0.0, da, dl, gr, dil, dil * da))

print("""
READING (mass-axis Delta_b, dex):
  canonLam  = canonical footing, pure Lambda: exactly 0.000 at all z.
  canonCPL  = canonical footing under DESI DR2 CPL (a0 DECLINES -> Delta_b > 0,
              i.e. slightly HIGHER M_bar at fixed v at high z).
  ALT       = rho_total/cH0 footing (a0 RISES ~ E(z)) -> Delta_b < 0.
  LCDM      = standard halo-scaling drift -log10[E sqrt(Dc ratio)] -- note it
              TRACKS the ALT column within ~0.1 dex at every z: the alt footing
              is LCDM-degenerate in this observable at all z.
  dilution  = fraction of the deep-MOND a0-lever actually available at the
              sample's typical acceleration (framework's own nu). The fork
              separation quoted by the bank (0.20 dex velocity-axis at z=3)
              assumes deep-MOND; in-hand samples carry 7-45%% of it.
""")
print("EXIT 0")
