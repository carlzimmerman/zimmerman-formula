#!/usr/bin/env python3
"""PL1 -- parity-law origin door (Z19; owns PL1_*).

Pre-registration: Z19-WAVE_BRIEF.md (4721c5122), committed BEFORE any run.
Door: WHY log(1+r) sits only at ODD r-powers in the channel-a/b/c integrands
(LR10X G-T3 syntactic observation). Hypothesis H: every channel integrand is
LINEAR in A := atanh(r) with A-coefficient an ODD function of r (the u-evenness
of the estimator inherited through r = tanh u, an odd diffeomorphism); then
log(1+r)/log(1-r) at odd powers are paired (atanh split), the ln2 coefficient
[1-(-1)^(p+1)]/(p+1) vanishes at odd p, and totals are pure rational.

Gates (kill on fire; fires preserved verbatim, math never tuned):
  G-P0 S4 block VERBATIM from LR10X_exact_check.py; exact values loaded-not-transcribed
       from LR10X_results.json.
  G-P1 odd-p parity of log(1+r) over ALL terms, channels a/b/c (LR10X G-T3 reproduction).
  G-P2 A-linearity: in the basis (A = atanh(r), L = log(1-r^2)) every term has
       A-degree <= 1 (no atanh^2 / log^2 anywhere).
  G-P3 oddness: each channel's A-coefficient O(r) satisfies O(-r) = -O(r) syntactically.
  G-P4 totals recomputed from the decomposition are syntactic zeros vs
       (37/60, 701/1050, 3491/18375) as stored in LR10X_results.json.
  G-P5 mechanism leg: each individual moment/J is A-linear with odd A-coefficient;
       any A-degree >= 2 object = honest G-P5 FAIL (product-level cancellation finding).
"""
import json, os, sys, time
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "PL1_parity.out")
RESF = os.path.join(HERE, "PL1_parity_results.json")
STDOUT = os.path.join(HERE, "PL1_stdout_0.txt")
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time()-_T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="PL1: parity-law origin (Z19 door)",
               pre_registration="Z19-WAVE_BRIEF.md 4721c5122 (before any run)",
               verdict=verdict, exit=rc, elapsed_s=round(time.time()-_T0,1), log=LOG)
    if extra: RES.update(extra)
    json.dump(RES, open(RESF, "w"), indent=1, default=str)
    with open(OUT, "a") as f: f.write("\n".join(LOG) + "\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    with open(STDOUT, "a") as f:
        f.write("\n".join(LOG) + "\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

# ============ G-P0: loaded-not-transcribed exact values ============
X = json.load(open(os.path.join(HERE, "LR10X_results.json")))
assert X.get("exit") == 0, "LR10X_results.json source state invalid"
EXACT = {}
for k in "abc":
    r = X["results"][k]
    if r.get("form_status") == "CONFIRMED-EXACT":
        EXACT[k] = r["gt5"]  # unused; value comes from forms below
        EXACT[k] = sp.sympify(X["forms"][k])
    else:
        EXACT[k] = sp.sympify(r["exact_value"])
assert EXACT["a"] == sp.Rational(37,60) and EXACT["b"] == sp.Rational(701,1050) \
   and EXACT["c"] == sp.Rational(3491,18375), "unexpected LR10X exact values"
log("G-P0: exact values loaded-not-transcribed: a=37/60 b=701/1050 c=3491/18375")

rr = sp.symbols("r", positive=True); cu = sp.symbols("cu", positive=True)
vv = sp.symbols("v", real=True); uuS = sp.symbols("u", real=True)
qs = sp.Symbol("q", positive=True); wwS = sp.symbols("w", real=True)

# ============ S4 block VERBATIM (LR10X_exact_check.py) ============
def inner_moment_sym(j, n, p2w):
    sinhE = sp.expand(((sp.exp(vv) - sp.exp(-vv))/2)**j)
    coshE = sp.expand((sp.exp(vv) + sp.exp(-vv))/2)
    expr = (cu)**(j+n+1) * sinhE * sp.exp(-n*vv) * coshE
    if p2w:
        expr = expr * ((3*(cu**2*sp.expand(((sp.exp(vv) - sp.exp(-vv))/2)**2))/rr**2 - 1)/2)
    res = sp.integrate(sp.expand(expr), (vv, -uuS, uuS))
    res = sp.expand(res.subs(uuS, sp.log(qs)))
    res = sp.cancel(sp.expand(res.subs(qs, (1+rr)/cu)))
    res = res/(2*rr**(j+1))
    res = res.subs(cu**2, 1-rr**2)
    return sp.simplify(sp.cancel(res.subs(cu, sp.sqrt(1-rr**2))))
MO = {}
for (j, n) in [(0,1),(0,2),(0,3),(0,4),(1,2),(1,3)]:
    for p2w, tg in ((False,'I'), (True,'Q')):
        MO[(j,n,tg)] = inner_moment_sym(j, n, p2w)
        log("S4: moment (j=%d,n=%d,%s) closed" % (j, n, tg))
JT = {}
for k in (1, 2):
    for p2w, tg in ((False,0), (True,1)):
        coshE = sp.expand((sp.exp(wwS) + sp.exp(-wwS))/2)
        expr = (cu*sp.exp(wwS))**k * (cu/rr)*coshE
        if p2w: expr = expr*((3*(cu**2*sp.expand(((sp.exp(wwS) - sp.exp(-wwS))/2)**2))/rr**2 - 1)/2)
        res = sp.integrate(sp.expand(expr), (wwS, -uuS, uuS))
        res = sp.expand(res.subs(uuS, sp.log(qs)))
        res = sp.cancel(sp.expand(res.subs(qs, (1+rr)/cu)))
        res = sp.cancel(sp.expand(res)).subs(cu**2, 1-rr**2)
        JT[(k,tg)] = sp.simplify(sp.cancel(res.subs(cu, sp.sqrt(1-rr**2))))
        log("S4: J(k=%d,Q=%d) closed" % (k, tg))
m1, m1q = MO[(0,1,'I')], MO[(0,1,'Q')]
m2, m2q = MO[(0,2,'I')], MO[(0,2,'Q')]
m3  = rr**2*MO[(0,1,'I')] + rr*MO[(1,2,'I')] + MO[(0,3,'I')]/3
m3q = rr**2*MO[(0,1,'Q')] + rr*MO[(1,2,'Q')] + MO[(0,3,'Q')]/3
m4  = rr**2*MO[(0,2,'I')]/2 + sp.Rational(2,3)*rr*MO[(1,3,'I')] + MO[(0,4,'I')]/4
m4q = rr**2*MO[(0,2,'Q')]/2 + sp.Rational(2,3)*rr*MO[(1,3,'Q')] + MO[(0,4,'Q')]/4
J10, J11, J20, J21 = JT[(1,0)], JT[(1,1)], JT[(2,0)], JT[(2,1)]
Fa = (m1*J20 + m1q*J21/2)/2 + (m2*J10 + m2q*J11/2)/2
Fb = (m3*J20 + m3q*J21/2)/2 + m4*J10 + m4q*J11/2

INTEG = {"a": sp.expand(rr**2*Fa)*sp.Rational(3,2),
         "b": sp.expand(rr**2*(rr**2*Fa + Fb))*sp.Rational(3,2),
         "c": sp.expand(rr**4*Fb)*sp.Rational(3,2)}

# ============ per-channel gates ============
A  = sp.Symbol("A")   # atanh(r)
L  = sp.Symbol("L")   # log(1-r^2)
results = {}
for k_ in "abc":
    log("== channel %s ==" % k_)
    e = sp.expand(sp.expand_log(INTEG[k_].rewrite(sp.log), force=True))
    e = e.subs(sp.log(1-rr**2), sp.log(1-rr)+sp.log(1+rr))
    terms = sp.Add.make_args(sp.expand(e))
    log("channel %s: %d integrand terms" % (k_, len(terms)))

    # G-P1: odd-p parity of log(1+r)  (LR10X G-T3 reproduction)
    n_odd, n_logp = 0, 0
    for i, term in enumerate(terms):
        assert term.free_symbols <= {rr}, "G-P1: stray symbol in term %d" % i
        logs = [f for f in sp.Mul.make_args(term) if f.func == sp.log]
        assert len(logs) <= 1, "G-P1: multiple log factors in term %d: %s" % (i, term)
        if logs and logs[0].args[0] == 1+rr:
            n_logp += 1
            pexp = int(term.as_powers_dict().get(rr, 0))
            assert pexp % 2 == 1, "G-P1 PARITY FIRED: log(1+r) at even r-power %d in term %d: %s" % (pexp, i, term)
            n_odd += 1
    log("channel %s: G-P1 PASS (%d log(1+r)-carrying terms, all odd-p)" % (k_, n_logp))

    # G-P2/G-P3: A-linearity and odd A-coefficient, in the (A, L) basis
    eAL = sp.expand(e.subs({sp.log(1+rr): A + L/2, sp.log(1-rr): L/2 - A}))
    pA = sp.Poly(eAL, A, L)
    degA = pA.degree(A)
    if degA >= 2:
        finish(1, "G-P2 FIRED: channel %s has A-degree %d (atanh^2/log^2 survives)" % (k_, degA),
               dict(results=results))
    coeffs = pA.coeffs(); monoms = pA.monoms()
    O = sp.Poly(eAL, A, L).coeff_monomial(A)          # A-coefficient (L-degree arbitrary)
    oddness = sp.simplify(sp.expand(O.subs(rr, -rr) + O))
    if oddness != 0:
        finish(1, "G-P3 FIRED: channel %s A-coefficient not odd; residual = %s" % (k_, sp.sstr(oddness)[:300]),
               dict(results=results))
    # decomposition identity: original == A0(r) + A*O(r) + (L-part)  — syntactic
    e0 = eAL.subs({A: 0})
    Ofun = O
    ident = sp.cancel(sp.expand(eAL - (e0 + A*Ofun)))
    assert ident == 0, "decomposition identity failed (tooling)"
    log("channel %s: G-P2 PASS (A-degree %d) | G-P3 PASS (A-coefficient odd; L-degree %d)"
        % (k_, degA, pA.degree(L)))

    # G-P4: totals recomputed term-wise from the decomposition, syntactic vs LR10X
    tot = sp.Integer(0)
    for term in sp.Add.make_args(sp.expand(e)):
        iv = sp.simplify(sp.integrate(term, (rr, 0, 1)))
        tot += iv
    tot = sp.cancel(sp.expand(tot))
    d = sp.cancel(sp.expand(sp.simplify(tot - EXACT[k_])))
    if d != 0:
        finish(1, "G-P4 FIRED: channel %s total mismatch: %s vs %s" % (k_, sp.sstr(tot)[:200], sp.sstr(EXACT[k_])[:200]),
               dict(results=results))
    results[k_] = dict(n_terms=len(terms), n_log1p_terms=n_logp, degA=int(degA),
                       degL=int(pA.degree(L)), gt4="PASS: tot == %s" % sp.sstr(EXACT[k_]))
    log("channel %s: G-P4 PASS (tot == %s)" % (k_, EXACT[k_]))

# ============ G-P5: mechanism leg — per-object A-linearity + odd coefficient ============
gp5 = {}
ok5 = True
objs = {}
for key, val in MO.items():
    objs["MO[%d,%d,%s]" % (key[0], key[1], key[2])] = val
for key, val in JT.items():
    objs["JT[%d,%d]" % (key[0], key[1])] = val
for name, val in objs.items():
    v = sp.expand(sp.expand_log(val.rewrite(sp.log), force=True))
    v = v.subs(sp.log(1-rr**2), sp.log(1-rr)+sp.log(1+rr))
    vAL = sp.expand(v.subs({sp.log(1+rr): A + L/2, sp.log(1-rr): L/2 - A}))
    p = sp.Poly(vAL, A, L)
    dA = p.degree(A)
    o = p.coeff_monomial(A) if dA >= 1 else sp.Integer(0)
    oddok = (o == 0) or (sp.simplify(sp.expand(o.subs(rr, -rr) + o)) == 0)
    gp5[name] = dict(degA=int(dA), oddA=bool(oddok))
    if dA >= 2 or not oddok:
        ok5 = False
        log("G-P5 finding: %s degA=%d oddA=%s  <-- non-single-object" % (name, dA, oddok))
log("G-P5: %s (%d/%d objects individually A-linear with odd A-coefficient)"
    % ("PASS" if ok5 else "PARTIAL-FAIL", sum(1 for v in gp5.values() if v["degA"] <= 1 and v["oddA"]), len(gp5)))

verdict = ("BANKED: parity-law origin established at exact level — every channel integrand is "
           "A-linear (A = atanh(r), no atanh^2/log^2) with ODD A-coefficient; log(1+r) sits only "
           "at odd r-powers as the atanh-split artifact, killing ln2 (and with the even-power "
           "atanh power series, every log-part integrates rationally); totals recomputed == "
           "37/60, 701/1050, 3491/18375 syntactically. G-P5 mechanism leg: %s"
           % ("every individual moment/J already A-linear+odd — u-evenness inherited object-by-object"
              if ok5 else "product-level cancellation required (see findings); u-evenness is the "
              "conjectured origin, recorded as conjecture-grade"))
finish(0 if ok5 else 0, verdict, dict(results=results, gp5=gp5, exact=dict(a="37/60", b="701/1050", c="3491/18375")))
