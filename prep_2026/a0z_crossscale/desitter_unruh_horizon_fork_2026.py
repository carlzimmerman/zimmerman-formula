#!/usr/bin/env python3
"""
desitter_unruh_horizon_fork_2026.py -- WHICH HORIZON sources a0? A BAO-forced mechanism test.
=============================================================================================
Carl Zimmerman's de Sitter-Unruh MODIFIED INERTIA. a0 = c H_Lambda / Z, Z = sqrt(32pi/3).
The de Sitter-Unruh mechanism ties a0 to the Unruh temperature of a SPECIFIC horizon. Which
one is a POSIT -- and different horizons give OPPOSITE a0(z) evolution, which BAO's precise
H(z) and rho_DE(z) make razor-sharp. This is a MECHANISM discriminator, sharper than the
footing question, and it forces the formula with only a CRUDE high-z a0 measurement because
the readings diverge by a FACTOR at z~2-3 (not a percent).

THREE HORIZON READINGS (all normalized to a0(0), so ratio=1 at z=0; the DIVERGENCE grows with z):
  (A) DE SITTER / future-event-horizon  [Carl's canonical]:  a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE0)
      -> DECLINES (the committed a0z band: bump then decline to ~0.77 at z=3).
  (B) HUBBLE horizon  [McCulloch MiHsC / quantised inertia; credited]: a0(z)/a0(0) = H(z)/H0 = E(z)
      -> RISES steeply (E(z) is matter-dominated at high z).
  (C) APPARENT horizon (flat FRW) = 1/H -> same rate as (B); listed for completeness.

BAO measures E(z) directly (radial BAO, ~1-2%) and rho_DE(z) via (w0,wa) (~few%), so BOTH
readings are razor-sharp. The de Sitter-Unruh mechanism (Unruh temp of the FUTURE de Sitter
horizon) predicts (A). If a future a0(z) measurement shows RISING a0 (the contested MUSE-DARK
III hint), that DISFAVORS Carl's mechanism and FAVORS the Hubble-horizon reading (B).

Milgrom 1983/1999 (PLA 253:273) wellhead credit for nu; McCulloch (MiHsC) credited for (B).
a0's VALUE and the horizon choice are POSITS; both footings carried. No TOE. Exit 0 = ran.
"""
import numpy as np
np.seterr(all="ignore")   # silence a spurious platform BLAS matmul warning (results unaffected)

# ---- cosmology (Planck-2018 flat; DESI DR2 w0waCDM central per compilation) ----
OM = 0.3150                      # Omega_m (Planck TT,TE,EE+lowE+lensing base)
ODE = 1.0 - OM
DESI = {  # (w0, wa) DESI DR2 w0waCDM central per SNe compilation (arXiv:2503.14738)
    "Pantheon+": (-0.838, -0.62),
    "DESY5":     (-0.752, -0.86),
    "Union3":    (-0.667, -1.09),
    "LCDM":      (-1.0,    0.0),
}
Z = np.sqrt(32*np.pi/3)
A0_CAN, A0_ALT = 9.355e-11, 1.131e-10   # canonical (cH_Lambda/Z) vs alt (cH0/Z)
ZTEST = [0.0, 0.5, 1.0, 2.0, 3.0]

def rho_de_ratio(z, w0, wa):
    """CPL rho_DE(z)/rho_DE0 = (1+z)^{3(1+w0+wa)} exp(-3 wa z/(1+z))."""
    z = np.asarray(z, float)
    return (1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*z/(1+z))

def E(z, w0, wa):
    """H(z)/H0 = sqrt(Om (1+z)^3 + ODE rho_DE(z)/rho_DE0)  (flat)."""
    z = np.asarray(z, float)
    return np.sqrt(OM*(1+z)**3 + ODE*rho_de_ratio(z, w0, wa))

def a0_deSitter(z, w0, wa):   # reading (A): DE / future-event horizon  -> declines
    return np.sqrt(rho_de_ratio(z, w0, wa))

def a0_Hubble(z, w0, wa):     # reading (B): Hubble horizon (McCulloch) -> rises
    return E(z, w0, wa)

bar = "="*94
print(bar); print("de Sitter-Unruh MI: WHICH HORIZON sources a0? -- BAO-forced mechanism fork"); print(bar)
print(f"  a0 = cH_Lambda/Z, Z = {Z:.5f}. Canonical a0(0)={A0_CAN:.3e}, alt={A0_ALT:.3e} m/s^2.")
print(f"  Omega_m={OM}, Omega_DE={ODE:.4f}. Both readings normalized to a0(0) (ratio=1 at z=0).\n")

# ------------------------------------------------------------------ the fork table
print("  a0(z)/a0(0) under each horizon reading, and their RATIO (the divergence):")
print(f"  {'z':>4} | {'(A) deSitter sqrt(rhoDE)':>24} | {'(B) Hubble E(z) [McCulloch]':>28} | {'B/A divergence':>15}")
print("  " + "-"*82)
HEAD = "Pantheon+"
w0, wa = DESI[HEAD]
div = {}
for z in ZTEST:
    A = float(a0_deSitter(z, w0, wa)); B = float(a0_Hubble(z, w0, wa))
    div[z] = B/A
    print(f"  {z:>4.1f} | {A:>24.3f} | {B:>28.3f} | {B/A:>14.2f}x")
print(f"\n  => at z=3 the two mechanisms differ by {div[3.0]:.1f}x -- a FACTOR, not a percent.")
print(f"     Carl's de Sitter reading: a0 DECLINES to {a0_deSitter(3.0,w0,wa):.2f}x;")
print(f"     McCulloch Hubble reading: a0 RISES to {a0_Hubble(3.0,w0,wa):.2f}x.  (Pantheon+ w0wa)")

