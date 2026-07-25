#!/usr/bin/env python3
"""
highz_deepmond_target_list_2026.py -- D-1: REAL NAMED z~1.5-2.5 CANDIDATES FOR THE
DEEP-MOND CUT g_bar < 0.3 a0.  TARGET IDENTIFICATION ONLY (no GO/NO-GO is rendered here).
==========================================================================================
Carl Zimmerman's de Sitter-Unruh MODIFIED-INERTIA framework: a0 = c H_Lambda / Z,
Z = sqrt(32 pi / 3) = 5.78881 (computed here, not quoted), canonical a0(0) = 9.355e-11 m/s^2 (alt footing cH0/Z =
1.1305e-10); its OWN dS-Unruh interpolation g_obs = sqrt(g_bar^2 + g_bar a0), equivalently
the EXACT a0-line identity g_obs^2 - g_bar^2 = a0 g_bar.  nu = sqrt(1+1/y) is Milgrom 1999
(PLA 253:273 Eq.9) -- wellhead credit; the framework's distinctive content is the cH_Lambda/Z
coefficient plus the MI completion.  McCulloch (MiHsC) credited for the rising/Hubble reading.
a0's VALUE and the HORIZON CHOICE are POSITS.  No TOE.  No "theory closed".

ROLE IN THE DEC-vs-RISE PROGRAM (committed parents, not modified here):
  desitter_unruh_horizon_fork_2026.py  DEC (dS/future-event horizon) = 0.874 @ z=2 ;
                                       RISE (Hubble horizon, McCulloch) = 3.005 @ z=2 ;
                                       3.44x apart -> ~37% a0 precision = 3-sigma call.
  a0z_fork_likelihood_2026.py          prior-robust 20:1 needs sigma(a0) ~ 10.9% @ z=2 ;
                                       framework-derived dilution lever L = 1/(1+2y).
  highz_a0_fork_confront_2026.py       decisive spec: z~2-3, g_bar < 0.3 a0, N~15-40 --
                                       and the finding that NO current sample meets the cut.
  estimator_bias_mocks.py              RESOLVED estimator: GLS biased +10.34pp; the frozen
                                       PRIMARY is galaxy_median_then_median (+0.31pp).

THIS FILE ANSWERS ONE QUESTION AND ONLY THAT QUESTION:
  Are there REAL, NAMED objects at z ~ 1.5-2.5 that could satisfy g_bar < 0.3 a0, and for
  how many of them is g_bar/a0 actually COMPUTABLE from published data?

HARD CALIBRATION (a manufactured target list is penalized exactly as a manufactured desert):
  * Every object below is a REAL published object with an in-line citation.  Nothing invented.
  * Every number is tagged PUB (published value), DERIVED (arithmetic on published values),
    SCALED (published scaling relation applied -- Tacconi+2018 / van der Wel+2014), or
    UNMEASURED.  A SCALED gas mass is NOT allowed to create a "pass".
  * The pass/fail verdict per object is rendered THREE ways: on PUB data only, on the
    optimistic bracket, and on the pessimistic bracket.  A pass only counts as CONFIRMED
    when it survives PUB-only.
  * The two things lensing does to the observables are DERIVED (sympy, S1), not asserted:
    g_bar is magnification-INVARIANT (it is a surface density) but the deep-MOND a0 readout
    is LINEAR in mu.  That is good news for the SELECTION and bad news for the PRECISION,
    and both halves are printed.
  * Both footings carried: the cut threshold itself is footing-dependent (0.3 a0 is 21%
    higher on the alt footing), so BOTH Sigma_cut values are printed.  The DEC/RISE ratio
    the program is testing remains footing-independent.
Exit 0 = target list built + computability audited.  NOT a verdict, NOT a GO/NO-GO.
"""
import numpy as np
import sympy as sp
import json
import os

np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
BAR = "=" * 104

# ==========================================================================================
# CONSTANTS
# ==========================================================================================
G = 6.67430e-11                     # m^3 kg^-1 s^-2  (CODATA 2018)
MSUN = 1.98892e30                   # kg
PC = 3.0856775814913673e16          # m
KPC = 1.0e3 * PC
Z_CONST = float(np.sqrt(32 * np.pi / 3))
A0_CAN = 9.355e-11                  # canonical  c H_Lambda / Z   (rho_DE footing)
A0_ALT = 1.1305e-10                 # alt        c H0 / Z         (rho_total footing)
CUT = 0.30                          # the deep-MOND selection cut: g_bar < CUT * a0(0)

# the two bars this program is aiming at (from the committed parents)
BAR_3SIG = 0.37                     # ~37% a0 precision @ z=2 -> 3-sigma DEC-vs-RISE call
BAR_20TO1 = 0.109                   # ~10.9% @ z=2 -> prior-robust 20:1 Bayes factor

print(BAR)
print("D-1  TARGET IDENTIFICATION: real named z~1.5-2.5 candidates for g_bar < 0.3 a0")
print(BAR)
print(f"  a0 = c H_Lambda / Z,  Z = {Z_CONST:.5f};  canonical a0(0) = {A0_CAN:.4e} m/s^2,"
      f"  alt = {A0_ALT:.4e}.")
print(f"  Deep-MOND selection cut: g_bar < {CUT:g} a0(0).  Bars: {100*BAR_3SIG:.0f}% a0 = 3-sigma"
      f" mechanism call; {100*BAR_20TO1:.1f}% = prior-robust 20:1.")

# ==========================================================================================
# S0 -- WHAT THE CUT ACTUALLY MEANS OBSERVATIONALLY  (three equivalent forms)
# ==========================================================================================
print("\n" + BAR)
print("S0 -- TRANSLATING g_bar < 0.3 a0 INTO OBSERVABLES (surface density / radius / velocity)")
print(BAR)


def sigma_cut(a0, cut=CUT):
    """Mean ENCLOSED baryonic surface density at the cut: g_bar = G M/R^2 = pi G Sigma_enc,
    Sigma_enc := M_bar/(pi R^2).  Returns Msun/pc^2."""
    sig_si = cut * a0 / (np.pi * G)                      # kg/m^2
    return sig_si * PC ** 2 / MSUN


def R_required_kpc(Mbar_msun, a0=A0_CAN, cut=CUT):
    """The OUTERMOST kinematic radius the data must reach for the object to satisfy the cut:
    G M_bar / R^2 < cut*a0  =>  R > sqrt(G M_bar/(cut a0))."""
    R = np.sqrt(G * np.asarray(Mbar_msun, float) * MSUN / (cut * a0))
    return R / KPC


def gbar_over_a0(Mbar_msun, R_kpc, a0=A0_CAN):
    """g_bar/a0(0) = G M_bar / (R^2 a0).  Spherical-equivalent (point-mass) form."""
    R = np.asarray(R_kpc, float) * KPC
    return G * np.asarray(Mbar_msun, float) * MSUN / (R ** 2 * a0)


def V_at_cut_kms(R_kpc, a0=A0_CAN, cut=CUT):
    """Circular speed a system AT the cut would show: g_obs = sqrt(g_bar^2+g_bar a0) with
    g_bar = cut*a0 -> V = sqrt(g_obs R).  The framework's OWN kernel (not McGaugh's nu)."""
    gb = cut * a0
    gobs = np.sqrt(gb ** 2 + gb * a0)
    return np.sqrt(gobs * np.asarray(R_kpc, float) * KPC) / 1.0e3


for lab, a0 in [("canonical cH_Lambda/Z", A0_CAN), ("alt cH0/Z", A0_ALT)]:
    print(f"  [{lab:22}] a0/(2 pi G) = {a0/(2*np.pi*G)*PC**2/MSUN:7.1f} Msun/pc^2   "
          f"cut Sigma_enc < {sigma_cut(a0):6.1f} Msun/pc^2")
print("  => the deep-MOND cut IS a baryonic SURFACE-DENSITY cut.  For reference the local")
print("     Freeman HSB disk value is ~100-150 Msun/pc^2 and cosmic-noon main-sequence discs")
print("     run 100-1000 Msun/pc^2 -- i.e. the cut is INTRINSICALLY RARE at z~2, which is a")
print("     PHYSICS obstacle, not only an observational one.  Stated up front.")
print(f"\n  Required outermost kinematic radius R_req = sqrt(G M_bar/({CUT:g} a0)) "
      f"= {R_required_kpc(1e9):.3f} kpc * sqrt(M_bar/1e9 Msun):")
print(f"    {'M_bar [Msun]':>14} | {'R_req canon [kpc]':>17} | {'R_req alt [kpc]':>15} | "
      f"{'V at the cut [km/s]':>19}")
for M in [1e8, 3e8, 1e9, 3e9, 1e10, 3e10, 1e11]:
    Rc = float(R_required_kpc(M, A0_CAN))
    Ra = float(R_required_kpc(M, A0_ALT))
    print(f"    {M:>14.1e} | {Rc:>17.2f} | {Ra:>15.2f} | {float(V_at_cut_kms(Rc)):>19.1f}")
print("  => TWO independent routes into the cut: LOWER M_bar, or LARGER R.  Because")
print("     g_bar ~ M/R^2, doubling the measured radius is worth quartering the mass.")
print("     Both routes are represented in the target table below (dwarf route + big-disc route).")

