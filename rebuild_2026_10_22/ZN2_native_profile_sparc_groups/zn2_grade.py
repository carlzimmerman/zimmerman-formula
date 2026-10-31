#!/usr/bin/env python3
"""ZN2_native_profile_sparc_groups (FROZEN_CRITERIA.md): ZN1's native z = 0 shape on SPARC and the groups.
    python3 zn2_grade.py --k1          # K1: FC1's own rule as a table; reads no ZN1 snapshot
    python3 zn2_grade.py [--mutate]    # needs ../ZN1_zooms_to_z0/zn1_shapes.json
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, re, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SLOPE = "2.7774425603108597"; CE1 = os.path.join(RB, "CE1_converged_eta_grade"); FC1 = os.path.join(RB, "FC1_cold_share_native_eta"); SHAPES = os.path.join(RB, "ZN1_zooms_to_z0", "zn1_shapes.json")
if "--worker" in sys.argv:
    WD = os.environ["ZN2_WD"]; X74F = os.path.join(RB, "X74_all_measured_native_cf", "x74_native_cf.py"); TX = open(X74F).read()
    INJ = re.search(r"INJ = r'''(.*?)'''", open(os.path.join(FC1, "fc1_x74.py")).read(), re.S).group(1)
    L = 'HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)'; assert TX.count(L) == 1; TX = TX.replace(L, f"HERE = {WD!r}; REB = {RB!r}")
    MY = f"""
sub({L!r}, {('HERE = %r; REB = %r' % (WD, RB))!r})
_d = open({os.path.join(HERE, 'zn2_def.py')!r}).read()
sub('def sparc(f, tag, rule=True):', _d + 'def sparc(f, tag, rule=True):')
sub('        r0 = solve_r0(M200 * MSUNE, R200, s); Mh = math.pi * s * r0 ** 2 * B(q["Rm"] / r0)\\n', '''        if ZN2["on"] and rule and ETA_USE["v"] == ETA: Mh = zn2_mass(M200 * MSUNE, rc, q["Rm"], q)
        else: r0 = solve_r0(M200 * MSUNE, R200, s); Mh = math.pi * s * r0 ** 2 * B(q["Rm"] / r0)\\n''')
sub('        r0 = solve_r0(M200, R200, sc); rr = XG * a\\n        Mh = math.pi * sc * r0 ** 2 * B(np.minimum(rr, R200) / r0); gN = gN + Mh / Mb / XG ** 2', '''        rr = XG * a
        if ZN2["on"] and ETA_USE["v"] == ETA: Mh = zn2_mass(M200, rc, rr, None)
        else: r0 = solve_r0(M200, R200, sc); Mh = math.pi * sc * r0 ** 2 * B(np.minimum(rr, R200) / r0)
        gN = gN + Mh / Mb / XG ** 2''')
