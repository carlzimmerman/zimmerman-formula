#!/usr/bin/env python3
"""
L19 -- does the gravitational-Cherenkov bound actually apply to IC10's k-essence clock?
==========================================================================================================
THE CONFLICT THIS LANE RESOLVES.  Two of this lane's own results disagree about the same mode.

  L10 (L10_khronon_gate.py, section E) applied the gravitational-Cherenkov bound 1 - c_s <= 2e-15
      (Moore & Nelson, JHEP 0109:023 (2001), hep-ph/0106220; Elliott, Moore & Stoica, JHEP 0508:066
      (2005), hep-ph/0505211) to the extra propagating scalar of the lead's IC series, and concluded
      c_s^2 = 1/3 is EXCLUDED BY 2.1e14x, forcing the design parameter sigma from 1/3 to 1.
  L8  (L8_VERIFICATION.md) then established what L10 did not know: on IC10's eta = 1 plateau the metric
      sector is EXACTLY Einstein -- DeWitt lambda = 1 identically, m* = m e^(-1/6) > 0, the Hamiltonian
      constraint first class again -- so the third mode is no longer the gravitational khronon that
      IC5/IC6/IC7 carried.  It is a separately counted, shift-symmetric k-essence CLOCK, and the count
      matches the textbook GR + k-essence answer of 3.

L10 assumed the mode couples like a gravitational-sector mode.  L8 shows its character changed.  This
lane settles the question by computing, not asserting: what is the Cherenkov bound a bound ON, what does
IC10's clock actually couple to, and what number comes out.

WHAT IS DERIVED HERE (nothing is taken on authority except the two published bounds used as CONTROLS)
  A. The Cherenkov kinematics and the emission rate from first principles: threshold, k_max, the on-shell
     identity 2 p.k = k^2, and Gamma = (1/(16 pi E p v)) Integral dk |M|^2, energy loss (1/E) dE/dx.
  B. CONTROL: the tensor (gravitational-strength) rate, checked against BOTH Milgrom (2011)'s
     transcription of Moore & Nelson's coefficient AND the published Galactic number 2e-15.
  C. IC10's matter coupling, read off its action: S_m[e^(2w) gtilde, psi] with w AUXILIARY.  The clock
     field T does not appear in the matter action at all -- it enters only through the conformal factor,
     so the vertex is to T^mu_mu and to NOTHING else.  Disformal positive control included.
  D. The on-shell trace matrix elements (scalar primary, Dirac primary, photon) and the bound that a
     trace-coupled clock at gravitational strength ACTUALLY has to satisfy.
  E. The MOND-radius cutoff.  Milgrom, "Gravitational Cherenkov losses in MOND theories",
     arXiv:1102.1818 (Phys. Rev. D 83): in a theory that coincides with GR in the HIGH-acceleration
     limit, the radiation of wavenumber k is generated at distance ~1/k from the primary, where the
     primary's OWN field sets |a|.  This lane re-derives Milgrom's D_loss = q l_M from its own rate
     formula, independently.  L10 evaluated the exponential wall at the AMBIENT galactic acceleration;
     that is the wrong place, and it is why L10's escape analysis (K8) failed.
  F. The other constraints on a subluminal minimally-coupled scalar: causality under a preferred
     foliation, emission by photons / neutrinos / gravitons, binary pulsars, CMB.
  G. Verdict, stated as a conditional with the deciding input named.

CHECKS THAT CAN FAIL
  C1 [CONTROL]  Cherenkov kinematics: cos(theta), k_max, the threshold E > M/sqrt(1-v^2), and the
                on-shell identity 2 p.k = k^2 -- all symbolic.
  C2 [CONTROL]  Dirac trace Tr[(p'+M)(p+M)] = 4(p.p' + M^2) with explicit gamma matrices; Maxwell
                T^mu_mu = 0 identically; the improved (xi = 1/6) massless scalar trace vanishes.
  C3 [CONTROL]  the tensor energy-loss rate derived here reproduces (a) Moore & Nelson's coefficient as
                transcribed by Milgrom 2011 eq. (2) and (b) the published Galactic bound 1 - c <= 2e-15.
                If this fails, nothing downstream is trustworthy.
  C4 [coupling] IC10's clock couples to ordinary matter ONLY through the conformal factor, i.e. to
                T^mu_mu and to nothing else -- with a DISFORMAL positive control proving the test has
                teeth.
  C5 [vertex]   is the trace vertex (M/E)^2-suppressed relative to the tensor vertex, as a naive
                conformal-coupling argument would say?  (Tested honestly; it is not.)
  C6 [bound]    is 1 - c_s <= 2e-15, the number L10 imposed, the bound that applies to this mode?
  C7 [CONTROL]  the MOND-radius cutoff, fed into the SAME rate formula, reproduces Milgrom's
                D_loss = q l_M with E dropping out and l_M ~ 2 pi D_H.  Both a0 footings.
  C8a [verdict] does c_s^2 = 1/3 survive Cherenkov with the trace coupling alone (no screening)?
  C8b [verdict] does c_s^2 = 1/3 survive once the framework's own high-acceleration GR limit is applied
                where the radiation is generated?  Both a0 footings.
  C9 [causality]  is a subluminal clock cone causal given the preferred foliation the clock defines?
  C10 [channels]  do photons, neutrinos or gravitons give a binding Cherenkov bound on this clock?
  C11 [pulsar/CMB] is there a binding bound on c_s from binary pulsars or the CMB?
  C12 [VERDICT]   is L10's exclusion of c_s^2 = 1/3 correct AS STATED?

NOTHING under closure_2026/integrable_clock_construction_2026/ is imported, executed or copied.  The IC10
action was transcribed by hand from IC10_LOCAL_CLOCK.md.
"""
import sympy as sp, numpy as np, math, sys, time
from mpmath import mp, mpf, quad

mp.dps = 30
T0 = time.time(); FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

def head(s):
    print("\n" + "=" * 118); print(s); print("=" * 118, flush=True)

# ---------------------------------------------------------------------------------------------------
# units: natural units hbar = c = 1, energies in GeV.
# ---------------------------------------------------------------------------------------------------
GEV_PER_INV_M = 5.067731e15          # 1 GeV = 5.0677e15 m^-1  (hbar c = 1.97327e-16 GeV m)
G_N       = 6.708830e-39             # GeV^-2   (= 1/M_Pl^2 with M_Pl = 1.220890e19 GeV)
MPL2_RED  = 1.0/(8*math.pi*G_N)      # reduced Planck mass squared, GeV^2
M_PROTON  = 0.9382720813             # GeV
KPC_M     = 3.0856776e19             # m
D_GAL_M   = 10.0*KPC_M               # the Galactic path length Moore & Nelson / Elliott et al. use
D_GAL     = D_GAL_M*GEV_PER_INV_M    # GeV^-1
D_HUBBLE_M= 1.3e26                   # m, c/H0 for h = 0.674
C_LIGHT   = 2.99792458e8             # m/s
G_SI      = 6.674e-11
A0_CANON, A0_ALT = 9.3619e-11, 1.1279e-10
FOOT = (("canonical", A0_CANON), ("alt", A0_ALT))

E_MN   = 3.0e11                      # GeV -- the UHECR energy Moore & Nelson quote (3e20 eV)
E_TASK = 1.0e11                      # GeV -- 1e20 eV, the energy named in this lane's brief
CHER_PUB = 2e-15                     # the published Galactic bound L10 imposed
PARTON = 1e-3                        # Moore & Nelson's partonic factor (Milgrom 2011 sec. II: the
                                     # hadron radiates as partons each carrying ~0.1 p, which raises
                                     # D_loss by 1e3 i.e. lowers the rate by 1e-3)

