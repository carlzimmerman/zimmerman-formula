#!/usr/bin/env python3
"""
L40 -- RIGIDITY: can any of L32's three surviving structures fix beta/sqrt(Z~) = 0.354 with NO freedom left?
============================================================================================================
WHERE THIS LANE STARTS.  L32 reduced the entire coefficient problem to one pure number.  Once a0 is promoted to a
dynamical order parameter X -- which L32's T5 shows is NECESSARY, because no curvature polynomial on de Sitter takes a
half-integer power of Lambda -- the FORM of a0 = kappa c sqrt(G rho_Lambda) becomes structural, the amplitude of X
cancels, and everything collapses to the canonically normalised coupling

        kappa = sqrt(2) beta / sqrt(Z~)      <=>      beta/sqrt(Z~) = kappa/sqrt(2) = 0.354      <=>      Z~/beta^2 = 8.

L32 then closed seven of ten enumerated structures with theorems T1-T6 and left THREE named survivors plus a sharpened
version of L3's membrane door.  This script tests the survivors on the only question that matters:

        DOES THE STRUCTURE FIX THE NUMBER, OR DOES IT MOVE THE FIT SOMEWHERE ELSE?

THE METHOD, and it matters more than the answer.  Derivation-first, never match-first.  For each structure: (1) enumerate
what it CAN produce, as a set, WITHOUT reference to 0.354; (2) count the free choices and the size of the candidate set;
(3) only then compare with the measurement.  A structure derives the number only if it has no free choices.  If you must
pick which group, which representation, which level, which condensate or which scheme, the structure has RELOCATED the fit
into a discrete or continuous choice -- and a choice with many options is still a fit.

THE BINDING GUARD.  L32's D3 found that 27 simple "principle-shaped" numbers already lie inside the measured 3-sigma band
(29 with the H0 convention).  LANDING IN THE BAND IS NOT EVIDENCE.  Only a derivation is evidence.  This script therefore
carries a CALIBRATED candidate-set counter: it must first reproduce L32's 27 (A3) before any structure's candidate set is
counted against it.  A structure whose own candidate set puts a comparable number of members in the band is excluded as a
DERIVATION even if one of its members lands exactly on 0.354 -- and two of them do, which is reported in full.

  A1  [CONTROL]      reproduce L32's reduction independently: kappa = sqrt(2) beta/sqrt(Z~) from kappa^2 = 2 beta^2/Z~,
                     and kappa = 1/2 <=> Z~/beta^2 = 8 exactly (sympy), with L3's b-correction Z/beta^2 = 8 - 2b;
  A2  [CONTROL]      reproduce the combined measurement kappa = 0.530 +/- 0.037 from 0.465 +/- 0.076 and 0.551 +/- 0.043;
  A3  [CONTROL]      the candidate-set counter reproduces L32's 27 in-band numbers -- calibration of the whole method;
  A4  [footing]      is the target integer 8 footing-robust?  (lambda = 2/kappa^2 on both a0 footings);
  A5  [ceiling]      how much evidence could a PERFECT integer-valued derivation ever supply, given the band's width?
  B1-B4 [S8]         horizon thermodynamics: what identity forces what, the 2 pi, the candidate set, the H0 degeneracy;
  C1-C4 [S9]         two-condensate dimensional transmutation: what cancels, what survives, and whether what survives is
                     a scheme-independent pure number (tested on the one strongly coupled sector whose condensates are MEASURED);
  D1-D4 [S10]        coset / nonlinear realisation: the zero-freedom form, the group-theoretic candidate set built from
                     standard Lie-algebra tables, and the exact hits;
  E1-E2 [membrane]   L3's surviving door sharpened: an a0-dependent membrane charge/tension, both branches, LOCK-vs-RIGIDITY;
  F1-F2 [verdict]    does ANY structure derive kappa; and is any zero-freedom form REFUTED rather than merely relocating.

FAIL marks a requirement a structure does not meet.  The expected honest outcome is that all three relocate; that outcome
CLOSES the coefficient problem in general form rather than for one action, which is why it is worth establishing hard.  A
structure with genuinely zero free choices that lands ELSEWHERE than 0.354 is a REFUTATION of that structure and is
reported as such.  NOTHING HERE DERIVES kappa, and kappa remains FITTED.  Both a0 footings on every dimensional number.
"""
import numpy as np, math, sys
import sympy as sp
from fractions import Fraction

FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

# ------------------------------------------------------------------ constants (L32's, independently restated) -------
G = 6.674e-11; C_LIGHT = 2.998e8; MPC = 3.0857e22
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
H0_PLANCK, H0_SH0ES, OMEGA_L = 67.4, 73.0, 0.685
KAPPA_MEAS = {"BTFR": (0.465, 0.076), "distance-free": (0.551, 0.043)}

def rho_Lambda(H0kms=H0_PLANCK, OL=OMEGA_L):
    H0 = H0kms*1e3/MPC
    return OL*3*H0**2/(8*math.pi*G)

RHO_L = rho_Lambda()
LAMBDA = 8*math.pi*G*RHO_L/C_LIGHT**2
L_DS = math.sqrt(3/LAMBDA)
CSQRT = C_LIGHT*math.sqrt(G*RHO_L)                       # c sqrt(G rho_Lambda) = 1.8725e-10 m/s^2
KAP_FOOT = {f: a/CSQRT for f, a in A0.items()}           # the framework's ADOPTED kappa on each a0 footing

print("=" * 126)
print("L40 -- RIGIDITY: can horizon thermodynamics, two-condensate transmutation or a coset fix beta/sqrt(Z~) = 0.354?")
print("=" * 126)
print(f"    Planck footing for the cosmology: H0 = {H0_PLANCK} km/s/Mpc, Omega_Lambda = {OMEGA_L}")
print(f"    c sqrt(G rho_Lambda) = {CSQRT:.4e} m/s^2;  L_dS = {L_DS:.4e} m = {L_DS/MPC:.0f} Mpc")
print(f"    ADOPTED kappa by a0 footing: " + ", ".join(f"{f} a0 = {a:.4e} -> kappa = {KAP_FOOT[f]:.4f}" for f, a in A0.items()))

# ====================================================================================================================
# SECTION A -- controls: the reduction, the measurement, and the CALIBRATION of the candidate-set counter
# ====================================================================================================================
print("\n" + "-" * 126)
print("SECTION A -- controls: reproduce L32's reduction, its measurement, and calibrate the candidate-set counter")
print("-" * 126)

# --- A1: the reduction, symbolically and independently ---------------------------------------------------------
Zt, beta_s, b_s, q_s, G_s, lam_s = sp.symbols('Ztilde beta b q G lambda', positive=True)
P_flux   = Zt*q_s**2/2                                    # the order parameter's own quadratic action (k04 / L3)
eps_flux = sp.simplify(q_s*sp.diff(P_flux, q_s) - P_flux) # Legendre (gravitating) energy = Z~ q^2/2
a0_flux  = beta_s*sp.sqrt(G_s)*q_s                        # a0 linear in the SAME order parameter (L32's N2)
kap2_sym = sp.simplify(a0_flux**2/(G_s*eps_flux))         # kappa^2 = a0^2/(G eps)
kap_sym  = sp.sqrt(kap2_sym)
q_cancels = (not kap2_sym.has(q_s)) and (not kap2_sym.has(G_s))
lam_at_half = sp.solve(sp.Eq(kap2_sym, sp.Rational(1, 4)), Zt)[0]/beta_s**2   # Z~/beta^2 at kappa = 1/2
canon = sp.simplify(kap_sym - sp.sqrt(2)*beta_s/sp.sqrt(Zt))
print(f"    A1: eps = q P_q - P = {eps_flux};  a0 = beta sqrt(G) q  =>  kappa^2 = a0^2/(G eps) = {kap2_sym}")
print(f"    A1: kappa - sqrt(2) beta/sqrt(Z~) = {canon} (identically zero);  the amplitude q and G BOTH cancel: {q_cancels}")
print(f"    A1: kappa = 1/2  <=>  Z~/beta^2 = {lam_at_half};  equivalently lambda = 2/kappa^2 and beta/sqrt(Z~) = kappa/sqrt(2)")
# L3's b-correction: the four-form's OWN stiffness Z vs the total Z~ = Z + 2 b beta^2
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
Delta_rar = lambda s: s/np.expm1(np.sqrt(s)) if s > 0 else 0.0
_o = minimize_scalar(lambda s: -Delta_rar(s), bounds=(0.5, 6), method='bounded')
I_RAR = 2*(_o.x*(-_o.fun) - quad(Delta_rar, 0, _o.x)[0])
B_REF = 2.0*I_RAR/(16*math.pi)                                # b = (2-K_B) I /(16 pi) at K_B = 0
print(f"    A1: L3's split Z~ = Z + 2 b beta^2 with b = {B_REF:.5f} (nu_RAR kernel, K_B = 0)  =>  Z/beta^2 = 8 - 2b = {8 - 2*B_REF:.4f}")
check("A1 [CONTROL] the reduction reproduces independently: kappa = sqrt(2) beta/sqrt(Z~) with the amplitude and G cancelling identically, and kappa = 1/2 <=> Z~/beta^2 = 8 exactly",
      q_cancels and canon == 0 and sp.simplify(lam_at_half - 8) == 0,
      f"kappa^2 = 2 beta^2/Z~; Z~/beta^2 = {lam_at_half} at kappa = 1/2; L3's four-form-only ratio Z/beta^2 = {8 - 2*B_REF:.4f}")

