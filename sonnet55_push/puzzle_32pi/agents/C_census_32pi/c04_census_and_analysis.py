#!/usr/bin/env python3
"""c04_census_and_analysis.py -- census lane C: the census as DATA, and the structural analysis.

The census table is machine-checked: every instance carries its coefficient and a decomposition into labelled ORIGIN atoms; the script verifies
(1) product of atoms == coefficient (exactly, sympy), (2) that a mutated decomposition is rejected, (3) the classification counts, and then runs
the analysis tests:
  A1  frequency of literal 8 pi^k / 16 pi^k / 32 pi^k / 64 pi^k coefficients in the table (descriptive; the table is selection-biased, see README)
  A2  the origin of the '4' in 32 pi = 8 pi x 4 across the gravitational instances (a table of origin tags; the test 'is one origin shared?')
  A3  the pi-power of every instance that links a RATE^2 to G x density, against the puzzle's pi^0 relation  a0^2 = G rho/4
  A4  rate / sqrt(G rho) for every classical dynamical rate at density rho, against a0 = 1/2 sqrt(G rho)
  A5  hypothesis tests: H_GW (Isaacson 1/(32 pi) as the cause), H_FF (free fall), H_BH (horizon with kappa = a0), H_TOP (Gauss-Bonnet), H_hbar
  A6  the MOND-literature coefficients: derivations land at 2H, data want H/(2 pi) .. H/6 (a gap ~ 4 pi)
Controls (each MUST be caught): a mutated decomposition; a false 'common origin' claim; a false 'rate = a0' claim.
Exit 0 = every check and every control behaves.
"""
import sys
import sympy as sp

ok = []
def check(name, cond):
    ok.append(bool(cond)); print(f"  [{'OK' if cond else 'FAIL'}] {name}")

pi = sp.pi; R = sp.Rational
import os
HERE = os.path.dirname(os.path.abspath(__file__))
def read_out(name):
    p = os.path.join(HERE, name)
    return open(p).read() if os.path.exists(p) else ''

# origin tags
E8 = 'E8'            # Einstein coupling 8 pi G (source normalisation)
ACT = 'ACT'          # normalisation of the quadratic Einstein-Hilbert action / field (1/2, 1/4, canonical 1/2, virial 2, polarisation 2)
SPH = 'SPH'          # solid angle / sphere volume / ball volume (4 pi, 2 pi^2, ...)
HOR = 'HOR'          # Schwarzschild horizon geometry: r_s = 2M, kappa = 1/(4M)
THM = 'THM'          # thermal period 2 pi (Hawking/Unruh)
ANG = 'ANG'          # an angle integral (pi/2 from the cycloid)
SPEC = 'SPEC'        # spectral integral / zeta / loop measure
TOP = 'TOP'          # Pfaffian / winding / trace normalisation of a topological integral
NRM = 'NRM'          # a norm convention
NUM = 'NUM'          # a pure number from a specific calculation (Kepler harmonic, 1/5 from an angular average, ...)
FIT = 'FIT'          # the fitted framework factor kappa = 1/2

