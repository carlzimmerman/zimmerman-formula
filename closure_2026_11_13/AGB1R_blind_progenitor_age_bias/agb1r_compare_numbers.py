"""AGB1R comparison helper (written after RESULT_BLIND.md was committed and AGB1's README was opened).
Number-by-number comparison of this build's outputs with AGB1's committed outputs. Flags chi2-type differences
> 0.005 and parameter differences > 0.0015 (the README's printed precision is 0.01 in dchi2 and 0.001 in parameters).
Writes agb1r_compare_numbers.out / .json."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
OTHER = os.path.join(HERE, "..", "AGB1_progenitor_age_bias")
J = lambda d, n: json.load(open(os.path.join(d, n)))
rows = []; flags = []
def cmp(label, mine, theirs, tol):
    if mine is None or theirs is None:
        rows.append(f"{label:58s} mine {mine}  AGB1 {theirs}"); return
    d = mine - theirs
    flag = abs(d) > tol
    rows.append(f"{label:58s} mine {mine:+12.5f}  AGB1 {theirs:+12.5f}  diff {d:+.5f}{'   <-- beyond tolerance' if flag else ''}")
    if flag: flags.append(dict(label=label, mine=mine, agb1=theirs, diff=d))

CHI, PAR = 0.005, 0.0015
for part, mypre, thpre, samples in (("A", "agb1r_A_", "agb1_A_", ["full", "des_only", "rand197", "bao_overlap"]),
                                    ("C", "agb1r_C_", "agb1_C_", ["full", "des_only"])):
    for s in samples:
        m = J(HERE, f"{mypre}{s}.json"); t = J(OTHER, f"{thpre}{s}.json"); ts = t["summary"]
        p = f"{part} {s}"
        cmp(f"{p} A_free", m["A_free"]["A"], ts["A_free"], PAR)
        cmp(f"{p} chi2_free", m["A_free"]["chi2"], ts["chi2_free"], CHI)
        cmp(f"{p} dchi2(A=0)", m["dchi2_A0"], ts["D_A0"], CHI)
        cmp(f"{p} dchi2(A=1)", m["dchi2_A1"], ts["D_A1"], CHI)
        for lev, mk, tk in ((1, "interval_1", "ci68"), (4, "interval_4", "ci95")):
            for i, end in enumerate(("lo", "hi")):
                cmp(f"{p} dchi2={lev} interval {end}", m[mk][i], ts[tk][i], PAR)
        # profile grid
        tp = t["profile"]; mp = m["profile"]
        dmax = 0.0; worst = None
        for a, rec in tp.items():
            key = f"{float(a):.1f}" if part == "A" else f"{float(a):.2f}"
            mk = next((k for k in mp if abs(float(k) - float(a)) < 1e-9), None)
            if mk is None: continue
            d = mp[mk]["chi2"] - rec["chi2"]
            if abs(d) > abs(dmax): dmax, worst = d, a
        rows.append(f"{p} profile: largest chi2 difference over the grid {dmax:+.5f} at A {worst}")
        if "forks" in m and "forks" in t:
            for lab in ("A0", "A1", "Afree"):
                mf, tf = m["forks"][lab], t["forks"][lab]
                for k in ("Om", "w0", "wa", "q0"):
                    cmp(f"{p} {lab} best {k}", mf["best"][k], tf["base"][k], PAR)
                cmp(f"{p} {lab} best chi2", mf["best"]["chi2"], tf["base"]["chi2"], CHI)
                cmp(f"{p} {lab} q0=0 chi2", mf["q0zero"]["chi2"], tf["today"]["chi2"], CHI)
                cmp(f"{p} {lab} never chi2", mf["never"]["chi2"], tf["never"]["chi2"], CHI)
                cmp(f"{p} {lab} dchi2_today", mf["dchi2_today"], tf["D_today"], CHI)
                cmp(f"{p} {lab} dchi2_never", mf["dchi2_never"], tf["D_never"], CHI)
for s in ("full", "des_only"):
    m = J(HERE, f"agb1r_A_tmplW_{s}.json"); t = J(OTHER, f"agb1_W_{s}.json"); ts = t["summary"]
    cmp(f"T_W {s} A_free", m["A_free"]["A"], ts["A_free"], PAR)
    cmp(f"T_W {s} chi2_free", m["A_free"]["chi2"], ts["chi2_free"], CHI)
    cmp(f"T_W {s} dchi2(A_W=0)", m["dchi2_A0"], ts["D_A0"], CHI)
    cmp(f"T_W {s} dchi2(A_W=0.23)", m["dchi2_AW_023"], ts["D_A023"], CHI)
    cmp(f"T_W {s} dchi2(A_W=1)", m["dchi2_A1"], ts["D_A1"], CHI)
    cmp(f"T_W {s} dchi2=1 lower", m["interval_1"][0], ts["ci68"][0], PAR)
m = J(HERE, "agb1r_C_k5.json"); t = J(OTHER, "agb1_C_K5.json")
cmp("K5 dchi2(w0wa - LCDM)", m["dchi2"], t["dchi2"], CHI)
open(os.path.join(HERE, "agb1r_compare_numbers.out"), "w").write("\n".join(rows) + "\n")
json.dump(dict(flags=flags), open(os.path.join(HERE, "agb1r_compare_numbers.json"), "w"), indent=1)
print("\n".join(r for r in rows if "<--" in r or "profile" in r))
print(f"{len(flags)} differences beyond tolerance out of {sum(1 for r in rows if 'mine' in r)} compared numbers")
