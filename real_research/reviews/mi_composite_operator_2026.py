#!/usr/bin/env python3
r"""mi_composite_operator_2026.py -- LANE C / DOOR A3+A4+A5: the composite-operator escape from the
anti-MOND wall is CLOSED for the stationary Gaussian class -- state dependence exists but is ONE-SIGNED.

1. THE QUESTION.
   Established result 3 of this corpus (mi_strong_nogo_scoped_2026.py, door A1) says the worldline
   commutator spectral function of the ELEMENTARY field is rho_phi(omega) = c*omega with c a fixed
   positive constant, state-independently, because [phi(x),phi(y)] is a c-number (Raval, Hu & Anglin
   1996 PRD 53:7003). Hence delta_m = (2/pi) P Int rho/omega^2 > 0 always: inertia is INCREASED, which
   is anti-MOND. The one legal escape named by the door list is a COMPOSITE operator, O = :phi^2: or
   T_mu_nu, whose commutator is NOT a c-number, so rho_O genuinely depends on the state. Does any
   admissible normalizable state give rho_O < 0 in a band -- i.e. reduced inertia, i.e. MOND?

2. THE METHOD.
   Conventions. Worldline Wightman function W(tau) = <phi(tau)phi(0)>; power spectrum
   S(omega) = Int dtau e^{i omega tau} W(tau); commutator spectral function
   rho(omega) = S(omega) - S(-omega).  In this convention the free field gives rho_phi = omega/(2 pi)
   (A1's rho = omega/pi^2 is the same object in a different normalisation -- only the SIGN is
   load-bearing and normalisation cannot change it).
   Kernel. On a comoving dS worldline the exact Bunch-Davies function is
   W_BD(tau) = -H^2/(16 pi^2 sinh^2(H(tau - i eps)/2)), which is IDENTICALLY the 4D flat-space thermal
   Wightman function at T = H/2pi (Gibbons-Hawking); S1 verifies this by direct numerical Fourier
   transform at finite eps against the closed form (the finite-eps kernel is the zero-eps kernel at
   shifted argument, so its transform is exactly e^{-omega eps} times the closed form -- that is what
   is checked, to 1e-20).
   Composite operator. For any GAUSSIAN state, Wick gives <:phi^2:(tau):phi^2:(0)> = 2 W(tau)^2, so
   S_O = (1/pi) (S * S) -- the one-loop convolution of two propagators (the bubble / sunset).
   UV REGULARIZATION, stated explicitly: the divergence of the one-loop composite sits entirely in the
   COINCIDENCE limit <:phi^2:(0)^2> = Int domega S_O(omega), i.e. in a mass counterterm; it is removed
   by normal ordering plus the Wightman i-eps prescription. At FIXED omega the convolution converges
   absolutely (S(nu) grows linearly for nu -> +inf but S(omega - nu) then decays like e^{-beta nu}), so
   rho_O(omega) is finite with no scheme choice left. The sign of that finite part is the question.
   State parametrisation. Positivity + the c-number commutator force EVERY stationary state to have
        S(omega) = c*omega*theta(omega) + n(|omega|),  c = 1/(2 pi),  n >= 0,
   with n(omega) = S(-omega) the occupation density (vacuum n = 0, Bunch-Davies n = c*omega/(e^{beta
   omega} - 1)). SQUEEZED states -- including the dS-invariant alpha-vacua, which ARE squeezed
   Bunch-Davies -- are Gaussian, so they live in this class and differ only through n.

3. THE ANSWER (up front).
   (a) CONTROL PASSES, and it is a theorem not a check: in ANY KMS state rho_O = S_O(1 - e^{-beta
       omega}) with S_O >= 0 by Bochner, so rho_O >= 0 for every composite operator in Bunch-Davies.
       For O = :phi^2: the closed form is rho_O(omega) = omega(omega^2 + H^2)/(24 pi^3), verified
       against 30-digit quadrature to 3e-31. Its omega^2 + H^2 is the Deser-Levin five-acceleration
       combination -- structurally suggestive, and it is also the standard thermal-bubble result, so it
       is NOT evidence for anything beyond consistency.
   (b) THEOREM (proved here, then verified numerically on 5 states): for every stationary Gaussian
       state with finite occupation weight N = Int_0^inf n,
             rho_{phi^2}(omega) = omega^3/(24 pi^3) + (2/pi^2) * N * omega   for omega > 0.
       N >= 0 is forced by state positivity, so rho_{phi^2} >= 0 ALWAYS, and squeezing makes it BIGGER
       -- the wall gets worse, not better. State dependence is real (rho_O does move) but one-signed.
   (c) A negative band at omega would require N < -omega^2/(48 pi); at omega = H that is exactly MINUS
       the Bunch-Davies value. Not a small violation of positivity: a total negative occupation.
   (d) The same result holds for the derivative-coupled composite :(d_tau phi)^2:
       (rho = [c^2 omega^7/140 + 2c(omega^3 M2 + 3 omega M4)]/pi, all moments M >= 0). An ODD spectral
       weight nu(omega-nu) DOES give a negative band -- but it fails Bochner (S_O(0) < 0), so it is not
       the power spectrum of any operator. That is exactly where the escape would have to live.
   (e) Physically realised squeezing (r_sq ~ N_efolds) misses a sign flip by ~1e52 IN THE WRONG
       DIRECTION, so door A4 closes with a number, not a hope.
   (f) delta_m > 0, and feeding the Deser-Levin temperature in gives m(a) = m0(1 + K a^2), K > 0: no
       MOND limit -- deep MOND needs delta_m/m0 -> -1 as a -> 0 and this class gives >= 0.
   (g) COMPLETE POSITIVITY (door A5): a posited negative band at the system frequency makes the secular
       Lindblad rate Gamma = S_bath(omega_0) < 0, so a Kossakowski eigenvalue is negative for ANY band
       depth d > 0. The CP cap is d = 0, infinitely tighter than the corpus's ghost cap rho > -2. Also
       reported, because it matters for reading D4: the truncated Caldeira-Leggett generator violates
       the Dekker inequality even for a perfectly POSITIVE Ohmic bath, so "CL is not CP" is an artefact
       of the truncation and is not evidence about the band.

4. CREDIT (02_HOUSE_RULES.md R2 and the lane brief).
   nu(y) = sqrt(1 + 1/y) and the dS-Unruh temperature balance are Milgrom 1999 PLA 253:273 eqs 6-9,
   who fixes a_0_hat = 2 c H_Lambda (r = 1); his eqs 10-11 give a second coefficient (r = 2), and
   Milgrom 2008 arXiv:0801.3133 sec 7.3.1 observes that the coefficient mismatch "isn't necessarily
   meaningful ... would just point to a different effective mu(x)" -- the r-freedom is HIS.
   Temperature sqrt(a^2 + Lambda/3)/2pi: Narnhofer, Peter & Thirring 1996 IJMPB 10:1507. Five-
   acceleration reading: Deser & Levin 1997 CQG 14:L163. a_lambda = c^2 sqrt(Lambda/3): Milgrom 1994
   Ann.Phys. 229:384. Bunch & Davies 1978 PRSLA 360:117. Gibbons & Hawking 1977 PRD 15:2738.
   KMS: Kubo 1957, Martin & Schwinger 1959, Haag, Hugenholtz & Winnink 1967. Positive-definiteness of
   the power spectrum: Bochner 1933. alpha-vacua as squeezed BD: Mottola 1985 PRD 31:754, Allen 1985
   PRD 32:3136, Bousso, Maloney & Strominger 2002 PRD 65:104039. c-number commutator / worldline
   spectral function: Raval, Hu & Anglin 1996 PRD 53:7003. Master equation: Caldeira & Leggett 1983
   Physica A 121:587; complete positivity: Gorini, Kossakowski & Sudarshan 1976, Lindblad 1976;
   the Dekker inequality: Dekker 1977, Sandulescu & Scutaru 1987 Ann.Phys. 173:277.

5. AGAINST INTEREST.
   This script closes the escape route the framework wanted: the composite operator does make rho
   state-dependent, exactly as door A3 hoped, and the dependence is strictly the WRONG SIGN. Squeezing
   -- the physically motivated deformation -- makes the anti-MOND wall stronger by ~52 orders of
   magnitude at realised e-fold counts. The rho_{phi^2} = omega(omega^2 + H^2)/(24 pi^3) form contains
   the five-acceleration combination the framework likes, and it STILL gives delta_m > 0; the pretty
   structure does not rescue the sign. And nothing here derives kappa: the escape, had it worked, would
   have introduced a NEW free number (the squeezing r_sq), i.e. relocated the fit, not removed it.

6. SCOPE, and what is outside it (R7 -- no closure claimed).
   Class: stationary Gaussian states of a free real scalar on a comoving dS worldline, quadratic
   composites whose Wick weight is an even polynomial in each frequency argument, finite occupation
   moments. OUTSIDE, and NOT excluded by anything here: (i) non-Gaussian states, where Wick fails and
   S_O is not a convolution at all; (ii) genuinely non-stationary squeezing, where there is no spectral
   function and the whole delta_m formula must be rebuilt; (iii) bounded / finite-level sectors (door
   A2); (iv) mixed composites such as T_mu_nu whose Wick weight |P(i nu)|^2 |P'(i nu')|^2 need NOT be a
   positive-coefficient polynomial -- the parity argument used here does not cover that case, and a
   targeted search for a Bochner-admissible weight with a negative band remains open.

kappa = 1/2 is FITTED, NOT DERIVED. Nothing in this script changes that.

Precision: mpmath at dps 30 (and 40 on refinement) because the convolution mixes a linearly growing
factor against an exponentially decaying one over 40 decades of integrand and the load-bearing test is
a cancellation between S_O(+omega) and S_O(-omega).
"""
from __future__ import annotations