# --- A2: the measurement ---------------------------------------------------------------------------------------
w = {n: 1/e**2 for n, (m, e) in KAPPA_MEAS.items()}
KBAR = sum(w[n]*KAPPA_MEAS[n][0] for n in w)/sum(w.values())
SBAR = 1/math.sqrt(sum(w.values()))
dsep = KAPPA_MEAS["distance-free"][0] - KAPPA_MEAS["BTFR"][0]
sdsep = math.hypot(KAPPA_MEAS["BTFR"][1], KAPPA_MEAS["distance-free"][1])
SYS = abs(1 - H0_PLANCK/H0_SH0ES)/2                            # H0-convention half-range on kappa
TOT = math.hypot(SBAR/KBAR, SYS)                               # total fractional comparison uncertainty
BAND_STAT = (KBAR - 3*SBAR, KBAR + 3*SBAR)
BAND_TOT  = (KBAR*(1 - 3*TOT), KBAR*(1 + 3*TOT))
SIG_TOT = KBAR*TOT
print(f"    A2: combined kappa = {KBAR:.4f} +/- {SBAR:.4f} ({100*SBAR/KBAR:.1f}%); the two inputs are {abs(dsep)/sdsep:.2f} sigma apart")
print(f"    A2: H0 convention (Planck 67.4 -> SH0ES 73.0) moves kappa_meas by {100*(H0_PLANCK/H0_SH0ES - 1):+.1f}%, half-range {100*SYS:.1f}%")
print(f"    A2: total comparison uncertainty {100*TOT:.1f}% ({SIG_TOT:.4f} absolute); 3-sigma bands: statistical "
      f"[{BAND_STAT[0]:.3f}, {BAND_STAT[1]:.3f}], with convention [{BAND_TOT[0]:.3f}, {BAND_TOT[1]:.3f}]")
check("A2 [CONTROL] the combined measurement reproduces L32's kappa = 0.530 +/- 0.037 and its 8.0% total comparison uncertainty",
      abs(KBAR - 0.530) < 0.002 and abs(SBAR - 0.037) < 0.002 and abs(TOT - 0.080) < 0.003,
      f"{KBAR:.4f} +/- {SBAR:.4f}, total {100*TOT:.1f}%; nothing inside [{BAND_TOT[0]:.2f}, {BAND_TOT[1]:.2f}] is rejectable at 3 sigma")

# --- A3: CALIBRATION of the candidate-set counter (L32's D3 catalogue, reproduced verbatim) ---------------------
def catalogue():
    cands = {}
    for qd in range(2, 13):
        for p in range(1, qd):
            if math.gcd(p, qd) == 1: cands[f"{p}/{qd}"] = float(Fraction(p, qd))
    pi = math.pi; e = math.e
    named = {"1/(2pi) x sqrt(8pi/3)": math.sqrt(8*pi/3)/(2*pi), "1/pi": 1/pi, "2/pi": 2/pi, "pi/6": pi/6,
             "3/(2pi)": 3/(2*pi), "pi^2/16": pi**2/16, "1/sqrt(pi)": 1/math.sqrt(pi), "sqrt(3/(8pi))": math.sqrt(3/(8*pi)),
             "e/(2pi)": e/(2*pi), "1/sqrt(e)": 1/math.sqrt(e), "ln2": math.log(2), "1/sqrt(2pi)": 1/math.sqrt(2*pi),
             "1/sqrt(3)": 1/math.sqrt(3), "sqrt(2)/e": math.sqrt(2)/e, "1/phi": 2/(1 + math.sqrt(5)),
             "sqrt(2)-1": math.sqrt(2) - 1, "pi/(2e)": pi/(2*e), "3/(4+pi)": 3/(4 + pi), "sqrt(2/pi)/2": math.sqrt(2/pi)/2,
             "2/(pi+e)": 2/(pi + e), "1/(2 sqrt(2))": 1/(2*math.sqrt(2)), "sqrt(5)/4": math.sqrt(5)/4,
             "e/5": e/5, "pi/2 - 1": pi/2 - 1, "1/e": 1/e, "3/(2 pi) x sqrt(pi)": 3/(2*pi)*math.sqrt(pi)}
    cands.update(named)
    return cands

def count_in_band(values, lo, hi):
    """The calibrated counter.  values: dict name -> number (a structure's candidate SET).  Returns the in-band members."""
    return sorted([k for k, v in values.items() if lo <= v <= hi], key=lambda k: values[k])

CAT = catalogue()
CAT_IN_STAT = count_in_band(CAT, *BAND_STAT)
CAT_IN_TOT  = count_in_band(CAT, *BAND_TOT)
print(f"    A3: L32's catalogue of {len(CAT)} principle-shaped numbers; in the 3-sigma statistical band [{BAND_STAT[0]:.3f}, {BAND_STAT[1]:.3f}]: "
      f"{len(CAT_IN_STAT)}; with the H0 convention: {len(CAT_IN_TOT)}")
print(f"        " + ", ".join(f"{k} = {CAT[k]:.4f}" for k in CAT_IN_STAT[:10]) + " ...")
BASELINE = len(CAT_IN_STAT)
check("A3 [CONTROL] the candidate-set counter is CALIBRATED: it reproduces L32's finding of 27 simple numbers inside the 3-sigma statistical band (29 with the H0 convention)",
      len(CAT_IN_STAT) == 27 and len(CAT_IN_TOT) == 29,
      f"{len(CAT_IN_STAT)} / {len(CAT_IN_TOT)}.  BASELINE = {BASELINE}: any structure whose OWN candidate set puts a comparable number of "
      f"members in the band cannot be evidence for kappa = 1/2, however exactly one of them lands on 0.354")

# --- A4: is the target integer footing-robust? -----------------------------------------------------------------
LAM_FOOT = {f: 2/k**2 for f, k in KAP_FOOT.items()}
BN_FOOT  = {f: k/math.sqrt(2) for f, k in KAP_FOOT.items()}
for f in A0:
    print(f"    A4: {f:9s} kappa = {KAP_FOOT[f]:.4f}  =>  beta/sqrt(Z~) = kappa/sqrt(2) = {BN_FOOT[f]:.4f},  lambda = Z~/beta^2 = 2/kappa^2 = {LAM_FOOT[f]:.4f}")
int_dev = {f: abs(v - round(v)) for f, v in LAM_FOOT.items()}
print(f"    A4: distance to the nearest integer: canonical {int_dev['canonical']:.4f}, alt {int_dev['alt']:.4f} (the maximum possible is 0.5)")
check("A4 [footing] the target ratio lambda = Z~/beta^2 is an INTEGER on BOTH a0 footings, so an integer-valued principle could hit it without also selecting a footing",
      max(int_dev.values()) < 0.05,
      f"canonical gives lambda = {LAM_FOOT['canonical']:.3f} (the '8', {int_dev['canonical']:.4f} from an integer), the alt footing gives "
      f"{LAM_FOOT['alt']:.3f} -- {int_dev['alt']:.3f} from the nearest integer, i.e. as far from any integer as it is possible to be.  "
      f"'8' is a CANONICAL-FOOTING statement, exactly the guard L3's Q8 and L32's A2 raise; an integer principle would have to fix the footing too")