# each atom: (tag, value).   coeff must equal the product.
census = [
 # id, short name, coefficient, atoms, class, source status
 ('I01', 'Isaacson GW energy: rho = <hdot_ij hdot_ij>/(32 pi G)', 1 / (32 * pi),
     [(E8, 1 / (8 * pi)), (ACT, R(1, 2)), (ACT, R(1, 4)), (ACT, 2)], 'scale', 'opened gr-qc/0501041 eq.(5.38),(5.40); derived c01 A'),
 ('I02', 'graviton coupling kappa^2 = 32 pi G (tensor-canonical)', 32 * pi,
     [(E8, 8 * pi), (ACT, 2), (ACT, 4), (ACT, R(1, 2))], 'scale', 'opened 1703.05448 eq.(2.9.11); derived c01 B'),
 ('I03', 'per-polarisation kappa^2 = 16 pi G', 16 * pi,
     [(E8, 8 * pi), (ACT, 2), (ACT, 4), (ACT, R(1, 2)), (NRM, R(1, 2))], 'scale', 'derived c01 B'),
 ('I04', 'Bondi mass loss (1/32 pi) oint N_AB N^AB', 1 / (32 * pi),
     [(E8, 1 / (8 * pi)), (ACT, R(1, 2)), (ACT, R(1, 4)), (ACT, 2)], 'scale', 'from memory (Bondi-Sachs); follows from I01 by flux integration'),
 ('I05', 'ADM mass 1/(16 pi G) oint(...)', 1 / (16 * pi),
     [(E8, 1 / (8 * pi)), (ACT, R(1, 2))], 'scale', 'derived c01 E'),
 ('I06', 'Komar mass 1/(4 pi G) oint', 1 / (4 * pi),
     [(E8, 1 / (8 * pi)), (NUM, 2)], 'scale', 'derived c01 E'),
 ('I07', 'BH first law kappa/(8 pi) dA', 1 / (8 * pi),
     [(THM, 1 / (2 * pi)), (HOR, R(1, 4))], 'scale', 'derived c01 E (Kerr, sympy)'),
 ('I08', 'Schwarzschild area A = 16 pi M^2', 16 * pi,
     [(SPH, 4 * pi), (HOR, 4)], 'scale', 'derived c01 E'),
 ('I09', 'Schwarzschild A kappa^2 = pi (max over Kerr-Newman)', pi,
     [(SPH, 4 * pi), (HOR, R(1, 4))], 'dimensionless-geometric', 'derived c01 E (sharp bound, 200000-sample scan + proof)'),
 ('I10', 'Hawking temperature T = 1/(8 pi G M)', 1 / (8 * pi),
     [(THM, 1 / (2 * pi)), (HOR, R(1, 4))], 'scale', 'derived c01 E'),
 ('I11', 'mean density of a Schwarzschild ball rho = 3/(32 pi G^3 M^2)', 3 / (32 * pi),
     [(NUM, 3), (SPH, 1 / (4 * pi)), (HOR, R(1, 8))], 'scale', 'opened Wikipedia "Schwarzschild radius"; algebra here'),
 ('I12', 'Hawking photon-only power 1/(15360 pi G^2 M^2)', 1 / (15360 * pi),
     [(SPEC, pi**2 / 60), (SPH, 16 * pi), (THM, (1 / (2 * pi))**4), (HOR, R(1, 4)**4)], 'scale', 'derived c02 D4; opened Wikipedia "Hawking radiation"'),
 ('I13', 'evaporation time 5120 pi G^2 M^3', 5120 * pi,
     [(NUM, R(1, 3)), (SPEC, 60 / pi**2), (SPH, 1 / (16 * pi)), (THM, (2 * pi)**4), (HOR, 4**4)], 'scale', 'derived c02 D4; opened Wikipedia'),
 ('I14', 'free fall: G rho t_ff^2 = 3 pi/32', 3 * pi / 32,
     [(ANG, (pi / 2)**2), (E8, 3 / (8 * pi))], 'scale', 'derived c02 D2; Wikipedia "Free-fall time" form (1/4)sqrt(3 pi/2 G rho)'),
 ('I15', 'Friedmann H^2 = (8 pi/3) G rho', 8 * pi / 3,
     [(E8, 8 * pi), (NUM, R(1, 3))], 'scale', 'derived c02 D1 (sympy FRW G_tt = 3H^2)'),
 ('I16', 'Jeans k_J^2 c_s^2 = 4 pi G rho', 4 * pi,
     [(SPH, 4 * pi)], 'scale', 'derived c02 D3'),
 ('I17', 'Peters P = (32/5) G^4 mu^2 M^3/a^5 (pi-free)', R(32, 5),
     [(NUM, 2), (NUM, 64), (NUM, R(1, 4)), (NUM, R(1, 5))], 'scale', 'derived c01 C'),
 ('I18', 'chirp fdot = (96/5) pi^(8/3) ...', R(96, 5) * pi**R(8, 3),
     [(NUM, 3), (NUM, R(32, 5)), (NUM, pi**R(8, 3))], 'scale', 'derived c01 C'),
 ('I19', 'Larmor P = q^2 a^2/(6 pi) (HL)', 1 / (6 * pi),
     [(SPH, 1 / (4 * pi)**2), (SPH, 8 * pi / 3)], 'scale', 'derived c01 D'),
 ('I20', 'Chern-Gauss-Bonnet int E4 = 32 pi^2 chi', 32 * pi**2,
     [(TOP, 2), (SPH, (4 * pi)**2)], 'topological', 'derived c03 T1 (S^4, S^2xS^2, n=1..6); hep-th/9308075 eq.(35) form'),
 ('I21', 'BPST instanton: int F Ftilde = 32 pi^2 k', 32 * pi**2,
     [(SPH, 2 * pi**2), (TOP, 16)], 'topological', 'derived c03 T2 (explicit BPST); opened 0802.1862 eq.(10.3),(12.7)'),
 ('I22', 'instanton action 8 pi^2/g^2', 8 * pi**2,
     [(SPH, 2 * pi**2), (TOP, 16), (NUM, R(1, 4))], 'topological', 'derived c03 T2; opened 0802.1862 eq.(1.1)'),
 ('I23', 'loop factor 1/(16 pi^2)', 1 / (16 * pi**2),
     [(SPH, 1 / (8 * pi**2)), (SPEC, R(1, 2))], 'scale-free', 'derived c03 T4'),
 ('I24', 'Chern-Simons: Delta S = 2 pi k from (k/12 pi)(24 pi^2)', 2 * pi,
     [(TOP, 1 / (12 * pi)), (TOP, 24 * pi**2)], 'topological', 'derived c03 T3'),
 ('I25', 'Euler-Heisenberg e^4/(360 pi^2 m^4)', 1 / (360 * pi**2),
     [(SPEC, 1 / (8 * pi**2)), (SPEC, R(1, 45))], 'scale', 'derived c02 D6; opened hep-th/0406216 eq.(1.9)'),
 ('I26', 'Schwinger rate (eE)^2/(4 pi^3) exp(-pi m^2/eE)', 1 / (4 * pi**3),
     [(NUM, 2), (SPEC, 1 / (8 * pi**2)), (SPEC, pi), (SPEC, 1 / pi**2)], 'scale', 'derived c02 D6; opened hep-th/0406216 eq.(1.10),(1.11)'),
 ('I27', 'trace anomaly a_scalar/(16 pi^2) = 1/(5760 pi^2)', 1 / (5760 * pi**2),
     [(SPH, 1 / (16 * pi**2)), (NUM, R(1, 360))], 'scale-free', 'derived c03 T5; opened hep-th/9308075 eq.(30),(31)'),
 ('I28', 'de Sitter conformal-scalar rho = H^4/(960 pi^2)', 1 / (960 * pi**2),
     [(NUM, 6), (SPH, 1 / (16 * pi**2)), (NUM, R(1, 360))], 'scale', 'derived c03 T5 (value from memory: Bunch-Davies vacuum)'),
 ('I29', 'semiclassical self-consistent dS: G H^2 = 360 pi/N', 360 * pi,
     [(NUM, 3), (SPH, 960 * pi**2), (E8, 1 / (8 * pi))], 'scale-free', 'derived c03 T5'),
 ('I30', 'Polyakov c/(96 pi) int R box^-1 R', 1 / (96 * pi),
     [(TOP, 1 / (24 * pi)), (NRM, R(1, 4))], 'scale-free', 'derived c03 T6; opened hep-th/0402009 App.B (c/24 pi)'),
 ('I31', 'Casimir E/A = -pi^2/(720 d^3)', pi**2 / 720,
     [(SPEC, 1 / (6 * pi)), (SPEC, pi**3), (SPEC, R(1, 120))], 'scale', 'derived c02 D5'),
 ('I32', 'Stefan-Boltzmann sigma = pi^2/60', pi**2 / 60,
     [(NUM, R(1, 4)), (SPEC, pi**2 / 15)], 'scale', 'derived c02 D4'),
 ('I33', 'S^4: 32 pi^2 = 12 Vol(S^4)', 32 * pi**2,
     [(NUM, 12), (SPH, 8 * pi**2 / 3)], 'topological', 'derived c03 T1, T7'),
 ('I34', 'de Sitter horizon A Lambda = 12 pi', 12 * pi,
     [(SPH, 4 * pi), (NUM, 3)], 'dimensionless-geometric', 'derived c01 F'),
 ('I35', 'Nariai horizon A Lambda = 4 pi', 4 * pi,
     [(SPH, 4 * pi)], 'dimensionless-geometric', 'derived c01 F'),
 ('I39', 'quadratic EH action for h_ij h_ij: S_2 = (1/(64 pi G)) int (hdot_ij hdot_ij - ...)', 1 / (64 * pi),
     [(E8, 1 / (8 * pi)), (ACT, R(1, 2)), (ACT, R(1, 4))], 'scale', 'derived c01 A (A0 = 1, sympy)'),
 ('I40', 'Euclidean Nariai S^2 x S^2: int E4 = 128 pi^2 (chi = 4)', 128 * pi**2,
     [(TOP, 4), (TOP, 2), (SPH, (4 * pi)**2)], 'topological', 'derived c03 T1'),
 ('I41', 'Euclidean S^4 / Schwarzschild: int E4 = 64 pi^2 (chi = 2)', 64 * pi**2,
     [(TOP, 2), (TOP, 2), (SPH, (4 * pi)**2)], 'topological', 'derived c03 T1 (S^4); Euclidean Schwarzschild in p01'),
 ('I38', 'Eddington luminosity L = 4 pi G M c/kappa_es (radiation force = gravity)', 4 * pi,
     [(SPH, 4 * pi)], 'scale', 'from memory (standard); one-line algebra'),
 ('I36', 'THE PUZZLE: Lambda = 32 pi a0^2 (G rho_Lambda = 4 a0^2)', 32 * pi,
     [(E8, 8 * pi), (FIT, 4)], 'scale', 'the record; p01, p04'),
 ('I37', 'THE PUZZLE, dimensionless: A Lambda = 32 pi^2 with A = pi/a0^2', 32 * pi**2,
     [(E8, 8 * pi), (SPH, 4 * pi)], 'dimensionless-geometric', 'the record; p01, p04'),
]
names = {c[0]: c for c in census}
# hbar appears in the relation itself / relation belongs to classical gravity or Newtonian gravity (set by hand, one line each)
HBAR = {'I07', 'I10', 'I12', 'I13', 'I23', 'I25', 'I26', 'I27', 'I28', 'I29', 'I30', 'I31', 'I32'}
GRAV = {'I01', 'I02', 'I03', 'I04', 'I05', 'I06', 'I07', 'I08', 'I09', 'I10', 'I11', 'I12', 'I13', 'I14', 'I15', 'I16', 'I17', 'I18', 'I20', 'I27',
        'I28', 'I29', 'I30', 'I34', 'I35', 'I36', 'I37', 'I38'}

