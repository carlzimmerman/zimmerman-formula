#!/usr/bin/env python3
"""CFG307 -- stress test of ALESS 122.1's implied a0 (the one class-M galaxy on the a0(z) chart with a root; CFG229 s* = 8.82).
A declared full-factorial grid of record-held input choices (pressure x gas x M* x inclination x radius = 540 cells), CFG229's estimator and random stream
replayed, the frozen decision rule, the same grid on the six class-M siblings, and a common-calibration outlier test.
Descriptive; one galaxy is not a measurement of a0(z).  kappa = 1/2 FITTED.  FLAT a0(z) is the framework's distinctive law, a0 ~ H(z) the rival; LambdaCDM has no a0.
No halo-fit quantity enters a cell.  No sentence of this lane says the data favour a law.  A NO-ROOT cell is a statement about baryons against dynamics.
Frozen criteria: FROZEN_CRITERIA.md (3b1ca88f7), committed before any cell was computed.
POST HOC EDIT after the first run (outputs kept as *_firstrun.*): sibling cells at the bracket LIMIT (s* > 1e3) are now counted as rooted and above both laws, as the
criteria define (the first run counted 30 ALPAKA 18 LIMIT cells as no root); the alt-footing label prints the exact footing ratio.  The ALESS 122.1 grid is unchanged.
Run: python3 campaign_fresh_gravity/CFG307_aless122_stress_test/cfg307_stress.py        MUTATE=1: V x 0.7 in every cell of every galaxy (separate outputs)"""
import os, sys, re, math, json, time, itertools
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from scipy.special import i0e, i1e, k0e, k1e, j1
from scipy.optimize import brentq
from scipy.integrate import quad

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
EXT = os.path.join(os.path.dirname(REPO), "_external_data")             # the external data directory beside the repo (read only)
MODE = os.environ.pop("MUTATE", "").strip()
MUT = MODE == "1"
TAG = "_MUTATE" if MUT else ""
VFAC = 0.7 if MUT else 1.0
sys.path.insert(0, CFG)
import CFG4_common as K
C229 = os.path.join(CFG, "CFG229_class_m_gold")
sys.path.insert(0, C229)
from a0implied import implied, lever                                      # CFG229's copy of CFG223's estimator (read-only import, no bytecode written)

T0 = time.time()
OUT, CHK = [], []
G2SI = 1e6 / 3.0856775814913673e19                                        # (km/s)^2/kpc -> m/s^2 (CFG229)
G_KPC = 4.30091e-6
XN = 1.678
OM = 0.315
HE, LOGHE = 1.36, math.log10(1.36)
SEED, BMC = 229, 10000
NU, NU_P2 = K.nu_mono, K.nu_p2
A0 = K.A0["canonical"]
ALT = K.A0["alt"] / K.A0["canonical"]
LN10 = math.log(10.0)


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + 1 - OM)


def disc_v2(M, Re, Rr):                                                   # CFG229's thin exponential disc (Freeman), R_d = R_e/1.678
    Rd = Re / XN
    y = Rr / (2 * Rd)
    return 2 * G_KPC * M / Rd * y ** 2 * (i0e(y) * k0e(y) - i1e(y) * k1e(y))


def gdisc(M, Re, Rr):
    return disc_v2(M, Re, Rr) / Rr * G2SI


P(__doc__.split("Run:")[0].strip())
P(f"MUTATE = {'1 (V x 0.7 in every cell of every galaxy)' if MUT else 'none'}")

# ===================================================================================== inputs
ST = pd.read_csv(os.path.join(C229, "cfg229_inputs_static.csv"))
KN = pd.read_csv(os.path.join(C229, "cfg229_inputs_kin.csv"))
R229 = json.load(open(os.path.join(C229, "cfg229_score_results.json")))
DU = os.path.join(REPO, "data_assembly", "multitracer_gas", "dunne2022")
AT = os.path.join(REPO, "data_assembly", "arxiv_tables")
SN = os.path.join(REPO, "data_assembly", "highz_literature_tables", "sins_ao")
DM = pd.read_csv(os.path.join(DU, "dunne2022_master.csv")).set_index("Name")
OPT = {k: pd.read_csv(os.path.join(DU, f"dunne2022_opt_{k}.csv")).set_index("Name") for k in ("ad", "dax", "xa", "xd")}
AMB = pd.read_csv(os.path.join(AT, "amvrosiadis_bestfit.csv"), dtype={"alessid": str}).set_index("alessid")
ALK = pd.read_csv(os.path.join(AT, "alpaka1_kinematics.csv")).set_index("id")
ALD = pd.read_csv(os.path.join(AT, "alpaka1_digitised", "alpaka1_vrot_digitised.csv"))
SN6 = pd.read_csv(os.path.join(SN, "sins_ao_table6_kinematics.csv")).set_index("source")
n = len(ST)
gid = ST["gid"].tolist()
z = ST["z"].values.astype(float)
Ms0 = ST["Mstar"].values.astype(float)
Mg0 = 10 ** ST["logMgas_He"].values.astype(float)
Re0, R0 = ST["Re_kpc"].values.astype(float), ST["R_kpc"].values.astype(float)
e_st, e_gas = ST["e_logMstar_inner"].values.astype(float), ST["e_logMH2"].values.astype(float)
i_used, e_i, i_alt = ST["i_used"].values.astype(float), ST["e_i_used"].values.astype(float), ST["i_alt"].values.astype(float)
V_noP, alpha_pub = KN["V_noP"].values.astype(float), KN["alpha_pub"].values.astype(float)
sig, eVhi, eVlo = KN["sigma"].values.astype(float), KN["eV_hi"].values.astype(float), KN["eV_lo"].values.astype(float)
V2_base = V_noP ** 2 + alpha_pub * sig ** 2
is_alp = np.array([g.startswith("ALPAKA") for g in gid])
IA = gid.index("ALESS_122.1")

# ----------------------------------------------------------------- C2: source constants read from the TeX on disk (not retyped)
P("\nLOADER (C2): source constants parsed from the TeX on disk (external data directory beside the repo; read only)")
TEX_A = os.path.join(EXT, "arxiv_src", "2312.08959", "main.tex")
TEX_D = os.path.join(EXT, "arxiv_src", "2208.01622", "MonsterCalibration.tex")
DECL = dict(eq8=1.68, sig_cr18=129.0, vmax=564.0, vcirc=533.0, evcirc=37.0, sigma=157.0, inc=55.0, inc_lo=6.0, inc_hi=8.0, re=0.62,
            a850_smg=7.3e12, ea850_smg=0.1e12, aco_smg=3.8, eaco_smg=0.1, aci_smg=16.2, eaci_smg=0.4)
SRC = dict(DECL)
okA = okD = False
if os.path.exists(TEX_A):
    ta = open(TEX_A).read()
    m_eq8 = "+ 1.68 \\sigma^2 \\left( \\frac{r}{r_e} \\right)" in ta
    m_cr = re.search(r"V_\{\\rm max\} = (\d+) \\pm (\d+)\$ km\\,s\$\^\{-1\}\$ and \$\\sigma = (\d+) \\pm (\d+)\$", ta)
    m_row = re.search(r"^\s*\\textbf\{122\.1\} & \$([\d.]+)_\{\\, -([\d.]+)\}\^\{\\, \+([\d.]+)\}\$ & \$(\d+)_\{\\, -(\d+)\}\^\{\\, \+(\d+)\}\$ & "
                      r"\$(\d+)_\{\\, -(\d+)\}\^\{\\, \+(\d+)\}\$ & \$(\d+)_\{\\, -(\d+)\}\^\{\\, \+(\d+)\}\$ & \$(\d+)_\{\\, -(\d+)\}\^\{\\, \+(\d+)\}\$ & (\d+) \$\\pm\$ (\d+)", ta, re.M)
    if m_eq8 and m_cr and m_row:
        g = m_row.groups()
        SRC.update(eq8=1.68, sig_cr18=float(m_cr.group(3)), vmax=float(g[9]), vcirc=float(g[15]), evcirc=float(g[16]), sigma=float(g[12]),
                   inc=float(g[6]), inc_lo=float(g[7]), inc_hi=float(g[8]), re=float(g[0]))
        okA = (float(m_cr.group(1)) == 564.0)