# ==========================================================================================
# S1 -- WHAT MAGNIFICATION DOES (sympy-derived, not asserted): the good half and the bad half
# ==========================================================================================
print("\n" + BAR)
print("S1 -- LENSING ALGEBRA (sympy): g_bar is mu-INVARIANT; the deep-MOND a0 readout is ~mu")
print(BAR)
mu, Mi, Ri, V, a0s = sp.symbols("mu M_img R_img V a0", positive=True)
# source-plane de-lensing: mass scales as 1/mu ; solid angle (hence area) scales as 1/mu, so
# the equivalent-circular source radius scales as 1/sqrt(mu).  Velocities are UNCHANGED by
# lensing (gravitational lensing preserves spectra/redshifts).
M_src = Mi / mu
R_src = Ri / sp.sqrt(mu)
g_bar_src = G * M_src / R_src ** 2
g_obs_src = V ** 2 / R_src
a0_read = sp.simplify((g_obs_src ** 2 - g_bar_src ** 2) / g_bar_src)     # the a0-line readout
print(f"  M_src = M_img/mu ,  R_src = R_img/sqrt(mu) ,  V unchanged by lensing.")
print(f"  g_bar(source) = {sp.simplify(g_bar_src)}")
d_gbar = sp.simplify(sp.diff(sp.log(g_bar_src), mu) * mu)
assert d_gbar == 0, "g_bar must be magnification-invariant"
print(f"  d ln g_bar / d ln mu = {d_gbar}      -> g_bar is EXACTLY mu-INVARIANT (it is pi G Sigma).")
d_gobs = sp.simplify(sp.diff(sp.log(g_obs_src), mu) * mu)
print(f"  d ln g_obs / d ln mu = {d_gobs}    -> g_obs ~ sqrt(mu).")
# deep-MOND limit of the readout: g_obs >> g_bar
a0_deep = sp.simplify(g_obs_src ** 2 / g_bar_src)
d_a0 = sp.simplify(sp.diff(sp.log(a0_deep), mu) * mu)
assert sp.simplify(a0_deep - V ** 4 / (G * Mi / mu)) == 0
assert sp.simplify(d_a0 - 1) == 0, "deep-MOND a0 readout must be linear in mu"
assert sp.simplify(d_gobs - sp.Rational(1, 2)) == 0, "g_obs must scale as sqrt(mu)"
print(f"  deep-MOND readout a0 = V^4/(G M_bar) = {a0_deep}")
print(f"  d ln a0 / d ln mu = {d_a0}          -> a0 readout is EXACTLY LINEAR in mu.")
print("\n  THE SPLIT (both halves load-bearing, neither spun):")
print("   (+) GOOD: the SELECTION cut g_bar<0.3a0 is mu-INVARIANT, so a factor-2 lens-model")
print("       disagreement does NOT move an object across the cut.  Deep-MOND selection is")
print("       therefore ROBUST to the single largest lensing systematic.")
print("   (-) BAD: the a0 VALUE inherits sigma(mu)/mu ONE-TO-ONE.  Published cluster-arc")
print("       models give mu to ~10-30% typically, and MACS0451 below carries a mu = 21.5")
print("       vs 49 disagreement between two refereed papers = a FACTOR 2.3 = a factor 2.3")
print(f"       in a0.  A 10-30% mu error alone already brackets the {100*BAR_20TO1:.1f}% (20:1) bar and")
print(f"       eats a large part of the {100*BAR_3SIG:.0f}% (3-sigma) bar.  Target selection must")
print("       therefore PREFER multiply-imaged arcs with many lens-model constraints and")
print("       AVOID objects sitting on/near a critical curve.")

# ==========================================================================================
# S2 -- PUBLISHED SCALING RELATIONS used ONLY to BRACKET unmeasured quantities
# ==========================================================================================
def mu_mol_tacconi(z, logMstar, dMS=1.0):
    """Molecular gas-to-stellar ratio M_mol/M*.  Tacconi, Genzel & Sternberg -- the
    Tacconi+2018 (ApJ 853,179) global scaling:
       log mu_mol = A + B[log(1+z)-F]^2 + C log(dMS) + D (log M* - 10.7)
    with (A,B,F,C,D) = (0.12, -3.62, 0.66, 0.53, -0.35).
    *** EXTRAPOLATION WARNING: the calibrating samples barely reach log M* < 9.5.  Every use
    below log M* = 9.0 is an EXTRAPOLATION and is labelled SCALED, never PUB. ***"""
    A, B, F, C, D = 0.12, -3.62, 0.66, 0.53, -0.35
    return 10.0 ** (A + B * (np.log10(1.0 + z) - F) ** 2 + C * np.log10(dMS)
                    + D * (logMstar - 10.7))


def re_vdw14_kpc(z, logMstar):
    """Late-type/SFG mass-size relation, van der Wel+2014 (ApJ 788,28) form
    r_e = A (M*/5e10)^0.22 with A ~ 3.3, 2.8, 2.5 kpc at z ~ 1.75, 2.25, 2.75.
    Scatter ~0.19 dex.  Used ONLY to bracket R_out where no size is published."""
    A = np.interp(z, [1.25, 1.75, 2.25, 2.75], [4.0, 3.3, 2.8, 2.5])
    return A * (10.0 ** logMstar / 5.0e10) ** 0.22


print("\n" + BAR)
print("S2 -- BRACKETING RELATIONS (used ONLY where a quantity is UNMEASURED; never to create")
print("      a 'pass'; every bracketed number is tagged SCALED)")
print(BAR)
print("  gas : Tacconi+2018 ApJ 853,179 mu_mol scaling  (EXTRAPOLATED below log M*=9.0)")
print("  size: van der Wel+2014 ApJ 788,28 SFG mass-size, R_out taken as 2.0 r_e (pessimistic)")
print("        to 3.0 r_e (optimistic).  Ionized-gas discs run ~1.0-1.3x the stellar r_e")
print("        (Nelson+2016, Wilman+2020), which is inside this bracket.")
print("  HI  : *** UNMEASURABLE at z~2 ***.  Carried as an INTERVAL M_HI in [0, M_mol].")
print("        SIGN-LOCKED CONSEQUENCE (stated because it matters for the fork): omitting HI")
print("        UNDER-estimates M_bar, which (a) makes an object look MORE deep-MOND than it")
print("        is, and (b) makes the readout a0 = V^4/(G M_bar) come out HIGH -- i.e. it")
print("        pushes toward RISE.  Same sign as the Magneticum apparent drift.  It does NOT")
print("        help the DEC branch and must not be presented as if it did.")
print(f"    {'z':>4} {'logM*':>6} | {'mu_mol (Tacconi18)':>19} {'r_e [kpc] (vdW14)':>18}")
for z in [1.6, 2.0, 2.4]:
    for lm in [8.0, 8.5, 9.0, 9.5, 10.0]:
        print(f"    {z:>4.1f} {lm:>6.2f} | {float(mu_mol_tacconi(z, lm)):>19.2f} "
              f"{float(re_vdw14_kpc(z, lm)):>18.2f}")

