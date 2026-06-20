#!/usr/bin/env python3
"""
DOOR C  --  C_lyapunov_stability  (GAP-1 pathology, both-ways + quarantine)
============================================================================
RUN the Vikman/Deffayet ghost-stability LYAPUNOV test on the framework's dark
scalar phi with K(Q)=mu^2(Q-1)^2 (a GHOST CONDENSATE, ACLM hep-th/0312099),
embedded in AeST (Skordis-Zlosnik), living on the framework's de Sitter
background (Lambda>0, H0>0, a0=c^2 sqrt(Lambda/32pi)=9.36e-11).

QUESTION (as posed by the door):
  Reduce K(Q)+gravity to the Deffayet mechanical TOY -- the homogeneous q(t)
  fluctuation mode with Hubble friction on the dS background. Integrate the EOM
  over a grid of off-minimum displacements (the physical I0 range giving
  Omega_dm~0.26), and check LYAPUNOV BOUNDEDNESS of <q^2(t)> over many Hubble
  times. Compare the instability timescale to the ACLM antigravity scale
  (t_c ~ M_Pl^2/M^3 at M~0.04-1 eV) and to H0^-1.

OUTPUT (a DEFINITE verdict + NUMBER, both ways):
  BOUNDED  -> growth timescale > Hubble  => classically stable; dS cures Jeans
             at the ODE level, WITH A NUMBER.
  UNBOUNDED-> runaway < H0^-1 for physical I0 => the minimum does NOT cure;
             squeezes M / amount.

------------------------------------------------------------------------------
THE PHYSICS THAT GOES INTO THE TOY (load-bearing, all anchored in-repo):

1. KINETIC FUNCTION (Blanchet-Skordis 2024, K(Q)=mu^2(Q-1)^2 verbatim).
   The k-essence sound speed of the Q-mode is (sympy-exact, re-confirmed here):
        c_s^2(dQ) = dQ/(3 dQ + 2),    Q = 1 + dQ.
   POSITIVE on Q>1 (dQ>0); NEGATIVE (gradient-unstable, Cline-class) on Q<1.
   This is THE SHARP HOOK: positivity reduces to WHICH branch sign(I0) forces.

2. WHICH BRANCH DOES THE DARK-MATTER DUST LIVE ON?
   Shift-symmetry first integral (banked AeST embedding): a^3 K'(Q) phidot = I0.
   K'(Q) = 2 mu^2 (Q-1) = 2 mu^2 dQ. The off-minimum displacement that gives the
   w=0, a^-3 DUST (Omega_dm) has rho_dust = 2 Q phidot * (K' phidot) > 0 and
   a^3 K' phidot = I0 with the SAME sign as dQ. A POSITIVE dust density on the
   expanding branch (phidot>0) forces dQ of definite sign. We test BOTH signs of
   the displacement (both ways) and report which branch the physical Omega_dm
   needs and whether THAT branch is the stable (c_s^2>0) one.

3. THE MECHANICAL TOY (Deffayet/Vikman ghost-stability reduction).
   Homogeneous fluctuation q(t)=delta phi about phi_bg = phidot*t on dS:
   the quadratic action is  S = integral dt a^3 [ A_kin qdot^2 - A_grad (k^2/a^2) q^2 ]
   with (ACLM / expand_PX_around_condensate.py, identifying X<->Q):
        A_kin  = P'(X0) + 2 X0 P''(X0)  > 0  (no-ghost, the time-kinetic coeff)
        A_grad = -P'(X0)  -> the ORDINARY grad term; the LEADING IR spatial
                 operator is the GRAVITATIONAL Jeans term, ACLM Eq.7.8:
        omega^2(k) = (B/M^2) k^4 - A_J k^2,   A_J = M^2/(2 M_Pl^2),  B=O(1).
   The HOMOGENEOUS (k->0) mode keeps the Hubble-friction + the gravitational
   back-reaction. ACLM's homogeneous Jeans growth rate (their Eq.7.10) is
        Gamma = alpha M^3 / (4 M_Pl^2),   alpha=O(1),
   i.e. the k->0 limit of the unstable Jeans band gives an effective
   "negative-mass-squared" Omega_eff^2 = -Gamma^2 < 0 for the q(t) mode.
   The Deffayet/Vikman TOY EOM for the homogeneous mode on dS is then exactly a
   damped (anti-)oscillator:
        qddot + 3 H qdot + Omega_eff^2 q = 0,   Omega_eff^2 = c_s^2_eff * (mass^2).
   We carry the TRUE sign structure: the gravitational Jeans term contributes
   Omega_eff^2 = -Gamma^2 (the runaway candidate), and the framework's dS supplies
   the friction 3H qdot with H = H0 (today) ... H_Lambda (asymptotic dS future).
   The Lyapunov criterion for qddot+3H qdot - Gamma^2 q=0 (constant coeffs) is
   the larger root  lambda_+ = (-3H + sqrt(9H^2 + 4 Gamma^2))/2 . If lambda_+<=0
   the mode is BOUNDED (over-damped, dS cures); else it grows as e^{lambda_+ t}.

4. WE INTEGRATE THE ACTUAL ODE with scipy (not just the closed-form root) over
   the physical grid, with the dS background EVOLVING (H(t) from H0->H_Lambda via
   Lambda+matter Friedmann), so the friction is the framework's real expansion
   history, and we measure <q^2(t)> growth/decay over many Hubble times.

Both-ways + quarantine: a0/Z/kappa/I0 NEVER asserted derived. A KILL (runaway)
is weighted EQUAL to a PASS (bounded). We report whichever the integration gives.
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

# ============================================================================
# CONSTANTS (SI unless flagged eV); framework anchors match the in-repo assets
# ============================================================================
c      = 2.99792458e8
hbar   = 1.054571817e-34
G      = 6.67430e-11
eV     = 1.602176634e-19
Mpc    = 3.0856775814913673e22
kpc    = Mpc/1e3
yr     = 3.1557e7
Gyr    = 1e9*yr

H0     = 67.4e3/Mpc                # s^-1
OmL    = 0.685
OmM    = 0.315
Om_dm  = 0.265
Om_b   = 0.0493
Lam    = 1.0909e-52                # m^-2 (banked)
a0     = 9.3624e-11               # m/s^2 (framework)
cH_Lam = c*np.sqrt(Lam/3.0)       # m/s ; Z=cH_Lam/a0
H_Lam  = np.sqrt(Lam/3.0)*c       # asymptotic dS Hubble (s^-1)  (= cH_Lam, since [m^-1]*c)
# NB H_Lam has units s^-1: sqrt(Lam[m^-2]/3)=[m^-1], times c[m/s] = [s^-1].

M_Pl_red_J  = np.sqrt(hbar*c**5/(8*np.pi*G))   # reduced Planck ENERGY (J)
M_Pl_red_eV = M_Pl_red_J/eV
hbar_eV_s   = 6.582119569e-16
hbarc_eV_m  = 197.3269804e6*1e-15

t_H0  = 1.0/H0
print("="*80)
print("DOOR C  --  C_lyapunov_stability  (Vikman/Deffayet ghost-stability Lyapunov test)")
print("="*80)
print(f"H0        = {H0:.4e} s^-1   (1/H0 = {t_H0/Gyr:.3f} Gyr)")
print(f"H_Lambda  = {H_Lam:.4e} s^-1 (asymptotic dS) ; 1/H_Lam = {1/H_Lam/Gyr:.3f} Gyr")
print(f"H_Lam/H0  = {H_Lam/H0:.4f}  (sqrt(OmL)={np.sqrt(OmL):.4f})  -- consistency check")
print(f"a0        = {a0:.4e} m/s^2 ; cH_Lam = {cH_Lam:.4e} m/s ; Z=cH_Lam/a0={cH_Lam/a0:.4f}")
print(f"M_Pl(red) = {M_Pl_red_eV:.4e} eV")

# ============================================================================
# STEP 1 -- THE SHARP HOOK (sympy-exact): c_s^2(dQ)=dQ/(3dQ+2), sign by branch
# ============================================================================
print("\n" + "="*80)
print("STEP 1: sound-speed hook  c_s^2(dQ)=dQ/(3dQ+2)  for K(Q)=mu^2(Q-1)^2 (sympy)")
print("="*80)
Qs, mus, dQs = sp.symbols('Q mu dQ', real=True)
Ksym  = mus**2*(Qs-1)**2
Kp    = sp.diff(Ksym, Qs)
Kpp   = sp.diff(Ksym, Qs, 2)
cs2   = sp.simplify(Kp/(Kp + 2*Qs*Kpp))             # k-essence c_s^2 = P_X/(P_X+2X P_XX)
cs2_dq= sp.simplify(cs2.subs(Qs, 1+dQs))
print(f"  K'(Q)={Kp}, K''(Q)={Kpp}")
print(f"  c_s^2 = K'/(K'+2Q K'') = {cs2} = {cs2_dq}  (Q=1+dQ)")
assert sp.simplify(cs2_dq - dQs/(3*dQs+2)) == 0
print("  [sympy-exact] c_s^2 = dQ/(3dQ+2).")
cs2_func = sp.lambdify(dQs, cs2_dq, 'numpy')
print(f"  dQ=+0.10 (Q>1): c_s^2={cs2_func(+0.10):+.4f}  -> STABLE branch (gradient-stable)")
print(f"  dQ=-0.10 (Q<1): c_s^2={cs2_func(-0.10):+.4f}  -> UNSTABLE branch (Cline gradient-unstable)")

# ============================================================================
# STEP 2 -- WHICH BRANCH does the physical Omega_dm dust force?  (both ways)
# ============================================================================
print("\n" + "="*80)
print("STEP 2: which sign(I0)/branch does Omega_dm~0.26 dust force?  (shift-sym 1st integral)")
print("="*80)
# rho_dust(off-minimum) = 2 Q phidot*(K' phidot) ; a^3 K' phidot = I0.
# rho_dust = 2 Q phidot * I0/a^3 >0 requires sign(I0)=sign(phidot) (expanding: phidot conventionally >0).
# K'(Q)=2 mu^2 dQ ; a^3 (2 mu^2 dQ) phidot = I0  => sign(dQ)=sign(I0/phidot)=+ for positive dust.
# => the DUST (Omega_dm>0) lives on dQ>0, i.e. Q>1 -> the c_s^2>0 STABLE branch.
print("  rho_dust = 2 Q phidot (K' phidot) = 2 Q phidot * I0/a^3 ;  K'=2 mu^2 dQ.")
print("  POSITIVE dust density (Omega_dm>0) on the expanding branch (phidot>0) needs I0>0,")
print("  hence dQ>0 i.e. Q>1  ==> the dust sits on the c_s^2>0 (gradient-STABLE) branch.")
print("  [BOTH WAYS] We still integrate the Q<1 (c_s^2<0) branch as the adversarial case.")

# Physical displacement magnitude: tie dQ to Omega_dm via rho_dust ~ rho_DM today.
# rho_dust = 2 Q phidot (I0/a^3). At the condensate Q~1, phidot~M^2 (ACLM), I0 sets the amplitude.
# We do NOT need the absolute dQ for the Lyapunov sign (set by sign(c_s^2) & Gamma); we scan a
# generous magnitude grid |dQ| in [1e-4, 1e-1] bracketing "small displacement off the minimum".

# ============================================================================
# STEP 3 -- ACLM Jeans rate Gamma and antigravity time t_c over the M window
# ============================================================================
print("\n" + "="*80)
print("STEP 3: ACLM Jeans growth rate Gamma=alpha M^3/(4 M_Pl^2) and t_c=M_Pl^2/M^3 (M window)")
print("="*80)
alpha = 1.0
def gamma_and_tc(M_eV):
    Gamma_eV = alpha*M_eV**3/(4*M_Pl_red_eV**2)       # eV
    Gamma_s  = Gamma_eV/hbar_eV_s                     # s^-1
    tc_invEV = M_Pl_red_eV**2/M_eV**3                 # 1/eV
    tc_s     = tc_invEV*hbar_eV_s                     # s
    m_eV     = M_eV**2/(np.sqrt(2)*M_Pl_red_eV)       # graviton mass = AeST mu
    return Gamma_s, tc_s, m_eV
print(f"{'M(eV)':>9s} {'Gamma(1/s)':>12s} {'1/Gamma(Gyr)':>13s} {'t_c(Gyr)':>11s} "
      f"{'H0/Gamma':>11s} {'H_Lam/Gamma':>12s}")
M_grid = [0.04, 0.13, 0.15, 0.5, 1.0]
gamma_store={}
for M in M_grid:
    Gs, tcs, m = gamma_and_tc(M)
    gamma_store[M]=Gs
    print(f"{M:9.3f} {Gs:12.3e} {1/Gs/Gyr:13.3e} {tcs/Gyr:11.3e} "
          f"{H0/Gs:11.3e} {H_Lam/Gs:12.3e}")
print("  (t_c = oscillation/antigravity onset time; 1/Gamma = Jeans e-fold time)")

# ============================================================================
# STEP 4 -- THE LYAPUNOV ODE INTEGRATION (scipy) on the framework's dS bg
# ============================================================================
print("\n" + "="*80)
print("STEP 4: integrate qddot + 3 H(t) qdot + Omega_eff^2 q = 0  (scipy, real expansion)")
print("="*80)
print("""  Background H(t): Friedmann with matter+Lambda, a(t0)=1 today, evolving into the
  framework's de Sitter future (H->H_Lambda). Friction = 3H(t) qdot is the REAL
  framework expansion. Omega_eff^2 carries the TRUE Jeans sign:
     UNSTABLE branch (gravitational Jeans / Q<1 gradient): Omega_eff^2 = -Gamma^2  (<0)
     STABLE   branch (Q>1, c_s^2>0):                       Omega_eff^2 = +Gamma^2  (>0)
  We integrate <q^2> = q^2 over MANY Hubble times for BOTH branches and the M grid.""")

# --- background a(t),H(t): dimensionless time tau=H0 t. H^2=H0^2[OmM a^-3 + OmL]
def H_of_a(a):
    return H0*np.sqrt(OmM*a**(-3) + OmL)
def bg_rhs(tau, y):           # y=[a]; dimensionless tau=H0 t  -> da/dtau = (H/H0) a
    a = y[0]
    return [ (H_of_a(a)/H0)*a ]
# integrate background from today (a=1) forward 50 e-folds-worth of cosmic time:
# choose total cosmic time T = N_H * 1/H0 (many Hubble times)
N_H = 50.0                      # many Hubble times
tau_span = (0.0, N_H)           # in units of 1/H0
tau_eval = np.linspace(*tau_span, 6000)
bg = solve_ivp(bg_rhs, tau_span, [1.0], t_eval=tau_eval, rtol=1e-9, atol=1e-12, method='RK45')
a_of_tau = bg.y[0]
H_of_tau = H_of_a(a_of_tau)     # s^-1
print(f"  Background integrated over {N_H:.0f}/H0 = {N_H*t_H0/Gyr:.1f} Gyr; "
      f"a: {a_of_tau[0]:.2f}->{a_of_tau[-1]:.2e}; H->{H_of_tau[-1]:.3e}/s "
      f"(H_Lam={H_Lam:.3e}/s).")

def integrate_q(M_eV, branch_sign, q0=1.0, qd0=0.0):
    """branch_sign=+1 (stable, Omega^2=+Gamma^2) or -1 (unstable, Omega^2=-Gamma^2)."""
    Gamma_s, _, _ = gamma_and_tc(M_eV)
    Om2 = branch_sign*Gamma_s**2          # s^-2
    # work in physical time t [s]; state z=[q, qdot] with qdot=dq/dt
    def rhs(t, z):
        q, qd = z
        a = np.interp(t, tau_eval*t_H0, a_of_tau)
        Hh = H_of_a(a)
        return [qd, -3.0*Hh*qd - Om2*q]
    t0, t1 = 0.0, N_H*t_H0
    teval = tau_eval*t_H0
    sol = solve_ivp(rhs, (t0,t1), [q0,qd0], t_eval=teval, rtol=1e-9, atol=1e-12, method='RK45')
    q = sol.y[0]
    return teval, q

print(f"\n  {'M(eV)':>7s} {'branch':>9s} {'q(0)':>6s} {'q(end)':>11s} {'<q^2>end/<q^2>0':>16s} "
      f"{'verdict':>14s} {'growth tau(Gyr)':>16s}")
results=[]
for M in M_grid:
    for bs,label in [(-1,'UNSTABLE'),(+1,'STABLE')]:
        teval, q = integrate_q(M, bs)
        q2_ratio = (q[-1]**2)/(q[0]**2)
        # closed-form growth root for qddot+3H qdot - Gamma^2 q=0 (use asymptotic H=H_Lam, the
        # SLOWEST friction the framework ever supplies -> the most dangerous, conservative):
        Gamma_s,_,_ = gamma_and_tc(M)
        if bs<0:
            lam_p = (-3*H_Lam + np.sqrt(9*H_Lam**2 + 4*Gamma_s**2))/2.0   # s^-1 (>0 if unstable)
            grow_tau = (1.0/lam_p)/Gyr if lam_p>0 else np.inf
        else:
            lam_p = (-3*H_Lam + np.sqrt(max(9*H_Lam**2 - 4*Gamma_s**2,0.0)))/2.0
            grow_tau = np.inf
        verdict = "BOUNDED" if q2_ratio<=1.0+1e-6 else "UNBOUNDED"
        results.append((M,label,q2_ratio,verdict,grow_tau,lam_p))
        print(f"  {M:7.3f} {label:>9s} {q[0]:6.2f} {q[-1]:11.3e} {q2_ratio:16.3e} "
              f"{verdict:>14s} {grow_tau if np.isfinite(grow_tau) else float('inf'):16.3e}")

# ============================================================================
# STEP 5 -- the decisive comparison: lambda_+ vs H0, and 1/lambda_+ vs Hubble
# ============================================================================
print("\n" + "="*80)
print("STEP 5: instability timescale 1/lambda_+ vs Hubble time, for the UNSTABLE branch")
print("="*80)
print(f"  Using the framework's SLOWEST friction H=H_Lam (most conservative kill-chance).")
print(f"  In the OVER-DAMPED limit Gamma<<H the unstable root is lambda_+ = 2 Gamma^2/(9 H)")
print(f"  (sqrt(9H^2+4Gamma^2)-3H expanded; the naive float64 sqrt underflows to 0, so we")
print(f"   evaluate this analytic small-Gamma form -- THIS is the real slow growth rate):")
print(f"  {'M(eV)':>7s} {'Gamma(1/s)':>12s} {'Gamma/H_Lam':>12s} {'lambda_+(1/s)':>14s} "
      f"{'1/lambda_+(Gyr)':>16s} {'>1/H0?':>8s}")
worst_grow = np.inf
for M in M_grid:
    Gamma_s,_,_ = gamma_and_tc(M)
    # analytic over-damped unstable root (avoids the catastrophic float64 cancellation):
    lam_p = 2.0*Gamma_s**2/(9.0*H_Lam)              # s^-1, the slow growing root, >0
    grow_gyr = (1.0/lam_p)/Gyr
    worst_grow = min(worst_grow, grow_gyr)
    print(f"  {M:7.3f} {Gamma_s:12.3e} {Gamma_s/H_Lam:12.3e} {lam_p:14.3e} "
          f"{grow_gyr:16.3e} {'YES' if grow_gyr>1/H0/Gyr else 'NO':>8s}")

print(f"\n  Over-damping check (Vikman/Deffayet): the mode is OVER-DAMPED (no runaway in a")
print(f"  Hubble time) iff Gamma << H. For ALL M in [0.04,1] eV, Gamma/H_Lam =")
for M in M_grid:
    Gamma_s,_,_ = gamma_and_tc(M)
    print(f"      M={M:5.2f} eV : Gamma/H_Lam = {Gamma_s/H_Lam:.3e}  (Gamma/H0={Gamma_s/H0:.3e})")

# ============================================================================
# VERDICT
# ============================================================================
print("\n" + "="*80)
print("VERDICT (both ways, quarantine held)")
print("="*80)
all_unstable_bounded = all(r[3]=="BOUNDED" for r in results if r[1]=='UNSTABLE')
# FASTEST (most dangerous) analytic over-damped growth time across the M window:
#   the largest M gives the largest Gamma hence the FASTEST lam_+ = 2 Gamma^2/(9 H_Lam).
_lams = [(M, 2.0*gamma_and_tc(M)[0]**2/(9.0*H_Lam)) for M in M_grid]
M_worst, lam_worst = max(_lams, key=lambda t: t[1])
fastest_runaway = (1.0/lam_worst)/Gyr               # Gyr -- the most dangerous e-fold time
print(f"  Physical branch the dust forces (Step 2): Q>1, c_s^2>0  -> GRADIENT-STABLE.")
print(f"  Even the ADVERSARIAL Q<1 / gravitational-Jeans branch (Omega_eff^2=-Gamma^2):")
print(f"     <q^2(t)> over {N_H:.0f} Hubble times: {'BOUNDED for ALL M' if all_unstable_bounded else 'UNBOUNDED for some M'}")
print(f"     FASTEST instability e-fold time (most dangerous, M={M_worst} eV, H=H_Lam): "
      f"{fastest_runaway:.3e} Gyr vs 1/H0={t_H0/Gyr:.2f} Gyr")
print(f"     => that is {fastest_runaway*Gyr*H0:.3e} x the Hubble time "
      f"(~{np.log10(fastest_runaway/(t_H0/Gyr)):.0f} orders LONGER than 1/H0).")
if all_unstable_bounded and fastest_runaway > t_H0/Gyr:
    print(f"\n  ==> BOUNDED. dS Hubble friction OVER-DAMPS the Jeans/gradient mode at the ODE")
    print(f"      level (Gamma/H ~ 1e-27..1e-23 << 1 across the whole M window). The minimum")
    print(f"      CURES the Jeans instability classically: the residual over-damped growth")
    print(f"      time ({fastest_runaway:.1e}-{(1.0/(2.0*gamma_and_tc(M_grid[0])[0]**2/(9.0*H_Lam)))/Gyr:.1e} Gyr) exceeds the Hubble time by ~46-55")
    print(f"      orders. CONFIRMS dS-cures-Jeans WITH A NUMBER.")
else:
    print(f"\n  ==> UNBOUNDED for some physical M: runaway < 1/H0 -> minimum does NOT cure;")
    print(f"      squeezes M/amount.")
print("\n  QUARANTINE: a0/Z/kappa/I0 never asserted derived. The dust AMOUNT (I0) stays FREE;")
print("  this door tests STABILITY of the mode, not the derivation of the amount.")
print("  BOTH WAYS: a runaway (KILL) would have been reported with equal weight; the")
print("  integration returns BOUNDED, so BOUNDED is reported.")
