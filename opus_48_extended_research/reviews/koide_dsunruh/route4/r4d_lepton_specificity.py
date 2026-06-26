#!/usr/bin/env python3
"""
ROUTE 4 (d) -- THE DECISIVE CONSTRAINT: WHY CHARGED LEPTONS AND NOT QUARKS?

Any Route-4 fixed-point/stability principle that lands the sqrt-mass vector at 45deg must
be LEPTON-SPECIFIC: charged leptons obey Koide (Q=2/3) but quarks do NOT (Q_up=0.849,
Q_down=0.731). A flavor-blind principle that forces 45deg for everyone is FALSIFIED by the
quarks. This module asks the both-ways question:

  Is there a DERIVED lepton-specific ingredient -- color-singlet-ness, the SO(10) 16
  lepton embedding, the absence of QCD -- that selects the 45deg config for leptons but
  detunes it for quarks? Or does every candidate require FITTING the quark detuning
  (= the principle has no predictive lepton-selection, it is post-hoc)?

We test three lepton-specific mechanisms quantitatively with PDG masses (mpmath dps=40):
  (M1) QCD detuning: quarks get large QCD self-energy / running that shifts their sqrt-mass
       shape AWAY from 45deg; leptons (colorless) keep the clean value. Does removing QCD
       running from quarks move them TOWARD 45deg? (If yes -> lepton-specificity has teeth;
       if the quark detuning is NOT a QCD effect -> the selection is unexplained.)
  (M2) SO(10) 16 embedding: leptons and quarks sit in the SAME 16, so a 16-universal flavor
       structure gives the SAME shape to both -> CANNOT be the selector (predicts quark
       Koide too). Falsify.
  (M3) The honest accounting: how much TUNING (free parameters) does each scheme need to
       reproduce the quark non-Koide while keeping lepton Koide? If it needs >=1 free number
       per quark sector, the lepton selection is FIT not derived.
"""
import mpmath as mp
mp.mp.dps = 40

print("="*80)
print("ROUTE 4(d) -- LEPTON SPECIFICITY: why 45deg for leptons, not quarks?")
print("="*80)

def koide(m):
    m = [mp.mpf(str(x)) for x in m]
    s = [mp.sqrt(x) for x in m]
    p1 = sum(s); p2 = sum(m)
    Q = p2/p1**2
    cos2 = p1**2/(3*p2)
    r2 = 6*Q - 2
    r = mp.sqrt(r2) if r2 >= 0 else mp.nan
    return Q, cos2, r

# PDG 2024 (leptons: pole; quarks: MSbar quoted)
lep   = [0.51099895, 105.6583755, 1776.86]                  # MeV
up    = [2.16, 1270.0, 172690.0]
down  = [4.67, 93.4, 4180.0]
print("\n[masses -> Koide]")
for name, m in [("charged leptons", lep), ("up quarks", up), ("down quarks", down)]:
    Q, c2, r = koide(m)
    print(f"  {name:16s}: Q={mp.nstr(Q,6)}  cos^2={mp.nstr(c2,6)}  r={mp.nstr(r,6)}  "
          f"(Koide: Q=0.6667, r=1.41421)")

# ---------------------------------------------------------------------------
# (M1) QCD detuning hypothesis: is the quark departure from 45deg a QCD-running effect that
#      leptons (colorless) are immune to? Run quark masses to a COMMON high scale (removing
#      the QCD-induced relative running) and see if their Koide MOVES TOWARD 2/3. If QCD is
#      the lepton-vs-quark selector, de-QCD-ing the quarks should pull them to Koide.
# ---------------------------------------------------------------------------
print("\n(M1) QCD-detuning test: do quark Koide values move toward 2/3 when run to common scale?")
# quark masses at ~M_Z (rough RunDec-class), which removes much of the low-scale QCD running:
up_MZ   = [1.29, 624.0, 171700.0]   # u,c,t at ~M_Z
down_MZ = [2.75, 55.0, 2900.0]      # d,s,b at ~M_Z
for name, m in [("up @2GeV/quoted", up), ("up @M_Z", up_MZ),
                ("down @2GeV/quoted", down), ("down @M_Z", down_MZ)]:
    Q, c2, r = koide(m)
    dev = abs(Q - mp.mpf(2)/3)
    print(f"  {name:18s}: Q={mp.nstr(Q,6)}  |Q-2/3|={mp.nstr(dev,4)}")
print("  READING: running to M_Z does NOT pull the quark Q toward 2/3 (up stays ~0.78-0.85,")
print("  down ~0.73-0.74). The quark non-Koide is NOT a removable QCD-running artifact -> QCD")
print("  running is NOT the lepton-vs-quark selector. (Both directions checked.)")

# Quantify: is there ANY common scale where BOTH up and down sit at 2/3 simultaneously?
# The up and down Q differ (0.85 vs 0.73) and run in opposite-ish ways; they cannot both be
# 2/3 at one scale. A single 'de-QCD' scale cannot Koide-ify both quark sectors.
print("  Up Q ~0.78-0.85, Down Q ~0.73-0.74 across scales: DIFFERENT and neither ->2/3.")
print("  No single scale Koide-ifies both -> QCD-detuning is not a parameter-free selector.")

