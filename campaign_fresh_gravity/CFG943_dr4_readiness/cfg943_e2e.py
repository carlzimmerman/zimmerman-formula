#!/usr/bin/env python3
"""CFG943: the release-day command chain end to end on MOCK catalogues (FROZEN_CRITERIA.md section 3, last paragraph).

For classes A0, B1, B3, C (one 30,000-pair MOCK catalogue each):
  1. write the registered --catalog CSV (sep_kAU, v_perp_kms, M1_msun, M2_msun, d_pc) and the cfg816_r pair table (to a scratch dir;
     their sha256 are recorded here, the files are not committed);
  2. K2: the frozen ingest_csv v-tilde equals the in-memory v-tilde (relative difference < 1e-12);
  3. the frozen pipeline: python3 -B cfg943_frozen_harness.py --catalog CSV  (log kept in this directory);
  4. python3 -B dr4_ready_1/amdt14_distances.py --log LOG and dr4_ready_1/arm_c_rows.py --log LOG (they only print);
  5. CFG825's read_table + score (B = 2000) on the pair table (never its --dr4/--dr3 paths).
Every number is a MOCK.  python3 -B cfg943_e2e.py [SCRATCH_DIR]  -> e2e_<class>.out, cfg943_e2e_results.json
"""
import sys
sys.dont_write_bytecode = True
import os, json, hashlib, subprocess, re
import numpy as np
import cfg943_common as C
from cfg943_common import W, R825

SCR = sys.argv[1] if len(sys.argv) > 1 else "/tmp"
CLASSES = [("A0_NEWTON", 0), ("B1_MOND_BENCH", 2), ("B3_ARM_A_FLOOR", 4), ("C_CFG740", 5)]
ENV = dict(os.environ, OMP_NUM_THREADS="1")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run(cmd, log=None):
    r = subprocess.run(cmd, capture_output=True, text=True, env=ENV, cwd=C.HERE)
    if log:
        open(log, "w").write(r.stdout.replace(SCR.rstrip("/") + "/", "<scratch>/"))     # no local paths in committed logs
    return r.returncode, r.stdout, r.stderr


def main():
    h0 = C.frozen_hashes()
    allres = dict(lane="CFG943", mode="e2e", classes={})
    for cls, ci in CLASSES:
        L = [f"CFG943 end-to-end release-day chain on a MOCK catalogue: {cls} (N = 30,000). MOCK numbers only."]
        rng = np.random.default_rng([943, 900 + ci])
        c = C.make_catalogue(30000, rng, cls)
        cat_csv = os.path.join(SCR, f"mock_{cls}_catalog.csv")
        pair_csv = os.path.join(SCR, f"mock_{cls}_pairs.csv")
        t = C.pair_table(c)
        with open(cat_csv, "w") as f:
            f.write("sep_kAU,v_perp_kms,M1_msun,M2_msun,d_pc\n")
            for i in range(len(c["vt"])):
                f.write(f"{t['sep_kAU'][i]!r},{t['v_perp_kms'][i]!r},{t['M1_msun'][i]!r},{t['M2_msun'][i]!r},{t['d_pc'][i]!r}\n")
        cols = list(t.keys())
        with open(pair_csv, "w") as f:
            f.write(",".join(cols) + "\n")
            for i in range(len(c["vt"])):
                f.write(",".join("" if np.isnan(t[k][i]) else repr(float(t[k][i])) for k in cols) + "\n")
        gN, vt_reg, _ = W.ingest_csv(cat_csv)
        k2 = float(np.max(np.abs(vt_reg / c["vt"] - 1)))
        L.append(f"[step 1] wrote {os.path.basename(cat_csv)} sha256 {sha(cat_csv)[:16]} and {os.path.basename(pair_csv)} sha256 {sha(pair_csv)[:16]} (scratch, not committed)")
        L.append(f"[step 2] K2 frozen ingest_csv v-tilde vs in-memory: max relative difference {k2:.2e} -> {'PASS' if k2 < 1e-12 else 'FAIL'}")
        log = os.path.join(C.HERE, f"e2e_{cls}_pipeline.log")
        rc, out, err = run([sys.executable, "-B", os.path.join(C.HERE, "cfg943_frozen_harness.py"), "--catalog", cat_csv], log)
        st = re.search(r"PIPELINE SELF-TEST: (\w+)", out)
        L.append(f"[step 3] frozen pipeline (harness): exit {rc}; self-test {st.group(1) if st else 'NOT PRINTED'}; {err.strip().splitlines()[-1] if err.strip() else ''}")
        L += ["    " + x for x in out.splitlines() if x.lstrip().startswith(("catalog [", "[7(e)]", "[gated] catalog", "[aniso] catalog"))]
        rc14, o14, e14 = run([sys.executable, "-B", os.path.join(C.DR4R, "amdt14_distances.py"), "--log", log])
        rcC, oC, eC = run([sys.executable, "-B", os.path.join(C.DR4R, "arm_c_rows.py"), "--log", log])
        L.append(f"[step 4] amdt14_distances.py exit {rc14}:"); L += ["    " + x for x in o14.strip().splitlines()]
        L.append(f"[step 4] arm_c_rows.py exit {rcC}:"); L += ["    " + x for x in oC.strip().splitlines()]
        tt = R825.read_table(pair_csv)
        res, final, txt = C.r_score(tt, np.random.default_rng([943, 950 + ci]), 2000, f"MOCK {cls} pair table (CSV path)")
        L.append("[step 5] CFG825 read_table + score (B = 2000):"); L += ["    " + x for x in txt.strip().splitlines()]
        fits = {m.group(1): (float(m.group(2)), float(m.group(3))) for m in
                re.finditer(r"catalog \[a0 (canonical|alt footing)\]\s+gamma_inf = ([0-9.]+) \+- ([0-9.]+)", out)}
        allres["classes"][cls] = dict(cat_sha256=sha(cat_csv), pairs_sha256=sha(pair_csv), K2_max_rel=k2, K2=k2 < 1e-12,
                                      pipeline_exit=rc, self_test=st.group(1) if st else None, harness_stderr=err.strip()[-300:],
                                      fits=fits, amdt14_exit=rc14, amdt14=o14.strip().splitlines(), arm_c_exit=rcC, arm_c=oC.strip().splitlines(),
                                      R_primary=res["primary"], R_label=final)
        open(os.path.join(C.HERE, f"e2e_{cls}.out"), "w").write("\n".join(L) + "\n")
        print("\n".join(L), flush=True)
    h1 = C.frozen_hashes()
    allres["K4"] = (h0 == h1) and not h1["DR4_SLOT_EXISTS"]
    allres["chain_ok"] = all(v["K2"] and v["amdt14_exit"] == 0 and v["arm_c_exit"] == 0 and v["pipeline_exit"] in (0, 1) and len(v["fits"]) == 2
                             for v in allres["classes"].values())
    print(f"K4 frozen files unchanged and CFG825 DR4 slot absent: {allres['K4']}; chain ran end to end for every class: {allres['chain_ok']}")
    json.dump(allres, open(os.path.join(C.HERE, "cfg943_e2e_results.json"), "w"), indent=1, default=float)
    return 0 if (allres["K4"] and allres["chain_ok"]) else 2


if __name__ == "__main__":
    sys.exit(main())
