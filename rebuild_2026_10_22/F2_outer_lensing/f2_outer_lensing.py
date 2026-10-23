#!/usr/bin/env python3
"""F2_outer_lensing: from-scratch rebuild of the isolated-galaxy outer-lensing shortfall (CFG804 -> CFG902 -> CFG903).

Criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (e9816b47d2, committed alone before any script or number).
Run (from the repo root or anywhere):  OMP_NUM_THREADS=1 nice -n 15 python3 f2_outer_lensing.py [--mutate]
Outputs: f2_outer_lensing{,_MUTATE}.out, f2_outer_lensing_results{,_MUTATE}.json (in this lane).
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed.
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, math, time, resource
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import f2_aqual as AQ

np.seterr(all="ignore")
MUT = "--mutate" in sys.argv[1:]
SFX = "_MUTATE" if MUT else ""
T0 = time.time()
OUT, RES, CHK = [], {"lane": "F2_outer_lensing", "mutate": MUT}, {}


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, val, thr):
    CHK[name] = bool(ok)
    P(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")


DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
B21 = os.path.join(DATA, "brouwer2021_rar")
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
Gpc = 4.30091e-3                              # pc (km/s)^2 / Msun
def a0u(foot): return A0[foot] * 3.0857e16 / 1e6   # (km/s)^2 / pc

# ============================================================================ 1. B21 Fig. 3 data (Track A)
R, Y = [], []
for b in range(1, 5):
    d = np.loadtxt(os.path.join(B21, f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt"))
    R.append(d[:, 0]); Y.append(d[:, 1] / d[:, 4])
R, Y = np.array(R), np.array(Y)
if MUT:
    Y = Y * 1.10                              # MUTATE: must break K0
c = np.loadtxt(os.path.join(B21, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt")); mins = sorted(set(c[:, 0]))
C = np.zeros((60, 60))
for row in c:
    m, n = mins.index(row[0]), mins.index(row[1])
    i, j = int(np.argmin(abs(R[0] - row[2]))), int(np.argmin(abs(R[0] - row[3])))
    C[m * 15 + i, n * 15 + j] = row[4] / row[6]
RB = R[0].copy()                              # B21 radius labels (h70^-1 Mpc); ranges are defined on these labels
IDX_ALL = list(range(15)); IDX_PRIM = [i for i in range(15) if RB[i] <= 0.31]
IDX_IN = IDX_PRIM; IDX_O1 = [i for i in range(15) if 0.4 < RB[i] < 1.1]; IDX_O2 = [i for i in range(15) if RB[i] > 1.1]
IDX_OUT = IDX_O1 + IDX_O2
assert len(IDX_O1) == 4 and len(IDX_O2) == 3


def sel_of(idx):
    return np.concatenate([np.array(idx) + 15 * b for b in range(4)])


def chi2_vec(y, m, idx, Cm=None):
    s = sel_of(idx); r = (y.ravel() - m.ravel())[s]
    if not np.all(np.isfinite(r)): return float("inf")
    return float(r @ np.linalg.solve((C if Cm is None else Cm)[np.ix_(s, s)], r))


def gls_amp(y, m, idx, Cm=None):
    """GLS amplitude A of data = A * model on the selected points, and its sigma."""
    s = sel_of(idx); Cs = (C if Cm is None else Cm)[np.ix_(s, s)]
    mm = m.ravel()[s]; yy = y.ravel()[s]
    Ci_m = np.linalg.solve(Cs, mm)
    F = float(mm @ Ci_m)
    return float(yy @ Ci_m) / F, 1.0 / math.sqrt(F)


# ============================================================================ 2. K0: record reproduction (own re-implementation)
SUP = 5.364; FB = 1 / (1 + SUP); SHIFT = math.log10(0.674)
def fret_of(lM):
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)
def N_decl(logMb):
    f = 0.10
    for _ in range(200):
        lMta = logMb - math.log10(f * FB) + SHIFT; fn = fret_of(lMta)
        if abs(fn - f) < 1e-12: break
        f = 0.5 * (f + fn)
    return 1 / f
edge_of = lambda N: math.sqrt(((2 * SUP * N + 1) ** 2 - 1) / 4)
NGRID = np.round(np.concatenate([[1.0], np.arange(2.0, 10.01, 0.25)]), 2)
SG = np.logspace(-4, 6, 4001)                 # dimensionless s = r / r_M
# K0 uses the record's numerical scheme (projected law density on a 600-point log grid, log interpolation),
# re-implemented here; the rebuild itself uses f2_aqual.delta_sigma.
from scipy.integrate import quad
XK = np.logspace(-3, 3, 600)
rho_law = lambda s: 1.0 / (2 * math.pi * s * math.sqrt(1 + 4 * s * s))
_SH = {}
def shape_rec(smax):
    if smax in _SH: return _SH[smax]
    Sig = np.empty_like(XK)
    for i, x in enumerate(XK):
        if smax is not None and x >= smax:
            Sig[i] = 0.0; continue
        tm = math.sqrt(smax ** 2 - x * x) if smax is not None else np.inf
        Sig[i] = 2 * quad(lambda t: rho_law(math.hypot(x, t)), 0, tm, limit=300)[0]
    integ = 2 * math.pi * XK ** 2 * Sig
    M0 = math.pi * XK[0] ** 2 * Sig[0]
    Mc = np.concatenate([[M0], M0 + np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(np.log(XK)))])
    _SH[smax] = np.maximum(Mc / (math.pi * XK ** 2) - Sig + 1.0 / (math.pi * XK ** 2), 1e-30)
    return _SH[smax]
def shape_ds(x, smax):
    """Delta Sigma / (M/r_M^2) at x = R/r_M for the law truncated at sphere radius smax (None: no edge)."""
    return np.exp(np.interp(np.log(x), np.log(XK), np.log(shape_rec(smax))))
GRID = np.round(np.arange(9.0, 12.0001, 0.01), 2); ZK = [10.14, 10.46, 10.70, 10.89]


def build_table(foot, kind, Rphys, gscale=1.0):
    """model table T[g, b, i] for log M_b on GRID at data radii (Mpc); kind 'B' or 'D'."""
    a0 = a0u(foot); T = np.empty((len(GRID), 4, 15)); cache = {}
    for gi, lm in enumerate(GRID):
        M = 10 ** lm; rM = math.sqrt(Gpc * M / a0)
        if kind == "B":
            key = None
        else:
            N = N_decl(lm); key = float(NGRID[np.argmin(abs(NGRID - N))])
        for b in range(4):
            x = Rphys[b] * 1e6 / rM
            T[gi, b] = M / rM ** 2 * shape_ds(x, None if key is None else edge_of(key)) * gscale
    return T


def fit_tab(T, y, idx, start=ZK, Cm=None):
    L = [int(np.argmin(abs(GRID - v))) for v in start]
    def c2(Li):
        m = np.array([T[Li[b], b] for b in range(4)]); return chi2_vec(y, m, idx, Cm)
    for _ in range(3):
        for b in range(4):
            best = min(range(len(GRID)), key=lambda g: c2(L[:b] + [g] + L[b + 1:]))
            L[b] = best
    return [float(GRID[g]) for g in L], c2(L), np.array([T[L[b], b] for b in range(4)])


P(f"F2_outer_lensing{'  [MUTATE: B21 data x 1.10]' if MUT else ''}   criteria e9816b47d2   kappa = 1/2 FITTED; footings never pooled")
P("")
REF902 = {}
for foot in FOOTS:
    j = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG902_cfg804_units_rerun",
                                    f"cfg902_results_declared{'_alt' if foot == 'alt' else ''}.json")))
    REF902[foot] = dict(B_all=j["all"]["chi2_B"], d_all=j["all"]["dchi2"], d_prim=j["primary"]["dchi2"])
K0 = {}
TAB = {}
for foot in FOOTS:
    TB = build_table(foot, "B", R); TD = build_table(foot, "D", R)
    TAB[foot] = (TB, TD)
    out = {}
    for lab, idx in (("primary", IDX_PRIM), ("all", IDX_ALL)):
        LB, cB, mB = fit_tab(TB, Y, idx); LD, cD, mD = fit_tab(TD, Y, idx)
        out[lab] = dict(chi2_B=cB, chi2_D=cD, dchi2=cD - cB, logMb_B=LB, logMb_D=LD)
    K0[foot] = out
    ref = REF902[foot]
    dev = max(abs(out["all"]["chi2_B"] - ref["B_all"]), abs(out["all"]["dchi2"] - ref["d_all"]), abs(out["primary"]["dchi2"] - ref["d_prim"]))
    P(f"  [{foot}] B chi2(all) {out['all']['chi2_B']:.2f} (record {ref['B_all']:.2f}); D_der - B all {out['all']['dchi2']:+.2f} "
      f"(record {ref['d_all']:+.2f}); primary {out['primary']['dchi2']:+.2f} (record {ref['d_prim']:+.2f}); logMb_B {out['all']['logMb_B']}")
    check(f"K0_{foot}", dev <= 0.05, f"{dev:.3f}", "<=0.05")
RES["K0"] = K0
if not all(CHK[f"K0_{f}"] for f in FOOTS):
    P("K0 FAILED: the record is not reproduced; the lane stops here (criteria Sec. 1).")
    RES["checks"] = CHK
    json.dump(RES, open(os.path.join(HERE, f"f2_outer_lensing_results{SFX}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"f2_outer_lensing{SFX}.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(1)
P(f"  [{time.time() - T0:.0f} s]")

# ============================================================================ 3. AQUAL solver checks (K1, K2, K3) and EFE tables
YE = {}
for foot in FOOTS:
    YE[foot] = {"zero": 0.0, "noclu": 10 ** -3.215 * 1.2e-10 / A0[foot], "maxclu": 10 ** -2.30 * 1.2e-10 / A0[foot]}
RES["y_e"] = YE
SOL = {}
for foot in FOOTS:
    for k in ("noclu", "maxclu"):
        SOL[(foot, k)] = AQ.solve_efe(YE[foot][k])
        s = SOL[(foot, k)]
        P(f"  AQUAL EFE solve [{foot} {k}] y_e {s['y_e']:.3e} -> x_e {s['x_e']:.4f}; iters {s['iters']}, last change {s['resid']:.1e}; "
          f"M_eff(inf)/M_b {s['M_far']:.2f}; r_e = r_M/x_e = {1 / s['x_e']:.0f} r_M")
s1 = AQ.solve_efe(1e-6)
sg = np.array([0.1, 0.3, 1, 3, 10])
k1a = float(np.max(np.abs(np.interp(np.log(sg), np.log(s1["r"]), s1["M"]) / AQ.M_iso(sg) - 1)))
k1b = 0.0
for key, s in SOL.items():
    far = s["r"] >= 10 / s["x_e"]
    k1b = max(k1b, float(np.max(np.abs(s["M"][far] / s["M_far"] - 1))))
check("K1_isolated_limit", k1a <= 1e-3, f"{k1a:.1e}", "<=1e-3")
check("K1_far_field", k1b <= 0.02, f"{k1b:.1e}", "<=0.02")
# K2: the record's independent E2 solver (read-only import), canonical noclu
try:
    sys.path.insert(0, os.path.join(REPO, "doors_push_2026_10_22", "E2_field_equation"))
    import aqual_axi as RA
    yq = YE["canonical"]["noclu"]
    E2 = RA.AxiSolver(RA.law_canonical(), yq, Nr_per_dec=40, Nt=64, r_in=1e-3, r_out=3e3)
    iso_chk = abs(float(RA.law_canonical().nu(np.array([1e-4]))[0]) / float(AQ.nu_simple(1e-4)) - 1)
    E2.solve(tol=1e-10, maxit=400)
    Pm = E2.psi.reshape(E2.Nr, E2.Nt)
    wq = np.cos(E2.th - 0.5 * E2.dth) - np.cos(E2.th + 0.5 * E2.dth)
    dpr = (Pm[1:] - Pm[:-1]) / (E2.r[1:] - E2.r[:-1])[:, None]
    Me2 = 1.0 + E2.rf ** 2 * np.einsum("ij,j->i", dpr, wq) / 2.0
    mine = SOL[("canonical", "noclu")]
    sgr = np.logspace(0, 2, 9)
    k2 = float(np.max(np.abs(np.interp(np.log(sgr), np.log(mine["r"]), mine["M"]) / np.interp(np.log(sgr), np.log(E2.rf), Me2) - 1)))
    check("K2_vs_E2_solver", k2 <= 0.02 and iso_chk < 1e-6, f"{k2:.1e} (E2 law = mu x/(1+x): nu ratio-1 {iso_chk:.0e})", "<=0.02")
    RES["K2"] = dict(maxdev=k2, E2_iters=int(E2.iters))
except Exception as e:  # criteria: reported N/A, not PASS
    P(f"K2_vs_E2_solver N/A ({type(e).__name__}: {e})"); RES["K2"] = "N/A"
# K3: projection vs analytic (point mass; singular isothermal sphere)
Rt = np.array([0.03, 0.3, 3.0])
rg = np.logspace(-6, 6, 6001)
pm = AQ.delta_sigma(Rt, rg, np.ones_like(rg), "const") * math.pi * Rt ** 2
sis = AQ.delta_sigma(Rt, rg, rg.copy(), "linear") * 4 * Rt
k3 = float(max(np.max(np.abs(pm - 1)), np.max(np.abs(sis - 1))))
check("K3_projection", k3 <= 1e-3, f"{k3:.1e}", "<=1e-3")
P(f"  [{time.time() - T0:.0f} s]")

# ============================================================================ 4. lens inventory (record's lens catalogue) and native background
LN = np.load(os.path.join(DATA, "lr_lenses.npz"))
PL = np.load(os.path.join(DATA, "cfg110_perlens.npz"))
WG_L, WW_L = PL["WG"], PL["WW"]
GB_EDGES = PL["gbar_edges"]
WLENS = WW_L.sum(axis=1)                                   # each lens's total Sigma_crit^-2-weighted source weight
logMs70 = LN["logM"]; zl = LN["z"]
BIN_EDGES = [8.5, 10.3, 10.6, 10.8, 11.0001]
LBIN = np.digitize(logMs70, BIN_EDGES) - 1                 # 0..3 ; outside -> -1 / 4
H_NAT = {"mid": 0.679, "lo": 0.672, "hi": 0.686}
OM_NAT = 0.3085
T_OM_A, T_OM_B = 1.0128, 1.0037                          # CFG885 committed JSON (B21 fid 0.2793 / record fid 0.3)
_j885 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG885_kids_rar_native_distances", "cfg885_results.json")))
t885a = _j885["fiducial_envelope"]["0.2793"]["T_window"]["Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt"]
t885b = _j885["fiducial_envelope"]["0.3"]["T_window"]["Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt"]
assert abs(t885a - T_OM_A) < 5e-4 and abs(t885b - T_OM_B) < 5e-4, (t885a, t885b)


def chi_flat(z, om):
    zz = np.linspace(0, 1.0, 4001); E = np.sqrt(om * (1 + zz) ** 3 + 1 - om)
    ch = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))])
    return np.interp(z, zz, ch)


qDA_lens = chi_flat(zl, OM_NAT) / chi_flat(zl, 0.3)       # Omega_m-only D_A ratio (LePhare masses, fid 0.3)
INV = {}
for b in range(4):
    m = LBIN == b
    w = WLENS[m]
    INV[b] = dict(n=int(m.sum()), w=w, logMs70=logMs70[m], z=zl[m], qDA=qDA_lens[m],
                  zeff=float(np.sum(w * zl[m]) / np.sum(w)), meanlogMs=float(np.sum(w * logMs70[m]) / np.sum(w)))
    P(f"  bin {b + 1}: {INV[b]['n']:,} lenses; weighted <log M*> {INV[b]['meanlogMs']:.3f} (h70, LePhare+0.15); z_eff {INV[b]['zeff']:.3f}")
RES["inventory"] = {f"bin{b + 1}": dict(n=INV[b]["n"], meanlogMs70=INV[b]["meanlogMs"], zeff=INV[b]["zeff"]) for b in range(4)}


def data_native(h, Ydata=Y, Tom=T_OM_A, extra=1.0):
    """B21 data in native units: R (Mpc), Y (Msun/pc^2), covariance."""
    Rn = np.array([R[b] * (0.70 / h) * float(chi_flat(INV[b]["zeff"], OM_NAT) / chi_flat(INV[b]["zeff"], 0.2793)) for b in range(4)])
    f = (h / 0.70) * Tom * extra
    return Rn, Ydata * f, f


LMG = np.round(np.arange(6.8, 11.81, 0.02), 2)              # log M* grid (native) for the tables
RGRID_PC = np.logspace(1.0, 10.0, 3601)                     # pc


def meff_profile(foot, logMs, f_hot, dcold_dex, ye_key, logMcold=None):
    """lensing mass M_eff(<r) on RGRID_PC for one lens (native Msun)."""
    a0 = a0u(foot); Ms = 10 ** logMs
    Mcold = (10 ** logMcold) if logMcold is not None else Ms * 10 ** (-0.69 * logMs + 6.63 + dcold_dex)
    Mpt = Ms + Mcold; Mhot = f_hot * Ms
    Mb = Mpt + Mhot * np.minimum(1.0, (RGRID_PC / 1e5) ** 3)
    Miso = Mb * AQ.nu_simple(Gpc * Mb / RGRID_PC ** 2 / a0)
    if ye_key == "zero":
        return Miso, "linear"
    s = SOL[(foot, ye_key)]
    rM = math.sqrt(Gpc * (Mpt + Mhot) / a0)
    sg = RGRID_PC / rM
    Me = np.interp(np.log(sg), np.log(s["r"]), s["M"], left=np.nan, right=s["M_far"])
    Cr = np.where(np.isnan(Me), 1.0, Me / AQ.M_iso(sg))
    return Miso * Cr, "const"


def stack_model(foot, Rn, cfg):
    """lens-weighted stacked Delta Sigma_T at native radii Rn[b] (Mpc), for configuration cfg."""
    h = cfg["h"]; out = np.empty((4, 15))
    for b in range(4):
        # native M* per lens: (0.70/h)^2 and the Omega_m D_A ratio; SPS shift dMs applied to stars only
        lMs_nat = INV[b]["logMs70"] + 2 * np.log10(0.70 / h) + 2 * np.log10(INV[b]["qDA"])
        # table over the native M* grid, holding the cold-gas fraction law in the catalogue M*
        tab = np.empty((len(LMG), 15))
        for gi, lm in enumerate(LMG):
            lm70 = lm - 2 * np.log10(0.70 / h)
            lmc = lm + (-0.69 * lm70 + 6.63) + cfg["dcold"]
            M, tail = meff_profile(foot, lm + cfg["dMs"], cfg["fhot"] * 10 ** (-cfg["dMs"]), 0.0, cfg["ye"], logMcold=lmc)
            tab[gi] = AQ.delta_sigma(Rn[b] * 1e6, RGRID_PC, M, tail)
        w = INV[b]["w"]
        vals = np.array([np.interp(lMs_nat, LMG, tab[:, i]) for i in range(15)])     # (15, nlens)
        out[b] = vals @ w / w.sum()
    return out
P(f"  [{time.time() - T0:.0f} s]")

# ============================================================================ 5. Track A ladder (B21 Fig. 3, released covariance)
def amps(y, m, Cm):
    o = {}
    for lab, idx in (("in", IDX_IN), ("O1", IDX_O1), ("O2", IDX_O2), ("out", IDX_OUT)):
        a, s = gls_amp(y, m, idx, Cm); o[f"A_{lab}"] = a; o[f"sA_{lab}"] = s
    o["chi2_all"] = chi2_vec(y, m, IDX_ALL, Cm); o["chi2_out"] = chi2_vec(y, m, IDX_OUT, Cm)
    o["chi2_in"] = chi2_vec(y, m, IDX_IN, Cm)
    return o


def row(lab, o, chiB):
    o["dchi2_vs_B"] = o["chi2_all"] - chiB
    P(f"    {lab:34s} chi2_all {o['chi2_all']:7.1f}  dchi2 {o['dchi2_vs_B']:+7.1f}  chi2_out(28) {o['chi2_out']:6.1f}  "
      f"A_in {o['A_in']:.3f}+-{o['sA_in']:.3f}  A_O1 {o['A_O1']:.3f}+-{o['sA_O1']:.3f}  A_O2 {o['A_O2']:.3f}+-{o['sA_O2']:.3f}  "
      f"A_out {o['A_out']:.3f}+-{o['sA_out']:.3f}")
    return o


CENTRAL = dict(h=H_NAT["mid"], dMs=0.0, dcold=0.0, fhot=0.5, ye="noclu", pz=1.0)
LADDER_A = {}
for foot in FOOTS:
    P(f"\n  Track A ladder [{foot}]  (dchi2 = chi2(model) - chi2(B refit on the same data version), B = law, no EFE, M_b profiled)")
    L = {}
    TB, TD = TAB[foot]
    LB, cB, mB = fit_tab(TB, Y, IDX_ALL); LD, cD, mD = fit_tab(TD, Y, IDX_ALL)
    L["L0_record_Dder"] = row("L0 record D_der (CFG902)", amps(Y, mD, C), cB)
    L["L1_no_edge_B"] = row("L1 no catchment edge (= B, profiled)", amps(Y, mB, C), cB)
    L["L1_no_edge_B"]["logMb"] = LB
    # native background, masses still profiled
    Rn, Yn, f = data_native(H_NAT["mid"]); Cn = C * f * f
    TBn = build_table(foot, "B", Rn)
    LBn, cBn, mBn = fit_tab(TBn, Yn, IDX_ALL, Cm=Cn)
    L["L2_native_B"] = row("L2 native h 0.679, Om 0.3085 (B)", amps(Yn, mBn, Cn), cBn)
    L["L2_native_B"]["logMb"] = LBn
    cfgs = [("L3_inventory_star_cold", dict(CENTRAL, fhot=0.0, ye="zero")),
            ("L4_plus_hotCGM", dict(CENTRAL, ye="zero")),
            ("L5_plus_EFE_noclu=T_central", dict(CENTRAL))]
    MODELS = {}
    for lab, cfg in cfgs:
        m = stack_model(foot, Rn, cfg); MODELS[lab] = m
        L[lab] = row(lab, amps(Yn, m, Cn), cBn)
    P(f"    -- one at a time from T_central --")
    OAT = [("EFE y_e = 0", dict(CENTRAL, ye="zero")), ("EFE y_e = maxclu", dict(CENTRAL, ye="maxclu")),
           ("f_hot = 0", dict(CENTRAL, fhot=0.0)), ("f_hot = 1.0", dict(CENTRAL, fhot=1.0)),
           ("f_cold -0.2 dex", dict(CENTRAL, dcold=-0.2)), ("f_cold +0.2 dex", dict(CENTRAL, dcold=0.2)),
           ("M* -0.2 dex (E1)", dict(CENTRAL, dMs=-0.2)), ("M* +0.2 dex", dict(CENTRAL, dMs=0.2)),
           ("h 0.672", dict(CENTRAL, h=H_NAT["lo"])), ("h 0.686", dict(CENTRAL, h=H_NAT["hi"])),
           ("photo-z Sigma_crit -3%", dict(CENTRAL, pz=0.97)), ("photo-z Sigma_crit +3%", dict(CENTRAL, pz=1.03))]
    for lab, cfg in OAT:
        Rn2, Yn2, f2 = data_native(cfg["h"], extra=cfg["pz"]); Cn2 = C * f2 * f2
        if cfg["h"] != H_NAT["mid"] or cfg["pz"] != 1.0:
            LB2, cB2, _ = fit_tab(build_table(foot, "B", Rn2), Yn2, IDX_ALL, Cm=Cn2)
        else:
            cB2 = cBn
        m = stack_model(foot, Rn2, cfg)
        L["OAT " + lab] = row("  " + lab, amps(Yn2, m, Cn2), cB2)
    # upper envelope for the outer signal (most generous to the theory): y_e 0, f_hot 1, M* +0.2, cold +0.2
    env = dict(CENTRAL, ye="zero", fhot=1.0, dMs=0.2, dcold=0.2)
    L["ENVELOPE_max_outer"] = row("ENVELOPE y_e 0,f_hot 1,M* +.2,cold +.2", amps(Yn, stack_model(foot, Rn, env), Cn), cBn)
    LADDER_A[foot] = L
    P(f"  [{time.time() - T0:.0f} s]")
RES["trackA"] = LADDER_A

# ============================================================================ 6. Track B: record per-lens re-measurement, isolation samples
from astropy.io import fits
from scipy.spatial import cKDTree
ISO = np.load(os.path.join(DATA, "cfg96_isoflags.npz"))
STK = np.load(os.path.join(DATA, "cfg96_stack.npz"))
PATCH = STK["patch"]; TYP = LN["typ"]; NPATCH = 50
# K4a: per-patch, per-class sums of the per-lens arrays reproduce the record's W10 stack
wg_pc = np.zeros((NPATCH, 2, 15)); ww_pc = np.zeros((NPATCH, 2, 15))
np.add.at(wg_pc, (PATCH, TYP), WG_L); np.add.at(ww_pc, (PATCH, TYP), WW_L)
k4a = float(max(np.max(np.abs(wg_pc - STK["wgE_10"])) / np.max(np.abs(STK["wgE_10"])),
                np.max(np.abs(ww_pc - STK["W_10"])) / np.max(np.abs(STK["W_10"]))))
check("K4a_perlens_vs_record_stack", k4a <= 1e-10, f"{k4a:.1e}", "<=1e-10")
# S_strict: no neighbour at least as massive within projected 1 Mpc (physical, h70) and |dchi| < 100 Mpc, inside S30
bh = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample.fits"), memmap=True)[1].data
lh = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True)[1].data
r_mag = np.array(bh["MAG_AUTO_CALIB"], "f8"); zph = np.array(bh["zphot_ANNz2"], "f8"); msk = np.array(bh["masked"])
lMp = np.array(lh["MASS_MED"], "f8") + 0.15
pool = (r_mag < 20) & (zph > 0.1) & (zph < 0.5) & (msk == 0) & np.isfinite(lMp) & (lMp > 7)
raP = np.array(bh["RAJ2000"], "f8")[pool]; deP = np.array(bh["DECJ2000"], "f8")[pool]; zP = zph[pool]; lMP = lMp[pool]
del bh, lh, r_mag, zph, msk, lMp


def chi_h70(z):  # record convention: flat, Om 0.3, H0 70 (comoving Mpc)
    return chi_flat(z, 0.3) * 2.998e5 / 70.0


chiP = chi_h70(zP)
def uvec(ra, de):
    a, d = np.radians(ra), np.radians(de)
    return np.c_[np.cos(d) * np.cos(a), np.cos(d) * np.sin(a), np.sin(d)]
treeP = cKDTree(uvec(raP, deP))
UL = uvec(LN["ra"], LN["dec"])
dself, iself = treeP.query(UL)
k4c = float(np.max(dself)) < 1e-9 and np.allclose(lMP[iself], logMs70, atol=1e-9)
theta = 1.0 * (1 + zl) / LN["chi"]                       # 1 Mpc physical at the lens
host = np.zeros(len(zl), bool)
CH = 20000
for i0 in range(0, len(zl), CH):
    lists = treeP.query_ball_point(UL[i0:i0 + CH], r=theta[i0:i0 + CH])
    for k, js in enumerate(lists):
        i = i0 + k
        if len(js) < 2: continue
        js = np.array(js); js = js[js != iself[i]]
        if js.size and np.any((lMP[js] >= logMs70[i]) & (np.abs(chiP[js] - LN["chi"][i]) < 100.0)):
            host[i] = True
SAMP = {"S10": np.ones(len(zl), bool), "S20": ISO["f20"], "S30": ISO["f30"]}
SAMP["S_strict"] = SAMP["S30"] & ~host
k5 = bool(np.all(SAMP["S_strict"] <= SAMP["S30"]) and np.all(SAMP["S30"] <= SAMP["S20"]) and np.all(SAMP["S20"] <= SAMP["S10"]))
check("K5_nested_samples", k5 and k4c, f"self-match {k4c}; n " + "/".join(str(int(v.sum())) for v in SAMP.values()), "nested")
RES["trackB_samples"] = {k: int(v.sum()) for k, v in SAMP.items()}
RES["trackB_host_vetoed_in_S10"] = int(host.sum())
P(f"  Track B samples: " + ", ".join(f"{k} {int(v.sum()):,}" for k, v in SAMP.items()) + f"   (host-veto flags {int(host.sum()):,} of all)")

# ---- geometry per lens and g_bar bin
SIGU = (3.0857e16) ** 2 / 1.989e30                       # kg/m^2 -> Msun/pc^2
ONEK = 0.9853                                            # B21 (1 + K)
GBC = np.sqrt(GB_EDGES[1:] * GB_EDGES[:-1])
R70 = np.sqrt(6.674e-11 * LN["Mgal"][:, None] * 1.989e30 / GBC[None, :]) / 3.0857e22   # (nlens, 15) h70 Mpc
qB = chi_flat(zl, OM_NAT) / chi_flat(zl, 0.3)
LRT = np.linspace(np.log(0.005), np.log(8.0), 121)        # native Mpc grid for tables


def table_RM(foot, cfg):
    """Delta Sigma_T on (LMG native M*, LRT) for configuration cfg (native units)."""
    h = cfg["h"]; tab = np.empty((len(LMG), len(LRT)))
    for gi, lm in enumerate(LMG):
        lm70 = lm - 2 * np.log10(0.70 / h)
        lmc = lm + (-0.69 * lm70 + 6.63) + cfg["dcold"]
        M, tail = meff_profile(foot, lm + cfg["dMs"], cfg["fhot"] * 10 ** (-cfg["dMs"]), 0.0, cfg["ye"], logMcold=lmc)
        tab[gi] = AQ.delta_sigma(np.exp(LRT) * 1e6, RGRID_PC, M, tail)
    return tab


def perlens_model(tab, cfg):
    """model Delta Sigma (native) per lens and g_bar bin, bilinear in (log M*, ln R)."""
    h = cfg["h"]
    lMn = logMs70 + 2 * np.log10(0.70 / h) + 2 * np.log10(qB)
    Rn = R70 * (0.70 / h) * qB[:, None]
    gx = np.clip((lMn - LMG[0]) / (LMG[1] - LMG[0]), 0, len(LMG) - 1.001)
    gy = np.clip((np.log(Rn) - LRT[0]) / (LRT[1] - LRT[0]), 0, len(LRT) - 1.001)
    i0 = gx.astype(int); fx = gx - i0
    j0 = gy.astype(int); fy = gy - j0
    I0 = i0[:, None]
    v = ((1 - fx)[:, None] * ((1 - fy) * tab[I0, j0] + fy * tab[I0, j0 + 1])
         + fx[:, None] * ((1 - fy) * tab[I0 + 1, j0] + fy * tab[I0 + 1, j0 + 1]))
    return v


RMED = np.zeros((4, 15))
for b in range(4):
    m = LBIN == b
    for k in range(15):
        ww = WW_L[m, k]
        if ww.sum() > 0:
            o = np.argsort(R70[m, k]); cw = np.cumsum(ww[o]); RMED[b, k] = R70[m, k][o][np.searchsorted(cw, 0.5 * cw[-1])]
RANGE = {"O1": (RMED > 0.4) & (RMED < 1.1), "O2": (RMED > 1.1) & (RMED <= 3.0), "in": (RMED <= 0.31) & (RMED > 0.03)}
RANGE["out"] = RANGE["O1"] | RANGE["O2"]
RES["trackB_Rmed_h70"] = RMED.tolist()


def trackB_stats(foot, cfg, tab=None, samples=("S10", "S20", "S30", "S_strict")):
    tab = table_RM(foot, cfg) if tab is None else tab
    MOD = perlens_model(tab, cfg)                                      # (nlens, 15) native
    fdat = (cfg["h"] / 0.70) * T_OM_B * SIGU / ONEK * cfg.get("pz", 1.0)
    out = {}
    JK = {}
    for sname in samples:
        S = SAMP[sname]
        # patch sums per mass bin: WG, WW, WW*model
        sg = np.zeros((NPATCH, 4, 15)); sw = np.zeros((NPATCH, 4, 15)); sm = np.zeros((NPATCH, 4, 15))
        ok = S & (LBIN >= 0) & (LBIN < 4)
        np.add.at(sg, (PATCH[ok], LBIN[ok]), WG_L[ok]); np.add.at(sw, (PATCH[ok], LBIN[ok]), WW_L[ok])
        np.add.at(sm, (PATCH[ok], LBIN[ok]), WW_L[ok] * MOD[ok])
        tg, tw, tm = sg.sum(0), sw.sum(0), sm.sum(0)
        with np.errstate(all="ignore"):
            d = tg / tw * fdat; mm = tm / tw
            dj = (tg[None] - sg) / (tw[None] - sw) * fdat; mj = (tm[None] - sm) / (tw[None] - sw)
        var = (NPATCH - 1) / NPATCH * np.sum((dj - dj.mean(0)) ** 2, axis=0)
        res = {}
        for lab, msk_ in RANGE.items():
            sel = msk_ & np.isfinite(d) & (var > 0)
            wgt = np.where(sel, mm / var, 0.0)
            A = float(np.sum(wgt * d) / np.sum(wgt * mm))
            Aj = np.sum(wgt[None] * dj, axis=(1, 2)) / np.sum(wgt[None] * mj, axis=(1, 2))
            sA = float(math.sqrt((NPATCH - 1) / NPATCH * np.sum((Aj - Aj.mean()) ** 2)))
            res[f"A_{lab}"] = A; res[f"sA_{lab}"] = sA; JK[(sname, lab)] = Aj
            chi = float(np.sum(np.where(sel, (d - mm) ** 2 / var, 0.0))); res[f"chi2diag_{lab}"] = chi; res[f"n_{lab}"] = int(sel.sum())
        out[sname] = res
        out[sname + "_profile"] = dict(d=d.tolist(), m=mm.tolist(), sig=np.sqrt(var).tolist())
    # paired jackknife differences S10 - S_strict
    for lab in ("O1", "O2", "out"):
        if ("S10", lab) in JK and ("S_strict", lab) in JK:
            dd = out["S10"][f"A_{lab}"] - out["S_strict"][f"A_{lab}"]
            dj = JK[("S10", lab)] - JK[("S_strict", lab)]
            out[f"diff_{lab}"] = dict(d=dd, s=float(math.sqrt((NPATCH - 1) / NPATCH * np.sum((dj - dj.mean()) ** 2))))
    return out, MOD


# K4b: base stack (h70) vs B21 Fig. 9 (B21 isolated, same g_bar bins)
ratios = []
for b in range(4):
    f9 = np.loadtxt(os.path.join(B21, f"Fig-9_RAR-KiDS-isolated_Massbin-{b + 1}.txt"))
    m = LBIN == b
    d = WG_L[m].sum(0) / WW_L[m].sum(0) * SIGU / ONEK
    y9 = f9[:, 1] / f9[:, 4]; e9 = f9[:, 3] / f9[:, 4]
    good = (y9 / e9 > 3) & np.isfinite(d)
    ratios += list(d[good] / y9[good])
k4b = float(np.median(ratios))
check("K4b_stack_vs_B21_Fig9_median_ratio", 0.8 <= k4b <= 1.25, f"{k4b:.3f} (n={len(ratios)})", "[0.8,1.25]")
RES["K4b_median_ratio"] = k4b
P(f"  [{time.time() - T0:.0f} s]")

TRACKB = {}
for foot in FOOTS:
    TRACKB[foot] = {}
    for yk in ("zero", "noclu", "maxclu"):
        cfg = dict(CENTRAL, ye=yk)
        o, _ = trackB_stats(foot, cfg)
        TRACKB[foot][yk] = o
        P(f"\n  Track B [{foot}, T_central with y_e {yk}]  (A = data / T, inverse-variance weights, patch jackknife)")
        for sname in ("S10", "S20", "S30", "S_strict"):
            r_ = o[sname]
            P(f"    {sname:8s} A_in {r_['A_in']:.3f}+-{r_['sA_in']:.3f}  A_O1 {r_['A_O1']:.3f}+-{r_['sA_O1']:.3f} (n {r_['n_O1']})  "
              f"A_O2 {r_['A_O2']:.3f}+-{r_['sA_O2']:.3f} (n {r_['n_O2']})  A_out {r_['A_out']:.3f}+-{r_['sA_out']:.3f}")
        for lab in ("O1", "O2", "out"):
            P(f"    S10 - S_strict {lab}: {o['diff_' + lab]['d']:+.3f} +- {o['diff_' + lab]['s']:.3f}")
    P(f"  [{time.time() - T0:.0f} s]")
RES["trackB"] = {f: {y: {k: v for k, v in o.items()} for y, o in d.items()} for f, d in TRACKB.items()}

# ============================================================================ 7. frozen verdict rule (criteria Sec. 5)
def cls_amp(A, s):
    if A - 1 > 3 * s: return "short"
    if 1 - A > 3 * s: return "over"
    if abs(A - 1) <= 2 * s: return "consistent"
    return "between"


VERD = {}
for foot in FOOTS:
    VERD[foot] = {}
    for yk, lab in (("zero", "OAT EFE y_e = 0"), ("noclu", "L5_plus_EFE_noclu=T_central"), ("maxclu", "OAT EFE y_e = maxclu")):
        a = LADDER_A[foot][lab]; b = TRACKB[foot][yk]
        st = b["S_strict"]
        cA = (cls_amp(a["A_O1"], a["sA_O1"]), cls_amp(a["A_O2"], a["sA_O2"]))
        cS = (cls_amp(st["A_O1"], st["sA_O1"]), cls_amp(st["A_O2"], st["sA_O2"]))
        dz = b["diff_out"]["d"] / b["diff_out"]["s"]
        if cA == ("consistent", "consistent"):
            v = "EXPLAINED (no catchment edge)"
        elif dz > 3 and cS == ("consistent", "consistent"):
            v = "EXPLAINED (contamination of the isolated sample)"
        elif any(x in ("short", "over") for x in cS):
            v = "REAL FAILURE"
        else:
            v = "UNDECIDABLE"
        VERD[foot][yk] = dict(verdict=v, trackA=cA, strict=cS, diff_out_sigma=dz)
        P(f"  VERDICT [{foot}, y_e {yk}]: {v}   Track A (O1, O2) {cA}; S_strict (O1, O2) {cS}; S10 - S_strict outer {dz:.1f} sigma")
    vs = {v["verdict"] for v in VERD[foot].values()}
    VERD[foot]["lane"] = VERD[foot]["noclu"]["verdict"] if len(vs) == 1 else "UNDECIDABLE (g_ext-limited)"
    P(f"  LANE VERDICT [{foot}]: {VERD[foot]['lane']}")
LANE = VERD["canonical"]["lane"] if VERD["canonical"]["lane"] == VERD["alt"]["lane"] else "UNDECIDABLE (footing split)"
P(f"  LANE VERDICT (both footings): {LANE}")
RES["verdict"] = VERD; RES["lane_verdict"] = LANE

# ============================================================================ 8. post-hoc diagnostics (REPORTED ONLY; not in any verdict line)
P("\n  POST-HOC DIAGNOSTICS (reported only)")
PH = {}
# (a) wider host-veto window: |dchi| < 300 Mpc (same-z capture ~99% at sigma 115 Mpc, CFG502)
host300 = np.zeros(len(zl), bool)
for i0 in range(0, len(zl), CH):
    lists = treeP.query_ball_point(UL[i0:i0 + CH], r=theta[i0:i0 + CH])
    for k, js in enumerate(lists):
        i = i0 + k
        if len(js) < 2: continue
        js = np.array(js); js = js[js != iself[i]]
        if js.size and np.any((lMP[js] >= logMs70[i]) & (np.abs(chiP[js] - LN["chi"][i]) < 300.0)):
            host300[i] = True
SAMP["S_x300"] = SAMP["S30"] & ~host300
P(f"   (a) S_x300 = S30 & no >= M_lens neighbour within 1 Mpc, |dchi| < 300: {int(SAMP['S_x300'].sum()):,} lenses")
PH["S_x300_n"] = int(SAMP["S_x300"].sum())
for foot in FOOTS:
    for yk in ("zero", "noclu"):
        o, _ = trackB_stats(foot, dict(CENTRAL, ye=yk), samples=("S_x300",))
        r_ = o["S_x300"]
        P(f"       [{foot}, y_e {yk}] S_x300 A_O1 {r_['A_O1']:.3f}+-{r_['sA_O1']:.3f}  A_O2 {r_['A_O2']:.3f}+-{r_['sA_O2']:.3f}  A_in {r_['A_in']:.3f}+-{r_['sA_in']:.3f}")
        PH[f"S_x300_{foot}_{yk}"] = {k: v for k, v in r_.items()}
# absolute strict-sample outer profile (canonical, native units) vs T(y_e = 0) and T(noclu)
for yk in ("zero", "noclu"):
    pr = TRACKB["canonical"][yk]["S_strict_profile"]
    d_, m_, s_ = np.array(pr["d"]), np.array(pr["m"]), np.array(pr["sig"])
    sel = RANGE["O2"]
    P(f"   S_strict O2 points (canonical, Msun/pc^2): data {np.round(d_[sel], 3).tolist()}")
    P(f"       +- {np.round(s_[sel], 3).tolist()}; T(y_e {yk}) {np.round(m_[sel], 3).tolist()}")
# (b) external-field scan on Track A (largest y_e with Track A O1 and O2 within 3 sigma)
for foot in FOOTS:
    Rn, Yn, f = data_native(H_NAT["mid"]); Cn = C * f * f
    scan = {}
    for ye in (1e-6, 1e-5, 3e-5, 1e-4, 3e-4):
        SOL[(foot, f"scan{ye:g}")] = AQ.solve_efe(ye, maxit=200)
        m = stack_model(foot, Rn, dict(CENTRAL, ye=f"scan{ye:g}"))
        o = amps(Yn, m, Cn); scan[f"{ye:g}"] = o
        P(f"   (b) [{foot}] y_e {ye:7.0e} (x_e {SOL[(foot, f'scan{ye:g}')]['x_e']:.4f}): A_O1 {o['A_O1']:.3f}+-{o['sA_O1']:.3f}  "
          f"A_O2 {o['A_O2']:.3f}+-{o['sA_O2']:.3f}  chi2_all {o['chi2_all']:.1f}")
    PH[f"ye_scan_{foot}"] = scan
# (c) bound: T_central (noclu) + CFG903's catalogue two-halo term (catchment-supplied neighbours, heavier per galaxy than
#     the noclu AQUAL halo: 1 + 5.364 N >= 33 M_b against M_eff(inf) <= 31.4 M_b), Track A
j903 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG903_framework_two_halo_kids", "cfg903_results.json")))
for foot in FOOTS:
    Rn, Yn, f = data_native(H_NAT["mid"]); Cn = C * f * f
    T2 = np.array(j903["footings"][foot]["T2h_primary"]) * f            # h70 -> native, same factor as the data
    m = stack_model(foot, Rn, CENTRAL) + T2
    o = amps(Yn, m, Cn)
    P(f"   (c) [{foot}] T_central + CFG903 two-halo (upper-bound proxy): A_O1 {o['A_O1']:.3f}+-{o['sA_O1']:.3f}  A_O2 {o['A_O2']:.3f}+-{o['sA_O2']:.3f}  chi2_all {o['chi2_all']:.1f}")
    PH[f"T_plus_cfg903_{foot}"] = o
    m0 = stack_model(foot, Rn, dict(CENTRAL, ye="zero")) + T2
    o0 = amps(Yn, m0, Cn)
    P(f"       [{foot}] T(y_e 0) + CFG903 two-halo: A_O1 {o0['A_O1']:.3f}+-{o0['sA_O1']:.3f}  A_O2 {o0['A_O2']:.3f}+-{o0['sA_O2']:.3f}")
    PH[f"Tzero_plus_cfg903_{foot}"] = o0
# (d) dust (cold energy) the data would need: extra lensing mass at the O1 midpoint, in units of the theory's own M_eff
for foot in FOOTS:
    a = LADDER_A[foot]["L5_plus_EFE_noclu=T_central"]
    PH[f"required_extra_{foot}"] = dict(inner=a["A_in"] - 1, O1=a["A_O1"] - 1, O2=a["A_O2"] - 1)
    P(f"   (d) [{foot}] required extra lensing mass / T_central: inner {a['A_in'] - 1:+.2f}, O1 {a['A_O1'] - 1:+.2f}, O2 {a['A_O2'] - 1:+.2f}")
# (e) B21's own samples in g_bar bins (mass-independent for the isolated law): spectroscopic GAMA isolation vs photo-z
#     KiDS isolation, and KiDS "all" vs "isolated", over the outer bins g_bar < 3e-14 m/s^2
def _ld(fn):
    a = np.loadtxt(os.path.join(B21, fn)); return a[:, 0], a[:, 1] / a[:, 4], a[:, 3] / a[:, 4]
gk, yk_, ek = _ld("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt"); gg, yg, eg = _ld("Fig-4-C1_RAR-GAMA-isolated_Nobins.txt")
lo = gk < 3e-14
w_ = 1 / (eg[lo] ** 2 + (yg[lo] / yk_[lo] * ek[lo]) ** 2 / 1.0)
rat = yg[lo] / yk_[lo]; er = np.sqrt(eg[lo] ** 2 / yk_[lo] ** 2 + (yg[lo] * ek[lo] / yk_[lo] ** 2) ** 2)
rG = float(np.sum(rat / er ** 2) / np.sum(1 / er ** 2)); sG = float(1 / math.sqrt(np.sum(1 / er ** 2)))
P(f"   (e) B21 GAMA (spec-z isolated) / KiDS (photo-z isolated), g_bar < 3e-14, 6 bins: {rG:.2f} +- {sG:.2f}")
ra_, sa_ = [], []
for b in range(1, 5):
    _, y9, e9 = _ld(f"Fig-9_RAR-KiDS-isolated_Massbin-{b}.txt"); ga, ya, ea = _ld(f"Fig-A4_RAR-KiDS-all_Massbin-{b}.txt")
    l2 = ga < 3e-14
    ra_ += list(ya[l2] / y9[l2]); sa_ += list(np.sqrt((ea[l2] / y9[l2]) ** 2 + (ya[l2] * e9[l2] / y9[l2] ** 2) ** 2))
ra_, sa_ = np.array(ra_), np.array(sa_)
rA = float(np.sum(ra_ / sa_ ** 2) / np.sum(1 / sa_ ** 2)); sA_ = float(1 / math.sqrt(np.sum(1 / sa_ ** 2)))
P(f"   (e) B21 KiDS all / isolated (4 mass bins), g_bar < 3e-14: {rA:.2f} +- {sA_:.2f}  (errors treated as independent)")
PH["gama_over_kids_iso_outer"] = [rG, sG]; PH["kids_all_over_iso_outer"] = [rA, sA_]
RES["posthoc"] = PH

# ============================================================================ 9. outputs
ncheck = len(CHK); npass = sum(CHK.values())
P(f"\n  peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB; runtime {time.time() - T0:.0f} s")
P(f"F2_OUTER_LENSING COMPLETE: {npass}/{ncheck} checks PASS.")
RES["checks"] = CHK
json.dump(RES, open(os.path.join(HERE, f"f2_outer_lensing_results{SFX}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"f2_outer_lensing{SFX}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == ncheck else 1)