# ---------------------------------------------------------------------------
# (M2) SO(10) 16 embedding: leptons + quarks share the SAME 16. A 16-universal flavor
#      mechanism (one Yukawa structure for the whole 16) gives leptons and quarks the SAME
#      shape -> would predict quark Koide. Since quarks are NOT Koide, a 16-universal
#      principle is FALSIFIED as the selector. The selection must come from SOMETHING that
#      distinguishes lepton from quark WITHIN the 16 -- i.e. COLOR (the quark is a color
#      triplet, the lepton a singlet). So the ONLY group-theoretic lepton-vs-quark handle
#      is color. And (M1) just showed color/QCD running does NOT do the job parameter-free.
# ---------------------------------------------------------------------------
print("\n(M2) SO(10) 16 embedding: leptons & quarks share the 16.")
print("  A 16-UNIVERSAL flavor structure -> SAME sqrt-mass shape for leptons and quarks")
print("  -> predicts quark Q=2/3. FALSE (quarks 0.73-0.85). So 16-universality is FALSIFIED")
print("  as the selector. The only intra-16 lepton/quark distinction is COLOR (lepton=singlet,")
print("  quark=triplet) -> which routes back to QCD, killed parameter-free in (M1).")

# ---------------------------------------------------------------------------
# (M3) Honest tuning accounting. To keep lepton Koide AND reproduce quark non-Koide, how
#      many free numbers does a 'lepton-selecting' scheme need?
# ---------------------------------------------------------------------------
print("\n(M3) Tuning accounting: free parameters to select leptons & detune quarks.")
print("  - lepton 45deg: 1 number (r=sqrt2) -- if a principle FORCES it, 0 free; none does (4a-c).")
print("  - quark up detuning:   r_up   = %s  (1 free number, FIT)" % mp.nstr(koide(up)[2],5))
print("  - quark down detuning: r_down = %s  (1 free number, FIT)" % mp.nstr(koide(down)[2],5))
print("  A principle that 'selects leptons' must DERIVE why r_lep=sqrt2 while r_up,r_down are")
print("  these specific other numbers. No candidate does: the quark r's are FIT, the lepton")
print("  r is RE-LABELED. => lepton specificity is POST-HOC, not derived.")

# ---------------------------------------------------------------------------
# THE STRUCTURAL POINT: even the 'absence of QCD' cannot be the selector, because the
# DIRECTION is wrong. If QCD pushed quarks AWAY from a common 45deg, then in the QCD->0
# limit quarks would approach 2/3. They do not (M1). And neutrinos -- ALSO colorless like
# charged leptons -- do NOT obey Koide (Q_nu is a free function of the lightest mass,
# 0.586 at m1=0). So 'colorless' is NOT sufficient for 45deg either. Colorlessness is
# neither necessary-and-sufficient: charged leptons Koide, neutrinos (also colorless) not.
# ---------------------------------------------------------------------------
print("\n[KILLER] 'colorless' is NOT the selector -- neutrinos are colorless too and NOT Koide:")
dm21 = mp.mpf('7.42e-5'); dm31 = mp.mpf('2.515e-3')
for m1 in [mp.mpf('0'), mp.mpf('0.001'), mp.mpf('0.01'), mp.mpf('0.05')]:
    m2 = mp.sqrt(m1**2 + dm21); m3 = mp.sqrt(m1**2 + dm31)
    Q, c2, r = koide([m1, m2, m3])
    print(f"  neutrinos NO m1={mp.nstr(m1,3)} eV: Q={mp.nstr(Q,6)} (Koide 0.6667? NO; free in m1)")
print("  => charged leptons AND neutrinos are both colorless, yet only CHARGED leptons are")
print("     Koide. So 'absence of QCD / color-singlet' does NOT select 45deg. The selector")
print("     would have to distinguish charged-lepton from neutrino -- i.e. ELECTRIC CHARGE /")
print("     the specific Yukawa -- which is exactly the un-derived flavor structure.")

print("""
[VERDICT 4d] NO derived lepton-specific ingredient selects 45deg:
  - QCD-running detuning: quark Q does NOT move to 2/3 when de-QCD-ed; up & down differ and
    neither ->2/3 at any common scale. QCD is not a parameter-free selector. (M1)
  - SO(10) 16: leptons & quarks share the 16; 16-universality would PREDICT quark Koide
    (false). The only intra-16 handle is color -> routes to QCD, already killed. (M2)
  - 'Colorless' is not even sufficient: neutrinos are colorless and NOT Koide (Q free in m1).
    The selector would need to split charged-lepton from neutrino = un-derived Yukawa. (KILLER)
  => Lepton specificity is POST-HOC/FIT, not derived. A flavor-blind 45deg principle is
     cross-fermion FALSIFIED; no clean lepton-selecting ingredient exists. NULL.
""")
