#!/usr/bin/env python3
"""S3_v3_mw_seals Part C: SEALED Gaia DR4 Milky Way predictions for v3 (tile 45), committed before 2026-12-02.

Criteria FROZEN_CRITERIA.md §4 (8f6c6587e1) + A1, A2, A3.  New files only (CFG553 is never edited): SEALED_V3_MW_DR4.json
(deterministic, no timestamps), PREDICTIONS_V3_HASH.txt (its SHA-256), PREDICTIONS_V3.md (tables from the JSON).
v3 = AQUAL mu = x/(1+x) on McMillan17 census baryons (stars x s, s in CFG553's five-point band), EFE of the record's field
(h81 e_N, gamma = 57 deg; in-plane quantities by AMENDMENT A3's pointwise 3-D estimator, vertical quantities from the exact
axisymmetric gamma = 0 solve), isolated v3 as a sealed variant.  Rival: B1 Newtonian + NFW fitted to Ou+24 (refitted per s).
Decision rules after DR4: CFG553 §4-§5 adopted verbatim (F = v3 band, R = NFW band; P6 scalar per radius, rival 0).
Run: OMP_NUM_THREADS=1 nice -n 15 python3 s3_partC_seal.py [--mutate]   (S3_CACHE_DIR=... for the C1 independent rerun)
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; predictions, not results; not theory closed.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, time, hashlib, resource
import numpy as np
from scipy.optimize import least_squares, brentq
from scipy.stats import chi2 as chi2dist

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import s3_aqual as S
import s3_mw as MWm

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TAG = S.TAG
FOOTS = S.FOOTS
OUT, CHECKS = [], []
T0 = time.time()


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); OUT.append(s)


def check(name, ok, detail=""):
    CHECKS.append(dict(name=name, ok=bool(ok), detail=detail))
    P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")
    return bool(ok)


P("=" * 112)
P(f"S3 Part C: sealed Gaia DR4 MW predictions for v3 {'*** MUTATE: mu == 1 (nothing sealed) ***' if S.MUTATE else ''}")
P("kappa = 1/2 FITTED; footings never pooled; predictions, not results; not theory closed")
P("=" * 112)
G = S.G
KZU = 2 * math.pi * G * 1e6                         # (km/s)^2/kpc -> K_z/(2 pi G) in Msun/pc^2
MSUN_KG, PC_M, GEV_KG = 1.98847e30, 3.0856775814913673e16, 1.78266192e-27
GEV_PER_MSUNPC3 = MSUN_KG / PC_M ** 3 / GEV_KG / 1e6   # GeV/cm^3 per Msun/pc^3
R0 = MWm.R0
RKZ = np.arange(5.0, 16.01, 1.0); ZKZ = (0.5, 1.1, 2.0)
RVC = np.arange(5.0, 27.01, 1.0)
R5 = np.array([30.0, 40.0, 50.0, 60.0])
R6 = np.array([15.0, 20.0, 25.0, 30.0, 40.0, 50.0, 60.0])
SS = MWm.S_SEAL

# ------------------------------------------------------------------ solves (child processes; cached)
mw = MWm.MW()
g = mw.g
cells = [(f, s_, e) for f in FOOTS for s_ in SS for e in (0.0, MWm.EN_H81[f])]
nrun, pk = MWm.presolve(mw, MWm.GRID_MAIN, "main", cells, batch=4)
RSS = dict(presolve=pk)
vjobs = [dict(grid=list(MWm.GRID_MAIN), tag="main", foot=f, variant=v, eN=MWm.EN_H81[f]) for f in FOOTS for v in MWm.VARIANTS]
_, pk = S.run_batch("s3_mw", "job_mw_variant", vjobs, batch=2); RSS["variants"] = pk
TD = {}
for f in FOOTS:
    for gam in (0.0, MWm.GAMMA_DEG):
        TD[(f, gam)] = MWm.run_3d(mw, f, MWm.EN_H81[f], gam, 160)
P(f"  solves ready ({nrun} new main, {len(vjobs)} variants; child peaks {RSS}); {time.time() - T0:.0f} s")

# ------------------------------------------------------------------ C5: the pointwise 3-D estimator on the tilted Plummer reference
pc, pk = S.run_batch("s3_mw", "job_plummer_check", [dict(foot="canonical", eN=MWm.EN_H81["canonical"])], batch=1); RSS["C5"] = pk
pc = pc[0]
c5 = pc["max_rel_err"] <= 0.01 and pc["p2p_absdiff"] <= 0.005
check("C5", c5, f"tilted Plummer: pointwise estimator vs exact 57 deg in-plane F_R max |d| {pc['max_rel_err']:.4f} (tol 0.01); "
      f"peak-to-peak exact {np.round(pc['p2p_exact'], 4).tolist()} vs estimator {np.round(pc['p2p_est'], 4).tolist()} (max |d| {pc['p2p_absdiff']:.4f}, tol 0.005)")
USE3D = c5

# ------------------------------------------------------------------ helpers
def ratio_grid(foot, R):
    """(len(R), 72) pointwise ratio on the 3-D azimuth grid."""
    a57 = np.array(TD[(foot, MWm.GAMMA_DEG)]["FR"]); a0_ = np.array(TD[(foot, 0.0)]["FR"])
    rat = a57 / a0_
    return np.array([[np.interp(np.log(r), np.log(MWm.R3D), rat[:, j]) for j in range(rat.shape[1])] for r in np.atleast_1d(R)])


WEDGE = MWm.anticentre_mask(MWm.PH3D)


def model_fields(foot, s, eN):
    Phi, info, PB, ge = mw.solve(foot, s, eN)
    return Phi, PB, ge


def vc_curves(foot, s):
    """in-plane V_c: isolated, gamma 0 (exact), and with the 3-D estimator (wedge, mean, per azimuth)."""
    Pi, PBi, _ = model_fields(foot, s, 0.0)
    Pe, PBe, _ = model_fields(foot, s, MWm.EN_H81[foot])
    out = {}
    for name, R in (("RVC", RVC), ("R5", R5), ("R6", R6)):
        v2i = g.vc2(Pi, R); v2e = g.vc2(Pe, R)
        rg = ratio_grid(foot, R)
        v2az = v2e[:, None] * rg
        out[name] = dict(iso=np.sqrt(v2i), gamma0=np.sqrt(v2e), wedge=np.sqrt(v2az[:, WEDGE].mean(1)), mean=np.sqrt(v2az.mean(1)),
                         az=np.sqrt(v2az))
    return out


def slope_even(R, V, lo, hi):
    m = (R >= lo - 1e-9) & (R <= hi + 1e-9)
    x, y = np.log(R[m]), np.log(V[m])
    return float(np.polyfit(x, y, 1)[0])


def kz_table(Phi, PB, Rs, zs):
    return np.array([[float(g.kz_sym(Phi, PB, np.array([r]), np.array([z]))[0]) for z in zs] for r in Rs])


def sigma_z(Phi, PB, R, h):
    zz = np.linspace(0.0, 20 * h, 801)
    K = g.kz_sym(Phi, PB, np.full_like(zz, R), zz)
    return math.sqrt(np.trapz(np.exp(-zz / h) * K, zz))


def p3_local(Phi, PB, rho_b):
    rd = g.lap_density(Phi, PB)
    ph = rd - rho_b
    j = g.jc
    mid_ph = float(np.interp(R0, g.Rc, ph[:, j])); mid_tot = float(np.interp(R0, g.Rc, rd[:, j]))
    rc = np.hypot(g.RR, g.ZZ); sh = np.abs(rc - R0) <= 0.2
    shell = float(np.sum((ph * g.V)[sh]) / np.sum(g.V[sh]))
    i = int(np.argmin(np.abs(g.Rc - R0)))
    zw = np.clip(np.minimum(g.ze[1:], 1.1) - np.maximum(g.ze[:-1], -1.1), 0, None)
    col_tot = float(sum(np.interp(R0, g.Rc, rd[:, jj]) * zw[jj] for jj in range(g.nz) if zw[jj] > 0))
    col_ph = float(sum(np.interp(R0, g.Rc, ph[:, jj]) * zw[jj] for jj in range(g.nz) if zw[jj] > 0))
    kz11 = float(g.kz_sym(Phi, PB, np.array([R0]), np.array([1.1]))[0])
    return dict(phantom_mid_Msun_pc3=mid_ph / 1e9, phantom_mid_GeV_cm3=mid_ph / 1e9 * GEV_PER_MSUNPC3,
                phantom_shell_Msun_pc3=shell / 1e9, phantom_shell_GeV_cm3=shell / 1e9 * GEV_PER_MSUNPC3,
                Kz_R0_1p1_over_2piG=kz11 / KZU, Sigma_tot_1p1_Msun_pc2=col_tot / 1e6, Sigma_phantom_1p1_Msun_pc2=col_ph / 1e6,
                rho_tot_R0_Msun_pc3=mid_tot / 1e9)


def gauss_vc(Phi, PB, r, nth=200):
    dPR, dPz = g.cell_derivs(Phi, PB)
    mu = (np.arange(nth) + 0.5) / nth
    out = []
    for rr in np.atleast_1d(r):
        z = rr * mu; R = rr * np.sqrt(1 - mu ** 2)
        fR = g.interp2(dPR, R, z); fzp = g.interp2(dPz, R, z); fzm = g.interp2(dPz, R, -z)
        gr = (fR * R + 0.5 * (fzp - fzm) * z) / rr
        out.append(math.sqrt(max(rr * float(np.mean(gr)), 0)))
    return np.array(out)


# ------------------------------------------------------------------ C3 Jeans integrator
zz = np.linspace(0, 20 * 0.3, 801)
c3v = math.sqrt(np.trapz(np.exp(-zz / 0.3) * 100.0, zz)) ** 2 / (100.0 * 0.3)
check("C3", abs(c3v - 1) < 1e-3, f"Jeans integrator: uniform K_z -> sigma^2 / (K h) = {c3v:.6f} (tol 1e-3)")

# ------------------------------------------------------------------ the v3 predictions
SEAL = {"label": "v3 sealed Gaia DR4 Milky Way predictions (S3_v3_mw_seals); NOT CFG553 (the old-model set, untouched)",
        "theory": "v3 static limit: AQUAL div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho_b, mu = x/(1+x); EFE; screening l_g << 1 pc (unscreened); "
                  "mu_K^2 term not included (batch R6)",
        "inputs": {"baryons": "McMillan 2017 Table 3 (CFG514 transcription), stars x s, gas held", "s_band": SS,
                   "e_N_h81": MWm.EN_H81, "field_direction_lb_deg": MWm.DIR_LB, "gamma_deg": MWm.GAMMA_DEG, "R0_kpc": R0,
                   "a0_SI": S.A0_SI, "grid": g.describe(), "3d": {"N": 160, "box_kpc": 640.0, "estimator": "pointwise ratio (AMENDMENT A3)",
                                                                   "validated_C5": bool(USE3D)}},
        "rules": "CFG553 FROZEN_CRITERIA.md s4-s5 adopted verbatim: F = the v3 census band (primary: EFE), R = the NFW census band; "
                 "P6 scored as a scalar per radius with rival 0; footings and variants never pooled",
        "v3": {}, "v3_isolated": {}, "NFW_Ou24": {}, "variants": {}}
for foot in FOOTS:
    for model in ("v3", "v3_isolated"):
        SEAL[model][foot] = {}
    for s in SS:
        sk = f"{s:.6f}"
        Pe, PBe, ge = model_fields(foot, s, MWm.EN_H81[foot])
        Pi, PBi, _ = model_fields(foot, s, 0.0)
        vc = vc_curves(foot, s)
        rho_b = mw.rho(s)
        for model, Phi, PB in (("v3", Pe, PBe), ("v3_isolated", Pi, PBi)):
            d = {}
            kz = kz_table(Phi, PB, RKZ, ZKZ)
            d["P1_Kz_over_2piG_Msun_pc2"] = {f"R{r:.0f}": {f"z{z}": kz[i, k] / KZU for k, z in enumerate(ZKZ)} for i, r in enumerate(RKZ)}
            d["P1_nu_z2_kms_kpc2"] = {f"R{r:.0f}": float(g.kz_sym(Phi, PB, np.array([r]), np.array([0.075]))[0]) / 0.075 for r in RKZ}
            if model == "v3":
                V = vc["RVC"]["wedge"] if USE3D else vc["RVC"]["gamma0"]
                d["P2_Vc_anticentre_wedge"] = dict(zip([f"R{r:.0f}" for r in RVC], V.tolist()))
                d["P2_Vc_azimuthal_mean"] = dict(zip([f"R{r:.0f}" for r in RVC], vc["RVC"]["mean"].tolist()))
                d["P2_Vc_gamma0_exact"] = dict(zip([f"R{r:.0f}" for r in RVC], vc["RVC"]["gamma0"].tolist()))
            else:
                V = vc["RVC"]["iso"]
                d["P2_Vc"] = dict(zip([f"R{r:.0f}" for r in RVC], V.tolist()))
            Rgrid = np.arange(15.0, 27.51, 0.5)
            if model == "v3":
                v2e = g.vc2(Pe, Rgrid); rg = ratio_grid(foot, Rgrid)
                Vg = np.sqrt((v2e[:, None] * rg)[:, WEDGE].mean(1)) if USE3D else np.sqrt(v2e)
                Vg0 = np.sqrt(v2e)
                d["P2_slope_15_22_gamma0"] = slope_even(Rgrid, Vg0, 15, 22); d["P2_slope_15_27p5_gamma0"] = slope_even(Rgrid, Vg0, 15, 27.5)
            else:
                Vg = np.sqrt(g.vc2(Pi, Rgrid))
            d["P2_slope_15_22"] = slope_even(Rgrid, Vg, 15, 22)
            d["P2_slope_15_27p5"] = slope_even(Rgrid, Vg, 15, 27.5)
            d["P3"] = p3_local(Phi, PB, rho_b)
            d["P4_sigma_z_kms"] = {f"h{h}": {f"R{r:.0f}": sigma_z(Phi, PB, r, h) for r in RKZ} for h in (0.30, 0.90)}
            if model == "v3":
                V5w = vc["R5"]["wedge"] if USE3D else vc["R5"]["gamma0"]
                d["P5_Vc_anticentre_wedge"] = dict(zip([f"R{r:.0f}" for r in R5], V5w.tolist()))
                d["P5_Vc_azimuthal_mean"] = dict(zip([f"R{r:.0f}" for r in R5], vc["R5"]["mean"].tolist()))
                d["P5_Vc_gamma0_exact"] = dict(zip([f"R{r:.0f}" for r in R5], vc["R5"]["gamma0"].tolist()))
                sph0 = gauss_vc(Pe, PBe, R5)
                a57 = np.array(TD[(foot, MWm.GAMMA_DEG)]["Fsph"]); a0s = np.array(TD[(foot, 0.0)]["Fsph"])
                corr = np.sqrt(np.interp(np.log(R5), np.log(MWm.R3D), a57 / a0s))
                d["P5_Vc_spherical_equiv"] = dict(zip([f"R{r:.0f}" for r in R5], (sph0 * (corr if USE3D else 1.0)).tolist()))
                rr = np.arange(30.0, 60.01, 2.5)
                v2e30 = g.vc2(Pe, rr); rg30 = ratio_grid(foot, rr)
                d["P5_mean_30_60_wedge"] = float(np.mean(np.sqrt((v2e30[:, None] * rg30)[:, WEDGE].mean(1)))) if USE3D else float(np.mean(np.sqrt(v2e30)))
                d["P5_mean_30_60_azimuthal_mean"] = float(np.mean(np.sqrt((v2e30[:, None] * rg30).mean(1))))
                Vaz = vc["R6"]["az"]
                A = 2 * (Vaz.max(1) - Vaz.min(1)) / (Vaz.max(1) + Vaz.min(1))
                d["P6_asymmetry_A"] = dict(zip([f"R{r:.0f}" for r in R6], A.tolist()))
                d["P6_azimuth_Vmax_deg"] = dict(zip([f"R{r:.0f}" for r in R6], np.degrees(MWm.PH3D[Vaz.argmax(1)]).tolist()))
                d["P6_azimuth_Vmin_deg"] = dict(zip([f"R{r:.0f}" for r in R6], np.degrees(MWm.PH3D[Vaz.argmin(1)]).tolist()))
                d["P6_validated"] = bool(USE3D)
            else:
                d["P5_Vc"] = dict(zip([f"R{r:.0f}" for r in R5], vc["R5"]["iso"].tolist()))
                d["P5_Vc_spherical_equiv"] = dict(zip([f"R{r:.0f}" for r in R5], gauss_vc(Pi, PBi, R5).tolist()))
                rr = np.arange(30.0, 60.01, 2.5)
                d["P5_mean_30_60"] = float(np.mean(np.sqrt(g.vc2(Pi, rr))))
                d["P6_asymmetry_A"] = {f"R{r:.0f}": 0.0 for r in R6}
            SEAL[model][foot][sk] = d
    P(f"  {foot}: v3 cells done ({time.time() - T0:.0f} s)")
# variants (census only, EFE gamma 0 exact; envelope)
for foot in FOOTS:
    for v in MWm.VARIANTS:
        rho = MWm.VARIANTS[v](g.RR, g.ZZ)
        Phi, info, PB, ge = mw.solve(foot, 1.0, MWm.EN_H81[foot], rho=rho, key_extra=v)
        Rgrid = np.arange(15.0, 27.51, 0.5)
        SEAL["variants"][f"{foot}|{v}"] = dict(V20_gamma0=float(np.sqrt(g.vc2(Phi, np.array([20.0])))[0]),
                                                slope_15_27p5_gamma0=slope_even(Rgrid, np.sqrt(g.vc2(Phi, Rgrid)), 15, 27.5),
                                                Kz_R0_1p1_over_2piG=float(g.kz_sym(Phi, PB, np.array([R0]), np.array([1.1]))[0]) / KZU,
                                                V60_gamma0=float(np.sqrt(g.vc2(Phi, np.array([60.0])))[0]))

# ------------------------------------------------------------------ rival: B1 Newtonian + NFW fitted to Ou+24 (per s)
ou = {}
rows = [l.split() for l in open(os.path.join(REPO, "real_research", "data", "mw_rc_ou2024_table1.tsv")) if l.strip() and not l.startswith("#")]
hdr = rows[0]; arr = np.array([[float(x) for x in r] for r in rows[1:]])
ou = {h: arr[:, i] for i, h in enumerate(hdr)}
OR, OV = ou["R_kpc"], ou["vc_kms"]; OE = np.hypot(0.5 * (ou["sig_plus"] + ou["sig_minus"]), np.where(OR <= 22.0, 0.03, 0.15) * OV)
H0N = 67.7
RHO_CRIT = 3 * (H0N / 1e3) ** 2 / (8 * math.pi * G)


def nfw_params(M200, c):
    r200 = (3 * M200 / (4 * math.pi * 200 * RHO_CRIT)) ** (1 / 3); rs = r200 / c
    m = math.log(1 + c) - c / (1 + c); rhos = M200 / (4 * math.pi * rs ** 3 * m)
    return dict(M200=M200, c=c, rs=rs, rhos=rhos)


def nfw_g(p, r):
    x = r / p["rs"]
    return G * 4 * math.pi * p["rhos"] * p["rs"] ** 3 * (np.log1p(x) - x / (1 + x)) / r ** 2


def nfw_rho(p, r):
    x = r / p["rs"]
    return p["rhos"] / (x * (1 + x) ** 2)


def fit_nfw(s):
    vb2 = mw.gN_plane(s, OR) * OR

    def res(x):
        p = nfw_params(10 ** x[0], x[1])
        return (np.sqrt(np.maximum(vb2 + OR * nfw_g(p, OR), 0)) - OV) / OE
    best = None
    for lm0 in (11.0, 11.7, 12.3):
        for c0 in (5.0, 12.0, 25.0):
            f = least_squares(res, x0=[lm0, c0], bounds=([10.0, 1.0], [13.5, 60.0]))
            if best is None or f.cost < best.cost:
                best = f
    return nfw_params(10 ** best.x[0], best.x[1]), float(2 * best.cost)


p1, c2v = fit_nfw(1.0)
check("C2", abs(c2v / 9.872 - 1) <= 0.03, f"NFW fit to Ou+24 on my B1 Newtonian field: chi2 {c2v:.3f} vs CFG553 9.872 (tol 3%); M200 {p1['M200']:.3e} c {p1['c']:.2f}")
for s in SS:
    sk = f"{s:.6f}"
    p, c2 = fit_nfw(s)
    PhiN, PBN = mw.phiN(s)
    d = dict(M200=p["M200"], c=p["c"], chi2_Ou=c2)
    VN2 = mw.gN_plane(s, RVC) * RVC
    Vn = np.sqrt(VN2 + RVC * nfw_g(p, RVC)); d["P2_Vc"] = dict(zip([f"R{r:.0f}" for r in RVC], Vn.tolist()))
    Rgrid = np.arange(15.0, 27.51, 0.5)
    Vg = np.sqrt(mw.gN_plane(s, Rgrid) * Rgrid + Rgrid * nfw_g(p, Rgrid))
    d["P2_slope_15_22"] = slope_even(Rgrid, Vg, 15, 22); d["P2_slope_15_27p5"] = slope_even(Rgrid, Vg, 15, 27.5)
    kz = {}
    for r in RKZ:
        kz[f"R{r:.0f}"] = {}
        for z in ZKZ:
            rr = math.hypot(r, z)
            kz[f"R{r:.0f}"][f"z{z}"] = (float(g.kz_sym(PhiN, PBN, np.array([r]), np.array([z]))[0]) + float(nfw_g(p, np.array([rr]))[0]) * z / rr) / KZU
    d["P1_Kz_over_2piG_Msun_pc2"] = kz
    zz = np.linspace(0, 20 * 0.9, 801)

    def sz(R, h):
        K = g.kz_sym(PhiN, PBN, np.full_like(zz[zz <= 20 * h], R), zz[zz <= 20 * h]) + nfw_g(p, np.hypot(R, zz[zz <= 20 * h])) * zz[zz <= 20 * h] / np.hypot(R, zz[zz <= 20 * h])
        zh = zz[zz <= 20 * h]
        return math.sqrt(np.trapz(np.exp(-zh / h) * K, zh))
    d["P4_sigma_z_kms"] = {f"h{h}": {f"R{r:.0f}": sz(r, h) for r in RKZ} for h in (0.30, 0.90)}
    rhoD = float(nfw_rho(p, np.array([R0]))[0])
    zw = np.linspace(-1.1, 1.1, 441)
    col = float(np.trapz(nfw_rho(p, np.hypot(R0, zw)), zw))
    rb = mw.rho(s); j = g.jc
    colb = float(sum(np.interp(R0, g.Rc, rb[:, jj]) * max(min(g.ze[jj + 1], 1.1) - max(g.ze[jj], -1.1), 0) for jj in range(g.nz)))
    d["P3"] = dict(dark_Msun_pc3=rhoD / 1e9, dark_GeV_cm3=rhoD / 1e9 * GEV_PER_MSUNPC3,
                   Kz_R0_1p1_over_2piG=(float(g.kz_sym(PhiN, PBN, np.array([R0]), np.array([1.1]))[0])
                                        + float(nfw_g(p, np.array([math.hypot(R0, 1.1)]))[0]) * 1.1 / math.hypot(R0, 1.1)) / KZU,
                   Sigma_tot_1p1_Msun_pc2=(colb + col) / 1e6, Sigma_dark_1p1_Msun_pc2=col / 1e6,
                   rho_tot_R0_Msun_pc3=(float(np.interp(R0, g.Rc, rb[:, j])) + rhoD) / 1e9)
    V5 = np.sqrt(mw.gN_plane(s, R5) * R5 + R5 * nfw_g(p, R5)); d["P5_Vc"] = dict(zip([f"R{r:.0f}" for r in R5], V5.tolist()))
    rr = np.arange(30.0, 60.01, 2.5); d["P5_mean_30_60"] = float(np.mean(np.sqrt(mw.gN_plane(s, rr) * rr + rr * nfw_g(p, rr))))
    SEAL["NFW_Ou24"][sk] = d
P(f"  NFW rival done ({time.time() - T0:.0f} s)")

# ------------------------------------------------------------------ C4: consistency with Part A
JA = os.path.join(HERE, f"s3_partA_mw_results{TAG}.json")
if os.path.exists(JA):
    A = json.load(open(JA))
    worst = 0.0
    for foot in FOOTS:
        v20 = SEAL["v3"][foot][f"{1.0:.6f}"]["P2_Vc_gamma0_exact"]["R20"]
        worst = max(worst, abs(v20 - A["steps"]["AQ_gamma0"][foot]["cells"]["Ou24"]["V20_census"]))
    check("C4", worst <= 1e-9, f"seal's gamma-0 V_c(20 kpc) equals Part A's AQ_gamma0 V20 (max |d| {worst:.1e} km/s)")
else:
    check("C4", False, "Part A results JSON missing")

# ------------------------------------------------------------------ required precisions (CFG553 s4) for the scalars
def band(vals):
    return [float(min(vals)), float(max(vals))]


def scal(model, foot, path):
    out = []
    for s in SS:
        d = SEAL[model][foot][f"{s:.6f}"] if model != "NFW_Ou24" else SEAL[model][f"{s:.6f}"]
        for k in path:
            d = d[k]
        out.append(float(d))
    return out


REQ = {}
for foot in FOOTS:
    for nm, pF, pR in (("slope_15_27p5", ["P2_slope_15_27p5"], ["P2_slope_15_27p5"]), ("slope_15_22", ["P2_slope_15_22"], ["P2_slope_15_22"]),
                       ("Kz_R0_1p1", ["P3", "Kz_R0_1p1_over_2piG"], ["P3", "Kz_R0_1p1_over_2piG"]),
                       ("V60", ["P5_Vc_anticentre_wedge", "R60"], ["P5_Vc", "R60"]),
                       ("mean_30_60", ["P5_mean_30_60_wedge"], ["P5_mean_30_60"])):
        F = scal("v3", foot, pF); Rv = scal("NFW_Ou24", foot, pR)
        Fb, Rb = band(F), band(Rv); Fc, Rc = F[2], Rv[2]
        if Rb[0] <= Fc <= Rb[1] or Fb[0] <= Rc <= Fb[1]:
            req = "NOT SEPARABLE"
        else:
            req = dict(sigma_req_F=min(abs(Fc - Rb[0]), abs(Fc - Rb[1])) / 3, sigma_req_R=min(abs(Rc - Fb[0]), abs(Rc - Fb[1])) / 3)
        REQ[f"{foot}|{nm}"] = dict(F_band=Fb, F_central=Fc, R_band=Rb, R_central=Rc, required=req)
SEAL["required_precision"] = REQ

# ------------------------------------------------------------------ outputs
RES = dict(lane="S3_v3_mw_seals", part="C", mutate=S.MUTATE, criteria="8f6c6587e1", amendments=["A1 0501ac4248", "A2 938675e060", "A3 94a73d19b0"],
           C5=pc, use3d=USE3D, checks=CHECKS)
blob = json.dumps(SEAL, sort_keys=True, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)).encode()
sha = hashlib.sha256(blob).hexdigest()
RES["sha256_this_run"] = sha
prev_hash_file = os.path.join(HERE, "PREDICTIONS_V3_HASH.txt")
npass = sum(c["ok"] for c in CHECKS)
if os.environ.get("S3_C1_COMPARE"):
    ref = open(prev_hash_file).read().split()[0] if os.path.exists(prev_hash_file) else None
    check("C1", ref == sha, f"independent rerun (independent cache directory '{os.path.basename(S.CACHE.rstrip('/'))}', populated from scratch by this check's first run) hash {sha} vs sealed {ref}")
    npass = sum(c["ok"] for c in CHECKS)
elif not S.MUTATE and npass == len(CHECKS) and os.path.exists(prev_hash_file):
    ref = open(prev_hash_file).read().split()[0]
    P(f"seal exists (never overwritten): recomputed hash {sha} {'EQUALS' if ref == sha else 'DIFFERS FROM'} the sealed {ref}")
elif not S.MUTATE and npass == len(CHECKS):
    open(os.path.join(HERE, "SEALED_V3_MW_DR4.json"), "wb").write(blob)
    open(prev_hash_file, "w").write(f"{sha}  SEALED_V3_MW_DR4.json\n")
    P(f"SEALED_V3_MW_DR4.json sha256 = {sha}")
else:
    P("nothing sealed (MUTATE or a failed check)")
RES["runtime_s"] = round(time.time() - T0, 1)
RES["peak_rss_MB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6, 1)
RES["child_rss_MB"] = RSS
suffix = "_C1RERUN" if os.environ.get("S3_C1_COMPARE") else ""
json.dump(RES, open(os.path.join(HERE, f"s3_partC_seal_results{TAG}{suffix}.json"), "w"), indent=1, default=str)
# headline lines
for foot in FOOTS:
    d = SEAL["v3"][foot][f"{1.0:.6f}"]; di = SEAL["v3_isolated"][foot][f"{1.0:.6f}"]; dn = SEAL["NFW_Ou24"][f"{1.0:.6f}"]
    P(f"  {foot:<9} v3: V20 wedge {d['P2_Vc_anticentre_wedge']['R20']:.1f} | slope 15-27.5 {d['P2_slope_15_27p5']:+.3f} (gamma0 {d['P2_slope_15_27p5_gamma0']:+.3f}; isolated {di['P2_slope_15_27p5']:+.3f}; NFW {dn['P2_slope_15_27p5']:+.3f}) | "
      f"Kz(R0,1.1)/2piG {d['P3']['Kz_R0_1p1_over_2piG']:.1f} (NFW {dn['P3']['Kz_R0_1p1_over_2piG']:.1f}) | phantom(R0) {d['P3']['phantom_mid_GeV_cm3']:.2f} GeV/cm3 | "
      f"V60 wedge {d['P5_Vc_anticentre_wedge']['R60']:.1f} mean {d['P5_Vc_azimuthal_mean']['R60']:.1f} (isolated {di['P5_Vc']['R60']:.1f}; NFW {dn['P5_Vc']['R60']:.1f}) | "
      f"P6 A(20/30/60) {d['P6_asymmetry_A']['R20']:.3f}/{d['P6_asymmetry_A']['R30']:.3f}/{d['P6_asymmetry_A']['R60']:.3f}")
P(f"\nS3_PARTC COMPLETE: {npass}/{len(CHECKS)} checks PASS.  runtime {RES['runtime_s']} s, parent peak RSS {RES['peak_rss_MB']} MB, child peaks {RSS}")
open(os.path.join(HERE, f"s3_partC_seal{TAG}{suffix}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHECKS) else 1)
