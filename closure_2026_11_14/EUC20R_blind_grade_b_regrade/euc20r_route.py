#!/usr/bin/env python3
"""EUC20R route driver: one source script, one mode, one fresh process (READING.md section 2).

  python3 -I -B euc20r_route.py --lane euc8|euc5a1|lnj1 --mode f1|primary|F1a|F1b|invert

- euc8, euc5a1 (wrapped loader): EUC1's euc1.py is imported as module `euc1`; its `load` is wrapped so that each row's
  `lm` is shifted by the mode (errors untouched); the source script is imported from its own folder, given a
  write-redirecting `open`, and its unmodified `main()` is called with --data-dir.
- lnj1 (one substitution): its source text with exactly one occurrence of the mass-parsing expression replaced, compiled
  under its own path and executed with the write-redirecting `open` in its globals.
Every write goes to runs/<mode>/<lane>/.  Nothing is written into a source folder.
kappa = 1/2 FITTED; not theory closed.  Adopts nothing.
"""
import argparse, builtins, json, os, sys, time
sys.dont_write_bytecode = True
for _v in ("EUC1_MUTATE", "EUC4_MUTATE", "EUC5_MUTATE", "EUC6_MUTATE", "EUC8_MUTATE"):
    os.environ.pop(_v, None)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import euc20r_common as C

TARGET = 'fl(r["eclipse_log_survived_mass_med"])'
REPL = '(fl(r["eclipse_log_survived_mass_med"]) + __EUC20R_DLM__(r["unique_identifier"], r["eclipse_effective_radius"], r["eclipse_sersic_index"]))'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True, choices=("euc8", "euc5a1", "lnj1"))
    ap.add_argument("--mode", required=True, choices=C.MODES)
    a = ap.parse_args()
    outdir = os.path.join(HERE, "runs", a.mode, a.lane)
    os.makedirs(outdir, exist_ok=True)
    sh = C.Shifter(a.mode)
    wlog = []
    ropen = C.redirecting_open(outdir, wlog)
    meta = dict(lane=a.lane, mode=a.mode, re_scale=sh.scale, mask_tables=sh.info, writes=wlog)
    t0 = time.time()
    code = 0
    if a.lane in ("euc8", "euc5a1"):
        E = C.euc1()
        orig = E.load
        def wrapped(data_dir):
            rows, nobj = orig(data_dir)
            for r in rows:
                d = sh.dlm(r["id"], r["te"], r["n"])
                if d != 0.0:
                    r["lm"] = r["lm"] + d
            return rows, nobj
        E.load = wrapped
        src_dir = C.DIRS["EUC8"] if a.lane == "euc8" else C.DIRS["EUC5"]
        sys.path.insert(0, src_dir)
        mod = __import__("euc8" if a.lane == "euc8" else "euc5_a1")
        meta["source"] = C.rel(mod.__file__)
        meta["loader_wrapped"] = bool(mod.E is E and mod.D.E is E)
        mod.open = ropen
        os.chdir(C.REPO)
        sys.argv = [os.path.basename(mod.__file__), "--data-dir", C.rel(C.DATA)]
        try:
            mod.main()
        except SystemExit as ex:
            code = ex.code if isinstance(ex.code, int) else (0 if ex.code is None else 9)
    else:
        path = os.path.join(C.DIRS["LNJ1"], "lnj1.py")
        src = builtins.open(path, encoding="utf-8").read()
        cnt = src.count(TARGET)
        meta["substitution_count"] = cnt
        if cnt != 1:
            raise SystemExit("substitution target found %d times, not exactly once" % cnt)
        src2 = src.replace(TARGET, REPL)
        g = {"__name__": "__main__", "__file__": path, "__builtins__": builtins, "open": ropen,
             "__EUC20R_DLM__": sh.dlm}
        meta["source"] = C.rel(path)
        try:
            exec(compile(src2, path, "exec"), g)
        except SystemExit as ex:
            code = ex.code if isinstance(ex.code, int) else (0 if ex.code is None else 9)
    meta.update(exit_code=code, seconds=round(time.time() - t0, 1), lenses_shifted=len(sh.applied),
                lenses_without_mask_seen=len(sh.nomask), lenses_bad_share=len(sh.badf),
                nomask_ids=sorted(sh.nomask), badf_ids=sorted(sh.badf))
    with builtins.open(os.path.join(outdir, "driver.json"), "w") as f:
        json.dump(meta, f, indent=1)
    sys.exit(0)


if __name__ == "__main__":
    main()
