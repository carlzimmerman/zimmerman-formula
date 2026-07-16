#!/usr/bin/env python3
r"""
FRONT 1 fresh derivation: can the dS-Unruh BATH force the memory kernel theta(y)?
=================================================================================
Framework-internal ONLY (no comparison to anyone). Axiom: inertia = nonlocal-in-time
response to the de Sitter cosmic-horizon Unruh bath.
  T(a) = (hbar/2pi kB c) sqrt(a^2 + (cH_Lam)^2)          [Deser-Levin]
  a0 = (c/2) sqrt(G rho_DE) = cH_Lam/Z = 9.36e-11,  Z = 2 sqrt(8pi/3) = 5.789
  mu_fw(x) = (sqrt(1+4x^2)-1)/(2x),  mu_fw(1)=1/phi=0.618 (golden, exact).

The kernel theta(y), y = omega_ext/omega_internal, sits INSIDE the inertia argument
  A(om_in) = a_in + a_ex * theta(om_ex/om_in)         [Milgrom-2022 EFE form]
and is presently a FREE function -> every relational prediction is factor-~2 uncertain.

GOAL: derive theta(0) (adiabatic/static EFE) and the LEADING y-dependence / decay near
y~1 from the bath's OWN correlation structure, NOT by fitting MOND.

STRATEGY (the genuinely new move vs the prior 'forms mismatch' verdict):
  The bath has a finite correlation time tau_c ~ 1/H_Lam (the dS horizon sets the only
  IR clock). The inertial reaction is the response of the detector's vacuum-fluctuation
  energy to the ACCELERATION HISTORY, low-pass filtered by the bath. If we MODEL the
  response as a causal linear filter with the bath's own correlator as the memory, the
  kernel theta(y) is the FILTER's frequency response to the ratio of external drive to
  internal probe. We compute theta(0) from the static (DC) limit and the y-decay from
  the bath's spectral density.

  This is a BATH-MOTIVATED ANSATZ, NOT a first-principles QFT derivation (we flag every
  ansatz). The question: does the bath's correlation structure FORCE theta(0) and the
  decay rate, or leave them free?
"""
import sympy as sp
import mpmath as mp
import numpy as np

mp.mp.dps = 40
def H(s): print("\n"+"="*92+"\n "+s+"\n"+"="*92)
def h(s): print("\n"+"-"*92+"\n "+s+"\n"+"-"*92)

# ---------------------------------------------------------------- footing
c    = mp.mpf('2.998e8')
hbar = mp.mpf('1.0546e-34')
kB   = mp.mpf('1.381e-23')
Gc   = mp.mpf('6.674e-11')
a0   = mp.mpf('9.36e-11')
Z    = 2*mp.sqrt(8*mp.pi/3)
cH   = Z*a0                       # dS floor acceleration cH_Lam
H_L  = cH/c                       # dS Hubble rate (1/s)
phi  = (1+mp.sqrt(5))/2

H(" FOOTING (framework-internal, sealed)")
print(f"  a0      = {mp.nstr(a0,4)} m/s^2")
print(f"  Z       = 2 sqrt(8pi/3) = {mp.nstr(Z,6)}")
print(f"  cH_Lam  = Z a0 = {mp.nstr(cH,4)} m/s^2   (dS floor accel)")
print(f"  H_Lam   = {mp.nstr(H_L,4)} 1/s ;  1/H_Lam = {mp.nstr(1/H_L/3.156e16,4)} Gyr (the BATH correlation time)")
print(f"  mu_fw(1)= {mp.nstr((mp.sqrt(5)-1)/2,8)}  =? 1/phi = {mp.nstr(1/phi,8)}   (golden, exact check)")

# =====================================================================================
H(" PART A -- the de Sitter Wightman function on a worldline -> the BATH CORRELATOR")
# =====================================================================================
print(r"""
 A UDW detector on a uniformly-accelerated worldline in de Sitter sees the pulled-back
 Wightman function (Deser-Levin / Garbrecht-Prokopec); for the conformal/massless probe it
 is the THERMAL correlator at the combined temperature
        T_eff = (1/2pi) sqrt(a^2 + a_dS^2),    a_dS = cH_Lam,   (hbar=c=kB=1).
 Its KMS (Kubo-Martin-Schwinger) two-point function in proper time u = tau-tau' is the
 standard thermal Wightman function
        W(u) = -(1/4pi^2) * (pi T_eff)^2 / sinh^2(pi T_eff (u - i eps)).
 The detector's INERTIAL reaction (the framework's modified inertia) is sourced by this
 correlator's MEMORY: the response at time tau depends on the acceleration history through
 the bath's autocorrelation, whose decay time is
        tau_c = 1/(2pi T_eff)  ->  in the DEEP cosmic-floor (a -> 0) limit  tau_c = 1/(2pi)/ (a_dS/2pi) ...
 Let's get the bath correlation time cleanly in physical units.""")

