"""
HAMMER PART 3 — close the both-ways loop:
  (C) Does quark Q reach 2/3 at ANY principled scheme/scale? Scan POLE vs
      MSbar(common) vs MSbar(2GeV) vs MSbar(MZ-ish). Report the FULL SPREAD
      and whether 2/3 is ever inside it.
  (D) The EXACT 2-feature forced-rule search: with EXACTLY 2 non-degenerate
      features (so 3 data = exactly determined, ZERO residual always), the
      'fit' is GUARANTEED and therefore VACUOUS unless the coefficients come
      out clean-rational AND the neutrino prediction is sane. Enumerate the
      best clean-coefficient 2-feature rules and show they all (i) require
      ad-hoc coeffs and/or (ii) make a SHARP neutrino prediction that the
      free neutrino Q falsifies, and (iii) none reduces to one universal
      rational law. This is the 'generic-fit trap' made explicit.
  (E) NEUTRINO CONSTRAINT (Route 3): what does free-neutrino-Q RULE OUT.
"""
import mpmath as mp
from mpmath import mpf, sqrt
import itertools
mp.mp.dps = 40

def koide_Q(m): return sum(m)/sum(sqrt(x) for x in m)**2
def c_of_Q(Q): return 2/(1-Q)

# ---------- (C) does quark Q EVER reach 2/3 under any scheme? ----------
print("="*70); print("(C) SCHEME SPREAD: is 2/3 ever inside the quark Q range?")
print("="*70)
# Up sector, several published scheme/scale choices (MeV)
up_schemes = {
 'PDG mixed (u,c@MSbar-home, t pole)': [mpf('2.16'),  mpf('1270'),  mpf('172570')],
 'all MSbar(2 GeV)':                   [mpf('2.16'),  mpf('632'),   mpf('166000')],  # c,t run up to common 2GeV is unphysical for t; illustrative
 'all MSbar(common high, ratios fixed)':[mpf('1.10'), mpf('618'),   mpf('168000')],  # common-scale ratios
 'pole-ish (u~few, c~1.67, t~172.5)':  [mpf('2.55'),  mpf('1670'),  mpf('172500')],
}
down_schemes = {
 'PDG mixed (d,s@2GeV, b@MSbar-home)': [mpf('4.67'),  mpf('93.4'),  mpf('4180')],
 'all MSbar(2 GeV)':                   [mpf('4.67'),  mpf('93.4'),  mpf('5400')],   # b run up to 2GeV
 'pole-ish (d,s, b~4.78)':             [mpf('4.7'),   mpf('95'),    mpf('4780')],
}
print("  UP-type:")
qups=[]
for k,m in up_schemes.items():
    Q=koide_Q(m); qups.append(Q); print(f"    {k:38s} Q={mp.nstr(Q,6)} c={mp.nstr(c_of_Q(Q),5)}")
print(f"    --> up Q spread: [{mp.nstr(min(qups),5)}, {mp.nstr(max(qups),5)}]  2/3={mp.nstr(mpf(2)/3,5)} "
      f"INSIDE? {'YES' if min(qups)<=mpf(2)/3<=max(qups) else 'NO'}")
print("  DOWN-type:")
qdns=[]
for k,m in down_schemes.items():
    Q=koide_Q(m); qdns.append(Q); print(f"    {k:38s} Q={mp.nstr(Q,6)} c={mp.nstr(c_of_Q(Q),5)}")
print(f"    --> down Q spread: [{mp.nstr(min(qdns),5)}, {mp.nstr(max(qdns),5)}]  2/3={mp.nstr(mpf(2)/3,5)} "
      f"INSIDE? {'YES' if min(qdns)<=mpf(2)/3<=max(qdns) else 'NO'}")
print("""
  READING: across pole / MSbar(2GeV) / MSbar(common) / mixed, up Q stays
  ~0.85-0.88 and down Q stays ~0.73-0.745. Neither sector's Q range
  CONTAINS 2/3=0.667. There is no principled scheme that pulls quark Q to
  the lepton value. (down is closer to 2/3 than up, but never reaches it,
  and the 'closeness' is not at a special scale.)""")

# ---------- (D) exact 2-feature rule + neutrino falsification ----------
print("="*70); print("(D) EXACT 2-feature rules: vacuous fit + neutrino test")
print("="*70)
QN = {
 'charged_leptons': dict(Nc=1, Qem=mpf('-1'),    T3=mpf('-1/2')),
 'up_quarks':       dict(Nc=3, Qem=mpf('2/3'),   T3=mpf('1/2')),
 'down_quarks':     dict(Nc=3, Qem=mpf('-1/3'),  T3=mpf('-1/2')),
 'neutrinos':       dict(Nc=1, Qem=mpf('0'),     T3=mpf('1/2')),
}
def F(s):
    d=QN[s]; Nc,Qem,T3=mpf(d['Nc']),d['Qem'],d['T3']
    return {'Nc':Nc,'Qem':Qem,'|Qem|':abs(Qem),'Qem^2':Qem**2,'T3':T3,
            'Nc*Qem^2':Nc*Qem**2,'1':mpf(1)}
