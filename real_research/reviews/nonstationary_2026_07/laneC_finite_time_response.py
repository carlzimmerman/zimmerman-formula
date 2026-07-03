#!/usr/bin/env python3
"""
Lane C, part 1 -- FINITE-TIME (windowed) Unruh-DeWitt response, first-principles
reconstruction of the Luo (arXiv:2602.14515) broadening mechanism.

Setup (c = hbar = 1):
  Uniformly accelerated worldline, massless scalar vacuum, pulled-back Wightman
     W(u) = -(1/4pi^2) (A/2)^2 / sinh^2( A(u - i eps)/2 ),   A = proper acceleration.
  (Deser-Levin 1997: for acceleration a in de Sitter with Hubble H the pulled-back
   Wightman has EXACTLY this form with A = sqrt(a^2 + H^2); for a=0 comoving dS the
   conformal-factor algebra gives (eta-eta')^2 a(eta)a(eta') -> (4/H^2) sinh^2(H dtau/2),
   i.e. the same sinh^2 kernel with A=H. So 'A' below already carries the dS floor.)

  Gaussian window chi(tau) = exp(-tau^2/(2 T^2)).  Windowed response
     F(w) = int dtau dtau' chi chi' e^{-iw(tau-tau')} W(tau-tau') = sqrt(pi) T * f(w),
     f(w) = int du e^{-iwu} G(u) W(u),  G(u) = exp(-u^2/(4T^2))   (rate).

  Split W = W_vac + dW,  W_vac = -(1/4pi^2)/(u-i eps)^2 (Minkowski k=0 pole; its
  windowed transform is CLOSED FORM), dW regular real even (numerical quadrature).

Deliverables:
  (1) Planck-limit validation (T -> inf reproduces exact Unruh thermality).
  (2) Effective spectral scale a_eff(A, T): fit a_eff^2 ~ c_a A^2 + c_T / T^2
      -> quadrature structure  a_eff ~ sqrt(a^2 + H^2 + kappa^2/T^2).
  (3) SHAPE: sympy proof that the Milgrom/Deser-Levin Delta-T mapping
      mu(a) = [sqrt(a^2+aL^2)-aL]/a  is EXACTLY the framework nu(y)=sqrt(1+1/y)
      with a0 = 2 aL.
  (4) SCALE: the forced normalization a0_DL = 2 c H_Lambda vs framework a0 (both footings).
"""
import numpy as np, math, sys

PASS = True
def check(name, ok, detail=""):
    global PASS
    print(("  [PASS] " if ok else "  [FAIL] ") + name + ("  " + detail if detail else ""))
    if not ok: PASS = False

# ---------- windowed vacuum-pole piece (closed form) ----------
def f_vac(w, T):
    x = w * T
    # I_int = int_0^inf mu exp(-(mu+w)^2 T^2) dmu = e^{-x^2}/(2T^2) - (sqrt(pi) w /(2T)) erfc(x)
    I = math.exp(-x * x) / (2 * T * T) - (math.sqrt(math.pi) * w / (2 * T)) * math.erfc(x)
    return (math.sqrt(math.pi) * T / (2 * math.pi ** 2)) * I

# ---------- regular remainder dW(u;A) = (1/4pi^2)[1/u^2 - (A^2/4)/sinh^2(Au/2)] ----------
def dW(u, A):
    out = np.empty_like(u)
    x = A * u / 2.0
    small = x < 1e-4
    big = x > 30.0
    mid = ~(small | big)
    out[small] = (A ** 2 / 12.0 - A ** 4 * u[small] ** 2 / 240.0) / (4 * math.pi ** 2)
    out[big] = 1.0 / (4 * math.pi ** 2 * u[big] ** 2)
    um = u[mid]
    out[mid] = (1.0 / um ** 2 - (A ** 2 / 4.0) / np.sinh(A * um / 2.0) ** 2) / (4 * math.pi ** 2)
    return out

def f_delta(w, T, A, du_factor=80.0):
    if A == 0.0:
        return 0.0
    du = 1.0 / (du_factor * max(A, abs(w), 1.0 / T, 0.2))
    umax = 9.0 * T
    n = int(umax / du) + 2
    if n > 4_000_000:
        n = 4_000_000
    u = np.linspace(0.0, umax, n)
    integ = np.cos(w * u) * np.exp(-u ** 2 / (4 * T ** 2)) * dW(u, A)
    return 2.0 * np.trapz(integ, u)

def f_tot(w, T, A, du_factor=80.0):
    return f_vac(w, T) + f_delta(w, T, A, du_factor)

print("=" * 78)
print("TEST 1: infinite-window (T=200/A) limit reproduces exact Unruh Planck spectrum")
print("=" * 78)
A = 1.0
T = 200.0
for w in (0.3, 0.7, 1.5):
    got = f_tot(w, T, A, du_factor=200.0)
    planck = w / (2 * math.pi * (math.exp(2 * math.pi * w / A) - 1.0))
    check(f"f({w})={got:.6e} vs Planck {planck:.6e}", abs(got / planck - 1) < 0.02,
          f"rel.err={abs(got/planck-1):.2e}")
    # detailed balance / commutator identity f(-w)-f(w) = w/2pi (exact for Gaussian window)
    gotm = f_tot(-w, T, A, du_factor=200.0)
    check(f"f(-{w})-f({w}) = w/2pi", abs((gotm - got) - w / (2 * math.pi)) < 1e-4 * w)

