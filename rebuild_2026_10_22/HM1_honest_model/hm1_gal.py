#!/usr/bin/env python3
"""HM1 galaxies (FROZEN_CRITERIA.md): SP3's native cells through OP3's worker, own cache, other lanes read only. kappa = 1/2 FITTED, unused; not theory closed. python3 hm1_gal.py"""
import json, os, re, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SP3 = os.path.join(RB, "SP3_starting_point"); ZD = os.path.join(RB, "ZN2_native_profile_sparc_groups"); OP3 = os.path.join(RB, "OP3_contraction_on_native"); CE1 = os.path.join(RB, "CE1_converged_eta_grade"); SLOPE = "2.7774425603108597"; CD = os.path.join(HERE, "cache_gal"); os.makedirs(CD, exist_ok=True)
OPX = os.path.join(CD, "opx_gn.py"); _t = open(os.path.join(OP3, "op3_x.py")).read(); _a = 'contract(rg, Mbg, M0, OP3_MB * Mtot_ / float(M0[-1]))'; assert _t.count(_a) == 1; open(OPX, "w").write(_t.replace(_a, 'contract(rg, Mbg, M0, OP3_MB * Mtot_ / float(M0[-1]), gnedin=(0.85, 0.8, R2))'))
def cell(tag, mapn, fq, gn=False, shapes=None):
    o = os.path.join(CD, f"{tag}.json")
    if os.path.exists(o): return json.load(open(o))
    WD = tempfile.mkdtemp(dir=CD); t = o + ".tmp"
    env = dict(os.environ, FC1_MODE="cold", X74_CF=os.path.join(CE1, "CE1_med_fs0.034_cf_table.json"), X73_FSTAR="0.034", X73_SLOPE=SLOPE, ZN2_OUT=t, ZN2_WD=WD, ZN2_SHAPES=shapes or os.path.join(ZD, "zn2_low_shapes.json"), ZN2_MAP=mapn, ZN2_RX="1", ZN2_K1="", ZN2_TAGS="1e10,1e11,1e12,1e13,1e14", OP3_X=os.path.join(HERE, "hm1_spx.py"), HM1_SP3X=os.path.join(SP3, "sp3_x.py"), SP3_OP3X=OPX if gn else os.path.join(OP3, "op3_x.py"), OP3_FQ=str(fq), OP3_MB="1", SP3_MAP="EM1", SP3_DELTA="0.0", SP3_TABLES=os.path.join(SP3, "sp3_tables.json"), PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    if gn: env["HM1_GN"] = "1"
    p = subprocess.run(["nice", "-n", "15", sys.executable, os.path.join(OP3, "op3.py"), "--worker"], cwd=WD, env=env, capture_output=True, text=True); shutil.rmtree(WD, ignore_errors=True)
    if not os.path.exists(t): raise SystemExit(f"NOT DECIDED {tag}: exit {p.returncode}: {p.stdout[-600:]} {p.stderr[-1800:]}")
    os.replace(t, o); return json.load(open(o))
if __name__ == "__main__":
    SH80 = os.path.join(HERE, "cache_gal", "shapes_ng80proxy.json")
    C = [("tot_off", "tot", 0), ("tot_fq", "tot", 0.872), ("fc1_off", "fc1", 0), ("fc1_fq", "fc1", 0.872), ("tot_blum", "tot", 1.0), ("tot_MUTATE05", "tot", 0.436)]
    for tag, m, f in C: r = cell(tag, m, f); print(tag, {t: round(r["sparc"][t]["U_median"], 3) for t in r["sparc"]}, r["sp3"]["tilt"], r["sp3"]["lt"], r["groups"]["Z"], {t: r["sp3"]["ltE"][t]["IC 1613"] for t in r["sp3"]["ltE"]}, flush=True)
    r = cell("tot_gn", "tot", 1.0, gn=True); print("tot_gn", {t: round(r["sparc"][t]["U_median"], 3) for t in r["sparc"]}, r["sp3"]["tilt"], r["sp3"]["lt"], flush=True)
    if os.path.exists(SH80): r = cell("tot_fq_ng80proxy", "tot", 0.872, shapes=SH80); print("ng80 proxy", {t: round(r["sparc"][t]["U_median"], 3) for t in r["sparc"]}, r["sp3"]["tilt"], r["sp3"]["lt"], r["groups"]["Z"], flush=True)