sub("sys.exit(0 if (n == len(checks) and x74ok) else 1)", open({os.path.join(HERE, 'zn2_tail.py')!r}).read())
"""
    A = "sys.argv = [SRC]\n"; assert TX.count(A) == 1; TX = TX.replace(A, INJ + MY + A); sys.argv = [X74F]
    exec(compile(TX, X74F, "exec"), {"__file__": os.path.join(WD, "x74_native_cf.py"), "__name__": "__main__"})
TD = tempfile.mkdtemp(); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def run(fs="0.034", shapes=SHAPES, mapn="tot", rx=1.0, k1=False):
    WD = os.path.join(TD, f"{mapn}_{rx:g}_{int(k1)}"); os.makedirs(WD); o = os.path.join(WD, "o.json"); env = dict(os.environ, FC1_MODE="cold", X74_CF=os.path.join(CE1, f"CE1_med_fs{fs}_cf_table.json"), X73_FSTAR=fs, X73_SLOPE=SLOPE, ZN2_OUT=o, ZN2_WD=WD, ZN2_SHAPES=shapes, ZN2_MAP=mapn, ZN2_RX=str(rx), ZN2_K1="1" if k1 else "", PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    p = subprocess.run(["nice", "-n", "5", sys.executable, os.path.abspath(__file__), "--worker"], cwd=WD, env=env, capture_output=True, text=True)
    if not os.path.exists(o): raise SystemExit(f"NOT DECIDED: {mapn} wrote no result (exit {p.returncode}): {p.stdout[-400:]} {p.stderr[-1500:]}")
    r = json.load(open(o)); shutil.rmtree(WD, ignore_errors=True); return r
def ln(lab, R):
    s = R["sparc"]; g = R["groups"]; P(f"  {lab}: " + "; ".join(f"SPARC [{t}] rms {s[t]['rms']:.4f}, median U {s[t]['U_median']:.2f}, line {'PASS' if s[t]['line'] else 'FAIL'}" for t in s) + f"; groups mean {g['mean']:+.4f} Z {g['Z']:+.2f} {g['verdict']}; clamped below the 1e12 tag {R['stat']['below']} of {R['stat']['n']} galaxy evaluations"); 
    if R.get("bins"): P("     by V_flat, U / dV at U 0.50: " + "; ".join(f"{k} (n {v['n']}) {v['U']:.2f}/{v['dV']:+.1f}" for k, v in R["bins"].items()))
    if R.get("above"): P(f"     galaxies above the 1e12 tag only: n {R['above']['n']}, rms {R['above']['rms']:.4f}, median U {R['above']['U_median']:.2f}")
def cls(R):
    s = R["sparc"]; f = [t for t in s if not s[t]["line"]]; gp = R["groups"]["PASS"]
    if not f and gp: return "NATIVE PROFILE PASSES SPARC AND GROUPS"
    if f:
        t = f[0]; d = "U low" if s[t]["U_median"] < 0.50 else "U high" if s[t]["U_median"] > 0.80 else "rms"
    return f"SPARC FAILS ({d})" if f and gp else "GROUPS FAIL" if not f else f"BOTH FAIL (SPARC {d})"
if __name__ == "__main__":
    if "--k1" in sys.argv:
        R = run(mapn="fc1", k1=True); k = R["k1"]; ok = k["rms"] <= 2e-3 and k["U"] <= 0.01 and k["gZ"] <= 0.05; P(f"K1 FC1's rule as a table through this path, canonical, background A: rms {k['rms']:.1e} (2e-3), median U {k['U']:.3f} (0.01), group Z {k['gZ']:.3f} (0.05): {'PASS' if ok else 'FAIL'}"); open(os.path.join(HERE, "zn2_k1.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
    MUT = "--mutate" in sys.argv; TAG = "zn2_MUTATE" if MUT else "zn2"; P(f"ZN2 {TAG}: native z = 0 profile on SPARC and groups; kappa = 1/2 FITTED; not theory closed")
    if MUT:
        b = run(); m = run(rx=1.5); ln("base", b); ln("shape's r x 1.5", m); d = m["sparc"]["A_c2b_refit"]["U_median"] - b["sparc"]["A_c2b_refit"]["U_median"]; ok = abs(d) >= 0.02; P(f"MUTATE moves median U by {d:+.2f}: {'BITES' if ok else 'INSENSITIVE, lane UNDECIDED'}"); open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
    with ThreadPoolExecutor(2) as ex: A, B = ex.map(lambda mp: run(mapn=mp), ("tot", "fc1"))
    ln("frozen mapping (M_t = M200/f_c, R_t)", A); ln("FC1's normalisation (M200, R200)", B); V, V2 = cls(A), cls(B); tags = (" [LOW-MASS CLAMPED]" if A["stat"]["below"] else "") + ("" if V == V2 else " [NORMALISATION-DEPENDENT]"); P(f"VERDICT: {V}{tags}. FC1's normalisation: {V2}.")
    json.dump(dict(verdict=V, tags=tags, frozen=A, fc1_norm=B), open(os.path.join(HERE, "zn2_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "zn2.out"), "w").write("\n".join(OUT) + "\n")
