#!/usr/bin/env python3
"""KT30 (copy of KT28): TRACE-FREE tidal rule xi_TF = sqrt6 tau^3 / (|dtau/dr|^2 g*), tau = |T - trT/3 I| = sqrt(2/3)|g' - g/r|
for a spherical field; --full swaps back to KT28's Frobenius norm and 4/sqrt3 (check R1). Older text: KT28 (copy of KT27): tidal filter rule xi_tid = (4/sqrt3) tau^3 / (|dtau/dr|^2 g*), tau = sqrt(g'^2 + 2 (g/r)^2) from the
system's own field (a uniform external field drops out), g* = a0 / kappa, applied row-wise on Cassini (KT16's integral), the
24 dwarfs (KT15's model) and SPARC (KT19's code). python3 kt30.py [--mutate] [--full]. kappa = 1/2 FITTED and held fixed; not theory
closed.

CW3 COPY (cw_lanes_2026_11_04/CW3_cz1_defect_sweep). The original rebuild_2026_10_22/KT30_tracefree_tidal_rule/kt30.py is not edited.
Only the external field inside nu changes, exactly as CZ2 did for KT25-KT28.  CW3_FIELD=orig: the committed fields, Cassini eta =
2.32e-10/a0 (observed) and dwarfs ge = (200 km/s)^2/D (MOND), the K1 run.  CW3_FIELD=newton: Cassini eta_N from nu_s(y) y = 2.32e-10/a0,
dwarfs ge = G M_MW,b / D^2 with M_MW,b = 7.0e10 Msun (KT15's frozen value, CZ1 E1).  In the newton run the R1 reference values become
CZ1/CZ2's corrected values for KT25's constant rule (Cassini 1.179 / 2.97, dwarfs 18/24), a K2 check of the field code.
CW3_MUTATE=1 (or --mutate): nu == 1 (the lane's own MUTATE).  The inversion for eta_N keeps nu_s, so the two fields still differ.
Run: CW3_FIELD=... OMP_NUM_THREADS=1 nice -n 10 python3 -I kt30_cw3.py.  kappa = 1/2 FITTED; not theory closed."""
import csv, glob, json, math, os, sys
sys.dont_write_bytecode = True
import numpy as np
from scipy.special import erf
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.join(os.path.dirname(os.path.dirname(HERE)), "rebuild_2026_10_22")
FIELD = os.environ.get("CW3_FIELD", "orig"); assert FIELD in ("orig", "newton"); M_MW = 7.0e10
MUT = "--mutate" in sys.argv or os.environ.get("CW3_MUTATE") == "1"; FULL = "--full" in sys.argv; OUT = []; RES = {}; fail = 0
def P(s): print(s, flush=True); OUT.append(s)
P(f"[CW3] external field = {FIELD}; MUTATE nu == 1: {MUT}")
KAP = 0.5; A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; Gk = 4.30091e-6; CONV = 3.0857e19 / 1e6; XCLIP = 200.0
nu_s = lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300))
nu = (lambda y: np.ones_like(np.asarray(y, float))) if MUT else nu_s
from scipy.ndimage import gaussian_filter1d
def xi_loc(r, gm, gs, clip, sm=0.0):
    """tidal rule (4/sqrt3) tau^3 / (|tau'|^2 g*) on a grid from the system's own field gm; sm > 0 smooths ln tau in ln r
    (Gaussian width sm) before differentiating, on a log-uniform grid. Clipped where tau' -> 0."""
    gp = np.gradient(gm, r); tau = np.sqrt(gp ** 2 + 2 * (gm / r) ** 2) if FULL else math.sqrt(2 / 3) * np.abs(gp - gm / r); CC = 4 / math.sqrt(3) if FULL else math.sqrt(6)
    lt = np.log(np.maximum(tau, 1e-300))
    if sm > 0: lt = gaussian_filter1d(lt, sm / float(np.mean(np.diff(np.log(r)))), mode="nearest"); tau = np.exp(lt)
    dt = np.abs(tau * np.gradient(lt, np.log(r)) / r); return np.minimum(CC * tau ** 3 / np.maximum(dt * dt * gs, 1e-300), clip)
