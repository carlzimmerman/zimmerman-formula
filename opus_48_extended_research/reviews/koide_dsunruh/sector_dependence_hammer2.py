"""
HAMMER PART 2 — the two decisive sub-tests:
  (A) DEGENERACY AUDIT: many "good" single-feature fits are illusory
      because T3, Nc, etc. take only 2 distinct values across the 3
      charged sectors => a 2-param line through 2 distinct x-values
      ALWAYS hits 2 of 3 exactly and the 3rd is "predicted" only if it
      shares an x-value.  Expose which features are degenerate.
  (B) SCHEME/SCALE ANGLE: run the up/down quark Koide Q at a LADDER of
      common renormalization scales (MSbar running) and at POLE masses,
      to test whether quark Q converges to a clean pattern (or 2/3) at a
      PRINCIPLED scale.  Use 1-loop QCD mass running (analytic, mpmath).
"""
import mpmath as mp
from mpmath import mpf, sqrt, log, pi
mp.mp.dps = 40

# ----------------------------------------------------------------------
def koide_Q(masses):
    s_lin = sum(masses); s_root = sum(sqrt(m) for m in masses)
    return s_lin/(s_root**2)
def c_of_Q(Q): return 2/(1-Q)

# ---------- (A) DEGENERACY AUDIT ----------
print("="*70); print("(A) DEGENERACY AUDIT — distinct x-values across the 3 sectors")
print("="*70)
QN = {
 'charged_leptons': dict(Nc=1, Qem=mpf('-1'),    T3=mpf('-1/2')),
 'up_quarks':       dict(Nc=3, Qem=mpf('2/3'),   T3=mpf('1/2')),
 'down_quarks':     dict(Nc=3, Qem=mpf('-1/3'),  T3=mpf('-1/2')),
}
feats = {}
for s,d in QN.items():
    feats[s] = {'Nc':mpf(d['Nc']),'Qem':d['Qem'],'|Qem|':abs(d['Qem']),
                'Qem^2':d['Qem']**2,'T3':d['T3'],'Nc*|Qem|':d['Nc']*abs(d['Qem'])}
for f in feats['charged_leptons']:
    vals = [feats[s][f] for s in QN]
    nd = len(set(mp.nstr(v,10) for v in vals))
    flag = "  <-- DEGENERATE (only %d distinct => 2-param fit is vacuous/2-of-3)"%nd if nd<3 else ""
    print(f"  {f:10s}: {[mp.nstr(v,5) for v in vals]}  distinct={nd}{flag}")
print("""
  READING: any feature with <3 distinct values CANNOT predict the 3rd
  sector by a 2-param line — it either coincides (vacuous 0 residual on a
  shared point) or the fit is underdetermined. The earlier max_resid~0.12
  'best fits' (T3, Nc*|Qem|) are DEGENERATE (T3 has 2 distinct values;
  the up/down share Nc). They do NOT predict; they interpolate 2 points.
  The only NON-degenerate single features are Qem, |Qem|, Qem^2 (3 distinct)
  and their best max_resid was ~0.13-0.35 => NO single quantum number
  predicts the quark c-values from the lepton anchor.""")

# Honest restatement: a forced predictive rule needs <3 params for 3 data.
# Non-degenerate features all FAIL at the 13%+ level. So NO 1-feature law.

# ---------- (B) SCHEME / SCALE ANGLE ----------
print("="*70); print("(B) SCHEME/SCALE: quark Koide Q vs renormalization scale (1-loop QCD)")
print("="*70)
# 1-loop running mass: m(mu) = m(mu0) * (alpha_s(mu)/alpha_s(mu0))^(gamma0/beta0)
# gamma0 = 8 (mass anomalous dim, =2*4=8 in the conv where m~alpha^(gamma0/(2beta0)))
# Standard: m(mu)/m(mu0) = (a_s(mu)/a_s(mu0))^(4/beta0), beta0 = 11 - 2/3 nf.
# alpha_s 1-loop: a_s(mu) = a_s(MZ)/(1 + a_s(MZ)*beta0/(2pi)*ln(mu/MZ))
MZ   = mpf('91187.6')      # MeV
asMZ = mpf('0.1180')

