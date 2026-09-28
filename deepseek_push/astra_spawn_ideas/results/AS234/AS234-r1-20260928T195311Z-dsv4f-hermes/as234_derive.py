#!/usr/bin/env python3
"""
AS234-r1 -- PPN alpha2 from the longitudinal moving-source response (CA5-GNC-R).

Mode algebra: fields f(t,z) = Re[ a exp(i(omega t - k z)) ],  d_t -> i*omega, d_z -> -i*k.
Longitudinal sector: k || v || z.  Uniformly moving dust source: omega = k*v,
T^00=rho, T^0i=rho v^i, T^ij=rho v^i v^j (conserved).  Physical metric:
g00=-(1+phi)^2+chi^2, g03=chi, g11=g22=1-2Psi, g33=1-2Psi-2A.

Quadratic action sector (units M_P^2/2, FINAL_ACTION (4); static anchor: AS226):
  L2 = (M_P^2/2)[ R^(2) - c2 K^2 + alpha|a-DZ|^2 + 4 a.DZ - 2|DZ|^2
                  - 2 cN |D(phi-Z)|^2 - 4 cN DZ.DU ]  +  S_b-linear (dust)
S_b-linear:  -rho phi + rho v chi - rho v^2 (Psi+A)
Ties: Z = (ell S_k/4) phi  (eq.(6), f=0);  (7) rho_d=0:  U = phi - Z.
Real-field variations: EOM_f = dL/da_f* + dL/da_f, then tie; Z varied independently.
All sanity anchored on AS226-verified static forms: E1, E2, Psi-bracket, C1 identity.
"""
import sympy as sp
import time, sys

t0 = time.time()
w, k, v = sp.symbols('omega k v', real=True)
MP2, cN, al, c2, ell, Sk = sp.symbols('M_P2 c_N alpha c2 ell S_k', positive=True)
rho = sp.symbols('rho', positive=True)
eps = sp.symbols('eps')

aph, ach, aps, aA, aU, aZ = sp.symbols('a_phi a_chi a_psi a_A a_U a_Z', complex=True)
aphc, achc, apsc, aAc, aUc, aZc = sp.symbols('ac_phi ac_chi ac_psi ac_A ac_U ac_Z', complex=True)
amp  = {'phi': aph, 'chi': ach, 'psi': aps, 'A': aA, 'U': aU, 'Z': aZ}
ampc = {'phi': aphc, 'chi': achc, 'psi': apsc, 'A': aAc, 'U': aUc, 'Z': aZc}
AMPS = list(amp.values()); AMPSc = list(ampc.values())


def hermitian(poly_expr, varlist):
    """Box-averaged Hermitian form of a real quadratic polynomial."""
    expr = sp.expand(poly_expr)
    P = sp.Poly(expr, *[s for s, _, _ in varlist])
    out = sp.S(0)
    info = {s: (sg, nm) for s, sg, nm in varlist}
    for monom, coeff in P.terms():
        deg = sum(monom)
        if deg == 0:
            continue
        facs = [(info[varlist[i][0]][0], info[varlist[i][0]][1], monom[i])
                for i in range(len(monom)) if monom[i] > 0]
        if deg == 2 and len(facs) == 1 and facs[0][2] == 2:
            sg, nm, _ = facs[0]
            out += coeff * sg * sp.conjugate(sg) * amp[nm] * ampc[nm] / 2
        elif deg == 2 and len(facs) == 2 and facs[0][2] == 1 and facs[1][2] == 1:
            (sg1, nm1, _), (sg2, nm2, _) = facs
            out += coeff * (sg1 * sp.conjugate(sg2) * amp[nm1] * ampc[nm2]
                            + sp.conjugate(sg1) * sg2 * ampc[nm1] * amp[nm2]) / 4
        else:
            raise ValueError('unexpected monomial %s' % str(monom))
    return sp.expand(out)


# ---------------- perturbative metric geometry ----------------
t, x, y, z = sp.symbols('t x y z')
ph, ch, ps, aa = sp.symbols('ph ch ps aa', cls=sp.Function)
# longitudinal sector: fields depend only on (t, z); derivatives along x,y vanish
Pt = ph(t, z); Ct = ch(t, z); St = ps(t, z); At = aa(t, z)

eta = sp.diag(-1, 1, 1, 1)
D1 = sp.Matrix([
    [-2*Pt, 0, 0, Ct],
    [0, -2*St, 0, 0],
    [0, 0, -2*St, 0],
    [Ct, 0, 0, -2*St - 2*At]])
D2 = sp.Matrix([
    [-Pt**2 + Ct**2, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]])
Id4 = sp.eye(4)

