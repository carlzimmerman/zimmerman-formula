#!/usr/bin/env python3
"""FINAL4 (GROWTH) -- the structure-growth history the formation reading gives, graded on the record's own gates.

Criteria FROZEN_CRITERIA.md, committed alone (c5d897706f) before this file and before any FINAL4 number.
  1  the two-fluid linear growth system, its coefficients, and where it departs from the cold-reference form
  2  P(k, z) through FRZ1's forest gate (12 DESI P1D bins z 2.2-4.4, 755 pts, full covariance, dchi2 <= 4)
  3  CMB-lensing amplitude (GAL1's PR4 best-amplitude rule) and DESI DR1 f sigma8 (4 bins)
  4  the tilt verdict, and PR-F4 printed either way
Read-only reuse from their own paths; nothing written in their folders. TEST lane; adopts nothing.
"""
import os, sys, json, math, time, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FRZ = os.path.join(REPO, "closure_2026_11_10", "FRZ1_forest_redistribution_at_z")
SRH = os.path.join(REPO, "closure_2026_11_10", "SRH1_settled_radius_history")
CO1D = os.path.join(REPO, "closure_2026_11_09", "CO1_form_b_cosmology_computed")
QX3 = os.path.join(REPO, "closure_2026_11_06", "QX3_cmb_growth", "iter2_kq_dust")

OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def sec(t):
    P(""); P("-- " + t + " --")
T0 = time.time(); tm = lambda: f"[{time.time()-T0:7.1f}s]"
P("=" * 100)
P("FINAL4 (GROWTH)  the structure-growth history the formation reading gives, graded")
P("     criteria FROZEN_CRITERIA.md (c5d897706f).  kappa = 1/2 FITTED; not theory closed.  Adopts nothing.")
P("=" * 100)

# ================================================================ the record's own machinery (read-only)
_s = open(os.path.join(SRH, "srh1_hm.py")).read()
_cut = _s.index("# ------------------------------------------------------------------ checkpointed run\n")
NS = {"__file__": os.path.join(SRH, "srh1_hm.py"), "__name__": "srh1_prefix"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_s[:_cut], NS["__file__"], "exec"), NS)
rfold_kpc = NS["rfold_kpc"]
Xsh = NS["Xsh"]
Mb_fold = NS["Mb_fold"]
L = NS["L"]
set_z = NS["set_z"]
ratios_S = NS["ratios_S"]
h = NS["h"]
KK = NS["KK"]
ZB = NS["ZB"]
FOOTS = NS["FOOTS"]
FB = NS["FB"]
VST = NS["VST"]
F1 = NS["F"]
m_nfw = lambda x: math.log1p(x) - x / (1.0 + x)
DC = float(L["DC"])
LMG = np.asarray(F1["LM"], float)
SG0 = np.asarray(F1["SIG0"], float) if "SIG0" in F1 else np.asarray(L["SIG"], float)
P(f"SRH1/FRZ1 halo-model prefix loaded.  h {h:.4f}  DC {DC}  n_z {len(ZB)}  footings {FOOTS}  {tm()}")

# ================================================================ CLASS (form B's own cosmology)
import classy
C_KMS = 299792.458
MPC_M = 3.0856775814913673e22
MSUN = 1.98892e30
G_SI = 6.674e-11
OB = float(L["om_b"])
OD = float(L["om_c"])
MC = classy.Class()
MC.set({"output": "mPk,mTk", "h": h, "omega_b": OB, "omega_cdm": OD, "A_s": 2.0e-9,
        "n_s": float(L["NS"]), "tau_reio": 0.06, "N_ur": 3.046, "T_cmb": 2.7255,
        "P_k_max_1/Mpc": 12.0, "z_max_pk": 1000.0})
MC.compute()
HC0 = MC.Hubble(0.0)
S80 = float(MC.sigma8())
A0M = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
P(f"CLASS: h {h:.4f}  Om_b h^2 {OB:.5f}  Om_c h^2 {OD:.5f}  sigma8(0) {S80:.4f}")

