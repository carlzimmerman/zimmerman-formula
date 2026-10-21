#!/usr/bin/env python3
"""CFG943 shared code: read-only imports of the frozen DR4 code, the MOCK-sky generator (an exact replica of the frozen
make_population that also returns the per-star fields the R pair table needs), the class boosts, the pair table, the
RSS guard and the frozen-file hash guard.  FROZEN_CRITERIA.md section 3.  Nothing here edits a frozen file.
Every catalogue built here is a MOCK, never data."""
import sys
sys.dont_write_bytecode = True          # never write __pycache__ into the frozen / other-lane directories
import os, json, hashlib, resource, threading, contextlib, io
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PREP = os.path.join(ROOT, "prep_2026", "gaia_dr4_prep")
DR4R = os.path.join(PREP, "dr4_ready_1")
C825 = os.path.join(ROOT, "campaign_fresh_gravity", "CFG816_dr4_r_statistic_scoring")
C740 = os.path.join(ROOT, "campaign_fresh_gravity", "CFG740_sealed_wb_slope2")
for p in (PREP, DR4R, C825):
    if p not in sys.path:
        sys.path.insert(0, p)
import wide_binary_pipeline as W          # noqa: E402  frozen pipeline, read-only
import cfg816_r as R825                   # noqa: E402  CFG825 scorer, read-only (never its --dr3/--dr4 paths)
import arm_c_rows as ARMC                 # noqa: E402  release-day Arm C row tool (prints only)
import amdt14_distances as A14            # noqa: E402  release-day Amendment 14 tool (prints only)

RSS_LIMIT_MB = 900.0
CHUNK = 250_000
A0_R = R825.A0_PRIMARY                    # 1.2e-10, the R statistic's r_M scale
LSTAR_PC = json.load(open(os.path.join(C740, "cfg740_predictions.json")))["Lstar_pc"]   # 5.754399, read from the seal


def rss_mb():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / 1e6 if sys.platform == "darwin" else r / 1e3


def guard(where=""):
    m = rss_mb()
    if m > RSS_LIMIT_MB:
        sys.stderr.write(f"RSS GUARD: peak {m:.0f} MB > {RSS_LIMIT_MB} MB at {where}; aborting\n")
        os._exit(3)
    return m


def start_watchdog(period=1.0):
    def loop():
        while True:
            guard("watchdog")
            threading.Event().wait(period)
    t = threading.Thread(target=loop, daemon=True); t.start()


# ---------------------------------------------------------------- frozen-file hash guard (control K4)
FROZEN = [
    "prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md",
    "prep_2026/gaia_dr4_prep/wide_binary_pipeline.py",
    "prep_2026/gaia_dr4_prep/catalog_builder/build_catalog.py",
    "prep_2026/gaia_dr4_prep/catalog_builder/fetch_extract.py",
    "prep_2026/gaia_dr4_prep/dr4_ready_1/arm_c_rows.py",
    "prep_2026/gaia_dr4_prep/dr4_ready_1/amdt14_distances.py",
    "prep_2026/gaia_dr4_prep/dr4_ready_1/edge_table_dr4.json",
    "campaign_fresh_gravity/CFG740_sealed_wb_slope2/cfg740_predictions.json",
    "campaign_fresh_gravity/CFG800_wb_2026_scoring/FROZEN_CRITERIA.md",
    "campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/FROZEN_CRITERIA.md",
    "campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/cfg816_r.py",
    "campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/cfg816_r_results.json",
    "campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/cfg816_r_MUTATE_results.json",
    "campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/cfg816_r_dr3_results.json",
    "campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/cfg816_r_dr3.out",
]
DR4_SLOT = "campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/cfg816_r_dr4_results.json"


def frozen_hashes():
    h = {}
    for rel in FROZEN:
        h[rel] = hashlib.sha256(open(os.path.join(ROOT, rel), "rb").read()).hexdigest()
    for f in sorted(os.listdir(PREP)):
        if f.startswith("AMENDMENT") and f.endswith("_HASH.txt"):
            rel = f"prep_2026/gaia_dr4_prep/{f}"
            h[rel] = hashlib.sha256(open(os.path.join(ROOT, rel), "rb").read()).hexdigest()
    h["DR4_SLOT_EXISTS"] = os.path.exists(os.path.join(ROOT, DR4_SLOT))
    return h


