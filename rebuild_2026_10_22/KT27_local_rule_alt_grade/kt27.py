#!/usr/bin/env python3
"""KT27: KT26's local filter rule xi_loc = |g|^2 / (|d|g|/dr| g*), g* = a0 / kappa, applied row-wise (smoothing width taken
at the point evaluated) on Cassini (KT16's integral), the 24 dwarfs (KT15's model) and SPARC (KT19's code). |g| is the
unfiltered board-law field. python3 kt27.py [--mutate]. kappa = 1/2 FITTED and held fixed; not theory closed."""
import csv, glob, json, math, os, sys
sys.dont_write_bytecode = True
import numpy as np
from scipy.special import erf
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)
MUT = "--mutate" in sys.argv; OUT = []; RES = {}; fail = 0
def P(s): print(s, flush=True); OUT.append(s)
KAP = 0.5; A0SI = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; Gk = 4.30091e-6; CONV = 3.0857e19 / 1e6; XCLIP = 200.0
nu_s = lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300))
nu = (lambda y: np.ones_like(np.asarray(y, float))) if MUT else nu_s
def xi_loc(r, gm, gs, clip):
    """|g|^2 / (|d|g|/dr| g*) on a grid, clipped where d|g|/dr -> 0."""
    dg = np.abs(np.gradient(gm, r)); return np.minimum(gm * gm / np.maximum(dg * gs, 1e-300), clip)
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
        gq = np.sqrt(x ** -4.0 + eta * eta); gm = nu(gq) * gq; return xi_loc(x, gm, 1 / KAP, 1e4)
    return f
R1REF = {"canonical": 0.481, "alt": 1.06}
for foot, a0 in A0SI.items():
    eta = GEXT / a0; rM = math.sqrt(GMs / a0); qp = CEIL / (1.5 * a0 / rM)
    q5, _ = qcas(eta, 0.5); ok = abs(round(q5 / qp, 3 if foot == "canonical" else 2) - R1REF[foot]) < 1e-9 if not MUT else True; fail += not ok
    P(f"R1 Cassini [{foot}] constant xi 0.5 r_M: {q5 / qp:.4g} x ceiling (KT25 {R1REF[foot]}): {'PASS' if ok else 'FAIL'}")
    x = np.array([100.0]); gd = lambda xx: nu(xx ** -2.0) * xx ** -2.0; h = 1e-5 * 100; r2 = KAP * gd(x) ** 2 / (abs(gd(x + h) - gd(x - h)) / (2 * h))
    ok = MUT or abs(r2[0] / KAP - 1) <= 1e-3; fail += not ok; P(f"R2 [{foot}] point mass deep limit at 100 r_M: xi_loc / (kappa r_M) {r2[0] / KAP:.5f}: {'PASS' if ok else 'FAIL'}")
    qq, X = qcas(eta, cas_xi(eta)); xr = np.exp(np.linspace(math.log(1e-7), math.log(1e5), 20000)); i = int(np.argmin(X))
    RES[f"cassini|{foot}"] = dict(q=qq, x_ceiling=qq / qp, ok=bool(qq <= qp), xi_min_rM=float(X[i]), at_x=float(xr[i]))
    P(f"T1 Cassini [{foot}] local rule: q {qq:.4g} = {qq / qp:.3g} x ceiling: {'PASS' if qq <= qp else 'FAIL'}; xi_loc min {X[i]:.3g} r_M at r = {xr[i]:.3g} r_M, at Saturn {np.interp(9.58 * 1.495978707e11 / rM, xr, X):.4g} r_M")
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
    """mode 'plain' (xi 0), 'const' (xi0), 'local' (row-wise xi_loc), 'at_a' (xi_loc(a), one value)."""
    if mode == "local" or mode == "at_a":
        r = rgrid(a, XCLIP); rho = plummer(r, M, a); gN = Gk * menc(r, rho) / r ** 2; gq = np.sqrt(gN * gN + ge * ge); X = xi_loc(r, nu(gq / a0) * gq, a0 / KAP, XCLIP)
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
            ge = (200.0 ** 2 / d["D"]) if d["sub"] == "MW" else 0.0; sp = []; xa = None
            for j, u in enumerate(UPS):
                M = u * d["L"] + 1.33 * d["MHI"]; s, X, r = sig_los(M, d["a"], mode, a0, ge, 0.5 * math.sqrt(Gk * M / a0)); sp.append(s)
                if j == 20: xa = float(np.interp(d["a"], r, X)) if np.ndim(X) else float(X)
            sp = np.array(sp); ok = bool((np.abs(sp - d["s"]) <= 2 * d["e"]).any()); n += ok; det.append(dict(name=d["name"], obs=d["s"], pred_U2=float(sp[20]), xi_at_a_U2=xa, rM_half_U2=0.5 * math.sqrt(Gk * (2 * d["L"] + 1.33 * d["MHI"]) / a0), passed=ok))
        cnt[mode] = n; RES[f"dwarf|{foot}|{mode}"] = dict(n_pass=n, rows=det)
    ok = MUT or cnt["const"] == 15; fail += not ok; P(f"R1 dwarfs [{foot}] constant 0.5 r_M: {cnt['const']}/24 (KT25 15/24): {'PASS' if ok else 'FAIL'}")
    fi = [r_["name"] for r_ in rows].index("Fornax"); dl = RES[f"dwarf|{foot}|local"]["rows"]
    P(f"T2 dwarfs [{foot}] local rule: {cnt['local']}/24 (plain {cnt['plain']}/24, xi 0.5 r_M {cnt['const']}/24): {'PASS' if cnt['local'] >= 15 else 'FAIL'}; beside, xi_loc(a) one value {cnt['at_a']}/24; Fornax pred {dl[fi]['pred_U2']:.1f} (obs 11.7), xi_loc(a) {dl[fi]['xi_at_a_U2']:.3g} vs r_M/2 {dl[fi]['rM_half_U2']:.3g} kpc")
    P("    xi_loc(a)/(r_M/2) per dwarf at Upsilon 2: " + ", ".join(f"{x['name']} {x['xi_at_a_U2'] / x['rM_half_U2']:.2g}{'*' if x['passed'] else ''}" for x in dl))
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
    if loc: gb = G * Mi / r ** 2; X = xi_loc(r, nu(gb / a0) * gb, a0 / KAP, XCLIP)
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
    if xs: x = np.concatenate(xs); out.update(xi_pct=[float(v) for v in np.percentile(x, [5, 50, 95])], frac_clip=float(np.mean(x >= XCLIP * 0.999)), mass_ratio=[float(min(mr)), float(np.median(mr)), float(max(mr))])
    return out