# ==========================================================================================
# S3 -- THE TARGET TABLE.  Every row a REAL published object; every field tagged.
#       Mstar / Mmol in Msun (source-plane, i.e. already magnification-corrected as published)
#       Rout_kpc = outermost radius of EXISTING resolved kinematics (source plane), or None
# ==========================================================================================
# tags:  PUB = published value  |  SCALED = from a cited scaling relation  |  UNMEAS = absent
T = [
    # -------------------------------------------------------------------------------------
    # TIER 1: z=1.5-2.5, LENSED, resolved kinematics EXIST *and* a cold-gas mass EXISTS.
    # -------------------------------------------------------------------------------------
    dict(name="MACS0451-arc (MACS J0451+0006)", z=2.013, mu=49.0, mu_alt=21.5,
         Mstar=2.05e9, Mstar_tag="PUB", Mmol=5.1e9, Mmol_tag="PUB",
         Rout=2.5, Rout_tag="PUB", V=38.0, sig=80.0, vsig_pub=0.48,
         kin="Keck/OSIRIS AO Ha (RESOLVED)",
         tier=1,
         cite="Jones+2010 MNRAS 404,1247 (z=2.014, mu=49+/-11, D=5+/-1 kpc, Vsin i=38+/-10, "
              "sig=80+/-5); Dessauges-Zavadsky+2015 A&A 577,A50 (CO(3-2), alpha_CO=4.36, "
              "M_mol=5.1e9, f_gas=0.71, mu=21.5); Schaerer+2015 A&A 576,L2 (ALMA [CII] 10sig, "
              "mu=49+/-5, M*~2.5e9)",
         note="THE ONLY z~2 object in the literature with BOTH resolved kinematics AND a "
              "cold-gas mass. mu disagreement 21.5 vs 49 between two refereed papers = a "
              "factor 2.3 directly on any a0 readout. Vsin i/sig = 0.48 -> DISPERSION-"
              "DOMINATED, not a usable rotator as observed."),
    # -------------------------------------------------------------------------------------
    # TIER 2: z=1.5-2.5, LENSED, resolved kinematics EXIST, NO gas mass (M* only).
    #   OLAS = Hirtenstein+2019 ApJ 880,54 (arXiv:1811.11768), Keck/OSIRIS AO, Tables 1-2.
    #   sig = integrated sigma; V = Delta_v/2 from the published peak-to-peak shear.
    # -------------------------------------------------------------------------------------
    dict(name="OLAS A370-03097", z=1.55, mu=2.30, Mstar=10 ** 9.32, Mstar_tag="PUB",
         Mmol=None, Mmol_tag="UNMEAS", Rout=None, Rout_tag="UNMEAS",
         V=134 / 2, sig=68.8, vsig_pub=2.09, kin="Keck/OSIRIS AO Ha (RESOLVED, class 1)", tier=2,
         cite="Hirtenstein+2019 ApJ 880,54 Table 1 (dv=134 km/s, sig_int=68.8, v/sig=2.09)",
         note="rotation-dominated; no gas mass, no published size"),
    dict(name="OLAS M0717-02064", z=2.07, mu=6.48, Mstar=10 ** 8.08, Mstar_tag="PUB",
         Mmol=None, Mmol_tag="UNMEAS", Rout=None, Rout_tag="UNMEAS",
         V=142 / 2, sig=74.4, vsig_pub=1.64, kin="Keck/OSIRIS AO Ha (RESOLVED, class 1)", tier=2,
         cite="Hirtenstein+2019 ApJ 880,54 Table 1 (dv=142 km/s, sig_int=74.4, v/sig=1.64)",
         note="*** LOWEST-M* rotation-dominated LENSED object known at z>2 (log M*=8.08, "
              "mu=6.48) -> the single best deep-MOND CANDIDATE in the published literature. "
              "But sig=74.4 km/s > V=71 km/s: pressure support is the whole problem."),
    dict(name="OLAS M0744-01203", z=1.65, mu=3.16, Mstar=10 ** 9.26, Mstar_tag="PUB",
         Mmol=None, Mmol_tag="UNMEAS", Rout=None, Rout_tag="UNMEAS",
         V=188 / 2, sig=97.9, vsig_pub=1.28, kin="Keck/OSIRIS AO Ha (RESOLVED, class 1)", tier=2,
         cite="Hirtenstein+2019 ApJ 880,54 Table 1 (dv=188, sig_int=97.9, v/sig=1.28)",
         note="rotation-dominated but very turbulent"),
    dict(name="OLAS M1149-00683", z=1.68, mu=4.05, Mstar=10 ** 8.14, Mstar_tag="PUB",
         Mmol=None, Mmol_tag="UNMEAS", Rout=None, Rout_tag="UNMEAS",
         V=102 / 2, sig=62.9, vsig_pub=1.17, kin="Keck/OSIRIS AO Ha (RESOLVED, class 1)", tier=2,
         cite="Hirtenstein+2019 ApJ 880,54 Table 1 (dv=102, sig_int=62.9, v/sig=1.17)",
         note="2nd-lowest-M* rotation-dominated lensed object at z>1.5; strong candidate"),
    dict(name="OLAS M1149-01802", z=2.16, mu=2.42, Mstar=10 ** 9.70, Mstar_tag="PUB",
         Mmol=None, Mmol_tag="UNMEAS", Rout=None, Rout_tag="UNMEAS",
         V=264 / 2, sig=84.2, vsig_pub=2.39, kin="Keck/OSIRIS AO Ha (RESOLVED, class 1)", tier=2,
         cite="Hirtenstein+2019 ApJ 880,54 Table 1 (dv=264, sig_int=84.2, v/sig=2.39)",
         note="best v/sig at z>2 in OLAS but log M*=9.70 -> too much mass for the cut"),
    dict(name="OLAS M2129-00478", z=1.67, mu=1.79, Mstar=10 ** 8.58, Mstar_tag="PUB",
         Mmol=None, Mmol_tag="UNMEAS", Rout=None, Rout_tag="UNMEAS",
         V=20 / 2, sig=37.4, vsig_pub=0.47, kin="Keck/OSIRIS AO Ha (RESOLVED, class 2 DISTURBED)", tier=2,
         cite="Hirtenstein+2019 ApJ 880,54 Table 1 (dv=20, sig_int=37.4, v/sig=0.47)",
         note="LOWEST sigma at z>1.5 (37.4) but v/sig=0.47 -> NOT rotating. The anti-"
              "correlation in one object: the coldest low-mass z~2 lensed systems are the "
              "ones that are not rotators."),
    dict(name="OLAS M2129-01665", z=1.56, mu=1.52, Mstar=10 ** 9.27, Mstar_tag="PUB",
         Mmol=None, Mmol_tag="UNMEAS", Rout=None, Rout_tag="UNMEAS",
         V=4 / 2, sig=40.5, vsig_pub=0.03, kin="Keck/OSIRIS AO Ha (RESOLVED, class 2 DISTURBED)", tier=2,
         cite="Hirtenstein+2019 ApJ 880,54 Table 1 (dv=4, sig_int=40.5, v/sig=0.03)",
         note="essentially zero shear -> unusable as a rotator"),
    dict(name="OLAS M2129-01833", z=2.29, mu=1.56, Mstar=10 ** 9.66, Mstar_tag="PUB",
         Mmol=None, Mmol_tag="UNMEAS", Rout=None, Rout_tag="UNMEAS",
         V=158 / 2, sig=104.5, vsig_pub=1.01, kin="Keck/OSIRIS AO Ha (RESOLVED, class 2)", tier=2,
         cite="Hirtenstein+2019 ApJ 880,54 Table 1 (dv=158, sig_int=104.5, v/sig=1.01)",
         note="massive + hottest sigma in the sample"),
    #   Jones+2010 AO IFU lensed sample (MNRAS 404,1247): dynamical masses PUB, M* mostly not.
    dict(name="Cl 0024+1709 arc", z=1.680, mu=1.38, Mstar=None, Mstar_tag="UNMEAS",
         Mmol=None, Mmol_tag="UNMEAS", Rout=10.0, Rout_tag="PUB", V=69.0, sig=76.0,
         kin="Keck/OSIRIS AO Ha (RESOLVED)", tier=2, Mdyn=5.5e10,
         cite="Jones+2010 MNRAS 404,1247 Table 2 (D=20+/-2 kpc, Vmax sin i=69+/-5, "
              "sig=76+/-12, M_dyn=(55+/-10)e9)",
         note="*** THE BIG-RADIUS ROUTE: kinematics to R=10 kpc, the largest R in any lensed "
              "z>1.5 sample. R_req for a 2e10 M_bar is ~10 kpc -> this object sits AT the cut "
              "boundary by radius alone. But mu=1.38 (barely lensed) and sig>V."),
    dict(name="MACS J0744+3927 arc", z=2.209, mu=16.0, Mstar=None, Mstar_tag="UNMEAS",
         Mmol=None, Mmol_tag="UNMEAS", Rout=1.0, Rout_tag="PUB", V=129.0, sig=99.0,
         kin="Keck/OSIRIS AO Ha (RESOLVED)", tier=2, Mdyn=1.1e10,
         cite="Jones+2010 MNRAS 404,1247 Table 2 (D=2.0+/-0.3 kpc, Vmax sin i=129+/-12, "
              "sig=99+/-4, M_dyn=(11+/-2)e9)",
         note="compact (R=1 kpc) + massive -> g_bar VERY far above the cut"),
    dict(name="Cl 0949+5153 arc (merger)", z=2.394, mu=7.3, Mstar=None, Mstar_tag="UNMEAS",
         Mmol=None, Mmol_tag="UNMEAS", Rout=3.5, Rout_tag="PUB", V=None, sig=71.0,
         kin="Keck/OSIRIS AO Ha (RESOLVED, MERGER - two components)", tier=2, Mdyn=1.3e10,
         cite="Jones+2010 MNRAS 404,1247 Table 2 (D=7+/-1 kpc merging, sig_NE=71+/-2, "
              "sig_SW=57+/-2, M_dyn 13e9 / 7e9)",
         note="MERGER -> disqualified for a rotation-based a0 readout"),
    # -------------------------------------------------------------------------------------
    # TIER 3: z=1.5-2.5, LENSED, cold-gas mass EXISTS, resolved kinematics DO NOT.
    #   Dessauges-Zavadsky+2015 A&A 577,A50 (IRAM PdBI/30m CO; alpha_CO=4.36 Galactic)
    # -------------------------------------------------------------------------------------
    dict(name="A68-C0", z=1.958, mu=9.1, Mstar=1.28e9, Mstar_tag="PUB", Mmol=4.7e9,
         Mmol_tag="PUB", Rout=None, Rout_tag="UNMEAS", V=None, sig=None,
         kin="CO unresolved; no resolved RC published", tier=3,
         cite="Dessauges-Zavadsky+2015 A&A 577,A50 Table 1 (CO(2-1), f_gas=0.79)",
         note="gas mass IN HAND; needs the kinematics"),
    dict(name="A68-h7", z=2.145, mu=2.2, Mstar=6.44e9, Mstar_tag="PUB", Mmol=1.16e10,
         Mmol_tag="PUB", Rout=None, Rout_tag="UNMEAS", V=None, sig=None,
         kin="CO unresolved", tier=3,
         cite="Dessauges-Zavadsky+2015 A&A 577,A50 Table 1 (CO(3-2), f_gas=0.64)",
         note="too massive for the cut at any plausible radius"),
    dict(name="A68-HLS115", z=2.491, mu=5.3, Mstar=0.72e9, Mstar_tag="PUB", Mmol=2.8e9,
         Mmol_tag="PUB", Rout=None, Rout_tag="UNMEAS", V=None, sig=None,
         kin="CO unresolved", tier=3,
         cite="Dessauges-Zavadsky+2015 A&A 577,A50 Table 1 (CO(2-1), f_gas=0.80)",
         note="*** LOWEST M* with a REAL CO gas mass at z>1.5 (7.2e8). Best TIER-3 candidate: "
              "gas mass PUB, only the kinematics missing."),
    dict(name="A2218-Mult", z=1.658, mu=33.8, Mstar=1.82e9, Mstar_tag="PUB", Mmol=1.9e9,
         Mmol_tag="PUB-UPPERLIM", Rout=None, Rout_tag="UNMEAS", V=None, sig=None,
         kin="CO NON-detection", tier=3,
         cite="Dessauges-Zavadsky+2015 A&A 577,A50 Table 1 (CO non-detection, M_mol<1.9e9, "
              "f_gas<0.51)",
         note="mu=33.8 is the largest magnification of any gas-constrained z~1.5-2.5 target"),
    dict(name="SL2S 0217 (SL2S J021737-051329)", z=1.844, mu=17.0, Mstar=1.0e9,
         Mstar_tag="PUB-UPPERLIM", Mmol=3.0e8, Mmol_tag="PUB-TENTATIVE",
         Rout=None, Rout_tag="UNMEAS", V=None, sig=None,
         kin="NO resolved kinematics (sub-kpc Lya imaging only)", tier=3,
         cite="Berg+2018 ApJ 859,164 (M*<1e9, Z~1/20 Zsun, mu~17, 25-arcsec arc); "
              "Vanzella-class EELG; ALMA [CII] 3-4sigma TENTATIVE + CO(2-1) NON-detection, "
              "M_gas ~ few e8 (arXiv:2101.00841 = ApJ 2021); Lya imaging ApJ 2019 "
              "(10.3847/1538-4357/ab3daf)",
         note="*** THE LOWEST-MASS LENSED z~2 GALAXY WITH ANY GAS CONSTRAINT AT ALL. But: "
              "[CII] is 30x FAINTER than the local dwarf [CII]-SFR relation at Z~0.05 Zsun, "
              "so the [CII]->M_gas conversion is BROKEN here. Gas mass is NOT reliable."),
    # -------------------------------------------------------------------------------------
    # TIER 4: extension rows just outside 1.5-2.5, carried because they set the achievable
    #         benchmarks (best V/sigma; the big-disc route; the cold-tracer control).
    # -------------------------------------------------------------------------------------
    dict(name="A1689B11", z=2.54, mu=7.2, Mstar=10 ** 9.8, Mstar_tag="PUB", Mmol=None,
         Mmol_tag="UNMEAS", Rout=3.9, Rout_tag="PUB", V=200.0, sig=23.0, vsig_pub=11.0,
         kin="Gemini/NIFS AO Ha (RESOLVED, COOL THIN disc)", tier=4,
         cite="Yuan+2017 ApJ 850,61 (arXiv:1710.11130 / 10.3847/1538-4357/aa951d): "
              "mu=7.2+/-0.8, log M*=9.8+/-0.3, V_c=200+/-12 km/s, turnover R=1.7+/-0.1 kpc, "
              "sigma_mean=23+/-4 and sigma_outer=15+/-2 km/s, V/sigma ~ 9-13, "
              "r_s=1.3+/-0.4 kpc, r_1/2=2.6+/-0.7 kpc, SFR=22+/-2",
         note="*** THE DECISIVE COUNTERWEIGHT ON PRESSURE SUPPORT, and it is in WARM IONIZED "
              "GAS (Ha, AO): sigma_outer = 15+/-2 km/s and V/sigma ~ 9-13 at z=2.54. So a "
              "50-100 km/s dispersion is NOT an inevitable property of z~2 kinematics -- it "
              "is partly beam-smearing + seeing + tracer. But log M*=9.8 with r_1/2=2.6 kpc "
              "puts it far ABOVE the cut: this object is cold BECAUSE it is dense. R_out "
              "taken as 3 r_s = 3.9 kpc (the RC turnover is at 1.7 kpc)."),
    dict(name="DSFG850.95", z=1.555, mu=1.0, Mstar=None, Mstar_tag="UNMEAS", Mmol=None,
         Mmol_tag="UNMEAS", Rout=14.0, Rout_tag="PUB", V=285.0, sig=48.0,
         kin="Keck/MOSFIRE (RESOLVED, FLAT outer RC 6-14 kpc)", tier=4, Mdyn=2.6e11,
         cite="Drew+2018 ApJ 869,58 (arXiv:1811.01958): V_flat=285+/-12, sig=48+/-4, flat "
              "between 6-14 kpc, f_DM=0.44+/-0.08 at the H-band half-light radius",
         note="UNLENSED. The BIG-RADIUS route in its purest form: R_out=14 kpc is the largest "
              "at z~1.5-2.5 anywhere. Massive, so still above the cut -- but it shows the "
              "radius lever is real without lensing."),
    dict(name="zC-400569 (cold-tracer control)", z=2.24, mu=1.0, Mstar=7.8e10,
         Mstar_tag="PUB", Mmol=None, Mmol_tag="UNMEAS", Rout=8.0, Rout_tag="PUB",
         V=300.0, sig=15.0, kin="ALMA CO (RESOLVED, flat to ~8 kpc)", tier=4,
         cite="Lelli+2023 A&A 672,A106 (aa45105-22): sigma_CO <~15 km/s, V/sigma >~17-22, "
              "systematically BELOW ionized-gas IFU dispersions",
         note="*** THE PRESSURE-SUPPORT EXISTENCE PROOF: cold tracers at cosmic noon give "
              "sigma <~15 km/s, not the 50-100 km/s of warm ionized gas. Massive and unlensed, "
              "so useless for the cut -- but it is the decisive methodological benchmark."),
    dict(name="Big Wheel (reference, in compilation)", z=3.245, mu=1.0, Mstar=3.7e11,
         Mstar_tag="PUB", Mmol=None, Mmol_tag="UNMEAS", Rout=9.6, Rout_tag="PUB",
         V=None, sig=None, kin="JWST NIRCam+spectroscopy (RESOLVED)", tier=4,
         cite="Nature Astronomy s41550-025-02500-2 (arXiv:2409.17956): r_1/2=9.6 kpc, "
              "M*=3.7e11, rotation consistent with the LOCAL Tully-Fisher relation",
         note="already carried in the committed compilation as a0_eff/a0(0)~1.0-1.3 +/-0.22 dex; "
              "listed here only to show the big-radius route at z>3"),
]