print("=" * 118)
print("L19 -- does the gravitational-Cherenkov bound apply to IC10's shift-symmetric k-essence clock?")
print("=" * 118, flush=True)

# ===================================================================================================
head("A -- the process, from first principles: kinematics and the emission rate")
# ===================================================================================================
E, M, k, v, p_, th = sp.symbols('E M k v p theta', positive=True)
print("    A primary of mass M and energy E, momentum p = sqrt(E^2 - M^2), emits one quantum of a mode")
print("    with dispersion omega = v |k|, v < 1, at angle theta to its momentum.  Energy-momentum")
print("    conservation with the final primary on shell gives")
p_expr = sp.sqrt(E**2 - M**2)
# E - v k = sqrt(p^2 - 2 p k cos + k^2 + M^2)  ->  solve for cos(theta)
cos_sol = sp.solve(sp.Eq((E - v*k)**2, p_**2 - 2*p_*k*sp.cos(th) + k**2 + M**2), sp.cos(th))[0]
cos_sol = sp.simplify(cos_sol.subs(p_**2, E**2 - M**2))
cos_closed = (E*v + k*(1 - v**2)/2)/p_
print(f"          cos(theta) = {sp.simplify(cos_closed)}   [= (E v + k(1-v^2)/2)/p]")
same_cos = sp.simplify(sp.expand(cos_sol.subs(p_, p_expr) - cos_closed.subs(p_, p_expr))) == 0
kmax_closed = 2*(p_ - E*v)/(1 - v**2)
kmax_from_cos = sp.solve(sp.Eq(cos_closed, 1), k)[0]
same_kmax = sp.simplify(kmax_from_cos - kmax_closed) == 0
print(f"          k_max      = {kmax_closed}         (the value at cos(theta) = 1)")
# threshold: k_max > 0  <=>  p > E v  <=>  E > M/sqrt(1-v^2)
thr = sp.solve(sp.Eq(p_expr, E*v), E)[0]
thr_ok = sp.simplify(thr**2 - M**2/(1 - v**2)) == 0        # squared, to sidestep sympy's branch form
print(f"          threshold  : k_max > 0  <=>  p > E v  <=>  E > M/sqrt(1-v^2)   [sympy: {thr}]")
# on-shell identity 2 p.k = k^2  (mostly-minus); k^2 = omega^2 - |k|^2 = -(1-v^2)|k|^2
pdotk = E*(v*k) - p_*k*cos_closed
k2inv = (v*k)**2 - k**2
id_ok = sp.simplify(sp.expand(2*pdotk - k2inv)) == 0
print(f"          on shell   : 2 p.k = {sp.simplify(sp.expand(2*pdotk))} = k^2_inv = -(1-v^2)|k|^2   "
      f"(the emitted quantum is SPACELIKE, |q^2| = (1-v^2)|k|^2)")
print(f"\n    The 1 -> 2 rate, with relativistic state normalisation and the azimuthal integral done:")
print(f"          Gamma      = (1/(16 pi E p v)) Integral_0^k_max dk  |M|^2")
print(f"          dE/dx      = (1/(16 pi E p))   Integral_0^k_max dk  k |M|^2      (each quantum carries v k)")
print(f"          D_loss^-1  = (1/E) dE/dx                                          (the survival criterion)")
check("C1 [CONTROL] the Cherenkov kinematics derive symbolically: cos(theta), k_max = 2(p - Ev)/(1-v^2), the "
      "threshold E > M/sqrt(1-v^2), and the on-shell identity 2 p.k = k^2 = -(1-v^2)|k|^2",
      same_cos and same_kmax and thr_ok and id_ok,
      f"cos(theta) {'matches' if same_cos else 'DIFFERS'}; k_max {'matches' if same_kmax else 'DIFFERS'}; "
      f"threshold {'matches' if thr_ok else 'DIFFERS'}; 2p.k - k^2 = "
      f"{sp.simplify(sp.expand(2*pdotk - k2inv))}")

# ---- matrix-element controls -------------------------------------------------------------------
g = np.diag([1.0, -1.0, -1.0, -1.0])
I2 = np.eye(2); sx = np.array([[0,1],[1,0]], dtype=complex); sy = np.array([[0,-1j],[1j,0]])
sz = np.array([[1,0],[0,-1]], dtype=complex); Z2 = np.zeros((2,2), dtype=complex)
gam = [np.block([[I2, Z2],[Z2, -I2]]).astype(complex)] + \
      [np.block([[Z2, s],[-s, Z2]]).astype(complex) for s in (sx, sy, sz)]
def slash(pv): return sum(pv[m]*g[m][m]*gam[m] for m in range(4))
rng = np.random.default_rng(19)
Mv = 0.7
pv3, ppv3 = rng.normal(size=3), rng.normal(size=3)
pv  = np.array([math.sqrt(Mv**2 + pv3 @ pv3), *pv3])
ppv = np.array([math.sqrt(Mv**2 + ppv3 @ ppv3), *ppv3])
pdotpp = pv[0]*ppv[0] - pv[1:] @ ppv[1:]
tr_dirac = np.trace((slash(ppv) + Mv*np.eye(4)) @ (slash(pv) + Mv*np.eye(4))).real
tr_pred = 4*(pdotpp + Mv**2)
# Maxwell: T^mu_mu = 0
A = rng.normal(size=(4,4)); F = A - A.T
Fud = g @ F @ g                                        # F^{mu nu} with indices raised
T_max = np.einsum('ma,na->mn', F, F @ g) - 0.25*g*np.einsum('ab,ab->', F, Fud)
tr_max = np.einsum('mn,mn->', np.linalg.inv(g), T_max)
# massless scalar, improved (xi = 1/6): trace = 2M^2 -> 0 at M = 0
print(f"\n    Matrix-element controls, with explicit Dirac matrices and an explicit random F_mu_nu:")
print(f"      Tr[(p'+M)(p+M)] = {tr_dirac:.10f}  vs  4(p.p' + M^2) = {tr_pred:.10f}")
print(f"      Maxwell T^mu_mu = {tr_max:.3e}  (identically zero in 4D: a photon cannot emit a conformally")
print(f"                        coupled scalar at tree level, whatever that scalar's speed)")
check("C2 [CONTROL] Tr[(p'+M)(p+M)] = 4(p.p' + M^2) with explicit gamma matrices, and Maxwell's stress tensor "
      "is traceless identically",
      abs(tr_dirac - tr_pred) < 1e-9*abs(tr_pred) and abs(tr_max) < 1e-10,
      f"Dirac trace rel. err {abs(tr_dirac/tr_pred - 1):.2e}; Maxwell trace {tr_max:.2e}")

# ===================================================================================================
head("B -- CONTROL: the rate for a mode with GRAVITATIONAL-strength (tensor) coupling")
# ===================================================================================================
print("    Interaction L = -(kappa/2) h_mu_nu T^mu_nu with kappa = sqrt(32 pi G).  For a primary at E >> M")
print("    the TT polarisation sum gives  Sum_pol |M|^2 = 2 p^4 sin^4(theta) / M_Pl^2  (M_Pl reduced), with")
print("    sin^2(theta) from section A.  This is the standard structure Moore & Nelson and Elliott, Moore &")
print("    Stoica use; the Lorentz-violating polarisation basis differs in O(1) factors, which is exactly")
print("    what this control is checking.")

