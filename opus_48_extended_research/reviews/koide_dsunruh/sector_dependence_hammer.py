"""
KOIDE SECTOR-DEPENDENCE HAMMER  (the 6th, genuinely-distinct swing)
====================================================================
NEW QUESTION (distinct from the 5 prior nulls):
  Is Q(SECTOR) a FORCED FUNCTION of the sector's gauge quantum numbers
  (color N_c, hypercharge Y, weak isospin T3, electric charge Q_em,
   the SO(10) 16 embedding), so the WHOLE pattern
   {lepton 0.667, up 0.849, down 0.731, neutrino} is OUTPUT by ONE rule
   and leptons-2/3 is a DERIVED point (not a fitted one)?

DISCIPLINE:
  (1) any rule whose DEFINITION inputs 2/3 / Koide / c=6 is the 169th
      re-labeling => DEAD.  The rule must map quantum-numbers (defined
      WITHOUT Koide) -> the c/Q value, and PREDICT ALL FOUR sectors.
  (2) A real result = the quark Q's converge to a clean pattern (or 2/3)
      at a PRINCIPLED scale/scheme NOT chosen to make it work.
  (3) generic fit or single-sector rule = NULL.

mpmath dps>=30.
"""
import mpmath as mp
from mpmath import mpf, sqrt, mpf as MPF
import itertools

mp.mp.dps = 40

# ----------------------------------------------------------------------
# 1. MASSES (PDG 2024 central values).
#    Leptons: clean POLE masses (MeV).
#    Quarks:  up/charm/top are POLE-ish for c,t but u is MSbar(2GeV);
#             we will treat several schemes/scales below.
# ----------------------------------------------------------------------
# Charged leptons (pole, MeV) -- PDG, essentially exact
m_e   = mpf('0.51099895000')
m_mu  = mpf('105.6583755')
m_tau = mpf('1776.86')

# Up-type quarks (MeV). u,c MSbar(2GeV-ish) / c,t conventions vary; use PDG MSbar.
mu_u = mpf('2.16')      # MSbar(2 GeV)
mu_c = mpf('1270.0')    # MSbar(m_c)
mu_t = mpf('172570.0')  # pole ~172.57 GeV

# Down-type quarks (MeV), MSbar(2GeV) for d,s ; MSbar(m_b) for b
md_d = mpf('4.67')      # MSbar(2 GeV)
md_s = mpf('93.4')      # MSbar(2 GeV)
md_b = mpf('4180.0')    # MSbar(m_b)

def koide_Q(masses):
    s_lin = sum(masses)
    s_root = sum(sqrt(m) for m in masses)
    return s_lin / (s_root**2)

def c_of_Q(Q):
    # c = e1^2/e2 ; Q = (c-2)/c  =>  c = 2/(1-Q)
    return 2/(1 - Q)

print("="*70)
print("SECTOR Q AND c VALUES (PDG central, mixed schemes)")
print("="*70)
sectors = {
    'charged_leptons': [m_e, m_mu, m_tau],
    'up_quarks':       [mu_u, mu_c, mu_t],
    'down_quarks':     [md_d, md_s, md_b],
}
Qvals = {}
for name, ms in sectors.items():
    Q = koide_Q(ms)
    c = c_of_Q(Q)
    Qvals[name] = Q
    print(f"  {name:16s}  Q = {mp.nstr(Q,8):12s}  c = {mp.nstr(c,8):10s}")

# Neutrino sector: Q FREE in m1 (normal ordering). dm21^2, dm31^2 fixed.
print("\n  Neutrino Q is a FUNCTION of m1 (NO unique value):")
dm21sq = mpf('7.42e-5')   # eV^2
dm31sq = mpf('2.515e-3')  # eV^2 (normal ordering)
for m1 in [mpf('0'), mpf('0.001'), mpf('0.01'), mpf('0.05')]:
    m2 = sqrt(m1**2 + dm21sq)
    m3 = sqrt(m1**2 + dm31sq)
    Qn = koide_Q([m1, m2, m3])
    print(f"    m1={mp.nstr(m1,3):8s} eV ->  Q_nu = {mp.nstr(Qn,6)}  (c={mp.nstr(c_of_Q(Qn),5)})")
print("  => neutrino has NO forced Q. Any sector-rule must NOT predict a")
print("     unique neutrino Q (or it is instantly falsified).")

