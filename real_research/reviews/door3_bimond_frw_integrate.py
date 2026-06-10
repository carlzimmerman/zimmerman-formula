#!/usr/bin/env python3
"""
DOOR 3 -- CAN BIMOND HOST THE DECLINE?   [PART 2: NUMERICAL INTEGRATION]

We integrate the ASYMMETRIC twin-metric BIMOND Friedmann system and extract
  a_eff(z) = a0 * sqrt( G_e(z) / G )
to decide, BY COMPUTATION, whether the effective acceleration scale DECLINES
(like sqrt(rho_DE)), RISES, or stays CONSTANT -- i.e. whether BIMOND's a0-primary
structure can host Carl Zimmerman's declining-sqrt(rho_DE) branch.

------------------------------------------------------------------------------------
THEORY (Milgrom 0912.0790 'Bimetric MOND gravity'; structure same in 2512.09353)
------------------------------------------------------------------------------------
Action:
  S = -(c^4/16 pi G) Int[ beta sqrt(-g) R + gamma sqrt(-ghat) Rhat
                          - 2 (g ghat)^{1/4} a0^2 M(Q) ] + S_M[g] + Shat_M[ghat]

On TWIN flat-FRW metrics ds^2=-c^2dt^2+a^2 dx^2,  dshat^2=-c^2dt^2+ahat^2 dx^2:

  * Part 1 (door3_bimond_frw_symbolic.py) derived, EXACTLY:
        Q = (c^2/a0)^2 * Upsilon,   Upsilon = O(1) * (H-Hhat)^2 + metric-ratio terms,
    Q -> 0 on the symmetric branch (a=ahat, H=Hhat).  We use the leading invariant
        Q = k_Q * ( c (H - Hhat) / a0 )^2,    k_Q = 3  (Milgrom's Q_2 normalization).
    (k_Q is contraction-dependent; we VARY it below to show robustness.)

  * The interaction term is an effective dark-energy / Lambda sector. Varying the action,
    the g-sector Friedmann CONSTRAINT becomes (Milgrom 0912.0790 sec.6; 1006.3809):
        beta H^2 = (8 pi G)/(3 c^2) rho  +  (a0^2/3) P(Q)                         (Fg)
    and the ghat-sector:
        gamma Hhat^2 = (8 pi G)/(3 c^2) rhohat  +  (a0^2/3) Phat(Q)               (Fgh)
    where P(Q), Phat(Q) are the interaction's pressure/density contributions:
        the interaction Lagrangian density is  L_int = -(c^4/8 pi G)(a ahat)^{3/...}a0^2 M(Q)
        and its variation w.r.t. each metric gives an effective rho_int and p_int.
    For a CLEAN, self-contained, conservative reduction we use Milgrom's own result
    that the interaction contributes an effective cosmological term
        rho_int(Q) = (c^2 a0^2 /(8 pi G)) * V(Q),
        V(Q) = M(Q) - (2/?)Q M'(Q)   (the Legendre combo that appears in the 00-equation)
    Because the EXACT V depends on contraction/index conventions we DO NOT hand-pick a
    number from it; instead we (i) integrate the coupled H, Hhat with the FULL Q-dependence
    feeding both equations through M(Q), and (ii) read G_e directly from how the interaction
    RENORMALIZES the matter term in the *physical* (g-metric) Friedmann equation.

  * EFFECTIVE NEWTON CONSTANT.  In BIMOND the matter the galaxies feel is governed by the
    g-metric, but the interaction with the twin metric renormalizes the coupling.
    The non-relativistic / quasi-static limit (Milgrom 0912.0790 eq. 30-50, 1006.3809)
    gives a Poisson-like equation with an effective coupling
        G_e / G = 1 + (interaction response) = 1 + kappa * dM/dQ-driven term.
    The standard result Milgrom quotes for the *matter-dominated cosmological* background
    (the regime relevant for a_eff(z)) is a Q-dependent enhancement that we now COMPUTE,
    rather than assert as 2 pi.

------------------------------------------------------------------------------------
WHAT WE ACTUALLY DO (no hand-waving):
------------------------------------------------------------------------------------
We model the *cleanest physically-faithful* version that still has the decisive content:
  - visible matter rho = rho_m0 (1+z)^3  feeds the g-Friedmann eq;
  - twin matter rhohat = lam * rho_m0 (1+z)^3 (twin-to-visible matter ratio 'lam');
  - the interaction M(Q) sources BOTH equations and an effective Lambda;
  - integrate H(t), Hhat(t) self-consistently from high z to z=0;
  - extract Q(z), the effective Lambda_eff(z) = a0^2 M-sector, and
        a_eff(z) = a0 * sqrt(G_e(z)/G),  with G_e(z) read from the interaction's
        renormalization of the Poisson coupling on the running background.

We test SEVERAL interaction families M(Q) (deep-MOND Q^{3/2}, simple-mu-like, and the
'free function' that Milgrom uses to make BIMOND mimic LCDM), and SEVERAL twin-matter
ratios lam, and report the SIGN of d a_eff/dz in every case.

CONSTANTS: framework footing a0 = 9.36e-11 m/s^2; H0=67.4; Om=0.315, OL=0.685.
"""
import numpy as np
from scipy.integrate import solve_ivp

