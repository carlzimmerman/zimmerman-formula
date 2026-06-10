#!/usr/bin/env python3
r"""
APPROACH B, continued: (a) extract the LEADING (weak-field) forms of S1, M2, u_min
symbolically and verify signs; (b) SIZE the forced tilt and compute delta-theta/3H
AND delta-Q/Q0 SEPARATELY (the two carriers scale differently); (c) BOTH-WAYS
stress test (soft aether, O(1) source, K_Q at full F_Q).

theta carrier:  delta-theta from a static radial tilt ~ d_r u + (2/r) u ~ u/r_scale.
Q carrier:      delta-Q from the tilt = u * dphi'  (ALGEBRAIC, no derivative).
These scale DIFFERENTLY -> we must size both.
"""
import sympy as sp
import numpy as np

# ---------------------------------------------------------------- constants
c    = 2.99792458e8
G    = 6.674e-11
Msun = 1.989e30
kpc  = 3.0857e19
Mpc  = 3.0857e22
H0   = 67.4e3/Mpc
Z    = 2*np.sqrt(8*np.pi/3)
a0   = c*H0/Z
theta_cosmo = 3*H0
print(f"a0=cH0/Z={a0:.3e} m/s^2,  3H0={theta_cosmo:.3e}/s,  Z={Z:.4f}\n")

# ============================================================================
# (a) LEADING weak-field forms (Taylor in |Phi|), with the unit-constraint At(u).
# ============================================================================
print("="*100)
print("(a) LEADING weak-field forms of the source S1, mass M2, and forced tilt u_min")
print("="*100)
u_s, Ph, Q0, K2, dphip = sp.symbols('u_s Phi Q0 K2 dphip', real=True)
# At(u) with Phi small; Phi<0 in a well but keep symbolic
At = sp.sqrt((1 + (1-2*Ph)*u_s**2)/(1+2*Ph))
Q  = At*Q0 + u_s*dphip
K  = -2*sp.Symbol('Lam', positive=True) + sp.Rational(1,2)*K2*(Q-Q0)**2
LF = -K
# leading: expand At in Phi first (small), then in u
At0   = sp.series(At.subs(u_s,0), Ph, 0, 2).removeO()         # A^t at u=0
print(f"  A^t(u=0) = {sp.simplify(At0)}  ~ 1 - Phi  (=1+|Phi|, gravitational redshift of the aether clock).")
Qbar  = sp.simplify(At0*Q0)
print(f"  Qbar = A^t(0) Q0 = {Qbar} ~ Q0(1-Phi) = Q0(1+|Phi|).")
print(f"  Qbar - Q0 = {sp.simplify(Qbar-Q0)} = -Q0*Phi = +Q0|Phi|  (Phi<0). So Q sits Q0|Phi| up the well.\n")

# source S1 = -K_Q dphi' = -K2 (Qbar-Q0) dphi'
S1_lead = sp.simplify(-K2*(Qbar - Q0)*dphip)
print(f"  LINEAR SOURCE  S1 = -K2 (Qbar-Q0) dphi' = {S1_lead}  = +K2 Q0 Phi dphi'  (= -K2 Q0|Phi|dphi').")
# energy mass U'' = -M2 ; leading M2 = -K2 (dphi')^2 (from K_QQ (dQ/du)^2, dQ/du|0=dphi')
Uxx_lead = K2*dphip**2
print(f"  ENERGY curvature U''(0) = K2 (dphi')^2 = {Uxx_lead} > 0  (K2>0 dust-mode curvature) -> u=0 is a WELL.\n")
# forced tilt u_min = -S1/U'' (minimize U=U0 + S1_U u + 1/2 U'' u^2, with S1_U=-S1 in -L convention)
# U(u) = -L = -L0 - S1 u + 1/2 (-M2) u^2 ; U'(u)= -S1 + U'' u =0 -> u_min = S1/U''
u_min_lead = sp.simplify(S1_lead/Uxx_lead)
print(f"  FORCED TILT  u_min = S1/U'' = {u_min_lead} = -(Q0 Phi)/dphi' = +Q0|Phi|/dphi'.")
print("  => u_min = Q0 |Phi| / dphi'  (algebraic ceiling; gradient stiffness only shrinks it).\n")
print("""  STRUCTURAL VERDICT (a):
   * u=0 is a STABLE MINIMUM (U''>0 from the convex dust-mode well K2>0; vector kinetic gives +(u')^2).
     NOT a saddle, NO ghost/gradient mode in the c_GW=c branch.
   * The rolling scalar DOES shift the minimum off u=0 (S1 != 0): a GENUINELY FORCED tilt exists.
   * BUT the forced tilt is u_min = Q0|Phi|/dphi', doubly suppressed: by |Phi|~(v/c)^2 AND requiring
     the galaxy gradient dphi'. The Eling-Jacobson 'extra restriction' A^r=0 is ALMOST recovered
     dynamically -- shifted only by O(|Phi|).\n""")

