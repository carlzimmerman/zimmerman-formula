#!/usr/bin/env python3
"""P1D4_m6_native_3d_forest: X57's M6 at its bound vs DESI DR1 P1D (z 2.2-4.4) with a framework-native 3D forest model
(forest3d.py). FROZEN_CRITERIA.md + forest3d.py committed alone first (f05be7280b).

kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating w ~ 0 field component, never a particle;
not theory closed; nothing here says the data favour the framework.
Run:  PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I p1d4_m6_3d.py      (P1D4_MUTATE=1 twin)
Preemptible: tables checkpointed per (footing, z) under tables{TAG}/ (not committed); SIGTERM exits after the current table.
"""
import os, sys, json, math, time, resource, hashlib, tarfile, io, signal, gc
os.environ.setdefault("OMP_NUM_THREADS", "1")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
from scipy.interpolate import RegularGridInterpolator, interp1d
from scipy.optimize import minimize, brentq
from scipy.stats import chi2 as CHI2
from astropy.io import fits
import forest3d as F3

MUT = os.environ.get("P1D4_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
RAW = os.path.join(REPO, "_external_data", "desi_dr1_p1d_qmle", "raw", "data_points.tar")
TDIR = os.path.join(HERE, f"tables{TAG}")
os.makedirs(TDIR, exist_ok=True)
T0 = time.time()
OUT = open(os.path.join(HERE, f"p1d4_m6_3d{TAG}.out"), "a")
STOP = {"flag": False}
signal.signal(signal.SIGTERM, lambda *a: STOP.update(flag=True))
RES = {"lane": "P1D4_m6_native_3d_forest", "criteria": "f05be7280b", "mutate": MUT, "checks": {},
       "settings": "kappa = 1/2 FITTED; footings never pooled; cold dark energy = gravitating field component, never a particle; not theory closed"}


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); OUT.write(s + "\n"); OUT.flush()


def check(name, ok, value, thr):
    RES["checks"][name] = {"pass": bool(ok), "value": value, "threshold": thr}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {value} | {thr}")


def rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9


def dump():
    RES["elapsed_s"] = time.time() - T0; RES["peak_rss_GB"] = rss()
    json.dump(RES, open(os.path.join(HERE, f"p1d4_m6_3d_results{TAG}.json"), "w"), indent=1, default=float)


FOOTS = ("canonical", "alt")
P("\n" + "=" * 100 + "\nP1D4_m6_native_3d_forest" + (" [MUTATE m1-m2: control output, not physics]" if MUT else "") +
  ": criteria f05be7280b; kappa = 1/2 FITTED; footings never pooled; no particle; not theory closed")

# ============================================================== data
P("\n== STEP 0 (stop rule)")
s0 = {"S0a": hashlib.md5(open(RAW, "rb").read()).hexdigest() == "33d7fc21bfd3d745ed71a0bbe80ca433"}
with tarfile.open(RAW) as tf:
    HD = fits.open(io.BytesIO(tf.extractfile("desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits").read()))
T = HD["P1D_BLIND"].data
Zall = np.round(np.asarray(T["Z"], float), 2); Kall = np.asarray(T["K"], float); Pall = np.asarray(T["PLYA"], float)
C_full = np.asarray(HD["COVARIANCE"].data, float); C_stat = np.asarray(HD["COVARIANCE_STAT"].data, float)
ZB = np.unique(Zall)
sd = np.sqrt(np.diag(C_full)); R = C_full / np.outer(sd, sd)
cross = np.abs(R[np.not_equal.outer(Zall, Zall)])
RES["cross_z_corr"] = {"max": float(cross.max()), "mean": float(cross.mean())}
CLIGHT, LLYA, DLAM = 299792.458, 1215.67, 0.8
BG = F3.Background()
NBOX, LBOX = 256, 64.0
KF = 2 * math.pi / LBOX
SEL = {}
for z in ZB:
    kmax = 0.5 * math.pi / (CLIGHT * DLAM / ((1 + z) * LLYA))
    kmin_box = 2 * KF / BG.cz(z)
    SEL[z] = np.where((Zall == z) & (Kall > 0.001) & (Kall < kmax) & (Kall >= kmin_box))[0]