# Everything below is parametrised by dd = delta = 1 - v rather than by v, and every difference
# (p - E), (p - E v), (1 - cos theta) is formed WITHOUT cancelling large numbers -- at delta ~ 1e-20 and
# E ~ 1e11 GeV a naive "1 - v*v" underflows to zero and the whole calculation is silently wrong.
def _om2(dd):   return dd*(2.0 - dd)                     # 1 - v^2, exact
def _p(EE, MM): return math.sqrt(EE*EE - MM*MM)
def _pmEv(dd, EE, MM):
    """p - E v = (p - E) + E delta, with p - E = -M^2/(p+E) formed exactly."""
    return EE*dd - MM*MM/(_p(EE, MM) + EE)

def k_max(dd, EE, MM):
    num = _pmEv(dd, EE, MM)
    return 2.0*num/_om2(dd) if num > 0 else 0.0

def sin2_theta(dd, kk, EE, MM):
    """1 - cos^2(theta), formed as u(2-u) with u = 1 - cos(theta) computed without cancellation."""
    u = (_pmEv(dd, EE, MM) - kk*_om2(dd)/2.0)/_p(EE, MM)
    return max(0.0, u*(2.0 - u))

def amp2_tensor(dd, kk, EE, MM):
    """Sum_pol |M|^2 for the tensor coupling: 2 p^4 sin^4(theta)/M_Pl^2."""
    s2 = sin2_theta(dd, kk, EE, MM)
    return 2.0*_p(EE, MM)**4*s2*s2/MPL2_RED

def amp2_trace(dd, kk, EE, MM, beta=1.0):
    """Sum_spins |M|^2, averaged over the initial spin, for a conformal (trace) coupling
       L = (beta/M_Pl) phi T^mu_mu on a DIRAC primary:
            <p'|T^mu_mu|p> = M ubar(p') u(p),  Sum/2 = 2 M^2 (p.p' + M^2),
            p.p' = M^2 + (1-v^2)k^2/2  (from the on-shell identity 2 p.k = k^2)."""
    return beta*beta*MM*MM*(4.0*MM*MM + _om2(dd)*kk*kk)/MPL2_RED

def amp2_trace_scalarprimary(dd, kk, EE, MM, beta=1.0):
    """the same for a SPIN-0 primary: <T^mu_mu> = 2M^2 + k^2_inv = 2M^2 - (1-v^2)k^2."""
    return beta*beta*(2.0*MM*MM - _om2(dd)*kk*kk)**2/MPL2_RED

def loss_inv(dd, EE, MM, amp2, kcut=None, **kw):
    """D_loss^-1 = (1/E)(1/(16 pi E p)) Int_0^min(kmax,kcut) dk k |M|^2, in GeV."""
    km = k_max(dd, EE, MM)
    if km <= 0: return 0.0
    if kcut is not None: km = min(km, kcut)
    integ = quad(lambda kk: float(kk)*amp2(dd, float(kk), EE, MM, **kw), [0, km/2, km])
    return float(integ)/(16*math.pi*EE*EE*_p(EE, MM))

# (a) the analytic small-delta limit and Milgrom's transcription of Moore & Nelson
print(f"\n    B.1  the analytic small-delta limit of the derived integral.  With M << E and delta = 1 - v << 1,")
print(f"         sin^2(theta) = 2 delta (1 - k/E) - M^2/E^2 and k_max -> E, so")
print(f"             D_loss^-1 = (1/E)(1/(16 pi E^2)) Int_0^E dk k 2E^4 [2 delta (1-k/E)]^2 / M_Pl^2")
print(f"                       = delta^2 E^3/(24 pi M_Pl^2)  =  (1/3) G delta^2 E^3.")
print(f"         Milgrom 2011 (arXiv:1102.1818) eq. (2) transcribes Moore & Nelson as D_loss^-1 = G p^3 Q,")
print(f"         with Q ~ 1e-3 (n-1)^2 where n = 1/v; the 1e-3 is their PARTONIC factor (each parton carries")
print(f"         ~0.1 p).  Stripping it, Q_coherent = delta^2, i.e. D_loss^-1 = G delta^2 E^3.")
delta_t = 1e-15
num_coeff = loss_inv(delta_t, E_MN, M_PROTON, amp2_tensor)/(G_N*delta_t**2*E_MN**3)
print(f"         numerically, from the full integral at delta = {delta_t:.0e}, E = {E_MN:.1e} GeV:")
print(f"             D_loss^-1 / (G delta^2 E^3) = {num_coeff:.6f}    (analytic 1/3 = {1/3:.6f};  "
      f"Moore & Nelson coherent: 1)")
coeff_ok = abs(num_coeff - 1/3) < 0.02 and (1/5 < num_coeff/1.0 < 5)

# (b) reproduce the published Galactic bound
def bound_delta(EE, MM, amp2, D, extra=1.0, **kw):
    """solve D_loss(delta) = D for delta = 1 - v, by bisection on log delta."""
    def f(logd):
        dd = math.exp(logd)
        Li = loss_inv(dd, EE, MM, amp2, **kw)*extra
        return (1.0/Li if Li > 0 else 1e300) - D
    lo, hi = math.log(1e-22), math.log(0.9)
    for _ in range(200):
        mid = 0.5*(lo + hi)
        if f(mid) > 0: lo = mid
        else: hi = mid
    return math.exp(0.5*(lo + hi))

d_MN   = bound_delta(E_MN,   M_PROTON, amp2_tensor, D_GAL, extra=PARTON)
d_task = bound_delta(E_TASK, M_PROTON, amp2_tensor, D_GAL, extra=PARTON)
print(f"\n    B.2  the bound this rate imposes, with Moore & Nelson's own partonic factor {PARTON:.0e} and a "
      f"10 kpc path:")
print(f"           E = {E_MN:.1e} GeV (3e20 eV, the energy MN quote):  1 - v <= {d_MN:.3e}")
print(f"           E = {E_TASK:.1e} GeV (1e20 eV, this lane's brief):   1 - v <= {d_task:.3e}")
print(f"         published (Moore & Nelson 2001, Galactic; the number L10 used):  1 - v <= {CHER_PUB:.1e}")
print(f"         ratio derived/published at MN's energy: {d_MN/CHER_PUB:.2f}x")
check("C3 [CONTROL] the tensor-coupled energy-loss rate derived here reproduces BOTH Moore & Nelson's "
      "coefficient (as transcribed by Milgrom 2011 eq. 2) and the published Galactic bound 1 - c <= 2e-15",
      coeff_ok and (1/5 < d_MN/CHER_PUB < 5),
      f"coefficient D_loss^-1/(G delta^2 E^3) = {num_coeff:.4f} vs analytic 1/3 and MN-coherent 1 "
      f"(agreement to a factor {max(3*num_coeff, 1/(3*num_coeff)):.1f} / {max(num_coeff, 1/num_coeff):.1f}); "
      f"derived Galactic bound {d_MN:.2e} vs published {CHER_PUB:.1e}, a factor {d_MN/CHER_PUB:.2f}. "
      f"The machinery is calibrated against the literature it is about to be used to overturn")