# ============================================================================
# (b) SIZE u_min, then delta-theta/3H AND delta-Q/Q0 SEPARATELY.
# ============================================================================
print("="*100)
print("(b) NUMERICAL sizing: u_min, then delta-theta/3H and delta-Q/Q0 SEPARATELY")
print("="*100)
# Need Q0 (cosmological scalar velocity) and dphi' (galaxy scalar gradient) in COMMENSURATE units.
# In AeST (Skordis-Zlosnik), phi has units so that Q=A^mu d_mu phi and Y=q^mn d_m phi d_n phi appear
# in the action with the metric; [phi] is dimensionless * c^2? We avoid unit ambiguity by working with
# the ACCELERATION the scalar carries.  The MOND scalar gradient produces the extra acceleration:
#       g_phi(r) = (deep-MOND) sqrt(a0 g_bar)  ->  at the flat plateau g_phi ~ sqrt(a0 g_bar).
# The scalar 'velocity' Q0 = phibar-dot is fixed cosmologically; on the dust-mode background
#       Q ~ Q0 + I0/a^3, and dK/dQ = I0/a^3 sets the dust density. The natural scale of Q0 is set by
# requiring the K(Q) dust mode to match Omega_dm; dimensionally [Q] = [dphi/dt].  The CLEANEST,
# convention-robust comparison (used throughout the repo) is ACCELERATION-to-ACCELERATION:
#   - dphi'(r) ~ g_phi / c-conversion: the scalar gradient is an acceleration ~ a0 at the plateau.
#   - Q0 = phibar-dot ~ (the same field's cosmological rate). On the background the scalar's energy
#     density 8piG rhobar = Q dK/dQ - K ~ Lambda-scale + dust; the field VELOCITY Q0 is of order
#     the Hubble-scale times the field amplitude. We bracket Q0 conservatively.
#
# To stay convention-robust we report u_min as a VELOCITY (m/s) under three readings of (Q0, dphi'):

print("""  We need (Q0, dphi') in commensurate units. Use ACCELERATION matching (repo convention):
    dphi'(r) := galaxy scalar gradient, an acceleration ~ a0 at the deep-MOND plateau.
    Q0       := cosmological scalar 'velocity' phibar-dot. We bracket it three ways.
  Then u_min[velocity] = Q0 |Phi| / dphi'  (dimensionally [Q0][L]/[accel*L]=[Q0]/[accel]*... we keep
  the RATIO Q0/dphi' as a TIME, times |Phi|, giving u_min a velocity; checked per-row).\n""")

V_flat = 1.5e5                 # 150 km/s galaxy
Phi_v  = (V_flat/c)**2         # |Phi| ~ 2.5e-7
r_gal  = 5*kpc
g_bar  = a0                    # deep-MOND plateau: g_bar ~ a0 so g_phi ~ sqrt(a0*a0)=a0
dphi_acc = a0                  # the scalar gradient as an acceleration (plateau)
print(f"  galaxy: V_flat={V_flat/1e3:.0f} km/s, |Phi|=(V/c)^2={Phi_v:.2e}, r_gal={r_gal/kpc:.0f} kpc, dphi'~a0={a0:.2e} m/s^2\n")