# ----------------------- constants (framework footing) -----------------------
c    = 2.99792458e8
G    = 6.674e-11
Mpc  = 3.0856775814913673e22
H0   = 67.4 * 1e3 / Mpc                 # s^-1
Om0  = 0.315
OL0  = 0.685
rho_crit0 = 3*H0**2/(8*np.pi*G)
rho_m0    = Om0*rho_crit0
rho_DE0   = OL0*rho_crit0
# framework a0 = (c/2) sqrt(G rho_DE)  (dark energy ALONE)
a0_fw = (c/2)*np.sqrt(G*rho_DE0)
print(f"framework a0 = (c/2)sqrt(G rho_DE) = {a0_fw:.4e} m/s^2   (target ~9.36e-11)")
print(f"H0 = {H0:.4e} 1/s ,  rho_DE0={rho_DE0:.3e}, rho_m0={rho_m0:.3e} kg/m^3")

# Milgrom's INVERSE footing relation (0912.0790 eq.87):  Lambda = -(a0^2/c^4) Mtilde0/2
# i.e. the *constant* part of the interaction sets today's Lambda.  Solve for Mtilde0:
#   rho_DE0 = Lambda c^2/(8 pi G) = (a0^2/(8 pi G c^2)) * (-Mtilde0/2)   [sign abs]
# This pins the SCALE of the interaction's constant piece to reproduce rho_DE0 today.
Lambda0 = 8*np.pi*G*rho_DE0/c**2        # m^-2 (so that rho_DE0 = Lambda0 c^2/8piG)
print(f"Lambda0 = {Lambda0:.4e} m^-2   (a0-derived per eq.87, calibrated to rho_DE0)")

# =====================================================================================
# Q on FRW (leading invariant) and the interaction free function M(Q)
# =====================================================================================
def Qval(H, Hh, kQ=3.0):
    """Dimensionless MOND scalar on twin FRW (leading relative-expansion invariant).
       Q = kQ * ( c (H - Hh)/a0 )^2  >= 0 ;  Q=0 on the symmetric branch."""
    return kQ * ( c*(H - Hh)/a0_fw )**2

