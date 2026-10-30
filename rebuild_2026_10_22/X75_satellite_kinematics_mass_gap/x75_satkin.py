#!/usr/bin/env python3
"""X75_satellite_kinematics_mass_gap: satellite line-of-sight dispersions around GAMA G09 centrals (G3C spec z, GKV M*),
graded against route E's smooth-core halos (EM1 SPARC M200, shifted by a common log M200 offset) and the isolated law.
Frozen criteria: FROZEN_CRITERIA.md (e7dfee54b9). Halo and law machinery: X53's committed script, executed read-only
(smooth shape patched as X74). One thread.
kappa = 1/2 FITTED; c_f EXTERNAL; footings never pooled; not theory closed; nothing here says the data favour the framework.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x75_satkin.py            [X75_MUTATE=1 -> shuffled dv control]
"""
import os, sys, io, json, math, time, contextlib, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
os.environ.pop("X53_MUTATE", None)
import numpy as np, pandas as pd
from scipy.optimize import minimize
from scipy.spatial import cKDTree

T0 = time.time()
MUT = os.environ.get("X75_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
MAXNFOF = int(os.environ.get("X75_MAXNFOF", "0"))                     # AMENDMENT A1 (post-result, reported only); 0 = frozen sample
if MAXNFOF: TAG += f"_A1_nfof{MAXNFOF}"
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
EXT = os.path.join(os.path.dirname(REPO), "_external_data")
OUT, CHK = [], {}
RES = dict(lane="X75_satellite_kinematics_mass_gap", criteria="e7dfee54b9", mutate=MUT,
           settings="kappa = 1/2 FITTED; c_f EXTERNAL; footings never pooled; not theory closed")


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, val):
    CHK[name] = bool(ok); P(f"  {name}: {'PASS' if ok else 'FAIL'}  ({val})")


# ============================================================ X53 machinery (read-only), Burkert and smooth
X53D = os.path.join(REB, "X53_outer_lensing_law_vs_halos"); X53SRC = os.path.join(X53D, "x53_outer_lensing.py")
T53 = open(X53SRC).read(); base = T53[:T53.index("for foot in FOOTS:\n    P(f\"\\n=== [{foot}]")]
SMOOTH = (("def B(x):\n    x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)\n",
           "def B(x):\n    x = np.asarray(x, float)\n    return 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))\n"),
          ("    return 4.0 / (3.0 * B1) * cf ** 1.25\n", "    return 4.0 / (3.0 * B1) * cf ** 1.25 * B1 / float(B(1.0))\n"),
          ("(St / r0t) * r0t ** 3 / ((r + r0t) * (r * r + r0t * r0t))", "(St / r0t) * r0t ** 3 / (r * r + r0t * r0t) ** 1.5"))


def load_ns(shape):
    src = base
    if shape == "S":
        for a, b in SMOOTH:
            assert src.count(a) == 1; src = src.replace(a, b)
    ns = {"__file__": X53SRC, "__name__": "x53_ro"}; argv0 = sys.argv; sys.argv = [X53SRC]
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        exec(compile(src, X53SRC, "exec"), ns)
    sys.argv = argv0
    orig = ns["halo_setup"]; bgb = ns["BG"]
    ns["halo_setup"] = lambda foot, lmb, cfg: orig(foot, lmb + cfg.get("dlM", 0.0) / bgb[cfg["bg"]]["b"], cfg)
    return ns


NS = {"S": load_ns("S"), "B": load_ns("B")}
N0 = NS["S"]
Gpc, H_NAT, OM_NAT, chi_flat, FOOTS = N0["Gpc"], N0["H_NAT"], N0["NF"]["OM_NAT"], N0["NF"]["chi_flat"], N0["FOOTS"]
HP = dict(N0["H_PRIMARY"])
P(f"X75_satellite_kinematics_mass_gap{' [MUTATE: shuffled dv control, not physics]' if MUT else ''}  criteria e7dfee54b9")
P(f"X53 machinery loaded read-only (smooth + Burkert); native h {H_NAT}, Omega_m {OM_NAT}  [{time.time() - T0:.0f} s]")