check("K1", all(len(v) > 10 for v in SEL.values()), "bins per z " + ", ".join(f"{z}:{len(v)}" for z, v in SEL.items()) +
      f"; cross-z |r| max {RES['cross_z_corr']['max']:.3f} mean {RES['cross_z_corr']['mean']:.1e}", "DESI cut and k >= 2 k_f")

P1 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22/P1D1_m6_boera_high_z_forest/p1d1_m6_boera_results.json")))
X22 = json.load(open(os.path.join(REPO, "rebuild_2026_10_22/X22_cosmic_dust_window/x22_cosmic_dust_window_results.json")))
RL = X22["step2"]["per_footing"]["canonical"]["R_L_Mpc_h"][2]
FMAX = {f: X22["step2"]["per_footing"][f]["f_max"] for f in FOOTS}
M6 = {}
for f in FOOTS:
    dbi = BG.RRAT * (1 - FMAX[f])
    D3 = BG.Dz(3.0)
    kf_ = np.logspace(-4, 3, 4000)
    sh = kf_ ** (3 + BG.ns) * BG.Tk(kf_) ** 2
    s2R0 = BG.NORM * F3.trapz(sh * F3.W(kf_ * RL) ** 2, np.log(kf_))
    Fb3 = 0.2 * s2R0 * D3 ** 2 / (dbi ** 2 / (1 + dbi))
    M6[f] = {"delta_b_in": dbi, "f_V": Fb3 / (1 + dbi), "Fb_max_z3": Fb3}
ok_b, txt = [], []
for f in FOOTS:
    ref = P1["backgrounds"]["native"]["m6"][f]
    for key in ("delta_b_in", "f_V", "Fb_max_z3"):
        tgt = ref[key] * (1.01 if (MUT and f == "canonical" and key == "f_V") else 1.0)       # m2
        ok_b.append(round(M6[f][key], 4) == round(tgt, 4)); txt.append(f"{f} {key} {M6[f][key]:.5f}/{tgt:.5f}")
s0["S0b"] = all(ok_b)
P(f"  S0b P1D1 native M6 reproduced: {sum(ok_b)}/{len(ok_b)}")

# S0c Gaussian normalisation (z 3, R_J 0.1)
bx = F3.Box(NBOX, LBOX, 0, 2)
d, psi, var = bx.gaussian(BG, 3.0, 0.1)
Pg = (np.abs(bx.dx * np.fft.rfft(d, axis=2)) ** 2 / bx.L).mean(axis=(0, 1))
an = F3.p1d_analytic(BG, 3.0, 0.1, bx.kpar)
msk = (bx.kpar >= KF) & (bx.kpar <= 6.0)
s0c = float(np.max(np.abs(Pg[msk] / an[msk] - 1)))
s0["S0c"] = s0c <= 0.05
P(f"  S0c box Gaussian P1D vs analytic projection (k_f..6 h/Mpc): max |r-1| {s0c:.4f} (<= 0.05)")
del d, psi
# S0d patch fraction
s0d = []
for f in FOOTS:
    pf, fv = bx.patches(RL, M6[f]["f_V"], M6[f]["delta_b_in"], 1.0, 0.1)
    N1 = int(round(M6[f]["f_V"] * LBOX ** 3 / (4 * math.pi * RL ** 3 / 3)))
    tol = 3 * M6[f]["f_V"] / math.sqrt(N1) + 2 * M6[f]["f_V"] ** 2
    s0d.append(abs(fv - M6[f]["f_V"]) <= tol); P(f"  S0d {f}: covered {fv:.5f} vs f_V {M6[f]['f_V']:.5f} (N1 {N1}, tol {tol:.5f})")
    del pf
s0["S0d"] = all(s0d)
gc.collect()

# ============================================================== tables
GAM = [1.0, 1.3, 1.6]
RJS = [0.05, 0.12, 0.20]
MUS = [0.0, 0.25, 0.5, 1.0, 2.0]
BS = np.array([6.0, 9.0, 13.0, 18.0, 23.0, 29.0, 35.0])
FBS = np.linspace(0.15, 0.90, 10)
LGT = lambda x: np.log(x / (1 - x))


def model_at(bx, z, kv_box, Pk, kd):
    """log-log interpolation of mock P1D at box modes onto DESI k (km/s)."""
    m = kv_box > 0
    return np.exp(np.interp(np.log(kd), np.log(kv_box[m]), np.log(np.maximum(Pk[m], 1e-30))))


