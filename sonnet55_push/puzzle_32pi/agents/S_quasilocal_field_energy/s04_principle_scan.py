"""s04: the pre-declared budget principles (PREDECLARED_PRINCIPLES.md, written before any script was run), solved for xi = a0^2/(G rho).
Units a0 = G = c = 1  =>  G rho = 1/xi,  H^2 = 8 pi/(3 xi),  L = sqrt(3 xi/(8 pi)),  R_a = 1,  r_sa = 1/2,  M_a = 1,  M_s = 1/4,  M_dS = L/2.
Every entry is an equation LHS(xi) = RHS(xi); roots xi > 0 are found on a log grid (floats) and refined with mpmath (40 digits).
Outputs: entry table (rho-free identities / inconsistent / rho-dependent), pi-class of every root, Z = sqrt((8 pi/3)/xi), exact hits at the target xi = 1/4
(compared only here, at the end), decoy hit rates, the mutation E_vac: 4 pi/3 -> 4 pi, and the planted controls II3, V3.
"""
import math, itertools, sys
import mpmath as mp
mp.mp.dps = 40
PI = math.pi

# ----------------------------------------------------------------------------- helpers
def consts(xi, mm, evac_coeff):
    pi = mm.pi
    rho = 1/xi
    L = mm.sqrt(3*xi/(8*pi))
    H = 1/L
    Evac = lambda R: evac_coeff(pi)*rho*R**3
    return pi, rho, L, H, Evac

def entry_typeIII(D, rin_kind, Rk, Mk, Tk, evac_coeff):
    def f(xi, mm):
        pi, rho, L, H, Evac = consts(xi, mm, evac_coeff)
        R = {'L': L, 'Ra': 1, 'rsa': 0.5*(1 + 0*xi)}[Rk]
        M = {'Ma': 1 + 0*xi, 'Ms': 0.25 + 0*xi, 'MdS': L/2, 'Mvac': Evac(R), 'MM': R**2}[Mk]
        rin = {'0': 0*xi, 'rM': mm.sqrt(M), 'rs': 2*M}[rin_kind]
        if not (R > rin):
            return None
        if D == 0:
            E = M*(R - rin)/2
        else:
            if rin == 0:
                return None
            E = (M**1.5)*mm.log(R/rin)/3*(1 if D == 1 else 2)
        T = {'M': M, 'Evac': Evac(R), 'hor': R/2}[Tk]
        return E, T
    return f

def name_III(D, rin_kind, Rk, Mk, Tk):
    return "III D%d r_in=%s R=%s M=%s T=%s" % (D, rin_kind, Rk, Mk, Tk)

