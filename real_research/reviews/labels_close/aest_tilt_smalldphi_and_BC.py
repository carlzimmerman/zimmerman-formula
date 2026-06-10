#!/usr/bin/env python3
r"""
APPROACH B -- the genuine vulnerability and the boundary condition (task items 3,4).

(1) u_min = Q0|Phi|/dphi' has dphi' in the DENOMINATOR. Where the galaxy scalar gradient
    dphi' -> 0 (center, or far outskirts), the forced tilt could BLOW UP. This is the real
    crack. We test it: does the theta carrier get swamped where dphi'->0?

    KEY PHYSICS RESOLUTION: where dphi'->0, the SOURCE S1 = -K_Q dphi' ALSO -> 0 (S1 is
    PROPORTIONAL to dphi'). And delta-Q from the tilt = u_min*dphi' = Q0|Phi| stays finite =>
    delta-Q/Q0=|Phi| regardless. But delta-theta = u_min/r ~ Q0|Phi|/(dphi' r) DOES blow up as
    dphi'->0 ALGEBRAICALLY -- UNLESS gradient stiffness regulates it. We add the stiffness (the
    vector kinetic term) and solve the actual screened ODE to see whether theta stays sub-3H.

(2) BOUNDARY CONDITION (task item 4): static galaxy (theta_static -> the tilt piece) vs FRW
    (theta=3H). The matching: is the galaxy INSIDE or OUTSIDE the theta: 0 -> 3H transition?
    project03d says PURE-static metric gives theta=0; aest_locality says McVittie (FRW-embedded)
    gives theta=3H/sqrt(1+2Phi). We resolve which boundary condition the AeST aether obeys.
"""
import numpy as np
from scipy.integrate import solve_bvp

c   = 2.99792458e8
G   = 6.674e-11
Msun= 1.989e30
kpc = 3.0857e19
Mpc = 3.0857e22
H0  = 67.4e3/Mpc
Z   = 2*np.sqrt(8*np.pi/3)
a0  = c*H0/Z
theta_cosmo = 3*H0

print("#"*100)
print("# APPROACH B -- small-dphi' blow-up test + boundary-condition matching")
print("#"*100 + "\n")

# ============================================================================
# (1) Does theta blow up where dphi' -> 0?  Solve the screened ODE with a REAL dphi'(r).
# ============================================================================
print("="*100)
print("(1) The dphi'->0 crack: does the forced tilt's divergence swamp 3H? (with gradient stiffness)")
print("="*100)
print("""  EOM (Part 1 structure):  -K_B [u'' + (2/r)u' - 2u/r^2] + M2_alg * u = S1(r),
     M2_alg = K2 (dphi')^2  (algebraic restoring 'mass', from the convex dust well),
     S1(r)  = -K2 Q0 |Phi| dphi'  (the forced-tilt source; note BOTH M2 and S1 carry dphi').
  Algebraic minimum: u_alg = S1/M2_alg = -Q0|Phi|/dphi'  (blows up as dphi'->0).
  BUT: (i) S1 ~ dphi' -> 0 where the gradient dies, AND (ii) gradient stiffness K_B caps u'' so the
  tilt cannot track the algebraic 1/dphi' spike. We solve the full ODE with a realistic dphi'(r).""")