# ===================================================================================================
head("C -- what IC10's clock actually couples to, read off the action as published")
# ===================================================================================================
print("    IC10_LOCAL_CLOCK.md, the eta = 1 plateau (hand-transcribed):")
print("        S10|eta=1 = Int sqrt(-gtilde) [ m* Rtilde/2 + P(Xtilde, w) ] + S_m[e^(2w) gtilde, psi],")
print("        m* = m e^(-1/6),  Xtilde = -gtilde^{mu nu} T_mu T_nu / 2,  P_w = 0 the ALGEBRAIC w equation,")
print("    and the frozen ingredient I2 (CRISPY_FRIED_CHICKEN_RECIPE.md): S_m = S_m[g, psi], ONE physical")
print("    metric.  IC10 says the same: 'all ordinary matter still uses the single original physical metric g'")
print("    with g = e^(2w) gtilde.\n")
print("    C.1  THE STRUCTURAL FACT.  The clock field T does not appear in S_m AT ALL.  Matter sees only")
print("         g = e^(2w) gtilde.  The clock reaches matter ONLY because w is slaved to Xtilde by P_w = 0.")
print("         So the entire clock-matter vertex is carried by delta w, and delta w enters S_m as a")
print("         CONFORMAL rescaling -- which couples to the TRACE of the matter stress tensor and to")
print("         nothing else.  Derived symbolically, with a scalar matter field:")

w, Xt_psi, V = sp.symbols('w Xtilde_psi V', real=True)
# S_m density in gtilde variables: sqrt(-g) L_m with L_m = (1/2) g^{mu nu} d psi d psi - V
sm_dens = sp.exp(4*w)*(sp.exp(-2*w)*Xt_psi - V)          # sqrt(-g)/sqrt(-gtilde) * L_m
dSm_dw  = sp.simplify(sp.diff(sm_dens, w))
X_psi_g = sp.exp(-2*w)*Xt_psi                            # X_psi measured with g
T_trace = sp.simplify(2*X_psi_g - 4*(X_psi_g - V))       # T^mu_mu = 2X - 4L_m
sqrtg_T = sp.simplify(sp.exp(4*w)*T_trace)
conformal_ok = sp.simplify(dSm_dw + sqrtg_T) == 0
print(f"           d(S_m density)/dw = {dSm_dw}")
print(f"           sqrt(-g)/sqrt(-gt) * T^mu_mu = {sqrtg_T}")
print(f"           => dS_m/dw = -sqrt(-g) T^mu_mu   [{'exact' if conformal_ok else 'DIFFERS'}]  -- the whole")
print(f"           coupling, with no free structure left over.  The w field equation with matter present is")
print(f"           therefore  P_w + e^(4w) T^mu_mu = 0, and matter's TRACE is the only thing that sources it.")

print(f"\n    C.2  POSITIVE CONTROL: the test has teeth.  If the matter metric carried a DISFORMAL piece,")
print(f"         g_mu_nu = e^(2w) gtilde_mu_nu + B T_mu T_nu, the clock WOULD appear in S_m explicitly.")
B = sp.symbols('B', real=True)
# explicit 4x4: gtilde = diag(1,-1,-1,-1), T_mu = (t0, 0,0,0), matter gradient d psi = (a0_, a1, 0, 0)
t0, a0_, a1 = sp.symbols('t_0 a_0 a_1', real=True)
gt = sp.diag(1, -1, -1, -1)
Tm = sp.Matrix([t0, 0, 0, 0]); dps = sp.Matrix([a0_, a1, 0, 0])
g_conf = sp.exp(2*w)*gt
g_disf = sp.exp(2*w)*gt + B*Tm*Tm.T
kin_conf = sp.simplify((dps.T*g_conf.inv()*dps)[0, 0])
kin_disf = sp.simplify((dps.T*g_disf.inv()*dps)[0, 0])
dep_conf = sp.simplify(sp.diff(kin_conf, t0))
dep_disf = sp.simplify(sp.diff(kin_disf, t0))
print(f"           conformal metric:  g^ab dpsi_a dpsi_b = {kin_conf};   d/dT_0 = {dep_conf}")
print(f"           disformal metric:  d/dT_0 = {sp.simplify(dep_disf)}  -- NONZERO, a vertex proportional to")
print(f"           T^mu T^nu dpsi_mu dpsi_nu, i.e. to T^mu_nu contracted with the clock gradient, NOT to the trace.")
teeth = (dep_conf == 0) and sp.simplify(dep_disf) != 0
check("C4 [coupling] IC10's clock couples to ordinary matter ONLY through the conformal factor -- the vertex is "
      "to T^mu_mu and to nothing else -- and the test detects a direct coupling when one is present "
      "(disformal positive control)",
      conformal_ok and teeth,
      f"dS_m/dw = -sqrt(-g) T^mu_mu {'exactly' if conformal_ok else 'NOT reproduced'}; the clock field T is absent "
      f"from S_m for the conformal metric (d/dT_0 = 0) and present for a disformal one (d/dT_0 = "
      f"{sp.simplify(dep_disf)}), so the check is not vacuous.  ASSUMPTIONS, stated: (i) IC10's S_m[e^(2w)gtilde,psi] "
      f"is the complete matter action -- IC10 itself flags 'matter-coupled clock kinetic mixing must still be varied'; "
      f"(ii) w remains auxiliary (P_ww != 0), which L8-P6/P7/P8 verified on the sampled window")

print(f"\n    C.3  WHY THIS IS THE WHOLE QUESTION.  In Einstein-aether / khronometric theory -- which is what")
print(f"         IC5/IC6/IC7 were, and what Elliott, Moore & Stoica (2005) bound -- the spin-0 mode lives")
print(f"         INSIDE the gravitational sector: the aether supplies a preferred vector u_mu, the scalar's")
print(f"         effective polarisation carries a u_mu u_nu piece, and e_mu_nu T^mu_nu then picks out")
print(f"         T^00 ~ E^2.  That is why the spin-0 bound is as strong as the spin-2 one.  On IC10's eta = 1")
print(f"         plateau there is no such structure: L8 verified the DeWitt supermetric is lambda = 1")
print(f"         IDENTICALLY and m* = m e^(-1/6) > 0, so the graviton kinetic operator is Einstein's, with no")
print(f"         preferred-frame mixing to inherit.  The clock's polarisation is a SCALAR: it contracts with")
print(f"         g_mu_nu, not with u_mu u_nu.  The mode's character genuinely changed, and with it the vertex.")

# ===================================================================================================
head("D -- the bound a TRACE-coupled clock at gravitational strength actually has to satisfy")
# ===================================================================================================
print("    The on-shell trace vertices, all three derived above:")
print("      Dirac primary (a proton):   <p'|T^mu_mu|p> = M ubar(p')u(p);  Sum/2 = 2M^2 (p.p' + M^2)")
print("                                  with p.p' = M^2 + (1-v^2)k^2/2   =>  M^2 [4M^2 + (1-v^2)k^2]")
print("      spin-0 primary:             <T^mu_mu> = 2M^2 + k^2_inv = 2M^2 - (1-v^2)k^2")
print("      photon:                     <T^mu_mu> = 0 identically (C2)")
print("      massless conformal scalar:  0 (the xi = 1/6 improvement cancels the k^2 piece)")
print("\n    D.1  THE NAIVE ARGUMENT, TESTED AND CORRECTED.  A conformally coupled scalar is usually said to")
print("         decouple from ultra-relativistic matter because T^mu_mu = -M^2/E per particle, a (M/E)^2")
print("         suppression relative to the graviton's T^00 ~ E.  That is TRUE for soft/forward emission and")
print("         FALSE at Cherenkov kinematics, because the emitted quantum is spacelike with |q^2| =")
print("         (1-v^2)k^2, and the trace vertex picks that up.  This lane checked it rather than assuming it:")
d13 = 1.0 - math.sqrt(1/3.0)          # delta = 1 - c_s at the measured c_s^2 = 1/3
for lab, EE in (("E = 1e20 eV", E_TASK), ("E = 3e20 eV", E_MN)):
    kk = 0.5*k_max(d13, EE, M_PROTON)
    at, atr = amp2_tensor(d13, kk, EE, M_PROTON), amp2_trace(d13, kk, EE, M_PROTON)
    naive = (M_PROTON/EE)**4
    print(f"         {lab}, c_s^2 = 1/3, at k = k_max/2:  |M_trace|^2/|M_tensor|^2 = {atr/at:.3e},"
          f"   naive (M/E)^4 = {naive:.3e}   (naive too small by {naive/(atr/at):.1e}x)")
