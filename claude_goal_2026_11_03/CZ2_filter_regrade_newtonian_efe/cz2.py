#!/usr/bin/env python3
"""CZ2: re-grade the filter forms LOC (KT26/27), TID (KT28), HALF (KT25 r_M/2) on MW, Cassini, 24 dwarfs, SPARC with the
host's Newtonian field inside QUMOND's nu. Criteria 1fadaa469a. Cassini and dwarfs recomputed (KT27/KT28 code copied, CZ1's
field change); MW and SPARC carried from committed JSON (no external field in those models).
OMP_NUM_THREADS=1 python3 -I cz2.py [--mutate]. kappa = 1/2 FITTED and held fixed; not theory closed."""
import csv, json, math, os, resource, sys
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
from scipy.special import erf
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); RB = os.path.join(REPO, "rebuild_2026_10_22")
MUT = "--mutate" in sys.argv; OUT = []; RES = {}; fail = 0
def P(s): print(s, flush=True); OUT.append(s)
KAP = 0.5; A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; Gk = 4.30091e-6; CONV = 3.0857e19 / 1e6; XCLIP = 200.0
nu_s = lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300))
nu = (lambda y: np.ones_like(np.asarray(y, float))) if MUT else nu_s
M_MW = 7.0e10  # KT15's frozen MW baryonic mass
P(f"CZ2 (criteria 1fadaa469a){'  [MUTATE]' if MUT else ''}; kappa = 1/2 FITTED; not theory closed")

# ---------- the two local rules, copied (KT27 xi_loc, KT28 xi_tid) ----------
def xi_loc(r, gm, gs, clip):
    dg = np.abs(np.gradient(gm, r)); return np.minimum(gm * gm / np.maximum(dg * gs, 1e-300), clip)
def xi_tid(r, gm, gs, clip):
    tau = np.sqrt(np.gradient(gm, r) ** 2 + 2 * (gm / r) ** 2); lt = np.log(np.maximum(tau, 1e-300))
    dt = np.abs(tau * np.gradient(lt, np.log(r)) / r); return np.minimum(4 / math.sqrt(3) * tau ** 3 / np.maximum(dt * dt * gs, 1e-300), clip)

# ---------- T1 Cassini (KT16's integral) ----------
GMs = 6.6743e-11 * 1.98892e30; GEXT, CEIL = 2.32e-10, 5.2e-27
def gh_pt(r, xi):
    xi = np.broadcast_to(xi, r.shape); x = r / xi; out = np.empty_like(r); s = x < 1e-3
    out[~s] = (erf(x[~s] / math.sqrt(2)) - math.sqrt(2 / math.pi) * x[~s] * np.exp(-x[~s] ** 2 / 2)) / r[~s] ** 2; out[s] = math.sqrt(2 / math.pi) / 3 * r[s] / xi[s] ** 3; return out
def qcas(eta, xi, nr=20000, nm=200):
    u = np.linspace(math.log(1e-7), math.log(1e5), nr); r = np.exp(u); mu, w = np.polynomial.legendre.leggauss(nm)
    X = xi(r) if callable(xi) else xi; g = gh_pt(r, X)[:, None]; M = mu[None, :]
    A_ = nu(np.sqrt(eta * eta + g * g + 2 * eta * g * M)) - 1; return abs(1.5 * float(np.trapz(((A_ * (eta * (3 * M - 5 * M ** 3) + g * (1 - 3 * M * M))) @ w) / r, u))), X
def cas_loc(eta):
    def f(x):
        gq = np.sqrt(x ** -4.0 + eta * eta); return xi_loc(x, nu(gq) * gq, 1 / KAP, 1e4)
    return f
def cas_tid(eta):
    def f(x):
        gq = np.sqrt(x ** -4.0 + eta * eta); return xi_tid(x, nu(gq) * x ** -2.0, 1 / KAP, 1e4)
    return f
