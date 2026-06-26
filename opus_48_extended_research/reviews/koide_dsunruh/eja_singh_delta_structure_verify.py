import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*78)
print("FINAL VERIFICATION (Singh 2508.10131, Eqs.1-9 of the Koide appendix)")
print("="*78)
delta, k = sp.symbols('delta k', positive=True)

# Singh Eq.7: K = (3 + 2 delta^2)/9  for the symmetric triple (1-delta,1,1+delta) at k=1
K_sym = sp.Rational(3,1)  # placeholder
s = [1-delta, 1, 1+delta]
K7 = sp.simplify(sum(si**2 for si in s)/(sum(s))**2)
print(f"\nEq.7  K(delta) for (1-delta,1,1+delta) = {K7}   [Singh: (3+2 delta^2)/9]")
print(f"      == (3+2 delta^2)/9 ?  {sp.simplify(K7 - (3+2*delta**2)/9)==0}")

# Eq.8-9: at the unbroken Dirac point (delta/k)^2 = 3/2  =>  K = 2/3 EXACTLY
K_dirac = sp.simplify(K7.subs(delta, sp.sqrt(sp.Rational(3,2))))
print(f"\nEq.8-9 DIRAC/unbroken  delta^2=3/2 :  K = {K_dirac}  (EXACT 2/3 ? {K_dirac==sp.Rational(2,3)})")

# Post-breaking: delta^2 = 3/8 (Majorana set). The bare symmetric triple would give:
K_maj_bare = sp.simplify(K7.subs(delta, sp.sqrt(sp.Rational(3,8))))
print(f"       MAJORANA bare triple delta^2=3/8 :  K = {K_maj_bare}  ( = 5/12 = {sp.N(K_maj_bare,8)} )")

# But Singh's ACTUAL post-breaking lepton ladder (Eq.2) is NOT the bare symmetric triple:
# S = X*G,  T = X,  with X=(1+delta)/(1-delta), G=(1/3+delta)/(delta-1/3), delta=sqrt(3/8)
dval = mp.sqrt(mp.mpf(3)/8)
X = (1+dval)/(1-dval)
G = (mp.mpf(1)/3+dval)/(dval-mp.mpf(1)/3)
S = X*G; T = X
K_th = (1 + S**2 + (S*T)**2)/(1 + S + S*T)**2
print(f"\nEq.2-3 POST-BREAKING lepton ladder (S=XG,T=X, delta=sqrt(3/8)):")
print(f"       X=(1+d)/(1-d) = {mp.nstr(X,8)},  G=(1/3+d)/(d-1/3) = {mp.nstr(G,8)}")
print(f"       S = {mp.nstr(S,8)},  T = {mp.nstr(T,8)}")
print(f"       K_th = {mp.nstr(K_th,10)}   [Singh Eq.3: 0.669163]")

# PDG experimental
me=mp.mpf("0.51099895000"); mmu=mp.mpf("105.6583755"); mta=mp.mpf("1776.86")
Sx=mp.sqrt(mmu/me); Tx=mp.sqrt(mta/mmu)
Kexp=(1+Sx**2+(Sx*Tx)**2)/(1+Sx+Sx*Tx)**2
print(f"       K_exp(PDG) = {mp.nstr(Kexp,10)}   [Singh Eq.4: 0.666661]")
print(f"       overshoot dK = {mp.nstr(K_th-Kexp,4)}  (~{mp.nstr((K_th/Kexp-1)*100,3)}%)  [Singh: +0.38%]")

print("\n" + "="*78)
print("THE delta^2 = 3/2  -> 3/8 HALVING (Singh: 'symmetry breaking halves delta^2')")
print("="*78)
print(f"   unbroken (Dirac) charged-family  delta^2 = 3/2 = {sp.Rational(3,2)}")
print(f"   broken   (Majorana) charged-fam  delta^2 = 3/8 = {sp.Rational(3,8)}")
print(f"   ratio (3/2)/(3/8) = {sp.Rational(3,2)/sp.Rational(3,8)}  -> halving in delta is /2 in delta^2? ")
print(f"   sqrt(3/2)/sqrt(3/8) = {sp.sqrt(sp.Rational(3,2))/sp.sqrt(sp.Rational(3,8))} = 2  (delta itself HALVES: 3/2 = 4*(3/8))")

print("\n" + "="*78)
print("WHAT SELECTS delta (Singh's own logic):")
print("="*78)
print("  delta is NOT free and NOT chosen to fit 2/3. It is fixed by:")
print("   - the EJA characteristic eq + coassociativity => equally-spaced (q-d,q,q+d), delta^2=Sigma/...")
print("   - the NEUTRINO being Dirac (unbroken) vs Majorana (broken) -- a PHYSICAL property")
print("   - Dirac/unbroken: delta^2=3/2 => K=2/3 EXACT but lepton mass ratios WRONG (mu/e<0)")
print("   - Majorana/broken: delta^2=3/8 => mass ratios RIGHT (~0.4-2%) but K=0.66916 (off 0.38%)")
print("  Singh PICKS Majorana (3/8) because it fits the MEASURED ratios; 2/3-exact is sacrificed.")