if os.path.exists(TEX_D):
    td = open(TEX_D).read()
    m_smg = re.search(r"SMGs\s*&\s*\$([\d.]+)\\pm([\d.]+)\$\s*&\s*\$([\d.]+)\\pm([\d.]+)\$\s*&\s*\$([\d.]+)\\pm([\d.]+)\$", td)
    if m_smg and "include a factor 1.36 to account for He" in td:
        g = [float(v) for v in m_smg.groups()]
        SRC.update(a850_smg=g[0] * 1e12, ea850_smg=g[1] * 1e12, aco_smg=g[2], eaco_smg=g[3], aci_smg=g[4], eaci_smg=g[5])
        okD = True
P(f"  Amvrosiadis+ (2312.08959): eq. 8 coefficient {SRC['eq8']}, ALESS 122.1 r_e {SRC['re']}\", i {SRC['inc']} (-{SRC['inc_lo']}/+{SRC['inc_hi']}), V_max {SRC['vmax']}, sigma {SRC['sigma']}, "
  f"V_circ(2 r_e) {SRC['vcirc']} +- {SRC['evcirc']}; Calistro Rivera+18 image-plane sigma (quoted) {SRC['sig_cr18']}")
P(f"  Dunne+22 (2208.01622) single-tracer SMG row (incl. He): alpha850 {SRC['a850_smg']:.2e} +- {SRC['ea850_smg']:.1e}, alpha_CO {SRC['aco_smg']} +- {SRC['eaco_smg']}, alpha_CI {SRC['aci_smg']} +- {SRC['eaci_smg']}")
ab = AMB.loc["122.1"]
check("C2a the Amvrosiadis TeX gives eq. 8 (1.68 sigma^2 r/r_e), sigma_CR18 = 129 and the ALESS 122.1 row, equal to the repo's best-fit CSV and CFG229's kinematics file",
      f"TeX found {okA}; row V_circ {SRC['vcirc']}/{float(ab['vcirc_2re_kms'])}/{KN['V_pub'][IA]}, sigma {SRC['sigma']}/{float(ab['sigma_kms'])}/{sig[IA]}, V_max {SRC['vmax']}/{float(ab['vmax_kms'])}, i {SRC['inc']}/{float(ab['inc_deg'])}/{i_used[IA]}",
      okA and SRC["vcirc"] == float(ab["vcirc_2re_kms"]) == float(KN["V_pub"][IA]) and SRC["sigma"] == float(ab["sigma_kms"]) == sig[IA] and SRC["vmax"] == float(ab["vmax_kms"])
      and SRC["inc"] == float(ab["inc_deg"]) == i_used[IA] and SRC["sig_cr18"] == 129.0 and SRC["inc_lo"] == float(ab["inc_deg_errlo"]) and SRC["inc_hi"] == float(ab["inc_deg_errhi"]))
check("C2b the Dunne TeX gives the single-tracer SMG row 7.3 / 3.8 / 16.2 (incl. He)", f"TeX found {okD}; {SRC['a850_smg']:.2e} / {SRC['aco_smg']} / {SRC['aci_smg']}",
      okD and abs(SRC["a850_smg"] - 7.3e12) < 1 and SRC["aco_smg"] == 3.8 and SRC["aci_smg"] == 16.2)
dA = OPT["ad"].loc["ALESS122"]
check("C2c Dunne's ALESS122 opt_ad row equals CFG229's static inputs (logMH2 11.258 +- 0.104) and the master's L'_CO(1-0) 11.110 (JCorr 0), L850 24.052",
      f"logMH2 {dA['logMH2']} / {ST['logMH2'][IA]}; e {dA['e_logMH2']} / {e_gas[IA]}; LCO {DM.loc['ALESS122', 'logLCO']} / {dA['logLCO']}; L850 {DM.loc['ALESS122', 'logL850py']}; JCorr {dA['JCorr']}",
      float(dA["logMH2"]) == float(ST["logMH2"][IA]) and float(dA["e_logMH2"]) == e_gas[IA] and float(DM.loc["ALESS122", "logLCO"]) == float(dA["logLCO"]) == 11.110
      and float(DM.loc["ALESS122", "logL850py"]) == 24.052 and float(dA["JCorr"]) == 0.0)

# ===================================================================================== CFG229's random stream, replayed exactly (seed 230, the seven galaxies in order)
rngi = np.random.default_rng(SEED + 1)
DRAW = {}
REPLAY = {}
for i in range(n):
    g_ = rngi.normal(size=BMC)
    Vd = np.sqrt(V2_base[i]) + np.where(g_ > 0, g_ * eVhi[i], g_ * eVlo[i])
    fac = np.ones(BMC)
    ii = None
    if is_alp[i]:
        ii = rngi.normal(i_used[i], e_i[i], BMC)
        for _ in range(60):
            bad = (ii < 5) | (ii > 85)
            if not bad.any():
                break
            ii[bad] = rngi.normal(i_used[i], e_i[i], int(bad.sum()))
        fac = (math.sin(math.radians(i_used[i])) / np.sin(np.radians(ii))) ** 2
    rs = rngi.normal(0, e_st[i], BMC)
    rg = rngi.normal(0, e_gas[i], BMC)
    DRAW[gid[i]] = dict(Vd=Vd, ii=ii, rs=rs, rg=rg, Vc=float(np.sqrt(V2_base[i])))
    god = (Vd ** 2 / R0[i] * G2SI * 1.0) * fac                            # CFG229's own formula (GM = 1): the C1b replay
    Msd, Mgd = Ms0[i] * 10 ** rs, Mg0[i] * 10 ** rg
    gbd = gdisc(Msd, Re0[i], R0[i]) + gdisc(Mgd, Re0[i], R0[i])
    ls, unb = implied((god / gbd)[:, None], gbd[:, None], NU, A0)
    ok = ~unb
    REPLAY[gid[i]] = dict(frac_noroot=float(unb.mean()), q=[float(v) for v in np.percentile(ls[ok], [2.5, 16, 50, 84, 97.5])] if ok.sum() > 20 else [float("nan")] * 5)


# ===================================================================================== the cell evaluator
def classify(ls, unb):
    """per-draw: rooted log10 s*, floor (no root, s -> 0) or ceiling (limit above the bracket)"""
    floor = unb & (ls < 0)
    ceil = unb & (ls > 0)
    return floor, ceil


def mc_cell(g, V2nom, Vrot_c, T_c, Rr, Ms, Mg, e_s, e_g, i_c=None, vcomm=False):
    """10,000 MC draws for one cell with CFG229's deviates (common random numbers).  velocity scatter r = V_draw/V_committed applied to the whole V
    (rotation and pressure parts alike), the ALPAKA inclination draws shifted to the cell's inclination and applied to the rotation part only;
    baryons: the cell's statistical error times the same standard deviates."""
    d = DRAW[g]
    i = gid.index(g)
    if vcomm and not is_alp[i]:
        V2d = d["Vd"] ** 2                                                # bit-identical to CFG229 for the committed cell
    else:
        r = d["Vd"] / d["Vc"]
        if is_alp[i]:
            iic = np.clip(d["ii"] - i_used[i] + i_c, 5.0, 85.0)
            finc = math.sin(math.radians(i_c)) / np.sin(np.radians(iic))
        else:
            finc = 1.0
        V2d = (Vrot_c * r * finc) ** 2 + T_c * r ** 2
    V2d = V2d * VFAC ** 2
    god = (V2d / Rr * G2SI * 1.0) * np.ones(BMC)
    Msd = Ms * 10 ** (d["rs"] * (e_s / e_st[i]))
    Mgd = Mg * 10 ** (d["rg"] * (e_g / e_gas[i]))
    gbd = gdisc(Msd, Re0[i], Rr) + gdisc(Mgd, Re0[i], Rr)
    ls, unb = implied((god / gbd)[:, None], gbd[:, None], NU, A0)
    floor, ceil = classify(ls, unb)
    ok = ~unb
    q1 = [float(v) for v in np.percentile(ls[ok], [2.5, 16, 50, 84, 97.5])] if ok.sum() > 20 else [float("nan")] * 5
    la = np.where(floor, -99.0, np.where(ceil, 99.0, ls))
    q2 = [float(v) for v in np.percentile(la, [2.5, 16, 50, 84, 97.5])]
    return dict(q=q1, q_all=q2, frac_noroot=float(floor.mean()), frac_ceil=float(ceil.mean()))