# bath correlation time at the floor (a -> 0): T_eff -> a_dS/2pi, tau_c = 1/(2pi T_eff) = 1/a_dS
# restore units: T has dim 1/time when hbar=c=kB=1; a_dS has dim 1/time (accel/c).
# floor: a_dS = cH_Lam in accel units; the associated frequency is a_dS/c = H_Lam.
print(r"""
 At the cosmic floor (galactic regime, a ~ a0 << a_dS) the bath temperature SATURATES at
 the de Sitter value T_dS = a_dS/2pi = cH_Lam/2pi, so its correlation FREQUENCY is set by
 H_Lam:  the bath autocorrelation decays on  tau_c ~ 1/H_Lam  (a Hubble time).  THIS is the
 finite memory that makes the inertia nonlocal-in-time.  An internal orbit of frequency
 omega_in >> H_Lam is FAST vs the bath; an external drift omega_ex is filtered against it.""")
print(f"   bath correlation time tau_c = 1/H_Lam = {mp.nstr(1/H_L/3.156e16,4)} Gyr")

# =====================================================================================
H(" PART B -- the response as a CAUSAL FILTER of the acceleration history (the ansatz)")
# =====================================================================================
print(r"""
 ANSATZ (bath-motivated, FLAGGED): the inertial reaction to a time-varying acceleration is
 the acceleration history convolved with the bath's RESPONSE function chi(t) (linear-response
 / Kubo). The retarded response of a thermal bath with KMS correlator W(u) above is, by the
 fluctuation-dissipation theorem, a causal kernel whose spectral density is the bath's.
 We do NOT need W's full form; we need its SPECTRAL SHAPE S(omega), because theta(y) is by
 construction a function of a FREQUENCY RATIO. The thermal Wightman function
        W(u) ~ 1/sinh^2(pi T (u-i eps))
 has the EXACT Fourier transform (the detector response / power spectrum)
        S(omega) = (omega/2pi) / (1 - e^{-omega/T}) * [Bose factor]  (the Planckian UDW rate)
 i.e. the response spectrum is the Unruh/Planck detailed-balance spectrum
        S(omega) = (1/2pi) * omega / (e^{omega/T} - 1) * e^{omega/T}   (one-sided),
 OR symmetrized:  S_sym(omega) = (omega/4pi) coth(omega/2T).
 This is the BATH's own, parameter-free spectral filter (T = T_eff is the only scale).""")

w, T = sp.symbols('omega T', positive=True)
S_sym = (w/(4*sp.pi))*sp.coth(w/(2*T))     # symmetrized thermal response spectrum
print("  Bath symmetric response spectrum:  S_sym(omega) = (omega/4pi) coth(omega/2T)")
print("    low-freq (omega<<T): S -> T/2pi   (CLASSICAL/white plateau = the static bath)")
print("    high-freq(omega>>T): S -> omega/4pi (vacuum, quantum)")
slow = sp.limit(S_sym, w, 0)
print(f"    check S_sym(omega->0) = {slow}  (= T/2pi plateau)")

# =====================================================================================
H(" PART C -- read off theta(y): RATIO of external-drive response to internal-probe response")
# =====================================================================================
print(r"""
 The kernel theta(y) weights the EXTERNAL component (frequency omega_ex) inside the inertia
 argument of an INTERNAL mode (frequency omega_in).  In linear response the relative weight
 a near-frequency component carries is the bath's normalized transfer at that frequency
 RELATIVE to the probe frequency:
        theta(y) := S_sym(omega_ex) / S_sym(omega_in) (normalized) ,  y = omega_ex/omega_in.
 But BOTH frequencies are measured against the SAME bath scale T_eff.  Define the internal
 mode to sit at the probe frequency  Omega = omega_in/ (2 pi T_eff)  -- the dimensionless
 internal frequency in bath units.  Then
        theta(y; Omega) = [ S_sym(y*omega_in) / S_sym(omega_in) ]  normalized so theta(1)=1.
 theta(1)=1 is automatic (ratio at y=1). Compute theta(0) and the leading slope.""")