CAND = ("LOC", "TID", "HALF"); T1 = {}
K1C = {"canonical": dict(LOC=0.0005, TID=0.11), "alt": dict(LOC=0.0021, TID=0.209)}
K2C = {"canonical": dict(LOC=0.003948, HALF=1.179), "alt": dict(LOC=0.02147, HALF=2.97)}
P("\nT1 Cassini (Q2 / ceiling)")
for foot, a0 in A0SI.items():
    rM = math.sqrt(GMs / a0); qp = CEIL / (1.5 * a0 / rM); eta0 = GEXT / a0; etaN = brentq(lambda y: float(nu_s(y)) * y - eta0, 1e-6, eta0)
    out = {}
    for lab, eta in (("E0", eta0), ("N", etaN)):
        for c, xi in (("LOC", cas_loc(eta)), ("TID", cas_tid(eta)), ("HALF", 0.5), ("0.55", 0.55)):
            q, X = qcas(eta, xi); out[f"{lab}|{c}"] = dict(eta=eta, x_ceiling=q / qp, ok=bool(q <= qp), xi_min_rM=float(np.min(X)))
    for c, v in K1C[foot].items():
        x = out[f"E0|{c}"]["x_ceiling"]; ok = MUT or abs(round(x, len(str(v).split(".")[1])) - v) < 1e-9
        fail += not ok; P(f"K1 [{foot}] {c} with eta0: {x:.4g} x (KT2{'7' if c == 'LOC' else '8'} {v}): {'PASS' if ok else 'FAIL'}")
    for c, v in K2C[foot].items():
        x = out[f"N|{c}"]["x_ceiling"]; ok = MUT or abs(round(x, len(str(v).split(".")[1])) - v) < 1e-9
        fail += not ok; P(f"K2 [{foot}] {c} with eta_N: {x:.4g} x (CZ1 {v}): {'PASS' if ok else 'FAIL'}")
    for c in ("LOC", "TID", "HALF", "0.55"):
        a_, b_ = out[f"E0|{c}"], out[f"N|{c}"]
        P(f"  [{foot}] {c:5s}: eta0 {a_['x_ceiling']:.4g} x -> eta_N {b_['x_ceiling']:.4g} x ({'PASS' if b_['ok'] else 'FAIL'}); xi min {b_['xi_min_rM']:.3g} r_M")
    RES[f"cassini|{foot}"] = dict(eta0=eta0, etaN=etaN, rows=out); T1[foot] = {c: out[f"N|{c}"]["ok"] for c in CAND}

# ---------- T2 dwarfs (KT15's model, row-wise width) ----------
UPS = np.linspace(1, 3, 41)
def rgrid(a, xi, n=2000): return np.geomspace(1e-4 * a, 60 * a + 8 * xi, n)
def plummer(r, M, a): return 3 * M / (4 * math.pi * a ** 3) * (1 + (r / a) ** 2) ** -2.5
def smooth_rows(r, rho, s, mask_small=False):
    s = np.broadcast_to(np.asarray(s, float), r.shape); R, Rp, S = r[:, None], r[None, :], s[:, None]
    K = (Rp / (math.sqrt(2 * math.pi) * S * R)) * (np.exp(-(R - Rp) ** 2 / (2 * S * S)) - np.exp(-(R + Rp) ** 2 / (2 * S * S))); out = np.trapz(K * rho[None, :], r, axis=1)
    if mask_small:
        dr = np.gradient(r); m = s < 3 * dr; out[m] = rho[m]
    return out
def menc(r, rho):
    f = 4 * math.pi * r * r * rho; return np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(r))]) + 4 * math.pi * rho[0] * r[0] ** 3 / 3
def sig_los(M, a, mode, a0, ge, xi0=0.0):
    """mode 'plain', 'const' (xi0), 'LOC' (row-wise xi_loc on the total field), 'TID' (row-wise xi_tid on the own field)."""
    if mode in ("LOC", "TID"):
        r = rgrid(a, XCLIP); rho = plummer(r, M, a); gN = Gk * menc(r, rho) / r ** 2; gq = np.sqrt(gN * gN + ge * ge)
        X = xi_loc(r, nu(gq / a0) * gq, a0 / KAP, XCLIP) if mode == "LOC" else xi_tid(r, nu(gq / a0) * gN, a0 / KAP, XCLIP)
    else:
        X = xi0; r = rgrid(a, X); rho = plummer(r, M, a); gN = Gk * menc(r, rho) / r ** 2
    gh = gN if mode == "plain" else Gk * menc(r, smooth_rows(r, rho, X, mode in ("LOC", "TID"))) / r ** 2
    g = gN + (nu(np.sqrt(ge * ge + gh * gh) / a0) - 1) * gh; return math.sqrt(np.trapz(rho * r * g * 4 * math.pi * r * r, r) / (3 * M))