def build_table(foot, z, seed=0, dbi_scale=1.0, mus=MUS, only=None):
    """Table[gam, rj, mu, b, F, k] of P1D at DESI-selected k for one footing and z."""
    bxx = F3.Box(NBOX, LBOX, seed, 2)
    kd = Kall[SEL[z]]
    fz, cz = BG.fz(z), BG.cz(z)
    tab = np.zeros((len(GAM), len(RJS), len(mus), len(BS), len(FBS), len(kd)), np.float32)
    for j, rj in enumerate(RJS):
        if only is not None and rj != only[1]: continue
        dl, ps, vr = bxx.gaussian(BG, z, rj)
        Dad = np.exp(dl - vr / 2).astype(np.float32)
        for m, mu in enumerate(mus):
            if mu > 0:
                pf, _ = bxx.patches(RL, M6[foot]["f_V"], dbi_scale * M6[foot]["delta_b_in"], mu, rj)
                Dl = Dad * pf; del pf
            else:
                Dl = Dad
            for g, gam in enumerate(GAM):
                if only is not None and gam != only[0]: continue
                tr = F3.tau_redshift(Dl, ps, fz, gam, bxx.dx)
                for ib, b in enumerate(BS):
                    for iF, Fb in enumerate(FBS):
                        kv, Pk, _, _ = F3.flux_p1d(tr, b, Fb, cz, bxx.dx, bxx.L)
                        tab[g, j, m, ib, iF] = model_at(bxx, z, kv, Pk, kd)
                del tr
            del Dl
        del dl, ps, Dad
        gc.collect()
    del bxx; gc.collect()
    return tab


def direct(foot, z, gam, rj, mu, b, Fb, seed=0, dbi_scale=1.0):
    bxx = F3.Box(NBOX, LBOX, seed, 2)
    dl, ps, vr = bxx.gaussian(BG, z, rj)
    D = np.exp(dl - vr / 2).astype(np.float32)
    if mu > 0:
        pf, _ = bxx.patches(RL, M6[foot]["f_V"], dbi_scale * M6[foot]["delta_b_in"], mu, rj); D = D * pf
    tr = F3.tau_redshift(D, ps, BG.fz(z), gam, bxx.dx)
    kv, Pk, _, _ = F3.flux_p1d(tr, b, Fb, BG.cz(z), bxx.dx, bxx.L)
    out = model_at(bxx, z, kv, Pk, Kall[SEL[z]])
    del bxx, dl, ps, D, tr; gc.collect()
    return out


def table_path(foot, z):
    return os.path.join(TDIR, f"tab_{foot}_z{z:.1f}.npy")


DBS = -0.8 if MUT else 1.0                                                          # m1 (fit tables only)
P(f"\n== TABLES: {len(GAM)} gamma x {len(RJS)} R_J x {len(MUS)} mu x {len(BS)} b x {len(FBS)} Fbar per (footing, z); stride-2 skewers (16384)")
null_cache = {}
SHARD = os.environ.get("P1D4_SHARD")                                               # A2: "i/n" table-only worker
JOBS = [(f, z) for f in FOOTS for z in ZB]
if SHARD:
    si, sn = (int(v) for v in SHARD.split("/"))
    JOBS = [jz for k, jz in enumerate(JOBS) if k % sn == si]
for f, z in JOBS:
    if True:
        pth = table_path(f, z)
        if os.path.exists(pth):
            continue
        if STOP["flag"]:
            P("SIGTERM: tables checkpointed; rerun to resume."); dump(); sys.exit(0)
        t = time.time()
        if f == "alt" and os.path.exists(table_path("canonical", z)):
            # mu = 0 slice identical across footings (K2): compute mu > 0 only
            can = np.load(table_path("canonical", z))
            sub = build_table(f, z, dbi_scale=DBS, mus=MUS[1:])
            tab = np.concatenate([can[:, :, :1], sub], axis=2); del can, sub
        else:
            tab = build_table(f, z, dbi_scale=DBS)
        np.save(pth, tab)
        P(f"  table {f} z {z:.1f}: {time.time() - t:.0f} s, RSS {rss():.2f} GB")
        del tab; gc.collect()
if SHARD:
    P(f"  shard {SHARD}: tables done"); sys.exit(0)
missing = [(f, z) for f in FOOTS for z in ZB if not os.path.exists(table_path(f, z))]
if missing:
    P(f"STOP: {len(missing)} tables missing (shards unfinished)"); sys.exit(2)