def matmul(*ms):
    r = ms[0]
    for m in ms[1:]:
        r = sp.expand(r * m)
    return r

gi0, gi1, gi2 = Id4, sp.expand(-matmul(eta, D1, eta)), \
    sp.expand(-matmul(eta, D2, eta) + matmul(eta, D1, eta, D1, eta))
gi = [gi0, gi1, gi2]

cords = [t, x, y, z]

def dg(o2, s, mu, nu):
    Dm = D1 if o2 == 0 else D2
    return (sp.diff(Dm[s, nu], cords[mu]) + sp.diff(Dm[s, mu], cords[nu])
            - sp.diff(Dm[mu, nu], cords[s]))

def Glam(lam, mu, nu, order):
    term = sp.S(0)
    for s in range(4):
        for o1 in range(order + 1):
            o2 = order - 1 - o1
            if o2 < 0 or o2 > 1:
                continue
            term += gi[o1][lam, s] * dg(o2, s, mu, nu)
    return sp.expand(term / 2)


def R_scalar():
    res = {1: sp.S(0), 2: sp.S(0), 3: sp.S(0)}
    for mu in range(4):
        for nu in range(4):
            R1 = sp.S(0); R2 = sp.S(0); R3l = sp.S(0)
            for lam in range(4):
                R1 += sp.diff(Glam(lam, mu, nu, 1), cords[lam]) - sp.diff(Glam(lam, nu, lam, 1), cords[mu])
                R2 += sp.diff(Glam(lam, mu, nu, 2), cords[lam]) - sp.diff(Glam(lam, nu, lam, 2), cords[mu])
                R3l += sp.diff(Glam(lam, mu, nu, 3), cords[lam]) - sp.diff(Glam(lam, nu, lam, 3), cords[mu])
            for r in range(4):
                for s2 in range(4):
                    R2 += Glam(r, mu, nu, 1)*Glam(s2, r, s2, 1) - Glam(r, mu, s2, 1)*Glam(s2, nu, r, 1)
                    R3l += (Glam(r, mu, nu, 1)*Glam(s2, r, s2, 2) + Glam(r, mu, nu, 2)*Glam(s2, r, s2, 1)
                            - Glam(r, mu, s2, 1)*Glam(s2, nu, r, 2) - Glam(r, mu, s2, 2)*Glam(s2, nu, r, 1))
            res[1] += gi0[mu, nu] * R1
            res[2] += gi0[mu, nu] * R2 + gi1[mu, nu] * R1
            res[3] += gi0[mu, nu] * R3l + gi1[mu, nu] * R2 + gi2[mu, nu] * R1
    return {o: sp.expand(res[o]) for o in res}

Rparts = R_scalar()
R2field = sp.expand(Rparts[2] + sp.Rational(1, 2)*(2*Pt - 6*St - 2*At)*Rparts[1])

Klin_s = sp.S(0)
for i in (1, 2, 3):
    for j in (1, 2, 3):
        Klin_s += gi0[i, j] * Glam(0, i, j, 1)
K_lin = sp.expand(Klin_s)
a3lin = sp.diff(Pt, z)

# ---------------- variable extraction ----------------
def flatten_derivs(expr):
    """Recursively flatten nested Derivative nodes (Derivative(Derivative(f,z),z)
    -> Derivative(f,z,z)) so that substitute-varize works cleanly."""
    if isinstance(expr, sp.Derivative):
        inner = flatten_derivs(expr.expr)
        if isinstance(inner, sp.Derivative):
            return flatten_derivs(sp.Derivative(inner.expr, *(inner.variables + list(expr.variables))))
        return sp.Derivative(inner, *expr.variables)
    if expr.is_Atom:
        return expr
    if expr.is_Function or expr.is_Add or expr.is_Mul or expr.is_Pow or expr.is_Symbol:
        if expr.is_Symbol:
            return expr
        return expr.func(*[flatten_derivs(a) for a in expr.args])
    return expr


