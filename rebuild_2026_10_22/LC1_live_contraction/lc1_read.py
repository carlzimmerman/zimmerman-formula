#!/usr/bin/env python3
"""LC1 read-out (FROZEN_CRITERIA.md f4c8459748): same-seed pairs, disc against ZN1's no-disc run: Q(r), R_live, Blumenthal's and Gnedin's Q(r), f_Q, the frozen labels, MUTATE.
    python3 lc1_read.py             # all finished pairs
    python3 lc1_read.py --selftest  # synthetic pairs with a known response; reads no LC1 snapshot
kappa = 1/2 FITTED; not theory closed."""
import glob, importlib.util, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); ZN1R = os.path.join(REB, "ZN1_zooms_to_z0", "runs")
X77P = os.path.join(REB, "X77_direct_core_surface_density", "x77_direct_eta.py"); _src = open(X77P).read(); _src = _src[:_src.index("# K2: formula vs direct integration")]
NS = dict(__file__=X77P, __name__="x77_prefix"); _a = sys.argv; sys.argv = [X77P]; exec(compile(_src, X77P, "exec"), NS); sys.argv = _a; FIT, XA = NS["fit"], NS["XA"]
_x39 = open(os.path.join(REB, "X39_baryonic_contraction", "x39_contraction.py")).read(); CN = dict(np=np, SGN=1.0); exec(_x39[_x39.index("def contract(r, Mb, M0, F, gnedin=None):"):_x39.index('P("\\n=== checks")')], CN); contract = CN["contract"]
RDG = np.array([1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 10.0]); Om, h = 0.2976016, 0.6856427; G = 4.30091e-9
def rho_c(z): return 3 * (100 * h) ** 2 * (Om * (1 + z) ** 3 + 1 - Om) / (8 * math.pi * G)
def cr(x, m): c = XA.centre(x, m); return np.sort(np.sqrt(((x - c) ** 2).sum(1)))
def S_fit(x, m, rho, eps):
    o, f = FIT(x, m, rho, eps)
    return None if f is None else dict(S=f["S"]["eta"] * 18 * math.pi ** 2 * rho * o["rvir"], a=f["S"]["a"], eta=f["S"]["eta"], rvir=o["rvir"], rconv=o["rconv"], c=o.get("c_nfw_fit"))
def r200(r, m, z):
    d = np.arange(1, len(r) + 1) * m / (4 / 3 * math.pi * r ** 3); return float(r[np.where(d >= 200 * rho_c(z))[0].max()])
def spherical(rB, m0, Md, a, Msim, R200):
    """Blumenthal and Gnedin on this seed's no-disc profile: the particles' mass is m0 (1 - f), the disc's spherical mass M_d [1 - a/sqrt(r^2 + a^2)], F = M_d/(M_sim - M_d)."""
    f = Md / Msim; rg = np.geomspace(1e-5, float(rB[-1]), 6000); M0 = (1 - f) * m0 * np.searchsorted(rB, rg); Mb = Md * (1 - a / np.sqrt(rg ** 2 + a ** 2)); F = Md / (Msim - Md)
    Mf, c1, _ = contract(rg, Mb, M0, F); Mg, c2, _ = contract(rg, Mb, M0, F, gnedin=(0.85, 0.8, R200))
    return rg, M0, Mf, Mg, max(c1, c2)
def pair(xd, xn, m0, Md, Rd, eps, rho, z):
    N = len(xn); Msim = m0 * N; m1 = m0 * (1 - Md / Msim); assert len(xd) == N, "N differs"
    rA, rB = cr(xd, m1), cr(xn, m0); rr = RDG * Rd; Q = np.searchsorted(rA, rr) / np.searchsorted(rB, rr); R2 = r200(rB, m0, z)
    rg, M0, Mf, Mg, cv = spherical(rB, m0, Md, Rd, Msim, R2); M0r = np.interp(np.log(rr), np.log(rg), M0); QB = np.interp(np.log(rr), np.log(rg), Mf) / M0r; QG = np.interp(np.log(rr), np.log(rg), Mg) / M0r
    fA, fB, fC = S_fit(xd, m1, rho, eps), S_fit(xn, m0, rho, eps), S_fit(xd, m0, rho, eps); i = [1, 2, 3]
    return dict(Q=Q.tolist(), QB=QB.tolist(), QG=QG.tolist(), f_Q=float(np.median((Q[i] - 1) / (QB[i] - 1))), f_G=float(np.median((Q[i] - 1) / (QG[i] - 1))), R_live=fA["S"] / fB["S"] if fA and fB else None, R_count=fC["S"] / fB["S"] if fC and fB else None, a_disc=fA["a"] if fA else None, a_nodisc=fB["a"] if fB else None, c_disc=fA["c"] if fA else None, c_nodisc=fB["c"] if fB else None, x_conv=3 * eps / Rd, conv=cv, Md=Md, Msim=Msim)
