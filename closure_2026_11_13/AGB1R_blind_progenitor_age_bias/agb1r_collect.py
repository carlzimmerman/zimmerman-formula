"""AGB1R collect: applies the known-answer checks and the frozen words; writes agb1r_results.json and agb1r_collect.out."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agb1r_common import HERE, dump

def J(name):
    p = os.path.join(HERE, name)
    return json.load(open(p)) if os.path.exists(p) else None

lines = []
def log(s=""): print(s); lines.append(s)

tm = J("agb1r_templates.json"); ch = {k: J(f"agb1r_checks_{k}.json") for k in ("counts", "k1", "k2", "k3", "k4")}
A = {m: J(f"agb1r_A_{m}.json") for m in ("full", "des_only", "rand197", "bao_overlap", "tmplW_full", "tmplW_des_only",
                                         "legacy_offset")}
C = {m: J(f"agb1r_C_{m}.json") for m in ("k5", "full", "des_only")}

checks = dict(counts=ch["counts"]["counts"]["pass"], KT=tm["KT"]["pass"], K1=ch["k1"]["K1"]["pass_"],
              K2=ch["k2"]["K2"]["pass_"], K3=ch["k3"]["K3"]["pass_"], K4=ch["k4"]["K4"]["pass_"], KA=A["full"]["KA"]["pass_"])
checksC = dict(K5=C["k5"]["K5_pass"], K6=C["full"]["K6"]["pass_"])
log("Known-answer checks: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in checks.items()))
log("Part C checks: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in checksC.items()))
evalA = all(checks[k] for k in ("KT", "K1", "K2", "K3", "K4", "KA"))
evalC = all(checksC.values())

def iv(x): return "open" if x is None else ("[" + ", ".join("open" if v is None else f"{v:+.3f}" for v in x) + "]")

res = dict(checks=checks, checksC=checksC, partA_evaluable=evalA, partC_evaluable=evalC)
for part, R, ev in (("A", A, evalA), ("C", C, evalC)):
    f = R["full"]
    first = f["W1_first"]
    second_from = ["des_only", "bao_overlap"] if part == "A" else ["des_only"]
    diff = [s for s in second_from if R[s]["W1_first"] != first]
    second = "ROBUST" if not diff else "FRAGILE (" + ", ".join(f"{s}: {R[s]['W1_first']}" for s in diff) + ")"
    w1 = f"{first}, {second}" if ev else f"NOT EVALUABLE (reading: {first}, {second})"
    tag = "W1" if part == "A" else "W1c"
    log(f"\nPart {part}  {tag}: {w1}")
    samples = ["full", "des_only", "rand197", "bao_overlap"] if part == "A" else ["full", "des_only"]
    for s in samples:
        r = R[s]
        log(f"  {s:12s} best A {r['A_free']['A']:+.3f}  dchi2=1 {iv(r['interval_1'])}  dchi2=4 {iv(r['interval_4'])}  "
            f"dchi2(A=0) {r['dchi2_A0']:.3f}  dchi2(A=1) {r['dchi2_A1']:.3f}  -> {r['W1_first']}")
    res[f"part{part}"] = dict(W1=w1, W1_first=first, W1_second=second)
    for s in (["full", "des_only", "bao_overlap"] if part == "A" else ["full", "des_only"]):
        for lab in ("A0", "A1", "Afree"):
            fk = R[s]["forks"][lab]; b = fk["best"]
            w2 = fk["W2"] if ev else f"NOT EVALUABLE (reading: {fk['W2']})"
            w3 = fk["W3"] if ev else f"NOT EVALUABLE (reading: {fk['W3']})"
            edge = (" AT PRIOR EDGE " + ",".join(b["edge"])) if b["edge"] else ""
            nm = fk["never"]; nmet = "" if nm.get("constraint_met", True) else " (never-fit CONSTRAINT NOT MET)"
            log(f"  {s:12s} fork {lab:5s} Om {b['Om']:.4f} w0 {b['w0']:+.3f} wa {b['wa']:+.3f} q0 {b['q0']:+.3f}"
                f" A {b['A']:+.3f}{edge}; dchi2_today {fk['dchi2_today']:.3f}; dchi2_never {fk['dchi2_never']:.3f}{nmet}"
                + (f"  -> W2 {w2}; W3 {w3}" if s != "bao_overlap" else "  (numbers only)"))
            res[f"part{part}"].setdefault(s, {})[lab] = dict(W2=fk["W2"], W3=fk["W3"], dchi2_today=fk["dchi2_today"],
                                                              dchi2_never=fk["dchi2_never"], best=b)
if A["full"]["W1_first"] != A["des_only"]["W1_first"]:
    log(f"\nrand197 control: first word {A['rand197']['W1_first']} "
        f"({'same as full: the change comes from the legacy set' if A['rand197']['W1_first'] == A['full']['W1_first'] else 'also changes'})")
for m in ("tmplW_full", "tmplW_des_only"):
    r = A[m]
    if r: log(f"\nreported {m}: best A_W {r['A_free']['A']:+.3f} dchi2=1 {iv(r['interval_1'])} dchi2=4 {iv(r['interval_4'])};"
              f" dchi2(A_W=0) {r['dchi2_A0']:.3f}, dchi2(A_W=0.23) {r['dchi2_AW_023']:.3f}, dchi2(A_W=1) {r['dchi2_A1']:.3f}")
r = A["legacy_offset"]
if r:
    log(f"\nreported legacy_offset: delta only: best delta {r['delta_only']['free']['A']:+.4f} mag, dchi2(delta=0) "
        f"{r['delta_only']['dchi2_delta0']:.3f}; delta and A free: best A {r['delta_and_A']['free']['A']:+.3f} (delta "
        f"{r['delta_and_A']['delta']:+.4f}) dchi2=1 {iv(r['delta_and_A']['interval_1'])} dchi2=4 "
        f"{iv(r['delta_and_A']['interval_4'])}; dchi2(A=0) {r['delta_and_A']['dchi2_A0']:.3f}, dchi2(A=1) "
        f"{r['delta_and_A']['dchi2_A1']:.3f}")
dump(res, os.path.join(HERE, "agb1r_results.json"))
open(os.path.join(HERE, "agb1r_collect.out"), "w").write("\n".join(lines) + "\n")