def build_entries(evac_coeff):
    ents = []      # (label, family, func, uses_log)
    # TYPE I
    ents.append(("I1 w0(a0)=rho", 'I', lambda xi, mm: (1/(8*mm.pi), 1/xi), False))
    ents.append(("I2 w1(a0)=rho", 'I', lambda xi, mm: (1/(12*mm.pi), 1/xi), False))
    ents.append(("I3 w2(a0)=rho", 'I', lambda xi, mm: (1/(6*mm.pi), 1/xi), False))
    for k in (0, 1, 2):
        for Mk in ('Ma', 'Ms', 'MdS'):
            def f(xi, mm, k=k, Mk=Mk):
                pi, rho, L, H, Evac = consts(xi, mm, evac_coeff)
                M = {'Ma': 1 + 0*xi, 'Ms': 0.25 + 0*xi, 'MdS': L/2}[Mk]
                rstar = mm.sqrt(mm.sqrt(M))/H              # r*^2 = sqrt(G M a0)/H^2
                g = H**2*rstar
                w = [g**2/(8*pi), g**3/(12*pi), g**3/(6*pi)][k]
                return w, rho
            ents.append(("I4 w%d at r_zg, M=%s" % (k, Mk), 'I', f, False))
    # TYPE II
    for ell in ('Ra', 'rsa', 'L'):
        def f(xi, mm, ell=ell):
            pi, rho, L, H, Evac = consts(xi, mm, evac_coeff)
            l = {'Ra': 1 + 0*xi, 'rsa': 0.5 + 0*xi, 'L': L}[ell]
            return 1/(8*pi), rho*l
        ents.append(("II1 s_BY(a0)=rho*ell, ell=%s" % ell, 'II', f, False))
    for ell in ('L', 'Ra', 'rsa'):
        def f(xi, mm, ell=ell):
            pi, rho, L, H, Evac = consts(xi, mm, evac_coeff)
            l = {'Ra': 1 + 0*xi, 'rsa': 0.5 + 0*xi, 'L': L}[ell]
            return H/(8*pi), rho*l
        ents.append(("II2 T_dS sigma = rho*ell, ell=%s" % ell, 'II', f, False))
    ents.append(("II3 PLANTED restatement: rho/a0 = 32 pi T_U sigma", 'II', lambda xi, mm: (1/xi, 32*mm.pi*(1/(8*mm.pi))), False))
    # TYPE IV
    for R_ in (1.0, 0.5):
        def f(xi, mm, R_=R_):
            pi, rho, L, H, Evac = consts(xi, mm, evac_coeff)
            E = Evac(R_)
            return 3*E**2/(5*R_), E
        ents.append(("IV1 |U_self| = E_vac(R), R=%s" % ("Ra" if R_ == 1.0 else "rsa"), 'IV', f, False))
    # TYPE V
    for R_ in (1.0, 0.5):
        def f1(xi, mm, R_=R_):
            pi, rho, L, H, Evac = consts(xi, mm, evac_coeff)
            return 0.5 + 0*xi, Evac(R_)
        ents.append(("V1 E_BY(r_sa)=r_sa/G = E_vac(R), R=%s" % ("Ra" if R_ == 1.0 else "rsa"), 'V', f1, False))
        def f2(xi, mm, R_=R_):
            pi, rho, L, H, Evac = consts(xi, mm, evac_coeff)
            return 0.125 + 0*xi, Evac(R_)
        ents.append(("V2 T S = M_s/2 = E_vac(R), R=%s" % ("Ra" if R_ == 1.0 else "rsa"), 'V', f2, False))
    ents.append(("V3 PLANTED restatement: G rho A(r_sa) = 4 pi", 'V', lambda xi, mm: (mm.pi*(1/xi), 4*mm.pi), False))
    # TYPE III grid
    for D in (0, 1, 2):
        rins = ('0', 'rM', 'rs') if D == 0 else ('rM', 'rs')
        for rin_kind, Rk, Mk, Tk in itertools.product(rins, ('L', 'Ra', 'rsa'), ('Ma', 'Ms', 'MdS', 'Mvac', 'MM'), ('M', 'Evac', 'hor')):
            ents.append((name_III(D, rin_kind, Rk, Mk, Tk), 'III', entry_typeIII(D, rin_kind, Rk, Mk, Tk, evac_coeff), D > 0))
    return ents

def evaluate(fn, xi, mm):
    try:
        out = fn(xi, mm)
    except (ValueError, ZeroDivisionError, OverflowError):
        return None
    return out

GRID = [10**(-6 + 12*i/900) for i in range(901)]
def find_roots(fn):
    vals = []
    for xi in GRID:
        out = evaluate(fn, xi, math)
        vals.append(None if out is None else out[0] - out[1])
    roots = []
    for i in range(len(GRID) - 1):
        a, b = vals[i], vals[i+1]
        if a is None or b is None:
            continue
        if a == 0:
            roots.append(mp.mpf(GRID[i])); continue
        if a*b < 0:
            def h(xv):
                o = fn(xv, mp)
                return o[0] - o[1]
            try:
                r = mp.findroot(h, (mp.mpf(GRID[i]), mp.mpf(GRID[i+1])), solver='anderson', tol=1e-30, maxsteps=200)
                if r > 0 and abs(h(r)) < 1e-20*max(1, abs(fn(r, mp)[1])):
                    roots.append(r)
            except Exception:
                pass
    # deduplicate
    uniq = []
    for r in roots:
        if not any(abs(r/u - 1) < 1e-15 for u in uniq):
            uniq.append(r)
    return uniq, vals