# ============================================================ data
g3 = pd.read_csv(os.path.join(EXT, "cfg519_work", "G3CGalv10.csv"))
gk = pd.read_csv(os.path.join(EXT, "gama_dr4_gkv", "gkv_stellarmass_g09.csv"), usecols=["CATAID", "logmstar"])
g3 = g3[(g3.RA > 125) & (g3.RA < 145) & (g3.Z > 0.002) & (g3.Z < 0.6)].reset_index(drop=True)
g3 = g3.merge(gk.drop_duplicates("CATAID"), on="CATAID", how="left")
ra, dec, z = g3.RA.values, g3.Dec.values, g3.Z.values
CKMS = 299792.458
DH = CKMS / (100 * H_NAT)                                                   # Mpc
DA = DH * chi_flat(z, OM_NAT) / (1 + z)                                     # native angular diameter distance, Mpc
qDA = chi_flat(z, OM_NAT) / chi_flat(z, 0.3)
lm = np.where(g3.logmstar.values > 5, g3.logmstar.values + 2 * np.log10(0.70 / H_NAT) + 2 * np.log10(qDA), np.nan)
xyz = np.c_[np.cos(np.radians(dec)) * np.cos(np.radians(ra)), np.cos(np.radians(dec)) * np.sin(np.radians(ra)), np.sin(np.radians(dec))]
TR = cKDTree(xyz)
P(f"G3C rows near G09 {len(g3)}; with GKV mass {np.isfinite(lm).sum()}")


def neigh(i, Rmpc):
    idx = np.array(TR.query_ball_point(xyz[i], 2 * math.sin(Rmpc / DA[i] / 2)), int); idx = idx[idx != i]
    R = DA[i] * np.arccos(np.clip(xyz[idx] @ xyz[i], -1, 1)); dv = CKMS * (z[idx] - z[i]) / (1 + z[i])
    return idx, R, dv


BINS = [8.5, 10.3, 10.6, 10.8, 11.0]
host_ok = np.zeros(len(g3), bool)
for i in np.where((z >= 0.05) & (z <= 0.25) & np.isfinite(lm) & (lm >= BINS[0]) & (lm <= BINS[-1]))[0]:
    buf = math.degrees(1.0 / DA[i])
    if not (129 + buf / math.cos(math.radians(dec[i])) < ra[i] < 141 - buf / math.cos(math.radians(dec[i])) and -2 + buf < dec[i] < 3 - buf):
        continue
    idx, R, dv = neigh(i, 1.0)
    near = (np.abs(dv) < 2000) & np.isfinite(lm[idx])
    if np.any(lm[idx][near] > lm[i]):
        continue
    host_ok[i] = True
if MAXNFOF:
    grp = pd.read_csv(os.path.join(EXT, "cfg519_work", "G3CFoFGroupv10.csv"), usecols=["GroupID", "Nfof"])
    nf = g3[["GroupID"]].merge(grp, on="GroupID", how="left").Nfof.fillna(1).values
    host_ok &= (g3.GroupID.values == 0) | (nf <= MAXNFOF)
    P(f"AMENDMENT A1 (post-result, reported only): hosts restricted to ungrouped or N_fof <= {MAXNFOF}")
H = np.where(host_ok)[0]
# pairs; a galaxy within 2000 km/s of two hosts goes to the nearer in R
best = {}
for i in H:
    idx, R, dv = neigh(i, 0.3)
    m = (R >= 0.05) & (R <= 0.30) & (np.abs(dv) < 2000)
    for j, Rj, dvj in zip(idx[m], R[m], dv[m]):
        if host_ok[j]:
            continue
        if j not in best or Rj < best[j][1]:
            best[j] = (i, Rj, dvj)
pairs = np.array([(v[0], v[1], v[2]) for v in best.values()]) if best else np.zeros((0, 3))
ph, pR, pdv = pairs[:, 0].astype(int), pairs[:, 1], pairs[:, 2]
if MUT:
    pdv = np.random.default_rng(1).uniform(-2000, 2000, len(pdv))
hbin = np.digitize(lm[H], BINS) - 1; pbin = np.digitize(lm[ph], BINS) - 1
P(f"hosts {len(H)} per bin {[int((hbin == b).sum()) for b in range(4)]}; pairs {len(ph)} per bin {[int((pbin == b).sum()) for b in range(4)]}  [{time.time() - T0:.0f} s]")
RES["counts"] = dict(hosts=[int((hbin == b).sum()) for b in range(4)], pairs=[int((pbin == b).sum()) for b in range(4)])

# ============================================================ measurement
VERR2 = 2 * 50.0 ** 2; VW = 2000.0


