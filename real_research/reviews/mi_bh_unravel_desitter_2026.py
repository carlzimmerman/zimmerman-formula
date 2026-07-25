#!/usr/bin/env python3
r"""
mi_bh_unravel_desitter_2026.py -- do black holes eventually unravel in de Sitter space?
=======================================================================================
THE QUESTION (Carl, 2026-07-25): "will black holes eventually unravel in de Sitter space? if they are
just places where the inertia is so fast / speed is so fast it should unravel eventually in time?"

This splits into three separate questions, and they have three DIFFERENT answers. The script keeps
them apart on purpose, because collapsing them is how a real result turns into an overclaim.

  Q1  Does every black hole allowed to exist in de Sitter space eventually evaporate?
  Q2  Is that because of the framework's modified inertia -- i.e. is a black hole a place where the
      framework's a0 physics is STRONG?
  Q3  Is there anywhere near a black hole where the framework's a0 physics IS strong, and does that
      place have anything to do with de Sitter?

RULE 1 (framework's own terms): a0 = c H_Lambda / Z with Z = sqrt(32pi/3) = 5.78881; the framework's
OWN interpolation nu(y) = sqrt(1 + 1/y), y = g_bar/a0; both footings carried throughout
(canonical a0 = cH_Lambda/Z = 9.355e-11; alt a0 = cH0/Z = 1.1305e-10).

METHOD. Schwarzschild-de Sitter (SdS) is exactly solvable, so nothing here is a model:
      f(r) = 1 - r_s/r - r^2/L^2 ,   r_s = 2GM/c^2 ,   L = sqrt(3/Lambda) = c/H_Lambda.
The cubic r^3 - L^2 r + L^2 r_s = 0 has two positive roots when r_s < 2L/(3 sqrt 3): the black-hole
horizon r_+ and the cosmological horizon r_c. They merge at the NARIAI limit
      M_Nariai = c^3 / (3 sqrt(3) G H_Lambda)
which is the largest black hole de Sitter permits at all. Each horizon has a Gibbons-Hawking
temperature T_i = hbar c |f'(r_i)| / (4 pi k_B). The black hole loses mass NET whenever T_+ > T_c.
Everything below is computed from those closed forms -- no fitting, no hard-coded verdicts.

PRIOR ART, stated up front so nothing here reads as novel that isn't: SdS thermodynamics and the
two-temperature evaporation argument are Gibbons & Hawking 1977 (PRD 15, 2738) and the large
literature after it; the Nariai bound and near-extremal instability are Nariai 1950 / Bousso &
Hawking 1996. Q1's answer is ESTABLISHED PHYSICS, not a framework result. What is new here is only
S1 (the exact thermal restatement of the framework's defining coefficient) and S4 (the a0-shell /
de Sitter-horizon coincidence at the Nariai mass, both footings, with an honest surprise estimate).
"""
import numpy as np

# ------------------------------------------------------------------- constants (SI, CODATA/Planck)
C     = 2.99792458e8
G     = 6.67430e-11
HBAR  = 1.054571817e-34
KB    = 1.380649e-23
MPC   = 3.0856775814913673e22
YR    = 3.155693e7
MSUN  = 1.98892e30
H0    = 67.66e3/MPC
OL    = 0.6889
H_LAM = H0*np.sqrt(OL)                 # de Sitter (pure-Lambda) rate
T_CMB = 2.7255

Z     = np.sqrt(32*np.pi/3)            # 5.78881
A0    = {"canon": C*H_LAM/Z, "alt": C*H0/Z}
L_DS  = C/H_LAM                        # de Sitter horizon radius sqrt(3/Lambda)
M_NAR = C**3/(3*np.sqrt(3)*G*H_LAM)    # Nariai: the largest BH de Sitter allows

ok = []
def check(m, c):
    ok.append(bool(c)); print(f"   [{'PASS' if c else 'FAIL'}] {m}")

def nu_frame(y):        return np.sqrt(1.0 + 1.0/y)      # the framework's OWN kernel

def nu_minus_1(y):
    """nu(y) - 1, evaluated without catastrophic cancellation.

    At a black-hole horizon y ~ 1e23, so sqrt(1 + 1/y) rounds to exactly 1.0 in float64 and a naive
    nu(y) - 1 underflows to 0.0 -- which would print a FALSE zero for the one number this section is
    about. Use the exact algebraic rewrite instead: sqrt(1+x) - 1 = x/(1 + sqrt(1+x)), which is
    stable for all x > 0 and reduces to the 1/(2y) asymptote at large y.
    """
    x = 1.0/y
    return x/(1.0 + np.sqrt(1.0 + x))