# ------------------------------------------------------------------------------- sample rows
SAMPLE_POOLS = [
    dict(name="KLASS (KMOS Lens-Amplified Spectroscopic Survey)", N=52, z="0.6-2.3",
         logM="8.1-11 (median 9.5)", mu="~2",
         cite="Girard+2020 MNRAS 497,173 (arXiv:2006.14633); first results Mason+2017 "
              "ApJ 838,14",
         status="44/52 resolved kinematics; median v_rot/sigma0 ~ 2.5; NO gas masses; "
                "KMOS SEEING-LIMITED (~0.6-0.7 arcsec ~ 5-6 kpc at z=2) -> outer radii and "
                "beam smearing are the limitation, not sample size",
         verdict="LARGEST existing lensed low-mass cosmic-noon kinematic pool; the z>1.5 "
                 "low-mass tail is the natural parent catalogue for a JWST follow-up"),
    dict(name="OLAS (OSIRIS Lens-Amplified Survey)", N=17, z="1.2-2.3", logM="8.0-9.8",
         mu="1.5-20.2",
         cite="Hirtenstein+2019 ApJ 880,54 (arXiv:1811.11768)",
         status="AO-assisted (good resolution); 8 objects at z=1.5-2.3 tabulated above; "
                "~9/16 rotation-dominated; NO gas masses; NO published source-plane radii",
         verdict="the ONLY AO-resolution lensed sample that reaches log M* ~ 8 at z~2"),
    dict(name="MUSE Lensing Cluster Survey / MUSE-DARK II", N=95, z="0.56-1.37",
         logM="8.1-10.3", mu="1.4-12.4",
         cite="Jeanneau+2026 A&A (arXiv:2603.28856), lensing-aware GalPaK3D forward modelling",
         status="EXACTLY the right object class (lensed, low-mass, 3D lensing-aware modelling) "
                "but the REDSHIFT CEILING IS HARD: MUSE's 4750-9350 A window puts [OII]3727 "
                "out of range beyond z~1.5, so this sample CANNOT be pushed to z~2",
         verdict="the method to copy; the wrong instrument for z~2 -> JWST/NIRSpec required"),
    dict(name="SGAS lensed arcs with ALMA cold gas", N=12, z="1.917-3.625",
         logM="<10.5", mu="~2.8-5.1",
         cite="Solimano+2024 A&A (aa51892-24) 'Molecular gas budget of strongly magnified "
              "low-mass star-forming galaxies at cosmic noon'; + Solimano+2021",
         status="only 3/12 CO DETECTIONS (J0033 z=1.917, J0108 z=2.514, J1050A z=3.625); "
                "the rest are UPPER LIMITS; no resolved kinematics reported",
         verdict="*** THE HARD NUMBER ON GAS MASSES: a dedicated ALMA program on magnified "
                 "low-mass cosmic-noon arcs detects CO in 25% of targets. This is why g_bar "
                 "is not computable a priori."),
    dict(name="LEGGOS (JWST lensed clumps survey)", N="ongoing", z="~2-4",
         logM="n/a", mu="~30 (SGAS J1110+6459 arc)",
         cite="LEGGOS II, arXiv:2606.20804 (SGAS J111020.0+645950.8 at z=2.481, JWST "
              "NIRCam + NIRSpec + archival HST, ~30x total magnification); source "
              "reconstruction Johnson+2017 ApJ 843,78 and ApJL 843,L21",
         status="JWST-era lensed z~2.5 target with a modern lens model and NIRSpec data; "
                "whether the NIRSpec mode delivers a SOURCE-PLANE ROTATION CURVE (IFU) vs "
                "clump spectroscopy (MSA) is a CANDIDATE-TO-CHECK, not asserted here",
         verdict="highest-priority archival check (hands off to D-2)"),
    dict(name="TEMPLATES (JWST ERS 1355)", N=4, z="1.33-4.22", logM="n/a", mu="~10-30",
         cite="JWST ERS program 1355 (stsci.edu/jwst/phase2-public/1355.pdf): NIRSpec + MIRI "
              "IFU of 4 lensed galaxies at 1<z<4 -- SGAS J1723+3411 (z=1.33), "
              "SGAS J1226+2152 (z=2.92), SPT0418-47 (z=4.22), SPT2147-50 (z=3.76)",
         status="REAL NIRSpec IFU data on lensed arcs exists, but the two z-bracketing "
                "targets are z=1.33 and z=2.92 -- NEITHER lands in 1.5-2.5 -- and all four "
                "are luminous/massive, not deep-MOND candidates",
         verdict="proves the OBSERVING MODE works on lensed arcs; provides no cut-passing target"),
]