TAB = {f: {z: np.load(table_path(f, z)) for z in ZB} for f in FOOTS}
k2 = max(float(np.max(np.abs(TAB["canonical"][z][:, :, 0] - TAB["alt"][z][:, :, 0]))) for z in ZB)
check("K2", k2 == 0.0, f"mu = 0 slices identical across footings (max diff {k2:.1e})", "== 0")

# interpolators in (b, logit F) on log P
INTP = {f: {z: {(g, j, m): RegularGridInterpolator((BS, LGT(FBS)), np.log(TAB[f][z][g, j, m]), method="cubic")
                for g in range(len(GAM)) for j in range(len(RJS)) for m in range(len(MUS))} for z in ZB} for f in FOOTS}


def model(f, z, g, j, m, b, Fb):
    return np.exp(INTP[f][z][(g, j, m)]([[b, LGT(Fb)]])[0])


# S0e interpolation check (direct vs interpolated), mu = 0, gamma 1.3, R_J 0.12
rng7 = np.random.default_rng(7)
s0e = 0.0
for z in ZB:
    for _ in range(5):
        b = float(rng7.uniform(BS[0] + 1, BS[-1] - 1)); Fb = float(rng7.uniform(FBS[0] + 0.03, FBS[-1] - 0.03))
        dirv = direct("canonical", z, 1.3, 0.12, 0.0, b, Fb)
        s0e = max(s0e, float(np.max(np.abs(model("canonical", z, 1, 1, 0, b, Fb) / dirv - 1))))
s0["S0e"] = s0e <= 0.015
P(f"  S0e interpolation vs direct (60 points): max |r-1| {s0e:.4f} (<= 0.015)")
check("S0", all(s0.values()), f"{s0}", "all Step-0 items")
RES["step0"] = {"items": s0, "S0b": txt, "S0c_maxdev": s0c, "S0e_maxdev": s0e}
if not all(s0.values()) and not MUT:
    P("STOP: Step 0 failed; nothing graded."); RES["verdict"] = "STOPPED AT STEP 0"; dump(); sys.exit(1)

# ============================================================== fitting
BLO, BHI = BS[0], BS[-1]


def fit_node(f, z, g, j, m, d, Ci):
    bb, FF = np.meshgrid(BS, FBS, indexing="ij")
    best = None
    for ib in range(len(BS)):
        for iF in range(len(FBS)):
            r = d - TAB[f][z][g, j, m, ib, iF]; c = float(r @ Ci @ r)
            if best is None or c < best[0]: best = (c, BS[ib], FBS[iF])
    fun = lambda x: (lambda r: float(r @ Ci @ r))(d - model(f, z, g, j, m, x[0], 1 / (1 + math.exp(-x[1]))))
    r = minimize(fun, [best[1], LGT(best[2])], method="L-BFGS-B", bounds=[(BLO, BHI), (LGT(FBS[0]), LGT(FBS[-1]))])
    if r.fun < best[0]:
        return float(r.fun), float(r.x[0]), float(1 / (1 + math.exp(-r.x[1])))
    return best


def prof_z(f, z, m, d, Ci):
    best = None
    for g in range(len(GAM)):
        for j in range(len(RJS)):
            c, b, Fb = fit_node(f, z, g, j, m, d, Ci)
            if best is None or c < best[0]: best = (c, g, j, b, Fb)
    return best


def covs(kind, mcvar=None, floor=False, f=None, nullpars=None):
    out = {}
    for z in ZB:
        idx = SEL[z]
        C = (C_stat if kind == "stat" else C_full)[np.ix_(idx, idx)].copy()
        if mcvar is not None: C += np.diag(mcvar[z])
        if floor:
            c, g, j, b, Fb = nullpars[z]
            C += np.diag((0.02 * model(f, z, g, j, 0, b, Fb)) ** 2)
        out[z] = np.linalg.inv(C)
    return out


def profile_mu(f, zs, Ci, data=None):
    prof = {}
    pars = {}
    for m, mu in enumerate(MUS):
        tot = 0.0; pz = {}
        for z in zs:
            d = Pall[SEL[z]] if data is None else data[z]
            pz[z] = prof_z(f, z, m, d, Ci[z]); tot += pz[z][0]
        prof[mu] = tot; pars[mu] = pz
    return prof, pars