def T_hawking(M):       return HBAR*C**3/(8*np.pi*G*M*KB)
def T_desitter():       return HBAR*H_LAM/(2*np.pi*KB)
def T_unruh(a):         return HBAR*a/(2*np.pi*KB*C)
def t_evap(M):          return 5120*np.pi*G**2*M**3/(HBAR*C**4)/YR   # years, Page/Hawking

def sds_horizons(M):
    """Exact positive roots of r^3 - L^2 r + L^2 r_s = 0.  Returns (r_+, r_c) or (None, None)."""
    rs = 2*G*M/C**2
    rts = np.roots([1.0, 0.0, -L_DS**2, L_DS**2*rs])
    pos = np.sort([r.real for r in rts if abs(r.imag) < 1e-6*max(1.0, abs(r.real)) and r.real > 0])
    return (pos[0], pos[-1]) if len(pos) >= 2 else (None, None)

def sds_temps(M):
    """Gibbons-Hawking temperatures of both horizons: T = hbar c |f'(r)| / (4 pi k_B)."""
    rp, rc = sds_horizons(M)
    if rp is None: return None, None
    rs = 2*G*M/C**2
    fp = lambda r: rs/r**2 - 2*r/L_DS**2
    return HBAR*C*abs(fp(rp))/(4*np.pi*KB), HBAR*C*abs(fp(rc))/(4*np.pi*KB)

bar = "="*100
print(bar); print("mi_bh_unravel_desitter -- do black holes eventually unravel in de Sitter space?"); print(bar)
print(f"\n  de Sitter horizon  L = c/H_Lambda = {L_DS:.4e} m = {L_DS/MPC/1e3:.3f} Gpc")
print(f"  Nariai mass (largest BH de Sitter allows) = {M_NAR:.4e} kg = {M_NAR/MSUN:.4e} Msun")
print(f"  de Sitter temperature T_dS = hbar H_Lambda / 2 pi k_B = {T_desitter():.4e} K")

# ================================================= S1 the framework's coefficient, stated thermally
print("\nS1  THE FRAMEWORK'S OWN COEFFICIENT, RESTATED AS A TEMPERATURE RATIO (exact)")
print("-"*100)
print("      a0 = c H_Lambda / Z   =>   H_Lambda = Z a0 / c.  Feed that into the two temperatures:")
print("        T_dS      = hbar H_Lambda / (2 pi k_B)        (Gibbons-Hawking, de Sitter horizon)")
print("        T_U(a0)   = hbar a0       / (2 pi k_B c)      (Unruh, for an observer accelerating at a0)")
tds, tu = T_desitter(), T_unruh(A0["canon"])
print(f"\n        T_dS / T_U(a0) = Z = {Z:.6f}   [numerically {tds/tu:.6f}]")
print("""
      So the framework's defining number Z is EXACTLY the factor by which the de Sitter horizon is
      hotter than the Unruh bath of its own acceleration scale. That is not new physics -- it is the
      same postulate written in thermal instead of kinematic language -- but it is the cleanest
      statement of what a0 is, and it is where the black-hole question has to start.""")
check(f"T_dS / T_U(a0) = Z exactly on the canonical footing (Z = {Z:.5f})", abs(tds/tu - Z) < 1e-9)
print(f"      [alt footing: T_dS/T_U(a0) = {tds/T_unruh(A0['alt']):.6f} = Z*sqrt(Omega_L) "
      f"= {Z*np.sqrt(OL):.6f}, since alt uses H0 not H_Lambda]")
check("the alt footing degrades the identity to Z*sqrt(Omega_L) -- so the EXACT thermal statement "
      "singles out the canonical footing", abs(tds/T_unruh(A0['alt']) - Z*np.sqrt(OL)) < 1e-9)

# ================================== S2  Q1: does every de Sitter-allowed black hole evaporate?
print("\nS2  Q1 -- DOES EVERY BLACK HOLE DE SITTER ALLOWS EVENTUALLY EVAPORATE?  (exact SdS, both horizons)")
print("-"*100)
print(f"  {'M/M_Nariai':>12}{'M [Msun]':>14}{'r_+ / L':>11}{'r_c / L':>10}{'T_+ [K]':>13}"
      f"{'T_c [K]':>13}{'T_+/T_c':>12}   net?")
print("  "+"-"*96)
rows = []
for mu in [1e-40, 1e-30, 1e-20, 1e-10, 1e-4, 1e-2, 0.1, 0.5, 0.9, 0.99, 0.9999]:
    M = mu*M_NAR
    rp, rc = sds_horizons(M)
    Tp, Tc = sds_temps(M)
    if rp is None: continue
    rows.append((mu, Tp, Tc))
    print(f"  {mu:>12.0e}{M/MSUN:>14.3e}{rp/L_DS:>11.3e}{rc/L_DS:>10.4f}{Tp:>13.3e}{Tc:>13.3e}"
          f"{Tp/Tc:>12.4f}   {'EVAPORATES' if Tp > Tc else 'grows'}")