print("\nCensus table: decomposition into origin atoms is exact")
bad = [c[0] for c in census if sp.simplify(sp.Mul(*[v for _, v in c[3]]) - c[2]) != 0]
check(f"all {len(census)} decompositions multiply back to the coefficient exactly (sympy)", not bad)
if bad: print("      BAD:", bad)
# CONTROL: mutate one atom of one instance
mut = list(names['I01'][3]); mut[2] = (ACT, R(1, 8))
check("CONTROL C-4a: Isaacson with the expansion factor 1/8 instead of 1/4 is rejected", sp.simplify(sp.Mul(*[v for _, v in mut]) - names['I01'][2]) != 0)
mut = list(names['I36'][3]); mut[1] = (FIT, 2)
check("CONTROL C-4b: the puzzle with '2' instead of 4 (Lambda = 16 pi a0^2) is rejected", sp.simplify(sp.Mul(*[v for _, v in mut]) - names['I36'][2]) != 0)

print("\n      id   coefficient            class                    decomposition (tag: value)                                  | name  [source status]")
for c in sorted(census, key=lambda c: int(c[0][1:])):
    dec = ' x '.join(f"{t}:{sp.simplify(v)}" for t, v in c[3])
    print(f"      {c[0]}  {str(sp.simplify(c[2])):22s} {c[4]:24s} {dec:60s} | {c[1]}  [{c[5]}]")