R1S = {"canonical": 0.0021, "alt": -0.0006}
for foot, a0 in A0.items():
    base = run(a0, "plain"); cst = run(a0, "const"); loc = run(a0, "local"); d0 = cst["rms"] - base["rms"]; d = loc["rms"] - base["rms"]
    ok = MUT or abs(round(d0, 4) - R1S[foot]) < 1e-9; fail += not ok; P(f"R1 SPARC [{foot}] constant 0.5 r_M: d rms {d0:+.4f} (KT25 {R1S[foot]:+.4f}): {'PASS' if ok else 'FAIL'}")
    t3 = d <= 0.005 and abs(loc["med"]) <= 0.05; RES[f"sparc|{foot}"] = dict(plain={k: base[k] for k in ("rms", "med", "med_inner")}, local={k: v for k, v in loc.items() if k != "per_gal"}, d_rms=d, ok=bool(t3))
    P(f"T3 SPARC [{foot}] plain rms {base['rms']:.4f} med {base['med']:+.4f} inner {base['med_inner']:+.4f}; local rms {loc['rms']:.4f} med {loc['med']:+.4f} inner {loc['med_inner']:+.4f}; d rms {d:+.4f}: {'PASS' if t3 else 'FAIL'}")
    P(f"    xi_loc at data points 5/50/95 % {loc['xi_pct'][0]:.3g}/{loc['xi_pct'][1]:.3g}/{loc['xi_pct'][2]:.3g} kpc, clipped {loc['frac_clip']:.3f}; total mass ratio min/med/max {loc['mass_ratio'][0]:.3f}/{loc['mass_ratio'][1]:.3f}/{loc['mass_ratio'][2]:.3f}")
    w = sorted(((loc["per_gal"][k] - base["per_gal"][k], GAL[k]["name"]) for k in range(len(GAL))), reverse=True)[:6]; P("    largest per-galaxy rms rises: " + "; ".join(f"{n} {v:+.3f}" for v, n in w)); RES[f"sparc|{foot}"]["worst"] = w
for foot in A0SI:
    bad = [t for t, ok in (("Cassini", RES[f"cassini|{foot}"]["ok"]), ("dwarfs", RES[f"dwarf_ok|{foot}"]), ("SPARC", RES[f"sparc|{foot}"]["ok"])) if not ok]
    lab = ("LOCAL RULE SURVIVES ON ALT" if not bad else "LOCAL RULE FAILS ON ALT: " + ", ".join(bad)) if foot == "alt" else "already FAILS (MW, KT26)" + ("" if not bad else "; also fails here: " + ", ".join(bad))
    RES[f"label|{foot}"] = lab; P(f"LABEL [{foot}]: {lab}")
RES["fail"] = fail; P(f"failed checks: {fail}")
sfx = "_MUTATE" if MUT else ""; open(os.path.join(HERE, f"kt27{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"kt27{sfx}.json"), "w"), indent=1, default=float)
sys.exit(1 if (MUT or fail) else 0)