naive_ratio = (M_PROTON/E_MN)**4
kk_mid = 0.5*k_max(d13, E_MN, M_PROTON)
true_ratio = amp2_trace(d13, kk_mid, E_MN, M_PROTON)/amp2_tensor(d13, kk_mid, E_MN, M_PROTON)
check("C5 [vertex] the trace vertex is (M/E)^2-suppressed relative to the tensor vertex at Cherenkov kinematics, "
      "as the standard conformal-decoupling argument would have it",
      abs(true_ratio/naive_ratio - 1) < 0.5,
      f"it is NOT: the true ratio of |M|^2 at c_s^2 = 1/3 is {true_ratio:.2e}, the naive (M/E)^4 is "
      f"{naive_ratio:.2e}, too small by {naive_ratio/true_ratio:.1e}x.  The reason is the on-shell identity "
      f"2p.k = k^2 of C1: for a SUBLUMINAL mode the emitted quantum is spacelike, so p.p' = M^2 + (1-v^2)k^2/2 "
      f"grows with k and the trace does not vanish.  This FAIL is this lane correcting its own first-pass "
      f"reasoning, and it cuts AGAINST the clock -- the suppression is real but far smaller than 'conformal "
      f"scalars do not couple to radiation' suggests")

print(f"\n    D.2  the bound.  Coupling L = (beta/M_Pl) phi T^mu_mu, beta = 1 the gravitational-strength")
print(f"         benchmark (Brans-Dicke has beta = 1/sqrt(2 omega+3); f(R) has beta = 1/sqrt6 = 0.408).")
print(f"         Analytic small-delta limit of the same integral:  D_loss^-1 = (1/4) beta^2 G M^2 delta E,")
print(f"         LINEAR in delta, not quadratic -- so the bound scales quite differently from the tensor one.")
d_trace_MN   = bound_delta(E_MN,   M_PROTON, amp2_trace, D_GAL)
d_trace_task = bound_delta(E_TASK, M_PROTON, amp2_trace, D_GAL)
d_trace_s    = bound_delta(E_MN,   M_PROTON, amp2_trace_scalarprimary, D_GAL)
print(f"           {'primary / energy':<42} {'bound on 1 - c_s (beta = 1)':>28} {'vs L10 2e-15':>16}")
for lab, val in (("proton (Dirac), E = 1e20 eV", d_trace_task),
                 ("proton (Dirac), E = 3e20 eV", d_trace_MN),
                 ("spin-0 primary (not physical), E = 3e20 eV", d_trace_s)):
    print(f"           {lab:<42} {val:>28.3e} {val/CHER_PUB:>15.1e}x")
d_tensor_coh = bound_delta(E_MN, M_PROTON, amp2_tensor, D_GAL)          # no partonic factor, for comparison
print(f"         Note the third row, and it is not a rounding coincidence: for a SPIN-0 primary the trace")
print(f"         coupling gives NUMERICALLY THE SAME bound as the tensor coupling treated the same way")
print(f"         ({d_trace_s:.3e} vs the coherent tensor bound {d_tensor_coh:.3e}) -- both integrals reduce to")
print(f"         (2/3) delta^2 E^6 in the small-delta limit.  So the suppression found here is NOT a generic")
print(f"         property of conformal coupling: it is entirely the DIRAC structure <T^mu_mu> = M ubar(p')u(p),")
print(f"         which carries one power of M^2 that the spin-0 trace 2M^2 - (1-v^2)k^2 does not.  The physical")
print(f"         primary is a proton, so the fermionic row is the one that counts -- but the mechanism has to be")
print(f"         named correctly, and 'conformal scalars decouple from radiation' is NOT the mechanism.")
print(f"         No partonic factor is applied here, and that is deliberate: the trace charge of a proton is")
print(f"         its MASS (<p|T^mu_mu|p> = 2M_p^2 exactly for the hadron state), so the coherent treatment is")
print(f"         the right one.  The proton's trace form factor at |q^2| ~ ({math.sqrt((1-1/3.)*k_max(d13,E_MN,M_PROTON)**2):.1e} GeV)^2 would")
print(f"         suppress it enormously further; omitting it is CONSERVATIVE, i.e. generous to the exclusion.")
cs2 = 1/3.0; cs = math.sqrt(cs2); one_minus = 1 - cs
Dl_trace = 1.0/loss_inv(one_minus, E_MN, M_PROTON, amp2_trace)
Dl_tensor = 1.0/loss_inv(one_minus, E_MN, M_PROTON, amp2_tensor)
print(f"\n         At the measured c_s^2 = 1/3 (1 - c_s = {one_minus:.4f}), E = {E_MN:.0e} GeV:")
print(f"           trace coupling  (beta = 1):  D_loss = {Dl_trace/GEV_PER_INV_M:.3e} m = {Dl_trace/GEV_PER_INV_M/KPC_M:.3e} kpc"
      f"  -> D/D_loss = {D_GAL/Dl_trace:.2e}")
print(f"           tensor coupling (L10's):     D_loss = {Dl_tensor/GEV_PER_INV_M:.3e} m = {Dl_tensor/GEV_PER_INV_M/KPC_M:.3e} kpc"
      f"  -> D/D_loss = {D_GAL/Dl_tensor:.2e}")
print(f"           the trace coupling weakens the LOSS RATE by {Dl_trace/Dl_tensor:.2e}x and the SPEED BOUND by "
      f"{d_trace_MN/CHER_PUB:.2e}x")
check("C6 [bound] 1 - c_s <= 2e-15, the number L10 imposed, is the bound that applies to IC10's clock",
      abs(d_trace_MN/CHER_PUB - 1) < 0.5,
      f"it is NOT.  The bound that applies to a trace-coupled clock at gravitational strength is "
      f"1 - c_s <= {d_trace_MN:.2e} at 3e20 eV / {d_trace_task:.2e} at 1e20 eV -- L10's number is too tight by "
      f"{d_trace_MN/CHER_PUB:.1e}x in the speed, equivalently {Dl_trace/Dl_tensor:.1e}x in the loss rate AT "
      f"c_s^2 = 1/3 (the two differ because the tensor rate goes as delta^2 and the trace rate as delta).  L10's stated exclusion "
      f"factor 2.1e14 should read {one_minus/d_trace_MN:.1e}.  THIS FAIL IS L10 BEING CORRECTED, and the correction "
      f"is 5.9 orders of magnitude -- but see C8a: it does not by itself save c_s^2 = 1/3")

# ===================================================================================================
head("E -- where the exponential wall is actually evaluated: the MOND radius of the cosmic ray")
# ===================================================================================================
print("    L10 section D asked whether the construction's own screening u^2 = 1 - exp(-|a|/a_0) could")
print("    suppress the Cherenkov coupling, evaluated it at the AMBIENT galactic acceleration along the")
print("    10 kpc path (|a| ~ a_0 there), and concluded no.  That is the wrong place to evaluate it, and")
print("    the reason is published: Milgrom, 'Gravitational Cherenkov losses in MOND theories',")
print("    arXiv:1102.1818 (2011).  Radiation of wavenumber k is generated coherently at distance ~1/k")
print("    from the primary, and THERE the field is the primary's OWN, not the Galaxy's.  A high-energy")
print("    hadron carries a bubble of radius r_M = (G p / c a_0)^(1/2) inside which |a| >> a_0 and a")
print("    GR-compatible MOND theory is simply GR; waves with k > 1/r_M are not produced.\n")
print(f"    E.1  the numbers, on BOTH footings (M_p = {M_PROTON:.4f} GeV):")
print(f"      {'footing':<11} {'E [eV]':>9} {'r_M [m]':>12} {'k_dB^-1 [m]':>13} {'(r_M k_dB)^2':>14} "
      f"{'|a| at k_dB^-1 / a_0':>21} {'l_M = c^2/a_0 [m]':>19}")
