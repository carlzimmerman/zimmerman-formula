#!/usr/bin/env python3
"""Q5 / item 1: first-order shift of the extremal mass (charge-to-mass ratio) of a
Reissner-Nordstrom black hole from the eight four-derivative operators of the
Cheung-Liu-Remmen basis, by the Reall-Santos on-shell-action method, in sympy (exact).

Real run:     python3 q1_extremality_shift.py           -> exit 0, writes q1_extremality_shift.out (by the caller: tee)
MUTATE ctrl:  python3 q1_extremality_shift.py MUTATE    -> the ONLY trigger is the literal argv 'MUTATE'
              (background is made non-extremal, m = 1.1 Q; the H2/H3/H4 checks must FAIL, exit 1)

Units: kappa = 1 (so d_i = c_i, G = 1/(8 pi), m := G M).  Extremal RN: m = Q = r_+, f = (1-Q/r)^2.
Fields: electric F_tr = sqrt2 Q/(kappa r^2) ; magnetic F_thph = sqrt2 Q sin(th)/kappa  (same energy density).
Delta M_ext(Q) = - Int_{r_+}^{inf} 4 pi r^2 Delta L dr,  Delta z = - Delta m/m with Delta m = G Delta M.
"""
import sys
import sympy as sp

MUTATE = (len(sys.argv) > 1 and sys.argv[1] == 'MUTATE')
results = []
def check(name, ok, info=""):
    results.append(bool(ok))
    print(("[PASS] " if ok else "[FAIL] ") + name + (("  " + info) if info else ""))

t, r, th, ph = sp.symbols('t r theta phi', positive=True)
Q = sp.symbols('Q', positive=True)
X = [t, r, th, ph]
G = 1 / (8 * sp.pi)   # kappa = 1  ->  kappa^2 = 8 pi G

def geometry(f):
    g = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th)**2)
    gi = g.inv()
    n = 4
    Gam = [[[sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(n)) / 2
             for c in range(n)] for b in range(n)] for a in range(n)]
    Gam = [[[sp.simplify(Gam[a][b][c]) for c in range(n)] for b in range(n)] for a in range(n)]
    # R^a_{bcd} = d_c Gam^a_{db} - d_d Gam^a_{cb} + Gam^a_{ce} Gam^e_{db} - Gam^a_{de} Gam^e_{cb}   (MTW)
    Rud = {}
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    e = sp.diff(Gam[a][d][b], X[c]) - sp.diff(Gam[a][c][b], X[d])
                    e += sum(Gam[a][c][k] * Gam[k][d][b] - Gam[a][d][k] * Gam[k][c][b] for k in range(n))
                    Rud[a, b, c, d] = sp.simplify(e)
    Rdn = {(a, b, c, d): sp.simplify(sum(g[a, k] * Rud[k, b, c, d] for k in range(n)))
           for a in range(n) for b in range(n) for c in range(n) for d in range(n)}
    Ric = sp.Matrix(n, n, lambda b, d: sp.simplify(sum(Rud[a, b, a, d] for a in range(n))))
    Rs = sp.simplify(sum(gi[b, d] * Ric[b, d] for b in range(n) for d in range(n)))
    return g, gi, Rdn, Ric, Rs