# ---------------------------------------------------------------- MOCK generator: exact replica of W.make_population (+ extra fields)
def mock_population(N, rng, dr4=True, dmax_pc=250., smin_kAU=2., smax_kAU=30., Gcut=17., ecc='thermal'):
    """Same draws, same order, same arithmetic as wide_binary_pipeline.make_population (frozen); returns (frozen_dict, extra).
    Control K1 checks byte identity of every field the frozen function returns."""
    G, MSUN, KAU = W.G, W.MSUN, W.KAU
    M1 = rng.uniform(0.45, 1.25, N)
    q = rng.uniform(0.30, 1.00, N)
    M2 = np.clip(q * M1, 0.15, None)
    Mt = M1 + M2
    d = (rng.uniform(25. ** 3, dmax_pc ** 3, N)) ** (1 / 3.)
    p = -0.6
    lo, hi = (smin_kAU * 0.5) ** p, (smax_kAU * 2.0) ** p
    a_sma = (rng.uniform(hi, lo, N)) ** (1 / p) * KAU
    if ecc == 'thermal':
        e = np.sqrt(rng.uniform(0, 1, N))
    else:
        e = rng.uniform(0, 1, N)
    Ma = rng.uniform(0, 2 * np.pi, N); E = Ma.copy()
    for _ in range(60):
        E -= (E - e * np.sin(E) - Ma) / (1 - e * np.cos(E))
    n = np.sqrt(G * Mt * MSUN / a_sma ** 3)
    b_ = a_sma * np.sqrt(1 - e ** 2)
    xo, yo = a_sma * (np.cos(E) - e), b_ * np.sin(E)
    Ed = n / (1 - e * np.cos(E))
    vxo, vyo = -a_sma * np.sin(E) * Ed, b_ * np.cos(E) * Ed
    Om, w = rng.uniform(0, 2 * np.pi, N), rng.uniform(0, 2 * np.pi, N)
    ci = rng.uniform(-1, 1, N); si = np.sqrt(1 - ci ** 2)
    cO, sO, cw, sw = np.cos(Om), np.sin(Om), np.cos(w), np.sin(w)
    P = np.stack([cO * cw - ci * sO * sw, sO * cw + ci * cO * sw, si * sw])
    Q = np.stack([-cO * sw - ci * sO * cw, -sO * sw + ci * cO * cw, si * cw])
    r3 = xo * P + yo * Q
    v3 = vxo * P + vyo * Q
    r_ = np.linalg.norm(r3[:, :2000], axis=0)
    vv = np.sum(v3[:, :2000] ** 2, axis=0)
    assert np.allclose(vv, G * Mt[:2000] * MSUN * (2 / r_ - 1 / a_sma[:2000]), rtol=1e-8)
    r3d = np.linalg.norm(r3, axis=0)
    s_proj = np.hypot(r3[0], r3[1])
    g_true = G * Mt * MSUN / r3d ** 2
    G1 = W.MG_of_mass(M1) + 5 * np.log10(d / 10.)
    G2 = W.MG_of_mass(M2) + 5 * np.log10(d / 10.)
    spm = np.sqrt(W.sigma_pm(G1, dr4) ** 2 + W.sigma_pm(G2, dr4) ** 2)
    splx = 1 / np.sqrt(W.sigma_plx(G1, dr4) ** -2 + W.sigma_plx(G2, dr4) ** -2)
    plx = 1000. / d
    d_obs = 1000. / (plx + splx * rng.standard_normal(N))
    dkpc = d / 1000.
    pmx, pmy = v3[0] / (4.74e3 * dkpc), v3[1] / (4.74e3 * dkpc)
    npmx, npmy = spm * rng.standard_normal(N), spm * rng.standard_normal(N)
    s_obs = s_proj * (d_obs / d)
    M_obs = Mt * (1 + 0.05 * rng.standard_normal(N))
    sel = ((s_obs > smin_kAU * KAU) & (s_obs < smax_kAU * KAU) & (d < dmax_pc)
           & (np.maximum(G1, G2) < Gcut) & (d_obs > 0) & (M_obs > 0.2))
    frozen = dict(pmx=pmx[sel], pmy=pmy[sel], npmx=npmx[sel], npmy=npmy[sel],
                  d_obs=d_obs[sel], s_obs=s_obs[sel], M_obs=M_obs[sel],
                  g_true=g_true[sel],
                  g_proj=G * M_obs[sel] * MSUN / s_obs[sel] ** 2,
                  vc_obs=np.sqrt(G * M_obs[sel] * MSUN / s_obs[sel]))
    extra = dict(M1=M1[sel], M2=M2[sel], Mt=Mt[sel], G1=G1[sel], G2=G2[sel], r3d=r3d[sel], d=d[sel],
                 spm=spm[sel], splx=splx[sel], plx=plx[sel])
    return frozen, extra


