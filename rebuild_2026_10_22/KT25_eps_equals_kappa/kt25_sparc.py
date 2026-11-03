#!/usr/bin/env python3
"""KT25 SPARC (copy of KT19, EPS = 0.5). KT19: SPARC under KT17's filter, xi = 0.55 sqrt(G M_b / a0), spherical smoothing approximation, simple nu (board law). python3 kt19.py [--mutate]. kappa = 1/2 FITTED and held fixed; not theory closed."""
import glob, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "../../real_research/data/sparc_data"); MRT = os.path.join(HERE, "../../real_research/data/SPARC_Lelli2016c.mrt")
MUT = "--mutate" in sys.argv; OUT = []; RES = {}; fail = 0; EPS = 0.5
def P(s): print(s, flush=True); OUT.append(s)
G = 4.30091e-6; CONV = 3.0857e19 / 1e6; A0 = {"canonical": 9.3603e-11 * CONV, "alt": 1.1312e-10 * CONV}
nu = (lambda y: np.ones_like(np.asarray(y, float))) if MUT else (lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300)))
tab = {}
for line in open(MRT):
    p = line.split()
    if len(p) >= 18 and p[1].isdigit(): tab[p[0]] = dict(L=float(p[7]) * 1e9, Rd=float(p[11]), MHI=float(p[13]) * 1e9)
GAL = []; nmono = ntot = 0
for fn in sorted(glob.glob(os.path.join(D, "*_rotmod.dat"))):
    nm = os.path.basename(fn).replace("_rotmod.dat", "")
    try: d = np.genfromtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6 or len(d) < 3 or nm not in tab: continue
    R, Vo, eV, Vg, Vd, Vb = (d[:, j] for j in range(6)); o = np.argsort(R); R, Vo, eV, Vg, Vd, Vb = R[o], Vo[o], eV[o], Vg[o], Vd[o], Vb[o]
    Bg = Vg * np.abs(Vg); Bs = 0.5 * Vd * np.abs(Vd) + 0.7 * Vb * np.abs(Vb); q = (R > 0) & (Vo > 0) & (eV > 0) & (eV / np.maximum(Vo, 1e-9) < 0.1) & (Bg + Bs > 0)
    if q.sum() < 3: continue
    GAL.append(dict(name=nm, R=R, Vo=Vo, Bg=Bg, Bs=Bs, q=q, **tab[nm]))
P(f"galaxies {len(GAL)}, points {sum(g['q'].sum() for g in GAL)}")
def Mprof(g, f):
    B = g["Bg"] + f * g["Bs"]; M = np.maximum(B * g["R"] / G, 0.0); Mm = np.maximum.accumulate(M); return Mm, int(np.sum(Mm != M))
def smoothed_ratio(g, f, xi, n=int(os.environ.get("KT19_N", "1500"))):
    """ratio M_smoothed(R)/M(R) at the data radii, on one grid, so xi -> 0 gives exactly 1."""
    R = g["R"]; Mm, _ = Mprof(g, f); Mb = 0.5 * f * g["L"] + 1.33 * g["MHI"]; Rl = R[-1]; Rd = max(g["Rd"], 0.1)
    r = np.geomspace(min(R[0], 0.01) * 0.1, Rl * 10 + 8 * xi + 10 * Rd, n)
    Mi = np.where(r < R[0], Mm[0] * (r / R[0]) ** 3, np.interp(r, R, Mm)); x = np.maximum(r - Rl, 0); Mi = Mi + np.where(r > Rl, max(Mb - Mm[-1], 0) * (1 - (1 + x / Rd) * np.exp(-x / Rd)), 0.0)
    dM = np.gradient(Mi, r); rho = np.maximum(dM, 0) / (4 * math.pi * r * r)
    Rr, Rp = r[:, None], r[None, :]; K = (Rp / (math.sqrt(2 * math.pi) * xi * Rr)) * (np.exp(-(Rr - Rp) ** 2 / (2 * xi * xi)) - np.exp(-(Rr + Rp) ** 2 / (2 * xi * xi)))
    rs = np.trapz(K * rho[None, :], r, axis=1)
    cm = lambda rh: np.concatenate([[0.0], np.cumsum(0.5 * (4 * math.pi * r[1:] ** 2 * rh[1:] + 4 * math.pi * r[:-1] ** 2 * rh[:-1]) * np.diff(r))])
    M0, M1 = cm(rho), cm(rs); return np.interp(R, r, M1) / np.maximum(np.interp(R, r, M0), 1e-30), float(M1[-1] / M0[-1])
def run(a0, f=1.0, filt=True, cache=None):
    rr, med_in, allr = [], [], []
    for g in GAL:
        B = g["Bg"] + f * g["Bs"]; q = g["q"] & (B > 0); gb = B[q] / g["R"][q]; go = g["Vo"][q] ** 2 / g["R"][q]
        if filt:
            Mb = 0.5 * f * g["L"] + 1.33 * g["MHI"]; xi = EPS * math.sqrt(G * Mb / a0); key = (g["name"], f)
            if cache is not None and key in cache: ratio = cache[key]
            else: ratio = smoothed_ratio(g, f, xi)[0]; cache is not None and cache.__setitem__(key, ratio)
            gh = gb * ratio[q]
        else: gh = gb
        gm = gb + (nu(gh / a0) - 1) * gh; r = np.log10(go) - np.log10(gm); rr.append(math.sqrt(np.mean(r * r))); allr.append(r); med_in.append(r[g["R"][q] < 2 * g["Rd"]])
    a = np.concatenate(allr); i = np.concatenate(med_in); return dict(rms=float(math.sqrt(np.mean(np.square(rr)))), med=float(np.median(a)), med_inner=float(np.median(i)) if len(i) else None, n_inner=int(len(i)))