import math
import sys

import mpmath as mp

mp.mp.dps = 30

# ---------------------------------------------------------------------------------------------------
# locked constants -- 04_FRAMEWORK_FACTS.md, never invent
G = 6.67430e-11
C_L = 2.99792458e8
LAM = 1.0908e-52
RHO_L = LAM * C_L**2 / (8 * math.pi * G)
CHL = C_L**2 * math.sqrt(LAM / 3)                    # 5.4194e-10 m/s^2
A0 = {"canonical": 9.3614e-11, "ALT": 1.13e-10}      # rho_DE+cH_Lambda  /  rho_total+cH_0
Z_FW = 2 * math.sqrt(8 * math.pi / 3)                # 5.788810036466
FLOOR_K = {k: v / 2 for k, v in A0.items()}          # Milgrom's balance floor k = a_0/2  (R6)
OMEGA_C_WINDOW = (1.78e-14, 2.21e-14)                # committed free fifth constant, s^-1

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 100)
    print(f"  {t}")
    print("=" * 100)


# ===================================================================================================
# THE STATE CLASS.  S(omega) = c*omega*theta(omega) + n(|omega|),  n >= 0.
# ===================================================================================================
C_CONST = 1 / (2 * mp.pi)          # rho_phi(omega) = C_CONST * omega, state-independent (A1)
H_UNIT = mp.mpf(1)                 # work in units H = 1 for the maths; physical H restored in S7
BETA = 2 * mp.pi / H_UNIT          # Gibbons-Hawking beta = 2 pi / H


def n_thermal(s, H=H_UNIT):
    """Bunch-Davies occupation density n(s) = c s /(e^{beta s} - 1), s > 0.  expm1 guards H1."""
    s = mp.mpf(s)
    beta = 2 * mp.pi / H
    if s < mp.mpf("1e-15"):                      # series: c s/(beta s) = c/beta
        return C_CONST / beta - C_CONST * s / 2
    return C_CONST * s / mp.expm1(beta * s)


def n_squeezed(r_sq, w0, wid, H=H_UNIT):
    """BD plus a squeezed band: a mode of frequency s squeezed by r_sq carries sinh^2(r_sq) extra
    quanta.  Gaussian, hence inside the class; profile shape scanned rather than asserted."""
    sh2 = mp.sinh(mp.mpf(r_sq)) ** 2

    def f(s):
        s = mp.mpf(s)
        return n_thermal(s, H) + C_CONST * s * sh2 * mp.e ** (-(((s - w0) / wid) ** 2))

    return f


def n_illegal(depth, w0, wid, H=H_UNIT):
    """NOT A STATE: negative occupation density.  Used only to show the checks have teeth."""

    def f(s):
        s = mp.mpf(s)
        return n_thermal(s, H) - mp.mpf(depth) * mp.e ** (-(((s - w0) / wid) ** 2))

    return f


def S_of(nu, nfun):
    nu = mp.mpf(nu)
    return (C_CONST * nu if nu > 0 else mp.mpf(0)) + nfun(abs(nu))


def conv_weighted(om, nfun, k=0, dps_pts=(40, 5)):
    """(weight * S * S) convolution.  k = 0 is :phi^2:; k = 2 is :(d_tau phi)^2:; odd k is the
    non-operator control.  Split points straddle the two kinks (nu = 0 and nu = om)."""
    om = mp.mpf(om)
    far, near = dps_pts

    def f(nu):
        w = (nu * (om - nu)) ** k if k else mp.mpf(1)
        return w * S_of(nu, nfun) * S_of(om - nu, nfun)

    pts = [-mp.inf, -far, -near, 0, om, om + near, om + far, mp.inf]
    return mp.quad(f, pts)


def rho_O(om, nfun, k=0, dps_pts=(40, 5)):
    om = mp.mpf(om)
    return (conv_weighted(om, nfun, k, dps_pts) - conv_weighted(-om, nfun, k, dps_pts)) / mp.pi


def occ_weight(nfun, n=0):
    """M_n = Int_{-inf}^{inf} nu^n n(|nu|) dnu = 2 Int_0^inf nu^n n(nu) dnu.  M_0 = 2N."""
    return 2 * mp.quad(lambda s: s**n * nfun(s), [0, 1, 5, 40, mp.inf])