mondnum = {}
for nm, a0v in FOOT:
    for EE in (E_TASK, E_MN):
        E_J = EE*1e9*1.602176634e-19                       # GeV -> J
        r_M = math.sqrt(G_SI*E_J/(C_LIGHT**2*a0v))         # m ; GM/r^2 = a_0 with M = E/c^2
        l_dB = 1.0/(EE*GEV_PER_INV_M)                      # m
        a_dB = G_SI*(E_J/C_LIGHT**2)/l_dB**2               # m/s^2, the primary's own field at k_dB^-1
        lM = C_LIGHT**2/a0v
        print(f"      {nm:<11} {EE*1e9:9.1e} {r_M:12.4e} {l_dB:13.4e} {(r_M/l_dB)**2:14.4e} {a_dB/a0v:21.4e} {lM:19.4e}")
        mondnum[(nm, EE)] = (r_M, l_dB, lM)
print(f"      columns 5 and 6 are equal BY THE IDENTITY a(r)/a_0 = (r_M/r)^2 -- that is what r_M means.")
print(f"      Milgrom's quoted values, for comparison: r_M ~ 3e-12 (cp/GeV)^(1/2) cm = "
      f"{3e-12*math.sqrt(E_MN)*1e-2:.3e} m at 3e20 eV; (r_M k_dB)^2 ~ 1e39 at cp = 3e11 GeV;")
print(f"      l_M ~ 2 pi D_H = {2*math.pi*D_HUBBLE_M:.3e} m.  Milgrom uses a_0 = 1.2e-10 m/s^2; rescaling his r_M to")
print(f"      the canonical footing gives {3e-12*math.sqrt(E_MN)*1e-2*math.sqrt(1.2e-10/A0_CANON):.3e} m, "
      f"{abs(3e-12*math.sqrt(E_MN)*1e-2*math.sqrt(1.2e-10/A0_CANON)/mondnum[('canonical', E_MN)][0] - 1)*100:.0f}% "
      f"from this lane's value -- the residual is his ~ sign.")

print(f"\n    E.2  CONTROL -- feeding that cutoff into the SAME rate formula reproduces Milgrom's result")
print(f"         independently.  For k << k_max, sin^2(theta) -> 1 - v^2, so with k_cut = 1/r_M and")
print(f"         k_cut^2 = a_0/(G E) (c = 1):")
print(f"             D_loss^-1 = (1/2) G E (1-v^2)^2 k_cut^2 = (1/2)(1-v^2)^2 a_0")
print(f"             => D_loss  = q l_M   with   q = 2/(1-v^2)^2   and   l_M = c^2/a_0,")
print(f"         E CANCELS EXACTLY -- Milgrom's eq. (4), derived here from scratch.  Numerically:")
print(f"      {'footing':<11} {'E [eV]':>9} {'q predicted':>12} {'q measured':>12} {'D_loss [m]':>13} "
      f"{'D_loss/10kpc':>14} {'D_loss/D_H':>12}")
q_pred = 2.0/(1 - cs2)**2
mond_safe_all, q_ok_all = True, True
for nm, a0v in FOOT:
    for EE in (E_TASK, E_MN):
        r_M, l_dB, lM = mondnum[(nm, EE)]
        kcut = 1.0/(r_M*GEV_PER_INV_M)                     # GeV
        Li = loss_inv(one_minus, EE, M_PROTON, amp2_tensor, kcut=kcut)
        Dl_m = (1.0/Li)/GEV_PER_INV_M
        q_meas = Dl_m/lM
        print(f"      {nm:<11} {EE*1e9:9.1e} {q_pred:12.4f} {q_meas:12.4f} {Dl_m:13.4e} {Dl_m/D_GAL_M:14.4e} "
              f"{Dl_m/D_HUBBLE_M:12.4e}")
        if not (0.7 < q_meas/q_pred < 1.4): q_ok_all = False
        if Dl_m < D_GAL_M: mond_safe_all = False
check("C7 [CONTROL] the derived rate, cut off at the primary's MOND radius, reproduces Milgrom 2011 eq. (4) "
      "D_loss = q l_M with the cosmic-ray energy cancelling exactly, q = 2/(1-v^2)^2 -- on both a_0 footings",
      q_ok_all,
      f"predicted q = 2/(1-c_s^2)^2 = {q_pred:.3f} at c_s^2 = 1/3; measured from the full integral at all four "
      f"(footing, energy) combinations to within 40%; E cancels because k_cut^2 = a_0/(G E) exactly undoes the "
      f"E-dependence of the rate.  This is an INDEPENDENT re-derivation of a published, refereed result, from "
      f"the same machinery that reproduced Moore & Nelson in C3")

print(f"\n    E.3  the framework's own wall is STRONGER than Milgrom's sharp cutoff.  IC5/IC10 define")
print(f"         w = (u-1) xi, and the static regular branch (IC-4, retained at eta = 0: 'the old exponential")
print(f"         constitutive equation therefore survives') has u^2 = 1 - exp(-|a|/a_0), so")
print(f"             1 - u  ~  (1/2) exp(-|a|/a_0)   =>   w ~ -(xi/2) exp(-|a|/a_0)   =>   e^(2w) -> 1")
print(f"         and the ENTIRE clock-matter vertex, which is carried by w alone (C.1), switches off")
print(f"         exponentially in |a|/a_0.  In the cosmic ray's own near field at the de Broglie radius,")
for nm, a0v in FOOT:
    r_M, l_dB, lM = mondnum[(nm, E_MN)]
    E_J = E_MN*1e9*1.602176634e-19
    a_dB = G_SI*(E_J/C_LIGHT**2)/l_dB**2
    print(f"             {nm:<10}: |a|/a_0 = {a_dB/a0v:.3e}   =>   coupling ~ exp(-{a_dB/a0v:.2e})")
print(f"         which is not a factor of 1e-39, it is zero for every purpose.  The residual emission comes")
print(f"         only from k < 1/r_M, and E.2 shows that is D_loss ~ {q_pred:.1f} l_M -- longer than a Hubble")
print(f"         distance.  Note this is with the FULL tensor coupling; the trace coupling of section D makes")
print(f"         it {Dl_trace/Dl_tensor:.0e}x safer still.")

# ===================================================================================================
head("F -- the verdict on c_s^2 = 1/3, arm by arm")
# ===================================================================================================
survive_trace = D_GAL/Dl_trace < 1.0
print(f"    F.1  trace coupling alone, NO screening, point-like proton, beta = 1, 10 kpc:")
print(f"           D/D_loss = {D_GAL/Dl_trace:.3e}   ->  c_s^2 = 1/3 is {'ALLOWED' if survive_trace else 'EXCLUDED'} "
      f"by this arm alone, by {max(D_GAL/Dl_trace, Dl_trace/D_GAL):.2e}x in the loss rate")
print(f"           (required suppression of the coupling: beta^2 <= {Dl_trace/D_GAL:.2e}, i.e. beta <= "
      f"{math.sqrt(Dl_trace/D_GAL):.2e})")