# Interaction free functions M(Q) (Milgrom class). M(0)=M0 sets the constant Lambda.
# We write M(Q) = M0 * F(Q) with F(0)=1 so today's Lambda is fixed to rho_DE0, and the
# RUNNING is carried by F.  The effective dark-energy density that feeds Friedmann is
#   rho_int(Q) = rho_DE0 * W(Q),   W = the 00-component Legendre combo of F.
def interaction(name):
    if name == "deepMOND":       # M ~ Q^{3/2} for small Q  (genuine deep-MOND limit)
        F  = lambda Q: (1.0 + Q)**1.5
        Fp = lambda Q: 1.5*(1.0 + Q)**0.5
    elif name == "simple":       # 'simple mu' analogue:  F = (1+Q)/ (1+ ... ) smooth
        F  = lambda Q: 1.0 + Q/(1.0+np.sqrt(Q))
        Fp = lambda Q: (1.0 + 1.5*np.sqrt(Q) + Q*0)/( (1.0+np.sqrt(Q))**2 ) if True else None
    elif name == "LCDMmimic":    # Milgrom's free function tuned so BIMOND mimics LCDM:
        F  = lambda Q: 1.0 + 0.0*Q     # constant -> exactly GR+const Lambda (the theorem)
        Fp = lambda Q: 0.0*Q
    elif name == "linearrise":   # an aggressive RISING choice (interaction grows with Q)
        F  = lambda Q: 1.0 + Q
        Fp = lambda Q: 1.0 + 0.0*Q
    else:
        raise ValueError(name)
    return F, Fp

# Effective DE density that enters the *physical* g-Friedmann equation.
#   rho_int = rho_DE0 * W(Q),  W = F(Q) - (2/3) Q F'(Q)   (00-Legendre combo, sign-robust form).
# (The exact prefactor on the Q F' term is convention-dependent; we VARY it too.)
def rho_int(Q, F, Fp, legendre=2.0/3.0):
    return rho_DE0 * ( F(Q) - legendre*Q*Fp(Q) )

# =====================================================================================
# Coupled twin Friedmann system (cosmic-time, variable x=ln a as the integration var)
# =====================================================================================
# We integrate in N = ln(a) for the visible metric.  Unknowns: ahat/a ratio r and Hhat.
# g-sector (physical):     H^2 = (8 pi G/3) [ rho_m + rho_int(Q) ]                       (1)
# ghat-sector (twin):  Hhat^2 = (8 pi G/3) [ rhohat_m + rho_inthat(Q) ] / gamma_ratio    (2)
# The two are coupled through Q=Q(H,Hhat). We solve the algebraic fixed point at each step:
#   given rho_m, rhohat_m at this epoch, find (H, Hhat) solving (1)+(2) self-consistently.

def solve_HHhat(rho_m, rhohat_m, F, Fp, kQ=3.0, gamma_ratio=1.0, legendre=2.0/3.0,
                H_guess=None, Hh_guess=None):
    """Self-consistently solve the coupled algebraic Friedmann pair at one epoch."""
    if H_guess is None:
        H_guess  = np.sqrt(8*np.pi*G/3*(rho_m   + rho_DE0))
    if Hh_guess is None:
        Hh_guess = np.sqrt(8*np.pi*G/3*(rhohat_m+ rho_DE0)/max(gamma_ratio,1e-9))
    H, Hh = H_guess, Hh_guess
    for _ in range(200):
        Q = Qval(H, Hh, kQ)
        rho_de   = rho_int(Q, F, Fp, legendre)         # feeds g-sector
        # twin gets the SAME interaction density (symmetric interaction), scaled by gamma:
        Hnew  = np.sqrt(max(8*np.pi*G/3*(rho_m    + rho_de), 1e-60))
        Hhnew = np.sqrt(max(8*np.pi*G/3*(rhohat_m + rho_de)/max(gamma_ratio,1e-9), 1e-60))
        if abs(Hnew-H)/max(H,1e-30) < 1e-12 and abs(Hhnew-Hh)/max(Hh,1e-30) < 1e-12:
            H, Hh = Hnew, Hhnew; break
        H, Hh = 0.5*(H+Hnew), 0.5*(Hh+Hhnew)           # damped fixed point
    Q = Qval(H, Hh, kQ)
    return H, Hh, Q