# --- A5: the evidence ceiling on ANY integer-valued derivation --------------------------------------------------
lam_lo, lam_hi = 2/BAND_TOT[1]**2, 2/BAND_TOT[0]**2
ints_in = [m for m in range(1, 200) if lam_lo <= m <= lam_hi]
PRIOR_MAX = 32                                            # "small integer" prior: lambda in {1..32}
p_hit = len(ints_in)/PRIOR_MAX
bits = -math.log2(p_hit)
sig_equiv = math.sqrt(2*math.log(1/p_hit))
print(f"    A5: the 3-sigma band on kappa maps to lambda = 2/kappa^2 in [{lam_lo:.2f}, {lam_hi:.2f}], which contains the integers {ints_in}")
print(f"    A5: with a uniform prior over 'small integers' lambda in 1..{PRIOR_MAX}, a correct integer prediction has chance {p_hit:.2f} of landing in the band")
print(f"        =>  a PERFECT, zero-freedom integer derivation supplies at most {bits:.1f} bits = {sig_equiv:.1f} sigma-equivalent of evidence")
check("A5 [ceiling] the coefficient band is narrow enough that a perfect integer-valued derivation would be decisive (>= 3 sigma-equivalent) on the coefficient alone",
      sig_equiv >= 3.0,
      f"{len(ints_in)} integers lie in the band, so even a flawless derivation of lambda = 8 is worth {bits:.1f} bits = {sig_equiv:.1f} sigma. "
      f"This is an upper bound INDEPENDENT of the mechanism: it is why L32's N6 says the derivation, not the proximity, is the evidence, "
      f"and why the registered a0(z) measurement -- not kappa -- is the discriminating observable")

# ====================================================================================================================
# SECTION B -- S8: horizon thermodynamics.  Derivation or identification?
# ====================================================================================================================
print("\n" + "-" * 126)
print("SECTION B -- S8 horizon thermodynamics: kappa = 0.4607 <=> a0 = c^2/(2 pi L_dS).  What does thermodynamics FORCE?")
print("-" * 126)
# Everything in this sector is one dimensionless number zeta in a0 = zeta c^2/L_dS, because A2 of L32 already showed
# the relation IS a ratio of two lengths.  kappa = zeta / sqrt(3/8pi) = zeta sqrt(8pi/3).
ZFAC = math.sqrt(8*math.pi/3)                                  # kappa = ZFAC * zeta
zeta_of = lambda kap: kap/ZFAC
kappa_of = lambda z: z*ZFAC
ZETA_BAND = (zeta_of(BAND_TOT[0]), zeta_of(BAND_TOT[1]))
print(f"    B0: a0 = zeta c^2/L_dS with kappa = zeta sqrt(8 pi/3) = {ZFAC:.4f} zeta; the measured band maps to "
      f"zeta in [{ZETA_BAND[0]:.4f}, {ZETA_BAND[1]:.4f}] (measured zeta = {zeta_of(KBAR):.4f})")

# --- B1: THE identity.  Unruh temperature of a0 = Gibbons-Hawking temperature of de Sitter -----------------------
# T_U(a) = hbar a/(2 pi c k_B);  T_dS = hbar H_Lambda/(2 pi k_B) = hbar c/(2 pi k_B L_dS).
# T_U(a0) = T_dS  =>  a0 = c^2/L_dS  =>  zeta = 1.  The 2 pi's are IDENTICAL on both sides and CANCEL.
a_sym, LdS_sym, hbar_s, kB_s, c_sym = sp.symbols('a L_dS hbar k_B c', positive=True)
T_unruh = hbar_s*a_sym/(2*sp.pi*c_sym*kB_s)
T_dS    = hbar_s*c_sym/(2*sp.pi*kB_s*LdS_sym)
a_forced = sp.solve(sp.Eq(T_unruh, T_dS), a_sym)[0]
zeta_identity = sp.simplify(a_forced*LdS_sym/c_sym**2)
kap_identity = float(zeta_identity)*ZFAC
z_ident = abs(kap_identity - KBAR)/SIG_TOT
print(f"    B1: T_Unruh(a) = {T_unruh};  T_dS = {T_dS};  the 2 pi is the SAME factor on both sides and cancels")
print(f"    B1: T_Unruh(a0) = T_dS  =>  a0 = {a_forced}, i.e. zeta = {zeta_identity} EXACTLY  =>  kappa = sqrt(8 pi/3) = {kap_identity:.4f}")
print(f"    B1: that is a0 = c H_Lambda = {kappa_of(1.0)*CSQRT:.4e} m/s^2, a factor "
      f"{kappa_of(1.0)*CSQRT/A0['canonical']:.2f} (canonical) / {kappa_of(1.0)*CSQRT/A0['alt']:.2f} (alt) above the framework's a0")
check("B1 [S8, the identity] the ZERO-FREEDOM horizon-thermodynamic statement -- the acceleration whose Unruh temperature equals the de Sitter temperature -- agrees with the measured kappa",
      abs(kap_identity - KBAR) <= 3*SIG_TOT,
      f"it forces kappa = sqrt(8 pi/3) = {kap_identity:.4f}, which is {z_ident:.0f} sigma from {KBAR:.3f} and {100*(kap_identity/KBAR - 1):.0f}% high. "
      f"THIS IS A REFUTATION, not a relocation: the one form of the horizon route with no free factor is excluded. "
      f"(Milgrom 1999's zeta = 2 variant, a0 = 2 c H_Lambda, is already excluded at 15.6 sigma in the corpus.)")

# --- B2: is there any identity that forces the extra 1/(2 pi)? ---------------------------------------------------
K_2PI = math.sqrt(8*math.pi/3)/(2*math.pi)
T_ratio_needed = sp.simplify((T_unruh.subs(a_sym, c_sym**2/(2*sp.pi*LdS_sym)))/T_dS)
print(f"    B2: the candidate kappa = sqrt(8 pi/3)/(2 pi) = {K_2PI:.4f} is a0 = c^2/(2 pi L_dS) = c H_Lambda/(2 pi)")
print(f"    B2: in temperature terms that is T_Unruh(a0)/T_dS = {T_ratio_needed} -- NOT an equality of temperatures but a")
print(f"        temperature SUPPRESSED by 2 pi.  Enumerate the standard de Sitter horizon quantities and what each forces:")
HORIZON_ROUTES = {
    # (zeta, is it forced by an IDENTITY between two independently defined horizon quantities, or is a factor inserted?)
    "T_Unruh(a0) = T_dS  (Unruh = Gibbons-Hawking; the 2 pi's cancel)":                   (1.0, True),
    "a0 = de Sitter surface gravity kappa_sg = c^2/L_dS":                                 (1.0, True),
    "a0 = G E_BY/(c^2 L_dS^2) with Brown-York E_BY = c^4 L_dS/G  (L3 Q10)":               (1.0, True),
    "a0 = G M_hor/L_dS^2 with the Misner-Sharp mass M = c^2 L_dS/(2G)":                   (0.5, True),
    "a0 = 2 c H_Lambda  (Milgrom 1999 de Sitter-Unruh; excluded 15.6 sigma in-corpus)":   (2.0, False),
    "a0 = c^2/(2 pi L_dS)  [the S8 claim: T_Unruh(a0) = T_dS/(2 pi)]":                    (1/(2*math.pi), False),
    "a0 = c^2/(4 pi L_dS)  (an entropy-per-area 1/4 inserted as well)":                   (1/(4*math.pi), False),
    "a0 = 4 pi c^2/L_dS  (an area factor inserted)":                                      (4*math.pi, False),
}
for nm, (zv, forced) in sorted(HORIZON_ROUTES.items(), key=lambda kv: kv[1][0]):
    tag = "IN BAND" if ZETA_BAND[0] <= zv <= ZETA_BAND[1] else ""
    print(f"        zeta = {zv:8.4f} -> kappa = {kappa_of(zv):8.4f}  [{'identity' if forced else 'inserted'}]  {nm}   {tag}")
