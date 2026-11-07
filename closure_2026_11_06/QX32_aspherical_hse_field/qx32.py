#!/usr/bin/env python3
"""QX32 (criteria c302aa5804 + A1 + A2): aspherical-cluster bias of spherical HSE in the law's QUMOND field.
    python3 qx32.py     # qx32.json / qx32.out (main, K1, K2, MUTATE)
Grid 256^3, box 6 Mpc, FFT. QUMOND: g = longitudinal part of nu(|g_N|/a0) g_N, nu = g_law(g_N)/g_N per footing.
kappa = 1/2 FITTED; not theory closed. 1 thread, float32."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); TAG = "qx32"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
I5 = os.path.join(HERE, "..", "QX7_unified_cold_switch", "iter_5_host_hydrostatic", "qx7_iter5.py")
s5 = open(I5).read(); s5 = s5[:s5.index("# ---- the host-hydrostatic")]
argv0, sys.argv = sys.argv, [I5]; NS = {"__file__": os.path.abspath(I5), "__name__": "iter5_reused"}
exec(compile(s5, I5, "exec"), NS); sys.argv = argv0
G, MS, KPC, A0, glaw, XC, XPROF = (NS[k] for k in ("G", "MS", "KPC", "A0", "glaw", "XC", "XPROF"))
# grid units: kpc, Msun, (km/s)^2/kpc  (float32-safe)
GU = 4.30091e-6; AU = {f: a * KPC / 1e6 for f, a in A0.items()}
N, L = 256, 6.0e3; h = L / N
x1 = ((np.arange(N) - N // 2 + 0.5) * h).astype(np.float32)
X, Y, Z = np.meshgrid(x1, x1, x1, indexing="ij"); Rg = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
kx = (2 * np.pi * np.fft.fftfreq(N, d=h)).astype(np.float32); kz = (2 * np.pi * np.fft.rfftfreq(N, d=h)).astype(np.float32)
KX, KY, KZ = np.meshgrid(kx, kx, kz, indexing="ij"); K2 = KX ** 2 + KY ** 2 + KZ ** 2; K2[0, 0, 0] = 1.0

def rho_sph(name):
    fx, Ml = XPROF[name]; rr = np.geomspace(1.0, 4e3, 4000); M = fx(rr * KPC)
    rho = np.gradient(M, rr) / (4 * np.pi * rr ** 2); rho[rho < 0] = 0
    return lambda r: np.interp(r, rr, rho, left=rho[0], right=0.0)
def density(name, q, kind):
    f = rho_sph(name)
    if q == 1.0: m = Rg
    elif kind == "oblate": m = np.sqrt(q ** (2 / 3) * (X ** 2 + Y ** 2) + q ** (-4 / 3) * Z ** 2)
    else: m = np.sqrt(q ** (-4 / 3) * (X ** 2 + Y ** 2) + q ** (2 / 3) * Z ** 2)
    rho = f(m).astype(np.float32); Mtot = XPROF[name][1]; rho *= np.float32(Mtot / (rho.sum(dtype=np.float64) * h ** 3)); return rho
def gN_field(rho):
    rk = np.fft.rfftn(rho); phik = (-4 * np.pi * GU) * rk / K2; phik[0, 0, 0] = 0; del rk
    return [np.fft.irfftn(-1j * Kc * phik, s=rho.shape).astype(np.float32) for Kc in (KX, KY, KZ)]
def qumond(g, a0, mode="law"):
    gm = np.sqrt(g[0] ** 2 + g[1] ** 2 + g[2] ** 2) + np.float32(1e-30)
    nu = (glaw(gm.astype(np.float64), a0) / gm).astype(np.float32)
    if mode == "nu2": nu = nu * nu
    if mode == "newton": nu = np.ones_like(nu)
    kdotF = KX * np.fft.rfftn(nu * g[0])
    kdotF += KY * np.fft.rfftn(nu * g[1]); kdotF += KZ * np.fft.rfftn(nu * g[2]); del nu, gm
    return [np.fft.irfftn(Kc * kdotF / K2, s=g[0].shape).astype(np.float32) for Kc in (KX, KY, KZ)]
def shell(g, rho, rlist):
    gr = -(g[0] * X + g[1] * Y + g[2] * Z) / np.maximum(Rg, 1e-9)
    out = []
    for r in rlist:
        sel = np.abs(Rg - r) <= 0.5 * h; Mapp = r ** 2 * float(gr[sel].mean()) / GU
        Mb = float(rho[Rg <= r].sum(dtype=np.float64)) * h ** 3; out.append((Mapp, Mb))
    return out
def mlaw(Mb, r, a0): return glaw(GU * Mb / r ** 2, a0) * r ** 2 / GU

SHAPES = [(1.0, "sph"), (0.7, "oblate"), (0.5, "oblate"), (0.7, "prolate"), (0.5, "prolate")]
names = sorted(XPROF); RES = dict(tag=TAG, criteria="c302aa5804 + A1 + A2", grid=dict(N=N, box_kpc=L, cell_kpc=h), note="kappa = 1/2 FITTED; not theory closed")
P(f"QX32: grid {N}^3, cell {h:.1f} kpc; {len(names)} X-COP clusters; shapes {SHAPES}")
rows = {}; k1 = []; k2 = []; mut = []
for nm in names:
    rl = [z["r_kpc"] for z in XC if z["name"] == nm]; ref = {}
    for q, kind in SHAPES:
        rho = density(nm, q, kind); gN = gN_field(rho)
        sn = shell(gN, rho, rl); k2row = [math.log10(Ma / Mb) for Ma, Mb in sn]   # Newton: M_app / M_b(<r) = 1 by Gauss
        for f, a0 in AU.items():
            gq = qumond(gN, a0); sq = shell(gq, rho, rl)
            lg = [math.log10(Ma / mlaw(Mb, r, a0)) for (Ma, Mb), r in zip(sq, rl)]
            key = f"{nm}|{kind}{q}|{f}"; rows[key] = lg
            if q == 1.0: ref[f] = lg; k1.append((nm, f, lg))
            if q == 1.0 and f == "canonical":
                sm = shell(qumond(gN, a0, "nu2"), rho, rl); mut.append(math.log10(sm[3][0] / sq[3][0]))
            del gq
        if q == 1.0: k2.append((nm, "sph", k2row))
        else: k2.append((nm, f"{kind}{q}", k2row))
        del gN, rho
    for q, kind in SHAPES[1:]:
        for f in A0:
            d = [a - b for a, b in zip(rows[f"{nm}|{kind}{q}|{f}"], ref[f])]; rows[f"{nm}|{kind}{q}|{f}|Delta"] = d
    P(f"  {nm}: K1 (q=1 vs algebraic law, canonical) " + " ".join(f"{v:+.3f}" for v in ref["canonical"])
      + " | Delta canonical: " + "; ".join(f"{kind}{q} " + " ".join(f"{v:+.3f}" for v in rows[f'{nm}|{kind}{q}|canonical|Delta']) for q, kind in SHAPES[1:]))
RES["rows"] = rows
# K1: |q=1 vs law| <= 0.03 at 0.2-0.7 R500 (indices 1..4)
k1err = max(abs(v) for _, _, lg in k1 for v in lg[1:]); K1 = k1err <= 0.03
k2err = max(abs(v) for _, _, r in k2 for v in r[1:]); K2p = k2err <= max(0.03, k1err)
MUT = min(abs(v) for v in mut) > 0.1
P(f"  K1: max |q=1 - law| at 0.2-0.7 R500 = {k1err:.4f} -> {'PASS' if K1 else 'FAIL'}; K2 (Newton, Gauss): max |log M_app/M_b| = {k2err:.4f} -> {'PASS' if K2p else 'FAIL'}; "
  f"MUTATE nu^2 at 0.5 R500: min move {min(abs(v) for v in mut):.3f} -> {'BITES' if MUT else 'NO BITE'}")
summ = {}
for q, kind in SHAPES[1:]:
    for f in A0:
        allv = [v for nm in names for v in rows[f"{nm}|{kind}{q}|{f}|Delta"]]; summ[f"{kind}{q}|{f}"] = dict(mean=float(np.mean(allv)), min=float(min(allv)), max=float(max(allv)))
        P(f"  class {kind} q={q} {f}: mean Delta {np.mean(allv):+.4f} [{min(allv):+.4f}, {max(allv):+.4f}]")
RES["summary"] = summ; RES["K1"] = dict(err=k1err, pass_=bool(K1)); RES["K2"] = dict(err=k2err, pass_=bool(K2p)); RES["MUTATE"] = dict(moves=mut, bites=bool(MUT))
mx = max(summ.values(), key=lambda s: abs(s["mean"]))["mean"]
lab = "EXPLAINS" if mx >= 0.30 else ("PARTIAL" if abs(mx) >= 0.10 else "NEGLIGIBLE")
if not (K1 and K2p and MUT): lab = "NO VERDICT (control failed) | numbers read " + lab
RES["label"] = lab; P(f"  LABEL: {lab} (largest |class-mean Delta| {mx:+.4f}; needed +0.30 to +0.47)")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