# ==========================================================================================
# S4 -- COMPUTE g_bar/a0 THREE WAYS PER OBJECT AND AUDIT COMPUTABILITY
# ==========================================================================================
print("\n" + BAR)
print("S3/S4 -- THE TARGET TABLE: g_bar/a0 where it is COMPUTABLE, and the audit where it is not")
print(BAR)


def evaluate(o):
    """Return (mode, gbar_pub, gbar_lo, gbar_hi, Mbar_pub, Rreq_pub) for one object.
    mode: 'PUB'      both M_bar and R_out published  -> a REAL g_bar/a0
          'BRACKET'  M* published, gas and/or R bracketed -> an INTERVAL, never a pass
          'NONE'     not even M* published per-object -> NOT COMPUTABLE
    """
    z, Ms, Mm, R = o["z"], o.get("Mstar"), o.get("Mmol"), o.get("Rout")
    if Ms is None:
        # dynamical-mass-only rows: we can still bound g_bar from BELOW using M_bar<=M_dyn,
        # which is the ONLY honest statement (baryons cannot exceed the dynamical mass).
        if o.get("Mdyn") and R:
            gb_hi = float(gbar_over_a0(o["Mdyn"], R))
            return "NONE", None, 0.0, gb_hi, None, None
        return "NONE", None, None, None, None, None
    logMs = float(np.log10(Ms))
    # ---- baryonic mass
    if Mm is not None and o.get("Mmol_tag") == "PUB-UPPERLIM":
        # an UPPER LIMIT on M_mol: the honest lower corner sets the gas to ZERO, the upper
        # corner keeps the limit + an equal HI allowance.  Never treated as a detection.
        Mbar_pub = None
        Mbar_lo, Mbar_hi = Ms, Ms + 2.0 * Mm
        gas_known = False
    elif Mm is not None:
        Mbar_pub = Ms + Mm
        Mbar_lo, Mbar_hi = Ms + Mm, Ms + 2.0 * Mm       # HI interval [0, M_mol]
        gas_known = True
    else:
        mm = Ms * float(mu_mol_tacconi(z, logMs))       # SCALED
        Mbar_pub = None
        Mbar_lo, Mbar_hi = Ms + 0.5 * mm, Ms + 2.0 * mm  # gas scatter ~0.3 dex + HI interval
        gas_known = False
    # ---- radius
    if R is not None:
        R_lo = R_hi = R
        rad_known = True
    else:
        re = float(re_vdw14_kpc(z, logMs))
        R_lo, R_hi = 2.0 * re, 3.0 * re                  # SCALED
        rad_known = False
    # optimistic corner = lowest mass, largest radius ; pessimistic = highest mass, smallest R
    gb_lo = float(gbar_over_a0(Mbar_lo, R_hi))
    gb_hi = float(gbar_over_a0(Mbar_hi, R_lo))
    if gas_known and rad_known:
        return ("PUB", float(gbar_over_a0(Mbar_pub, R)), gb_lo, gb_hi, Mbar_pub,
                float(R_required_kpc(Mbar_pub)))
    Rreq = float(R_required_kpc(0.5 * (Mbar_lo + Mbar_hi)))
    return "BRACKET", None, gb_lo, gb_hi, 0.5 * (Mbar_lo + Mbar_hi), Rreq


rows = []
for o in T:
    mode, gpub, glo, ghi, Mbar, Rreq = evaluate(o)
    raw = (o["V"] / o["sig"]) if (o.get("V") and o.get("sig")) else None
    gmid = float(np.sqrt(glo * ghi)) if (glo and ghi) else None
    rows.append(dict(o, mode=mode, gpub=gpub, glo=glo, ghi=ghi, gmid=gmid, Mbar=Mbar,
                     Rreq=Rreq, vsig_raw=raw, vsig=o.get("vsig_pub")))

hdr = (f"  {'object':34} {'tr':>3} {'z':>5} {'mu':>6} {'logM*':>7} {'M_gas':>10} "
       f"{'R_out':>6} {'v/s pub':>8} {'g_bar/a0  [lo, MID, hi]':>30} {'R_req':>7}")
print(hdr)
print("  " + "-" * (len(hdr) - 2))
for r in rows:
    lm = f"{np.log10(r['Mstar']):.2f}" if r.get("Mstar") else "--"
    if r.get("Mstar_tag") == "PUB-UPPERLIM":
        lm = "<" + lm
    mg = ("%.1e" % r["Mmol"]) if r.get("Mmol") else "--"
    if r.get("Mmol_tag") == "PUB-UPPERLIM":
        mg = "<" + mg
    elif r.get("Mmol_tag") == "PUB-TENTATIVE":
        mg = "~" + mg
    ro = f"{r['Rout']:.1f}" if r.get("Rout") else "--"
    vs = f"{r['vsig']:.2f}" if r.get("vsig") else "--"
    if r["mode"] == "PUB":
        g = f"{r['gpub']:.2f}  ** PUB **"
    elif r["mode"] == "BRACKET":
        g = f"[{r['glo']:.2f}, {r['gmid']:.2f}, {r['ghi']:.2f}]"
    elif r["glo"] is not None:
        g = f"< {r['ghi']:.2f}  (M_bar<=M_dyn)"
    else:
        g = "NOT COMPUTABLE"
    rq = f"{r['Rreq']:.2f}" if r.get("Rreq") else "--"
    print(f"  {r['name'][:34]:34} {r['tier']:>3} {r['z']:>5.2f} {r['mu']:>6.1f} {lm:>7} "
          f"{mg:>10} {ro:>6} {vs:>8} {g:>30} {rq:>7}")
print("  (g_bar/a0 on the CANONICAL footing; R_out and R_req in kpc, source plane.)")
print("  ** PUB ** = both M_bar and R_out published -> a REAL g_bar/a0.  [lo, MID, hi] =")
print("  bracket from cited scaling relations (Tacconi+2018 gas / van der Wel+2014 size);")
print("  MID is the geometric mean = the CENTRAL estimate, and it is the honest headline.")
print("  '<' = published upper limit;  '~' = tentative (<5 sigma) detection.")
print("  v/s pub = the PUBLISHED v/sigma.  (This file also computes a raw Delta_v/(2 sigma_int)")
print("  ratio which differs from the published v/sigma -- different inclination/dispersion")
print("  conventions.  The PUBLISHED value is the one used for every rotation test below.)")
print("  APPROXIMATION, stated with its sign: g_bar = G M_bar/R^2 is the spherical-equivalent")
print("  form.  For a thin exponential disc the in-plane radial force at 2-3 r_e is HIGHER")
print("  than this by ~10-25%, so this formula makes objects look slightly MORE deep-MOND")
print("  than they are -- i.e. it errs toward finding targets, not toward a desert.")

