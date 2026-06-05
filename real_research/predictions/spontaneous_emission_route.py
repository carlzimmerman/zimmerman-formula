#!/usr/bin/env python3
"""
ROUTE TEST: atomic SPONTANEOUS EMISSION (Einstein A coefficient, QED vacuum)  vs  the cosmological a0.
====================================================================================================
Question (honest): does the rate at which an excited atom spontaneously emits a photon -- the Einstein
A coefficient, i.e. the atom's coupling to the QED vacuum -- have any *physical* connection to the
emergent-gravity acceleration a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_Lambda) = 9.36e-11 m/s^2?

The de Sitter (Gibbons-Hawking) background turns the vacuum into a thermal bath at
    T_dS = hbar H_Lambda / (2 pi k_B),   H_Lambda = c sqrt(Lambda/3)  (the asymptotic de Sitter rate).
That bath *does* perturb radiative processes. Three REAL, literature-backed channels:
   (1) downward-emission enhancement:  A -> A (1 + n_bar),  n_bar = 1/(exp(hbar w0/kT_dS) - 1)  [Einstein 1917]
   (2) spontaneous EXCITATION of a ground-state atom, "as if" in a bath at T_dS  [Yu & Zhou 0802.2018]
   (3) de Sitter curvature correction to the Lamb shift ~ (H_Lambda/w0)^2          [Zhu & Yu 1012.4055]

We COMPUTE the size of each for real atomic transitions, extract what a0 / Z / a0(z) this route predicts,
and grade the connection. Needs numpy/scipy(optional). Reproducible: `python spontaneous_emission_route.py`.
"""
import numpy as np

# ---------------- constants (SI) ----------------
C    = 2.99792458e8       # m/s
G    = 6.674e-11          # m^3 kg^-1 s^-2
HBAR = 1.054571817e-34    # J s
KB   = 1.380649e-23       # J/K
EV   = 1.602176634e-19    # J
MPC  = 3.0857e22          # m

# ---------------- cosmology / framework ----------------
H0   = 67.4e3 / MPC       # Hubble now, s^-1
OmL  = 0.685              # dark-energy fraction now
Om_m = 0.315              # matter fraction now
LAM  = 3 * OmL * H0**2 / C**2          # cosmological constant, 1/m^2
RHO_L = LAM * C**2 / (8 * np.pi * G)   # dark-energy density (Einstein), kg/m^3

H_LAM = C * np.sqrt(LAM / 3)           # de Sitter (asymptotic) rate, s^-1
A0    = C**2 * np.sqrt(LAM / (32 * np.pi))   # framework a0
A0_b  = (C/2) * np.sqrt(G * RHO_L)     # equivalent form (cross-check)
Z_FR  = np.sqrt(32 * np.pi / 3)        # framework dimensionless Z = c H_Lam / a0

# de Sitter (Gibbons-Hawking) temperature, and Unruh temperature AT a0
T_dS   = HBAR * H_LAM / (2 * np.pi * KB)
T_U_a0 = HBAR * A0 / (2 * np.pi * C * KB)

print("#"*100)
print("# SPONTANEOUS-EMISSION ROUTE  vs  a0 = c^2 sqrt(Lambda/32pi)")
print("#"*100)
print(f"  rho_Lambda      = {RHO_L:.3e} kg/m^3   (target 5.85e-27)")
print(f"  Lambda          = {LAM:.3e} /m^2")
print(f"  H_Lambda        = {H_LAM:.4e} /s       (de Sitter rate; 1/H_Lam = {1/H_LAM/(3.156e7*1e9):.1f} Gyr)")
print(f"  a0 (32pi form)  = {A0:.4e} m/s^2")
print(f"  a0 ((c/2) form) = {A0_b:.4e} m/s^2     (cross-check, must match)")
print(f"  Z = cH_Lam/a0   = {C*H_LAM/A0:.4f}        (framework sqrt(32pi/3) = {Z_FR:.4f})")
print(f"  T_dS            = {T_dS:.4e} K")
print(f"  T_U(a0)         = {T_U_a0:.4e} K        (Unruh temp at a0; ~{T_dS/T_U_a0:.2f}x below T_dS)")
print()

