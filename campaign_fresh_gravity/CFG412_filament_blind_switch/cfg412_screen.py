#!/usr/bin/env python3
"""CFG412: screen V-web (a), non-local turnaround-cover (b) and other readers for a filament-blind switch.
FROZEN_CRITERIA.md (committed alone first).  Light CPU: one process, one FFT thread, nice 15; analyses the CFG410
BASE z0 snapshots only (no PM run).  CFG412_MUTATE=1 replaces every candidate reader by T1 alone (separate outputs).
Usage: nice -n 15 python3 cfg412_screen.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, math, time
import numpy as np
from scipy import fft as sfft
from scipy import ndimage
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg410_work"))
sys.path.insert(0, os.path.join(HERE, "..", "CFG100_kids_mass_rederivation"))
import cfg100_lib as C100                                    # read-only import: r_ta_law, dta, nu_mono, G_MPC

MUTATE = os.environ.get("CFG412_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
if __name__ == "__main__":
    try:
        os.nice(15)
    except OSError:
        pass

# ---------------------------------------------------------------- constants (copied from the CFG410 engine)
h = 0.6736; om_b, om_c = 0.02237, 0.1200
Om = (om_b + om_c) / h ** 2; OL = 1.0 - Om; FB = om_b / (om_b + om_c)
MPC = 3.0856775814913673e22
ACC_UNIT = 1e10 * h / MPC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
L = 200.0; M = 256; DX = L / M; EPS = 0.077
MIXA = (0.28, 0.54, 0.18)
X_CFG410 = {"canonical": 0.89, "alt": 0.86}                  # cfg410_results.json X (rounded there to 0.89 / 0.86)
DTA0 = json.load(open(os.path.join(WORK, "cfg361_delta_ta_table.json")))["D"][0]   # 11.8056 (z = 0)
TAU = (DTA0 - 1.0) / 3.0

LINES, OUT, CHECKS = [], {"mutate": MUTATE}, []
def P(s=""):
    print(s, flush=True); LINES.append(s)
def check(name, ok, meas=""):
    CHECKS.append((name, bool(ok))); P(f"  [{'PASS' if ok else 'FAIL'}] {name}  {meas}")

# ---------------------------------------------------------------- nu_mono (CFG410 engine copy)
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6):
    return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
from scipy.optimize import brentq
Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0); H_P = float(h_rar(Y_P))
LYG = np.linspace(-12, 12, 240001); YG = 10 ** LYG
DH_MONO = np.maximum(dh_rar(YG), 0.05 * H_P / (YG + Y_P))
H_MONO = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])
def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 + np.interp(np.log10(y), LYG, H_MONO) / y

# ---------------------------------------------------------------- mesh
k1 = (2 * np.pi * sfft.fftfreq(M, d=DX)).astype(np.float32); kz1 = (2 * np.pi * sfft.rfftfreq(M, d=DX)).astype(np.float32)
KX, KY, KZ = k1[:, None, None], k1[None, :, None], kz1[None, None, :]
K2 = KX ** 2 + KY ** 2 + KZ ** 2; K2[0, 0, 0] = 1.0; IK2 = (1.0 / K2).astype(np.float32); IK2[0, 0, 0] = 0.0; K2[0, 0, 0] = 0.0
KV = (KX, KY, KZ)
fwd = lambda x: sfft.rfftn(x, workers=1)
inv = lambda xk: sfft.irfftn(xk, s=(M, M, M), workers=1).astype(np.float32)

def deposit(pos):
    u = pos / DX; i0 = np.floor(u).astype(np.int64); w = (u - i0).astype(np.float32); i0 %= M; i1 = (i0 + 1) % M
    rho = np.zeros(M ** 3, np.float64)
    for cx in (0, 1):
        ix = i1[:, 0] if cx else i0[:, 0]; wx = w[:, 0] if cx else 1 - w[:, 0]
        for cy in (0, 1):
            iy = i1[:, 1] if cy else i0[:, 1]; wy = w[:, 1] if cy else 1 - w[:, 1]
            for cz in (0, 1):
                iz = i1[:, 2] if cz else i0[:, 2]; wz = w[:, 2] if cz else 1 - w[:, 2]
                rho += np.bincount((ix * M + iy) * M + iz, weights=wx * wy * wz, minlength=M ** 3)
    rho = rho.reshape((M,) * 3); return (rho / rho.mean() - 1.0).astype(np.float32)

def eig3(t):
    """CFG410 closed-form eigenvalues, l1 >= l2 >= l3, evaluated in slabs to bound memory."""
    out = [np.empty((M, M, M), np.float32) for _ in range(3)]
    for s in range(0, M, 32):
        a11, a22, a33, a12, a13, a23 = [x[s:s + 32].astype(np.float64) for x in t]
        p1 = a12 ** 2 + a13 ** 2 + a23 ** 2; q = (a11 + a22 + a33) / 3
        p2 = (a11 - q) ** 2 + (a22 - q) ** 2 + (a33 - q) ** 2 + 2 * p1; p = np.sqrt(p2 / 6); ps = np.where(p > 0, p, 1.0)
        b11, b22, b33 = (a11 - q) / ps, (a22 - q) / ps, (a33 - q) / ps; b12, b13, b23 = a12 / ps, a13 / ps, a23 / ps
        r = 0.5 * (b11 * (b22 * b33 - b23 ** 2) - b12 * (b12 * b33 - b23 * b13) + b13 * (b12 * b23 - b22 * b13))
        ph = np.arccos(np.clip(r, -1, 1)) / 3
        l1 = q + 2 * p * np.cos(ph); l3 = q + 2 * p * np.cos(ph + 2 * np.pi / 3); l2 = 3 * q - l1 - l3
        out[0][s:s + 32], out[1][s:s + 32], out[2][s:s + 32] = l1, l2, l3
    return out

def smear(x):
    return np.clip(0.5 + (x - TAU) / (2 * EPS), 0, 1).astype(np.float32)

# ---------------------------------------------------------------- B1: turnaround cover around density peaks
_GEOM = {}
def geom(hw):
    if hw not in _GEOM:
        g = np.arange(-hw, hw + 1); r2 = (g[:, None, None] ** 2 + g[None, :, None] ** 2 + g[None, None, :] ** 2).ravel()
        order = np.argsort(r2, kind="stable"); r2s = r2[order]
        last = np.r_[np.nonzero(np.diff(r2s))[0], len(r2s) - 1]          # last index of each distance group
        grp = np.repeat(np.arange(len(last)), np.diff(np.r_[-1, last]))   # group id per sorted cell
        _GEOM[hw] = (g, order, r2s, last, grp)
    return _GEOM[hw]

def turnaround_cover(delta, exclusive=False):
    """f_B1(x) = max over peaks c of F_c(|x - c|); F_c = smear((Dbar_c(<r) - 1)/3), first crossing from c outward
    (running minimum).  Peaks: 3x3x3 local maxima of delta that can be ON at r = 0.  exclusive=True (reported only):
    a peak already inside a denser peak's ON ball (f > 0.5) is skipped."""
    fB = np.zeros(M ** 3, np.float32)
    mx = ndimage.maximum_filter(delta, size=3, mode="wrap")
    pk = np.argwhere((delta == mx) & (delta >= 3 * (TAU - EPS)))
    pk = pk[np.argsort(-delta[pk[:, 0], pk[:, 1], pk[:, 2]])]
    rmax_cells, grown, skipped = [], 0, 0
    for c in pk:
        if exclusive and fB[(c[0] * M + c[1]) * M + c[2]] > 0.5:
            skipped += 1; continue
        hw = 3
        while True:
            g, order, r2s, last, grp = geom(hw)
            ix, iy, iz = (c[0] + g) % M, (c[1] + g) % M, (c[2] + g) % M
            idx = ((ix[:, None, None] * M + iy[None, :, None]) * M + iz[None, None, :]).ravel()
            ds = delta.ravel()[idx][order].astype(np.float64)
            cum = np.cumsum(ds)[last]; n = last + 1
            F = np.minimum.accumulate(smear(((1.0 + cum / n) - 1.0) / 3.0))
            inside = r2s[last] <= hw * hw                                  # groups fully inside the inscribed sphere
            if F[inside][-1] > 0 and hw < 40:
                hw *= 2; grown += 1; continue
            break
        Fc = F[grp]; ok = inside[grp] & (Fc > 0)
        sel = idx[order][ok]; fB[sel] = np.maximum(fB[sel], Fc[ok])
        on = inside & (F > 0.5)
        rmax_cells.append(float(math.sqrt(r2s[last][on][-1])) if on.any() else 0.0)
    return fB.reshape((M,) * 3), dict(n_peaks=int(len(pk)), n_skipped=skipped, n_grown=grown,
                                      rmax_cells_median=float(np.median(rmax_cells)) if rmax_cells else 0.0,
                                      rmax_cells_max=float(np.max(rmax_cells)) if rmax_cells else 0.0)

