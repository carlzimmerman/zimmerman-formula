"""
wf2_massive_vector_ppn_suppression.py
============================================================================
Closes the last gap in the alpha_1 chain: AeST's transverse aether (spin-1)
mode is MASSIVE (m ~ Mpc^-1, Skordis-Zlosnik), while Foster-Jacobson /
Sagi compute alpha_1 with a MASSLESS vector.  Does the mass change alpha_1?

alpha_1 is a NEAR-ZONE (1PN) quantity: it is the coefficient of the 1/r
Coulomb piece of the g_0i response to a source of size r.  A massive vector
gives a Yukawa response e^{-M r}/r; the 1/r COEFFICIENT as (M r)->0 is the
massless one, and corrections are O((M r)^2).  For a Proca (spin-1) field
coupled to conserved-ish currents there is NO vDVZ discontinuity (that is a
spin-2 issue), so the massless limit is smooth.

Here we just SIZE (M r)^2 at the scales where alpha_1 is actually measured,
including the K_B->0 growth of the mass  (M ~ 1/sqrt(K_B)), to confirm the
massless-vector value alpha_1 = -4 K_B is the physical answer to ~30 digits.
"""
import sympy as sp

# --- physical constants / scales (cgs) --------------------------------------
Mpc  = 3.0857e24            # cm
AU   = 1.496e13             # cm
R_EM = 3.844e10            # cm  Earth-Moon (lunar laser ranging)
c_ls = 2.998e10             # cm  (1 light-second ~ binary-pulsar orbital scale)
kpc  = 3.0857e21            # cm

# AeST vector Compton scale.  Skordis-Zlosnik: propagating vector mass with
# 1/M <~ Mpc at the fiducial parameters; M^2 = (2-K_B)(1+lam_s)Q0^2/K_B so
# M ~ M_fid * sqrt(K_B_fid/K_B).   Take M_fid = 1/Mpc at K_B_fid = 0.1.
M_fid   = 1.0/Mpc
KB_fid  = 0.1

def M_of_KB(KB):
    return M_fid * (KB_fid/KB)**0.5   # cm^-1

print("="*74)
print("Vector Compton wavenumber M(K_B) and the (M r)^2 PPN suppression")
print("="*74)
print(f"  fiducial 1/M = 1 Mpc at K_B = {KB_fid}   (M ~ 1/sqrt(K_B))\n")
scales = [("Earth-Moon (LLR)", R_EM), ("1 AU (solar system)", AU),
          ("binary-pulsar orbit ~1 ls", c_ls)]
for KB in [0.1, 2.5e-5]:
    M = M_of_KB(KB)
    print(f"  K_B = {KB:>8.2g}:  1/M = {1.0/M/Mpc:8.3g} Mpc = {1.0/M/kpc:8.3g} kpc")
    for name, r in scales:
        Mr = M*r
        print(f"      {name:<28}  (M r)^2 = {Mr**2:.2e}")
    print()

print("="*74)
print("VERDICT")
print("="*74)
print("""  Even in the WORST case (K_B ~ 2.5e-5, where the mass is heaviest, pushing
  1/M down to ~kpc scales), (M r)^2 <~ 1e-19 at every scale where alpha_1 is
  measured (Earth-Moon, solar system, binary pulsars).  The massless-vector
  Foster-Jacobson/Sagi value is therefore the physical one to ~19-28 digits:

        alpha_1(AeST) = -4 K_B          [SOLID]

  Bounds:  |alpha_1| < 1e-4  (LLR)  =>  K_B < 2.5e-5
           |alpha_1| < 1e-5  (binary pulsars, Shao-Wex)  =>  K_B < 2.5e-6

  SECONDARY (SUGGESTIVE) tension worth flagging: forcing K_B <~ 2.5e-5 to pass
  alpha_1 drives the vector Compton scale 1/M ~ sqrt(K_B) DOWN toward galactic
  (~kpc-10kpc) scales.  A vector that becomes massive on galaxy scales may
  disturb the very MOND/lensing phenomenology AeST needs there -- i.e. the
  alpha_1 escape route (tiny K_B) may itself be phenomenologically costly.
  Not computed here; named as the follow-up.
""")