def nominal(V2, Rr, Ms, Mg, i):
    go = V2 * VFAC ** 2 / Rr * G2SI * 1.0
    gb = float(gdisc(Ms, Re0[i], Rr) + gdisc(Mg, Re0[i], Rr))
    D = go / gb
    ls, unb = implied(np.array([[D]]), np.array([[gb]]), NU, A0)
    ls, unb = float(ls[0]), bool(unb[0])
    state = "root" if not unb else ("noroot" if ls < 0 else "limit")
    lam = float("nan")
    if state == "root":
        lm, lf = lever(np.array([D]), np.array([gb]), NU, A0)
        lam = float(lm[0]) if not bool(lf[0]) else float("nan")
    lp2, up2 = implied(np.array([[D]]), np.array([[gb]]), NU_P2, A0)
    return dict(g_obs=go, g_bar=gb, y=gb / A0, D=D, ls=ls, state=state, lever=lam, ls_p2=(float(lp2[0]) if not bool(up2[0]) else float("nan")))


def inside(q2_5, q97_5, lev):
    if not (math.isfinite(q2_5) and math.isfinite(q97_5)):
        return "undef"
    if q2_5 > lev:
        return "excl_above"
    if q97_5 < lev:
        return "excl_below"
    return "inside"


# ===================================================================================== ALESS 122.1: the levels
a = IA
zA = z[a]
EZ = E(zA)
LF, LH = 0.0, math.log10(EZ)
LF_alt, LH_alt = math.log10(ALT), math.log10(EZ * ALT)
sA, sM = SRC["sigma"], SRC["sig_cr18"]
reA, R2 = Re0[a], R0[a]
VROT2 = math.sqrt(SRC["vcirc"] ** 2 - SRC["eq8"] * sA ** 2 * (R2 / reA))  # eq. 8 inverted at 2 r_e
x2 = brentq(lambda x: 1 - math.atan(x) / x - VROT2 / SRC["vmax"], 1e-6, 1e6, xtol=1e-14)
r_t = R2 / x2
def vrot_arctan(Rr):
    x = Rr / r_t
    return SRC["vmax"] * (1 - math.atan(x) / x)
VROT1 = vrot_arctan(reA)
P(f"\nALESS 122.1 (z = {zA}; E(z) = {EZ:.4f}; canonical a0 {A0:.4e}, alt/canonical {ALT:.4f})")
P(f"  V_rot(2 r_e) from eq. 8 inverted: sqrt({SRC['vcirc']:.0f}^2 - 1.68 x {sA:.0f}^2 x 2) = {VROT2:.2f} km/s; arctan law with V_max {SRC['vmax']:.0f}: r_t = {r_t:.4f} kpc ({r_t / reA:.4f} r_e; "
  f"not tabulated, solved), V_rot(r_e) = {VROT1:.2f} km/s")
check("C3 the reconstruction: eq. 8 at 2 r_e gives back the published V_circ and the arctan law with the solved r_t gives back V_rot(2 r_e) (1e-9)",
      f"{math.sqrt(VROT2 ** 2 + 1.68 * sA ** 2 * 2.0):.10f} vs {SRC['vcirc']}; {vrot_arctan(R2):.10f} vs {VROT2:.10f}",
      abs(math.sqrt(VROT2 ** 2 + 1.68 * sA ** 2 * (R2 / reA)) - SRC["vcirc"]) < 1e-9 and abs(vrot_arctan(R2) - VROT2) < 1e-9)

PRESS = ["P0", "C168", "EQ8", "P1", "MSIG"]
def Tterm(lev, Rr, re_, s_, s_m):
    return {"P0": 0.0, "C168": 1.68 * s_ ** 2, "EQ8": 1.68 * s_ ** 2 * (Rr / re_), "P1": 3.36 * s_ ** 2 * (Rr / re_),
            "MSIG": (1.68 * s_m ** 2 * (Rr / re_) if s_m is not None else float("nan"))}[lev]

lLCO, eLCO = float(DM.loc["ALESS122", "logLCO"]), float(DM.loc["ALESS122", "e_logLCO"])
lL850, eL850 = float(DM.loc["ALESS122", "logL850py"]), float(DM.loc["ALESS122", "e_logL850py"])
GASA = {"G0": (float(ST["logMgas_He"][a]), e_gas[a]),
        "CO1": (math.log10(SRC["aco_smg"]) + lLCO, math.hypot(eLCO, SRC["eaco_smg"] / (SRC["aco_smg"] * LN10))),
        "DU1": (lL850 - math.log10(SRC["a850_smg"]), math.hypot(eL850, SRC["ea850_smg"] / (SRC["a850_smg"] * LN10))),
        "A08": (math.log10(0.8) + lLCO, eLCO), "A36": (math.log10(3.6) + lLCO, eLCO), "A436": (math.log10(4.36) + lLCO, eLCO)}
MSTA = {"M0": 0.0, "M+": +e_st[a], "M-": -e_st[a]}
INCA = {"i55": SRC["inc"], "i49": SRC["inc"] - SRC["inc_lo"], "i63": SRC["inc"] + SRC["inc_hi"]}
RADA = {"2re": R2, "re": reA}
P("  levels: pressure " + ", ".join(PRESS) + "; gas " + ", ".join(f"{k} log M {v[0]:.3f} (+-{v[1]:.3f})" for k, v in GASA.items())
  + f"; M* log {math.log10(Ms0[a]):.3f} +- {e_st[a]:.2f}; inclination " + ", ".join(f"{k} {v:.0f}" for k, v in INCA.items()) + f"; radius 2 r_e {R2:.4f} / r_e {reA:.4f} kpc")


def aless_cell(p, gk, mk, ik, rk):
    Rr = RADA[rk]
    vr = (VROT2 if rk == "2re" else VROT1) * math.sin(math.radians(SRC["inc"])) / math.sin(math.radians(INCA[ik]))
    T_ = Tterm(p, Rr, reA, sA, sM)
    commit_v = (p == "EQ8" and ik == "i55" and rk == "2re")
    V2 = V2_base[a] if commit_v else vr ** 2 + T_                         # the committed velocity exactly as CFG229 (533^2)
    lg, eg = GASA[gk]
    Mg = Mg0[a] if gk == "G0" else 10 ** lg
    Ms = Ms0[a] * 10 ** MSTA[mk]
    nm = nominal(V2, Rr, Ms, Mg, a)
    mc = mc_cell(gid[a], V2, vr, T_, Rr, Ms, Mg, e_st[a], eg, vcomm=commit_v)
    return dict(pressure=p, gas=gk, mstar=mk, incl=ik, radius=rk, V=math.sqrt(V2 * VFAC ** 2), R=Rr, logMgas=math.log10(Mg), logMstar=math.log10(Ms), **nm, **mc)


AX = dict(pressure=PRESS, gas=list(GASA), mstar=list(MSTA), incl=list(INCA), radius=list(RADA))
COMMIT = dict(pressure="EQ8", gas="G0", mstar="M0", incl="i55", radius="2re")
P(f"\nRUNNING the full grid: {np.prod([len(v) for v in AX.values()])} cells x {BMC} MC draws ...")
CELLS = [aless_cell(*c) for c in itertools.product(*AX.values())]
N = len(CELLS)
for c in CELLS:
    c["root"] = c["state"] != "noroot"
    for lab, (lf, lh), qk in (("", (LF, LH), "q"), ("_all", (LF, LH), "q_all"), ("_alt", (LF_alt, LH_alt), "q")):
        q = c[qk]
        c["FLAT" + lab] = (inside(q[0], q[4], lf) if c["state"] == "root" else "excl_above") if c["root"] else "noroot"
        c["Hz" + lab] = (inside(q[0], q[4], lh) if c["state"] == "root" else "excl_above") if c["root"] else "noroot"
    c["s"] = 10 ** c["ls"] if c["state"] == "root" else (float("inf") if c["state"] == "limit" else float("nan"))
cc = [c for c in CELLS if all(c[k] == v for k, v in COMMIT.items())][0]