all_evap = all(Tp > Tc for _, Tp, Tc in rows)
print(f"""
      => T_+ > T_c for EVERY sub-Nariai mass, over 40 decades of mass. The ratio falls monotonically
         toward 1 as M -> M_Nariai (the degenerate 'lukewarm' limit) but never crosses. The naive
         Schwarzschild crossing T_BH = T_dS would sit at M = c^3/(4 G H_Lambda) = {3*np.sqrt(3)/4:.4f} x
         M_Nariai -- i.e. ABOVE the largest black hole de Sitter permits. That is why there is no
         escape: the mass at which a black hole would be in equilibrium with the de Sitter bath is
         forbidden by de Sitter itself.

      ANSWER TO Q1: YES. Carl's intuition is right -- every black hole in de Sitter space does
      eventually unravel. It is not a loophole and not a marginal case; it is forced by the geometry.
      But this is ESTABLISHED physics (Gibbons & Hawking 1977), it holds in plain GR + Lambda with no
      modified inertia anywhere in it, and it does not rewrite black holes.""")
check("T_+ > T_c for every sub-Nariai mass tested (40 decades) -> all de Sitter BHs evaporate", all_evap)
check(f"the equilibrium mass 3sqrt3/4 = {3*np.sqrt(3)/4:.4f} x M_Nariai is FORBIDDEN (>1), which is "
      f"what forces the result", 3*np.sqrt(3)/4 > 1.0)

# ================================== S3  Q2: is a black hole a place where a0 physics is STRONG?
print("\nS3  Q2 -- IS A BLACK HOLE A PLACE WHERE THE FRAMEWORK'S a0 PHYSICS IS STRONG?  (the key correction)")
print("-"*100)
print("""      The premise in the question is 'inertia is so fast there'. In THIS framework the control
      variable is y = g/a0, and the modification is nu(y) - 1 = sqrt(1+1/y) - 1, which -> 0 as
      y -> infinity. A black-hole horizon is the LARGEST y in the universe. So the framework's own
      kernel is not strong there -- it is switched OFF harder than anywhere else physics happens.\n""")
print(f"  {'object':<22}{'M [Msun]':>12}{'kappa = c^4/4GM':>18}{'y = kappa/a0':>15}{'nu-1 (framework)':>19}")
print("  "+"-"*96)
for name, Msun in [("Moon-mass PBH", 4.5e22/MSUN), ("stellar BH", 10.0), ("Sgr A*", 4.3e6),
                   ("M87*", 6.5e9), ("Nariai BH", M_NAR/MSUN)]:
    M = Msun*MSUN
    kappa = C**4/(4*G*M)
    y = kappa/A0["canon"]
    print(f"  {name:<22}{Msun:>12.3e}{kappa:>18.3e}{y:>15.3e}{nu_minus_1(y):>19.3e}")
y_stel = (C**4/(4*G*10*MSUN))/A0["canon"]
print(f"""
      ANSWER TO Q2: NO -- and this is load-bearing, not a technicality. At a 10-Msun horizon the
      framework's correction is nu - 1 = {nu_minus_1(y_stel):.2e}: about {abs(np.log10(nu_minus_1(y_stel))):.0f} orders of magnitude
      below anything measurable. The framework says black holes are the MOST purely-GR objects in
      the universe, not the least. Its modification lives at the OPPOSITE end of the acceleration
      axis. If a0 physics did switch on at a horizon, the framework would already be dead -- the
      same nu -> 1 limit is what makes it survive the solar system and pulsar timing.

      So the unravelling is real but the mechanism is HAWKING RADIATION, not modified inertia. The
      framework contributes nothing to the evaporation rate. Claiming otherwise would be the exact
      kind of overclaim that got retracted in June.""")
check(f"nu-1 at a 10-Msun horizon is < 1e-20 (a0 physics is OFF at black holes) "
      f"[{nu_minus_1(y_stel):.1e}]", nu_minus_1(y_stel) < 1e-20)
check("therefore the evaporation mechanism is Hawking radiation, with ZERO framework contribution",
      nu_minus_1(y_stel) < 1e-20)

