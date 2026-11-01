#!/usr/bin/env python3
"""PZ1 read-out (FROZEN_CRITERIA.md 81c8d83d90): LC1's reader, imported and not edited, on PZ1's runs; same-seed pairs with LC1; K4, K6, MUTATE; the frozen labels.
    python3 pz1_read.py          # all finished runs
    python3 pz1_read.py --k4     # reader baseline on LC1's own runs only
kappa = 1/2 FITTED, unused; not theory closed."""
import sys; sys.dont_write_bytecode = True
import glob, importlib.util, json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); LC1 = os.path.join(REB, "LC1_live_contraction"); X48R = os.path.join(REB, "X48_native_cf_zoom", "runs"); RUNS = os.path.join(HERE, "runs")
_s = importlib.util.spec_from_file_location("lc1_read", os.path.join(LC1, "lc1_read.py")); R = importlib.util.module_from_spec(_s); _s.loader.exec_module(R)
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
LRES = json.load(open(os.path.join(LC1, "lc1_results.json")))["pairs"]; RDG = R.RDG; Rd = 3.565e-3
def k4():
    runs = sorted(glob.glob(os.path.join(LC1, "runs", "M1e12_s?_ng64"))); rows = R.read("0.00", runs); dm = 0.0
    for s, q in rows.items():
        o = LRES["0.00"][s]; dm = max(dm, *(abs(a - b) for a, b in zip(q["Q"], o["Q"])), abs(q["f_Q"] - o["f_Q"]), abs(q["R_live"] - o["R_live"]))
    ok = len(rows) == 9 and dm <= 1e-6; P(f"K4 imported reader on LC1's own nine runs against lc1_results.json, z = 0: {len(rows)} seeds, max |d| {dm:.1e}: {'PASS' if ok else 'FAIL'}"); return ok
def rho_of(meta, z): return meta["Mf"] / (4 / 3 * math.pi * meta["qM"] ** 3) * (1 + z) ** 3
def null_cmp(fa, fb, z):
    A, B = np.load(fa, allow_pickle=False), np.load(fb, allow_pickle=False); ma, mb = json.loads(str(A["meta"])), json.loads(str(B["meta"])); m = float(B["m"]); assert len(A["x"]) == len(B["x"])
    ra, rb = R.cr(A["x"], m), R.cr(B["x"], m); rr = RDG * Rd; Q = np.searchsorted(ra, rr) / np.searchsorted(rb, rr); rho = rho_of(mb, z); fa_, fb_ = R.S_fit(A["x"], m, rho, ma["eps"]), R.S_fit(B["x"], m, rho, ma["eps"]); return Q, fa_["S"] / fb_["S"], float(np.sqrt(((A["x"] - B["x"]) ** 2).sum(1)).max())
def read_zf(runs):
    rows = {}
    for d in runs:
        s = os.path.basename(d); fd, fn = os.path.join(d, "snap_zf.npz"), os.path.join(X48R, s, "snap_zf.npz")
        if not (os.path.exists(fd) and os.path.exists(fn)): continue
        A, B = np.load(fd, allow_pickle=False), np.load(fn, allow_pickle=False); ma = json.loads(str(A["meta"])); mb = json.loads(str(B["meta"])); rho = rho_of(mb, mb["zf"]); rows[s] = R.pair(A["x"], B["x"], float(B["m"]), ma["Md_now"], ma["lc1"]["Rd_kpc"] * 1e-3, ma["eps"], rho, mb["zf"])
    return rows
def boot(v, null, n=20000):
    v = np.asarray(v); rng = np.random.default_rng(1); M = np.median(v[rng.integers(0, len(v), (n, len(v)))], axis=1); lo, hi = np.percentile(M, [2.5, 97.5]); return float(lo), float(hi), bool(lo <= null <= hi)
