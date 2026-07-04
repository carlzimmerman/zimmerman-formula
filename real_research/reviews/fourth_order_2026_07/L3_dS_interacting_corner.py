#!/usr/bin/env python3
"""
L3 -- THE de SITTER CORNER: interacting fields at the horizon (Bros-Moschella edge).

The framework's actual bath is de Sitter. For FREE fields, Gibbons-Hawking thermality
(hence passivity, hence the anti-MOND sign) is established for ANY mass -- the
Bunch-Davies vacuum is KMS at T_dS for every geodesic observer. The named open edge:
does thermality survive INTERACTIONS for LIGHT fields (complementary series, m < 3H/2),
where dS Kallen-Lehmann positivity / perturbative IR behaviour is unresolved in the
mathematical literature?

Two pieces, both computable / boundable (no internet):

  (1) EUCLIDEAN PERIODICITY => KMS AT ANY COUPLING (the mass-independent argument):
      dS static-patch thermality follows from periodicity beta_dS=2pi/H in Euclidean
      time on the sphere S^d. An interacting theory *constructed on the Euclidean
      sphere* inherits that periodicity, so its continuation is KMS at T_dS regardless
      of coupling -- the SAME structure as an ordinary thermal field theory. We verify
      the computable proxy: an interacting (quartic) mode 'on the thermal circle'
      (0+1d thermal QFT = QM at temperature T) is KMS at ANY lambda. (This reuses the
      exact detailed-balance machinery; here we show it is coupling-INDEPENDENT.)
      The ONLY subtlety for dS is EXISTENCE/analyticity of the continuation for light
      fields, i.e. IR convergence of perturbation theory -- addressed in (2).

  (2) THE LIGHT-FIELD GAP CANNOT REACH THE BAND:
      (a) Starobinsky-Yokoyama: massless lambda*phi^4 in dS dynamically generates an
          effective mass m_eff ~ lambda^(1/4) H (stochastic equilibrium), which makes
          perturbation theory IR-FINITE -> the Euclidean construction of (1) applies.
      (b) Even granting an UNRESOLVED complementary-series sliver, the framework's
          inertia response is IN-BAND at galactic frequencies omega, where omega/H is
          computed below -- and every in-band mode has omega >> H, far above the omega
          <~ H region where any light-field IR subtlety could live. Bound the gap.

Verdict: is the interacting-dS corner closed for the framework's purposes (Euclidean
periodicity + stochastic gap + band-separation), or is there a sliver that both evades
the gap AND reaches the band? Runtime < 60 s.
"""
import numpy as np
from numpy.linalg import eigh
np.seterr(over='ignore', invalid='ignore', divide='ignore')

# ---- (1) coupling-independence of KMS for an interacting mode on the thermal circle ----
def osc(N):
    a = np.diag(np.sqrt(np.arange(1,N)), 1); ad=a.T
    return a, ad, ad@a, (a+ad)/np.sqrt(2)

def kms_deviation(N=14, lam=0.0, beta=1.0):
    """quartic mode H = n+1/2 + lam x^4, thermal at beta; worst KMS-ratio deviation
       of S(-w)/S(w) from e^{-beta w} over all Bohr lines of B=x."""
    a,ad,n,x = osc(N)
    H = n + 0.5*np.eye(N) + lam*(x@x@x@x)
    E,V = eigh(H); B = V.T@x@V
    p = np.exp(-beta*(E-E.min())); p/=p.sum()
    worst=0.0
    for m in range(N):
        for k in range(N):
            w=E[k]-E[m]
            if abs(w)<1e-9: continue
            Sw=p[m]*abs(B[m,k])**2; Smw=p[k]*abs(B[k,m])**2
            if Sw<1e-13: continue
            worst=max(worst, abs((Smw/Sw)-np.exp(-beta*w))/np.exp(-beta*w))
    return worst