# ---------------------------------------------------------------- PM leg
def pm_leg(foot):
    t0 = time.time()
    snap = np.load(os.path.join(WORK, f"cfg410_RES_Rc3_MIXA_FLAT_{foot}_N256_z0.npz"))
    delta = deposit(snap["pos"].astype(np.float64)); f_st = snap["f"].astype(np.float32); l3_st = snap["l3"].astype(np.float32)
    rho = 1.0 + delta
    dk = fwd(delta)
    tk = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
    t = [inv(KV[i] * KV[j] * dk * IK2) for i, j in tk]
    l1, l2, l3 = eig3(t); del t
    fT1 = smear(l2)
    agree = float(np.mean((fT1 > 0.5) == (f_st > 0.5)))
    check(f"K1 {foot}: re-computed T1 ON agrees with stored f", agree >= 0.995, f"agreement {agree:.5f}; l3 sign agreement {np.mean((l3 < 0) == (l3_st < 0)):.5f}")
    fil = l3 < 0
    on_T1 = fT1 > 0.5
    mass_on = float((rho * on_T1).mean())
    fveto = fT1 * (~fil)
    drop = 1 - float((rho * (fveto > 0.5)).mean()) / mass_on
    check(f"K2 {foot}: l3-veto ON-mass drop reproduces CFG410's 64%", abs(drop - 0.64) <= 0.03, f"drop {drop:.3f}")
    # V-web from the LINEAR velocity v = -f H grad psi (code units f H = 1; sign: converging = positive eigenvalue of -dv)
    vel = [inv(-(1j * kv) * (-dk * IK2)) for kv in KV]                      # v_j = -d_j psi, psi_k = -delta_k / k^2
    sig = []
    for i, j in tk:
        sig.append(-inv(1j * KV[i] * fwd(vel[j])))                         # Sigma_ij = -d_i v_j  (converging > 0)
    del vel
    v1, v2, v3 = eig3(sig); del sig
    sc = max(float(np.abs(l1).max()), 1e-30)
    relerr = max(float(np.abs(v1 - l1).max()), float(np.abs(v2 - l2).max()), float(np.abs(v3 - l3).max())) / sc
    check(f"K3 {foot}: linear V-web eigenvalues = f H x Hessian eigenvalues", relerr < 1e-4, f"max rel diff {relerr:.2e}")
    fA1 = fT1 * (v3 > 0)                                                   # T1 AND all three V-web axes converging
    fA2 = smear(v2)                                                        # V-web middle eigenvalue at T1's threshold
    del v1, v2, v3
    # excess source (CFG410 RES pre-compensation): e = f max(s_ph - s_c, 0) at a = 1, MIX-A filter
    phik = (-1.5 * Om) * dk * IK2
    kJ = lambda T: math.sqrt(1.5 * Om) * 100.0 / (math.sqrt(5 * 1.380649e-23 * T / (3 * 0.6 * 1.67262192e-27)) / 1e3)
    Wk = (MIXA[0] / (1.0 + K2 / kJ(1e4) ** 2) + MIXA[1] / (1.0 + K2 / kJ(1e6) ** 2) + MIXA[2]).astype(np.float32)
    gb = [FB * (-inv(1j * kv * phik * Wk)) for kv in KV]; del Wk
    y = np.sqrt(gb[0] ** 2 + gb[1] ** 2 + gb[2] ** 2) / (A0[foot] / ACC_UNIT)
    w = (nu_mono(y) - 1.0).astype(np.float32); del y
    divk = sum(1j * kv * fwd(w * g) for kv, g in zip(KV, gb)); del gb, w
    s_ph = -inv(divk); del divk
    s_c = (1.5 * Om * (1.0 - FB)) * rho
    exc = np.maximum(s_ph - s_c, 0.0).astype(np.float32); del s_ph, s_c, dk
    # B1 turnaround cover
    fB1, binfo = turnaround_cover(delta)
    fB1x, binfo_x = turnaround_cover(delta, exclusive=True)
    cands = {"A1_T1_and_Vweb_allconv": fA1, "A2_Vweb_middle": fA2, "B1_cover": fB1, "B1T_T1_and_cover": np.minimum(fT1, fB1),
             "B1xT_T1_and_cover_exclusive(reported)": np.minimum(fT1, fB1x), "VETO_l3_(CFG410_reference)": fveto}
    if MUTATE:
        cands = {k: fT1 for k in cands}
    Mfil_T1 = float((rho * (on_T1 & fil)).mean()); Mknot_T1 = float((rho * (on_T1 & ~fil)).mean())
    Efil_T1 = float((fT1 * exc * fil).mean())
    res = dict(T1=dict(mass_on=mass_on, Mfil=Mfil_T1, Mknot=Mknot_T1, fil_share_of_on=Mfil_T1 / mass_on),
               veto_drop=drop, K1=agree, K3=relerr, B1=binfo, B1x=binfo_x, cands={})
    P(f"  {foot}: T1 ON mass {mass_on:.4f}; share in l3<0 {Mfil_T1 / mass_on:.3f}; B1 peaks {binfo['n_peaks']} "
      f"(median ON radius {binfo['rmax_cells_median'] * DX:.2f}, max {binfo['rmax_cells_max'] * DX:.2f} Mpc/h); exclusive skipped {binfo_x['n_skipped']}")
    for name, fc in cands.items():
        on = fc > 0.5
        Rfil = 1 - float((rho * (on & fil)).mean()) / Mfil_T1
        keep_knot = float((rho * (on & ~fil)).mean()) / Mknot_T1
        Efil = float((fc * exc * fil).mean())
        Xhat = X_CFG410[foot] * (1 - Efil / Efil_T1)
        extra_on = float((rho * (on & ~on_T1)).mean()) / mass_on
        res["cands"][name] = dict(R_fil=Rfil, knot_keep=keep_knot, Xhat=Xhat, new_on_outside_T1=extra_on)
        P(f"    {name:40s} R_fil {Rfil:6.3f} | knot ON mass kept {keep_knot:6.3f} | Xhat {Xhat:6.3f} | ON outside T1 {extra_on:6.3f} (of T1 ON)")
    P(f"  ({time.time() - t0:.0f} s)")
    return res