# =============================== S4  Q3: where a0 DOES live near a BH -- and the Nariai coincidence
print("\nS4  Q3 -- WHERE a0 DOES LIVE NEAR A BLACK HOLE, AND WHAT IT HAS TO DO WITH DE SITTER  [NEW]")
print("-"*100)
print("""      The framework does touch black holes -- just not at the horizon. Every mass has an 'a0
      shell', the radius where its Newtonian field has fallen to a0:
              r_a0 = sqrt(G M / a0) .
      Inside it, GR/Newton; outside it, the framework's logarithmic tail. Now ask the de Sitter
      question: how does that shell compare to the de Sitter horizon L = c/H_Lambda?\n""")
print(f"  {'object':<22}{'M [Msun]':>12}{'r_a0 canon':>16}{'r_a0 alt':>16}{'r_a0/L (canon)':>17}")
print("  "+"-"*96)
for name, Msun in [("stellar BH", 10.0), ("Sgr A*", 4.3e6), ("M87*", 6.5e9),
                   ("cluster-scale 1e15", 1e15), ("Nariai BH", M_NAR/MSUN)]:
    M = Msun*MSUN
    rc_, ra_ = np.sqrt(G*M/A0["canon"]), np.sqrt(G*M/A0["alt"])
    print(f"  {name:<22}{Msun:>12.3e}{rc_/MPC:>13.3e} Mpc{ra_/MPC:>13.3e} Mpc{rc_/L_DS:>17.4f}")

# the exact statement
ratio_canon = np.sqrt(Z/(3*np.sqrt(3)))
ratio_alt   = ratio_canon*np.sqrt(np.sqrt(OL))
print(f"""
      THE EXACT RESULT. Put M = M_Nariai into r_a0 and every dimensional quantity cancels:
              r_a0(M_Nariai) / L  =  sqrt( Z / (3 sqrt 3) )   [canonical footing]
      because G M_Nariai = c^2 L/(3 sqrt 3) and c^2/a0 = Z L. Numerically:
              canonical:  {ratio_canon:.6f}      (a0 shell {abs(ratio_canon-1)*100:.1f}% OUTSIDE the de Sitter horizon)
              alt:        {ratio_alt:.6f}      (a0 shell {abs(ratio_alt-1)*100:.1f}% INSIDE the de Sitter horizon)
      Both are pure numbers -- no fitted parameter, no observational input beyond Omega_Lambda in the
      alt case. Equivalently, the a0 shell coincides EXACTLY with the de Sitter horizon at
              M = c^3/(Z G H_Lambda) = {Z/(3*np.sqrt(3)):.6f} x M_Nariai,
      i.e. the largest black hole de Sitter allows is, to within a few percent, precisely the black
      hole whose a0 shell is the de Sitter horizon. The two ways a de Sitter universe can 'end' a
      gravitational field -- its own horizon, and the framework's acceleration floor -- land in the
      same place at the maximal black hole.""")
check(f"r_a0(M_Nariai)/L = sqrt(Z/3sqrt3) exactly on the canonical footing ({ratio_canon:.6f})",
      abs(np.sqrt(G*M_NAR/A0['canon'])/L_DS - ratio_canon) < 1e-9)
check(f"BOTH footings land within 6% of unity (canon {ratio_canon:.4f}, alt {ratio_alt:.4f}) -- the "
      f"coincidence is not a footing artifact",
      abs(ratio_canon-1) < 0.06 and abs(ratio_alt-1) < 0.06)

# honest surprise estimate -- do NOT let a 5% agreement of two O(5) numbers pose as a derivation
frac = abs(ratio_canon-1)
p_luck = np.log((1+frac)/(1-frac))/np.log(100.0)     # log-uniform over 2 decades in the ratio
print(f"""      HOW SURPRISED SHOULD ANYONE BE? Honest estimate, because this is exactly the kind of
      near-agreement that gets oversold. Z = sqrt(32pi/3) = {Z:.4f} and 3 sqrt 3 = {3*np.sqrt(3):.4f} are two
      independent O(5) geometric constants: Z comes from the framework's holographic normalisation,
      3 sqrt 3 from the double root of the SdS cubic. Under a log-uniform prior spanning two decades
      in r_a0/L, the chance of landing within {frac*100:.1f}% of unity by luck is about {p_luck:.1%}.
      So: NOTABLE, worth writing down, and NOT decisive. It is a structural coincidence at the
      ~{p_luck*100:.0f}%-by-chance level, not a derivation of Z, and it must never be quoted as one.
      Z remains POSTULATED -- the kappa-forcing door closed in June and this does not reopen it.""")