def fit_sigma(dv, w=None):
    w = np.ones_like(dv) if w is None else w
    def nll(p):
        s, f = math.exp(p[0]), 1 / (1 + math.exp(-p[1]))
        g = np.exp(-0.5 * dv ** 2 / s ** 2) / (math.sqrt(2 * math.pi) * s * math.erf(VW / (math.sqrt(2) * s)))
        return -np.sum(w * np.log(f * g + (1 - f) / (2 * VW)))
    r = min((minimize(nll, [math.log(s0), 0.0], method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-8, maxiter=4000)) for s0 in (80, 150, 300)), key=lambda r: r.fun)
    s2 = math.exp(r.x[0]) ** 2 - VERR2
    return math.sqrt(max(s2, 1.0)), 1 / (1 + math.exp(-r.x[1]))


rng = np.random.default_rng(0)
dvs = rng.normal(0, 150, 3000); dvs = np.r_[np.sqrt(150 ** 2 + VERR2) / 150 * dvs, rng.uniform(-VW, VW, 1500)]
sk, _ = fit_sigma(dvs); check("K1_synthetic_sigma", abs(sk / 150 - 1) < 0.03, f"{sk:.1f} vs 150")

ph_host = {h: k for k, h in enumerate(H)}
meas = {}
for wmode in ("pair", "host"):
    sig, err, frac = [], [], []
    for b in range(4):
        m = pbin == b
        hs = ph[m]; uh, inv, cnt = np.unique(hs, return_inverse=True, return_counts=True)
        w = np.ones(m.sum()) if wmode == "pair" else 1.0 / cnt[inv]
        s, f = fit_sigma(pdv[m], w)
        bs = []
        for k in range(1000 if wmode == "pair" else 300):
            pick = rng.integers(0, len(uh), len(uh)); c = np.bincount(pick, minlength=len(uh))
            wk = w * c[inv]
            if wk.sum() < 5: continue
            bs.append(fit_sigma(pdv[m], wk)[0])
        sig.append(s); err.append(float(np.std(bs))); frac.append(f)
    meas[wmode] = dict(sigma=sig, err=err, gauss_frac=frac)
    P(f"  measured sigma ({wmode}-weighted): " + ", ".join(f"bin{b + 1} {sig[b]:.1f}+-{err[b]:.1f} (f_gauss {frac[b]:.2f})" for b in range(4)) + f"  [{time.time() - T0:.0f} s]")
RES["measured"] = meas

# tracer slope gamma per bin (|dv|<500 minus scaled 1000-2000 sideband)
RE = np.logspace(math.log10(0.05), math.log10(0.30), 6); RC = np.sqrt(RE[1:] * RE[:-1]); AREA = math.pi * np.diff(RE ** 2)
GAM, WCNT = [], {}
for b in range(4):
    m = pbin == b
    inn = np.histogram(pR[m & (np.abs(pdv) < 500)], RE)[0]; sb = np.histogram(pR[m & (np.abs(pdv) > 1000)], RE)[0] * (1000 / 2000)
    S = np.clip(inn - sb, 0.5, None) / AREA
    sl = np.polyfit(np.log(RC), np.log(S), 1)[0]; GAM.append(float(1 - sl))
P(f"  tracer gamma per bin: {np.round(GAM, 2).tolist()}")
RES["gamma"] = GAM
for i in H:
    WCNT[i] = 0
for h_, d_ in zip(ph, pdv):
    if abs(d_) < 500: WCNT[h_] += 1

# ============================================================ Jeans prediction (vectorised over mass profiles)
SEL = (N0["RGRID_PC"] >= 1e3) & (N0["RGRID_PC"] <= 1e7); RG = N0["RGRID_PC"][SEL]
DRG = np.diff(RG)
KER = {}


def kernel(Rlo, Rhi):
    key = (Rlo, Rhi)
    if key not in KER:
        Rp = np.logspace(math.log10(Rlo), math.log10(Rhi), 24); A = np.zeros((24, len(RG))); Bm = np.zeros_like(A)
        for k, R in enumerate(Rp):
            u = np.where(RG > R * 1.0005)[0]; r = RG[u]; g = 2 * r / np.sqrt(r * r - R * R)
            w = np.zeros(len(u)); w[1:] += 0.5 * np.diff(r); w[:-1] += 0.5 * np.diff(r)
            A[k, u] = w * g; Bm[k, u] = w * g * R * R / r ** 2
        wR = np.zeros(24); wR[1:] += 0.5 * np.diff(Rp); wR[:-1] += 0.5 * np.diff(Rp)
        KER[key] = (A, Bm, wR * Rp)
    return KER[key]