CHUNK_MASTER = 50_000
_ORIG_MAKE_POPULATION = W.make_population


def chunked_frozen_population(N, rng, keys=None, chunk=CHUNK_MASTER, **kw):
    """The FROZEN make_population called in chunks (memory cap); statistically identical, RNG stream differs.
    keys: keep only these returned arrays (memory); concatenation is per key with the parts freed as it goes."""
    parts, left = [], N
    while left > 0:
        n = min(chunk, left)
        d = _ORIG_MAKE_POPULATION(n, rng, **kw); left -= n
        parts.append({k: v for k, v in d.items() if keys is None or k in keys}); del d
        guard("master chunk")
    out = {}
    for k in list(parts[0]):
        out[k] = np.concatenate([p[k] for p in parts])
        for p in parts:
            del p[k]
    return out


def lean_model_medians(pop_master, a0, grid, rng, batch=2):
    """W.model_medians with a memory-lean bootstrap.  The grid medians come from the frozen bin_medians (exact, boot = 0);
    the model's finite-MC error is the same estimator (100 resamples of each bin of the master at the reference gamma 1.15,
    std ddof = 1) drawn in batches of `batch` resamples, because the frozen one-shot (100 x n_bin) draw needs ~0.7 GB on a
    3,000,000-pair master.  Control K6 compares it with the frozen function on a small master."""
    logy = np.log10(pop_master['g_proj'] / a0)
    out = np.full((len(grid), len(W.EDGES) - 1), np.nan)
    for i, g in enumerate(grid):
        vt = W.vtilde_of(pop_master, g, a0)
        out[i], _, _ = W.bin_medians(logy, vt)
    vt_ref = W.vtilde_of(pop_master, 1.15, a0)
    sig = np.full(len(W.EDGES) - 1, np.nan)
    for b in range(len(W.EDGES) - 1):
        m = (logy >= W.EDGES[b]) & (logy < W.EDGES[b + 1]) & (vt_ref < W.VTCAP)
        if m.sum() < W.MINBIN:
            continue
        v = vt_ref[m]
        bs = np.concatenate([np.median(v[rng.integers(0, len(v), (batch, len(v)))], axis=1) for _ in range(100 // batch)])
        sig[b] = bs.std(ddof=1)
        guard("lean bootstrap")
    return out, sig


# ---------------------------------------------------------------- class boosts (applied to the TRUE velocity before noise)
def x_obs(c):
    return c["s_obs"] / np.sqrt(W.G * c["M_obs"] * W.MSUN / A0_R)


BOOSTS = {
    "A0_NEWTON": lambda c: np.ones(len(c["s_obs"])),
    "A1_NEWTON_CUTS": lambda c: np.ones(len(c["s_obs"])),
    "B1_MOND_BENCH": lambda c: W.gamma_of_y(c["g_true"] / W.A0_CAN, W.GAMMA_MOND, W.y_extN(W.A0_CAN)),
    "B2_MOND_STEP": lambda c: np.where(x_obs(c) > 1.0, 1.15, 1.0),
    "B3_ARM_A_FLOOR": lambda c: W.gamma_of_y(c["g_true"] / W.A0_CAN, W.GAMMA_TARGET, W.y_extN(W.A0_CAN)),
    "C_CFG740": lambda c: 1.0 + 0.5 * (c["r3d"] / (LSTAR_PC * W.PC)) ** 2,
    "D_FALSIFIER_EDGE": lambda c: np.where(x_obs(c) > 1.0, 1.01, 1.0),
    "MUTATE_STEP_1p2": lambda c: np.where(x_obs(c) > 1.0, 1.2, 1.0),
}


def velocities(c, b):
    """Exactly W.vtilde_of's arithmetic with the per-pair boost b: returns (vtilde, v_perp in km/s)."""
    vX = (b * c["pmx"] + c["npmx"]) * 4.74e3 * (c["d_obs"] / 1000.)
    vY = (b * c["pmy"] + c["npmy"]) * 4.74e3 * (c["d_obs"] / 1000.)
    vp = np.hypot(vX, vY)
    return vp / c["vc_obs"], vp / 1e3


def vt_err_p3(c, vt):
    """CFG825 converter's P3 leading-order sigma(vtilde): PM-difference term + 1.5 vt sigma_d/d (d = observed distance)."""
    vc_kms = c["vc_obs"] / 1e3
    return np.sqrt((4.74047 * (c["d_obs"] / 1000.0) / vc_kms) ** 2 * c["spm"] ** 2 + (1.5 * vt * c["splx"] / c["plx"]) ** 2)


def catalogue_cuts(c, vt):
    """A1 only: frozen cut 4 (parallax S/N >= 40 both, true parallax, per-star sigma_plx(G)) and cut 15
    (sigma(vt) <= 0.1 max(1, vt/2)) with sigma(vt) = P3 (+) the 5.5%-per-star mass term (leading order; no LOS/perspective term,
    because the frozen population model carries no systemic proper motion)."""
    s1, s2 = W.sigma_plx(c["G1"], True), W.sigma_plx(c["G2"], True)
    cut4 = (c["plx"] / s1 >= 40) & (c["plx"] / s2 >= 40)
    mass = 0.5 * 0.055 * np.sqrt(c["M1"] ** 2 + c["M2"] ** 2) / c["Mt"] * vt
    sig15 = np.sqrt(vt_err_p3(c, vt) ** 2 + mass ** 2)
    cut15 = sig15 <= 0.1 * np.maximum(1.0, vt / 2)
    return cut4 & cut15


def make_catalogue(n_cat, rng, cls, chunk=CHUNK):
    """MOCK catalogue of n_cat pairs: replica population, oversampled x2.7 (the frozen gate's procedure), class boost,
    optional A1 cuts, random keep of n_cat.  Returns (cat dict incl. vt and v_perp_kms)."""
    acc, have = [], 0
    while have < n_cat:
        n = min(chunk, max(int((n_cat - have) * 2.7), 20000))
        fz, ex = mock_population(n, rng, dr4=True)
        c = dict(fz); c.update(ex)
        b = BOOSTS[cls](c)
        vt, vp = velocities(c, b)
        c["vt"], c["v_perp_kms"], c["boost"] = vt, vp, b
        if cls == "A1_NEWTON_CUTS":
            m = catalogue_cuts(c, vt)
            c = {k: v[m] for k, v in c.items()}
        acc.append(c); have += len(c["vt"])
        guard("catalogue chunk")
    cat = {k: np.concatenate([a[k] for a in acc]) for k in acc[0]}
    keep = rng.permutation(len(cat["vt"]))[:n_cat]
    return {k: v[keep] for k, v in cat.items()}


def pair_table(c):
    """The cfg816_r.py pair-table columns for a clean MOCK sky."""
    n = len(c["vt"])
    s1, s2 = W.sigma_plx(c["G1"], True), W.sigma_plx(c["G2"], True)
    z = np.zeros(n)
    return dict(sep_kAU=c["s_obs"] / W.KAU, v_perp_kms=c["v_perp_kms"],
                M1_msun=c["M_obs"] * c["M1"] / c["Mt"], M2_msun=c["M_obs"] * c["M2"] / c["Mt"],
                d_pc=c["d_obs"], plx_err_frac=np.maximum(s1, s2) / c["plx"],
                ruwe1=np.ones(n), ruwe2=np.ones(n), ipd1=z, ipd2=z,
                vt_err=vt_err_p3(c, c["vt"]), drv_kms=np.full(n, np.nan), nss1=z, nss2=z)


def r_score(t, rng, B, label, quiet=True):
    """CFG825's own score() (primary + branches + label logic), output captured; its OUT buffer is cleared after."""
    buf = io.StringIO()
    if quiet:
        with contextlib.redirect_stdout(buf):
            res, final = R825.score(t, rng, B, label)
    else:
        res, final = R825.score(t, rng, B, label)
    R825.OUT.clear()
    return res, final, buf.getvalue()


def fit_line(foot, g, sg):
    lab = "canonical" if foot == "canonical" else "alt footing"
    return f"  catalog [a0 {lab}]             gamma_inf = {g:.4f} +- {sg:.4f}  (chi2)\n"