# ------------------------------------------------------------------ classification
print("\nClassification")
klass = {}
for c in census: klass.setdefault(c[4], []).append(c[0])
for k, v in klass.items(): print(f"      {k:26s} n = {len(v):2d}: {' '.join(v)}")
topo = klass['topological']; scale = klass['scale']; dimless = klass['dimensionless-geometric']
check("[table] the 32 pi^2 (two-pi) instances are TOPOLOGICAL normalisations: GB (I20), instanton (I21), S^4 identity (I33) - scale-free integers",
      all(i in topo for i in ('I20', 'I21', 'I33')) and all(names[i][2] == 32 * pi**2 for i in ('I20', 'I21', 'I33')))
check("[table] the 32 pi (one-pi) literal coefficients are I01, I02, I04 (field normalisations) and the puzzle I36",
      {c[0] for c in census if c[2] in (32 * pi, 1 / (32 * pi))} == {'I01', 'I02', 'I04', 'I36'})

# ------------------------------------------------------------------ A1 literal frequencies
print("\nA1  literal coefficient frequencies (descriptive only; the table was assembled by SEARCHING for 32 pi, so 32 pi is over-represented)")
def literal(c, m, k):                                            # c == m pi^k or 1/(m pi^k)
    return sp.simplify(c - m * pi**k) == 0 or sp.simplify(c - 1 / (m * pi**k)) == 0
