#!/usr/bin/env python3
"""CFG217 -- the attack on CFG216: does RC100's "the rival's z-dependence is not in the data" survive gas-prior, pressure and selection
systematics?  Frozen criteria: FROZEN_CRITERIA.md here (0c2aa7da9 + addendum 04a8a927f), committed before any number.
kappa = 1/2 FITTED, NOT DERIVED.  The aim is to break CFG216's result.  Author decompositions, not a direct a0 measurement.
Run:  python3 campaign_fresh_gravity/CFG217_rc100_attack/cfg217_attack.py        (MUTATE=1: D_obs x 10^(0.2 (z - z_med)))
"""
import os, sys, csv, math, json
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.stats import spearmanr

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
sys.path.insert(0, CFG)
_mut = os.environ.pop("MUTATE", None)
try:
    import CFG4_common as K
    import CFG7_common as C
finally:
    if _mut is not None:
        os.environ["MUTATE"] = _mut
MODE = (_mut or "").strip()
assert MODE in ("", "0", "1")
MUT = MODE == "1"
CORR = os.environ.get("RC100_INPUT", "").strip() == "corrected"      # input-correction switch (data chat's provenance check 03922e8c7)
RC100_PATH = (os.path.join(REPO, "data_assembly", "rc100_provenance", "rc100_table3_six_fields_paper_values.csv") if CORR
              else os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3.csv"))
SFX = "_corrected" if CORR else ""
R = C.Report("cfg217_attack" + SFX, MUT)
P, check = R.P, R.check
P(__doc__.split("Run:")[0].strip())

G2SI = 1e6 / 3.0856775814913673e19
OM = 0.315
A0 = K.A0["canonical"]
NBOOT, SEED = 10000, 216
NU = K.nu_mono


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + 1 - OM)


def nu1(y):
    return float(NU(np.array([y]))[0])


def gbar_of_gobs(gobs_si, a0):
    q = gobs_si / a0
    return a0 * 10 ** brentq(lambda ly: nu1(10 ** ly) * 10 ** ly - q, -80, 14, xtol=1e-14, rtol=1e-14)


def mu_t18(z, logm):
    return 10 ** (0.06 - 3.3 * (math.log10(1 + z) - 0.65) ** 2 - 0.41 * (logm - 10.7))