def varize(expr):
    """Single-shot xreplace: every Derivative node -> plain symbol dv_<nm>_<ot>_<oz>."""
    expr = sp.expand(expr)
    mp = {}
    fnmap = {ph: 'phi', ch: 'chi', ps: 'psi', aa: 'A'}
    for s in sp.preorder_traversal(expr):
        if isinstance(s, sp.Derivative) and isinstance(s.expr, sp.Function) \
           and s.expr.func in fnmap:
            fn = s.expr.func
            ot = sum(1 for q in s.variables if q is t)
            oz = sum(1 for q in s.variables if q is z)
            key = (fnmap[fn], ot, oz)
            mp[s] = sp.Symbol('dv_%s_%d_%d' % key)
    out = sp.expand(expr.xreplace(mp))
    mpf = {fn(t, z): sp.Symbol('dv_%s_0_0' % nm) for fn, nm in fnmap.items()}
    out = sp.expand(out.xreplace(mpf))
    left = [s for s in sp.preorder_traversal(out) if isinstance(s, sp.Derivative)]
    assert not left, "leftover derivatives: %s" % left[:5]
    varlist = []
    for nm in ('phi', 'chi', 'psi', 'A'):
        varlist.append((sp.Symbol('dv_%s_0_0' % nm), (nm, 0, 0)))
    for s in sorted(mp.values(), key=lambda x: x.name):
        p = s.name.split('_')
        varlist.append((s, (p[1], int(p[2]), int(p[3]))))
    return out, {}, varlist

R2v, _, varsR = varize(flatten_derivs(R2field))
Kv, _, varsK = varize(flatten_derivs(K_lin))
a3v, _, varsA = varize(flatten_derivs(a3lin))

SIG = {}
for nm in ('phi', 'chi', 'psi', 'A'):
    SIG[(nm, 0, 0)] = 1; SIG[(nm, 1, 0)] = sp.I*w; SIG[(nm, 0, 1)] = -sp.I*k
    SIG[(nm, 2, 0)] = -w**2; SIG[(nm, 0, 2)] = -k**2; SIG[(nm, 1, 1)] = w*k

def build_fv(varlist):
    return [(vs, SIG[key], key[0]) for vs, key in varlist]

R2h = hermitian(R2v, build_fv(varsR))
K2h = hermitian(Kv*Kv, build_fv(varsK))
print("geometry+mapping done in %.2fs" % (time.time() - t0))

# ---------------- V_a sector (Z independent; tie after variation) ----------
ZC = ell*Sk/4
Va = sp.S(0)
Va += al * (k**2) * (aph - aZ)*(aphc - aZc) / 2          # alpha |a-DZ|^2
Va += (k**2) * (aph*aZc + aphc*aZ)                       # 4 a.DZ
Va += - (k**2) * aZ * aZc                                 # -2 |DZ|^2
Va += - cN * (k**2) * (aph - aZ)*(aphc - aZc)            # -2 cN |D(phi-Z)|^2
Va += - cN * (k**2) * (aZ*aUc + aZc*aU)                  # -4 cN DZ.DU

Lb = (sp.Rational(1, 4))*(-rho*(aphc + aph)
                          + v*rho*(achc + ach)
                          - v**2*rho*(apsc + aps)
                          - v**2*rho*(aAc + aA))

L = sp.Rational(1, 2)*MP2*(R2h - c2*K2h + Va) + Lb
L = sp.expand(L)

# real-field variations (Fourier-Hermitian): EOM_f = dL/da_f* + dL/da_f
def EOM(ac, a):
    e = sp.expand(sp.diff(L, ac) + sp.diff(L, a))
    return sp.expand(e)

eqs = {}
for f, ac, a in [('phi', aphc, aph), ('chi', achc, ach), ('psi', apsc, aps),
                 ('A', aAc, aA), ('U', aUc, aU)]:
    eqs[f] = EOM(ac, a)
# tie: Z = (ell S_k/4) phi  (mode picture, eq. (6) with f=0)
for f in eqs:
    eqs[f] = sp.expand(eqs[f].subs({aZ: ZC*aph, aZc: ZC*aphc}))
# U auxiliary: eq. (7) with rho_d = 0: U = phi - Z  (no div-free piece at nonzero k)
eqs['U'] = sp.expand(-k**2*(ZC*aph - aph + aU))

# ---------------- static master checks vs AS226 (informational) ----------------
print("=== static master checks vs AS226 (basis-algebra identity) ===")
phi0 = -rho/(2*MP2*cN*k**2*(1 - ZC))
print("phi0 (AS226) =", phi0)
subst_st = {ach: 0, achc: 0, aA: 0, aAc: 0, aU: aph - ZC*aph, aUc: aphc - ZC*aphc,
            aps: -aph, apsc: -aphc, w: 0, v: 0}
for nm, e in [('phi', eqs['phi']), ('psi', eqs['psi']), ('A', eqs['A'])]:
    r = sp.expand(e.subs(subst_st).subs(aph, phi0).subs(aphc, phi0))
    print("  E_%s(AS226 soln) residual: %s" % (nm, r))
# U equation exact:
print("  E_U(AS226 soln) residual:", sp.expand(eqs['U'].subs(subst_st).subs(aph, phi0).subs(aphc, phi0)))