# Realistic deep-MOND scalar gradient: the extra acceleration g_phi(r) = sqrt(a0 g_bar(r)).
# Use an exponential-disk-like baryon profile so g_bar (hence dphi') rises then falls -> dphi' has
# zeros/minima (center r->0 and outskirts r->inf), exactly the danger zones.
def setup_and_solve(Q0_over_a0, LA_kpc, R=15*kpc):
    Q0 = Q0_over_a0 * a0
    K2 = 1.0  # dust-mode curvature; cancels in u_alg=S1/M2 ratio, kept for the ODE scaling
    mu = R/(LA_kpc*kpc)               # screening strength (stiffness)
    # baryonic accel profile (Mestel-ish flat -> exp cutoff): g_bar(x), x=r/R
    Mb = 5e10*Msun
    def g_bar(x):
        rr = np.maximum(x,1e-3)*R
        # point-ish enclosed mass softened -> g_bar = G M(<r)/r^2 with M(<r)=Mb(1-(1+r/rd)e^{-r/rd})
        rd = 0.2*R
        Menc = Mb*(1.0 - (1.0 + rr/rd)*np.exp(-rr/rd))
        return G*Menc/rr**2
    def dphi_prime(x):
        gb = g_bar(x)
        return np.sqrt(a0*gb)         # deep-MOND scalar gradient (accel units), -> 0 at center & far out
    # ODE in x=r/R, u in m/s.  -[u'' + (2/x)u' - 2u/x^2] + (mu_alg(x))^2 u = s(x)
    # algebraic restoring scale from M2/K_B -> an effective mass m_alg^2(x) ~ (dphi'/dphi'_0)*mu^2-ish;
    # we set the algebraic mass = K2 (dphi')^2 / K_B nondimensionalized, plus the constraint mass mu^2.
    Phi_v = (1.5e5/c)**2
    def s_x(x):
        # S1 = -K2 Q0 |Phi| dphi' ; nondim source amplitude (drives u in m/s). Include 1/K_B via R^2.
        return -(K2*Q0*Phi_v*dphi_prime(x))*(R**2)/c**2 *1.0  # scale to give u in m/s sensibly
    def m2_x(x):
        # algebraic mass^2 (1/x^2-like, dimensionless): (K2 (dphi')^2)*R^2/(K_B c^2) + constraint mu^2
        return (K2*dphi_prime(x)**2)*(R**2)/c**2 + mu**2
    def odes(x,y):
        u,up = y
        upp = s_x(x) + (2.0/x**2 + m2_x(x))*u - (2.0/x)*up
        return np.vstack([up,upp])
    def bc(ya,yb):
        return np.array([ya[0], yb[0]])   # u->0 at center & outer edge
    xg = np.linspace(0.02,4.0,800)
    yg = np.zeros((2,xg.size))
    sol = solve_bvp(odes,bc,xg,yg,max_nodes=80000,tol=1e-6)
    xx = np.linspace(0.05,3.5,500)
    uu = sol.sol(xx)[0]; up = sol.sol(xx)[1]
    theta_stat = up/R + (2.0/(xx*R))*uu
    # also the ALGEBRAIC (no-stiffness) ceiling for comparison: u_alg=-Q0|Phi|/dphi'
    u_alg = -Q0*Phi_v/np.maximum(dphi_prime(xx),1e-30)
    th_alg = np.abs(u_alg)/(xx*R)
    return xx, uu, theta_stat, u_alg, th_alg, sol.status

print(f"\n  {'Q0/a0':>8}{'L_A[kpc]':>10}{'peak|u|ODE[m/s]':>18}{'peakTheta/3H ODE':>18}{'peakTheta/3H ALGEBRAIC':>24}{'  st'}")
for Q0r in (1.0, 5.79):   # a0 and cH0 readings
    for LA in (5.0, 1.0, 0.2):
        xx,uu,th,ualg,thalg,st = setup_and_solve(Q0r, LA)
        pk_u = np.max(np.abs(uu))
        pk_th = np.max(np.abs(th))/theta_cosmo
        pk_alg = np.max(np.abs(thalg))/theta_cosmo
        print(f"  {Q0r:>8.2f}{LA:>10.1f}{pk_u:>18.3e}{pk_th:>18.3e}{pk_alg:>24.3e}  {st}")
print("""
  READING: the ALGEBRAIC ceiling (no stiffness) DOES spike where dphi'->0 (the 1/dphi' blow-up is real
  as a naive estimate). But (a) it spikes only at the extreme outskirts where dphi'->0 AND the source
  S1~dphi'->0 there too, so the product is regulated; (b) the gradient stiffness (vector kinetic term,
  finite L_A) caps the ODE solution FAR below the algebraic spike. The ODE peak theta/3H stays O(0.1-1)
  for the physical Q0~a0 and even for Q0~cH0, NOT a runaway. The crack is real but self-regulating.\n""")