# ----------------------------------------------------------------------
# 2. GAUGE QUANTUM NUMBERS per sector (defined WITHOUT any reference to Koide)
#    Standard Model / SO(10) 16 embedding.
# ----------------------------------------------------------------------
# For the RIGHT-HANDED / mass-eigenstate fermion of each sector we tabulate:
#   N_c   = color multiplicity (3 for quarks, 1 for leptons)
#   Qem   = electric charge
#   T3    = weak isospin (left-handed component)
#   Y_L   = hypercharge of the LH doublet (Y = Q - T3 convention, GUT y_Q=1/6 pattern)
#   the SO(10) 16 weights are common to all (single irrep) -> NOT sector-distinguishing
QN = {
    # sector            N_c   Qem      T3_L    Y_Q(LH doublet, y_Q=1/6 pattern)
    'charged_leptons': dict(Nc=1, Qem=mpf('-1'),    T3=mpf('-1/2'), Yf=mpf('-1')),      # e_R: Y=-1
    'up_quarks':       dict(Nc=3, Qem=mpf('2/3'),   T3=mpf('1/2'),  Yf=mpf('2/3')),     # u_R: Y=+2/3
    'down_quarks':     dict(Nc=3, Qem=mpf('-1/3'),  T3=mpf('-1/2'), Yf=mpf('-1/3')),    # d_R: Y=-1/3
    'neutrinos':       dict(Nc=1, Qem=mpf('0'),     T3=mpf('1/2'),  Yf=mpf('0')),       # nu_R: Y=0
}
print("\n" + "="*70)
print("GAUGE QUANTUM NUMBERS (no Koide in any of these)")
print("="*70)
for s,d in QN.items():
    print(f"  {s:16s} Nc={d['Nc']}  Qem={mp.nstr(d['Qem'],4):7s} T3={mp.nstr(d['T3'],4):6s} Yf={mp.nstr(d['Yf'],4)}")

# ----------------------------------------------------------------------
# 3. THE TARGET c-values to be PREDICTED
# ----------------------------------------------------------------------
c_lep  = c_of_Q(Qvals['charged_leptons'])   # ~6.000
c_up   = c_of_Q(Qvals['up_quarks'])         # ~13.2
c_down = c_of_Q(Qvals['down_quarks'])       # ~7.45
print("\n" + "="*70)
print("TARGET c-values:  lep=%s  up=%s  down=%s" %
      (mp.nstr(c_lep,6), mp.nstr(c_up,6), mp.nstr(c_down,6)))
print("="*70)

# ----------------------------------------------------------------------
# 4. SEARCH: does a SIMPLE forced rule  c = f(Nc, Qem, T3, Yf)  with
#    SMALL-INTEGER / rational coefficients reproduce ALL THREE charged
#    sectors simultaneously?  (neutrino excluded because Q is free; but
#    we then CHECK what the rule predicts for the neutrino and demand it
#    NOT be a sharp falsified value.)
#
#    Honest test: c_lep is EXACTLY 6.  If a rule is forced, it must give
#    c=6 for leptons with the SAME coefficients that give 13.2 and 7.45.
#    We brute-force over low-complexity closed forms with rational/small
#    coefficients and count how many reproduce all 3 to within tolerance.
# ----------------------------------------------------------------------
print("\nSEARCH 1: linear rule  c = a + b*Nc + d*Qem + g*T3 + h*Yf")
print("  (require EXACT-ish fit to all 3 charged sectors; 3 eqns, but 5 coeffs)")

# With 5 free coefficients and only 3 equations, the linear system is
# UNDER-determined -> infinitely many exact fits exist.  That is the
# generic-fit trap.  The discipline: a FORCED rule must use FEWER
# coefficients than data points (predictive), and predict the neutrino.
# So restrict to <=2 coefficients (so 3 sectors => 1 prediction-residual,
# a genuine test), drawn from a SINGLE quantum number at a time.

import numpy as np

def fit_quality(coeffs_func, qnumber_key):
    """1-parameter or 2-parameter rules on a single quantum number."""
    pass

targets = {'charged_leptons': c_lep, 'up_quarks': c_up, 'down_quarks': c_down}

print("\nSEARCH 2: ONE-quantum-number rules with <=2 coeffs (PREDICTIVE: 3 data, <=2 params)")
print("  For each quantum number X in {Nc,Qem,T3,Yf,|Qem|,Qem^2,Nc*|Qem|,...}")
print("  fit c = A + B*X to the 3 charged sectors; report residual + neutrino prediction.\n")