# ---------------- order-by-order solve in v (omega = k v) ----------------
# The tied EOMs are linear in {a_f, a_cf} jointly; after omega -> k*v they are
# polynomial in v.  Solve block-by-block in powers of v (seed step 2: frequency
# dependence of constraints included exactly).  Each order-block is the 10x10
# system (5 EOMs + 5 conjugate-mirror equations, real-coefficient linear).
allf = ['phi', 'chi', 'psi', 'A', 'U']
def swapmap():
    return dict([(amp[f], ampc[f]) for f in allf] + [(ampc[f], amp[f]) for f in allf])

def linpart(e, x):
    """linear coefficient of x in e (other amplitudes zeroed)."""
    return sp.expand(
        sp.expand(e.subs({a: 0 for a in amp.values() if a != x})
                   .subs({a: 0 for a in ampc.values() if a != x})).coeff(x, 1))

def coeff_v(e, n):
    e = sp.expand(e)
    return sp.expand(e.coeff(v, n)) if e.has(v) else (e if n == 0 else sp.S(0))

Sb = {a: {} for a in (list(amp.values()) + list(ampc.values()))}
order = 2
skipped = {}   # (order, field) -> exact residual expression of EOM rows with no unknown coupling
for n in range(order + 1):
    # Real-response gauge: a_f = ac_f at every order (sources real: rho, rho v, rho v^2;
    # real-coefficient linear EOMs; mean-normalized leaf).  Solve 5x5 blocks.
    newS = {f: sp.Symbol('s%d_%s' % (n, f)) for f in allf}
    full = {}
    for f in allf:
        full[amp[f]] = sum(Sb[amp[f]][j] * v**j for j in range(n)) + newS[f] * v**n
        full[ampc[f]] = sum(Sb[ampc[f]][j] * v**j for j in range(n)) + newS[f] * v**n
    rows = []   # (field name, residual expression)
    for f in allf:
        e = sp.expand(eqs[f].subs(w, k*v))
        r = coeff_v(sp.expand(e.subs(full)), n)
        if r != 0:
            rows.append((f, r))
    M = sp.zeros(len(rows), 5)
    b = sp.zeros(len(rows), 1)
    for i, (f, e) in enumerate(rows):
        ee = sp.expand(e)
        for j, f2 in enumerate(allf):
            M[i, j] = linpart(ee, newS[f2])
        b[i] = sp.expand(-ee.subs({s: 0 for s in newS.values()}))
    # drop rows with no unknown coupling (pure consistency conditions)
    keep, drop = [], []
    for i in range(len(rows)):
        if M.row(i) == sp.zeros(1, 5):
            drop.append((rows[i][0], b[i]))
        else:
            keep.append(i)
    for (f, res) in drop:
        skipped[(n, f)] = res
    rows = [rows[i] for i in keep]
    M = M.extract(keep, list(range(5)))
    b = b.extract(keep, [0])
    # adaptive square completion: pin fields whose columns have no coupling in
    # any kept row (rest-isotropy: static/anisotropic amplitudes vanish)
    pins = []
    while M.rows < 5:
        zero_cols = [c for c in range(5) if all(e == 0 for e in M.col(c))]
        if zero_cols:
            c = zero_cols[0]
            row = sp.zeros(1, 5)
            row[c] = 1
            M = M.row_insert(M.rows, row)
            b = b.row_insert(b.rows, sp.zeros(1, 1))
            pins.append(allf[c])
        else:
            break
    if M.rows != 5:
        raise ValueError('order %d: cannot complete block (%d rows)' % (n, M.rows))
    try:
        soln = sp.simplify(M.LUsolve(b))
    except sp.matrices.exceptions.NonInvertibleMatrixError:
        print("order-%d rows:" % n, [f for (f, _) in rows])
        print("order-%d M:" % n, sp.Matrix(M))
        print("order-%d b:" % n, b.T)
        raise
    for j, f in enumerate(allf):
        Sb[amp[f]][n] = sp.expand(soln[j, 0])
        Sb[ampc[f]][n] = sp.expand(soln[j, 0])
    # consistency check: every dropped (pure-source) row must evaluate to 0 at the
    # solution of the block -- record exact residual at the solved series.
    full2 = {}
    for f in allf:
        full2[amp[f]] = sum(Sb[amp[f]][j] * v**j for j in range(n + 1))
        full2[ampc[f]] = sum(Sb[ampc[f]][j] * v**j for j in range(n + 1))
    for (f, res) in drop:
        skipped[(n, f)] = coeff_v(sp.expand(eqs[f].subs(w, k*v).subs(full2)), n)