def fmt_s(c):
    return "NO ROOT" if c["state"] == "noroot" else ("LIMIT>1e3" if c["state"] == "limit" else f"{c['s']:.3g}")


def fracs(cells, lab=""):
    Nn = len(cells)
    fF = sum(1 for c in cells if c["FLAT" + lab] == "excl_above") / Nn
    fH = sum(1 for c in cells if c["Hz" + lab] == "excl_above") / Nn
    fin = sum(1 for c in cells if c["FLAT" + lab] in ("inside", "undef")) / Nn
    fbel = sum(1 for c in cells if c["FLAT" + lab] == "excl_below") / Nn
    fnr = sum(1 for c in cells if not c["root"]) / Nn
    fHin = sum(1 for c in cells if c["Hz" + lab] in ("inside", "undef")) / Nn
    if fin >= 0.25 or fnr >= 0.25:
        dec = "NOT ROBUST"
    elif fF >= 0.80 and fH >= 0.50:
        dec = "ROBUSTLY ABOVE BOTH"
    else:
        dec = "MIXED"
    return dict(N=Nn, f_FLAT_excl=fF, f_Hz_excl=fH, f_FLAT_inside=fin, f_FLAT_below=fbel, f_noroot=fnr, f_Hz_inside=fHin, decision=dec)


# ----------------------------------------------------------------- C1: the committed cell = CFG229
r229 = R229["IMPL"]["ALESS_122.1"]
P("\nCOMMITTED CELL (EQ8, G0, M* nominal, i = 55, 2 r_e)")
P(f"  V {cc['V']:.2f} km/s, g_obs {cc['g_obs']:.4e}, g_bar {cc['g_bar']:.4e}, y {cc['y']:.3f}, D {cc['D']:.4f}, s* {fmt_s(cc)} (log {cc['ls']:+.6f}), lever {cc['lever']:+.2f}")
P(f"  MC (CFG229 convention, rooted draws): log s* 2.5/16/50/84/97.5 % = " + " / ".join(f"{v:+.4f}" for v in cc["q"]) + f"  -> 68 % {10 ** cc['q'][1]:.2f}-{10 ** cc['q'][3]:.2f}, 95 % {10 ** cc['q'][0]:.2f}-{10 ** cc['q'][4]:.2f}; no-root {cc['frac_noroot']:.4f}")
lo_all = "0 (floor)" if cc["q_all"][0] < -3 else f"{10 ** cc['q_all'][0]:.2f}"
P(f"  MC (secondary, all draws; no-root -> s = 0): " + " / ".join(("floor" if v < -3 else f"{v:+.4f}") for v in cc["q_all"]) + f"  -> 95 % {lo_all}-{10 ** cc['q_all'][4]:.2f}")
if not MUT:
    check("C1 the committed cell reproduces CFG229 exactly: log10 s*, the five MC quantiles and the no-root fraction (1e-12)",
          f"log s* {cc['ls']:.15f} vs {r229['s0'][0]:.15f}; max |dq| {max(abs(u - v) for u, v in zip(cc['q'], r229['stat']['q'])):.1e}; no-root {cc['frac_noroot']} vs {r229['stat']['frac_noroot']}",
          abs(cc["ls"] - r229["s0"][0]) < 1e-12 and max(abs(u - v) for u, v in zip(cc["q"], r229["stat"]["q"])) < 1e-12 and cc["frac_noroot"] == r229["stat"]["frac_noroot"])
    dmax = 0.0; nrok = True
    for g in gid:
        qa, qb = REPLAY[g]["q"], R229["IMPL"][g]["stat"]["q"]
        nrok &= REPLAY[g]["frac_noroot"] == R229["IMPL"][g]["stat"]["frac_noroot"]
        for u, v in zip(qa, qb):
            if not (math.isnan(u) and (v is None or (isinstance(v, float) and math.isnan(v)))):
                dmax = max(dmax, abs(u - float(v)))
    check("C1b the replayed stream reproduces CFG229's committed MC for all seven galaxies (no-root fractions identical; quantiles to 1e-12)", f"max |dq| {dmax:.1e}; no-root fractions identical {nrok}", nrok and dmax < 1e-12)

# ----------------------------------------------------------------- C4 independent inversion, C5 Hankel, C6 directions, C7 bookkeeping
def brent_ls(D, y):
    f = lambda ls: math.log10(D) - math.log10(float(NU(np.array([y / 10 ** ls]))[0]))
    if not (f(-3.0) > 0 and f(3.0) < 0):
        return None
    return brentq(f, -3.0, 3.0, xtol=1e-13, rtol=1e-14, maxiter=500)


bad4, nroot4 = 0, 0
for c in CELLS:
    b = brent_ls(c["D"], c["y"])
    if c["state"] == "root":
        nroot4 += 1
        if b is None or abs(b - c["ls"]) > 1e-6:
            bad4 += 1
    elif b is not None:
        bad4 += 1
check("C4 every rooted cell's s* equals an independent brentq inversion of nu_mono(y/s) = D (1e-6 dex), and no NO-ROOT cell has one", f"{nroot4} rooted cells; {bad4} mismatches", bad4 == 0)


def hankel_g(M, Re, Rr):
    Rd = Re / XN; S0 = M / (2 * math.pi * Rd ** 2)
    f_k = lambda k: k * j1(k * Rr) * (1 + (k * Rd) ** 2) ** (-1.5)
    edges = np.linspace(0, 400.0 / Rd, 4001)
    return 2 * math.pi * G_KPC * S0 * Rd ** 2 * sum(quad(f_k, a_, b_, limit=200)[0] for a_, b_ in zip(edges[:-1], edges[1:])) * G2SI


hk = [(hankel_g(1e11, reA, Rr), float(gdisc(1e11, reA, Rr))) for Rr in (R2, reA)]
check("C5 the Hankel-transform disc force equals the Bessel closed form at 2 r_e and r_e (1e-4)", "; ".join(f"{u:.6e} vs {v:.6e}" for u, v in hk), all(abs(u / v - 1) < 1e-4 for u, v in hk))

IDX = {tuple(c[k] for k in AX): c for c in CELLS}
viol = []
for key, c in IDX.items():
    p, gk, mk, ik, rk = key
    if p == "P0":
        seq = [IDX[("P0", gk, mk, ik, rk)]["D"], IDX[("C168", gk, mk, ik, rk)]["D"], IDX[("EQ8", gk, mk, ik, rk)]["D"], IDX[("P1", gk, mk, ik, rk)]["D"]]
        okp = seq[0] < seq[1] and (seq[1] < seq[2] if rk == "2re" else abs(seq[1] / seq[2] - 1) < 1e-12) and seq[2] < seq[3]
        if not okp: viol.append(("pressure", key))
    if gk == "G0":
        order = sorted(GASA, key=lambda k: GASA[k][0])
        ds = [IDX[(p, k, mk, ik, rk)]["D"] for k in order]
        if not all(u > v for u, v in zip(ds[:-1], ds[1:])): viol.append(("gas", key))
    if mk == "M0":
        if not (IDX[(p, gk, "M+", ik, rk)]["D"] < c["D"] < IDX[(p, gk, "M-", ik, rk)]["D"]): viol.append(("stars", key))
    if ik == "i55":
        if not (IDX[(p, gk, mk, "i49", rk)]["D"] > c["D"] > IDX[(p, gk, mk, "i63", rk)]["D"]): viol.append(("incl", key))
check("C6 directions over the grid: D rises P0 < C168 <= EQ8 < P1 (C168 = EQ8 at r_e), falls with more gas and more stars, rises as the inclination falls", f"{len(viol)} violations {viol[:3]}", len(viol) == 0)

book = [sum(1 for v in (not c["root"], c["FLAT"] == "excl_above", c["FLAT"] in ("inside", "undef"), c["FLAT"] == "excl_below") if v) for c in CELLS]
FR = fracs(CELLS)
check("C7 bookkeeping: each cell is exactly one of {no root, FLAT excluded above, FLAT inside, FLAT excluded below}; the four fractions sum to 1",
      f"cells with exactly one: {sum(1 for b in book if b == 1)}/{N}; sum {FR['f_noroot'] + FR['f_FLAT_excl'] + FR['f_FLAT_inside'] + FR['f_FLAT_below']:.12f}",
      all(b == 1 for b in book) and abs(FR["f_noroot"] + FR["f_FLAT_excl"] + FR["f_FLAT_inside"] + FR["f_FLAT_below"] - 1) < 1e-12)

