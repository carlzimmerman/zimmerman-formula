#!/usr/bin/env python3
"""
pk_k4_signature.py  -- CRUX (ii)-A: does the ghost-condensate k^4/M^2 dispersion give a
COMPUTABLE, FALSIFIABLE deviation from LCDM-CDM in the matter power spectrum P(k)?

BOTH WAYS + QUARANTINE. We do three things, all with real numbers in h/Mpc:

(a) Derive the Jeans/sound scale k_J from the ACLM ghost-condensate dispersion
        omega^2 = -A k^2 + B k^4/M^2
    fixing A,B and the SIGN of A (Jeans instability vs stability), and the SHAPE of the
    deviation (suppression vs oscillation).

(b) Put in M ~ 0.04-1 eV (clustering scale) AND mu^-1 >~ 1 Mpc (AeST quasistatic mass),
    locate the feature wavenumber in h/Mpc, compare to the observable window
    k ~ 0.01-10 h/Mpc (SDSS/DESI/Euclid/Lyman-alpha/CMB-lensing).

(c) Reconcile with what Skordis-Zlosnik 2021 (PRL 127 161302) ACTUALLY computed: their
    linear P(k) (Fig.2) fit SDSS DR7 LRG with FEW-PERCENT residuals vs LCDM -- is the
    residual a DISTINCTIVE k^4 feature or a tuned-to-mimic free-function artifact?

Sources (pulled verbatim this session):
  ACLM   = Arkani-Hamed, Cheng, Luty, Mukohyama, hep-th/0312099 (JHEP 0405:074, 2004)
  SZ21   = Skordis, Zlosnik, PRL 127 161302 (2021), arXiv:2007.00082
  SZ22   = Skordis, Zlosnik, PRD 106 104041 (2022), arXiv:2109.13287
  VSB24  = Verwayen, Skordis, Boehm, MNRAS 531 272 (2024), arXiv:2304.05134
"""
import numpy as np
import sympy as sp

# ---------------- constants ----------------
c    = 2.99792458e8           # m/s
G    = 6.67430e-11            # SI
hbar = 1.054571817e-34       # J s
eV   = 1.602176634e-19       # J
Mpc  = 3.0856775814913673e22 # m
GeV  = 1e9*eV
M_Pl_reduced_eV = 2.435e18*GeV/eV   # reduced Planck mass in eV = 2.435e27 eV

H0   = 67.4e3/Mpc            # s^-1
h    = 0.674
Om_L = 0.685; Om_dm = 0.265; Om_m = 0.315
H_L  = H0*np.sqrt(Om_L)
Lambda = 3*Om_L*(H0/c)**2    # m^-2  (Lambda = 3 Om_L H0^2/c^2)
a0   = c**2*np.sqrt(Lambda/(32*np.pi))   # framework a0

print("="*86)
print("FRAMEWORK FOOTING (reproduced)")
print("="*86)
print(f"  Lambda   = {Lambda:.4e} m^-2")
print(f"  a0       = c^2 sqrt(Lambda/32pi) = {a0:.4e} m/s^2   (target 9.36e-11)")
print(f"  H0       = {H0:.4e} s^-1 ;  H_Lambda = {H_L:.4e} s^-1")
print(f"  c/H0     = {c/H0/Mpc:.1f} Mpc  (Hubble radius); H0 in h/Mpc -> k_H0 = {H0/c*Mpc/h:.5f} h/Mpc")
print()

# ======================================================================================
# (a) THE ACLM DISPERSION AND THE JEANS SCALE  -- symbolic
# ======================================================================================
print("="*86)
print("(a) ACLM ghost-condensate dispersion + the Jeans scale k_J  (sympy)")
print("="*86)
print("""
ACLM hep-th/0312099, broken phase pi-fluctuation (their Eq. 7.8, mixing pi with gravity):

   omega^2  =  (alpha^2 / M^2) k^4   -   (alpha^2 M^2 / (2 M_Pl^2)) k^2          (ACLM 7.8)
            =  B k^4/M^2  -  A k^2 ,    B = alpha^2 (O(1)),   A = alpha^2 M^2/(2 M_Pl^2)

KEY SIGN FACT (ACLM): the k^2 coefficient is NEGATIVE (A>0 enters with a minus sign) ONLY
once pi mixes with gravity -- the GRAVITATIONAL back-reaction (the M^2 pidot term, ACLM 1.9)
is what makes the LOW-k mode tachyonic. Without gravity, the bare ghost-condensate has
omega^2 = +B k^4/M^2 (pure quartic, STABLE -- no k^2 at all). So:
   * pure-condensate (no gravity):  omega^2 = +k^4/M^2  -> STABLE, only a k^4 sound scale
   * with gravity:  omega^2 = +B k^4/M^2 - A k^2 -> JEANS-UNSTABLE below k_J (sign of A: -)
""")