check("C8a [verdict] c_s^2 = 1/3 survives gravitational Cherenkov on the CORRECTED coupling alone, with no "
      "screening applied",
      survive_trace,
      f"it does not: D/D_loss = {D_GAL/Dl_trace:.2e} at beta = 1.  The corrected bound is 1 - c_s <= "
      f"{d_trace_MN:.2e}, and 1 - c_s = {one_minus:.4f} exceeds it by {one_minus/d_trace_MN:.1e}x.  So L10's "
      f"CONCLUSION survives on this arm even though its NUMBER was wrong by {d_trace_MN/CHER_PUB:.1e}x")

mond_ok = True
print(f"\n    F.2  with the framework's own high-acceleration GR limit applied where the radiation is generated:")
print(f"      {'footing':<11} {'E [eV]':>9} {'coupling':>9} {'D_loss [m]':>13} {'D_loss / 10 kpc':>17} {'verdict':>10}")
for nm, a0v in FOOT:
    for EE in (E_TASK, E_MN):
        r_M, l_dB, lM = mondnum[(nm, EE)]
        kcut = 1.0/(r_M*GEV_PER_INV_M)
        for cl, fn in (("tensor", amp2_tensor), ("trace", amp2_trace)):
            Li = loss_inv(one_minus, EE, M_PROTON, fn, kcut=kcut)
            Dl_m = (1.0/Li)/GEV_PER_INV_M
            ok = Dl_m > D_GAL_M
            if not ok: mond_ok = False
            print(f"      {nm:<11} {EE*1e9:9.1e} {cl:>9} {Dl_m:13.4e} {Dl_m/D_GAL_M:17.4e} {'SAFE' if ok else 'FAILS':>10}")
check("C8b [verdict] c_s^2 = 1/3 survives gravitational Cherenkov once the high-acceleration GR limit is applied "
      "where the radiation is generated (Milgrom 2011), on BOTH a_0 footings and BOTH couplings",
      mond_ok and mond_safe_all,
      f"yes, and not marginally: even with the FULL gravitational-strength tensor coupling the loss distance is "
      f"{q_pred:.1f} l_M, {(q_pred*mondnum[('canonical', E_MN)][2])/D_GAL_M:.2e}x the Galactic path and "
      f"{(q_pred*mondnum[('canonical', E_MN)][2])/D_HUBBLE_M:.1f}x the Hubble distance.  With the trace coupling "
      f"of section D it is safer by a further {Dl_trace/Dl_tensor:.0e}x.  Footing-independent")

# ===================================================================================================
head("G -- the other constraints that could bite on a subluminal, minimally coupled clock")
# ===================================================================================================
print("    G.1  CAUSALITY.  Subluminal is the easy direction: the clock cone lies strictly INSIDE the metric")
print("         null cone, so the causal future of the coupled system is contained in the metric light cone")
print("         and no closed causal curve can be built from it.  The preferred foliation is not even needed")
print("         for this -- it is needed only for the SUPERLUMINAL case, where the clock's own level sets")
print("         T = const provide a global time function that all cones respect.  Worth recording because")
print("         L8-D7 found a superluminal band 0.0267 < S < 0.0377 inside eta = 1, in this solution's PAST:")
print("         that band needs the foliation argument, this one does not.")
causal_ok = cs < 1.0
check("C9 [causality] the subluminal clock cone is causal -- it lies inside the metric null cone, so no closed "
      "causal curve can be formed",
      causal_ok, f"c_s = {cs:.6f} < 1, cone strictly inside; the preferred foliation is a spare argument here, "
                 f"and is the one that would be needed for L8-D7's superluminal band at S < 0.0377")

print(f"\n    G.2  OTHER EMITTERS.  Cherenkov by something other than a hadron:")
m_nu = 0.1e-9                                              # GeV, a generous neutrino mass
print(f"      photons:    T^mu_mu = 0 identically in 4D (C2), so a photon CANNOT emit a conformally coupled")
print(f"                  clock quantum at tree level, at any speed.  LHAASO's PeV photons give nothing.")
print(f"      neutrinos:  the vertex is proportional to m_nu^2; against a proton the rate is down by")
print(f"                  (m_nu/M_p)^4 = {(m_nu/M_PROTON)**4:.2e}.  IceCube's PeV events give nothing.")
print(f"      gravitons:  the tensor mode is exactly luminal here (c_T = 1, an exact action identity, IC9/IC10,")
print(f"                  verified L8-A2/A3), so the channel Elliott, Moore & Stoica actually bound is closed at")
print(f"                  zero.  A graviton could emit a clock quantum only via the background clock gradient")
print(f"                  Tbar_mu, and there is no observed ultra-high-energy graviton flux to constrain it")
print(f"                  (GW170817's quanta are ~1e-13 eV).  Vacuous, not passed.")
channels_ok = True
check("C10 [channels] photons, neutrinos or gravitons impose a Cherenkov bound on this clock that is stronger "
      "than the hadronic one",
      False,
      f"none of them do: photon vertex identically zero (Maxwell trace = {tr_max:.1e}), neutrino rate down by "
      f"{(m_nu/M_PROTON)**4:.1e}, no UHE graviton flux exists.  This FAIL means 'no additional constraint found', "
      f"which is the honest reading -- the hadronic channel is the binding one and it is the one computed above")

print(f"\n    G.3  BINARY PULSARS.  A conformally coupled scalar generically radiates DIPOLE energy from an")
print(f"         asymmetric binary, and PSR J0348+0432 / J1738+0333 bound the scalar-charge difference at the")
print(f"         |alpha_A - alpha_B|^2 ~ 1e-6 level.  Two things are true and both must be said:")
print(f"           (i) this is a HIGH-acceleration system, so the same exponential wall applies, and it applies")
print(f"               HERE at the right place (the binary's own field, not an ambient one).  Milgrom 2011 makes")
print(f"               exactly this point: 'constraints on solar-system and binary-pulsar limits on preferred-")
print(f"               frame parameters are easily satisfied by GR-compatible MOND theories, inasmuch as these")
print(f"               limits pertain to experiments in high-acceleration systems'.  L10's own K6 is the same")
print(f"               statement in the Solar System (Cassini at 5.8e5 a_0).")
print(f"          (ii) the dipole coefficient is NOT computed here and cannot be, because IC10's clock-matter")
print(f"               sector is one of its own stated open items ('matter-coupled clock kinetic mixing must")
print(f"               still be varied').  It is a live constraint, not a passed one.")
print(f"    G.4  CMB.  c_s^2 = 1/3 is exactly the radiation sound speed; a component with that sound speed does")
print(f"         not cluster below its sound horizon and its perturbations are CMB-degenerate with a smooth")
print(f"         relativistic fluid.  The CMB constrains the clock's ENERGY DENSITY (N_eff), not its speed --")
print(f"         which is L10's K5b arm, unchanged and still open.  No bound on c_s from the CMB.")
check("C11 [pulsar/CMB] binary pulsars or the CMB impose a bound on the clock's SOUND SPEED that is binding at "
      "c_s^2 = 1/3",
      False,
      "neither does.  The CMB constrains the clock's density, not c_s -- c_s^2 = 1/3 is the radiation value and is "
      "perturbatively degenerate.  Binary-pulsar dipole radiation constrains the COUPLING, not the speed, is "
      "subject to the same high-acceleration wall that Cassini already passes by 3.7e4x (L10 K6), and its "
      "coefficient is uncomputed here because IC10's matter-coupled clock sector is an open item.  Recorded as "
      "the constraint that actually deserves the lead's next calculation")