rows = {}
for m in (4, 8, 12, 16, 24, 32, 48, 64, 96):
    ids = [c[0] for c in census if any(literal(c[2], m, k) for k in (1, 2))]
    rows[m] = ids
    print(f"      literal {m:3d} pi^k (k = 1, 2) or reciprocal: n = {len(ids):2d} : {' '.join(ids)}")
tags0 = {c[0]: {t for t, v in c[3]} for c in census}
lit32 = set(rows[32])
print(f"      literal-32 set = {sorted(lit32)}")
check("[table] every member of the literal 32 pi^k set (other than the puzzle) is EITHER a topological normalisation (GB, instanton, S^4 identity) OR a field normalisation (tag ACT: kappa^2, Isaacson, Bondi) - no third kind",
      all((names[i][4] == 'topological') != (ACT in tags0[i]) for i in lit32 - {'I36', 'I37'}))
check("[table] the occurrence count says nothing about physics: 32 pi^k appears 3 (topological) + 3 (field normalisation) + 2 (puzzle) times; the counts of 8, 16, 64 are set by which formulae I searched",
      len(rows[32]) == 8)

# ------------------------------------------------------------------ A2 origin of the '4'
print("\nA2  the origin of the extra '4' in 32 pi = 8 pi x 4 (gravitational, hbar-free instances only)")
origin_of_4 = {
    'I01/I02/I04': 'ACT: second-order expansion of sqrt(-g)R (1/4), EH half (1/2), canonical half, e_ij e_ij = 2  [field normalisation; convention-laden]',
    'I14 free fall': 'ANG: (pi/2)^2 from the cycloid angle; the 8 pi is Gauss/Friedmann; net pi count is +1 in the numerator',
    'I07/I08/I09/I10/I11/I12': 'HOR: r_s = 2M and kappa = 1/(4M); (1/2)^2 = 1/4 = (r_s kappa)^2',
    'I20 GB (32 pi^2)': 'TOP: (4 pi)^n n! Pfaffian normalisation; with a tensor-vs-2-form norm factor 4 (2-form norm, 1/8 pi^2)',
    'I21 instanton': 'TOP/SPH: Vol(S^3) = 2 pi^2 times 16; 32 pi^2 = 8 pi^2 x 2 x 2 (trace norm 1/2, F^F = (1/2) F Ftilde)',
    'I36 puzzle': 'FIT: 4 = 1/kappa^2 with kappa = 1/2 (fitted); on the horizon reading it is the HOR entry (r_s kappa = 1/2), which p06 shows cannot be realised',
}
for k, v in origin_of_4.items(): print(f"      {k:26s} {v}")
tag_sets = {c[0]: {t for t, v in c[3]} for c in census}
grav_32ish = ['I01', 'I02', 'I04', 'I14']
common = set.intersection(*[tag_sets[i] for i in grav_32ish])
print(f"      tags common to all of {grav_32ish}: {sorted(common)}")
check("[table+derivations] across the 32 pi-type gravitational instances (I01, I02, I04, I14) the only common origin tag is Einstein's 8 pi G coupling itself: the residual factors have different origins",
      common == {E8})
