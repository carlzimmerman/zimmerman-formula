#!/usr/bin/env python3
"""SV5 iter_1 (class W: a0 law on the linear web, target sector field) + iter_2 (class C: Jeans scale switched by the AC2q
charge D.P + 2X). Criteria: FROZEN_CRITERIA.md + iter_1/iter_2 FROZEN_CRITERIA.md (247d2eaa2f).
    python3 sv5_web.py            -> iter_1_law_on_web/sv5_iter1.json/.out, iter_2_charge_switched_sound_speed/sv5_iter2.json/.out
    python3 sv5_web.py --mutate   -> the *_MUTATE twins (iter_1: nu == 1; iter_2: M1 switch off, M2 web charge 0)
kappa = 1/2 FITTED; not theory closed. 1 thread, 128^3. Footings never pooled. No field dumps."""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sv5_common as C
import numpy as np
MUT = "--mutate" in sys.argv; OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
HERE = C.HERE; D1 = os.path.join(HERE, "iter_1_law_on_web"); D2 = os.path.join(HERE, "iter_2_charge_switched_sound_speed")
N3 = C.load_growth(); I2 = N3["I2"]; M = N3["M"]
sigA, AX0 = C.sigma_A_rel(N3)
G = 6.67430e-11; CC = 2.99792458e8; MPC = 3.0856775814913673e22; MSUN = 1.98892e30
ob, od, H0, h = N3["ob"], N3["od"], N3["H0"], N3["h"]
Om = (ob + od) / h ** 2; H0s = H0 * 1e3 / MPC
NG, LBOX = 128, 2000.0; ZG = [0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 12.0, 20.0, 50.0]
def nu(y): return 0.5 + np.sqrt(0.25 + 1.0 / np.maximum(y, 1e-300))

kf = 2 * np.pi / LBOX; k1 = np.fft.fftfreq(NG, d=LBOX / NG) * 2 * np.pi
KX, KY, KZ = np.meshgrid(k1, k1, k1, indexing="ij"); K2 = KX ** 2 + KY ** 2 + KZ ** 2; KK = np.sqrt(K2); K2[0, 0, 0] = 1.0
edges = np.geomspace(kf, np.pi * NG / LBOX, 17); kc = np.sqrt(edges[1:] * edges[:-1]); sh = np.digitize(KK, edges) - 1
def shell_mean(x): return np.array([x[sh == i].mean() if np.any(sh == i) else np.nan for i in range(16)])

def realise(seed):
    rng = np.random.default_rng(seed); w = np.fft.fftn(rng.standard_normal((NG, NG, NG))); dV = (LBOX / NG) ** 3
    return w, dV
def delta_k(w, dV, z):
    Pk = np.zeros_like(KK); m = KK > 0
    kk = np.clip(KK[m], 1e-5, 9.0); ku = np.unique(np.round(np.log(kk), 4))
    zc = min(z, N3["I2"].ZPK); fac = ((1 + zc) / (1 + z)) ** 2          # A1: z > z_max_pk uses EdS growth D ~ a
    Pu = np.array([M.pk_lin(float(np.exp(x)), zc) for x in np.linspace(ku.min(), ku.max(), 400)]) * fac
    Pk[m] = np.exp(np.interp(np.log(kk), np.linspace(ku.min(), ku.max(), 400), np.log(Pu))) * AX0
    return w * np.sqrt(Pk / dV), Pk

def fields(dk, z, a0, law=True):
    a = 1 / (1 + z); kSI = 1.0 / MPC
    phik = -1.5 * H0s ** 2 * Om * dk / (a * K2 * kSI ** 2); phik[0, 0, 0] = 0
    gx, gy, gz = [np.real(np.fft.ifftn(-1j * Kc * kSI * phik)) / a for Kc in (KX, KY, KZ)]
    gn = np.sqrt(gx ** 2 + gy ** 2 + gz ** 2); y = gn / a0
    n = nu(y) if law else np.ones_like(y)
    Vk = [np.fft.fftn(n * gc) for gc in (gx, gy, gz)]; Nk = [np.fft.fftn(gc) for gc in (gx, gy, gz)]
    divV = KX * Vk[0] + KY * Vk[1] + KZ * Vk[2]; divN = KX * Nk[0] + KY * Nk[1] + KZ * Nk[2]
    B = shell_mean(np.abs(divV) ** 2) / shell_mean(np.abs(divN) ** 2)
    # integrated gradient power of the longitudinal fields (Lean bound): |g_k|^2 = |k.V_k|^2/k^2
    PL = (np.abs(divV) ** 2 / K2).sum(); PN = (np.abs(divN) ** 2 / K2).sum()
    # phantom density rho_ph = -div_phys[(nu-1) g_N]/(4 pi G)
    Wk = [np.fft.fftn((n - 1) * gc) for gc in (gx, gy, gz)]
    div = np.real(np.fft.ifftn(1j * (KX * Wk[0] + KY * Wk[1] + KZ * Wk[2]))) * kSI / a
    rho_ph = -div / (4 * np.pi * G)
    return dict(B=B, ymax=float(y.max()), ymed=float(np.median(y)), Pint=float(PL / PN), rho_ph=rho_ph, gn=gn)