# ---------- T1 Cassini (KT16's integral, xi per radius) ----------
GMs = 6.6743e-11 * 1.98892e30; GEXT, CEIL = 2.32e-10, 5.2e-27
def gh_pt(r, xi):
    xi = np.broadcast_to(xi, r.shape); x = r / xi; out = np.empty_like(r); s = x < 1e-3
    out[~s] = (erf(x[~s] / math.sqrt(2)) - math.sqrt(2 / math.pi) * x[~s] * np.exp(-x[~s] ** 2 / 2)) / r[~s] ** 2; out[s] = math.sqrt(2 / math.pi) / 3 * r[s] / xi[s] ** 3; return out
def qcas(eta, xi, nr=20000, nm=200):
    u = np.linspace(math.log(1e-7), math.log(1e5), nr); r = np.exp(u); mu, w = np.polynomial.legendre.leggauss(nm)
    X = xi(r) if callable(xi) else xi; g = gh_pt(r, X)[:, None]; M = mu[None, :]
    A = nu(np.sqrt(eta * eta + g * g + 2 * eta * g * M)) - 1; return abs(1.5 * float(np.trapz(((A * (eta * (3 * M - 5 * M ** 3) + g * (1 - 3 * M * M))) @ w) / r, u))), X
def cas_xi(eta):
    def f(x):
        gq = np.sqrt(x ** -4.0 + eta * eta); gm = nu(gq) * x ** -2.0; return xi_loc(x, gm, 1 / KAP, 1e4)
    return f
R1REF = {"canonical": 0.481, "alt": 1.06} if FIELD == "orig" else {"canonical": 1.179, "alt": 2.97}
for foot, a0 in A0SI.items():
    eta = GEXT / a0; rM = math.sqrt(GMs / a0); qp = CEIL / (1.5 * a0 / rM)
    if FIELD == "newton": eta = brentq(lambda y: float(nu_s(y)) * y - GEXT / a0, 1e-6, GEXT / a0)   # CW3: the only change in T1
    q5, _ = qcas(eta, 0.5); ok = abs(round(q5 / qp, 3 if foot == "canonical" else 2) - R1REF[foot]) < 1e-9 if not MUT else True; fail += not ok
    P(f"R1 Cassini [{foot}] constant xi 0.5 r_M: {q5 / qp:.4g} x ceiling (KT25 {R1REF[foot]}): {'PASS' if ok else 'FAIL'}")
    xg = np.geomspace(50, 200, 4001); r2 = float(np.interp(100.0, xg, xi_loc(xg, nu(xg ** -2.0) * xg ** -2.0, 1 / KAP, 1e9)))
    ok = MUT or abs(r2 / KAP - 1) <= 1e-2; fail += not ok; P(f"R2 [{foot}] point mass deep limit at 100 r_M: xi_tid / (kappa r_M) {r2 / KAP:.5f}: {'PASS' if ok else 'FAIL'}")
    if foot == "alt" and not MUT and not FULL:
        ru = np.geomspace(1e-2, 1.0, 400); gu = ru.copy(); t0 = math.sqrt(2 / 3) * np.abs(np.gradient(gu, ru) - gu / ru); tf = np.sqrt(np.gradient(gu, ru) ** 2 + 2 * (gu / ru) ** 2)
        e3u = float(np.max(t0 / tf)); ok = e3u <= 1e-6; fail += not ok; P(f"R3 uniform-density sphere: max tau_TF / tau_full {e3u:.1e}: {'PASS' if ok else 'FAIL'}")
        rp = np.geomspace(1e-3, 1e3, 1500); gp = rp / (rp * rp + 1) ** 1.5; m = (rp > 0.1) & (rp < 10); x0, x1 = xi_loc(rp, gp, 1.0, 1e30)[m], xi_loc(rp, gp, 1.0, 1e30, 0.1)[m]; e3 = abs(float(np.median(x1 / x0)) - 1)
        ok = e3 <= 0.05; fail += not ok; P(f"R3b ln tau smoothing on an analytic Plummer field, 0.1-10 a: median xi change {e3:.3f}: {'PASS' if ok else 'FAIL'}")
    qq, X = qcas(eta, cas_xi(eta)); xr = np.exp(np.linspace(math.log(1e-7), math.log(1e5), 20000)); i = int(np.argmin(X))
    RES[f"cassini|{foot}"] = dict(q=qq, x_ceiling=qq / qp, ok=bool(qq <= qp), xi_min_rM=float(X[i]), at_x=float(xr[i]))
    P(f"T1 Cassini [{foot}] tidal rule: q {qq:.4g} = {qq / qp:.3g} x ceiling: {'PASS' if qq <= qp else 'FAIL'}; xi_tid min {X[i]:.3g} r_M at r = {xr[i]:.3g} r_M, at Saturn {np.interp(9.58 * 1.495978707e11 / rM, xr, X):.4g} r_M")