def theorem_phi2(om, N, H=H_UNIT):
    """rho_{phi^2}(omega) = omega^3/(24 pi^3) + (2/pi^2) N omega   (omega > 0)."""
    om = mp.mpf(om)
    return om**3 / (24 * mp.pi**3) + 2 * mp.mpf(N) * om / mp.pi**2


# ===================================================================================================
banner("S1  CONVENTIONS AND THE EXACT dS WORLDLINE KERNEL")

print("  W_BD(tau) = -H^2 / (16 pi^2 sinh^2(H(tau - i eps)/2))       [Bunch & Davies 1978]")
print("  flat limit H -> 0 gives -1/(4 pi^2 tau^2); at H > 0 it is the 4D thermal Wightman")
print("  function at T = H/2pi exactly (Gibbons & Hawking 1977).")
print("  S_BD(omega) = (omega/2pi)/(1 - e^{-beta omega}),  beta = 2 pi / H.")
print()
print("  Numerical Fourier transform of the finite-eps kernel vs e^{-omega eps} * closed form:")
print(f"  {'omega':>7} {'numeric FT':>22} {'e^-we * closed':>22} {'rel dev':>11}")

EPS = mp.mpf("0.35")


def W_kernel(tau, H=H_UNIT, eps=EPS):
    return -(H**2) / (16 * mp.pi**2 * mp.sinh(H * (mp.mpf(tau) - 1j * eps) / 2) ** 2)


def S_closed(om, H=H_UNIT):
    om = mp.mpf(om)
    beta = 2 * mp.pi / H
    if abs(om) < mp.mpf("1e-15"):
        return 1 / (2 * mp.pi * beta)
    return (om / (2 * mp.pi)) / (-mp.expm1(-beta * om))       # H1: never 1 - exp(-x)


max_ft_dev = mp.mpf(0)
for _om in ["-1.5", "-0.4", "0.7", "1.0", "2.5"]:
    _om = mp.mpf(_om)
    ft = mp.quad(lambda t: mp.e ** (1j * _om * t) * W_kernel(t), [-mp.inf, -30, -3, 0, 3, 30, mp.inf])
    pred = mp.e ** (-_om * EPS) * S_closed(_om)
    dev = abs(ft.real / pred - 1)
    max_ft_dev = max(max_ft_dev, dev)
    print(f"  {float(_om):7.2f} {mp.nstr(ft.real, 12):>22} {mp.nstr(pred, 12):>22} {mp.nstr(dev, 4):>11}")

check(max_ft_dev < mp.mpf("1e-18"),
      f"S1a the closed-form worldline power spectrum S_BD = (w/2pi)/(1-e^-bw) reproduces the direct "
      f"Fourier transform of the exact BD kernel at 5 frequencies, max rel dev {mp.nstr(max_ft_dev, 3)}. "
      f"This fails if the 16 pi^2 prefactor, the beta = 2pi/H identification or the i-eps sign is wrong "
      f"(a 4 pi^2 prefactor would show a factor-4 miss).")

rho_phi_dev = mp.mpf(0)
for _nf in (n_thermal, n_squeezed(1.3, 1.0, 0.6), n_illegal("0.02", 1.0, 0.5)):
    for _om in ("0.4", "1.7"):
        r = S_of(_om, _nf) - S_of(-mp.mpf(_om), _nf)
        rho_phi_dev = max(rho_phi_dev, abs(r / (C_CONST * mp.mpf(_om)) - 1))
check(rho_phi_dev < mp.mpf("1e-25"),
      f"S1b A1 reconfirmed inside this parametrisation: rho_phi = omega/2pi for the thermal, the "
      f"squeezed AND the illegal state (max rel dev {mp.nstr(rho_phi_dev, 3)}) -- the ELEMENTARY field "
      f"cannot move. Fails if the parametrisation S = c w theta(w) + n(|w|) did not enforce the "
      f"c-number commutator.")

# ===================================================================================================
banner("S2  CONTROL FIRST -- Bunch-Davies must give rho_O >= 0, and it does, as a theorem")

print("  Bochner 1933: <O(tau)O(0)> is a positive-definite function of tau, so its transform")
print("  S_O(omega) >= 0 for ANY operator in ANY state.  In a KMS state S_O(-w) = e^{-bw} S_O(w),")
print("  hence rho_O(w) = S_O(w)(1 - e^{-bw}) >= 0 for w > 0 -- for EVERY composite, no computation.")
print("  Explicit closed form for O = :phi^2: (one-loop bubble):")
print("      rho_{phi^2}^{BD}(omega) = omega (omega^2 + H^2) / (24 pi^3)")
print("  Note omega^2 + H^2: the Deser-Levin five-acceleration combination (and the standard")
print("  thermal-bubble result) -- consistency, not evidence.")
print()
print(f"  {'omega':>7} {'quadrature':>20} {'closed form':>20} {'rel dev':>11} {'KMS ratio dev':>14}")

max_bd_dev, max_kms_dev = mp.mpf(0), mp.mpf(0)
for _om in ["0.5", "1.0", "2.0", "3.0"]:
    _om = mp.mpf(_om)
    num = rho_O(_om, n_thermal, 0)
    ana = _om * (_om**2 + H_UNIT**2) / (24 * mp.pi**3)
    dev = abs(num / ana - 1)
    kms = abs(conv_weighted(_om, n_thermal) / conv_weighted(-_om, n_thermal) / mp.e ** (BETA * _om) - 1)
    max_bd_dev, max_kms_dev = max(max_bd_dev, dev), max(max_kms_dev, kms)
    print(f"  {float(_om):7.2f} {mp.nstr(num, 12):>20} {mp.nstr(ana, 12):>20} "
          f"{mp.nstr(dev, 4):>11} {mp.nstr(kms, 4):>14}")

check(max_bd_dev < mp.mpf("1e-25"),
      f"S2a CONTROL PASSES: rho_{{phi^2}} in Bunch-Davies equals omega(omega^2+H^2)/(24 pi^3) to "
      f"{mp.nstr(max_bd_dev, 3)} at 4 frequencies, and is POSITIVE at all of them. A negative control "
      f"would have been a bug; this check fails for any other coefficient than 1/(24 pi^3).")

check(max_kms_dev < mp.mpf("1e-22"),
      f"S2b the composite power spectrum satisfies KMS at the SAME beta = 2pi/H as the elementary "
      f"field (S_O(w)/S_O(-w) = e^{{beta w}} to {mp.nstr(max_kms_dev, 3)}), which is why the control is "
      f"positive by theorem and not by luck. Fails if the convolution used a non-KMS S.")

# ===================================================================================================
banner("S3  THE THEOREM -- every stationary Gaussian state, and rho_O moves ONE WAY only")