def label(R): return "WEAK" if R <= 1.25 else "STRONG" if R >= 1.45 else "INTERMEDIATE"
def lab2(f): return "BLUMENTHAL HOLDS" if f >= 0.8 else "PARTIAL" if f >= 0.4 else "WEAK RESPONSE"
OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def selftest():
    mu = lambda y: np.log1p(y) - y / (1 + y); rng = np.random.default_rng(5); N = 57777; c = 8.0; R2 = 0.21; ymax = c * 4; yg = np.geomspace(1e-6, ymax, 40000); u = rng.random(N) * float(mu(ymax)); y = np.interp(u, mu(yg), yg); v = rng.standard_normal((N, 3)); v /= np.linalg.norm(v, axis=1)[:, None]; r0 = y / c * R2; xn = r0[:, None] * v
    M2 = 200 * rho_c(0.0) * 4 / 3 * math.pi * R2 ** 3; Msim = M2 * float(mu(ymax) / mu(c)); m0 = Msim / N; Md = 6.7e10; Rd = 3.565e-3; eps = 3.5e-4; rho = Om * rho_c(0.0) / (Om + 1 - Om); f = Md / Msim; F = Md / (Msim - Md); rs = np.sort(r0); rg = np.geomspace(1e-5, float(rs[-1]), 6000); M0 = (1 - f) * m0 * np.searchsorted(rs, rg); Mb = Md * (1 - Rd / np.sqrt(rg ** 2 + Rd ** 2)); ok = True
    o = pair(xn, xn, m0, 0.0 + 1e-6 * Md, Rd, eps, rho, 0.0); a1 = max(abs(q - 1) for q in o["Q"]) <= 1e-12 and abs(o["R_live"] - 1) <= 1e-3; P(f"S1 identity pair, disc mass about 0: max |Q - 1| {max(abs(q - 1) for q in o['Q']):.1e}, R_live {o['R_live']:.4f}: {'PASS' if a1 else 'FAIL'}"); ok &= a1
    # a pair built by moving each particle to Blumenthal's own final radius
    rf = rg.copy(); Mi = M0.copy()
    for _ in range(200): rf = 0.5 * rf + 0.5 * rg * Mi * (1 + F) / np.maximum(np.interp(np.log(rf), np.log(rg), Mb) + Mi, 1e-300)
    rf_i = np.interp(np.log(r0), np.log(rg), np.log(rf)); xd = (np.exp(rf_i) / r0)[:, None] * xn; o = pair(xd, xn, m0, Md, Rd, eps, rho, 0.0); a2 = abs(o["f_Q"] - 1) <= 0.05; P(f"S2 particles moved to Blumenthal's radii: Q {[round(q, 3) for q in o['Q']]}, Q_B {[round(q, 3) for q in o['QB']]}, f_Q {o['f_Q']:.3f} (within 0.05 of 1), R_live {o['R_live']:.3f}, R_count {o['R_count']:.3f}: {'PASS' if a2 else 'FAIL'}"); ok &= a2
    return ok
def read(zs, runs):
    rows = {}
    for d in runs:
        s = os.path.basename(d); fd, fn = os.path.join(d, f"snap_z{zs}.npz"), os.path.join(ZN1R, s.replace("_MUTATE", ""), f"snap_z{zs}.npz")
        if not (os.path.exists(fd) and os.path.exists(fn)): continue
        A, B_ = np.load(fd, allow_pickle=False), np.load(fn, allow_pickle=False); ma = json.loads(str(A["meta"])); mb = json.loads(str(B_["meta"])); assert ma["N"] == mb["N"] and abs(float(A["m"]) / float(B_["m"]) - 1) < 1e-12, "seeds differ"
        rho = mb["Mf"] / (4 / 3 * math.pi * mb["qM"] ** 3) * (1 + float(zs)) ** 3; rows[s] = pair(A["x"], B_["x"], float(B_["m"]), ma["Md_now"], ma["lc1"]["Rd_kpc"] * 1e-3, ma["eps"], rho, float(zs))
    return rows