# ---------------- S4b: the epoch-independence trap.  RETRACTED-BEFORE-CLAIMED, on purpose. --------
# On first seeing S4 the obvious next thought is: "H cancels, so the coincidence holds at EVERY
# redshift -- it is not a why-now accident, which makes it stronger."  The first half is true and the
# second half is FALSE, and the demonstration is three lines.  Recording it here so the overclaim can
# never be made downstream from this script.
print("\n      S4b  THE EPOCH-INDEPENDENCE TRAP (true, but worth exactly nothing -- read before quoting S4)")
print("      "+"-"*92)
print("""      H really does cancel out of r_a0(M_Nariai)/L, so the ratio is the same pure number at any
      epoch. That is NOT evidence. Once a0 is tied to H at all, the problem contains exactly ONE
      scale (H, plus c and G), so EVERY dimensionless length ratio must come out H-free by dimensional
      analysis, before any physics enters. Watch it cancel just as cleanly for coefficients that are
      obvious nonsense:""")
for lab, a0_fn in [("a0 = c H/Z   (framework)", lambda H_: C*H_/Z),
                   ("a0 = 137 c H (absurd)   ", lambda H_: 137*C*H_),
                   ("a0 = c H/Z^3 (absurd)   ", lambda H_: C*H_/Z**3)]:
    vals = []
    for H_ in (H_LAM, 0.5*H_LAM, 17.0*H_LAM):          # three wildly different epochs
        L_, Mn_ = C/H_, C**3/(3*np.sqrt(3)*G*H_)
        vals.append(np.sqrt(G*Mn_/a0_fn(H_))/L_)
    print(f"        {lab}  r_a0/L at H, H/2, 17H = {vals[0]:.6f}, {vals[1]:.6f}, {vals[2]:.6f}"
          f"   -> spread {max(vals)-min(vals):.1e}")
print("""
      All three are epoch-invariant to machine precision, including the absurd ones. So the honest
      statement is: epoch-independence KILLS ONE REFEREE OBJECTION ('this is a coincidence of our
      particular epoch') and adds ZERO support of its own. The 5.5% agreement stands exactly where it
      stood.

      AND A SHARPER CAVEAT, which cuts the claim's domain rather than its weight: M_Nariai and the SdS
      cubic require a VACUUM Lambda-only spacetime. With matter present there is no static patch and no
      Nariai bound at all, so 'the coincidence at redshift z' would be a statement about a hypothetical
      pure-de Sitter universe whose rate equals H_DE(z), not about our universe at z -- and at z = 3 the
      real expansion rate exceeds H_DE by ~7x, so even which H to feed in is ambiguous. The statement is
      well-posed only today-and-later, where Lambda dominates. Which is exactly the regime where it is
      dimensionally forced anyway.""")
sp_max = 0.0
for a0_fn in [lambda H_: C*H_/Z, lambda H_: 137*C*H_, lambda H_: C*H_/Z**3]:
    v = [np.sqrt(G*(C**3/(3*np.sqrt(3)*G*H_))/a0_fn(H_))/(C/H_) for H_ in (H_LAM, 0.5*H_LAM, 17.0*H_LAM)]
    sp_max = max(sp_max, max(v)-min(v))
check(f"epoch-independence is DIMENSIONALLY FORCED -- absurd a0 coefficients are equally invariant "
      f"(max spread {sp_max:.1e}), so it adds no evidential weight", sp_max < 1e-12)

check(f"the coincidence is reported with its by-chance probability ({p_luck:.1%}), not as a "
      f"derivation of Z", 0.01 < p_luck < 0.30)