# ---------------------------------------------------------------- spherical host (cfg100_lib r_ta_law)
def sphere_leg():
    P("\n(2) spherical hosts (cfg100_lib r_ta_law), edge = r(f > 0.5 continuously from the centre) / r_ta")
    rows = []
    rho_m = C100.OM * C100.RHOC0
    for foot in ("canonical", "alt"):
        a0 = C100.A0[foot]
        for lm in (10.5, 11.0, 11.5):
            Mb = 10 ** lm
            for lab, D in (("cfg100 11.765", C100.dta(0.0)), ("CFG361 11.806", DTA0)):
                tau = (D - 1) / 3
                rta = math.exp(brentq(lambda lr: math.log(Mb * float(C100.nu_mono(C100.G_MPC * Mb / math.exp(2 * lr) / a0)))
                             - math.log(4 * math.pi / 3 * math.exp(3 * lr) * rho_m * D), math.log(1e-5), math.log(1e3), xtol=1e-12))
                if abs(D - C100.dta(0.0)) < 1e-12:
                    assert abs(rta / C100.r_ta_law(Mb, a0, 0.0) - 1) < 1e-6        # same solver as cfg100_lib r_ta_law
                r = np.linspace(1e-3, 1.5, 15001) * rta
                Meff = Mb * C100.nu_mono(C100.G_MPC * Mb / r ** 2 / a0)
                Dbar = 3 * Meff / (4 * math.pi * r ** 3 * rho_m)
                lt = (Dbar - 1) / 3                                       # tangential eigenvalue = l2 on the sphere
                fT1 = np.clip(0.5 + (lt - tau) / (2 * EPS), 0, 1)
                Fc = np.minimum.accumulate(fT1)                           # B1 around the centre peak: first crossing
                def edge(f):
                    off = np.nonzero(f <= 0.5)[0]
                    return float(r[off[0]] / rta) if off.size else float(r[-1] / rta)
                e = dict(T1=edge(fT1), B1=edge(Fc), B1T=edge(np.minimum(fT1, Fc)))
                rows.append(dict(foot=foot, logMb=lm, Delta=lab, rta_Mpc=rta, **e))
                P(f"  {foot:9s} log M_b {lm}  Delta_ta {lab}: r_ta {rta:.3f} Mpc | edges T1 {e['T1']:.4f}  B1 {e['B1']:.4f}  B1T {e['B1T']:.4f}")
    # K4: B1 painted on a mesh around an isolated analytic sphere (point mass in a uniform background)
    n = 96; c = n // 2; g = np.arange(n) - c
    rr = np.sqrt(g[:, None, None] ** 2 + g[None, :, None] ** 2 + g[None, None, :] ** 2).astype(np.float64)
    dlt = np.zeros((n, n, n)); Mpt = 1.0 + (DTA0 - 1.0) * (4 / 3) * math.pi * 20.0 ** 3   # r_ta = 20 cells by construction
    dlt[c, c, c] = Mpt - 1.0                                                       # point mass + background in cell units
    order = np.argsort(rr.ravel(), kind="stable"); r_s = rr.ravel()[order]
    cum = 1.0 + np.cumsum(dlt.ravel()[order]) / np.arange(1, n ** 3 + 1)
    last = np.r_[np.nonzero(np.diff(r_s))[0], len(r_s) - 1]
    F = np.minimum.accumulate(smear((cum[last] - 1) / 3)); rg = r_s[last]
    e_mesh = float(rg[F > 0.5][-1])
    check("K4 B1 on an isolated mesh sphere ends at r_ta = 20 cells (one grid step)", abs(e_mesh - 20.0) <= 1.0, f"edge {e_mesh:.3f} cells")
    return rows