def sigma2_ap(M, gam, beta=0.0, Rlo=5e4, Rhi=3e5):
    """aperture sigma_los^2 (km/s)^2 for enclosed masses M (N, len RG) [Msun], tracer n ~ r^-gam, constant beta."""
    M = np.atleast_2d(M); n = RG ** -gam
    f = n * RG ** (2 * beta) * Gpc * M / RG ** 2
    seg = 0.5 * (f[:, 1:] + f[:, :-1]) * DRG
    I = np.concatenate([np.cumsum(seg[:, ::-1], axis=1)[:, ::-1], np.zeros((len(M), 1))], axis=1)
    nsr2 = I / RG ** (2 * beta)                                   # n * sigma_r^2
    A, Bm, wR = kernel(Rlo, Rhi)
    num = nsr2 @ (A - beta * Bm).T; den = A @ n                   # (N, 24), (24,)
    return (num @ wR) / (den @ wR)


Msis = (200.0 ** 2) * RG / Gpc
s_sis = math.sqrt(float(sigma2_ap(Msis, 2.0)[0]))
check("K2_jeans_SIS", abs(s_sis / (200 / math.sqrt(2)) - 1) < 0.01, f"{s_sis:.2f} vs {200 / math.sqrt(2):.2f}")
LGRID = np.round(np.arange(8.5, 11.31, 0.05), 2)
SH = np.round(np.arange(-0.5, 1.2001, 0.01), 2)
Mt, _ = NS["S"]["mass_H"]("canonical", 10.7, H_NAT, dict(HP, dlM=0.0)); Mt2, _ = NS["S"]["mass_H"]("canonical", 10.7, H_NAT, HP)
check("K3_shift0_identity", float(np.max(np.abs(Mt / Mt2 - 1))) == 0.0, "mass_H at dlM 0 == X53/X74 smooth")
# variant specs: label -> (beta, dgamma, Rhi)
SPECS = {"primary": (0.0, 0.0, 3e5), "beta-0.3": (-0.3, 0.0, 3e5), "beta+0.3": (0.3, 0.0, 3e5), "gamma-0.5": (0.0, -0.5, 3e5),
         "gamma+0.5": (0.0, 0.5, 3e5), "aperture 50-200": (0.0, 0.0, 2e5)}


def tables(foot, ns, cfg, specs, law=False):
    """{spec: array (4 bins, LGRID[, SH]) of sigma_ap^2}; masses built once per LGRID row."""
    out = {sp: np.empty((4, len(LGRID)) + (() if law else (len(SH),))) for sp in specs}
    for a, l in enumerate(LGRID):
        if law:
            l70 = l - 2 * np.log10(0.70 / H_NAT); lmc = l + (-0.69 * l70 + 6.63)
            M = ns["NF"]["meff_profile"](foot, l, 0.5, 0.0, "zero", logMcold=lmc)[0][SEL][None, :]
        else:
            M = np.array([ns["mass_H"](foot, l, H_NAT, dict(cfg, dlM=float(s)))[0][SEL] for s in SH])
        for sp in specs:
            be, dg, Rhi = SPECS[sp]
            for b in range(4):
                v = sigma2_ap(M, GAM[b] + dg, be, Rhi=Rhi)
                out[sp][b, a] = v[0] if law else v
    return out


def stack(tab_b, b, wmode="pair"):
    hs = H[hbin == b]; w = np.array([WCNT[i] for i in hs], float)
    if wmode == "host": w = (w > 0).astype(float)
    if tab_b.ndim == 1:
        return math.sqrt(np.sum(w * np.interp(lm[hs], LGRID, tab_b)) / w.sum())
    v = np.array([np.interp(lm[hs], LGRID, tab_b[:, k]) for k in range(tab_b.shape[1])])
    return np.sqrt(v @ w / w.sum())


def grade(tabH, tabL, wmode="pair"):
    ms, me = np.array(meas[wmode]["sigma"]), np.array(meas[wmode]["err"])
    pred = np.array([stack(tabH[b], b, wmode) for b in range(4)])
    chi = (((pred - ms[:, None]) / me[:, None]) ** 2).sum(0); k = int(np.argmin(chi)); D = float(SH[k])
    ok = chi <= chi[k] + 1; lo, hi = float(SH[ok].min()), float(SH[ok].max())
    perbin = [float(SH[int(np.argmin(np.abs(pred[b] - ms[b])))]) for b in range(4)]
    k0 = int(np.argmin(np.abs(SH)))
    lawp = np.array([stack(tabL[b], b, wmode) for b in range(4)])
    return dict(D=D, lo=lo, hi=hi, sD=0.5 * (hi - lo), chi2_min=float(chi[k]), chi2_H0=float(chi[k0]), pred_H0=pred[:, k0].tolist(),
                pred_best=pred[:, k].tolist(), perbin_D=perbin, law_pred=lawp.tolist(), chi2_L=float((((lawp - ms) / me) ** 2).sum()),
                edge=bool(k in (0, len(SH) - 1)))


