#!/usr/bin/env python3
"""CFG532: the Gaia-era Milky Way rotation curves (the 'Keplerian decline' debate, Melchiorri & Ruchika arXiv:2608.10189)
against the law with census baryons HELD.

Frozen criteria: FROZEN_CRITERIA.md (committed alone first, 9d73cbc17).
Curves (on disk only): C1 Ou+2024 Table 1, C2 Eilers+2019 Table 1, C3 the review's own 35-entry compilation (cross-check).
Law: the round cold-energy rule (CFG516) in both definitions RM-v and RM-phi; ALG reference; nu_mono; both footings.
Baryons held: B1 McMillan17 (census stars 5.43 +- 0.57e10 + gas); B2 6.0e10 and B2b 7.3e10 declared variants.
Machinery: CFG514's solver/baryons and CFG516's Base/build_PD, executed read-only from their committed files.
MUTATE (CFG532_MUTATE=1): M1 law off; M2 law on with B1 x 0.5. Exit 1 = DETECTED.
kappa = 1/2 is FITTED; cold energy mass still required; not theory closed.
Run: nice -n 10 python3 cfg532_mw_curves.py   (2 threads)
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "2"
import sys, json, math, time, re, io, contextlib
import numpy as np
from scipy.optimize import least_squares, minimize_scalar
from scipy.stats import chi2 as chi2dist

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data")
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
REVIEW_TEX = os.path.join(EXT, "cfg532_work", "src", "MW_RC_review_corrected_6_11.tex")
MUTATE = os.environ.get("CFG532_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""

# ------------------------------------------------------------------ re-used machinery (read-only exec)
SRC516 = os.path.join(HERE, "..", "CFG516_round_cold_energy", "cfg516_mw.py")
src = open(SRC516).read()
head = src.split("# ------------------------------------------------------------------ controls")[0]
ns = {"__file__": os.path.abspath(SRC516)}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(head, "cfg516_head", "exec"), ns)
G, A0, GR, nu_mono = ns["G"], ns["A0"], ns["GR"], ns["nu_mono"]
Base, build_PD, flux_mass, Mtab, RS = ns["Base"], ns["build_PD"], ns["flux_mass"], ns["Mtab"], ns["RS"]
rho_b2, rho_mcm = ns["rho_b2"], ns["rho_mcm"]
nfw_params, nfw_g = ns["nfw_params"], ns["nfw_g"]
EIL_R_K1, EIL_V_K1, EIL_E_K1 = ns["EIL_R"], ns["EIL_V"], ns["EIL_E"]
NS514 = ns["ns"]  # CFG514 namespace (cfg516 exec'd it into its own "ns")
FOOTS = ("canonical", "alt")
MSTAR_CENSUS, MSTAR_ERR = 5.43e10, 0.57e10

OUT, CHECKS = [], []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); OUT.append(s)


def check(cond, msg):
    CHECKS.append((bool(cond), msg)); P(f"  [{'PASS' if cond else 'FAIL'}] {msg}")
    return bool(cond)


T0 = time.time()
P("=" * 112)
P(f"CFG532  Gaia-era MW rotation curves vs the law with census baryons HELD   {'*** MUTATE ***' if MUTATE else 'PRIMARY'}")
P("kappa = 1/2 FITTED; footings 9.36e-11 / 1.13e-10 never pooled; nu_mono; cold energy mass still required")
P("=" * 112)

# ------------------------------------------------------------------ data
def load_tsv(path):
    rows = [l.split() for l in open(path) if l.strip() and not l.startswith("#")]
    hdr = rows[0]; arr = np.array([[float(x) for x in r] for r in rows[1:]])
    return {h: arr[:, i] for i, h in enumerate(hdr)}


def parse_compilation(path):
    t = open(path).read()
    blk = t.split(r"\label{tab:rc_data}")[1].split(r"\bottomrule")[0].split(r"\midrule")[1]
    rows = []
    for line in blk.split(r"\\"):
        cells = [c.strip() for c in line.replace("\n", " ").split("&")]
        for k in range(0, len(cells) - 2, 3):
            try:
                rows.append((float(cells[k]), float(cells[k + 1]), float(cells[k + 2])))
            except ValueError:
                pass
    a = np.array(sorted(rows))
    return a[:, 0], a[:, 1], a[:, 2]


ou = load_tsv(os.path.join(DATA, "mw_rc_ou2024_table1.tsv"))
el = load_tsv(os.path.join(DATA, "mw_rc_eilers2019_table1.tsv"))
OU_R, OU_V, OU_RAND = ou["R_kpc"], ou["vc_kms"], 0.5 * (ou["sig_plus"] + ou["sig_minus"])
EL_R, EL_V, EL_RAND = el["R_kpc"], el["vc_kms"], 0.5 * (el["sig_plus"] + el["sig_minus"])
CR, CV, CE = parse_compilation(REVIEW_TEX)


def ou_err(V, R, inner=0.03):
    return np.hypot(OU_RAND, np.where(R <= 22.0, inner, 0.15) * V)


CURVES = {
    "C1_Ou24": dict(R=OU_R, V=OU_V, E=ou_err(OU_V, OU_R), R0=8.178, rand=OU_RAND),
    "C2_Eilers19": dict(R=EL_R, V=EL_V, E=np.hypot(EL_RAND, 0.03 * EL_V), R0=8.122, rand=EL_RAND),
    "C3_review_compilation": dict(R=CR, V=CV, E=CE, R0=8.178, rand=None),
}
m3d = CR <= 26.5
CURVES["C3d_compilation_R<=26.5"] = dict(R=CR[m3d], V=CV[m3d], E=CE[m3d], R0=8.178, rand=None)
for k, c in CURVES.items():
    P(f"  {k:<26} N = {len(c['R']):2d}  R = {c['R'].min():.2f}-{c['R'].max():.2f} kpc  R0 = {c['R0']}")

# ------------------------------------------------------------------ baryons
P("\n--- baryons (grid; held)")
rho_stars = NS514["rho_stars_only"]
b_st = Base("B1_stars", rho_stars)
b_gas = Base("B1_gas", lambda R, z: rho_mcm(R, z) - rho_stars(R, z))
b_b2 = Base("B2_6.0e10", lambda R, z: rho_b2(R, z, 6.0e10))
b_b2b = Base("B2b_7.3e10", lambda R, z: rho_b2(R, z, 7.3e10))
MSTAR_GRID = b_st.Mb
P(f"  B1 McMillan17 grid: stars {b_st.Mb:.4e}, gas {b_gas.Mb:.4e}, total {b_st.Mb + b_gas.Mb:.4e} Msun "
  f"(census stars {MSTAR_CENSUS:.2e} +- {MSTAR_ERR:.2e}); B2 {b_b2.Mb:.4e}, B2b {b_b2b.Mb:.4e}")
ZC0 = GR.zc[0]


class Mix:
    """linear mix of Newtonian bases: rho = sum c_i rho_i (fields, enclosed masses and boundary potentials are linear)."""

    def __init__(self, parts):
        self.parts = [(b, c) for b, c in parts if c != 0]
        self.rho = sum(c * b.rho for b, c in self.parts)
        self.Mb = sum(c * b.Mb for b, c in self.parts)
        self.Phi = sum(c * b.Phi for b, c in self.parts)
        self.pR = sum(c * b.pR for b, c in self.parts)
        self.pZ = sum(c * b.pZ for b, c in self.parts)
        self.Menc = sum(c * b.Menc for b, c in self.parts)
        self.gNplane = sum(c * b.gNplane for b, c in self.parts)

    def gN(self, R):
        R = np.asarray(R, float)
        return sum(c * b.m.gRz(R, np.full_like(R, ZC0))[0] for b, c in self.parts)


_PDCACHE = {}


def v_model(kind, mix, key, foot, R):
    """in-plane circular speed. kind: N (Newtonian), ALG, RMv, RMphi."""
    R = np.asarray(R, float)
    gN = mix.gN(R)
    if kind == "N":
        return np.sqrt(np.maximum(R * gN, 0))
    a0 = A0[foot]
    if kind == "ALG":
        return np.sqrt(np.maximum(R * nu_mono(np.abs(gN) / a0) * np.abs(gN), 0))
    if kind == "RMv":
        g = np.abs(mix.gNplane)
        Mc = RS * (RS * nu_mono(g / a0) * g) / G - mix.Menc
    elif kind == "RMphi":
        ck = (key, foot)
        if ck not in _PDCACHE:
            pd, _ = build_PD(mix, 1.0, foot)
            _PDCACHE[ck] = flux_mass(pd.gm.gRz, RS) - mix.Menc
        Mc = _PDCACHE[ck]
    else:
        raise ValueError(kind)
    return np.sqrt(np.maximum(R * gN + G * Mtab(Mc, R) / R, 0))


def b1mix(s=1.0, scale=1.0):
    return Mix([(b_st, s * scale), (b_gas, scale)]), f"B1_s{s:.5f}_x{scale:.3f}"


def chi2(v, c, E=None):
    E = c["E"] if E is None else E
    return float(np.sum(((v - c["V"]) / E) ** 2))


def pval(x, dof):
    return float(chi2dist.sf(x, max(dof, 1)))


def slope(R, V, E, lo=15.0, hi=27.5):
    m = (R >= lo) & (R <= hi)
    x, y, w = np.log(R[m]), np.log(V[m]), (V[m] / E[m]) ** 2
    A = np.vstack([np.ones_like(x), x]).T
    C = np.linalg.inv(A.T @ (A * w[:, None]))
    beta = C @ (A.T @ (w * y))
    return float(beta[1]), float(math.sqrt(C[1, 1])), int(m.sum())


# ------------------------------------------------------------------ controls
P("\n--- controls")
m1, k1 = b1mix(1.0)
ref = {("RMphi", "canonical"): 425.79160083344334, ("RMphi", "alt"): 186.23356268194124,
       ("RMv", "canonical"): 62.143743385244626, ("RMv", "alt"): 18.554399914300035}
k1dev = 0.0
for (kind, foot), x in ref.items():
    v = v_model(kind, m1, k1, foot, EIL_R_K1)
    c2 = float(np.sum(((v - EIL_V_K1) / EIL_E_K1) ** 2))
    k1dev = max(k1dev, abs(c2 / x - 1))
    P(f"    K1 {kind:<5} {foot:<9} chi2 vs Eilers (CFG514 errors) {c2:8.2f}  CFG516 {x:8.2f}")
check(k1dev < 0.01, f"K1 CFG516's RM chi2_RC vs Eilers reproduced (max dev {k1dev:.3%} < 1%)")
check(len(CR) == 35 and abs(CR.min() - 6.3) < 1e-9 and abs(CR.max() - 49.0) < 1e-9,
      f"K2 compilation parser: {len(CR)} rows, {CR.min()}-{CR.max()} kpc")
Rt = np.linspace(15, 27.5, 12)
bk, _, _ = slope(Rt, 200 * (Rt / 15) ** -0.5, np.full(12, 5.0)); bf, _, _ = slope(Rt, np.full(12, 200.0), np.full(12, 5.0))
check(abs(bk + 0.5) < 1e-6 and abs(bf) < 1e-6, f"K3 slope estimator: Kepler {bk:+.7f}, flat {bf:+.7f}")

# ------------------------------------------------------------------ comparators
def fit_nfw(c, mixN):
    vb2 = mixN.gN(c["R"]) * c["R"]

    def res(x):
        p = nfw_params(10 ** x[0], x[1])
        return (np.sqrt(np.maximum(vb2 + c["R"] * nfw_g(p, c["R"]), 0)) - c["V"]) / c["E"]
    best = None
    for lm0 in (11.0, 11.7, 12.3):
        for c0 in (5.0, 12.0, 25.0):
            f = least_squares(res, x0=[lm0, c0], bounds=([10.0, 1.0], [13.5, 60.0]))
            if best is None or f.cost < best.cost:
                best = f
    p = nfw_params(10 ** best.x[0], best.x[1])
    return dict(M200=float(10 ** best.x[0]), c=float(best.x[1]), chi2=float(2 * best.cost), p=pval(2 * best.cost, len(c["R"]) - 2),
                vfun=lambda R: np.sqrt(np.maximum(mixN.gN(R) * R + R * nfw_g(p, R), 0)))


def fit_kepler(c, Rmin=19.0):
    m = c["R"] >= Rmin
    R, V, E = c["R"][m], c["V"][m], c["E"][m]
    # V = sqrt(GM/R): linear in sqrt(M)
    f = minimize_scalar(lambda lm: np.sum(((np.sqrt(G * 10 ** lm / R) - V) / E) ** 2), bounds=(10, 13), method="bounded")
    c2 = float(f.fun)
    return dict(M=float(10 ** f.x), chi2=c2, n=int(m.sum()), p=pval(c2, m.sum() - 1))


# ------------------------------------------------------------------ verdict machinery
ORDER = {"CONSISTENT": 0, "NOT DIAGNOSTIC": 1, "NEEDS-HEAVY-DISC": 2, "EXCLUDED": 3}


def score(kind, foot, c, scale=1.0, E=None, Rscale=1.0):
    """census (B1 x scale) score, post hoc s*, shape; verdict per Sec. 4."""
    cc = dict(c); cc["R"] = c["R"] * Rscale
    if E is not None:
        cc["E"] = E
    N = len(cc["R"])
    bd, sb, nsl = slope(cc["R"], cc["V"], cc["E"])
    mx, key = b1mix(1.0, scale)
    v0 = v_model(kind, mx, key, foot, cc["R"])
    c0 = chi2(v0, cc); p0 = pval(c0, N)
    b0, _, _ = slope(cc["R"], v0, cc["E"])
    out = dict(N=N, chi2_census=c0, p_census=p0, slope_data=bd, slope_err=sb, n_slope=nsl, slope_census=b0,
               dslope_census_sig=(bd - b0) / sb, V20_census=float(v_model(kind, mx, key, foot, np.array([20.0]))[0]))

    def f(s):
        m, k = b1mix(s, scale)
        return chi2(v_model(kind, m, k, foot, cc["R"]), cc)
    fr = minimize_scalar(f, bounds=(0.25, 4.0), method="bounded", options=dict(xatol=1e-3))
    s = float(fr.x); cs = float(fr.fun)
    ms, ks = b1mix(s, scale)
    vs = v_model(kind, ms, ks, foot, cc["R"])
    bs, _, _ = slope(cc["R"], vs, cc["E"])
    Mneed = s * scale * MSTAR_CENSUS
    out.update(s_star=s, chi2_s=cs, p_s=pval(cs, N - 1), Mstar_need=Mneed, z_need=(Mneed - MSTAR_CENSUS) / MSTAR_ERR,
               slope_s=bs, dslope_s_sig=(bd - bs) / sb, at_bound=bool(s < 0.26 or s > 3.99))
    shape_nd = bool(2 * sb > abs(b0 + 0.5))
    shape_ok0 = abs(out["dslope_census_sig"]) <= 2
    shape_oks = abs(out["dslope_s_sig"]) <= 2
    if p0 >= 0.01 and shape_ok0:
        v = "NOT DIAGNOSTIC" if shape_nd else "CONSISTENT"
    elif s > 1 and out["p_s"] >= 0.01 and shape_oks and not out["at_bound"]:
        v = "NEEDS-HEAVY-DISC"
    else:
        v = "EXCLUDED"
    out.update(shape_not_diagnostic=shape_nd, verdict=v)
    return out


def fmt(o):
    z = f" z_need {o['z_need']:+.1f}" if o["verdict"] == "NEEDS-HEAVY-DISC" else ""
    return (f"chi2 {o['chi2_census']:8.1f}/{o['N']} p {o['p_census']:.1e} | s* {o['s_star']:.3f} M*need {o['Mstar_need']:.2e} "
            f"(z {o['z_need']:+.1f}) chi2* {o['chi2_s']:6.1f} p* {o['p_s']:.2f} | slope data {o['slope_data']:+.3f}+-{o['slope_err']:.3f} "
            f"law {o['slope_census']:+.3f} ({o['dslope_census_sig']:+.1f}sig) @s* {o['slope_s']:+.3f} ({o['dslope_s_sig']:+.1f}sig)"
            f"{' [shape ND]' if o['shape_not_diagnostic'] else ''} -> {o['verdict']}{z}")


RES = dict(mutate=MUTATE, curves={k: dict(N=len(c["R"]), Rmin=float(c["R"].min()), Rmax=float(c["R"].max()), R0=c["R0"])
                                   for k, c in CURVES.items()},
           baryons=dict(B1_stars_grid=float(b_st.Mb), B1_gas_grid=float(b_gas.Mb), B2=float(b_b2.Mb), B2b=float(b_b2b.Mb),
                        census_stars=MSTAR_CENSUS, census_err=MSTAR_ERR),
           cells={}, comparators={}, variants={}, systematics={}, overall={}, dr4={}, mutate_rows={})

if MUTATE:
    P("\n--- MUTATE M1: law OFF (Newtonian B1, held); M2: law ON with B1 x 0.5")
    det = []
    for foot in FOOTS:
        for cn in ("C1_Ou24", "C2_Eilers19"):
            c = CURVES[cn]
            o = score("N", foot, c)
            P(f"  M1 {cn:<12} {foot:<9} {fmt(o)}")
            RES["mutate_rows"][f"M1|{cn}|{foot}"] = o
            det.append(o["p_census"] < 1e-6)
            for kind in ("RMv", "RMphi"):
                o = score(kind, foot, c, scale=0.5)
                P(f"  M2 {cn:<12} {foot:<9} {kind:<5} {fmt(o)}")
                RES["mutate_rows"][f"M2|{cn}|{foot}|{kind}"] = o
                det.append(o["p_census"] < 1e-6 and o["verdict"] != "CONSISTENT")
    detected = all(det)
    check(detected, f"MUTATE DETECTED in {sum(det)}/{len(det)} cells (M1 p_census < 1e-6; M2 p_census < 1e-6 and not CONSISTENT)")
    RES["mutate_detected"] = detected
else:
    P("\n--- K4 / comparators: NFW (B1 Newtonian + NFW, 2 free), Kepler (R >= 19), Newtonian baryons alone")
    mN, _ = b1mix(1.0)
    for cn, c in CURVES.items():
        nf = fit_nfw(c, mN)
        kp = fit_kepler(c)
        vN = v_model("N", mN, "B1N", "canonical", c["R"])
        cN = chi2(vN, c)
        bd, sb, _ = slope(c["R"], c["V"], c["E"])
        bn, _, _ = slope(c["R"], nf["vfun"](c["R"]), c["E"])
        m19 = c["R"] >= 19
        c19 = dict(R=c["R"][m19], V=c["V"][m19], E=c["E"][m19])
        nf19 = chi2(nf["vfun"](c19["R"]), c19)
        RES["comparators"][cn] = dict(NFW=dict(M200=nf["M200"], c=nf["c"], chi2=nf["chi2"], p=nf["p"], slope=bn,
                                                dslope_sig=(bd - bn) / sb, chi2_R19=nf19),
                                      Kepler=kp, Newton_B1=dict(chi2=cN, p=pval(cN, len(c["R"]))),
                                      slope_data=bd, slope_err=sb, slope_kepler_sig=(bd + 0.5) / sb, slope_flat_sig=bd / sb)
        P(f"  {cn:<26} NFW M200 {nf['M200']:.2e} c {nf['c']:5.1f} chi2 {nf['chi2']:7.1f} p {nf['p']:.2f} slope {bn:+.3f} "
          f"({(bd - bn) / sb:+.1f}sig) | Kepler(R>=19, n={kp['n']}) M {kp['M']:.2e} chi2 {kp['chi2']:6.1f} p {kp['p']:.2f} | "
          f"Newton B1 chi2 {cN:8.1f} | data slope {bd:+.3f}+-{sb:.3f} (Kepler {(bd + 0.5) / sb:+.1f}sig, flat {bd / sb:+.1f}sig)")
        if cn == "C1_Ou24":
            check(nf["chi2"] < cN, f"K4 NFW improves on Newtonian baryons for Ou+24 ({nf['chi2']:.1f} < {cN:.1f})")

    P("\n--- law cells (B1 census held; s* post hoc, reported only)")
    for foot in FOOTS:
        for kind in ("RMv", "RMphi", "ALG"):
            for cn, c in CURVES.items():
                o = score(kind, foot, c)
                m19 = c["R"] >= 19
                mx, key = b1mix(1.0)
                o["chi2_R19_census"] = chi2(v_model(kind, mx, key, foot, c["R"][m19]),
                                            dict(V=c["V"][m19], E=c["E"][m19]))
                o["n_R19"] = int(m19.sum())
                RES["cells"][f"{cn}|{foot}|{kind}"] = o
                P(f"  {foot:<9} {kind:<5} {cn:<26} {fmt(o)}  [chi2(R>=19) {o['chi2_R19_census']:.1f}/{o['n_R19']}]")

    P("\n--- declared baryon variants B2 6.0e10 / B2b 7.3e10 (held; no verdict)")
    for foot in FOOTS:
        for kind in ("RMv", "RMphi", "ALG"):
            for bn_, bb in (("B2", b_b2), ("B2b", b_b2b)):
                mx = Mix([(bb, 1.0)])
                for cn in ("C1_Ou24", "C2_Eilers19", "C3_review_compilation"):
                    c = CURVES[cn]
                    v = v_model(kind, mx, bn_, foot, c["R"])
                    x = chi2(v, c); bm, _, _ = slope(c["R"], v, c["E"]); bd, sb, _ = slope(c["R"], c["V"], c["E"])
                    RES["variants"][f"{bn_}|{cn}|{foot}|{kind}"] = dict(chi2=x, p=pval(x, len(c["R"])), slope=bm,
                                                                         dslope_sig=(bd - bm) / sb,
                                                                         V20=float(v_model(kind, mx, bn_, foot, np.array([20.0]))[0]))
                    P(f"  {foot:<9} {kind:<5} {bn_:<3} {cn:<22} chi2 {x:8.1f}/{len(c['R'])} p {pval(x, len(c['R'])):.1e} "
                      f"slope {bm:+.3f} ({(bd - bm) / sb:+.1f}sig)")

    P("\n--- overall (worse of C1, C2; C3 cross-check)")
    for foot in FOOTS:
        for kind in ("RMv", "RMphi"):
            cs = [RES["cells"][f"{cn}|{foot}|{kind}"] for cn in ("C1_Ou24", "C2_Eilers19")]
            w = max(cs, key=lambda o: (ORDER[o["verdict"]], o["z_need"]))
            c3 = RES["cells"][f"C3_review_compilation|{foot}|{kind}"]["verdict"]
            c3d = RES["cells"][f"C3d_compilation_R<=26.5|{foot}|{kind}"]["verdict"]
            zmax = max(o["z_need"] for o in cs)
            RES["overall"][f"{foot}|{kind}"] = dict(verdict=w["verdict"], z_need_max=zmax,
                                                    per_curve=[o["verdict"] for o in cs], C3=c3, C3d=c3d,
                                                    C3_agrees=bool(c3 == w["verdict"]))
            P(f"  {foot:<9} {kind:<5} OVERALL {w['verdict']}  (Ou {cs[0]['verdict']}, Eilers {cs[1]['verdict']}; "
              f"max z_need {zmax:+.1f}) | C3 {c3}, C3d {c3d}")

    P("\n--- systematics S1 random-only, S2 5% inner, S3 R0 rescale (crude)")
    for foot in FOOTS:
        for kind in ("RMv", "RMphi"):
            for cn in ("C1_Ou24", "C2_Eilers19"):
                c = CURVES[cn]
                base_v = RES["cells"][f"{cn}|{foot}|{kind}"]["verdict"]
                rows = {}
                rows["S1_random_only"] = score(kind, foot, c, E=c["rand"])
                if cn == "C1_Ou24":
                    rows["S2_5pct_inner"] = score(kind, foot, c, E=ou_err(c["V"], c["R"], inner=0.05))
                else:
                    rows["S2_5pct"] = score(kind, foot, c, E=np.hypot(c["rand"], 0.05 * c["V"]))
                for r0p in (8.122, 8.178, 8.34):
                    if abs(r0p - c["R0"]) > 1e-6:
                        rows[f"S3_R0_{r0p}"] = score(kind, foot, c, Rscale=r0p / c["R0"])
                for k, o in rows.items():
                    flip = o["verdict"] != base_v
                    o["flips"] = flip
                    P(f"  {foot:<9} {kind:<5} {cn:<12} {k:<16} {fmt(o)}{'  <-- FLIP' if flip else ''}")
                RES["systematics"][f"{cn}|{foot}|{kind}"] = rows

    P("\n--- Gaia DR4 decider (release 2026-12-02)")
    Rg = np.array([15.0, 17.5, 20.0, 22.5, 25.0, 27.5])
    Eg = np.full_like(Rg, 1.0)
    for foot in FOOTS:
        for kind in ("RMv", "RMphi"):
            rows = {}
            sOu = RES["cells"][f"C1_Ou24|{foot}|{kind}"]["s_star"]
            for lab, mx, key in (("B1_census",) + b1mix(1.0), ("B2b_7.3e10", Mix([(b_b2b, 1.0)]), "B2b"),
                                 ("B1_s*_Ou",) + b1mix(sOu)):
                v = v_model(kind, mx, key, foot, Rg)
                bl, _, _ = slope(Rg, v, Eg * v / 100)
                rows[lab] = dict(V20=float(v[2]), V25=float(v[4]), V275=float(v[5]), slope=bl,
                                 sig_b_needed_vs_kepler_3sig=abs(bl + 0.5) / 3)
            for cn in ("C1_Ou24", "C2_Eilers19"):
                bd = RES["cells"][f"{cn}|{foot}|{kind}"]["slope_data"]
                rows[f"sig_b_needed_vs_{cn}_3sig"] = abs(bd - rows["B1_census"]["slope"]) / 3
                c = CURVES[cn]; m = np.abs(c["R"] - 20) <= 0.75
                rows[f"gap_V20_census_{cn}"] = float(np.mean(c["V"][m]) - rows["B1_census"]["V20"])
            RES["dr4"][f"{foot}|{kind}"] = rows
            r = rows["B1_census"]
            P(f"  {foot:<9} {kind:<5} census V(20/25/27.5) {r['V20']:.1f}/{r['V25']:.1f}/{r['V275']:.1f} slope {r['slope']:+.3f}; "
              f"7.3e10 slope {rows['B2b_7.3e10']['slope']:+.3f}; s*(Ou) slope {rows['B1_s*_Ou']['slope']:+.3f} | "
              f"sigma_b needed: vs Kepler {r['sig_b_needed_vs_kepler_3sig']:.3f}, vs Ou slope {rows['sig_b_needed_vs_C1_Ou24_3sig']:.3f}, "
              f"vs Eilers {rows['sig_b_needed_vs_C2_Eilers19_3sig']:.3f} | V20 gap (data-census) Ou {rows['gap_V20_census_C1_Ou24']:+.1f}, "
              f"Eilers {rows['gap_V20_census_C2_Eilers19']:+.1f} km/s")

if not MUTATE:
    P("\n--- POST-RUN diagnostics (added after the first run; NOT in the frozen criteria; no verdict input)")
    pr = {}
    # (a) the same frozen shape rule applied to the fitted NFW and to the Kepler fit
    for cn, c in RES["comparators"].items():
        pr[f"NFW_shape|{cn}"] = dict(dslope_sig=c["NFW"]["dslope_sig"], fails_2sig=bool(abs(c["NFW"]["dslope_sig"]) > 2))
        P(f"  (a) {cn:<26} fitted NFW slope offset {c['NFW']['dslope_sig']:+.1f} sigma -> "
          f"{'would FAIL' if abs(c['NFW']['dslope_sig']) > 2 else 'passes'} the frozen 2-sigma shape rule; "
          f"Kepler slope offset {c['slope_kepler_sig']:+.1f} sigma")
    # (b) Eilers' own slope systematic (dv/dR +-0.46 km/s/kpc) converted to dlnV/dlnR at R = 20, V = 200, added to the
    #     random-only slope error
    eS = 0.46 * 20.0 / 200.0
    for foot in FOOTS:
        for kind in ("RMv", "RMphi"):
            o = RES["systematics"][f"C2_Eilers19|{foot}|{kind}"]["S1_random_only"]
            sb = math.hypot(o["slope_err"], eS)
            d = (o["slope_data"] - o["slope_census"]) / sb
            pr[f"Eilers_gradsys|{foot}|{kind}"] = dict(slope_err=sb, dslope_sig=d)
            P(f"  (b) Eilers random-only slope {o['slope_data']:+.3f} +- {o['slope_err']:.3f} (+) gradient sys {eS:.3f} = {sb:.3f}: "
              f"{foot} {kind} law {o['slope_census']:+.3f} -> {d:+.1f} sigma")
    # (c) the law's steepest and shallowest 15-27.5 kpc slope across every scored cell (census, variants, s*)
    sl = [o["slope_census"] for o in RES["cells"].values()] + [o["slope_s"] for o in RES["cells"].values()] + \
         [o["slope"] for o in RES["variants"].values()]
    pr["law_slope_range"] = [float(min(sl)), float(max(sl))]
    P(f"  (c) the law's dlnV/dlnR (15-27.5 kpc) across all cells, baryon variants and s*: {min(sl):+.3f} to {max(sl):+.3f} "
      f"(Kepler -0.500; Ou data {RES['comparators']['C1_Ou24']['slope_data']:+.3f}, Eilers {RES['comparators']['C2_Eilers19']['slope_data']:+.3f})")
    RES["post_run"] = pr

RES["checks"] = [dict(ok=a, msg=b) for a, b in CHECKS]
RES["runtime_s"] = time.time() - T0
P(f"\nchecks: {sum(a for a, _ in CHECKS)}/{len(CHECKS)} pass; runtime {RES['runtime_s']:.0f} s")


def jc(o):
    if isinstance(o, dict):
        return {k: jc(v) for k, v in o.items() if not callable(v)}
    if isinstance(o, (list, tuple)):
        return [jc(v) for v in o]
    if isinstance(o, (np.floating, np.integer, np.bool_)):
        return o.item()
    return o


json.dump(jc(RES), open(os.path.join(HERE, f"cfg532_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg532{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUTATE:
    sys.exit(1 if RES.get("mutate_detected") else 0)
sys.exit(0 if all(a for a, _ in CHECKS) else 2)
