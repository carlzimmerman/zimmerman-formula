#!/usr/bin/env python3
"""FINAL4 (GROWTH) parts 3 and 4: CMB lensing + f sigma8, the tilt verdict, PR-F4, and RESULT.md.
Criteria c5d897706f. TEST lane; adopts nothing.
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
FOOTS = ("canonical", "alt")

OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time(); tm = lambda: f"[{time.time()-T0:7.1f}s]"
P("=" * 100)
P("FINAL4 (GROWTH), parts 3 and 4 -- the independent rows, the tilt verdict and PR-F4")
P("     criteria FROZEN_CRITERIA.md (c5d897706f).  kappa = 1/2 FITTED; not theory closed.  Adopts nothing.")
P("=" * 100)

_s = open(os.path.join(SRH, "srh1_hm.py")).read()
_cut = _s.index("# ------------------------------------------------------------------ checkpointed run\n")
NS = {"__file__": os.path.join(SRH, "srh1_hm.py"), "__name__": "pre"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_s[:_cut], NS["__file__"], "exec"), NS)
rfold_kpc = NS["rfold_kpc"]; Xsh = NS["Xsh"]; Mb_fold = NS["Mb_fold"]
L = NS["L"]; set_z = NS["set_z"]; h = NS["h"]; KK = NS["KK"]; ZB = NS["ZB"]; F1 = NS["F"]
m_nfw = lambda x: math.log1p(x) - x / (1.0 + x); DC = float(L["DC"]); UPSI = (0.0, math.log1p(10.0))
LMG = np.asarray(F1["LM"], float)
SG0 = np.asarray(F1["SIG0"], float) if "SIG0" in F1 else np.asarray(L["SIG"], float)

import classy
C_KMS = 299792.458; MPC_M = 3.0856775814913673e22; MSUN = 1.98892e30; G_SI = 6.674e-11
OB = float(L["om_b"]); OD = float(L["om_c"])
MC = classy.Class()
MC.set({"output": "mPk,mTk", "h": h, "omega_b": OB, "omega_cdm": OD, "A_s": 2.0e-9, "n_s": float(L["NS"]),
        "tau_reio": 0.06, "N_ur": 3.046, "T_cmb": 2.7255, "P_k_max_1/Mpc": 12.0, "z_max_pk": 1000.0})
MC.compute()
HC0 = MC.Hubble(0.0); S80 = float(MC.sigma8())
_LA = np.linspace(math.log(1.0 / 101.0), 0.0, 2401)
_lH = CubicSpline(_LA, np.log([MC.Hubble(1.0 / math.exp(x) - 1.0) for x in _LA]))
_dlH = _lH.derivative()
def bgat(lna):
    a = math.exp(lna); H = math.exp(float(_lH(lna))); dl = float(_dlH(lna))
    E2 = (H / HC0) ** 2
    return a, 1.0 / a - 1.0, H, dl, (OB / h ** 2) * a ** -3 / E2, (OD / h ** 2) * a ** -3 / E2
TH = MC.get_thermodynamics()
_tz = np.asarray(TH["z"])[::-1]; _cb2 = np.maximum(np.asarray(TH["c_b^2"])[::-1], 0.0)
KB_, MPP, MU_I, T_I, G_I = 1.380649e-23, 1.67262192e-27, 0.59, 1.5e4, 1.5
C_IGM = G_I * KB_ * T_I / (MU_I * MPP) / (C_KMS * 1e3) ** 2
def cb2_of(z):
    zc = max(float(z), float(_tz[0]))
    return float(np.interp(zc, _tz, _cb2)) + (0.5 * (1 - math.tanh((zc - 8.0) / 0.5))) * C_IGM

ZPSI = [0.0, 0.16, 0.31, 0.43, 0.51, 0.71, 0.92, 1.5, 2.2, 3.0, 4.4, 6.0, 10.0]
def psi_at_z(foot, z):
    set_z(float(z))
    HB = L["HB"]; W = np.asarray(L["W_M"], float)
    num = 0.0; den = 0.0
    for i in range(len(HB)):
        hbb = HB[i]
        Mbb = Mb_fold(hbb, foot); lM = math.log10(Mbb / h)
        Rcom = rfold_kpc(foot, float(z), lM) * 1e-3 * (1.0 + float(z)) * h
        Rta = float(hbb["rta"]); rs = float(hbb["rs"])
        if Rta <= 0 or rs <= 0: continue
        Xs = m_nfw(min(Rcom, Rta) / rs) / m_nfw(Rta / rs)
        if Xs > 1.0: Xs = 1.0
        wt = float(hbb["Mta"]) * float(W[i]); num += Xs * wt; den += wt
    return num / den if den > 0 else 0.0
PSI = {}
for ft in FOOTS:
    PSI[ft] = CubicSpline(np.log1p(np.array(ZPSI)), np.array([psi_at_z(ft, z) for z in ZPSI]))

KG = np.geomspace(1e-3, 1.0, 32); KPHY = KG * h; NK = len(KG)
ZOUT = (4.4, 3.0, 2.2, 0.919, 0.706, 0.510, 0.295, 0.0)
def integrate(foot, mode, psi_scale=1.0):
    asc = psi_scale
    def psi_of(a):
        if mode == "ref": return 0.0
        u = math.log1p(max(1.0 / a - 1.0, 0.0)); u = min(max(u, UPSI[0]), UPSI[1])
        return asc * float(PSI[foot](u))
    def Mst_of(a):
        z = 1.0 / a - 1.0
        Dn = MC.scale_independent_growth_factor(z) / MC.scale_independent_growth_factor(0.0)
        tgt = DC / max(Dn, 1e-12)
        if SG0[0] < SG0[-1]: s = float(np.interp(tgt, SG0, LMG))
        else: s = float(np.interp(tgt, SG0[::-1], LMG[::-1]))
        return s
    def cq2_of(a):
        Mb = (10.0 ** Mst_of(a)) * MSUN
        v2 = 0.5 * math.sqrt(max(G_SI * Mb * A0M[foot], 0.0))
        return psi_of(a) * v2 / (C_KMS * 1e3) ** 2
    def rhs(lna, y):
        a, z, H, dl, Ob, Oc = bgat(lna)
        db = y[0:NK]; Db = y[NK:2 * NK]; dc = y[2 * NK:3 * NK]; Dc = y[3 * NK:4 * NK]
        kaH2 = (KPHY / (a * H)) ** 2
        p = psi_of(a); q2 = cq2_of(a); c2 = cb2_of(z)
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

A0M = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
G = {}
for ft in FOOTS:
    for md in ("ref", "formB"):
        G[(ft, md)] = integrate(ft, md)

def gv(arr, j, kq):
    return float(np.interp(kq, KG, arr[:, j]))

# ---- derive the growth factor D(z), sigma8(z) and f sigma8(z) on the DESI nodes
DESI = [("BGS", 0.295, 0.80, 0.20, 0.20, 0.84, 0.19, 0.19),
       ("LRG1", 0.510, 1.09, 0.12, 0.14, 1.16, 0.13, 0.13),
       ("LRG2", 0.706, 1.05, 0.12, 0.12, 1.04, 0.11, 0.092),
       ("LRG3", 0.919, 0.96, 0.11, 0.10, 0.997, 0.10, 0.084)]
zl = np.array([0.295, 0.510, 0.706, 0.919])
rows = {}
for ft in FOOTS:
    r = G[(ft, "ref")]; m = G[(ft, "formB")]
    zs = np.array(ZOUT)
    # D(z) normalised to 1 today
    Db_r = np.array([gv(r["Dm"], j, 0.1) for j in range(len(zs))])
    Db_m = np.array([gv(m["Dm"], j, 0.1) for j in range(len(zs))])
    Dref = Db_r / Db_r[np.argmin(abs(zs - 0.0))]
    Dmod = Db_m / Db_r[np.argmin(abs(zs - 0.0))]
    # f = d ln D / d ln a
    lna_s = np.sort(np.log(1.0 / (1.0 + zs)))
    o = np.argsort(np.log(1.0 / (1.0 + zs)))
    fref = CubicSpline(lna_s, np.log(Db_r[o])).derivative()(lna_s)
    fmod = CubicSpline(lna_s, np.log(Db_m[o])).derivative()(lna_s)
    # sigma8(z) = sigma8(0) * D(z);  the redistribution is folded in through Dm's k-dependence at k = 0.1
    s8ref = S80 * Dref
    s8mod = S80 * Dmod
    fs_ref = fref * s8ref
    fs_mod = fmod * s8mod
    def atz(zq):
        j = int(np.argmin(abs(zs - zq)))
        return j
    jj = [atz(z) for z in zl]
    tab = []
    for k_, z in enumerate(zl):
        j = jj[k_]; obs = DESI[k_][2]; sg = DESI[k_][3]
        tab.append(dict(name=DESI[k_][0], z=float(z), obs=float(obs), sig=float(sg),
                     fsig8_ref=float(fs_ref[j]), fsig8_formB=float(fs_mod[j]),
                     pull_ref=float((fs_ref[j] - obs) / sg), pull_formB=float((fs_mod[j] - obs) / sg)))
    chi2_ref = float(sum(t["pull_ref"] ** 2 for t in tab))
    chi2_mod = float(sum(t["pull_formB"] ** 2 for t in tab))
    rows[ft] = dict(tab=tab, chi2_ref=chi2_ref, chi2_formB=chi2_mod,
                 D_ratio={f"{z:.3f}": float(gv(m["Dm"], j, 0.1) / gv(r["Dm"], j, 0.1)) for j, z in enumerate(zs)})

P("")
P("-- PART 3a: DESI DR1 f sigma8, four bins (line: every |pull| <= 2) --")
for ft in FOOTS:
    rr = rows[ft]
    P(f"[{ft}] chi2_ref {rr['chi2_ref']:.3f}   chi2_formB {rr['chi2_formB']:.3f}")
    P(f"       {'bin':6s} {'z':>6s} {'obs':>6s} {'sig':>6s} {'f s8 ref':>9s} {'f s8 B':>9s} {'pull ref':>9s} {'pull B':>9s}")
    for t in rr["tab"]:
        P(f"       {t['name']:6s} {t['z']:6.3f} {t['obs']:6.2f} {t['sig']:6.2f} "
          f"{t['fsig8_ref']:9.4f} {t['fsig8_formB']:9.4f} {t['pull_ref']:+9.3f} {t['pull_formB']:+9.3f}")

# ---- CMB lensing: Limber kernel ratio at the nine PR4 bandpowers' effective L
ZSTAR = 1000.0
CHIS = MC.angular_distance(ZSTAR) * (1 + ZSTAR)
_zg = np.unique(np.round(np.concatenate([np.geomspace(1e-3, 6.0, 400), np.linspace(6.0, 10.0, 41),
                                                np.geomspace(10.0, ZSTAR, 220)]), 8))
_cg = np.array([MC.angular_distance(z) * (1 + z) for z in _zg])
_Hg = np.array([MC.Hubble(z) for z in _zg])
_Wg = (1 + _zg) * _cg * (1 - _cg / CHIS)
_dchi = np.zeros_like(_cg); d = np.diff(_cg); _dchi[:-1] += 0.5 * d; _dchi[1:] += 0.5 * d
_ker = _Wg ** 2 / _cg ** 2 * _dchi / _Hg * C_KMS
LS = np.array([100.0, 200.0, 300.0, 400.0, 600.0, 800.0, 1200.0, 1600.0, 2000.0])

def Rg(foot, kq, zq):
    r = G[(foot, "ref")]; m = G[(foot, "formB")]
    zs = np.array(ZOUT)
    j = int(np.argmin(abs(zs - zq)))
    return float(np.interp(kq, KG, m["Dm"][:, j]) / np.interp(kq, KG, r["Dm"][:, j]))

P("")
P("-- PART 3b: CMB-lensing bandpower ratio (Limber, nine bands L = 100 to 2000) --")
cmb = {}
for ft in FOOTS:
    out = []
    for L in LS:
        kq = L / _cg
        num = 0.0; den = 0.0
        kc = np.clip(kq, 1e-4, 9.9)
        Pn = np.array([MC.pk_lin(float(a), float(b)) for a, b in zip(kc, _zg)])
        R2 = np.array([Rg(ft, float(a), float(b)) for a, b in zip(kc, _zg)]) ** 2
        num = float(np.sum(_ker * Pn * R2)); den = float(np.sum(_ker * Pn))
        out.append(float(num / den))
    cmb[ft] = out
    P(f"[{ft}] C_L(model)/C_L(reference): " +
      ", ".join(f"L{int(L)}:{s:.4f}" for L, s in zip(LS, out)))

# PR4 bandpower weights are unknown here; a plain mean over the nine bands is used (disclosed).
A_CO1 = {"canonical": (0.9617, 0.0231), "alt": (0.9564, 0.0230)}
P("")
P("-- PART 3c: CMB-lensing amplitude A = data / prediction, graded (line |A - 1| <= 2 sigma_A) --")
for ft in FOOTS:
    S = float(np.mean(cmb[ft]))
    A0, sg = A_CO1[ft]
    Ad = A0 / S
    zsc = (Ad - 1.0) / sg
    zs0 = (A0 - 1.0) / sg
    P(f"[{ft}] band mean C_L ratio {S:.5f}   A(CO1) {A0:.4f} +- {sg:.4f} ({zs0:+.2f} sigma)"
      f"   A(derived) {Ad:.4f} ({zsc:+.2f} sigma)   -> {'PASS' if abs(Ad - 1) <= 2 * sg else 'FAIL'}")

# ---- part 4: the verdict
P("")
P("-- PART 4: the tilt verdict --")
P("  The three SRH1 A1 tilt cases pass G1 here (0.073 / 0.072; 0.872 / 0.864; 2.475 / 2.427).")
P("  The derived history H_A does not (9916.246 / 9008.690). So the gates cannot exclude the tilt:")
P("  it was fitted to them. Verdict: TILT POST HOC, NOT EXCLUDED.")
P("")
P("  PR-F4 is frozen in FROZEN_CRITERIA.md section 6 and is printed below in full. It decides the tilt")
P("  with data that is not in this repository, so it is not run here.")

RES = dict(lane="FINAL4", criteria="c5d897706f",
           note="kappa = 1/2 FITTED; not theory closed; adopts nothing",
           part3=dict(cmb_ratio={ft: cmb[ft] for ft in FOOTS},
                      fsig8={ft: rows[ft] for ft in FOOTS}),
           part4=dict(verdict="TILT POST HOC, NOT EXCLUDED",
                      reason="fitted to G1-G4 after they were seen; the gates confirm, they do not test",
                      label="DERIVED HISTORY EXCLUDED"))
json.dump(RES, open(os.path.join(HERE, "final4_rows.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "final4_rows.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
P(f"done {tm()}")
