#!/usr/bin/env python3
"""
Mode analysis for the reduced scalar system (from L2s checkpoint):
 - numeric branch structure omega^2(k), mode vectors, mode ENERGIES (ghost diagnostic),
 - stability scan over K_B and K2 (the no-ghost / stability window),
 - clean symbolic limits: H->0 sub-horizon dispersion, the (K_B - 2) factor, switch-offs.
Frozen-background WKB: trustworthy for omega, k >> H; k -> 0 rows are formal.
"""
import sympy as sp
import numpy as np
import time, sys, functools, itertools
print = functools.partial(print, flush=True)
t0 = time.time()
def banner(s): print("\n" + "="*100 + "\n" + s + "\n" + "="*100)
def check(cond, label):
    print(("  [PASS] " if cond else "  [FAIL] ") + label)
    if not cond: print("  *** HARD FAIL ***"); sys.exit(1)

k   = sp.Symbol('k', positive=True)
G   = sp.Symbol('G', positive=True)
Lam = sp.Symbol('Lam', real=True)
KB  = sp.Symbol('K_B', real=True)
Ab  = sp.Symbol('A_b', real=True)
ub  = sp.Symbol('u_b', real=True)
K0, K1, K2 = sp.symbols('K0 K1 K2', real=True)
A0cp = sp.Symbol('A0cp', positive=True)
p0, s0, x0, a0v = sp.symbols('p0 s0 x0 a0v', real=True)
s1, x1, a1v, p1 = sp.symbols('s1 x1 a1v p1', real=True)
Hh  = sp.Symbol('H', real=True)
av  = sp.Symbol('a_v', positive=True)
Qbs = sp.Symbol('Qb', real=True)
FRIEDMANN = [(Lam, 3*Hh**2 - 8*sp.pi*G*(Qbs*K1 - K0))]

L2s = sp.sympify(open('L2s_checkpoint.txt').read())
cP  = sp.expand(sp.diff(L2s, p0))
AP  = sp.expand(sp.diff(cP, p0)/2)
cP0 = sp.expand(cP.subs(p0, 0))
Lred_num = sp.expand((4*AP*L2s.subs(p0, 0) - cP0**2).subs(FRIEDMANN))
APf = sp.factor(AP.subs(FRIEDMANN))
vels = [s1, x1, a1v]; flds = [s0, x0, a0v]
names = ["Psi", "chi", "alpha"]

# L = (1/2) v^T T v + v^T C q + (1/2) q^T U q   (all times 1/(4AP))
Tm = sp.Matrix(3,3, lambda i,j: sp.diff(Lred_num, vels[i], vels[j])/2)
Um = sp.Matrix(3,3, lambda i,j: sp.diff(Lred_num, flds[i], flds[j])/2)
Cm = sp.Matrix(3,3, lambda i,j: sp.diff(sp.diff(Lred_num, vels[i]), flds[j]))
print("built T, C, U numerators (%.1f s); T rank on-shell = %d" % (time.time()-t0, Tm.rank()))

banner("NUMERIC MODE ANALYSIS -- roots omega^2, mode vectors, mode energies (ghost diagnostic)")
argsyms = (G, av, Hh, Qbs, K0, K1, K2, Ab, ub, A0cp, KB, k)
Tf = sp.lambdify(argsyms, Tm, 'numpy')
Uf = sp.lambdify(argsyms, Um, 'numpy')
Cf = sp.lambdify(argsyms, Cm, 'numpy')
APl = sp.lambdify(argsyms, APf, 'numpy')