def fnum(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else float("nan")
    except (TypeError, ValueError):
        return float("nan")


# ------------------------------------------------------------------------------------------------ data (CFG216's sample)
raw = list(csv.DictReader(open(RC100_PATH, newline="")))
rows = []
for r in raw:
    z, Re, Vc, fd, lm, s0 = (fnum(r[k]) for k in ("z", "Re_kpc", "Vc_Re_kms", "fDM_within_Re", "logMbar_Msun", "sigma0_kms"))
    if all(math.isfinite(v) for v in (z, Re, Vc, fd)) and 0 < fd < 1:
        rows.append(dict(name=r["name"], z=z, Re=Re, Vc=Vc, fd=fd, lm=lm, s0=s0))
N = len(rows)
z = np.array([r["z"] for r in rows]); zmed = float(np.median(z))
Re = np.array([r["Re"] for r in rows]); Vc = np.array([r["Vc"] for r in rows]); fd = np.array([r["fd"] for r in rows])
lmb = np.array([r["lm"] for r in rows]); s0 = np.array([r["s0"] for r in rows])
gobs0 = Vc ** 2 / Re * G2SI
gbar0 = (1 - fd) * gobs0
D0 = 1 / (1 - fd)
if MUT:
    D0 = D0 * 10 ** (0.2 * (z - zmed))
    gobs0 = D0 * gbar0
    P("  MUTATE=1: D_obs x 10^(0.2 (z - z_med)) in the baseline")
P(f"  RC100: {N} galaxies; z {z.min():.2f}-{z.max():.2f} (median {zmed:.2f})")
rc41 = {r["id"].replace("_", " "): r for r in csv.DictReader(open(os.path.join(REPO, "data_assembly", "price2021_rc41", "price2021_rc41.csv")))}
in41 = np.array([r["name"] in rc41 for r in rows])
P(f"  RC41 galaxies found in RC100 by name: {int(in41.sum())}")

# ------------------------------------------------------------------------------------------------ bootstrap machinery (seed 216, as CFG216)
rng = np.random.default_rng(SEED)
IDX = {}


def boots(n):
    if n not in IDX:
        IDX[n] = rng.integers(0, n, size=(NBOOT, n))
    return IDX[n]


def ts(x, y):
    i, j = np.triu_indices(len(x), 1)
    dx = x[j] - x[i]
    m = dx != 0
    return float(np.median((y[j] - y[i])[m] / dx[m]))


def ts_boot(x, y):
    n = len(x)
    i, j = np.triu_indices(n, 1)
    B = boots(n)
    out = np.empty(NBOOT)
    for k in range(NBOOT):
        xb, yb = x[B[k]], y[B[k]]
        dx = xb[j] - xb[i]
        m = dx != 0
        out[k] = np.median((yb[j] - yb[i])[m] / dx[m])
    return out


def delta_arr(zv, Dv, gv, law):
    a0 = A0 * (np.array([E(v) for v in zv]) if law == "rival" else 1.0)
    return np.log10(Dv / NU(gv / a0))


def slope_stats(zv, dv):
    bs = ts_boot(zv, dv)
    return dict(slope=ts(zv, dv), lo=float(np.percentile(bs, 2.5)), hi=float(np.percentile(bs, 97.5)), sd=float(np.std(bs)),
                med=float(np.median(dv)))


def expectations(zv, gobs):
    """slopes of delta_flat / delta_rival if each law were exactly true (baryons from that law's inversion)"""
    out = {}
    for truth in ("flat", "rival"):
        dfl, dri = [], []
        for zz, go in zip(zv, gobs):
            a0t = A0 * (E(zz) if truth == "rival" else 1.0)
            gt = gbar_of_gobs(go, a0t)
            Dt = go / gt
            dfl.append(math.log10(Dt / nu1(gt / A0))); dri.append(math.log10(Dt / nu1(gt / (A0 * E(zz)))))
        out[truth] = dict(flat=ts(zv, np.array(dfl)), rival=ts(zv, np.array(dri)))
    return out


def analyse(tag, zv, gobs, gbar, verbose=True):
    Dv = gobs / gbar
    res = {law: slope_stats(zv, delta_arr(zv, Dv, gbar, law)) for law in ("flat", "rival")}
    ex = expectations(zv, gobs)
    for law in res:
        r_ = res[law]
        r_["z_vs_flat_true"] = (r_["slope"] - ex["flat"][law]) / r_["sd"]
        r_["z_vs_rival_true"] = (r_["slope"] - ex["rival"][law]) / r_["sd"]
        r_["z_vs_zero"] = (0 - r_["slope"]) / r_["sd"]
    res["exp"] = ex
    if verbose:
        P(f"  {tag:34s} flat: slope {res['flat']['slope']:+.3f} [{res['flat']['lo']:+.3f}, {res['flat']['hi']:+.3f}] (z: flat-true {res['flat']['z_vs_flat_true']:+.1f}, rival-true {res['flat']['z_vs_rival_true']:+.1f}); "
          f"rival: slope {res['rival']['slope']:+.3f} [{res['rival']['lo']:+.3f}, {res['rival']['hi']:+.3f}] (z: flat-true {res['rival']['z_vs_flat_true']:+.1f}, rival-true {res['rival']['z_vs_rival_true']:+.1f})")
    return res


def survives(r):
    return r["rival"]["hi"] < 0 and r["rival"]["z_vs_zero"] >= 3.0


# ------------------------------------------------------------------------------------------------ controls C1, C2
R.banner("CONTROLS")
c1 = max(abs(math.log10(nu1(3.0 * A0 / fac) / nu1(3.0 * A0 / fac))) for fac in (1.0, E(1.5), E(2.5)))
check("C1 a synthetic galaxy placed exactly on each law returns delta = 0", f"max {c1:.1e}", c1 < 1e-12)
BASE = analyse("baseline (CFG216)", z, gobs0, gbar0, verbose=False)
J216 = json.load(open(os.path.join(CFG, "CFG216_rc100_within_sample", "cfg216_rc100" + SFX + "_results.json")))["numbers"]["results"]
if not MUT:
    dmax = 0.0
    for law in ("flat", "rival"):
        ref = J216[f"nu_mono|canonical|{law}"]
        for k, kk in (("slope", "slope"), ("lo", "lo"), ("hi", "hi"), ("sd", "sd"), ("med", "med")):
            dmax = max(dmax, abs(BASE[law][k] - ref[kk]))
    check("C2 the baseline slopes, CIs, sigmas and medians reproduce CFG216's committed values to 1e-9", f"max |difference| {dmax:.1e}", dmax < 1e-9)
else:
    P("  (C2 not applicable under MUTATE)")

# ------------------------------------------------------------------------------------------------ G1: gas prior
R.banner("G1 -- the gas prior and its z-dependence")
logMs = np.array([brentq(lambda x, zz=zz, l=l: x + math.log10(1 + mu_t18(zz, x)) - l, 6.0, 13.5) for zz, l in zip(z, lmb)])
mu0 = np.array([mu_t18(zz, x) for zz, x in zip(z, logMs)])
ov = [i for i in range(N) if in41[i]]
dM = np.array([logMs[i] - fnum(rc41[rows[i]["name"]]["logMstar_SED"]) for i in ov])
recon_ok = float(np.median(np.abs(dM))) <= 0.15
P(f"  C-recon: reconstructed log M* - SED log M* for the {len(ov)} RC41 overlaps: median {np.median(dM):+.3f}, median |diff| {np.median(np.abs(dM)):.3f} dex, range [{dM.min():+.2f}, {dM.max():+.2f}]")
check("C-recon (reported) the reconstruction of M* from M_bar under the Tacconi+18 scaling: median |Delta log M*| <= 0.15 dex", f"{np.median(np.abs(dM)):.3f} dex -> "
      f"{'accepted: G1 runs on all 100' if recon_ok else 'REJECTED: G1 runs on the RC41 overlap only, with actual M* and M_gas'}", recon_ok, load_bearing=False)
R.num("recon", dict(median=float(np.median(dM)), median_abs=float(np.median(np.abs(dM))), accepted=bool(recon_ok)))
if recon_ok:
    sel = np.ones(N, bool); Ms = 10 ** logMs; mu_use = mu0
    P("  G1 sample: all 100, M* reconstructed")
else:
    sel = in41.copy()
    Ms = np.array([10 ** fnum(rc41[r["name"]]["logMstar_SED"]) if r["name"] in rc41 else np.nan for r in rows])
    mu_use = np.array([10 ** fnum(rc41[r["name"]]["logMgas"]) / 10 ** fnum(rc41[r["name"]]["logMstar_SED"]) if r["name"] in rc41 else np.nan for r in rows])
    P(f"  G1 sample: the RC41 overlap only (n = {int(sel.sum())}), with the actual M* and M_gas")
VAR = {"V0 baseline": lambda zz, m, mu: mu,
       "V1 gas fraction fixed with z (mu_T18 at z = 1.5)": lambda zz, m, mu: mu_t18(1.5, math.log10(m)),
       "V2 0.5 mu": lambda zz, m, mu: 0.5 * mu, "V3 2 mu": lambda zz, m, mu: 2.0 * mu,
       "V4 0.18 mu (alpha_CO 0.8)": lambda zz, m, mu: 0.18 * mu, "V5 1.49 mu (alpha_CO 6.5)": lambda zz, m, mu: 1.49 * mu}
G1 = {}
zs_, gob_s, gba_s = z[sel], gobs0[sel], gbar0[sel]
if not recon_ok:
    # the bootstrap index matrix is for the sample size actually used
    pass
for name, f in VAR.items():
    fac = np.array([(1 + f(zz, m, mu)) / (1 + mu) for zz, m, mu in zip(zs_, Ms[sel], mu_use[sel])])
    G1[name] = analyse(name, zs_, gob_s, gba_s * fac)
    G1[name]["fac_range"] = [float(fac.min()), float(fac.max())]
    G1[name]["fac_z"] = [float(np.median(fac[zs_ <= np.median(zs_)])), float(np.median(fac[zs_ > np.median(zs_)]))]
R.num("G1", {k: {l: v[l] for l in ("flat", "rival")} | {"fac_z": v["fac_z"]} for k, v in G1.items()})
P("\n  the median baryon-mass factor (1 + mu')/(1 + mu) in the low-z / high-z halves: " + "; ".join(f"{k.split(' ')[0]} {v['fac_z'][0]:.2f} / {v['fac_z'][1]:.2f}" for k, v in G1.items()))
surv = {k: survives(v) for k, v in G1.items()}
P("  the rival's deficit survives (CI upper < 0 and z >= 3 from 0): " + "; ".join(f"{k.split(' ')[0]} {'YES' if v else 'NO'}" for k, v in surv.items()))

# ------------------------------------------------------------------------------------------------ G2: prior-driven?
R.banner("G2 -- is f_DM prior-driven?  (RC41 overlap, actual SED + gas)")
prior = np.array([math.log10(10 ** fnum(rc41[rows[i]["name"]]["logMstar_SED"]) + 10 ** fnum(rc41[rows[i]["name"]]["logMgas"])) for i in ov])
dprior = lmb[ov] - prior
dfl = delta_arr(z[ov], D0[ov], gbar0[ov], "flat")
ok2 = np.isfinite(dprior) & np.isfinite(dfl)
rho, pv = spearmanr(dfl[ok2], dprior[ok2])
b_pr = ts(dprior[ok2], dfl[ok2])
resid = dfl[ok2] - b_pr * dprior[ok2]
zov = z[ov][ok2]
bsr = np.empty(NBOOT)
Bq = boots(int(ok2.sum()))
i_, j_ = np.triu_indices(int(ok2.sum()), 1)
for k in range(NBOOT):
    xb, yb = zov[Bq[k]], resid[Bq[k]]
    dx = xb[j_] - xb[i_]
    m_ = dx != 0
    bsr[k] = np.median((yb[j_] - yb[i_])[m_] / dx[m_])
P(f"  Delta_prior = log M_bar,fit - log(M* + M_gas): median {np.median(dprior[ok2]):+.3f} dex (n = {int(ok2.sum())}); Spearman rho(delta_flat, Delta_prior) = {rho:+.2f} (p = {pv:.3f})")
P(f"  Theil-Sen slope of delta_flat on Delta_prior {b_pr:+.3f}; z-slope of delta_flat after removing it: {ts(zov, resid):+.3f} [{np.percentile(bsr, 2.5):+.3f}, {np.percentile(bsr, 97.5):+.3f}] (n = {int(ok2.sum())})")
prior_driven = abs(rho) >= 0.3 and pv < 0.05
P(f"  -> prior-driven (|rho| >= 0.3 and p < 0.05): {'YES' if prior_driven else 'no'}")
R.num("G2", dict(rho=float(rho), p=float(pv), prior_driven=bool(prior_driven), n=int(ok2.sum())))

# ------------------------------------------------------------------------------------------------ G3: pressure
R.banner("G3 -- the pressure term (V_c'^2 = V_c^2 - (3.36 - alpha) sigma0^2; g_bar fixed)")
G3 = {}
if MUT:
    P("  (G3 not run under MUTATE)")
else:
    for alpha in (3.36, 1.68, 0.0):
        vc2 = Vc ** 2 - (3.36 - alpha) * s0 ** 2
        ok3 = vc2 > 0                # (added after the first run crashed: at alpha = 0 some V_c'^2 are <= 0, i.e. the fit's pressure correction exceeds
        #                               the whole V_c^2; those galaxies are excluded from that variant and counted)
        if not ok3.all():
            P(f"  alpha = {alpha}: {int((~ok3).sum())} galaxies have V_c'^2 <= 0 (the fit's pressure term exceeds V_c^2) and are excluded from this variant")
        go = vc2[ok3] / Re[ok3] * G2SI
        G3[alpha] = analyse(f"alpha = {alpha} (n = {int(ok3.sum())})", z[ok3], go, gbar0[ok3])
    R.num("G3", {str(a): {l: v[l] for l in ("flat", "rival")} for a, v in G3.items()})
    P("  the rival's deficit survives: " + "; ".join(f"alpha {a}: {'YES' if survives(v) else 'NO'}" for a, v in G3.items()))

# ------------------------------------------------------------------------------------------------ G4: the non-RC41 flat slope
R.banner("G4 -- the negative flat slope in the non-RC41 galaxies (n = %d)" % int((~in41).sum()))
nz = z[~in41]
G4 = {}
variants4 = {}
if recon_ok:
    for name, f in VAR.items():
        fac_all = np.array([(1 + f(zz, m, mu)) / (1 + mu) for zz, m, mu in zip(z, Ms, mu_use)])
        variants4[name] = (gobs0, gbar0 * fac_all)
else:
    P("  (reconstruction rejected: the non-RC41 galaxies have no actual M* and gas, so G4's gas variants cannot be formed)")
if not MUT:
    for alpha in (1.68, 0.0):
        variants4[f"pressure alpha = {alpha}"] = ((Vc ** 2 - (3.36 - alpha) * s0 ** 2) / Re * G2SI, gbar0)
for name, (go, gb) in variants4.items():
    okn = go[~in41] > 0
    if not okn.all():
        P(f"  ({name}: {int((~okn).sum())} non-RC41 galaxies with g_obs <= 0 excluded)")
    Dn = go[~in41][okn] / gb[~in41][okn]
    st = slope_stats(nz[okn], delta_arr(nz[okn], Dn, gb[~in41][okn], "flat"))
    G4[name] = st
    P(f"  {name:48s} delta_flat slope {st['slope']:+.3f} [{st['lo']:+.3f}, {st['hi']:+.3f}]")
sens_v1 = None
for name, st in G4.items():
    if name.startswith("V1"):
        sens_v1 = st["lo"] <= 0 <= st["hi"]
P(f"  -> gas-scaling-sensitive (the CI contains 0 under V1): {('YES' if sens_v1 else 'no') if sens_v1 is not None else 'n/a'}")
R.num("G4", G4)

# ------------------------------------------------------------------------------------------------ G5: mocks
R.banner("G5 -- can a z-dependent gas mis-scaling ALONE produce the pattern?  g_bar,analysis = g_bar,true x 10^(beta log10((1 + z)/2.5))")
gt = {t: np.array([gbar_of_gobs(go, A0 * (E(zz) if t == "rival" else 1.0)) for zz, go in zip(z, gobs0)]) for t in ("flat", "rival")}
sf_obs, sr_obs = BASE["flat"]["slope"], BASE["rival"]["slope"]
sf_sd, sr_sd = BASE["flat"]["sd"], BASE["rival"]["sd"]
DLOG = math.log10(3.5 / 1.6)


def mock_slopes(truth, beta):
    ga = gt[truth] * 10 ** (beta * np.log10((1 + z) / 2.5))
    Dv = gobs0 / ga
    return ts(z, delta_arr(z, Dv, ga, "flat")), ts(z, delta_arr(z, Dv, ga, "rival"))


s00 = mock_slopes("flat", 0.0)
check("C4 machinery: the flat-truth mock at beta = 0 gives slopes (0, expected) equal to the baseline expectations to 1e-9", f"{s00[0]:+.2e}, {s00[1]:+.6f} vs {BASE['exp']['flat']['rival']:+.6f}",
      abs(s00[0]) < 1e-9 and abs(s00[1] - BASE["exp"]["flat"]["rival"]) < 1e-9)
# M1: flat truth: beta that reproduces the observed delta_flat slope
try:
    b1 = brentq(lambda b: mock_slopes("flat", b)[0] - sf_obs, -3.0, 3.0, xtol=1e-6)
    P(f"  M1 (flat truth): the mis-scaling that reproduces the observed delta_flat slope {sf_obs:+.3f}: beta = {b1:+.3f} -> differential dlog M_bar (z 0.6 -> 2.5) = {b1 * DLOG:+.3f} dex; "
      f"the rival's slope there {mock_slopes('flat', b1)[1]:+.3f} (observed {sr_obs:+.3f})")
except ValueError:
    b1 = float("nan"); P("  M1: no beta in [-3, 3] reproduces the observed flat slope")
# M2: rival truth: beta minimising chi2 against both observed slopes
chi2 = lambda b: ((mock_slopes("rival", b)[0] - sf_obs) / sf_sd) ** 2 + ((mock_slopes("rival", b)[1] - sr_obs) / sr_sd) ** 2
grid = np.arange(-2.0, 2.0001, 0.02)
c2g = np.array([chi2(b) for b in grid])
bg = float(grid[int(np.argmin(c2g))])
res2 = minimize_scalar(chi2, bounds=(bg - 0.05, bg + 0.05), method="bounded", options=dict(xatol=1e-7))
bstar, cmin = float(res2.x), float(res2.fun)
lim = 0.2 / DLOG
plaus = np.abs(grid) <= lim
c_pl = float(c2g[plaus].min()); b_pl = float(grid[plaus][int(np.argmin(c2g[plaus]))])
sf2, sr2 = mock_slopes("rival", bstar)
P(f"  M2 (rival truth): best beta = {bstar:+.3f} (dlog M_bar = {bstar * DLOG:+.3f} dex) with chi2 = {cmin:.2f} (slopes {sf2:+.3f}, {sr2:+.3f} vs observed {sf_obs:+.3f}, {sr_obs:+.3f}); "
  f"within the plausible range |dlog M_bar| <= 0.2 dex (|beta| <= {lim:.2f}): best chi2 = {c_pl:.2f} at beta = {b_pl:+.2f}; at beta = 0: chi2 = {chi2(0.0):.1f}")
m2_produces = c_pl < 2.0
P(f"  -> M2 produces the pattern at a plausible mis-scaling (chi2 < 2 with |dlog M_bar| <= 0.2 dex): {'YES' if m2_produces else 'no'}; "
  f"the stress variant V1 (gas fraction fixed with z) corresponds to about {math.log10(np.median(np.array([(1 + mu_t18(1.5, logMs[i])) / (1 + mu0[i]) for i in range(N) if z[i] > 2.0])) / np.median(np.array([(1 + mu_t18(1.5, logMs[i])) / (1 + mu0[i]) for i in range(N) if z[i] < 1.0]))):+.2f} dex of differential M_bar")
R.num("G5", dict(beta_M1=b1, beta_M2=bstar, chi2_M2=cmin, chi2_plausible=c_pl, beta_plausible=b_pl, produces=bool(m2_produces), dlogM_M2=bstar * DLOG))

# ------------------------------------------------------------------------------------------------ G7: is the z-slope just a g_bar slope?
R.banner("G7 -- regress delta on log g_bar first (Theil-Sen), then the z-slope of the residuals")
lg = np.log10(gbar0 / A0)


def partial(zv, dv, lgv):
    b = ts(lgv, dv)
    return b, ts(zv, dv - b * lgv)


def partial_boot(zv, dv, lgv):
    B = boots(len(zv))
    bs = np.empty((NBOOT, 2))
    for k in range(NBOOT):
        bs[k] = partial(zv[B[k]], dv[B[k]], lgv[B[k]])
    return bs


G7 = {}
for law in ("flat", "rival"):
    dv = delta_arr(z, gobs0 / gbar0, gbar0, law)
    b, sz = partial(z, dv, lg)
    bs = partial_boot(z, dv, lg)
    G7[law] = dict(b_g=b, slope=sz, lo=float(np.percentile(bs[:, 1], 2.5)), hi=float(np.percentile(bs[:, 1], 97.5)), sd=float(np.std(bs[:, 1])),
                   bg_lo=float(np.percentile(bs[:, 0], 2.5)), bg_hi=float(np.percentile(bs[:, 0], 97.5)))
expG7 = {}
for truth in ("flat", "rival"):
    ga = gt[truth]
    Dv = gobs0 / ga
    lgt = np.log10(ga / A0)
    expG7[truth] = {law: partial(z, delta_arr(z, Dv, ga, law), lgt)[1] for law in ("flat", "rival")}
for law in ("flat", "rival"):
    g = G7[law]
    P(f"  {law:5s}: slope on log g_bar {g['b_g']:+.3f} [{g['bg_lo']:+.3f}, {g['bg_hi']:+.3f}]; residual z-slope {g['slope']:+.3f} [{g['lo']:+.3f}, {g['hi']:+.3f}] "
      f"(expected if flat true {expG7['flat'][law]:+.3f}, if rival true {expG7['rival'][law]:+.3f}; z: {(g['slope'] - expG7['flat'][law]) / g['sd']:+.1f} / {(g['slope'] - expG7['rival'][law]) / g['sd']:+.1f})")
g7_survives = G7["rival"]["hi"] < 0
P(f"  -> the rival's residual z-slope stays negative (CI upper < 0): {'YES' if g7_survives else 'NO'}")
R.num("G7", dict(res=G7, expected=expG7, survives=bool(g7_survives)))

# ------------------------------------------------------------------------------------------------ decision rows
R.banner("DECISION ROWS (frozen, with addendum 1)")
v25 = all(surv[k] for k in surv if k[:2] in ("V2", "V3", "V4", "V5"))
g3ok = all(survives(v) for v in G3.values()) if G3 else True
v1ok = surv.get([k for k in surv if k.startswith("V1")][0], False)
broken = m2_produces or (not v25) or (not g3ok)
mixed_items = []
if not v1ok:
    mixed_items.append("V1 (gas fraction held fixed with z)")
if not g7_survives:
    mixed_items.append("G7 (the z-slope is partly a g_bar slope)")
if prior_driven:
    mixed_items.append("G2 (f_DM prior-driven)")
if broken:
    d3 = "ATTACK-BROKEN"
elif mixed_items:
    d3 = "ATTACK-MIXED: fails " + "; ".join(mixed_items)
else:
    d3 = "ATTACK-ROBUST"
P(f"  D2 gas prior: survives V2-V5 (the plausible variants): {v25}; survives V1 (the stress variant): {v1ok}")
P(f"  D2 pressure: survives alpha = 1.68 and 0: {g3ok}")
P(f"  G4: gas-scaling-sensitive negative flat slope: {sens_v1}")
P(f"  D3 (headline): CFG216's outcome is {d3}")
R.num("D3", d3)
P("\n  NOTE (written after the numbers above were seen): the literal D3 is driven by G1 on the 38-galaxy RC41 overlap, where even V0 (the baseline)")
P("  fails the survival rule (the deficit is not significant in that subsample: CFG216's own sensitivity (a) has the same weakness). So G1's frozen version")
P("  cannot discriminate, and the literal ATTACK-BROKEN is a power artefact, not evidence against the deficit. The informative rows are G3, G5 and G7 and the post hoc block below.")

R.banner("POST HOC (written after the frozen numbers were seen; reported only)")
PH = {}
if not MUT:
    # (A) G1 on all 100 with the reconstructed M* (the frozen accept line 0.15 dex was missed at 0.229 dex; the median offset is -0.017 dex, so the
    #     scatter enters the factors (1 + mu')/(1 + mu) only through mu ~ M*^-0.41)
    P("  (A) G1 variants on ALL 100 galaxies with the reconstructed M*:")
    fullv = {}
    Mfull = 10 ** logMs
    for name, f in VAR.items():
        fac = np.array([(1 + f(zz, m, mu)) / (1 + mu) for zz, m, mu in zip(z, Mfull, mu0)])
        fullv[name] = analyse(name, z, gobs0, gbar0 * fac)
        fullv[name]["fac_z"] = [float(np.median(fac[z <= zmed])), float(np.median(fac[z > zmed]))]
    P("      the rival's deficit survives: " + "; ".join(f"{k.split(' ')[0]} {'YES' if survives(v) else 'NO'}" for k, v in fullv.items())
      + "; median baryon-mass factor low-z / high-z: " + "; ".join(f"{k.split(' ')[0]} {v['fac_z'][0]:.2f}/{v['fac_z'][1]:.2f}" for k, v in fullv.items()))
    PH["A_full"] = {k: {l: v[l] for l in ("flat", "rival")} for k, v in fullv.items()}
    # (B) the differential baryon mis-scaling that would make the rival exactly right, from the data side
    def data_side(beta):
        ga = gbar0 * 10 ** (beta * np.log10((1 + z) / 2.5))
        Dv = gobs0 / ga
        return ts(z, delta_arr(z, Dv, ga, "flat")), ts(z, delta_arr(z, Dv, ga, "rival"))
    b0 = brentq(lambda b: data_side(b)[1], -3.0, 3.0, xtol=1e-6)
    P(f"  (B) data side: g_bar x 10^(beta log10((1 + z)/2.5)) makes the rival's slope exactly 0 at beta = {b0:+.3f}, i.e. a differential dlog M_bar (z 0.6 -> 2.5) of "
      f"{b0 * DLOG:+.3f} dex; the flat slope there {data_side(b0)[0]:+.3f} (rival-true expectation {BASE['exp']['rival']['flat']:+.3f})")
    bl = brentq(lambda b: data_side(b)[0], -3.0, 3.0, xtol=1e-6)
    P(f"      and makes the flat slope exactly 0 at beta = {bl:+.3f} (dlog M_bar = {bl * DLOG:+.3f} dex; the rival's slope there {data_side(bl)[1]:+.3f})")
    PH["B"] = dict(beta_rival_zero=b0, dlogM_rival_zero=b0 * DLOG, beta_flat_zero=bl, dlogM_flat_zero=bl * DLOG)
R.num("posthoc", PH)
if MUT:
    R.banner("MUTATE RESPONSE")
    dflat = BASE["flat"]["slope"] - J216["nu_mono|canonical|flat"]["slope"]
    gob_un = (1 / (1 - fd))[sel] * gbar0[sel]                    # the unmutated g_obs for the same G1 sample
    shifts = []
    for name, f in VAR.items():
        fac = np.array([(1 + f(zz, m, mu)) / (1 + mu) for zz, m, mu in zip(zs_, Ms[sel], mu_use[sel])])
        d_un = delta_arr(zs_, gob_un / (gba_s * fac), gba_s * fac, "flat")
        d_mu = delta_arr(zs_, gob_s / (gba_s * fac), gba_s * fac, "flat")
        shifts.append(ts(zs_, d_mu) - ts(zs_, d_un))
    check("MUTATE: the injected 0.2 (z - z_med) slope moves the baseline delta_flat slope by +0.2 (>= +0.19) and every G1 variant's slope by within 0.05 of +0.2",
          f"baseline shift {dflat:+.4f}; G1 variant shifts {', '.join(f'{v:+.3f}' for v in shifts)}", dflat >= 0.19 and all(abs(v - 0.2) <= 0.05 for v in shifts))
R.write(here=LANE)