def project(Bz):
    kg, zg = N3["kgrid"], N3["zgrid"]; lz = np.log1p(np.array(ZG)); Rr = np.empty((len(kg), len(zg)))
    lB = np.array([np.interp(np.log(kg), np.log(kc), np.sqrt(b)) for b in Bz])      # held outside shells
    for j, z in enumerate(zg):
        x = np.clip(math.log1p(z), lz[0], lz[-1])
        for i in range(len(kg)): Rr[i, j] = np.interp(x, lz, lB[:, i])
    S = I2.limber_ratio(M, H0, kg, zg, Rr); c, A = I2.best_amp_chi2(N3["X0"] * S); c0, A0x = I2.best_amp_chi2(N3["X0"])
    return dict(r=float(A0x / A), dchi2=float(c - c0), S={str(L): float(S[L]) for L in (8, 30, 100, 200, 300, 400)})

# ---------------- hosts (iter_2)
Q = C.load_qx10()
def host_rho(Mfn, r_kpc, a0):
    rr = np.array([r_kpc * (1 - 1e-3), r_kpc * (1 + 1e-3)]) * 1e3 * 3.0856775814913673e16
    q = []
    for x in rr:
        Mx = Mfn(x / (1e3 * 3.0856775814913673e16)) * MSUN; gN = G * Mx / x ** 2; g = 0.5 * gN + math.sqrt(0.25 * gN ** 2 + a0 * gN)
        q.append(x ** 2 * (g - gN))
    x = r_kpc * 1e3 * 3.0856775814913673e16
    return (q[1] - q[0]) / (rr[1] - rr[0]) / (4 * np.pi * G * x ** 2)
def hosts(a0):
    rows = []
    for nm, Mb, Ro in Q["G5SYS"]:
        rows.append(dict(name=nm, Mb=Mb, Mfn=Q["expdisc"](Mb, Ro), rin=max(Ro, 10.0)))
    for lm in (9.4, 10.45, 10.7, 10.9):
        rows.append(dict(name=f"KiDS logMb {lm}", Mb=10 ** lm, Mfn=Q["pointmass"](10 ** lm), rin=10.0))
    out = []
    for hr in rows:
        rta = Q["r_ta"](hr["Mb"]); rr = np.geomspace(hr["rin"], rta, 40); rho = np.array([host_rho(hr["Mfn"], x, a0) for x in rr])
        out.append(dict(name=hr["name"], Mb=hr["Mb"], r_ta_kpc=rta, rho_ph_rta=float(rho[-1]), monotone=bool(np.all(np.diff(rho) <= 1e-12 * abs(rho[0])))))
    return out