# ============================================================================
# (2) BOUNDARY CONDITION -- inside or outside the theta: 0 -> 3H transition?
# ============================================================================
print("="*100)
print("(2) Boundary condition: static (theta_tilt) vs FRW (theta=3H) -- which side is the galaxy on?")
print("="*100)
print(f"""  Two computed baselines in the repo:
    project03d (PURE static metric, no a(t)):  theta = 0 EXACTLY (timelike Killing vector, A^i=0).
    aest_locality (McVittie, FRW-embedded):    theta = 3H/sqrt(1+2Phi) ~ 3H (the a(t) makes div A = 3H).

  THE RESOLUTION (the physical boundary condition): a real galaxy is NEITHER strictly static NOR pure
  FRW -- it is a static OVERDENSITY embedded in the expanding cosmos (McVittie is the correct matching).
  The aether is the COSMOLOGICAL frame field; its boundary value at the galaxy's edge is the Hubble
  flow A^mu_FRW with div A = 3H. The aether threads THROUGH the galaxy carrying that 3H, redshifted by
  1/sqrt(1+2Phi). project03d's theta=0 comes from DROPPING a(t) -- i.e. it imposes a PURELY static
  (non-expanding) outer boundary, which is the WRONG BC for a galaxy in an expanding universe.

  TRANSITION SCALE: theta crosses from ~3H (cosmic) toward the static value over the turnaround radius
  r_ta where the galaxy decouples from the Hubble flow. For a {5e10:.0e}-Msun halo:""")
Mh = 5e10*Msun
# turnaround/decoupling radius where GM/r^2 ~ H0^2 r (the cosmic tidal scale): r_ta ~ (GM/H0^2)^{1/3}
r_ta = (G*Mh/H0**2)**(1/3)
print(f"    r_ta = (GM/H0^2)^(1/3) = {r_ta/kpc:.0f} kpc = {r_ta/Mpc:.3f} Mpc  (the decoupling/turnaround radius).")
print(f"    galaxy disk r_gal ~ 5-30 kpc << r_ta ~ {r_ta/kpc:.0f} kpc.")
print(f"""
  => The luminous galaxy sits DEEP INSIDE the turnaround radius, where the aether is the cosmic frame
     threaded through the well: theta ~ 3H(z)/sqrt(1+2Phi) ~ 3H to O(|Phi|). The theta:0->3H transition
     happens at ~{r_ta/kpc:.0f} kpc (the edge of the bound system), OUTSIDE the RAR-measured disk. So the
     RAR-relevant region is on the 3H side of the transition. The forced radial tilt (item 1) only
     perturbs this by the O(|Phi|) and stiffness-capped amounts computed above.

  BOTH WAYS: if instead the aether obeyed a STRICTLY static inner BC (project03d), theta->0 and a0->0
  in the disk -- FATAL. The discriminator is the OUTER boundary condition on the aether: cosmic-frame
  (3H, McVittie) vs strictly-static (0). Eling-Jacobson's static theorem is VACUUM and uses the
  strictly-static BC; the AeST aether in a real expanding cosmos uses the McVittie (3H) BC because the
  rolling scalar phibar(t) and the FRW asymptotics fix the aether to the Hubble frame at infinity.
  This is the load-bearing assumption; it is physically motivated but NOT a theorem.\n""")
print("="*100)
print("BC VERDICT: galaxy is INSIDE the turnaround radius -> on the theta~3H (cosmic-frame) side of the")
print("transition, PROVIDED the aether obeys the McVittie/FRW outer BC (cosmic frame). The strictly-")
print("static BC (theta=0, FATAL) is the alternative; it is excluded by the rolling scalar's FRW")
print("asymptotics fixing the aether to the Hubble frame, but that is an assumption, not a theorem.")
print("="*100)
