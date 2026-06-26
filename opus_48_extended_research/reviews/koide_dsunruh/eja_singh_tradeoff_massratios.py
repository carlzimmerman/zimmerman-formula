import sympy as sp
import mpmath as mp
mp.mp.dps = 40
x, r, d, c, M, delta = sp.symbols('x r d c M delta', positive=True)

print("="*78)
print("(2b) RECONCILE: EJA's K=1/3+2d^2/9 vs standard Koide K=1/3+r^2/6")
print("="*78)
# Standard Brannen circulant: sqrt(m_i) = M(1 + r cos(2pi i/3 + phase)) -> K=1/3+r^2/6.
# EJA equally-spaced: s_i=(c-d,c,c+d) = c(1 + (d/c)*{-1,0,+1}).  The {-1,0,1} pattern
# is NOT cos(2pi i/3 + phase) [which gives values summing to 0 with specific spacing].
# But ANY symmetric-about-center triple s=(c-d,c,c+d) has Sum s_i = 3c, and
# Sum s_i^2 = 3c^2 + 2d^2.  So K = (3c^2+2d^2)/(9c^2) = 1/3 + 2d^2/(9c^2).
# Matching to standard r: the standard amplitude r for a triple (c-d,c,c+d):
# cos values would be {cos(phase-2pi/3),cos(phase),cos(phase+2pi/3)}; for the linear
# {-1,0,1} pattern there is NO single (r,phase) reproducing it as a cosine triple in
# general -- the EJA triple is a DIFFERENT (arithmetic, not circulant) ansatz.
# The Koide K is still well-defined from the masses. Equate K's:
# 1/3 + 2d^2/(9c^2) == 1/3 + r_eff^2/6  =>  r_eff^2 = (12/9)(d/c)^2 = (4/3)(d/c)^2
r_eff = sp.sqrt(sp.Rational(4,3))*(d/c)
print(f"  EJA triple (c-d,c,c+d): K = 1/3 + 2(d/c)^2/9")
print(f"  equivalent standard amplitude r_eff = sqrt(4/3)*(d/c) = (2/sqrt3)(d/c)")
for name, dd in [("Majorana d=sqrt(3/8), c=1", sp.sqrt(sp.Rational(3,8))),
                 ("Dirac    d=sqrt(3/2), c=1", sp.sqrt(sp.Rational(3,2)))]:
    re = sp.simplify(r_eff.subs({d:dd, c:1}))
    print(f"    {name}: r_eff = {sp.nsimplify(re)} = {sp.N(re,20)}  (Koide-2/3 needs r=sqrt2={sp.N(sp.sqrt(2),20)})")
print("  => Dirac d=sqrt(3/2) gives r_eff = sqrt2 EXACTLY (the 45-deg / Koide point).")
print("     sympy check r_eff(Dirac)^2 == 2 ?", sp.simplify(r_eff.subs({d:sp.sqrt(sp.Rational(3,2)),c:1})**2 - 2)==0)

print("\n" + "="*78)
print("(4) THE TRADEOFF -- mass ratios from EACH delta vs PDG (mpmath dps=40)")
print("="*78)
# PDG charged-lepton masses (MeV)
me  = mp.mpf("0.51099895000"); mmu = mp.mpf("105.6583755"); mta = mp.mpf("1776.86")
sqrt_mu_e_exp  = mp.sqrt(mmu/me);  sqrt_ta_e_exp = mp.sqrt(mta/me)
print(f"  PDG sqrt(m_mu/m_e) = {mp.nstr(sqrt_mu_e_exp,8)}   sqrt(m_tau/m_e) = {mp.nstr(sqrt_ta_e_exp,8)}")
# Singh's electron-family eigenvalues are charge-1/3 set: (1/3 - d, 1/3, 1/3 + d).
# His root-mass ratios (Eq.53,54) use products of eigenvalue ratios. Reproduce his
# stated formulae literally:
#   mu/e  : [ (1/3+d)/|1/3-d| ] * [ (largest)/(smallest) of charge-1 set = (1+d)/(1-d) ]   (Eq.53)
#   tau/e : that * (1+d)/(1-d) again  (Eq.54: square of strange/down * ratio)
def ratios(dval):
    d_ = mp.mpf(str(dval)) if not isinstance(dval,mp.mpf) else dval
    e_small = abs(mp.mpf(1)/3 - d_); e_mid = mp.mpf(1)/3; e_big = mp.mpf(1)/3 + d_
    # charge-1 (down) family set: (1-d,1,1+d)
    q1_small = mp.mpf(1)-d_; q1_big = mp.mpf(1)+d_
    sd = q1_big/q1_small                      # strange/down root-ratio
    mu_e  = (e_big/e_small) * sd              # Eq.53 structure
    tau_e = (e_big/e_small) * sd * sd         # Eq.54 structure (extra sd)
    return mu_e, tau_e
for name, dd in [("MAJORANA sqrt(3/8)", mp.sqrt(mp.mpf(3)/8)),
                 ("DIRAC    sqrt(3/2)", mp.sqrt(mp.mpf(3)/2))]:
    mu_e, tau_e = ratios(dd)
    print(f"  {name}:  sqrt(m_mu/m_e)_th = {mp.nstr(mu_e,7)}  (PDG {mp.nstr(sqrt_mu_e_exp,7)}, dev {mp.nstr((mu_e/sqrt_mu_e_exp-1)*100,3)}%)")
    print(f"  {' '*len(name)}   sqrt(m_tau/m_e)_th = {mp.nstr(tau_e,7)}  (PDG {mp.nstr(sqrt_ta_e_exp,7)}, dev {mp.nstr((tau_e/sqrt_ta_e_exp-1)*100,3)}%)")

print("\n" + "="*78)
print("(Eq.62) Majorana predicted Koide value from the THREE charged-lepton sqrt-masses")
print("="*78)
# Build sqrt-masses for Majorana set as Singh does: sqrt(m_e)=1, sqrt(m_mu)=mu_e, sqrt(m_tau)=tau_e
for name, dd in [("MAJORANA sqrt(3/8)", mp.sqrt(mp.mpf(3)/8)),
                 ("DIRAC    sqrt(3/2)", mp.sqrt(mp.mpf(3)/2))]:
    mu_e, tau_e = ratios(dd)
    s = [mp.mpf(1), mu_e, tau_e]
    K = sum(si**2 for si in s)/(sum(s))**2
    print(f"  {name}: K(from predicted ratios) = {mp.nstr(K,8)}  (Singh Eq.62 Majorana=0.669163; exact 2/3={mp.nstr(mp.mpf(2)/3,8)})")
