"""AGB3R collector: checks, gates and the frozen words of AGB3 applied to this folder's outputs.

Usage: python3 -I agb3r_collect.py   (reads agb3r_*.json here; writes agb3r_results.json and prints the table)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
log = lambda m: print(m, flush=True)


def J(name):
    return json.load(open(os.path.join(HERE, f"agb3r_{name}.json")))


def w1(d0, d1):
    if d1 >= 9 and d0 < 4: return "AGE BIAS EXCLUDED AT 3 SIGMA"
    if 4 <= d1 < 9 and d0 < 4: return "AGE BIAS DISFAVOURED"
    if d0 >= 9 and d1 < 4: return "AGE BIAS REQUIRED AT 3 SIGMA"
    if 4 <= d0 < 9 and d1 < 4: return "AGE BIAS FAVOURED"
    if d0 < 4 and d1 < 4: return "UNDECIDED"
    return "NEITHER"


def wu(a, d1):
    if d1 < 4: return "HOSTS AS LARGE AS THE SLOPE NEEDS"
    if a < 1 and d1 >= 9: return "SLOPE OVERPREDICTS THE HOSTS AT 3 SIGMA"
    if a < 1: return "SLOPE OVERPREDICTS THE HOSTS (2 SIGMA)"
    return "HOSTS LARGER THAN THE SLOPE NEEDS"


def w2(q0, dt):
    if q0 < 0 and dt >= 4: return "ACCELERATING TODAY"
    if q0 > 0 and dt >= 4: return "DECELERATING TODAY"
    return "SIGN NOT SETTLED"


def w3(dn):
    if dn >= 9: return "NEVER-ACCELERATED EXCLUDED AT 3 SIGMA"
    if dn >= 4: return "NEVER-ACCELERATED DISFAVOURED"
    return "NEVER-ACCELERATED ALLOWED"


def second(first, forks):
    bad = [k for k, w in forks.items() if w != first]
    return ("ROBUST" if not bad else "FRAGILE (" + ", ".join(bad) + ")"), bad


def main():
    KM, K1, K3, K24, KS, D = J("KM")["KM"], J("K1")["K1"], J("K3")["K3"], J("K2K4"), J("KS")["KS"], J("D")
    K2, K4 = K24["K2"], K24["K4"]["cfg"]
    checks = dict(KM=KM["passed"], K1=K1["passed"], K2=K2["passed"], K3=K3["passed"],
                  K4_D1=K4["D1"]["passed"], K4_D2=K4["D2"]["passed"], K4_U=K4["U"]["passed"], KS=KS["passed"])
    log("CHECKS")
    for k, v in checks.items(): log(f"  {k:6s} {'PASS' if v else 'FAIL'}")
    d_ok = checks["KM"] and checks["K1"] and checks["K2"] and checks["K3"]
    se_ok = checks["KM"] and checks["K1"] and checks["KS"]
    res = dict(checks=checks, words={}, numbers={})

    # D2
    d2 = D["D2"]; p = d2["primary"]; first = w1(p["D_A0"], p["D_A1"])
    fk = {k: w1(v["D_A0"], v["D_A1"]) for k, v in d2.items() if k != "primary"}
    sec, _ = second(first, fk)
    ev = d_ok and checks["K4_D2"]
    res["words"]["D2"] = dict(first=first, second=sec, forks=fk, evaluable=ev)
    log(f"\nD2 (des_only, R, 20 bins, z_f 3, step free): A {p['A']:+.4f} +- {p['sd_A']:.4f}; dchi2(A=0) {p['D_A0']:.3f}, dchi2(A=1) {p['D_A1']:.3f}")
    for k, v in d2.items():
        if k != "primary": log(f"    fork {k:7s}: A {v['A']:+.4f} +- {v['sd_A']:.4f}  dchi2 {v['D_A0']:7.3f} {v['D_A1']:7.3f} -> {fk[k]}")
    log(f"  D2 = {first}, {sec}" + ("" if ev else "  [NOT EVALUABLE]"))

    # U
    u = D["U"]; p = u["primary"]; first = wu(p["A"], p["D_A1"])
    fk = {k: wu(v["A"], v["D_A1"]) for k, v in u.items() if k != "primary"}
    sec, _ = second(first, fk); ev = d_ok and checks["K4_U"]
    res["words"]["U"] = dict(first=first, second=sec, forks=fk, evaluable=ev)
    log(f"\nU (des_only, R, g = 0): A {p['A']:+.4f} +- {p['sd_A']:.4f}; dchi2(A=0) {p['D_A0']:.3f}, dchi2(A=1) {p['D_A1']:.3f}")
    for k, v in u.items():
        if k != "primary": log(f"    fork {k:7s}: A {v['A']:+.4f} +- {v['sd_A']:.4f}  dchi2 {v['D_A0']:7.3f} {v['D_A1']:7.3f} -> {fk[k]}")
    log(f"  U = {first}, {sec}" + ("" if ev else "  [NOT EVALUABLE]"))

    # S2, S3
    S = {k: J(f"S_{k}") for k in ("full", "des", "mass", "zf2", "zf5", "host")}
    b = S["full"]["best"]["A1"]; first = w2(b["q0"], b["D_today"])
    fk = {"des_only": w2(S["des"]["best"]["A1"]["q0"], S["des"]["best"]["A1"]["D_today"]),
          "mass_only_T_H": w2(S["mass"]["best"]["A1"]["q0"], S["mass"]["best"]["A1"]["D_today"]),
          "zf2": w2(S["zf2"]["best"]["A1"]["q0"], S["zf2"]["best"]["A1"]["D_today"]),
          "zf5": w2(S["zf5"]["best"]["A1"]["q0"], S["zf5"]["best"]["A1"]["D_today"])}
    sec, _ = second(first, fk)
    s3 = w3(b["D_never"]); s3f = {k: w3(S[sk]["best"]["A1"]["D_never"]) for k, sk in (("des_only", "des"), ("mass_only_T_H", "mass"), ("zf2", "zf2"), ("zf5", "zf5"))}
    res["words"]["S2"] = dict(first=first, second=sec, forks=fk, evaluable=se_ok)
    res["words"]["S3"] = dict(first=s3, forks=s3f, evaluable=se_ok)
    log("\nPart S at A_H = 1 (q0, dchi2_today, dchi2_never):")
    for k, sk in (("full (primary)", "full"), ("des_only", "des"), ("mass_only_T_H", "mass"), ("zf2", "zf2"), ("zf5", "zf5"), ("host_by_host", "host")):
        bb = S[sk]["best"]["A1"]; sm = S[sk]["summary"]
        log(f"  {k:15s} q0 {bb['q0']:+.4f}  today {bb['D_today']:7.3f}  never {bb['D_never']:8.3f}  -> {w2(bb['q0'], bb['D_today'])}; {w3(bb['D_never'])}"
            f"   | A_H free {sm['A_free']:+.3f}, dchi2(0) {sm['D_A0']:.3f}, dchi2(1) {sm['D_A1']:.3f}")
    log(f"  S2 = {first}, {sec};  S3 = {s3} (forks: {s3f})" + ("" if se_ok else "  [NOT EVALUABLE]"))

    # J2, J3
    Jr = J("J")["J"]; pj = Jr["primary"]; j_ok = res["words"]["D2"]["evaluable"] and se_ok
    first = w2(pj["q0"], pj["D_today"]); fk = {k: w2(Jr[k]["q0"], Jr[k]["D_today"]) for k in ("des_only", "D2_P", "half", "mass_T_H", "U_prior")}
    sec, _ = second(first, fk)
    res["words"]["J2"] = dict(first=first, second=sec, forks=fk, evaluable=j_ok)
    res["words"]["J3"] = dict(first=w3(pj["D_never"]), forks={k: w3(Jr[k]["D_never"]) for k in fk}, evaluable=j_ok)
    log("\nPart J (joint A_H, q0 at it, dchi2_today, dchi2_never):")
    for k, r in Jr.items():
        log(f"  {k:14s} A_H {r['A']:+.3f} [{r['ci68'][0]}, {r['ci68'][1]}]  dchi2(0) {r['D_A0']:7.3f} dchi2(1) {r['D_A1']:7.3f}  q0 {r['q0']:+.4f}"
            f"  today {r['D_today']:6.3f}  never {r['D_never']:8.3f} -> {w2(r['q0'], r['D_today'])}; {w3(r['D_never'])}")
    log(f"  J2 = {first}, {sec};  J3 = {res['words']['J3']['first']}" + ("" if j_ok else "  [NOT EVALUABLE]"))

    # E2, E3
    E = J("E")["E"]; y = E["young"]; first = w2(y["base"]["q0"], y["D_today"])
    fk = {"blue": w2(E["blue"]["base"]["q0"], E["blue"]["D_today"]), "log_s_ge_-10": w2(E["ls10"]["base"]["q0"], E["ls10"]["D_today"])}
    sec, _ = second(first, fk)
    res["words"]["E2"] = dict(first=first, second=sec, forks=fk, evaluable=se_ok)
    res["words"]["E3"] = dict(first=w3(y["D_never"]), forks={k: w3(E[s]["D_never"]) for k, s in (("blue", "blue"), ("log_s_ge_-10", "ls10"))}, evaluable=se_ok)
    log("\nPart E (BAO + the supernova subsample; no age term):")
    for k, r in E.items():
        bb = r["base"]
        log(f"  {k:12s} n {r['n_sn']:4d} ({r['n_des']} DES)  Om {bb['Om']:.4f} w0 {bb['w0']:+.4f} wa {bb['wa']:+.4f} q0 {bb['q0']:+.4f} edge {bb['edge']}"
            f"  today {r['D_today']:6.3f}  never {r['D_never']:8.3f} -> {r['word_today']}; {r['word_ever']}")
    log(f"  E2 = {first}, {sec};  E3 = {res['words']['E3']['first']}" + ("" if se_ok else "  [NOT EVALUABLE]"))

    log("\nWORDS")
    for k, v in res["words"].items():
        log(f"  {k}: {v['first']}" + (f", {v['second']}" if "second" in v else "") + ("" if v["evaluable"] else "  [NOT EVALUABLE]"))
    res["numbers"] = dict(D2=D["D2"]["primary"], U=D["U"]["primary"], reported=D["reported"], S_full=S["full"]["summary"],
                          J_primary=pj, K2=K2, K4=K4, K1=K1, KM={k: KM[k] for k in ("i", "ii")} | dict(iii_worst=KM["iii"]["worst"]))
    with open(os.path.join(HERE, "agb3r_results.json"), "w") as fh: json.dump(res, fh, indent=1, default=float)
    log("\nwrote agb3r_results.json")


if __name__ == "__main__":
    main()
