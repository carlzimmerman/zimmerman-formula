"""AGB3, POST HOC (written after AGB3's numbers were seen; not in FROZEN_CRITERIA.md; carries no frozen word).

How noisy are the photometric star-formation ages, and what does that do to D2, U and J2?
The half-template fork of the criteria is a stress test with no number behind it. This script puts a number on it
with witnesses that do not share the host photometry's noise:
  A. Supernova stretch. Fast-declining (low-stretch) supernovae come from old stars. Their share is tabulated
     against the two-component age; it reads no magnitude.
  B. Reliability. With W the two-component age, and two witnesses Z1, Z2 whose own errors are independent of W's
     (stretch x1 and host mass), the variance of what the three share is cov(W,Z1) cov(W,Z2) / cov(Z1,Z2), all inside
     redshift bins. What is left of var(W) is counted as noise. That is an UPPER bound on the noise: real age
     information that the star-formation rate holds and stretch and mass do not is counted as noise too. Host colour
     in the place of mass shares photometry with W and gives the other end of the bracket.
     Inside a fit the reliability is 1 - noise / (template variance left after the fit's other columns), and the
     noise-corrected amplitude is A / reliability. Errors by bootstrap over supernovae (fit and reliability redone).
  C. Part J's arithmetic with the corrected amplitudes as the prior (grids of agb3_S.json).
  D. Stretch against redshift and survey, as a check on the sample's age drift.
Writes agb3_posthoc_noise.json; log to agb3_posthoc_noise.out."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = ["agb3_run.py", "none"]; sys.path.insert(0, HERE)
import numpy as np
import agb3_run as R
import agb3_twocomp as T2
import agb2_joint as J2

d = R.DES(); out = {}; log = lambda s: print(s, flush=True)
age_all = T2.age(d.lm, d.ls, d.z); lowx_all = (d.x1 < -1).astype(float)

# ---- A. stretch against the two-component age (DES hosts)
m = d.mask("des_only"); z, x1, age = d.z[m], d.x1[m], age_all[m]
log("A. share of low-stretch supernovae (x1 < -1) against the host's two-component age, DES hosts:")
rows = []
for lo, hi in zip([0, 0.5, 1, 2, 3, 4, 5, 7], [0.5, 1, 2, 3, 4, 5, 7, 12]):
    s = (age >= lo) & (age < hi); f = float((x1[s] < -1).mean()); e = float(np.sqrt(f*(1 - f)/s.sum()))
    rows.append(dict(age=[lo, hi], n=int(s.sum()), share=f, err=e, mean_x1=float(x1[s].mean())))
    log(f"   age {lo:4.1f}-{hi:4.1f} Gyr: n {s.sum():4d}  share {f:.3f} +- {e:.3f}  mean x1 {x1[s].mean():+.2f}")
sl = np.polyfit(age, (x1 < -1).astype(float), 1); out["A"] = dict(rows=rows, line=[float(sl[1]), float(sl[0])])
log(f"   straight line: share = {sl[1]:.3f} + {sl[0]:.4f} per Gyr")

# ---- B. reliability and the corrected amplitudes
w = 1.0/d.err[m]**2; n = int(m.sum()); b = R.bins_of(z, 20); B = np.zeros((n, 20)); B[np.arange(n), b] = 1.0
lm, col, c = d.lm[m], d.col[m], d.c[m]; low = (lm < 10).astype(float); lowx = (x1 < -1).astype(float)
y = R.yvec(d, m, "R"); T = -0.030*age


def wres(v, cols, ww):
    X = np.column_stack(cols); XW = X.T*ww
    return v - X@np.linalg.solve(XW@X, XW@v)


def cv(a, bb, ww):
    return float((ww*a*bb).sum()/ww.sum())


def pipeline(idx, z1, z2):
    """Fit amplitudes, noise variance and inside-fit reliabilities on the rows idx."""
    ww = w[idx]; Bi = B[idx]; Bi = Bi[:, Bi.sum(0) > 0]
    W, Z1, Z2 = (wres(v[idx], [Bi], ww) for v in (age, z1, z2))
    vx = cv(W, Z1, ww)*cv(W, Z2, ww)/cv(Z1, Z2, ww); vw = cv(W, W, ww); vu = vw - vx
    res = dict(rel=vx/vw, noise_sd=float(np.sqrt(max(vu, 0.0))))
    for name, cols in (("D2", [Bi, x1[idx], c[idx], low[idx] - 0.5]), ("U", [Bi, x1[idx], c[idx]])):
        X = np.column_stack(cols + [T[idx]]); XW = X.T*ww; beta = np.linalg.solve(XW@X, XW@y[idx])
        Wr = wres(age[idx], cols, ww); rel = 1 - vu/cv(Wr, Wr, ww)
        res[name] = (float(beta[-1]), float(rel), float(beta[-1]/rel))
    return res


rng = np.random.default_rng(20261116); allidx = np.arange(n); out["B"] = {}
log("\nB. reliability of the two-component age (inside redshift bins) and noise-corrected amplitudes (bootstrap of 500):")
for key, lab, z1, z2 in (("x1_mass", "stretch + host mass (upper bound on the noise)", x1, lm), ("lowx_mass", "low-stretch flag + host mass", lowx, lm),
                         ("x1_colour", "stretch + host colour (shares photometry with the age)", x1, col)):
    p0 = pipeline(allidx, z1, z2); bs = [pipeline(rng.integers(0, n, n), z1, z2) for _ in range(500)]
    sd = lambda f: float(np.std([f(q) for q in bs], ddof=1))
    o = dict(reliability=[p0["rel"], sd(lambda q: q["rel"])], noise_sd_gyr=p0["noise_sd"])
    log(f"  witnesses: {lab}")
    log(f"     reliability {p0['rel']:.3f} +- {o['reliability'][1]:.3f}; noise {p0['noise_sd']:.2f} Gyr rms against a spread of {np.sqrt(cv(wres(age, [B], w), wres(age, [B], w), w)):.2f} Gyr")
    for name in ("D2", "U"):
        a, rel, ac = p0[name]; e_a = sd(lambda q: q[name][0]); e_rel = sd(lambda q: q[name][1]); e_c = sd(lambda q: q[name][2])
        o[name] = dict(A=a, sd_A=e_a, rel_in_fit=rel, sd_rel=e_rel, A_corrected=ac, sd_A_corrected=e_c, D_A0=(ac/e_c)**2, D_A1=((ac - 1)/e_c)**2)
        log(f"     {name:2s}: fitted A {a:+.3f} +- {e_a:.3f}; reliability inside the fit {rel:.3f} +- {e_rel:.3f}; corrected A {ac:+.3f} +- {e_c:.3f}"
            f"   dchi2(A=0) {o[name]['D_A0']:.1f}  dchi2(A=1) {o[name]['D_A1']:.1f}")
    out["B"][key] = o

# ---- C. Part J with the corrected amplitudes as the prior
S = json.load(open(os.path.join(HERE, "agb3_S.json"))); Af, An = np.array(J2.GRID_F), np.array(J2.GRID_N); out["C"] = {}
log("\nC. Part J's arithmetic with the corrected amplitude as the prior on A_H:")
for key in ("x1_mass", "x1_colour"):
    for name in ("U", "D2"):
        o = out["B"][key][name]
        for gk in ("full_sfr", "des_only_sfr"):
            g = S["grids"][gk]; r = J2.joint(Af, np.array(g["f"]), np.array(g["q0"]), An, np.array(g["n"]), np.array(g["t"]), o["A_corrected"], o["sd_A_corrected"])
            out["C"][f"{key}_{name}_{gk}"] = r
            log(f"   prior {name} corrected with {key} ({o['A_corrected']:+.3f} +- {o['sd_A_corrected']:.3f}) on {gk}: joint A_H {r['A']:+.3f}, q0 {r['q0']:+.3f},"
                f" q0 = 0: dchi2 {r['D_today']:.2f}; never accelerated: dchi2 {r['D_never']:.1f}")

# ---- D. stretch against redshift and survey
log("\nD. low-stretch share and mean two-component age by sample and redshift (stretch selection is not corrected):")
out["D"] = []
for lab, s in (("legacy, z < 0.1", d.ids != 10), ("DES 0.07-0.3", (d.ids == 10) & (d.z <= 0.3)), ("DES 0.3-0.5", (d.ids == 10) & (d.z > 0.3) & (d.z <= 0.5)),
               ("DES 0.5-0.7", (d.ids == 10) & (d.z > 0.5) & (d.z <= 0.7)), ("DES 0.7-1.14", (d.ids == 10) & (d.z > 0.7))):
    f = float(lowx_all[s].mean()); e = float(np.sqrt(f*(1 - f)/s.sum())); implied = (f - sl[1])/sl[0]
    out["D"].append(dict(sample=lab, n=int(s.sum()), share=f, err=e, mean_age=float(age_all[s].mean()), age_from_stretch=float(implied)))
    log(f"   {lab:16s} n {s.sum():4d}  low-stretch share {f:.3f} +- {e:.3f}  mean x1 {d.x1[s].mean():+.2f} | mean two-component age {age_all[s].mean():.2f} Gyr;"
        f" age the DES stretch line would give for that share: {implied:.1f} Gyr")
json.dump(out, open(os.path.join(HERE, "agb3_posthoc_noise.json"), "w"), indent=1, default=float)
log("\nwrote agb3_posthoc_noise.json")