DATA = os.path.join(REPO, "real_research/data/dsph/mcconnachie2012_dsph.csv"); rows = []
for d in csv.DictReader(open(DATA)):
    if not d["e_sigma*"] or float(d["VMag"]) > -8 or d["Name"].startswith(("M32", "NGC", "Sagittarius")): continue
    rows.append(dict(name=d["Name"], sub=d["SubG"], D=float(d["D"]), L=10 ** (-0.4 * (float(d["VMag"]) - 4.83)), a=float(d["R2"]) / 1e3, s=float(d["sigma*"]), e=float(d["e_sigma*"]), MHI=float(d["M.HI"]) * 1e6 if d["M.HI"] else 0.0))
cz1 = json.load(open(os.path.join(HERE, "..", "CZ1_newtonian_external_field", "cz1.json")))
E2G = {r_["name"]: r_["ge_over_a0"] for r_ in cz1["dwarf|alt|E2|plain"]["rows"]}  # CZ1's MW + M31 field, in units of alt a0
GEV = {"E0": lambda d, a0: (200.0 ** 2 / d["D"]) if d["sub"] == "MW" else 0.0, "E1": lambda d, a0: Gk * M_MW / d["D"] ** 2 if d["sub"] == "MW" else 0.0,
       "E2": lambda d, a0: E2G[d["name"]] * A0SI["alt"] * CONV}
MODES = {"E0": [("plain", 0.0), ("HALF", 0.5), ("LOC", 0.0), ("TID", 0.0)], "E1": [("plain", 0.0), ("HALF", 0.5), ("0.55", 0.55), ("LOC", 0.0), ("TID", 0.0)]}
MODES["E2"] = MODES["E1"]
K1D = {"canonical": dict(plain=15, HALF=15, LOC=14, TID=15, forn_TID=9.0), "alt": dict(plain=15, HALF=15, LOC=14, TID=15, forn_TID=9.4)}
K2D = {"canonical": dict(plain=18, HALF=18, LOC=17, forn_LOC=11.94), "alt": dict(plain=18, HALF=18, LOC=17, forn_LOC=12.52)}
fi = [r_["name"] for r_ in rows].index("Fornax"); T2 = {}
P(f"\nT2 dwarfs {len(rows)} (line >= 15/24; STRICT >= plain under the same field)")
for foot, a0s in A0SI.items():
    a0 = a0s * CONV; T2[foot] = {}
    for ev, modes in MODES.items():
        cnt = {}; forn = {}
        for mode, eps in modes:
            n = 0; det = []; m = "const" if mode in ("HALF", "0.55") else mode
            for d in rows:
                ge = GEV[ev](d, a0); sp = np.array([sig_los(u_ * d["L"] + 1.33 * d["MHI"], d["a"], m, a0, ge, eps * math.sqrt(Gk * (u_ * d["L"] + 1.33 * d["MHI"]) / a0)) for u_ in UPS])
                ok = bool((np.abs(sp - d["s"]) <= 2 * d["e"]).any()); n += ok; det.append(dict(name=d["name"], obs=d["s"], pred_U2=float(sp[20]), ge_over_a0=ge / a0, passed=ok))
            cnt[mode] = n; forn[mode] = det[fi]["pred_U2"]; RES[f"dwarf|{foot}|{ev}|{mode}"] = dict(n_pass=n, rows=det)
        P(f"  [{foot} {ev}] " + ", ".join(f"{k} {v}/24" for k, v in cnt.items()) + "; Fornax " + ", ".join(f"{k} {forn[k]:.2f}" for k in cnt) + " (obs 11.7)")
        if ev in ("E0", "E1"):
            ref = (K1D if ev == "E0" else K2D)[foot]; ok = MUT or all(cnt[k] == v for k, v in ref.items() if not k.startswith("forn")) and all(abs(round(forn[k[5:]], 1 if ev == "E0" else 2) - v) < 1e-9 for k, v in ref.items() if k.startswith("forn"))
            fail += not ok; P(f"  K{'1' if ev == 'E0' else '2'} [{foot}] {ev} reproduces {'KT27/KT28' if ev == 'E0' else 'CZ1'} {ref}: {'PASS' if ok else 'FAIL'}")
        if ev == "E1":
            for mode, _ in modes:
                ch = [(x["name"].split(" (")[0], x["passed"]) for x, y in zip(RES[f"dwarf|{foot}|E1|{mode}"]["rows"], RES[f"dwarf|{foot}|E0|{'HALF' if mode == '0.55' else mode}"]["rows"]) if x["passed"] != y["passed"]]
                if ch and mode != "0.55": P(f"      {mode}: vs E0: " + ", ".join(f"{nm} {'now PASS' if p else 'now fail'}" for nm, p in ch))
            T2[foot] = {c: dict(n=cnt[c], ok=cnt[c] >= 15, strict=cnt[c] >= cnt["plain"]) for c in CAND}; T2[foot]["plain"] = cnt["plain"]

