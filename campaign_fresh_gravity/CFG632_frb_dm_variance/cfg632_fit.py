#!/usr/bin/env python3
"""CFG632 fit (FROZEN_CRITERIA.md secs. 4-8): the FRB DM-z scatter of the Sharma+26 sample (extended, N = 114) vs the framework's
census-gas sigma_DM(z) from cfg632_predict.json.  The authors' eq. 1 likelihood (log-normal DM_cosmic, log-normal rest-frame host,
MW halo 50) re-implemented in numpy; amplitude sigma_DM = A sigma_v(z); flat ln A prior; host (mu, s) marginalised on a grid.

  nice -n 10 python3 -I cfg632_fit.py                  -> cfg632_fit.out / .json   (census verdict + power gate + C1/C2/K1-K3)
  CFG632_MUTATE=1 nice -n 10 python3 -I cfg632_fit.py  -> cfg632_fit_MUTATE.out / .json  (MU1 f_ret = 1, MU2 f_ret = 0.01 on real data)

kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "2")
import csv, json, math, sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cfg632_predict as PR  # noqa: E402  (constants, mean DM, kernel, profile code for K1-K3)

MUT = os.environ.get("CFG632_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
DATA = Path(os.environ.get("CFG632_DATA", str(HERE.parents[2] / "_external_data" / "frb_sharma26" / "repo")))
OUT = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

PRED = json.load(open(HERE / "cfg632_predict.json"))
ZG = np.array(PRED["z"])

# ------------------------------------------------------------------ data
def load_sample(which="extended"):
    rows = list(csv.DictReader(open(DATA / "data" / "frb_results" / "frb_sample.csv")))
    keep = ("yes", "unclear") if which == "extended" else ("yes",)
    rows = [r for r in rows if r["sharma_sample"].strip() in keep]
    dm = np.array([float(r["DMexgal"]) for r in rows]); z = np.array([float(r["z_sample"]) for r in rows])
    return dm, z, [r["FRB"] for r in rows]

# ------------------------------------------------------------------ likelihood grids
LNA = np.arange(-2.5, 2.5 + 1e-9, 0.02)
MU = np.linspace(4.0, 6.0, 41); SH = np.linspace(0.2, 1.0, 33)
MUg, SHg = np.meshgrid(MU, SH, indexing="ij"); MUf, SHf = MUg.ravel(), SHg.ravel()
NHB = 400

def lognorm_pdf(x, mu_log, s):
    x = np.maximum(x, 1e-300)
    return np.exp(-0.5 * ((np.log(x) - mu_log) / s) ** 2) / (x * s * math.sqrt(2 * math.pi))

def host_matrices(dm, z, mwh=50.0):
    """per FRB: host bins (obs frame), width, host pdf matrix H[x, (mu, s)]."""
    out = []
    for d, zz in zip(dm, z):
        mx = max(1.0, d - mwh)
        x = 1e-2 + (mx - 1e-2) * np.linspace(0, 1, NHB); w = max((mx - 1e-2) / NHB, 1e-12)
        xr = x * (1 + zz)
        H = lognorm_pdf(xr[:, None], MUf[None, :], SHf[None, :]) * (1 + zz)
        out.append((x, w, H))
    return out

def loglike_grid(dm, z, mean, sig, hm, mwh=50.0):
    """returns log L[lnA, host] summed over FRBs.  mean, sig: arrays per FRB (sig is the A = 1 sigma)."""
    tot = np.zeros((len(LNA), len(MUf)))
    for i, (d, zz) in enumerate(zip(dm, z)):
        x, w, H = hm[i]
        dc = d - x - mwh                                              # DM_cosmic values
        s = np.exp(LNA)[:, None] * sig[i]
        v = s ** 2; m = mean[i]
        sl = np.sqrt(np.log1p(v / m ** 2)); ml = np.log(m ** 2 / np.sqrt(m ** 2 + v))
        C = np.where(dc[None, :] > 0, lognorm_pdf(np.maximum(dc, 1e-300)[None, :], ml, sl), 0.0)
        C = np.clip(np.nan_to_num(C), 1e-300, None)
        with np.errstate(all="ignore"):
            L = (C * w) @ H
        tot += np.log(np.maximum(L, 1e-300))
    return tot

def posterior_lnA(LL):
    mx = LL.max(); P = np.exp(LL - mx).sum(1); P /= P.sum()
    c = np.cumsum(P)
    q = lambda p: float(np.interp(p, c, LNA))
    return q(0.5), q(0.16), q(0.84), P

def zscore(m, p16, p84):
    if m < 0: return m / max(p84 - m, 1e-9)
    return m / max(m - p16, 1e-9)

def sig_interp(key, z):
    return np.interp(z, ZG, np.array(PRED["cases"][key]["sigma"]))

def mean_dm(z, imf="chabrier"):
    if imf == "chabrier":
        return np.interp(z, ZG, np.array(PRED["mean_dm"]))
    fd = PR.f_d(ZG, "salpeter"); zz = np.linspace(0, 2.3, 500); f = np.interp(zz, ZG, fd)
    integ = PR.NE0 * f * (1 + zz) * PR.C_KMS / (100 * PR.h * PR.Ez(zz)) * (PR.MPC_CM / PR.PC_CM)
    cum = np.concatenate([[0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(zz))])
    return np.interp(z, zz, cum)

def fit(dm, z, key_or_sig, hm, mwh=50.0, imf="chabrier"):
    sig = sig_interp(key_or_sig, z) if isinstance(key_or_sig, str) else key_or_sig
    LL = loglike_grid(dm, z, mean_dm(z, imf), sig, hm, mwh)
    m, lo, hi, P = posterior_lnA(LL)
    ib = np.unravel_index(np.argmax(LL), LL.shape)
    return dict(m=m, p16=lo, p84=hi, Z=zscore(m, lo, hi), maxLL=float(LL.max()),
                host_best=(float(MUf[ib[1]]), float(SHf[ib[1]])), lnA_best=float(LNA[ib[0]]))

def draw_mock(rng, z, mean, sig, mu=5.0, s=0.5, mwh=50.0):
    v = sig ** 2; sl = np.sqrt(np.log1p(v / mean ** 2)); ml = np.log(mean ** 2 / np.sqrt(mean ** 2 + v))
    cos = np.exp(ml + sl * rng.standard_normal(len(z)))
    host = np.exp(mu + s * rng.standard_normal(len(z))) / (1 + z)
    return cos + host + mwh

def bin_of(Zn, Zf):
    a = abs(Zn)
    if a >= 3: return "EXCLUDED"
    if a >= 2: return "TENSION"
    return "CONSISTENT (interval-limited)" if abs(Zf) >= 2 else "CONSISTENT"

CENSUS_VARS = [f"{r}|{p}|{o}" for r in ("lo", "hi") for p in ("H", "BETA") for o in ("DIFF", "SHELL")]
CTRL_VARS = ["lo|H|DIFF", "hi|H|DIFF", "lo|BETA|DIFF", "hi|H|SHELL"]
FOOTS = ("canonical", "alt")

def main():
    t0 = time.time()
    say(f"CFG632 fit{' (MUTATE)' if MUT else ''} -- FROZEN_CRITERIA.md. kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
    dm, z, names = load_sample("extended")
    say(f"sample: extended (yes + unclear) N = {len(dm)}; z median {np.median(z):.3f} max {z.max():.3f}; DMexgal median {np.median(dm):.1f}")
    hm = host_matrices(dm, z)
    res = dict(lane="CFG632", mutate=MUT, N=len(dm), footings={})
    if MUT:
        for foot in FOOTS:
            r = {}
            for mode in ("one", "dep"):
                fits = {v: fit(dm, z, f"{foot}|{mode}|{v}", hm) for v in CTRL_VARS}
                Zs = [f["Z"] for f in fits.values()]
                Zn = min(Zs, key=abs); Zf = max(Zs, key=abs)
                lab = "MU1 f_ret=1" if mode == "one" else "MU2 f_ret=0.01"
                for v, f in fits.items():
                    say(f"  {foot:9s} {lab:15s} {v:14s} lnA {f['m']:+.3f} ({f['p16']:+.3f}, {f['p84']:+.3f})  Z {f['Z']:+.2f}  maxLL {f['maxLL']:.2f}")
                excl = abs(Zn) >= 3
                say(f"{foot:9s} {lab}: Z_near {Zn:+.2f} Z_far {Zf:+.2f} -> {bin_of(Zn, Zf)}; tooth {'BITES (EXCLUDED)' if excl else 'DOES NOT BITE'}")
                r[mode] = dict(fits=fits, Z_near=Zn, Z_far=Zf, bin=bin_of(Zn, Zf), excluded=excl)
            r["teeth"] = bool(r["one"]["excluded"] and r["dep"]["excluded"])
            say(f"{foot:9s} TEETH: {'YES (both controls EXCLUDED)' if r['teeth'] else 'NO -- the test has no teeth against ' + ', '.join(k for k in ('one', 'dep') if not r[k]['excluded'])}")
            res["footings"][foot] = r
        json.dump(res, open(HERE / f"cfg632_fit{TAG}.json", "w"), indent=1, default=float)
        open(HERE / f"cfg632_fit{TAG}.out", "w").write("\n".join(OUT) + "\n")
        sys.exit(0 if all(res["footings"][f]["teeth"] for f in FOOTS) else 1)

    # ---------------- K1 kernel
    y = np.geomspace(1e-8, 1, 2000)
    k1 = float(np.max(np.abs(PR.nu_mono(y) - 1 / (-np.expm1(-np.sqrt(y))))))
    k1r = float(np.max(np.abs(PR.nu_mono(y) * (-np.expm1(-np.sqrt(y))) - 1)))
    say(f"K1 kernel: max |nu_mono - nu_exp| (y<1) = {k1:.2e} abs, {k1r:.2e} rel -> {'PASS' if k1 < 1e-4 else 'FAIL'} (tol 1e-4)")
    res["K1"] = dict(abs=k1, rel=k1r, pass_=k1 < 1e-4)
    # ---------------- K2 projection: real space vs Fourier, one 1e14 census halo
    zt = 0.25; hb = PR.halo_basics(1e14, zt)
    fr = PR.fret_of(math.log10(hb["Mta"])); Mb = fr * PR.FB * hb["Mta"] / PR.h; a0 = PR.A0MPC["canonical"]
    re = math.sqrt(PR.G * Mb / a0) / math.log1p(fr * PR.FB / (1 - PR.FB)); re = min(re, hb["rta"] / PR.h / (1 + zt))
    r200c = hb["r200c"] / PR.h / (1 + zt); Ms = min(PR.moster_mstar(hb["M200c"] / PR.h, zt), Mb); Mg = Mb - Ms
    rho, ne = PR.hydro_profiles(np.array([Mg]), np.array([Ms]), np.array([0.015 * r200c / (1 + math.sqrt(2))]), np.array([re]), a0,
                                np.array([0.5 * math.sqrt(PR.G * Mb * a0)]))
    edges = re * PR.XG[None, :]
    Qr = float(PR.column_sq_integral(rho, edges)[0])
    kk = np.geomspace(1e-3 / re, 3e3 / re, 6000)
    u = PR.u_of_k(rho, edges, kk)[0]
    Qk = float(np.trapz(kk * (Mg * u) ** 2 / (2 * math.pi), kk))
    say(f"K2 projection (1e14 Msun/h, z 0.25, canonical): real {Qr:.4e} vs Fourier {Qk:.4e} Msun^2/Mpc^2 -> ratio {Qk / Qr:.4f} {'PASS' if abs(Qk / Qr - 1) < 0.02 else 'FAIL'}")
    res["K2"] = dict(real=Qr, fourier=Qk, ratio=Qk / Qr, pass_=abs(Qk / Qr - 1) < 0.02)
    k3 = max(PRED["cases"][k]["norm_err_max"] for k in PRED["cases"] if "|H|" in k)
    say(f"K3 profile normalisation: max |M_gas(<r_edge)/M_gas - 1| over H profiles = {k3:.2e} -> {'PASS' if k3 < 1e-6 else 'FAIL'}")
    res["K3"] = dict(max=k3, pass_=k3 < 1e-6)

    # ---------------- C1 reproduction (context only)
    npz = np.load(DATA / "data" / "frb_results" / "DMvar_Sharma2026.npz")
    sig_pub = np.interp(z, npz["z"], npz["median"])
    c1 = fit(dm, z, sig_pub, hm)
    i3 = np.argmin(abs(npz["z"] - 0.3)); band = (npz["p16"][i3] / npz["median"][i3], npz["p84"][i3] / npz["median"][i3])
    A = math.exp(c1["m"]); rep = band[0] <= A <= band[1]
    say(f"C1 reproduction (CONTEXT ONLY): authors' median sigma_DM(z) shape x A -> A_hat {A:.3f} (lnA {c1['m']:+.3f} [{c1['p16']:+.3f}, {c1['p84']:+.3f}]),"
        f" their band at z 0.3 [{band[0]:.3f}, {band[1]:.3f}] -> {'REPRODUCED' if rep else 'NOT REPRODUCED'}; host best (mu, s) = {c1['host_best']}")
    res["C1"] = dict(fit=c1, A_hat=A, band=band, reproduced=rep)

    # ---------------- power gate + C2 (forecast; mocks, host truth (5.0, 0.5))
    rng = np.random.default_rng(632)
    for foot in FOOTS:
        kc = f"{foot}|census|lo|H|DIFF"; mean = mean_dm(z); sc = sig_interp(kc, z)
        lc, wc, cover = [], [], 0
        for j in range(200):
            dmm = draw_mock(rng, z, mean, sc)
            f = fit(dmm, z, kc, host_matrices(dmm, z))
            lc.append(f["m"]); wc.append(0.5 * (f["p84"] - f["p16"])); cover += (f["p16"] <= 0 <= f["p84"])
        sig_f = float(np.median(wc)); med_c = float(np.median(lc))
        sep = {}
        for mode in ("one", "dep"):
            kx = f"{foot}|{mode}|lo|H|DIFF"; sx = sig_interp(kx, z); lx = []
            for j in range(100):
                dmm = draw_mock(rng, z, mean, sx)
                lx.append(fit(dmm, z, kc, host_matrices(dmm, z))["m"])
            sep[mode] = dict(median_lnA=float(np.median(lx)), S=abs(float(np.median(lx)) - med_c) / sig_f)
        gate = sep["one"]["S"] >= 2 and sep["dep"]["S"] >= 2
        cov = cover / 200
        say(f"{foot:9s} POWER GATE (forecast): sigma_f(lnA) {sig_f:.3f}; census mocks median lnA {med_c:+.3f};"
            f" MU1 median {sep['one']['median_lnA']:+.3f} S {sep['one']['S']:.2f}; MU2 median {sep['dep']['median_lnA']:+.3f} S {sep['dep']['S']:.2f}"
            f" -> {'PASSES' if gate else 'FAILS: NON-DIAGNOSTIC'}   [{time.time()-t0:.0f}s]")
        say(f"{foot:9s} C2 recovery: 68% coverage {cov:.3f} -> {'PASS' if 0.55 <= cov <= 0.81 else 'FAIL'}; bias median lnA {med_c:+.3f}")
        res["footings"][foot] = dict(gate=dict(sigma_f=sig_f, census_median=med_c, sep=sep, passes=gate), C2=dict(coverage=cov, bias=med_c))

    # ---------------- verdict on the real data
    for foot in FOOTS:
        fits = {v: fit(dm, z, f"{foot}|census|{v}", hm) for v in CENSUS_VARS}
        for v, f in fits.items():
            say(f"  {foot:9s} census {v:16s} lnA {f['m']:+.3f} ({f['p16']:+.3f}, {f['p84']:+.3f})  A {math.exp(f['m']):.3f}  Z {f['Z']:+.2f}  maxLL {f['maxLL']:.2f}  host {f['host_best']}")
        Zs = [f["Z"] for f in fits.values()]
        Zn = min(Zs, key=abs); Zf = max(Zs, key=abs); Zp = fits["lo|H|DIFF"]["Z"]
        g = res["footings"][foot]["gate"]["passes"]
        b = bin_of(Zn, Zf); bp = bin_of(Zp, Zp)
        side = "data scatter BELOW the census prediction" if fits["lo|H|DIFF"]["m"] < 0 else "data scatter ABOVE the census prediction"
        verdict = b if g else f"NON-DIAGNOSTIC (would read {b})"
        say(f"{foot:9s} VERDICT: Z_primary {Zp:+.2f} ({bp}); Z_near {Zn:+.2f}; Z_far {Zf:+.2f} -> {verdict}; {side}")
        res["footings"][foot].update(fits=fits, Z_primary=Zp, Z_near=Zn, Z_far=Zf, bin=b, bin_primary=bp, verdict=verdict, side=side)
        # sensitivity (no verdict weight)
        kc = f"{foot}|census|lo|H|DIFF"; sens = {}
        for lab, kw, sample in (("MW halo 30", dict(mwh=30.0), None), ("MW halo 80", dict(mwh=80.0), None),
                                ("Salpeter f_d", dict(imf="salpeter"), None), ("yes-only N=92", {}, "yes")):
            if sample:
                d2, z2, _ = load_sample(sample); f = fit(d2, z2, kc, host_matrices(d2, z2))
            elif "mwh" in kw:
                f = fit(dm, z, kc, host_matrices(dm, z, kw["mwh"]), mwh=kw["mwh"])
            else:
                f = fit(dm, z, kc, hm, **kw)
            sens[lab] = f
            say(f"  {foot:9s} sensitivity {lab:14s} lnA {f['m']:+.3f} ({f['p16']:+.3f}, {f['p84']:+.3f})  Z {f['Z']:+.2f}")
        res["footings"][foot]["sensitivity"] = sens
    json.dump(res, open(HERE / f"cfg632_fit{TAG}.json", "w"), indent=1, default=float)
    open(HERE / f"cfg632_fit{TAG}.out", "w").write("\n".join(OUT) + "\n")

if __name__ == "__main__":
    main()