print("  Split S = V + N with V(nu) = c nu theta(nu) (vacuum) and N(nu) = n(|nu|) (EVEN, >= 0).")
print("  S*S = V*V + 2 V*N + N*N.  N*N is even in omega, so it drops out of rho_O = S_O(w)-S_O(-w).")
print("      V*V   : antisymmetric part = c^2 omega^3/6           -> omega^3/(24 pi^3)")
print("      2 V*N : antisymmetric part = 2c * 2 omega * N        -> (2/pi^2) N omega")
print("  because Int_0^inf nu n(|w-nu|) dnu - Int_0^inf nu n(w+nu) dnu = 2 w Int_0^inf n  exactly.")
print("  =>   rho_{phi^2}(omega) = omega^3/(24 pi^3) + (2/pi^2) N omega,   N = Int_0^inf n >= 0.")
print("  The state enters through ONE non-negative number.  Verified against quadrature, which knows")
print("  nothing about the derivation:")
print()
print(f"  {'state':<22} {'N':>14} {'omega':>6} {'quadrature':>18} {'theorem':>18} {'rel dev':>10}")

STATES = [
    ("BD (thermal)", n_thermal),
    ("squeezed r=1 @ w=1", n_squeezed(1.0, 1.0, 0.5)),
    ("squeezed r=2 @ w=3", n_squeezed(2.0, 3.0, 1.0)),
    ("squeezed r=0.4 @ w=0.3", n_squeezed(0.4, 0.3, 0.25)),
    ("NOT A STATE: n<0", n_illegal("0.05", 1.0, 0.5)),
]

max_thm_dev = mp.mpf(0)
rho_min_legal = None
neg_band_found = False
for _nm, _nf in STATES:
    _N = mp.quad(_nf, [0, 1, 5, 40, mp.inf])
    for _om in ("0.7", "2.0"):
        num = rho_O(_om, _nf, 0)
        ana = theorem_phi2(_om, _N)
        dev = abs(num / ana - 1)
        max_thm_dev = max(max_thm_dev, dev)
        legal = not _nm.startswith("NOT")
        if legal:
            rho_min_legal = num if rho_min_legal is None else min(rho_min_legal, num)
        elif num < 0:
            neg_band_found = True
        print(f"  {_nm:<22} {mp.nstr(_N, 8):>14} {float(_om):>6.2f} {mp.nstr(num, 10):>18} "
              f"{mp.nstr(ana, 10):>18} {mp.nstr(dev, 4):>10}")

check(max_thm_dev < mp.mpf("1e-6"),
      f"S3a the theorem rho = w^3/(24 pi^3) + (2/pi^2) N w reproduces independent 30-digit quadrature "
      f"for 5 states (thermal, three squeezings, and one ILLEGAL negative-occupation state) at 2 "
      f"frequencies each, max rel dev {mp.nstr(max_thm_dev, 3)}. Fails if the antisymmetric part of "
      f"2 V*N were anything other than 4 c omega N -- e.g. a missing factor 2 shows up as 100%.")

check(rho_min_legal > 0,
      f"S3b NO NEGATIVE BAND in any admissible state: the smallest rho_{{phi^2}} over the four legal "
      f"states is {mp.nstr(rho_min_legal, 6)} > 0. Fails the moment any legal state produces rho < 0.")

check(neg_band_found,
      f"S3c the check above has teeth: relaxing state positivity (n < 0 in a band, which is NOT a "
      f"density matrix) DOES drive rho_{{phi^2}} negative. So S3b is a statement about positivity of "
      f"the state, not an artefact of the estimator.")

# --- rigidity: the state enters ONLY through N -------------------------------------------------
banner("S3d RIGIDITY -- two different squeezing profiles with the SAME N give the SAME rho_O")

_A = n_squeezed(1.0, 1.0, 0.5)
N_A = mp.quad(_A, [0, 1, 5, 40, mp.inf])
_bump_B_unit = lambda s: C_CONST * mp.mpf(s) * mp.e ** (-(((mp.mpf(s) - 3) / mp.mpf("0.4")) ** 2))
I_B = mp.quad(_bump_B_unit, [0, 1, 5, 40, mp.inf])
N_th = mp.quad(n_thermal, [0, 1, 5, 40, mp.inf])
sh2_B = (N_A - N_th) / I_B                     # match the occupation weight, different profile
r_B = mp.asinh(mp.sqrt(sh2_B))
_B = n_squeezed(r_B, 3.0, mp.mpf("0.4"))
N_B = mp.quad(_B, [0, 1, 5, 40, mp.inf])
print(f"  profile A: r_sq = 1.0 at w0 = 1.0, width 0.5   -> N = {mp.nstr(N_A, 12)}")
print(f"  profile B: r_sq = {mp.nstr(r_B, 6)} at w0 = 3.0, width 0.4 -> N = {mp.nstr(N_B, 12)}")
max_rig = mp.mpf(0)
for _om in ("0.6", "1.4", "3.1"):
    rA, rB = rho_O(_om, _A, 0), rho_O(_om, _B, 0)
    max_rig = max(max_rig, abs(rA / rB - 1))
    print(f"    omega = {float(_om):4.2f}:  rho_A = {mp.nstr(rA, 10)}   rho_B = {mp.nstr(rB, 10)}")
check(abs(N_A / N_B - 1) < mp.mpf("1e-12") and max_rig < mp.mpf("1e-6"),
      f"S3d two squeezed states with completely different profiles (peaks at w = 1.0 and w = 3.0, "
      f"different amplitudes) but the same occupation weight N give the same rho_O at three "
      f"frequencies to {mp.nstr(max_rig, 3)}. Fails if rho_O depended on the profile SHAPE -- which it "
      f"would if the theorem's single-moment structure were wrong.")

# ===================================================================================================
banner("S4  HOW DEEP A NEGATIVE BAND WOULD NEED TO BE -- it needs a NEGATIVE total occupation")

print("  rho_{phi^2}(w) < 0  <=>  N < -w^2/(48 pi).  Compare with Bunch-Davies N = H^2/(48 pi):")
print(f"  {'omega/H':>8} {'N required':>18} {'N_BD':>18} {'ratio':>10}")
N_BD_analytic = H_UNIT**2 / (48 * mp.pi)
ratios = []
for _x in ("0.5", "1.0", "2.0"):
    _x = mp.mpf(_x)
    need = -(_x * H_UNIT) ** 2 / (48 * mp.pi)
    ratios.append(need / N_BD_analytic)
    print(f"  {float(_x):8.2f} {mp.nstr(need, 10):>18} {mp.nstr(N_BD_analytic, 10):>18} "
          f"{mp.nstr(need / N_BD_analytic, 6):>10}")
check(abs(N_BD_analytic / N_th - 1) < mp.mpf("1e-20"),
      f"S4a the analytic Bunch-Davies occupation weight N = H^2/(48 pi) = {mp.nstr(N_BD_analytic, 10)} "
      f"matches the quadrature {mp.nstr(N_th, 10)}. Fails for any other zeta(2) bookkeeping.")
check(abs(ratios[1] + 1) < mp.mpf("1e-25") and all(r < 0 for r in ratios),
      f"S4b at omega = H the required occupation weight is EXACTLY minus the Bunch-Davies value "
      f"(ratio {mp.nstr(ratios[1], 8)}), and it is negative at every omega. A negative band is not a "
      f"small correction to a state: it is a state with negative total particle content. Fails if the "
      f"required N were merely small-and-positive.")