share = {t: [i for i in grav_32ish if t in tag_sets[i]] for t in (ACT, ANG, HOR, E8)}
print("      incidence:", share)
check("[table+derivations] the ACT normalisation is shared by I01, I02, I04 (same cause: the quadratic EH action) but NOT by the free-fall time, which has an ANG origin; HOR is in none of them",
      set(share[ACT]) == {'I01', 'I02', 'I04'} and share[ANG] == ['I14'] and share[HOR] == [])
check("CONTROL C-4c: the false claim 'the same origin tag (ACT) is shared by all four 32 pi-type gravitational instances' is rejected", set(share[ACT]) != set(grav_32ish))
hor_ids = [i for i, s in tag_sets.items() if HOR in s]
print(f"      instances carrying the Schwarzschild-horizon origin HOR: {hor_ids}")
check("[table+derivations] the only instances that share the puzzle's horizon-type '4' are the black-hole-geometry ones (I07-I13); the puzzle's own horizon reading is p06's excluded object",
      set(hor_ids) == {'I07', 'I08', 'I09', 'I10', 'I11', 'I12', 'I13'})

# ------------------------------------------------------------------ A3 pi-power of rate^2 = G rho relations
print("\nA3  rate^2 versus G rho: pi-power in the coefficient")
rate_rel = [   # name, coefficient c in rate^2 = c G rho
    ('Friedmann H^2', 8 * pi / 3),
    ('free fall 1/t_ff^2', 32 / (3 * pi)),
    ('Jeans (k_J c_s)^2', 4 * pi),
    ('uniform-ball harmonic omega_0^2', 4 * pi / 3),
    ('THE PUZZLE a0^2', R(1, 4)),
]
def pipow(c_):
    d = sp.powsimp(sp.simplify(c_)).as_powers_dict()
    return d.get(pi, 0)
for n_, c_ in rate_rel:
    print(f"      {n_:34s} c = {sp.simplify(c_)!s:12s} = {float(c_):8.4f}   pi-power {pipow(c_)}")
check("every classical dynamical rate^2 at density rho carries pi^(+1) or pi^(-1) (Poisson/Gauss 4 pi or the cycloid angle); the puzzle's a0^2 = G rho/4 carries pi^0",
      all(abs(pipow(c_)) == 1 for n_, c_ in rate_rel[:-1]) and pipow(rate_rel[-1][1]) == 0)
check("relative to the Friedmann rate the puzzle's extra factor is 1/(4 x 8 pi/3) = 1/Z^2: pi^(-1) all sits in the Friedmann 8 pi; the '4' is the only new content",
      sp.simplify(rate_rel[0][1] / rate_rel[-1][1] - 32 * pi / 3) == 0)

# ------------------------------------------------------------------ A4 rates over sqrt(G rho)
print("\nA4  classical rate / sqrt(G rho)  versus  a0 / sqrt(G rho_Lambda) = 1/2")
rates = {n_: sp.sqrt(c_) for n_, c_ in rate_rel}
for n_, v in rates.items(): print(f"      {n_:34s} {float(v):7.4f}")
a0c = rates['THE PUZZLE a0^2']
fastest_ratio = {n_: float(v / a0c) for n_, v in rates.items() if n_ != 'THE PUZZLE a0^2'}
print("      ratio to a0:", {k: round(v, 3) for k, v in fastest_ratio.items()})
check("every classical dynamical rate of a self-gravitating density rho is 3.7 to 7.1 times FASTER than a0 = (1/2) sqrt(G rho): a0 is not a dynamical rate of the vacuum (it is the README's 'sub-Hubble' statement, seen from the census)",
      min(fastest_ratio.values()) > 3.5 and max(fastest_ratio.values()) < 7.2)
check("CONTROL C-4d: the false claim 'free fall gives a0 (ratio 1)' is rejected", abs(fastest_ratio['free fall 1/t_ff^2'] - 1) > 1)