# ===================================================================================== results: one axis at a time, the decision, the axis table
P("\nONE AXIS AT A TIME about the committed cell (s*; 68 % / 95 % CFG229-convention intervals; FLAT / H(z) vs the 95 % interval)")
P("  axis       level   V (km/s)  R (kpc)  log Mgas  log M*   y       D        s*          68 %            95 %            no-root  lever    FLAT        H(z)")
OAT = {}
for ax, levs in AX.items():
    OAT[ax] = {}
    for lv in levs:
        key = tuple((lv if k == ax else COMMIT[k]) for k in AX)
        c = IDX[key]
        OAT[ax][lv] = c
        q = c["q"]
        i68 = f"{10 ** q[1]:.2f}-{10 ** q[3]:.2f}" if c["root"] and math.isfinite(q[1]) else "-"
        i95 = f"{10 ** q[0]:.2f}-{10 ** q[4]:.2f}" if c["root"] and math.isfinite(q[0]) else "-"
        P(f"  {ax:9s}  {lv:6s}  {c['V']:7.1f}  {c['R']:6.2f}   {c['logMgas']:6.3f}   {c['logMstar']:6.3f}  {c['y']:6.2f}  {c['D']:7.4f}  {fmt_s(c):>9s}  {i68:>14s}  {i95:>14s}   {c['frac_noroot']:.3f}  {c['lever']:+6.2f}  {c['FLAT']:10s}  {c['Hz']:10s}")
OAT_RANGE = {}
for ax in AX:
    vals = [OAT[ax][lv] for lv in AX[ax]]
    rooted = [c["ls"] for c in vals if c["state"] == "root"]
    OAT_RANGE[ax] = dict(removes_root=any(not c["root"] for c in vals), range_dex=(max(rooted) - min(rooted)) if len(rooted) >= 2 else 0.0,
                         lo=min(rooted) if rooted else float("nan"), hi=max(rooted) if rooted else float("nan"))
PER_LEVEL = {}
for ax in AX:
    PER_LEVEL[ax] = {}
    for lv in AX[ax]:
        sub = [c for c in CELLS if c[ax] == lv]
        rl = [c["ls"] for c in sub if c["state"] == "root"]
        PER_LEVEL[ax][lv] = dict(n=len(sub), f_root=sum(1 for c in sub if c["root"]) / len(sub), f_FLAT_excl=sum(1 for c in sub if c["FLAT"] == "excl_above") / len(sub),
                                 f_Hz_excl=sum(1 for c in sub if c["Hz"] == "excl_above") / len(sub), med_ls_rooted=float(np.median(rl)) if rl else float("nan"))
spread_root = {ax: max(v["f_root"] for v in PER_LEVEL[ax].values()) - min(v["f_root"] for v in PER_LEVEL[ax].values()) for ax in AX}
RANK = sorted(AX, key=lambda ax: (OAT_RANGE[ax]["removes_root"], OAT_RANGE[ax]["range_dex"], spread_root[ax]), reverse=True)
P("\nAXIS RANKING (frozen rule: one-axis range of log10 s*; an axis with a NO-ROOT level ranks above any finite range; ties by the spread of the full-grid root fraction)")
for k, ax in enumerate(RANK, 1):
    r = OAT_RANGE[ax]
    P(f"  {k}. {ax:9s} removes the root: {str(r['removes_root']):5s}  rooted one-axis range {r['range_dex']:.3f} dex (s* {10 ** r['lo']:.3g} to {10 ** r['hi']:.3g})  "
      f"full-grid root fraction by level: " + ", ".join(f"{lv} {PER_LEVEL[ax][lv]['f_root']:.2f}" for lv in AX[ax]))
P("\nFULL-GRID PER-LEVEL TABLE (fraction of the cells at that level: rooted / FLAT excluded above / H(z) excluded above; median rooted log10 s*)")
for ax in AX:
    P(f"  {ax:9s} " + "   ".join(f"{lv}: {v['f_root']:.2f}/{v['f_FLAT_excl']:.2f}/{v['f_Hz_excl']:.2f} ({v['med_ls_rooted']:+.2f})" for lv, v in PER_LEVEL[ax].items()))

DEC = dict(primary=FR, secondary=fracs(CELLS, "_all"), alt_footing=fracs(CELLS, "_alt"),
           only_2re=fracs([c for c in CELLS if c["radius"] == "2re"]), oat=fracs([IDX[k] for k in {tuple((lv if kk == ax else COMMIT[kk]) for kk in AX) for ax in AX for lv in AX[ax]}]))
P(f"\nDECISION (frozen rule; primary = CFG229-convention intervals, canonical footing, all {N} cells)")
P("  set                         N     FLAT excl.  H(z) excl.  FLAT inside  FLAT below  no root   -> decision")
for k, lab in (("primary", "PRIMARY (gates the wording)"), ("secondary", "secondary (all draws)"), ("alt_footing", f"alt footing (FLAT s={ALT:.4f})"), ("only_2re", "2 r_e only (beside)"), ("oat", "one axis at a time (beside)")):
    d = DEC[k]
    P(f"  {lab:27s} {d['N']:4d}   {d['f_FLAT_excl']:8.3f}   {d['f_Hz_excl']:8.3f}    {d['f_FLAT_inside']:8.3f}    {d['f_FLAT_below']:8.3f}  {d['f_noroot']:7.3f}   -> {d['decision']}")
rooted_s = np.array([c["s"] for c in CELLS if c["state"] == "root"])
P(f"  rooted cells: {len(rooted_s)} of {N}; s* median {np.median(rooted_s):.3g}, 16-84 % of the rooted cells {np.percentile(rooted_s, 16):.3g}-{np.percentile(rooted_s, 84):.3g}, range {rooted_s.min():.3g}-{rooted_s.max():.3g}")

# ----------------------------------------------------------------- beside rows (never in the decision)
P("\nBESIDE (one-axis changes from the committed cell that the criteria exclude from the grid; printed only)")
BES = {}
def beside(label, Mg=None, Ms=None, T_=None):
    Mg = Mg0[a] if Mg is None else Mg
    Ms = Ms0[a] if Ms is None else Ms
    if T_ is None:
        V2 = V2_base[a]; vr = VROT2; T_ = SRC["eq8"] * sA ** 2 * 2.0; vc = True
    else:
        V2 = VROT2 ** 2 + T_; vr = VROT2; vc = False
    nm = nominal(V2, R2, Ms, Mg, a)
    mc = mc_cell(gid[a], V2, vr, T_, R2, Ms, Mg, e_st[a], e_gas[a], vcomm=vc)
    BES[label] = dict(**nm, **mc)
    q = mc["q"]
    P(f"  {label:66s} D {nm['D']:.4f}  s* {('NO ROOT' if nm['state'] != 'root' else format(10 ** nm['ls'], '.3g')):>8s}  95 % " + (f"{10 ** q[0]:.2f}-{10 ** q[4]:.2f}" if nm["state"] == "root" and math.isfinite(q[0]) else "-"))
beside("gas: Dunne luminosity-dependent CO fit (log a_CO = -0.062 log L' + 1.25)", Mg=10 ** ((-0.062 * lLCO + 1.25) + lLCO))
beside("gas: Dunne luminosity-dependent dust fit (log a850 = 0.052 log L850 + 11.60)", Mg=10 ** (lL850 - (0.052 * lL850 + 11.60)))
beside("gas: Amvrosiadis parent table 11.30 (Calistro Rivera+18; conversion not on disk)", Mg=10 ** 11.30)
beside("gas: alpha_CO 0.92 x L'_CO (Amvrosiadis; f_DM = 0.25 halo-anchored: EXCLUDED)", Mg=10 ** (math.log10(0.92) + lLCO))
beside("stars: CFG229's declared band +0.30 dex", Ms=Ms0[a] * 10 ** 0.30)
beside("stars: CFG229's declared band -0.30 dex", Ms=Ms0[a] * 10 ** -0.30)
beside("pressure: Burkert P1 form with sigma = 129 (3.36 x 129^2 x 2)", T_=3.36 * sM ** 2 * 2.0)