identity_forced = sorted({zv for nm, (zv, f_) in HORIZON_ROUTES.items() if f_})
ident_in_band = [zv for zv in identity_forced if ZETA_BAND[0] <= zv <= ZETA_BAND[1]]
check("B2 [S8, the 2 pi] some thermodynamic IDENTITY forces the extra factor 1/(2 pi), i.e. the 2 pi is derived rather than inserted",
      sp.simplify(T_ratio_needed - 1) == 0 or len(ident_in_band) > 0,
      f"it does not: a0 = c^2/(2 pi L_dS) requires T_Unruh(a0) = T_dS/(2 pi), which is not an identity but an assignment.  The 2 pi's of the "
      f"Unruh and Gibbons-Hawking formulae are the SAME 2 pi and CANCEL when the temperatures are equated.  Every identity-forced route in the "
      f"enumeration gives zeta in {identity_forced} -- {len(ident_in_band)} of them in the band -- and every route that reaches the band has a "
      f"factor put in by hand.  S8 is an IDENTIFICATION -- someone writing down a plausible relation and finding it works -- not a derivation "
      f"from field equations")

# --- B3: the horizon route's candidate set ----------------------------------------------------------------------
HZ_SET = {}
for p_ in range(1, 13):
    for qd_ in range(1, 13):
        if math.gcd(p_, qd_) == 1: HZ_SET[f"{p_}/{qd_}"] = p_/qd_
for nm, v in {"1/(2pi)": 1/(2*math.pi), "1/(4pi)": 1/(4*math.pi), "1/pi": 1/math.pi, "1/(pi^2)": 1/math.pi**2,
              "1/(8pi)": 1/(8*math.pi), "2/pi": 2/math.pi, "1/(2pi^2)": 1/(2*math.pi**2), "3/(8pi)": 3/(8*math.pi),
              "1/(3pi)": 1/(3*math.pi), "sqrt(3/(8pi))": math.sqrt(3/(8*math.pi)), "1/(2 sqrt(pi))": 1/(2*math.sqrt(math.pi)),
              "e/(4pi)": math.e/(4*math.pi), "ln2/(2pi)": math.log(2)/(2*math.pi)}.items():
    HZ_SET[nm] = v
HZ_IN = count_in_band(HZ_SET, *ZETA_BAND)
print(f"    B3: candidate set for the horizon prefactor zeta ({len(HZ_SET)} simple rationals and pi-forms of the kind a horizon argument produces):")
print(f"        {len(HZ_IN)} lie inside the measured band, including " + ", ".join(f"{k} = {HZ_SET[k]:.4f}" for k in HZ_IN[:8])
      + (" ..." if len(HZ_IN) > 8 else ""))
check("B3 [S8, rigidity] the horizon route's own candidate set for zeta singles out 1/(2 pi): at most one member lies inside the measured band",
      len(HZ_IN) <= 1,
      f"{len(HZ_IN)} members lie in the band (including 1/6 = {1/6:.4f}, Milgrom's original a0 ~ c H0/6).  ONE free choice -- the numerical "
      f"factor relating a0 to the horizon scale -- and it is not fixed by any identity, so the route fits it")

# --- B4: the H0-convention degeneracy (reproduces k03's P2 independently) ----------------------------------------
def a0_pred(kap, H0kms): return kap*C_LIGHT*math.sqrt(G*rho_Lambda(H0kms))
a_half_planck = a0_pred(0.5, H0_PLANCK); a_2pi_shoes = a0_pred(K_2PI, H0_SH0ES)
sep_kappa = abs(0.5/K_2PI - 1)
conv_units = sep_kappa/(2*SYS)                                 # the separation measured in H0-convention spans
print(f"    B4: a0(kappa = 1/2, Planck H0) = {a_half_planck:.4e};  a0(kappa = {K_2PI:.4f}, SH0ES H0) = {a_2pi_shoes:.4e}; "
      f"they differ by {100*abs(a_2pi_shoes/a_half_planck - 1):.2f}%")
print(f"    B4: 1/2 and the horizon value are {100*sep_kappa:.1f}% apart -- {conv_units:.2f} x the full Planck-to-SH0ES span ({100*2*SYS:.1f}%)")
check("B4 [S8, convention] the horizon coefficient is separated from 1/2 by more than the H0 convention can move it, so the two are distinguishable in principle",
      conv_units > 1.5,
      f"the separation is {conv_units:.2f} convention-spans: changing H0 from Planck to SH0ES converts one candidate into the other to "
      f"{100*abs(a_2pi_shoes/a_half_planck - 1):.1f}% in a0.  A coefficient that a change of cosmological convention absorbs carries "
      f"essentially no information -- k03's P2, reproduced here independently")

print(f"\n    S8 VERDICT: EXCLUDED as a derivation.  Free choices = 1 (the prefactor zeta).  Its ZERO-choice form -- the Unruh/"
      f"Gibbons-Hawking temperature equality -- is REFUTED at {z_ident:.0f} sigma (kappa = {kap_identity:.3f}).  Its in-band form requires "
      f"inserting 1/(2 pi)\n                by hand, has {len(HZ_IN)} in-band alternatives in its own candidate set, and is absorbed by the H0 convention.")

# ====================================================================================================================
# SECTION C -- S9: dimensional transmutation with two condensates in ONE strongly coupled sector
# ====================================================================================================================
print("\n" + "-" * 126)
print("SECTION C -- S9 two-condensate dimensional transmutation: what cancels, what survives, and is what survives rigid?")
print("-" * 126)
# Setup (natural units hbar = c = 1).  One strongly coupled sector, one gauge coupling g(mu), one dynamical scale
# Lambda_c = mu exp(-8 pi^2/(b0 g^2(mu))).  N2 needs an order parameter X of mass dimension 2 with rho_vac ~ X^2 and
# a0 ~ X.  Dimensional analysis then FORCES  X = c_X Lambda_c^2  and  rho_vac = c_2 Lambda_c^4, with c_X, c_2 pure
# numbers set by the non-perturbative dynamics.  a0 = beta X/M_Pl, rho_Lambda = c_2 Lambda_c^4.
mu_s, g_s, b0_s, cX_s, c2_s, MPl_s = sp.symbols('mu g b_0 c_X c_2 M_Pl', positive=True)
Lc = mu_s*sp.exp(-8*sp.pi**2/(b0_s*g_s**2))
X_cond   = cX_s*Lc**2
rho_cond = c2_s*Lc**4
a0_cond  = beta_s*X_cond/MPl_s
kap_cond = sp.simplify(a0_cond/sp.sqrt(rho_cond/MPl_s**2))     # kappa = a0/(c sqrt(G rho)) with G = 1/M_Pl^2
kap_cond = sp.simplify(sp.powsimp(kap_cond, force=True))
transmutation_cancels = (not kap_cond.has(g_s)) and (not kap_cond.has(mu_s)) and (not kap_cond.has(b0_s))
print(f"    C1: Lambda_c = {Lc};  X = c_X Lambda_c^2;  rho_vac = c_2 Lambda_c^4;  a0 = beta X/M_Pl")
print(f"    C1: kappa = a0/sqrt(G rho_vac) = {kap_cond}  -- the coupling g, the matching scale mu and the beta-function")
print(f"        coefficient b0 ALL cancel identically: {transmutation_cancels}.  This is a REAL property of the route and the")
print(f"        reason L32 kept it open: the LOCK (N3) is automatic, because ONE scale sets both sides.")
check("C1 [S9, credit where due] dimensional transmutation makes kappa independent of the coupling, the matching scale and the beta-function coefficient, so the LOCK (N3) holds automatically",
      transmutation_cancels,
      f"kappa = {kap_cond}: only the condensate coefficients and beta survive.  d ln a0/d ln Lambda = 1/2 along g, mu and b0 by construction. "
      f"S9 genuinely satisfies N1-N3 -- the question is whether what SURVIVES is rigid")