# ---------- T0 MW and T3 SPARC, carried ----------
J = lambda p: json.load(open(os.path.join(RB, p)))
mwj = dict(LOC=J("KT26_local_filter_rule/kt26.json"), TID=J("KT28_tidal_filter_rule/kt28_mw.json"), HALF=J("KT25_eps_equals_kappa/kt25.json"))
spj = dict(LOC=J("KT27_local_rule_alt_grade/kt27.json"), TID=J("KT28_tidal_filter_rule/kt28.json"), HALF=J("KT25_eps_equals_kappa/kt25_sparc.json"))
K3MW = {"canonical": dict(LOC=0, TID=0, HALF=9), "alt": dict(LOC=30, TID=19, HALF=78)}
K3SP = {"canonical": dict(LOC=0.0129, TID=0.0079, HALF=0.0021), "alt": dict(LOC=0.0031, TID=0.0005, HALF=-0.0006)}
P("\nT0 MW and T3 SPARC, carried from committed JSON")
T0, T3 = {}, {}
for foot in A0SI:
    T0[foot], T3[foot] = {}, {}
    for c in CAND:
        n = mwj[c][f"mw|{foot}|0.5"]["n_pass"]; T0[foot][c] = dict(n=n, ok=n >= 1)
        if c == "HALF": s = spj[c][foot]; dr = s["d_rms"]; sok = s["label"] == "SURVIVES SPARC"
        else: s = spj[c][f"sparc|{foot}"]; dr = s["d_rms"]; sok = bool(s["ok"])
        T3[foot][c] = dict(d_rms=dr, ok=sok)
        ok = MUT or (n == K3MW[foot][c] and abs(round(dr, 4) - K3SP[foot][c]) < 1e-9); fail += not ok
        P(f"  K3 [{foot}] {c}: MW cells {n} ({'PASS' if n >= 1 else 'FAIL'}), SPARC d rms {dr:+.4f} ({'PASS' if sok else 'FAIL'}); matches README: {'PASS' if ok else 'FAIL'}")

# ---------- labels ----------
P("\nLABELS (Newtonian external field)")
for foot in A0SI:
    for c in CAND:
        bad = [t for t, ok in (("T0 MW", T0[foot][c]["ok"]), ("T1 Cassini", T1[foot][c]), ("T2 dwarfs", T2[foot][c]["ok"]), ("T3 SPARC", T3[foot][c]["ok"])) if not ok]
        lab = f"{c} SURVIVES" if not bad else f"{c} FAILS: " + ", ".join(bad); st = "STRICT pass" if T2[foot][c]["strict"] else "STRICT fail"
        RES[f"label|{foot}|{c}"] = dict(label=lab, strict=st, T0=T0[foot][c], T1=T1[foot][c], T2=T2[foot][c], T3=T3[foot][c])
        P(f"LABEL [{foot}] {lab}  ({st}: {T2[foot][c]['n']}/24 vs plain {T2[foot]['plain']}/24)")

rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 30; RES["peak_rss_GB"] = rss; RES["fail"] = fail
P(f"\npeak RSS {rss:.2f} GB; failed checks: {fail}")
sfx = "_MUTATE" if MUT else ""; open(os.path.join(HERE, f"cz2{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"cz2{sfx}.json"), "w"), indent=1)
sys.exit(1 if (MUT or fail) else 0)
