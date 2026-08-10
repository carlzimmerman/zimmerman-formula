#!/usr/bin/env python3
"""
Part 3 of the adversarial verification: my own reduction pipeline, run on
 (a) TRUNCATED = their checkpointed L2s  (verifies claims 8,9,10,12,13 as internal math)
 (b) FULL      = L2s + DeltaL2s          (the action THE_COMPLETION says it is: AeST Eq. 5)
"""
import sympy as sp
import numpy as np
import functools, sys, time
print = functools.partial(print, flush=True)
T0 = time.time()
def chk(c, lbl):
    print(("  [OK ] " if c else "  [BAD] ") + lbl)
    return bool(c)

k = sp.Symbol('k', positive=True); G = sp.Symbol('G', positive=True)
Lam = sp.Symbol('Lam', real=True); KB = sp.Symbol('K_B', real=True)
Ab = sp.Symbol('A_b', real=True); ubs = sp.Symbol('u_b', real=True)
K0, K1, K2 = sp.symbols('K0 K1 K2', real=True)
A0cp = sp.Symbol('A0cp', positive=True)
p0, s0, x0, a0v = sp.symbols('p0 s0 x0 a0v', real=True)
s1, x1, a1v, p1 = sp.symbols('s1 x1 a1v p1', real=True)
Hh = sp.Symbol('H', real=True); av = sp.Symbol('a_v', positive=True)
Qbs = sp.Symbol('Qb', real=True)
FRIED = [(Lam, 3*Hh**2 - 8*sp.pi*G*(Qbs*K1 - K0))]
vels = [s1, x1, a1v]; flds = [s0, x0, a0v]

L2s  = sp.sympify(open('L2s_checkpoint.txt').read())
dL2s = sp.sympify(open('DeltaL2s_checkpoint.txt').read())

def klead(e):
    e = sp.cancel(sp.together(e)); num, den = sp.fraction(e)
    pn, pd = sp.Poly(num, k), sp.Poly(den, k)
    return sp.cancel(pn.coeff_monomial(k**pn.degree())/pd.coeff_monomial(k**pd.degree())
                     * k**(pn.degree()-pd.degree()))