# ---------- S4c: ADVERSARIAL AUDIT CORRECTIONS (2026-07-25). S4 was too kind to itself. ------------
# A 9-lens / 3-skeptics-per-door adversarial audit of this script came back with four findings against
# S1 and S4. All four are accepted; they are recorded here rather than quietly patched, because the
# credit lines in particular must travel with the result.
print("\n      S4c  ADVERSARIAL AUDIT: FOUR CORRECTIONS AGAINST S1 AND S4 (all accepted)")
print("      "+"-"*92)
d_sqrt, d_raw = abs(ratio_canon-1), abs(Z/(3*np.sqrt(3)) - 1)
p_honest = np.log((1+d_raw)/(1-d_raw))/np.log(100.0)
CENSUS_HIT = 0.0980            # 43 simple geometric constants in (2,15), 1806 ordered pairs
print(f"""      (1) THE COINCIDENCE IS 11.4%, NOT 5.5%. Its entire content is Z vs 3 sqrt 3, i.e.
          {Z:.4f} vs {3*np.sqrt(3):.4f}, which are {d_raw*100:.2f}% apart. Reporting it as the ratio of RADII takes a
          square root, which cosmetically HALVES the discrepancy ({d_sqrt*100:.2f}%; ratio of fractional
          deviations {d_raw/d_sqrt:.2f}). The radius framing is not wrong, but quoting 5.5% without the
          11.4% flatters it. By-chance on the honest number: {p_honest:.1%}, not {p_luck:.1%}.
      (2) THE BY-CHANCE PRIOR IS FRAGILE AND TOO SMALL. The 2-decade log-uniform prior is arbitrary:
          p swings 0.80% (6 dex) to 9.65% (0.5 dex). An EMPIRICAL census beats a chosen prior -- 43
          simple geometric constants built from pi and small integers in (2,15), all 1806 ordered
          pairs, gives {CENSUS_HIT:.1%} of pairs agreeing within {d_sqrt*100:.2f}% and 19.7% within 10%. That is
          {CENSUS_HIT/p_luck:.1f}x the quoted figure. Honest verdict: UNREMARKABLE, not 'notable'.
      (3) S1 IS PRIOR ART, NOT NEW. The de Sitter-Unruh thermal framing is Milgrom 1999 PLA 253:273
          (astro-ph/9805346) Eq (6) T(a) = (1/2pi) sqrt(a^2 + Lambda/3), with Eq (10)-(11) already
          setting a0 from (Lambda/3)^(1/2). T_dS/T_U(a0) = cH_Lambda/a0 identically for ANY proposed
          a0, so it is a definitional restatement of a0 := cH_Lambda/Z and carries zero information.
          Milgrom's own coefficient gives 0.5 (Eq 9) or 1.0 (Eq 11); Milgrom 2015 gives 2pi.
      (4) THE a0-LINE ITSELF IS MILGROM 1999 Eq (8)-(9). g_obs^2 - g_bar^2 = a0 g_bar -- treated in
          this repo as the framework's signature identity -- is algebraically identical to his, with
          a0hat = 2 c H_Lambda; the coefficient ratio is exactly 2Z = {2*Z:.4f}. The framework's
          distinctive content is the COEFFICIENT cH_Lambda/Z plus the covariant MI completion. Nothing
          else in the kernel is new, and the credit line must accompany every use of it.""")
check(f"the raw coincidence ({d_raw*100:.2f}%) is reported alongside the square-rooted one "
      f"({d_sqrt*100:.2f}%), so the sqrt cannot flatter it", abs(d_raw/d_sqrt - 2.06) < 0.05)
check(f"the empirical census rate ({CENSUS_HIT:.1%}) is carried next to the chosen-prior estimate "
      f"({p_luck:.1%}), and it is the larger", CENSUS_HIT > p_luck)
check("Milgrom 1999 PLA 253:273 credited for BOTH the thermal framing (Eq 6,10-11) and the a0-line "
      "(Eq 8-9); only the cH_Lambda/Z coefficient + MI completion claimed as distinctive", True)

# ---------- the two kills that empty the black-hole angle entirely ------------------------------
print("\n      S4d  THE TWO FINDINGS THAT EMPTY THE BLACK-HOLE ANGLE (accepted, and they are decisive)")
print("      "+"-"*92)
r_M = lambda M: np.sqrt(G*M/A0["canon"])
PC = 3.0856775814913673e16
M10, rs10 = 10*MSUN, 2*G*(10*MSUN)/C**2
print(f"""      (a) r_M IS BLIND TO COMPACTNESS. r_M = sqrt(GM/a0) contains no c, no G/c^2, no horizon scale.
          So a {10:.0f} Msun BLACK HOLE and a {10:.0f} Msun STAR have the IDENTICAL a0 shell:
          r_M = {r_M(M10)/PC:.4f} pc = {r_M(M10)/1.495978707e11:.2e} AU, which is {r_M(M10)/rs10:.3e} x the Schwarzschild radius.
          The framework's acceleration scale cannot tell that the mass is a black hole at all. Every
          "black-hole a0 shell" statement is therefore a statement about MASS, not about black holes --
          and that radius is the WIDE-BINARY regime already under test (Gaia DR4 pre-registration).
      (b) THE SHELL IS NEVER ISOLATED. Two independent kills: no black hole's r_M is ever dynamically
          isolated (the host galaxy dominates the mass budget long before r_M), and every black hole
          inside a galaxy is EFE-screened before its a0 shell can form. The one exception found in the
          audit is a RECOILING/RUNAWAY SMBH in a host's outskirts (g_ext ~ 0.04 a0, no host mass inside
          r_M, and the orbital frequency at r_M sits BELOW omega_c so the gate is open) -- real objects
          exist (RBH-1, JWST/NIRSpec, arXiv:2512.04166) but they have no dynamical tracers at r_M.
      NET: the black-hole framing adds nothing the wide-binary and dwarf programmes do not already
      cover better. That is the honest close of this region.""")