def invariants(f, kind):
    g, gi, Rdn, Ric, Rs = geometry(f)
    n = 4
    Fd = sp.zeros(4, 4)
    if kind == 'E':
        Fd[0, 1] = sp.sqrt(2) * Q / r**2; Fd[1, 0] = -Fd[0, 1]
    else:
        Fd[2, 3] = sp.sqrt(2) * Q * sp.sin(th); Fd[3, 2] = -Fd[2, 3]
    Fu = gi * Fd * gi.T                     # F^{ab}
    Fmix = gi * Fd                          # F^a_b
    Ricu = gi * Ric * gi.T
    F2 = sp.simplify(sum(Fd[a, b] * Fu[a, b] for a in range(n) for b in range(n)))
    Ric2 = sp.simplify(sum(Ric[a, b] * Ricu[a, b] for a in range(n) for b in range(n)))
    # Riem^2 = R_{abcd} R^{abcd}
    def up4(a, b, c, d):
        return sum(gi[a, i] * gi[b, j] * gi[c, k] * gi[d, l] * Rdn[i, j, k, l]
                   for i in range(n) for j in range(n) for k in range(n) for l in range(n)
                   if gi[a, i] != 0 and gi[b, j] != 0 and gi[c, k] != 0 and gi[d, l] != 0)
    Riem2 = 0; RFF = 0
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    if Rdn[a, b, c, d] != 0:
                        Riem2 += Rdn[a, b, c, d] * up4(a, b, c, d)
                        RFF += Rdn[a, b, c, d] * Fu[a, b] * Fu[c, d]
    Riem2 = sp.simplify(Riem2); RFF = sp.simplify(RFF)
    # R_{mn} F^{m r} F^{n}_{r} = R_{mn} F^{m r} g_{rs} F^{n s}
    RicFF = sp.simplify(sum(Ric[m, nn] * Fu[m, rr] * g[rr, s] * Fu[nn, s]
                            for m in range(n) for nn in range(n) for rr in range(n) for s in range(n)))
    # F^4 = F_{mn} F^{n r} F_{r s} F^{s m} = tr( F_lower * F^{up}... ) via mixed: F^m_n
    F4 = sp.simplify((Fmix * Fmix * Fmix * Fmix).trace())
    ops = {'c1': Rs**2, 'c2': Ric2, 'c3': Riem2, 'c4': Rs * F2, 'c5': RicFF, 'c6': RFF,
           'c7': F2**2, 'c8': F4}
    return {k: sp.simplify(v) for k, v in ops.items()}, Rs, F2

def dM_integral(dL, rplus):
    """Delta M = - Int_{r_+}^{inf} 4 pi r^2 dL dr (dL a function of r only)."""
    return sp.simplify(-sp.integrate(sp.simplify(4 * sp.pi * r**2 * dL), (r, rplus, sp.oo)))

mfac = sp.Rational(11, 10) if MUTATE else 1
m_ = mfac * Q
if MUTATE:
    # non-extremal outer horizon, so the 'extremal' identities cannot hold
    rp = m_ + sp.sqrt(m_**2 - Q**2)
    f = 1 - 2 * m_ / r + Q**2 / r**2
else:
    rp = Q
    f = (1 - Q / r)**2

print("MUTATE =", MUTATE, "  background f =", sp.factor(f), "  r_+ =", sp.simplify(rp))
w_expected = {'c1': 0, 'c2': 1, 'c3': 4, 'c4': 0, 'c5': 1, 'c6': 1, 'c7': 4, 'c8': 2}

shift = {}   # background -> {op: Delta z_i * Q^2}
for kind in ('E', 'B'):
    ops, Rs, F2 = invariants(f, kind)
    print(f"\n[{kind}] R = {Rs}  F^2 = {F2}")
    shift[kind] = {}
    for k, v in ops.items():
        dM = dM_integral(v, rp)
        dz = sp.simplify(-(G * dM) / m_)      # Delta z per unit coefficient
        shift[kind][k] = sp.simplify(dz * Q**2)
        print(f"  {k}: Delta z * Q^2 = {shift[kind][k]}    (expected (2/5) w = {sp.Rational(2,5)*w_expected[k]})")
    if kind == 'E':
        ops_E = ops

# ---- Q1-H1 structure: linear form
check("Q1-H1 shift is a linear form in c1..c8 with Q-independent weights (all Delta z_i Q^2 free of Q)",
      all(not shift[k][o].has(Q) for k in shift for o in shift[k]))

# ---- Q1-H2: CLR eq 61/68 reproduced (electric)
ok2 = all(sp.simplify(shift['E'][k] - sp.Rational(2, 5) * w_expected[k]) == 0 for k in w_expected)
check("Q1-H2 electric weights = (2/5)*(0,1,4,0,1,1,4,2): d0 = d2+4d3+d5+d6+4d7+2d8, Delta z = 2 d0/(5 m^2)  [CLR eq 61, 68]", ok2)

# ---- Q1-H3: Gauss-Bonnet decouples at T=0
GB_E = sp.simplify(ops_E['c3'] - 4 * ops_E['c2'] + ops_E['c1'])    # Riem^2 - 4 Ric^2 + R^2
dM_GB = dM_integral(GB_E, rp)
check("Q1-H3a Gauss-Bonnet Riem^2-4Ric^2+R^2 gives Delta M_ext = 0 on the extremal background", sp.simplify(dM_GB) == 0, f"Delta M_GB = {dM_GB}")
# non-extremal control (computed regardless): proportional to temperature
rpl, rmi = sp.symbols('rp rm', positive=True)
fne = (1 - rpl / r) * (1 - rmi / r)
g_, gi_, Rdn_, Ric_, Rs_ = geometry(fne)
Riem2_ne = 0
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4):
                if Rdn_[a, b, c, d] != 0:
                    Riem2_ne += Rdn_[a, b, c, d] * sum(gi_[a, i] * gi_[b, j] * gi_[c, k] * gi_[d, l] * Rdn_[i, j, k, l]
                                                        for i in range(4) for j in range(4) for k in range(4) for l in range(4)
                                                        if gi_[a, i] != 0 and gi_[b, j] != 0 and gi_[c, k] != 0 and gi_[d, l] != 0)