def scan_stats(prof):
    mus = np.array(MUS); ch = np.array([prof[m] for m in MUS])
    ip = interp1d(mus, ch, kind="quadratic")
    fine = np.linspace(0, MUS[-1], 4001); cf = ip(fine)
    i = int(np.argmin(cf)); muh, cmin = float(fine[i]), float(cf[i])
    above = np.where((fine > muh) & (cf - cmin > 3.84))[0]
    mu95 = float(fine[above[0]]) if len(above) else None
    return {"mu_hat": muh, "chi2_min": cmin, "chi2_mu0": float(prof[0.0]), "chi2_mu1": float(prof[1.0]),
            "dchi2_1": float(prof[1.0] - cmin), "dchi2_0": float(prof[0.0] - cmin), "mu95": mu95, "grid": {str(k): v for k, v in prof.items()}}


def analyse(f, label, zs, Ci, planted=False):
    prof, pars = profile_mu(f, zs, Ci)
    c0 = prof[0.0]
    nb = sum(len(SEL[z]) for z in zs); dof = nb - 4 * len(zs)
    pj = float(CHI2.sf(c0, dof))
    perz = {}
    for z in zs:
        c, g, j, b, Fb = pars[0.0][z]
        dz = len(SEL[z]) - 4
        perz[f"{z:.1f}"] = {"chi2": c, "dof": dz, "p": float(CHI2.sf(c, dz)), "gamma": GAM[g], "R_J": RJS[j], "b": b, "Fbar": Fb}
    G0 = pj >= 0.01 and all(v["p"] >= 0.001 for v in perz.values())
    asim = {z: model(f, z, pars[0.0][z][1], pars[0.0][z][2], 0, pars[0.0][z][3], pars[0.0][z][4]) for z in zs}
    pa, _ = profile_mu(f, zs, Ci, asim)
    dA = pa[1.0] - pa[0.0]; G1 = dA >= 9
    sc = scan_stats(prof)
    cls = ("NOT DIAGNOSTIC (NATIVE 3D MODEL INADEQUATE)" if not G0 else "NOT DIAGNOSTIC (NUISANCE ABSORBS M6)" if not G1
           else "M6 AT X57's BOUND EXCLUDED" if sc["dchi2_1"] >= 9 else "M6-SHAPED EXCESS PRESENT" if sc["dchi2_0"] >= 9 else "NOT EXCLUDED")
    out = {"class": cls, "G0": {"pass": G0, "chi2": c0, "dof": dof, "p": pj, "per_z": perz}, "G1": {"pass": G1, "dchi2_asimov": dA},
           "scan": sc, "Fb_95": None if sc["mu95"] is None else sc["mu95"] * M6[f]["Fb_max_z3"]}
    worst = sorted(perz.items(), key=lambda kv: kv[1]["p"])[:3]
    P(f"  [{label}] {cls}")
    P(f"     G0 null chi2 {c0:.1f} / {dof} dof, p {pj:.3g}; worst z: " + ", ".join(f"z{z} {v['chi2']:.1f}/{v['dof']} p {v['p']:.2g} (gam {v['gamma']}, RJ {v['R_J']}, b {v['b']:.1f}, F {v['Fbar']:.3f})" for z, v in worst))
    P(f"     G1 Asimov {dA:.2f}; mu_hat {sc['mu_hat']:.3f}, dchi2(mu=1) {sc['dchi2_1']:.2f}, dchi2(mu=0) {sc['dchi2_0']:.2f}, mu95 {sc['mu95']}")
    return out, pars