def rho_dependence(fn):
    outs = []
    for xi in (0.37, 0.91, 2.9, 7.3, 31.0, 0.011, 113.0):
        o = evaluate(fn, xi, math)
        if o is not None:
            outs.append(o)
    if len(outs) < 2:
        return 'undefined'
    # identity: LHS == RHS for every sampled xi (both may depend on xi through L, rho, M(xi))
    if all(abs(o[0] - o[1]) <= 1e-12*max(abs(o[0]), abs(o[1]), 1e-300) for o in outs):
        return 'identity'
    # xi-independent but unequal
    if all(abs(o[0] - outs[0][0]) < 1e-12*max(1, abs(outs[0][0])) for o in outs) and all(abs(o[1] - outs[0][1]) < 1e-12*max(1, abs(outs[0][1])) for o in outs):
        return 'inconsistent'
    return 'rho-dependent'

from fractions import Fraction
def pi_class(x, uses_log):
    """Return (label, kind).  Finds the smallest degree k <= 8 and exponent j such that (x / pi^j)^k is rational (pslq), preferring j = 1, 0, -1, 2, -2, 3, -3.
    kind: 'Q' (xi rational), 'Qpi' (xi = q pi^j, k = 1, j != 0), 'algebraic*pi^j' (k > 1), 'log' (D1/D2 entries), 'other'."""
    if uses_log:
        return 'log/other', 'log'
    for k in range(1, 9):
        for j in (1, 0, -1, 2, -2, 3, -3):
            q = (x/mp.pi**j)**k
            rel = mp.pslq([q, 1], maxcoeff=10**11, maxsteps=100000, tol=mp.mpf(10)**-27)
            if rel is not None and rel[0] != 0 and rel[1] != 0:
                frac = Fraction(-rel[1], rel[0])
                lab = ("xi" if j == 0 else "xi/pi^%d" % j) + (" = " if k == 1 else " has (.)^%d = " % k) + str(frac)
                if k == 1 and j == 0:
                    kind = 'Q'
                elif k == 1:
                    kind = 'Qpi^%d' % j
                else:
                    kind = 'algebraic*pi^%d' % j
                return lab, kind
    for j in (1, 0, -1):
        poly = mp.findpoly(x/mp.pi**j, 4, maxcoeff=100000, tol=mp.mpf(10)**-24)
        if poly is not None:
            return 'xi/pi^%d is algebraic (poly %s)' % (j, poly), 'algebraic*pi^%d' % j
    return 'other', 'other'

TARGET = mp.mpf(1)/4
DECOYS = {'1/2': mp.mpf(1)/2, '1/3': mp.mpf(1)/3, '1/6': mp.mpf(1)/6, '1/8': mp.mpf(1)/8, '1/5': mp.mpf(1)/5, '2/3': mp.mpf(2)/3,
          '3/4': mp.mpf(3)/4, '1/16': mp.mpf(1)/16, '2/(3pi)': 2/(3*mp.pi), '2pi/27': 2*mp.pi/27, '1/(4pi)': 1/(4*mp.pi)}

def run(evac_coeff, label, verbose=True):
    ents = build_entries(evac_coeff)
    table = []
    for (lab, fam, fn, uses_log) in ents:
        cls = rho_dependence(fn)
        roots = []
        if cls in ('rho-dependent', 'undefined'):
            roots, _ = find_roots(fn)
            if cls == 'undefined' and not roots:
                cls = 'undefined/empty'
        table.append((lab, fam, cls, roots, uses_log))
    return table