# ================================================================ PART 1a: the settled fraction, DERIVED
# Share fixed at formation (FRM1 / HIS1; rule 5, counted once): X = M_C/M_b = X_L(g_{b,f}).
# An element settles when the fold reaches it; the fold reach is FLD1's R_fold(z, M_b).
#   => settled region R_set = R_fold; settled fraction of the halo's cold charge =
#      the reference's own enclosed cold mass there over its value at the turnaround shell:
#        X_s(z, M_b) = m_nfw(R_fold/r_s) / m_nfw(r_ta/r_s).
# psi(z) = the mass-weighted mean of X_s over FRZ1's halo population at z.
ZPSI = [0.0, 0.16, 0.31, 0.43, 0.51, 0.71, 0.92, 1.5, 2.2, 3.0, 4.4, 6.0, 10.0]
UPSI = (math.log1p(ZPSI[0]), math.log1p(ZPSI[-1]))

def psi_at_z(foot, z):
    set_z(float(z))
    HB = L["HB"]
    W = np.asarray(L["W_M"], float)
    num = 0.0
    den = 0.0
    for i in range(len(HB)):
        hbb = HB[i]
        Mbb = Mb_fold(hbb, foot)
        lM = math.log10(Mbb / h)
        Rcom = rfold_kpc(foot, float(z), lM) * 1e-3 * (1.0 + float(z)) * h
        Rta = float(hbb["rta"])
        rs = float(hbb["rs"])
        if Rta <= 0 or rs <= 0:
            continue
        Xs = m_nfw(min(Rcom, Rta) / rs) / m_nfw(Rta / rs)
        if Xs > 1.0:
            Xs = 1.0
        wt = float(hbb["Mta"]) * float(W[i])
        num = num + Xs * wt
        den = den + wt
    return num / den if den > 0 else 0.0

sec("PART 1a: the settled fraction psi(z) = <X_s>, DERIVED (share fixed at formation; R_set = FLD1's R_fold)")
PSI = {}
for foot in FOOTS:
    vs = [psi_at_z(foot, z) for z in ZPSI]
    vs = np.array(vs)
    PSI[foot] = CubicSpline(np.log1p(np.array(ZPSI)), vs)
    P(f"[{foot}] psi at z = " + ", ".join(f"{zz:.2f}:{vv:.4f}" for zz, vv in zip(ZPSI, vs)) + f"  {tm()}")
P("     psi(a) is the ONLY place the epoch enters the linear system (a_0 does not run: flat branch, FRZ2).")

# ================================================================ PART 1b: the two-fluid ODE
def pklin(k_1Mpc, z):
    k = np.atleast_1d(np.asarray(k_1Mpc, float))
    return np.array([MC.pk_lin(float(kk), float(z)) for kk in k.ravel()]).reshape(k.shape)

KLIN = np.geomspace(1e-4, 10.0, 600)              # 1/Mpc for the sigma8 / Limber integrals
_LA = np.linspace(math.log(1.0 / 101.0), 0.0, 2401)
_lH = CubicSpline(_LA, np.log([MC.Hubble(1.0 / math.exp(x) - 1.0) for x in _LA]))
_dlH = _lH.derivative()
def bgat(lna):
    a = math.exp(lna)
    H = math.exp(float(_lH(lna)))
    dl = float(_dlH(lna))
    E2 = (H / HC0) ** 2
    return a, 1.0 / a - 1.0, H, dl, (OB / h ** 2) * a ** -3 / E2, (OD / h ** 2) * a ** -3 / E2

TH = MC.get_thermodynamics()
_tz = np.asarray(TH["z"])[::-1]
_cb2 = np.maximum(np.asarray(TH["c_b^2"])[::-1], 0.0)
KB, MPP, MU_I, T_I, G_I = 1.380649e-23, 1.67262192e-27, 0.59, 1.5e4, 1.5
C_IGM = G_I * KB * T_I / (MU_I * MPP) / (C_KMS * 1e3) ** 2
def cb2_of(z):
    zc = max(float(z), float(_tz[0]))
    return float(np.interp(zc, _tz, _cb2)) + (0.5 * (1 - math.tanh((zc - 8.0) / 0.5))) * C_IGM

KG = np.geomspace(1e-3, 1.0, 32)                 # h/Mpc
KPHY = KG * h                                   # 1/Mpc
NK = len(KG)
ZSTART = 100.0
ZOUT = (4.4, 3.0, 2.2, 0.919, 0.706, 0.510, 0.295, 0.0)