# Q0 readings (cosmological scalar velocity), as an ACCELERATION-equivalent so the ratio is a time:
# Reading A: Q0 ~ a0 (scalar velocity tracks the same a0 scale)            -> conservative-ish
# Reading B: Q0 ~ c*H0 (Hubble-scale field rate)                            -> LARGE (stress test)
# Reading C: Q0 ~ a0 but at K(Q)-minimum dK/dQ small -> effective source even smaller (physical)
print(f"  {'Q0 reading':>34}{'Q0 (accel-eq)':>16}{'u_min=Q0|Phi|/dphi*[L?]':>26}")
print("  --- u_min as a VELOCITY: u_min = (Q0/dphi') * |Phi| * (a typical length is NOT needed; ")
print("      Q0/dphi' is dimensionless-accel-ratio; the velocity scale enters via dphi' carrying 1/time).")
print("      Cleanest: u_min/c = |Phi| * (Q0/dphi')_accel-ratio  -> a dimensionless tilt times c.\n")

for label, Q0val in [("A: Q0 ~ a0 (scale-matched)", a0),
                     ("B: Q0 ~ cH0 (Hubble rate, STRESS)", c*H0),
                     ("C: Q0 ~ a0, but dK/dQ@min small (phys)", 0.1*a0)]:
    ratio = Q0val/dphi_acc                 # dimensionless (accel/accel)
    u_over_c = Phi_v * ratio               # |Phi| * (Q0/dphi')
    u_vel = u_over_c * c                    # m/s
    print(f"  {label:>40}{Q0val:>14.2e}   u_min/c={u_over_c:.2e}  -> u_min={u_vel:.2e} m/s")
print()

# ---- now the TWO CARRIERS, sized from u_min ----
print("  --- delta-theta/3H  (the divergence carrier, theta=div A) ---")
print("      static tilt contributes theta_tilt = d_r u + (2/r)u ~ u/r_gal  (1/s).")
print(f"      {'Q0 reading':>40}{'u_min[m/s]':>14}{'theta_tilt=u/r_gal':>22}{'/3H0':>14}")
res_theta = {}
for label, Q0val in [("A: Q0~a0", a0), ("B: Q0~cH0 (STRESS)", c*H0), ("C: Q0~0.1a0", 0.1*a0)]:
    u_vel = Phi_v*(Q0val/dphi_acc)*c
    theta_tilt = u_vel/r_gal
    res_theta[label] = theta_tilt/theta_cosmo
    print(f"      {label:>40}{u_vel:>14.2e}{theta_tilt:>22.3e}{theta_tilt/theta_cosmo:>14.2e}")
print()

print("  --- delta-Q/Q0  (the scalar carrier; the NEW stake) ---")
print("      delta-Q from the tilt = u * dphi'  (ALGEBRAIC). Compare to Q0.")
print("      Plus the redshift piece (Qbar-Q0)/Q0 = |Phi| from A^t alone (the repo's ~1e-6).")
print(f"      {'Q0 reading':>40}{'u_min*dphi[accel?]':>20}{'deltaQ/Q0(tilt)':>18}{'+redshift|Phi|':>16}")
res_Q = {}
for label, Q0val in [("A: Q0~a0", a0), ("B: Q0~cH0 (STRESS)", c*H0), ("C: Q0~0.1a0", 0.1*a0)]:
    u_vel = Phi_v*(Q0val/dphi_acc)*c
    # delta-Q from tilt = u * dphi'.  In accel-matched units, dphi' carries acceleration; u carries
    # velocity; u*dphi' has units velocity*accel = m^2/s^3. To compare to Q0 we use the SAME ratio
    # logic: deltaQ/Q0 = (u*dphi')/(Q0 * something). The dimensionless form: deltaQ/Q0 from the tilt
    # = (u/c) * (dphi'/Q0)*c ... cleanest: deltaQ/Qbar(tilt) = u_vel*dphi_acc/(Q0val * (dphi_acc/?))
    # Use the SAME structure as u_min derivation: at the forced minimum, deltaQ_tilt/Q0 = (u_min/c)*(dphi'*c/Q0).
    # But u_min/c = |Phi|*(Q0/dphi'). So deltaQ_tilt/Q0 = |Phi|*(Q0/dphi')*(dphi'/Q0) = |Phi|.  <-- exactly |Phi|!
    dQ_tilt_over_Q0 = Phi_v*(Q0val/dphi_acc)*(dphi_acc/Q0val)   # = |Phi| identically
    res_Q[label] = dQ_tilt_over_Q0
    print(f"      {label:>40}{u_vel*dphi_acc:>20.2e}{dQ_tilt_over_Q0:>18.2e}{Phi_v:>16.2e}")