# ---------- T2 dwarfs (KT15's model, row-wise width) ----------
DATA = os.path.join(RB, "../real_research/data/dsph/mcconnachie2012_dsph.csv"); UPS = np.linspace(1, 3, 41)
def rgrid(a, xi, n=2000): return np.geomspace(1e-4 * a, 60 * a + 8 * xi, n)
def plummer(r, M, a): return 3 * M / (4 * math.pi * a ** 3) * (1 + (r / a) ** 2) ** -2.5
def smooth_rows(r, rho, s, mask_small=False):
    """KT15's spherical Gaussian smoothing with width s (scalar or one per output radius)."""
    s = np.broadcast_to(np.asarray(s, float), r.shape); R, Rp, S = r[:, None], r[None, :], s[:, None]
    K = (Rp / (math.sqrt(2 * math.pi) * S * R)) * (np.exp(-(R - Rp) ** 2 / (2 * S * S)) - np.exp(-(R + Rp) ** 2 / (2 * S * S))); out = np.trapz(K * rho[None, :], r, axis=1)
    if mask_small:
        dr = np.gradient(r); m = s < 3 * dr; out[m] = rho[m]
    return out
def menc(r, rho):
    f = 4 * math.pi * r * r * rho; return np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(r))]) + 4 * math.pi * rho[0] * r[0] ** 3 / 3
def sig_los(M, a, mode, a0, ge, xi0=0.0):
    """mode 'plain' (xi 0), 'const' (xi0), 'local' (row-wise xi_loc), 'at_a' (xi_tid(a), one value)."""
    if mode == "local" or mode == "at_a":
        r = rgrid(a, XCLIP); rho = plummer(r, M, a); gN = Gk * menc(r, rho) / r ** 2; gq = np.sqrt(gN * gN + ge * ge); X = xi_loc(r, nu(gq / a0) * gN, a0 / KAP, XCLIP)
        if mode == "at_a": X = float(np.interp(a, r, X))
    else:
        X = xi0; r = rgrid(a, X); rho = plummer(r, M, a); gN = Gk * menc(r, rho) / r ** 2
    gh = gN if mode == "plain" else Gk * menc(r, smooth_rows(r, rho, X, mode == "local")) / r ** 2
    g = gN + (nu(np.sqrt(ge * ge + gh * gh) / a0) - 1) * gh; return math.sqrt(np.trapz(rho * r * g * 4 * math.pi * r * r, r) / (3 * M)), X, r
rows = []
for d in csv.DictReader(open(DATA)):
    if not d["e_sigma*"] or float(d["VMag"]) > -8 or d["Name"].startswith(("M32", "NGC", "Sagittarius")): continue
    rows.append(dict(name=d["Name"], sub=d["SubG"], D=float(d["D"]), L=10 ** (-0.4 * (float(d["VMag"]) - 4.83)), a=float(d["R2"]) / 1e3, s=float(d["sigma*"]), e=float(d["e_sigma*"]), MHI=float(d["M.HI"]) * 1e6 if d["M.HI"] else 0.0))