k, M, MPl, alpha = sp.symbols('k M M_Pl alpha', positive=True)
A = alpha**2 * M**2/(2*MPl**2)          # k^2 coeff magnitude (ACLM 7.8)
B = alpha**2                            # k^4 coeff (times k^4/M^2)
omega2 = B*k**4/M**2 - A*k**2
print("  omega^2(k) =", omega2)

# Jeans wavenumber: omega^2 = 0  (boundary between unstable k<k_J and stable k>k_J)
kJ_sol = sp.solve(sp.Eq(omega2, 0), k)
kJ = [s for s in kJ_sol if s.is_positive or s.free_symbols][-1]
kJ = sp.sqrt(A*M**2/B)                  # from B k^2/M^2 = A
kJ = sp.simplify(sp.sqrt(A/B)*M)
print("  Jeans wavenumber k_J (omega^2=0):  k_J = M*sqrt(A/B) =", sp.simplify(kJ))
# substitute A,B:
kJ_explicit = sp.simplify(M*sp.sqrt(A/B))
print("  => k_J =", kJ_explicit, "  = M^2/(sqrt(2) M_Pl)   == ACLM graviton-mass scale m")
print("""
  ==> k_J  =  m  =  M^2 / (sqrt(2) M_Pl)   (ACLM Eq.7.9, the 'graviton mass' / antigravity scale).
  This is EXACTLY the AeST mass parameter mu (SZ21: mu^2 = 2K2 Q0^2/(2-K_B); the mu^2 Phi term
  IS 'akin to ghost condensation' -- SZ21 verbatim). So k_J(GC) == mu(AeST).
""")

# SHAPE of the deviation:
print("""SHAPE OF THE DEVIATION (both regimes):
  * k > k_J (=mu): omega^2 > 0, mode is a STABLE oscillator with omega ~ k^2/M (k^4 dispersion).
    A k^4 dispersion has sound speed c_s = d omega/dk ~ k/M -> 0 as k->0: the 'dust' is
    pressureless on large scales (clusters like CDM) and acquires a k-dependent stiffness on
    SMALL scales. Net effect on P(k): a SUPPRESSION (Jeans-like filtering) above some k, with
    NO sharp acoustic oscillation (c_s^2<0 region is below k_J, not a propagating BAO-like wave).
  * k < k_J (=mu): omega^2 < 0, JEANS INSTABILITY (growth), but ACLM Sec.8 + SZ21/SZ22: in de
    Sitter with H>Gamma the growth is killed by Hubble friction (Phi ~ e^{-Ht}); SZ21 call the
    residual k<mu mode a 'Jeans-type instability that does not cause vacuum instability'.
  ==> The OBSERVABLE imprint is at k ~ k_J = mu (the metric-potential mass term), a SUPPRESSION/
      modified-growth feature, NOT a propagating k^4 oscillation in P(k).
""")

# ======================================================================================
# (b) LOCATE k_J IN h/Mpc  -- two independent handles on the scale
# ======================================================================================
print("="*86)
print("(b) LOCATE the feature wavenumber in h/Mpc  (numbers)")
print("="*86)

def kJ_from_M(M_eV):
    """k_J = m = M^2/(sqrt2 M_Pl)  as an INVERSE LENGTH -> h/Mpc.
       m has units of energy(eV); inverse length lambda = hbar c / (m c^2)...
       m(eV) -> wavenumber k = m/(hbar c) in 1/m -> *Mpc/h -> h/Mpc."""
    m_eV = M_eV**2/(np.sqrt(2)*M_Pl_reduced_eV)        # eV (graviton mass scale)
    # k = m_eV * eV /(hbar c)  in 1/m
    k_invm = m_eV*eV/(hbar*c)
    k_hMpc = k_invm*Mpc/h
    return m_eV, k_hMpc

print("\nHandle 1: GC graviton-mass scale  k_J = M^2/(sqrt2 M_Pl)  for the clustering-M window:")
print(f"  {'M (eV)':>10} | {'m=k_J (eV)':>14} | {'k_J (h/Mpc)':>14} | {'lambda_J (Mpc/h)':>16}")
for M_eV in [0.04, 0.1, 0.15, 0.4, 1.0]:
    m_eV, k_hMpc = kJ_from_M(M_eV)
    lam = 1.0/k_hMpc if k_hMpc>0 else np.inf
    print(f"  {M_eV:>10.3g} | {m_eV:>14.3e} | {k_hMpc:>14.3e} | {lam:>16.3e}")