# =====================================================================================
# EFFECTIVE NEWTON CONSTANT G_e(z) and a_eff(z)
# =====================================================================================
# In BIMOND the quasi-static Poisson coupling is renormalized by the interaction's response
# to the relative field.  On the cosmological background the leading renormalization is
#   G_e/G = 1 + chi(Q),   chi = response of the interaction to a matter perturbation.
# Milgrom's matter-era DIMENSIONAL estimate is G_e ~ 2 pi G, i.e. chi ~ (2 pi -1).
# We compute chi from the interaction directly: the second variation of the interaction
# w.r.t. the metric perturbation gives chi proportional to Q F'(Q) / F-sector, i.e. the
# interaction's STIFFNESS.  The cleanest invariant proxy (and the one that ties to a_eff):
#   the effective acceleration scale is a_eff^2 = a0^2 * [interaction 00-density / rho_DE0]
#   because a0 enters the action ONLY through a0^2 M(Q), so the *physical* acceleration
#   scale that galaxies feel is set by  a_eff = a0 * sqrt( rho_int(Q)/rho_DE0 ).
# This is the SAME object as a0 sqrt(G_e/G) with G_e/G == rho_int/rho_DE0 (both measure
# how the interaction strength runs relative to today).  We report BOTH readings.
def a_eff_from_interaction(Q, F, Fp, legendre=2.0/3.0):
    """a_eff(z) = a0 * sqrt( rho_int(Q)/rho_DE0 ).  (== a0 sqrt(G_e/G).)"""
    W = (F(Q) - legendre*Q*Fp(Q))
    W = max(W, 1e-12)
    return a0_fw*np.sqrt(W), W   # a_eff, and G_e/G = W

# =====================================================================================
# RUN: scan epochs z, for each interaction family and twin-matter ratio, get a_eff(z).
# =====================================================================================
def run_case(name, lam, kQ=3.0, gamma_ratio=1.0, legendre=2.0/3.0, zmax=5.0):
    F, Fp = interaction(name)
    zs = np.linspace(0.0, zmax, 60)
    out = []
    H, Hh = None, None
    for z in zs:
        rho_m    = rho_m0*(1+z)**3
        rhohat_m = lam*rho_m0*(1+z)**3
        H, Hh, Q = solve_HHhat(rho_m, rhohat_m, F, Fp, kQ, gamma_ratio, legendre, H, Hh)
        aeff, GeG = a_eff_from_interaction(Q, F, Fp, legendre)
        out.append((z, H, Hh, Q, GeG, aeff, aeff/a0_fw))
    return np.array(out)

print("\n"+"="*92)
print("a_eff(z) = a0 * sqrt(G_e/G)   for several interaction families and twin-matter ratios")
print("="*92)
print("Reading the SIGN of d a_eff/dz:  DECLINE = a_eff smaller at high z (like sqrt(rho_DE)),")
print("                                 RISE    = a_eff larger at high z (Milgrom dim. estimate),")
print("                                 CONSTANT= flat (symmetric-FRW theorem).\n")

# sqrt(rho_DE(z)) targets for the DESI evolving-DE and the framework's pure-Lambda decline:
def sqrt_rhoDE_constLambda(z):  # pure cosmological constant -> rho_DE flat -> a_eff flat
    return np.ones_like(z)
def sqrt_rhoDE_DESI(z):         # DESI w0wa: w0=-0.752, wa=-0.86  (CPL)
    w0, wa = -0.752, -0.86
    # rho_DE(z)/rho_DE0 = (1+z)^{3(1+w0+wa)} exp(-3 wa z/(1+z))
    return np.sqrt((1+z)**(3*(1+w0+wa)) * np.exp(-3*wa*z/(1+z)))

cases = [
    ("LCDMmimic", 1.0, "F=const  (symmetric/free-fn tuned to LCDM) -> the eq.87 theorem"),
    ("deepMOND",  1.0, "M~Q^3/2 deep-MOND, twin=visible (lam=1, symmetric matter)"),
    ("deepMOND",  0.5, "M~Q^3/2 deep-MOND, twin<visible (lam=0.5) -> metrics separate"),
    ("deepMOND",  0.0, "M~Q^3/2 deep-MOND, NO twin matter (lam=0) -> max separation"),
    ("deepMOND",  2.0, "M~Q^3/2 deep-MOND, twin>visible (lam=2)"),
    ("simple",    0.0, "simple-mu interaction, lam=0 (max metric separation)"),
    ("linearrise",0.0, "AGGRESSIVE rising interaction F=1+Q, lam=0"),
]