Ric2_ne = sum(Ric_[a, b] * (gi_ * Ric_ * gi_.T)[a, b] for a in range(4) for b in range(4))
GB_ne = sp.simplify(Riem2_ne - 4 * Ric2_ne + Rs_**2)
dMGB_ne = sp.simplify(dM_integral(GB_ne, rpl))
Tem = (rpl - rmi) / (4 * sp.pi * rpl**2)
print("  non-extremal GB integral:", sp.factor(dMGB_ne), "  T =", Tem, "  ratio/T =", sp.simplify(dMGB_ne / Tem))
check("Q1-H3b non-extremal GB integral vanishes at r_+ = r_- (proportional to T), as argued",
      sp.simplify(dMGB_ne.subs(rmi, rpl)) == 0)

# ---- Q1-H4: field-redefinition equivalences (electric and magnetic)
ok4 = True
for kind in ('E', 'B'):
    # on-shell Ric = T:  c2 Ric^2 -> c2 (F^4 - (F^2)^2/4);  c5 Ric FF -> c5 (F^4 - (F^2)^2/4)   (kappa = 1)
    lhs2 = shift[kind]['c2']; rhs2 = shift[kind]['c8'] - shift[kind]['c7'] / 4
    lhs5 = shift[kind]['c5']
    ok4 &= (sp.simplify(lhs2 - rhs2) == 0) and (sp.simplify(lhs5 - rhs2) == 0)
    # Riem^2 = 4 Ric^2 - R^2 + GB, and R = 0 on shell
    ok4 &= sp.simplify(shift[kind]['c3'] - 4 * shift[kind]['c2']) == 0
check("Q1-H4 c2, c5 equal their on-shell (c7,c8) replacements; c3 = 4 c2 (E and B)", ok4)

# ---- Q1-H5 magnetic: report
same = all(sp.simplify(shift['E'][k] - shift['B'][k]) == 0 for k in w_expected)
print("\nQ1-H5 magnetic weights (2/5)*w_mag:", {k: sp.nsimplify(shift['B'][k] * sp.Rational(5, 2)) for k in w_expected})
print("      electric == magnetic weights:", same)
check("Q1-H5 c1 and c4 absent; c7,c8 enter only as 4c7+2c8 in both backgrounds",
      all(shift[k]['c1'] == 0 and shift[k]['c4'] == 0 and sp.simplify(shift[k]['c8'] - shift[k]['c7'] / 2) == 0 for k in shift))

# ---- Q1-H6: (F F~)^2 identity and Euler-Heisenberg map
a_, m_e = sp.symbols('alpha m', positive=True)
E, B = sp.symbols('E B', real=True)
F2v = 2 * (B**2 - E**2)
FFd = -4 * E * B          # F_{mn} Ftilde^{mn}
F4v = sp.expand((F2v**2 / 2 + FFd**2 / 4))    # tr F^4 = (F^2)^2/2 + (F Ftilde)^2/4
# direct check with explicit F for a parallel E,B configuration
Fm = sp.Matrix([[0, E, 0, 0], [-E, 0, 0, 0], [0, 0, 0, B], [0, 0, -B, 0]])   # (t,x,y,z) with F_tx=E, F_yz=B
eta = sp.diag(-1, 1, 1, 1)
Fmixed = eta * Fm
F4direct = sp.expand((Fmixed**4).trace())
F2direct = sp.expand(sum((eta * Fm * eta)[a, b] * Fm[a, b] for a in range(4) for b in range(4)))
check("Q1-H6a explicit E||B: F^2 = 2(B^2-E^2) and tr F^4 = (F^2)^2/2 + (F Ftilde)^2/4 (=> (FFt)^2 = 4F^4 - 2(F^2)^2)",
      sp.simplify(F2direct - F2v) == 0 and sp.simplify(F4direct - F4v) == 0)