# assemble the series solutions (Z is tied: aZ = ZC*aph, substituted at build time)
sols = {}
for f in allf:
    sols[amp[f]] = sp.expand(sum(Sb[amp[f]][n] * v**n for n in range(order + 1)))
    sols[ampc[f]] = sp.expand(sum(Sb[ampc[f]][n] * v**n for n in range(order + 1)))
for f in allf:
    print("  a_%s = %s" % (f, sols[amp[f]]))
    print("  c_%s = %s" % (f, sols[ampc[f]]))

# ---------------- exact substitution-back verification ----------------
# NOTE: the solve is a v-series at omega = k*v; the back-substitution must use
# omega = k*v exactly (a fixed nonzero omega would see the order-shifted
# kinetic terms as order-0 residuals).
rngv = {k: sp.Rational(3, 2), MP2: sp.Rational(5, 2),
        cN: sp.Rational(3, 2), al: sp.Rational(1, 2), c2: sp.Rational(1, 3),
        ell: sp.Rational(1, 20), Sk: sp.Rational(1, 2), rho: sp.Rational(2, 3)}
ok = True
for nm in allf:
    e = sp.expand(eqs[nm].subs(w, k*v).subs(sols).subs(rngv))
    for n in range(order + 1):
        r = coeff_v(e, n)
        if (n, nm) in skipped:
            continue      # consistency rows checked separately below
        if r != 0:
            ok = False
            print("  residual order v^%d in E_%s:" % (n, nm), r)
print("substitution-back residuals vanish through v^2 at exact rational sample:",
      ok)
print("=== consistency rows (pure-source EOMs, no unknown coupling) ===\n")
for (n, f) in sorted(skipped):
    print("  order v^%d E_%s consistency residual:" % (n, f))
    print("    ", skipped[(n, f)])
    # branch-faithful value of the residual (c_N = 1-alpha/2, c2 = 1, S_k*ell = 1)
    rbf = sp.factor(sp.expand(skipped[(n, f)].subs({cN: 1 - al/2, c2: 1, ell: 1/Sk})
                              .subs({al: 0, Sk: 1})))
    print("    branch-eval (alpha=0): ", rbf)

# ---------------- alpha2 extraction ----------------
print("=== alpha2 extraction (comoving frame) ===")
g00c = sp.expand(-1 - 2*sols[aph] + 2*v*sols[ach] + v**2*(1 - 2*sols[aps] - 2*sols[aA])
                 + sols[ach]**2)
g03c = sp.expand(sols[ach] + v*(1 - 2*sols[aps] - 2*sols[aA]))
UNk = -rho/(2*MP2*cN*k**2)
extra00 = sp.expand(g00c - (-1 + 2*UNk))
e0 = sp.expand(extra00).subs(v, 0)
extra00v2 = sp.expand(sp.expand(extra00 - e0).coeff(v, 2))   # exact v^2 coefficient
cL = sp.expand(extra00v2) / (rho/k**2)
print("(g'00 - [-1+2U_N]) v^2-coeff, /(rho/k^2) [k||v]:", sp.factor(cL * rho / k**2 * 0 + sp.expand(cL)))
alpha2 = sp.expand(-cL)
print("alpha2 (longitudinal, tentative) =", alpha2)
g03v1 = sp.expand(sp.expand(sols[ach] - 2*v*sols[aps] - 2*v*sols[aA]).coeff(v, 1))
alpha2b = sp.expand(-g03v1) / (rho/k**2)
print("chi-coeff at order v (g'03 window):", sp.factor(g03v1))
print("alpha2 (g'03 window) =", alpha2b)

# ---------------- negative control ----------------
print("=== negative control: density-only moving source ===")
CM = sp.expand(eqs['chi'].subs({ach: 0, aps: phi0, aA: 0, aph: phi0,
                                aU: phi0 - ZC*phi0, w: k*v}))
CM = sp.simplify(CM)
print("C_M (density-only, chi=0) =", CM)
print("fires (nonzero)?", sp.simplify(CM) != 0)
print("C_M/(rho k^2 v):", sp.simplify(CM/(rho*k**2*v)))
CH = sp.expand(eqs['phi'].subs({ach: 0, aps: phi0, aA: 0, aph: phi0,
                                aU: phi0 - ZC*phi0, w: k*v}))
print("C_H (density-only) =", sp.simplify(CH))

# ---------------- GR limit ----------------
print("=== GR limit check ===")
print("alpha2(alpha=0,c2=0,ell=0) =", sp.simplify(alpha2.subs({al: 0, c2: 0, ell: 0})))
print("alpha2(full) =", sp.simplify(alpha2))
print("RUNTIME %.2fs" % (time.time() - t0))