def nf_of(mu):
    # number of active flavors by threshold (MeV)
    if mu < mpf('1270'):   return 3
    if mu < mpf('4180'):   return 4
    if mu < mpf('172570'): return 5
    return 6

def alpha_s(mu):
    # crude 1-loop with fixed nf=5 from MZ down to ~mb, then nf=4,3 (piecewise)
    # for the purpose of SCHEME test we use a single effective nf=5 line (the
    # qualitative scale dependence is what matters, not 0.1% precision).
    nf = 5
    beta0 = 11 - mpf(2)/3*nf
    return asMZ/(1 + asMZ*beta0/(2*pi)*log(mu/MZ))

def run_mass(m_ref, mu_ref, mu, nf=5):
    beta0 = 11 - mpf(2)/3*nf
    return m_ref * (alpha_s(mu)/alpha_s(mu_ref))**(mpf(4)/beta0)

# reference MSbar masses at their "home" scales
refs_up   = {'u':(mpf('2.16'),mpf('2000')), 'c':(mpf('1270'),mpf('1270')), 't':(mpf('172570'),mpf('172570'))}
refs_down = {'d':(mpf('4.67'),mpf('2000')), 's':(mpf('93.4'),mpf('2000')),  'b':(mpf('4180'),mpf('4180'))}

print("\n  Common-scale MSbar(mu) Koide Q for up & down sectors:")
print(f"  {'mu(GeV)':>10s} {'Q_up':>12s} {'c_up':>10s} {'Q_down':>12s} {'c_down':>10s}")
for muGeV in ['2','5','10','100','1000','10000','172570','1e6','1e9','1e12','1e15']:
    mu = mpf(muGeV) if 'e' not in muGeV else mpf(muGeV)
    if float(muGeV) < 1000:  # interpret <1000 as GeV, else as MeV-ish big scales
        mu = mpf(muGeV)*1000  # GeV->MeV
    else:
        mu = mpf(muGeV)       # already large (MeV)
    up = [run_mass(*refs_up[q], mu) for q in ('u','c','t')]
    dn = [run_mass(*refs_down[q], mu) for q in ('d','s','b')]
    Qu, Qd = koide_Q(up), koide_Q(dn)
    print(f"  {muGeV:>10s} {mp.nstr(Qu,6):>12s} {mp.nstr(c_of_Q(Qu),5):>10s} "
          f"{mp.nstr(Qd,6):>12s} {mp.nstr(c_of_Q(Qd),5):>10s}")

print("""
  READING (scheme angle): common-mass-scale running multiplies ALL three
  masses in a sector by the SAME factor (4/beta0 power of the same a_s
  ratio) — but Koide Q is NOT scale-invariant because the masses run by
  the SAME multiplicative factor ONLY at 1-loop with EQUAL anomalous
  dimensions, which they have. A COMMON multiplicative rescaling
  m_i -> lambda*m_i leaves Q EXACTLY invariant (Q is degree-0 homogeneous:
  numerator ~lambda, denominator ~lambda). So 1-loop common running does
  NOT move Q at all. Verify:""")

# Q is homogeneous degree 0 -> invariant under common rescale. Prove:
lam = mpf('3.7')
base = [mpf('2.16'),mpf('1270'),mpf('172570')]
print("   Q(up) unscaled =", mp.nstr(koide_Q(base),10))
print("   Q(up)*lambda   =", mp.nstr(koide_Q([lam*x for x in base]),10), " (IDENTICAL => Q scale-inv)")
print("""
  => The quark non-Koide is NOT a common-running artifact. The masses run
  with the SAME multiplicative QCD factor (flavor-blind anomalous dim) =>
  Q is EXACTLY unchanged by changing the common MSbar scale. The ONLY way
  scheme could move Q is FLAVOR-DEPENDENT corrections (threshold/matching,
  m_q-dependent 2-loop), which are tiny for the heavy quarks that dominate
  Q. So 'quark non-Koide is a scheme artifact' is FALSE — Q_up=0.849,
  Q_down=0.731 are scheme-robust to leading order, NOT pulled to 2/3.""")