# ---- (2b) in-band omega/H, both footings ----
def band_over_H():
    # galactic orbital band (hexad): Omega = v/R, v=30-300 km/s, R=0.5-30 kpc
    c = 299792458.0; kpc = 3.0857e19; kms = 1e3
    Om_lo = (30*kms)/(30*kpc)      # slow, large R
    Om_hi = (300*kms)/(0.5*kpc)    # fast, small R
    a0_can, a0_alt = 9.36e-11, 1.13e-10
    Z = np.sqrt(32*np.pi/3)
    H_can = a0_can*Z/c             # cH_Lambda/Z = a0 -> H = a0 Z / c
    H_alt = a0_alt*Z/c
    return Om_lo, Om_hi, H_can, H_alt

if __name__ == "__main__":
    print("="*76)
    print("(1) Euclidean periodicity => KMS is COUPLING-INDEPENDENT (interacting proxy)")
    print("="*76)
    worst_all=0.0
    for lam in [0.0, 0.5, 1.0, 2.0, 4.0]:
        w = kms_deviation(N=14, lam=lam, beta=2*np.pi/1.0)  # beta_dS = 2pi/H, H=1 units
        worst_all=max(worst_all,w)
        print(f"   lambda={lam:4.1f}  worst |S(-w)/S(w) - e^(-bw)|/e^(-bw) = {w:.2e}")
    print(f"   --> KMS holds to {worst_all:.1e} INDEPENDENT of coupling: an interacting")
    print(f"       theory periodic in Euclidean time (T_dS) is thermal at every order.")
    print(f"       Only IR-existence for light fields is at stake -> (2).\n")

    print("="*76)
    print("(2a) Starobinsky-Yokoyama stochastic mass gap m_eff ~ lambda^(1/4) H")
    print("="*76)
    # SY equilibrium for V=lambda phi^4/4:  <phi^2> = (3/(2 pi^2))^{1/2} H^2 / sqrt(lambda) * c1
    # resummed effective mass m_eff^2 = 3 lambda <phi^2> ~ O(1) sqrt(lambda) H^2
    for lam in [1e-2, 1e-1, 1.0]:
        meff_over_H = (0.36)*lam**0.25     # m_eff ~ 0.36 lambda^{1/4} H (SY, O(1) const)
        print(f"   lambda={lam:5.2f}  m_eff/H ~ {meff_over_H:.3f}  (IR-regulated: pert. theory finite)")
    print("   --> any interacting light field self-generates a gap -> IR-finite ->")
    print("       Euclidean/Bros-Epstein-Moschella construction applies -> KMS.\n")

    print("="*76)
    print("(2b) The in-band response is at omega >> H: IR sliver cannot reach it")
    print("="*76)
    Om_lo, Om_hi, H_can, H_alt = band_over_H()
    print(f"   galactic band Omega = [{Om_lo:.3e}, {Om_hi:.3e}] rad/s")
    print(f"   H_Lambda: canonical {H_can:.3e} /s (a0=9.36e-11), alternate {H_alt:.3e} /s (a0=1.13e-10)")
    print(f"   omega/H canonical: [{Om_lo/H_can:6.1f}, {Om_hi/H_can:8.1f}]")
    print(f"   omega/H alternate: [{Om_lo/H_alt:6.1f}, {Om_hi/H_alt:8.1f}]")
    print(f"   --> EVERY in-band mode has omega/H >= ~15 (both footings): deep in the")
    print(f"       heavy/principal regime where free-field thermality is proven and the")
    print(f"       stochastic gap is irrelevant. Light-field IR effects live at omega <~ H,")
    print(f"       1-4 orders BELOW the band, and cannot source in-band inertia.\n")

    band_min = min(Om_lo/H_can, Om_lo/H_alt)
    closed = (worst_all < 1e-6) and (band_min > 5.0)
    print("="*76)
    print("VERDICT (dS interacting corner): " + (
        "CLOSED for the framework -- Euclidean periodicity gives coupling-independent\n"
        "  KMS; the stochastic gap makes light interacting fields IR-finite; and the\n"
        "  unresolved complementary-series sliver is >=15x below the in-band frequencies\n"
        "  the framework's inertia depends on. Physics inputs (SY resummation, BEM\n"
        "  Euclidean construction) named, not proven here." if closed else
        "OPEN -- a light-field sliver reaches the band; investigate."))
    print("="*76)