def mode_analysis(p, KBv, kv, verbose=True):
    vals = (p['G'], p['av'], p['H'], p['Qb'], p['K0'], p['K1'], p['K2'],
            p['Ab'], p['ub'], p['A0cp'], KBv, kv)
    T = np.array(Tf(*vals), float); U = np.array(Uf(*vals), float); C = np.array(Cf(*vals), float)
    ap4 = 4*APl(*vals)
    T, U, C = T/ap4, U/ap4, C/ap4
    A = C - C.T
    # quadratic eigenproblem [-w^2 T + i w A - U] v = 0 -> linearize
    n = 3
    Z, I = np.zeros((n,n)), np.eye(n)
    # state (q, qd): qdd from T qdd + A qd - U q = 0 where T singular -> use generalized eig:
    # [[ -U, 0],[0, T]] ? cleaner: polynomial eigen via companion with pencil:
    # ( w^2 [T] - i w [A] + [U'] ) v = 0 with U' = -U ... build lambda-matrix pencil:
    # generalized linearization: [[ -iA? ...]] -- use scipy.linalg.eig on pencil:
    #   [ 0   I ] [v]         [ I  0 ] [v]
    #   [ U'  A'] [wv]  = w   [ 0  T ] [wv]   with U'v + A' (w v) = w T (w v)
    # EL: -w^2 T v + i w A v - U'' v = 0  with U'' = U (from L: EL = T qdd + A qd - U q)
    # => w^2 T v = i w A v - U v.  Set u = w v:  w T u = i A u - U v ; w v = u.
    import scipy.linalg as sla
    LHS = np.block([[Z, I], [-U.astype(complex), 1j*A]])
    RHS = np.block([[I, Z], [Z, T]])
    w_all, V = sla.eig(LHS, RHS)
    out = []
    for i, wv in enumerate(w_all):
        if not np.isfinite(wv): continue
        v = V[:n, i]
        nrm = np.linalg.norm(v)
        if nrm < 1e-12: continue
        v = v/nrm
        w2 = wv**2
        Tq = np.real(np.conj(v)@T@v); Uq = np.real(np.conj(v)@U@v)
        E = 0.25*(np.abs(wv)**2*Tq - Uq)  # time-averaged energy of the mode
        out.append((np.real(w2), np.imag(w2), np.real(wv), np.imag(wv), Tq, E))
    out.sort(key=lambda r: abs(r[0]))
    return out, T, U

pars = dict(G=1.0, av=1.0, H=0.05, Qb=1.0, K0=-0.10, K1=0.02, K2=0.40, Ab=0.01, ub=1e-3, A0cp=1.0)
print("baseline: K1=%.3g (charge n), K2=%.3g (K''), Ab=%.3g, ub=%.3g, H=%.3g" %
      (pars['K1'], pars['K2'], pars['Ab'], pars['ub'], pars['H']))
print("%8s | %s" % ("k", "distinct omega^2 roots (re, im)  [v* T v]  [energy E]"))
for kv in [10.0, 100.0, 1000.0, 10000.0]:
    out, T, U = mode_analysis(pars, 0.5, kv)
    seen = []
    row = []
    for r in out:
        key = (round(r[0], 8), round(r[1], 8))
        if any(abs(key[0]-s[0]) < 1e-6*max(1, abs(key[0])) and abs(key[1]-s[1]) < 1e-8 for s in seen): continue
        seen.append(key)
        row.append("w2=%.5g%+.2gi Tv=%.3g E=%.4g" % (r[0], r[1], r[4], r[5]))
    print("%8g | %s" % (kv, " ; ".join(row)))

banner("STABILITY SCAN -- reality of omega (no exponential growth) and energy signs, k = 1e3")
def verdict(p, KBv):
    out, T, U = mode_analysis(p, KBv, 1e3, verbose=False)
    w2s = [r[0] for r in out]; ims = [abs(r[3]) for r in out]; Es = [r[5] for r in out]
    grow = max(ims) if ims else 0.0
    minw2 = min(w2s) if w2s else 0.0
    minE = min(Es) if Es else 0.0
    return grow, minw2, minE
hdr = "%28s | %12s %12s %12s | %s"
print(hdr % ("case", "max|Im w|", "min Re w2", "min E", "verdict"))
cases = []
for KBv in [-0.5, 0.1, 0.5, 1.0, 1.5, 1.9, 2.1, 3.0]:
    cases.append(("K_B=%g, K2=+0.4" % KBv, dict(pars), KBv))
pbad = dict(pars); pbad['K2'] = -0.4
cases.append(("K_B=0.5, K2=-0.4 (ghost K'')", pbad, 0.5))
pneg = dict(pars); pneg['K1'] = -0.02
cases.append(("K_B=0.5, K1<0 (negative charge)", pneg, 0.5))
poff = dict(pars); poff['K1'] = 0.0; poff['Ab'] = 0.0; poff['ub'] = 0.0
cases.append(("K1=Ab=ub=0 (pure vacuum)", poff, 0.5))
for lab, p, KBv in cases:
    g, mw, mE = verdict(p, KBv)
    v = "STABLE" if (g < 1e-8 and mw > -1e-8) else "UNSTABLE"
    if mE < -1e-12: v += " + NEGATIVE-ENERGY MODE"
    print(hdr % (lab, "%.3g" % g, "%.5g" % mw, "%.4g" % mE, v))