def table(rows, zs):
    med = lambda k: np.median([q[k] for q in rows.values()], axis=0); Rl = [q["R_live"] for q in rows.values() if q["R_live"] is not None]; fq = [q["f_Q"] for q in rows.values()]; fg = [q["f_G"] for q in rows.values()]
    P(f"z {zs}: {len(rows)} pairs; M_d now, median {np.median([q['Md'] for q in rows.values()]):.3e}; r/R_d {RDG.tolist()}; softening x 3 at r/R_d {list(rows.values())[0]['x_conv']:.2f}")
    P("  Q live       " + " ".join(f"{q:.3f}" for q in med("Q"))); P("  Q Blumenthal " + " ".join(f"{q:.3f}" for q in med("QB"))); P("  Q Gnedin     " + " ".join(f"{q:.3f}" for q in med("QG")))
    P(f"  R_live {np.median(Rl):.3f} [{min(Rl):.3f}, {max(Rl):.3f}]; f_Q (Blumenthal) {np.median(fq):.3f} [{min(fq):.3f}, {max(fq):.3f}], f (Gnedin) {np.median(fg):.3f}; c_nfw no disc {np.median([q['c_nodisc'] for q in rows.values()]):.2f}, with disc {np.median([q['c_disc'] for q in rows.values()]):.2f}; by seed R_live " + " ".join(f"{x:.2f}" for x in Rl))