# ==========================================================================================
# S5 -- THE COUNT: how many plausibly meet g_bar < 0.3 a0?
# ==========================================================================================
print("\n" + BAR)
print("S5 -- THE COUNT (the answer to 'how many plausibly meet the deep-MOND cut?')")
print(BAR)
inwin = [r for r in rows if 1.5 <= r["z"] <= 2.5]
confirmed = [r for r in inwin if r["mode"] == "PUB" and r["gpub"] < CUT]
pub_fail = [r for r in inwin if r["mode"] == "PUB" and r["gpub"] >= CUT]
central = [r for r in inwin if r["mode"] == "BRACKET" and r["gmid"] < CUT]
plausible = [r for r in inwin if r["mode"] == "BRACKET" and r["glo"] < CUT]
plaus_rot = [r for r in plausible if r.get("vsig") and r["vsig"] >= 1.0]
cent_rot = [r for r in central if r.get("vsig") and r["vsig"] >= 1.0]
excluded = [r for r in inwin if r["mode"] == "BRACKET" and r["glo"] >= CUT]
noncomp = [r for r in inwin if r["mode"] == "NONE"]


def vs_str(r):
    return f"{r['vsig']:.2f}" if r.get("vsig") else "n/a"


print(f"  objects in the z=1.5-2.5 window in this table:              {len(inwin):3d}")
print(f"  TIER-0  CONFIRMED pass on PUBLISHED data alone:            {len(confirmed):3d}   "
      f"{[r['name'] for r in confirmed]}")
print(f"  TIER-0  CONFIRMED FAIL on published data:                  {len(pub_fail):3d}   "
      f"{[r['name'] for r in pub_fail]}")
print(f"  TIER-1  CENTRAL estimate passes (bracket MIDpoint < 0.3):  {len(central):3d}"
      f"   <-- the honest short list")
for r in central:
    print(f"       - {r['name']:32} z={r['z']:.2f} mu={r['mu']:.1f} "
          f"logM*={np.log10(r['Mstar']):.2f} g_bar/a0 mid={r['gmid']:.2f} "
          f"[{r['glo']:.2f},{r['ghi']:.2f}] v/s={vs_str(r)} R_req={r['Rreq']:.2f} kpc")
print(f"          of those ALSO rotation-dominated (published v/s>=1): {len(cent_rot):3d}   "
      f"{[r['name'] for r in cent_rot]}")
print(f"  TIER-2  pass only at the OPTIMISTIC bracket corner:        {len(plausible):3d}")
for r in plausible:
    print(f"       - {r['name']:32} z={r['z']:.2f} mu={r['mu']:.1f} "
          f"logM*={np.log10(r['Mstar']):.2f} g_bar/a0 [{r['glo']:.2f},{r['gmid']:.2f},"
          f"{r['ghi']:.2f}] v/s={vs_str(r)} R_req={r['Rreq']:.2f} kpc")
print(f"          of those ALSO rotation-dominated (published v/s>=1): {len(plaus_rot):3d}   "
      f"{[r['name'] for r in plaus_rot]}")
print(f"  TIER-3  bracket EXCLUDES the cut even optimistically:      {len(excluded):3d}   "
      f"{[r['name'] for r in excluded]}")
print(f"  TIER-X  g_bar/a0 NOT COMPUTABLE at all:                    {len(noncomp):3d}   "
      f"{[r['name'] for r in noncomp]}")

# the sharp statement about computability across the whole window
n_gas = sum(1 for r in inwin if r.get("Mmol") is not None)
n_rad = sum(1 for r in inwin if r.get("Rout") is not None)
n_both = sum(1 for r in inwin if r.get("Mmol") is not None and r.get("Rout") is not None)
n_kin = sum(1 for r in inwin if "RESOLVED" in r.get("kin", ""))
n_gas_and_kin = sum(1 for r in inwin
                    if r.get("Mmol") is not None and "RESOLVED" in r.get("kin", ""))
print(f"\n  COMPUTABILITY AUDIT over the {len(inwin)} in-window objects:")
print(f"    published cold-gas mass:                 {n_gas:3d}")
print(f"    published source-plane outer radius:      {n_rad:3d}")
print(f"    BOTH (=> g_bar/a0 computable):            {n_both:3d}")
print(f"    resolved kinematics of any kind:          {n_kin:3d}")
print(f"    gas-mass set INTERSECT kinematics set:    {n_gas_and_kin:3d}"
      f"   <-- the whole problem in one number")

# ---- the SUSPECTED anti-correlation, tested rather than asserted -------------------------
print("\n  IS 'low mass <=> not rotating' REAL AT z~2?  Spearman test on the ONE homogeneous")
print("  sample that can answer it (OLAS z>1.5, N=8, published v/sigma vs published log M*):")
olas = [r for r in rows if r["name"].startswith("OLAS")]
lm = np.array([np.log10(r["Mstar"]) for r in olas])
vv = np.array([r["vsig"] for r in olas])


def spearman(x, y):
    rx = np.argsort(np.argsort(x)) + 1.0
    ry = np.argsort(np.argsort(y)) + 1.0
    n = len(x)
    rho = float(np.corrcoef(rx, ry)[0, 1])
    t = rho * np.sqrt((n - 2) / max(1e-12, 1 - rho ** 2))
    # two-sided p from the t-approximation (n=8 -> 6 dof); crude but adequate and stated as such
    from math import erf
    p = 2 * (1 - 0.5 * (1 + erf(abs(t) / np.sqrt(2))))
    return rho, n, p


rho, n_sp, p_sp = spearman(lm, vv)
print(f"    Spearman rho(log M*, v/sigma) = {rho:+.3f}  (N={n_sp}, two-sided p ~ {p_sp:.2f},"
      f" normal-approx)")
print(f"    reading: the sign is POSITIVE (more massive -> better rotational support), which is")
print(f"    the direction that HURTS a deep-MOND-selected sample -- but with N={n_sp} and p~{p_sp:.2f}")
print("    this is a SUGGESTIVE TREND, NOT a measurement.  It must not be quoted as a")
print("    demonstrated anti-correlation, and it must not be dismissed either.  The two")
print("    lowest-M* OLAS rotators do carry v/sigma = 1.64 and 1.17 (i.e. barely rotating),")
print("    and A1689B11 (log M*=9.8, sigma_outer=15 km/s, v/sigma~9-13) is the counterexample")
print("    at the HIGH-mass end.  Both facts are on the table; D-3 owns the consequence.")

# ==========================================================================================
# S6 -- THE DILUTION LEVER THE DEEP-MOND CUT BUYS  (framework-derived, from the parent)
# ==========================================================================================
print("\n" + BAR)
print("S6 -- WHY THE CUT IS WORTH CHASING: the framework's OWN dilution lever L = 1/(1+2y)")
print(BAR)


def lever(y):
    return 1.0 / (1.0 + 2.0 * y)


print("  L = 1/(1+2y), y = g_bar/a0 -- derived in a0z_fork_likelihood_2026.py from the")
print("  framework's own kernel g_obs = sqrt(g_bar^2 + g_bar a0).  L=1 is the deep-MOND limit.")
print(f"    {'sample / regime':44} {'y':>6} {'L':>7} {'gain vs Ubler z=2.3':>21}")
REF = [("Ubler+2017 KMOS3D z=2.3 (massive HSB)", np.sqrt(2.0 * 6.0)),
       ("Amvrosiadis+2025 ALMA CO DSFGs z=2.4", np.sqrt(5.0 * 7.0)),
       ("Jeanneau+2026 MUSE-DARK II lensed z~0.9", np.sqrt(0.3 * 1.0)),
       ("Big Wheel z=3.25", np.sqrt(0.2 * 0.3)),
       ("*** THIS PROGRAM: g_bar = 0.3 a0 (cut edge)", 0.30),
       ("*** THIS PROGRAM: g_bar = 0.15 a0 (target)", 0.15),
       ("    (deeper still, g_bar = 0.05 a0)", 0.05)]
L_ubl = lever(np.sqrt(2.0 * 6.0))
for lab, y in REF:
    print(f"    {lab:44} {y:>6.3f} {lever(y):>7.3f} {lever(y)/L_ubl:>20.1f}x")
print(f"  => selecting g_bar<0.3a0 buys a {lever(0.3)/L_ubl:.1f}x lever gain at the CUT EDGE and"
      f" {lever(0.15)/L_ubl:.1f}x at g_bar=0.15a0,")
print(f"     rising to {lever(0.05)/L_ubl:.1f}x only if the sample is pushed to g_bar~0.05a0.")
print("     HONEST CORRECTION TO THE PREMISE: the gain is ~5-6x at the stated cut, NOT ~10x.")
print(f"     The ~{1.0/L_ubl:.0f}x figure is the y->0 IDEAL (L=1); a g_bar<0.3a0 sample gets"
      f" {lever(0.3)/L_ubl:.1f}x of it,")
print(f"     and {lever(0.3)/lever(np.sqrt(5.0*7.0)):.1f}x relative to the Amvrosiadis DSFG point (L=0.078).")
print("     Still a REAL, framework-derived gain and the entire reason this class matters.")
print("     It does NOT by itself defeat pressure support -- that is D-3's question, not this")
print("     file's, and nothing here should be read as answering it.")