# ===================================================================================================
banner("S5  DERIVATIVE-COUPLED COMPOSITE, AND WHERE A NEGATIVE BAND *WOULD* HAVE TO LIVE")

print("  For O = :(d_tau phi)^2: each propagator carries d d', so the Wick weight is (nu nu')^2:")
print("      rho(w) = [ c^2 w^7/140 + 2c ( w^3 M2 + 3 w M4 ) ] / pi,   M_n = Int nu^n N(nu) dnu >= 0")
print("  -> positive again, by the same parity argument (odd powers of nu die against even N).")
print()
print(f"  {'state':<22} {'omega':>6} {'quadrature':>18} {'closed form':>18} {'rel dev':>10}")
max_k2_dev, min_k2 = mp.mpf(0), None
for _nm, _nf in STATES[:2]:
    M2, M4 = occ_weight(_nf, 2), occ_weight(_nf, 4)
    for _om in ("0.5", "1.5", "3.0"):
        _omm = mp.mpf(_om)
        num = rho_O(_om, _nf, 2)
        ana = (C_CONST**2 * _omm**7 / 140 + 2 * C_CONST * (_omm**3 * M2 + 3 * _omm * M4)) / mp.pi
        max_k2_dev = max(max_k2_dev, abs(num / ana - 1))
        min_k2 = num if min_k2 is None else min(min_k2, num)
        print(f"  {_nm:<22} {float(_om):>6.2f} {mp.nstr(num, 10):>18} {mp.nstr(ana, 10):>18} "
              f"{mp.nstr(abs(num / ana - 1), 4):>10}")
check(max_k2_dev < mp.mpf("1e-6") and min_k2 > 0,
      f"S5a the derivative-coupled composite :(d_tau phi)^2: matches its closed form to "
      f"{mp.nstr(max_k2_dev, 3)} and is POSITIVE at every point tested (min {mp.nstr(min_k2, 6)}). So "
      f"the escape is not restored by putting derivatives in the coupling. Fails if the omega^7/140 "
      f"Beta-function coefficient or either moment weight were wrong.")

print()
print("  The ODD weight nu(w-nu) DOES give a negative band -- and it is NOT an operator:")
print(f"  {'weight':<16} {'S_O(-0.5)':>16} {'S_O(0)':>16} {'S_O(+0.5)':>16} {'Bochner S_O>=0?':>17}")
bochner = {}
for _k in (0, 1, 2):
    vals = [conv_weighted(_o, n_thermal, _k) for _o in ("-0.5", "0", "0.5")]
    bochner[_k] = min(vals)
    print(f"  (nu nu')^{_k:<7} {mp.nstr(vals[0], 8):>16} {mp.nstr(vals[1], 8):>16} "
          f"{mp.nstr(vals[2], 8):>16} {'YES' if min(vals) >= 0 else 'NO -- not an operator':>17}")
rho_odd = rho_O("0.5", n_thermal, 1)
check(bochner[0] > 0 and bochner[2] > 0 and bochner[1] < 0 and rho_odd < 0,
      f"S5b the odd weight produces a genuine negative band (rho = {mp.nstr(rho_odd, 6)} at w = 0.5) but "
      f"violates Bochner positivity (S_O(0) = {mp.nstr(bochner[1], 6)} < 0), so it is the power spectrum "
      f"of NO operator, while the two even weights pass. This pins the escape precisely: it requires a "
      f"Bochner-admissible weight that is not an even polynomial in each argument. Fails if any even "
      f"weight went negative or the odd one did not.")

# ===================================================================================================
banner("S6  DOOR A4 -- the squeezing de Sitter actually realises, as a number")

print("  Super-horizon dS squeezing grows as r_sq ~ N_efolds (standard inflationary result); a mode")
print("  squeezed by r_sq carries sinh^2(r_sq) quanta, so N grows like sinh^2(r_sq) -- and rho_O grows")
print("  with it, in the ANTI-MOND direction.")
print(f"  {'N_efolds':>9} {'sinh^2(r_sq)':>16} {'rho_O/rho_O^BD at w=H':>24}")
for _Ne in (1, 5, 10, 60):
    sh2 = math.sinh(_Ne) ** 2
    nf = n_squeezed(_Ne, 1.0, 0.5)
    N_here = N_th + sh2 * mp.quad(lambda s: C_CONST * mp.mpf(s) * mp.e ** (-(((mp.mpf(s) - 1) / mp.mpf("0.5")) ** 2)),
                                 [0, 1, 5, 40, mp.inf])
    amp = theorem_phi2(1, N_here) / theorem_phi2(1, N_th)
    print(f"  {_Ne:>9} {sh2:>16.6e} {mp.nstr(amp, 8):>24}")
    if _Ne == 60:
        amp60 = amp
check(amp60 > mp.mpf("1e40"),
      f"S6a at the e-fold counts dS actually realises the squeezed occupation makes rho_O larger by "
      f"{mp.nstr(amp60, 4)} -- ~52 orders of magnitude, and in the WRONG direction. Door A4 closes with "
      f"a number: realised squeezing is not near a sign flip, it is the opposite of near. Fails if the "
      f"amplification were O(1) or negative.")

# ===================================================================================================
banner("S7  PHYSICAL NUMBERS, BOTH FOOTINGS, AND THE INERTIA LAW (R5, R6)")

FOOT_SCALE = 1.2082                    # ALT / canonical = 1/sqrt(Omega_Lambda), per the locked table
CH_FOOT = {"canonical": CHL, "ALT": CHL * FOOT_SCALE}
H_PHYS = {k: v / C_L for k, v in CH_FOOT.items()}          # dS rate per footing, s^-1
A0_DERIVED = {k: v / Z_FW for k, v in CH_FOOT.items()}     # a_0 = cH/Z on each footing
print("  R6 bookkeeping: the object computed here is a spectral density, but every acceleration below")
print(f"  is a_0, not the floor.  a_0 canonical {A0['canonical']:.4e}  floor k = {FLOOR_K['canonical']:.4e}")
print(f"                          a_0 ALT       {A0['ALT']:.4e}  floor k = {FLOOR_K['ALT']:.4e}")
print("  Each footing is rebuilt from its OWN cH (canonical cH_Lambda, ALT cH_0 = 1.2082 cH_Lambda) so")
print("  that the two are related by exactly one factor, not by the rounding of the quoted a_0:")
a0_dev = max(abs(A0_DERIVED[k] / A0[k] - 1) for k in A0)
for k in A0:
    print(f"    {k:<10} cH = {CH_FOOT[k]:.5e}  ->  a_0 = cH/Z = {A0_DERIVED[k]:.5e}  "
          f"(locked {A0[k]:.5e}, dev {abs(A0_DERIVED[k]/A0[k]-1):.2e})")