# ===================================================================================== siblings
P("\nSIBLINGS: the same grid on each galaxy's own record (committed: ALPAKA P0 / V_ext at R_ext; BX610 P1 at R_e = FS+18 Eq. 1)")
DN = {g: str(ST["dunne_name"][gid.index(g)]) for g in gid}


def sib_levels(g):
    i = gid.index(g)
    dn = DN[g]
    mrow = DM.loc[dn]
    L = {}
    # gas
    gas = {"G0": (float(ST["logMgas_He"][i]), e_gas[i], True)}
    if g == "SINS_BX610":
        for t in ("ad", "xa", "xd"):
            if dn in OPT[t].index:
                gas[f"D_{t}"] = (float(OPT[t].loc[dn, "logMH2"]) + LOGHE, float(OPT[t].loc[dn, "e_logMH2"]), False)
    lco, elco = float(mrow["logLCO"]), float(mrow["e_logLCO"])
    lci, elci = float(mrow["logLCI"]), float(mrow["e_logLCI"])
    l850, el850 = float(mrow["logL850py"]), float(mrow["e_logL850py"])
    if math.isfinite(lco):
        gas["CO1"] = (math.log10(SRC["aco_smg"]) + lco, math.hypot(elco, SRC["eaco_smg"] / (SRC["aco_smg"] * LN10)), False)
    if math.isfinite(lci):
        gas["CI1"] = (math.log10(SRC["aci_smg"]) + lci, math.hypot(elci, SRC["eaci_smg"] / (SRC["aci_smg"] * LN10)), False)
    if math.isfinite(l850):
        gas["DU1"] = (l850 - math.log10(SRC["a850_smg"]), math.hypot(el850 if math.isfinite(el850) else 0.0, SRC["ea850_smg"] / (SRC["a850_smg"] * LN10)), False)
    if math.isfinite(lco):
        for k, aco in (("A08", 0.8), ("A36", 3.6), ("A436", 4.36)):
            gas[k] = (math.log10(aco) + lco, elco, False)
    L["gas"] = gas
    L["mstar"] = {"M0": 0.0, "M+": e_st[i], "M-": -e_st[i]}
    if is_alp[i]:
        aid = int(g.replace("ALPAKA", ""))
        sm = float(ALK.loc[aid, "sigma_m_kms"])
        L["pressure"] = PRESS
        L["sig_m"] = sm
        L["incl"] = {"i0": i_used[i], "i-1s": max(5.0, i_used[i] - e_i[i]), "i+1s": min(85.0, i_used[i] + e_i[i]), "i_alt": i_alt[i]}
        rd = ALD[(ALD["id"] == aid) & (ALD["panel"] == "V")].sort_values("R_kpc")
        rad = {"Rext": (R0[i], V_noP[i])}
        if rd["R_kpc"].min() <= Re0[i] <= rd["R_kpc"].max():
            rad["Re"] = (Re0[i], float(np.interp(Re0[i], rd["R_kpc"].values, rd["value_kms"].values)))
        L["radius"] = rad
        L["commit"] = dict(pressure="P0", gas="G0", mstar="M0", incl="i0", radius="Rext")
    else:                                                                   # BX610: FS+18 Table 6
        s6 = SN6.loc["Q2343-BX610"]
        si, slo, shi = float(s6["sin_i"]), float(s6["sin_i_errlo"]), float(s6["sin_i_errhi"])
        L["pressure"] = ["P0", "C168", "EQ8", "P1"]
        L["sig_m"] = None
        L["incl"] = {"i0": i_used[i], "i-1s": math.degrees(math.asin(si - slo)), "i+1s": math.degrees(math.asin(min(1.0, si + shi)))}
        L["radius"] = {"Re": (R0[i], V_noP[i])}
        L["commit"] = dict(pressure="P1", gas="G0", mstar="M0", incl="i0", radius="Re")
    return L


SIB = {}
SIB_ROWS = []
for g in gid:
    if g == "ALESS_122.1":
        continue
    i = gid.index(g)
    L = sib_levels(g)
    rows = []
    for p, gk, mk, ik, rk in itertools.product(L["pressure"], L["gas"], L["mstar"], L["incl"], L["radius"]):
        Rr, Vr_R = L["radius"][rk]
        vr = Vr_R * math.sin(math.radians(i_used[i])) / math.sin(math.radians(L["incl"][ik]))
        T_ = Tterm(p, Rr, Re0[i], sig[i], L["sig_m"])
        comm = dict(pressure=p, gas=gk, mstar=mk, incl=ik, radius=rk) == L["commit"]
        V2 = V2_base[i] if (p == L["commit"]["pressure"] and ik == "i0" and rk == L["commit"]["radius"]) else vr ** 2 + T_
        lg, eg, isg0 = L["gas"][gk]
        Mg = Mg0[i] if isg0 else 10 ** lg
        Ms = Ms0[i] * 10 ** L["mstar"][mk]
        nm = nominal(V2, Rr, Ms, Mg, i)
        row = dict(gid=g, pressure=p, gas=gk, mstar=mk, incl=ik, radius=rk, committed=comm, V=math.sqrt(V2 * VFAC ** 2), R=Rr, logMgas=math.log10(Mg), logMstar=math.log10(Ms),
                   i_deg=L["incl"][ik], **nm)
        if nm["state"] != "noroot":                                     # a LIMIT (s* above the bracket) counts as a root above every law (criteria section 2)
            mc = mc_cell(g, V2, vr, T_, Rr, Ms, Mg, e_st[i], eg, i_c=L["incl"][ik])
            row.update(mc)
            lFz, lHz = 0.0, math.log10(E(z[i]))
            if nm["state"] == "limit":
                row["FLAT"] = row["Hz"] = "excl_above"
            else:
                row["FLAT"] = inside(mc["q"][0], mc["q"][4], lFz); row["Hz"] = inside(mc["q"][0], mc["q"][4], lHz)
        else:
            row.update(q=[float("nan")] * 5, q_all=[float("nan")] * 5, frac_noroot=float("nan"), frac_ceil=float("nan"), FLAT="noroot", Hz="noroot")
        rows.append(row)
    SIB_ROWS += rows
    nr = sum(1 for r in rows if r["state"] != "noroot")
    best = max(rows, key=lambda r: r["D"])
    cm = [r for r in rows if r["committed"]][0]
    SIB[g] = dict(n_cells=len(rows), n_root=nr, f_root=nr / len(rows), gains_root=nr > 0, D_committed=cm["D"], D_max=best["D"],
                  best_cell={k: best[k] for k in ("pressure", "gas", "mstar", "incl", "radius")}, levels={k: (list(v) if isinstance(v, (dict, list)) else v) for k, v in L.items() if k != "commit"},
                  root_cells=[{k: r[k] for k in ("pressure", "gas", "mstar", "incl", "radius", "D", "state")} | {"s": (10 ** r["ls"] if r["state"] == "root" else float("inf")), "FLAT": r["FLAT"], "Hz": r["Hz"]} for r in rows if r["state"] != "noroot"])
    rl = SIB[g]["root_cells"]
    by = {ax: sorted({c[ax] for c in rl}) for ax in ("pressure", "gas", "mstar", "incl", "radius")}
    P(f"  {g:11s} cells {len(rows):4d}; committed D {cm['D']:.3f}; max D {best['D']:.3f} at {best['pressure']}/{best['gas']}/{best['mstar']}/{best['incl']}/{best['radius']}; "
      f"ROOTED cells {nr} ({100 * nr / len(rows):.1f} %)" + (f"; the rooted cells use: " + "; ".join(f"{ax} {by[ax]}" for ax in by) + f"; s* {min(c['s'] for c in rl):.3g}-{max(c['s'] for c in rl):.3g}" if nr else ""))
if not MUT:
    dd = max(abs(SIB[g]["D_committed"] - R229["D"][gid.index(g)]) / R229["D"][gid.index(g)] for g in SIB)
    check("C8 each sibling's committed cell reproduces CFG229's committed D (relative 1e-9)", f"max relative difference {dd:.1e}", dd < 1e-9)
n_gain = sum(1 for g in SIB if SIB[g]["gains_root"])
P(f"  => {n_gain} of {len(SIB)} siblings gain a root in at least one cell: {[g for g in SIB if SIB[g]['gains_root']]}; none: {[g for g in SIB if not SIB[g]['gains_root']]}")