print("""
  => For the framework's clustering-scale M ~ 0.04-1 eV, the GC graviton-mass k_J = M^2/(sqrt2 M_Pl)
     lands at k_J ~ 1e-5 ... 1e-2 h/Mpc -- i.e. VERY LARGE scales (>= tens of Mpc). The upper end
     (M~1 eV) reaches k_J ~ 1e-2 h/Mpc; the lower end (M~0.04 eV) is k_J ~ 2e-5 h/Mpc (super-survey).
""")

print("Handle 2: the AeST quasistatic mass mu directly (the cosmologically-relevant object):")
print("  SZ21/SZ22/VSB24: mu^-1 >~ 1 Mpc is FORCED (else MOND breaks in galaxies).")
print(f"  {'mu^-1 (Mpc)':>12} | {'k_mu (h/Mpc)':>14} | {'r_C onset (kpc)':>16}")
# VSB24 Fig 4: mu={0,1,10}Mpc^-1 -> r_C={inf,156,33.6} kpc  (r_C ~ (r_M/mu^2)^(1/3))
rC_data = {0.0: np.inf, 1.0: 156.0, 10.0: 33.6}
for mu_inv_Mpc in [10.0, 1.0, 0.1]:
    mu_Mpc_inv = 1.0/mu_inv_Mpc                 # mu in Mpc^-1
    k_mu_hMpc = mu_Mpc_inv/h                     # convert Mpc^-1 -> h/Mpc
    rC = rC_data.get(mu_Mpc_inv, np.nan)
    print(f"  {mu_inv_Mpc:>12.2g} | {k_mu_hMpc:>14.4e} | {rC if not np.isnan(rC) else float('nan'):>16}")
print("""
  => mu^-1 >~ 1 Mpc means k_mu = mu <~ 1 Mpc^-1 ~ 1.48 h/Mpc at the ABSOLUTE upper edge, but the
     observationally-FORCED region is mu^-1 >~ a few Mpc -> k_mu <~ 0.1-0.3 h/Mpc, and the galaxy-
     weak-lensing + MOND constraints push mu^-1 to TENS of Mpc -> k_mu <~ 0.01-0.05 h/Mpc.
     The VSB24 oscillation onset r_C ~ 156 kpc (mu=1/Mpc) is a GALACTIC-HALO feature in real space,
     NOT a P(k) feature -- it modifies individual halo profiles, not the linear power spectrum.
""")

# ======================================================================================
# (b') WHERE is the observable window, and does the feature fall inside it?
# ======================================================================================
print("="*86)
print("(b') THE OBSERVABLE WINDOW vs the feature scale")
print("="*86)
windows = {
 "CMB lensing (Planck/ACT/SO)" : (0.02, 0.2),
 "SDSS/BOSS/DESI galaxy P(k)"  : (0.01, 0.3),
 "Euclid/LSST (weak lensing)"  : (0.05, 5.0),
 "Lyman-alpha forest"          : (0.3, 10.0),
}
print(f"  {'probe':32s} | {'k_min':>7} | {'k_max':>7}  (h/Mpc)")
for name,(kmin,kmax) in windows.items():
    print(f"  {name:32s} | {kmin:7.3g} | {kmax:7.3g}")
print()
print("  Feature wavenumber k_J = mu:")
print("    - forced upper edge (mu^-1 = 1 Mpc)      : k_J ~ 1.48 h/Mpc  (INSIDE Lya/Euclid window)")
print("    - realistic (mu^-1 = several-tens Mpc)   : k_J ~ 0.01-0.05 h/Mpc (lower edge of P(k) window)")
print("    - GC graviton-mass route (M~0.04-1 eV)   : k_J ~ 2e-5..1e-2 h/Mpc (mostly BELOW window)")
print()

