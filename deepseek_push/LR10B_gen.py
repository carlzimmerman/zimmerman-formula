#!/usr/bin/env python3
"""LR10B -- generate the Lean certificate of the LR10X-corrected rational closed forms (Z18 door).

Gates (Z18-WAVE_BRIEF.md, frozen before any run):
  G-L0 classify ALL 30 terms from LR10X_results.json (exit 0, loaded-not-transcribed);
       core values consistent across terms sharing a core; B(1) endpoint vs data.
  G-L2 core values vs independent mpmath quad (dps 40), rel <= 1e-30.
  G-L1 lake env lean LR10_rat.lean rc 0; zero sorry; #print axioms of ch_a/ch_b/ch_c
       subset of {propext, Classical.choice, Quot.sound}.
Output: fable_independent_2026/lean_2026/LR10_rat.lean

PATCH 2 (conductor tick 2026-10-06): full emitter appended per the stage-1
template's own plan ("full emitter follows in patch 2"). Disclosed fixes before
run-1, gate VALUES unchanged:
  (i)  stage-1 used rr = sp.symbols("r", positive=True) while LR10X integrand
       strings parse to plain Symbol("r") -- assumptions differ, symbols don't
       match; rr is now the plain symbol.
  (ii) the antiderivative's polynomial part carries P' = -s/(p+1) Q for BOTH
       signs (stage-1 draft had the s=+1-only Bp; the G-L0 B(1) gate would have
       caught it -- fixed forward).
  (iii) HasDerivAt.comp takes no explicit point argument (Comp.lean:258).
"""
import json, os, sys, time, subprocess
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "LR10B_gen.out")
RESF = os.path.join(HERE, "LR10B_gen.json")
LEANF = os.path.abspath(os.path.join(HERE, "..", "fable_independent_2026", "lean_2026", "LR10_rat.lean"))
LEANDIR = os.path.abspath(os.path.join(HERE, "..", "fable_independent_2026", "lean_2026"))
STDOUT = os.path.join(HERE, "LR10B_lean_stdout.txt")
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time()-_T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="LR10B: Lean-certificate generator (Z18 door)",
               pre_registration="Z18-WAVE_BRIEF.md (committed before any run)",
               verdict=verdict, exit=rc, elapsed_s=round(time.time()-_T0,1), log=LOG)
    if extra: RES.update(extra)
    json.dump(RES, open(RESF, "w"), indent=1, default=str)
    with open(OUT, "a") as f: f.write("\n".join(LOG) + "\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

E = json.load(open(os.path.join(HERE, "LR10X_results.json")))
assert E.get("exit") == 0, "LR10X_results.json must be exit 0"
log("loaded LR10X_results.json (exit 0)")

rr = sp.Symbol("r")   # plain symbol: matches the parsed LR10X integrand strings (fix i)
u = sp.Symbol("u")

def rat_lean(q):
    q = sp.Rational(q); n, d = q.p, q.q
    if n == 0: return "(0: ℝ)"
    if n > 0: return "((%d: ℝ) / %d)" % (n, d)
    return "(-((%d: ℝ) / %d))" % (-n, d)

def mono_terms(poly, var):
    poly = sp.expand(poly)
    if poly == 0: return []
    out = []
    for mon in sp.Add.make_args(poly):
        if mon == 0: continue
        d = sp.degree(mon, gen=var)
        c = sp.simplify(mon / var**d)
        assert c.is_Rational, ("non-rational monomial coeff", mon)
        out.append((sp.Rational(c), int(d)))
    out.sort(key=lambda t: -t[1])
    return out

def mono_str(terms_, varname):
    parts = []
    for c, d in terms_:
        base = "%s ^ %d" % (varname, d)
        if d == 0: parts.append(rat_lean(c))
        elif c == 1: parts.append(base)
        else: parts.append("%s * %s" % (rat_lean(c), base))
    return " + ".join(parts) if parts else "(0: ℝ)"

def gsum_str(p, v):
    return " + ".join("(1: ℝ)" if j == 0 else (v if j == 1 else "%s ^ %d" % (v, j)) for j in range(p+1))

# ---------- G-L0 part 1: classify all 30 terms from the data ----------
terms, CORE = {}, {}
for ch in "abc":
    lst = []
    for k, rec in enumerate(E["results"][ch]["terms"]):
        t = sp.expand(sp.sympify(rec["integrand"])); v = sp.sympify(rec["integral"])
        assert v.is_Rational, ("non-rational term integral", ch, k, rec["integral"])
        pd = t.as_powers_dict()
        p = int(pd.get(rr, 0))
        logs = [f for f in sp.Mul.make_args(t) if f.func == sp.log]
        if logs:
            assert len(logs) == 1, ("multi-log term", ch, k)
            arg = logs[0].args[0]
            assert arg in (1 - rr, 1 + rr), ("bad log arg", ch, k, rec["integrand"])
            s = -1 if arg == 1 - rr else 1
            coeff = sp.simplify(t / (rr**p * logs[0]))
            assert coeff.is_Rational, ("non-rational coeff", ch, k)
            lst.append(dict(kind="L", coeff=sp.Rational(coeff), p=p, s=s, value=sp.Rational(v)))
            CORE.setdefault(("L", s, p), set()).add(sp.simplify(v / coeff))
        else:
            coeff = sp.simplify(t / rr**p)
            assert coeff.is_Rational, ("non-rational coeff", ch, k)
            lst.append(dict(kind="P", coeff=sp.Rational(coeff), p=p, value=sp.Rational(v)))
            CORE.setdefault(("P", 0, p), set()).add(sp.simplify(v / coeff))
    terms[ch] = lst
log("classified %d terms (a=%d b=%d c=%d)" % (sum(len(v) for v in terms.values()),
    len(terms["a"]), len(terms["b"]), len(terms["c"])))
COREd = {}
for k, vs in CORE.items():
    assert len(vs) == 1, ("G-L0 FIRED: core %s inconsistent across terms: %s" % (k, vs))
    val = sp.Rational(list(vs)[0]); assert val.is_Rational, ("G-L0 FIRED: core %s non-rational" % (k,))
    COREd[k] = val
CORE = COREd
log("cores (%d): %s" % (len(CORE), {str(k): str(v) for k, v in sorted(CORE.items(), key=str)}))
for ch in "abc":
    for t in terms[ch]:
        key = ("L", t["s"], t["p"]) if t["kind"] == "L" else ("P", 0, t["p"])
        assert sp.simplify(t["coeff"] * CORE[key] - t["value"]) == 0, ("term/core mismatch", ch, t)
log("G-L0 part 1 PASS: per-term coeff*core == data integral for all 30 terms")

# ---------- G-L0 part 2: core exactness (independent sympy integration + B(1)) ----------
BINFO = {}
for (kind, s, p), val in sorted(CORE.items(), key=str):
    if kind == "P":
        sym = sp.integrate(rr**p, (rr, 0, 1))
        assert sp.simplify(sym - val) == 0, ("G-L0 FIRED: poly core %s sympy mismatch" % p)
        continue
    sym = sp.integrate(rr**p * sp.log(1 + s*rr), (rr, 0, 1))
    assert sp.simplify(sym - val) == 0, ("G-L0 FIRED: core %s sympy integral mismatch" % ((s, p),))
    Q = sp.div(u**(p+1) - 1, 1 + s*u, u)[0]
    S1 = sp.integrate(Q, (u, 0, 1))
    b1 = sp.simplify(-sp.Rational(s, 1)/(p+1) * S1)
    assert sp.simplify(b1 - val) == 0, ("G-L0 FIRED (B(1) gate): core %s B(1)=%s vs data %s" % ((s, p), b1, val))
    P = sp.expand(-sp.Rational(s, 1)/(p+1) * sp.integrate(Q, u))
    assert sp.simplify(P.subs(u, 0)) == 0, ("P(0) != 0", (s, p))
    assert sp.Rational(sp.simplify(P.subs(u, 1))) == val, ("P(1) != value", (s, p))
    assert sp.simplify(sp.diff(P, u) + sp.Rational(s, 1)/(p+1) * Q) == 0, ("dP mismatch", (s, p))
    BINFO[(s, p)] = (Q, P)
log("G-L0 part 2 PASS: sympy exact integrals + B(1) endpoints match data for %d log cores" % len(BINFO))

# ---------- G-L2: independent mpmath quad of every core ----------
pts = [0, mp.mpf('0.5'), mp.mpf('0.9'), mp.mpf('0.99'), mp.mpf('0.9999'), 1]
# AMENDMENT 1 (after run-1 G-L2 fire, preserved verbatim in LR10B_gen.out):
# run-1 grid included split 0.9999999, on which mp.quad's tanh-sinh returns -inf
# for the log(1-x) cores (instrument bug, not a math failure); grid now equals
# LR10X's verified QUAD_PTS exactly; gate threshold 1e-30 unchanged.
for (kind, s, p), val in sorted(CORE.items(), key=str):
    if kind == "P":
        f = lambda x, p=p: mp.mpf(x)**p
    elif s < 0:
        f = lambda x, p=p: mp.mpf(x)**p * mp.log(1 - mp.mpf(x))
    else:
        f = lambda x, p=p: mp.mpf(x)**p * mp.log(1 + mp.mpf(x))
    rel = abs(mp.quad(f, pts) - val)/abs(val)
    if rel > mp.mpf("1e-30"):
        finish(1, "G-L2 FIRED: core %s quad rel %.3e > 1e-30" % ((kind, s, p), float(rel)))
    log("G-L2: core %s quad rel %.2e" % ((kind, s, p), float(rel)))
log("G-L2 PASS")

# ---------- channel totals vs LR10X exact values; c1 assembly ----------
S_Q = [sp.Rational(1, 3), sp.Rational(1, 3), sp.Rational(46, 525)]
assert "46/525" in open(os.path.join(HERE, "LR9_results.json")).read(), "S(q) constants must be LR9-banked on disk"
E2 = {}
for ch in "abc":
    tot = sum(t["value"] for t in terms[ch])
    # AMENDMENT 2 (after run-2 KeyError fire, preserved verbatim in LR10B_gen.out):
    # LR10X stores the adjudicated totals in forms.a ("37/60") and in the
    # gt5 strings ("exact tot = 701/1050" / "= 3491/18375") -- parsed here,
    # loaded-not-transcribed.
    m = __import__("re").search(r"exact tot = (\S+)", str(E["results"][ch]["gt5"]))
    ex = sp.Rational(E["forms"][ch]) if m is None else sp.Rational(m.group(1))
    assert tot == ex, ("channel %s sum %s != exact %s" % (ch, tot, ex))
    E2[ch] = ex
    log("channel %s: sum of %d term integrals == exact %s" % (ch, len(terms[ch]), ex))
c1 = [E2["a"] - S_Q[0], E2["b"] - S_Q[1], E2["c"] - S_Q[2]]
assert c1 == [sp.Rational(17, 60), sp.Rational(117, 350), sp.Rational(627, 6125)], ("c1 mismatch", c1)
log("c1 assembly check PASS: c1(q) = 17/60 + (117/350) q + (627/6125) q^2 == E2 - S")


# ================= emit Lean (v4, after run-9 fires; fixes: left-assoc .add
# chains via accumulator parens (Lean parses a.add b.add c right-assoc per
# run-9 elaboration traces); A-part as w^0-monomial (continuous_const cannot be
# applied explicitly); log(1+x) forms switched to (x+1) to match comp_sub_right;
# logp_int via comp_sub_right (-1) + simp/norm_num; pointwise endpoint
# continuity via typed intermediate haves + exact (avoids the comp elaboration
# trap seen at run-9 lines 29/32/137); hinner pins the (1+-y) derivative before
# HasDerivAt.comp; tendsto_alm MapsTo lambda simp-only; final congr
# (field_simp [hQ]; ring) without `first`) =================
L = []
A = L.append
INT = u"\u222b"; FORALL = u"\u2200"; IN = u"\u2208"; NE = u"\u2260"
A("import Mathlib")
A("open Real Filter Topology intervalIntegral MeasureTheory")
A("")
A("/-- LR10B -- Lean certificate of the LR10X-corrected rational closed forms (Z18 door).")
A("   LR10X (deepseek_push/LR10X_results.json, exit 0) adjudicated EXACTLY:")
A("     E2(q) = 37/60 + (701/1050) q + (3491/18375) q^2   (channel a/b/c sums)")
A("   hence the thin-window law c1(q) = E2(q) - S(q) = 17/60 + (117/350) q + (627/6125) q^2")
A("   with S(q) = 1/3 + q/3 + 46 q^2/525 (LR9-certified).")
A("   Certified HERE unconditionally, with no unfinished tactic proofs: 10 single-log")
A("   core integrals int_0^1 u^p log(1+-u) du (odd p in {1,3,5,7,9}), 4 polynomial")
A("   cores, the 30 per-term integral certificates, the three channel assemblies, and")
A("   the c1 coefficient law -- via the normalized antiderivative")
A("     F = P + ((u^(p+1)-1)/(p+1)) log(1+-u),  P' = -s/(p+1) Q,  Q = (u^(p+1)-1)/(1+-u),")
A("   and mathlib's integral_eq_sub_of_hasDerivAt_of_tendsto (the technique of")
A("   mathlib's own integral_log lemmas). The geometric reduction chain upstream of")
A("   these integrals remains numerically audited (E2F1 G1/G2b, LR10X G-T1) and is")
A("   NOT probability-space-certified -- K01 consistency-family labeling carries over.")
A("   Gates: G-L0/G-L2 in LR10B_gen.py (loaded-not-transcribed from LR10X data),")
A("   G-L1 = this file compiles rc 0 with zero unfinished proofs and channel-law axiom")
A("   footprints inside {propext, Classical.choice, Quot.sound}. -/")
A("")
A("theorem logm_int : IntervalIntegrable (fun x : \u211d => Real.log (1 - x)) volume 0 1 := by")
A("  simpa using (intervalIntegrable_log' (a := (0: \u211d)) (b := (1: \u211d))).comp_sub_left 1 |>.symm")
A("")
A("theorem logp_int : IntervalIntegrable (fun x : \u211d => Real.log (x + 1)) volume 0 1 := by")
A("  have h := (intervalIntegrable_log' (a := (1: \u211d)) (b := (2: \u211d))).comp_sub_right (-1)")
A("  simp only [sub_neg_eq_add] at h")
A("  norm_num at h")
A("  exact h")
A("")
A("theorem logp_contAt0 : ContinuousAt (fun u : \u211d => Real.log (1 + u)) 0 := by")
A("  have h1 : ContinuousAt (fun u : \u211d => 1 + u) 0 := by fun_prop")
A("  exact ContinuousAt.comp_of_eq (Real.continuousAt_log (by norm_num : (1: \u211d) %s 0)) h1 (by norm_num)" % NE)
A("")
A("theorem logp_contAt1 : ContinuousAt (fun u : \u211d => Real.log (1 + u)) 1 := by")
A("  have h1 : ContinuousAt (fun u : \u211d => 1 + u) 1 := by fun_prop")
A("  exact ContinuousAt.comp_of_eq (Real.continuousAt_log (by norm_num : (2: \u211d) %s 0)) h1 (by norm_num)" % NE)
A("")
A("theorem mono_cont (c : \u211d) (k : \u2115) : Continuous fun w : \u211d => c * w ^ k :=")
A("  Continuous.mul continuous_const (by fun_prop : Continuous fun w : \u211d => w ^ k)")
A("")
A("theorem mono_contAt (c : \u211d) (k : \u2115) (x : \u211d) : ContinuousAt (fun w : \u211d => c * w ^ k) x :=")
A("  (mono_cont c k).continuousAt")
A("")
A("theorem tendsto_t_log_t : Tendsto (fun t : \u211d => t * Real.log t) (nhdsWithin 0 (Set.Ioi 0)) (nhds 0) := by")
A("  simpa [mul_comm] using tendsto_log_mul_rpow_nhdsGT_zero one_pos")
A("")
A("theorem tendsto_alm {G : \u211d \u2192 \u211d} (hG : ContinuousAt G 1) :")
A("    Tendsto (fun u : \u211d => ((1 - u) * Real.log (1 - u)) * G u) (nhdsWithin 1 (Set.Iio 1)) (nhds 0) := by")
A("  have hsub : Tendsto (fun u : \u211d => 1 - u) (nhdsWithin 1 (Set.Iio 1)) (nhdsWithin 0 (Set.Ioi 0)) := by")
A("    have h1 : ContinuousWithinAt (fun u : \u211d => 1 - u) (Set.Iio 1) 1 := by fun_prop")
A("    have h2 : Tendsto (fun u : \u211d => 1 - u) (nhdsWithin 1 (Set.Iio 1)) (nhdsWithin ((1: \u211d) - 1) (Set.Ioi 0)) :=")
A("      h1.tendsto_nhdsWithin (t := Set.Ioi 0) (fun z hz => by")
A("        simp only [Set.mem_Iio, Set.mem_Ioi] at hz \u22a2")
A("        linarith)")
A("    rwa [show ((1: \u211d) - 1) = 0 by norm_num] at h2")
A("  have h2 : Tendsto (fun u : \u211d => (1 - u) * Real.log (1 - u)) (nhdsWithin 1 (Set.Iio 1)) (nhds 0) :=")
A("    tendsto_t_log_t.comp hsub")
A("  simpa using h2.mul (hG.tendsto.mono_left nhdsWithin_le_nhds)")
A("")

def rat(q): return rat_lean(q)

def chain(parts):
    expr = parts[0]
    for pp in parts[1:]:
        expr = "(%s.add %s)" % (expr, pp)
    return expr

def mono_chain(Pt, x):
    return chain(["(mono_contAt %s %d %s)" % (rat(c), d, x) for c, d in Pt])

def deriv_chain(Pt, x):
    return chain(["((hasDerivAt_pow %d x).const_mul %s)" % (d, rat(c)) for c, d in Pt])

def hint_congr(s, p, C=None):
    lsrc = "Real.log (1 - x)" if s < 0 else "Real.log (x + 1)"
    ltgt = "Real.log (1 - x)" if s < 0 else "Real.log (1 + x)"
    lint = "logm_int" if s < 0 else "logp_int"
    tgt = "x ^ %d * %s" % (p, ltgt) if C is None else "%s * (x ^ %d * %s)" % (rat(C), p, ltgt)
    src = "%s * x ^ %d" % (lsrc, p) if C is None else "%s * (%s * x ^ %d)" % (lsrc, rat(C), p)
    gfun = "(by fun_prop : Continuous fun x : \u211d => x ^ %d)" % p if C is None \
        else "(Continuous.mul continuous_const (by fun_prop : Continuous fun u : \u211d => u ^ %d))" % p
    return ["    refine IntervalIntegrable.congr (show Set.EqOn (fun x : \u211d => %s) (fun x : \u211d => %s) (Set.uIoc (0: \u211d) 1) from fun x _ => by ring)" % (src, tgt),
            "      (%s.mul_continuousOn (Continuous.continuousOn %s))" % (lint, gfun)]

def core_lean(s, p, val):
    name = "core_lm_%d" % p if s < 0 else "core_lp_%d" % p
    uw = "Real.log (1 - w)" if s < 0 else "Real.log (1 + w)"
    ux = "Real.log (1 - x)" if s < 0 else "Real.log (1 + x)"
    uu = "Real.log (1 - u)" if s < 0 else "Real.log (1 + u)"
    Q, P = BINFO[(s, p)]
    Qx = mono_str(mono_terms(Q, u), "x")
    Pt = mono_terms(P, u)
    Pw = mono_str(Pt, "w")
    dPt = "%s * (%s)" % (rat(-sp.Rational(s, 1)/(p+1)), Qx)
    Fw = "%s + ((w ^ %d - 1) / %d) * %s" % (Pw, p+1, p+1, uw)
    cA, cA0 = rat(sp.Rational(1, p+1)), rat(-sp.Rational(1, p+1))
    ALT = "%s * w ^ %d + %s * w ^ 0" % (cA, p+1, cA0)
    P0sum = " + ".join("%s * 0 ^ %d" % (rat(c), k) for c, k in Pt)
    P1sum = " + ".join("%s * 1 ^ %d" % (rat(c), k) for c, k in Pt)
    A("theorem %s : %s u in (0: \u211d)..1, u ^ %d * %s = %s := by" % (name, INT, p, uu, rat(val)))
    A("  have hint : IntervalIntegrable (fun x : \u211d => x ^ %d * %s) volume 0 1 := by" % (p, ux))
    for ln in hint_congr(s, p):
        A(ln)
    A("  have hderiv : %s x %s Set.Ioo (0: \u211d) 1, HasDerivAt" % (FORALL, IN))
    A("      (fun w : \u211d => %s)" % Fw)
    A("      (x ^ %d * %s) x := by" % (p, ux))
    A("    intro x hx")
    if s > 0:
        A("    have hx1 : (1: \u211d) + x %s 0 := by have := hx.1; linarith" % NE)
        A("    have hid : HasDerivAt (fun y : \u211d => y) 1 x := hasDerivAt_id' x")
        A("    have hinner : HasDerivAt (fun y : \u211d => 1 + y) ((0: \u211d) + 1) x := (hasDerivAt_const x 1).add hid")
        A("    have hlog : HasDerivAt (fun w : \u211d => Real.log (1 + w)) ((1: \u211d) / (1 + x)) x := by")
        A("      refine HasDerivAt.comp_of_eq x (hasDerivAt_log hx1) hinner rfl |>.congr_deriv ?_")
        A("      ring")
    else:
        A("    have hx1 : (1: \u211d) - x %s 0 := by have := hx.2; linarith" % NE)
        A("    have hid : HasDerivAt (fun y : \u211d => y) 1 x := hasDerivAt_id' x")
        A("    have hinner : HasDerivAt (fun y : \u211d => 1 - y) ((0: \u211d) - 1) x := (hasDerivAt_const x 1).sub hid")
        A("    have hlog : HasDerivAt (fun w : \u211d => Real.log (1 - w)) ((-1: \u211d) / (1 - x)) x := by")
        A("      refine HasDerivAt.comp_of_eq x (hasDerivAt_log hx1) hinner rfl |>.congr_deriv ?_")
        A("      ring")
    A("    have hA : HasDerivAt (fun w : \u211d => (w ^ %d - 1) / %d) (x ^ %d) x := by" % (p+1, p+1, p))
    A("      refine ((hasDerivAt_pow %d x).sub (hasDerivAt_const x 1)).div_const %d |>.congr_deriv ?_" % (p+1, p+1))
    A("      ring")
    A("    have hQ : (x: \u211d) ^ %d - 1 = (%s) * (%s) := by ring" % (p+1, "(1 + x)" if s > 0 else "(1 - x)", Qx))
    A("    have hP : HasDerivAt (fun w : \u211d => %s) (%s) x := by" % (Pw, dPt))
    A("      refine %s |>.congr_deriv ?_" % deriv_chain(Pt, "x"))
    A("      ring")
    A("    refine (hP.add (hA.mul hlog)).congr_deriv ?_")
    A("    field_simp [hQ]; ring")
    A("  have hPc0 : ContinuousAt (fun w : \u211d => %s) 0 := %s" % (Pw, mono_chain(Pt, "0")))
    A("  have hPc1 : ContinuousAt (fun w : \u211d => %s) 1 := %s" % (Pw, mono_chain(Pt, "1")))
    A("  have hAc0 : ContinuousAt (fun w : \u211d => %s) 0 := (mono_contAt %s %d 0).add (mono_contAt %s 0 0)" % (ALT, cA, p+1, cA0))
    A("  have hAc1 : ContinuousAt (fun w : \u211d => %s) 1 := (mono_contAt %s %d 1).add (mono_contAt %s 0 1)" % (ALT, cA, p+1, cA0))
    A("  have heq : (fun w : \u211d => %s) = (fun w : \u211d => %s + (%s) * %s) := by" % (Fw, Pw, ALT, uw))
    A("    funext w")
    A("    have hdiv : (w ^ %d - 1) / %d = %s * w ^ %d + %s * w ^ 0 := by ring" % (p+1, p+1, cA, p+1, cA0))
    A("    rw [hdiv]")
    if s > 0:
        A("  have hv0 : (%s + (%s * 0 ^ %d + %s * 0 ^ 0) * Real.log (1 + 0)) = (0: \u211d) := by norm_num [Real.log_one]" % (P0sum, cA, p+1, cA0))
        A("  have hv1 : (%s + (%s * 1 ^ %d + %s * 1 ^ 0) * Real.log (1 + 1)) = %s := by norm_num [Real.log_one]" % (P1sum, cA, p+1, cA0, rat(val)))
        A("  have ha : Tendsto (fun w : \u211d => %s) (nhdsWithin (0: \u211d) (Set.Ioi 0)) (nhds (0: \u211d)) := by" % Fw)
        A("    rw [heq]")
        A("    have hten : Tendsto (fun w : \u211d => %s + (%s) * %s) (nhdsWithin (0: \u211d) (Set.Ioi 0)) (nhds (%s + (%s * 0 ^ %d + %s * 0 ^ 0) * Real.log (1 + 0))) :=" % (Pw, ALT, uw, P0sum, cA, p+1, cA0))
        A("      (hPc0.add (hAc0.mul logp_contAt0)).tendsto.mono_left nhdsWithin_le_nhds")
        A("    rwa [hv0] at hten")
        A("  have hb : Tendsto (fun w : \u211d => %s) (nhdsWithin (1: \u211d) (Set.Iio 1)) (nhds %s) := by" % (Fw, rat(val)))
        A("    rw [heq]")
        A("    have hten : Tendsto (fun w : \u211d => %s + (%s) * %s) (nhdsWithin (1: \u211d) (Set.Iio 1)) (nhds (%s + (%s * 1 ^ %d + %s * 1 ^ 0) * Real.log (1 + 1))) :=" % (Pw, ALT, uw, P1sum, cA, p+1, cA0))
        A("      (hPc1.add (hAc1.mul logp_contAt1)).tendsto.mono_left nhdsWithin_le_nhds")
        A("    rwa [hv1] at hten")
    else:
        A("  have hc0 : ContinuousAt (fun w : \u211d => Real.log (1 - w)) 0 := by")
        A("    have h1 : ContinuousAt (fun w : \u211d => 1 - w) 0 := by fun_prop")
        A("    exact ContinuousAt.comp_of_eq (Real.continuousAt_log (by norm_num : (1: \u211d) %s 0)) h1 (by norm_num)" % NE)
        A("  have hv0 : (%s + (%s * 0 ^ %d + %s * 0 ^ 0) * Real.log (1 - 0)) = (0: \u211d) := by norm_num [Real.log_one]" % (P0sum, cA, p+1, cA0))
        A("  have ha : Tendsto (fun w : \u211d => %s) (nhdsWithin (0: \u211d) (Set.Ioi 0)) (nhds (0: \u211d)) := by" % Fw)
        A("    rw [heq]")
        A("    have hten : Tendsto (fun w : \u211d => %s + (%s) * %s) (nhdsWithin (0: \u211d) (Set.Ioi 0)) (nhds (%s + (%s * 0 ^ %d + %s * 0 ^ 0) * Real.log (1 - 0))) :=" % (Pw, ALT, uw, P0sum, cA, p+1, cA0))
        A("      (hPc0.add (hAc0.mul hc0)).tendsto.mono_left nhdsWithin_le_nhds")
        A("    rwa [hv0] at hten")
        gz = "(-((1: \u211d) / %d)) * (%s)" % (p+1, gsum_str(p, "z"))
        gu = gz.replace("z", "u")
        A("  have hAeq : %s z : \u211d, (%s * z ^ %d + %s * z ^ 0) * Real.log (1 - z)" % (FORALL, cA, p+1, cA0))
        A("      = ((1 - z) * Real.log (1 - z)) * (%s) := by intro z; ring" % gz)
        A("  have tA2 : Tendsto (fun u : \u211d => (%s * u ^ %d + %s * u ^ 0) * Real.log (1 - u)) (nhdsWithin (1: \u211d) (Set.Iio 1)) (nhds (0: \u211d)) := by" % (cA, p+1, cA0))
        A("    have key : Tendsto (fun u : \u211d => ((1 - u) * Real.log (1 - u)) * (%s)) (nhdsWithin (1: \u211d) (Set.Iio 1)) (nhds (0: \u211d)) :=" % gu)
        A("      tendsto_alm (by fun_prop : ContinuousAt (fun u : \u211d => %s) 1)" % gu)
        A("    have heq2 : (fun u : \u211d => (%s * u ^ %d + %s * u ^ 0) * Real.log (1 - u))" % (cA, p+1, cA0))
        A("        = (fun u : \u211d => ((1 - u) * Real.log (1 - u)) * (%s)) := by" % gu)
        A("      funext u; rw [hAeq u]")
        A("    rw [heq2]; exact key")
        A("  have hv1 : (%s + (0: \u211d)) = %s := by norm_num" % (P1sum, rat(val)))
        A("  have hb : Tendsto (fun w : \u211d => %s) (nhdsWithin (1: \u211d) (Set.Iio 1)) (nhds %s) := by" % (Fw, rat(val)))
        A("    rw [heq]")
        A("    have hten : Tendsto (fun w : \u211d => %s + (%s) * %s) (nhdsWithin (1: \u211d) (Set.Iio 1)) (nhds (%s + (0: \u211d))) :=" % (Pw, ALT, uw, P1sum))
        A("      (hPc1.tendsto.mono_left nhdsWithin_le_nhds).add tA2")
        A("    rwa [hv1] at hten")
    A("  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_tendsto (a := (0: \u211d)) (b := (1: \u211d))")
    A("    (by norm_num : (0: \u211d) < (1: \u211d)) hderiv hint ha hb")
    A("  exact h.trans (by norm_num)")
    A("")

for (kind, s, p), val in sorted(CORE.items(), key=str):
    if kind != "P": continue
    A("theorem poly_core_%d : %s u in (0: \u211d)..1, u ^ %d = %s := by" % (p, INT, p, rat(val)))
    A("  have hderiv : %s x %s Set.Ioo (0: \u211d) 1, HasDerivAt (fun w : \u211d => w ^ %d / %d) (x ^ %d) x := by" % (FORALL, IN, p+1, p+1, p))
    A("    intro x _")
    A("    refine ((hasDerivAt_pow %d x).div_const %d) |>.congr_deriv ?_" % (p+1, p+1))
    A("    ring")
    A("  have hint : IntervalIntegrable (fun x : \u211d => x ^ %d) volume 0 1 := Continuous.intervalIntegrable (by fun_prop) 0 1" % p)
    A("  have ha : Tendsto (fun w : \u211d => w ^ %d / %d) (nhdsWithin (0: \u211d) (Set.Ioi 0)) (nhds (((0: \u211d) ^ %d) / %d)) :=" % (p+1, p+1, p+1, p+1))
    A("    ((by fun_prop : ContinuousAt (fun w : \u211d => w ^ %d / %d) 0) |>.tendsto |>.mono_left nhdsWithin_le_nhds)" % (p+1, p+1))
    A("  have hb : Tendsto (fun w : \u211d => w ^ %d / %d) (nhdsWithin (1: \u211d) (Set.Iio 1)) (nhds (((1: \u211d) ^ %d) / %d)) :=" % (p+1, p+1, p+1, p+1))
    A("    ((by fun_prop : ContinuousAt (fun w : \u211d => w ^ %d / %d) 1) |>.tendsto |>.mono_left nhdsWithin_le_nhds)" % (p+1, p+1))
    A("  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_tendsto (a := (0: \u211d)) (b := (1: \u211d)) (by norm_num : (0: \u211d) < (1: \u211d)) (f' := fun x : \u211d => x ^ %d) hderiv hint ha hb" % p)
    A("  exact h.trans (by norm_num)")
    A("")

for (kind, s, p), val in sorted(CORE.items(), key=str):
    if kind == "L": core_lean(s, p, val)

def term_str(t):
    if t["kind"] == "L":
        uu = "Real.log (1 - u)" if t["s"] < 0 else "Real.log (1 + u)"
        return "%s * (u ^ %d * %s)" % (rat(t["coeff"]), t["p"], uu)
    return "%s * u ^ %d" % (rat(t["coeff"]), t["p"])

for ch in "abc":
    for k, t in enumerate(terms[ch]):
        cname = ("core_lm_%d" % t["p"]) if (t["kind"] == "L" and t["s"] < 0) else \
                ("core_lp_%d" % t["p"]) if t["kind"] == "L" else ("poly_core_%d" % t["p"])
        A("theorem term_%s%d : %s u in (0: \u211d)..1, %s = %s := by" % (ch, k, INT, term_str(t), rat(t["value"])))
        A("  rw [intervalIntegral.integral_const_mul, %s]" % cname)
        A("  norm_num")
        A("")

for ch in "abc":
    n = len(terms[ch])
    tot = sum(t["value"] for t in terms[ch])
    ts = [term_str(t) for t in terms[ch]]
    rstr = {n-1: ts[n-1]}
    for k in range(n-2, -1, -1):
        rstr[k] = "%s + (%s)" % (ts[k], rstr[k+1])
    A("theorem ch_%s : %s u in (0: \u211d)..1, %s = %s := by" % (ch, INT, rstr[0], rat(tot)))
    for k, t in enumerate(terms[ch]):
        if t["kind"] == "L":
            A("  have hint%d : IntervalIntegrable (fun u : \u211d => %s) volume 0 1 := by" % (k, ts[k]))
            for ln in hint_congr(t["s"], t["p"], C=t["coeff"]):
                A(ln)
        else:
            A("  have hint%d : IntervalIntegrable (fun u : \u211d => %s) volume 0 1 := by" % (k, ts[k]))
            A("    refine Continuous.intervalIntegrable (Continuous.mul continuous_const (by fun_prop : Continuous fun u : \u211d => u ^ %d))" % t["p"])
            A("      0 1")
    A("  have rs%d : IntervalIntegrable (fun u : \u211d => %s) volume 0 1 := hint%d" % (n-1, rstr[n-1], n-1))
    for k in range(n-2, -1, -1):
        A("  have rs%d : IntervalIntegrable (fun u : \u211d => %s) volume 0 1 := hint%d.add rs%d" % (k, rstr[k], k, k+1))
    rws = ["intervalIntegral.integral_add hint%d rs%d" % (k, k+1) for k in range(n-1)]
    A("  rw [%s]" % ", ".join(rws))
    A("  rw [%s]" % ", ".join("term_%s%d" % (ch, k) for k in range(n)))
    A("  norm_num")
    A("")

A("theorem c1_q0 : ((37: \u211d) / 60 - (1: \u211d) / 3) = ((17: \u211d) / 60) := by norm_num")
A("theorem c1_q1 : ((701: \u211d) / 1050 - (1: \u211d) / 3) = ((117: \u211d) / 350) := by norm_num")
A("theorem c1_q2 : ((3491: \u211d) / 18375 - (46: \u211d) / 525) = ((627: \u211d) / 6125) := by norm_num")
A("theorem c1_law : %s q : \u211d, ((17: \u211d) / 60 + (117 / 350) * q + (627 / 6125) * q ^ 2)" % FORALL)
A("    = ((37: \u211d) / 60 + (701 / 1050) * q + (3491 / 18375) * q ^ 2)")
A("    - ((1: \u211d) / 3 + (1 / 3) * q + (46 / 525) * q ^ 2) := by")
A("  intro q; ring")
A("")
for th in ["ch_a", "ch_b", "ch_c"]:
    A("#print axioms %s" % th)
A("")

src = "\n".join(L) + "\n"
open(LEANF, "w").write(src)
log("emitted %s (%d lines)" % (LEANF, len(L)))

# ---------- G-L1: compile ----------
r = subprocess.run(["lake", "env", "lean", "LR10_rat.lean"], cwd=LEANDIR,
                   capture_output=True, text=True, timeout=1800)
outp = r.stdout + r.stderr
open(STDOUT, "w").write(outp)
log("lake env lean rc=%d (%d bytes stdout)" % (r.returncode, len(outp)))
if r.returncode != 0:
    finish(1, "G-L1 FIRED: lean compile rc=%d (fires preserved verbatim in LR10B_lean_stdout.txt)" % r.returncode,
           dict(lean_stdout_head=outp[:4000]))
import re as _re
src_txt = open(LEANF).read()
n_sorry = len(_re.findall(r"\bsorry\b|\badmit\b", src_txt))
if n_sorry != 0:
    finish(1, "G-L1 FIRED: %d sorry/admit tokens in emitted file" % n_sorry)
AX_OK = {"propext", "Classical.choice", "Quot.sound"}
bad = []
hits = 0
for m in _re.finditer(r"'(ch_[abc])' depends on axioms: \[([^\]]*)\]", outp):
    hits += 1
    axs = {a.strip() for a in m.group(2).split(",")}
    if not axs <= AX_OK:
        bad.append((m.group(1), sorted(axs)))
for m in _re.finditer(r"'(ch_[abc])' does not depend on any axioms", outp):
    hits += 1
if hits < 3:
    finish(1, "G-L1 FIRED: #print axioms output missing for ch_a/ch_b/ch_c")
if bad:
    finish(1, "G-L1 FIRED: axiom overflow %s" % bad)
finish(0, "BANKED: all gates PASS (G-L0, G-L2, G-L1); LR10_rat.lean = zero-sorry Lean certificate of the rational closed forms",
       dict(a="37/60", b="701/1050", c="3491/18375",
            c1="17/60 + (117/350)q + (627/6125)q^2",
            lean_file=LEANF, lean_stdout=STDOUT))