# ----------------------------------------------------------------- common-calibration outlier test
P("\nCOMMON-CALIBRATION OUTLIER TEST (each shared recipe at every galaxy's committed M*, inclination and radius; log10 D; ALESS 122.1's rank and gap to the largest sibling)")
P("  recipe          n   log D: " + " ".join(f"{g[:9]:>9s}" for g in gid) + "   ALESS rank  gap (dex)  galaxies with a root")
COMMON = []
for p in ("P0", "C168", "EQ8", "P1"):
    for gk in ("G0", "DU1", "CO1", "A08", "A36", "A436"):
        vals = {}
        for g in gid:
            i = gid.index(g)
            if g == "ALESS_122.1":
                vr, Rr, T_ = VROT2, R2, Tterm(p, R2, reA, sA, sM)
                if gk not in GASA: continue
                Mg = Mg0[a] if gk == "G0" else 10 ** GASA[gk][0]
                V2 = V2_base[a] if p == "EQ8" else vr ** 2 + T_
            else:
                L = sib_levels(g)
                if gk not in L["gas"] or p not in L["pressure"]: continue
                rk = L["commit"]["radius"]; Rr, vr = L["radius"][rk]
                T_ = Tterm(p, Rr, Re0[i], sig[i], L["sig_m"])
                Mg = Mg0[i] if gk == "G0" else 10 ** L["gas"][gk][0]
                V2 = V2_base[i] if p == L["commit"]["pressure"] else vr ** 2 + T_
            nm = nominal(V2, Rr, Ms0[i], Mg, i)
            vals[g] = nm
        if "ALESS_122.1" not in vals: continue
        lds = {g: math.log10(v["D"]) for g, v in vals.items()}
        sibs = {g: v for g, v in lds.items() if g != "ALESS_122.1"}
        rank = 1 + sum(1 for v in sibs.values() if v > lds["ALESS_122.1"])
        gap = lds["ALESS_122.1"] - max(sibs.values())
        nroot = [g for g, v in vals.items() if v["state"] != "noroot"]
        COMMON.append(dict(recipe=f"{p}/{gk}", n=len(vals), logD=lds, aless_rank=rank, gap=gap, rooted=nroot))
        P(f"  {p + '/' + gk:14s} {len(vals):2d}         " + " ".join(f"{lds[g]:+9.3f}" if g in lds else f"{'-':>9s}" for g in gid) + f"     {rank:2d}       {gap:+.3f}    {nroot}")
gaps = [c["gap"] for c in COMMON]
n_top = sum(1 for c in COMMON if c["aless_rank"] == 1)
P(f"  => ALESS 122.1 has the largest D in {n_top} of {len(COMMON)} shared recipes; gap to the largest sibling median {np.median(gaps):+.3f} dex (range {min(gaps):+.3f} to {max(gaps):+.3f})")
P("  Dunne+22 per-galaxy optimised conversions (descriptive, read from the opt tables): " + "; ".join(
    f"{g}: a_CO {OPT[t].loc[DN[g], 'aCO']:.2f}" + (f", kappa_H {OPT[t].loc[DN[g], 'kappaH']:.0f}" if "kappaH" in OPT[t].columns else "") for g in gid for t in ("ad", "dax") if DN[g] in OPT[t].index and (t == "ad" or DN[g] not in OPT["ad"].index)))

# ===================================================================================== MUTATE controls
if MUT:
    P("\nMUTATE CONTROLS (V x 0.7 in every cell: D x 0.49)")
    base_p = os.path.join(LANE, "cfg307_stress_results.json")
    if os.path.exists(base_p):
        B0 = json.load(open(base_p))
        b_cells = {tuple(c[k] for k in AX): c for c in B0["cells"]}
        badm, nchk, notless = 0, 0, 0
        for key, c in IDX.items():
            b = b_cells[key]
            D0 = b["D"]
            exp = brent_ls(D0 * 0.49, b["y"])
            nchk += 1
            if exp is None:
                if c["state"] == "root": badm += 1
            else:
                if c["state"] != "root" or abs(c["ls"] - exp) > 1e-6: badm += 1
                if b["state"] == "root" and not (c["ls"] < b["ls"]): notless += 1
        check("M1 every cell's mutated s* equals the independent inversion at D x 0.49 (root exactly where it has one; 1e-6 dex)", f"{nchk} cells; {badm} mismatches", badm == 0)
        check("M2 every cell that keeps a root has a smaller s* than in the main run", f"{notless} cells not smaller; kept roots {sum(1 for c in CELLS if c['state'] == 'root')} of {N} (main run {sum(1 for c in B0['cells'] if c['state'] == 'root')})", notless == 0)
    else:
        check("M1/M2 need the main run's cfg307_stress_results.json first", "missing", False)

# ===================================================================================== hand estimates
HAND = []
def hs(tag, text, ok):
    HAND.append((tag, bool(ok))); P(f"  {tag:4s} {'REPRODUCES' if ok else 'WRONG     '} {text}")
if not MUT:
    P("\nHAND ESTIMATES (frozen in FROZEN_CRITERIA.md section 8; scored by code; misses kept)")
    sv = lambda ax, lv: OAT[ax][lv]
    def s_in(c, lo, hi): return c["state"] == "root" and lo <= c["s"] <= hi
    hs("H1", "the committed cell reproduces CFG229 exactly (C1)", abs(cc["ls"] - r229["s0"][0]) < 1e-12 and max(abs(u - v) for u, v in zip(cc["q"], r229["stat"]["q"])) < 1e-12)
    hs("H2", f"pressure one axis: P0 {fmt_s(sv('pressure', 'P0'))} (2.2-3.3), C168 {fmt_s(sv('pressure', 'C168'))} (4.5-6.5), P1 {fmt_s(sv('pressure', 'P1'))} (15-21), MSIG {fmt_s(sv('pressure', 'MSIG'))} (5.5-7.5)",
       s_in(sv("pressure", "P0"), 2.2, 3.3) and s_in(sv("pressure", "C168"), 4.5, 6.5) and s_in(sv("pressure", "P1"), 15, 21) and s_in(sv("pressure", "MSIG"), 5.5, 7.5))
    co1 = sv("gas", "CO1")
    hs("H3", f"gas one axis: A436 {fmt_s(sv('gas', 'A436'))} (NO ROOT), CO1 {fmt_s(co1)} (1.0-1.6 or NO ROOT), A36 {fmt_s(sv('gas', 'A36'))} (1.4-2.2), DU1 {fmt_s(sv('gas', 'DU1'))} (13-19), A08 {fmt_s(sv('gas', 'A08'))} (18-28)",
       sv("gas", "A436")["state"] == "noroot" and (co1["state"] == "noroot" or s_in(co1, 1.0, 1.6)) and s_in(sv("gas", "A36"), 1.4, 2.2) and s_in(sv("gas", "DU1"), 13, 19) and s_in(sv("gas", "A08"), 18, 28))
    hs("H4", f"M* +0.21 -> {fmt_s(sv('mstar', 'M+'))} (6.3-6.9), -0.21 -> {fmt_s(sv('mstar', 'M-'))} (10.3-10.9)", s_in(sv("mstar", "M+"), 6.3, 6.9) and s_in(sv("mstar", "M-"), 10.3, 10.9))
    hs("H5", f"inclination 49 -> {fmt_s(sv('incl', 'i49'))} (10.5-14.5), 63 -> {fmt_s(sv('incl', 'i63'))} (5.3-7.2)", s_in(sv("incl", "i49"), 10.5, 14.5) and s_in(sv("incl", "i63"), 5.3, 7.2))
    cre = sv("radius", "re")
    hs("H6", f"at r_e D = {cre['D']:.4f} (0.93-1.12) and s* {fmt_s(cre)} (< 1.5 or NO ROOT)", 0.93 <= cre["D"] <= 1.12 and (cre["state"] == "noroot" or cre["s"] < 1.5))
    hs("H7", f"the dominant axis is the gas and the radius is second (ranking {RANK})", RANK[0] == "gas" and RANK[1] == "radius")
    hs("H8", f"decision NOT ROBUST with f_noroot >= 0.25 and f_FLAT,in >= 0.25 ({FR['decision']}; {FR['f_noroot']:.3f}; {FR['f_FLAT_inside']:.3f})", FR["decision"] == "NOT ROBUST" and FR["f_noroot"] >= 0.25 and FR["f_FLAT_inside"] >= 0.25)
    hs("H9", f"f_FLAT,excl {FR['f_FLAT_excl']:.3f} (0.15-0.35), f_H,excl {FR['f_Hz_excl']:.3f} (0.04-0.18), f_noroot {FR['f_noroot']:.3f} (0.30-0.55)",
       0.15 <= FR["f_FLAT_excl"] <= 0.35 and 0.04 <= FR["f_Hz_excl"] <= 0.18 and 0.30 <= FR["f_noroot"] <= 0.55)
    hs("H10", f"the 2 r_e-only subgrid is NOT ROBUST ({DEC['only_2re']['decision']})", DEC["only_2re"]["decision"] == "NOT ROBUST")
    a18 = [c for c in SIB["ALPAKA18"]["root_cells"] if c["incl"] == "i-1s"]
    hs("H11", f"3 or 4 siblings gain a root ({n_gain}); ALPAKA 15 and 20 none ({SIB['ALPAKA15']['n_root']}, {SIB['ALPAKA20']['n_root']}); ALPAKA 18 through i-1s ({len(a18)} cells); every rooted fraction < 0.15 ({max(SIB[g]['f_root'] for g in SIB):.3f} max)",
       n_gain in (3, 4) and SIB["ALPAKA15"]["n_root"] == 0 and SIB["ALPAKA20"]["n_root"] == 0 and len(a18) > 0 and all(SIB[g]["f_root"] < 0.15 for g in SIB))
    hs("H12", f"ALESS 122.1 has the largest D in every shared recipe ({n_top} of {len(COMMON)}) with a median gap >= 0.3 dex ({np.median(gaps):+.3f})", n_top == len(COMMON) and np.median(gaps) >= 0.3)
    P(f"  H13  scored in the MUTATE run (it needs the mutated grid)")
    hs("H14", f"the secondary convention gives the same decision ({DEC['secondary']['decision']}); the committed cell's secondary 95 % lower bound {('0 (floor)' if cc['q_all'][0] < -3 else format(10 ** cc['q_all'][0], '.3f'))} in 1.0-1.3",
       DEC["secondary"]["decision"] == FR["decision"] and cc["q_all"][0] > -3 and 1.0 <= 10 ** cc["q_all"][0] <= 1.3)
    P(f"  => {sum(1 for t, o in HAND if o)} of {len(HAND)} scored hand estimates reproduce (H13 in the MUTATE run)")