# ------------------------------------------------------------------ A5 hypothesis tests
print("\nA5  can any census cause be the cause of the puzzle's 32 pi?")
# H_GW: rho_Lambda = <hdot_ij hdot_ij>/(32 pi G)  with rho_Lambda = 4 a0^2/G  ->  omega^2 <h_ij h_ij> = 128 pi a0^2
hh_needed = 128 * pi
w_over_a0_for_pert = sp.sqrt(hh_needed / R(1, 100))              # <h_ij h_ij> = 0.01
print(f"      H_GW: omega^2 <h_ij h_ij> = 128 pi a0^2 = {float(hh_needed):.1f} a0^2; if omega = a0 then <h_ij h_ij> = {float(hh_needed):.0f} (h_+ ~ {float(sp.sqrt(hh_needed/2)):.1f} >> 1);")
print(f"            perturbative (<h_ij h_ij> <= 0.01) requires omega >= {float(w_over_a0_for_pert):.0f} a0: an extra free scale (the frequency) and a free amplitude")
Zsq = 32 * pi / 3                                                # Z^2 = (H_Lambda/a0)^2
hh_H = sp.simplify(128 * pi / Zsq)                               # omega = H_Lambda = Z a0  ->  <h_ij h_ij> = 128 pi a0^2/H^2 = 128 pi/Z^2
print(f"            at omega = H_Lambda: <h_ij h_ij> = 128 pi/Z^2 = {hh_H} (h_+ = sqrt(6) = {float(sp.sqrt(hh_H/2)):.2f}); NOTE the Isaacson average assumes omega >> H, so omega = H is outside its domain: illustrative only")
check("[illustrative] H_GW at omega = H_Lambda would need <h_ij h_ij> = 12 exactly (= 3 x 4: the Friedmann 3 and the puzzle's 4): non-perturbative (h_+ = 2.45), outside the short-wave domain, and it only restates Z^2 = 32 pi/3",
      hh_H == 12)
check("H_GW fails: reading the puzzle as rho_Lambda = GW-like condensate needs h_+ ~ 14 at omega = a0 (non-perturbative), or a free frequency omega >= 200 a0 (then a0 is not the rate); either way a second scale enters",
      float(sp.sqrt(hh_needed / 2)) > 10 and float(w_over_a0_for_pert) > 199)
# H_FF: G rho t_ff^2 = 3 pi/32 vs a0^2 t_ff^2 = 3 pi/128
aff = sp.simplify(R(1, 4) * 3 * pi / 32)
check("H_FF fails: a0 t_ff = (1/2) sqrt(3 pi/32) = 0.271 (not 1, not pi-free): free fall supplies neither the 1/2 nor the pi-power (pi^-1 in rate^2)",
      sp.simplify(sp.sqrt(aff) - R(1, 2) * sp.sqrt(3 * pi / 32)) == 0 and abs(float(sp.sqrt(aff)) - 0.2714) < 1e-3)
# H_BH: embeddability, Z <= 2 iff r_s <= L
Zf = sp.sqrt(32 * pi / 3)
ratio_MN = 3 * sp.sqrt(3) * Zf / 4
check(f"H_BH fails as a realised object: M_s/M_Nariai = 3 sqrt(3) Z/4 = {float(ratio_MN):.3f} > 1, so Schwarzschild-de Sitter with kappa = a0 has NO horizon (p06, recomputed)", float(ratio_MN) > 7.5 and float(ratio_MN) < 7.53)
check("H_BH: Z <= 2 would be needed to fit r_s = Z L/2 <= L; the puzzle has Z = 5.789", Zf > 2)
# H_TOP: scale-free (checked in c03 for S^4, S^2xS^2 at every L)
c03 = read_out('c03_topology_loops_anomalies.out')
check("H_TOP: c03 shows the GB integrals are the same at every radius (S^4: 64 pi^2 for every L) and the instanton integral independent of rho: scale-free, so they cannot fix a0/H",
      'int E4 = 64 pi^2 = 32 pi^2 chi with chi(S^4) = 2, for every L' in c03 and 'int F^a Ftilde^a d^4x = Vol(S^3) x 192 x (1/12) = 32 pi^2' in c03 and '[OK] int E4 = 64 pi^2' in c03)