def cls(g):
    D, s = g["D"], max(g["sD"], 1e-3)
    if abs(D) < 2 * s and D < 0.30 - 2 * s: return "KINEMATICS SIDE WITH SPARC"
    if D > 2 * s and abs(D - 0.40) < 2 * s + 0.10: return "KINEMATICS SIDE WITH LENSING"
    if abs(D) > 2 * s and abs(D - 0.40) > 2 * s + 0.10: return "KINEMATICS REQUIRE A DIFFERENT MASS"
    return "NOT DECIDED"


RES["footings"] = {}
for foot in FOOTS:
    sp_all = list(SPECS) if not MUT else ["primary"]
    tS = tables(foot, NS["S"], HP, sp_all); tL = tables(foot, NS["S"], HP, sp_all, law=True)
    g = grade(tS["primary"], tL["primary"]); g["class"] = cls(g)
    P(f"\n=== [{foot}] PRIMARY (smooth, pair-weighted, beta 0): common dlogM200 {g['D']:+.2f} [{g['lo']:+.2f}, {g['hi']:+.2f}]; chi2 min {g['chi2_min']:.1f}, at 0 {g['chi2_H0']:.1f}; law chi2 {g['chi2_L']:.1f}")
    P(f"   measured {np.round(meas['pair']['sigma'], 1).tolist()}; pred at 0 {np.round(g['pred_H0'], 1).tolist()}; best {np.round(g['pred_best'], 1).tolist()}; law {np.round(g['law_pred'], 1).tolist()}; per-bin D {g['perbin_D']}")
    P(f"   CLASS [{foot}]: {g['class']}  [{time.time() - T0:.0f} s]")
    rep = {}
    if not MUT:
        vs = [(sp, tS[sp], tL[sp], "pair") for sp in SPECS if sp != "primary"] + [("host-weighted", tS["primary"], tL["primary"], "host")]
        tB = tables(foot, NS["B"], HP, ["primary"]); vs.append(("Burkert", tB["primary"], tL["primary"], "pair"))
        tG = tables(foot, NS["S"], dict(HP, bg="B_cfg886_bg"), ["primary"]); vs.append(("EM1 bg B", tG["primary"], tL["primary"], "pair"))
        NS["S"]["MUT"] = True                                            # A2 (post-result, reported only): halo to 100 R200
        tU = tables(foot, NS["S"], HP, ["primary"]); NS["S"]["MUT"] = False; vs.append(("A2 untruncated", tU["primary"], tL["primary"], "pair"))
        for lab, th, tl, wm in vs:
            gv = grade(th, tl, wm); gv["class"] = cls(gv); rep[lab] = gv
            P(f"   (reported) {lab:16s}: D {gv['D']:+.2f} [{gv['lo']:+.2f}, {gv['hi']:+.2f}] chi2 {gv['chi2_min']:.1f} (at 0 {gv['chi2_H0']:.1f}; law {gv['chi2_L']:.1f}) -> {gv['class']}")
    g["reported"] = rep; RES["footings"][foot] = g
    P(f"   [{time.time() - T0:.0f} s, RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB]")
if MUT:
    # per bin: amplitude collapsed, sigma at the fit floor, or a Gaussian wider than the +-2000 window (indistinguishable from the floor)
    check("MUTATE_shuffle_collapses", all(f < 0.2 or s <= 1.0 or s > VW for f, s in zip(meas["pair"]["gauss_frac"], meas["pair"]["sigma"])),
          f"f_gauss {np.round(meas['pair']['gauss_frac'], 2).tolist()}, sigma {np.round(meas['pair']['sigma'], 1).tolist()}")
V = {f: RES["footings"][f]["class"] for f in FOOTS}
RES["verdict"] = V["canonical"] if V["canonical"] == V["alt"] else f"FOOTINGS DISAGREE: {V}"
RES["checks"] = CHK; n = sum(CHK.values())
P(f"\n=== VERDICT: {RES['verdict']}\nchecks {n}/{len(CHK)}; runtime {time.time() - T0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB")
json.dump(RES, open(os.path.join(HERE, f"x75_satkin_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"x75_satkin{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n == len(CHK) else 1)