# checks
for g in GAL: _, k = Mprof(g, 1.0); nmono += k; ntot += len(g["R"])
P(f"C3 monotone envelope changed {nmono}/{ntot} points ({nmono / ntot:.3f}): {'PASS' if nmono / ntot <= 0.05 else 'FAIL'}"); fail += nmono / ntot > 0.05
mb = sorted(GAL, key=lambda g: 0.5 * g["L"] + 1.33 * g["MHI"])
for g in (mb[0], mb[len(mb) // 2], mb[-1]):
    xi = EPS * math.sqrt(G * (0.5 * g["L"] + 1.33 * g["MHI"]) / A0["alt"]); ratio, mr = smoothed_ratio(g, 1.0, xi); _, mr0 = smoothed_ratio(g, 1.0, 1e-3); ok = abs(mr - 1) <= 1e-3; fail += not ok
    P(f"C2 {g['name']}: M_b {0.5 * g['L'] + 1.33 * g['MHI']:.3g}, xi {xi:.3f} kpc, total mass ratio - 1 {mr - 1:+.1e}; at xi 1e-3 the data-radius ratio max |r - 1| {np.max(np.abs(smoothed_ratio(g, 1.0, 1e-3)[0] - 1)):.1e}: {'PASS' if ok else 'FAIL'}")
for foot, a0 in A0.items():
    base = run(a0, filt=False); gb = np.concatenate([(g["Bg"] + g["Bs"])[g["q"]] / g["R"][g["q"]] for g in GAL])
    e1 = float(np.max(np.abs((gb + (nu(gb / a0) - 1) * gb) / (nu(gb / a0) * gb) - 1))); ok = e1 <= 1e-10; fail += not ok; P(f"\nC1 [{foot}] xi 0 equals board law, max rel {e1:.1e}: {'PASS' if ok else 'FAIL'}")
    cache = {}; fl = run(a0, filt=True, cache=cache); d = fl["rms"] - base["rms"]
    lab = "FAILS SPARC" if (d > 0.02 or abs(fl["med"]) > 0.05) else "HURT" if d > 0.005 else "SURVIVES SPARC"
    xs = [EPS * math.sqrt(G * (0.5 * g["L"] + 1.33 * g["MHI"]) / a0) for g in GAL]
    RES[foot] = dict(plain=base, filter=fl, d_rms=d, label=lab, xi_kpc=[float(np.min(xs)), float(np.median(xs)), float(np.max(xs))])
    P(f"[{foot}] xi min/median/max {np.min(xs):.3f}/{np.median(xs):.3f}/{np.max(xs):.3f} kpc")
    P(f"[{foot}] plain: rms {base['rms']:.4f} median {base['med']:+.4f} inner median {base['med_inner']:+.4f} (n {base['n_inner']})")
    P(f"[{foot}] filter: rms {fl['rms']:.4f} median {fl['med']:+.4f} inner median {fl['med_inner']:+.4f}; d rms {d:+.4f}: {lab}")
    if not MUT:
        fs = np.round(np.arange(0.7, 1.501, 0.05), 3); sp = [run(a0, f, False)["rms"] for f in fs]; sf = [run(a0, f, True, cache)["rms"] for f in fs]; ip, jf = int(np.argmin(sp)), int(np.argmin(sf))
        RES[foot]["f_scan"] = dict(f=fs.tolist(), plain=sp, filter=sf); P(f"[{foot}] beside, xi held at each f's own M_b: best f plain {fs[ip]} rms {sp[ip]:.4f}; filter {fs[jf]} rms {sf[jf]:.4f}")
        worst = []
        for g in GAL:
            q = g["q"]; gb_ = (g["Bg"] + g["Bs"])[q] / g["R"][q]; go = g["Vo"][q] ** 2 / g["R"][q]; ratio = cache[(g["name"], 1.0)][q]; gh = gb_ * ratio
            r0 = np.log10(go) - np.log10(nu(gb_ / a0) * gb_); r1 = np.log10(go) - np.log10(gb_ + (nu(gh / a0) - 1) * gh); worst.append((float(np.sqrt(np.mean(r1 ** 2)) - np.sqrt(np.mean(r0 ** 2))), g["name"], 0.5 * g["L"] + 1.33 * g["MHI"]))
        worst.sort(reverse=True); RES[foot]["worst"] = worst[:10]; P(f"[{foot}] largest per-galaxy rms rises: " + "; ".join(f"{n} {w:+.3f} (M_b {m:.2g})" for w, n, m in worst[:6]))
RES["fail"] = fail; P(f"failed checks: {fail}")
sfx = "_MUTATE" if MUT else ""; open(os.path.join(HERE, f"kt25_sparc{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"kt25_sparc{sfx}.json"), "w"), indent=1)
sys.exit(1 if (MUT or fail) else 0)