# ===================================================================================================
head("H -- VERDICT, as a conditional, with the deciding input named")
# ===================================================================================================
print(f"    THE BOUND APPLIES AT STRENGTH X IF THE CLOCK COUPLES IN WAY Y:")
print(f"      Y1  the mode propagates in the GRAVITATIONAL sector with preferred-frame mixing (DeWitt")
in_grav = f"1 - c_s <= {CHER_PUB:.0e}"
print(f"          lambda != 1, no first-class Hamiltonian constraint, an aether vector u_mu in the mode's")
print(f"          polarisation): the vertex is e_mu_nu T^mu_nu with e ~ u_mu u_nu, hence ~E^2, and")
print(f"          X = {in_grav}.  This is IC5/IC6/IC7, it is what Elliott, Moore & Stoica bound, and it")
print(f"          is what L10 assumed.  It is ALSO what IC10 becomes OFF the eta = 1 plateau: L8-P9/P10 found")
print(f"          IC9's lambda = 1/3 + 2/(3 J9) != 1 and a residual e^(2w) once eta != 1.")
print(f"      Y2  the mode is a shift-symmetric k-essence clock in an EXACTLY Einstein metric sector, coupled")
print(f"          to matter only through a conformal factor (IC10 at eta = 1, as published, plus frozen")
print(f"          ingredient I2): the vertex is T^mu_mu, and X = 1 - c_s <= {d_trace_MN:.1e} at beta = 1 --")
print(f"          {d_trace_MN/CHER_PUB:.0e}x weaker than L10's number, but STILL violated by c_s^2 = 1/3.")
print(f"      Y3  the same, plus the theory's high-acceleration GR limit holding in the cosmic ray's own near")
print(f"          field (Milgrom 2011): NO BOUND AT ALL -- D_loss = {q_pred:.1f} l_M > 2 pi D_H, for any")
print(f"          0 < c_s <= 1, on both footings, even at full gravitational-strength coupling.")
print(f"\n    THE DECIDING INPUT, stated so the lead can settle it from its own action and nothing else:")
print(f"      Does the clock-matter conformal coupling switch off in the high-acceleration limit?  Concretely:")
print(f"      expand IC10's w equation with matter present,  P_w + e^(4w) T^mu_mu = 0, on the STATIC branch,")
print(f"      and evaluate  dw/dXtilde  as |a|/a_0 -> infinity.  If  dw/dXtilde -> 0 at least as fast as")
print(f"      (a_0/|a|)^(1/2) -- and IC-4's u^2 = 1 - exp(-|a|/a_0) with w = (u-1) xi says it goes as")
print(f"      exp(-|a|/a_0), vastly faster -- then Y3 holds, there is no Cherenkov bound, and sigma = 1/3")
print(f"      SURVIVES.  If instead the coupling stays O(1) at high acceleration (i.e. the theory is not")
print(f"      GR-compatible in Milgrom's sense on the branch the cosmic ray's near field probes), Y2 holds and")
print(f"      sigma = 1 is forced.  One calculation decides it, and it is the same calculation IC10 already")
print(f"      lists as open item 3 (the sourced galactic branch and PPN).")
print(f"\n    WHAT L10 GOT WRONG, quantified, since it is this lane's own result:")
print(f"      (a) it used the bound for a mode with GRAVITATIONAL-sector coupling on a mode L8 later showed is")
print(f"          not one.  The applicable bound is {d_trace_MN:.1e}, not {CHER_PUB:.0e}: too tight by "
      f"{d_trace_MN/CHER_PUB:.1e}x in speed,")
print(f"          {Dl_trace/Dl_tensor:.1e}x in rate.  Its 'excluded by 2.1e14x' should read "
      f"'{one_minus/d_trace_MN:.1e}x'.")
print(f"      (b) its escape analysis (K8) evaluated the exponential wall at the AMBIENT galactic acceleration")
print(f"          along the cosmic-ray path.  That is the wrong place.  The cosmic ray is the SOURCE, and the")
print(f"          radiation of wavenumber k is generated at ~1/k from it, where its own field gives |a|/a_0 =")
print(f"          {G_SI*(E_MN*1e9*1.602176634e-19/C_LIGHT**2)/(1.0/(E_MN*GEV_PER_INV_M))**2/A0_CANON:.1e}, not ~1.  "
      f"K8's conclusion 'the exp wall cannot rescue this gate' is")
print(f"          WITHDRAWN; the wall does rescue it, by the published mechanism this lane re-derived in E.2.")
print(f"      (c) what L10 got RIGHT and this lane confirms: the mode's speed is the invariant that matters,")
print(f"          the tensor sector is not the issue, and if the coupling does NOT screen then c_s^2 = 1/3 is")
print(f"          still excluded -- by {one_minus/d_trace_MN:.0e}x rather than 2e14x.  The PPN arm (K6) is untouched.")
verdict = mond_ok and mond_safe_all
check("C12 [VERDICT] L10's exclusion of c_s^2 = 1/3 by gravitational Cherenkov is correct AS STATED (bound "
      "2e-15, exclusion 2.1e14x, exp wall cannot rescue)",
      (not survive_trace) and (not mond_ok),
      f"it is not.  The bound is {d_trace_MN/CHER_PUB:.0e}x weaker than stated, and the exp wall DOES rescue the "
      f"gate once it is evaluated where the radiation is generated rather than along the ambient path.  Handoff "
      f"A5 must be rewritten as a conditional.  The lead's construction is ALIVE with a subluminal clock IF its "
      f"clock-matter coupling screens at high acceleration -- which its own static branch says it does -- and only "
      f"then; sigma = 1 is NOT forced by Cherenkov as things stand")

print(f"\n  Caveats, stated in the direction they cut:")
print(f"  * AGAINST the clock: C5.  The naive 'conformal scalars decouple from radiation' argument is FALSE at")
print(f"    Cherenkov kinematics, because 2p.k = k^2 makes the emitted quantum spacelike.  Without screening the")
print(f"    trace coupling still excludes c_s^2 = 1/3 by {one_minus/d_trace_MN:.0e}x.  Do not quote the trace")
print(f"    coupling alone as a rescue.")
print(f"  * AGAINST the clock: everything here is the eta = 1 plateau.  L8-P10 showed the Einstein form is a")
print(f"    statement about that plateau, not the theory; off it, lambda != 1 and Y1 applies again with the full")
print(f"    2e-15.  A transition that spends any time off the plateau at low acceleration reopens this.")
print(f"  * AGAINST the clock: the dipole/pulsar arm (G.3) is a genuine live constraint that this lane has NOT")
print(f"    computed, and it constrains exactly the coupling beta that the Cherenkov verdict now hangs on.")
print(f"  * FOR the clock: the proton trace form factor at |q^2| ~ (2e11 GeV)^2 is omitted entirely, which is")
print(f"    conservative by many orders of magnitude in the direction of exclusion.")
print(f"  * FOR the clock: the TT polarisation sum used in the tensor control is the Lorentz-invariant one; a")
print(f"    Lorentz-violating basis changes O(1) factors.  C3 shows those factors are within a factor {d_MN/CHER_PUB:.1f}.")
print(f"  * The Milgrom cutoff is imported, not re-derived from IC10: E.2 re-derives its CONSEQUENCE")
print(f"    (D_loss = q l_M) from this lane's own rate formula, but the premise -- that the coupling is switched")
print(f"    off inside r_M -- is the deciding input named above and is NOT established for IC10's clock.")
print(f"  total {time.time()-T0:.0f}s")

print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(2 if FAILS else 0)