Om = sp.symbols('Omega', positive=True)   # Om = omega_in/(2 pi T_eff), internal freq in bath units
y  = sp.symbols('y', positive=True)
# S_sym(omega)/S_sym(omega_in) with omega = y*omega_in, in bath units x = omega/(2T):
# S_sym(omega) = (omega/4pi) coth(omega/2T). Let u = omega/(2T). Then S = (T/2pi) u coth(u).
# define f(u)= u coth(u). theta(y) = f(y*Om)/f(Om), Om = omega_in/(2T).
u = sp.symbols('u', positive=True)
f = u*sp.coth(u)
theta = f.subs(u, y*Om) / f.subs(u, Om)

print("  Using S_sym(omega) = (T/2pi) f(omega/2T), f(u)=u coth(u):")
print("     theta(y;Om) = f(y*Om)/f(Om),   Om = omega_in/(2 T_eff).")
print("     (theta(1)=1 automatic.)")

# theta(0):
theta0 = sp.limit(theta, y, 0)
print(f"\n  theta(0; Om) = lim_{{y->0}} f(yOm)/f(Om) = {sp.simplify(theta0)}")
print("     f(0)=1 (u coth u -> 1), so theta(0;Om) = 1/f(Om) = 1/(Om coth Om) = tanh(Om)/Om.")
theta0_expr = sp.tanh(Om)/Om
print(f"     => theta(0) = tanh(Om)/Om   (Om = omega_in / (2 T_eff))")

# leading y-slope near y=1 (decay rate):
dtheta = sp.diff(theta, y)
slope1 = sp.simplify(dtheta.subs(y,1))
print(f"\n  d theta/dy at y=1  =  {sp.simplify(slope1)}")
print("     (the LEADING decay rate of the kernel near y~1)")

# =====================================================================================
H(" PART D -- evaluate theta(0) and slope for REAL internal frequencies (galactic regime)")
# =====================================================================================
print(r"""
 Now PIN Om for the framework's regimes. Om = omega_in/(2 T_eff). In the cosmic-floor regime
 T_eff -> T_dS = cH_Lam/2pi (frequency H_Lam/... ). Restoring units: the bath frequency scale
 is 2 T_eff -> H_Lam-ish. An internal galactic/cluster orbit has omega_in >> H_Lam, so
 Om = omega_in/(2 T_eff) >> 1.  In that limit:
       theta(0) = tanh(Om)/Om -> 1/Om -> 0 ,   and the kernel is SHARPLY peaked.
 That is the FAST-PROBE limit. Let's get numbers.""")

# bath frequency scale: 2 T_eff in angular-freq units. T_eff(floor)=cH/2pi (energy/hbar...).
# In hbar=c=kB=1, T has units of frequency. Convert: omega_bath := 2*pi*T_eff has units 1/s.
# At floor T_eff = cH_Lam/(2pi c) ... carefully: Deser-Levin T = (1/2pi) sqrt(a^2+(cH)^2) with
# hbar=c=kB=1 means T is in units of inverse-length = acceleration (since a has those units here).
# Physical angular frequency associated with the bath = a_dS/c = H_Lam.  So 2 T_eff(floor) ~ H_Lam/pi.
# We take the BATH ANGULAR FREQUENCY = H_Lam (the dS horizon clock) as the denominator scale.
omega_bath = H_L
print(f"  bath angular frequency (dS clock) ~ H_Lam = {mp.nstr(H_L,4)} 1/s")