# H_hbar: classical relation
hbar_ids = sorted(HBAR)
check("[bookkeeping] H_hbar: the puzzle relation carries no hbar (classical), so it cannot be a member of the hbar-carrying family (Hawking, Schwinger, EH, Casimir, SB, anomalies, loops: %s)" % ' '.join(hbar_ids),
      'I36' not in HBAR and 'I37' not in HBAR)
classical = [c[0] for c in census if c[0] not in HBAR]
print(f"      hbar-free instances: {classical}")

# ------------------------------------------------------------------ A6 MOND literature
print("\nA6  MOND-literature coefficients (sources opened: astro-ph/9805346, 0801.3133, 1611.02269, 1704.00780, 1005.3537, 1104.2022)")
lit = [   # (description, coefficient of H_Lambda = sqrt(Lambda/3) in the derived a0)
  ('Milgrom 1999 (astro-ph/9805346) eq.(9): a0_hat = 2 (Lambda/3)^(1/2) = 2 H_Lambda [crossover of mu_hat with mu_hat(x<<1) = x]', 2),
  ('1104.2022 eq.(9): A_0 = 2 c H_dS', 2),
  ('Smolin (1704.00780) eq.(32): a^2 = 2 a_N a_Lambda, a_Lambda = c^2 sqrt(Lambda) = sqrt(3) H_Lambda  ->  a0 = 2 a_Lambda', 2 * sp.sqrt(3)),
  ('Ho-Minic-Ng (1005.3537) eq.(5),(6): F = m a^2/(2 a0), a0 = sqrt(Lambda/3) = H  ->  MOND a0 = 2 H before their a_c := a0/(2 pi)', 2),
]
for n_, v in lit: print(f"      derivation: {n_}  -> a0 = {sp.simplify(v)} H_Lambda = {float(v):.3f} H_Lambda")
data_lo, data_hi = 1 / (2 * pi), R(1, 6)                         # H/(2 pi) (Milgrom, 0801.3133 'observed'), H/6 (Verlinde eq.(1.7),(7.43))
print(f"      data-side coefficients: Milgrom's observed 2 pi a0 ~ c H0 [0801.3133] -> {float(data_lo):.4f} H; Verlinde's DERIVED a_M = a0/6 with a0 = cH0 [1611.02269 eq.(1.7),(7.43): (d-3)/((d-2)(d-1)) at d = 4] -> {float(data_hi):.4f} H; framework 1/Z = {float(1/Zf):.4f} H_Lambda; Smolin a0 ~ a_Lambda/8.3")
gap_M = 2 / data_lo
gap_V = 2 / data_hi
gap_F = 2 * Zf
print(f"      gap = (Unruh-type 2H)/(coefficient that matches the data): vs Milgrom's 2 pi {float(gap_M):.2f} = 4 pi; vs Verlinde's 1/6 {float(gap_V):.2f}; framework 2Z = {float(gap_F):.2f}")
check("the four Unruh/entropic derivations land at 2 to 2 sqrt(3) H_Lambda (pi-free) while the coefficients that match the data are H/(2 pi) (observed, Milgrom), H/6 (Verlinde's separate derivation), 1/Z (framework): the gap is 4 pi = 12.6 (Milgrom 2H), 12, 2Z = 11.6, and every one of the four derivations exceeds every data-side coefficient by a factor >= 11.5",
      sp.simplify(gap_M - 4 * pi) == 0 and gap_V == 12 and abs(float(gap_F) - 11.58) < 0.01
      and all(float(v / c_) >= 11.5 for _, v in lit for c_ in (data_lo, data_hi, 1 / Zf)) and all(not sp.sympify(v).has(pi) for _, v in lit))
print("      => the puzzle's Z is the statement 'the Unruh / entropic derivation over-predicts a0 by 2Z = 11.58' (Milgrom's own version: 4 pi). No new content.")

print(f"\n  {sum(ok)}/{len(ok)} checks held.")
sys.exit(0 if all(ok) else 1)