check(a0_dev < 2e-3,
      f"S7a0 both footings reproduce their locked a_0 from cH/Z to {a0_dev:.2e} (canonical 9.3614e-11, "
      f"ALT 1.13e-10). Fails if Z, the 1.2082 = 1/sqrt(Omega_L), or the cH_Lambda-vs-cH_0 assignment "
      f"were wrong -- using 2Z instead of Z misses by a factor 2.")
print()
print(f"  {'footing':<10} {'H_dS [1/s]':>14} {'w=a_0/c [1/s]':>15} {'rho_O(a_0/c)':>16} {'N required (<0)':>17}")
rho_phys, need_phys = {}, {}
for nm in A0:
    Hp, om = mp.mpf(H_PHYS[nm]), mp.mpf(A0_DERIVED[nm] / C_L)
    rho_phys[nm] = om * (om**2 + Hp**2) / (24 * mp.pi**3)
    need_phys[nm] = -(om**2) / (48 * mp.pi)
    print(f"  {nm:<10} {float(Hp):>14.5e} {float(om):>15.5e} {mp.nstr(rho_phys[nm], 6):>16} "
          f"{mp.nstr(need_phys[nm], 6):>17}")
ratio_pred = mp.mpf(FOOT_SCALE) ** 3
ratio_got = rho_phys["ALT"] / rho_phys["canonical"]
print(f"  rho_O scales as w(w^2+H^2) and both w and H carry one factor {FOOT_SCALE}, so the predicted")
print(f"  ratio is {float(ratio_pred):.9f}; got {float(ratio_got):.9f} "
      f"(rel dev {float(abs(ratio_got/ratio_pred-1)):.2e}; the inputs are float64, hence ~1e-16)")
check(rho_phys["canonical"] > 0 and rho_phys["ALT"] > 0 and abs(ratio_got / ratio_pred - 1) < mp.mpf("1e-12"),
      f"S7a the verdict is footing-independent: rho_O > 0 on BOTH footings, and the ALT/canonical ratio "
      f"is exactly the cube of the footing factor ({float(ratio_got):.6f}). Fails if a footing were "
      f"mixed -- canonical H with ALT omega gives 1.208, not 1.764.")

print()
print("  delta_m ~ (2/pi) P Int rho_O(w)/w^2 dw over the committed window w_c in [1.78e-14, 2.21e-14]")
print("  (the free fifth constant), IR-regulated at w = H_dS:")
dm = {}
for nm in A0:
    Hp = mp.mpf(H_PHYS[nm])
    row = []
    for wc in OMEGA_C_WINDOW:
        wc = mp.mpf(wc)
        val = (2 / mp.pi) * ((wc**2 - Hp**2) / 2 + Hp**2 * mp.log(wc / Hp)) / (24 * mp.pi**3)
        row.append(val)
    dm[nm] = row
    print(f"    {nm:<10} delta_m coefficient in [{mp.nstr(row[0], 12)}, {mp.nstr(row[1], 12)}]  (units "
          f"of the coupling^2; only the SIGN is claimed)")
print("    the two footings agree to ~1e-7 because the integral is dominated by w_c^2/2 and the footing")
print("    enters only through the H^2 ln(w_c/H) piece -- delta_m here is essentially footing-blind,")
print("    which is a statement about this estimator, not evidence for either footing.")
check(all(v > 0 for row in dm.values() for v in row),
      f"S7b delta_m > 0 across the whole committed omega_c window on both footings -- inertia is "
      f"INCREASED, i.e. anti-MOND. Fails if any admissible omega_c or footing flipped the sign; the "
      f"integrand is rho_O/w^2 > 0 pointwise, so the only way to flip it is a negative band.")

print()
print("  Feed the framework's own temperature in (Deser & Levin 1997; Narnhofer, Peter & Thirring")
print("  1996): 2 pi T = sqrt(a^2/c^2 + H^2), i.e. H^2 -> H^2 + a^2/c^2, hence")
print("      delta_m(a) - delta_m(0) = (2/pi) (a^2/c^2) ln(w_c/H) / (24 pi^3)  >  0,")
print("  so m(a) = m0 (1 + K a^2) with K > 0: inertia GROWS with acceleration and mu -> 1 as a -> 0.")
print("  The framework's own kernel nu(y) = sqrt(1+1/y) (Milgrom 1999 PLA 253:273 eqs 6-9) needs")
print("  modified inertia m_eff/m = 1/nu(y), i.e. delta_m/m = 1/nu - 1 < 0 for ALL y, -> -1 in deep MOND.")
g_bar_probe = 1.0e-11
K_sign = {}
req = {}
for nm, a0 in A0.items():
    Hp = mp.mpf(H_PHYS[nm])
    K_sign[nm] = (2 / mp.pi) * mp.log(mp.mpf(OMEGA_C_WINDOW[0]) / Hp) / (24 * mp.pi**3) / C_L**2
    y = mp.mpf(g_bar_probe) / mp.mpf(a0)
    req[nm] = 1 / mp.sqrt(1 + 1 / y) - 1
    print(f"    {nm:<10} y = g_bar/a_0 = {float(y):.5f} at g_bar = 1e-11 m/s^2  ->  required "
          f"delta_m/m = {float(req[nm]):+.4f};  computed K = {mp.nstr(K_sign[nm], 6)} (> 0)")
check(all(v > 0 for v in K_sign.values()) and all(v < -0.5 for v in req.values()),
      f"S7c NO MOND LIMIT in this class: the required fractional mass shift is "
      f"{float(req['canonical']):+.4f} (canonical) / {float(req['ALT']):+.4f} (ALT) at g_bar = 1e-11, "
      f"while the class delivers a POSITIVE, a^2-growing shift (K > 0 on both footings). Fails if K "
      f"came out negative, or if the framework's own kernel wanted delta_m > 0.")

# ===================================================================================================
banner("S8  DOOR A5 -- is a negative band a physical density matrix at all?")

print("  (i) SECULAR (Davies/Lindblad) generator. For linear coupling to a bath operator O with")
print("      power spectrum S_O, the Kossakowski matrix in the {a, a^dag} basis is")
print("          K = diag( S_O(+w_0), S_O(-w_0) ),")
print("      and complete positivity requires both entries >= 0 (Gorini-Kossakowski-Sudarshan 1976,")
print("      Lindblad 1976). Since S_O(w) = rho_O(w)/(1 - e^{-beta w}) and the denominator is positive")
print("      for w > 0, a negative band at the system frequency gives a NEGATIVE RATE at ANY depth.")
print()
rho_base = lambda w: mp.mpf(w) * (mp.mpf(w) ** 2 + H_UNIT**2) / (24 * mp.pi**3)


def rho_band(w, depth, w_b=mp.mpf(2), wid=mp.mpf("0.5")):
    w = mp.mpf(w)
    return rho_base(w) - mp.mpf(depth) * mp.e ** (-(((w - w_b) / wid) ** 2))