if __name__ == '__main__':
    ok = []
    def chk(n, c):
        ok.append(bool(c)); print(("PASS " if c else "FAIL ") + n)

    table = run(lambda pi: 4*pi/3, "baseline")
    n_all = len(table)
    counts = {}
    for (lab, fam, cls, roots, ul) in table:
        counts[cls] = counts.get(cls, 0) + 1
    print("entries:", n_all, " classification:", counts)
    fam_counts = {}
    for (lab, fam, cls, roots, ul) in table:
        fam_counts.setdefault(fam, {}).setdefault(cls, 0)
        fam_counts[fam][cls] += 1
    print("by family:", fam_counts)

    # ---------------- rho-dependent entries with roots
    print("\n=== rho-dependent entries and their roots (xi = a0^2/(G rho); Z = sqrt((8 pi/3)/xi)) ===")
    rows = []
    for (lab, fam, cls, roots, ul) in table:
        if cls == 'rho-dependent' and roots:
            for r_ in roots:
                Z = mp.sqrt((8*mp.pi/3)/r_)
                pc, kind = pi_class(r_, ul)
                rows.append((lab, fam, r_, Z, pc, kind))
    for (lab, fam, r_, Z, pc, kind) in rows:
        if fam != 'III':
            print("  %-58s xi = %-22s Z = %-10s  %s" % (lab, mp.nstr(r_, 15), mp.nstr(Z, 8), pc))
    n_III_rows = sum(1 for r_ in rows if r_[1] == 'III')
    n_III_entries = sum(1 for e in table if e[1] == 'III')
    print("  TYPE III grid: %d entries, %d rho-dependent (entry, root) pairs with a positive root (listed in the .tsv-like block below)" % (n_III_entries, n_III_rows))
    print("\n  TYPE III roots:")
    for (lab, fam, r_, Z, pc, kind) in rows:
        if fam == 'III':
            print("  %-48s xi = %-20s Z = %-9s %s" % (lab, mp.nstr(r_, 12), mp.nstr(Z, 6), pc))

    # ---------------- rho-free entries
    idn = [e for e in table if e[2] == 'identity']
    inc = [e for e in table if e[2] == 'inconsistent']
    print("\n=== rho-free entries: %d identities (scale-free: fix nothing), %d inconsistent (no xi-content), %d rho-dependent without positive root, %d undefined/empty ===" % (
        len(idn), len(inc), sum(1 for e in table if e[2] == 'rho-dependent' and not e[3]), sum(1 for e in table if e[2].startswith('undefined'))))
    for e in idn:
        print("  identity:", e[0])
    for e in inc:
        print("  inconsistent (rho-free, LHS != RHS for every rho):", e[0])

    # ---------------- cross-check of the TYPE III energies against direct quadrature (independent of the closed forms)
    def g_of(M_, r_): return mp.sqrt(M_)/r_
    w = {0: lambda gg: gg**2/(8*mp.pi), 1: lambda gg: gg**3/(12*mp.pi), 2: lambda gg: gg**3/(6*mp.pi)}
    allmatch = True
    for (D, rk, Rk, Mk) in [(0, '0', 'Ra', 'Ma'), (0, 'rM', 'L', 'MdS'), (1, 'rM', 'L', 'Mvac'), (2, 'rs', 'L', 'Ma'), (1, 'rM', 'Ra', 'Ms'), (2, 'rM', 'rsa', 'Ms')]:
        fn = entry_typeIII(D, rk, Rk, Mk, 'M', lambda pi: 4*pi/3)
        xi0 = mp.mpf('0.37') if Mk != 'Ma' else mp.mpf('2.9')
        o = evaluate(fn, xi0, mp)
        if o is None:
            print("   (cross-check skipped: empty entry)", D, rk, Rk, Mk); continue
        pi_, rho_, L_, H_, Evac_ = consts(xi0, mp, lambda pi: 4*pi/3)
        R_ = {'L': L_, 'Ra': mp.mpf(1), 'rsa': mp.mpf(1)/2}[Rk]
        M_ = {'Ma': mp.mpf(1), 'Ms': mp.mpf(1)/4, 'MdS': L_/2, 'Mvac': Evac_(R_)}[Mk]
        rin_ = {'0': mp.mpf(0), 'rM': mp.sqrt(M_), 'rs': 2*M_}[rk]
        Eq = mp.quad(lambda rr: 4*mp.pi*rr**2*w[D](g_of(M_, rr)), [rin_, R_])
        allmatch = allmatch and abs(Eq/o[0] - 1) < 1e-15
    chk("S0 TYPE III energies used in the scan equal direct mpmath quadrature of the density (six sampled entries, D0/D1/D2)", allmatch)

    # ---------------- hits
    def hits_for(target, tab, tol=mp.mpf('1e-9')):
        h = []
        for (lab, fam, cls, roots, ul) in tab:
            for r_ in roots:
                if abs(r_/target - 1) < tol:
                    h.append((lab, r_))
        return h
    def near_for(target, tab, tol):
        n = 0
        for (lab, fam, cls, roots, ul) in tab:
            for r_ in roots:
                if abs(r_/target - 1) < tol:
                    n += 1
        return n
    h_t = hits_for(TARGET, table)
    print("\n=== exact hits (rel. 1e-9) at the target xi = 1/4 ===")
    for lab, r_ in h_t:
        print("  HIT:", lab, mp.nstr(r_, 20))
    planted = [lab for lab, r_ in h_t if 'PLANTED' in lab]
    genuine = [lab for lab, r_ in h_t if 'PLANTED' not in lab]
    chk("S1 the scan detects both planted restatements (II3, V3) at xi = 1/4", len(planted) == 2)
    print("   non-planted exact hits at the target:", len(genuine), genuine)
    print("\n=== decoy calibration: exact hits (1e-9) and near hits within 2% / 10% ===")
    tot_pairs = sum(len(e[3]) for e in table if e[2] == 'rho-dependent')
    print("  total (entry, root) pairs:", tot_pairs)
    for name, d in list(DECOYS.items()) + [('TARGET 1/4', TARGET)]:
        hx = hits_for(d, table)
        print("  %-10s exact hits %d (non-planted %d) ; within 2%%: %d ; within 10%%: %d" % (name, len(hx), sum(1 for l, r_ in hx if 'PLANTED' not in l), near_for(d, table, mp.mpf('0.02')), near_for(d, table, mp.mpf('0.10'))))
    dec_exact_nonplanted = sum(1 for name, d in DECOYS.items() for l, r_ in hits_for(d, table) if 'PLANTED' not in l)
    print("  decoy exact hits (non-planted, all 11 decoys):", dec_exact_nonplanted)

    # ---------------- pi-class census of rho-dependent roots
    print("\n=== pi-class census of all rho-dependent roots ===")
    nonplanted = [r_ for r_ in rows if 'PLANTED' not in r_[0]]
    # distinct equations: dedupe by root value (many grid entries coincide, e.g. M_dS = E_vac(L))
    distinct = []
    for r_ in nonplanted:
        if not any(abs(r_[2]/d[2] - 1) < 1e-12 for d in distinct):
            distinct.append(r_)
    census = {}
    for (lab, fam, r_, Z, pc, kind) in nonplanted:
        census[kind] = census.get(kind, 0) + 1
    census_d = {}
    for (lab, fam, r_, Z, pc, kind) in distinct:
        census_d[kind] = census_d.get(kind, 0) + 1
    print("  non-planted (entry, root) pairs:", len(nonplanted), census)
    print("  distinct root values (distinct equations):", len(distinct), census_d)
    print("   (Q = pi-free rational xi, the class of the target 1/4; Qpi^j = rational x pi^j; algebraic*pi^j = algebraic (degree k) x pi^j; log = D1/D2 entries with ln)")
    Q_only = [(lab, mp.nstr(r_, 12), pc) for (lab, fam, r_, Z, pc, kind) in nonplanted if kind == 'Q']
    print("  non-planted entries whose xi is a pure rational (the class of the target):", len(Q_only), Q_only)
    # Lambda held fixed: a0^2/Lambda = xi/(8 pi)
    lam_kind = {}
    for (lab, fam, r_, Z, pc, kind) in distinct:
        if kind in ('Q',) or kind.startswith('Qpi') or kind.startswith('algebraic'):
            q = r_/(8*mp.pi)
            found = None
            rel = mp.pslq([q, 1], maxcoeff=10**11, maxsteps=100000, tol=mp.mpf(10)**-27)
            if rel is not None and rel[0] != 0 and rel[1] != 0:
                found = 'Q'
            else:
                poly = mp.findpoly(q, 4, maxcoeff=100000, tol=mp.mpf(10)**-24)
                if poly is not None:
                    found = 'algebraic (degree %d)' % (len(poly) - 1)
            lam_kind[found or 'other'] = lam_kind.get(found or 'other', 0) + 1
    print("  Lambda held fixed (a0^2/Lambda = xi/(8 pi)): class of the distinct non-log roots:", lam_kind)
    print("  target: a0^2/Lambda = 1/(32 pi) (NOT rational);  in the G rho variable xi = 1/4 (rational).  Budget principles land on the OTHER side in both variables.")

    # ---------------- data-compatibility window (declared here, comparison only)
    zlo, zhi = mp.mpf('4.8'), mp.mpf('6.6')
    dc = [(lab, mp.nstr(r_, 8), mp.nstr(Z, 6)) for (lab, fam, r_, Z, pc, kind) in rows if zlo <= Z <= zhi]
    print("\n=== entries whose Z lies in the data-compatible window [4.8, 6.6] (footing dependent): %d of %d roots ===" % (len(dc), len(rows)))
    for d in dc:
        print("     ", d)

    # ---------------- mutation: E_vac 4 pi/3 -> 4 pi
    table_m = run(lambda pi: 4*pi, "mutated")
    changed = 0; compared = 0
    for a, b in zip(table, table_m):
        if a[2] == 'rho-dependent' and b[2] == 'rho-dependent':
            compared += 1
            ra = sorted([float(x) for x in a[3]]); rb = sorted([float(x) for x in b[3]])
            if len(ra) != len(rb) or any(abs(x/y - 1) > 1e-9 for x, y in zip(ra, rb)):
                changed += 1
    print("\n=== mutation E_vac: 4 pi/3 -> 4 pi: %d of %d rho-dependent entries change their roots ===" % (changed, compared))
    chk("S2 mutation control: the E_vac coefficient is felt by the scan (many entries change)", changed > 30)
    h_m = [l for l, r_ in hits_for(TARGET, table_m) if 'PLANTED' not in l]
    print("   non-planted exact hits at 1/4 after mutation:", len(h_m), h_m)

    # ---------------- mutation 2: remove the pi from the vacuum volume (E_vac = (4/3) rho R^3): the pi-class census must SEE the change
    table_m2 = run(lambda pi: mp.mpf(4)/3, "no-pi volume")
    rows2 = []
    for (lab, fam, cls, roots, ul) in table_m2:
        if cls == 'rho-dependent' and 'PLANTED' not in lab:
            for r_ in roots:
                pc, kind = pi_class(r_, ul)
                rows2.append((lab, kind))
    c2 = {}
    for lab, kind in rows2:
        c2[kind] = c2.get(kind, 0) + 1
    print("\n=== mutation 2: E_vac = (4/3) rho R^3 (pi removed by hand): census of (entry, root) pairs:", c2)
    n_Q_2 = c2.get('Q', 0)
    chk("S2b mutation control: with the pi removed from the volume, some budget entries become pi-free rational (the census can see a change of class; the baseline has none)", n_Q_2 > 0)
    print("   entries that become rational:", [lab for lab, kind in rows2 if kind == 'Q'][:12])

    # ---------------- verdict lines
    chk("S3 no non-planted exact hit at xi = 1/4 in the declared menu", len(genuine) == 0)
    chk("S4 no non-planted rho-dependent root is a pure rational at all (pi-free xi never arises from an energy budget in the menu)", len(Q_only) == 0)
    print("\nTOTAL", sum(ok), "/", len(ok), "pass;", len(ok) - sum(ok), "fail")