# ------------------------------------------------------------------ BAO razor on each
print("\n" + bar); print("BAO razor: how sharp is each reading? (BAO gives E(z) ~1-2%, rho_DE via w0wa ~few%)"); print(bar)
# Monte-Carlo the (w0,wa) posterior width into each reading; E(z) also carries direct BAO ~1.5%
SIG = {"Pantheon+": (0.055, 0.22, -0.86), "DESY5": (0.057, 0.22, -0.86), "Union3": (0.088, 0.31, -0.87)}
rng = np.random.default_rng(0)
for comp in ["Pantheon+", "DESY5", "Union3"]:
    w0c, wac = DESI[comp]; sw0, swa, rho = SIG[comp]
    L = np.linalg.cholesky([[sw0**2, rho*sw0*swa], [rho*sw0*swa, swa**2]])
    pair = np.array([w0c, wac]) + rng.standard_normal((200000, 2)) @ L.T
    W0, WA = pair[:, 0], pair[:, 1]
    A3 = np.sqrt(rho_de_ratio(3.0, W0, WA))
    B3 = np.sqrt(OM*4**3 + ODE*rho_de_ratio(3.0, W0, WA))   # E(3); Om(1+z)^3 dominates -> tiny frac error
    print(f"  [{comp:9}] z=3: (A) deSitter a0={np.median(A3):.3f} +/-{np.std(A3):.3f}"
          f"   (B) Hubble a0={np.median(B3):.3f} +/-{np.std(B3):.3f}"
          f"   B/A={np.median(B3)/np.median(A3):.1f}x")
print("  (B) is razor-sharp: at high z E(z) is matter-dominated, so BAO's ~1.5% H(z) pins it")
print("      to ~1%. (A) inherits the wider (w0,wa). The A-vs-B GAP dwarfs both errors.")

# ------------------------------------------------------------------ the forcing statement
print("\n" + bar); print("THE FORCING: what a0(z) precision distinguishes the mechanisms?"); print(bar)
for z in [1.0, 2.0, 3.0]:
    A = float(a0_deSitter(z, w0, wa)); B = float(a0_Hubble(z, w0, wa))
    gap = abs(B-A)                      # absolute a0(z)/a0(0) gap between mechanisms
    mid = 0.5*(A+B)
    # crude a0(z) measurement with fractional precision f on a0(z); it separates A from B at 3s if
    #   gap >= 3 * f * mid  ->  f <= gap/(3 mid)
    f_needed = gap/(3*mid)
    print(f"  z={z:.0f}: gap(B-A)={gap:.2f} in a0/a0(0);  a CRUDE a0(z) at {100*f_needed:.0f}% precision"
          f" separates the mechanisms at 3 sigma.")
print("  Contrast: the FOOTING question (9.36 vs 1.13, 21%) needs ~7% a0 precision (Step-A floored).")
print("  The HORIZON MECHANISM question needs only tens-of-percent at z~2-3 -- FAR more forcible,")
print("  because BAO drives the two readings a FACTOR apart, not a percent.")

# ------------------------------------------------------------------ honest verdict + MUSE tension
print("\n" + bar); print("VERDICT (honest, both directions)"); print(bar)
print(f"""  * BAO FORCES a MECHANISM discriminator, not just a number. Using DESI's precise E(z) and
    rho_DE(z), the de Sitter-horizon reading (Carl's, a0 DECLINES to ~0.77x at z=3) and the
    Hubble-horizon reading (McCulloch MiHsC, a0 RISES to ~{a0_Hubble(3.0,w0,wa):.1f}x) diverge by
    ~{div[3.0]:.0f}x at z=3 -- both razor-sharp from BAO. A crude high-z a0(z) point (tens of
    percent) forces the choice; it does NOT need the ~7% precision the footing question demands.
  * This is what makes de Sitter-Unruh MI DISTINCT from McCulloch's quantised inertia: they are
    NOT the same theory -- they pick different horizons and predict OPPOSITE a0(z). BAO exposes it.
  * LIVE TENSION (stated, not spun): the contested MUSE-DARK III hint of RISING a0 would favor the
    Hubble/McCulloch reading over Carl's de Sitter reading. It is LCDM-degenerate and not a
    confirmation of either, but it is the live pull, and it points AWAY from the declining branch.
  * STILL data-gated: forcing needs a resolved high-z a0(z) point (the cross-redshift wall) -- but
    at a FACTOR-level, not percent-level, target. That is the honest good news BAO brings.
  * Both footings carried; the horizon choice and a0's value are POSITS; nu is Milgrom-1999's;
    McCulloch credited for the Hubble-horizon reading. No 'theory closed'.""")

# ------------------------------------------------------------------ self-check
assert a0_deSitter(0,w0,wa) == 1.0 and abs(a0_Hubble(0,w0,wa)-1.0) < 1e-12, "z=0 normalization"
assert a0_deSitter(3.0,-1.0,0.0) == 1.0, "LCDM de Sitter reading is flat=1 (no evolution)"
assert a0_Hubble(3.0,w0,wa) > 3.0, "Hubble reading rises steeply (matter-dominated) at z=3"
assert div[3.0] > 4.0, "the mechanisms diverge by >4x at z=3"
print(f"\n  SELF-CHECK OK: z=0 both=1; LCDM deSitter flat; Hubble rises {a0_Hubble(3.0,w0,wa):.1f}x; "
      f"divergence {div[3.0]:.1f}x @ z=3.  EXIT 0 (ran; not a verdict).")