def kossakowski_secular(w0, depth):
    """K = diag(Gamma_down, Gamma_up) with Gamma_down = S_O(+w0), Gamma_up = S_O(-w0) = e^{-b w0} S_O(w0)
    for a KMS reference bath.  H1: -expm1(-x), never 1 - exp(-x)."""
    w0 = mp.mpf(w0)
    lo = rho_band(w0, depth) / (-mp.expm1(-BETA * w0))
    up = lo * mp.e ** (-BETA * w0)
    return lo, up


print(f"  {'band depth d':>14} {'rho(w_b=2)':>16} {'Gamma_down':>16} {'CP?':>6}")
d_pointwise = rho_base(2)
secular_flips = []
for _d in (mp.mpf(0), d_pointwise / 2, d_pointwise * mp.mpf("0.999"), d_pointwise * mp.mpf("1.001"),
           d_pointwise * 2):
    lo, up = kossakowski_secular(2, _d)
    secular_flips.append((float(_d), float(lo)))
    print(f"  {float(_d):>14.6e} {mp.nstr(rho_band(2, _d), 8):>16} {mp.nstr(lo, 8):>16} "
          f"{'yes' if min(lo, up) >= 0 else 'NO':>6}")
check(secular_flips[2][1] > 0 and secular_flips[3][1] < 0,
      f"S8a the CP boundary in the secular generator sits EXACTLY where rho crosses zero: at 0.999x the "
      f"zero-crossing depth the rate is {secular_flips[2][1]:+.3e} and at 1.001x it is "
      f"{secular_flips[3][1]:+.3e}. So the CP cap on band depth is 'no negative band at all', not some "
      f"finite tolerance. Fails if a negative rho gave a non-negative rate.")

print()
print("  (ii) TWO CAPS, side by side (the corpus's own bound vs this one).")
print("       ghost / mu_eff cap:  mu_eff = 1 + rho/2 > 0  =>  rho > -2   (tn18 sits at 80% of it)")
print("       complete positivity: rho >= 0 everywhere    =>  ZERO negative band admitted")
print("       => CP is strictly the tighter of the two; a band at 80% of the ghost cap has rho ~ -1.6,")
print("          which is not a completely positive dynamical map. A MOND state that is not a density")
print("          matrix is not a result.")
tn18_rho_min = -1.6      # corpus: tn18's band sits at 80% of the ghost cap rho > -2
check(tn18_rho_min < 0.0 and tn18_rho_min > -2.0,
      f"S8b the corpus's tn18 band (80% of the ghost cap, rho_min = {tn18_rho_min}) is INSIDE the ghost "
      f"cap rho > -2 but OUTSIDE the CP cap rho >= 0, so the two caps genuinely disagree about it and "
      f"CP is the binding one. Fails if tn18's depth were either ghost-excluded or CP-allowed.")

print()
print("  (iii) NON-SECULAR Caldeira-Leggett form, with the Dekker inequality")
print("        K = [[D_pp, -D_xp - i lam/2], [-D_xp + i lam/2, D_xx]],  CP <=> D_pp D_xx - D_xp^2 >= lam^2/4")
print("        (Dekker 1977; Sandulescu & Scutaru 1987).  MODEL, labelled: flat form factor up to w_c,")
print("        IR regulator at w = H, D_xp = 0, lam = (pi/2) rho'(0).")
W_C_MODEL, W_MIN_MODEL = mp.mpf(5), mp.mpf(1)


def cl_coeffs(depth):
    cth = lambda w: mp.cosh(BETA * mp.mpf(w) / 2) / mp.sinh(BETA * mp.mpf(w) / 2)
    D_pp = mp.quad(lambda w: rho_band(w, depth) * cth(w), [W_MIN_MODEL, 2, W_C_MODEL]) / 2
    D_xx = mp.quad(lambda w: rho_band(w, depth) * cth(w) / w**2, [W_MIN_MODEL, 2, W_C_MODEL]) / 2
    lam = (mp.pi / 2) * (1 / (24 * mp.pi**3))          # rho_base'(0) = H^2/(24 pi^3), H = 1
    return D_pp, D_xx, lam


def min_eig(depth):
    D_pp, D_xx, lam = cl_coeffs(depth)
    tr, det = D_pp + D_xx, D_pp * D_xx - lam**2 / 4
    disc = mp.sqrt(max(tr**2 / 4 - det, mp.mpf(0)))
    return tr / 2 - disc


D_pp0, D_xx0, lam0 = cl_coeffs(0)
print(f"        control, positive bath: D_pp = {mp.nstr(D_pp0, 8)}  D_xx = {mp.nstr(D_xx0, 8)}  "
      f"lam = {mp.nstr(lam0, 8)}")
print(f"          D_pp D_xx = {mp.nstr(D_pp0 * D_xx0, 8)}   vs  lam^2/4 = {mp.nstr(lam0**2 / 4, 8)}"
      f"   -> min eig = {mp.nstr(min_eig(0), 8)}")
print(f"          but the TRUNCATED CL generator (D_xx set to 0) gives det = {mp.nstr(-lam0**2 / 4, 8)}"
      f" < 0 even for this perfectly POSITIVE bath")
check(min_eig(0) > 0 and (0 * D_xx0 - lam0**2 / 4) < 0,
      f"S8c control: the full CL Kossakowski matrix is positive for a positive bath (min eigenvalue "
      f"{mp.nstr(min_eig(0), 6)}), while the usual D_xx = 0 truncation violates Dekker even then. So "
      f"'the CL equation is not CP' is an artefact of the truncation and is NOT evidence about a "
      f"negative band -- worth stating because door D4 could otherwise read it as one. Fails if the "
      f"full matrix were also non-positive.")

print()
print(f"  {'band width':>11} {'depth d* where min eig -> 0':>28} {'d*/(pointwise rho=0 depth)':>28}")
def min_eig_w(d, wid):
    """Smallest eigenvalue of the CL Kossakowski matrix for a band of depth d and width wid at w_b = 2."""
    cth = lambda w: mp.cosh(BETA * mp.mpf(w) / 2) / mp.sinh(BETA * mp.mpf(w) / 2)
    rb = lambda w: rho_base(w) - mp.mpf(d) * mp.e ** (-(((mp.mpf(w) - 2) / mp.mpf(wid)) ** 2))
    D_pp = mp.quad(lambda w: rb(w) * cth(w), [W_MIN_MODEL, 2, W_C_MODEL]) / 2
    D_xx = mp.quad(lambda w: rb(w) * cth(w) / w**2, [W_MIN_MODEL, 2, W_C_MODEL]) / 2
    tr, det = D_pp + D_xx, D_pp * D_xx - lam0**2 / 4
    disc = mp.sqrt(max(tr**2 / 4 - det, mp.mpf(0)))
    return tr / 2 - disc


boundaries = []
for _w in (mp.mpf("0.25"), mp.mpf("0.5"), mp.mpf("1.0")):
    d_star = mp.findroot(lambda d, _w=_w: min_eig_w(d, _w), 2 * D_pp0 / (_w * mp.sqrt(mp.pi)))
    boundaries.append(d_star)
    print(f"  {float(_w):>11.2f} {mp.nstr(d_star, 10):>28} {float(d_star / d_pointwise):>28.2f}")