# ==========================================================================================
# S7 -- OBSERVABILITY OF THE PLAUSIBLE CANDIDATES (angular scales, honest and checkable)
# ==========================================================================================
print("\n" + BAR)
print("S7 -- OBSERVABILITY: does R_req fit inside a JWST/NIRSpec-IFU pointing?")
print(BAR)
# flat LCDM Planck-2018 angular scale, computed here (no external tables)
OM, OL, H0 = 0.3150, 0.6850, 67.36
C_KMS = 299792.458


def kpc_per_arcsec(z, n=20000):
    zz = np.linspace(0.0, z, n)
    Ez = np.sqrt(OM * (1 + zz) ** 3 + OL)
    DC = (C_KMS / H0) * np.trapezoid(1.0 / Ez, zz) if hasattr(np, "trapezoid") else \
         (C_KMS / H0) * np.trapz(1.0 / Ez, zz)          # Mpc, comoving
    DA = DC / (1.0 + z)                                  # Mpc, angular diameter
    return DA * 1000.0 * (np.pi / 180.0 / 3600.0)        # kpc per arcsec


print(f"  flat LCDM (Om={OM}, H0={H0}): scale = "
      f"{kpc_per_arcsec(2.0):.2f} kpc/arcsec at z=2.0, "
      f"{kpc_per_arcsec(1.7):.2f} at z=1.7, {kpc_per_arcsec(2.5):.2f} at z=2.5.")
print("  NIRSpec IFU: 3.0x3.0 arcsec FOV, 0.1 arcsec spaxels, PSF FWHM ~0.10-0.17 arcsec")
print("  over 1.7-5 um (Halpha lands at 2.0 um at z=2.0 -> G235H/G235M).")
print(f"  {'candidate':32} {'z':>5} {'mu':>5} {'R_req[kpc]':>10} {'R_req src[\"]':>12} "
      f"{'R_req img[\"] (~mu_t=sqrt(mu))':>29} {'PSF-elements across':>19}")
for r in plausible + [x for x in inwin if x["mode"] == "BRACKET" and x not in plausible][:3]:
    kpa = kpc_per_arcsec(r["z"])
    th_src = r["Rreq"] / kpa
    mu_t = np.sqrt(max(r["mu"], 1.0))                    # conservative: tangential ~ sqrt(mu)
    th_img = th_src * mu_t
    n_psf = 2 * th_img / 0.14
    print(f"  {r['name'][:32]:32} {r['z']:>5.2f} {r['mu']:>5.1f} {r['Rreq']:>10.2f} "
          f"{th_src:>12.3f} {th_img:>29.3f} {n_psf:>19.1f}")
print("  => the ANGULAR requirement is comfortably met: a magnified low-mass rotator needs")
print("     R_req ~ 2-4 kpc of source-plane coverage, which is 0.3-0.5 arcsec unlensed and")
print("     ~1-2 arcsec once tangentially stretched -- tens of PSF elements inside a single")
print("     NIRSpec IFU pointing.  The blocker is NOT angular resolution or FOV.  The blockers")
print("     are (i) the missing GAS MASS and (ii) the surface-brightness depth needed to")
print("     reach R_req in Halpha, plus (iii) pressure support, which is D-3's call.")

# ==========================================================================================
# S8 -- SAMPLE POOLS (where an N=15-40 sample would actually come from)
# ==========================================================================================
print("\n" + BAR)
print("S8 -- PARENT POOLS for an N=15-40 deep-MOND-selected sample (all REAL, all cited)")
print(BAR)
for p in SAMPLE_POOLS:
    print(f"\n  [{p['name']}]  N={p['N']}  z={p['z']}  logM*={p['logM']}  mu={p['mu']}")
    print(f"    cite   : {p['cite']}")
    print(f"    status : {p['status']}")
    print(f"    verdict: {p['verdict']}")

# ==========================================================================================
# S9 -- HONEST FINDINGS + PRE-REGISTRATION HOOKS (no GO/NO-GO here: that is D-3)
# ==========================================================================================
print("\n" + BAR)
print("S9 -- D-1 FINDINGS (target identification only; the GO/NO-GO belongs to D-3)")
print(BAR)
print(f"""  F1. NAMED CANDIDATES EXIST BUT THE LIST IS SHORT AND NONE IS CONFIRMED.  Scoring the
      z=1.5-2.5 window three ways:
        TIER-0 (published data alone):  {len(confirmed)} pass, {len(pub_fail)} fail.  ZERO confirmed deep-MOND objects.
        TIER-1 (bracket CENTRAL estimate < 0.3 a0):  {len(central)} objects -- A2218-Mult (z=1.658,
               mu=33.8, log M*=9.26, CO NON-detection so the gas is an upper limit) and
               SL2S 0217 (z=1.844, mu~17, log M*<9.0, Z~1/20 Zsun).  NEITHER HAS RESOLVED
               KINEMATICS AT ALL, so neither can currently yield an a0.
        TIER-2 (pass only at the optimistic bracket corner):  {len(plausible)} objects, of which {len(plaus_rot)} are
               also rotation-dominated on their PUBLISHED v/sigma: OLAS A370-03097 (z=1.55,
               v/s=2.09), OLAS M0717-02064 (z=2.07, mu=6.48, log M*=8.08, v/s=1.64),
               OLAS M0744-01203 (z=1.65, v/s=1.28), OLAS M1149-00683 (z=1.68, mu=4.05,
               log M*=8.14, v/s=1.17).
      THE OPERATIONAL SHORT LIST is therefore {len(plaus_rot)} named objects, all from OLAS
      (Hirtenstein+2019 ApJ 880,54), best two being M0717-02064 and M1149-00683 (the only
      log M* ~ 8 rotation-dominated LENSED objects known at z>1.5).  They need R_out ~ 2.5-2.6
      kpc, which is 0.29-0.31 arcsec in the source plane -- easy for NIRSpec IFU.  What they
      do NOT have is a gas mass, and that is decisive (F2).
      A 15-40 object cut-passing sample DOES NOT EXIST TODAY.  Said plainly.

  F2. g_bar/a0 IS NOT COMPUTABLE A PRIORI -- THIS IS THE KEY FINDING.  Across the
      {len(inwin)} in-window objects tabulated here, {n_gas} have a published cold-gas mass, {n_rad} have a
      published source-plane outer radius, and only {n_both} has BOTH.  The intersection of
      "has a cold-gas mass" and "has resolved kinematics" is exactly ONE object,
      MACS0451-arc (z=2.013) -- and it FAILS the cut at g_bar/a0 =
      {[r['gpub'] for r in rows if r['name'].startswith('MACS0451')][0]:.2f} and is dispersion-dominated (Vsin i/sigma = 0.48).
      CONSEQUENCE FOR THE DESIGN: the deep-MOND cut CANNOT be a selection criterion applied
      to an existing catalogue.  It must be an OUTCOME of stage 1 of a two-stage program:
        stage 1  measure M_gas (ALMA CO/[CII]) and R_out (JWST NIRSpec IFU) on a lensed
                 low-mass parent sample;  then
        stage 2  apply g_bar < 0.3 a0 and read a0 only on the survivors.
      Any design that assumes an N=15-40 cut-passing sample can be assembled from the
      archive is assuming something that does not exist.

  F3. THE CUT IS A SURFACE-DENSITY CUT, AND IT IS MAGNIFICATION-INVARIANT (S1, sympy).
      Sigma_enc < {sigma_cut(A0_CAN):.0f} Msun/pc^2 (canonical) / {sigma_cut(A0_ALT):.0f} Msun/pc^2 (alt footing).  Because both
      M_bar and source area scale as 1/mu, g_bar does not move with the lens model -- so the
      SELECTION is robust to the factor-2 mu disagreements that really occur in this
      literature.  The a0 VALUE is a different story: it is EXACTLY linear in mu, so
      sigma(mu)/mu enters sigma(a0)/a0 one-to-one.  At the 10-30% mu precision typical of
      published cluster-arc models that term alone sits at or above the {100*BAR_20TO1:.1f}% (20:1) bar.
      Target selection must therefore prefer multiply-imaged arcs with many constraints and
      avoid objects near critical curves.  Neither half of this is spun: selection is easier
      than the parents assumed, precision is harder.

  F4. TWO PHYSICAL ROUTES INTO THE CUT, AND THE SECOND IS UNDER-USED.  g_bar ~ M_bar/R^2, so
      LARGER R is worth more than smaller M.  Route A (lensed dwarfs, log M* ~ 8-8.6) needs
      R_out ~ 2-4 kpc.  Route B (big radius) is exemplified by REAL objects: Cl 0024+1709
      (z=1.68) has kinematics to R=10 kpc and DSFG850.95 (z=1.555) has a FLAT outer rotation
      curve from 6-14 kpc -- the largest radii measured at cosmic noon.  Neither passes the
      cut as published (both too massive), but the radius lever is demonstrated real, and a
      deliberately LARGE-RADIUS lensed target is a legitimate second search axis.

  F5. THE LOW-MASS/HOT-KINEMATICS TREND IS SUGGESTIVE, NOT SIGNIFICANT (Spearman rho
      = +0.24, N=8, p~0.55) -- it must be pre-registered as a RISK, not quoted as a
      measured anti-correlation.  Among the OLAS z>1.5
      objects, the two lowest-mass rotators carry sigma = 74.4 and 62.9 km/s against
      V ~ 71 and 51 km/s (V/sigma ~ 1.0-1.2), while the ONE object with a genuinely cold
      sigma = 37.4 km/s (M2129-00478) has V/sigma = 0.47 and is not a rotator at all.  The
      pattern -- coldest low-mass systems being the non-rotators -- is a DYNAMICAL
      property if real, not a resolution artifact, and lensing would not remove it.
      But N=8 cannot establish it, and this file does not claim it does.
      COUNTERWEIGHT, stated with equal force: A1689B11 (z=2.54, mu=7.2) is a "very cool and
      thin disc" with ordered rotation, and Lelli+2023's COLD (CO) tracers at cosmic noon
      give sigma <~ 15 km/s with V/sigma >~ 17-22 in massive discs -- i.e. a large part of
      the warm-ionized sigma ~ 50-100 km/s is TRACER-DEPENDENT, not intrinsic.  Whether the
      cold-tracer escape is available at log M* ~ 8 (where CO is undetected in 9/12 ALMA
      attempts on magnified low-mass arcs, Solimano+2024) is exactly D-3's question.
      D-1 hands over both the obstacle and the counterweight, and takes no GO/NO-GO position.

  F6. GAS-MASS COMPLETENESS IS SIGN-LOCKED TOWARD 'RISE'.  HI is unmeasurable at z~2, and
      omitting it under-estimates M_bar, which makes objects look MORE deep-MOND and makes
      a0 = V^4/(G M_bar) read HIGH.  If M_HI ~ M_mol at z=2 the readout is biased by
      +{np.log10(2.0):.2f} dex = +{100*(2.0**1-1):.0f}% in a0 -- larger than the {100*BAR_3SIG:.0f}% 3-sigma bar on its own, and in
      the direction that MIMICS the McCulloch/rising branch.  It does not help M-DEC and is
      not presented as if it did.  Any pre-registration must carry M_HI as an explicit
      nuisance with a prior, not as zero.

  F7. WHAT IS *NOT* HERE.  No z~1.5-2.5 object anywhere in the searched literature has a
      PUBLISHED g_bar/a0, and no paper reports a high-z galaxy explicitly in the deep-MOND
      regime.  MSA-3D (JWST/NIRSpec, z<1.7) reaches only log M* ~ 9.0 and is UNLENSED.
      MUSE-DARK II has the right object class but a hard z<~1.5 ceiling ([OII] leaves the
      MUSE window).  TEMPLATES has real NIRSpec-IFU lensed-arc data but at z=1.33 and
      z=2.92, bracketing the window without landing in it, on massive targets.
""")