# =====================================================================================================
# (1)+(2)  EMISSION/EXCITATION CHANNEL:  governed by the Planck occupation n_bar at the transition freq.
#          The de Sitter bath is at T_dS ~ 2e-30 K. Real lines have hbar*w0 >> kT_dS by ~28-34 orders.
# =====================================================================================================
print("="*100)
print("(1)+(2) EMISSION/EXCITATION CHANNEL  --  thermal correction factor (1 + n_bar), n_bar = Planck occ. at T_dS")
print("="*100)

# representative real transitions: (label, photon energy)
lines = [
    ("HI 21 cm (hyperfine)",        5.9e-6  * EV),   # 1420 MHz
    ("Rotational mm (CO J=1-0)",    4.8e-4  * EV),   # 115 GHz
    ("Lyman-alpha (optical/UV)",    10.2     * EV),
    ("Hydrogen 1s-2p (~optical)",   10.2     * EV),
    ("Na D line (visible)",         2.1      * EV),
]
print(f"   {'transition':<26}{'hbar*w0 [eV]':>14}{'hbar*w0/kT_dS':>16}{'n_bar (=corr.)':>18}")
for lab, E in lines:
    x = E / (KB * T_dS)                 # hbar*w0 / kT_dS  -- huge
    # n_bar = 1/(exp(x)-1) ~ exp(-x); compute log10 to avoid overflow
    log10_nbar = -x / np.log(10)        # log10(exp(-x))
    print(f"   {lab:<26}{E/EV:>14.3e}{x:>16.3e}{'1e'+format(log10_nbar,'.2e'):>18}")
print(f"""
   => For EVERY real atomic/molecular line, hbar*w0/kT_dS ~ 1e28 (21cm) to ~1e33 (optical).
      The fractional de Sitter correction to the emission rate is n_bar = exp(-hbar*w0/kT_dS),
      i.e. ~1e(-1e28) for 21 cm down to ~1e(-1e33) for optical. UTTERLY negligible (Boltzmann-killed).
      The linear-in-T 'hint' (~T_dS/E ~ 1e-30 K / eV ~ 1e-30) is only the *pre-exponential* scale and is
      itself never reached: the true factor is exp(-1/that), astronomically smaller.""")

# Where would a dS-ORDER correction (n_bar ~ O(1)) actually appear?  hbar*w0 ~ kT_dS:
w0_crossover = KB * T_dS / HBAR         # rad/s
P_crossover  = 2*np.pi / w0_crossover   # s
print(f"""
   CROSSOVER (where n_bar ~ O(1), i.e. hbar*w0 ~ kT_dS):  w0 ~ {w0_crossover:.3e} rad/s,
      period ~ {P_crossover/(3.156e7*1e9):.1f} Gyr ~ the Hubble time 1/H_Lam = {1/H_LAM/(3.156e7*1e9):.1f} Gyr.
      No atomic line is within ~28 orders of magnitude of that. The bath is real but irrelevant for atoms.""")
print()

# =====================================================================================================
# (3)  LAMB-SHIFT CHANNEL:  de Sitter curvature correction ~ (H_Lambda / w0)^2  [Zhu & Yu 1012.4055]
#      Power-law (not Boltzmann), so it's "larger" than channel (1)+(2) -- but still ~1e-68 for hydrogen.
# =====================================================================================================
print("="*100)
print("(3) LAMB-SHIFT CHANNEL  --  de Sitter curvature correction ~ (H_Lambda/w0)^2  (power-law)")
print("="*100)
w0_Lamb = 1.06e9 * 2*np.pi     # Lamb shift itself ~1 GHz; use a 2p atomic frequency ~2.5e15 rad/s for the line
w0_line = 2.5e15               # optical-ish atomic transition rad/s (hydrogen n=1->2 ~ 1.55e16; use 2.5e15 as rep.)
for lab, w0 in [("optical line w0~2.5e15 rad/s", 2.5e15),
                ("21cm hyperfine w0~8.9e9 rad/s", 1420e6*2*np.pi)]:
    frac = (H_LAM / w0)**2
    print(f"   {lab:<32}  (H_Lam/w0)^2 = {frac:.3e}")
print(f"""
   => Fractional dS Lamb-shift correction ~ (H_Lam/w0)^2 ~ 1e-68 (optical) to ~1e-56 (21cm).
      Power-law, so it BEATS the Boltzmann channel, but is still unobservable by ~56-68 orders.
      (Zhou & Yu 1204.2015: this becomes O(25%) ONLY at neutron-star curvature ~4GM/c^2, never cosmologically.)""")
