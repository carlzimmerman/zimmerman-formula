#!/usr/bin/env python3
"""CG1 part A: original, minimal and full repairs; same-bar matrix. --mutate restores the mismatch behind the guard. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, subprocess, sys
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, HERE)
import gate.fdr as F, gate.forced_kernel as K
assert os.path.dirname(os.path.dirname(os.path.abspath(F.__file__))) == HERE
import calibrate_original_copy as C
from gate.verdict import validate
from gate.candidate import Candidate
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""; OUT = []; RES = {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
def setrep(on):
    for k in F.REPAIRS: F.REPAIRS[k] = on
    K.REPAIR_A5 = on
FOOT = dict(canonical=9.3603e-11, alt=1.1312e-10); A0T = 1.2e-10; TOL = .05
def a0_cand(rel=None, target=A0T):
    c = C.candidate_a0(); s = c.search
    r = rel if rel is not None else A0T
    def null(N):
        rng = np.random.default_rng(20260625); return 10. ** rng.uniform(-1, 1, size=N) * 2 * r
    s.structural_null = null; s.structural_target = target; s.structural_relation = r; s.structural_eps = target * TOL
    return c
def row(name, c, req=None):
    v = validate(c); b = v.fdr.bits
    d = dict(status=v.status, A=bool(v.fdr.passed), B=bool(v.kernel.passed), C=bool(v.interlock.passed), bits=("inf" if math.isinf(b) else round(float(b), 3)), mode=v.fdr.mode, tell=v.fdr.tell, required=req, ok=(v.status == req) if req else None, B_tell=v.kernel.tell, C_tell=v.interlock.tell)
    P(f"  {name[:44]:<45} A {'P' if d['A'] else 'F'} B {'P' if d['B'] else 'F'} C {'P' if d['C'] else 'F'} bits {str(d['bits']):>8} {v.status:<24} {d['mode']}" + (f" {'row ok' if d['ok'] else 'ROW FAILS, required ' + req}" if req else ""))
    return d
def suite(a0rows):
    out = {}
    for name, c, r in a0rows: out[name] = row(name, c, r)
    for b, r, g, kind in C.SUITE[1:]:
        c = b(); out[c.name] = row(c.name, c, r)
    return out
# K2 true original
r = subprocess.run([sys.executable, "-B", os.path.join(REPO, "project_atomos", "calibration", "calibrate.py")], capture_output=True, text=True, cwd=os.path.join(REPO, "project_atomos")); line = [l for l in r.stdout.splitlines() if "CALIBRATION VERDICT" in l]; inf = "bits=inf" in r.stdout
P("K2 project_atomos original: " + (line[0] if line else "NO VERDICT") + f"; a0 bits inf printed: {inf}"); RES["K2"] = bool(line and "8/8" in line[0] and inf)
P("\nR0 local copy, repairs off, original candidate"); setrep(False); RES["R0"] = suite([("a0 kernel, original candidate", C.candidate_a0(), "CERTIFIED")])
P("\nR1 A1 only: null compared with a0 = 1.2e-10"); RES["R1"] = suite([("a0, A1 only", a0_cand(), "CERTIFIED")])
P("\nR2 all repairs, per footing"); setrep(True)
if MUT:
    bad = a0_cand(FOOT["alt"], target=C.KERNEL); bad.search.structural_eps = C.KERNEL * TOL; rows = [("a0 alt, MUTATE mismatch restored", bad, "CERTIFIED")]
else:
    rows = [(f"a0 {k} {v:.4e}", a0_cand(v), "CERTIFIED") for k, v in FOOT.items()] + [("a0 as bits, relation set to target", a0_cand(), "CERTIFIED")]
RES["R2"] = suite(rows); RES["R2_rows_ok"] = sum(1 for d in RES["R2"].values() if d["ok"]); RES["R2_rows"] = len(RES["R2"])
P(f"R2 rows matching required status: {RES['R2_rows_ok']}/{RES['R2_rows']}")
# A6 values
c = C.candidate_dsunruh_sqrt2(); P("A6 " + F.fdr_test(c).tell); RES["A6"] = F.fdr_test(c).tell
# same bar
P("\nSAME BAR 1: every row through a0's null, free factor log-uniform +- 1 dex about its relation, own tolerance. Exact bits = log2(2 / log10((1+t)/(1-t)))")
def a0null_bits(t): return math.log2(2 / math.log10((1 + t) / (1 - t)))
bar = {}; rowsb = [("a0, 5 %", A0T, A0T, TOL)]
for b, _, _, _ in C.SUITE[2:]:
    c = b(); rowsb.append((c.name, c.target_value, c.relation_value, c.search.tol))
for name, t, rel, tol in rowsb:
    close = abs(rel - t) / t; bits = a0null_bits(tol); bt = a0null_bits(close) if close > 0 else None
    rng = np.random.default_rng(7); mc = float(np.mean(np.abs(10. ** rng.uniform(-1, 1, 2000000) * rel - t) < t * tol)) if rel else 0
    bar[name] = dict(tol=tol, closeness=close, bits_at_tol=bits, bits_at_closeness=bt, mc_P=mc, hit_at_tol=bool(close < tol))
    P(f"  {name[:40]:<41} tol {tol:<7.4g} closeness {close:.2e} bits at tol {bits:6.2f} at closeness {('n/a' if bt is None else f'{bt:.2f}'):>6}, MC P {mc:.2e}")
RES["bar1"] = bar
P("\nSAME BAR 2: a0's kernel 2.894 through the germ-pool route at 5 %, and negatives at actual closeness")
setrep(True); lib = F.build_value_set(C.GERM_POOL); bar2 = {}
n, e = F._poisson_e_chance(C.KERNEL, lib, TOL); bar2["a0 kernel 5 %"] = dict(n_hit=n, e_chance=e); P(f"  kernel 2.894, tol 5 %: {n} hits, E_chance {e:.1f}, BAKED by the route the negatives get")
n, e = F._poisson_e_chance(1 / C.Z, lib, TOL); bar2["1/Z 5 %"] = dict(n_hit=n, e_chance=e); P(f"  x = 1/Z 0.1727, tol 5 %: {n} hits, E_chance {e:.1f}")
for b, _, _, _ in C.SUITE[2:7]:
    c = b(); t = c.target_value; close = max(abs(c.relation_value - t) / t, 1e-12); n, e = F._poisson_e_chance(t, lib, close); bar2[c.name] = dict(closeness=close, n_hit=n, e_chance=e, bits=-math.log2(min(1, e)) if e > 0 else None)
    P(f"  {c.name[:30]:<31} closeness {close:.2e}: {n} hits, E_chance {e:.3g}, bits {bar2[c.name]['bits'] if e>0 else None}")
RES["bar2"] = bar2
P("\nSAME BAR 3: Koide null, mass range sensitivity, eps 1e-5")
Q = lambda m: m.sum(1) / np.sqrt(m).sum(1) ** 2; kd = {}
for lo, hi in ((-2, 4), (-3, 5), (-1, 3.5)):
    rng = np.random.default_rng(20260625); q = Q(10. ** rng.uniform(lo, hi, size=(4000000, 3))); p = float(np.mean(np.abs(q - 2 / 3) < 1e-5)); kd[f"{lo},{hi}"] = p; P(f"  decades [{lo},{hi}]: P {p:.3e}, bits {-math.log2(p) if p else None:.2f}")
qm = (C.M_E + C.M_MU + C.M_TAU) / (C.M_E ** .5 + C.M_MU ** .5 + C.M_TAU ** .5) ** 2; RES["koide"] = dict(P=kd, Q=qm, dev=qm - 2 / 3); P(f"  Q measured {qm:.7f}, dev {qm-2/3:+.2e}. Null window chosen at this deviation; no multiplier for the choice of form")
# B laxness
setrep(False); c = C.candidate_a0(); c.coefficient.target_value = C.KERNEL * 7.3; lax = K.forced_kernel_detector(c).passed; setrep(True); c = C.candidate_a0(); c.coefficient.target_value = C.KERNEL * 7.3; strict = K.forced_kernel_detector(c).passed
P(f"\nA5 check: a coefficient 7.3 x kernel, same declarations: original gate B passes {lax}, repaired {strict}"); RES["A5"] = dict(orig=bool(lax), repaired=bool(strict))
# label
neg = [C.SUITE[i][0]().name for i in range(2, 7)]
a0b = max([d["bits"] for k, d in RES["R1"].items() if k.startswith("a0")]); kok = any(d["status"] == "REAL-PUZZLE-RE-LABELED" for d in RES["R2"].values()); a0cert = any(d["status"] == "CERTIFIED" for k, d in RES["R2"].items() if k.startswith("a0")); negdead = all(RES["R2"][n]["status"] == "FDR-DEAD" for n in neg)
beat = [n for n in neg if bar[n]["bits_at_tol"] >= bar["a0, 5 %"]["bits_at_tol"]]; RES["negs_at_or_above_a0_under_a0s_null"] = beat
lab = "SEPARATES" if (a0cert and kok and negdead and not beat) else "SEPARATES KOIDE ONLY" if (kok and negdead) else "DOES NOT SEPARATE"; RES["label"] = lab
P(f"\nSEPARATION LABEL: {lab}; a0 certified {a0cert}; Koide holds {kok}; negatives dead {negdead}; a0 R1 bits {a0b}; negatives at or above a0 under a0's null: {len(beat)}/{len(neg)}")
json.dump(RES, open(f"cg1_gate{TAG}.json", "w"), indent=1, sort_keys=True, default=lambda o: o.item() if hasattr(o, "item") else str(o)); open(f"cg1_gate{TAG}.out", "w").write("\n".join(OUT) + "\n")
sys.exit(1 if (MUT and RES["R2"].get("a0 alt, MUTATE mismatch restored", {}).get("mode") == "NULL-SCALE-MISMATCH") else 0)