print()
print("=" * 78)
print("TEST 2: finite-window broadening -> effective scale a_eff(A, T_win); quadrature fit")
print("  a_eff := 2*pi*T_eff, T_eff from detailed balance at probe w_p=0.3*sqrt(A^2+(2/T)^2)")
print("=" * 78)
rows = []
for A in (0.0, 0.5, 1.0, 2.0):
    for T in (0.75, 1.5, 3.0, 6.0, 12.0, 48.0):
        wp = 0.3 * math.sqrt(A ** 2 + (2.0 / T) ** 2)
        fp = f_tot(wp, T, A); fm = f_tot(-wp, T, A)
        if fp <= 0:      # numerically zero excitation -> skip (deep-thermal-suppressed corner)
            continue
        a_eff = 2 * math.pi * wp / math.log(fm / fp)
        rows.append((A, T, a_eff))
        print(f"  A={A:4.1f}  T_win={T:6.2f}  a_eff={a_eff:8.4f}")
M = np.array([[A ** 2, 1.0 / T ** 2] for A, T, _ in rows])
y = np.array([ae ** 2 for _, _, ae in rows])
coef, *_ = np.linalg.lstsq(M, y, rcond=None)
c_a, c_T = coef
pred = M @ coef
frac = np.abs(np.sqrt(np.maximum(pred, 1e-30)) - np.sqrt(y)) / np.sqrt(y)
kappa = math.sqrt(c_T)
print(f"\n  FIT: a_eff^2 = {c_a:.3f}*A^2 + {c_T:.3f}/T_win^2   (kappa = {kappa:.3f})")
print(f"  max fractional residual in a_eff over grid: {frac.max():.3f}, rms {np.sqrt((frac**2).mean()):.3f}")
check("quadrature structure a_eff ~ sqrt(A^2 + kappa^2/T^2) holds to <~15%",
      frac.max() < 0.15 and 0.8 < c_a < 1.2)
print("  (probe convention: doubling w_p at A=1,T=3 shifts a_eff by the amount below)")
wp = 0.3 * math.sqrt(1 + (2 / 3.0) ** 2)
a1 = 2 * math.pi * wp / math.log(f_tot(-wp, 3.0, 1.0) / f_tot(wp, 3.0, 1.0))
a2 = 2 * math.pi * 2 * wp / math.log(f_tot(-2 * wp, 3.0, 1.0) / f_tot(2 * wp, 3.0, 1.0))
print(f"    a_eff(probe w_p)={a1:.3f}  a_eff(2w_p)={a2:.3f}  -> spread {abs(a2/a1-1)*100:.0f}% (shape claim structural, not precision)")
print("  With Deser-Levin A=sqrt(a^2+H^2):  a_eff ~ sqrt(a^2 + H^2 + kappa^2 c^2/T_win^2).")

print()
print("=" * 78)
print("TEST 3 (SHAPE): sympy -- Deser-Levin Delta-T mapping == framework nu EXACTLY")
print("  mapping: m*a*mu(a) = g_bar with mu(a) = [T_U(sqrt(a^2+aL^2)) - T_U(aL)]/T_U(a)")
print("          = [sqrt(a^2+aL^2)-aL]/a  (normalization FORCED: mu->1 automatically)")
print("=" * 78)
import sympy as sp
g, aL = sp.symbols('g a_Lambda', positive=True)
gbar = sp.sqrt(g ** 2 + aL ** 2) - aL          # g_bar = mu(g)*g
a0 = 2 * aL
framework = sp.sqrt(gbar ** 2 + gbar * a0)      # framework g_obs(g_bar) with a0 = 2 aL
check("sqrt(g_bar^2 + g_bar*(2 aL)) == g identically",
      sp.simplify(framework - g) == 0, "=> nu(y)=sqrt(1+1/y) IS the Delta-T form, a0=2*aL")

print()
print("=" * 78)
print("TEST 4 (SCALE): the forced Deser-Levin normalization vs the framework's a0")
print("=" * 78)
c = 2.998e8
Z = math.sqrt(32 * math.pi / 3)
for label, a0v in (("canonical rho_DE/cH_Lambda", 9.36e-11), ("alternate rho_total/cH0", 1.13e-10)):
    cH = Z * a0v                       # the horizon rate this footing uses: a0 = cH/Z
    a0_DL = 2 * cH                     # forced by the Delta-T mapping (aL = cH, a0 = 2 aL)
    print(f"  {label}: a0={a0v:.3e}, cH={cH:.3e}, a0_DL=2cH={a0_DL:.3e}"
          f"  -> a0_DL/a0 = {a0_DL/a0v:.2f} (=2Z)")
print(f"  vs empirical MOND a0=1.2e-10: a0_DL(canonical)/1.2e-10 = {2*Z*9.36e-11/1.2e-10:.1f}x")
print("  => the mechanism reproduces the framework's nu SHAPE exactly, but its FORCED")
print("     coefficient overshoots the framework a0 by 2Z = %.2f on both footings." % (2 * Z))

print()
print("OVERALL:", "PASS" if PASS else "FAIL")
sys.exit(0 if PASS else 1)