# --- C2: is the surviving ratio a scheme-independent pure number? ------------------------------------------------
# Test it on the ONE strongly coupled sector whose condensates are measured: QCD.  X of dimension 2 is <qbar q>^(2/3);
# rho_vac of dimension 4 is <(alpha_s/pi) G^2>.  The Lambda_c dependence cancels between them, exactly as in C1.
QQ_MEV = {"MS-bar, mu = 1 GeV": 246.0, "MS-bar, mu = 2 GeV (FLAG)": 272.0, "MS-bar, mu = 3 GeV": 285.0}
GG_GEV4 = {"SVZ central 0.012 GeV^4": 0.012, "low end 0.005 GeV^4": 0.005, "high end 0.024 GeV^4": 0.024}
print(f"    C2: the surviving number is c_X/sqrt(c_2) = <qbar q>^(2/3)/sqrt(<(alpha_s/pi)G^2>) -- Lambda_c cancels between them.")
print(f"        Evaluated on QCD's MEASURED condensates (beta = 1, i.e. the most favourable case for the route):")
S9_SET = {}
for qn, qv in QQ_MEV.items():
    for gn, gv in GG_GEV4.items():
        ratio = (qv*1e-3)**2/math.sqrt(gv)                       # (GeV^2)/(GeV^2), dimensionless
        S9_SET[f"{qn} x {gn}"] = ratio
for k_ in sorted(S9_SET, key=lambda k: S9_SET[k]):
    tag = "IN BAND" if BAND_TOT[0] <= S9_SET[k_] <= BAND_TOT[1] else ""
    print(f"        kappa = {S9_SET[k_]:.4f}   {k_}   {tag}")
S9_IN = count_in_band(S9_SET, *BAND_TOT)
spread = max(S9_SET.values())/min(S9_SET.values())
print(f"    C2: the SAME two physical condensates give kappa from {min(S9_SET.values()):.3f} to {max(S9_SET.values()):.3f} "
      f"(a factor {spread:.1f}) purely from the renormalisation scale of <qbar q> and the quoted range of <G^2>;")
print(f"        {len(S9_IN)} of the {len(S9_SET)} combinations land inside the measured band, {len(S9_SET) - len(S9_IN)} outside.")
scheme_stable = (max(S9_SET.values()) - min(S9_SET.values())) < 0.5*SIG_TOT
check("C2 [S9, rigidity] the surviving ratio of condensates is a scheme- and scale-independent pure number, so the route predicts ONE kappa",
      scheme_stable,
      f"it is not: <qbar q> is a renormalised, scale-dependent quantity and the gluon condensate is quoted over a factor 5.  The prediction "
      f"moves from {min(S9_SET.values()):.2f} (inside the band) to {max(S9_SET.values()):.2f} (outside it) with the SCHEME alone.  The candidate "
      f"set contains an INTERVAL, so it has measure, so it can never be evidence")

# --- C3: the candidate set is a continuum, and the discrete data do not reach kappa ------------------------------
# Discrete data available: N_c, N_f (through b0 = (11 N_c - 2 N_f)/3), and the operator dimensions.  C1 showed b0
# CANCELS.  So the discrete data of the sector do not enter kappa at all: only the non-perturbative O(1) coefficients do.
b0_in_kappa = kap_cond.has(b0_s)
# What survives into kappa?  Split the free symbols into DISCRETE data (integers of the sector) and CONTINUOUS parameters.
DISCRETE_SYMS = {b0_s}                                            # b0 = (11 N_c - 2 N_f)/3 is the only integer-valued datum available
CONTINUOUS_SYMS = {beta_s, cX_s, c2_s, g_s, mu_s}
survivors = kap_cond.free_symbols
disc_surv = sorted([str(s) for s in survivors & DISCRETE_SYMS])
cont_surv = sorted([str(s) for s in survivors & CONTINUOUS_SYMS])
NC = range(2, 11)
combos = sum(1 for nc in NC for nf in range(0, int(11*nc/2)) if (11*nc - 2*nf) > 0)
OPS = ["qbar q (d=3)", "G^2 (d=4)", "qbar sigma G q (d=5)", "(qbar q)^2 (d=6)", "F^2 hidden (d=4)"]
op_pairs = len(OPS)*(len(OPS) - 1)//2
print(f"    C3: the DISCRETE data of a strongly coupled sector are N_c, N_f (through b0 = (11 N_c - 2 N_f)/3) and the operator")
print(f"        dimensions.  C1 showed b0 CANCELS from kappa: b0 present in kappa = {b0_in_kappa}.")
print(f"    C3: symbols surviving into kappa -- DISCRETE: {disc_surv if disc_surv else 'NONE'};  CONTINUOUS: {cont_surv}")
print(f"        Free choices anyway: gauge group/N_c ({len(list(NC))} shown) x matter content ({combos} asymptotically free (N_c,N_f) pairs)")
print(f"        x operator pair ({op_pairs} from {len(OPS)} candidates) x renormalisation scheme (continuous).")
check("C3 [S9, rigidity] the transmutation route's candidate set is DISCRETE -- at least one integer-valued datum of the strong sector survives into kappa, so a hit could in principle carry information",
      len(disc_surv) > 0,
      f"none does: the surviving symbols are {cont_surv}, all continuous, because the beta-function coefficient b0 cancels together with the "
      f"coupling.  The candidate set therefore contains an INTERVAL, i.e. has positive measure, and a candidate set of positive measure "
      f"supplies ZERO evidence no matter which member is realised -- strictly WORSE than the {BASELINE}-member numerology baseline, not better")

# --- C4: and beta itself ----------------------------------------------------------------------------------------
beta_survives = kap_cond.has(beta_s)
print(f"    C4: beta survives in kappa: {beta_survives}.  beta is the coupling of the condensate to the MOND sector.  Two cases,")
print(f"        both bad: (i) the MOND sector is EXTERNAL to the strong sector, so beta is a Wilson coefficient generated at some")
print(f"        UV scale -- a continuous parameter the strong dynamics does not compute; (ii) the MOND sector is INSIDE the strong")
print(f"        sector, so beta is itself a non-perturbative O(1) number -- computable in principle, on a lattice, for a theory")
print(f"        nobody has specified.  Neither is discrete or structural data, which is what L32's N4 requires.")
check("C4 [S9, rigidity] the coupling beta is fixed by the strong sector rather than left as an independent parameter",
      not beta_survives,
      f"kappa = {kap_cond} retains beta explicitly.  Transmutation fixes the SCALES and leaves the COUPLING free -- which is exactly "
      f"T2's split degeneracy reappearing in a new sector: the strong dynamics sets Z~ (the condensate's own normalisation) but not the "
      f"split between Z~ and beta")

print(f"\n    S9 VERDICT: RELOCATES -- into a CONTINUUM.  Free choices = 4 discrete (gauge group, matter content, operator pair, which")
print(f"                sector hosts beta) + at least 2 continuous (the renormalisation scheme/scale, and beta itself).  The route earns")
print(f"                its N1-N3 credit honestly (C1) and then fails N4 completely: nothing discrete survives into the coefficient.")

# ====================================================================================================================
# SECTION D -- S10: nonlinear realisation / coset normalisation.  The only structure L32 flagged as able to give RIGIDITY
# ====================================================================================================================
print("\n" + "-" * 126)
print("SECTION D -- S10 coset / nonlinear realisation: what group theory FORCES, and how big the forced set is")
print("-" * 126)

# --- D1: the ZERO-FREEDOM form ----------------------------------------------------------------------------------
# CCWZ: for a coset G/H whose isotropy representation of H on g/h is IRREDUCIBLE, the G-invariant metric on the coset
# is UNIQUE up to overall scale (all irreducible symmetric spaces are of this type).  That is the ONLY circumstance in
# which a coset supplies rigidity WITHOUT further choices: with one invariant metric there is one normalisation F^2,
# so the order parameter's stiffness and its coupling to the second sector are THE SAME invariant and their ratio is 1.
# A1 established that beta and sqrt(Z~) carry the SAME dimensions (their ratio is dimensionless), so beta/sqrt(Z~) = 1
# is a meaningful, and forced, statement.
kap_irred = math.sqrt(2)*1.0
z_irred = abs(kap_irred - KBAR)/SIG_TOT
print(f"    D1: isotropy-IRREDUCIBLE coset => the G-invariant metric on g/h is unique up to overall scale => ONE normalisation F^2")
print(f"        for the order parameter's stiffness AND for its coupling to the second sector => beta/sqrt(Z~) = 1 exactly.")
print(f"    D1: that FORCES kappa = sqrt(2) x 1 = {kap_irred:.4f}, i.e. lambda = Z~/beta^2 = 1, against the measured {KBAR:.3f} +/- {SIG_TOT:.3f}")
check("D1 [S10, the zero-freedom form] the one coset construction with NO free choices -- a single invariant metric on an isotropy-irreducible coset -- agrees with the measured kappa",
      abs(kap_irred - KBAR) <= 3*SIG_TOT,
      f"it forces kappa = sqrt(2) = {kap_irred:.4f}, {z_irred:.0f} sigma from {KBAR:.3f} and {100*(kap_irred/KBAR - 1):.0f}% high.  THIS IS A "
      f"REFUTATION of the rigid form: to land anywhere near 0.354 a coset construction must put the stiffness and the coupling in "
      f"DIFFERENT invariants, which requires a reducible isotropy representation or a second scale -- i.e. free choices")