print(BAR)
print("PRE-REGISTRATION HOOKS (D-1's binding contributions to the eventual frozen design)")
print(BAR)
print(f"""  P1. ESTIMATOR -- MEDIAN-LIKE, PRE-REGISTERED, NEVER GLS.  The committed
      estimator_bias_mocks.py verdict (prereg a0_line_estimator_bias_v1) measures
      gls_origin biased +10.34 pp (FAIL) and theilsen_pairwise +7.93 pp (FAIL), while the
      PRIMARY galaxy_median_then_median carries +0.31 pp (unique smallest RMS bias) and the
      surviving alternatives are median_a0pt (+0.84), trimmed_mean_a0pt (+1.13),
      ivw_median_a0pt (+0.66), galaxy_gls_then_median (+1.41), log_median_a0pt (+0.84).
      THIS DESIGN PRE-REGISTERS galaxy_median_then_median: per-object median of the
      point-wise a0-line readouts, then the median across objects, with a bootstrap CI.
      GLS IS FORBIDDEN.  A +10.3 pp estimator bias alone would blow the 10.9% 20:1 bar.
  P2. SELECTION IS ON g_bar, WHICH IS mu-INVARIANT (S1) -- freeze the cut at
      g_bar < 0.30 a0(0) on the CANONICAL footing and report the alt-footing cut
      (Sigma_enc < {sigma_cut(A0_CAN):.0f} vs {sigma_cut(A0_ALT):.0f} Msun/pc^2) alongside, since the threshold itself is 21%
      footing-dependent even though the DEC/RISE ratio being tested is not.
  P3. mu ENTERS sigma(a0) ONE-TO-ONE.  Require per-target sigma(mu)/mu, and prefer
      multiply-imaged systems; exclude anything whose image sits within the lens model's
      critical-curve uncertainty.  Do not average mu errors down across targets that share
      one cluster lens model -- that error is COHERENT within a cluster.
  P4. M_HI CARRIED AS A NUISANCE with a sign-locked prior M_HI in [0, M_mol] (F6), never
      set to zero, because zero biases a0 HIGH i.e. toward RISE.
  P5. TWO-STAGE PROGRAM (F2): the cut is an OUTCOME of stage 1, not an archival selection.
      Pre-register the stage-1 measurement thresholds (M_gas detection significance, R_out
      in kpc) BEFORE unblinding any a0.
""")

# ==========================================================================================
# MACHINE-READABLE OUTPUT
# ==========================================================================================
out = dict(
    role="D-1 target identification",
    footings=dict(canonical=A0_CAN, alt=A0_ALT, ratio_is_footing_independent=True),
    cut=dict(gbar_over_a0=CUT, sigma_enc_canon_msun_pc2=float(sigma_cut(A0_CAN)),
             sigma_enc_alt_msun_pc2=float(sigma_cut(A0_ALT))),
    bars=dict(three_sigma_frac=BAR_3SIG, twenty_to_one_frac=BAR_20TO1),
    lensing_algebra=dict(dln_gbar_dln_mu=0.0, dln_gobs_dln_mu=0.5, dln_a0_dln_mu=1.0),
    counts=dict(in_window=len(inwin), confirmed_pass=len(confirmed),
                confirmed_fail=len(pub_fail), plausible_pass=len(plausible),
                plausible_and_rotating=len(plaus_rot), bracket_excluded=len(excluded),
                not_computable=len(noncomp), with_gas=n_gas, with_radius=n_rad,
                with_both=n_both, with_resolved_kin=n_kin),
    estimator_prereg="galaxy_median_then_median (GLS FORBIDDEN: +10.34 pp bias)",
    targets=[{k: (float(v) if isinstance(v, (int, float, np.floating)) and v is not None
                  else v)
              for k, v in r.items() if k in ("name", "z", "mu", "Mstar", "Mmol", "Rout",
                                             "V", "sig", "tier", "mode", "gpub", "glo",
                                             "ghi", "Mbar", "Rreq", "vsig", "kin", "cite",
                                             "note")} for r in rows],
    pools=SAMPLE_POOLS,
)
with open(os.path.join(HERE, "highz_deepmond_target_list_2026_results.json"), "w") as f:
    json.dump(out, f, indent=2)
print(f"  wrote highz_deepmond_target_list_2026_results.json")

# ==========================================================================================
# SELF-CHECK
# ==========================================================================================
assert abs(sigma_cut(A0_CAN) - CUT * A0_CAN / (np.pi * G) * PC ** 2 / MSUN) < 1e-9
assert abs(float(R_required_kpc(1e9)) - 2.229) < 0.02, "R_req(1e9 Msun) ~ 2.23 kpc"
assert abs(float(gbar_over_a0(1e9, float(R_required_kpc(1e9)))) - CUT) < 1e-9, "cut round-trip"
assert len(confirmed) == 0, "no in-window object may be scored as a CONFIRMED pass"
assert n_both == 1, "exactly one in-window object has BOTH a gas mass and an outer radius"
_m = [r for r in rows if r["name"].startswith("MACS0451")][0]
assert _m["gpub"] > CUT, "MACS0451-arc must FAIL the cut on published numbers"
assert 4.5 < lever(0.30) / L_ubl < 5.5, "cut-edge lever gain vs Ubler z=2.3 must be ~5x (NOT ~10x)"
assert len(central) <= 3, "the central-estimate candidate list must be short by construction"
assert 0 < len(plaus_rot) <= 6, "the operational short list must be short"
assert sum(1 for r in central if "RESOLVED" in r.get("kin", "")) == 0, \
    "no central-estimate deep-MOND candidate currently has resolved kinematics"
assert abs(float(spearman(lm, vv)[2]) - p_sp) < 1e-12 and p_sp > 0.05, \
    "the low-mass/hot-kinematics trend must NOT be reported as significant"
print(f"\nSELF-CHECK OK: cut round-trips; CONFIRMED passes = {len(confirmed)} (zero, as found); "
      f"gas+radius overlap = {n_both}; MACS0451 g_bar/a0 = {_m['gpub']:.2f} > {CUT}; "
      f"lever gain {lever(0.30)/L_ubl:.1f}x.")
print("EXIT 0 (target list built + computability audited; NOT a verdict, NOT a GO/NO-GO).")