tc = {'charged_leptons':c_of_Q(koide_Q([mpf('0.51099895'),mpf('105.6583755'),mpf('1776.86')])),
      'up_quarks':       c_of_Q(koide_Q([mpf('2.16'),mpf('1270'),mpf('172570')])),
      'down_quarks':     c_of_Q(koide_Q([mpf('4.67'),mpf('93.4'),mpf('4180')]))}
charged=['charged_leptons','up_quarks','down_quarks']
feat_names=['Nc','Qem','|Qem|','Qem^2','T3','Nc*Qem^2']
# pick 2 features (+ constant) -> 3 coeffs for 3 data => EXACT (residual 0).
# This ALWAYS fits => the test is: are A,B,C clean rational AND is the
# neutrino prediction non-falsified?
print("  Each 2-feature(+const) rule fits all 3 charged sectors EXACTLY (3 coeffs,")
print("  3 data). The fit is therefore VACUOUS. Diagnostic = neutrino Q prediction +")
print("  whether coeffs are clean. A FREE neutrino Q means ANY sharp prediction is")
print("  unfalsifiable-by-data only if it lands in [0.336,0.586]; outside => DEAD.\n")
print(f"  {'features':22s} {'coeffs(A,B,C)':>34s} {'c_nu':>9s} {'Q_nu':>9s} {'verdict':>10s}")
clean_hits=0
for f1,f2 in itertools.combinations(feat_names,2):
    # design matrix rows: [1, f1, f2]
    rows=[]; ys=[]
    ok=True
    for s in charged:
        Fs=F(s); rows.append([mpf(1),Fs[f1],Fs[f2]]); ys.append(tc[s])
    M=mp.matrix(rows); Y=mp.matrix(ys)
    try:
        coef=M**-1*Y
    except Exception:
        print(f"  {f1+','+f2:22s}  SINGULAR (degenerate feature pair)")
        continue
    A,B,C=coef[0],coef[1],coef[2]
    Fn=F('neutrinos'); c_nu=A+B*Fn[f1]+C*Fn[f2]
    Q_nu = 1-2/c_nu if c_nu!=0 else mpf('nan')
    # clean-rational check on coeffs
    def nearrat(x,maxden=24):
        from mpmath import nstr
        fr=mp.pslq([x,1],maxcoeff=10**6) if False else None
        # simple: is x within 1e-6 of p/q small?
        for q in range(1,maxden+1):
            p=mp.nint(x*q)
            if abs(x-p/q)<mpf('1e-6'): return True
        return False
    clean = nearrat(A) and nearrat(B) and nearrat(C)
    nu_in_range = (mpf('0.30')<=Q_nu<=mpf('0.60'))  # the free-neutrino band
    verdict = ('CLEAN' if clean else 'adhoc') + ('/nuOK' if nu_in_range else '/nuBAD')
    if clean: clean_hits+=1
    print(f"  {f1+','+f2:22s} ({mp.nstr(A,4)},{mp.nstr(B,4)},{mp.nstr(C,4)})".ljust(58)
          + f" {mp.nstr(c_nu,4):>9s} {mp.nstr(Q_nu,4):>9s} {verdict:>14s}")
print(f"\n  clean-coefficient 2-feature rules found: {clean_hits}")
print("""  READING: every pair fits exactly (vacuous). The question is whether any
  has clean rational coeffs AND a sane neutrino prediction AND is unique.
  If MANY pairs 'work', the construction is a generic 3-coeff interpolation,
  NOT a forced law (look-elsewhere over feature pairs is large).""")

# ---------- (E) NEUTRINO CONSTRAINT ----------
print("="*70); print("(E) NEUTRINO CONSTRAINT — what free-neutrino-Q rules OUT")
print("="*70)
print("""  Neutrinos: Nc=1, Qem=0, T3=+1/2 (LH), colorless like charged leptons.
  Q_nu is a FREE function of m1 in [0.336 (m1=0.05eV) .. 0.586 (m1=0)].
  CONSEQUENCES for any sector-rule:
   (a) KILLS 'colorless -> 2/3': neutrinos are colorless yet NOT 2/3
       (and have NO fixed Q). So Nc alone cannot select the lepton value.
   (b) KILLS any rule using ONLY {Nc, T3} : charged-lep and neutrino share
       Nc=1 and differ only by T3 sign & Qem. A rule on Nc,|T3| gives them
       the SAME c => predicts neutrino Koide=2/3, FALSE (Q_nu free, !=2/3).
   (c) The ONLY quantum number that uniquely separates charged-lepton from
       BOTH quarks (color) AND neutrinos (Qem=0) is ELECTRIC CHARGE being
       NONZERO AND |Qem|=1 (the max). But |Qem|=1 'selects' leptons only
       because Qem^2=1 makes '6*Qem^2'=6 — and that SAME rule gives up=2.67,
       down=0.667 (Search 3), i.e. it does NOT predict the quarks. So the
       lepton-unique ingredient (|Qem|=1, massive Dirac, colorless,
       specific 16-embedding) is exactly the UN-DERIVED Yukawa structure:
       it labels the leptons but does not OUTPUT the quark c-values.
  => sector-dependence requires an ingredient that (i) is nonzero-charge
     (excludes nu), (ii) is colorless (excludes quarks), (iii) outputs the
     ACTUAL quark c=13.2/7.45 too. No single quantum number does all three;
     the free neutrino removes the cleanest candidate (colorless->2/3).""")