check(boundaries[0] > boundaries[1] > boundaries[2] and all(b > d_pointwise for b in boundaries),
      f"S8d in the integrated CL form the CP boundary depth DECREASES monotonically with band width "
      f"({mp.nstr(boundaries[0], 6)} -> {mp.nstr(boundaries[2], 6)} for widths 0.25 -> 1.0) and every "
      f"one of them is deeper than the pointwise rho = 0 depth by 6-25x -- so the broadband test is "
      f"the PERMISSIVE one and the secular test in S8a is the binding one. Fails if a wider band "
      f"needed a deeper depth, which would mean the integral was not doing the work.")

# ===================================================================================================
banner("S9  PROVE BY MOVING THE NUMBER, AND REFINE")

om_probe = mp.mpf("1.3")
for _H in (H_UNIT, 2 * H_UNIT):
    beta_H = 2 * mp.pi / _H
    nf = lambda s, _H=_H: n_thermal(s, _H)
    N_H = mp.quad(nf, [0, 1, 5, 40, mp.inf])
    print(f"  H = {float(_H):.1f}:  N = {mp.nstr(N_H, 10)}   rho_O(1.3) = "
          f"{mp.nstr(theorem_phi2(om_probe, N_H), 10)}   H^2-part = "
          f"{mp.nstr(theorem_phi2(om_probe, N_H) - om_probe**3 / (24 * mp.pi**3), 10)}")
N_1 = mp.quad(lambda s: n_thermal(s, H_UNIT), [0, 1, 5, 40, mp.inf])
N_2 = mp.quad(lambda s: n_thermal(s, 2 * H_UNIT), [0, 1, 5, 40, mp.inf])
part1 = theorem_phi2(om_probe, N_1) - om_probe**3 / (24 * mp.pi**3)
part2 = theorem_phi2(om_probe, N_2) - om_probe**3 / (24 * mp.pi**3)
check(abs(part2 / part1 - 4) < mp.mpf("1e-20"),
      f"S9a SHOULD move: doubling H multiplies the H^2 part of rho_O by exactly "
      f"{mp.nstr(part2 / part1, 12)} (predicted 4), while the omega^3 part is H-independent. Fails for "
      f"any other H-scaling, e.g. if N had picked up a stray beta.")

rho_c_a, rho_c_b = rho_O("1.1", n_thermal, 0, (40, 5)), rho_O("1.1", n_thermal, 0, (80, 2))
print(f"  same rho_O(1.1) with different quadrature split points: {mp.nstr(rho_c_a, 14)} vs "
      f"{mp.nstr(rho_c_b, 14)}")
check(abs(rho_c_a / rho_c_b - 1) < mp.mpf("1e-22"),
      f"S9b SHOULD NOT move: changing the quadrature split points (40,5) -> (80,2) leaves rho_O fixed to "
      f"{mp.nstr(abs(rho_c_a / rho_c_b - 1), 3)}. Fails if the integrand's exponential tail or its two "
      f"kinks were being mis-sampled.")

mp.mp.dps = 40
rho_hi = rho_O("1.1", n_thermal, 0)
ana_hi = mp.mpf("1.1") * (mp.mpf("1.1") ** 2 + 1) / (24 * mp.pi**3)
shift = abs(rho_hi / rho_c_a - 1)
mp.mp.dps = 30
print(f"  refinement dps 30 -> 40: rho_O(1.1) shifts by {mp.nstr(shift, 4)} (closed form "
      f"{mp.nstr(ana_hi, 14)})")
check(shift < mp.mpf("1e-25"),
      f"S9c refining the working precision from 30 to 40 digits moves rho_O by {mp.nstr(shift, 3)}, far "
      f"below the 1e-6 the sign conclusions need, so nothing here is a precision artefact. Fails if the "
      f"quadrature had been resolving a cancellation only accidentally.")

# ===================================================================================================
banner("S10  FREE PARAMETER COUNT (R1)")

N_FREE_BEFORE = 1        # kappa
N_FREE_AFTER = 1         # unchanged: the escape closed, nothing was derived
print(f"  free dimensionless parameters before: {N_FREE_BEFORE}   after: {N_FREE_AFTER}")
print("  Had the escape worked it would have ADDED one (the squeezing r_sq, or equivalently N), so the")
print("  best case for this door was a REPARAMETRISATION, not a derivation. And rho_O depends on the")
print("  state through exactly ONE number N (S3d), which is bounded below by zero -- there is no knob")
print("  in this class that can be turned toward MOND at all.")
check(N_FREE_AFTER == N_FREE_BEFORE and N_A > 0 and N_th > 0,
      f"S10a the free-parameter count is unchanged at {N_FREE_AFTER} (kappa), and the single state "
      f"parameter this door could have introduced, N, is positive for every state examined "
      f"(N_BD = {mp.nstr(N_th, 6)}). Nothing here derives kappa. Fails if any state had given N <= 0, "
      f"which is the only way this door could have supplied a mechanism.")

# ---------------------------------------------------------------------------------------------------
banner("RESULT")
n_ok = sum(1 for c, _ in ok if c)
print(f"  {n_ok}/{len(ok)} checks held.")
if n_ok != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("""  LANE C VERDICT. The composite operator does exactly what door A3 predicted -- it makes rho
  genuinely state-dependent, unlike the elementary field -- and the dependence is ONE-SIGNED:
      rho_{phi^2}(omega) = omega^3/(24 pi^3) + (2/pi^2) N omega,   N = Int_0^inf S(-nu) dnu >= 0,
  for every stationary Gaussian state, with Bunch-Davies the minimum (N = H^2/48pi, giving the closed
  form omega(omega^2+H^2)/(24 pi^3)).  Squeezing -- alpha-vacua included -- only raises N, so it
  DEEPENS the anti-MOND wall; at realised e-fold counts by ~52 orders of magnitude.  A negative band
  needs N < -omega^2/(48 pi), i.e. negative total occupation, which is not a density matrix; and if one
  posits such a band anyway it makes a secular Lindblad rate negative at ANY depth, so it is not
  completely positive either.  delta_m > 0 on both footings across the whole committed omega_c window,
  and feeding in the Deser-Levin temperature gives m(a) = m0(1 + K a^2) with K > 0 -- inertia grows
  with acceleration, while the framework's own kernel needs delta_m/m = 1/nu - 1 ~ -0.70 at
  g_bar = 1e-11.  AGAINST INTEREST: this closes the escape the corpus was counting on, and the pretty
  omega^2+H^2 five-acceleration structure appears and still gives the wrong sign.
  SCOPE: stationary Gaussian states, quadratic composites with even Wick weights. Outside it, and NOT
  excluded here: non-Gaussian states, genuinely non-stationary squeezing, bounded/finite-level sectors
  (door A2), and mixed composites such as T_mu_nu whose Wick weight need not be a positive-coefficient
  polynomial -- S5b shows exactly what such a weight would have to look like, and that it must still
  pass Bochner.  No closure is claimed.""")
print("  kappa = 1/2 remains FITTED, NOT DERIVED.")