# ---------------------------------------------------------------- V-web on a nonlinear secondary-infall host
def infall_leg():
    P("\n(2a) nonlinear V-web in a secondary-infall host (record's Lambda shell ODE, seed + background, z = 0)")
    ai = 1e-3; Hi = math.sqrt(Om / ai ** 3 + OL)
    def shell(di):
        Ri = ai * (1 - di / 3.0); GM = 0.5 * Om * (1 + di) * Ri ** 3 / ai ** 3
        rhs = lambda t, y: [y[0] * math.sqrt(Om / y[0] ** 3 + OL), y[2], -GM / y[1] ** 2 + OL * y[1]]
        hit = lambda t, y: y[0] - 1.0; hit.terminal = True
        crash = lambda t, y: y[1] - 1e-4 * Ri / ai; crash.terminal = True
        s = solve_ivp(rhs, [0, 50], [ai, Ri, Hi * Ri * (1 - di / 3.0)], events=[hit, crash], rtol=1e-10, atol=1e-13)
        if s.t_events[0].size:
            a, R, V = s.y_events[0][0]
            return R, V, (1 + di) * (Ri / ai) ** 3 / R ** 3
        return None
    out = {}
    for eps_prof in (1.0, 2.0 / 3.0):                       # dbar_i ∝ x^(-3 eps): 1 = point seed; 2/3 = shallower
        # find the shell turning around now, then scan inner shells
        lo, hi = 1e-4, 0.05
        for _ in range(70):
            mid = math.sqrt(lo * hi); r = shell(mid)
            if r is None or r[1] < 0: hi = mid
            else: lo = mid
        dta_now = shell(lo)[2]
        check(f"K5 infall solver eps {eps_prof:.2f}: turnaround shell density = Delta_ta (1%)", abs(dta_now / DTA0 - 1) < 0.01, f"{dta_now:.4f} vs {DTA0:.4f}")
        x_ta = 1.0
        xs = np.linspace(0.30, 1.0, 400)                   # shells inside the turnaround shell (comoving label / x_ta)
        R, V = [], []
        for x in xs:
            r = shell(lo * x ** (-3 * eps_prof))
            R.append(np.nan if r is None else x * r[0]); V.append(np.nan if r is None else x * r[1])   # R, V scale with the label
        R, V = np.array(R), np.array(V); ok = np.isfinite(R)
        Rta = shell(lo)[0]; Rn = R / Rta
        # single-stream region: R monotone in the label, outside the record's outer caustic (>= 0.37 r_ta)
        mono = np.r_[False, np.diff(R) > 0] & ok
        reg = mono & (Rn >= 0.37) & (Rn < 0.999)
        dVdR = np.gradient(V, R); VR = V / R                  # total (proper) velocity; H(a = 1) = 1 in these units
        pr, pt = dVdR - 1.0, VR - 1.0                           # peculiar shear (Hubble flow subtracted), as the PM leg's V-web
        stretch = float(np.mean(dVdR[reg] > 0)); conv_t = float(np.mean(VR[reg] < 0))
        pstretch = float(np.mean(pr[reg] > 0)); pconv_t = float(np.mean(pt[reg] < 0))
        allconv = (pr < 0) & (pt < 0)                           # A1's V-web condition (peculiar, all three axes converging)
        # A1 edge: outermost radius such that all single-stream shells inside it (>= 0.37 r_ta) satisfy the condition
        ordr = np.argsort(Rn[reg]); Rr = Rn[reg][ordr]; ac = allconv[reg][ordr]
        bad = np.nonzero(~ac)[0]
        a1edge = float(Rr[bad[0]]) if bad.size else 1.0
        P(f"  eps {eps_prof:.2f}: single-stream infall region {Rn[reg].min():.3f}-{Rn[reg].max():.3f} r_ta ({reg.sum()} shells)")
        P(f"    proper flow: radial dv/dr > 0 (stretching) in {stretch:.3f}; tangential v/r < 0 (converging) in {conv_t:.3f}")
        P(f"    peculiar flow: radial dv/dr - H > 0 (stretching) in {pstretch:.3f}; tangential converging in {pconv_t:.3f}; "
          f"radial (dv/dr - H)/H range {pr[reg].min():.2f} to {pr[reg].max():.2f}")
        P(f"    -> A1 (all peculiar V-web axes converging) holds continuously from the caustic out to {a1edge:.3f} r_ta (1.000 = to r_ta)")
        out[f"eps{eps_prof:.2f}"] = dict(region=[float(Rn[reg].min()), float(Rn[reg].max())], frac_radial_stretch_proper=stretch,
                                          frac_tangential_conv=conv_t, frac_radial_stretch_peculiar=pstretch,
                                          peculiar_radial_range=[float(pr[reg].min()), float(pr[reg].max())], A1_edge_upper=a1edge)
    return out