P(f"\ndwarfs {len(rows)}")
for foot, a0s in A0SI.items():
    a0 = a0s * CONV; cnt = {}
    for mode in ("plain", "const", "local", "at_a"):
        n = 0; det = []
        for d in rows:
            ge = (((200.0 ** 2 / d["D"]) if FIELD == "orig" else Gk * M_MW / d["D"] ** 2) if d["sub"] == "MW" else 0.0); sp = []; xa = None   # CW3: the only change in T2
            for j, u in enumerate(UPS):
                M = u * d["L"] + 1.33 * d["MHI"]; s, X, r = sig_los(M, d["a"], mode, a0, ge, 0.5 * math.sqrt(Gk * M / a0)); sp.append(s)
                if j == 20: xa = float(np.interp(d["a"], r, X)) if np.ndim(X) else float(X)
            sp = np.array(sp); ok = bool((np.abs(sp - d["s"]) <= 2 * d["e"]).any()); n += ok; det.append(dict(name=d["name"], obs=d["s"], pred_U2=float(sp[20]), xi_at_a_U2=xa, rM_half_U2=0.5 * math.sqrt(Gk * (2 * d["L"] + 1.33 * d["MHI"]) / a0), passed=ok))
        cnt[mode] = n; RES[f"dwarf|{foot}|{mode}"] = dict(n_pass=n, rows=det)
    cref = 15 if FIELD == "orig" else 18
    ok = MUT or cnt["const"] == cref; fail += not ok; P(f"R1 dwarfs [{foot}] constant 0.5 r_M: {cnt['const']}/24 ({'KT25' if FIELD == 'orig' else 'CZ1 E1'} {cref}/24): {'PASS' if ok else 'FAIL'}")
    fi = [r_["name"] for r_ in rows].index("Fornax"); dl = RES[f"dwarf|{foot}|local"]["rows"]
    P(f"T2 dwarfs [{foot}] tidal rule: {cnt['local']}/24 (plain {cnt['plain']}/24, xi 0.5 r_M {cnt['const']}/24): {'PASS' if cnt['local'] >= 15 else 'FAIL'}; beside, xi_tid(a) one value {cnt['at_a']}/24; Fornax pred {dl[fi]['pred_U2']:.1f} (obs 11.7), xi_tid(a) {dl[fi]['xi_at_a_U2']:.3g} vs r_M/2 {dl[fi]['rM_half_U2']:.3g} kpc")
    P("    xi_tid(a)/(r_M/2) per dwarf at Upsilon 2: " + ", ".join(f"{x['name']} {x['xi_at_a_U2'] / x['rM_half_U2']:.2g}{'*' if x['passed'] else ''}" for x in dl))
    RES[f"dwarf_ok|{foot}"] = bool(cnt["local"] >= 15)
# ---------- T3 SPARC (KT19's code, row-wise width) ----------
D = os.path.join(RB, "../real_research/data/sparc_data"); MRT = os.path.join(RB, "../real_research/data/SPARC_Lelli2016c.mrt"); G = Gk; A0 = {k: v * CONV for k, v in A0SI.items()}
tab = {}
for line in open(MRT):
    p = line.split()
    if len(p) >= 18 and p[1].isdigit(): tab[p[0]] = dict(L=float(p[7]) * 1e9, Rd=float(p[11]), MHI=float(p[13]) * 1e9)
GAL = []
for fn in sorted(glob.glob(os.path.join(D, "*_rotmod.dat"))):
    nm = os.path.basename(fn).replace("_rotmod.dat", "")
    try: d = np.genfromtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6 or len(d) < 3 or nm not in tab: continue
    R, Vo, eV, Vg, Vd, Vb = (d[:, j] for j in range(6)); o = np.argsort(R); R, Vo, eV, Vg, Vd, Vb = R[o], Vo[o], eV[o], Vg[o], Vd[o], Vb[o]
    Bg = Vg * np.abs(Vg); Bs = 0.5 * Vd * np.abs(Vd) + 0.7 * Vb * np.abs(Vb); q = (R > 0) & (Vo > 0) & (eV > 0) & (eV / np.maximum(Vo, 1e-9) < 0.1) & (Bg + Bs > 0)
    if q.sum() < 3: continue
    GAL.append(dict(name=nm, R=R, Vo=Vo, Bg=Bg, Bs=Bs, q=q, **tab[nm]))