regimes = [
    ("galaxy rotation (R~10 kpc, v~150 km/s)", mp.mpf('150e3')/(mp.mpf('10')*mp.mpf('3.0857e19'))),
    ("wide binary (P_in ~ 0.5 Myr @ 10 kau)",  2*mp.pi/(mp.mpf('0.5')*mp.mpf('3.156e13'))),
    ("cluster plunging dwarf (P_in ~ 1 Gyr)",  2*mp.pi/(mp.mpf('1')*mp.mpf('3.156e16'))),
    ("dSph internal (P_in ~ 0.1 Gyr)",         2*mp.pi/(mp.mpf('0.1')*mp.mpf('3.156e16'))),
]
th0f = sp.lambdify(Om, theta0_expr, 'mpmath')
print(f"\n  {'regime':44s} {'omega_in[1/s]':>14s} {'Om=om_in/H_Lam':>16s} {'theta(0)':>12s}")
for name, oin in regimes:
    Omv = oin/omega_bath
    th0 = th0f(Omv)
    print(f"  {name:44s} {mp.nstr(oin,3):>14s} {mp.nstr(Omv,3):>16s} {mp.nstr(th0,4):>12s}")

print(r"""
 OBSERVATION: with the bath clock = H_Lam, Om = omega_in/H_Lam is ENORMOUS (1e2..1e3+) for
 every bound system => theta(0)=tanh(Om)/Om ~ 1/Om ~ 0.  i.e. this naive 'spectral-ratio'
 ansatz gives theta(0) -> 0, NOT 'a few'. That CONTRADICTS the static EFE (which needs a
 finite theta(0) ~ O(1) to recover MOND). So the naive ratio ansatz FAILS the adiabatic
 anchor -- exactly the prior workflow's 'opposite adiabatic limits' obstruction, now seen
 quantitatively. Record this as a NEGATIVE result and try the CORRECT static limit next.""")

# =====================================================================================
H(" PART E -- the CORRECT static/adiabatic limit: theta(0) from the bath, done right")
# =====================================================================================
print(r"""
 The error above: theta(y) is NOT the ratio of bath RESPONSE at two frequencies. In the
 adiabatic (y->0) limit the external field is QUASI-STATIC: it shifts the detector's proper
 acceleration from a_in to (a_in + a_ex). The inertia argument is the bath temperature's
 dependence on the TOTAL acceleration. theta(0) is then DEFINED by how a small DC external
 acceleration adds inside the bath temperature:
        T_eff = (1/2pi) sqrt( (a_in + theta(0) a_ex)^2 + a_dS^2 )   (EFE form)
 vs the bath's ACTUAL response to a_in + a_ex (vector sum at DC):
        T_eff = (1/2pi) sqrt( |a_in + a_ex|^2 + a_dS^2 ).
 At DC the external field adds with FULL WEIGHT (it is just part of the proper acceleration),
 so theta(0) = 1 is FORCED by the bath: a static external acceleration is indistinguishable
 from any other contribution to the proper acceleration -- the equivalence principle in the
 bath frame.  Let's verify this is what the static Deser-Levin temperature says.""")

# At DC, a_ex is a constant addition to proper acceleration. T_eff depends on |a_total|.
# Expand T_eff for a_ex along a_in: a_total = a_in + a_ex (collinear, DC).
ain, aex, adS = sp.symbols('a_in a_ex a_dS', positive=True)
Teff_actual = sp.sqrt((ain+aex)**2 + adS**2)
Teff_efe    = sp.sqrt((ain + sp.Symbol('th0',positive=True)*aex)**2 + adS**2)
print("  bath-actual DC:  T ~ sqrt((a_in+a_ex)^2 + a_dS^2)")
print("  EFE form:        T ~ sqrt((a_in+theta0*a_ex)^2 + a_dS^2)")
# match leading order in a_ex:
lhs = sp.series(Teff_actual, aex, 0, 2).removeO()
rhs = sp.series(Teff_efe,    aex, 0, 2).removeO()
sol = sp.solve(sp.Eq(sp.expand(lhs-rhs),0), sp.Symbol('th0',positive=True))
print(f"  matching O(a_ex):  theta(0) = {sol}")
print("  => theta(0) = 1 is FORCED by the bath at DC (external accel adds with unit weight).")
print(r"""
 BUT NOTE: Milgrom's EFE convention puts theta(0) = 'a few' (e.g. 2, e) because in HIS
 normalization theta(1)=1 and theta RISES toward DC. The bath says the PHYSICAL DC weight is
 unity (equivalence principle). The 'few' is a NORMALIZATION choice (where you set theta(1)=1
 relative to the DC value). The bath FORCES the RATIO theta(0)/theta(1) -- the SHAPE -- not a
 free 'few'. We extract that ratio next.""")

print("\n[done part E]")