# --- D2: the group-theoretic candidate set ----------------------------------------------------------------------
# Standard Lie-algebra data: dim, rank, dual Coxeter number h^v, index of the defining rep T(F), dim of the defining rep.
# Conventions: T(fund SU(N)) = 1/2, T(vector SO(N)) = 1, T(fund Sp(2n)) = 1/2, T(adj) = h^v; C_2(R) = T(R) dim G/dim R.
ALG = {}
for n in range(1, 12):                                            # A_n = SU(n+1)
    N = n + 1; ALG[f"SU({N})"] = dict(dim=N*N - 1, rank=n, h=N, TF=0.5, dimF=N)
for n in range(2, 8):                                             # B_n = SO(2n+1)
    N = 2*n + 1; ALG[f"SO({N})"] = dict(dim=N*(N - 1)//2, rank=n, h=N - 2, TF=1.0, dimF=N)
for n in range(3, 8):                                             # C_n = Sp(2n)
    ALG[f"Sp({2*n})"] = dict(dim=n*(2*n + 1), rank=n, h=n + 1, TF=0.5, dimF=2*n)
for n in range(4, 9):                                             # D_n = SO(2n)
    N = 2*n; ALG[f"SO({N})"] = dict(dim=N*(N - 1)//2, rank=n, h=N - 2, TF=1.0, dimF=N)
ALG["Sp(4)"] = dict(dim=10, rank=2, h=3, TF=0.5, dimF=4)          # C_2 = Sp(4) ~ SO(5)
ALG["G2"] = dict(dim=14, rank=2, h=4,  TF=1.0, dimF=7)
ALG["F4"] = dict(dim=52, rank=4, h=9,  TF=3.0, dimF=26)
ALG["E6"] = dict(dim=78, rank=6, h=12, TF=3.0, dimF=27)
ALG["E7"] = dict(dim=133, rank=7, h=18, TF=6.0, dimF=56)
ALG["E8"] = dict(dim=248, rank=8, h=30, TF=30.0, dimF=248)
# standard maximal-subgroup chains (G, H, number of extra U(1) factors in H); dim(G/H) is computed, never assumed
# the third entry is the dimension of any extra factor in H (U(1) -> 1, SU(2) -> 3); dim(G/H) = dim G - dim H throughout
CHAINS = [("SU(3)", "SU(2)", 1), ("SU(4)", "SU(3)", 1), ("SU(5)", "SU(4)", 1), ("SU(6)", "SU(5)", 1),
          ("SU(4)", "Sp(4)", 0), ("SU(6)", "Sp(6)", 0), ("SU(8)", "SO(8)", 0), ("SU(5)", "SO(5)", 0),
          ("SO(7)", "G2", 0), ("SO(9)", "SO(8)", 0), ("SO(8)", "SO(7)", 0), ("SO(10)", "SU(5)", 1),
          ("SO(12)", "SU(6)", 1), ("G2", "SU(3)", 0), ("F4", "SO(9)", 0), ("E6", "F4", 0),
          ("E7", "E6", 1), ("E8", "E7", 3), ("E8", "SO(16)", 0)]
S10_SET = {}
# family 1: normalised index ratio  sqrt(T(F)/T(adj)) = sqrt(T(F)/h^v)
for nm, d in ALG.items(): S10_SET[f"F1 sqrt(T(F)/T(adj)) {nm}"] = math.sqrt(d["TF"]/d["h"])
# family 2: WZW / GKO level normalisation  sqrt(k/(k+h^v))
for nm, d in ALG.items():
    for k in range(1, 13): S10_SET[f"F2 sqrt(k/(k+h)) {nm} k={k}"] = math.sqrt(k/(k + d["h"]))
# family 3: Casimir ratio  sqrt(C2(F)/C2(adj))
for nm, d in ALG.items():
    C2F = d["TF"]*d["dim"]/d["dimF"]; S10_SET[f"F3 sqrt(C2(F)/C2(adj)) {nm}"] = math.sqrt(C2F/d["h"])
# family 4: coset dimension ratios  sqrt(dim H/dim G) and sqrt(dim(G/H)/dim G)
for g_, h_, extra in CHAINS:
    assert g_ in ALG and h_ in ALG, f"missing algebra in table: {g_} or {h_}"
    dH = ALG[h_]["dim"] + extra; dG = ALG[g_]["dim"]; dGH = dG - dH
    assert dGH > 0, f"bad chain {g_}/{h_}"
    S10_SET[f"F4 sqrt(dimH/dimG) {g_}/{h_}"] = math.sqrt(dH/dG)
    S10_SET[f"F4 sqrt(dim(G/H)/dimG) {g_}/{h_}"] = math.sqrt(dGH/dG)
# family 5: a bare index or level, 1/sqrt(m)
for m in range(1, 25): S10_SET[f"F5 1/sqrt(m) m={m}"] = 1/math.sqrt(m)
# family 6: sqrt(rank/dim)
for nm, d in ALG.items(): S10_SET[f"F6 sqrt(rank/dim) {nm}"] = math.sqrt(d["rank"]/d["dim"])

BN_BAND = (BAND_TOT[0]/math.sqrt(2), BAND_TOT[1]/math.sqrt(2))     # the band on beta/sqrt(Z~) = kappa/sqrt(2)
S10_IN = count_in_band(S10_SET, *BN_BAND)
fams, fam_tot = {}, {}
for k_ in S10_SET: fam_tot[k_.split()[0]] = fam_tot.get(k_.split()[0], 0) + 1
for k_ in S10_IN: fams[k_.split()[0]] = fams.get(k_.split()[0], 0) + 1
print(f"    D2: candidate set built from STANDARD Lie-algebra data ({len(ALG)} simple algebras, {len(CHAINS)} maximal-subgroup chains):")
print(f"        F1 sqrt(T(F)/T(adj)), F2 sqrt(k/(k+h^v)) (WZW/GKO level), F3 sqrt(C2(F)/C2(adj)), F4 coset dimension ratios,")
print(f"        F5 1/sqrt(index), F6 sqrt(rank/dim)  ->  {len(S10_SET)} candidate values for beta/sqrt(Z~).")
print(f"    D2: the measured band on beta/sqrt(Z~) is [{BN_BAND[0]:.4f}, {BN_BAND[1]:.4f}] (target 0.354); {len(S10_IN)} candidates lie inside it,")
print(f"        by family (in band / total): " + ", ".join(f"{f_}: {fams.get(f_, 0)}/{fam_tot[f_]}" for f_ in sorted(fam_tot)))
check("D2 [S10, rigidity] the coset route's group-theoretic candidate set is discriminating: fewer members land in the band than L32's numerology baseline",
      len(S10_IN) < BASELINE,
      f"{len(S10_IN)} of {len(S10_SET)} group-theoretic normalisations land in the band, against the calibrated numerology baseline of "
      f"{BASELINE}.  The route is therefore WORSE than picking a simple number at random: it supplies more ways to land in the band, "
      f"not fewer.  Group theory is not scarce")

# --- D3: the exact hits -- reported in full, and NOT adopted -----------------------------------------------------
TARGET = 1/math.sqrt(8)                                            # = kappa/sqrt(2) at kappa = 1/2, i.e. lambda = 8
exact = sorted([k for k, v in S10_SET.items() if abs(v - TARGET) < 1e-9], key=lambda k: k)
print(f"    D3: the target beta/sqrt(Z~) = 1/sqrt(8) = {TARGET:.6f} is hit EXACTLY by {len(exact)} members of the set:")
for k_ in exact: print(f"        {k_:52s} = {S10_SET[k_]:.6f}")
print(f"    D3: these are STRUCTURALLY DIFFERENT constructions -- an index ratio, a current-algebra level, and a bare index -- that")
print(f"        happen to coincide because lambda = 8 is a SMALL INTEGER and small integers are what all of them produce.  8 is also")
print(f"        dim(adjoint SU(3)), h^v(SU(8)), and 2^3.  Reporting them is the point; adopting any of them would be the error this")
print(f"        lane exists to prevent.  Nothing selects SU(4) over SU(5), or level 1 over level 2, except the answer.")
check("D3 [S10, uniqueness] the exact hit on 1/sqrt(8) is reached by ONE construction, so the group and representation are singled out",
      len(exact) <= 1,
      f"{len(exact)} structurally different group-theoretic constructions land EXACTLY on 1/sqrt(8): {'; '.join(exact)}.  Each would read as a "
      f"derivation of kappa = 1/2 if quoted alone.  That they disagree about WHICH group and WHICH level is the proof that none of them "
      f"derives anything -- and it is precisely the failure mode this repository has been burned by before")

# --- D4: counting the free choices ------------------------------------------------------------------------------
CHOICES_S10 = ["the group G", "the subgroup H / the embedding", "the representation R of the order parameter",
               "the level k (or the index), where the construction has one", "which invariant carries the stiffness vs the coupling"]
print(f"    D4: free choices in a coset construction: {len(CHOICES_S10)} -- " + "; ".join(CHOICES_S10))
print(f"        With the isotropy representation IRREDUCIBLE the last choice disappears and the answer is forced to kappa = sqrt(2) (D1,")
print(f"        refuted).  With it REDUCIBLE, the number of independent invariant metrics equals the number of irreducible summands,")
print(f"        each with its own free normalisation -- so the coefficient becomes a CONTINUOUS ratio again, not a group-theoretic one.")
check("D4 [S10, freedom] the coset route has zero free choices once the physical requirement (an order parameter with rho_vac ~ X^2, a0 ~ X) is imposed",
      len(CHOICES_S10) == 0,
      f"{len(CHOICES_S10)} free choices, and they form a dichotomy with no interior: IRREDUCIBLE isotropy forces kappa = sqrt(2) "
      f"({z_irred:.0f} sigma out, D1), REDUCIBLE isotropy restores one free normalisation per summand and the coefficient is continuous "
      f"again.  There is no coset that is rigid AND lands in the band")

print(f"\n    S10 VERDICT: RELOCATES.  Free choices = {len(CHOICES_S10)}.  Candidate set {len(S10_SET)} with {len(S10_IN)} in band vs the "
      f"{BASELINE}-member numerology baseline;\n                 {len(exact)} exact hits on 1/sqrt(8) from different groups.  Its zero-choice "
      f"form is REFUTED at kappa = sqrt(2) (D1).  L32's hope that a coset\n                 could supply N4 is NOT borne out: the rigidity it "
      f"has is rigidity about the WRONG number, and the freedom it needs to reach 0.354 destroys the rigidity.")

# ====================================================================================================================
# SECTION E -- L3's surviving door: a membrane whose charge or tension depends on beta at fixed Z~
# ====================================================================================================================
print("\n" + "-" * 126)
print("SECTION E -- the a0-dependent membrane (L3's survivor, sharpened by L32): can e(beta) or T(beta) break the split degeneracy?")
print("-" * 126)
n_s, e0_s, T0_s, p_s, s_s, eps_obs = sp.symbols('n e_0 T_0 p s epsilon_obs', positive=True)
e_of_beta = e0_s*beta_s**p_s
T_of_beta = T0_s*beta_s**s_s

# --- E1: control -- the amplitude cancels, so an a0-dependent CHARGE cannot enter through q ----------------------
print(f"    E1: L3's Q5 leaves one door: make the membrane charge e or tension T depend on beta at fixed Z~.  But A1 already showed")
print(f"        kappa^2 = 2 beta^2/Z~ with the flux amplitude q cancelling IDENTICALLY.  Changing e changes q_n = n e/Z~ and hence")
print(f"        Lambda -- it does NOT change the formula for kappa.  The door can only work by making the CONSTRAINT that fixes Z~")
print(f"        depend on beta.  Two such constraints exist, and both are tested.")
check("E1 [CONTROL] the flux amplitude cancels identically from kappa, so an a0-dependent membrane charge cannot enter kappa through the amplitude",
      q_cancels, f"kappa^2 = {kap2_sym}: no q, no G.  Any effect of e(beta) must come through whatever equation determines Z~")

# --- E2: THEOREM T7 -- the two branches, and the LOCK-vs-RIGIDITY pincer -----------------------------------------
# BRANCH 1: Z~ is fixed by matching the flux energy to the OBSERVED vacuum energy, eps_n = n^2 e^2/(2 Z~) = eps_obs.
Zt_b1 = sp.simplify(sp.solve(sp.Eq(n_s**2*e_of_beta**2/(2*Zt), eps_obs), Zt)[0])
kap2_b1 = sp.simplify((2*beta_s**2/Zt_b1))
a0_b1 = sp.simplify(beta_s*sp.sqrt(G_s)*n_s*e_of_beta/Zt_b1)
lock_b1 = sp.simplify(eps_obs*sp.diff(a0_b1, eps_obs)/a0_b1)                   # d ln a0/d ln eps at fixed (beta, n, e_0)
beta_dep_b1 = sp.simplify(sp.diff(sp.log(kap2_b1), beta_s))
p_rigid_b1 = sp.solve(sp.Eq(sp.simplify(beta_s*sp.diff(sp.log(kap2_b1), beta_s)), 0), p_s)
print(f"    E2 branch 1 (Z~ set by matching to the observed vacuum energy):  Z~ = {Zt_b1};  kappa^2 = {kap2_b1}")
print(f"        beta-independence of kappa requires p = {p_rigid_b1}; at that p, kappa^2 = {sp.simplify(kap2_b1.subs(p_s, 1))} -- it depends on")
print(f"        eps_obs, so kappa is NOT a pure number.  And a0 = {sp.simplify(a0_b1.subs(p_s, 1))} gives d ln a0/d ln Lambda = "
      f"{sp.simplify(lock_b1.subs(p_s, 1))}, not 1/2: the LOCK (N3) is VIOLATED.")
# BRANCH 2: Z~ is fixed by the terminal (marginal) nucleation condition, Delta eps_n = (2n-1)e^2/(2 Z~) = 6 pi G T^2.
Zt_b2 = sp.simplify(sp.solve(sp.Eq((2*n_s - 1)*e_of_beta**2/(2*Zt), 6*sp.pi*G_s*T_of_beta**2), Zt)[0])
kap2_b2 = sp.simplify(2*beta_s**2/Zt_b2)
q_b2 = sp.simplify(n_s*e_of_beta/Zt_b2)
a0_b2 = sp.simplify(beta_s*sp.sqrt(G_s)*q_b2)
eps_b2 = sp.simplify(Zt_b2*q_b2**2/2)
# LOCK exponent along each free-parameter direction: d ln a0 / d ln eps
def lock_exponent(var):
    da = sp.simplify(var*sp.diff(sp.log(a0_b2), var)); de = sp.simplify(var*sp.diff(sp.log(eps_b2), var))
    return sp.simplify(da/de) if sp.simplify(de) != 0 else sp.oo
rig_cond = sp.solve(sp.Eq(sp.simplify(beta_s*sp.diff(sp.log(kap2_b2), beta_s)), 0), p_s)
kap2_b2_rigid = sp.simplify(kap2_b2.subs(p_s, rig_cond[0]))
lock_beta = sp.simplify(lock_exponent(beta_s).subs(p_s, rig_cond[0]))
lock_T0 = sp.simplify(lock_exponent(T0_s).subs(p_s, rig_cond[0]))
de_e0 = sp.simplify(e0_s*sp.diff(sp.log(eps_b2.subs(p_s, rig_cond[0])), e0_s))
da_e0 = sp.simplify(e0_s*sp.diff(sp.log(a0_b2.subs(p_s, rig_cond[0])), e0_s))
print(f"    E2 branch 2 (Z~ set by the terminal nucleation condition Delta eps = 6 pi G T^2):  Z~ = {Zt_b2}")
print(f"        kappa^2 = {kap2_b2};  beta-independence requires p = {rig_cond[0]}, and then kappa^2 = {kap2_b2_rigid}")
print(f"        -- the freedom has moved from (beta, Z~) to the CONTINUOUS ratio T_0/e_0.  LOCK exponents d ln a0/d ln Lambda:")
print(f"        along beta: {lock_beta} (holds);  along T_0: {lock_T0};  along e_0: d ln eps = {de_e0}, d ln a0 = {da_e0}")
print(f"        so along e_0 the vacuum energy does not move while a0 does -- N3 requires the LOCK along EVERY free-parameter direction.")
pincer = (sp.simplify(lock_b1.subs(p_s, 1) - sp.Rational(1, 2)) != 0) and (sp.simplify(lock_T0 - sp.Rational(1, 2)) != 0) \
         and sp.simplify(de_e0) == 0 and sp.simplify(da_e0) != 0
check("E2 [membrane, THEOREM T7] an a0-dependent membrane charge or tension can fix kappa (N4) while preserving the LOCK (N3) along every free-parameter direction",
      not pincer,
      f"it cannot -- a PINCER with no interior.  Branch 1: beta-rigidity needs p = 1 and then d ln a0/d ln Lambda = {sp.simplify(lock_b1.subs(p_s, 1))}, "
      f"not 1/2 (N3 fails), and kappa is a function of the observed Lambda rather than a pure number.  Branch 2: beta-rigidity needs p - s = 1 and "
      f"then kappa^2 = {kap2_b2_rigid} -- continuous in T_0/e_0 (N4 fails), with the LOCK exponent {lock_T0} along T_0 and a0 moving at FIXED "
      f"Lambda along e_0.  Either the LOCK breaks or the coefficient stays continuous.  This CLOSES L3's surviving door")

print(f"\n    MEMBRANE VERDICT: EXCLUDED by T7.  Free choices after imposing rigidity: branch 2 leaves the continuous ratio T_0/e_0, and it")
print(f"                      violates the LOCK along T_0 and e_0; branch 1 is rigid in beta only at the price of a0 ~ Lambda^1.")

# ====================================================================================================================
# SECTION F -- the verdict
# ====================================================================================================================
print("\n" + "-" * 126)
print("SECTION F -- verdict: does ANY surviving structure DERIVE kappa?")
print("-" * 126)
VERDICTS = [
    ("S8  horizon thermodynamics",      1, len(HZ_SET), len(HZ_IN), "EXCLUDED",
     f"zero-choice form REFUTED at kappa = {kap_identity:.3f} ({z_ident:.0f} sigma); the 1/(2 pi) is inserted, not derived; absorbed by the H0 convention"),
    ("S9  two-condensate transmutation", 6, math.inf, math.inf, "RELOCATES",
     f"LOCK automatic (real credit), but the surviving number is a scheme-dependent non-perturbative O(1): {min(S9_SET.values()):.2f}-{max(S9_SET.values()):.2f} on QCD's own condensates"),
    ("S10 coset / nonlinear realisation", len(CHOICES_S10), len(S10_SET), len(S10_IN), "RELOCATES",
     f"zero-choice form REFUTED at kappa = sqrt(2) ({z_irred:.0f} sigma); {len(exact)} exact hits on 1/sqrt(8) from different groups"),
    ("L3  a0-dependent membrane",        3, 0, 0, "EXCLUDED",
     "T7 pincer: branch 1 breaks the LOCK (a0 ~ Lambda^1); branch 2 relocates kappa into the continuous ratio T_0/e_0 and breaks the LOCK along it"),
]
print(f"    {'structure':36s} {'free choices':>12s} {'candidate set':>14s} {'in band':>9s}  verdict")
for nm, nf_, ns_, ni_, vd, why in VERDICTS:
    ns_s = "continuum" if ns_ == math.inf else str(ns_); ni_s = "continuum" if ni_ == math.inf else str(ni_)
    print(f"    {nm:36s} {nf_:>12d} {ns_s:>14s} {ni_s:>9s}  {vd}")
    print(f"        {why}")
derives = [nm for nm, nf_, ns_, ni_, vd, why in VERDICTS if vd == "DERIVES"]
check("F1 [VERDICT] at least one surviving structure DERIVES kappa: zero free choices, a candidate set of one, and that one member equal to 0.354",
      len(derives) >= 1,
      f"none does.  {sum(1 for v in VERDICTS if v[4] == 'EXCLUDED')} are EXCLUDED and {sum(1 for v in VERDICTS if v[4] == 'RELOCATES')} RELOCATE. "
      f"kappa remains FITTED.  The coefficient problem is now closed in GENERAL FORM: T1-T6 (L32) plus T7 (here) close eight of the ten "
      f"enumerated structures, and the two that survive as structures relocate the fit into a discrete choice ({len(S10_IN)} in-band members, "
      f"vs the {BASELINE}-member numerology baseline) or into a continuum")
refuted = [("S8 Unruh = Gibbons-Hawking", kap_identity, z_ident),
           ("S10 isotropy-irreducible coset", kap_irred, z_irred)]
print(f"    F2: zero-freedom forms that are REFUTED rather than merely relocating (these are results, not failures of the search):")
for nm, kv, zv in refuted:
    print(f"        {nm:34s} forces kappa = {kv:.4f}  ->  {zv:.0f} sigma from {KBAR:.3f} +/- {SIG_TOT:.3f}; "
          f"vs the adopted {KAP_FOOT['canonical']:.3f} (canonical) / {KAP_FOOT['alt']:.3f} (alt)")
check("F2 [refutation ledger] the search produced at least one genuine REFUTATION -- a structure with zero free choices whose forced value lands outside the band",
      len(refuted) >= 1,
      f"{len(refuted)}: the Unruh/Gibbons-Hawking identity forces kappa = {kap_identity:.3f} and the isotropy-irreducible coset forces "
      f"kappa = {kap_irred:.3f}.  Both are excluded on both a0 footings.  A structure is only worth calling rigid if it can be wrong, and "
      f"these two are the only ones in the whole enumeration that could be")

print("\n  OUTCOME: none of L32's three survivors derives kappa, and the way each fails is now specific."
      "\n           S8 HORIZON THERMODYNAMICS is an IDENTIFICATION, and the question is settled: the 2 pi in the Unruh formula and the 2 pi in"
      "\n           the Gibbons-Hawking formula are the SAME 2 pi and CANCEL when the temperatures are equated, so the only identity-forced"
      f"\n           statement is a0 = c H_Lambda (kappa = {kap_identity:.3f}, {z_ident:.0f} sigma out).  Reaching 0.4607 requires putting the 2 pi back in by"
      "\n           hand, and a change of H0 convention converts the result into kappa = 1/2 to 1% in a0."
      "\n           S9 TRANSMUTATION earns its LOCK honestly -- the coupling, the matching scale and the beta-function coefficient all cancel --"
      "\n           and then fails rigidity completely: every discrete datum of the sector cancels WITH them, and what survives is a"
      "\n           non-perturbative prefactor that moves from inside the band to outside it with the renormalisation scheme alone."
      "\n           S10 COSET, which L32 flagged as the only structure that could supply RIGIDITY, turns out to be rigid about the wrong number:"
      f"\n           a single invariant metric forces kappa = sqrt(2) ({z_irred:.0f} sigma out), and every construction that can reach 0.354 needs the group,"
      f"\n           the embedding, the representation and the level chosen.  Its candidate set puts {len(S10_IN)} members in the band against the"
      f"\n           {BASELINE}-member numerology baseline, and hits 1/sqrt(8) EXACTLY {len(exact)} times from different groups."
      "\n           L3's a0-DEPENDENT MEMBRANE is closed here by a new theorem (T7): a beta-dependent charge or tension is a pincer -- rigidity"
      "\n           in beta forces either a0 ~ Lambda^1 (LOCK broken) or kappa ~ T_0/e_0 (continuous)."
      f"\n           And a bound that outlives all four: the 3-sigma band maps to lambda = Z~/beta^2 in [{lam_lo:.1f}, {lam_hi:.1f}], containing {len(ints_in)} integers,"
      f"\n           so even a PERFECT integer derivation of lambda = 8 would be worth {bits:.1f} bits = {sig_equiv:.1f} sigma-equivalent -- and lambda = 8 is a"
      f"\n           CANONICAL-FOOTING statement ({LAM_FOOT['alt']:.2f} on the alt footing, not an integer at all)."
      "\n           kappa remains FITTED.  Nothing here derives it, and nothing here makes 1/2 preferred over 0.461.")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(0)