def reduce_pipeline(L2, tag):
    print("\n" + "#"*100); print("### %s" % tag); print("#"*100)
    res = {}
    chk(sp.diff(L2, p1) == 0, "Phidot absent (Phi is a multiplier)")
    cP = sp.expand(sp.diff(L2, p0)); AP = sp.expand(sp.diff(cP, p0)/2)
    chk(not any(AP.has(v) for v in vels+[p1]), "AP velocity-free")
    cP0 = sp.expand(cP.subs(p0, 0))
    Lred_num = sp.expand(4*AP*L2.subs(p0, 0) - cP0**2)   # Lred = Lred_num/(4AP)
    res['AP_f'] = sp.factor(sp.expand(AP.subs(FRIED)))
    print("  AP (Friedmann) =", res['AP_f'])
    Tnum_off = sp.Matrix(3, 3, lambda i, j: sp.expand(sp.diff(Lred_num, vels[i], vels[j])/2))
    det_off = sp.factor(sp.expand(Tnum_off.det()))
    print("  off-shell det Tnum =", det_off)
    Tnum = Tnum_off.applyfunc(lambda e: sp.factor(sp.expand(e.subs(FRIED))))
    detT = sp.expand(Tnum.det())
    res['deg'] = (detT == 0)
    chk(res['deg'], "det Tnum == 0 on Friedmann (kinetic degeneracy)")
    res['Tnum'] = Tnum
    names = ["Psi", "chi", "alpha"]
    for i in range(3):
        for j in range(i, 3):
            print("   Tnum[%s,%s] = %s" % (names[i], names[j], Tnum[i, j]))
    if res['deg']:
        ns = Tnum.nullspace()
        if len(ns) == 1:
            nv = ns[0].applyfunc(lambda e: sp.factor(sp.cancel(e)))
            nv = nv/nv[2]
            print("  null direction (Psi,chi,alpha)-velocities ~", list(sp.simplify(e) for e in nv.T))
            res['null'] = nv
    # frozen-background WKB dispersion
    Lf = sp.expand(Lred_num.subs(FRIED))
    acc = sp.symbols('s2 x2 a2v', real=True)
    def ddt(e):
        return (sum(sp.diff(e, f)*v for f, v in zip(flds, vels))
                + sum(sp.diff(e, v)*aa for v, aa in zip(vels, acc)))
    EL = [sp.expand(ddt(sp.diff(Lf, vels[i])) - sp.diff(Lf, flds[i])) for i in range(3)]
    w = sp.Symbol('omega'); hat = sp.symbols('hS hX hA', real=True)
    sub = (list(zip(acc, [-w**2*h for h in hat])) + list(zip(vels, [sp.I*w*h for h in hat]))
           + list(zip(flds, hat)))
    M = sp.Matrix(3, 3, lambda i, j: sp.diff(sp.expand(EL[i].subs(sub, simultaneous=True)), hat[j]))
    D = sp.expand(M.det()); Dp = sp.Poly(D, w)
    print("  det M(omega) degree:", Dp.degree())
    d0 = sp.expand(Dp.coeff_monomial(1)); d2 = sp.expand(Dp.coeff_monomial(w**2))
    d4 = sp.expand(Dp.coeff_monomial(w**4))
    d6 = sp.expand(Dp.coeff_monomial(w**6)) if Dp.degree() >= 6 else sp.S(0)
    odd = all(sp.expand(Dp.coeff_monomial(w**n)) == 0 for n in range(1, Dp.degree()+1, 2))
    print("  odd coefficients vanish:", odd)
    res.update(d0=d0, d2=d2, d4=d4, d6=d6)
    # soft branch, H->0, Ab=0
    s0H = sp.cancel(-sp.factor(sp.expand(d0.subs(Hh, 0).subs(Ab, 0)))
                    / sp.factor(sp.expand(d2.subs(Hh, 0).subs(Ab, 0))))
    res['soft'] = s0H
    lead = klead(s0H)
    print("  soft branch (H->0, Ab=0): c_s^2 k^2 (k->inf) =", sp.factor(lead))
    try:
        ser = sp.series(s0H, k, 0, 5).removeO()
        c2 = sp.simplify(ser.coeff(k, 2)); c4 = sp.simplify(ser.coeff(k, 4))
        print("  soft branch k->0: k^2 coeff =", sp.factor(c2), ";  k^4 coeff =", sp.factor(c4))
        res['c2'], res['c4'] = c2, c4
    except Exception as ex:
        print("  series failed:", ex)
    # flat-band test: K1 = Ab = 0
    d0z = sp.expand(d0.subs([(K1, 0), (Ab, 0)])); d2z = sp.expand(d2.subs([(K1, 0), (Ab, 0)]))
    print("  switch-off (K1=Ab=0): d0 =", sp.factor(d0z) if d0z != 0 else 0,
          " | d2 =", sp.factor(d2z) if d2z != 0 else 0)
    res['flat'] = (d0z == 0 and d2z == 0)
    return res

resT = reduce_pipeline(L2s, "TRUNCATED action (= their master script)")
print("\n  --- verify THEIR claimed formulas on the truncated result ---")
Tn = resT['Tnum']
targets = {
 (0,0): -3*av**4*(8*sp.pi*G*K2*Qbs**2*av**2 + KB*k**2)/(128*sp.pi**2*G**2),
 (0,1): -3*Hh*K2*Qbs*av**6/(16*sp.pi*G),
 (0,2): 3*Hh*KB*av**4*k**2/(128*sp.pi**2*G**2),
 (1,1): K2*av**4*(KB*k**2 - 6*Hh**2*av**2)/(32*sp.pi*G),
 (1,2): K2*KB*Qbs*av**4*k**2/(32*sp.pi*G),
 (2,2): KB*av**4*k**2*(4*sp.pi*G*K2*Qbs**2 - 3*Hh**2)/(128*sp.pi**2*G**2)}
allok = True
for (i, j), tgt in targets.items():
    allok &= (sp.simplify(sp.expand(Tn[i, j] - tgt)) == 0)