banner("SYMBOLIC -- sub-horizon (H -> 0) dispersion; the (K_B - 2) factor; switch-offs")
w = sp.Symbol('omega')
acc = sp.symbols('s2 x2 a2v', real=True)
def ddt_frozen(e):
    out = 0
    for f, v in zip(flds, vels): out += sp.diff(e, f)*v
    for v, aa in zip(vels, acc): out += sp.diff(e, v)*aa
    return out
EL = [sp.expand(ddt_frozen(sp.diff(Lred_num, vels[i])) - sp.diff(Lred_num, flds[i])) for i in range(3)]
hat = sp.symbols('hS hX hA', real=True)
subw = (list(zip(acc, [-w**2*h for h in hat]))
        + list(zip(vels, [sp.I*w*h for h in hat]))
        + list(zip(flds, hat)))
Msys = sp.Matrix(3,3, lambda i,j: sp.diff(sp.expand(EL[i].subs(subw, simultaneous=True)), hat[j]))
D = sp.expand(Msys.det())
Dp = sp.Poly(D, w)
d0 = sp.expand(Dp.coeff_monomial(1)); d2 = sp.expand(Dp.coeff_monomial(w**2)); d4 = sp.expand(Dp.coeff_monomial(w**4))
print("built det M (%.1f s)" % (time.time()-t0))

d0H0 = sp.factor(sp.expand(d0.subs(Hh, 0)))
d2H0 = sp.factor(sp.expand(d2.subs(Hh, 0)))
d4H0 = sp.factor(sp.expand(d4.subs(Hh, 0)))
print("\n  H -> 0 (sub-horizon):")
print("  d0|H=0 =", d0H0)
print("  d2|H=0 =", d2H0)
print("  d4|H=0 =", d4H0)
softH0 = sp.cancel(-d0H0/d2H0)
print("\n  soft branch omega^2 |H=0 =", sp.factor(softH0))
hardH0 = sp.cancel(-d2H0/d4H0)
print("  hard branch omega^2 ~ -d2/d4 |H=0 =", sp.factor(hardH0))
# small-k expansions of both, H=0
try:
    print("\n  soft branch, k->0 (H=0):", sp.factor(sp.expand(sp.series(softH0, k, 0, 5).removeO())))
except Exception as e: print("  soft k->0 failed:", e)
try:
    print("  hard branch, k->0 (H=0):", sp.factor(sp.expand(sp.series(hardH0, k, 0, 5).removeO())))
except Exception as e: print("  hard k->0 failed:", e)
# k->infinity
def klead(e):
    e = sp.cancel(sp.together(e)); num, den = sp.fraction(e)
    pn, pd = sp.Poly(num, k), sp.Poly(den, k)
    return sp.factor(pn.coeff_monomial(k**pn.degree())/pd.coeff_monomial(k**pd.degree())*k**(pn.degree()-pd.degree()))
print("\n  soft branch, k->inf (H=0):", klead(softH0))
print("  hard branch, k->inf (H=0):", klead(hardH0))

# the (K_B-2) factor: last bracket of d0 at k->inf
print("\n  KEY: the k^4 coefficient inside d0's last factor is (K_B - 2):")
lastfac = sp.factor(sp.expand(d0.subs([(Ab, 0)])))
print("  d0[Ab=0] =", lastfac)
print("\n  switch-offs (exact):")
print("   d0[K1=0, Ab*ub^2=0] =", sp.simplify(sp.expand(d0.subs([(K1, 0), (Ab, 0)]))))
print("   d2[K1=0, Ab*ub^2=0] =", sp.factor(sp.expand(d2.subs([(K1, 0), (Ab, 0)]))))
print("   => with the charge off (K1 = n = 0) and the bump/trace off (Ab ub^2 = 0):")
print("      d0 == 0 exactly: the khronon band is FLAT (omega^2 = 0 for ALL k).")
print("      NO k^2 and NO k^4 gradient term is generated by the action itself at quadratic order;")
print("      the corpus's k^4 dispersion is the ACLM-EFT completion ON TOP of this flat band")
print("      (mi_cosmo_perturbations_2026.py line 52: 'supplying the only gradient term').")

print("\nDONE (%.1f s)" % (time.time()-t0))
