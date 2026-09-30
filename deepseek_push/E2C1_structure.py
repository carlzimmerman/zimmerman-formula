#!/usr/bin/env python3
"""E2C1 (Z15 door): Lean certificate of the E2(q) degree-2 structure.
G1: lake env lean on E2C1_structure.lean -- rc 0, no sorry, axiom subset.
G2: fresh sympy q-expansion == pre-registered forms; .lean contains L1/L5.
G3: E2Q1_results.json loaded-not-transcribed (exit 0, maxdeg 2, qfree True).
Pre-registration: Z15-WAVE_BRIEF.md, commit e7840fc69 (BEFORE any run).
"""
import json, os, re, subprocess, sys, time
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN_DIR = os.path.join(os.path.dirname(HERE), "fable_independent_2026/lean_2026")
LEAN = os.path.join(LEAN_DIR, "E2C1_structure.lean")
LOG = []
T0 = time.time()
def P(s=""):
    print(s, flush=True); LOG.append(s)

ok = True

# ---- G2: fresh sympy re-derivation of the q-expansion ----
a1, s1, W2, A2, c00f, c0qf, qq = sp.symbols("a1 s1 W2 A2 c00f c0qf q", real=True)
integrand = sp.expand((1 + qq*a1) * (s1*(W2 + qq*A2) + (c00f + qq*c0qf)))
degset = sorted({m[0][0] for m in sp.Poly(integrand, qq).terms()})  # run-1 fix: univariate terms() monoms are 1-tuples
P(f"G2: fresh q-degree set: {degset}")
if degset != [0, 1, 2]:
    P("G2 FIRE: degree set != {0,1,2}"); ok = False
C0 = sp.expand(integrand.coeff(qq, 0)); C1 = sp.expand(integrand.coeff(qq, 1)); C2 = sp.expand(integrand.coeff(qq, 2))
want0 = s1*W2 + c00f
want1 = a1*(s1*W2 + c00f) + s1*A2 + c0qf
want2 = a1*(s1*A2 + c0qf)
for name, got, want in (("C0", C0, want0), ("C1", C1, want1), ("C2", C2, want2)):
    d = sp.simplify(sp.expand(got - want))
    P(f"G2: coefficient {name}: fresh {got} vs pre-registered {want}: dev {d}")
    if d != 0:
        P(f"G2 FIRE: {name} mismatch"); ok = False
qf = {v for v in (C0.free_symbols | C1.free_symbols | C2.free_symbols)}
P(f"G2: symbols in coefficients: {sorted(map(str, qf))} -- q-free: {qq not in qf}")  # run-1 fix: real-assumption Symbols sort via Relational
if qq in qf:
    P("G2 FIRE: q appears in a coefficient"); ok = False

# Lean file must literally contain the law statements (LR9 G2 precedent)
lean = open(LEAN).read()
pats = ["theorem e2c1_integrand_q_expansion",
        "+ q ^ 2 * (a1 * (s1 * A2 + c0qf))",
        "theorem e2c1_poly_eval", "theorem e2c1_coeff_gt2", "theorem e2c1_coeff2",
        "theorem e2c1_c1_quadratic", "(c - 46/525) * q ^ 2",
        "variable {R : Type*} [CommRing R]"]
for pat in pats:
    if pat not in lean:
        P(f"G2 MISSING in lean file: {pat!r}"); ok = False
P(f"G2: lean statement patterns: all {len(pats)} present" if ok else "G2: see fires above")

# ---- G3: chain -- E2Q1 banked verdict, loaded-not-transcribed ----
E = json.load(open(os.path.join(HERE, "E2Q1_results.json")))
g3 = (E["exit"] == 0 and E["r0"]["maxdeg"] == 2 and E["r0"]["qfree"] is True)
P(f"G3: E2Q1_results.json: exit {E['exit']}, r0.maxdeg {E['r0']['maxdeg']}, r0.qfree {E['r0']['qfree']} -> {'PASS' if g3 else 'FIRE'}")
if not g3: ok = False
fit = E["fit"]
zs = {k: abs(fit[k]/fit["s"+k]) for k in "abc"}
P(f"G3: measured nonvanishing (degree EXACTLY 2 payload): |z| a={zs['a']:.0f} b={zs['b']:.0f} c={zs['c']:.0f} (E2Q1 fit block)")

# ---- G1: compile ----
P("G1: lake env lean E2C1_structure.lean ...")
r = subprocess.run(["lake", "env", "lean", "E2C1_structure.lean"], cwd=LEAN_DIR,
                   capture_output=True, text=True, timeout=1200)
out = (r.stdout + r.stderr)
open(os.path.join(HERE, "E2C1_lean_stdout.txt"), "w").write(out)
P(f"G1: lake rc {r.returncode}")
axok = True
for line in out.splitlines():
    if "depends on axioms" in line:
        P(f"G1: {line.strip()}")
        m = re.search(r"\[(.*)\]", line)
        ax = {x.strip() for x in m.group(1).split(",")} if m else set()
        if not ax <= {"propext", "Classical.choice", "Quot.sound"}:
            P(f"G1 FIRE: axioms {ax} not a subset"); axok = False; ok = False
errlines = [l for l in out.splitlines() if "error" in l.lower()]
for l in errlines:
    P(f"G1 FIRE: {l.strip()}"); ok = False
if "declaration uses 'sorry'" in out:
    P("G1 FIRE: a declaration uses 'sorry'"); ok = False
if r.returncode != 0:
    P("G1 FIRE: nonzero lake exit"); ok = False
if r.returncode == 0 and axok and not errlines and "declaration uses 'sorry'" not in out:
    P("G1 PASS: rc 0, zero sorry, zero error, axioms subset {propext, Classical.choice, Quot.sound}")

P("")
P(("E2C1 ALL PASS" if ok else "E2C1 FIRED") + f"  ({time.time()-T0:.0f} s)")
res = dict(title="E2C1: Lean certificate of the E2(q) degree-2 structure (Z15 door)",
           pre_registration="Z15-WAVE_BRIEF.md, commit e7840fc69 (before any run)",
           verdict=("BANKED: exit 0 -- L1 unconditional ring expansion + L2 polynomial form + "
                    "L3 coeff>2 zero + L4 coeff2 exact q-free (all over an arbitrary CommRing, "
                    "no side hypotheses -- LR4b trap respected) + L5 c1 chain assembly over Q "
                    "with the LR9-certified S(q) constants; zero sorry, axioms subset "
                    "{propext, Classical.choice, Quot.sound}. Degree EXACTLY 2 carried at the "
                    "measured level by E2Q1 (a,b,c nonzero at |z| = 2682/1193/1601). "
                    "K01 label: consistency-family A/B-class (algebra of the model's own "
                    "integrand definition); certificate-grade status is the payload.")
           if ok else "FIRED -- see log",
           exit=0 if ok else 1, lean_rc=r.returncode, g2_degset=degset,
           g3_e2q1=dict(exit=E["exit"], maxdeg=E["r0"]["maxdeg"], qfree=E["r0"]["qfree"]),
           measured_nonvanishing_z={k: zs[k] for k in "abc"},
           elapsed_s=round(time.time()-T0, 1), log=LOG)
open(os.path.join(HERE, "E2C1_results.json"), "w").write(json.dumps(res, indent=1) + "\n")
sys.exit(0 if ok else 1)