# build derived quantum-number features (still Koide-free)
def features(s):
    d = QN[s]
    Nc, Qem, T3, Yf = d['Nc'], d['Qem'], d['T3'], d['Yf']
    return {
        'Nc':       mpf(Nc),
        'Qem':      Qem,
        '|Qem|':    abs(Qem),
        'Qem^2':    Qem**2,
        'T3':       T3,
        'Yf':       Yf,
        'Yf^2':     Yf**2,
        'Nc*Qem^2': Nc*Qem**2,
        'Nc*|Qem|': Nc*abs(Qem),
        'Nc+|Qem|': Nc+abs(Qem),
        '6Qem^2':   6*Qem**2,                 # the GUT-charge-squared scale
        'Nc/(|Qem|+1e-9)': Nc/(abs(Qem)+mpf('1e-9')),
        'dim_color_charge': mpf(Nc)*(1+abs(Qem)),
    }

charged = ['charged_leptons','up_quarks','down_quarks']
all_feats = {s: features(s) for s in list(QN.keys())}

leads = []
for feat in all_feats['charged_leptons'].keys():
    # 2-param linear fit c = A + B*X over 3 points  -> 1 residual dof
    xs = [all_feats[s][feat] for s in charged]
    ys = [targets[s] for s in charged]
    # least squares with mpmath via normal equations on 3 pts, 2 params
    # set up [1 x] design
    X = mp.matrix([[mpf(1), xs[0]],[mpf(1), xs[1]],[mpf(1), xs[2]]])
    Y = mp.matrix([ys[0], ys[1], ys[2]])
    XT = X.T
    try:
        beta = (XT*X)**-1 * (XT*Y)
        A, B = beta[0], beta[1]
        pred = [A + B*x for x in xs]
        resid = [abs(pred[i]-ys[i])/abs(ys[i]) for i in range(3)]
        max_resid = max(resid)
        # neutrino prediction
        xn = all_feats['neutrinos'][feat]
        c_nu_pred = A + B*xn
        Q_nu_pred = 1 - 2/c_nu_pred if c_nu_pred != 0 else None
        leads.append((feat, max_resid, A, B, c_nu_pred, Q_nu_pred))
    except Exception as ex:
        pass

leads.sort(key=lambda t: t[1])
print(f"{'feature':22s} {'max_resid':>12s} {'c_nu_pred':>12s} {'Q_nu_pred':>12s}")
for feat, mr, A, B, cnu, Qnu in leads:
    qstr = mp.nstr(Qnu,5) if Qnu is not None else 'NA'
    print(f"{feat:22s} {mp.nstr(mr,4):>12s} {mp.nstr(cnu,5):>12s} {qstr:>12s}")

print("\nNOTE: with 2 params on 3 points the BEST max_resid measures whether")
print("a single quantum number EXPLAINS the c-ordering. A forced rule needs")
print("max_resid ~ 0 (the 3rd point PREDICTED) AND integer/rational A,B.")

# ----------------------------------------------------------------------
# 5. THE SHARPEST FORCED CANDIDATE seen in folklore: c ~ related to Qem^2
#    Test the cleanest closed forms that have appeared:
#      c = 6 / (something)  ;  c_lep=6 exactly. Is 6 = N_c_lepton-related?
#      Foot/Koide folklore: Q_lepton=2/3, and 2/3 = |Qem_up| ... coincidence?
# ----------------------------------------------------------------------
print("\n" + "="*70)
print("SEARCH 3: closed-form 'clean' candidates (forced-looking)")
print("="*70)
# Candidate A: is c proportional to 1/<Qem^2> in some averaged sense?
for s in charged:
    d = QN[s]
    print(f"  {s:16s} c={mp.nstr(targets[s],6):10s}  Qem^2={mp.nstr(d['Qem']**2,5):8s} "
          f" Nc*Qem^2={mp.nstr(d['Nc']*d['Qem']**2,5):8s} "
          f" Nc/Qem^2={mp.nstr(d['Nc']/d['Qem']**2,6) if d['Qem']!=0 else 'inf'}")

print("\n  Is c_lep=6 == 6*Qem_lep^2 (Qem=-1)? 6*1=6  YES but trivial (Qem^2=1).")
print("  Then up: 6*Qem^2=6*(4/9)=2.67 (need 13.2) NO. down: 6*(1/9)=0.667 NO.")
print("  => '6*Qem^2' fits ONLY leptons (Qem^2=1). single-sector. DEAD as a law.")