chk(allok, "claim10: all six claimed Tnum entries CONFIRMED independently")
chk(sp.simplify(sp.cancel(klead(resT['soft'])
    - K1*(2-KB)*k**2/(av**2*(3*K1*KB + K2*Qbs*(KB+2))))) == 0,
    "claim12: truncated c_s^2(k->inf) = K1(2-K_B)/(a^2[3K1 K_B + K2 Qb(K_B+2)]) CONFIRMED")
chk(sp.simplify(resT['c2'] + 1/(3*av**2)) == 0 and
    sp.simplify(resT['c4'] - KB/(72*sp.pi*G*K1*Qbs*av**4)) == 0,
    "claim13: truncated k^2 = -1/(3a^2), k^4 = K_B/(72 pi G K1 Qb a^4) CONFIRMED")
print("  [t=%.1fs]" % (time.time()-T0))

resF = reduce_pipeline(sp.expand(L2s + dL2s), "FULL AeST action (with the omitted 2(2-K_B)J.gradphi - (2-K_B)Y)")

print("\n" + "="*100)
print("COMPARISON: what the omission changes")
print("="*100)
print("  c_s^2 (k->inf, H=0, Ab=0):")
print("    truncated:", sp.factor(klead(resT['soft'])))
print("    full     :", sp.factor(klead(resF['soft'])))
if 'c4' in resF:
    print("  k->0: k^2 coeff  truncated:", sp.factor(resT['c2']), " full:", sp.factor(resF['c2']))
    print("        k^4 coeff  truncated:", sp.factor(resT['c4']), " full:", sp.factor(resF['c4']))
print("  flat band at K1=Ab=0: truncated:", resT['flat'], "  full:", resF['flat'])

# numeric branch comparison at physical hierarchy
print("\n  numeric soft/hard branches, Omega_dust=1e-6 (K0=-rho_cr), Qb=1, K2=0.4, H=0.05, a=1:")
rho_cr = 3*0.05**2/(8*np.pi)
subs_common = [(G, 1.0), (av, 1.0), (Hh, 0.05), (Qbs, 1.0), (K0, -rho_cr), (K1, 1e-6*rho_cr),
               (K2, 0.4), (Ab, 0.0), (ubs, 0.0), (A0cp, 1.0)]
for tag, rr in [("TRUNCATED", resT), ("FULL", resF)]:
    d0n = sp.lambdify((KB, k), rr['d0'].subs(subs_common), 'numpy')
    d2n = sp.lambdify((KB, k), rr['d2'].subs(subs_common), 'numpy')
    d4n = sp.lambdify((KB, k), rr['d4'].subs(subs_common), 'numpy')
    d6n = sp.lambdify((KB, k), rr['d6'].subs(subs_common), 'numpy') if rr['d6'] != 0 else None
    print("  --- %s ---" % tag)
    print("   %5s %9s | %14s %14s" % ("K_B", "k/aH", "w2_soft", "w2_hard"))
    for KBv in [0.5, 1.9, 2.1]:
        for kv in [1.0, 1e3, 1e5]:
            kk = kv*0.05
            cofs = [d0n(KBv, kk), 0.0, d2n(KBv, kk), 0.0, d4n(KBv, kk)]
            if d6n is not None:
                cofs += [0.0, d6n(KBv, kk)]
            roots = np.roots(list(reversed(cofs)))
            w2 = sorted(set(np.round(roots**2, 30)), key=abs)
            # w2 from roots of poly in w: collect squared values (pairs +-)
            uniq = []
            for r_ in np.sort_complex(roots):
                v = r_**2
                if not any(abs(v-u) <= 1e-9*max(1, abs(u)) for u in uniq):
                    uniq.append(v)
            uniq = sorted(uniq, key=abs)
            def fmt(x):
                return ("%.4g%+.1gi" % (x.real, x.imag)) if abs(x.imag) > 1e-12*abs(x.real)+1e-30 else ("%.4g" % x.real)
            print("   %5s %9g | " % (KBv, kv), "  ".join(fmt(v) for v in uniq[:3]))
print("\nDONE (%.1f s)" % (time.time()-T0))