else:
    P("\nHAND ESTIMATE H13 (scored here)")
    nkeep = sum(1 for c in CELLS if c["state"] == "root")
    hs("H13", f"the committed cell loses its root (D {cc['D']:.4f}, state {cc['state']}) and fewer than 20 % of the cells keep a root ({nkeep}/{N} = {nkeep / N:.3f})",
       cc["state"] == "noroot" and 0.93 <= cc["D"] <= 0.95 and nkeep / N < 0.20)

# ===================================================================================== outputs
P(f"\n{sum(CHK)}/{len(CHK)} checks pass; {time.time() - T0:.0f} s")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o
res = dict(mode=MODE, frozen="3b1ca88f7", z=zA, E_z=EZ, alt_over_can=ALT, VROT_2re=VROT2, VROT_re=VROT1, r_t_kpc=r_t, source_constants=SRC,
           committed=dict(cell={k: cc[k] for k in ("V", "D", "y", "ls", "s", "q", "q_all", "frac_noroot", "lever", "FLAT", "Hz", "FLAT_all", "Hz_all")}, cfg229=r229["s0"] + [r229["stat"]]),
           decision=DEC, axis_ranking=RANK, oat_range=OAT_RANGE, per_level=PER_LEVEL,
           oat={ax: {lv: {k: OAT[ax][lv][k] for k in ("V", "R", "logMgas", "logMstar", "y", "D", "state", "ls", "q", "q_all", "frac_noroot", "lever", "FLAT", "Hz")} for lv in AX[ax]} for ax in AX},
           beside=BES, siblings=SIB, n_siblings_gain_root=n_gain, common=COMMON, replay=REPLAY, hand=HAND, checks=CHK,
           cells=[{k: c[k] for k in ("pressure", "gas", "mstar", "incl", "radius", "V", "R", "logMgas", "logMstar", "g_obs", "g_bar", "y", "D", "state", "ls", "lever", "ls_p2",
                                     "q", "q_all", "frac_noroot", "frac_ceil", "FLAT", "Hz", "FLAT_all", "Hz_all", "FLAT_alt", "Hz_alt")} for c in CELLS])
json.dump(clean(res), open(os.path.join(LANE, f"cfg307_stress_results{TAG}.json"), "w"), indent=1, default=float)
rows = []
for c in CELLS:
    q, qa = c["q"], c["q_all"]
    rows.append(dict(pressure=c["pressure"], gas=c["gas"], mstar=c["mstar"], incl=c["incl"], radius=c["radius"], committed=all(c[k] == v for k, v in COMMIT.items()),
                     V_kms=c["V"], R_kpc=c["R"], logMgas=c["logMgas"], logMstar=c["logMstar"], g_obs=c["g_obs"], g_bar=c["g_bar"], y=c["y"], D=c["D"], state=c["state"],
                     s_star=(10 ** c["ls"] if c["state"] == "root" else np.nan), log10_s=(c["ls"] if c["state"] == "root" else np.nan), lever=c["lever"],
                     s_lo95=(10 ** q[0] if c["root"] and math.isfinite(q[0]) else np.nan), s_lo68=(10 ** q[1] if c["root"] and math.isfinite(q[1]) else np.nan),
                     s_med=(10 ** q[2] if c["root"] and math.isfinite(q[2]) else np.nan), s_hi68=(10 ** q[3] if c["root"] and math.isfinite(q[3]) else np.nan),
                     s_hi95=(10 ** q[4] if c["root"] and math.isfinite(q[4]) else np.nan), frac_mc_noroot=c["frac_noroot"],
                     s_lo95_alldraws=(0.0 if qa[0] < -3 else 10 ** qa[0]), s_hi95_alldraws=(np.inf if qa[4] > 3 else 10 ** qa[4]),
                     FLAT_vs_95=c["FLAT"], Hz_vs_95=c["Hz"], FLAT_vs_95_alldraws=c["FLAT_all"], Hz_vs_95_alldraws=c["Hz_all"], FLAT_vs_95_altfooting=c["FLAT_alt"], Hz_vs_95_altfooting=c["Hz_alt"],
                     s_star_P2kernel=(10 ** c["ls_p2"] if math.isfinite(c["ls_p2"]) else np.nan)))
pd.DataFrame(rows).to_csv(os.path.join(LANE, f"cfg307_grid{TAG}.csv"), index=False, float_format="%.6g")
srows = []
for r in SIB_ROWS:
    q = r["q"]
    srows.append(dict(gid=r["gid"], pressure=r["pressure"], gas=r["gas"], mstar=r["mstar"], incl=r["incl"], radius=r["radius"], committed=r["committed"], i_deg=r["i_deg"], V_kms=r["V"], R_kpc=r["R"],
                      logMgas=r["logMgas"], logMstar=r["logMstar"], y=r["y"], D=r["D"], state=r["state"], s_star=(10 ** r["ls"] if r["state"] == "root" else (np.inf if r["state"] == "limit" else np.nan)),
                      s_lo95=(10 ** q[0] if math.isfinite(q[0]) else np.nan), s_hi95=(10 ** q[4] if math.isfinite(q[4]) else np.nan), FLAT_vs_95=r["FLAT"], Hz_vs_95=r["Hz"]))
pd.DataFrame(srows).to_csv(os.path.join(LANE, f"cfg307_siblings_grid{TAG}.csv"), index=False, float_format="%.6g")
txt = "\n".join(OUT).replace(REPO, "<repo>").replace(os.path.dirname(REPO), "<parent>")
open(os.path.join(LANE, f"cfg307_stress{TAG}.out"), "w").write(txt + "\n")
sys.exit(0 if all(CHK) else 1)