RES["footings"] = {}
for f in FOOTS:
    P(f"\n== {f.upper()} footing")
    Ci1 = covs("full")
    _, pars1 = profile_mu(f, list(ZB), Ci1) if False else (None, {0.0: {z: prof_z(f, z, 0, Pall[SEL[z]], Ci1[z]) for z in ZB}})
    # MC variance from phase seeds 1, 2 at the pass-1 null best fit (A: computed once, shared by footings since mu = 0)
    if "mcvar" not in RES:
        mcvar = {}
        for z in ZB:
            c, g, j, b, Fb = pars1[0.0][z]
            v0 = model(f, z, g, j, 0, b, Fb)
            v1 = direct(f, z, GAM[g], RJS[j], 0.0, b, Fb, seed=1)
            v2 = direct(f, z, GAM[g], RJS[j], 0.0, b, Fb, seed=2)
            mcvar[z] = np.var(np.vstack([v0, v1, v2]), axis=0, ddof=1)
        RES["mcvar"] = {f"{z:.1f}": (np.sqrt(mcvar[z]) / Pall[SEL[z]]).tolist() for z in ZB}
        MCV = mcvar
        P("  MC rel. error (median per z): " + ", ".join(f"z{z:.1f} {np.median(np.sqrt(mcvar[z]) / Pall[SEL[z]]):.3f}" for z in ZB))
    Ci = covs("full", MCV)
    prim, pars = analyse(f, "PRIMARY", list(ZB), Ci)
    fr = {"primary": prim, "variants": {}}
    if f == "canonical":
        # K3 / K4: injection from DIRECT mocks with the footing's true positive patches (repairs the P1D3 twin flaw)
        rng = np.random.default_rng(0)
        pl1, pl0 = {}, {}
        for z in ZB:
            c, g, j, b, Fb = pars[0.0][z]
            inv = np.linalg.inv(Ci[z]); nz = rng.multivariate_normal(np.zeros(len(SEL[z])), inv)
            pl1[z] = direct(f, z, GAM[g], RJS[j], 1.0, b, Fb, dbi_scale=1.0) + nz
            pl0[z] = model(f, z, g, j, 0, b, Fb) + nz
        s1 = scan_stats(profile_mu(f, list(ZB), Ci, pl1)[0]); s0p = scan_stats(profile_mu(f, list(ZB), Ci, pl0)[0])
        G1 = prim["G1"]["pass"]
        fr["K3"] = {"pass": (0.5 <= s1["mu_hat"] <= 1.5 and s1["dchi2_0"] >= 9) if G1 else True, "vacuous": not G1, "scan": s1}
        fr["K4"] = {"pass": (s0p["mu95"] is not None and s0p["mu95"] < 1) if G1 else True, "vacuous": not G1, "scan": s0p}
        check("K3", fr["K3"]["pass"], f"planted mu=1 (true positive patches): mu_hat {s1['mu_hat']:.3f}, dchi2_0 {s1['dchi2_0']:.2f} (vacuous {not G1})", "mu_hat in [0.5,1.5], dchi2_0 >= 9 when G1 passes")
        check("K4", fr["K4"]["pass"], f"planted null: mu95 {s0p['mu95']} (vacuous {not G1})", "mu95 < 1 when G1 passes")
    fr["variants"]["V-stat"] = analyse(f, "V-stat", list(ZB), covs("stat", MCV))[0]
    fr["variants"]["V-floor2"] = analyse(f, "V-floor2", list(ZB), covs("full", MCV, floor=True, f=f, nullpars=pars[0.0]))[0]
    fr["variants"]["V-hiz"] = analyse(f, "V-hiz", [z for z in ZB if z >= 3.6 - 1e-9], Ci)[0]
    # reported: full-covariance chi2 at per-z null best fits
    idx = np.concatenate([SEL[z] for z in ZB])
    r = np.concatenate([Pall[SEL[z]] - model(f, z, pars[0.0][z][1], pars[0.0][z][2], 0, pars[0.0][z][3], pars[0.0][z][4]) for z in ZB])
    Cf = C_full[np.ix_(idx, idx)] + np.diag(np.concatenate([MCV[z] for z in ZB]))
    fr["full_cov_chi2_at_blockfit"] = float(r @ np.linalg.solve(Cf, r))
    flips = [k for k, v in fr["variants"].items() if v["class"] != prim["class"]]
    fr["verdict"] = prim["class"] + (" (ROBUST)" if not flips else f" (FRAGILE: flips in {', '.join(flips)})")
    P(f"  [reported] full-covariance null chi2 at block fits {fr['full_cov_chi2_at_blockfit']:.1f}")
    P(f"  ==> {f}: {fr['verdict']}")
    RES["footings"][f] = fr
    dump()

check("K5", rss() < 1.0, f"peak RSS {rss():.3f} GB, 1 thread, {time.time() - T0:.0f} s this session", "< 1 GB")
P("\n== VERDICT")
for f in FOOTS:
    P(f"  {f}: {RES['footings'][f]['verdict']}")
P(f"  checks {sum(v['pass'] for v in RES['checks'].values())}/{len(RES['checks'])}")
dump()
sys.exit(0 if all(v["pass"] for v in RES["checks"].values()) else 1)