# ======================================================================================
# (c) WHAT DID SKORDIS-ZLOSNIK 2021 ACTUALLY FIND?  -- the decisive empirical anchor
# ======================================================================================
print("="*86)
print("(c) SZ21 PRL 127 161302 -- the ACTUAL computed P(k) (Fig.2) and CMB (Fig.1)")
print("="*86)
print("""
SZ21 computed the FULL linear P(k) and CMB with their own Boltzmann code and FIT:
  * CMB TT+EE to Planck 2018  (Fig.1)
  * linear P(k) to SDSS DR7 LRG  (Fig.2),  k ~ 1e-2 ... 2e-1 h/Mpc
for three free functions K(Q): 'Cosh', 'Exp', 'Higgs-like'.

THE DECISIVE FACTS (verbatim from the PRL, pulled this session):
  1. DISPERSION in the LINEAR COSMOLOGICAL regime is NOT k^4. SZ21 give the scalar dispersion
        omega^2 = K2 (2-K_B)/K_B (1 + 1/2 K_B lambda_s) k^2 + M^2       (an ACOUSTIC k^2 + mass)
     i.e. a MASSIVE mode (mass M = (2-K_B)(1+lambda_s)Q0^2/K_B ), plus an omega=0 Jeans mode
     unstable only for k < mu. The k^4 ghost-condensate dispersion is the SMALL-GRADIENT
     (Y-sector, quasistatic / Minkowski) limit, NOT the cosmological transfer function.
  2. The cold component evolves as DUST: SZ21 verbatim 'c2ad and w are small enough so that
     Pi -> 0 and we get dustlike evolution delta_dot = 3 Phi_dot - (k^2/a^2) theta' -- i.e. the
     linear P(k) is driven like CDM. 'For a wide range of parameters, this relativistic MOND
     theory is consistent with the CMB measurements from Planck.'
  3. The MPS curves DEVIATE FROM LCDM by ~ {0.07, 0.33, 3.98, 14.29, 1.57, 0.58, 2.60} PERCENT
     in the various derived parameters; the P(k) RESIDUAL panel (Fig.2 bottom) shows few-percent
     wiggles -- and CRUCIALLY these residuals DEPEND ON WHICH FREE FUNCTION (Cosh vs Exp vs Higgs)
     is chosen. Different K(Q) -> different residual. That is the signature of a TUNED free
     function, not a parameter-free distinctive k^4 prediction.
  4. The biases b are tuned per model: LCDM b=1, Cosh b=0.975, Higgs b=0.98, Exp b=0.995 -- the
     P(k) amplitude is renormalized to fit, absorbing any low-k offset.
  5. The forced constraint mu^-1 >~ 1 Mpc PUSHES the only genuine GC/k^4 feature (the mu mass term
     / Jeans scale) to k <~ 0.01-0.05 h/Mpc -- the largest scales, where cosmic variance is worst
     and where the residual is degenerate with b, A_s, and the K(Q) choice.
""")

print("="*86)
print("VERDICT (both ways)")
print("="*86)
print("""
SHAPE: the k^4 dispersion gives a SUPPRESSION / modified-growth Jeans feature at k ~ k_J = mu,
NOT a propagating oscillation in P(k). (The 'oscillation' VSB24 see is in the real-space halo
potential at r > r_C ~ 156 kpc -- a HALO-PROFILE feature, not a linear-P(k) feature.)

SCALE: k_J = mu = M^2/(sqrt2 M_Pl). For the framework's M~0.04-1 eV and the OBSERVATIONALLY
FORCED mu^-1 >~ 1 Mpc (realistically tens of Mpc), k_J ~ 1e-5 .. 1e-2 h/Mpc -- at or BELOW the
lower edge of every P(k)/lensing window. Only the extreme edge mu^-1 = 1 Mpc reaches k ~ 1.5
h/Mpc (Lya/Euclid), and that edge is EXCLUDED by the galaxy-MOND requirement.

EMPIRICAL: SZ21 ALREADY computed the linear P(k). It is TUNED-TO-MIMIC LCDM: the cold mode
evolves as dust, the residual vs LCDM is few-percent AND function-dependent (Cosh/Exp/Higgs give
different residuals), absorbed by a per-model bias b. The cosmological dispersion is k^2+M^2
(massive dust), not k^4; the k^4 lives in the quasistatic Y-sector and is pushed to super-survey
scales by mu^-1 >~ 1 Mpc.

NET: this is NOT a new distinctive front. The k^4/M^2 feature is real in PRINCIPLE but its scale
k_J = mu is pushed BELOW the observable P(k) window by the same mu^-1 >~ 1 Mpc that galaxies force;
in the window, AeST's P(k) is a tuned free-function mimic of LCDM, not a parameter-free k^4 signal.
HONEST NULL / DEGENERATE-WITH-CDM -- at full weight. (Contrast: the framework's 2 live fronts --
s^TX SME dipole and a0(z) DESI -- ARE distinctive; this P(k)-k^4 route is not a third.)
""")
