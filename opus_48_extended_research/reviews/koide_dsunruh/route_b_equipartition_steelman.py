#!/usr/bin/env python3
"""
ROUTE B -- STEELMAN: try HARDEST to FORCE r=sqrt(2) via 'equal partition'.

The one genuine geometric content of Koide is: Q=2/3 <=> |standard component|^2 =
|democratic component|^2 of the sqrt-mass vector (equal partition of the S3 trivial and
standard reps). r=sqrt(2) is EXACTLY the equal-partition point. If the framework's dS-Unruh
democratic thermal background forced EQUIPARTITION between the symmetric (trivial) and the
broken (standard) directions, that WOULD force r=sqrt(2) without inputting it.

We test this steelman rigorously and look for the cross-fermion escape.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 30

print("="*78)
print("ROUTE B STEELMAN -- can a dS-Unruh 'equipartition' principle FORCE equal partition?")
print("="*78)

r = sp.symbols('r', positive=True)
# equal partition: |std|^2 = |dem|^2  <=>  r^2/2 = 1  <=> r=sqrt(2). (from route_b_force_r)
print("""
The TARGET reframed: r=sqrt(2)  <=>  |standard|^2/|democratic|^2 = 1  (EQUAL PARTITION).
So forcing r=sqrt(2) == forcing equal energy/variance in the trivial vs standard S3 modes.
""")
eq_partition_r = sp.solve(sp.Eq(r**2/2, 1), r)
print("  equal partition r^2/2=1 -> r =", eq_partition_r, " = sqrt(2).  GOOD target restatement.")

print("""
STEELMAN ARGUMENT A (dS thermal equipartition):
  In a de Sitter / Unruh thermal bath every quadratic mode gets <E>=kT/2 (classical
  equipartition). If the sqrt-mass vector were a set of thermalized oscillator amplitudes
  with the trivial mode and the (2-dim) standard mode each carrying equal thermal energy,
  one might argue |dem|^2 = |std|^2.
RUTHLESS CHECK -- this FAILS three ways:
  (1) DIMENSION COUNT: the standard rep is 2-DIMENSIONAL, the trivial is 1-DIMENSIONAL.
      Genuine equipartition gives ENERGY proportional to the number of modes:
      E_std/E_dem = dim(std)/dim(trivial) = 2/1, i.e. |std|^2/|dem|^2 = 2, NOT 1.
      That gives r^2/2=2 -> r=2 -> Q=1/3+4/6=1, NOT 2/3.  So honest equipartition
      OVERSHOOTS: it predicts Q=1, the maximal-breaking point, not 2/3.""")
# show: equipartition by mode count -> r=2 -> Q=1
r_equi = sp.sqrt(2*sp.Rational(2,1))  # |std|^2/|dem|^2 = dim ratio 2 -> r^2/2=2 -> r=2
Q_equi = sp.Rational(1,3)+ (sp.sqrt(4))**2/6
print("      mode-count equipartition: |std|^2/|dem|^2 = 2 -> r=2 -> Q =", sp.Rational(1,3)+4/sp.Integer(6), "= 1  (WRONG, not 2/3)")
print("""  (2) PER-COMPONENT vs TOTAL: to get |std|^2=|dem|^2 you must instead demand equal energy
      PER REP (trivial total = standard total), i.e. treat the standard rep as ONE collective
      mode. That is a CHOICE (equipartition per irreducible block, ignoring its dimension) --
      not forced; the opposite choice (per real component) gives r=2. Two equally-'natural'
      equipartition conventions bracket the answer (r=sqrt2 vs r=2). NOT FORCED.
  (3) FERMION-BLIND (the killer): any equipartition argument from the dS bath is identical
      for leptons and quarks (same generation S3, same bath). It would give the SAME r for
      quarks. Data: quarks are NOT at r=sqrt(2) (route_b_cross_fermion: r=1.08..1.76).
      => CROSS-FERMION FALSIFIED. The dS bath cannot select charged leptons.
""")

print("STEELMAN ARGUMENT B (the kappa=1/2 -> 1/sqrt(kappa)=sqrt2 'holographic' hook):")
print("""  kappa=1/2 is the framework's holographic OUTSIDE fraction (rho_DE normalization). The
  coincidence 1/sqrt(kappa)=sqrt(2)=r is numerically exact. RUTHLESS:
   - kappa lives in the GRAVITY/dark-energy sector (a0=cH/Z normalization), and the banked
     KAPPA_FORCING result proves kappa is itself UNFORCEABLE and is the OUTSIDE fraction --
     it has no Yukawa/lepton content.
   - cross-sector transfer is exactly the FDR-dead move (gravity O(1) -> SM amplitude) that
     fails for every other transferred formula.
   - and it is fermion-blind: a single universal constant 1/sqrt(kappa) would set r for
     quarks too -> 2/3 for quarks (FALSE). CROSS-FERMION FALSIFIED.
  => coincidence, not derivation. (Banked; reconfirmed sympy-exact + cross-fermion-killed.)
""")

# Quantify the kappa coincidence look-elsewhere: how many simple O(1) framework numbers land
# within 0.5% of sqrt(2)?
import itertools
mp.mp.dps=20
Z = mp.sqrt(mp.mpf(32)/3*mp.pi)
pool = {'sqrt2_target':mp.sqrt(2),'1/sqrt(kappa)':mp.sqrt(2),'Z/4':Z/4,'sqrt(Z)/2':mp.sqrt(Z)/2,
        'sqrt(2/3)':mp.sqrt(mp.mpf(2)/3),'(8pi/3)^(1/4)/...':(8*mp.pi/3)**mp.mpf('0.25')/mp.mpf('1.585'),
        'pi/sqrt(5)':mp.pi/mp.sqrt(5),'4/pi*1.111':mp.mpf(4)/mp.pi*mp.mpf('1.111')}
print("  look-elsewhere: simple O(1) combos near sqrt(2)=1.41421:")
for k,v in pool.items():
    print(f"    {k:22s} = {mp.nstr(v,8):>10s}  (/sqrt2 = {mp.nstr(v/mp.sqrt(2),5)})")

print("""
STEELMAN VERDICT: every route to FORCE r=sqrt(2) either
  (i) overshoots (honest mode-count equipartition gives r=2/Q=1),
  (ii) is a convention choice (per-rep vs per-component), or
  (iii) is fermion-blind and CROSS-FERMION FALSIFIED (would give quarks 2/3 too),
or (iv) is a cross-sector numerical coincidence (1/sqrt(kappa)) with no lepton mechanism.
r=sqrt(2) STAYS FREE. The geometric route does NOT force it. (Banked status reconfirmed,
having tried the strongest equipartition steelman, both ways.)
""")
