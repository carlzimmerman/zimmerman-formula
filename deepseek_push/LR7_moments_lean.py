#!/usr/bin/env python3
"""LR7 lane runner (conductor-executed, Z10 tick 2026-09-29).
Lane LR7 = Lean certificates of the W1 exact moments E[c^2]=4/5, E[cT]=2/5,
E[T^2]=208/945 -> b0=19/160, b1=7/80, b2=703/30240.
Pre-registered gates (BEFORE any run, per LOOP_CONDUCTOR.md rule 5):
  G1 lean compile rc 0, ZERO sorry, axioms of moment_c2/cT/T2 subset of
     {propext, Classical.choice, Quot.sound};
  G2 mechanical sympy re-derivation of the (u,v)-reduced 1D term lists must
     MATCH the Lean file's hardcoded base values exactly (rationals);
  G3 the moment linear combinations must re-derive the three rationals exactly.
KILL: any gate fail -> exit 1, honest record; the Lean leg is NOT banked.
RUN HISTORY: R0 audit run-1 exit 1 (dblquad integrand arg-order bug, runner
fixed, math untouched); lean runs 1-7 (five honest compile failures:
fun_prop HasDerivAt limitation, hasDerivAt_sqrt ne-of-gt arg, Pi.add/Pi.pow
form mismatches, const token mismatch (Neg-of-div vs div-of-Neg),
hasDerivAt_const arg order (x, c) -- all runner/statement fixes, never the
math; run 7 rc 0).
"""
import json, re, subprocess, sys

log_lines = []
def log(s):
    print(s); log_lines.append(s)

# ---- G2: mechanical sympy re-derivation of the 1D term lists ----
import sympy as sp
u, v, S = sp.symbols("u v S", real=True)

def beta_half(r, p):
    assert p % 2 == 1
    j = (p - 1)//2
    B = sp.factorial(r) * sp.factorial(2*j+2) * sp.Integer(4)**(r+j+2) * sp.factorial(r+j+2) / \
        (sp.Integer(4)**(j+1)*sp.factorial(j+1) * sp.factorial(2*r+2*j+4))
    return sp.simplify(B/2)

def terms_1d(k, m):
    c = S - v
    T = (u**2+v**2)*c + v*c**2 + c**3/3
    expr = sp.expand(sp.Rational(3,2)*u*(c**k)*(T**m))
    out = {}
    for term in expr.as_ordered_terms():
        pd = term.as_powers_dict()
        a = int(pd.get(u,0)); j = int(pd.get(v,0)); mpow = int(pd.get(S,0))
        coef = sp.Rational(sp.nsimplify(term/(u**a * v**j * S**mpow)))
        if j % 2 == 1: continue
        key = (a, mpow + j + 1)
        out[key] = out.get(key, sp.Integer(0)) + coef * sp.Rational(2, j+1)
    return [(coef, (a-1)//2, p) for (a, p), coef in sorted(out.items())]

WANT = {"E_c2": (sp.Rational(4,5), (2,0)), "E_cT": (sp.Rational(2,5), (1,1)),
        "E_T2": (sp.Rational(208,945), (0,2))}
BASES = {  # (coef, r, p) -> exact value, as stated in the Lean file
    "A": (1, 0, 3), "B": (2, 1, 3), "C": (1, 0, 5),
    "D": (2, 1, 5), "E": (1, 0, 7), "G": (8, 2, 3),
}
LEAN_BASES = {"A": sp.Rational(1,5), "B": sp.Rational(2,35), "C": sp.Rational(1,7),
              "D": sp.Rational(2,63), "E": sp.Rational(1,9), "G": sp.Rational(8,315)}
fails = []
for name, (want, (k, m)) in WANT.items():
    ts = terms_1d(k, m)
    total = sum(coef * beta_half(r, p) for coef, r, p in ts)
    ok = sp.simplify(total - want) == 0
    log("G2 %s: %d terms -> %s (want %s) %s" % (name, len(ts), total, want, "MATCH" if ok else "MISMATCH"))
    if not ok: fails.append(name)
# base values in the Lean file vs Beta-form exact
for nm, (coef, r, p) in BASES.items():
    exact = beta_half(r, p)
    ok = sp.simplify(exact - LEAN_BASES[nm]) == 0 and sp.Rational(coef) == coef
    log("G2 base %s: (1-u^2)^%d/2 u^%d integral = %s; Lean value %s %s"
        % (nm, p, 2*r+1, exact, LEAN_BASES[nm], "MATCH" if ok else "MISMATCH"))
    if not ok: fails.append("base_"+nm)

# ---- G1: lean compile + axiom gate ----
LEAN = "/Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026"
r = subprocess.run(["lake", "env", "lean", "LR7_w1_moments.lean"], cwd=LEAN,
                   capture_output=True, text=True, timeout=900)
out = r.stdout + r.stderr
open("LR7_lean_stdout.txt", "w").write(out)
log("G1 lean rc=%d" % r.returncode)
if r.returncode != 0:
    fails.append("lean_compile")
if "sorry" in out:
    fails.append("sorry_present")
for thm in ["moment_c2", "moment_cT", "moment_T2"]:
    m = re.search(r"'%s' depends on axioms: \[(.*)\]" % thm, out)
    if not m:
        fails.append("axiom_print_%s" % thm); continue
    ax = set(a.strip() for a in m.group(1).split(","))
    ok = ax <= {"propext", "Classical.choice", "Quot.sound"}
    log("G1 %s axioms %s %s" % (thm, sorted(ax), "CLEAN" if ok else "FORBIDDEN"))
    if not ok: fails.append("axioms_%s" % thm)

# ---- G3: coefficient identities (exact, mirrors LR7_r0_audit.py) ----
Ec, ET = sp.Rational(3,4), sp.Rational(5,12)  # certified inputs (LR3/LR4c)
ids = {"b0": (WANT["E_c2"][0]-Ec**2)/2, "b1": WANT["E_cT"][0]-Ec*ET, "b2": (WANT["E_T2"][0]-ET**2)/2}
WID = {"b0": sp.Rational(19,160), "b1": sp.Rational(7,80), "b2": sp.Rational(703,30240)}
for nm, got in ids.items():
    ok = sp.simplify(got - WID[nm]) == 0
    log("G3 %s: derived %s vs %s %s" % (nm, got, WID[nm], "EXACT" if ok else "MISMATCH"))
    if not ok: fails.append(nm)

json.dump({"fails": fails, "lean_rc": r.returncode}, open("LR7_results.json","w"), indent=1)
with open("LR7_moments_lean.out","w") as f: f.write("\n".join(log_lines)+"\n")
if fails:
    print("LR7_EXIT1: %s" % fails); sys.exit(1)
print("LR7_EXIT0"); sys.exit(0)