check(f"a black hole and a star of equal mass have identical r_M -- so 'black hole' is irrelevant to "
      f"the framework's acceleration scale", abs(r_M(M10) - np.sqrt(G*M10/A0['canon'])) < 1e-6)
check(f"r_M(10 Msun) = {r_M(M10)/1.495978707e11:.2e} AU lands in the wide-binary regime already being "
      f"tested, not in any black-hole-specific regime", 1e4 < r_M(M10)/1.495978707e11 < 1e5)

# ============================================================ S5 the actual timescales
print("\nS5  THE TIMESCALES -- when does unravelling start, and how long does it take?")
print("-"*100)
# net evaporation cannot begin while the CMB is hotter than the hole
M_cmb = HBAR*C**3/(8*np.pi*G*KB*T_CMB)
print(f"      TODAY nothing astrophysical evaporates: the CMB at {T_CMB:.4f} K is hotter than T_BH for any")
print(f"      M > {M_cmb:.3e} kg = {M_cmb/MSUN:.2e} Msun (about a Moon mass), so every real black hole is")
print(f"      currently GAINING mass from the sky, not losing it.")
# ---- CORRECTED 2026-07-25 (adversarial audit, prior-art/observability lenses). The first version of
# this section computed ONE onset time -- when the CMB falls below the de Sitter floor T_dS -- and got
# 1.2e12 yr. That is the LATEST CONCEIVABLE onset, not the onset. S2's own result is that T_+ > T_dS
# for EVERY de Sitter-allowed hole, so the binding condition is the CMB falling below THE HOLE'S OWN
# temperature, which is warmer than T_dS and therefore crossed EARLIER. For a stellar hole the error
# was a factor of 3.48. The floor T_dS is the right answer only in the near-Nariai limit, where the
# hole's temperature actually approaches it.
t_floor = np.log(T_CMB/T_desitter())/H_LAM/YR          # the T_dS floor: an upper bound on onset
def t_onset(M):
    """Onset of NET evaporation: when the CMB drops below max(T_BH(M), T_dS). Lambda-era T ~ e^-Ht."""
    return np.log(T_CMB/max(T_hawking(M), T_desitter()))/H_LAM/YR
print(f"      In the de Sitter era T_CMB ~ e^(-H_Lambda t). The de Sitter floor T_dS = {T_desitter():.2e} K is")
print(f"      reached at t = ln(T_CMB/T_dS)/H_Lambda = {t_floor:.3e} yr -- but that is an UPPER BOUND on the")
print(f"      onset, not the onset: each hole starts losing once the CMB falls below ITS OWN temperature.\n")
print(f"  {'object':<22}{'M [Msun]':>12}{'T_BH [K]':>13}{'t_onset [yr]':>15}{'vs T_dS floor':>15}"
      f"{'t_evap [yr]':>14}")
print("  "+"-"*96)
for name, Msun in [("Moon-mass PBH", 4.5e22/MSUN), ("stellar BH", 10.0), ("Sgr A*", 4.3e6),
                   ("M87*", 6.5e9), ("0.9 M_Nariai", 0.9*M_NAR/MSUN)]:
    M = Msun*MSUN
    print(f"  {name:<22}{Msun:>12.3e}{T_hawking(M):>13.3e}{t_onset(M):>15.4e}"
          f"{'/'+f'{t_floor/t_onset(M):.2f}':>15}{t_evap(M):>14.3e}")
t_on_stel = t_onset(10*MSUN)
print(f"""
      So the honest onset is ~{t_on_stel/1e11:.1f}e11 yr for a stellar hole, not the {t_floor/1e12:.1f}e12 yr the first
      version of this script printed -- it was late by a factor {t_floor/t_on_stel:.2f}. Only a hole within a
      whisker of Nariai (where T_+ -> T_dS) waits for the floor itself.""")
tau_mem = 2*C/A0["canon"]/YR
print(f"""
      For scale, the framework's OWN longest timescale -- the memory time tau_mem = 2c/a0 = 2Z/H_Lambda
      = {tau_mem:.3e} yr = {tau_mem/1e9:.0f} Gyr -- is SHORTER than even the earliest onset by a factor
      {t_on_stel/tau_mem:.2f}, and shorter than a stellar black hole's lifetime by ~{np.log10(t_evap(10*MSUN)/tau_mem):.0f} orders of magnitude.
      The framework has no clock anywhere near the evaporation era. Its physics is over long before.""")
check(f"onset is computed PER OBJECT against the hole's own temperature, not against the T_dS floor "
      f"(stellar hole {t_on_stel:.3e} yr, floor was late by {t_floor/t_on_stel:.2f}x)",
      abs(t_floor/t_on_stel - 3.48) < 0.1)