P(f"\nSPARC galaxies {len(GAL)}, points {sum(g['q'].sum() for g in GAL)}")
def Mprof(g, f):
    B = g["Bg"] + f * g["Bs"]; M = np.maximum(B * g["R"] / G, 0.0); return np.maximum.accumulate(M)
def smoothed_ratio(g, a0, xi, n=1500):
    """KT19's ratio M_smoothed(R)/M(R); xi a number (KT19's grid) or 'local' (row-wise xi_loc on a grid reaching 8 XCLIP)."""
    R = g["R"]; Mm = Mprof(g, 1.0); Mb = 0.5 * g["L"] + 1.33 * g["MHI"]; Rl = R[-1]; Rd = max(g["Rd"], 0.1); loc = xi == "local"
    r = np.geomspace(min(R[0], 0.01) * 0.1, Rl * 10 + 8 * (XCLIP if loc else xi) + 10 * Rd, n)
    Mi = np.where(r < R[0], Mm[0] * (r / R[0]) ** 3, np.interp(r, R, Mm)); x = np.maximum(r - Rl, 0); Mi = Mi + np.where(r > Rl, max(Mb - Mm[-1], 0) * (1 - (1 + x / Rd) * np.exp(-x / Rd)), 0.0)
    dM = np.gradient(Mi, r); rho = np.maximum(dM, 0) / (4 * math.pi * r * r)
    if loc: gb = G * Mi / r ** 2; X = xi_loc(r, nu(gb / a0) * gb, a0 / KAP, XCLIP, 0.1)
    else: X = xi
    rs = smooth_rows(r, rho, X, loc)
    cm = lambda rh: np.concatenate([[0.0], np.cumsum(0.5 * (4 * math.pi * r[1:] ** 2 * rh[1:] + 4 * math.pi * r[:-1] ** 2 * rh[:-1]) * np.diff(r))])
    M0, M1 = cm(rho), cm(rs); return np.interp(R, r, M1) / np.maximum(np.interp(R, r, M0), 1e-30), float(M1[-1] / M0[-1]), (np.interp(R, r, X) if loc else np.full(len(R), X))
def run(a0, mode):
    rr, allr, med_in, xs, mr = [], [], [], [], []
    for g in GAL:
        B = g["Bg"] + g["Bs"]; q = g["q"] & (B > 0); gb = B[q] / g["R"][q]; go = g["Vo"][q] ** 2 / g["R"][q]
        if mode == "plain": gh = gb
        else:
            xi = "local" if mode == "local" else 0.5 * math.sqrt(G * (0.5 * g["L"] + 1.33 * g["MHI"]) / a0); ratio, m, X = smoothed_ratio(g, a0, xi); gh = gb * ratio[q]; xs.append(X[q]); mr.append(m)
        gm = gb + (nu(gh / a0) - 1) * gh; r = np.log10(go) - np.log10(gm); rr.append(math.sqrt(np.mean(r * r))); allr.append(r); med_in.append(r[g["R"][q] < 2 * g["Rd"]])
    a = np.concatenate(allr); i = np.concatenate(med_in); out = dict(rms=float(math.sqrt(np.mean(np.square(rr)))), med=float(np.median(a)), med_inner=float(np.median(i)), per_gal=rr)
    if xs: x = np.concatenate(xs); out.update(xi_pct=[float(v) for v in np.percentile(x, [5, 50, 95])], frac_clip=float(np.mean(x >= XCLIP * 0.999)), frac_floor=float(np.mean(x < 0.01)), mass_ratio=[float(min(mr)), float(np.median(mr)), float(max(mr))])
    return out