if __name__ == "__main__":
    W, dV = realise(5)
    R1 = dict(lane="SV5 iter_1" + (" MUTATE" if MUT else ""), criteria="247d2eaa2f", sigma_A_rel=sigA, A_X0=AX0, box=[NG, LBOX], z=ZG, foot={})
    R2 = dict(lane="SV5 iter_2" + (" MUTATE" if MUT else ""), criteria="247d2eaa2f", f_line=1.5 * sigA, foot={})
    P(f"SV5 web lanes ({'MUTATE' if MUT else 'main'}). kappa = 1/2 FITTED; not theory closed. sigma_A,rel {sigA:.4f}, A_X0 {AX0:.4f}; box {NG}^3, {LBOX:g} Mpc.")
    # K1 (main only): realisation power vs input at z = 1
    if not MUT:
        dk, Pk = delta_k(W, dV, 1.0); Pest = shell_mean(np.abs(dk) ** 2 * dV / NG ** 3) / shell_mean(Pk)
        R1["K1"] = dict(ratio_by_shell=Pest.tolist(), median=float(np.nanmedian(Pest)), pass_=bool(abs(np.nanmedian(Pest) - 1) <= 0.15))
        P(f"K1 realisation/input power at z 1: median {R1['K1']['median']:.3f} -> {'PASS' if R1['K1']['pass_'] else 'FAIL'}")
    for f, a0 in C.A0.items():
        rho_de = 4 * a0 ** 2 / (G * CC ** 2)
        Bz = []; rows = []; webq = {}
        for z in ZG:
            dk, _ = delta_k(W, dV, z); fl = fields(dk, z, a0, law=not MUT)
            Bz.append(fl["B"]); numin = float(nu(np.array(fl["ymax"])))
            rows.append(dict(z=z, B_by_shell=fl["B"].tolist(), ymax=fl["ymax"], ymed=fl["ymed"], nu_min=numin, Lean_bound=numin ** 2 if not MUT else 1.0, P_int_ratio=fl["Pint"]))
            wts = np.maximum(1 + np.real(np.fft.ifftn(dk)), 0.0); webq[z] = (fl["rho_ph"], wts)
        pr = project(Bz)
        w1 = abs(pr["r"] - 1) <= 3 * sigA; w2 = pr["dchi2"] <= I2.DCHI2_LINE
        R1["foot"][f] = dict(rows=rows, proj=pr, W1_pass=bool(w1), W2_pass=bool(w2))
        P(f"[{f}] iter_1: lensing amplitude r = {pr['r']:.3g} (line |r-1| <= {3*sigA:.3f}) -> W1 {'PASS' if w1 else 'FAIL'}; shape dchi2 {pr['dchi2']:.1f} -> W2 {'PASS' if w2 else 'FAIL'}; S(L) 30/100/400 "
          + "/".join(f"{pr['S'][L]:.3g}" for L in ('30', '100', '400')))
        for rw in rows:
            P(f"   z {rw['z']:g}: |g_N|/a0 median {rw['ymed']:.3g} max {rw['ymax']:.3g}; nu_min {rw['nu_min']:.3g} -> Lean bound {rw['Lean_bound']:.3g}; integrated |g|^2 ratio {rw['P_int_ratio']:.3g}; B(k) first/mid/last shell "
              f"{rw['B_by_shell'][0]:.3g}/{rw['B_by_shell'][8]:.3g}/{rw['B_by_shell'][15]:.3g}")
        # iter_2
        H = hosts(a0); Sst = min(x["rho_ph_rta"] for x in H); mono = all(x["monotone"] for x in H)
        sun = host_rho(Q["pointmass"](6e10), 8.2, a0)
        Fz = {}; F0 = {}
        for z in ZG:
            rp, wt = webq[z]
            if MUT: rp = np.zeros_like(rp)
            Fz[str(z)] = float((wt * (rp >= Sst)).sum() / wt.sum()); F0[str(z)] = float((wt * (rp >= 0)).sum() / wt.sum())
        c2 = all(v <= 1.5 * sigA for v in Fz.values())
        R2["foot"][f] = dict(hosts=H, Sigma_star=Sst, Sigma_star_over_rhoDE=Sst / rho_de, C1_monotone=mono, sun_rho_ph=sun, C4_sun_stiff=bool(sun >= Sst),
                             F=Fz, F_sign_switch=F0, C2_pass=bool(c2), Aweb_branch_pass=bool(Sst > 2 * rho_de),
                             web_rho_ph_median_over_rhoDE={str(z): float(np.median(webq[z][0][webq[z][0] > 0]) / rho_de) for z in ZG})
        P(f"[{f}] iter_2: Sigma_* = {Sst:.3g} kg/m^3 = {Sst/rho_de:.3g} rho_DE (least-charged host at r_ta: {min(H, key=lambda x: x['rho_ph_rta'])['name']}); C1 monotone {mono}; "
          f"Sun {sun/rho_de:.3g} rho_DE -> C4 {'stiff' if sun >= Sst else 'NOT stiff'}")
        P(f"   web stiff fraction F(z) (line {1.5*sigA:.3f}): " + ", ".join(f"z{z}: {v:.3f}" for z, v in Fz.items()) + f" -> C2 {'PASS' if c2 else 'FAIL'}")
        P(f"   AC2q sign switch F_0(z): " + ", ".join(f"z{z}: {v:.3f}" for z, v in F0.items()) + f"; A-web branch (Sigma_* > 2 rho_DE): {R2['foot'][f]['Aweb_branch_pass']}")
        P(f"   web median positive charge / rho_DE: " + ", ".join(f"z{z}: {v:.3g}" for z, v in R2['foot'][f]['web_rho_ph_median_over_rhoDE'].items()))
        del webq
    if not MUT:
        # K1 for iter_2: deep-MOND point mass, rho_ph 4 pi G r^2 = sqrt(a0 G M) at 100 r_M
        a0 = C.A0["canonical"]; Mb = 1e10; rM = math.sqrt(G * Mb * MSUN / a0) / (1e3 * 3.0856775814913673e16)
        lhs = host_rho(Q["pointmass"](Mb), 100 * rM, a0) * 4 * np.pi * G * (100 * rM * 1e3 * 3.0856775814913673e16) ** 2
        rhs = math.sqrt(a0 * G * Mb * MSUN); R2["K1"] = dict(ratio=lhs / rhs, pass_=bool(abs(lhs / rhs - 1) <= 0.01))
        P(f"iter_2 K1 deep-MOND point-mass phantom: ratio {lhs/rhs:.4f} -> {'PASS' if R2['K1']['pass_'] else 'FAIL'}")
        # K2 (iter_1): a0 x 1e-8 -> nu -> 1
        dk, _ = delta_k(W, dV, 1.0); fl = fields(dk, 1.0, C.A0["canonical"] * 1e-8); dev = float(np.max(np.abs(fl["B"] - 1)))
        R1["K2"] = dict(max_dev=dev, pass_=bool(dev <= 1e-2)); P(f"iter_1 K2 (a0 x 1e-8): max |B-1| {dev:.2e} -> {'PASS' if dev <= 1e-2 else 'FAIL'}")
        W6, dV6 = realise(6); dk, _ = delta_k(W6, dV6, 1.0); fl = fields(dk, 1.0, C.A0["canonical"])
        R1["K3_seed6_z1_B"] = fl["B"].tolist(); P(f"iter_1 K3 seed 6 z 1 canonical B first/mid/last {fl['B'][0]:.3g}/{fl['B'][8]:.3g}/{fl['B'][15]:.3g}")
        labW = "NO-GO FOR CLASS W" if all((not R1["foot"][f]["W1_pass"]) and all(r_["Lean_bound"] > 1 + 3 * sigA for r_ in R1["foot"][f]["rows"]) for f in C.A0) else \
               ("FAIL" if any(not (R1["foot"][f]["W1_pass"] and R1["foot"][f]["W2_pass"]) for f in C.A0) else "PASS")
        labC = "NO-GO FOR CLASS C" if all(not R2["foot"][f]["C2_pass"] for f in C.A0) else ("FAIL" if any(not R2["foot"][f]["C2_pass"] for f in C.A0) else "PASS (C2; C3 by construction)")
        R1["label"] = labW; R2["label"] = labC; P(f"iter_1 LABEL: {labW}"); P(f"iter_2 LABEL: {labC}")
    else:
        R1["bites"] = bool(all(abs(R1["foot"][f]["proj"]["r"] - 1) <= 1e-6 and abs(R1["foot"][f]["proj"]["dchi2"]) <= 1e-6 for f in C.A0))
        m1 = {}
        for f in C.A0:
            a0k = Q["A0K"][f]; o = Q["grade_cell"](1.0, a0k); m1[f] = dict(G5_max=max(x["ratio"] for x in o["G5"]["rows"]), G5_pass=bool(o["G5"]["pass_"]))
        R2["M1"] = dict(rows=m1, bites=bool(all(not v["G5_pass"] for v in m1.values())))
        R2["M2_C2_pass"] = bool(all(R2["foot"][f]["C2_pass"] for f in C.A0))
        P(f"iter_1 MUTATE (nu == 1): r and dchi2 -> {'r = 1, dchi2 = 0: W1, W2 PASS (bites iff main fails W1)' if R1['bites'] else 'NOT REPRODUCED'}")
        P(f"iter_2 MUTATE M1 (switch off, lambda 1 kpc): " + "; ".join(f"{f} G5 max {v['G5_max']:.2f}" for f, v in m1.items()) + f" -> {'BITES' if R2['M1']['bites'] else 'NO BITE'}")
        P(f"iter_2 MUTATE M2 (web charge 0): C2 {'PASS' if R2['M2_C2_pass'] else 'FAIL'} (bites iff main C2 fails)")
    for D, R, nm in ((D1, R1, "sv5_iter1"), (D2, R2, "sv5_iter2")):
        tag = nm + ("_MUTATE" if MUT else "")
        json.dump(R, open(os.path.join(D, tag + ".json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o))
    open(os.path.join(HERE, "sv5_web" + ("_MUTATE" if MUT else "") + ".out"), "w").write("\n".join(OUT) + "\n")