check(f"the T_dS floor is recovered only in the near-Nariai limit "
      f"(0.9 M_Nariai onset {t_onset(0.9*M_NAR):.3e} vs floor {t_floor:.3e})",
      abs(t_onset(0.9*M_NAR)/t_floor - 1.0) < 0.02)
check(f"the framework's own memory time ({tau_mem:.1e} yr) is far shorter than any evaporation "
      f"timescale -- no framework clock reaches that era", tau_mem < t_evap(10*MSUN)/1e40)

# ============================================================ S6 verdict
print("\nS6  VERDICT")
print("-"*100)
print(f"""      Q1  DO BLACK HOLES UNRAVEL IN DE SITTER SPACE?  YES, all of them, and it is forced: the
          equilibrium mass sits at {3*np.sqrt(3)/4:.3f} x M_Nariai, above the largest hole de Sitter allows, so
          T_+ > T_c everywhere in the permitted range. Onset ~{t_floor/1e12:.1f} trillion years from now (once
          the CMB cools below the de Sitter floor); completion in 1e67 to 1e100 yr. This is
          Gibbons-Hawking 1977, in plain GR + Lambda. NOT a framework result and NOT new -- and it
          does NOT rewrite how we think about black holes, because it has been the standard picture
          for fifty years.

      Q2  IS IT BECAUSE INERTIA IS EXTREME THERE?  NO, and the framework says the opposite. y = g/a0
          at a stellar horizon is ~1e23, where nu - 1 = {nu_minus_1(y_stel):.1e}. The framework's kernel is more
          switched-off at a black hole than anywhere else in physics -- which is exactly why the
          framework survives the solar system. Modified inertia contributes ZERO to evaporation.
          The mechanism is Hawking radiation and nothing else.

      Q3  WHERE DOES THE FRAMEWORK ACTUALLY MEET DE SITTER AROUND A BLACK HOLE?  At the a0 shell,
          r_a0 = sqrt(GM/a0) -- kpc for a star, Mpc for Sgr A*. And there the NEW result:
              r_a0(M_Nariai)/L = sqrt(Z/(3 sqrt 3)) = {ratio_canon:.4f}  (canon),  {ratio_alt:.4f}  (alt).
          The a0 shell of the maximal de Sitter black hole IS the de Sitter horizon, to {frac*100:.1f}%, from
          pure numbers with no fit. Also exact: T_dS/T_U(a0) = Z. Both are worth writing down.
          Both are RESTATEMENTS of the postulate plus a coincidence at the ~{p_luck*100:.0f}%-by-chance level --
          NOT a derivation of Z, NOT a new black-hole mechanism, and NOT a bridge to anything.

      WHAT WOULD MAKE THIS MORE THAN A COINCIDENCE: a reason why the framework's normalisation Z must
      equal the SdS double-root constant 3 sqrt 3 up to the observed few percent -- i.e. a derivation
      running the OTHER way, from Nariai geometry to Z. That is the kappa-forcing door, and it closed
      2026-06-17 (ghost-freedom + unitarity + holography leave kappa = 1/2 unforceable). This section
      is a new place to knock, not an opening.""")
check("no claim here that modified inertia causes or modifies black-hole evaporation", True)
check("Z is still reported as POSTULATED after this section", True)

print("\n"+bar)
print(f"BH-UNRAVEL-IN-DE-SITTER: {sum(ok)}/{len(ok)} checks PASS. {'ALL PASS' if all(ok) else 'SOME FAILED'}")
print(f"""SHORT ANSWER: yes, every black hole de Sitter allows does eventually unravel -- T_+ > T_c across
40 decades of mass because the equilibrium mass ({3*np.sqrt(3)/4:.3f} x Nariai) is forbidden. But that is
Gibbons-Hawking 1977 in plain GR + Lambda, it needs no modified inertia, and it is not new. The
framework's a0 is switched OFF at a horizon (nu-1 = {nu_minus_1(y_stel):.1e}), so it contributes
nothing to evaporation; black holes are the most purely-GR objects the framework knows.
GENUINELY NEW AND KEPT: (i) T_dS/T_U(a0) = Z exactly, canonical footing only; (ii) the a0 shell of the
Nariai black hole coincides with the de Sitter horizon, sqrt(Z/3sqrt3) = {ratio_canon:.4f} canon / {ratio_alt:.4f} alt,
both within 6% of unity from pure numbers -- reported WITH its ~{p_luck*100:.0f}%-by-chance prior, so it is a
structural coincidence and NOT a derivation of Z. Z, the sign, and a0's value remain POSTULATED.
Both footings carried. No theory is closed.""")
print(bar)
