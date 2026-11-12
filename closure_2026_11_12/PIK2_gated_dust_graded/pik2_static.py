#!/usr/bin/env python3
"""PIK2 rows 3-8 (criteria 95edd35e0b): the gated static dust M_K(r) = (mu^2/G) Int S(u) |Phi| r^2 dr, u = rho_halo / (xi rho_d0),
rho_halo = the dust-free law phantom of the baryons, on X-COP (row 3), Lovisari groups (row 4), point galaxies on the capped
law potential (rows 5, 6: proxy inequality against MK1's ungated bounds), the Sun (row 7); row 8a law back-reaction and
row 8b static-background health at every graded radius; K-SC self-consistent phantom for any rows 3-7 pass; label inputs.
Builders copied in content into ./copied/ (QX2 qx2.py X-COP builder + psi_profile; QX5 groups(); MK1 mk1_lib.py capped and
uncapped profiles) from commit 7172d3dd4f, executed here read-only; data read in place under real_research/data.
  python3 pik2_static.py            -> pik2_static.json / .out
  python3 pik2_static.py --mutate   -> pik2_static_MUTATE.json / .out   (M-S1, M-SIGN, M-PIB, M-NOCAP)
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "copied"))
import pik2_common as CM
import mk1_lib as LB
MUT = "--mutate" in sys.argv
TAG = "pik2_static_MUTATE" if MUT else "pik2_static"
OUT = []; T0 = time.time()
def P(s=""): print(s, flush=True); OUT.append(str(s))
G, MS, KPC, MPC = CM.G, CM.MS, CM.KPC, CM.MPC
REPO = CM.REPO

# ------------------------------------------------------------------ builders (copied in content; executed read-only)
q2src = open(os.path.join(HERE, "copied", "qx2.py")).read()
pre = q2src[:q2src.index("# ---------- iter 1: plain law ----------")]
Q2 = dict(__file__=os.path.join(REPO, "closure_2026_11_06", "QX2_clusters", "qx2.py"), __name__="qx2_prefix"); _argv = sys.argv; sys.argv = [sys.argv[0]]
exec(compile(pre, "copied/qx2.py", "exec"), Q2); sys.argv = _argv
exec(compile(q2src[q2src.index("def psi_profile(c):"):q2src.index("for c in XC:\n    rr, psi = psi_profile(c)")], "copied/qx2.py:psi_profile", "exec"), Q2)
XC = Q2["XC"]
q5src = open(os.path.join(HERE, "copied", "qx5.py")).read()
Q5 = dict(os=os, np=np, math=math, DATA=os.path.join(REPO, "real_research", "data"))
exec(compile(q5src[q5src.index("def groups():"):q5src.index("XC, SP, EL, LE, GR = ")], "copied/qx5.py:groups", "exec"), Q5)
GR = Q5["groups"]()


def glaw(gN, a0): return 0.5 * gN + np.sqrt(0.25 * gN ** 2 + a0 * gN)
def lawM(Mb, r_m, a0):   # Mb [kg] array, r [m] -> M_L [kg]
    Mb = np.asarray(Mb, float); gN = G * np.abs(Mb) / r_m ** 2; return np.sign(Mb) * glaw(gN, a0) * r_m ** 2 / G
def cumtrapz0(y, x): return np.concatenate([[0.0], np.cumsum(0.5 * (y[1:] + y[:-1]) * np.diff(x))])
def dens(M, r_m): return np.gradient(M, r_m) / (4 * math.pi * r_m ** 2)


# ------------------------------------------------------------------ X-COP set-up
for c in XC:
    rr, psi = Q2["psi_profile"](c); rows = c["rows"]
    rx = np.array([z["r_kpc"] for z in rows]); mb = np.array([z["M_b"] for z in rows])
    lr, lm = np.log(rx), np.log(mb)
    s_in = (lm[1] - lm[0]) / (lr[1] - lr[0]); s_out = (lm[-1] - lm[-2]) / (lr[-1] - lr[-2])
    L = np.log(rr); lMb = np.where(L < lr[0], lm[0] + s_in * (L - lr[0]), np.where(L > lr[-1], lm[-1] + s_out * (L - lr[-1]), np.interp(L, lr, lm)))
    c["_rr"] = rr; c["_rm"] = rr * KPC; c["_psi"] = psi; c["_Mb"] = np.exp(lMb) * MS
    c["_w"] = np.abs(psi) * c["_rm"] ** 2; c["_gN"] = np.gradient(-psi, c["_rm"])   # |Phi| r^2 ; dPhi/dr
    c["_rhob"] = dens(c["_Mb"], c["_rm"])
    c["_ix"] = [int(np.argmin(np.abs(rr - z["r_kpc"]))) for z in rows]
    for f in CM.FOOT:
        c[f"_ph_{f}"] = dens(lawM(c["_Mb"], c["_rm"], CM.A0[f]) - c["_Mb"], c["_rm"])
# groups set-up (MK1's power-law HSE potential, zero at 3 x 1.5 R500)
for gp in GR:
    sl = math.log(gp["M5"] / gp["M25"]) / math.log(gp["R5"] / gp["R25"]); rz = 3 * 1.5 * gp["R5"]
    rr = np.geomspace(1e-3 * gp["R25"], rz, 4000); Mr = gp["M25"] * (rr / gp["R25"]) ** sl
    gacc = G * Mr * MS / (rr * KPC) ** 2; seg = 0.5 * (gacc[1:] + gacc[:-1]) * np.diff(rr * KPC)
    psi = -np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    sg = math.log(gp["g5"] / gp["pts"][0]["M_gas"]) / math.log(gp["R5"] / gp["R25"])
    gp["_rr"] = rr; gp["_rm"] = rr * KPC; gp["_psi"] = psi; gp["_w"] = np.abs(psi) * (rr * KPC) ** 2; gp["_gN"] = gacc
    gp["_Mgas"] = gp["pts"][0]["M_gas"] * (rr / gp["R25"]) ** sg * MS
    gp["_ix"] = [int(np.argmin(np.abs(rr - p["r_kpc"]))) for p in gp["pts"]]
    for f in CM.FOOT:
        for s in (0.0, 1.0):
            Mb = gp["_Mgas"] * (1 + s); gp[f"_ph_{f}_{s}"] = dens(lawM(Mb, gp["_rm"], CM.A0[f]) - Mb, gp["_rm"])
            gp[f"_rhob_{s}"] = dens(Mb, gp["_rm"])


# ------------------------------------------------------------------ galaxies (point baryon mass on the capped law potential; MK1 lib)
def galaxy(Mb_msun, f, capped=True):
    a0 = CM.A0[f]; M = Mb_msun * MS; rM = math.sqrt(G * M / a0); s = math.sqrt(G * M * a0)
    if capped:
        p = LB.capped_profile(0.0, CM.XSHARE[f], n_out=20000)
    else:
        x3 = 3 * MPC / rM; p = LB.uncapped_profile(0.0, x3, 30 * MPC / rM, n_out=20000)
    x = p["x"]; r = x * rM
    Phi = p["phi"] * s
    rho_ph = M * p["dell"] / (4 * math.pi * rM ** 3 * x ** 2)
    rho_b = np.zeros_like(x)          # point mass: no extended baryons (M-PIB reads zero there -> gate fully on)
    return dict(r=r, Phi=Phi, w=np.abs(Phi) * r ** 2, rho_ph=rho_ph, rho_b=rho_b, gr=G * M * p["ell"] / r ** 2, rc=p["xc"] * rM, rM=rM)
GAL = {}
for f in CM.FOOT:
    for lm in (9, 10, 11, 12):
        GAL[(f, lm, True)] = galaxy(10.0 ** lm, f, True)
        if MUT: GAL[(f, lm, False)] = galaxy(10.0 ** lm, f, False)


# ------------------------------------------------------------------ grading functions
def S_of(gate, u, mut): return CM.S_eval(gate, u, mut)


def xcop(gate, xi, mu, f, mut=None, selfcons=False):
    rc = xi * CM.rho_d0(f); m2 = (mu / MPC) ** 2; a0 = CM.A0[f]; d = []; r8a = 0.0; r8b = 0.0; nneg = 0
    for c in XC:
        rho = c["_rhob"] if mut == "M-PIB" else c[f"_ph_{f}"]
        nneg += int(np.sum(rho[: max(c["_ix"]) + 1] < 0))
        S, S1, S2 = S_of(gate, rho / rc, mut)
        MK = m2 / G * cumtrapz0(S * c["_w"], c["_rm"])
        if selfcons:
            for _ in range(5):
                rho2 = dens(lawM(c["_Mb"] + MK, c["_rm"], a0) - c["_Mb"] - MK, c["_rm"])
                S, S1, S2 = S_of(gate, rho2 / rc, mut); MK = m2 / G * cumtrapz0(S * c["_w"], c["_rm"])
        for z, i in zip(c["rows"], c["_ix"]):
            Mt = z["M_b"] * MS + MK[i]
            Ml = float(lawM(Mt, z["r_kpc"] * KPC, a0)) if Mt > 0 else 1e-30
            d.append(math.log10(max(z["M_HSE"] * MS / Ml, 1e-300)))   # guard: an infinite model (M-SIGN) reads -300
        # row 8 at the graded points
        Phi = c["_psi"]; c2Gm = m2 * Phi ** 2 * S1 / (8 * math.pi * G * rc)
        g8 = np.gradient(c2Gm, c["_rm"]); ix = c["_ix"]
        r8a = max(r8a, float(np.max(np.abs(c2Gm[ix] / Phi[ix]))), float(np.max(np.abs(g8[ix] / c["_gN"][ix]))))
        rhoK1 = m2 * np.abs(Phi) / (4 * math.pi * G)
        Lst = CM.LSTAR_PC[f] * 3.0857e16; r8b = max(r8b, float(np.max(S2[ix] * (rhoK1[ix] / rc) ** 2 / (mu / MPC * Lst) ** 2)))
    d = np.array(d); mean = float(d.mean()); rms = float(np.sqrt((d ** 2).mean()))
    return dict(mean=mean, rms=rms, PASS=bool(abs(mean) <= 0.05 and rms <= 0.10), r8a=r8a, r8b=r8b, nneg=nneg)


def groups(gate, xi, mu, f, mut=None, selfcons=False):
    rc = xi * CM.rho_d0(f); m2 = (mu / MPC) ** 2; a0 = CM.A0[f]; gm = {}
    for s in (0.0, 1.0):
        d = []
        for gp in GR:
            rho = gp[f"_rhob_{s}"] if mut == "M-PIB" else gp[f"_ph_{f}_{s}"]
            S = S_of(gate, rho / rc, mut)[0]; MK = m2 / G * cumtrapz0(S * gp["_w"], gp["_rm"])
            Mb = gp["_Mgas"] * (1 + s)
            if selfcons:
                for _ in range(5):
                    rho2 = dens(lawM(Mb + MK, gp["_rm"], a0) - Mb - MK, gp["_rm"])
                    S = S_of(gate, rho2 / rc, mut)[0]; MK = m2 / G * cumtrapz0(S * gp["_w"], gp["_rm"])
            for p, i in zip(gp["pts"], gp["_ix"]):
                Mt = p["M_gas"] * (1 + s) * MS + MK[i]
                Ml = float(lawM(Mt, p["r_kpc"] * KPC, a0)) if Mt > 0 else 1e-30
                d.append(math.log10(max(p["M_obs"] * MS / Ml, 1e-300)))
        gm[s] = float(np.mean(d))
    lo, hi = sorted(gm.values())
    return dict(bracket=[gm[1.0], gm[0.0]], PASS=bool(lo <= 0.05 and hi >= -0.05))


def galrow(gate, xi, mu, f, which, mut=None):
    """rows 5 / 6 proxy: M_K^gate(<r; mu) <= M_K^{S=1}(<r; mu_bound) on the range; returns worst ratio and row-8 numbers."""
    rc = xi * CM.rho_d0(f); m2 = (mu / MPC) ** 2
    if which == 5: lms, mub, rlo, rhi = (9, 10, 11), CM.MU_SPARC[f], 1.0, 30.0
    else: lms, mub, rlo, rhi = (10, 11, 12), CM.MU_KIDS[f], 1.0, 1000.0
    capped = not (mut == "M-NOCAP")
    worst = 0.0; r8a = 0.0; r8b = 0.0; at = None
    for lm in lms:
        g = GAL[(f, lm, capped)]; r = g["r"]
        rho = g["rho_b"] if mut == "M-PIB" else g["rho_ph"]
        S, S1, S2 = S_of(gate, rho / rc, mut)
        MKg = m2 / G * cumtrapz0(S * g["w"], r); MKu = (mub / MPC) ** 2 / G * cumtrapz0(g["w"], r)
        hi_ = min(rhi * KPC, g["rc"]) if capped else rhi * KPC
        sel = (r >= rlo * KPC) & (r <= hi_)
        ratio = MKg[sel] / MKu[sel]; j = int(np.argmax(ratio))
        if ratio[j] > worst: worst = float(ratio[j]); at = (lm, float(r[sel][j] / KPC))
        Phi = g["Phi"]; c2Gm = m2 * Phi ** 2 * S1 / (8 * math.pi * G * rc); g8 = np.gradient(c2Gm, r)
        r8a = max(r8a, float(np.max(np.abs(c2Gm[sel] / Phi[sel]))), float(np.max(np.abs(g8[sel] / g["gr"][sel]))))
        rhoK1 = m2 * np.abs(Phi) / (4 * math.pi * G); Lst = CM.LSTAR_PC[f] * 3.0857e16
        r8b = max(r8b, float(np.max(S2[sel] * (rhoK1[sel] / rc) ** 2 / (mu / MPC * Lst) ** 2)))
    return dict(worst_ratio=worst, at=at, PASS=bool(worst <= 1.0), r8a=r8a, r8b=r8b)


# Solar System (EW2 iter4 cassini, MK1 row 7)
GM_SUN = 1.32712440018e20; AU = 1.495978707e11; R_SAT = 9.5826 * AU; PHI0 = (600e3) ** 2; SAT, HEES = 7.0e-15, 9.0e-27
MU7 = MPC * min(math.sqrt(SAT / (GM_SUN / 2 + PHI0 * R_SAT / 3)), math.sqrt(3 * HEES / PHI0))
def u_sun(f):
    a0 = CM.A0[f]; M = 5e10 * MS; rM = math.sqrt(G * M / a0); x = 8 * KPC / rM
    return M * (x / math.sqrt(0.25 + x * x)) / (4 * math.pi * rM ** 3 * x * x)       # law phantom density [kg/m^3]
def sun(gate, xi, mu, f, mut=None):
    rc = xi * CM.rho_d0(f); S = float(S_of(gate, np.array([u_sun(f) / rc]), mut)[0][0])
    return dict(S=S, PASS=bool(mu * mu * S <= MU7 * MU7))


# ------------------------------------------------------------------ known answers
RES = dict(lane="PIK2", file=TAG, criteria="95edd35e0b", KA={}, scan={}, note=CM.NOTE)
if not MUT:
    P("Known answers")
    def xcop_S1(mu, f, form):
        a0 = CM.A0[f]; m2 = (mu / MPC) ** 2; d = []
        for c in XC:
            MK = m2 / G * cumtrapz0(c["_w"], c["_rm"])
            for z, i in zip(c["rows"], c["_ix"]):
                mk = float(np.interp(z["r_kpc"], c["_rr"], MK)) / MS
                if form == "additive": Ml = float(lawM(z["M_b"] * MS, z["r_kpc"] * KPC, a0)) / MS + mk
                else: Ml = float(lawM((z["M_b"] + mk) * MS, z["r_kpc"] * KPC, a0)) / MS
                d.append(math.log10(z["M_HSE"] / Ml))
        return float(np.mean(d))
    def mean0(f, form):
        lo, hi = 0.1, 1e3
        for _ in range(80):
            mid = math.sqrt(lo * hi); lo, hi = (mid, hi) if xcop_S1(mid, f, form) > 0 else (lo, mid)
        return math.sqrt(lo * hi)
    for f, rm, rz, re in (("canonical", 0.4644, 1.778, 1.53), ("alt", 0.4317, 1.736, 1.46)):
        m01 = xcop_S1(0.1, f, "additive"); z_add = mean0(f, "additive"); z_ex = mean0(f, "exact")
        ok = abs(m01 - rm) <= 1e-3 and abs(z_add - rz) <= 0.01 and abs(z_ex - re) <= 0.01
        RES["KA"][f"KA1 {f}"] = dict(add_mean_0p1=m01, add_mu0=z_add, exact_mu0=z_ex, ref=[rm, rz, re], ok=bool(ok))
        P(f"KA1 [{f}] S = 1: additive mean at 0.1 {m01:+.4f} ({rm:+.4f}); mean-zero additive {z_add:.3f} ({rz}); action-exact {z_ex:.3f} ({re}) -> {'PASS' if ok else 'FAIL'}")
    for f in CM.FOOT:
        I0 = CM.KD1[f]["I0"]; a = 1 / 3401.0; mb = math.sqrt(I0 * 0.99 / (4 * 0.01 * a ** 3)); ok = abs(mb / CM.KD1[f]["mu_B1a"] - 1) <= 1e-6
        RES["KA"][f"KA2 {f}"] = dict(value=mb, ok=bool(ok)); P(f"KA2 [{f}] mu_B1a = {mb:.3f} (KD1 {CM.KD1[f]['mu_B1a']:.3f}) -> {'PASS' if ok else 'FAIL'}")
    # KA5 phantom density
    f = "canonical"; M = 1e11 * MS; a0 = CM.A0[f]; rM = math.sqrt(G * M / a0); r = np.geomspace(0.5, 400, 200001) * KPC; x = r / rM
    rho_fd = dens(lawM(np.full_like(r, M), r, a0) - M, r); rho_cf = M * x / np.sqrt(0.25 + x * x) / (4 * math.pi * rM ** 3 * x * x)
    sel = (r >= KPC) & (r <= 300 * KPC); d5 = float(np.max(np.abs(rho_fd[sel] / rho_cf[sel] - 1)))
    xb = 1e3; deep = math.sqrt(M * a0 / G) / (4 * math.pi * (xb * rM) ** 2); cfb = M * xb / math.sqrt(0.25 + xb * xb) / (4 * math.pi * rM ** 3 * xb * xb)
    d5b = abs(cfb / deep - 1); g11 = galaxy(1e11, f); dg = float(np.max(np.abs(np.interp(r[sel], g11["r"], g11["rho_ph"]) / rho_cf[sel] - 1)))
    ok = d5 <= 1e-4 and d5b <= 1e-6 and dg <= 1e-4
    RES["KA"]["KA5"] = dict(fd_vs_closed=d5, deep_x1e3=d5b, lib_vs_closed=dg, ok=bool(ok))
    P(f"KA5 phantom: finite difference vs closed form {d5:.1e}; MK1-lib dell vs closed form {dg:.1e} (line 1e-4); closed vs deep at x 1e3 {d5b:.1e} (line 1e-6) -> {'PASS' if ok else 'FAIL'}")
    # KA6: S = 1 dust through the gated code (any gate at u -> 0, xi huge) equals MK1's MKc construction (QX2's integ) at mu 1
    d6 = 0.0
    for c in XC:
        rr, psi = Q2["psi_profile"](c)
        integ = np.concatenate([[0.0], np.cumsum(0.5 * (np.abs(psi[1:]) * (rr[1:] * KPC) ** 2 + np.abs(psi[:-1]) * (rr[:-1] * KPC) ** 2) * np.diff(rr * KPC))])
        mk1 = (1 / MPC) ** 2 / G * integ
        mine = (1 / MPC) ** 2 / G * cumtrapz0(CM.S_eval("E1", c["_ph_canonical"] / 1e300)[0] * c["_w"], c["_rm"])
        d6 = max(d6, float(np.max(np.abs(mine[1:] / mk1[1:] - 1))))
    RES["KA"]["KA6"] = dict(rel=d6, ok=bool(d6 <= 1e-8)); P(f"KA6 S -> 1 dust vs MK1/QX2 construction: max rel {d6:.1e} -> {'PASS' if d6 <= 1e-8 else 'FAIL'}")
    for f, ref in (("canonical", (0.196, 0.359)), ("alt", (0.158, 0.320))):
        b = groups("E1", 1e300, 0.0, f)["bracket"]; dv = max(abs(b[0] - ref[0]), abs(b[1] - ref[1]))
        RES["KA"][f"KA7 {f}"] = dict(value=b, ok=bool(dv <= 2e-3)); P(f"KA7 [{f}] groups at mu 0: [{b[0]:+.3f}, {b[1]:+.3f}] ({ref}) -> {'PASS' if dv <= 2e-3 else 'FAIL'}")
    m2 = (2.04e4 / MPC) ** 2; dg8 = m2 * GM_SUN / 2 + m2 * PHI0 * R_SAT / 3; ok = abs(dg8 / 7.5e-14 - 1) <= 0.02 and abs(MU7 - 6223.35) <= 1
    RES["KA"]["KA8"] = dict(dg=dg8, mu7=MU7, ok=bool(ok)); P(f"KA8 Saturn at 2.04e4: {dg8:.3e} (7.5e-14); mu_7 = {MU7:.2f} (6223.35) -> {'PASS' if ok else 'FAIL'}")
    # KA9: SI recomputation of rho_d0 and of c^2 Gm (energy units, separately)
    for f in CM.FOOT:
        H0 = CM.H_LIT * 100e3 / MPC; Om_d = CM.KD1[f]["I0"] * (CM.C_KMS / (CM.H_LIT * 100)) ** 2 / 3
        rd_si = 3 * H0 ** 2 * Om_d / (8 * math.pi * G); d9 = abs(rd_si / CM.rho_d0(f) - 1)
        # c^2 Gm at Phi = -(1000 km/s)^2, S' = 1, rho_c = 1e-24: F = mu^2 (Phi/c^2)^2/(2K), K = 4 pi G/c^4 [m/J]; Pi_c = c^2 rho_c [J/m^3]
        mu_ = 2.512e4 / MPC; Phi = -1e12; K = 4 * math.pi * G / CM.C ** 4; F = mu_ ** 2 * (Phi / CM.C ** 2) ** 2 / (2 * K)
        Gm = F * 1.0 / (CM.C ** 2 * 1e-24); simp = mu_ ** 2 * Phi ** 2 / (8 * math.pi * G * 1e-24); d9b = abs(CM.C ** 2 * Gm / simp - 1)
        ok = d9 <= 1e-6 and d9b <= 1e-6
        RES["KA"][f"KA9 {f}"] = dict(rho_d0=CM.rho_d0(f), rho_d0_SI=rd_si, rel=d9, c2Gm_rel=d9b, ok=bool(ok))
        P(f"KA9 [{f}] rho_d0 = {CM.rho_d0(f):.5e} kg/m^3 (SI from H0, Omega_d: {rd_si:.5e}); c^2 Gm energy-unit route vs formula rel {d9b:.1e} -> {'PASS' if ok else 'FAIL'}")
    P(f"   u_Sun reference: law phantom at 8 kpc (5e10) = {u_sun('canonical'):.3e} kg/m^3 = {u_sun('canonical') / CM.rho_d0('canonical'):.3e} rho_d0")
    RES["KA_all_pass"] = all(v["ok"] for v in RES["KA"].values())
    P(f"Known answers: {sum(v['ok'] for v in RES['KA'].values())}/{len(RES['KA'])} PASS")
    # reference densities (reported): phantom density ranges probed by each row, in units of rho_d0
    for f in CM.FOOT:
        r0 = CM.rho_d0(f)
        xs = [c[f"_ph_{f}"][c["_ix"]] / r0 for c in XC]; gg = [gp[f"_ph_{f}_0.0"][gp["_ix"]] / r0 for gp in GR]
        P(f"[{f}] u*xi (phantom/rho_d0): X-COP points {min(map(min, xs)):.3g}..{max(map(max, xs)):.3g}; groups {min(map(min, gg)):.3g}..{max(map(max, gg)):.3g}; "
          + "; ".join(f"gal 1e{lm} 1-30 kpc {np.interp(30 * KPC, GAL[(f, lm, True)]['r'], GAL[(f, lm, True)]['rho_ph']) / r0:.3g}..{np.interp(KPC, GAL[(f, lm, True)]['r'], GAL[(f, lm, True)]['rho_ph']) / r0:.3g}" for lm in (9, 10, 11, 12))
          + f"; r_c 1e10/1e12: {GAL[(f, 10, True)]['rc'] / KPC:.0f}/{GAL[(f, 12, True)]['rc'] / KPC:.0f} kpc")

# ------------------------------------------------------------------ the scan
ARMS = [None] if not MUT else ["M-S1", "M-SIGN", "M-PIB", "M-NOCAP"]
GATESCAN = CM.GRADED + ([f"BAND{b}" for b in range(13)] if not MUT else [])
for arm in ARMS:
    akey = arm or "primary"; RES["scan"][akey] = {}
    gates = (["E1"] if arm in ("M-S1", "M-SIGN") else (["E1", "P2", "F2"] if MUT else GATESCAN))
    for f in CM.FOOT:
        RES["scan"][akey][f] = {}
        for mlab, mu in CM.MU_LIST(f).items():
            RES["scan"][akey][f][mlab] = {}
            P(f"\n[{akey}] [{f}] mu {mu:.5g} ({mlab})")
            for g in gates:
                rows = []
                for lx in CM.LOGXI:
                    xi = 10.0 ** lx
                    r3 = xcop(g, xi, mu, f, arm); r4 = groups(g, xi, mu, f, arm); r5 = galrow(g, xi, mu, f, 5, arm); r6 = galrow(g, xi, mu, f, 6, arm); r7 = sun(g, xi, mu, f, arm)
                    r8a = max(r3["r8a"], r5["r8a"], r6["r8a"]); r8b = max(r3["r8b"], r5["r8b"], r6["r8b"])
                    p37 = r3["PASS"] and r4["PASS"] and r5["PASS"] and r6["PASS"] and r7["PASS"]
                    sc = None
                    if p37:
                        s3 = xcop(g, xi, mu, f, arm, selfcons=True); s4 = groups(g, xi, mu, f, arm, selfcons=True); sc = bool(s3["PASS"] and s4["PASS"])
                    rows.append(dict(logxi=float(lx), r3=r3, r4=r4, r5=r5, r6=r6, r7=r7, r8a=r8a, r8b=r8b, p37=p37, KSC=sc,
                                     p8=bool(r8a <= 0.02 and r8b <= 1.0), galaxy_ok=bool(r5["PASS"] and r6["PASS"] and r7["PASS"]),
                                     cluster_ok=bool(r3["PASS"] and r4["PASS"])))
                cnt = {k: sum(r[k] for r in rows) for k in ("p37", "galaxy_ok", "cluster_ok")}
                c3 = [r for r in rows if r["r3"]["PASS"]]; c4 = [r for r in rows if r["r4"]["PASS"]]
                b3 = min(rows, key=lambda r: r["r3"]["rms"])
                gal = [r for r in rows if r["galaxy_ok"]]
                RES["scan"][akey][f][mlab][g] = dict(counts=cnt, rows=rows)
                P(f"  {g:6s} pass: X-COP {len(c3)}, groups {len(c4)}, SPARC {sum(r['r5']['PASS'] for r in rows)}, KiDS {sum(r['r6']['PASS'] for r in rows)}, Sun {sum(r['r7']['PASS'] for r in rows)}; "
                  f"galaxy rows together {cnt['galaxy_ok']}, cluster rows together {cnt['cluster_ok']}, rows 3-7 {cnt['p37']}; "
                  f"X-COP best rms {b3['r3']['rms']:.3f} (mean {b3['r3']['mean']:+.3f}) at log xi {b3['logxi']}"
                  + (f"; groups pass log xi {c4[0]['logxi']}..{c4[-1]['logxi']}" if c4 else "")
                  + (f"; galaxy rows pass log xi {gal[0]['logxi']}..{gal[-1]['logxi']}" if gal else "")
                  + (f"; X-COP pass log xi {[r['logxi'] for r in c3]} r8a {[round(r['r8a'], 3) for r in c3]} r8b {[float('%.2g' % r['r8b']) for r in c3]}" if c3 else ""))
                for r in rows:
                    if r["p37"]:
                        P(f"     rows 3-7 PASS at log xi {r['logxi']}: r8a {r['r8a']:.3g}, r8b {r['r8b']:.3g}, K-SC {r['KSC']}")
P(f"\nruntime {time.time() - T0:.0f} s"); P(CM.NOTE)
json.dump(CM.clean(RES), open(os.path.join(HERE, TAG + ".json"), "w"))
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