print()

# =====================================================================================================
# WHAT a0 / Z / a0(z) DOES THIS ROUTE PREDICT?
# =====================================================================================================
print("="*100)
print("WHAT THIS ROUTE PREDICTS for a0, Z, and the a0(z) evolution")
print("="*100)

# The ONLY acceleration scale you can build from the emission physics + de Sitter bath is via T_dS:
#   the bath is set by H_Lambda. If you (over-)interpret 'the acceleration whose Unruh temp = T_dS', you get
#   a_such-that T_U(a) = T_dS  ==>  a = 2 pi c k T_dS / hbar = c H_Lambda  (Z = 1), NOT a0.
a_from_TdS = 2*np.pi * C * KB * T_dS / HBAR
Z_from_TdS = C*H_LAM / a_from_TdS
print(f"""   The emission/Lamb-shift physics contains NO acceleration a0. The only scale it references is the
   de Sitter RATE H_Lambda (via T_dS). The 'acceleration whose Unruh temperature equals T_dS' is
       a = 2 pi c k_B T_dS / hbar = c H_Lambda = {a_from_TdS:.3e} m/s^2,  i.e. Z = {Z_from_TdS:.2f}  (the naive Z=1),
   which is ~{a_from_TdS/A0:.1f}x LARGER than the framework a0 and is EXCLUDED by the data band Z in [4.2, 6.0].
   So this route does NOT predict a0 = c^2 sqrt(Lambda/32pi); it predicts (at best) the wrong-by-6x Z=1 scale,
   and only by smuggling in the de Sitter temperature -- not from anything about the Einstein A coefficient.""")

# Evolution fork:
print(f"""
   EVOLUTION FORK:  whatever scale the bath sets tracks H(z), the *instantaneous* expansion rate that fixes the
   Gibbons-Hawking temperature of the apparent horizon. For a LCDM background:
       H(z)/H0 = sqrt(Om_m (1+z)^3 + OmL),  so T_GH(z) ~ H(z) RISES at high z (~ sqrt(rho_total)).
   The framework instead needs a0(z) ~ sqrt(rho_DE), tied to the FUTURE EVENT horizon (constant Lambda),
   which is FLAT then declines -- the OPPOSITE high-z behavior. Numbers at a few redshifts:""")
print(f"   {'z':>5}{'H(z)/H0':>12}{'sqrt(rho_tot)/now':>20}{'sqrt(rho_DE)/now':>20}")
for z in [0.0, 0.5, 1.0, 2.0, 3.0]:
    Hz = np.sqrt(Om_m*(1+z)**3 + OmL)              # in units of H0
    sqrt_rho_tot = Hz                               # rho_tot ~ H^2
    sqrt_rho_DE  = 1.0                               # rho_DE = const (cosmological constant) -> sqrt = 1
    print(f"   {z:>5.1f}{Hz:>12.3f}{sqrt_rho_tot:>20.3f}{sqrt_rho_DE:>20.3f}")
print(f"""
   => The de Sitter-bath / Gibbons-Hawking scale this route uses is ~ H(z) ~ sqrt(rho_total): RISING at high z.
      That is the DISFAVORED branch of the fork. It does NOT reproduce the framework's declining sqrt(rho_DE).
      (The asymptotic H_Lambda is constant, but the *thermal/horizon* temperature an atom sees redshifts with
       the real horizon, i.e. tracks H(z); either way you do not get a *declining* sqrt(rho_DE).)""")
print()

print("#"*100)
print("# BOTTOM LINE (spontaneous-emission route):")
print(f"#   predicted a0 from this route: NONE intrinsically; at most a = c H_Lam = {a_from_TdS:.2e} m/s^2 (Z=1), EXCLUDED.")
print(f"#   real physical effect on any A-coefficient: 1e-68 (Lamb) ... exp(-1e28) (emission) -- unobservable.")
print(f"#   a0 NEVER enters; only H_Lam does, as a thermal/curvature scale. Evolution ~ sqrt(rho_tot) (RISING) = wrong fork.")
print("#   GRADE: loose analogy + same-scale coincidence (shared Lambda, shared words 'spontaneous'/'vacuum'); NOT a derivation.")
print("#"*100)
