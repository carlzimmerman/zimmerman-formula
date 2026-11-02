#!/usr/bin/env python3
"""FR1 (FROZEN_CRITERIA.md): 15 keys and X-COP with the measured line map. Drives zn3_grade.py --worker as OP2's ng 80 driver; other lanes read only. Each job cached, so a killed run resumes.
    python3 fr1.py   kappa = 1/2 FITTED, unused; not theory closed."""
import ast, json, math, os, re, subprocess, sys, tempfile, shutil
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); Z3 = os.path.join(RB, "ZN3_native_shape_at_1e15"); ZG = os.path.join(Z3, "zn3_grade.py"); CE1 = os.path.join(RB, "CE1_converged_eta_grade"); SH = os.path.join(RB, "ZN4_cluster_resolution", "zn4_shapes.json"); SLOPE = "2.7774425603108597"; CC = os.path.join(HERE, "cache_jobs"); os.makedirs(CC, exist_ok=True)
ZT = open(os.path.join(RB, "ZN1_zooms_to_z0", "zn1_grade.py")).read(); GAS = ast.literal_eval(re.search(r'GAS = ("""(?:.*?)""")', ZT, re.S).group(1)); LN = json.load(open(os.path.join(HERE, "fr1_line.json")))
DEF = open(os.path.join(HERE, "fr1_def.py")).read()
XP = f'''sub('def zn1_fn(foot, tag, pp, z):', {DEF!r} + 'def zn1_fn(foot, tag, pp, z):')
sub('Mfs, Rfs, thr = zn1_m200_fs(pp["Mb"], z)', '_FRH.update(tag=tag, foot=foot); Mfs, Rfs, thr = zn1_m200_fs(pp["Mb"], z)')
sub('fc = NAT_RRAT / (1 + NAT_RRAT); ZN1_STAT["cells"] += 1', 'fc = (NAT_RRAT / (1 + NAT_RRAT) if _FRL["mode"] == "one" else 1 - _FRH["F"] / (1 + NAT_RRAT)); ZN1_STAT["cells"] += 1')
sub('Mh = zn1_fn(foot, tag, pp, NX["CL"][int(i)]["z"])(RM)', '_FRI["i"] = int(i); _zf = zn1_fn(foot, tag, pp, NX["CL"][int(i)]["z"]); Mh = _zf(RM); _fr_rec(foot, tag, pp, NX["CL"][int(i)]["z"], _zf, *zn1_m200_fs(pp["Mb"], NX["CL"][int(i)]["z"])[:2]); _FRI["i"] = None')
'''
def run(lab, fs, gas, line, slope=SLOPE):
    c = os.path.join(CC, re.sub(r"\W", "_", lab) + ".json")
    if os.path.exists(c) and "_old" not in c: return lab, json.load(open(c))
    WD = tempfile.mkdtemp(); o = os.path.join(WD, "o.json"); xf = os.path.join(WD, "x.py"); open(xf, "w").write(GAS.replace("0.111", gas) + XP); dp = os.path.join(WD, "dump.json")
    env = dict(os.environ, FC1_MODE="cold", X74_CF=os.path.join(CE1, f"CE1_med_fs{fs}_cf_table.json"), X73_FSTAR=fs, X73_SLOPE=slope, XH1_OUT=o, XH1_SMULT="1", MA1_MODE="m200", MA1_MULT="1", MA1_WD=WD, ZN1_MODE="fs", ZN1_RX="1.0", ZN1_SNAP="nearest", ZN1_SHAPES=SH, ZN1_XFILE=xf, FR1_LINE=json.dumps(line), FR1_DUMP=dp, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1"); env.pop("XH1_K0_REF", None)
    p = subprocess.run(["nice", "-n", "15", sys.executable, ZG, "--worker"], cwd=WD, env=env, capture_output=True, text=True)
    if not os.path.exists(o): raise SystemExit(f"NOT DECIDED {lab} exit {p.returncode}: {p.stdout[-300:]} {p.stderr[-1800:]}")
    R = json.load(open(o)); R = dict(grader=dict(canonical=dict(clusters=dict(cells=R["grader"]["canonical"]["clusters"]["cells"]))), M_outer={k: v for k, v in R["M_outer"].items() if k.startswith("canonical")}, footings=dict(canonical=R["footings"]["canonical"]), zn1=R["zn1"])
    if os.path.exists(dp):
        D = json.load(open(dp)); R["dump"] = {k: v for k, v in D.items() if k.startswith("canonical")}
    json.dump(R, open(c, "w")); shutil.rmtree(WD, ignore_errors=True); return lab, R
def L(k, **w): q = LN[k]; return dict(mode="line", x="M", a=q["a"], b=q["b"], piv=q["piv"], **w)
H = L("H"); s = (LN["H"]["cov"], LN["H"]["sa"])
def se(x): c = LN["H"]["cov"]; d = x - 14.5; return math.sqrt(c[0][0] + 2 * d * c[0][1] + d * d * c[1][1])
ONE = dict(mode="one")
J = []
for fs in ("0.034", "0.0615"):
    J += [(f"K1 one {fs}", fs, "0.005", ONE), (f"H {fs}", fs, "0.005", H), (f"MUT flip {fs}", fs, "0.005", dict(H, b=-H["b"]))]
    J += [(f"W {fs}", fs, "0.005", L("W")), (f"Hplusg {fs}", fs, "0.005", L("Hg")), (f"HgasX {fs}", fs, "0.005", dict(L("HG"), x="G")), (f"H noL20 {fs}", fs, "0.005", L("H_without_L20")), (f"H noL15S09 {fs}", fs, "0.005", L("H_without_L15_S09")), (f"H +0.111 {fs}", fs, "0.111", H)]
    J += [(f"Hp1s {fs}", fs, "0.005", dict(H, a=H["a"] + se(14.2))), (f"Hm1s {fs}", fs, "0.005", dict(H, a=H["a"] - se(14.2)))]
J += [("post carry XCOP 0.034", "0.034", "0.005", dict(H, carry=0.031)), ("post carry XCOP g 0.034", "0.034", "0.005", dict(L("Hg"), carry=0.031)), ("post s2676 0.034", "0.034", "0.005", H, "2.676"), ("post s3071 0.034", "0.034", "0.005", H, "3.071")]
only = sys.argv[1:]
if only: J = [j for j in J if any(j[0].startswith(o) for o in only)]
with ThreadPoolExecutor(2) as ex:
    for lab, R in ex.map(lambda j: run(*j), J): print("done", lab, flush=True)