R1S = {"canonical": 0.0021, "alt": -0.0006}
for foot, a0 in A0.items():
    base = run(a0, "plain"); cst = run(a0, "const"); loc = run(a0, "local"); d0 = cst["rms"] - base["rms"]; d = loc["rms"] - base["rms"]
    ok = MUT or abs(round(d0, 4) - R1S[foot]) < 1e-9; fail += not ok; P(f"R1 SPARC [{foot}] constant 0.5 r_M: d rms {d0:+.4f} (KT25 {R1S[foot]:+.4f}): {'PASS' if ok else 'FAIL'}")
    t3 = d <= 0.005 and abs(loc["med"]) <= 0.05; RES[f"sparc|{foot}"] = dict(plain={k: base[k] for k in ("rms", "med", "med_inner")}, local={k: v for k, v in loc.items() if k != "per_gal"}, d_rms=d, ok=bool(t3))
    P(f"    beside: data points with xi < 0.01 kpc (tau_TF near a zero) {loc['frac_floor']:.3f}")
    P(f"T3 SPARC [{foot}] plain rms {base['rms']:.4f} med {base['med']:+.4f} inner {base['med_inner']:+.4f}; local rms {loc['rms']:.4f} med {loc['med']:+.4f} inner {loc['med_inner']:+.4f}; d rms {d:+.4f}: {'PASS' if t3 else 'FAIL'}")
    P(f"    xi_tid at data points 5/50/95 % {loc['xi_pct'][0]:.3g}/{loc['xi_pct'][1]:.3g}/{loc['xi_pct'][2]:.3g} kpc, clipped {loc['frac_clip']:.3f}; total mass ratio min/med/max {loc['mass_ratio'][0]:.3f}/{loc['mass_ratio'][1]:.3f}/{loc['mass_ratio'][2]:.3f}")
    w = sorted(((loc["per_gal"][k] - base["per_gal"][k], GAL[k]["name"]) for k in range(len(GAL))), reverse=True)[:6]; P("    largest per-galaxy rms rises: " + "; ".join(f"{n} {v:+.3f}" for v, n in w)); RES[f"sparc|{foot}"]["worst"] = w
for foot in A0SI:
    bad = [t for t, ok in (("Cassini", RES[f"cassini|{foot}"]["ok"]), ("dwarfs", RES[f"dwarf_ok|{foot}"]), ("SPARC", RES[f"sparc|{foot}"]["ok"])) if not ok]
    lab = ("T1-T3 PASS" if not bad else "FAILS: " + ", ".join(bad)) + " (T0 Milky Way in kt30_mw)"
    RES[f"label|{foot}"] = lab; P(f"LABEL [{foot}]: {lab}")
if FULL and not MUT:
    K = json.load(open(os.path.join(RB, "KT28_tidal_filter_rule/kt28.json"))); e1 = 0.0
    for foot in A0SI:
        pr = [(RES[f"cassini|{foot}"]["q"], K[f"cassini|{foot}"]["q"]), (RES[f"dwarf|{foot}|local"]["n_pass"], K[f"dwarf|{foot}|local"]["n_pass"]), (RES[f"sparc|{foot}"]["d_rms"], K[f"sparc|{foot}"]["d_rms"]), (RES[f"sparc|{foot}"]["local"]["med"], K[f"sparc|{foot}"]["local"]["med"])]
        e1 = max([e1] + [abs(a / b - 1) if b else abs(a) for a, b in pr])
    ok = e1 <= 1e-3; fail += not ok; P(f"R1 full-norm mode reproduces KT28 T1-T3 (Cassini q, dwarf count, SPARC d rms, median): max rel {e1:.1e}: {'PASS' if ok else 'FAIL'}")
RES["fail"] = fail; P(f"failed checks: {fail}")
sfx = f"_cw3_{FIELD}" + ("_MUTATE" if MUT else "") + ("_FULL" if FULL else ""); open(os.path.join(HERE, f"kt30{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"kt30{sfx}.json"), "w"), indent=1, default=float)
sys.exit(1 if (MUT or fail) else 0)