def integrate(foot, mode, psi_scale=1.0):
    asc = psi_scale
    def psi_of(a):
        if mode == "ref":
            return 0.0
        u = math.log1p(max(1.0 / a - 1.0, 0.0))
        u = min(max(u, UPSI[0]), UPSI[1])
        return asc * float(PSI[foot](u))
    def Mst_of(a):
        z = 1.0 / a - 1.0
        Dn = MC.scale_independent_growth_factor(z) / MC.scale_independent_growth_factor(0.0)
        tgt = DC / max(Dn, 1e-12)
        if SG0[0] < SG0[-1]:
            s = float(np.interp(tgt, SG0, LMG))
        else:
            s = float(np.interp(tgt, SG0[::-1], LMG[::-1]))
        return s
    def cq2_of(a):
        Mb = (10.0 ** Mst_of(a)) * MSUN       # Msun
        v2 = 0.5 * math.sqrt(max(G_SI * Mb * A0M[foot], 0.0))
        return psi_of(a) * v2 / (C_KMS * 1e3) ** 2
    def rhs(lna, y):
        a, z, H, dl, Ob, Oc = bgat(lna)
        db = y[0:NK]
        Db = y[NK:2 * NK]
        dc = y[2 * NK:3 * NK]
        Dc = y[3 * NK:4 * NK]
        kaH2 = (KPHY / (a * H)) ** 2
        p = psi_of(a)
        q2 = cq2_of(a)
        c2 = cb2_of(z)
        dDb = -(2 + dl) * Db + 1.5 * (Ob * db + Oc * dc) - kaH2 * c2 * db
        dDc = -(2 + dl) * Dc + 1.5 * (Ob * db + Oc * (1 - p) * dc) - kaH2 * q2 * dc
        return np.concatenate([Db, dDb, Dc, dDc])
    lna = np.sort(np.log(np.array([1.0 / (1.0 + zz) for zz in ZOUT], float)))
    so = solve_ivp(rhs, (math.log(1.0 / 101.0), float(lna[-1])), np.ones(4 * NK),
                   t_eval=lna, method="Radau", rtol=1e-9, atol=1e-13)
    assert so.success, so.message
    Y = so.y.reshape(4, NK, -1)
    Dm = ((OB / h ** 2) * Y[0] + (OD / h ** 2) * Y[2]) / ((OB + OD) / h ** 2)
    return dict(z=np.array(ZOUT, float), db=Y[0], dc=Y[2], Dm=Dm)

sec("PART 1b: two-fluid growth, ratio to the cold reference (k in h/Mpc)")
G = {}
for foot in FOOTS:
    for mode in ("ref", "formB"):
        G[(foot, mode)] = integrate(foot, mode)

RES = dict(lane="FINAL4", criteria="c5d897706f",
      note="kappa = 1/2 FITTED; not theory closed; adopts nothing",
      part1={}, part2={}, part3={}, part4={}, KA={}, MUTATE={})

def gv(arr, j, kq):
    return float(np.interp(kq, KG, arr[:, j]))

for foot in FOOTS:
    r = G[(foot, "ref")]
    m = G[(foot, "formB")]
    rows = []
    for j in range(len(ZOUT)):
        z = float(ZOUT[j])
        ps = float(PSI[foot](math.log1p(z)))
        rows.append((z, ps, gv(m["Dm"], j, 0.1) / gv(r["Dm"], j, 0.1),
                      gv(m["dc"], j, 0.1) / gv(r["dc"], j, 0.1),
                      gv(m["Dm"], j, 0.5) / gv(r["Dm"], j, 0.5)))
    RES["part1"][foot] = dict(
        z=[t[0] for t in rows],
        psi=[t[1] for t in rows],
        Dm_ratio_k0p1=[t[2] for t in rows],
        dc_ratio_k0p1=[t[3] for t in rows],
        Dm_ratio_k0p5=[t[4] for t in rows])
    P(f"[{foot}]      z     psi   D_m/D_ref(k.1)  d_c/D_ref(k.1)  D_m/D_ref(k.5)")
    for t in rows:
        P(f"        {t[0]:6.3f}  {t[1]:.4f}   {t[2]:.5f}          {t[3]:.5f}          {t[4]:.5f}")
P(f"  {tm()}")

json.dump(RES, open(os.path.join(HERE, "final4.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "final4.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
P(f"stage 1 written {tm()}")