if __name__ == "__main__":
    P("PZ1 read-out: LC1's disc started at each seed's measured turnaround; gravity only; kappa = 1/2 FITTED, unused; not theory closed")
    good = R.selftest(); good &= k4()
    if "--k4" in sys.argv: sys.exit(0 if good else 1)
    if not good: sys.exit("reader checks failed: no reading")
    SEEDS = sorted(glob.glob(os.path.join(RUNS, "M1e12_s?_ng64"))); RES = {}
    ta = {}
    for d in SEEDS:
        f = os.path.join(d, "turnaround.json")
        if os.path.exists(f):
            T = json.load(open(f)); dn = os.path.join(d, "done.json"); J = json.load(open(dn)) if os.path.exists(dn) else {}; ta[os.path.basename(d)] = dict(t_ta=T["t_ta"], z_ta=T["z_ta"], t_ta_median=T["t_ta_median"], t_f=T["t_f"], frac_zf=(T["t_f"] - T["t_ta"]) / (13.78621266894681 - T["t_ta"]), jmax_kpc=J.get("jmax", float("nan")) * 1e3, n_jump_gt_Rd=len(J.get("jumps", [])))
    P("Turnaround by seed: seed, t_ta Gyr, z_ta, t_ta/t_f, median-radius t_ta, M_d(z_f)/M_d, largest centre jump kpc, jumps > R_d")
    for s, q in ta.items(): P(f"  {s.split('_')[1]} {q['t_ta']:.3f} {q['z_ta']:.3f} {q['t_ta'] / q['t_f']:.3f} {q['t_ta_median']:.3f} {q['frac_zf']:.3f} {q['jmax_kpc']:.2f} {q['n_jump_gt_Rd']}")
    rz = read_zf(SEEDS); RES["zf"] = rz
    if rz: table(rz, "z_f (no-disc partner X48's snap_zf; LC1 has no disc here)")
    for zs in ("0.50", "0.25", "0.00"):
        rows = R.read(zs, SEEDS); RES[zs] = rows
        if rows:
            table(rows, zs); P(f"  LC1 at this z: M_d now {np.median([q['Md'] for q in LRES[zs].values()]):.3e}, R_live {np.median([q['R_live'] for q in LRES[zs].values()]):.3f}, f_Q {np.median([q['f_Q'] for q in LRES[zs].values()]):.3f}; not the same disc mass except at z = 0")
    z0 = RES["0.00"]; n = len(z0); V = "UNDECIDED"; pairs = {}
    if n >= 6:
        Rm = float(np.median([q["R_live"] for q in z0.values()])); fm = float(np.median([q["f_Q"] for q in z0.values()]))
        sd = sorted(z0); rho = [z0[s]["R_live"] / LRES["0.00"][s]["R_live"] for s in sd]; df = [z0[s]["f_Q"] - LRES["0.00"][s]["f_Q"] for s in sd]; b1, b2 = boot(rho, 1.0), boot(df, 0.0)
        P("Same-seed pairs with LC1, z = 0: seed, R_live PZ1, LC1, rho; f_Q PZ1, LC1, delta")
        for s, a, b in zip(sd, rho, df): P(f"  {s.split('_')[1]} {z0[s]['R_live']:.3f} {LRES['0.00'][s]['R_live']:.3f} {a:.3f}; {z0[s]['f_Q']:.3f} {LRES['0.00'][s]['f_Q']:.3f} {b:+.3f}")
        up = lambda lo, hi, nu: 0 if lo <= nu <= hi else (1 if lo > nu else -1); sg = (up(b1[0], b1[1], 1.0), up(b2[0], b2[1], 0.0)); V2 = "NO DETECTED CHANGE" if sg == (0, 0) else "MIXED" if sg[0] * sg[1] < 0 else "SHIFT UP" if max(sg) > 0 else "SHIFT DOWN"
        P(f"  median rho {np.median(rho):.3f} [{b1[0]:.3f}, {b1[1]:.3f}], {sum(q > 1 for q in rho)} of {n} above 1; median delta f_Q {np.median(df):+.3f} [{b2[0]:+.3f}, {b2[1]:+.3f}], {sum(q > 0 for q in df)} of {n} above 0")
        V = f"{R.label(Rm)}; {R.lab2(fm)}; {V2}"; P(f"VERDICT at z = 0, {n} seeds: {V} (R_live {Rm:.3f}, LC1 2.154; f_Q {fm:.3f}, LC1 0.872)"); pairs = dict(rho=rho, df=df, b_rho=b1, b_df=b2, R=Rm, f=fm)
    else: P(f"VERDICT: UNDECIDED, {n} finished seeds (need 6)")
    N = os.path.join(RUNS, "M1e12_s1_ng64_NULL"); k6 = None
    if os.path.exists(os.path.join(N, "snap_zf.npz")):
        Q, Sr, _ = null_cmp(os.path.join(N, "snap_zf.npz"), os.path.join(X48R, "M1e12_s1_ng64", "snap_zf.npz"), json.loads(str(np.load(os.path.join(N, "snap_zf.npz"))["meta"]))["zf"]); md = float(np.abs(Q[1:] - 1).max()); k6 = md <= 0.10 and abs(Sr - 1) <= 0.15; P(f"K6 whole-path null at z_f against X48's snap_zf: Q {' '.join(f'{q:.3f}' for q in Q)}; max |Q - 1| at r/R_d 2-10 {md:.3f} (line 0.10), S ratio {Sr:.3f} (within 15 %): {'PASS' if k6 else 'FAIL'}")
        if os.path.exists(os.path.join(N, "snap_z0.00.npz")):
            Q0, S0, _ = null_cmp(os.path.join(N, "snap_z0.00.npz"), os.path.join(R.ZN1R, "M1e12_s1_ng64", "snap_z0.00.npz"), 0.0); P(f"  chaos floor at z = 0 against ZN1, reported: Q {' '.join(f'{q:.3f}' for q in Q0)}; S ratio {S0:.3f}")
    else: P("K6 not finished")
    if k6 is not True and V != "UNDECIDED": P("K6 not passed: no verdict stands"); V = "NO VERDICT, K6"
    M = os.path.join(RUNS, "M1e12_s1_ng64_MUTATE"); mt = R.read("0.00", [M])
    if mt and "M1e12_s1_ng64" in z0:
        q1, q2 = z0["M1e12_s1_ng64"]["Q"][2], mt["M1e12_s1_ng64_MUTATE"]["Q"][2]; d = (q2 - 1) / (q1 - 1) - 1; P(f"MUTATE M_d x 2, seed 1: Q(3 R_d) - 1 from {q1 - 1:.3f} to {q2 - 1:.3f}, {d:+.0%}: {'BITES' if d > 0.30 else 'INSENSITIVE, lane UNDECIDED'}")
        if d <= 0.30: V = "UNDECIDED"
    else: P("MUTATE not finished")
    json.dump(dict(verdict=V, r_over_Rd=RDG.tolist(), turnaround=ta, pairs_lc1=pairs, pairs=RES), open(os.path.join(HERE, "pz1_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "pz1.out"), "w").write("\n".join(OUT) + "\n")
