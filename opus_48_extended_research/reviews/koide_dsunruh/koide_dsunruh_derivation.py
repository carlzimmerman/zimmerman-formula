#!/usr/bin/env python3
"""
ROUTE A: can the framework's dS-Unruh mechanism DERIVE Koide Q=2/3 (r=sqrt2 / 45deg)?
Sumino IR radiative cancellation supplied by the de Sitter-Unruh background.

BOTH WAYS + QUARANTINE:
 - a "derivation" is VALID only if (1) FORCED (does NOT input 2/3 or r=sqrt2 by hand),
   and (2) passes CROSS-FERMION (lepton-specific; must NOT give 2/3 for quarks/neutrinos).
 - a0/Z/kappa never asserted derived. Q=2/3 must not be smuggled.

This script confronts the dS-Unruh kernel against the THREE Sumino requirements,
verbatim from arXiv:0903.3640 / 0812.2103 (WebFetch'd this session):
  R1. cancel the QED log shift  +3alpha/(8pi) * (-log m_i^2) in sqrt(m_i)  [size ~0.1% in Q]
  R2. with an OPPOSITE-SIGN, SAME-LOG-SHAPE family correction obeying alpha_F ~= 4 alpha
  R3. lepton-specific (conjugate U(3) reps for psi_L vs e_R), NOT quarks/neutrinos.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 50

print("="*78)
print("ROUTE A: dS-Unruh -> Sumino IR cancellation -> Koide Q=2/3 ?")
print("="*78)

# ---------------------------------------------------------------------------
# 0. EXPERIMENTAL ANCHOR (PDG, MeV). The 2/3 we must EXPLAIN, not input.
# ---------------------------------------------------------------------------
me  = mp.mpf("0.51099895000")
mmu = mp.mpf("105.6583755")
mta = mp.mpf("1776.86")
def Q_of(m1,m2,m3):
    s = m1+m2+m3
    r = mp.sqrt(m1)+mp.sqrt(m2)+mp.sqrt(m3)
    return s/r**2
Qpole = Q_of(me,mmu,mta)
# angle of sqrt-mass vector to (1,1,1):  Q = 1/(2 cos^2 theta), cos^2=(v.n)^2/(|v|^2|n|^2)
_v = [mp.sqrt(me),mp.sqrt(mmu),mp.sqrt(mta)]
cos2 = (sum(_v))**2/((sum(x*x for x in _v))*3)   # Foot's cos^2 theta to (1,1,1) = 1/2 at Q=2/3
theta = mp.acos(mp.sqrt(cos2))*180/mp.pi          # = 45 deg
# Koide amplitude r in sqrt(m_i) = M(1 + r cos(2pi i/3 + delta)): Q = 1/3 + r^2/6 => r=sqrt(6Q-2)
r_amp = mp.sqrt(6*Qpole-2)
print(f"\n[anchor] Q_pole (PDG)      = {mp.nstr(Qpole,10)}   (2/3 = {mp.nstr(mp.mpf(2)/3,10)})")
print(f"[anchor] angle to (1,1,1)  = {mp.nstr(theta,8)} deg   (Foot: exactly 45)")
print(f"[anchor] Koide amplitude r = {mp.nstr(r_amp,10)}     (sqrt2 = {mp.nstr(mp.sqrt(2),10)})")
print(f"[anchor] Q=1/3+r^2/6 identity: ONLY r matters, NOT the phase delta (sympy below)")

# ---------------------------------------------------------------------------
# 1. THE Q=1/3+r^2/6 IDENTITY (sympy-exact): the unforced content is r alone.
# ---------------------------------------------------------------------------
print("\n" + "-"*78)
print("1. SYMPY: Q depends ONLY on the amplitude r, never the circulant phase delta")
print("-"*78)
M, r, d, i = sp.symbols('M r delta i', positive=True)
# Koide circulant ansatz sqrt(m_i)=M(1+r cos(2pi i/3 + delta))
sm = [M*(1+r*sp.cos(2*sp.pi*k/3 + d)) for k in (1,2,3)]
mass = [s**2 for s in sm]
Qsym = sp.simplify(sum(mass)/sum(sm)**2)
Qsym = sp.simplify(sp.trigsimp(Qsym))
print(f"   Q(r,delta) simplifies to: {Qsym}")
print(f"   -> phase delta CANCELS. Q = 1/3 + r^2/6 exactly.")
Qr = sp.Rational(1,3)+r**2/6
print(f"   check 1/3+r^2/6 == Q? {sp.simplify(Qsym-Qr)==0}")
r_for_23 = sp.solve(sp.Eq(Qr, sp.Rational(2,3)), r)
print(f"   Q=2/3  <=>  r = {r_for_23}  (= sqrt2).  So DERIVING Koide == DERIVING r=sqrt2.")

# ---------------------------------------------------------------------------
# 2. SUMINO REQUIREMENT R1: the QED log shift that must be cancelled.
#    sqrt(m_i^pole) gets a flavor-dependent (3alpha/8pi)*log(m_i) tilt that
#    rotates the sqrt-mass vector off 45deg by ~0.1% in Q.
# ---------------------------------------------------------------------------
print("\n" + "-"*78)
print("2. SUMINO R1: size of the QED radiative tilt that breaks Q=2/3")
print("-"*78)
alpha = mp.mpf(1)/mp.mpf("137.035999084")
# 1-loop pole mass: m_pole = mbar[1 + (alpha/pi){3/4 log(mu^2/mbar^2)+1}]
# the Koide-breaking piece is the mass-DEPENDENT log: delta sqrt(m)/sqrt(m) ~ (3alpha/8pi) log(...)
# Numerically: undo a (3alpha/8pi)log(m_i^2/mu^2) tilt and watch Q move.
mu = mp.mpf("1000.0")  # MeV reference scale (any; the tilt is what matters)
def sqrt_tilt(m, coeff):
    # sqrt(m) -> sqrt(m)*(1 + coeff * log(m/mu))   (schematic Sumino-shape, per-flavor log)
    return mp.sqrt(m)*(1+coeff*mp.log(m/mu))
def Q_from_sqrts(s1,s2,s3):
    s = s1*s1+s2*s2+s3*s3
    r = s1+s2+s3
    return s/r**2
c_qed = 3*alpha/(8*mp.pi)
sQ = [sqrt_tilt(m, -c_qed) for m in (me,mmu,mta)]   # remove QED -> "underlying" sqrt masses
Q_underlying = Q_from_sqrts(*sQ)
print(f"   QED log coeff 3alpha/(8pi) = {mp.nstr(c_qed,6)}  (~{mp.nstr(c_qed*100,4)} %)")
print(f"   Q with a (3a/8pi)*log per-flavor tilt undone: {mp.nstr(Q_underlying,10)}")
print(f"   shift in Q from the tilt: {mp.nstr(Q_underlying-Qpole,4)}  (Sumino: ~0.1% scale)")
print(f"   => to PIN Q=2/3 you must CANCEL a per-flavor log of coefficient ~3alpha/8pi={mp.nstr(c_qed,5)}")

# ---------------------------------------------------------------------------
# 3. SUMINO REQUIREMENT R2/R3: the cancellation needs an OPPOSITE-SIGN, SAME-LOG
#    family correction with alpha_F ~= 4 alpha, from CONJUGATE U(3) reps.
#    Question: can dS-Unruh supply a log-shaped, opposite-sign, family correction?
# ---------------------------------------------------------------------------
print("\n" + "-"*78)
print("3. CAN dS-Unruh SUPPLY the Sumino correction? (magnitude / shape / coupling)")
print("-"*78)
# dS-Unruh effective temperature (Deser-Levin): T_eff=(hbar/2pi c kB) sqrt(a^2+(cH)^2)
# rest-frame floor energy: E0 = hbar H_Lambda / (2pi)  (the a->0 dS Gibbons-Hawking quantum)
hbar = mp.mpf("1.054571817e-34"); c=mp.mpf("299792458"); kB=mp.mpf("1.380649e-23")
H0   = mp.mpf("2.18e-18")          # s^-1  (H_Lambda ~ 67 km/s/Mpc * sqrt(OmegaL))
cH   = c*H0
a0   = mp.mpf("9.36e-11")          # m/s^2 framework
# dS floor energy quantum (rest frame, a=0): E_floor = hbar*cH/(c) ... in energy: hbar*H0
E_floor_J = hbar*H0/(2*mp.pi)      # most conservative: the 1/2pi Unruh prefactor
E_floor_eV = E_floor_J/mp.mpf("1.602176634e-19")
me_eV = me*mp.mpf("1e6")
dS_frac = E_floor_eV/me_eV
print(f"   dS-Unruh rest floor   E0 = hbar H/(2pi) = {mp.nstr(E_floor_eV,4)} eV")
print(f"   electron mass         m_e             = {mp.nstr(me_eV,6)} eV")
print(f"   dS fractional shift   E0/m_e c^2       = {mp.nstr(dS_frac,4)}")
print(f"   REQUIRED Sumino coeff 3alpha/8pi       = {mp.nstr(c_qed,4)}")
gap = mp.log10(c_qed/dS_frac)
print(f"   MAGNITUDE GAP (orders of 10): log10(req/dS) = {mp.nstr(gap,5)}")
# steelman: drop the 1/2pi, use E0 = hbar H (bigger by 2pi); still:
E_floor_eV2 = (hbar*H0/mp.mpf("1.602176634e-19"))
gap2 = mp.log10(c_qed/(E_floor_eV2/me_eV))
print(f"   steelman (drop 1/2pi): gap = {mp.nstr(gap2,5)} orders  (still astronomically short)")

# ---------------------------------------------------------------------------
# 4. CROSS-FERMION FALSIFICATION: does the SAME mechanism wrongly give 2/3
#    for quarks / neutrinos? (a derivation that does is REFUTED.)
# ---------------------------------------------------------------------------
print("\n" + "-"*78)
print("4. CROSS-FERMION: do quarks / neutrinos obey Koide Q=2/3? (must be NO)")
print("-"*78)
# up-type quarks (MSbar 2GeV-ish / pole, MeV); down-type; charged leptons already 2/3
up   = [mp.mpf("2.16"), mp.mpf("1270"), mp.mpf("172760")]      # u,c,t
down = [mp.mpf("4.67"), mp.mpf("93.4"), mp.mpf("4180")]        # d,s,b
lep  = [me,mmu,mta]
# neutrinos: normal ordering, m1~0, dm21^2, dm31^2 (eV^2)
dm21 = mp.mpf("7.42e-5"); dm31 = mp.mpf("2.515e-3")
nu_NO = [mp.mpf("0.0"), mp.sqrt(dm21), mp.sqrt(dm31)]          # eV, m1=0
nu_NO_m1 = [mp.mpf("0.01"), mp.sqrt(mp.mpf("0.01")**2+dm21), mp.sqrt(mp.mpf("0.01")**2+dm31)]
for name, trip in [("charged leptons (e,mu,tau)",lep),
                   ("up quarks (u,c,t)",up),
                   ("down quarks (d,s,b)",down),
                   ("neutrinos NO m1=0 (eV)",nu_NO),
                   ("neutrinos NO m1=0.01 (eV)",nu_NO_m1)]:
    q = Q_of(*trip)
    flag = "  <-- ~2/3" if abs(q-mp.mpf(2)/3)<mp.mpf("0.01") else ""
    print(f"   Q({name:32s}) = {mp.nstr(q,7)}{flag}")
print("   => ONLY charged leptons hit 2/3. A mechanism that gives 2/3 for ALL is REFUTED.")
print("   => Sumino's conjugate-rep / QED-charge structure is INTRINSICALLY lepton-specific.")

# ---------------------------------------------------------------------------
# 5. DOES dS-Unruh CARRY the lepton-specific QED-charge structure? (the crux)
# ---------------------------------------------------------------------------
print("\n" + "-"*78)
print("5. CRUX: does dS-Unruh single out charged leptons the way Sumino's QED-cancel does?")
print("-"*78)
print("   Sumino's specificity SOURCE = QED electric charge (the thing being cancelled) +")
print("   the conjugate U(3) assignment of psi_L vs e_R (only invariant operator).")
print("   dS-Unruh T_eff couples to PROPER ACCELERATION |a| (universal, equivalence principle),")
print("   carries NO electric-charge / no-family-rep structure -> it is FLAVOR-BLIND and")
print("   CHARGE-BLIND. It cannot be the lepton-selective agent. (cross-fermion: it would")
print("   apply identically to quarks & neutrinos, which do NOT obey Koide -> would REFUTE.)")

print("\n" + "="*78)
print("SUMMARY of the four independent failure legs (each lethal):")
print(f"  L1 MAGNITUDE : dS floor / m_e = {mp.nstr(dS_frac,3)} vs needed {mp.nstr(c_qed,3)};"
      f" gap ~10^{mp.nstr(gap,4)}")
print( "  L2 COUPLING  : dS couples to classical |a|, ABSENT from the off-shell loop / gamma_m")
print( "  L3 SHAPE     : dS gives an ADDITIVE common-mode floor (1/m per-flavor), NOT QED's log")
print( "  L4 SELECTIVITY: dS is charge/flavor-BLIND; cannot select leptons; would hit quarks too")
print( "  + r=sqrt2 is the ENTIRE unforced content (Q=1/3+r^2/6) and nothing in the spine sets it")
print("="*78)