# ---------------------------------------------------------------- main
if __name__ == "__main__":
    P(f"CFG412 screen  (MUTATE={MUTATE}); Delta_ta(z=0) {DTA0:.4f}, tau {TAU:.4f}, eps {EPS}; FFT workers 1")
    P("Velocities: NOT stored in the CFG410 snapshots -> PM leg uses the LINEAR-THEORY velocity from the z0 potential (declared).")
    P("\n(1) PM diagnostic on CFG410 BASE z0 snapshots (ESTIMATE; no PM re-run)")
    OUT["pm"] = {foot: pm_leg(foot) for foot in ("canonical", "alt")}
    OUT["sphere"] = sphere_leg()
    OUT["infall"] = infall_leg()

    # ---------------------------------------------------------------- verdicts
    P("\nVerdicts (worse footing; legality per README / FROZEN_CRITERIA)")
    LEGAL = {"A1_T1_and_Vweb_allconv": ("LEGAL", 1), "A2_Vweb_middle": ("LEGAL", 1), "B1_cover": ("CONDITIONAL", 1),
             "B1T_T1_and_cover": ("CONDITIONAL", 1)}
    sph_edge = {"A1_T1_and_Vweb_allconv": min(v["A1_edge_upper"] for v in OUT["infall"].values()),
                "A2_Vweb_middle": min(r["T1"] for r in OUT["sphere"]),         # linear V-web = T1 on spheres
                "B1_cover": min(r["B1"] for r in OUT["sphere"]), "B1T_T1_and_cover": min(r["B1T"] for r in OUT["sphere"])}
    VER = {}
    for c, (leg, ncon) in LEGAL.items():
        R = min(OUT["pm"][f]["cands"][c]["R_fil"] for f in ("canonical", "alt"))
        p1, p2 = R >= 0.60, sph_edge[c] >= 0.90
        if p1 and p2 and leg == "LEGAL" and ncon <= 1: v = "PROMISING"
        elif (p1 or p2) and ncon <= 1: v = "PARTIAL"
        else: v = "NO-GO"
        VER[c] = dict(R_fil_min=R, sphere_edge_min=sph_edge[c], legality=leg, constants=ncon, verdict=v)
        P(f"  {c:28s} R_fil(min) {R:6.3f} [{'pass' if p1 else 'fail'}] | sphere edge(min) {sph_edge[c]:.3f} r_ta [{'pass' if p2 else 'fail'}] | {leg}, {ncon} const -> {v}")
    OUT["verdicts"] = VER
    if MUTATE:
        mx = max(abs(OUT["pm"][f]["cands"][c]["R_fil"]) for f in ("canonical", "alt") for c in OUT["pm"][f]["cands"])
        P(f"\nMUTATE: every reader replaced by T1 alone -> max |R_fil| = {mx:.2e}")
        det = mx < 0.01
        P(f"MUTATE {'DETECTED' if det else 'NOT DETECTED'} (expected |R_fil| < 0.01)")
        OUT["mutate_max_abs_Rfil"] = mx
    nfail = sum(1 for _, ok in CHECKS if not ok)
    P(f"\nchecks: {len(CHECKS) - nfail}/{len(CHECKS)} pass")
    OUT["checks"] = CHECKS
    json.dump(OUT, open(os.path.join(HERE, f"cfg412_screen_results{SUF}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"cfg412_screen{SUF}.out"), "w").write("\n".join(LINES) + "\n")
    sys.exit((1 if det else 0) if MUTATE else (1 if nfail else 0))