if __name__ == "__main__":
    P("LC1 read-out: a disc grown in a live zoom at 1e12, gravity only; kappa = 1/2 FITTED; not theory closed")
    if not selftest(): sys.exit("self-test failed: no reading")
    if "--selftest" in sys.argv: sys.exit(0)
    RUNS = sorted(glob.glob(os.path.join(HERE, "runs", "M1e12_s?_ng64"))); RES = {}
    for zs in ("0.50", "0.25", "0.00"):
        rows = read(zs, RUNS); RES[zs] = rows
        if not rows: P(f"z {zs}: no finished pair"); continue
        med = lambda k: np.median([q[k] for q in rows.values()], axis=0); Rl = [q["R_live"] for q in rows.values() if q["R_live"] is not None]; Rc = [q["R_count"] for q in rows.values() if q["R_count"] is not None]; fq = [q["f_Q"] for q in rows.values()]; fg = [q["f_G"] for q in rows.values()]
        P(f"z {zs}: {len(rows)} pairs; M_d now {list(rows.values())[0]['Md']:.3e}; r/R_d {RDG.tolist()}; softening x 3 at r/R_d {list(rows.values())[0]['x_conv']:.2f}")
        P("  Q live      " + " ".join(f"{q:.3f}" for q in med("Q"))); P("  Q Blumenthal " + " ".join(f"{q:.3f}" for q in med("QB"))); P("  Q Gnedin    " + " ".join(f"{q:.3f}" for q in med("QG")))
        P(f"  R_live {np.median(Rl):.3f} [{min(Rl):.3f}, {max(Rl):.3f}], at equal particle mass {np.median(Rc):.3f}; f_Q (Blumenthal) {np.median(fq):.3f} [{min(fq):.3f}, {max(fq):.3f}], f (Gnedin) {np.median(fg):.3f}; c_nfw no disc {np.median([q['c_nodisc'] for q in rows.values()]):.2f}, with disc {np.median([q['c_disc'] for q in rows.values()]):.2f}; by seed R_live " + " ".join(f"{x:.2f}" for x in Rl))
    z0 = RES["0.00"]; n = len(z0)
    if n < 6: P(f"VERDICT: UNDECIDED, {n} finished pairs (need 6)"); V = "UNDECIDED"
    else:
        Rm = float(np.median([q["R_live"] for q in z0.values()])); Rc = float(np.median([q["R_count"] for q in z0.values()])); fm = float(np.median([q["f_Q"] for q in z0.values()])); V = label(Rm); P(f"VERDICT at z = 0, {n} pairs: {V} (R_live {Rm:.3f}; WEAK at or below 1.25, STRONG at or above 1.45); {lab2(fm)} (f_Q {fm:.3f}); at equal particle mass R_live {Rc:.3f}, {label(Rc)}")
    M = os.path.join(HERE, "runs", "M1e12_s1_ng64_MUTATE"); mt = read("0.00", [M]); 
    if mt and "M1e12_s1_ng64" in z0:
        q1, q2 = z0["M1e12_s1_ng64"]["Q"][2], mt["M1e12_s1_ng64_MUTATE"]["Q"][2]; d = (q2 - 1) / (q1 - 1) - 1; P(f"MUTATE M_d x 2, seed 1: Q(3 R_d) - 1 from {q1 - 1:.3f} to {q2 - 1:.3f}, {d:+.0%}: {'BITES' if d > 0.30 else 'INSENSITIVE, lane UNDECIDED'}")
        if d <= 0.30: V = "UNDECIDED"
    else: P("MUTATE not finished")
    json.dump(dict(verdict=V, r_over_Rd=RDG.tolist(), pairs=RES), open(os.path.join(HERE, "lc1_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "lc1.out"), "w").write("\n".join(OUT) + "\n")