# L_EH = (2 a^2/(45 m^4)) [(E^2-B^2)^2 + 7 (E B)^2] = c7 (F^2)^2 + c8 F^4
c7s, c8s = sp.symbols('c7s c8s')
LEH = 2 * a_**2 / (45 * m_e**4) * ((E**2 - B**2)**2 + 7 * (E * B)**2)
sol = sp.solve(sp.Poly(sp.expand(c7s * F2v**2 + c8s * F4v - LEH), E, B).coeffs(), [c7s, c8s], dict=True)
c7v, c8v = sol[0][c7s], sol[0][c8s]
print("  EH map: c7 =", c7v, " c8 =", c8v, "  4c7+2c8 =", sp.simplify(4 * c7v + 2 * c8v))
check("Q1-H6b EH (recalled form): 4c7+2c8 = 2 alpha^2/(45 m^4) = E^4 coefficient > 0",
      sp.simplify(4 * c7v + 2 * c8v - 2 * a_**2 / (45 * m_e**4)) == 0)

# ---- Q1-H7: rank of the form; the equality locus is a hyperplane
cs = sp.symbols('c1:9')
form = sum(cs[i] * sp.Rational(5, 2) * shift['E'][f'c{i+1}'] for i in range(8))
rank = sp.Matrix([[sp.diff(form, c) for c in cs]]).rank()
print("\nQ1-H7 Delta z * Q^2 = (2/5) * (", sp.simplify(form), ") ; rank of the linear form =", rank)
check("Q1-H7 (structure, NOT a test) extremality shift is a rank-1 free linear form d0(c); the equality locus at any alpha is a hyperplane", rank == 1)
# explicit: for any target alpha and any particle z_p, d0 = (5/2) (z_p-1) Q^2 : solvable
zp, d0 = sp.symbols('z_p d0')
print("       WGC saturation z_p = 1 + (2/5) d0/Q^2  =>  d0 = (5/2)(z_p-1) Q^2 : solvable for d0 for ANY (alpha, m); e does not fix d0, d0 does not fix e")

# ---- Q1-H8/H9: numbers (Thomson alpha; alpha(m_P) = 1/104.94)
print("\nQ1-H8/H9 sizes, Delta z = (2/5) delta l_P^2/Q^2 ; delta = d0/l_P^2 (dimensionless)")
deltas = [1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0]
for alpha_val, lab in ((1 / 137.035999177, 'Thomson'), (1 / 104.94, 'alpha(m_P)')):
    ratio_el = 1 / alpha_val            # l_P^2/Q_e^2, n=1
    ratio_mg = 4 * alpha_val            # l_P^2/Q_m^2, n=1
    print(f"  {lab}: l_P^2/Q_e^2 = {ratio_el:.3f} ; l_P^2/Q_m^2 = {ratio_mg:.5f}")
    for dl in deltas:
        print(f"     delta = {dl:8.0e}: Delta z electric n=1 = {0.4*dl*ratio_el:10.4g}   magnetic n=1 = {0.4*dl*ratio_mg:10.4g}")
    # charge needed for |Delta z| < 5e-10 (magnetic): n^2 > 0.4 delta 4 alpha / 5e-10
    for dl in (1e-2, 1e-1, 1.0):
        nreq = (0.4 * dl * 4 * alpha_val / 5e-10) ** 0.5
        print(f"     magnetic: n needed for |Delta z| < 5e-10 at delta={dl:g}: n >= {nreq:.3e}")
a0 = 1 / 137.035999177
check("Q1-H8 electric n=1 shift is O(1)+ for delta >= 1e-2 at Thomson alpha (EFT not valid there); magnetic/electric ratio = 4 alpha^2 exactly",
      0.4 * 1e-2 / a0 > 0.5 and abs((4 * a0) / (1 / a0) - 4 * a0**2) < 1e-15)
n_req = (0.4 * 0.16 * 4 / 137.036 / 5e-10) ** 0.5
check("Q1-H9 magnetic object needs n >~ 1e3-1e4 Dirac quanta for |Delta z| < 5e-10 at loop-natural delta ~ 1/(2 pi)", 1e3 < n_req < 1e5, f"n_req = {n_req:.3e}")

print("\nSUMMARY: %d/%d checks pass (MUTATE=%s)" % (sum(results), len(results), MUTATE))
sys.exit(0 if all(results) else 1)