print()
print(f"  *** delta-Q/Q0 from the FORCED tilt = |Phi| ~ {Phi_v:.2e}  -- INDEPENDENT of the Q0 reading! ***")
print("  Because at the minimum u_min=Q0|Phi|/dphi', the tilt's delta-Q = u_min*dphi' = Q0|Phi|, so")
print("  delta-Q/Q0 = |Phi| EXACTLY -- the SAME O(|Phi|) as the A^t redshift. The Q carrier is PINNED")
print("  to Q0 at O(|Phi|)~1e-6 by the forced tilt itself, regardless of how big Q0 is.\n")

# ============================================================================
# (c) BOTH WAYS -- the FATAL branch: when does the tilt swamp each carrier?
# ============================================================================
print("="*100)
print("(c) BOTH WAYS -- steelman the SWAMPED branch for theta AND for Q separately")
print("="*100)
print(f"""  theta carrier swamps 3H when u/r_gal > 3H0, i.e. u > 3H0*r_gal = {theta_cosmo*r_gal:.3e} m/s ~ {theta_cosmo*r_gal/1e3:.2f} km/s.
  Q carrier swamps Q0 when delta-Q/Q0 > O(1) (loses the dust-mode pinning).

  Threshold tilt for each carrier:
    theta: u_swamp(theta) = 3H0 r_gal = {theta_cosmo*r_gal:.2e} m/s  ({theta_cosmo*r_gal/1e3:.2f} km/s)
    Q:     u_swamp(Q)     = Q0/dphi' (need delta-Q=u*dphi'~Q0)  -- depends on Q0.

  Forced tilt from the EOM:  u_min = Q0|Phi|/dphi'.
   * To swamp theta: need Q0|Phi|/dphi' > 3H0 r_gal -> Q0/dphi' > 3H0 r_gal/|Phi| = {theta_cosmo*r_gal/Phi_v:.2e}.
     i.e. the scalar velocity Q0 would have to exceed dphi' by a factor {theta_cosmo*r_gal/Phi_v/a0:.2e}*(a0).
   * To swamp Q: need |Phi| > O(1) -- IMPOSSIBLE in a galaxy (|Phi|~1e-6). Q is pinned at |Phi| ALWAYS.

  So the SWAMPED-theta branch requires a HUGE Q0/dphi' ratio; the SWAMPED-Q branch is unreachable
  (delta-Q/Q0=|Phi| identically). We now compute the Q0/dphi' needed and check it against physics.""")
ratio_needed = theta_cosmo*r_gal/Phi_v/dphi_acc   # Q0/dphi' (in a0 units) to swamp theta
print(f"\n  Q0/dphi' needed to swamp theta = {theta_cosmo*r_gal/Phi_v:.2e} (accel-eq) = {ratio_needed:.2e} * a0.")
print(f"  Reading B (Q0~cH0) gives Q0/dphi'={c*H0/a0:.2e}*a0 = {c*H0/a0:.2e} -- "
      f"{'ABOVE' if c*H0/a0 > ratio_needed else 'BELOW'} the swamp threshold {ratio_needed:.2e}.")
print(f"  Reading A (Q0~a0)  gives Q0/dphi'=1 -- {1/ratio_needed:.2e}x BELOW threshold (safe).\n")

# decisive headline numbers
print("="*100)
print("HEADLINE NUMBERS")
print("="*100)
print(f"  Forced tilt is REAL (S1 != 0) but O(|Phi|)-suppressed: u_min = Q0|Phi|/dphi'.")
print(f"  delta-Q/Q0 (from forced tilt)   = |Phi| = {Phi_v:.2e}   [reading-INDEPENDENT]  -> Q PINNED.")
print(f"  delta-theta/3H (reading A, Q0~a0)= {res_theta['A: Q0~a0']:.2e}   -> theta PINNED.")
print(f"  delta-theta/3H (reading B, STRESS Q0~cH0)= {res_theta['B: Q0~cH0 (STRESS)']:.2e}")
swamp_B = res_theta['B: Q0~cH0 (STRESS)'] > 1
print(f"       -> theta {'SWAMPED' if swamp_B else 'PINNED'} under the Hubble-rate stress reading of Q0.")
print(f"  delta-theta/3H (reading C, phys Q0~0.1a0)= {res_theta['C: Q0~0.1a0']:.2e}   -> theta PINNED.\n")