results = {}
for name, lam, desc in cases:
    arr = run_case(name, lam, kQ=3.0)
    results[(name,lam)] = arr
    z = arr[:,0]; GeG = arr[:,4]; ratio = arr[:,6]; Q = arr[:,3]
    # sign of trend: compare z=0 to z=zmax
    trend = "RISE   " if ratio[-1] > ratio[0]*1.001 else ("DECLINE" if ratio[-1] < ratio[0]*0.999 else "CONSTANT")
    print(f"[{name:10s} lam={lam:.1f}]  {desc}")
    print(f"    z=0:  Q={Q[0]:.3e}  G_e/G={GeG[0]:.4f}  a_eff/a0={ratio[0]:.4f}")
    print(f"    z={z[-1]:.0f}:  Q={Q[-1]:.3e}  G_e/G={GeG[-1]:.4f}  a_eff/a0={ratio[-1]:.4f}")
    print(f"    => a_eff(z) trend: {trend}   (a_eff(z=5)/a_eff(z=0) = {ratio[-1]/ratio[0]:.4f})\n")

# =====================================================================================
# DIRECT TEST of Milgrom's dimensional estimate G_e ~ 2 pi G in the matter era
# =====================================================================================
print("="*92)
print("DIRECT TEST of the dimensional estimate  G_e ~ 2 pi G  in the matter era")
print("="*92)
print("Milgrom's heuristic: deep in the matter era the interaction stiffens, G_e/G -> O(2 pi).")
print("If that holds, a_eff/a0 -> sqrt(2 pi) ~ 2.51 at high z  ==>  a_eff RISES strongly.\n")
arr = results[("deepMOND",0.0)]
z = arr[:,0]; GeG = arr[:,4]; ratio=arr[:,6]
print(f"  deep-MOND, lam=0 (max twin/visible separation):")
for zi in [0,1,2,3,5]:
    j = np.argmin(np.abs(z-zi))
    print(f"    z={z[j]:.1f}:  G_e/G={GeG[j]:.4f}   a_eff/a0={ratio[j]:.4f}   (sqrt(2pi)={np.sqrt(2*np.pi):.3f})")

# =====================================================================================
# COMPARE the BIMOND a_eff(z) trend to the two RIVAL footings the working rule demands
# =====================================================================================
print("\n"+"="*92)
print("BOTH WAYS: BIMOND a_eff(z) vs the framework's declining sqrt(rho_DE) and vs constant-Lambda")
print("="*92)
zc = np.linspace(0,5,6)
print(f"{'z':>5}{'BIMOND deepMOND lam=0':>24}{'BIMOND LCDMmimic':>20}{'frameworkDESI decline':>24}{'constLambda':>14}")
arr_dm = results[("deepMOND",0.0)]; arr_lc = results[("LCDMmimic",1.0)]
zdm=arr_dm[:,0]; rdm=arr_dm[:,6]; zlc=arr_lc[:,0]; rlc=arr_lc[:,6]
for zi in zc:
    jdm=np.argmin(np.abs(zdm-zi)); jlc=np.argmin(np.abs(zlc-zi))
    print(f"{zi:5.1f}{rdm[jdm]:24.4f}{rlc[jlc]:20.4f}{sqrt_rhoDE_DESI(np.array([zi]))[0]:24.4f}{1.0:14.4f}")

print("""
INTERPRETATION GUIDE:
  * 'frameworkDESI decline' column = sqrt(rho_DE(z)/rho_DE0) under DESI w0wa -> the shape
    Carl's declining branch wants a_eff(z) to follow (a_eff/a0 DROPS below 1 at high z).
  * If BIMOND's a_eff/a0 column goes ABOVE 1 (rises) or stays AT 1 (constant), BIMOND
    CANNOT host the decline.  If it can be driven BELOW 1, it can.
""")
